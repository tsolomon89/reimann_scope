# Experiment Run Digest — Coupled coordinate covariance invariance of clean and perturbed converter waves

**Run ID:** `20260820T180313Z_coupled-perturbation-covariance-001_0d4e4b51`  
**Experiment ID:** `coupled-perturbation-covariance-001`  
**Status:** `COMPLETE`  
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > Under simultaneous origin coordinate dilation A = tau^k, s' = A*s, x' = x^(1/A), rho_clean' = A*rho_clean, and rho_pert' = A*rho_pert, both clean single-zero converter contributions C_J(x', rho_clean') = C_J(x, rho_clean) and perturbed converter contributions C_J(x', rho_pert') = C_J(x, rho_pert) are exact mathematical identities, achieving maximum absolute covariance residual <= 1e-25 across single-pair diagnostic and symmetry-complete split modes at 80 dps.

- **Primary Criterion (max_abs):** `covariance_residual <= 1e-25`
- **Observed Metric:** `1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `covariance_residual` | `primary_criterion` | 120 | `0.0` | `1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94` | `1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94` |
| `clean_cj_residual` | `criterion_component` | 120 | `0.0` | `9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95` | `9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95` |
| `pert_cj_residual` | `criterion_component` | 120 | `0.0` | `1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94` | `1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94` |
| `delta_cj_residual` | `criterion_component` | 120 | `0.0` | `2.7797453355984927567487855894785892133870451074090463440751860507296025705251873e-96` | `2.7797453355984927567487855894785892133870451074090463440751860507296025705251873e-96` |

---

## 3. Metric Diagnostics & Worst Points

### `covariance_residual`
- **Classification:** `primary_criterion`
- **Description:** Primary metric: covariance_residual
- **Max Absolute Value:** `1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94`
- **Argmax Parameter Point (id=79):** `val=1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94` | `zero_index=1, delta=-0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_split`
- **Top Worst Parameter Points:**
  - id=79 | `val=1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94` | `zero_index=1, delta=-0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_split`
  - id=119 | `val=1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94` | `zero_index=1, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_split`
  - id=99 | `val=1.8159052160762364261455750914004341745557896775347938538242741716660961634399276e-94` | `zero_index=1, delta=0.0, k=2, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_split`
  - id=118 | `val=9.3559565918412214187433549501919356830783975192290602715875230118980981832082861e-95` | `zero_index=1, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=78 | `val=9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95` | `zero_index=1, delta=-0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`

### `clean_cj_residual`
- **Classification:** `criterion_component`
- **Description:** Clean converter wave covariance residual |C_J(x^(1/A), A*rho_0) - C_J(x, rho_0)|
- **Max Absolute Value:** `9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95`
- **Argmax Parameter Point (id=78):** `val=9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95` | `zero_index=1, delta=-0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
- **Top Worst Parameter Points:**
  - id=78 | `val=9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95` | `zero_index=1, delta=-0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=79 | `val=9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95` | `zero_index=1, delta=-0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_split`
  - id=98 | `val=9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95` | `zero_index=1, delta=0.0, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=99 | `val=9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95` | `zero_index=1, delta=0.0, k=2, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_split`
  - id=118 | `val=9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95` | `zero_index=1, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`

### `pert_cj_residual`
- **Classification:** `criterion_component`
- **Description:** Perturbed converter wave covariance residual |C_J(x^(1/A), A*rho_pert) - C_J(x, rho_pert)|
- **Max Absolute Value:** `1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94`
- **Argmax Parameter Point (id=79):** `val=1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94` | `zero_index=1, delta=-0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_split`
- **Top Worst Parameter Points:**
  - id=79 | `val=1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94` | `zero_index=1, delta=-0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_split`
  - id=119 | `val=1.8164904256205729509364695725771665091270290554521431267388163160978287113495119e-94` | `zero_index=1, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_split`
  - id=99 | `val=1.8159052160762364261455750914004341745557896775347938538242741716660961634399276e-94` | `zero_index=1, delta=0.0, k=2, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_split`
  - id=118 | `val=9.3559565918412214187433549501919356830783975192290602715875230118980981832082861e-95` | `zero_index=1, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=98 | `val=9.0779292233806687373689766713030154721947506340526973226313982719155291358407478e-95` | `zero_index=1, delta=0.0, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`

### `delta_cj_residual`
- **Classification:** `criterion_component`
- **Description:** Converter perturbation response covariance residual |Delta C_J' - Delta C_J|
- **Max Absolute Value:** `2.7797453355984927567487855894785892133870451074090463440751860507296025705251873e-96`
- **Argmax Parameter Point (id=118):** `val=2.7797453355984927567487855894785892133870451074090463440751860507296025705251873e-96` | `zero_index=1, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
- **Top Worst Parameter Points:**
  - id=118 | `val=2.7797453355984927567487855894785892133870451074090463440751860507296025705251873e-96` | `zero_index=1, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=78 | `val=2.6974502434261689580292491740006046643065075877818048404676969900172130207399021e-96` | `zero_index=1, delta=-0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=56 | `val=5.7057930572811167112211914731402620695839346941554109167859082093923421184464371e-97` | `zero_index=0, delta=0.01, k=2, x=10.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=16 | `val=5.5594906711969855134975711789571784267740902148180926881503721014592051410503746e-97` | `zero_index=0, delta=-0.01, k=2, x=10.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=65 | `val=4.6816763546921983271558494138586765699150233387941833163371554538603832766739996e-97` | `zero_index=1, delta=-0.01, k=-1, x=10.0, num_zeros=10, perturbation_mode=symmetry_complete_split`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `987ccb58f331306e001a6f2c6ba2845a707f761f` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252...`
- **Points Requested:** `120`
- **Points Completed:** `120`
- **Started At:** `2026-08-20T18:03:13.011596+00:00`
- **Completed At:** `2026-08-20T18:03:13.685437+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
