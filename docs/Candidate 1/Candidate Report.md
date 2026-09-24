# Candidate 1 — Complementary Threat Knowledge in Federated Android Malware Detection: Candidate Report (audit trail and evidence dossier)

Companion to [Roadmap.md](Roadmap.md). Status vocabulary: `PASS`, `PARTIAL`, `MISSING`, `BLOCKED`, `REJECTED`, `SUPERSEDED`.

Paths are relative to `docs/Candidate 1/poc/` unless prefixed with `docs/poc/temp/` (archived exploratory workspace, kept unchanged) or `legacy/` (copies of exploratory scripts and outputs for this candidate). Raw data are outside the repository (`CASE_RAW`); caches are in `data/cache/` (git-ignored). Human-readable analysis output: `out/analysis_c1.txt` (regenerate with `python c1_analyze.py`).

## Dashboard

| Item | Status | Summary |
|---|---|---|
| Overall status | **PASS with narrowed claims** | A real, reproducible collaboration benefit on unseen families exists, but only 30–40% of it is complementary knowledge; the complementary part is unstable across family sets |
| Chapter fit | PASS | Android malware, data-local collaboration, unseen threats |
| PhD relevance | PASS | Collaborative FL malware detection, non-IID and heterogeneous clients, scarce local evidence / cold start, worst-client performance, when collaboration helps, negative transfer. Not IoT; second-domain test of the thesis question |
| Dataset readiness | PASS | LAMDA + AndroZoo fully inspected; split leakage found and fixed; family semantics documented |
| POC readiness | PASS | 5-seed main scenario, dose-response, natural axis, second scorer, second family set, leakage sensitivity, own-market check |
| Novelty confidence | MODERATE-LOW | Direct collisions on "FL helps clients with missing families" and on prototype exchange; decomposition with pooling control is the remaining distinction |
| Mechanism / headroom | Headroom small | Best simple arm recovers 69–89% of the oracle gap for the mean client; residual 0.05–0.08 recall (< 0.10 trigger); worst-client noisy. No mechanism justified |
| Implementation readiness | PASS | Scripts, assertions, `run_all.sh`; confirmatory seeds 100–109 not yet run |
| Biggest remaining risk | Complementary effect is small (≈ +0.06 mean), positive for family set 1 and the natural axis, about zero for family set 2; AVClass2 adware families share behaviour so "unseen family" is partly "seen behaviour" |

## 1. Inventory and mapping of pre-existing artifacts

Nothing was deleted. Legacy copies are in `legacy/`; originals remain in `docs/poc/temp/`.

| Artifact | Supports | Status | Note |
|---|---|---|---|
| `legacy/p6_unseen_family.py`, `p6_unseen_family_s{0..4}_n{1500,6000}_a0.05.json`, `p6_unseen_family_analyze.py` | P60 controlled-exposure study | SUPERSEDED by `c1_study.py main` | Package-only grouping; results differ (Section 9, item 1) |
| `legacy/p6b_nofam.py`, `p6b_nofam_s*_n6000.json` | no-family-anywhere control | SUPERSEDED | Refilled sample size not matched; rerun with size-matched refill |
| `legacy/p6_mia.py`, `p6_mia_s*_n{500,3000}.json` | membership-inference on federated detectors | REJECTED | AUC 0.48–0.58, no measurable leakage; separate topic |
| `legacy/c3_audit.py`, `c3_audit_output.txt` | LAMDA family audit | SUPERSEDED | Reported 0% singleton share; actual 40.7% (Section 9, item 3) |
| `legacy/c4_repack_audit.py`, `c4_repack_poc.py` | cross-market package identity | PRESERVED (negative) | linking same package across markets gave no detection gain |
| `legacy/p3_engine.py` | model/FL engine | REUSED as `engine.py` | unchanged |
| `docs/poc/temp/p3_lamda_v2.py`, `p3_extras.py`, `p4_*` and their JSON | collaboration-scope POCs P26–P48 (local/global/cluster/blend/negative transfer/robust aggregation) | PRESERVED (negative evidence) | central ≥ every FL arm; fixed blends ≈ central; no negative transfer to repair; see Section 7 |
| `docs/poc/Final Report.md` P60 section | earlier numbers | PRESERVED | contradictions logged in Section 9 |

## 2. Dataset Verification Matrix (`build_lamda_cache.py`, `audit_lamda.py` → `out/audit_lamda.json`)

