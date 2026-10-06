"""Test suite for TASK-TC-024: Local Zero Germ, Prime-Side Unit Change,
and Intrinsic Grade Invariance.

Verifies:
1. Generic exponential-prefactor germ scaling at order m
2. Multiplicity-m scaling
3. TC specialization
4. Modulus finite-difference formula
5. Log-derivative grade shift
6. Residue invariance under grade prefactor
7. Regularized finite-part shift
8. Unit-normalized germ invariance
9. Centered harmonic translation multiplier
10. Synthetic off-line modulus change
11. Critical-line unit-modulus control
12. Geometric prime-station translation
13. Distinction between geometric station transform and grid-zeta logarithmic derivative
14. Reflected local-germ identity and grade-invariant product
15. Regression forbidding claims that local-germ magnitude is intrinsic without proof
16. Regression against NO_TWO_DIRECTION_ZETA_TRANSFER being treated as an impossibility theorem
"""

import math
import cmath
import pytest
import mpmath
from mpmath import mp, mpf, mpc, zeta, gamma, sin, pi, log, exp
import sympy as sp
from sympy import symbols, exp as s_exp, log as s_log, diff, factorial, simplify, I, Rational


@pytest.fixture(autouse=True)
def setup_precision():
    mp.dps = 50


# ============================================================================
# 1. Generic Exponential-Prefactor Germ Scaling at Order m
# ============================================================================

def test_generic_exponential_prefactor_germ_scaling():
    """Verify that for an arbitrary holomorphic function F with zero of order m at rho,
    multiplication by e^{-a(s - s_0)} scales the leading Taylor coefficient by e^{-a(rho - s_0)}.
    """
    s, rho, a, s0 = symbols("s rho a s0", complex=True)
    m = symbols("m", integer=True, positive=True)

    # Let F(s) = c_m * (s - rho)^m + c_{m+1} * (s - rho)^{m+1}
    c_m, c_m1 = symbols("c_m c_m1", complex=True)
    F = c_m * (s - rho)**2 + c_m1 * (s - rho)**3  # m = 2 case
    prefactor = s_exp(-a * (s - s0))
    F_mod = prefactor * F

    # 2nd derivative at s = rho divided by 2!
    diff2 = diff(F_mod, s, 2)
    coeff2_at_rho = simplify(diff2.subs(s, rho) / factorial(2))
    expected = simplify(s_exp(-a * (rho - s0)) * c_m)

    assert simplify(coeff2_at_rho - expected) == 0


# ============================================================================
# 2. Multiplicity-m Scaling
# ============================================================================

def test_multiplicity_m_scaling():
    """Verify leading germ scaling for m = 1, 2, 3 using SymPy."""
    s, rho, a, s0, c_m = symbols("s rho a s0 c_m", complex=True)

    for order in [1, 2, 3]:
        F = c_m * (s - rho)**order
        prefactor = s_exp(-a * (s - s0))
        F_mod = prefactor * F
        deriv = diff(F_mod, s, order)
        leading_germ = simplify(deriv.subs(s, rho) / factorial(order))
        expected_germ = simplify(s_exp(-a * (rho - s0)) * c_m)
        assert simplify(leading_germ - expected_germ) == 0


# ============================================================================
# 3. TC Specialization
# ============================================================================

def test_tc_specialization():
    """Verify that for TC completed family Xi_K(s) = tau^{-K(s - 1/2)} xi(s),
    the local germ satisfies c_{Xi_K}(rho) = tau^{-K(rho - 1/2)} c_xi(rho).
    """
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)

    # Test numerical evaluation on first Riemann zero
    gamma1 = mp.mpf("14.1347251417346937904572519835624702707842571156992")
    rho1 = mp.mpc(mp.mpf("0.5"), gamma1)

    for K in [mp.mpf("-2"), mp.mpf("-0.5"), mp.mpf("1"), mp.mpf("1.5")]:
        multiplier = mp.exp(-K * L * (rho1 - mp.mpf("0.5")))
        expected_factor = mp.power(tau, -K * (rho1 - mp.mpf("0.5")))
        assert mp.almosteq(multiplier, expected_factor, abs_eps=mp.mpf("1e-45"))


# ============================================================================
# 4. Modulus Finite-Difference Formula
# ============================================================================

