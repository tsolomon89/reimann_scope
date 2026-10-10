# TASK-TC-030R Review: Trinomial Kernel Evidence Alignment, Canonical Support Repair, and Certificate-Scope Correction

**Authoritative Status**: Corrective Audit & Evidence Alignment Artifact  
**Task ID**: TASK-TC-030R  
**Baseline Git HEAD**: `f74fb15987bdedb6c5d845929df5634bb0c7fc6a`  
**Substantive Parent**: `74469d360fbfdf3fe80370199ed36a83b62816f9`  
**Primary Classification**: `TRINOMIAL_FRONTIER_STRUCTURALLY_CLASSIFIED_EXISTENCE_OPEN`  
**Task Classification**: `TASK_TC_030R_TRINOMIAL_REPAIR_COMPLETE`  
**Machine-Readable Data**: `data/tc_minimal_rank_two_trinomial_kernel.json`  

---

## Executive Summary

TASK-TC-030R completes the corrective audit of the minimal rank-two trinomial kernel programme ($a_0 + a_1 \tau^\alpha + a_2 \tau^\beta = 0$, $\tau = 2\pi$, $\alpha/\beta \notin \mathbb{Q}$). The mathematical baseline established in TASK-TC-030 remains valid:
- Minimal support size $m=1$ is impossible;
- $m=2$ reduces to $S_\tau$;
- $m=3, r=1$ reduces to a one-variable Laurent polynomial equation ($S_\tau$);
- $m=3, r=2$ is isolated as the first genuinely open kernel support (`FIRST_OPEN_KERNEL_SUPPORT`).

This corrective pass repaired ten specific evidence, algebraic canonicalization, and certificate accounting defects without reopening generic polynomial searches or claiming unproved transcendence theorems.

---

## Defect Repairs & Evidence Classifications

### Defect 1: Uncanonicalized Support Classification
- **Defect**: Raw lists of terms were classified without grouping identical grades, allowing uncombined or cancelling terms (e.g. $1[0] - 1[0] + 1[1]$) to report spurious support size 3.
- **Affected File**: `tc/trinomial_kernel.py`
- **Repair**: Implemented `canonicalize_group_algebra_terms` to symbolically group identical grades, sum coefficients, remove zero sums, and sort deterministically before support classification.
- **Evidence Classification**: `ALGEBRAIC_CANONICALIZATION_VERIFIED`
- **Regression Tests**: `test_repeated_grades_combined_before_classification`, `test_coefficient_cancellation_removes_grade`, `test_complete_cancellation_yields_empty_support`.

### Defect 2: Unresolved Affine Rational Rank Silent Default
- **Defect**: `compute_affine_support_rank_trinomial` used `ratio.is_rational`, which could silently default to rank 2 when SymPy returned `None`.
- **Affected File**: `tc/trinomial_kernel.py`
- **Repair**: Rewrote `compute_affine_support_rank_trinomial` to use exact number-field basis reduction via `compute_rational_support_rank`, failing closed with `ValueError("EXACT_AFFINE_RANK_UNRESOLVED: ...")` upon ambiguity.
- **Evidence Classification**: `FAIL_CLOSED_ALGEBRAIC_RANK`
- **Regression Tests**: `test_unresolved_rationality_fails_closed`, `test_exact_rank_two_radical_support_recognized`.

### Defect 3: Hardcoded Relation-Space Helper
- **Defect**: `evaluate_relation_space_dimension_bound` returned a bare integer `1` without validating hypotheses or exposing external dependencies.
- **Affected File**: `tc/trinomial_kernel.py`
- **Repair**: Added `derive_relation_space_dimension_bound` returning a typed `RelationSpaceDimensionBound` record exposing rational independence, external Gelfond-Schneider dependency, and proof structure.
- **Evidence Classification**: `PROVED_PAPER_DERIVATION_PLUS_EXTERNAL_GELFOND_SCHNEIDER`
- **Regression Test**: `test_relation_space_helper_records_assumptions`.

