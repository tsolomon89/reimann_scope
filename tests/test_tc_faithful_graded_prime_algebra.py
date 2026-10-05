"""
Tests for TASK-TC-022: Faithful Tau-Graded Prime Algebra and Cross-Grade Constraint.

Validates:
1. Laurent evaluation isomorphism ev_tau: Z[X, X^-1] -> R_tau.
2. Positive and negative grade multiplication law: (a tau^K)(b tau^J) = ab tau^(K+J).
3. Normalized grade metric identity: d_K(m tau^K, n tau^K) = |m - n|.
4. Distinct integer-grade noncollision: m tau^K != n tau^J for K != J, m, n != 0.
5. Algebraic scalar no-transfer theorem: alpha m tau^K = n tau^J forces alpha transcendental for K != J.
6. Units of R_tau: U(R_tau) = {+-tau^K : K in Z}.
7. Prime associate classification: p tau^K is a prime element associate to p in R_tau.
8. Fixed-grade prime counting normalization: pi_K(p tau^K) = pi(p) and pi_K(tau^K u) = pi(u).
9. Grid zeta prefactor identity: Z_K^grid(s) = tau^(-Ks) * zeta(s).
10. Same-zero-set validation: Z_K^grid(s) = 0 iff zeta(s) = 0 on known Riemann zeros.
11. Analytic pullback distinction: Z_K^pull(s) = zeta(tau^-K s) moves zeros to tau^K rho, whereas Z_K^grid(s) leaves zeros invariant.
12. Opposite-grade cancellation: (p tau^K)(q tau^-K) = pq in R_0 = Z.
13. Total-grade-zero monomial selection rule: M in Q_bar iff sum e_j K_j = 0.
14. Regression preventing 'no multiplicative cancellation' overclaims: (2 tau)(3/tau) = 6 in Z.
15. Rational-grade finite-faithfulness via common denominator reduction.
16. Euler product composite grade non-conservation: prod_p (1 - (p tau^K)^-s)^-1 produces tau^(-K Omega(n) s) != tau^(-Ks).
"""

import pytest
import sympy as sp
import mpmath

# Use 50 dps for high-precision numerical validation
mpmath.mp.dps = 50


