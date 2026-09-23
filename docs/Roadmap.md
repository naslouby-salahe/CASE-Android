# CASE-Android Research Roadmap

**Project:** CASE-Android  
**Acronym:** Context-Aware Scoping of Evidence in Android  
**Full title:** *Context-Aware Scoping of Recorded Android Behavioral-Security Evidence Across OS Versions*  
**Role:** Authoritative scientific roadmap for the CASE-Android project  
**Companion document:** [`technical_doc.md`](technical_doc.md) defines implementation and engineering contracts.

---

## 1. Research statement

Dynamic Android analysis reports describe behavior that was **observed in a particular execution context**. The same APK may produce a different recorded report in another context because the Android version, emulator/runtime, interaction path, observation window, instrumentation, and execution stochasticity can all affect what is seen.

CASE-Android studies a narrow operational question:

> **Given a behavioral-security indicator observed for an APK in one recorded Android context, how strongly should that evidence be carried into a named target context that has not yet been observed?**

The project does **not** try to prove that a behavior is truly present or absent in the APK. It predicts **recorded cross-context recurrence** and uses that estimate to scope the wording of a security report.

The intended contribution is a lightweight, claim-level reporting layer:

```text
recorded source-context evidence
          ↓
source-positive claim
          ↓
source-only context features
          ↓
cross-context recurrence score
          ↓
calibration / operating-point view
          ↓
report scope
 ┌───────────────────────────────┐
 │ cross-context-supported       │
 │ source-context-only           │
 └───────────────────────────────┘

(optional uncertainty/abstention sensitivity only if it proves useful)
```

This is deliberately a **decision/reporting contribution**, not a new malware classifier and not a new deep-learning architecture.

### Research-development principle

CASE-Android is the result of a long discovery, dataset-audit, feasibility, and collision-screening process. That work was done precisely to arrive at a research direction that is both **scientifically defensible and practically feasible**. The roadmap therefore uses gates as evidence-quality controls, not as arbitrary reasons to discard the project.

When new evidence exposes a weaker effect, an asymmetric result, a dataset limitation, or a narrower construct than expected, the default response is:

```text
audit the issue
→ preserve methodological validity
→ adapt the mechanism if scientifically justified
→ narrow or reformulate the claim
→ continue with the strongest defensible version
```

The project should stop or fundamentally re-scope only for a **structural validity failure** such as unrecoverable leakage, an invalid estimand, unusable provenance/licensing, or a direct capability collision that removes the contribution itself. A modest result is not automatically a failed project; it usually means a more modest claim.

---

## 2. Why this is worth studying

The core failure mode is simple: a dynamic-analysis report can sound global even though its evidence was recorded under one finite execution condition. Prior Android work already shows that dynamic behavior can vary across devices and environments, and SELENE itself documents Android-version effects. CASE-Android therefore does **not** claim to discover context dependence.

The residual problem is what to do with that dependence at the level of an individual report claim.

A conservative intersection rule avoids over-generalization but can discard large amounts of observed evidence. An always-report rule preserves coverage but silently treats context-specific observations as portable. CASE-Android tests whether a simple source-only recurrence score can give a better **coverage-versus-non-recurrence** trade-off than those naive assumptions.

The novelty target is therefore modest and practical:

> **Explicit, claim-level, context-scoped reporting of recorded Android behavioral-security evidence, evaluated as a selective evidence-transfer decision.**

It is not a claim of unprecedented novelty. The project only needs to show that this reporting capability is distinct enough, useful enough, and empirically defensible enough for a technically meaningful chapter.

---

## 3. Relationship to the PhD

The PhD studies **collaborative malware detection using federated learning across heterogeneous IoT devices**.

CASE-Android does not perform federated learning and does not use IoT clients. Its connection is the shared scientific principle:

```text
heterogeneous participants / environments
                ↓
different local evidence distributions and reliability
                ↓
shared or global assumptions may not transfer equally
                ↓
security decisions should preserve contextual reliability
```

In the PhD, heterogeneous IoT participants may contribute differently distributed and differently reliable evidence to a collaborative detector. CASE-Android studies the same reliability problem one level lower: whether an individual behavioral-security assertion observed in one execution context should be generalized to another.

The chapter may motivate future work in which federated or collaborative systems exchange reliability-qualified evidence or calibration summaries. That is **future motivation only**. APKs, packages, Android versions, indicators, and split groups are never called FL clients.

---

## 4. Scientific scope and non-goals

### In scope

- Recorded SELENE behavioral/security indicators.
- Android 10 / API 29 and Android 14 / API 34 execution-context pairs.
- Source-positive claim recurrence in the paired target context.
- Source-only recurrence scoring.
- Selective reporting and evidence scoping.
- Coverage-versus-non-recurrence trade-offs.
- Direction-specific and indicator-specific heterogeneity.
- Calibration and uncertainty of recurrence estimates.
- Reproducible offline analysis of released artifacts.

### Explicitly out of scope

