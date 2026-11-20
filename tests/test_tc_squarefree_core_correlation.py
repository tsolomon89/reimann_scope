"""Focused & adversarial test suite for TASK-TC-064:
Squarefree-Core Correlations and the Arithmetic Regularity Constraint (SUBGATE-TC-043A).
"""

from __future__ import annotations

import copy
from fractions import Fraction
import json
from pathlib import Path
import re

from flint import arb, ctx as flint_ctx
import pytest

from certification import REQUIRED_FORMAL_SOURCES
from scripts.build_formal import FORMAL_SOURCE_FILES
from tc.canonical_theta_correlation_bound import REPO_ROOT, serialize_arb_certified
from tc.mixed_arithmetic_covariance import (
    CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME,
    compute_selberg_centered_remainder_table_fast_arb,
)
from tc.squarefree_core_correlation import (
    DECLARED_PREMISE_STATUSES,
    EXPECTED_TC064_THEOREMS,
    FROZEN_TC064_PROTOCOL_ID,
    FROZEN_TC064_PROTOCOL_REGISTRATION_COMMIT,
    FROZEN_TC064_PROTOCOL_SHA256,
    PRESCRIBED_TC064_INTERVAL_SPLITS,
    REQUIRED_CURRENT_TC064_STATUS_KEYS,
    SQUAREFREE_CORE_ARTIFACT_PATH,
    SQUAREFREE_CORE_LEAN_PATH,
    SQUAREFREE_CORE_LEAN_REL,
    SQUAREFREE_CORE_PROTOCOL_PATH,
    TASK_TC_064_ID,
    TC_064_REVIEW_DOC_PATH,
    aggregate_tc064_section5_and_derive_outcomes,
    compare_tc064_artifacts_by_stable_key,
    compute_uniform_same_core_constants_arb,
    core_square_multipliers_B_a,
    odd_squarefree_common_factor_set,
    odd_squarefree_core_and_root,
    odd_squarefree_cores_C_T,
    reprocess_task_tc064_metadata_and_lean_audit,
    squarefree_core_star,
    verify_divisor_core_support_exhaustive_exact,
    verify_five_piece_hilbert_and_feature_bound_at_Y16_arb,
    verify_frozen_tc064_protocol_immutability,
    verify_squarefree_core_decomposition_exhaustive_exact,
    verify_tc064_review_document_consistency,
)


@pytest.fixture(scope="module")
def tc064_protocol() -> dict:
    chk = verify_frozen_tc064_protocol_immutability()
    assert chk["verified"] is True, chk
    return chk["protocol_object"]


@pytest.fixture(scope="module")
def tc064_artifact() -> dict:
    assert SQUAREFREE_CORE_ARTIFACT_PATH.exists()
    return json.loads(SQUAREFREE_CORE_ARTIFACT_PATH.read_text(encoding="utf-8"))


def test_tc064_protocol_immutability_and_prior_exposure_separation(
    tc064_protocol: dict, tc064_artifact: dict
) -> None:
    assert tc064_protocol["protocol_id"] == FROZEN_TC064_PROTOCOL_ID
    assert tc064_protocol["protocol_sha256"] == FROZEN_TC064_PROTOCOL_SHA256
    assert tc064_protocol["circle_constant_convention"] == "tau_exclusively"

    sec1 = tc064_artifact["section_1_protocols_endpoint_and_premise_chain"]
    assert sec1["all_section_1_checks_pass"] is True
    assert sec1["preserved_tc061_protocol_immutability"]["verified"] is True
    assert sec1["preserved_tc062_protocol_immutability"]["verified"] is True
    assert sec1["preserved_tc063_protocol_immutability"]["verified"] is True
    assert sec1["frozen_tc064_protocol_immutability"]["verified"] is True
    assert (
        sec1["frozen_tc064_protocol_immutability"]["registration_commit"]
        == FROZEN_TC064_PROTOCOL_REGISTRATION_COMMIT
    )

    up = sec1["preserved_upstream_artifacts"]
    assert up["tc061_artifact"]["verified"] is True
    assert up["tc061_artifact"]["total_certified_arb_balls"] == 3208
    assert up["tc062_artifact"]["verified"] is True
    assert up["tc062_artifact"]["total_certified_arb_balls"] == 885
    assert up["tc063r_artifact"]["verified"] is True
    assert up["tc063r_artifact"]["total_certified_arb_balls"] == 688

    # Seen scales {512, 576, 960, 1408} must never appear in unseen validation schedule:
    seen_labels = {"512", "576", "960", "1408", "512/1", "576/1", "960/1", "1408/1"}
    prior_excl = set(
        tc064_protocol["calibration_and_prior_exposure_separation"][
            "previously_exposed_scales_excluded_from_tc064_unseen_validation"
        ]
    )
    for pt in tc064_protocol["unseen_validation_schedule"]["points"]:
        assert pt["prior_exposure_status"] == "UNSEEN_FOR_ALL_OBSERVABLES"
        assert pt["label"] not in seen_labels
        assert pt["rational_factor"] not in seen_labels
        assert pt["label"] not in prior_excl

    # Declaration-level premise table uses only the 5 canonical status classes:
    prem_rows = sec1["premise_and_dependency_table"]
    assert len(prem_rows) >= 12
    statuses_seen = {r["status"] for r in prem_rows}
    assert statuses_seen.issubset(set(DECLARED_PREMISE_STATUSES))
    assert statuses_seen == set(DECLARED_PREMISE_STATUSES)


