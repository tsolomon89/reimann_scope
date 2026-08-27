# Experiment Run Digest — Transcendental Continuation Actual Zero Worldline Invariant Sweep

**Run ID:** `transcendental-worldlines-001`
**Experiment ID:** `transcendental-worldlines-001`
**Status:** `COMPLETE`
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**
  > For any actual critical-line zero rho = 1/2 + i*gamma (delta = 0), the transformed point s_rho(k) = tau^k * rho is an exact zero of Z_tau(s, k), and its normalized radial coordinate R_tau(s_rho(k), k) = 0 identically.

- **Primary Criterion (max_abs):** `max_residual <= 1e-35`
- **Observed Metric:** `4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `max_residual` | `criterion_component` | 33 | `6.1772373841355150313365816210135629005986137204355296188943269305078809269212743e-40` | `4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39` | `4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39` |
| `zeta_residual` | `criterion_component` | 33 | `6.1772373841355150313365816210135629005986137204355296188943269305078809269212743e-40` | `4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39` | `4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39` |
| `radial_residual` | `criterion_component` | 33 | `0.0` | `4.1581639062579596874121618322727625471158171233502750009033692303187586218218283e-112` | `4.1581639062579596874121618322727625471158171233502750009033692303187586218218283e-112` |

---

## 3. Metric Diagnostics & Worst Points

### `max_residual`
- **Classification:** `criterion_component`
- **Description:** Combined maximum residual max(zeta_residual, radial_residual)
- **Max Absolute Value:** `4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39`
- **Argmax Parameter Point (id=11):** `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39` | `zero_index=1, delta=0.0, K=-5`
- **Top Worst Parameter Points:**
  - id=11 | `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39` | `zero_index=1, delta=0.0, K=-5`
  - id=12 | `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658027825e-39` | `zero_index=1, delta=0.0, K=-4`
  - id=13 | `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658027825e-39` | `zero_index=1, delta=0.0, K=-3`
  - id=14 | `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658027825e-39` | `zero_index=1, delta=0.0, K=-2`
  - id=15 | `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658027825e-39` | `zero_index=1, delta=0.0, K=-1`

### `zeta_residual`
- **Classification:** `criterion_component`
- **Description:** Residual of Z_tau at transformed zero point
- **Max Absolute Value:** `4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39`
- **Argmax Parameter Point (id=11):** `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39` | `zero_index=1, delta=0.0, K=-5`
- **Top Worst Parameter Points:**
  - id=11 | `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658259573e-39` | `zero_index=1, delta=0.0, K=-5`
  - id=12 | `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658027825e-39` | `zero_index=1, delta=0.0, K=-4`
  - id=13 | `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658027825e-39` | `zero_index=1, delta=0.0, K=-3`
  - id=14 | `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658027825e-39` | `zero_index=1, delta=0.0, K=-2`
  - id=15 | `val=4.9344784536429921804934358231243654710334708809244720258861308310492763658027825e-39` | `zero_index=1, delta=0.0, K=-1`

### `radial_residual`
- **Classification:** `criterion_component`
- **Description:** Radial coordinate error |R_tau(s, k) - 0|
- **Max Absolute Value:** `4.1581639062579596874121618322727625471158171233502750009033692303187586218218283e-112`
- **Argmax Parameter Point (id=0):** `val=4.1581639062579596874121618322727625471158171233502750009033692303187586218218283e-112` | `zero_index=0, delta=0.0, K=-5`
- **Top Worst Parameter Points:**
  - id=0 | `val=4.1581639062579596874121618322727625471158171233502750009033692303187586218218283e-112` | `zero_index=0, delta=0.0, K=-5`
  - id=11 | `val=4.1581639062579596874121618322727625471158171233502750009033692303187586218218283e-112` | `zero_index=1, delta=0.0, K=-5`
  - id=22 | `val=4.1581639062579596874121618322727625471158171233502750009033692303187586218218283e-112` | `zero_index=2, delta=0.0, K=-5`
  - id=1 | `val=0.0` | `zero_index=0, delta=0.0, K=-4`
  - id=2 | `val=0.0` | `zero_index=0, delta=0.0, K=-3`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `02955a091f9df252f2be454aaaf1c0be566bbe39` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252... (2*pi)`
- **Points Requested:** `33`
- **Points Completed:** `33`
- **Started At:** `2026-08-27T14:19:51.636077+00:00`
- **Completed At:** `2026-08-27T14:19:52.227402+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
