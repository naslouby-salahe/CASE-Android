# Candidate 2 — CASE-Android: Candidate Report (audit trail and evidence dossier)

Companion to [Roadmap.md](Roadmap.md). This file records what was checked, with which script and which output, and why each roadmap decision was made. Status vocabulary: `PASS`, `PARTIAL`, `MISSING`, `BLOCKED`, `REJECTED`, `SUPERSEDED`.

Paths are relative to `docs/Candidate 2/poc/` unless prefixed with `docs/poc/temp/` (archived exploratory workspace, kept unchanged) or `legacy/` (copies of the exploratory scripts and outputs for this candidate). Raw data live outside the repository (`CASE_RAW`, default `/home/naslouby/Projects/datp-shared-data/raw`; KronoDroid archives in `data/cache/krono`, git-ignored).

## Dashboard

| Item | Status | Summary |
|---|---|---|
| Overall status | **PASS with narrowed claims** | Defensible measurement chapter; several earlier statements were corrected or superseded (Section 9) |
| Chapter fit | PASS | Android dynamic-analysis reporting, cross-context reliability, calibrated scoping |
| PhD relevance | PARTIAL (explicit, not forced) | Heterogeneity, reliability of local evidence, calibration and threshold scope, worst-group performance, pooling versus per-group scope. Not an FL result and not IoT. Link is substantive on 4 themes, absent on FL and IoT proper |
| Dataset readiness | PASS (SELENE), PASS (KronoDroid, with schema caveats) | Files inspected, hashed, paired, leakage assertions pass; event layers and repeated runs unavailable |
| POC readiness | PASS | Package/family-grouped OOF prediction, calibration-only scoping, verification cost, cross-direction transfer, external replication run |
| Novelty confidence | MODERATE-LOW | Estimand, protocol and negative results are bounded contributions; closest work: cross-device studies, selective conformal risk control, an Android conformal filtering paper |
| Mechanism / headroom | PASS (headroom exists) | Logistic gains modest (Brier skill 4–9%); nonlinear comparator roughly doubles them (10–17%); a metadata-only baseline is competitive in one direction |
| Implementation readiness | PASS | Scripts, splits, assertions and stable rerun commands exist; confirmatory salts not yet run |
| Biggest remaining risk | Two named context pairs only; SELENE paper content not read (may already report cross-context differences); pairing-selection bias |

## 1. Inventory and mapping of pre-existing artifacts

Nothing was deleted. `docs/poc/` remains as the archival workspace; artifacts below were copied into `legacy/` for traceability.

| Artifact | Supports | Status | Note |
|---|---|---|---|
| `docs/Roadmap.md`, `docs/technical_doc.md` | Candidate 2 input | SUPERSEDED by [Roadmap.md](Roadmap.md) | Kept unchanged as the original CASE roadmap |
| `legacy/selene_poc.py`, `selene_poc_results.json`, `selene_poc_split314159.json`, `selene_pair_audit.json` | SELENE recurrence, four-state, broken pair | SUPERSEDED by `c2_selene.py prob` | Single 80/20 grouped split; results consistent within ±0.01 Brier skill of the 5-fold protocol (Section 9, item 4) |
| `legacy/p6_case_calibrated_policy.py`, `p6_case_calibrated_policy_results.json` | Calibration-only scoping | SUPERSEDED by `c2_selene.py scope` | Same qualitative result; new run adds UCB, family-conditioned baseline, worst-family and report metrics |
| `legacy/kronodroid_audit.py`, `kronodroid_audit.json` | KronoDroid schema, pairing | SUPERSEDED by `audit_krono.py` | Contained a NaN-comparison error (Section 9, item 1) |
| `legacy/kronodroid_fl_context_poc.py`, `..._results.json` | Two-client FL over emulator/device | REJECTED as FL line | Local-only beat FedAvg/FedProx; SHA-grouped (not package-grouped) split; kept as negative evidence |
| `docs/poc/Final Report.md`, `Research Matrix.md`, `Dataset & POC Audit.md`, `Novelty & Literature Audit.md`, `temp/progress.txt` | narrative and matrices | PRESERVED | Contain the P1–P70 candidate history; not edited |

## 2. Dataset Verification Matrix

### 2.1 SELENE / ARTEMIS compact features (`audit_selene.py` → `out/audit_selene.json`, `out/audit_selene.log`)

