# PoC audit checkpoint

Checkpoint: 2026-09-23. Primary task is the broad pre-implementation audit. No changes have been made to `docs/Roadmap.md` or `docs/technical_doc.md`.

## Idempotency / state

- Initial `docs/poc/` did not exist. Current authoritative outputs are `Dataset Audit.md`, `Novelty Audit.md`, `PoC Matrix.md`, `Claim and Gate Audit.md`, and `Final Report.md`.
- Data and result scripts live in this `temp/` directory. No raw dataset rows or archives were copied into the repository.
- SELENE inputs are read from `/home/naslouby/Projects/datp-shared-data/raw/SELENE` (external shared cache). KronoDroid CSV archives were streamed from GitHub into memory, then released. The JSON outputs contain schema/aggregate metadata only.
- Both CASE-Android RQ/metric groups use the source-positive processed-flag recurrence estimand. Claims concern recorded observations only.
- Temporary work has completed; no analysis process should still be running.

## Commands and outputs

SELENE descriptive/model PoC:

```text
python3 docs/poc/temp/selene_poc.py /home/naslouby/Projects/datp-shared-data/raw/SELENE
CASE_POC_SPLIT_SEED=314159 python3 docs/poc/temp/selene_poc.py /home/naslouby/Projects/datp-shared-data/raw/SELENE
python3 docs/poc/temp/selene_poc.py /home/naslouby/Projects/datp-shared-data/raw/SELENE --audit-only
```

Run from WSL repo root `/home/naslouby/Projects/CASE-Android`. Model split seeds: 20260923 (default) and 314159; 80/20 package-grouped holdout, separate direction models, one split per seed. The default rich model uses released source Boolean flags + log1p raw count fields + log1p volume/duration features. Also attempted Boolean-only, count-only, duration-normalized count-only, activity-volume-only, raw rich and normalized-count rich variants. Each main split uses 300 package-cluster bootstrap resamples. This is discovery, not confirmation.

Outputs:

- `selene_poc_results.json` — seed 20260923, both directions, all model variants, pair and report diagnostics.
- `selene_poc_split314159.json` — alternate valid grouped split seed, same protocol.
- `selene_pair_audit.json` — all paired/unpaired count and per-indicator four-state tables.
- `selene_poc.py` — reproducible analysis; no raw sample rows are written.

KronoDroid artifact PoC:

```text
python3 docs/poc/temp/kronodroid_audit.py
```

The script downloads these four URLs in memory and writes aggregate JSON only:

- `https://raw.githubusercontent.com/aleguma/kronodroid/main/emulator/emu_legitimate_v1.zip`
- `https://raw.githubusercontent.com/aleguma/kronodroid/main/emulator/emu_malware_v1.zip`
- `https://raw.githubusercontent.com/aleguma/kronodroid/main/real_device/real_legitimate_v1.zip`
- `https://raw.githubusercontent.com/aleguma/kronodroid/main/real_device/real_malware_v1.zip`

Compressed size: 25,679,248 bytes; expanded CSV size: 160,108,784 bytes; 142,128 rows over four archives. The run took about 10 seconds in current WSL. Peak RAM was not measured.

## SELENE input checksums

All eight files below were checked with SHA-256 during this audit; each input was immutable for the recorded PoCs.

| File | Bytes | SHA-256 |
|---|---:|---|
| `data_analyses_android10.parquet` | 3,876,547 | `5F3173ED902487C6FF50273E4ACEA96747B935EE053176833C4004DDF6B64EA7` |
| `data_analyses_android14.parquet` | 2,686,400 | `AB52F0A02974FBB97F29DB2598F6EA9505D93704CDF232F628CE1E0A525FCC54` |
| `data_fidelity_evidence_android10.parquet` | 1,237,029 | `107BCAE2B1D007953E575A250F42F293EFA6DC31700E259B7546177097072E88` |
| `data_fidelity_evidence_android14.parquet` | 1,545,721 | `918D55A30EEC94493EA5A5631B6D936721FE3B2A586E975AD4DB132C9F777374` |
| `data_fidelity_oracle_android10.parquet` | 1,389,463 | `6447336AE6C40424EC7751879DA1E24FF33CEE9D1A9BAD65495D79DBB17B139C` |
| `data_fidelity_oracle_android14.parquet` | 1,755,546 | `5E25A9325F1C80E9DDE1F10F0689EF06564AD608E3FB06BDAE882340BD51DA9B` |
| `data_run_features_android10.parquet` | 9,990,871 | `56C90C45A6742EEAC340EBD7369761EE643E38CFA5A86A4DB1A9F678F28C1C20` |
| `data_run_features_android14.parquet` | 7,296,134 | `64CFCD3BF0D5CCB3F7AA95B76E262EFF11CF3B0BF00524A8D1A95880D68B4334` |

## Literature and dataset pages already checked

- SELENE/ARTEMIS: https://huggingface.co/datasets/serrooT/selene-android-paper-artifacts and its README/license.
- AndroCT: https://zenodo.org/records/6336104, README preview, and DOI `10.1109/MSR52588.2021.00076`.
- KronoDroid: https://github.com/aleguma/kronodroid and DOI `10.1016/j.cose.2021.102399`.
- Cross-device consistency: DOI `10.1016/j.mlwa.2022.100357`.
- Same App, Different Behaviors: https://arxiv.org/abs/2406.09807.
- CIC-InvesAndMal2019 official page: https://www.unb.ca/cic/datasets/invesandmal2019.html.
- DYNAMISM current restricted Zenodo record: https://zenodo.org/records/21280255.
- TraceDroid: https://zenodo.org/records/3665877.
- Learn Then Test: https://arxiv.org/abs/2110.01052; Conformal Risk Control: https://arxiv.org/abs/2208.02814.

## Unresolved assumptions and next steps

1. Verify exact current SELENE/ARTEMIS license text and mandatory citation files before data redistribution/publication.
2. Audit the live SELENE public artifact version against the eight local cached files; event/lifecycle/context-rich layers were not present locally and were not downloaded.
3. Reconcile KronoDroid’s 484 actual columns against the README statement of 200 static + 289 dynamic; keep `MalFamily` out until the 33,838 label disagreements are explained.
4. If AndroCT is reconsidered, first obtain the stated faculty/permanent-staff agreement, then verify archive member identifiers and exact one-to-one pairing before any feature extraction.
5. If DYNAMISM is reconsidered, request/verify access first; inspect failed-run bias and same-context run pair identities before estimating stochasticity.
6. If CIC reboot analysis is reconsidered, first resolve the 5,000 versus 5,491 row-count discrepancy and prove exact APK/run pairing across states.
7. After the roadmap is revised, freeze a confirmatory split/threshold/feature protocol before running outer-test claims. Do not label this exploratory run confirmatory.

## Attempted variants retained

SELENE: global, per-indicator persistence, Boolean pooled logistic, raw evidence-count-only, duration-normalized evidence-count-only, activity-volume-only, rich raw count+volume, rich duration-normalized counts; two split seeds; both directions; broken-target-pair control; test-ranked 50%/80% coverage; paired-population differences; per-indicator 4-state transitions.

KronoDroid: schema/identity duplicate audit; label agreement; 288 call fields plus aggregate check; emulator→device and device→emulator; benign/malware strata; support≥100 feature-macro recurrence; broken-pair row permutation. No source-only model is fitted on KronoDroid in this pass.
