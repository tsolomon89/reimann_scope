# Experiment Run Digest — Riemann–Weil Explicit Formula Radial Second-Variation and Non-Negative Energy Analysis

**Run ID:** `explicit-formula-radial-second-variation-001`
**Experiment ID:** `explicit-formula-radial-second-variation-001`
**Status:** `COMPLETE`
**Criterion Outcome:** **CRITERION MET**

---

## 1. Mathematical Statement & Criterion

- **Hypothesis:**
  > Radial zero-orbit displacement delta produces a leading second-order defect Delta C_h = -2 delta^2 h''(gamma) + O(delta^4) with strictly positive quadratic radial energy E(u) = u^T K^T K u; non-negativity u_n = delta_n^2 >= 0 prevents exact non-negative least-squares compensation across the sampled test family under fixed arithmetic data.

- **Primary Criterion (max_abs):** `relative_second_order_error <= 0.01`
- **Observed Metric:** `0.0003289246365900508287095260762751405467533010995001401432654816361226234528648121`
- **Criterion Met:** `True`

*Note: This result applies strictly to the evaluated finite parameter space. It does not constitute proof or refutation of broader conjectures.*

---

## 2. Multi-Metric Summary

| Metric | Classification | Count | Min | Max | Max Abs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `relative_second_order_error` | `criterion_component` | 16 | `0.000000015624999916993876057771485070932565463841160297789286205035521172817706943538559` | `0.0003289246365900508287095260762751405467533010995001401432654816361226234528648121` | `0.0003289246365900508287095260762751405467533010995001401432654816361226234528648121` |
| `exact_radial_defect_norm` | `diagnostic` | 16 | `0.0000001250000019674017412050294114052662604256495774567885719919350266305035963064543` | `0.001251031312900599654913452341810993086419966901466935871616133199731702902757793` | `0.001251031312900599654913452341810993086419966901466935871616133199731702902757793` |
| `linear_second_order_norm` | `diagnostic` | 16 | `0.00000012500000001427672118438881353937342859802465381051997413668251349082013530286921` | `0.0012508446492353363222116923825195450584213293816138232918143358484952840288984693` | `0.0012508446492353363222116923825195450584213293816138232918143358484952840288984693` |
| `quadratic_ratio` | `diagnostic` | 16 | `4.0` | `4.0004477` | `4.0004477` |
| `quadratic_energy` | `diagnostic` | 16 | `0.000000000000015625000003569180296301028152620133476350711920902653618103125043362107401019158` | `0.0000015646123365206715597630537083693936459213718080573626502511260113962955432162321` | `0.0000015646123365206715597630537083693936459213718080573626502511260113962955432162321` |
| `nnls_residual_norm` | `diagnostic` | 16 | `0.00000000000000025548926025817578737495826574344258065045183932358644885782566619141460161143675` | `0.0012495192334332076146253221474642769182837673185998199034192237216629430542016144` | `0.0012495192334332076146253221474642769182837673185998199034192237216629430542016144` |

---

## 3. Metric Diagnostics & Worst Points

### `relative_second_order_error`
- **Classification:** `criterion_component`
- **Description:** Relative second-order Taylor linearization error
- **Max Absolute Value:** `0.0003289246365900508287095260762751405467533010995001401432654816361226234528648121`
- **Argmax Parameter Point (id=3):** `val=0.0003289246365900508287095260762751405467533010995001401432654816361226234528648121` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
- **Top Worst Parameter Points:**
  - id=3 | `val=0.0003289246365900508287095260762751405467533010995001401432654816361226234528648121` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
  - id=7 | `val=0.000099996290563946719161634403150192678263756849895182241307369635682701045913442427` | `mode=pure_radial_variation, zero_index=10, delta=0.05`
  - id=11 | `val=0.000051015828693039416804040807188793830689950481839796727549467300994221826935584346` | `mode=pure_radial_variation, zero_index=50, delta=0.05`
  - id=15 | `val=0.000039061991369633635447754315008186086911060644532018516477431815275665689319579468` | `mode=pure_radial_variation, zero_index=100, delta=0.05`
  - id=2 | `val=0.000013191649352325735684473734185993719787464863227652492999109487848523558068965251` | `mode=pure_radial_variation, zero_index=1, delta=0.01`

### `exact_radial_defect_norm`
- **Classification:** `diagnostic`
- **Description:** Exact pure radial defect L2 norm
- **Max Absolute Value:** `0.001251031312900599654913452341810993086419966901466935871616133199731702902757793`
- **Argmax Parameter Point (id=3):** `val=0.001251031312900599654913452341810993086419966901466935871616133199731702902757793` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
- **Top Worst Parameter Points:**
  - id=3 | `val=0.001251031312900599654913452341810993086419966901466935871616133199731702902757793` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
  - id=7 | `val=0.00080008302483171920393732163382805437862087511854286264264289937437260025679232902` | `mode=pure_radial_variation, zero_index=10, delta=0.05`
  - id=11 | `val=0.00040821419034575630150898399190964903703558597255048439012598272719414366913407703` | `mode=pure_radial_variation, zero_index=50, delta=0.05`
  - id=15 | `val=0.00031251220738483742315508772657601508180374808507348933658303586390255110612315627` | `mode=pure_radial_variation, zero_index=100, delta=0.05`
  - id=2 | `val=0.000050034084474731343950965518376958120250253117007618444947367337253508046628064683` | `mode=pure_radial_variation, zero_index=1, delta=0.01`

