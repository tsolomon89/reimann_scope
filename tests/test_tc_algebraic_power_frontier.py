"""Unit and mathematical regression tests for tc/algebraic_power_frontier.py.

TASK-TC-029: Systematic investigation of the unconditional rank-two algebraic-power frontier.
"""

import pytest
import sympy as sp
from sympy import Rational, sqrt

from tc.algebraic_power_frontier import (
    classify_rank_two_pair,
    evaluate_quadratic_conjugate_product,
    analyze_monomial_relation,
    get_sharp_unconditional_boundary_matrix,
    certify_rank_two_polynomial_exclusion,
    PAIR_TYPE_BASE_ONE,
    PAIR_TYPE_INCOMMENSURABLE_RADICALS,
    PAIR_TYPE_QUADRATIC_CONJUGATES,
    PAIR_TYPE_GENERAL,
)


def test_01_classify_rank_two_base_one():
    """Test classification of base-one canonical minimal instances (1, sqrt(2)) and (sqrt(3), 1)."""
    res1 = classify_rank_two_pair(sp.Integer(1), sqrt(2))
    assert res1.pair_type == PAIR_TYPE_BASE_ONE
    assert res1.is_base_one is True
    assert res1.rational_support_rank == 2

    res2 = classify_rank_two_pair(sqrt(3), sp.Integer(1))
    assert res2.pair_type == PAIR_TYPE_BASE_ONE
    assert res2.is_base_one is True


def test_02_classify_rank_two_incommensurable_radicals():
    """Test classification of incommensurable radical instances (sqrt(2), sqrt(3))."""
    res = classify_rank_two_pair(sqrt(2), sqrt(3))
    assert res.pair_type == PAIR_TYPE_INCOMMENSURABLE_RADICALS
    assert res.is_base_one is False
    assert res.is_quadratic_conjugate is False
    assert res.rational_support_rank == 2


def test_03_classify_rank_two_quadratic_conjugates():
    """Test classification of quadratic conjugate pairs in Q(sqrt(d))."""
    alpha = 1 + sqrt(2)
    beta = 1 - sqrt(2)
    res = classify_rank_two_pair(alpha, beta)
    assert res.pair_type == PAIR_TYPE_QUADRATIC_CONJUGATES
    assert res.is_quadratic_conjugate is True
    assert res.trace_val == Rational(2, 1)
    assert res.norm_val == Rational(-1, 1)

    alpha2 = Rational(2, 3) + Rational(1, 2) * sqrt(5)
    beta2 = Rational(2, 3) - Rational(1, 2) * sqrt(5)
    res2 = classify_rank_two_pair(alpha2, beta2)
    assert res2.pair_type == PAIR_TYPE_QUADRATIC_CONJUGATES
    assert res2.trace_val == Rational(4, 3)


def test_04_classify_rank_two_fails_on_rank_one():
    """Test that linearly dependent pairs raise ValueError because rational rank is 1."""
    with pytest.raises(ValueError, match="Expected rational support rank 2, but got rank 1"):
        classify_rank_two_pair(sqrt(2), 2 * sqrt(2))


def test_05_evaluate_quadratic_conjugate_product():
    """Test the trace/norm product law for quadratic conjugate pairs."""
    alpha = 1 + sqrt(2)
    beta = 1 - sqrt(2)
    prod_res = evaluate_quadratic_conjugate_product(alpha, beta)
    assert prod_res.trace == Rational(2, 1)
    assert prod_res.p == 2
    assert prod_res.q == 1
    assert prod_res.relation_over_qbar_tau == "(X * X')^1 = (2*pi)^2"
    assert prod_res.product_transcendence_status == "PROVED_TRANSCENDENTAL_LINDEMANN"
    assert prod_res.product_algebraicity_status == "REFUTED_WITHIN_SCOPE"

    # Half-integer trace
    alpha2 = Rational(1, 4) + sqrt(3)
    beta2 = Rational(1, 4) - sqrt(3)
    prod_res2 = evaluate_quadratic_conjugate_product(alpha2, beta2)
    assert prod_res2.trace == Rational(1, 2)
    assert prod_res2.p == 1
    assert prod_res2.q == 2
    assert prod_res2.relation_over_qbar_tau == "(X * X')^2 = (2*pi)^1"


def test_06_evaluate_quadratic_conjugate_pure_imaginary_fails():
    """Test that pure radical pairs alpha = sqrt(2), beta = -sqrt(2) fail closed."""
    with pytest.raises(ValueError, match="Expected rational support rank 2, but got rank 1"):
        evaluate_quadratic_conjugate_product(sqrt(2), -sqrt(2))