| Check | Expected | Actual | Status | Evidence | Consequence |
|---|---|---|---|---|---|
| Source and licence | LAMDA on Hugging Face, MIT; AndroZoo access terms | `README.md`: `license: mit`; citation ICLR 2026 (Haque et al.); AndroZoo `latest.csv.gz` present (3.52 GB) | PASS | file inspection | cite both; no raw redistribution |
| Files | parquet by year, metadata, feature mapping | `var_thresh_0.01/<year>/<year>_{train,test}.parquet` for 12 years (2015 absent), `metadata.csv` 124,417,238 B, `feature_mapping.csv` (925 rows) | PASS | listing | one cache builder |
| Row counts | 1,008,381 | 1,008,381; unique SHA-256 = rows; all matched in AndroZoo catalogue | PASS | audit (`unique_hash`, `no_market_join = 0`) | identity valid |
| Schema | README: 4,561 features (variance 0.001) | parquet has 930 columns = `hash`, `label`, `family`, `vt_count`, `year_month`, 925 binary `feat_*`; README describes the default 4,561-feature configuration, so the 0.01 variant is 925 (earlier notes said 920) | PARTIAL | schema dump; `feature_mapping.csv` | use 925; document README mismatch |
| Feature values | binary | {0, 1}; minimum prevalence 1.01%; no constant column | PASS | audit | none |
| Preprocessing | filter by provider | variance threshold applied by the provider over the whole corpus (global preprocessing) | PARTIAL | README | cannot be undone; limitation |
| Labels | malware = VT ≥ 4 | label ≡ (`vt_count` ≥ 4) with zero violations; benign = 0 detections (grey zone 1–3 absent); prevalence 36.7% | PASS | `label_vt_rule_violations_ge4 = 0` | no natural label noise of the grey-zone kind |
| Timestamps | date meaning | `year_month` = year and month of the `added` field in `metadata.csv` (100% year agreement); it is not verified as build or first-seen time; 2015 absent | PARTIAL | metadata inspection | used only for Google Play era split (≤ 2018 / ≥ 2019) |
| Duplicates: hash | none | none | PASS | audit | none |
| Duplicates: feature vector | some | 452,155 rows (44.8%) share a feature vector with another row; 2,418 identical-vector groups carry both labels | PASS (found) | `dup_feature_vector_rows`, `..._label_conflict_groups` | **splits must group on feature vector as well as package**; label noise floor |
| Package identity | present | 772,200 distinct packages; 111,368 packages have multiple rows; 9,109 packages carry conflicting labels across rows; 24,803 packages occur in more than one primary market; 19,069 packages have single-market rows in more than one client market | PASS | audit | package grouping alone leaks; component grouping (package ∪ vector) adopted; 0 components straddle partitions |
| Market membership | single market for clients | 935,789 rows list exactly one market; 66,053 list two, up to 8 | PASS | `n_markets_dist` | clients use single-market rows only |
| Client definitions | Play (2 eras), Anzhi, AppChina | play_e 297,387 rows (74,220 malware, 25%); play_l 342,209 (18,965; 5.5%); anzhi 104,287 (90,801; 87%); appchina 88,282 (73,578; 83%) | PASS | `p60_client_sizes` | clients differ mostly in prevalence and era; local training samples of 6,000 rows contain ~330 malware for play_l |
| Family labels | AVClass2 | 151,985 distinct malware labels: 1,381 named families + 151,075 malware rows carrying `singleton:<sha256>` labels (40.7% of malware); 115 named families with ≥ 150 samples; top 16 named families = 40.6% of malware; benign family = `benign` | PASS (semantics established) | `mal_singleton_share`, `named_families_ge150`, `top_families` | only named, supported families are eligible; family = AV token, adware-dominated |
| Family support per client | enough for hiding | (package-hash partition) e.g. `dowgin` train per client [55, 4, 16,705, 793]; `kuguo` [47, 2, 8,495, 2,431]; `airpush` [5,535, 182, 179, 1,277]; play_l holds fewer than 100 training samples of 13 of the 16 studied families | PASS | `p60_family_support` | for many (client, family) pairs natural exposure is already near zero, so hiding acts mostly on the owning market |
| Family × market concentration | concentrated | dowgin and kuguo mostly Anzhi; airpush, dnotua, revmob mostly Play; gappusin, adwo mostly AppChina | PASS | `family_x_market_top` | unseen-family test rows come mostly from the peer market that holds the family: cross-market confound (own-market check added) |
| Conflicting labels across markets | some | 800 packages benign on Play but malicious elsewhere (archived audit) | PASS | `docs/poc/Dataset & POC Audit.md` | not used as a label source |
| Static feature limits | static only | Drebin-style tokens; no dynamic behaviour | PASS | README | claims limited to static detection |
| Sample size and imbalance | adequate | markets range 2.5 k–640 k apps; malware share 1.8%–99.7% by market | PASS | `single_market` | four large clients only |
| Runtime and storage | feasible | cache 170 MB; one seed ≈ 2 min (GPU); dose ≈ 8 min | PASS | logs | none |
| Supported claims | unseen-family detection recall at fixed FPR | supports recall/FPR decomposition in a simulated federation; does not support drift, real-organisation, privacy, or dynamic-behaviour claims | PASS | above | Roadmap Sections 26, 31 |

