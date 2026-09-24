# What Does a Verification Budget Buy? Repairing Contaminated Client Calibration in Federated Malware Detectors

**Working title (chapter):** *Contaminated Calibration in Collaborative Malware Detection: How Many Verified Labels Restore Client Security, and Where Should They Go?*

**Document role:** research protocol, written before the confirmatory experiment. It fixes domains, contamination scenarios, policies, budgets, metrics, gates and claim wording before confirmatory results are inspected.

---

## 1. Motivation

A malware detector is only as useful as its operating threshold. Deployed detectors, and in particular per-client detectors in a collaborative or federated system, set each client's threshold from a local calibration pool that is *assumed* to be benign: traffic or apps seen locally that no analyst has labelled as malicious. If that pool secretly contains unknown malware, the threshold rises, the false-positive rate stays low and the true-positive rate collapses, silently and unevenly across clients. Clients differ in contamination rate, in how strongly contaminants score, and in how much calibration data they hold, so the damage is heterogeneous. A small, centrally coordinated verification budget (analysts labelling a few calibration items) is a realistic remedy; how far it goes and how it should be spent is unclear.

## 2. Problem Statement

Given K clients, each with a calibration pool that may contain undisclosed malware, and a single global verification budget B (a total number of pool items whose true label is revealed), how much of the security lost to contamination can be recovered, at what label cost, without harming clean clients, and which simple policy is best in which regime?

## 3. Research Gap

Trimming or relabelling contaminated calibration data with a limited labelling budget is studied for single conformal outlier detectors; site-conditional shrinkage of federated thresholds is studied without contamination; federated intrusion detection under contaminated *training* data is studied separately. The combination is unmeasured: heterogeneous contamination across federated clients, one shared verification budget, client-level security constraints (worst-client TPR and FPR), and comparison of simple policies against oracle policies on Android app-market data and IoT device data. The contribution is an empirical study of label efficiency and allocation headroom. No new estimator is claimed unless the gates in Section 27 justify one.

## 4. Research Questions

- **RQ1 (calibration trust).** When can a client trust its own contaminated pool, and how large is the loss in true-positive rate when it does not?
- **RQ2 (peer borrowing).** When does borrowing information from peers (pooled contamination estimates, shrunk thresholds) beat using local information alone?
- **RQ3 (global budget and allocation).** For a fixed total budget B, does allocating labels unevenly (by contamination, adaptively, or by an oracle) beat uniform allocation?
- **RQ4 (label efficiency).** What fraction of the pool must be verified to recover 50%, 80% and 90% of the oracle security, per policy and domain?
- **RQ5 (clean-client safety).** Do repair policies harm clean clients?
- **RQ6 (robustness).** How do conclusions change with contaminant score profile, contamination heterogeneity, pool size, FPR target and domain?

## 5. Hypotheses

- **H1.** Contamination sharply reduces TPR at almost unchanged FPR when contaminants score high or resemble the malware population; stealth contaminants (low-scoring) do little damage.
- **H2.** With very small budgets (well below 1/α verified items per client), pooling verification counts across clients (estimating contamination from all verified items) beats per-client policies.
- **H3.** With larger budgets (about 1/α verified items per client, i.e. 20 at α = 5%, or more), thresholds computed from verified-benign items alone become competitive or best; the crossover is governed by the number of verified items relative to 1/α rather than by the fraction of the pool.
- **H4.** Non-uniform allocation, including oracle allocation, brings little or no gain over uniform allocation at equal total budget.
- **H5.** Repair policies that use estimated contamination do not harm clean clients; global-threshold policies do.
- **H6.** A pool of about 200 items cannot support an FPR target of 1%; conclusions are limited to α ≥ 5% for such pools.

## 6. Expected Contributions

1. A domain-spanning simulation protocol for heterogeneous calibration contamination with a global verification budget and explicit oracle bounds.
2. Label-efficiency curves (budget versus oracle-gap recovery and success rate) for a fixed set of simple policies.
3. A crossover characterisation: which policy is preferable at which budget (verified items per client, relative to 1/α).
4. Evidence on allocation headroom (oracle and adaptive allocation versus uniform).
5. A clean-client safety analysis and boundary conditions (pool size, α).

## 7. Threat Model and Assumptions

