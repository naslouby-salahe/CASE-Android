# CASE-Android Technical Documentation

**Project:** CASE-Android  
**Authority:** Engineering and implementation companion to [`Roadmap.md`](Roadmap.md)  
**Principle:** implement the scientific roadmap exactly, with the smallest architecture that preserves reproducibility and auditability.

---

## 1. Document authority

`Roadmap.md` defines scientific meaning: population, estimand, features, baselines, splits, metrics, policy semantics, experiments, and claim boundaries.

This document defines:

- repository structure;
- module responsibilities;
- CLI behavior;
- configuration and typing;
- data access;
- artifact/provenance rules;
- tests;
- execution and reporting workflow.

Code must not silently “improve” or reinterpret a roadmap decision. If implementation exposes a scientific problem, stop that workflow and update the roadmap first.

The engineering posture is **feasibility-first but validity-preserving**. Pre-implementation audit work informs the roadmap, but the technical implementation must remain prospective and must not encode expected scientific outcomes. A weaker-than-expected result is not an engineering failure condition. The software must make it easy to regenerate evidence under a corrected protocol and to narrow claims cleanly, while making it difficult to hide leakage, silently move thresholds, or rewrite historical outputs.

---



## 2. Engineering goals

CASE-Android now has two engineering scopes:

1. a **primary SELENE semantic claim-portability/scoping study**;
2. a **gated secondary context-family replication** using KronoDroid when its access, identity, schema, grouping, and leakage gates pass.

The implementation should optimize for:

1. scientific inspectability;
2. zero target leakage;
3. reproducible package/group-held-out evaluation;
4. explicit dataset and feature provenance;
5. strict separation of exploratory/reproducibility artifacts and protocol-frozen outputs;
6. idempotent reruns and safe resume;
7. transparent negative controls;
8. dataset-specific claim semantics;
9. fast routine tests;
10. minimal architecture.

Do not copy FedIEC-scale orchestration, registries, client abstractions, attack regimes, distributed execution, or generic research frameworks.

Do not enlarge architecture merely because the scientific roadmap enlarged. The code should remain a small offline evidence pipeline with dataset-specific contracts.

## 3. Repository shape

The intended tree remains deliberately small:

```text
CASE-Android/
├── README.md
├── LICENSE
├── CITATION.cff
├── .gitignore
├── pyproject.toml
├── config.yaml
├── docs/
│   ├── Roadmap.md
│   └── technical_doc.md
├── src/
│   └── case_android/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── data.py
│       ├── splits.py
│       ├── scoping.py
│       ├── evaluation.py
│       ├── workflows.py
│       └── reporting.py
├── tests/
├── outputs/          # ignored reproducible working artifacts
└── results/          # ignored promoted chapter evidence
```

`data.py` may contain small dataset-specific adapters internally; do not create a hierarchy of dataset services unless the current module becomes genuinely unreadable.

All SELENE and KronoDroid scientific artifacts must carry an explicit dataset identity. Their claim tables are never concatenated into one semantic ontology.

Do not add more top-level packages or service layers unless a concrete roadmap requirement cannot be implemented cleanly with this structure.

## 4. Module responsibilities

### `config.py`

Owns typed loading and validation of `config.yaml` plus machine-local environment/path overrides.

It must:

- resolve one immutable runtime configuration object;
- validate enums, paths, numeric domains, dataset-specific options, and mutually exclusive settings;
- compute a canonical configuration hash;
- reject unknown keys;
- separate local environment values from scientific configuration.

It must not contain experiment logic.

### `data.py`

Owns immutable external-data discovery and canonical CASE data preparation.

SELENE responsibilities:

- locate and verify audited compact source files;
- validate checksums/schemas;
- validate `(sha256, run_id)` uniqueness and exact context pairing;
- construct package groups;
- expose the frozen 19-indicator claim ontology;
- expose the approved source Boolean/count/activity/duration fields;
- construct source-positive recurrence claims;
- construct source-negative cells for target-recorded emergence;
- construct four-state `n00/n01/n10/n11` tables;
- construct paired-vs-unpaired and run-duration audit tables;
- construct indicator redundancy metadata;
- never modify raw source files.

KronoDroid responsibilities (only when the secondary dataset is enabled):

- verify exact dataset revision and source files;
- validate unique SHA pairing and duplicate exclusion;
- verify the aligned 288 syscall-count columns and `nr_syscalls`;
- detect/reject unresolved schema drift;
- construct a **separate** syscall-presence claim ontology;
- expose only roadmap-approved source fields for any model-level replication;
- preserve malware/family/date fields as non-predictive metadata with explicit restrictions.

Optional datasets must have explicit roadmap approval before any adapter is added.

### `splits.py`

Owns persisted train/calibration/test manifests.

SELENE:

- five outer folds grouped by `package_name`;
- deterministic calibration groups inside outer-training partitions;
- same package-to-fold mapping for both directions;
- zero package overlap across roles.

KronoDroid model replication:

- disabled until a valid grouping key and split contract pass the roadmap gates;
- once enabled, persist a separate dataset-specific manifest;
- never reuse SELENE split semantics by assumption.

No model code belongs here.

### `scoping.py`

Owns prospective recurrence scorers and scope policies.

