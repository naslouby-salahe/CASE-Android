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

The engineering posture is **feasibility-first but validity-preserving**. The project was selected after extensive discovery and dataset-backed PoCs. Therefore a weaker-than-expected result is not an engineering failure condition. The software must make it easy to regenerate evidence under a corrected protocol and to narrow claims cleanly, while making it difficult to hide leakage, silently move thresholds, or rewrite historical outputs.

---



## 2. Engineering goals

CASE-Android is one compact offline paired-context study. The implementation should optimize for:

1. scientific inspectability;
2. zero target leakage;
3. reproducible package-grouped evaluation;
4. explicit provenance;
5. idempotent reruns;
6. fast routine tests;
7. minimal architecture.

Do not copy FedIEC-scale orchestration, registries, client abstractions, attack regimes, or audit frameworks.

---

## 3. Repository shape

The intended implementation tree is deliberately small:

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

Do not add more top-level packages or service layers unless a concrete roadmap requirement cannot be implemented cleanly with this structure.

---

## 4. Module responsibilities

### `config.py`

Owns typed loading and validation of `config.yaml` plus machine-local overrides.

It must:

- resolve one immutable runtime configuration object;
- validate enums, paths, numeric domains, and mutually exclusive settings;
- compute a canonical configuration hash;
- reject unknown keys;
- separate local environment values from scientific configuration.

It must not contain experiment logic.

### `data.py`

Owns immutable external-data discovery and canonical CASE data preparation.

Responsibilities:

- locate SELENE under the shared data root;
- verify expected files/checksums/schema;
- validate `(sha256, run_id)` uniqueness and joins;
- construct the exact paired APK population;
- construct package groups;
- expose the frozen 19-indicator schema;
- create source-positive claim tables per direction;
- create the paired-vs-unpaired audit table;
- never modify raw source files.

### `splits.py`

Owns package-level train/calibration/test manifests.

Responsibilities:

- generate or load the frozen five outer package folds;
- generate deterministic calibration groups inside outer-training folds;
- assert zero package overlap across roles;
- persist exact split manifests;
- provide split identities/hashes to workflows.

No model code belongs here.

### `scoping.py`

Owns all prospective scoring methods and the CASE scope policy.

Contains only roadmap-approved methods:

- always-generalize policy;
- per-indicator persistence;
- activity-volume baseline;
- pooled L2 logistic CASE scorer;
- secondary per-indicator logistic scorer;
- calibration-only threshold selection for optional reporting operating points;
- `cross-context-supported` versus `source-context-only` assignment;
- optional abstention/uncertainty sensitivity only when explicitly enabled by a separate roadmap protocol.

This module must expose a single source-feature interface. It must be impossible for callers to pass target-context feature columns as predictors without validation failure.

### `evaluation.py`

Owns metrics and statistical summaries only.

Responsibilities:

- Brier score;
- log loss;
- average precision;
- calibration intercept/slope and descriptive ECE;
- risk/coverage curves;
- generalized risk-coverage summary;
- fixed-coverage summaries;
- recurrence retention;
- scope status metrics;
- micro, indicator-macro, package-macro, and worst-indicator summaries;
- fractional tie handling;
- package-cluster bootstrap;
- explicit `NA` reasons.

It must not decide scientific claim language.

### `workflows.py`

Owns the thin orchestration for the roadmap experiments:

- `validate-selene-contract`;
- `audit-paired-population`;
- `reproduce-exploratory-baselines`;
- `evaluate-case-scoping`;
- `stress-indicator-and-direction`.

A workflow coordinates existing responsibilities; it must not duplicate model or metric implementations.

### `reporting.py`

Owns generation of validated tables and figures from completed artifacts.

It may create:

- CSV/Parquet result tables;
- PNG/PDF/SVG figures as required;
- concise machine-readable evidence indices.

It must **not** generate manuscript prose, claims, or a second Markdown scientific report. Human-authored research interpretation stays in `docs/` and the manuscript.

### `cli.py`

Owns only argument parsing, command dispatch, readable status/error output, and exit codes.

No scientific computation belongs directly in CLI handlers.

---

## 5. Types and semantic identities

Use explicit types/enums at scientific boundaries rather than free-form strings.

Minimum semantic types:

