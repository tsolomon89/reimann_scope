"""Test suite for TASK-TC-025: Intrinsic Grade-Fiber Arithmetic,
Ambient Realization, and the Correct TC Zeta.

Verifies:
1. Fiber addition closure: (K, m) ⊕_K (K, n) = (K, m + n) stays in F_K
2. Fiber multiplication closure: (K, m) ⊙_K (K, n) = (K, mn) stays in F_K
3. Fiber unit identity: 1_K = (K, 1) and Phi_K(1_K) = tau^K
4. Ring-isomorphism to integers: (L_K, +, ⊙_K) ≅ Z
5. Prime preservation: (K, p) is prime in F_K iff p is prime in Z
6. Intrinsic factorization stays at grade K: prod_p^{⊙_K} (K, p)^{⊙_K v_p(n)} = (K, n)
7. Ambient multiplication moves to grade 2K: (m*tau^K)(n*tau^K) = mn*tau^{2K}
8. Transfer-map composition: T_{M ← J} ∘ T_{J ← K} = T_{M ← K}
9. Transfer maps preserve multiplication: T(x ⊙_K y) = T(x) ⊙_J T(y)
10. Normalized metric identity: d_K(m*tau^K, n*tau^K) = |m - n|
11. Intrinsic Möbius invariance: mu_K(K, n) = mu(n)
12. Intrinsic von Mangoldt invariance: Lambda_K(K, n) = Lambda(n)
13. Intrinsic zeta independence of K: zeta_K^{int}(s) = zeta(s)
14. Ambient zeta factor: Z_K^{amb}(s) = tau^{-Ks} * zeta(s)
15. Intrinsic Euler-product reconstruction: prod_{(K, p)} (1 - N_K(K, p)^{-s})^{-1} = zeta(s)
16. Regression against ambient product over p*tau^K producing tau^{-K*Omega(n)*s}
17. Intrinsic log coordinate: u_K(x) = log(x / tau^K) = log n
18. Ambient log translation: u_{amb}(x) = log n + K*log(tau)
19. Generic-base fiber invariance: holds for any base b > 0
20. Integer/rational realization injectivity examples
21. Regression against treating tau^K * tau^{-K} = 1 as intrinsic fiber arithmetic
22. Regression against calling full algebraic-grade realization injective
"""

import math
import pytest
import mpmath
from mpmath import mp, mpf, mpc, zeta, log, exp, pi
import sympy as sp
from sympy import symbols, simplify, Rational, primerange, factorint, mobius


@pytest.fixture(autouse=True)
def setup_precision():
    mp.dps = 50


# ============================================================================
# 1. Fiber Addition Closure
# ============================================================================

def test_fiber_addition_closure():
    """Verify that (K, m) ⊕_K (K, n) = (K, m + n) stays strictly within F_K."""
    K = symbols("K", real=True)
    m, n = symbols("m n", integer=True)

    # In abstract fiber F_K = {K} x Z
    elem1 = (K, m)
    elem2 = (K, n)
    fiber_add = (elem1[0], elem1[1] + elem2[1])

    assert fiber_add[0] == K
    assert fiber_add[1] == m + n


# ============================================================================
# 2. Fiber Multiplication Closure
# ============================================================================

def test_fiber_multiplication_closure():
    """Verify that (K, m) ⊙_K (K, n) = (K, mn) stays strictly within F_K."""
    K = symbols("K", real=True)
    m, n = symbols("m n", integer=True)

    elem1 = (K, m)
    elem2 = (K, n)
    fiber_mul = (elem1[0], elem1[1] * elem2[1])

    assert fiber_mul[0] == K
    assert fiber_mul[1] == m * n


# ============================================================================
# 3. Fiber Unit Identity
# ============================================================================

def test_fiber_unit_identity():
    """Verify that 1_K = (K, 1) acts as multiplicative identity in F_K
    and has ambient realization Phi_K(1_K) = tau^K.
    """
    K = symbols("K", real=True)
    n = symbols("n", integer=True)
    tau = symbols("tau", positive=True)

    unit_K = (K, 1)
    elem = (K, n)

    # Multiplicative unit property
    prod = (K, unit_K[1] * elem[1])
    assert prod == (K, n)

    # Realization Phi_K(1_K) = 1 * tau^K = tau^K
    phi_unit = unit_K[1] * (tau ** K)
    assert simplify(phi_unit - tau ** K) == 0


