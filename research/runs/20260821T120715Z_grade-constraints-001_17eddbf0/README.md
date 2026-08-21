# Experiment Run Digest — Bilateral Grade Constraint Identity Verification

**Run ID:** `20260821T120715Z_grade-constraints-001_17eddbf0`  
**Experiment ID:** `grade-constraints-001`  
**Status:** `COMPLETE`  
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > For any bilateral integer grade K in Z and radial displacement delta in R, the bilateral symmetric defect satisfies |D_K| = 4 * sinh^2(K * delta * ln(tau) / 2) identically at arbitrary precision, vanishing if and only if delta = 0 or K = 0.

- **Primary Criterion (max_abs):** `residual <= 1e-30`
- **Observed Metric:** `5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `residual` | `primary_criterion` | 60 | `0.0` | `5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` |
| `identity_error` | `criterion_component` | 60 | `0.0` | `5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` |
| `abs_D_K` | `observational_metric` | 60 | `0.0` | `0.076482880970726034915584954873985893950020240501351640438253893785480379876604674` | `0.076482880970726034915584954873985893950020240501351640438253893785480379876604674` |

---

## 3. Metric Diagnostics & Worst Points

### `residual`
- **Classification:** `primary_criterion`
- **Description:** Primary metric: residual
- **Max Absolute Value:** `5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98`
- **Argmax Parameter Point (id=10):** `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=-2, delta=-0.05, zero_index=0`
- **Top Worst Parameter Points:**
  - id=10 | `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=-2, delta=-0.05, zero_index=0`
  - id=11 | `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=-2, delta=-0.05, zero_index=1`
  - id=18 | `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=-2, delta=0.05, zero_index=0`
  - id=19 | `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=-2, delta=0.05, zero_index=1`
  - id=40 | `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=2, delta=-0.05, zero_index=0`

### `identity_error`
- **Classification:** `criterion_component`
- **Description:** Defect identity error | |D_K| - 4 sinh^2(K * delta * ln(tau) / 2) |
- **Max Absolute Value:** `5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98`
- **Argmax Parameter Point (id=10):** `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=-2, delta=-0.05, zero_index=0`
- **Top Worst Parameter Points:**
  - id=10 | `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=-2, delta=-0.05, zero_index=0`
  - id=11 | `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=-2, delta=-0.05, zero_index=1`
  - id=18 | `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=-2, delta=0.05, zero_index=0`
  - id=19 | `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=-2, delta=0.05, zero_index=1`
  - id=40 | `val=5.8520954433652479089448117673233457123937791734927291454214443173254790958424996e-98` | `K=2, delta=-0.05, zero_index=0`

### `abs_D_K`
- **Classification:** `observational_metric`
- **Description:** Bilateral symmetric defect magnitude |D_K|
- **Max Absolute Value:** `0.076482880970726034915584954873985893950020240501351640438253893785480379876604674`
- **Note:** *Observational response metric; no pass/fail criterion declared.*
- **Argmax Parameter Point (id=0):** `val=0.076482880970726034915584954873985893950020240501351640438253893785480379876604674` | `K=-3, delta=-0.05, zero_index=0`
- **Top Worst Parameter Points:**
  - id=0 | `val=0.076482880970726034915584954873985893950020240501351640438253893785480379876604674` | `K=-3, delta=-0.05, zero_index=0`
  - id=1 | `val=0.076482880970726034915584954873985893950020240501351640438253893785480379876604674` | `K=-3, delta=-0.05, zero_index=1`
  - id=8 | `val=0.076482880970726034915584954873985893950020240501351640438253893785480379876604674` | `K=-3, delta=0.05, zero_index=0`
  - id=9 | `val=0.076482880970726034915584954873985893950020240501351640438253893785480379876604674` | `K=-3, delta=0.05, zero_index=1`
  - id=50 | `val=0.076482880970726034915584954873985893950020240501351640438253893785480379876604674` | `K=3, delta=-0.05, zero_index=0`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `1c04fbf57b6e1801d3966965234991391a42cb09` (Dirty: `True`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252...`
- **Points Requested:** `60`
- **Points Completed:** `60`
- **Started At:** `2026-08-21T12:07:15.458026+00:00`
- **Completed At:** `2026-08-21T12:07:15.482426+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
