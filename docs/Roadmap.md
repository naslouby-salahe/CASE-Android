# CASE-Android Research Roadmap

**Project:** CASE-Android  
**Acronym:** Context-Aware Scoping of Evidence in Android  
**Full title:** *CASE-Android: Context-Aware Claim Portability for Recorded Android Behavioral-Security Evidence Across Versioned Execution Contexts*  
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

These results are **exploratory only**. The three historical `GroupShuffleSplit` runs overlap and are not independent replications. The earlier “non-saturated” slice used target-test prevalence to select indicators and is therefore post-hoc; it cannot become the protocol-frozen headline.

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

### RQ1 — Cross-context recurrence and portability structure

**How often, and for which indicators, do recorded behavioral-security observations agree or disagree across the paired Android execution contexts?**

RQ1 is intentionally broader than a one-direction conditional recurrence rate. It characterizes the paired context relationship using both directional source-positive recurrence and symmetric paired-context summaries, without attributing observed differences causally to Android OS version alone.

### RQ2 — Source-only recurrence estimation

**Can source-context information estimate claim recurrence better than simple training-only prevalence and per-indicator persistence baselines?**

The primary comparison is probabilistic quality, not malware-detection accuracy.

### RQ3 — Evidence-scoping utility

**Does CASE improve the selective reporting frontier: lower target non-recurrence among claims labeled cross-context-supported while preserving useful claim coverage?**

This is the main operational question.

### RQ4 — Heterogeneity, fidelity, and robustness

**How stable are recurrence patterns and CASE benefit across direction, indicator, package weighting, report-level aggregation, broad-versus-derived indicator definitions, and fidelity strata?**

This determines whether the result is a broad reporting effect or a small artifact of a few common indicators, parser-derived redundancy, or one direction.

### 7.1 RQ-to-evidence map

| RQ | Population / unit | Main comparison | Primary evidence | Permitted interpretation |
|---|---|---|---|---|
| RQ1 | paired APKs and source-positive claims | descriptive | directional recurrence; `n00/n01/n10/n11`; disagreement; Jaccard; paired prevalence difference; paired-population audit | recorded evidence portability differs across indicators and/or directions in the tested contexts |
| RQ2 | held-out package-grouped claims | CASE score vs global prevalence and per-indicator persistence | Brier, log loss, Brier skill, paired package-bootstrap deltas | source-only context carries predictive information about recorded recurrence beyond simple priors |
| RQ3 | same held-out claims and APK reports | CASE selective policy vs persistence ranking / always-generalize | generalized risk-coverage, ordinary AURC, risk at coverage, coverage at risk budget, recurrence retention, report-level scoping metrics | CASE changes the evidence-scoping trade-off |
| RQ4 | direction, indicator, package, report, and fidelity strata | macro/worst-stratum and predeclared sensitivities | per-indicator metrics, package/report-macro metrics, broad-indicator sensitivity, fidelity sensitivity, broken-pair negative control | benefit/limitations are heterogeneous or robust within this artifact |

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

Before the protocol-frozen evaluation, run `audit-paired-population`:

- compare Android-10 paired vs Android-10-only flag prevalences;
- compare number of positive flags per APK;
- compare package-group composition where possible;
- report absolute prevalence differences for every flag;
- report the largest absolute prevalence difference and macro mean difference;
- do not infer why an APK is unpaired unless the source metadata supports that explanation.

This audit does not “correct” the paired population. It defines the population to which the protocol-frozen claims apply and quantifies how selective that population may be.

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

These values were already used during exploration. They are frozen before the protocol-frozen evaluation, and there is no hyperparameter search against outer-test outcomes. Because the model family and these settings were informed by earlier work on the same SELENE population, the main evaluation is described as **protocol-frozen post-exploratory out-of-fold evaluation**, not as an independent external confirmation study.

A separate per-indicator logistic model is retained as a **secondary complexity comparator**, not the definition of CASE.

### 10.3 Report-scope policy

The primary CASE output is a **continuous recurrence score** for each source-positive claim. The score is the scientific object; any categorical reporting rule is a readable operating view derived from that score.

The default two-scope interpretation is:

- **`cross-context-supported`** — the score is high enough, under a threshold chosen without using outer-test outcomes, to justify carrying the recorded claim into the named target context.
- **`source-context-only`** — keep the claim tied to the source context rather than generalizing it. This does **not** mean the behavior is absent in the target context.

CASE does **not** require a third `insufficiently-tested` outcome. If an indicator is genuinely too sparse for a reliable stratum-specific estimate, that limitation is reported through its sample/package count, uncertainty interval, and `NA` metric rules rather than converted into an artificial scientific class.

An optional abstention/uncertainty region may be evaluated later as a **secondary sensitivity analysis** if the score calibration shows that it adds useful information. It is not part of the core contribution and is not required for the chapter.

### 10.4 Operating points are descriptive, not project gates

The primary evidence is the complete probability-quality and risk-coverage analysis. Fixed operating points are used to make the trade-off easy to interpret, not to decide whether CASE-Android “passes” or “fails.”

