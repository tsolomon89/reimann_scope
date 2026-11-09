"""Tests for TASK-TC-054 and TASK-TC-054R: Liouville Square-Dilation Transfer, Unconstrained
Common-Factor Expansion, Non-Schwartz Transition Poisson Summation, Certified Hypergeometric
Fourier Tail Bounds, Exact Rational Cutoffs, Unequal-Block Bounds, and Repaired Global
Stieltjes Energy Proof.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
import json

from flint import arb, ctx as flint_ctx
import pytest

from certification import REQUIRED_FORMAL_SOURCES
from scripts.build_formal import FORMAL_SOURCE_FILES
from tc.canonical_theta_correlation_bound import REPO_ROOT, verify_all_serialized_arb_in_tree
from tc.liouville_square_dilation import (
    LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH,
    PRIOR_MERGED_MAIN_TC_053R,
    TASK_TC_054_ID,
    TASK_TC_054R_ID,
    TASK_TC_054R2_ID,
    TASK_TC_055_ID,
    TASK_TC_055R_ID,
    TC_053R2_IMPLEMENTATION_COMMIT,
    TC_053R2_REVIEWED_TIP,
    TC_054_IMPLEMENTATION_COMMIT,
    TC_054_REVIEWED_TIP,
    TC_054R_IMPLEMENTATION_COMMIT,
    TC_054R_REVIEWED_TIP,
    TC_054R2_IMPLEMENTATION_COMMIT,
    TC_054R2_MERGED_MAIN_BASELINE,
    TC_054R2_REVIEWED_TIP,
    TC_055_IMPLEMENTATION_COMMIT,
    TC_055_INITIAL_CLOSEOUT_COMMIT,
    TC_055_REVIEWED_TIP,
    compute_hat_f_tail_ratios_arb,
    evaluate_1d_dyadic_sum_U_lambda_arb,
    evaluate_E_a2_certified_arb,
    evaluate_Q_1_unweighted_certified_arb,
    evaluate_Q_a2_certified_arb,
    evaluate_Q_aS_certified_arb,
    evaluate_Q_arith_certified_arb,
    evaluate_Q_lambda_finite_T_certified_arb,
    evaluate_Q_lambda_from_prime_excluded_inverse_certified_arb,
    evaluate_Q_lambda_P_finite_L_certified_arb,
    evaluate_Q_lambda_prime_excluded_direct_certified_arb,
    evaluate_Q_lambda_prime_excluded_operator_certified_arb,
    evaluate_d_sum_certified_arb,
    evaluate_decoupled_rectangular_block_B_AB_certified_arb,
    evaluate_energy_kernel_K_Y_certified_arb,
    evaluate_hat_f_hypergeometric_certified_arb,
    evaluate_hat_f_quadrature_certified_arb,
    evaluate_rectangular_block_B_AB_certified_arb,
    evaluate_square_dilation_transfer_certified_arb,
    execute_task_tc054_liouville_square_dilation_audit,
    execute_task_tc055_simultaneous_tau_compatibility_audit,
    finite_prime_parity_aS_int,
    generate_P_smooth_up_to,
    liouville_lambda_int,
    omega_with_multiplicity_int,
    prime_exclusion_sieve_sum_int,
    reproduce_tc054_cutoff_tolerance_counterexample_arb,
    reproduce_tc054_hat_f_k1_counterexample_arb,
    square_divisor_inverse_liouville_sum_int,
    square_divisor_moebius_sum_int,
    two_adic_parity_a2_int,
    verify_abel_scaling_and_global_stieltjes_energy_proof,
    verify_euler_maclaurin_derivatives_and_constants_arb,
    verify_liouville_square_dilation_lean_module,
    verify_mellin_contour_and_reflection_identities_arb,
    verify_section_2_and_3_square_dilation_transfer,
    verify_section_4_unconstrained_common_factor_and_euler_maclaurin,
    verify_section_5_poisson_summation_at_transition,
    verify_section_6_transition_attacks_and_decoupling,
    verify_tc055_coupled_cutoff_and_norm_obstruction,
    verify_tc055_integrated_energy_kernel_and_near_diagonal_bound,
    verify_tc055_multiplicative_parity_controls,
    verify_tc055_opposite_parity_dilation_pairing_and_obstruction,
    verify_tc055_simultaneous_joint_identities_and_trivial_zero_cancellation,
    verify_tc055r_finite_truncation_and_signed_energy_attempt,
)
from tc.prime_euler_moebius_recovery import moebius_mu_int

EXPECTED_PUBLIC_THEOREM_NAMES = (
    "liouville_complete_multiplicativity_and_common_factor_cancellation_nat",
    "prime_power_square_divisor_moebius_liouville_inversion_nat",
    "actual_omega_factorization_and_liouville_common_factor_cancellation_nat",
    "actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat",
    "reversible_weighted_dilation_norm_and_grade_interval_equivalence",
    "euler_maclaurin_c2_and_subtransition_growing_range_exponent",
    "dyadic_parity_energy_and_off_critical_mode_nonvanishing",
    "abel_scaling_fourier_ratio_and_unequal_block_algebra",
    "actual_finite_prime_exclusion_sieve_identity_nat",
    "prime_parity_control_multiplicative_and_moebius_separation_nat",
    "near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing",
    "pairing_counterexample_replacement_and_finite_reconstruction_tc055r",
)


def test_square_divisor_moebius_liouville_convolutions_and_common_factor_sign() -> None:
    """Verify lambda(n) = sum_{d^2 | n} mu(n/d^2), mu(n) = sum_{d^2 | n} mu(d) lambda(n/d^2)
    up to n = 200, and lambda(d r) lambda(d s) = lambda(r) lambda(s) for 1 <= d, r, s <= 30.
    """
    assert omega_with_multiplicity_int(1) == 0
    assert liouville_lambda_int(1) == 1
    assert liouville_lambda_int(2) == -1
    assert liouville_lambda_int(4) == 1
    assert liouville_lambda_int(8) == -1
    assert liouville_lambda_int(12) == -1
    assert liouville_lambda_int(36) == 1

    for n in range(1, 201):
        assert square_divisor_moebius_sum_int(n) == liouville_lambda_int(n), f"Forward failed at n={n}"
        assert square_divisor_inverse_liouville_sum_int(n) == moebius_mu_int(n), f"Inverse failed at n={n}"

    for d in [1, 2, 4, 6, 8, 9, 12, 16, 18, 25, 27, 30]:
        for r in range(1, 31):
            for s in range(1, 31):
                assert (
                    liouville_lambda_int(d * r) * liouville_lambda_int(d * s)
                    == liouville_lambda_int(r) * liouville_lambda_int(s)
                )


def test_section_2_and_3_square_dilation_transfer_and_norm_multipliers() -> None:
    """Verify direct vs square-dilation transfer evaluations of Q_mu(X) and Q_lambda(X),
    weighted norm multipliers across eta > 0, 12/tau^2 residue, and Lindemann irrationality scope.
    """
    sec23 = verify_section_2_and_3_square_dilation_transfer(prec_bits=256)
    assert sec23["square_divisor_convolution_audit"]["all_forward_lambda_eq_sum_mu_n_over_d2"] is True
    assert sec23["square_divisor_convolution_audit"]["all_inverse_mu_eq_sum_mu_d_lambda_n_over_d2"] is True
    assert (
        sec23["complete_multiplicativity_common_factor_audit"][
            "all_triples_satisfy_lambda_dr_lambda_ds_eq_lambda_r_lambda_s"
        ]
        is True
    )
    assert sec23["all_transfer_enclosures_contain_zero_difference"] is True

    rows = sec23["square_dilation_transfer_rows"]
    assert len(rows) == 6
    for row in rows:
        assert row["Q_mu_zero_in_difference"] is True
        assert row["Q_lambda_zero_in_difference"] is True
        assert row["abs_Q_mu_le_zeta3_X_5_2"] is True
        assert row["abs_Q_lambda_le_zeta3_X_5_2"] is True

    wn = sec23["weighted_dilation_norm_equivalence"]
    assert "12/(tau^2 * eta)" in wn["eta_zero_singularity_and_operator_scope_note"]
    assert "triangle-inequality" in wn["eta_zero_singularity_and_operator_scope_note"]
    mult_rows = wn["multiplier_table"]
    assert len(mult_rows) == 5
    for mrow in mult_rows:
        assert "eta" in mrow
        assert mrow["forward_multiplier_positive_finite"] is True
        assert mrow["reverse_multiplier_positive_finite"] is True

    g_equiv = sec23["grade_interval_energy_and_mellin_bridge"]
    bridge_note = g_equiv["mellin_identities"]["bridge_to_subgate_tc_043a_explanation"]
    assert "irrational" in bridge_note
    assert "Lindemann" in bridge_note


def test_section_4_euler_maclaurin_constants_and_subtransition_error_bounds() -> None:
    """Verify symbolic and 256-bit Arb derivatives f', f'', f^{(3)}, f^{(4)}, inflection
    points v_+/-, c_0 = 3*sqrt(tau/2)/8, C_2, C_4, d-sum bounds, pairwise bounds, and
    coprime aggregate bounds.
    """
    sec4 = verify_section_4_unconstrained_common_factor_and_euler_maclaurin(prec_bits=256)
    em = sec4["euler_maclaurin_derivatives_and_constants"]
    assert em["sympy_derivative_identities_verified"] is True
    assert em["f_prime_v_minus_positive"] is True
    assert em["f_prime_v_plus_negative"] is True

    c2_low = float(em["C_2"]["lower_dec"])
    c2_high = float(em["C_2"]["upper_dec"])
    assert c2_low <= 1.851257667016958 <= c2_high

    c4_low = float(em["C_4"]["lower_dec"])
    c4_high = float(em["C_4"]["upper_dec"])
    assert c4_low <= 8.752371760035366 <= c4_high

    assert sec4["all_d_sum_em_bounds_hold"] is True
    assert sec4["all_pairwise_bounds_hold"] is True
    assert sec4["all_aggregate_bounds_hold"] is True


def test_section_5_hat_f_k1_counterexample_and_tail_ratio_certification() -> None:
    """Reproduce the K_terms=1, xi=4/tau (omega=4) failure of the unguarded 2x tail formula,
    test tail ratio thresholds (R <= 1/2, 1/2 < R < 1, R > 1), strict_K vs adaptive mode,
    interval inputs, large frequencies, symmetry, and quadrature cross-checks.
    """
    k1_reg = reproduce_tc054_hat_f_k1_counterexample_arb(prec_bits=256)
    assert k1_reg["R_even_exceeds_one"] is True
    assert k1_reg["old_upper_strictly_below_neg_Gamma_5_2"] is True
    assert k1_reg["strict_K1_raises_value_error"] is True
    assert k1_reg["repaired_k4_contains_adaptive"] is True
    assert float(k1_reg["old_upper_endpoint"]["upper_dec"]) < -2.69957
    assert float(k1_reg["trivial_lower_bound_neg_Gamma_5_2"]["lower_dec"]) > -1.32935

    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau = 2 * arb.pi()

        # 1. Ratio threshold R <= 1/2: K = 1, xi = 2/tau => omega = 2, R_even = 4/15 < 1/2
        r_ev_2, r_od_2 = compute_hat_f_tail_ratios_arb(arb(2), 1)
        assert bool(r_ev_2.upper() <= arb("0.5"))
        assert bool(r_od_2.upper() <= arb("0.5"))
        val_k1_w2_strict = evaluate_hat_f_hypergeometric_certified_arb(2 / tau, K_terms=1, prec_bits=256, strict_K=True)
        val_w2_adapt = evaluate_hat_f_hypergeometric_certified_arb(2 / tau, K_terms=120, prec_bits=256)
        assert bool((val_k1_w2_strict - val_w2_adapt).contains(0))

        # 2. Ratio threshold 1/2 < R < 1: K = 1, xi = 3/tau => omega = 3, R_even = 9/15 = 3/5 in (1/2, 1)
        r_ev_3, r_od_3 = compute_hat_f_tail_ratios_arb(arb(3), 1)
        assert bool(r_ev_3.lower() > arb("0.5")) and bool(r_ev_3.upper() < arb(1))
        assert bool(r_od_3.upper() <= arb("0.5"))
        val_k1_w3_strict = evaluate_hat_f_hypergeometric_certified_arb(3 / tau, K_terms=1, prec_bits=256, strict_K=True)
        val_w3_adapt = evaluate_hat_f_hypergeometric_certified_arb(3 / tau, K_terms=120, prec_bits=256)
        assert bool(val_k1_w3_strict.lower() <= val_w3_adapt.lower())
        assert bool(val_k1_w3_strict.upper() >= val_w3_adapt.upper())

        # 3. Ratio threshold R > 1: K = 1, xi = 4/tau => omega = 4, R_even = 16/15 > 1
        r_ev_4, _ = compute_hat_f_tail_ratios_arb(arb(4), 1)
        assert bool(r_ev_4.lower() > arb(1))
        with pytest.raises(ValueError, match="R_even"):
            evaluate_hat_f_hypergeometric_certified_arb(4 / tau, K_terms=1, prec_bits=256, strict_K=True)
        val_k1_w4_adaptive = evaluate_hat_f_hypergeometric_certified_arb(
            4 / tau, K_terms=1, prec_bits=256, strict_K=False
        )
        val_w4_quad = evaluate_hat_f_quadrature_certified_arb(4 / tau, prec_bits=256)
        assert bool((val_k1_w4_adaptive - val_w4_quad).contains(0))

        # 4. Zero frequency and even symmetry hat{f}(-xi) = hat{f}(xi)
        val_zero = evaluate_hat_f_hypergeometric_certified_arb(0, prec_bits=256)
        gamma_5_2 = (3 * (tau / 2).sqrt()) / 4
        assert bool((val_zero - gamma_5_2).contains(0))
        for xi_test in [Fraction(1, 2), Fraction(3, 2), 2]:
            pos_val = evaluate_hat_f_hypergeometric_certified_arb(xi_test, prec_bits=256)
            neg_val = evaluate_hat_f_hypergeometric_certified_arb(-xi_test, prec_bits=256)
            assert bool((pos_val - neg_val).contains(0))

        # 5. Large frequencies xi = 10 and xi = 20 (bounded by Gamma(5/2) and tight adaptive radius)
        for xi_large in [10, 20]:
            v_large = evaluate_hat_f_hypergeometric_certified_arb(xi_large, K_terms=10, prec_bits=256)
            assert bool(abs(v_large).upper() <= gamma_5_2.upper())
            assert bool(v_large.rad() < arb("1e-30"))

        # 6. Interval inputs (narrow ball around 1/2 and interval straddling 0)
        xi_ball = arb("0.5") + arb(0, "1e-10")
        v_ball = evaluate_hat_f_hypergeometric_certified_arb(xi_ball, prec_bits=256)
        v_pt_low = evaluate_hat_f_hypergeometric_certified_arb(arb("0.5") - arb("1e-10"), prec_bits=256)
        v_pt_high = evaluate_hat_f_hypergeometric_certified_arb(arb("0.5") + arb("1e-10"), prec_bits=256)
        assert bool(v_ball.overlaps(v_pt_low)) and bool(v_ball.overlaps(v_pt_high))

        xi_straddle = arb(0, "0.25")
        v_straddle = evaluate_hat_f_hypergeometric_certified_arb(xi_straddle, prec_bits=256)
        assert bool(v_straddle.overlaps(val_zero))

        # 7. Parameter validation
        with pytest.raises(ValueError, match="K_terms"):
            evaluate_hat_f_hypergeometric_certified_arb(1, K_terms=0)
        with pytest.raises(ValueError, match="prec_bits"):
            evaluate_hat_f_hypergeometric_certified_arb(1, prec_bits=16)
    finally:
        flint_ctx.prec = saved_prec


def test_section_5_transition_poisson_summation_and_sign_changes() -> None:
    """Verify non-Schwartz C^1(R/Z) Poisson summation formula, certified sign changes of hat{f}(xi),
    and independent quadrature cross-checks.
    """
    sec5 = verify_section_5_poisson_summation_at_transition(prec_bits=256)
    assert "NOT in the Schwartz class" in sec5["poisson_summation_hypotheses_and_non_schwartz_note"]
    assert "DLMF 1.8.14" in sec5["poisson_summation_hypotheses_and_non_schwartz_note"]
    assert sec5["all_witnesses_agree_with_independent_quadrature"] is True
    assert sec5["all_poisson_enclosures_contain_zero_difference"] is True

    witnesses = {w["xi_label"]: w for w in sec5["hat_f_sign_change_witnesses"]}
    assert witnesses["0"]["sign_strictly_certified"] is True
    assert float(witnesses["0"]["hat_f_xi"]["lower_dec"]) > 1.32934

    assert witnesses["1/2"]["expected_sign"] == "negative"
    assert witnesses["1/2"]["sign_strictly_certified"] is True
    assert float(witnesses["1/2"]["hat_f_xi"]["upper_dec"]) < -0.562854

    assert witnesses["4/tau"]["expected_sign"] == "negative"
    assert witnesses["4/tau"]["sign_strictly_certified"] is True
    assert float(witnesses["4/tau"]["hat_f_xi"]["upper_dec"]) < -0.775775

    assert witnesses["1"]["expected_sign"] == "negative"
    assert witnesses["1"]["sign_strictly_certified"] is True
    assert float(witnesses["1"]["hat_f_xi"]["upper_dec"]) < -0.366836

    assert witnesses["3/2"]["expected_sign"] == "positive"
    assert witnesses["3/2"]["sign_strictly_certified"] is True
    assert float(witnesses["3/2"]["hat_f_xi"]["lower_dec"]) > 0.263617

    assert witnesses["2"]["expected_sign"] == "positive"
    assert witnesses["2"]["sign_strictly_certified"] is True
    assert float(witnesses["2"]["hat_f_xi"]["lower_dec"]) > 0.124712

    for prow in sec5["poisson_vs_direct_d_sum_rows"]:
        assert prow["zero_in_difference"] is True


def test_exact_cutoffs_straddling_balls_and_decoupled_blocks() -> None:
    """Verify exact rational cutoffs for U_lambda(Y; M) across integer/rational endpoints,
    values just below/above integers (1 +/- 2^{-42}), doubled endpoints (3/2 +/- 2^{-42}),
    0 < M < 1, straddling arb balls ('enclose' vs 'raise'), and direct vs decoupled B_{A,B}(X)
    on both dyadic and non-integer (A, B).
    """
    cutoff_reg = reproduce_tc054_cutoff_tolerance_counterexample_arb(prec_bits=256)
    assert cutoff_reg["true_integer_set"] == [2]
    assert cutoff_reg["old_tolerance_selected_integer_set"] == [1]
    assert cutoff_reg["true_value_strictly_negative"] is True
    assert cutoff_reg["old_value_strictly_positive"] is True
    assert cutoff_reg["repaired_matches_true_exact"] is True

    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # m=1 term at Y=1 is +e^{-1}; m=2 term at Y=1 is -e^{-1/4}/8; m=3 term at Y=1 is -e^{-1/9}/27
        term_m1 = (-arb(1)).exp()
        term_m2 = -((-arb(1) / arb(4)).exp()) / arb(8)
        term_m3 = -((-arb(1) / arb(9)).exp()) / arb(27)

        # 1. Exact integer and rational endpoints M = 1, 2, 3/2
        u_m1 = evaluate_1d_dyadic_sum_U_lambda_arb(1, 1, prec_bits=256)
        assert bool((u_m1 - term_m1).contains(0))

        u_m2 = evaluate_1d_dyadic_sum_U_lambda_arb(1, 2, prec_bits=256)
        assert bool((u_m2 - (term_m2 + term_m3)).contains(0))

        u_m3_2 = evaluate_1d_dyadic_sum_U_lambda_arb(1, Fraction(3, 2), prec_bits=256)
        assert bool((u_m3_2 - term_m2).contains(0))

        # 2. Just below and just above 1: M = 1 - 2^{-42} selects {1}, M = 1 + 2^{-42} selects {2}
        eps = Fraction(1, 2**42)
        u_below_1 = evaluate_1d_dyadic_sum_U_lambda_arb(1, Fraction(1) - eps, prec_bits=256)
        assert bool((u_below_1 - term_m1).contains(0))
        u_above_1 = evaluate_1d_dyadic_sum_U_lambda_arb(1, Fraction(1) + eps, prec_bits=256)
        assert bool((u_above_1 - term_m2).contains(0))

        # 3. Doubled endpoint crossing integer 3: M = 3/2 - 2^{-42} selects {2}; M = 3/2 + 2^{-42} selects {2, 3}
        u_below_3_2 = evaluate_1d_dyadic_sum_U_lambda_arb(1, Fraction(3, 2) - eps, prec_bits=256)
        assert bool((u_below_3_2 - term_m2).contains(0))
        u_above_3_2 = evaluate_1d_dyadic_sum_U_lambda_arb(1, Fraction(3, 2) + eps, prec_bits=256)
        assert bool((u_above_3_2 - (term_m2 + term_m3)).contains(0))

        # 4. Positive M < 1: M = 1/4 => [1/4, 1/2) has no integers => 0; M = 3/4 => [3/4, 3/2) selects {1}
        u_quarter = evaluate_1d_dyadic_sum_U_lambda_arb(1, Fraction(1, 4), prec_bits=256)
        assert bool(u_quarter == arb(0))
        u_three_quarters = evaluate_1d_dyadic_sum_U_lambda_arb(1, Fraction(3, 4), prec_bits=256)
        assert bool((u_three_quarters - term_m1).contains(0))

        # 5. Straddling arb ball around M = 1: encloses both {1} and {2} under "enclose", raises under "raise"
        m_straddle = arb(1) + arb(0, "1e-20")
        u_enclose = evaluate_1d_dyadic_sum_U_lambda_arb(
            1, m_straddle, prec_bits=256, on_ambiguous_ball="enclose"
        )
        assert bool(u_enclose.overlaps(term_m1))
        assert bool(u_enclose.overlaps(term_m2))
        assert bool(u_enclose.lower() <= term_m2.lower())
        assert bool(u_enclose.upper() >= term_m1.upper())
        with pytest.raises(ValueError, match="straddles"):
            evaluate_1d_dyadic_sum_U_lambda_arb(
                1, m_straddle, prec_bits=256, on_ambiguous_ball="raise"
            )

        # 6. Direct vs decoupled B_{A,B}(X) on non-integer rational scales (A, B)
        for a_val, b_val, x_val in [
            (Fraction(3, 2), Fraction(5, 2), 2),
            (Fraction(7, 4), Fraction(11, 4), 3),
        ]:
            b_dir = evaluate_rectangular_block_B_AB_certified_arb(
                a_val, b_val, x_val, D_cutoff=80, prec_bits=256
            )
            b_dec = evaluate_decoupled_rectangular_block_B_AB_certified_arb(
                a_val, b_val, x_val, D_cutoff=80, prec_bits=256
            )
            assert bool((b_dir - b_dec).contains(0))
    finally:
        flint_ctx.prec = saved_prec


def test_section_6_separable_gaussian_decoupling_abel_scaling_and_dyadic_parity() -> None:
    """Verify rectangular-block separable Gaussian decoupling, repaired unequal-block bound
    (7/3)*C_* min(A,B)^3 / max(A,B)^2, unimodal d-sum bound, repaired Abel scaling & global
    Stieltjes energy proof, and dyadic parity annihilation/inversion (Attack B).
    """
    sec6 = verify_section_6_transition_attacks_and_decoupling(prec_bits=256)
    rect = sec6["rectangular_block_decomposition_and_decoupling"]
    assert rect["all_unimodal_d_sum_bounds_hold"] is True
    assert rect["all_decoupled_blocks_match_direct"] is True
    assert rect["all_widely_unequal_bounds_hold"] is True
    assert float(rect["C_star"]["lower_dec"]) <= 2.008921040021895 <= float(rect["C_star"]["upper_dec"])
    assert (
        float(rect["seven_thirds_C_star"]["lower_dec"])
        <= 4.687482426717755
        <= float(rect["seven_thirds_C_star"]["upper_dec"])
    )

    abel_proof = verify_abel_scaling_and_global_stieltjes_energy_proof(prec_bits=256)
    assert "M^{1/2}" in abel_proof["corrected_dyadic_abel_bound"]["formula"]
    assert abel_proof["divisor_weight_collapse_identity"]["verified_up_to_q_100"] is True
    assert abel_proof["scaling_integral_verification"]["zero_in_difference"] is True
    assert abel_proof["global_stieltjes_energy_proof"]["all_stieltjes_rows_match_direct"] is True

    att_a = sec6["attack_A_coprime_euler_series_and_separable_gaussian_replacement_theorem"]
    assert att_a["residue_at_z_0_strictly_negative"] is True
    for mrow in att_a["mellin_1d_rows"]:
        assert mrow["zero_in_difference"] is True
    for brow in att_a["bivariate_coprime_dirichlet_rows"]:
        assert brow["zero_in_difference"] is True

    att_b = sec6["attack_B_dyadic_parity_and_cross_scale_correlation"]
    assert att_b["all_dyadic_parity_identities_hold"] is True
    for drow in att_b["dyadic_parity_rows"]:
        assert drow["odd_sum_zero_in_difference"] is True
        assert drow["dyadic_inversion_zero_in_difference"] is True
        assert drow["pointwise_energy_zero_in_difference"] is True
    for orow in att_b["off_critical_mode_nonvanishing_rows"]:
        assert orow["strictly_positive_lower_bound"] is True


def test_lean_formalization_and_serialized_artifact_synchronization() -> None:
    """Verify formal/RiemannScope/LiouvilleSquareDilation.lean registration, 8 public theorems,
    live captured #check and #print axioms outputs, and serialized artifact integrity.
    """
    rel_lean = "formal/RiemannScope/LiouvilleSquareDilation.lean"
    assert rel_lean in REQUIRED_FORMAL_SOURCES
    assert rel_lean in FORMAL_SOURCE_FILES
    root_lean = (REPO_ROOT / "formal" / "RiemannScope.lean").read_text(encoding="utf-8")
    assert "import RiemannScope.LiouvilleSquareDilation" in root_lean

    lean_info = verify_liouville_square_dilation_lean_module()
    assert lean_info["definition_count"] == 21
    assert lean_info["public_theorem_count"] == 12
    assert lean_info["private_helper_theorem_count"] == 16
    assert lean_info["total_declaration_count"] == 49
    assert lean_info["expected_public_theorems_present"] is True
    assert lean_info["sorry_count"] == 0
    assert lean_info["custom_axiom_count"] == 0

    assert LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH.exists()
    artifact = json.loads(LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert artifact["task_id"] == TASK_TC_054_ID
    assert artifact["repair_task_id"] == TASK_TC_054R_ID
    assert artifact["closeout_task_id"] == TASK_TC_054R2_ID
    assert artifact["simultaneous_compatibility_task_id"] == TASK_TC_055_ID
    assert artifact["simultaneous_compatibility_repair_task_id"] == TASK_TC_055R_ID
    assert artifact["prior_merged_main"] == PRIOR_MERGED_MAIN_TC_053R
    assert artifact["tc053r2_implementation_commit"] == TC_053R2_IMPLEMENTATION_COMMIT
    assert artifact["tc053r2_reviewed_tip"] == TC_053R2_REVIEWED_TIP
    assert artifact["tc054_implementation_commit"] == TC_054_IMPLEMENTATION_COMMIT
    assert artifact["tc054_reviewed_tip"] == TC_054_REVIEWED_TIP
    assert artifact["tc054r_implementation_commit"] == TC_054R_IMPLEMENTATION_COMMIT
    assert artifact["tc054r_reviewed_tip"] == TC_054R_REVIEWED_TIP
    assert artifact["tc054r2_implementation_commit"] == TC_054R2_IMPLEMENTATION_COMMIT
    assert artifact["tc054r2_reviewed_tip"] == TC_054R2_REVIEWED_TIP
    assert artifact["tc054r2_merged_main_baseline"] == TC_054R2_MERGED_MAIN_BASELINE
    assert artifact["tc055_implementation_commit"] == TC_055_IMPLEMENTATION_COMMIT
    assert artifact["tc055_reviewed_tip"] == TC_055_REVIEWED_TIP
    assert artifact["tc055_initial_closeout_commit"] == TC_055_INITIAL_CLOSEOUT_COMMIT
    assert artifact["subgate_tc043a_status"] == "OPEN"
    assert artifact["rh_proved"] is False

    live_audit = artifact["section_7_lean_formalization_audit"]["live_lean_invocation_audit"]
    assert live_audit["exit_code"] == 0
    per_thm = live_audit["per_theorem_captured_output"]
    assert set(per_thm.keys()) == set(EXPECTED_PUBLIC_THEOREM_NAMES)
    for thm_name, cap in per_thm.items():
        assert thm_name in cap["captured_check_output"]
        assert "depends on axioms:" in cap["captured_print_axioms_output"]
    assert (
        "actualFlatMoebiusSquareDivisorSum"
        in per_thm["actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat"][
            "captured_check_output"
        ]
    )
    assert (
        "actualFlatInverseLiouvilleSquareDivisorSum"
        in per_thm["actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat"][
            "captured_check_output"
        ]
    )
    assert (
        "Finset.Ico"
        in per_thm["abel_scaling_fourier_ratio_and_unequal_block_algebra"]["captured_check_output"]
    )

    live_rep = execute_task_tc054_liouville_square_dilation_audit(prec_bits=256)
    arb_check = verify_all_serialized_arb_in_tree(live_rep)
    assert arb_check["all_enclose_original_256bit_arb_ball"] is True
    assert arb_check["failed_paths"] == []


def test_section_4_pairwise_spurious_factor_counterexample_regression() -> None:
    """Verify the r=1, s=1, L=9/5 (X = 9/(5*sqrt(2))) counterexample falsifying the old
    TC-054 draft factor 1/(2*sqrt(2)) on the pairwise common-factor remainder while
    satisfying the repaired C_2 bound.
    """
    sec4 = verify_section_4_unconstrained_common_factor_and_euler_maclaurin(prec_bits=256)
    reg = sec4["pairwise_spurious_factor_counterexample_regression"]
    assert reg["r"] == 1
    assert reg["s"] == 1
    assert reg["L_formula"] == "9/5"
    assert reg["ratio_strictly_exceeds_1_over_2_sqrt2"] is True
    assert reg["true_pairwise_bound_holds"] is True
    assert reg["spurious_pairwise_bound_violated"] is True
    assert float(reg["ratio_abs_error_over_C2_L_neg7"]["lower_dec"]) > 0.403034
    assert float(reg["spurious_factor_1_over_2_sqrt2"]["upper_dec"]) < 0.353554
    assert float(reg["ratio_minus_1_over_2_sqrt2"]["lower_dec"]) > 0.04948


def test_section_5_mellin_contour_reflection_dlmf_and_even_sign_identities() -> None:
    """Verify the TASK-TC-054R2 Mellin contour proof identities (lack of exponential decay of
    1/|sin(tau*z/4)*Gamma(1-z)| on z = 1/2 + i*b, corrected reflection formula, DLMF 5.8.3
    lower bound, shifted contour a_M = -(2M+3/2) decay, strictly positive even tail signs
    (-1)^m Gamma(5/2-m) > 0 for m >= 2), and separate series vs quadrature accuracy metadata.
    """
    contour_rep = verify_mellin_contour_and_reflection_identities_arb(prec_bits=256)
    assert (
        contour_rep["critical_line_constant_product_check"][
            "all_rows_match_constant_2_over_sqrt_tau"
        ]
        is True
    )
    assert (
        contour_rep["corrected_reflection_and_mellin_kernel_identities"][
            "all_reflection_and_kernel_identities_hold"
        ]
        is True
    )
    assert (
        contour_rep["dlmf_5_8_3_gamma_lower_bound_checks"]["all_dlmf_lower_bounds_hold"]
        is True
    )
    assert all(
        row["abs_sin_tau_z_over_2_equals_cosh_tau_b_over_2_at_b1"]
        for row in contour_rep["shifted_contour_remainder_bounds"]["rows_at_omega_4"]
    )
    assert contour_rep["even_series_term_sign_analysis"]["all_m_ge_2_strictly_positive"] is True
    assert contour_rep["even_series_term_sign_analysis"]["m3_matches_Gamma_1_2_over_360"] is True

    sec5 = verify_section_5_poisson_summation_at_transition(prec_bits=256)
    for w in sec5["hat_f_sign_change_witnesses"]:
        assert isinstance(w["working_prec_bits"], int) and w["working_prec_bits"] >= 256
        assert isinstance(w["series_truncation_K_eff"], int) and w["series_truncation_K_eff"] >= 2
        assert "series_truncation_radius" in w
        assert "series_total_radius" in w
        assert "quadrature_interval" in w
        assert "quadrature_right_tail_bound_2_over_5_V1_pow_5" in w
        assert "quadrature_total_radius" in w
        assert w["quadrature_contains_series"] is True
        assert w["series_overlaps_quadrature"] is True
        assert w["series_minus_quadrature_contains_zero"] is True


def test_tc054r2_closeout_report_and_corpus_formula_synchronization() -> None:
    """Verify docs/reviews/TC_054R2_CLOSEOUT_REPORT.md, compact-range energy coefficient
    zeta(3)^2*(tau^5-1)/5, and verify that none of the corpus records retain stale TC-054
    draft formulas.
    """
    closeout_path = REPO_ROOT / "docs" / "reviews" / "TC_054R2_CLOSEOUT_REPORT.md"
    assert closeout_path.exists()
    closeout_text = closeout_path.read_text(encoding="utf-8")
    for token in [
        "TASK-TC-054R2",
        "27489f195d3313d9ee60773157e3a8240f5bcadd",
        "f265042ab52cabda29e76859cebace21cfae9239",
        "actualFlatMoebiusSquareDivisorSum",
        "actualFlatInverseLiouvilleSquareDivisorSum",
        "0.4030344210273",
        "2829.665108928656654314420748974452322268",
    ]:
        assert token in closeout_text, f"Missing {token!r} in TC_054R2_CLOSEOUT_REPORT.md"

    abel_proof = verify_abel_scaling_and_global_stieltjes_energy_proof(prec_bits=256)
    g_stieltjes = abel_proof["global_stieltjes_energy_proof"]
    coeff = g_stieltjes["compact_range_Y5_coefficient_zeta3_sq_tau5_minus_1_over_5"]
    assert float(coeff["lower_dec"]) <= 2829.6651089286567 <= float(coeff["upper_dec"])
    assert "Y >= 256" in g_stieltjes["stretched_exponential_range"]
    assert "Y >= 2" in g_stieltjes["all_logarithmic_range"]

    # Check that stale TC-054 and retired TC-055 draft formulas are absent from all updated corpus records
    stale_tokens = (
        "d^{-5/2} Q_\\mu(X/d)",
        "d^{-5/2}Q_\\mu(X/d)",
        "d^{-5/2} Q_mu(X/d)",
        "1 + 2^{-(2+z)}",
        "(1/8)*Q_lambda(X/2)",
        "\\frac{1}{8}Q_\\lambda(X/2)",
        "2(3/(2e))^{3/2} = (3/e)^{3/2}",
        "2(3/(2e))^{3/2}=(3/e)^{3/2}",
    )
    corpus_files = [
        REPO_ROOT / "RESEARCH_LEDGER.md",
        REPO_ROOT / "TRANSCENDENTAL_CONTINUATION.md",
        REPO_ROOT / ".agents" / "corpus_map" / "obligation_register.md",
        REPO_ROOT / "docs" / "reviews" / "TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md",
        REPO_ROOT / "docs" / "reviews" / "TC_055_SIMULTANEOUS_TAU_COMPATIBILITY.md",
        REPO_ROOT / "formal" / "RiemannScope" / "README.md",
        REPO_ROOT / ".agents" / "research" / "queue.json",
        REPO_ROOT / ".agents" / "research" / "state.json",
    ]
    for cpath in corpus_files:
        ctext = cpath.read_text(encoding="utf-8")
        for st in stale_tokens:
            assert st not in ctext, f"Stale TC-054/TC-055 token {st!r} found in {cpath.name}"


def test_tc054_review_and_state_synchronization() -> None:
    """Verify that docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md, .agents/research/state.json,
    and .agents/research/queue.json are synchronized with data/tc_liouville_square_dilation.json
    and keep SUBGATE-TC-043A OPEN and rh_proved False.
    """
    review_path = REPO_ROOT / "docs" / "reviews" / "TC_LIOUVILLE_SQUARE_DILATION.md"
    assert review_path.exists()
    review_text = review_path.read_text(encoding="utf-8")
    for token in [
        "0.6646701940895685102368128062529294435491",
        "1.851257667016958056850958359201349291641",
        "8.752371760035365551239039765015814873069",
        "-0.5628546550179851263755109492164491931001",
        "-0.7757751802167744117629682956314216290713",
        "-0.3668367826642069184644449070564857828859",
        "0.2636171831500303372338138695632955698496",
        "0.1247126116325928138362162976104693467978",
        "2.008921040021894970679058028804597412605",
        "4.687482426717754931584468733877393962745",
        "0.9462603202968596578665609415280250426843",
        *EXPECTED_PUBLIC_THEOREM_NAMES,
    ]:
        assert token in review_text, f"Missing token {token!r} in TC_LIOUVILLE_SQUARE_DILATION.md"

    artifact = json.loads(LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH.read_text(encoding="utf-8"))
    em = artifact["section_4_unconstrained_common_factor_and_euler_maclaurin"][
        "euler_maclaurin_derivatives_and_constants"
    ]
    rect = artifact["section_6_rectangular_blocks_and_transition_attacks"][
        "rectangular_block_decomposition_and_decoupling"
    ]
    abel = artifact["section_6_rectangular_blocks_and_transition_attacks"][
        "abel_scaling_and_global_stieltjes_energy_proof"
    ]
    witnesses = {
        w["xi_label"]: w["hat_f_xi"]
        for w in artifact["section_5_transition_poisson_summation"]["hat_f_sign_change_witnesses"]
    }
    displayed_latex_checks = [
        (
            "[0.6646701940895685102368128062529294435491 \\pm 2.00 \\times 10^{-40}]",
            "0.6646701940895685102368128062529294435491",
            "2.00e-40",
            artifact["section_5_transition_poisson_summation"]["c_0"],
        ),
        (
            "[0.4211708612882846189067416640646506740997 \\pm 2.00 \\times 10^{-40}]",
            "0.4211708612882846189067416640646506740997",
            "2.00e-40",
            em["v_minus"],
        ),
        (
            "[0.7327351635395962094861244517470714998819 \\pm 2.00 \\times 10^{-40}]",
            "0.7327351635395962094861244517470714998819",
            "2.00e-40",
            em["v_plus"],
        ),
        (
            "[1.851257667016958056850958359201349291641 \\pm 2.00 \\times 10^{-39}]",
            "1.851257667016958056850958359201349291641",
            "2.00e-39",
            em["C_2"],
        ),
        (
            "[8.752371760035365551239039765015814873069 \\pm 4.00 \\times 10^{-39}]",
            "8.752371760035365551239039765015814873069",
            "4.00e-39",
            em["C_4"],
        ),
        (
            "[2.008921040021894970679058028804597412605 \\pm 2.00 \\times 10^{-39}]",
            "2.008921040021894970679058028804597412605",
            "2.00e-39",
            rect["C_star"],
        ),
        (
            "[4.687482426717754931584468733877393962745 \\pm 2.00 \\times 10^{-39}]",
            "4.687482426717754931584468733877393962745",
            "2.00e-39",
            rect["seven_thirds_C_star"],
        ),
        (
            "[0.9462603202968596578665609415280250426843 \\pm 2.00 \\times 10^{-40}]",
            "0.9462603202968596578665609415280250426843",
            "2.00e-40",
            abel["scaling_integral_verification"]["closed_form"],
        ),
        (
            "[-0.1551682265483492584272379814757961069612 \\pm 2.00 \\times 10^{-40}]",
            "-0.1551682265483492584272379814757961069612",
            "2.00e-40",
            artifact["section_6_rectangular_blocks_and_transition_attacks"][
                "attack_A_coprime_euler_series_and_separable_gaussian_replacement_theorem"
            ]["residue_at_z_0_Gamma_5_4_over_4_zeta_1_2"],
        ),
    ]
    getcontext().prec = 100
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for disp_str, mid_s, rad_s, cert in displayed_latex_checks:
            assert disp_str in review_text, f"Missing displayed interval {disp_str!r} in TC_LIOUVILLE_SQUARE_DILATION.md"
            d_mid = Decimal(mid_s)
            d_rad = Decimal(rad_s)
            c_low = Decimal(cert["lower_dec"])
            c_high = Decimal(cert["upper_dec"])
            assert d_mid - d_rad <= c_low <= c_high <= d_mid + d_rad
            b_cert = arb(cert["arb_ball_str"])
            b_disp = arb(mid_s) + arb(0, rad_s)
            assert bool(b_disp.lower() <= b_cert.lower()) and bool(b_disp.upper() >= b_cert.upper())
        for xi_label, cert in witnesses.items():
            assert cert["arb_ball_str"] in review_text, f"Missing witness arb_ball_str for xi={xi_label}"
            b_cert = arb(cert["arb_ball_str"])
            assert bool(b_cert.lower() >= arb(cert["lower_dec"]).lower())
            assert bool(b_cert.upper() <= arb(cert["upper_dec"]).upper())
    finally:
        flint_ctx.prec = saved_prec

    state = json.loads((REPO_ROOT / ".agents" / "research" / "state.json").read_text(encoding="utf-8"))
    assert "data/tc_liouville_square_dilation.json" in state["linked_runs"]["campaign_artifacts"]

    queue = json.loads((REPO_ROOT / ".agents" / "research" / "queue.json").read_text(encoding="utf-8"))
    assert queue["active_task_id"] in ("TASK-TC-054", "TASK-TC-055", "TASK-TC-055R")
    tc055_entries = [t for t in queue["tasks"] if t["task_id"] == "TASK-TC-055"]
    assert len(tc055_entries) == 1
    assert tc055_entries[0]["status"] == "OPEN"
    assert tc055_entries[0]["review_status"] == "AWAITING_INDEPENDENT_REVIEW"


def test_tc055_simultaneous_joint_identities_and_trivial_zero_cancellation() -> None:
    """Verify TASK-TC-055 Section 1 & Section 3:
    - Dependency chain and grade-scope note (K in A_R = Qbar intersect R, Lindemann irrationality,
      no claim of log_tau(2) transcendence).
    - Exact finite-prime exclusion sieve sum sum_{d | gcd(n, N_P)} |mu(d)| lambda(n / d) = 1_{gcd(n, N_P)=1} lambda(n)
      up to n = 120 for N_P in {2, 6, 30, 210}.
    - Removable trivial-zero ratio cancellation lim_{z -> -(2m+1/2)} zeta(1+2z)/zeta(1/2+z) = 2 zeta'(-4m)/zeta'(-2m) != 0,
      and pole/zero locations of D_lambda(s) = zeta(2s)/zeta(s) (pole at s = 1/2, zero at s = 1).
    - Direct coprime sum vs operator product prod_{p in P}(I + p^{-1/2} S_p) Q_lambda(X) and convergent P-smooth
      inverse reconstruction Q_lambda(X) = sum_{m in S(P)} (lambda(m)/sqrt(m)) Q_{lambda,P}(X/m).
    """
    sec8 = verify_tc055_simultaneous_joint_identities_and_trivial_zero_cancellation(prec_bits=256)
    assert len(sec8["dependency_chain_to_subgate_tc043a"]) == 4
    assert "do NOT claim log_tau(2) is transcendental" in sec8["grade_scope_and_auxiliary_dilation_distinction"]
    assert sec8["sieve_integer_audit_up_to_120"]["all_sieve_sums_match_coprime_indicator_times_lambda"] is True
    tz = sec8["trivial_zero_and_mellin_cancellation_audit"]
    assert tz["all_trivial_zero_ratios_match_and_nonzero"] is True
    assert "s = 1/2" in tz["pole_and_zero_locations_note"]
    assert "s = 1" in tz["pole_and_zero_locations_note"]
    assert sec8["all_prime_exclusion_and_inverse_checks_hold"] is True

    for row in sec8["finite_prime_exclusion_and_inverse_rows"]:
        assert row["comparison_classification"] == "same_observable_operator_vs_series_consistency_check"
        assert row["forward_zero_in_difference"] is True
        assert row["inverse_zero_in_difference"] is True


def test_tc055_coupled_cutoff_neumann_majorant_and_off_critical_modes() -> None:
    """Verify TASK-TC-055 Section 4 and TASK-TC-055R Section 4 & 5.2:
    - Non-integer cutoff counterexample at u = 2.9: sum_{n > 2.9} n^{-3} = 0.0770569... > 1/(2 * 2.9^2) = 50/841 = 0.059453...,
      and 3-term sum 1/27 + 1/64 + 1/125 = 0.0606620... > 50/841, while 1/(2 * floor(2.9)^2) = 1/8 = 0.125 holds.
    - Exact coprime decomposition Q_{lambda,P_u}(w) = w^{5/2} exp(-w^2) + R_{lambda,P_u}(w)
      across boundary cutoffs u in {2.9, 3.0, 3.1, 4.9, 5.0, 5.1} and integer cutoffs u in {5, 7, 11, 13}.
    - Exact full-space operator norm ||P_u^{-1}||_{H_eta -> H_eta} = prod_{p <= u} (1 - p^{-1/2 - eta})^{-1}
      with continuous Kronecker approximation witness attaining > 99.9% of the supremum.
    - Off-critical mode multiplier bounds 0 < prod_{p <= u}(1 - p^{-x}) <= |M_u(rho)| <= prod_{p <= u}(1 + p^{-x}).
    """
    sec9 = verify_tc055_coupled_cutoff_and_norm_obstruction(prec_bits=256)
    cop = sec9["coprime_decomposition_and_coupled_cutoff_attempt"]
    assert cop["all_coprime_tail_bounds_hold"] is True
    for r in cop["coprime_tail_rows"]:
        assert r["bound_strictly_certified"] is True

    u29 = sec9["non_integer_cutoff_counterexample_and_boundary_repair"]
    assert u29["u29_counterexample_and_floor_repair_certified"] is True
    assert u29["all_repaired_boundary_cutoffs_hold"] is True
    assert float(u29["exact_unrestricted_tail_at_2_9"]["lower_dec"]) > 0.077056
    assert float(u29["three_term_lower_bound_n_3_4_5"]["lower_dec"]) > 0.060662
    assert float(u29["claimed_1_over_2_u_sq_at_2_9"]["upper_dec"]) < 0.0594531

    u_labels = {r["u_label"]: r for r in u29["boundary_cutoff_rows"]}
    for lbl in ["2.9", "3.0", "3.1", "4.9", "5.0", "5.1"]:
        assert lbl in u_labels
        assert u_labels[lbl]["repaired_floor_bound_strictly_certified"] is True
        assert u_labels[lbl]["coprime_tail_bounds_strictly_certified"] is True
    assert u_labels["2.9"]["naive_bound_holds_for_unrestricted_tail"] is False

    op_obs = sec9["exact_full_space_operator_norm_obstruction"]
    assert (
        op_obs["kronecker_phase_alignment_witness_P_2_3_5_eta_1_4"][
            "witness_exceeds_99_9_percent_of_supremum"
        ]
        is True
    )
    neum = {r["eta_label"]: r for r in op_obs["rows"]}
    assert neum["1/10"]["uniform_as_u_to_infty"] is False
    assert neum["1/4"]["uniform_as_u_to_infty"] is False
    assert neum["1/2"]["uniform_as_u_to_infty"] is False
    assert neum["3/4"]["uniform_as_u_to_infty"] is True
    assert neum["1"]["uniform_as_u_to_infty"] is True

    modes = sec9["off_critical_mode_test"]
    assert modes["all_mode_bounds_hold"] is True
    for mrow in modes["rows"]:
        assert mrow["strictly_positive_and_within_bounds"] is True


def test_tc055_integrated_energy_kernel_diagonal_asymptotic_and_near_diagonal_band() -> None:
    """Verify TASK-TC-055 Section 5:
    - Closed-form antiderivative evaluation of K_Y(m, n) and symmetry/AM-GM inequality
      2 K_Y(m, n) <= K_Y(m, m) + K_Y(n, n).
    - Diagonal energy asymptotic D_E(Y) = (3 sqrt(tau) / 64) log tau + R_{D,E}(Y)
      with |R_{D,E}(Y)| <= C_{D,2} Y^{-2} and |R_{D,E}(Y)| <= C_{D,4} Y^{-4} for all Y > 0.
    - Near-diagonal band inequality sum_{|m - n| <= H} K_Y(m, n) <= (2 H + 1) D_E(Y).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for Y_int in (1, 2, 4):
            for m_int, n_int in [(1, 2), (2, 5), (3, 7)]:
                k_mn = evaluate_energy_kernel_K_Y_certified_arb(Y_int, m_int, n_int, prec_bits=256)
                k_nm = evaluate_energy_kernel_K_Y_certified_arb(Y_int, n_int, m_int, prec_bits=256)
                k_mm = evaluate_energy_kernel_K_Y_certified_arb(Y_int, m_int, m_int, prec_bits=256)
                k_nn = evaluate_energy_kernel_K_Y_certified_arb(Y_int, n_int, n_int, prec_bits=256)
                assert bool((k_mn - k_nm).contains(0))
                assert bool((k_mm + k_nn - arb(2) * k_mn).lower() > 0)
    finally:
        flint_ctx.prec = saved_prec

    sec10 = verify_tc055_integrated_energy_kernel_and_near_diagonal_bound(prec_bits=256)
    assert sec10["all_diagonal_bounds_hold"] is True
    assert sec10["all_near_diagonal_bounds_hold"] is True
    assert (
        float(sec10["leading_constant_3_sqrt_tau_over_64_log_tau"]["lower_dec"])
        <= 0.2159472478105098
        <= float(sec10["leading_constant_3_sqrt_tau_over_64_log_tau"]["upper_dec"])
    )
    assert (
        float(sec10["explicit_N2_error_constant_C_D2"]["lower_dec"])
        <= 0.07974240995631961
        <= float(sec10["explicit_N2_error_constant_C_D2"]["upper_dec"])
    )


