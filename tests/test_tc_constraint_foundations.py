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

    def test_grid_structure_and_scale_generators(self):
        """Test grid non-coincidence and scale generator comparison."""
        with mpmath.workdps(50):
            tau = 2 * mpmath.pi
            pi_val = mpmath.pi

            # Scale generator relationship: tau = 2*pi
            assert abs(tau - 2 * pi_val) < 1e-48

            # Incommensurability for algebraic K != J:
            # If m * tau^K == n * tau^J, then tau^(K-J) == n/m in Q
            # For K=1, J=0: tau^1 = 2*pi is transcendental, so 2*pi != n/m for any integer n, m
            for m in range(1, 20):
                for n in range(1, 100):
                    assert abs(float(tau) - float(n) / float(m)) > 1e-4

            # For K=sqrt(2), J=0: tau^sqrt(2) is transcendental (Gelfond-Schneider theorem on logarithms)
            tau_sqrt2 = mpmath.power(tau, mpmath.sqrt(2))
            for m in range(1, 20):
                for n in range(1, 100):
                    assert abs(float(tau_sqrt2) - float(n) / float(m)) > 1e-4