## 3. POC Matrix

Commands from `docs/Candidate 1/poc/`. Scorer: 128-unit MLP over 925 binary features unless stated; FedAvg 30 rounds × 3 epochs; FedProx μ = 0.05; fine-tune 3 epochs; per-client training sample 6,000 rows. Threshold at the client's benign-validation (1−α) quantile. Outputs `out/c1_<mode>_s<seed>_<scorer>_f<fams>_n<n>_<grouping>.json`. All values α = 0.05 unless stated.

| ID | Question | Script | Input | Split | Seeds | Baseline | Candidate | Oracle | Metric | Result | Interpretation | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1-P0 | Dataset facts | `build_lamda_cache.py`, `audit_lamda.py` | LAMDA, AndroZoo | n/a | n/a | n/a | n/a | n/a | counts | Section 2 | inputs valid; leakage source found | PASS |
| C1-P1 | Split/exposure assertions | `python c1_study.py check SEED` | cache | component 60/20/20 | 0, 3 | n/a | n/a | n/a | assertions | pass: hidden families absent from the owner's training data, present in peers; evaluation rows only from the test partition; thresholds from benign validation only; no component straddles partitions | no leakage of the construction | PASS |
| C1-P2 | Does the failure exist? Main controlled exposure | `c1_study.py main` | 4 clients, family set 1 | component | 0–4 | local | central, FedAvg, FedProx, FedAvg + FT, blends | oracle local/FedAvg/central (full exposure) | unseen-family recall, worst client, known recall, FPR | local .453 (worst client .289); central .667; FedAvg .637; FedProx .628; FT .619; oracle central .694; realised FPR .046–.050 | local misses peer-known families; simple collaborative arms recover 69–89% of the oracle gap (mean client) | PASS |
| C1-P3 | Pooling versus complementary knowledge | same (`*_nofam` arms) | same | component | 0–4 | no-family-anywhere central / FedAvg (size-matched) | central − nofam | n/a | paired differences | total +.214 [+.179,+.249]; generic pooling +.149 [+.092,+.206]; complementary **+.065 [+.038,+.092]** (5/5 seeds), share 30%. FedAvg: total +.185, generic +.117, complementary +.067 [+.050,+.085], share 36% | most of the gain is pooling; complementary part is small but positive | PASS |
| C1-P4 | Worst client | same | same | component | 0–4 | local | central, FedAvg | n/a | worst-client recall | worst client: local .289, central .339, FedAvg .353; complementary +.101 [+.016,+.187] (central, 5/5) but generic pooling −.051 [−.136,+.034] | worst-client gain is entirely complementary (pooling alone does not help the worst client) but intervals are wide | PARTIAL |
| C1-P5 | Dose-response | `c1_study.py dose` | families hidden at their owner; peers keep m samples in total | component | 0–4 | dose 0 | central, FedAvg, FT | all | recall vs effective peer samples | central .571 at 0 samples, .593 at ≈ 12, .642 at ≈ 53, .656 at ≈ 90, .674 at ≈ 292; FedAvg .510 → .644; FedAvg + FT .517 → .630; local ≈ .38–.46 (varies with the re-drawn training samples); means over 5 seeds | benefit rises with peer samples and is small below ≈ 10–50 samples per family | PASS |
| C1-P6 | Natural exposure axis (no hiding) | `c1_study.py natural` | 12 (client, family) pairs where the client holds ≤ 5% of the family, peers ≥ 150, own-market test ≥ 15 | component | 0–4 | local | central, FedAvg, FedProx, FT | central without the family anywhere | own-market recall | local .648; central .802; FedAvg .720; central-no-family .637; complementary +.165 [+.132,+.197] (5/5) | large effect where the client holds a few samples of a family peers hold in bulk; the no-family control removes the client's own scarce samples too | PASS (different construct; not comparable to C1-P3) |
| C1-P7 | Own-market evaluation of hidden families | `c1_study.py main` (`*_own`) | as C1-P2 | component | 0–4 | local | central | central-no-family | own-market recall (removes cross-market confound) | local .344; central .485; central-no-family .425; total +.141 [+.041,+.240]; generic +.081; complementary +.059 [−.026,+.145] (4/5 seeds) | complementary share rises to ≈ 40% but is not statistically resolved with 5 seeds | PARTIAL |
| C1-P8 | Second scorer: linear | `c1_study.py main --scorer linear` | same | component | 0–2 | local | central, FedAvg | no-family | recall | local .384; central .578; no-family .554; complementary +.024 [+.010,+.037]; generic +.170 | same ordering; complementary smaller | PASS |
| C1-P9 | Second scorer: gradient boosting | `c1_study.py gbdt` | same | component | 0–4 | local | pooled | no-family, oracle | recall | local .515; pooled .686; no-family .631; oracle .716; complementary +.055 [+.046,+.064] (5/5); generic +.116 | decomposition is not an MLP artefact | PASS |
| C1-P10 | Second family set | `c1_study.py main --fams 2` | 16 further families | component | 0–2 | local | central | no-family | recall | local .435; central .586; no-family .580; complementary **+.006 [−.028,+.040]**; generic +.146 | complementary knowledge vanishes for the second set: pure pooling | PASS (negative for generality) |
| C1-P11 | Leakage sensitivity | `c1_study.py main --grouping package` | as C1-P2 | package only | 0–2 | local | central | no-family | recall | local .531 (vs .453 with component grouping); central .704; complementary +.108 [+.012,+.203] | package-only splits inflate local recall by ≈ 0.08 and the complementary component by ≈ 0.04 | PASS |
| C1-P12 | Other FPR targets | same (α .01, .10) | as C1-P2 | component | 0–4 | local | central | oracle | recall | α = .01: local .219, central .508, no-family .444 (complementary +.064); α = .10: local .589, central .758, no-family .688 (+.070); FedAvg at .01 recovers only 60% of the gap | conclusions hold; α = .01 has ~30 validation benign scores per client at the threshold and is noisy | PASS |
| C1-P13 | Known-family cost | same | as C1-P2 | component | 0–4 | local | central, FedAvg, FT | n/a | known-family recall | central +.033 [+.019,+.047]; FedAvg −.005 [−.020,+.010]; FT −.004 [−.013,+.005] | no known-family cost | PASS |
| C1-P14 | FL versus pooled; blends | same | as C1-P2 | component | 0–4 | central; FedAvg + FT | FedAvg, FedProx, blends | n/a | unseen recall | FedAvg −.029 [−.061,+.002], FedProx −.038 [−.062,−.014], FT −.048 [−.077,−.018] versus central; local/FedAvg blend vs FT +.000; local/central blend vs FT +.019 [−.010,+.049] | pooling beats FL variants; the simple blend is not better than the best FL arm | PASS |
| C1-P15 | Which families cannot be rescued | same | per-family recall | component | 0–4 | local | central | oracle central | family recall | oracle recall < .6: plankton .59, smsreg .53, leadbolt .57, youmi .45, hiddad .35, revmob .30, dnotua .25 (7 of 16). Rescued (central − local ≥ .2): zdtad, dowgin, inmobi, kuguo, ewind. Complementary gain ≥ .10: inmobi +.31, revmob +.15, leadbolt +.13, smsreg +.10; dowgin +.02 (detected .95 even when no client has it) | irreducible families are feature-level failures; some "unseen" families are detected from other adware families (shared behaviour) | PASS |
| C1-P16 | Family support versus benefit | `c1_analyze.py` | 16 families | component | 0–4 | n/a | Spearman | n/a | correlation | support ~ complementary gain ρ = 0.00 (p = 1.0); support ~ oracle recall ρ = 0.34 (p = 0.20) | family rarity does not explain complementary benefit | PASS |
| C1-P17 | Residual headroom for a mechanism | derived | C1-P2 | component | 0–4 | best simple arm | none | oracle central | residual gap | mean: central −.027, FedAvg −.057, FT −.075 below oracle; worst client: FedAvg above oracle (noise) | < 0.10 threshold; Stage-4 mechanism not justified | PASS (mechanism line closed) |
| C1-P18 | Membership inference on federated Android detectors (side question) | `legacy/p6_mia.py` | LAMDA markets | random | 0–2 | n/a | loss-threshold MIA | n/a | AUC | 0.48–0.58 | no leakage under this weak attack | REJECTED |
| C1-P20 | Negative control: family labels permuted among malware | `c1_study.py main --permute-fam` | 16 pseudo-families of preserved sizes | component | 0–2 | local | central, no-family central | oracle | complementary contrast | local .640; central .778; no-family .775; complementary **+.003 [−.034,+.041]** (1/3 seeds positive); generic +.134 | the complementary component is family-specific and vanishes under label permutation; the pooling component persists | PASS |
| C1-P19 | Collaboration-scope POCs P26–P48 (archive) | `docs/poc/temp/p3_*.py`, `p4_*.py` | LAMDA markets, N-BaIoT, Pi | random | 5 | central | local/global/cluster/blend | oracle arm | BA, worst-FPR | central ≥ FL arms; fixed blends ≈ central; no negative transfer; valid-set arm selection unreliable | supports "no selection mechanism" | PASS (negative) |

