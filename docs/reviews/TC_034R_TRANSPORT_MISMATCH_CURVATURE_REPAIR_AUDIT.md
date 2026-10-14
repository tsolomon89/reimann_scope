# Transport-Mismatch Curvature Evidence Repair Audit (`TASK-TC-034R`)

**Task ID:** `TASK-TC-034R`  
**Repaired Task:** `TASK-TC-034`  
**Starting Commit:** `9f4701280a05c5c4ba9dc8be8d2bdb968588c799`  
**Substantive Parent:** `684c324960c8cfb3014808004926bb4d157c2fd9`  
**Principal Classification (Preserved):** `MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A`  
**Task Completion Classification:** `TASK_TC_034R_TRANSPORT_CURVATURE_REPAIR_COMPLETE`  
**Canonical Open Obligation:** `OBL-CT-001A` (`OPEN`)

---

## 1. Mission & Scope

`TASK-TC-034` established the principal conclusion `MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A`: infinitesimal transport-mismatch curvature around the unique label-preserving transport $b = 1$ ($b = 1 + \eta$, $\eta \to 0$) reproduces the existing Curvature Transport detector $B_\rho(2\eta K)$ on the centered conjugate block without providing a kernel-independent flat arithmetic functional or a positive diagonal spectral descent.

`TASK-TC-034R` repairs five evidence-attribution and implementation defects identified in the review of `TASK-TC-034` while preserving all valid mathematical derivations and keeping `OBL-CT-001A` **OPEN**.

---

## 2. Defect & Evidence Repair Ledger

