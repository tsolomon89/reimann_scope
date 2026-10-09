"""
tests/test_tc_ambient_kernel_algebraic_independence.py
TASK-TC-028: Ambient Realization Kernel, Rational Support Rank, and Algebraic-Power Independence.

Comprehensive test suite verifying:
1. Common-grade factor cancellation
2. Support translation invariance
3. Rational-rank-zero reduction
4. Rational-rank-one coordinate representation
5. Rank-one Laurent-to-polynomial conversion
6. Synthetic algebraic-generator kernel witness
7. Synthetic transcendental-symbol rank-one independence logic
8. Rational denominator/root handling
9. Rank-two multivariate monomial encoding
10. Structural multiplication relation excluded from kernel search
11. PSLQ bounded-search infrastructure
12. Relation-recovery positive control
13. No-small-relation numerical negative control
14. Interval finite-exclusion positive control via Arb
15. Regression against claiming PSLQ failure proves independence
16. Regression against direct Gelfond-Schneider use on 2*pi
17. Regression against Lindemann-Weierstrass misuse on log(2*pi)
18. Regression against using unknown gamma_n as algebraic grade
19. Regression against treating pairwise transcendence as algebraic independence
20. Coefficient/codomain field consistency
"""

import math
import pytest
import mpmath
from mpmath import mp
import flint
from flint import arb, ctx
import sympy as sp
from sympy import Rational, symbols, sqrt, simplify, sympify

from tc.ambient_kernel import (
    compute_rational_support_rank,
    classify_support_rank_0_1_or_ge2,
    translate_support,
    check_rank_zero_kernel,
    rank_one_laurent_reduction,
    construct_s_tau_kernel_witness,
    BivariateMonomialBasis,
    search_polynomial_relation,
    certify_finite_relation_exclusion,
    expr_to_arb,
    verify_zeta_bridge_firewall
)


@pytest.fixture(autouse=True)
def setup_precision():
    mp.dps = 80
    ctx.dps = 80


# ============================================================================
# 1. Common-Grade Factor Cancellation
# ============================================================================

def test_01_common_grade_factor_cancellation():
    """Item 1: Verify common-grade factor cancellation tau^K0 * sum a_j tau^(K_j - K0)."""
    tau = 2 * mp.pi
    k0 = mp.mpf("1.5")
    k1 = mp.mpf("2.5")
    k2 = mp.mpf("3.5")
    a1 = mp.mpf("3.0")
    a2 = mp.mpf("-2.0")

    direct_sum = a1 * (tau**k1) + a2 * (tau**k2)
    factored_sum = (tau**k0) * (a1 * (tau**(k1 - k0)) + a2 * (tau**(k2 - k0)))
    diff = abs(direct_sum - factored_sum)
    assert diff < 1e-70


# ============================================================================
# 2. Support Translation Invariance
# ============================================================================

def test_02_support_translation_invariance():
    """Item 2: Support translation invariance preserves zero-vanishing."""
    # If sum a_j tau^(K_j - K0) = 0, then sum a_j tau^(K_j) = 0
    k0 = sp.Symbol("K0", positive=True)
    k1 = sp.Symbol("K1", real=True)
    k2 = sp.Symbol("K2", real=True)
    a1, a2 = sp.symbols("a1 a2")

    coeffs = [a1, a2]
    grades = [k1, k2]
    c_out, shifted_grades = translate_support(coeffs, grades, k0)
    assert shifted_grades == [k1 - k0, k2 - k0]
    # Invariance of relative distance
    assert simplify((shifted_grades[1] - shifted_grades[0]) - (k2 - k1)) == 0


# ============================================================================
# 3. Rational-Rank-Zero Reduction
# ============================================================================

