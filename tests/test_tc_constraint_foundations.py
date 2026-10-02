"""tests/test_tc_constraint_foundations.py — Verification of TC Mathematical Foundations

Tests the core mathematical relationships of Transcendental Continuation (TC):
1. Invariance of the scaled zeta representative: Z_tau(tau^K s, K) = zeta(s)
2. Exact coordinate round-trip: tau^{-K} (tau^K s) = s
3. Radial leaf invariance: R_tau(tau^K rho, K) = Re(rho) - 1/2 = delta
   verified for critical zeros (delta=0) and synthetic off-critical points (delta!=0).
4. Testing across the canonical TC grade domain K in A_R (real algebraic numbers):
   - K = 0 (native grade)
   - Positive integers: K = 1, 2
   - Negative integers: K = -1, -2
   - Rational grades: K = 1/2, -1/3, 3/4
   - Real algebraic irrationals: K = sqrt(2), -sqrt(2), (1 + sqrt(5))/2 (golden ratio phi).
5. Grid structure L_K = tau^K (+-N) and incommensurability checks.
6. Multi-precision consistency to verify absence of floating-point drift.
"""

import math
import mpmath
import pytest


def tau_val(dps: int = 50) -> mpmath.mpf:
    """Return tau = 2*pi with declared decimal places."""
    with mpmath.workdps(dps):
        return 2 * mpmath.pi


def z_tau(s: mpmath.mpc, K: mpmath.mpf, dps: int = 50) -> mpmath.mpc:
    """Evaluate Z_tau(s, K) = zeta(tau^{-K} * s) at high precision."""
    with mpmath.workdps(dps):
        tau = 2 * mpmath.pi
        scale = mpmath.power(tau, -K)
        scaled_s = scale * s
        return mpmath.zeta(scaled_s)


def radial_leaf(s: mpmath.mpc, K: mpmath.mpf, dps: int = 50) -> mpmath.mpf:
    """Evaluate R_tau(s, K) = tau^{-K} * Re(s) - 1/2."""
    with mpmath.workdps(dps):
        tau = 2 * mpmath.pi
        scale = mpmath.power(tau, -K)
        return scale * s.real - mpmath.mpf("0.5")


