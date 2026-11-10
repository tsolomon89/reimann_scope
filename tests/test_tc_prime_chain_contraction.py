"""
Unit, certification, edge-case, and negative-control tests for TASK-TC-056:
Prime-chain contraction, uniform total contraction bound, falsification controls,
and signed mixed-prime block energy analysis (`tc/prime_chain_contraction.py`,
`data/tc_prime_chain_contraction.json`, `docs/reviews/TC_056_PRIME_CHAIN_CONTRACTION.md`,
and `formal/RiemannScope/LiouvilleSquareDilation.lean`).
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re

from flint import arb, ctx as flint_ctx
import pytest

from tc.canonical_theta_correlation_bound import (
    REPO_ROOT,
    verify_all_serialized_arb_in_tree,
)
from tc.liouville_square_dilation import (
    TC_054R2_MERGED_MAIN_BASELINE,
    TC_055R2_IMPLEMENTATION_COMMIT,
    TC_055R2_REVIEWED_TIP,
    _parse_arb_ball_str_to_fractions,
    finite_prime_parity_aS_int,
    liouville_lambda_int,
    two_adic_parity_a2_int,
)
from tc.prime_chain_contraction import (
    PRIME_CHAIN_CONTRACTION_ARTIFACT_PATH,
    TC_056_REVIEW_DOC_PATH,
    TC_056R_REVIEWED_COMMIT,
    KernelMatrixCacheArb,
    compute_prime_reciprocal_cube_minus_one_sum_arb,
    evaluate_C_P_p_chain_quadrature_arb,
    evaluate_C_p_alternating_shift_arb,
    evaluate_D_T_diagonal_arb,
    evaluate_Delta_P_p_cross_fibers_arb,
    evaluate_E_T_signed_arb,
    evaluate_F_P_r_pointwise_arb,
    evaluate_F_adjoin_erroneous_uncoupled_cutoff_arb,
    evaluate_M_P_p_chain_quadrature_arb,
    evaluate_M_P_p_erroneous_extra_factor_two_arb,
    evaluate_M_P_p_ordered_k_ne_l_arb,
    evaluate_V_P_erroneous_omitted_cofactor_weight_arb,
    evaluate_V_P_independent_fiber_quadrature_arb,
    evaluate_V_P_kernel_grouping_arb,
    evaluate_finite_unimodal_alternating_chain_arb,
    evaluate_low_prime_alpha_half_euler_product_arb,
    evaluate_phi_n_arb,
    evaluate_smooth_cutoff_surge_I_kappa_arb,
    evaluate_unsigned_euler_product_P_eta_arb,
    exact_M_companion_cutoff,
    exact_T_cutoff_ceil_Y_5_4,
    exact_U0_cutoff_ceil_2_Y_5_8,
    primes_up_to,
    validate_adjoin_prime,
    validate_prime_set_tuple,
    verify_section_6_uniform_total_contraction_bound,
    verify_tc056_review_displayed_enclosures,
)

LEAN_FILE_PATH = REPO_ROOT / "formal" / "RiemannScope" / "LiouvilleSquareDilation.lean"


@pytest.fixture(scope="module")
def tc056_artifact() -> dict:
    assert PRIME_CHAIN_CONTRACTION_ARTIFACT_PATH.exists(), (
        f"Missing artifact {PRIME_CHAIN_CONTRACTION_ARTIFACT_PATH}"
    )
    return json.loads(PRIME_CHAIN_CONTRACTION_ARTIFACT_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. Artifact Provenance, Gate Status, Circle Constant, & Review Enclosures
# ---------------------------------------------------------------------------


def test_tc056_artifact_provenance_and_serialized_arb_balls(tc056_artifact: dict) -> None:
    assert tc056_artifact["task_id"] == "TASK-TC-056"
    assert tc056_artifact["parent_epic"] == "EPIC-TC-042"
    assert tc056_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc056_artifact["rh_proved"] is False
    assert tc056_artifact["precision_bits"] == 256
    assert tc056_artifact["tc054r2_merged_main_baseline"] == TC_054R2_MERGED_MAIN_BASELINE
    assert tc056_artifact["tc055r2_implementation_commit"] == TC_055R2_IMPLEMENTATION_COMMIT
    assert tc056_artifact["tc055r2_reviewed_tip"] == TC_055R2_REVIEWED_TIP

    assert tc056_artifact["section_1_and_2_baseline_and_cleanup"]["all_section_1_and_2_checks_pass"] is True
    assert tc056_artifact["section_3_finite_prime_filtration"]["all_section_3_checks_pass"] is True
    assert tc056_artifact["section_4_single_prime_gaussian_contraction"]["all_section_4_checks_pass"] is True
    assert tc056_artifact["section_5_contraction_vs_mixed_and_p_independence"]["all_section_5_checks_pass"] is True
    assert tc056_artifact["section_6_uniform_total_contraction_bound"]["all_section_6_checks_pass"] is True
    assert tc056_artifact["section_7_falsification_and_parity_controls"]["all_section_7_checks_pass"] is True
    assert tc056_artifact["section_8_mixed_prime_block_attempt"]["all_section_8_checks_pass"] is True

    arb_self = tc056_artifact["serialized_arb_self_check"]
    assert arb_self["total_certified_arb_balls_checked"] >= 200
    assert arb_self["live_original_count_matches_enumerated_total"] is True
    assert arb_self["all_enclose_original_256bit_arb_ball"] is True

    live_sec6_arb = verify_all_serialized_arb_in_tree(verify_section_6_uniform_total_contraction_bound())
    assert live_sec6_arb["total_certified_arb_balls_checked"] >= 10
    assert live_sec6_arb["all_enclose_original_256bit_arb_ball"] is True


def test_tc056_review_doc_sole_tau_notation_and_generator_enclosures(tc056_artifact: dict) -> None:
    assert TC_056_REVIEW_DOC_PATH.exists()
    review_text = TC_056_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    # Sole circle constant tau: no \pi macro anywhere in the review document
    assert re.findall(r"\\pi\b", review_text) == []
    # Semantic guard: V_P is explicitly distinguished from orthogonal projection / martingale
    assert "never** called or treated as an orthogonal projection" in review_text

    live_audit = verify_tc056_review_displayed_enclosures(tc056_artifact, TC_056_REVIEW_DOC_PATH)
    assert live_audit["total_displayed_intervals_found"] >= 45
    assert live_audit["untagged_count"] == 0
    assert live_audit["failed_count"] == 0
    assert live_audit["all_displayed_intervals_contain_generated_enclosures"] is True

    embedded = tc056_artifact["section_9_tc056_review_displayed_enclosures_audit"]
    assert embedded["all_displayed_intervals_contain_generated_enclosures"] is True
    assert embedded["total_displayed_intervals_found"] == live_audit["total_displayed_intervals_found"]


# ---------------------------------------------------------------------------
# 2. Exact Schedule Cutoffs, Prime-Set Validation, and Section 2 Cleanups
# ---------------------------------------------------------------------------


def test_exact_T_vs_M_cutoffs_and_binary_float_rejection() -> None:
    eps = Fraction(1, 1 << 100)
    assert exact_T_cutoff_ceil_Y_5_4(1) == 1
    assert exact_M_companion_cutoff(1) == 2
    assert exact_T_cutoff_ceil_Y_5_4(Fraction(1, 1) + eps) == 2
    assert exact_M_companion_cutoff(Fraction(1, 1) + eps) == 2

    # Exact fourth-power transitions at Y = 16 (16^{5/4} = 32) and Y = 81 (81^{5/4} = 243):
    assert exact_T_cutoff_ceil_Y_5_4(Fraction(16, 1) - eps) == 32
    assert exact_T_cutoff_ceil_Y_5_4(16) == 32
    assert exact_T_cutoff_ceil_Y_5_4(Fraction(16, 1) + eps) == 33
    assert exact_T_cutoff_ceil_Y_5_4(Fraction(81, 1) - eps) == 243
    assert exact_T_cutoff_ceil_Y_5_4(81) == 243
    assert exact_T_cutoff_ceil_Y_5_4(Fraction(81, 1) + eps) == 244
    assert exact_T_cutoff_ceil_Y_5_4(128) == 431

    with pytest.raises(TypeError):
        exact_T_cutoff_ceil_Y_5_4(16.0)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        exact_T_cutoff_ceil_Y_5_4(True)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        exact_T_cutoff_ceil_Y_5_4(Fraction(99, 100))
    with pytest.raises(TypeError):
        evaluate_phi_n_arb(4.0, 2)  # type: ignore[arg-type]


def test_prime_set_and_adjoin_prime_validation() -> None:
    assert validate_prime_set_tuple(()) == ()
    assert validate_prime_set_tuple([5, 2, 3]) == (2, 3, 5)
    assert validate_adjoin_prime((5, 2), 3) == ((2, 5), (2, 3, 5))

    for bad_p in (0, 1, 4, 6, 9, -3):
        with pytest.raises(ValueError):
            validate_prime_set_tuple((2, bad_p))
        with pytest.raises(ValueError):
            validate_adjoin_prime((2, 3), bad_p)

    # Duplicate prime in P or adjoining an already-present prime must fail:
    with pytest.raises(ValueError):
        validate_prime_set_tuple((2, 3, 2))
    with pytest.raises(ValueError):
        validate_adjoin_prime((2, 3, 5), 3)
    with pytest.raises(TypeError):
        validate_prime_set_tuple((True,))  # type: ignore[arg-type]


def test_section_2_uncoupled_excess_w6_and_polylog_scale() -> None:
    # At P = {2}, T = 3, uncoupled excess is identically w(6):
    # Test an arbitrary weight w(n) with w(1)=7, w(2)=-11, w(3)=13, w(6)=w6:
    for w6_val in (0, 19, -5):
        weights = {1: 7, 2: -11, 3: 13, 6: w6_val}
        coupled = sum(liouville_lambda_int(n) * weights[n] for n in (1, 2, 3))
        uncoupled = sum(
            liouville_lambda_int(m) * liouville_lambda_int(r) * weights[m * r]
            for m in (1, 2)
            for r in (1, 3)
        )
        assert uncoupled - coupled == w6_val

    # Three-regime analysis of P_eta(u) = prod_{p <= u} (1 - p^{-1/2-eta})^{-2} (beta = 1/2 - eta):
    # - Regime A (0 < eta < 1/2, concrete case eta = 1/4, alpha = 3/4, beta = 1/4):
    #   For u(Y) = c * (log Y * log log Y)^{1/beta} = c * (log Y * log log Y)^4 at eps = 1/4:
    #   c_adm = (1/16)^4 = 1/65536 (2 * c^{1/4} = 1/8 < eps) is admissible, whereas
    #   c_inc = (1/4)^4 = 1/256 (2 * c^{1/4} = 1/2 > eps) violates 2 * u^beta / (beta * log u) <= eps * log Y:
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        logY = arb(1000)
        beta = arb(1) / arb(4)
        eps = arb(1) / arb(4)
        u_adm = (arb(1) / arb(65536)) * ((logY * logY.log()) ** arb(4))
        u_inc = (arb(1) / arb(256)) * ((logY * logY.log()) ** arb(4))
        ratio_adm = (arb(2) * (u_adm ** beta)) / (beta * u_adm.log() * logY)
        ratio_inc = (arb(2) * (u_inc ** beta)) / (beta * u_inc.log() * logY)
        assert bool((eps - ratio_adm).lower() > 0)
        assert bool((ratio_inc - eps).lower() > 0)

        regA_1000 = evaluate_unsigned_euler_product_P_eta_arb(Fraction(1, 4), 1000, prec_bits=256)
        assert regA_1000["regime"] == "REGIME_A_SUBCRITICAL_0_LT_ETA_LT_1_OVER_2"
        assert bool(regA_1000["higher_power_tail"].lower() > 0)

        # - Regime B (eta = 1/2, alpha = 1, beta = 0): squared Mertens product P_{1/2}(u) ~ e^{2*gamma_E} (log u)^2:
        regB_1000 = evaluate_unsigned_euler_product_P_eta_arb(Fraction(1, 2), 1000, prec_bits=256)
        assert regB_1000["regime"] == "REGIME_B_CRITICAL_MERTENS_ETA_EQ_1_OVER_2"
        assert bool((regB_1000["ratio_to_mertens_asymptotic"] - arb(9) / arb(10)).lower() > 0)
        assert bool((arb(11) / arb(10) - regB_1000["ratio_to_mertens_asymptotic"]).lower() > 0)

        # - Regime C (1/2 < eta < 1, concrete case eta = 3/4, alpha = 5/4): convergent to zeta(5/4)^2:
        regC_1000 = evaluate_unsigned_euler_product_P_eta_arb(Fraction(3, 4), 1000, prec_bits=256)
        regC_10000 = evaluate_unsigned_euler_product_P_eta_arb(Fraction(3, 4), 10000, prec_bits=256)
        assert regC_1000["regime"] == "REGIME_C_SUPERCRITICAL_CONVERGENT_1_OVER_2_LT_ETA_LT_1"
        assert bool((regC_10000["P_eta"] - regC_1000["P_eta"]).lower() > 0)
        assert bool(regC_1000["gap_below_zeta_limit"].lower() > 0)
        assert bool(regC_10000["gap_below_zeta_limit"].lower() > 0)
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 3. Edge Cases (T=0, T=1, p>T, P=empty), Filtration, Contraction & P-Indep.
# ---------------------------------------------------------------------------


def test_filtration_edge_cases_T0_T1_p_gt_T_and_prime_boundaries() -> None:
    # T = 0:
    assert evaluate_V_P_kernel_grouping_arb(4, 0, ()) == arb(0)
    assert evaluate_V_P_independent_fiber_quadrature_arb(4, 0, (2, 3)) == arb(0)
    assert evaluate_D_T_diagonal_arb(4, 0) == arb(0)
    assert evaluate_E_T_signed_arb(4, 0) == arb(0)
    assert evaluate_Delta_P_p_cross_fibers_arb(4, 0, (2,), 3) == arb(0)
    assert evaluate_C_p_alternating_shift_arb(4, 0, 2) == arb(0)
    assert evaluate_M_P_p_ordered_k_ne_l_arb(4, 0, (2,), 3) == arb(0)

    # T = 1 at Y = 1:
    kc1 = KernelMatrixCacheArb(1, prec_bits=256)
    d1 = evaluate_D_T_diagonal_arb(1, 1, kernel_cache=kc1)
    e1 = evaluate_E_T_signed_arb(1, 1, kernel_cache=kc1)
    v1_empty = evaluate_V_P_kernel_grouping_arb(1, 1, (), kernel_cache=kc1)
    v1_p2 = evaluate_V_P_kernel_grouping_arb(1, 1, (2,), kernel_cache=kc1)
    assert (d1 - e1).contains(0)
    assert (v1_empty - d1).contains(0)
    assert (v1_p2 - e1).contains(0)
    assert evaluate_Delta_P_p_cross_fibers_arb(1, 1, (), 2, kernel_cache=kc1) == arb(0)

    # p > T at Y = 4, T = 5 (prime boundary T = 5; adjoining p = 7 > 5):
    kc4 = KernelMatrixCacheArb(4, prec_bits=256)
    v_23_t5 = evaluate_V_P_kernel_grouping_arb(4, 5, (2, 3), kernel_cache=kc4)
    v_237_t5 = evaluate_V_P_kernel_grouping_arb(4, 5, (2, 3, 7), kernel_cache=kc4)
    assert (v_237_t5 - v_23_t5).contains(0)
    assert evaluate_Delta_P_p_cross_fibers_arb(4, 5, (2, 3), 7, kernel_cache=kc4) == arb(0)
    assert evaluate_C_p_alternating_shift_arb(4, 5, 7, kernel_cache=kc4) == arb(0)
    assert evaluate_M_P_p_ordered_k_ne_l_arb(4, 5, (2, 3), 7, kernel_cache=kc4) == arb(0)

    # Exact prime boundary T = 5 vs T = 6: adjoining p = 5 changes V at T = 5!
    d_p5_t5 = evaluate_Delta_P_p_cross_fibers_arb(4, 5, (2, 3), 5, kernel_cache=kc4)
    e_t5 = evaluate_E_T_signed_arb(4, 5, kernel_cache=kc4)
    assert (v_23_t5 + d_p5_t5 - e_t5).contains(0)
    assert not d_p5_t5.contains(0)


def test_unimodal_chain_edge_cases_and_non_unimodal_counterexample() -> None:
    # Empty, singleton, ties, and trailing zeros satisfy |A| <= max a_k and A^2 <= sum a_k^2:
    for seq in (
        [],
        [arb(7)],
        [arb(2), arb(5), arb(5), arb(3), arb(0), arb(0)],
        [arb(0), arb(4), arb(4), arb(1)],
    ):
        res = evaluate_finite_unimodal_alternating_chain_arb(seq)
        assert res["sup_bound_holds"] is True
        assert res["sq_contraction_holds"] is True

    # Negative control: non-unimodal nonnegative sequence [1, 3, 1, 3] has A = -4, |A| = 4 > max = 3!
    bad = evaluate_finite_unimodal_alternating_chain_arb([arb(1), arb(3), arb(1), arb(3)])
    assert bad["sup_bound_holds"] is False
    assert bool(bad["sup_margin_max_minus_abs_A"].upper() < 0)

    # Negative control: thick intervals whose midpoint violates contraction ([1+-0.4, 3+-0.4, 1+-0.4, 3+-0.4])
    # and negative entries must fail closed (.lower() >= 0):
    thick_ambig = evaluate_finite_unimodal_alternating_chain_arb(
        [arb("1 +/- 0.4"), arb("3 +/- 0.4"), arb("1 +/- 0.4"), arb("3 +/- 0.4")]
    )
    assert thick_ambig["sup_bound_holds"] is False
    neg_entry = evaluate_finite_unimodal_alternating_chain_arb([arb(-1), arb(2)])
    assert neg_entry["all_terms_certified_nonnegative"] is False
    assert neg_entry["sup_bound_holds"] is False
    assert neg_entry["sq_contraction_holds"] is False


def test_p_independence_of_C_P_p_and_mixed_decomposition() -> None:
    Y_val, T_val, p_val = 5, 10, 3
    kc = KernelMatrixCacheArb(Y_val, prec_bits=256)
    c_shift = evaluate_C_p_alternating_shift_arb(Y_val, T_val, p_val, kernel_cache=kc)
    c_diff = evaluate_D_T_diagonal_arb(Y_val, T_val, kernel_cache=kc) - evaluate_V_P_kernel_grouping_arb(
        Y_val, T_val, (p_val,), kernel_cache=kc
    )
    assert bool(c_shift.lower() > 0)
    assert (c_shift - c_diff).contains(0)

    for P_set in ((), (2,), (5,), (2, 5), (2, 5, 7)):
        c_chain = evaluate_C_P_p_chain_quadrature_arb(Y_val, T_val, P_set, p_val)
        assert (c_chain - c_shift).contains(0)

        m_chain = evaluate_M_P_p_chain_quadrature_arb(Y_val, T_val, P_set, p_val)
        m_knel = evaluate_M_P_p_ordered_k_ne_l_arb(Y_val, T_val, P_set, p_val, kernel_cache=kc)
        delta_step = evaluate_Delta_P_p_cross_fibers_arb(Y_val, T_val, P_set, p_val, kernel_cache=kc)
        assert (m_chain - m_knel).contains(0)
        assert (delta_step - (m_knel - c_shift)).contains(0)


# ---------------------------------------------------------------------------
# 4. Uniform Contraction Bound, Falsification Controls 7a/7b/7c, & Section 8
# ---------------------------------------------------------------------------


def test_shifted_diagonal_change_of_variable_and_uniform_contraction_cap(tc056_artifact: dict) -> None:
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # Direct verification of K_Y(n, n*d) = d^{-3} c_d^{-5} K_{c_d Y}(n, n):
        Y_val = arb(3)
        for n_int, d_int in ((1, 2), (2, 3), (3, 5)):
            d_arb = arb(d_int)
            c_d = ((arb(1) + d_arb ** (-2)) / arb(2)).sqrt()
            lhs = KernelMatrixCacheArb(Y_val, prec_bits=256).get(n_int, n_int * d_int)
            rhs = (d_arb ** (-3)) * (c_d ** (-5)) * KernelMatrixCacheArb(c_d * Y_val, prec_bits=256).get(n_int, n_int)
            assert (lhs - rhs).contains(0)

        p_sum = compute_prime_reciprocal_cube_minus_one_sum_arb(prec_bits=256)
        assert p_sum["prime_sum_1_over_p3_minus_1"].overlaps(p_sum["direct_prime_sum_cross_check"])
        assert bool(
            (p_sum["elementary_upper_8_over_7_times_zeta3_minus_1"] - p_sum["prime_sum_1_over_p3_minus_1"]).lower() > 0
        )

        sec6 = tc056_artifact["section_6_uniform_total_contraction_bound"]
        margin_low, _, _ = _parse_arb_ball_str_to_fractions(
            sec6["one_minus_elementary_cap_margin"]["arb_ball_str"]
        )
        assert margin_low > Fraction(19, 1000)
    finally:
        flint_ctx.prec = saved


def test_falsification_controls_7a_7b_and_parity_controls_7c(tc056_artifact: dict) -> None:
    sec7 = tc056_artifact["section_7_falsification_and_parity_controls"]
    # 7a: Delta_{{2},3}(4, 6) strictly positive outward lower endpoint:
    low_7a, _, _ = _parse_arb_ball_str_to_fractions(
        sec7["control_7a_stepwise_positivity_witness_Y4_T6_P2_p3"]["Delta_P2_p3"]["arb_ball_str"]
    )
    assert low_7a > Fraction(77, 10000)

    # 7b: [sum_{64 <= p < 128} Delta_p(128, 431)] / D_{431}(128) > 1 outward lower endpoint:
    low_7b, _, _ = _parse_arb_ball_str_to_fractions(
        sec7["control_7b_dyadic_block_surge_Y128_T431_block_64_to_128"]["ratio_sum_Delta_over_D_431"]["arb_ball_str"]
    )
    assert low_7b > Fraction(134, 100)

    # 7c: Live check that a_S contracts at singleton {p} iff p in S:
    kc = KernelMatrixCacheArb(6, prec_bits=256)
    d_8 = evaluate_D_T_diagonal_arb(6, 8, kernel_cache=kc)
    a35_fn = lambda n: finite_prime_parity_aS_int(n, primes_S=(3, 5))
    v_p2_a2 = evaluate_V_P_kernel_grouping_arb(6, 8, (2,), weight_fn=two_adic_parity_a2_int, kernel_cache=kc)
    v_p3_a2 = evaluate_V_P_kernel_grouping_arb(6, 8, (3,), weight_fn=two_adic_parity_a2_int, kernel_cache=kc)
    v_p2_a35 = evaluate_V_P_kernel_grouping_arb(6, 8, (2,), weight_fn=a35_fn, kernel_cache=kc)
    v_p3_a35 = evaluate_V_P_kernel_grouping_arb(6, 8, (3,), weight_fn=a35_fn, kernel_cache=kc)
    assert bool((d_8 - v_p2_a2).lower() > 0)
    assert bool((v_p3_a2 - d_8).lower() > 0)
    assert bool((v_p2_a35 - d_8).lower() > 0)
    assert bool((d_8 - v_p3_a35).lower() > 0)


def test_section_8_super_sqrt_T_identity_and_smooth_cutoff_surge() -> None:
    # Live super-sqrt(T) check at Y = 16, T = T(16) = 32 (sqrt(32) = 5.656..., so B = 8 > sqrt(T)):
    Y_val, T_val, B_val = 16, 32, 8
    P_lt_8 = primes_up_to(7)
    P_lt_16 = primes_up_to(15)
    block_primes = [p for p in P_lt_16 if p >= 8]  # [11, 13]
    kc = KernelMatrixCacheArb(Y_val, prec_bits=256)

    lhs = evaluate_V_P_kernel_grouping_arb(Y_val, T_val, P_lt_16, kernel_cache=kc) - evaluate_V_P_kernel_grouping_arb(
        Y_val, T_val, P_lt_8, kernel_cache=kc
    )
    # Compute ||S_{<16, 32}||^2 - ||S_{<8, 32}||^2 - sum_{p in {11, 13}} (1/p) E_{floor(32/p)}(16/p):
    s8_sq = evaluate_V_P_independent_fiber_quadrature_arb(Y_val, T_val, P_lt_8) - sum(
        (
            evaluate_E_T_signed_arb(Fraction(Y_val, p), T_val // p) / arb(p)
            for p in primes_up_to(T_val)
            if p >= 8
        ),
        arb(0),
    )
    s16_sq = evaluate_V_P_independent_fiber_quadrature_arb(Y_val, T_val, P_lt_16) - sum(
        (
            evaluate_E_T_signed_arb(Fraction(Y_val, p), T_val // p) / arb(p)
            for p in primes_up_to(T_val)
            if p >= 16
        ),
        arb(0),
    )
    diag_band = sum(
        (evaluate_E_T_signed_arb(Fraction(Y_val, p), T_val // p) / arb(p) for p in block_primes),
        arb(0),
    )
    assert (lhs - ((s16_sq - s8_sq) - diag_band)).contains(0)

    # Live surge check with N0 = 600 terms: I(2) - I(1) > 0.118 > 0:
    i1 = evaluate_smooth_cutoff_surge_I_kappa_arb(Fraction(1, 1), N0_terms=600, prec_bits=256)["I_kappa"]
    i2 = evaluate_smooth_cutoff_surge_I_kappa_arb(Fraction(2, 1), N0_terms=600, prec_bits=256)["I_kappa"]
    assert bool(((i2 - i1) - arb("0.118")).lower() > 0)


# ---------------------------------------------------------------------------
# 5. Mandatory Negative Controls (Missing Weight, Extra Factor 2, Common Cutoff, Review Tags)
# ---------------------------------------------------------------------------


def test_negative_controls_missing_weight_extra_factor_two_and_uncoupled_cutoff() -> None:
    Y_val, T_val = 4, 6
    kc = KernelMatrixCacheArb(Y_val, prec_bits=256)

    # (a) Missing 1/r cofactor weight in V_P strictly disagrees with V_P and breaks contraction!
    v_true = evaluate_V_P_kernel_grouping_arb(Y_val, T_val, (2,), kernel_cache=kc)
    v_bad_weight = evaluate_V_P_erroneous_omitted_cofactor_weight_arb(Y_val, T_val, (2,))
    d_true = evaluate_D_T_diagonal_arb(Y_val, T_val, kernel_cache=kc)
    assert not (v_bad_weight - v_true).contains(0)
    assert bool((v_bad_weight - d_true).lower() > 0)  # falsely appears to expand instead of contracting!

    # (b) Extra factor of 2 on ordered m != n in M_{P,p} breaks Delta_{P,p} = M_{P,p} - C_p:
    delta_2_3 = evaluate_Delta_P_p_cross_fibers_arb(Y_val, T_val, (2,), 3, kernel_cache=kc)
    c_3 = evaluate_C_p_alternating_shift_arb(Y_val, T_val, 3, kernel_cache=kc)
    m_true = evaluate_M_P_p_ordered_k_ne_l_arb(Y_val, T_val, (2,), 3, kernel_cache=kc)
    m_bad_factor2 = evaluate_M_P_p_erroneous_extra_factor_two_arb(Y_val, T_val, (2,), 3, kernel_cache=kc)
    assert (delta_2_3 - (m_true - c_3)).contains(0)
    assert not (delta_2_3 - (m_bad_factor2 - c_3)).contains(0)
    assert bool(abs(delta_2_3 - (m_bad_factor2 - c_3)).lower() > arb("0.009"))

    # (c) Illicit uncoupled cutoff on F_{P union {p}, s}(X) disagrees with actual coupled fiber
    #     by the out-of-range term m = 4 <= 6, p^1 = 3 <= 6 -> m*p = 12 > 6:
    f_coupled = evaluate_F_P_r_pointwise_arb(4, (2, 3), T_int=6, r_int=1)
    f_uncoupled = evaluate_F_adjoin_erroneous_uncoupled_cutoff_arb(4, (2,), 3, T_int=6, s_int=1)
    expected_excess_12 = arb(liouville_lambda_int(12)) * evaluate_phi_n_arb(4, 12)
    assert ((f_uncoupled - f_coupled) - expected_excess_12).contains(0)
    assert not (f_coupled - f_uncoupled).contains(0)
    assert bool(abs(f_coupled - f_uncoupled).lower() > arb("0.015"))


def test_negative_controls_review_interval_verifier_catches_tampering(
    tc056_artifact: dict, tmp_path: Path
) -> None:
    valid_line = (
        r"$$\Delta_{\{2\}, 3}(4, 6) \in [0.007708594152727606280552027802897859033100 \pm 2.00 \times 10^{-43}]$$ "
        '<!-- tc-enclosure: observable="Delta_P2_p3" params="Y=4; T=6; adjoined_prime_p=3" '
        'json_path="section_7_falsification_and_parity_controls.control_7a_stepwise_positivity_witness_Y4_T6_P2_p3.Delta_P2_p3" -->\n'
    )
    p_ok = tmp_path / "ok.md"
    p_ok.write_text(valid_line, encoding="utf-8")
    assert verify_tc056_review_displayed_enclosures(tc056_artifact, p_ok)[
        "all_displayed_intervals_contain_generated_enclosures"
    ] is True

    # 1. Untagged interval:
    p_untagged = tmp_path / "untagged.md"
    p_untagged.write_text(r"$[0.00770859 \pm 1.00 \times 10^{-6}]$" + "\n", encoding="utf-8")
    res_untagged = verify_tc056_review_displayed_enclosures(tc056_artifact, p_untagged)
    assert res_untagged["untagged_count"] == 1
    assert res_untagged["all_displayed_intervals_contain_generated_enclosures"] is False

    # 2. Drifted midpoint:
    p_drift = tmp_path / "drift.md"
    p_drift.write_text(valid_line.replace("0.007708594", "0.008708594"), encoding="utf-8")
    res_drift = verify_tc056_review_displayed_enclosures(tc056_artifact, p_drift)
    assert res_drift["failed_count"] == 1
    assert res_drift["all_displayed_intervals_contain_generated_enclosures"] is False

    # 3. Overly narrow radius (smaller than generated 1.92e-43 radius):
    p_narrow = tmp_path / "narrow.md"
    p_narrow.write_text(valid_line.replace("2.00 \\times 10^{-43}", "1.00 \\times 10^{-44}"), encoding="utf-8")
    res_narrow = verify_tc056_review_displayed_enclosures(tc056_artifact, p_narrow)
    assert res_narrow["failed_count"] == 1
    assert res_narrow["all_displayed_intervals_contain_generated_enclosures"] is False

    # 4. Wrong parameter binding:
    p_param = tmp_path / "param.md"
    p_param.write_text(valid_line.replace("Y=4; T=6", "Y=4; T=999"), encoding="utf-8")
    res_param = verify_tc056_review_displayed_enclosures(tc056_artifact, p_param)
    assert res_param["failed_count"] == 1
    assert res_param["all_displayed_intervals_contain_generated_enclosures"] is False

    # 5. Wrong observable identifier:
    p_obs = tmp_path / "obs.md"
    p_obs.write_text(valid_line.replace('observable="Delta_P2_p3"', 'observable="wrong_metric"'), encoding="utf-8")
    res_obs = verify_tc056_review_displayed_enclosures(tc056_artifact, p_obs)
    assert res_obs["failed_count"] == 1
    assert res_obs["all_displayed_intervals_contain_generated_enclosures"] is False

    # 6. Bloated/vacuous radius (fails radius_is_tight and/or strict sign preservation):
    p_bloat = tmp_path / "bloat.md"
    p_bloat.write_text(valid_line.replace("2.00 \\times 10^{-43}", "1.00 \\times 10^{-10}"), encoding="utf-8")
    res_bloat = verify_tc056_review_displayed_enclosures(tc056_artifact, p_bloat)
    assert res_bloat["failed_count"] == 1
    assert res_bloat["all_displayed_intervals_contain_generated_enclosures"] is False


# ---------------------------------------------------------------------------
# 6. Formal Lean 4 Theorem Signatures & Zero-Sorry / Zero-Axiom Verification
# ---------------------------------------------------------------------------


def test_lean_tc056_theorems_present_and_zero_sorry_or_axiom() -> None:
    lean_src = LEAN_FILE_PATH.read_text(encoding="utf-8")
    # Strip comments before scanning for sorry/admit/axiom:
    no_block = re.sub(r"/-.*?-/", "", lean_src, flags=re.DOTALL)
    code_only = re.sub(r"--[^\n]*", "", no_block)

    assert re.findall(r"\bsorry\b", code_only) == []
    assert re.findall(r"\badmit\b", code_only) == []
    assert re.findall(r"\baxiom\b", code_only) == []

    expected_theorems = (
        "finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056",
        "finite_alternating_unimodal_chain_contraction_tc056",
        "gaussian_prime_chain_unimodal_and_singleton_contraction_tc056",
        "mixed_interaction_decomposition_and_p_independence_tc056",
    )
    for thm_name in expected_theorems:
        assert f"theorem {thm_name}" in code_only, f"Missing Lean theorem {thm_name}"


# ---------------------------------------------------------------------------
# 7. TASK-TC-056R Regression Tests (Grade Scope, U0 Cutoff, Theorem 8.E, Claims)
# ---------------------------------------------------------------------------


def test_tc056r_rational_vs_algebraic_grade_scope_and_no_overclaim(tc056_artifact: dict) -> None:
    review_text = TC_056_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    # The unsupported algebraic-grade overclaim must not appear in the review document:
    assert "cannot solve $p^k = \\tau^K$ by Lindemann" not in review_text
    assert "cannot solve $p^k = \\tau^K$ by Lindemann\u2013Weierstrass / Gelfond\u2013Schneider" not in review_text
    assert "irrational" in review_text
    assert "does **not** determine whether $K = \\frac{k \\log p}{\\log \\tau}$ is algebraic irrational" in review_text

    grade_audit = tc056_artifact["section_1_and_2_baseline_and_cleanup"][
        "rational_vs_algebraic_grade_scope_audit"
    ]
    assert grade_audit["verified"] is True
    assert "PROVED_IRRATIONAL_BY_LINDEMANN" in grade_audit["rational_exclusion_status"]
    assert "OPEN_UNESTABLISHED" in grade_audit["algebraic_irrational_vs_transcendental_status"]
    assert grade_audit["any_tc056_theorem_depends_on_algebraic_grade_exclusion"] is False

    polylog_audit = tc056_artifact["section_1_and_2_baseline_and_cleanup"][
        "admissible_polylogarithmic_scale_correction"
    ]
    assert polylog_audit["unsigned_majorant_budget_scope_only"] is True
    assert "P_eta(u)" in polylog_audit["product_definition"]


def test_tc056r_exact_U0_cutoff_boundaries_and_empty_prime_bands(tc056_artifact: dict) -> None:
    eps = Fraction(1, 1 << 100)
    assert exact_U0_cutoff_ceil_2_Y_5_8(1) == 2
    assert exact_U0_cutoff_ceil_2_Y_5_8(Fraction(1, 1) + eps) == 3
    assert exact_U0_cutoff_ceil_2_Y_5_8(2) == 4
    # Exact eighth-power boundary at Y = 256 = 2^8 -> 2 * 256^{5/8} = 2 * 32 = 64:
    assert exact_U0_cutoff_ceil_2_Y_5_8(Fraction(256, 1) - eps) == 64
    assert exact_U0_cutoff_ceil_2_Y_5_8(256) == 64
    assert exact_U0_cutoff_ceil_2_Y_5_8(Fraction(256, 1) + eps) == 65
    assert exact_U0_cutoff_ceil_2_Y_5_8(128) == 42

    for Y_sample in (1, 2, 4, 6, 16, 81, 128, 256):
        u0_val = exact_U0_cutoff_ceil_2_Y_5_8(Y_sample)
        t_val = exact_T_cutoff_ceil_Y_5_4(Y_sample)
        assert u0_val * u0_val > t_val

    # Empty prime bands at Y = 1 (U0 = 2, T = 1) and Y = 2 (U0 = 4, T = 3):
    assert [p for p in primes_up_to(exact_T_cutoff_ceil_Y_5_4(1)) if p >= exact_U0_cutoff_ceil_2_Y_5_8(1)] == []
    assert [p for p in primes_up_to(exact_T_cutoff_ceil_Y_5_4(2)) if p >= exact_U0_cutoff_ceil_2_Y_5_8(2)] == []

    with pytest.raises(TypeError):
        exact_U0_cutoff_ceil_2_Y_5_8(4.0)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        exact_U0_cutoff_ceil_2_Y_5_8(False)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        exact_U0_cutoff_ceil_2_Y_5_8(Fraction(99, 100))

    sched = tc056_artifact["section_1_and_2_baseline_and_cleanup"]["schedule_T_vs_M_boundary_audit"]
    assert sched["all_boundary_checks_pass"] is True


def test_tc056r_theorem_8E_mellin_sign_step_B_truncation_and_claim_separation(
    tc056_artifact: dict,
) -> None:
    sec8 = tc056_artifact["section_8_mixed_prime_block_attempt"]
    thm_8c = sec8["theorem_8C_refutation_of_localized_single_block_subpower_conjecture"]
    thm_8e = sec8["theorem_8E_conditional_moving_cutoff_buchstab_asymptotic"]

    # Unconditional vs conditional separation:
    assert thm_8c["requires_rh"] is False
    assert "does NOT use RH" in thm_8c["contradiction_vs_unconditional_block_asymptotic_scope"]
    assert thm_8e["is_conditional_on_rh"] is True
    assert thm_8e["verified"] is True
    assert thm_8e["F_at_half_exact_zero"] == 0

    # Outward-rounded endpoint checks on Mellin derivative, log moment, norm coefficient, and Step F cap:
    fp_low, _, _ = _parse_arb_ball_str_to_fractions(
        thm_8e["F_prime_at_half_tau2_over_48"]["arb_ball_str"]
    )
    _, lm_high, _ = _parse_arb_ball_str_to_fractions(
        thm_8e["log_moment_int_Q_lambda_w_neg_3_2_log_w"]["arb_ball_str"]
    )
    nc_low, _, _ = _parse_arb_ball_str_to_fractions(
        thm_8e["norm_sq_leading_coeff_tau_minus_1_tau4_over_2304"]["arb_ball_str"]
    )
    sf_low, _, _ = _parse_arb_ball_str_to_fractions(
        thm_8e["step_F_Q_T_tail_cap_tau_5_2_over_2"]["arb_ball_str"]
    )
    assert fp_low > Fraction(8224, 10000)
    assert lm_high < Fraction(-8224, 10000)
    assert nc_low > Fraction(3573, 1000)
    assert sf_low > Fraction(4947, 100)

    # Claim classification check:
    claims = tc056_artifact["five_category_claim_classification"]
    assert any("Theorem 8.C" in item for item in claims["2_analytic_theorems_proved_outside_lean"])
    assert any("Theorem 8.E" in item for item in claims["5_conditional_and_open_statements"])


# ---------------------------------------------------------------------------
# 8. TASK-TC-056R2 Regression Tests (3-Regime P_eta, Low-Prime alpha=1/2,
#    Unsupported Probe Removal, and Small-Y Cutoff Ordering Domain)
# ---------------------------------------------------------------------------


def test_tc056r2_three_regime_P_eta_and_low_prime_alpha_half_distinction(
    tc056_artifact: dict,
) -> None:
    assert tc056_artifact["repair_task_id"] == "TASK-TC-056R2"
    assert tc056_artifact["tc056r_reviewed_commit"] == TC_056R_REVIEWED_COMMIT

    polylog_audit = tc056_artifact["section_1_and_2_baseline_and_cleanup"][
        "admissible_polylogarithmic_scale_correction"
    ]
    assert polylog_audit["verified"] is True
    assert (
        polylog_audit["regime_A_subcritical_0_lt_eta_lt_half"]["regression_eta_quarter_u1000"]["verified"]
        is True
    )
    assert (
        polylog_audit["regime_B_critical_eta_eq_half"]["regression_eta_half_u1000"]["verified"]
        is True
    )
    assert (
        polylog_audit["regime_C_supercritical_half_lt_eta_lt_1"]["regression_eta_three_quarters"]["verified"]
        is True
    )

    # Verify invalid eta outside (0, 1) and u < 0 raise ValueError:
    with pytest.raises(ValueError):
        evaluate_unsigned_euler_product_P_eta_arb(0, 100)
    with pytest.raises(ValueError):
        evaluate_unsigned_euler_product_P_eta_arb(1, 100)
    with pytest.raises(ValueError):
        evaluate_unsigned_euler_product_P_eta_arb(Fraction(1, 4), -1)

    # Distinct alpha = 1/2 (eta = 0) low-prime bound in Theorem 8.B(1):
    thm_8b = tc056_artifact["section_8_mixed_prime_block_attempt"][
        "theorem_8B_unconditional_low_and_top_block_bounds"
    ]
    assert thm_8b["low_prime_abs_sum_samples_verified"] is True
    abs_sum_low, _, _ = _parse_arb_ball_str_to_fractions(
        thm_8b["sample_partial_block_Y8_T14_U5_abs_sum_Mp"]["arb_ball_str"]
    )
    _, cap_high, _ = _parse_arb_ball_str_to_fractions(
        thm_8b["sample_partial_block_Y8_T14_U5_analytic_cap"]["arb_ball_str"]
    )
    assert abs_sum_low > Fraction(218, 10000)
    assert cap_high > abs_sum_low

    prod_5 = evaluate_low_prime_alpha_half_euler_product_arb(5, prec_bits=256)
    assert bool((prod_5 - arb(1)).lower() > 0)


def test_tc056r2_unsupported_reciprocal_zeta_probe_removed_and_small_Y_domain(
    tc056_artifact: dict,
) -> None:
    py_src = (REPO_ROOT / "tc" / "prime_chain_contraction.py").read_text(encoding="utf-8")
    json_src = PRIME_CHAIN_CONTRACTION_ARTIFACT_PATH.read_text(encoding="utf-8")
    review_src = TC_056_REVIEW_DOC_PATH.read_text(encoding="utf-8")

    for forbidden_token in ("z_probe", "inv_s_minus_1_zeta_ball", "G_at_half_probe"):
        assert forbidden_token not in py_src
        assert forbidden_token not in json_src
        assert forbidden_token not in review_src

    thm_8e = tc056_artifact["section_8_mixed_prime_block_attempt"][
        "theorem_8E_conditional_moving_cutoff_buchstab_asymptotic"
    ]
    assert thm_8e["closed_form_constant_consistency_check_only"] is True
    assert "closed-form constants" in thm_8e["finite_sample_check_scope"]
    assert "O(1 / log Y)" in thm_8e["steps_A_through_F_proof_summary"]["step_D_moving_endpoints_and_log_expansion"]

    # Small-Y cutoff ordering:
    # - At Y in {1, 2, 3}: U_0(Y) >= T(Y) and [U_0(Y), T(Y)] cap P = empty;
    # - For all tested Y >= 4: 5 <= U_0(Y) <= T(Y) - 1 < T(Y) with non-empty [U_0(Y), T(Y)] cap P:
    assert (exact_U0_cutoff_ceil_2_Y_5_8(1), exact_T_cutoff_ceil_Y_5_4(1)) == (2, 1)
    assert (exact_U0_cutoff_ceil_2_Y_5_8(2), exact_T_cutoff_ceil_Y_5_4(2)) == (4, 3)
    assert (exact_U0_cutoff_ceil_2_Y_5_8(3), exact_T_cutoff_ceil_Y_5_4(3)) == (4, 4)
    for y_small in (1, 2, 3):
        u0_s = exact_U0_cutoff_ceil_2_Y_5_8(y_small)
        t_s = exact_T_cutoff_ceil_Y_5_4(y_small)
        assert u0_s >= t_s
        assert [p for p in primes_up_to(t_s) if p >= u0_s] == []

    eps = Fraction(1, 1 << 100)
    for y_ge_4 in (
        4,
        Fraction(4, 1) + eps,
        Fraction(21, 5),
        Fraction(22, 5),
        5,
        16,
        128,
    ):
        u0_val = exact_U0_cutoff_ceil_2_Y_5_8(y_ge_4)
        t_val = exact_T_cutoff_ceil_Y_5_4(y_ge_4)
        assert 5 <= u0_val <= t_val - 1 < t_val
        assert len([p for p in primes_up_to(t_val) if p >= u0_val]) >= 1



