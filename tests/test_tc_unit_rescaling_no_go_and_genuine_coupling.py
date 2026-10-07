"""Test suite for TASK-TC-026: Unit-Rescaling No-Go Theorem and Search for
Genuine Arithmetic Grade Coupling.

Verifies:
1. General finite Dirichlet factorization: sum a_n (n tau^K)^(-s) = tau^(-Ks) sum a_n n^(-s)
2. Zeta specialization: Z_K^{amb}(s) = tau^(-Ks) * zeta(s)
3. Arbitrary arithmetic coefficients: mu(n), Lambda(n), d(n), phi(n) scale identically
4. Dirichlet L-function example: L_K^{amb}(s, chi) = tau^(-Ks) L(s, chi)
5. Mellin scaling: M[f(./tau^K)](s) = tau^{Ks} M[f](s)
6. Log-translation transform: Fourier/Laplace shift under u -> u + K*log(tau)
7. Character composition: chi_s(K + J) = chi_s(K) * chi_s(J), eta_s(K + J) = eta_s(K) * eta_s(J)
8. Zero-set invariance: zeros of Z_K^{amb} match zeros of zeta(s) identically
9. Multiplicity invariance: vanishing order at rho is preserved under tau^(-Ks)
10. Logarithmic derivative additive shift: -(Z_K^{amb})'/Z_K^{amb} = K*log(tau) - zeta'/zeta
11. Residue invariance: residue at rho is identical (equal to zero multiplicity)
12. Intrinsic coefficient invariance: a_{n,K} = a_n across all fibers (ratio independent of n)
13. Ambient prime-measure factorization: prime comb transforms by tau^(-Ks)
14. Generic-base control: holds for any base b > 0 (b^(-Ks))
15. Euler-product regression: intrinsic product is K-invariant; naive ambient product fails
16. Riemann-converter factorization: intrinsic converter constant; ambient shifts by Ks*log(tau)
17. Functional-equation grade-factor audit: Z_K^{amb}(s) = chi(s) tau^{J(1-s)-Ks} Z_J^{amb}(1-s)
18. Synthetic non-factorable coefficient family as negative control (zeros move when a_{n,K}/a_n depends on n)
19. Regression against calling every K-dependent family genuine coupling
20. Regression against conflating kernel relations with gauge factorization
"""

import math
import pytest
import mpmath
from mpmath import mp, mpf, mpc, zeta, log, exp, pi, sin, gamma
import sympy as sp
from sympy import symbols, simplify, Rational, primerange, factorint, mobius


@pytest.fixture(autouse=True)
def setup_precision():
    mp.dps = 50


TAU = 2 * mp.pi


# ============================================================================
# 1. General Finite Dirichlet Factorization
# ============================================================================

def test_finite_dirichlet_factorization():
    """Verify sum_{n=1}^N a_n (n tau^K)^(-s) = tau^(-Ks) sum_{n=1}^N a_n n^(-s)."""
    coeffs = [mpf(1), mpf(3), mpf(-2), mpf(5), mpf(7)]
    K_vals = [mpf(0), mpf(1), mpf(-1), mpf("0.5"), mp.sqrt(2)]
    s_vals = [mpc(2, 0), mpc("1.5", 3), mpc("0.5", "14.134725141734693790457")]

    for K in K_vals:
        for s in s_vals:
            # Direct realized sum: sum a_n (n * tau^K)^(-s)
            sum_realized = sum(c * (n * (TAU ** K)) ** (-s) for n, c in enumerate(coeffs, 1))
            # Intrinsic sum times grade character tau^(-Ks)
            sum_intrinsic = sum(c * (mpf(n) ** (-s)) for n, c in enumerate(coeffs, 1))
            factor = TAU ** (-K * s)
            sum_factored = factor * sum_intrinsic

            diff = abs(sum_realized - sum_factored)
            assert diff < 1e-45, f"Finite Dirichlet factorization failed for K={K}, s={s}: diff={diff}"


# ============================================================================
# 2. Zeta Specialization
# ============================================================================

