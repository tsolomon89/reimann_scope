# Experiment Run Digest — Isolated off-critical radial perturbation of Riemann zeros and prime reconstruction response

**Run ID:** `20260820T130413Z_isolated-radial-perturbation-001_124c130a`  
**Experiment ID:** `isolated-radial-perturbation-001`  
**Status:** `COMPLETE`  
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > For a selected reference zero rho_n = 1/2 + i*gamma_n, an off-critical radial perturbation delta = Re(rho) - 1/2 != 0 produces a nonzero isolated converter deformation Delta C_J and reconstructed prime count shift Delta pi_N, with delta = 0 exactly recovering baseline (Delta pi_N = 0) across both single-pair diagnostic and symmetry-complete quartet modes at 80 dps.

- **Primary Criterion:** `residual >= 0.0`
- **Observed Metric:** `0.366951471936781181693021380851860158145427703857421875`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `residual` | `primary_criterion` | 126 | `0.0` | `0.366951471936781181693021380851860158145427703857421875` | `0.366951471936781181693021380851860158145427703857421875` |
| `delta_cj` | `perturbation_response` | 126 | `-0.1784063035215965042912245053230435587465763092041015625` | `0.25058011142007063920544851498561911284923553466796875` | `0.25058011142007063920544851498561911284923553466796875` |
| `delta_cpi` | `perturbation_response` | 126 | `-0.322257389297858243271122091755387373268604278564453125` | `0.366951471936781181693021380851860158145427703857421875` | `0.366951471936781181693021380851860158145427703857421875` |
| `delta_pi_n` | `perturbation_response` | 126 | `-0.322257389297858243271122091755387373268604278564453125` | `0.366951471936781181693021380851860158145427703857421875` | `0.366951471936781181693021380851860158145427703857421875` |

---

## 3. Metric Diagnostics & Worst Points

### `residual`
- **Classification:** `primary_criterion`
- **Description:** Primary criterion metric: residual
- **Max Absolute Value:** `0.366951471936781181693021380851860158145427703857421875`
- **Argmax Parameter Point (id=3):** `zero_index=0, delta=-0.05, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
- **Top Worst Parameter Points:**
  - id=3 | `val=0.366951471936781181693021380851860158145427703857421875` | `zero_index=0, delta=-0.05, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=39 | `val=0.366951471936781181693021380851860158145427703857421875` | `zero_index=0, delta=0.05, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=9 | `val=0.361852059072685416918346845704945735633373260498046875` | `zero_index=0, delta=-0.01, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=33 | `val=0.361852059072685416918346845704945735633373260498046875` | `zero_index=0, delta=0.01, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=15 | `val=0.3616420653413177088708607698208652436733245849609375` | `zero_index=0, delta=-0.001, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`

### `delta_cj`
- **Classification:** `perturbation_response`
- **Description:** Isolated single-zero J contribution shift Delta C_J
- **Max Absolute Value:** `0.25058011142007063920544851498561911284923553466796875`
- **Argmax Parameter Point (id=5):** `zero_index=0, delta=-0.05, x=50.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
- **Top Worst Parameter Points:**
  - id=5 | `val=0.25058011142007063920544851498561911284923553466796875` | `zero_index=0, delta=-0.05, x=50.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=41 | `val=0.25058011142007063920544851498561911284923553466796875` | `zero_index=0, delta=0.05, x=50.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=11 | `val=0.2418062782300085533648825730779208242893218994140625` | `zero_index=0, delta=-0.01, x=50.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=35 | `val=0.2418062782300085533648825730779208242893218994140625` | `zero_index=0, delta=0.01, x=50.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=17 | `val=0.241445489712646066404744260580628179013729095458984375` | `zero_index=0, delta=-0.001, x=50.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`

### `delta_cpi`
- **Classification:** `perturbation_response`
- **Description:** Isolated single-zero pi contribution shift Delta C_pi
- **Max Absolute Value:** `0.366951471936781181693021380851860158145427703857421875`
- **Argmax Parameter Point (id=3):** `zero_index=0, delta=-0.05, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
- **Top Worst Parameter Points:**
  - id=3 | `val=0.366951471936781181693021380851860158145427703857421875` | `zero_index=0, delta=-0.05, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=39 | `val=0.366951471936781181693021380851860158145427703857421875` | `zero_index=0, delta=0.05, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=9 | `val=0.361852059072685416918346845704945735633373260498046875` | `zero_index=0, delta=-0.01, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=33 | `val=0.361852059072685416918346845704945735633373260498046875` | `zero_index=0, delta=0.01, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=15 | `val=0.3616420653413177088708607698208652436733245849609375` | `zero_index=0, delta=-0.001, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`

### `delta_pi_n`
- **Classification:** `perturbation_response`
- **Description:** Full spectrum reconstructed prime count shift Delta pi_N(x)
- **Max Absolute Value:** `0.366951471936781181693021380851860158145427703857421875`
- **Argmax Parameter Point (id=3):** `zero_index=0, delta=-0.05, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
- **Top Worst Parameter Points:**
  - id=3 | `val=0.366951471936781181693021380851860158145427703857421875` | `zero_index=0, delta=-0.05, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=39 | `val=0.366951471936781181693021380851860158145427703857421875` | `zero_index=0, delta=0.05, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=9 | `val=0.361852059072685416918346845704945735633373260498046875` | `zero_index=0, delta=-0.01, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=33 | `val=0.361852059072685416918346845704945735633373260498046875` | `zero_index=0, delta=0.01, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`
  - id=15 | `val=0.3616420653413177088708607698208652436733245849609375` | `zero_index=0, delta=-0.001, x=20.0, num_zeros=10, perturbation_mode=symmetry_complete_quartet`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `10be6b46af780f66dab638540ec67e0dfaaf9d2e` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252...`
- **Points Requested:** `126`
- **Points Completed:** `126`
- **Started At:** `2026-08-20T13:04:13.414985+00:00`
- **Completed At:** `2026-08-20T13:05:29.455448+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
