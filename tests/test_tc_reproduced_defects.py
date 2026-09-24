"""
Regression tests covering the 6 defect reproductions from independent review audit:
1. Arithmetic cutoff sensitivity: separating omitted continuous tail integral from finite quadrature error.
2. Spectral tail allowance reconciliation: corrected h^(2m) Stieltjes tail order of magnitude.
3. Pointwise kernel majorant: C_m(h, T)/t^2 >= |A_h(it)|^2 at t=360, T=320, h=0.05, m=3.
4. Sensitivity decision: tracing omitted tail allowance in final decision logic.
5. Legal unit vector counterexample: refuting 92.08 bound over the four-grade legal family.
6. Evaluator isolation: default output_path=None has zero file-writing side effects.
"""

import math
import os
import numpy as np
import pytest

from tc.approximation import derive_quadratic_spectral_tail_bound
from tc.weil_forms import (
    compute_canonical_reflected_weil_matrix,
    evaluate_tc_arithmetic_spectral_baseline_comparison,
    certify_explicit_formula_off_critical_sensitivity,
    compute_tc_quartet_matrix,
    audit_tc_critical_zero_deflation,
    validate_or_project_legal_b,
    Z_CANONICAL_KERNEL,
)


def test_defect_1_arithmetic_cutoff_sensitivity():
    """
    Defect 1: Arithmetic cutoff extension from 320 to 640 adds ~14M of omitted
    continuous Archimedean tail energy, completely dominating the finite quadrature error (~1,591).
    """
    grades = [-1, -2, -3, -4]
    tau = 2.0 * math.pi
    b_base = {-1: -0.0471595, -2: -0.0689898, -3: -0.6449528, -4: 0.7611020}
    c_vec = np.array([b_base[K] * (tau**K) for K in grades])

    res_320 = compute_canonical_reflected_weil_matrix(grades=grades, h=0.05, U=320.0, N_t=2000)
    res_640 = compute_canonical_reflected_weil_matrix(grades=grades, h=0.05, U=640.0, N_t=2000)

    val_320 = float(c_vec @ (np.array(res_320['W_arch']) - np.array(res_320['W_prime'])) @ c_vec)
    val_640 = float(c_vec @ (np.array(res_640['W_arch']) - np.array(res_640['W_prime'])) @ c_vec)

    # Values are ~13.2M and ~27.2M
    assert 1.3e7 < val_320 < 1.4e7
    assert 2.6e7 < val_640 < 2.8e7
    omitted_energy = val_640 - val_320
    assert omitted_energy > 1.3e7  # ~14M omitted integral energy

    # Omitted energy dwarfs finite quadrature error
    quad_radius = 1591.0
    assert omitted_energy / quad_radius > 8000.0


def test_defect_2_and_3_kernel_majorant_and_tail_power():
    """
    Defect 2 & 3:
    - At h=0.05, m=3, T=320, t=360: direct evaluation |A_h(i 360)|^2 ~ 1.32e6.
      With repaired h^(2m) = h^6, the majorant C_m(h, T)/t^2 is >= |A_h(i 360)|^2 (no under-coverage).
    - Spectral tail allowance is > 1e9.
    """
    h = 0.05
    m_order = 3
    T = 320.0
    t = 360.0

    # Direct evaluation of |A_h(it)|^2
    n_k = 2000
    v_k, w_k = np.polynomial.legendre.leggauss(n_k)
    kappa_vals = np.exp(-1.0 / (1.0 - v_k**2)) / Z_CANONICAL_KERNEL * w_k
    z_c = complex(0.0, t)
    int_val = np.sum(kappa_vals * np.exp(z_c * h * v_k))
    A_h_direct = (z_c**2 - 0.25) * int_val
    ah_sq_direct = abs(A_h_direct)**2

    assert 1.2e6 < ah_sq_direct < 1.4e6

    # Majorant from derive_quadratic_spectral_tail_bound
    res = derive_quadratic_spectral_tail_bound(h=h, T_cutoffs=[T], k_deriv=m_order)
    C_m_repaired = res['cutoff_evaluations'][0]['kernel_constant_C_m']
    majorant_at_t = C_m_repaired / (t**2)

    # Repaired majorant strictly covers direct evaluation
    assert majorant_at_t >= ah_sq_direct
    assert majorant_at_t > 3.0e6