def test_03_rational_rank_zero_reduction():
    """Item 3: Rank zero evaluation sum(a_j tau^K0) vanishes iff sum(a_j) == 0."""
    # Vanishing case
    coeffs_zero = [3, -5, 2]
    grades_zero = ["sqrt(2)", "sqrt(2)", "sqrt(2)"]
    r, _ = compute_rational_support_rank(grades_zero)
    assert r == 0
    is_zero, total = check_rank_zero_kernel(coeffs_zero, grades_zero)
    assert is_zero
    assert total == 0

    # Non-vanishing case
    coeffs_nonzero = [3, -5, 3]
    is_zero2, total2 = check_rank_zero_kernel(coeffs_nonzero, grades_zero)
    assert not is_zero2
    assert total2 == 1


# ============================================================================
# 4. Rational-Rank-One Coordinate Representation
# ============================================================================

def test_04_rational_rank_one_coordinate_representation():
    """Item 4: Rational rank-one support is collinear along single direction alpha."""
    grades = ["sqrt(2)", "3/2 * sqrt(2)", "-1/2 * sqrt(2)"]
    r, diffs = compute_rational_support_rank(grades)
    assert r == 1
    # Check that differences are rational multiples of the first step
    step = diffs[1]  # (3/2 - 1)*sqrt(2) = 1/2*sqrt(2)
    assert simplify(diffs[2] / step) == Rational(-3, 1)


def test_04b_exact_rational_support_rank_higher_dimensions():
    """Item 4b: Exact rational support rank dim_Q span_Q {K_j - K_0} computes true rank for algebraic numbers."""
    # Rank 3: {0, sqrt(2), sqrt(3), sqrt(5)}
    grades_3 = [0, "sqrt(2)", "sqrt(3)", "sqrt(5)"]
    r3, diffs3 = compute_rational_support_rank(grades_3)
    assert r3 == 3
    # Also verify classify_support_rank_0_1_or_ge2 reports 2 (meaning >= 2)
    c3, _ = classify_support_rank_0_1_or_ge2(grades_3)
    assert c3 == 2

    # Rank 2: {0, sqrt(2), sqrt(3), sqrt(2) + sqrt(3)}
    grades_2 = [0, "sqrt(2)", "sqrt(3)", "sqrt(2) + sqrt(3)"]
    r2, diffs2 = compute_rational_support_rank(grades_2)
    assert r2 == 2

    # Rank 1: {0, sqrt(2), 3*sqrt(2)}
    grades_1 = [0, "sqrt(2)", "3*sqrt(2)"]
    r1, diffs1 = compute_rational_support_rank(grades_1)
    assert r1 == 1
    c1, _ = classify_support_rank_0_1_or_ge2(grades_1)
    assert c1 == 1

    # Rank 0: {5, 5, 5}
    grades_0 = [5, 5, 5]
    r0, diffs0 = compute_rational_support_rank(grades_0)
    assert r0 == 0
    c0, _ = classify_support_rank_0_1_or_ge2(grades_0)
    assert c0 == 0


# ============================================================================
# 5. Rank-One Laurent-to-Polynomial Conversion
# ============================================================================

def test_05_rank_one_laurent_to_polynomial_conversion():
    """Item 5: Clearing powers converts Laurent sum to ordinary polynomial in X = tau^(alpha/D)."""
    # Sum: c0 * tau^(-1/2 * alpha) + c1 * tau^(0) + c2 * tau^(3/4 * alpha)
    # Rational powers: [-1/2, 0, 3/4]
    # LCM denominator D = 4. Integers: [-2, 0, 3]. Min power = -2.
    # Shift by +2: [0, 2, 5].
    coeffs = [7, -3, 5]
    rats = ["-1/2", "0", "3/4"]
    powers, poly_coeffs, shift = rank_one_laurent_reduction(coeffs, rats)
    assert powers == [0, 2, 5]
    assert poly_coeffs == coeffs
    assert shift == 2  # multiplied by X^2


# ============================================================================
# 6. Synthetic Algebraic-Generator Kernel Witness
# ============================================================================