Roadmap-approved methods:

- direction-global prevalence;
- per-claim/indicator persistence;
- activity-volume baseline;
- evidence-strength-only baseline;
- Boolean pooled L2 logistic CASE scorer;
- rich Boolean+count/activity CASE sensitivity;
- duration-normalized rich sensitivity;
- secondary per-indicator logistic scorer;
- calibration-only threshold selection;
- `CROSS_CONTEXT_SUPPORTED` / `SOURCE_CONTEXT_ONLY`;
- explicit `NO_OPERATING_POINT`;
- optional abstention only under a separate protocol identity.

The feature API must validate the named feature profile and reject target/identity/label fields.

### `evaluation.py`

Owns metrics/statistical summaries only.

Responsibilities include:

- four-state transition tables;
- directional recurrence;
- target-recorded emergence;
- disagreement/Jaccard/prevalence difference;
- Brier and Brier Skill Score;
- log loss;
- recurrence and non-recurrence average precision;
- calibration intercept/slope and descriptive ECE;
- risk/coverage curves;
- AUGRC/generalized risk-coverage summary;
- ordinary AURC;
- fixed-coverage and calibration-derived operating-point summaries;
- recurrence retention;
- matched-coverage/matched-risk comparisons;
- report-level coverage/risk/failure/retention;
- micro/indicator-macro/package-macro/report-macro summaries;
- worst-stratum summaries with support;
- fractional ties;
- package-cluster bootstrap;
- typed `NA` reasons.

It must not decide scientific claim language.

### `workflows.py`

Owns thin orchestration for roadmap workflows:

- `validate-selene-contract`;
- `audit-paired-population-and-exposure`;
- `characterize-paired-portability`;
- `reproduce-exploratory-baselines`;
- `evaluate-case-probability`;
- `evaluate-case-scoping`;
- `stress-case-boundaries`;
- `broken-pair-negative-control`;
- `validate-kronodroid-contract`;
- `characterize-kronodroid-portability`;
- `evaluate-kronodroid-scoping` when enabled by gates.

A workflow coordinates existing responsibilities and cannot duplicate model or metric code.

### `reporting.py`

Generates validated tables/figures/evidence indices from completed structured artifacts.

It may create:

- CSV/Parquet result tables;
- PNG/PDF/SVG figures;
- compact JSON evidence/gate indices.

It must not:

- generate manuscript prose;
- decide that a claim is supported;
- create a second generated Markdown research report;
- combine SELENE and KronoDroid claim units into a misleading pooled metric.

### `cli.py`

Owns argument parsing, command dispatch, readable status/errors, and exit codes.

No scientific computation belongs directly in CLI handlers.

## 5. Types and semantic identities

Use explicit enums/types at every scientific boundary.

Minimum semantic types:

```text
DatasetName
  SELENE
  KRONODROID

Direction
  ANDROID10_TO_ANDROID14
  ANDROID14_TO_ANDROID10
  EMULATOR_TO_DEVICE
  DEVICE_TO_EMULATOR

ScopeStatus
  CROSS_CONTEXT_SUPPORTED
  SOURCE_CONTEXT_ONLY

EvidenceState
  STABLE_ABSENT
  TARGET_RECORDED_EMERGENT
  SOURCE_ONLY
  STABLE_PRESENT

FeatureProfile
  BOOLEAN
  ACTIVITY_ONLY
  EVIDENCE_STRENGTH_ONLY
  RICH
  RICH_DURATION_NORMALIZED

WorkflowName
  VALIDATE_SELENE_CONTRACT
  AUDIT_PAIRED_POPULATION_AND_EXPOSURE
  CHARACTERIZE_PAIRED_PORTABILITY
  REPRODUCE_EXPLORATORY_BASELINES
  EVALUATE_CASE_PROBABILITY
  EVALUATE_CASE_SCOPING
  STRESS_CASE_BOUNDARIES
  BROKEN_PAIR_NEGATIVE_CONTROL
  VALIDATE_KRONODROID_CONTRACT
  CHARACTERIZE_KRONODROID_PORTABILITY
  EVALUATE_KRONODROID_SCOPING

DatasetRole
  FIT
  CALIBRATION
  TEST

GateStatus
  PASS
  PARTIAL
  FAIL
  BLOCKED
```

Use dataclasses or Pydantic models for:

- dataset manifests;
- source-file identities;
- split manifests;
- source-feature contracts;
- prediction rows;
- metric results;
- operating-point results;
- gate status;
- artifact metadata.

Avoid dictionary-shaped public interfaces where a typed structure is practical.

Identifiers such as dataset, context, package name, APK SHA-256, run ID, fold ID, claim/indicator, syscall, and feature profile must remain semantically distinct fields.

## 6. Data location and environment

Raw datasets remain outside the repository.

Default shared estate:

```text
/home/naslouby/Projects/datp-shared-data/raw
```

Expected logical locations are resolved by dataset adapter rather than hard-coded into scientific code.

The program resolves the raw-data root in this order:

1. explicit CLI `--data-root`;
2. `CASE_ANDROID_DATA_ROOT`;
3. documented local default only if deliberately selected by the repository.

Do not commit user-specific absolute paths in `config.yaml`.

### Acquisition policy

Standard CASE commands do **not**:

- download SELENE;
- download KronoDroid;
- download restricted datasets;
- execute APKs;
- start Android emulators;
- communicate with physical devices.

`doctor` reports whether required local artifacts exist and whether an optional dataset is disabled, unavailable, blocked, or ready.

Dataset acquisition remains a separate human-controlled action consistent with each dataset's license/access terms.

## 7. Raw-data immutability and canonical preparation

Raw external files are read-only inputs.

`preprocess` creates/reuses dataset-specific canonical artifacts under `outputs/`.

### 7.1 SELENE canonical artifacts

At minimum persist:

- paired APK identity table;
- package group;
- source/target context identities;
- 19 Boolean flags for both recorded contexts in an evaluation-only paired table;
- approved source evidence-count/activity/duration fields;
- source-positive recurrence claims per direction;
- source-negative cells for emergence analysis;
- four-state transitions;
- target recurrence label in an evaluation table physically/logically separated from predictors;
- paired/unpaired selection audit;
- duration/exposure audit;
- indicator redundancy metadata;
- provenance linking every column family to source fields.

### 7.2 Predictor separation

Create typed source-feature matrices from the canonical paired table.

Keep target columns physically separate from predictor frames wherever practical.

No API may select predictor columns by “all numeric fields.”

### 7.3 KronoDroid canonical artifacts

When enabled:

- exact clean unique SHA-pair table;
- duplicate/exclusion audit;
- aligned syscall schema manifest;
- source/target syscall-count matrices;
- binary syscall-presence claims;
- four-state syscall transition table;
- metadata restrictions;
- optional source-feature frame only after model-level gates pass.

SELENE and Krono canonical tables have distinct schema identifiers and cannot be mixed accidentally.

Every canonical artifact carries the input dataset-manifest hash and code/config identity that produced it.

## 8. Leakage firewall

Target leakage is the highest-risk implementation failure and receives architectural protection.

### 8.1 Typed feature profiles

The model API accepts a typed `SourceFeatureFrame` plus an explicit `FeatureProfile`.

SELENE primary `BOOLEAN` profile allows only:

- source 19-flag vector;
- one-hot claim identity.

Other frozen profiles may allow:

- `ACTIVITY_ONLY`: claim identity + approved activity summary;
- `EVIDENCE_STRENGTH_ONLY`: claim identity + approved source count/strength fields;
- `RICH`: Boolean + approved source count/activity fields;
- `RICH_DURATION_NORMALIZED`: frozen normalized transforms.

Krono source profiles are separate and cannot reuse SELENE field names by pattern matching.

### 8.2 Forbidden predictor content

Reject:

- target flags/counts/events;
- target metadata;
- recurrence/emergence labels;
- package name;
- SHA-256;
- run ID;
- fold/split identity;
- malware label;
- malware family;
- target-derived fidelity outcome;
- APK date fields used as temporal target proxies;
- any unknown numeric column.

### 8.3 Poison tests

Tests deliberately inject:

- target-derived columns with plausible names;
- identity columns encoded numerically;
- label aliases;
- metadata/date columns;
- unknown count fields.

The feature builder must reject them.

### 8.4 Fit / calibration / test separation

- fit labels train recurrence models and estimate persistence/global priors;
- calibration labels choose reporting thresholds and assess operating-point feasibility;
- outer-test labels enter only `evaluation.py` after predictions and assignments are frozen;
- calibration target labels do not refit recurrence probability models in the primary protocol.

### 8.5 Discovery/frozen separation

Exploratory/reproducibility outputs cannot be used by code to alter the frozen feature list, folds, thresholds, or metric definitions.

## 9. Split implementation

### 9.1 SELENE frozen evaluation

Use five non-overlapping outer folds grouped by `package_name`.

Build once from one row per exact paired APK using target-label-blind `GroupKFold(n_splits=5)` and reuse the exact package-to-fold mapping for both Android directions.

Requirements:

- every package is outer-test exactly once;
- inside each outer-training partition, 20% of package groups become deterministic calibration groups;
- fit/calibration/test groups are disjoint;
- same manifest is consumed by every model/baseline;
- manifest is generated once, validated, hashed, and reused;
- row order does not change assignment;
- source-positive and source-negative claim tables inherit APK/package roles rather than being independently split.

`plan` displays package/APK/source-positive/source-negative claim counts and per-indicator support by role.

Any legacy exploratory split contract is allowed only in `reproduce-exploratory-baselines`.

### 9.2 KronoDroid

Descriptive recurrence does not require a train/test split.

`evaluate-kronodroid-scoping` remains disabled until the roadmap's grouping gate passes.

When enabled:

- use the frozen validated grouping key;
- persist a dataset-specific outer/calibration manifest;
- keep both context directions on the same base grouping assignment where meaningful;
- do not fall back to row-level random splitting;
- never use family labels for grouping/OOD until reconciled.

## 10. Configuration policy

Use one tracked `config.yaml`.

It may contain:

- logical dataset names and expected relative locations;
- enabled dataset workflows;
- frozen SELENE indicator list;
- broad/non-derived sensitivity list;
- approved source feature profiles;
- evidence-count/activity field allowlists;
- duration-normalization formula/parameters;
- model contract (`C`, `max_iter`, etc.);
- outer fold count;
- calibration split rule;
- predeclared 50%/80% descriptive coverage views;
- optional calibration-derived risk targets;
- bootstrap resample count and seed;
- broken-pair permutation count/seeds;
- fidelity sensitivity definitions;
- figure/table formatting that affects scientific output.

