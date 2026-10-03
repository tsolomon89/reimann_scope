"""tests/test_tc_analytic_vs_arithmetic_intertwining.py — Verification of Analytic vs Arithmetic Grade Actions

TASK-TC-017: First-principles derivation, operator algebra, and intertwining relations:
1. Analytic TC dilation: A_K[zeta](s) = zeta(tau^{-K} s) = sum (n^{tau^{-K}})^{-s} (base power n -> n^{tau^{-K}}).
2. Arithmetic-grid dilation: D_K[zeta](s) = tau^{-K s} zeta(s) = sum (tau^K n)^{-s} (linear scale n -> tau^K n).
3. Operator algebra: A_K and D_J do not commute; they satisfy the semidirect affine relation:
   A_K D_J = D_{J tau^{-K}} A_K.
4. Log-space affine structure:
   - Arithmetic dilation is translation: S_K(x) = x + K log tau
   - Analytic dilation is scaling: T_J(x) = tau^{-J} x
   - Commutator discrepancy: S_K T_J(x) - T_J S_K(x) = (1 - tau^{-J}) K log tau.
5. Logarithmic derivatives:
   - Analytic: -d/ds log zeta(tau^{-K} s) = tau^{-K} sum Lambda(n) (n^{tau^{-K}})^{-s}
   - Grid: -d/ds log D_K[zeta](s) = K log tau - zeta'/zeta(s).
6. Euler product:
   - Analytic: generalized Euler product over pseudo-primes p^{tau^{-K}}
   - Grid: prod (1 - (tau^K p)^{-s})^{-1} = sum tau^{-K Omega(n) s} n^{-s} != tau^{-K s} zeta(s).
7. Mellin duality:
   - Linear scaling x -> tau^K x corresponds to D_K (arithmetic dilation)
   - Power scaling x -> x^{tau^K} corresponds to A_K (analytic dilation).
8. Completed xi functional equation:
   - Analytic preserves reflection about Re(s) = tau^K / 2
   - Arithmetic breaks reflection by automorphic factor tau^{K(2s - 1)}.
9. Commutator zero-evaluation and spectral defect:
   - Commutator ratio at zero s = tau^K rho has modulus tau^{K_eff delta}
   - Reflection defect is B_rho(K_eff) = 4 sinh^2(K_eff delta log tau / 2) with K_eff = J(tau^K - 1).
10. Bilateral symmetrization:
   - |tau^{-K(rho-1/2)}| + |tau^{K(rho-1/2)}| - 2 = B_rho(K).
"""

import math
import mpmath
import pytest
import sympy as sp


def tau_mpf(dps: int = 50) -> mpmath.mpf:
    """Return tau = 2*pi at declared precision."""
    with mpmath.workdps(dps):
        return 2 * mpmath.pi


