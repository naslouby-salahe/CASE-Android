"""Small deployment-motivated FL POC: paired emulator/device Android malware.

Clients are explicitly simulated context silos (emulator, physical-device
collection), not independent organizations or privacy owners. APK hashes are
grouped once across both clients into train/calibration/test so the same APK
never crosses a split. Raw archive bytes and rows remain in memory; only
aggregate JSON metrics are written.
"""
from __future__ import annotations

import io
import json
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (balanced_accuracy_score, brier_score_loss,
                             confusion_matrix, f1_score, roc_auc_score,
                             roc_curve)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


URLS = {
    "emulator_benign": "https://raw.githubusercontent.com/aleguma/kronodroid/main/emulator/emu_legitimate_v1.zip",
    "emulator_malware": "https://raw.githubusercontent.com/aleguma/kronodroid/main/emulator/emu_malware_v1.zip",
    "device_benign": "https://raw.githubusercontent.com/aleguma/kronodroid/main/real_device/real_legitimate_v1.zip",
    "device_malware": "https://raw.githubusercontent.com/aleguma/kronodroid/main/real_device/real_malware_v1.zip",
}
SEEDS = [20260923, 314159, 42]
ROUNDS = 12
LOCAL_EPOCHS = 1
BATCH = 1024
LR = 0.03
PROX_MU = 0.1
DEVICE = torch.device("cpu")
torch.set_num_threads(2)


def read_zip(url: str) -> tuple[pd.DataFrame, int]:
    req = urllib.request.Request(url, headers={"User-Agent": "CASE-Android audit"})
    raw = urllib.request.urlopen(req, timeout=90).read()
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        csvs = [x for x in zf.namelist() if x.lower().endswith(".csv")]
        if len(csvs) != 1:
            raise ValueError(f"expected one CSV, found {csvs}")
        with zf.open(csvs[0]) as stream:
            return pd.read_csv(stream, low_memory=False), len(raw)


def metrics(y: np.ndarray, p: np.ndarray, threshold: float = 0.5) -> dict:
    yhat = (p >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, yhat, labels=[0, 1]).ravel()
    return {
        "n": int(len(y)), "prevalence": float(y.mean()),
        "auc": float(roc_auc_score(y, p)),
        "balanced_accuracy": float(balanced_accuracy_score(y, yhat)),
        "macro_f1": float(f1_score(y, yhat, average="macro", zero_division=0)),
        "fpr": float(fp / max(1, fp + tn)),
        "fnr": float(fn / max(1, fn + tp)),
        "brier": float(brier_score_loss(y, p)),
        "threshold": float(threshold),
    }


def youden_threshold(y: np.ndarray, p: np.ndarray) -> float:
    fpr, tpr, thresholds = roc_curve(y, p)
    score = tpr - fpr
    candidates = np.flatnonzero(score == np.max(score))
    # Fixed deterministic tie rule: choose the candidate closest to 0.5.
    idx = candidates[np.argmin(np.abs(thresholds[candidates] - 0.5))]
    return float(thresholds[idx])


def fit_sklearn(x: np.ndarray, y: np.ndarray) -> LogisticRegression:
    return LogisticRegression(C=1.0, max_iter=500, solver="lbfgs")


def fit_federated(xs: list[np.ndarray], ys: list[np.ndarray], seed: int,
                  prox_mu: float = 0.0) -> torch.nn.Linear:
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    dim = xs[0].shape[1]
    global_model = torch.nn.Linear(dim, 1, bias=True).to(DEVICE)
    loss_fn = torch.nn.BCEWithLogitsLoss()
    tx = [torch.as_tensor(x, dtype=torch.float32, device=DEVICE) for x in xs]
    ty = [torch.as_tensor(y[:, None], dtype=torch.float32, device=DEVICE) for y in ys]
    sizes = np.asarray([len(y) for y in ys], dtype=float)

    for _round in range(ROUNDS):
        base = {k: v.detach().clone() for k, v in global_model.state_dict().items()}
        client_states = []
        for client in range(len(xs)):
            local = torch.nn.Linear(dim, 1, bias=True).to(DEVICE)
            local.load_state_dict(base)
            opt = torch.optim.SGD(local.parameters(), lr=LR)
            n = len(ys[client])
            for _epoch in range(LOCAL_EPOCHS):
                order = rng.permutation(n)
                for start in range(0, n, BATCH):
                    ix = torch.as_tensor(order[start:start+BATCH], dtype=torch.long, device=DEVICE)
                    opt.zero_grad(set_to_none=True)
                    logits = local(tx[client][ix])
                    loss = loss_fn(logits, ty[client][ix])
                    if prox_mu:
                        prox = sum(torch.sum((p - base[name]) ** 2)
                                   for name, p in local.named_parameters())
                        loss = loss + (prox_mu / 2.0) * prox
                    loss.backward()
                    opt.step()
            client_states.append({k: v.detach().clone() for k, v in local.state_dict().items()})

        total = sizes.sum()
        avg = {k: sum(client_states[j][k] * (sizes[j] / total)
                      for j in range(len(xs))) for k in base}
        global_model.load_state_dict(avg)
    global_model.eval()
    return global_model


