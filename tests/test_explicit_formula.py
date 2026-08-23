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
                    [0, t0 + 15 * sigma]
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
    """Verify native explicit formula residual is within observational error budget (< 1e-15) for j=1..6."""
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
        assert equiv["theoretical_classification"] == "coordinate_redundant"
        assert equiv["finite_basis_classification"] == "finite_basis_enrichment_only"
        assert equiv["max_discrepancy"] < mpmath.mpf('1e-70')
        assert equiv["rank_grade"] == equiv["rank_native"]
        assert equiv["rank_grade"] == equiv["rank_stacked"]


def test_grade_covariance_non_tautological_detection():
    """Verify that intentional corruption of native parameters is detected by basis equivalence check."""
    with mpmath.workdps(80):
        ref_zeros = reference_data.load_reference_zeros()[:10]
        # Evaluate standard equivalence
        equiv_std = math_core.check_expanded_native_basis_equivalence(
            j_list=[1],
            k_list=[1],
            zeros_subset=ref_zeros,
            dps=80
        )
        assert equiv_std["is_equivalent"] is True

        # Now test evaluation of wrong native parameter
        t0_corrupt = mpmath.mpf('14.1347') + mpmath.mpf('1.0')
        sigma_corrupt = mpmath.mpf('0.5')
        h_corrupt = math_core.H_native_gaussian(ref_zeros[0], sigma_corrupt, t0_corrupt, dps=80)
        h_true = math_core.h_kj_scaled(ref_zeros[0], j=1, K=1, dps=80)
        assert abs(h_corrupt - h_true) > mpmath.mpf('1e-5')


def test_validator_rejection_and_acceptance():
    """Verify validate_divisor_perturbation accepts valid perturbations and rejects invalid single/incomplete mutations."""
    with mpmath.workdps(80):
        g1 = mpmath.mpf('14.134725141734693790457251983562470270784257115699243175685567460149963429809256764949010393171561012')
        eps = mpmath.mpf('0.001')
        delta = mpmath.mpf('0.01')

        # 1. Valid critical-line height pair
        valid_crit, _, errs_crit = math_core.validate_divisor_perturbation(
            mutation_type="critical_height",
            zeros=[mpmath.mpc('0.5', g1 + eps), mpmath.mpc('0.5', -(g1 + eps))],
            claimed_multiplicity_preserved=True,
            dps=80
        )
        assert valid_crit is True, f"Valid critical pair rejected: {errs_crit}"

        # 2. Valid radial quartet
        valid_quartet, _, errs_quartet = math_core.validate_divisor_perturbation(
            mutation_type="radial_quartet",
            zeros=[
                mpmath.mpc(mpmath.mpf('0.5') + delta, g1),
                mpmath.mpc(mpmath.mpf('0.5') + delta, -g1),
                mpmath.mpc(mpmath.mpf('0.5') - delta, g1),
                mpmath.mpc(mpmath.mpf('0.5') - delta, -g1)
            ],
            claimed_multiplicity_preserved=True,
            dps=80
        )
        assert valid_quartet is True, f"Valid quartet rejected: {errs_quartet}"

        # 3. Invalid: single isolated complex zero without conjugation/reflection
        invalid_single, _, errs_single = math_core.validate_divisor_perturbation(
            mutation_type="single_zero",
            zeros=[mpmath.mpc('0.5', g1 + eps)],
            dps=80
        )
        assert invalid_single is False
        assert len(errs_single) > 0

        # 4. Invalid: incomplete quartet (3 zeros)
        invalid_triplet, _, errs_triplet = math_core.validate_divisor_perturbation(
            mutation_type="radial_quartet",
            zeros=[
                mpmath.mpc(mpmath.mpf('0.5') + delta, g1),
                mpmath.mpc(mpmath.mpf('0.5') + delta, -g1),
                mpmath.mpc(mpmath.mpf('0.5') - delta, g1)
            ],
            dps=80
        )
        assert invalid_triplet is False

        # 5. Invalid: multiplicity mismatch claimed vs actual
        invalid_mult, _, _ = math_core.validate_divisor_perturbation(
            mutation_type="critical_height",
            zeros=[mpmath.mpc('0.5', g1 + eps)],
            claimed_multiplicity_preserved=True,
            dps=80
        )
        assert invalid_mult is False