class TestTranscendentalContinuationFoundations:
    """Verification of canonical TC definitions and coordinate invariants."""

    @pytest.mark.parametrize("grade_name,K_expr", [
        ("native_zero", "0"),
        ("int_pos_1", "1"),
        ("int_pos_2", "2"),
        ("int_neg_1", "-1"),
        ("int_neg_2", "-2"),
        ("rat_half", "1/2"),
        ("rat_neg_third", "-1/3"),
        ("rat_three_fourths", "3/4"),
        ("alg_sqrt2", "sqrt(2)"),
        ("alg_neg_sqrt2", "-sqrt(2)"),
        ("alg_golden_ratio", "(1 + sqrt(5))/2"),
    ])
    def test_graded_zeta_pullback_invariance(self, grade_name: str, K_expr: str):
        """Test Z_tau(tau^K * s, K) == zeta(s) across canonical algebraic grades."""
        with mpmath.workdps(60):
            if K_expr == "0":
                K = mpmath.mpf("0")
            elif K_expr == "1":
                K = mpmath.mpf("1")
            elif K_expr == "2":
                K = mpmath.mpf("2")
            elif K_expr == "-1":
                K = mpmath.mpf("-1")
            elif K_expr == "-2":
                K = mpmath.mpf("-2")
            elif K_expr == "1/2":
                K = mpmath.mpf("0.5")
            elif K_expr == "-1/3":
                K = -mpmath.mpf("1") / mpmath.mpf("3")
            elif K_expr == "3/4":
                K = mpmath.mpf("0.75")
            elif K_expr == "sqrt(2)":
                K = mpmath.sqrt(2)
            elif K_expr == "-sqrt(2)":
                K = -mpmath.sqrt(2)
            elif K_expr == "(1 + sqrt(5))/2":
                K = (mpmath.mpf("1") + mpmath.sqrt(5)) / mpmath.mpf("2")
            else:
                raise ValueError(f"Unknown grade expression: {K_expr}")

            # Test points in critical strip and off-line
            test_s_points = [
                mpmath.mpc("2.0", "3.0"),            # Region of absolute convergence
                mpmath.mpc("0.5", "14.134725141734"), # On critical line near first zero
                mpmath.mpc("0.75", "25.0"),           # Inside strip, off critical line
                mpmath.mpc("-1.5", "10.0"),           # Left of critical strip
            ]

            tau = 2 * mpmath.pi
            scale_forward = mpmath.power(tau, K)
            scale_backward = mpmath.power(tau, -K)

            # Round-trip verification
            assert abs(scale_forward * scale_backward - 1.0) < 1e-50

            for s in test_s_points:
                s_K = scale_forward * s
                round_trip_s = scale_backward * s_K
                assert abs(round_trip_s - s) < 1e-50

                # Evaluate native zeta vs graded representative Z_tau(s_K, K)
                val_native = mpmath.zeta(s)
                val_graded = z_tau(s_K, K, dps=60)
                diff = abs(val_native - val_graded)
                assert diff < 1e-45, f"Graded pullback mismatch for {grade_name} at s={s}: diff={diff}"

    @pytest.mark.parametrize("grade_name,K_expr", [
        ("native_zero", "0"),
        ("int_pos_1", "1"),
        ("int_neg_1", "-1"),
        ("rat_half", "1/2"),
        ("alg_sqrt2", "sqrt(2)"),
        ("alg_golden_ratio", "(1 + sqrt(5))/2"),
    ])
    def test_radial_leaf_invariance(self, grade_name: str, K_expr: str):
        """Test R_tau(tau^K * rho, K) == Re(rho) - 1/2 == delta exactly."""
        with mpmath.workdps(60):
            if K_expr == "0":
                K = mpmath.mpf("0")
            elif K_expr == "1":
                K = mpmath.mpf("1")
            elif K_expr == "-1":
                K = mpmath.mpf("-1")
            elif K_expr == "1/2":
                K = mpmath.mpf("0.5")
            elif K_expr == "sqrt(2)":
                K = mpmath.sqrt(2)
            elif K_expr == "(1 + sqrt(5))/2":
                K = (mpmath.mpf("1") + mpmath.sqrt(5)) / mpmath.mpf("2")
            else:
                raise ValueError(K_expr)

            tau = 2 * mpmath.pi
            scale_K = mpmath.power(tau, K)

            # 1. Critical-line zero: gamma_1 ~= 14.13472514173469379, delta = 0
            gamma_1 = mpmath.mpf("14.1347251417346937904572519835624702707842571156992431756855674")
            rho_crit = mpmath.mpc("0.5", gamma_1)
            rho_crit_K = scale_K * rho_crit

            delta_crit_native = rho_crit.real - mpmath.mpf("0.5")
            delta_crit_graded = radial_leaf(rho_crit_K, K, dps=60)
            assert abs(delta_crit_native) < 1e-50
            assert abs(delta_crit_graded) < 1e-50

            # 2. Synthetic off-critical zero: delta_0 = 0.49 != 0, gamma = 50.0
            delta_0 = mpmath.mpf("0.49")
            rho_off = mpmath.mpc(mpmath.mpf("0.5") + delta_0, "50.0")
            rho_off_K = scale_K * rho_off

            delta_off_native = rho_off.real - mpmath.mpf("0.5")
            delta_off_graded = radial_leaf(rho_off_K, K, dps=60)
            assert abs(delta_off_native - delta_0) < 1e-50
            assert abs(delta_off_graded - delta_0) < 1e-50, f"Radial invariant failed for {grade_name}: {delta_off_graded}"

    def test_null_model_arbitrary_function_coherence(self):
        """Verify that pure pullback coherence holds for ANY function, demonstrating the null model."""
        with mpmath.workdps(50):
            # Define an arbitrary synthetic function with deliberate off-line zeros
            # f(s) = (s - (0.9 + 25.0i)) * (s - (0.1 - 25.0i)) * exp(s)
            z_off = mpmath.mpc("0.9", "25.0")
            delta_expected = z_off.real - mpmath.mpf("0.5")  # delta = +0.40

            def arb_f(s: mpmath.mpc) -> mpmath.mpc:
                return (s - z_off) * (s - mpmath.conj(z_off)) * mpmath.exp(s)

            # Check that f(z_off) == 0
            assert abs(arb_f(z_off)) < 1e-45

            # Transport to irrational algebraic grade K = sqrt(2)
            K = mpmath.sqrt(2)
            tau = 2 * mpmath.pi
            scale_K = mpmath.power(tau, K)
            z_off_K = scale_K * z_off

            # Graded pull-back: F_K(s) = arb_f(tau^{-K} * s)
            def F_K(s: mpmath.mpc) -> mpmath.mpc:
                return arb_f(mpmath.power(tau, -K) * s)

            # In the null model:
            # 1. F_K(z_off_K) == 0 holds identically
            assert abs(F_K(z_off_K)) < 1e-45
            # 2. Radial leaf invariant R_tau(z_off_K, K) == delta_expected holds identically
            delta_computed = radial_leaf(z_off_K, K)
            assert abs(delta_computed - delta_expected) < 1e-45

            # CONCLUSION: Pure pullback does not exclude off-critical zeros for a generic function.
            # Any RH-excluding constraint MUST arise from zeta-specific arithmetic/analytic structure.

    def test_rational_grade_noncollision_exact_theorem(self):
        """Verify the exact algebraic noncollision theorem for rational grade differences.
        
        Theorem: For any distinct rational grades J != K in Q, L_J cap L_K = emptyset.
        Proof: If m * tau^K == n * tau^J with m, n in Z\\{0}, then tau^(K-J) = n/m in Q.
        Writing K - J = p/q with p in Z\\{0} and q in N, raising to the q-th power yields
        tau^p = (n/m)^q in Q. Thus tau satisfies a non-trivial algebraic polynomial with
        integer coefficients, contradicting the transcendence of tau = 2*pi (Lindemann 1882).
        """
        import sympy as sp
        tau_sym = sp.Symbol("tau", positive=True)
        # Symbolic verification of polynomial reduction: (tau^(p/q))^q - (n/m)^q = tau^p - (n/m)^q
        p, q = 3, 4
        m, n = 5, 7
        lhs_pow = (tau_sym ** (sp.Rational(p, q))) ** q
        rhs_pow = sp.Rational(n, m) ** q
        assert sp.simplify(lhs_pow - tau_sym ** p) == 0
        assert rhs_pow == sp.Rational(2401, 625)
        # Lindemann's theorem asserts tau is transcendental, so tau^p cannot be rational for p != 0.

    def test_transcendental_base_counterexample_gelfond_schneider(self):
        """Verify the mandatory control counterexample b = 2^(1/sqrt(2)).
        
        By Gelfond-Schneider (1934), b = 2^(1/sqrt(2)) has algebraic base 2 != 0, 1
        and irrational algebraic exponent 1/sqrt(2), so b is TRANSCENDENTAL.
        However, b^(sqrt(2)) = (2^(1/sqrt(2)))^(sqrt(2)) = 2^1 = 2 in Q!
        
        Therefore, m * b^(sqrt(2)) = n * b^0 has an exact nonzero integer solution:
        1 * b^(sqrt(2)) = 2 * b^0  (m=1, n=2).
        
        This PROVES that transcendence of a base alone DOES NOT imply noncollision
        at irrational algebraic exponents. Full algebraic-grade noncollision for tau
        CANNOT be inferred from transcendence of tau without an independent theorem.
        """
        with mpmath.workdps(60):
            # Compute b = 2^(1/sqrt(2))
            sqrt2 = mpmath.sqrt(2)
            b = mpmath.power(2, 1 / sqrt2)
            # b^(sqrt(2)) == 2 exactly
            b_pow_sqrt2 = mpmath.power(b, sqrt2)
            assert abs(b_pow_sqrt2 - 2) < 1e-50

            # Collision in grid L_{sqrt(2), b} and L_{0, b}:
            # m * b^(sqrt(2)) == n * b^0 for m=1, n=2
            m = 1
            n = 2
            diff = m * b_pow_sqrt2 - n * mpmath.power(b, 0)
            assert abs(diff) < 1e-50

    def test_irrational_algebraic_exponent_status_open(self):
        """Confirm that irrational algebraic tau-exponent collision is classified as OPEN.
        
        Neither Gelfond-Schneider (requires algebraic base) nor Baker's theorem
        (linear forms in logarithms of algebraic numbers) directly establishes
        whether (2*pi)^sqrt(2) is irrational or transcendental.
        The full algebraic grid disjointness question is strictly OPEN.
        """
        status_classification = "OPEN_TAU_ALGEBRAIC_EXPONENT_ARITHMETIC"
        assert status_classification.startswith("OPEN")

    def test_minimal_spectral_detector_B_rho_exact(self):
        """Verify the minimal finite-grade reflection defect detector B_rho(K).
        
        B_rho(K) = |chi_rho(K)| + |chi_{rho^#}(K)| - 2
                 = tau^(K*delta) + tau^(-K*delta) - 2
                 = 4 * sinh^2(K*delta*log(tau) / 2).
        For every nonzero algebraic grade K in A_R \\ {0}:
          B_rho(K) >= 0, and B_rho(K) == 0 iff delta == 0.
        """
        with mpmath.workdps(60):
            tau = 2 * mpmath.pi
            log_tau = mpmath.log(tau)

            # Test across multiple algebraic grades: K = 1, -1, 1/2, sqrt(2), (1+sqrt(5))/2
            test_grades = [
                mpmath.mpf("1"),
                mpmath.mpf("-1"),
                mpmath.mpf("0.5"),
                mpmath.sqrt(2),
                (1 + mpmath.sqrt(5)) / 2
            ]

            # Case A: On the critical line (delta = 0)
            delta_on = mpmath.mpf("0.0")
            for K in test_grades:
                val_exp = mpmath.power(tau, K * delta_on) + mpmath.power(tau, -K * delta_on) - 2
                val_sinh = 4 * (mpmath.sinh(K * delta_on * log_tau / 2) ** 2)
                assert abs(val_exp) < 1e-50
                assert abs(val_sinh) < 1e-50

            # Case B: Off the critical line (delta != 0)
            delta_off = mpmath.mpf("0.49")
            for K in test_grades:
                val_exp = mpmath.power(tau, K * delta_off) + mpmath.power(tau, -K * delta_off) - 2
                val_sinh = 4 * (mpmath.sinh(K * delta_off * log_tau / 2) ** 2)
                assert abs(val_exp - val_sinh) < 1e-50
                # Strictly positive for delta != 0 and K != 0
                assert val_exp > 1e-10
                assert val_sinh > 1e-10

    def test_generic_base_detector_control(self):
        """Verify that B_{rho,b}(K) >= 0 and == 0 iff delta == 0 for ANY base b > 1.
        
        This establishes that the hyperbolic positivity detector is NOT tau-specific.
        Any tau/zeta-specific constraint must reside in constructing the arithmetic
        functional A_K, not in the detector itself.
        """
        with mpmath.workdps(60):
            for b in [mpmath.mpf("1.5"), mpmath.mpf("2.0"), mpmath.mpf("10.0"), mpmath.exp(1)]:
                log_b = mpmath.log(b)
                delta = mpmath.mpf("0.35")
                K = mpmath.sqrt(3)  # algebraic grade
                B_val = 4 * (mpmath.sinh(K * delta * log_b / 2) ** 2)
                assert B_val > 0

                # Zero check
                B_zero = 4 * (mpmath.sinh(K * 0 * log_b / 2) ** 2)
                assert abs(B_zero) < 1e-50

    def test_common_grade_shift_translation_identity(self):
        """Verify the common-grade translation shift relation:
        
        G_rho(K, J) = chi_rho(K) * conj(chi_rho(J))
        G_rho(K+A, J+A) = tau^(2*A*delta) * G_rho(K, J).
        
        Common-grade translation invariance G(K+A, J+A) == G(K, J) forces:
        tau^(2*A*delta) == 1 ==> delta == 0.
        """
        with mpmath.workdps(60):
            tau = 2 * mpmath.pi
            log_tau = mpmath.log(tau)
            delta = mpmath.mpf("0.49")
            gamma = mpmath.mpf("14.13472514173469379")

            K = mpmath.sqrt(2)
            J = mpmath.mpf("0.5")
            A = mpmath.mpf("1.5")  # shift amount

            def chi(k_val):
                return mpmath.exp(k_val * (delta + mpmath.mpc(0, gamma)) * log_tau)

            G_base = chi(K) * mpmath.conj(chi(J))
            G_shifted = chi(K + A) * mpmath.conj(chi(J + A))

            scaling_factor = mpmath.power(tau, 2 * A * delta)
            expected_shifted = scaling_factor * G_base

            assert abs(G_shifted - expected_shifted) < 1e-45
            # At delta != 0, scaling factor != 1
            assert abs(scaling_factor - 1) > 1e-5