| Check | Expected | Actual | Status | Evidence | Consequence |
|---|---|---|---|---|---|
| Source and licence | Hugging Face `serrooT/selene-android-paper-artifacts`; dual licence | Live README: "SELENE Paper Artifacts Data License 1.0" plus upstream "ARTEMIS Dynamic Traces Data License 1.0"; derivatives and redistribution permitted subject to both; public outputs must cite both papers (ARTEMIS DOI 10.5753/sbseg.2025.11393; SELENE accepted SBSeg 2026, DOI pending) | PASS | web fetch of the README | Cite both; keep derived tables aggregate |
| Files present locally | 8 compact Parquet files | 8 files, 29.78 MB total: `analyses`, `run_features`, `fidelity_evidence`, `fidelity_oracle` × 2 contexts; SHA-256 recorded in audit JSON | PASS | audit JSON `files` | Compact families sufficient |
| Event/lifecycle layers | absent locally | absent (live README lists `events_l05`, `events_l1`, `lifecycle_events`, `context_*`, `table_04/05/07`) | BLOCKED (granularity lane) | `event_layers_present = []` | Granularity/lifecycle questions stay out; `table_*` configs not read (see risk R-11) |
| Row counts | 44,485 Android 10; 30,751 Android 14 | 44,485; 30,751; unique SHA = rows in both | PASS | audit | one run per APK per context |
| Paired APKs | 30,746 | 30,746 (13,739 Android-10-only) | PASS | audit `paired` | Inferential population |
| Repeated runs per APK | needed for run-to-run variance | none (one run per SHA per context) | BLOCKED | unique_sha = rows | Same-context stochasticity cannot be estimated |
| Schema | 82 columns in `run_features` | 82; 19 Boolean `has_*` columns; 18 count columns; 8 volume fields; `family`, `package_name`, `sha256`, `run_id` | PASS | schema dump | Column names listed in Roadmap |
| Missingness | none in identity columns | `package_name`, `family`, `sha256` complete; `time_to_first_*` 37–69% missing; `first_event_time` 0.1–2.5% missing | PASS | audit | time-to-first fields excluded as predictors |
| Timestamps | date or run-relative? | `first_event_time` values ≈ 12,000–53,000 with run durations 21–660 s: trace-clock values, not calendar dates and not run-relative | PASS (semantics established) | `first_event_time_sample` | No chronology; no temporal-drift claim; field excluded |
| Chronology / capture order | unknown | `selection_order` unique; not a time | PASS | audit | none usable |
| Status filter | all runs completed | `normalized_status = completed_behavior` for 100% of rows | PASS | audit | no failed-run selection in released rows |
| Runs without any recorded event | few | 1,109 Android-10 and 24 Android-14 rows have `n_l1_events = 0` and all 19 flags false | PASS | audit | contribute no source-positive claims; reported as sensitivity |
| Identity keys | SHA-256, run id, package | SHA-256 unique; package names present; package name identical across contexts for all pairs | PASS | `paired_pkg_same_across_ctx = 1.0` | Group on package |
| Package structure | many APKs per package | 22,475 packages in the paired set; 18,866 singleton packages; max package size documented in `pkg_size_dist` | PASS | audit | Package grouping required; effective sample smaller than APK count |
| Family labels | unknown before | `family` present, 47 distinct values, identical in both contexts for 100% of pairs; 38 families with ≥ 50 paired APKs; mixed adware, banking-trojan and packer tokens | PASS (**new finding**) | `paired_family_same_across_ctx = 1.0` | Family-held-out evaluation becomes possible; earlier statement "SELENE is not a family study" superseded |
| Duplicate/derived indicators | some | two exact duplicate flag pairs: `has_NETWORK_EXTERNAL`=`has_external_tcp`, `has_PROCESS_MEMORY_READ`=`has_process_vm_readv`; two `*_high_volume` flags are threshold-derived | PASS | `exact_duplicate_flag_pairs` | Redundancy sensitivity in Roadmap |
| Indicator support | some rare | `has_rwx_anon` only 212 positive in the smaller context; others ≥ 9,700 | PASS | `flag_support_min` | rare indicator handled by pooled model; per-indicator NA rules |
| Class prevalence (recurrence) | high | 89.96% (10→14) and 85.48% (14→10) of source-positive claims recur | PASS | four-state table | persistence strong; Brier/log loss lead |
| Four-state structure | heterogeneous | per-indicator recurrence 0.46–1.00; target-recorded evidence among source-absent 0.2%–99.8% | PASS | `four_state` | H1 evidence |
| Context differences | duration differs | median duration 177.5 s vs 143.8 s (paired); correlation 0.08 | PASS | audit | context bundles duration; no causal wording |
| Paired versus unpaired | selection differences | Android-10 paired versus unpaired indicator prevalence differs by 3.2 points on average and 8.7 at most (recomputed in `audit_selene.py`, matches the archived audit) | PASS (effect present) | `a10_paired_minus_unpaired_prevalence` | inference limited to the paired population |
| Fidelity oracle | independent truth? | 1,000 rows per context; 56 shared paired APKs | PARTIAL | `oracle_in_paired = 56` | cannot serve as behaviour ground truth |
| Feature preprocessing | none by provider | counts and durations are released raw; no normalisation | PASS | schema | fit scaling inside training partitions |
| Sample-size support | adequate | 377,800 (10→14) and 397,626 (14→10) source-positive claims | PASS | `c2_selene.py check` | metrics computable |
| Client/domain identifiers | none | not applicable (no FL) | PASS | n/a | none |
| Supported claims | recurrence, scoping | supports recorded-evidence recurrence, worst-indicator/family risk, verification cost; does not support behaviour truth, causal OS attribution, temporal drift, run-to-run variance | PASS | above | Roadmap limitations |

### 2.2 KronoDroid (`fetch_krono.sh`, `audit_krono.py` → `out/audit_krono.json`)

