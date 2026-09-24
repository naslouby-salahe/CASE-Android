# Research Summary — Three Book-Chapter Candidates (2026-09-24)

Scope: the three candidates in `docs/Candidate 1/`, `docs/Candidate 2/`, `docs/Candidate 3/`. Each folder has a clean protocol (`Roadmap.md`), an evidence dossier (`Candidate Report.md`) and runnable scripts (`poc/`; the exploratory versions are under `poc/legacy/`). The earlier exploratory workspace `docs/poc/` and the original CASE roadmap `docs/Roadmap.md` are preserved unchanged; contradictions between old and new findings are logged in each report (Section 9).

## 1. What the candidates are

| | Candidate 1 | Candidate 2 | Candidate 3 |
|---|---|---|---|
| Title | Complementary threat knowledge in federated Android malware detection: controlled-exposure decomposition | CASE-Android: reliability-qualified scoping of recorded Android evidence across execution contexts | What does a verification budget buy? Repairing contaminated client calibration in collaborative malware detectors |
| Type of contribution | empirical / measurement | measurement + operational protocol + negative result | empirical / operational |
| Datasets | LAMDA + AndroZoo (4 simulated market clients) | SELENE (Android 10 ↔ 14, 30,746 pairs); KronoDroid (emulator ↔ device, 63,316 pairs) | LAMDA markets (7), N-BaIoT (9 devices), Raspberry-Pi ScienceDB release (8 devices) |
| New method claimed | none | none | none |

## 2. Comparison

| Dimension | Candidate 1 | Candidate 2 | Candidate 3 |
|---|---|---|---|
| Chapter fit | Strong: Android malware, data-local collaboration | Strongest: Android dynamic-analysis reporting, cross-context reliability | Medium: mobile is the primary domain but the topic is detector calibration, not app privacy |
| PhD relevance | Strong (collaboration value, non-IID clients, scarce evidence, worst client, when collaboration helps); not IoT | Partial, by analogy (heterogeneity, reliability, calibration, thresholds, worst group, pooling vs per-group scope); not FL, not IoT | Strong (calibration and client thresholds, contamination, worst-client TPR/FPR, scarce labels); IoT replication in two IoT device corpora |
| Novelty confidence | Moderate-low: direct collisions on "FL helps clients with missing families" (2026) and prototype exchange | Moderate-low: cross-device studies, selective conformal risk control, an Android conformal filtering paper; SELENE/ARTEMIS papers unread | Low-moderate: Label-Trim (ICML 2025), site-conditional federated shrinkage (2026), retained-law trimming (2026) |
| Dataset readiness | High; split leakage found and fixed (45% duplicate vectors); AVClass2 semantics documented | High; two datasets audited and paired; family label newly found in SELENE; earlier Krono family finding corrected; no repeated runs, no execution timestamps | High for three domains; one earlier error found and fixed (N-BaIoT attack de-duplication); contamination must be injected |
| Existing evidence | 5 seeds main; dose (5 seeds), natural axis (5), linear (3), family set 2 (3), package-only (3), GBDT (5), own-market (5), permuted-family control (3; complementary +.003, null) | 3 salts probability quality, scoping, transfer; calibration, exposure-normalisation and redundancy checks (1 salt); 2 salts KronoDroid | 5 seeds × 3 domains × contaminant types × profiles × budgets × 2 α; pool-size sensitivities |
| Oracle / headroom | Oracle gap recovered 69–89% by simple arms; residual .03–.08 mean recall (below the 0.10 trigger): no mechanism headroom | Boosted comparator roughly doubles logistic Brier skill (17% / 10% vs 9% / 4%); headroom for better scorers, not for a new policy | Repair headroom large (LOCAL TPR ≈ 43–49% of oracle); allocation headroom absent (oracle allocation lowers success in all domains) |
| Added value | Quantifies that most collaborative benefit is generic pooling (complementary share 30–42%, ≈ 0 for a second family set; large only where the client holds a few samples); dose-response; 7 of 16 families irreducible | Calibrated scoping with stated risk and coverage; worst-indicator/worst-family risk 4–5× the pooled target; about 1,000 verified target claims for a reliable threshold; no cross-direction transfer | Label-efficiency and crossover at ≈ 1/α verified items per client in three domains; pooled trimming harms clean clients (FPR .14–.23 vs .05); no allocation gain |
| Implementation burden | Low (GPU minutes per seed) | Medium (CPU hours; two datasets) | Low–medium (three scorers; N-BaIoT cache reads 9 GB once) |
| Replication strength | Internal only: second scorer, second family set (fails), natural axis, leakage sensitivity; no external corpus | Best: a second dataset with a different ontology replicates the main qualitative results | Good internal replication: three domains; no natural contamination data |
| Main scientific risk | Small complementary component, unstable across family sets; "unseen family" partly "seen behaviour" (adware families share features) | Two context pairs; PhD link by analogy; logistic gain modest and beaten by a metadata baseline in one direction | Injected contamination only; crossover may not survive natural contamination; novelty collision |
| Main implementation risk | Confirmatory seeds not run; AndroZoo access for cache building | Confirmatory salts not run; SELENE paper and table configs unread | Pi dependence within infection runs cannot be removed; α = 1% unsupported |
| Overall readiness | Ready to run confirmatory seeds; claims already narrowed | Ready; protocol most complete; needs literature closure on two papers | Ready; policy set frozen; needs literature closure on Label-Trim distinction |

