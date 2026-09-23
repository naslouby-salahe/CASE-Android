"""Exploratory SELENE source-positive recurrence audit.

Run from WSL with:
  python3 docs/poc/temp/selene_poc.py /home/naslouby/Projects/datp-shared-data/raw/SELENE

The script uses only released compact Parquet files and writes aggregate JSON
to stdout. It never prints app identities or raw trace text.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline


ROOT = Path(sys.argv[1])
BOOLS = [
    "has_NETWORK_EXTERNAL", "has_NETWORK_LOCAL", "has_BINDER_IPC",
    "has_TLS_CERT_ACTIVITY", "has_APP_PRIVATE_FILE_ACTIVITY", "has_PROC_ACCESS",
    "has_MEMORY_EXEC", "has_ENV_CHECK", "has_PROCESS_ACTIVITY",
    "has_PROCESS_MEMORY_READ", "has_WAIT_ACTIVITY", "has_ERROR_PROBING",
    "has_tcp_443", "has_external_tcp", "has_app_private_db", "has_rwx_anon",
    "has_process_vm_readv", "has_app_private_db_high_volume",
    "has_error_probing_high_volume",
]
COUNT_MAP = {
    "has_NETWORK_EXTERNAL": "n_NETWORK_EXTERNAL",
    "has_NETWORK_LOCAL": "n_NETWORK_LOCAL", "has_BINDER_IPC": "n_BINDER_IPC",
    "has_TLS_CERT_ACTIVITY": "n_TLS_CERT_ACTIVITY",
    "has_APP_PRIVATE_FILE_ACTIVITY": "n_APP_PRIVATE_FILE_ACTIVITY",
    "has_PROC_ACCESS": "n_PROC_ACCESS", "has_MEMORY_EXEC": "n_MEMORY_EXEC",
    "has_ENV_CHECK": "n_ENV_CHECK", "has_PROCESS_ACTIVITY": "n_PROCESS_ACTIVITY",
    "has_PROCESS_MEMORY_READ": "n_PROCESS_MEMORY_READ", "has_WAIT_ACTIVITY": "n_WAIT_ACTIVITY",
    "has_ERROR_PROBING": "n_ERROR_PROBING", "has_tcp_443": "n_tcp_443",
    "has_external_tcp": "n_external_tcp", "has_app_private_db": "n_app_private_db",
    "has_rwx_anon": "n_rwx_anon", "has_process_vm_readv": "n_process_vm_readv",
    "has_app_private_db_high_volume": "n_app_private_db",
    "has_error_probing_high_volume": "n_error_probing",
}
VOLUME = ["duration_sec", "n_l1_events", "n_event_types", "n_medium_interest",
          "n_high_interest", "n_informational", "n_low_contextual", "l1_active_duration_sec"]


def metrics(y, p):
    p = np.clip(np.asarray(p, dtype=float), 1e-7, 1 - 1e-7)
    return {"brier": float(brier_score_loss(y, p)),
            "log_loss": float(log_loss(y, p, labels=[0, 1])),
            "ap": float(average_precision_score(y, p))}


def fixed_coverage(scores, y, groups, coverage):
    """Descriptive held-out risk/coverage; thresholds are not calibration-valid."""
    n_keep = max(1, int(round(len(y) * coverage)))
    cutoff = np.partition(scores, len(scores) - n_keep)[len(scores) - n_keep]
    above = scores > cutoff
    tied = scores == cutoff
    tie_fraction = float((n_keep - int(above.sum())) / max(1, int(tied.sum())))
    weight = above.astype(float) + tied.astype(float) * tie_fraction
    risk = float(np.sum(weight * (1 - y)) / max(weight.sum(), 1e-12))
    report_mean, report_any = [], []
    for group in np.unique(groups):
        ix = groups == group
        report_mean.append(float(np.sum(weight[ix] * (1 - y[ix]))))
        certain_bad = bool(np.any(above[ix] & (y[ix] == 0)))
        uncertain_bad = int(np.sum(tied[ix] & (y[ix] == 0)))
        report_any.append(1.0 if certain_bad else 1 - (1 - tie_fraction) ** uncertain_bad)
    return {"coverage": float(weight.mean()), "nonrecurrence_risk": risk,
            "recurrence_retention": float(np.sum(weight * y) / max(1, np.sum(y))),
            "mean_unsupported_claims_per_report": float(np.mean(report_mean)),
            "expected_reports_with_any_unsupported_transfer": float(np.mean(report_any)),
            "cutoff_tie_count": int(tied.sum()), "fractional_tie_selection": tie_fraction}


def load_pair():
    a10 = pd.read_parquet(ROOT / "data_run_features_android10.parquet")
    a14 = pd.read_parquet(ROOT / "data_run_features_android14.parquet")
    if a10.sha256.duplicated().any() or a14.sha256.duplicated().any():
        raise ValueError("run_features contains non-unique APK SHA-256 identities")
    a10 = a10.set_index("sha256", drop=False)
    a14 = a14.set_index("sha256", drop=False)
    ids = a10.index.intersection(a14.index)
    if not set(BOOLS).issubset(a10.columns) or not set(BOOLS).issubset(a14.columns):
        raise ValueError("expected 19 released Boolean claim columns")
    return a10, a14


def dataset_audit(a10, a14):
    ids10 = set(a10.sha256)
    ids14 = set(a14.sha256)
    paired = ids10 & ids14
    a10_pair = a10[a10.sha256.isin(paired)]
    a10_only = a10[~a10.sha256.isin(paired)]
    p10 = a10_pair.set_index("sha256").loc[sorted(paired)]
    p14 = a14[a14.sha256.isin(paired)].set_index("sha256").loc[sorted(paired)]
    deltas = {}
    four_state = {}
    for col in BOOLS:
        d = float(a10_pair[col].fillna(0).mean() - a10_only[col].fillna(0).mean())
        deltas[col] = d
        s = p10[col].fillna(0).astype(bool).to_numpy()
        t = p14[col].fillna(0).astype(bool).to_numpy()
        n00, n01 = int(np.sum(~s & ~t)), int(np.sum(~s & t))
        n10, n11 = int(np.sum(s & ~t)), int(np.sum(s & t))
        four_state[col] = {"n00_stable_absent": n00, "n01_target_emergent": n01,
                           "n10_source_only": n10, "n11_stable_present": n11,
                           "10_to_14_recurrence": n11 / (n11 + n10) if n11 + n10 else None,
                           "14_to_10_recurrence": n11 / (n11 + n01) if n11 + n01 else None,
                           "emergence_given_source_absent": n01 / (n00 + n01) if n00 + n01 else None}
    oracle10 = pd.read_parquet(ROOT / "data_fidelity_oracle_android10.parquet")
    oracle14 = pd.read_parquet(ROOT / "data_fidelity_oracle_android14.parquet")
    oracle_shared = set(oracle10.sha256) & set(oracle14.sha256)
    return {"run_feature_rows": {"android10": len(a10), "android14": len(a14)},
            "unique_hashes": {"android10": len(ids10), "android14": len(ids14),
                              "shared": len(paired), "android10_only": len(ids10 - ids14),
                              "android14_only": len(ids14 - ids10)},
            "package_groups": {"android10": int(a10.package_name.nunique(dropna=False)),
                               "android14": int(a14.package_name.nunique(dropna=False)),
                               "paired_android10": int(a10_pair.package_name.nunique(dropna=False)),
                               "android10_only": int(a10_only.package_name.nunique(dropna=False))},
            "android10_paired_minus_unpaired_indicator_prevalence": {
                "macro_absolute_difference": float(np.mean(np.abs(list(deltas.values())))),
                "max_absolute_difference": float(max(abs(x) for x in deltas.values())),
                "per_indicator": deltas},
            "paired_four_state_by_indicator": four_state,
            "fidelity_oracle": {"android10_rows": len(oracle10), "android14_rows": len(oracle14),
                                "unique_hashes_each": [int(oracle10.sha256.nunique()), int(oracle14.sha256.nunique())],
                                "shared_hashes": len(oracle_shared)}}


def evaluate(src, tgt):
    src = src.reset_index(drop=True)
    tgt = tgt.reset_index(drop=True)
    groups = src.package_name.fillna("<missing>").astype(str).to_numpy()
    ymat = tgt[BOOLS].fillna(0).astype(int).to_numpy()
    xbool = src[BOOLS].fillna(0).astype(float).to_numpy()
    count_cols = list(dict.fromkeys(COUNT_MAP.values()))
    xcounts = np.log1p(src[count_cols].fillna(0).clip(lower=0).astype(float)).to_numpy()
    elapsed = src.duration_sec.fillna(src.duration_sec.median()).clip(lower=1).to_numpy(dtype=float)
    xcounts_norm = np.log1p(src[count_cols].fillna(0).clip(lower=0).astype(float).to_numpy() / elapsed[:, None])
    xvol = np.log1p(src[VOLUME].fillna(0).clip(lower=0).astype(float)).to_numpy()
    xrich = np.concatenate([xbool, xcounts, xvol], axis=1)
    xrich_norm = np.concatenate([xbool, xcounts_norm, xvol], axis=1)
    xevidence = xcounts
    n = len(src)
    claim_idx = np.argwhere(src[BOOLS].fillna(0).astype(int).to_numpy() == 1)
    app_idx, ind_idx = claim_idx[:, 0], claim_idx[:, 1]
    y = ymat[app_idx, ind_idx]
    g = groups[app_idx]
    claim_onehot = np.eye(len(BOOLS))[ind_idx]
    xb, xr, xrn, xe, xen, xv = (xbool[app_idx], xrich[app_idx], xrich_norm[app_idx],
                                xevidence[app_idx], xcounts_norm[app_idx], xvol[app_idx])
    # A single predeclared grouped holdout keeps this first discovery probe
    # tractable. The roadmap's repeated, calibrated OOF protocol remains future work.
    split_seed = int(os.environ.get("CASE_POC_SPLIT_SEED", "20260923"))
    tr, te = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=split_seed)
                  .split(np.zeros(len(y)), y, groups=g))
    prevalence = float(y[tr].mean())
    global_p = np.full(len(te), prevalence)
    per_ind = np.zeros(len(BOOLS), dtype=float)
    for j in range(len(BOOLS)):
        mask = ind_idx[tr] == j
        per_ind[j] = (y[tr][mask].sum() + 1.0) / (mask.sum() + 2.0)
    pers_p = per_ind[ind_idx[te]]
    bool_model = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=250, solver="liblinear"))
    evidence_model = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=250, solver="liblinear"))
    normalized_evidence_model = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=250, solver="liblinear"))
    volume_model = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=250, solver="liblinear"))
    rich_model = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=250, solver="liblinear"))
    rich_normalized_model = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=250, solver="liblinear"))
    bool_model.fit(np.concatenate([claim_onehot[tr], xb[tr]], axis=1), y[tr])
    evidence_model.fit(np.concatenate([claim_onehot[tr], xe[tr]], axis=1), y[tr])
    normalized_evidence_model.fit(np.concatenate([claim_onehot[tr], xen[tr]], axis=1), y[tr])
    volume_model.fit(np.concatenate([claim_onehot[tr], xv[tr]], axis=1), y[tr])
    rich_model.fit(np.concatenate([claim_onehot[tr], xr[tr]], axis=1), y[tr])
    rich_normalized_model.fit(np.concatenate([claim_onehot[tr], xrn[tr]], axis=1), y[tr])
    pred = {"global": global_p, "persistence": pers_p,
            "boolean": bool_model.predict_proba(np.concatenate([claim_onehot[te], xb[te]], axis=1))[:, 1],
            "evidence_count": evidence_model.predict_proba(np.concatenate([claim_onehot[te], xe[te]], axis=1))[:, 1],
            "normalized_evidence_count": normalized_evidence_model.predict_proba(np.concatenate([claim_onehot[te], xen[te]], axis=1))[:, 1],
            "activity_volume": volume_model.predict_proba(np.concatenate([claim_onehot[te], xv[te]], axis=1))[:, 1],
            "rich": rich_model.predict_proba(np.concatenate([claim_onehot[te], xr[te]], axis=1))[:, 1],
            "rich_normalized_counts": rich_normalized_model.predict_proba(np.concatenate([claim_onehot[te], xrn[te]], axis=1))[:, 1]}
    summary = {k: metrics(y[te], pred[k]) for k in pred}
    # Broken-pair control: permute target APK rows within held-out packages only.
    # Source features and model scores remain fixed; only the target pairing is broken.
    test_app_ids = np.unique(app_idx[te])
    rng = np.random.default_rng(4451)
    permuted_apps = rng.permutation(test_app_ids)
    app_to_perm = dict(zip(test_app_ids, permuted_apps))
    broken_y = np.asarray([ymat[app_to_perm[a], j] for a, j in zip(app_idx[te], ind_idx[te])])
    broken = {k: metrics(broken_y, p) for k, p in pred.items()}
    # Package-clustered paired bootstrap of absolute Brier improvements vs persistence.
    rng = np.random.default_rng(7252026)
    y_test = y[te]
    g_test = g[te]
    p_test = {k: pred[k] for k in pred}
    unique = np.unique(g_test)
    deltas = {k: [] for k in ["boolean", "evidence_count", "normalized_evidence_count",
                              "activity_volume", "rich", "rich_normalized_counts"]}
    pkg_rows = {u: np.flatnonzero(g_test == u) for u in unique}
    # 300 replicates provide a discovery-stage interval at low compute cost;
    # the frozen study should use the roadmap's larger bootstrap count.
    for _ in range(300):
        draw = rng.choice(unique, size=len(unique), replace=True)
        ix = np.concatenate([pkg_rows[u] for u in draw])
        base = brier_score_loss(y_test[ix], p_test["persistence"][ix])
        for k in deltas:
            deltas[k].append(base - brier_score_loss(y_test[ix], p_test[k][ix]))
    ci = {k: [float(np.quantile(v, .025)), float(np.quantile(v, .975))]
          for k, v in deltas.items()}
    # Pooled test-stratum counts, with repeated claims retained as distinct rows.
    per_indicator = {}
    for j, name in enumerate(BOOLS):
        ix = ind_idx == j
        per_indicator[name] = {"n_source_positive": int(ix.sum()),
                               "recurrence": float(y[ix].mean()) if ix.any() else None,
                               "positive_rate_target_all_pairs": float(ymat[:, j].mean())}
    selective = {method: {str(cov): fixed_coverage(pred[method], y_test, app_idx[te], cov)
                         for cov in [.5, .8]}
                 for method in ["persistence", "boolean", "rich"]}
    return {"n_pairs": n, "n_claims": int(len(y)), "n_packages_in_holdout": int(len(unique)),
            "n_packages_overall": int(len(set(groups))),
            "recurrence": float(y.mean()), "support_by_indicator": per_indicator,
            "grouped_holdout": {"seed": split_seed, "train_claims": int(len(tr)), "test_claims": int(len(te)),
                                 "train_packages": int(len(set(g[tr]))), "test_packages": int(len(set(g[te]))),
                                 "metrics": {k: metrics(y[te], pred[k]) for k in pred}},
            "holdout_metrics": summary,
            "brier_skill_vs_persistence": {
                k: float(1 - summary[k]["brier"] / summary["persistence"]["brier"])
                for k in ["global", "boolean", "evidence_count", "normalized_evidence_count", "activity_volume", "rich", "rich_normalized_counts"]},
            "paired_cluster_bootstrap_ci_brier_improvement_vs_persistence": ci,
            "broken_pair_negative_control": {"metrics_after_test_target_app_permutation": broken,
                "brier_improvement_vs_persistence": {
                    k: float(broken["persistence"]["brier"] - broken[k]["brier"])
                    for k in ["boolean", "evidence_count", "normalized_evidence_count",
                              "activity_volume", "rich", "rich_normalized_counts"]}},
            "descriptive_selective_and_report_metrics": selective,
            "metric_scope_note": "Grouped holdout is discovery only; fixed coverage uses held-out ranks, and cluster bootstrap uses 300 packages draws."}


def main():
    a10, a14 = load_pair()
    if len(sys.argv) > 2 and sys.argv[2] == "--audit-only":
        print(json.dumps(dataset_audit(a10, a14), indent=2, allow_nan=False))
        return
    ids = set(a10.sha256) & set(a14.sha256)
    p10 = a10[a10.sha256.isin(ids)].copy()
    p14 = a14[a14.sha256.isin(ids)].copy()
    p10 = p10.set_index("sha256").loc[sorted(ids)].reset_index()
    p14 = p14.set_index("sha256").loc[sorted(ids)].reset_index()
    out = {"input": str(ROOT), "boolean_indicators": BOOLS,
           "dataset_audit": dataset_audit(a10, a14),
           "direction_10_to_14": evaluate(p10, p14),
           "direction_14_to_10": evaluate(p14, p10)}
    print(json.dumps(out, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