The roadmap keeps the exploratory **50% and 80% coverage** views because they are already interpretable from the existing PoC. It may additionally show one or more recurrence-risk targets such as 5% or 10% when the calibration data support them.

For each outer fold, any reporting threshold must be chosen from calibration data only after the probability model has been fit on the fold's fit partition. If a requested risk target is not achievable at useful coverage, report that fact and the achievable frontier. Do **not** lower the target after inspecting the outer test set, but also do **not** treat an unavailable operating point as project failure.

A stronger finite-sample risk-control layer may be explored later only as a clearly separated extension. It is not part of the core CASE claim unless its assumptions are explicitly satisfied under package dependence and selective-set evaluation.

### 10.5 Support and sparse-stratum rule

The term **support gating** means only checking whether a secondary stratum-specific model or metric is mathematically estimable from the fit/calibration partitions. It must never remove claims from the primary 19-indicator population because their outer-test outcomes are inconvenient.

Rules:

- all 19 audited indicators remain in the primary pooled CASE evaluation;
- sparse indicators remain visible with counts and uncertainty;
- a secondary per-indicator logistic model may be `NA` when its fit partition is not estimable;
- an undefined secondary metric/model does not remove that indicator's claims from pooled or descriptive evaluation;
- all feasibility rules are based on fit/calibration support only, never outer-test outcomes.

### 10.6 Probability-stability contract

For metrics requiring finite probabilities:

- store the raw model probability separately from the evaluation probability;
- for log loss only, clip evaluation probabilities to `[1e-6, 1 - 1e-6]`;
- Brier, ranking, and risk-coverage computations use the raw probability unless the metric implementation mathematically requires otherwise;
- if an indicator has no source-positive fit claims for the per-indicator persistence baseline in a fold, fall back to that direction's global fit-partition recurrence prevalence and mark the fallback in the prediction artifact;
- secondary per-indicator logistic models that cannot be fit receive `NA` rather than a hidden fallback.

### 10.7 Adaptive evidence rule

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

**Direction-global prevalence**  
Every source-positive claim receives the overall recurrence prevalence estimated from the **fit partition only** for that direction. This is the weakest probabilistic prior and quantifies how much is gained merely by knowing the base rate.

**Per-indicator persistence**  
For each indicator, predict the fit-partition recurrence rate for every source-positive claim of that indicator. This is the principal simple baseline. If an indicator has no source-positive fit claims in a fold, use the declared global-prevalence fallback from Section 10.6 and record the event.

**Activity-volume baseline**  
Use indicator identity plus only the source report’s total positive-flag count. This tests whether CASE merely exploits “busy apps have more recurring flags.”

**CASE pooled logistic**  
Indicator identity plus the complete source Boolean flag vector. This is the primary method.

**Per-indicator logistic**  
One simple logistic model per indicator using source flags. This is a secondary comparator to test whether indicator-specific weights are materially necessary.

### 11.2 Fair data-budget contract

Every learned probabilistic method and learned baseline obeys the same fold-local information budget:

- **fit groups** may train probability models or estimate recurrence priors;
- **calibration groups** may select reporting thresholds/risk budgets and support diagnostics, but their target labels may not be used to refit CASE probabilities or persistence estimates;
- **outer-test groups** may only be scored and evaluated;
- target labels from calibration or outer-test groups never enter feature selection or model training.

This prevents CASE from being compared against a persistence baseline that was estimated from more labeled recurrence data than CASE itself was allowed to use.

### 11.3 Retrospective descriptive reference

**Strict intersection** requires observing both source and target reports. It is therefore not a prospective baseline for CASE. It may be reported only as a descriptive “what would remain if both reports were already available?” reference.

It must never be presented as a deployable competitor in the main predictive comparison.

---

## 12. Protocol-frozen post-exploratory split and evaluation protocol

The previous three random grouped splits are exploratory and are not reused as main evidence. The protocol below is frozen before the main out-of-fold run, but it is **not described as statistically independent external confirmation**, because the same SELENE population informed earlier exploratory model and analysis choices.

### 12.1 Outer evaluation

Use **five non-overlapping package-grouped outer folds**. Build the fold manifest once from the paired-APK table (one row per paired APK, grouped by `package_name`) with `GroupKFold(n_splits=5)`, without using target recurrence labels. Reuse the same package-to-fold assignment for both directions. Each package appears in the test partition of exactly one outer fold.

A persisted `split_manifest` must record for every APK/package:

- package group;
- APK hash;
- outer fold;
- direction eligibility;
- fit/calibration/test role for each fold.

Before model execution, publish a **fold-balance audit** containing, for each fold and direction:

- package count;
- paired APK count;
- source-positive claim count;
- per-indicator source-positive support;
- source-context positive-flag-count distribution.

The audit is descriptive only. Once the target-label-blind fold manifest is frozen, it must not be regenerated merely because a later outer-test stratum looks inconvenient.

### 12.2 Inner calibration