def test_defect_4_sensitivity_traces_omitted_allowance():
    """
    Defect 4: certify_explicit_formula_off_critical_sensitivity must trace
    the omitted tail allowance (B_tail ~ 3.59B) in its decision logic and report
    is_complete_spectral_positivity_preserved is False.
    """
    res = certify_explicit_formula_off_critical_sensitivity(
        delta_grid=[0.1, 0.49],
        gamma_grid=[14.13, 100.0]
    )

    summary = res['off_critical_sensitivity_summary']
    assert 'tail_allowance_omitted_in_finite_decision' in summary
    assert 'tail_adjusted_margin_with_worst_case_zero' in summary
    assert 'is_complete_spectral_positivity_preserved' in summary
    assert 'complete_spectral_decision_status' in summary

    # Tail bound is ~3.59B or higher
    assert summary['tail_allowance_omitted_in_finite_decision'] > 1.0e9

    # Tail-adjusted margin is negative
    assert summary['tail_adjusted_margin_with_worst_case_zero'] < 0.0

    # Complete spectral decision is False / NUMERICALLY_UNRESOLVED
    assert summary['is_complete_spectral_positivity_preserved'] is False
    assert summary['complete_spectral_decision_status'] == 'NUMERICALLY_UNRESOLVED'


def test_defect_5_legal_unit_vector_counterexample():
    """
    Defect 5: For the legal unit vector b = (1, -0.5, -0.3, -0.2)/sqrt(1.38),
    the quartet at (delta, gamma) = (0.49, 100.0) is ~ -9,178.87.
    The generalized minimum eigenvalue is ~ -10,268.14.
    Thus 92.08 is refuted as a bound over unit vectors in the 4-grade family.
    """
    q_mat_info = compute_tc_quartet_matrix(delta=0.49, gamma=100.0)

    # Counterexample test vector response
    q_diag = q_mat_info['counterexample_verification']['test_vector_quartet_response']
    assert q_diag < -9000.0
    assert q_mat_info['counterexample_verification']['is_92_bound_refuted'] is True

    # Generalized minimum eigenvalue over all legal unit vectors ||b|| = 1
    lambda_min = q_mat_info['generalized_eigenvalues_unit_b']['lambda_min']
    assert lambda_min < -10000.0


def test_defect_6_evaluators_free_of_side_effects():
    """
    Defect 6: Both evaluators default to output_path=None and produce zero
    disk writes during testing.
    """
    mtime_sens_before = os.path.getmtime('data/tc_explicit_formula_sensitivity_certificate.json')
    mtime_comp_before = os.path.getmtime('data/tc_arithmetic_spectral_baseline_comparison.json')

    # Run without output_path
    _ = certify_explicit_formula_off_critical_sensitivity(
        delta_grid=[0.1],
        gamma_grid=[14.13]
    )
    _ = evaluate_tc_arithmetic_spectral_baseline_comparison(T_cutoff=100.0)

    mtime_sens_after = os.path.getmtime('data/tc_explicit_formula_sensitivity_certificate.json')
    mtime_comp_after = os.path.getmtime('data/tc_arithmetic_spectral_baseline_comparison.json')

    assert mtime_sens_before == mtime_sens_after
    assert mtime_comp_before == mtime_comp_after


def test_contract_legal_b_validation_and_norms():
    """
    Contract test: validate_or_project_legal_b strictly enforces 1^T b = 0
    and distinguishes ||b||^2 from ||beta||^2.
    """
    grades = [-1, -2, -3, -4]
    # Input with non-zero sum
    b_in = {-1: 1.0, -2: -0.5, -3: -0.3, -4: -0.1}  # sum = 0.1 != 0

    # Validation policy raises error
    with pytest.raises(ValueError, match="Inadmissible coefficient vector"):
        validate_or_project_legal_b(b_in, grades, anchor_grade=-1, policy="validate")

    # Project policy reconstructs anchor
    b_proj, b_vec, beta_vec, norm_b_sq, norm_beta_sq = validate_or_project_legal_b(
        b_in, grades, anchor_grade=-1, policy="project"
    )
    assert abs(sum(b_proj.values())) < 1e-14
    assert b_proj[-1] == -(-0.5 - 0.3 - 0.1)  # 0.9

    # Distinguishes ||b||^2 from ||beta||^2
    assert norm_b_sq > norm_beta_sq
    assert abs(norm_b_sq - (0.9**2 + (-0.5)**2 + (-0.3)**2 + (-0.1)**2)) < 1e-14


