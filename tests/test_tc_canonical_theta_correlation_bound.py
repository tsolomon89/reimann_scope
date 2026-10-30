"""
Tests for EPIC-TC-042 / TASK-TC-042: Canonical Theta Correlation Bound —
Arithmetic Derivation, Certified Tests, and a Proof Attempt.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from flint import acb, arb
import pytest

from tc.canonical_theta_correlation_bound import (
    ARITHMETIC_SPECTRAL_ENCLOSURES_INTERSECT_ON_GRID,
    CANONICAL_THETA_CORRELATION_LEAN_DEFS,
    CANONICAL_THETA_CORRELATION_LEAN_THEOREMS,
    CLOSED_FORM_AUTOCORRELATION_PROVED,
    CROSS_GRADE_MOEBIUS_RECOVERY_STATUS,
    DEFAULT_ARTIFACT_PATH,
    EPIC_TC_042_ID,
    FINITE_GRID_CORRELATION_BOUND_CERTIFIED,
    FIXED_SEED_RH_EQUIVALENCE_PROVED,
    GENERIC_WIDTH_AND_BASE_SCALING_PROVED,
    INDEPENDENT_REVIEW_STATUS,
    LEAN_MODULE_PATH,
    LOCAL_ORIGIN_CONCAVITY_CERTIFIED,
    POINTWISE_KERNEL_DIFFERENCE_SIGN_FALSIFIED,
    SEED_DEFECT_REPRODUCED_AND_REPAIRED,
    SUBGATE_TC_042A_ID,
    SUBGATE_TC_042A_STATUS,
    STARTING_HEAD_TC_045R2,
    TASK_TC_042_ID,
    TASK_TC_045_ID,
    TASK_TC_045R_ID,
    TASK_TC_045R2_ID,
    UNIVERSAL_ARITHMETIC_CORRELATION_BOUND_OPEN,
    audit_rh_equivalence_and_laplace_resolvent,
    compute_unconditional_spectral_tail_bound_arb,
    derive_closed_form_autocorrelation_h_K,
    derive_seed_spatial_polynomial_and_mellin,
    evaluate_a_rho_acb,
    evaluate_c_tau_arithmetic_certified,
    evaluate_c_tau_spectral_certified,
    evaluate_f_tau_acb,
    evaluate_finite_toeplitz_gram_matrices,
    evaluate_h0_arb,
    evaluate_h_K_arb,
    evaluate_local_concavity_and_derivatives_at_zero,
    evaluate_synthetic_off_critical_quartet_controls,
    evaluate_tau_scaling_controls,
    serialize_arb_certified,
    verify_all_serialized_arb_in_tree,
    verify_canonical_theta_correlation_lean_module,
    verify_serialized_arb_roundtrip,
)


@pytest.fixture(scope="module")
def artifact_payload():
    assert DEFAULT_ARTIFACT_PATH.exists(), (
        f"Expected artifact {DEFAULT_ARTIFACT_PATH} to exist"
    )
    return json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. Seed Defect Reproduction & Exact Mellin Transform (Section 2)
# ---------------------------------------------------------------------------


def test_01_seed_spatial_polynomial_reproduction_and_tc036r_defect():
    """Verify P(D) G_t and P(D)^2 G_t spatial polynomials and defective TC-036R diagnosis."""
    res = derive_seed_spatial_polynomial_and_mellin()
    assert res["status"] == SEED_DEFECT_REPRODUCED_AND_REPAIRED
    assert res["first_order_matches_r2_minus_3_2_r"] is True
    assert res["second_order_matches_r4_minus_7r3_plus_41_4_r2_minus_9_4_r"] is True
    assert res["exact_polynomial_coefficients_r1_to_r4"] == [
        "-9/4",
        "41/4",
        "-7",
        "1",
    ]
    assert res["defective_tc036r_polynomial_coefficients_r1_to_r4"] == [
        "-3/8",
        "45/8",
        "-6",
        "1",
    ]
    assert res["exact_pochhammer_identity_verified"] is True
    assert res["centered_z_pochhammer_identity_verified"] is True
    assert res["defective_pochhammer_at_s_eq_1"] == "-21/32"
    assert res["defective_fails_at_s_eq_1"] is True


def test_02_f_tau_mellin_transform_endpoints_and_strip_nonvanishing():
    """Verify F_tau(s) vanishes at s = 0, 1, matches quadrature, and is nonvanishing on 0 < Re(s) < 1."""
    res = derive_seed_spatial_polynomial_and_mellin()
    ep = res["endpoint_values"]
    assert ep["F_tau_at_0"] == 0.0
    assert math.isclose(ep["F_tau_deriv_at_0"], 1.0 / 16.0, abs_tol=1e-15)
    assert ep["F_tau_at_1"] == 0.0
    assert ep["F_tau_deriv_at_1"] == 0.0
    assert (
        res["critical_strip_nonvanishing"][
            "nonvanishing_on_open_strip_0_lt_Re_s_lt_1"
        ]
        is True
    )
    assert res["mellin_quadrature_verification"]["max_abs_err"] < 1e-40

    # Direct Acb check at s = 1 and on the critical strip s = 1/2 + 14.1347i
    f_at_1 = evaluate_f_tau_acb(acb(1))
    assert float(abs(f_at_1).upper()) == 0.0
    rho_1 = acb(arb("0.5"), arb("14.13472514173469379"))
    a_rho_1 = evaluate_a_rho_acb(rho_1)
    assert float(a_rho_1.real.lower()) > 1e-4


# ---------------------------------------------------------------------------
# 2. Exact Closed-Form Autocorrelation h_K(x) = h_0(tau^K x) (Section 3 & 6)
# ---------------------------------------------------------------------------


def test_03_closed_form_autocorrelation_h_K_and_symmetry():
    """Verify closed-form h_0(alpha) formula, inversion symmetry h_0(1/alpha) = h_0(alpha), and quadrature."""
    res = derive_closed_form_autocorrelation_h_K()
    assert res["status"] == CLOSED_FORM_AUTOCORRELATION_PROVED
    assert res["palindromic_polynomial_verified"] is True
    assert res["symmetric_W_numerator_verified"] is True
    assert res["numerator_at_W_eq_4"] == 92193
    assert res["inversion_symmetry_h0_inv_eq_h0"] is True
    assert res["quadrature_verification"]["max_convolution_abs_err"] < 1e-40
    assert res["quadrature_verification"]["max_inversion_symmetry_abs_err"] < 1e-42

    # Direct Arb check of h_0(1) = 92193 / (131072 * sqrt(2)) and h_K(1/x) = h_{-K}(x)
    from flint import ctx as flint_ctx
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        h0_1 = evaluate_h0_arb(arb(1))
        expected_h0_1 = arb(92193) / (arb(131072) * arb(2).sqrt())
        assert h0_1.overlaps(expected_h0_1)
        assert float(abs(h0_1 - expected_h0_1).upper()) < 1e-70

        K_arb = arb("0.375")
        x_arb = arb("2.3")
        h_pos_inv = evaluate_h_K_arb(K_arb, arb(1) / x_arb)
        h_neg_x = evaluate_h_K_arb(-K_arb, x_arb)
        assert h_pos_inv.overlaps(h_neg_x)
        assert float(abs(h_pos_inv - h_neg_x).upper()) < 1e-70
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 3. Fixed-Seed RH Equivalence & Laplace Resolvent Audit (Sections 4 & 5)
# ---------------------------------------------------------------------------


def test_04_rh_equivalence_and_laplace_resolvent_proof_steps():
    """Verify all 6 steps of the Laplace-resolvent equivalence proof are recorded and complete."""
    res = audit_rh_equivalence_and_laplace_resolvent()
    assert res["status"] == FIXED_SEED_RH_EQUIVALENCE_PROVED
    steps = res["laplace_resolvent_proof_steps"]
    for key in (
        "step_1_density_and_continuity",
        "step_2_normal_convergence_of_partial_fractions",
        "step_3_right_half_plane_holomorphy_from_bound",
        "step_4_nonvanishing_simple_pole_residue",
        "step_5_functional_equation_reflection",
        "step_6_converse_under_rh",
    ):
        assert key in steps and len(steps[key]) > 40


# ---------------------------------------------------------------------------
# 4. Certified Spectral & Arithmetic Evaluators & Grade Grid (Sections 6 & 7)
# ---------------------------------------------------------------------------


def test_05_unconditional_spectral_and_arithmetic_evaluators_at_zero_and_quarter():
    """Verify unconditional spectral tail bound uses delta_max = 0.5 and arithmetic/spectral routes overlap."""
    tail_0 = compute_unconditional_spectral_tail_bound_arb(arb(0), T_cutoff=arb(100))
    tail_8 = compute_unconditional_spectral_tail_bound_arb(arb(8), T_cutoff=arb(100))
    assert 0.0 < float(tail_0.upper()) < 1e-53
    assert 0.0 < float(tail_8.upper()) < 1e-50

    sp_0 = evaluate_c_tau_spectral_certified(0)
    ar_0 = evaluate_c_tau_arithmetic_certified(0, n_primes_max=6000)
    assert sp_0["unconditional_delta_max_used_in_tail"] == 0.5
    assert sp_0["enclosure_arb"].overlaps(ar_0["enclosure_arb"])
    assert sp_0["lower"] > 0.0009504
    assert ar_0["lower"] > 0.0009504


def test_06_grade_grid_enclosures_delta_positivity_and_evenness(artifact_payload):
    """Verify full grade grid evaluations in artifact have intersecting enclosures, Delta_tau(K) > 0, and evenness."""
    grid = artifact_payload["section_6_7_certified_grade_grid_and_controls"][
        "grade_grid_evaluation"
    ]
    assert grid["status"] == ARITHMETIC_SPECTRAL_ENCLOSURES_INTERSECT_ON_GRID
    assert grid["bound_certification_status"] == FINITE_GRID_CORRELATION_BOUND_CERTIFIED
    assert grid["C_tau_0_spectral"]["certified_strictly_positive"] is True
    assert grid["C_tau_0_arithmetic"]["certified_strictly_positive"] is True
    assert grid["all_enclosures_intersect"] is True
    assert grid["all_nonzero_delta_spectral_certified_positive"] is True
    assert grid["all_monotone_regime_delta_arithmetic_certified_positive"] is True
    assert grid["max_evenness_abs_diff"] < 1e-15

    labels = [row["grade_label"] for row in grid["grade_evaluations"]]
    for expected_label in (
        "0",
        "1/8",
        "1/4",
        "1/2",
        "1",
        "sqrt(2)",
        "2",
        "4",
        "8",
        "-1/4",
        "-1/2",
        "-1",
        "-sqrt(2)",
        "-2",
    ):
        assert expected_label in labels


def test_07_local_concavity_and_derivatives_at_zero():
    """Verify C_tau''(0) < 0, archimedean dominance near K = 0, and certified concavity radius K_loc > 0.05."""
    conc = evaluate_local_concavity_and_derivatives_at_zero()
    assert conc["status"] == LOCAL_ORIGIN_CONCAVITY_CERTIFIED
    assert conc["C_tau_prime_0_exact"] == 0.0
    assert conc["C_tau_double_prime_0_certified_negative"] is True
    assert conc["C_tau_double_prime_0_upper"] < -0.641
    assert conc["C_tau_fourth_deriv_0_mid"] > 400.0
    assert conc["certified_local_concavity_radius_K_loc"] > 0.05
    assert (
        conc["arithmetic_second_derivative_decomposition"][
            "both_prime_and_completed_archimedean_concave_at_zero"
        ]
        is True
    )


def test_08_finite_toeplitz_gram_matrices_positive_definite():
    """Verify finite Toeplitz Gram matrices on rational and algebraic grids are strictly positive-definite."""
    gram = evaluate_finite_toeplitz_gram_matrices()
    assert gram["all_gram_matrices_positive_definite"] is True
    assert gram["rational_gram_matrix"]["min_eigenvalue"] > 0.0
    assert gram["algebraic_gram_matrix"]["min_eigenvalue"] > 0.0
    assert gram["rational_gram_matrix"]["min_off_diagonal_2x2_minor_det"] > 0.0


def test_09_synthetic_off_critical_quartet_controls():
    """Verify synthetic off-critical zero quartets have nonzero weight and violate |C(K)| <= C(0)."""
    ctrl = evaluate_synthetic_off_critical_quartet_controls()
    assert ctrl["all_off_critical_quartets_have_nonzero_weight"] is True
    assert ctrl["all_off_critical_quartets_violate_bound"] is True
    assert len(ctrl["synthetic_quartets"]) == 3


# ---------------------------------------------------------------------------
# 5. Controls on tau = 2*pi, Arithmetic Proof Attempts & Lean 4 Module
# ---------------------------------------------------------------------------


def test_10_tau_width_and_base_scaling_controls():
    """Verify C_{a,b}(K) = sqrt(a_0 / a) C_{a_0,tau}(K log(b) / log(tau)) across (a, b) pairs."""
    ctrl = evaluate_tau_scaling_controls()
    assert ctrl["status"] == GENERIC_WIDTH_AND_BASE_SCALING_PROVED
    assert ctrl["max_scaling_abs_err"] < 1e-40
    assert len(ctrl["evaluations"]) == 5


def test_11_arithmetic_proof_attempts_and_open_subgate(artifact_payload):
    """Verify pointwise kernel difference sign change, large-K wavelet decomposition, and SUBGATE-TC-042A OPEN."""
    attempts = artifact_payload[
        "section_9_arithmetic_proof_attempts_and_remaining_subgate"
    ]
    att1 = attempts["attempt_1_pointwise_kernel_difference"]
    assert att1["status"] == POINTWISE_KERNEL_DIFFERENCE_SIGN_FALSIFIED
    assert att1["sign_changes_across_primes"] is True
    assert att1["value_at_n_eq_3"] > 0.0
    assert att1["value_at_n_eq_7_near_tau"] < 0.0

    subgate = attempts["exact_remaining_subgate"]
    assert subgate["subgate_id"] == SUBGATE_TC_042A_ID
    assert subgate["status"] == SUBGATE_TC_042A_STATUS

    dims = artifact_payload["status_dimensions"]
    assert dims["universal_arithmetic_bound_status"] == UNIVERSAL_ARITHMETIC_CORRELATION_BOUND_OPEN
    assert dims["independent_review_status"] == INDEPENDENT_REVIEW_STATUS
    assert dims["rh_proved"] is False
    assert artifact_payload["epic_id"] == EPIC_TC_042_ID
    assert artifact_payload["task_id"] == TASK_TC_042_ID


def test_12_lean_formalization_module_verified():
    """Verify formal/RiemannScope/CanonicalThetaCorrelationBound.lean has 24 defs, 42 theorems, 0 sorry/admit, and non-vacuous residue hypothesis."""
    assert LEAN_MODULE_PATH.exists()
    ver = verify_canonical_theta_correlation_lean_module()
    assert ver["matches_exact"] is True
    assert ver["contains_sorry"] is False
    assert ver["contains_admit"] is False
    assert ver["actual_defs"] == CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert ver["actual_theorems"] == CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    assert len(ver["actual_defs"]) == 24
    assert len(ver["actual_theorems"]) == 43

    lean_text = LEAN_MODULE_PATH.read_text(encoding="utf-8")
    # Ensure the vacuous universal quantification over res_sq is absent
    assert "∀ w_re res_sq : ℝ, 0 < w_re → res_sq = 0" not in lean_text
    assert "∀ w_re w_im : ℝ, 0 < w_re → resSq w_re w_im = 0" in lean_text
    assert "laplace_holomorphic_rhp_hypothesis_satisfiable" in lean_text
    assert "stieltjes_rescaled_variable_and_erroneous_factor_obstruction" in lean_text
    assert "bernstein_weighted_h0_polynomial_endpoints" in lean_text
    assert "taylor_sixth_order_two_sided_abs_correlation_bound" in lean_text
    assert "stieltjes_signed_pairing_uniform_bound_equivalence" in lean_text
    assert "primitive_transfer_zero_lower_boundary_and_spurious_term_obstruction" in lean_text
    assert "dyadic_shell_weighted_sum_and_misplaced_factor_obstruction" in lean_text
    assert "single_seed_stieltjes_and_squared_polynomial_identities" in lean_text
    assert "single_seed_sech_energy_implies_complete_correlation_bound" in lean_text
    assert "unconditional_reflected_grade_invariance" in lean_text
    assert "hyperbolic_offline_pair_invariance_and_indefiniteness" in lean_text
    assert "quotient_unitary_grade_transport_of_positivity" in lean_text
    assert "attempt_A_shift_difference_square_identity" in lean_text
    assert "attempt_B_universal_pole_pnt_archimedean_cancellation" in lean_text
    assert "complex_reflected_pair_conjugate_inverse_invariance" in lean_text
    assert "sesquilinear_shift_difference_identity" in lean_text
    assert "two_dim_gram_cauchy_schwarz_from_nonneg" in lean_text
    assert "cross_grade_complex_zero_ray_collinearity" in lean_text
    assert "attempt_B_pole_vanishing_transfer_cancellation_on_S_tau" in lean_text
    assert "coercive_norm_shift_semiboundedness_implies_correlation_bound" in lean_text
    assert "majorant_without_sign_cancellation_exceeds_fixed_coercive_norm" in lean_text
    assert "majorant_window_lower_bound_and_envelope_ordering" in lean_text
    assert "zero_moment_subtracted_and_chordal_stieltjes_equivalence" in lean_text
    assert "transfer_form_plancherel_bound_and_minus_state_vanishing" in lean_text


def test_13_archimedean_taylor_remainder_defect_and_branch_analyticity_repair():
    """Verify reproduction of the 2.189e-23 Taylor remainder at series_order=36 and its Cauchy circle repair + analytic=True branch checking."""
    from tc.canonical_theta_correlation_bound import (
        evaluate_h0_acb,
        reproduce_tc042_archimedean_taylor_remainder_defect,
    )

    rep = reproduce_tc042_archimedean_taylor_remainder_defect()
    assert rep["old_series_order"] == 36
    assert rep["old_integrated_terms_count"] == 35
    assert rep["lies_in_user_audit_interval_2_064e_23_to_2_212e_23"] is True
    assert rep["exceeds_old_allowance_ratio"] > 20.0
    assert rep["repaired_cauchy_encloses_N_35"] is True
    assert rep["new_series_order"] == 49
    assert rep["new_integrated_terms_count"] == 48
    assert rep["repaired_cauchy_encloses_N_48"] is True
    assert rep["repaired_cauchy_bound_at_N_48"] < 1e-26

    # Verify branch-cut sensitivity when analytic=True at u = i * pi / 2 (where e^u + e^{-u} = 0)
    u_branch = acb(arb(0), arb.pi() / arb(2))
    val_analytic = evaluate_h0_acb(u_branch.exp(), analytic=True)
    assert not val_analytic.is_finite()


def test_14_two_sided_local_theorem_zero_free_and_unconditional_spectral(artifact_payload):
    """Verify zero-free arithmetic vs unconditional spectral-tail two-sided local Taylor bounds and computed derivative tails."""
    conc = artifact_payload["section_6_7_certified_grade_grid_and_controls"][
        "local_concavity_and_derivatives"
    ]
    assert conc["arithmetic_spectral_derivative_enclosures_intersect_at_0"] is True

    tails = conc["computed_spectral_derivative_tail_bounds_T_100"]
    assert tails["unconditional_delta_max_used"] == 0.5
    assert 0.0 < tails["order_0_tail_upper"] < 1e-53
    assert 0.0 < tails["order_2_tail_upper"] < 1e-48
    assert 0.0 < tails["order_4_tail_on_K_le_0_14_upper"] < 1e-42

    zf = conc["zero_free_arithmetic_local_enclosure"]
    assert zf["uses_spectral_zero_inputs"] is False
    assert zf["K_positivity_radius_C_gt_0"] > 0.045
    assert zf["K_two_sided_abs_bound_radius_abs_C_lt_C0"] > 0.050

    sp = conc["unconditional_spectral_tail_local_enclosure"]
    assert sp["uses_certified_turing_zeros_up_to_100"] is True
    assert sp["accounts_for_off_critical_zeros_above_100"] is True
    assert 0.050 < sp["K_positivity_radius_C_gt_0"] < 0.052
    assert 0.068 < sp["K_two_sided_abs_bound_radius_abs_C_lt_C0"] < 0.069
    assert 0.133 < sp["K_upper_concavity_radius_C_lt_C0"] < 0.134


def test_15_outward_rounded_arb_mat_sylvester_gram_minors(artifact_payload):
    """Verify outward-rounded flint.arb_mat.det() leading principal minors certify Sylvester positive-definiteness."""
    gram = artifact_payload["section_6_7_certified_grade_grid_and_controls"][
        "finite_toeplitz_gram_matrices"
    ]
    assert gram["all_gram_matrices_positive_definite"] is True
    for key, expected_dim in (
        ("rational_gram_matrix", 6),
        ("algebraic_gram_matrix", 5),
        ("zero_free_arithmetic_3_point_gram_matrix", 3),
    ):
        mat_info = gram[key]
        assert mat_info["dimension"] == expected_dim
        assert mat_info["positive_definite_certified_by_sylvester_arb_mat"] is True
        minors = mat_info["leading_principal_minors_arb_mat"]
        assert len(minors) == expected_dim
        for m_idx, minor in enumerate(minors, start=1):
            assert minor["order"] == m_idx
            assert minor["certified_positive"] is True
            assert minor["det_lower"] > 0.0


def test_16_uniform_prime_wavelet_boundedness_subgate_tc042b(artifact_payload):
    """Verify SUBGATE-TC-042B reduction, PNT main-term moment vanishing H_0(1/2) = 0, and certified scale evaluations."""
    from tc.canonical_theta_correlation_bound import (
        SUBGATE_TC_042B_ID,
        SUBGATE_TC_042B_STATUS,
        TASK_TC_042R_ID,
    )

    assert artifact_payload["repair_task_id"] == TASK_TC_042R_ID
    att3 = artifact_payload[
        "section_9_arithmetic_proof_attempts_and_remaining_subgate"
    ]["attempt_3_large_grade_wavelet_decomposition"]
    wv = att3["uniform_prime_wavelet_boundedness"]
    assert wv["subgate_id"] == SUBGATE_TC_042B_ID
    assert wv["status"] == SUBGATE_TC_042B_STATUS
    eq = wv["equivalence_to_complete_correlation_boundedness"]
    assert 0.0 < eq["forward_prime_global_bound_M_fwd"] < 0.65
    assert 0.0 < eq["archimedean_global_bound_M_arch"] < 6.6
    st = wv["stieltjes_chebyshev_error_representation"]
    assert st["pnt_main_term_moment_H0_at_half_contains_zero"] is True
    assert st["pnt_main_term_moment_abs_upper"] < 1e-13
    assert len(wv["certified_scale_evaluations_X_1_to_1000"]) == 9
    assert wv["max_certified_abs_W_wavelet_on_1_to_1000"] < 0.15


def test_17_stieltjes_finite_cutoff_identities_and_old_formula_refutation(artifact_payload):
    """Verify repaired Stieltjes identities (Form A in x and Form B in alpha = x/X) at B = 50 for X in {1, 4, 100} and failure of old X^{-1/2} formula at X != 1."""
    from tc.canonical_theta_correlation_bound import (
        STIELTJES_IDENTITY_REPAIRED_AND_CERTIFIED,
        TASK_TC_042R2_ID,
    )

    assert artifact_payload["sprint_task_id"] == TASK_TC_042R2_ID
    att3 = artifact_payload[
        "section_9_arithmetic_proof_attempts_and_remaining_subgate"
    ]["attempt_3_large_grade_wavelet_decomposition"]
    wv = att3["uniform_prime_wavelet_boundedness"]
    st = wv["stieltjes_chebyshev_error_representation"]
    assert st["H0_at_0_mellin_value_positive"] > 0.0
    assert "W_alpha" in wv["notation_separation"]
    assert "W_X" in wv["notation_separation"]

    fc = st["finite_cutoff_stieltjes_verification"]
    assert fc["status"] == STIELTJES_IDENTITY_REPAIRED_AND_CERTIFIED
    assert fc["B_cutoff"] == 50
    assert fc["all_form_A_enclose_lhs"] is True
    assert fc["all_form_B_enclose_lhs"] is True
    assert fc["old_erroneous_formula_refuted_at_X_ne_1"] is True

    by_X = {row["X"]: row for row in fc["scale_verifications"]}
    for x_val in (1, 4, 100):
        row = by_X[x_val]
        assert row["form_A_encloses_lhs"] is True
        assert row["form_B_encloses_lhs"] is True
        assert row["form_A_abs_mid_diff"] < 1e-28
        assert row["form_B_abs_mid_diff"] < 1e-28
        assert row["stieltjes_integral_certified_nonzero"] is True
        if x_val != 1:
            assert row["old_erroneous_formula_encloses_lhs"] is False
            assert row["old_erroneous_formula_abs_discrepancy"] > 1e-2


def test_18_exact_rational_bernstein_weighted_kernel_envelopes():
    """Verify exact rational Bernstein polynomial certificates for |g^{(m)}(v)| <= |g^{(m)}(0)| 2^{5/2} (2 cosh v)^{-5/2}."""
    from tc.canonical_theta_correlation_bound import (
        BERNSTEIN_KERNEL_ENVELOPES_EXACT_RATIONAL_CERTIFIED,
        certify_weighted_kernel_envelopes_bernstein,
    )

    res = certify_weighted_kernel_envelopes_bernstein()
    assert res["status"] == BERNSTEIN_KERNEL_ENVELOPES_EXACT_RATIONAL_CERTIFIED
    assert res["all_even_envelopes_certified"] is True
    assert res["all_interior_bernstein_strictly_smaller_than_endpoint"] is True
    for m_key in ("m_0", "m_2", "m_4", "m_6", "m_8"):
        cert = res["even_derivative_certificates"][m_key]
        assert cert["all_bernstein_control_points_bounded_by_endpoint"] is True
        assert cert["strict_interior_dominance_certified"] is True
        assert cert["max_interior_bernstein_to_endpoint_ratio"] < 0.95

    odd = res["first_euler_derivative_and_tilde_h0_envelope"]
    assert odd["certified_D1_sq_exceeds_bernstein_max"] is True
    assert 15.7 < odd["certified_tilde_h0_envelope_constant_float"] < 15.8


def test_19_scoped_m6_elementary_prime_bound_and_exact_rational_endpoints(artifact_payload):
    """Verify M_6^{arith} scope |K| <= 0.08, elementary prime cube sum bound < 0.225, and exact rational endpoints 1/20 = 0.05 and 17/250 = 0.068."""
    conc = artifact_payload["section_6_7_certified_grade_grid_and_controls"][
        "local_concavity_and_derivatives"
    ]
    elem = conc["elementary_prime_cube_sum_bound"]
    assert elem["elementary_bound_strictly_below_0_225"] is True
    assert 0.216 < elem["elementary_upper_bound_float"] < 0.217
    assert 0.164 < elem["direct_sum_25000_plus_rs_tail_upper"] < 0.165

    assert math.isclose(conc["C_tau_fourth_deriv_0_mid"], 433.5413086756161, rel_tol=1e-12)
    zf = conc["zero_free_arithmetic_local_enclosure"]
    assert "|K| <= 0.08" in zf["sixth_derivative_domain_scope"]
    assert math.isclose(zf["sixth_derivative_bound_M6_arith_on_0_08"], 27971954.786589753, rel_tol=1e-12)
    assert zf["certified_exact_rational_endpoint"] == "1/20"
    assert zf["certified_exact_rational_endpoint_float"] == 0.05
    assert zf["certified_exact_rational_positivity_endpoint"] == "9/200"
    assert zf["certified_exact_rational_positivity_endpoint_float"] == 0.045
    assert zf["exact_rational_1_20_certified"] is True
    assert zf["upper_concavity_margin_at_1_20_lower"] > 0.0
    assert zf["positivity_margin_at_9_200_lower"] > 0.0
    assert zf["lower_abs_margin_at_1_20_lower"] > 0.0

    sp = conc["unconditional_spectral_tail_local_enclosure"]
    assert sp["certified_exact_rational_endpoint"] == "17/250"
    assert sp["certified_exact_rational_endpoint_float"] == 0.068
    assert sp["certified_exact_rational_positivity_endpoint"] == "1/20"
    assert sp["certified_exact_rational_positivity_endpoint_float"] == 0.05
    assert sp["exact_rational_17_250_certified"] is True
    assert sp["upper_concavity_margin_at_17_250_lower"] > 0.0
    assert sp["positivity_margin_at_1_20_lower"] > 0.0
    assert sp["lower_abs_margin_at_17_250_lower"] > 0.0


def test_20_derived_uniform_archimedean_bound_and_discrepancy_reconciliation(artifact_payload):
    """Verify derived uniform archimedean bound < 4.95 (total W_arch <= 5.9943) and baseline narrative discrepancy reconciliation."""
    from tc.canonical_theta_correlation_bound import (
        derive_and_certify_uniform_archimedean_bound,
    )

    arch_b = derive_and_certify_uniform_archimedean_bound()
    assert arch_b["valid_for_all_real_K"] is True
    assert arch_b["strictly_improves_previous_4_95_bound"] is True
    assert 4.448 < arch_b["derived_arch_integral_uniform_bound"] < 4.449
    assert 5.994 < arch_b["derived_w_arch_total_uniform_bound"] < 5.995

    reconcil = artifact_payload["section_6_7_certified_grade_grid_and_controls"][
        "baseline_narrative_discrepancy_reconciliation"
    ]
    assert reconcil["all_discrepancies_reconciled"] is True
    assert len(reconcil["reconciled_items"]) == 3
    disc3 = reconcil["reconciled_items"][2]
    assert disc3["stale_narrative_value"] == 0.0319695591
    assert math.isclose(disc3["certified_W_at_tau_mid"], -0.012081947061365263, rel_tol=1e-9)
    assert math.isclose(
        disc3["certified_H0_at_0_mellin_mid"],
        2.8290934399732197e-05,
        rel_tol=1e-9,
    )


def test_21_subgate_tc042b_cancellation_attempts_and_seed_convolution(artifact_payload):
    """Verify the three SUBGATE-TC-042B cancellation attempts (Euler operator factorization, dyadic decomposition, and single-seed convolution V_tau)."""
    att3 = artifact_payload[
        "section_9_arithmetic_proof_attempts_and_remaining_subgate"
    ]["attempt_3_large_grade_wavelet_decomposition"]
    wv = att3["uniform_prime_wavelet_boundedness"]
    canc = wv["subgate_tc042b_cancellation_attempts"]

    assert canc["boundary_term_uniform_bound"]["exact_rational_coeff"] == "92193/24576"
    attA = canc["attempt_A_multiscale_euler_operator_and_primitive_transfer"]
    assert attA["symbolic_factorization_verified"] is True
    op_m = attA["operator_multiplicity_vs_mellin_vanishing_order"]
    assert op_m["operator_factor_multiplicity_at_D_eq_pos_half"] == 5
    assert op_m["operator_factor_multiplicity_at_D_eq_neg_half"] == 4
    assert op_m["H0_mellin_vanishing_order_at_z_eq_pm_half"] == 3
    assert op_m["tilde_H0_mellin_vanishing_order_at_z_eq_pos_half"] == 3
    assert op_m["tilde_H0_mellin_vanishing_order_at_z_eq_neg_half"] == 4

    attB = canc["attempt_B_signed_dyadic_scale_decomposition"]
    assert 0.0 < attB["l1_majorant_weight_sum_upper"] < 17.5
    assert len(attB["dyadic_shells_minus6_to_5"]) == 12
    assert attB["all_dyadic_shell_sums_enclose_I_B"] is True

    attC = canc["attempt_C_seed_wavelet_multiplicative_convolution_factorization"]
    assert attC["single_seed_pnt_moment_vanishes"] is True
    assert attC["single_seed_pnt_moment_abs_upper"] < 1e-18
    assert attC["finite_sum_convolution_verification_at_X_4_abs_diff"] < 1e-10
    assert math.isclose(attC["weighted_psi_tau_l2_norm_C_psi"], 1.5326496414421077, rel_tol=1e-11)


def test_22_attempt_a_b_c_repairs_and_mellin_vanishing_orders(artifact_payload):
    """Verify the four substantive repairs:
    1. Attempt B dyadic shell definition without X^{-1/2} and [1, inf) cutoff at B=50;
    2. Attempt A primitive transfer without spurious (1/2)*h_1(1/X) boundary term at B=50;
    3. Differentiated seed H_0(0) = F_tau(1/2)^2 ~ 2.82909344e-5 and Mellin vanishing orders (1, 2, 3);
    4. Attempt C exact Gaussian moment formula for C_psi^2, single-seed Stieltjes identity, and sech^2 energy.
    """
    seed_sec = artifact_payload["section_2_seed_defect_and_mellin_audit"]
    ep = seed_sec["endpoint_values"]
    assert ep["F_tau_vanishing_order_at_0"] == 1
    assert ep["F_tau_vanishing_order_at_1"] == 2
    assert ep["H0_vanishing_order_at_z_eq_pm_half"] == 3

    att3 = artifact_payload[
        "section_9_arithmetic_proof_attempts_and_remaining_subgate"
    ]["attempt_3_large_grade_wavelet_decomposition"]
    wv = att3["uniform_prime_wavelet_boundedness"]
    st = wv["stieltjes_chebyshev_error_representation"]
    assert math.isclose(
        st["H0_at_0_mellin_value_positive"],
        2.8290934399732197e-05,
        rel_tol=1e-9,
    )

    canc = wv["subgate_tc042b_cancellation_attempts"]

    # Point 2: Attempt A primitive transfer without spurious (1/2) h_1(1/X)
    attA = canc["attempt_A_multiscale_euler_operator_and_primitive_transfer"]
    assert attA["all_primitive_transfer_finite_cutoff_enclose"] is True
    assert math.isclose(
        attA["spurious_half_h1_at_X_eq_1_refuted_value"],
        -7.77359913117768,
        rel_tol=1e-10,
    )
    pt_by_X = {row["X"]: row for row in attA["primitive_transfer_verifications"]}
    for x_val in (1, 4, 100):
        assert pt_by_X[x_val]["exact_encloses_lhs"] is True
        assert pt_by_X[x_val]["exact_abs_mid_diff"] < 1e-28
    assert pt_by_X[1]["erroneous_rhs_with_spurious_term_abs_discrepancy"] > 7.77

    # Point 1: Attempt B dyadic shells without misplaced X^{-1/2}
    attB = canc["attempt_B_signed_dyadic_scale_decomposition"]
    assert attB["all_dyadic_shell_sums_enclose_I_B"] is True
    assert attB["erroneous_X_minus_half_factor_refuted"] is True
    sh_by_X = {row["X"]: row for row in attB["dyadic_shell_finite_cutoff_verifications"]}
    for x_val in (1, 4, 100):
        assert sh_by_X[x_val]["exact_abs_diff"] < 1e-28
        if x_val != 1:
            assert sh_by_X[x_val]["erroneous_X_minus_half_abs_discrepancy"] > 1e-2

    # Point 4: Attempt C exact Gaussian moment C_psi, single-seed Stieltjes, and sech^2 energy
    attC = canc["attempt_C_seed_wavelet_multiplicative_convolution_factorization"]
    assert (
        attC["exact_gaussian_moment_formula_C_psi_sq"]
        == "C_psi^2 = (1 / sqrt(2)) * (1143585 / (524288 * pi) + 92193 / 65536 + 12735 * pi / 32768)"
    )
    assert attC["symbolic_gaussian_moment_identity_verified"] is True
    assert math.isclose(
        attC["C_psi_sq_exact_mid"], 2.3490149234126213, rel_tol=1e-12
    )
    assert math.isclose(
        attC["C_psi_exact_mid"], 1.5326496414421077, rel_tol=1e-12
    )
    assert attC["C_psi_certified_lt_1_533"] is True
    assert attC["quadrature_with_tail_overlaps_exact_C_psi_sq"] is True
    assert attC["single_seed_stieltjes_identity_verified"] is True
    for st_row in attC["single_seed_stieltjes_verifications"]:
        assert st_row["encloses"] is True
        assert st_row["abs_mid_diff"] < 1e-25
    assert attC["all_sampled_cauchy_schwarz_bounds_satisfied"] is True


def test_23_repairs_8a_8b_8c_and_task_tc042f_arithmetic_fourier_factorization(
    artifact_payload,
):
    """Verify Repairs 8A, 8B, 8C and TASK-TC-042F (Arithmetic–Fourier Positive Factorization)."""
    from tc.canonical_theta_correlation_bound import (
        ARITHMETIC_FOURIER_FACTORIZATION_STATUS,
        TASK_TC_042F_ID,
    )

    # Repair 8C: F_tau''(1) = 1/16 = 0.0625 and hat{tilde{h}_0}(z) = (1/2 + z) H_0(z)
    seed_sec = artifact_payload["section_2_seed_defect_and_mellin_audit"]
    ep = seed_sec["endpoint_values"]
    assert ep["F_tau_second_deriv_at_1_exact"] == "1/16"
    assert math.isclose(ep["F_tau_second_deriv_at_1"], 0.0625, rel_tol=1e-15)

    att3 = artifact_payload[
        "section_9_arithmetic_proof_attempts_and_remaining_subgate"
    ]["attempt_3_large_grade_wavelet_decomposition"]
    wv = att3["uniform_prime_wavelet_boundedness"]
    canc = wv["subgate_tc042b_cancellation_attempts"]
    attA_wv = canc["attempt_A_multiscale_euler_operator_and_primitive_transfer"]
    op_m = attA_wv["operator_multiplicity_vs_mellin_vanishing_order"]
    assert "(1/2 + z) H_0(z)" in op_m["tilde_H0_mellin_formula"]

    # Repair 8A: Derived [4, infty) tail bound for _f_conv_25 so enclosures overlap
    attC = canc["attempt_C_seed_wavelet_multiplicative_convolution_factorization"]
    assert attC["finite_sum_convolution_enclosures_overlap"] is True
    assert 4.5e-19 < attC["finite_sum_convolution_tail_bound_4_inf_upper"] < 1.1e-18

    # Repair 8B: Prime-power cutoff 25000 >= 5*exp(8.5) ~ 24574 and EMPIRICAL grid diagnostic status
    assert attC["sech_squared_energy_prime_power_cutoff"] == 25000
    assert (
        attC["sech_squared_energy_samples_status"]
        == "TRUNCATED_GRID_DIAGNOSTIC_NOT_CERTIFIED"
    )
    assert attC["sech_squared_energy_samples_evidence_class"] == "EMPIRICAL"
    sens = attC["sech_squared_energy_cutoff_sensitivity_at_X_100"]
    assert len(sens) == 4
    sens_by_cut = {row["prime_power_cutoff"]: row for row in sens}
    assert sens_by_cut[600]["covers_5_exp_8_5_eq_24574"] is False
    assert sens_by_cut[25000]["covers_5_exp_8_5_eq_24574"] is True
    assert (
        sens_by_cut[25000]["E_tau_log_100_grid"]
        < 0.01 * sens_by_cut[600]["E_tau_log_100_grid"]
    )

    # TASK-TC-042F: Arithmetic–Fourier Positive Factorization
    assert artifact_payload["factorization_task_id"] == TASK_TC_042F_ID
    assert (
        artifact_payload["status_dimensions"][
            "arithmetic_fourier_factorization_status"
        ]
        == ARITHMETIC_FOURIER_FACTORIZATION_STATUS
    )
    sec11 = artifact_payload[
        "section_11_arithmetic_fourier_positive_factorization"
    ]
    assert sec11["task_id"] == TASK_TC_042F_ID
    assert len(sec11["section_2_reuse_map"]) == 5

    # Section 3: Unconditional grade invariance & reflected off-line pair hyperbolic form
    sec3 = sec11["section_3_normalized_pairing_and_grade_invariance"]
    pair = sec3["reflected_offline_pair_block"]
    assert pair["symbolic_diagonal_invariance_verified"] is True
    assert pair["q_at_u1_v_minus1"] == -2
    assert pair["q_at_u1_v_plus1"] == 2
    assert pair["symbolic_off_diagonal_cosh_verified"] is True

    # Section 5: Five-place tau = 2*pi coupling audit
    sec5 = sec11["section_5_five_place_tau_coupling_audit"]
    assert len(sec5["five_places_of_tau_eq_2pi"]) == 5
    incoh = sec5["incoherent_tau_perturbation_controls"]
    assert len(incoh) == 4
    canonical_rows = [
        r for r in incoh if r["preserves_canonical_self_duality"] is True
    ]
    assert len(canonical_rows) == 1
    assert math.isclose(
        canonical_rows[0]["tau_arch_float"], 2.0 * math.pi, rel_tol=1e-14
    )

    # Section 6 & 7: Attempt A & Attempt B
    sec67 = sec11["section_6_7_factorization_attempts_and_tests"]
    attA_f = sec67["attempt_A_euler_resolvent_semilocal"]
    assert math.isclose(
        attA_f["c_tau_A_value"], 5.3721834192256654, rel_tol=1e-13
    )
    assert len(attA_f["three_structural_obstructions"]) == 3

    attB_f = sec67[
        "attempt_B_direct_arithmetic_kernel_and_pole_pnt_cancellation"
    ]
    assert math.isclose(
        attB_f["c_tau_B_value"], 3.3721834192256654, rel_tol=1e-13
    )
    assert attB_f["spatial_vs_analytic_norm_A_B_abs_diff"] < 1e-13

    unreg = attB_f["unregularized_pole_pnt_cancellation_check_at_B_50"]
    assert unreg["encloses"] is True
    assert unreg["abs_mid_diff"] < 1e-28
    assert unreg["nonzero_growing_pole_integral_1_to_B"] > 0.43

    sb = attB_f["quantitative_sign_balance_discovery_on_psi_tau"]
    assert math.isclose(
        sb["norm_A_B_sq_positive"], 0.594767833460595, rel_tol=1e-11
    )
    assert math.isclose(
        sb["local_term_minus_c_tau_B_norm_f_sq_negative"],
        -1.6771975212486425,
        rel_tol=1e-11,
    )
    assert sb["net_smooth_part_strictly_negative"] < -1.082
    assert sb["chebyshev_prime_error_stieltjes_positive"] > 1.083
    assert math.isclose(
        sb["net_complete_pairing_Q_tau_positive"],
        0.0009504777883195959,
        rel_tol=1e-9,
    )

    for d_row in sec67["diagonal_grade_evaluations"]:
        assert d_row["attempt_A_identity_abs_diff"] < 1e-28
        assert d_row["attempt_B_identity_abs_diff"] < 1e-28
    for od_row in sec67["off_diagonal_grade_evaluations"]:
        assert od_row["attempt_A_identity_abs_diff"] < 1e-28
        assert od_row["attempt_B_identity_abs_diff"] < 1e-28
        assert od_row["cauchy_schwarz_on_A_B_satisfied"] is True
        assert od_row["cauchy_schwarz_on_Q_tau_satisfied"] is True
    for mg_row in sec67["multi_grade_superposition_evaluations"]:
        assert mg_row["Q_tau_positive"] is True
        assert mg_row["attempt_A_identity_abs_diff"] < 1e-28
        assert mg_row["attempt_B_identity_abs_diff"] < 1e-28
        assert mg_row["attempt_B_smooth_part"] < 0.0
        assert mg_row["attempt_B_prime_error_stieltjes"] > 0.0


def test_24_tc042f_bounded_reconciliation_regressions(artifact_payload):
    """Targeted regression tests for the 6 bounded TC-042F reconciliation items (Step 2 of TASK-TC-043)."""
    sec11 = artifact_payload[
        "section_11_arithmetic_fourier_positive_factorization"
    ]
    sec12 = artifact_payload[
        "section_12_admissible_cross_grade_compatibility"
    ]
    rec = sec12["section_1_tc042f_reconciliation"]

    # 1. Complex reflected-pair scaling q(lambda * u, conj(lambda)^{-1} * v) = q(u, v) vs naive lambda^{-1}
    d1 = rec["defect_1_complex_reflected_pair_scaling"]
    assert d1["status"] == "RECONCILED_AND_VERIFIED"
    assert d1["conj_inv_symbolic_invariance_verified"] is True
    ce = d1["counterexample_lambda_eq_i"]
    assert ce["q_orig_u1_v1"] == 2
    assert ce["q_conj_inv_u1_v1"] == 2
    assert ce["q_naive_inv_u1_v1"] == -2
    assert ce["naive_inverse_fails"] is True

    # 2. General sesquilinear shift-difference identity <(I - S_u)f, (I - S_u)g> = 2<f,g> - <S_u f, g> - <S_{-u} f, g>
    d2 = rec["defect_2_shift_difference_sesquilinear_identity"]
    assert d2["status"] == "RECONCILED_AND_VERIFIED"
    assert d2["two_sided_matches_polarization"] is True
    assert d2["one_sided_omission_fails_on_asymmetric_pair"] is True
    assert d2["asymmetry_abs_gap"] > 1e-3

    # 3. Stieltjes endpoint at x = 1 (integration-by-parts boundary value E(1) = -1, not jump of psi)
    d3 = rec["defect_3_stieltjes_endpoint_at_one"]
    assert d3["status"] == "RECONCILED_AND_VERIFIED"
    assert d3["psi_at_1"] == 0.0
    assert d3["psi_jump_at_1"] == 0.0
    assert d3["first_jump_station_of_psi"] == 2
    assert d3["E_at_1"] == -1.0

    # 4. Reconciled numerical summaries (-1.0824296878, +1.0833801676) vs stale (-0.399957, +0.400908)
    d4 = rec["defect_4_conflicting_numerical_summaries"]
    assert d4["status"] == "RECONCILED_AND_VERIFIED"
    assert math.isclose(
        d4["reconciled_smooth_part_B"], -1.0824296877880101, rel_tol=1e-11
    )
    assert math.isclose(
        d4["reconciled_prime_error_stieltjes_B"],
        1.0833801655763297,
        rel_tol=1e-8,
    )
    assert math.isclose(
        d4["certified_J0_halfline_pole_integral"],
        0.0259597612844062,
        rel_tol=1e-11,
    )
    assert math.isclose(
        d4["certified_B_transfer_psi_tau"], 0.9687652063353962, rel_tol=1e-11
    )
    assert math.isclose(
        d4["stale_smooth_value_diagnosed"], -0.3999571341592074, rel_tol=1e-7
    )
    assert math.isclose(
        d4["stale_prime_value_diagnosed"], 0.400907611947527, rel_tol=1e-7
    )
    q4_text = sec11["closing_questions"][
        "question_4_where_prime_or_off_critical_terms_resist"
    ]
    assert "-0.399957" not in q4_text
    assert "-1.0824296878" in q4_text

    # 5. Complete error accounting in TC-042F
    d5 = rec["defect_5_complete_error_accounting"]
    assert d5["status"] == "RECONCILED_AND_VERIFIED"
    assert d5["u_top_B"] == 20
    assert d5["cauchy_circle_arcs"] == 512
    assert d5["cauchy_taylor_remainder_bound_on_0_025"] < 1e-26
    assert d5["tail_A_B_upper_from_u20"] < 1e-21
    assert 3.0e-14 < d5["old_truncated_u12_abs_diff"] < 4.5e-14
    assert d5["repaired_u20_abs_diff"] < 1e-22
    assert d5["spatial_and_analytic_enclosures_overlap"] is True
    assert 0.0 < d5["rosser_schoenfeld_prime_tail_rad_at_K0"] < 1e-8

    # 6. Formalization scope & provenance
    d6 = rec["defect_6_formalization_scope_and_provenance"]
    assert d6["status"] == "RECONCILED_AND_VERIFIED"
    assert "two_dim_gram_cauchy_schwarz_from_nonneg" in d6["quotient_unitary_theorem_scope"]


def test_25_task_tc043_admissible_cross_grade_compatibility(artifact_payload):
    """Verify TASK-TC-043 cross-grade compatibility specification, synthetic quartet audit, and Candidates I, II, III on S_tau."""
    from tc.canonical_theta_correlation_bound import (
        ADMISSIBLE_CROSS_GRADE_COMPATIBILITY_STATUS,
        TASK_TC_043_ID,
    )

    assert artifact_payload["compatibility_task_id"] == TASK_TC_043_ID
    assert (
        artifact_payload["status_dimensions"][
            "admissible_cross_grade_compatibility_status"
        ]
        == ADMISSIBLE_CROSS_GRADE_COMPATIBILITY_STATUS
    )
    sec12 = artifact_payload[
        "section_12_admissible_cross_grade_compatibility"
    ]
    assert sec12["task_id"] == TASK_TC_043_ID

    # Step 3: Compatibility candidate, complex zero collinearity, and synthetic quartet audit
    spec = sec12["section_2_compatibility_candidate_and_controls"]
    collin = spec["cross_grade_complex_zero_and_transcendence_audit"][
        "real_part_only_alignment_test"
    ]
    assert collin["shifted_real_part_equals_half"] is True
    assert collin["moving_only_real_part_fails_zero_membership"] is True
    assert collin["imag_mismatch_from_gamma_0"] > 3.0

    q_audit = spec["synthetic_off_critical_quartet_control_audit"]
    assert len(q_audit["what_survives_synthetic_quartet"]) == 4
    assert len(q_audit["which_arithmetic_hypotheses_synthetic_quartet_violates"]) == 3
    q_sum = q_audit["certified_synthetic_quartet_controls_summary"]
    assert q_sum["case_A_max_ratio_on_grid"] > 1.0
    assert q_sum["case_B_adversarial_escaped_up_to_K4"] is True
    assert q_sum["case_B_caught_at_K8"] is True

    # Step 4: Worked Candidates I, II, III on S_tau
    s_tau = sec12["section_3_worked_candidates_on_S_tau"]
    assert s_tau["domain_properties_verified"]["w_pole_vanishes_identically_on_S_tau"] is True

    # Candidate I: Spectral Multiplier mu_tau^B(t) and Exact Pole-Vanishing Transfer Decomposition
    c1 = s_tau["candidate_1_spectral_multiplier_and_transfer_decomposition"]
    assert c1["mu_0_matches_neg_c_tau_B"] is True
    assert math.isclose(c1["mu_tau_B_at_0"], -3.3721834192256654, rel_tol=1e-13)
    assert c1["root_bracket_certified"] is True
    assert 46.4061555 <= c1["unique_positive_root_t_star_B_mid"] <= 46.4061557
    assert c1["mu_at_root_bracket_low"] < 0.0
    assert c1["mu_at_root_bracket_high"] > 0.0
    assert c1["plancherel_vs_spatial_smooth_B_abs_diff"] < 1e-22
    assert c1["plancherel_vs_spatial_B_transfer_abs_diff"] < 1e-22
    assert 0.894 < c1["transfer_share_of_smooth_deficit_on_psi_tau"] < 0.896

    # Candidate II: Coercive Norm-Shifted Hilbert Space & Semiboundedness Reduction
    c2 = s_tau["candidate_2_coercive_norm_shifted_semiboundedness"]
    assert math.isclose(
        c2["coercive_norm_sq_on_psi_tau_at_mu0_1"],
        1.092130317270496,
        rel_tol=1e-11,
    )
    assert math.isclose(
        c2["implied_uniform_correlation_bound_at_mu0_1"],
        4.350070487905407,
        rel_tol=1e-9,
    )

    # Candidate III: Cross-Grade Scale Separation & Scoped Monotone Envelope Majorant Obstruction
    c3 = s_tau["candidate_3_scale_separation_and_majorant_obstruction"]
    assert c3["symbolic_antiderivative_identity_verified"] is True
    assert c3["subinterval_strictly_less_than_full_integral"] is True
    assert c3["c_abs_methods_overlap"] is True
    assert (
        0.0
        < c3["unsigned_window_moment_c0_lower"]
        <= c3["unsigned_window_moment_c0_upper"]
        < c3["unsigned_full_moment_C_abs_lower"]
        <= c3["unsigned_full_moment_C_abs_upper"]
    )
    assert math.isclose(
        c3["unsigned_window_moment_c0_on_half_to_two"],
        1.7456980946329538,
        rel_tol=1e-13,
    )
    assert math.isclose(
        c3["unsigned_full_moment_C_abs"],
        2.486331970643793,
        rel_tol=1e-13,
    )
    assert 3.0 < c3["crossover_grade_delta_star_chebyshev_004x_at_mu0_1"] < 4.0
    assert (
        c3["crossover_grade_delta_star_chebyshev_004x_at_mu0_1"]
        < c3["crossover_grade_delta_star_chebyshev_004x_window_lower_at_mu0_1"]
    )
    assert 0.0 < c3["crossover_grade_delta_star_dlvp_at_mu0_1"] <= 0.01
    assert (
        0.5
        < c3["crossover_grade_delta_star_dlvp_window_lower_at_mu0_1"]
        < 0.7
    )
    assert (
        c3["crossover_grade_delta_star_dlvp_at_mu0_1"]
        < c3["crossover_grade_delta_star_dlvp_window_lower_at_mu0_1"]
    )
    rows_c3 = {r["Delta"]: r for r in c3["off_diagonal_scale_separation_table"]}
    assert abs(rows_c3[8.0]["G_L2_Delta"]) < 1e-15
    assert abs(rows_c3[8.0]["J_Delta"]) < 1e-5
    assert abs(rows_c3[8.0]["D_smooth_B_Delta"]) < 1e-5
    assert math.isclose(
        rows_c3[8.0]["coercive_norm_sq_f_minus_at_mu0_1"],
        c2["coercive_norm_sq_on_psi_tau_at_mu0_1"],
        rel_tol=1e-5,
    )


def test_26_task_tc043r_repairs_and_signed_cancellation_invariants(
    artifact_payload,
):
    """Verify TASK-TC-043R mathematical & numerical repairs (Steps 3A, 3B, 3C, 4) and signed cancellation invariants (Step 5)."""
    from tc.canonical_theta_correlation_bound import TASK_TC_043R_ID

    assert artifact_payload["compatibility_repair_task_id"] == TASK_TC_043R_ID
    sec12 = artifact_payload["section_12_admissible_cross_grade_compatibility"]
    assert sec12["repair_task_id"] == TASK_TC_043R_ID

    s_tau = sec12["section_3_worked_candidates_on_S_tau"]
    dom = s_tau["domain_properties_verified"]
    assert dom["seed_uncentered_zero_orders_s0_simple_s1_double"] is True
    assert dom["autocorrelation_H0_triple_zeros_at_z_pm_half"] is True

    # 1. Step 3B & 4B: Plancherel tail bounds, Arb subtraction enclosures, and R_0 / positive shifted norm multiplier
    c1 = s_tau["candidate_1_spectral_multiplier_and_transfer_decomposition"]
    assert c1["plancherel_cutoff_T_top"] == 80
    assert 0.0 < c1["plancherel_smooth_B_tail_bound_from_T80"] < 1e-41
    assert 0.0 < c1["plancherel_B_transfer_tail_bound_from_T80"] < 1e-41
    assert 1e-19 < c1["plancherel_smooth_B_tail_bound_from_T40"] < 1e-17
    assert 1e-19 < c1["plancherel_B_transfer_tail_bound_from_T40"] < 1e-17
    assert c1["plancherel_minus_spatial_smooth_B_encloses_zero"] is True
    assert c1["plancherel_minus_spatial_B_transfer_encloses_zero"] is True
    assert 0.0 < c1["plancherel_vs_spatial_smooth_B_abs_diff"] < 1e-24
    assert 0.0 < c1["plancherel_vs_spatial_B_transfer_abs_diff"] < 1e-24
    assert "4 ||f||_{L^2(d^*y)}^2 - 4 ||R_0 f||_{L^2(d^*y)}^2" in c1[
        "linear_operator_R0_and_J_fourier_identity"
    ]
    levels = c1["methodological_distinction_three_levels"]
    assert "1_analytic_proof_of_identity" in levels
    assert "2_certified_numerical_consistency" in levels
    assert "3_truncated_numerical_diagnostic" in levels

    c2 = s_tau["candidate_2_coercive_norm_shifted_semiboundedness"]
    assert "mu_tau^B(t) + c_tau^B + mu_0" in c2[
        "positive_shifted_norm_plancherel_multiplier"
    ]
    assert "(psi_tau +/- T_K psi_tau) / sqrt(2)" in c2["normalized_two_grade_states"]
    assert 0.0 < c2["coercive_norm_sq_on_psi_tau_at_mu0_1_rad"] < 1e-24

    # 2. Step 3A & 4A: Subinterval c_0 < full integral C_abs with complete error budgets and Candidate III J(Delta) tail bounds
    c3 = s_tau["candidate_3_scale_separation_and_majorant_obstruction"]
    assert len(c3["certified_sign_change_roots_of_tilde_h0"]) == 7
    assert 0.0 < c3["unsigned_window_moment_c0_rad"] < 1e-25
    assert 0.0 < c3["unsigned_full_moment_C_abs_rad"] < 1e-25
    assert 0.0 < c3["unsigned_full_moment_window_plus_bernstein_tails_rad"] < 2e-3
    assert c3["signed_full_moment_encloses_zero"] is True
    sep_defs = c3["separate_unsigned_definitions_and_envelope_ordering"]
    assert "A_E(X) <= M_omega(X)" in sep_defs["envelope_ordering"]
    assert "omega(2X)" in sep_defs["monotone_majorant_lower_bound"]
    for row in c3["off_diagonal_scale_separation_table"]:
        assert row["u_top_J"] >= 20
        assert 0.0 < row["J_Delta_tail_bound"] < 1e-20
        assert 0.0 < row["J_Delta_rad"] < 1e-20
        assert 0.0 < row["coercive_norm_sq_f_minus_at_mu0_1_rad"] < 1e-20

    # 3. Step 3C: Continuation identity alpha^{-3/2} tilde{h}_0(alpha) = -d/d_alpha (alpha^{-1/2} h_0(alpha))
    sec4 = sec12["section_4_remaining_implication_and_next_step"]
    assert (
        "alpha^{-3/2} tilde{h}_0(alpha) = -d/d_alpha (alpha^{-1/2} h_0(alpha))"
        in sec4["next_justified_calculation"]
    )
    assert "B_boundary(X)" in sec4["remaining_implication"]

    # 4. Step 5: Zero-moment subtracted increment, chordal Stieltjes equivalence, and Chebyshev primitive transfer
    c4 = sec12["section_5_signed_cancellation_investigation"]
    prim = c4["next_justified_refinement_chebyshev_primitive_transfer"]
    assert prim["symbolic_ibp_verified"] is True
    assert prim["k1_signed_full_moment_encloses_zero"] is True
    assert (
        0.0
        < prim["k1_unsigned_window_moment_c1_on_half_to_two"]
        < prim["k1_unsigned_full_moment_C1_abs"]
    )
    assert math.isclose(
        prim["k1_unsigned_window_moment_c1_on_half_to_two"],
        11.489756672104577,
        rel_tol=1e-12,
    )
    assert math.isclose(
        prim["k1_unsigned_full_moment_C1_abs"],
        14.756398942720541,
        rel_tol=1e-12,
    )

    scale_checks = c4["certified_scale_checks"]
    assert len(scale_checks) == 4
    for sc in scale_checks:
        assert sc["lower_tail_plus_B_boundary_encloses_zero"] is True
        assert sc["lower_tail_plus_B_boundary_abs_upper"] < 1e-27
        assert sc["k1_lower_tail_identity_encloses_zero"] is True
        assert sc["k1_lower_tail_identity_abs_upper"] < 1e-27
        assert sc["zero_moment_decomp_encloses_zero"] is True
        assert sc["zero_moment_decomp_abs_upper"] < 1e-24
        assert sc["chordal_stieltjes_closed_form_encloses_zero"] is True
        assert sc["chordal_stieltjes_closed_form_abs_upper"] < 1e-24
        assert sc["inc_equals_chord_minus_drift_encloses_zero"] is True
        assert sc["inc_equals_chord_minus_drift_abs_upper"] < 1e-24
        assert sc["primitive_transfer_encloses_zero"] is True
        assert sc["primitive_transfer_abs_upper"] < 1e-24


def test_27_task_tc044_prime_shift_quadratic_form_and_divisor_aggregation(
    artifact_payload,
):
    """Verify TASK-TC-044 narrow corrections, prime-shift quadratic form D_N(f), divisor-aggregated W_log(X) unconditional bound, Moebius inversion, and controls."""
    from tc.canonical_theta_correlation_bound import (
        PRIME_SHIFT_QUADRATIC_FORM_STATUS,
        TASK_TC_044_ID,
    )

    assert artifact_payload["prime_shift_task_id"] == TASK_TC_044_ID
    assert (
        artifact_payload["status_dimensions"]["prime_shift_quadratic_form_status"]
        == PRIME_SHIFT_QUADRATIC_FORM_STATUS
    )
    sec13 = artifact_payload[
        "section_13_prime_shift_quadratic_form_and_divisor_aggregation"
    ]
    assert sec13["task_id"] == TASK_TC_044_ID
    assert sec13["status"] == PRIME_SHIFT_QUADRATIC_FORM_STATUS

    # 1. Step 1 & Step 2: Baseline recovery and narrow corrections
    sec1 = sec13["section_1_baseline_and_narrow_corrections"]
    nc = sec1["narrow_corrections_verified"]
    assert nc["primitive_kernel_mellin_multiplier"]["symbolic_verified"] is True
    assert (
        "(z + 1/2)(z + 3/2) H_0(z) = rho(rho + 1) H_0(z)"
        in nc["primitive_kernel_mellin_multiplier"]["formula"]
    )
    assert nc["stieltjes_x_differential_identity"]["symbolic_verified"] is True
    assert (
        "x^{-3/2} tilde{h}_0(x/X) dx = -d[x^{-1/2} h_0(x/X)]"
        in nc["stieltjes_x_differential_identity"]["formula"]
    )
    assert (
        "psi_1(x) = (x^2 - 1)/2 + E_1(x)"
        in nc["chebyshev_primitive_relation"]["formula"]
    )
    assert (
        "psi(x) < 1.03883 * x"
        in nc["rosser_schoenfeld_primary_source_record"][
            "theorem_12_one_sided_bound"
        ]
    )
    assert math.isclose(
        nc["authoritative_c_tau_B_enclosure"]["c_tau_B_mid"],
        3.3721834192256654,
        rel_tol=1e-15,
    )

    #Also check that Section 12 was updated with the narrow corrections:
    sec12 = artifact_payload["section_12_admissible_cross_grade_compatibility"]
    c3_12 = sec12["section_3_worked_candidates_on_S_tau"][
        "candidate_3_scale_separation_and_majorant_obstruction"
    ]
    assert (
        "1.03883*x"
        in c3_12["separate_unsigned_definitions_and_envelope_ordering"][
            "classical_bounds_vs_illustrative_models"
        ]
    )
    assert (
        "0.0397"
        not in c3_12["separate_unsigned_definitions_and_envelope_ordering"][
            "classical_bounds_vs_illustrative_models"
        ]
    )
    c4_12 = sec12["section_5_signed_cancellation_investigation"]
    assert (
        "-d[x^{-1/2} h_0(x/X)]"
        in c4_12["chordal_prime_power_stieltjes_equivalence"][
            "closed_form_chordal_jump_integral"
        ]
    )
    assert (
        "psi_1(x) := int_1^x psi(t) dt = (x^2 - 1)/2 + E_1(x)"
        in c4_12["next_justified_refinement_chebyshev_primitive_transfer"][
            "normalized_primitive_definition"
        ]
    )
    assert (
        "M[h_1](z) = (z + 1/2)(z + 3/2) H_0(z) = rho(rho + 1) H_0(z)"
        in c4_12["next_justified_refinement_chebyshev_primitive_transfer"][
            "what_improves_vs_where_obligation_reappears"
        ]
    )

    # 2. Step 3: Prime-shift quadratic form D_N(f)
    sec2 = sec13["section_2_prime_shift_quadratic_form"]
    assert (
        sec2["lean_theorem"]
        == "prime_shift_quadratic_form_and_subtracted_finite_part_equivalence"
    )
    cutoff_rows = sec2["cutoff_evaluation_table"]
    assert len(cutoff_rows) == 4
    for row in cutoff_rows:
        assert row["D_N_psi_tau_positive"] is True
        assert row["D_N_f_minus_K1_positive"] is True
        assert row["D_N_f_plus_K1_positive"] is True
        assert row["subtracted_equals_neg_W_prime_N_encloses_zero"] is True
    # Verify D_N(psi_tau) - 2 L_N ||psi_tau||^2 converges to -2 W(1) ~ +0.114614959 while 2 L_N ||psi_tau||^2 grows as ~ 4 sqrt(N) h_0(1):
    assert cutoff_rows[-1]["two_L_N_norm_psi_tau_sq_mid"] > 300.0
    assert math.isclose(
        cutoff_rows[-1]["subtracted_D_N_minus_2LN_psi_tau_mid"],
        0.11461495924093341,
        rel_tol=1e-6,
    )
    sm_rows = sec2["scale_matched_cutoff_table"]
    assert len(sm_rows) == 4
    assert (
        sm_rows[-1]["trivial_lower_bound_from_D_N_nonneg_neg_2LN_norm_mid"]
        < -90.0
    )

    # 3. Step 4: Divisor-aggregated functional W_log(X) and exact Moebius inversion
    sec3 = sec13["section_3_divisor_aggregated_candidate_and_moebius_inversion"]
    assert (
        sec3["lean_theorem"]
        == "divisor_aggregated_stieltjes_and_moebius_inversion_identity"
    )
    vm = sec3["vanishing_zeroth_and_first_logarithmic_moments"]
    assert vm["H0_at_half_zero"] is True
    assert vm["H0_prime_at_half_contains_zero"] is True
    assert vm["H0_prime_at_half_abs_upper"] < 1e-13

    st_rep = sec3["exact_stieltjes_representation"]
    assert st_rep["boundary_rational_coeff"] == "30731/98304"
    assert st_rep["M_tilde_h_0_tv_equals_two_sum_extrema"] is True
    assert st_rep["M_tilde_h_log_methods_overlap"] is True
    assert st_rep["signed_tilde_h_log_moment_encloses_zero"] is True
    assert math.isclose(
        st_rep["M_tilde_h_0_minus_3_2_mid"], 2.4304910449396404, rel_tol=1e-13
    )
    assert math.isclose(
        st_rep["M_tilde_h_log_minus_3_2_mid"], 1.2118101520691849, rel_tol=1e-13
    )
    assert 3.34 < st_rep["unconditional_global_max_on_X_ge_1"] < 3.36

    fc_checks = sec3["certified_finite_cutoff_checks"]
    assert len(fc_checks) == 4
    for fc in fc_checks:
        assert fc["stieltjes_decomp_encloses_zero"] is True
        assert fc["stieltjes_decomp_abs_upper"] < 1e-24
        assert fc["B_log_boundary_within_rational_bound"] is True
        assert fc["B_log_ibp_identity_encloses_zero"] is True
        assert fc["moebius_inversion_finite_cutoff_encloses_zero"] is True
        assert fc["moebius_inversion_finite_cutoff_abs_upper"] < 1e-50

    w_log_rows = sec3["certified_w_log_scale_enclosures"]
    assert len(w_log_rows) == 7
    for w_row in w_log_rows:
        assert w_row["certified_within_unconditional_stirling_bound"] is True
        assert w_row["W_log_abs_upper"] < 0.08

    # 4. Step 4 & Step 5: Premise classification & diagnostic controls
    sec4 = sec13["section_4_premise_classification_and_next_lemma"]
    assert len(sec4["category_i_already_proved_in_repository"]) == 4
    assert len(sec4["category_ii_unconditional_external_theorems"]) == 4
    assert len(sec4["category_iii_new_statements_proved_in_task_tc044"]) == 3
    assert (
        sec4["category_iv_unproved_premise"]["subgate_id"] == "SUBGATE-TC-043A"
    )

    sec5 = sec13["section_5_diagnostics_and_controls"]
    assert len(sec5["modified_weight_controls"]) == 5
    sq_ctrl = sec5["synthetic_off_critical_quartet_divisor_aggregation_control"]
    assert sq_ctrl["zeta_at_rho_0_certified_nonzero"] is True
    assert sq_ctrl["abs_divisor_aggregated_quartet_amplitude_mid"] > 0.0
    assert (
        sq_ctrl["mellin_convention_and_common_strip"][
            "common_absolute_convergence_strip"
        ]
        == "1/2 < Re(z) < 5/2"
    )
    assert (
        sq_ctrl["isolated_mode_divergence_and_regularization"][
            "regularized_error_below_1e_3"
        ]
        is True
    )


def test_28_task_tc045_cross_grade_moebius_recovery_and_serialization_roundtrip(
    artifact_payload,
):
    """Verify TASK-TC-045 cross-grade compatibility, Moebius recovery, Mellin strip & regularization, continuity, Mertens IBP, and round-trip Arb enclosure."""
    assert artifact_payload["moebius_recovery_task_id"] == TASK_TC_045_ID
    dims = artifact_payload["status_dimensions"]
    assert (
        dims["cross_grade_moebius_recovery_status"]
        == CROSS_GRADE_MOEBIUS_RECOVERY_STATUS
    )
    assert dims["rh_proved"] is False

    sec14 = artifact_payload[
        "section_14_cross_grade_compatibility_and_moebius_recovery"
    ]
    assert sec14["task_id"] == TASK_TC_045_ID
    assert sec14["status"] == CROSS_GRADE_MOEBIUS_RECOVERY_STATUS

    # 1. Section 1 & 2: Recovered arithmetic result and complete implication chain
    s1 = sec14["section_1_recovered_arithmetic_result_and_implication_chain"]
    assert (
        "R_mu(X) := sum_{m>=2} (mu(m)/sqrt(m)) W_log(X/m)"
        in s1["exact_moebius_recovery_and_equivalence"]["moebius_decomposition"]
    )
    assert (
        "does NOT independently establish"
        in s1["exact_moebius_recovery_and_equivalence"]["equivalence_statement"]
    )
    imp = s1["complete_implication_chain_to_correlation_bound"]
    assert (
        imp["lean_theorem"]
        == "mixed_grade_pairing_moebius_recovery_and_semiboundedness_equivalence"
    )
    assert (
        "tau^K and tau^{-K}"
        in imp[
            "step_2_both_scale_directions_in_mixed_and_two_grade_prime_pairings"
        ]
    )

    # 2. Section 3: Repaired TC-044 defects (Mellin strip + synthetic quartet regularization + round-trip Arb serialization)
    s2 = sec14["section_2_repaired_tc044_defects_audit"]
    d3a = s2["defect_3a_spectral_aggregation_and_synthetic_quartet_repair"]
    assert (
        d3a["mellin_transform_conventions"]["symbolic_scale_shift_verified"]
        is True
    )
    cs = d3a["common_strip_fubini_tonelli_derivation"]
    assert cs["common_strip"] == "1/2 < Re(z) < 5/2"
    assert cs["strip_aggregation_identity_encloses_zero"] is True
    assert cs["strip_moebius_identity_encloses_zero"] is True
    reg_table = d3a["synthetic_quartet_convergence_and_regularization"][
        "regularization_convergence_table"
    ]
    assert len(reg_table) == 3
    # Euler-Maclaurin order-1 and order-2 regularized errors strictly decrease with M while unsubtracted distance stays O(1):
    assert (
        reg_table[0]["euler_maclaurin_order1_error_upper"]
        > reg_table[1]["euler_maclaurin_order1_error_upper"]
        > reg_table[2]["euler_maclaurin_order1_error_upper"]
    )
    assert reg_table[2]["euler_maclaurin_order2_error_upper"] < 1e-7

    d3b = s2["defect_3b_numerical_serialization_and_roundtrip_repair"]
    assert d3b["all_acceptance_comparisons_in_interval_arithmetic"] is True
    assert (
        d3b["all_sample_roundtrips_enclose_original_256bit_arb_ball"] is True
    )
    for sample_name, sample_entry in d3b[
        "roundtrip_sample_verifications"
    ].items():
        ver = sample_entry["verification"]
        assert ver["decimal_endpoints_enclose_original"] is True, sample_name
        assert ver["arb_ball_str_encloses_original"] is True, sample_name
        assert (
            ver["outward_float_mid_rad_encloses_original"] is True
        ), sample_name
        assert ver["all_reconstructions_enclose_original"] is True, sample_name

    # Perform direct independent 256-bit Arb round-trip enclosure test on live Arb balls:
    from flint import ctx as flint_ctx

    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau_a = arb(2) * arb.pi()
        c_tau_b_live = (
            (arb(4) * tau_a).log()
            + arb.const_euler()
            + tau_a / arb(4)
            - arb(2)
        )
        h0_1_live = evaluate_h0_arb(arb(1))
        for live_ball, exported_key in (
            (c_tau_b_live, "c_tau_B"),
            (h0_1_live, "h0_at_1"),
        ):
            payload_json = d3b["roundtrip_sample_verifications"][exported_key][
                "serialized"
            ]
            rt_check = verify_serialized_arb_roundtrip(live_ball, payload_json)
            assert rt_check["all_reconstructions_enclose_original"] is True
            # Also check that serialize_arb_certified reproduces an enclosing interval:
            fresh_ser = serialize_arb_certified(live_ball)
            assert (
                verify_serialized_arb_roundtrip(live_ball, fresh_ser)[
                    "all_reconstructions_enclose_original"
                ]
                is True
            )
    finally:
        flint_ctx.prec = saved_prec

    # 3. Section 4: Continuity and the role of algebraic grades A_R = Qbar intersect R
    s3 = sec14["section_3_continuity_and_algebraic_grades_role"]
    ss_rows = s3["small_scale_decay_lemma"]["certified_small_scale_table"]
    assert len(ss_rows) == 7
    for s_row in ss_rows:
        assert s_row["certified_within_C_log_0_u_5_2_bound"] is True
    # Check that as u -> 0^+, |W_log(u)| / u^{5/2} approaches (81/64)(-zeta'(3)) ~ 0.25069158:
    assert math.isclose(
        ss_rows[-1]["ratio_abs_W_log_to_u_5_2_mid"],
        ss_rows[-1]["asymptotic_limit_81_64_neg_zeta_prime_3"],
        rel_tol=2e-3,
    )
    ct_rows = s3["compact_interval_uniform_convergence_and_continuity"][
        "compact_tail_bounds_table"
    ]
    assert len(ct_rows) == 6
    assert (
        "does NOT weaken its uniform boundedness requirement"
        in s3["role_of_algebraic_grades_A_R"]["narrow_scope_statement"]
    )

    # 4. Section 5: Mixed-grade pairing polarization & Mertens Stieltjes representation
    s4 = sec14["section_4_mixed_grade_relation_and_moebius_recovery"]
    mp = s4["mixed_grade_polarization_identity"]
    assert (
        mp["lean_theorem"]
        == "mixed_grade_pairing_moebius_recovery_and_semiboundedness_equivalence"
    )
    assert (
        mp["unconditional_bound_on_B_known"]["certified_below_9_4468"] is True
    )
    mg_rows = mp["certified_mixed_grade_table"]
    assert len(mg_rows) == 5
    for m_row in mg_rows:
        assert m_row["W_minus_W_log_plus_R_mu_encloses_zero"] is True
        assert m_row["W_minus_W_log_plus_R_mu_abs_upper"] < 0.05

    cov_ctrl = s4[
        "simultaneous_grade_covariance_and_counterexample_control"
    ]
    ce_rows = cov_ctrl["counterexample_evaluation_table"]
    assert len(ce_rows) == 5
    assert all(r["shift_invariance_exact"] is True for r in ce_rows)
    assert ce_rows[-1]["cosh_envelope_mid"] > 9.0 * ce_rows[0]["cosh_envelope_mid"]

    mert = s4["mertens_stieltjes_representation_of_R_mu"]
    assert mert["symbolic_derivative_verified"] is True
    assert (
        mert["lean_theorem"]
        == "small_scale_w_log_tail_and_mertens_stieltjes_ibp_identity"
    )
    m_checks = mert["certified_finite_cutoff_checks"]
    assert len(m_checks) == 4
    for mc in m_checks:
        assert mc["abel_summation_by_parts_encloses_zero"] is True
        assert mc["abel_summation_by_parts_abs_upper"] < 1e-50
        assert mc["stieltjes_integral_ibp_encloses_zero"] is True
        assert mc["stieltjes_integral_ibp_abs_upper"] < 1e-24

    s5 = sec14["section_5_premise_classification_and_next_lemma"]
    assert len(s5["category_i_already_proved_in_repository"]) == 3
    assert len(s5["category_ii_unconditional_external_theorems"]) == 4
    assert len(s5["category_iii_new_statements_proved_in_task_tc045"]) == 3
    assert (
        s5["category_iv_unproved_premise"]["subgate_id"] == "SUBGATE-TC-043A"
    )


def test_29_task_tc045r_norm_floor_transfer_bound_mellin_pole_and_live_regressions(
    artifact_payload,
):
    """Verify TASK-TC-045R mathematical repairs and live 256-bit Arb regressions for Steps 2, 3, 4, 5, 6, and 7."""
    from flint import ctx as flint_ctx

    assert artifact_payload["moebius_recovery_repair_task_id"] == TASK_TC_045R_ID
    assert (
        artifact_payload["moebius_recovery_followup_repair_task_id"]
        == TASK_TC_045R2_ID
    )
    assert (
        STARTING_HEAD_TC_045R2
        == "71398c70c049b53d3546a7258ccda765481114f7"
    )
    assert (
        artifact_payload["moebius_recovery_followup_repair_starting_head"]
        == STARTING_HEAD_TC_045R2
    )
    sec13 = artifact_payload[
        "section_13_prime_shift_quadratic_form_and_divisor_aggregation"
    ]
    sec14 = artifact_payload[
        "section_14_cross_grade_compatibility_and_moebius_recovery"
    ]
    assert sec14["repair_task_id"] == TASK_TC_045R_ID
    assert sec14["followup_repair_task_id"] == TASK_TC_045R2_ID
    assert sec14["followup_repair_inspected_baseline"] == STARTING_HEAD_TC_045R2

    s1 = sec14["section_1_recovered_arithmetic_result_and_implication_chain"]
    imp = s1["complete_implication_chain_to_correlation_bound"]
    nft = s1["norm_floor_and_transfer_bound_repair_tc045r"]

    # 1. Step 2: Norm-floor behavior of f_pm^{(K)} at K = 0, K = +/- 1/4, and small rational grades K = +/- 1/100, +/- 1/1000
    assert "plus_state_norm_floor_certified" not in nft
    assert (
        nft["exact_two_grade_norm_identity"]
        == "||f_pm^{(K)}||_{L^2}^2 = h_0(1) +/- h_0(tau^{|K|})"
    )
    assert (
        nft["valid_two_grade_norm_bounds"]
        == "0 <= ||f_pm^{(K)}||_{L^2}^2 <= 2 h_0(1) for all K in A_R"
    )
    assert "Excluding K = 0 does NOT produce" in nft["minus_state_vanishing_as_K_to_0"]
    assert (
        "0.243250897826609" in nft["plus_state_counterexample_at_K_pm_1_4"]
    )
    nf_by_label = {
        row["K_label"]: row for row in nft["two_grade_norm_and_transfer_table"]
    }
    assert nf_by_label["0"]["norm_f_minus_sq_certified"]["mid_float"] == 0.0
    assert (
        0.0
        < nf_by_label["1/1000"]["norm_f_minus_sq_certified"]["mid_float"]
        < nf_by_label["1/100"]["norm_f_minus_sq_certified"]["mid_float"]
        < 3e-3
    )
    for k_lbl in ("0", "1/1000", "-1/1000", "1/100", "-1/100", "1/10"):
        assert nf_by_label[k_lbl]["norm_f_minus_sq_below_false_floor_0_258495"] is True
    for k_lbl in ("1/4", "-1/4"):
        assert nf_by_label[k_lbl]["norm_f_plus_sq_in_0_2432_0_2433"] is True
        assert nf_by_label[k_lbl]["norm_f_plus_sq_below_false_floor_0_258495"] is True
        assert (
            0.2432
            < nf_by_label[k_lbl]["norm_f_plus_sq_certified"]["mid_float"]
            < 0.2433
        )
    assert math.isclose(
        nf_by_label["-1/4"]["norm_f_plus_sq_certified"]["mid_float"],
        nf_by_label["1/4"]["norm_f_plus_sq_certified"]["mid_float"],
        rel_tol=1e-14,
    )
    assert math.isclose(
        nf_by_label["-1/1000"]["norm_f_minus_sq_certified"]["mid_float"],
        nf_by_label["1/1000"]["norm_f_minus_sq_certified"]["mid_float"],
        rel_tol=1e-14,
    )
    assert math.isclose(
        nf_by_label["-1/100"]["norm_f_minus_sq_certified"]["mid_float"],
        nf_by_label["1/100"]["norm_f_minus_sq_certified"]["mid_float"],
        rel_tol=1e-14,
    )

    # 2. Step 3: Corrected transfer-term bound across K = 0, small |K|, and large |K|
    tb_false = nft["false_0_633039_transfer_bound_reproduction_and_origin"]
    tb_planch = nft["proven_plancherel_transfer_bounds"]
    assert (
        tb_planch["operator_R0_definition"]
        == "(R_0 f)(x) = int_0^x (y/x)^{1/2} (D_y f)(y) dy/y,   D_y = y d/dy"
    )
    assert (
        "b(t) = 2 - 1/(t^2 + 1/4) in [-2, 2]"
        in tb_planch["polarized_mixed_bound_formula"]
    )
    assert (
        tb_planch["lean_theorem"]
        == "transfer_form_plancherel_bound_and_minus_state_vanishing"
    )
    assert tb_false["B_transfer_f_plus_0_certified"]["mid_float"] > 1.93
    assert tb_false["B_transfer_psi_tau_certified"]["mid_float"] > 0.96
    assert (
        1.98944
        < tb_planch["two_grade_uniform_bound_4_h0_1_certified"]["mid_float"]
        < 1.98946
    )
    assert (
        0.99472
        < tb_planch["mixed_grade_uniform_bound_2_h0_1_certified"]["mid_float"]
        < 0.99473
    )
    for row in nft["two_grade_norm_and_transfer_table"]:
        assert row["abs_B_transfer_f_minus_le_2_norm_minus_sq"] is True
        assert row["abs_B_transfer_f_plus_le_2_norm_plus_sq"] is True
        assert row["abs_B_transfer_f_pm_le_4_h0_1"] is True
        assert row["abs_B_transfer_mixed_le_2_h0_1"] is True
        assert row["refutes_false_0_633039_bound"] is True

    # 3. Step 4: Mixed-grade decomposition with retained transfer term and both scale directions
    mp = sec14["section_4_mixed_grade_relation_and_moebius_recovery"][
        "mixed_grade_polarization_identity"
    ]
    assert "B_transfer(T_K psi_tau, T_L psi_tau)" in mp["formula"]
    assert "W(tau^{-|K-L|})" in mp["formula"]
    assert "W_log(tau^{|K-L|})" in mp["formula"]
    assert (
        "without dividing by ||f_-^{(K)}||_{L^2}^2"
        in imp[
            "step_4_direct_equivalence_to_correlation_bound_and_separate_conditional_semiboundedness"
        ]
    )
    b_known = mp["unconditional_bound_on_B_known"]
    assert b_known["certified_below_9_4468"] is True
    assert b_known["certified_below_7_07943_via_operator_transfer"] is True
    assert 9.277 < b_known["B_known_universal_upper_bound"] < 9.278
    assert (
        7.0794
        < b_known["B_known_operator_plus_transfer_upper_bound"]
        < 7.0795
    )
    for m_row in mp["certified_mixed_grade_table"]:
        assert m_row["smooth_plus_transfer_equals_W_arch_encloses_zero"] is True
        assert m_row["abs_B_known_below_operator_transfer_bound"] is True
        assert m_row["Q_tau_equals_B_known_minus_R_mu_encloses_zero"] is True

    # 4. Step 5: Mellin pole behavior of -H_0(z) zeta'(z + 1/2) at z = 5/2
    d3a_pole = sec14["section_2_repaired_tc044_defects_audit"][
        "defect_3a_spectral_aggregation_and_synthetic_quartet_repair"
    ]["kernel_strip_holomorphy_vs_global_poles"]
    assert d3a_pole["holomorphic_open_strip"] == "|Re(z)| < 5/2"
    assert d3a_pole["is_entire_on_C"] is False
    assert d3a_pole["res_H0_at_5_2_rational"] == "81/64"
    assert d3a_pole["res_H0_at_5_2_symbolic_verified"] is True
    assert d3a_pole["res_neg_H0_zeta_prime_at_5_2_certified_nonzero"] is True
    assert math.isclose(
        d3a_pole["res_neg_H0_zeta_prime_at_5_2_certified"]["mid_float"],
        0.25075352615213414,
        rel_tol=1e-13,
    )

    # 5. Step 6 & 7: Live 256-bit Arb regressions and full-tree round-trip verification
    d3b = sec14["section_2_repaired_tc044_defects_audit"][
        "defect_3b_numerical_serialization_and_roundtrip_repair"
    ]
    rt13 = d3b["full_section_13_tree_roundtrip_verification"]
    rt14 = d3b["full_section_14_tree_roundtrip_verification"]
    assert rt13["all_enclose_original_256bit_arb_ball"] is True
    assert rt14["all_enclose_original_256bit_arb_ball"] is True
    assert rt13["live_original_count_matches_enumerated_total"] is True
    assert rt14["live_original_count_matches_enumerated_total"] is True
    assert (
        rt13["compared_against_live_original_arb_count"]
        == rt13["total_certified_arb_balls_checked"]
        == len(rt13["checked_paths"])
    )
    assert (
        rt14["compared_against_live_original_arb_count"]
        == rt14["total_certified_arb_balls_checked"]
        == len(rt14["checked_paths"])
    )
    enum13_recheck = verify_all_serialized_arb_in_tree(
        sec13, path_prefix="section_13"
    )
    enum14_recheck = verify_all_serialized_arb_in_tree(
        sec14, path_prefix="section_14"
    )
    assert (
        rt13["compared_against_live_original_arb_count"]
        == enum13_recheck["total_certified_arb_balls_checked"]
    )
    assert (
        rt14["compared_against_live_original_arb_count"]
        == enum14_recheck["total_certified_arb_balls_checked"]
    )
    assert all(
        "plus_state_norm_floor_certified" not in p
        for p in rt14["checked_paths"]
    )

    v1 = s1["exact_moebius_recovery_and_equivalence"]["values_at_X_eq_1"]
    assert v1["W_1_is_strictly_negative"] is True
    assert v1["W_1_certified"]["mid_float"] < -0.057
    assert v1["h0_at_9_is_strictly_negative"] is True
    assert v1["h0_at_9_certified"]["mid_float"] < -0.00034

    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau_a = arb(2) * arb.pi()
        h0_1_live = evaluate_h0_arb(arb(1))
        h0_9_live = evaluate_h0_arb(arb(9))
        assert bool(h0_1_live > arb(0))
        assert bool(h0_9_live < arb(0))

        # Live plus-state counterexample at K = +/- 1/4:
        # ||f_+^{(+/- 1/4)}||_{L^2}^2 = h_0(1) + h_0(tau^{1/4}) in (0.2432, 0.2433)
        for k_sign in (1, -1):
            k_1_4 = arb(k_sign) / arb(4)
            h0_tau_1_4 = evaluate_h0_arb(tau_a ** abs(k_1_4))
            norm_plus_1_4 = h0_1_live + h0_tau_1_4
            assert bool(h0_tau_1_4 < arb("-0.2541"))
            assert bool(norm_plus_1_4.lower() > arb("0.2432"))
            assert bool(norm_plus_1_4.upper() < arb("0.2433"))
            assert bool(norm_plus_1_4.upper() < arb("0.258495"))

        # Live minus-state norm-floor check at K = 0, +/-1/1000, +/-1/100
        diff_k0 = h0_1_live - evaluate_h0_arb(arb(1))
        assert bool(diff_k0.contains(0)) and bool(abs(diff_k0) < arb("1e-75"))
        for n_denom in (1000, 100):
            k_arb = arb(1) / arb(n_denom)
            norm_minus = h0_1_live - evaluate_h0_arb((tau_a ** k_arb))
            assert bool(norm_minus > arb(0))
            assert bool(norm_minus < arb("0.003"))

        # Live Plancherel transfer bound check: 4 * h0(1) and 2 * h0(1)
        four_h0_1 = arb(4) * h0_1_live
        two_h0_1 = arb(2) * h0_1_live
        assert bool(four_h0_1 > arb("1.98944")) and bool(
            four_h0_1 < arb("1.98945")
        )
        assert bool(two_h0_1 > arb("0.99472")) and bool(
            two_h0_1 < arb("0.99473")
        )

        # Live pole residue of -H_0(z) * zeta'(z + 1/2) at z = 5/2 (s = 3)
        from flint import acb_series
        neg_zeta_prime_3 = -acb_series([acb(3), acb(1)], prec=flint_ctx.prec).zeta()[1].real
        res_z_5_2_live = (arb(81) / arb(64)) * neg_zeta_prime_3
        assert bool(res_z_5_2_live > arb("0.2507535")) and bool(
            res_z_5_2_live < arb("0.2507536")
        )
        # Verify by evaluating (z - 5/2) * H_0(z) near z = 5/2 that H_0(z) has simple pole of residue +81/64:
        eps_z = arb("1e-30")
        z_near = acb(arb(5) / arb(2) - eps_z)
        h0_z_near = evaluate_f_tau_acb(
            acb(arb(1) / arb(2)) + z_near
        ) * evaluate_f_tau_acb(acb(arb(1) / arb(2)) - z_near)
        approx_res = (-eps_z) * h0_z_near.real
        assert abs(float(approx_res.mid()) - (81.0 / 64.0)) < 1e-12
    finally:
        flint_ctx.prec = saved_prec