- Contamination is **unknown, non-adversarial** or weakly adversarial: contaminants are malware items whose scores come from the client's own malware score distribution (random), its highest-scoring half (top) or its lowest-scoring half (stealth). An adaptive adversary who chooses contaminants after seeing thresholds is out of scope.
- A verification oracle (an analyst) returns the true label of a chosen pool item at unit cost.
- The scorer (a frozen federated detector) is not retrained; only thresholds change.
- Contamination is injected. The public datasets contain no labelled natural calibration contamination (see Section 9); results are claims about the simulation.

## 8. Datasets and Dataset Roles

| Role | Dataset | Clients | Scorer (frozen) |
|---|---|---|---|
| Primary (mobile) | LAMDA + AndroZoo markets | 7 single-market clients (`1mobile`, `PlayDrone`, `angeeks`, `anzhi`, `appchina`, `play`, `slideme`) | supervised FedAvg MLP, score = malware logit |
| IoT replication 1 | N-BaIoT (two split variants: chunked primary, contiguous-tail sensitivity) | 9 devices | federated autoencoder (benign only), reconstruction error |
| IoT replication 2 | Raspberry-Pi crowdsensing malware release (ScienceDB, DOI 10.57760/sciencedb.25380, 32-feature device files) | 8 devices | federated autoencoder, reconstruction error |

Licences: LAMDA MIT; N-BaIoT per dataset description (cite Meidan et al.); ScienceDB record CC BY 4.0 (the associated article is CC BY-NC-ND 4.0 and is cited, derived rows are not redistributed). Only aggregate scores summaries are versioned.

## 9. Dataset Properties and Constraints

- **LAMDA:** benign label = zero VirusTotal detections; the grey zone (1–3) is not in the data, so there is no natural calibration contamination. Nearly half of the rows share an identical feature vector with another row, so splits group on package ∪ feature vector. Market sizes range from 2.5k to 640k apps; small markets limit the benign calibration pool (300–600).
- **N-BaIoT:** unnormalised Kitsune damped-window statistics; no timestamp column but file order is capture order; lag-1 autocorrelation of benign rows reaches 0.8 on some devices, so splits use blocks of consecutive rows. Attack rows exceed 84% of rows per device; benign and malware are separate files. Attack files contain many repeated identical windows (20–40% of a random sample); they are the hard, benign-like windows and are **kept** (the autoencoder never trains on attacks, so duplicates among attack rows do not leak). Benign duplicates are removed before splitting. Per-client AUROC of the federated autoencoder is about 0.61–0.99.
- **Pi devices:** every feature vector appears about five times per file (20% unique); features are globally min–max scaled by the provider; no run, session or time identifier exists, so dependence between windows of one infection run remains and results are optimistic. Two malware conditions on one device share identical windows (label conflict among malware classes only; irrelevant for the binary task).

## 9.1 Client Definition and Deployment Interpretation

- Mobile clients are app markets: each market's security team calibrates a threshold on apps it believes are benign.
- N-BaIoT and Pi clients are individual IoT devices: each device calibrates on its own recent traffic.
- No client is an arbitrary shard: clients are defined by the natural site key of the dataset and differ in prevalence, size and feature distribution.

## 10. Identity and Grouping

- Mobile: component of (package name ∪ feature vector) as split unit; 60/20/20 train / calibration / test.
- N-BaIoT (primary): every file is cut into chunks of 500 consecutive rows; chunks are assigned 60/15/25 to train / calibration / test (benign after order-preserving de-duplication; attack files without de-duplication). Sensitivity: contiguous-tail split (benign first 60/15/25 of the file; attack rows 60–75% calibration, 75–100% test). Scaling statistics come from pooled training rows only.
- Pi: exact duplicate windows collapsed before splitting; random 60/15/25 split; scaling from pooled training rows.
- The calibration pool never overlaps training rows or test rows. Contaminants are drawn from the calibration partition of malware, never from test malware.

## 11. Calibration Pool Construction

Each client's pool has N items (200 for mobile and N-BaIoT; 60 for Pi) drawn **without replacement** from its benign calibration scores, with round(N·ε_c) items replaced by contaminant scores. Sampling that would need replacement is disallowed.

## 12. Experimental Scenarios