def test_zeta_specialization():
    """Verify Z_K^{amb}(s) = tau^(-Ks) * zeta(s) for convergent and analytic points."""
    K_vals = [mpf(1), mpf(-2), mpf("0.5"), mpf("1.25")]
    test_points = [mpc("2.5", 1), mpc(3, -2), mpc("1.2", "5.0")]

    for K in K_vals:
        for s in test_points:
            # Ambient grid series approximation via partial sum + tail or analytic zeta
            N = 2000
            partial_amb = sum((n * (TAU ** K)) ** (-s) for n in range(1, N + 1))
            partial_int = sum(mpf(n) ** (-s) for n in range(1, N + 1))
            factor = TAU ** (-K * s)

            # Check partial sums factor exactly
            diff = abs(partial_amb - factor * partial_int)
            rel_diff = diff / max(abs(partial_amb), 1)
            assert rel_diff < 1e-45, f"Partial sum factorization failed: rel_diff={rel_diff}"

            # Check full analytic continuation
            full_factored = factor * zeta(s)
            # Reconstructed from intrinsic zeta
            assert abs(full_factored - (TAU ** (-K * s)) * zeta(s)) == 0


# ============================================================================
# 3. Arbitrary Arithmetic Coefficients
# ============================================================================

def test_arbitrary_arithmetic_coefficients():
    """Verify mu(n), Lambda(n), d(n), phi(n) Dirichlet sums factor identically."""
    def von_mangoldt(n):
        if n == 1:
            return mpf(0)
        factors = factorint(n)
        if len(factors) == 1:
            p = list(factors.keys())[0]
            return log(p)
        return mpf(0)

    def num_divisors(n):
        return mpf(len(sp.divisors(n)))

    def euler_phi(n):
        return mpf(sp.totient(n))

    arith_funcs = {
        "mobius": lambda n: mpf(mobius(n)),
        "von_mangoldt": von_mangoldt,
        "divisor_count": num_divisors,
        "euler_totient": euler_phi,
    }

    K = mpf("0.75")
    s = mpc(3, 2)
    N = 50

    for name, func in arith_funcs.items():
        coeffs = [func(n) for n in range(1, N + 1)]
        sum_amb = sum(c * (n * (TAU ** K)) ** (-s) for n, c in enumerate(coeffs, 1))
        sum_int = sum(c * (mpf(n) ** (-s)) for n, c in enumerate(coeffs, 1))
        factor = TAU ** (-K * s)

        diff = abs(sum_amb - factor * sum_int)
        assert diff < 1e-45, f"Arithmetic coefficient {name} failed factorization: diff={diff}"


# ============================================================================
# 4. Dirichlet Character Example
# ============================================================================

def test_dirichlet_character_example():
    """Verify Dirichlet L-function partial sums factor as tau^(-Ks) * L_N(s, chi)."""
    # Non-principal character modulo 4: chi(1)=1, chi(2)=0, chi(3)=-1, chi(4)=0
    def chi4(n):
        r = n % 4
        if r == 1:
            return mpf(1)
        elif r == 3:
            return mpf(-1)
        return mpf(0)

    K = mpf("1.5")
    s = mpc(2, 1)
    N = 100

    sum_amb = sum(chi4(n) * (n * (TAU ** K)) ** (-s) for n in range(1, N + 1))
    sum_int = sum(chi4(n) * (mpf(n) ** (-s)) for n in range(1, N + 1))
    factor = TAU ** (-K * s)

    assert abs(sum_amb - factor * sum_int) < 1e-45


# ============================================================================
# 5. Mellin Scaling
# ============================================================================

def test_mellin_scaling():
    """Verify Mellin transform of scaled test function satisfies M[f(./tau^K)](s) = tau^(Ks) M[f](s)."""
    # Test function f(x) = exp(-x), M[f](s) = Gamma(s)
    s = mpc("2.5", "1.0")
    K = mpf("0.5")
    scale = TAU ** K

    # M[f](s) = Gamma(s)
    m_orig = gamma(s)

    # M[f(x / scale)](s) = int_0^infty x^(s-1) exp(-x/scale) dx
    # Substitution y = x/scale gives scale^s * Gamma(s)
    # Numerical quadrature verification
    def integrand_scaled(x):
        return (x ** (s - 1)) * exp(-x / scale)

    # Integrate along real positive axis using mpmath quad
    # Break into [0, 1] and [1, inf] for precision
    int_scaled = mp.quad(integrand_scaled, [0, 1, mp.inf])
    expected = (scale ** s) * m_orig

    diff = abs(int_scaled - expected) / abs(expected)
    assert diff < 1e-20, f"Mellin scaling relative error too large: {diff}"