def test_tc064_deliverable_a_exact_decomposition_and_gram_diagonal_guard(
    tc064_artifact: dict,
) -> None:
    exact_res = verify_squarefree_core_decomposition_exhaustive_exact()
    assert exact_res["verified"] is True

    # Edge-case spot checks:
    assert odd_squarefree_cores_C_T(0) == []
    assert odd_squarefree_cores_C_T(1) == []
    assert odd_squarefree_cores_C_T(2) == [1]
    assert core_square_multipliers_B_a(1, 17) == [1]
    assert core_square_multipliers_B_a(1, 18) == [1, 3]
    assert core_square_multipliers_B_a(3, 53) == [1]
    assert core_square_multipliers_B_a(3, 54) == [1, 3]
    assert core_square_multipliers_B_a(3, 149) == [1, 3]
    assert core_square_multipliers_B_a(3, 150) == [1, 3, 5]

    sec2 = tc064_artifact["section_2_squarefree_core_decomposition_and_cross_checks"]
    assert sec2["all_section_2_checks_pass"] is True

    # Critical Gram-diagonal vs full-kernel guard:
    diag_guards = sec2["gram_diagonal_vs_full_kernel_discrepancy_witnesses"]
    assert len(diag_guards) == 2
    for dg in diag_guards:
        assert dg["strictly_nonzero_certified"] is True
        disc = arb(dg["nonzero_discrepancy_full_minus_gram"]["arb_ball_str"])
        assert bool(abs(disc).lower() > arb("1e-3"))

    # Independent 2D-vs-1D cross-validation across Y in {2, 4, 8, 16, 32, 64}:
    cross_rows = sec2["independent_2d_vs_1d_cross_checks"]
    assert [r["Y"] for r in cross_rows] == [2, 4, 8, 16, 32, 64]
    for cr in cross_rows:
        assert cr["validation_kind"] == "INDEPENDENT_DIRECT_NUMERICAL_VALIDATION"
        assert cr["verified"] is True


def test_tc064_deliverable_b_divisor_support_and_omission_guards(
    tc064_artifact: dict,
) -> None:
    div_res = verify_divisor_core_support_exhaustive_exact()
    assert div_res["verified"] is True
    assert div_res["e_eq_1_explicitly_included"] is True
    assert 27 in div_res["noncoprime_c_f_divisors_explicitly_included"]
    assert 45 in div_res["noncoprime_c_f_divisors_explicitly_included"]

    # Explicit non-coprime gcd(c, f) > 1 test at e = 27 = 3 * 3^2 (c = 3, f = 3, gcd(c, f) = 3):
    r_27, c_27, f_27 = odd_squarefree_core_and_root(27)
    assert (r_27, c_27, f_27) == (0, 3, 3)
    assert squarefree_core_star(15, 3) == 5
    assert squarefree_core_star(5, 3) == 15

    tbl = compute_selberg_centered_remainder_table_fast_arb(64, prec_bits=288)
    fp16 = verify_five_piece_hilbert_and_feature_bound_at_Y16_arb(tbl, prec_bits=256)
    assert fp16["verified"] is True
    assert fp16["four_piece_beta_identity_exact"] is True
    assert fp16["all_omission_guards_strictly_nonzero"] is True
    assert fp16["station_feature_norm_inequality_all_n_le_32"] is True

    u_consts = compute_uniform_same_core_constants_arb(prec_bits=256)
    assert bool(u_consts["C_tau"].lower() > arb(1000))
    assert bool(u_consts["C_core"].lower() > u_consts["C_A"].upper() * arb("0.99"))
    assert bool(u_consts["C_square"].lower() > u_consts["C_core"].lower())

    sec3 = tc064_artifact["section_3_same_core_bound_and_divisor_support"]
    assert sec3["all_section_3_checks_pass"] is True
    assert len(sec3["same_core_and_rsquare_bound_rows"]) == 10


