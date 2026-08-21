# Experiment Run Digest — Bilateral Symmetric Defect and Hyperbolic Scaling Invariant Sweep

**Run ID:** `20260821T143605Z_grade-constraints-001_5bd3da56`  
**Experiment ID:** `grade-constraints-001`  
**Status:** `COMPLETE`  
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > The bilateral defect D_K = (tau^(K*delta) - 1)*(1 - tau^(-K*delta)) satisfies |D_K| = 4*sinh^2(K*delta*ln(tau)/2) identically, vanishing if and only if delta = 0 or K = 0.

- **Primary Criterion (max_abs):** `identity_error <= 1e-50`
- **Observed Metric:** `7.4906821675075173234493590621738825118640373420706933061394487261766132426783994e-96`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `identity_error` | `criterion_component` | 105 | `0.0` | `7.4906821675075173234493590621738825118640373420706933061394487261766132426783994e-96` | `7.4906821675075173234493590621738825118640373420706933061394487261766132426783994e-96` |
| `abs_D_K` | `observational_metric` | 105 | `0.0` | `4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` |
| `expected_abs_D_K` | `observational_metric` | 105 | `0.0` | `4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` |

---

## 3. Metric Diagnostics & Worst Points

### `identity_error`
- **Classification:** `criterion_component`
- **Description:** Defect identity absolute error
- **Max Absolute Value:** `7.4906821675075173234493590621738825118640373420706933061394487261766132426783994e-96`
- **Argmax Parameter Point (id=0):** `val=7.4906821675075173234493590621738825118640373420706933061394487261766132426783994e-96` | `zero_index=0, delta=-0.1, K=-10`
- **Top Worst Parameter Points:**
  - id=0 | `val=7.4906821675075173234493590621738825118640373420706933061394487261766132426783994e-96` | `zero_index=0, delta=-0.1, K=-10`
  - id=20 | `val=7.4906821675075173234493590621738825118640373420706933061394487261766132426783994e-96` | `zero_index=0, delta=-0.1, K=10`
  - id=84 | `val=7.4906821675075173234493590621738825118640373420706933061394487261766132426783994e-96` | `zero_index=0, delta=0.1, K=-10`
  - id=104 | `val=7.4906821675075173234493590621738825118640373420706933061394487261766132426783994e-96` | `zero_index=0, delta=0.1, K=10`
  - id=1 | `val=3.7453410837537586617246795310869412559320186710353466530697243630883066213391997e-96` | `zero_index=0, delta=-0.1, K=-9`

### `abs_D_K`
- **Classification:** `observational_metric`
- **Description:** Observed bilateral defect magnitude |D_K|
- **Max Absolute Value:** `4.4423402502714818126941705299315201304287984444906680906975565286745296102066445`
- **Note:** *Observational response metric; no pass/fail criterion declared.*
- **Argmax Parameter Point (id=0):** `val=4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `zero_index=0, delta=-0.1, K=-10`
- **Top Worst Parameter Points:**
  - id=0 | `val=4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `zero_index=0, delta=-0.1, K=-10`
  - id=20 | `val=4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `zero_index=0, delta=-0.1, K=10`
  - id=84 | `val=4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `zero_index=0, delta=0.1, K=-10`
  - id=104 | `val=4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `zero_index=0, delta=0.1, K=10`
  - id=1 | `val=3.419582789290407627458118825094116095649146056989868872789347759249511240989067` | `zero_index=0, delta=-0.1, K=-9`

### `expected_abs_D_K`
- **Classification:** `observational_metric`
- **Description:** Theoretically expected defect magnitude 4*sinh^2(K*delta*ln(tau)/2)
- **Max Absolute Value:** `4.4423402502714818126941705299315201304287984444906680906975565286745296102066445`
- **Note:** *Observational response metric; no pass/fail criterion declared.*
- **Argmax Parameter Point (id=0):** `val=4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `zero_index=0, delta=-0.1, K=-10`
- **Top Worst Parameter Points:**
  - id=0 | `val=4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `zero_index=0, delta=-0.1, K=-10`
  - id=20 | `val=4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `zero_index=0, delta=-0.1, K=10`
  - id=84 | `val=4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `zero_index=0, delta=0.1, K=-10`
  - id=104 | `val=4.4423402502714818126941705299315201304287984444906680906975565286745296102066445` | `zero_index=0, delta=0.1, K=10`
  - id=1 | `val=3.419582789290407627458118825094116095649146056989868872789347759249511240989067` | `zero_index=0, delta=-0.1, K=-9`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `624ce7b4bbfd93a547871022b9d884533fa5c207` (Dirty: `True`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252...`
- **Points Requested:** `105`
- **Points Completed:** `105`
- **Started At:** `2026-08-21T14:36:05.424219+00:00`
- **Completed At:** `2026-08-21T14:36:05.473680+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