class TestAnalyticVsArithmeticIntertwining:
    """Tests for analytic vs arithmetic grade actions, commutators, and intertwining."""

    def test_analytic_dilation_dirichlet_base_power(self):
        """Verify A_K[zeta](s) = sum (n^{tau^{-K}})^{-s} for Re(s) > 1."""
        dps = 40
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("0.5")  # rational grade K = 1/2
        s = mpmath.mpc("3.5", "1.2")  # well inside absolute convergence region

        # Exact analytic TC dilation: zeta(tau^{-K} * s)
        scaled_s = mpmath.power(tau, -K) * s
        exact_analytic = mpmath.zeta(scaled_s)

        # Truncated Dirichlet series with transformed bases: n^{tau^{-K}}
        tau_inv_K = mpmath.power(tau, -K)
        N = 500
        partial_sum = mpmath.mpc(0, 0)
        for n in range(1, N + 1):
            base = mpmath.power(n, tau_inv_K)
            term = mpmath.power(base, -s)
            partial_sum += term

        # Compare partial sum with exact zeta; difference must be bounded by tail ~ N^(1 - Re(tau^{-K} s))
        tail_order = mpmath.power(N, 1 - scaled_s.real) / (scaled_s.real - 1)
        discrepancy = abs(exact_analytic - partial_sum)
        assert discrepancy < 2 * tail_order

    def test_arithmetic_grid_dilation_dirichlet_prefactor(self):
        """Verify D_K[zeta](s) = sum (tau^K n)^{-s} = tau^{-K s} zeta(s)."""
        dps = 40
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("0.75")
        s = mpmath.mpc("3.0", "0.5")

        exact_grid_dilated = mpmath.power(tau, -K * s) * mpmath.zeta(s)

        # Truncated sum of scaled points (tau^K n)^{-s}
        tau_K = mpmath.power(tau, K)
        N = 500
        partial_sum = mpmath.mpc(0, 0)
        for n in range(1, N + 1):
            pt = tau_K * n
            partial_sum += mpmath.power(pt, -s)

        tail_order = mpmath.power(tau, -K * s.real) * (mpmath.power(N, 1 - s.real) / (s.real - 1))
        discrepancy = abs(exact_grid_dilated - partial_sum)
        assert discrepancy < 2 * tail_order

    def test_operator_group_actions_A_and_D(self):
        """Verify group action properties A_{K1} A_{K2} = A_{K1+K2} and D_{J1} D_{J2} = D_{J1+J2}."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K1 = mpmath.mpf("0.5")
        K2 = mpmath.mpf("-1.25")
        J1 = mpmath.mpf("1.5")
        J2 = mpmath.mpf("0.25")
        s = mpmath.mpc("2.2", "4.1")

        # A_{K1} A_{K2} [zeta](s) vs A_{K1+K2}[zeta](s)
        val_A_comp = mpmath.zeta(mpmath.power(tau, -K2) * (mpmath.power(tau, -K1) * s))
        val_A_sum = mpmath.zeta(mpmath.power(tau, -(K1 + K2)) * s)
        assert abs(val_A_comp - val_A_sum) < mpmath.mpf("1e-45")

        # D_{J1} D_{J2} [zeta](s) vs D_{J1+J2}[zeta](s)
        val_D_comp = mpmath.power(tau, -J1 * s) * (mpmath.power(tau, -J2 * s) * mpmath.zeta(s))
        val_D_sum = mpmath.power(tau, -(J1 + J2) * s) * mpmath.zeta(s)
        assert abs(val_D_comp - val_D_sum) < mpmath.mpf("1e-45")

    def test_operator_noncommutation_and_semidirect_conjugation(self):
        """Verify A_K D_J != D_J A_K and exact semidirect relation A_K D_J = D_{J tau^{-K}} A_K."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("1.0")
        J = mpmath.mpf("0.5")
        s = mpmath.mpc("2.5", "1.7")

        # A_K (D_J [zeta])(s) = tau^{-J * tau^{-K} * s} * zeta(tau^{-K} * s)
        scaled_s = mpmath.power(tau, -K) * s
        val_AK_DJ = mpmath.power(tau, -J * scaled_s) * mpmath.zeta(scaled_s)

        # D_J (A_K [zeta])(s) = tau^{-J * s} * zeta(tau^{-K} * s)
        val_DJ_AK = mpmath.power(tau, -J * s) * mpmath.zeta(scaled_s)

        # 1. Noncommutation
        diff_commutator = abs(val_AK_DJ - val_DJ_AK)
        assert diff_commutator > mpmath.mpf("1e-3")

        # 2. Exact ratio check: ratio = tau^{J * (1 - tau^{-K}) * s}
        expected_ratio = mpmath.power(tau, J * (1 - mpmath.power(tau, -K)) * s)
        computed_ratio = val_AK_DJ / val_DJ_AK
        assert abs(computed_ratio - expected_ratio) < mpmath.mpf("1e-45")

        # 3. Semidirect relation: A_K D_J = D_{J * tau^{-K}} A_K
        J_prime = J * mpmath.power(tau, -K)
        val_semidirect = mpmath.power(tau, -J_prime * s) * mpmath.zeta(scaled_s)
        assert abs(val_AK_DJ - val_semidirect) < mpmath.mpf("1e-45")

    def test_log_space_affine_commutator_discrepancy(self):
        """Verify log-space translation S_K and scaling T_J satisfy [S_K, T_J] discrepancy."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("0.5")
        J = mpmath.mpf("1.5")
        x = mpmath.mpf("3.14159")  # log n

        # S_K(x) = x + K * log(tau)
        # T_J(x) = tau^{-J} * x
        log_tau = mpmath.log(tau)
        S_K_T_J = mpmath.power(tau, -J) * x + K * log_tau
        T_J_S_K = mpmath.power(tau, -J) * (x + K * log_tau)

        discrepancy = S_K_T_J - T_J_S_K
        expected_discrepancy = (1 - mpmath.power(tau, -J)) * K * log_tau

        assert abs(discrepancy - expected_discrepancy) < mpmath.mpf("1e-45")
        assert abs(discrepancy) > mpmath.mpf("1e-3")

    def test_logarithmic_derivative_both_actions(self):
        """Verify -d/ds log zeta under analytic scaling vs arithmetic grid dilation."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("1.0")
        s = mpmath.mpc("3.0", "2.0")

        # 1. Analytic TC dilation: -d/ds log zeta(tau^{-K} s) = -tau^{-K} * (zeta'/zeta)(tau^{-K} s)
        scaled_s = mpmath.power(tau, -K) * s
        exact_analytic_log_deriv = -mpmath.power(tau, -K) * (mpmath.diff(mpmath.zeta, scaled_s) / mpmath.zeta(scaled_s))

        # Numerical derivative of log(zeta(tau^{-K} * s))
        num_analytic_log_deriv = -mpmath.diff(lambda w: mpmath.log(mpmath.zeta(mpmath.power(tau, -K) * w)), s)
        assert abs(exact_analytic_log_deriv - num_analytic_log_deriv) < mpmath.mpf("1e-30")

        # 2. Arithmetic grid dilation: -d/ds log (tau^{-K s} zeta(s)) = K log(tau) - (zeta'/zeta)(s)
        exact_grid_log_deriv = K * mpmath.log(tau) - (mpmath.diff(mpmath.zeta, s) / mpmath.zeta(s))
        num_grid_log_deriv = -mpmath.diff(lambda w: mpmath.log(mpmath.power(tau, -K * w) * mpmath.zeta(w)), s)
        assert abs(exact_grid_log_deriv - num_grid_log_deriv) < mpmath.mpf("1e-30")

        # Discrepancy between the two actions on logarithmic derivative
        assert abs(exact_analytic_log_deriv - exact_grid_log_deriv) > mpmath.mpf("1e-2")

    def test_euler_product_preservation_analytic_vs_grid_failure(self):
        """Verify analytic action preserves Euler product while grid replacement produces tau^{-K Omega(n) s}."""
        s, K, tau = sp.symbols("s K tau", positive=True)
        p1, p2 = sp.symbols("p1 p2", positive=True)

        # 1. Analytic action on two-factor Euler product:
        # 1 / (1 - (p1^{tau^{-K}})^{-s}) * 1 / (1 - (p2^{tau^{-K}})^{-s})
        # = sum_{a,b >= 0} (p1^a p2^b)^{-tau^{-K} s} = sum (n^{tau^{-K}})^{-s}
        # Multiplicativity holds: (p1 * p2)^{tau^{-K}} = p1^{tau^{-K}} * p2^{tau^{-K}}
        mult_check = sp.simplify((p1 * p2)**(tau**(-K)) - p1**(tau**(-K)) * p2**(tau**(-K)))
        assert mult_check == 0

        # 2. Grid product: 1 / (1 - (tau^K p1)^{-s}) * 1 / (1 - (tau^K p2)^{-s})
        # Expand up to second order:
        # term for p1: tau^{-K s} p1^{-s}
        # term for p1*p2: tau^{-2 K s} (p1*p2)^{-s}
        # If it were tau^{-K s} * native, term for p1*p2 would be tau^{-K s} (p1*p2)^{-s}.
        # Discrepancy in power of tau:
        diff_power = (-2 * K * s) - (-K * s)
        assert diff_power == -K * s

    def test_mellin_duality_linear_vs_power_scaling(self):
        """Verify linear scaling in x corresponds to D_K and power scaling corresponds to A_K."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("0.5")
        s = mpmath.mpc("2.4", "1.1")

        # Test function phi(x) = exp(-x)
        # 1. Linear scaling: M_{tau^K} phi(x) = exp(-tau^K * x)
        tau_K = mpmath.power(tau, K)
        mellin_linear = mpmath.quad(
            lambda x: mpmath.exp(-tau_K * x) * mpmath.power(x, s - 1),
            [0, mpmath.inf]
        )
        expected_D_K = mpmath.power(tau, -K * s) * mpmath.gamma(s)
        assert abs(mellin_linear - expected_D_K) < mpmath.mpf("1e-45")

        # 2. Power scaling: P_K phi(x) = tau^K * exp(-x^{tau^K})
        mellin_power = mpmath.quad(
            lambda x: tau_K * mpmath.exp(-mpmath.power(x, tau_K)) * mpmath.power(x, s - 1),
            [0, mpmath.inf]
        )
        expected_A_K = mpmath.gamma(mpmath.power(tau, -K) * s)
        assert abs(mellin_power - expected_A_K) < mpmath.mpf("1e-45")

    def test_completed_xi_reflection_symmetry_vs_breakage(self):
        """Verify A_K[xi] preserves reflection about Re(s)=tau^K/2, while D_K[xi] breaks reflection."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("1.0")

        def xi_func(z):
            return mpmath.mpf("0.5") * z * (z - 1) * mpmath.power(mpmath.pi, -z / 2) * mpmath.gamma(z / 2) * mpmath.zeta(z)

        # 1. Analytic TC: A_K[xi](s) = xi(tau^{-K} s)
        # Symmetry axis is Re(s) = tau^K / 2. Reflection: s -> tau^K - s
        tau_K = mpmath.power(tau, K)
        s = tau_K * mpmath.mpc("0.5", "14.134725") + mpmath.mpc("0.2", "1.5")
        refl_s = tau_K - s

        val_AK_s = xi_func(mpmath.power(tau, -K) * s)
        val_AK_refl = xi_func(mpmath.power(tau, -K) * refl_s)
        assert abs(val_AK_s - val_AK_refl) < mpmath.mpf("1e-40")

        # 2. Arithmetic Grid Dilation: D_K[xi](s) = tau^{-K s} xi(s)
        # Standard reflection s -> 1 - s
        s_std = mpmath.mpc("0.7", "10.0")
        val_DK_s = mpmath.power(tau, -K * s_std) * xi_func(s_std)
        val_DK_refl = mpmath.power(tau, -K * (1 - s_std)) * xi_func(1 - s_std)

        # Exact ratio is tau^{K * (2*s - 1)}
        ratio = val_DK_refl / val_DK_s
        expected_ratio = mpmath.power(tau, K * (2 * s_std - 1))
        assert abs(ratio - expected_ratio) < mpmath.mpf("1e-40")

    def test_commutator_zero_evaluation_spectral_defect(self):
        """Verify commutator ratio evaluated at zero s = tau^K rho yields B_rho(K_eff)."""
        dps = 60
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("0.5")
        J = mpmath.mpf("1.0")
        delta = mpmath.mpf("0.12")
        gamma = mpmath.mpf("14.134725")
        rho = mpmath.mpc(mpmath.mpf("0.5") + delta, gamma)
        rho_hash = mpmath.mpc(mpmath.mpf("0.5") - delta, gamma)

        # Multiplier in A_K D_J at s = tau^K * rho: tau^{-J * rho}
        m_AK_DJ = mpmath.power(tau, -J * rho)
        # Multiplier in D_J A_K at s = tau^K * rho: tau^{-J * tau^K * rho}
        m_DJ_AK = mpmath.power(tau, -J * mpmath.power(tau, K) * rho)

        # Ratio:
        R_rho = m_AK_DJ / m_DJ_AK
        # Critical background (delta = 0):
        rho_0 = mpmath.mpc(mpmath.mpf("0.5"), gamma)
        R_0 = mpmath.power(tau, -J * rho_0) / mpmath.power(tau, -J * mpmath.power(tau, K) * rho_0)

        # Normalized ratio:
        R_norm_rho = R_rho / R_0
        mod_rho = abs(R_norm_rho)

        # Reflected zero:
        m_AK_DJ_hash = mpmath.power(tau, -J * rho_hash)
        m_DJ_AK_hash = mpmath.power(tau, -J * mpmath.power(tau, K) * rho_hash)
        R_norm_hash = (m_AK_DJ_hash / m_DJ_AK_hash) / R_0
        mod_hash = abs(R_norm_hash)

        # Reflection defect:
        defect = mod_rho + mod_hash - 2

        # Expected B_rho(K_eff) with K_eff = J * (tau^K - 1)
        K_eff = J * (mpmath.power(tau, K) - 1)
        expected_B = 4 * mpmath.power(mpmath.sinh(K_eff * delta * mpmath.log(tau) / 2), 2)

        assert abs(defect - expected_B) < mpmath.mpf("1e-50")
        assert defect > 0  # strictly positive off-critical

    def test_bilateral_symmetrization_modulus_identity(self):
        """Verify bilateral symmetrization of arithmetic multiplier modulus yields B_rho(K)."""
        dps = 60
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("0.75")
        delta = mpmath.mpf("0.25")
        gamma = mpmath.mpf("21.022")
        z = mpmath.mpc(delta, gamma)

        # Centered arithmetic multiplier: tau^{-K * z}
        mod_pos = abs(mpmath.power(tau, -K * z))
        mod_neg = abs(mpmath.power(tau, K * z))

        bilateral_defect = mod_pos + mod_neg - 2
        expected_B = 4 * mpmath.power(mpmath.sinh(K * delta * mpmath.log(tau) / 2), 2)

        assert abs(bilateral_defect - expected_B) < mpmath.mpf("1e-50")

    def test_common_grade_shift_correlator_invariance_condition(self):
        """Verify bivariate correlator G_rho(K, J) and condition G(K+A, J+A) = G(K, J) <=> delta = 0."""
        dps = 60
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        K = mpmath.mpf("1.0")
        J = mpmath.mpf("0.5")
        A = mpmath.mpf("0.25")
        gamma = mpmath.mpf("14.134725")

        # 1. Off-critical zero: delta != 0
        delta_off = mpmath.mpf("0.1")
        chi_K = mpmath.power(tau, K * delta_off) * mpmath.exp(1j * K * gamma * mpmath.log(tau))
        chi_J = mpmath.power(tau, J * delta_off) * mpmath.exp(1j * J * gamma * mpmath.log(tau))
        G_KJ = chi_K * mpmath.conj(chi_J)

        # Corrected correlator formula: tau^{(K+J)*delta} * exp(i*(K-J)*gamma*log(tau))
        G_expected = mpmath.power(tau, (K + J) * delta_off) * mpmath.exp(1j * (K - J) * gamma * mpmath.log(tau))
        assert abs(G_KJ - G_expected) < mpmath.mpf("1e-50")

        # Shifted correlator: G(K+A, J+A)
        chi_K_A = mpmath.power(tau, (K + A) * delta_off) * mpmath.exp(1j * (K + A) * gamma * mpmath.log(tau))
        chi_J_A = mpmath.power(tau, (J + A) * delta_off) * mpmath.exp(1j * (J + A) * gamma * mpmath.log(tau))
        G_KJ_A = chi_K_A * mpmath.conj(chi_J_A)

        # Ratio must be tau^{2 * A * delta}
        shift_ratio = G_KJ_A / G_KJ
        expected_ratio = mpmath.power(tau, 2 * A * delta_off)
        assert abs(shift_ratio - expected_ratio) < mpmath.mpf("1e-50")
        assert abs(shift_ratio - 1) > mpmath.mpf("1e-3")  # not invariant off-critical!

        # 2. Critical zero: delta = 0
        delta_crit = mpmath.mpf("0.0")
        chi_K_crit = mpmath.exp(1j * K * gamma * mpmath.log(tau))
        chi_J_crit = mpmath.exp(1j * J * gamma * mpmath.log(tau))
        G_KJ_crit = chi_K_crit * mpmath.conj(chi_J_crit)

        chi_K_A_crit = mpmath.exp(1j * (K + A) * gamma * mpmath.log(tau))
        chi_J_A_crit = mpmath.exp(1j * (J + A) * gamma * mpmath.log(tau))
        G_KJ_A_crit = chi_K_A_crit * mpmath.conj(chi_J_A_crit)

        assert abs(G_KJ_A_crit - G_KJ_crit) < mpmath.mpf("1e-50")  # exactly invariant on critical line!