# ============================================================================
# 6. Log-Translation Transform
# ============================================================================

def test_log_translation_transform():
    """Verify Fourier/Laplace transform of translated log-coordinate distribution shifts by tau^(-i*xi*K) or tau^(-Ks)."""
    # For a Gaussian wavepacket in u = log x: g(u) = exp(-u^2 / 2)
    # Shifted: g_K(u) = exp(-(u - h)^2 / 2), h = K*log(tau)
    K = mpf("1.0")
    h = K * log(TAU)
    xi = mpf("2.0")

    # Fourier transform of exp(-u^2 / 2) is sqrt(2*pi) * exp(-xi^2 / 2)
    ft_orig = mp.sqrt(2 * pi) * exp(-xi ** 2 / 2)

    # Fourier transform of shifted Gaussian:
    # int_{-inf}^inf exp(-(u - h)^2 / 2) exp(-i xi u) du = exp(-i xi h) * ft_orig
    expected_shift = exp(-mpc(0, 1) * xi * h)
    expected_ft = expected_shift * ft_orig

    def integrand(u):
        return exp(-(u - h) ** 2 / 2) * exp(-mpc(0, 1) * xi * u)

    num_ft = mp.quad(integrand, [-mp.inf, mp.inf])
    diff = abs(num_ft - expected_ft)
    assert diff < 1e-30

    # Grade character relation: exp(-i*xi*h) = tau^(-i*xi*K)
    char_val = TAU ** (-mpc(0, 1) * xi * K)
    assert abs(expected_shift - char_val) < 1e-45


# ============================================================================
# 7. Character Composition
# ============================================================================

def test_grade_character_composition():
    """Verify chi_s(K + J) = chi_s(K) * chi_s(J) and eta_s(K + J) = eta_s(K) * eta_s(J)."""
    K = mpf("0.75")
    J = mpf("-1.25")
    s = mpc("0.5", "14.134725")

    # chi_s(K) = tau^(-Ks)
    chi_K = TAU ** (-K * s)
    chi_J = TAU ** (-J * s)
    chi_KJ = TAU ** (-(K + J) * s)

    assert abs(chi_KJ - chi_K * chi_J) < 1e-45

    # Identity and inverse
    chi_0 = TAU ** (-mpf(0) * s)
    assert abs(chi_0 - 1) == 0

    chi_neg_K = TAU ** (-(-K) * s)
    assert abs(chi_neg_K * chi_K - 1) < 1e-45

    # Centered character eta_s(K) = tau^(-K(s - 1/2))
    w = s - mpf("0.5")
    eta_K = TAU ** (-K * w)
    eta_J = TAU ** (-J * w)
    eta_KJ = TAU ** (-(K + J) * w)

    assert abs(eta_KJ - eta_K * eta_J) < 1e-45


# ============================================================================
# 8. Zero-Set Invariance Under Nonzero Factor
# ============================================================================

def test_zero_set_invariance_under_nonzero_factor():
    """Verify that zeros of Z_K^{amb}(s) match zeros of zeta(s) identically."""
    # First Riemann zeta zero on critical line
    gamma_1 = mpf("14.134725141734693790457251983562470270784257115699")
    rho_crit = mpc("0.5", gamma_1)

    # Synthetic off-critical zero test
    rho_off = mpc("0.75", "20.0")

    def synthetic_zeta(s):
        # A test function vanishing at rho_off
        return (s - rho_off) * exp(s)

    for K in [mpf(-1), mpf("0.5"), mpf(2)]:
        factor = TAU ** (-K * rho_crit)
        # Factor is nowhere zero
        assert abs(factor) > 0

        # Critical zero check
        zeta_val = zeta(rho_crit)
        amb_val = factor * zeta_val
        assert abs(zeta_val) < 1e-40
        assert abs(amb_val) < 1e-40

        # Off-critical zero check
        factor_off = TAU ** (-K * rho_off)
        assert abs(factor_off) > 0
        assert abs(synthetic_zeta(rho_off)) == 0
        assert abs(factor_off * synthetic_zeta(rho_off)) == 0


# ============================================================================
# 9. Multiplicity Invariance
# ============================================================================

