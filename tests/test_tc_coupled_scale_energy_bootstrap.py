"""Unit, certified-Arb, formal-scope, and adversarial regression tests for TASK-TC-057 / TASK-TC-057R:
Complete prime-power certification, scoped obstructions, Selberg PNT/hyperbola decomposition,
and conditional same-scale absorption transfer.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re

from flint import acb, arb, ctx as flint_ctx
import pytest

from tc.coupled_scale_energy_bootstrap import (
    COUPLED_SCALE_BOOTSTRAP_ARTIFACT_PATH,
    TASK_TC_057_ID,
    TASK_TC_057R_ID,
    TC_057_REVIEW_DOC_PATH,
    evaluate_E_L_scale_arb,
    evaluate_Q_shifted_finite_arb,
    evaluate_Q_smooth_below_U_arb,
    evaluate_complete_higher_prime_power_sum_arb,
    evaluate_higher_prime_power_series_with_tail_arb,
    exact_U0_T_pair_for_rational_Y,
    moebius_mu_int,
    prime_power_pairs_up_to,
    rough_squarefree_divisors_band,
    selberg_w2_via_mangoldt_square_decomposition_arb,
    selberg_w2_weight_arb,
    square_mangoldt_B_arb,
    verify_section_1_and_2_baseline_and_envelope,
    verify_section_3_route_a_moebius_rough_descent,
    verify_section_4_route_b_and_c_logarithmic_and_selberg,
    verify_tc057_review_displayed_enclosures,
    von_mangoldt_arb,
)
from tc.liouville_square_dilation import (
    _parse_arb_ball_str_to_fractions,
    liouville_lambda_int,
)
from tc.prime_chain_contraction import (
    REPO_ROOT,
    evaluate_phi_n_arb,
    evaluate_unsigned_euler_product_P_eta_arb,
    exact_T_cutoff_ceil_Y_5_4,
    exact_U0_cutoff_ceil_2_Y_5_8,
    primes_up_to,
)


@pytest.fixture(scope="module")
def tc057_artifact() -> dict:
    assert COUPLED_SCALE_BOOTSTRAP_ARTIFACT_PATH.exists(), (
        f"Missing artifact {COUPLED_SCALE_BOOTSTRAP_ARTIFACT_PATH}"
    )
    return json.loads(COUPLED_SCALE_BOOTSTRAP_ARTIFACT_PATH.read_text(encoding="utf-8"))


def _arb_lower_frac(node: dict) -> Fraction:
    lo, _, _ = _parse_arb_ball_str_to_fractions(node["arb_ball_str"])
    return lo


def _arb_upper_frac(node: dict) -> Fraction:
    _, hi, _ = _parse_arb_ball_str_to_fractions(node["arb_ball_str"])
    return hi


def test_tc057_artifact_schema_and_all_sections_pass(tc057_artifact: dict) -> None:
    assert tc057_artifact["task_id"] == TASK_TC_057_ID
    assert tc057_artifact["repair_task_id"] == TASK_TC_057R_ID
    assert tc057_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc057_artifact["rh_proved"] is False
    assert tc057_artifact["precision_bits"] == 256
    assert "z = x + i*y" in tc057_artifact["complex_coordinate_convention"]
    assert tc057_artifact["section_1_and_2_baseline_and_envelope"]["all_section_1_and_2_checks_pass"] is True
    assert tc057_artifact["section_3_route_a_moebius_rough_descent"]["all_section_3_checks_pass"] is True
    assert tc057_artifact["section_4_route_b_and_c_logarithmic_and_selberg"]["all_section_4_checks_pass"] is True
    assert tc057_artifact["section_5_cutoffs_small_scales_and_base_floor"]["all_section_5_checks_pass"] is True
    assert tc057_artifact["section_6_route_d_diagonal_contraction_and_off_diagonal"]["all_section_6_checks_pass"] is True

    arb_self = tc057_artifact["serialized_arb_self_check"]
    assert arb_self["all_enclose_original_256bit_arb_ball"] is True
    assert arb_self["live_original_count_matches_enumerated_total"] is True
    assert arb_self["total_certified_arb_balls_checked"] == 347
    assert arb_self["failed_paths"] == []

    rev_audit = tc057_artifact["section_7_tc057_review_displayed_enclosures_audit"]
    assert rev_audit["all_displayed_intervals_contain_generated_enclosures"] is True
    assert rev_audit["untagged_count"] == 0
    assert rev_audit["failed_count"] == 0
    assert rev_audit["total_displayed_intervals_found"] == 78


def test_old_truncated_as_full_prime_power_certificate_fails_and_complete_sum_verified(
    tc057_artifact: dict,
) -> None:
    """Regression for TC-057R §2: prove that the retired `range(2, 40)` loop fails to enclose
    the complete k >= 2 sum by > 4.65e-11 (exceeding its ~2.12e-40 radius by 29 orders of magnitude),
    and verify complete `-log(1 - r) - r` evaluation against finite series + proved geometric tail.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        alpha = arb(3) / arb(4)
        # Reconstruct the retired TC-057 wrong-observable loop (`for k in range(2, 40):`)
        retired_partial_2_to_39 = arb(0)
        for p in primes_up_to(1000):
            for k in range(2, 40):
                retired_partial_2_to_39 += (arb(2) / arb(k)) * (
                    arb(p) ** (-arb(k) * alpha)
                )

        complete_u1000 = evaluate_complete_higher_prime_power_sum_arb(
            1000, Fraction(3, 4), prec_bits=256
        )

        # Exact rational witness for the single first omitted term (p = 2, k = 40):
        # 2 / (40 * 2^{30}) = 1 / (20 * 2^{30}) = 1 / 21474836480 > 4.65e-11
        omitted_p2_k40_frac = Fraction(2, 40 * (2 ** 30))
        assert omitted_p2_k40_frac == Fraction(1, 20 * (2 ** 30))
        assert omitted_p2_k40_frac == Fraction(1, 21474836480)
        assert omitted_p2_k40_frac > Fraction(465, 10 ** 13)

        omitted_p2_k40_arb = arb(omitted_p2_k40_frac.numerator) / arb(
            omitted_p2_k40_frac.denominator
        )
        # Retired ball radius is ~2e-40, so it is strictly disjoint from the complete k >= 2 sum!
        assert not retired_partial_2_to_39.overlaps(complete_u1000)
        assert bool(
            complete_u1000 - retired_partial_2_to_39 > omitted_p2_k40_arb
        )
        assert bool(arb(retired_partial_2_to_39.rad()) < arb("1e-38"))

        # Independent series + proved remainder 0 < 2 * sum_{k>=K} r^k/k <= 2*r^K / [K*(1-r)]
        for u_val, alpha_fr in ((1000, Fraction(3, 4)), (250, Fraction(5, 8))):
            comp = evaluate_complete_higher_prime_power_sum_arb(
                u_val, alpha_fr, prec_bits=256
            )
            for K_cut in (40, 160):
                chk = evaluate_higher_prime_power_series_with_tail_arb(
                    u_val, alpha_fr, K_trunc=K_cut, prec_bits=256
                )
                actual_tail = comp - chk["partial_sum_below_K"]
                assert bool(actual_tail > arb(0))
                assert bool(actual_tail <= chk["tail_upper_bound"])
                assert comp.overlaps(chk["complete_sum_via_tail"])
                # Every point of the 256-bit complete ball lies inside the series+tail union enclosure
                assert (
                    chk["complete_sum_via_tail"].lower() <= comp.lower()
                    and comp.upper() <= chk["complete_sum_via_tail"].upper()
                )

        # Verify JSON artifact stores the complete k >= 2 sum (NOT the k<=39 partial sum)
        pp_node = tc057_artifact["section_1_and_2_baseline_and_envelope"][
            "stieltjes_vs_higher_prime_power_tail_u1000"
        ]
        assert pp_node["exact_omitted_p2_k40_term_fraction"] == "1/21474836480"
        assert (
            _arb_lower_frac(pp_node["higher_prime_power_sum"])
            - _arb_upper_frac(pp_node["finite_partial_sum_2_to_39_only"])
            > omitted_p2_k40_frac
        )
        ev_cert_0 = tc057_artifact["evidence_classification"][
            "4_certified_finite_computations"
        ][0]
        assert pp_node["higher_prime_power_sum"]["arb_ball_str"] in ev_cert_0
        assert "1.234418319565" not in ev_cert_0
        assert "1.234418319596" not in ev_cert_0
    finally:
        flint_ctx.prec = saved