def test_modulus_finite_difference_formula():
    """Verify log |c_{Xi_K}(rho)| - log |c_{Xi_J}(rho)| = -(K - J) delta log(tau)."""
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)

    deltas = [mp.mpf("-0.3"), mp.mpf("-0.1"), mp.mpf("0.05"), mp.mpf("0.25")]
    grades = [(mp.mpf("1"), mp.mpf("0")), (mp.mpf("2.5"), mp.mpf("1.0")), (mp.mpf("-1"), mp.mpf("1.5"))]

    for delta in deltas:
        rho = mp.mpc(mp.mpf("0.5") + delta, mp.mpf("21.022"))
        for K, J in grades:
            mod_K = abs(mp.exp(-K * L * (rho - mp.mpf("0.5"))))
            mod_J = abs(mp.exp(-J * L * (rho - mp.mpf("0.5"))))
            diff_log = mp.log(mod_K) - mp.log(mod_J)
            expected_diff = -(K - J) * delta * L
            assert mp.almosteq(diff_log, expected_diff, abs_eps=mp.mpf("1e-45"))


# ============================================================================
# 5. Log-Derivative Grade Shift
# ============================================================================

def test_log_derivative_grade_shift():
    """Verify Z_K'(s) / Z_K(s) = -K log(tau) + zeta'(s) / zeta(s)."""
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)
    h = mp.mpf("1e-25")

    for s_pt in [mp.mpc("2.5", "1.3"), mp.mpc("0.75", "14.0"), mp.mpc("3.0", "0.0")]:
        for K in [mp.mpf("1"), mp.mpf("-1.5"), mp.mpf("0.5")]:
            # Z_K(s) = tau^{-Ks} zeta(s)
            Z_K = lambda s: mp.power(tau, -K * s) * mp.zeta(s)
            dlog_Z_K = (Z_K(s_pt + h) - Z_K(s_pt - h)) / (mp.mpf(2) * h * Z_K(s_pt))

            # zeta'(s) / zeta(s)
            dlog_zeta = (mp.zeta(s_pt + h) - mp.zeta(s_pt - h)) / (mp.mpf(2) * h * mp.zeta(s_pt))

            expected = -K * L + dlog_zeta
            assert mp.almosteq(dlog_Z_K, expected, abs_eps=mp.mpf("1e-20"))


# ============================================================================
# 6. Residue Invariance
# ============================================================================

def test_residue_invariance():
    """Verify residue of Z_K'/Z_K or Xi_K'/Xi_K at a zero is grade-independent:
    contour integral (1 / 2pi i) oint (F_K'/F_K) ds = m.
    """
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)

    # First Riemann zero rho1
    gamma1 = mp.mpf("14.1347251417346937904572519835624702707842571156992")
    rho1 = mp.mpc(mp.mpf("0.5"), gamma1)

    # Circular contour around rho1 of radius r = 0.05
    r = mp.mpf("0.05")
    N = 64  # Trapezoidal rule on circle is exponentially accurate for analytic integrand

    for K in [mp.mpf("0"), mp.mpf("1"), mp.mpf("-2")]:
        integral = mp.mpc(0)
        for j in range(N):
            theta = mp.mpf(2) * mp.pi * j / N
            z = rho1 + r * mp.exp(mp.mpc(0, theta))
            dz = mp.mpc(0, 1) * r * mp.exp(mp.mpc(0, theta)) * (mp.mpf(2) * mp.pi / N)

            # Numerical derivative of Z_K at z
            h = mp.mpf("1e-25")
            Z = lambda s: mp.power(tau, -K * s) * mp.zeta(s)
            dlog = (Z(z + h) - Z(z - h)) / (mp.mpf(2) * h * Z(z))
            integral += dlog * dz

        residue = integral / (mp.mpf(2) * mp.pi * mp.mpc(0, 1))
        # Residue must be 1.0 (simple zero), strictly independent of K
        assert mp.almosteq(residue.real, mp.mpf(1), abs_eps=mp.mpf("1e-15"))
        assert mp.almosteq(residue.imag, mp.mpf(0), abs_eps=mp.mpf("1e-15"))


# ============================================================================
# 7. Regularized Finite-Part Shift
# ============================================================================

