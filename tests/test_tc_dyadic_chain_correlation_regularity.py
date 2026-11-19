r"""
Regression, falsification, and adversarial governance suite for `TASK-TC-063`:
Dyadic-Chain Correlations and the Arithmetic Regularity Constraint (`EPIC-TC-042`, `SUBGATE-TC-043A`).
"""

from __future__ import annotations

import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Dict

import pytest
from flint import arb, ctx as flint_ctx

from certification import REQUIRED_FORMAL_SOURCES
from scripts.build_formal import FORMAL_SOURCE_FILES
from tc.canonical_theta_correlation_bound import serialize_arb_certified
from tc.dyadic_chain_correlation_regularity import (
    ACCEPTED_TC062R4_DELIVERED_TIP,
    DYADIC_CHAIN_ARTIFACT_PATH,
    DYADIC_CHAIN_PROTOCOL_PATH,
    EXPECTED_TC062_ARTIFACT_SHA256,
    EXPECTED_TC063_THEOREMS,
    FROZEN_TC063_PROTOCOL_ID,
    FROZEN_TC063_PROTOCOL_REGISTRATION_COMMIT,
    FROZEN_TC063_PROTOCOL_SHA256,
    PRESERVED_TC062R_PRODUCING_COMMIT,
    REQUIRED_CURRENT_TC063_STATUS_KEYS,
    TASK_TC_063_ID,
    TC_063_LEAN_MODULE_PATH,
    TC_063_REVIEW_DOC_PATH,
    aggregate_tc063_section5_and_derive_outcomes,
    audit_continuous_interval_split_certificate_tc063,
    build_tc063_premise_and_dependency_table,
    compare_tc063_artifacts_by_stable_key,
    dyadic_chain_exponents_J_u,
    extract_lean_declaration_spans_tc063,
    greedy_sign_extension_witness,
    interior_two_adic_anchors,
    max_dyadic_chain_length_L,
    odd_chain_parts_O_T,
    odd_common_factor_gcd_set,
    reprocess_task_tc063_metadata_and_lean_audit,
    verify_frozen_tc063_protocol_immutability,
    verify_odd_part_decomposition_exhaustive_exact,
    verify_tc063_review_enclosures_and_lean_anchors,
)
from tc.dyadic_power_lift_primitive_correlation import (
    EPISTEMIC_CATEGORIES,
    PARENT_SUBGATE_ID,
)
from tc.joint_prime_dilation_signed_remainder import (
    FROZEN_TC062_PROTOCOL_ID,
    JOINT_PRIME_DILATION_ARTIFACT_PATH,
    JOINT_PRIME_DILATION_PROTOCOL_PATH,
    _exact_arb_endpoints_as_fractions,
    _parse_serialized_arb_enclosure_tc062,
    verify_frozen_tc062_protocol_immutability,
)
from tc.mixed_arithmetic_covariance import (
    CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME,
    FROZEN_PROTOCOL_ID as TC061_FROZEN_PROTOCOL_ID,
    MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH,
    MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH,
    strip_enclosure_arb_for_json,
    verify_all_serialized_arb_in_tree,
    verify_frozen_protocol_immutability,
)
from tc.signed_dilation_arithmetic_energy import verify_section_epistemic_scope_metadata


