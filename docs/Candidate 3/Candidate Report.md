# Candidate 3 — What Does a Verification Budget Buy? Candidate Report (audit trail and evidence dossier)

Companion to [Roadmap.md](Roadmap.md). Status vocabulary: `PASS`, `PARTIAL`, `MISSING`, `BLOCKED`, `REJECTED`, `SUPERSEDED`.

Paths are relative to `docs/Candidate 3/poc/` unless prefixed with `docs/poc/temp/` (archived exploratory workspace, unchanged) or `legacy/` (byte-identical copies of exploratory scripts and outputs; see `legacy/MANIFEST.tsv`). Raw data: `CASE_RAW`; ScienceDB device files re-fetched to `data/cache/scidb/` (git-ignored). Analysis text output: `out/analysis_<domain>_a<alpha>_N<pool>.txt`, `out/analysis_label_efficiency.txt`.

## Dashboard

| Item | Status | Summary |
|---|---|---|
| Overall status | **PASS as an empirical chapter; no method claim** | Contamination failure is large and reproducible in three domains; label-efficiency and a budget crossover are consistent across domains; no policy dominates; allocation headroom is absent or estimator-dependent |
| Chapter fit | PARTIAL–PASS | Mobile app markets are the primary domain (LAMDA), IoT device federations are replications; the chapter is about detector calibration rather than app privacy per se |
| PhD relevance | PASS | Calibration and client-specific thresholds, unreliable/contaminated local evidence, poisoning-like contamination, worst-client TPR/FPR, scarce labels, IoT device federations |
| Dataset readiness | PASS (three domains) | Scorers regenerated with leakage-controlled splits; one earlier error found and repaired (N-BaIoT attack de-duplication); contamination is injected (no natural contamination exists in the data) |
| POC readiness | PASS | 5 seeds × 3 domains × 3 contaminant types × 5–6 profiles × 5–6 budgets × 2 α values, plus pool-size sensitivities |
| Novelty confidence | LOW–MODERATE | Label-Trim (ICML 2025), retained-law trimming (2026), site-conditional federated shrinkage (2026), federated NIDS under contaminated training data (2026) cover the components; heterogeneous federated pools with one global budget and client-level constraints remain |
| Mechanism / headroom | Headroom real, mechanism not justified | Oracle repair restores TPR (LOCAL .31–.37 → oracle .70–.80); simple verified-benign shrinkage and contamination-trimming each win in different budget ranges; no consistent winner; oracle allocation does not help |
| Implementation readiness | PASS | Scripts, assertions, stable commands; confirmatory seeds 100–109 not yet run |
| Biggest remaining risk | Injected contamination only; the pooled trimming estimators harm clean clients under heterogeneous contamination; α = 1% unsupported |

## 1. Inventory and mapping of pre-existing artifacts

Nothing was deleted from `docs/poc/`. Legacy copies live in `legacy/` (large duplicates `v1_nogate`–`v4_peer2` removed from the copy, originals retained; see `legacy/README.md`).

| Artifact | Supports | Status | Note |
|---|---|---|---|
| `legacy/p5_scores.py`, `p5_mobsup_scores.py`, `c1_common.py`, `p5_scores/*.npz` | frozen scorers for P59 | SUPERSEDED by `c3_scores.py` | Old scripts point to a deleted scratchpad; `p5_scores/` kept for comparison (Section 3, C3-P2) |
| `legacy/p5_budget.py`, `p5_budget_*_a{0.05,0.01}.json`, `p5_final_output.txt`, `p5_analyze_output.txt` | P59 verification-budget study | SUPERSEDED by `c3_budget.py` | Different policy set (tau-corrected variants added after seeing results; pool drawn with replacement for small support; homogeneous-only clean-client check) |
| `legacy/c1_run.py`, `c1_analyze.py`, `c1_results_*.json` (variants v1–v4 in `docs/poc/temp/`) | threshold-scope policies under contamination (DATP-style) | PRESERVED (negative for mechanisms) | LOCAL/GLOBAL/cluster scope; peer trimming recovers 20–30% label-free |
| `legacy/c2_leakage_scidb.py`, `..._results.json` | duplicate-window leakage in Pi data | PRESERVED | AUROC .857 raw vs .837 de-duplicated |
| `legacy/p4_iot_v3.py`, `p4_data.py`, `p4_scidb_list.py`, `scidb_dataset_page.html`, `iot_dfl_candidate_metadata.json` | Pi dataset access and metadata | PRESERVED | |
| `docs/poc/temp/p3_*`, `p4_*` | collaboration-scope POCs | PRESERVED | see Candidate 1 |
| `docs/poc/Final Report.md` P59 sections | earlier claims | PRESERVED | contradictions in Section 9 |