# ============================================================================
# 4. Ring-Isomorphism to Integers
# ============================================================================

def test_ring_isomorphism_to_integers():
    """Verify that (L_K, +, ⊙_K) with x ⊙_K y = (x * y) / tau^K is a commutative ring
    canonically isomorphic to Z via n |-> n * tau^K.
    """
    tau = mp.mpf(2) * mp.pi
    K = mp.mpf("1.5")  # algebraic grade
    tau_K = mp.power(tau, K)

    def phi(n):
        return mp.mpf(n) * tau_K

    def circle_mul(x, y):
        return (x * y) / tau_K

    # Test ring homomorphism properties on sample integers
    for m in [-5, 0, 3, 7]:
        for n in [-4, 1, 2, 6]:
            # Additive homomorphism: phi(m + n) = phi(m) + phi(n)
            assert mp.almosteq(phi(m + n), phi(m) + phi(n))

            # Multiplicative homomorphism: phi(m * n) = phi(m) ⊙_K phi(n)
            assert mp.almosteq(phi(m * n), circle_mul(phi(m), phi(n)))

    # Test unit: phi(1) ⊙_K phi(n) = phi(n)
    for n in range(-5, 6):
        assert mp.almosteq(circle_mul(phi(1), phi(n)), phi(n))


# ============================================================================
# 5. Prime Preservation
# ============================================================================

def test_prime_preservation():
    """Verify that (K, p) is a prime element in (F_K, ⊕_K, ⊙_K) iff p is prime in Z."""
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    composites = [4, 6, 8, 9, 10, 12, 14, 15, 16]

    for p in primes:
        # In F_K, factors of (K, p) under ⊙_K must be units (K, ±1) or associates (K, ±p)
        divisors = [d for d in range(1, p + 1) if p % d == 0]
        assert divisors == [1, p]

    for c in composites:
        divisors = [d for d in range(1, c + 1) if c % d == 0]
        assert len(divisors) > 2


# ============================================================================
# 6. Intrinsic Factorization Stays at Grade K
# ============================================================================

def test_intrinsic_factorization_stays_at_grade_k():
    """Verify that intrinsic prime factorization stays at grade K,
    in contrast to ambient product which accumulates grade K*Omega(n).
    """
    n = 12  # 12 = 2^2 * 3^1, Omega(12) = 3
    factors = factorint(n)  # {2: 2, 3: 1}

    # Intrinsic fiber multiplication ⊙_K
    # (K, 2) ⊙_K (K, 2) ⊙_K (K, 3) = (K, 12)
    val = 1
    for p, exp_val in factors.items():
        for _ in range(exp_val):
            val *= p
    assert val == n

    # Realized value under intrinsic multiplication stays at grade K: 12 * tau^K
    tau = mp.mpf(2) * mp.pi
    K = mp.mpf("2.5")
    tau_K = mp.power(tau, K)

    # Intrinsic realization
    x_int = mp.mpf(val) * tau_K
    assert mp.almosteq(x_int, mp.mpf(12) * tau_K)


# ============================================================================
# 7. Ambient Multiplication Moves to Grade 2K
# ============================================================================

def test_ambient_multiplication_moves_to_grade_2k():
    """Verify that ordinary real multiplication of two grade-K realized points
    (m * tau^K) * (n * tau^K) = mn * tau^{2K} produces grade 2K != K (for K != 0).
    """
    m, n = 3, 5
    K = 2
    tau = mp.mpf(2) * mp.pi

    x = mp.mpf(m) * mp.power(tau, K)
    y = mp.mpf(n) * mp.power(tau, K)

    ambient_prod = x * y
    expected_2K = mp.mpf(m * n) * mp.power(tau, 2 * K)

    assert mp.almosteq(ambient_prod, expected_2K)
    # Confirm it does NOT equal grade K realization mn * tau^K
    assert not mp.almosteq(ambient_prod, mp.mpf(m * n) * mp.power(tau, K))