## 3. Status of the decision

No candidate is clearly ahead, so no final chapter is chosen here.

- If **PhD relevance and chapter fit together** decide: Candidate 1 is the most balanced, but its central effect is the weakest and least stable.
- If **robustness of the measured effects and replication** decide: Candidate 2 is strongest, at the cost of a PhD link that is an analogy.
- If **PhD relevance with the most robust cross-domain effect** decides: Candidate 3, at the cost of a lower chapter fit and the most collided literature.

Questions that would settle the choice:

1. How much weight does the chapter's mobile-privacy focus receive relative to the thesis link? (Candidate 2 above 3 above 1 for fit; the reverse for the thesis link.)
2. Is an empirical decomposition whose main component is small acceptable as a headline (Candidate 1), or must the headline effect be larger (Candidates 2 and 3)?
3. Can the two literature checks (SELENE/ARTEMIS papers for Candidate 2; the 2026 Cybersecurity federated missing-malware paper for Candidate 1) be closed without a collision?

Infrastructure overlaps: Candidates 1 and 3 share the LAMDA cache and split code; a combined chapter (Candidate 1 as the main study, Candidate 3 as its calibration section, following the archived recommendation) is technically cheap but not evaluated here.

## 4. Old findings overturned or corrected during this audit

| Earlier statement | Now | Where |
|---|---|---|
| KronoDroid family labels disagree on 33,838 pairs and are unusable | artefact of comparing missing values; 1,200 of 30,678 labelled pairs disagree (3.9%) | Candidate 2 report, 2.2 and 9 |
| SELENE offers no family structure | `family` field present, identical across contexts | Candidate 2 report, 2.1 and 9 |
| A simple logistic ladder is sufficient for CASE | boosted comparator roughly doubles the gain; a metadata-only baseline is competitive in one direction | Candidate 2 report, 3 and 9 |
| Complementary knowledge ≈ .075–.098 mean recall (P60) | .065 / .067 with leakage-hardened, size-matched controls; .006 for a second family set | Candidate 1 report, 3 and 9 |
| LAMDA has no singleton family labels | 40.7% of malware rows carry `singleton:<sha256>` | Candidate 1 report, 2 and 9 |
| N-BaIoT generic evaluation saturates | only after de-duplicating attack rows, which removes the hard windows; with them kept AUROC is .61–.99 | Candidate 3 report, 3 and 9 |
| Clean clients are not harmed by estimated-contamination policies | true only for homogeneous ε = 0; pooled estimators raise clean-client FPR to .14–.23 under heterogeneous contamination | Candidate 3 report, 3 and 9 |
| No duplicate group spans two labels (Pi data) | device 7 has 480 vectors shared by two malware conditions | Candidate 3 report, 2.3 and 9 |
| Pool of 60–200 items sampled with replacement | without replacement, with support assertions | Candidate 3 report, 9 |

## 5. Not done and why

- No confirmatory (frozen-protocol) run was executed; seeds 100–109 and salts 100–104 are reserved.
- Literature searches are targeted, not systematic. Two full texts (Cybersecurity 2026 missing-malware FL; SELENE/ARTEMIS papers) were not read.
- A clean-environment reinstall of the software stack was not performed; scripts use path variables and fixed seeds, and were run from the repository state.
- No unit-test suite exists; correctness relies on the assertion modes (`c1_study.py check`, `c2_selene.py check`, assertions inside `c3_scores.py`).
