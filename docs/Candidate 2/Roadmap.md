# CASE-Android: Reliability-Qualified Scoping of Recorded Android Security Evidence Across Execution Contexts

**Working title (chapter):** *When Can a Recorded Android Behaviour Be Carried to Another Execution Context? Recurrence Prediction, Calibrated Scoping and the Cost of Verification*

**Document role:** research protocol, written before the confirmatory experiment. It fixes populations, estimands, models, thresholds, metrics, gates and claim wording before confirmatory results are inspected.

---

## 1. Motivation

Dynamic analysis reports record what an app *did in one finite execution*: a given Android version, execution substrate, stimulation script and observation window. Security reports nevertheless tend to be read as statements about the app. When the same app is later analysed in a different context, some recorded behaviours recur and some do not. A reader, or a downstream system, must decide whether a recorded claim may be carried into a named context that has not been observed.

Two simple policies exist: carry everything (full coverage, hidden risk) or carry only what a per-claim-type base rate supports ("persistence"). Whether source-side evidence improves on those policies, how reliably an operating point chosen on calibration data delivers its stated risk, and how much verification of the target context is needed to trust it, are open, measurable questions.

## 2. Problem Statement

Given behavioural-security evidence recorded for an APK in a source context, how reliably can it be transferred to a named, unobserved target context, and how should report claims be scoped when reliability differs across claim types, malware families and directions?

The study does **not** infer full application capability, does not treat source non-observation as target absence, and does not attribute differences causally to a single context component.

## 3. Research Gap

Cross-device and emulator-versus-device behaviour differences are established. What is missing is an operational, claim-level estimate of *recurrence* for an individual recorded claim in a named target context, evaluated with proper scores against strong simple baselines, converted into a calibration-only scoping policy with explicit risk and coverage, and stress-tested by worst-group reliability, verification cost and an external context family. The contribution is measurement and operational protocol, not a new learning architecture.

## 4. Research Questions

- **RQ1 (recorded portability structure).** How often do paired source and target contexts agree, disagree or record evidence that was absent in the other context (four-state structure), per claim type and direction?
- **RQ2 (source-only signal).** Do source-context indicators and source evidence-strength fields estimate target recurrence better than direction prevalence, per-indicator persistence and family-conditioned persistence under package-held-out evaluation, and how much does a nonlinear comparator add?
- **RQ3 (scoping value and worst-group reliability).** Does a calibration-only policy deliver its stated non-recurrence risk on untouched data, how much coverage does it retain relative to persistence, and how large is the worst-indicator and worst-family risk hidden by pooled operating points?
- **RQ4 (verification cost and transfer).** How many verified target-context claims are needed to set a scoping threshold that keeps risk within tolerance, and does a recurrence model trained in the opposite direction transfer with or without recalibration?
- **RQ5 (boundaries and replication).** Do results survive unseen-family evaluation, indicator-redundancy correction, broken-pair controls and an independently paired context family (emulator versus physical device syscall evidence)?

## 5. Hypotheses

- **H1.** Recurrence is high overall but heterogeneous across claim types; target-recorded evidence among source-absent claims is common and claim-type dependent.
- **H2.** Source-side evidence beats indicator persistence in probability quality (Brier, log loss) in both directions; the gain is modest for logistic models and larger for a nonlinear comparator.
- **H3.** Calibration-only thresholds achieve realised risk within 1 percentage point of target on average, at a coverage above persistence at equal risk.
- **H4.** A pooled threshold hides materially higher risk for some indicators and families; per-indicator thresholds reduce that at a coverage cost.
- **H5.** A model transferred from the opposite direction does not beat in-direction persistence even after recalibration; roughly a thousand verified target claims are needed for a reliable pooled threshold.
- **H6.** The main qualitative findings replicate on an independent context family with a different claim ontology.

## 6. Expected Contributions

1. A claim-level recurrence estimand and four-state descriptive protocol for recorded dynamic evidence.
2. A probability-quality comparison against strong simple baselines (including family-conditioned persistence) with paired package-cluster and family-cluster inference.
3. A calibration-only scoping policy evaluation with risk, coverage, worst-indicator, worst-family and report-level metrics.
4. A verification-cost curve: risk violation versus number of verified target claims.
5. A negative result on cross-direction model transfer and a bounded external replication.

