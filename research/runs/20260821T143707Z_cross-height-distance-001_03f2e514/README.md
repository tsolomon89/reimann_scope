# Experiment Run Digest — Cross-Height Trajectory Distance and Norm Sweep

**Run ID:** `20260821T143707Z_cross-height-distance-001_03f2e514`  
**Experiment ID:** `cross-height-distance-001`  
**Status:** `COMPLETE`  
**Criterion Outcome:** **INCOMPLETE / INVALID**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > Derivative-normalized paths P_n(u) from different height blocks lie within an O(Delta_n) bounded envelope around the leading linear term u.

- **Primary Criterion (max):** `max_distance <= 2.0`
- **Observed Metric:** `N/A`
- **Criterion Met:** `None`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `max_distance` | `criterion_component` | 0 | `N/A` | `N/A` | `N/A` |

---

## 3. Metric Diagnostics & Worst Points

### `max_distance`
- **Classification:** `criterion_component`
- **Description:** Maximum normalized trajectory distance ||P_m - P_n||
- **Max Absolute Value:** `N/A`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `624ce7b4bbfd93a547871022b9d884533fa5c207` (Dirty: `True`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252...`
- **Points Requested:** `3`
- **Points Completed:** `3`
- **Started At:** `2026-08-21T14:37:07.055285+00:00`
- **Completed At:** `2026-08-21T14:37:08.607488+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