It must not contain:

- secrets;
- machine-specific absolute paths;
- free-form method names;
- arbitrary claim prose;
- silently enabled blocked datasets;
- runtime flags that mutate the frozen protocol.

Every scientific run persists the resolved config and canonical hash.

Changing a scientific value creates a new semantic run identity.

## 11. CLI contract

Keep the public command surface small:

```text
case-android doctor
case-android preprocess
case-android plan
case-android smoke
case-android run <workflow>
case-android status
case-android report
```

### `doctor`

Read-only prerequisite audit:

- Python/package environment;
- raw-data root;
- required SELENE files;
- SELENE schema/checksum state;
- optional KronoDroid availability/readiness;
- blocked optional-dataset status where configured;
- output writeability;
- Git state where useful.

No preprocessing or experiments.

### `preprocess`

Create/reuse canonical artifacts for explicitly enabled datasets.

It never downloads external data.

Idempotent: identical parents reuse a provenance-valid artifact.

### `plan`

Dry-run scientific expansion:

- dataset;
- context directions;
- feature profiles;
- folds/roles;
- workflows;
- methods/baselines;
- expected inputs/outputs;
- counts where materialized;
- gate-dependent disabled workflows.

No fitting.

### `smoke`

Run deterministic synthetic/reduced fixtures through:

```text
paired evidence
→ split
→ source feature profile
→ recurrence score
→ calibration-only policy
→ metrics
→ artifacts
```

Smoke results are not research evidence.

### `run <workflow>`

Execute one descriptive `WorkflowName`.

A blocked workflow exits clearly with the failed/unmet gate; it does not silently degrade into another experiment.

### `status`

Reads manifests/completion/gate metadata and reports state. File existence alone is never completion.

### `report`

Reads validated completed outputs and creates tables/figures/evidence indices.

It never launches preprocessing/fitting/evaluation implicitly.

## 12. Artifact model

### 12.1 Outputs versus results

```text
outputs/
```

contains reproducible working artifacts.

```text
results/
```

contains the small promoted chapter-facing evidence set.

Neither directory is tracked in Git.

### 12.2 Dataset/workflow namespace

Artifacts are namespaced by:

```text
dataset / workflow / semantic_run_id
```

SELENE and KronoDroid outputs never share a prediction/claim table.

### 12.3 Required run metadata

Every completed workflow contains:

```text
manifest.json
completion.json
resolved_config.json
data_manifest.json
gate_snapshot.json
```

and where applicable:

```text
split_manifest.parquet
paired_states.parquet
predictions.parquet
scope_assignments.parquet
metrics.json
report_metrics.parquet
bootstrap_summary.parquet
negative_control_summary.parquet
```

`manifest.json` records:

- dataset/workflow identity;
- semantic run ID;
- Git commit;
- config hash;
- source checksums/revision;
- parent artifact IDs;
- feature profile/schema IDs;
- split identity;
- software environment;
- start/completion metadata;
- generated schema versions.

### 12.4 Completion semantics

A run is complete only when:

- all required payloads exist;
- payload schemas/checks pass;
- parents still match;
- required gates were satisfied at start;
- `completion.json` records successful validation.

A stale/partial run is not reusable.

Use atomic writes/renames for completion-critical artifacts.

## 13. Semantic run identity and invalidation

Run identity changes when any scientific parent changes, including:

- dataset name/revision/checksum;
- license/provenance manifest where it affects allowed processing;
- paired-population/duplicate policy;
- claim ontology;
- broad/non-derived subset;
- source feature allowlist/profile;
- duration-normalization transform;
- split/calibration manifest;
- model parameters;
- baseline definitions;
- reporting coverage/risk targets;
- tie/metric/report aggregation contract;
- broken-pair permutation contract;
- bootstrap configuration;
- code revision when behavior changes.

Formatting-only report changes do not retrigger modeling when scientific parents are unchanged.

`report` never silently regenerates missing scientific parents.

## 14. Metric implementation contracts

### 14.1 Paired-state metrics

Implement exact per-claim-type counts:

```text
n00
n01
n10
n11
```

Derived metrics include:

- both directional source-positive recurrence rates;
- target-recorded emergence among source-negative cells;
- paired disagreement;
- Jaccard overlap;
- paired prevalence difference.

Direction mapping must be unit-tested so `n01/n10` are never silently reversed.

### 14.2 Proper probability scores

Implement:

- Brier;
- Brier Skill Score versus persistence;
- log loss.

Clip probabilities only for log-loss numerical stability using the roadmap epsilon.

Brier and ranking use raw probabilities.

### 14.3 Calibration

Headline calibration uses untouched concatenated OOF test predictions.

Implement:

- calibration intercept;
- calibration slope;
- reliability-bin table;
- descriptive ECE with bin count/strategy/denominator.

Calibration-partition diagnostics are stored separately and never presented as held-out calibration quality.

### 14.4 Ranking

Implement:

- recurrence AP;
- non-recurrence AP using `1 - score` against `1 - target`;
- prevalence/persistence reference values.

AP is secondary.

### 14.5 Risk / coverage

Threshold sweep returns:

- supported coverage;
- supported non-recurrence risk;
- recurrence retention.

Implement:

- AUGRC/generalized risk-coverage summary;
- ordinary AURC;
- fixed-coverage views;
- calibration-derived risk-target views;
- matched-coverage risk difference;
- matched-risk coverage difference.

AUGRC must pass both a hand fixture and independent formula/reference check.

### 14.6 Report-level aggregation

For each APK report at a declared operating point compute:

- supported fraction;
- non-recurrence risk among selected claims;
- whether any selected claim failed recurrence;
- recurrence retention;
- selected-claim count.

Aggregate as report/APK macro with exact denominator rules.

These metrics never get labels such as “analyst efficiency” or “security benefit.”

### 14.7 Macro / worst-stratum

Keep separate functions for:

- claim-micro;
- indicator/claim-macro;
- package-macro;
- report/APK-macro.

Worst-indicator/stratum summaries always include support counts.

Do not hide weighting behind a generic ambiguous `average=` option.

### 14.8 Fixed-coverage ties

Use fractional cutoff handling or mathematically equivalent expected-value logic.

Unit tests must prove row-order invariance.

### 14.9 Undefined metrics

Every metric result is typed with:

- value/null;
- denominator/population;
- `DEFINED` or `NA`;
- machine-readable `NA` reason.

Never replace undefined metrics with zero.

### 14.10 Probability calibration policy

The primary recurrence models use their raw logistic probabilities.

No Platt/isotonic/temperature calibrator is fitted in the primary protocol.

A future probability calibrator is a separate predeclared protocol identity.

## 15. Package-cluster bootstrap

The bootstrap resamples `package_name`, never individual claim rows.

Implementation contract:

1. Build a package→claim-index mapping from OOF predictions.
2. Draw packages with replacement using the frozen analysis seed.
3. Materialize all claims for each sampled package, preserving multiplicity.
4. Recompute method metrics on the same resample.
5. Compute paired method-minus-baseline differences.
6. Repeat 10,000 times.
7. Persist percentile intervals and bootstrap metadata.

Tests must include packages with unequal claim counts so an accidental row-level bootstrap is detectable.

---

## 16. Scope-policy implementation

The core policy API receives:

- dataset/direction/fold identity;
- frozen recurrence scores for one method;
- calibration scores/outcomes/group IDs;
- predeclared fixed-coverage views;
- optional calibration-derived empirical risk targets.

It returns:

- the continuous recurrence score unchanged;
- calibration threshold diagnostics;
- selected threshold(s);
- deterministic `CROSS_CONTEXT_SUPPORTED` / `SOURCE_CONTEXT_ONLY` assignments;
- explicit `NO_OPERATING_POINT` when a requested target is unavailable.

Rules:

- threshold selection is deterministic under tied scores and row permutation;
- test outcomes are never available to threshold selection;
- a risk target is never relaxed after test inspection;
- `SOURCE_CONTEXT_ONLY` can never serialize/render as `TARGET_ABSENT`;
- descriptive fixed-coverage metrics may rank OOF test scores for analysis, but those are labeled retrospective and are distinct from a deployable calibration-selected policy;
- formal guarantee metadata is absent unless the roadmap G13 contract passes.

An optional abstention protocol, if later added, has a distinct type/schema/run identity and cannot silently alter the two-status core.

## 17. Experiment workflow contracts

### `validate-selene-contract`

Produces:

- source inventory/checksums;
- live license/citation record;
- schema snapshot;
- join/uniqueness checks;
- paired/unpaired counts;
- package counts;
- 19-indicator inventory;
- redundancy/derived-feature inventory;
- source feature allowlist;
- fidelity/provenance warning summary.

### `audit-paired-population-and-exposure`

Produces:

- paired vs Android-10-only prevalences;
- macro/max absolute prevalence difference;
- source-positive claim/activity distributions;
- package summary;
- both context duration distributions.

No causal explanation is inferred from metadata that does not support it.

### `characterize-paired-portability`

Produces:

- per-indicator `n00/n01/n10/n11`;
- directional recurrence;
- target-recorded emergence;
- disagreement/Jaccard/prevalence difference;
- support counts;
- descriptive uncertainty.

No model fitting.

### `reproduce-exploratory-baselines`

Uses the separately identified exploratory split contracts only.

Reproduces:

- persistence;
- Boolean;
- count/activity/rich/normalized variants;
- descriptive selective views;
- broken-pair reproducibility diagnostic.

Outputs an expected-versus-reproduced reconciliation table.

It never contributes directly to frozen claim support.

### `evaluate-case-probability`

For every SELENE direction/fold/profile:

- fit model/prior on fit groups;
- score untouched outer test;
- persist raw probabilities;
- compute proper-score/calibration/ranking artifacts;
- after folds, assemble OOF predictions;
- compute paired package-bootstrap comparisons.

No scope threshold is selected here.

### `evaluate-case-scoping`

For every direction/fold:

- read already-fit model scores;
- select thresholds on calibration groups only;
- freeze assignments;
- evaluate untouched test assignments;
- aggregate OOF selective/report results.