## 7. Relation to the Doctoral Programme

The doctoral topic is collaborative malware detection with federated learning over heterogeneous IoT networks. This chapter is **not** a federated-learning experiment and does not use IoT clients. Its link is the reliability question that federated systems face one level up: local evidence produced in heterogeneous contexts, decisions that should not silently assume transfer, calibrated and client-specific operating points, worst-group performance under pooled thresholds, and the trade-off between pooling and per-group scope. These are measured here directly on recorded Android evidence. Contexts, indicators and packages are never called FL clients.

## 8. Threat Model and Assumptions

- Analysts have a source-context report and must decide, before observing the target context, which claims to carry across.
- Reports are outputs of automated pipelines; they contain finite observations. Absence of a record is not absence of behaviour.
- No adversary is modelled. Evasion by malware that detects analysis environments is a limitation.
- Family labels in SELENE are AV-derived metadata available before the target run; a deployment that lacks such labels must use the models that exclude them.

## 9. Datasets and Dataset Roles

| Role | Dataset | Content used |
|---|---|---|
| Primary | SELENE / ARTEMIS compact Parquet (Android 10 / API 29 and Android 14 / API 34) | `run_features`, `analyses`, `fidelity_oracle` |
| External replication | KronoDroid (emulator and real-device archives, four public zip files) | 288 syscall-count columns, static permission columns, `Package`, `sha256` |

SELENE: Hugging Face `serrooT/selene-android-paper-artifacts`; both the SELENE artifact licence and the upstream ARTEMIS licence and citation requirements apply and must be verified in the live data card before release of any derived table. KronoDroid: public GitHub repository archives; cite the original dataset paper.

Raw data are immutable, kept outside the repository and never printed. Raw sensitive strings from traces are never echoed.

## 10. Context and Claim Construction

**Contexts.** SELENE: Android 10 (strace observer, Monkey input) and Android 14 (same observer and input). KronoDroid: emulator and physical device. A context is the bundle of platform, substrate and run settings; differences are never attributed to one component.

**Claim.** For a source-positive cell (APK a, claim type j) in direction s→t, the outcome is whether the same claim type is recorded in the target context.

- SELENE claim types: the 19 released Boolean indicators. Two pairs are exact duplicates (`has_NETWORK_EXTERNAL` = `has_external_tcp`, `has_PROCESS_MEMORY_READ` = `has_process_vm_readv`); both members are retained in the primary analysis and one member of each is dropped in the redundancy sensitivity.
- KronoDroid claim types: syscall present (count > 0), 288 syscalls; different ontology, reported separately.

**Four states.** n00, n01 (target-recorded), n10 (source-only), n11 for every claim type and direction.

## 11. Identity and Grouping

- APK identity: exact SHA-256; pair only APKs present in both contexts with a unique row per context (SELENE: 30,746 pairs; KronoDroid: unique-SHA rows in both archives, 63,316 pairs; duplicated SHA rows are excluded).
- **Outer grouping:** package name (SELENE 22,475 packages in the paired set; KronoDroid 47,709). All APKs of a package share a fold.
- **Family grouping** (unseen-family evaluation, SELENE): the released `family` field is identical in both contexts for every paired APK; folds are formed by family hash.
- Package name, SHA-256, run id, family and fold id are never predictors, except the explicitly named family-conditioned models.
- The paired population is the inferential population. Unpaired Android-10 runs are used only for a selection audit.

## 12. Preprocessing

- Predictors come from the **source context only**. Target columns, target metadata and outcomes never enter features. An automatic test permutes target rows and requires identical predictor matrices.
- Log1p transforms of counts and volume fields, standardisation fitted inside the training partition.
- Excluded from predictors: derived triage/richness scores, first/last event times (trace-clock values, not dates), time-to-first fields with >50% missingness, identifiers, and all target-context fields.
- KronoDroid: static permission columns are identical across contexts and are permitted as source-side APK metadata in one variant. AV labels, detection ratio, scanner counts and dates are never predictors. Date columns are APK metadata with a 1980 sentinel and are not execution times.

## 13. Train / Calibration / Validation / Test Protocol