- Malware classification or family attribution.
- Proving that an APK can or cannot perform a behavior.
- Treating a non-observation as proof of absence.
- Causal attribution to Android OS version alone.
- Universal Android-version portability.
- Real-world analyst productivity or security benefit unless separately measured.
- APK execution, emulator campaigns, fresh captures, or physical devices.
- Federated-learning or IoT performance claims.
- Deep learning merely to increase model complexity.

---

## 5. Current evidence base

The authoritative discovery evidence comes from the latest R5 audit in the FedIEC research project.

### 5.1 SELENE audit anchors

- Android 10/API29 selected runs: **44,485**.
- Android 14/API34 selected runs: **30,751**.
- Exact paired APK SHA-256 identities: **30,746**.
- Package groups in the audited population: **22,475**.
- Android-10-only identities: **13,739**.
- Android-14-only identities: **5**.
- Shared processed Boolean indicators used by the R5 probes: **19**.
- Current project-local compact inputs: **29,777,711 bytes** across the eight audited files.
- The fidelity oracle contains 1,000 rows per context but only **56 shared APK hashes** across the two oracle subsets.

The official SELENE dataset card confirms that `android10` and `android14` are **execution-environment splits, not train/test splits**, and that the artifacts are finite Monkey-driven emulator observations. Absence of an event is not proof that the APK cannot perform it.

### 5.2 Existing exploratory signal

The latest audited exploratory probe uses source-positive `(APK, indicator)` claims, package-grouped train/test splits, source-context flags only, and the target label “same processed flag appears in the paired target context.”

For the all-19-indicator pooled model:

| Direction | Exploratory recurrence | Pooled AP | Persistence AP | Pooled Brier | Persistence Brier | Pooled top-50 precision | Persistence top-50 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Android 10 → 14 | ~0.898–0.900 | ~0.9865 | ~0.9778 | ~0.066–0.067 | ~0.072 | ~0.9965–0.9967 | ~0.9859–0.9863 |
| Android 14 → 10 | ~0.852–0.857 | ~0.952–0.957 | ~0.944–0.950 | ~0.097–0.102 | ~0.099–0.104 | ~0.961–0.968 | ~0.953–0.959 |

These results are **exploratory only**. The three historical `GroupShuffleSplit` runs overlap and are not independent replications. The earlier “non-saturated” slice used target-test prevalence to select indicators and is therefore post-hoc; it cannot become the confirmatory headline.

### 5.3 Fidelity warning

Several compact flags do not agree perfectly with raw-evidence paths in the SELENE fidelity material. For example, audited TLS activity agreement was approximately 0.545 in Android 10 and 0.659 in Android 14. The fidelity material checks parser/provenance behavior from the same underlying traces; it is not independent ground truth for cross-context security truth.

Therefore the estimand throughout CASE-Android is **processed-flag recurrence**, not behavior truth.

---

## 6. Operational scenario and estimand

CASE-Android only has operational value if it makes a decision **before the target context is observed**.

For a source context `s`, target context `t`, APK `a`, and indicator `j`:

- `x[a,j,s] = 1` means the indicator was recorded in the source report.
- A CASE claim exists only when `x[a,j,s] = 1`.
- The target outcome is `y[a,j,s→t] = x[a,j,t]`.
- CASE estimates:

\[
\hat p_{a,j}^{s\rightarrow t}
= P\left(y_{a,j}^{s\rightarrow t}=1\mid X_a^s, j\right),
\]

where `X_a^s` contains **source-context information only**.

The primary decision unit is therefore:

> **one source-positive APK × indicator claim in one declared direction.**

The primary estimand is the expected recurrence quality and selective-reporting risk for such claims in the audited paired population.

### Consequence

A rule that inspects the target report before deciding whether the claim is portable is **not a deployable CASE baseline**. In particular, strict source/target intersection is useful as a retrospective descriptive reference, but it is not a fair prospective predictor.

---

## 7. Research questions

### RQ1 — Cross-context recurrence

**How often, and for which indicators, do source-positive recorded behavioral-security claims recur in the paired target context?**

This establishes the problem structure without attributing differences causally to the OS version.

### RQ2 — Source-only recurrence estimation

**Can source-context information estimate claim recurrence better than a training-only per-indicator persistence baseline?**

The primary comparison is probabilistic quality, not malware-detection accuracy.

### RQ3 — Evidence-scoping utility

**Does CASE improve the selective reporting frontier: lower target non-recurrence among claims labeled cross-context-supported while preserving useful claim coverage?**

This is the main operational question.

### RQ4 — Heterogeneity and robustness

**How stable are the recurrence patterns and CASE benefit across direction, indicator, package weighting, and broad-versus-derived indicator definitions?**

This determines whether the result is a broad reporting effect or a small artifact of a few common indicators.

### 7.1 RQ-to-evidence map

