# CASE-Android Dataset Audit

Audit snapshot: 2026-09-23. This file records files inspected locally, metadata checked online, and access or semantic limits. It does not alter `docs/Roadmap.md`.

## Dataset disposition

| Dataset | Access and inspected artifact | Identity/pairing | Context and fields | CASE decision |
|---|---|---|---|---|
| SELENE / ARTEMIS | Eight compact Parquet files already present in the shared data cache; 29,777,711 bytes total. | 30,746 exact SHA-256 pairs. Run-feature hashes are unique within each version. 22,475 package groups among paired rows. | Android 10/API 29 and Android 14/API 34; both `strace`, Monkey, and `completed_behavior`. Released L1 flags plus event counts, volumes, duration, event timing, ratios, and derived summaries. | **PRIMARY** for semantic claim-level CASE. Restrict claims to finite, processed evidence in these two emulator contexts. |
| KronoDroid | Public four-file CSV release streamed and parsed in memory from the maintainer repository; 25,679,248 compressed bytes across four archives. | SHA-256 is present. 63,320 intersecting hashes before duplicate handling; **63,316** one-to-one pairs after excluding four duplicate-hash identities per context. No malware/benign disagreement remains among valid pairs. Family labels disagree on 33,838/63,316 pairs. | Emulator versus real-device syscall count profiles, 288 syscall fields plus `nr_syscalls`, static/manifest fields, and APK metadata. The 288 dynamic fields have identical names/order and no missing values in the downloaded rows. | **CORE REPLICATION / SECONDARY** for direction-specific recurrence and broken-pair validation. Do not use this release for family-OOD claims without label reconciliation. |
| AndroCT | Zenodo metadata and README inspected; 6.3 GB release. Per the release, reuse requires a faculty member or person in a permanent position to agree to its terms; no redistribution or commercial use. No trace archive extracted in this audit. | The release describes 35,974 apps with emulator and real-device traces; this is the **nominal** pairing count. Exact APK-hash join and duplicate count remain unverified from the released archive. | Ten-minute Monkey-driven method-call traces on an emulator and Samsung Galaxy S4. Method-call edges carry full method signatures. Same Android platform version and same-length/input-coverage criteria are described. 18,277 benign and 17,697 malicious apps. | **OPTIONAL / BLOCKED pending agreement and artifact-level identity audit.** Very useful for abstraction/granularity follow-up; high direct novelty collision for cross-device behavior differences. |
| DYNAMISM 2016–2023 | Zenodo record is public but files are marked **Restricted**; no archive was accessible locally. | Maintainer metadata says filenames preserve AndroZoo hashes. Same-app 2nd-run subset: 1,049 benign and 772 malware. | Android 9 container; 20,000 Monkey events or five-minute limit; one-second aggregates. First-run filtered set: 12,706 benign and 10,560 malware; failed runs are numerous and class-skewed. | **DIAGNOSTIC / BLOCKED** until file access is granted. Best candidate for same-context execution-instability comparison if authorized. |
| CIC-InvesAndMal2019 | Official UNB dataset page inspected; files not present in shared cache, no state tables extracted. | Page gives no stable SHA-256/run-identity contract for joining `AfterInstall`, `Before`, and `After`. | Three captures around reboot on physical devices; API calls, logs, network flows, battery/process/package data. | **BLOCKED** as a CASE dataset until exact app and comparable-feature pairing is verified. Publisher numbers conflict: “5,000” installed samples versus 426 malware + 5,065 benign (=5,491). |
| TraceDroid | Local shared cache contains 85 files totaling 45,181,835 bytes, including historical per-year profile tables and feature archives. | SHA-like APK filenames are present in annual profiles. No same-APK paired execution contexts are described by the dataset record. | Historical static/dynamic profiles for apps from 2010–2017; function-call profiles were collected under a single analysis setup. | **DIAGNOSTIC / DEFER** for historical cohort or feature drift only. It does not estimate same-APK cross-context recurrence. |
| AndroZoo metadata | Shared cache has a multi-gigabyte latest metadata dump; it is an APK metadata catalog, not a set of paired dynamic traces. | APK hashes and dates support cohort definitions, not target dynamic evidence. | Metadata only. | **REJECT** as a CASE outcome dataset; may be used only to resolve external metadata, subject to access terms. |
| AndroidMischief / AntiARA / other local Android artifacts | Local directories exist, but the initial file inventory found no paired, comparable same-APK context traces for the CASE estimand. | No verified cross-context pair manifest. | Malware action/evasion artifacts, not a paired report-evidence table. | **DIAGNOSTIC** for background only; do not add absent a specific paired estimand. |

## SELENE / ARTEMIS: direct artifact audit

The local external cache is `/home/naslouby/Projects/datp-shared-data/raw/SELENE` (not part of this repository and not copied into it). The eight files and their row counts are:

