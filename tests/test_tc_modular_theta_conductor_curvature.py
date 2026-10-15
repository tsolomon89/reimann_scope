"""Tests for TASK-TC-036: Modular-Covariant Theta-Conductor Curvature Audit."""

from __future__ import annotations

import json
import math
from pathlib import Path

from tc.canonical_selector_audit import audit_canonical_zeta_selector
from tc.modular_theta_conductor_curvature import (
    COMPLETED_THETA_CONDUCTOR_REGULARIZATION_REPAIRED,
    CORRECTED_POLE_REGULARIZER_D_SQUARED_MINUS_ONE_SIXTEENTH,
    UNSHIFTED_REGULARIZER_DOES_NOT_ANNIHILATE_POLES,
    audit_completed_theta_conductor_functional,
    audit_conductor_operator_primary_sources,
    audit_dilation_conductor_commutator,
    audit_linear_quadratic_firewall,
    audit_modular_covariance,
    audit_modular_theta_conductor_curvature,
    audit_no_contradiction_firewall,
    audit_unique_heat_drift_compensator,
    build_task_tc_035_scope_corrections,
    certify_prime_only_covariant_variance_arb,
    compare_heat_and_modular_hessians,
    evaluate_general_drift_operator_L_c,
    evaluate_generic_base_heat_control,
    evaluate_theta_euler_and_heat_jets,
    evaluate_unshifted_vs_corrected_pole_regularizer,
    solve_operator_selector_axioms,
    verify_modular_theta_conductor_lean_map_against_file,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_JSON_PATH = REPO_ROOT / "data" / "tc_modular_theta_conductor_curvature.json"
TC035_JSON_PATH = REPO_ROOT / "data" / "tc_canonical_zeta_selector_audit.json"
LEAN_MODULE_PATH = (
    REPO_ROOT / "formal" / "RiemannScope" / "ModularThetaConductorCurvature.lean"
)

REQUIRED_JSON_KEYS = [
    "task_id",
    "task_completion_status",
    "title",
    "starting_head",
    "substantive_parent_head",
    "task_tc_035_scope_corrections",
    "theta_heat_state",
    "spatial_euler_generator",
    "heat_parameter_generator",
    "heat_scaling_identity",
    "general_drift_operator",
    "unique_drift_compensator",
    "modular_weight",
    "modular_covariant_derivative",
    "heat_hessian",
    "modular_hessian",
    "hessian_comparison",
    "conductor_operator_definition",
    "conductor_domain",
    "fourier_invariance_status",
    "dilation_commutator_status",
    "operator_selector_axioms",
    "operator_uniqueness_status",
    "prime_only_covariant_variance",
    "completed_functional_status",
    "linear_or_quadratic",
    "complete_spectral_transfer_status",
    "natural_zero_pairing",
    "cross_term_status",
    "background_term_status",
    "arithmetic_sign_status",
    "spectral_sign_status",
    "contradiction_status",
    "weil_equivalence_status",
    "generic_base_status",
    "tau_specific_input",
    "primary_source_literature_table",
    "obl_ct_001a_status",
    "obl_ct_001a_completed",
    "rh_claimed",
    "candidate_failure_refutes_tc",
    "principal_classification",
    "exact_remaining_subgate",
    "lean_theorem_map",
    "hypothesis_fidelity",
]


# ---------------------------------------------------------------------------
# 1. TASK-TC-035 Scope Repairs (Tests 01-04)
# ---------------------------------------------------------------------------


def test_01_distribution_vs_prime_power_distinction_repaired():
    """Verify Section 3.1 repair distinguishes zeta(s) from -zeta'(s)/zeta(s) and test-kernel selection."""
    repairs = build_task_tc_035_scope_corrections()
    dist = repairs["distribution_vs_prime_power_distinction"]
    assert dist["zeta_dirichlet_series"] == "zeta(s) = sum_{n>=1} n^{-s}"
    assert (
        dist["von_mangoldt_log_derivative"]
        == "-zeta'(s)/zeta(s) = sum_{n>=2} Lambda(n) n^{-s}"
    )
    assert dist["zeta_and_von_mangoldt_identified_as_one_scalar_ray"] is False
    assert dist["selects_unique_test_kernel"] is False
    assert len(dist["valid_deductive_chain"]) == 3

    tc035 = audit_canonical_zeta_selector()
    sel1 = tc035["candidate_selector_audits"][0]
    assert "zeta(s) = sum_{n>=1} n^{-s}" in sel1["unique_object_selected"]
    assert (
        "-zeta'(s)/zeta(s) = sum_{n>=2} Lambda(n) n^{-s}"
        in sel1["unique_object_selected"]
    )
    assert (
        sel1["selects_unique_test_kernel_status"]
        == "SELECTS_DISTRIBUTION_RAY_NOT_TEST_KERNEL"
    )


def test_02_gaussian_uniqueness_scope_repaired():
    """Verify Section 3.2 repair scopes Gaussian uniqueness to the positive heat/ground-state/minimum-uncertainty class."""
    repairs = build_task_tc_035_scope_corrections()
    g_scope = repairs["gaussian_uniqueness_scope"]
    assert g_scope["full_self_fourier_space_is_one_dimensional"] is False
    assert "positive heat-semigroup" in g_scope["scoped_statement"]
    assert "harmonic-oscillator ground-state" in g_scope["scoped_statement"]
    assert "minimum-uncertainty" in g_scope["scoped_statement"]


def test_03_theta_certificate_parameters_consistent_at_n15():
    """Verify Section 3.3 repair keeps N_cutoff = 15 and outward tail bound ~ 4.91e-347 without narrative N=60 or 10^-3400."""
    repairs = build_task_tc_035_scope_corrections()
    params = repairs["canonical_theta_certificate_parameters"]
    assert params["committed_N_cutoff"] == 15
    assert "4.90944663560190599562356800150073399e-347" in (
        params["committed_outward_tail_bound_str"]
    )
    assert "N=60" in params["uncommitted_narrative_values_removed"]
    assert "10^{-3400}" in params["uncommitted_narrative_values_removed"]

    tc035_doc = (
        REPO_ROOT / "docs" / "reviews" / "TC_CANONICAL_ZETA_SELECTOR_AUDIT.md"
    ).read_text(encoding="utf-8")
    assert "N_{\\mathrm{cutoff}} = 15" in tc035_doc
    assert "N=60" not in tc035_doc
    assert "10^{-3400}" not in tc035_doc


def test_04_trilemma_lean_scope_accurately_reported():
    """Verify Section 3.4 repair distinguishes SIX_STANDARD_SELECTOR_FAMILIES_AUDITED from CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED."""
    repairs = build_task_tc_035_scope_corrections()
    tri = repairs["selector_trilemma_scope"]
    assert tri["families_audited_status"] == "SIX_STANDARD_SELECTOR_FAMILIES_AUDITED"
    assert (
        tri["lean_dichotomy_status"]
        == "CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED"
    )
    assert tri["lean_proves_all_possible_selectors_exhausted"] is False


# ---------------------------------------------------------------------------
# 2. Heat Scaling and Drift Compensation (Tests 05-09)
# ---------------------------------------------------------------------------


def test_05_euler_heat_scaling_first_order():
    """Verify E Theta_t = 2 D Theta_t across sample points and heat scales."""
    for x, y, t in [(2.0, 3.0, 0.7), (1.5, 2.5, 1.0), (3.0, 4.0, 1.4)]:
        res = evaluate_theta_euler_and_heat_jets(x, y, t)
        assert res["E_minus_2D_abs_err"] < 1e-13
        assert math.isclose(
            res["E_theta_t"], res["two_D_theta_t"], rel_tol=1e-13, abs_tol=1e-15
        )


def test_06_euler_heat_scaling_second_order():
    """Verify E^2 Theta_t = 4 D^2 Theta_t = 4 t^2 d_t^2 Theta_t + 4 t d_t Theta_t."""
    for x, y, t in [(1.2, 1.8, 0.8), (2.0, 2.5, 1.0), (1.5, 3.0, 1.25)]:
        res = evaluate_theta_euler_and_heat_jets(x, y, t)
        assert res["E2_expansion_abs_err"] < 1e-12
        assert math.isclose(
            res["E2_theta_t"],
            4.0 * res["D2_theta_t"],
            rel_tol=1e-12,
            abs_tol=1e-14,
        )
        assert math.isclose(
            res["E2_theta_t"],
            res["four_t2_dt2_plus_4t_dt1"],
            rel_tol=1e-12,
            abs_tol=1e-14,
        )


def test_07_general_drift_operator_formula():
    """Verify L_c Theta_t = (E^2 - c E) Theta_t = 4 t^2 d_t^2 Theta_t + (4 - 2c) t d_t Theta_t."""
    for c in [-2.0, -0.5, 0.0, 1.0, 2.0, 3.5]:
        res = evaluate_general_drift_operator_L_c(c, 1.5, 2.0, t=1.1)
        assert res["drift_coefficient_4_minus_2c"] == 4.0 - 2.0 * c
        assert res["expansion_abs_err"] < 1e-12


def test_08_c_equals_2_uniquely_cancels_heat_drift():
    """Verify c = 2 uniquely cancels the first-order t d/dt drift term in L_c = E(E - c)."""
    comp = audit_unique_heat_drift_compensator()
    assert comp["unique_compensator_c"] == 2.0
    assert comp["classification"] == "HEAT_DRIFT_COMPENSATOR_UNIQUELY_FORCED"
    assert (
        comp["decision_tree_status"]
        == "HEAT_DRIFT_COMPENSATOR_UNIQUE_BUT_NOT_MODULAR_SELECTOR"
    )
    assert comp["is_modularly_canonical"] is False
    assert comp["max_c2_drift_residual"] < 1e-9


def test_09_c_not_equal_2_leaves_nonzero_drift_controls():
    """Verify c in {0, 1, -1, 3} leaves a nonzero drift coefficient 4 - 2c != 0."""
    comp = audit_unique_heat_drift_compensator()
    controls = comp["non_c2_controls"]
    expected_coeffs = {
        "c=0.0": 4.0,
        "c=1.0": 2.0,
        "c=-1.0": 6.0,
        "c=3.0": -2.0,
    }
    for key, exp_coeff in expected_coeffs.items():
        assert key in controls
        assert controls[key]["drift_coefficient_4_minus_2c"] == exp_coeff
        assert controls[key]["drift_coefficient_4_minus_2c"] != 0.0


# ---------------------------------------------------------------------------
# 3. Modular Covariance (Tests 10-12)
# ---------------------------------------------------------------------------


def test_10_modular_weight_normalization_involution():
    """Verify weight-normalized state tilde{f}(t) = t^{w/2} f(t) satisfies tilde{f}(1/t) = tilde{f}(t)."""
    mod = audit_modular_covariance()
    assert mod["weight_1d_theta"] == 0.5
    assert mod["weight_2d_product_theta"] == 1.0
    assert mod["max_involution_abs_err_1d_w_half"] < 1e-12
    assert mod["max_involution_abs_err_2d_w_one"] < 1e-12


def test_11_modular_covariant_first_derivative_vanishes_at_self_dual_point():
    """Verify nabla_w f(1) = ((t d/dt + w/2) f)(1) = 0 at the self-dual point t = 1."""
    mod = audit_modular_covariance()
    assert mod["self_dual_first_derivative_vanishes_verified"] is True
    assert abs(mod["nabla_1_2_theta_1d_at_t_eq_1"]) < 1e-12
    assert abs(mod["nabla_1_theta_2d_at_t_eq_1"]) < 1e-12


def test_12_heat_and_modular_hessian_difference_identity():
    """Verify 4 H_{mod,1} - L_heat = 8 D + 1 = 4 E + 1 and that the two operators do not coincide."""
    diff = compare_heat_and_modular_hessians()
    assert diff["exact_operator_difference"] == "4*H_{mod,1} - L_heat = 8*D + 1 = 4*E + 1"
    assert diff["operators_coincide"] is False
    assert diff["modular_hessian_removes_heat_drift"] is False
    assert diff["heat_compensator_is_modularly_covariant"] is False
    assert diff["difference_identity_abs_err"] < 1e-14
    assert (
        "HEAT_AND_MODULAR_HESSIANS_DIFFER_BY_FORCED_CONNECTION_TERMS"
        in diff["classifications"]
    )
    assert "MODULAR_HESSIAN_DOES_NOT_REMOVE_HEAT_DRIFT" in diff["classifications"]
    assert "HEAT_COMPENSATOR_NOT_MODULARLY_FORCED" in diff["classifications"]
    assert (
        "MODULAR_HESSIAN_DIFFERS_FROM_HEAT_COMPENSATOR" in diff["classifications"]
    )


# ---------------------------------------------------------------------------
# 4. Conductor Operator and Commutator Audit (Tests 13-16)
# ---------------------------------------------------------------------------


def test_13_conductor_operator_primary_source_fields_recorded():
    """Verify Section 9 primary-source Burnol conductor definitions and 5-row comparison table."""
    cond = audit_conductor_operator_primary_sources()
    assert "H_nu = A + B" in cond["conductor_operator_definition"]
    assert "Delta(K_nu)" in cond["conductor_domain"]
    assert (
        cond["fourier_invariance_status"]
        == "PROVED_ON_INVARIANT_CORE_DELTA_BY_BURNOL_THEOREM_E2"
    )
    table = cond["object_comparison_table"]
    assert len(table) == 5
    objects = [row["object"] for row in table]
    assert any("Multiplication by log|x|_nu" in o for o in objects)
    assert any("Fourier-conjugate logarithmic operator" in o for o in objects)
    assert any("Local conductor operator" in o for o in objects)
    assert any("Global sum over places" in o for o in objects)
    assert any("Global explicit-formula distribution" in o for o in objects)


def test_14_dilation_commutator_with_log_x_and_fourier_log():
    """Verify [A_dil, A] = I and [A_dil, B] = -I cancel to give [A_dil, C] = 0."""
    comm = audit_dilation_conductor_commutator()
    assert comm["commutator_A_dil_with_A"] == "I"
    assert comm["commutator_A_dil_with_B"] == "-I"
    assert comm["commutator_A_dil_with_C"] == "0"
    assert comm["double_commutator_A_dil_with_C"] == "0"
    assert comm["comm_A_scalar_coeff"] == 1.0
    assert comm["comm_B_scalar_coeff"] == -1.0
    assert comm["comm_C_scalar_coeff"] == 0.0
    assert comm["double_comm_C_scalar_coeff"] == 0.0


def test_15_conductor_dilation_commutator_status_recorded():
    """Verify CONDUCTOR_COMMUTES_WITH_DILATION and CONDUCTOR_DILATION_COMMUTATION_REMOVES_NEW_GRADE_SIGNAL."""
    comm = audit_dilation_conductor_commutator()
    assert comm["status"] == "CONDUCTOR_COMMUTES_WITH_DILATION"
    assert (
        comm["secondary_status"]
        == "CONDUCTOR_DILATION_COMMUTATION_REMOVES_NEW_GRADE_SIGNAL"
    )
    assert comm["removes_new_grade_curvature_from_conductor_commutators"] is True


def test_16_operator_selector_axiom_system_has_no_fitted_coefficients():
    """Verify Section 11 operator selector system uses no fitted coefficients and proves joint inconsistency at 2nd order."""
    sel = solve_operator_selector_axioms()
    assert sel["fitted_coefficients_used"] is False
    assert len(sel["axioms_audited"]) == 8
    sol = sel["joint_linear_system_solution_for_scale_part"]
    assert sol["c_0"] == 0.0
    assert sol["c_1"] == 0.0
    assert sol["c_2"] == 0.0
    assert sol["c_4"] == 0.0
    assert sol["second_order_scale_term_survives_joint_axioms"] is False


# ---------------------------------------------------------------------------
# 5. Prime-Only and Completed Functionals (Tests 17-30)
# ---------------------------------------------------------------------------


def test_17_prime_only_covariant_variance_identity():
    """Verify C_prime^cov(t) = A_0(t) A_{2,cov}(t) - A_1(t)^2 = 4*pi^2*t^2*(M_0 M_2 - M_1^2)."""
    cert = certify_prime_only_covariant_variance_arb()
    assert cert["certified"] is True
    assert cert["identity_verified"] is True


def test_18_prime_only_covariant_variance_strictly_positive_arb():
    """Verify 128-bit Arb certification that C_prime^cov(1) > 0 with zero excluded."""
    cert = certify_prime_only_covariant_variance_arb()
    assert cert["status"] == "PRIME_ONLY_COVARIANT_VARIANCE_POSITIVE_CERTIFIED"
    assert cert["zero_excluded"] is True
    assert cert["covariant_variance_enclosure"]["strictly_positive"] is True
    assert (
        cert["infinite_lattice_covariant_variance_enclosure"]["strictly_positive"]
        is True
    )
    lo, hi = cert["covariant_variance_enclosure"]["outward_float_interval"]
    assert lo > 1.6e-26
    assert hi >= lo


def test_19_prime_only_covariant_variance_labeled_control_not_completed_zeta():
    """Verify prime-only covariant variance is explicitly marked as a control theorem and not a completed-zeta constraint."""
    cert = certify_prime_only_covariant_variance_arb()
    assert cert["is_control_theorem_only"] is True
    assert cert["is_completed_zeta_constraint"] is False


def test_20_positive_arithmetic_and_positive_spectral_not_treated_as_contradiction():
    """Verify Section 14 no-contradiction firewall: A_arith >= 0 and A_spec >= 0 is not a contradiction."""
    fw = audit_no_contradiction_firewall()
    assert fw["incompatible_sign_pair_present"] is False
    assert (
        fw["classification"]
        == "POSITIVE_ARITHMETIC_VARIANCE_HAS_NO_CONTRADICTORY_SPECTRAL_LAW"
    )
    assert len(fw["valid_contradiction_templates"]) == 3


def test_21_linear_and_quadratic_functionals_strictly_distinguished():
    """Verify Section 12 linear vs quadratic functional firewall."""
    lq = audit_linear_quadratic_firewall()
    assert (
        lq["linear_functional"]["spectral_classification"]
        == "SIGNED_SINGLE_ZERO_SUM"
    )
    assert (
        lq["quadratic_variance_functional"]["spectral_classification"]
        == "UNRESTRICTED_DOUBLE_ZERO_SUM"
    )
    assert lq["transfer_of_quadratic_positivity_to_linear_sum_allowed"] is False
    assert lq["conflation_error_code"] == "LINEAR_QUADRATIC_FUNCTIONAL_CONFLATION"


def test_22_completed_theta_conductor_functional_includes_all_background_terms():
    """Verify Section 15 completed functional includes prime, pole, trivial/Gamma, conductor, normalization, and regularization terms."""
    comp = audit_completed_theta_conductor_functional()
    assert comp["defined_without_nontrivial_zero_coordinates"] is True
    assert comp["all_background_terms_explicit"] is True
    bg = comp["background_terms_included"]
    for key in [
        "prime_power_terms",
        "pole_terms_s_eq_0_and_1",
        "trivial_zero_and_archimedean_gamma_terms",
        "normalization_terms",
        "regularization_at_origin_and_infinity",
        "operator_domain_condition",
    ]:
        assert key in bg and len(bg[key]) > 0


def test_23_complete_spectral_transfer_classification_honest():
    """Verify Section 16 complete spectral transfer is classified as UNRESTRICTED_DOUBLE_ZERO_SUM (quadratic) and SIGNED_SINGLE_ZERO_SUM (linear)."""
    comp = audit_completed_theta_conductor_functional()
    spec = comp["complete_spectral_representation"]
    assert spec["linear_transfer_classification"] == "SIGNED_SINGLE_ZERO_SUM"
    assert spec["quadratic_transfer_classification"] == "UNRESTRICTED_DOUBLE_ZERO_SUM"
    assert spec["convolution_square_classification"] == "HERMITIAN_WEIL_FORM"
    assert spec["includes_multiplicities"] is True
    assert spec["includes_reflections_and_conjugates"] is True
    assert spec["includes_cross_zero_terms"] is True


def test_24_natural_zero_pairing_audit_honest():
    """Verify Section 17 natural zero-pairing audit reports THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL."""
    comp = audit_completed_theta_conductor_functional()
    pair = comp["natural_zero_pairing_audit"]
    assert (
        pair["pairing_classification"]
        == "THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL"
    )
    assert pair["conjugate_block_selected_by_hand"] is False
    assert pair["conjugate_pair_rho_bar_rho"]["isolated_by_completed_functional"] is False
    assert (
        pair["reflection_pair_rho_1_minus_bar_rho"][
            "isolated_by_completed_functional"
        ]
        is False
    )
    assert pair["general_double_pair_rho_sigma"]["present_in_quadratic_variance"] is True


def test_25_complement_sign_not_promoted_without_proof():
    """Verify Section 18 complement sign audit does not promote R_comp >= 0 or R_comp = 0 without proof."""
    comp = audit_completed_theta_conductor_functional()
    cs = comp["complement_sign_audit"]
    assert cs["R_comp_zero_proved"] is False
    assert cs["R_comp_nonneg_proved"] is False
    assert cs["strict_remainder_domination_reused"] is False
    assert cs["finite_truncation_promoted"] is False
    assert cs["status"] == "COMPLEMENT_SIGN_UNCONTROLLED_WITHOUT_WEIL_POSITIVITY"


def test_26_generic_scale_base_control_q_2_e_tau_10():
    """Verify Section 20 generic scale-base control across q in {2, e, tau, 10}."""
    ctrl = evaluate_generic_base_heat_control()
    assert ctrl["classification"] == "GENERIC_HEAT_VARIANCE_NOT_TC_CONSTRAINT"
    assert ctrl["heat_compensator_depends_on_tau"] is False
    assert ctrl["prime_variance_sign_depends_on_tau"] is False
    assert ctrl["max_normalized_ratio_diff_across_q"] < 1e-15
    assert len(ctrl["per_base_evaluations"]) == 4


def test_27_tau_specific_inputs_isolated():
    """Verify Section 20 explicitly isolates the four tau = 2*pi entry points."""
    ctrl = evaluate_generic_base_heat_control()
    tau_inputs = ctrl["tau_specific_entry_points"]
    assert len(tau_inputs) == 4
    assert any("exp(-2*pi*i*x*y)" in s for s in tau_inputs)
    assert any("theta(1/t) = sqrt(t) theta(t)" in s for s in tau_inputs)
    assert any("pi^{-s/2} Gamma(s/2)" in s for s in tau_inputs)
    assert any("log(2*pi) + gamma_E" in s for s in tau_inputs)


def test_28_lean_module_compiles_with_zero_sorry():
    """Verify formal/RiemannScope/ModularThetaConductorCurvature.lean exists, has 0 sorry/admit, and declares all 17 theorems and 2 defs."""
    assert LEAN_MODULE_PATH.exists()
    ver = verify_modular_theta_conductor_lean_map_against_file(LEAN_MODULE_PATH)
    assert ver["matches_exact"] is True
    assert ver["contains_sorry"] is False
    assert ver["contains_admit"] is False
    assert len(ver["actual_theorems"]) == 17
    assert len(ver["actual_defs"]) == 2


def test_29_artifact_json_schema_complete():
    """Verify data/tc_modular_theta_conductor_curvature.json exists and contains all required keys from Section 27."""
    assert DATA_JSON_PATH.exists()
    payload = json.loads(DATA_JSON_PATH.read_text(encoding="utf-8"))
    for key in REQUIRED_JSON_KEYS:
        assert key in payload, f"Missing required JSON key: {key}"


def test_30_obl_ct_001a_status_matches_proof_status():
    """Verify OBL-CT-001A remains OPEN and principal classification is ONE_PRECISE_THETA_CONDUCTOR_SUBGATE_OPEN."""
    report = audit_modular_theta_conductor_curvature()
    assert report["obl_ct_001a_status"] == "OPEN"
    assert report["obl_ct_001a_completed"] is False
    assert report["rh_claimed"] is False
    assert report["candidate_failure_refutes_tc"] is False
    assert (
        report["principal_classification"]
        == "ONE_PRECISE_THETA_CONDUCTOR_SUBGATE_OPEN"
    )
    assert report["exact_remaining_subgate"]["subgate_id"] == "SUBGATE-TC-036A"
    assert report["exact_remaining_subgate"]["status"] == "OPEN"


def test_31_unshifted_regularizer_defect_diagnosed():
    """Verify TASK-TC-036R diagnoses the unshifted regularizer D(D - 1/2) defect on tilde{g}_t(u) = t^{1/4} exp(-pi t u^2)."""
    res = evaluate_unshifted_vs_corrected_pole_regularizer(t=1.0)
    assert res["defect_status"] == UNSHIFTED_REGULARIZER_DOES_NOT_ANNIHILATE_POLES
    defect = res["defective_unshifted_operator"]
    assert defect["annihilates_poles"] is False
    assert math.isclose(defect["value_at_s_eq_0"], -1.0 / 16.0, abs_tol=1e-15)
    assert math.isclose(defect["value_at_s_eq_1"], 3.0 / 16.0, abs_tol=1e-15)
    assert math.isclose(defect["origin_value_at_u_eq_0"], -1.0 / 16.0, abs_tol=1e-15)
    assert math.isclose(defect["half_line_integral_value"], 3.0 / 32.0, abs_tol=1e-15)


def test_32_corrected_pole_regularizer_mellin_and_spatial_identities():
    """Verify TASK-TC-036R repaired regularizer P_reg(D) = D^2 - 1/16 has Mellin multiplier s(s-1)/4 = (z^2-1/4)/4 and vanishes at u=0 and in half-line integral."""
    res = evaluate_unshifted_vs_corrected_pole_regularizer(t=1.0)
    assert res["repair_status"] == CORRECTED_POLE_REGULARIZER_D_SQUARED_MINUS_ONE_SIXTEENTH
    assert res["completed_repair_status"] == COMPLETED_THETA_CONDUCTOR_REGULARIZATION_REPAIRED
    assert res["max_multiplier_identity_abs_err"] < 1e-15

    rep = res["repaired_pole_regularizer"]
    assert rep["annihilates_poles"] is True
    assert rep["annihilates_t_pos_quarter"] is True
    assert rep["annihilates_t_neg_quarter"] is True
    assert rep["value_at_s_eq_0"] == 0.0
    assert rep["value_at_s_eq_1"] == 0.0
    assert rep["origin_value_Phi_t_0"] == 0.0
    assert rep["origin_first_derivative_Phi_t_prime_0"] == 0.0
    assert rep["half_line_integral_int_0_infty_Phi_t_du"] == 0.0


def test_33_completed_functional_uses_corrected_regularizer_D2_minus_1_16():
    """Verify completed theta-conductor functional uses P_reg(D) = D^2 - 1/16 and preserves double-zero and RH-equivalence classifications."""
    comp = audit_completed_theta_conductor_functional()
    assert "(D^2 - 1/16)" in comp["zero_independent_definition"]
    assert "D^2 - 1/16" in comp["background_terms_included"]["operator_domain_condition"]
    assert (
        comp["complete_spectral_representation"]["quadratic_transfer_classification"]
        == "UNRESTRICTED_DOUBLE_ZERO_SUM"
    )
    assert (
        comp["natural_zero_pairing_audit"]["pairing_classification"]
        == "THETA_CONDUCTOR_FUNCTIONAL_REMAINS_DOUBLE_SPECTRAL"
    )
    assert (
        comp["weil_equivalence_audit"]["classification"]
        == "THETA_CONDUCTOR_POSITIVITY_IS_RH_EQUIVALENT"
    )


def test_34_section_11_two_parameter_modular_fourier_subspace_documented():
    """Verify Section 11 operator selector documents the 2-parameter invariant subspace b_0 I + b_2 (E + I)^2 before ker(E + I) normalization."""
    sel = solve_operator_selector_axioms()
    mod_part = sel["modular_and_fourier_constraint_on_scale_part"]
    assert "b_0 I + b_2 (E + I)^2" in mod_part["two_parameter_invariant_subspace"]
    assert "c_2 + b_0" in mod_part["coefficient_relations"]["c_0"]
    sol = sel["joint_linear_system_solution_for_scale_part"]
    assert sol["c_2"] == 0.0
    assert sol["c_1"] == 0.0
    assert sol["b_0"] == 0.0