## 2. Dataset Verification Matrix

### 2.1 LAMDA + AndroZoo markets (mobile domain)

Identity, labels, duplicates and package overlap are shared with Candidate 1 (`../Candidate 1/Candidate Report.md`, Section 2). Checks specific to this candidate:

| Check | Expected | Actual | Status | Evidence | Consequence |
|---|---|---|---|---|---|
| Natural contamination | benign pool may contain undetected malware | label rule VT = 0 for benign; grey zone 1–3 excluded; no VirusTotal timeline | PASS (established) | `label_vt_rule_violations_ge4 = 0` | contamination must be injected |
| Client list | 7 single-market clients | `1mobile` 4,018; `PlayDrone` 6,232; `angeeks` 3,325; `anzhi` 104,287; `appchina` 88,282; `play` 639,596; `slideme` 4,448 rows (single-market rows) | PASS | `single_market` | market sizes range 3 k–640 k |
| Benign calibration support | ≥ N | pools of 304–600 per client after component split (angeeks 304, 1mobile 306, PlayDrone 588, others 600) | PASS | `out/compare_legacy_scores.txt` | N ≤ 300; N = 200 primary |
| Malware calibration and test support | enough contaminants | calibration malware 303–600 per client (seed 0); test malware 311–2,000 | PASS | score logs | contaminants drawn without replacement up to ε = 0.3 |
| Split leakage | none | components (package ∪ vector) disjoint across train/cal/test; assertions in `c3_scores.py` | PASS | runs pass | none |
| Scorer quality | usable | supervised FedAvg MLP AUROC .93–.99 per client (legacy .93–.99) | PASS | `compare_legacy_scores.py` | none |

### 2.2 N-BaIoT (`audit_c3.py` → `out/audit_c3.json`)

| Check | Expected | Actual | Status | Evidence | Consequence |
|---|---|---|---|---|---|
| Source and licence | public UCI dataset; cite Meidan et al. (2018) | 9 device directories with `benign_traffic.csv` and `gafgyt_attacks`, `mirai_attacks` (each also as `.rar`); description file present | PASS | listing; `N_BaIoT_dataset_description_v1.txt` | cite |
| Rows | per device | benign 13,113–175,240; attack rows 316,400–968,750; attack share 84–98% | PASS | `attack_share` | attack-heavy natural prevalence |
| Schema | 115 features | 115 float columns, no header identifiers | PASS | audit | none |
| Identity / client keys | device | one directory per device; no per-row id, session or timestamp | PASS | audit | device = client |
| Chronology | unknown | no time column; file order is capture order; lag-1 autocorrelation of benign rows 0.07–0.81 | PASS (semantics established) | `lag1_autocorr_benign` | random row splits leak neighbouring windows; chunked blocks used |
| Duplicates: benign | some | 4 to 10,099 exact duplicate benign rows per device | PASS | `benign_dup_rows` | removed before splitting (order preserved) |
| Duplicates: attack | some | 20–40% of a random attack sample consists of repeated identical rows (`investigate_nbaiot.py`) | PASS | investigation log | **kept**; removing them changes the test distribution (Section 9, item 1) |
| Global normalisation | none by provider | raw damped-window statistics; scaling from pooled training rows | PASS | audit | no provider-side leakage |
| Nearest-neighbour leakage of random split | leak | mean 1-NN distance test→train smaller for random than for block splits on 6 of 9 devices (e.g. Ennio .99 vs 1.72; Provision-838 1.62 vs 2.60) | PARTIAL | `nn_dist_*` | chunked split justified; effect not uniform |
| Scorer quality | usable | federated AE per-client AUROC .61–.99 (chunked) and .61–.99 (contiguous-tail); legacy .65–.99 | PASS | `compare_legacy_scores.txt` | non-saturated; the low-AUROC devices are hard |
| Calibration support | ≥ N | benign calibration 1,966–3,000 per device | PASS | score logs | N up to 1,000 |
| Supported claims | thresholds under contamination on device traffic | supports simulation of contaminated calibration; not natural contamination; not deployment claims | PASS | | Roadmap |

### 2.3 Raspberry-Pi crowdsensing malware release (ScienceDB DOI 10.57760/sciencedb.25380; `audit_c3.py`)