| RQ | Population / unit | Main comparison | Primary evidence | Permitted interpretation |
|---|---|---|---|---|
| RQ1 | paired source-positive claims | descriptive | recurrence by direction/indicator; paired-population audit | recorded recurrence varies across the tested contexts |
| RQ2 | held-out package-grouped claims | CASE score vs persistence | Brier, log loss, paired cluster-bootstrap deltas | source-only context carries predictive information about recorded recurrence |
| RQ3 | same held-out claims | CASE selective policy vs persistence ranking / always-report | generalized risk-coverage, risk at coverage, coverage at risk budget, recurrence retention | CASE changes the evidence-scoping trade-off |
| RQ4 | direction and indicator strata | macro/worst-stratum and sensitivity analyses | per-indicator metrics, package-macro metrics, broad-indicator sensitivity | benefit/limitations are heterogeneous or robust within this artifact |

---

## 8. Dataset and provenance contract

### 8.1 Source

Primary dataset: **SELENE Android Paper Artifacts**, derived from ARTEMIS dynamic Android analyses.

Shared raw-data root:

```text
/home/naslouby/Projects/datp-shared-data/raw
```

Expected CASE source directory:

```text
/home/naslouby/Projects/datp-shared-data/raw/SELENE
```

Raw/external data are immutable and never committed into CASE-Android.

### 8.2 Required source families

The initial study requires only the compact released files needed for:

- `analyses` metadata;
- `run_features` in Android 10 and Android 14;
- `fidelity_oracle` and `fidelity_evidence` for provenance/fidelity auditing.

Event-level multi-gigabyte tables are not needed for the primary experiment.

### 8.3 Identity and join rules

- APK identity: exact SHA-256.
- Run identity: released SELENE run identifier.
- Grouping identity for train/calibration/test separation: `package_name`.
- Paired context record: exact APK SHA-256 present in both environments.
- Claims are constructed only after the pair has been validated one-to-one.
- Package/hash/run identifiers are grouping/provenance variables, **never predictive features**.

### 8.4 License and citation

The SELENE artifact is released under the SELENE Paper Artifacts Data License 1.0 and remains subject to the upstream ARTEMIS Dynamic Traces Data License 1.0. Public outputs must follow the citation requirements of both releases. CASE-Android’s MIT license applies only to original CASE-Android code and repository material.

### 8.5 Sensitive released content

The upstream artifact card warns that recorded malware-controlled endpoints, identifiers, paths, and credential-shaped strings may be present in some artifact families. CASE-Android uses compact Boolean features for the primary study and must not echo raw sensitive strings into logs, tables, figures, or public outputs.

---

## 9. Population and selection-bias audit

The paired population is not automatically representative of all SELENE runs. Android 10 has 13,739 unpaired identities while Android 14 has only five unpaired identities. This asymmetry can induce selection bias.

Before any confirmatory modeling, run `audit-paired-population`:

- compare Android-10 paired vs Android-10-only flag prevalences;
- compare number of positive flags per APK;
- compare package-group composition where possible;
- report absolute prevalence differences for every flag;
- report the largest absolute prevalence difference and macro mean difference;
- do not infer why an APK is unpaired unless the source metadata supports that explanation.

This audit does not “correct” the paired population. It defines the population to which the confirmatory claims apply and quantifies how selective that population may be.

---

## 10. CASE-Android mechanism

### 10.1 Information allowed at decision time

For a source-positive claim, the primary CASE scorer may use only:

- the 19 source-context Boolean indicators;
- one-hot identity of the claim indicator;
- the declared source→target direction, by fitting a separate model per direction.

It may not use:

- any target-context flag;
- target-context summaries;
- target run metadata produced after target execution;
- package name, APK hash, run ID, family label, malware label, or timing identifiers;
- fidelity-oracle outcomes as a prediction label.

### 10.2 Primary recurrence scorer

The primary scorer is intentionally simple:

> **direction-specific pooled L2-regularized logistic regression** with indicator identity and the source Boolean feature vector.

Default scientific model contract:

```text
penalty = L2
C = 1.0
max_iter = 1000
class_weight = None
```

These values were already used in exploration and are frozen before confirmatory execution; there is no hyperparameter search on confirmatory outcomes.

A separate per-indicator logistic model is retained as a **secondary complexity comparator**, not the definition of CASE.

### 10.3 Report-scope policy

The primary CASE output is a **continuous recurrence score** for each source-positive claim. The score is the scientific object; any categorical reporting rule is a readable operating view derived from that score.

The default two-scope interpretation is:

- **`cross-context-supported`** — the score is high enough, under a threshold chosen without using test outcomes, to justify carrying the recorded claim into the named target context.
- **`source-context-only`** — keep the claim tied to the source context rather than generalizing it. This does **not** mean the behavior is absent in the target context.

CASE does **not** require a third `insufficiently-tested` outcome. If an indicator is genuinely too sparse for a reliable stratum-specific estimate, that limitation is reported through its sample/package count, uncertainty interval, and `NA` metric rules rather than converted into an artificial scientific class.

An optional abstention/uncertainty region may be evaluated later as a **secondary sensitivity analysis** if the score calibration shows that it adds useful information. It is not part of the core contribution and is not required for the chapter.

### 10.4 Operating points are descriptive, not project gates

The primary evidence is the complete probability-quality and risk-coverage analysis. Fixed operating points are used to make the trade-off easy to interpret, not to decide whether CASE-Android “passes” or “fails.”