- **Contamination profile:** homogeneous ε ∈ {0, 0.05, 0.10, 0.20}; heterogeneous linear 0–0.30 assigned by random client permutation; mobile-only heterogeneous natural: ε_c = 0.3 × client malware prevalence.
- **Contaminant type:** random, top, stealth.
- **Budget:** total B = k·K, k ∈ {0, 2, 5, 10, 20, 40} (Pi: up to 20).
- **Allocation:** uniform; oracle (proportional to ε_c + 0.02); two-stage adaptive (half uniform, remainder proportional to the smoothed observed contamination).
- **FPR target:** α ∈ {0.05, 0.10}; α = 0.01 reported as a limit case.
- **Pool size:** mobile N ∈ {100, 200, 300}; N-BaIoT N ∈ {100, 200, 400, 1000}; Pi N ∈ {30, 60} (supported by the benign calibration counts of the smallest client).
- 30 pool redraws per seed and scenario; ten confirmatory seeds (100–109) that also re-train the frozen scorers.

## 13. Baselines and Policies (fixed in advance)

| Policy | Threshold rule |
|---|---|
| LOCAL | (1−α) quantile of the client's contaminated pool |
| GLOBAL | mean of all clients' LOCAL thresholds |
| CLEAN-K | quantile of the client's verified-benign items (falls back to LOCAL if none) |
| CLEAN-K-SHRINK (w = 0.25 / 0.5 / 0.75) | (1−w)·CLEAN-K + w·mean of clients' CLEAN-K |
| LAB-LOCAL (per-client Label-Trim) | trim the top ε̂_c = m_c/k_c of the pool, then quantile |
| LAB-POOL | ε̂ = Σm/Σk shared by all clients |
| LAB-EB | empirical-Bayes shrinkage of ε̂_c towards the pooled rate, then trim |
| ORACLE-TRUE | quantile of the true clean pool |
| ORACLE-TRIM | trim the true ε_c |

Policies with allocation variants use the same estimators with @oracle or @two-stage label placement. The set is closed; no policy is added after the confirmatory seeds are run.

## 14. Proposed Analysis

The primary analysis is comparative: for each domain, contaminant type and scenario, compare policies by security under the constraints below, and map the regime (verified items per client relative to 1/α, contamination heterogeneity) in which each policy is best. A **crossover rule** (LAB-EB below a verified-item threshold near 1/α per client, CLEAN-K-SHRINK at or above it) is examined only as an exploratory description. It becomes a confirmatory method only if its switching point is computed from calibration-available quantities (verified items per client, α, pool size and estimated contamination), is fixed on development seeds distinct from the confirmatory seeds, and is evaluated once on confirmatory seeds.

## 15. Oracle / Upper Bounds

- ORACLE-TRUE and ORACLE-TRIM (knowledge of contaminant identity / rate).
- Oracle allocation (knowledge of ε_c) for the allocation question.
- Clean-pool LOCAL (ε = 0) as the security ceiling.

## 16. Primary Metrics

- **Success rate** (per client, averaged over clients and draws): FPR ≤ 2α **and** TPR ≥ 0.8 × TPR of ORACLE-TRUE for that client.
- **Oracle-gap recovery of mean TPR**: (TPR_policy − TPR_LOCAL) / (TPR_ORACLE-TRUE − TPR_LOCAL), computed as a ratio of means; reported together with the FPR-deviation recovery based on mean |FPR − α| so that recoveries above 1 achieved by FPR overshoot are visible.

## 17. Secondary Metrics

- Mean TPR, mean FPR, FPR standard deviation across clients.
- Label efficiency: smallest budget at which a policy reaches success ≥ 0.8 and gap recovery ≥ 0.5 / 0.8 / 0.9, reported as verified items per client k, as a fraction of the pool (k/N) and as a multiple of 1/α.
- Allocation efficiency: success gain of an allocation variant over uniform at equal B.
- Contaminated-client recovery (TPR gain over LOCAL for clients with ε > 0.01).

## 18. Worst-Client and Dispersion Metrics

- Worst-client TPR and worst-client FPR (minimum and maximum over clients, averaged over draws).
- FPR dispersion (standard deviation over clients).

## 19. Clean-Client Safety Metrics