def test_tc064_deliverable_c_attempts_seen_diagnostics_and_deliverable_d(
    tc064_artifact: dict,
) -> None:
    sec4 = tc064_artifact[
        "section_4_distinct_core_attempts_seen_diagnostics_and_euler_robustness"
    ]
    assert sec4["all_section_4_checks_pass"] is True

    att1 = sec4["attempt_1_common_factor_coprime_and_scale_blocks"]
    c1a = att1["candidate_C1A_core_sector_nonpositivity"]
    assert c1a["outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert bool(arb(c1a["witness_Y16_g5"]["arb_ball_str"]).lower() > arb(0))
    assert bool(arb(c1a["witness_Y32_g7"]["arb_ball_str"]).lower() > arb(0))
    assert bool(arb(c1a["witness_seen_Y512_coprime_g1"]["arb_ball_str"]).lower() > arb(0))

    att2 = sec4["attempt_2_squarefree_prime_toggle_involution"]
    c2a = att2["candidate_C2A_toggle_pair_nonpositivity"]
    assert c2a["outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert bool(arb(c2a["witness_Y16_p3_a5"]["arb_ball_str"]).lower() > arb(0))
    assert bool(arb(c2a["witness_Y32_p3_a5"]["arb_ball_str"]).lower() > arb(0))

    seen = sec4["seen_scale_mechanism_diagnostics"]
    assert [r["Y"] for r in seen] == [512, 576, 960, 1408]
    for sr in seen:
        assert sr["exposure_role"] == "SEEN_DIAGNOSTIC_NOT_UNSEEN_HOLDOUT"
        assert sr["verified"] is True

    deliv_d = sec4["deliverable_d_finite_euler_factor_robustness"]
    assert deliv_d["verified"] is True
    assert deliv_d["exact_bidirectional_coeff_identities_n_le_600"] is True
    assert deliv_d["z_eq_1_removable_zero_limit_check"]["verified"] is True
    for er in deliv_d["restricted_Q_and_E_finite_flip_diagnostics"]:
        assert er["observable_scope"] == "RESTRICTED_TO_Q_AND_E_ONLY"


def test_tc064_section5_unseen_validation_and_adversarial_mutations(
    tc064_protocol: dict, tc064_artifact: dict, tmp_path: Path
) -> None:
    assert tc064_artifact["all_mathematical_and_numerical_checks_pass"] is True
    assert tc064_artifact["parent_subgate_status"] == "OPEN"
    assert tc064_artifact["rh_proved"] is False
    assert tc064_artifact["resource_compliance_status"] == "WITHIN"

    sec5 = tc064_artifact["section_5_unseen_validation_and_interval_splits"]
    assert sec5["all_section_5_checks_pass"] is True
    assert sec5["registered_unseen_point_count"] == 8
    assert sec5["evaluated_unseen_point_count"] == 8
    assert sec5["coverage_complete"] is True
    assert sec5["certification_integrity_ok"] is True

    outcomes = sec5["probe_global_outcomes"]
    assert outcomes["TC064-P0-CORE"] == "SURVIVED_TESTED_POINTS"
    assert outcomes["TC064-P-NEG-CORE"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert outcomes["KL1_same_core_square"] == "SURVIVED_TESTED_POINTS"
    assert outcomes["KL1_distinct_core"] == "SURVIVED_TESTED_POINTS"

    splits = sec5["continuous_interval_case_splits"]
    assert set(splits.keys()) == set(PRESCRIBED_TC064_INTERVAL_SPLITS.keys())
    assert len(splits["interval_54_55_to_54_80_across_e4_and_B3_mult5"]["branches"]) == 3
    assert len(splits["interval_146_75_to_147_35_across_T512_L5_and_C257"]["branches"]) == 4
    assert len(splits["interval_1296_pm_2_neg12_across_T7776"]["branches"]) == 2

    # --- Mutation 1: Deleted domain branch from continuous interval split ---
    mut_del_branch = copy.deepcopy(sec5)
    mut_del_branch["continuous_interval_case_splits"][
        "interval_146_75_to_147_35_across_T512_L5_and_C257"
    ]["branches"].pop()
    s5_m1, top_m1 = aggregate_tc064_section5_and_derive_outcomes(mut_del_branch, tc064_protocol)
    assert s5_m1["certification_integrity_ok"] is False
    assert top_m1["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert any(
        c["conflict_type"] == "DELETED_OR_EXTRA_INTERVAL_BRANCHES"
        for c in s5_m1["certification_integrity_conflicts"]
    )

    # --- Mutation 2: Wrong core map / tampered class-membership count & broken split ---
    mut_wrong_core = copy.deepcopy(sec5)
    mut_wrong_core["holdout_point_evaluations"][2]["squarefree_core_count_C_T"] += 1
    mut_wrong_core["holdout_point_evaluations"][2]["S_core_Y"] = serialize_arb_certified(arb(5))
    s5_m2, top_m2 = aggregate_tc064_section5_and_derive_outcomes(mut_wrong_core, tc064_protocol)
    assert s5_m2["certification_integrity_ok"] is False
    assert top_m2["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    ctypes_m2 = {c["conflict_type"] for c in s5_m2["certification_integrity_conflicts"]}
    assert "POINT_CUTOFF_OR_CORE_MAP_MISMATCH" in ctypes_m2
    assert "POINT_CORE_SPLIT_RECONSTRUCTION_CONFLICT" in ctypes_m2

    # --- Mutation 3: Reversed inequality direction on M_P0_CORE ---
    mut_rev = copy.deepcopy(sec5)
    pt0 = mut_rev["holdout_point_evaluations"][0]
    flint_ctx.prec = 256
    rev_margin = arb(pt0["log_Y_times_D_tilde"]["arb_ball_str"]) - arb(
        pt0["S_core_Y"]["arb_ball_str"]
    )
    pt0["M_P0_CORE"] = serialize_arb_certified(rev_margin)
    s5_m3, top_m3 = aggregate_tc064_section5_and_derive_outcomes(mut_rev, tc064_protocol)
    assert s5_m3["certification_integrity_ok"] is False
    assert top_m3["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert any(
        c["conflict_type"] == "POINT_MARGIN_OPERAND_MISMATCH_OR_REVERSED_INEQUALITY"
        for c in s5_m3["certification_integrity_conflicts"]
    )

    # --- Mutation 4: Shrunk binary domain without changing outward decimal Y_sub_ball ---
    mut_shrunk = copy.deepcopy(sec5)
    br0 = mut_shrunk["continuous_interval_case_splits"][
        "interval_54_55_to_54_80_across_e4_and_B3_mult5"
    ]["branches"][0]
    br0["evaluated_Y_interval_exact_fractions"] = ["873/16", "1747/32"]
    br0["evaluated_Y_mid_man_exp"] = [3493, -6]
    br0["evaluated_Y_rad_man_exp"] = [1, -6]
    s5_m4, top_m4 = aggregate_tc064_section5_and_derive_outcomes(mut_shrunk, tc064_protocol)
    assert s5_m4["certification_integrity_ok"] is False
    assert top_m4["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert any(
        c["conflict_type"] == "INCOMPLETE_BRANCH_BINARY_DOMAIN_COVERAGE"
        for c in s5_m4["certification_integrity_conflicts"]
    )

    mut_bad_manexp = copy.deepcopy(mut_shrunk)
    mut_bad_manexp["continuous_interval_case_splits"][
        "interval_54_55_to_54_80_across_e4_and_B3_mult5"
    ]["branches"][0]["evaluated_Y_mid_man_exp"] = [3495, -6]
    s5_m4b, _ = aggregate_tc064_section5_and_derive_outcomes(mut_bad_manexp, tc064_protocol)
    assert any(
        c["conflict_type"] == "BINARY_MAN_EXP_OR_ENCLOSURE_DOMAIN_MISMATCH"
        for c in s5_m4b["certification_integrity_conflicts"]
    )

    # --- Mutation 5: Deleted status key in artifact provenance comparison ---
    mut_del_status = copy.deepcopy(tc064_artifact)
    del mut_del_status["primary_log_saving_probe_outcome"]
    cmp_m5 = compare_tc064_artifacts_by_stable_key(mut_del_status, tc064_artifact)
    assert cmp_m5["comparison_status"] == "INCOMPLETE_MISSING_REQUIRED_STATUS_KEYS"
    assert "top.primary_log_saving_probe_outcome" in cmp_m5["missing_required_status_keys"]

    bad_art_p = tmp_path / "bad_status.json"
    bad_art_p.write_text(json.dumps(mut_del_status), encoding="utf-8")
    rep_m5 = reprocess_task_tc064_metadata_and_lean_audit(bad_art_p, write_output=False)
    assert rep_m5["all_mathematical_and_numerical_checks_pass"] is False
    assert rep_m5["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME


def test_tc064_lean_formalization_review_consistency_and_registers(
    tc064_artifact: dict, tmp_path: Path
) -> None:
    assert SQUAREFREE_CORE_LEAN_PATH.exists()
    assert SQUAREFREE_CORE_LEAN_REL in FORMAL_SOURCE_FILES
    assert SQUAREFREE_CORE_LEAN_REL in REQUIRED_FORMAL_SOURCES
    root_lean = (REPO_ROOT / "formal" / "RiemannScope.lean").read_text(encoding="utf-8")
    assert "import RiemannScope.SquarefreeCoreCorrelation" in root_lean

    sec6 = tc064_artifact["section_6_lean_audit_and_gate_accounting"]
    assert sec6["all_section_6_checks_pass"] is True
    la = sec6["lean_module_audit"]
    assert la["public_theorem_names"] == EXPECTED_TC064_THEOREMS
    assert la["sorry_or_admit_count"] == 0
    assert la["custom_axiom_count"] == 0
    assert la["banned_circle_tokens"] == []
    assert la["banned_non_grade_K_tokens"] == []
    assert la["formal_build_report_verified"] is True

    # Live review document consistency + adversarial report mutations:
    rev_chk = verify_tc064_review_document_consistency(tc064_artifact, TC_064_REVIEW_DOC_PATH)
    assert rev_chk["verified"] is True, rev_chk

    orig_md = TC_064_REVIEW_DOC_PATH.read_text(encoding="utf-8")

    # Report Mutation A: untagged interval
    bad_untagged = tmp_path / "untagged.md"
    bad_untagged.write_text(orig_md + "\nUntagged `[0.1234 +/- 1.0e-5]`.\n", encoding="utf-8")
    assert verify_tc064_review_document_consistency(tc064_artifact, bad_untagged)["verified"] is False

    # Report Mutation B: stale ball count & forbidden von Mangoldt conflation
    bad_stale = tmp_path / "stale.md"
    total_balls = str(tc064_artifact["serialized_arb_self_check"]["total_certified_arb_balls_checked"])
    bad_stale.write_text(
        orig_md.replace(total_balls, "999999") + "\n$\\sum \\Lambda(n)\\log n / n^{1+\\delta}$\n",
        encoding="utf-8",
    )
    res_stale = verify_tc064_review_document_consistency(tc064_artifact, bad_stale)
    assert res_stale["verified"] is False
    assert len(res_stale["stale_or_guardrail_errors"]) >= 2

    # Shared registers check:
    q_obj = json.loads((REPO_ROOT / ".agents" / "research" / "queue.json").read_text(encoding="utf-8"))
    assert q_obj["active_task_id"] == TASK_TC_064_ID
    s_obj = json.loads((REPO_ROOT / ".agents" / "research" / "state.json").read_text(encoding="utf-8"))
    assert s_obj.get("rh_proved", False) is False