Sampling noise: adding the own-market evaluation changed the random-number consumption of the main scenario; the rerun moved `central_nofam` from .614 to .602 and the complementary mean from +.053 to +.065. Seed-level noise of this size (≈ ±0.01) is the resolution of the decomposition.

## 4. Claim & Gate Matrix

| Claim | Required evidence | Current evidence | Gate | Result | Allowed wording | Forbidden wording | Remaining experiment |
|---|---|---|---|---|---|---|---|
| C1 Local clients miss peer-known families | central/FedAvg − local positive in ≥ 8/10 seeds | +.214, +.185; 5/5 seeds | as stated | PASS (design seeds) | "local recall on hidden families is .45 versus .67 with peers, at 5% FPR" | "zero-day detection" | confirmatory seeds |
| C2 Complementary knowledge is positive | ≥ .03, interval excludes 0, ≥ 8/10, label-permutation null | set 1 +.065 [+.038,+.092]; own-market +.059 [−.026,+.145]; linear +.024; GBDT +.055; **set 2 +.006**; permutation control +.003 (null, as required) | as stated | PARTIAL | "small and family-dependent" | "collaboration transfers unseen-family knowledge" | permutation control; confirmatory seeds |
| C3 Generic pooling explains the majority of the gain | share > 50% | share 30% (cross-market), ≈ 58% pooling own-market, 64% FedAvg | interval excludes 50% | PARTIAL: majority is pooling in all constructs except natural scarcity | "most of the gain is available without family-specific peer knowledge" | "collaboration is mostly generic" (unqualified) | interval on the share |
| C4 Dose-response | monotone trend, ≥ .03 above dose 0 at ≥ 100 samples | central .570 → .585 (12) → .638 (52) → .669 (289) | as stated | PASS | "gains appear once peers hold tens of samples per family" | "one sample is enough" | more seeds |
| C5 Irreducible families exist | ≥ 3 families with oracle recall < .6 in ≥ 8/10 seeds | 7 of 16 | as stated | PASS | "7 of 16 studied families are detected poorly even with full exposure" | "collaboration cannot help these families" | feature-level analysis |
| C6 Worst-client benefit | worst-client complementary interval excludes 0 | +.101 [+.016,+.187] central; +.107 [+.003,+.211] FedAvg (4/5) | as stated | PARTIAL | "the worst client benefits mainly from complementary knowledge; intervals are wide" | "guarantees the worst client" | confirmatory seeds |
| C7 Known-family cost small | within ±0.02 for FedAvg | −.005 [−.020,+.010] | as stated | PASS | "no measurable known-family cost for FedAvg" | | none |
| C8 Blends do not beat the best collaborative arm | blend − best ≤ 0 | +.000; +.019 [−.010,+.049] | as stated | PARTIAL (not better, not shown worse) | "a 50/50 blend was not better than FedAvg + fine-tune" | "blends hurt" | none |
| C9 Effect generalises across model class | positive complementary in linear and GBDT | +.024, +.055 | as stated | PASS | | | none |
| C10 Effect generalises across families | family set 2 positive | +.006 | as stated | FAIL (narrow: "for the studied set 1") | "for family set 1; not for set 2" | "for Android families" | more family sets |
| C11 Natural exposure shows complementary benefit | natural-scarcity effect > 0 | +.165 (5/5) | as stated | PASS (different construct) | "where a client holds ≤ 5% of a family, pooling with peers adds .15 own-market recall" | comparison of magnitudes with C2 | none |
| C12 New mechanism | residual gap > .10 | .03–.08 | G-Complexity | NOT TRIGGERED | "no mechanism was warranted" | any new method claim | none |