def test_tc055_opposite_parity_dilation_pairing_and_unmatched_residual() -> None:
    """Verify TASK-TC-055R Section 2, Section 3, and Section 5.3:
    - Counterexample to retired TC-055 Lemma 6.1 at Y = 33, p = 11, q = 2, r = 5, m = 1, n = 11 (q r = 10):
      certified normalized difference 0.8194252817... > 3993/10000 = 0.3993, and elementary floating-point-free
      contradiction 1559/2890 > 3993/10000.
    - Valid replacement bounds across all 5 regimes (comparable scales, large Y/a, unequal indices m > 1,
      tiny gaps, and zero gap a = b): two-sided integrand-ratio enclosure and transition relative-gap bound
      ((b - a) / a) (b / a)^3 (3 + 2 tau^2 Y^2 / a^2) K_Y(b, n).
    - Separation of fixed finite factor set vs growing cutoff u = Y^theta unmatched prime energy.
    """
    sec11 = verify_tc055_opposite_parity_dilation_pairing_and_obstruction(prec_bits=256)

    ce = sec11["retired_tc055_lemma61_counterexample"]
    assert ce["counterexample_parameters"] == {
        "Y": 33,
        "p": 11,
        "q": 2,
        "r": 5,
        "qr": 10,
        "m": 1,
        "n": 11,
    }
    assert ce["counterexample_strictly_certified"] is True
    assert float(ce["actual_normalized_difference"]["lower_dec"]) > 0.819425
    assert float(ce["retired_claimed_normalized_upper_bound_3993_over_10000"]["upper_dec"]) <= 0.3993001
    assert (
        "1559/2890 > 3993/10000"
        in ce["elementary_floating_point_free_contradiction"]["inequality_chain"]
    )

    rep = sec11["valid_replacement_bounds"]
    assert rep["all_replacement_bounds_hold"] is True
    regimes = {r["regime"]: r for r in rep["rows"]}
    for reg_name in [
        "comparable_transition_scale",
        "large_Y_over_a_counterexample",
        "large_Y_over_a_subtransition",
        "widely_unequal_indices",
        "tiny_relative_gap",
        "zero_gap_a_eq_b",
    ]:
        assert reg_name in regimes
        assert regimes[reg_name]["two_sided_ratio_enclosure_holds"] is True
        assert regimes[reg_name]["integrand_ratio_diff_bound_holds"] is True
        assert regimes[reg_name]["transition_relative_gap_bound_holds"] is True
    assert regimes["zero_gap_a_eq_b"]["verification_classification"] == "exact_algebraic_zero_identity"
    assert float(regimes["zero_gap_a_eq_b"]["transition_relative_gap_upper_bound"]["upper_dec"]) == 0.0

    obs = sec11["unmatched_residual_and_multiplicity_obstruction"]
    assert obs["unmatched_k_count_with_W_pair_eq_0"] > 0
    assert obs["k_count_with_W_pair_ne_w_bar"] == 240
    assert (
        "Y / (log Y)^2"
        in obs["fixed_vs_growing_factor_set_separation"][
            "growing_factor_set_and_unmatched_primes_scale"
        ]
    )