| Check | Expected | Actual | Status | Evidence | Consequence |
|---|---|---|---|---|---|
| Source and licence | record CC BY 4.0; article CC BY-NC-ND 4.0 | manifest read via the public file-tree API; eight device files fetched by file id; sizes match the manifest byte-for-byte (87,742,914 bytes total (87.7 MB)); SHA-256 recorded | PASS | `out/audit_c3.json`, `legacy/p4_scidb_list.py` | cite both licences; no redistribution of rows |
| Files and rows | 8 files | 20,448–21,765 rows each, 32 columns (31 features + `label`); no missing cells | PASS | audit | none |
| Feature scaling | raw? | every feature in [0,1] with min 0 and max 1 (provider min–max normalisation over the whole release) | PARTIAL | `fmin`, `fmax` | global preprocessing cannot be undone; limitation |
| Duplicates | some | each vector repeated about 5× (80% duplicate rows; 3,839–4,321 unique vectors per device); no vector shared across devices | PASS | `dup_frac`, `vectors_shared_across_devices = 0` | de-duplicate before splitting |
| Label conflicts among duplicates | none (earlier note) | device 7: 480 identical vectors carry both label 1 and label 2 (two malware conditions); none involve benign | PASS (**corrects earlier statement**) | investigation of `7.csv` | irrelevant for binary task; documented |
| Identity, time, run | none | no device id column, timestamp, session or run identifier | BLOCKED | audit | window dependence within an infection run cannot be removed; results optimistic |
| Class prevalence | high malware | 8 malware conditions + benign; unique-vector malware share ≈ 89% | PASS | `malware_prevalence_unique` | thresholds from benign scores |
| Calibration support | small | benign calibration 68–72 unique windows per device | PARTIAL | score logs | N = 60 primary, 30 sensitivity; α = 1% unsupported |
| Supported claims | contamination simulation on 8 devices | same as above | PASS | | |

## 3. POC Matrix

Commands from `docs/Candidate 3/poc/`. Scorers frozen; policy simulations run at score level with 30 pool redraws per seed and scenario. Seeds 0–4 (scorer and pool draws). Outputs `out/c3_budget_<domain>_a<alpha>_N<pool>.json`. Contaminated scenarios: homogeneous ε ∈ {.05, .10, .20}, heterogeneous linear 0–.30, mobile natural (.3 × prevalence); contaminant types random and top unless stated. "Success" = per client FPR ≤ 2α and TPR ≥ 0.8 × oracle TPR.