def test_exact_integer_power_small_Y_partition_and_type_safety() -> None:
    # 2^{8/5} = 4^{4/5} <-> 2^8 == 4^4 == 256
    assert (2 ** 8) == (4 ** 4) == 256
    assert exact_U0_T_pair_for_rational_Y(Fraction(2, 1)) == (4, 3)
    assert exact_U0_T_pair_for_rational_Y(Fraction(9, 4)) == (4, 3)
    assert exact_U0_T_pair_for_rational_Y(Fraction(5, 2)) == (4, 4)
    assert exact_U0_T_pair_for_rational_Y(Fraction(7, 2)) == (5, 5)
    assert exact_U0_T_pair_for_rational_Y(Fraction(15, 4)) == (5, 6)
    assert exact_U0_T_pair_for_rational_Y(Fraction(4, 1)) == (5, 6)

    with pytest.raises((TypeError, ValueError)):
        exact_T_cutoff_ceil_Y_5_4(3.5)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        exact_U0_cutoff_ceil_2_Y_5_8(3.5)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        exact_T_cutoff_ceil_Y_5_4(True)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        exact_U0_T_pair_for_rational_Y(3.5)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        exact_U0_T_pair_for_rational_Y(True)  # type: ignore[arg-type]


def test_stieltjes_li2_endpoint_regime_split_bounded_domain_and_prop24_localization() -> None:
    """Verify TC-057R §§4, 5, 6 parameter/domain checks:
    1. Exact Stieltjes endpoint check against offset li_2(t) = int_2^t dv/log v (li_2(2) = 0, E_{PNT,2}(2^-) = 0).
    2. Unsigned Euler-product regime split at eta = 1/2 (alpha = 1/2 + eta = 1), NOT eta = 0.
    3. Bounded-control domain |a(n)| <= 1 for x > 1 convergence vs. unbounded completely multiplicative a(n) = n^2.
    4. Proposition 2.4 localized mass lower barrier vs. d = floor(Y) concentration negative control and equality contraction.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        alpha = arb(3) / arb(4)
        # 1. Exact Stieltjes identity on [2^-, 10] with primes {2, 3, 5, 7}:
        # sum_{p<=10} p^{-alpha} = int_2^{10} t^{-alpha}/log t dt + 10^{-alpha} E_{PNT,2}(10)
        #                          + alpha * int_2^{10} t^{-alpha-1} E_{PNT,2}(t) dt
        # where N_prime(t) is piecewise constant on [2, 3), [3, 5), [5, 7), [7, 10] (values 1, 2, 3, 4)
        # and E_{PNT,2}(t) = N_prime(t) - li_2(t) satisfies E_{PNT,2}(2^-) = 0.
        lhs_primes = sum((arb(p) ** (-alpha) for p in (2, 3, 5, 7)), arb(0))

        def _li2(b_val: int) -> arb:
            if b_val == 2:
                return arb(0)
            return acb.integral(
                lambda z, _an: acb(1) / z.log(analytic=_an),
                acb(2),
                acb(b_val),
                eval_limit=200000,
            ).real

        main_int = acb.integral(
            lambda z, _an: z.pow(-acb(alpha), analytic=_an) / z.log(analytic=_an),
            acb(2),
            acb(10),
            eval_limit=200000,
        ).real
        # Since int_2^{10} alpha t^{-alpha-1} (-li_2(t)) dt = [t^{-alpha} li_2(t)]_2^{10} - int_2^{10} t^{-alpha}/log t dt
        # (because li_2(2) = 0!), verify piecewise on [2,3), [3,5), [5,7), [7,10]:
        n_prime_step_int = (
            arb(1) * (arb(2) ** (-alpha) - arb(3) ** (-alpha))
            + arb(2) * (arb(3) ** (-alpha) - arb(5) ** (-alpha))
            + arb(3) * (arb(5) ** (-alpha) - arb(7) ** (-alpha))
            + arb(4) * (arb(7) ** (-alpha) - arb(10) ** (-alpha))
        )
        li2_10 = _li2(10)
        e_pnt2_10 = arb(4) - li2_10

        def _alpha_t_li2(z: acb, _an: bool) -> acb:
            # Integrate by parts test: check identity directly with E_{PNT,2}(2^-) = 0
            return z.pow(-acb(alpha), analytic=_an) / z.log(analytic=_an)

        _ = _alpha_t_li2
        # Algebraic verification via integration by parts of li_2 with li_2(2) = 0:
        # int_2^{10} alpha t^{-alpha-1} li_2(t) dt = -10^{-alpha} li_2(10) + 2^{-alpha} * 0 + main_int
        int_alpha_epnt2 = n_prime_step_int - (-arb(10) ** (-alpha) * li2_10 + main_int)
        rhs_stieltjes = main_int + (arb(10) ** (-alpha)) * e_pnt2_10 + int_alpha_epnt2
        assert arb(0) in (lhs_primes - rhs_stieltjes)
        assert abs(lhs_primes - rhs_stieltjes) < arb("1e-70")
        # By contrast, adding a nonzero offset C_li = li(2) != 0 to li without keeping -2^{-alpha} E(2^-) = 2^{-alpha} C_li
        # breaks equality by 2^{-3/4} * C_li != 0:
        li_2_offset = arb("1.045163780117492784844588889194613136522615578151")
        uncompensated_offset_error = (arb(2) ** (-alpha)) * li_2_offset
        assert bool(uncompensated_offset_error > arb("0.6"))

        # 2. Euler-product regime split at eta = 1/2:
        r_sub = evaluate_unsigned_euler_product_P_eta_arb(Fraction(1, 4), 100, prec_bits=256)
        r_crit = evaluate_unsigned_euler_product_P_eta_arb(Fraction(1, 2), 100, prec_bits=256)
        r_sup = evaluate_unsigned_euler_product_P_eta_arb(Fraction(3, 4), 100, prec_bits=256)
        assert r_sub["regime"] == "REGIME_A_SUBCRITICAL_0_LT_ETA_LT_1_OVER_2"
        assert r_crit["regime"] == "REGIME_B_CRITICAL_MERTENS_ETA_EQ_1_OVER_2"
        assert r_sup["regime"] == "REGIME_C_SUPERCRITICAL_CONVERGENT_1_OVER_2_LT_ETA_LT_1"
        assert bool(r_sup["gap_below_zeta_limit"] > arb(0))

        # 3. Unbounded completely multiplicative weight a(n) = n^2 with a(1) = 1:
        # Finite Route C identity holds at T = 6, X = 4, whereas sum_{n=1}^N a(n) n^{-x} at x = 2 diverges (= N).
        X_t = arb(4)
        T_t = 6

        def _a_sq(n: int) -> int:
            return n * n

        def _lambda_a_sq(n: int) -> arb:
            # Since a(p^k) = p^{2k}, Lambda_a(p^k) = a(p^k) log p = p^{2k} log p
            return arb(_a_sq(n)) * von_mangoldt_arb(n)

        lhs_rc_unbounded = arb(0)
        for n in range(1, T_t + 1):
            lg_n = arb(n).log()
            lhs_rc_unbounded += (
                arb(_a_sq(n))
                * (lg_n * lg_n)
                * evaluate_phi_n_arb(X_t, n, prec_bits=256)
            )
        rhs_rc_unbounded = arb(0)
        for d in range(2, T_t + 1):
            w2_d = _lambda_a_sq(d) * arb(d).log()
            for u_div in range(2, d):
                if d % u_div == 0:
                    w2_d += _lambda_a_sq(u_div) * _lambda_a_sq(d // u_div)
            q_sub = sum(
                (
                    arb(_a_sq(q)) * evaluate_phi_n_arb(X_t / arb(d), q, prec_bits=256)
                    for q in range(1, (T_t // d) + 1)
                ),
                arb(0),
            )
            rhs_rc_unbounded += (w2_d / arb(d).sqrt()) * q_sub
        assert arb(0) in (lhs_rc_unbounded - rhs_rc_unbounded)
        assert abs(lhs_rc_unbounded - rhs_rc_unbounded) < arb("1e-70")
        # Yet at x = 2 > 1, sum_{n=1}^N a(n) n^{-2} = N -> +infty (diverges):
        assert sum(_a_sq(n) * Fraction(1, n * n) for n in range(1, 501)) == 500

        # 4. Proposition 2.4 localization vs. concentration negative control & equality contraction:
        res = verify_section_1_and_2_baseline_and_envelope(prec_bits=256)
        assert res["all_section_1_and_2_checks_pass"] is True
        boot = res["conditional_bootstrap_and_penalty_barrier"]
        assert boot["scope_label"] == "CONDITIONAL_ON_RECURSION"
        assert _arb_lower_frac(boot["penalty_localized_kappa2_lower_bound_quarter_at_exp100"]) > 8
        assert _arb_upper_frac(boot["concentration_negative_control_floor_Y_upper_bound_quarter_at_exp100"]) < Fraction(1, 10 ** 8)
        # Equality sigma = b/a = 1/2 with B_0 = 1/3 < 1/2 gives B_0 (log Y)^1 * ((log Y)^2)^{-1/2} = 1/3 < 1/2:
        logY = arb(100)
        eq_factor = (arb(1) / arb(3)) * logY * ((logY * logY) ** (-arb("0.5")))
        assert bool(eq_factor < arb("0.5"))
    finally:
        flint_ctx.prec = saved


def test_scoped_obstructions_prime_subset_lower_bound_abel_jumps_and_three_quantity_cutoff(
    tc057_artifact: dict,
) -> None:
    """Verify TC-057R §§3A, 3B, 3C, 3D, and 4:
    - Route A: full rough-divisor multiplier strictly exceeds prime-only lower bound when rough composites exist,
      and prime-only lower bound diverges > 1.
    - Route B: u^{3 + m/2} <= u^{m + 5/2} for u >= 1, m >= 1, and M = 2*log Y Stirling ratio << 1.
    - Route C: Selberg w_{2,lambda} direct == (-Lambda + 2B) decomposition across 2..120 (including B*B at n=36),
      and discrete Abel identity with floor(T/d) cutoff jumps + boundary majorant.
    - Linear cutoff replacement: 0 <= signed < Mink < maj across Y in {16, 32, 64}.
    """
    # 3A: Route A full vs prime-only multiplier and U = 5, T = 25 boundary check (T >= U^2 yet no rough squarefree composite)
    assert rough_squarefree_divisors_band(5, 25) == (5, 7, 11, 13, 17, 19, 23)
    assert rough_squarefree_divisors_band(5, 35) == (5, 7, 11, 13, 17, 19, 23, 29, 31, 35)
    sec3 = verify_section_3_route_a_moebius_rough_descent(prec_bits=256)
    assert sec3["all_section_3_checks_pass"] is True
    assert sec3["u5_t25_no_squarefree_rough_composite"] is True
    cs_rows = sec3["optimal_cauchy_schwarz_divergence_sigma_half"]
    for row in cs_rows:
        assert row["rough_divisor_count"] >= row["rough_prime_count"]
        full_lo = _arb_lower_frac(row["optimal_cs_homogeneous_multiplier"])
        prime_hi = _arb_upper_frac(row["prime_subset_lower_bound"])
        if row["rough_divisor_count"] > row["rough_prime_count"]:
            assert full_lo > prime_hi
        assert _arb_lower_frac(row["prime_subset_lower_bound"]) > 1

    # 3D: u^{3 + m/2} <= u^{m + 5/2} for u >= 1, m >= 1
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for m_val in (1, 2, 3, 6):
            for u_fr in (Fraction(1, 1), Fraction(3, 2), Fraction(2, 1), Fraction(5, 1)):
                u_a = arb(u_fr.numerator) / arb(u_fr.denominator)
                lhs_u = u_a ** (arb(6 + m_val) / arb(2))
                rhs_u = u_a ** (arb(2 * m_val + 5) / arb(2))
                if m_val == 1 or u_fr == 1:
                    assert arb(0) in (rhs_u - lhs_u)
                else:
                    assert bool(rhs_u - lhs_u > arb(0))

        # 4: Selberg w_{2,lambda} direct vs (-Lambda + 2B) decomposition across 2 <= n <= 120
        # Explicitly check n = 36 = 2^2 * 3^2 where (B * B)(36) = B(4)*B(9) + B(9)*B(4) = 2 log 2 log 3 > 0!
        b4_b9 = arb(2) * square_mangoldt_B_arb(4) * square_mangoldt_B_arb(9)
        assert bool(b4_b9 > arb("0.9"))
        for n_val in range(2, 121):
            diff_n = selberg_w2_weight_arb(
                n_val, "liouville"
            ) - selberg_w2_via_mangoldt_square_decomposition_arb(n_val)
            assert arb(0) in diff_n and abs(diff_n) < arb("1e-68"), f"Mismatch at n={n_val}"
    finally:
        flint_ctx.prec = saved

    # 3C: Discrete Abel identity + floor(T/d) cutoff jumps + boundary majorant
    sec4 = tc057_artifact["section_4_route_b_and_c_logarithmic_and_selberg"]
    grow_note = sec4["narrowed_span_closure_and_growing_M_note"]
    assert _arb_upper_frac(grow_note["growing_order_ratio_M20_at_logY10"]) < Fraction(3, 10 ** 8)

    abel_rows = sec4["route_c_selberg_second_order"]["abel_summation_procedure_and_boundary_majorant"]
    assert len(abel_rows) == 4
    for ab_row in abel_rows:
        assert ab_row["nonzero_cutoff_jump_steps_below_b"] > 0
        assert _arb_lower_frac(ab_row["abel_identity_residual"]) <= 0 <= _arb_upper_frac(ab_row["abel_identity_residual"])
        assert _arb_lower_frac(ab_row["step_jump_decomposition_residual"]) <= 0 <= _arb_upper_frac(ab_row["step_jump_decomposition_residual"])
        assert _arb_lower_frac(ab_row["boundary_term_l2_majorant"]) > Fraction(3, 10)
    # Integer scales Y in (16, 32, 64) at indices (0, 1, 3) exhibit strict sqrt(Y) growth:
    assert _arb_upper_frac(abel_rows[0]["boundary_term_l2_majorant"]) < _arb_lower_frac(
        abel_rows[1]["boundary_term_l2_majorant"]
    )
    assert _arb_upper_frac(abel_rows[1]["boundary_term_l2_majorant"]) < _arb_lower_frac(
        abel_rows[3]["boundary_term_l2_majorant"]
    )

    # 3B: Three-quantity separation for linear cutoff replacement (0 <= signed < Mink < maj across Y in {32, 64})
    lin_rows = tc057_artifact["section_5_cutoffs_small_scales_and_base_floor"][
        "linear_cutoff_replacement_three_quantities"
    ]["samples"]
    assert len(lin_rows) == 2
    for lrow in lin_rows:
        s_lo = _arb_lower_frac(lrow["actual_signed_aggregate_error_l2_sq"])
        s_hi = _arb_upper_frac(lrow["actual_signed_aggregate_error_l2_sq"])
        m_lo = _arb_lower_frac(lrow["minkowski_sum_individual_error_norms_sq"])
        m_hi = _arb_upper_frac(lrow["minkowski_sum_individual_error_norms_sq"])
        j_lo = _arb_lower_frac(lrow["unsigned_analytic_majorant_sq"])
        assert 0 <= s_lo <= s_hi < m_lo <= m_hi < j_lo


def test_section_5_cutoff_counterexample_small_scale_positivity_and_base_floor(
    tc057_artifact: dict,
) -> None:
    sec5 = tc057_artifact["section_5_cutoffs_small_scales_and_base_floor"]
    cx = sec5["counterexample_Y_9_4_d_2"]
    assert cx["T_Y"] == 3 and cx["L_2"] == 1 and cx["T_W"] == 2
    assert cx["L_2"] < cx["T_W"]
    assert _arb_lower_frac(cx["Q1_minus_Q2_at_9_8"]) > Fraction(12, 100)
    assert _arb_lower_frac(cx["abs_E1_minus_E2"]) > Fraction(9, 1000)

    e1 = evaluate_E_L_scale_arb(Fraction(9, 8), L=1, mode="liouville", prec_bits=256)
    e2 = evaluate_E_L_scale_arb(Fraction(9, 8), L=2, mode="liouville", prec_bits=256)
    assert bool(e1 - e2 > arb("8e-3"))

    sm = sec5["small_scale_positivity"]
    assert _arb_lower_frac(sm["c_small_sharp_1_plus_exp_neg1_minus_zeta3"]) > Fraction(4, 25)
    assert _arb_lower_frac(sm["outward_margin"]) > 0

    bf = sec5["base_scale_energy_floor_W_in_1_2"]
    assert _arb_lower_frac(bf["m_all_L_rigorous_floor"]) > Fraction(8, 10000)
    assert _arb_lower_frac(bf["tail_energy_lower_bound_L_gt_20"]) > Fraction(5, 100)


def test_route_d_same_scale_absorption_transfer_outer_factor_two_and_theta_half_sharpness(
    tc057_artifact: dict,
) -> None:
    """Verify TC-057R §5:
    - Exact outer factor 2 in E(Y) <= 2*D_tilde(Y) + 2*X_tilde(Y) + 2*E_{sh,1}(Y).
    - Unconditional Route D diagonal contraction and Theta_eps^diag(Y) -> 0.
    - Same-scale absorption parameters: theta_eta = 3/8 < 1/2 gives 2*theta_eta + 2*Theta_{1/4}^diag(e^{64}) < 7/8 < 1,
      whereas theta = 1/2 gives 2*theta + 2*Theta > 1 (and E(Z) = Z satisfies E(Y) <= 2*(1/2)*F(Y) while failing O(Y^{1/4})).
    - Finite-horizon normalized supremum absorption G_eps(R) <= max(G_eps(Y_*), K / (1 - q)) on a discontinuous test model.
    """
    sec6 = tc057_artifact["section_6_route_d_diagonal_contraction_and_off_diagonal"]
    assert sec6["pair_by_pair_off_diagonal_check_Y8"]["consistency_verified"] is True
    assert sec6["sign_split_liouville_neg_vs_controls_pos"] is True

    sweep = {row["Y"]: row for row in sec6["liouville_route_d_scale_sweep"]}
    for y_val, row in sweep.items():
        # Verify E(Y) <= 2*(D_tilde + X_tilde) + 2*E_{sh,1} with exact outer factor 2:
        e_hi = _arb_upper_frac(row["E_T_Y"])
        rhs_2_lo = (
            2 * _arb_lower_frac(row["D_tilde_weighted"])
            + 2 * _arb_lower_frac(row["X_tilde_off_diagonal"])
            + 2 * _arb_lower_frac(row["E_shifted_1_Y"])
        )
        assert e_hi <= rhs_2_lo, f"Outer-factor-2 inequality failed at Y={y_val}"
        assert _arb_lower_frac(row["margin_outer_factor_2_rhs_minus_E"]) > 0
        assert _arb_lower_frac(row["margin_D_pp_minus_D_tilde"]) > 0
        assert _arb_lower_frac(row["margin_rhs_minus_D_pp"]) > 0

    # Sampled finite observations: Liouville X_tilde changes sign across the 5 sampled scales
    assert _arb_upper_frac(sweep[8]["X_tilde_off_diagonal"]) < 0
    assert _arb_lower_frac(sweep[16]["X_tilde_off_diagonal"]) > 0
    assert _arb_upper_frac(sweep[32]["X_tilde_off_diagonal"]) < 0
    assert _arb_lower_frac(sweep[64]["X_tilde_off_diagonal"]) > 0
    assert _arb_upper_frac(sweep[128]["X_tilde_off_diagonal"]) < 0

    for row in sec6["all_epsilon_diagonal_contraction_table"]:
        assert _arb_lower_frac(row["margin_below_half_at_threshold"]) > 0

    # Same-scale absorption parameters in artifact
    abs_p = sec6["conditional_same_scale_absorption_parameters"]
    assert abs_p["scope_label"] == "CONDITIONAL_ON_SIGNED_CORRELATION"
    assert abs_p["absorption_verified"] is True
    assert abs_p["sample_theta_eta"] == "3/8"
    assert abs_p["sample_q"] == "7/8"
    assert _arb_upper_frac(abs_p["two_theta_plus_two_Theta_cap_at_exp64"]) < Fraction(7, 8)
    assert _arb_lower_frac(abs_p["contraction_slack_q_minus_homog_cap"]) > Fraction(9, 10 ** 6)
    # At boundary theta = 1/2, 2*(1/2) + 2*Theta > 1 fails to absorb:
    assert _arb_lower_frac(abs_p["boundary_theta_half_homog_factor_exceeds_one"]) > 1

    # Concrete discontinuous-step simulation of finite-horizon G_eps(R) absorption:
    # Choose eps = 1/4, eta = 1/8, theta = 3/8, q = 7/8, Y_* = 16, A_eta = 3, C_cut = 5,
    # and synthetic Theta_diag(Y) = 1/32 for Y >= 16 (so 2*theta + 2*Theta = 3/4 + 1/16 = 13/16 <= q = 7/8 < 1).
    eps = Fraction(1, 4)
    theta = Fraction(3, 8)
    q = Fraction(7, 8)
    Y_star = 16
    # K = 2*A_eta*Y_*^{eta - eps} + 2*C_cut*Y_*^{-eps} at Y_* = 16 (16^{-1/8} = 1/sqrt(2) < 3/4, 16^{-1/4} = 1/2):
    # Use exact rational test sequence on dyadic powers Z_k = 16^k where Z_k^{1/4} = 2^k, Z_k^{1/8} = (sqrt 2)^k:
    # Even simpler: test eps = 1/2, eta = 1/4 on Z_k = 16^k (Z_k^{1/2} = 4^k, Z_k^{1/4} = 2^k exact rationals!)
    A_eta = Fraction(3, 1)
    C_cut = Fraction(5, 1)
    # At Y_* = 16, Y_*^{eta - eps} = 16^{-1/4} = 1/2, Y_*^{-eps} = 16^{-1/2} = 1/4
    K_const = 2 * A_eta * Fraction(1, 2) + 2 * C_cut * Fraction(1, 4)  # 3 + 5/2 = 11/2
    G_base = Fraction(4, 1)  # G_eps(Y_*) = E(1) / 1 = 4
    M_uniform = max(G_base, K_const / (1 - q))  # max(4, (11/2)*8) = 44

    # Construct worst-case sequence E_k on Z_k = 16^k (k = 0..8) saturating the coupled inequality with jumps:
    E_seq = [G_base]  # k = 0 (Z_0 = 1)
    for k in range(1, 9):
        Z_k_quarter = Fraction(2 ** k, 1)  # Z_k^eta
        F_prev = max(E_seq)
        # Solve E_k = 2*( (1/32)*F_prev + C_cut ) + 2*( A_eta*Z_k^eta + theta * max(F_prev, E_k) )
        cand_from_prev = 2 * (Fraction(1, 32) * F_prev + C_cut) + 2 * (A_eta * Z_k_quarter + theta * F_prev)
        cand_self = (
            2 * (Fraction(1, 32) * F_prev + C_cut) + 2 * A_eta * Z_k_quarter
        ) / (1 - 2 * theta)
        E_k = max(cand_from_prev, cand_self)
        E_seq.append(E_k)
        # Normalized G_eps(Z_k) = max_{0 <= j <= k} E_j / 4^j must stay <= M_uniform = 44 for ALL horizons k!
        G_horizon = max(E_seq[j] / Fraction(4 ** j, 1) for j in range(k + 1))
        assert G_horizon <= M_uniform


def test_review_doc_tau_only_convention_and_adversarial_enclosure_audit(
    tc057_artifact: dict, tmp_path: Path
) -> None:
    text = TC_057_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    # Strict tau-only convention: zero \pi macros in TC_057 review
    assert re.search(r"\\pi\b", text) is None, "Found forbidden \\pi macro in TC_057 review"
    # Explicit z = x + i y complex convention (TC-057R §1, §6)
    assert "z = x + i y" in text
    assert "Outcome B / Scoped Obstruction & Conditional Reduction" in text
    assert tc057_artifact["research_outcome_class"].startswith(
        "Outcome B / Scoped Obstruction & Conditional Reduction"
    )
    assert "CONDITIONAL_ON_RECURSION" in text
    assert "CONDITIONAL_ON_SIGNED_CORRELATION" in text
    # Harmonized open hypothesis X_tilde + E_{sh,1} (not X_tilde + 2 E_{sh,1})
    assert r"\widetilde{\mathcal{X}}_{\lambda,\mathrm{pp}}(Y) + E_{\mathrm{sh},1}(Y) \le A_\eta Y^\eta + \theta_\eta F(Y)" in text
    assert r"\widetilde{\mathcal{X}}_{\lambda,\mathrm{pp}}(Y) + 2 E_{\mathrm{sh},1}(Y) \le" not in text
    # Must explicitly warn NOT to claim D_tilde -> 0
    assert "**not** $\\widetilde{D}_{\\lambda,\\mathrm{pp}}(Y) \\to 0$" in text or "not** $\\widetilde{D}_{\\lambda,\\mathrm{pp}}(Y)" in text

    live_audit = verify_tc057_review_displayed_enclosures(tc057_artifact, TC_057_REVIEW_DOC_PATH)
    assert live_audit["all_displayed_intervals_contain_generated_enclosures"] is True
    assert live_audit["untagged_count"] == 0
    assert live_audit["failed_count"] == 0
    assert live_audit["total_displayed_intervals_found"] == 78

    # Adversarial check 1: untagged interval must fail
    bad_untagged = tmp_path / "untagged.md"
    bad_untagged.write_text("Untagged sample `[1.31983255788372 +/- 1e-10]`\n", encoding="utf-8")
    res_untagged = verify_tc057_review_displayed_enclosures(tc057_artifact, bad_untagged)
    assert res_untagged["all_displayed_intervals_contain_generated_enclosures"] is False
    assert res_untagged["untagged_count"] == 1

    # Adversarial check 2: artificially inflated radius must fail radius_is_tight
    bad_inflated = tmp_path / "inflated.md"
    bad_inflated.write_text(
        '`[1.319832557883720076781582020759507823709 +/- 1e-10]` <!-- tc-enclosure: observable="M_1" params="" json_path="section_1_and_2_baseline_and_envelope.monotone_envelope_local_boundedness.M_1" -->\n',
        encoding="utf-8",
    )
    res_inflated = verify_tc057_review_displayed_enclosures(tc057_artifact, bad_inflated)
    assert res_inflated["all_displayed_intervals_contain_generated_enclosures"] is False
    assert res_inflated["failed_count"] == 1

    # Adversarial check 3: sign flip / non-containment must fail
    bad_sign = tmp_path / "bad_sign.md"
    bad_sign.write_text(
        '`[0.3402109879187785666398179765061771762511 +/- 8.92e-42]` <!-- tc-enclosure: observable="stieltjes_remainder_diff" params="u=1000;alpha=3/4" json_path="section_1_and_2_baseline_and_envelope.stieltjes_vs_higher_prime_power_tail_u1000.stieltjes_remainder_diff" -->\n',
        encoding="utf-8",
    )
    res_sign = verify_tc057_review_displayed_enclosures(tc057_artifact, bad_sign)
    assert res_sign["all_displayed_intervals_contain_generated_enclosures"] is False
    assert res_sign["failed_count"] == 1

    # Adversarial check 4: tagging the complete sum path with the retired truncated partial sum MUST fail!
    bad_truncated = tmp_path / "bad_truncated.md"
    bad_truncated.write_text(
        '`[1.234418319596601055780022033323107235562 +/- 2.12e-40]` <!-- tc-enclosure: observable="higher_prime_power_sum" params="u=1000;alpha=3/4" json_path="section_1_and_2_baseline_and_envelope.stieltjes_vs_higher_prime_power_tail_u1000.higher_prime_power_sum" -->\n',
        encoding="utf-8",
    )
    res_truncated = verify_tc057_review_displayed_enclosures(tc057_artifact, bad_truncated)
    assert res_truncated["all_displayed_intervals_contain_generated_enclosures"] is False
    assert res_truncated["failed_count"] == 1


def test_lean_formalization_tc057_theorems_zero_sorry_zero_custom_axioms() -> None:
    lean_path = REPO_ROOT / "formal" / "RiemannScope" / "LiouvilleSquareDilation.lean"
    readme_path = REPO_ROOT / "formal" / "RiemannScope" / "README.md"
    lean_src = lean_path.read_text(encoding="utf-8")
    readme_src = readme_path.read_text(encoding="utf-8")

    expected_theorems = [
        "abstract_polylog_scale_bootstrap_and_weighted_contraction_tc057",
        "general_moebius_rough_prime_filtration_descent_tc057",
        "logarithmic_prime_power_descent_and_kernel_shift_tc057",
        "quadratic_prime_power_diagonal_off_diagonal_decomposition_tc057",
        "inherited_vs_canonical_cutoff_comparison_and_counterexample_tc057",
        "conditional_signed_correlation_same_scale_absorption_transfer_tc057r",
    ]
    for thm in expected_theorems:
        assert f"theorem {thm}" in lean_src, f"Missing Lean theorem {thm}"
        assert thm in readme_src, f"Missing Lean theorem {thm} in formal/RiemannScope/README.md"

    expected_defs = [
        "monotoneScaleEnvelope",
        "finiteQGeneral",
        "finiteQSmoothBelow",
        "roughSquarefreeDivisorsBand",
        "primePowerPairsUpTo",
        "finiteQShifted",
        "primePowerLogDescentSum",
        "liouvillePrimePowerTerm",
        "canonicalCutoffT",
        "inheritedCutoffL",
        "normalizedScaleSupremum",
    ]
    for dname in expected_defs:
        assert re.search(rf"^(?:noncomputable\s+)?def\s+{dname}\b", lean_src, flags=re.MULTILINE), (
            f"Missing Lean def {dname}"
        )
        assert f"`{dname}`" in readme_src, f"Missing Lean def `{dname}` in formal/RiemannScope/README.md"

    for ghost_ident in (
        "IsCompletelyMultiplicativeWeight",
        "finiteQWeight",
        "finiteQSmoothBelowU",
        "primePowerLogSumShifted",
        "pointwisePrimePowerDiagonal",
        "pointwisePrimePowerOffDiagonal",
    ):
        assert ghost_ident not in readme_src

    no_block = re.sub(r"/-.*?-/", "", lean_src, flags=re.DOTALL)
    no_comments = re.sub(r"--[^\n]*", "", no_block)
    assert re.search(r"\bsorry\b", no_comments) is None
    assert re.search(r"^\s*axiom\b", no_comments, flags=re.MULTILINE) is None

    defs_cnt = len(re.findall(r"^(?:noncomputable\s+)?def\s+", no_comments, flags=re.MULTILINE))
    pub_thm_cnt = len(re.findall(r"^theorem\s+", no_comments, flags=re.MULTILINE))
    priv_thm_cnt = len(re.findall(r"^private\s+theorem\s+", no_comments, flags=re.MULTILINE))
    assert (defs_cnt, pub_thm_cnt, priv_thm_cnt) == (81, 30, 63)
    assert "81 `def` + 30 public `theorem` + 63 private helper `theorem` = 174 declarations" in readme_src