- In homogeneous ε = 0 scenarios: TPR and FPR of each policy versus LOCAL.
- In heterogeneous scenarios: FPR and TPR of clients with ε_c ≤ 0.01 versus LOCAL (clean-client harm).

## 20. Statistical Analysis

- Replication unit: seed (10 confirmatory seeds; each seed re-trains the scorer and redraws pools 30 times; within-seed draws are averaged).
- Paired comparisons of policies on identical cells (domain × contaminant type × scenario × budget): mean difference, 95% seed-cluster bootstrap interval (10,000 draws over seeds), and Wilcoxon signed-rank across cells (unit: cell mean over seeds).
- Multiplicity: three primary comparisons per domain (LAB-EB versus CLEAN-K-SHRINK 0.5; LAB-POOL versus CLEAN-K-SHRINK 0.5; oracle allocation versus uniform for LAB-EB), Holm-adjusted; all others exploratory.
- Effect sizes: absolute difference in success rate and in worst-client TPR.

## 21. Ablations

- Shrinkage weight w ∈ {0.25, 0.5, 0.75}.
- Estimator (LAB-LOCAL / LAB-POOL / LAB-EB).
- Allocation rule.
- Frozen scorer quality (supervised vs autoencoder; AUROC of the domain).

## 22. Sensitivity Analyses

- Pool size, α, contaminant type, contamination heterogeneity, budget grid.
- Mobile: package-only grouping versus component grouping.
- N-BaIoT: contiguous-block versus random split.
- Pi: two-fold versus three-fold contaminant support (contaminant pool size).

## 23. Negative Controls

- ε = 0 in every domain: no policy may lose more than 0.02 TPR versus LOCAL if it is claimed clean-safe.
- Contaminant-type contrast: stealth (low-scoring) contaminants must cause much less damage than random and top contaminants; a policy that repairs stealth pools but not top pools is suspect.
- Automatic checks that pool items, calibration rows and test rows are disjoint.

## 24. Robustness Checks

- Pool redraw count 30 versus 100.
- Contaminant pool truncated to the top or bottom quartile.
- Removal of the smallest client in each domain.

## 25. External Replication

The three domains are internal replications of the mechanism (Android app markets versus two IoT device federations). No further dataset is required. Chapter statements distinguish domain-consistent findings (same sign in at least two of three domains) from domain-specific ones.

## 26. Claims

| Claim | Statement |
|---|---|
| C1 | Contaminated calibration pools materially reduce client TPR at nearly unchanged FPR (random and top contaminants) |
| C2 | Stealth contaminants do little damage |
| C3 | Below about 1/α verified items per client, pooled contamination estimates give higher success; at and above it, verified-benign shrinkage does |
| C4 | Allocation beyond uniform gives no reliable gain at equal budget (estimator- and budget-dependent; see G-Allocation) |
| C5 | About 1/α verified items per client (20 at α = 5%) recover most of the oracle security under the best simple policy, independent of pool size in the tested range |
| C6 | Estimated-contamination policies do not harm clean clients; global thresholds do |
| C7 | α = 1% is not supported by pools of the studied size |

## 27. Claim Promotion Gates

| Gate | Requirement |
|---|---|
| G-Failure | LOCAL TPR ≤ 0.6 × ORACLE-TRUE TPR in ≥ 2 of 3 domains for random and top contaminants (contaminated scenarios) |
| G-Headroom | ORACLE-TRUE minus LOCAL TPR ≥ 0.15 in the domain; otherwise the domain is excluded from repair claims |
| G-Baseline | every repair claim is evaluated against CLEAN-K-SHRINK 0.5 and LAB-LOCAL; "best" requires positive paired interval |
| G-Allocation | for the best simple estimator at a given budget, oracle or adaptive allocation improves success by ≥ 0.10 over uniform in ≥ 2 domains; otherwise C4 is promoted and the allocation line is closed. An adaptive rule that passes is confirmed on confirmatory seeds before promotion |
| G-Clean | clean-client TPR loss ≤ 0.02 and FPR change ≤ 0.02 versus LOCAL |
| G-Domain | same-sign conclusions in ≥ 2 of 3 domains for C3 and C5, and crossover budget within a factor of two across pool sizes |
| G-Complexity | a new estimator (including the crossover rule) is promoted only if it beats the best simple policy in success rate with positive paired interval in ≥ 2 domains and does not lose worst-client TPR by more than 0.02 |
| G-Validity | leakage assertions pass; pools drawn without replacement; realised support adequate |

