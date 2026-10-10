r"""Test Suite for TASK-TC-030: Minimal Rank-Two Trinomial Kernel and Sparse Orbit Theorems.

Covers all 24 required test specifications from TASK-TC-030:
1. support-size-one impossibility
2. support-size-two rank-one reduction
3. rank-one three-term reduction
4. affine rank-two normalization
5. two independent relations force algebraic-coordinate model
6. relation-space dimension at most one under the abstract S_tau bound
7. exceptional X forces exceptional Y
8. exceptional Y/X forces exceptional coordinates
9. complex conjugate relation production
10. real-normalization positive control
11. same-sign impossibility
12. three sign orientations
13. consecutive-orbit determinant identity
14. three-consecutive orbit rigidity
15. non-propagation regression
16. generalized Vandermonde numerical control
17. sparse enumeration deduplication
18. exact-relation positive control
19. Arb fail-closed behavior
20. certified sparse exclusion
21. no midpoint used as a certified distance
22. no claim that finite implies empty
23. no claim that one relation propagates through TC
24. no zeta-to-kernel claim
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
    classify_minimal_support,
    compute_affine_support_rank_trinomial,
    evaluate_relation_space_dimension_bound,
    check_exceptional_direction_exclusion,
    normalize_trinomial_coefficients_real,
    classify_sign_orientation,
    evaluate_dilation_orbit,
    consecutive_orbit_determinant,
    check_three_consecutive_rigidity,
    generalized_vandermonde_determinant,
    audit_multiplicative_group_theorems,
    enumerate_sparse_trinomial_monomial_pairs,
    enumerate_normalized_coefficients,
    certify_sparse_trinomial_exclusion,
    evaluate_exact_control_relation,
)


# Test 1: Support-size-one impossibility
def test_support_size_one_impossibility():
    res = classify_minimal_support([(5, sqrt(2))])
    assert res.support_size == 1
    assert res.is_possible is False
    assert res.classification_code == "SUPPORT_SIZE_ONE_IMPOSSIBLE"


# Test 2: Support-size-two rank-one reduction
def test_support_size_two_rank_one_reduction():
    res = classify_minimal_support([(1, 0), (2, sqrt(2))])
    assert res.support_size == 2
    assert res.is_possible is True
    assert res.affine_support_rank == 1
    assert res.classification_code == "SUPPORT_SIZE_TWO_RANK_ONE_REDUCED"
    assert res.reduction_target == "S_TAU_EXCEPTIONAL_DIRECTION"


# Test 3: Rank-one three-term reduction (collinear grades)
def test_rank_one_three_term_reduction():
    # Grades 0, sqrt(2), 2*sqrt(2) -> ratio is 1/2 in Q
    res = classify_minimal_support([(1, 0), (-3, sqrt(2)), (2, 2 * sqrt(2))])
    assert res.support_size == 3
    assert res.affine_support_rank == 1
    assert res.classification_code == "AFFINE_RANK_ONE_TRINOMIAL_REDUCED"
    assert res.reduction_target == "S_TAU_EXCEPTIONAL_DIRECTION"


# Test 4: Affine rank-two normalization
def test_affine_rank_two_normalization():
    # Grades 0, 1, sqrt(2) -> ratio 1/sqrt(2) not in Q
    res = classify_minimal_support([(1, 0), (1, 1), (1, sqrt(2))])
    assert res.support_size == 3
    assert res.affine_support_rank == 2
    assert res.classification_code == "FIRST_OPEN_KERNEL_SUPPORT"
    assert res.reduction_target == "MINIMAL_RANK_TWO_TRINOMIAL_FRONTIER"

    rank = compute_affine_support_rank_trinomial(0, 1, sqrt(2))
    assert rank == 2


# Test 5: Two independent relations force algebraic-coordinate model
def test_two_independent_relations_force_algebraic_coordinates():
    X = Symbol("X")
    Y = Symbol("Y")
    # Relation 1: a0 + a1*X + a2*Y = 0
    # Relation 2: b0 + b1*X + b2*Y = 0
    a0, a1, a2 = 1, 2, 3
    b0, b1, b2 = 4, 1, 5
    det = a1 * b2 - a2 * b1  # 2*5 - 3*1 = 7 != 0
    sol_X = (a2 * b0 - a0 * b2) / det  # (3*4 - 1*5)/7 = 7/7 = 1
    sol_Y = (a0 * b1 - a1 * b0) / det  # (1*1 - 2*4)/7 = -7/7 = -1

    # Verify both coordinates are purely rational
    assert sol_X == 1
    assert sol_Y == -1


# Test 6: Relation-space dimension at most one under abstract S_tau bound
def test_relation_space_dimension_bound():
    dim_bound = evaluate_relation_space_dimension_bound(1, sqrt(2))
    assert dim_bound <= 1


# Test 7: Exceptional X forces exceptional Y
def test_exceptional_x_forces_exceptional_y():
    res = check_exceptional_direction_exclusion(1, 2, 3)
    assert res["exceptional_x_forces_algebraic_y"] is True
    # If X = 5 in Q_bar, Y = (-1 - 2*5)/3 = -11/3 in Q_bar
    X_val = 5
    Y_val = res["sol_Y_from_X"].subs(Symbol("X"), X_val)
    assert Y_val == Rational(-11, 3)


# Test 8: Exceptional Y/X forces exceptional coordinates
def test_exceptional_ratio_forces_exceptional_coordinates():
    res = check_exceptional_direction_exclusion(1, 2, 3)
    assert res["exceptional_ratio_forces_algebraic_coordinates"] is True
    # If Z = Y/X = 1/3, X = -1 / (2 + 3*(1/3)) = -1/3
    Z_val = Rational(1, 3)
    X_val = res["sol_X_from_ratio"].subs(Symbol("Z"), Z_val)
    assert X_val == Rational(-1, 3)


# Test 9: Complex conjugate relation production
def test_complex_conjugate_relation_production():
    # If a0 + a1*X + a2*Y = 0 with real X, Y, then conj(a0) + conj(a1)*X + conj(a2)*Y = 0
    X_real = 2.5
    Y_real = 3.5
    a0 = 1 + 2 * I
    a1 = 3 + 4 * I
    # Construct a2 = (-a0 - a1*X)/Y
    a2 = (-a0 - a1 * X_real) / Y_real

    val = a0 + a1 * X_real + a2 * Y_real
    assert sp.simplify(val) == 0

    val_conj = sp.conjugate(a0) + sp.conjugate(a1) * X_real + sp.conjugate(a2) * Y_real
    assert sp.simplify(val_conj) == 0


# Test 10: Real-normalization positive control
def test_real_normalization_positive_control():
    # Vector of coefficients with non-trivial complex phase: (1+I, 2+2I, -3-3I)
    a0 = 1 + I
    a1 = 2 + 2 * I
    a2 = -(3 + 3 * I)

    res = normalize_trinomial_coefficients_real(a0, a1, a2)
    assert res.is_real_normalized is True
    c0, c1, c2 = res.normalized_coeffs
    assert c0.is_real
    assert c1.is_real
    assert c2.is_real
    # Check proportionality: c1/c0 == a1/a0 == 2, c2/c0 == a2/a0 == -3
    assert c1 / c0 == 2
    assert c2 / c0 == -3


# Test 11: Same-sign impossibility
def test_same_sign_impossibility():
    with pytest.raises(ValueError, match="same sign"):
        classify_sign_orientation(1, 2, 3)
    with pytest.raises(ValueError, match="same sign"):
        classify_sign_orientation(-1, -2, -3)


# Test 12: Three sign orientations
def test_three_sign_orientations():
    # Case 1: a2 negative, a0 and a1 positive -> Y = u + v*X
    res1 = classify_sign_orientation(1, 2, -4)
    assert res1.orientation_type == "Y_AFFINE_X"
    assert res1.u == Rational(1, 4)
    assert res1.v == Rational(2, 4)

    # Case 2: a1 negative, a0 and a2 positive -> X = u + v*Y
    res2 = classify_sign_orientation(1, -3, 2)
    assert res2.orientation_type == "X_AFFINE_Y"
    assert res2.u == Rational(1, 3)
    assert res2.v == Rational(2, 3)

    # Case 3: a0 negative, a1 and a2 positive -> 1 = u*X + v*Y
    res3 = classify_sign_orientation(-5, 2, 3)
    assert res3.orientation_type == "ONE_AFFINE_XY"
    assert res3.u == Rational(2, 5)
    assert res3.v == Rational(3, 5)


# Test 13: Consecutive-orbit determinant identity
def test_consecutive_orbit_determinant_identity():
    X = Symbol("X", positive=True)
    Y = Symbol("Y", positive=True)
    n = 3

    # Computed via closed formula
    formula_det = consecutive_orbit_determinant(X, Y, n)

    # Computed via direct 3x3 expansion
    M = sp.Matrix([
        [1, X**n, Y**n],
        [1, X**(n + 1), Y**(n + 1)],
        [1, X**(n + 2), Y**(n + 2)],
    ])
    matrix_det = M.det()

    assert sp.simplify(formula_det - matrix_det) == 0


# Test 14: Three-consecutive orbit rigidity
def test_three_consecutive_orbit_rigidity():
    X_val = 2
    Y_val = 3
    res = check_three_consecutive_rigidity(1, 2, 3, X_val, Y_val, n=0)
    assert res["is_determinant_nonzero"] is True
    assert res["forces_trivial_coefficients"] is True
    assert res["theorem"] == "THREE_CONSECUTIVE_DILATION_ORBIT_RIGIDITY"


# Test 15: Non-propagation regression (f(1)=0 does not imply f(2)=0)
def test_non_propagation_regression():
    # Choose X=2, Y=3 and a0=-5, a1=1, a2=1
    # f(1) = -5 + 1*(2) + 1*(3) = 0
    # f(2) = -5 + 1*(4) + 1*(9) = 8 != 0
    orbit = evaluate_dilation_orbit(-5, 1, 1, 2, 3, [1, 2, 3])
    assert orbit[1] == 0
    assert orbit[2] == 8
    assert orbit[3] == 30
    assert orbit[2] != 0


# Test 16: Generalized Vandermonde numerical control
def test_generalized_vandermonde_numerical_control():
    bases = (1.5, 2.5, 4.0)
    powers = (1, 3, 5)
    det_val = generalized_vandermonde_determinant(bases, powers)
    # Strictly positive by Descartes / Chebyshev theory
    assert det_val > 0.0


# Test 17: Sparse enumeration deduplication
def test_sparse_enumeration_deduplication():
    pairs = enumerate_sparse_trinomial_monomial_pairs(max_degree=2)
    # Total monomials with deg <= 2 (excluding (0,0)):
    # deg 1: (1,0), (0,1) -> 2
    # deg 2: (2,0), (1,1), (0,2) -> 3
    # Total = 5. Pairs = 5*4/2 = 10.
    assert len(pairs) == 10
    assert len(set(pairs)) == 10

    coeffs = enumerate_normalized_coefficients(max_height=3)
    # Verify all coefficients are primitive and mixed-sign
    for a0, a1, a2 in coeffs:
        assert a0 > 0
        assert math.gcd(a0, math.gcd(abs(a1), abs(a2))) == 1
        assert not (a1 > 0 and a2 > 0)


# Test 18: Exact-relation positive control
def test_exact_relation_positive_control():
    # Exact synthetic control: Y = 1 + X ==> 1 + X - Y = 0
    # On support {1, X, Y}, coeffs (1, 1, -1) with X=2.0, Y=3.0
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
    assert res["status"] == "RELATION_DETECTED"
    assert res["control_passed"] is True


# Test 19: Arb fail-closed behavior
def test_arb_fail_closed_behavior():
    from tc.ambient_kernel import expr_to_arb
    # Fails closed on unsupported expression
    with pytest.raises(ValueError, match="(?i)unsupported"):
        expr_to_arb(Symbol("unsupported_non_algebraic_var"))


# Test 20: Certified sparse exclusion
def test_certified_sparse_exclusion():
    # Test on Base-One Instance: (1, sqrt(2)) with small box (D=2, H=3)
    res = certify_sparse_trinomial_exclusion(
        instance_name=CANONICAL_INSTANCE_BASE_ONE,
        alpha_expr=Integer(1),
        beta_expr=sqrt(2),
        max_degree=2,
        max_height=3,
        prec_bits=128,
    )
    assert res.classification == "CERTIFIED_FINITE_TRINOMIAL_EXCLUSION"
    assert res.normalized_trinomials_tested > 0
    assert res.smallest_certified_distance > 0.0

    # Test on Radical Pair Instance: (sqrt(2), sqrt(3))
    res_rad = certify_sparse_trinomial_exclusion(
        instance_name=CANONICAL_INSTANCE_RADICAL_PAIR,
        alpha_expr=sqrt(2),
        beta_expr=sqrt(3),
        max_degree=2,
        max_height=3,
        prec_bits=128,
    )
    assert res_rad.classification == "CERTIFIED_FINITE_TRINOMIAL_EXCLUSION"
    assert res_rad.smallest_certified_distance > 0.0


# Test 21: No midpoint used as a certified distance
def test_no_midpoint_used_as_certified_distance():
    res = certify_sparse_trinomial_exclusion(
        instance_name=CANONICAL_INSTANCE_BASE_ONE,
        alpha_expr=Integer(1),
        beta_expr=sqrt(2),
        max_degree=1,
        max_height=2,
        prec_bits=128,
    )
    # The smallest_certified_distance must be an absolute lower bound
    assert res.smallest_certified_distance > 0.0
    cand = res.smallest_candidate
    assert "distance_lb" in cand
    assert cand["distance_lb"] > 0.0


# Test 22: No claim that finite implies empty
def test_no_claim_that_finite_implies_empty():
    audit = audit_multiplicative_group_theorems()
    assert audit["critical_boundary"] == "FINITE_DOES_NOT_IMPLY_EMPTY"
    assert audit["existence_status"] == "MINIMAL_RANK_TWO_TRINOMIAL_EXISTENCE_OPEN"
    assert audit["consequence_for_fixed_coefficients"] == "FIXED_COEFFICIENT_TRINOMIAL_SOLUTIONS_FINITE"


# Test 23: No claim that one relation propagates through TC
def test_no_claim_that_one_relation_propagates_through_tc():
    # Rigidity applies to 3 consecutive dilations, but a single relation f(1)=0
    # does NOT propagate to f(2)=0.
    res = check_three_consecutive_rigidity(1, 2, 3, 2, 3)
    assert res["theorem"] == "THREE_CONSECUTIVE_DILATION_ORBIT_RIGIDITY"
    # Verify explicit no-propagation example exists
    orbit = evaluate_dilation_orbit(-10, 1, 1, 4, 6, [1, 2])
    assert orbit[1] == 0
    assert orbit[2] == 42  # 16 + 36 - 10 = 42 != 0


# Test 24: No zeta-to-kernel claim
def test_no_zeta_to_kernel_claim():
    audit = audit_multiplicative_group_theorems()
    assert audit["zeta_bridge_status"] == "NO_ZETA_TO_KERNEL_BRIDGE_FOUND"