The roadmap keeps the exploratory **50% and 80% coverage** views because they are already interpretable from the existing PoC. It may additionally show one or more recurrence-risk targets such as 5% or 10% when the calibration data support them.

For each outer fold, any reporting threshold must be chosen from training/calibration data only. If a requested risk target is not achievable at useful coverage, report that fact and the achievable frontier. Do **not** lower the target after inspecting the test set, but also do **not** treat an unavailable operating point as project failure.

### 10.5 Adaptive evidence rule

The mechanism, metrics, and claims must stay aligned with what the data actually support:

- if CASE clearly improves probability quality and selective reporting, claim the improvement;
- if the gain is small but consistent, claim a modest practical improvement;
- if the gain is directional, make the contribution direction-dependent;
- if simple persistence is competitive at broad coverage, say so and identify where CASE adds value;
- if an indicator is too sparse or unstable, report it as a limitation rather than inventing a new class;
- if a methodological issue is discovered, repair the protocol and regenerate the affected evidence with a new protocol identity.

This flexibility is **not** permission to move thresholds post hoc to manufacture positive results. The adaptation is in the *claim and scope*, not in selectively rewriting the evidence.

---

## 11. Baselines and references

### 11.1 Prospective baselines

**Always-generalize**  
Every source-positive claim is treated as cross-context-supported. This defines full-coverage recurrence risk.

**Per-indicator persistence**  
For each indicator, predict the training-set recurrence rate for every source-positive claim of that indicator. This is the principal simple baseline.

**Activity-volume baseline**  
Use indicator identity plus only the source report’s total positive-flag count. This tests whether CASE merely exploits “busy apps have more recurring flags.”

**CASE pooled logistic**  
Indicator identity plus the complete source Boolean flag vector. This is the primary method.

**Per-indicator logistic**  
One simple logistic model per indicator using source flags. This is a secondary comparator to test whether indicator-specific weights are materially necessary.

### 11.2 Retrospective descriptive reference

**Strict intersection** requires observing both source and target reports. It is therefore not a prospective baseline for CASE. It may be reported only as a descriptive “what would remain if both reports were already available?” reference.

It must never be presented as a deployable competitor in the main predictive comparison.

---

## 12. Confirmatory split protocol

The previous three random grouped splits are exploratory and are not reused as confirmatory evidence.

### 12.1 Outer evaluation

Use **five non-overlapping package-grouped outer folds**. Build the fold manifest once from the paired-APK table (one row per paired APK, grouped by `package_name`) with `GroupKFold(n_splits=5)`, without using target recurrence labels. Reuse the same package-to-fold assignment for both directions. Each package appears in the test partition of exactly one outer fold.

A persisted `split_manifest` must record for every APK/package:

- package group;
- APK hash;
- outer fold;
- direction eligibility;
- train/calibration/test role for each fold.

### 12.2 Inner calibration

Within each outer-training partition, reserve **20% of the outer-training package groups** as a deterministic calibration subset using one fixed calibration seed plus the outer-fold identity. Models fit only the remaining training groups. Calibration groups are used for:

- CASE risk-budget threshold selection;
- probability-calibration diagnostics;
- support gating.

The primary confirmatory protocol does **not** add Platt scaling, isotonic regression, temperature scaling, or another post-hoc probability calibrator. The logistic probabilities are evaluated as produced; the separate calibration partition exists to set the reporting policy and assess support without touching the outer test set.

Outer-test outcomes are never used for method selection, threshold selection, indicator eligibility, or calibration.

### 12.3 Out-of-fold evidence

After all five outer folds:

- every eligible package has exactly one out-of-fold test prediction;
- concatenate out-of-fold predictions for overall evaluation;
- retain fold identity for diagnostics;
- do not treat the five folds as five independent studies.

### 12.4 No target-derived feature selection

The primary analysis includes all 19 audited indicators.

Any “broad-only” sensitivity subset must be defined **from source schema semantics before confirmatory outcomes are inspected**. The historical `<98% target recurrence` rule is forbidden because it used test outcomes to define eligibility.

---

## 13. Metrics

High recurrence makes some standard ranking metrics look impressive even for weak models. CASE therefore uses metrics tied directly to probability quality and selective reporting.

### 13.1 Descriptive recurrence

For each direction and indicator report:

- source-positive claim count;
- package count;
- target recurrence rate;
- 95% package-cluster bootstrap interval;
- macro mean, median, IQR, minimum, and maximum recurrence across indicators.

### 13.2 Primary probabilistic metrics

**Brier score**  
Primary proper scoring rule for recurrence probability quality.

\[
BS = \frac{1}{N}\sum_i (\hat p_i-y_i)^2.
\]

Report the paired difference `CASE − persistence`; negative is better.

**Log loss**  
Secondary proper scoring rule that penalizes overconfident errors.

These are preferred over ECE as primary metrics because Brier and log loss are proper scoring rules. Binned ECE may be reported only as a descriptive calibration diagnostic.

### 13.3 Calibration diagnostics

Report:

- calibration intercept;
- calibration slope;
- reliability plot with predeclared bins;
- descriptive ECE with the exact binning rule stated;
- Brier by direction and indicator.