## 5. Literature Collision Matrix

Targeted 2024–2026 searches (September 2026); not systematic. Novelty risk HIGH/MED/LOW.

| Closest paper | Collision | Remaining distinction | Novelty risk | Status |
|---|---|---|---|---|
| *Federated multimodal malware classification under non-IID data* (Cybersecurity, 2026, s42400-026-00630-2) | construct class-dominant partitions and "malware-missing clients"; reports that FedAvg learns absent malware behaviour through collective knowledge when fewer than ten clients miss a class (search snippet; full text not read) | controlled exposure, no-family-anywhere control, decomposition, dose-response, worst-client, Android static features at market scale | **HIGH** for the statement "FL helps clients with missing families" | PARTIAL (read full text) |
| Darwish et al., *FedP3E* (arXiv 2507.07258; IEEE TIFS 2025) | prototype exchange gives clients representations of unseen classes; N-BaIoT | measurement not mechanism; Android; pooling control | MED | PASS |
| Abhijit et al., *Federated transfer learning for rare attack class detection in NIDS* (Sci Rep 2025) | transfers knowledge from clients holding a class to those lacking it | same | **HIGH** for a mechanism claim; not for ours | PASS |
| *EdgeFedCIL* (Sensors 2026, from archive) | federated class-incremental IDS for novel attacks | same | MED | PASS |
| *A distributed framework for zero-day malware detection using federated ensemble models* (PLOS One 2026) | zero-day, ensemble, family evaluation | same | MED | PASS |
| *FL-MalDrift* (Sci Rep 2025); *Droidware* (2026); *AndroIDS* (arXiv 2506.17349); *FedHGCDroid* (Entropy 2022) | Android FL under drift, non-IID label skew, security hardening | not a controlled-exposure decomposition | MED | PASS |
| Haque et al., *LAMDA* (ICLR 2026); *McNdroid* (arXiv 2605.06894) | benchmarks; drift; no FL | dataset provenance; McNdroid is a candidate second corpus | LOW | PASS |

