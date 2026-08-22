# Experiment Run Digest — Trivial Zero Transcendental Continuation Worldline Invariant Sweep

**Run ID:** `trivial-worldlines-001`
**Experiment ID:** `trivial-worldlines-001`
**Status:** `COMPLETE`
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**
  > For any trivial zero s_m = -2m (m in Z+), the continuation point s_m(K) = tau^K * (-2m) satisfies Z_tau(s_m(K), K) = 0 identically, and has normalized radial leaf coordinate R_tau(s_m(K), K) = -2m - 1/2 != 0.

- **Primary Criterion (max_abs):** `max_residual <= 1e-35`
- **Observed Metric:** `1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `max_residual` | `criterion_component` | 50 | `0.0` | `1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93` | `1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93` |
| `zeta_residual` | `criterion_component` | 50 | `0.0` | `1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93` | `1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93` |
| `radial_residual` | `criterion_component` | 50 | `0.0` | `1.4981364335015034646898718124347765023728074684141386612278897452353226485356799e-95` | `1.4981364335015034646898718124347765023728074684141386612278897452353226485356799e-95` |

---

## 3. Metric Diagnostics & Worst Points

### `max_residual`
- **Classification:** `criterion_component`
- **Description:** Combined maximum residual max(zeta_residual, radial_residual)
- **Max Absolute Value:** `1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93`
- **Argmax Parameter Point (id=45):** `val=1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93` | `trivial_index=10, K=-2`
- **Top Worst Parameter Points:**
  - id=45 | `val=1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93` | `trivial_index=10, K=-2`
  - id=49 | `val=8.8817160092033184087326441847655878175026202477906655662124228705994802513539599e-94` | `trivial_index=10, K=2`
  - id=48 | `val=7.3194708887006948338349114007791358551779679052951455009104512559124828484131495e-94` | `trivial_index=10, K=1`
  - id=44 | `val=1.1642239627864529720747441903506655959188913130196251490422195107500752200216775e-94` | `trivial_index=9, K=2`
  - id=40 | `val=9.9388533226414291421413044424670657522543887698171043070060825028177532334880603e-95` | `trivial_index=9, K=-2`

### `zeta_residual`
- **Classification:** `criterion_component`
- **Description:** Residual of Z_tau at transformed trivial zero point
- **Max Absolute Value:** `1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93`
- **Argmax Parameter Point (id=45):** `val=1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93` | `trivial_index=10, K=-2`
- **Top Worst Parameter Points:**
  - id=45 | `val=1.6535796073871116603092502764262975132529204063851442652634946707448450879181566e-93` | `trivial_index=10, K=-2`
  - id=49 | `val=8.8817160092033184087326441847655878175026202477906655662124228705994802513539599e-94` | `trivial_index=10, K=2`
  - id=48 | `val=7.3194708887006948338349114007791358551779679052951455009104512559124828484131495e-94` | `trivial_index=10, K=1`
  - id=44 | `val=1.1642239627864529720747441903506655959188913130196251490422195107500752200216775e-94` | `trivial_index=9, K=2`
  - id=40 | `val=9.9388533226414291421413044424670657522543887698171043070060825028177532334880603e-95` | `trivial_index=9, K=-2`

### `radial_residual`
- **Classification:** `criterion_component`
- **Description:** Radial coordinate error |R_tau(s, K) - (-2m - 1/2)|
- **Max Absolute Value:** `1.4981364335015034646898718124347765023728074684141386612278897452353226485356799e-95`
- **Argmax Parameter Point (id=25):** `val=1.4981364335015034646898718124347765023728074684141386612278897452353226485356799e-95` | `trivial_index=6, K=-2`
- **Top Worst Parameter Points:**
  - id=25 | `val=1.4981364335015034646898718124347765023728074684141386612278897452353226485356799e-95` | `trivial_index=6, K=-2`
  - id=30 | `val=1.4981364335015034646898718124347765023728074684141386612278897452353226485356799e-95` | `trivial_index=7, K=-2`
  - id=34 | `val=1.4981364335015034646898718124347765023728074684141386612278897452353226485356799e-95` | `trivial_index=7, K=2`
  - id=10 | `val=7.4906821675075173234493590621738825118640373420706933061394487261766132426783994e-96` | `trivial_index=3, K=-2`
  - id=0 | `val=0.0` | `trivial_index=1, K=-2`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `c42abca1318ae5031b1972af785ef49e772d359c` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252... (2*pi)`
- **Points Requested:** `50`
- **Points Completed:** `50`
- **Started At:** `2026-08-22T22:01:27.704474+00:00`
- **Completed At:** `2026-08-22T22:01:27.876903+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