Structural failures block the affected domain or experiment. A weak effect narrows the claim (for example "budgets above 5% only"). If no policy beats CLEAN-K-SHRINK in ≥ 2 domains the chapter reports the label-efficiency study without a method claim. Allowed wording: "in the simulated contamination scenarios", "in the tested domains". Forbidden wording: "first", "novel", "guarantee", any claim about natural contamination rates, adaptive adversaries or real-world deployment.

## 28. Reproducibility

- `c3_scores.py DOMAIN SEEDS` trains the frozen scorers and writes score arrays (no raw rows); `c3_budget.py DOMAIN SEEDS [--alpha A] [--pool N]` runs the simulations; `c3_analyze.py DOMAIN ALPHA N` prints the analysis tables; `audit_c3.py` re-derives all dataset facts.
- Data caches come from `CASE_RAW` / `CASE_CACHE`; ScienceDB files are fetched by file id with size and SHA-256 verification.
- Seeds fixed; JSON outputs contain all per-client metrics.

## 29. Compute Plan

Scorer training: LAMDA about two minutes per seed on GPU; N-BaIoT and Pi about one minute per seed. The N-BaIoT cache build reads about 9 GB of CSV once (about fifteen minutes). Budget simulations take seconds to minutes per domain and seed on CPU. No special hardware.

## 30. Expected Figures

1. TPR and FPR of LOCAL versus ORACLE under contamination, by contaminant type.
2. Label-efficiency curves: oracle-gap recovery and success versus verified items per client for each policy.
3. Crossover figure: best policy by verified items per client and domain.
4. Allocation headroom: uniform versus adaptive versus oracle at equal budget.
5. Clean-client safety panel.
6. Sensitivity to pool size and α.

## 31. Expected Tables

1. Domain, client and pool summary.
2. Policy comparison at k = 5, 10, 20 (success, worst-client TPR and FPR, recovery).
3. Label budget required for 50/80/90% recovery.
4. Paired comparison table with intervals and Holm-adjusted p-values.
5. Gate outcomes.

## 32. Limitations

- Contamination is injected; natural contamination rates and score profiles are unknown.
- Score-level simulation with frozen scorers; retraining with contaminated data is not studied.
- Pi results are optimistic because dependence within infection runs cannot be removed.
- N-BaIoT scorer saturation limits the effect of thresholds on discrimination.
- Small pools limit the resolution of low FPR targets.
- Threshold rules are quantile-based; conformal guarantees are not claimed.

## 33. Threats to Validity

- **Construct:** contaminants drawn from the labelled malware calibration partition are assumed representative of undetected malware; real undetected malware may be harder.
- **Internal:** verification oracle is perfect; allocation of the same labels in policies changes which items are verified; controlled by shared random draws.
- **Statistical:** seeds as replication units; correlated contamination cells; Holm for primary contrasts only.
- **External:** three domains, simulated clients.

## 34. Ethical and Security Considerations

Public data only. The analysis explains how calibration contamination degrades detectors and how verification helps; it does not describe how to construct contaminants that evade a deployed system beyond the generic notion of "stealth" score profiles used for simulation.

## 35. Chapter Structure

1. Motivation: thresholds in collaborative malware detection.
2. Related work.
3. Simulation protocol, domains and policies.
4. Failure: what contamination costs.
5. What a verification budget buys: label efficiency, crossover, allocation.
6. Clean-client safety and robustness.
7. Discussion: implications for federated deployments and limits.

## 36. Execution Order

1. Verify licences, hashes and support; run leakage assertions.
2. Train frozen scorers for the confirmatory seeds.
3. Failure and headroom checks (G-Failure, G-Headroom).
4. Policy comparison, allocation and clean-client experiments.
5. Sensitivities and controls.
6. Gate evaluation and write-up.

## 37. Completion Criteria

- All three domains run for ten confirmatory seeds; validity gates pass.
- Every claim has a gate outcome; the crossover rule is labelled exploratory unless G-Complexity passes.
- Tables and figures regenerate from the scripts.