Produces full curves plus declared operating-point tables.

### `stress-case-boundaries`

Reuses frozen OOF predictions where possible.

Computes:

- indicator macro/worst;
- package/report macro;
- broad/non-derived sensitivity;
- raw vs duration-normalized feature sensitivity;
- direction comparison;
- paired-selection/exposure summaries;
- fidelity diagnostics;
- any predeclared split/missing/noise sensitivity.

It cannot tune the primary model from test outcomes.

### `broken-pair-negative-control`

Permutes **complete target APK evidence blocks** inside each frozen test fold/direction using predeclared seeds.

It preserves target marginal evidence distributions while breaking true APK identity.

Produces method-vs-persistence diagnostic summaries.

A persistent large CASE advantage marks the workflow/gate as invalid for interpretation.

### `validate-kronodroid-contract`

Produces:

- exact source/revision/checksums;
- schema report;
- current-artifact discrepancy resolution status;
- exact hash overlap;
- duplicate/conflicting identity exclusions;
- aligned syscall field manifest;
- metadata restrictions;
- model-level grouping/source-feature readiness.

### `characterize-kronodroid-portability`

Produces:

- exact clean paired population;
- per-syscall four states;
- both recurrence directions;
- support≥100 macro;
- broken-pair descriptive control;
- valid descriptive malware/benign strata where allowed.

### `evaluate-kronodroid-scoping`

Disabled unless model-level gates pass.

Uses a separately frozen Krono source-only feature/baseline/split contract and produces external model/scoping evidence.

Never pools Krono predictions with SELENE predictions.

## 18. Testing strategy

Routine tests should finish comfortably within five minutes on a normal development machine. Full research workflows are not routine tests.

### 18.1 Unit tests

Cover:

- config parsing/unknown keys;
- dataset/direction/status/evidence-state/feature-profile enums;
- SELENE source-positive recurrence claim construction;
- source-negative emergence construction;
- four-state mapping;
- evidence-count transforms and duration normalization;
- Brier/Brier-skill/log-loss fixtures;
- calibration helper edge cases;
- recurrence/non-recurrence AP;
- risk/coverage formulas;
- AUGRC/AURC fixtures;
- fractional ties;
- macro/report aggregation;
- typed `NA`;
- threshold boundaries;
- canonical hashing.

### 18.2 Leakage tests

Mandatory:

- target-column poison;
- target-count poison;
- recurrence-label alias poison;
- package/hash/run identity poison;
- numeric metadata/date poison;
- unknown-feature poison;
- test-outcome access during threshold selection;
- post-hoc indicator-filter attempt.

Any leakage test failure blocks research workflows.

### 18.3 Split tests

SELENE:

- each package outer-test exactly once;
- fit/calibration/test disjoint;
- source-positive/source-negative tables inherit roles correctly;
- row reorder leaves persisted split identity unchanged;
- all methods consume same manifest.

Krono model replication gets separate tests after its grouping contract exists.

### 18.4 Negative-control tests

Verify:

- permutation happens at complete target-APK block level;
- source rows are unchanged;
- target marginal claim frequencies are preserved;
- deterministic seeds;
- no identity column leaks into permutation/scoring.

### 18.5 Bootstrap tests

Verify package—not row—resampling, unequal package sizes, deterministic seed, paired method resamples, and fixture percentile intervals.

### 18.6 Integration tests

Synthetic tables validate:

```text
paired observations
→ four-state claims
→ source-positive/source-negative tables
→ group split
→ feature profile
→ recurrence scorer
→ calibration-only policy
→ claim/report metrics
→ negative control
→ manifests
```

### 18.7 End-to-end smoke

One deterministic smoke path validates CLI/artifact lifecycle without full datasets.

### 18.8 Local-data contract tests

Optional local tests:

- real SELENE `validate-selene-contract`;
- real Krono `validate-kronodroid-contract` when data are available.

They skip with explicit reason and never download data.

## 19. Dependencies

Keep dependencies limited to what the roadmap requires. A reasonable initial set is:

- Python 3.12 or the repository-selected supported version;
- NumPy;
- Polars or pandas — choose one primary dataframe library, not both without need;
- PyArrow for Parquet;
- scikit-learn for logistic models and standard metrics;
- Pydantic for typed configuration/manifests;
- Typer for CLI;
- Matplotlib for figures;
- pytest for tests.

Add SciPy only if a roadmap-backed statistical operation materially needs it.

Do not add PyTorch/TensorFlow, Flower, Docker, a database, a web framework, or distributed execution tooling for the current project.

---

## 20. Logging and error behavior

Logs are diagnostic, not scientific evidence.

Use structured, concise logging for:

- workflow start/end;
- artifact reuse/invalidation;
- fold/method progress;
- validation failures;
- counts and paths useful for debugging.

Do not print full APK hashes or raw potentially sensitive SELENE strings at high volume.

Errors must be explicit. Never convert a failed validation into an empty result or a completed artifact.

---

## 21. Idempotency and resume

All commands are safe to rerun.

- `doctor` is read-only.
- `preprocess` reuses only provenance-valid canonical data.
- `plan` is read-only.
- `smoke` writes to its own deterministic smoke namespace.
- `run` reuses valid completed cells and recomputes only invalid/missing dependencies.
- `report` reads validated outputs only.

