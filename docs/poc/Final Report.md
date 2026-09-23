# CASE-Android Pre-Implementation Scientific Audit

Audit date: 2026-09-23. This report is a decision document for revising the roadmap. The authoritative `docs/Roadmap.md` and `docs/technical_doc.md` were not modified.

## Executive conclusion

**Keep CASE-Android, narrow its language, and strengthen the evidence plan.** The best supported identity is a reproducible study of **recorded claim portability and reliability-qualified report scoping** across named Android execution contexts. It should not be presented as discovery of context sensitivity, a malware classifier, a causal study of Android versions, or a formal risk-guarantee method.

SELENE is a feasible primary dataset: the shared cache contains the eight compact Parquet files (29.78 MB), and their hashes/joins were inspected. Exact pairing gives 30,746 APKs. In two package-grouped exploratory splits, source-only pooled logistic models improve Brier score over indicator-persistence baselines in both directions, but the gains are modest and asymmetric: 4.0–9.7% Brier skill. A broken-pair control removes the advantage. This supports a confirmatory test of incremental signal; it does not establish production utility.

Add a small, explicit **four-state estimand** so the study distinguishes stable-present, source-only, target-emergent and stable-absent recorded evidence. SELENE contains 57,745 target-emergent APK/flag rows; pooled target emergence among source-absent claims is 27.98%. Keep this separate from source-positive recurrence and do not call it behavior “emergence.”

Promote KronoDroid to an external **context-level descriptive replication**: direct file inspection yields 63,316 valid SHA pairs and a broken-pair control. Its syscall units do not equal SELENE’s semantic security indicators, and prior cross-device studies occupy the broad behavior-difference question. Treat this as a narrow robustness/replication lane, not as proof that the CASE reporting model generalizes.

Keep persistence as the key baseline, pooled logistic as the primary candidate, and raw source-side evidence counts as a secondary variant. The model should remain simple. Do not freeze a formal risk-control claim, a granularity frontier, time/family/claim OOD, analyst-time savings, or an Android-wide portability claim. Reconcile SELENE licenses and the report’s technical details, then freeze one confirmatory protocol before using outer-test outcomes.

## Current design audit

### What is strong

- The estimand is operational and bounded: for a source-positive APK × indicator claim, estimate whether the same **processed observation** appears in a named target context.
- The roadmap already excludes fresh device collection, malware classification, behavior truth, causal Android-version attribution, federated-learning performance, and unsupported analyst-productivity claims.
- SELENE provides exact paired SHA identities, two named Android/API contexts, source-side behavior features, and an existing reproducible exploratory base.
- The design treats source/target direction explicitly, groups by package, separates prospective baselines from retrospective intersection, and forbids target-derived threshold selection.
- The existing implementation contract is unusually strong on provenance, leakage tests, package bootstrap, tie handling, report-level aggregation, and idempotency.

### What limits value and breadth

- Current SELENE recurrence is high (85.5–90.0% micro), so persistence already performs well. A large average-precision score can be misleading; Brier/log loss and the risk/coverage curve should lead.
- The 19 flags include exact duplicates and threshold-derived flags. They are not 19 independent behavioral concepts.
- The paired sample is selected: Android-10 paired versus unpaired prevalence differs by 3.20 points on average and 8.72 points at maximum.
- Run duration differs (median 188.33 s for Android 10 versus 143.79 s for Android 14). Context means bundled observation differences; do not claim a causal Android-version effect.
- The fidelity oracle includes only 56 shared hashes. It cannot serve as independent behavior truth or a broad high-fidelity replication.
- A single SELENE artifact cannot sustain general claims about heterogeneous Android execution, unseen time periods, families, evidence kinds, or devices.
- The current selective results are only retrospective fixed-coverage diagnostics. Calibration-only deployment-style policies have not yet been evaluated.

## Dataset audit

