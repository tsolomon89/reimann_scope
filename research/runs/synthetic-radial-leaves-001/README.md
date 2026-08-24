# Experiment Run Digest — Synthetic Off-Line Radial Leaf Invariance and Defect Scaling Sweep

**Run ID:** `synthetic-radial-leaves-001`
**Experiment ID:** `synthetic-radial-leaves-001`
**Status:** `COMPLETE`
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**
  > For any synthetic off-line point s(0) = 1/2 + delta + i*gamma with injected delta != 0, the transformed point s(k) = tau^k * s(0) satisfies R_tau(s(k), k) = tau^(-k) Re(s(k)) - 1/2 = delta identically, and absolute defect |Re(s(k)) - tau^k / 2| = tau^k * |delta|.

- **Primary Criterion (max_abs):** `max_residual <= 1e-45`
- **Observed Metric:** `9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `max_residual` | `criterion_component` | 44 | `7.4888531951705853970293034599232453473555866391538452766269679838040842779011127e-109` | `9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94` | `9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94` |
| `radial_residual` | `criterion_component` | 44 | `7.4888531951705853970293034599232453473555866391538452766269679838040842779011127e-109` | `2.7252606241614667791299308648715685733797065426437702355920681935509144007420262e-108` | `2.7252606241614667791299308648715685733797065426437702355920681935509144007420262e-108` |
| `signed_defect_error` | `criterion_component` | 44 | `0.0` | `0.0` | `0.0` |
| `defect_scaling_error` | `criterion_component` | 44 | `0.0` | `9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94` | `9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94` |

---

## 3. Metric Diagnostics & Worst Points

### `max_residual`
- **Classification:** `criterion_component`
- **Description:** Combined maximum residual max(radial_residual, defect_scaling_error)
- **Max Absolute Value:** `9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94`
- **Argmax Parameter Point (id=10):** `val=9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94` | `zero_index=0, delta=-0.1, K=5`
- **Top Worst Parameter Points:**
  - id=10 | `val=9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94` | `zero_index=0, delta=-0.1, K=5`
  - id=43 | `val=9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94` | `zero_index=0, delta=0.1, K=5`
  - id=9 | `val=2.3970182936024055435037948998956424037964919494626218579646235923765162376570878e-94` | `zero_index=0, delta=-0.1, K=4`
  - id=42 | `val=2.3970182936024055435037948998956424037964919494626218579646235923765162376570878e-94` | `zero_index=0, delta=0.1, K=4`
  - id=20 | `val=1.4981364335015034646898718124347765023728074684141386612278897452353226485356799e-95` | `zero_index=0, delta=-0.01, K=4`

### `radial_residual`
- **Classification:** `criterion_component`
- **Description:** Radial coordinate error |R_tau(s, k) - delta|
- **Max Absolute Value:** `2.7252606241614667791299308648715685733797065426437702355920681935509144007420262e-108`
- **Argmax Parameter Point (id=0):** `val=2.7252606241614667791299308648715685733797065426437702355920681935509144007420262e-108` | `zero_index=0, delta=-0.1, K=-5`
- **Top Worst Parameter Points:**
  - id=0 | `val=2.7252606241614667791299308648715685733797065426437702355920681935509144007420262e-108` | `zero_index=0, delta=-0.1, K=-5`
  - id=2 | `val=2.7252606241614667791299308648715685733797065426437702355920681935509144007420262e-108` | `zero_index=0, delta=-0.1, K=-3`
  - id=3 | `val=2.7252606241614667791299308648715685733797065426437702355920681935509144007420262e-108` | `zero_index=0, delta=-0.1, K=-2`
  - id=4 | `val=2.7252606241614667791299308648715685733797065426437702355920681935509144007420262e-108` | `zero_index=0, delta=-0.1, K=-1`
  - id=5 | `val=2.7252606241614667791299308648715685733797065426437702355920681935509144007420262e-108` | `zero_index=0, delta=-0.1, K=0`

### `signed_defect_error`
- **Classification:** `criterion_component`
- **Description:** Signed defect error |(Re(s) - tau^k/2) - tau^k*delta|
- **Max Absolute Value:** `0.0`
- **Argmax Parameter Point (id=0):** `val=0.0` | `zero_index=0, delta=-0.1, K=-5`
- **Top Worst Parameter Points:**
  - id=0 | `val=0.0` | `zero_index=0, delta=-0.1, K=-5`
  - id=1 | `val=0.0` | `zero_index=0, delta=-0.1, K=-4`
  - id=2 | `val=0.0` | `zero_index=0, delta=-0.1, K=-3`
  - id=3 | `val=0.0` | `zero_index=0, delta=-0.1, K=-2`
  - id=4 | `val=0.0` | `zero_index=0, delta=-0.1, K=-1`

### `defect_scaling_error`
- **Classification:** `criterion_component`
- **Description:** Absolute defect scaling error | |Re(s) - tau^k/2| - tau^k*|delta| |
- **Max Absolute Value:** `9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94`
- **Argmax Parameter Point (id=10):** `val=9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94` | `zero_index=0, delta=-0.1, K=5`
- **Top Worst Parameter Points:**
  - id=10 | `val=9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94` | `zero_index=0, delta=-0.1, K=5`
  - id=43 | `val=9.5880731744096221740151795995825696151859677978504874318584943695060649506283513e-94` | `zero_index=0, delta=0.1, K=5`
  - id=9 | `val=2.3970182936024055435037948998956424037964919494626218579646235923765162376570878e-94` | `zero_index=0, delta=-0.1, K=4`
  - id=42 | `val=2.3970182936024055435037948998956424037964919494626218579646235923765162376570878e-94` | `zero_index=0, delta=0.1, K=4`
  - id=20 | `val=1.4981364335015034646898718124347765023728074684141386612278897452353226485356799e-95` | `zero_index=0, delta=-0.01, K=4`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `a8368d5d1a2b9b1801cd8cc60fea26beb53cb108` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252... (2*pi)`
- **Points Requested:** `44`
- **Points Completed:** `44`
- **Started At:** `2026-08-24T14:46:34.642248+00:00`
- **Completed At:** `2026-08-24T14:46:35.328744+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