Partial workflows may resume from completed valid artifacts. Do not delete successful upstream work because a later fold/method failed.

No `--overwrite` path may bypass provenance checks. If an explicit overwrite option is later added, it removes/rebuilds the requested artifact safely rather than mutating scientific files in place.

---

## 22. Results promotion

`results/` contains chapter-facing evidence only.

Promotion requires:

- source workflow complete and provenance-valid;
- relevant roadmap validity gates pass;
- expected metric schema present;
- `NA` values affecting the claim are explicitly handled;
- evaluation-stage status explicit (exploratory, protocol-frozen, or external);
- table/figure generated from exact structured parents;
- dataset/claim ontology explicit.

Recommended structure:

```text
results/
├── selene/
│   ├── tables/
│   └── figures/
├── kronodroid/
│   ├── tables/
│   └── figures/
└── evidence_index.json
```

`evidence_index.json` maps every promoted artifact to:

- dataset;
- workflow/run IDs;
- input/source manifest;
- split identity where applicable;
- feature profile;
- metric artifact;
- gate snapshot;
- evaluation-stage classification.

It is lineage metadata, not a `claim_registry`.

Do not promote a broad multi-context figure that silently combines SELENE semantic indicators and Krono syscall claims into one pooled metric.

## 23. Quality rules

- Keep functions small enough to understand without creating responsibility-free wrappers.
- Prefer tested library implementations for standard operations.
- Keep dataset, source/target direction, claim ontology, and feature profile explicit in names/types.
- No `Any`/untyped dictionary interfaces at core scientific boundaries when typed models are practical.
- Avoid hidden global state and mutable singleton config.
- No data work at import time.
- No experiment-specific duplicated metric implementations.
- No manual scientific values copied into reporting code.
- No generated Markdown research reports.
- No Docker requirement.
- No claim registry.
- No FL-client/IoT abstractions.
- No automatic APK execution/emulator/device path.
- No automatic restricted-dataset acquisition.
- Do not make SELENE and KronoDroid share a claim schema merely for code reuse.
- Dataset-specific adapters may share generic utilities but must preserve semantic contracts.
- Do not add AI-flavored comments/docstrings; document the scientific reason for non-obvious behavior.

## 24. Implementation sequence

### Step 1 — Project foundation

Create package/config/CLI skeleton, semantic types, artifact manifests, and fast tests.

**Completion:** `doctor`, `plan`, and smoke wiring work without full data.

### Step 2 — SELENE contract and canonical evidence

Implement file/checksum/license records, exact pairing, package groups, 19 indicators, approved source count/activity fields, source-positive/source-negative tables, four states, selection/exposure audits.

**Completion:** audited anchors reproduce or discrepancies are documented.

### Step 3 — Splits and leakage firewall

Implement five outer folds, calibration groups, feature-profile firewall, and poison tests.

**Completion:** G5/G6 implementation tests pass.

### Step 4 — Metrics and baselines

Implement paired-state metrics, global/persistence/activity/evidence-strength baselines, proper scores, calibration, AP, selective/report metrics, tie rules, bootstrap.

**Completion:** all fixtures pass.

### Step 5 — CASE model ladder and policy

Implement Boolean pooled L2 primary, rich/count sensitivities, normalized sensitivity, per-indicator comparator, calibration-only policy, `NO_OPERATING_POINT`.

**Completion:** feature profile and test-label firewalls pass.

### Step 6 — Negative controls

Implement complete-target-APK broken-pair permutations and diagnostics.

**Completion:** permutation invariants/tests pass.

### Step 7 — Discovery reproduction

Reproduce the separately identified exploratory baseline/model contracts only as an implementation-continuity check; do not encode expected outcome values.

**Completion:** material discrepancies reconciled.

### Step 8 — Evaluation freeze

Persist final SELENE scientific config, folds, feature contracts, baselines, metrics, policy, sensitivity, negative-control and claim/gate interpretation identity.

**Completion:** Roadmap pre-frozen checklist passes.

### Step 9 — Main SELENE evaluation

Run paired characterization, probability evaluation, calibration-only scoping, boundary sensitivities, and bootstrap.

**Completion:** all required OOF/metric artifacts validate.

### Step 10 — KronoDroid descriptive replication

Implement/freeze the audited exact-pair/syscall recurrence workflow and resolve schema provenance.

**Completion:** descriptive external evidence validates.

### Step 11 — KronoDroid model-level replication

Only if its grouping/source-feature gates pass, freeze and run the external source-only model/scoping protocol.

**Completion:** external result is promoted or explicitly marked unsupported/insufficient; do not tune SELENE from it.

### Step 12 — Reporting/promotion

Generate only roadmap-required tables/figures/evidence lineage.

**Completion:** every promoted number traces to validated structured output.

## 25. Definition of done

An implementation change is complete only when:

- it has one clear roadmap-backed responsibility;
- dataset/claim semantics match `Roadmap.md`;
- relevant unit/integration/leakage/negative-control tests pass;
- generated artifacts carry complete provenance;
- rerunning identical valid inputs is idempotent;
- no raw dataset/output/result is accidentally staged in Git;
- blocked workflows fail explicitly rather than silently changing design;
- documentation reflects current behavior, not aspirational behavior;
- no broader claim is introduced through naming/reporting;
- SELENE and external-replication evidence remain semantically separated.