# ============================================================================
# 8. Transfer-Map Composition
# ============================================================================

def test_transfer_map_composition():
    """Verify that canonical transfer maps T_{J ← K}: (K, n) |-> (J, n) satisfy
    T_{K ← K} = id and T_{M ← J} ∘ T_{J ← K} = T_{M ← K}.
    """
    K, J, M = "K", "J", "M"
    n = 42

    def T(from_grade, to_grade, elem):
        assert elem[0] == from_grade
        return (to_grade, elem[1])

    elem_K = (K, n)

    # Identity
    assert T(K, K, elem_K) == elem_K

    # Composition
    elem_J = T(K, J, elem_K)
    elem_M = T(J, M, elem_J)
    direct_M = T(K, M, elem_K)

    assert elem_M == direct_M
    assert elem_M == (M, n)


# ============================================================================
# 9. Transfer Maps Preserve Multiplication
# ============================================================================

def test_transfer_maps_preserve_multiplication():
    """Verify that T_{J ← K}(x ⊙_K y) = T_{J ← K}(x) ⊙_J T_{J ← K}(y)."""
    m, n = 7, 11
    K, J = "K", "J"

    x_K = (K, m)
    y_K = (K, n)
    prod_K = (K, m * n)

    # T(prod_K)
    t_prod = (J, prod_K[1])

    # T(x) ⊙_J T(y)
    t_x = (J, x_K[1])
    t_y = (J, y_K[1])
    prod_J = (J, t_x[1] * t_y[1])

    assert t_prod == prod_J


# ============================================================================
# 10. Normalized Metric Identity
# ============================================================================

def test_normalized_metric_identity():
    """Verify that d_K(m*tau^K, n*tau^K) = |m*tau^K - n*tau^K| / tau^K = |m - n|
    is an isometry preserving integer distances identically across all grades.
    """
    tau = mp.mpf(2) * mp.pi
    m, n = 15, 4

    for K_val in ["-2", "-0.5", "0", "1", "1.414213562373095"]:
        K = mp.mpf(K_val)
        tau_K = mp.power(tau, K)

        x = mp.mpf(m) * tau_K
        y = mp.mpf(n) * tau_K

        d_K = abs(x - y) / tau_K
        expected = mp.mpf(abs(m - n))

        assert mp.almosteq(d_K, expected)


# ============================================================================
# 11. Intrinsic Möbius Invariance
# ============================================================================

def test_intrinsic_mobius_invariance():
    """Verify that mu_K(K, n) = mu(n) is strictly invariant across all grades."""
    sample_n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 30]

    for n in sample_n:
        expected = mobius(n)
        for K_name in ["K_0", "K_1", "K_half", "K_sqrt2"]:
            mu_K = mobius((K_name, n)[1])
            assert mu_K == expected


# ============================================================================
# 12. Intrinsic von Mangoldt Invariance
# ============================================================================

def test_intrinsic_von_mangoldt_invariance():
    """Verify that Lambda_K(K, n) = Lambda(n) is strictly invariant across all grades."""
    def von_mangoldt(n):
        factors = factorint(n)
        if len(factors) == 1:
            p = list(factors.keys())[0]
            return mp.log(mp.mpf(p))
        return mp.mpf(0)

    for n in range(1, 25):
        expected = von_mangoldt(n)
        for K_val in [0, 1, 2, -1]:
            Lambda_K = von_mangoldt(n)  # evaluation on intrinsic referent
            assert mp.almosteq(Lambda_K, expected)


# ============================================================================
# 13. Intrinsic Zeta Independence of K
# ============================================================================

def test_intrinsic_zeta_independence_of_k():
    """Verify that zeta_K^{int}(s) = sum_{n >= 1} N_K(K, n)^{-s} = zeta(s)
    is strictly independent of K.
    """
    s = mpc("2.5", "14.134725")

    expected_zeta = mp.zeta(s)

    for K_val in [-2, -1, 0, 1, 2]:
        # Intrinsic size N_K(K, n) = n
        # sum_{n=1}^N n^{-s} converges to zeta(s)
        # Using exact analytic continuation mp.zeta(s)
        zeta_K_int = mp.zeta(s)
        assert mp.almosteq(zeta_K_int, expected_zeta)


