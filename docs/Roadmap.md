# CASE-Android Research Roadmap

**Project:** CASE-Android  
**Acronym:** Context-Aware Scoping of Evidence in Android  
**Full title:** *CASE-Android: Reliability-Qualified Scoping of Recorded Android Behavioral-Security Evidence Across Execution Contexts*  
**Role:** Authoritative scientific roadmap for the CASE-Android project  
**Companion document:** [`technical_doc.md`](technical_doc.md) defines implementation and engineering contracts.

---

## 1. Research statement

Dynamic Android analysis reports describe behavior that was **recorded in a finite execution context**. The same APK may yield different recorded evidence under another context because platform version, execution substrate, stimulation, observation duration, instrumentation, lifecycle state, and ordinary execution stochasticity can all affect what is observed.

CASE-Android studies the operational problem that follows from this fact:

> **Given behavioral-security evidence recorded for an APK in a source context, how reliably should that evidence be carried into a named target context that has not yet been observed?**

The project does **not** infer complete application capability and does not treat a source non-observation as proof of target absence. Its primary predictive estimand remains **source-positive recorded-evidence recurrence**. A separate secondary descriptive estimand captures **target-recorded emergence** when evidence was not recorded in the source context.

The intended contribution is a lightweight, claim-level reliability and reporting layer:

```text
recorded source-context evidence
        ↓
source claim + source-only evidence properties
        ↓
cross-context recurrence score
        ↓
probability-quality / calibration analysis
        ↓
calibration-only operating policy
        ↓
report scope
┌───────────────────────────────┐
│ cross-context-supported       │
│ source-context-only           │
└───────────────────────────────┘
```

The primary semantic study uses SELENE's Android 10/API29 and Android 14/API34 paired observations. A second dataset may support a **separate context-family replication** when identity, feature semantics, licensing, grouping, and leakage gates pass. The current audited secondary candidate is KronoDroid's paired emulator/device syscall profiles; those syscall-presence claims are never pooled with SELENE semantic indicators as if they were the same ontology.

CASE-Android is therefore a **recorded-evidence portability and report-scoping contribution**, not a malware classifier, behavior-truth oracle, causal Android-version study, or deep-learning architecture.

### Research-development principle

CASE-Android follows an evidence-first development process. Pre-implementation feasibility, dataset, and novelty audits are used to decide which scientific lanes belong in the roadmap and which remain gated extensions. The roadmap itself is prospective: it specifies what must be tested, how it must be tested, and what evidence is required for each claim; it does not embed discovery-stage outcomes.

When new evidence exposes a weaker effect, asymmetric result, dataset limitation, or narrower construct than expected, the default response is:

```text
audit the issue
→ preserve methodological validity
→ repair the protocol only when scientifically justified
→ narrow or reformulate the affected claim
→ retain the strongest defensible version
```

The project should stop or fundamentally re-scope only for a **structural validity failure** such as unrecoverable leakage, invalid identity/pairing, incompatible claim semantics, unusable provenance/licensing, or a direct novelty collision that removes the contribution itself. A modest predictive effect is not a structural failure.

## 2. Why this is worth studying

Prior Android work already establishes that dynamic observations can vary across devices, emulators, runtime conditions, versions, and repeated executions. CASE-Android therefore does **not** claim discovery of context sensitivity.

The residual problem is narrower and operational:

> when a security report contains an observation from one context, should that individual claim be generalized to another named context, or remain explicitly source-context-specific?

A conservative source/target intersection can avoid some over-generalization but is not prospective because it requires seeing the target report. Always-generalize preserves coverage but silently assumes portability. Per-indicator persistence is a strong prospective baseline whenever recurrence is common.

CASE-Android therefore tests whether **source-only evidence about the APK and the observed claim** can improve recurrence estimation beyond those simple priors, and whether that improvement translates into a better **coverage-versus-non-recurrence** reporting trade-off under a calibration-only operating policy.

The novelty target is specific:

> **Estimate recurrence of an individual recorded source claim in a named unobserved target context, then use that estimate to scope report language and quantify the associated coverage/non-recurrence trade-off.**

The project does not need to invent a new classifier family to be useful. Its added value must come from the estimand, leakage-controlled evidence transfer, source-evidence ablations, calibrated/scoped reporting, negative controls, report-level reconstruction, and bounded external replication.

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

- Exact paired SELENE Android 10/API29 and Android 14/API34 recorded observations.
- Source-positive semantic claim recurrence.
- Symmetric paired evidence transitions: stable-absent, target-recorded-emergent, source-only, and stable-present.
- Target-recorded emergence as a **separate descriptive estimand** over source-negative observations.
- Source-only recurrence scoring.
- The 19 released Boolean indicators as the primary semantic claim ontology.
- Source-side evidence-strength/count/activity features as a secondary representation ladder.
- Raw-count versus duration-normalized evidence-strength sensitivity.
- Broad/non-derived indicator sensitivity defined from schema semantics before frozen test evaluation.
- Selective reporting and claim scoping with calibration-only operating-point selection.
- Probability quality, calibration, coverage-versus-non-recurrence, recurrence retention, and APK/report-level offline proxy metrics.
- Direction-, indicator-, package-, report-, and fidelity-related heterogeneity.
- Paired-population selection audit and execution-duration exposure audit.
- Broken-pair and other leakage/shortcut negative controls.
- A separate KronoDroid emulator/device syscall-presence replication after its remaining schema/grouping gates pass.
- Reproducible offline analysis of released datasets and traces.

### Gated extensions, not core claims

These may enter only after their explicit validity gates pass:

- AndroCT method/class/package/API granularity analysis.
- DYNAMISM repeated-run analysis for same-context stochasticity.
- CIC-InvesAndMal2019 install/pre-reboot/post-reboot transitions.
- formal finite-sample risk guarantees;
- chronological portability drift;
- future-period generalization;
- malware-family OOD;
- unseen-claim OOD;
- multi-hop or worst-context portability.

### Explicitly out of scope

- Malware classification or malware-family attribution as a CASE target.
- Proving that an APK can or cannot perform a behavior.
- Treating source non-observation as proof of target absence.
- Saying that a behavior itself “emerged” merely because it was newly recorded.
- Causal attribution to Android OS version, emulator/device status, or any single context component.
- Universal Android portability.
- Fresh APK execution campaigns.
- New emulator/device capture campaigns as a project dependency.
- Purchasing or manually operating physical devices.
- User recruitment or field deployment.
- Real-world analyst productivity or security benefit unless separately measured.
- Formal distribution-free risk guarantees without a dependence/shift-valid method.
- Federated-learning or IoT performance claims.
- Deep learning or complex model tournaments merely to increase novelty.

## 5. Pre-implementation design basis

This roadmap is informed by a separate feasibility, dataset, novelty, and claim/gate audit. Those materials are **not part of the scientific result set**. Their role is only to identify feasible additions, remove weak or collision-prone ideas, and define the prospective protocol below.

The roadmap therefore adopts the following design decisions without importing discovery-stage outcome values:

### 5.1 Primary semantic dataset

SELENE / ARTEMIS is the primary dataset because it provides:

- two named Android execution contexts;
- exact APK identity suitable for paired analysis;
- package identity suitable for grouped evaluation;
- a compact semantic `run_features` representation;
- the released Boolean indicator ontology used for claim-level recurrence;
- source-side evidence counts/activity/timing fields that can support a secondary representation ladder;
- fidelity/provenance material suitable for limited parser and extraction diagnostics.