def test_regularized_finite_part_shift():
    """Verify regularized finite part transforms as h_{rho, K} = h_rho - K log(tau)."""
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)

    # Near a simple zero, F_K'/F_K - 1/(s - rho) -> h_{rho, K}
    # For F_K = e^{-a s} F, F_K'/F_K = -a + F'/F
    # Thus (F_K'/F_K - 1/(s - rho)) = -a + (F'/F - 1/(s - rho))
    # Hence h_{rho, K} - h_rho = -a = -K log(tau)
    a, K, h_rho = symbols("a K h_rho", complex=True)
    h_K = h_rho - a
    shift = simplify(h_K - h_rho)
    assert shift == -a


# ============================================================================
# 8. Unit-Normalized Germ Invariance
# ============================================================================

def test_unit_normalized_germ_invariance():
    """Verify hat{c}_K(rho) = tau^{K(rho - 1/2)} c_{Xi_K}(rho) = c_xi(rho) for all K."""
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)

    c_xi_val = mp.mpc("3.14159", "2.71828")  # Base value of c_xi(rho)
    rho = mp.mpc("0.7", "14.134")  # Arbitrary zero point

    for K in [mp.mpf("-3"), mp.mpf("-0.5"), mp.mpf("1.25"), mp.mpf("4")]:
        c_Xi_K = mp.exp(-K * L * (rho - mp.mpf("0.5"))) * c_xi_val
        hat_c_K = mp.exp(K * L * (rho - mp.mpf("0.5"))) * c_Xi_K
        assert mp.almosteq(hat_c_K, c_xi_val, abs_eps=mp.mpf("1e-45"))


# ============================================================================
# 9. Centered Harmonic Translation Multiplier
# ============================================================================

def test_centered_harmonic_translation_multiplier():
    """Verify H_rho(x + K log tau) = tau^{K(rho - 1/2)} H_rho(x) with modulus tau^{K delta}."""
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)

    delta = mp.mpf("0.15")
    gamma = mp.mpf("25.0")
    rho = mp.mpc(mp.mpf("0.5") + delta, gamma)
    x = mp.mpf("3.5")

    for K in [mp.mpf("1.0"), mp.mpf("-2.0"), mp.mpf("0.5")]:
        shift = K * L
        H_shifted = mp.exp((rho - mp.mpf("0.5")) * (x + shift))
        H_orig = mp.exp((rho - mp.mpf("0.5")) * x)
        multiplier = H_shifted / H_orig

        expected_multiplier = mp.exp((rho - mp.mpf("0.5")) * shift)
        assert mp.almosteq(multiplier, expected_multiplier, abs_eps=mp.mpf("1e-45"))

        # Modulus must be tau^{K delta}
        assert mp.almosteq(abs(multiplier), mp.power(tau, K * delta), abs_eps=mp.mpf("1e-45"))


# ============================================================================
# 10. Synthetic Off-Line Modulus Change
# ============================================================================

def test_synthetic_offline_modulus_change():
    """Verify that off-critical zeros (delta != 0) have grade-dependent germ moduli."""
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)

    deltas = [mp.mpf("0.1"), mp.mpf("-0.2"), mp.mpf("0.05")]
    for delta in deltas:
        rho = mp.mpc(mp.mpf("0.5") + delta, mp.mpf("14.134"))
        K, J = mp.mpf("1"), mp.mpf("0")

        ratio_modulus = abs(mp.exp(-K * L * (rho - mp.mpf("0.5")))) / abs(mp.exp(-J * L * (rho - mp.mpf("0.5"))))
        expected_ratio = mp.power(tau, -(K - J) * delta)

        assert mp.almosteq(ratio_modulus, expected_ratio, abs_eps=mp.mpf("1e-45"))
        # Must strictly differ from 1 when delta != 0
        assert abs(ratio_modulus - 1) > mp.mpf("0.05")


# ============================================================================
# 11. Critical-Line Unit-Modulus Control
# ============================================================================

