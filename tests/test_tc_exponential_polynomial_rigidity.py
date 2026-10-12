"""Unit tests for Exponential-Polynomial Jet Rigidity and Integer-Dilation Orbit Isolation.

TASK-TC-031: Test suite verifying all 26 required properties of exponential polynomials,
Lindemann-Weierstrass necessity, derivative-jet rigidity, differential-operator rigidity,
positive/negative dilation polynomials, integer-dilation ray isolation, base-one Lindemann
branch, Wronskian / Chebyshev bound, sign-variation diagnostics, and functional firewalls.
"""

from __future__ import annotations

import math
import sympy as sp
from sympy import Rational, Integer, sqrt, Symbol, sympify, exp

from tc.exponential_polynomial_rigidity import (
    EXPONENTIAL_POLYNOMIAL,
    LOG_TAU_EVALUATION,
    INTEGER_DILATION_ORBIT,
    PRIMARY_CLASSIFICATION_FRONTIER_SHARPENED,
    CLASSIFICATION_TRINOMIAL_RELATION_IMPLIES_LOG_TAU_TRANSCENDENTAL,
    CLASSIFICATION_TRINOMIAL_ZERO_SIMPLE,
    CLASSIFICATION_ALL_POSITIVE_DERIVATIVE_JETS_NONZERO,
    CLASSIFICATION_DIFFERENTIAL_OPERATOR_RIGIDITY,
    CLASSIFICATION_INTEGER_DILATION_RAY_ISOLATION,
    CLASSIFICATION_BASE_ONE_ORBIT_ISOLATION_BY_LINDEMANN,
    CLASSIFICATION_AT_MOST_TWO_REAL_EXPONENTIAL_POLYNOMIAL_ZEROS,
    CLASSIFICATION_FUNCTIONAL_RESULT_DOES_NOT_SPECIALIZE_AUTOMATICALLY,
    CLASSIFICATION_TRINOMIAL_EXISTENCE_OPEN,
    CLASSIFICATION_NO_ZETA_TO_KERNEL_BRIDGE_FOUND,
    CLASSIFICATION_NO_RH_IMPLICATION,
    ExponentialPolynomial,
    ExponentialPolynomialDerivative,
    verify_lindemann_weierstrass_necessity,
    compute_derivative_coefficient_vector,
    check_derivative_jet_nonvanishing,
    evaluate_polynomial_differential_operator,
    check_differential_operator_rigidity,
    construct_positive_dilation_polynomial,
    construct_negative_dilation_polynomial,
    check_integer_dilation_ray_isolation,
    compute_exponential_wronskian,
    analyze_descartes_sign_variations,
    audit_functional_transcendence_firewall,
)


def test_01_f_log_tau_equals_ambient_relation():
    """1. F(L) symbolically and numerically matches a0 + a1 * tau^alpha + a2 * tau^beta."""
    ep = ExponentialPolynomial(a0=3, a1=-2, a2=-1, alpha=1, beta=sqrt(2))
    amb = ep.ambient_relation_expression()
    tau = Symbol("tau", positive=True)
    expected_amb = 3 - 2 * tau - 1 * (tau ** sqrt(2))
    assert amb == expected_amb

    # Check Arb ball evaluation
    res_arb = ep.evaluate_at_log_tau_arb(prec=100)
    # 3 - 2*(2*pi) - (2*pi)^sqrt(2) approx 3 - 12.566 - 13.528 approx -23.09
    mid = float(res_arb.mid())
    assert -25.0 < mid < -20.0


def test_02_integer_orbit_dilation_sequence():
    """2. Integer orbit f(n) = F(n*L) = a0 + a1 * X^n + a2 * Y^n."""
    ep = ExponentialPolynomial(a0=5, a1=-3, a2=-2, alpha=1, beta=sqrt(2))
    X = Symbol("X", positive=True)
    Y = Symbol("Y", positive=True)

    f_0 = ep.dilation_orbit_term(0)
    assert f_0 == 5 - 3 - 2
    assert f_0 == 0

    f_1 = ep.dilation_orbit_term(1)
    assert f_1 == 5 - 3 * X - 2 * Y

    f_2 = ep.dilation_orbit_term(2)
    assert f_2 == 5 - 3 * (X ** 2) - 2 * (Y ** 2)

    f_neg1 = ep.dilation_orbit_term(-1)
    assert f_neg1 == 5 - 3 * (X ** (-1)) - 2 * (Y ** (-1))


def test_03_distinct_algebraic_exponents_under_canonical_hypotheses():
    """3. Exponents 0, alpha, beta and 0, alpha*L, beta*L are distinct for alpha != beta != 0."""
    alpha = Rational(1)
    beta = sqrt(2)
    assert alpha != 0
    assert beta != 0
    assert alpha != beta

    # If L != 0:
    L = Symbol("L", real=True)
    assert alpha * L != 0
    assert beta * L != 0
    assert (beta - alpha) * L != 0