| Check | Expected | Actual | Status | Evidence | Consequence |
|---|---|---|---|---|---|
| Source and licence | public GitHub archives; "released publicly for research purpose", cite Guerra-Manzanares et al. 2021 | 4 zip archives (25.68 MB): emulator benign/malware, real device benign/malware; SHA-256 in audit JSON | PASS | README fetched; audit `files` | cite; no redistribution of rows |
| Rows | 28,745 + 35,246 emulator; 41,382 + 36,755 device | 63,991 emulator; 78,137 device | PASS | audit `rows` | matches README |
| Columns | README: 289 dynamic + 200 static | 484 columns (483 in the emulator-malware archive): `Package`, `Malware`, 288 syscall counts, `nr_syscalls` (=289 dynamic), 166 permission-style static columns, static aggregates, then `sha256`, dates, `Scanners`, `Detection_Ratio`, `MalFamily` | PARTIAL | audit `col_groups` | dynamic count matches; static count differs by a handful; archives differ in date columns (below) |
| Schema across archives | identical | emulator archives have `FirstModDate`/`LastModDate`; device archives have `EarliestModDate`/`HighestModDate` instead; `FilesInsideAPK` extra in three archives | PARTIAL | `archive_schema` | concatenation creates NaNs; dates not used |
| Timestamps | execution time? | date columns are APK archive entry dates with a 1980-01-01 sentinel; not execution or capture time | PASS (semantics established) | min value `1/1/1980` | no drift/chronology claims |
| Identity | SHA-256 | unique SHA per context: 63,987 emulator (4 duplicated groups), 78,133 device (4 groups); duplicated groups carry conflicting `Malware` labels | PASS | `emu_dup`, `dev_dup` | exclude duplicated SHAs |
| Pairing | exact SHA | 63,320 SHAs intersect; 63,316 after removing duplicated SHAs; `Malware` label agrees for 100% of pairs; package agrees 100% | PASS | `pairs` | replication population |
| Package structure | many APKs per package | 47,709 packages in pairs; largest package 1,159 APKs | PASS | audit | package grouping required (the archived FL POC grouped by SHA only) |
| Repeated runs | possible via duplicates | the 4 duplicated groups per context differ in 0.6% (emulator) and 3.0% (device) of syscall presence bits: too few (4 pairs) for a variance estimate | BLOCKED | `pair_syscall_presence_disagree_mean` | no stochasticity claim |
| Family label semantics | unreliable? | 33,838 naive inequalities were an artefact of comparing missing values; both-present pairs: 30,678 with 1,200 disagreements (3.9%); benign pairs mostly have missing family (31,962 both missing); 2,719 benign pairs carry a family | PASS (**supersedes earlier "unusable" finding**) | `family_resolution` | families usable descriptively; still excluded from primary Krono model; naming inconsistency remains for 1,200 pairs |
| Static columns across contexts | context-invariant | 100% identical across paired APKs | PASS | `static_cols_identical_across_ctx = 1.0` | can be source-side APK metadata; never evidence of context effects |
| Zero-syscall APKs | some | 68 emulator, 352 device (nr_syscalls = 0) | PASS | audit | no source-positive claims; kept |
| Syscall activity | sparse | mean presence 12.8% (emulator), 11.0% (device); 157 of 288 syscalls ever present in either context; 56 have ≥ 100 positive claims in both | PASS | audit | macro summaries restricted; README variance counts (122/128) consistent in scale |
| Missing cells | none | 0 in syscall columns | PASS | audit | none |
| Class prevalence | balanced | 44.8% malware in pairs | PASS | audit | strata valid |
| Supported claims | descriptive replication | supports syscall-presence recurrence and worst-syscall risk; not semantic behaviour claims, not temporal drift, not stochasticity | PASS | above | Roadmap Section 26 |

### 2.3 Datasets considered and not used

| Dataset | Status | Reason | Evidence |
|---|---|---|---|
| AndroCT | BLOCKED | access agreement (faculty/permanent staff), 6.3 GB, prohibited redistribution | `docs/poc/Dataset & POC Audit.md` |
| DYNAMISM 2016–2023 | BLOCKED | restricted record | same |
| CIC-InvesAndMal2019 | BLOCKED | 5,000 vs 5,491 install count conflict; pairing unproven | same |
| TraceDroid | PARTIAL | single context; historical cohort | same |
| AndroZoo metadata | REJECTED as outcome data | no behaviour outcome | same |

## 3. POC Matrix

Commands are run from `docs/Candidate 2/poc/`. Seeds are split salts (hash of package or family name plus salt). Outputs are in `out/`.