The primary study remains bounded to **recorded observations in the tested named contexts**. It does not interpret non-observation as behavior absence or attribute differences causally to Android version alone.

### 5.2 Secondary context-family replication

KronoDroid is retained as the preferred **gated secondary replication dataset** because it exposes paired emulator/device dynamic evidence at the syscall level and can support a separate source-positive recurrence construct.

It is not pooled with SELENE. Before model-level use, it must pass its own access/provenance, identity, schema-comparability, grouping, leakage, and baseline-fairness gates. Malware-family or temporal claims remain excluded unless their metadata semantics are independently validated.

### 5.3 Gated optional datasets

The following remain optional extensions rather than dependencies of the core project:

- **AndroCT** for evidence-abstraction/granularity studies after access and exact-pair validation;
- **DYNAMISM 2016–2023** for same-context repeated-run stochasticity after lawful access and comparable-unit validation;
- **CIC-InvesAndMal2019** for lifecycle/reboot transitions after exact cross-stage identity and feature comparability are proven;
- **TraceDroid** or other historical-profile datasets only for separately validated cohort questions.

### 5.4 Design consequences carried into the roadmap

The main protocol must therefore include:

- a four-state paired evidence characterization in addition to directional recurrence;
- target-recorded emergence as a **separate descriptive estimand**;
- a primary Boolean CASE scorer and a secondary source-evidence-strength representation ladder;
- raw-count and exposure-normalized source-feature sensitivities;
- explicit paired-population and observation-exposure audits;
- schema-defined broad/non-derived indicator sensitivity;
- broken-pair negative controls;
- package-grouped fit/calibration/test separation;
- report-level offline scoping metrics;
- external model-level replication before broad multi-context framework claims;
- validity gates and claim-promotion gates kept separate.

No numerical discovery-stage result is a success criterion for the future implementation. The frozen evaluation decides claim strength.

## 6. Operational scenario and estimands

CASE-Android only has operational value if its transfer decision is made **before the target context is observed**.

For source context `s`, target context `t`, APK `a`, and claim/indicator `j`:

- `x[a,j,s] = 1` means the evidence was recorded in the source context;
- `x[a,j,t] = 1` means the corresponding evidence was recorded in the paired target context.

### 6.1 Primary predictive estimand — source-positive recurrence

A primary CASE claim exists only when:

\[
x_{a,j,s}=1.
\]

The target outcome is:

\[
y_{a,j}^{s\rightarrow t}=x_{a,j,t}.
\]

CASE estimates:

\[
\hat p_{a,j}^{s\rightarrow t}
=
P\!\left(
y_{a,j}^{s\rightarrow t}=1
\mid X_a^s,\;j
\right),
\]

where `X_a^s` contains **source-context information only**.

The primary decision unit is:

> **one source-positive APK × claim in one declared source→target direction.**

The primary population is the audited exact-pair population for the relevant dataset/context pair.

### 6.2 Secondary descriptive estimand — target-recorded emergence

For source-negative cells:

\[
x_{a,j,s}=0,
\]

report:

\[
E_j^{s\rightarrow t}
=
P(x_{a,j,t}=1 \mid x_{a,j,s}=0).
\]

This quantity is called **target-recorded emergence** or **target-recorded evidence among source-negative observations**.

It must never be described as proof that the underlying behavior newly appeared, because source non-observation can arise from finite stimulation, observation exposure, instrumentation, parser behavior, or execution stochasticity.

A predictive emergence model is **not** part of the current core roadmap.

### 6.3 Symmetric paired-state estimand

For each claim type, characterize:

```text
n00 = source absent, target absent
n01 = source absent, target present
n10 = source present, target absent
n11 = source present, target present
```

These states support disagreement, overlap, directional recurrence, and target-recorded-emergence summaries without forcing a causal interpretation.

### 6.4 Prospective baseline consequence

Any rule that inspects target evidence before deciding whether the source claim is portable is **not** a deployable CASE baseline.

Strict source/target intersection may be shown retrospectively, but it is not a fair prospective competitor.

## 7. Research questions

### RQ1 — Recorded portability structure

**How often do paired source and target contexts agree, disagree, or contain target-recorded evidence that was not recorded in the source context?**

This includes directional source-positive recurrence and the full `n00/n01/n10/n11` paired structure. It characterizes finite recorded evidence, not behavior truth or causal Android-version effects.

### RQ2 — Source-only recurrence signal

**Do source Boolean indicators and source-run evidence properties estimate target recurrence better than direction-global prevalence, per-indicator persistence, and simple activity/evidence-strength baselines under package-held-out evaluation?**

The primary comparison uses proper probabilistic scores.

### RQ3 — Scoping value

**Does a calibration-only CASE policy reduce target non-recurrence among transferred claims while retaining useful claim and report coverage compared with persistence-based scoping?**

This is the primary operational question. It must be answered only by the protocol-frozen calibration/test evaluation defined below.

### RQ4 — Boundaries and replication

**How stable are recurrence and scoping effects across direction, indicator, package/report aggregation, broad-versus-derived definitions, fidelity/exposure sensitivities, negative controls, and one independently paired context family?**

SELENE supplies the primary semantic analysis. KronoDroid supplies the audited secondary context family when its model-level gates pass.

### 7.1 RQ-to-evidence map

| RQ | Main population / unit | Main comparison | Primary evidence | Permitted interpretation |
|---|---|---|---|---|
| RQ1 | exact paired APKs; source-positive and source-negative claim cells | descriptive paired structure | `n00/n01/n10/n11`, directional recurrence, target-recorded emergence, disagreement, Jaccard, prevalence difference | recorded evidence portability is heterogeneous in tested contexts |
| RQ2 | package-held-out source-positive claims | CASE vs global prevalence, persistence, activity, evidence-strength | Brier, log loss, Brier skill, calibration, package-bootstrap deltas | source-only evidence carries incremental recurrence information |
| RQ3 | untouched OOF claims and reconstructed APK reports | calibration-only CASE policy vs persistence / always-generalize | risk-coverage, AUGRC/AURC, risk at coverage, coverage at risk, recurrence retention, report metrics | CASE changes the selective evidence-transfer trade-off |
| RQ4 | direction/indicator/report/fidelity/exposure strata plus gated external dataset | predeclared sensitivity and replication | broad-only, duration normalization, broken-pair control, paired-selection audit, external paired recurrence/model replication | identifies boundaries, robustness, and degree of generalizability |

Granularity, temporal drift, family OOD, claim OOD, and repeated-run stochasticity remain **named extension questions**, not core RQs, until their validity gates pass.

## 8. Dataset and provenance contract

### 8.1 Primary dataset — SELENE / ARTEMIS

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

The primary implementation requires the audited compact families:

- `analyses`;
- `run_features`;
- `fidelity_oracle`;
- `fidelity_evidence`.

The current primary study does not require the multi-gigabyte L0.5/L1/lifecycle layers.

### 8.2 SELENE identity and join rules

- APK identity: exact SHA-256.
- Run identity: released SELENE run identifier.
- Train/calibration/test grouping identity: `package_name`.
- Paired context record: exact APK SHA-256 present in both audited contexts.
- Claims are constructed only after one-to-one pair validation.
- Package/hash/run identifiers are grouping/provenance variables, never predictors.
- The paired population is the explicit inferential population; unpaired observations are used for selection-bias auditing only.