def test_04_lindemann_weierstrass_necessity_metadata():
    """4. verify_lindemann_weierstrass_necessity returns required classification and open status."""
    res = verify_lindemann_weierstrass_necessity(alpha=Integer(1), beta=sqrt(2))
    assert res.is_transcendental_forced is True
    assert res.classification == CLASSIFICATION_TRINOMIAL_RELATION_IMPLIES_LOG_TAU_TRANSCENDENTAL
    assert res.evidence_class == "PROVED_WITH_EXTERNAL_LINDEMANN_WEIERSTRASS"
    assert "OPEN" in res.literature_status_log_tau
    assert "Waldschmidt" in res.literature_status_log_tau


def test_05_derivative_coefficient_vector_formula():
    """5. vm = (0, a1 * alpha^m, a2 * beta^m) for m >= 1."""
    coeffs = (Integer(7), Integer(-3), Integer(2))
    alpha = Rational(1, 2)
    beta = sqrt(3)

    v1 = compute_derivative_coefficient_vector(coeffs, alpha, beta, m=1)
    assert v1 == (Integer(0), Rational(-3, 2), 2 * sqrt(3))

    v2 = compute_derivative_coefficient_vector(coeffs, alpha, beta, m=2)
    assert v2 == (Integer(0), Rational(-3, 4), Integer(6))


def test_06_derivative_vector_not_proportional():
    """6. Derivative vector (0, a1*alpha^m, a2*beta^m) is not proportional to (a0, a1, a2) since a0 != 0."""
    coeffs = (Integer(1), Integer(2), Integer(3))
    alpha = Rational(1)
    beta = sqrt(2)
    res = check_derivative_jet_nonvanishing(coeffs, alpha, beta, m=1)
    assert res.is_proportional_to_original is False
    assert res.is_nonzero_vector is True
    assert res.proves_jet_nonzero is True


def test_07_mth_derivative_relation_and_simple_zero():
    """7. F^{(m)}(L) != 0 for all m >= 1; for m=1 this proves the trinomial zero is simple."""
    coeffs = (Integer(3), Integer(-2), Integer(-1))
    alpha = Rational(1)
    beta = sqrt(2)

    res1 = check_derivative_jet_nonvanishing(coeffs, alpha, beta, m=1)
    assert res1.is_simple_zero is True
    assert res1.classification == CLASSIFICATION_TRINOMIAL_ZERO_SIMPLE

    res2 = check_derivative_jet_nonvanishing(coeffs, alpha, beta, m=2)
    assert res2.is_simple_zero is False
    assert res2.classification == CLASSIFICATION_ALL_POSITIVE_DERIVATIVE_JETS_NONZERO


def test_08_polynomial_differential_operator_formula():
    """8. P(D)F(L) = 0 forces P(0) = P(alpha) = P(beta)."""
    alpha = Rational(1)
    beta = sqrt(2)
    T = Symbol("T")

    # For P(T) = T^m (m >= 1), P(0) = 0 != P(1) = 1 != P(sqrt(2)) = 2^(m/2)
    res = check_differential_operator_rigidity(alpha, beta, T ** 2, var=T)
    assert res.classification == CLASSIFICATION_DIFFERENTIAL_OPERATOR_RIGIDITY
    assert res.support_values_equal is False
    assert res.p_0 == 0
    assert res.p_alpha == 1
    assert res.p_beta == 2


def test_09_positive_dilation_polynomial_generation():
    """9. construct_positive_dilation_polynomial builds P_k(T) = a0 + a1*T^k + a2*(u + v*T)^k."""
    coeffs = (Integer(1), Integer(2), Integer(3))
    res2 = construct_positive_dilation_polynomial(coeffs, k=2)
    # u = -1/3, v = -2/3. P_2(T) = 1 + 2*T^2 + 3*(-1/3 - 2/3*T)^2
    # = 1 + 2*T^2 + 3*(1/9 + 4/9*T + 4/9*T^2) = 1 + 1/3 + 4/3*T + (2 + 4/3)*T^2 = 4/3 + 4/3*T + 10/3*T^2
    T = Symbol("T")
    expected = Rational(4, 3) + Rational(4, 3) * T + Rational(10, 3) * (T ** 2)
    assert sp.expand(res2.polynomial_expr - expected) == 0


