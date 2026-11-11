"""Regression and mathematical verification suite for TASK-TC-058 / TASK-TC-058R:
Simultaneous Arithmetic Compatibility, Combined Scale Energy, and Repaired Closure Criteria.

Verifies:
1. Narrow TC-057R repairs (§1): (U=5, T=25) vs T=35 rough squarefree composite witness
   ("when an admissible composite exists") and "sufficient condition" wording for Theorem 26.
2. Reconstructed 5-category dependency table & repaired inherited bridges (§2):
   - Exact finite r^{-1} square-dilation bridge Q_{lambda,T}(X) = sum_{r^2<=T} r^{-1} Q_{mu,floor(T/r^2)}(X/r^2)
     across T in {0, 1, 2, 4, 9, 15, 40, 100}, plus active falsification of the retired r^{-1/2} weight.
   - Uniform B_tau = tau^{5/2}*sqrt(log tau)/2 finite/full norm comparison, quadratic transfer,
     and unsigned a = 1 O(1) tail diagnostic.
   - K-independence of normalized trivial-zero slopes across real algebraic (including negative) grades.
3. Repaired closure implications & normalized finite-horizon absorption (§3):
   - Direct 256-bit Arb quadrature of <P_Y, R_Y>_Y and independent prime-power fiber evaluation.
   - All four closure-criterion contraction coefficients: TC-057R (2*theta + 2*Theta),
     TC-058 S_comb (theta + Theta), second-order T_2 (theta + 4*Theta via E = 4*D_tilde + T_2),
     and growing-order FULL Gram J_M = D_M + X_M ((1+delta)*theta with delta = (1-theta)/2,
     valid at theta = 0), plus the abstract inference countermodel E = D = Y/(log Y)^2, X = r = 0.
4. Compensated Selberg reconstruction & repaired bounds (§4):
   - Finite square projection across T >= 0 (including T = 0, 1) and uniform C_sq bound for X >= 1.
   - Coupled upper-endpoint bound L_{T(Y)} = 1, g_{T(Y)}(X) = phi_{T(Y)}(X), and X^{5/2}/T(Y)^2 <= tau^{5/2}
     including exact fourth-power boundaries Y in {1, 16, 81}.
   - Finite-cutoff smooth-step majorant |Delta_d^{sm}(X)| <= C_sm * sqrt(X) / (d*(d+1)) across
     small d >= 1 and near-endpoint d = T - 1, plus TC-057R Selberg/PNT provenance for |R_2^{int}(d)| <= C_W*d.
5. Growing order M(Y) = ceil(2*log Y) & reconciled numerical scope (§5):
   - Robbins-Stirling + 17-subinterval compact [2, e^9] remainder bound <= 2068*(log Y)*Y^{-3}.
   - Live certified Y = 64 off-diagonal shares (~94.86% for a_2, ~85.03% for a_{3,5,7}, ~96.33% for 1).
   - Nonmonotone finite strict Minkowski triangle excess separating norm ratios from squared-norm ratios.
6. TC compatibility discriminators (§6) & Formal Lean 4 Theorems 27-31 (§7):
   - Exact line-anchor verification in LiouvilleSquareDilation.lean, zero \\pi macros,
     generator-backed displayed enclosures, retired-claim absence, and tampering controls.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re

from flint import arb, arb_series, ctx as flint_ctx
import pytest

from tc.canonical_theta_correlation_bound import REPO_ROOT
from tc.coupled_scale_energy_bootstrap import (
    _tau_arb,
    evaluate_Q_shifted_finite_arb,
    moebius_mu_int,
    rough_squarefree_divisors_band,
)
from tc.liouville_square_dilation import liouville_lambda_int
from tc.prime_chain_contraction import evaluate_phi_n_arb, exact_T_cutoff_ceil_Y_5_4
from tc.simultaneous_compatibility_combined_energy import (
    EXPECTED_TC058_THEOREMS,
    SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH,
    TASK_TC_058_ID,
    TASK_TC_058R_ID,
    TC_057R_IMPLEMENTATION_COMMIT,
    TC_057R_REVIEWED_TIP,
    TC_058_IMPLEMENTATION_COMMIT,
    TC_058_REVIEW_DOC_PATH,
    TC_058_REVIEWED_TIP,
    evaluate_B_tau_cutoff_norm_bound_arb,
    evaluate_C_smooth_step_arb,
    evaluate_C_square_arb,
    evaluate_Q_square_arb,
    evaluate_c_lambda_arb,
    evaluate_direct_cross_term_PR_arb,
    evaluate_finite_square_dilation_Q_mu_rhs_arb,
    evaluate_scaled_fiber_g_arb,
    evaluate_window_tail_norm_and_full_energy_enclosure_arb,
    exact_growing_order_M_int,
    positive_divisor_count_int,
    verify_section_1_and_2_narrow_repairs_and_dependency_table,
    verify_section_3_combined_target_and_direct_cross_term,
    verify_section_4_compensated_selberg_and_shift_elimination,
    verify_section_5_growing_order_and_joint_gram,
    verify_section_6_tc_compatibility_discriminators,
    verify_tc058_lean_theorems_live,
    verify_tc058_review_displayed_enclosures,
)


@pytest.fixture(scope="module")
def tc058_artifact() -> dict:
    assert SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH.exists(), (
        f"Missing {SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH}"
    )
    return json.loads(
        SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH.read_text(encoding="utf-8")
    )


def test_section_1_and_2_narrow_repairs_and_dependency_table(tc058_artifact: dict) -> None:
    """Verify §1 narrow TC-057R repairs and §2 5-category dependency audit + known context."""
    assert tc058_artifact["task_id"] == TASK_TC_058_ID
    assert tc058_artifact["repair_task_id"] == TASK_TC_058R_ID
    assert tc058_artifact["tc057r_implementation_commit"] == TC_057R_IMPLEMENTATION_COMMIT
    assert tc058_artifact["tc057r_reviewed_tip"] == TC_057R_REVIEWED_TIP
    assert tc058_artifact["tc058_implementation_commit"] == TC_058_IMPLEMENTATION_COMMIT
    assert tc058_artifact["tc058_reviewed_tip"] == TC_058_REVIEWED_TIP
    assert tc058_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc058_artifact["rh_proved"] is False

    # Direct live check of §1a: U = 5, T = 25 has NO rough squarefree composite; 35 enters at T = 35
    assert list(rough_squarefree_divisors_band(5, 25)) == [5, 7, 11, 13, 17, 19, 23]
    assert list(rough_squarefree_divisors_band(5, 34)) == [5, 7, 11, 13, 17, 19, 23, 29, 31]
    assert 35 in rough_squarefree_divisors_band(5, 35)

    # Check TC-057R source and review wording repairs
    tc057_py = (REPO_ROOT / "tc" / "coupled_scale_energy_bootstrap.py").read_text(encoding="utf-8")
    tc057_md = (
        REPO_ROOT / "docs" / "reviews" / "TC_057_COUPLED_ARITHMETIC_SCALE_ENERGY_BOOTSTRAP.md"
    ).read_text(encoding="utf-8")
    assert "when an admissible composite exists" in tc057_py
    assert "when an admissible composite exists" in tc057_md
    assert "whenever T >= U^2" not in tc057_py
    assert "whenever $T \\ge U^2$" not in tc057_md
    assert "sufficient condition" in tc057_py
    assert "sufficient condition" in tc057_md

    sec12 = verify_section_1_and_2_narrow_repairs_and_dependency_table(prec_bits=256)
    assert sec12["all_section_1_and_2_checks_pass"] is True
    assert sec12["narrow_tc057r_repairs"]["rough_band_U5_T25_composites"] == []
    assert sec12["narrow_tc057r_repairs"]["rough_band_U5_T34_composites"] == []
    assert sec12["narrow_tc057r_repairs"]["rough_band_U5_T35_composites"] == [35]
    assert sec12["agarwal_garg_maji_riesz_bridge_check"]["verified"] is True
    assert (
        sec12["normalized_trivial_zero_slope_k_independence"][
            "supplies_additional_k_dependent_moments"
        ]
        is False
    )
    assert sec12["normalized_trivial_zero_slope_k_independence"]["verified"] is True

    dep = sec12["compact_dependency_table"]
    assert set(dep.keys()) == {
        "a_actual_arithmetic_theorems",
        "b_analytic_results_proved_outside_lean",
        "c_conditional_implications",
        "d_finite_numerical_observations",
        "e_missing_tc_to_arithmetic_implication",
    }
    for cat_items in dep.values():
        assert len(cat_items) >= 1


def test_section_2_finite_square_bridge_and_B_tau_cutoff_transfer(tc058_artifact: dict) -> None:
    """Verify §4A exact finite r^{-1} square-dilation bridge (and active falsification of r^{-1/2})
    and §4B uniform B_tau norm comparison + unsigned a = 1 tail diagnostic.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau = _tau_arb()
        # 1. Exact finite r^{-1} square-dilation identity across T in {0, 1, 2, 4, 9, 15, 40, 100}
        for T_val in (0, 1, 2, 4, 9, 15, 40, 100):
            for x_int in (0, 1, 7, 13):
                x_arb = arb(x_int)
                lhs = (
                    arb(0)
                    if (T_val == 0 or x_int == 0)
                    else evaluate_Q_shifted_finite_arb(
                        x_arb, L=T_val, m_shift=0, mode="liouville", prec_bits=256
                    )
                )
                rhs = evaluate_finite_square_dilation_Q_mu_rhs_arb(x_arb, T_val, prec_bits=256)
                diff = lhs - rhs
                assert bool(arb(0) in diff)
                assert bool(abs(diff) < arb("1e-68"))

        # Active falsification of the retired r^{-1/2} weight at (X=7, T=40):
        x7 = arb(7)
        q_lam_40 = evaluate_Q_shifted_finite_arb(x7, L=40, m_shift=0, mode="liouville", prec_bits=256)
        wrong_r_half = arb(0)
        for r in range(1, 7):  # r^2 <= 40
            L_in = 40 // (r * r)
            q_mu_in = sum(
                (
                    arb(moebius_mu_int(n)) * evaluate_phi_n_arb(x7 / arb(r * r), n, prec_bits=256)
                    for n in range(1, L_in + 1)
                    if moebius_mu_int(n) != 0
                ),
                arb(0),
            )
            wrong_r_half += q_mu_in / arb(r).sqrt()
        assert bool(abs(wrong_r_half - q_lam_40) > arb("1e-2"))

        # 2. Uniform B_tau cutoff norm comparison and bilateral transfer algebra
        B_tau = evaluate_B_tau_cutoff_norm_bound_arb(prec_bits=256)
        assert bool(arb("67.07") < B_tau < arb("67.08"))
        for Y_val in (1, 2, 4, 8, 16, 81):
            T_Y = exact_T_cutoff_ceil_Y_5_4(Y_val)
            tail_at_upper = ((tau * arb(Y_val)) ** (arb(5) / arb(2))) / (arb(2) * arb(T_Y * T_Y))
            cap = (tau ** (arb(5) / arb(2))) / arb(2)
            if Y_val in (1, 16, 81):
                assert bool(arb(0) in (cap - tail_at_upper))
            else:
                assert bool(cap - tail_at_upper > arb(0))

        enc_lam = evaluate_window_tail_norm_and_full_energy_enclosure_arb(
            8, mode="liouville", N_trunc=800, prec_bits=256
        )
        enc_u1 = evaluate_window_tail_norm_and_full_energy_enclosure_arb(
            8, mode="unsigned_1", N_trunc=800, prec_bits=256
        )
        for enc in (enc_lam, enc_u1):
            assert bool(B_tau - enc["norm_diff_T_to_inf_enclosure"] > arb(0))
            quad_rhs = arb(2) * B_tau * enc["norm_inf_enclosure"] + B_tau * B_tau
            assert bool(quad_rhs - abs(enc["E_T"] - enc["E_inf_enclosure"]) > arb(0))
        # Unsigned diagnostic: O(1) tail norm > 1 (not exponentially decaying)
        assert bool(enc_u1["norm_diff_T_to_inf_enclosure"] > arb(2))
    finally:
        flint_ctx.prec = saved

    ftf = tc058_artifact["section_1_and_2_narrow_repairs_and_dependency_table"][
        "finite_to_full_cutoff_comparison"
    ]
    assert ftf["verified"] is True