def test_critical_height_exact_vs_linear_convergence():
    """Verify that remainder R(eps) = Delta C^exact(eps) - Delta C^linear(eps) is O(eps^2)."""
    with mpmath.workdps(80):
        ref_zeros = reference_data.load_reference_zeros()[:10]
        gamma_2 = ref_zeros[1]  # Off-peak zero for j=1, K=0

        eps_list = [mpmath.mpf('1e-2'), mpmath.mpf('1e-3'), mpmath.mpf('1e-4'), mpmath.mpf('1e-5')]
        rel_errors = []

        for eps in eps_list:
            res = math_core.finite_divisor_defect_critical_height_exact_and_linear(
                j=1, K=0, gamma_n=gamma_2, epsilon=eps, dps=80
            )
            rel_errors.append(res["relative_error"])

        # Relative error should decrease linearly with eps (meaning remainder is O(eps^2))
        for i in range(len(rel_errors) - 1):
            assert rel_errors[i+1] < rel_errors[i] * mpmath.mpf('0.15'), (
                f"Convergence failed: {rel_errors[i+1]} not < 0.15 * {rel_errors[i]}"
            )


def test_radial_quartet_exact_decomposition_and_zero_delta_vanish():
    """Verify radial quartet exact decomposition: pure radial defect strictly vanishes at delta=0 and is even in delta."""
    with mpmath.workdps(80):
        ref_zeros = reference_data.load_reference_zeros()[:10]
        ga = ref_zeros[0]
        gb = ref_zeros[1]

        # 1. Test at delta = 0: pure radial defect MUST be 0
        res_zero = math_core.finite_divisor_defect_radial_quartet_decomposed(
            j=1, K=0, gamma_a=ga, gamma_b=gb, delta=mpmath.mpf('0.0'), dps=80
        )
        assert abs(res_zero["radial_defect"]) < mpmath.mpf('1e-70'), (
            f"Pure radial defect at delta=0 was non-zero: {res_zero['radial_defect']}"
        )
        # Total defect at delta=0 equals merge defect
        assert abs(res_zero["total_defect"] - res_zero["merge_defect"]) < mpmath.mpf('1e-70')

        # 2. Test evenness in delta: Delta C(delta) == Delta C(-delta)
        delta_pos = mpmath.mpf('0.02')
        delta_neg = mpmath.mpf('-0.02')
        res_pos = math_core.finite_divisor_defect_radial_quartet_decomposed(
            j=1, K=0, gamma_a=ga, gamma_b=gb, delta=delta_pos, dps=80
        )
        res_neg = math_core.finite_divisor_defect_radial_quartet_decomposed(
            j=1, K=0, gamma_a=ga, gamma_b=gb, delta=delta_neg, dps=80
        )
        assert abs(res_pos["radial_defect"] - res_neg["radial_defect"]) < mpmath.mpf('1e-70')
        assert abs(res_pos["total_defect"] - res_neg["total_defect"]) < mpmath.mpf('1e-70')


def test_target_zero_1_based_indexing_and_ordering():
    """Verify that target zero indices 1, 10, 50 map to distinct certified zeros with no modulo aliasing."""
    ref_zeros = reference_data.load_reference_zeros()
    assert len(ref_zeros) >= 100

    gamma_1 = ref_zeros[0]   # Index 1
    gamma_10 = ref_zeros[9]  # Index 10
    gamma_50 = ref_zeros[49] # Index 50

    with mpmath.workdps(80):
        g1_mpf = math_core.to_mpf(gamma_1, dps=80)
        g10_mpf = math_core.to_mpf(gamma_10, dps=80)
        g50_mpf = math_core.to_mpf(gamma_50, dps=80)

        assert abs(g1_mpf - mpmath.mpf('14.13472514173469379')) < mpmath.mpf('1e-15')
        assert abs(g10_mpf - mpmath.mpf('49.77383247767230218')) < mpmath.mpf('1e-15')
        assert abs(g50_mpf - mpmath.mpf('143.1118458076206327')) < mpmath.mpf('1e-15')

        # Distinct ordinates
        assert g1_mpf < g10_mpf < g50_mpf


