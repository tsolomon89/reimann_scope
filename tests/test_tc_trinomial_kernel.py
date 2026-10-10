r"""Test Suite for TASK-TC-030R: Trinomial Kernel Evidence Alignment, Canonical Support Repair, and Certificate-Scope Correction.

Covers all 24 required test specifications from TASK-TC-030R:
1. repeated-grade terms are combined before support classification
2. coefficient cancellation removes a grade
3. complete cancellation yields empty support
4. unresolved rationality fails closed
5. exact rank-two radical support is recognized
6. relation-space helper records external assumptions rather than returning bare 1
7. Cramer full-paper proof handles a nonzero minor not in columns X, Y
8. exceptional helper uses the supplied Y_sym
9. degenerate coefficients fail closed
10. ratio denominator zero implies a0 = 0
11. real normalization rejects non-proportional conjugate coefficient vectors
12. real normalization returns exact transformed coefficients
13. no real-part truncation after failed normalization
14. no-propagation wording regression
15. group rank and product-group rank are distinguished
16. diagonal orbit is distinguished
17. support accounting gives 36 total, 30 rank two, 6 rank one
18. total three-monomial subsets are 120
19. certificate metadata identifies constant-anchored scope
20. candidate counts partition correctly
21. positive controls still enclose zero
22. no midpoint is used as certified distance
23. no full algebraic-independence claim
24. no RH claim
"""

import math
import pytest
import sympy as sp
from sympy import Rational, Integer, sqrt, Symbol, I

import flint
from flint import arb, ctx

from tc.trinomial_kernel import (
    CANONICAL_INSTANCE_BASE_ONE,
    CANONICAL_INSTANCE_RADICAL_PAIR,
    SUPPORT_BOX_TOTAL_MONOMIALS,
    SUPPORT_BOX_TOTAL_THREE_MONOMIAL_SUBSETS,
    SUPPORT_BOX_CONSTANT_ANCHORED_SUPPORTS,
    SUPPORT_BOX_AFFINE_RANK_TWO_SUPPORTS,
    SUPPORT_BOX_AFFINE_RANK_ONE_CONTROLS,
    NORMALIZED_COEFFICIENTS_PER_SUPPORT,
    canonicalize_group_algebra_terms,
    classify_minimal_support,
    compute_affine_support_rank_trinomial,
    derive_relation_space_dimension_bound,
    evaluate_relation_space_dimension_bound,
    solve_two_relations_algebraic_coordinates,
    check_exceptional_direction_exclusion,
    normalize_trinomial_coefficients_real,
    classify_sign_orientation,
    evaluate_dilation_orbit,
    consecutive_orbit_determinant,
    check_three_consecutive_rigidity,
    generalized_vandermonde_determinant,
    audit_multiplicative_group_theorems,
    enumerate_sparse_trinomial_monomial_pairs,
    partition_monomial_supports_by_rank,
    enumerate_normalized_coefficients,
    certify_sparse_trinomial_exclusion,
    evaluate_exact_control_relation,
)


# 1. repeated-grade terms are combined before support classification
def test_repeated_grades_combined_before_classification():
    # 1[0] - 1[0] + 1[1] must canonicalize to 1[1] and be classified as support size 1
    terms = [(1, 0), (-1, 0), (1, 1)]
    canon = canonicalize_group_algebra_terms(terms)
    assert len(canon) == 1
    assert canon[0] == (Integer(1), Integer(1))

    res = classify_minimal_support(terms)
    assert res.support_size == 1
    assert res.classification_code == "SUPPORT_SIZE_ONE_IMPOSSIBLE"


# 2. coefficient cancellation removes a grade
def test_coefficient_cancellation_removes_grade():
    # 1[0] + 1[1] - 1[1] must canonicalize to 1[0] and have support size 1
    terms = [(1, 0), (1, 1), (-1, 1)]
    canon = canonicalize_group_algebra_terms(terms)
    assert len(canon) == 1
    assert canon[0] == (Integer(1), Integer(0))

    res = classify_minimal_support(terms)
    assert res.support_size == 1
    assert res.classification_code == "SUPPORT_SIZE_ONE_IMPOSSIBLE"


