"""
tests/test_explicit_formula.py

Comprehensive test suite for the Riemann–Weil explicit formula,
grade-indexed test function family, Fourier scaling, finite divisor defects,
linearized Jacobian compensation, and expanded-native-basis equivalence.
"""

import json
import pytest
import mpmath
import math_core
import reference_data


def test_test_function_evenness_and_derivatives():
    """Verify test functions H_j(t) are strictly even and analytic derivatives match numerical differentiation."""
    with mpmath.workdps(80):
        for j in range(1, 7):
            # Evenness: H_j(-t) == H_j(t)
            for t_val in [mpmath.mpf('0.0'), mpmath.mpf('14.1347'), mpmath.mpf('50.25')]:
                h_pos = math_core.H_test_function(t_val, j, dps=80)
                h_neg = math_core.H_test_function(-t_val, j, dps=80)
                assert abs(h_pos - h_neg) < mpmath.mpf('1e-70'), f"Test function j={j} failed evenness at t={t_val}"

            # Derivative check vs mpmath.diff
            for t_val in [mpmath.mpf('1.5'), mpmath.mpf('14.1347'), mpmath.mpf('30.0')]:
                analytic_prime = math_core.H_test_function_prime(t_val, j, dps=80)
                numerical_prime = mpmath.diff(lambda u: math_core.H_test_function(u, j, dps=int(mpmath.mp.dps) + 10), t_val)
                assert abs(analytic_prime - numerical_prime) < mpmath.mpf('1e-20'), f"j={j} derivative mismatch at t={t_val}"


def test_fourier_transform_analytic_vs_quadrature():
    """Verify analytic Fourier transform H_hat_j(x) against numerical quadrature."""
    with mpmath.workdps(70):
        for j in [1, 2, 3]:
            sigma, t0 = math_core.get_test_function_params(j, dps=70)
            for x_val in [mpmath.mpf('0.0'), mpmath.mpf('0.5'), mpmath.mpf('2.0')]:
                ana_hat = math_core.H_test_function_hat(x_val, j, dps=70)
                # Numerical Fourier transform: 2 * int_0^inf H_j(t) cos(x*t) dt
                num_hat = mpmath.mpf(2) * mpmath.quad(
                    lambda t: math_core.H_test_function(t, j, dps=70) * mpmath.cos(x_val * t),
                    [0, float(t0 + 15 * sigma)]
                )
                assert abs(ana_hat - num_hat) < mpmath.mpf('1e-20'), f"j={j} Fourier transform discrepancy at x={x_val}"


def test_grade_k_fourier_scaling():
    """Verify Fourier scaling \\widehat{h}_{K,j}(x) = a_K^{-1} * \\widehat{H}_j(a_K^{-1} * x) across K in {-2, -1, 0, 1, 2}."""
    with mpmath.workdps(80):
        tau = math_core.get_tau(dps=80)
        for K in [-2, -1, 0, 1, 2]:
            a_K = mpmath.power(tau, K)
            for j in [1, 2, 3, 4, 5, 6]:
                for x_val in [mpmath.mpf('0.5'), mpmath.mpf('1.5'), mpmath.mpf('3.0')]:
                    h_hat_scaled = math_core.h_kj_scaled_hat(x_val, j, K, dps=80)
                    expected_hat = (mpmath.mpf(1) / a_K) * math_core.H_test_function_hat(x_val / a_K, j, dps=80)
                    assert abs(h_hat_scaled - expected_hat) < mpmath.mpf('1e-70'), f"K={K}, j={j} Fourier scaling error at x={x_val}"


def test_explicit_formula_native_baseline_eval():
    """Verify native explicit formula residual is within the observational error budget (< 1e-15) for j=1..6."""
    with mpmath.workdps(80):
        ref_zeros = reference_data.load_reference_zeros()
        assert len(ref_zeros) >= 100

        for j in range(1, 7):
            res = math_core.explicit_formula_eval(
                j=j,
                K=0,
                zeros_ordinates=ref_zeros,
                prime_cutoff=50000,
                dps=70
            )
            # Residual = Spectral_Sum - Total_RHS
            assert abs(res["residual"]) < mpmath.mpf('1e-15'), f"j={j} explicit formula baseline residual too large: {res['residual']}"
            assert res["spectral_sum"] > 0
            assert res["total_rhs"] > 0