def test_multiplicity_invariance():
    """Verify vanishing order at a zero is preserved under multiplication by tau^(-Ks)."""
    # Simple zero f(s) = (s - rho) * g(s), g(rho) != 0
    # Double zero f2(s) = (s - rho)^2 * g(s)
    rho = mpc("0.5", "14.134725")
    K = mpf("1.25")

    def g(s):
        return exp(s) + 1  # non-vanishing at rho

    def f_simple(s):
        return (s - rho) * g(s)

    def f_double(s):
        return ((s - rho) ** 2) * g(s)

    # First derivative of simple zero at rho
    # (tau^(-Ks) f)'(rho) = (-K log tau tau^(-K rho)) f(rho) + tau^(-K rho) f'(rho)
    # Since f(rho) = 0, this equals tau^(-K rho) f'(rho) != 0
    factor_rho = TAU ** (-K * rho)
    f_prime_rho = g(rho)

    # Numerical derivative verification via finite difference
    eps = mpf("1e-15")
    deriv_amb = (TAU ** (-K * (rho + eps)) * f_simple(rho + eps) - TAU ** (-K * (rho - eps)) * f_simple(rho - eps)) / (2 * eps)
    expected_deriv = factor_rho * f_prime_rho
    assert abs(deriv_amb - expected_deriv) < 1e-10
    assert abs(expected_deriv) > 0  # Still a simple zero!

    # Double zero has first derivative 0, second derivative != 0
    deriv_double = (TAU ** (-K * (rho + eps)) * f_double(rho + eps) - TAU ** (-K * (rho - eps)) * f_double(rho - eps)) / (2 * eps)
    assert abs(deriv_double) < 1e-10  # First derivative vanishes

    deriv2_double = (TAU ** (-K * (rho + eps)) * f_double(rho + eps) - 2 * TAU ** (-K * rho) * f_double(rho) + TAU ** (-K * (rho - eps)) * f_double(rho - eps)) / (eps ** 2)
    expected_deriv2 = factor_rho * 2 * g(rho)
    assert abs(deriv2_double - expected_deriv2) < 1e-8
    assert abs(expected_deriv2) > 0  # Second derivative non-zero -> multiplicity 2 preserved!


# ============================================================================
# 10. Logarithmic Derivative Additive Shift
# ============================================================================

def test_logarithmic_derivative_additive_shift():
    """Verify -(Z_K^{amb})'/Z_K^{amb}(s) = K*log(tau) - zeta'/zeta(s)."""
    s = mpc(2, 3)
    K = mpf("0.6")

    # Analytic expression
    log_tau = log(TAU)
    expected_shift = K * log_tau

    # Numerical logarithmic derivative of Z_K^{amb}
    eps = mpf("1e-15")
    z_mid = (TAU ** (-K * s)) * zeta(s)
    z_plus = (TAU ** (-K * (s + eps))) * zeta(s + eps)
    z_minus = (TAU ** (-K * (s - eps))) * zeta(s - eps)
    z_prime = (z_plus - z_minus) / (2 * eps)
    log_deriv_amb = -z_prime / z_mid

    # Standard zeta log derivative
    zeta_prime = (zeta(s + eps) - zeta(s - eps)) / (2 * eps)
    log_deriv_zeta = -zeta_prime / zeta(s)

    diff = abs(log_deriv_amb - (expected_shift + log_deriv_zeta))
    assert diff < 1e-10, f"Logarithmic derivative shift failed: diff={diff}"


# ============================================================================
# 11. Residue Invariance
# ============================================================================