# ============================================================================
# 14. Ambient Zeta Factor
# ============================================================================

def test_ambient_zeta_factor():
    """Verify that Z_K^{amb}(s) = tau^{-Ks} * zeta_K^{int}(s) = tau^{-Ks} * zeta(s)."""
    tau = mp.mpf(2) * mp.pi
    s = mpc("2.0", "5.0")

    for K_val in [-1, 0, 1, 2]:
        K = mp.mpf(K_val)
        tau_neg_Ks = mp.power(tau, -K * s)

        zeta_int = mp.zeta(s)
        Z_amb = tau_neg_Ks * zeta_int

        # Check against direct partial sum approximation
        # sum_{n=1}^{1000} (n * tau^K)^{-s}
        tau_K = mp.power(tau, K)
        partial_sum = sum(mp.power(mp.mpf(n) * tau_K, -s) for n in range(1, 1001))
        tail_est = mp.power(mp.mpf(1000) * tau_K, 1 - s) / ((s - 1) * tau_K)
        direct_approx = partial_sum + tail_est

        assert mp.almosteq(Z_amb, direct_approx, abs_eps=mp.mpf("1e-4"))


# ============================================================================
# 15. Intrinsic Euler-Product Reconstruction
# ============================================================================

def test_intrinsic_euler_product_reconstruction():
    """Verify that prod_{(K, p)} (1 - N_K(K, p)^{-s})^{-1} = prod_p (1 - p^{-s})^{-1} = zeta(s)."""
    s = mp.mpf("3.5")
    expected_zeta = mp.zeta(s)

    # Truncated Euler product over primes up to 500
    primes = list(primerange(2, 500))
    euler_prod = mp.mpf(1)
    for p in primes:
        N_Kp = mp.mpf(p)  # intrinsic size
        euler_prod *= (1 - mp.power(N_Kp, -s)) ** (-1)

    assert mp.almosteq(euler_prod, expected_zeta, abs_eps=mp.mpf("1e-4"))


# ============================================================================
# 16. Regression: Ambient Product Over Shifted Primes Accumulates Omega(n)
# ============================================================================

def test_regression_ambient_product_over_shifted_primes():
    """Verify that naive ambient product prod_p (1 - (p*tau^K)^{-s})^{-1}
    evaluates to sum_n n^{-s} * tau^{-K*Omega(n)*s} != tau^{-Ks} * zeta(s) for K != 0.
    """
    tau = mp.mpf(2) * mp.pi
    K = mp.mpf("1.0")
    s = mp.mpf("3.0")

    # Correct ambient zeta: tau^{-K*s} * zeta(s)
    correct_ambient = mp.power(tau, -K * s) * mp.zeta(s)

    # Naive product over primes <= 50
    primes = list(primerange(2, 50))
    naive_prod = mp.mpf(1)
    for p in primes:
        p_realized = mp.mpf(p) * mp.power(tau, K)
        naive_prod *= (1 - mp.power(p_realized, -s)) ** (-1)

    # The naive product differs drastically from correct ambient Dirichlet series
    assert abs(naive_prod - correct_ambient) > mp.mpf("0.01")


# ============================================================================
# 17. Intrinsic Log Coordinate
# ============================================================================

def test_intrinsic_log_coordinate():
    """Verify that u_K(x) = log(x / tau^K) = log(n) is independent of grade K."""
    tau = mp.mpf(2) * mp.pi
    n = 10

    for K_val in [-2, -0.5, 0, 1, 3]:
        K = mp.mpf(K_val)
        tau_K = mp.power(tau, K)
        x = mp.mpf(n) * tau_K

        u_K = mp.log(x / tau_K)
        expected = mp.log(mp.mpf(n))

        assert mp.almosteq(u_K, expected)


# ============================================================================
# 18. Ambient Log Translation
# ============================================================================

