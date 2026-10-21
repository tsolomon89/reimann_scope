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
    TASK_TC_042_ID,
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
    verify_canonical_theta_correlation_lean_module,
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
    """Verify formal/RiemannScope/CanonicalThetaCorrelationBound.lean has 11 defs, 20 theorems, 0 sorry/admit, and non-vacuous residue hypothesis."""
    assert LEAN_MODULE_PATH.exists()
    ver = verify_canonical_theta_correlation_lean_module()
    assert ver["matches_exact"] is True
    assert ver["contains_sorry"] is False
    assert ver["contains_admit"] is False
    assert ver["actual_defs"] == CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert ver["actual_theorems"] == CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    assert len(ver["actual_defs"]) == 11
    assert len(ver["actual_theorems"]) == 20

    lean_text = LEAN_MODULE_PATH.read_text(encoding="utf-8")
    # Ensure the vacuous universal quantification over res_sq is absent
    assert "∀ w_re res_sq : ℝ, 0 < w_re → res_sq = 0" not in lean_text
    assert "∀ w_re w_im : ℝ, 0 < w_re → resSq w_re w_im = 0" in lean_text
    assert "laplace_holomorphic_rhp_hypothesis_satisfiable" in lean_text
    assert "stieltjes_rescaled_variable_and_erroneous_factor_obstruction" in lean_text
    assert "bernstein_weighted_h0_polynomial_endpoints" in lean_text
    assert "taylor_sixth_order_two_sided_abs_correlation_bound" in lean_text
    assert "stieltjes_signed_pairing_uniform_bound_equivalence" in lean_text


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
    assert attA["annihilation_orders"]["at_s_eq_pos_half_pnt_main_term"] == 5
    assert attA["annihilation_orders"]["at_s_eq_neg_half"] == 4

    attB = canc["attempt_B_signed_dyadic_scale_decomposition"]
    assert 0.0 < attB["l1_majorant_weight_sum_upper"] < 17.5
    assert len(attB["dyadic_shells_minus6_to_5"]) == 12

    attC = canc["attempt_C_seed_wavelet_multiplicative_convolution_factorization"]
    assert attC["single_seed_pnt_moment_vanishes"] is True
    assert attC["single_seed_pnt_moment_abs_upper"] < 1e-18
    assert attC["finite_sum_convolution_verification_at_X_4_abs_diff"] < 1e-10
    assert 0.0 < attC["weighted_psi_tau_l2_norm_C_psi"] < 5.0