Outer 5-fold split by group hash (salt-dependent). Inside each training partition, 20% of groups form a calibration partition; the remainder is the fit partition. Models and priors are fit on the fit partition; thresholds are chosen on the calibration partition; the outer test fold is used once. Five confirmatory salts (100–104). Directions are modelled separately.

## 14. Experimental Scenarios

1. **Package-held-out prediction** (both directions).
2. **Family-held-out prediction** (SELENE; families in different folds).
3. **Calibration-only scoping** at risk targets 1%, 2% and 5% (KronoDroid: 10% and 20%).
4. **Verification-cost experiment:** threshold chosen from k random verified claims of the calibration partition, k ∈ {30, 100, 300, 1000, 3000, 10000, all}, 30 draws per fold.
5. **Cross-direction transfer:** model fitted in the opposite direction on the same package folds, applied raw and after one-dimensional recalibration with k verified claims, k ∈ {10, …, 10000}.
6. **External replication:** KronoDroid, both directions, same protocol.

## 15. Baselines

| Baseline | Definition |
|---|---|
| Always generalise | carry every source-positive claim (full-coverage risk) |
| Direction prevalence | fit-partition recurrence rate |
| Indicator persistence | smoothed recurrence rate per claim type (principal simple baseline) |
| Family × indicator persistence | recurrence rate per (family, claim type), shrunk to the indicator rate with m = 10; unavailable families fall back to indicator persistence |
| Activity-volume model | claim identity + volume fields |
| Boolean logistic | claim identity + source indicators, L2, C = 1 |
| Count logistic | claim identity + log evidence counts |

## 16. Proposed Method / Analysis

**Primary scorer:** direction-specific pooled L2 logistic (C = 1, standardised inputs) on claim identity, source Boolean vector, log source evidence counts and log activity/volume fields ("rich"). **Comparators fixed in advance:** Boolean logistic, rich logistic with family one-hot ("rich + family"), and a gradient-boosted tree ensemble (150 iterations, learning rate 0.1) on the rich features as a nonlinear ceiling. No other models are added.

**Scoping policy.** Keep a claim if its score is at least a threshold t. Thresholds: (a) *pooled*: largest coverage whose calibration risk is at most r*; (b) *per-indicator*: the same rule per claim type when the calibration partition holds at least 400 claims of that type (else pooled); (c) *UCB pooled*: as (a) with a one-sided 95% Clopper–Pearson upper bound ≤ r*. Minimum 200 kept calibration claims; otherwise `NO_OPERATING_POINT`. Targets are never relaxed after seeing test results.

## 17. Oracle / Upper Bounds

- Retrospective risk at fixed coverage (scores ranked on the test fold): an upper bound on any threshold rule, labelled non-deployable.
- In-direction model as the ceiling for cross-direction transfer.
- Full-calibration threshold as the ceiling for the verification-cost curve.

## 18. Primary Metrics

- **Probability quality:** Brier score and Brier skill score versus indicator persistence (BSS = 1 − Brier_model / Brier_persistence), with log loss (probabilities clipped to [1e−6, 1−1e−6]).
- **Scoping:** realised non-recurrence risk among kept claims and claim coverage at each target r*; coverage at matched realised risk.

## 19. Secondary Metrics

- Recurrence retention (fraction of recurring claims kept).
- Calibration slope and intercept on the out-of-fold predictions; expected calibration error with fixed 10 equal-mass bins.
- Average risk-coverage area over coverage 0.05–1.0.
- Report level: for each APK with at least one source-positive claim, unsupported kept claims per report and share of reports with at least one unsupported kept claim.
- Four-state counts, target-recorded evidence rate among source-absent claims.
- Verification cost: mean realised risk, fraction of draws exceeding r* + 2 points, fraction without an operating point, versus k.
- Transfer: BSS of raw and recalibrated opposite-direction model versus in-direction persistence.

## 20. Worst-Group Metrics

- Worst-indicator realised risk (claim types with ≥ 100 kept test claims) and indicator risk dispersion (SD across qualified indicators).
- Worst-family realised risk (families with ≥ 200 kept test claims) and family dispersion.
- Worst-fold risk (maximum over outer folds).

## 21. Statistical Analysis