| Artifact | Android 10 rows | Android 14 rows | Fields observed | Bytes, A10 / A14 |
|---|---:|---:|---|---:|
| `analyses` | 44,485 | 30,751 | 20 each: exact hash/run IDs, Android/API, observer, input method, status, duration, trace and source artifact metadata | 3,876,547 / 2,686,400 |
| `run_features` | 44,485 | 30,751 | 82 each; includes 19 `has_*` flags, semantic event counts, event totals/diversity/severity buckets, first/last event time, active duration, syscall/resource counts, ratios, and derived behavior scores | 9,990,871 / 7,296,134 |
| `fidelity_oracle` | 1,000 | 1,000 | 50 each; raw artifact availability, raw evidence and signals for parser/fidelity checks | 1,389,463 / 1,755,546 |
| `fidelity_evidence` | 49,345 | 54,944 | 9 each; signal, artifact path/type, line and matched text | 1,237,029 / 1,545,721 |

The eight local Parquet files total **29,777,711 bytes**. Their SHA-256 checksums are captured in `temp/progress.md`. This exact local inventory is smaller than the complete public SELENE artifact card: no `events_l05`, `events_l1`, lifecycle tables, or context-representation files were present in this cache. The public release card describes 73,635,326 / 86,050,148 L0.5 events and 73,673,283 / 82,843,224 L1 events in the two contexts, but those layers were not locally audited row by row here.

Actual `analyses` values: all Android 10 rows are version 10/API 29 and all Android 14 rows are version 14/API 34; both contexts report `strace`, Monkey, and `completed_behavior`. Median run duration is **188.33 seconds** in Android 10 and **143.79 seconds** in Android 14 (ranges 25.56–659.82 and 21.01–651.74 seconds). This difference is a plausible measurement-exposure covariate; it prevents causal attribution of observed differences to Android version alone.

The paired run-feature population is 30,746 hashes (30,746 shared; 13,739 Android-10-only; 5 Android-14-only). The paired Android-10 feature distribution is selected: versus Android-10-only rows, mean absolute indicator-prevalence difference is **3.20 percentage points**, and the maximum absolute difference is **8.72 points**. This is material for external validity and must appear in the main report.

Across all 30,746 paired APKs × 19 flags, the four-state table is: `n00` stable absent **148,629**, `n01` target-emergent **57,745**, `n10` source-only **37,919**, `n11` stable present **339,881**. Thus micro recurrence is 89.96% in 10→14 and 85.48% in 14→10; target-emergence probability among source-absent claims is 27.98%. Indicator-macro recurrence is 85.52% / 79.63%, and indicator-macro emergence among source-absent cases is 50.99%. These descriptive numbers support keeping emergence as a distinct secondary estimand; they do not support treating a source non-observation as a proof of target absence.

The fidelity oracle has 1,000 records per context but only **56 shared hashes**. It can support limited parser/provenance auditing, not independent ground truth or broad context-level risk guarantees. Fidelity-evidence text and paths may expose raw strings; only aggregate summaries should be published.

### Source-only predictor eligibility

For the PoC, source-side input was restricted to the source `run_features` row: the 19 released flags, released semantic/syscall count fields, total event/activity fields, and source duration. No target-side fields, target metadata, hashes, package names, malware labels, or family labels entered the model. Hash is used only to form the one-to-one pair; `package_name` is used only as the grouping variable. `family`, selection/run identifiers, derived triage scores, and raw fidelity text are excluded from predictors.

The 19 flags are not 19 independent behaviors. At least these overlaps are visible in the released table: `has_NETWORK_EXTERNAL` and `has_external_tcp` match exactly in source context; `has_PROCESS_MEMORY_READ` and `has_process_vm_readv` also match; the two `*_high_volume` flags are threshold-derived from count columns. Future evaluation should retain the released 19-flag result for reconciliation and add a predeclared broad/non-derived sensitivity. It must not interpret the 19-row indicator macro as 19 independent discoveries.

**Access/licensing:** the public SELENE card specifies a dedicated SELENE data license plus the upstream ARTEMIS license and mandatory citation to both papers. The card states that raw malware-controlled endpoints, paths, identifiers, and credential-shaped strings are not redacted. Respect both licenses and keep raw strings out of public artifacts. The roadmap currently describes its earlier license characterization; reconcile exact license text and citations against the live dataset card before protocol freeze.

## KronoDroid: actual CSV findings

The four public CSV archives were fetched from the maintainer GitHub release and parsed in memory; no APKs or extracted dataset files were retained. The archive sizes are approximately 6.1 MB emulator-benign, 5.4 MB emulator-malware, 5.8 MB real-device-benign, and 8.3 MB real-device-malware. The full four-archive extraction is practical for CPU-only local analysis; the audit completed in seconds on the current WSL host. Peak RAM was not measured.

