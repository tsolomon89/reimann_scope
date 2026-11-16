"""Focused regression and falsification test suite for TASK-TC-061:
Preregistered Mixed Arithmetic Covariance Test and Signed-Kernel Proof Attempt
toward SUBGATE-TC-043A (EPIC-TC-042).

Crucial test-design discipline (Prompt Section 4):
- Validates exact margin classification (`PASS`, valid counterexample `FAIL`, zero-straddling
  `UNRESOLVED`, `NOT_EVALUATED`, and explicit `exact_algebraic_zero_proved=True`), global probe
  outcome aggregation (`REFUTED_BY_CERTIFIED_WITNESS`, `SURVIVED_TESTED_POINTS`,
  `UNRESOLVED/INCOMPLETE_COVERAGE`, `PROVED_UNIFORMLY`), and positive-denominator ratio guards.
- Does NOT require the conjectured Liouville inequalities to be true merely for software tests to
  pass: holdout tests re-parse the exact outward-rounded Arb endpoints of every recorded margin
  and verify that the recorded `point_verdict` and `global_probe_outcome` faithfully match those
  endpoints without ever claiming `PROVED_UNIFORMLY` from finite grid survival.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re
from typing import Any, Dict, List

from flint import arb, ctx as flint_ctx
import pytest

from tc.canonical_theta_correlation_bound import (
    REPO_ROOT,
    serialize_arb_certified,
    verify_all_serialized_arb_in_tree,
)
from tc.dyadic_power_lift_primitive_correlation import EPISTEMIC_CATEGORIES, PARENT_SUBGATE_ID
from tc.liouville_square_dilation import (
    _parse_arb_ball_str_to_fractions,
    _sci_or_latex_num_to_fraction,
)
from tc.mixed_arithmetic_covariance import (
    ACCEPTED_TC060R2_IMPLEMENTATION,
    ACCEPTED_TC060R2_TIP,
    EXPECTED_TC061_THEOREMS,
    FROZEN_PROTOCOL_ID,
    FROZEN_PROTOCOL_REGISTRATION_COMMIT,
    FROZEN_PROTOCOL_SHA256,
    MERGED_MAIN_BASELINE_TC061,
    MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH,
    MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH,
    POINT_MARGIN_VERDICTS,
    PROBE_GLOBAL_OUTCOMES,
    PROPOSED_TC061_BRANCH,
    PROPOSED_TC061R_BRANCH,
    REVIEWED_TC061_IMPLEMENTATION,
    REVIEWED_TC061_TIP,
    TASK_TC_061_ID,
    TASK_TC_061R_ID,
    TC_061_LEAN_MODULE_PATH,
    TC_061_REVIEW_DOC_PATH,
    ExactScaleSpec,
    calibrate_secondary_a_eta_exact,
    certified_ratio_with_positive_denominator,
    certify_exact_scale_cutoffs,
    classify_global_probe_outcome,
    classify_probe_margin_arb,
    compute_complete_core_s_Y_and_beta_Y_arb,
    compute_finite_prime_control_invariants,
    compute_selberg_centered_remainder_table_fast_arb,
    evaluate_divisor_sum_aS_direct,
    evaluate_finite_prime_parity_convolution_formula,
    evaluate_interval_via_cutoff_case_split_arb,
    evaluate_mixed_covariance_point_arb,
    evaluate_window_gram_G_Y_r_arb,
    execute_holdout_point_with_protocol_escalation,
    load_frozen_protocol_rules,
    resolve_protocol_quadrature_settings,
    verify_coarse_halfline_complement_bound_arb,
    verify_frozen_protocol_immutability,
    verify_self_collision_elementary_majorant_proof_arb,
    verify_tc061_lean_theorems_live,
    verify_tc061_review_displayed_enclosures,
)
from tc.signed_dilation_arithmetic_energy import (
    REVIEWED_TC060R_IMPLEMENTATION,
    SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH,
    AmbiguousCutoffError,
    certify_D0_small_divisor_cutoff,
    certify_T_canonical_cutoff,
    verify_section_epistemic_scope_metadata,
)


@pytest.fixture(scope="module")
def tc061_artifact() -> Dict[str, Any]:
    assert MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH.exists(), (
        f"Missing {MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH}; run python tc/mixed_arithmetic_covariance.py"
    )
    return json.loads(MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH.read_text(encoding="utf-8"))


def test_tc061_artifact_provenance_epistemic_scope_and_preserved_tc060r2(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify top-level provenance, open subgate status, component-scoped epistemic labels,
    tau-only / K-grade notation hygiene, serialized Arb self-check, and TC-060R2 preservation.
    """
    assert tc061_artifact["task_id"] == TASK_TC_061_ID
    assert tc061_artifact["repair_task_id"] == TASK_TC_061R_ID
    assert tc061_artifact["parent_subgate"] == PARENT_SUBGATE_ID
    assert tc061_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc061_artifact["rh_proved"] is False
    assert tc061_artifact["hypothesis_H_status"] == "OPEN_CONJECTURE_OR_FAILED_CANDIDATE"
    assert tc061_artifact["merged_main_baseline"] == MERGED_MAIN_BASELINE_TC061
    assert tc061_artifact["accepted_tc060r2_tip"] == ACCEPTED_TC060R2_TIP
    assert tc061_artifact["accepted_tc060r2_implementation"] == ACCEPTED_TC060R2_IMPLEMENTATION
    assert tc061_artifact["inherited_tc060r_formal_commit"] == REVIEWED_TC060R_IMPLEMENTATION
    assert tc061_artifact["reviewed_tc061_tip"] == REVIEWED_TC061_TIP
    assert tc061_artifact["reviewed_tc061_implementation"] == REVIEWED_TC061_IMPLEMENTATION
    assert tc061_artifact["branch"] == PROPOSED_TC061R_BRANCH
    assert tc061_artifact["original_tc061_branch"] == PROPOSED_TC061_BRANCH
    assert tc061_artifact["epistemic_categories_enforced"] == list(EPISTEMIC_CATEGORIES)
    assert tc061_artifact["probe_global_outcomes_enforced"] == list(PROBE_GLOBAL_OUTCOMES)

    for sec_key in (
        "section_1_protocol_and_exact_mixed_identity",
        "section_2_cutoff_and_interval_certification",
        "section_3_preregistered_holdout_experiment",
        "section_4_controls_and_tc_arithmetic_attribution",
        "section_5_arithmetic_proof_attempt_and_kernel_reduction",
        "section_6_route_d_conditional_transfer_and_scope",
    ):
        sec_obj = tc061_artifact[sec_key]
        ok_ep, msg_ep = verify_section_epistemic_scope_metadata(sec_obj)
        assert ok_ep is True, f"{sec_key} failed epistemic scope check: {msg_ep}"
        assert "epistemic_status" not in sec_obj, f"Blanket epistemic_status forbidden on {sec_key}"

    arb_chk = tc061_artifact["serialized_arb_self_check"]
    assert arb_chk["all_enclose_original_256bit_arb_ball"] is True
    assert arb_chk["total_certified_arb_balls_checked"] >= 1000

    # Verify zero circle-half tokens and zero non-grade K_* identifiers across TC-061 deliverables:
    checked_paths = [
        REPO_ROOT / "tc" / "mixed_arithmetic_covariance.py",
        MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH,
        MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH,
        TC_061_LEAN_MODULE_PATH,
    ]
    if TC_061_REVIEW_DOC_PATH.exists():
        checked_paths.append(TC_061_REVIEW_DOC_PATH)
    for p in checked_paths:
        txt = p.read_text(encoding="utf-8")
        pi_cnt = len(re.findall(r"\x5cpi(?![a-zA-Z])", txt)) + txt.count("\u03c0")
        assert pi_cnt == 0, f"Found {pi_cnt} forbidden circle-half tokens in {p}"

    code_and_doc_paths = [
        REPO_ROOT / "tc" / "mixed_arithmetic_covariance.py",
        TC_061_LEAN_MODULE_PATH,
    ]
    if TC_061_REVIEW_DOC_PATH.exists():
        code_and_doc_paths.append(TC_061_REVIEW_DOC_PATH)
    for code_path in code_and_doc_paths:
        code_txt = code_path.read_text(encoding="utf-8")
        k_matches = set(re.findall(r"\bK_[A-Za-z0-9_]+\b", code_txt))
        assert k_matches == set(), f"Forbidden non-grade K_* identifiers in {code_path}: {k_matches}"

    # Verify inherited TC-060R2 certificate remains intact:
    tc060_art = json.loads(SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert tc060_art["subgate_tc043a_status"] == "OPEN"
    assert tc060_art["rh_proved"] is False
    assert (
        tc060_art["section_6_lean_formalization_audit"]["formal_build_report_provenance"][
            "producing_git_commit"
        ]
        == REVIEWED_TC060R_IMPLEMENTATION
    )
    assert tc060_art["serialized_arb_self_check"]["total_certified_arb_balls_checked"] == 398


def test_tc061_frozen_protocol_immutability_and_adversarial_tamper_rejection(
    tmp_path: Path,
) -> None:
    """Verify SHA-256 and git registration-commit immutability of the preregistered protocol,
    and verify fail-closed rejection when any calibrated constant or threshold is tampered with.
    """
    chk = verify_frozen_protocol_immutability()
    assert chk["verified"] is True
    assert chk["protocol_id"] == FROZEN_PROTOCOL_ID
    assert chk["computed_protocol_sha256"] == FROZEN_PROTOCOL_SHA256
    assert chk["recorded_protocol_sha256"] == FROZEN_PROTOCOL_SHA256
    assert chk["registration_commit"] == FROZEN_PROTOCOL_REGISTRATION_COMMIT
    assert chk["git_blob_matches_registration_commit"] is True
    assert chk["registration_commit_is_ancestor_of_head"] is True

    # Adversarial tamper test 1: inflate calibrated a_{1/2} numerator from 2/64 (1/32) to 3/64:
    proto_tampered = json.loads(MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH.read_text(encoding="utf-8"))
    proto_tampered["frozen_candidate_probes"][1]["a_numerator"] = 99
    tampered_path = tmp_path / "tampered_protocol.json"
    tampered_path.write_text(
        json.dumps(proto_tampered, indent=2, sort_keys=False, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    chk_bad = verify_frozen_protocol_immutability(tampered_path)
    assert chk_bad["sha256_verified"] is False
    assert chk_bad["verified"] is False


def test_tc061_exact_rational_ceiling_calibration_and_diagnostic_separation(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify exact rational ceiling calibration `a_eta = ceil(64 * U_eta) / 64` (zero floats),
    negative-quotient clamping to 0, strict separation of diagnostic `{2, 4, 8}`, and exact
    agreement on `C = {16, 32, 64}` (`a_{1/2} = 1/32, a_{1/4} = 3/64, a_{1/8} = 5/64`).
    """
    # Negative quotients clamp U_eta to 0 => a_eta = 0:
    cal_neg = calibrate_secondary_a_eta_exact([arb(-3), arb("-0.001")])
    assert cal_neg["U_eta_fraction"] == Fraction(0, 1)
    assert cal_neg["ceil_64_U_eta"] == 0
    assert cal_neg["a_eta_fraction"] == Fraction(0, 1)

    # Exact dyadic boundary 3/64 stays 3/64; adding 2^{-100} rounds strictly UP to 4/64 = 1/16:
    exact_3_64 = arb(3) / arb(64)
    cal_exact = calibrate_secondary_a_eta_exact([exact_3_64])
    assert cal_exact["ceil_64_U_eta"] == 3
    assert cal_exact["a_eta_fraction"] == Fraction(3, 64)

    tiny_above = exact_3_64 + (arb(2) ** (-100))
    cal_up = calibrate_secondary_a_eta_exact([tiny_above])
    assert cal_up["ceil_64_U_eta"] == 4
    assert cal_up["a_eta_fraction"] == Fraction(1, 16)

    with pytest.raises(ValueError, match="Non-finite"):
        calibrate_secondary_a_eta_exact([arb("nan")])

    sec1 = tc061_artifact["section_1_protocol_and_exact_mixed_identity"]
    cal_rev = sec1["exact_rational_calibration_reverification"]
    assert cal_rev["1/2"]["matches_frozen_protocol"] is True
    assert cal_rev["1/2"]["a_eta_fraction"] == "1/32"
    assert cal_rev["1/4"]["matches_frozen_protocol"] is True
    assert cal_rev["1/4"]["a_eta_fraction"] == "3/64"
    assert cal_rev["1/8"]["matches_frozen_protocol"] is True
    assert cal_rev["1/8"]["a_eta_fraction"] == "5/64"

    rows_le_64 = {int(r["Y"]): r for r in sec1["diagnostic_and_calibration_evaluations"]}
    for y_diag in (2, 4, 8):
        assert rows_le_64[y_diag]["role"] == "DIAGNOSTIC_OUTSIDE_DECLARED_DOMAIN"
        for pdata in rows_le_64[y_diag]["probe_evaluations"].values():
            assert pdata["in_declared_domain"] is False
    for y_cal in (16, 32, 64):
        assert rows_le_64[y_cal]["role"] == "CALIBRATION_SET_C_NOT_HOLDOUT_EVIDENCE"
        for pid in ("TC061-P_1_2", "TC061-P_1_4", "TC061-P_1_8"):
            assert rows_le_64[y_cal]["probe_evaluations"][pid]["point_verdict"] == "PASS"
    assert rows_le_64[16]["probe_evaluations"]["TC061-P0"]["in_declared_domain"] is False
    assert rows_le_64[32]["probe_evaluations"]["TC061-P0"]["in_declared_domain"] is False
    assert rows_le_64[64]["probe_evaluations"]["TC061-P0"]["in_declared_domain"] is True


def test_tc061_margin_and_global_classifiers_pass_fail_unresolved_and_exact_zero() -> None:
    """Validate strict classification of `PASS`, valid counterexample `FAIL`, zero-straddling
    `UNRESOLVED`, non-finite `UNRESOLVED`, `exact_algebraic_zero_proved`, all 4 global outcomes,
    and positive-denominator ratio guards.
    """
    # 1. Pointwise margin classifier:
    c_pass = classify_probe_margin_arb(arb("-0.125"))
    assert c_pass["verdict"] == "PASS" and c_pass["certified_definite"] is True

    c_exact_zero = classify_probe_margin_arb(arb(0))
    assert c_exact_zero["verdict"] == "PASS" and c_exact_zero["certified_definite"] is True

    # Outward mag_t inflation in arb_union pushes upper([-1, 0]) to +2^{-30} > 0 => UNRESOLVED:
    c_union_zero = classify_probe_margin_arb(arb(-1).union(arb(0)))
    assert c_union_zero["verdict"] == "UNRESOLVED" and c_union_zero["certified_definite"] is False

    c_fail = classify_probe_margin_arb(arb("0.0625"))
    assert c_fail["verdict"] == "FAIL" and c_fail["certified_definite"] is True

    c_straddle = classify_probe_margin_arb(arb(0, arb("1e-30")))
    assert c_straddle["verdict"] == "UNRESOLVED" and c_straddle["certified_definite"] is False

    c_nan = classify_probe_margin_arb(arb("nan"))
    assert c_nan["verdict"] == "UNRESOLVED" and c_nan["certified_definite"] is False

    # Explicit algebraic zero equality certification path:
    c_alg_ok = classify_probe_margin_arb(arb(0, arb("1e-50")), exact_algebraic_zero_proved=True)
    assert c_alg_ok["verdict"] == "PASS"
    assert "EXACT_ALGEBRAIC_ZERO" in c_alg_ok["reason"]

    with pytest.raises(ValueError):
        classify_probe_margin_arb(arb("-0.5"), exact_algebraic_zero_proved=True)
    with pytest.raises(ValueError):
        classify_probe_margin_arb(arb("0.5"), exact_algebraic_zero_proved=True)
    with pytest.raises(ValueError):
        classify_probe_margin_arb(arb("1e-5", arb("1e-10")), exact_algebraic_zero_proved=True)

    # 2. Global probe outcome aggregator across all 4 mandatory outcomes:
    assert (
        classify_global_probe_outcome(["PASS", "FAIL", "PASS"], coverage_complete=True)
        == "REFUTED_BY_CERTIFIED_WITNESS"
    )
    assert (
        classify_global_probe_outcome(["PASS", "UNRESOLVED"], coverage_complete=True)
        == "UNRESOLVED/INCOMPLETE_COVERAGE"
    )
    assert (
        classify_global_probe_outcome(["PASS", "NOT_EVALUATED"], coverage_complete=True)
        == "UNRESOLVED/INCOMPLETE_COVERAGE"
    )
    assert (
        classify_global_probe_outcome(["PASS", "PASS"], coverage_complete=False)
        == "UNRESOLVED/INCOMPLETE_COVERAGE"
    )
    assert (
        classify_global_probe_outcome(["PASS", "PASS"], coverage_complete=True, uniform_proof_established=False)
        == "SURVIVED_TESTED_POINTS"
    )
    assert (
        classify_global_probe_outcome(["PASS", "PASS"], coverage_complete=True, uniform_proof_established=True)
        == "PROVED_UNIFORMLY"
    )
    with pytest.raises(ValueError):
        classify_global_probe_outcome(["INVALID_STATUS"], coverage_complete=True)

    # 3. Positive-denominator ratio guard:
    r_pos = certified_ratio_with_positive_denominator(arb(-3), arb(4))
    assert r_pos["denominator_certified_positive"] is True
    assert r_pos["ratio"] is not None

    for bad_den in (arb(0), arb(-2), arb(0, arb("1e-20")), arb("nan")):
        r_bad = certified_ratio_with_positive_denominator(arb(1), bad_den)
        assert r_bad["denominator_certified_positive"] is False
        assert r_bad["ratio"] is None


def test_tc061_mixed_identity_theta_inequality_dtilde_authenticity_and_sign_flips(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify exact reconstruction `4*D_tilde + J = ||2*P_Y - B_Y||_Y^2 = ||Q_Y + A_Y||_Y^2`,
    theta-inequality, strict separation of inherited `D_tilde(Y)` from coefficient diagonal
    `D_coeff(Y)`, and certified sign changes of `<P_Y, B_Y>_Y`.
    """
    sec1 = tc061_artifact["section_1_protocol_and_exact_mixed_identity"]
    assert sec1["all_section_1_checks_pass"] is True
    assert sec1["pair_P_B_sign_change_verified"] is True

    rows = {int(r["Y"]): r for r in sec1["diagnostic_and_calibration_evaluations"]}
    for y_pos in (2, 8, 32):
        assert rows[y_pos]["pair_P_B_sign"] == "STRICTLY_POSITIVE"
    for y_neg in (4, 16, 64):
        assert rows[y_neg]["pair_P_B_sign"] == "STRICTLY_NEGATIVE"

    # Live check at Y = 16 that D_tilde(16) is the inherited prime-power diagonal (NOT D_coeff(16)):
    tbl = compute_selberg_centered_remainder_table_fast_arb(64, prec_bits=288)
    sp16 = ExactScaleSpec(label="16", kind="exact_rational", rational_factor=Fraction(16, 1))
    res16 = evaluate_mixed_covariance_point_arb(
        sp16, prec_bits=256, quad_tol_bits=240, use_three_zone=False, selberg_table=tbl
    )
    assert bool(arb(0) in res16["J_consistency_residual_QA"])
    assert bool(abs(res16["J_consistency_residual_QA"]) < arb("1e-68"))
    assert bool(arb(0) in res16["J_consistency_residual_2PB"])
    assert bool(abs(res16["J_consistency_residual_2PB"]) < arb("1e-68"))
    # D_tilde(16) ~ 0.029693 whereas D_coeff(16) ~ 0.05398:
    assert bool(res16["D_tilde_Y"] < arb("0.035"))
    assert bool(res16["D_tilde_Y"] > arb("0.025"))


def test_tc061_cutoff_discontinuities_straddling_rejection_and_interval_case_splits(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify exact sided cutoffs across `e^5` and `256`, `AmbiguousCutoffError` on unsplit
    straddling balls, float endpoint rejection, and rigorous branch-splitting interval evaluation.
    """
    sec2 = tc061_artifact["section_2_cutoff_and_interval_certification"]
    assert sec2["all_section_2_checks_pass"] is True

    sc = sec2["sided_discontinuity_cutoffs"]
    assert sc["e5_minus"]["D0_raw"] == 4 and sc["e5_minus"]["T_Y"] == 518
    assert sc["e5_plus"]["D0_raw"] == 5 and sc["e5_plus"]["T_Y"] == 519
    assert sc["256_minus"]["T_Y"] == 1024 and sc["256_minus"]["D0_raw"] == 5
    assert sc["256_exact"]["T_Y"] == 1024 and sc["256_exact"]["D0_raw"] == 5
    assert sc["256_plus"]["T_Y"] == 1025 and sc["256_plus"]["D0_raw"] == 5

    # Unsplit straddling enclosures must raise AmbiguousCutoffError:
    with pytest.raises(AmbiguousCutoffError):
        certify_T_canonical_cutoff(arb(256, arb(2) ** (-20)))
    with pytest.raises(AmbiguousCutoffError):
        certify_D0_small_divisor_cutoff(arb(5).exp() + arb(0, arb(2) ** (-20)), kappa=1)

    # Float endpoints must raise TypeError in interval case-split evaluator:
    with pytest.raises(TypeError, match="Float endpoints are forbidden"):
        evaluate_interval_via_cutoff_case_split_arb(255.99, 256.01)  # type: ignore[arg-type]

    cs = sec2["straddling_interval_case_splits"]
    assert cs["interval_256_pm_2_neg12"]["active_branch_count"] == 2
    assert cs["interval_256_pm_2_neg12"]["P0_interval_classification"]["verdict"] == "PASS"
    assert cs["interval_148_40_to_148_45_across_e5_and_T518"]["active_branch_count"] == 3
    assert (
        cs["interval_148_40_to_148_45_across_e5_and_T518"]["P0_interval_classification"]["verdict"]
        == "PASS"
    )
    assert cs["unit_interval_148_to_149_across_e5"]["active_branch_count"] == 6
    assert (
        cs["unit_interval_148_to_149_across_e5"]["P0_interval_classification"]["verdict"]
        == "PASS"
    )
    assert cs["wide_interval_64_to_65_unresolved_wrapping_example"]["active_branch_count"] == 4
    assert (
        cs["wide_interval_64_to_65_unresolved_wrapping_example"]["P0_interval_classification"]["verdict"]
        == "UNRESOLVED"
    )

    # Live small-scale branch-splitting check across Y = 16 (where T jumps from 32 to 33):
    tbl_small = compute_selberg_centered_remainder_table_fast_arb(40, prec_bits=288)
    cs_16 = evaluate_interval_via_cutoff_case_split_arb(
        Fraction(16, 1) - Fraction(1, 4096),
        Fraction(16, 1) + Fraction(1, 4096),
        prec_bits=256,
        quad_tol_bits=120,
        selberg_table=tbl_small,
    )
    assert cs_16["T_range"] == [32, 33]
    assert cs_16["active_branch_count"] == 2
    assert cs_16["P0_interval_classification"]["verdict"] in POINT_MARGIN_VERDICTS


def test_tc061_holdout_classification_faithfulness_and_full_tail_4096(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify faithful classification across all 14 preregistered holdout points WITHOUT requiring
    the conjectured inequalities to be true merely for tests to pass, and verify full-energy
    evaluation of the nonempty `d >= ceil(tau*Y)` tail at `Y = 2048` and `Y = 4096`.
    """
    sec3 = tc061_artifact["section_3_preregistered_holdout_experiment"]
    cov = sec3["holdout_coverage_summary"]
    assert cov["registered_count"] == 14
    assert cov["evaluated_count"] == 14
    assert cov["coverage_complete"] is True
    assert cov["Y_4096_nonempty_subunit_tail_evaluated"] is True

    rows = sec3["holdout_point_evaluations"]
    assert len(rows) == 14

    recomputed_verdicts: Dict[str, List[str]] = {
        "TC061-P0": [],
        "TC061-P_1_2": [],
        "TC061-P_1_4": [],
        "TC061-P_1_8": [],
    }
    for row in rows:
        assert row["algebraic_consistency_verified"] is True
        assert row["J_consistency_check_role"] == "ALGEBRAIC_CONSISTENCY_CHECK_SAME_INPUTS"
        assert row["J_over_log_Y_D_tilde"]["denominator_certified_positive"] is True
        for pid, pdata in row["probe_evaluations"].items():
            assert pdata["in_declared_domain"] is True
            assert pdata["a_Y_eta_share_of_total_rhs"]["denominator_certified_positive"] is True
            lo_bs, hi_bs, _ = _parse_arb_ball_str_to_fractions(pdata["margin_M_Y"]["arb_ball_str"])
            lo_f = max(lo_bs, _sci_or_latex_num_to_fraction(pdata["margin_M_Y"]["lower_dec"]))
            hi_f = min(hi_bs, _sci_or_latex_num_to_fraction(pdata["margin_M_Y"]["upper_dec"]))
            if hi_f <= Fraction(0, 1):
                expected_verdict = "PASS"
            elif lo_f > Fraction(0, 1):
                expected_verdict = "FAIL"
            else:
                expected_verdict = "UNRESOLVED"
            assert pdata["point_verdict"] == expected_verdict, (
                f"Unfaithful margin classification at {row['point_id']} {pid}: "
                f"recorded {pdata['point_verdict']}, endpoints=({lo_f}, {hi_f})"
            )
            recomputed_verdicts[pid].append(expected_verdict)

    for pid, gsum in sec3["global_probe_outcomes"].items():
        assert gsum["uniform_proof_established"] is False
        assert gsum["global_probe_outcome"] != "PROVED_UNIFORMLY"
        expected_global = classify_global_probe_outcome(
            recomputed_verdicts[pid],
            coverage_complete=cov["coverage_complete"],
            uniform_proof_established=False,
        )
        assert gsum["global_probe_outcome"] == expected_global

    by_id = {r["point_id"]: r for r in rows}
    r2048 = by_id["HO-EXT-2048"]
    assert r2048["cutoffs"]["T_Y"] == 13778
    assert r2048["has_subunit_tail_ge_ceil_tau_Y"] is True
    assert r2048["subunit_tail_breakdown"]["subunit_tail_d_range_inclusive"] == [12868, 13777]

    r4096 = by_id["HO-EXT-4096"]
    assert r4096["cutoffs"]["T_Y"] == 32768
    assert r4096["has_subunit_tail_ge_ceil_tau_Y"] is True
    tb4096 = r4096["subunit_tail_breakdown"]
    assert tb4096 is not None
    assert tb4096["subunit_tail_d_range_inclusive"] == [25736, 32767]
    b_tail_lo, _, _ = _parse_arb_ball_str_to_fractions(tb4096["B_tail_norm_sq"]["arb_ball_str"])
    assert b_tail_lo > Fraction(0, 1), "Y = 4096 sub-unit tail energy ||B_{Y,tail}||_Y^2 must be > 0"


def test_tc061_matched_laurent_controls_and_hybrid_labeling(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify exact matched `z = 1` double-pole Laurent reconstructions for negative controls
    (`unsigned_1`, `a2`, `a_3_5_7`), certified `FAIL` counterexamples on `Y >= 64`, and explicit
    `HYBRID_DIAGNOSTIC_INNER_A2_OUTER_LIOUVILLE_COMPENSATION` labeling on `hybrid_a2_liouville`.
    """
    sec4 = tc061_artifact["section_4_controls_and_tc_arithmetic_attribution"]
    assert sec4["all_section_4_checks_pass"] is True
    assert sec4["matched_reconstruction_identities_verified"] is True
    assert sec4["all_negative_controls_certified_fail_on_Y_ge_64"] is True

    rows = sec4["control_comparison_rows"]
    for neg_mode in ("unsigned_1", "a2", "a_3_5_7"):
        neg_rows_ge_64 = [r for r in rows if r["mode"] == neg_mode and int(r["Y"]) >= 64]
        assert len(neg_rows_ge_64) == 4  # 64, 128, 256, 512
        for nr in neg_rows_ge_64:
            assert nr["matched_identity_verified"] is True
            for pid, v in nr["shared_probe_verdicts"].items():
                assert v == "FAIL", f"Expected {neg_mode} at Y={nr['Y']} to FAIL {pid}, got {v}"
                lo_m, _, _ = _parse_arb_ball_str_to_fractions(nr["shared_probe_margins"][pid]["arb_ball_str"])
                assert lo_m > Fraction(0, 1)
            assert (
                classify_global_probe_outcome(list(nr["shared_probe_verdicts"].values()), coverage_complete=True)
                == "REFUTED_BY_CERTIFIED_WITNESS"
            )

    hybrid_rows = [r for r in rows if r["mode"] == "hybrid_a2_liouville"]
    assert len(hybrid_rows) == 6
    for hr in hybrid_rows:
        assert hr["model_class"] == "HYBRID_DIAGNOSTIC_INNER_A2_OUTER_LIOUVILLE_COMPENSATION"


def test_tc061_signed_kernel_w2_self_collision_bound_and_coprime_bridge(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify Section 5 `w_{2,lambda}` factorization, same-integer sign agreement, finite-window
    Gram kernel expansion, unconditional uniform composite self-collision bound
    `0 < X_self(Y) <= (1377/160)*log(tau) < 16`, aggregate `(log X)^{-2}`-removal & complement-
    window bridge, and Section 6 Route D threshold checks.
    """
    sec5 = tc061_artifact["section_5_arithmetic_proof_attempt_and_kernel_reduction"]
    assert sec5["all_section_5_checks_pass"] is True
    assert sec5["w2_and_sign_agreement_1_to_500"]["w2_factorization_verified"] is True
    assert sec5["w2_and_sign_agreement_1_to_500"]["same_integer_sign_agreement_verified"] is True

    for kr in sec5["finite_window_gram_kernel_expansion_checks"]:
        assert kr["verified"] is True

    sc_thm = sec5["composite_self_collision_theorem"]
    assert sc_thm["lean_status"] == "CONCRETE_ANALYTIC_IN_LEAN"
    assert sc_thm["outside_lean_refinement_status"] == "ANALYTIC_PROVED_OUTSIDE_LEAN"
    assert sc_thm["elementary_analytic_proof"]["verified"] is True
    assert sc_thm["verified"] is True
    assert len(sc_thm["evaluated_scales_16_to_4096"]) == 9
    for sr in sc_thm["evaluated_scales_16_to_4096"]:
        assert sr["strictly_positive_and_le_uniform_bound"] is True
        lo_s, hi_s, _ = _parse_arb_ball_str_to_fractions(sr["X_self_Y"]["arb_ball_str"])
        assert Fraction(0, 1) < lo_s <= hi_s < Fraction(16, 1)

    br = sec5["aggregate_log_removal_and_global_coprime_bridge"]
    assert br["tau_adic_tower_verified"] is True
    assert br["verified"] is True
    for brow in br["bridge_rows"]:
        assert brow["aggregate_log_removal_certified"] is True
        assert brow["complement_window_identity_verified"] is True

    assert sec5["remaining_quantitative_lemma"]["lemma_id"] == "TC061R-OBL-SIGNED-REMAINDER-F"
    assert (
        sec5["remaining_quantitative_lemma"]["exact_equivalent_obligation_id"]
        == "TC061R-OBL-SIGNED-REMAINDER-F"
    )
    assert (
        sec5["remaining_quantitative_lemma"]["sufficient_unsigned_core_relaxation_id"]
        == "TC061-LEM-OFFDIAG-AND-CORE"
    )

    sec6 = tc061_artifact["section_6_route_d_conditional_transfer_and_scope"]
    assert sec6["all_section_6_checks_pass"] is True
    for rdr in sec6["route_d_threshold_checks"]:
        assert rdr["feedback_le_one_half_certified"] is True
        assert rdr["known_component_coeff_direct_theta_half"] == 2
        assert rdr["known_component_coeff_companion_tc060_reuse"] == 4


def test_tc061_self_collision_elementary_majorant_proof_and_scope_sync(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify the standalone elementary 3-zone majorant proof `(3/4 + 16/15 + 3 = 289/60 < 1377/160)`
    for `(289/60)*log(tau) < (1377/160)*log(tau) < 16`, non-circular Section 6 remaining-hypothesis
    mapping, and presence of `section_8_tc061_review_displayed_enclosures_audit` in the artifact.
    """
    proof = verify_self_collision_elementary_majorant_proof_arb()
    assert proof["verified"] is True
    assert proof["head_constant_fraction"] == "3/4"
    assert proof["tail_base_constant_fraction"] == "16/15"
    assert proof["tail_log_sq_constant_fraction"] == "3"
    assert proof["sharp_pointwise_constant_fraction"] == "289/60"
    assert proof["envelope_pointwise_constant_fraction"] == "1377/160"
    assert proof["log2_gt_two_thirds_certified"] is True
    assert proof["c_self_general_prime_power_identity_1_to_200_verified"] is True
    assert proof["pointwise_density_lt_289_60_spot_checked"] is True
    lo_sharp, hi_sharp, _ = _parse_arb_ball_str_to_fractions(
        proof["sharp_window_bound_289_60_log_tau"]["arb_ball_str"]
    )
    lo_env, hi_env, _ = _parse_arb_ball_str_to_fractions(
        proof["envelope_window_bound_1377_160_log_tau"]["arb_ball_str"]
    )
    assert Fraction(0, 1) < lo_sharp <= hi_sharp < lo_env <= hi_env < Fraction(16, 1)

    sec6 = tc061_artifact["section_6_route_d_conditional_transfer_and_scope"]
    rem_map = sec6["remaining_hypothesis_mapping"]
    assert len(rem_map) == 5
    assert rem_map[0]["status"] == "OPEN_CONJECTURE_OR_FAILED_CANDIDATE"
    assert "G_eps(R)" in rem_map[1]["hypothesis_name"]
    assert rem_map[1]["status"] == "ANALYTIC_PROVED_OUTSIDE_LEAN"
    assert rem_map[2]["status"] == "ANALYTIC_PROVED_OUTSIDE_LEAN"
    assert "M_lin" in rem_map[3]["hypothesis_name"]
    assert rem_map[3]["status"] == "ANALYTIC_PROVED_OUTSIDE_LEAN"
    assert "TC-059R" in rem_map[4]["source_or_obligation"]
    assert "Theorem 8" not in rem_map[4]["source_or_obligation"]

    assert "section_8_tc061_review_displayed_enclosures_audit" in tc061_artifact
    sec8 = tc061_artifact["section_8_tc061_review_displayed_enclosures_audit"]
    assert sec8["all_displayed_intervals_contain_generated_enclosures"] is True
    assert sec8["pi_macro_count"] == 0
    assert sec8["pi_glyph_count"] == 0
    assert sec8["untagged_count"] == 0
    assert sec8["failed_count"] == 0


def test_tc061_lean_wiring_and_live_axiom_audit() -> None:
    """Verify registration of `MixedArithmeticCovariance.lean` across formal build infrastructure
    and verify live `lake env lean --stdin` `#check` and `#print axioms` (`0` `sorry`, `0` custom axioms).
    """
    umbrella = (REPO_ROOT / "formal" / "RiemannScope.lean").read_text(encoding="utf-8")
    assert "import RiemannScope.MixedArithmeticCovariance" in umbrella

    build_py = (REPO_ROOT / "scripts" / "build_formal.py").read_text(encoding="utf-8")
    assert '"formal/RiemannScope/MixedArithmeticCovariance.lean"' in build_py

    cert_py = (REPO_ROOT / "certification.py").read_text(encoding="utf-8")
    assert '"formal/RiemannScope/MixedArithmeticCovariance.lean"' in cert_py

    readme_md = (REPO_ROOT / "formal" / "RiemannScope" / "README.md").read_text(encoding="utf-8")
    assert "MixedArithmeticCovariance.lean" in readme_md

    live = verify_tc061_lean_theorems_live(EXPECTED_TC061_THEOREMS)
    assert live["all_tc061_lean_checks_pass"] is True
    assert live["sorry_count"] == 0
    assert live["admit_count"] == 0
    assert live["custom_axiom_count"] == 0
    assert live["pi_token_count"] == 0
    assert set(EXPECTED_TC061_THEOREMS).issubset(set(live["declared_theorems"]))


def test_tc061_review_displayed_enclosures_and_adversarial_tamper_rejection(
    tc061_artifact: Dict[str, Any],
    tmp_path: Path,
) -> None:
    """Verify every displayed interval in `docs/reviews/TC_061_MIXED_ARITHMETIC_COVARIANCE.md`
    against `data/tc_mixed_arithmetic_covariance.json` and test adversarial tamper rejection.
    """
    assert TC_061_REVIEW_DOC_PATH.exists(), f"Missing review report {TC_061_REVIEW_DOC_PATH}"
    rev = verify_tc061_review_displayed_enclosures(tc061_artifact, TC_061_REVIEW_DOC_PATH)
    assert rev["pi_macro_count"] == 0
    assert rev["pi_glyph_count"] == 0
    assert rev["total_displayed_intervals_found"] >= 20
    assert rev["untagged_count"] == 0
    assert rev["failed_count"] == 0
    assert rev["all_displayed_intervals_contain_generated_enclosures"] is True

    # Adversarial check 1: untagged interval must fail closed:
    bad_untagged = tmp_path / "untagged.md"
    bad_untagged.write_text("Untagged sample `[1.0 +/- 1e-5]`.\n", encoding="utf-8")
    res_untagged = verify_tc061_review_displayed_enclosures(tc061_artifact, bad_untagged)
    assert res_untagged["untagged_count"] == 1
    assert res_untagged["all_displayed_intervals_contain_generated_enclosures"] is False

    # Adversarial check 2: forbidden circle-half token must fail closed:
    orig_txt = TC_061_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    bad_pi = tmp_path / "bad_circle_half.md"
    bad_pi.write_text(orig_txt + "\nForbidden token " + chr(92) + "p" + "i.\n", encoding="utf-8")
    res_pi = verify_tc061_review_displayed_enclosures(tc061_artifact, bad_pi)
    assert res_pi["pi_macro_count"] >= 1
    assert res_pi["all_displayed_intervals_contain_generated_enclosures"] is False

    # Adversarial check 3: shifted midpoint outside generated Arb ball must fail closed:
    bad_shift = tmp_path / "bad_shift.md"
    bad_shift.write_text(
        '`[999999.0 +/- 1e-40]` <!-- tc-enclosure: observable="J_direct" params="Y=64" '
        'json_path="section_1_protocol_and_exact_mixed_identity.diagnostic_and_calibration_evaluations[Y=64].J_direct" -->\n',
        encoding="utf-8",
    )
    res_shift = verify_tc061_review_displayed_enclosures(tc061_artifact, bad_shift)
    assert res_shift["failed_count"] == 1
    assert res_shift["all_displayed_intervals_contain_generated_enclosures"] is False

    # Adversarial check 4: mismatched Lean declaration line anchor must fail closed (even with valid interval):
    bad_anchor = tmp_path / "bad_anchor.md"
    bad_anchor.write_text(
        '`[0.1171271185860626646392829570809787502938 +/- 5.0e-40]` '
        '<!-- tc-enclosure: observable="J_direct" params="Y=64" '
        'json_path="section_1_protocol_and_exact_mixed_identity.diagnostic_and_calibration_evaluations[Y=64].J_direct" -->\n'
        "Bad anchor [`MixedCovarianceClosureHypothesis`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/MixedArithmeticCovariance.lean#L1-L2).\n",
        encoding="utf-8",
    )
    res_anc = verify_tc061_review_displayed_enclosures(tc061_artifact, bad_anchor)
    assert res_anc["failed_count"] == 0
    assert len(res_anc["failed_lean_line_anchors"]) == 1
    assert res_anc["all_displayed_intervals_contain_generated_enclosures"] is False


def test_tc061r_protocol_quadrature_boundary_selection_and_silent_override_rejection() -> None:
    """Verify frozen-protocol quadrature selection at `T = 431` (`Y = 128`), `T = 511`, and
    `T = 512`, escalation tiers 1 and 2, and fail-closed rejection of silent caller overrides
    and inactive three-zone parameters in `unsplit` mode (`TASK-TC-061R` §6).
    """
    rules = load_frozen_protocol_rules()

    # 1. Boundary T = 431 (< 512) and T = 511 (< 512) -> unsplit, quad_tol_bits = 240, n_panels = 1:
    r_431 = resolve_protocol_quadrature_settings(rules, 431, 805, escalation_tier=0)
    assert r_431["quadrature_mode"] == "unsplit"
    assert r_431["three_zone"] is False
    assert r_431["used_settings"] == {
        "quadrature_mode": "unsplit",
        "prec_bits": 256,
        "quad_tol_bits": 240,
        "n_panels": 1,
        "zone1_ratio_threshold_x_over_n": None,
        "zone3_cutoff_N1": None,
        "zone3_taylor_degree_M": None,
    }
    assert r_431["inactive_parameters"] == [
        "quad_tol_bits_three_zone_large_T",
        "n_panels",
        "zone1_ratio_threshold_x_over_n",
        "zone3_cutoff_N1",
        "zone3_taylor_degree_M",
    ]

    r_511 = resolve_protocol_quadrature_settings(rules, 511, 900, escalation_tier=0)
    assert r_511["quadrature_mode"] == "unsplit"
    assert r_511["used_settings"]["quad_tol_bits"] == 240
    assert r_511["used_settings"]["n_panels"] == 1

    # 2. Boundary T = 512 (>= 512) -> three_zone, quad_tol_bits = 160, 16 panels, ratio 12, M = 56:
    r_512 = resolve_protocol_quadrature_settings(rules, 512, 900, escalation_tier=0)
    assert r_512["quadrature_mode"] == "three_zone"
    assert r_512["three_zone"] is True
    assert r_512["used_settings"] == {
        "quadrature_mode": "three_zone",
        "prec_bits": 256,
        "quad_tol_bits": 160,
        "n_panels": 16,
        "zone1_ratio_threshold_x_over_n": 12,
        "zone3_cutoff_N1": 900,
        "zone3_taylor_degree_M": 56,
    }
    assert r_512["inactive_parameters"] == ["quad_tol_bits_unsplit_small_T"]

    # 3. Registered escalation tiers 1 and 2:
    r_512_t1 = resolve_protocol_quadrature_settings(rules, 512, 900, escalation_tier=1)
    assert r_512_t1["used_settings"]["prec_bits"] == 512
    assert r_512_t1["used_settings"]["quad_tol_bits"] == 240
    assert r_512_t1["used_settings"]["n_panels"] == 32
    assert r_512_t1["used_settings"]["zone1_ratio_threshold_x_over_n"] == 16
    assert r_512_t1["used_settings"]["zone3_taylor_degree_M"] == 80

    r_512_t2 = resolve_protocol_quadrature_settings(rules, 512, 900, escalation_tier=2)
    assert r_512_t2["used_settings"]["prec_bits"] == 1024
    assert r_512_t2["used_settings"]["quad_tol_bits"] == 440
    assert r_512_t2["used_settings"]["n_panels"] == 64
    assert r_512_t2["used_settings"]["zone1_ratio_threshold_x_over_n"] == 22
    assert r_512_t2["used_settings"]["zone3_taylor_degree_M"] == 112

    # 4. Silent caller overrides at Y = 128 (T = 431) and Y = 256 (T = 1024) must raise ValueError:
    sp128 = ExactScaleSpec("128", "exact_rational", Fraction(128, 1))
    with pytest.raises(ValueError, match="Silent quad_tol_bits override"):
        evaluate_mixed_covariance_point_arb(sp128, quad_tol_bits=160)
    with pytest.raises(ValueError, match="Silent n_panels override"):
        evaluate_mixed_covariance_point_arb(sp128, n_panels=16)
    with pytest.raises(ValueError, match="Silent M_taylor override"):
        evaluate_mixed_covariance_point_arb(sp128, M_taylor=56)
    with pytest.raises(ValueError, match="Inactive three-zone parameters"):
        evaluate_mixed_covariance_point_arb(
            sp128,
            quad_tol_bits=180,
            M_taylor=56,
            use_three_zone=False,
            allow_nonprotocol_override=True,
        )

    sp256 = ExactScaleSpec("256", "exact_rational", Fraction(256, 1))
    with pytest.raises(ValueError, match="Silent quad_tol_bits override"):
        evaluate_mixed_covariance_point_arb(sp256, quad_tol_bits=240)


def test_tc061r_holdout_y128_240bit_rerun_and_stored_settings_consistency(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify live `Y = 128` (`T = 431 < 512`) evaluation runs at `quadrature_mode='unsplit'`,
    `quad_tol_bits = 240`, `n_panels = 1`, matches stored `HO-BASE-128`, and check that all 14
    stored holdout rows obey the frozen `T < 512` vs `T >= 512` quadrature rule (`TASK-TC-061R` §6).
    """
    tbl = compute_selberg_centered_remainder_table_fast_arb(500, prec_bits=288)
    sp128 = ExactScaleSpec("128", "exact_rational", Fraction(128, 1))
    live_128 = evaluate_mixed_covariance_point_arb(sp128, selberg_table=tbl)
    assert live_128["cutoffs"]["T_Y"] == 431
    assert live_128["quadrature_mode"] == "unsplit"
    assert live_128["three_zone_used"] is False
    assert live_128["quad_tol_bits"] == 240
    assert live_128["panels_used"] == 1
    assert live_128["zone1_ratio_threshold_used"] is None
    assert live_128["M_taylor_used"] is None

    sec3 = tc061_artifact["section_3_preregistered_holdout_experiment"]
    rows = sec3["holdout_point_evaluations"]
    assert len(rows) == 14
    for r in rows:
        t_y = int(r["cutoffs"]["T_Y"])
        if t_y < 512:
            assert r["point_id"] == "HO-BASE-128"
            assert r["quadrature_mode"] == "unsplit"
            assert r["quad_tol_bits_used"] == 240
            assert r["panels_used"] == 1
            assert r["used_settings"]["zone1_ratio_threshold_x_over_n"] is None
            assert r["used_settings"]["zone3_taylor_degree_M"] is None
        else:
            assert r["quadrature_mode"] == "three_zone"
            assert r["quad_tol_bits_used"] == 160
            assert r["panels_used"] == 16
            assert r["used_settings"]["zone1_ratio_threshold_x_over_n"] == 12
            assert r["used_settings"]["zone3_taylor_degree_M"] == 56
        assert r["resource_budget_check"]["within_resource_budget"] is True
        assert (
            r["resource_budget_check"]["enforcement_mode"]
            == "POST_EVALUATION_BUDGET_AUDIT_NO_OS_PREEMPTIVE_KILL"
        )

    by_id = {r["point_id"]: r for r in rows}
    stored_j128_lo, stored_j128_hi, _ = _parse_arb_ball_str_to_fractions(
        by_id["HO-BASE-128"]["J_direct"]["arb_ball_str"]
    )
    live_j128_lo, live_j128_hi, _ = _parse_arb_ball_str_to_fractions(
        serialize_arb_certified(live_128["J_direct"])["arb_ball_str"]
    )
    assert max(stored_j128_lo, live_j128_lo) <= min(stored_j128_hi, live_j128_hi)

    comp = sec3["tc061r_protocol_deviation_and_rerun_comparison"]
    assert comp["verified"] is True
    assert comp["all_verdicts_identical_pass"] is True
    assert (
        comp["epistemic_role"]
        == "CORRECTED_PROTOCOL_REPEAT_ON_SAME_REGISTERED_POINT_NOT_NEW_UNSEEN_POINT"
    )
    for obs_cmp in comp["observable_enclosure_comparisons"].values():
        assert obs_cmp["enclosures_overlap"] is True
        assert obs_cmp["corrected_240bit_enclosed_within_original_160bit"] is True


def test_tc061r_escalation_state_machine_kl1_unresolved_final_unresolved_and_certified_fail() -> None:
    """Exercise `execute_holdout_point_with_protocol_escalation` across:
    1. Main probes all `PASS` + one `KL1` sub-budget `UNRESOLVED` at Tier 0 -> triggers Tier 1;
    2. Final-tier `UNRESOLVED` -> stops after Tier 2 and yields `UNRESOLVED/INCOMPLETE_COVERAGE`;
    3. Certified `FAIL` -> stops at Tier 0 without changing constants (`REFUTED_BY_CERTIFIED_WITNESS`);
    4. Post-evaluation wall-clock / RSS budget audit failure (`within_resource_budget == False`).
    """
    proto = json.loads(MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH.read_text(encoding="utf-8"))
    probes = proto["frozen_candidate_probes"]
    rules = proto["numerical_settings_and_escalation_rules"]
    spec = ExactScaleSpec("256", "exact_rational", Fraction(256, 1))

    def _make_stub_result(
        tier: int,
        *,
        J_ball: arb,
        X_ball: arb,
        R_mix_ball: arb,
        elapsed_sec: float = 0.05,
        peak_rss_mb: float = 128.0,
    ) -> Dict[str, Any]:
        resolved = resolve_protocol_quadrature_settings(rules, 1024, 1609, escalation_tier=tier)
        used = resolved["used_settings"]
        d_b = arb(1)
        lg_y = arb(256).log()
        return {
            "cutoffs": {
                "label": "256",
                "kind": "exact_rational",
                "T_Y": 1024,
                "D0_raw": 5,
                "D0_eff": 5,
                "ceil_tau_Y": 1609,
                "cutoff_prec_bits_used": int(used["prec_bits"]),
            },
            "Y_arb": arb(256),
            "log_Y_arb": lg_y,
            "D_tilde_Y": d_b,
            "log_Y_times_D_tilde": lg_y * d_b,
            "X_tilde_Y": X_ball,
            "R_mix_Y": R_mix_ball,
            "J_direct": J_ball,
            "quadrature_mode": resolved["quadrature_mode"],
            "escalation_tier": tier,
            "requested_settings": resolved["requested_settings"],
            "used_settings": used,
            "inactive_parameters": resolved["inactive_parameters"],
            "prec_bits": int(used["prec_bits"]),
            "quad_tol_bits": int(used["quad_tol_bits"]),
            "panels_used": int(used["n_panels"]),
            "elapsed_sec": elapsed_sec,
            "current_rss_mb": peak_rss_mb,
            "peak_rss_mb": peak_rss_mb,
        }

    lg_256 = arb(256).log()
    rhs_1_4 = (arb(1) / arb(4)) * lg_256

    # Case 1: Main probes PASS (J = -1.0 << log(256)), offdiag PASS (4*X = -1.0),
    # but R_mix straddles (1/4)*log(256) at Tier 0 and resolves strictly below at Tier 1!
    def _eval_kl1_only(sp, *, escalation_tier=0, protocol_rules=None, allow_nonprotocol_override=False, selberg_table=None):
        assert allow_nonprotocol_override is False
        rmix = (rhs_1_4 + arb(0, arb("1e-20"))) if escalation_tier == 0 else (rhs_1_4 - arb("0.1"))
        return _make_stub_result(escalation_tier, J_ball=arb(-1), X_ball=arb("-0.25"), R_mix_ball=rmix)

    out_kl1 = execute_holdout_point_with_protocol_escalation(
        spec, probes, rules, evaluator_fn=_eval_kl1_only
    )
    assert out_kl1["escalation_tier_used"] == 1
    assert len(out_kl1["escalation_history"]) == 2
    assert out_kl1["escalation_history"][0]["any_main_probe_in_domain_unresolved"] is False
    assert out_kl1["escalation_history"][0]["any_kl1_in_domain_unresolved"] is True
    assert out_kl1["escalation_history"][1]["used_settings"]["prec_bits"] == 512
    assert out_kl1["escalation_history"][1]["used_settings"]["quad_tol_bits"] == 240
    assert out_kl1["escalation_history"][1]["used_settings"]["n_panels"] == 32
    assert out_kl1["probe_evaluation"]["mechanism_kl1_sub_budgets"]["R_mix_verdict"] == "PASS"

    # Case 2: Margin remains UNRESOLVED through final escalation Tier 2 -> preserved UNRESOLVED:
    def _eval_always_unresolved(sp, *, escalation_tier=0, protocol_rules=None, allow_nonprotocol_override=False, selberg_table=None):
        return _make_stub_result(
            escalation_tier,
            J_ball=lg_256 + arb(0, arb("1e-15")),
            X_ball=arb(0),
            R_mix_ball=arb(0),
        )

    out_unres = execute_holdout_point_with_protocol_escalation(
        spec, probes, rules, evaluator_fn=_eval_always_unresolved
    )
    assert out_unres["escalation_tier_used"] == 2
    assert len(out_unres["escalation_history"]) == 3
    assert out_unres["escalation_history"][2]["used_settings"]["prec_bits"] == 1024
    assert out_unres["escalation_history"][2]["used_settings"]["quad_tol_bits"] == 440
    assert out_unres["escalation_history"][2]["used_settings"]["n_panels"] == 64
    p0_v = out_unres["probe_evaluation"]["per_probe"]["TC061-P0"]["point_verdict"]
    assert p0_v == "UNRESOLVED"
    assert classify_global_probe_outcome([p0_v], coverage_complete=True) == "UNRESOLVED/INCOMPLETE_COVERAGE"

    # Case 3: Certified FAIL at Tier 0 (J = 100 >> RHS) -> no escalation, probe constants untouched:
    probes_snapshot = json.dumps(probes, sort_keys=True)

    def _eval_cert_fail(sp, *, escalation_tier=0, protocol_rules=None, allow_nonprotocol_override=False, selberg_table=None):
        return _make_stub_result(escalation_tier, J_ball=arb(100), X_ball=arb(20), R_mix_ball=arb(20))

    out_fail = execute_holdout_point_with_protocol_escalation(
        spec, probes, rules, evaluator_fn=_eval_cert_fail
    )
    assert out_fail["escalation_tier_used"] == 0
    assert len(out_fail["escalation_history"]) == 1
    assert json.dumps(probes, sort_keys=True) == probes_snapshot
    for pid, pd in out_fail["probe_evaluation"]["per_probe"].items():
        assert pd["point_verdict"] == "FAIL", f"{pid} must be FAIL"
    assert (
        classify_global_probe_outcome(["FAIL", "PASS"], coverage_complete=True)
        == "REFUTED_BY_CERTIFIED_WITNESS"
    )

    # Case 4: Budget audit catches wall-clock > 300s or peak_rss > 4096 MB:
    def _eval_over_budget(sp, *, escalation_tier=0, protocol_rules=None, allow_nonprotocol_override=False, selberg_table=None):
        return _make_stub_result(
            escalation_tier,
            J_ball=arb(0),
            X_ball=arb(0),
            R_mix_ball=arb(0),
            elapsed_sec=305.0,
            peak_rss_mb=5000.0,
        )

    out_bgt = execute_holdout_point_with_protocol_escalation(
        spec, probes, rules, evaluator_fn=_eval_over_budget
    )
    assert out_bgt["resource_budget_check"]["wall_budget_exceeded"] is True
    assert out_bgt["resource_budget_check"]["rss_budget_exceeded"] is True
    assert out_bgt["resource_budget_check"]["within_resource_budget"] is False


def test_tc061r_finite_prime_control_convolution_densities_residues_and_scoped_prose(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify exact `(1 * a_S)(n)` convolution formula against direct divisor sums across `1..300`,
    required spot checks `(∅, 12) -> 6` and `({2}, 3, 6, 12) -> (2, 0, 2)`, distinct support
    densities vs `z = 1` residues, and absence of unproved asymptotic claims (`TASK-TC-061R` §3).
    """
    assert evaluate_finite_prime_parity_convolution_formula(12, ()) == 6
    assert evaluate_divisor_sum_aS_direct(12, ()) == 6
    assert evaluate_finite_prime_parity_convolution_formula(3, (2,)) == 2
    assert evaluate_finite_prime_parity_convolution_formula(6, (2,)) == 0
    assert evaluate_finite_prime_parity_convolution_formula(12, (2,)) == 2
    assert [evaluate_divisor_sum_aS_direct(n, (2,)) for n in (3, 6, 12)] == [2, 0, 2]

    for s_primes in ((), (2,), (3, 5, 7)):
        inv = compute_finite_prime_control_invariants(s_primes, verify_up_to=300)
        assert inv["convolution_formula_verified"] is True

    sec4 = tc061_artifact["section_4_controls_and_tc_arithmetic_attribution"]
    assert sec4["control_arithmetic_invariants_verified"] is True
    invs = sec4["control_arithmetic_invariants"]
    assert invs["unsigned_1"]["nonzero_support_natural_density_fraction"] == "1/1"
    assert invs["unsigned_1"]["dirichlet_series_D_aS_residue_at_z1_fraction"] == "1/1"
    assert invs["a2"]["nonzero_support_natural_density_fraction"] == "2/3"
    assert invs["a2"]["dirichlet_series_D_aS_residue_at_z1_fraction"] == "1/3"
    assert invs["a_3_5_7"]["nonzero_support_natural_density_fraction"] == "35/64"
    assert invs["a_3_5_7"]["dirichlet_series_D_aS_residue_at_z1_fraction"] == "1/4"

    # Ensure unproved O(Y) / asymp growth claims are absent from Section 4 metadata and top-level summary:
    for prose_txt in (
        sec4["section_epistemic_scope_note"],
        sec4["tc_arithmetic_attribution_statement"],
        tc061_artifact["research_outcome_class"],
    ):
        assert "O(Y) growth" not in prose_txt
        assert "O(Y) known-component growth" not in prose_txt
        assert r"\asymp" not in prose_txt


def test_tc061r_complete_core_sY_vs_betaY_compact_gram_and_spillover_above_T(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify distinct `s_Y` vs `beta_Y` vectors, nonzero spillover on `T < n <= 2*T`, pointwise
    complete-core bridge, and compact `(0, 2, 4)` Gram identity against 1D window evaluation
    (`TASK-TC-061R` §2).
    """
    tbl = compute_selberg_centered_remainder_table_fast_arb(30, prec_bits=288)
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for y_k in (2, 4, 8):
            sp = ExactScaleSpec(str(y_k), "exact_rational", Fraction(y_k, 1))
            res_1d = evaluate_mixed_covariance_point_arb(sp, selberg_table=tbl)
            T_k = res_1d["cutoffs"]["T_Y"]
            D0_eff = res_1d["cutoffs"]["D0_eff"]
            vecs = compute_complete_core_s_Y_and_beta_Y_arb(T_k, D0_eff, tbl["R_osc"], prec_bits=256)
            a_n = vecs["a_n"]
            s_Y = vecs["s_Y"]
            beta_Y = vecs["beta_Y"]

            # Distinct on 2 <= n <= T (since a_n != 0 and (log n)^2 > 0), equal on T < n <= 2*T:
            assert bool(abs(s_Y[2] - beta_Y[2]) > arb("0.4"))
            assert len(vecs["spillover_above_T_indices"]) > 0
            assert bool(vecs["max_spillover_above_T_abs"] > arb(0))
            for n_sp in vecs["spillover_above_T_indices"]:
                assert T_k < n_sp <= 2 * T_k
                assert bool(arb(0) in (s_Y[n_sp] - beta_Y[n_sp]))

            # Direct compact (0, 2, 4) Gram sum vs 1D J_direct:
            Y_b = arb(y_k)
            N2 = 2 * T_k
            g_sum = arb(0)
            for m_i in range(1, N2 + 1):
                for n_i in range(1, N2 + 1):
                    if a_n[m_i] != arb(0) and a_n[n_i] != arb(0):
                        g_sum += (
                            a_n[m_i]
                            * a_n[n_i]
                            * evaluate_window_gram_G_Y_r_arb(Y_b, m_i, n_i, 0, prec_bits=256)
                        )
                    cross = a_n[m_i] * beta_Y[n_i] + beta_Y[m_i] * a_n[n_i]
                    if cross != arb(0):
                        g_sum -= cross * evaluate_window_gram_G_Y_r_arb(Y_b, m_i, n_i, 2, prec_bits=256)
                    if beta_Y[m_i] != arb(0) and beta_Y[n_i] != arb(0):
                        g_sum += (
                            beta_Y[m_i]
                            * beta_Y[n_i]
                            * evaluate_window_gram_G_Y_r_arb(Y_b, m_i, n_i, 4, prec_bits=256)
                        )
            j_compact = g_sum - arb(4) * res_1d["D_tilde_Y"]
            diff_j = j_compact - res_1d["J_direct"]
            assert bool(arb(0) in diff_j and abs(diff_j) < arb("1e-55"))
    finally:
        flint_ctx.prec = saved_prec

    sec1 = tc061_artifact["section_1_protocol_and_exact_mixed_identity"]
    for r1 in sec1["diagnostic_and_calibration_evaluations"]:
        assert r1["spillover_above_T_count"] > 0
        lo_br, hi_br, _ = _parse_arb_ball_str_to_fractions(
            r1["max_pointwise_adjusted_beta_Y_bridge_residual"]["arb_ball_str"]
        )
        assert max(abs(lo_br), abs(hi_br)) < Fraction(1, 10**65)


def test_tc061r_coarse_halfline_complement_bound_signed_F_S_and_headline_reconciliation(
    tc061_artifact: Dict[str, Any],
) -> None:
    """Verify unconditional coarse half-line complement bound `D_inf(T) <= 2*c_G*T*zeta''(2)`,
    signed `Y = 32` log-removal sandwich, same-integer mixed `(P_Y, B_Y)` cancellation witness,
    `F(Y)` / `S(Y)` certificates across `16..4096`, and programmatic headline/exposure reconciliation
    (`TASK-TC-061R` §§4, 5, 7).
    """
    coarse = verify_coarse_halfline_complement_bound_arb()
    assert coarse["verified"] is True
    assert coarse["c_G_matches_half_gamma_5_2"] is True
    assert coarse["kernel_majorant_1_to_40_verified"] is True
    assert coarse["Q_lambda_halfline_norm_le_2_cG_L_verified"] is True

    sec5 = tc061_artifact["section_5_arithmetic_proof_attempt_and_kernel_reduction"]
    assert sec5["w2_and_sign_agreement_1_to_500"]["same_integer_mixed_PB_cancellation_witness_verified"] is True
    br = sec5["aggregate_log_removal_and_global_coprime_bridge"]
    assert br["signed_y32_sandwich_verified"] is True
    assert br["coarse_halfline_complement_bound"]["verified"] is True
    for brow in br["bridge_rows"]:
        assert brow["coarse_complement_diag_bound_certified"] is True

    for sr in sec5["composite_self_collision_theorem"]["evaluated_scales_16_to_4096"]:
        assert sr["J_le_5Xself_plus_Dtilde_plus_S_certified"] is True
        lo_res, hi_res, _ = _parse_arb_ball_str_to_fractions(
            sr["J_minus_4Xself_plus_F_residual"]["arb_ball_str"]
        )
        assert lo_res <= Fraction(0, 1) <= hi_res
        assert max(abs(lo_res), abs(hi_res)) < Fraction(1, 10**40)

    rec = tc061_artifact["headline_and_exposure_reconciliation"]
    exp_r = rec["holdout_exposure_reconciliation"]
    assert exp_r["total_holdout_points"] == 14
    assert exp_r["unseen_for_all_observables_count"] == 8
    assert exp_r["unseen_for_all_tc054_to_tc060_window_observables_count"] == 1
    assert exp_r["combined_zero_prior_window_observable_count"] == 9
    assert exp_r["counts_by_status"] == {
        "PRIOR_PARTIAL_COMPONENT_EXPOSURE": 2,
        "UNSEEN_FOR_ALL_OBSERVABLES": 8,
        "PRIOR_ANCILLARY_EXPOSURE": 2,
        "UNSEEN_FOR_ALL_TC054_TO_TC060_WINDOW_OBSERVABLES": 1,
        "PRIOR_INDEX_PARTITION_EXPOSURE_ONLY": 1,
    }

    cut_r = rec["cutoff_transitions_reconciliation"]
    assert cut_r["e5_sided_pair"] == {
        "e5_minus_D0_raw": 4,
        "e5_plus_D0_raw": 5,
        "e5_minus_T_Y": 518,
        "e5_plus_T_Y": 519,
    }
    assert cut_r["unit_interval_64_to_65"]["T_range"] == [182, 185]
    assert cut_r["unit_interval_64_to_65"]["active_branch_count"] == 4

    r4096_ratio = rec["headline_holdout_values"]["HO_EXT_4096"]["J_over_log_Y_D_tilde"]["ratio"]
    lo_r, hi_r, _ = _parse_arb_ball_str_to_fractions(r4096_ratio["arb_ball_str"])
    assert Fraction(-1356, 10000) < lo_r <= hi_r < Fraction(-1355, 10000)