| ID | Question | Script | Input | Split | Seeds | Baseline | Candidate | Oracle | Metric | Result | Interpretation | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C3-P0 | Dataset facts | `audit_c3.py`, `../Candidate 1/poc/audit_lamda.py` | three domains | n/a | n/a | n/a | n/a | n/a | counts | Section 2 | inputs valid | PASS |
| C3-P1 | Regenerate frozen scorers with leakage controls | `c3_scores.py` | three domains | components (mobile); chunks and tail (N-BaIoT); de-duplicated windows (Pi) | 0–4 | archived scorers | regenerated | n/a | AUROC, pool support | assertions pass; AUROC mobile .93–.99, N-BaIoT .61–.99, Pi .75–.93 (identical to archived for Pi) | scorers usable | PASS |
| C3-P2 | Investigate disagreement: regenerated N-BaIoT AUROC ≈ 1.0 versus archived .65–.99 | `investigate_nbaiot.py` | N-BaIoT | random rows, np.unique benign | 0 | archived sampling | remove attack duplicates | n/a | AUROC | archived sampling reproduces .65–.99; removing repeated attack rows gives ≈ 1.0 | de-duplicating attack rows deletes the hard windows; corrected in `c3_scores.py`; superseded outputs kept in `out/superseded_attackdedup/` | PASS |
| C3-P3 | Does the failure exist? | `c3_budget.py`, `c3_analyze.py` [1] | all | as above | 0–4 | LOCAL, GLOBAL | none | ORACLE-TRUE / TRIM | TPR, FPR | LOCAL TPR (rand+top): mobile .340 vs oracle .799; N-BaIoT (chunked) .370 vs .757; Pi .305 vs .702; FPR stays ≤ .007 (mean); clean pools LOCAL = oracle; by type (LOCAL TPR): random .42/.47/.38, top .26/.27/.23, stealth .68/.68/.62 | contamination halves TPR at unchanged FPR; stealth contaminants do little damage | PASS |
| C3-P4 | Label efficiency and crossover | `c3_budget.py`, `c3_label_efficiency.py` | all | as above | 0–4 | LOCAL | CLEAN-K, CLEAN-K-SHRINK (w .25/.5/.75), LAB-LOCAL, LAB-POOL, LAB-EB | ORACLE-TRUE | success by budget fraction | success at 1–2% of pool: LAB-POOL/LAB-EB .50–.71 (mobile), .53–.62 (N-BaIoT), .48–.68 (Pi) versus CLEAN-K-SHRINK ≤ .36; at 10%: CLEAN-K-SHRINK .86 (mobile), .98 (N-BaIoT), .66 (Pi at 17%) versus LAB-EB .80/.67/.66; at 20%: CLEAN-K 1.00 (mobile); see `out/analysis_label_efficiency.txt` | consistent crossover in all three domains; in absolute terms the verified-benign policies reach success ≥ .8 at k = 20 items per client (= 1/α) for pools of N = 100, 200, 300, 400 and 1,000 (e.g. CLEAN-K-SHRINK .98 at N = 100 and .96 at N = 1,000 for N-BaIoT; mobile first reaches .8 at k = 20 for N = 100/200/300), and at k = 10 (= 1/α) for α = .10; so the crossover scales with 1/α, not with the pool fraction | PASS |
| C3-P5 | Strongest simple baseline | `c3_analyze.py` [3] | all | as above | 0–4 | CLEAN-K-SHRINK 0.5 | LAB-EB, LAB-POOL | n/a | paired cell differences (Wilcoxon over cells) | success LAB-EB − CLEAN-K-SHRINK (mean over all budgets; seed-cluster 95% interval; 5/5 seeds positive in each): mobile +.186 [+.177,+.194], N-BaIoT chunked +.049 [+.034,+.064], Pi +.233 [+.130,+.364] (cell Wilcoxon p = .004 / .34 / .0002; Holm across the three primary comparisons still significant for mobile and Pi, not for N-BaIoT); worst-client TPR: mobile −.126, N-BaIoT −.031 (p < 1e-6), Pi +.033 (p = .17) | no policy dominates: LAB wins success at small budget, loses worst-client TPR | PASS |
| C3-P6 | Allocation headroom | `c3_analyze.py` [4] | hetero scenarios | as above | 0–4 | uniform | @oracle (∝ ε + .02), @2stage | oracle allocation | success at equal B | LAB-EB: oracle allocation lowers success in every domain, 0/5 seeds positive (hetero scenarios, k = 10–20): mobile −.125 [−.154,−.096], N-BaIoT −.144 [−.178,−.100], Pi −.256 [−.319,−.194]; CLEAN-K-SHRINK at k = 20: two-stage +.12 (mobile .96 vs .84), +.11 (Pi .47 vs .36), −.08 (N-BaIoT .90 vs .98); oracle −.06 / +.36 / −.46 | ε-proportional allocation starves clean clients; no consistent headroom | PASS (mechanism line closed, estimator-dependent nuance recorded) |
| C3-P7 | Clean-client safety | `c3_analyze.py` [5] | ε = 0 and clean clients in hetero scenarios | as above | 0–4 | LOCAL | all policies | n/a | clean-client FPR, TPR | all clients clean: LAB-* = LOCAL exactly; CLEAN-K variants overshoot FPR at ≤ 5% budgets (e.g. mobile CLEAN-K-SHRINK k=5 FPR .139); clean clients inside heterogeneous scenarios (k=10): FPR LOCAL .046–.070; CLEAN-K-SHRINK .082 / .122 / .045; **LAB-POOL .198 / .229 / .199; LAB-EB .142 / .181 / .170** (mobile / N-BaIoT / Pi); GLOBAL FPR ≈ 0 with TPR .19–.41 | pooled estimators harm clean clients when contamination is heterogeneous; the archived "clean clients not harmed" held only for homogeneous ε = 0 | PASS |
| C3-P8 | α and pool-size sensitivity | `c3_budget.py --alpha/--pool` | mobile, N-BaIoT, Pi | as above | 0–4 | see P4 | see P4 | ORACLE-TRUE | success | α = .10: LAB-EB success .85–.99 from 1% budget (mobile, N-BaIoT, Pi), CLEAN-K reaches .97–.99 at k = 10 (5%; = 1/α); mobile N = 100/300 and N-BaIoT N = 100/400/1,000: same crossover at k ≈ 20; Pi N = 30: no policy exceeds .8 except CLEAN-K at k = 20 of 30 items | crossover budget ≈ 1/α verified items per client; small pools break everything | PASS |
| C3-P9 | Split sensitivity | `c3_scores.py nbaiot` (tail) vs `nbaiot_chunk` | N-BaIoT | tail vs chunked | 0–4 | primary chunked | tail | n/a | success | tail: CLEAN-K-SHRINK .97 at 10% of pool, LAB-EB ≤ .79; LAB-EB − CLEAN-K-SHRINK +.045 [+.005,+.085]; oracle allocation −.106; chunked: .98 / .67 / +.049 / −.144 | same conclusions | PASS |
| C3-P10 | Archived P59 estimator (`LAB-EB-TAU`, `HYB`) | `legacy/p5_budget.py` | archived scores | random | 5 | CLEAN-K-SHRINK | LAB-EB-TAU | oracle | success | archived: LAB-EB-TAU .58–.72 vs oracle .92–1.0; CLEAN-K-SHRINK ties or beats in 3 of 6 cells | tau-corrected and hybrid variants were added after seeing results and are excluded from the frozen policy set | SUPERSEDED |
| C3-P11 | Archived allocation `LAB-EB-ALLOC` (∝ peer suspicion) | `legacy/p5_budget.py` | archived scores | random | 5 | uniform | suspicion-proportional | n/a | success | no consistent gain | consistent with C3-P6 | SUPERSEDED (agrees) |
| C3-P12 | Archived label-free peer trimming (P59b) | `docs/poc/temp/c1_run.py` (`v1`–`v4`) | archived | random | 5 | LOCAL | PEER-TRIM, admission | oracle | recovery | recovers 20–30% of the gap and harms clean pools | label-free repair ruled out | REJECTED |