| ID | Question | Script | Input | Split | Seeds | Baseline | Candidate | Oracle | Metric | Result | Interpretation | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C2-P1 | Dataset facts, pairing, four-state | `audit_selene.py`, `audit_krono.py` | SELENE parquet; Krono zips | n/a | n/a | n/a | n/a | n/a | counts | Section 2 | inputs valid | PASS |
| C2-P2 | Identity and leakage assertions | `python c2_selene.py check --salt 0` | SELENE | package and family folds | 0 | n/a | n/a | n/a | assertions | pass: predictors unchanged when target rows are shuffled; fit/cal/test disjoint by package and by family; package folds agree across directions | no target information in features; cross-direction transfer valid | PASS |
| C2-P3 | Source-only recurrence signal beyond persistence | `c2_selene.py prob` | SELENE claims (377,800 / 397,626) | 5-fold package-grouped OOF, 20% calibration packages held out from fit | 0, 1, 2 | global, indicator persistence, family × indicator persistence | Boolean, count, volume, rich logistic; rich + family; gradient-boosted rich (salt 0) | none | Brier skill vs persistence, log loss, package-cluster bootstrap | 10→14: Boolean .073, count .080, volume .073, rich .088, rich + family .096, boosted .167, family-persistence .054. 14→10: Boolean .019, count .036, volume .030, rich .042, rich + family .061, boosted .104, family-persistence .071. Bootstrap 95% intervals of Brier gain exclude 0 for every model; salts agree to ±.002 | signal beyond indicator persistence in both directions; logistic gains modest; metadata-only baseline beats rich logistic in 14→10; nonlinear roughly doubles logistic gain | PASS |
| C2-P4 | Broken-pair control | same | same | same | 0 | persistence | all learned models | n/a | Brier gain under permuted target rows | every model loses to persistence (−.002 to −.012 Brier) | advantage requires true pairing | PASS |
| C2-P5 | Unseen-family generalisation | `c2_selene.py prob` (family folds) | SELENE | 5-fold by family hash | 0, 1, 2 | indicator persistence (family-persistence falls back to it) | as above | none | Brier skill | 10→14: Boolean .071, rich .079, boosted .117 (family-cluster bootstrap, 1,000 draws, salt 0: Brier-gain intervals [.0023,.0084], [.0028,.0094], [.0053,.0123], all excluding 0). 14→10: Boolean .005, rich .024, boosted .069 (intervals [−.0023,.0029], [−.0005,.0050], [.0036,.0121]: only the boosted model and the volume/rich + family variants exclude 0) | forward signal survives unseen families; reverse logistic signal is not resolved once dependence within families is respected; per-fold spread is large (14→10 rich: −.023 to .080) | PARTIAL |
| C2-P6 | Calibration-only scoping | `c2_selene.py scope` | SELENE | 5-fold, 20% calibration packages | 0, 1, 2 | persistence, family-persistence | Boolean, rich; pooled / per-indicator / UCB thresholds | retrospective risk at fixed coverage | realised risk, coverage, retention, worst-indicator and worst-family risk, report-level | see Section 3.1 | stated risk is attained; coverage advantage over persistence; pooled thresholds hide worst-group risk | PASS |
| C2-P7 | Verification cost | `c2_selene.py xdir` (threshold part) | SELENE | as above | 0, 1, 2 | full-calibration threshold | pooled threshold from k verified claims | full calibration | mean realised risk at target 5%, fraction of draws with risk > 7%, no-operating-point rate | (14→10 / 10→14) k = 30: risk .066 / .049, violation 42% / 22%; k = 100: 25% / 19%; k = 300: 14% / 9%; k = 1,000: 3% / 1%; k ≥ 3,000: 0% | roughly a thousand verified target claims for a reliable pooled threshold at this risk target | PASS |
| C2-P8 | Cross-direction transfer | `c2_selene.py xdir` (model part) | SELENE | same folds both directions | 0, 1, 2 | in-direction persistence | model fitted in the opposite direction, raw and Platt-recalibrated with k target claims | in-direction model | Brier skill | raw −.106 (14→10) / −.206 (10→14); recalibrated with k = 10,000 −.031 / −.055; in-direction model recalibrated with k = 100 reaches .012 / .053, with k = 1,000 .039 / .084 (in-direction .042 / .088) | an opposite-direction model does not beat persistence even with recalibration; verification helps only in-direction | PASS |
| C2-P9 | External replication | `c2_krono.py` | KronoDroid pairs (2.33 M / 2.01 M claims) | 5-fold package-grouped, calibration packages | 0, 1 | per-syscall persistence | Boolean, rich, rich + static, boosted; pooled / per-syscall thresholds | none | Brier skill; scope | emu→dev: Boolean .099, rich .111, rich + static .133, boosted .286; dev→emu: .206, .229, .247, .445; all with intervals excluding 0; broken pair loses; worst-syscall risk 0.3–1.0 at pooled operating points | qualitative replication of C2-P3/P4/P6 on a different ontology | PASS |
| C2-P11 | Calibration of predicted probabilities | `c2_selene.py prob` (`calibration`) | SELENE | 5-fold OOF | 0 | persistence | Boolean, rich, boosted | none | calibration slope, intercept, ECE (10 equal-mass bins) | package grouping: slopes .99–1.07, ECE ≤ .012 (10→14 rich .0056; 14→10 rich .0087); family grouping: slopes .91–.94 (mild overconfidence), ECE ≤ .022 | models are well calibrated under package grouping, slightly overconfident for unseen families | PASS |
| C2-P12 | Exposure normalisation | same (`count_norm`, `rich_norm`) | SELENE | same | 0 | raw counts | duration-normalised counts | none | Brier skill | count: .080 raw vs .043 normalised (10→14); .036 vs .031 (14→10); rich: .088 vs .085; .043 vs .039 | duration normalisation does not improve the signal; raw counts kept | PASS |
| C2-P13 | Indicator redundancy | `c2_selene.py redundancy` | SELENE minus `has_external_tcp`, `has_process_vm_readv` (17 indicators); class-level subset (12 upper-case indicators) | 5-fold package | 0 | persistence | Boolean, rich | none | Brier skill | duplicates dropped: 10→14 Boolean .083, rich .098; 14→10 Boolean .018, rich .042 (355,340 / 374,460 claims); class-level only: 10→14 Boolean .050, rich .101; 14→10 Boolean .008, rich .046; family-persistence .061 / .074 in the class-level subset | conclusions unchanged; family-persistence still beats rich logistic in 14→10 | PASS |
| C2-P10 | Archived FL POC on KronoDroid contexts | `legacy/kronodroid_fl_context_poc.py` | KronoDroid | SHA-grouped | 3 | local-only | central, FedAvg, FedProx, opposite-context transfer, agreement mask | n/a | macro balanced accuracy | local .823, FedAvg .759, FedProx .758, transfer ≈ .508, mask ≈ .500 | no FL benefit with two contexts | REJECTED (FL line) |

