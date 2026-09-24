# Research Matrix

> **SUPERSEDED RULES (Phase 6 consolidation, 2026-09-24).** The following earlier rules are void wherever they appear below; the scientific measurements they gated are kept.
> - Requirement of *natural data owners*, *real hardware*, or *one linked Android+IoT dataset* (G-PHD-4, G-PHD v1/v2 "hard conjunction", "NO ELIGIBLE PROJECT" verdicts). Replaced by: simulated, deployment-motivated clients on public data are acceptable (no arbitrary APK shards); PhD relevance = clear link to >=1 thesis theme, used as a hard *filter* not a conjunction.
> - Verdicts "NO STRONG CANDIDATE" (Phase 5) and "no winner" — superseded by the Phase 6 classification in `Final Report.md`.
> - G-MECH/G-NOVEL remain in force as evidence standards.

## PHASE 6 — candidate register under corrected rules (2026-09-24)

PhD-relevance filter: clear link to >=1 thesis theme (heterogeneity/non-IID clients, collaboration vs personalization vs local, calibration/thresholds, reliability of local evidence, negative transfer, contamination/robustness, worst-client, drift, cold start, privacy). Ranking after filter: chapter fit > added value > working mechanism > novelty > feasibility > reproducibility. Staged POC: Failure -> Oracle/headroom -> Strong simple baseline -> Minimal mechanism -> Stability (1-3 seeds discovery, 5 finalists).