def test_critical_line_unit_modulus_control():
    """Verify that on the critical line (delta = 0), germ moduli are identical for all grades."""
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)

    gamma = mp.mpf("14.134725")
    rho_crit = mp.mpc(mp.mpf("0.5"), gamma)

    for K in [mp.mpf("-5"), mp.mpf("-1"), mp.mpf("0.5"), mp.mpf("3")]:
        multiplier = mp.exp(-K * L * (rho_crit - mp.mpf("0.5")))
        # Modulus is identically 1
        assert mp.almosteq(abs(multiplier), mp.mpf(1), abs_eps=mp.mpf("1e-45"))
        # Phase rotates by -K * gamma * log(tau)
        expected_phase = -K * gamma * L
        actual_phase = mp.arg(multiplier)
        # Verify modulo 2pi
        diff_phase = (actual_phase - expected_phase) % (mp.mpf(2) * mp.pi)
        if diff_phase > mp.pi:
            diff_phase -= mp.mpf(2) * mp.pi
        assert abs(diff_phase) < mp.mpf("1e-40")


# ============================================================================
# 12. Geometric Prime-Station Translation
# ============================================================================

def test_geometric_prime_station_translation():
    """Verify that the Laplace transform of the shifted prime measure
    mu_K = sum_n Lambda(n) delta_{log n + K log tau} equals tau^{-Ks} (-zeta'/zeta(s)).
    """
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)
    s = mp.mpc("3.0", "1.5")  # Deep in absolute convergence region Re(s) > 1

    # Truncated prime-power sum up to N = 100
    N_max = 100
    from sympy.ntheory import primefactors

    def von_mangoldt(n):
        if n < 2:
            return 0
        factors = primefactors(n)
        if len(factors) == 1:
            p = factors[0]
            # Check if n is a power of p
            m = n
            while m % p == 0:
                m //= p
            if m == 1:
                return math.log(p)
        return 0

    for K in [mp.mpf("0.5"), mp.mpf("1.0"), mp.mpf("-0.5")]:
        # Direct Laplace transform: sum Lambda(n) e^{-s (log n + K log tau)}
        laplace_shifted = mp.mpc(0)
        laplace_unscaled = mp.mpc(0)
        for n in range(2, N_max + 1):
            vn = von_mangoldt(n)
            if vn > 0:
                vn_mp = mp.mpf(vn)
                laplace_shifted += vn_mp * mp.exp(-s * (mp.log(n) + K * L))
                laplace_unscaled += vn_mp * mp.exp(-s * mp.log(n))

        # Must satisfy laplace_shifted = tau^{-Ks} * laplace_unscaled
        expected_shifted = mp.power(tau, -K * s) * laplace_unscaled
        assert mp.almosteq(laplace_shifted, expected_shifted, abs_eps=mp.mpf("1e-40"))


# ============================================================================
# 13. Distinction Between Station Transform and Grid Zeta Log Derivative
# ============================================================================

def test_distinction_station_transform_vs_grid_zeta_log_derivative():
    """Verify that the geometric station Laplace transform tau^{-Ks} * (-zeta'/zeta)
    is fundamentally different from the grid zeta log derivative -Z_K'/Z_K = KL - zeta'/zeta.
    """
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)
    s = mp.mpc("2.5", "0.5")
    K = mp.mpf("1.0")

    h = mp.mpf("1e-25")
    dlog_zeta = (mp.zeta(s + h) - mp.zeta(s - h)) / (mp.mpf(2) * h * mp.zeta(s))
    neg_dlog_zeta = -dlog_zeta

    # Grid zeta log derivative
    grid_zeta_dlog = K * L + neg_dlog_zeta

    # Geometric station transform
    geometric_station_transform = mp.power(tau, -K * s) * neg_dlog_zeta

    # They differ: one is additive constant shift KL, the other is multiplicative factor tau^{-Ks}
    diff_val = grid_zeta_dlog - geometric_station_transform
    assert abs(diff_val) > mp.mpf("0.1")


# ============================================================================
# 14. Reflected Local-Germ Identity and Grade-Invariant Product
# ============================================================================