| Role | Recommendation | Exact finding and limits |
|---|---|---|
| **PRIMARY** | SELENE / ARTEMIS compact features | 44,485 Android-10 and 30,751 Android-14 runs; 30,746 exact hash pairs; 22,475 paired package groups. Local artifacts include `analyses`, `run_features`, `fidelity_oracle`, `fidelity_evidence`. No event-level or lifecycle files were in the local cache. Source flags/counts/timing are usable; IDs, labels and target fields are not predictors. |
| **CORE REPLICATION** | KronoDroid (narrow descriptive context replication) | Four actual CSV archives give 63,316 valid unique SHA pairs after duplicate exclusion. 288 syscall counts align, with zero missing dynamic cells. The CSV schema (484 columns) conflicts with the public README’s 200+289 count; family labels disagree on 33,838 paired hashes. Use exact valid pairs, binary syscall-presence labels and context-only conclusions; reconcile schema and exclude family OOD. |
| **SECONDARY** | KronoDroid source-only recurrence replication | Feasible at 25.68 MB compressed; CPU-only. Requires a later model-level protocol on matched syscall claims and package grouping. Do not treat syscall calls as semantic security reports. |
| **OPTIONAL / BLOCKED** | AndroCT | 6.3 GB; nominally 35,974 apps each with emulator and Galaxy S4 traces, 10-minute Monkey runs and method-call edges. Actual identities/duplicates unverified. Use requires faculty/permanent-staff agreement; redistribution/commercial use prohibited. Direct collision on cross-device behavior differences. |
| **DIAGNOSTIC / BLOCKED** | DYNAMISM 2016–2023 | Zenodo files are Restricted. Metadata says Android 9, one-second aggregates and 1,821 repeated-run apps. Candidate for same-context stochasticity, but paired tables and missingness are unverified. |
| **BLOCKED** | CIC-InvesAndMal2019 | Page describes install, pre-reboot and post-reboot captures, but exact run identity/comparable features are unverified. The listed 5,000 installs conflict with 426 malware + 5,065 benign (=5,491). |
| **DIAGNOSTIC / DEFER** | TraceDroid | Local 45.18 MB historical profile set; one analysis context, no demonstrated same-APK context pair. Can support a separate historical cohort question, not cross-context recurrence. |
| **REJECT as outcome data** | AndroZoo metadata | Hash/date catalog only; no paired target behavior outcome. Use only for external metadata if license/access permits. |

