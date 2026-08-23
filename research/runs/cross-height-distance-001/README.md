# Experiment Run Digest — Cross-Height Trajectory Distance and Norm Sweep

**Run ID:** `cross-height-distance-001`
**Experiment ID:** `cross-height-distance-001`
**Status:** `COMPLETE`
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**
  > Derivative-normalized paths P_n(u) from different height blocks lie within an O(Delta_n) bounded envelope around the leading linear term u on compact sampling intervals.

- **Primary Criterion (max):** `max_distance <= 2.0`
- **Observed Metric:** `0.38240592176751609848014585791416788604882581986114612998519056028673809479739175`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `max_distance` | `criterion_component` | 3 | `0.13350697972097460935409208904331846947946151196025828414122284177608080343896453` | `0.38240592176751609848014585791416788604882581986114612998519056028673809479739175` | `0.38240592176751609848014585791416788604882581986114612998519056028673809479739175` |
| `L_infty_distance` | `observational_metric` | 3 | `0.13350697972097460935409208904331846947946151196025828414122284177608080343896453` | `0.38240592176751609848014585791416788604882581986114612998519056028673809479739175` | `0.38240592176751609848014585791416788604882581986114612998519056028673809479739175` |
| `L_2_distance` | `observational_metric` | 3 | `0.054316411931935703912087286231740359879125975361367446363097800582439536143769959` | `0.17246299341930178879295986113935151447075013349518755897654881806805469731470391` | `0.17246299341930178879295986113935151447075013349518755897654881806805469731470391` |

---

## 3. Metric Diagnostics & Worst Points

### `max_distance`
- **Classification:** `criterion_component`
- **Description:** Maximum normalized trajectory L_infty distance ||P_m - P_n||_infty
- **Max Absolute Value:** `0.38240592176751609848014585791416788604882581986114612998519056028673809479739175`
- **Argmax Parameter Point (id=0):** `val=0.38240592176751609848014585791416788604882581986114612998519056028673809479739175` | `block_pair=low_to_medium, zero_index=0, u_max=0.5`
- **Top Worst Parameter Points:**
  - id=0 | `val=0.38240592176751609848014585791416788604882581986114612998519056028673809479739175` | `block_pair=low_to_medium, zero_index=0, u_max=0.5`
  - id=2 | `val=0.2848326345065421874651171528651159018543817272359346633803749590352522279203261` | `block_pair=low_to_very_high, zero_index=0, u_max=0.5`
  - id=1 | `val=0.13350697972097460935409208904331846947946151196025828414122284177608080343896453` | `block_pair=low_to_high, zero_index=0, u_max=0.5`

### `L_infty_distance`
- **Classification:** `observational_metric`
- **Description:** Discrete supremum path distance L_infty
- **Max Absolute Value:** `0.38240592176751609848014585791416788604882581986114612998519056028673809479739175`
- **Note:** *Observational response metric; no pass/fail criterion declared.*
- **Argmax Parameter Point (id=0):** `val=0.38240592176751609848014585791416788604882581986114612998519056028673809479739175` | `block_pair=low_to_medium, zero_index=0, u_max=0.5`
- **Top Worst Parameter Points:**
  - id=0 | `val=0.38240592176751609848014585791416788604882581986114612998519056028673809479739175` | `block_pair=low_to_medium, zero_index=0, u_max=0.5`
  - id=2 | `val=0.2848326345065421874651171528651159018543817272359346633803749590352522279203261` | `block_pair=low_to_very_high, zero_index=0, u_max=0.5`
  - id=1 | `val=0.13350697972097460935409208904331846947946151196025828414122284177608080343896453` | `block_pair=low_to_high, zero_index=0, u_max=0.5`

### `L_2_distance`
- **Classification:** `observational_metric`
- **Description:** Root-mean-square path distance L_2
- **Max Absolute Value:** `0.17246299341930178879295986113935151447075013349518755897654881806805469731470391`
- **Note:** *Observational response metric; no pass/fail criterion declared.*
- **Argmax Parameter Point (id=0):** `val=0.17246299341930178879295986113935151447075013349518755897654881806805469731470391` | `block_pair=low_to_medium, zero_index=0, u_max=0.5`
- **Top Worst Parameter Points:**
  - id=0 | `val=0.17246299341930178879295986113935151447075013349518755897654881806805469731470391` | `block_pair=low_to_medium, zero_index=0, u_max=0.5`
  - id=2 | `val=0.12632567377502783394312549701280023497500813123100975790829228762538091344526929` | `block_pair=low_to_very_high, zero_index=0, u_max=0.5`
  - id=1 | `val=0.054316411931935703912087286231740359879125975361367446363097800582439536143769959` | `block_pair=low_to_high, zero_index=0, u_max=0.5`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `72aac6eefa0665b2348c729cefa0e534dc6e932a` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252... (2*pi)`
- **Points Requested:** `3`
- **Points Completed:** `3`
- **Started At:** `2026-08-23T20:32:09.085656+00:00`
- **Completed At:** `2026-08-23T20:32:18.105852+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