```text
Direction
  ANDROID10_TO_ANDROID14
  ANDROID14_TO_ANDROID10

ScopeStatus
  CROSS_CONTEXT_SUPPORTED
  SOURCE_CONTEXT_ONLY

WorkflowName
  VALIDATE_SELENE_CONTRACT
  AUDIT_PAIRED_POPULATION
  REPRODUCE_EXPLORATORY_BASELINES
  EVALUATE_CASE_SCOPING
  STRESS_INDICATOR_AND_DIRECTION

DatasetRole
  TRAIN
  CALIBRATION
  TEST
```

Use dataclasses or Pydantic models for manifests/config/artifact metadata. Avoid dictionary-shaped public interfaces where a typed structure is practical.

Identifiers such as package name, APK SHA-256, run ID, fold ID, and indicator must remain semantically distinct fields.

---

## 6. Data location and environment

Raw data remain outside the repository.

Default shared estate:

```text
/home/naslouby/Projects/datp-shared-data/raw
```

The program resolves the local root in this order:

1. explicit CLI `--data-root` if provided;
2. `CASE_ANDROID_DATA_ROOT` environment variable;
3. documented local default only if the roadmap/repository deliberately chooses one.

Do not commit a user-specific absolute path in `config.yaml`.

No standard command downloads SELENE automatically. `doctor` explains missing data and the expected source; acquisition is a separate human-controlled action.

---

## 7. Raw-data immutability and canonical preparation

Raw SELENE files are read-only inputs.

`preprocess` may write a compact canonical CASE representation under `outputs/`, containing only the columns required by the roadmap. The canonical data should include, at minimum:

- APK SHA-256;
- package name;
- direction/context identity;
- frozen 19 source flags;
- target recurrence label for evaluation artifacts only;
- source-positive claim indicator;
- provenance linking back to source files.

Keep target columns physically separate from predictor matrices wherever practical.

The canonical representation must never overwrite the raw data and must carry the source-manifest hash that produced it.

---

## 8. Leakage firewall

Target leakage is the highest-risk implementation failure and receives explicit architectural protection.

### 8.1 Predictor allowlist

The model-building API accepts a typed `SourceFeatureFrame` rather than arbitrary table columns.

Allowed predictor content for the primary scorer:

- source 19-flag vector;
- claim-indicator identity.

Forbidden predictor content:

- any target flag;
- target run metadata;
- target summaries;
- recurrence label;
- package name;
- SHA-256;
- run ID;
- family/malware labels.

### 8.2 Poison tests

Tests must deliberately add target-derived columns with attractive names and verify that the pipeline rejects them rather than silently using “all numeric columns.”

### 8.3 Fit/threshold separation

Model fitting receives train claims only. Threshold/support selection receives calibration claims only. Outer-test targets are consumed only by `evaluation.py` after predictions/status assignments are frozen.

---

## 9. Split implementation

The confirmatory protocol is five non-overlapping outer folds grouped by `package_name`. Generate the outer manifest once from the paired-APK table (one row per paired APK) with `GroupKFold(n_splits=5)` and reuse the exact package-to-fold mapping in both directions. No target recurrence label participates in fold construction.

Requirements:

- every package occurs in exactly one outer test fold;
- within each outer-training partition, 20% of its package groups are assigned to calibration using the frozen calibration seed and fold identity;
- each outer-training population is subdivided into train and calibration groups without overlap;
- no APK or package crosses roles within a fold;
- the same persisted manifest is used by every method;
- fold assignment is generated once, validated, hashed, and reused;
- row order cannot change fold assignment.

`plan` must show package/APK/claim counts by direction and role before any run begins.

The historical seeds 17/42/91 are allowed only in `reproduce-exploratory-baselines`; they are not the confirmatory split protocol.

---

## 10. Configuration policy

Use one tracked `config.yaml`.

It may contain:

- dataset logical name and expected relative paths;
- frozen indicator list;
- model contract values such as `C` and `max_iter`;
- outer-fold count;
- calibration split rule;
- predeclared coverage points and any optional calibration-derived risk targets used for reporting;
- optional abstention-sensitivity settings only if that analysis is explicitly retained;
- bootstrap resample count and analysis seed;
- figure/table formatting values that affect outputs.

It must not contain:

- secrets;
- machine-specific absolute paths;
- free-form method names;
- arbitrary claim text;
- runtime switches that can silently change the confirmatory protocol.

Every run persists the resolved config and config hash.

Changing a scientific value creates a new semantic run identity; it never mutates an existing completed run.

---

## 11. CLI contract

The public command surface remains small:

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
- data-root resolution;
- required SELENE files;
- expected schemas;
- writeability of generated-output locations;
- current Git state where relevant.

No preprocessing or experiments.