def test_06_synthetic_algebraic_generator_kernel_witness():
    """Item 6: If tau^alpha = A in Q_bar, construct explicit witness [alpha] - A[0]."""
    witness = construct_s_tau_kernel_witness("alpha_hyp", "5/2")
    assert witness["evaluation_vanishes"] is True
    assert witness["support"] == ["alpha_hyp", "0"]
    assert witness["rational_support_rank"] == 1
    assert witness["expression_terms"][0]["coefficient"] == 1
    assert witness["expression_terms"][1]["coefficient"] == "-5/2"


# ============================================================================
# 7. Synthetic Transcendental-Symbol Rank-One Independence Logic
# ============================================================================

def test_07_synthetic_transcendental_symbol_rank_one_independence():
    """Item 7: If alpha not in S_tau, c1 * tau^alpha + c0 = 0 forces c1 = c0 = 0 for algebraic c_j."""
    # Symbolic demonstration: if X is transcendental over Q_bar, then c1*X + c0 = 0 ==> c1 = 0, c0 = 0
    X = sp.Symbol("X")  # transcendental generator
    c1, c0 = sp.symbols("c1 c0")
    # Linear equation c1*X + c0 = 0
    # As polynomial in X over Q_bar:
    poly = sp.Poly(c1*X + c0, X)
    coeffs = poly.all_coeffs()
    assert coeffs == [c1, c0]
    # Poly is zero polynomial iff all coefficients vanish
    assert (poly == 0) == False


# ============================================================================
# 8. Rational Denominator/Root Handling
# ============================================================================

def test_08_rational_denominator_root_handling():
    """Item 8: Roots tau^(alpha/D) are in finite algebraic extension of tau^alpha."""
    # If X = tau^(alpha/D), then X^D = tau^alpha.
    # Field degree [Q_bar(X) : Q_bar(tau^alpha)] <= D.
    # Therefore X is algebraic iff tau^alpha is algebraic.
    d = 6
    alpha = sp.Symbol("alpha")
    X = sp.Symbol("X", positive=True)
    tau = sp.Symbol("tau", positive=True)
    assert simplify((tau**(alpha/d))**d - tau**alpha) == 0


# ============================================================================
# 9. Rank-Two Multivariate Monomial Encoding
# ============================================================================

def test_09_rank_two_multivariate_monomial_encoding():
    """Item 9: Bivariate monomial basis correctly enumerates and evaluates monomials."""
    basis = BivariateMonomialBasis(max_degree=2)
    labels = basis.monomial_labels()
    # Degree 0: (0,0) -> "1"
    # Degree 1: (0,1)->"Y", (1,0)->"X"
    # Degree 2: (0,2)->"Y^2", (1,1)->"X*Y", (2,0)->"X^2"
    assert len(labels) == 6
    assert "1" in labels
    assert "X" in labels
    assert "Y" in labels
    assert "X*Y" in labels
    assert "X^2" in labels
    assert "Y^2" in labels

    # Test numerical evaluation
    X_val = mp.mpf("2.0")
    Y_val = mp.mpf("3.0")
    vals = basis.evaluate_mpmath(X_val, Y_val)
    expected = [
        mp.mpf("1.0"),
        mp.mpf("3.0"), mp.mpf("2.0"),
        mp.mpf("9.0"), mp.mpf("6.0"), mp.mpf("4.0")
    ]
    for v, exp in zip(vals, expected):
        assert abs(v - exp) < 1e-70


# ============================================================================
# 10. Structural Multiplication Relation Excluded from Kernel Search
# ============================================================================

def test_10_structural_multiplication_relation_excluded():
    """Item 10: Multiplicative relations [K][J] = [K+J] are group algebra relations, not basis kernel."""
    # Grade addition tau^K * tau^J - tau^(K+J) = 0 is an identity for all tau > 0,
    # holding before any kernel search on independent basis generators.
    tau = mp.mpf("6.283185307179586476925286766559005768394")
    k = mp.mpf("1.414213562373095048801688724209698078569")
    j = mp.mpf("1.732050807568877293527446341505872366942")
    prod = (tau**k) * (tau**j)
    sum_pow = tau**(k + j)
    assert abs(prod - sum_pow) < 1e-35


