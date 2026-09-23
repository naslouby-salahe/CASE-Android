"""Inspect public KronoDroid CSVs in memory; raw archives are not retained."""
from __future__ import annotations

import io
import json
import urllib.request
import zipfile

import numpy as np
import pandas as pd

FILES = {
    "emulator_benign": "https://raw.githubusercontent.com/aleguma/kronodroid/main/emulator/emu_legitimate_v1.zip",
    "emulator_malware": "https://raw.githubusercontent.com/aleguma/kronodroid/main/emulator/emu_malware_v1.zip",
    "device_benign": "https://raw.githubusercontent.com/aleguma/kronodroid/main/real_device/real_legitimate_v1.zip",
    "device_malware": "https://raw.githubusercontent.com/aleguma/kronodroid/main/real_device/real_malware_v1.zip",
}


def read_archive(url):
    request = urllib.request.Request(url, headers={"User-Agent": "CASE-Android research audit"})
    data = urllib.request.urlopen(request, timeout=60).read()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = [n for n in archive.namelist() if n.lower().endswith(".csv")]
        if len(names) != 1:
            raise ValueError(f"expected one CSV in archive, found {names}")
        csv_bytes = archive.getinfo(names[0]).file_size
        with archive.open(names[0]) as f:
            df = pd.read_csv(f, low_memory=False)
    return df, len(data), csv_bytes, names[0]