Full per-file counts, checksums, semantics and references are in [Dataset Audit.md](Dataset%20Audit.md). The primary SELENE card says the contexts are environment splits, the finite Monkey-driven traces preserve unredacted strings, and non-observation is not proof an app cannot perform a behavior. The audit must honor both the SELENE and upstream ARTEMIS licenses and cite both artifacts ([dataset card](https://huggingface.co/datasets/serrooT/selene-android-paper-artifacts), [license/limitations](https://huggingface.co/datasets/serrooT/selene-android-paper-artifacts/blob/main/README.md)).

## PoC results

### SELENE recurrence and model comparison

One source-positive APK × one of 19 released flags is one claim. The two directions use the same paired APK population and package-grouped 80/20 holdouts (seeds 20260923 and 314159). Models: global train prevalence, train-only per-indicator persistence, pooled Boolean logistic, evidence-count-only, activity-volume-only, rich Boolean+count+volume, and duration-normalized count/rich variants. No target fields entered predictors.

| Direction | Split | Holdout recurrence | Persistence Brier | Boolean Brier (BSS) | Rich Brier (BSS) | Rich log loss | Rich AP |
|---|---:|---:|---:|---:|---:|---:|---:|
| Android 10 → 14 | 20260923 | 89.96% overall | 0.07033 | 0.06458 (8.18%) | **0.06349 (9.74%)** | 0.20930 | 0.98759 |
| Android 10 → 14 | 314159 | 89.96% overall | 0.07025 | 0.06518 (7.21%) | **0.06414 (8.69%)** | 0.21016 | 0.98762 |
| Android 14 → 10 | 20260923 | 85.48% overall | 0.10675 | 0.10453 (2.08%) | **0.10226 (4.21%)** | 0.33279 | 0.95756 |
| Android 14 → 10 | 314159 | 85.48% overall | 0.09953 | 0.09776 (1.78%) | **0.09554 (4.01%)** | 0.31383 | 0.96055 |

Rich-versus-persistence Brier improvements are 0.00611–0.00685 forward and 0.00399–0.00450 reverse. The 300-draw package-cluster bootstrap intervals are positive for all four cells (forward: [0.00509, 0.00725] and [0.00577, 0.00794]; reverse: [0.00309, 0.00490] and [0.00351, 0.00544]). These intervals quantify sampling variability within these holdouts only. They are not external confirmation or final 10,000-resample inference.

The simplest baselines matter. Global prevalence is weaker than persistence. Boolean pooled logistic improves over persistence. Evidence-count-only improves modestly beyond Boolean, and the rich model improves further. Raw counts beat the tested per-second normalized counts in both directions and both seeds; this weakens the claim that exposure duration explains the richer model signal. Activity volume alone is comparable to or slightly below Boolean forward and helps reverse. This is a small, consistent incremental effect, not a large model discovery.

The broken-pair control permutes held-out target APK rows. In all four direction/seed combinations, Boolean/count/rich models become worse than persistence (rich Brier difference from persistence ranges −0.00456 to −0.00781). This supports that genuine pairing contributes to the advantage.

### SELENE four-state and reporting diagnostics

Across 30,746 × 19 paired APK/flag cells: stable-absent `n00=148,629`; target-emergent `n01=57,745`; source-only `n10=37,919`; stable-present `n11=339,881`. Micro recurrence is 89.96% forward / 85.48% reverse. Among source-absent claims, 27.98% have a target observation; the mean indicator-specific emergence rate is 50.99%. Keep this as a distinct descriptive estimand.

At score-ranked 50% coverage on each held-out test, rich-model non-recurrence risk is approximately 0.30% forward and 3.07–3.35% reverse. At 80%, it is about 3.32–3.35% and 7.02–8.11%. Persistence is worse in these holdouts, especially at 50%. The same APK-level report proxy shows fewer unsupported claims/report. **These are retrospective diagnostics:** held-out labels determine the ranking evaluation and no calibration-only threshold was selected. They cannot support a deployed policy claim or formal risk budget.

### KronoDroid paired context diagnostic

On 63,316 valid SHA pairs, with an app/syscall claim defined as a released count > 0:

| Direction | Source-positive claims | Recurrence | Broken-pair recurrence | Support≥100 syscall-macro recurrence |
|---|---:|---:|---:|---:|
| Emulator → device | 2,328,191 | 59.14% | 51.84% | 50.04% |
| Device → emulator | 2,007,336 | 68.59% | 60.11% | 57.70% |

This is useful external evidence of a same-app context association. It does not test CASE’s source-only prediction model or semantic reporting effect. The older [cross-device behavioral consistency study](https://doi.org/10.1016/j.mlwa.2022.100357) already covers broad cross-device behavior differences, so CASE must not claim that general finding as novel.

## Failed, blocked and rejected ideas

- **Formal distribution-free risk control:** not implemented; package and report dependence plus target shift invalidate casual use of i.i.d. guarantees. Keep empirical risk/coverage only.
- **Evidence granularity frontier:** promising but not run. SELENE event-level layers are not local; AndroCT requires permission and 6.3 GB. Do not spend scope on a lane without exact identity/claim mappings.
- **Portability drift / future period:** not run. Current two SELENE contexts are versions, not chronological cohorts; Krono’s mod/submission dates are not verified trace times.
- **Malware-family OOD:** do not promote. Krono family disagreement is 53.4% across unique paired hashes; SELENE is not a family-held-out study.
- **Unseen-claim OOD:** 19 flags contain duplicate/derived indicators, leaving too few independent claim families to separate claim transfer from persistence.
- **Same-context repeat instability:** DYNAMISM is a strong candidate but files are restricted; no estimate was computed.
- **CIC reboot transitions:** no artifact-level identity or numerical reconciliation; reject it as a primary dataset until the join is proven.
- **Complex models (GAM, random forest, boosting, MLP, sequence):** no PoC evidence justifies added complexity. The logistic ladder already yields a repeatable modest increment; a later nonlinear comparator is a single ceiling sensitivity only.
- **Analyst-time savings, operational security impact, and federation:** not tested and should not be claimed. Report-level claim counts are an offline proxy only.

## Best-performing feasible variants

1. **Best defensible model:** pooled direction-specific L2 logistic over claim identity, 19 source flags, event/count fields and source activity/duration. It is interpretable, CPU-only and stable across the two discovery splits.
2. **Best lean candidate:** pooled Boolean logistic; it already improves over per-indicator persistence. If the full source-count contract complicates implementation, keep this primary and demote rich features to sensitivity.
3. **Best evidence-strength variant:** raw released count features. Duration-normalized features were worse in all tested direction/split cells. Preserve normalization as a sensitivity because the direction-specific run duration differs.
4. **Best operational comparison:** persistence versus CASE risk/coverage and report proxy at 50% and 80% coverage. Treat current values as descriptive. The confirmatory protocol must choose thresholds on calibration groups only.
5. **Best external lane:** Krono exact-hash syscall recurrence and broken-pair diagnostic, with semantic scope clearly separated from SELENE.

No method should be selected solely from its largest test score. The evidence says rich features are promising but only modestly better than Boolean; all variants remain recorded in [PoC Matrix.md](PoC%20Matrix.md) and `temp/` results.

## Novelty assessment

Broad Android context dependence, emulator/device differences, system-call inconsistency, behavior abstraction, concept drift, selective prediction, and conformal risk control are established neighboring contributions. The defensible residual is the **estimand and report operation**: estimate recurrence for a recorded source-positive APK × claim in a named target context, then make a prospective report-scope decision without interpreting non-observation as proof of absence.

Do not claim firstness. Do not claim that SELENE is ground truth. Do not claim portability across Android generally. Details and closest-work comparisons are in [Novelty Audit.md](Novelty%20Audit.md).

## Recommended scientific identity

**Recommended title:** *CASE-Android: Reliability-Qualified Scoping of Recorded Android Behavioral-Security Evidence Across Execution Contexts*.

**Central statement:** Dynamic analysis reports record finite observations made under a particular execution context. CASE estimates whether a source-context claim is likely to recur as a recorded observation in a named target context, and exposes that estimate as a claim-scoping signal. Its result is about the released observation process, not an app’s full capability or behavior truth.

**Contribution framing:** (1) a paired claim-level portability dataset/protocol for processed Android evidence; (2) a leakage-controlled evaluation of recurrence signal beyond persistence; (3) an empirically evaluated selective reporting view; and (4) an external, semantically narrower context replication. The report mechanism and evidence semantics matter more than a new model architecture.

## Recommended estimands

| Priority | Estimand | Decision |
|---|---|---|
| Primary | Source-positive recurrence: `P(target flag=1 | source flag=1)` for exact paired APK × indicator × direction, evaluated on held-out package groups. | Retain as primary. |
| Primary descriptive | Symmetric four-state paired transitions (`n00/n01/n10/n11`), per-indicator recurrence/disagreement and target emergence among source-absent claims. | Add as a separate descriptive estimand; do not collapse emergence into recurrence. |
| Secondary | Incremental source-only probability quality beyond global prevalence, per-indicator persistence and activity-only baselines. | Retain; judge with Brier/log loss and paired package uncertainty. |
| Secondary | Selective scoping: non-recurrence risk versus claim coverage and recurrence retention, with a calibration-only operating point. | Retain; policy thresholds must be selected without outer-test outcomes. |
| Secondary | Evidence strength/structure incremental value beyond Boolean flags and activity volume, with raw and duration-normalized counts. | Add conditionally; make no strength claim unless confirmatory. |
| Secondary replication | Paired emulator/device syscall-presence recurrence and broken-pair contrast in KronoDroid. | Add as a different evidence unit; report separately from semantic SELENE claims. |
| Exploratory | APK-level report coverage/contamination and target-emergence report counts. | Keep as offline proxy only; do not infer analyst value. |
| Deferred/rejected | Formal risk guarantee, time/family/claim OOD, multi-hop/worst-context, context-vs-repeat variance, clinical-style severity costs. | Defer until valid data/method assumptions are audited. |

## Recommended RQs

1. **RQ1 — Recorded portability structure:** How often do paired source and target contexts agree, disagree, or exhibit target-recorded evidence when source evidence was not recorded?
2. **RQ2 — Source-only signal:** Do source flags and source-run evidence properties estimate target recurrence better than global and indicator-persistence baselines under package-held-out evaluation?
3. **RQ3 — Scoping value:** Does a calibration-only CASE policy improve non-recurrence risk/coverage and retain useful claim/report content compared with persistence-based scoping?
4. **RQ4 — Boundaries and replication:** How stable are recurrence and scoping effects across direction, indicators, paired-population/fidelity sensitivities, and one independently paired context family with compatible limitations?

Keep granularity, time drift, unseen family/claim, and run stochasticity as named extension questions, not extra core RQs.

## Recommended claims

| Claim | Required evidence / gate | Current support | Risk | Status |
|---|---|---|---|---|
| A. Portability heterogeneity | Paired four-state tables, per-indicator/direction intervals; G1–G3, G7, G22 | SELENE and Krono show substantial measured asymmetry and disagreement. | Only named processed contexts. | **Promote, bounded.** |
| B. Source-only recurrence signal beyond persistence | Package-held-out Brier/log loss, bootstrap, negative control; G5–G10, G22 | Positive modest skill in both SELENE directions and seeds; broken-pair advantage disappears. | One dataset and exploratory splits. | **Promote for frozen confirmation.** |
| C. Evidence strength adds value | Boolean/count/volume/raw-normalized paired ablations; G8, G11, G22 | Raw counts improve slightly; normalized counts lower. | Redundant derived features and exposure effects. | **Secondary.** |
| D. Selective policy improves scoping | Calibration-only policy, untouched test curve/operating points vs persistence; G12–G14 | Retrospective fixed-score coverage only. | No calibration-only policy evidence. | **Conditional.** |
| E. Formal risk-controlled policy | Valid cluster-aware risk control; G13 | None. | Dependence/shift assumptions unresolved. | **Defer.** |
| F. Granularity/portability frontier | Matched abstraction levels and report semantics; G3, G7, G11 | None yet. | Missing event files; AndroCT permissions. | **Defer.** |
| G. Whole-report reliability benefit | APK-report grouped calibrated policy and report bootstrap; G14 | Descriptive report proxy only. | No analyst or deployment outcome. | **Secondary, proxy only.** |
| H. Independent context replication | Same CASE estimand/model/baselines in a second compatible dataset; G19–G20 | Krono descriptive pairing only. | Different syscall unit; known cross-device literature. | **Partial; do not make broad claim yet.** |
| I/J. Portability drift/future apps | Verified observation times and chronological OOD; G15 | None. | Current time fields/context design do not establish valid future period. | **Defer.** |
| K. Malware-family OOD | Harmonized family keys and grouped holdout; G16 | Invalid/discordant Krono family labels. | Label mismatch. | **Blocked.** |
| L. Claim OOD | Independent claim families, leave-family-out; G17 | 19 SELENE flags, several redundant. | Too few independent claims. | **Defer.** |
| M. Context vs stochastic instability | Same-context repeats and context pairs under comparable units; G20 | Restricted DYNAMISM metadata only. | No traces inspected. | **Blocked/diagnostic.** |
| N. Target-recorded emergence | Four-state counts, source-absent denominator; G1–G3, G7 | SELENE target-emergence rate is measurable and varies by indicator. | Not proof behavior newly began. | **Promote as descriptive secondary.** |
| O. PhD relevance | Conceptual alignment only; no FL/IoT claim | Motivation plausible. | Overgeneralization. | **Keep as motivation.** |

The complete A–O specification and gate statuses are in [Claim and Gate Audit.md](Claim%20and%20Gate%20Audit.md).

## Recommended gates

Use the 25 detailed gates in [Claim and Gate Audit.md](Claim%20and%20Gate%20Audit.md), organized as:

- **Validity gates G0–G9:** access/license; identity; context semantics; claim comparability; provenance; leakage; grouping; support; baseline fairness; negative-control integrity.
- **Claim-promotion gates G10–G24:** probability quality; richer-feature value; selective policy; risk-control validity; report-level value; temporal OOD; family OOD; claim OOD; fidelity; independent dataset/context replication; complexity; sensitivity; reproducibility; final claim wording.

A structural failure blocks only the affected dataset/claim. A small effect narrows claim strength; it does not kill the project. Formal guarantee gate G13 is required only if the report uses a guarantee label.

## Recommended models and baselines

1. **Primary candidate:** direction-specific pooled L2 logistic with claim-indicator identity and source Boolean flags. It is simple and already outperforms persistence on both discovery splits.
2. **Secondary feature ladder:** released source evidence counts; count-per-duration variant; total activity volume; rich combined model. Keep transformations fixed before frozen evaluation.
3. **Baselines:** global train prevalence; smoothed per-indicator persistence; source activity-volume-only. Optionally Boolean CASE as the lean model. Same split, same source-positive rows, no target-side features.
4. **Do not implement every model from the candidate ladder.** One later nonlinear tabular comparator may serve as a ceiling if necessary; no MLP or sequence model is justified by current evidence.
5. **Krono replication:** separate syscall occurrence scorer only after a frozen claim definition. Do not pool its 288 syscalls with SELENE semantic indicators as if they were the same claim ontology.

## Recommended metrics

- Primary probability: Brier and log loss; Brier skill versus persistence. Report AP only with prevalence and persistence reference.
- Paired structure: `n00/n01/n10/n11`, conditional recurrence by direction, disagreement/Jaccard or prevalence difference when useful.
- Selective reporting: risk at fixed coverage and coverage at predeclared risk target, recurrence retention, absolute risk reduction, coverage retained. Use calibration-only thresholding; descriptive fixed-rank diagnostics are labeled as such.
- Calibration: reliability curve, intercept/slope; ECE descriptive only if binning details are fixed.
- Report proxy: coverage, unsupported transferred claims/report, fraction of reports with ≥1 unsupported transfer, and recurrence retention.
- Weighting/strata: claim-micro, indicator-macro, package/report-macro; direction and rare-indicator support. Add malware/benign only where labels are semantically valid and not predictors.
- Uncertainty: paired package-cluster bootstrap; do not treat claims as independent.

Drop metrics that do not answer a stated question. Do not use test-set-selected thresholds as risk guarantees.

## Recommended future experiment suite

1. Freeze SELENE file hashes, dual-license citation, schema and exact SHA/package pair manifest.
2. Report paired versus unpaired population differences and actual context/run-duration distributions.
3. Build source-positive claims and separate source-absent emergence rows; save four-state transitions for each indicator/direction.
4. Freeze package-grouped fit/calibration/test folds; every package belongs to the test set once. Preserve the historical exploration separately.
5. Compare global, indicator persistence, volume-only, Boolean pooled L2, raw-count pooled L2 and normalized-count sensitivity on the same rows.
6. Run paired proper scores, calibration, indicator/package macro summaries and 10,000 package-cluster bootstrap draws.
7. Run broken-pair target-permutation control, alternative split manifests, row-order/tie checks, and feature/indicator redundancy sensitivities.
8. Select thresholds from calibration data only; report all test risks/coverage and `NO_OPERATING_POINT` when a target risk is unsupported.
9. Report one-APK report proxies and recurrence retention; do not claim time savings.
10. Add the KronoDroid external study as a distinct syscall-present estimand: exact SHA pair filtering, duplicate audit, four states, class strata, package grouping, broken-pair control, then one simple source-only model if its schema discrepancies are resolved.
11. Keep AndroCT, DYNAMISM and CIC as extension candidates only after their access and identity gates pass.

## Proposed confirmatory protocol

After revising the roadmap:

1. Recheck the live SELENE and ARTEMIS licenses/citation files and retain raw artifacts outside Git.
2. Freeze exact input checksums, indicator meanings (including broad/non-derived subset), source feature allowlist and the paired population.
3. Define the primary population as all exact paired APK identities and the unit as one source-positive APK × indicator × direction. Define emergence separately over source-absent units.
4. Freeze deterministic package-grouped outer folds and a disjoint package-grouped calibration partition inside training. Keep the historical discovery results out of confirmation claims.
5. Freeze directions, no-target predictors, logistic model settings, smoothing for persistence, proper metrics, operating points and bootstrap plan before inspecting outer-test results.
6. Calibrate thresholds on calibration groups only. If the target risk budget cannot be reached, report no operating point rather than moving the budget.
7. Compare methods on identical test claims; bootstrap packages (not individual claims); report micro, indicator macro and package/report macro.
8. Include broken-pair control, indicator redundancy/broad-only, duration normalization, missing-feature/noise sensitivity, selected-versus-unpaired audit, direction reversal and all indicators with sparse-support NA reasons.
9. Freeze a limited independent KronoDroid replication protocol only after resolving 484-column versus README feature counts and excluding family-dependent features.
10. Treat all discovered design choices—including pooled logistic, claim identity, raw counts, 50/80% coverage views and current split seeds—as exploratory-informed. The future run is confirmatory only for its newly frozen comparisons; external replication remains necessary for generality.

## Scope boundaries

CASE still must not claim:

- that the APK cannot perform a behavior because it was not recorded;
- true behavior absence/presence, malware verdict, family attribution or malicious intent;
- a causal Android-version effect from two bundled execution environments;
- universal portability to Android versions, devices, users or observation conditions;
- formal risk guarantees without a valid dependence/shift-aware method;
- time drift from APK dates treated as execution timestamps;
- analyst time savings or operational security gains without direct measurement;
- a federated-learning or IoT result from an Android report study.

## Roadmap change matrix

| Current roadmap component | Change | Evidence and recommended edit |
|---|---|---|
| Research statement / title | **MODIFY** | Keep claim-level recurrence/report scope; use “recorded evidence” and “named execution contexts” in every claim. Consider the proposed title above; remove language that implies Android-wide scope. |
| SELENE as primary dataset | **KEEP** | Exact pairs and features are present locally; narrow population to paired APKs. Reconcile live dual-license terms. |
| Primary contexts Android 10/API29 ↔ Android 14/API34 | **KEEP / MODIFY** | Treat as a bundled named context contrast. Add duration imbalance and paired-selection audit; no causal OS claim. |
| Research questions RQ1–RQ4 | **MODIFY** | Use the four streamlined RQs above; add four-state emergence to RQ1; make RQ4 external replication and boundaries. |
| Source-positive recurrence estimand | **KEEP** | Strong center of CASE. Report direction separately and use exact paired rows. |
| Target-emergent evidence | **ADD** | Add separate source-absent estimand and four-state table; label only “target-recorded emergence.” |
| 19 Boolean CASE features | **KEEP / MODIFY** | Retain for exact historical reconciliation; add fixed broad/non-derived sensitivity and disclose duplicate/threshold-derived flags. |
| Source-side evidence strength and `run_features` | **ADD** | Test raw counts, total volume and normalized counts against Boolean and persistence. Exclude triage/richness scores until provenance demonstrates independent source meaning. |
| SELENE event/lifecycle/context layers | **DEFER** | Not present in local cache and may be large/sensitive; use only after an artifact-level pilot and scope approval in revised roadmap. |
| Logistic model | **KEEP** | Direction-specific pooled L2 logistic remains simplest adequate candidate. No evidence supports bigger models. |
| Persistence/global/activity baselines | **KEEP / MODIFY** | Keep indicator persistence as key baseline; specify identical rows, fit-only rates and a distinct activity-volume-only model. |
| Calibration and operating policy | **KEEP / MODIFY** | Keep raw score primary. Thresholds must come from calibration groups; promote no formal risk-control guarantee. |
| 50% / 80% coverage points | **MODIFY** | Keep only as interpretable operating views fixed before test; include full curve and persistence comparison. Current test-ranked values remain exploratory. |
| Package grouped evaluation and bootstrap | **KEEP** | Two discovery seeds are supportive; freeze exact OOF manifest and use larger package bootstrap for future evaluation. |
| Fidelity sensitivity | **MODIFY** | Keep as provenance/parser diagnostic; only 56 shared oracle hashes, not behavior ground truth. No fidelity claim without more paired support. |
| Broken-pair negative control | **KEEP / STRENGTHEN** | Discovery control behaves as expected; freeze multiple permutations and retain target labels at APK block level. |
| Report-level proxy | **KEEP / MODIFY** | Keep claim coverage, unsupported count/report, report-any-unsupported and recurrence retention; no analyst utility claim. |
| Formal conformal/LTT guarantee | **REMOVE from core / DEFER** | No valid group/shift contract demonstrated. Mention only as future method option. |
| KronoDroid | **ADD as secondary replication** | Exact 63,316 paired SHA rows and broken-pair descriptive replication; resolve feature count, exclude labels/families, separate syscall unit. |
| AndroCT | **DEFER** | High data/method value but terms require agreement, 6.3 GB and direct behavior-difference collision. |
| DYNAMISM repeats | **DEFER / diagnostic** | Strong future stochasticity lane but data are restricted. Do not make it core. |
| CIC reboot sequence | **DEFER** | Interesting but totals conflict and exact stage pairing unverified. |
| Drift/future/family/claim OOD | **DEFER** | Current audited data do not validate corresponding identities/timestamps or independent claims. |
| Broad malware/benign and family comparisons | **MODIFY** | Use only after label semantics/family mismatch is reconciled; labels remain stratification only, never predictors. |
| PhD/federated/IoT relevance | **KEEP** | Keep as conceptual motivation only, with no simulated clients or performance claim. |
| Gates | **MODIFY** | Split into validity G0–G9 and claim-promotion G10–G24; weak effects narrow claims, structural failures block the affected lane. |
| Chapter outputs and provenance | **KEEP** | Maintain tables/figures from exact structured parents; add dataset/checksum index for external replication. |

## Final prioritized recommendation

### Tier 1 — Must add

- Add actual paired-population bias results and run-duration summaries to the primary evaluation.
- Keep recurrence and target emergence as distinct conditional estimands; include all four paired states.
- Retain persistence and global prevalence as mandatory baselines; report Brier skill, not AP alone.
- Add raw count / activity / normalized count feature ablations and a broad/non-derived indicator sensitivity.
- Freeze package-grouped confirmatory folds and calibration-only policy selection; promote no fixed-test threshold.
- Make broken-pair control and package bootstrap mandatory.
- Reconcile SELENE + ARTEMIS live license/citation requirements before data handling or public report output.

### Tier 2 — Strong additions

- Add KronoDroid as a separate secondary context-family replication with a narrowly defined syscall-presence claim and same-APK SHA pairing.
- Require external model-level replication before broad claim H or general cross-context language.
- Keep the report-level proxy, but frame it as retained/unsupported recorded claims, not analyst benefit.

### Tier 3 — Optional extensions

- AndroCT granularity–portability analysis after agreement and exact pair manifest.
- DYNAMISM same-context repeated execution if access is granted.
- CIC reboot stages if a usable identity/feature join resolves the sample discrepancy.
- Event-level SELENE granularity, chronological drift, family OOD, claim OOD and worst-context analysis after each lane’s identity/support gate passes.

### Tier 4 — Reject or defer

- New physical-device collection, device purchase, user recruitment or new APK runs.
- “First” claim, true behavior or absence claim, causal Android-version attribution, general Android portability.
- Formal finite-sample risk guarantee under unverified package dependence/shift.
- Deep sequence/MLP stack and broad nonlinear model tournament without incremental evidence.
- Analyst productivity/security impact, federated learning, or IoT evaluation claims.

## Final proposed CASE-Android scope

Build a source-only claim recurrence and scoping study with SELENE as the primary paired versioned-emulator dataset. Measure four-state recorded evidence transitions, compare simple persistence to pooled logistic using Boolean and a small source-count ladder, report proper probability quality and calibration-only risk/coverage, and aggregate one-APK report proxies. Use package-held-out splits, cluster uncertainty, broken-pair controls, paired-population/fidelity/exposure sensitivities and exact provenance. Add KronoDroid only as a separate syscall-level descriptive/external replication until a model-level replication is frozen. Treat AndroCT, DYNAMISM and CIC as optional gated datasets. Keep conclusions tied to the released finite observations and tested named contexts.