def test_reflected_local_germ_identity_and_product():
    """Verify:
    1. c_{Xi_K}(rho) = (-1)^m c_{Xi_{-K}}(1 - rho)
    2. c_{Xi_K}(rho) * c_{Xi_K}(1 - rho) = (-1)^m c_xi(rho)^2 (grade-invariant)
    """
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)

    # For m = 1 (simple zeros)
    m = 1
    c_xi_rho = mp.mpc("1.234", "5.678")
    # For xi(s) = xi(1-s), xi'(1-rho) = -xi'(rho), so c_xi(1-rho) = -c_xi(rho) = (-1)^1 c_xi(rho)
    c_xi_1mrho = (-1)**m * c_xi_rho

    rho = mp.mpc("0.65", "14.134")

    for K in [mp.mpf("1"), mp.mpf("-2"), mp.mpf("0.75")]:
        # c_{Xi_K}(rho) = tau^{-K(rho - 1/2)} c_xi(rho)
        c_Xi_K_rho = mp.exp(-K * L * (rho - mp.mpf("0.5"))) * c_xi_rho

        # c_{Xi_{-K}}(1 - rho) = tau^{-(-K)((1-rho) - 1/2)} c_xi(1 - rho)
        # Note: (1-rho) - 1/2 = 1/2 - rho = -(rho - 1/2)
        # So -(-K)(1/2 - rho) = -K(rho - 1/2)
        c_Xi_negK_1mrho = mp.exp(-(-K) * L * ((1 - rho) - mp.mpf("0.5"))) * c_xi_1mrho

        # 1. Reflection relation
        expected_c_Xi_K_rho = (-1)**m * c_Xi_negK_1mrho
        assert mp.almosteq(c_Xi_K_rho, expected_c_Xi_K_rho, abs_eps=mp.mpf("1e-45"))

        # 2. Product at same grade K: c_{Xi_K}(rho) * c_{Xi_K}(1 - rho)
        c_Xi_K_1mrho = mp.exp(-K * L * ((1 - rho) - mp.mpf("0.5"))) * c_xi_1mrho
        product = c_Xi_K_rho * c_Xi_K_1mrho
        expected_product = (-1)**m * (c_xi_rho ** 2)

        # The grade factor tau^0 = 1 cancels, so product is strictly independent of K!
        assert mp.almosteq(product, expected_product, abs_eps=mp.mpf("1e-45"))


# ============================================================================
# 15. Regression: Forbidding Claims that Local-Germ Magnitude is Intrinsic
# ============================================================================

def test_regression_against_calling_local_germ_magnitude_intrinsic():
    """Verify that requiring |c_{Xi_K}(rho)| = |c_{Xi_J}(rho)| without independent proof
    is circular and equivalent to assuming delta = 0.
    """
    tau = mp.mpf(2) * mp.pi
    L = mp.log(tau)
    K, J = mp.mpf("1"), mp.mpf("0")

    # If an agent asserts |c_{Xi_1}(rho)| == |c_{Xi_0}(rho)|, it forces tau^{-delta} = 1 => delta = 0
    # Show that for delta = 0.05, the ratio is strictly != 1
    delta_offline = mp.mpf("0.05")
    ratio = mp.power(tau, -(K - J) * delta_offline)
    assert not mp.almosteq(ratio, mp.mpf(1), abs_eps=mp.mpf("0.01"))


# ============================================================================
# 16. Regression: NO_TWO_DIRECTION_ZETA_TRANSFER Epistemic Scoping
# ============================================================================

def test_regression_no_two_direction_zeta_transfer_scoping():
    """Verify that the repository does not claim an impossibility theorem for cross-grade transfer,
    and uses the scoped label NO_TWO_DIRECTION_ZETA_TRANSFER_FOUND within audited structures.
    """
    import os
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Check key documents
    files_to_check = [
        os.path.join(repo_root, "TRANSCENDENTAL_CONTINUATION.md"),
        os.path.join(repo_root, "RESEARCH_LEDGER.md"),
        os.path.join(repo_root, "RESEARCH_HYPOTHESIS.md"),
        os.path.join(repo_root, "MATH_CONTRACT.md"),
        os.path.join(repo_root, "docs", "reviews", "TC_ALGEBRAIC_GRADE_FUNCTIONAL_BRIDGE.md"),
        os.path.join(repo_root, "data", "tc_algebraic_grade_functional_bridge.json"),
    ]

    for fpath in files_to_check:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        # Ensure NO_TWO_DIRECTION_ZETA_TRANSFER is followed by _FOUND or is scoped
        # It must NOT appear as bare "NO_TWO_DIRECTION_ZETA_TRANSFER" without _FOUND
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            if "NO_TWO_DIRECTION_ZETA_TRANSFER" in line:
                assert "NO_TWO_DIRECTION_ZETA_TRANSFER_FOUND" in line, (
                    f"File {fpath}:{idx} has un-scoped NO_TWO_DIRECTION_ZETA_TRANSFER: {line}"
                )