def main():
    frames, file_meta = {}, {}
    for name, url in FILES.items():
        frames[name], size, csv_size, member = read_archive(url)
        file_meta[name] = {"download_bytes": size, "csv_member": member,
                           "extracted_csv_bytes": csv_size,
                           "rows": len(frames[name]), "columns": len(frames[name].columns),
                           "column_names": list(map(str, frames[name].columns))}
    all_frames = {
        "emulator": pd.concat([frames["emulator_benign"], frames["emulator_malware"]], ignore_index=True),
        "device": pd.concat([frames["device_benign"], frames["device_malware"]], ignore_index=True),
    }
    out = {"files": file_meta, "contexts": {}}
    for context, df in all_frames.items():
        hash_cols = [c for c in df.columns if any(t in str(c).lower() for t in ["sha256", "sha-256", "hash", "md5"]) ]
        time_cols = [c for c in df.columns if any(t in str(c).lower() for t in ["date", "time", "year"]) ]
        label_cols = [c for c in df.columns if any(t in str(c).lower() for t in ["label", "class", "family", "malware"]) ]
        df_hash = df[hash_cols[0]].astype(str).str.lower().str.strip() if hash_cols else None
        out["contexts"][context] = {
            "rows": len(df), "columns": len(df.columns), "candidate_hash_columns": hash_cols,
            "candidate_time_columns": time_cols, "candidate_label_columns": label_cols,
            "hash_nonmissing": int(df_hash.notna().sum()) if df_hash is not None else 0,
            "hash_unique": int(df_hash.nunique()) if df_hash is not None else 0,
            "duplicate_hash_rows": int(df_hash.duplicated().sum()) if df_hash is not None else None,
            "missing_cells": int(df.isna().sum().sum()),
            "family_values_sample": {c: list(map(str, df[c].dropna().astype(str).unique()[:12])) for c in label_cols},
            "dynamic_feature_candidates": [str(c) for c in df.columns[:291]],
        }
    device_hash = next((c for c in all_frames["device"].columns if str(c).lower() in {"sha256", "sha-256", "md5", "hash"}), None)
    emu_hash = next((c for c in all_frames["emulator"].columns if str(c).lower() in {"sha256", "sha-256", "md5", "hash"}), None)
    out["pairing"] = {"emulator_identity_column": emu_hash, "device_identity_column": device_hash}
    if emu_hash and device_hash:
        e = all_frames["emulator"][emu_hash].astype(str).str.lower().str.strip()
        d = all_frames["device"][device_hash].astype(str).str.lower().str.strip()
        em = all_frames["emulator"].assign(_hash=e)
        dm = all_frames["device"].assign(_hash=d)
        overlap = set(e) & set(d)
        eu = em[~em._hash.duplicated(keep=False)]
        du = dm[~dm._hash.duplicated(keep=False)]
        valid_overlap = set(eu._hash) & set(du._hash)
        label_check = eu[eu._hash.isin(valid_overlap)][["_hash", "Malware", "MalFamily"]].merge(
            du[du._hash.isin(valid_overlap)][["_hash", "Malware", "MalFamily"]],
            on="_hash", suffixes=("_emu", "_device"), validate="one_to_one")
        dynamic_e = list(all_frames["emulator"].columns[2:291])
        dynamic_d = list(all_frames["device"].columns[2:291])
        feature_agreement = {}
        ordered_hashes = sorted(valid_overlap)
        emat = eu.set_index("_hash").reindex(ordered_hashes)
        dmat = du.set_index("_hash").reindex(ordered_hashes)
        for col in dynamic_e:
            if col in dynamic_d:
                lhs = pd.to_numeric(emat[col], errors="coerce").fillna(0).to_numpy()
                rhs = pd.to_numeric(dmat[col], errors="coerce").fillna(0).to_numpy()
                feature_agreement[col] = float(np.mean(lhs == rhs))
        syscall_cols = [c for c in dynamic_e if c not in {"nr_syscalls"}]
        emat = emat[syscall_cols].apply(pd.to_numeric, errors="coerce").fillna(0).to_numpy()
        dmat = dmat[syscall_cols].apply(pd.to_numeric, errors="coerce").fillna(0).to_numpy()
        y_e = emat > 0
        y_d = dmat > 0
        malware = pd.to_numeric(emat_df := eu.set_index("_hash").reindex(ordered_hashes)["Malware"], errors="coerce").fillna(0).to_numpy().astype(int)
        def direction_summary(source, target):
            n11 = int(np.sum(source & target))
            n10 = int(np.sum(source & ~target))
            source_pos = int(np.sum(source))
            per_feature_support = source.sum(axis=0)
            per_feature_recur = (source & target).sum(axis=0) / np.maximum(1, per_feature_support)
            source_counts = np.maximum(0, np.nan_to_num(np.asarray(source, dtype=float)))
            return {"source_positive_app_syscall_claims": source_pos,
                    "target_recurrence_pooled": n11 / source_pos if source_pos else None,
                    "source_only_fraction": n10 / source_pos if source_pos else None,
                    "four_state_counts_across_all_app_syscall_pairs": {
                        "n00": int(np.sum(~source & ~target)), "n01": int(np.sum(~source & target)),
                        "n10": n10, "n11": n11},
                    "syscall_macro_recurrence_all_features": float(np.mean(per_feature_recur)),
                    "syscall_macro_recurrence_support_ge_100": float(np.mean(per_feature_recur[per_feature_support >= 100])),
                    "top_feature_support": int(np.max(per_feature_support)),
                    "malware_recurrence": float(np.sum(source[malware == 1] & target[malware == 1]) / max(1, np.sum(source[malware == 1]))),
                    "benign_recurrence": float(np.sum(source[malware == 0] & target[malware == 0]) / max(1, np.sum(source[malware == 0])))}
        k_rng = np.random.default_rng(2033)
        perm = k_rng.permutation(len(ordered_hashes))
        broken_device = y_d[perm]
        broken_emu = y_e[perm]
        portability = {"emulator_to_device": direction_summary(y_e, y_d),
                       "device_to_emulator": direction_summary(y_d, y_e),
                       "broken_pair_control_emulator_to_device": direction_summary(y_e, broken_device),
                       "broken_pair_control_device_to_emulator": direction_summary(y_d, broken_emu)}
        dup_detail = {}
        for context, df, hcol in [("emulator", all_frames["emulator"], emu_hash), ("device", all_frames["device"], device_hash)]:
            dup = df[df[hcol].duplicated(keep=False)]
            dup_detail[context] = {"duplicate_rows": int(len(dup)),
                "duplicate_hash_groups": int(dup[hcol].nunique()),
                "duplicate_groups_with_conflicting_malware_label": int(sum(g.Malware.nunique(dropna=False) > 1 for _, g in dup.groupby(hcol)))}
        out["pairing"].update({"emulator_unique": int(e.nunique()), "device_unique": int(d.nunique()),
                               "intersecting_hashes": int(len(overlap)),
                               "one_to_one_pairs_after_duplicate_exclusion": int(len(valid_overlap)),
                               "emulator_only": int(len(set(e) - set(d))),
                               "device_only": int(len(set(d) - set(e))),
                               "unique_pair_malware_label_disagreements": int((label_check.Malware_emu != label_check.Malware_device).sum()),
                               "valid_pair_malware_benign_counts": {str(k): int(v) for k, v in label_check.Malware_emu.value_counts().items()},
                               "unique_pair_family_label_disagreements": int((label_check.MalFamily_emu != label_check.MalFamily_device).sum()),
                               "dynamic_feature_schema": {"emulator_289_fields": len(dynamic_e),
                                   "device_289_fields": len(dynamic_d), "same_ordered_schema": dynamic_e == dynamic_d,
                                   "feature_count_after_dropping_nr_syscalls": len(syscall_cols),
                                   "matching_feature_mean_value_agreement": float(np.mean(list(feature_agreement.values())))},
                               "archive_schema_differences": {
                                   "emulator_benign_vs_malware_columns": sorted(set(frames["emulator_benign"].columns) ^ set(frames["emulator_malware"].columns)),
                                   "device_benign_vs_malware_columns": sorted(set(frames["device_benign"].columns) ^ set(frames["device_malware"].columns)),
                                   "emulator_metadata_date_fields": [c for c in all_frames["emulator"].columns[291:] if "date" in str(c).lower()],
                                   "device_metadata_date_fields": [c for c in all_frames["device"].columns[291:] if "date" in str(c).lower()]},
                               "missing_dynamic_values": {
                                   "emulator": int(pd.concat([frames["emulator_benign"], frames["emulator_malware"]], ignore_index=True)[dynamic_e].isna().sum().sum()),
                                   "device": int(pd.concat([frames["device_benign"], frames["device_malware"]], ignore_index=True)[dynamic_d].isna().sum().sum())},
                               "syscall_portability_poC": portability,
                               "duplicate_hash_audit": dup_detail,
                               "valid_pair_family_agreement_rate": float(np.mean(label_check.MalFamily_emu == label_check.MalFamily_device)),
                               "dynamic_feature_per_column_agreement": feature_agreement})
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