def test_section_3_combined_target_closure_table_and_countermodel(
    tc058_artifact: dict,
) -> None:
    """Verify §3 direct <P_Y, R_Y>_Y evaluation, all four closure-criterion contraction
    coefficients (including theta_eta = 0 and 4*Theta for T_2), and the Y/(log Y)^2 logical
    inference countermodel.
    """
    sec3 = tc058_artifact["section_3_combined_target_and_direct_cross_term"]
    assert sec3["all_section_3_checks_pass"] is True
    assert sec3["direct_cross_term_positive_scales"] == [8, 16, 32, 128]
    assert sec3["direct_cross_term_negative_scales"] == [64]
    assert sec3["S_comb_positive_scales"] == [16, 64]
    assert sec3["S_comb_negative_scales"] == [8, 32, 128]
    assert "identities, NOT arithmetic cancellation theorems" in sec3["identity_vs_estimate_note"]

    # Live direct quadrature check at Y = 8 and Y = 64
    c8 = evaluate_direct_cross_term_PR_arb(8, mode="liouville", prec_bits=256)
    c64 = evaluate_direct_cross_term_PR_arb(64, mode="liouville", prec_bits=256)
    assert bool(c8 > arb(0))
    assert bool(c64 < arb(0))

    for f_row in sec3["independent_prime_power_fiber_cross_checks"]:
        assert f_row["verified"] is True

    # Verify all 4 closure-criterion rows & exact contraction formulas
    imp_table = sec3["closure_criteria_implication_table"]
    assert len(imp_table) == 4
    coeffs = [row["contraction_coefficient"] for row in imp_table]
    assert any("2*theta_eta + 2*Theta" in c for c in coeffs)
    assert any("theta_eta + Theta_eps^{diag}(Y)" in c for c in coeffs)
    assert any("theta_eta + 4*Theta_eps^{diag}(Y)" in c for c in coeffs)
    assert any("(1 + delta)*theta_eta" in c for c in coeffs)
    for row in imp_table:
        assert row["arithmetic_hypothesis_status"] == "OPEN"

    # Exact rational Young schedule for J_M across theta_eta in {0, 1/4, 1/2, 3/4, 99/100}
    for theta in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(99, 100)):
        delta = (1 - theta) / 2
        q = (1 + delta) * theta
        rem_mult = 1 + Fraction(1, delta)
        assert delta > 0
        assert 0 <= q < 1
        assert rem_mult >= 3
        if theta == 0:
            assert delta == Fraction(1, 2) and q == 0 and rem_mult == 3

    # Independent verification of E = 4*D_tilde + T_2 and S_comb = 3*D_tilde + T_2 across Y in {8, 16, 32, 64}
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        s3_by_y = {r["Y"]: r for r in sec3["sampled_combined_target_rows"]}
        s4_by_y = {
            r["Y"]: r
            for r in tc058_artifact["section_4_compensated_selberg_and_shift_elimination"][
                "summation_by_parts_and_shift_elimination_rows"
            ]
        }
        for Y_k in (8, 16, 32, 64):
            r3 = s3_by_y[Y_k]
            r4 = s4_by_y[Y_k]
            E_v = arb(r3["E_Y"]["arb_ball_str"])
            D_v = arb(r3["D_tilde_Y"]["arb_ball_str"])
            X_v = arb(r3["X_tilde_Y"]["arb_ball_str"])
            S_v = arb(r3["S_comb_direct"]["arb_ball_str"])
            D2_sq = arb(r4["D2_window_energy_direct"]["arb_ball_str"])
            P_D2 = arb(r4["P_D2_cross_direct"]["arb_ball_str"])
            T2_v = arb(4) * X_v - arb(4) * P_D2 + D2_sq
            assert bool(arb(0) in (E_v - (arb(4) * D_v + T2_v)))
            assert bool(arb(0) in (S_v - (arb(3) * D_v + T2_v)))

        # Verify threshold_log_Y_for_T2_4Theta_q == 2 * threshold_log_Y_for_S_comb_q
        for sched in sec3["relaxed_conditional_absorption_schedule_rows"]:
            lg_s = arb(sched["threshold_log_Y_for_S_comb_q"]["arb_ball_str"])
            lg_t2 = arb(sched["threshold_log_Y_for_T2_4Theta_q"]["arb_ball_str"])
            assert bool(arb(0) in (lg_t2 - arb(2) * lg_s))

        # Verify abstract inference countermodel E = D = Y/(log Y)^2, X = r = 0
        cm = sec3["logical_non_implication_countermodel"]
        assert cm["classification"] == "countermodel_to_inference_not_arithmetic_lambda_counterexample"
        assert cm["sample_witness_eps_half_Mc_10"]["verified"] is True
        y_wit = arb(528).exp()
        e_wit = y_wit / (arb(528) ** 2)
        assert bool(e_wit - arb(10) * y_wit.sqrt() > arb("1e200"))
    finally:
        flint_ctx.prec = saved


