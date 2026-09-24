# Final Report

> **SUPERSEDED RULES (Phase 6 consolidation, 2026-09-24).** The following earlier rules are void wherever they appear below; the scientific measurements they gated are kept.
> - Requirement of *natural data owners*, *real hardware*, or *one linked Android+IoT dataset* (G-PHD-4, G-PHD v1/v2 "hard conjunction", "NO ELIGIBLE PROJECT" verdicts). Replaced by: simulated, deployment-motivated clients on public data are acceptable (no arbitrary APK shards); PhD relevance = clear link to >=1 thesis theme, used as a hard *filter* not a conjunction.
> - Verdicts "NO STRONG CANDIDATE" (Phase 5) and "no winner" — superseded by the Phase 6 classification in `Final Report.md`.
> - G-MECH/G-NOVEL remain in force as evidence standards.

## PHASE 6 (2026-09-24) — chapter-candidate search under the corrected rules

**Rules in force:** simulated deployment-motivated clients on public data are acceptable; PhD relevance (>=1 clear thesis theme) is a hard *filter*; ranking = PhD relevance > chapter fit > added value > working mechanism > defensible novelty > feasibility > reproducibility. Old "natural owners / real hardware / one Android+IoT dataset" rules are superseded (see banner). Roadmap and technical doc untouched. No unit tests exist for the POC scripts; results are exploratory, package-grouped, literature search is targeted (not systematic).

### Consolidation
`docs/poc/` now holds exactly four Markdown files (this file, `Research Matrix.md`, `Dataset & POC Audit.md`, `Novelty & Literature Audit.md`) plus `temp/` (scripts, JSON, `progress.txt`). `docs/poc2/` was merged in (its scripts moved to `temp/`, its four notes are sections of the four files) and removed. All candidate IDs (P1-P59, A/B series), negative POCs, dataset findings and collision rows are preserved in the merged files; duplicated text is only the two `Paper Candidates` stubs and the two `PoC/POC Matrix` files kept as separate sections.