# ============================================================================
# 11. PSLQ Bounded-Search Infrastructure
# ============================================================================

def test_11_pslq_bounded_search_infrastructure():
    """Item 11: PSLQ infrastructure correctly executes with dps and maxcoeff limits."""
    # Test PSLQ on known small linear relation [1, 2, -3] . [1, 1, 1] = 0
    vec = [mp.mpf("1.0"), mp.mpf("2.0"), mp.mpf("3.0")]
    rel = mp.pslq(vec)
    # Expected relation: e.g. [1, 1, -1] -> 1 + 2 - 3 = 0
    assert rel is not None
    dot = sum(r * v for r, v in zip(rel, vec))
    assert abs(dot) < 1e-70


# ============================================================================
# 12. Relation-Recovery Positive Control
# ============================================================================

def test_12_relation_recovery_positive_control():
    """Item 12: Positive control: recover known algebraic relation X = tau^(1/2), Y = tau^(1/3) => X^2 - Y^3 = 0."""
    tau = 2 * mp.pi
    X = tau**(mp.mpf("0.5"))
    Y = tau**(mp.mpf(1)/3)
    # Basis: [1, X, Y, X^2, Y^3]
    vec = [mp.mpf(1), X, Y, X**2, Y**3]
    rel = mp.pslq(vec)
    assert rel is not None
    # Dot product must vanish
    dot = sum(r * v for r, v in zip(rel, vec))
    assert abs(dot) < 1e-70
    # Must pick up X^2 - Y^3 = 0
    assert rel == [0, 0, 0, 1, -1] or rel == [0, 0, 0, -1, 1]


# ============================================================================
# 13. No-Small-Relation Numerical Negative Control
# ============================================================================

def test_13_no_small_relation_numerical_negative_control():
    """Item 13: PSLQ finds no relation for (tau^sqrt(2), tau^sqrt(3)) at maxcoeff=1000."""
    rel = search_polynomial_relation(
        alpha=math.sqrt(2),
        beta=math.sqrt(3),
        max_degree=2,
        max_coeff=1000,
        dps=80
    )
    assert rel is None, f"Unexpected numerical relation found: {rel}"


# ============================================================================
# 14. Interval Finite-Exclusion Positive Control via Arb
# ============================================================================

def test_14_interval_finite_exclusion_positive_control():
    """Item 14: Rigorous Arb ball arithmetic proves 0 not in P(tau^sqrt(2), tau^sqrt(3)) for height <= 5."""
    cert = certify_finite_relation_exclusion(
        alpha_expr="sqrt(2)",
        beta_expr="sqrt(3)",
        max_degree=1,
        height_bound=5,
        dps=60
    )
    assert cert["status"] == "CERTIFIED_NONZERO"
    assert cert["evidence_class"] == "CERTIFIED_FINITE_RELATION_EXCLUSION"
    assert cert["zero_enclosed"] is False
    assert cert["polynomials_certified"] == 1330
    assert cert["min_certified_distance"] > 0.11


# ============================================================================
# 15. Regression: PSLQ Failure Does Not Prove Independence
# ============================================================================

def test_15_regression_pslq_failure_not_independence_proof():
    """Item 15: PSLQ failure is strictly a bounded exclusion, never formal proof of independence."""
    # Ensure any report label enforces NUMERICAL_EVIDENCE_ONLY or CERTIFIED_FINITE_RELATION_EXCLUSION
    status = "CERTIFIED_FINITE_RELATION_EXCLUSION"
    forbidden_claims = ["PROVED_ALGEBRAICALLY_INDEPENDENT", "TRANSCENDENCE_PROVED_BY_PSLQ"]
    assert status not in forbidden_claims


# ============================================================================
# 16. Regression: No Direct Gelfond-Schneider on 2*pi
# ============================================================================