Do not claim “calibrated” merely because ECE is small.

### 13.4 Ranking metrics

Average precision remains a secondary metric because recurrence prevalence is high and AP is prevalence-sensitive. Always report recurrence prevalence next to AP.

Optionally report AP lift over the per-indicator persistence baseline; do not headline raw AP alone.

### 13.5 Selective-reporting metrics

For threshold `τ`:

**Supported coverage**

\[
C(\tau)=\frac{\#\{i:\hat p_i\ge\tau\}}{N}.
\]

**Supported non-recurrence risk**

\[
R(\tau)=\frac{\sum_i \mathbf 1[\hat p_i\ge\tau](1-y_i)}{\sum_i \mathbf 1[\hat p_i\ge\tau]}.
\]

This is the main operational error quantity. It must not be renamed malware false-positive rate.

**Recurrence retention**

\[
U(\tau)=\frac{\sum_i \mathbf 1[\hat p_i\ge\tau]y_i}{\sum_i y_i}.
\]

This measures how much genuinely recurrent recorded evidence is retained.

**Risk-coverage curve**  
Plot `R(τ)` against `C(τ)` over all score thresholds.

**AUGRC / generalized risk-coverage summary**  
Use the generalized risk-coverage area as the primary threshold-independent selective-reporting summary, treating target non-recurrence as the selective error event. Follow the modern selective-classification evaluation literature and report the exact implementation contract and orientation; lower is better. Because this metric is newer than ordinary AURC, validate it against both a hand-computable fixture and an independent formula/reference implementation before confirmatory use.

For continuity with the exploratory work, also report risk/precision and recurrence retention at 50% and 80% coverage, but these are secondary descriptive points, not the sole confirmatory gate.

### 13.6 Evidence-scoping decision metrics

For each predeclared or calibration-derived operating point report:

- fraction of claims labeled `cross-context-supported`;
- fraction retained as `source-context-only`;
- observed target non-recurrence risk among `cross-context-supported` claims;
- recurrence retention among supported claims;
- **absolute risk reduction** versus always-generalize at the same evaluated population;
- **risk difference** versus persistence at matched coverage;
- **coverage difference** versus persistence at matched risk where both methods reach the target;
- package-macro versions of the same measures where meaningful.

If an optional uncertainty/abstention sensitivity is evaluated, report it separately and do not merge it into the core two-scope results.

### 13.7 Macro and worst-stratum reporting

Every main metric must be reported at least as:

1. claim-micro;
2. macro across eligible indicators;
3. package-macro where meaningful.

Also report the worst indicator’s supported non-recurrence risk among indicators for which the metric is defined, always alongside that indicator’s claim and package counts. Sparse indicators remain visible as sparse/uncertain rather than being silently excluded by a post-hoc support threshold. This prevents common flags from hiding poor performance on smaller indicators.

---

## 14. Tie handling and undefined metrics

Persistence gives identical scores to many claims. Row order must never decide which tied claim enters a fixed-coverage tranche.

For fixed-coverage summaries:

- use fractional tie handling at the cutoff, or an exactly equivalent expected-value calculation;
- persist the tie rule in the metric artifact;
- test the result against row permutations.

If a metric is mathematically undefined because no claims are selected, no failures occur, or a stratum contains one target class, store `NA` with a machine-readable reason. Never silently substitute zero.

---

## 15. Uncertainty and statistical comparison

Claims from the same package are correlated. Claim-level IID confidence intervals are therefore invalid.

### 15.1 Package-cluster bootstrap

Use a paired **package-cluster bootstrap** on the concatenated out-of-fold test predictions:

- resample package groups with replacement;
- include all claims belonging to each sampled package;
- use the same resample for CASE and every baseline;
- 10,000 bootstrap resamples;
- report 95% percentile confidence intervals for metric values and paired differences.

The bootstrap seed is frozen in the confirmatory configuration.

### 15.2 Interpretation

The project prioritizes effect sizes and uncertainty intervals over p-value hunting.

The five outer folds are evaluation partitions, not independent replications. Do not report `mean ± SD across folds` as if `n=5` were the scientific sample size. Fold-level values may be shown diagnostically, while confirmatory uncertainty comes from package-cluster resampling of out-of-fold predictions.

---

## 16. Main experiments

Only the following core experiments are required initially.

### `validate-selene-contract`

**Purpose:** prove the data, identities, pairing, indicators, and provenance match the roadmap.  
**Outputs:** dataset manifest, schema manifest, checksums, join audit, duplicate audit, indicator inventory, paired/unpaired counts.  
**Completion condition:** no unresolved identity/join ambiguity in the primary population.

### `audit-paired-population`

**Purpose:** quantify selection differences between paired and Android-10-only observations.  
**Outputs:** prevalence-difference table, claim-count distribution, package summary.  
**Interpretation rule:** there is no performance gate; findings define the population limitation and may narrow the population claim.

### `reproduce-exploratory-baselines`

**Purpose:** reproduce the known persistence and pooled-logistic exploratory results using the new implementation.  
**Outputs:** side-by-side reproducibility table against the audited FedIEC numbers.  
**Completion condition:** unexplained material discrepancies are resolved before the main frozen evaluation; if the historical result was wrong, the corrected result becomes the new reference.

### `evaluate-case-scoping`

**Purpose:** answer RQ2 and RQ3 using the frozen five-fold grouped out-of-fold protocol.  
**Methods:** always-generalize, persistence, activity-volume, CASE pooled logistic, secondary per-indicator logistic.  
**Primary metrics:** Brier difference, log-loss difference, generalized risk-coverage difference.  
**Outputs:** OOF predictions, probability metrics, risk-coverage curves, evidence-scoping-policy tables, package-cluster bootstrap intervals.

### `stress-indicator-and-direction`

**Purpose:** answer RQ4 and expose hidden dependence on a few indicators or one direction.  
**Analyses:** per-indicator metrics, macro/worst indicator, package-macro, Android10→14 vs Android14→10, schema-defined broad-only sensitivity, source-activity baseline comparison.  
**Interpretation rule:** sensitivity findings may narrow or qualify the final claim but must not be used to redefine the primary metrics after the fact.

Optional second-dataset replication is **not required** for the initial chapter. It becomes a separate experiment only if a lawfully reusable dataset measures a genuinely comparable source-positive recurrence construct.

---

## 17. Claim-to-evidence contract

The claim contract keeps the chapter honest without turning every numerical threshold into a kill switch. Results determine the **strength and scope of the claim**.

Use the following evidence labels:

```text
SUPPORTED
PARTIALLY_SUPPORTED
NOT_SUPPORTED
INSUFFICIENT_EVIDENCE
```

`NOT_SUPPORTED` means that a particular claim is not justified by the current evidence; it does not automatically invalidate the project.

### Claim A — context-specific recurrence exists

> Source-positive recorded SELENE indicators do not recur uniformly across the two tested execution contexts.

**Evidence:** RQ1 descriptive recurrence, indicator-level distributions, and both directions.  
**If strong:** report material and heterogeneous non-recurrence.  
**If weaker:** narrow the statement to the indicators/direction where heterogeneity is observed.  
**If nearly universal:** do not manufacture heterogeneity; report that simple portability is a strong baseline for this artifact.  
**Must not become:** “Android 10 causes behavior X” or “the APK cannot perform X on Android 14.”

### Claim B — source context contains recurrence signal

> Source-context information carries information about recorded target-context recurrence beyond per-indicator persistence.

**Primary evidence:** paired OOF Brier and log-loss differences, supported by calibration/ranking diagnostics.

Interpretation:

- **`SUPPORTED`** — CASE improves proper scoring in both directions with uncertainty consistent with a real improvement.
- **`PARTIALLY_SUPPORTED`** — improvement is modest, metric-dependent, indicator-dependent, or directional.
- **`NOT_SUPPORTED`** — persistence performs as well or better under the valid protocol.
- **`INSUFFICIENT_EVIDENCE`** — the comparison cannot be interpreted because of a validity/data issue that cannot yet be repaired.

A `PARTIALLY_SUPPORTED` result is entirely acceptable and should directly shape the chapter wording.

### Claim C — CASE improves evidence scoping

> CASE provides a more useful recurrence-risk/coverage trade-off than a simple persistence-based policy in at least some practically relevant parts of the frontier.

**Primary evidence:** full risk-coverage curves, generalized risk-coverage summary, matched-coverage risk differences, and matched-risk coverage differences.

Interpretation:

- broad improvement → claim a general scoping benefit within the tested artifact;
- improvement only at selective coverage → claim a targeted selective-reporting benefit;
- improvement only in one direction/indicator family → make the claim explicitly conditional;
- no material improvement → report that simple persistence is sufficient under the tested conditions and retain CASE's value as an audited evidence-scoping framework only if the full analysis still provides a meaningful contribution.

Do not rewrite the operating points after the test outcomes are known.

### Claim D — context-scoped reporting is operationally interpretable

> CASE can convert a recurrence score into a transparent decision about whether to carry a recorded claim into a named target context or keep it source-context-specific.

**Evidence:** threshold/coverage tables, examples, and deterministic status assignment from calibration-only choices.

The required core statuses are only:

```text
cross-context-supported
source-context-only
```

An uncertainty/abstention state is optional and must earn its place empirically; it is not required for the contribution.

### Claim E — PhD implication

> Heterogeneous environments can require reliability-aware handling of shared security evidence, which is relevant to collaborative malware detection under heterogeneous participants.

**Class:** conceptual implication only.  
No CASE experiment can mark FL or IoT effectiveness as empirically supported.

### 17.1 Adaptation rule

The discovery work preceding CASE-Android was intentionally extensive so that implementation starts from a feasible, evidence-backed problem rather than from a speculative algorithm. If later audits expose an issue, adapt in the smallest scientifically valid way:

1. fix validity problems first;
2. preserve the original evidence;
3. revise the protocol identity when a scientific contract changes;
4. reduce or redirect the claim to match the corrected evidence;
5. avoid adding complexity merely to rescue a preferred conclusion.

This is the project-wide rule for gates, claims, and sensitivity findings.

---

## 18. Loopholes and threat controls

This section records the main ways CASE-Android could accidentally overstate its contribution.

| Loophole / threat | Why it matters | Required control |
|---|---|---|
| Target leakage | The target context makes recurrence trivial if inspected | strict source-feature allowlist; target-column poison tests |
| Strict intersection used as a “baseline” | Intersection sees the target report | retrospective reference only, never prospective competitor |
| High recurrence inflates AP | AP near 1 can look impressive for weak models | Brier/log loss + prevalence + selective-risk metrics are primary |
| Overlapping random splits | historical seeds are correlated | non-overlapping package-grouped OOF protocol |
| Claim dependence within APK/package | IID intervals are too narrow | package-grouped splitting and package-cluster bootstrap |
| Common indicators dominate micro results | a few frequent flags can hide weak strata | macro-indicator, package-macro, and worst-indicator reporting |
| Derived indicators duplicate broad flags | model can exploit parser redundancy | schema-defined broad-only sensitivity; no test-derived subset |
| Paired-cohort selection | paired APKs may differ from Android-10-only population | explicit paired-population audit |
| Direction asymmetry misread as OS causality | source-positive conditioning changes the evaluated cohort | report each direction separately; no causal language |
| Same parser in both contexts | correlated parser errors can look like portability | fidelity caveat + broad-only sensitivity; no truth claim |
| Finite Monkey execution | non-observation may reflect untriggered behavior | target is recurrence, never absence |
| Threshold tuning on test | creates optimistic status performance | nested calibration groups only |
| Tie-dependent ranking | row order can change top-coverage baseline | fractional tie handling + permutation tests |
| Data-driven indicator exclusion | post-hoc “non-saturated” subset inflated earlier results | all 19 primary; any subset defined before target test |
| Activity-volume shortcut | model may learn only that busy reports recur more | dedicated activity-volume baseline |
| No independent external replication | generalization beyond SELENE is uncertain | limit claims; optional later replication, not invented |

---

## 19. Literature position and novelty boundary

The targeted audit confirms that the broad neighboring problems are already occupied:

- **Cross-device behavioral consistency (2022)** shows that Android system-call behavior and malware-detection performance vary across real and virtual devices. CASE cannot claim discovery of environment-dependent behavior.
- **SELENE / ARTEMIS** provides the recorded Android 10/API29 and Android 14/API34 evidence and explicitly states that the artifacts are finite observations, not behavior truth. CASE builds on these artifacts rather than reproducing SELENE’s semantic-compaction contribution.
- **DYNAMISM 2016–2023 (2026)** includes repeated Android executions and explicitly targets detector stability; its files are restricted. CASE therefore does not claim generic repeatability as novel.
- **FARO-Droid (2026)** explicitly models per-sample feature reliability for robust Android malware detection under obfuscation. CASE cannot claim generic reliability-aware feature fusion.
- **Android malware conformal-prediction work (2023)** already addresses uncertainty guarantees for final malware classifications. CASE is not a confidence layer for benign/malicious verdicts.
- **Selective-classification literature** formalizes accuracy/risk versus coverage and recent work warns that naive risk-coverage evaluation can be misleading. CASE uses this literature for evaluation, not as its novelty claim.

The residual CASE contribution is narrower:

> **A source-to-target, claim-level evidence-scoping policy for recorded Android behavioral-security assertions, evaluated by recurrence probability quality and selective-reporting risk/coverage.**

A final literature check before chapter submission should focus on this exact capability, not restart a broad search across all Android malware research.

### Web-verified anchors

- SELENE Android Paper Artifacts: https://huggingface.co/datasets/serrooT/selene-android-paper-artifacts
- Cross-device behavioral consistency: https://doi.org/10.1016/j.mlwa.2022.100357
- FARO-Droid: https://doi.org/10.1016/j.jisa.2026.104503
- DYNAMISM 2016–2023: https://doi.org/10.5281/zenodo.21280255
- Android Malware Detection with Unbiased Confidence Guarantees: https://arxiv.org/abs/2312.11559
- Selective-classification evaluation (NeurIPS 2024): https://doi.org/10.52202/079017-0076
- Classifier calibration survey: https://doi.org/10.1007/s10994-023-06336-7

---

## 20. Exploratory versus confirmatory evidence

### Existing exploratory evidence

The historical R5 probes establish feasibility and informed this roadmap. They remain exploratory because they used overlapping random group splits, a narrow baseline set, and some post-hoc sensitivity definitions.

They may be reported as development history but not merged with confirmatory estimates.

### Confirmatory freeze

Before `evaluate-case-scoping` produces confirmatory test predictions, freeze and commit:

- SELENE file identities/checksums;
- paired-population construction;
- 19-indicator primary schema;
- package grouping key;
- five outer folds and inner calibration groups;
- feature allowlist;
- logistic model contract;
- any optional operating-point thresholds or risk targets used for categorical reporting;
- the rule for any optional abstention sensitivity, if such a sensitivity is retained;
- baseline definitions;
- metric formulas and tie handling;
- package-cluster bootstrap seed and resample count;
- claim-interpretation and adaptation rules above.

Any later change creates a new protocol identity and cannot silently overwrite the frozen confirmatory run.

---

## 21. Scientific outputs

Every numerical chapter result must have a machine-readable parent.

Minimum promoted evidence:

1. dataset/provenance table;
2. paired-population selection audit;
3. recurrence-by-indicator table;
4. probability-quality comparison table;
5. risk-coverage figure for each direction;
6. evidence-scoping table at the declared coverage/risk operating points;
7. per-indicator robustness figure/table;
8. claim-support summary with `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, or `INSUFFICIENT_EVIDENCE`.

Figures and chapter tables are generated from validated structured results; values are not manually transcribed into code or configuration.

---

## 22. Implementation phases and adaptive scientific gates

The phases below protect correctness and reproducibility. They are not a chain of arbitrary performance hurdles. CASE-Android was selected after extensive feasibility research; when a valid experiment is weaker than expected, the normal action is to adapt the claim or operating scope rather than discard the entire direction.

### Phase 1 — Foundation and provenance

Implement the dataset manifest, schema validation, immutable external-data access, and project configuration.

**Completion condition:** `validate-selene-contract` reproduces audited identities and fails loudly on mismatched files/schema.

### Phase 2 — Canonical paired-claim dataset

Implement exact APK pairing, package grouping, source-positive claim construction, and direction generation.

**Completion condition:** package leakage is structurally prevented and population counts reconcile with the audit or any discrepancy is explained and documented.

### Phase 3 — Baselines and metric engine

Implement always-generalize, persistence, activity-volume, pooled logistic, per-indicator logistic, proper scores, selective-risk metrics, tie handling, and package bootstrap.

**Completion condition:** hand-computed fixtures, leakage tests, and row-permutation tests pass.

### Phase 4 — Exploratory reproduction

Reproduce the existing FedIEC R5 baseline numbers within explained tolerance.

**Completion condition:** differences are reconciled. If a historical result was wrong, preserve that fact and update the starting expectation rather than forcing reproduction.

### Phase 5 — Freeze the valid evaluation protocol

Persist the outer folds, calibration groups, source-feature contract, model/baseline definitions, metric definitions, and any operating points that will be shown.

**Completion condition:** the pre-confirmatory checklist is complete and the protocol no longer depends on unseen outer-test outcomes.

### Phase 6 — Main CASE evaluation

Run `evaluate-case-scoping` and `stress-indicator-and-direction`.

**Completion condition:** all OOF predictions, metrics, uncertainty intervals, scoping decisions, and sensitivity outputs validate.

The result is then interpreted according to the claim contract:

- broad improvement → broad but bounded claim;
- modest improvement → modest claim;
- directional/stratum-specific improvement → conditional claim;
- simple baseline parity → report the parity and narrow the contribution;
- structural validity failure → repair/re-scope before interpretation.

### Phase 7 — Chapter evidence

Promote only validated outputs needed by the chapter.

**Completion condition:** every manuscript-facing number traces to an immutable result artifact and every statement stays within the claim-to-evidence contract.

---

## 23. Final pre-confirmatory checklist

The confirmatory run must not begin until every item is true:

- [ ] SELENE source revision and local checksums recorded.
- [ ] Dataset license/citation requirements recorded.
- [ ] Exact paired population reproduced.
- [ ] Paired-vs-unpaired selection audit completed.
- [ ] All 19 primary indicators frozen.
- [ ] Any broad-only sensitivity subset defined from schema semantics only.
- [ ] Package grouping validated with zero cross-partition leakage.
- [ ] Five outer folds persisted; each package is test exactly once.
- [ ] Inner calibration groups persisted.
- [ ] Feature allowlist contains no target-context or identity fields.
- [ ] Primary CASE model contract frozen.
- [ ] Baselines frozen, including activity-volume shortcut baseline.
- [ ] Any categorical operating points to be reported are defined from training/calibration evidence only.
- [ ] Any optional uncertainty/abstention sensitivity is predeclared separately from the core two-scope policy.
- [ ] Brier, log loss, generalized risk-coverage, coverage/risk, and recurrence-retention formulas tested.
- [ ] Tie handling verified under row permutation.
- [ ] Package-cluster bootstrap implementation verified on known fixtures.
- [ ] Undefined-metric rules tested.
- [ ] Claim interpretation rules frozen; effect strength may change claim strength but not metric definitions.
- [ ] Existing exploratory results clearly separated from confirmatory evidence.
- [ ] No FL/IoT, malware-truth, OS-causal, or analyst-benefit claim appears in the planned outputs.

---

## 24. Roadmap authority

This document is the scientific source of truth for CASE-Android.

`technical_doc.md` may determine **how** the software implements this roadmap, but it may not redefine:

- the estimand;
- the population;
- feature availability;
- baselines;
- split semantics;
- metrics;
- evidence-scoping policy;
- claim boundaries and adaptation rules.

If implementation reveals that a scientific contract is infeasible or incorrect, update this roadmap explicitly before changing the scientific behavior of the code.
