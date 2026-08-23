# Experiment Run Digest — Riemann–Weil Explicit Formula Divisor Perturbation Jacobian and Compensation Diagnostic

**Run ID:** `explicit-formula-perturbation-rank-001`
**Experiment ID:** `explicit-formula-perturbation-rank-001`
**Status:** `COMPLETE`
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**
  > Holding arithmetic data fixed while perturbing a zero orbit produces a non-zero finite divisor defect Delta C_{K,j} that is detected by the explicit formula; linearized compensation can find a minimum-norm candidate within the sampled subspace.

- **Primary Criterion (max_abs):** `defect_vector_norm >= 1e-25`
- **Observed Metric:** `1.5529373867671306901342939793794465747058776475134628465514687110003118832649899`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `defect_vector_norm` | `criterion_component` | 18 | `0.00000039679137085740183599169838599529939567936026604690863276082018845191449810589567` | `1.5529373867671306901342939793794465747058776475134628465514687110003118832649899` | `1.5529373867671306901342939793794465747058776475134628465514687110003118832649899` |
| `compensation_residual_norm` | `criterion_component` | 9 | `6.6069175728860886185596035163997524452563295509671723869940465466549948051852443e-34` | `0.000013118518127169039427854529458710267340319035580809619927684197294857745382909747` | `0.000013118518127169039427854529458710267340319035580809619927684197294857745382909747` |

---

## 3. Metric Diagnostics & Worst Points

### `defect_vector_norm`
- **Classification:** `criterion_component`
- **Description:** Defect vector L2 norm
- **Max Absolute Value:** `1.5529373867671306901342939793794465747058776475134628465514687110003118832649899`
- **Argmax Parameter Point (id=20):** `val=1.5529373867671306901342939793794465747058776475134628465514687110003118832649899` | `mode=radial_quartet, zero_index=0, epsilon=0.01`
- **Top Worst Parameter Points:**
  - id=20 | `val=1.5529373867671306901342939793794465747058776475134628465514687110003118832649899` | `mode=radial_quartet, zero_index=0, epsilon=0.01`
  - id=23 | `val=1.5529373867671306901342939793794465747058776475134628465514687110003118832649899` | `mode=radial_quartet, zero_index=9, epsilon=0.01`
  - id=26 | `val=1.5529373867671306901342939793794465747058776475134628465514687110003118832649899` | `mode=radial_quartet, zero_index=49, epsilon=0.01`
  - id=19 | `val=1.5529061848517790638879835252852498405585750207729890040364154623629713997867747` | `mode=radial_quartet, zero_index=0, epsilon=0.001`
  - id=22 | `val=1.5529061848517790638879835252852498405585750207729890040364154623629713997867747` | `mode=radial_quartet, zero_index=9, epsilon=0.001`

### `compensation_residual_norm`
- **Classification:** `criterion_component`
- **Description:** Compensation residual norm
- **Max Absolute Value:** `0.000013118518127169039427854529458710267340319035580809619927684197294857745382909747`
- **Argmax Parameter Point (id=11):** `val=0.000013118518127169039427854529458710267340319035580809619927684197294857745382909747` | `mode=critical_height, zero_index=0, epsilon=0.01`
- **Top Worst Parameter Points:**
  - id=11 | `val=0.000013118518127169039427854529458710267340319035580809619927684197294857745382909747` | `mode=critical_height, zero_index=0, epsilon=0.01`
  - id=10 | `val=0.0000013118518127169039427854529458710267340319035580809619927684197294857745382909747` | `mode=critical_height, zero_index=0, epsilon=0.001`
  - id=9 | `val=0.00000013118518127169039427854529458710267340319035580809619927684197294857745382909747` | `mode=critical_height, zero_index=0, epsilon=0.0001`
  - id=17 | `val=3.5438225898103490397813843368166253187895893959711026519468712250594249658381019e-31` | `mode=critical_height, zero_index=49, epsilon=0.01`
  - id=14 | `val=6.6069175728860886185596035163997524452563295509671723869940465466549948051852443e-32` | `mode=critical_height, zero_index=9, epsilon=0.01`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `21e81963a0272add656d543510c9d5bcd904a228` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252... (2*pi)`
- **Points Requested:** `27`
- **Points Completed:** `27`
- **Started At:** `2026-08-23T14:16:27.117142+00:00`
- **Completed At:** `2026-08-23T14:16:33.426472+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