def torch_predict(model: torch.nn.Linear, x: np.ndarray) -> np.ndarray:
    with torch.no_grad():
        t = torch.as_tensor(x, dtype=torch.float32, device=DEVICE)
        return torch.sigmoid(model(t)).cpu().numpy().ravel()


def context_heterogeneity(xe: np.ndarray, xd: np.ndarray, ye: np.ndarray,
                          yd: np.ndarray, names: list[str]) -> dict:
    pe, pdv = (xe > 0), (xd > 0)
    p1 = pe.mean(axis=0).clip(1e-8, 1-1e-8)
    p2 = pdv.mean(axis=0).clip(1e-8, 1-1e-8)
    m = (p1 + p2) / 2
    def kl(a, b):
        return a*np.log(a/b) + (1-a)*np.log((1-a)/(1-b))
    js = 0.5*kl(p1, m) + 0.5*kl(p2, m)
    agreement = (pe == pdv).mean(axis=0)
    change = np.abs(p1-p2)
    order = np.argsort(-change)[:12]
    return {
        "client_count": 2,
        "client_ids": ["emulator", "physical_device_collection"],
        "client_rows": {"emulator": int(len(ye)), "physical_device_collection": int(len(yd))},
        "label_prevalence": {"emulator": float(ye.mean()), "physical_device_collection": float(yd.mean())},
        "label_prevalence_absolute_gap": float(abs(ye.mean()-yd.mean())),
        "feature_binary_marginal_mean_abs_gap": float(np.mean(change)),
        "feature_binary_marginal_max_abs_gap": float(np.max(change)),
        "mean_feature_bernoulli_js_nats": float(np.mean(js)),
        "mean_paired_feature_presence_agreement": float(np.mean(agreement)),
        "top_shifted_features": [{"feature": names[i], "emulator_presence": float(p1[i]),
                                  "device_presence": float(p2[i]), "abs_gap": float(change[i]),
                                  "paired_presence_agreement": float(agreement[i])} for i in order],
    }


