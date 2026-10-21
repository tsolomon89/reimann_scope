"""
Unit and adversarial control tests for EPIC-TC-041 / TASK-TC-041:
Establish the TC Arithmetic-Spectral Quartet Connection and Resolve the Remainder Inequality.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path

import mpmath
import pytest

import tc
import transcendental
from tc.quartet_remainder_connection import (
    COMPACT_WINDOW_RATIONAL_SEPARATION_PROVED,
    CONSTRUCTION_GATE_STATUS,
    CRITICAL_LINE_MULTIPLIER_SIGN_INVERSION_IDENTIFIED,
    DEFAULT_ARTIFACT_PATH,
    EPIC_TC_041_ID,
    NARROW_SMOOTHING_SPECTRAL_BANDWIDTH_COST_QUANTIFIED,
    ORDERED_AND_SYMMETRIZED_DOUBLE_SUM_EQUIVALENCE_PROVED,
    REDUCTIO_SUBORDINATION_INTERPRETATION_CORRECTED,
    REMAINDER_CONSISTENCY_IDENTITY_NOT_INDEPENDENT_BOUND,
    RESEARCH_GATE_STATUS,
    RH_GATE_STATUS,
    SINGLE_ORDINATE_FILTER_DOES_NOT_ANNIHILATE_INFINITE_SPECTRUM,
    SIXTEEN_PAIR_QUARTET_POSITIVITY_PROVED_UNDER_H,
    SIX_POINT_CONVOLUTION_WINDOW_ADMISSIBLE_AND_POSITIVE,
    SMALL_DELTA_QUADRATIC_SCALING_BARRIER_QUANTIFIED,
    SMOOTHED_EXPLICIT_FORMULA_SIGN_AND_SUBTRACTION_VERIFIED,
    SUBGATE_TC_041B_ID,
    SUBGATE_TC_041B_STATUS,
    TASK_TC_041_ID,
    analyze_remainder_components_and_mechanisms,
    audit_physical_to_logarithmic_jacobian,
    audit_reductio_subordination_interpretation,
    audit_window_admissibility_and_zeros,
    build_quartet_window_spec,
    c_epsilon_laplace,
    certify_compact_window_rational_separation,
    enumerate_prime_power_stations,
    evaluate_archimedean_pole_term_A_epsilon,
    evaluate_bilinear_B_h_spatial,
    evaluate_composite_window_W_transform,
    evaluate_composite_window_w,
    evaluate_grade_second_difference_multiplier_T,
    evaluate_prime_power_sum_P_epsilon,
    evaluate_second_difference_D_spatial,
    evaluate_target_quartet_profile_S0,
    evaluate_target_quartet_sixteen_pairs,
     verify_elementary_bump_laplace_bound,
    verify_explicit_formula_pointwise,
)


def test_facade_exports_and_identifiers():
    """Verify public symbols are exported in both tc and transcendental facades."""
    assert tc.EPIC_TC_041_ID == "EPIC-TC-041"
    assert tc.TASK_TC_041_ID == "TASK-TC-041"
    assert transcendental.EPIC_TC_041_ID == "EPIC-TC-041"
    assert transcendental.SUBGATE_TC_041B_ID == "SUBGATE-TC-041B"
    assert hasattr(tc, "evaluate_target_quartet_sixteen_pairs")
    assert hasattr(transcendental, "evaluate_target_quartet_sixteen_pairs")


def test_part_a_rational_grade_enforcement_and_station_enumeration():
    """Verify exact rational grade enforcement and interior/boundary station enumeration."""
    with pytest.raises(TypeError):
        certify_compact_window_rational_separation(x_w=0.45, d=0.05)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        certify_compact_window_rational_separation(x_w=0.45, d=Fraction(-1, 10))

    # Choose x_shift = log(5) - 0.05 so +/- log(5) are boundary stations in [-x_shift - eps_0, x_shift + eps_0]
    x_shift = math.log(5.0) - 0.05
    stations = enumerate_prime_power_stations(x_shift=x_shift, eps_0=0.10, dps=40)
    boundary = [s for s in stations if s.is_boundary_station]
    interior = [s for s in stations if not s.is_boundary_station]
    assert len(boundary) == 2
    assert {s.n for s in boundary} == {5}
    assert {s.sign for s in boundary} == {-1, +1}
    assert {s.n for s in interior} == {2, 3, 4}


def test_part_a_compact_window_separation_and_controls():
    """Verify certified station separation for tau=2*pi and adversarial controls."""
    # 1. Canonical tau = 2*pi separation
    cert_tau = certify_compact_window_rational_separation(
        x_w=0.45,
        d=Fraction(1, 20),
        eps_0=0.15,
        profile_type="cosine_power_6",
        dps=45,
    )
    assert cert_tau.min_separation_distance > 0.025
    assert cert_tau.certified_arb_lower_bound > 0.025
    assert cert_tau.boundary_station_count >= 2
    assert cert_tau.q_plus1 == 0.0
    assert cert_tau.q_0 == 0.0
    assert cert_tau.q_minus1 == 0.0
    assert cert_tau.second_difference_D_P == 0.0
    assert cert_tau.vanishes_identically_certified is True
    assert cert_tau.classification == COMPACT_WINDOW_RATIONAL_SEPARATION_PROVED

    # 2. Overlap violation control: 2*eps > Delta_min breaks vanishing
    cert_overlap = certify_compact_window_rational_separation(
        x_w=0.45,
        d=Fraction(1, 20),
        eps_0=0.25,
        test_epsilon=0.22,
        profile_type="cosine_power_6",
        dps=40,
    )
    assert cert_overlap.test_epsilon > cert_overlap.max_admissible_epsilon
    assert cert_overlap.q_plus1 > 1.0
    assert cert_overlap.second_difference_D_P > 1.0
    assert cert_overlap.vanishes_identically_certified is False

    # 3. Colliding rational-base control: B = 2, d = 1 => B^d = 2 = 4/2 in Q
    cert_rat = certify_compact_window_rational_separation(
        x_w=0.80,
        d=Fraction(1, 1),
        eps_0=0.20,
        test_epsilon=0.05,
        base_value=2.0,
        base_name="rational_base_2",
        profile_type="cosine_power_6",
        dps=40,
    )
    assert cert_rat.min_separation_distance < 1e-35
    assert cert_rat.max_admissible_epsilon < 1e-35
    assert cert_rat.q_plus1 > 0.5
    assert cert_rat.second_difference_D_P > 1.0
    assert cert_rat.vanishes_identically_certified is False

    # 4. Generic transcendental-base control: B = e preserves Part (A) separation
    cert_e = certify_compact_window_rational_separation(
        x_w=0.45,
        d=Fraction(1, 20),
        eps_0=0.15,
        base_value=math.e,
        base_name="transcendental_base_e",
        profile_type="cosine_power_6",
        dps=40,
    )
    assert cert_e.certified_arb_lower_bound > 0.04
    assert cert_e.vanishes_identically_certified is True


def test_part_b_smoothed_explicit_formula_verification():
    """Verify P_eps = A_eps - S_eps signs, constants, u=0 subtraction, and tail bound."""
    res = verify_explicit_formula_pointwise(
        x_points=(0.0, 0.35, math.log(2.0), 1.0),
        epsilon=0.25,
        max_zeros=100,
        profile_type="cosine_power_6",
        dps=40,
    )
    assert res["log_2tau_equals_log_4pi"] is True
    assert res["u0_removable_singularity_verified"] is True
    assert res["classification"] == SMOOTHED_EXPLICIT_FORMULA_SIGN_AND_SUBTRACTION_VERIFIED
    for pt in res["pointwise_evaluations"]:
        assert pt["abs_discrepancy"] < 1e-7
        assert pt["abs_discrepancy"] < pt["analytic_tail_bound"]


def test_part_d_admissible_window_and_transform_zeros():
    """Verify 6-point convolution window admissibility and quarter/half-period transform zeros."""
    win = audit_window_admissibility_and_zeros(
        delta=0.12,
        gamma=14.134725141734693,
        x_0=0.25,
        profile_type="cosine_power_6",
        dps=50,
    )
    assert win["arb_certified_quarter_and_half_period_zeros"] is True
    assert win["max_transform_zero_residual"] < 1e-45
    assert win["W_2delta_closed"] > 1.0
    assert win["spatial_vs_closed_diff"] < 1e-14
    assert win["is_nonnegative"] is True
    assert win["is_even"] is True
    assert win["vanishes_outside_support"] is True
    assert win["classification"] == SIX_POINT_CONVOLUTION_WINDOW_ADMISSIBLE_AND_POSITIVE

    # Also verify with true C_c^infty bump exp(-1/(1-t^2))
    win_cc = audit_window_admissibility_and_zeros(
        delta=0.12,
        gamma=14.134725141734693,
        x_0=0.25,
        profile_type="cc_inf_bump",
        dps=40,
    )
    assert win_cc["arb_certified_quarter_and_half_period_zeros"] is True
    assert win_cc["max_transform_zero_residual"] < 1e-35
    assert win_cc["is_nonnegative"] is True
    assert win_cc["vanishes_outside_support"] is True


def test_part_e_sixteen_pair_quartet_three_routes():
    """Verify exact 3-route agreement and category vanishing for the 16-pair quartet."""
    q = evaluate_target_quartet_sixteen_pairs(
        delta=0.12,
        gamma=14.134725141734693,
        multiplicity_m=1,
        d=Fraction(1, 20),
        epsilon=0.02,
        x_0=0.25,
        profile_type="cosine_power_6",
        dps=50,
    )
    assert len(q["pair_records"]) == 16
    assert q["is_d_below_threshold"] is True
    assert q["is_strictly_positive_certified"] is True
    assert q["arb_certified_lower_bound"] > 0.20
    assert q["exp_vs_cosh_diff"] < 1e-45
    assert q["ordered_vs_closed_diff"] < 1e-45
    assert q["spatial_vs_closed_diff"] < 1e-14
    assert abs(q["category_sums"]["opposite_pairs_T0"]) == 0.0
    assert abs(q["category_sums"]["self_pairs_W_2d_2ig"]) < 1e-45
    assert abs(q["category_sums"]["vertical_pairs_W_2ig"]) < 1e-45
    assert abs(q["category_sums"]["conjugate_pairs_2d"] - q["C_eps_closed_formula_E"]) < 1e-45
    assert q["classification"] == SIXTEEN_PAIR_QUARTET_POSITIVITY_PROVED_UNDER_H


def test_part_e_adversarial_parameter_controls():
    """Verify adversarial controls: delta->0+, small delta, large gamma, m>1, d near threshold, c_eps->0."""
    gamma_1 = 14.134725141734693

    # 1. Critical-line limit delta = 0 => C_eps = 0
    q_zero_delta = evaluate_target_quartet_sixteen_pairs(
        delta=0.0,
        gamma=gamma_1,
        multiplicity_m=1,
        d=Fraction(1, 20),
        epsilon=0.02,
        x_0=0.25,
        include_spatial_quadrature=False,
        dps=45,
    )
    assert abs(q_zero_delta["C_eps_closed_formula_E"]) < 1e-45
    assert abs(q_zero_delta["C_eps_ordered_16_exp"]) < 1e-45

    # 2. Small positive delta => C_eps > 0 and scales as O(delta^2)
    q_small_1 = evaluate_target_quartet_sixteen_pairs(
        delta=1e-3,
        gamma=gamma_1,
        multiplicity_m=1,
        d=Fraction(1, 20),
        epsilon=0.02,
        x_0=0.25,
        include_spatial_quadrature=False,
        dps=45,
    )
    q_small_2 = evaluate_target_quartet_sixteen_pairs(
        delta=2e-3,
        gamma=gamma_1,
        multiplicity_m=1,
        d=Fraction(1, 20),
        epsilon=0.02,
        x_0=0.25,
        include_spatial_quadrature=False,
        dps=45,
    )
    assert q_small_1["is_strictly_positive_certified"] is True
    ratio_quad = q_small_2["C_eps_closed_formula_E"] / q_small_1["C_eps_closed_formula_E"]
    assert abs(ratio_quad - 4.0) < 1e-4

    # 3. Multiplicity m > 1 => exact m^2 scaling
    q_m1 = evaluate_target_quartet_sixteen_pairs(
        delta=0.12,
        gamma=gamma_1,
        multiplicity_m=1,
        d=Fraction(1, 20),
        epsilon=0.02,
        x_0=0.25,
        include_spatial_quadrature=False,
        dps=45,
    )
    q_m3 = evaluate_target_quartet_sixteen_pairs(
        delta=0.12,
        gamma=gamma_1,
        multiplicity_m=3,
        d=Fraction(1, 20),
        epsilon=0.02,
        x_0=0.25,
        include_spatial_quadrature=False,
        dps=45,
    )
    assert abs(q_m3["C_eps_closed_formula_E"] / q_m1["C_eps_closed_formula_E"] - 9.0) < 1e-14

    # 4. Large gamma (gamma = 100.0) with rational d < tau/(4*gamma*L) ~ 0.00855
    q_large_gamma = evaluate_target_quartet_sixteen_pairs(
        delta=0.10,
        gamma=100.0,
        multiplicity_m=1,
        d=Fraction(1, 200),
        epsilon=0.005,
        x_0=0.10,
        include_spatial_quadrature=False,
        dps=45,
    )
    assert q_large_gamma["is_d_below_threshold"] is True
    assert q_large_gamma["is_strictly_positive_certified"] is True

    # 5. Rational d just below vs just above threshold tau/(4*gamma*L) ~ 0.06046667
    q_below = evaluate_target_quartet_sixteen_pairs(
        delta=0.12,
        gamma=gamma_1,
        multiplicity_m=1,
        d=Fraction(6, 100),  # 0.06 < 0.06046667
        epsilon=0.02,
        x_0=0.25,
        include_spatial_quadrature=False,
        dps=45,
    )
    q_above = evaluate_target_quartet_sixteen_pairs(
        delta=0.12,
        gamma=gamma_1,
        multiplicity_m=1,
        d=Fraction(7, 100),  # 0.07 > 0.06046667
        epsilon=0.02,
        x_0=0.25,
        include_spatial_quadrature=False,
        dps=45,
    )
    assert q_below["is_d_below_threshold"] is True
    assert q_below["C_eps_closed_formula_E"] > 0.0
    assert q_above["is_d_below_threshold"] is False
    assert q_above["C_eps_closed_formula_E"] < 0.0

    # 6. Elementary bump Laplace bound and regime where c_eps approaches zero
    bound_ok = verify_elementary_bump_laplace_bound(
        z=complex(0.12, gamma_1),
        epsilon=0.02,
        profile_type="cosine_power_6",
        dps=45,
    )
    assert bound_ok["satisfies_cosh_bound"] is True
    assert bound_ok["satisfies_exp_bound"] is True
    assert bound_ok["is_guaranteed_nonzero_by_elementary_bound"] is True

    # For cosine_power_6 on [-1,1], the first Fourier zero on the imaginary axis is at eps*gamma = 4*pi
    with mpmath.workdps(45):
        gamma_mp = mpmath.mpf("14.134725141734693")
        eps_zero_mp = (4 * mpmath.pi) / gamma_mp
        c_at_zero = c_epsilon_laplace(1j * gamma_mp, eps_zero_mp, "cosine_power_6", dps=45)
        assert abs(c_at_zero) < 1e-40

    q_near_c_zero = evaluate_target_quartet_sixteen_pairs(
        delta=0.01,
        gamma=gamma_1,
        multiplicity_m=1,
        d=Fraction(1, 20),
        epsilon=float((4.0 * math.pi) / gamma_1),
        x_0=0.25,
        include_spatial_quadrature=False,
        dps=45,
    )
    assert q_near_c_zero["abs_c_eps_squared"] < 1e-6


def test_contract_item_7_physical_to_logarithmic_jacobian():
    """Verify exact Jacobian identity between physical and logarithmic overlap integrals."""
    jac = audit_physical_to_logarithmic_jacobian(
        h_midpoint=1,
        d=Fraction(1, 10),
        dps=45,
    )
    assert jac["haar_measure_dy_over_y_equals_dx_verified"] is True
    assert jac["abs_jacobian_error"] < 1e-40
    assert abs(jac["actual_ratio"] - 2.0 * math.pi) < 1e-14


def test_wp4_remainder_analysis_and_wp6_reductio_repair():
    """Verify independent remainder assembly, 4 mechanisms, and WP6 reductio repair."""
    with open(DEFAULT_ARTIFACT_PATH, "r", encoding="utf-8") as f:
        artifact = json.load(f)

    assert artifact["epic_id"] == EPIC_TC_041_ID
    assert artifact["task_id"] == TASK_TC_041_ID
    assert artifact["gates"]["construction_gate"] == CONSTRUCTION_GATE_STATUS
    assert artifact["gates"]["research_gate"] == RESEARCH_GATE_STATUS
    assert artifact["gates"]["rh_gate"] == RH_GATE_STATUS

    rem = artifact["part_F_and_WP4_remainder_analysis"]
    terms = rem["independently_assembled_terms"]
    assert terms["uses_consistency_identity_R_eq_minus_C"] is False
    expected_sum = (
        terms["R_AA_full_archimedean_pole"]
        + terms["R_AS0_minus_2D_A_S0"]
        + terms["R_ASrest_minus_2D_A_Srest"]
        + terms["R_0_rest_plus_2D_S0_Srest"]
        + terms["R_rest_rest_D_Srest_Srest"]
    )
    assert abs(terms["R_eps_assembled_sum"] - expected_sum) < 1e-10

    # Mechanism 1: T(2*i*gamma_n) <= 0 on critical-line diagonal sums
    for row in rem["mechanism_1_and_2_critical_line_table"]:
        assert row["T_2i_gamma_n"] <= 0.0
    # Target ordinate gamma_1 is annihilated by W(2*i*gamma_1) = 0, but gamma_2 is not
    assert abs(rem["mechanism_1_and_2_critical_line_table"][0]["W_2i_gamma_n"]) < 1e-18
    assert abs(rem["mechanism_1_and_2_critical_line_table"][1]["W_2i_gamma_n"]) > 1e-4

    # Mechanism 3: C_eps / delta^2 converges to a positive constant while cross term stays O(1)
    sweep = rem["mechanism_3_small_delta_sweep"]
    assert sweep[-1]["abs_ratio_cross_to_C_eps"] > 1e5
    assert 13.0 < sweep[-1]["C_eps_over_delta_squared"] < 15.0

    # Subgate and WP6 repair
    assert rem["decisive_open_subgate"]["subgate_id"] == SUBGATE_TC_041B_ID
    assert rem["decisive_open_subgate"]["status"] == SUBGATE_TC_041B_STATUS
    wp6 = audit_reductio_subordination_interpretation()
    assert wp6["algebraic_incompatibility_theorem_valid"] is True
    assert wp6["universal_prohibition_inference_retracted"] is True
    assert wp6["classification"] == REDUCTIO_SUBORDINATION_INTERPRETATION_CORRECTED


def test_wp5_lean_formalization_declarations_and_no_sorry():
    """Verify formal/RiemannScope/QuartetRemainderConnection.lean has 0 sorry and all synchronized declarations."""
    lean_path = (
        Path(__file__).resolve().parent.parent
        / "formal"
        / "RiemannScope"
        / "QuartetRemainderConnection.lean"
    )
    assert lean_path.exists()
    content = lean_path.read_text(encoding="utf-8")
    code_lines = [
        line.split("--")[0]
        for line in content.splitlines()
        if not line.strip().startswith("--")
    ]
    joined_code = "\n".join(code_lines)
    assert "sorry" not in joined_code
    assert "admit" not in joined_code
    assert "axiom " not in joined_code

    expected_theorems = [
        "quartet_radial_factor_eq_sq",
        "quartet_radial_sq_pos",
        "quartet_radial_factor_pos",
        "ordered_pair_symmetrized_cosh_equivalence",
        "sixteen_pair_quartet_block_reduction",
        "sixteen_pair_target_quartet_pos",
        "sixteen_pair_multiplicity_scaling",
        "sixteen_pair_critical_line_vanishing",
        "elementary_bump_nonvanishing_from_bound",
        "critical_line_multiplier_nonpos",
        "exact_remainder_consistency_identity",
        "conditional_remainder_dominance_contradiction",
        "conditional_reductio_negates_offcritical_hypothesis",
        "second_diff_multiplier_imag_eq",
        "quartet_target_coeff_pos",
        "arithmetic_spectral_second_diff_expansion",
        "quartet_remainder_decomposition_identity",
        "arithmetic_second_diff_vanishes",
        "quartet_remainder_identity_from_vanishing",
        "quartet_subordination_contradiction",
        "unconditional_subordination_contradiction",
        "unconditional_subordination_contradiction_repaired",
        "reductio_from_quartet_and_remainder_lower_bound",
        "prob_conv_nonneg",
        "prob_conv_normalization",
        "quartet_opposite_pair_sum_zero",
        "quartet_vertical_pair_sum",
        "quartet_horizontal_pair_sum_pos",
        "quartet_second_diff_pos",
        "quartet_block_pos_under_H",
        "ibp_laplace_error_bound_nonneg",
        "bump_laplace_error_bound_nonneg",
        "cosh_filter_factor_pos",
        "nu_b_kappa_pos",
        "window_transform_vertical_zero",
        "window_transform_self_zero",
        "quadratic_truncation_error_bound",
        "regrouped_remainder_algebraic_identity",
    ]
    for thm in expected_theorems:
        assert f"theorem {thm}" in content


def test_tc_041r_wp1_separation_violation_reproduction_and_enforcement():
    """Verify WP1.1: reproduce eps=0.08 overlap violation (D(P,P) ≈ 2.200149) and certify eps=0.01."""
    repro = tc.reproduce_wp1_benchmark_separation_violation(dps=40)
    assert abs(repro["delta_min_certified_arb_lower"] - 0.02588918233591618) < 1e-12
    assert abs(repro["max_admissible_epsilon"] - 0.01294459116795809) < 1e-12

    inv = repro["invalid_benchmark_eps_008"]
    assert inv["violates_two_eps_lt_delta_min"] is True
    assert inv["vanishes_identically_certified"] is False
    assert inv["classification"] == "OVERLAP_OR_COLLISION_DETECTED"
    assert abs(inv["constructed_window_pairings"]["Q_minus_1"] - 1.1000747) < 1e-4
    assert inv["constructed_window_pairings"]["Q_0"] == 0.0
    assert abs(inv["constructed_window_pairings"]["Q_plus_1"] - 1.1000747) < 1e-4
    assert abs(inv["constructed_window_pairings"]["D_P_eps_P_eps"] - 2.200149) < 1e-4

    val = repro["repaired_admissible_benchmark_eps_001"]
    assert val["satisfies_two_eps_lt_delta_min"] is True
    assert val["vanishes_identically_certified"] is True
    assert val["constructed_window_pairings"]["D_P_eps_P_eps"] == 0.0


def test_tc_041r_wp1_spectral_tail_counterexample_and_unconditional_rvm_bound():
    """Verify WP1.2: u = 19.5*pi counterexample ratio ≈ 1.03786 > 1, eps^N in denominator, and RvM Stieltjes tail."""
    ce = tc.reproduce_cosine_power_6_asymptotic_counterexample(dps=50)
    assert ce["u_over_pi"] == 19.5
    assert ce["exceeds_naive_asymptotic_certified"] is True
    assert abs(ce["exact_to_naive_ratio_arb_lower"] - 1.0378607972) < 1e-8

    ibp = tc.compute_proved_bump_laplace_upper_bound(
        z=complex(0.12, 61.261056745),
        epsilon=1.0,
        profile_type="cosine_power_6",
        ibp_order=6,
        dps=50,
    )
    assert ibp["profile_bound_holds"] is True
    assert ibp["general_ibp_bound_holds"] is True
    assert ibp["eps_in_denominator_verified"] is True

    rvm = tc.compute_unconditional_rvm_spectral_tail_bound(
        t_cutoff=236.5242296658,
        epsilon=0.25,
        x_shift_max=1.0,
        delta_max=0.0,
        dps=50,
    )
    assert rvm["counts_both_ordinate_signs"] is True
    assert rvm["counts_zero_multiplicities_via_dN"] is True
    assert rvm["includes_shifted_domain_exp_delta_x"] is True
    assert 0.0 < rvm["total_tail_bound_arb_upper"] < 1e-5


def test_tc_041r_wp1_genuine_arb_acb_enclosures_and_symbolic_zeros():
    """Verify WP1.3: genuine Arb/Acb enclosures from enclosed inputs and symbolic SymPy zero proofs."""
    sym_zeros = tc.prove_symbolic_window_and_multiplier_zeros()
    assert sym_zeros["T_0_equals_zero_proved"] is True
    assert sym_zeros["vertical_factor_plus_2ig_zero_proved"] is True
    assert sym_zeros["vertical_factor_minus_2ig_zero_proved"] is True
    assert sym_zeros["all_four_self_pair_factors_zero_proved"] is True
    assert sym_zeros["radial_square_identity_proved"] is True

    q = evaluate_target_quartet_sixteen_pairs(
        delta=0.12,
        gamma=14.134725141734693,
        multiplicity_m=1,
        d=Fraction(1, 20),
        epsilon=0.01,
        x_0=0.25,
        include_spatial_quadrature=False,
        dps=50,
    )
    assert q["arb_enclosure_from_enclosed_inputs"] is True
    assert q["arb_certified_lower_bound"] > 0.0
    assert q["arb_certified_lower_bound"] <= q["C_eps_closed_formula_E"] <= q["arb_certified_upper_bound"]


def test_tc_041r_wp2_actual_zeta_consistency_and_quadratic_truncation_bounds():
    """Verify WP2: actual zeta consistency check in separated regime and quadratic truncation error propagation."""
    quad_err = tc.compute_quadratic_truncation_error_bound(
        w_l1_norm=1.0,
        sup_s_truncated=10.0,
        sup_a_eps=5.0,
        tail_eta=0.01,
    )
    assert abs(quad_err["D_SS_truncation_error_bound"] - 4.0 * (2.0 * 10.0 * 0.01 + 0.0001)) < 1e-12
    assert abs(quad_err["minus_2_D_AS_truncation_error_bound"] - 8.0 * 5.0 * 0.01) < 1e-12

    with open(DEFAULT_ARTIFACT_PATH, "r", encoding="utf-8") as f:
        artifact = json.load(f)

    wp2 = artifact["wp2_actual_zeta_consistency_check"]
    assert wp2["uses_synthetic_zero_replacement"] is False
    sim = wp2["certified_simultaneous_regime"]
    assert sim["separation_certified"] is True
    assert sim["D_P_eps_P_eps"] == 0.0
    assert sim["u0_eps_T"] > 3.0 * math.pi
    assert sim["residual_within_certified_truncation_bound"] is True


def test_tc_041r_wp3_wp4_wp5_coordinate_bridge_subgate_and_provenance():
    """Verify WP3 Jacobian proofs, WP4 regrouped identity and J-filter sweep, and WP5 bibliography/gates."""
    with open(DEFAULT_ARTIFACT_PATH, "r", encoding="utf-8") as f:
        artifact = json.load(f)

    jac = artifact["contract_item_7_jacobian_audit"]
    assert jac["one_variable_jacobian_e_pow_x_minus_xp_over_2_proved"] is True
    assert jac["omitted_dy_typo_identified_and_corrected"] is True
    assert jac["paired_half_density_tau_pow_h_proved"] is True
    assert jac["additive_logarithmic_vs_physical_smoothing_distinguished"] is True

    wp4 = artifact["wp4_subgate_tc_041b_continuation"]
    reg = wp4["regrouped_identity_verification"]
    assert reg["symbolic_polynomial_difference_zero"] is True
    assert reg["cancels_linear_cross_term_2_D_P_S0_identically"] is True
    j_sweep = wp4["multi_ordinate_filter_sweep"]
    assert len(j_sweep) == 5
    # Window half-width X_w(J) and station count grow with J while max_admissible_epsilon shrinks
    assert j_sweep[-1]["window_half_width_X_w"] > j_sweep[0]["window_half_width_X_w"]
    assert j_sweep[-1]["enlarged_station_count"] >= j_sweep[0]["enlarged_station_count"]
    assert j_sweep[-1]["max_admissible_epsilon"] < j_sweep[0]["max_admissible_epsilon"]

    wp5 = artifact["wp5_provenance_and_novelty_calibration"]
    cits = {c["arxiv_id"]: c for c in wp5["verified_arxiv_citations"]}
    assert "Burnol" in cits["math/0101068"]["authors"]
    assert "Connes" in cits["2511.22755"]["authors"]
    assert "Shi" in cits["2609.04908"]["authors"]
    assert "Suzuki" in cits["2606.09096"]["authors"]
    assert wp5["three_gate_status"]["independent_review_status"] == "AWAITING_INDEPENDENT_REVIEW"