### Defect 4: Incomplete Two-Relation Minor Proof
- **Defect**: The paper proof and Lean reference for the two-relation theorem assumed $\Delta_0 = a_1 b_2 - a_2 b_1 \ne 0$ without proving that other $2 \times 2$ minors could not be the sole non-vanishing minors.
- **Affected Files**: `tc/trinomial_kernel.py`, `docs/reviews/TC_MINIMAL_RANK_TWO_TRINOMIAL_KERNEL.md`
- **Repair**: Implemented `solve_two_relations_algebraic_coordinates` with invariant nullspace proof: the $2 \times 3$ algebraic matrix $M$ has rank 2 and a 1D nullspace spanned by $(\Delta_0, -\Delta_1, \Delta_2)$. Since $(1, X, Y)$ lies in the nullspace with first coordinate 1, $\Delta_0 \ne 0$ is mathematically guaranteed; hence Cramer's rule is universally applicable.
- **Evidence Classification**: `PROVED_PAPER_DERIVATION_WITH_LEAN_CRAMER_CORE`
- **Regression Test**: `test_cramer_full_paper_proof_all_minors`.

### Defect 5: Exceptional Direction Diagnostic Deficiencies
- **Defect**: `check_exceptional_direction_exclusion` ignored the supplied `Y_sym` parameter and returned unconditional flags on degenerate inputs ($a_0 a_1 a_2 = 0$).
- **Affected File**: `tc/trinomial_kernel.py`
- **Repair**: Rewrote helper to use `Y_sym`, fail closed on degenerate inputs with `ValueError("DEGENERATE_COEFFICIENT_VECTOR: ...")`, expose solved expressions, and prove ratio denominator $a_1 + a_2(Y/X) = 0 \implies a_0 = 0$ (contradicting nondegeneracy).
- **Evidence Classification**: `LEAN_PROVED_SOLVING_IDENTITIES_FEEDING_PAPER_PLUS_GELFOND_SCHNEIDER`
- **Regression Tests**: `test_exceptional_helper_uses_supplied_y_sym`, `test_degenerate_coefficients_fail_closed`, `test_ratio_denominator_zero_implies_a0_zero`.

### Defect 6: Non-Fail-Closed Real Normalization
- **Defect**: `normalize_trinomial_coefficients_real` took `sp.re()` of transformed coefficients, concealing failed normalization on non-proportional conjugate vectors.
- **Affected File**: `tc/trinomial_kernel.py`
- **Repair**: Implemented direct elementary proof with pivot phase multiplier $\mu = 1 + \lambda$ (or $\mu = i$), verified $\overline{a_j} = \lambda a_j$ across all coordinates, verified imaginary parts vanish exactly, and failed closed with `ValueError("COEFFICIENT_VECTOR_NOT_CONJUGATE_PROPORTIONAL: ...")`.
- **Evidence Classification**: `PROVED_PAPER_DERIVATION`
- **Regression Tests**: `test_real_normalization_rejects_non_proportional`, `test_real_normalization_returns_exact_transformed_coeffs`, `test_no_real_part_truncation_after_failed_normalization`.

### Defect 7: Misleading "No Propagation" Wording
- **Defect**: Prior documentation stated "$f(1)=0$ imposes no algebraic condition on $f(2), f(3), \ldots$". A single relation does constrain the generators algebraically; it merely does not force higher-dilation vanishing equations.
- **Affected Files**: `tc/trinomial_kernel.py`, `docs/reviews/TC_MINIMAL_RANK_TWO_TRINOMIAL_KERNEL.md`, `data/tc_minimal_rank_two_trinomial_kernel.json`
- **Repair**: Corrected terminology to `NO_CANONICAL_ORBIT_VANISHING_PROPAGATION`: "$f(1)=0$ does not force $f(2)=0, f(3)=0$, or any further orbit vanishing."
- **Evidence Classification**: `PROVED_PAPER_DERIVATION`
- **Regression Test**: `test_no_propagation_wording_regression`.

