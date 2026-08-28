# Experiment Run Digest — Cross-Height Path Coherence and Taylor Shape Metric Sweep

**Run ID:** `cross-height-path-coherence-001`
**Experiment ID:** `cross-height-path-coherence-001`
**Status:** `COMPLETE`
**Criterion Outcome:** **OBSERVATIONAL / NO CRITERION DECLARED**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**
  > Derivative-normalized trajectories P_n(u) = zeta(s_n(u)) / [i * Delta_n * zeta'(rho_n)] evaluated at verified simple zeros share common local geometric structures across spectrum blocks.

- **Primary Criterion:** `N/A (Observational)`
- **Observed Metric:** `N/A`
- **Criterion Met:** `null (Observational)`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `zeta_residual` | `observational_metric` | 60 | `9.2276457241903664452649216898289727359325326239446637884415490748462600712483747e-78` | `1.959987133393609569533775075844783089603082075334671114667267382320539894654549e-62` | `1.959987133393609569533775075844783089603082075334671114667267382320539894654549e-62` |
| `abs_c2` | `observational_metric` | 60 | `3.1510887211586578936362910344682922854414047174106530649336890000151674709344852` | `3.6040238317678523695568867754748901539668189886200331684653356226742979856467196` | `3.6040238317678523695568867754748901539668189886200331684653356226742979856467196` |
| `abs_c3` | `observational_metric` | 60 | `6.5143648210060392127973773083456161892901189628537519614453500368875759764307264` | `8.9884726726457715427427084966263261886944580506259509747438037207374134217565024` | `8.9884726726457715427427084966263261886944580506259509747438037207374134217565024` |
| `abs_P_n` | `observational_metric` | 60 | `3.1196570097674775082727232041211816367891942616403840206428668396609231427917691e-78` | `0.61708873686807776296292175566971470450883983051685091817580179601757214082047956` | `0.61708873686807776296292175566971470450883983051685091817580179601757214082047956` |

---

## 3. Metric Diagnostics & Worst Points

### `zeta_residual`
- **Classification:** `observational_metric`
- **Description:** Zeta residual at zero ordinate |zeta(1/2 + i*gamma)|
- **Max Absolute Value:** `1.959987133393609569533775075844783089603082075334671114667267382320539894654549e-62`
- **Note:** *Observational response metric; no pass/fail criterion declared.*
- **Argmax Parameter Point (id=40):** `val=1.959987133393609569533775075844783089603082075334671114667267382320539894654549e-62` | `block=high_research, zero_index=2, u=-0.5`
- **Top Worst Parameter Points:**
  - id=40 | `val=1.959987133393609569533775075844783089603082075334671114667267382320539894654549e-62` | `block=high_research, zero_index=2, u=-0.5`
  - id=41 | `val=1.959987133393609569533775075844783089603082075334671114667267382320539894654549e-62` | `block=high_research, zero_index=2, u=-0.2`
  - id=42 | `val=1.959987133393609569533775075844783089603082075334671114667267382320539894654549e-62` | `block=high_research, zero_index=2, u=0.0`
  - id=43 | `val=1.959987133393609569533775075844783089603082075334671114667267382320539894654549e-62` | `block=high_research, zero_index=2, u=0.2`
  - id=44 | `val=1.959987133393609569533775075844783089603082075334671114667267382320539894654549e-62` | `block=high_research, zero_index=2, u=0.5`

### `abs_c2`
- **Classification:** `observational_metric`
- **Description:** Second-order Taylor shape coefficient magnitude |c_{2,n}|
- **Max Absolute Value:** `3.6040238317678523695568867754748901539668189886200331684653356226742979856467196`
- **Note:** *Observational response metric; no pass/fail criterion declared.*
- **Argmax Parameter Point (id=55):** `val=3.6040238317678523695568867754748901539668189886200331684653356226742979856467196` | `block=very_high_sparse, zero_index=2, u=-0.5`
- **Top Worst Parameter Points:**
  - id=55 | `val=3.6040238317678523695568867754748901539668189886200331684653356226742979856467196` | `block=very_high_sparse, zero_index=2, u=-0.5`
  - id=56 | `val=3.6040238317678523695568867754748901539668189886200331684653356226742979856467196` | `block=very_high_sparse, zero_index=2, u=-0.2`
  - id=57 | `val=3.6040238317678523695568867754748901539668189886200331684653356226742979856467196` | `block=very_high_sparse, zero_index=2, u=0.0`
  - id=58 | `val=3.6040238317678523695568867754748901539668189886200331684653356226742979856467196` | `block=very_high_sparse, zero_index=2, u=0.2`
  - id=59 | `val=3.6040238317678523695568867754748901539668189886200331684653356226742979856467196` | `block=very_high_sparse, zero_index=2, u=0.5`

### `abs_c3`
- **Classification:** `observational_metric`
- **Description:** Third-order Taylor shape coefficient magnitude |c_{3,n}|
- **Max Absolute Value:** `8.9884726726457715427427084966263261886944580506259509747438037207374134217565024`
- **Note:** *Observational response metric; no pass/fail criterion declared.*
- **Argmax Parameter Point (id=55):** `val=8.9884726726457715427427084966263261886944580506259509747438037207374134217565024` | `block=very_high_sparse, zero_index=2, u=-0.5`
- **Top Worst Parameter Points:**
  - id=55 | `val=8.9884726726457715427427084966263261886944580506259509747438037207374134217565024` | `block=very_high_sparse, zero_index=2, u=-0.5`
  - id=56 | `val=8.9884726726457715427427084966263261886944580506259509747438037207374134217565024` | `block=very_high_sparse, zero_index=2, u=-0.2`
  - id=57 | `val=8.9884726726457715427427084966263261886944580506259509747438037207374134217565024` | `block=very_high_sparse, zero_index=2, u=0.0`
  - id=58 | `val=8.9884726726457715427427084966263261886944580506259509747438037207374134217565024` | `block=very_high_sparse, zero_index=2, u=0.2`
  - id=59 | `val=8.9884726726457715427427084966263261886944580506259509747438037207374134217565024` | `block=very_high_sparse, zero_index=2, u=0.5`

### `abs_P_n`
- **Classification:** `observational_metric`
- **Description:** Derivative-normalized path magnitude |P_n(u)|
- **Max Absolute Value:** `0.61708873686807776296292175566971470450883983051685091817580179601757214082047956`
- **Note:** *Observational response metric; no pass/fail criterion declared.*
- **Argmax Parameter Point (id=15):** `val=0.61708873686807776296292175566971470450883983051685091817580179601757214082047956` | `block=medium_research, zero_index=0, u=-0.5`
- **Top Worst Parameter Points:**
  - id=15 | `val=0.61708873686807776296292175566971470450883983051685091817580179601757214082047956` | `block=medium_research, zero_index=0, u=-0.5`
  - id=59 | `val=0.58329607383970510863198293371646086210379344395501090776196108809313169314799925` | `block=very_high_sparse, zero_index=2, u=0.5`
  - id=50 | `val=0.5664391618937471915917855616550553842516096877641489302981742478655220047220332` | `block=very_high_sparse, zero_index=1, u=-0.5`
  - id=45 | `val=0.5169200327693551815256110730082299704193648002012507627053795562374157280432781` | `block=very_high_sparse, zero_index=0, u=-0.5`
  - id=40 | `val=0.47311874026491906667782197528762323260470351544398624007436466309570404597155572` | `block=high_research, zero_index=2, u=-0.5`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `de87edd24b96e49ddf63538d8e0924a0246195fd` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252... (2*pi)`
- **Points Requested:** `60`
- **Points Completed:** `60`
- **Started At:** `2026-08-28T19:47:33.941335+00:00`
- **Completed At:** `2026-08-28T19:48:00.021643+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
