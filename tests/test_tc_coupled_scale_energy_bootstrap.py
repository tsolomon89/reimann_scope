"""Unit, certified-Arb, formal-scope, and adversarial tests for TASK-TC-057:
Arithmetic compatibility across scales and a coupled energy bootstrap.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re

from flint import arb, ctx as flint_ctx
import pytest

from tc.coupled_scale_energy_bootstrap import (
    COUPLED_SCALE_BOOTSTRAP_ARTIFACT_PATH,
    TASK_TC_057_ID,
    TC_057_REVIEW_DOC_PATH,
    evaluate_E_L_scale_arb,
    evaluate_Q_shifted_finite_arb,
    evaluate_Q_smooth_below_U_arb,
    exact_U0_T_pair_for_rational_Y,
    moebius_mu_int,
    prime_power_pairs_up_to,
    rough_squarefree_divisors_band,
    selberg_w2_weight_arb,
    verify_section_1_and_2_baseline_and_envelope,
    verify_section_3_route_a_moebius_rough_descent,
    verify_section_4_route_b_and_c_logarithmic_and_selberg,
    verify_tc057_review_displayed_enclosures,
)
from tc.liouville_square_dilation import (
    _parse_arb_ball_str_to_fractions,
    liouville_lambda_int,
)
from tc.prime_chain_contraction import (
    REPO_ROOT,
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
    assert tc057_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc057_artifact["rh_proved"] is False
    assert tc057_artifact["precision_bits"] == 256
    assert tc057_artifact["section_1_and_2_baseline_and_envelope"]["all_section_1_and_2_checks_pass"] is True
    assert tc057_artifact["section_3_route_a_moebius_rough_descent"]["all_section_3_checks_pass"] is True
    assert tc057_artifact["section_4_route_b_and_c_logarithmic_and_selberg"]["all_section_4_checks_pass"] is True
    assert tc057_artifact["section_5_cutoffs_small_scales_and_base_floor"]["all_section_5_checks_pass"] is True
    assert tc057_artifact["section_6_route_d_diagonal_contraction_and_off_diagonal"]["all_section_6_checks_pass"] is True

    arb_self = tc057_artifact["serialized_arb_self_check"]
    assert arb_self["all_enclose_original_256bit_arb_ball"] is True
    assert arb_self["live_original_count_matches_enumerated_total"] is True
    assert arb_self["total_certified_arb_balls_checked"] >= 250
    assert arb_self["failed_paths"] == []

    rev_audit = tc057_artifact["section_7_tc057_review_displayed_enclosures_audit"]
    assert rev_audit["all_displayed_intervals_contain_generated_enclosures"] is True
    assert rev_audit["untagged_count"] == 0
    assert rev_audit["failed_count"] == 0
    assert rev_audit["total_displayed_intervals_found"] >= 45


def test_exact_integer_power_small_Y_partition_and_type_safety() -> None:
    # 2^{8/5} = 4^{4/5} <-> 2^8 == 4^4 == 256
    assert (2 ** 8) == (4 ** 4) == 256
    # Exact 4-interval partition on [2, 4):
    # [2, 3^{4/5}] -> (4, 3), (3^{4/5}, 4^{4/5}] -> (4, 4),
    # (4^{4/5}, 5^{4/5}] -> (5, 5), (5^{4/5}, 4) -> (5, 6)
    assert exact_U0_T_pair_for_rational_Y(Fraction(2, 1)) == (4, 3)
    assert exact_U0_T_pair_for_rational_Y(Fraction(9, 4)) == (4, 3)
    assert exact_U0_T_pair_for_rational_Y(Fraction(5, 2)) == (4, 4)
    assert exact_U0_T_pair_for_rational_Y(Fraction(7, 2)) == (5, 5)
    assert exact_U0_T_pair_for_rational_Y(Fraction(15, 4)) == (5, 6)
    assert exact_U0_T_pair_for_rational_Y(Fraction(4, 1)) == (5, 6)

    # Reject floating-point and boolean inputs on exact cutoff functions
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


def test_envelope_boundedness_discontinuous_jump_and_conditional_bootstrap() -> None:
    res = verify_section_1_and_2_baseline_and_envelope(prec_bits=256)
    assert res["all_section_1_and_2_checks_pass"] is True

    env = res["monotone_envelope_local_boundedness"]
    assert env["jump_certified_nonzero"] is True
    assert _arb_lower_frac(env["jump_gap_abs"]) > Fraction(9, 100)
    assert _arb_lower_frac(env["envelope_upper_bound_margin_at_jump"]) > 0

    boot = res["conditional_bootstrap_and_penalty_barrier"]
    assert boot["scope_label"] == "CONDITIONAL_ON_RECURSION"
    assert _arb_lower_frac(boot["smaller_scale_monotonicity_factor_at_exp4"]) > Fraction(13, 100)
    # B_eta = 10 > 1 still contracts strictly below 1/2 at Y_* = exp(4096)
    assert _arb_upper_frac(boot["B_eta_10_contraction_factor"]) < Fraction(1, 2)
    # (log Y)^b penalty barrier: sigma = 1/4 < 1/2 fails (> 1), sigma = 3/4 > 1/2 contracts (< 1/2)
    assert _arb_lower_frac(boot["penalty_subcritical_sigma_quarter_at_exp100"]) > 1
    assert _arb_upper_frac(boot["penalty_supercritical_sigma_three_quarters_at_exp100"]) < Fraction(1, 2)


def test_route_a_moebius_rough_descent_and_a2_negative_control() -> None:
    # Sub-sqrt(T) band at U = 5, T = 431 includes 3-prime composite 385 = 5 * 7 * 11
    divs_5_431 = rough_squarefree_divisors_band(5, 431)
    assert 385 in divs_5_431
    assert all(moebius_mu_int(d) * liouville_lambda_int(d) == 1 for d in divs_5_431)

    # Super-sqrt(T) band at U = 42, T = 431 (42^2 = 1764 > 431) reduces to primes
    assert rough_squarefree_divisors_band(42, 431) == tuple(
        p for p in primes_up_to(431) if p >= 42
    )

    sec3 = verify_section_3_route_a_moebius_rough_descent(prec_bits=256)
    assert sec3["all_section_3_checks_pass"] is True
    assert sec3["a2_falsifies_uniform_liouville_sign"] is True
    assert _arb_lower_frac(sec3["a2_wrong_uniform_sign_discrepancy_U3_T15"]) > Fraction(7, 10)

    cs_rows = sec3["optimal_cauchy_schwarz_divergence_sigma_half"]
    m0 = _arb_lower_frac(cs_rows[0]["optimal_cs_homogeneous_multiplier"])
    m1 = _arb_lower_frac(cs_rows[1]["optimal_cs_homogeneous_multiplier"])
    m2 = _arb_lower_frac(cs_rows[2]["optimal_cs_homogeneous_multiplier"])
    assert 1 < m0 < _arb_upper_frac(cs_rows[0]["optimal_cs_homogeneous_multiplier"]) < m1
    assert _arb_upper_frac(cs_rows[1]["optimal_cs_homogeneous_multiplier"]) < m2


def test_route_b_and_c_identities_factorial_growth_and_selberg_cancellation() -> None:
    # Explicit T = 0 and T = 1 edge checks
    assert prime_power_pairs_up_to(0) == ()
    assert prime_power_pairs_up_to(1) == ()
    assert evaluate_Q_shifted_finite_arb(4, L=0, m_shift=0, mode="liouville") == arb(0)
    assert evaluate_Q_smooth_below_U_arb(4, U=2, T=0, mode="liouville") == arb(0)

    sec4 = verify_section_4_route_b_and_c_logarithmic_and_selberg(prec_bits=256)
    assert sec4["all_section_4_checks_pass"] is True
    assert sec4["a2_falsifies_liouville_neg1_k_formula"] is True
    assert sec4["shift_hierarchy_Y128_T431"]["telescope_verified"] is True

    # M_1^{[0]} matches M_1, and M_1^{[6]} > M_1^{[3]} > M_1^{[0]}
    gtab = sec4["kernel_shift_factorial_growth_table"]
    u0 = _arb_lower_frac(gtab[0]["M_1_shifted_upper"])
    u3 = _arb_lower_frac(gtab[3]["M_1_shifted_upper"])
    u6 = _arb_lower_frac(gtab[6]["M_1_shifted_upper"])
    assert u0 < _arb_upper_frac(gtab[0]["M_1_shifted_upper"]) < u3
    assert _arb_upper_frac(gtab[3]["M_1_shifted_upper"]) < u6

    # Route C Selberg double-pole cancellation vs a_2 logarithmic divergence
    rc = sec4["route_c_selberg_second_order"]
    assert _arb_upper_frac(rc["c_sel_lambda_residue_4_zetap2_over_zeta2_minus_2_gamma"]) < Fraction(-343, 100)
    assert _arb_upper_frac(rc["sum_w2_lambda_over_u"]) < -2
    assert _arb_lower_frac(rc["sum_w2_a2_over_u_log_u"]) > 1

    # Direct spot check of w_{2,lambda}(6): 6 = 2*3 is not a prime power, so w_{2,lambda}(6) = 2*(-log 2)*(-log 3) = +2 log 2 log 3
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        diff_w2_6 = selberg_w2_weight_arb(6, "liouville") - arb(2) * arb(2).log() * arb(3).log()
        assert arb(0) in diff_w2_6 and abs(diff_w2_6) < arb("1e-70")
    finally:
        flint_ctx.prec = saved


def test_section_5_cutoff_counterexample_small_scale_positivity_and_base_floor(
    tc057_artifact: dict,
) -> None:
    sec5 = tc057_artifact["section_5_cutoffs_small_scales_and_base_floor"]
    cx = sec5["counterexample_Y_9_4_d_2"]
    assert cx["T_Y"] == 3 and cx["L_2"] == 1 and cx["T_W"] == 2
    assert cx["L_2"] < cx["T_W"]
    assert _arb_lower_frac(cx["Q1_minus_Q2_at_9_8"]) > Fraction(12, 100)
    assert _arb_lower_frac(cx["abs_E1_minus_E2"]) > Fraction(9, 1000)

    # Live Arb check of E_1(9/8) != E_2(9/8)
    e1 = evaluate_E_L_scale_arb(Fraction(9, 8), L=1, mode="liouville", prec_bits=256)
    e2 = evaluate_E_L_scale_arb(Fraction(9, 8), L=2, mode="liouville", prec_bits=256)
    assert bool(e1 - e2 > arb("8e-3"))

    # Sharp small-scale positivity constant > 4/25 > 1/24
    sm = sec5["small_scale_positivity"]
    assert _arb_lower_frac(sm["c_small_sharp_1_plus_exp_neg1_minus_zeta3"]) > Fraction(4, 25)
    assert _arb_lower_frac(sm["outward_margin"]) > 0

    # Certified all-L >= 1 base-scale energy floor on W in [1, 2]
    bf = sec5["base_scale_energy_floor_W_in_1_2"]
    assert _arb_lower_frac(bf["m_all_L_rigorous_floor"]) > Fraction(8, 10000)
    assert _arb_lower_frac(bf["tail_energy_lower_bound_L_gt_20"]) > Fraction(5, 100)


def test_route_d_unconditional_diagonal_contraction_and_X_tilde_sign_split(
    tc057_artifact: dict,
) -> None:
    sec6 = tc057_artifact["section_6_route_d_diagonal_contraction_and_off_diagonal"]
    assert sec6["pair_by_pair_off_diagonal_check_Y8"]["consistency_verified"] is True
    assert sec6["sign_split_liouville_neg_vs_controls_pos"] is True

    sweep = {row["Y"]: row for row in sec6["liouville_route_d_scale_sweep"]}
    for y_val, row in sweep.items():
        assert _arb_lower_frac(row["margin_D_pp_minus_D_tilde"]) > 0, f"D_tilde <= D_pp failed at Y={y_val}"
        assert _arb_lower_frac(row["margin_rhs_minus_D_pp"]) > 0, f"D_pp <= RHS failed at Y={y_val}"

    # Liouville X_tilde oscillates around 0 (< 0 at {8, 32, 128}, > 0 at {16, 64})
    assert _arb_upper_frac(sweep[8]["X_tilde_off_diagonal"]) < 0
    assert _arb_lower_frac(sweep[16]["X_tilde_off_diagonal"]) > 0
    assert _arb_upper_frac(sweep[32]["X_tilde_off_diagonal"]) < 0
    assert _arb_lower_frac(sweep[64]["X_tilde_off_diagonal"]) > 0
    assert _arb_upper_frac(sweep[128]["X_tilde_off_diagonal"]) < 0

    # Parity controls grow coherently positive
    ctrls = {row["label"]: row for row in sec6["parity_control_sign_split"]}
    assert _arb_lower_frac(ctrls["a2_Y32"]["X_tilde"]) > Fraction(1, 2)
    assert _arb_lower_frac(ctrls["a2_Y128"]["X_tilde"]) > Fraction(39, 10)
    assert _arb_lower_frac(ctrls["a_3_5_7_Y32"]["X_tilde"]) > Fraction(4, 10)
    assert _arb_lower_frac(ctrls["unsigned_1_Y32"]["X_tilde"]) > Fraction(44, 10)

    # All-epsilon diagonal contraction below 1/2 at thresholds
    for row in sec6["all_epsilon_diagonal_contraction_table"]:
        assert _arb_lower_frac(row["margin_below_half_at_threshold"]) > 0


def test_review_doc_tau_only_convention_and_adversarial_enclosure_audit(
    tc057_artifact: dict, tmp_path: Path
) -> None:
    text = TC_057_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    # Strict tau-only convention: zero \pi macros in TC_057 review
    assert re.search(r"\\pi\b", text) is None, "Found forbidden \\pi macro in TC_057 review"
    assert "z = a + i b" in text
    assert "CONDITIONAL_ON_RECURSION" in text

    live_audit = verify_tc057_review_displayed_enclosures(tc057_artifact, TC_057_REVIEW_DOC_PATH)
    assert live_audit["all_displayed_intervals_contain_generated_enclosures"] is True
    assert live_audit["untagged_count"] == 0
    assert live_audit["failed_count"] == 0

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
    ]
    for thm in expected_theorems:
        assert f"theorem {thm}" in lean_src, f"Missing Lean theorem {thm}"
        assert thm in readme_src, f"Missing Lean theorem {thm} in formal/RiemannScope/README.md"

    # Strip comments before checking for sorry / axiom declarations
    no_block = re.sub(r"/-.*?-/", "", lean_src, flags=re.DOTALL)
    no_comments = re.sub(r"--[^\n]*", "", no_block)
    assert re.search(r"\bsorry\b", no_comments) is None
    assert re.search(r"^\s*axiom\b", no_comments, flags=re.MULTILINE) is None

    defs_cnt = len(re.findall(r"^(?:noncomputable\s+)?def\s+", no_comments, flags=re.MULTILINE))
    pub_thm_cnt = len(re.findall(r"^theorem\s+", no_comments, flags=re.MULTILINE))
    priv_thm_cnt = len(re.findall(r"^private\s+theorem\s+", no_comments, flags=re.MULTILINE))
    assert (defs_cnt, pub_thm_cnt, priv_thm_cnt) == (60, 25, 54)
    assert "60 `def` + 25 public `theorem` + 54 private helper `theorem` = 139 declarations" in readme_src