| ID | Candidate | PhD themes | Stage reached | Result | Verdict |
|---|---|---|---|---|---|
| A01/P2/P61 | CASE-Android recorded-claim recurrence + calibrated scoping | heterogeneity, calibration/thresholds, worst-group reliability (analogy) | 1-3 (5 seeds, both directions) | Brier skill 4-10% vs persistence; risk targets met; coverage +3.7/+7.0 pts at equal risk; pooled worst-indicator risk .21 vs .06 per-indicator | TOP TIER (component) |
| P60 | B: complementary threat knowledge / unseen-family asymmetry, Android clients | collaboration vs local, cold start/scarce, non-IID, worst-client, negative transfer | 1-3 (5 seeds; +nofam control) | local unseen recall .49 / worst .28; FedAvg-FT .68/.43; central .70/.38; oracle .745/.47; complementary-knowledge part +.075-.10 mean, +.11 worst | TOP TIER / needs replication POC |
| P59 | C: contaminated federated calibration + verification budget | contamination, calibration, scarce labels, worst-client, robustness | 1-5 | CLEAN-K-SHRINK ties/beats estimator; ~10 verified labels ~ oracle mean TPR | TOP TIER only as component |
| P62 | Membership inference on federated Android detectors | privacy | 1 | MIA AUC .48-.58 (no leakage) | REJECT |
| P63 | VirusTotal grey-zone / label delay as verification cost | unreliable labels, scarce verification | not run | collisions MalWhiteout (ASE'22), Mitigating Emergent Malware Label Noise (PACM SE 2025), ActDroid | NEEDS ONE MORE POC (low priority) |
| P64 | Cold-start client via peer transfer / routing (P37-P48) | cold start, personalization | 1-3 | fixed blend ~ central | REJECT |
| P65 | Which peers to trust for a family (peer selection) | negative transfer, personalization | not run | only worth it if B replication leaves >.10 oracle gap | NEEDS ONE MORE POC (conditional) |
| P66 | Federated class-incremental novel-attack detection | unseen classes | not run | EdgeFedCIL 2026; rare-class federated transfer 2025 | REJECT (collision; B shows FedAvg-FT suffices) |
| P67 | Robust aggregation vs honest heterogeneity (P44) | robustness, heterogeneity | 1-3 | no headroom | REJECT |
| P68 | Drift vs stable heterogeneity (P38) | drift | 1-3 | self-referenced detector suffices | REJECT |
| P69 | Client-level thresholds on app markets (P26/P52) | thresholds, worst-client | 1-4 | is DATP | REJECT |
| P70 | Paired-context FL KronoDroid (P11) | context heterogeneity | 1-3 | local > FedAvg, K=2 | REJECT |
| P71 | Mobile/IoT interaction | cross-domain | 0 | no linked data | REJECT |

Additional CASE assessment: CASE alone is a strong mobile-security chapter (best fit, defensible bounded novelty, modest results); its PhD link is by analogy. The P61 extension (pooled vs per-indicator calibrated thresholds, worst-indicator risk) reproduces the scope/worst-group trade-off of the thesis on a second object without inventing clients. Not rejected for being non-federated; not forced into FL.



---

## Research Matrix (Phases 1-5)

*Source: `poc/Research Matrix.md` (merged 2026-09-24). *

### CASE-Android Research Matrix

Audit date: 2026-09-23. This matrix extends the existing SELENE/KronoDroid feasibility work to the full research and FL formulation space requested for this audit. No authoritative roadmap was edited. Literature coverage is a targeted collision audit, not a systematic review.

#### Decision rule

The most highly aligned candidate must also have valid data and a distinct research question. An Android package, APK, Android version, dataset row, or synthetic partition is not an FL client unless there is a defensible participant/data-ownership unit. A useful predictive association is not itself a contribution if a recent paper already solves the same operational question.

#### A. Core scientific formulations

| ID | Formulation | CASE relation / FL role | Closest collisions and residual question | Data, minimum POC, baseline | Verdict |
|---|---|---|---|---|---|
| A01 | Original claim portability | CASE core; FL unnecessary | Context-dependent Android behavior and emulator/device inconsistency are established. Narrow residual: prospective source-only recurrence of a processed source-positive claim, followed by report scoping. | SELENE exact SHA pairs; already tested persistence vs pooled logistic, both directions, grouped splits, broken-pair control. | **PROMOTE, bounded.** |
| A02 | Federated claim-portability learning | CASE plus cross-silo collaboration | Ordinary malware FL and Android FL are established; no close paper found on this exact claim-level outcome, but absence is not evidence of novelty. Residual requires separate custodians who hold compatible paired source-target claim data. | No such clients in SELENE/KronoDroid. Tinyest valid POC is client/data inventory, not synthetic FedAvg. Compare central, local-only, FedAvg/FedProx only after client access. | **BLOCKED_GROUPING / BLOCKED_IDENTITY.** |
| A03 | Reliability-aware federated malware detection | Reliability becomes evidence-level input | FL-MalDrift (2025), M2FD (2025), ADAM personalization/FL (2023), 2026 DCAA aggregation, and Droidware (2026 online) collide with generic reliability/robustness-aware detection. Residual requires reliability evidence measured independently of client accuracy/drift. | No natural compatible participants. A source-context-only scoring POC exists in SELENE but has no malware-detection or federation label. | **DEFER; do not claim as CASE result.** |
| A04 | Portability-weighted FL aggregation | CASE reliability influences update weights | Direct collision: drift/client/reliability adaptive aggregation is now proposed for malware FL (DCAA, 2026); FL-MalDrift gates participation using local drift. A new weight from measured claim portability would be incremental only if it beats those on held-out natural clients. | Missing client records and no local update validity labels. A synthetic test would not resolve the collision or naturalness. | **REJECT as current contribution; revisit only with a distinct real dataset.** |
| A05 | Personalized FL by execution context | Shared model + context-specific heads | ADAM (2023) combines cross-smartphone adaptation, personalization and FL; AndroIDS (2025) reports personalized privacy-preserving Android syscall FL. Residual could be worst-context improvement with held-out device/context evaluation. | SELENE has two contexts but no clients and severe context-client confounding. Do not split APKs into artificial clients. | **BLOCKED_GROUPING; keep as future extension.** |
| A06 | Clustered FL by behavioral context | Group compatible data owners | Clustered FL is established in heterogeneous IoT. CASE could add measured claim-level compatibility, but no multiple owners exist. | No client count/support; clustering two environments is not a federation. Baseline would be FedAvg and global/local context model. | **REJECT for current data.** |
| A07 | Federated domain adaptation | Adapt shared detector between observed source/target domains | Domain adaptation and federated adaptation are mature; Android FL applications are already numerous. Domain labels alone do not make contexts into clients. | No independent unlabeled target-owner data or distribution-preserving client collection. | **DEFER.** |
| A08 | Federated domain generalization | Train across observed environments for unseen context | Federated domain generalization is an established broad field; credible novelty would need a prospective held-out natural context plus relevant malware task. SELENE has only two named contexts; Krono two acquisition modes. | No third independent context family with aligned labels. Baseline client/global/local domain models cannot test unseen context here. | **BLOCKED_SUPPORT / BLOCKED_GROUPING.** |
| A09 | Federated selective malware detection | Shared detector can abstain/context-scope | Selective classification, calibration and federated conformal methods are established. Residual would be group/shift-valid selective malware claims, not abstention alone. | SELENE target is observation recurrence, not malware verdict; cannot transfer a classifier policy claim. Calibration diagnostics exist but are retrospective. | **Keep selective scoping in A01 only; no FL claim.** |
| A10 | Reliability-qualified collaborative threat intelligence | Share reliability summaries, not raw evidence | Collaborative threat intelligence and privacy-preserving exchange predate this audit. Distinctive residual: interoperable, evidence-level portability summaries with provenance and explicit context scope; no compatible real partners currently available. | Requires 3+ independent security labs/sandbox providers and shared claim ontology; dataset inventory fails this prerequisite. | **Strong conceptual bridge; BLOCKED_ACCESS / BLOCKED_GROUPING.** |
| A11 | Context-conditioned collaborative detection | Detector conditions on execution context | Context-conditioned classification is established; context metadata risks learning dataset/process shortcuts. No context-cardinal support for robustness. | SELENE permits context-stratified recurrence but the target context is the label domain, not a learned client feature. | **Merge with A01 descriptive stratification; reject as standalone.** |
| A12 | Multi-level reliability architecture | Observation quality → feature portability → detector uncertainty → report reliability | Each layer is separately familiar; a four-stage stack risks complexity-by-decoration. CASE has direct evidence only for recorded claim recurrence and a retrospective report proxy. | Existing fidelity sample (56 shared IDs), recurrence model, and report proxy. No independent observation-truth or calibrated deployment policy. | **Narrow to claim recurrence + report proxy; defer other layers.** |

#### B. Federated-learning design formulations

| ID | Design | Required comparison / client validity | Evidence and disposition |
|---|---|---|---|
| B01 | FedAvg | Natural clients, central and local-only baselines; report per-client metrics | Generic Android FL is established; no natural multi-owner client table in current artifacts. **BLOCKED_GROUPING.** |
| B02 | FedProx / heterogeneity optimization | Same clients/splits as FedAvg and a non-IID rationale | Standard optimizer baseline, not novelty. Two SELENE contexts are insufficient clients. **DEFER.** |
| B03 | Personalized local heads | Show worst-client gain against global and local models | Smartphone malware personalization already appears in ADAM; AndroIDS reports personalization. **High collision; no valid clients.** |
| B04 | Shared representation + context head | Must demonstrate context support beyond a global/context-local model | SELENE can compare named contexts descriptively but has no per-client train rounds. **Not an FL design without owners.** |
| B05 | Local calibration, global detector | Calibration data and target clients must be local, disjoint and exchangeable enough for stated claims | No federation; FL conformal/calibration methods already exist. **Defer.** |
| B06 | Context-similarity clustered FL | Learn clusters on train clients only; compare arbitrary and context-informed grouping | Two environments cannot yield valid group discovery; high risk of inventing clusters. **Reject.** |
| B07 | Portability/reliability-weighted aggregation | Portability score must be independently estimated, temporally available, privacy-compatible, and outperform sample-count, FedProx and drift-aware baselines | Direct 2026 collision with reliability/drift aggregation; no update-level clients. **Reject as current lane.** |
| B08 | Reliability-aware participant selection | Measure excluded-client harm and coverage/utility, not only global accuracy | FL-MalDrift already gates participation based on drift; no natural SELENE clients. **Defer/high collision.** |
| B09 | Federated prototype exchange | Compare full-model FL, local-only and leakage/utility of prototypes | Prototype sharing is established; no reason to exchange claim prototypes between two context labels from one corpus. **Reject.** |
| B10 | Federated distillation / evidence summaries | Specify what summary is private, what leakage remains and what decision it improves | Generic distillation and threat-intelligence exchange are mature; no multi-owner evidence table. **Defer.** |
| B11 | Cross-silo lab/SOC/sandbox clients | Name actual custodians, data rights, harmonized claim definition, client count, and held-out organization evaluation | No organizations/participants or authorized raw datasets identified. **BLOCKED_ACCESS / BLOCKED_GROUPING.** |
| B12 | Vertical / partial-feature FL | Distinct participants must hold complementary modalities for the same APK/decision and have aligned identity/label linkage | SELENE provides modalities centrally in one artifact; no separately owned feature parties. Shared hashes do not create feature-owning silos. **BLOCKED_IDENTITY / BLOCKED_GROUPING.** |

##### B-design conclusion

None of B01–B12 is promoted. This is a structural data/participant constraint, not a failed optimizer experiment. Running FedAvg on APK partitions or treating Android 10 and Android 14 as two clients would fabricate a participant model, put shared APK identities across sites, and leave the real question unanswered. A valid federation requires independent data custodians or actual heterogeneous endpoints, valid partition provenance, and a decision that collaboration changes. No secure aggregation/privacy mechanism can repair a false client definition.

#### C. Direct comparison of project identities

| ID | Project identity | Scientific need / distinctive contribution | Closest collision | Available data / result that would matter | FL natural? / PhD / chapter | PHD class | Decision |
|---|---|---|---|---|---|---|
| P1 | Original CASE | Whether a source-positive recorded claim should be generalized to a named target context | Context dependence and cross-device behavior; narrow report-level recurrence remains | SELENE exact pairs; modest, repeated source-only Brier gains and successful pairing control | No / medium-low / high | **PHD_INELIGIBLE** | CASE-only component; not final project. |
| P2 | Enlarged non-FL CASE | Add source evidence strength, four-state transitions and independent context replication | Same collision, but richer contribution evidence | SELENE count ladder; Krono exact-pair descriptive replication; no event-level SELENE layer | No / medium / high | **PHD_INELIGIBLE** | Prior weighted winner withdrawn; component only. |
| P3 | Federated claim-portability CASE | Collaborative learning of claim recurrence across data custodians | Android malware FL and reliability/transfer fields; exact claim-scoping collision not found | No natural clients; would need external custodians with paired claim data | Potentially / high if validated / high | **PHD_PARTIAL** | Blocked; not runner-up. |
| P4 | Reliability-aware federated malware detection | Decide which behavior evidence contributes to collaboration | FL-MalDrift, M2FD, recent drift/reliability-weighted aggregation | No owner clients; CASE observations are not malware labels | Artificial on current data / high / medium | **PHD_PARTIAL** | Reject as current project. |
| P5 | Personalized FL by execution context | Share common malware patterns while preserving device/context specificity | ADAM (2023), AndroIDS (2025), personalization literature | Only two bundled contexts; no clients or meaningful worst-client groups | Artificial / high / medium-high | **PHD_PARTIAL** | Defer. |
| P6 | Reliability-aware aggregation | Let portable evidence drive aggregation weight | 2026 DCAA reliability/drift-aware aggregation; drift participation gating in FL-MalDrift | No update/reliability labels across real clients; incremental-vs-direct collision unresolved | Potential on real client data / high / medium | **PHD_PARTIAL** | Reject absent distinct data/question. |
| P7 | Federated domain-generalized malware detection | Generalize from multiple owner domains to an unseen one | FDG methods broadly mature; mobile malware FL and drift work now overlap | No third context; target split would be context confounded | Could be natural with partners / high / medium | **PHD_PARTIAL** | Blocked support. |
| P8 | Federated selective/calibrated malware detection | Make collaborative outputs uncertainty qualified | Federated conformal/calibration research; Android FL collision | CASE lacks malware classification outcome and federation; calibration is only retrospective | No / high if actual thesis setting / high | **PHD_PARTIAL** | Merge policy question into CASE component; no FL. |
| P9 | Cross-silo threat intelligence / cross-silo CASE | Exchange scoped evidence/reliability summaries among security holders | Existing CTI and collaborative malware FL | Needs actual SOC/lab/sandbox partners and common claim ontology; none available | Natural in principle / high / high | **PHD_PARTIAL** | Strategic future direction; blocked access. |
| P10 | Hybrid portability + FL + personalization | Combine all layers | Stacks multiple crowded components and inherits missing clients | No data can identify each component contribution | No with present artifacts / high / medium-high | **PHD_PARTIAL** | Reject as artificial complexity. |

#### D. Superseded unconstrained scorecard (not a project-selection rule)

This scorecard predates hard G-PHD and is retained only for audit traceability. Its unconstrained numerical ordering **must not be used** to select a project; a PHD_INELIGIBLE or PHD_PARTIAL candidate cannot be rescued by weighted scoring. Raw scores (0–5; high collision and complexity scores are penalties) used: `.20 novelty + .20 PhD + .15 added value + .10 book + .10 feasibility + .10 data + .05 result + .05 external + .05 reproducibility`, then subtract `.25 × complexity` and `.25 × collision`.

| ID | Novelty | PhD | Book | Added value | Feas. | Dataset | Natural FL | Result | External | Repro. | Complexity penalty | Collision penalty | Weighted net* | Fatal issue |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| P1 | 3 | 2 | 4 | 3 | 5 | 4 | 0 | 3 | 2 | 4 | 1 | 2 | 2.45 | PhD result is only methodological analogy |
| P2 | 3 | 3 | 4 | 4 | 4 | 4 | 0 | 4 | 3 | 4 | 1 | 2 | 2.80 (superseded) | PHD_INELIGIBLE; limited to recorded-evidence datasets |
| P3 | 3 | 5 | 4 | 4 | 1 | 1 | 3* | 2 | 3 | 2 | 3 | 3 | 1.65 | No natural clients |
| P4 | 2 | 5 | 3 | 3 | 1 | 1 | 2* | 3 | 2 | 2 | 4 | 4 | 0.70 | No compatible owner data; close collisions |
| P5 | 2 | 5 | 4 | 3 | 1 | 2 | 2* | 3 | 2 | 2 | 3 | 3 | 1.40 | Only two contexts; personalization collision |
| P6 | 2 | 5 | 3 | 3 | 1 | 1 | 2* | 2 | 2 | 2 | 4 | 5 | 0.40 | Direct 2026 aggregation collision |
| P7 | 2 | 5 | 3 | 3 | 1 | 2 | 2* | 2 | 2 | 2 | 4 | 3 | 1.00 | No unseen aligned context |
| P8 | 2 | 5 | 3 | 5 | 1 | 1 | 1 | 2 | 2 | 2 | 3 | 4 | 1.10 | Wrong outcome/data for classifier calibration |
| P9 | 3 | 5 | 4 | 5 | 0 | 1 | 4* | 2 | 5 | 1 | 3 | 3 | 1.70 | Access and ontology unavailable |
| P10 | 1 | 5 | 2 | 4 | 0 | 1 | 1 | 1 | 1 | 1 | 5 | 5 | -0.35 | Multiple fatal design constraints |

* Natural-FL scores with an asterisk mean natural in an appropriate future setting, not supported by current data. The score does not waive the fatal issue. CASE earns book-fit **4/5** because the empirical contribution sits on the mobile application security/reporting side of the call, but it does not supply a privacy-enhancing learning method; privacy is addressed through bounded data handling and provenance only. Weighted net is a decision aid, not a scientific result; ordinal scoring uncertainty is substantial.

#### E. Stronger PhD-alignment challenger: IoT crowdsensing malware data

A newly published 2026 *Scientific Data* descriptor releases 342,106 30-second windows from eight Raspberry Pi 3/4 devices, 32 selected features plus a 687-dimensional processed representation and raw logs, collected over 288 hours for benign conditions and eight malware attack scenarios. It explicitly organizes files by device, and its paper already compares centralized FL and decentralized FL, topologies and data distributions. This supplies a more natural **device-level** client key than Android APK datasets, but the eight devices were one controlled testbed rather than independent organizational owners, and the release paper already establishes its core DFL benchmark result. The label/task is IoT malware behavior, not Android app privacy or report scoping. Global min-max normalization and repeated windows also require split/leakage scrutiny. Treat as a strong PhD dataset lead, not as a replacement chapter project without a narrower collision-tested question. See the current [dataset paper](https://www.nature.com/articles/s41597-026-07155-w) and [associated data](https://pmc.ncbi.nlm.nih.gov/articles/PMC13219454/).

The Science Data Bank index reports 331,750,002,920 bytes overall (the page description says 308.1 GB, an apparent unit/display discrepancy); only the smaller 32-feature processed subset is relevant to a first POC, but the folder manifest and subset size were not retrieved. The dataset record lists CC BY 4.0 while the article is CC BY-NC-ND 4.0. The descriptor says attack behaviors are repeatedly triggered with scripts, so label meaning needs verification before claims about real-world malware-family generalization. Do not download the full collection to resolve these open questions.

N-BaIoT also has naturally device-indexed traffic and existing federated IoT malware studies; ToN-IoT includes multiple lab/testbed sources and attack telemetry but not Android-app behavioral reports. Both can support a separate IoT-PhD experiment, not the mobile-app book chapter’s main estimand. Neither provides evidence that the Android CASE formulation itself becomes federated.

#### F. Hard PhD eligibility gate and final decision

The supplied requirement changes the decision rule: a final choice must directly and empirically strengthen collaborative malware detection using FL in heterogeneous IoT networks **and** fit a mobile-application privacy/security chapter. P1 and P2 fail the first condition and are **PHD_INELIGIBLE** as final projects. A conceptual analogy, generic book fit, or post-hoc dissertation implication does not pass. “Eligible” also requires a defensible client construction, malware outcome, heterogeneous network/device setting, privacy/security relevance, valid splits, and an experiment against central/local/FedAvg/FedProx. Deployment-motivated simulated clients can qualify for an early study when their boundaries map to real operating domains; arbitrary APK shards do not.

The audit found no candidate that passes every condition. The closest practical mobile candidate is P11, with emulator and physical-device acquisition contexts used as two simulated clients over exact paired APKs. Its 1–3 seed CPU POC finds severe cross-context transfer failure, but local models outperform FedAvg/FedProx, only two dependent contexts exist, and no IoT network, independent owners, or privacy mechanism is evaluated. It is **PHD_PARTIAL**, not eligible. The device-indexed 2026 IoT malware corpus better fits the dissertation topic, but it is not a mobile-app privacy/security study and its broad decentralized-learning benchmark is already published. It is also **PHD_PARTIAL**.

##### P11–P25 candidate register

| ID | Candidate | Evidence/data route and decisive issue | PHD class | Disposition |
|---|---|---|---|---|
| P11 | Federated Android malware detection under paired emulator/device execution-context shift, with cross-context portability and local calibration diagnostics | KronoDroid supplies 63,316 exact paired APKs and 288 syscall counts; only two simulated context clients. POC is below; no IoT-network or independent-owner evidence. | **PHD_PARTIAL** | Strongest runnable mobile-app bridge; not final-eligible. |
| P12 | Reliability/selective-risk evaluation for device-level IoT malware DFL | 2026 eight-Raspberry-Pi crowdsensing corpus; the paper already evaluates centralized and decentralized FL. No Android app or mobile-app privacy outcome. | **PHD_PARTIAL** | Separate dissertation line only after a distinct question and leakage/label audit. |
| P13 | Mobile/Android endpoint malware FL using simulated end-user devices | M2FD and related Android FL show direct prior art; client partitions are simulated, and no IoT-network behavior/client-owner evidence is provided by the audited artifact. | **PHD_PARTIAL** | Narrow against drift/Android-FL collisions; no unoccupied outcome yet. |
| P14 | CASE-derived reliability-weighted update aggregation | Needs a prospectively available client-round signal and direct DCAA/drift baselines; current CASE signal is an outcome from paired records, not an independently held client reliability label. | **PHD_PARTIAL** | Reject as current contribution; direct collision and invalid signal timing. |
| P15 | Personalized Android FL with client-specific calibration | Android personalization and local operating-point ideas are occupied; two context clients cannot support a general heterogeneous network claim. | **PHD_PARTIAL** | Keep local calibration as a diagnostic, not novelty. |
| P16 | CASE-guided selective sharing of malware evidence/features | Could fit privacy/security, but no independent evidence custodians, feature owners, leakage model, or share/no-share utility labels are available. | **PHD_PARTIAL** | Block on clients and privacy threat model. |
| P17 | Federated domain generalization across Android device/runtime contexts | Requires multiple train contexts plus a truly held-out context; the paired KronoDroid study has two acquisition modes and shared APK identities. | **PHD_PARTIAL** | Block on support; no broad unseen-domain claim. |
| P18 | Differentially private/secure-aggregation Android malware FL informed by CASE | Privacy mechanism could fit the chapter, but generic Android FL and privacy-preserving malware work already exist; no new privacy budget/leakage or IoT client evidence. | **PHD_PARTIAL** | Not a contribution without a distinct threat model and measured trade-off. |
| P19 | Provenance-qualified collaboration of mobile malware observations | Provenance is valuable, but no separate custodians or compatible provenance exchange protocol was found; provenance alone is not malware detection improvement. | **PHD_PARTIAL** | Keep as a design requirement, not the research question. |
| P20 | Robust Android malware FL under malicious or unreliable IoT clients | Direct collision with current security-hardened Android FL (including Droidware); no attack-capable client set or threat model in available paired data. | **PHD_PARTIAL** | Reject stacked robustness modules absent a new threat model and benchmark. |
| P21 | Train-time portable-feature filtering for federated Android malware models | KronoDroid POC tested a train-only paired-presence-agreement top-half mask; it selected mostly invariant zero features and achieved chance-level balanced accuracy. | **PHD_PARTIAL** | Negative result; do not pursue that mask. |
| P22 | Shared representation with context-specific heads for paired Android executions | Same two-context limitation; personalization is already established and local-only models are the strongest measured baseline in the POC. | **PHD_PARTIAL** | No evidence of advantage; reject as current final project. |
| P23 | DEFEAT Android APT behavior as an FL/mobile-IoT dataset | Public physical-device behavior/attack-stage data may fit mobile security, but the inspected release appears single-device and cannot establish natural heterogeneous clients. | **PHD_PARTIAL** | Dataset lead only; verify exact schema/access and client count before modeling. |
| P24 | Cross-silo Android threat-intelligence learning with scoped CASE summaries | Requires actual labs/SOCs/sandbox providers, aligned labels, and a privacy-preserving sharing protocol; none are available. | **PHD_PARTIAL** | Blocked access/governance; strongest future collaboration concept. |
| P25 | Unified Android-app and IoT-network malware FL benchmark | Android behavior and IoT traffic use incompatible sample units/features/labels; concatenating them would create a modality shortcut, not heterogeneous clients. | **PHD_INELIGIBLE** | Reject; no valid joint target or mobile-to-network mapping. |

P1 and P2 are **PHD_INELIGIBLE** final projects by explicit rule. P3–P10 and P11–P24 are **PHD_PARTIAL**: each has either a potentially relevant component or chapter fit, but fails at least one required empirical bridge. P25 is **PHD_INELIGIBLE** because its proposed joint benchmark has no valid harmonized task. No **PHD_ELIGIBLE** candidate is supported by current evidence. The strongest next experiment, if a single lead must be carried forward, is P11 as a tightly bounded *mobile malware context-heterogeneity* study, paired with a separate IoT device study only if the dissertation chapter scope allows two linked experiments; it must not be represented as a complete answer to the PhD requirement.

##### Revised selection

**No final project passes the hard gate.** Do not select P2. Retain CASE only as a measured reliability/portability component. P11 is the runner-up/closest mobile candidate because it has real paired malware data and an executed, split-safe FL POC; P12 is the runner-up for direct IoT-device fit but fails mobile-app chapter fit and collision novelty. The decisive evidence is that P11's local-only models beat FedAvg/FedProx and its clients are simulated contexts from one dataset, while P12's broad DFL comparison is already in the dataset paper. A valid eligible project needs a mobile-app malware outcome in an IoT/edge deployment setting with a defensible heterogeneous client model and an empirically evaluated privacy/security contribution.


---

### Phase 3 addendum — search for a G-PHD-eligible project (2026-09-23)

Method: CASE-agnostic restart ("If CASE never existed, which mobile-malware FL question best strengthens the PhD?"), then P26–P45 from the brief, plus 13 invented lanes P46–P58. Existing IDs P1–P25 and A/B rows are unchanged. All numbers come from `temp/p3_*` scripts (5 seeds, GPU MLP 920→128→1, package-grouped splits, per-client test sets). Status vocabulary: PHD_ELIGIBLE / PHD_PARTIAL / PHD_INELIGIBLE / BLOCKED_DATA / REJECT. **No lane is PHD_ELIGIBLE.**

#### Anchor construction (P46)
Natural-site clients = AndroZoo app markets (7 clients; config B = 11 clients with Play era cohorts). See `Dataset Audit.md` D-P3-1. This is the only audited data source with a natural site key, both classes, feature compatibility, sample identity and strong measured heterogeneity, at the cost of no IoT/edge semantics.

#### Main POC finding (config A, mean BA / worst-client BA at local-threshold scope, 5 seeds)

| Train samples/client | local | central | FedAvg | FedProx | FedAvg+FT | cluster | shrink (local↔FedAvg logit blend) | val-selected policy | oracle arm (upper bound) |
|---:|---|---|---|---|---|---|---|---|---|
| 100 | .774/.666 | .818/.717 | .804/.712 | .811/.727 | .809/.718 | .801/.721 | .812/.726 | .807/.720 | .823/.742 |
| 300 | .831/.752 | .855/.773 | .834/.742 | .849/.783 | .843/.766 | .843/.769 | .850/.779 | .847/.763 | .858/.794 |
| 1000 | .882/.830 | .888/.832 | .864/.801 | .872/.816 | .872/.812 | .872/.810 | **.889/.828** | .884/.822 | .891/.835 |
| 5000 | .912/.875 | .921/.881 | .901/.857 | .899/.859 | .916/.872 | .903/.859 | .916/.876 | .916/.872 | .921/.879 |

Reading: (1) central ≥ every FL arm at every support level (FL pays a heterogeneity cost); (2) FedAvg beats local-only only at n≈100 (+0.030), is level at 300 (+0.003), and loses at 1000/5000 (−0.018/−0.011), so "when to collaborate" has a support-dependent answer; (3) a fixed local/global logit blend (`shrink`, w = n/(n+500)) matches or beats every other arm at n ≥ 300; (4) the oracle per-client arm choice is only 0.002-0.011 BA above the best fixed rule.

#### Lane verdicts

| ID | Lane | What was done | Result | Verdict |
|---|---|---|---|---|
| P26 | FL detector with shared / cluster / per-client operating points | threshold scopes fixed, global, local, shrunk on FedAvg, FedAvg+FT, central, local (A,B; n=100…5000) | local scope best everywhere: FedAvg+FT n=1000 BA .850→.872, worst-client FPR .442→.239, FPR sd .167→.071; shrunk between, never above local | PHD_PARTIAL (G4, G6; overlaps own DATP) |
| P27 | Heterogeneity-gated personalization | leave-one-seed-out logistic gate on (log n, transfer gap, feature JSD, prevalence gap, own-AUC) predicting FT>local | gate mean gain +0.0111 (A) / +0.0151 (B) vs always-FT +0.0100 / +0.0160; oracle +0.0164 / +0.0228; Spearman(gain, log n) ≈ −0.35, heterogeneity stats ≤ 0.25 | REJECT as method; support n, not measured heterogeneity, explains most |
| P28 | Client→client transfer matrix T[i,j] | pairwise AUC of local_i on val_j | off-diagonal AUC 0.52-0.98 (median 0.80) vs diagonal 0.96; weakest slideme→anzhi 0.52, anzhi→PlayDrone 0.57 | keep as diagnostic only |
| P29 | Transferability-graph collaboration | logit ensemble of local models weighted by (T−0.5)² | −0.011…−0.024 BA vs shrink; cluster-by-T ≈ FedAvg (+0.008 only at n=1000) | REJECT |
| P30 | Local calibration of a global detector | see P26, plus prior-correction test (P52) | local calibration helps; shrunk calibration never beat local even at n=100 (val 60) | PHD_PARTIAL |
| P31 | Reliability-conditioned personalization | n-based shrinkage + val-selected policy | shrink ≥ val-select ≥ others at n ≥ 300; policy ≈ shrink; blend is a known technique | REJECT as novelty |
| P32 | Static vs dynamic evidence in FL | not run this phase | KronoDroid gives only two contexts (P11); LAMDA static only | BLOCKED_GROUPING |
| P33 | Context-fragile feature suppression | not rerun | no valid dynamic multi-client data; prior CASE mask ≈ chance | BLOCKED_DATA |
| P34 | FL under real device/context shift | leave-one-market-out cold start (P39) | no domain-generalisation baseline run | PHD_PARTIAL (weak) |
| P35 | Worst-client-aware detection | worst BA, worst FPR, FPR sd for all arms | disparity is large (fixed-threshold worst FPR .31-.58) and mostly removed by local thresholds; no worst-client optimiser tested | PHD_PARTIAL |
| P36 | Selective federated detection | global vs client-specific confidence cutoffs at 60/80/90 % coverage | at 80 %: client cutoffs equalise coverage (sd .023 vs .069) but worst-client error .120 vs .105 (FedAvg) | REJECT (generic selective prediction) |
| P37 | Small-calibration-data personalization | support sweep n=100…5000 | see table; blend robust, local threshold robust down to 60 val samples | PHD_PARTIAL |
| P38 | Drift vs context heterogeneity | descriptive feature-drift study (benign) | cross-market same-year JSD 0.011-0.015 vs 0.0021 mean one-year Play drift; 12/17 cross-market pairs exceed the maximum observed Play one-year drift; η² market 0.63 vs year 0.35 (7 cells, 2016-2018) | diagnostic promising; no corrected detector built → PHD_PARTIAL |
| P39 | New-client cold start | leave-one-market-out, k=20/100 labelled shots | global+FT(100) BA .841 (worst .739); local on 100 shots .830 (worst .782); nearest-3 / route-3 not better than plain global | routing REJECT |
| P40 | Federated evidence routing | route-3 by measured transfer on k shots | .789/.812 (fixed/k-shot thr) vs global .786/.789 | REJECT |
| P41 | Mobile/IoT gateway collaboration | dataset search + local listing | no linked malware data; PingPong/Hue/moniotr are benign IoT | BLOCKED_DATA |
| P42 | Android Automotive / embedded Android | 3 web searches | none found | BLOCKED_DATA |
| P43 | Calibration poisoning | not run | would be DATP-CP on Android | REJECT (duplicate) |
| P44 | Honest heterogeneity vs poisoned client | mean/median/trimmed-mean/Krum, label-flip attacker at 1mobile/appchina/play vs no attacker | Krum honest BA .744 vs mean .845 (no attack); trimmed flags rank honest Anzhi .46 / Play .40 above the attacker 1mobile .25; label flip lowers honest BA only .845→.825 | best residual, needs a method + stronger attacks → PHD_PARTIAL |
| P45 | Provenance reliability | market id only as split key | not tested as evidence | DEFER |

#### Additional lanes (13)

| ID | Question | Status / result |
|---|---|---|
| P46 | App-market natural-site client construction | done; anchor data lane |
| P47 | At what client support does collaboration start paying? | done: FedAvg−local +.030 / +.003 / −.018 / −.011 at n = 100/300/1000/5000; FT and blend positive from n=100 up |
| P48 | Local/global logit shrinkage as personalization baseline | done: best simple arm at n ≥ 300 (known technique; APFL-style) |
| P49 | Negative-transfer map between markets | done: mean-over-seeds min 0.52; one seed showed 0.42 |
| P50 | Store-identity shortcut audit | not run |
| P51 | AV-vendor label heterogeneity (McNdroid, 119 vendors) | inspected, not run; partition invalid (G-PHD-7) |
| P52 | Is threshold benefit label-prior shift or score-distribution shift? | done: prior-corrected logits lower BA .847→.802 (FedAvg n=1000) while local tuning raises it to .864 → **score-distribution shift, not prior shift** |
| P53 | Per-client cost of federation (central − FedAvg) | done: .017-.044 at n=1000 (PlayDrone .044, Anzhi .036) |
| P54 | IoT vs mobile regime contrast in the same harness | done: N-BaIoT BA ≥ .995; no scope problem |
| P55 | Reliability of validation-based arm selection | done: N-BaIoT n=100 val-select BA .959 vs oracle .992 (picks local in 38/45) |
| P56 | Minimum support before local deployment | subsumed by P47 |
| P57 | Simulated era cohorts as sites (config B, 11 clients) | done: same qualitative picture |
| P58 | Worst-client FPR budget as an explicit target | not run |

#### Decision
No lane satisfies every G-PHD check. Strongest **partial**: P46 + P26/P30/P35/P52 (mobile app-market federation with client-level operating points and worst-client FPR equity), failing G-PHD-4 (no IoT/edge link) and G-PHD-6 (no method beats the shrinkage/threshold baselines; the threshold-scope principle is the thesis's own DATP). Runner-up partial: P44. See `Final Report.md`.


#### Phase 5 (2026-09-24) — corrected eligibility, mechanism-first re-audit

Eligibility correction: lack of real phones/owners is no longer a rejection reason. Candidates rejected on that ground were reopened (list in `Final Report.md`). New lanes:

| ID | Question | Stage reached | Verdict |
|---|---|---|---|
| P59 | Contaminated (unknown malware in "benign" pool) client calibration + k in {0,5,10,20,50} verified items: pooled/EB estimate + trim | failure OK, oracle OK, mechanism OK vs LOCAL/per-client Label-Trim, strong baseline NOT beaten consistently, 5 seeds x 3 domains, alpha .05/.01 | **RUNNER-UP, not promoted** (G-MECH-3, G-MECH-8, G-NOVEL) |
| P59b | label-free contamination correction (peer trim, tail gate, admission) | done in poc2 + re-run | REJECT: 20-30% of oracle gap, clean-pool harm |
| P59c | federated allocation of scarce verification (proportional to peer suspicion) | done (`LAB-EB-ALLOC`) | REJECT: mixed, higher FPR |
| P60 | robust aggregation confuses honest heterogeneity with attackers, with a fix | Stage 1/2 from P44 data | REJECT: only Krum harms; no headroom |
| P61 | drift detector confounded by cross-client heterogeneity | reasoned + P38 | REJECT: strawman baseline |
| P62 | support x mismatch collaboration policy | Stage 2 from P47/P48/P55 | REJECT: blend ~ central, no headroom |
| P63 | negative-transfer / who-should-collaborate | Stage 2 from P28/P29 | REJECT: central >= FL; graph lost |

Mobile domain note: the frozen AE scorer used earlier for LAMDA markets is poor (AUC .44-.92; anzhi 87% malware), so oracle headroom was tiny; Phase 5 uses a supervised FedAvg MLP scorer (AUC .92-.99) for mobile with the same threshold mechanism. N-BaIoT/Pi keep AE scorers (supervised N-BaIoT is saturated).


---

## Claim and Gate Audit

*Source: `poc/Claim and Gate Audit.md` (merged 2026-09-24). G-PHD text superseded per banner; gate definitions and claim dispositions retained.*

### CASE-Android Claim and Gate Audit

#### G-PHD — hard project eligibility gate

**Rule:** The recommended final project must directly and empirically strengthen the PhD topic, *collaborative malware detection with federated learning in heterogeneous IoT networks*, and remain a defensible contribution to a mobile-application privacy/security chapter. A conceptual analogy or generic statement that smartphones are IoT is insufficient. Candidate data must instantiate malware detection, FL, a heterogeneous IoT/edge deployment or a clearly mapped deployment-motivated simulation, and an app privacy/security question. APK rows must not be split arbitrarily and called clients. For every feasible candidate, the minimum CPU POC compares centralized/local/FedAvg/FedProx and candidate method(s), reports macro and worst-client performance and disparity, and documents client construction, heterogeneity, identity-safe splits, and privacy limits.

| Check | Required evidence | Current finding | Status |
|---|---|---|---|
| G-PHD-1: PhD task alignment | Malware detection as the modeled task; explicit relevance to collaborative learning | P11 KronoDroid POC directly models Android malware under simulated FL; P12 is device-level IoT malware | P11/P12 partial |
| G-PHD-2: IoT/edge heterogeneity | Valid IoT endpoints or a deployment-motivated simulation with operationally meaningful clients and no arbitrary APK sharding | KronoDroid offers two paired acquisition-context domains, not independent owners or IoT network clients; 2026 IoT data offer 8 Raspberry Pi endpoints | No candidate passes both G-PHD-2 and the app gate |
| G-PHD-3: Mobile app privacy/security chapter fit | App-level security/privacy outcome, or an explicit mobile-app security method evaluated in the same project | P11 is Android malware security; its data path does not measure privacy or networked IoT behavior. P12 is network/device malware, not mobile app | P11/P12 partial |
| G-PHD-4: Meaningful privacy/security contribution | Threat model and measurable privacy/security intervention; do not infer privacy from FL alone | P11 uses no secure aggregation, DP, or leakage attack; P12 paper's broad DFL benchmark is already published | Fail for current candidates |
| G-PHD-5: Valid clients and identity split | Real owners/endpoints or deployment-motivated contexts; group identical APKs across splits; never arbitrary APK shards | P11 has exactly 63,316 paired APK identities in each context, grouped together for train/calibration/test; clients remain only simulated contexts | Pass for exploratory POC only |
| G-PHD-6: Minimum comparator and outcome | Central/local/FedAvg/FedProx, candidate baseline, macro/worst-client/disparity, 1–3 CPU seeds | Completed for P11; FedAvg/FedProx trail local-only; portability mask is chance-level | Negative/partial evidence |
| **Overall eligibility** | All checks pass and a residual contribution survives collision review | None of P1–P25 passes. See P11–P25 register in [Research Matrix.md](Research%20Matrix.md). | **NO PHD_ELIGIBLE CANDIDATE** |

This gate supersedes the previous CASE-only weighted scorecard. P1/P2 cannot be selected as final projects unless the user explicitly relaxes the requirement; they remain useful components.

#### Claim dispositions

Evidence labels below refer to the discovery campaign, not a protocol-frozen confirmatory result.

| ID | Candidate claim / estimand | Required evidence, dataset, baseline and metric | Current PoC support | Risk | Recommendation |
|---|---|---|---|---|---|
| A | **Context dependence:** recorded Android security evidence has heterogeneous recurrence across named contexts. Estimand: direction- and indicator-specific paired `n00/n01/n10/n11`, recurrence and emergence. | SELENE primary; KronoDroid paired syscall secondary. Compare all flags/calls, directions, indicators, paired bootstrap intervals. | SELENE micro recurrence 89.96% and 85.48%; emergence conditional on source absence 27.98%; strong per-indicator heterogeneity. KronoDroid exact paired syscall recurrence 59.14% and 68.59%. | Both are finite processed observations; context and instrumentation effects are entangled. | **PROMOTE**, bounded to tested artifacts and outcomes. No causal OS/device attribution. |
| B | **Source signal:** source-only evidence predicts recurrence beyond per-indicator persistence. Estimand: package-held-out proper-score improvement. | SELENE primary; train-only global and indicator-persistence baselines; Brier/log loss/AP; package bootstrap; broken-pair control. | Two grouped holdout seeds show rich model 4.01–9.74% Brier skill vs persistence; broken pairing makes all CASE models worse than persistence. | Two splits are exploratory; one compact dataset; gains asymmetric and micro-weighted. | **PROMOTE for confirmatory testing**, but phrase as modest incremental signal, not solved portability. |
| C | **Evidence strength:** counts/structure add beyond Boolean flags and activity volume. Estimand: proper-score delta for raw/normalized count features. | SELENE, matched split and support; Boolean, evidence-count-only, activity-only, rich and normalized-count ablations. | Raw counts modestly improve vs Boolean across directions/seeds; duration-normalized counts underperform raw counts. | Correlated/derived counts; counts may reflect duration or feature construction. | **PROMOTE_AS_SECONDARY**, only if the frozen study retains both raw and normalized ablation. |
| D | **Selective utility:** CASE gives a better recurrence-risk/coverage curve than persistence. Estimand: risk among transferred claims and coverage/recurrence retention. | SELENE grouped OOF predictions; train/calibration/test separation; compare persistence, Boolean CASE and rich CASE; risk at fixed coverage, coverage at predeclared risk targets. | Descriptive fixed-test coverage shows improvement, especially at 50%; 80% effects are smaller. | Current thresholds/ranks are selected and evaluated on the same held-out labels; no calibrated policy result exists. | **PROMOTE as primary implementation question**, require calibration-only test in confirmatory evaluation. |
| E | **Formal risk-controlled reporting:** calibration-only CASE meets declared risk with useful coverage. | Cluster-aware LTT/CRC or justified method, source/target sampling assumptions, calibration-only threshold and group dependence analysis. | No formal method implemented. Package-conditional exchangeability and cross-context shift are unresolved. | Generic i.i.d. guarantees do not automatically apply to multiple claims per app/package or context shift. | **DEFER.** Do not claim a guarantee; report empirical risk/coverage only. |
| F | **Granularity:** finer behavior claims are less portable. Estimand: recurrence/predictability/selective risk across matched abstractions. | SELENE raw L0.5/L1 or AndroCT method→class→package/API families; matched claim mapping and granularity cost. | SELENE event layers are not locally cached; AndroCT not artifact-audited. | Abstraction changes the claim denominator and semantics; AndroCT permissions and 6.3 GB access burden. | **DEFER** until identity and semantic mapping pass. |
| G | **Report reliability:** claim scoping reduces unsupported claims per report while retaining evidence. | Per-APK report grouping; recurrence retention, unsupported transferred claims/report, report-any-unsupported, coverage. Must compare calibrated CASE with persistence. | Report proxy calculated on two test holdouts at fixed score-ranked coverage; rich ranking reduces report-level unsupported counts in those holdouts. | Retrospective test ranking, high recurrence base rate, and “report” currently means the 19-feature released record. | **PROMOTE_AS_SECONDARY** after calibration-only thresholding; no analyst-time claim. |
| H | **Context-family replication:** the CASE predictive/scoping effect replicates across independent context families. | SELENE versioned emulator and KronoDroid emulator/device as minimum; same estimand, predeclared source-only models/baselines and metric. | Krono supports a descriptive exact-pair and broken-pair replication, but not a source-only trained scoping-model replication. | Syscall activity units differ from semantic indicators; existing cross-device consistency work directly covers broad instability. | **PARTIAL / PROMOTE_AS_SECONDARY.** Make a model-level external replication mandatory before a broad multi-context claim. |
| I | **Portability drift:** recurrence relation changes over actual observation time. | Verified capture timestamps and paired future-period evaluation; rolling/leave-year-out calibration and risk. | Not supported: SELENE has two Android versions; Krono fields are APK metadata and not validated as execution timestamps. | Confusing APK age/cohort with trace time. | **DEFER.** |
| J | **Future generalization:** useful signal persists for future apps. | Valid chronological app/observation cohorts; train past, evaluate future; compare all baselines. | Not tested; dates not validated for suitable target chronology. | Apps may not recur and APK release time is not necessarily trace time. | **DEFER.** |
| K | **Malware-family OOD:** signal holds for unseen families. | Harmonized family identity, grouped family splits, adequate support, family-macro risk and proper scores. | SELENE has no family OOD contrast needed for this claim; Krono family labels disagree on 53.4% of valid SHA pairs. | Conflicting taxonomy and label leakage risk. | **BLOCKED / DEFER.** |
| L | **Claim OOD:** evidence source signal transfers to held-out evidence kinds. | Multiple comparable claim families, family-held-out training/test, identity-free features. | Only 19 SELENE flags, several exact duplicates/threshold derivatives. | Too few nonredundant claim families to separate feature transfer from persistence. | **DEFER.** |
| M | **Context versus stochastic instability:** cross-context instability exceeds same-context repeated-run instability. | Same APK, same exact claim ontology, multiple same-context executions plus another context; paired variance decomposition. | No repeated-run sample in audited SELENE. DYNAMISM metadata is a promising but Restricted diagnostic. | Different stimulation and observation time can masquerade as run/context instability. | **BLOCKED / DIAGNOSTIC.** |
| N | **Emergence:** target-context evidence appears despite no source observation, in structured ways. Estimand: `P(target=1 | source=0)` per claim and context direction. | Four-state table, source-absence denominator, indicators and context directions; optionally source-only predictor compared to target prevalence. | SELENE has 57,745 target-emergent flag/APK rows; pooled emergence 27.98%, indicator-macro 50.99%. | A non-observation may be a missed observation; a future target model is not implemented. | **PROMOTE_AS_SECONDARY descriptive estimand.** Do not say “new behavior emerged”; say “target evidence was newly recorded.” |
| O | **PhD relevance:** heterogeneous execution contexts motivate reliability-qualified collaborative security evidence. | Link CASE result to PhD problem conceptually, with no FL-client or IoT claim. | Motivation is plausible; no federated/IoT empirical result is in scope. | Risk of overstating transfer from APK evidence to collaborative IoT detection. | **KEEP as motivation only**, not a contribution claim. |

#### Gate architecture

Use two explicit gate classes. Structural validity failures block only the affected dataset/claim. A weak scientific effect narrows the claim; it does not automatically cancel the project.

| Gate | Class and purpose | PASS | PARTIAL | FAIL | BLOCKED | Current state / consequence |
|---|---|---|---|---|---|---|
| G0 Access/license | Valid use, citation, provenance, redistribution boundaries. | Terms and required acknowledgments are verified for each used artifact. | One artifact verified while optional lanes remain under review. | Use violates terms or required data provenance cannot be established. | Files/terms require unavailable permission. | **PARTIAL:** SELENE terms need exact dual-license reconciliation; AndroCT faculty agreement and DYNAMISM access prevent those lanes. Block only affected data. |
| G1 Identity | Exact APK/run identities and one-to-one joins. | Unique source/target pairing, duplicate policy and counts are recorded. | Known duplicate rows excluded with sensitivity reported. | Unresolvable identity collision or invalid pairing. | Identity key absent/unverified. | **PASS for SELENE hashes and Krono valid hashes; BLOCKED for AndroCT/CIC artifact-level joins.** |
| G2 Context semantics | Define what differs and what stays comparable. | Source/target conditions are documented; interpretation is explicitly bounded. | Context includes multiple bundled differences but remains interpretable as a named context contrast. | Context labels are wrong or outcome definition conflates units. | Missing acquisition metadata. | **PARTIAL:** SELENE contexts are named versioned emulator conditions with run-duration imbalance; Krono is emulator/device; no causal component effect. |
| G3 Claim comparability | Ensure same claim has same meaning across contexts. | Claim ontology and observation rule are identical in source and target. | Comparison is valid for a narrower released processed flag/call. | Semantic mapping invalid. | Required event-level mapping unavailable. | **PARTIAL:** SELENE processed flags comparable; Krono call presence is a different unit; finer SELENE layers absent locally. |
| G4 Provenance | Exact inputs, hashes, transformations and outputs. | Checksums and parents are recorded and reproducible. | Some optional metadata or upstream artifact links incomplete. | Results cannot be traced to immutable inputs. | Upstream access prevents provenance inspection. | **PARTIAL:** SELENE input SHA-256 values recorded; Krono download URL/revision should be frozen before confirmatory use. |
| G5 Leakage | Source-only decision-time firewall. | Predictors are source-side; IDs/targets/outcomes are excluded and poison checks pass. | Exploratory script restrictions reviewed but not full application tests. | Any target-derived or grouping ID predictor changes outcome. | Raw schema prevents source/target boundary. | **PARTIAL:** PoC predictors are source-side; final implementation still needs the roadmap leakage tests. |
| G6 Grouping | Prevent package/version claims crossing train/calibration/test. | One grouping manifest holds all claims per package outside split and is frozen. | Alternative valid package manifests are reported. | Same package leaks across partitions. | Package identity missing. | **PARTIAL:** Two grouped holdouts pass by construction; OOF split manifest not generated. |
| G7 Support | Avoid unstable sparse claims. | Predeclared claim/package minimum met for every promoted stratum. | Sparse claims reported with NA/interval and no promotion. | Support silently excluded or denominator altered post hoc. | No support for lane. | **PARTIAL:** many flags have adequate counts; rare `has_rwx_anon` has only 212/270 source-positive cases and must be diagnostic. |
| G8 Baseline fairness | Same examples and information budget. | Persistence/global/activity and CASE use same outer rows; train-only priors; no target summaries. | One baseline’s feature budget needs clarification. | Baseline uses future target or more test data. | Baseline cannot be computed. | **PARTIAL:** PoC baselines share held-out rows and fit-only persistence; final pipeline must freeze exact baseline definitions. |
| G9 Negative-control integrity | Verify source-target pairing contributes. | Shuffling genuine target identity removes CASE’s advantage over persistence. | One shuffle seed and directions show expected loss. | CASE retains a large gain after pairing is broken. | No pairable identity. | **PARTIAL/PASS at discovery:** model loses vs persistence after shuffle in both SELENE directions/seeds; more permutations should be frozen. |
| G10 Probability quality | Evidence that probability estimates improve over simple priors. | Predeclared Brier/log-loss comparison and package interval support improvement on primary test. | Improvement is small/asymmetric or limited to one direction; claim narrowed. | No improvement or calibration substantially worse. | No labels. | **PARTIAL:** two discovery splits show positive Brier skill; not protocol-frozen. |
| G11 Rich-feature increment | Show evidence counts add beyond Boolean/persistence/activity. | Incremental Brier improvement holds on frozen splits and after exposure/derived-feature checks. | Small but stable improvement; retain as secondary. | Added complexity has no incremental value. | Fields unavailable. | **PARTIAL:** raw count gains repeat, normalized counts lower; run the frozen broad/non-derived sensitivity. |
| G12 Selective utility | Does scoping improve coverage/non-recurrence trade-off? | Calibration-only thresholds improve predeclared risk/coverage comparison on untouched tests. | Better curve but requested budget/coverage unavailable or effects small. | CASE underperforms persistence. | No valid calibration split. | **PARTIAL:** test-ranked fixed-coverage results are descriptive only; a deployable policy gate remains open. |
| G13 Risk-control validity | Support formal finite-sample risk guarantee. | A cited/validated method’s sampling, cluster and shift assumptions hold; calibration is separate. | Only empirical risk/coverage is supportable. | Assumptions contradicted or test used for threshold. | No suitable cluster-aware method. | **BLOCKED for guarantees:** keep empirical policy; no guarantee language. |
| G14 Report-level utility | Quantify claim/reports retained and unsupported. | Frozen policy changes report metrics against persistence with report bootstrap. | Offline proxy only; no analyst study. | Proxy denominator or policy is post hoc. | Reports cannot be reconstructed. | **PARTIAL:** one-APK report proxy exists descriptively; no analyst-time/safety outcome claim. |
| G15 Temporal OOD | Validate train-past/test-future portability. | True trace observation times and chronological identities verified. | Valid APK release cohort only; claim narrowed to cohort drift. | Future labels leak or dates are wrong. | No timestamps. | **BLOCKED:** SELENE two contexts; Krono date semantics not verified. |
| G16 Family OOD | Validate unseen malware-family transfer. | Family labels harmonized; holdout by family; adequate support. | Only one dataset supports a narrower family analysis. | Labels conflict or family leaks. | Family identity missing. | **BLOCKED:** Krono family disagreement is substantial. |
| G17 Claim OOD | Validate unseen evidence-kind generalization. | Claim-family split is meaningful and contains enough independent families. | Only broad held-out categories, exploratory. | Derived/redundant flags make split tautological. | Too few claims. | **BLOCKED/DEFER:** 19 flags with known duplicates do not support this claim yet. |
| G18 Fidelity robustness | Check dependence on extraction/parser fidelity. | Predefined fidelity strata and evidence support are interpretable with adequate common hashes. | Small matched oracle; only limited diagnostics. | Fidelity data used as target truth or unsupported stratum suppressed. | Too few paired oracle IDs. | **PARTIAL:** oracle overlaps on 56 hashes; treat as artifact-fidelity diagnostic only. |
| G19 Independent dataset replication | Replicate CASE model/decision on another dataset. | Same estimand, model and baselines run on independently prepared compatible pair data. | Descriptive pairability/recurrence only. | Replication contradicts but result hidden. | Access/claim mapping unavailable. | **PARTIAL:** Krono supports a descriptive replication, not yet predictive/scoping replication. |
| G20 Independent context-family replication | Replicate across version/device/reboot/repeat context families. | Compatible claim-level effect appears in independent context family. | Different feature semantics support a narrower context association. | No effect across context family. | Access unavailable. | **PARTIAL:** Krono supports syscall recurrence only; AndroCT/DYNAMISM/CIC remain optional or blocked. |
| G21 Complexity justification | Ensure model complexity earns its cost. | More complex model adds stable utility over the simplest interpretable model. | Logistic ladder sufficient; additional methods unneeded. | Complex model adds no stable value. | Comparative fit impossible. | **PARTIAL:** pooled L2 logistic is adequate candidate; no random forest/GAM/boosted model needed yet. |
| G22 Sensitivity robustness | Check directions, indicators, weighting, derived features, durations, thresholds, folds. | Main conclusion stable under predeclared sensitivities. | Clear heterogeneity narrows claim. | Outcome depends on post hoc subset or one fragile split. | Needed stratum not available. | **PARTIAL:** direction, two seeds, normalized counts, broken pairing run; broad-only and fidelity sensitivity remain. |
| G23 Reproducibility | Repeat from artifact checksums and stored split manifest. | Deterministic CLI and inputs recreate structured results. | Discovery scripts/results are saved; implementation contract remains. | Results not reproducible or inputs changed silently. | Data access lost. | **PARTIAL:** PoC scripts, JSON outputs, and eight local SELENE input hashes recorded; no final pipeline yet. |
| G24 Claim promotion | Decide wording and scope after all relevant gates. | Claim has all required validity gates and frozen confirmatory evidence. | Empirical result supports qualified language only. | Structural validity failure invalidates claim. | Required dataset/method unavailable. | **OPEN:** this document recommends claim dispositions; no roadmap claim is promoted until the roadmap is revised and future protocol is executed. |

#### Gate consequence rule

1. A failure of G0–G6 blocks the affected dataset/estimand until repaired; do not carry a number forward.
2. A failure or partial result in G7–G12 narrows the stratum, metric or language. It does not automatically stop CASE.
3. G13 is required only for a formal risk guarantee. Empirical selective curves do not need to be disguised as guarantees.
4. G15–G20 are extension gates; they are not prerequisites to a bounded SELENE chapter, but at least one independent dataset/context replication should be required before broad cross-context language.
5. G21–G23 constrain model choice and reproducibility; G24 controls wording only after the frozen evaluation. None permits moving a gate based on outer-test outcomes.


---

### Phase 3 addendum — G-PHD v2 (eight checks, absolute gate)

The Phase 3 brief restates G-PHD as eight checks (numbering below supersedes the six-row table above; earlier rows are kept for history). A project is eligible only if **every** check passes; PHD_PARTIAL cannot win. Numbers: see `PoC Matrix.md` Phase 3.

Candidate assessed: **P46 anchor** — federated Android malware detection over natural app-market clients (LAMDA × AndroZoo markets) with client-level operating points / shrinkage and worst-client reporting (lanes P26, P30, P35, P37, P47, P48, P52), with an N-BaIoT device federation as replication (P54).

| Check | Requirement | Evidence | Result |
|---|---|---|---|
| G-PHD-1 Security task | real malware / intrusion detection | Android malware vs benign (VT ≥ 4), IoT botnet vs benign | PASS |
| G-PHD-2 FL/collaboration | FL or comparable evaluated | FedAvg, FedProx, FedAvg+FT, cluster FL, local/central, 5 seeds | PASS |
| G-PHD-3 Heterogeneous participants | meaningful non-IID sites | 7 markets, prevalence 14.6 %-87 %, feature JSD up to 0.022, transfer AUC 0.52-0.98 | PASS (natural site key; not independent organisations; prevalence partly a collection artifact) |
| G-PHD-4 IoT/edge relevance | deployment maps credibly to IoT/edge collaborative security | app markets are cross-silo store operators, static APK features, no device/edge identity; N-BaIoT replication is a different task and feature space and is saturated (BA ≥ 0.995) so it does not test the same mechanism | **FAIL** |
| G-PHD-5 Mobile application security | Android apps remain the modelled problem | Android APK static features | PASS |
| G-PHD-6 Added contribution | security/privacy/reliability/personalisation contribution beyond FedAvg | client-level thresholds (= DATP principle) and blending are known; heterogeneity gate, transfer graph, routing, abstention all negative or ≤ baseline; only descriptive residuals (score- vs prior-shift P52, P38 drift-vs-context, P44 honest-vs-attacker) | **FAIL** (no method with positive, non-duplicated result) |
| G-PHD-7 Valid client construction | no arbitrary APK shards; justified simulated clients | markets are a natural key; package-grouped splits shared across clients; config B eras are simulated and labelled as such | PASS with caveats |
| G-PHD-8 Baseline evidence | central, local, FedAvg, FedProx, candidate; client-level + worst-client | all reported, worst BA/FPR and FPR sd | PASS |

**Outcome: PHD_PARTIAL (fails G-PHD-4 and G-PHD-6).** Every other lane (P26-P58) is at best PHD_PARTIAL or BLOCKED/REJECT; none passes G-PHD-4 and G-PHD-6 together.

#### Claim register additions (Phase 3; all exploratory, single anchor dataset)
| Claim | Evidence | Status |
|---|---|---|
| Central pooled training outperforms every FL arm on app-market clients | 4 support levels × 5 seeds (A), same in B | supported (exploratory) |
| FedAvg beats local-only only at very small client support | +0.030 (n=100), +0.003 (300), −0.018 (1000), −0.011 (5000) | supported (exploratory) |
| Client-level thresholds reduce worst-client FPR and FPR dispersion | worst FPR .442→.239, sd .167→.071 (FedAvg+FT n=1000) | supported (exploratory); duplicates DATP principle |
| Local-threshold benefit is score-distribution shift, not label-prior shift | prior correction −0.045 BA; local +0.017 | supported (single dataset) |
| Training-only heterogeneity statistics predict when to personalise | Spearman ≤ 0.25; gate ≤ always-FT | **not supported** |
| Transferability graph / routing improves collaboration | −0.011…−0.024 BA vs blend; route-3 ≈ global | **not supported** |
| Robust aggregation penalises honest heterogeneous markets more than a label-flip attacker | Krum honest BA −0.10; trimmed flags Anzhi/Play > attacker | descriptive only |
| Federation-referenced drift signals confuse market differences with temporal drift | cross-market JSD 5-7× temporal; 12/17 pairs above max Play drift | descriptive only |

Forbidden wording: "first", "state of the art", IoT/edge deployment claims for the market federation, any statement that N-BaIoT results test the same mechanism.


#### Phase 5 gates: G-MECH and G-NOVEL (2026-09-24)

| Gate | P59 result |
|---|---|
| G-MECH-1 failure exists | PASS (TPR -.30 to -.40; worst-client -.37 to -.39; FPR unchanged) |
| G-MECH-2 mechanism improves | PASS (recovers 90-93% mean, 82-88% worst gap vs LOCAL) |
| G-MECH-3 beats strong simple alternatives | **FAIL** (CLEAN-K-SHRINK ties/wins in heterogeneous average; CLEAN-K wins at k>=50) |
| G-MECH-4 meaningful | pass vs LOCAL; +.00-.09 success vs strongest baseline |
| G-MECH-5 stability | PASS vs LOCAL (5 seeds); mixed vs strongest baseline (k=20 N-BaIoT 1/5) |
| G-MECH-6 no hidden oracle | PASS (k verified labels + pool scores) |
| G-MECH-7 mobile + IoT | PASS qualitatively (3 domains) |
| G-MECH-8 complexity earns cost | **FAIL** |
| G-NOVEL | **FAIL** (Bashari Label-Trim; weak residual) |
Outcome: not promoted. All other Phase 5 lanes failed G-MECH-1/2 (no headroom). Claim wording allowed: "unlabeled peer trimming recovers only 20-30% of contamination-induced TPR loss; a verified budget of ~5-10% of the pool recovers most of it; pooling verified counts across clients matters at k<=10." Forbidden: any winner/first/novel-mechanism claim.