### 3.1 Scoping results (mean of 3 salts; risk target r*)

| Direction | r* | Policy | Realised risk | Coverage | Worst-indicator risk | Worst-family risk | Note |
|---|---|---|---|---|---|---|---|
| 10→14 | 5% | persistence, pooled | .048 | .812 | .186 | .222 | |
| 10→14 | 5% | family-persistence, pooled | .049 | .856 | .214 | .089 | |
| 10→14 | 5% | rich, pooled | .050 | .874 | .218 | .088 | worst-fold .053 |
| 10→14 | 5% | rich, UCB | .048 | .866 | .218 | .085 | conservative |
| 10→14 | 5% | rich, per-indicator | .023 | .702 | .053 | .074 | thresholds fixed per indicator; risk far below target, coverage cost |
| 14→10 | 5% | persistence, pooled | .047 | .552 | .088 | .236 | |
| 14→10 | 5% | family-persistence, pooled | .047 | .692 | .156 | .254 | equals rich coverage |
| 14→10 | 5% | rich, pooled | .048 | .695 | .118 | .256 | worst-family risk five times target under every policy |
| 14→10 | 2% | persistence, pooled | none | 0 | | | `NO_OPERATING_POINT` in all folds |
| 14→10 | 2% | rich, pooled | .017 | .151 | .018 | .161 | |
| 10→14 | 1% | rich, pooled | .009 | .600 | .041 | .023 | |

Report-level (10→14, r* = 5%, pooled): rich keeps 0.55 unsupported claims per APK report (28% of reports contain at least one), persistence 0.49 (31%), per-indicator rich 0.20 (14%).

## 4. Claim & Gate Matrix

| Claim | Required evidence | Current evidence | Gate | Result | Allowed wording | Forbidden wording | Remaining experiment |
|---|---|---|---|---|---|---|---|
| C1 Recorded portability is heterogeneous | four-state tables, per-indicator recurrence spread | recurrence 46%–100% across indicators; target-recorded evidence among source-absent claims 0.2%–99.8% | spread ≥ 0.10 | PASS | "recorded evidence recurs heterogeneously in the tested contexts" | "behaviour emerged", "OS causes" | none |
| C2 Source-only evidence beats persistence | intervals excluding 0, both directions, broken-pair loss | PASS in both directions for all learned models, 3 salts (package grouping); family-grouped positive forward, mixed reverse (see C12) | Brier gain interval excludes 0 | PASS | "improves Brier score by 2–9% (logistic) and 7–17% (boosted) over indicator persistence" | "large", "solves" | confirmatory salts |
| C3 …and beats family-conditioned persistence | same against family × indicator persistence | 10→14: rich .088 vs .054 (PASS); 14→10: rich .042 vs .071 (FAIL); rich + family .061 also below | both directions | PARTIAL | "beats family-conditioned persistence in one direction; boosted model beats it in both" | "beats all baselines" | boosted vs family-persistence paired interval |
| C4 Nonlinear comparator adds beyond logistic | paired gain above rich logistic | boosted BSS .167/.104 vs rich .088/.042; intervals non-overlapping | both directions | PASS (exploratory: salt 0 only) | "a boosted-tree comparator roughly doubles the gain" | "logistic is enough" | more salts |
| C5 Calibration-only policy attains target | mean realised risk within r* ± 0.01, worst fold ≤ r* + 0.02 | pooled: .047–.050 at 5%; worst fold ≤ .053; 14→10 at 1–2% coverage collapses (operating point unavailable or coverage ≤ .15) | as stated | PASS at 5%; PARTIAL at ≤ 2% (14→10) | "meets a 5% risk target on untouched groups" | "guarantee" | UCB versus pooled comparison in confirmatory |
| C6 More coverage than persistence at equal risk | coverage difference > 0 both directions | rich .874 vs .812 (10→14), .695 vs .552 (14→10); but family-persistence .856 / .692 | sign consistent | PARTIAL (holds against indicator persistence; ties family-persistence in 14→10) | "retains 6–14 points more coverage than indicator persistence at a 5% target" | "outperforms all baselines" | none |
| C7 Pooled thresholds hide worst-group risk | worst-indicator or worst-family ≥ pooled + 0.05 | worst-indicator .218 vs .050 (10→14, rich); worst-family .256 vs .048 (14→10); per-indicator thresholds bring worst-indicator to .053 at −17 points coverage; worst-family risk stays .07–.26 | ≥ 0.05 | PASS | "pooled operating points mask indicator- and family-level risk up to 5× the target" | "per-indicator thresholds solve reliability" | per-family thresholds (exploratory) |
| C8 About 1,000 verified target claims for a reliable threshold | violation ≤ 5% at k = 1,000 and > 10% at k = 100 | violation 1–3% at k = 1,000; 19–25% at k = 100 | as stated | PASS (3 salts) | "on the order of a thousand" | "exactly" | salts 1–2 |
| C9 Opposite-direction models do not transfer | raw and recalibrated Brier skill ≤ 0 vs in-direction persistence | all ≤ 0 up to k = 10,000 | as stated | PASS | "did not transfer in these two contexts" | "cross-context models cannot work" | none |
| C10 Replicates on KronoDroid | same sign of C2 and C7 | C2 positive both directions in salts 0 and 1 (emu→dev rich .111, boosted .286; dev→emu .229 / .445 in salt 0; .227 / .437 in salt 1); broken pair loses; worst-syscall risk 0.3–1.0 | same sign | PASS | "qualitatively replicated on a different ontology" | "generalises across Android" | confirmatory salts |
| C11 Report-level benefit | offline proxy | unsupported claims per report reduced by per-indicator scope (0.55 → 0.20) at coverage cost | descriptive | PARTIAL | "offline proxy only" | "analyst time savings" | none |
| C12 Family-held-out generalisation | positive interval (family-cluster bootstrap) | forward positive for all learned models; reverse: logistic intervals include 0, boosted [.0036,.0121] excludes 0 | positive both | PARTIAL | "signal survives unseen families in 10→14; in 14→10 only the nonlinear comparator is resolved" | "family-agnostic" | confirmatory salts |
| C13 Stochastic run variation vs context variation | repeated runs | none | n/a | BLOCKED | none | any variance decomposition | needs data |