# 3. complete cancellation yields empty support
def test_complete_cancellation_yields_empty_support():
    # 1[0] + 2[1] - 2[1] - 1[0] must canonicalize to empty support
    terms = [(1, 0), (2, 1), (-2, 1), (-1, 0)]
    canon = canonicalize_group_algebra_terms(terms)
    assert len(canon) == 0

    res = classify_minimal_support(terms)
    assert res.support_size == 0
    assert res.classification_code == "EMPTY_SUPPORT"
    assert res.is_possible is False


# 4. unresolved rationality fails closed
def test_unresolved_rationality_fails_closed():
    # An unresolved symbol expression must raise ValueError with EXACT_AFFINE_RANK_UNRESOLVED
    x = Symbol("x")
    with pytest.raises(ValueError, match="EXACT_AFFINE_RANK_UNRESOLVED"):
        compute_affine_support_rank_trinomial(0, x, x**2 + 1)


# 5. exact rank-two radical support is recognized
def test_exact_rank_two_radical_support_recognized():
    # 1, (2pi)^sqrt(2), (2pi)^sqrt(3) has affine rank 2
    rank = compute_affine_support_rank_trinomial(0, sqrt(2), sqrt(3))
    assert rank == 2

    res = classify_minimal_support([(1, 0), (1, sqrt(2)), (1, sqrt(3))])
    assert res.support_size == 3
    assert res.affine_support_rank == 2
    assert res.classification_code == "FIRST_OPEN_KERNEL_SUPPORT"
    assert res.reduction_target == "MINIMAL_RANK_TWO_TRINOMIAL_FRONTIER"


# 6. relation-space helper records external assumptions rather than returning bare 1
def test_relation_space_helper_records_assumptions():
    bound_res = derive_relation_space_dimension_bound(1, sqrt(2))
    assert bound_res.dimension_bound == 1
    assert bound_res.is_rationally_independent is True
    assert bound_res.assumes_external_gelfond_schneider is True
    assert bound_res.theorem_conclusion == "AT_MOST_ONE_DIMENSIONAL"
    assert bound_res.evidence_class == "PROVED_PAPER_DERIVATION_PLUS_EXTERNAL_GELFOND_SCHNEIDER"
    assert bound_res.status == "RESOLVED"

    # Backward compatibility helper also works
    assert evaluate_relation_space_dimension_bound(1, sqrt(2)) == 1


# 7. Cramer full-paper proof handles a nonzero minor not in columns X, Y
def test_cramer_full_paper_proof_all_minors():
    # Case A: Standard minor in columns X, Y (Delta_0 != 0)
    r1 = (1, 2, 3)
    r2 = (4, 1, 5)
    sol_std = solve_two_relations_algebraic_coordinates(r1, r2)
    assert sol_std["is_rank_2"] is True
    assert sol_std["delta_0"] == 7
    assert sol_std["sol_X"] == 1
    assert sol_std["sol_Y"] == -1

    # Case B: Delta_0 == 0, but Delta_1 or Delta_2 != 0
    # e.g. rows where X, Y columns are proportional:
    # r1 = (1, 2, 4)
    # r2 = (2, 1, 2) -> wait, here 2*2 - 4*1 = 0!
    r1_deg = (1, 2, 4)
    r2_deg = (2, 1, 2)
    sol_deg = solve_two_relations_algebraic_coordinates(r1_deg, r2_deg)
    assert sol_deg["is_rank_2"] is True
    assert sol_deg["delta_0"] == 0
    # Any nullspace vector has first coordinate 0, so (1, X, Y) cannot satisfy both
    assert sol_deg["solution_exists_with_first_coord_one"] is False


# 8. exceptional helper uses the supplied Y_sym
def test_exceptional_helper_uses_supplied_y_sym():
    X_var = Symbol("CustomX")
    Y_var = Symbol("CustomY")
    res = check_exceptional_direction_exclusion(1, 2, 3, X_sym=X_var, Y_sym=Y_var)
    # Must contain CustomX and CustomY in the respective solved expressions
    assert X_var in res["sol_Y_from_X"].free_symbols
    assert Y_var in res["sol_X_from_Y"].free_symbols