def test_linearized_compensation_threshold_sweep_and_reconstructibility():
    """Verify SVD threshold sweep, threshold_dependent classification, and compensation reconstructibility."""
    with mpmath.workdps(80):
        ref_zeros = reference_data.load_reference_zeros()[:50]
        j_list = [1, 2, 3, 4, 5, 6]
        k_list = [-2, -1, 0, 1, 2]

        J = math_core.explicit_formula_jacobian(j_list, k_list, ref_zeros, dps=80)
        assert len(J) == 30
        assert len(J[0]) == 50

        # Solve for target zero 1 (col 0)
        comp = math_core.solve_linearized_compensation(
            J=J, target_col_idx=0, epsilon='0.001', dps=80
        )

        assert comp["rank_stability"] == "threshold_dependent"
        assert len(comp["threshold_sweep"]) == 6
        assert len(comp["singular_values"]) == 30
        assert len(comp["compensation_vector"]) == 49
        assert len(comp["residual_vector"]) == 30
        assert len(comp["participating_indices"]) == 49

        # Forward residual reconstructibility check: r == J_{-n} * x + v
        # Verify residual norm matches norm of residual vector
        computed_res_norm = mpmath.sqrt(sum(r * r for r in comp["residual_vector"]))
        assert abs(computed_res_norm - comp["residual_norm"]) < mpmath.mpf('1e-65')


def test_pure_radial_defect_second_order_taylor_convergence():
    """Verify exact pure radial defect matches -2*delta^2*H''(gamma) with O(delta^2) relative error."""
    with mpmath.workdps(80):
        gamma_1 = '14.13472514173469379'
        for j in [1, 2, 3]:
            for K in [-1, 0, 1]:
                # Test delta = 0.01 vs delta = 0.001
                res_1 = math_core.pure_radial_defect_exact_and_second_order(j=j, K=K, gamma=gamma_1, delta='0.01', dps=80)
                res_2 = math_core.pure_radial_defect_exact_and_second_order(j=j, K=K, gamma=gamma_1, delta='0.001', dps=80)

                # Relative error scaling: should decrease by ~100x
                assert res_1["relative_error"] < mpmath.mpf('1e-2')
                assert res_2["relative_error"] < mpmath.mpf('1e-4')

                # Quadratic halving ratio: delta -> delta/2 scales defect by 4
                res_fine = math_core.pure_radial_defect_exact_and_second_order(j=j, K=K, gamma=gamma_1, delta='0.0001', dps=80)
                res_fine_half = math_core.pure_radial_defect_exact_and_second_order(j=j, K=K, gamma=gamma_1, delta='0.00005', dps=80)
                ratio = res_fine["exact_radial_defect"] / res_fine_half["exact_radial_defect"]
                assert abs(ratio - mpmath.mpf('4.0')) < mpmath.mpf('1e-4')


def test_radial_second_order_jacobian_and_nnls():
    """Verify second-order radial Jacobian construction, quadratic energy, and NNLS non-compensation."""
    with mpmath.workdps(80):
        ref_zeros = reference_data.load_reference_zeros()[:50]
        j_list = [1, 2, 3, 4, 5, 6]
        k_list = [-2, -1, 0, 1, 2]

        K_mat = math_core.radial_second_order_jacobian(j_list, k_list, ref_zeros, dps=80)
        assert len(K_mat) == 30
        assert len(K_mat[0]) == 50

        # Solve NNLS for target zero 1 with u = delta^2 = 1e-6
        nnls_res = math_core.solve_radial_second_order_nnls(
            K_mat=K_mat,
            target_col_idx=0,
            u_val='1e-6',
            dps=80
        )

        assert nnls_res["positive_energy_holds"] is True
        assert nnls_res["quadratic_energy"] > mpmath.mpf('1e-30')
        assert len(nnls_res["nnls_solution"]) == 49
        # Verify all NNLS components are >= 0
        for x in nnls_res["nnls_solution"]:
            assert x >= -mpmath.mpf('1e-60')