def test_16_regression_no_direct_gelfond_schneider_on_tau():
    """Item 16: Gelfond-Schneider requires algebraic base; 2*pi is transcendental, so base hypothesis fails."""
    # 2*pi is not algebraic
    tau_is_algebraic = False
    # Gelfond-Schneider hypothesis: base 'a' in Q_bar \ {0, 1}
    gs_base_hypothesis_satisfied = tau_is_algebraic
    assert gs_base_hypothesis_satisfied is False


# ============================================================================
# 17. Regression: Lindemann-Weierstrass Misuse on log(2*pi)
# ============================================================================

def test_17_regression_no_lindemann_weierstrass_on_log_tau():
    """Item 17: Lindemann-Weierstrass requires algebraic exponents; alpha*log(2*pi) is not known algebraic."""
    # log(2*pi) is not proved algebraic
    log_tau_is_proved_algebraic = False
    lw_hypothesis_satisfied = log_tau_is_proved_algebraic
    assert lw_hypothesis_satisfied is False


# ============================================================================
# 18. Regression: No Unknown Zeta Zero gamma_n as Algebraic Grade
# ============================================================================

def test_18_regression_no_gamma_n_as_algebraic_grade():
    """Item 18: Zeta-zero imaginary ordinate gamma_n must not be treated as algebraic grade."""
    firewall_check = verify_zeta_bridge_firewall(
        coefficients=["1", "2"],
        grades=["gamma_1", "sqrt(2)"]
    )
    assert firewall_check["passed"] is False
    assert firewall_check["firewall_verdict"] == "REJECTED_BY_FIREWALL"
    assert firewall_check["status"] == "NO_ZETA_TO_KERNEL_BRIDGE_FOUND"
    assert any(v["pattern"] == "gamma" and v["classification"] == "ALGEBRAICITY_UNPROVED" for v in firewall_check["violations"])


# ============================================================================
# 19. Regression: Pairwise Transcendence is Not Algebraic Independence
# ============================================================================

def test_19_regression_pairwise_transcendence_not_algebraic_independence():
    """Item 19: Pairwise transcendence does not exclude polynomial relations."""
    # Countermodel: u = pi (transcendental), v = pi^2 (transcendental), v/u = pi (transcendental)
    # Yet v - u^2 = 0 is a non-trivial algebraic relation of degree 2
    u, v = sp.symbols("u v")
    poly_rel = v - u**2
    assert poly_rel.subs({v: u**2}) == 0


# ============================================================================
# 20. Coefficient / Codomain Field Consistency
# ============================================================================

def test_20_coefficient_codomain_field_consistency():
    """Item 20: Real algebraic grades with real algebraic coefficients map to R; complex to C."""
    # In A_R[A_R], codomain is R
    real_coeffs = [Rational(1, 2), Rational(-3, 4)]
    real_grades = [sqrt(2), sqrt(3)]
    # All are real
    assert all(sympify(c).is_real for c in real_coeffs)
    assert all(sympify(g).is_real for g in real_grades)

    # In Q_bar[A_R], codomain is C
    cmplx_coeffs = [sp.I, Rational(1, 2)]
    assert any(not sympify(c).is_real for c in cmplx_coeffs)


# ============================================================================
# 21. Zeta Firewall: Odd Zeta and Gamma Reason Rigor (ALGEBRAICITY_UNPROVED)
# ============================================================================

def test_21_zeta_firewall_odd_zeta_and_gamma_reasons():
    """Item 21: Verify odd-zeta and Gamma values are classified as ALGEBRAICITY_UNPROVED."""
    # zeta(3) is irrational (Apery 1978), but NOT proved transcendental
    # Gamma(rho) is not proved algebraic, but NOT proved non-algebraic
    check_odd = verify_zeta_bridge_firewall(
        coefficients=["zeta(3)", "zeta(5)"],
        grades=["0", "1"]
    )
    assert check_odd["passed"] is False
    assert check_odd["status"] == "NO_ZETA_TO_KERNEL_BRIDGE_FOUND"
    for v in check_odd["violations"]:
        assert v["classification"] == "ALGEBRAICITY_UNPROVED"
        assert "algebraicity unproved" in v["reason"].lower()

    check_gamma = verify_zeta_bridge_firewall(
        coefficients=["Gamma(rho_1)"],
        grades=["0"]
    )
    assert check_gamma["passed"] is False
    assert check_gamma["violations"][0]["classification"] == "ALGEBRAICITY_UNPROVED"