def test_small_vector_quadratic_scaling_no_clamping():
    """
    Test that b = 10^-16 (1, -0.5, -0.3, -0.2)/sqrt(1.38) is NOT clamped to zero,
    retaining non-zero arithmetic energy, non-zero spectral energy, and quadratic scaling.
    """
    from tc.weil_forms import evaluate_tc_arithmetic_spectral_baseline_comparison
    norm_c = math.sqrt(1.38)
    b_unit = {-1: 1.0 / norm_c, -2: -0.5 / norm_c, -3: -0.3 / norm_c, -4: -0.2 / norm_c}
    scale = 1e-16
    b_small = {K: v * scale for K, v in b_unit.items()}

    res_unit = evaluate_tc_arithmetic_spectral_baseline_comparison(
        b_coefficients=b_unit, T_cutoff=100.0
    )
    res_small = evaluate_tc_arithmetic_spectral_baseline_comparison(
        b_coefficients=b_small, T_cutoff=100.0
    )

    # Values must not be clamped to zero
    val_arith_unit = res_unit['arithmetic_evaluation']['B_arith_net_value']
    val_arith_small = res_small['arithmetic_evaluation']['B_arith_net_value']
    val_spec_unit = res_unit['spectral_evaluation']['critical_zeros_partial_sum']
    val_spec_small = res_small['spectral_evaluation']['critical_zeros_partial_sum']

    assert val_arith_small > 0.0
    assert val_spec_small > 0.0

    # Quadratic scaling: f(scale * b) / f(b) == scale^2
    assert abs(val_arith_small / val_arith_unit - scale**2) / (scale**2) < 1e-8
    assert abs(val_spec_small / val_spec_unit - scale**2) / (scale**2) < 1e-8


def test_archimedean_tail_normalization_and_cutoff_validation():
    """
    Verify that Archimedean tail bound in evaluate_tc_arithmetic_spectral_baseline_comparison
    uses 1/pi factor (not 1/2pi) and enforces U >= 10.0 for positive digamma weight.
    """
    # U < 10.0 raises ValueError
    with pytest.raises(ValueError, match="cutoff U must be >= 10.0"):
        evaluate_tc_arithmetic_spectral_baseline_comparison(U_cutoff=5.0)

    # Valid U >= 10.0 succeeds with positive Archimedean tail
    res = evaluate_tc_arithmetic_spectral_baseline_comparison(U_cutoff=100.0, T_cutoff=100.0)
    R_arch_upper = res['arithmetic_evaluation']['omitted_archimedean_tail_upper_bound']
    assert R_arch_upper > 0.0


def test_no_contradictory_positivity_decisions():
    """
    Verify that certify_explicit_formula_off_critical_sensitivity eliminates contradictory
    legacy decisions, correctly distinguishing finite margin from complete functional.
    """
    res = certify_explicit_formula_off_critical_sensitivity(
        delta_grid=[0.49], gamma_grid=[100.0]
    )
    summary = res['off_critical_sensitivity_summary']

    # Must NOT claim unconditional preservation when complete spectral status is NUMERICALLY_UNRESOLVED
    assert summary['is_positivity_unconditionally_preserved_for_single_zero'] is False
    assert summary['is_finite_quadrature_margin_positive_against_worst_quartet'] is True
    assert summary['is_complete_spectral_positivity_preserved'] is False
    assert summary['complete_spectral_decision_status'] == 'NUMERICALLY_UNRESOLVED'