def test_section_4_compensated_selberg_endpoint_smooth_step_and_shift_elimination(
    tc058_artifact: dict,
) -> None:
    """Verify §4 square projection (including T=0,1), uniform C_sq bound, coupled upper-endpoint
    bound g_{T(Y)}(X) = phi_{T(Y)}(X) & X^{5/2}/T(Y)^2 <= tau^{5/2} (including exact fourth-power
    boundaries), finite-cutoff smooth-step majorant C_sm, and TC-057R provenance for |R_2^{int}(d)| <= C_W*d.
    """
    sec4 = tc058_artifact["section_4_compensated_selberg_and_shift_elimination"]
    assert sec4["all_section_4_checks_pass"] is True

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau = _tau_arb()
        c_lam = evaluate_c_lambda_arb(prec_bits=256)
        C_sq = evaluate_C_square_arb(prec_bits=256)
        C_sm = evaluate_C_smooth_step_arb(prec_bits=256)
        assert bool(c_lam < arb("-3.43")) and bool(c_lam > arb("-3.44"))
        assert bool(C_sq > arb("1.046")) and bool(C_sq < arb("1.047"))
        assert bool(C_sm > arb("8.204")) and bool(C_sm < arb("8.205"))

        # Boundary T = 0 and T = 1 checks for sum_{d=1}^T g_d(X) = Q_{square,T}(X)
        assert bool(evaluate_Q_square_arb(arb(5), 0, prec_bits=256) == arb(0))
        q_sq_1 = evaluate_Q_square_arb(arb(5), 1, prec_bits=256)
        g1_1 = evaluate_scaled_fiber_g_arb(arb(5), 1, 1, prec_bits=256)
        assert bool(arb(0) in (q_sq_1 - g1_1))
        assert bool(C_sq - evaluate_Q_square_arb(arb(1), 500, prec_bits=256) > arb(0))

        # §3A Coupled upper-endpoint checks including exact fourth-power boundaries Y in {1, 16, 81}
        for Y_ep in (1, 2, 8, 16, 32, 81):
            T_ep = exact_T_cutoff_ceil_Y_5_4(Y_ep)
            assert T_ep // T_ep == 1
            for x_pt in (arb(Y_ep), tau * arb(Y_ep)):
                g_T = evaluate_scaled_fiber_g_arb(x_pt, T_ep, T_ep, prec_bits=256)
                phi_T = evaluate_phi_n_arb(x_pt, T_ep, prec_bits=256)
                assert bool(arb(0) in (g_T - phi_T))
                assert bool(abs(g_T - phi_T) < arb("1e-68"))
            ratio_hi = ((tau * arb(Y_ep)) ** (arb(5) / arb(2))) / arb(T_ep * T_ep)
            tau_5_2 = tau ** (arb(5) / arb(2))
            if Y_ep in (1, 16, 81):
                assert bool(arb(0) in (tau_5_2 - ratio_hi))
            else:
                assert bool(tau_5_2 - ratio_hi > arb(0))

        # §3B Finite-cutoff smooth-step checks |Delta_d^{sm}(X)| <= C_sm*sqrt(X)/(d*(d+1))
        for Y_sm in (4, 8, 16, 32):
            T_sm = exact_T_cutoff_ceil_Y_5_4(Y_sm)
            for d_sm in (1, 2, max(1, T_sm // 2), T_sm - 1):
                L_d = T_sm // d_sm
                for x_pt in (arb(Y_sm), tau * arb(Y_sm)):
                    delta_sm = (
                        evaluate_Q_shifted_finite_arb(
                            x_pt / arb(d_sm), L=L_d, m_shift=0, mode="liouville", prec_bits=256
                        )
                        / arb(d_sm).sqrt()
                        - evaluate_Q_shifted_finite_arb(
                            x_pt / arb(d_sm + 1), L=L_d, m_shift=0, mode="liouville", prec_bits=256
                        )
                        / arb(d_sm + 1).sqrt()
                    )
                    ub = C_sm * x_pt.sqrt() / arb(d_sm * (d_sm + 1))
                    assert bool(ub - abs(delta_sm) > arb(0))

        # Exact jet verification of d/du phi_{u*q}(X) = (sqrt(X)/u^2)*w^2*q^{-3}*exp(-w^2/q^2)*(2*w^2/q^2 - 3)
        # and pointwise |H'_{L_d}(u)| < C_sm * sqrt(X) / u^2 across both w > 1 and 0 < w <= 1
        for x_num, u_num, L_chk in ((4, 1, 7), (16, 2, 16), (1, 1, 5), (64, 181, 1), (1, 4, 3)):
            x_v = arb(x_num)
            u_v = arb(u_num)
            w_v = x_v / u_v
            u_jet = arb_series([u_v, arb(1)], prec=2)
            H_deriv_sum = arb(0)
            for q_int in range(1, L_chk + 1):
                q_v = arb(q_int)
                phi_jet = (
                    (x_v ** (arb(5) / arb(2)))
                    * (u_jet ** (-3))
                    * (q_v ** (-3))
                    * (-(x_v * x_v) / ((u_jet * u_jet) * (q_v * q_v))).exp()
                )
                auto_deriv = phi_jet[1]
                exact_deriv = (
                    (x_v.sqrt() / (u_v * u_v))
                    * (w_v * w_v)
                    * (q_v ** (-3))
                    * (-(w_v * w_v) / (q_v * q_v)).exp()
                    * (arb(2) * (w_v * w_v) / (q_v * q_v) - arb(3))
                )
                assert bool(arb(0) in (auto_deriv - exact_deriv))
                assert bool(abs(auto_deriv - exact_deriv) < arb("1e-65"))
                if x_num != u_num and q_int == 1:
                    retired_typo_deriv = exact_deriv * w_v.sqrt()
                    assert bool(arb(0) not in (auto_deriv - retired_typo_deriv))
                    assert bool(
                        abs(auto_deriv - retired_typo_deriv) > arb("0.4") * abs(auto_deriv)
                    )
                H_deriv_sum += arb(liouville_lambda_int(q_int)) * exact_deriv
            assert bool((C_sm * x_v.sqrt() / (u_v * u_v)) - abs(H_deriv_sum) > arb(0))
    finally:
        flint_ctx.prec = saved

    assert sec4["upper_endpoint_coupled_cutoff_checks"]["verified"] is True
    assert sec4["smooth_step_finite_cutoff_bound_checks"]["verified"] is True
    assert "TC-057R" in sec4["R2_int_linear_bound_provenance"]
    assert "Chebyshev" in sec4["R2_int_linear_bound_provenance"]

    assert positive_divisor_count_int(1) == 1
    assert positive_divisor_count_int(15) == 4
    assert positive_divisor_count_int(36) == 9
    assert (
        sec4["dyadic_parity_control_divisor_identity"][
            "asymptotic_energy_inferred_from_divisor_identity"
        ]
        is False
    )
    assert sec4["dyadic_parity_control_divisor_identity"]["verified"] is True

    rows = sec4["summation_by_parts_and_shift_elimination_rows"]
    assert [r["Y"] for r in rows] == [8, 16, 32, 64]
    for r in rows:
        assert r["verified"] is True
        assert r["jump_count_sum_d_delta_L"] == sum(
            r["T_Y"] // d for d in range(1, r["T_Y"] + 1)
        ) - r["T_Y"]
        assert r["max_jump_product_index"] >= r["T_Y"] + 1
        assert float(r["M_sq_bound_margin"]["lower_dec"]) > 0.0


def test_section_5_growing_order_remainder_live_percentages_and_triangle_excess(
    tc058_artifact: dict,
) -> None:
    """Verify §5 uniform remainder bound, live certified Y = 64 off-diagonal shares (~94.86%,
    ~85.03%, ~96.33%), and nonmonotone norm vs squared-norm Minkowski triangle excess.
    """
    assert exact_growing_order_M_int(2) == 2
    assert exact_growing_order_M_int(8) == 5
    assert exact_growing_order_M_int(64) == 9
    assert exact_growing_order_M_int(Fraction(9, 4)) == 2

    sec5 = tc058_artifact["section_5_growing_order_and_joint_gram"]
    assert sec5["all_section_5_checks_pass"] is True
    assert sec5["generic_in_bounded_controls"] is True
    assert sec5["asymptotic_e9_constants"]["stirling_verified_m_1_to_40"] is True
    assert float(sec5["asymptotic_e9_constants"]["C_rem_ge_e9"]["upper_dec"]) < 38.0

    comp = sec5["compact_2_to_e9_partition"]
    assert comp["subinterval_count"] == 17
    assert comp["C_rem_global_proven"] == 2068
    assert float(comp["C_rem_compact_max"]["upper_dec"]) < 2068.0

    for s_row in sec5["sampled_terminal_remainder_rows"]:
        assert s_row["verified"] is True

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        gram_rows = sec5["joint_M_layer_gram_rows"]
        assert [gr["Y"] for gr in gram_rows] == [8, 16, 32, 64]
        norm_ratios = []
        sq_ratios = []
        for gr in gram_rows:
            lm = gr["modes"]["liouville"]
            nr = arb(lm["minkowski_norm_ratio_over_joint"]["arb_ball_str"])
            sr = arb(lm["minkowski_sq_over_joint_ratio"]["arb_ball_str"])
            assert bool(nr > arb("1.033"))
            assert bool(sr > arb("1.067"))
            assert bool(arb(0) in (nr * nr - sr))
            norm_ratios.append(nr)
            sq_ratios.append(sr)
        # Explicitly verify nonmonotonicity: peak at Y=16 exceeds Y=32, then rises at Y=64
        assert bool(norm_ratios[1] > norm_ratios[0])
        assert bool(norm_ratios[1] > norm_ratios[2])
        assert bool(norm_ratios[3] > norm_ratios[2])
        assert bool(sq_ratios[1] > sq_ratios[2])

        # Recompute Y = 64 percentages directly from live certified numerators & denominators
        y64_modes = next(r["modes"] for r in gram_rows if r["Y"] == 64)
        expected_ranges = {
            "a2": ("94.85", "94.86"),
            "a_3_5_7": ("85.02", "85.03"),
            "unsigned_1": ("96.33", "96.34"),
        }
        for ctrl, (lo_s, hi_s) in expected_ranges.items():
            num_x = arb(y64_modes[ctrl]["joint_M_prime_power_off_diagonal"]["arb_ball_str"])
            den_j = arb(y64_modes[ctrl]["joint_M_layer_norm_sq"]["arb_ball_str"])
            pct_recomp = arb(100) * (num_x / den_j)
            pct_stored = arb(y64_modes[ctrl]["off_diagonal_over_joint_pct"]["arb_ball_str"])
            assert bool(arb(0) in (pct_recomp - pct_stored))
            assert bool(arb(lo_s) < pct_recomp < arb(hi_s))
    finally:
        flint_ctx.prec = saved


def test_section_6_tc_discriminators_and_honest_classification(tc058_artifact: dict) -> None:
    """Verify §6 pre-stated schemas, [Y, b*Y] window-base test, and control discriminators."""
    sec6 = tc058_artifact["section_6_tc_compatibility_discriminators"]
    assert sec6["all_section_6_checks_pass"] is True

    schemas = sec6["prestated_compatibility_lemma_schemas"]
    assert len(schemas) == 6
    assert {s["lemma_id"] for s in schemas} == {
        "LEM-TC058-A",
        "LEM-TC058-B",
        "LEM-TC058-C",
        "LEM-TC058-D",
        "LEM-TC058-E",
        "LEM-TC058R-F",
    }
    required_schema_keys = {
        "lemma_id",
        "title",
        "objects",
        "quantifiers",
        "hypotheses",
        "input_source",
        "conclusion",
        "status",
        "tc_discriminator_result",
    }
    for s in schemas:
        assert required_schema_keys.issubset(s.keys())

    wb = sec6["window_base_discriminator"]
    assert wb["bases_tested"] == ["2", "e", "tau"]
    assert wb["tau_preserved_in_circle_fourier_stirling"] is True
    assert wb["extra_tau_specific_lattice_constraint_found"] is False
    assert wb["honest_classification"] == "TC-inspired analytic number theory"
    assert wb["verified"] is True


def test_section_7_lean_theorems_links_retired_claims_and_tampering_controls(
    tc058_artifact: dict, tmp_path: Path
) -> None:
    """Verify Lean Theorems 27-31, exact line-anchor links, README synchronization, zero \\pi macros,
    absence of retired TC-058 claims, generator-backed displayed enclosures, and tampering controls.
    """
    lean_path = REPO_ROOT / "formal" / "RiemannScope" / "LiouvilleSquareDilation.lean"
    lean_src = lean_path.read_text(encoding="utf-8")
    lean_lines = lean_src.splitlines()
    readme_src = (REPO_ROOT / "formal" / "RiemannScope" / "README.md").read_text(encoding="utf-8")

    expected_new_defs = (
        "positiveDivisorCount",
        "squareVonMangoldtB",
        "liouvilleVonMangoldt",
        "selbergLiouvilleWeight2",
        "scaledLiouvilleFiberG",
        "finiteQSquare",
        "selbergCumulativeW2",
        "selbergCenteredRemainderInt",
        "scaledFiberSmoothStep",
        "scaledFiberCutoffJump",
        "normalizedPrimePowerTermP",
        "normalizedFirstShiftTermR",
        "compensatedSelbergResidualD2",
        "pointwisePrimePowerDiagNorm",
        "pointwisePrimePowerOffDiagNorm",
        "pointwiseCombinedResidualS",
        "growingLogOrderM",
        "growingLogFilterPoly",
        "jointLayerKernelFilter",
        "jointPrimePowerFiber",
    )
    for dname in expected_new_defs:
        assert re.search(rf"^(?:noncomputable\s+)?def\s+{dname}\b", lean_src, flags=re.MULTILINE)
        assert f"`{dname}`" in readme_src

    assert len(EXPECTED_TC058_THEOREMS) == 5
    for thm in EXPECTED_TC058_THEOREMS:
        assert re.search(rf"^theorem\s+{thm}\b", lean_src, flags=re.MULTILINE)
        assert f"`{thm}`" in readme_src

    lean_live = verify_tc058_lean_theorems_live()
    assert lean_live["all_tc058_lean_checks_pass"] is True
    assert lean_live["sorry_count"] == 0
    assert lean_live["custom_axiom_count"] == 0
    expected_std_axioms = {"propext", "Classical.choice", "Quot.sound"}
    for thm in EXPECTED_TC058_THEOREMS:
        assert set(lean_live["per_theorem"][thm]["parsed_axioms"]) == expected_std_axioms
        assert (
            set(
                tc058_artifact["section_7_lean_formalization_audit"]["per_theorem"][thm][
                    "parsed_axioms"
                ]
            )
            == expected_std_axioms
        )

    arb_self = tc058_artifact["serialized_arb_self_check"]
    assert arb_self["total_certified_arb_balls_checked"] >= 580
    assert arb_self["live_original_count_matches_enumerated_total"] is True
    assert arb_self["all_enclose_original_256bit_arb_ball"] is True
    assert arb_self["failed_paths"] == []

    assert TC_058_REVIEW_DOC_PATH.exists()
    rev_check = verify_tc058_review_displayed_enclosures(tc058_artifact, TC_058_REVIEW_DOC_PATH)
    assert rev_check["pi_macro_count"] == 0
    assert rev_check["untagged_count"] == 0
    assert rev_check["failed_count"] == 0
    assert rev_check["total_displayed_intervals_found"] >= 50
    assert rev_check["all_displayed_intervals_contain_generated_enclosures"] is True

    orig_text = TC_058_REVIEW_DOC_PATH.read_text(encoding="utf-8")

    # Verify every LiouvilleSquareDilation.lean#Lstart-Lend link in the review doc points to a real theorem
    anchor_matches = re.findall(r"LiouvilleSquareDilation\.lean#L(\d+)-L(\d+)", orig_text)
    assert len(anchor_matches) >= 5
    for s_ln_s, e_ln_s in anchor_matches:
        s_ln, e_ln = int(s_ln_s), int(e_ln_s)
        assert 1 <= s_ln <= e_ln <= len(lean_lines)
        assert lean_lines[s_ln - 1].startswith("theorem ")

    # Verify absence of retired TC-058 claims in review doc and JSON artifact
    artifact_raw = SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH.read_text(
        encoding="utf-8"
    )
    for retired in (
        "r^{-1/2} Q_\\mu",
        "Y^{-5/8}",
        "\\mathbb{Q} \\cap \\mathbb{R}",
        "growing Minkowski blowup",
        "E_\\infty(Y) + O(Y\\exp",
        "exp(-c' sqrt(log Y))",
    ):
        assert retired not in orig_text, f"Retired claim {retired!r} survived in review doc"
        assert retired not in artifact_raw, f"Retired claim {retired!r} survived in JSON artifact"

    # Tamper 1: inject forbidden \pi macro
    p_pi = tmp_path / "tamper_pi.md"
    p_pi.write_text(orig_text + "\nForbidden circle constant $\\pi$.\n", encoding="utf-8")
    res_pi = verify_tc058_review_displayed_enclosures(tc058_artifact, p_pi)
    assert res_pi["pi_macro_count"] >= 1
    assert res_pi["all_displayed_intervals_contain_generated_enclosures"] is False

    # Tamper 2: inject untagged interval
    p_untag = tmp_path / "tamper_untag.md"
    p_untag.write_text(orig_text + "\nUntagged `[1.0464 +/- 1.0e-3]`.\n", encoding="utf-8")
    res_untag = verify_tc058_review_displayed_enclosures(tc058_artifact, p_untag)
    assert res_untag["untagged_count"] >= 1
    assert res_untag["all_displayed_intervals_contain_generated_enclosures"] is False

    # Tamper 3: inject wrong midpoint on C_sq
    p_bad = tmp_path / "tamper_bad_mid.md"
    p_bad.write_text(
        orig_text
        + '\nWrong `[2.0464331771475893 +/- 1.0e-12]` <!-- tc-enclosure: observable="C_sq" params="" json_path="section_4_compensated_selberg_and_shift_elimination.C_sq" -->\n',
        encoding="utf-8",
    )
    res_bad = verify_tc058_review_displayed_enclosures(tc058_artifact, p_bad)
    assert res_bad["failed_count"] >= 1
    assert res_bad["all_displayed_intervals_contain_generated_enclosures"] is False

    # Tamper 4: inject overly wide interval on C_sq
    p_wide = tmp_path / "tamper_wide.md"
    p_wide.write_text(
        orig_text
        + '\nWide `[1.0464331771475893 +/- 0.5]` <!-- tc-enclosure: observable="C_sq" params="" json_path="section_4_compensated_selberg_and_shift_elimination.C_sq" -->\n',
        encoding="utf-8",
    )
    res_wide = verify_tc058_review_displayed_enclosures(tc058_artifact, p_wide)
    assert res_wide["failed_count"] >= 1
    assert res_wide["all_displayed_intervals_contain_generated_enclosures"] is False