## 26. Explicit non-goals

Do not build:

- federated-learning orchestration;
- simulated FL clients;
- IoT/device abstractions;
- a generic experiment registry;
- a generic claims subsystem;
- a database-backed artifact service;
- a web API;
- distributed workers;
- a deep-learning stack;
- automatic dataset download/execution tooling;
- APK execution;
- Android emulator execution;
- physical-device execution/control;
- user-study infrastructure;
- a broad model tournament;
- automatic access workarounds for restricted datasets;
- large architecture-enforcement machinery copied from FedIEC.

Reconsider any item only after an explicit roadmap revision creates a scientifically justified requirement.

## 27. Engineering audit checklist

Before implementation is ready for the main frozen SELENE run:

### Architecture / provenance

- [ ] Repository tree remains minimal.
- [ ] One authoritative config surface exists.
- [ ] Raw datasets are external and immutable.
- [ ] Dataset/source revision and checksums are persisted.
- [ ] Dataset identity is present on every scientific artifact.
- [ ] Discovery and frozen artifacts cannot be confused/reused interchangeably.
- [ ] Artifact reuse validates all scientific parents.
- [ ] Stale/partial artifacts cannot be promoted.

### SELENE data contract

- [ ] Exact paired identities reproduce the roadmap contract.
- [ ] Package groups validated.
- [ ] 19-indicator schema frozen.
- [ ] source count/activity/duration allowlists frozen.
- [ ] source-negative emergence cells constructed correctly.
- [ ] four-state mapping tested.
- [ ] paired/unpaired and duration audits generated.
- [ ] duplicate/derived indicator metadata persisted.
- [ ] fidelity data cannot become predictor/ground truth silently.

### Splits / leakage

- [ ] Five package-grouped outer manifests persisted.
- [ ] Every package outer-test exactly once.
- [ ] Fit/calibration/test are disjoint.
- [ ] Target-column poison tests pass.
- [ ] Target-count/label-alias poison tests pass.
- [ ] Identity poison tests pass.
- [ ] Unknown numeric feature poison test passes.
- [ ] Threshold selection cannot access test outcomes.
- [ ] Test outcomes cannot filter indicators/features.
- [ ] All methods consume the same split manifest.

### Models / baselines

- [ ] global prevalence implemented fit-only.
- [ ] persistence implemented fit-only with recorded fallback.
- [ ] activity baseline implemented.
- [ ] evidence-strength-only baseline implemented.
- [ ] Boolean pooled L2 primary implemented.
- [ ] rich and normalized sensitivity profiles implemented separately.
- [ ] secondary per-indicator model produces explicit `NA` when not estimable.
- [ ] no blocked complex model enters the frozen run.

### Metrics / policy

- [ ] `n00/n01/n10/n11` and direction mapping tested.
- [ ] target-recorded emergence tested.
- [ ] Brier/BSS/log-loss fixtures pass.
- [ ] recurrence/non-recurrence AP tested.
- [ ] calibration intercept/slope use OOF test predictions.
- [ ] AUGRC/AURC independently validated.
- [ ] risk/coverage/retention formulas pass.
- [ ] matched coverage/risk rules are deterministic.
- [ ] report-level aggregation tested.
- [ ] tie handling is row-order invariant.
- [ ] typed `NA` reasons implemented.
- [ ] `NO_OPERATING_POINT` is a valid result.
- [ ] formal guarantee labels are impossible unless explicitly enabled by a future roadmap protocol.

### Uncertainty / controls

- [ ] package—not row—bootstrap tested.
- [ ] paired method resamples tested.
- [ ] broken-pair permutation operates on complete target APK blocks.
- [ ] broken-pair seeds/count persisted.
- [ ] negative-control results cannot alter the primary model contract.
- [ ] split-sensitivity diagnostics cannot select the “best” main run.

### CLI / reporting

- [ ] `doctor` is read-only.
- [ ] `preprocess` never downloads/runs APKs.
- [ ] `plan` is read-only.
- [ ] `report` never launches analysis.
- [ ] results promotion records gate and evaluation-stage status.
- [ ] no generated Markdown research report.
- [ ] no full raw data/outputs/results tracked by Git.

### KronoDroid before model-level external replication

- [ ] exact external revision/checksums frozen.
- [ ] unique SHA pair/duplicate logic validated.
- [ ] 288 syscall fields + aggregate schema frozen.
- [ ] current-artifact/public-documentation discrepancy resolved.
- [ ] family disagreement documented and excluded from OOD claims.
- [ ] metadata dates excluded from temporal claims.
- [ ] valid grouping key established.
- [ ] source feature profile frozen.
- [ ] leakage/split tests exist for Krono.
- [ ] Krono outputs cannot be pooled semantically with SELENE.

### Scope boundaries

- [ ] no behavior-truth/absence terminology.
- [ ] no causal Android-version/device statement.
- [ ] no universal Android portability wording.
- [ ] no analyst-time/security-impact claim.
- [ ] no FL/IoT empirical claim.
- [ ] no fresh physical-device/emulator collection path.