Most dangerous collision: the Cybersecurity 2026 paper. Statement from us that would collide: "federated learning lets clients detect malware families they have never observed." Remaining unanswered: how much of that benefit is complementary knowledge as opposed to generic pooling, how it depends on peer sample count, and which families remain undetectable. Contribution type: **empirical / measurement**. No "first" or "novel" claim.

## 6. Implementation-Risk Register

| ID | Risk | Category | Status | Mitigation |
|---|---|---|---|---|
| R-01 | LAMDA or AndroZoo unavailable, AndroZoo access terms | availability, licensing | PARTIAL | local copies; document terms; only aggregates released |
| R-02 | README feature count mismatch (4,561 vs 925) | schema | PARTIAL | audit-derived count in Roadmap |
| R-03 | AVClass2 label semantics and singleton labels | label semantics | PASS | eligibility rules; wording "AVClass2-labelled family" |
| R-04 | Insufficient support per client for hiding | support | PARTIAL | eligibility thresholds; play_l has fewer than 100 training samples of 13 of 16 families; natural axis restricted to 12 pairs |
| R-05 | Duplicate feature vectors leak across splits | leakage | PASS (fixed) | component grouping; `check` mode |
| R-06 | Cross-market confound in unseen-family evaluation | design | PARTIAL | own-market metric; natural axis; complementary share reported both ways |
| R-07 | Global variance filtering by provider | preprocessing | PARTIAL | limitation |
| R-08 | Complementary effect unstable across family sets | scientific | PARTIAL | claim narrowed; more family sets in confirmatory design |
| R-09 | Runtime and memory | runtime | PASS | ≈ 2 min per seed on GPU; 3 GB RAM |
| R-10 | Chronology unusable | data | BLOCKED (not needed) | era split only; no drift claim |
| R-11 | External replication corpus missing | replication | PARTIAL | McNdroid candidate; internal replications only |
| R-12 | Stochastic noise ±0.01 in the decomposition | statistics | PARTIAL | 10 confirmatory seeds; paired intervals |
| R-13 | Reproducibility from clean environment | reproducibility | PARTIAL | `run_all.sh`, `paths.py`; clean-environment rerun not executed |