### `preprocess`

Create/reuse the canonical CASE paired data and provenance manifest.

Idempotent: identical inputs/config reuse a valid artifact; changed parents invalidate it.

### `plan`

Dry-run scientific expansion:

- directions;
- folds;
- workflows;
- methods;
- expected input artifacts;
- expected output artifacts;
- counts where already materialized.

It performs no model fitting.

### `smoke`

Run a tiny deterministic fixture through data → split → score → policy → metric → artifact.

The smoke path uses synthetic/reduced fixtures, not a hidden mini research result.

### `run <workflow>`

Execute exactly one descriptive roadmap workflow.

Accepted workflow names are derived from `WorkflowName`; no opaque numeric experiment IDs.

### `status`

Read manifests/completion markers and show current validity/completion state. It does not infer completion from “file exists.”

### `report`

Read validated completed outputs and create tables/figures/results. It never starts preprocessing, fitting, or evaluation implicitly.

---

## 12. Artifact model

### 12.1 Outputs versus results

```text
outputs/
```

contains working/reproducible artifacts.

```text
results/
```

contains a small promoted set of chapter-facing evidence generated from validated outputs.

Neither directory is committed to Git.

### 12.2 Required run metadata

Every completed workflow directory contains at least:

```text
manifest.json
completion.json
resolved_config.json
data_manifest.json
```

and, where applicable:

```text
split_manifest.parquet
predictions.parquet
metrics.json
bootstrap_summary.parquet
```

`manifest.json` records:

- workflow identity;
- semantic run ID;
- Git commit;
- resolved config hash;
- dataset/source checksums;
- parent artifact IDs;
- software environment identity;
- start/completion metadata;
- schema versions for generated tables.

### 12.3 Completion semantics

A run is complete only when:

- all required payloads exist;
- payload checks pass;
- parent identities still match;
- `completion.json` records successful validation.

A stale or partially written run is never treated as reusable.

Use atomic write/rename for completion-critical files.

---

## 13. Semantic run identity and invalidation

Run identity must change when any scientific parent changes, including:

- source dataset checksum;
- indicator schema;
- paired-population construction;
- split manifest;
- source-feature contract;
- model parameters;
- reporting coverage points and any optional calibration-derived risk targets;
- metric contract;
- bootstrap configuration;
- code revision when behavior changes.

Reporting-only formatting changes should not retrigger modeling if the scientific parents are unchanged.

`report` must never silently regenerate missing predictions.

---

## 14. Metric implementation contracts

### 14.1 Proper scoring rules

Implement Brier and log loss directly or through trusted library functions with fixture verification.

Predicted probabilities must be clipped only for numerical safety in log loss, using one documented epsilon. Brier uses the unmodified probability within `[0,1]`.

### 14.2 Calibration

Calibration intercept/slope are computed from held-out out-of-fold predictions. ECE is descriptive only and must store:

- number of bins;
- binning strategy;
- denominator;
- direction/indicator population.

### 14.3 Fixed-coverage tie handling

Implement fractional cutoff handling. A unit test must demonstrate identical results after arbitrary row permutation.

Never break ties by stable input order, hash, or package name for a scientific metric.

### 14.4 Risk-coverage

The evaluation module exposes a monotone threshold sweep from scores to:

- coverage;
- supported non-recurrence risk;
- recurrence retention.

The generalized risk-coverage summary must be validated against a small hand-computable fixture and an independent reference implementation or direct formula test before use in confirmatory outputs.

### 14.5 Macro aggregation

Keep distinct functions for:

- claim-micro;
- indicator-macro;
- package-macro.

Do not implement a generic `average=` switch that makes scientific weighting ambiguous.

### 14.6 Undefined values

Every metric result uses a typed structure containing:

- value or null;
- denominator/population;
- status `DEFINED` or `NA`;
- `NA` reason when undefined.

---

### 14.7 Probability calibration policy

The primary confirmatory model uses the raw logistic probability output. Do not fit Platt, isotonic, temperature, or other post-hoc calibrators in the primary workflow. The calibration partition is reserved for operating-point selection and diagnostics. A future calibrator would be a separate predeclared sensitivity experiment with a new protocol identity, not an invisible implementation tweak.

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

- test scores for one direction/fold;
- calibration scores/outcomes and package IDs;
- predeclared reporting coverage points;
- any optional calibration-derived risk targets.

It returns:

- the continuous score unchanged;
- calibration diagnostics for candidate thresholds;
- deterministic `CROSS_CONTEXT_SUPPORTED` / `SOURCE_CONTEXT_ONLY` assignments for any selected operating point;
- explicit `NO_OPERATING_POINT` when a requested risk target is not achievable from calibration data.

`NO_OPERATING_POINT` is a valid result, not an exception and not a project failure. The caller reports the achievable risk-coverage frontier instead of relaxing the target after seeing test outcomes.

Threshold selection must be deterministic under tied scores and row permutation. Target-test outcomes are never used to choose the threshold.

`SOURCE_CONTEXT_ONLY` means “do not generalize this recorded source observation under this operating policy.” It must never be encoded or rendered as `TARGET_ABSENT`.

An optional uncertainty/abstention policy, if later retained, must implement a distinct protocol type and output schema so it cannot silently alter the core two-scope analysis.

---

## 17. Experiment workflow contracts

### `validate-selene-contract`

Must produce:

- source file inventory/checksums;
- schema snapshot;
- join/uniqueness checks;
- paired/unpaired APK counts;
- package counts;
- indicator inventory;
- fidelity/provenance warning summary.

### `audit-paired-population`

Must produce:

- paired vs A10-only flag prevalences;
- absolute prevalence differences;
- claim-count distributions;
- package-level summary;
- no causal explanations not present in source metadata.

### `reproduce-exploratory-baselines`

Must use the historical exploratory split contract only and output a reconciliation table with expected/audited values and tolerances.

It cannot create confirmatory claim support.

### `evaluate-case-scoping`

Must produce for every direction and outer fold:

- trained-method identity;
- calibration threshold/operating-point diagnostics;
- untouched test predictions;
- two-scope assignments for selected operating points;
- metric artifacts.

After all folds it produces one OOF prediction table per direction and the paired cluster-bootstrap comparison.

### `stress-indicator-and-direction`

Must reuse the frozen OOF predictions. It may not refit or tune the primary model in response to test results.

It computes:

- indicator macro/worst results;
- package macro results;
- broad-only schema sensitivity if predeclared;
- activity-volume comparison;
- direction-specific summaries.

---

## 18. Testing strategy

Routine tests should finish comfortably within five minutes on a normal development machine.

### 18.1 Unit tests

Cover:

- config parsing and unknown-key rejection;
- direction/status enums;
- source-positive claim construction;
- Brier/log-loss fixtures;
- calibration helper edge cases;
- risk/coverage formulas;
- fractional ties;
- macro aggregation;
- `NA` handling;
- evidence-scoping threshold boundary behavior;
- canonical hashing.

### 18.2 Leakage tests

Mandatory:

- package overlap test;
- target-column poison test;
- identity-column poison test;
- test-outcome access test for threshold selection;
- post-hoc indicator filter test.

A leakage test failure blocks every research workflow.

### 18.3 Split tests

Verify:

- each package is outer-test exactly once;
- train/calibration/test are disjoint within each fold;
- row reordering does not change the persisted split identity;
- all methods consume the same split manifest.

### 18.4 Bootstrap tests

Verify package rather than row resampling, deterministic seed behavior, paired method resamples, and known percentile intervals on a small fixture.

### 18.5 Integration tests

Use tiny synthetic tables to validate:

```text
raw-like rows
→ paired claims
→ group split
→ scorer
→ calibration-only operating policy
→ scope decisions
→ metrics
→ manifests
```

### 18.6 End-to-end smoke

One small deterministic smoke workflow validates CLI wiring and artifact lifecycle without requiring the full SELENE dataset.

### 18.7 Local-data contract test

An optional local test runs `validate-selene-contract` against the real external data. It skips with an explicit reason when SELENE is unavailable; it never downloads data.

---

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

`results/` is for chapter-facing evidence only.

Promotion requires:

- source run complete and provenance-valid;
- expected metric schema present;
- no unresolved `NA` affecting the promoted claim;
- confirmatory/exploratory status explicit;
- table/figure generated from exact structured parents.

Recommended promoted structure:

```text
results/
├── tables/
├── figures/
└── evidence_index.json
```

`evidence_index.json` maps each promoted artifact to its exact parent run IDs and source tables. It is lineage metadata, not a software `claim_registry`.

---

## 23. Quality rules