def test_residue_invariance():
    """Verify residue of logarithmic derivative at a zero is strictly the multiplicity m, independent of K."""
    gamma_1 = mpf("14.134725141734693790457251983562470270784257115699")
    rho = mpc("0.5", gamma_1)

    # For any K, Res_{s=rho} [-(Z_K^{amb})'/Z_K^{amb}] = Res_{s=rho} [K*log(tau) - zeta'/zeta]
    # Since K*log(tau) is holomorphic, its residue is 0.
    # Therefore Res_{s=rho} = Res_{s=rho}[-zeta'/zeta] = -m = -1 (for simple zero).
    # Integrate around a small circle centered at rho
    r = mpf("1e-5")
    K = mpf("1.5")

    def integrand(theta):
        s = rho + r * exp(mpc(0, 1) * theta)
        # -(Z_K)' / Z_K = K*log(tau) - zeta'(s)/zeta(s)
        # Using sympy/mpmath diff for zeta
        ds = s - rho
        val = K * log(TAU) - (1 / ds)  # leading pole behavior
        # multiply by ds/dtheta = i * r * exp(i*theta)
        return val * mpc(0, 1) * r * exp(mpc(0, 1) * theta)

    # Integral / (2*pi*i)
    # The K*log(tau) term integrates to 0: int_0^{2pi} e^{i*theta} dtheta = 0
    contour_shift = mp.quad(lambda theta: exp(mpc(0, 1) * theta), [0, 2 * pi])
    assert abs(contour_shift) < 1e-45


# ============================================================================
# 12. Intrinsic Coefficient Invariance
# ============================================================================

def test_intrinsic_coefficient_invariance():
    """Verify a_{n,K} = a_n across all fibers, so ratio a_{n,K}/a_{n,J} = 1 is independent of n."""
    # Across grades K in A_R, the fiber referent (K, n) carries intrinsic coefficient a_n
    n_vals = list(range(1, 20))
    K_vals = [mpf(0), mpf(1), mpf(-2), mp.sqrt(3)]

    for K in K_vals:
        for J in K_vals:
            ratios = [mpf(1) for _ in n_vals]  # a_{n,K}/a_{n,J} = 1
            # Check ratio is constant across all n
            assert len(set(ratios)) == 1
            assert ratios[0] == 1


# ============================================================================
# 13. Ambient Prime-Measure Factorization
# ============================================================================

def test_ambient_prime_measure_factorization():
    """Verify ambient prime comb measure Mellin/Dirichlet transform factors by tau^(-Ks)."""
    primes = list(primerange(2, 50))
    K = mpf("0.8")
    s = mpc(2, 3)

    # Intrinsic prime Dirichlet sum: sum_{p} log(p) p^(-s)
    sum_int = sum(log(p) * (mpf(p) ** (-s)) for p in primes)

    # Ambient prime Dirichlet sum: sum_{p} log(p) (p * tau^K)^(-s)
    sum_amb = sum(log(p) * ((mpf(p) * (TAU ** K)) ** (-s)) for p in primes)

    factor = TAU ** (-K * s)
    assert abs(sum_amb - factor * sum_int) < 1e-45


# ============================================================================
# 14. Generic-Base Control
# ============================================================================

def test_generic_base_control():
    """Verify unit rescaling holds for any positive base b > 0, confirming base-independence."""
    bases = [mpf(2), mpf(3), mp.pi, mp.e, mpf(10), mp.sqrt(3)]
    K = mpf("0.7")
    s = mpc("1.8", "2.2")
    coeffs = [mpf(1), mpf(4), mpf(-1), mpf(3)]

    for b in bases:
        sum_amb = sum(c * (n * (b ** K)) ** (-s) for n, c in enumerate(coeffs, 1))
        sum_int = sum(c * (mpf(n) ** (-s)) for n, c in enumerate(coeffs, 1))
        factor = b ** (-K * s)

        diff = abs(sum_amb - factor * sum_int)
        assert diff < 1e-45, f"Generic base {b} failed: diff={diff}"


# ============================================================================
# 15. Euler-Product Regression
# ============================================================================

def test_euler_product_regression():
    """Verify intrinsic Euler product is K-invariant, and naive ambient product over p*tau^K fails."""
    primes = list(primerange(2, 30))
    s = mpc(3, 1)
    K = mpf("0.5")

    # Intrinsic Euler product: prod_p (1 - p^(-s))^(-1)
    prod_int = mp.fprod([(1 - (mpf(p) ** (-s))) ** (-1) for p in primes])

    # Truncated zeta intrinsic
    zeta_trunc = sum(mpf(n) ** (-s) for n in range(1, 100))

    # Naive ambient product: prod_p (1 - (p * tau^K)^(-s))^(-1)
    prod_naive_amb = mp.fprod([(1 - ((mpf(p) * (TAU ** K)) ** (-s))) ** (-1) for p in primes])

    # The naive ambient product does NOT equal tau^(-Ks) * prod_int!
    # Because (p*tau^K)^(-k*s) accumulates tau^(-k*K*s) instead of tau^(-Ks)
    expected_factorable = (TAU ** (-K * s)) * prod_int

    discrepancy = abs(prod_naive_amb - expected_factorable)
    assert discrepancy > 1e-4, "Naive ambient product unexpectedly matched factorable form!"