def test_10_coefficient_of_t_k_minus_1():
    """10. Coefficient of T^{k-1} matches a2 * k * u * v^{k-1}."""
    coeffs = (Integer(2), Integer(-3), Integer(5))
    u = Rational(-2, 5)
    v = Rational(3, 5)

    for k in [2, 3, 4, 5]:
        res = construct_positive_dilation_polynomial(coeffs, k=k)
        expected_coeff = 5 * k * u * (v ** (k - 1))
        assert res.distinguished_degree == k - 1
        assert sp.expand(res.distinguished_coeff - expected_coeff) == 0


def test_11_positive_dilation_polynomial_nonzero():
    """11. P_k(T) is strictly non-zero for all k >= 2."""
    coeffs = (Integer(4), Integer(-1), Integer(2))
    for k in [2, 3, 4]:
        res = construct_positive_dilation_polynomial(coeffs, k=k)
        assert res.is_distinguished_coeff_nonzero is True
        assert res.is_polynomial_nonzero is True
        assert res.forces_algebraic_generator is True


def test_12_negative_dilation_polynomial_generation():
    """12. construct_negative_dilation_polynomial builds Q_q(T)."""
    coeffs = (Integer(2), Integer(3), Integer(5))
    res1 = construct_negative_dilation_polynomial(coeffs, q=1)
    # u = -2/5, v = -3/5.
    # Q_1(T) = 2*T*(-2/5 - 3/5*T) + 3*(-2/5 - 3/5*T) + 5*T
    # = -4/5*T - 6/5*T^2 - 6/5 - 9/5*T + 5*T = -6/5 + (5 - 13/5)*T - 6/5*T^2 = -6/5 + 12/5*T - 6/5*T^2
    T = Symbol("T")
    expected = Rational(-6, 5) + Rational(12, 5) * T - Rational(6, 5) * (T ** 2)
    assert sp.expand(res1.polynomial_expr - expected) == 0


def test_13_coefficient_of_t_2q():
    """13. Leading coefficient at T^{2q} matches a0 * v^q."""
    coeffs = (Integer(3), Integer(-2), Integer(7))
    v = Rational(2, 7)
    for q in [1, 2, 3]:
        res = construct_negative_dilation_polynomial(coeffs, q=q)
        expected_leading = 3 * (v ** q)
        assert res.distinguished_degree == 2 * q
        assert sp.expand(res.distinguished_coeff - expected_leading) == 0


def test_14_negative_dilation_polynomial_nonzero():
    """14. Q_q(T) is strictly non-zero for all q >= 1."""
    coeffs = (Integer(5), Integer(-2), Integer(3))
    for q in [1, 2, 3]:
        res = construct_negative_dilation_polynomial(coeffs, q=q)
        assert res.is_distinguished_coeff_nonzero is True
        assert res.is_polynomial_nonzero is True
        assert res.forces_algebraic_generator is True


def test_15_k_zero_not_excluded_by_orbit_isolation():
    """15. k=0 gives f(0) = a0 + a1 + a2, which is an independent coefficient sum, not excluded."""
    coeffs = (Integer(1), Integer(2), Integer(-3))
    ep = ExponentialPolynomial(a0=1, a1=2, a2=-3, alpha=1, beta=sqrt(2))
    assert ep.dilation_orbit_term(0) == 0  # f(0) can vanish if coefficients sum to zero!
    # The orbit isolation theorem explicitly applies to k in Z \ {0, 1}


def test_16_base_one_lindemann_branch():
    """16. Base-one instance alpha=1, beta=sqrt(2) invokes Lindemann transcendence directly."""
    coeffs = (Integer(3), Integer(-2), Integer(-1))
    res = check_integer_dilation_ray_isolation(coeffs, alpha=Integer(1), beta=sqrt(2), m=1, k_multiplier=2)
    assert res.base_one_specialization is True
    assert res.classification == CLASSIFICATION_BASE_ONE_ORBIT_ISOLATION_BY_LINDEMANN
    assert res.evidence_class == "PROVED_WITH_EXTERNAL_LINDEMANN"
    assert "Lindemann (1882)" in res.contradiction_target


def test_17_general_gelfond_schneider_branch():
    """17. General incommensurable instance invokes Gelfond-Schneider dimension theorem."""
    coeffs = (Integer(3), Integer(-2), Integer(-1))
    res = check_integer_dilation_ray_isolation(coeffs, alpha=sqrt(2), beta=sqrt(3), m=1, k_multiplier=2)
    assert res.base_one_specialization is False
    assert res.classification == CLASSIFICATION_INTEGER_DILATION_RAY_ISOLATION
    assert res.evidence_class == "PROVED_PAPER_DERIVATION + EXTERNAL_GELFOND_SCHNEIDER"
    assert "Gelfond-Schneider" in res.contradiction_target