## 5. Literature Collision Matrix

Targeted 2024–2026 searches (web, September 2026); not a systematic review. "Novelty risk" is HIGH/MED/LOW.

| Closest paper | Collision | Remaining distinction | Novelty risk | Status |
|---|---|---|---|---|
| Dong et al., *Same App, Different Behaviors: Uncovering Device-specific Behaviors in Android Apps* (ASE 2024, arXiv 2406.09807) | Device-dependent behaviour of the same app on 20,000+ apps (static analysis) | ours: dynamic recorded claims, recurrence estimand, calibrated scoping | LOW | PASS |
| *Concept drift and cross-device behavior: challenges and implications for effective Android malware detection* (Computers & Security 2022) and the cross-device consistency study cited in the archive | Cross-device dynamic behaviour differences and detection impact | not claimed as novel; ours is per-claim recurrence and scoping | MED | PASS (cite, do not claim) |
| Alzaylaee et al., *Emulator vs. Real Phone* (arXiv 1703.10926); *DL-Droid* (2020); Guerra-Manzanares et al., *KronoDroid* (2021) | emulator versus device differences in detection | same | LOW | PASS |
| Angelopoulos et al., *Conformal Risk Control* (ICLR 2024) and *Learn then Test*; *Selective Conformal Risk Control* (arXiv 2512.12844) | selective prediction with risk control on accepted set | no guarantee claimed; dependence between claims of one APK and target shift make plain guarantees invalid; ours evaluates empirical operating points and UCB variant | MED | PASS |
| *Operational Android malware filtering: calibrated probabilities and distribution-free guarantees* (2025 preprint, found by search; full text not read) | calibrated conformal models in Android malware triage; calibration-size ablation | ours concerns cross-context recurrence of recorded claims, not malware classification | MED | PARTIAL (read before submission) |
| Shahid, *When Average Calibration Fails: Site-Conditional Federated Conformal Risk Control* (arXiv 2606.20115) | pooled calibration protects the average site but violates coverage at 40% of sites; shrinkage between site-local and pooled thresholds | same qualitative phenomenon on indicator and family groups; our pooled-versus-per-group scope result is a second-domain instance, not a first | MED | PASS |
| ARTEMIS (SBSeg 2025) and SELENE (SBSeg 2026) papers | dataset papers; SELENE ships `table_04/05/07` metric tables | unknown whether cross-context recurrence is analysed | UNKNOWN | MISSING (read both papers and the `table_*` configs) |

Contribution type: **measurement / operational protocol** (estimand, baselines, calibrated scoping, verification cost) with a **negative result** (no cross-direction transfer). Not methodological. No "first/novel/state of the art" wording.

## 6. Implementation-Risk Register