| Check | Actual result |
|---|---|
| Rows | Emulator: 35,246 benign + 28,745 malware = 63,991. Device: 36,755 benign + 41,382 malware = 78,137. |
| Total schema | 484 columns in concatenated contexts. The release README advertises 200 static + 289 dynamic (=489), which does not reconcile with these current CSVs. Emulator benign versus malware schemas also differ by `FilesInsideAPK`. Resolve this count discrepancy before implementation. |
| Dynamic schema | Exactly 289 aligned columns in the same order across contexts; `nr_syscalls` is an aggregate field, leaving 288 syscall count columns. No missing values were found in those dynamic fields. |
| Identity | Exact `sha256` field in both contexts. Raw overlap is 63,320 hashes. There are four duplicate-hash groups in each context, each with conflicting `Malware` labels; excluding non-unique identities yields 63,316 one-to-one pairs. All remaining paired malware/benign labels agree. |
| Label caveat | `MalFamily` disagrees on 33,838 of 63,316 unique-hash pairs (46.6% agreement). Do not use family identity for OOD splits until this is explained. |
| Time fields | The inspected CSVs expose APK metadata fields such as `FirstModDate`/`LastModDate` or `EarliestModDate`/`HighestModDate`, plus `TimesSubmitted`. Names differ by context. These are not verified as execution/capture timestamps; they do not yet validate portability drift or future-period evaluation. |

Syscall presence was defined as count > 0, yielding app × syscall recorded-evidence claims. On exact pairs, emulator→device recurrence was **59.14%** among 2,328,191 source-positive app/syscall claims; reverse recurrence was **68.59%** among 2,007,336. The support≥100 syscall-macro recurrence was 50.04% and 57.70%. Malware/benign pooled recurrence was 63.20% / 55.75% emulator→device and 65.31% / 72.01% in reverse. These are descriptive: features are system-call occurrences, not semantically named security claims.

The broken-pair negative control randomly permuted target APK rows. Pooled recurrence then fell to 51.84% and 60.11%; true pairing therefore adds about **7.29** and **8.48 percentage points** over that shuffled control. This supports a genuine same-APK association, but it does not establish a predictive CASE model or report-scoping benefit.

## Other candidate audit notes

### AndroCT

The current Zenodo record is [10.5281/zenodo.6336104](https://zenodo.org/records/6336104); the archive is 6.3 GB. Its README describes per-app traces under both context families, 10-minute execution, Android Monkey, emulator and Samsung Galaxy S4, with 35,974 unique apps across 2010–2019. The public terms require a faculty/permanent-position agreement, prohibit redistribution and commercial use, and require citation. Because that agreement was not verified, do not treat the artifact as an authorized CASE dataset in this audit. It is still the strongest optional granularity follow-up: method edges can be grouped to class/package/API family, but the same fact makes “emulator/device behavior differs” a direct novelty collision.

### DYNAMISM

The current [Zenodo record](https://zenodo.org/records/21280255) is explicitly Restricted. Its metadata are unusually well matched to the same-context instability question: Android 9, 1-second summaries, repeated traces for 1,821 apps, and original AndroZoo hashes in filenames. However, run-level pairing, feature schemas, and missingness cannot be checked until the files are accessible. The class-skewed run failures make complete-case selection a prominent risk.

### CIC-InvesAndMal2019

The [official UNB page](https://www.unb.ca/cic/datasets/invesandmal2019.html) defines AfterInstall, Before, and After captures, including around restart. It gives a contradictory sample total and no audited exact identity key or comparable-feature manifest. Keep the reboot idea as a promising blocked lane; do not infer stage pairing from matching folder names.

### TraceDroid and related datasets

The [TraceDroid Zenodo record](https://zenodo.org/records/3665877) covers historical app profiles and static/dynamic function-call data, but it is not a repeated same-APK/multi-context release. It can inform a separate historical cohort question after same-hash and feature semantics are verified; it cannot substitute for the recurrence outcome. Android-in-the-Wild is a device-control interaction dataset rather than a dynamic security-evidence dataset. Android device-specific behavior studies are important prior work, not fresh evidence for CASE. The local AndroidMischief and AntiARA directories contain action/evasion material but no verified paired same-APK evidence table in the inspected inventory.

## References checked

- [SELENE Android Paper Artifacts dataset card](https://huggingface.co/datasets/serrooT/selene-android-paper-artifacts) and [dataset README/license and limitations](https://huggingface.co/datasets/serrooT/selene-android-paper-artifacts/blob/main/README.md).
- [AndroCT current Zenodo record](https://zenodo.org/records/6336104) and [published MSR 2021 dataset paper](https://doi.org/10.1109/MSR52588.2021.00076).
- [KronoDroid repository and release README](https://github.com/aleguma/kronodroid) and [dataset paper](https://doi.org/10.1016/j.cose.2021.102399).
- [CIC-InvesAndMal2019 official data page](https://www.unb.ca/cic/datasets/invesandmal2019.html).
- [DYNAMISM 2016–2023 Zenodo record](https://zenodo.org/records/21280255).
- [TraceDroid Zenodo record](https://zenodo.org/records/3665877).