## 7. Negative Evidence

| Finding | Rules out |
|---|---|
| Complementary +.006 for family set 2 | a general claim that peer family knowledge is a large component |
| Complementary +.059 [−.026,+.145] own-market | claiming statistical resolution of the own-market component with 5 seeds |
| Generic pooling for the worst client −.051 | attributing worst-client gain to pooling |
| Local/FedAvg logit blend not better than FedAvg + fine-tune (+.000) | "simple blend" as the strongest cheap baseline |
| Central ≥ FedAvg/FedProx/FT (−.029, −.038, −.048) | FL matching pooled training |
| Support does not predict complementary benefit (ρ = 0.00) | family-rarity explanation |
| Package-only splits inflate local recall (+.08) and complementary (+.04) | using package-only grouping |
| MIA AUC 0.48–0.58 | privacy-leakage angle |
| Archived collaboration-scope POCs (P26–P48): no negative transfer, no selection gain | peer-selection / personalisation mechanisms |
| No mechanism trigger (residual < .10) | new method claim |

## 8. Roadmap Decisions and Evidence

| Decision | Evidence |
|---|---|
| Components (package ∪ feature vector) as split unit | 44.8% duplicate vectors; C1-P11 shows inflation |
| Four clients, single-market, Play by era | client table in Section 2; other markets too small or too one-sided |
| Hide one family group per client; size-matched no-family control | C1-P3 |
| Report mean and worst-client and complementary share | C1-P3, C1-P4 |
| Own-market metric and natural-scarcity axis | R-06, C1-P6, C1-P7 |
| Dose-response with effective counts | C1-P5 (caps bind at 6,000 rows per client) |
| Second scorer (linear, GBDT) and second family set | C1-P8–C1-P10 |
| α = 0.05 primary, 0.01 and 0.10 sensitivity | C1-P12 |
| Ten confirmatory seeds 100–109, paired t intervals, Holm for three primary contrasts | five seeds give intervals of width ≈ 0.05; noise ±0.01 |
| No mechanism unless residual > .10 | C1-P17 |
| Gates C2 and C6 as "PARTIAL-capable" (narrow wording, not kill); label-permutation control included | C1-P7, C1-P10, C1-P20 |
| Irreducible-family list with feature-level follow-up | C1-P15 |

## 9. Contradictions between experiments or documents (investigated)

1. **Complementary gain: archived P60 versus new run.** Archived (package-only grouping, refill not size-matched): mean complementary +.075 (central) / +.098 (FedAvg); worst client +.105–.110. New (component grouping, size-matched refill): +.065 / +.067; worst client +.101 / +.107. New package-only rerun: +.108. The archived value lies between the two: leakage through identical feature vectors inflates the complementary component; refill matching changes the control's size. Local recall also differs (archived .491, new .453, new package-only .531). **Explained; new protocol adopted.** Status: earlier numbers SUPERSEDED.
2. **Archived "families are naturally market-concentrated, so exposure asymmetry is realistic".** True (Section 2), but the concentration also means unseen-family test rows come mostly from the peer market that holds the family; the own-market metric shows complementary +.059 versus +.065 cross-market, similar in size but with lower statistical resolution. **PARTIAL**, not contradictory.
3. **Family label purity.** Archived `c3_audit_output.txt`: "share SINGLETON/empty/unknown: 0.0". Actual: 151,075 malware rows (40.7%) carry `singleton:<sha256>`. The archive tested the exact string `SINGLETON`, but the prefix is lower case. **SUPERSEDED**; consequence: only named, supported families are eligible (unchanged).
4. **Feature count 920 versus 925.** Archived notes say 920; the parquet has 925 `feat_*` columns. **SUPERSEDED**; cache uses 925.
5. **Rerun drift.** Same seeds, additional evaluation code changed RNG use: `central_nofam` .614 → .602 (Section 3). Documented as noise floor.