### 3.1 Split sensitivity and remaining runs

The N-BaIoT contiguous-tail split and the chunked split give the same qualitative picture; numbers are in `out/analysis_nbaiot_a0.05_N200.txt` (tail) and `out/analysis_nbaiot_chunk_a0.05_N200.txt` (chunked). Pool sizes 100/400/1,000 and α = .10 for N-BaIoT are in the corresponding `out/analysis_*` files.

## 4. Claim & Gate Matrix

| Claim | Required evidence | Current evidence | Gate | Result | Allowed wording | Forbidden wording | Remaining experiment |
|---|---|---|---|---|---|---|---|
| C1 Contamination reduces TPR at unchanged FPR | G-Failure: LOCAL TPR ≤ 0.6 × oracle in ≥ 2 of 3 domains | .43, .49, .43 of oracle (mobile, N-BaIoT chunked, Pi) for random+top | as stated | PASS | "in the simulated scenarios, TPR fell to 43–49% of the oracle value at unchanged FPR" | "in deployed systems" | confirmatory seeds |
| C2 Stealth contaminants do little damage | LOCAL TPR ≥ .8 × oracle | .68/.68/.62 vs .80/.76/.70 = 85/90/88% | as stated | PASS | "low-scoring contaminants cost 10–15% of TPR" | | none |
| C3 Below about 1/α verified items per client pooled estimates win; at and above it verified-benign shrinkage wins | same-sign in ≥ 2 of 3 domains; crossover within a factor of two across pool sizes | crossover at k ≈ 20 (α = .05) or 10 (α = .10) in all three domains and all tested pool sizes (Section 3, C3-P4, C3-P8); at α = .10 LAB-EB stays ≥ CLEAN-K-SHRINK at 1–2% budgets | G-Domain | PASS | "the crossover occurred near 1/α verified items per client, independently of pool size (100–1,000)" | "5–10% of the pool" | confirmatory seeds; α = .02 |
| C4 Allocation gives no reliable gain | G-Allocation | oracle allocation lowers success for LAB-EB in all domains; CLEAN-K-SHRINK two-stage +.12/+.11/−.08 | as stated | PARTIAL (no gain for LAB, mixed for CLEAN-K-SHRINK) | "ε-proportional allocation did not help; a two-stage rule helped one estimator in two of three domains" | "allocation never helps" | confirm two-stage rule on confirmatory seeds |
| C5 About 1/α verified items per client recover most oracle security | success ≥ .8 at k = 1/α in ≥ 2 domains | CLEAN-K-SHRINK at k = 20: .86 (mobile), .98 (N-BaIoT), Pi CLEAN-K .82 at k = 20 of 60 | as stated | PASS (Pi needs the unshrunk CLEAN-K; support 60) | "about twenty verified items per client at a 5% target" | a pool percentage without the α qualifier | more Pi support (not available) |
| C6 Estimated-contamination policies do not harm clean clients | G-Clean | fails for LAB-POOL/LAB-EB under heterogeneous contamination (clean-client FPR .14–.23) | ≤ .02 change | **FAIL** for LAB-*; PASS for LAB-LOCAL; CLEAN-K-SHRINK +.036–.052 FPR (borderline) | "pooled trimming raises clean-client FPR to 3–4× α under heterogeneous contamination" | "safe for clean clients" | policy that protects clean clients (exploratory) |
| C7 α = 1% unsupported | pool of 200 cannot resolve 1% | archived α = .01: success ≤ .33; N = 30 Pi results | as stated | PASS (archived + N = 30) | "not supported by pools of this size" | | none |
| C8 A new estimator beats the best simple policy | G-Complexity | LAB-EB beats CLEAN-K-SHRINK in success at small budgets only; loses worst-client TPR and clean-client safety | as stated | NOT TRIGGERED / FAIL | "no method claim" | any method claim | none |

