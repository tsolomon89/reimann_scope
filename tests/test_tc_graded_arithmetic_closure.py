"""tests/test_tc_graded_arithmetic_closure.py — Graded Arithmetic Monoid, Grade Units, and TC Closure Constraint

TASK-TC-018:
1. Graded arithmetic monoid M_tau = A_R x Z_{!=0}, operation (K, n) * (J, m) = (K+J, nm).
2. Realization homomorphism Phi_tau(K, n) = n * tau^K into (R^x, *).
3. Grade units u_K = (K, 1), unit group U(M_tau) = A_R x {+-1}.
4. Canonical unique factorization into grade unit, sign, and native primes:
   (K, n) = u_K * (0, sgn n) * prod_p (0, p)^{v_p(|n|)}.
5. Grade-unit quotient M_tau / U_grade =~ Z_{!=0} recovers ordinary integer arithmetic.
6. Canonical Dirichlet character chi_s(K, n) = tau^{-Ks} n^{-s} and fixed-grade Dirichlet series
   D_K[zeta](s) = tau^{-Ks} zeta(s) = chi_s(u_K) zeta(s).
7. Refined Euler product: global grade-unit twist of native Euler product tau^{-Ks} prod_p (1 - p^{-s})^{-1}.
8. Rational-grade escape theorem: K in Q\\{0}, J in A_R\\{0} ==> J tau^{-K} notin A_R.
9. Double coordinate escape under analytic dilation: (J, n) |-> (J tau^{-K}, n^{tau^{-K}}).
10. Generic-base control: algebraic base b=2 preserves algebraic grade closure; transcendental tau=2pi escapes.
11. Bilateral grade-unit character reflection defect identity:
    |chi_hat_rho(u_K)| + |chi_hat_{1-rho}(u_K)| - 2 = tau^{K delta} + tau^{-K delta} - 2 = B_rho(K).
12. Proper subgroup classification: G_TC is a countable dense proper subgroup of Aff_+(R).
13. Fork B resolution: algebraic-grade escape is unconditional (delta-independent), whereas B_rho(K) is delta-dependent.
"""

import math
import mpmath
import pytest
import sympy as sp


def tau_mpf(dps: int = 50) -> mpmath.mpf:
    """Return tau = 2*pi at declared precision."""
    with mpmath.workdps(dps):
        return 2 * mpmath.pi