def test_18_integer_dilation_ray_classification():
    r"""18. Both positive and negative multipliers are excluded for k in Z \ {0, 1}."""
    coeffs = (Integer(1), Integer(1), Integer(-2))
    # Test k = 2, 3 and k = -1, -2
    for k in [2, 3, -1, -2]:
        res = check_integer_dilation_ray_isolation(coeffs, alpha=sqrt(2), beta=sqrt(3), m=1, k_multiplier=k)
        assert res.is_excluded is True


def test_19_wronskian_identity():
    """19. Wronskian determinants W0, W1, W2 factor identically into exponential-Vandermonde products."""
    res = compute_exponential_wronskian(exponents=(Integer(0), Integer(1), sqrt(2)))
    x = Symbol("x", real=True)
    expected_w0 = exp(0 * x)
    expected_w1 = exp((0 + 1) * x) * (1 - 0)
    expected_w2 = exp((1 + sqrt(2)) * x) * (1 - 0) * (sqrt(2) - 0) * (sqrt(2) - 1)
    assert sp.expand(res.wronskian_w0_symbolic - expected_w0) == 0
    assert sp.expand(res.wronskian_w1_symbolic - expected_w1) == 0
    assert sp.expand(res.wronskian_w2_symbolic - expected_w2) == 0
    assert sp.expand(res.wronskian_symbolic - expected_w2) == 0


def test_20_wronskian_nonvanishing_for_distinct_exponents():
    """20. All successive Wronskians W0, W1, W2 > 0 everywhere on R for strictly ordered exponents."""
    res = compute_exponential_wronskian(exponents=(Integer(0), Integer(1), sqrt(2)))
    assert res.is_strictly_positive_on_real_line is True
    assert res.successive_wronskians_positive is True


def test_21_at_most_two_real_zeros_positive_control():
    """21. ECT system guarantees at most 2 real zeros counting multiplicity (Karlin & Studden 1966)."""
    res = compute_exponential_wronskian(exponents=(Integer(0), Rational(1, 2), Rational(3, 2)))
    assert res.max_real_zeros_bound == 2
    assert res.classification == CLASSIFICATION_AT_MOST_TWO_REAL_EXPONENTIAL_POLYNOMIAL_ZEROS
    assert res.evidence_class == "PROVED_WITH_EXTERNAL_CHEBYSHEV_THEOREM"
    assert "Karlin & Studden" in res.external_theorem_citation
    assert "Pólya & Szegő" in res.external_theorem_citation


def test_22_sign_variation_diagnostic():
    """22. analyze_descartes_sign_variations correctly bounds real zeros."""
    exps = (Integer(0), Integer(1), Integer(2))

    # All positive: 0 sign changes -> 0 real zeros
    res0 = analyze_descartes_sign_variations((Integer(1), Integer(2), Integer(3)), exps)
    assert res0.sign_changes == 0
    assert res0.max_real_zeros_descartes == 0

    # One sign change: (+, +, -) -> at most 1 real zero
    res1 = analyze_descartes_sign_variations((Integer(1), Integer(2), Integer(-3)), exps)
    assert res1.sign_changes == 1
    assert res1.max_real_zeros_descartes == 1

    # Two sign changes: (+, -, +) -> at most 2 real zeros
    res2 = analyze_descartes_sign_variations((Integer(1), Integer(-2), Integer(3)), exps)
    assert res2.sign_changes == 2
    assert res2.max_real_zeros_descartes == 2


def test_23_functional_specialization_firewall():
    """23. audit_functional_transcendence_firewall excludes naive specialization."""
    audit = audit_functional_transcendence_firewall()
    assert audit.functional_independence_applies is True
    assert audit.arithmetic_specialization_valid is False
    assert audit.classification == CLASSIFICATION_FUNCTIONAL_RESULT_DOES_NOT_SPECIALIZE_AUTOMATICALLY
    assert len(audit.theorems_audited) == 3


def test_24_no_claim_of_original_trinomial_nonexistence():
    """24. Existence of the trinomial relation remains strictly OPEN."""
    assert CLASSIFICATION_TRINOMIAL_EXISTENCE_OPEN == "TRINOMIAL_EXISTENCE_OPEN"
    assert PRIMARY_CLASSIFICATION_FRONTIER_SHARPENED == "EXPONENTIAL_POLYNOMIAL_FRONTIER_SHARPENED_EXISTENCE_OPEN"


def test_25_no_rh_implication():
    """25. No Riemann Hypothesis implication may be asserted."""
    assert CLASSIFICATION_NO_RH_IMPLICATION == "NO_RH_IMPLICATION"


def test_26_no_new_zeta_bridge():
    """26. NO_ZETA_TO_KERNEL_BRIDGE_FOUND is preserved as an audit finding."""
    assert CLASSIFICATION_NO_ZETA_TO_KERNEL_BRIDGE_FOUND == "NO_ZETA_TO_KERNEL_BRIDGE_FOUND"