## 5. Literature Collision Matrix

Targeted 2024–2026 searches (September 2026); not systematic.

| Closest paper | Collision | Remaining distinction | Novelty risk | Status |
|---|---|---|---|---|
| Bashari, Sesia, Romano, *Robust Conformal Outlier Detection under Contaminated Reference Data* (ICML 2025; arXiv 2502.04807) | contaminated calibration data; **Label-Trim** with a limited labelling budget | single detector; federated heterogeneous pools, global budget across clients, client-level constraints, IoT and mobile domains | **HIGH** for "labelling budget to repair contaminated calibration" | PASS |
| Wang, *When Does Trimming Help Conformal Prediction? A Retained-Law Diagnostic under Calibration Contamination* (arXiv 2605.06204) | when trimming helps under contamination | no multi-client budget | MED | PASS |
| Shahid, *When Average Calibration Fails: Site-Conditional Federated Conformal Risk Control* (arXiv 2606.20115) | pooled calibration violates coverage at many sites; risk-curve shrinkage between local and pooled | no contamination, no verification budget | MED | PASS |
| Wen, Simeone, Xing, *Efficient Federated Conformal Prediction with Group-Conditional Guarantee* (arXiv 2603.14198) | federated calibration under heterogeneous groups | no contamination | LOW–MED | PASS |
| Kamiguchi, Nishio, federated NIDS with contaminated unlabeled data (arXiv 2607.25439) | contamination in federated IDS | training contamination, not calibration thresholds; no verification budget | MED | PASS |
| Scholten et al., *Provably Reliable Conformal Prediction Sets in the Presence of Data Poisoning* (ICLR 2025) | poisoned calibration data | image classification, guarantees via aggregation | LOW–MED | PASS |
| *Self-Poisoning in Adaptive OOD Detection: A Sharp-Threshold Theory and Certified Label-Free Calibration* (arXiv 2607.21673) | contaminated calibration for detectors | label-free; single detector | LOW–MED | PARTIAL (not read) |
| DATP / DATP-CP (own prior work) | client-specific thresholds and conformal variants | this chapter concerns contamination and labels | LOW | PASS |

Most dangerous collision: Label-Trim. The exact statement from us that would collide: "a small labelling budget spent on a suspicious subset of a contaminated calibration pool restores detection quality." Remaining unanswered: heterogeneous contamination across federated clients, one shared budget and its allocation, client-level worst-case constraints, clean-client harm of pooled estimators, crossover against verified-benign thresholds. Contribution type: **empirical / operational**. Not methodological.

## 6. Implementation-Risk Register

| ID | Risk | Category | Status | Mitigation |
|---|---|---|---|---|
| R-01 | ScienceDB availability and licence | availability, licensing | PARTIAL | eight files (87.7 MB) fetched by id with size checks; cite both licences; do not redistribute rows |
| R-02 | Pi dependence within infection runs; global scaling | leakage, preprocessing | BLOCKED (cannot remove) | stated as optimistic; used as replication only |
| R-03 | N-BaIoT attack-row handling changes AUROC | design | PASS (fixed) | attack rows kept; investigation script |
| R-04 | Injected contamination only | validity | PARTIAL | claims limited to simulation |
| R-05 | Small Pi pools (60) | support | PARTIAL | α ≥ 5% only; N = 30 sensitivity |
| R-06 | Client harm from pooled estimators | design | PASS (found) | reported; G-Clean gate |
| R-07 | Legacy pool drawn with replacement for small support | leakage-like | PASS (fixed) | without replacement with assertion |
| R-08 | Memory and runtime | runtime | PASS | seconds to minutes per domain; N-BaIoT cache ≈ 15 min |
| R-09 | Mobile contaminants from calibration malware only | construct | PARTIAL | limitation |
| R-10 | Reproducibility from a clean environment | reproducibility | PARTIAL | `run_all.sh`; clean-environment rerun not executed |
| R-11 | Seeds re-train scorers; contamination and scorer variance mixed | statistics | PARTIAL | seed as unit; report both |