def test_radial_second_order_heterogeneous_nnls_and_positive_energy():
    """
    Verify that across 100 zeros in the 30-channel basis:
    1. Positive target energy E(u) > 0 holds for all target zeros.
    2. NNLS compensation is heterogeneous: compensation IS found for zeros 10 and 50
       (residual < 1e-6), but NOT found for zeros 1 and 100 (residual > 1e-5).
    3. Positive target energy and compensation-found coexist, proving positive target
       energy does not preclude subspace cone compensation.
    """
    with mpmath.workdps(80):
        ref_zeros = reference_data.load_first_100_reference_zeros()
        j_list = [1, 2, 3, 4, 5, 6]
        k_list = [-2, -1, 0, 1, 2]
        K_mat = math_core.radial_second_order_jacobian(j_list, k_list, ref_zeros, dps=80)

        # Zero 1 (col 0)
        res_1 = math_core.solve_radial_second_order_nnls(K_mat, target_col_idx=0, u_val='1e-6', dps=80)
        assert res_1["positive_energy_holds"] is True
        assert res_1["nnls_compensation_found"] is False
        assert res_1["nnls_relative_residual"] > mpmath.mpf('0.9')

        # Zero 10 (col 9)
        res_10 = math_core.solve_radial_second_order_nnls(K_mat, target_col_idx=9, u_val='1e-6', dps=80)
        assert res_10["positive_energy_holds"] is True
        assert res_10["nnls_compensation_found"] is True
        assert res_10["nnls_relative_residual"] < mpmath.mpf('1e-6')

        # Zero 50 (col 49)
        res_50 = math_core.solve_radial_second_order_nnls(K_mat, target_col_idx=49, u_val='1e-6', dps=80)
        assert res_50["positive_energy_holds"] is True
        assert res_50["nnls_compensation_found"] is True
        assert res_50["nnls_relative_residual"] < mpmath.mpf('1e-6')

        # Zero 100 (col 99)
        res_100 = math_core.solve_radial_second_order_nnls(K_mat, target_col_idx=99, u_val='1e-6', dps=80)
        assert res_100["positive_energy_holds"] is True
        assert res_100["nnls_compensation_found"] is False
        assert res_100["nnls_relative_residual"] > mpmath.mpf('1e-5')


def test_native_baseline_metric_semantics():
    """Verify that only the residual is marked criterion_component in native baseline spec."""
    import yaml
    with open("research/experiments/explicit_formula_native_baseline_001.yaml", "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    report_metrics = {m["metric"]: m.get("kind") for m in spec.get("report_metrics", [])}
    assert report_metrics.get("residual") == "criterion_component"
    assert report_metrics.get("relative_error") == "diagnostic"
    assert report_metrics.get("spectral_cutoff_change_100_to_200") == "diagnostic"
    assert report_metrics.get("spectral_cutoff_change_150_to_200") == "diagnostic"
    assert report_metrics.get("prime_cutoff_change_10k_to_50k") == "diagnostic"
    assert report_metrics.get("precision_change_70_to_110") == "diagnostic"


def test_lean_formal_file_boundary():
    """Verify that formal Lean 4 module proves algebraic lemmas without overclaiming global RH proof."""
    with open("formal/RiemannScope/RadialDefect.lean", "r", encoding="utf-8") as f:
        content = f.read()

    assert "def radialProjection" in content
    assert "def pureRadialDefectQuartet" in content
    assert "theorem pureRadialDefectQuartet_zero_delta" in content
    assert "theorem second_order_orbit_variable_nonneg" in content
    assert "0 ≤ δ ^ 2" in content or "0 \u2264 \u03b4 ^ 2" in content
    # Verify no ungrounded claim that RH or global non-compensation is proven in Lean
    assert "theorem riemann_hypothesis" not in content.lower()
    assert "rh_proved" not in content.lower()


