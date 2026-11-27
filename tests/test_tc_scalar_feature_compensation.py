"""Focused mathematical, numerical, formal-audit, and adversarial-governance test suite
for TASK-TC-065 (Arithmetic Scalar-Feature Compensation Across Squarefree Cores,
EPIC-TC-042 / SUBGATE-TC-043A).
"""

from __future__ import annotations

import copy
from fractions import Fraction
import json
import math
from pathlib import Path

from flint import acb, arb, ctx as flint_ctx
import pytest

from tc.canonical_theta_correlation_bound import REPO_ROOT
from tc.coupled_scale_energy_bootstrap import _tau_arb, prime_power_pairs_up_to
from tc.liouville_square_dilation import liouville_lambda_int
from tc.mixed_arithmetic_covariance import (
    CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME,
    compute_complete_core_s_Y_and_beta_Y_arb,
    compute_selberg_centered_remainder_table_fast_arb,
)
from tc.scalar_feature_compensation import (
    ACCEPTED_TC064R_TIP,
    EXPECTED_TC065_PUBLIC_DEFS,
    EXPECTED_TC065_THEOREMS,
    FROZEN_TC065_PROTOCOL_ID,
    FROZEN_TC065_PROTOCOL_SHA256,
    SCALAR_FEATURE_ARTIFACT_PATH,
    TASK_TC_065_ID,
    TASK_TC_065R_ID,
    TC_065_REVIEW_DOC_PATH,
    _audit_all_serialized_arb_balls_in_tc065_artifact,
    active_paired_prime_powers,
    aggregate_tc065_section4_and_derive_outcomes,
    certify_pointwise_oracle_residual_lower_bound_arb,
    compute_fringe_feature_theorem_bound_arb,
    derive_tc064_seen_damped_defects_exact,
    evaluate_bare_sequence_energy_and_diag_arb,
    evaluate_scalar_feature_compensation_1d_arb,
    paired_station_partition,
    reprocess_task_tc065_metadata_and_audit,
    verify_exact_tc065_algebraic_identities,
    verify_frozen_tc065_protocol_immutability,
    verify_section_1_protocols_and_premise_chain,
    verify_section_5_lean_audit_and_gate_accounting,
    verify_tc065_review_document_consistency,
)
from tc.signed_dilation_arithmetic_energy import verify_section_epistemic_scope_metadata
from tc.squarefree_core_correlation import (
    SQUAREFREE_CORE_ARTIFACT_PATH,
    canonical_cutoff_T_of_Y_exact,
)