## 7. Negative Evidence

| Finding | Rules out |
|---|---|
| Oracle allocation (∝ ε + .02) lowers success (mobile, N-BaIoT, Pi) | contamination-proportional allocation as a mechanism |
| Two-stage adaptive allocation ≈ uniform except for CLEAN-K-SHRINK at ≥ 10% budget in two domains | adaptive allocation as a robust improvement |
| LAB-POOL/LAB-EB raise clean-client FPR to .14–.23 | pooled estimators as clean-client-safe |
| GLOBAL threshold: FPR ≈ 0, TPR .18–.41 | a single global threshold as a repair |
| LAB-LOCAL (per-client Label-Trim): success .14–.27 at 1–2% budget | per-client estimation at small budgets |
| α = 1%: pools of 200 cannot resolve it (archived) | 1% targets |
| No policy beats CLEAN-K-SHRINK on worst-client TPR in mobile and N-BaIoT | new estimator claim |
| Archived label-free peer trimming (P59b): 20–30% recovery, clean-pool harm | label-free repair |
| Archived τ-corrected and hybrid estimators were added post hoc | any hybrid as a confirmatory method |

## 8. Roadmap Decisions and Evidence

| Decision | Evidence |
|---|---|
| Three domains with mobile primary | C3-P3 to C3-P7 in all three |
| Pools without replacement, N per domain | R-07; support counts (Section 2) |
| Fixed closed policy set, no tau/hybrid variants | C3-P10 |
| Success and oracle-gap recovery with FPR-deviation recovery | recovery above 1 from FPR overshoot for CLEAN-K at small budgets (C3-P4) |
| Budget grid as fraction of pool (1–20%) | crossover location (C3-P4) |
| Include oracle and two-stage allocation | C3-P6 |
| Clean-client metric and G-Clean gate | C3-P7 |
| α ∈ {.05, .10} with α = .01 as limit case | C3-P8 |
| Chunked N-BaIoT split primary, contiguous-tail as sensitivity | audit (autocorrelation, nearest-neighbour), C3-P9 |
| Keep attack rows in N-BaIoT | C3-P2 |
| No method claim unless G-Complexity | C3-P5, C3-P7 |
| Ten confirmatory seeds 100–109 | five seeds give cell-level significance but seed-level variance (scorer) not resolved |

## 9. Contradictions between experiments or documents (investigated)

1. **N-BaIoT scorer AUROC: ≈ 1.0 (first regeneration) versus .65–.99 (archived).** Reproduced the archived sampling (`investigate_nbaiot.py`): AUROC [.988, .869, .867, .807, .911, .859, .652, .838, .881]. Only difference: the regeneration removed repeated attack windows (20–40% of sampled attack rows); with attack rows kept the regeneration gives .61–.99, matching the archive. Repeated attack windows are the hard, benign-like ones. **Resolved**: attack rows are kept; the first regeneration is preserved in `out/superseded_attackdedup/` (SUPERSEDED, biased easy).
2. **Duplicate groups spanning labels in the Pi data.** Archived audit: "No duplicate group spans two labels". Actual: device 7 has 480 vectors shared by labels 1 and 2 (both malware). **SUPERSEDED**; irrelevant for the binary task.
3. **"CLEAN-K-SHRINK ties or beats the estimator" (archived P59) versus new results.** New: LAB-EB has higher success at ≤ 5% budgets in mobile (+.186) and Pi (+.233); CLEAN-K-SHRINK wins at ≥ 10% and on worst-client TPR. Reasons: the archived estimator variants were tuned on results; the new policy set is fixed; success metric definition uses per-client constraints; α and pool sizes differ. **Both true in different regimes**; new protocol adopted.
4. **"Clean clients are not harmed" (archived) versus new clean-client harm.** Archived test used homogeneous ε = 0 only, where LAB-* equals LOCAL exactly (reproduced). Heterogeneous scenarios reveal FPR .14–.23 for pooled estimators. **Both true**; the roadmap gate uses clean clients inside heterogeneous scenarios.
5. **Archived pools drawn with replacement.** For mobile clients with fewer than N benign calibration items the archive resampled with replacement, duplicating scores and understating quantile noise. New code draws without replacement and asserts support.
6. **SciDB scorer reproducibility.** AUROC per client identical to the archive to three decimals (`compare_legacy_scores.txt`): PASS.

## 10. Unresolved questions