| ID | Risk | Category | Likelihood | Impact | Status | Mitigation |
|---|---|---|---|---|---|---|
| R-01 | SELENE licence terms change or paper citation changes | licensing | low | med | PARTIAL | live README fetched 2026-09-24; re-check at release |
| R-02 | Schema instability in SELENE releases | schema | low | med | PASS | SHA-256 of all 8 files recorded; audit re-derives counts |
| R-03 | Family label semantics (AV-derived) | label semantics | med | med | PARTIAL | treated as metadata; family models labelled; family-held-out variant |
| R-04 | Insufficient support for rare indicator | support | low | low | PASS | pooled model; NA rules |
| R-05 | Runtime | runtime | low | low | PASS | boosted comparator ≈ 10 min/salt on 10 cores; Krono ≈ 30 min |
| R-06 | Family-grouped intervals clustered by package understate dependence | statistics | high (found) | med | PASS (fixed) | `c2_selene.py prob` clusters by family for family folds; salt-0 rerun at 1,000 draws widened the 14→10 intervals so that logistic gains include 0 |
| R-07 | Leakage through target fields or fold mismatch | leakage | low | high | PASS | `c2_selene.py check`: predictors invariant to target shuffling, group disjointness, cross-direction fold agreement |
| R-08 | Missing repeated runs | data | certain | med | BLOCKED | stochastic-variation question removed from core |
| R-09 | Krono schema differences across archives | schema | certain | low | PARTIAL | only syscall and static columns used; dates ignored |
| R-10 | Memory for Krono claims (2.3 M rows) | memory | med | low | PASS | fit on ≤ 400,000 claims; chunked prediction |
| R-11 | SELENE paper/`table_*` configs unread; possible collision | novelty | med | med | MISSING | read before submission |
| R-12 | Pairing selection bias | validity | certain | med | PARTIAL | inference limited to paired population; audit in Roadmap |
| R-13 | Reproducibility from clean environment | reproducibility | low | med | PARTIAL | `run_selene.sh`, `fetch_krono.sh`, path variables; clean-environment rerun not executed |
| R-14 | Nonlinear comparator invalidates "simple ladder" framing | design | med | low | PASS | comparator predeclared; claims worded with both |

## 7. Negative Evidence

| Finding | Rules out |
|---|---|
| Global prevalence loses to persistence (Brier skill −0.23 to −0.26) | a trivial baseline |
| Opposite-direction model raw (−.106/−.194) and recalibrated (−.03/−.05 at 10,000 claims) | cross-context model reuse |
| Duration-normalised counts worse than raw counts (archived POC, two seeds) | exposure-normalisation explains the count signal |
| Family × indicator persistence beats rich logistic in 14→10 (.071 vs .042) | claim that source flags/counts alone beat every cheap baseline |
| 14→10 at r* ≤ 2%: persistence has no operating point; rich has coverage ≤ .15 | strict risk targets in the reverse direction |
| Per-indicator thresholds leave worst-family risk at .07–.26 | indicator-level scoping as a fix for family heterogeneity |
| Two-context FL on KronoDroid: local beats FedAvg/FedProx (archived) | FL framing of CASE |
| Formal risk-guarantee claims not implemented | guarantees (dependence between claims of an APK, target shift) |
| AndroCT, DYNAMISM, CIC blocked | granularity, stochasticity, lifecycle lanes |

## 8. Roadmap Decisions and Evidence

| Decision in Roadmap | Evidence |
|---|---|
| Package-grouped 5-fold with calibration partition | 18,866 of 22,475 packages are singletons but 2,143 have ≥ 2 APKs; group leak assertions (C2-P2) |
| Add family-held-out evaluation and family-conditioned baseline | `family` present in SELENE and identical across contexts (Section 2.1); family-persistence reaches 5–7% skill (C2-P3) |
| Keep logistic as primary, predeclare a boosted comparator | boosted skill roughly twice logistic (C2-P3); logistic remains interpretable |
| Primary metric Brier skill and log loss, not AP | recurrence 85–90%; global prevalence loses; AP not informative (legacy AP > .95) |
| Risk targets 1/2/5% and UCB variant | 14→10 has no operating point at ≤ 2% for persistence (C2-P6) |
| Report worst-indicator and worst-family risk and per-indicator thresholds | pooled thresholds mask 4–5× risk (C2-P6) |
| Verification-cost experiment as RQ4 | violation rates by k (C2-P7) |
| Cross-direction transfer as a negative-result experiment | C2-P8 |
| KronoDroid as replication with syscall ontology, package grouping, static metadata variant, boosted comparator | audit (Section 2.2), C2-P9 |
| Drop stochastic-variation and temporal-drift questions | no repeated runs, no execution timestamps (Sections 2.1, 2.2) |
| Drop FL framing, keep explicit PhD-relation section | C2-P10 |
| Raw counts primary, duration-normalised as ablation | archived POC: raw counts better in both directions and both seeds |
| Confirmatory salts 100–104, 10,000 bootstrap draws | design salts 0–2 used here |

## 9. Contradictions between experiments or documents (investigated)