def test_grade_covariance_and_expanded_basis_equivalence():
    """Verify that grade-K explicit formula constraints are coordinate_redundant with the expanded K=0 basis."""
    with mpmath.workdps(80):
        ref_zeros = reference_data.load_reference_zeros()[:30]
        equiv = math_core.check_expanded_native_basis_equivalence(
            j_list=[1, 2, 3, 4, 5, 6],
            k_list=[-2, -1, 0, 1, 2],
            zeros_subset=ref_zeros,
            dps=80
        )
        assert equiv["is_equivalent"] is True
        assert equiv["classification"] == "coordinate_redundant"
        assert equiv["max_discrepancy"] < mpmath.mpf('1e-70')
        assert equiv["rank_K"] == equiv["rank_stacked"]


def test_critical_height_finite_divisor_defect_linear_response():
    """Verify finite divisor defect matches analytic Jacobian derivative in the linear regime."""
    with mpmath.workdps(80):
        ref_zeros = reference_data.load_reference_zeros()[:10]
        gamma_1 = ref_zeros[0]
        gamma_2 = ref_zeros[1]

        j = 1
        K = 0
        eps_small = mpmath.mpf('1e-5')

        # 1. Off-peak zero (gamma_2 for test function j=1): linear response J * eps dominates
        defect_off_peak = math_core.finite_divisor_defect_critical_height(j, K, gamma_2, eps_small, dps=80)
        linear_approx = mpmath.mpf(2) * math_core.H_test_function_prime(gamma_2, j, dps=80) * eps_small
        rel_diff = abs(defect_off_peak - linear_approx) / abs(defect_off_peak)
        assert rel_diff < mpmath.mpf('1e-4'), f"Linear response defect discrepancy: {rel_diff}"

        # 2. Peak zero (gamma_1 for test function j=1): H_1'(gamma_1) ~ 0, defect is quadratic in eps
        defect_peak = math_core.finite_divisor_defect_critical_height(j, K, gamma_1, eps_small, dps=80)
        assert defect_peak < 0  # since gamma_1 is maximum of Gaussian packet H_1
        assert abs(defect_peak) > mpmath.mpf('1e-15')


def test_radial_quartet_multiplicity_preserving_defect():
    """Verify symmetry-complete radial quartet defect is non-zero and multiplicity-preserving."""
    with mpmath.workdps(80):
        ref_zeros = reference_data.load_reference_zeros()[:10]
        ga = ref_zeros[0]
        gb = ref_zeros[1]
        delta = mpmath.mpf('0.05')

        # Evaluated at j=1, K=0
        defect = math_core.finite_divisor_defect_radial_quartet(1, 0, ga, gb, delta, dps=80)
        assert abs(defect) > mpmath.mpf('1e-5'), f"Radial quartet defect expected to be non-zero, got {defect}"


def test_linearized_compensation_rank_and_precision_stability():
    """Verify Jacobian SVD, rank, condition number, and compensation solution stability at 80 vs 120 dps."""
    ref_zeros = reference_data.load_reference_zeros()[:30]
    j_list = [1, 2, 3, 4, 5, 6]
    k_list = [-2, -1, 0, 1, 2]

    # 80 dps run
    J_80 = math_core.explicit_formula_jacobian(j_list, k_list, ref_zeros, dps=80)
    sol_80 = math_core.solve_linearized_compensation(J_80, target_col_idx=0, epsilon='0.001', dps=80)

    # 120 dps run
    J_120 = math_core.explicit_formula_jacobian(j_list, k_list, ref_zeros, dps=120)
    sol_120 = math_core.solve_linearized_compensation(J_120, target_col_idx=0, epsilon='0.001', dps=120)

    assert sol_80["detected"] is True
    assert sol_120["detected"] is True
    assert sol_80["numerical_rank"] == sol_120["numerical_rank"]
    assert sol_80["nullity"] == sol_120["nullity"]
    assert abs(sol_80["v_norm"] - sol_120["v_norm"]) < mpmath.mpf('1e-70')
    assert abs(sol_80["compensation_norm"] - sol_120["compensation_norm"]) < mpmath.mpf('1e-70')