def one_seed(seed: int, xe0: np.ndarray, xd0: np.ndarray, y: np.ndarray,
             hashes: np.ndarray, names: list[str]) -> dict:
    # One identity-level split is applied to both contexts.
    g1 = GroupShuffleSplit(n_splits=1, test_size=0.15, random_state=seed)
    trcal_ix, test_ix = next(g1.split(np.zeros(len(hashes)), y, groups=hashes))
    g2 = GroupShuffleSplit(n_splits=1, test_size=0.17647058823529413, random_state=seed+71)
    tr_rel, cal_rel = next(g2.split(np.zeros(len(trcal_ix)), y[trcal_ix], groups=hashes[trcal_ix]))
    train_ix, cal_ix = trcal_ix[tr_rel], trcal_ix[cal_rel]
    # Calibration/test identities are disjoint from training and each other.
    xe_log, xd_log = np.log1p(np.maximum(xe0, 0)), np.log1p(np.maximum(xd0, 0))
    scaler = StandardScaler().fit(np.vstack([xe_log[train_ix], xd_log[train_ix]]))
    xe, xd = scaler.transform(xe_log), scaler.transform(xd_log)

    Xtrain = [xe[train_ix], xd[train_ix]]
    Ytrain = [y[train_ix], y[train_ix]]
    clients_test = [xe[test_ix], xd[test_ix]]
    y_test = y[test_ix]
    clients_cal = [xe[cal_ix], xd[cal_ix]]
    y_cal = y[cal_ix]

    # Centralized, local-only, cross-context transfer, FedAvg and FedProx.
    central = fit_sklearn(np.vstack(Xtrain), np.concatenate(Ytrain)).fit(np.vstack(Xtrain), np.concatenate(Ytrain))
    local_models = [fit_sklearn(Xtrain[i], Ytrain[i]).fit(Xtrain[i], Ytrain[i]) for i in range(2)]
    p_central = [central.predict_proba(x)[:, 1] for x in clients_test]
    p_local = [local_models[i].predict_proba(clients_test[i])[:, 1] for i in range(2)]
    p_transfer = [local_models[1].predict_proba(clients_test[0])[:, 1],
                  local_models[0].predict_proba(clients_test[1])[:, 1]]
    fedavg = fit_federated(Xtrain, Ytrain, seed, 0.0)
    fedprox = fit_federated(Xtrain, Ytrain, seed, PROX_MU)
    p_avg = [torch_predict(fedavg, x) for x in clients_test]
    p_prox = [torch_predict(fedprox, x) for x in clients_test]

    # CASE-derived feature portability: select using only paired training APKs.
    train_agreement = ((xe0[train_ix] > 0) == (xd0[train_ix] > 0)).mean(axis=0)
    keep = np.argsort(-train_agreement, kind="stable")[:max(1, len(names)//2)]
    fed_port = fit_federated([Xtrain[0][:, keep], Xtrain[1][:, keep]], Ytrain, seed+101, 0.0)
    p_port = [torch_predict(fed_port, x[:, keep]) for x in clients_test]

    # Client-specific operating thresholds are selected on held-out calibration APKs.
    cal_avg = [torch_predict(fedavg, x) for x in clients_cal]
    global_thr = youden_threshold(np.concatenate([y_cal, y_cal]), np.concatenate(cal_avg))
    client_thr = [youden_threshold(y_cal, cal_avg[i]) for i in range(2)]

    def eval_clients(preds, thresholds=None):
        thresholds = thresholds or [0.5, 0.5]
        return {"emulator": metrics(y_test, preds[0], thresholds[0]),
                "physical_device_collection": metrics(y_test, preds[1], thresholds[1]),
                "macro_brier": float(np.mean([brier_score_loss(y_test, p) for p in preds])),
                "macro_balanced_accuracy": float(np.mean([balanced_accuracy_score(y_test, p >= thresholds[i]) for i,p in enumerate(preds)])),
                "worst_client_balanced_accuracy": float(np.min([balanced_accuracy_score(y_test, p >= thresholds[i]) for i,p in enumerate(preds)])),
                "fpr_gap": float(abs(metrics(y_test, preds[0], thresholds[0])["fpr"] - metrics(y_test, preds[1], thresholds[1])["fpr"])),
                "fnr_gap": float(abs(metrics(y_test, preds[0], thresholds[0])["fnr"] - metrics(y_test, preds[1], thresholds[1])["fnr"]))}

    return {
        "seed": seed, "apk_groups": {"train": int(len(train_ix)), "calibration": int(len(cal_ix)), "test": int(len(test_ix))},
        "centralized": eval_clients(p_central),
        "local_only": eval_clients(p_local),
        "cross_context_transfer": eval_clients(p_transfer),
        "fedavg": eval_clients(p_avg),
        "fedprox": eval_clients(p_prox),
        "fedavg_top_half_portable_features": eval_clients(p_port),
        "fedavg_calibration": {
            "global_threshold": global_thr,
            "client_thresholds": {"emulator": client_thr[0], "physical_device_collection": client_thr[1]},
            "global_threshold_metrics": eval_clients(p_avg, [global_thr, global_thr]),
            "client_threshold_metrics": eval_clients(p_avg, client_thr),
        },
        "training_feature_portability": {
            "selected_count": int(len(keep)), "feature_names": [names[i] for i in keep],
            "median_presence_agreement_all": float(np.median(train_agreement)),
            "selected_mean_presence_agreement": float(np.mean(train_agreement[keep])),
        },
    }


def main(out_path: str) -> None:
    frames, archive_bytes = {}, {}
    for name, url in URLS.items():
        frames[name], archive_bytes[name] = read_zip(url)
    em = pd.concat([frames["emulator_benign"], frames["emulator_malware"]], ignore_index=True)
    de = pd.concat([frames["device_benign"], frames["device_malware"]], ignore_index=True)
    hcol_e = next(c for c in em.columns if str(c).lower() == "sha256")
    hcol_d = next(c for c in de.columns if str(c).lower() == "sha256")
    # Current CSV schema: first two fields are package and label; syscall columns
    # occupy positions 2:291, with nr_syscalls removed as an aggregate.
    cand_e, cand_d = list(em.columns[2:291]), list(de.columns[2:291])
    feat_names = [c for c in cand_e if c != "nr_syscalls" and c in cand_d]
    if len(feat_names) != 288:
        raise ValueError(f"expected 288 aligned syscall features, got {len(feat_names)}")
    def unique_valid(df, hcol):
        z = df.copy()
        z["_hash"] = z[hcol].astype(str).str.lower().str.strip()
        z = z[~z["_hash"].duplicated(keep=False)].copy()
        return z
    em, de = unique_valid(em, hcol_e), unique_valid(de, hcol_d)
    overlap = sorted(set(em["_hash"]) & set(de["_hash"]))
    em = em.set_index("_hash").loc[overlap]
    de = de.set_index("_hash").loc[overlap]
    label_e = pd.to_numeric(em["Malware"], errors="raise").astype(int).to_numpy()
    label_d = pd.to_numeric(de["Malware"], errors="raise").astype(int).to_numpy()
    if not np.array_equal(label_e, label_d):
        raise ValueError("malware labels disagree among valid paired hashes")
    xe = em[feat_names].apply(pd.to_numeric, errors="coerce").fillna(0).to_numpy(dtype=np.float32)
    xd = de[feat_names].apply(pd.to_numeric, errors="coerce").fillna(0).to_numpy(dtype=np.float32)
    # Hashes are used only for identity-level grouping, never predictors.
    hashes = np.asarray(overlap)
    prevalence = float(label_e.mean())
    result = {
        "id": "KFL-CONTEXT-01", "dataset": "KronoDroid public CSV release",
        "client_construction": "Two simulated clients: emulator and real-device collection contexts. These are deployment-motivated context domains, not independent data owners or privacy silos.",
        "identity_split": "APK SHA groups held out consistently across both contexts; exact same APKs may appear at both clients only within the same partition.",
        "sample": {"unique_paired_apks": int(len(hashes)), "features": len(feat_names),
                   "feature_definition": "released syscall counts, log1p transform; nr_syscalls aggregate excluded",
                   "label": "released Malware field (0 benign, 1 malware)", "malware_prevalence": prevalence,
                   "archive_bytes_downloaded_in_memory": archive_bytes},
        "heterogeneity_all_paired_apks_descriptive": None,
        "seeds": [],
        "protocol": {"split": "70/15/15 identity groups for train/calibration/test (approx.)",
                     "seeds": SEEDS, "federated_rounds": ROUNDS, "local_epochs": LOCAL_EPOCHS,
                     "batch_size": BATCH, "optimizer": "SGD", "learning_rate": LR,
                     "FedProx_mu": PROX_MU, "calibration": "Youden threshold on calibration identities; global vs per-client, no test tuning"},
        "caveats": ["one dataset; two clients only", "client identity is context, not organization",
                    "older APK cohort; family labels are known inconsistent and excluded",
                    "centralized preprocessing scaler uses train rows from both clients, so this is not a privacy-preserving implementation",
                    "exploratory POC only; no secure aggregation or adversarial clients"],
    }
    result["heterogeneity_all_paired_apks_descriptive"] = context_heterogeneity(xe, xd, label_e, label_d, feat_names)
    for seed in SEEDS:
        result["seeds"].append(one_seed(seed, xe, xd, label_e, hashes, feat_names))
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(p), "paired_apks": len(hashes), "features": len(feat_names),
                      "seeds": SEEDS, "archive_bytes": archive_bytes}, indent=2))


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        raise SystemExit("usage: kronodroid_fl_context_poc.py OUTPUT.json")
    main(sys.argv[1])