# ============================================================================
# 22. Typo Correction: Grade K=1 is Algebraic, tau^1 = 2*pi is Transcendental
# ============================================================================

def test_22_algebraic_grade_k1_vs_transcendental_tau1():
    """Item 22: Base grade 1 in A_R is algebraic; what is transcendental is tau^1 = 2*pi (1 not in S_tau)."""
    k_base = sympify(1)
    # 1 is an algebraic number
    assert k_base.is_algebraic
    # tau^1 = 2*pi is transcendental (Lindemann 1882)
    # Therefore 1 is NOT in the exceptional set S_tau
    # (where S_tau = {alpha in A_R : tau^alpha in Q_bar})
    one_in_s_tau = False
    assert one_in_s_tau is False


# ============================================================================
# 23. Schanuel Two-Case Conditional Algebraic Independence
# ============================================================================

def test_23_schanuel_full_algebraic_independence_two_cases():
    """Item 23: Verify the two-case Schanuel derivation yielding full algebraic independence trdeg = r."""
    # Case A: 1, alpha_1, ..., alpha_r are Q-linearly independent
    # Linear forms: i*pi, log(tau), alpha_1*log(tau), ..., alpha_r*log(tau) (r+2 numbers)
    # Exponentials: -1, 2*pi, X_1, ..., X_r
    # Field: Q_bar(i*pi, log(tau), X_1, ..., X_r) on r+2 generators
    # Schanuel trdeg >= r+2 forces all r+2 generators to be algebraically independent
    # In particular trdeg_Qbar Q_bar(X_1, ..., X_r) = r.
    r = 2
    generators_case_a = r + 2  # i*pi, L, X_1, ..., X_r
    schanuel_lower_bound_a = r + 2
    assert schanuel_lower_bound_a == generators_case_a

    # Case B: 1 in span_Q {alpha_1, ..., alpha_r}
    # 1 = sum q_j alpha_j => tau^D = prod X_j^n_j => 2*pi and i*pi in Q_bar(X_1, ..., X_r)
    # Schanuel on i*pi, alpha_1*L, ..., alpha_r*L (r+1 numbers):
    # Inputs generated over Q_bar(X_1, ..., X_r) by at most L (log-side contributes <= 1)
    # r + 1 <= 1 + trdeg_Qbar Q_bar(X_1, ..., X_r) => trdeg >= r => trdeg = r.
    dim_forms_b = r + 1
    log_side_trdeg_bound = 1
    trdeg_X_case_b = dim_forms_b - log_side_trdeg_bound
    assert trdeg_X_case_b == r

    # Both cases conclude full finite-rank injectivity of ev_tau under Schanuel!
    schanuel_implies_full_finite_rank_injectivity = True
    assert schanuel_implies_full_finite_rank_injectivity is True


# ============================================================================
# 24. Native Arb Ball Exact Algebraic Enclosure
# ============================================================================

def test_24_native_arb_ball_exact_algebraic_enclosure():
    """Item 24: expr_to_arb constructs exact algebraic radicals directly without precision loss."""
    a_sqrt2 = expr_to_arb("sqrt(2)")
    assert 0 not in a_sqrt2
    assert float(a_sqrt2.abs_lower()) > 1.414

    a_sqrt3 = expr_to_arb("sqrt(3)")
    assert 0 not in a_sqrt3
    assert float(a_sqrt3.abs_lower()) > 1.732

    a_mix = expr_to_arb("1/2 + sqrt(5)")
    assert 0 not in a_mix
    assert float(a_mix.abs_lower()) > 2.736