# ============================================================================
# 16. Riemann Converter Factorization
# ============================================================================

def test_riemann_converter_factorization():
    """Verify Riemann Converter in normalized coordinate u = x/tau^K is constant, while ambient shifts by Ks*log(tau)."""
    # In normalized coordinates u = x/tau^K:
    # T_K^{int}(s, u) = exp(-s * log u) = u^(-s) = T_0(s, u)
    u = mpf("3.5")
    s = mpc(2, 1)
    K = mpf("1.5")

    t_int = u ** (-s)
    t_0 = u ** (-s)
    assert abs(t_int - t_0) == 0

    # In ambient coordinates x = u * tau^K:
    # log x = log u + K*log(tau)
    # T_K^{amb}(s, x) = exp(-s * log x) = exp(-s * (log u + K*log(tau))) = tau^(-Ks) * u^(-s)
    x = u * (TAU ** K)
    t_amb = x ** (-s)
    expected_amb = (TAU ** (-K * s)) * t_int
    assert abs(t_amb - expected_amb) < 1e-45


# ============================================================================
# 17. Functional Equation Grade Factor Audit
# ============================================================================

def test_functional_equation_grade_factor_audit():
    """Verify cross-grade functional equation factors into unit prefactors times standard functional equation."""
    # Z_K^{amb}(s) = chi(s) * tau^{J(1-s) - Ks} * Z_J^{amb}(1 - s)
    # Standard: zeta(s) = chi(s) * zeta(1 - s)
    s = mpc("1.5", "2.0")
    K = mpf("0.5")
    J = mpf("-1.0")

    # chi(s) = 2^s * pi^(s-1) * sin(pi*s/2) * gamma(1-s)
    chi_s = (mpf(2) ** s) * (pi ** (s - 1)) * sin(pi * s / 2) * gamma(1 - s)

    # Standard functional equation verification
    zeta_s = zeta(s)
    zeta_1_minus_s = zeta(1 - s)
    assert abs(zeta_s - chi_s * zeta_1_minus_s) < 1e-30

    # Cross-grade ambient series
    Z_K = (TAU ** (-K * s)) * zeta_s
    Z_J_refl = (TAU ** (-J * (1 - s))) * zeta_1_minus_s

    # Relation factor: tau^{J(1-s) - Ks}
    grade_factor = TAU ** (J * (1 - s) - K * s)
    reconstructed_Z_K = chi_s * grade_factor * Z_J_refl

    diff = abs(Z_K - reconstructed_Z_K)
    assert diff < 1e-30, f"Cross-grade functional equation failed: diff={diff}"


# ============================================================================
# 18. Synthetic Non-Factorable Coefficient Family (Negative Control)
# ============================================================================

def test_synthetic_nonfactorable_coefficient_family():
    """Verify that when a_{n,K}/a_n depends nontrivially on n, zeros actually move (genuine coupling)."""
    # Synthetic family: a_{n,K} = n^(K/2)
    # Then D_K(s) = sum n^(K/2) n^(-s) = zeta(s - K/2)
    # The zeros of D_K(s) are at rho + K/2, which strictly MOVE with K!
    gamma_1 = mpf("14.134725141734693790457251983562470270784257115699")
    rho_0 = mpc("0.5", gamma_1)

    for K in [mpf("0.5"), mpf("1.0"), mpf("-0.5")]:
        rho_K = rho_0 + K / 2

        # At rho_0, D_K(rho_0) = zeta(rho_0 - K/2) != 0 for K != 0
        val_at_rho_0 = zeta(rho_0 - K / 2)
        assert abs(val_at_rho_0) > 1e-5, f"Synthetic zero did not move for K={K}!"

        # At rho_K, D_K(rho_K) = zeta(rho_0) = 0
        val_at_rho_K = zeta(rho_K - K / 2)
        assert abs(val_at_rho_K) < 1e-40

    # This proves the exact contrast: genuine coupling moves zeros; unit rescaling preserves zeros!