- Whether the crossover budget is stable for other scorers, pool sizes and natural contamination (unknowable with public data).
- A policy that keeps the small-budget advantage of pooled estimation without clean-client harm (exploratory only; not part of the frozen set).
- Full text of arXiv 2607.21673.
- Clean-environment rerun of `run_all.sh` (R-10).
- N-BaIoT tail-versus-chunk comparison table (values in `out/analysis_nbaiot_*.txt`).

## 11. Reproduction commands

```bash
cd "docs/Candidate 3/poc"
python ../../"Candidate 1"/poc/build_lamda_cache.py          # mobile cache (shared)
./fetch_scidb.sh                                                  # 8 files, 87.7 MB -> data/cache/scidb/
./run_all.sh                                                  # audits, scorers, budget runs, analysis texts
python c3_label_efficiency.py > out/analysis_label_efficiency.txt
```

## 12. Final audit passes

### Pass 1 — scientific audit

| Check | Result | Status | Action taken |
|---|---|---|---|
| RQs match experiments | RQ1 → C3-P3; RQ2 → C3-P4, C3-P5; RQ3 → C3-P6; RQ4 → C3-P4; RQ5 → C3-P7; RQ6 → C3-P8, C3-P9 | PASS | |
| Baselines fair | verified-benign shrinkage (three weights), per-client Label-Trim, pooled and empirical-Bayes trimming, GLOBAL, oracle bounds; all use the same pools and the same verified items | PASS | |
| Metrics answer RQs | success and oracle-gap recovery (RQ2, RQ4); worst-client TPR/FPR (RQ1, RQ2); clean-client metrics (RQ5); recovery above 1 caused by FPR overshoot is exposed by FPR-deviation recovery | PASS | FPR-deviation recovery replaced an FPR-excess metric that was uninformative (contamination lowers FPR) |
| Claims follow from planned evidence | C6 fails, C4 partial, C3 and C5 restated at 1/α after the pool-size sweep | PASS | claim wording changed from a pool percentage to a verified-item count |
| Novelty bounded | Label-Trim distinction stated; no method claim | PASS | |
| No post-hoc method promoted | tau-corrected and hybrid estimators from the archive excluded; crossover rule exploratory | PASS | |
| Statistics | seed-cluster bootstrap and Holm added to the analysis; with five seeds the Wilcoxon floor is p = .0625 | PARTIAL | ten confirmatory seeds |
| Injected contamination | acknowledged; natural contamination unmeasurable | PARTIAL | limitation |
| Data errors | attack de-duplication error found and fixed; replacement-sampled pools fixed | PASS | Section 9 |
| Meaningless control removed | a "benign contaminants" control is tautological; replaced by the contaminant-type contrast | PASS | Roadmap edited |

### Pass 2 — implementation audit

| Check | Result | Status | Action taken |
|---|---|---|---|
| Files exist | LAMDA cache (Candidate 1 builder), N-BaIoT CSVs (9 devices), ScienceDB device files (8, 87.7 MB, re-fetched, sizes match the manifest) | PASS | |
| Required columns exist | mobile features as Candidate 1; N-BaIoT 115 columns; Pi 31 features + `label` | PASS | |
| Labels support the task | benign/malware per file (N-BaIoT), per label value (Pi), VT rule (LAMDA) | PASS | |
| Sample support adequate | pools without replacement need benign calibration ≥ N: mobile 304+, N-BaIoT 1,966+, Pi 68+; code asserts | PASS | |
| Client construction possible | natural site keys: markets and devices | PASS | |
| Splits possible | components (mobile), chunks and contiguous tail (N-BaIoT), de-duplicated random (Pi); leakage assertions inside `c3_scores.py` (pass for seeds 0–4; Pi also seed 100) | PASS | |
| Metrics computable | `c3_analyze.py`, `c3_label_efficiency.py` outputs in `out/` | PASS | |
| Hidden data dependency | ScienceDB file ids (public API; endpoint may change), N-BaIoT unpacked CSVs (the `.rar` files are not used), Candidate 1 LAMDA cache | PARTIAL | ids recorded in `legacy/p4_scidb_list.py` and `run_all.sh` |
| Runtime and storage | scorers ≈ 1–2 min per seed; N-BaIoT cache ≈ 15 min and about 1 GB on disk; budget runs seconds to minutes | PASS | |
| Hardware | none beyond a workstation; CPU fallback added | PASS | |
| Reproducibility from a clean environment | `run_all.sh` lists every step in order; clean reinstall not performed | PARTIAL | Section 10 |