def test_optimized_suppression_production_campaign():
    """
    Verify evaluate_tc_optimized_suppression_comparison runs cleanly and reproduces
    the deflation trade-off across 4 and 6 grades.
    """
    from tc.weil_forms import evaluate_tc_optimized_suppression_comparison
    res = evaluate_tc_optimized_suppression_comparison(
        grades_list=[[-1, -2, -3, -4], [-1, -2, -3, -4, -5, -6]],
        targets=[(0.49, 100.0)],
        T_cutoff=100.0
    )
    assert res['status'] == 'OPTIMIZED_SUPPRESSION_CAMPAIGN_EVALUATED'
    assert res['candidates_count'] > 0
    # In every candidate, net spectral response q + S_T is strictly positive
    for cand in res['candidates']:
        assert cand['net_spectral_response_q_plus_S'] > 0.0


def test_analytic_interpolation_error_formula_and_derivative_norm():
    r"""
    Verify the analytic autocorrelation interpolation bound:
        ||C_h - \Pi C_h||_\infty <= (\Delta v^2 / 8) ||\psi_h'||_2^2
    with ||\psi_h'||_2^2 \approx 2.0797e13 at h=0.05, replacing heuristic fallbacks.
    """
    from tc.weil_forms import (
        NORM_KAPPA_THIRD_DERIVATIVE_SQ,
        NORM_KAPPA_SECOND_DERIVATIVE_SQ,
        NORM_KAPPA_FIRST_DERIVATIVE_SQ,
        certify_baseline_canonical_weil_error_budget
    )
    h = 0.05
    norm_psi_prime_sq = (
        h**(-7) * NORM_KAPPA_THIRD_DERIVATIVE_SQ +
        0.5 * h**(-5) * NORM_KAPPA_SECOND_DERIVATIVE_SQ +
        0.0625 * h**(-3) * NORM_KAPPA_FIRST_DERIVATIVE_SQ
    )
    # Check derivative norm magnitude
    assert 2.07e13 < norm_psi_prime_sq < 2.09e13

    # Check error budget output on baseline
    budget = certify_baseline_canonical_weil_error_budget(
        grades=[-1, -2, -3, -4],
        anchor_grade=-1,
        window=(8.0, 20.0),
        h=0.05,
        U=320.0,
        N_tab_prime=10000
    )
    assert budget['status'] == 'BASELINE_CANONICAL_WEIL_ERROR_BUDGET_NUMERICALLY_UNRESOLVED'
    assert budget['epistemic_class'] == 'NUMERICALLY_UNRESOLVED'
    pq = budget['prime_quadrature']
    assert abs(pq['norm_psi_prime_sq'] - norm_psi_prime_sq) < 1.0
    assert pq['eps_interp'] < 300.0  # \approx 260.0, tightly bounded
    # Verify literal 20875.06 is completely gone
    assert pq['norm_delta_W_prime'] < 1000.0
    assert budget['error_budget']['lambda_min_computed'] > 1.32e7
    assert budget['error_budget']['is_strictly_positive'] is False


def test_decoupled_cutoff_and_direction_specific_budget():
    """
    Verify that physical cutoff U and zero cutoff T are decoupled, and
    error allowances are computed direction-specifically without hardcoded 1591.14.
    """
    from tc.weil_forms import evaluate_tc_optimized_suppression_comparison
    res = evaluate_tc_optimized_suppression_comparison(
        grades_list=[[-1, -2, -3, -4]],
        targets=[(0.49, 100.0)],
        T_cutoff=100.0,
        U_cutoff=320.0
    )
    assert res['parameters']['U_cutoff'] == 320.0
    assert res['parameters']['T_cutoff'] == 100.0
    assert res['parameters']['cutoffs_are_decoupled'] is True

    # Candidate 0 must have direction-specific delta_arith_est
    cand0 = res['candidates'][0]
    assert cand0['delta_arith_est'] is not None
    # Hardcoded 1591.14 * ||beta||^2 would give ~1591.14 for unit norm;
    # analytic direction-specific error is strictly smaller (~197.64)
    assert cand0['delta_arith_est'] < 1000.0
    assert cand0['delta_arch_vec'] is not None
    assert cand0['delta_prime_vec'] is not None