### 8.3 SELENE predictor families

Primary Boolean source representation:

- the frozen 19 source indicators;
- one-hot claim identity.

Secondary predeclared source-side representation ladder may use audited `run_features` fields that pass provenance/leakage review, including:

- semantic/event counts;
- total activity/event volume;
- source duration and predeclared exposure-normalized count transforms;
- other source-only evidence-strength fields explicitly allowlisted before frozen evaluation.

Derived triage/richness scores, raw sensitive strings, identifiers, target fields, labels, and post-target metadata are excluded unless a later roadmap revision proves a distinct valid role.

### 8.4 SELENE license, citation, and sensitive content

Before protocol freeze, reconcile the live SELENE Paper Artifacts Data License and upstream ARTEMIS Dynamic Traces license/citation requirements. CASE-Android's own repository license applies only to original CASE code/material.

The released artifacts may contain malware-controlled endpoints, paths, identifiers, and credential-shaped strings. Raw sensitive strings must not be echoed into logs, tables, figures, or public result artifacts.

### 8.5 Secondary replication dataset — KronoDroid

KronoDroid is a **separate secondary dataset**, not a pooled extension of SELENE.

Audited contract:

- pair on exact unique SHA-256;
- exclude duplicate/conflicting hash identities from the one-to-one paired population;
- use the 288 aligned syscall-count columns plus `nr_syscalls` only after schema reconciliation;
- define a syscall-presence claim as `count > 0` for descriptive recurrence;
- never reinterpret syscall-presence claims as SELENE semantic security indicators;
- malware/benign labels may be used only for valid descriptive strata, never predictors;
- family labels are currently unusable for family-OOD because paired labels disagree extensively;
- APK metadata dates are not execution timestamps and cannot support portability-drift claims.

Before a **model-level** KronoDroid replication is promoted, the workflow must additionally resolve:

1. the 484-column CSV versus public feature-count discrepancy;
2. the source feature allowlist;
3. a valid grouping key and split contract;
4. baseline fairness;
5. leakage tests;
6. licensing/citation provenance.

### 8.6 Gated optional datasets

AndroCT, DYNAMISM 2016–2023, CIC-InvesAndMal2019, TraceDroid, and any newly discovered dataset enter only through the validity gates in Section 22. They are not silently substituted for missing primary evidence.

No fresh physical-device or emulator execution campaign is required by this roadmap.

## 9. Population, redundancy, and exposure audits

These audits are **prospective controls**. They define limitations and sensitivities before claim promotion; they are not performance gates.

### 9.1 Paired-population selection audit

The paired population may differ from source-context observations that do not have a valid target pair. Before the frozen evaluation:

- compare paired versus unpaired source-context indicator prevalence where support exists;
- compare source-positive claim-count distributions per APK;
- compare package composition where the released metadata permit it;
- report absolute prevalence differences indicator by indicator;
- state clearly that primary claims apply to the validated paired population;
- do not infer the cause of non-pairing without source metadata that supports it.

The audit characterizes external-validity limits. It does not reweight or redefine the primary paired population unless a separate, predeclared sensitivity is added.

### 9.2 Observation-exposure audit

The named contexts may differ in observation duration or other recorded execution-exposure properties. Before interpreting cross-context differences:

- summarize source and target run-duration distributions;
- identify other source metadata that represent observation exposure and are comparable across contexts;
- retain raw source evidence counts as one secondary representation;
- evaluate a predeclared exposure-normalized count sensitivity;
- avoid causal wording that attributes recurrence differences to Android version or another single context component.

### 9.3 Indicator redundancy audit

The released Boolean ontology may contain duplicate, near-duplicate, or threshold-derived indicators.

The primary analysis retains the full released indicator set for reconciliation and reproducibility, while a **broad/non-derived sensitivity subset** must be defined from source schema semantics before outer-test outcomes are inspected.

The redundancy audit must:

- identify exact duplicates;
- identify deterministic/threshold-derived indicators where provenance supports that relationship;
- document the mapping;
- prohibit target-recurrence-driven indicator removal.

Primary results remain full-ontology results; the subset is a sensitivity only.

### 9.4 Fidelity/provenance audit

Fidelity material is used only to assess parser/provenance behavior where a defensible mapping exists.

The audit must:

- freeze the indicators with an interpretable fidelity mapping;
- report mapping support and agreement descriptively;
- keep fidelity outcomes out of recurrence predictors and target labels;
- avoid treating fidelity material as independent behavior ground truth;
- use limited support to narrow wording rather than silently dropping difficult indicators.

## 10. CASE-Android mechanism

### 10.1 Decision-time information firewall

For a source-positive claim, every CASE scorer may use **source-side information only**.

Primary Boolean scorer:

- frozen 19 source-context Boolean indicators;
- one-hot claim identity;
- separate fitted model per source→target direction.

Secondary rich-source scorer/sensitivities may additionally use predeclared audited source-only fields such as:

- evidence/event counts;
- total source activity volume;
- source duration;
- fixed duration-normalized count transforms.

Forbidden predictors include:

- any target-context flag/count/summary;
- target execution metadata;
- recurrence outcome;
- package name, SHA-256, run ID;
- malware/family labels;
- split/fold identifiers;
- fidelity outcomes;
- raw evidence strings;
- fields whose provenance cannot be shown to exist before target observation.

### 10.2 Model ladder

The roadmap does **not** define novelty through model complexity.

Required prospective methods:

1. direction-global prevalence;
2. per-indicator persistence;
3. source activity-volume baseline;
4. **Boolean CASE:** direction-specific pooled L2 logistic using claim identity + 19 source flags;
5. **evidence-strength comparator:** claim identity + predeclared source count/strength features;
6. **rich CASE sensitivity:** Boolean + approved count/activity fields;
7. **duration-normalized rich sensitivity**;
8. secondary per-indicator logistic when estimable.

Primary scientific scorer:

> **direction-specific pooled L2 logistic with claim identity and the source Boolean vector.**

Default contract:

```text
penalty = L2
C = 1.0
max_iter = 1000
class_weight = None
```

The richer source representation is a **secondary incremental-value test**. It is evaluated because the available source schema makes the hypothesis feasible, not because it is entitled to outperform the Boolean primary model.

One nonlinear tabular ceiling comparator may be added later only if the frozen simple ladder leaves a scientifically important unresolved question. Random-forest/boosting/GAM/MLP/sequence tournaments are not part of the core protocol.

### 10.3 Report-scope policy

The scientific output is the continuous recurrence probability.

The core readable statuses are:

- **`cross-context-supported`** — threshold selected from calibration data supports carrying the recorded source claim into the named target context under that operating policy;
- **`source-context-only`** — do not generalize the recorded source evidence under that policy.

`source-context-only` never means `target-absent`.

An optional third defer/abstention state is a separately predeclared sensitivity only.

### 10.4 Calibration-only operating points

The full probability-quality and risk-coverage analysis is primary.

Retain the exploratory 50% and 80% coverage views as predeclared descriptive operating views. Optionally evaluate recurrence-risk targets such as 5% or 10% when the calibration partition supports them.

For each outer fold:

1. fit recurrence models on fit groups only;
2. estimate persistence/global priors on fit groups only;
3. choose any threshold/risk operating point from calibration groups only;
4. freeze the threshold;
5. score untouched outer-test groups;
6. if a requested calibration risk target is unavailable, return `NO_OPERATING_POINT`.