Within each outer-training partition, reserve **20% of the outer-training package groups** as a deterministic calibration subset using one fixed calibration seed plus the outer-fold identity. Models fit only the remaining fit groups. Calibration groups are used for:

- CASE risk-budget threshold selection;
- operating-point selection;
- support/estimability diagnostics defined in Section 10.5;
- calibration-partition diagnostics used only to assess threshold stability.

The primary protocol does **not** add Platt scaling, isotonic regression, temperature scaling, or another post-hoc probability calibrator. The logistic probabilities are evaluated as produced.

**Headline probability-calibration metrics are computed only from concatenated outer-test OOF predictions.** Calibration-partition plots or diagnostics may be stored for development auditing but must not be reported as if they were held-out calibration performance.

Outer-test outcomes are never used for method selection, threshold selection, indicator eligibility, calibration, or support decisions.

### 12.3 Out-of-fold evidence

After all five outer folds:

- every eligible package has exactly one out-of-fold test prediction;
- concatenate out-of-fold predictions for overall evaluation;
- retain fold identity for diagnostics;
- do not treat the five folds as five independent studies.

### 12.4 No target-derived feature selection

The primary analysis includes all 19 audited indicators.

Any “broad-only” sensitivity subset must be defined **from source schema semantics before the protocol-frozen outer-test outcomes are inspected**. The historical `<98% target recurrence` rule is forbidden because it used target outcomes to define eligibility.

### 12.5 Fidelity sensitivity definition

Fidelity analysis is a sensitivity control, not a new prediction label and not a reason to discard inconvenient indicators.

Before the main evaluation:

- freeze which indicators have a direct auditable mapping to the released fidelity evidence;
- record direction-specific raw-evidence/processed-flag agreement where the oracle supports it;
- distinguish directly mapped indicators from indicators without an equivalent raw-evidence mapping;
- retain measured agreement as a continuous descriptive quantity rather than selecting indicators by a recurrence-informed threshold.

Primary CASE results remain all-19-indicator results. Fidelity-stratified results are secondary and answer whether apparent portability or CASE benefit is concentrated in indicators with stronger or weaker provenance agreement.

---

## 13. Metrics

High recurrence makes some standard ranking metrics look impressive even for weak models. CASE therefore uses metrics tied directly to probability quality, paired portability structure, and selective reporting.

### 13.1 Descriptive recurrence and paired portability

For each direction and indicator report:

- source-positive claim count;
- package count;
- target recurrence rate;
- 95% package-cluster bootstrap interval;
- macro mean, median, IQR, minimum, and maximum recurrence across indicators.

For each indicator over the paired APK population also report the symmetric 2×2 context table:

```text
n00: absent in both contexts
n01: absent in Android 10, present in Android 14
n10: present in Android 10, absent in Android 14
n11: present in both contexts
```

Derived paired summaries:

- **paired disagreement rate** `(n01 + n10) / N_paired`;
- **Jaccard overlap** `n11 / (n11 + n10 + n01)` when defined;
- **paired prevalence difference** `P(x14=1) - P(x10=1)`;
- both directional source-positive recurrence rates shown side by side.

These symmetric summaries prevent directional conditioning from being mistaken for a direct OS effect.

### 13.2 Primary probabilistic metrics

**Brier score**  
Primary proper scoring rule for recurrence probability quality.

\[
BS = rac{1}{N}\sum_i (\hat p_i-y_i)^2.
\]

Report paired differences for CASE against both direction-global prevalence and per-indicator persistence; negative is better.

**Brier Skill Score versus persistence**  
Secondary effect-size companion:

\[
BSS_{persist}=1-rac{BS_{CASE}}{BS_{persistence}}.
\]

Positive values indicate improvement over persistence. Raw Brier remains the primary proper score.

**Log loss**  
Secondary proper scoring rule that penalizes overconfident errors. Apply the probability-stability contract from Section 10.6.

These are preferred over ECE as primary metrics because Brier and log loss are proper scoring rules. Binned ECE may be reported only as a descriptive calibration diagnostic.

### 13.3 Calibration diagnostics

Using **outer-test OOF predictions only** for the headline evaluation, report:

- calibration intercept with package-bootstrap interval;
- calibration slope with package-bootstrap interval;
- reliability plot with predeclared bins;
- descriptive ECE with the exact binning rule stated;
- Brier by direction and indicator.

Do not claim “calibrated” merely because ECE is small.

### 13.4 Ranking metrics

Recurrence average precision remains secondary because recurrence prevalence is high and raw recurrence AP can look impressive even for weak scores. Always report recurrence prevalence next to recurrence AP.

Also report **non-recurrence AP** by ranking claims with `1 - p_hat` against target label `1 - y`. This directly measures ranking of the operational failure event and is less visually saturated when recurrence is common.

AP lift over persistence may be reported for both recurrence and non-recurrence ranking; neither AP replaces the proper scoring rules.

### 13.5 Selective-reporting metrics

For threshold `τ`:

**Supported coverage**