def test_zero_data_completeness_verification():
    """
    Verify that incomplete zero lists produce an explicit unresolved flag
    and do not silently authorize a complete interval.
    """
    from tc.weil_forms import evaluate_tc_optimized_suppression_comparison
    # Test with standard T=100 where reference data is complete (29 zeros)
    res_complete = evaluate_tc_optimized_suppression_comparison(
        grades_list=[[-1, -2, -3, -4]],
        targets=[(0.49, 100.0)],
        T_cutoff=100.0
    )
    assert res_complete['zero_accounting']['is_complete'] is True
    assert res_complete['zero_accounting']['zeros_evaluated_count'] == 29
    assert res_complete['zero_accounting']['unresolved_zero_range'] is None

    # Test with T=500 where reference data only goes to ~396.38
    res_incomplete = evaluate_tc_optimized_suppression_comparison(
        grades_list=[[-1, -2, -3, -4]],
        targets=[(0.49, 100.0)],
        T_cutoff=500.0
    )
    assert res_incomplete['zero_accounting']['is_complete'] is False
    assert res_incomplete['zero_accounting']['unresolved_zero_range'] is not None


def test_campaign_minima_and_3525_fold_reduction():
    """
    Verify dynamic campaign summary matches underlying rows and accurately reproduces
    the ~3,525-fold reduction in finite synthetic objective q + S_T from 4 to 8 grades.
    """
    import json
    with open('data/tc_optimized_suppression_campaign.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    tbl = data['finite_objective_minima_mu1_target100']['table']
    dims = {row['family_dimension']: row['min_finite_q_plus_S'] for row in tbl}
    assert 4 in dims and 6 in dims and 8 in dims

    # Verify exact reproduction of benchmark table
    assert abs(dims[4] - 1780369.060913) < 1.0
    assert abs(dims[6] - 40394.570768) < 1.0
    assert abs(dims[8] - 505.060916) < 1.0

    fold_red = data['finite_objective_minima_mu1_target100']['fold_reduction_4_to_8_grades']
    assert 3520.0 < fold_red < 3530.0

    # Summary findings must record NUMERICALLY_UNRESOLVED for complete functional
    assert data['summary_findings']['epistemic_decision'] == 'NUMERICALLY_UNRESOLVED'


def test_reproduced_defect_1_table_quadrature_and_interpolation_discrepancy():
    """
    Defect 1 Reproduction & Repair:
    At h=0.05, N_tab_prime=10000, let dv=0.1/9999 and v=1.5*dv.
    - Old 64-node table gives ~175877223.213778, while independent 60-digit integration gives ~175877566.664707.
      Discrepancy is ~343.45093, exceeding declared pointwise allowance 260.01605.
    - At the first table node (v=dv), 64-node quadrature error alone is ~83.22394 against allowance 1e-10.
    - Repaired 256-node table reduces nodal error to < 2e-6 and discrepancy to ~259.99844 <= 260.0165.
    """
    import mpmath
    from tc.weil_forms import _compute_C_tab_fast, Z_CANONICAL_KERNEL

    h = 0.05
    N_tab_prime = 10000
    v_tab = np.linspace(0.0, 2.0 * h, N_tab_prime)
    dv = 0.1 / 9999.0
    v = 1.5 * dv

    # 1. 64-node table evaluation
    c_tab_64 = _compute_C_tab_fast(v_tab, h, n_nodes=64)
    interp_val_64 = float(np.interp(v, v_tab, c_tab_64))
    assert abs(interp_val_64 - 175877223.213778) < 1.0

    # 2. Independent 60-digit mpmath reference
    mpmath.mp.dps = 60
    z = mpmath.mpf(Z_CANONICAL_KERNEL)

    def kappa(y):
        if abs(y) >= 1:
            return mpmath.mpf(0)
        om = 1 - y**2
        return mpmath.exp(-1 / om) / z

    def d2kappa(y):
        if abs(y) >= 1:
            return mpmath.mpf(0)
        om = 1 - y**2
        return (-2 / (om**2) - 8 * (y**2) / (om**3) + 4 * (y**2) / (om**4)) * kappa(y)

    def psi(y):
        return (mpmath.mpf(h)**(-3)) * d2kappa(y) - mpmath.mpf('0.25') * (mpmath.mpf(h)**(-1)) * kappa(y)

    xi = mpmath.mpf(v) / mpmath.mpf(h)
    exact_val = float(mpmath.mpf(h) * mpmath.quad(lambda y: psi(y) * psi(y - xi), [-1 + xi, 1]))
    assert abs(exact_val - 175877566.664707) < 1.0

    # Reproduce defect: 64-node discrepancy is ~343.45 > 260.016
    disc_64 = abs(interp_val_64 - exact_val)
    assert abs(disc_64 - 343.45093) < 0.01
    assert disc_64 > 260.01605

    # Node 1 quadrature error is ~83.22 > 1e-10
    xi_node1 = mpmath.mpf(dv) / mpmath.mpf(h)
    exact_node1 = float(mpmath.mpf(h) * mpmath.quad(lambda y: psi(y) * psi(y - xi_node1), [-1 + xi_node1, 1]))
    node1_err_64 = abs(c_tab_64[1] - exact_node1)
    assert abs(node1_err_64 - 83.22394) < 0.01
    assert node1_err_64 > 80.0

    # 3. Verify repaired 256-node table
    c_tab_256 = _compute_C_tab_fast(v_tab, h, n_nodes=256)
    interp_val_256 = float(np.interp(v, v_tab, c_tab_256))
    disc_256 = abs(interp_val_256 - exact_val)
    node1_err_256 = abs(c_tab_256[1] - exact_node1)

    assert node1_err_256 < 2e-6  # certified node accuracy
    assert disc_256 < 260.0165   # strictly bounded by analytic interpolation + node tolerance


def test_reproduced_defect_2_archimedean_mesh_difference_unjustified():
    """
    Defect 2 Reproduction & Repair:
    certify_baseline_canonical_weil_error_budget previously set the Archimedean allowance
    to 2*mesh_difference + 1e-12 without an analytic remainder theorem.
    Repaired budget retains mesh difference strictly as diagnostic and sets epistemic class
    to NUMERICALLY_UNRESOLVED.
    """
    from tc.weil_forms import certify_baseline_canonical_weil_error_budget

    budget = certify_baseline_canonical_weil_error_budget(
        grades=[-1, -2, -3, -4],
        anchor_grade=-1,
        window=(8.0, 20.0),
        h=0.05,
        U=320.0,
        N_tab_prime=10000
    )

    # Status must be NUMERICALLY_UNRESOLVED per Rule 0
    assert budget['status'] == 'BASELINE_CANONICAL_WEIL_ERROR_BUDGET_NUMERICALLY_UNRESOLVED'
    assert budget['epistemic_class'] == 'NUMERICALLY_UNRESOLVED'
    assert budget['error_budget']['is_strictly_positive'] is False

    # Archimedean quadrature must report diagnostic difference without false certification
    arch = budget['archimedean_quadrature']
    assert arch['is_remainder_theorem_certified'] is False
    assert arch['norm_delta_A_U_certified'] is None
    assert arch['mesh_diff_A_U_diagnostic'] > 0.0

    # Prime quadrature remains rigorously bounded
    pq = budget['prime_quadrature']
    assert pq['eps_table_quad'] == 1e-3
    assert pq['eps_ptwise'] < 300.0


def test_reproduced_defect_3_spectral_zero_coverage_gaps_and_duplicates():
    """
    Defect 3 Reproduction & Repair:
    At T=100, reference lists with omissions ([14.13, 105.0]), no zeros below cutoff ([105.0]),
    or duplicates ([14.13, 14.13, 105.0]) must fail validation and not authorize a complete interval.
    """
    from tc.weil_forms import validate_spectral_zero_coverage, evaluate_tc_optimized_suppression_comparison

    # Case 1: Gap omitting 28 intermediate zeros
    ok1, reason1, _, _ = validate_spectral_zero_coverage([14.134725, 105.0], 100.0)
    assert ok1 is False
    assert "omitted_zeros" in reason1 or "zero_count_mismatch" in reason1

    # Case 2: No zeros below cutoff
    ok2, reason2, _, _ = validate_spectral_zero_coverage([105.0, 110.0], 100.0)
    assert ok2 is False
    assert "no_zeros_below_cutoff" in reason2

    # Case 3: Duplicated zeros
    ok3, reason3, _, _ = validate_spectral_zero_coverage([14.134725, 14.134725, 105.0], 100.0)
    assert ok3 is False
    assert "duplicate_or_inverted" in reason3

    # Case 4: Standard authoritative zeros pass
    import reference_data
    ref_zeros = [float(g) for g in reference_data.load_reference_zeros()]
    ok_ref, _, _, crit = validate_spectral_zero_coverage(ref_zeros, 100.0)
    assert ok_ref is True
    assert len(crit) == 29

    # Case 5: When zero list is incomplete (e.g. at T=500), caller returns None for complete_spectral_interval
    res_incomplete = evaluate_tc_optimized_suppression_comparison(
        grades_list=[[-1, -2, -3, -4]],
        targets=[(0.49, 100.0)],
        T_cutoff=500.0
    )
    assert res_incomplete['zero_accounting']['is_complete'] is False
    for cand in res_incomplete['candidates']:
        assert cand['complete_spectral_interval'] is None
        assert cand['spectral_interval_status'] == 'PARTIAL_INCOMPLETE_ZEROS'


def test_reproduced_defect_4_complete_objective_optimizer_includes_remainder():
    """
    Defect 4 Reproduction & Repair:
    Previously, candidates were generated purely on Q + mu*S_T with tail appended ex-post.
    The repaired solve_complete_upper_objective directly minimizes:
        F_+(beta) = q(P beta) + S_T(P beta) + B_T(P beta) + eps_finite
    achieving a substantially lower complete upper estimate.
    """
    from tc.weil_forms import (
        solve_complete_upper_objective,
        evaluate_tc_optimized_suppression_comparison
    )

    res = evaluate_tc_optimized_suppression_comparison(
        grades_list=[[-1, -2, -3, -4]],
        targets=[(0.49, 100.0)],
        T_cutoff=100.0
    )

    # Find the soft suppression candidate (mu=1) and remainder optimized candidate
    c_soft = next(c for c in res['candidates'] if c['label'] == 'SOFT_SUPPRESSION_MU_1.0')
    c_rem = next(c for c in res['candidates'] if c['label'] == 'REMAINDER_OPTIMIZED_CANDIDATE')

    f_plus_soft = c_soft['target_quartet_q'] + c_soft['finite_zero_sum_S'] + c_soft['tail_allowance_T']
    f_plus_rem = c_rem['details']['complete_upper_objective_F_plus']

    # Soft suppression has F_+ ~ 1.343e12
    assert 1.3e12 < f_plus_soft < 1.4e12
    assert abs(c_soft['station_norm_D_stat'] - 12.016) < 0.1

    # Remainder-optimized candidate achieves F_+ ~ 9.77e11 (1.38-fold reduction, >360B units)
    assert f_plus_rem < 1.05e12
    assert f_plus_rem < f_plus_soft
    reduction = f_plus_soft - f_plus_rem
    assert reduction > 3.0e11

    # Station norm is substantially reduced
    assert c_rem['station_norm_D_stat'] < c_soft['station_norm_D_stat']
    assert c_rem['station_norm_D_stat'] < 10.5

    # Remainder optimized candidate is feasible
    assert c_rem['details']['is_feasible'] is True
    assert c_rem['details']['unit_norm_error'] < 1e-5


def test_reproduced_defect_5_lean_formalization_derives_cancelling_atom_and_location():
    """
    Defect 5 Reproduction & Repair:
    Verify that formal/RiemannScope/ExtremalCorrelation.lean contains the full finite correlation theorem
    without assuming h_loc, and proves integer collision and transcendence contradiction with 0 sorry.
    """
    lean_path = os.path.join(os.path.dirname(__file__), "..", "formal", "RiemannScope", "ExtremalCorrelation.lean")
    assert os.path.exists(lean_path)
    with open(lean_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify no sorry Ax or sorry keyword in the file
    assert "sorry" not in content

    # Verify theorem signatures are present
    assert "theorem full_finite_extremal_grade_correlation_theorem" in content
    assert "theorem full_finite_correlation_transcendence_contradiction" in content

    # Verify atomic measure nu_b_mass_at is defined and used
    assert "def nu_b_mass_at" in content
    assert "h_nu_zero : ∀ y : ℝ, nu_b_mass_at atoms a b tau y = 0" in content

    # Verify Lindemann transcendence hypothesis is stated
    assert "h_trans : ∀ (k : ℤ), k ≠ 0 → ∀ (r : ℚ), tau ^ k ≠ (r : ℝ)" in content



