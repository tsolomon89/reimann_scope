# Experiment Run Digest — Centered coordinate dilation zero-map preservation and function residual

**Run ID:** `20260820T134412Z_centered-dilation-zero-map-001_7ca0768c`  
**Experiment ID:** `centered-dilation-zero-map-001`  
**Status:** `COMPLETE`  
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**  
  > Under centered coordinate dilation s' = 1/2 + tau^K(s - 1/2), the algebraically predicted zero positions rho' = 1/2 + tau^K(rho - 1/2) yield vanishing function values f_K(rho') = 0 with residual <= 1e-25 at 80 dps.

- **Primary Criterion (max_abs):** `residual <= 1e-25`
- **Observed Metric:** `7.5805791207702920299719205622983354262578734264994515501672489906977062141173564e-42`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `residual` | `primary_criterion` | 15 | `1.189450589751380830005571823271358594978611027859858364311401964626651980406783e-64` | `7.5805791207702920299719205622983354262578734264994515501672489906977062141173564e-42` | `7.5805791207702920299719205622983354262578734264994515501672489906977062141173564e-42` |

---

## 3. Metric Diagnostics & Worst Points

### `residual`
- **Classification:** `primary_criterion`
- **Description:** Primary metric: residual
- **Max Absolute Value:** `7.5805791207702920299719205622983354262578734264994515501672489906977062141173564e-42`
- **Argmax Parameter Point (id=2):** `val=7.5805791207702920299719205622983354262578734264994515501672489906977062141173564e-42` | `mode=centered_dilation, k=-1.0, gamma=25.01085758014568876321379099256282181865955519888407429345827115`
- **Top Worst Parameter Points:**
  - id=2 | `val=7.5805791207702920299719205622983354262578734264994515501672489906977062141173564e-42` | `mode=centered_dilation, k=-1.0, gamma=25.01085758014568876321379099256282181865955519888407429345827115`
  - id=5 | `val=7.5805791207702920299719205622983354262578734264994515501672489906977062141173564e-42` | `mode=centered_dilation, k=-0.5, gamma=25.01085758014568876321379099256282181865955519888407429345827115`
  - id=8 | `val=7.5805791207702920299719205622983354262578734264994515501672489906977062141173564e-42` | `mode=centered_dilation, k=0.0, gamma=25.01085758014568876321379099256282181865955519888407429345827115`
  - id=11 | `val=7.5805791207702920299719205622983354262578734264994515501672489906977062141173564e-42` | `mode=centered_dilation, k=0.5, gamma=25.01085758014568876321379099256282181865955519888407429345827115`
  - id=14 | `val=7.5805791207702920299719205622983354262578734264994515501672489906977062141173564e-42` | `mode=centered_dilation, k=1.0, gamma=25.01085758014568876321379099256282181865955519888407429345827115`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `340f9c09347278cc1f4f1bb9b88642bcd0aac3f4` (Dirty: `True`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252...`
- **Points Requested:** `15`
- **Points Completed:** `15`
- **Started At:** `2026-08-20T13:44:12.916320+00:00`
- **Completed At:** `2026-08-20T13:44:12.980533+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