### New evidence this phase (all 5 seeds unless noted)
**B — complementary threat knowledge / unseen-family asymmetry (P60)** — `temp/p6_unseen_family.py`, `p6b_nofam.py`, `p6_unseen_family_analyze.py`, `p6_unseen_family_s*_n{6000,1500}_a0.05.json`, `p6b_nofam_s*_n6000.json`.
Clients (LAMDA x AndroZoo, package-grouped 60/20/20): Play<=2018, Play>=2019, Anzhi, AppChina; 920 static features; supervised MLP; 6,000 train samples/client at natural prevalence. Family exposure is *controlled*: 16 top AVClass2 families are split into 4 groups; client c deletes group G_c malware from its own training; peers keep it (families are naturally market-concentrated, e.g. dowgin in Anzhi, airpush/dnotua in Play, so the asymmetry is realistic). Unseen-family recall of client c = recall on test malware of G_c (from all four markets' test splits) at the threshold giving 5% FPR on c's own validation benign. FPR realised 0.047-0.053 for every arm.

| Arm (n=6000, alpha=.05) | unseen recall mean | worst client | known-family recall | gap recovered vs oracle (mean / worst) |
|---|---|---|---|---|
| local | .491±.076 | .283±.113 | .773 | 0 / 0 |
| central | .698±.027 | .378±.101 | .803 | .81 / .60 |
| FedAvg | .689±.036 | .426±.073 | .756 | .74 / .73 |
| FedProx | .697±.028 | .413±.103 | .786 | .79 / .58 |
| FedAvg + local fine-tune | .677±.029 | .434±.051 | .772 | .73 / 1.02 |
| local/FedAvg blend 50% | .643±.041 | .353±.094 | .797 | .59 / .39 |
| local/central blend 50% | .658±.039 | .333±.120 | .809 | .66 / .31 |
| ORACLE local (own exposure restored) | .595±.068 | .377±.108 | .768 | .42 / .60 |
| ORACLE central (nobody hides) | .745±.034 | .474±.115 | .794 | 1.00 / 1.00 |

(oracle gap = central-with-full-exposure minus local). All FL/central arms beat local in 5/5 seeds on mean unseen recall; FedAvg/FedProx/FT/central also on worst client in 5/5. n=1500 (3 seeds): same order (local .411, central .638, FedProx .621, FT .617; worst-client .20 -> .25-.27) but noisier.
**Decisive control (does the gain come from complementary knowledge or just from pooling?)** pooled/FedAvg models trained with G_c removed from *every* client: central-nofam .623 mean / .273 worst; FedAvg-nofam .591 / .314. Hence of the +.207 mean gain of central over local, ~.13 is generic pooling/regularisation and **~.075 (central) - .098 (FedAvg) mean and ~.105-.11 worst-client is genuine complementary family knowledge.** Worst client without the family stays at local level (.27-.31); with it .38-.43.
Per-family: peers rescue dowgin (.51 -> .94-.99), plankton (.67 -> .91-.98), revmob (.55 -> .77-.93), leadbolt (FT .17 -> .60), but not smsreg, gappusin, youmi, ewind, hiddad (all <=.6 even with central pooling): a large share of family-level failure is **collaboration-irreducible** (feature-level, not exposure-level).
**Headroom for a new mechanism** is small: best simple arms recover 73-81% of mean and 60-100% of worst-client oracle gap; residual to oracle ~.05-.07 mean recall. Local/FedAvg logit blends are *worse* than FedAvg/FT, i.e. the "simple blend" is not the strongest baseline here. No mechanism was implemented (Stage 4 gate not passed).

**P59 / C** no new run; existing 5-seed results stand (see above): `CLEAN-K-SHRINK` (k verified-benign items, 50/50 shrink to federation mean) ties/beats the estimator; ~5-10% of pool as verified labels recovers ~90% of the TPR gap. Answers to the question list: (i) trust local calibration only if verified-benign k is >=50 (25% of pool) or the pool is clean; (ii) shrinkage toward peers is the strongest simple repair, per-client Label-Trim recovers only 32-37% of worst gap at k=10 vs 86-96% pooled; (iii) ~10 verified labels/client achieves oracle mean TPR but with +2-3 pt FPR overshoot; (iv) clean clients are not harmed (estimated eps=0 gives identical thresholds). No consistent mechanism win -> component, not standalone.

**CASE extension (P61)** `temp/p6_case_calibrated_policy.py`, `p6_case_calibrated_policy_results.json`: calibration-only selective scoping (the previously deferred claim D). Package-grouped train/cal/test, 5 seeds, both directions, threshold picked on calibration to reach target non-recurrence risk. Realised test risk hits target (r*=5%: .049-.055). At equal realised risk, rich pooled logistic keeps more claims than persistence: coverage .873 vs .836 (10->14), .709 vs .639 (14->10) at r*=5%. **Heterogeneity result:** pooled threshold hides a bad worst indicator (worst-indicator realised risk .21-.22 at r*=5%, .53 at r*=10%); per-indicator ("local scope") thresholds cut it to .06 (rich) but lose coverage (.709 vs .873 forward). This is the DATP scope trade-off reproduced on a second mobile object, and is the honest PhD hook (worst-group reliability, thresholding under heterogeneity) without forcing FL.

**Membership-inference leakage of federated Android detectors (P62)** `temp/p6_mia.py`: loss-threshold MIA AUC per client, n=500/3000, 3 seeds: local .48-.55, FedAvg .50-.58, central .49-.56. **Stage 1 failure absent -> REJECT** (weak attack, static binary features; not evidence that no leakage exists under stronger attacks).

### Classification
**TOP TIER**
1. **B — Complementary threat knowledge for unseen Android malware families (P60)**
2. **CASE-Android + calibrated worst-indicator scoping (A01/P2 + P61)**
3. (co-listed component, not standalone) **C — verification-budgeted federated calibration (P59)** kept as a section/appendix: PhD-relevant, evidence complete, mechanism not novel.

**NEEDS ONE MORE POC:** B (see card). P65 (which peers to trust for a family; headroom test only if B's replication shows residual oracle gap >.10), P63 (VirusTotal grey-zone/label delay as verification cost, LAMDA has AV counts; direct collisions MalWhiteout, PACM SE 2025).

**REJECTED (one decisive reason each):** P62 MIA (no measurable leakage); P66 federated class-incremental novel-attack IDS (EdgeFedCIL 2026, FL transfer for rare classes 2025 already occupy it; and our B result shows simple FedAvg-FT suffices); P67 robust aggregation vs honest heterogeneity (P44: no headroom); P68 drift vs heterogeneity (P38: per-client detector already separates); P69 DATP-style client thresholds on app markets (own prior work, DATP); P70 paired-context FL (P11: local > FedAvg, K=2); P71 mobile/IoT interaction (no linked data); P64 cold-start clustering/routing (P37-P48: fixed blend ~ central); P59b unlabeled peer-trim (identifiability ceiling); P12 IoT DFL corpus (already benchmarked).

### Top-tier cards

#### 1. B — Working title: *How Much of Collaboration's Value on New Malware Families Is Complementary Knowledge? A Controlled-Exposure Study of Android Clients*
- **Research question:** When a client has never observed a malware family that peers have, how much unseen-family recall and worst-client recall does collaboration add beyond generic data pooling, and which families cannot be helped?
- **Mobile/chapter fit:** Android malware, privacy-preserving (data-local) collaboration, zero-day/new-family threat; directly a mobile-security chapter.
- **Exact PhD connection:** collaborative FL malware detection; heterogeneous/non-IID clients; scarce local evidence/cold start; worst-client performance/fairness; when to collaborate vs stay local; negative transfer (known-family cost: FedAvg -.017 known recall vs local). Not IoT-specific but tests the thesis's core "does collaboration help this client" on a second domain.
- **Datasets:** LAMDA (1,008,381 apps, 920 static features, AVClass2 families) joined with AndroZoo markets. **Client design:** 4 clients (Play<=2018, Play>=2019, Anzhi, AppChina), family exposure controlled by hiding one family group per client; families are naturally market-concentrated.
- **Scientific failure addressed:** local models miss unseen families (mean recall .49, worst client .28 at 5% FPR); pooling alone does not close the gap.
- **Mechanism / contribution:** measurement + decomposition (pooling vs complementary knowledge; collaboration-irreducible families; known-family trade-off). **No new method claimed**; a mechanism only if replication shows residual >.10 to oracle.
- **Strongest simple baseline:** FedAvg + local fine-tune / FedProx / central (recover 73-81% mean, 60-100% worst-client gap). **POC evidence:** table above, 5 seeds, plus nofam control. **Oracle/headroom:** local->oracle central +.25 mean, +.19 worst; simple arms leave ~.05-.07.
- **Novelty:** moderate. Closest: Federated transfer learning for rare attack classes (Sci Rep 2025), EdgeFedCIL (Sensors 2026), federated zero-day ensembles / leave-one-family-out (PLOS One), FL-MalDrift, Droidware, Sentinel. Most dangerous collision: rare-class federated transfer (already claims cross-client knowledge for unseen classes). Residual: controlled-exposure decomposition on Android with pooling control, worst-client view, irreducible-family analysis. Not a "first" claim.
- **Expected added value:** quantified, reproducible effect (+.075-.10 mean, +.11 worst-client recall from complementary knowledge at fixed FPR) and a negative finding that naive blends are worse than FedAvg-FT.
- **Remaining decisive POC:** (1) replicate on a second exposure axis (year cohorts or McNdroid / Drebin-style families) and a second scorer (gradient boosting or larger MLP) to show the decomposition is not an MLP artifact; (2) dose-response: recall gain vs number of peer samples of the family (1, 10, 100, 1000); (3) 3 alpha values (.01/.05/.1).
- **Implementation burden:** low (scripts exist, ~1 min/seed on GPU). **Main risk:** families are AVClass2 adware-heavy labels; "unseen family" is confounded with cross-market shift; effect may reduce to "more data helps". **Verdict:** TOP TIER; strongest PhD-relevant candidate, empirical rather than methodological.

#### 2. CASE-Android (+ calibrated worst-indicator scoping) — Working title: *Reliability-Qualified Scoping of Recorded Android Security Evidence Across Execution Contexts, with Calibrated Operating Points*
- **Research question:** Can source-context evidence predict which recorded claims recur in another named execution context, and can a calibration-only policy deliver a stated non-recurrence risk with more coverage than persistence while exposing worst-indicator heterogeneity?
- **Mobile/chapter fit:** strongest of all candidates (Android dynamic-analysis reports, context shift, evidence reliability).
- **Exact PhD connection:** heterogeneity/context shift, reliability of local evidence, calibration and thresholding, worst-group (indicator) reliability, personalization-vs-pooling scope (per-indicator vs pooled thresholds). It is an **analogy, not an FL result**; the thesis link is "decision reliability under heterogeneous contexts", supplied by the P61 scope experiment. FL is not forced in.
- **Dataset(s):** SELENE (30,746 exact Android 10/14 APK pairs); KronoDroid as descriptive syscall replication. **Client design:** none (contexts are directions, indicators act as heterogeneous groups).
- **Scientific failure addressed:** persistence already recurs 85-90%, but is unreliable per indicator; pooled thresholds give worst-indicator risk .21 at a 5% target.
- **Mechanism:** pooled L2 logistic on source flags/counts/volume + calibration-only threshold, per-indicator vs pooled scope. **Strongest simple baseline:** per-indicator persistence (and per-indicator threshold for scope).
- **POC evidence:** Brier skill 4-10% over persistence, positive package-cluster CIs, broken-pair control removes the advantage (Phase 1); Phase 6: risk targets met, coverage +3.7/+7.0 pts at equal risk, worst-indicator risk .21 -> .06 with per-indicator scope at a coverage cost. **Oracle/headroom:** modest by construction (persistence is strong).
- **Novelty:** bounded (estimand + report operation); collisions: cross-device behaviour studies (Same App, Different Behaviors; AndroCT), conformal risk control/LTT, selective prediction. **Expected added value:** moderate, honest, low risk; not a headline. **Remaining decisive POC:** frozen confirmatory split + KronoDroid model-level replication; cross-direction threshold transfer with k verified target claims. **Burden:** medium (protocol freeze). **Main risk:** two contexts only, modest effect, PhD link by analogy. **Verdict:** TOP TIER as chapter *component/second experiment*; does not carry the PhD link alone. A single small extension (P61 scope study, done) strengthens the link enough for a chapter section; FL was not injected.

#### 3. C — Working title: *What a Small Verified Budget Buys: Repairing Contaminated Client Calibration in Federated Malware Detectors* (P59)
- **RQ:** when should a client trust local calibration vs peer information, and how many verified labels repair contamination? **PhD connection:** contamination/unreliable local evidence, calibration and thresholds, worst-client TPR, scarce labels, robustness. **Chapter fit:** medium (mobile app markets are one of three domains; mobile supervised MLP on 7 markets).
- **Evidence:** 3 domains, 5 seeds: contaminated LOCAL TPR .43 vs clean .83 (mobile), oracle repair full; k=10 verified items/client recovers 90-93% of mean TPR gap. **Strongest simple baseline `CLEAN-K-SHRINK` ties or beats the estimator in 3/6 cells** (G-MECH-3 failed). **Novelty:** low-moderate; dangerous collision Bashari, Sesia & Romano (ICML 2025) Label-Trim; also arXiv 2605.06204, 2607.25439, DATP-CP. **Verdict:** keep as an appendix/section of B or CASE (not standalone); mechanism does not survive.

### Recommended Top 3 (ranked)
1. **B (P60)** — best PhD relevance, real and measured effect, controlled design, cheap to finish; empirical-study framing.
2. **CASE + calibrated worst-indicator scoping (P61)** — best chapter fit and lowest risk, weaker PhD link (analogy).
3. **C (P59) as a component** — strong PhD relevance, complete evidence, no surviving mechanism.

### If I Had to Choose Today
**B (P60), with CASE-P61 as the second experiment only if the chapter needs a reliability/report angle.** Reasoning: it is the only candidate that scores well on all of PhD relevance (collaboration value, cold-start/unseen threats, worst-client), chapter fit (Android malware, privacy-preserving collaboration), working measured effect (5/5 seeds, control isolates complementary knowledge), feasibility (minutes per run) and defensible-but-moderate novelty. Honest limits: no new method, the effect is partly plain pooling (~60%), and the rare-class federated-transfer literature is the collision to beat. CASE is the safer publication but has a weaker PhD link; C has the PhD link but no mechanism.



---

## Phase 1-5 report (poc)

*Source: `poc/Final Report.md` (merged 2026-09-24). Old "hard PhD gate" wording superseded.*

### FINAL RESEARCH DECISION

**NO STRONG CANDIDATE**

Phase 5 re-audit, 2026-09-24. Simulated clients accepted (natural-owner/hardware demands dropped); new gates G-MECH and G-NOVEL applied. `docs/Roadmap.md` and `docs/technical_doc.md` are unchanged; no roadmap rewrite is proposed.

**RUNNER-UP: P59 — verification-budgeted repair of contaminated client calibration** (pooled/empirical-Bayes contamination estimate from k verified items per client, then tau-corrected trim; `LAB-EB-TAU`).

**WHY IT LOST (three independent reasons):**
1. *G-MECH-3 not passed.* The strongest simple alternative — set each client threshold from its k verified-benign items and shrink 50/50 to the federation mean (`CLEAN-K-SHRINK`) — ties or beats the mechanism in the heterogeneous-contamination average (k=10 success rate: mobile .60 vs .58, N-BaIoT .75 vs .72; k=20 N-BaIoT .93 vs .80). Mechanism wins under homogeneous 10% contamination (mobile .74 vs .61, Pi .76 vs .61, N-BaIoT .84 vs .77) and on Pi at k=20, and the ad-hoc average of the two (`HYB`) helps mobile/N-BaIoT but hurts Pi. No consistent winner across three domains.
2. *G-MECH-8.* What works is "spend ~5-10% of the calibration pool on verified labels"; the contamination model adds at most ~+0.09 success rate over that.
3. *G-NOVEL.* Direct collisions: Bashari, Sesia & Romano (ICML 2025) Label-Trim (limited labeling budget + trimming of contaminated calibration data); arXiv 2605.06204 (trimming = conditioning, retained-law diagnostic); arXiv 2607.25439 (federated NIDS under contaminated unlabeled data); DATP / DATP-CP (own). Residual = pooling verified counts across heterogeneous clients; real (per-client Label-Trim recovers only 32-37% of the worst-client gap at k=10 vs 86-96% pooled) but a shrinkage estimator, not a new mechanism.

**Fill-in-the-blank test (requirement 19):** "We identify X (contaminated calibration collapses TPR at unchanged FPR — TRUE, 3 domains). Existing approaches Y do not resolve it (unlabeled peer trimming recovers 20-30% — TRUE). We propose Z, a simple deployment-available mechanism (k verified labels + pooled estimate — TRUE). Z consistently outperforms the strongest simple alternative (FALSE: ties/loses in 3 of 6 domain x k cells) and is residual-novel over Label-Trim + DATP-CP (WEAK)." The blanks cannot be honestly filled.

#### Phase 5 headline evidence (5 seeds; alpha=.05; N=200 pool (60 Pi); contamination INJECTED; only app-market prevalence is natural)

Mean TPR / worst-client TPR / success rate (all clients FPR<=2alpha and TPR>=.8 oracle TPR), 10% homogeneous random contamination, k=10 verified items/client:

| Domain (clients, scorer) | clean LOCAL | contaminated LOCAL | oracle (drop true contaminants) | LAB-LOCAL (per-client Label-Trim) | CLEAN-K-SHRINK (strongest simple) | LAB-EB-TAU |
|---|---|---|---|---|---|---|
| Mobile: 7 LAMDA app markets, supervised FedAvg MLP | .83/.69 | .43/.30, succ .01 | .83/.69, .98 | .75/.41, .37 | .84/.60, .61 | .83/.73, .74 |
| IoT: 9 N-BaIoT devices, federated AE | .77/.59 | .47/.32, .15 | .77/.59, 1.00 | .68/.41, .39 | .76/.59, .77 | .76/.59, .84 |
| IoT: 8 Pi devices (SciDB), federated AE | .69/.53 | .39/.18, .16 | .70/.54, .94 | .64/.30, .38 | .59/.45, .61 | .70/.55, .76 |

Averaged over hom .05/.10/.20 + heterogeneous (linear 0-.3; market-prevalence x .3 for mobile) x random/top-score contaminants, k=10: LOCAL .33/.19 (mobile), .37/.24, .30/.13; LAB-EB-TAU .78/.60, .73/.54, .67/.50; CLEAN-K-SHRINK .84/.61, .76/.59, .60/.45; HYB .81/.64, .74/.57, .60/.44. Oracle recovers full TPR; LAB-EB-TAU recovers 90-93% of mean-TPR gap, 82-88% of worst-TPR gap; success rate stays .58-.72 vs oracle .92-1.0 (residual FPR overshoot ~ +2-3 points mean FPR, worst-client FPR .12-.14 vs .08-.11).

Other facts: clean pools are not harmed (estimated eps = 0 gives identical thresholds; LOCAL-equal), whereas PEER-TRIM and GLOBAL raise worst-client FPR by +.08-.16 on clean pools. Stealth (low-score) contaminants barely hurt LOCAL (TPR .63-.68); mechanism still no worse. alpha=.01 fails for every method (pool of 200 cannot resolve 1%; success <=.33 vs oracle .54-.86). CLEAN-K alone (raw k verified-benign items) has excellent TPR but worst-client FPR .26-.27 at k=10; it catches up only at k>=50 (25% of the pool). Seed-wise: LAB-EB-TAU beats CLEAN-K on success rate in 5/5 seeds at k=10 in all domains, 1/5 (N-BaIoT) and 4/5 (Pi), 5/5 (mobile) at k=20. Files: `temp/p5_*.py`, `p5_budget_*_a{0.05,0.01}.json`, `p5_final_output.txt`, `p5_analyze_output.txt`.

#### Requirement-21 status: no winner, so no winner card is issued. Serious rejected candidates (decisive reason)

| Candidate | Single decisive reason |
|---|---|
| P59 contamination + verification budget (runner-up) | strongest simple baseline ties/wins; Label-Trim collision |
| P59b unlabeled contamination correction (PEER-TRIM, tail gate, admission, PEER+LAB) | identifiability ceiling: recovers 20-30% of oracle gap; clean pools harmed |
| P59c scarce-verification allocation (LAB-EB-ALLOC) | no consistent gain over uniform allocation; raises FPR |
| B / P26,P30,P35 scope (local/global/cluster) | LOCAL threshold is DATP; selection between scopes never beats fixed best (valid-set selection unreliable, P55) |
| C,G / P37,P39,P47,P48 support x mismatch, cold start | fixed local/global blend already ~central (mobile n=1000 .889 vs .888); no oracle headroom to justify a selection rule; APFL-style |
| D / P28,P29,P40 negative transfer, routing | central >= every FL arm at all supports: no negative transfer to fix; graph/routing lost |
| E / P44 robust aggregation vs honest heterogeneity | failure only for Krum (honest BA -.13); median/trimmed-mean cost <=.007 and already stop sign-flip; attacker detected with AUC~1 by max/median update-distance -> no headroom |
| H / P38 drift vs stable heterogeneity | federation-referenced detector is a strawman; self-referenced (per-client) detector already separates them, no decision improved |
| I / P15 personalised decision layer | is DATP (own); threshold gains are score shift not prior shift (P52) but no new method |
| P11/P3/P5/A05 paired-context FL (KronoDroid/SELENE) | local-only > FedAvg; only 2 contexts (K=2) cannot support collaboration study |
| P12 IoT DFL corpus | dataset paper already benchmarks DFL; N-BaIoT saturated (no headroom) |
| A04/B07/P6/P14 reliability-weighted aggregation | DCAA 2026 etc. collision, no CASE signal at update time |

#### Old-rejection audit (requirement 4): was it SCIENCE or ELIGIBILITY?

| Reason originally given | Candidates | Reopened? | Outcome |
|---|---|---|---|
| Not natural owners / simulated clients / no real hardware | P13, P26, P30, P34, P35, P37, P43, P44, P38, P39, A03, A05 | YES | Re-tested under simulated market/device clients (Phase 3/4 harness + Phase 5). All either already carried a science failure (P26-P40 negative, headroom absent) or became P59/P44/P38 above; none survives |
| Two contexts only (K=2) | P3, P5, A05, A06, B06 | no (data, not eligibility) | Still invalid: two clients give no heterogeneity structure; P11 adds a science failure (local > FedAvg) |
| No compatible paired multi-owner claim data | A02, A10, B11, P9, P16, P19, P24 | no | Data absent; simulating claim tables from app markets would fabricate the estimand |
| Novelty/mechanism failure | P29, P31, P36, P40, P48, A04, B07 | no | Left closed |

Complete task, dataset, novelty, POC and gate detail: Research Matrix, Dataset Audit, Novelty Audit, Novelty Collision Matrix, POC/PoC Matrix, Claim and Gate Audit (Phase 5 sections). Earlier text below is preserved; the "Superseding decision — hard PhD gate" wording about natural clients is **superseded** by the corrected eligibility rule (simulated, deployment-motivated clients are acceptable); its scientific conclusions stand.

---

### CASE-Android Pre-Implementation Scientific Audit

Audit date: 2026-09-23. This report is a decision document for revising the roadmap. The authoritative `docs/Roadmap.md` and `docs/technical_doc.md` were not modified.

#### Superseding decision — hard PhD gate

**No current candidate is recommended as the final PhD project.** The supplied requirement is a hard conjunction: directly and empirically strengthen collaborative malware detection with federated learning in heterogeneous IoT networks, while fitting a mobile-application privacy/security chapter. P1/P2 fail the direct empirical FL/IoT condition and are **PHD_INELIGIBLE** as final projects. P3–P24 are **PHD_PARTIAL**; P25 is **PHD_INELIGIBLE** because its proposed Android/IoT joint task has no valid harmonized sample or label. None is **PHD_ELIGIBLE** on the inspected data, literature, client assumptions, and POC evidence. The new [G-PHD gate](Claim%20and%20Gate%20Audit.md) supersedes all earlier weighted scorecards and CASE-first recommendation text below.

**Closest mobile candidate: P11**, paired-context Android malware FL on KronoDroid. It received a three-seed CPU POC with 63,316 exact paired APKs and two deployment-motivated *simulated* context clients (emulator, physical-device collection). It is explicitly not a natural-owner or IoT-network federation. Local-only models outperformed central/FedAvg/FedProx; opposite-context transfer was near chance; the tested CASE agreement mask collapsed to chance. P11 is **PHD_PARTIAL**, not a successful detector or final recommendation.

**Closest IoT candidate: P12**, the 2026 device-indexed IoT malware DFL corpus. It aligns with IoT malware but has no mobile-app privacy/security task, and its broad DFL benchmark is already in the dataset paper. It is **PHD_PARTIAL**. P11–P25 classifications and elimination reasons are in [Research Matrix.md](Research%20Matrix.md). The roadmap and technical document remain unchanged.

> **Phase 3 (2026-09-23) update:** a CASE-agnostic search of P26-P58 with new data (LAMDA×AndroZoo markets, N-BaIoT, others) and 5-seed POCs still finds **no G-PHD-eligible project**. See the final section, *G-PHD ELIGIBILITY RESULT*.

#### Executive conclusion

**The earlier P2 recommendation is withdrawn.** P2 remains a feasible mobile-app security component: a reproducible study of **recorded claim portability, source-only recurrence prediction, and reliability-qualified report scoping** across named Android execution contexts. It adds four-state transitions, source evidence-strength tests and a narrow external replication to the original CASE. It should not be presented as the final PhD project, discovery of context sensitivity, a malware classifier, a causal Android-version study, or a formal risk-guarantee method.

SELENE is a feasible primary dataset: the shared cache contains the eight compact Parquet files (29.78 MB), and their hashes/joins were inspected. Exact pairing gives 30,746 APKs. In two package-grouped exploratory splits, source-only pooled logistic models improve Brier score over indicator-persistence baselines in both directions, but the gains are modest and asymmetric: 4.0–9.7% Brier skill. A broken-pair control removes the advantage. This supports a confirmatory test of incremental signal; it does not establish production utility.

The hard priority disallows choosing a CASE-only project. Current data cannot support a complete bridge: no independently owned compatible source/target claims, only two paired context domains for Android, no privacy intervention in the P11 POC, and no linked mobile-app/IoT-network dataset. Recent work collides with generic Android FL, personalization, drift-aware participation and reliability-weighted aggregation. The 2026 Raspberry Pi crowdsensing malware dataset is a strong IoT lead, but its paper already reports DFL experiments and it is not Android-app evidence.

Add a small, explicit **four-state estimand** so the study distinguishes stable-present, source-only, target-emergent and stable-absent recorded evidence. SELENE contains 57,745 target-emergent APK/flag rows; pooled target emergence among source-absent claims is 27.98%. Keep this separate from source-positive recurrence and do not call it behavior “emergence.”

Promote KronoDroid to an external **context-level descriptive replication**: direct file inspection yields 63,316 valid SHA pairs and a broken-pair control. Its syscall units do not equal SELENE’s semantic security indicators, and prior cross-device studies occupy the broad behavior-difference question. Treat this as a narrow robustness/replication lane, not as proof that the CASE reporting model generalizes.

Keep persistence as the key baseline, pooled logistic as the primary candidate, and raw source-side evidence counts as a secondary variant. The model should remain simple. Do not freeze a formal risk-control claim, a granularity frontier, time/family/claim OOD, analyst-time savings, or an Android-wide portability claim. Reconcile SELENE licenses and the report’s technical details, then freeze one confirmatory protocol before using outer-test outcomes.

#### Current design audit

##### What is strong

- The estimand is operational and bounded: for a source-positive APK × indicator claim, estimate whether the same **processed observation** appears in a named target context.
- The roadmap already excludes fresh device collection, malware classification, behavior truth, causal Android-version attribution, federated-learning performance, and unsupported analyst-productivity claims.
- SELENE provides exact paired SHA identities, two named Android/API contexts, source-side behavior features, and an existing reproducible exploratory base.
- The design treats source/target direction explicitly, groups by package, separates prospective baselines from retrospective intersection, and forbids target-derived threshold selection.
- The existing implementation contract is unusually strong on provenance, leakage tests, package bootstrap, tie handling, report-level aggregation, and idempotency.

##### What limits value and breadth

- Current SELENE recurrence is high (85.5–90.0% micro), so persistence already performs well. A large average-precision score can be misleading; Brier/log loss and the risk/coverage curve should lead.
- The 19 flags include exact duplicates and threshold-derived flags. They are not 19 independent behavioral concepts.
- The paired sample is selected: Android-10 paired versus unpaired prevalence differs by 3.20 points on average and 8.72 points at maximum.
- Run duration differs (median 188.33 s for Android 10 versus 143.79 s for Android 14). Context means bundled observation differences; do not claim a causal Android-version effect.
- The fidelity oracle includes only 56 shared hashes. It cannot serve as independent behavior truth or a broad high-fidelity replication.
- A single SELENE artifact cannot sustain general claims about heterogeneous Android execution, unseen time periods, families, evidence kinds, or devices.
- The current selective results are only retrospective fixed-coverage diagnostics. Calibration-only deployment-style policies have not yet been evaluated.

#### Dataset audit

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

#### PoC results

##### SELENE recurrence and model comparison

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

##### SELENE four-state and reporting diagnostics

Across 30,746 × 19 paired APK/flag cells: stable-absent `n00=148,629`; target-emergent `n01=57,745`; source-only `n10=37,919`; stable-present `n11=339,881`. Micro recurrence is 89.96% forward / 85.48% reverse. Among source-absent claims, 27.98% have a target observation; the mean indicator-specific emergence rate is 50.99%. Keep this as a distinct descriptive estimand.

At score-ranked 50% coverage on each held-out test, rich-model non-recurrence risk is approximately 0.30% forward and 3.07–3.35% reverse. At 80%, it is about 3.32–3.35% and 7.02–8.11%. Persistence is worse in these holdouts, especially at 50%. The same APK-level report proxy shows fewer unsupported claims/report. **These are retrospective diagnostics:** held-out labels determine the ranking evaluation and no calibration-only threshold was selected. They cannot support a deployed policy claim or formal risk budget.

##### KronoDroid paired context diagnostic

On 63,316 valid SHA pairs, with an app/syscall claim defined as a released count > 0:

| Direction | Source-positive claims | Recurrence | Broken-pair recurrence | Support≥100 syscall-macro recurrence |
|---|---:|---:|---:|---:|
| Emulator → device | 2,328,191 | 59.14% | 51.84% | 50.04% |
| Device → emulator | 2,007,336 | 68.59% | 60.11% | 57.70% |

This is useful external evidence of a same-app context association. It does not test CASE’s source-only prediction model or semantic reporting effect. The older [cross-device behavioral consistency study](https://doi.org/10.1016/j.mlwa.2022.100357) already covers broad cross-device behavior differences, so CASE must not claim that general finding as novel.

#### Failed, blocked and rejected ideas

- **Formal distribution-free risk control:** not implemented; package and report dependence plus target shift invalidate casual use of i.i.d. guarantees. Keep empirical risk/coverage only.
- **Evidence granularity frontier:** promising but not run. SELENE event-level layers are not local; AndroCT requires permission and 6.3 GB. Do not spend scope on a lane without exact identity/claim mappings.
- **Portability drift / future period:** not run. Current two SELENE contexts are versions, not chronological cohorts; Krono’s mod/submission dates are not verified trace times.
- **Malware-family OOD:** do not promote. Krono family disagreement is 53.4% across unique paired hashes; SELENE is not a family-held-out study.
- **Unseen-claim OOD:** 19 flags contain duplicate/derived indicators, leaving too few independent claim families to separate claim transfer from persistence.
- **Same-context repeat instability:** DYNAMISM is a strong candidate but files are restricted; no estimate was computed.
- **CIC reboot transitions:** no artifact-level identity or numerical reconciliation; reject it as a primary dataset until the join is proven.
- **Complex models (GAM, random forest, boosting, MLP, sequence):** no PoC evidence justifies added complexity. The logistic ladder already yields a repeatable modest increment; a later nonlinear comparator is a single ceiling sensitivity only.
- **Analyst-time savings, operational security impact, and federation:** not tested and should not be claimed. Report-level claim counts are an offline proxy only.

#### Best-performing feasible variants

1. **Best defensible model:** pooled direction-specific L2 logistic over claim identity, 19 source flags, event/count fields and source activity/duration. It is interpretable, CPU-only and stable across the two discovery splits.
2. **Best lean candidate:** pooled Boolean logistic; it already improves over per-indicator persistence. If the full source-count contract complicates implementation, keep this primary and demote rich features to sensitivity.
3. **Best evidence-strength variant:** raw released count features. Duration-normalized features were worse in all tested direction/split cells. Preserve normalization as a sensitivity because the direction-specific run duration differs.
4. **Best operational comparison:** persistence versus CASE risk/coverage and report proxy at 50% and 80% coverage. Treat current values as descriptive. The confirmatory protocol must choose thresholds on calibration groups only.
5. **Best external lane:** Krono exact-hash syscall recurrence and broken-pair diagnostic, with semantic scope clearly separated from SELENE.

No method should be selected solely from its largest test score. The evidence says rich features are promising but only modestly better than Boolean; all variants remain recorded in [PoC Matrix.md](PoC%20Matrix.md) and `temp/` results.

#### Novelty assessment

Broad Android context dependence, emulator/device differences, system-call inconsistency, behavior abstraction, concept drift, selective prediction, and conformal risk control are established neighboring contributions. The defensible residual is the **estimand and report operation**: estimate recurrence for a recorded source-positive APK × claim in a named target context, then make a prospective report-scope decision without interpreting non-observation as proof of absence.

Do not claim firstness. Do not claim that SELENE is ground truth. Do not claim portability across Android generally. Details and closest-work comparisons are in [Novelty Audit.md](Novelty%20Audit.md).

The comprehensive collision matrix now includes 2025–2026 Android FL, mobile malware drift, reliability-aware aggregation, federated calibration and device-level IoT DFL. It rules out generic claims such as “reliability-aware FedAvg” and “personalized Android FL” as strong residual novelty. See [Novelty Collision Matrix.md](Novelty%20Collision%20Matrix.md).

#### Candidate identities and decisive comparison

The A01–A12 and B01–B12 formulations, P1–P25 classifications, POC index and rationale are in [Research Matrix.md](Research%20Matrix.md) and [POC Matrix.md](POC%20Matrix.md). The earlier P2 weighted winner is withdrawn because it violates the hard PhD gate. CASE remains a useful mobile-app security/reporting component; it does not supply an FL/IoT result.

#### CASE component scope (not a final PhD project)

**Component title:** *CASE-Android: Reliability-Qualified Scoping of Recorded Android Behavioral-Security Evidence Across Execution Contexts*.

**Central statement:** Dynamic analysis reports record finite observations made under a particular execution context. CASE estimates whether a source-context claim is likely to recur as a recorded observation in a named target context, and exposes that estimate as a claim-scoping signal. Its result is about the released observation process, not an app’s full capability or behavior truth.

**Contribution framing:** (1) a paired claim-level portability dataset/protocol for processed Android evidence; (2) a leakage-controlled evaluation of recurrence signal beyond persistence; (3) an empirically evaluated selective reporting view; and (4) an external, semantically narrower context replication. The report mechanism and evidence semantics matter more than a new model architecture.

#### Recommended estimands

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

#### Recommended RQs

1. **RQ1 — Recorded portability structure:** How often do paired source and target contexts agree, disagree, or exhibit target-recorded evidence when source evidence was not recorded?
2. **RQ2 — Source-only signal:** Do source flags and source-run evidence properties estimate target recurrence better than global and indicator-persistence baselines under package-held-out evaluation?
3. **RQ3 — Scoping value:** Does a calibration-only CASE policy improve non-recurrence risk/coverage and retain useful claim/report content compared with persistence-based scoping?
4. **RQ4 — Boundaries and replication:** How stable are recurrence and scoping effects across direction, indicators, paired-population/fidelity sensitivities, and one independently paired context family with compatible limitations?

Keep granularity, time drift, unseen family/claim, and run stochasticity as named extension questions, not extra core RQs.

#### Recommended claims

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
| O. PhD relevance | G-PHD requires direct empirical FL malware contribution in heterogeneous IoT plus mobile-app privacy/security fit | P11 POC directly tests Android malware FL over two simulated execution contexts but local-only is stronger, no IoT-network or privacy result; P12 is IoT DFL but not app security. | Overgeneralization; two partial candidates do not jointly establish one eligible project. | **No candidate passes G-PHD.** |

The complete A–O specification and gate statuses are in [Claim and Gate Audit.md](Claim%20and%20Gate%20Audit.md).

##### Superseded CASE-only recommendation card

The following describes a viable mobile-app security component only. It is **not** the final PhD-project recommendation and cannot pass G-PHD by itself.

- **Component identity:** P2, enlarged non-federated CASE (P1 as core); **PHD_INELIGIBLE** as a final project.
- **Working title:** *CASE-Android: Reliability-Qualified Scoping of Recorded Android Behavioral-Security Evidence Across Execution Contexts*.
- **Contribution:** Estimate recurrence of source-positive recorded claims in one named paired target context from source-only evidence, test incremental value over per-indicator persistence, and evaluate its prospective report-scoping tradeoff.
- **Why it may be novel:** The residual question is the claim-level recorded-observation estimand and report operation, not cross-device variability or an FL architecture. Current evidence supports the research question, not a “first” assertion.
- **Why it adds value:** SELENE PoCs show repeatable modest source-only Brier improvement and loss of that advantage when APK pairing is broken; the four-state table makes target-recorded emergence visible without calling it new behavior.
- **PhD contribution:** No direct empirical FL/IoT contribution; fails the required PhD gate. Any link is an analogy only.
- **Book fit:** Strong for the mobile-app security/reporting part of the call; only partial for privacy. CASE does not add differential privacy, secure aggregation or a privacy-preserving learning method. Limit privacy discussion to responsible handling of sensitive trace content, claim minimization, provenance and future multi-owner implications.
- **Primary/secondary data:** SELENE / ARTEMIS primary; KronoDroid as separate, narrower syscall context replication. Do not pool ontologies.
- **Natural FL clients:** None in the CASE source datasets. P11's two contexts are simulated domains and do not constitute independent data owners.
- **Core RQs:** RQ1 four-state recorded portability; RQ2 source-only signal beyond persistence; RQ3 prospective calibrated scoping tradeoff; RQ4 external/boundary stability.
- **Core claims:** (1) bounded recorded portability heterogeneity; (2) incremental recurrence signal beyond persistence, conditional on frozen confirmation; (3) calibration-selected scoping tradeoff, conditional on future valid policy evaluation. Evidence-strength and report proxies remain secondary.
- **Core gates:** License/provenance, identity, context/claim comparability, leakage, package grouping, support, fair persistence baseline, broken-pair control, proper-score increment, calibration-only policy, external replication and reproducibility.
- **Core baselines:** global prevalence; train-only per-indicator persistence; source-volume-only; Boolean pooled logistic; raw count/rich and duration-normalized sensitivity.
- **Core evaluation:** package-grouped outer folds plus disjoint package calibration; Brier/log loss; paired package bootstrap; four-state tables; target-pair permutation; claim/indicator/package reporting; no test-selected thresholds.
- **Main risks:** single primary dataset, context bundles, modest asymmetric signal, paired-population selection, finite Monkey traces, correlated/derived indicators, no direct analyst or FL utility measurement.
- **Remove from current CASE:** discovery-of-context-dependence language, Android-wide/casual OS claims, classifier/IoT/FL performance, formal risk guarantees, analyst-savings claims, and any “first” claim.
- **Keep:** source-positive recorded-claim recurrence, exact APK pairing, persistence baseline, source-only firewall, package-grouped evaluation, broken-pair control, conservative report scoping and provenance discipline.
- **Add:** four-state transitions, target-recorded emergence, evidence-strength ladder, paired-population and duration audits, calibration-only operations, direct FL-collision analysis, honest PhD-fit limit, and a separately gated Krono replication.

**P1 is the CASE-only simpler component**, not a PhD runner-up. Under the hard gate, P11 is the closest mobile candidate but its FL result is adverse and its IoT/privacy assumptions fail; P12 is the closest IoT candidate but fails the mobile-app chapter condition and has a direct benchmark collision. There is no eligible winner.

#### Recommended gates

Use the 25 claim/data gates plus hard G-PHD in [Claim and Gate Audit.md](Claim%20and%20Gate%20Audit.md), organized as:

- **Hard project gate G-PHD:** direct malware-FL/heterogeneous-IoT empirical contribution, mobile-app privacy/security chapter fit, valid client semantics, threat model, required baselines and no arbitrary APK sharding. All checks must pass for final selection.

- **Validity gates G0–G9:** access/license; identity; context semantics; claim comparability; provenance; leakage; grouping; support; baseline fairness; negative-control integrity.
- **Claim-promotion gates G10–G24:** probability quality; richer-feature value; selective policy; risk-control validity; report-level value; temporal OOD; family OOD; claim OOD; fidelity; independent dataset/context replication; complexity; sensitivity; reproducibility; final claim wording.

A structural failure blocks only the affected dataset/claim. A small effect narrows claim strength; it does not kill the project. Formal guarantee gate G13 is required only if the report uses a guarantee label.

#### Recommended models and baselines

1. **Primary candidate:** direction-specific pooled L2 logistic with claim-indicator identity and source Boolean flags. It is simple and already outperforms persistence on both discovery splits.
2. **Secondary feature ladder:** released source evidence counts; count-per-duration variant; total activity volume; rich combined model. Keep transformations fixed before frozen evaluation.
3. **Baselines:** global train prevalence; smoothed per-indicator persistence; source activity-volume-only. Optionally Boolean CASE as the lean model. Same split, same source-positive rows, no target-side features.
4. **Do not implement every model from the candidate ladder.** One later nonlinear tabular comparator may serve as a ceiling if necessary; no MLP or sequence model is justified by current evidence.
5. **Krono replication:** separate syscall occurrence scorer only after a frozen claim definition. Do not pool its 288 syscalls with SELENE semantic indicators as if they were the same claim ontology.

#### Recommended metrics

- Primary probability: Brier and log loss; Brier skill versus persistence. Report AP only with prevalence and persistence reference.
- Paired structure: `n00/n01/n10/n11`, conditional recurrence by direction, disagreement/Jaccard or prevalence difference when useful.
- Selective reporting: risk at fixed coverage and coverage at predeclared risk target, recurrence retention, absolute risk reduction, coverage retained. Use calibration-only thresholding; descriptive fixed-rank diagnostics are labeled as such.
- Calibration: reliability curve, intercept/slope; ECE descriptive only if binning details are fixed.
- Report proxy: coverage, unsupported transferred claims/report, fraction of reports with ≥1 unsupported transfer, and recurrence retention.
- Weighting/strata: claim-micro, indicator-macro, package/report-macro; direction and rare-indicator support. Add malware/benign only where labels are semantically valid and not predictors.
- Uncertainty: paired package-cluster bootstrap; do not treat claims as independent.

Drop metrics that do not answer a stated question. Do not use test-set-selected thresholds as risk guarantees.

#### Recommended future experiment suite

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

#### Proposed confirmatory protocol

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

#### Scope boundaries

CASE still must not claim:

- that the APK cannot perform a behavior because it was not recorded;
- true behavior absence/presence, malware verdict, family attribution or malicious intent;
- a causal Android-version effect from two bundled execution environments;
- universal portability to Android versions, devices, users or observation conditions;
- formal risk guarantees without a valid dependence/shift-aware method;
- time drift from APK dates treated as execution timestamps;
- analyst time savings or operational security gains without direct measurement;
- a federated-learning or IoT result from an Android report study.

#### Roadmap change matrix

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

#### Exact section-by-section roadmap rewrite plan (conditional; no silent edits)

The classifications below refer to the current numbered sections in `docs/Roadmap.md`; they are recommendations only. **Because no candidate passes G-PHD, do not rewrite the roadmap into a final-project plan yet.** First identify eligible linked data/clients or revise the user’s hard constraint. If the user authorizes a CASE-only chapter component, apply the following edits while labeling it PHD_INELIGIBLE standalone. Do not alter the authoritative roadmap or technical document in this audit.

| Roadmap section | Action | Proposed content / reason |
|---|---|---|
| Title and authority | KEEP_WITH_EDITS | Keep CASE and “reliability-qualified scoping”; use “recorded evidence” consistently and name P2 as the enlarged version. |
| 1. Research statement | KEEP_WITH_EDITS | State the source-positive recorded-claim recurrence question and report operation, no behavior truth. Add four-state emergence as separate descriptive outcome. |
| 2. Why worth studying | KEEP_WITH_EDITS | Present the gap as prospective claim scope versus persistence/intersection; describe modest SELENE discovery results only in audit context, not as a frozen claim. |
| 3. Relationship to PhD | REWRITE | Apply G-PHD as a hard gate; report that no candidate currently passes. Describe CASE as a component only, P11 as PHD_PARTIAL with an adverse FL POC, and P12 as PHD_PARTIAL with mobile-app/book-fit failure. Do not equate methodological analogy with PhD strengthening. |
| 4. Scope / non-goals | KEEP_WITH_EDITS | Keep current no-truth boundary. Add no generic FL claim, no arbitrary APK shards, no privacy-by-local-storage claim, and no representation of P11's two context domains as natural owners or heterogeneous IoT clients. |
| 5. Pre-implementation design basis | HOLD / REWRITE CONDITIONALLY | Remove P2 as the dissertation winner. If retaining CASE as a book component, state P1/P2 are PHD_INELIGIBLE final projects; include P11 and its adverse results as a bounded appendix/substudy only. Otherwise wait for a candidate to pass G-PHD. |
| 6. Operational scenario / estimands | KEEP_WITH_EDITS | Keep exact paired source-positive recurrence, four-state transitions, target-recorded emergence, report-level proxy; distinguish predictive and descriptive populations/denominators. |
| 7. Research questions | KEEP_WITH_EDITS | Retain four RQs; make RQ4 external replication and limits, remove interpretation of family/time OOD as core. |
| 8. Dataset / provenance | KEEP_WITH_EDITS | SELENE primary; Krono separate. Add upstream dual-license checks as a gate; treat IoT crowdsensing/N-BaIoT/ToN-IoT as separate PhD data leads, not CASE data. |
| 9. Population / redundancy / exposure | KEEP | Pair-selection, runtime and indicator redundancy audits are essential and supported by artifact inspection. |
| 10. CASE mechanism | KEEP_WITH_EDITS | Keep source-only firewall, logistic ladder, scope policy and calibration-only rule. Remove architectural layers without data evidence; state non-observation caveat. |
| 11. Baselines / ablations | KEEP_WITH_EDITS | Persistence/global/activity baseline and raw/normalized count ladder. Do not add FL optimizers here; no valid clients. |
| 12. Frozen split/evaluation | KEEP_WITH_EDITS | Define disjoint package fit/calibration/test once; preserve discovery splits as exploratory only; add paired/unpaired selection and broad/non-derived sensitivity. |
| 13. Metrics | KEEP_WITH_EDITS | Lead with Brier/log loss, Brier skill, calibrated risk/coverage and package/report summaries. AP is secondary and contextualized with prevalence. |
| 14. Ties / undefined | KEEP | Retain deterministic tie and sparse-support behavior. |
| 15. Uncertainty | KEEP_WITH_EDITS | Paired package bootstrap; do not treat APK-claim rows as independent; use final frozen resample count. |
| 16. Main experiments | REWRITE | Keep CASE component experiments only if chapter authorization exists. Include the P11 3-seed CPU result in the audit record: local-only > FedAvg/FedProx, cross-context transfer near chance, CASE agreement mask near chance. Treat it as negative feasibility evidence, not a promoted detection method. |
| 17. Claim-to-evidence | REWRITE | Keep CASE claims bounded to the component. Add G-PHD outcome “no eligible candidate”; make no claim of FL/IoT strengthening based on P11. Evidence-strength conditional secondary; formal guarantee, broad context, temporal/family/claim OOD gated/deferred. |
| 18. Loopholes / threat controls | KEEP_WITH_EDITS | Define the threat model as an analyst deciding whether finite source observations transfer to a named context; do not imply adversarial FL robustness or a malware attacker model. Include APK identity crossing clients as prohibited, test-time threshold selection, global scaling, paired-selection effects, duplicate indicators, context confounding and language inflation. |
| 19. Literature position | REWRITE | Keep ADAM, AndroIDS, FL-MalDrift, M2FD, DCAA, 2026 Droidware and IoT DFL dataset as explicit collisions. P11's paired-context question does not establish a novel Android FL method; no “first” language. |
| 20. Audit vs confirmation | KEEP_WITH_EDITS | Mark all current POCs exploratory and freeze a new protocol without test outcome reuse. |
| 21. Scientific outputs | KEEP_WITH_EDITS | Outputs: four-state tables, paired model scores, calibration policy metrics, report proxy, separate Krono syscall tables, negative controls, failure logs and machine-readable manifests. Chapter contribution: evidence-bounded guidance for scoping recorded Android security claims across named execution contexts, including where evidence should remain source-specific. No FL claims. |
| 22. Gates / phases | REWRITE | Add hard G-PHD before project selection, with separate checks for IoT/client validity, Android app chapter fit, privacy threat model, and the required central/local/FedAvg/FedProx POC. Require every check to pass; partial candidates cannot be promoted. |
| 23. Final pre-frozen checklist | KEEP_WITH_EDITS | Add recent literature refresh, dual licenses, canonical POC artifact names and gate review. |
| 24. Roadmap authority | KEEP | Preserve document authority and no-silent-scope-change rule. |

The high-level comparison, 12+12 formulation dispositions, IoT challenger and decision scores are maintained in [Research Matrix.md](Research%20Matrix.md); current quantitative POCs are indexed in [POC Matrix.md](POC%20Matrix.md). The roadmap and technical document remain unchanged.

#### Prioritized next steps for the CASE component only

##### Tier 1 — Must add

- Add actual paired-population bias results and run-duration summaries to the primary evaluation.
- Keep recurrence and target emergence as distinct conditional estimands; include all four paired states.
- Retain persistence and global prevalence as mandatory baselines; report Brier skill, not AP alone.
- Add raw count / activity / normalized count feature ablations and a broad/non-derived indicator sensitivity.
- Freeze package-grouped confirmatory folds and calibration-only policy selection; promote no fixed-test threshold.
- Make broken-pair control and package bootstrap mandatory.
- Reconcile SELENE + ARTEMIS live license/citation requirements before data handling or public report output.

##### Tier 2 — Strong additions

- Add KronoDroid as a separate secondary context-family replication with a narrowly defined syscall-presence claim and same-APK SHA pairing.
- Require external model-level replication before broad claim H or general cross-context language.
- Keep the report-level proxy, but frame it as retained/unsupported recorded claims, not analyst benefit.

##### Tier 3 — Optional extensions

- AndroCT granularity–portability analysis after agreement and exact pair manifest.
- DYNAMISM same-context repeated execution if access is granted.
- CIC reboot stages if a usable identity/feature join resolves the sample discrepancy.
- Event-level SELENE granularity, chronological drift, family OOD, claim OOD and worst-context analysis after each lane’s identity/support gate passes.

##### Tier 4 — Reject or defer as standalone PhD projects

- New physical-device collection, device purchase, user recruitment or new APK runs.
- “First” claim, true behavior or absence claim, causal Android-version attribution, general Android portability.
- Formal finite-sample risk guarantee under unverified package dependence/shift.
- Deep sequence/MLP stack and broad nonlinear model tournament without incremental evidence.
- Analyst productivity/security impact and any claim that current CASE results validate FL or heterogeneous-IoT performance.

#### Proposed CASE-Android component scope

Build a source-only claim recurrence and scoping study with SELENE as the primary paired versioned-emulator dataset. Measure four-state recorded evidence transitions, compare simple persistence to pooled logistic using Boolean and a small source-count ladder, report proper probability quality and calibration-only risk/coverage, and aggregate one-APK report proxies. Use package-held-out splits, cluster uncertainty, broken-pair controls, paired-population/fidelity/exposure sensitivities and exact provenance. Add KronoDroid only as a separate syscall-level descriptive/external replication until a model-level replication is frozen. Treat AndroCT, DYNAMISM and CIC as optional gated datasets. Keep conclusions tied to the released finite observations and tested named contexts.


---

### Phase 3 — search for a G-PHD-eligible project

Date 2026-09-23. Restart rule followed: first asked what the strongest feasible mobile-malware FL question would be if CASE did not exist, then whether any CASE result helps. Existing SELENE/KronoDroid/P11 work was reused, not rerun. Roadmap and technical document untouched.

#### What was done
- Found and used previously unexploited local data: LAMDA (1,008,381 Android apps, 920 static features, labels, family, time) joined to the AndroZoo catalogue by SHA-256, giving a **natural site key (app market)** for 100 % of apps; N-BaIoT (9 device clients) as IoT replication; listed/inspected McNdroid (119 AV-vendor columns), HITL-IoT, PingPong, TU Wien Hue, moniotr, AndroidMischief, Gotham2025 and others (`Dataset Audit.md`).
- Web searches (targeted, not systematic) on Android FL, collaboration structure, client thresholds, robust aggregation vs heterogeneity, drift-aware FL, Android automotive/Things/gateway datasets, mobile+IoT paired data (`Novelty Collision Matrix.md`).
- Evaluated P26-P45, invented P46-P58 (13 lanes), ran POCs for P26-P31, P35-P40, P44, P46-P48, P52-P55, P57 (`POC Matrix.md`, `PoC Matrix.md`). Not run: P32, P33, P43, P45, P50, P51, P58; P41/P42 blocked by absent data.

#### Key findings (exploratory; 5 seeds; package-grouped)
1. Heterogeneity across markets is large: malware prevalence 14.6 %-87 %, feature JSD up to 0.022, pairwise model transfer AUC 0.52-0.98.
2. Central pooling ≥ every FL arm at all support levels; FL pays a real heterogeneity cost.
3. FedAvg beats local-only only at ≈100 samples/client (+0.030 BA), ties at 300, loses at ≥ 1000 (−0.018, −0.011). P11's "local-only > FedAvg" therefore generalises to Android app markets and has a support-dependent crossover.
4. A fixed local/global logit blend is the best simple arm from n = 300 up (n=1000: BA .889, worst-client .828 ≈ central .888/.832).
5. Client-level thresholds raise BA and halve worst-client FPR (FedAvg+FT n=1000: worst FPR .442→.239, FPR sd .167→.071). This is **score-distribution shift, not label-prior shift** (prior correction lowered BA .847→.802).
6. Negative results: measured-heterogeneity gate ≈ always-FT; transfer-graph collaboration −0.011…−0.024 BA; transferability routing/cold-start clustering no better than global (fine-tuning on 100 labelled shots is best, .841 BA); client-specific abstention worsens worst-client error; valid-set arm selection is unreliable at tiny support (N-BaIoT n=100: .959 vs oracle .992).
7. N-BaIoT in the same harness is saturated (BA ≥ .995 for central/FedAvg/FedProx/FT at n ≥ 300-1000): there is no collaboration-scope problem to solve, so it cannot serve as a same-mechanism replication.
8. Descriptive positives: Krum discards honest markets (honest BA .845→.744) and trimmed-mean outlier scores rank honest Anzhi/Play above a label-flip attacker (P44); cross-market benign JSD is 5-7× one-year temporal drift (P38).

---

### G-PHD ELIGIBILITY RESULT

**NO ELIGIBLE PROJECT**

**Working title (strongest partial, not eligible):** Client-Level Operating Points and the Cost of Federation for Android Malware Detection Across Natural App-Market Clients.

**Central scientific question:** For which client support and heterogeneity should app-market clients federate, personalise or stay local, and does client-level thresholding reduce worst-client false-positive burden?

**Why it directly strengthens the PhD:** It would give a second-domain test of the thesis principle (client-level threshold scope, FPR equity). But this is DATP's principle, and the domain is not IoT: strengthening is by analogy plus a replication that turned out saturated.

**Why it belongs in the mobile-app security chapter:** Real Android APK malware, natural store clients, package-grouped evaluation.

**Exact novelty:** None claimed. The only non-obvious residuals are (a) score-shift-not-prior-shift explanation of threshold gains on app markets, (b) honest-store vs attacker separability under robust aggregation, (c) federation-referenced drift signals confounded by store differences. Each is descriptive; none is a validated method.

**Closest competing work:** DATP (own), FedCollab and "How to Collaborate", Sentinel, Heterogeneity-Oblivious Robust FL, FL-MalDrift, M2FD, DW-FedAvg 2026, FedHGCDroid, AndroIDS, Droidware (links in `Novelty Collision Matrix.md`).

**Dataset(s):** LAMDA + AndroZoo markets (primary); N-BaIoT (replication, saturated).

**Client definition:** 7 single-market clients (play.google.com, anzhi, appchina, PlayDrone, slideme, 1mobile, angeeks); config B replaces Play with five Play era cohorts (simulated).

**Why clients are valid:** market is a natural site key with documented prevalence/feature heterogeneity; no APK shards; package-grouped splits shared across clients. Weakness: markets are crawl origins, not independent data owners.

**Heterogeneity definition:** label prevalence, per-feature Bernoulli JSD, pairwise transfer AUC, sample size.

**Threat/privacy model:** none evaluated beyond a label-flip attacker (P44); no DP/secure aggregation.

**Core method:** none passes; baseline arms: local↔FedAvg logit blend and client-level thresholds.

**Core baselines:** central, local-only, FedAvg, FedProx, FedAvg+FT, cluster FL, blend, val-selected policy, oracle arm.

**Main POC results:** table in `Research Matrix.md` (n=1000: local .882/.830, central .888/.832, FedAvg .864/.801, FedProx .872/.816, FT .872/.812, blend .889/.828, val-select .884/.822 BA/worst-client BA).

**Worst-client results:** fixed-threshold worst FPR .31-.58; local thresholds .15-.42; FedAvg worst-client BA trails local by .029 (n=1000).

**Key negative results:** gate, transfer graph, routing, abstention, shrunk thresholds, IoT saturation, prior correction, val-select at tiny n, KronoDroid P11 (local > FedAvg; CASE mask ≈ chance).

**Core RQs (if the user later relaxes the gate):** RQ1 how does FL-vs-local depend on client support; RQ2 what explains the threshold-scope benefit; RQ3 do robust aggregators separate honest heterogeneous stores from attackers.

**Core claims:** only those marked "supported (exploratory)" in `Claim and Gate Audit.md`.

**Required gates:** G-PHD-1…8; here G-PHD-4 and G-PHD-6 fail.

**Main risks:** collection-artifact prevalence; single anchor dataset; static features; AV-label bias; DATP overlap; no privacy mechanism.

**What survives from CASE:** nothing empirical for this project; CASE stays a mobile-app reporting component (Phase 1/2 conclusion).

**What is discarded from CASE:** the agreement-mask / portability-weighting hypothesis for FL, and any FL/IoT framing of SELENE.

**What changes in the roadmap:** nothing; no roadmap rewrite (no winner).

**Runner-up:** P44 (honest heterogeneity vs poisoned client). Lost because no defence method, single attack type, and generic prior art (Heterogeneity-Oblivious Robust FL, FedCC, FLAURA).

#### Precisely what is missing
1. **Data property:** a malware/malicious-behaviour corpus with (i) natural multi-device or multi-owner client identity, (ii) Android/mobile app behaviour, (iii) an IoT/edge semantic link (gateway, companion app + device, Android Things/Automotive). Nothing found in local caches or 2025-2026 searches; DYNAMISM is restricted, AndroCT needs an agreement, KronoDroid/SELENE offer two contexts only.
2. **Method property:** a collaboration mechanism that beats "central-like blend + client threshold" with heterogeneity signals; in this harness support n explains what heterogeneity statistics do not.
3. **IoT side:** N-BaIoT is saturated in this harness; an IoT set with non-trivial headroom and matching mobile task would be needed for a same-mechanism replication.

#### What would change the verdict (options for the user; none applied)
- Obtain restricted DYNAMISM / AndroCT (agreement) and test device-level clients.
- Build a mobile-companion + IoT malware capture (collection outside the scope of pre-implementation audit).
- Explicitly decide, as the author, whether the app-market federation may be treated as cross-silo edge collaboration (this **relaxes G-PHD-4** and was not done here) and whether score-vs-prior shift plus P44 constitute a sufficient G-PHD-6 contribution after a method stage.

#### Roadmap rewrite plan
Not provided: there is no winner. `docs/Roadmap.md` and `docs/technical_doc.md` remain unchanged.


---

## poc2 report (contamination-aware decision layer)

*Source: `poc2/Final Report.md` (merged 2026-09-24). *

### poc2 — Contamination-aware decision layer for federated malware detection

Date 2026-09-23. Simulation and public datasets only (no real devices). Scripts/outputs: `temp/c1_*.py`, `temp/c1_results_{mobile,nbaiot,scidb}.json`, `temp/c1_analysis_output.txt`. Earlier iterations kept in `temp/v1_nogate`, `v2_gate`, `v3_peer`.

#### Idea (C1)
Calibration pools are assumed benign but are contaminated by unlabeled malware, at *different rates per client*. Which threshold scope (local / global / robust) survives, and can federation peers repair it without labels? Complements DATP (clean calibration) and datp-cp (adversarial poison).

#### Setup
Frozen federated autoencoder (FedAvg) per domain; clients: 7 LAMDA app markets (mobile), 9 N-BaIoT devices, 8 Pi devices (SciDB, de-duplicated). Pools of 200 (60 for Pi) with contamination eps in {0,.02,.05,.10,.20}, heterogeneous (market prevalence x r; linear 0-0.3), and contaminant type random / stealth / top-score. alpha=0.05, 30 resamples x 5 seeds. Policies: LOCAL, GLOBAL (DATP B1), GLOBAL-MED, CLUSTER, oracle-eps trim, PI bands, tail-shape gate, PEER-TRIM.

#### Results
1. Contamination costs power, not FPR (matches Bashari et al., ICML 2025): N-BaIoT TPR .77 -> .48 (eps .1, random) -> .25 (eps .2); FPR stays at or below alpha. Stealth contaminants barely matter (.70); top-score contaminants are worst (.24 at eps .1).
2. Scope flips only in one domain: under heterogeneous contamination on N-BaIoT, GLOBAL keeps worst-client TPR (.37) vs LOCAL (.14) at equal mean TPR (.44 vs .42). On Pi devices and mobile no flip (mobile: LOCAL FPR sd .014 vs GLOBAL .106 even when clean -- DATP effect replicates on app markets).
3. Unsupervised tail-shape gate failed: flags only 0-10% of dirty clients (identifiability limit: with eps >= alpha the FPR band is [0, alpha/(1-eps)], uninformative).
4. PEER-TRIM (estimate contamination by comparing a client's median-normalised pool tail with peers' pools, then trim): partial, label-free recovery. Random contamination eps .1 / hetero: TPR N-BaIoT .48->.56/.63 (v2), .42->.57-.59; Pi .40->.49; mobile .18->.30. Cost: on clean pools FPR deviation rises (N-BaIoT .012->.047-.059; mobile .013->.03; Pi .020->.03). Contamination is under-estimated at eps .2 (bias -.15 to -.19); oracle-eps trimming recovers full TPR (.77), so headroom is large.

#### Novelty audit (targeted search, not systematic)
- Direct collision: Bashari et al. ICML 2025 (robust conformal outlier detection under contaminated reference data; single client, uses a labeling budget); split conformal under contamination (arXiv 2407.07700); FLANDRE (2026, contamination in FL *training*); APEW-Fed/FASC (DP quantile sketches for federated score calibration); DP conformal prediction (2025-26); "Calibration granularity, not contamination" (Future Internet 2026).
- Residual: heterogeneous per-client contamination + federated threshold scope; label-free peer-referenced contamination estimate; identifiability limit. Not found elsewhere, but not proven absent.
- Verdict: moderate novelty; current estimator is weak (biased, harms clean clients). Would need a better estimator and a scope rule that beats LOCAL on all three domains.

#### Other candidates checked
- Leakage audit: SciDB release has ~10x duplicated windows (33,354 unique of 342,106), but AE metrics change only slightly (AUC .857 leaky vs .837 de-duplicated) -> low value alone. LAMDA cross-market package overlap is modest (5.9% of rows).
- DP threshold sharing: crowded (APEW-Fed, DP conformal). Not run.
- Held-out-family collaboration value: promising, not run.

#### Ranking (novelty x feasibility x thesis fit)
1. C1 contamination-aware scope + peer-referenced trimming (needs better estimator; feasible in weeks).
2. Held-out-family collaboration value (untested; strongest FL rationale).
3. Leakage/duplicate audit (cheap; small effect).
4. DP threshold sharing (crowded).

#### Roadmap
No authoritative roadmap touched. Not declared G-PHD eligible.


#### Update (final small runs)
After N-BaIoT benign de-duplication and stricter estimators (PEER-TRIM3, PEER-ADMIT) the picture is unchanged: peer trimming gives partial label-free recovery with a clean-pool cost; the admission rule did not help. See `Paper Candidates.md` (ranking) and `Dataset Audit.md`. Cross-market identity linking (`temp/c4_repack_poc.py`) gave no detection gain.


---

## poc2 README

*Source: `poc2/README.md` (merged 2026-09-24). *

### poc2
Contamination-aware decision-layer study. See `Final Report.md`. Prior work: `../poc/`. Scratch data lives outside Git; scripts in `temp/`.


---

## Paper Candidates (poc, Phase 5)

*Source: `poc/Paper Candidates.md` (merged 2026-09-24). *

### Paper Candidates (Phase 5, 2026-09-24)

No candidate passes G-MECH + G-NOVEL. Best defensible *component/appendix* result (not a paper): **What a small verified budget buys for contaminated federated calibration** (P59): failure, oracle headroom, unlabeled correction ceiling (20-30%), pooled vs per-client verification. Would become a candidate only if a mechanism beats verified-benign+shrinkage consistently and a residual over Bashari et al. (ICML 2025) is demonstrated. Other lanes (robust aggregation vs honest heterogeneity, drift confounding, support policies, negative transfer) rejected on missing headroom. See `Final Report.md`.


---

## Paper Candidates (poc2)

*Source: `poc2/Paper Candidates.md` (merged 2026-09-24). *

### poc2 Paper Candidates (research-driven, 2026-09-23)

Searches run (targeted, not systematic): contaminated calibration/conformal outlier detection; federated contamination and thresholds; DP thresholds/quantiles; federated unlearning; membership inference on FL malware; label delay/VirusTotal dynamics; federated PII leak detection; federated zero-day and leave-one-family-out; federated XAI; cross-market repackaging; FL-malware open challenges. Small POCs only.

#### Landscape (what is already taken)
Bashari et al. ICML 2025 (contaminated reference data, conformal outlier detection, Label-Trim); split conformal under contamination (2407.07700); FLANDRE 2026 (contamination in FL training); APEW-Fed/FASC (DP quantile sketches for federated score calibration); DP conformal prediction 2025-26; federated zero-day detection with ensembles and leave-one-family-out (PLOS One, Fed-DTCN); FedDroidMeter (privacy risk of FL Android malware); label-delay studies in malware pipelines; federated XAI for IDS/malware; cross-market clone detection; FL packet classification for PII leaks (2019); federated unlearning (generic and IoT).

#### Ranked candidates
1. **Peer-referenced calibration in federated malware detection under heterogeneous contamination** (best).
   - Question: when every client's "benign" calibration pool holds a different, unknown share of malware, can federation peers repair the threshold without labels, and when should a client refuse its local threshold?
   - Novelty: moderate. Single-client theory exists (Bashari). Residual: per-client heterogeneous contamination in a federation, label-free peer reference, identifiability limit (an unlabeled pool cannot reveal eps >= alpha), cross-domain mobile and IoT.
   - Evidence (5 seeds, alpha .05, random contamination): contamination cuts TPR at unchanged FPR (N-BaIoT .77 -> .47 at 10%, .25 at 20%; mobile .29 -> .18 -> .13). Peer trimming recovers TPR (N-BaIoT .47 -> .59-.63; mobile .18 -> .26-.28; Pi .40 -> .41-.46) with FPR control kept, but harms clean pools (N-BaIoT FPR deviation .012 -> .056-.063) and under-estimates contamination (bias about -.16 at eps .2). Oracle trimming reaches .77, so the headroom is large. Under heterogeneous contamination a global threshold protected worst-client TPR on N-BaIoT (.35 vs .14) but not on Pi or mobile. A tail-shape gate and a threshold-admission rule failed.
   - Risks: estimator biased and asymmetric; needs a better estimator or a labeling budget; effect sizes depend on simulated contamination.
2. **Benchmark-validity audit for federated malware detection** (low-moderate novelty, cheap).
   - Facts: 10x duplicated windows in the Pi release, 0-18.5% duplicate benign rows in N-BaIoT, 5.9% cross-market package overlap, 22.8% cross-market label conflicts, 111,758 AVClass2 "families". Measured effect on AE metrics is small (AUC .857 vs .837). Best used as an evaluation section of candidate 1, not a paper.
3. **Cross-market identity-linked detection** (rejected): linking the same package across markets did not improve detection (AUC .97-.98 local vs .97-.98 with anchor features); anchor verdicts hurt on conflict cases.
4. **Held-out-family collaboration value; DP threshold sharing; label-lag FL; federated unlearning/XAI** (crowded or unmeasurable on these datasets; not pursued).

#### Verdict
Nothing reaches "very high novelty"; candidate 1 is the best defensible paper if the estimator is improved (e.g., better peer reference or a small labeling budget) and the claim is limited to the measured contamination models. Not declared G-PHD eligible; no roadmap change.