@pytest.fixture(scope="module")
def tc063_artifact() -> Dict[str, Any]:
    assert DYADIC_CHAIN_ARTIFACT_PATH.exists(), (
        f"Missing {DYADIC_CHAIN_ARTIFACT_PATH}; generate before running pytest."
    )
    return json.loads(DYADIC_CHAIN_ARTIFACT_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def tc063_protocol() -> Dict[str, Any]:
    return json.loads(DYADIC_CHAIN_PROTOCOL_PATH.read_text(encoding="utf-8"))


def test_tc063_protocols_immutability_hygiene_and_open_gate(
    tc063_artifact: Dict[str, Any],
) -> None:
    """Verify all three frozen protocols, preserved TC-061/TC-062 artifacts, token hygiene,
    section epistemic scope maps, and honest OPEN gate status.
    """
    assert tc063_artifact["task_id"] == TASK_TC_063_ID
    assert tc063_artifact["parent_subgate"] == PARENT_SUBGATE_ID
    assert tc063_artifact["parent_subgate_status"] == "OPEN"
    assert tc063_artifact["rh_proved"] is False
    assert tc063_artifact["global_energy_improvement_claimed"] is False
    assert tc063_artifact["sampled_zeta_zeros_used"] == 0
    assert tc063_artifact["all_mathematical_and_numerical_checks_pass"] is True

    chk61 = verify_frozen_protocol_immutability()
    assert chk61["verified"] is True and chk61["protocol_id"] == TC061_FROZEN_PROTOCOL_ID
    chk62 = verify_frozen_tc062_protocol_immutability()
    assert chk62["verified"] is True and chk62["protocol_id"] == FROZEN_TC062_PROTOCOL_ID
    chk63 = verify_frozen_tc063_protocol_immutability()
    assert chk63["verified"] is True
    assert chk63["protocol_id"] == FROZEN_TC063_PROTOCOL_ID
    assert chk63["recorded_protocol_sha256"] == FROZEN_TC063_PROTOCOL_SHA256
    assert chk63["registration_commit"] == FROZEN_TC063_PROTOCOL_REGISTRATION_COMMIT

    # Verify all 885 TC-062 records and 3,208 TC-061 records remain untouched:
    tc062_bytes = JOINT_PRIME_DILATION_ARTIFACT_PATH.read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(tc062_bytes).hexdigest() == EXPECTED_TC062_ARTIFACT_SHA256
    tc062_json = json.loads(tc062_bytes.decode("utf-8"))
    assert tc062_json["serialized_arb_self_check"]["total_certified_arb_balls_checked"] == 885
    assert (
        tc062_json["provenance"]["numerical_producing_git_commit"]
        == PRESERVED_TC062R_PRODUCING_COMMIT
    )
    tc061_json = json.loads(MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert tc061_json["serialized_arb_self_check"]["total_certified_arb_balls_checked"] == 3208

    prov = tc063_artifact["provenance"]
    assert prov["accepted_tc062r4_delivered_tip"] == ACCEPTED_TC062R4_DELIVERED_TIP
    assert prov["frozen_tc063_protocol_registration_commit"] == FROZEN_TC063_PROTOCOL_REGISTRATION_COMMIT

    for sec_key in (
        "section_1_protocols_endpoint_and_premise_chain",
        "section_2_odd_part_decomposition_and_cross_checks",
        "section_3_same_chain_bound_and_matched_controls",
        "section_4_distinct_chain_attempts_and_obstructions",
        "section_5_unseen_validation_and_interval_splits",
        "section_6_lean_audit_and_gate_accounting",
    ):
        ep_ok, ep_msg = verify_section_epistemic_scope_metadata(tc063_artifact[sec_key])
        assert ep_ok is True, (sec_key, ep_msg)
        for st in tc063_artifact[sec_key]["epistemic_statuses"]:
            assert st in EPISTEMIC_CATEGORIES

    arb_self = tc063_artifact["serialized_arb_self_check"]
    assert arb_self["all_enclose_original_256bit_arb_ball"] is True
    assert arb_self["live_original_count_matches_enumerated_total"] is True
    assert arb_self["total_certified_arb_balls_checked"] == 674
    assert arb_self["failed_paths"] == []

    # Independently audit all 674 serialized Arb balls via 3-representation validator:
    req_k = {"mid_float", "rad_float_outward", "lower_dec", "upper_dec", "arb_ball_str"}
    checked_count = 0

    def _walk_check(node: Any, pth: str) -> None:
        nonlocal checked_count
        if isinstance(node, dict):
            if req_k.issubset(node.keys()):
                parsed = _parse_serialized_arb_enclosure_tc062(node)
                assert parsed is not None, f"Malformed serialized Arb ball at {pth}"
                checked_count += 1
                return
            for k, v in node.items():
                _walk_check(v, f"{pth}.{k}" if pth else k)
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                _walk_check(item, f"{pth}[{idx}]")

    _walk_check(tc063_artifact, "")
    assert checked_count == 674

    p_tok = "p" + "i"
    for fpath in (
        DYADIC_CHAIN_PROTOCOL_PATH,
        DYADIC_CHAIN_ARTIFACT_PATH,
        Path(__file__).resolve().parent.parent / "tc" / "dyadic_chain_correlation_regularity.py",
        TC_063_LEAN_MODULE_PATH,
        TC_063_REVIEW_DOC_PATH,
    ):
        assert fpath.exists(), f"Expected deliverable {fpath} to exist"
        raw = fpath.read_text(encoding="utf-8")
        for bad in ("\\" + p_tok, "\u03c0", "Real." + p_tok, "const_" + p_tok, "math." + p_tok):
            assert bad not in raw, (fpath.name, bad)
        k_toks = [
            tok
            for tok in re.findall(r"\bK_[A-Za-z0-9_]+", raw)
            if tok != "K_reserved_for_real_algebraic_geometric_grades_A_R"
        ]
        assert k_toks == [], (fpath.name, k_toks)


def test_tc063_section_1_endpoint_contradiction_and_premise_chain(
    tc063_artifact: Dict[str, Any],
) -> None:
    """Verify premise table completeness, Dirichlet product on x > 1, trivial-zero simultaneous
    vanishing, reflection, and generic window-base b > 1 checks.
    """
    sec1 = tc063_artifact["section_1_protocols_endpoint_and_premise_chain"]
    assert sec1["all_section_1_checks_pass"] is True

    prem_tbl = build_tc063_premise_and_dependency_table()
    assert len(prem_tbl) == 10
    open_prems = [p for p in prem_tbl if p["status"] == "OPEN"]
    lean_prems = [p for p in prem_tbl if p["status"] == "PROVED_IN_LEAN"]
    outside_prems = [p for p in prem_tbl if p["status"] == "PROVED_ANALYTICALLY_OUTSIDE_LEAN"]
    assert len(open_prems) == 1
    assert open_prems[0]["premise_id"] == "TC063-PREM-01-DISTINCT-ODD-CHAIN-BOUND"
    assert open_prems[0]["gap_kind"] == "MISSING_MATHEMATICS"
    assert len(lean_prems) == 3
    assert len(outside_prems) == 6
    assert all(p["gap_kind"] == "MISSING_LEAN_FORMALIZATION_ONLY" for p in outside_prems)

    assert all(r["verified"] and r["zeta_2z_certified_nonzero"] for r in sec1["dirichlet_ratio_nonvanishing_checks"])
    assert all(r["both_numerator_and_denominator_vanish"] for r in sec1["trivial_zero_double_vanishing_checks"])
    assert all(r["verified"] for r in sec1["functional_equation_reflection_checks"])
    bases = {r["window_base_label"]: r for r in sec1["generic_window_base_hilbert_checks"]}
    assert set(bases.keys()) == {"2", "3", "tau"}
    assert all(r["verified"] for r in bases.values())


def test_tc063_section_2_odd_part_decomposition_and_sign_change(
    tc063_artifact: Dict[str, Any],
) -> None:
    """Verify exhaustive small-T odd-part decomposition, empty/singleton chain edge cases,
    independent 1D-vs-2D validations, and certified sign change of S_same(Y).
    """
    assert odd_chain_parts_O_T(0) == []
    assert odd_chain_parts_O_T(1) == []
    assert interior_two_adic_anchors(1) == []
    assert max_dyadic_chain_length_L(1) == 0
    assert odd_chain_parts_O_T(2) == [1]
    assert dyadic_chain_exponents_J_u(1, 7) == [0]
    assert dyadic_chain_exponents_J_u(1, 8) == [0, 1]

    ex = verify_odd_part_decomposition_exhaustive_exact()
    assert ex["verified"] is True

    sec2 = tc063_artifact["section_2_odd_part_decomposition_and_cross_checks"]
    assert sec2["all_section_2_checks_pass"] is True
    assert sec2["S_same_sign_change_certified"]["Y_16_positive"] is True
    assert sec2["S_same_sign_change_certified"]["Y_64_negative"] is True
    assert len(sec2["complete_kernel_cross_validation_rows"]) == 6
    assert all(r["verified"] for r in sec2["complete_kernel_cross_validation_rows"])


def test_tc063_section_3_same_chain_hilbert_bound_and_matched_controls(
    tc063_artifact: Dict[str, Any],
) -> None:
    """Verify shifted-station disjointness, m = n self-collision indispensability, uniform
    same-chain Hilbert margins across Y = 2..1024, and matched control / hybrid S_different
    refutations on Y >= 64.
    """
    sec3 = tc063_artifact["section_3_same_chain_bound_and_matched_controls"]
    assert sec3["all_section_3_checks_pass"] is True
    f_chk = sec3["shifted_station_disjointness_and_feature_checks"]
    assert f_chk["disjointness_verified_on_I2_180"] is True
    assert f_chk["m_eq_n_self_collision_indispensability_certified_at_Y16_m3"] is True

    rows_same = sec3["same_chain_hilbert_bound_rows"]
    assert [r["Y"] for r in rows_same] == [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    assert all(r["verified"] for r in rows_same)

    ctrl_rows = sec3["matched_control_and_hybrid_chain_rows"]
    for row in ctrl_rows:
        mode = row["mode"]
        if mode == "hybrid_a2_liouville":
            assert row["is_hybrid_diagnostic"] is True
            assert row["exact_matched_core"] is False
        else:
            assert row["is_hybrid_diagnostic"] is False
            assert row["exact_matched_core"] is True
        if row["Y"] >= 64:
            if mode == "liouville":
                assert row["TC063_P0_DIFF_verdict"] == "PASS"
            else:
                assert row["TC063_P0_DIFF_verdict"] == "FAIL"


def test_tc063_section_4_distinct_chain_attempts_and_counterexamples(
    tc063_artifact: Dict[str, Any],
) -> None:
    """Verify Attempts A, B, and C, including exact constructive greedy sign extension on arbitrary
    non-symmetric matrices and certified refutations of CAND-A1, CAND-B1, and CAND-C1.
    """
    sec4 = tc063_artifact["section_4_distinct_chain_attempts_and_obstructions"]
    assert sec4["all_section_4_checks_pass"] is True

    att_a = sec4["attempt_A_common_factor_primitive_regrouping"]
    assert att_a["coprime_feature_decoupling_verified"] is True
    assert att_a["p2_smallop_jump_obstruction_certified"] is True
    assert att_a["candidate_A1_prim_nonpos"]["outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert att_a["candidate_A1_prim_nonpos"]["refutation_certified"] is True
    assert odd_common_factor_gcd_set(5) == []
    assert odd_common_factor_gcd_set(6) == [1]

    att_b = sec4["attempt_B_square_projection_and_selberg_compatibility"]
    assert att_b["station_selberg_decomposition_verified"] is True
    assert att_b["candidate_B1_sqproj_diag_dom"]["outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert att_b["candidate_B1_sqproj_diag_dom"]["refutation_certified"] is True

    att_c = sec4["attempt_C_arithmetic_restricted_vs_arbitrary_sign_comparison"]
    assert att_c["candidate_C1_arbitrary_sign"]["outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert att_c["candidate_C1_arbitrary_sign"]["refutation_and_omega_Y_obstruction_certified"] is True

    # Independently test `greedy_sign_extension_witness` on a non-symmetric exact matrix:
    flint_ctx.prec = 256
    nodes = [1, 3, 5, 7, 9, 11]
    seed = [3, 7]
    H_mat = {(u, v): arb(3 * u - 5 * v + 2) for u in nodes for v in nodes if u != v}
    eps = greedy_sign_extension_witness(nodes, seed, lambda u, v: H_mat.get((u, v), arb(0)))
    assert set(eps.keys()) == set(nodes)
    assert all(eps[u] in (-1, 1) for u in nodes)
    assert eps[3] == 1 and eps[7] == 1
    seed_q = sum((H_mat[(u, v)] for u in seed for v in seed if u != v), arb(0))
    full_q = sum((arb(eps[u] * eps[v]) * H_mat[(u, v)] for u in nodes for v in nodes if u != v), arb(0))
    assert bool(full_q >= seed_q)


def test_tc063_section_5_adversarial_coverage_witness_and_provenance(
    tc063_artifact: Dict[str, Any],
    tc063_protocol: Dict[str, Any],
    tmp_path: Path,
) -> None:
    """Verify actual Section 5 mixed discovery (`TC063-P-NEG-DIFF` refuted at `Y >= 960` while
    `TC063-P0-DIFF` survives 10/10 unseen points + 2 continuous intervals) AND test adversarial
    mutations across BOTH generator aggregator and metadata reprocessor (`TC-062R4` domain
    coverage, refutation admissibility, union containment, deleted-status provenance, and
    3-valued resource compliance).
    """
    sec5 = tc063_artifact["section_5_unseen_validation_and_interval_splits"]
    assert sec5["all_section_5_checks_pass"] is True
    assert sec5["registered_unseen_point_count"] == 10
    assert sec5["evaluated_unseen_point_count"] == 10
    assert sec5["coverage_complete"] is True
    assert sec5["certification_integrity_ok"] is True
    assert sec5["all_required_applicable_evaluations_resolved"] is True
    assert (
        tc063_artifact["holdout_hypothesis_outcome"]
        == "MIXED_ZERO_SLACK_REFUTED_LOG_SAVING_SURVIVED"
    )
    assert tc063_artifact["primary_log_saving_probe_outcome"] == "SURVIVED_TESTED_POINTS"
    assert tc063_artifact["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"
    assert sec5["per_candidate_mathematical_outcomes"]["TC063-SAME-LOCAL-HILBERT"] == "PROVED_UNIFORMLY"
    assert sec5["per_candidate_mathematical_outcomes"]["TC063-P0-DIFF"] == "SURVIVED_TESTED_POINTS"
    assert sec5["per_candidate_mathematical_outcomes"]["TC063-P-HALF-DIFF"] == "SURVIVED_TESTED_POINTS"
    assert sec5["per_candidate_mathematical_outcomes"]["KL1_same_chain"] == "SURVIVED_TESTED_POINTS"
    assert sec5["per_candidate_mathematical_outcomes"]["KL1_different_chain"] == "SURVIVED_TESTED_POINTS"
    assert (
        sec5["per_candidate_mathematical_outcomes"]["TC063-P-NEG-DIFF"]
        == "REFUTED_BY_CERTIFIED_WITNESS"
    )

    flint_ctx.prec = 256
    neg_ball = strip_enclosure_arb_for_json(serialize_arb_certified(arb(-1) / arb(16)))
    pos_ball = strip_enclosure_arb_for_json(serialize_arb_certified(arb(1) / arb(4)))

    # Build a synthetic all-PASS fixture `sec5_all_pass` to test pure SURVIVED_TESTED_POINTS paths:
    sec5_all_pass = copy.deepcopy(sec5)
    for row in sec5_all_pass["holdout_point_evaluations"]:
        pneg = row["probe_evaluations"]["TC063-P-NEG-DIFF"]
        if pneg["applicable_in_domain"]:
            pneg["margin_M_Y"] = copy.deepcopy(neg_ball)
            pneg["verdict"] = "PASS"
    sp1096_pass = sec5_all_pass["continuous_interval_case_splits"][
        "interval_1096_50_to_1096_66_across_T6310_and_e7"
    ]
    for br in sp1096_pass["branches"]:
        br["M_P_NEG_DIFF"] = copy.deepcopy(neg_ball)
        br["TC063_P_NEG_DIFF_branch_classification"] = {"verdict": "PASS"}
    sp1096_pass["union_M_P_NEG_DIFF"] = copy.deepcopy(neg_ball)
    sp1096_pass["TC063_P_NEG_DIFF_interval_classification"] = {"verdict": "PASS"}

    def _run_both(mut_sec5: Dict[str, Any], name: str) -> tuple[Dict[str, Any], Dict[str, Any]]:
        _, top_g = aggregate_tc063_section5_and_derive_outcomes(
            copy.deepcopy(mut_sec5), tc063_protocol
        )
        art_m = copy.deepcopy(tc063_artifact)
        art_m["section_5_unseen_validation_and_interval_splits"] = copy.deepcopy(mut_sec5)
        p_tmp = tmp_path / f"{name}.json"
        p_tmp.write_text(json.dumps(art_m), encoding="utf-8")
        rep = reprocess_task_tc063_metadata_and_lean_audit(p_tmp, write_output=False)
        return top_g, rep

    g0, r0 = _run_both(sec5_all_pass, "synthetic_all_pass")
    assert g0["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert r0["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert r0["all_mathematical_and_numerical_checks_pass"] is True

    # 1a. Drop middle branch `(6311, 6, 6)` on actual `sec5` -> `TC063-P-NEG-DIFF` stays REFUTED
    #     from point witness `Y = 960`, while `TC063-P0-DIFF` loses coverage (`PARTIAL_REFUTATION...`):
    s_drop_mixed = copy.deepcopy(sec5)
    s_drop_mixed["continuous_interval_case_splits"][
        "interval_1096_50_to_1096_66_across_T6310_and_e7"
    ]["branches"].pop(1)
    s_drop_mixed["continuous_interval_case_splits"][
        "interval_1096_50_to_1096_66_across_T6310_and_e7"
    ]["active_branch_count"] = 2
    g1m, r1m = _run_both(s_drop_mixed, "drop_middle_branch_mixed")
    assert (
        g1m["holdout_hypothesis_outcome"]
        == "PARTIAL_REFUTATION_WITH_UNRESOLVED_OR_INCOMPLETE_SIBLINGS"
    )
    assert g1m["primary_log_saving_probe_outcome"] == "UNRESOLVED/INCOMPLETE_COVERAGE"
    assert (
        r1m["section_5_unseen_validation_and_interval_splits"][
            "per_candidate_mathematical_outcomes"
        ]["TC063-P-NEG-DIFF"]
        == "REFUTED_BY_CERTIFIED_WITNESS"
    )
    assert r1m["all_mathematical_and_numerical_checks_pass"] is False

    # 1b. Drop middle branch `(6311, 6, 6)` on `sec5_all_pass` -> UNRESOLVED/INCOMPLETE_COVERAGE:
    s_drop = copy.deepcopy(sec5_all_pass)
    s_drop["continuous_interval_case_splits"][
        "interval_1096_50_to_1096_66_across_T6310_and_e7"
    ]["branches"].pop(1)
    s_drop["continuous_interval_case_splits"][
        "interval_1096_50_to_1096_66_across_T6310_and_e7"
    ]["active_branch_count"] = 2
    g1, r1 = _run_both(s_drop, "drop_middle_branch")
    assert g1["holdout_hypothesis_outcome"] == "UNRESOLVED/INCOMPLETE_COVERAGE"
    assert r1["holdout_hypothesis_outcome"] == "UNRESOLVED/INCOMPLETE_COVERAGE"
    assert r1["all_mathematical_and_numerical_checks_pass"] is False

    # 2. Delete `evaluated_Y_interval_exact_fractions` leaving only unlinked outward `Y_sub_ball`
    #    -> outward ball alone CANNOT certify complete subdomain coverage (`TC-062R4`):
    s_unlinked = copy.deepcopy(sec5_all_pass)
    s_unlinked["continuous_interval_case_splits"][
        "interval_81_pm_2_neg12_across_T243"
    ]["branches"][0].pop("evaluated_Y_interval_exact_fractions", None)
    g2, r2 = _run_both(s_unlinked, "unlinked_outward_ball")
    assert g2["holdout_hypothesis_outcome"] == "UNRESOLVED/INCOMPLETE_COVERAGE"
    assert r2["holdout_hypothesis_outcome"] == "UNRESOLVED/INCOMPLETE_COVERAGE"
    assert r2["all_mathematical_and_numerical_checks_pass"] is False

    # 3a. Shrink actual binary domain inside `[331775/4096, 81]` to `[809999/10000, 81]`
    #     (with consistent binary man/exp & Y_sub_ball) omitting `331775/4096 = 80.999755859375`
    #     -> PROVED_COVERAGE_GAP -> UNRESOLVED/INCOMPLETE_COVERAGE:
    s_shrunk = copy.deepcopy(sec5_all_pass)
    y_shrunk_arb = arb.union(arb(809999) / arb(10000), arb(81))
    sh_lo, sh_hi = _exact_arb_endpoints_as_fractions(y_shrunk_arb)
    sh_mid_me = y_shrunk_arb.mid().man_exp()
    sh_rad_me = y_shrunk_arb.rad().man_exp()
    br0_sh = s_shrunk["continuous_interval_case_splits"]["interval_81_pm_2_neg12_across_T243"][
        "branches"
    ][0]
    br0_sh["Y_sub_ball"] = strip_enclosure_arb_for_json(serialize_arb_certified(y_shrunk_arb))
    br0_sh["evaluated_Y_interval_exact_fractions"] = [
        f"{sh_lo.numerator}/{sh_lo.denominator}",
        f"{sh_hi.numerator}/{sh_hi.denominator}",
    ]
    br0_sh["evaluated_Y_mid_man_exp"] = [int(sh_mid_me[0]), int(sh_mid_me[1])]
    br0_sh["evaluated_Y_rad_man_exp"] = [int(sh_rad_me[0]), int(sh_rad_me[1])]
    g3, r3 = _run_both(s_shrunk, "shrunk_exact_domain")
    assert g3["holdout_hypothesis_outcome"] == "UNRESOLVED/INCOMPLETE_COVERAGE"
    assert r3["holdout_hypothesis_outcome"] == "UNRESOLVED/INCOMPLETE_COVERAGE"

    # 3b. Tamper with `evaluated_Y_interval_exact_fractions` WITHOUT matching binary man/exp
    #     -> CERTIFICATION_INTEGRITY_CONFLICT:
    s_tamper_frac = copy.deepcopy(sec5_all_pass)
    s_tamper_frac["continuous_interval_case_splits"][
        "interval_81_pm_2_neg12_across_T243"
    ]["branches"][0]["evaluated_Y_interval_exact_fractions"] = ["809999/10000", "81/1"]
    g3t, r3t = _run_both(s_tamper_frac, "tamper_exact_fractions")
    assert g3t["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert r3t["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME

    # 4. Admissible evaluated `FAIL` witness on branch 0 EVEN WHEN branch 1 is missing
    #    certifies `REFUTED_BY_CERTIFIED_WITNESS` for `TC063-P0-DIFF` (with partial sibling status):
    s_adm_fail = copy.deepcopy(sec5_all_pass)
    sp81 = s_adm_fail["continuous_interval_case_splits"]["interval_81_pm_2_neg12_across_T243"]
    sp81["branches"] = [sp81["branches"][0]]
    sp81["active_branch_count"] = 1
    sp81["branches"][0]["M_P0_DIFF"] = pos_ball
    sp81["branches"][0]["TC063_P0_DIFF_branch_classification"] = {"verdict": "FAIL"}
    sp81["union_M_P0_DIFF"] = pos_ball
    sp81["TC063_P0_DIFF_interval_classification"] = {"verdict": "FAIL"}
    g4, r4 = _run_both(s_adm_fail, "admissible_fail_partial")
    assert g4["primary_log_saving_probe_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert (
        r4["execution_and_certification_status"]
        == "PARTIAL_CERTIFICATION_REFUTED_WITH_UNRESOLVED_OR_INCOMPLETE_SIBLINGS"
    )
    assert r4["all_mathematical_and_numerical_checks_pass"] is False

    # 5. Conservative extra branch evaluated on a disjoint domain (`[80/1, 8099/100]`, outside
    #    `[331775/4096, 331777/4096]`) with `FAIL` margin CANNOT certify refutation:
    s_disj_fail = copy.deepcopy(sec5_all_pass)
    sp81_d = s_disj_fail["continuous_interval_case_splits"]["interval_81_pm_2_neg12_across_T243"]
    extra_br = copy.deepcopy(sp81_d["branches"][0])
    extra_br["branch_role"] = "POSSIBLY_EMPTY_CONSERVATIVE_BRANCH"
    extra_br["T_fixed"] = 242
    y_disj_arb = arb.union(arb(80), arb(8099) / arb(100))
    dj_lo, dj_hi = _exact_arb_endpoints_as_fractions(y_disj_arb)
    dj_mid_me = y_disj_arb.mid().man_exp()
    dj_rad_me = y_disj_arb.rad().man_exp()
    extra_br["Y_sub_ball"] = strip_enclosure_arb_for_json(serialize_arb_certified(y_disj_arb))
    extra_br["evaluated_Y_interval_exact_fractions"] = [
        f"{dj_lo.numerator}/{dj_lo.denominator}",
        f"{dj_hi.numerator}/{dj_hi.denominator}",
    ]
    extra_br["evaluated_Y_mid_man_exp"] = [int(dj_mid_me[0]), int(dj_mid_me[1])]
    extra_br["evaluated_Y_rad_man_exp"] = [int(dj_rad_me[0]), int(dj_rad_me[1])]
    extra_br["M_P0_DIFF"] = pos_ball
    extra_br["TC063_P0_DIFF_branch_classification"] = {"verdict": "FAIL"}
    sp81_d["branches"].append(extra_br)
    sp81_d["active_branch_count"] = 3
    zero_rad1 = strip_enclosure_arb_for_json(serialize_arb_certified(arb(0, 1)))
    sp81_d["union_M_P0_DIFF"] = zero_rad1
    sp81_d["TC063_P0_DIFF_interval_classification"] = {"verdict": "UNRESOLVED"}
    ia_disj = audit_continuous_interval_split_certificate_tc063(
        "interval_81_pm_2_neg12_across_T243", sp81_d
    )
    assert ia_disj["certification_integrity_ok"] is True
    assert ia_disj["derived_probe_outcomes"]["TC063-P0-DIFF"] == "SURVIVED_TESTED_POINTS"
    assert ia_disj["derived_probe_outcomes"]["TC063-P-HALF-DIFF"] == "SURVIVED_TESTED_POINTS"

    # 5b. `TC063-P-HALF-DIFF` tracks interval `M_P0_DIFF` AND candidate `domain_threshold_Y0`
    #     is enforced on continuous intervals (`D3`):
    s_int_p0_fail = copy.deepcopy(sec5_all_pass)
    sp81_pf = s_int_p0_fail["continuous_interval_case_splits"]["interval_81_pm_2_neg12_across_T243"]
    for br in sp81_pf["branches"]:
        br["M_P0_DIFF"] = copy.deepcopy(pos_ball)
        br["TC063_P0_DIFF_branch_classification"] = {"verdict": "FAIL"}
    sp81_pf["union_M_P0_DIFF"] = copy.deepcopy(pos_ball)
    sp81_pf["TC063_P0_DIFF_interval_classification"] = {"verdict": "FAIL"}
    so_pf, _ = aggregate_tc063_section5_and_derive_outcomes(s_int_p0_fail, tc063_protocol)
    assert so_pf["per_candidate_mathematical_outcomes"]["TC063-P0-DIFF"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert so_pf["per_candidate_mathematical_outcomes"]["TC063-P-HALF-DIFF"] == "REFUTED_BY_CERTIFIED_WITNESS"

    # Now raise `TC063-P0-DIFF` `domain_threshold_Y0` to `200` (above `[81-2^-12, 81+2^-12]`):
    proto_y200 = copy.deepcopy(tc063_protocol)
    for pr in proto_y200["frozen_candidate_probes"]:
        if pr["probe_id"] == "TC063-P0-DIFF":
            pr["domain_threshold_Y0"] = "200"
    s_y200 = copy.deepcopy(s_int_p0_fail)
    for row in s_y200["holdout_point_evaluations"]:
        if row["cutoffs"]["T_Y"] < 1000:  # Y in {81-2^-12, 81+2^-12, 96, 144} < 200
            row["probe_evaluations"]["TC063-P0-DIFF"]["applicable_in_domain"] = False
            row["probe_evaluations"]["TC063-P0-DIFF"]["verdict"] = "OUT_OF_DOMAIN_NOT_APPLICABLE"
    so_y200, _ = aggregate_tc063_section5_and_derive_outcomes(s_y200, proto_y200)
    assert so_y200["per_candidate_mathematical_outcomes"]["TC063-P0-DIFF"] == "SURVIVED_TESTED_POINTS"
    assert so_y200["per_candidate_mathematical_outcomes"]["TC063-P-HALF-DIFF"] == "REFUTED_BY_CERTIFIED_WITNESS"
    art_y200 = copy.deepcopy(tc063_artifact)
    art_y200["section_5_unseen_validation_and_interval_splits"] = s_y200
    p_y200 = tmp_path / "proto_y200.json"
    p_y200.write_text(json.dumps(art_y200), encoding="utf-8")
    rep_y200 = reprocess_task_tc063_metadata_and_lean_audit(
        p_y200, write_output=False, protocol_override=proto_y200
    )
    assert rep_y200["primary_log_saving_probe_outcome"] == "SURVIVED_TESTED_POINTS"

    # Interior `domain_threshold_Y0 = 663553/8192` (> 81) excludes branch 0 `[331775/4096, 81]`:
    sp81_b0_only = copy.deepcopy(sec5_all_pass["continuous_interval_case_splits"]["interval_81_pm_2_neg12_across_T243"])
    sp81_b0_only["branches"][0]["M_P0_DIFF"] = copy.deepcopy(pos_ball)
    sp81_b0_only["branches"][0]["TC063_P0_DIFF_branch_classification"] = {"verdict": "FAIL"}
    sp81_b0_only["union_M_P0_DIFF"] = zero_rad1
    sp81_b0_only["TC063_P0_DIFF_interval_classification"] = {"verdict": "UNRESOLVED"}
    ia_int_y0 = audit_continuous_interval_split_certificate_tc063(
        "interval_81_pm_2_neg12_across_T243",
        sp81_b0_only,
        cand_y0_by_id={"TC063-P0-DIFF": Fraction(663553, 8192)},
    )
    assert ia_int_y0["derived_probe_outcomes"]["TC063-P0-DIFF"] == "SURVIVED_TESTED_POINTS"
    assert ia_int_y0["derived_probe_outcomes"]["TC063-P-HALF-DIFF"] == "REFUTED_BY_CERTIFIED_WITNESS"

    # 6. Union ball failing to contain branch OR forged binary `man_exp` / point Y_enclosure /
    #    applicability / duplicate branch -> CERTIFICATION_INTEGRITY_CONFLICT (`D4`):
    s_bad_man_exp = copy.deepcopy(sec5)
    s_bad_man_exp["continuous_interval_case_splits"]["interval_81_pm_2_neg12_across_T243"][
        "branches"
    ][0]["evaluated_Y_mid_man_exp"] = [1, -999]
    g6m, r6m = _run_both(s_bad_man_exp, "bad_binary_man_exp")
    assert g6m["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert r6m["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME

    s_bad_u = copy.deepcopy(sec5)
    s_bad_u["continuous_interval_case_splits"]["interval_81_pm_2_neg12_across_T243"][
        "union_S_different_Y"
    ] = pos_ball
    g6, r6 = _run_both(s_bad_u, "bad_union_containment")
    assert g6["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert r6["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME

    s_forged_y = copy.deepcopy(sec5)
    s_forged_y["holdout_point_evaluations"][0]["Y_enclosure"] = copy.deepcopy(pos_ball)
    g6y, r6y = _run_both(s_forged_y, "forged_point_y")
    assert g6y["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert r6y["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME

    s_forged_app = copy.deepcopy(sec5)
    s_forged_app["holdout_point_evaluations"][0]["probe_evaluations"]["TC063-P0-DIFF"][
        "applicable_in_domain"
    ] = False
    g6a, r6a = _run_both(s_forged_app, "forged_applicability")
    assert g6a["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert r6a["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME

    s_dup_br = copy.deepcopy(sec5)
    sp81_dup = s_dup_br["continuous_interval_case_splits"]["interval_81_pm_2_neg12_across_T243"]
    sp81_dup["branches"].append(copy.deepcopy(sp81_dup["branches"][0]))
    g6d, r6d = _run_both(s_dup_br, "duplicate_branch")
    assert g6d["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert r6d["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME

    # 7. Deleted/wrong-typed/extra status fields & multi-scope verdict mutations in
    #    `compare_tc063_artifacts_by_stable_key` (`D5`):
    cmp_none = compare_tc063_artifacts_by_stable_key(None, tc063_artifact)
    assert cmp_none["comparison_status"] == "NOT_COMPARED"
    assert cmp_none["any_mathematical_verdict_changed"] is None
    assert cmp_none["any_status_classification_changed"] is None

    for rk in REQUIRED_CURRENT_TC063_STATUS_KEYS:
        mut_prior = copy.deepcopy(tc063_artifact)
        scope_p, field_p = rk.split(".", 1)
        if scope_p == "top":
            mut_prior.pop(field_p, None)
        else:
            mut_prior["section_5_unseen_validation_and_interval_splits"].pop(field_p, None)
        cmp_del = compare_tc063_artifacts_by_stable_key(tc063_artifact, mut_prior)
        assert cmp_del["comparison_status"] == "INCOMPLETE_COMPARISON"
        assert cmp_del["any_mathematical_verdict_changed"] is None
        assert cmp_del["any_status_classification_changed"] is None
        assert rk in cmp_del["missing_status_keys"]

    # Wrong-typed `rh_proved = 0` (`int` instead of `bool`) -> INCOMPLETE_COMPARISON (`None`):
    mut_type = copy.deepcopy(tc063_artifact)
    mut_type["rh_proved"] = 0
    cmp_type = compare_tc063_artifacts_by_stable_key(tc063_artifact, mut_type)
    assert cmp_type["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert cmp_type["any_status_classification_changed"] is None

    # Extra status key in `prior_art` deleted in `current_art` -> INCOMPLETE_COMPARISON (`None`):
    mut_extra_st = copy.deepcopy(tc063_artifact)
    mut_extra_st["prior_repair_status"] = "OPEN"
    cmp_extra = compare_tc063_artifacts_by_stable_key(tc063_artifact, mut_extra_st)
    assert cmp_extra["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert cmp_extra["any_status_classification_changed"] is None
    assert "top.prior_repair_status" in cmp_extra["removed_status_or_schema_fields"]

    # Multi-scope verdict changes (point, interval, control, Section 4) are detected:
    mut_v = copy.deepcopy(tc063_artifact)
    mut_v["section_5_unseen_validation_and_interval_splits"]["holdout_point_evaluations"][9][
        "probe_evaluations"
    ]["TC063-P-NEG-DIFF"]["verdict"] = "PASS"
    mut_v["section_3_same_chain_bound_and_matched_controls"][
        "matched_control_and_hybrid_chain_rows"
    ][0]["TC063_P0_DIFF_verdict"] = "FAIL"
    mut_v["section_4_distinct_chain_attempts_and_obstructions"][
        "attempt_A_common_factor_primitive_regrouping"
    ]["candidate_A1_prim_nonpos"]["outcome"] = "UNRESOLVED/INCOMPLETE_COVERAGE"
    cmp_v = compare_tc063_artifacts_by_stable_key(tc063_artifact, mut_v)
    assert cmp_v["comparison_status"] == "COMPLETE_COMPARED"
    assert cmp_v["any_mathematical_verdict_changed"] is True
    assert len(cmp_v["changed_mathematical_verdict_keys"]) == 3

    # Conflict sentinel in `per_candidate_mathematical_outcomes` -> INCOMPLETE_COMPARISON:
    mut_conf_v = copy.deepcopy(tc063_artifact)
    mut_conf_v["section_5_unseen_validation_and_interval_splits"][
        "per_candidate_mathematical_outcomes"
    ]["TC063-P0-DIFF"] = CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    cmp_cv = compare_tc063_artifacts_by_stable_key(tc063_artifact, mut_conf_v)
    assert cmp_cv["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert cmp_cv["any_mathematical_verdict_changed"] is None

    # 8. Corrupted Section 1 ball & corrupted CAND-A1 witnesses in `reprocess_task_tc063...` (`D6`):
    art_corrupt = copy.deepcopy(tc063_artifact)
    art_corrupt["section_1_protocols_endpoint_and_premise_chain"][
        "dirichlet_ratio_nonvanishing_checks"
    ][0]["abs_zeta_2z"]["lower_dec"] = "999.0"
    art_corrupt["section_1_protocols_endpoint_and_premise_chain"][
        "dirichlet_ratio_nonvanishing_checks"
    ][0]["abs_zeta_2z"]["upper_dec"] = "-999.0"
    art_corrupt["section_4_distinct_chain_attempts_and_obstructions"][
        "attempt_A_common_factor_primitive_regrouping"
    ]["candidate_A1_prim_nonpos"]["witness_Y16_g5"] = copy.deepcopy(neg_ball)
    p_corrupt = tmp_path / "corrupt_s1_s4.json"
    p_corrupt.write_text(json.dumps(art_corrupt), encoding="utf-8")
    rep_corrupt = reprocess_task_tc063_metadata_and_lean_audit(p_corrupt, write_output=False)
    assert rep_corrupt["all_mathematical_and_numerical_checks_pass"] is False
    assert (
        rep_corrupt["section_4_distinct_chain_attempts_and_obstructions"][
            "all_section_4_checks_pass"
        ]
        is False
    )
    assert rep_corrupt["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert rep_corrupt["serialized_arb_self_check"]["all_enclose_original_256bit_arb_ball"] is False

    # 9. Resource EXCEEDED / UNKNOWN remain orthogonal to mathematical outcome:
    s_exc = copy.deepcopy(sec5)
    s_exc["holdout_point_evaluations"][0]["tier_escalation_history"][0]["peak_rss_mb"] = 99999.0
    g8, _ = _run_both(s_exc, "res_exceeded")
    assert (
        g8["holdout_hypothesis_outcome"]
        == "MIXED_ZERO_SLACK_REFUTED_LOG_SAVING_SURVIVED"
    )
    assert g8["primary_log_saving_probe_outcome"] == "SURVIVED_TESTED_POINTS"
    assert g8["resource_compliance_status"] == "EXCEEDED"

    s_unk = copy.deepcopy(sec5)
    s_unk["holdout_point_evaluations"][0]["tier_escalation_history"][0][
        "peak_rss_measurement_semantics"
    ] = "TIER_LOCAL_SNAPSHOT"
    g9, _ = _run_both(s_unk, "res_unknown")
    assert (
        g9["holdout_hypothesis_outcome"]
        == "MIXED_ZERO_SLACK_REFUTED_LOG_SAVING_SURVIVED"
    )
    assert g9["primary_log_saving_probe_outcome"] == "SURVIVED_TESTED_POINTS"
    assert g9["resource_compliance_status"] == "UNKNOWN"


def test_tc063_section_6_lean_audit_and_review_verification(
    tc063_artifact: Dict[str, Any],
    tmp_path: Path,
) -> None:
    """Verify live Lean 4 declaration audit (`0` sorry/admit/custom axioms, all 5 expected public
    theorems, `formal_build_report_pass = True`), registration in `build_formal.py` &
    `certification.py`, prior-exposure audit disclosure (`D1`), and review enclosure/anchor/cutoff
    alignment (`D2`).
    """
    rel_lean = "formal/RiemannScope/DyadicChainCorrelationRegularity.lean"
    assert rel_lean in FORMAL_SOURCE_FILES
    assert rel_lean in REQUIRED_FORMAL_SOURCES
    lean_chk = extract_lean_declaration_spans_tc063()
    assert lean_chk["verified"] is True, lean_chk
    assert lean_chk["formal_build_report_pass"] is True, lean_chk
    assert lean_chk["sorry_count"] == 0
    assert lean_chk["admit_count"] == 0
    assert lean_chk["custom_axiom_count"] == 0
    assert lean_chk["expected_theorems_all_present"] is True
    assert set(EXPECTED_TC063_THEOREMS).issubset(set(lean_chk["public_theorems"]))

    sec1 = tc063_artifact["section_1_protocols_endpoint_and_premise_chain"]
    assert sec1["preserved_tc061_artifact_integrity"]["verified"] is True
    assert sec1["preserved_tc062_artifact_integrity"]["verified"] is True

    sec5 = tc063_artifact["section_5_unseen_validation_and_interval_splits"]
    assert (
        sec5["prior_exposure_audit_disclosure"]["strictly_zero_prior_occurrences_count"]
        == 9
    )
    assert "TC063-HO-UNSEEN-96" in sec5["prior_exposure_audit_disclosure"][
        "single_observable_prior_occurrence_points"
    ]

    sec6 = tc063_artifact["section_6_lean_audit_and_gate_accounting"]
    assert sec6["imported_in_root_RiemannScope_lean"] is True
    assert sec6["lean_module_audit"]["formal_build_report_pass"] is True
    assert sec6["all_section_6_checks_pass"] is True

    rev_chk = verify_tc063_review_enclosures_and_lean_anchors(tc063_artifact, TC_063_REVIEW_DOC_PATH)
    assert rev_chk["verified"] is True, rev_chk
    assert rev_chk["holdout_cutoffs_checked"] == 10
    assert rev_chk["holdout_cutoff_failures"] == []

    # Unknown Lean declaration name OR wrong holdout cutoff in review table must fail closed:
    rev_txt = TC_063_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    bad_anchor_p = tmp_path / "bad_anchor.md"
    bad_anchor_p.write_text(
        rev_txt + "\n[`nonexistent_decl_xyz`](../../formal/RiemannScope/DyadicChainCorrelationRegularity.lean#L1-L2)\n",
        encoding="utf-8",
    )
    assert verify_tc063_review_enclosures_and_lean_anchors(tc063_artifact, bad_anchor_p)["verified"] is False

    bad_cut_p = tmp_path / "bad_cut.md"
    bad_cut_p.write_text(rev_txt.replace("$(5344, 6, 6)$", "$(5351, 6, 6)$"), encoding="utf-8")
    assert verify_tc063_review_enclosures_and_lean_anchors(tc063_artifact, bad_cut_p)["verified"] is False