### Defect 8: Multiplicative-Group Rank Conflation
- **Defect**: Previous audits conflated the rank of the base group $\Gamma_0 = \langle X, Y \rangle \subset \mathbb{R}_{>0}^\times$ (rank 2) with the ambient group for solutions $(u, v)$ (rank 4) and the diagonal dilation orbit (rank 1).
- **Affected Files**: `tc/trinomial_kernel.py`, `docs/reviews/TC_MINIMAL_RANK_TWO_TRINOMIAL_KERNEL.md`, `data/tc_minimal_rank_two_trinomial_kernel.json`
- **Repair**: Updated `audit_multiplicative_group_theorems` to distinguish $\Gamma_0 \cong \mathbb{Z}^2$ (rank 2), $\Gamma_0 \times \Gamma_0$ (rank 4), and $\Delta_{\alpha, \beta} = \{(X^n, Y^n)\}$ (rank 1). Finiteness of solutions under Laurent (1984) and Evertse-Schlickewei-Schmidt (2002) is preserved under the boundary `FINITE_DOES_NOT_IMPLY_EMPTY`.
- **Evidence Classification**: `PROVED_WITH_EXTERNAL_MULTIPLICATIVE_GROUP_THEOREM`
- **Regression Tests**: `test_group_rank_and_product_group_rank_distinguished`, `test_diagonal_orbit_distinguished`.

### Defect 9: Certificate Scope & Support Accounting Conflation
- **Defect**: The campaign tested 36 constant-anchored supports ($1, M_1, M_2$) up to degree 3 and reported them as "all 36 rank-two supports" out of degree $\le 3$, omitting that the degree $\le 3$ box contains 120 total 3-monomial subsets, and that 6 of the 36 tested supports are rank-one controls.
- **Affected Files**: `tc/trinomial_kernel.py`, `data/tc_minimal_rank_two_trinomial_kernel.json`, `docs/reviews/TC_MINIMAL_RANK_TWO_TRINOMIAL_KERNEL.md`
- **Repair**: Added `partition_monomial_supports_by_rank`, decomposed the candidate counts ($90,828 = 75,690 \text{ [rank 2]} + 15,138 \text{ [rank 1 controls]}$ across $36 = 30 + 6$ supports), and scoped the certificate strictly as `constant-anchored sparse trinomial campaign`.
- **Evidence Classification**: `CERTIFIED_FINITE_TRINOMIAL_EXCLUSION`
- **Regression Tests**: `test_support_accounting_36_30_6`, `test_total_three_monomial_subsets_120`, `test_certificate_metadata_identifies_constant_anchored_scope`, `test_candidate_counts_partition_correctly`.

### Defect 10: Lean Formalization Scope Alignment
- **Defect**: General theorems (relation-space dimension bound, exceptional-direction exclusion) were described as "formalized in Lean", whereas Lean formalized the exact algebraic solving lemmas, leaving field closure and external transcendence theorems to the paper level.
- **Affected Files**: `docs/reviews/TC_MINIMAL_RANK_TWO_TRINOMIAL_KERNEL.md`, `data/tc_minimal_rank_two_trinomial_kernel.json`
- **Repair**: Formulated an explicit Lean Evidence Mapping Table linking all 12 compiled Lean declarations to what Lean proves, additional paper steps, and external theorems.
- **Evidence Classification**: `EVIDENCE_HIERARCHY_ALIGNED`
- **Regression Tests**: `test_no_full_algebraic_independence_claim`, `test_no_rh_claim`.

---

## Lean 4 Evidence Mapping Table

