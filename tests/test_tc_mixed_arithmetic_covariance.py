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

from flint import arb
import pytest

from tc.canonical_theta_correlation_bound import REPO_ROOT, verify_all_serialized_arb_in_tree
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
    TASK_TC_061_ID,
    TC_061_LEAN_MODULE_PATH,
    TC_061_REVIEW_DOC_PATH,
    ExactScaleSpec,
    calibrate_secondary_a_eta_exact,
    certified_ratio_with_positive_denominator,
    certify_exact_scale_cutoffs,
    classify_global_probe_outcome,
    classify_probe_margin_arb,
    compute_selberg_centered_remainder_table_fast_arb,
    evaluate_interval_via_cutoff_case_split_arb,
    evaluate_mixed_covariance_point_arb,
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
    assert tc061_artifact["parent_subgate"] == PARENT_SUBGATE_ID
    assert tc061_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc061_artifact["rh_proved"] is False
    assert tc061_artifact["hypothesis_H_status"] == "OPEN_CONJECTURE_OR_FAILED_CANDIDATE"
    assert tc061_artifact["merged_main_baseline"] == MERGED_MAIN_BASELINE_TC061
    assert tc061_artifact["accepted_tc060r2_tip"] == ACCEPTED_TC060R2_TIP
    assert tc061_artifact["accepted_tc060r2_implementation"] == ACCEPTED_TC060R2_IMPLEMENTATION
    assert tc061_artifact["inherited_tc060r_formal_commit"] == REVIEWED_TC060R_IMPLEMENTATION
    assert tc061_artifact["branch"] == PROPOSED_TC061_BRANCH
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

    assert sec5["remaining_quantitative_lemma"]["lemma_id"] == "TC061-LEM-OFFDIAG-AND-CORE"

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