@pytest.fixture(scope="module")
def tc065_artifact() -> dict:
    assert SCALAR_FEATURE_ARTIFACT_PATH.exists(), "Missing data/tc_scalar_feature_compensation.json"
    return json.loads(SCALAR_FEATURE_ARTIFACT_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def tc065_protocol() -> dict:
    p = verify_frozen_tc065_protocol_immutability()
    assert p["verified"] is True
    return p["protocol_object"]


def test_tc065_frozen_protocol_and_upstream_preservation() -> None:
    """Verify all five frozen protocols (TC-061..TC-065) and byte-for-byte preservation of
    all upstream artifacts, plus strict unseen disjointness of TC-065 validation targets.
    """
    sec1 = verify_section_1_protocols_and_premise_chain()
    assert sec1["all_section_1_checks_pass"] is True
    ok_scope, msg_scope = verify_section_epistemic_scope_metadata(sec1)
    assert ok_scope is True, msg_scope

    p65 = verify_frozen_tc065_protocol_immutability()
    assert p65["verified"] is True
    assert p65["protocol_id"] == FROZEN_TC065_PROTOCOL_ID
    assert p65["computed_protocol_sha256"] == FROZEN_TC065_PROTOCOL_SHA256

    # Verify unseen points are strictly disjoint from previously exposed historical scales
    proto = p65["protocol_object"]
    seen_ints = set(proto["calibration_and_prior_exposure_separation"]["previously_exposed_historical_scales_all_treated_as_seen"])
    unseen_pts = proto["unseen_validation_schedule"]["points"]
    assert len(unseen_pts) == 8
    for pt in unseen_pts:
        assert pt["prior_exposure_status"] == "UNSEEN_FOR_ALL_OBSERVABLES"
        if pt["kind"] == "exact_rational":
            q = Fraction(pt["rational_factor"])
            assert q.denominator == 1 and int(q.numerator) not in seen_ints
    assert len(proto["unseen_validation_schedule"]["prescribed_continuous_interval_splits"]) == 3


def test_tc065_seen_tc064_reproduction_and_exact_algebra() -> None:
    """Verify exact reconstruction of damped_core_defect_Y from recorded TC-064 outward
    decimal endpoints (SEEN_DERIVED_FROM_TC064_CERTIFICATES) and exhaustive exact algebra.
    """
    seen_rep = derive_tc064_seen_damped_defects_exact(SQUAREFREE_CORE_ARTIFACT_PATH)
    assert seen_rep["all_rows_verified"] is True
    assert [r["Y"] for r in seen_rep["rows"]] == [512, 576, 960, 1408]
    for r in seen_rep["rows"]:
        assert r["damped_core_defect_strictly_negative"] is True
        share_lo = Fraction(r["J_A_negativity_share_of_damped_defect"]["lower_dec"])
        share_hi = Fraction(r["J_A_negativity_share_of_damped_defect"]["upper_dec"])
        assert Fraction(1, 2) < share_lo <= share_hi < Fraction(3, 4)

    alg = verify_exact_tc065_algebraic_identities()
    assert alg["verified"] is True

    # Spot-check paired_station_partition and active_paired_prime_powers directly
    om2, ph2 = paired_station_partition(43)
    assert set(om2).isdisjoint(set(ph2))
    assert sorted(om2 + ph2) == list(range(1, 44))
    act43 = active_paired_prime_powers(43)
    for p, k in act43:
        assert p ** k <= 43
        assert p == 2 or 2 * (p ** k) <= 43


def test_tc065_live_1d_evaluator_budgets_oracle_and_unsigned_control() -> None:
    """Verify exact Route 5 & Route 6 budget residuals, general-base fringe bound,
    real-interval oracle lower bound, and unsigned a(n) = 1 scaling obstruction at Y = 16.
    """
    tbl = compute_selberg_centered_remainder_table_fast_arb(128, prec_bits=256)
    T_16 = canonical_cutoff_T_of_Y_exact(16)
    D0_16 = int(math.floor(math.log(16)))
    ev = evaluate_scalar_feature_compensation_1d_arb(
        arb(16), T_16, D0_16, tbl, prec_bits=256, quad_tol_bits=160, n_panels=8
    )
    for res_k in (
        "S1_budget_residual",
        "S2_budget_residual",
        "S3_budget_residual",
        "E1_budget_residual",
        "E2_budget_residual",
        "E3_budget_residual",
    ):
        assert bool(ev[res_k].contains(0)), f"{res_k} did not enclose 0: {ev[res_k]}"
        assert bool(abs(ev[res_k]) < arb(10) ** (-30))

    assert bool(ev["M_FRINGE_FEAT"] < arb(0))
    # Verify general-base fringe bound monotonicity in w_0 (w_0 = 2 vs w_0 = tau)
    bd_w2 = compute_fringe_feature_theorem_bound_arb(arb(16), w0_arb=arb(2), prec_bits=256)
    bd_tau = compute_fringe_feature_theorem_bound_arb(arb(16), prec_bits=256)
    assert bool(arb(0) < bd_w2 < bd_tau)

    # Certified strictly positive real-interval oracle residual lower bound at Y = 16, r = 1
    orc = certify_pointwise_oracle_residual_lower_bound_arb(
        arb(16), T_16, D0_16, tbl, r_val=Fraction(1, 1), n_subintervals=64, prec_bits=256
    )
    assert orc["certified_strictly_positive"] is True
    assert orc["verdict_for_zero_residual_contractive_pointwise_synthesis"] == "FAIL"
    assert Fraction(orc["oracle_residual_lower_bound"]["lower_dec"]) > 0

    # Unsigned a(n) = 1 scaling obstruction: E_1 / (4 D_tilde_1) > 3.5 already at Y = 16
    bare = evaluate_bare_sequence_energy_and_diag_arb(16, [0] + [1] * T_16, prec_bits=256, n_panels=8)
    assert bool(bare["E_over_4Dtilde_seq_Y"] > arb("3.5"))
    assert bool(bare["E_minus_4Dtilde_seq_Y"] > arb(0))


def test_tc065_certified_artifact_integrity_and_epistemic_scope(
    tc065_artifact: dict, tc065_protocol: dict
) -> None:
    """Validate the committed certified artifact data/tc_scalar_feature_compensation.json
    end-to-end: 975 Arb balls, 256-bit serialization tightness, 160-bit transcendental
    budget residuals, 5/5 valid epistemic scopes, 0 conflicts, open gate status.
    """
    assert tc065_artifact["task_id"] == TASK_TC_065_ID
    assert tc065_artifact["all_mathematical_and_numerical_checks_pass"] is True
    assert tc065_artifact["execution_and_certification_status"] == "CERTIFIED_COMPLETE_NO_UNRESOLVED_CONFLICTS"
    assert tc065_artifact["parent_subgate_status"] == "OPEN"
    assert tc065_artifact["rh_proved"] is False
    assert tc065_artifact["global_energy_improvement_claimed"] is False
    assert tc065_artifact["resource_compliance_status"] == "WITHIN"
    assert tc065_artifact["provenance"]["accepted_tc064r_tip"] == ACCEPTED_TC064R_TIP

    for sec_k in (
        "section_1_protocols_and_premise_chain",
        "section_2_seen_reproduction_algebra_and_cross_checks",
        "section_3_seen_discovery_and_controls",
        "section_4_unseen_validation_and_interval_splits",
        "section_5_lean_audit_and_gate_accounting",
    ):
        ok_s, msg_s = verify_section_epistemic_scope_metadata(tc065_artifact[sec_k])
        assert ok_s is True, f"{sec_k}: {msg_s}"

    arb_re = _audit_all_serialized_arb_balls_in_tc065_artifact(tc065_artifact)
    assert arb_re["verified"] is True
    assert arb_re["total_certified_arb_balls_checked"] == 975
    assert arb_re["failed_paths"] == []

    # Round 2 regression: verify >= 256-bit decimal serialization tightness (no 53-bit truncation)
    # on Section 2 and Section 3 serialized balls, and 160-bit quadrature accuracy on transcendental points.
    sec2 = tc065_artifact["section_2_seen_reproduction_algebra_and_cross_checks"]
    for row in sec2["independent_evaluator_cross_checks"]:
        w = Fraction(row["damped_core_defect_Y"]["upper_dec"]) - Fraction(row["damped_core_defect_Y"]["lower_dec"])
        assert w < Fraction(1, 10 ** 35), f"Section 2 decimal width too wide at Y={row['Y']}: {float(w)}"

    sec3 = tc065_artifact["section_3_seen_discovery_and_controls"]
    for row in sec3["seen_discovery_rows"]:
        w = Fraction(row["damped_core_defect_Y"]["upper_dec"]) - Fraction(row["damped_core_defect_Y"]["lower_dec"])
        assert w < Fraction(1, 10 ** 35), f"Section 3 decimal width too wide at Y={row['Y']}: {float(w)}"
        for rk in (
            "S1_budget_residual",
            "S2_budget_residual",
            "S3_budget_residual",
            "E1_budget_residual",
            "E2_budget_residual",
            "E3_budget_residual",
        ):
            r_lo = Fraction(row[rk]["lower_dec"])
            r_hi = Fraction(row[rk]["upper_dec"])
            assert r_lo <= 0 <= r_hi
            assert max(abs(r_lo), abs(r_hi)) < Fraction(1, 10 ** 45)

    sec4 = tc065_artifact["section_4_unseen_validation_and_interval_splits"]
    for pt_row in sec4["holdout_point_evaluations"]:
        for rk in (
            "S1_budget_residual",
            "S2_budget_residual",
            "S3_budget_residual",
            "E1_budget_residual",
            "E2_budget_residual",
            "E3_budget_residual",
        ):
            r_lo = Fraction(pt_row[rk]["lower_dec"])
            r_hi = Fraction(pt_row[rk]["upper_dec"])
            assert r_lo <= 0 <= r_hi
            assert max(abs(r_lo), abs(r_hi)) < Fraction(1, 10 ** 45), (
                f"{pt_row['point_id']} {rk} exceeded 1e-45: {float(max(abs(r_lo), abs(r_hi)))}"
            )

    re_agg = aggregate_tc065_section4_and_derive_outcomes(
        sec4["holdout_point_evaluations"],
        sec4["continuous_interval_case_splits"],
        tc065_protocol,
    )
    assert re_agg["all_section_4_checks_pass"] is True
    assert re_agg["certification_integrity_ok"] is True
    assert re_agg["certification_integrity_conflicts"] == []
    assert re_agg["total_continuous_interval_branches"] == 10
    assert re_agg["probe_outcomes"]["TC065-P0-DAMPED"] == "SURVIVED_TESTED_POINTS"
    assert re_agg["probe_outcomes"]["TC065-THM-FRINGE-FEAT-BOUND"] == "SURVIVED_TESTED_POINTS"
    for refuted_cand in (
        "TC065-CAND-S1-UNWEIGHTED-CONTRACTION",
        "TC065-CAND-S2-MERTENS-SUFF-BOUND",
        "TC065-CAND-S3-P2-SUFF-BOUND",
        "TC065-CAND-E1-MAIN-NONPOS",
        "TC065-CAND-E2-LARGE-PRIME-MAIN-NONPOS",
    ):
        assert re_agg["probe_outcomes"][refuted_cand] == "REFUTED_BY_CERTIFIED_WITNESS"


def test_tc065_adversarial_section4_fail_closed_mutations(
    tc065_artifact: dict, tc065_protocol: dict
) -> None:
    """Adversarial mutations against Section 4 aggregation MUST fail closed with
    certification_integrity_ok == False and CERTIFICATION_INTEGRITY_CONFLICT.
    """
    sec4 = tc065_artifact["section_4_unseen_validation_and_interval_splits"]
    base_pts = sec4["holdout_point_evaluations"]
    base_ivs = sec4["continuous_interval_case_splits"]

    # 1. Dropped unseen point
    pts_drop = copy.deepcopy(base_pts[:-1])
    r1 = aggregate_tc065_section4_and_derive_outcomes(pts_drop, base_ivs, tc065_protocol)
    assert r1["certification_integrity_ok"] is False
    assert r1["primary_damped_log_saving_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME

    # 2. Corrupted margin operand consistency (M_P0_DAMPED shifted by +10)
    pts_op = copy.deepcopy(base_pts)
    pts_op[0]["M_P0_DAMPED"]["lower_dec"] = "10.0"
    pts_op[0]["M_P0_DAMPED"]["upper_dec"] = "10.1"
    pts_op[0]["M_P0_DAMPED"]["mid_float"] = 10.05
    pts_op[0]["M_P0_DAMPED"]["rad_float_outward"] = 0.05
    pts_op[0]["M_P0_DAMPED"]["arb_ball_str"] = "[10.05 +/- 0.05]"
    pts_op[0]["probe_verdicts"]["TC065-P0-DAMPED"] = "FAIL"
    r2 = aggregate_tc065_section4_and_derive_outcomes(pts_op, base_ivs, tc065_protocol)
    assert r2["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "POINT_MARGIN_OPERAND_MISMATCH" for c in r2["certification_integrity_conflicts"])

    # 3. Corrupted damped identity (damped_core_defect_Y inconsistent with U_sq_minus_4V_sq - J_A)
    pts_id = copy.deepcopy(base_pts)
    pts_id[2]["J_A_Y"]["lower_dec"] = "5.0"
    pts_id[2]["J_A_Y"]["upper_dec"] = "5.1"
    pts_id[2]["J_A_Y"]["mid_float"] = 5.05
    pts_id[2]["J_A_Y"]["rad_float_outward"] = 0.05
    pts_id[2]["J_A_Y"]["arb_ball_str"] = "[5.05 +/- 0.05]"
    r3 = aggregate_tc065_section4_and_derive_outcomes(pts_id, base_ivs, tc065_protocol)
    assert r3["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "POINT_DAMPED_IDENTITY_MISMATCH" for c in r3["certification_integrity_conflicts"])

    # 4. Flipped point probe verdict without changing margin
    pts_flip = copy.deepcopy(base_pts)
    pts_flip[1]["probe_verdicts"]["TC065-P-NEG-DAMPED"] = "FAIL"
    r4 = aggregate_tc065_section4_and_derive_outcomes(pts_flip, base_ivs, tc065_protocol)
    assert r4["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "POINT_VERDICT_MISMATCH" for c in r4["certification_integrity_conflicts"])

    # 5. Flipped S4 oracle verdict without changing lower bound
    pts_orc = copy.deepcopy(base_pts)
    pts_orc[0]["probe_verdicts"]["TC065-CAND-S4-POINTWISE-ZERO-RESIDUAL"] = "FAIL"
    r5 = aggregate_tc065_section4_and_derive_outcomes(pts_orc, base_ivs, tc065_protocol)
    assert r5["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "POINT_ORACLE_VERDICT_MISMATCH" for c in r5["certification_integrity_conflicts"])

    # 6. Dropped feasible branch in continuous interval
    ivs_drop = copy.deepcopy(base_ivs)
    first_iv = next(iter(ivs_drop.keys()))
    ivs_drop[first_iv]["branches"].pop()
    r6 = aggregate_tc065_section4_and_derive_outcomes(base_pts, ivs_drop, tc065_protocol)
    assert r6["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "INTERVAL_BRANCH_PARTITION_MISMATCH" for c in r6["certification_integrity_conflicts"])

    # 7. Shrunk branch evaluated domain (fails TC-062R4 exact binary coverage!)
    ivs_shrink = copy.deepcopy(base_ivs)
    br0 = ivs_shrink[first_iv]["branches"][0]
    lo_q = Fraction(br0["evaluated_Y_interval_exact_fractions"][0])
    hi_q = Fraction(br0["evaluated_Y_interval_exact_fractions"][1])
    mid_q = (lo_q + hi_q) / 2
    br0["evaluated_Y_interval_exact_fractions"] = [
        f"{lo_q.numerator}/{lo_q.denominator}",
        f"{mid_q.numerator}/{mid_q.denominator}",
    ]
    br0["evaluated_Y_mid_man_exp"] = [0, 0]
    br0["evaluated_Y_rad_man_exp"] = [0, 0]
    r7 = aggregate_tc065_section4_and_derive_outcomes(base_pts, ivs_shrink, tc065_protocol)
    assert r7["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "INCOMPLETE_BRANCH_DOMAIN_COVERAGE" for c in r7["certification_integrity_conflicts"])

    # 8. Corrupted interval union failing to contain branch
    ivs_union = copy.deepcopy(base_ivs)
    ivs_union[first_iv]["union_M_P0_DAMPED"]["lower_dec"] = "-0.15"
    ivs_union[first_iv]["union_M_P0_DAMPED"]["upper_dec"] = "-0.14"
    ivs_union[first_iv]["union_M_P0_DAMPED"]["mid_float"] = -0.145
    ivs_union[first_iv]["union_M_P0_DAMPED"]["rad_float_outward"] = 0.005
    ivs_union[first_iv]["union_M_P0_DAMPED"]["arb_ball_str"] = "[-0.145 +/- 0.005]"
    r8 = aggregate_tc065_section4_and_derive_outcomes(base_pts, ivs_union, tc065_protocol)
    assert r8["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "UNION_DOES_NOT_CONTAIN_BRANCH" for c in r8["certification_integrity_conflicts"])

    # 9. Flipped branch classification without mutating margin
    ivs_cls = copy.deepcopy(base_ivs)
    ivs_cls[first_iv]["branches"][0]["TC065_P0_DAMPED_branch_classification"] = "FAIL"
    r9 = aggregate_tc065_section4_and_derive_outcomes(base_pts, ivs_cls, tc065_protocol)
    assert r9["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "BRANCH_VERDICT_MISMATCH" for c in r9["certification_integrity_conflicts"])

    # 10. L1 regression: forged branch M_P0_DAMPED and union_M_P0_DAMPED shifted together (verdicts & union containment still match,
    #     but branch M_P0_DAMPED contradicts branch damped_core_defect_Y - log_Y_times_D_tilde)
    ivs_l1 = copy.deepcopy(base_ivs)
    for key_b in (ivs_l1[first_iv]["branches"][0]["M_P0_DAMPED"], ivs_l1[first_iv]["union_M_P0_DAMPED"]):
        key_b["lower_dec"] = "-50.0"
        key_b["upper_dec"] = "-49.9"
        key_b["mid_float"] = -49.95
        key_b["rad_float_outward"] = 0.05
        key_b["arb_ball_str"] = "[-49.95 +/- 0.05]"
    # Make union contain all remaining branches too by widening union lower_dec to cover -50 and existing upper_dec
    orig_u_hi = base_ivs[first_iv]["union_M_P0_DAMPED"]["upper_dec"]
    ivs_l1[first_iv]["union_M_P0_DAMPED"]["lower_dec"] = "-50.0"
    ivs_l1[first_iv]["union_M_P0_DAMPED"]["upper_dec"] = orig_u_hi
    u_mid = 0.5 * (-50.0 + float(orig_u_hi))
    u_rad = 0.5 * (float(orig_u_hi) + 50.0) + 1e-6
    ivs_l1[first_iv]["union_M_P0_DAMPED"]["mid_float"] = u_mid
    ivs_l1[first_iv]["union_M_P0_DAMPED"]["rad_float_outward"] = u_rad
    ivs_l1[first_iv]["union_M_P0_DAMPED"]["arb_ball_str"] = f"[{u_mid} +/- {u_rad}]"
    r10 = aggregate_tc065_section4_and_derive_outcomes(base_pts, ivs_l1, tc065_protocol)
    assert r10["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "BRANCH_MARGIN_OPERAND_MISMATCH" for c in r10["certification_integrity_conflicts"])

    # 11. L2-L3 regression: forged point M_P_NEG_DAMPED + nonzero budget residual
    pts_l2 = copy.deepcopy(base_pts)
    pts_l2[0]["M_P_NEG_DAMPED"]["lower_dec"] = "-5.0"
    pts_l2[0]["M_P_NEG_DAMPED"]["upper_dec"] = "-4.9"
    pts_l2[0]["M_P_NEG_DAMPED"]["mid_float"] = -4.95
    pts_l2[0]["M_P_NEG_DAMPED"]["rad_float_outward"] = 0.05
    pts_l2[0]["M_P_NEG_DAMPED"]["arb_ball_str"] = "[-4.95 +/- 0.05]"
    pts_l2[1]["E1_budget_residual"]["lower_dec"] = "0.01"
    pts_l2[1]["E1_budget_residual"]["upper_dec"] = "0.02"
    pts_l2[1]["E1_budget_residual"]["mid_float"] = 0.015
    pts_l2[1]["E1_budget_residual"]["rad_float_outward"] = 0.005
    pts_l2[1]["E1_budget_residual"]["arb_ball_str"] = "[0.015 +/- 0.005]"
    r11 = aggregate_tc065_section4_and_derive_outcomes(pts_l2, base_ivs, tc065_protocol)
    assert r11["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "POINT_MARGIN_OPERAND_MISMATCH" for c in r11["certification_integrity_conflicts"])
    assert any(c["conflict_type"] == "POINT_BUDGET_RESIDUAL_NONZERO" for c in r11["certification_integrity_conflicts"])

    # 12. L4 regression: forged point T_Y violating frozen protocol expected_cutoffs
    pts_l4 = copy.deepcopy(base_pts)
    pts_l4[0]["T_Y"] = 999999
    r12 = aggregate_tc065_section4_and_derive_outcomes(pts_l4, base_ivs, tc065_protocol)
    assert r12["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "POINT_CUTOFF_PROTOCOL_MISMATCH" for c in r12["certification_integrity_conflicts"])

    # 13. L5 regression: forged S4_oracle_r1.certified_strictly_positive = True while lower_dec = 0
    pts_l5 = copy.deepcopy(base_pts)
    pts_l5[0]["S4_oracle_r1"]["certified_strictly_positive"] = True
    r13 = aggregate_tc065_section4_and_derive_outcomes(pts_l5, base_ivs, tc065_protocol)
    assert r13["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "POINT_ORACLE_FLAG_MISMATCH" for c in r13["certification_integrity_conflicts"])

    # 14. L8 regression: forged elapsed_sec exceeding budget & mismatched resource_compliance
    pts_l8 = copy.deepcopy(base_pts)
    pts_l8[0]["elapsed_sec"] = 2500.0
    pts_l8[1]["resource_compliance"]["overall_resource_status"] = "EXCEEDED"
    r14 = aggregate_tc065_section4_and_derive_outcomes(pts_l8, base_ivs, tc065_protocol)
    assert r14["certification_integrity_ok"] is False
    assert any(c["conflict_type"] == "POINT_ELAPSED_SEC_MISMATCH_OR_EXCEEDED" for c in r14["certification_integrity_conflicts"])
    assert any(c["conflict_type"] == "POINT_RESOURCE_COMPLIANCE_MISMATCH" for c in r14["certification_integrity_conflicts"])


def test_tc065_live_lean_audit_review_consistency_and_adversarial_review_checks(
    tc065_artifact: dict, tmp_path: Path
) -> None:
    """Verify live Lean 4 module audit (17 defs, 5 theorems, 845 compiled theorems),
    100% review consistency, register consistency, and 9 adversarial review mutations.
    """
    sec5 = verify_section_5_lean_audit_and_gate_accounting()
    assert sec5["all_section_5_checks_pass"] is True
    ok_s5, msg_s5 = verify_section_epistemic_scope_metadata(sec5)
    assert ok_s5 is True, msg_s5
    la = sec5["lean_module_audit"]
    assert la["public_definition_names"] == EXPECTED_TC065_PUBLIC_DEFS
    assert la["public_theorem_names"] == EXPECTED_TC065_THEOREMS
    assert la["sorry_or_admit_count"] == 0
    assert la["custom_axiom_count"] == 0
    assert la["banned_circle_tokens"] == []
    assert la["banned_non_grade_K_tokens"] == []
    assert la["formal_build_report_verified"] is True
    assert int(la["formal_build_report_total_theorems"]) >= 845

    assert TC_065_REVIEW_DOC_PATH.exists(), "Missing TC_065 review document"
    rev_res = verify_tc065_review_document_consistency(tc065_artifact, TC_065_REVIEW_DOC_PATH)
    assert rev_res["verified"] is True, rev_res
    assert rev_res["raw_tag_comment_count"] >= 199
    assert rev_res["matched_tag_count"] == rev_res["raw_tag_comment_count"]
    assert rev_res["failed_tags"] == []
    assert rev_res["untagged_intervals"] == []
    assert rev_res["bad_lean_anchors"] == []
    assert rev_res["guardrail_errors"] == []

    # Adversarial review mutations (all 9 must fail closed)
    orig_md = TC_065_REVIEW_DOC_PATH.read_text(encoding="utf-8")

    # M1: Untagged backtick [mid +/- rad]
    p1 = tmp_path / "m1.md"
    p1.write_text(orig_md + "\nUntagged `[-0.091 +/- 1e-4]`.\n", encoding="utf-8")
    assert verify_tc065_review_document_consistency(tc065_artifact, p1)["verified"] is False

    # M2: Untagged zero-centered `[+/- rad]`
    p2 = tmp_path / "m2.md"
    p2.write_text(orig_md + "\nUntagged `[+/- 0.05]`.\n", encoding="utf-8")
    assert verify_tc065_review_document_consistency(tc065_artifact, p2)["verified"] is False

    # M3: Untagged LaTeX `[-0.09 \pm 0.01]`
    p3 = tmp_path / "m3.md"
    p3.write_text(orig_md + "\nUntagged $[-0.09 \\pm 0.01]$.\n", encoding="utf-8")
    assert verify_tc065_review_document_consistency(tc065_artifact, p3)["verified"] is False

    # M4: Shrunk tagged enclosure that does not enclose JSON endpoints
    p4 = tmp_path / "m4.md"
    p4.write_text(orig_md.replace("`[-0.093836 +/- 3.50e-7]`", "`[-0.093836 +/- 1.00e-12]`", 1), encoding="utf-8")
    r_m4 = verify_tc065_review_document_consistency(tc065_artifact, p4)
    assert r_m4["verified"] is False and len(r_m4["failed_tags"]) >= 1

    # M5: Fake precision padding (> 45 sig digits)
    p5 = tmp_path / "m5.md"
    p5.write_text(
        orig_md.replace(
            "`[-0.093836 +/- 3.50e-7]`",
            "`[-0.09383600000000000000000000000000000000000000000000 +/- 1.00e-1]`",
            1,
        ),
        encoding="utf-8",
    )
    assert verify_tc065_review_document_consistency(tc065_artifact, p5)["verified"] is False

    # M6: Out-of-range Lean #L... anchor
    p6 = tmp_path / "m6.md"
    p6.write_text(
        orig_md + "\n[bad](../../formal/RiemannScope/ScalarFeatureCompensation.lean#L99999)\n",
        encoding="utf-8",
    )
    r_m6 = verify_tc065_review_document_consistency(tc065_artifact, p6)
    assert r_m6["verified"] is False and len(r_m6["bad_lean_anchors"]) >= 1

    # M7: Banned circle-half token
    p7 = tmp_path / "m7.md"
    p7.write_text(orig_md + "\nBad token \\" + "p" + "i here.\n", encoding="utf-8")
    assert verify_tc065_review_document_consistency(tc065_artifact, p7)["verified"] is False

    # M8: False rh_proved = true
    p8 = tmp_path / "m8.md"
    p8.write_text(orig_md.replace("rh_proved = false", "rh_proved = true", 1), encoding="utf-8")
    assert verify_tc065_review_document_consistency(tc065_artifact, p8)["verified"] is False

    # M9 (L10 regression): In-range Lean #L... anchor pointing to a non-declaration comment line
    p9 = tmp_path / "m9.md"
    p9.write_text(
        orig_md + "\n[bad decl](../../formal/RiemannScope/ScalarFeatureCompensation.lean#L1-L5)\n",
        encoding="utf-8",
    )
    r_m9 = verify_tc065_review_document_consistency(tc065_artifact, p9)
    assert r_m9["verified"] is False and len(r_m9["bad_lean_anchors"]) >= 1

    # Shared registers check
    q_obj = json.loads((REPO_ROOT / ".agents" / "research" / "queue.json").read_text(encoding="utf-8"))
    q_ids = {t["task_id"] for t in q_obj["tasks"]}
    assert TASK_TC_065_ID in q_ids
    assert TASK_TC_065R_ID in q_ids
    assert q_obj["active_task_id"] in {TASK_TC_065_ID, TASK_TC_065R_ID}
    s_obj = json.loads((REPO_ROOT / ".agents" / "research" / "state.json").read_text(encoding="utf-8"))
    assert s_obj.get("rh_proved", False) is False
    assert "data/tc_scalar_feature_compensation.json" in s_obj["linked_runs"]["campaign_artifacts"]


def test_tc065r_reconciliation_identities_ratios_and_payload_preservation(
    tc065_artifact: dict,
) -> None:
    """Targeted TASK-TC-065R regression: verify exact S3 identity & dyadic scaling relation,
    exact S2 M_pp(T) normalization, exact pairedOpenCoreOscO formula, outward Y=512 squared-norm
    ratios & exact S2/S3 witness sets (PASS at Y=300, 600), and metadata-only payload preservation.
    """
    saved_p = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # 1. Exact S3 identity L_S3 V_Y(X) = (log 2)/(2 log X) * S_even,Y(X), dyadic scaling,
        #    exact S2 M_pp(T), and exact pairedOpenCoreOscO at Y = 16
        Y = 16
        T = canonical_cutoff_T_of_Y_exact(Y)
        D0_eff = min(int(math.floor(math.log(Y))), T - 1)
        tbl = compute_selberg_centered_remainder_table_fast_arb(T, prec_bits=256)
        vecs = compute_complete_core_s_Y_and_beta_Y_arb(T, D0_eff, tbl["R_osc"], prec_bits=256)
        om2, phi2 = paired_station_partition(T)

        def _phi(n: int, x: arb) -> arb:
            return (x ** (arb(5) / arb(2))) * (arb(n) ** (-3)) * (-(x * x) / (arb(n) * arb(n))).exp()

        for mult in (1, 2, 5):
            X = arb(Y * mult)
            lgX = X.log()
            s_even = sum((arb(liouville_lambda_int(n)) * _phi(n, X) for n in om2 if n % 2 == 0), arb(0))
            q_half = sum(
                (arb(liouville_lambda_int(m)) * _phi(m, X / arb(2)) for m in range(1, T // 2 + 1)),
                arb(0),
            )
            phi2_even = sum((arb(liouville_lambda_int(n)) * _phi(n, X) for n in phi2 if n % 2 == 0), arb(0))
            assert bool((s_even - (-(arb(2) ** (arb(-1) / arb(2))) * q_half - phi2_even)).contains(0))

            # Exact pairedOpenCoreOscO matching Lean: (sum_{n in Omega_2} (s_Y(n) - lambda(n)*log(X/n)^2)*phi_n) / (log X)^2
            o_om_exact = sum(
                (
                    (vecs["s_Y"][n] - arb(liouville_lambda_int(n)) * ((X / arb(n)).log() ** 2))
                    * _phi(n, X)
                    for n in om2
                ),
                arb(0),
            ) / (lgX * lgX)
            u_om = sum(
                ((arb(liouville_lambda_int(n)) - vecs["beta_Y"][n] / (lgX * lgX)) * _phi(n, X) for n in om2),
                arb(0),
            )
            p_om = sum((arb(liouville_lambda_int(n)) * arb(n).log() * _phi(n, X) for n in om2), arb(0)) / lgX
            assert bool((u_om - (arb(2) * p_om - o_om_exact)).contains(0))

        # Exact S2 M_pp(T) and elementary S3 two-sided bounds against live evaluator
        ev16 = evaluate_scalar_feature_compensation_1d_arb(
            arb(Y), T, D0_eff, tbl, prec_bits=256, quad_tol_bits=160, n_panels=8
        )
        m_pp_direct = sum(
            (arb(p).log() ** 2) / arb(p ** k) for p, k in prime_power_pairs_up_to(T)
        ).sqrt()
        assert bool((ev16["S2_M_pp_T"] - m_pp_direct).contains(0))
        # Elementary two-sided S3 bounds via direct Arb quadrature of ||S_even,Y||_Y^2:
        # (log 2)^2 / (4*(log(tau*Y))^2) * ||S_even,Y||_Y^2 <= ||L_S3 V_Y||_Y^2 <= (log 2)^2 / (4*(log Y)^2) * ||S_even,Y||_Y^2
        tau_a = _tau_arb()
        log_tau_a = tau_a.log()
        om2_even = [n for n in om2 if n % 2 == 0]
        s_even_norm_sq = arb(0)
        tol_s = arb(2) ** (-140)
        for jp in range(4):
            u_lo = log_tau_a * arb(jp) / arb(4)
            u_hi = log_tau_a * arb(jp + 1) / arb(4)

            def _s_even_sq(u_var: acb, _an: bool) -> acb:
                x_c = acb(Y) * u_var.exp()
                x52 = x_c ** (acb(5) / acb(2))
                x2 = x_c * x_c
                val = acb(0)
                for n_e in om2_even:
                    val += acb(liouville_lambda_int(n_e)) * x52 * (acb(n_e) ** (-3)) * (-(x2 / acb(n_e * n_e))).exp()
                return val * val

            s_even_norm_sq += acb.integral(_s_even_sq, acb(u_lo), acb(u_hi), rel_tol=tol_s, abs_tol=tol_s).real

        c_lo_s3 = (arb(2).log() ** 2) / (arb(4) * ((tau_a * arb(Y)).log() ** 2)) * s_even_norm_sq
        c_hi_s3 = (arb(2).log() ** 2) / (arb(4) * (arb(Y).log() ** 2)) * s_even_norm_sq
        assert bool(c_lo_s3 < ev16["S3_LV_norm_sq"] < c_hi_s3)

        # 2. Exact Fraction outward-rounded Y = 512 squared-norm ratios and exact S2/S3 witness sets
        def _pct_interval(num_b: dict, den_b: dict, den_scale: Fraction = Fraction(1, 1)) -> tuple[Fraction, Fraction]:
            n_lo, n_hi = Fraction(num_b["lower_dec"]), Fraction(num_b["upper_dec"])
            d_lo, d_hi = Fraction(den_b["lower_dec"]) * den_scale, Fraction(den_b["upper_dec"]) * den_scale
            assert n_lo >= 0 and d_lo > 0
            return (n_lo / d_hi) * 100, (n_hi / d_lo) * 100

        r512 = tc065_artifact["section_3_seen_discovery_and_controls"]["seen_discovery_rows"][3]
        assert r512["Y"] == 512
        for (num_k, den_k, scale_d, pub_lo, pub_hi) in (
            ("S2_LV_norm_sq", "U_norm_sq_Y", Fraction(1, 1), Fraction("0.226195"), Fraction("0.226196")),
            ("S2_LV_norm_sq", "four_V_norm_sq_Y", Fraction(1, 4), Fraction("0.463958"), Fraction("0.463959")),
            ("S2_R_norm_sq", "U_norm_sq_Y", Fraction(1, 1), Fraction("119.340028"), Fraction("119.340029")),
            ("S3_LV_norm_sq", "U_norm_sq_Y", Fraction(1, 1), Fraction("0.265780"), Fraction("0.265781")),
            ("S3_LV_norm_sq", "four_V_norm_sq_Y", Fraction(1, 4), Fraction("0.545152"), Fraction("0.545153")),
            ("S3_R_norm_sq", "U_norm_sq_Y", Fraction(1, 1), Fraction("101.467599"), Fraction("101.467600")),
        ):
            r_lo, r_hi = _pct_interval(r512[num_k], r512[den_k], scale_d)
            assert pub_lo <= r_lo <= r_hi <= pub_hi, (
                f"Published 6dp bracket [{pub_lo}, {pub_hi}] does not enclose {num_k}/{den_k} = [{float(r_lo):.9f}, {float(r_hi):.9f}]"
            )

        # Verify seen TC-064 J_A / |D_core| exact outward containment in [50.4%, 71.3%]
        for seen_r in tc065_artifact["section_2_seen_reproduction_algebra_and_cross_checks"]["seen_derived_from_tc064_certificates"]["rows"]:
            ja_lo = Fraction(seen_r["J_A_negativity_share_of_damped_defect"]["lower_dec"]) * 100
            ja_hi = Fraction(seen_r["J_A_negativity_share_of_damped_defect"]["upper_dec"]) * 100
            assert Fraction("50.4") <= ja_lo <= ja_hi <= Fraction("71.3")

        # Verify S2 & S3 sufficient margins are strictly NEGATIVE (PASS) at unseen Y = 300 and Y = 600,
        # and strictly POSITIVE (FAIL) at Y = 1200, 1600, 1800 (with Y = 1800 ~ +0.03740 / +0.01865)
        pts_by_id = {
            r["point_id"]: r
            for r in tc065_artifact["section_4_unseen_validation_and_interval_splits"]["holdout_point_evaluations"]
        }
        # Outward enclosure [0.516%, 0.599%] for S2 ||LV||^2 / ||U||^2 across {600, 1200, 1600, 1800}
        # and [4.203150%, 4.203151%] at TC065-HO-EXP3-LEFT
        for pid in ("TC065-HO-600", "TC065-HO-1200", "TC065-HO-1600", "TC065-HO-1800"):
            p_lo, p_hi = _pct_interval(pts_by_id[pid]["S2_LV_norm_sq"], pts_by_id[pid]["U_norm_sq_Y"])
            assert Fraction("0.516") <= p_lo <= p_hi <= Fraction("0.599"), f"{pid}: [{float(p_lo):.6f}, {float(p_hi):.6f}]"
        exp3_lo, exp3_hi = _pct_interval(
            pts_by_id["TC065-HO-EXP3-LEFT"]["S2_LV_norm_sq"], pts_by_id["TC065-HO-EXP3-LEFT"]["U_norm_sq_Y"]
        )
        assert Fraction("4.203150") <= exp3_lo <= exp3_hi <= Fraction("4.203151")
        for pid in ("TC065-HO-300", "TC065-HO-600"):
            assert Fraction(pts_by_id[pid]["S2_suff_bound"]["upper_dec"]) < 0
            assert Fraction(pts_by_id[pid]["S3_suff_bound"]["upper_dec"]) < 0
        for pid in ("TC065-HO-1200", "TC065-HO-1600", "TC065-HO-1800"):
            assert Fraction(pts_by_id[pid]["S2_suff_bound"]["lower_dec"]) > 0
            assert Fraction(pts_by_id[pid]["S3_suff_bound"]["lower_dec"]) > 0
        assert abs(pts_by_id["TC065-HO-1800"]["S2_suff_bound"]["mid_float"] - 0.037401) < 1e-4
        assert abs(pts_by_id["TC065-HO-1800"]["S3_suff_bound"]["mid_float"] - 0.018646) < 1e-4
        # Verify E2 non-monotonicity between seen Y = 256 and unseen Y = 300
        r256 = tc065_artifact["section_3_seen_discovery_and_controls"]["seen_discovery_rows"][2]
        assert Fraction(r256["E2_T_main"]["lower_dec"]) > Fraction(pts_by_id["TC065-HO-300"]["E2_T_main"]["upper_dec"])
    finally:
        flint_ctx.prec = saved_p

    # 3. Verify metadata-only reprocess preserves Sections 2-5, generated_at_utc, producers, and all 975 Arb balls identically
    reproc = reprocess_task_tc065_metadata_and_audit(
        SCALAR_FEATURE_ARTIFACT_PATH,
        write_output=False,
        validation_commit_override=tc065_artifact["provenance"]["validation_git_commit"],
    )
    for sec_k in (
        "generated_at_utc",
        "section_2_seen_reproduction_algebra_and_cross_checks",
        "section_3_seen_discovery_and_controls",
        "section_4_unseen_validation_and_interval_splits",
        "section_5_lean_audit_and_gate_accounting",
        "serialized_arb_self_check",
    ):
        assert reproc[sec_k] == tc065_artifact[sec_k], f"Reprocess altered {sec_k}"
    assert reproc["provenance"]["numerical_producing_git_commit"] == tc065_artifact["provenance"]["numerical_producing_git_commit"]
    assert reproc["provenance"]["formal_producing_git_commit"] == tc065_artifact["provenance"]["formal_producing_git_commit"]