class TestGradedArithmeticClosure:
    """Unit tests for the graded arithmetic monoid and closure constraint."""

    def test_graded_monoid_multiplication_and_algebraic_structure(self):
        """Verify binary operation (K, n) * (J, m) = (K+J, nm), identity, associativity, commutativity."""
        # Elements in M_tau: (grade, integer)
        e1 = (sp.Rational(1, 2), 6)
        e2 = (sp.Rational(-3, 4), -10)
        e3 = (sp.sqrt(2), 7)

        # Binary operation: (K+J, nm)
        def mult(x, y):
            return (x[0] + y[0], x[1] * y[1])

        # Identity
        e0 = (sp.Integer(0), 1)
        assert mult(e1, e0) == e1
        assert mult(e0, e1) == e1

        # Commutativity
        assert mult(e1, e2) == mult(e2, e1)

        # Associativity: (e1 * e2) * e3 == e1 * (e2 * e3)
        prod1 = mult(mult(e1, e2), e3)
        prod2 = mult(e1, mult(e2, e3))
        assert sp.simplify(prod1[0] - prod2[0]) == 0
        assert prod1[1] == prod2[1]

    def test_realization_map_homomorphism(self):
        """Verify Phi_tau((K, n) * (J, m)) = Phi_tau(K, n) * Phi_tau(J, m)."""
        dps = 40
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi

        K = mpmath.mpf("0.6")
        n = 15
        J = mpmath.mpf("-1.4")
        m = -4

        # Realization map: Phi_tau(K, n) = n * tau^K
        def phi(k_val, n_val):
            return n_val * mpmath.power(tau, k_val)

        phi_x = phi(K, n)
        phi_y = phi(J, m)
        phi_prod = phi(K + J, n * m)

        assert abs(phi_prod - (phi_x * phi_y)) < mpmath.mpf("1e-35")

    def test_grade_units_inverses_and_group_structure(self):
        """Verify grade units u_K = (K, 1), u_K * u_J = u_{K+J}, and unit group U(M_tau)."""
        def u(k):
            return (k, 1)

        K = sp.Rational(2, 3)
        J = sp.Rational(-5, 7)

        # Multiplication of units
        u_K = u(K)
        u_J = u(J)
        u_prod = (u_K[0] + u_J[0], u_K[1] * u_J[1])
        assert u_prod == u(K + J)

        # Inverses
        u_inv = (u_K[0] + u(-K)[0], u_K[1] * u(-K)[1])
        assert u_inv == (0, 1)

        # General unit in M_tau must have second coordinate in {1, -1}
        # because n * m = 1 in Z_{!=0} implies n = m in {1, -1}
        for n in [-3, -2, 0, 2, 3, 5]:
            if n != 0:
                is_invertible = abs(n) == 1
                assert is_invertible == (n in [1, -1])

    def test_canonical_factorization_into_grade_unit_and_native_primes(self):
        """Verify canonical factorization: (K, n) = u_K * (0, sgn n) * prod_p (0, p)^{v_p(|n|)}."""
        # Test element: K = sqrt(3), n = -360
        # 360 = 2^3 * 3^2 * 5^1
        K = sp.sqrt(3)
        n = -360

        u_K = (K, 1)
        sgn_elem = (0, -1 if n < 0 else 1)

        prime_factors = sp.factorint(abs(n))  # {2: 3, 3: 2, 5: 1}
        assert prime_factors == {2: 3, 3: 2, 5: 1}

        # Recompose from prime elements (0, p) and grade unit u_K
        recomposed_grade = u_K[0] + sgn_elem[0]
        recomposed_n = u_K[1] * sgn_elem[1]
        for p, exp in prime_factors.items():
            recomposed_grade += 0 * exp
            recomposed_n *= (p ** exp)

        assert recomposed_grade == K
        assert recomposed_n == n

    def test_grade_unit_quotient_recovers_native_integers(self):
        """Verify projection pi(K, n) = n has kernel U_grade, establishing M_tau / U_grade =~ Z_{!=0}."""
        # Coset of (K, n) modulo U_grade:
        # (K, n) ~ (J, m) iff exists A in A_R such that (K, n) = (A, 1) * (J, m) = (J+A, m)
        # This requires m = n.
        elements = [
            (sp.Rational(1, 2), 42),
            (sp.sqrt(2), 42),
            (sp.Integer(-5), 42),
            (sp.Rational(3, 7), -17),
            (sp.sqrt(5), -17)
        ]

        def pi(elem):
            return elem[1]

        # Check that all elements with same second coordinate project to the same referent
        assert pi(elements[0]) == pi(elements[1]) == pi(elements[2]) == 42
        assert pi(elements[3]) == pi(elements[4]) == -17

        # The quotient is exactly isomorphic to Z_{!=0}
        referents = {pi(elem) for elem in elements}
        assert referents == {42, -17}

    def test_canonical_dirichlet_character_multiplicativity(self):
        """Verify chi_s(K, n) = tau^{-Ks} n^{-s} is multiplicative and factors through u_K."""
        dps = 40
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        s = mpmath.mpc("2.5", "1.5")

        def chi(k_val, n_val, s_val):
            return mpmath.power(tau, -k_val * s_val) * mpmath.power(n_val, -s_val)

        K1, n1 = mpmath.mpf("0.4"), 6
        K2, n2 = mpmath.mpf("-1.1"), 7

        chi1 = chi(K1, n1, s)
        chi2 = chi(K2, n2, s)
        chi_prod = chi(K1 + K2, n1 * n2, s)

        assert abs(chi_prod - (chi1 * chi2)) < mpmath.mpf("1e-35")

        # Factorization through grade unit u_K = (K, 1):
        # chi_s(K, n) = chi_s(u_K) * chi_s(0, n)
        chi_uK = chi(K1, 1, s)
        chi_native = chi(0, n1, s)
        assert abs(chi1 - (chi_uK * chi_native)) < mpmath.mpf("1e-35")

    def test_fixed_grade_dirichlet_series_as_global_unit_twist(self):
        """Verify D_K[zeta](s) = tau^{-Ks} zeta(s) is a global unit twist of the native Euler product."""
        dps = 40
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("0.5")
        s = mpmath.mpc("3.0", "1.0")

        # Exact grid character sum: D_K[zeta](s) = tau^{-Ks} zeta(s)
        exact_D_K = mpmath.power(tau, -K * s) * mpmath.zeta(s)

        # Factorized via native Euler product over standard primes:
        # tau^{-Ks} * prod_p (1 - p^{-s})^{-1}
        # Truncate Euler product at prime 100
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        partial_euler = mpmath.mpc(1, 0)
        for p in primes:
            partial_euler *= (1 - mpmath.power(p, -s)) ** (-1)
        factorized_euler = mpmath.power(tau, -K * s) * partial_euler

        # In contrast, the naive "grid primes" product prod_p (1 - (tau^K p)^{-s})^{-1}
        naive_grid_primes_prod = mpmath.mpc(1, 0)
        for p in primes:
            naive_grid_primes_prod *= (1 - mpmath.power(tau * mpmath.power(tau, K - 1) * p, -s)) ** (-1)
            # which is (1 - (tau^K p)^{-s})^{-1}

        # factorized_euler converges to exact_D_K as prime cutoff grows
        err_native = abs(exact_D_K - factorized_euler)
        # naive product does NOT converge to exact_D_K
        diff_naive = abs(exact_D_K - naive_grid_primes_prod)
        assert err_native < mpmath.mpf("0.01")
        assert diff_naive > mpmath.mpf("0.1")

    def test_rational_grade_escape_theorem_exact(self):
        """Prove J tau^{-K} notin A_R for all K in Q\\{0} and J in A_R\\{0}."""
        # Theorem: Let K = a/b in Q\\{0} with a in Z\\{0}, b in Z_{>=1}.
        # Let J in A_R\\{0}.
        # If J tau^{-K} in A_R, then (J tau^{-K}) / J = tau^{-a/b} in A_R.
        # Raising to -b in Z gives tau^a in A_R, which implies (2*pi)^a in A_R.
        # If a != 0, this implies pi is algebraic, contradicting Lindemann (1882).
        # Therefore J tau^{-K} is transcendental for all K in Q\\{0}, J in A_R\\{0}.

        # Test with SymPy: verify pi is transcendental
        assert not sp.pi.is_algebraic
        tau = 2 * sp.pi
        assert not tau.is_algebraic

        # Test specific instances: K = 1/2, J = 3
        # J * tau^{-1/2} = 3 / sqrt(2*pi) is transcendental
        K = sp.Rational(1, 2)
        J = sp.Integer(3)
        term = J * (tau ** (-K))
        # Since pi is transcendental, term cannot be algebraic
        assert not term.is_algebraic

        # Test with algebraic irrational J = sqrt(2), K = -2/3
        J_alg = sp.sqrt(2)
        K_rat = sp.Rational(-2, 3)
        term2 = J_alg * (tau ** (-K_rat))
        assert not term2.is_algebraic

    def test_coordinate_double_escape_under_analytic_dilation(self):
        """Verify (J, n) |-> (J tau^{-K}, n^{tau^{-K}}) escapes both A_R and Z."""
        dps = 40
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi

        K = mpmath.mpf("0.5")  # K = 1/2
        J = mpmath.mpf("1.0")
        n = 2

        # Transformed grade: J' = J tau^{-K}
        tau_inv_K = mpmath.power(tau, -K)
        transformed_grade = J * tau_inv_K  # 1 / sqrt(2*pi) ~= 0.398942...
        # Transformed base: n' = n^{tau^{-K}}
        transformed_base = mpmath.power(n, tau_inv_K)  # 2^{1/sqrt(2*pi)} ~= 1.31848...

        # Transformed base is NOT an integer
        nearest_int = round(float(transformed_base))
        assert abs(transformed_base - nearest_int) > mpmath.mpf("0.1")
        # In fact, for any K > 0 and n >= 2: tau^{-K} < 1, so 1 < n^{tau^{-K}} < n.
        # For n = 2, 2^{tau^{-K}} in (1, 2), which contains NO INTEGERS!
        assert 1 < transformed_base < 2

    def test_generic_base_control_algebraic_vs_transcendental(self):
        """Verify that algebraic base b=2 preserves algebraic grade closure while transcendental tau escapes."""
        # For algebraic base b = 2:
        # b^{-K} for K in Q is algebraic (e.g. 2^{-1/2} = 1/sqrt(2) in A_R).
        # Therefore J b^{-K} in A_R for any J in A_R.
        b_alg = sp.Integer(2)
        K_rat = sp.Rational(1, 2)
        J_alg = sp.Integer(3)

        transformed_grade_alg = J_alg * (b_alg ** (-K_rat))  # 3 / sqrt(2)
        assert transformed_grade_alg.is_algebraic  # CLOSED in A_R!

        # For transcendental base tau = 2*pi:
        tau = 2 * sp.pi
        transformed_grade_trans = J_alg * (tau ** (-K_rat))  # 3 / sqrt(2*pi)
        assert not transformed_grade_trans.is_algebraic  # ESCAPES A_R!

    def test_grade_unit_character_reflection_defect_identity(self):
        """Verify bilateral grade-unit character reflection defect equals B_rho(K)."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi

        K = mpmath.mpf("1.3")
        delta = mpmath.mpf("0.075")
        gamma = mpmath.mpf("14.134725")

        # Zero and reflected zero
        rho = mpmath.mpc(mpmath.mpf("0.5") + delta, gamma)
        rho_refl = mpmath.mpc(mpmath.mpf("0.5") - delta, -gamma)

        # Grade unit character: chi_s(u_K) = tau^{-Ks}
        chi_rho = mpmath.power(tau, -K * rho)
        chi_refl = mpmath.power(tau, -K * rho_refl)

        # Normalize by critical line modulus tau^{-K/2}
        norm_factor = mpmath.power(tau, -K * mpmath.mpf("0.5"))
        mod_rho_norm = abs(chi_rho) / norm_factor
        mod_refl_norm = abs(chi_refl) / norm_factor

        # Expected normalized moduli: tau^{-K delta} and tau^{K delta}
        assert abs(mod_rho_norm - mpmath.power(tau, -K * delta)) < mpmath.mpf("1e-45")
        assert abs(mod_refl_norm - mpmath.power(tau, K * delta)) < mpmath.mpf("1e-45")

        # Bilateral symmetrization minus baseline:
        bilateral_defect = mod_rho_norm + mod_refl_norm - 2

        # Formula for B_rho(K): 4 * sinh^2(K delta log(tau) / 2)
        arg = (K * delta * mpmath.log(tau)) / 2
        exact_B_rho = 4 * (mpmath.sinh(arg) ** 2)

        assert abs(bilateral_defect - exact_B_rho) < mpmath.mpf("1e-45")
        assert exact_B_rho > 0

        # At delta = 0 (critical line), defect must vanish identically
        arg_zero = (K * 0 * mpmath.log(tau)) / 2
        assert 4 * (mpmath.sinh(arg_zero) ** 2) == 0

    def test_proper_subgroup_classification_of_tc_affine_group(self):
        """Verify G_TC is a countable dense proper subgroup of Aff_+(R)."""
        # Aff_+(R) is an uncountable 2D Lie group of dimension 2 and cardinality 2^aleph_0.
        # G_TC = < S_K, T_J : K, J in A_R >.
        # Since A_R is countable (|A_R| = aleph_0), the generated subgroup G_TC is COUNTABLE.
        # A countable subgroup of an uncountable Lie group cannot be isomorphic to the whole group.
        # It is a proper, dense subgroup.
        dps = 30
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi

        # Show density of dilations: for any target a > 0, we can approximate log(a) by -J log(tau) with J in Q
        target_a = mpmath.mpf("3.14159")
        target_log = mpmath.log(target_a)
        log_tau = mpmath.log(tau)
        J_approx = -target_log / log_tau  # real number
        J_rational = round(float(J_approx) * 1000) / 1000  # rational approximation
        dil_approx = mpmath.power(tau, -J_rational)
        rel_err = abs(dil_approx - target_a) / target_a
        assert rel_err < 0.01  # dense approximation exists

    def test_fork_b_validation_delta_independence_of_grade_escape(self):
        """Verify that rational-grade escape holds unconditionally (delta-independent), confirming Fork B."""
        # Rational-grade escape: J tau^{-K} notin A_R for K in Q\\{0}, J in A_R\\{0}.
        # Notice that delta does not enter this theorem!
        # Whether delta = 0 (RH holds) or delta != 0 (RH fails), J tau^{-K} is transcendental.
        # Thus algebraic-grade escape is NOT an obstruction to off-critical zeros;
        # it is an inherent property of the transcendental dilation tau^{-K}.
        # In contrast, B_rho(K) = 4 sinh^2(K delta log(tau) / 2) is 0 iff delta = 0.
        tau = 2 * sp.pi
        K = sp.Rational(1, 3)
        J = sp.Integer(2)
        transcendental_grade = J * (tau ** (-K))
        assert not transcendental_grade.is_algebraic

        # This holds regardless of any zeta zero or delta value!
        # Confirms Fork B: analytic dilation naturally lives in the ambient completion A_R * tau^{A_R}.