- Keep functions small enough to understand, but do not split code into wrappers with no responsibility.
- Prefer library implementations for standard ML/metrics, backed by local fixtures.
- Keep source/target direction explicit in names and types.
- No `Any`/untyped dictionary interfaces at core scientific boundaries when a typed model is practical.
- Avoid hidden global state and mutable singleton configuration.
- No data work at import time.
- No experiment-specific duplicated metric code.
- No manual scientific values copied into reporting code.
- No generated Markdown research reports.
- No Docker requirement.
- No claim registry.
- No simulated FL clients or IoT abstractions.
- Do not add AI-flavored comments/docstrings; document the scientific reason for non-obvious code, not who wrote it.

---

## 24. Implementation sequence

### Step 1 — Project foundation

Create package/config/CLI skeleton and fast tests.

**Completion condition:** `doctor`, `plan`, and smoke command wiring work without full data.

### Step 2 — SELENE contract

Implement data manifest, schema validation, pairing, package groups, and immutable canonical preparation.

**Completion condition:** `validate-selene-contract` matches the roadmap audit anchors, or any discrepancy is explicitly reconciled.

### Step 3 — Splits and leakage firewall

Implement/persist outer folds, calibration groups, and feature allowlist.

**Completion condition:** all leakage/split tests pass.

### Step 4 — Metrics and baselines

Implement persistence, activity-volume, proper scores, risk-coverage, ties, macro aggregation, bootstrap.

**Completion condition:** all hand-calculated fixtures and permutation tests pass.

### Step 5 — CASE scorer and policy

Implement pooled logistic, secondary per-indicator logistic, the core two-scope decision policy, and optional reporting operating points.

**Completion condition:** no target/test access is possible during threshold selection; calibration-only threshold fixtures pass; unavailable risk targets return an explicit non-error result rather than being silently relaxed.

### Step 6 — Exploratory reproduction

Reproduce historical R5 values and reconcile deviations.

**Completion condition:** no unresolved material difference; corrected historical expectations are documented rather than forced.

### Step 7 — Evaluation freeze

Persist final protocol/config/split identities and the claim-interpretation rules.

**Completion condition:** the Roadmap pre-confirmatory checklist is complete and no outer-test result has influenced the protocol.

### Step 8 — Main evaluation

Run the frozen workflows and bootstrap.

**Completion condition:** OOF predictions and all required metrics validate. Effect size determines claim strength; it does not change the metric definitions or retroactively move operating points.

### Step 9 — Reporting and promotion

Generate only the required tables/figures and evidence lineage.

**Completion condition:** every promoted number traces to validated structured output.

---

## 25. Definition of done

An implementation change is complete only when:

- it has one clear roadmap-backed responsibility;
- scientific behavior matches `Roadmap.md`;
- relevant unit/integration/leakage tests pass;
- generated artifacts carry complete provenance;
- rerunning the same valid inputs is idempotent;
- no dataset or generated output is accidentally staged in Git;
- documentation reflects current behavior, not aspirational behavior;
- no broader claim is introduced through naming or reporting.

---

## 26. Explicit non-goals

Do not build:

- federated-learning orchestration;
- simulated client infrastructure;
- IoT/device abstractions;
- a generic experiment registry framework;
- a generic claims subsystem;
- a database-backed artifact service;
- a web API;
- distributed workers;
- a deep-learning stack;
- automatic dataset download/execution tooling;
- APK/emulator/device execution paths;
- large architecture-enforcement machinery copied from FedIEC.

Reconsider any of these only after a documented roadmap change creates a concrete requirement.

---

## 27. Engineering audit checklist

Before implementation is called ready for confirmatory work:

- [ ] Repository tree remains minimal.
- [ ] One authoritative config surface exists.
- [ ] Raw SELENE data are external and immutable.
- [ ] Dataset/source checksums are persisted.
- [ ] Exact package-grouped split manifests are persisted.
- [ ] Every package is outer-test exactly once.
- [ ] Target leakage poison tests pass.
- [ ] Identity leakage poison tests pass.
- [ ] Threshold selection cannot read outer-test labels.
- [ ] Post-hoc target-based indicator filtering is impossible in the confirmatory workflow.
- [ ] Tie handling is invariant to row order.
- [ ] Package-cluster bootstrap is tested independently.
- [ ] Micro/macro/package aggregation semantics are distinct.
- [ ] Undefined metrics produce typed `NA` reasons.
- [ ] `report` never launches analysis.
- [ ] Artifact reuse checks parent provenance.
- [ ] Stale artifacts cannot be silently promoted.
- [ ] Routine tests remain fast.
- [ ] No full datasets, outputs, or results are tracked by Git.
- [ ] No FL/IoT abstractions have entered the codebase.