def test_07_monomial_reduction_rational_lindemann():
    """Test monomial reduction when m*alpha + n*beta is a non-zero rational."""
    alpha = 1 + sqrt(2)
    beta = 1 - sqrt(2)
    res = analyze_monomial_relation(alpha, beta, m=1, n=1)
    assert res.is_rational is True
    assert res.status == "PROVED_TRANSCENDENTAL_LINDEMANN"
    assert res.algebraic_relation_possible is False
    assert res.combined_exponent == 2

    # Linear difference with rational result: alpha - beta = 2*sqrt(2) is irrational,
    # but for (1, sqrt(2)), m=2, n=0 is rational:
    res2 = analyze_monomial_relation(sp.Integer(1), sqrt(2), m=3, n=0)
    assert res2.is_rational is True
    assert res2.status == "PROVED_TRANSCENDENTAL_LINDEMANN"
    assert res2.combined_exponent == 3


def test_08_monomial_reduction_irrational_s_tau():
    """Test monomial reduction when m*alpha + n*beta is irrational."""
    res = analyze_monomial_relation(sqrt(2), sqrt(3), m=1, n=1)
    assert res.is_rational is False
    assert res.status == "REDUCES_TO_S_TAU"
    assert "S_tau" in res.explanation
    assert res.combined_exponent == sqrt(2) + sqrt(3)


def test_09_sharp_unconditional_boundary_matrix():
    """Test structure and completeness of the sharp unconditional boundary matrix."""
    matrix = get_sharp_unconditional_boundary_matrix()
    ranks = matrix["ranks"]
    assert "rank_0" in ranks
    assert "rank_1_rational" in ranks
    assert "rank_1_irrational" in ranks
    assert "rank_2_linear_binomial" in ranks
    assert "rank_2_monomial" in ranks
    assert "rank_2_quadratic_conjugate_product" in ranks
    assert "rank_2_general_polynomial" in ranks

    assert ranks["rank_0"]["unconditional_status"] == "PROVED_EXACT_EQUIVALENCE"
    assert ranks["rank_1_rational"]["unconditional_status"] == "PROVED_INJECTIVE_LINDEMANN"
    assert ranks["rank_1_irrational"]["unconditional_status"] == "EXACTLY_CLASSIFIED_BY_S_TAU"
    assert "LINDEMANN" in ranks["rank_2_linear_binomial"]["unconditional_status"]
    assert "LINDEMANN" in ranks["rank_2_monomial"]["unconditional_status"]
    assert "OPEN_FRONTIER" in ranks["rank_2_general_polynomial"]["unconditional_status"]


def test_10_certify_rank_two_polynomial_exclusion_base_one():
    """Test Arb ball non-vanishing certification for canonical base-one instance (1, sqrt(2))."""
    res = certify_rank_two_polynomial_exclusion(
        sp.Integer(1), sqrt(2), max_degree=1, height_bound=2, dps=100
    )
    assert res["status"] == "CERTIFIED_FINITE_RELATION_EXCLUSION"
    assert res["evidence_class"] == "CERTIFIED_FINITE"
    assert res["total_polynomials_tested"] == 5**3 - 1  # 124 polynomials
    assert res["min_rigorous_lower_bound"] > 0


def test_11_certify_rank_two_polynomial_exclusion_incommensurable():
    """Test Arb ball non-vanishing certification for (sqrt(2), sqrt(3))."""
    res = certify_rank_two_polynomial_exclusion(
        sqrt(2), sqrt(3), max_degree=1, height_bound=2, dps=100
    )
    assert res["status"] == "CERTIFIED_FINITE_RELATION_EXCLUSION"
    assert res["total_polynomials_tested"] == 124
    assert res["min_rigorous_lower_bound"] > 0


def test_12_certify_rank_two_polynomial_exclusion_quadratic_conjugate():
    """Test Arb ball non-vanishing certification for quadratic conjugate pair (1+sqrt(2), 1-sqrt(2))."""
    res = certify_rank_two_polynomial_exclusion(
        1 + sqrt(2), 1 - sqrt(2), max_degree=1, height_bound=2, dps=100
    )
    assert res["status"] == "CERTIFIED_FINITE_RELATION_EXCLUSION"
    assert res["total_polynomials_tested"] == 124
    assert res["min_rigorous_lower_bound"] > 0