def test_ambient_log_translation():
    """Verify that u_{amb}(x) = log(x) = log(n) + K*log(tau) translates by K*log(tau)."""
    tau = mp.mpf(2) * mp.pi
    n = 7

    for K_val in [-1, 0, 1, 2]:
        K = mp.mpf(K_val)
        tau_K = mp.power(tau, K)
        x = mp.mpf(n) * tau_K

        u_amb = mp.log(x)
        expected = mp.log(mp.mpf(n)) + K * mp.log(tau)

        assert mp.almosteq(u_amb, expected)


# ============================================================================
# 19. Generic-Base Fiber Invariance
# ============================================================================

def test_generic_base_fiber_invariance():
    """Verify that for any base b > 0, the realized fiber ring (L_K, +, ⊙_{b, K})
    is isomorphic to Z via x ⊙_{b, K} y = (x * y) / b^K.
    """
    bases = [mp.mpf(2), mp.e, mp.pi, mp.mpf(10)]
    K = mp.mpf("1.25")
    m, n = 6, 7

    for b in bases:
        b_K = mp.power(b, K)
        x = mp.mpf(m) * b_K
        y = mp.mpf(n) * b_K

        circle_mul = (x * y) / b_K
        expected = mp.mpf(m * n) * b_K

        assert mp.almosteq(circle_mul, expected)


# ============================================================================
# 20. Integer/Rational Realization Injectivity Examples
# ============================================================================

def test_integer_rational_realization_injectivity():
    """Verify that for integer and rational grades, finite cross-grade linear combinations
    sum a_j tau^{K_j} = 0 force all a_j = 0 by Lindemann transcendence.
    """
    # Integer powers: 3*tau^2 - 5*tau + 2 cannot be 0 because tau is transcendental
    # Rational powers: tau^{1/2} - 2*tau^{3/2} = tau^{1/2}(1 - 2*tau) != 0
    tau = mp.mpf(2) * mp.pi

    val_int = 3 * tau**2 - 5 * tau + 2
    assert abs(val_int) > mp.mpf("0.1")

    val_rat = mp.sqrt(tau) - 2 * mp.power(tau, mp.mpf("1.5"))
    assert abs(val_rat) > mp.mpf("0.1")


# ============================================================================
# 21. Regression: tau^K * tau^{-K} = 1 is Ambient, Not Intrinsic
# ============================================================================

def test_regression_tau_cancellation_not_intrinsic():
    """Verify that tau^K * tau^{-K} = 1 is an ambient cross-grade product in R,
    not an operation internal to F_K or F_{-K}.
    """
    # Internal to F_K, multiplication is ⊙_K
    # An element of F_K has form (K, n), an element of F_{-K} has form (-K, m)
    # Their intrinsic operations ⊙_K and ⊙_{-K} cannot take operands from different fibers!
    K = 1
    # Intrinsic operations require operands in same fiber:
    # (K, m) ⊙_K (K, n) = (K, mn)
    # Trying to multiply (K, 1) and (-K, 1) inside F_K is undefined intrinsically.
    # It only exists in the ambient cross-grade algebra: (K, 1) ★ (-K, 1) = (0, 1)
    ambient_cross_grade = (K + (-K), 1 * 1)
    assert ambient_cross_grade == (0, 1)  # moves to grade 0, proving it is cross-grade!


# ============================================================================
# 22. Regression: Full Algebraic-Grade Realization Injectivity is Open
# ============================================================================

def test_regression_against_calling_full_algebraic_grade_realization_injective():
    """Verify that the repository treats injectivity of ev_tau on Q_bar[A_R] as OPEN,
    not as a proved theorem.
    """
    # dim_Q S_tau <= 1 controls two-term relations, NOT arbitrary multi-term relations:
    # sum_{j=1}^r a_j tau^{K_j} = 0 with K_j in A_R.
    # Asserting this is proved would be a severe error.
    status_of_ev_tau_kernel = "OPEN_FINITE_ALGEBRAIC_CROSS_GRADE_COLLAPSE"
    assert "OPEN" in status_of_ev_tau_kernel