| Defect | Previous claim | Correct status | Repair | Regression test |
|---|---|---|---|---|
| **1. Nonexistent Lean compact-support theorem** | `formal/RiemannScope/README.md` listed a nonexistent compact-support ray-homogeneity theorem identifier (`compact_support_ray_` + `homogeneity_implies_zero`) under `TransportMismatchCurvature.lean`, while the Lean module header explicitly stated that the compact-support PDE theorem is not claimed in Lean. | `COMPACT_SUPPORT_HOMOGENEITY_NO_GO = PROVED_PAPER_DERIVATION` (`COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED`). Lean formalizes only the algebraic consequence $A_1 = d A_0, A_2 = d^2 A_0 \implies A_0 A_2 - A_1^2 = 0$ (`homogeneous_arithmetic_curvature_zero`). | Removed the nonexistent reference from `formal/RiemannScope/README.md`, added explicit 7-step paper ODE proof and `lean_formalized = False` in `audit_compact_support_homogeneity_no_go()`, and recorded the exact 18-declaration Lean map in `get_lean_theorem_map()`. | `test_01_no_false_lean_reference_in_repo`, `test_02_compact_support_no_go_classified_as_paper_derivation`, `test_27_actual_lean_theorem_identifiers_match_file` |
| **2. Noncompact witnesses described as compactly supported** | Positive and negative curvature prototypes $G_-(x,y) = \exp(-\frac{3}{2}(\log(xy/16))^2)$ and $G_+(x,y) = \cosh(\frac{6}{5}\log(xy/25))\exp(-\frac{2}{25}(\log(xy/25))^2)$ are smooth and nonnegative on $(0,\infty)^2$, but were evaluated directly with a finite station cutoff $n_{\max}=15$ rather than multiplied by an explicit compact-support cutoff. | Smooth prototypes $G_\pm$ are noncompact; compactly supported witnesses require multiplication by an explicit $C^\infty$ plateau cutoff $\mathrm{X}_{15}(x,y) = \chi_{15}(x)\chi_{15}(y) \in C_c^\infty((0,\infty)^2)$ supported in $(\frac{3}{2}, \frac{31}{2})^2 = (1.5, 15.5)^2$ with flat plateau $[\frac{7}{4}, \frac{61}{4}]^2 = [1.75, 15.25]^2$. | Implemented `flat_transition_h_jet`, `smooth_step_S_jet`, `plateau_cutoff_1d_jet`, `plateau_cutoff_2d_euler_jet`, `compactify_preserving_station_jets`, `build_compact_negative_witness`, and `build_compact_positive_witness` in `tc/transport_mismatch_curvature.py`. Verified that $\mathrm{X}_{15}(n,m)=1$ and $\mathcal E\mathrm{X}_{15}(n,m)=\mathcal E^2\mathrm{X}_{15}(n,m)=0$ for all active stations $2 \le n,m \le 15$. | `test_03_plateau_cutoff_zero_outside_support`, `test_04_plateau_cutoff_one_on_active_station_interval`, `test_05_first_cutoff_derivatives_vanish_at_active_stations`, `test_06_second_cutoff_derivatives_vanish_at_active_stations`, `test_07_compactification_preserves_F_at_active_stations`, `test_08_compactification_preserves_EF_at_active_stations`, `test_09_compactification_preserves_E2F_at_active_stations`, `test_11_negative_witness_nonnegative_and_compactly_supported`, `test_13_positive_witness_nonnegative_and_compactly_supported` |
| **3. Finite cutoff described as complete arithmetic evaluation & uncertified float display** | Finite sums up to $n_{\max}=15$ on noncompact prototypes were described as compact-support sign witnesses, and `G_+` used finite-difference Euler derivatives in `float` rather than exact analytic jets inside outward Arb ball arithmetic. | For $\widetilde G_\pm = \mathrm{X}_{15} G_\pm \in C_c^\infty((1.5, 15.5)^2)$, every integer station $n \ge 16$ lies outside the support, so the sum over active prime powers $2 \le n,m \le 15$ (`{2, 3, 4, 5, 7, 8, 9, 11, 13}`) is the **complete infinite arithmetic sum** for $\widetilde G_\pm$, certified by outward 128-bit Arb ball arithmetic (`COMPACT_SUPPORT_NEGATIVE_ARITHMETIC_CURVATURE_CERTIFIED` and `COMPACT_SUPPORT_POSITIVE_ARITHMETIC_CURVATURE_CERTIFIED`), superseding `FINITE_TRUNCATION_SIGN_INDEFINITENESS_OBSERVED` with `COMPACT_SUPPORT_ARITHMETIC_CURVATURE_SIGN_INDEFINITE`. | Supplied exact analytic formulas for $G_\pm, \mathcal E G_\pm, \mathcal E^2 G_\pm$, implemented fail-closed Arb certification in `certify_compact_witness_curvature_arb()` returning `ARB_CERTIFICATION_NOT_AVAILABLE` when `flint` is absent, labelled floats as `display_midpoint_approx` (`display_float_is_certificate = False`), and separated `COMPLETE_COMPACT_SUPPORT_SUM` from `FINITE_TRUNCATION_DIAGNOSTIC`. | `test_10_no_arithmetic_stations_outside_selected_complete_support`, `test_12_negative_witness_complete_curvature_enclosure_strictly_negative`, `test_14_positive_witness_complete_curvature_enclosure_strictly_positive`, `test_15_arb_failure_is_fail_closed`, `test_16_display_floats_are_not_labelled_certificates`, `test_17_complete_compact_support_sum_distinguished_from_finite_truncation`, `test_18_accidental_zero_scope_is_explicit` |
| **4. Theta–Mellin conditional claims encoded as Booleans** | `ThetaMellinNonScalarCandidateAudit` encoded convergence, second variation, and $\delta_\rho^2$ presence as unconditional `bool` fields (`True`), risking over-interpretation of unproved analytic steps. | Uncertain/conditional theta–Mellin properties must be represented as explicit evidence status strings (`PROVED_BY_DEFINITION`, `FALSE`, `CONDITIONAL_ON_REGULARIZATION`, `FORMAL_CANDIDATE_NOT_DERIVED`, `DIAGONAL_CONJUGATE_BLOCK_ONLY`, `COMPLETE_EXPANSION_NOT_DERIVED`, `RH_EQUIVALENT_IF_POSITIVE`, `CANDIDATE_THETA_MELLIN_AUDIT`). | Replaced all Boolean fields in `ThetaMellinNonScalarCandidateAudit` and `data/tc_transport_mismatch_curvature.json` with explicit status strings (`theta_definition_status`, `theta_convergence_status`, `theta_second_variation_status`, `theta_delta_squared_status`, `theta_complete_expansion_status`, `theta_positivity_status`, `theta_obl_ct_001a_status`). | `test_19_theta_uncertain_fields_are_statuses_not_booleans`, `test_20_theta_convergence_not_marked_proved`, `test_21_theta_complete_spectral_expansion_not_marked_proved`, `test_22_theta_delta_squared_limited_to_conjugate_block`, `test_23_theta_positivity_classified_as_rh_equivalent` |
| **5. Declaration count vs. compiled `theorem` count distinction** | Narrative text in `RESEARCH_HYPOTHESIS.md`, `RESEARCH_LEDGER.md`, `.agents/research/state.json`, and `.agents/research/queue.json` stated "566 total declarations compiled" without distinguishing `formal/build_report.json`'s `project_theorem_declarations_compiled = 565` (which counts `theorem` declarations across `formal/`) from the 18 declarations in `TransportMismatchCurvature.lean` (`1 def` `curvatureDet` + `17 theorem` declarations: $548 + 17 = 565$ `theorem`s). | `formal/RiemannScope/TransportMismatchCurvature.lean` contains 18 declarations (`1 def` + `17 theorem`s), bringing the repository's compiled `theorem` count in `formal/build_report.json` from 548 to **565** (with 0 `sorry`, 0 `admit`, no nonstandard project axioms introduced). | Updated `get_lean_theorem_map()`, `docs/reviews/TC_TRANSPORT_MISMATCH_CURVATURE.md`, and canonical docs/state files to state `565` compiled `theorem` declarations (`1 def` + `17 theorem`s in `TransportMismatchCurvature.lean`). | `test_27_actual_lean_theorem_identifiers_match_file` |

---

## 3. Certified Compact-Support Curvature Enclosures (128-bit Arb)