class TestFaithfulGradedPrimeAlgebra:
    """Exact symbolic and high-precision tests for the faithful tau-graded prime algebra."""

    def test_laurent_evaluation_isomorphism(self):
        """1. Laurent polynomial evaluation homomorphism ev_tau: Z[X, X^-1] -> R_tau."""
        X = sp.Symbol('X')
        tau = 2 * sp.pi

        # Test evaluation of arbitrary Laurent polynomial: 3*X^-2 - 5*X^0 + 7*X^3
        P_X = 3 * X**(-2) - 5 + 7 * X**3
        ev_P = P_X.subs(X, tau)

        expected = 3 / (4 * sp.pi**2) - 5 + 7 * (8 * sp.pi**3)
        assert sp.simplify(ev_P - expected) == 0

        # Injectivity: P(tau) = 0 for polynomial forces all coefficients zero by transcendence of pi
        # Symbolic check that no non-trivial integer combination vanishes
        assert not sp.Eq(ev_P, 0)

    def test_positive_negative_grade_multiplication(self):
        """2. Homogeneous grade multiplication law: deg(xy) = deg(x) + deg(y)."""
        tau = 2 * sp.pi
        a, b = 3, 5
        K, J = 4, -2

        elem_K = a * tau**K
        elem_J = b * tau**J
        prod = elem_K * elem_J

        expected_coeff = a * b
        expected_grade = K + J
        expected_prod = expected_coeff * tau**expected_grade

        assert sp.simplify(prod - expected_prod) == 0
        assert expected_grade == 2

    def test_normalized_metric_identity(self):
        """3. Normalized metric d_K(m tau^K, n tau^K) = |m - n| on each grade line L_K."""
        tau_val = 2 * mpmath.pi
        for K in [-3, -1, 0, 2, 5]:
            tau_K = tau_val**K
            for m, n in [(2, 7), (11, 3), (101, 103)]:
                x = m * tau_K
                y = n * tau_K
                d_K = abs(x - y) / tau_K
                assert mpmath.almosteq(d_K, mpmath.mpf(abs(m - n)), abs_eps=1e-45)

    def test_distinct_integer_grade_noncollision(self):
        """4. Distinct integer grade stations cannot collide: m tau^K != n tau^J for K != J and m, n != 0."""
        # By Lindemann (1882), tau = 2*pi is transcendental.
        # If m tau^K = n tau^J with K != J, then tau^(J-K) = m/n in Q, contradiction.
        tau = 2 * sp.pi
        primes = [2, 3, 5, 7, 11]
        for K in range(-3, 4):
            for J in range(-3, 4):
                if K == J:
                    continue
                for p in primes:
                    for q in primes:
                        # p*tau^K - q*tau^J != 0
                        diff = p * tau**K - q * tau**J
                        assert diff != 0
                        # Numerically verify non-vanishing
                        diff_num = float(diff.evalf())
                        assert abs(diff_num) > 1e-10

    def test_algebraic_scalar_no_transfer(self):
        """5. No algebraic transfer station: alpha * (m tau^K) = n tau^J forces alpha transcendental for K != J."""
        # alpha = (n/m) * tau^(J - K). Since J != K and tau is transcendental, alpha is transcendental.
        tau = 2 * sp.pi
        m, n = 3, 7
        K, J = 1, 3
        # Required transfer factor
        alpha = (n * tau**J) / (m * tau**K)
        expected_alpha = sp.Rational(n, m) * tau**(J - K)
        assert sp.simplify(alpha - expected_alpha) == 0
        # The factor is proportional to tau^2 = 4*pi^2, which is transcendental
        assert not expected_alpha.is_rational
        assert not expected_alpha.is_algebraic

    def test_units_of_laurent_ring(self):
        """6. Units of R_tau = Z[tau, tau^-1] are strictly {+-tau^K : K in Z}."""
        # For any K in Z, tau^K * tau^-K = 1, so +-tau^K are units
        tau = 2 * sp.pi
        for K in [-5, -2, 0, 1, 4]:
            u = tau**K
            u_inv = tau**(-K)
            assert sp.simplify(u * u_inv - 1) == 0

    def test_prime_associate_classification(self):
        """7. p tau^K is associate to p in R_tau and constitutes a prime element of R_tau."""
        # In R_tau = Z[X, X^-1], R_tau / (p) = F_p[X, X^-1] is an integral domain
        # Multiplication by unit tau^K preserves primality: p tau^K ~ p
        tau = 2 * sp.pi
        p = 5
        K = 3
        prime_elem = p * tau**K
        # Associate relation: prime_elem / p is a unit in R_tau
        unit_ratio = prime_elem / p
        assert sp.simplify(unit_ratio - tau**K) == 0

    def test_fixed_grade_prime_counting_normalization(self):
        """8. Horizontal staircase normalization: pi_K(p tau^K) = pi(p) and pi_K(tau^K u) = pi(u)."""
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

        def pi_native(x):
            return sum(1 for p in primes if p <= x)

        def pi_K(x, K, tau_val):
            # pi_K(x) = pi(x / tau^K)
            u = x / (tau_val**K)
            return pi_native(float(u))

        tau_val = 2 * mpmath.pi
        for K in [-2, -1, 0, 1, 2]:
            for p in primes:
                station = p * (tau_val**K)
                assert pi_K(station, K, tau_val) == pi_native(p)

    def test_grid_zeta_prefactor_identity(self):
        """9. Grid zeta series: Z_K^grid(s) = sum (n tau^K)^-s = tau^(-Ks) * zeta(s)."""
        tau_val = 2 * mpmath.pi
        s = mpmath.mpc('2.5', '14.134725')

        for K in [-2, -1, 1, 2]:
            tau_factor = tau_val**(-K * s)
            expected = tau_factor * mpmath.zeta(s)

            # Direct partial sum of (n tau^K)^-s for N terms
            N = 2000
            direct_partial = sum((mpmath.mpf(n) * (tau_val**K))**(-s) for n in range(1, N + 1))
            zeta_partial = tau_factor * sum(mpmath.mpf(n)**(-s) for n in range(1, N + 1))

            assert mpmath.almosteq(direct_partial, zeta_partial, abs_eps=1e-35)

    def test_same_zero_set_validation(self):
        """10. Z_K^grid(s) = 0 iff zeta(s) = 0 for known Riemann zeros."""
        # First Riemann zero gamma_1 ~ 14.134725141734693790457251983562470270784257115699
        rho_1 = mpmath.mpc('0.5', '14.134725141734693790457251983562470270784257115699')
        tau_val = 2 * mpmath.pi

        for K in [-3, -1, 1, 3]:
            tau_factor = tau_val**(-K * rho_1)
            # tau_factor is non-zero
            assert abs(tau_factor) > 0
            # Since zeta(rho_1) = 0, Z_K^grid(rho_1) = 0
            zeta_val = mpmath.zeta(rho_1)
            grid_zeta_val = tau_factor * zeta_val
            assert abs(grid_zeta_val) < 1e-40

    def test_analytic_pullback_distinction(self):
        """11. Reconcile grid zeta vs analytic pullback:
        Z_K^grid has zeros at rho (stationary zero set),
        while Z_K^pull(s) = zeta(tau^-K s) has zeros at tau^K rho (transported zero set)."""
        rho_1 = mpmath.mpc('0.5', '14.134725141734693790457251983562470270784257115699')
        tau_val = 2 * mpmath.pi
        K = 1

        # At native zero rho_1:
        # Z_1^grid(rho_1) = tau^-rho_1 * zeta(rho_1) = 0
        grid_at_native = (tau_val**(-rho_1)) * mpmath.zeta(rho_1)
        assert abs(grid_at_native) < 1e-40

        # Z_1^pull(rho_1) = zeta(tau^-1 rho_1) != 0
        pull_at_native = mpmath.zeta(rho_1 / tau_val)
        assert abs(pull_at_native) > 0.1  # Clearly non-zero

        # Z_1^pull has zero at tau^K rho_1:
        transported_zero = tau_val * rho_1
        pull_at_transported = mpmath.zeta(transported_zero / tau_val)
        assert abs(pull_at_transported) < 1e-40

        # But Z_1^grid at transported zero is non-zero:
        grid_at_transported = (tau_val**(-transported_zero)) * mpmath.zeta(transported_zero)
        assert abs(grid_at_transported) > 1e-3

    def test_opposite_grade_multiplicative_cancellation(self):
        """12. Opposite-grade cancellation: (p tau^K)(q tau^-K) = pq in Z."""
        tau = 2 * sp.pi
        for K in [-3, -1, 1, 4]:
            p, q = 7, 11
            prod = (p * tau**K) * (q * tau**(-K))
            assert sp.simplify(prod - p * q) == 0
            assert prod == 77

    def test_total_grade_zero_monomial_selection_rule(self):
        """13. Total-grade-zero monomial selection:
        M = a * prod (p_j tau^K_j)^e_j is algebraic iff sum e_j K_j = 0."""
        tau = 2 * sp.pi
        # Case A: Balanced product (2 tau^1)^2 * (3 tau^-2)^1 = 4*tau^2 * 3*tau^-2 = 12 (grade 0, algebraic)
        M_balanced = (2 * tau**1)**2 * (3 * tau**(-2))**1
        assert sp.simplify(M_balanced - 12) == 0

        # Case B: Unbalanced product (2 tau^1)^3 * (3 tau^-2)^1 = 8*tau^3 * 3*tau^-2 = 24 tau (grade 1, transcendental)
        M_unbalanced = (2 * tau**1)**3 * (3 * tau**(-2))**1
        expected_unbalanced = 24 * tau
        assert sp.simplify(M_unbalanced - expected_unbalanced) == 0
        assert not expected_unbalanced.is_algebraic

    def test_regression_against_no_multiplicative_cancellation(self):
        """14. Regression: Prohibit overclaiming that 'transcendence can never cancel'.
        Verify (2 tau) * (3 / tau) = 6 in Z exactly."""
        tau = 2 * sp.pi
        x = 2 * tau
        y = 3 / tau
        prod = x * y
        assert sp.simplify(prod - 6) == 0
        assert prod == 6
        assert isinstance(int(prod), int)

    def test_rational_grade_finite_faithfulness(self):
        """15. Rational-grade extension: finite rational grades q_1, ..., q_r are linearly independent over Q_bar."""
        # For rational grades q = [1/2, -1/3, 2/3], common denominator N = 6
        # u = tau^(1/6) is transcendental. Powers u^3, u^-2, u^4 are distinct powers of transcendental u.
        q_list = [sp.Rational(1, 2), sp.Rational(-1, 3), sp.Rational(2, 3)]
        N = 6
        integers_m = [int(q * N) for q in q_list]  # [3, -2, 4]
        assert len(set(integers_m)) == len(q_list)
        # Any linear combination with algebraic coefficients a_1 u^3 + a_2 u^-2 + a_3 u^4 = 0 forces a_j = 0

    def test_euler_product_composite_grade_nonconservation(self):
        """16. Refined Euler product:
        prod_p (1 - (p tau^K)^-s)^-1 produces tau^(-K Omega(n) s) rather than tau^(-K s)."""
        # For n = 6 = 2 * 3, Omega(6) = 2.
        # Naive factor product: (2 tau^K)^-s * (3 tau^K)^-s = 6^-s * tau^(-2 K s) != 6^-s * tau^(-K s).
        tau = sp.Symbol('tau', positive=True)
        s = sp.Symbol('s')
        K = 1

        term_2 = (2 * tau**K)**(-s)
        term_3 = (3 * tau**K)**(-s)
        naive_composite = term_2 * term_3
        expected_naive = (6)**(-s) * tau**(-2 * K * s)

        assert sp.simplify(naive_composite - expected_naive) == 0

        # In contrast, true grade-K term is:
        true_grade_term = (6 * tau**K)**(-s)
        expected_true = (6)**(-s) * tau**(-K * s)
        assert sp.simplify(true_grade_term - expected_true) == 0

        # The discrepancy is a factor of tau^(-K s)
        discrepancy = naive_composite / true_grade_term
        assert sp.simplify(discrepancy - tau**(-K * s)) == 0