\[
C(	au)=rac{\#\{i:\hat p_i\ge	au\}}{N}.
\]

**Supported non-recurrence risk**

\[
R(	au)=rac{\sum_i \mathbf 1[\hat p_i\ge	au](1-y_i)}{\sum_i \mathbf 1[\hat p_i\ge	au]}.
\]

This is the main operational error quantity. It must not be renamed malware false-positive rate.

**Recurrence retention**

\[
U(	au)=rac{\sum_i \mathbf 1[\hat p_i\ge	au]y_i}{\sum_i y_i}.
\]

This measures how much genuinely recurrent recorded evidence is retained.

**Risk-coverage curve**  
Plot `R(τ)` against `C(τ)` over all score thresholds.

**AUGRC / generalized risk-coverage summary**  
Use generalized risk-coverage area as the primary threshold-independent selective-reporting summary, treating target non-recurrence as the selective error event. Report the exact implementation contract and orientation; lower is better. Validate the implementation against both a hand-computable fixture and an independent formula/reference implementation before the protocol-frozen run.

**Ordinary AURC**  
Report ordinary AURC secondarily for comparability with broader selective-prediction literature. It does not replace AUGRC.

For continuity with the exploratory work, also report risk/precision and recurrence retention at 50% and 80% coverage, but these are secondary descriptive points, not the sole decision criterion.

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

### 13.7 APK/report-level metrics

Because CASE is a reporting contribution, claim-level metrics are necessary but not sufficient. At each declared operating point, aggregate predictions by source APK report and report:

- **report supported fraction:** selected claims / source-positive claims within each report, summarized macro across APKs;
- **report non-recurrence risk:** non-recurrent selected claims / selected claims within each report, macro across reports with at least one selected claim;
- **report failure incidence:** fraction of reports with at least one selected claim that fails to recur;
- **report recurrence retention:** recurrent selected claims / all recurrent source-positive claims within each report, macro where defined;
- distribution of selected-claim counts per report.

These metrics do not establish analyst productivity or real-world security benefit. They show whether a claim-level policy behaves coherently when reconstructed into the report-shaped object it is intended to scope.

### 13.8 Macro and worst-stratum reporting

Every main metric must be reported at least as:

1. claim-micro;
2. macro across eligible indicators;
3. package-macro where meaningful;
4. APK/report-macro where meaningful.

Also report the worst indicator’s supported non-recurrence risk among indicators for which the metric is defined, always alongside that indicator’s claim and package counts. Sparse indicators remain visible as sparse/uncertain rather than being silently excluded by a post-hoc support threshold. This prevents common flags from hiding poor performance on smaller indicators.

---

## 14. Tie handling and undefined metrics

Persistence and prevalence baselines produce many identical scores. Row order must never decide which tied claim enters a fixed-coverage tranche.

For fixed-coverage summaries:

- use fractional tie handling at the cutoff, or an exactly equivalent expected-value calculation;
- persist the tie rule in the metric artifact;
- test the result against row permutations.

If a metric is mathematically undefined because no claims are selected, no failures occur, a denominator is zero, or a stratum contains one target class, store `NA` with a machine-readable reason. Never silently substitute zero.

Log-loss probability stabilization and persistence fallbacks follow Section 10.6 and must be recorded per fold rather than applied silently.

---

## 15. Uncertainty and statistical comparison

Claims from the same package and APK are correlated. Claim-level IID confidence intervals are therefore invalid.

### 15.1 Package-cluster bootstrap

Use a paired **package-cluster bootstrap** on the concatenated out-of-fold test predictions:

- resample package groups with replacement;
- include all claims belonging to each sampled package;
- use the same resample for CASE and every baseline;
- 10,000 bootstrap resamples;
- report 95% percentile confidence intervals for metric values and paired differences.

The bootstrap seed is frozen in the protocol-frozen evaluation configuration.

### 15.2 What the bootstrap does and does not measure

The package-cluster bootstrap quantifies **sampling uncertainty over the evaluated package population conditional on the frozen OOF fitted models and split manifest**. It does not fully propagate uncertainty from retraining new models under new fold assignments.

Therefore:

- do not describe the intervals as full pipeline-retraining uncertainty;
- retain fold-level values as diagnostics only;
- if computationally cheap, run one predeclared alternative target-label-blind grouped split manifest as a **split-sensitivity diagnostic**, not as another independent study and not as an opportunity to choose the better result.

### 15.3 Interpretation

The project prioritizes effect sizes and uncertainty intervals over p-value hunting.

The five outer folds are evaluation partitions, not independent replications. Do not report `mean ± SD across folds` as if `n=5` were the scientific sample size. Main uncertainty comes from paired package-cluster resampling of concatenated OOF predictions under the scope above.

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

### `characterize-paired-portability`

**Purpose:** answer the symmetric part of RQ1 before predictive modeling.  
**Outputs:** per-indicator `n00/n01/n10/n11`, directional recurrence, disagreement, Jaccard, prevalence difference, package-cluster intervals.  
**Interpretation rule:** this is descriptive portability evidence only; no OS-causal interpretation is permitted.

### `reproduce-exploratory-baselines`

**Purpose:** reproduce the known persistence and pooled-logistic exploratory results using the new implementation.  
**Outputs:** side-by-side reproducibility table against the audited FedIEC numbers.  
**Completion condition:** unexplained material discrepancies are resolved before the main frozen evaluation; if the historical result was wrong, the corrected result becomes the new reference.

### `evaluate-case-scoping`

**Purpose:** answer RQ2 and RQ3 using the frozen five-fold grouped OOF protocol.  
**Methods:** always-generalize, direction-global prevalence, per-indicator persistence, activity-volume, CASE pooled logistic, secondary per-indicator logistic.  
**Primary metrics:** Brier difference, log-loss difference, generalized risk-coverage difference.  
**Secondary metrics:** Brier skill, ordinary AURC, recurrence AP, non-recurrence AP, report-level metrics.  
**Outputs:** OOF predictions, probability metrics, risk-coverage curves, evidence-scoping-policy tables, report-level tables, package-cluster bootstrap intervals.

### `stress-indicator-direction-and-fidelity`

**Purpose:** answer RQ4 and expose hidden dependence on a few indicators, one direction, parser fidelity, or report aggregation.  
**Analyses:** per-indicator metrics, macro/worst indicator, package-macro, report-macro, Android10→14 vs Android14→10, schema-defined broad-only sensitivity, source-activity baseline comparison, fidelity-stratified sensitivity.  
**Interpretation rule:** sensitivity findings may narrow or qualify the final claim but must not be used to redefine the primary metrics after the fact.

### `broken-pair-negative-control`

**Purpose:** verify that CASE benefit depends on genuine source-target APK correspondence rather than only marginal indicator prevalence, parser artifacts, or accidental pipeline leakage.  
**Protocol:** within each frozen outer-test fold and direction, permute complete target-context APK flag vectors across test APKs using a fixed diagnostic seed, thereby preserving the target-context marginal indicator distribution while destroying source-target identity correspondence. Repeat over a predeclared diagnostic set of permutations.  
**Expected interpretation:** the full source-context feature vector should not show a stable meaningful advantage over simple recurrence priors once genuine pairing is destroyed. A persistent large advantage is an audit flag requiring leakage/parser-shortcut investigation before main claims are accepted.  
**Claim role:** negative-control diagnostic only; it is not a significance test and cannot rescue weak main results.

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

`NOT_SUPPORTED` means that a particular claim is not justified by the current evidence; it does not automatically invalidate every other descriptive contribution.

### Claim A — context-specific portability structure exists

> Recorded SELENE behavioral-security indicators do not exhibit identical portability across the two tested execution contexts.

**Evidence:** RQ1 directional recurrence, symmetric paired `n00/n01/n10/n11` structure, disagreement/Jaccard/prevalence differences, and indicator-level distributions.  
**If strong:** report material and heterogeneous non-recurrence/disagreement.  
**If weaker:** narrow the statement to the indicators/direction where heterogeneity is observed.  
**If nearly universal:** do not manufacture heterogeneity; report that simple portability is a strong descriptive baseline for this artifact.  
**Must not become:** “Android 10 causes behavior X” or “the APK cannot perform X on Android 14.”

### Claim B — source context contains recurrence signal

> Source-context information carries information about recorded target-context recurrence beyond global prevalence and per-indicator persistence.

**Primary evidence:** paired OOF Brier and log-loss differences, supported by Brier skill and calibration/ranking diagnostics.

Interpretation:

- **`SUPPORTED`** — CASE improves proper scoring over persistence in both directions with uncertainty consistent with a real improvement.
- **`PARTIALLY_SUPPORTED`** — improvement is modest, metric-dependent, indicator-dependent, or directional.
- **`NOT_SUPPORTED`** — persistence performs as well or better under the valid protocol.
- **`INSUFFICIENT_EVIDENCE`** — the comparison cannot be interpreted because of a validity/data issue that cannot yet be repaired.

A `PARTIALLY_SUPPORTED` result is acceptable and should directly shape the chapter wording.

### Claim C — CASE improves evidence scoping

> CASE provides a more useful recurrence-risk/coverage trade-off than a simple persistence-based policy in at least some practically relevant parts of the frontier.

**Primary evidence:** full risk-coverage curves, generalized risk-coverage summary, matched-coverage risk differences, matched-risk coverage differences, recurrence retention, and report-level scoping metrics.

Interpretation:

- broad improvement → claim a general scoping benefit within the tested artifact;
- improvement only at selective coverage → claim a targeted selective-reporting benefit;
- improvement only in one direction/indicator family → make the claim explicitly conditional;
- no material improvement anywhere on the valid frontier → **Claim C is `NOT_SUPPORTED`** and simple persistence is reported as sufficient under the tested conditions.

The framework vocabulary or the fact that the analysis was carefully audited must **not** be used to rescue Claim C when the predictive/scoping comparison does not improve on persistence. In that case, any remaining chapter contribution must stand separately on Claim A's descriptive portability analysis or another explicitly re-scoped contribution with a new protocol identity.

Do not rewrite the operating points after the test outcomes are known.

### Claim D — context-scoped reporting is operationally interpretable

> A recurrence score can be converted into a transparent decision about whether to carry a recorded claim into a named target context or keep it source-context-specific.

**Evidence:** threshold/coverage tables, deterministic calibration-only status assignment, and report-level reconstruction metrics.

The required core statuses are only:

```text
cross-context-supported
source-context-only
```

An uncertainty/abstention state is optional and must earn its place empirically; it is not required for the contribution.

Claim D establishes interpretability of the mechanism, not superiority. It cannot substitute for Claims B or C.

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
| Calling the same-population frozen run “independent confirmation” | exploratory work on SELENE already informed model/analysis choices | describe it as protocol-frozen post-exploratory OOF evaluation; reserve independent confirmation for unseen data |
| Strict intersection used as a “baseline” | intersection sees the target report | retrospective reference only, never prospective competitor |
| High recurrence inflates recurrence AP | AP near 1 can look impressive for weak models | Brier/log loss + prevalence + non-recurrence AP + selective-risk metrics are primary/secondary as declared |
| Baseline gets more recurrence labels than CASE | unfair data budget can make comparisons uninterpretable | fit/calibration/test information budget is identical across learned methods |
| Undefined “support gating” | could become a hidden post-hoc exclusion rule | support means estimability only; all 19 remain in pooled primary evaluation |
| Calibration evaluated on calibration data | produces optimistic reliability evidence | headline calibration metrics use outer-test OOF predictions only |
| Zero/one probabilities or empty fit strata | log loss may explode or baseline behavior becomes ad hoc | predeclared clipping/fallback contract with machine-readable flags |
| Overlapping random splits | historical seeds are correlated | non-overlapping package-grouped OOF protocol |
| Claim dependence within APK/package | IID intervals are too narrow | package-grouped splitting and package-cluster bootstrap |
| Bootstrap interpreted as full retraining uncertainty | OOF prediction bootstrap conditions on fitted models | state the conditional scope; optional predeclared split-sensitivity diagnostic |
| Rare indicators distributed awkwardly across folds | fold-specific estimability can vary even without leakage | target-label-blind fold-balance audit before execution; no post-outcome refolding |
| Common indicators dominate micro results | a few frequent flags can hide weak strata | macro-indicator, package-macro, report-macro, and worst-indicator reporting |
| Derived indicators duplicate broad flags | model can exploit parser redundancy | schema-defined broad-only sensitivity; no test-derived subset |
| Paired-cohort selection | paired APKs may differ from Android-10-only population | explicit paired-population audit |
| Direction asymmetry misread as OS causality | source-positive conditioning changes the evaluated cohort | symmetric paired metrics + both directions + no causal language |
| Same parser in both contexts | correlated parser errors can look like portability | fidelity sensitivity + broad-only sensitivity + no behavior-truth claim |
| Finite Monkey execution | non-observation may reflect untriggered behavior | target is recorded recurrence, never absence |
| Threshold tuning on test | creates optimistic status performance | nested calibration groups only |
| Tie-dependent ranking | row order can change top-coverage baseline | fractional tie handling + row-permutation tests |
| Data-driven indicator exclusion | post-hoc “non-saturated” subset inflated earlier results | all 19 primary; any subset defined before outer-test outcomes |
| Activity-volume shortcut | model may learn only that busy reports recur more | dedicated activity-volume baseline |
| Marginal-frequency/parser shortcut | model may appear useful without genuine APK-level cross-context relation | broken-pair target-report permutation diagnostic |
| Claim-level success does not imply coherent report behavior | CASE is positioned as a reporting layer | report-level supported fraction, risk, failure incidence, and retention |
| No independent external replication | generalization beyond SELENE is uncertain | limit claims; optional later replication, not invented |
| Careful framework used to rescue a null predictive result | methodology alone does not establish CASE benefit | Claims B/C become `NOT_SUPPORTED` when valid baselines are not improved |

---

## 19. Literature position and novelty boundary

The targeted audit confirms that the broad neighboring problems are already occupied:

- **A Comparative Study of Android Malware Behavior in Different Contexts (2016)** repeatedly executed malware under different simulation conditions and compared behavioral observations. CASE therefore cannot claim that comparing Android malware behavior across execution contexts is itself novel.
- **Cross-device behavioral consistency (2022)** shows that Android system-call behavior and malware-detection performance vary across real and virtual devices. CASE cannot claim discovery of environment-dependent behavior.
- **AndroCT (2021)** provides runtime call traces for Android apps executed on both an emulator and a real device and supports cross-environment behavioral study. CASE therefore cannot claim that paired Android runtime evidence across environment types is novel.
- **SELENE / ARTEMIS** provides the recorded Android 10/API29 and Android 14/API34 evidence and explicitly states that the artifacts are finite observations, not behavior truth. CASE builds on these artifacts rather than reproducing SELENE’s semantic-compaction contribution.
- **DYNAMISM 2016–2023 (2026)** includes repeated Android executions and explicitly targets detector stability; its files are restricted. CASE therefore does not claim generic repeatability as novel.
- **FARO-Droid (2026)** explicitly models per-sample feature reliability for robust Android malware detection under obfuscation. CASE cannot claim generic reliability-aware feature fusion.
- **Android malware conformal-prediction work (2023)** already addresses uncertainty guarantees for final malware classifications. CASE is not a confidence layer for benign/malicious verdicts.
- **Selective-classification literature** formalizes accuracy/risk versus coverage and recent work warns that naive risk-coverage evaluation can be misleading. CASE uses this literature for evaluation, not as its novelty claim.

### 19.1 Residual novelty target

CASE should not frame novelty around “context dependence,” “reliability,” “Android-version effects,” or “dynamic-analysis instability.” Those spaces are already occupied.

The residual contribution is the combination of three narrower objects:

1. **Claim-portability estimand** — treat one source-positive recorded behavioral-security assertion as context-bound evidence and estimate its recurrence in a named, still-unobserved target context.
2. **Evidence-scoping mechanism** — use that recurrence estimate to decide whether the assertion is carried into the target-context report or retained as source-context-only.
3. **Portability/scoping evaluation protocol** — evaluate this decision through proper probability scores, selective risk/coverage, symmetric paired portability, indicator/package/report heterogeneity, provenance/fidelity sensitivity, and negative controls.

The concise novelty statement is:

> **A source-to-target, claim-level evidence-portability and reporting-scope policy for recorded Android behavioral-security assertions, evaluated by recurrence probability quality and selective-reporting risk/coverage without observing the target context at decision time.**

The logistic regression itself is **not** the novelty claim. It is intentionally simple so that any benefit is attributable to the evidence-scoping formulation rather than architectural complexity.

A final literature check before chapter submission should focus on this exact capability: **predicting recurrence of an individual source-positive Android dynamic-analysis claim into a named unobserved target context and using that prediction to scope the report claim**. It should not restart a broad search across all Android malware research.

### 19.2 Web-verified anchors

- SELENE Android Paper Artifacts: https://huggingface.co/datasets/serrooT/selene-android-paper-artifacts
- A Comparative Study of Android Malware Behavior in Different Contexts: https://doi.org/10.5220/0005997300470054
- AndroCT: Ten Years of App Call Traces in Android: https://doi.org/10.1109/MSR52588.2021.00076
- Cross-device behavioral consistency: https://doi.org/10.1016/j.mlwa.2022.100357
- FARO-Droid: https://doi.org/10.1016/j.jisa.2026.104503
- DYNAMISM 2016–2023: https://doi.org/10.5281/zenodo.21280255
- Android Malware Detection with Unbiased Confidence Guarantees: https://arxiv.org/abs/2312.11559
- Selective-classification evaluation (NeurIPS 2024): https://doi.org/10.52202/079017-0076
- Classifier calibration survey: https://doi.org/10.1007/s10994-023-06336-7

---

## 20. Exploratory evidence versus protocol-frozen evaluation

### Existing exploratory evidence

The historical R5 probes establish feasibility and informed this roadmap. They remain exploratory because they used overlapping random group splits, a narrow baseline set, and some post-hoc sensitivity definitions.

They may be reported as development history but not merged with the protocol-frozen OOF estimates.

### 20.1 Interpretation of the main frozen run

The main five-fold OOF evaluation is **protocol-frozen after exploration**. Its purpose is to prevent further test-driven tuning and obtain one coherent held-out prediction for each eligible package under a locked analysis contract.

It is not independent external confirmation because:

- the SELENE population was already inspected during discovery;
- the pooled logistic family and fixed `C=1` setting were already used in exploration;
- the choice of core problem and several evaluation views was informed by exploratory results.

Therefore manuscript wording should use terms such as:

```text
protocol-frozen evaluation
locked out-of-fold evaluation
post-exploratory validation
```

and avoid implying a completely untouched confirmatory cohort.

### 20.2 Protocol freeze

Before `evaluate-case-scoping` produces main outer-test predictions, freeze and commit:

- SELENE file identities/checksums;
- paired-population construction;
- 19-indicator primary schema;
- package grouping key;
- five outer folds and inner calibration groups;
- fold-balance audit;
- feature allowlist;
- logistic model contract;
- probability clipping and fallback rules;
- global-prevalence, persistence, activity-volume, and other baseline definitions;
- any optional operating-point thresholds or risk targets used for categorical reporting;
- the rule for any optional abstention sensitivity, if such a sensitivity is retained;
- metric formulas, report-level aggregation, and tie handling;
- fidelity sensitivity definitions;
- broken-pair negative-control permutation count/seed;
- package-cluster bootstrap seed and resample count;
- claim-interpretation and adaptation rules above.

Any later scientific-contract change creates a new protocol identity and cannot silently overwrite the frozen main run.

---

## 21. Scientific outputs

Every numerical chapter result must have a machine-readable parent.

Minimum promoted evidence:

1. dataset/provenance table;
2. paired-population selection audit;
3. symmetric paired-portability table (`n00/n01/n10/n11`, disagreement, Jaccard, prevalence difference, directional recurrence);
4. probability-quality comparison table including global prevalence, persistence, and CASE;
5. calibration table/plot from OOF predictions;
6. risk-coverage figure for each direction with AUGRC and ordinary AURC;
7. evidence-scoping table at the declared coverage/risk operating points;
8. APK/report-level scoping table;
9. per-indicator and fidelity robustness figure/table;
10. broken-pair negative-control summary;
11. claim-support summary with `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, or `INSUFFICIENT_EVIDENCE`.

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

Implement always-generalize, direction-global prevalence, persistence, activity-volume, pooled logistic, per-indicator logistic, symmetric portability metrics, proper scores, recurrence/non-recurrence ranking metrics, selective-risk metrics, report-level aggregation, tie handling, and package bootstrap.

**Completion condition:** hand-computed fixtures, probability-fallback tests, leakage tests, report-aggregation tests, AUGRC/AURC fixtures, and row-permutation tests pass.

### Phase 4 — Exploratory reproduction

Reproduce the existing FedIEC R5 baseline numbers within explained tolerance.

**Completion condition:** differences are reconciled. If a historical result was wrong, preserve that fact and update the starting expectation rather than forcing reproduction.

### Phase 5 — Freeze the post-exploratory evaluation protocol

Persist the outer folds, calibration groups, source-feature contract, model/baseline definitions, metric definitions, and any operating points that will be shown.

**Completion condition:** the pre-frozen-evaluation checklist is complete and the protocol no longer depends on unseen outer-test outcomes.

### Phase 6 — Main CASE evaluation

Run `characterize-paired-portability`, `evaluate-case-scoping`, `stress-indicator-direction-and-fidelity`, and `broken-pair-negative-control`.

**Completion condition:** all OOF predictions, paired-portability outputs, metrics, uncertainty intervals, report-level scoping decisions, fidelity sensitivities, and negative-control outputs validate.

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

## 23. Final pre-frozen-evaluation checklist

The main protocol-frozen OOF run must not begin until every item is true:

- [ ] SELENE source revision and local checksums recorded.
- [ ] Dataset license/citation requirements recorded.
- [ ] Exact paired population reproduced.
- [ ] Paired-vs-unpaired selection audit completed.
- [ ] Symmetric paired-portability formulas validated.
- [ ] All 19 primary indicators frozen.
- [ ] Any broad-only sensitivity subset defined from schema semantics only.
- [ ] Fidelity mappings/sensitivity definitions frozen independently of recurrence outcomes.
- [ ] Package grouping validated with zero cross-partition leakage.
- [ ] Five outer folds persisted; each package is test exactly once.
- [ ] Fold-balance audit generated without using target recurrence labels to alter folds.
- [ ] Inner calibration groups persisted.
- [ ] Feature allowlist contains no target-context or identity fields.
- [ ] Primary CASE model contract frozen.
- [ ] Direction-global prevalence, persistence, activity-volume, and secondary baselines frozen.
- [ ] Fair fit/calibration/test data-budget contract verified for every learned method.
- [ ] `support gating` verified to mean estimability only and incapable of removing primary pooled claims.
- [ ] Probability clipping and zero-support fallback rules frozen and tested.
- [ ] Any categorical operating points to be reported are defined from calibration evidence only.
- [ ] Any optional uncertainty/abstention sensitivity is predeclared separately from the core two-scope policy.
- [ ] Brier, Brier skill, log loss, AUGRC, ordinary AURC, coverage/risk, recurrence-retention, recurrence AP, and non-recurrence AP formulas tested.
- [ ] Headline calibration metrics are wired to OOF test predictions, not calibration predictions.
- [ ] Report-level supported fraction, report risk, report failure incidence, and report retention formulas tested.
- [ ] Tie handling verified under row permutation.
- [ ] Package-cluster bootstrap implementation verified on known fixtures and documented as conditional on frozen OOF fits.
- [ ] Broken-pair negative-control permutation seed/count frozen and implementation validated.
- [ ] Undefined-metric rules tested.
- [ ] Claim interpretation rules frozen; effect strength may change claim strength but not metric definitions.
- [ ] Existing exploratory results clearly separated from the protocol-frozen evaluation.
- [ ] Main manuscript terminology does not imply an untouched external confirmatory cohort.
- [ ] Claim C cannot survive solely because the framework is methodologically careful if persistence is not improved.
- [ ] No FL/IoT, malware-truth, OS-causal, universal-portability, or analyst-benefit claim appears in the planned outputs.

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
- report-level aggregation;
- fidelity sensitivity and negative-control semantics;
- evidence-scoping policy;
- claim boundaries and adaptation rules.

If implementation reveals that a scientific contract is infeasible or incorrect, update this roadmap explicitly before changing the scientific behavior of the code.