Both compactified witnesses use the $C^\infty$ plateau cutoff $\mathrm{X}_{15}(x,y) = \chi_{1.5, 1.75, 15.25, 15.5}(x)\chi_{1.5, 1.75, 15.25, 15.5}(y)$ supported in $(1.5, 15.5)^2$ and equal to $1$ with vanishing derivatives on $[1.75, 15.25]^2$. All 9 prime-power stations $n \in \{2, 3, 4, 5, 7, 8, 9, 11, 13\}$ ($81$ pairs) lie strictly inside $[1.75, 15.25]^2$, and all prime powers $n \ge 16$ lie strictly outside $(1.5, 15.5)^2$.

1. **Negative-Curvature Compact-Support Witness $\widetilde G_- = \mathrm{X}_{15} G_-$ (`COMPACT_SUPPORT_NEGATIVE_ARITHMETIC_CURVATURE_CERTIFIED`):**
   - Prototype: $G_-(x,y) = \exp\!\left(-\frac{3}{2}\bigl(\log\frac{xy}{16}\bigr)^2\right)$.
   - Exact Euler jets at active stations ($w = \log(xy/16)$):
     $$(\mathcal E G_-)(x,y) = -6w\,G_-(x,y), \qquad (\mathcal E^2 G_-)(x,y) = (36w^2 - 12)\,G_-(x,y).$$
   - 128-bit Arb enclosures:
     - $A_0(\widetilde G_-) \in [44.2893822257315359500578451369087093 \pm 2.39 \times 10^{-35}]$,
     - $A_1(\widetilde G_-) \in [6.76898617535648836988996873129612767 \pm 4.30 \times 10^{-35}]$,
     - $A_2(\widetilde G_-) \in [-144.426466248440423794815548224739239 \pm 1.15 \times 10^{-33}]$,
     - $\mathfrak C_{\mathrm{arith}}(\widetilde G_-) = A_0^- A_2^- - (A_1^-)^2 \in [-6442.34295182745976846022999751473105 \pm 8.42 \times 10^{-33}]$,
     - Certified sign: $\sup \mathfrak C_{\mathrm{arith}}(\widetilde G_-) < 0$ (`zero_excluded = True`).

2. **Positive-Curvature Compact-Support Witness $\widetilde G_+ = \mathrm{X}_{15} G_+$ (`COMPACT_SUPPORT_POSITIVE_ARITHMETIC_CURVATURE_CERTIFIED`):**
   - Prototype: $G_+(x,y) = \cosh\!\left(\frac{6}{5}w\right)\exp\!\left(-\frac{2}{25}w^2\right)$, $w = \log(xy/25)$.
   - Exact Euler jets at active stations ($a = 6/5, b = 2/25$):
     $$(\mathcal E G_+)(x,y) = 2\bigl(a\sinh(aw) - 2bw\cosh(aw)\bigr)e^{-bw^2},$$
     $$(\mathcal E^2 G_+)(x,y) = 4\Bigl[\bigl(a^2 - 2b + 4b^2 w^2\bigr)\cosh(aw) - 4abw\sinh(aw)\Bigr]e^{-bw^2}.$$
   - 128-bit Arb enclosures:
     - $A_0(\widetilde G_+) \in [292.864941291551953924667432356454488 \pm 2.38 \times 10^{-34}]$,
     - $A_1(\widetilde G_+) \in [-437.934469952524322584780511622059177 \pm 4.29 \times 10^{-34}]$,
     - $A_2(\widetilde G_+) \in [1310.06954632185106557198130198207429 \pm 1.25 \times 10^{-33}]$,
     - $\mathfrak C_{\mathrm{arith}}(\widetilde G_+) = A_0^+ A_2^+ - (A_1^+)^2 \in [+191887.248334839729574771407499577571 \pm 6.37 \times 10^{-31}]$,
     - Certified sign: $\inf \mathfrak C_{\mathrm{arith}}(\widetilde G_+) > 0$ (`zero_excluded = True`).

---

## 4. Final Classifications

- **Task Completion Classification:** `TASK_TC_034R_TRANSPORT_CURVATURE_REPAIR_COMPLETE`
- **Principal Mathematical Classification:** `MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A`
- **Secondary Classifications:**
  - `COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED`
  - `COMPACT_SUPPORT_ARITHMETIC_CURVATURE_SIGN_INDEFINITE`
  - `COMPACT_SUPPORT_NEGATIVE_ARITHMETIC_CURVATURE_CERTIFIED`
  - `COMPACT_SUPPORT_POSITIVE_ARITHMETIC_CURVATURE_CERTIFIED`
  - `FINITE_ACCIDENTAL_ARITHMETIC_CURVATURE_ZERO`
  - `THETA_MELLIN_AUDIT_CONDITIONAL`
  - `SPECTRAL_CURVATURE_IS_SIGNED_OR_DOUBLE_SUM`
  - `CURVATURE_POSITIVITY_IS_RH_EQUIVALENT`
  - `GENERIC_SCALE_CURVATURE`
  - `OBL_CT_001A_OPEN`
  - `CANDIDATE_FAILURE_DOES_NOT_REFUTE_TC`