# 9. degenerate coefficients fail closed
def test_degenerate_coefficients_fail_closed():
    with pytest.raises(ValueError, match="DEGENERATE_COEFFICIENT_VECTOR"):
        check_exceptional_direction_exclusion(0, 1, 2)
    with pytest.raises(ValueError, match="DEGENERATE_COEFFICIENT_VECTOR"):
        check_exceptional_direction_exclusion(1, 0, 2)
    with pytest.raises(ValueError, match="DEGENERATE_COEFFICIENT_VECTOR"):
        check_exceptional_direction_exclusion(1, 2, 0)


# 10. ratio denominator zero implies a0 = 0
def test_ratio_denominator_zero_implies_a0_zero():
    # For a0 + a1*X + a2*Y = 0, let Z = Y/X.
    # If a1 + a2*Z = 0, then a0 = -X*(a1 + a2*Z) = 0.
    res = check_exceptional_direction_exclusion(1, 2, 3)
    assert res["ratio_denominator_zero_forces_a0_zero"] is True
    Z = Symbol("Z")
    denom = res["ratio_denominator"]
    assert denom == 2 + 3 * Z
    # If denom == 0, then 1 + X*(0) = 0 => 1 = 0, contradiction!
    contradiction = 1 + Symbol("X") * 0
    assert contradiction == 1


# 11. real normalization rejects non-proportional conjugate coefficient vectors
def test_real_normalization_rejects_non_proportional():
    # If coefficients have differing conjugate phases, e.g. a0 = 1+I, a1 = 1+2I, a2 = 1
    # conj(a0)/a0 = -I, conj(a1)/a1 = (1-2I)/(1+2I) != -I
    with pytest.raises(ValueError, match="COEFFICIENT_VECTOR_NOT_CONJUGATE_PROPORTIONAL"):
        normalize_trinomial_coefficients_real(1 + I, 1 + 2 * I, 1)


# 12. real normalization returns exact transformed coefficients
def test_real_normalization_returns_exact_transformed_coeffs():
    # For (1+I, 2+2I, -3-3I), lambda = -I, mu = 1 - I.
    # (1-I)*(1+I) = 2, (1-I)*(2+2I) = 4, (1-I)*(-3-3I) = -6.
    res = normalize_trinomial_coefficients_real(1 + I, 2 + 2 * I, -3 - 3 * I)
    assert res.is_real_normalized is True
    assert res.normalized_coeffs == (Integer(2), Integer(4), Integer(-6))


# 13. no real-part truncation after failed normalization
def test_no_real_part_truncation_after_failed_normalization():
    # Previously, non-real values were silently converted via sp.re().
    # Now it must fail closed if transformed coefficients are not genuinely real.
    with pytest.raises(ValueError, match="COEFFICIENT_VECTOR_NOT_CONJUGATE_PROPORTIONAL"):
        normalize_trinomial_coefficients_real(1 + 2 * I, 3 + 4 * I, 5 + 6 * I)


# 14. no-propagation wording regression
def test_no_propagation_wording_regression():
    audit = audit_multiplicative_group_theorems()
    assert audit["orbit_propagation_statement"] == "NO_CANONICAL_ORBIT_VANISHING_PROPAGATION"
    assert "f(1) = 0 does not force f(2) = 0" in audit["orbit_propagation_description"]


# 15. group rank and product-group rank are distinguished
def test_group_rank_and_product_group_rank_distinguished():
    audit = audit_multiplicative_group_theorems()
    assert audit["base_group_rank"] == 2
    assert audit["solution_group_rank"] == 4
    assert audit["base_group_rank"] != audit["solution_group_rank"]


# 16. diagonal orbit is distinguished
def test_diagonal_orbit_distinguished():
    audit = audit_multiplicative_group_theorems()
    assert audit["diagonal_orbit_rank"] == 1
    assert "Delta_{alpha, beta}" in audit["diagonal_dilation_orbit"]