- Paired comparison on identical test claims. Inference by **package-cluster bootstrap** (10,000 multinomial cluster draws) for package-grouped evaluation and **family-cluster bootstrap** for family-grouped evaluation; intervals are 95% percentile intervals of Brier and log-loss differences.
- Salt repetition (five salts) reports the spread of the point estimates; intervals are computed on the pooled out-of-fold predictions of each salt and reported per salt.
- Effect sizes are absolute Brier differences and BSS.
- Primary contrasts (Holm-adjusted within direction): rich logistic − indicator persistence; rich logistic − family × indicator persistence; gradient-boosted comparator − indicator persistence. Others are exploratory.
- Risk targets: realised risk versus target reported with fold-level spread; no significance test is applied to risk targets.

## 22. Ablations

- Feature ladder: Boolean, count-only, volume-only, rich, rich + family, nonlinear.
- Duration-normalised count features versus raw counts.
- Removal of the two exact-duplicate indicator pairs.
- Class-level indicator subset: the 12 upper-case event-class indicators (NETWORK_EXTERNAL, NETWORK_LOCAL, BINDER_IPC, TLS_CERT_ACTIVITY, APP_PRIVATE_FILE_ACTIVITY, PROC_ACCESS, MEMORY_EXEC, ENV_CHECK, PROCESS_ACTIVITY, PROCESS_MEMORY_READ, WAIT_ACTIVITY, ERROR_PROBING); the seven specific or threshold-derived flags are excluded. The subset is fixed by naming class, not by recurrence.

## 23. Sensitivity Analyses

- Risk targets 1/2/5%; pooled versus per-indicator versus UCB thresholds.
- Calibration partition fraction (10%, 20%, 30%).
- Outer fold count (5 versus 10).
- Paired versus unpaired Android-10 prevalence (selection audit).
- Runs without any recorded event (no source-positive claims) versus others.

## 24. Negative Controls

- **Broken-pair control:** permute target rows across APKs within each test fold; every model must lose to persistence.
- **Target-independence test:** predictors are unchanged when target rows are shuffled.
- Group-leak assertions for fit, calibration and test partitions by package and by family.
- Package-fold agreement across directions (needed for cross-direction transfer).

## 25. Robustness Checks

- Alternative salts and fold assignments.
- Row-order and tie-handling invariance of the threshold rule (ties are kept whole).
- Removal of claim types with fewer than 300 positive claims.
- Excluding the two largest packages by APK count.

## 26. External Replication

KronoDroid emulator ↔ device with syscall-presence claims: package-grouped five-fold protocol; pooled L2 logistic (Boolean, rich, rich + static metadata) and gradient-boosted comparator versus per-syscall persistence; broken-pair control; per-syscall worst-group risk; malware and benign strata. A syscall-support filter of at least 100 claims per claim type is applied for macro summaries. Model fitting subsamples up to 400,000 fit claims. Replication asks whether qualitative conclusions (sign of the gain over persistence, loss under broken pairing, hidden worst-group risk) hold; it is not pooled with SELENE.

## 27. Claims and Claim Promotion Gates

| Claim | Gate |
|---|---|
| C1. Recorded portability is heterogeneous across claim types and directions | four-state table with per-indicator recurrence spread ≥ 0.10 |
| C2. Source-only evidence beats indicator persistence | Brier gain interval excludes 0 in both directions and all salts; broken-pair control loses |
| C3. It also beats family-conditioned persistence | same, in each direction; otherwise the claim is restricted to the direction(s) that pass |
| C4. Nonlinear comparator adds beyond logistic | gradient-boosted gain interval above rich logistic in both directions |
| C5. Calibration-only policy attains its target | mean realised risk within r* ± 0.01 and worst-fold risk ≤ r* + 0.02 |
| C6. Scoping retains more coverage than persistence at equal risk | coverage difference > 0 with fold-consistent sign in both directions |
| C7. Pooled thresholds hide worst-group risk | worst-indicator (or worst-family) risk exceeds pooled risk by ≥ 0.05 |
| C8. About one thousand verified target claims are needed | violation rate ≤ 5% at k = 1000 and > 10% at k = 100 |
| C9. Opposite-direction models do not transfer | raw and all recalibrated BSS ≤ 0 versus in-direction persistence |
| C10. Findings replicate on KronoDroid | same sign of C2 and C7 in both directions |
| C11. Signal survives unseen families | family-cluster Brier-gain interval excludes 0 in each direction (rich logistic and nonlinear comparator judged separately) |