Do not relax a target after seeing outer-test outcomes.

Formal conformal/LTT/CRC guarantee language is excluded from the core until G13 passes.

### 10.5 Sparse support

All 19 indicators stay visible in the primary pooled population.

Sparse support may make a secondary per-indicator model or stratum metric `NA`, but it may not remove primary claims because test outcomes are inconvenient.

Every `NA` must carry a machine-readable reason and denominator.

### 10.6 Probability stability

- Store raw model probability separately from any metric-specific stabilized probability.
- Clip only for log-loss evaluation, to `[1e-6, 1 - 1e-6]`.
- Brier/ranking/selective metrics use raw probabilities.
- If a fit partition contains no source-positive examples for an indicator-specific persistence estimate, fall back to direction-global fit prevalence and record the fallback.
- Do not silently fall back for per-indicator logistic models; mark them `NA`.

### 10.7 Evidence interpretation rule

- broad, stable improvement → bounded CASE benefit;
- modest but repeated improvement → modest incremental signal;
- directional or stratum-specific effect → explicitly conditional claim;
- persistence parity/superiority → predictive/scoping superiority claim is not supported;
- failed negative control → stop interpretation and investigate;
- structural data/provenance/leakage failure → affected lane is blocked;
- weaker effect never justifies changing metrics or thresholds post hoc.

## 11. Baselines, ablations, and retrospective references

### 11.1 Prospective baselines

**Always-generalize**  
Every source-positive claim is carried to the named target context. This defines full-coverage observed non-recurrence risk.

**Direction-global prevalence**  
Assign the fit-partition recurrence prevalence for that direction to every source-positive claim.

**Per-indicator persistence**  
Assign the fit-partition recurrence prevalence of that claim type. This remains the **principal simple baseline**.

**Activity-volume baseline**  
Use claim identity plus only the source report's total positive-flag/activity summary defined in the frozen contract. This tests whether CASE merely learns that “busy” reports recur more.

**Evidence-strength-only baseline**  
Use claim identity plus predeclared source evidence/count-strength fields without the full Boolean context. This tests whether richer CASE is simply a count proxy.

### 11.2 CASE methods

**Boolean CASE**  
Claim identity + 19 source Boolean flags. This is the primary method.

**Rich CASE sensitivity**  
Boolean CASE plus predeclared source count/activity fields.

**Duration-normalized rich sensitivity**  
Same conceptual feature family but with the frozen normalization transform.

**Per-indicator logistic**  
Secondary comparator for whether claim-specific weights materially help.

### 11.3 Fair data-budget contract

Every learned method uses the same fold-local label budget:

- fit groups may fit models or recurrence priors;
- calibration groups may select operating thresholds and run support diagnostics, but target outcomes there do not refit recurrence models or persistence estimates;
- outer-test groups are evaluation only;
- feature definitions and transformations are frozen before outer-test inspection;
- all methods are compared on identical eligible outer-test claim rows.

### 11.4 Retrospective descriptive reference

Strict source/target intersection requires the target report and is therefore not a prospective CASE baseline.

It may appear only as a descriptive upper-conservatism reference after clearly labeling its target access.

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
- source-negative claim-cell count for the emergence estimand;
- per-indicator source-positive and source-negative support;
- source-context positive-flag-count distribution.

The audit is descriptive only. Once the target-label-blind fold manifest is frozen, it must not be regenerated merely because a later outer-test stratum looks inconvenient.

### 12.2 Inner calibration

Within each outer-training partition, reserve **20% of the outer-training package groups** as a deterministic calibration subset using one fixed calibration seed plus the outer-fold identity. Models fit only the remaining fit groups. Calibration groups are used for:

- method-specific risk-budget threshold selection for CASE and persistence-based policies;
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
- **target-recorded emergence** `n01 / (n00 + n01)` for Android10→14 and `n10 / (n00 + n10)` for Android14→10, when defined;
- both directional source-positive recurrence rates shown side by side.

Target-recorded emergence is always reported with its source-negative denominator and is never interpreted as proof that the underlying behavior newly began.

These symmetric summaries prevent directional conditioning from being mistaken for a direct OS effect.

### 13.2 Primary probabilistic metrics

**Brier score**  
Primary proper scoring rule for recurrence probability quality.

\[
BS = \frac{1}{N}\sum_i (\hat p_i-y_i)^2.
\]

Report paired differences for CASE against both direction-global prevalence and per-indicator persistence; negative is better.

**Brier Skill Score versus persistence**  
Secondary effect-size companion:

\[
BSS_{persist}=1-\frac{BS_{CASE}}{BS_{persistence}}.
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
- **risk difference** versus persistence at the same predeclared/fractionally handled coverage;
- **coverage difference** versus persistence for the same **calibration-derived risk target**, with each method's threshold selected only on calibration data;
- package-macro versions of the same measures where meaningful.

Do not search the outer-test risk curves to choose a threshold that retrospectively matches a desired risk. Outer-test curves may be shown descriptively, but policy comparisons at a risk target use calibration-selected thresholds only.

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

The following experiments define the prospective evidence plan.

### `validate-selene-contract`

**Purpose:** verify SELENE files, licenses/citations, schemas, checksums, identities, paired population, package groups, predictor provenance, and indicator redundancy.  
**Outputs:** dataset manifest, checksum manifest, join/duplicate audit, paired/unpaired counts, indicator inventory, source-feature allowlist, redundancy map, fidelity warning.  
**Completion:** G0–G5 are not failed for the primary dataset.

### `audit-paired-population-and-exposure`

**Purpose:** quantify paired-population selection and context exposure differences before model interpretation.  
**Outputs:** paired-vs-unpaired prevalence differences, claim/activity distributions, package summaries, context duration/exposure summaries.  
**Interpretation:** defines external-validity and exposure limitations; no performance gate.

### `characterize-paired-portability`

**Purpose:** answer RQ1 before predictive modeling.  
**Outputs:** per-indicator `n00/n01/n10/n11`, both directional recurrence rates, target-recorded emergence, disagreement, Jaccard, paired prevalence difference, support counts, package-cluster intervals.  
**Interpretation:** recorded-evidence structure only.

### `reproduce-exploratory-baselines`

**Purpose:** verify that the implementation can reproduce the previously used baseline/model contracts before the protocol-frozen evaluation.  
**Methods:** direction-global prevalence, persistence, activity-volume, Boolean CASE, evidence-strength variants, and the broken-pair diagnostic under a separately identified exploratory configuration.  
**Outputs:** reproducibility/reconciliation artifact with inputs, split identity, method contract, and discrepancies.  
**Rule:** exploratory outputs are never merged with or used to tune the frozen outer-test evaluation.

### `evaluate-case-probability`

**Purpose:** answer RQ2 under the frozen five-fold OOF protocol.  
**Methods:** global prevalence, persistence, activity-volume, evidence-strength-only, Boolean CASE, rich-source sensitivity, exposure-normalized sensitivity, secondary per-indicator logistic.  
**Primary metrics:** Brier, log loss, paired Brier/log-loss differences versus persistence.  
**Secondary:** Brier skill, calibration, recurrence/non-recurrence AP.  
**Outputs:** untouched OOF probabilities and package-bootstrap comparisons.

### `evaluate-case-scoping`

**Purpose:** answer RQ3 using strict fit/calibration/test separation.  
**Methods:** persistence and CASE operating policies, with always-generalize as a full-coverage reference.  
**Outputs:** calibration-selected thresholds, untouched-test risk/coverage, AUGRC/AURC, recurrence retention, matched-coverage/matched-risk comparisons, scope assignments, report-level metrics.  
**Rule:** no threshold is chosen from outer-test outcomes.

### `stress-case-boundaries`

**Purpose:** answer the SELENE portion of RQ4.  
**Analyses:** direction, indicator macro/worst, package/report macro, broad/non-derived sensitivity, raw-vs-normalized count sensitivity, paired-selection audit, duration/exposure summaries, fidelity diagnostics, split sensitivity, and predeclared missing/noise sensitivities where justified.  
**Rule:** sensitivities qualify claims; they do not redefine the primary population post hoc.

### `broken-pair-negative-control`

**Purpose:** test whether CASE benefit depends on genuine source-target identity.  
**Protocol:** within each frozen test fold/direction, permute complete target APK evidence vectors across APKs using a predeclared set of seeds, preserving marginal target distributions while destroying source-target identity.  
**Expected diagnostic contract:** genuine-pair signal should not survive as a stable substantial CASE advantage after identity correspondence is destroyed.  
**Failure:** a persistent substantial advantage blocks G9 and requires leakage/shortcut investigation.

### `validate-kronodroid-contract`

**Purpose:** validate the secondary dataset before any model-level replication.  
**Required:** exact unique identity pairing, duplicate policy, aligned dynamic schema, documentation reconciliation, license/citation provenance, source feature allowlist, and valid grouping key.  
**Failure:** KronoDroid remains descriptive or is excluded.

### `characterize-kronodroid-portability`

**Purpose:** provide a separate external context-family descriptive characterization.  
**Unit:** exact paired APK × syscall-presence claim.  
**Outputs:** four-state transitions, both directional recurrence, support-aware syscall summaries, valid descriptive strata, and broken-pair control.  
**Interpretation:** syscall recorded-evidence recurrence only; do not merge it with SELENE semantic claims.

### `evaluate-kronodroid-scoping`

**Purpose:** test whether the CASE **source-only recurrence/scoping formulation**, rather than merely context instability, replicates in a second context family.  
**Status:** gated secondary experiment. Run only after G0–G9 and the KronoDroid grouping/source-feature contracts pass.  
**Methods:** simple fit-only prevalence/persistence baselines plus one source-only pooled logistic formulation appropriate to the frozen syscall claim ontology.  
**Claim role:** required before broad multi-context/framework-level replication language; not required for a bounded SELENE-only claim.

AndroCT, DYNAMISM, CIC, temporal OOD, family OOD, claim OOD, and formal risk-control experiments remain gated extensions rather than hidden mandatory work.

## 17. Claim-to-evidence contract

Use:

```text
SUPPORTED
PARTIALLY_SUPPORTED
NOT_SUPPORTED
INSUFFICIENT_EVIDENCE
```

A weak scientific effect narrows the affected claim. A structural validity failure blocks it. Methodological care alone cannot rescue a null predictive/scoping result.

### Claim A — recorded portability heterogeneity

> Recorded Android security evidence exhibits heterogeneous recurrence/disagreement across the tested named contexts.

**Required evidence:** paired four-state tables, directional recurrence, per-indicator support/uncertainty, disagreement/overlap, and valid paired-context semantics.  
**Promotion rule:** promote only to the breadth supported across indicators/directions.  
**Boundary:** finite processed observations only; no causal context-component claim.

### Claim B — source-only recurrence signal beyond persistence

> Source-side evidence provides incremental information about target recorded recurrence beyond direction-global and per-indicator persistence priors.

**Required evidence:** frozen package-held-out Brier/log-loss comparison, paired uncertainty, calibration diagnostics, and broken-pair integrity.  
**Promotion rule:** `SUPPORTED` only when the frozen comparison consistently improves proper scoring under the declared uncertainty contract; otherwise narrow or reject.

### Claim C — evidence strength adds incremental value

> Source evidence counts/structure add recurrence information beyond Boolean presence and simple activity volume.

**Required evidence:** raw-count, activity, Boolean, rich, and exposure-normalized ablations on identical frozen rows.  
**Role:** secondary. If the increment is absent or unstable, remove this contribution without affecting Claims A/B.

### Claim D — selective CASE scoping improves the trade-off

> A calibration-only CASE policy provides a better non-recurrence-risk/coverage trade-off than persistence-based scoping in at least some predeclared relevant region of the frontier.

**Required evidence:** calibration-only operating-point selection, untouched-test evaluation, full risk-coverage comparison, matched-coverage/matched-risk analysis, recurrence retention, and report reconstruction.  
**Promotion rule:** if no material improvement exists anywhere under the valid protocol, Claim D is `NOT_SUPPORTED`; framework quality cannot rescue it.

### Claim E — formal risk-controlled reporting

> CASE satisfies a formal declared portability-risk guarantee.

**Status:** **GATED / NOT A CORE CLAIM.**  
It may enter only after G13 passes with a method whose dependence and context-shift assumptions are explicitly justified.

### Claim F — evidence granularity versus portability

> Portability changes systematically with evidence abstraction/detail.

**Status:** **GATED EXTENSION.**  
Requires matched abstraction levels, valid claim mapping, and an authorized comparable dataset/layer.

### Claim G — report-level reliability proxy

> CASE scoping reduces unsupported transferred recorded claims at the reconstructed APK-report level while retaining useful report content.

**Required evidence:** calibrated policy, report-macro risk/coverage/failure incidence, persistence comparison, and package/report uncertainty.  
**Boundary:** offline proxy only; no analyst-time or real-world security-benefit claim.

### Claim H — independent context-family replication

> The CASE recurrence/scoping formulation shows useful evidence in more than one independently paired Android execution-context family.

**Required evidence:** model-level external replication with compatible prospective baselines, not merely descriptive context difference.  
**Promotion rule:** broad multi-context framework language is forbidden until G19 and G20 pass.

### Claim I — portability drift

> The evidence-portability relationship changes over actual observation time.

**Status:** **GATED EXTENSION.**  
Requires validated observation timestamps and chronological evaluation.

### Claim J — future-period generalization

> CASE retains useful recurrence/scoping performance on later observation periods.

**Status:** **GATED EXTENSION.**  
Requires verified temporal semantics and a predeclared train-past/test-future protocol.

### Claim K — malware-family OOD

> CASE generalizes to malware families excluded from fitting.

**Status:** **GATED EXTENSION.**  
Requires harmonized family identities and leakage-safe family-grouped evaluation.

### Claim L — unseen-claim OOD

> Contextual source evidence transfers portability signal to evidence kinds excluded from fitting.

**Status:** **GATED EXTENSION.**  
Requires enough independent claim families to define a meaningful holdout.

### Claim M — context-associated versus same-context stochastic instability

> Cross-context evidence instability exceeds ordinary repeated-run instability under comparable evidence units.

**Status:** **GATED DIAGNOSTIC/EXTENSION.**  
Requires lawful access to repeated-run data with comparable claim semantics.

### Claim N — target-recorded emergence

> Evidence not recorded in the source context can still be recorded in the target context at claim-dependent rates.

**Required evidence:** source-negative denominators and four-state paired tables.  
**Role:** descriptive secondary estimand.  
**Boundary:** never say the underlying behavior itself newly emerged.

### Claim O — PhD implication

> Heterogeneous environments motivate reliability-qualified handling of shared security evidence.

**Class:** conceptual motivation only.  
No CASE experiment supports FL/IoT effectiveness.

### 17.1 Claim promotion rule

Claims are promoted only after all relevant validity and claim-promotion gates pass.

- A descriptive claim can survive a null predictive result if its own evidence remains valid.
- Claims B/D cannot survive merely because the framework is methodologically careful if persistence is equally good or better.
- Claim H requires an external **model-level** replication before broad multi-context language.
- E/I/J/K/L/M remain outside the core contribution unless their gates are explicitly opened by valid data and a frozen protocol.
- Any scientific-contract change after freeze creates a new protocol identity.

## 18. Loopholes and threat controls

| Loophole / threat | Why it matters | Required control |
|---|---|---|
| Target leakage | Target context trivializes recurrence | strict source-feature allowlist; target-column poison tests |
| Identity leakage | Hash/package/run fields can memorize recurrence | typed predictor firewall; identity poison tests |
| Calling the frozen SELENE run independent confirmation | discovery already informed model/problem | call it protocol-frozen/post-exploratory OOF evaluation |
| High recurrence inflates AP | weak models can look impressive | Brier/log loss first; prevalence/persistence references; non-recurrence AP |
| Persistence baseline gets more labels | unfair comparison | common fit/calibration/test information budget |
| Test-selected threshold | optimistic policy | calibration-only selection; `NO_OPERATING_POINT` when needed |
| Test-selected indicator subset | post-hoc inflation | all 19 primary; broad/non-derived subset frozen from schema |
| Support gating hides sparse claims | changes population | support controls estimability only; sparse primary claims remain visible |
| Duplicate/derived indicators | apparent 19-way robustness is overstated | explicit redundancy map + broad/non-derived sensitivity |
| Paired-population selection | paired APKs differ from unpaired A10 population | regenerate 3.20 pp macro / 8.72 pp max-style selection audit |
| Unequal observation duration | count/recurrence difference may reflect exposure | report duration; raw vs normalized count sensitivity; no causal version claim |
| Same parser in both contexts | correlated extraction errors may mimic portability | fidelity/provenance sensitivity; no behavior-truth claim |
| Fidelity oracle treated as truth | only 56 shared hashes | diagnostic only |
| Finite Monkey execution | non-observation can be missed trigger | recorded-evidence wording only |
| Direction asymmetry interpreted causally | source-positive conditioning changes denominator | four-state table + both directions |
| Activity/count shortcut | richer model may just learn volume | dedicated activity and evidence-strength baselines |
| Broken pairing still performs | may reveal leakage/marginal shortcut | mandatory multiple broken-pair permutations; block G9 if effect persists |
| Row-order tie bias | changes fixed-coverage results | fractional ties + permutation tests |
| Claim/APK dependence | IID CIs too narrow | package-grouped split + package-cluster bootstrap |
| Bootstrap called full retraining uncertainty | bootstrap conditions on frozen OOF fits | state conditional interpretation; optional split-manifest sensitivity |
| Report-level proxy oversold | offline reconstruction is not analyst utility | report counts/risk only; no time/security-benefit claim |
| Krono syscall unit treated as semantic SELENE claim | invalid ontology pooling | separate dataset/result namespace and wording |
| Krono 484-column schema mismatch ignored | provenance/feature contract may be wrong | resolve before model-level replication |
| Krono family disagreement ignored | invalid family-OOD split | block family OOD until reconciled |
| APK metadata dates treated as execution time | false drift/future claim | G15 blocks temporal claims |
| Broad context instability claimed as novel | well established literature | novelty rests on source-positive recurrence + report scope |
| Formal risk method applied casually | package/report dependence and shift break guarantees | empirical policy unless G13 passes |
| Framework rigor used to rescue null result | methodology ≠ predictive utility | B/D become `NOT_SUPPORTED` when valid baselines are not improved |
| External descriptive replication called model replication | overstates H | H requires source-only model/scoping replication |

## 19. Literature position and novelty boundary

The novelty audit treats several neighboring findings as already established:

- Android behavior can vary across execution contexts.
- emulator/physical-device traces can differ for the same app.
- Android-version/environment differences are known.
- behavior abstraction/granularity is an established analysis technique.
- repeated dynamic executions are not perfectly stable.
- Android malware classifiers can experience temporal drift.
- selective prediction, conformal prediction, Learn-Then-Test, and conformal risk control are general methods rather than CASE inventions.
- reliability-aware Android malware features are an active neighboring area.

Therefore CASE must **not** claim novelty from merely observing instability, using logistic regression, applying selective prediction, or comparing emulator/device behavior.

### 19.1 Residual novelty

The defensible novelty is the intersection of:

1. **claim-level portability estimand** — one recorded source-positive Android evidence claim is the unit whose recurrence in a named still-unobserved target context is estimated;
2. **prospective source-only prediction** — target evidence is unavailable at decision time and simple persistence is treated as a serious baseline;
3. **reliability-qualified report scoping** — recurrence scores determine whether the recorded claim is carried forward or kept source-context-specific;
4. **selective/report-level evaluation** — proper scores, calibration-only operating policies, risk/coverage, recurrence retention, and reconstructed report behavior;
5. **validity diagnostics** — four-state paired structure, paired-selection/exposure audit, redundancy/fidelity sensitivity, broken-pair controls;
6. **bounded context-family replication** — a separate paired dataset may test whether the formulation extends beyond SELENE without pretending the evidence ontologies are identical.

Concise novelty statement:

> **CASE-Android evaluates whether source-context recorded security evidence can support source-only estimates of recurrence in a named unobserved target context and whether those estimates can be used to scope individual report claims with an explicit reliability/coverage trade-off.**

Do not claim “first” unless a final citation-chaining search immediately before submission supports that wording.

### 19.2 Current collision-aware dataset interpretation

**SELENE / ARTEMIS** supplies the primary versioned-emulator semantic evidence and explicitly frames its traces as finite observations.

**AndroCT** and **cross-device consistency studies** directly occupy broad emulator/device behavior-difference claims. If AndroCT is later used, CASE novelty must remain the claim-portability/scoping operation or a rigorously matched granularity analysis.

**KronoDroid** already supports cross-device/time malware research. CASE uses it only as a separate paired syscall evidence dataset; its value is external recurrence/model replication, not discovery that devices differ.

**DYNAMISM** occupies repeated-run stability as a broad phenomenon; a future CASE use would be to compare same-context and cross-context recurrence under matched evidence units.

**Selective/risk-control literature** supplies evaluation/method tools. CASE may use them but does not own their methodology.

### 19.3 Final novelty check

Before submission, search specifically for:

> prediction of recurrence of an individual source-positive Android dynamic-analysis claim into a named unobserved target context, followed by claim-level report scoping based on that prediction.

Also search citation chains around SELENE/ARTEMIS, AndroCT, cross-device consistency, dynamic-analysis repeatability, selective evidence/reporting, and recent Android feature-reliability work.

Search absence is not proof of firstness.

## 20. Pre-implementation audit versus protocol-frozen evaluation

### 20.1 Role of pre-implementation audit material

Pre-implementation feasibility, novelty, and dataset-audit materials exist to decide **what belongs in this roadmap**. They must not be merged into the roadmap's future result set or treated as evidence for the final chapter claims.

Their permitted influence is limited to design choices such as:

- which datasets are primary, secondary, gated, or excluded;
- which estimands are meaningful and feasible;
- which source-feature families deserve a predeclared ablation;
- which baselines and negative controls are mandatory;
- which validity gates must exist;
- which claims require external replication;
- which extension lanes should remain deferred.

The authoritative scientific results begin with the protocol-frozen evaluation and any separately frozen external replication.

### 20.2 Interpretation of the main SELENE frozen run

The main five-fold SELENE evaluation is described as:

```text
protocol-frozen evaluation
locked out-of-fold evaluation
post-exploratory validation
```

It is not described as a completely untouched independent confirmation cohort because earlier feasibility work informed the problem formulation and several design choices. Freezing now prevents **further** outcome-driven changes.

### 20.3 Protocol freeze

Before outer-test predictions are generated, freeze:

- exact SELENE inputs/checksums/licenses;
- paired population and package groups;
- primary claim ontology and broad/non-derived sensitivity;
- source Boolean allowlist;
- evidence-count/activity allowlist;
- exposure-normalization formula;
- model contracts;
- persistence/global/activity/evidence-strength baselines;
- five outer folds and calibration groups;
- support/NA/fallback rules;
- probability metrics/calibration diagnostics;
- selective/report-level metric formulas;
- descriptive coverage points and any calibration-derived risk target;
- tie handling;
- paired-population/exposure/fidelity sensitivities;
- negative-control seeds/count;
- bootstrap seed/count;
- claim/gate interpretation contract.

Any scientific change after this point creates a new protocol identity.

### 20.4 External replication

A bounded SELENE chapter does not require an external model-level replication. However, any claim that CASE generalizes across **different context families** requires a separately frozen secondary-dataset protocol satisfying G19 and G20.

## 21. Scientific outputs

Every manuscript-facing numerical result must have a machine-readable parent.

### 21.1 Primary SELENE evidence

Minimum promoted evidence:

1. dataset/provenance/license table;
2. paired-population selection and run-duration exposure table;
3. indicator redundancy/broad-sensitivity inventory;
4. symmetric four-state portability table (`n00/n01/n10/n11`);
5. directional recurrence and target-recorded-emergence table;
6. probability-quality comparison: global, persistence, activity, evidence-strength, Boolean CASE, rich sensitivity;
7. calibration table/plot from untouched OOF predictions;
8. risk-coverage figure per direction with AUGRC and ordinary AURC;
9. evidence-scoping table at declared calibration-derived or fixed-coverage views;
10. APK/report-level scoping table;
11. per-indicator/package/report and fidelity/exposure robustness outputs;
12. broken-pair negative-control summary;
13. package-bootstrap uncertainty table;
14. claim-support/gate summary.

### 21.2 Secondary KronoDroid evidence

If only the descriptive gates pass:

- dataset/schema/pair manifest;
- four-state syscall-presence recurrence;
- direction-specific recurrence and support;
- broken-pair comparison;
- clearly separated malware/benign descriptive strata if label semantics are valid.

If the model-level gates also pass, additionally promote:

- external source-only baseline/CASE probability comparison;
- external selective-scoping comparison;
- explicit statement of which Claim H language is supported.

### 21.3 Generation rule

Figures/tables are generated from validated structured results. No scientific number is manually copied into reporting code or configuration.

## 22. Validity gates, claim-promotion gates, and implementation phases

CASE uses two distinct gate classes.

- **Validity gates** decide whether a dataset/estimand/evaluation is structurally interpretable.
- **Claim-promotion gates** decide which scientific statements the resulting evidence is allowed to support.

A weak effect normally narrows a claim. A structural validity failure blocks the affected lane.

### 22.1 Gate architecture

| Gate | Purpose | PASS requirement | Failure / partial consequence |
|---|---|---|---|
| **G0 Access/license** | lawful use and citation/provenance | live terms, licenses, and required citations verified | block only the affected dataset/artifact |
| **G1 Identity** | exact pair construction | unique source/target identity and duplicate policy | block paired estimand until repaired |
| **G2 Context semantics** | define what the contrast means | source/target conditions documented and wording bounded | narrow interpretation; no causal component claim |
| **G3 Claim comparability** | same claim meaning across paired sides | identical or explicitly mapped observation rule within a dataset | drop incompatible claims or dataset lane |
| **G4 Provenance** | immutable input→output trace | revisions/checksums/transforms recorded | no promoted evidence until traceable |
| **G5 Leakage** | prospective source-only decision | predictor firewall and poison tests pass | block predictive/scoping claims |
| **G6 Grouping** | no related identity across roles | one frozen valid grouping/split manifest | rebuild before evaluation |
| **G7 Support** | sparse-stratum transparency | counts/denominators predeclared; `NA` is not exclusion | keep sparse strata visible; narrow stratum claims |
| **G8 Baseline fairness** | identical information budget | fit-only priors/models and same evaluation rows | repair comparison before interpretation |
| **G9 Negative-control integrity** | genuine pairing must matter | broken-pair control behaves as a null/shortcut diagnostic | investigate leakage/shortcut before claim promotion |
| **G10 Probability quality** | CASE improves recurrence probability | predeclared proper-score comparison supports the claim | Claim B narrows or becomes not supported |
| **G11 Rich-feature increment** | counts/structure add beyond Boolean/activity | paired incremental comparison survives sensitivities | remove Claim C / keep simpler model |
| **G12 Selective utility** | policy improves risk/coverage | calibration-only policy evaluated on untouched test | Claim D narrows or becomes not supported |
| **G13 Formal risk validity** | formal guarantee wording | dependence/shift-valid method and assumptions | use empirical risk/coverage only |
| **G14 Report-level utility** | policy behaves coherently per APK report | calibrated report metrics vs baseline | keep claim-level only / narrow Claim G |
| **G15 Temporal OOD** | actual future-period portability | validated observation times + chronological split | no temporal-drift/future claim |
| **G16 Family OOD** | unseen-family portability | harmonized family labels + grouped split | no family-OOD claim |
| **G17 Claim OOD** | unseen evidence-kind portability | enough independent claim families | no unseen-claim claim |
| **G18 Fidelity robustness** | parser/provenance sensitivity | predefined interpretable mapping/strata | qualify artifact-level interpretation |
| **G19 Independent dataset replication** | external method replication | same prospective recurrence/scoping formulation on another valid dataset | no external replication claim |
| **G20 Independent context-family replication** | broader than one context type | compatible model-level effect in independent context family | no broad multi-context framework language |
| **G21 Complexity justification** | complex models must earn cost | stable incremental utility over simpler model | keep simpler model |
| **G22 Sensitivity robustness** | result not one fragile slice | predeclared direction/indicator/exposure/redundancy/split sensitivities | narrow claim to stable conditions |
| **G23 Reproducibility** | exact rerun traceability | deterministic CLI/artifacts/provenance | no promoted evidence |
| **G24 Claim promotion** | final wording | all required gates for a claim pass | mark partial/not supported/insufficient |

### 22.2 Gate consequence rules

1. G0–G6 failure blocks the affected dataset/estimand.
2. G7–G12 weakness normally narrows the population/method/claim rather than cancelling CASE.
3. G13 is required **only** for a formal guarantee claim.
4. G15–G20 are extension/generalization gates; they are not prerequisites to a bounded SELENE result.
5. Broad multi-context language requires G19/G20 model-level support.
6. G21 prevents complexity-for-novelty.
7. G24 never allows a claim to be promoted merely because the methodology is rigorous.

### 22.3 Implementation phases

#### Phase 1 — Foundation and provenance

Implement manifests, immutable data access, license/citation recording, schemas, and config.

**Completion:** G0–G5 are not failed for SELENE.

#### Phase 2 — Canonical paired evidence

Implement exact pairing, package grouping, source-positive claims, source-negative cells for emergence, four-state transitions, source feature families, paired/unpaired audit, and exposure audit.

**Completion:** all canonical identities and transformation contracts validate.

#### Phase 3 — Splits, baselines, metrics, and negative controls

Implement five-fold package OOF, calibration groups, global/persistence/activity/evidence-strength baselines, Boolean/rich model ladder, paired metrics, selective/report metrics, broken-pair control, and package bootstrap.

**Completion:** fixtures, leakage, tie, NA, and negative-control implementation tests pass.

#### Phase 4 — Exploratory reproducibility check

Reproduce the separately identified exploratory baseline/model contracts only to validate implementation continuity.

**Completion:** material discrepancies are understood; no exploratory outcome changes the frozen protocol automatically.

#### Phase 5 — Protocol freeze

Persist the full scientific contract before main outer-test inference.

**Completion:** Section 23 checklist passes.

#### Phase 6 — Main SELENE evaluation

Run paired characterization, frozen probability evaluation, calibration-only scoping, boundary sensitivities, and negative controls.

**Completion:** all required structured evidence validates and claims are assigned according to Section 17.

#### Phase 7 — Secondary KronoDroid replication

First resolve G0–G9 for model-level use. Run descriptive portability characterization after its dataset contract passes; run model/scoping replication only after the grouping and source-feature contracts are frozen.

**Completion:** any external-replication claim is assigned according to G19/G20.

#### Phase 8 — Chapter evidence

Promote only validated tables/figures/results needed by supported or partially supported claims.

## 23. Final pre-frozen-evaluation checklist

The main SELENE protocol-frozen OOF run must not begin until every applicable item is true:

### Dataset / provenance

- [ ] SELENE source revision and exact checksums recorded.
- [ ] Live SELENE + ARTEMIS license/citation requirements reconciled.
- [ ] Exact paired population regenerated from the frozen identity/join contract and discrepancies from the source manifest explained.
- [ ] Paired-vs-unpaired selection audit regenerated.
- [ ] Context run-duration/exposure audit regenerated.
- [ ] All 19 primary indicators frozen.
- [ ] Duplicate/derived indicator inventory frozen.
- [ ] Broad/non-derived sensitivity subset frozen from source schema only.
- [ ] Fidelity mapping/sensitivity definition frozen independently of recurrence outcomes.

### Estimands

- [ ] Source-positive recurrence construction validated.
- [ ] Source-negative target-recorded-emergence construction validated.
- [ ] `n00/n01/n10/n11` definitions and direction mapping tested.
- [ ] Non-observation wording cannot be rendered as behavior absence.
- [ ] Report-level aggregation population/denominators frozen.

### Features / models / baselines

- [ ] Boolean source-feature allowlist frozen.
- [ ] Evidence count/activity allowlist frozen.
- [ ] Duration-normalization formula frozen.
- [ ] No target/context-future/identity/label field can enter predictors.
- [ ] Primary pooled L2 logistic contract frozen.
- [ ] Global prevalence, persistence, activity-volume, evidence-strength, Boolean CASE, rich, normalized, and secondary per-indicator contracts frozen.
- [ ] All learned methods obey the same label/information budget.
- [ ] Probability clipping and zero-support fallback rules frozen.

### Splits / policy

- [ ] Package grouping validated with zero cross-role leakage.
- [ ] Five target-label-blind outer folds persisted.
- [ ] Every package is outer-test exactly once.
- [ ] Fold-balance audit generated without refolding from outcomes.
- [ ] Inner calibration groups persisted.
- [ ] Categorical operating points are calibration-only.
- [ ] 50%/80% descriptive views and any risk targets are predeclared.
- [ ] `NO_OPERATING_POINT` behavior tested.
- [ ] No formal guarantee language is enabled unless G13 independently passes.

### Metrics / uncertainty

- [ ] Brier, log loss, Brier skill, calibration intercept/slope, recurrence/non-recurrence AP tested.
- [ ] Four-state, recurrence, emergence, disagreement, Jaccard, prevalence-difference formulas tested.
- [ ] AUGRC and ordinary AURC validated against fixtures/reference.
- [ ] Risk, coverage, recurrence retention, matched-coverage/risk rules tested.
- [ ] Report supported fraction, report non-recurrence, report-any-failure, and report retention tested.
- [ ] Tie handling is invariant to row order.
- [ ] Undefined metrics emit typed `NA` reasons.
- [ ] Package-cluster bootstrap uses frozen package resampling and paired method differences.

### Negative controls / sensitivities

- [ ] Broken-pair permutation count/seeds frozen.
- [ ] Broken-pair implementation permutes complete target APK evidence blocks.
- [ ] Broad/non-derived sensitivity implemented.
- [ ] Raw-versus-duration-normalized count sensitivity implemented.
- [ ] Selection/exposure/fidelity sensitivities wired.
- [ ] Any split-manifest sensitivity is target-label-blind and cannot be used to choose the preferred result.

### Claims / interpretation

- [ ] Pre-implementation/exploratory artifacts remain separate from frozen scientific results.
- [ ] Main manuscript terminology says protocol-frozen/post-exploratory, not untouched external confirmation.
- [ ] Claim B fails/narrows if persistence is not improved.
- [ ] Claim D fails/narrows if calibrated selective utility does not improve.
- [ ] Claim E remains absent unless G13 passes.
- [ ] Claim N uses “target-recorded emergence,” never behavior emergence.
- [ ] No OS-causal, behavior-truth, universal-portability, analyst-benefit, FL, or IoT empirical claim appears.

### External replication

These do not block the bounded SELENE run, but must be satisfied before a Krono model-level replication:

- [ ] KronoDroid exact dataset revision/checksums recorded.
- [ ] Clean unique-pair logic regenerated from the frozen KronoDroid identity/duplicate contract.
- [ ] Current artifact schema reconciled with the public/documented schema before model-level use.
- [ ] Valid Krono grouping key and split contract frozen.
- [ ] Krono source-feature allowlist and baselines frozen.
- [ ] Family labels excluded from OOD claims unless reconciled.
- [ ] APK metadata dates excluded from temporal claims unless execution semantics are proven.
- [ ] SELENE and Krono claim ontologies remain separate in outputs.

## 24. Roadmap authority

This document is the scientific source of truth for CASE-Android.

`technical_doc.md` determines **how** software implements this roadmap, but it may not silently redefine:

- dataset roles or validity-gate status;
- paired populations and identity rules;
- recurrence/emergence estimands;
- claim ontologies;
- source feature availability;
- baselines and model ladder;
- split/calibration semantics;
- probability, selective, report, and uncertainty metrics;
- negative-control semantics;
- evidence-scoping policy;
- external replication boundaries;
- claim-promotion gates or wording boundaries.

If implementation reveals that a scientific contract is infeasible or incorrect, update this roadmap explicitly, create a new protocol identity where necessary, and preserve the historical evidence rather than silently changing scientific behavior.

