# Experiment Run Digest — Coupled macroscope scaling of off-critical zero perturbations in explicit formula reconstruction

**Run ID:** `20260820T135950Z_macroscope-perturbation-001_24f0213c`  
**Experiment ID:** `macroscope-perturbation-001`  
**Status:** `COMPLETE`  
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > Under simultaneous origin coordinate dilation A = tau^k and synthetic zero perturbation delta != 0, the arithmetic residual Delta pi_N is measured under coupled coordinate normalization across both single-pair diagnostic and symmetry-complete quartet modes at 80 dps.

- **Primary Criterion (max_abs):** `residual >= 0.0`
- **Observed Metric:** `0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `residual` | `primary_criterion` | 120 | `0.0` | `0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` |
| `delta_cj` | `perturbation_response` | 120 | `-0.0062268890204092154766638853307250725156857170878245247232307289285718965525515844` | `0.0064162382405602060291945001213488467180119762787309519470616158278920595254851929` | `0.0064162382405602060291945001213488467180119762787309519470616158278920595254851929` |
| `delta_cpi` | `perturbation_response` | 120 | `-0.0080477145190561907760096488896415691671921134040470038212107133784532539490746552` | `0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` |
| `delta_pi_n` | `perturbation_response` | 120 | `-0.0080477145190561907760096488896415691671921134040470038212107133784532539490746552` | `0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` |

---

## 3. Metric Diagnostics & Worst Points

### `residual`
- **Classification:** `primary_criterion`
- **Description:** Primary metric: residual
- **Max Absolute Value:** `0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388`
- **Argmax Parameter Point (id=42):** `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=-2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
- **Top Worst Parameter Points:**
  - id=42 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=-2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=46 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=-1, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=50 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=0, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=54 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=1, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=58 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`

### `delta_cj`
- **Classification:** `perturbation_response`
- **Description:** Isolated single-zero J contribution shift Delta C_J
- **Max Absolute Value:** `0.0064162382405602060291945001213488467180119762787309519470616158278920595254851929`
- **Argmax Parameter Point (id=42):** `val=0.0064162382405602060291945001213488467180119762787309519470616158278920595254851929` | `zero_index=0, delta=0.01, k=-2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
- **Top Worst Parameter Points:**
  - id=42 | `val=0.0064162382405602060291945001213488467180119762787309519470616158278920595254851929` | `zero_index=0, delta=0.01, k=-2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=46 | `val=0.0064162382405602060291945001213488467180119762787309519470616158278920595254851929` | `zero_index=0, delta=0.01, k=-1, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=50 | `val=0.0064162382405602060291945001213488467180119762787309519470616158278920595254851929` | `zero_index=0, delta=0.01, k=0, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=54 | `val=0.0064162382405602060291945001213488467180119762787309519470616158278920595254851929` | `zero_index=0, delta=0.01, k=1, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=58 | `val=0.0064162382405602060291945001213488467180119762787309519470616158278920595254851929` | `zero_index=0, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`

### `delta_cpi`
- **Classification:** `perturbation_response`
- **Description:** Isolated single-zero pi contribution shift Delta C_pi
- **Max Absolute Value:** `0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388`
- **Argmax Parameter Point (id=42):** `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=-2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
- **Top Worst Parameter Points:**
  - id=42 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=-2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=46 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=-1, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=50 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=0, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=54 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=1, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=58 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`

### `delta_pi_n`
- **Classification:** `perturbation_response`
- **Description:** Full spectrum reconstructed prime count shift Delta pi_N(x)
- **Max Absolute Value:** `0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388`
- **Argmax Parameter Point (id=42):** `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=-2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
- **Top Worst Parameter Points:**
  - id=42 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=-2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=46 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=-1, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=50 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=0, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=54 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=1, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`
  - id=58 | `val=0.0082598292550106921342543088657797066545416327402134138695650988143570052415038388` | `zero_index=0, delta=0.01, k=2, x=20.0, num_zeros=10, perturbation_mode=single_pair_diagnostic`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `340f9c09347278cc1f4f1bb9b88642bcd0aac3f4` (Dirty: `True`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252...`
- **Points Requested:** `120`
- **Points Completed:** `120`
- **Started At:** `2026-08-20T13:59:50.096678+00:00`
- **Completed At:** `2026-08-20T14:05:55.092001+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