Structural failures (target-independence test fails, group leakage, identity mismatch) block the affected experiment. Weak or mixed effects narrow the claim and never lead to changed metrics or thresholds. Allowed wording: "recorded evidence", "in the tested contexts", "recurrence of recorded claims". Forbidden wording: behaviour "emerged", causal attribution to Android version or emulator, "ground truth", "guarantee", analyst time savings, generality across Android, first/novel/state of the art.

## 28. Reproducibility

- Scripts take explicit salts; outputs are JSON in `out/`. `python c2_selene.py check` runs the automatic identity/leakage assertions; `audit_selene.py` and `audit_krono.py` re-derive every dataset fact; `fetch_krono.sh` downloads and hashes the four archives.
- Paths through `CASE_RAW`, `CASE_CACHE`. SHA-256 of all inputs is recorded in the audit output.
- `run_selene.sh` and `python c2_krono.py` regenerate all tables.

## 29. Compute Plan

CPU only. SELENE probability quality with the nonlinear comparator: about ten minutes per salt on ten cores; scoping about fifteen minutes; transfer about ten minutes; KronoDroid about thirty minutes. Memory below 12 GB. No hardware or new data collection.

## 30. Expected Figures

1. Four-state stacked bars per indicator and direction.
2. Brier skill by model and direction with bootstrap intervals.
3. Risk–coverage curves (retrospective) and calibration-only operating points.
4. Worst-indicator and worst-family risk under pooled versus per-indicator thresholds.
5. Verification-cost curve (risk and violation rate against k).
6. Cross-direction transfer versus k.
7. KronoDroid replication panel.

## 31. Expected Tables

1. Dataset, pairing and support summary.
2. Probability-quality table (all models, both directions, both groupings).
3. Scoping table at each target risk (risk, coverage, retention, worst-group, report-level).
4. Verification-cost table.
5. Transfer table.
6. Claim/gate outcomes.

## 32. Limitations

- Two named context pairs; contexts bundle platform, substrate and duration; no causal attribution.
- Recorded observations are finite (Monkey-driven, minutes); non-recurrence may reflect exposure, not behaviour.
- Indicators are correlated and partly derived; effective number of independent claims is smaller than 19.
- Paired sample is selected (paired versus unpaired prevalence differs); conclusions apply to the paired population.
- Fidelity oracle overlaps only 56 paired APKs; it cannot serve as behaviour ground truth.
- Same-context stochastic variation cannot be measured (no repeated runs).
- No analyst study; report-level metrics are offline proxies.

## 33. Threats to Validity

- **Construct:** recurrence of a recorded claim is not behavioural equivalence.
- **Internal:** package reuse and family structure; mitigated by grouped folds and family-held-out evaluation. Threshold selection on calibration data of finite size; addressed by UCB variant and verification-cost curve.
- **Statistical:** claims within an APK are dependent; inference is clustered.
- **External:** one primary dataset from one pipeline; a second dataset with a different ontology.

## 34. Ethical and Security Considerations

Public data only. Trace contents may hold malware-controlled endpoints and credential-shaped strings; they are not reproduced. No executable artefact is redistributed. The scoping policy is a reporting aid and must not be presented as a detection guarantee.

## 35. Chapter Structure

1. Motivation: evidence recorded in one context.
2. Related work: cross-device behaviour, dynamic analysis reliability, selective prediction.
3. Estimand, data, pairing and four-state structure.
4. Recurrence prediction against strong baselines.
5. Calibrated scoping and worst-group reliability.
6. Verification cost and transfer.
7. External replication and boundaries.
8. Discussion and relation to collaborative, heterogeneous-context detection.

## 36. Execution Order

1. Verify licences and hashes; run identity and leakage assertions.
2. Four-state and selection audits.
3. Probability quality (package and family grouping) with controls.
4. Scoping, verification-cost and transfer experiments.
5. KronoDroid replication.
6. Gate evaluation and write-up.

## 37. Completion Criteria

- Assertions pass for all salts and both datasets.
- Every gate has a recorded outcome; every claim in the chapter is mapped to a gate or labelled exploratory.
- Tables and figures regenerate from the scripts with fixed salts.