## 10. Unresolved questions

- Whether the complementary component is statistically resolved in the own-market metric (needs the confirmatory seeds).
- Whether the permutation control holds on all ten confirmatory seeds (3 design seeds run).
- Full text of the 2026 Cybersecurity paper (PARTIAL).
- Additional family sets (a third set would resolve the set 1 versus set 2 disagreement).
- Feature-level explanation of irreducible families.
- Whether McNdroid can serve as an external replication with market-like clients (unverified).

## 11. Reproduction commands

```bash
cd "docs/Candidate 1/poc"
python build_lamda_cache.py && python audit_lamda.py     # ~10 min, aggregate audit
python c1_study.py check 0                                  # assertions
./run_all.sh                                              # all experiments (two parallel streams); SEEDS="100 ... 109" for the confirmatory run
python c1_analyze.py > out/analysis_c1.txt
```

## 12. Final audit passes

### Pass 1 — scientific audit

| Check | Result | Status | Action taken |
|---|---|---|---|
| RQs match experiments | RQ1 → C1-P2; RQ2 → C1-P3, C1-P20; RQ3 → C1-P5; RQ4 → C1-P4, C1-P15; RQ5 → C1-P13, C1-P14, C1-P17; RQ6 → C1-P6–C1-P12 | PASS | none |
| Baselines fair | same training rows per client in every arm (size-matched refill); local, FedAvg, FedProx and fine-tune share the model class; FedAvg/FedProx hyper-parameters are fixed, not tuned | PARTIAL | local-epoch and FedProx-μ ablations added to the Roadmap; not yet run |
| Metrics answer RQs | unseen recall (RQ1–4), known recall (RQ5), realised FPR (validity), worst client (RQ4); no metric without an RQ | PASS | AUROC kept as a secondary check only |
| Claims follow from planned evidence | C2, C6 and C10 carry PARTIAL/FAIL outcomes already; wording bounded | PASS | complementary-share interval defined (seed bootstrap of a ratio of means) |
| Novelty framing bounded | empirical decomposition only; collisions listed | PASS | no "first/novel" wording |
| No post-hoc mechanism | none promoted; mechanism trigger (residual > .10) is a pre-existing rule, not tuned to these results | PASS | none |
| Confounds identified | cross-market test rows (own-market metric added); adware families share behaviour (dowgin detected without any client holding it) | PASS | reported as limitation and in Section 3 |
| Negative controls exist | no-family-anywhere, dose 0, permuted-family (null +.003), package-only leakage contrast | PASS | permutation control implemented during the audit |

### Pass 2 — implementation audit

| Check | Result | Status | Action taken |
|---|---|---|---|
| Files exist | LAMDA parquet (12 years), `metadata.csv`, `feature_mapping.csv`, AndroZoo `latest.csv.gz` opened by `build_lamda_cache.py` | PASS | |
| Required columns exist | `hash`, `label`, `family`, `vt_count`, `year_month`, 925 `feat_*`; AndroZoo `sha256`, `pkg_name`, `markets` | PASS | |
| Labels support the task | VT ≥ 4 rule verified with zero violations; family = AVClass2 token; 41% singleton labels excluded by eligibility | PASS | |
| Sample support adequate | assertions pass on seeds 0, 3 and 100–109; every client has ≥ 832 unseen-family test rows and ≥ 109 peer training rows of its hidden families in all ten confirmatory seeds | PASS | |
| Client construction possible | four single-market clients; play_l has ≈ 330 malware in a 6,000-row sample | PASS | |
| Splits possible | 486,848 components; 0 straddle partitions | PASS | |
| Metrics computable | all in `out/analysis_c1.txt` | PASS | |
| Hidden data dependency | AndroZoo catalogue requires registration (3.5 GB); feature parquet is public | PARTIAL | documented in Roadmap Section 8 |
| Runtime and storage | ≈ 2–3 min per main seed (GPU), cache 170 MB, RAM ≈ 3 GB | PASS | CPU fallback added (`engine.py`); CPU runtime not measured |
| Hardware | none beyond a workstation; GPU optional | PASS | |
| Reproducibility from a clean environment | `run_all.sh` reproduces the analysed set; clean reinstall not performed | PARTIAL | listed in Section 10 |