| Mathematical Claim | Lean Theorem | What Lean Proves | Additional Paper Step | External Theorem |
| :--- | :--- | :--- | :--- | :--- |
| **Support Translation** | `RiemannScope.trinomial_support_translation` | Factoring $\tau^{K_0}$ from 3-term sum for $\tau > 0$ | None | None |
| **Same-Sign Positivity** | `RiemannScope.trinomial_same_sign_pos_impossible` | $a_0 + a_1 X + a_2 Y \ne 0$ for $a_j, X, Y > 0$ | None | None |
| **Same-Sign Negativity** | `RiemannScope.trinomial_same_sign_neg_impossible` | $a_0 + a_1 X + a_2 Y \ne 0$ for $a_j < 0, X, Y > 0$ | None | None |
| **Cramer Coordinate Determination** | `RiemannScope.trinomial_two_relations_cramer` | Expresses $X, Y$ as rational functions of coefficients when $\Delta_0 \ne 0$ | Invariant nullspace proof that $\Delta_0 \ne 0$ is guaranteed, and field closure of $\overline{\mathbb{Q}}$ | Gelfond-Schneider ($\dim_{\mathbb{Q}} S_\tau \le 1$) |
| **Exceptional $X$ Solves $Y$** | `RiemannScope.trinomial_exceptional_x_forces_exceptional_y` | $Y = (-a_0 - a_1 X)/a_2$ for $a_2 \ne 0$ | Field closure of $\overline{\mathbb{Q}}$ and $S_\tau$ membership | Gelfond-Schneider ($\dim_{\mathbb{Q}} S_\tau \le 1$) |
| **Exceptional $Y$ Solves $X$** | `RiemannScope.trinomial_exceptional_y_forces_exceptional_x` | $X = (-a_0 - a_2 Y)/a_1$ for $a_1 \ne 0$ | Field closure of $\overline{\mathbb{Q}}$ and $S_\tau$ membership | Gelfond-Schneider ($\dim_{\mathbb{Q}} S_\tau \le 1$) |
| **Exceptional Ratio Solves $X$** | `RiemannScope.trinomial_exceptional_ratio_forces_exceptional_coordinates` | $X = -a_0 / (a_1 + a_2(Y/X))$ when denom $\ne 0$ | Proof that denom $\ne 0$ because $a_1 + a_2(Y/X) = 0 \implies a_0 = 0$, and field closure | Gelfond-Schneider ($\dim_{\mathbb{Q}} S_\tau \le 1$) |
| **Consecutive Orbit Determinant** | `RiemannScope.trinomial_three_consecutive_orbit_determinant` | $\det(M_n) = X^n Y^n (X-1)(Y-1)(Y-X)$ | None | None |
| **Orbit Determinant Nonvanishing** | `RiemannScope.trinomial_three_consecutive_orbit_det_ne_zero` | $\det(M_n) \ne 0$ for distinct positive bases | None | None |
| **Three-Consecutive Orbit Rigidity** | `RiemannScope.trinomial_three_consecutive_orbit_rigidity` | $f(n)=f(n+1)=f(n+2)=0 \implies a_j = 0$ | Dilation does not canonically propagate $f(1)=0$ into higher zeros | None |
| **Distinct Powers of $\tau > 1$** | `RiemannScope.tau_powers_pairwise_distinct_of_ne` | $\tau^\alpha \ne \tau^\beta$ for $\tau > 1, \alpha \ne \beta$ | None | None |
| **Non-Unit Power for Exponent $\ne 0$** | `RiemannScope.tau_pow_ne_one_of_ne_zero` | $\tau^\alpha \ne 1$ for $\tau > 1, \alpha \ne 0$ | None | None |

---

## Conclusion & Classification

TASK-TC-030R establishes strict alignment across all mathematical claims, formal Lean proofs, Python modules, and machine-readable data:
- **Principal Classification**: `TRINOMIAL_FRONTIER_STRUCTURALLY_CLASSIFIED_EXISTENCE_OPEN`
- **Task Classification**: `TASK_TC_030R_TRINOMIAL_REPAIR_COMPLETE`
- **Audit Findings**: `NO_ZETA_TO_KERNEL_BRIDGE_FOUND`, `FINITE_DOES_NOT_IMPLY_EMPTY`, `NO_CANONICAL_ORBIT_VANISHING_PROPAGATION`.