def test_tc055_multiplicative_parity_controls_a2_and_aS() -> None:
    """Verify TASK-TC-055 Section 7 and TASK-TC-055R Section 5.1:
    - Multiplicative parity controls a_2(n) = (-1)^{v_2(n)} and a_S(n) = (-1)^{sum_{p in S} v_p(n)}:
      complete multiplicativity, common-factor cancellation, parity flip on p in S, and failure of
      sum_{d^2 | n} mu(n/d^2) = a_2(n) at n = 3.
    - Corrected unimodal constant C_{1,uni} = 2 (3 / (2 e))^{3/2} = (1 / sqrt(2)) (3 / e)^{3/2} < (3 / e)^{3/2}
      and second-order Euler-Maclaurin bound |Q_1(X) - sqrt(X)/2| <= 3 X^{-3/2} giving
      |Q_{a_2}(X) - sqrt(X)/6| <= C_{a_2} X^{-1/2} and E_{a_2}(Y) = ((tau - 1) / 36) Y + O(1).
    - S = {3, 5, 7} control mean 1/4, Q_{a_{3,5,7}}(X) ~ (1/8) sqrt(X), E_{a_{3,5,7}}(Y) ~ ((tau - 1)/64) Y.
    """
    for m in range(1, 35):
        for n in range(1, 35):
            assert two_adic_parity_a2_int(m * n) == two_adic_parity_a2_int(m) * two_adic_parity_a2_int(n)
            assert finite_prime_parity_aS_int(m * n, (2, 3)) == (
                finite_prime_parity_aS_int(m, (2, 3)) * finite_prime_parity_aS_int(n, (2, 3))
            )
        assert two_adic_parity_a2_int(2 * m) == -two_adic_parity_a2_int(m)
        assert finite_prime_parity_aS_int(3 * m, (2, 3)) == -finite_prime_parity_aS_int(m, (2, 3))
        assert finite_prime_parity_aS_int(5 * m, (2, 3)) == finite_prime_parity_aS_int(m, (2, 3))
    assert two_adic_parity_a2_int(3) == 1
    assert square_divisor_moebius_sum_int(3) == -1

    sec12 = verify_tc055_multiplicative_parity_controls(prec_bits=256)
    assert sec12["all_q1_bounds_and_dyadic_identities_hold"] is True
    assert sec12["all_e_a2_positive"] is True

    uni_audit = sec12["unimodal_and_second_order_euler_maclaurin_constants"]
    assert uni_audit["unimodal_constant_repair_certified"] is True
    assert 0.819832 < float(uni_audit["exact_C1_unimodal_2_times_3_over_2e_pow_3_2"]["lower_dec"]) <= float(
        uni_audit["exact_C1_unimodal_2_times_3_over_2e_pow_3_2"]["upper_dec"]
    ) < 0.819833
    assert float(uni_audit["strict_upper_3_over_e_pow_3_2"]["lower_dec"]) > 1.159418

    q_rows = {r["X"]: r for r in sec12["Q_a2_rows"]}
    assert q_rows[64]["second_order_em_bound_holds"] is True
    assert q_rows[64]["Q_1_exact_unimodal_and_em2_bounds_hold"] is True
    assert abs(float(q_rows[64]["ratio_Q_a2_over_sqrt_X"]["mid_float"]) - (1.0 / 6.0)) < 5e-3
    assert abs(float(q_rows[64]["scaled_remainder_sqrt_X_times_diff"]["upper_dec"])) < 0.3
    e_rows = {r["Y"]: r for r in sec12["E_a2_rows"]}
    tau_minus_1_over_36 = float(sec12["asymptotic_formulas"]["tau_minus_1_over_36"]["lower_dec"])
    assert (
        float(e_rows[32]["ratio_E_a2_over_Y"]["lower_dec"])
        <= tau_minus_1_over_36
        <= float(e_rows[32]["ratio_E_a2_over_Y"]["upper_dec"])
    )
    assert abs(float(e_rows[32]["ratio_E_a2_over_Y"]["mid_float"]) - tau_minus_1_over_36) < 1e-3

    s357 = sec12["asymptotic_formulas"]["control_S_3_5_7"]
    assert s357["s357_control_certified"] is True
    assert s357["euler_factor_mean_prod_p_minus_1_over_p_plus_1"] == "1/4"
    assert s357["leading_Q_aS_over_sqrt_X_coefficient"] == "1/8"
    assert abs(float(s357["ratio_Q_a_357_over_sqrt_64"]["mid_float"]) - 0.125) < 5e-3


