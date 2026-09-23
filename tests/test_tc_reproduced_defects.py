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