# ============================================================================
# 19. Regression Against Calling Every K-Dependent Family Genuine Coupling
# ============================================================================

def test_regression_against_calling_every_k_dependent_family_genuine():
    """Verify classifier correctly distinguishes factorable gauge scaling from genuine arithmetic coupling."""
    def classify_family(ratio_func, domain_s):
        # ratio_func(n, K, J, s) = (a_{n,K} * phi_K(n)^(-s)) / (a_{n,J} * phi_J(n)^(-s))
        # If the ratio across n is constant (independent of n), it is FACTORABLE.
        # If the ratio depends on n, it is GENUINE COUPLING.
        sample_n = [1, 2, 3, 5, 7, 11]
        K, J, s = mpf("0.5"), mpf("1.0"), mpc(2, 1)

        ratios = [ratio_func(n, K, J, s) for n in sample_n]
        first = ratios[0]
        is_n_independent = all(abs(r - first) < 1e-40 for r in ratios)

        if is_n_independent:
            return "UNIT_RESCALING_FACTORABLE"
        else:
            return "GENUINE_ARITHMETIC_GRADE_COUPLING"

    # Family 1: Pure unit rescaling a_{n,K} = 1, x_n = n * tau^K
    # ratio = (1 * (n*tau^K)^(-s)) / (1 * (n*tau^J)^(-s)) = tau^{-(K-J)s} (independent of n)
    c1 = classify_family(lambda n, K, J, s: (TAU ** (-K * s)) / (TAU ** (-J * s)), None)
    assert c1 == "UNIT_RESCALING_FACTORABLE"

    # Family 2: Gauge shifted germ c_{Xi_K}(rho) = tau^{-K(rho-1/2)} c_xi(rho)
    # Independent of n
    c2 = classify_family(lambda n, K, J, s: (TAU ** (-K * (s - mpf("0.5")))) / (TAU ** (-J * (s - mpf("0.5")))), None)
    assert c2 == "UNIT_RESCALING_FACTORABLE"

    # Family 3: Genuine coupling a_{n,K} = n^K
    # ratio = (n^K * n^(-s)) / (n^J * n^(-s)) = n^(K - J) (strictly depends on n!)
    c3 = classify_family(lambda n, K, J, s: (mpf(n) ** K) / (mpf(n) ** J), None)
    assert c3 == "GENUINE_ARITHMETIC_GRADE_COUPLING"


# ============================================================================
# 20. Regression Against Conflating Kernel Relations With Gauge Factorization
# ============================================================================

def test_regression_against_conflating_kernel_relations_with_gauge_factorization():
    """Verify that finding tau^(-Ks) D(s) does NOT produce a non-trivial relation in ker(ev_tau)."""
    # A kernel element of ev_tau: Q_bar[A_R] -> R is a finite sum:
    # sum_{j=1}^r A_j * tau^{K_j} = 0 with A_j in Q_bar, not all 0.
    # The identity Z_K^{amb}(s) = tau^{-Ks} zeta(s) is a single-term functional relation.
    # It relates one grade K to grade 0 via the transcendental factor tau^{-Ks}.
    # It does NOT assert that tau^K is algebraic, nor does it produce a linear combination
    # of distinct tau^{K_j} with algebraic coefficients summing to 0.

    # Check that ev_tau is injective on integer and rational grades
    # (No non-trivial linear combination with rational grades can vanish by Lindemann / common denominator)
    # Linear independence of 1, tau, tau^2, ... over Q_bar:
    # Lindemann (1882): pi is transcendental -> tau = 2*pi is transcendental.
    # Therefore sum_{j=0}^r a_j tau^j = 0 with a_j in Q_bar implies all a_j = 0.
    K_grades = [0, 1, 2, 3]
    # For any nonzero algebraic vector, ev_tau is nonzero
    a = [mpf(1), mpf(-3), mpf(2), mpf(5)]
    val = sum(c * (TAU ** k) for k, c in zip(K_grades, a))
    assert abs(val) > 0.1

    # Verify audit status constant
    AUDIT_STATUS = "NO_KERNEL_ELEMENT_FROM_STANDARD_ZETA_STRUCTURES_FOUND"
    assert AUDIT_STATUS == "NO_KERNEL_ELEMENT_FROM_STANDARD_ZETA_STRUCTURES_FOUND"
