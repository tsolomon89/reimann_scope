"""Focused & adversarial test suite for TASK-TC-064:
Squarefree-Core Correlations and the Arithmetic Regularity Constraint (SUBGATE-TC-043A).
"""

from __future__ import annotations

import copy
from fractions import Fraction
import json
from pathlib import Path
import re

from flint import acb, arb, ctx as flint_ctx
import pytest

from certification import REQUIRED_FORMAL_SOURCES
from scripts.build_formal import FORMAL_SOURCE_FILES
from tc.canonical_theta_correlation_bound import REPO_ROOT, serialize_arb_certified
from tc.coupled_scale_energy_bootstrap import _tau_arb
from tc.dyadic_power_lift_primitive_correlation import is_perfect_square_int
from tc.joint_prime_dilation_signed_remainder import _parse_serialized_arb_enclosure_tc062
from tc.liouville_square_dilation import (
    evaluate_energy_kernel_K_Y_certified_arb,
    inflate_arb_with_nonneg_bound,
    liouville_lambda_int,
)
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
    PRESERVED_TC064_FORMAL_PRODUCER,
    PRESERVED_TC064_NUMERICAL_PRODUCER,
    REQUIRED_CURRENT_TC064_STATUS_KEYS,
    SQUAREFREE_CORE_ARTIFACT_PATH,
    SQUAREFREE_CORE_LEAN_PATH,
    SQUAREFREE_CORE_LEAN_REL,
    SQUAREFREE_CORE_PROTOCOL_PATH,
    TASK_TC_064_ID,
    TASK_TC_064R_ID,
    TC_064_REVIEW_DOC_PATH,
    aggregate_tc064_section5_and_derive_outcomes,
    canonical_cutoff_T_of_Y_exact,
    compare_tc064_artifacts_by_stable_key,
    compare_tc064_numerical_payloads_by_observable_key,
    compute_uniform_same_core_constants_arb,
    core_square_multipliers_B_a,
    odd_squarefree_common_factor_set,
    odd_squarefree_core_and_root,
    odd_squarefree_cores_C_T,
    prime_toggle_boundary_and_paired_partition,
    reprocess_task_tc064_metadata_and_lean_audit,
    resonant_squarefree_cores_C_res,
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

    # --- Mutation 5: Deleted or None/wrong-typed status key in artifact provenance comparison ---
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

    # None / wrong-typed status key (without del) must ALSO fail closed:
    mut_null_status = copy.deepcopy(tc064_artifact)
    mut_null_status["primary_log_saving_probe_outcome"] = None
    mut_null_status["section_5_unseen_validation_and_interval_splits"]["coverage_complete"] = "yes"
    cmp_m5b = compare_tc064_artifacts_by_stable_key(mut_null_status, tc064_artifact)
    assert cmp_m5b["comparison_status"] == "INCOMPLETE_MISSING_REQUIRED_STATUS_KEYS"
    assert "top.primary_log_saving_probe_outcome" in cmp_m5b["missing_required_status_keys"]
    assert "sec5.coverage_complete" in cmp_m5b["missing_required_status_keys"]

    null_art_p = tmp_path / "null_status.json"
    null_art_p.write_text(json.dumps(mut_null_status), encoding="utf-8")
    rep_m5b = reprocess_task_tc064_metadata_and_lean_audit(null_art_p, write_output=False)
    assert rep_m5b["all_mathematical_and_numerical_checks_pass"] is False
    assert rep_m5b["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME

    # --- Mutation 6: Fabricated branch M_RSQ_LOC (-999) on continuous interval ---
    mut_br_rsq = copy.deepcopy(sec5)
    fake_rsq_loc = serialize_arb_certified(arb(-999))
    sp_i1 = mut_br_rsq["continuous_interval_case_splits"][
        "interval_54_55_to_54_80_across_e4_and_B3_mult5"
    ]
    for br_i in sp_i1["branches"]:
        br_i["M_RSQ_LOC"] = fake_rsq_loc
    sp_i1["union_M_RSQ_LOC"] = fake_rsq_loc
    s5_m6, top_m6 = aggregate_tc064_section5_and_derive_outcomes(mut_br_rsq, tc064_protocol)
    assert s5_m6["certification_integrity_ok"] is False
    assert top_m6["holdout_hypothesis_outcome"] == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    assert any(
        c["conflict_type"] == "BRANCH_MARGIN_OPERAND_MISMATCH" and c.get("margin_key") == "M_RSQ_LOC"
        for c in s5_m6["certification_integrity_conflicts"]
    )


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
    assert rev_chk["tagged_and_checked_count"] == rev_chk["raw_tag_comment_count"] >= 130

    orig_md = TC_064_REVIEW_DOC_PATH.read_text(encoding="utf-8")

    # Report Mutation A1: untagged `[mid +/- rad]` interval
    bad_untagged = tmp_path / "untagged.md"
    bad_untagged.write_text(orig_md + "\nUntagged `[0.1234 +/- 1.0e-5]`.\n", encoding="utf-8")
    assert verify_tc064_review_document_consistency(tc064_artifact, bad_untagged)["verified"] is False

    # Report Mutation A2: untagged zero-centered `[+/- rad]` interval
    bad_untagged_zc = tmp_path / "untagged_zc.md"
    bad_untagged_zc.write_text(orig_md + "\nUntagged zero-centered `[+/- 1.23e-5]`.\n", encoding="utf-8")
    res_uzc = verify_tc064_review_document_consistency(tc064_artifact, bad_untagged_zc)
    assert res_uzc["verified"] is False
    assert "[+/- 1.23e-5]" in res_uzc["untagged_intervals"]

    # Report Mutation A3: shrunk zero-centered `[+/- rad]` tagged enclosure
    bad_shrunk_zc = tmp_path / "shrunk_zc.md"
    m_zc = next(
        m_hit
        for m_hit in (
            "[+/- 0.0439]",
            "[+/- 0.0508]",
        )
        if m_hit in orig_md
    )
    bad_shrunk_zc.write_text(orig_md.replace(m_zc, "[+/- 1.0e-99]", 1), encoding="utf-8")
    res_szc = verify_tc064_review_document_consistency(tc064_artifact, bad_shrunk_zc)
    assert res_szc["verified"] is False
    assert len(res_szc["failed_tags"]) >= 1

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
    q_ids = {t["task_id"] for t in q_obj["tasks"]}
    assert TASK_TC_064_ID in q_ids
    assert TASK_TC_064R_ID in q_ids
    assert q_obj["active_task_id"] in {TASK_TC_064_ID, TASK_TC_064R_ID, "TASK-TC-065", "TASK-TC-065R"}
    s_obj = json.loads((REPO_ROOT / ".agents" / "research" / "state.json").read_text(encoding="utf-8"))
    assert s_obj.get("rh_proved", False) is False


def test_tc064r_prime_toggle_boundary_partition_counterexample_and_strict_threshold() -> None:
    """Verify the corrected prime-toggle resonant-shell boundary identity from the actual
    core definitions `C(T)`, `C_p^pair(T)`, `C_p^bdry(T)`, `C_res(Y)`, and `T(Y) = ceil(Y^(5/4))`:
      1. Exact counterexample `Y = 256, T(256) = 1024, p = 7, a = 301 = 7 * 43`;
      2. Exact identity `C_p^bdry(T(Y)) cap C_res(Y) = {a in C_res(Y) : p nmid a}` and
         `C_p^pair(T(Y)) cap C_res(Y) = {a in C_res(Y) : p | a}` whenever `2*p*Y > T(Y)`;
      3. Strict-inequality and ceiling sensitivity (`Y = 1297, p = 3`; `Y = 1296 - 2^-12, p = 3`;
         `Y = 2500, p = 3`).
    """
    # 1. Exact counterexample to full-shell absorption: Y = 256, T = 1024, p = 7, a = 301 = 7 * 43
    T_256 = canonical_cutoff_T_of_Y_exact(256)
    assert T_256 == 1024
    assert 2 * 7 * 256 > T_256
    c_1024 = set(odd_squarefree_cores_C_T(T_256))
    c_res_256 = resonant_squarefree_cores_C_res(256, T_256)
    paired_7, bdry_7 = prime_toggle_boundary_and_paired_partition(7, T_256)
    assert set(paired_7).isdisjoint(bdry_7)
    assert sorted(paired_7 + bdry_7) == sorted(c_1024)

    assert 301 in c_res_256
    assert 301 == 7 * 43
    assert squarefree_core_star(301, 7) == 43
    assert 43 in c_1024
    assert 301 in paired_7
    assert 301 not in bdry_7

    # 2. Exact resonant-shell partition under strict inequality 2*p*Y > T(Y)
    for y_val, p_val in ((256, 7), (256, 3), (1295, 3)):
        t_y = canonical_cutoff_T_of_Y_exact(y_val)
        assert 2 * p_val * y_val > t_y
        c_res = resonant_squarefree_cores_C_res(y_val, t_y)
        paired_p, bdry_p = prime_toggle_boundary_and_paired_partition(p_val, t_y)
        bdry_res = [a for a in c_res if a in set(bdry_p)]
        paired_res = [a for a in c_res if a in set(paired_p)]
        copr_res = [a for a in c_res if a % p_val != 0]
        pdiv_res = [a for a in c_res if a % p_val == 0]
        assert len(copr_res) > 0 and len(pdiv_res) > 0
        assert bdry_res == copr_res
        assert paired_res == pdiv_res

    # 3a. Strict inequality necessity: at Y = 1297, p = 3, 2*3*1297 = 7782 <= 7784 = T(1297),
    #     so 3-coprime resonant core a = 1297 remains paired with 1297 star 3 = 3891 in C(7784).
    T_1297 = canonical_cutoff_T_of_Y_exact(1297)
    assert T_1297 == 7784
    assert 2 * 3 * 1297 <= T_1297
    c_res_1297 = resonant_squarefree_cores_C_res(1297, T_1297)
    paired_1297, bdry_1297 = prime_toggle_boundary_and_paired_partition(3, T_1297)
    assert 1297 in c_res_1297
    assert 1297 % 3 != 0
    assert squarefree_core_star(1297, 3) == 3891
    assert 3891 in odd_squarefree_cores_C_T(T_1297)
    assert 1297 in paired_1297 and 1297 not in bdry_1297
    assert len([a for a in c_res_1297 if a in set(bdry_1297)]) < len(
        [a for a in c_res_1297 if a % 3 != 0]
    )

    # 3b. Ceiling necessity vs asymptotic p ~ Y^(1/4)/2: at Y = 1296 - 2^-12, p = 3 satisfies
    #     p > Y^(1/4)/2 (since 16*3^4 = 1296 > Y), yet 2*3*Y < 7776 = ceil(Y^(5/4)).
    y_left = Fraction(5308415, 4096)
    T_left = canonical_cutoff_T_of_Y_exact(y_left)
    assert T_left == 7776
    assert y_left < Fraction(16 * (3 ** 4), 1)
    assert not (2 * 3 * y_left > T_left)

    # 3c. Interior counterexample when 2*p*Y < T(Y): Y = 2500, T = 17678, p = 3, a = 2501 = 41 * 61.
    T_2500 = canonical_cutoff_T_of_Y_exact(2500)
    assert T_2500 == 17678
    assert 2 * 3 * 2500 < T_2500
    paired_2500, bdry_2500 = prime_toggle_boundary_and_paired_partition(3, T_2500)
    assert 2501 in resonant_squarefree_cores_C_res(2500, T_2500)
    assert 2501 % 3 != 0
    assert 2501 in paired_2500 and 2501 not in bdry_2500


def test_tc064r_signed_log_gcd_outward_enclosures_and_dilation_identities(
    tc064_artifact: dict,
) -> None:
    """Verify:
      1. Outward serialized Arb enclosures (not merely midpoints) of the signed logarithmic-GCD
         identity RHS at Y in {16, 32, 64} are strictly negative (`c_hi < 0`), while the equality
         residuals enclose 0;
      2. Exact bare Gaussian ratio `phi_{p*n}(X)/phi_n(X) = p^(-3)*exp((1 - p^(-2))*X^2/n^2) > p^(-3)`
         on `[Y, tau*Y]`, and `p*a <= 6*Y < tau*Y` for `p = 3` and `a in [Y, 2*Y]`;
      3. Distinction between fixed square dilation (`b^(-2*(x+iy))` Dirichlet multiplier and
         `phi_{b^2*n}(X) = b^(-1)*phi_n(X/b^2)`), running-index squaring (`sum (n^2)^(-z) = zeta(2z)`
         on `x > 1/2`), and Liouville convolution (`1 * lambda = 1_square`, `zeta(z)*L_lambda(z) = zeta(2z)`).
    """
    sec4 = tc064_artifact[
        "section_4_distinct_core_attempts_seen_diagnostics_and_euler_robustness"
    ]
    sm_checks = sec4["attempt_1_common_factor_coprime_and_scale_blocks"][
        "small_scale_sector_and_log_gcd_checks"
    ]
    assert [r["Y"] for r in sm_checks] == [16, 32, 64]
    for row in sm_checks:
        p_rhs = _parse_serialized_arb_enclosure_tc062(row["log_gcd_identity_rhs"])
        p_lhs = _parse_serialized_arb_enclosure_tc062(row["log_gcd_identity_lhs"])
        p_res = _parse_serialized_arb_enclosure_tc062(row["log_gcd_identity_residual"])
        assert p_rhs is not None and p_lhs is not None and p_res is not None
        # Actual outward enclosure upper bound strictly negative (refutes "purely positive"):
        assert p_rhs["c_hi"] < 0
        assert p_lhs["c_hi"] < 0
        # Equality residual encloses 0 tightly:
        assert p_res["c_lo"] <= 0 <= p_res["c_hi"]
        assert max(abs(p_res["c_lo"]), abs(p_res["c_hi"])) < Fraction(1, 10 ** 60)
        if row["Y"] == 16:
            ref_y16 = Fraction("-0.0232162511649197014")
            assert abs(p_rhs["c_lo"] - ref_y16) < Fraction(1, 10 ** 18)
            assert abs(p_rhs["c_hi"] - ref_y16) < Fraction(1, 10 ** 18)

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau = _tau_arb()

        def _phi(n_val: int, X_val: arb) -> arb:
            na = arb(n_val)
            return (X_val ** (arb(5) / arb(2))) * (na ** (-3)) * (-(X_val * X_val) / (na * na)).exp()

        # Bare Gaussian ratio identity & strict > p^(-3) on [Y, tau*Y]:
        Y_sample = arb(100)
        assert bool((arb(6) * Y_sample < tau * Y_sample))  # p = 3, a <= 2Y stays inside [Y, tau*Y]
        for p_val in (3, 5, 7):
            for n_val in (100, 150, 200):
                for X_val in (Y_sample, arb(3) * Y_sample, tau * Y_sample):
                    lhs_ratio = _phi(p_val * n_val, X_val) / _phi(n_val, X_val)
                    rhs_ratio = (arb(p_val) ** (-3)) * (
                        (arb(1) - arb(p_val) ** (-2)) * (X_val * X_val) / (arb(n_val) ** 2)
                    ).exp()
                    assert lhs_ratio.overlaps(rhs_ratio)
                    assert bool(abs(lhs_ratio - rhs_ratio).upper() < arb("1e-55"))
                    assert bool(lhs_ratio.lower() > (arb(p_val) ** (-3)).upper())

        # Bare window norm ratio at Y = 100, a = 100, p = 3 exceeds 20 * 3^(-3):
        norm_100 = evaluate_energy_kernel_K_Y_certified_arb(100, 100, 100, prec_bits=256).sqrt()
        norm_300 = evaluate_energy_kernel_K_Y_certified_arb(100, 300, 300, prec_bits=256).sqrt()
        assert bool((norm_300 / norm_100).lower() > arb(20) * (arb(3) ** (-3)))

        # Fixed square dilation on Gaussian: phi_{b^2 * n}(X) = b^(-1) * phi_n(X / b^2)
        for b_val in (2, 3, 5):
            for n_val in (1, 3, 7):
                for X_val in (arb(5), arb(19)):
                    lhs_d = _phi(b_val * b_val * n_val, X_val)
                    rhs_d = (arb(b_val) ** (-1)) * _phi(n_val, X_val / arb(b_val * b_val))
                    assert lhs_d.overlaps(rhs_d)
                    assert bool(abs(lhs_d - rhs_d).upper() < arb("1e-60"))

        # Fixed square dilation on Dirichlet series gives scalar factor b^(-2*(x+iy)), NOT zeta(2z):
        z_dir = acb(arb(3), arb(2))
        b_fix = 3
        s_plain = sum((acb(liouville_lambda_int(n)) * (acb(n) ** (-z_dir)) for n in range(1, 121)), acb(0))
        s_dil = sum(
            (acb(liouville_lambda_int(n)) * (acb(b_fix * b_fix * n) ** (-z_dir)) for n in range(1, 121)),
            acb(0),
        )
        expected_dil = (acb(b_fix) ** (-acb(2) * z_dir)) * s_plain
        assert s_dil.real.overlaps(expected_dil.real) and s_dil.imag.overlaps(expected_dil.imag)
        assert bool(abs(s_dil - expected_dil).upper() < arb("1e-60"))

        # Running-index squaring sum (n^2)^(-z) = zeta(2z) converges on x = 3/4 in (1/2, 1):
        z_half = acb(arb(3) / arb(4), arb(5) / arb(2))
        N_sq = 800
        part_sq = sum((acb(n * n) ** (-z_half) for n in range(1, N_sq + 1)), acb(0))
        # Tail |sum_{n > N} n^(-2*x)| <= N^(1 - 2*x)/(2*x - 1) = 2 / sqrt(N)
        tail_sq = arb(2) / arb(N_sq).sqrt()
        encl_sq = acb(
            inflate_arb_with_nonneg_bound(part_sq.real, tail_sq),
            inflate_arb_with_nonneg_bound(part_sq.imag, tail_sq),
        )
        zeta_2z = (acb(2) * z_half).zeta()
        assert encl_sq.real.overlaps(zeta_2z.real) and encl_sq.imag.overlaps(zeta_2z.imag)

        # Liouville convolution 1 * lambda = 1_square (exact) & zeta(z)*L_lambda(z) = zeta(2z) (x > 1):
        for n_i in range(1, 401):
            conv_n = sum(liouville_lambda_int(d) for d in range(1, n_i + 1) if n_i % d == 0)
            assert conv_n == (1 if is_perfect_square_int(n_i) else 0)
        N_conv = 400
        l_part = sum((acb(liouville_lambda_int(n)) * (acb(n) ** (-z_dir)) for n in range(1, N_conv + 1)), acb(0))
        tail_l = (arb(N_conv) ** (-2)) / arb(2)
        l_encl = acb(
            inflate_arb_with_nonneg_bound(l_part.real, tail_l),
            inflate_arb_with_nonneg_bound(l_part.imag, tail_l),
        )
        prod_encl = z_dir.zeta() * l_encl
        z2_exact = (acb(2) * z_dir).zeta()
        assert prod_encl.real.overlaps(z2_exact.real) and prod_encl.imag.overlaps(z2_exact.imag)
    finally:
        flint_ctx.prec = saved


def test_tc064r_numerical_payload_preservation_and_reprocess_integrity(
    tc064_artifact: dict, tmp_path: Path
) -> None:
    """Verify TC-064R metadata repair preserves all 686 Arb balls, domains, cutoffs, and holdout
    classifications identically, keeps truthful numerical/formal producer commits, and catches
    regression of repaired overclaims in the review document.
    """
    assert tc064_artifact.get("repair_task_id") == TASK_TC_064R_ID
    prov = tc064_artifact["provenance"]
    assert prov["numerical_producing_git_commit"] == PRESERVED_TC064_NUMERICAL_PRODUCER
    assert prov["formal_producing_git_commit"] == PRESERVED_TC064_FORMAL_PRODUCER

    att2 = tc064_artifact[
        "section_4_distinct_core_attempts_seen_diagnostics_and_euler_robustness"
    ]["attempt_2_squarefree_prime_toggle_involution"]
    assert att2.get("full_profile_p_neg3_comparison_status") == "UNPROVED"

    # Reprocess in memory and verify 686/686 numerical payload identity:
    reproc = reprocess_task_tc064_metadata_and_lean_audit(
        SQUAREFREE_CORE_ARTIFACT_PATH, write_output=False
    )
    assert reproc["all_mathematical_and_numerical_checks_pass"] is True
    payload_cmp = compare_tc064_numerical_payloads_by_observable_key(reproc, tc064_artifact)
    assert payload_cmp["total_arb_keys_compared"] == 686
    assert payload_cmp["numerical_payloads_identical"] is True
    assert payload_cmp["changed_arb_keys"] == []
    assert payload_cmp["changed_domain_cutoff_or_classification_keys"] == []

    # Mutating a single Arb ball must be detected immediately by observable-key comparison:
    mut_art = copy.deepcopy(tc064_artifact)
    mut_art["section_5_unseen_validation_and_interval_splits"]["holdout_point_evaluations"][0][
        "S_core_Y"
    ]["mid_float"] += 1.0
    bad_cmp = compare_tc064_numerical_payloads_by_observable_key(mut_art, tc064_artifact)
    assert bad_cmp["numerical_payloads_identical"] is False
    assert len(bad_cmp["changed_arb_keys"]) == 1

    # Report consistency checker must reject re-introduction of repaired overclaims:
    orig_md = TC_064_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    bad_overclaim = tmp_path / "overclaim.md"
    bad_overclaim.write_text(
        orig_md + "\nRegression check: swallows the entire resonant shell and purely positive.\n",
        encoding="utf-8",
    )
    res_oc = verify_tc064_review_document_consistency(tc064_artifact, bad_overclaim)
    assert res_oc["verified"] is False
    assert len(res_oc["stale_or_guardrail_errors"]) >= 2