1. **KronoDroid family labels.** Earlier audit (`legacy/kronodroid_audit.json`) reported 33,838 family disagreements on 63,316 pairs and declared the field unusable. Reproduced: `(a.MalFamily != b.MalFamily).sum() = 33,838` (`family_resolution.naive_ne_count`), but 31,962 of these are pairs where both are missing (NaN ≠ NaN). Among pairs where both labels are present, 1,200 of 30,678 (3.9%) differ. **Status: earlier finding SUPERSEDED**; families are usable descriptively, naming inconsistency remains for 3.9%.
2. **"SELENE is not a family study".** Earlier reports stated that SELENE offers no family-held-out design. `run_features` has a `family` field, identical across contexts for all pairs. **SUPERSEDED**; family-held-out evaluation added (C2-P5).
3. **"Simple logistic ladder is sufficient; no nonlinear model justified".** New boosted comparator roughly doubles the Brier skill (C2-P3). **SUPERSEDED**: roadmap predeclares the comparator and words claims accordingly.
4. **Brier skill: archived vs new protocol.** Archived single-split rich BSS: 9.7% / 8.7% (10→14) and 4.2% / 4.0% (14→10). New 5-fold OOF: 8.8% and 4.2–4.3%. Differences (≤ 0.9 points) come from the protocol (fit on 64% of packages instead of 80%, pooled OOF over all folds); qualitative conclusions unchanged. **PASS**.
5. **Scoping numbers.** Archived P61: rich coverage .873 vs persistence .836 (10→14) and .709 vs .639 (14→10) at r* = 5%. New: .874 vs .812 and .695 vs .552. The archived policy chose the threshold at the largest cumulative position (splitting tied persistence scores) with a 30-claim minimum; the new rule requires 200 kept calibration claims and keeps tied scores whole, which lowers persistence coverage (persistence has only 19 distinct scores). Direction and size of the gain agree. **PASS**, new protocol is the stated one.
6. **Worst-indicator risk.** Archived .21–.22 at r* = 5% pooled, .06 per-indicator; new .218 and .053. **PASS**.

## 10. Unresolved questions

- Read the SELENE and ARTEMIS papers and the `table_04/05/07` configs (MISSING, R-11).
- Read the Android conformal filtering preprint (PARTIAL).
- Clean-environment rerun of `run_selene.sh` and `c2_krono.py` (R-13).
- Whether per-family thresholds fix the worst-family risk (exploratory, not in the core protocol).

## 11. Reproduction commands

```bash
cd "docs/Candidate 2/poc"
./fetch_krono.sh                       # 25.7 MB, SHA-256 printed
python audit_selene.py; python audit_krono.py
python c2_selene.py check --salt 0     # identity and leakage assertions
python c2_selene.py prob  --salt 0 --boot 1000
python c2_selene.py scope --salt 0
python c2_selene.py xdir  --salt 0
python c2_krono.py --salt 0
python c2_tables.py > out/analysis_c2.txt
```

## 12. Final audit passes

### Pass 1 — scientific audit

| Check | Result | Status | Action taken |
|---|---|---|---|
| RQs match experiments | RQ1 → four-state audit; RQ2 → C2-P3, C2-P5, C2-P11–C2-P13; RQ3 → C2-P6; RQ4 → C2-P7, C2-P8; RQ5 → C2-P4, C2-P5, C2-P9, C2-P13 | PASS | |
| Baselines fair | persistence, family × indicator persistence (metadata), activity-volume model and Boolean/count ladders on identical claims; nonlinear comparator predeclared | PASS | family-conditioned baseline and comparator added during the audit |
| Metrics answer RQs | Brier skill, log loss, calibration slope/ECE (RQ2); risk, coverage, worst-group, report-level (RQ3); violation rate versus k (RQ4) | PASS | calibration slope/ECE implemented (was specified but missing) |
| Claims follow from planned evidence | C3, C6, C12 already PARTIAL; C8/C9 quantified with three salts | PASS | family-grouped intervals switched to family clusters, which weakened C12 |
| Novelty bounded | measurement/operational; SELENE/ARTEMIS papers unread | PARTIAL | flagged MISSING |
| No post-hoc method promoted | boosted comparator and family baseline were added after the archived work, are predeclared in the Roadmap and were not selected by test outcomes | PASS | |
| Duration normalisation, redundancy, class-level subset, paired-versus-unpaired audit | all specified in the Roadmap and now implemented | PASS | added during the audit |
| Broken-pair and target-independence controls | pass | PASS | |
| Stochastic run variation | no data | BLOCKED | question removed from the core |

### Pass 2 — implementation audit

| Check | Result | Status | Action taken |
|---|---|---|---|
| Files exist | 8 SELENE parquet files (29.78 MB, SHA-256 recorded); 4 KronoDroid zips (25.68 MB, SHA-256 recorded) | PASS | `fetch_krono.sh` |
| Required columns exist | 19 `has_*`, 18 count, 8 volume fields, `family`, `package_name`, `sha256`; Krono 288 syscall columns, static columns, `Package`, `sha256` | PASS | |
| Labels support the task | outcome = target flag/syscall presence; no labels used as predictors | PASS | |
| Sample support adequate | 377,800 / 397,626 SELENE claims; 2.33 M / 2.01 M Krono claims; assertions pass for salts 0 and 100–104 | PASS | |
| Client/context construction | two contexts per dataset with exact SHA pairing | PASS | |
| Splits possible | package and family folds disjoint; cross-direction fold agreement asserted | PASS | |
| Metrics computable | all in `out/analysis_c2.txt` | PASS | |
| Hidden data dependency | KronoDroid downloads from GitHub; SELENE files assumed present locally (public on Hugging Face) | PARTIAL | documented; SELENE download command not scripted |
| Runtime and storage | boosted comparator only for salt 0 in the development runs; the Roadmap requires it for all confirmatory salts (≈ 10 min per salt) | PARTIAL | cost recorded |
| Hardware | CPU only; no devices | PASS | |
| Reproducibility from a clean environment | `run_selene.sh`; clean reinstall not performed | PARTIAL | Section 10 |