# 17. support accounting gives 36 total, 30 rank two, 6 rank one
def test_support_accounting_36_30_6():
    pairs = enumerate_sparse_trinomial_monomial_pairs(max_degree=3)
    assert len(pairs) == SUPPORT_BOX_CONSTANT_ANCHORED_SUPPORTS
    assert len(pairs) == 36

    r1, r2 = partition_monomial_supports_by_rank(pairs)
    assert len(r1) == SUPPORT_BOX_AFFINE_RANK_ONE_CONTROLS
    assert len(r1) == 6
    assert len(r2) == SUPPORT_BOX_AFFINE_RANK_TWO_SUPPORTS
    assert len(r2) == 30


# 18. total three-monomial subsets are 120
def test_total_three_monomial_subsets_120():
    assert SUPPORT_BOX_TOTAL_MONOMIALS == 10
    assert SUPPORT_BOX_TOTAL_THREE_MONOMIAL_SUBSETS == 120
    assert math.comb(SUPPORT_BOX_TOTAL_MONOMIALS, 3) == 120


# 19. certificate metadata identifies constant-anchored scope
def test_certificate_metadata_identifies_constant_anchored_scope():
    res = certify_sparse_trinomial_exclusion(
        instance_name=CANONICAL_INSTANCE_BASE_ONE,
        alpha_expr=Integer(1),
        beta_expr=sqrt(2),
        max_degree=1,
        max_height=2,
        prec_bits=128,
    )
    assert res.certificate_scope == "constant-anchored sparse trinomial campaign"


# 20. candidate counts partition correctly
def test_candidate_counts_partition_correctly():
    pairs = enumerate_sparse_trinomial_monomial_pairs(max_degree=3)
    coeffs = enumerate_normalized_coefficients(max_height=10)
    assert len(coeffs) == NORMALIZED_COEFFICIENTS_PER_SUPPORT
    assert len(coeffs) == 2523

    r1, r2 = partition_monomial_supports_by_rank(pairs)
    total_cand = len(pairs) * len(coeffs)
    r2_cand = len(r2) * len(coeffs)
    r1_cand = len(r1) * len(coeffs)

    assert total_cand == 90828
    assert r2_cand == 75690
    assert r1_cand == 15138
    assert r2_cand + r1_cand == total_cand


# 21. positive controls still enclose zero
def test_positive_controls_still_enclose_zero():
    # Exact synthetic control: Y = 1 + X ==> 1 + X - Y = 0
    res = evaluate_exact_control_relation(
        X_val=2.0,
        Y_val=3.0,
        m1_pows=(1, 0),
        m2_pows=(0, 1),
        a0=1,
        a1=1,
        a2=-1,
    )
    assert res["contains_zero"] is True
    assert res["control_passed"] is True


# 22. no midpoint is used as certified distance
def test_no_midpoint_is_used_as_certified_distance():
    res = certify_sparse_trinomial_exclusion(
        instance_name=CANONICAL_INSTANCE_BASE_ONE,
        alpha_expr=Integer(1),
        beta_expr=sqrt(2),
        max_degree=1,
        max_height=2,
        prec_bits=128,
    )
    assert res.smallest_certified_distance > 0.0
    cand = res.smallest_candidate
    assert "distance_lb" in cand
    assert cand["distance_lb"] > 0.0


# 23. no full algebraic-independence claim
def test_no_full_algebraic_independence_claim():
    audit = audit_multiplicative_group_theorems()
    assert audit["critical_boundary"] == "FINITE_DOES_NOT_IMPLY_EMPTY"
    assert audit["existence_status"] == "MINIMAL_RANK_TWO_TRINOMIAL_EXISTENCE_OPEN"


# 24. no RH claim
def test_no_rh_claim():
    audit = audit_multiplicative_group_theorems()
    assert audit["zeta_bridge_status"] == "NO_ZETA_TO_KERNEL_BRIDGE_FOUND"