def test_tc055r_finite_truncation_and_signed_energy_attempt() -> None:
    """Verify TASK-TC-055R Section 6:
    - Exact finite T-truncation reconstruction Q_{lambda,T}(X) = sum_{m in S(P), m <= T} (lambda(m)/sqrt(m)) Q_{lambda,P,floor(T/m)}(X/m)
      with m-dependent inner cutoff floor(T/m), and non-zero excess when naive uncoupled cutoff T is used.
    - Tail energy bound int_Y^{tau Y} |Q_lambda(X) - Q_{lambda,T}(X)|^2 dX/X <= ((tau^5 - 1) Y^5) / (20 T^4)
      which is O(1) at T(Y) = ceil(Y^{5/4}), and L^2 transfer E_lambda(Y) <= 2 E_{lambda,T(Y)}(Y) + 2 R_{tail}(Y, T(Y)).
    - Noncircular signed decomposition E_{lambda,T}(Y) = E_{same-r} + E_{diff-r} = E_{smooth-diag} + E_{smooth-cross} < E_{unsigned,T}(Y).
    """
    sec13 = verify_tc055r_finite_truncation_and_signed_energy_attempt(prec_bits=256)
    rec = sec13["exact_finite_reconstruction_theorem"]
    assert rec["all_finite_reconstructions_match"] is True
    for r in rec["rows"]:
        assert r["exact_identity_and_nonzero_common_cutoff_error_verified"] is True

    tail = sec13["finite_truncation_tail_energy_and_L2_transfer"]
    assert tail["all_tail_energy_bounds_hold"] is True
    for r in tail["rows"]:
        assert r["strict_bound_and_uniform_cap_hold"] is True

    s_att = sec13["signed_energy_attempt_on_finite_reconstruction"]
    assert s_att["all_signed_decompositions_consistent"] is True
    for r in s_att["rows"]:
        assert r["coprime_decomposition_zero_in_diff"] is True
        assert r["smooth_decomposition_zero_in_diff"] is True
        assert r["strict_sign_cancellation_below_unsigned"] is True