### `linear_second_order_norm`
- **Classification:** `diagnostic`
- **Description:** Linearized second-order response L2 norm
- **Max Absolute Value:** `0.0012508446492353363222116923825195450584213293816138232918143358484952840288984693`
- **Argmax Parameter Point (id=3):** `val=0.0012508446492353363222116923825195450584213293816138232918143358484952840288984693` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
- **Top Worst Parameter Points:**
  - id=3 | `val=0.0012508446492353363222116923825195450584213293816138232918143358484952840288984693` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
  - id=7 | `val=0.00080000301983529912437443217360053537127173360695603859943317436412217795592950763` | `mode=pure_radial_variation, zero_index=10, delta=0.05`
  - id=11 | `val=0.00040819336687120240096154617355850418054042316478143343820445047865751918876500244` | `mode=pure_radial_variation, zero_index=50, delta=0.05`
  - id=15 | `val=0.00031250000003569180296097203384843357149506163452629993534170628372705033825717303` | `mode=pure_radial_variation, zero_index=100, delta=0.05`
  - id=2 | `val=0.000050033785969413452888467695300781802336853175264552931672573433939811361155938771` | `mode=pure_radial_variation, zero_index=1, delta=0.01`

### `quadratic_ratio`
- **Classification:** `diagnostic`
- **Description:** Quadratic halving ratio Delta C(delta) / Delta C(delta/2)
- **Max Absolute Value:** `4.0004477`
- **Argmax Parameter Point (id=3):** `val=4.0004477` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
- **Top Worst Parameter Points:**
  - id=3 | `val=4.0004477` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
  - id=7 | `val=4.0003` | `mode=pure_radial_variation, zero_index=10, delta=0.05`
  - id=11 | `val=4.000153` | `mode=pure_radial_variation, zero_index=50, delta=0.05`
  - id=15 | `val=4.0001172` | `mode=pure_radial_variation, zero_index=100, delta=0.05`
  - id=2 | `val=4.0000179` | `mode=pure_radial_variation, zero_index=1, delta=0.01`

### `quadratic_energy`
- **Classification:** `diagnostic`
- **Description:** Quadratic radial energy E(u)
- **Max Absolute Value:** `0.0000015646123365206715597630537083693936459213718080573626502511260113962955432162321`
- **Argmax Parameter Point (id=3):** `val=0.0000015646123365206715597630537083693936459213718080573626502511260113962955432162321` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
- **Top Worst Parameter Points:**
  - id=3 | `val=0.0000015646123365206715597630537083693936459213718080573626502511260113962955432162321` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
  - id=7 | `val=0.00000064000483174559800423292907776301390341943120559298971277553776534356400750087955` | `mode=pure_radial_variation, zero_index=10, delta=0.05`
  - id=11 | `val=0.00000016662182475764803779054396173969470791427587027171289935583269920838673432832907` | `mode=pure_radial_variation, zero_index=50, delta=0.05`
  - id=15 | `val=0.000000097656250022307376851881425953875834227191949505641585113144531521013171256369738` | `mode=pure_radial_variation, zero_index=100, delta=0.05`
  - id=2 | `val=0.0000000025033797384330744956208859333910298334741948928917802404018016182340728691459714` | `mode=pure_radial_variation, zero_index=1, delta=0.01`

### `nnls_residual_norm`
- **Classification:** `diagnostic`
- **Description:** Non-negative least squares compensation residual norm
- **Max Absolute Value:** `0.0012495192334332076146253221474642769182837673185998199034192237216629430542016144`
- **Argmax Parameter Point (id=3):** `val=0.0012495192334332076146253221474642769182837673185998199034192237216629430542016144` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
- **Top Worst Parameter Points:**
  - id=3 | `val=0.0012495192334332076146253221474642769182837673185998199034192237216629430542016144` | `mode=pure_radial_variation, zero_index=1, delta=0.05`
  - id=2 | `val=0.000049980769337328304585012885898571074827890224385403527419269382977925813888948345` | `mode=pure_radial_variation, zero_index=1, delta=0.01`
  - id=1 | `val=0.000012495192334332076146253221474642768723383069097002973313443681375884953976000473` | `mode=pure_radial_variation, zero_index=1, delta=0.005`
  - id=0 | `val=0.00000049980769342552880723195946309890947536898109413885161549897688026226033439816085` | `mode=pure_radial_variation, zero_index=1, delta=0.001`
  - id=15 | `val=0.0000000093693548126780269426049261909581870479250361240060506596600546293437130458285075` | `mode=pure_radial_variation, zero_index=100, delta=0.05`

---

## 4. Execution & Environment Metadata

- **Git Commit:** `acaa862a769f84f747bed75f4898b3174e1d985b` (Dirty: `False`)
- **Precision:** `80 dps`
- **Tau Value:** `6.2831853071795864769252... (2*pi)`
- **Points Requested:** `16`
- **Points Completed:** `16`
- **Started At:** `2026-08-23T20:23:34.565323+00:00`
- **Completed At:** `2026-08-23T20:25:11.736973+00:00`

---

## 5. Artifact Index

- Manifest: [`manifest.json`](manifest.json)
- Summary: [`summary.json`](summary.json)
- Detailed Points: [`results.jsonl`](results.jsonl)
