"""Focused regression and falsification test suite for TASK-TC-062:
Joint Prime-Dilation Kernel and Uniform Signed-Remainder Proof Attempt
toward SUBGATE-TC-043A (EPIC-TC-042).

Validates:
1. Byte-level immutability of BOTH preserved `TC-061` protocol (`bc2f9f70...`) and frozen `TC-062`
   protocol (`4961b031...`), preserved `TC-060R2` and `TC-061R3` artifacts, `0` circle-half tokens,
   `0` non-grade `K_*` tokens, and honest `SUBGATE-TC-043A = OPEN` / `rh_proved = False`.
2. Pointwise reassembly `A_Y(X) = -sum_{n<=2T} beta_Y(n)*phi_n(X)/(log X)^2` and complete signed
   kernel identity `F(Y) = sum_{m,n=1}^{2T} lambda(m)*lambda(n)*Hcal_Y(m, n)` (retaining both
   `-4*D_tilde` and `-4*X_self`).
3. Generic 4-term and 16-term finite anchor reindexing on arbitrary non-multiplicative sequences
   and non-symmetric kernels, Liouville 1-prime and 2-prime decompositions with explicit boundary
   splits, exact 16-term diagonal coincidence classification, exact `c(m, n)` difference laws, and
   matched control prime-pair sign laws (`+` outside `S`, `-` inside `S`) + finite-grid refutations.
4. Independent closed-form and half-line quadrature verification of the 5 whole-line contraction
   enclosures `r({2})`, `r({3})`, `r({2,3})`, `r({2,3,5})`, `r({2})*r({3})` and strict ordering
   `r({2})*r({3}) < r({2}) < r({2,3}) < r({2,3,5})`.
5. Spillover fringe support `T < n <= T + floor(T/(D+1))`, `q`-reindexing `d_q = floor(T/q)`,
   `|w_{2,lambda}(n)| <= (log n)^2`, Stage A interior Hilbert identity, `m = 1` refutation of
   Candidate Lemma A1 + aggregate Replacement Lemma A1', `Y = 64` 256-bit Arb refutation of
   Candidate Lemma A2, Stage B large-prime `b_{pm} - b_m` jump law, and Stage C harmonic-weighted
   prime-family average.
6. Endpoint-faithful validation of the 10 unseen `TC-062` holdout points (without requiring
   conjecture truth for software tests to pass), continuous interval case-splits across `625^(5/4)`
   and `e^6`, escalation witness preservation, `CERTIFICATION_INTEGRITY_CONFLICT` blocking, and
   3-valued (`WITHIN`, `EXCEEDED`, `UNKNOWN`) `PROCESS_LIFETIME_HIGH_WATER_MARK` resource compliance.
7. Live Lean 4 theorem audit (`JointPrimeDilationSignedRemainder.lean`, 7 public theorems, `0`
   `sorry`/`admit`/custom axioms) and 100% displayed review interval & Lean line-anchor containment.
"""

from __future__ import annotations

from fractions import Fraction
import json
import re
from typing import Any, Dict, Tuple

from flint import arb, arf, ctx as flint_ctx
import pytest

from certification import REQUIRED_FORMAL_SOURCES
from scripts.build_formal import FORMAL_SOURCE_FILES
from tc.dyadic_power_lift_primitive_correlation import EPISTEMIC_CATEGORIES, PARENT_SUBGATE_ID
from tc.joint_prime_dilation_signed_remainder import (
    ACCEPTED_TC061R3_IMPLEMENTATION,
    ACCEPTED_TC061R3_TIP,
    BRANCH_ADMISSIBILITY_STATUSES,
    BRANCH_COVERAGE_STATUSES,
    EXPECTED_TC062_THEOREMS,
    FROZEN_TC062_PROTOCOL_ID,
    FROZEN_TC062_PROTOCOL_REGISTRATION_COMMIT,
    FROZEN_TC062_PROTOCOL_SHA256,
    GLOBAL_CONSEQUENCE_CLASSES,
    HISTORICAL_TC062R_BRANCH_OBSERVABLE_SHA256,
    HISTORICAL_TC062R_GENERATED_AT_UTC,
    JOINT_PRIME_DILATION_ARTIFACT_PATH,
    JOINT_PRIME_DILATION_PROTOCOL_PATH,
    REQUIRED_CURRENT_TC062_STATUS_KEYS,
    REVIEWED_TC062_IMPLEMENTATION,
    REVIEWED_TC062_PRODUCING_COMMIT,
    REVIEWED_TC062_TIP,
    REVIEWED_TC062R_DELIVERED_TIP,
    REVIEWED_TC062R_PRODUCING_COMMIT,
    REVIEWED_TC062R2_DELIVERED_TIP,
    REVIEWED_TC062R2_VALIDATION_COMMIT,
    REVIEWED_TC062R3_DELIVERED_TIP,
    REVIEWED_TC062R3_VALIDATION_COMMIT,
    TASK_TC_062_ID,
    TASK_TC_062R_ID,
    TASK_TC_062R2_ID,
    TASK_TC_062R3_ID,
    TASK_TC_062R4_ID,
    TC_062_LEAN_MODULE_PATH,
    TC_062_REVIEW_DOC_PATH,
    _load_git_json_artifact_or_none,
    _replay_historical_tc062r_sub_ball,
    aggregate_tc062_section5_and_derive_outcomes,
    audit_continuous_interval_split_certificate_tc062,
    build_complete_signed_kernel_evaluator_small_T,
    compare_tc062_artifacts_by_stable_key,
    compute_zone1_prime_power_diag_perturbation_tc062_arb,
    derive_exact_interval_cutoff_partition,
    derive_tc062_outcome_summaries,
    evaluate_interior_paired_matrix_free_arb,
    evaluate_whole_line_contraction_ratio_closed_arb,
    execute_tc062_holdout_point_with_escalation,
    extract_lean_declaration_spans_tc062,
    generate_task_tc062_artifact,
    prime_even_valuation_anchors,
    prime_valuation_v_p,
    reconstruct_tc062r_legacy_interval_domains,
    reprocess_task_tc062_metadata_and_stage_b,
    verify_anchor_diagonal_identities_and_self_collision_bounds_arb,
    verify_beta_four_piece_endpoint_and_summed_strip_bound_arb,
    verify_complete_kernel_unsigned_linear_growth_arb,
    verify_frozen_tc062_protocol_immutability,
    verify_generic_finite_anchor_reindexing_exact,
    verify_section_3_whole_line_contraction_obstruction,
    verify_stage_b_large_prime_b_jump_identity_arb,
    verify_tc062_review_enclosures_and_lean_anchors,
    verify_zone1_prime_power_majorant_repair_tc062_arb,
)
from tc.liouville_square_dilation import (
    _sci_or_latex_num_to_fraction,
    liouville_lambda_int,
)
from tc.mixed_arithmetic_covariance import (
    CERTIFICATION_INTEGRITY_CONFLICT_VERDICT,
    ExactScaleSpec,
    MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH,
    MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH,
    certify_exact_scale_cutoffs,
    compute_selberg_centered_remainder_table_fast_arb,
    load_frozen_protocol_rules,
    verify_frozen_protocol_immutability,
)
from tc.signed_dilation_arithmetic_energy import (
    SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH,
    verify_section_epistemic_scope_metadata,
)


@pytest.fixture(scope="module")
def tc062_artifact() -> Dict[str, Any]:
    assert JOINT_PRIME_DILATION_ARTIFACT_PATH.exists(), (
        f"Missing {JOINT_PRIME_DILATION_ARTIFACT_PATH}; run python tc/joint_prime_dilation_signed_remainder.py"
    )
    return json.loads(JOINT_PRIME_DILATION_ARTIFACT_PATH.read_text(encoding="utf-8"))


def test_tc062_protocols_immutability_hygiene_and_honest_gate_status(
    tc062_artifact: Dict[str, Any],
) -> None:
    """Verify preserved TC-061 and frozen TC-062 protocols, epistemic scopes, hygiene, and OPEN gate."""
    assert tc062_artifact["task_id"] == TASK_TC_062_ID
    assert tc062_artifact["parent_subgate"] == PARENT_SUBGATE_ID
    assert tc062_artifact["parent_subgate_status"] == "OPEN"
    assert tc062_artifact["rh_proved"] is False
    assert "global_consequence_class" not in tc062_artifact
    assert tc062_artifact["global_energy_improvement_claimed"] is False
    assert tc062_artifact["global_consequence_classes_enforced"] == list(GLOBAL_CONSEQUENCE_CLASSES)
    assert tc062_artifact["sampled_zeta_zeros_used"] == 0
    assert tc062_artifact["all_mathematical_and_numerical_checks_pass"] is True

    prov = tc062_artifact["provenance"]
    assert prov["accepted_tc061r3_tip"] == ACCEPTED_TC061R3_TIP
    assert prov["accepted_tc061r3_implementation"] == ACCEPTED_TC061R3_IMPLEMENTATION
    assert prov["frozen_tc062_protocol_registration_commit"] == FROZEN_TC062_PROTOCOL_REGISTRATION_COMMIT
    assert prov["frozen_tc062_protocol_sha256"] == FROZEN_TC062_PROTOCOL_SHA256

    chk_61 = verify_frozen_protocol_immutability()
    assert chk_61["verified"] is True
    chk_62 = verify_frozen_tc062_protocol_immutability()
    assert chk_62["verified"] is True
    assert chk_62["protocol_id"] == FROZEN_TC062_PROTOCOL_ID

    assert MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH.exists()
    assert SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH.exists()

    for key in (
        "section_1_protocols_reassembly_and_complete_kernel",
        "section_2_disjoint_prime_decompositions_and_controls",
        "section_3_whole_line_contraction_obstruction",
        "section_4_quantitative_proof_attempt",
        "section_5_unseen_validation_and_interval_splits",
        "section_6_lean_formalization_and_gate_accounting",
    ):
        ep_ok, ep_msg = verify_section_epistemic_scope_metadata(tc062_artifact[key])
        assert ep_ok is True, (key, ep_msg)
        for st in tc062_artifact[key]["epistemic_statuses"]:
            assert st in EPISTEMIC_CATEGORIES

    for p in (
        JOINT_PRIME_DILATION_PROTOCOL_PATH,
        JOINT_PRIME_DILATION_ARTIFACT_PATH,
    ):
        txt = p.read_text(encoding="utf-8")
        assert "\\pi" not in txt and "\u03c0" not in txt
        k_toks = [
            tok
            for tok in re.findall(r"\bK_[A-Za-z0-9_]+", txt)
            if tok != "K_reserved_for_real_algebraic_geometric_grades_A_R"
        ]
        assert k_toks == [], (p.name, k_toks)


def test_tc062_section_1_reassembly_and_complete_signed_kernel() -> None:
    """Independently verify pointwise A_Y reassembly and Hcal_Y assembly at Y = 4 (T = 6, N = 12)."""
    tbl = compute_selberg_centered_remainder_table_fast_arb(40, prec_bits=288)
    flint_ctx.prec = 256
    Hcal = build_complete_signed_kernel_evaluator_small_T(arb(4), 6, 1, tbl, prec_bits=256)
    assert Hcal(0, 1) == arb(0)
    assert Hcal(13, 2) == arb(0)
    for m in (1, 2, 5, 8, 12):
        for n in (1, 3, 6, 9, 12):
            diff = Hcal(m, n) - Hcal(n, m)
            assert diff == arb(0) or (arb(0) in diff and abs(diff) < arb("1e-48"))


def test_tc062_section_2_generic_reindexing_prime_pairs_and_control_signs(
    tc062_artifact: Dict[str, Any],
) -> None:
    """Verify generic reindexing on arbitrary kernels, 16-term diagonal coincidences, and control signs."""
    gen = verify_generic_finite_anchor_reindexing_exact()
    assert gen["verified"] is True

    sec2 = tc062_artifact["section_2_disjoint_prime_decompositions_and_controls"]
    assert sec2["all_section_2_checks_pass"] is True
    assert sec2["all_negative_controls_refuted_on_F_for_Y_ge_64"] is True

    # Check that outside-S primes require +1 pairing sign and that misapplied -1 pairing strictly fails:
    sign_rows = sec2["matched_control_prime_pair_sign_checks"]
    outside_rows = [r for r in sign_rows if not r["p_in_parity_set_S"]]
    assert len(outside_rows) >= 4
    for r in outside_rows:
        assert r["derived_pair_sign_eps_p"] == 1
        lo = _sci_or_latex_num_to_fraction(r["misapplied_all_minus_discrepancy"]["lower_dec"])
        hi = _sci_or_latex_num_to_fraction(r["misapplied_all_minus_discrepancy"]["upper_dec"])
        assert hi < 0 or lo > 0  # strictly nonzero discrepancy


def test_tc062_section_3_whole_line_enclosures_and_strict_ordering() -> None:
    """Independently check all 5 whole-line contraction enclosures and r({2,3}) > r({2})*r({3})."""
    r2 = evaluate_whole_line_contraction_ratio_closed_arb((2,))["r_S"]
    r3 = evaluate_whole_line_contraction_ratio_closed_arb((3,))["r_S"]
    r23 = evaluate_whole_line_contraction_ratio_closed_arb((2, 3))["r_S"]
    r235 = evaluate_whole_line_contraction_ratio_closed_arb((2, 3, 5))["r_S"]
    prod = r2 * r3

    assert bool(r2 >= arb("0.460304612664") and r2 <= arb("0.460304612665"))
    assert bool(r3 >= arb("0.758504658430") and r3 <= arb("0.758504658431"))
    assert bool(r23 >= arb("0.577474326597") and r23 <= arb("0.577474326598"))
    assert bool(r235 >= arb("0.706402204851") and r235 <= arb("0.706402204852"))
    assert bool(prod >= arb("0.349143193002") and prod <= arb("0.349143193003"))
    assert bool(prod < r2 and r2 < r23 and r23 < r235)


def test_tc062_section_4_spillover_fringe_and_candidates_a1_a2(
    tc062_artifact: Dict[str, Any],
) -> None:
    """Verify spillover fringe bound, Candidate A1 m=1 refutation, and Candidate A2 Y=64 refutation."""
    sec4 = tc062_artifact["section_4_quantitative_proof_attempt"]
    assert sec4["all_section_4_checks_pass"] is True
    assert sec4["selberg_w2_pointwise_log_sq_bound_1_to_2000_verified"] is True

    # At Y = 4096 (T = 32768, D = 8), fringe upper bound is 32768 + floor(32768/9) = 36408 << 65536:
    row_4096 = next(r for r in sec4["spillover_fringe_and_young_reduction_rows"] if r["Y"] == 4096)
    assert row_4096["proved_fringe_upper_bound"] == 36408
    assert row_4096["max_nonzero_spillover_index"] <= 36408

    c_a1 = sec4["candidate_a1_pointwise_anchor_diagonal_refutation_and_replacement"]
    assert c_a1["verdict"] == "REFUTED_WITHIN_SCOPE"
    for r in c_a1["rows"]:
        lo = _sci_or_latex_num_to_fraction(r["m1_p2_Delta_Hcal_1_1"]["lower_dec"])
        assert lo > 0

    c_a2 = sec4["candidate_a2_unsigned_paired_block_majorant_refutation"]
    assert c_a2["verdict"] == "REFUTED_BY_CERTIFIED_WITNESS"
    lo_m = _sci_or_latex_num_to_fraction(c_a2["margin_Y64"]["lower_dec"])
    assert lo_m > 0

    b_jump = sec4["stage_b_large_prime_b_jump_audit"]
    assert b_jump["verified"] is True
    assert b_jump["general_all_m_identity_verified"] is True
    assert b_jump["odd_valuation_discrepancy_certified"] is True
    live_b_jump = verify_stage_b_large_prime_b_jump_identity_arb(T_chk=182, D_chk=4, primes=(7, 11, 13))
    assert live_b_jump["verified"] is True
    assert [w["m"] for w in live_b_jump["odd_valuation_discrepancy_witnesses"]] == [7, 14, 21]


def test_tc062_section_5_unseen_holdouts_witness_preservation_and_resource_semantics(
    tc062_artifact: Dict[str, Any],
) -> None:
    """Re-parse recorded unseen holdout margins without assuming conjecture truth, and test
    witness preservation, conflict fail-closed behavior, and 3-valued resource semantics.
    """
    sec5 = tc062_artifact["section_5_unseen_validation_and_interval_splits"]
    assert sec5["registered_unseen_point_count"] == 10
    assert sec5["evaluated_unseen_point_count"] == 10
    assert sec5["coverage_complete"] is True
    assert sec5["certification_integrity_ok"] is True

    # Never report PROVED_UNIFORMLY from a finite grid:
    for cid, out_str in sec5["global_candidate_outcomes"].items():
        assert out_str != "PROVED_UNIFORMLY", cid
        assert out_str in ("SURVIVED_TESTED_POINTS", "REFUTED_BY_CERTIFIED_WITNESS", "UNRESOLVED/INCOMPLETE_COVERAGE")

    for row in sec5["holdout_point_evaluations"]:
        assert row["prior_exposure_status"] == "UNSEEN_FOR_ALL_OBSERVABLES"
        rc = row["resource_budget_check"]
        assert rc["wall_budget_status"] == "WITHIN"
        assert rc["memory_budget_status"] == "WITHIN"
        for pid, pdata in row["last_tier_probe_evaluations"]["per_probe"].items():
            lo = _sci_or_latex_num_to_fraction(pdata["margin_M_Y"]["lower_dec"])
            hi = _sci_or_latex_num_to_fraction(pdata["margin_M_Y"]["upper_dec"])
            if hi <= 0:
                assert pdata["point_verdict"] == "PASS"
            elif lo > 0:
                assert pdata["point_verdict"] == "FAIL"
            else:
                assert pdata["point_verdict"] == "UNRESOLVED"

    # Synthetic runner tests:
    # (a) Decisive FAIL witness at Tier 0 preserved when Tier 1 returns UNRESOLVED, + TIER_LOCAL_SNAPSHOT -> UNKNOWN RSS:
    proto = json.loads(JOINT_PRIME_DILATION_PROTOCOL_PATH.read_text(encoding="utf-8"))
    probes = proto["frozen_candidate_probes"]
    rules = proto["numerical_settings_and_escalation_rules"]
    tbl_small = compute_selberg_centered_remainder_table_fast_arb(400, prec_bits=288)
    sp_112 = ExactScaleSpec("112", "exact_rational", Fraction(112, 1))

    def _mock_eval_preserve(spec, *, tier: int, resolved_settings):
        cut = {"T_Y": 365, "D0_raw": 4, "D0_eff": 4, "ceil_tau_Y": 704}
        if tier == 0:
            # TC062-P0-F fails (+0.5 > 0.1), TC062-P0-INT2 straddles zero (triggers escalation):
            return {
                "cutoffs": cut,
                "observables": {
                    "Y_arb": arb(112),
                    "E_Y": arb("0.02"),
                    "D_tilde_Y": arb("0.03"),
                    "X_self_Y": arb("0.001"),
                    "J_Y": arb("0.504"),
                    "F_Y": arb("0.50"),
                    "F_int_T_p2": arb("0.14155") + arb(0, arb("0.01")),  # straddles log(112)*0.03 ~= 0.14155
                    "diag_int_T_p2": arb("-0.10"),
                    "offdiag_int_T_p2": arb("-0.01"),
                    "F_bnd_T_p2": arb("0.35"),
                    "F_int_T_p23": arb("-0.02"),
                    "diag_int_T_p23": arb("-0.03"),
                    "offdiag_int_T_p23": arb("0.01"),
                    "F_bnd_T_p23": arb("0.52"),
                    "log_Y_times_D_tilde": arb("0.14155"),
                },
            }
        # Tier >= 1: everything straddles zero!
        z_strad = arb(0, arb("1.0"))
        return {
            "cutoffs": cut,
            "observables": {
                "Y_arb": arb(112),
                "E_Y": arb("0.02"),
                "D_tilde_Y": arb("0.03"),
                "X_self_Y": arb("0.001"),
                "J_Y": z_strad,
                "F_Y": z_strad,
                "F_int_T_p2": z_strad,
                "diag_int_T_p2": z_strad,
                "offdiag_int_T_p2": z_strad,
                "F_bnd_T_p2": z_strad,
                "F_int_T_p23": z_strad,
                "diag_int_T_p23": z_strad,
                "offdiag_int_T_p23": z_strad,
                "F_bnd_T_p23": z_strad,
                "log_Y_times_D_tilde": arb("0.14155"),
            },
        }

    res_pres = execute_tc062_holdout_point_with_escalation(
        "MOCK-112",
        sp_112,
        probes,
        rules,
        selberg_table=tbl_small,
        evaluator_fn=_mock_eval_preserve,
        rss_fn=lambda: {
            "current_rss_mb": 200.0,
            "peak_rss_mb": 200.0,
            "peak_rss_measurement_semantics": "TIER_LOCAL_SNAPSHOT",
        },
    )
    assert res_pres["final_tier_used"] == 2
    assert res_pres["accumulated_candidate_verdicts"]["TC062-P0-F"] == "FAIL"
    assert res_pres["decisive_witnesses"]["TC062-P0-F"]["deciding_tier"] == 0
    assert res_pres["accumulated_candidate_verdicts"]["TC062-P0-INT2"] == "UNRESOLVED"
    # Under-limit TIER_LOCAL_SNAPSHOT must report UNKNOWN memory compliance, not WITHIN:
    assert res_pres["resource_budget_check"]["memory_budget_status"] == "UNKNOWN"

    # (b) Contradictory PASS vs FAIL across tiers must flag CERTIFICATION_INTEGRITY_CONFLICT:
    def _mock_eval_conflict(spec, *, tier: int, resolved_settings):
        cut = {"T_Y": 365, "D0_raw": 4, "D0_eff": 4, "ceil_tau_Y": 704}
        f_val = arb("-0.10") if tier == 0 else arb("0.90")
        int2_val = arb("0.14155") + arb(0, arb("0.01")) if tier == 0 else arb("-0.10")
        return {
            "cutoffs": cut,
            "observables": {
                "Y_arb": arb(112),
                "E_Y": arb("0.02"),
                "D_tilde_Y": arb("0.03"),
                "X_self_Y": arb("0.001"),
                "J_Y": f_val,
                "F_Y": f_val,
                "F_int_T_p2": int2_val,
                "diag_int_T_p2": arb("-0.10"),
                "offdiag_int_T_p2": arb("-0.01"),
                "F_bnd_T_p2": arb("0.0"),
                "F_int_T_p23": arb("-0.02"),
                "diag_int_T_p23": arb("-0.03"),
                "offdiag_int_T_p23": arb("0.01"),
                "F_bnd_T_p23": arb("0.0"),
                "log_Y_times_D_tilde": arb("0.14155"),
            },
        }

    res_conf = execute_tc062_holdout_point_with_escalation(
        "MOCK-CONFLICT",
        sp_112,
        probes,
        rules,
        selberg_table=tbl_small,
        evaluator_fn=_mock_eval_conflict,
    )
    assert res_conf["certification_integrity_ok"] is False
    assert (
        res_conf["accumulated_candidate_verdicts"]["TC062-P0-F"]
        == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
    )


def test_tc062_lean_formalization_registration_and_review_synchronization(
    tc062_artifact: Dict[str, Any],
) -> None:
    """Verify Lean 4 module registration, 8 public theorems, 0 sorry/admit/axioms, and review sync."""
    rel_lean = "formal/RiemannScope/JointPrimeDilationSignedRemainder.lean"
    assert rel_lean in FORMAL_SOURCE_FILES
    assert rel_lean in REQUIRED_FORMAL_SOURCES
    assert TC_062_LEAN_MODULE_PATH.exists()

    assert len(EXPECTED_TC062_THEOREMS) == 8
    spans = extract_lean_declaration_spans_tc062()
    assert spans["hygiene_ok"] is True, spans
    assert spans["public_theorem_count"] == len(EXPECTED_TC062_THEOREMS)

    assert tc062_artifact["repair_task_id"] == TASK_TC_062R4_ID
    assert tc062_artifact["prior_repair_task_id"] == TASK_TC_062R3_ID
    prov = tc062_artifact["provenance"]
    assert prov["reviewed_tc062_tip"] == REVIEWED_TC062_TIP
    assert prov["reviewed_tc062_implementation"] == REVIEWED_TC062_IMPLEMENTATION
    assert prov["prior_tc062_producing_commit"] == REVIEWED_TC062_PRODUCING_COMMIT
    assert prov["reviewed_tc062r_delivered_tip"] == REVIEWED_TC062R_DELIVERED_TIP
    assert prov["reviewed_tc062r_producing_commit"] == REVIEWED_TC062R_PRODUCING_COMMIT
    assert prov["reviewed_tc062r2_delivered_tip"] == REVIEWED_TC062R2_DELIVERED_TIP
    assert prov["reviewed_tc062r2_validation_commit"] == REVIEWED_TC062R2_VALIDATION_COMMIT
    assert prov["reviewed_tc062r3_delivered_tip"] == REVIEWED_TC062R3_DELIVERED_TIP
    assert prov["reviewed_tc062r3_validation_commit"] == REVIEWED_TC062R3_VALIDATION_COMMIT
    comp_r4_as_sup = prov["tc062r4_validation_and_verdict_comparison"]
    assert comp_r4_as_sup["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert comp_r4_as_sup["enclosure_comparison_complete"] is True
    assert comp_r4_as_sup["any_numerical_enclosure_changed_on_comparable_balls"] is False
    assert comp_r4_as_sup["changed_numerical_enclosures_count"] == 0
    assert comp_r4_as_sup["changed_mathematical_verdicts_count"] == 0
    assert comp_r4_as_sup["raw_branch_margin_sign_verdicts_changed_count"] == 0
    assert comp_r4_as_sup["branch_coverage_classifications_changed_count"] == 5
    assert comp_r4_as_sup["any_integrity_coverage_or_execution_classification_changed"] is True
    comp_r4_post = prov["tc062r4_post_domain_recovery_verdict_comparison"]
    assert comp_r4_post["comparison_status"] == "COMPLETE_COMPARED"
    assert comp_r4_post["any_probe_kl1_control_or_candidate_verdict_changed"] is False
    assert comp_r4_post["any_numerical_enclosure_changed"] is False
    assert prov["formal_compiled_theorem_count"] == 830
    assert prov["formal_build_producing_git_commit"] == prov["numerical_producing_git_commit"]
    inv62 = prov["tc062r_certificate_impact_inventory"]
    assert inv62["policy"] == "OPTION_A_FULL_RECOMPUTATION_WITH_REPAIRED_ZONE1_EVALUATORS"
    assert inv62["prior_tc062_baseline_commit"] == REVIEWED_TC062_TIP
    assert inv62["recomputed_producing_git_commit"] == prov["numerical_producing_git_commit"]
    assert inv62["candidate_a2_Y64_counterexample_unaffected"] is True
    assert inv62["raw_branch_margin_sign_verdicts_changed_count"] == 0
    assert inv62["stable_key_verdict_comparison_v2"]["changed_mathematical_verdicts_count"] == 0
    assert sum(inv62["overall_ball_status_counts"].values()) == inv62["total_artifact_arb_balls"]

    assert TC_062_REVIEW_DOC_PATH.exists()
    rev_chk = verify_tc062_review_enclosures_and_lean_anchors(
        tc062_artifact, TC_062_REVIEW_DOC_PATH, lean_spans=spans
    )
    assert rev_chk["verified"] is True, rev_chk
    assert rev_chk["checked_holdout_cutoff_count"] == 10
    assert rev_chk["failed_holdout_cutoffs"] == []


def test_tc062r_zone1_prime_power_majorant_repair_and_permutations() -> None:
    """Verify TASK-TC-062R §2: omitted-prime-power reproduction at Y=224 (n0=18), complete
    reference agreement at n0=0..32 (including n0=3, 9, 18), permutation invariance, Arb panel
    vector-norm enclosure, and repaired 3-zone vs unsplit agreement at Y=224.
    """
    audit = verify_zone1_prime_power_majorant_repair_tc062_arb(prec_bits=256)
    assert audit["verified"] is True, audit
    assert audit["reproduced_Y224_n0_18_visited_buggy"] == [2, 4, 8, 16]
    assert audit["reproduced_Y224_n0_18_omitted_buggy"] == [3, 9, 5, 7, 11, 13, 17]
    assert audit["reference_and_permutation_invariance_verified"] is True
    assert audit["panel_signed_vector_norm_enclosure_Y224_verified"] is True
    assert audit["repaired_three_zone_vs_unsplit_Y224_verified"] is True

    # Explicit boundary check at n0 = 3 where (2,2)->4 > 3 preceded (3,1)->3 in prime_power_pairs_up_to:
    flint_ctx.prec = 256
    pp_unsorted = [(2, 10, arb(2).log() ** 2), (4, 5, arb(2).log() ** 2), (3, 6, arb(3).log() ** 2)]
    phi_demo = [arb(0), arb("1.0"), arb("0.5"), arb("0.25"), arb("0.125")]
    v_n0_0 = compute_zone1_prime_power_diag_perturbation_tc062_arb(
        pp_unsorted, 0, phi_demo, arb(1), arb(2)
    )
    v_n0_1 = compute_zone1_prime_power_diag_perturbation_tc062_arb(
        pp_unsorted, 1, phi_demo, arb(1), arb(2)
    )
    assert v_n0_0 == arb(0) and v_n0_1 == arb(0)
    v_n0_3 = compute_zone1_prime_power_diag_perturbation_tc062_arb(
        pp_unsorted, 3, phi_demo, arb(1), arb(2)
    )
    expected_n0_3 = (arb(1) / arb(2)) * (
        (arb(2).log() ** 2) * (arb("0.5") ** 2) + (arb(3).log() ** 2) * (arb("0.25") ** 2)
    ).sqrt()
    assert arb(0) in (v_n0_3 - expected_n0_3) and abs(v_n0_3 - expected_n0_3) < arb("1e-70")


def test_tc062r_anchor_diagonal_identities_young_bounds_and_complete_omega_Y(
    tc062_artifact: Dict[str, Any],
) -> None:
    """Verify TASK-TC-062R §§3, 4, 5, 7A, 7B, 7C, 7D repairs in code and generated artifact."""
    diag_chk = verify_anchor_diagonal_identities_and_self_collision_bounds_arb(prec_bits=256)
    assert diag_chk["verified"] is True, diag_chk
    assert diag_chk["retired_erroneous_578_15_log_tau_gt_64"] is True
    # At m = 3, p = 2 (Y = 8) and m = 33, p = 2 (Y = 64), omitting -4*c(m,m)*[...] strictly fails:
    for key_d in (
        "m3_p2_abbreviated_formula_discrepancy_Y8",
        "m33_p2_abbreviated_formula_discrepancy_Y64",
    ):
        disc_lo = _sci_or_latex_num_to_fraction(diag_chk[key_d]["lower_dec"])
        disc_hi = _sci_or_latex_num_to_fraction(diag_chk[key_d]["upper_dec"])
        assert disc_hi < 0 or disc_lo > 0

    # Verify 4 * X_self sharp bound (289/15)*log(tau) < (1377/40)*log(tau) < 64:
    hi_289_15 = _sci_or_latex_num_to_fraction(
        diag_chk["four_X_self_sharp_bound_289_15_log_tau"]["upper_dec"]
    )
    hi_1377_40 = _sci_or_latex_num_to_fraction(
        diag_chk["four_X_self_envelope_bound_1377_40_log_tau"]["upper_dec"]
    )
    assert hi_289_15 < Fraction(36, 1) < hi_1377_40 < Fraction(64, 1)

    # Verify complete-kernel Omega(Y) lower-bound proof audit (avoiding X = 2*sqrt(log 2)*m):
    omega_chk = verify_complete_kernel_unsigned_linear_growth_arb(prec_bits=256)
    assert omega_chk["verified"] is True, omega_chk
    bilin_lo = _sci_or_latex_num_to_fraction(
        omega_chk["odd_resonant_band_bilinear_lower_bound_Y256"]["lower_dec"]
    )
    assert bilin_lo > 0

    # Check Section 3 explicit separation of analytic Gaussian integral from Lean Theorem 4:
    sec3_live = verify_section_3_whole_line_contraction_obstruction(prec_bits=256)
    assert sec3_live["all_section_3_checks_pass"] is True
    assert "ANALYTIC_PROVED_OUTSIDE_LEAN" in sec3_live["epistemic_statuses"]
    assert (
        sec3_live["component_epistemic_map"][
            "improper_halfline_gaussian_integral_to_wholeLineGaussianGram_bridge"
        ]
        == "ANALYTIC_PROVED_OUTSIDE_LEAN"
    )
    sec3 = tc062_artifact["section_3_whole_line_contraction_obstruction"]
    assert "ANALYTIC_PROVED_OUTSIDE_LEAN" in sec3["epistemic_statuses"]
    assert (
        sec3["component_epistemic_map"][
            "improper_halfline_gaussian_integral_to_wholeLineGaussianGram_bridge"
        ]
        == "ANALYTIC_PROVED_OUTSIDE_LEAN"
    )

    # Check Section 4 Young boundary accounting & absence of retired false claims:
    sec4 = tc062_artifact["section_4_quantitative_proof_attempt"]
    yb = sec4["uncovered_young_boundary_accounting"]
    assert "delta * D_tilde(Y)" in yb["exact_lean_young_inequalities"]["forward_bound"]
    assert "1 + 1 / delta" in yb["exact_lean_young_inequalities"]["reverse_bound"]


def test_tc062r_shared_outcome_derivation_and_adversarial_scenarios(
    tc062_artifact: Dict[str, Any], tmp_path
) -> None:
    """Test BOTH `generate_task_tc062_artifact` and `reprocess_task_tc062_metadata_and_stage_b`
    across all 7 required TASK-TC-062R §6 scenarios:
    1. Complete all-pass coverage;
    2. One certified failure (completed evaluation, never HOLDOUT_SURVIVAL);
    3. Unresolved zero-straddling evidence;
    4. Empty coverage, missing/duplicate/unregistered point IDs, missing candidate entries,
       and applicable-domain violations;
    5. Contradictory certificates (cross-tier conflict and tampered margin-vs-verdict mismatch);
    6. Missing or non-covering (`TIER_LOCAL_SNAPSHOT`) memory measurements;
    7. Prior decisive failure at Tier 0 followed by unresolved escalation at Tiers 1..2.
    """
    from tc.canonical_theta_correlation_bound import serialize_arb_certified
    from tc.mixed_arithmetic_covariance import strip_enclosure_arb_for_json

    pre_1_4 = (
        tc062_artifact["section_1_protocols_reassembly_and_complete_kernel"],
        tc062_artifact["section_2_disjoint_prime_decompositions_and_controls"],
        tc062_artifact["section_3_whole_line_contraction_obstruction"],
        tc062_artifact["section_4_quantitative_proof_attempt"],
    )

    def _run_both_paths(mutated_sec5: Dict[str, Any], **ovr_kwargs: Any) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        gen_out = generate_task_tc062_artifact(
            write_output=False,
            precomputed_sections_1_to_4=pre_1_4,
            section_5_override=mutated_sec5,
            **ovr_kwargs,
        )
        synth_art = json.loads(json.dumps(tc062_artifact))
        synth_art["section_5_unseen_validation_and_interval_splits"] = json.loads(
            json.dumps(mutated_sec5)
        )
        p_tmp = tmp_path / "synth_tc062.json"
        p_tmp.write_text(json.dumps(synth_art), encoding="utf-8")
        rep_out = reprocess_task_tc062_metadata_and_stage_b(
            p_tmp,
            write_output=False,
            holdout_entries_override=ovr_kwargs.get("holdout_entries_override"),
        )
        assert gen_out["completion_outcome_code"] == rep_out["completion_outcome_code"]
        assert gen_out["research_outcome_class"] == rep_out["research_outcome_class"]
        assert gen_out["holdout_hypothesis_outcome"] == rep_out["holdout_hypothesis_outcome"]
        assert gen_out["resource_compliance_status"] == rep_out["resource_compliance_status"]
        assert (
            gen_out["execution_and_certification_status"]
            == rep_out["execution_and_certification_status"]
        )
        assert (
            gen_out["all_mathematical_and_numerical_checks_pass"]
            == rep_out["all_mathematical_and_numerical_checks_pass"]
        )
        assert (
            gen_out["section_5_unseen_validation_and_interval_splits"]["all_section_5_checks_pass"]
            == rep_out["section_5_unseen_validation_and_interval_splits"]["all_section_5_checks_pass"]
        )
        assert (
            gen_out["section_5_unseen_validation_and_interval_splits"][
                "six_dimension_closeout_audit"
            ]
            == rep_out["section_5_unseen_validation_and_interval_splits"][
                "six_dimension_closeout_audit"
            ]
        )
        return gen_out, rep_out

    # Scenario 1: Complete all-pass coverage
    s1 = json.loads(json.dumps(tc062_artifact["section_5_unseen_validation_and_interval_splits"]))
    g1, _ = _run_both_paths(s1)
    assert g1["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert g1["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"
    assert g1["resource_compliance_status"] == "WITHIN"
    assert "HOLDOUT_SURVIVAL" in g1["completion_outcome_code"]
    assert g1["all_mathematical_and_numerical_checks_pass"] is True

    # Scenario 2: One certified failure (must be CERTIFIED_EVALUATION_COMPLETE, NEVER survival!)
    flint_ctx.prec = 256
    pos_margin = strip_enclosure_arb_for_json(serialize_arb_certified(arb("0.25")))
    s2 = json.loads(json.dumps(s1))
    r0 = s2["holdout_point_evaluations"][0]
    r0["accumulated_candidate_verdicts"]["TC062-P-NEG-INT2"] = "FAIL"
    r0["decisive_witnesses"]["TC062-P-NEG-INT2"]["verdict"] = "FAIL"
    r0["decisive_witnesses"]["TC062-P-NEG-INT2"]["certified_margin_enclosure"] = pos_margin
    r0["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["point_verdict"] = "FAIL"
    r0["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["margin_M_Y"] = pos_margin
    g2, _ = _run_both_paths(s2)
    assert g2["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert g2["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"
    assert "SURVIVAL" not in g2["completion_outcome_code"]
    assert "SURVIVED" not in g2["research_outcome_class"]
    assert g2["all_mathematical_and_numerical_checks_pass"] is True

    # Scenario 3: Unresolved zero-straddling evidence
    strad_margin = strip_enclosure_arb_for_json(serialize_arb_certified(arb(0, arb("0.01"))))
    s3 = json.loads(json.dumps(s1))
    r3 = s3["holdout_point_evaluations"][2]
    r3["accumulated_candidate_verdicts"]["TC062-P0-INT2"] = "UNRESOLVED"
    r3["decisive_witnesses"]["TC062-P0-INT2"] = None
    r3["last_tier_probe_evaluations"]["per_probe"]["TC062-P0-INT2"]["point_verdict"] = "UNRESOLVED"
    r3["last_tier_probe_evaluations"]["per_probe"]["TC062-P0-INT2"]["margin_M_Y"] = strad_margin
    g3, _ = _run_both_paths(s3)
    assert g3["holdout_hypothesis_outcome"] == "UNRESOLVED_EVIDENCE"
    assert "SURVIVAL" not in g3["completion_outcome_code"]
    assert "SURVIVED" not in g3["research_outcome_class"]
    assert g3["all_mathematical_and_numerical_checks_pass"] is False

    # Scenario 4: Empty coverage, missing/duplicate/unregistered point IDs, missing candidate entries,
    #             and applicable-domain violation
    s_empty = json.loads(json.dumps(s1))
    s_empty["holdout_point_evaluations"] = []
    g_emp_sched, _ = _run_both_paths(s_empty, holdout_entries_override=[])
    assert g_emp_sched["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert "SURVIVAL" not in g_emp_sched["completion_outcome_code"]

    g_emp_rows, _ = _run_both_paths(s_empty)
    assert g_emp_rows["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert "SURVIVAL" not in g_emp_rows["completion_outcome_code"]

    s_miss_pt = json.loads(json.dumps(s1))
    s_miss_pt["holdout_point_evaluations"].pop()
    g_mp, _ = _run_both_paths(s_miss_pt)
    assert g_mp["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    s_dup_pt = json.loads(json.dumps(s1))
    s_dup_pt["holdout_point_evaluations"][-1] = json.loads(
        json.dumps(s_dup_pt["holdout_point_evaluations"][0])
    )
    g_dp, _ = _run_both_paths(s_dup_pt)
    assert g_dp["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    s_unreg = json.loads(json.dumps(s1))
    s_unreg["holdout_point_evaluations"][0]["point_id"] = "TC062-HO-UNREGISTERED-999"
    g_ur, _ = _run_both_paths(s_unreg)
    assert g_ur["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    s_miss_cand = json.loads(json.dumps(s1))
    del s_miss_cand["holdout_point_evaluations"][0]["accumulated_candidate_verdicts"][
        "KL1_int2_offdiag"
    ]
    g_mc, _ = _run_both_paths(s_miss_cand)
    assert g_mc["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert (
        g_mc["section_5_unseen_validation_and_interval_splits"]["global_candidate_outcomes"][
            "KL1_int2_offdiag"
        ]
        == "UNRESOLVED/INCOMPLETE_COVERAGE"
    )
    assert "SURVIVAL" not in g_mc["completion_outcome_code"]

    s_dom_viol = json.loads(json.dumps(s1))
    s_dom_viol["holdout_point_evaluations"][0]["accumulated_candidate_verdicts"][
        "TC062-P0-F"
    ] = "NOT_EVALUATED"
    s_dom_viol["holdout_point_evaluations"][0]["decisive_witnesses"]["TC062-P0-F"] = None
    g_dv, _ = _run_both_paths(s_dom_viol)
    assert g_dv["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    # Scenario 5: Contradictory certificates (tampered witness margin > 0 claiming PASS,
    #             plus interval-split union/branch/count tamper checks — Defect 3B)
    s_conf = json.loads(json.dumps(s1))
    s_conf["holdout_point_evaluations"][0]["decisive_witnesses"]["TC062-P0-F"][
        "certified_margin_enclosure"
    ] = pos_margin
    g_cf, _ = _run_both_paths(s_conf)
    assert g_cf["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_cf["completion_outcome_code"] == "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED_GATE_OPEN"
    assert "SURVIVAL" not in g_cf["completion_outcome_code"]
    assert g_cf["all_mathematical_and_numerical_checks_pass"] is False

    s_iv_union_conf = json.loads(json.dumps(s1))
    s_iv_union_conf["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["union_M_P0_F"] = pos_margin
    g_iv_uc, _ = _run_both_paths(s_iv_union_conf)
    assert g_iv_uc["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_iv_uc["completion_outcome_code"] == "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED_GATE_OPEN"
    assert "SURVIVAL" not in g_iv_uc["completion_outcome_code"]
    assert g_iv_uc["all_mathematical_and_numerical_checks_pass"] is False

    s_iv_br_conf = json.loads(json.dumps(s1))
    s_iv_br_conf["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["branches"][0]["M_P0_F"] = pos_margin
    g_iv_bc, _ = _run_both_paths(s_iv_br_conf)
    assert g_iv_bc["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_iv_bc["completion_outcome_code"] == "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED_GATE_OPEN"
    assert g_iv_bc["all_mathematical_and_numerical_checks_pass"] is False

    s_iv_cnt_conf = json.loads(json.dumps(s1))
    s_iv_cnt_conf["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["branches"] = []
    g_iv_cc, _ = _run_both_paths(s_iv_cnt_conf)
    assert g_iv_cc["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_iv_cc["all_mathematical_and_numerical_checks_pass"] is False

    s_iv_missing = json.loads(json.dumps(s1))
    s_iv_missing["continuous_straddling_interval_splits"] = {}
    g_iv_miss, _ = _run_both_paths(s_iv_missing)
    assert g_iv_miss["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert "SURVIVAL" not in g_iv_miss["completion_outcome_code"]
    assert g_iv_miss["all_mathematical_and_numerical_checks_pass"] is False

    # Contradictory FAIL union over negative PASS branches MUST trigger CERTIFICATION_INTEGRITY_CONFLICT
    # (`TASK-TC-062R2` §2):
    s_iv_fail_contradiction = json.loads(json.dumps(s1))
    s_iv_fail_contradiction["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["union_M_P0_F"] = pos_margin
    s_iv_fail_contradiction["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["TC062_P0_F_interval_classification"]["verdict"] = "FAIL"
    g_iv_fc, _ = _run_both_paths(s_iv_fail_contradiction)
    assert g_iv_fc["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert (
        g_iv_fc["execution_and_certification_status"]
        == "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED"
    )
    assert g_iv_fc["completion_outcome_code"] == "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED_GATE_OPEN"
    assert g_iv_fc["all_mathematical_and_numerical_checks_pass"] is False

    # Separate structurally coherent certified-refutation interval fixture (both branches positive
    # and enclosed by their true Arb union):
    s_iv_coherent_fail = json.loads(json.dumps(s1))
    sp625_cf = s_iv_coherent_fail["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    b0_m_arb = arb("0.21", arb("0.005"))
    b1_m_arb = arb("0.24", arb("0.005"))
    b0_f_arb = arb("0.92", arb("0.005"))
    b1_f_arb = arb("0.95", arb("0.005"))
    sp625_cf["branches"][0]["evaluated_Y_interval_exact_fractions"] = ["2559999/4096", "625"]
    sp625_cf["branches"][1]["evaluated_Y_interval_exact_fractions"] = ["625", "2560001/4096"]
    sp625_cf["branches"][0]["F_Y"] = strip_enclosure_arb_for_json(serialize_arb_certified(b0_f_arb))
    sp625_cf["branches"][1]["F_Y"] = strip_enclosure_arb_for_json(serialize_arb_certified(b1_f_arb))
    sp625_cf["union_F_Y"] = strip_enclosure_arb_for_json(
        serialize_arb_certified(b0_f_arb.union(b1_f_arb))
    )
    sp625_cf["branches"][0]["M_P0_F"] = strip_enclosure_arb_for_json(
        serialize_arb_certified(b0_m_arb)
    )
    sp625_cf["branches"][1]["M_P0_F"] = strip_enclosure_arb_for_json(
        serialize_arb_certified(b1_m_arb)
    )
    sp625_cf["branches"][0]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp625_cf["branches"][1]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp625_cf["union_M_P0_F"] = strip_enclosure_arb_for_json(
        serialize_arb_certified(b0_m_arb.union(b1_m_arb))
    )
    sp625_cf["TC062_P0_F_interval_classification"] = {"verdict": "FAIL"}
    g_iv_f, _ = _run_both_paths(s_iv_coherent_fail)
    assert g_iv_f["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert g_iv_f["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"
    assert (
        g_iv_f["section_5_unseen_validation_and_interval_splits"]["global_candidate_outcomes"][
            "TC062-P0-F"
        ]
        == "REFUTED_BY_CERTIFIED_WITNESS"
    )
    assert "SURVIVAL" not in g_iv_f["completion_outcome_code"]
    assert g_iv_f["all_mathematical_and_numerical_checks_pass"] is True

    # Scenario 6: Missing, non-covering (`TIER_LOCAL_SNAPSHOT`), or EXCEEDED resource telemetry
    #             (including secondary wall-time fields — Defects 3A & 3C)
    s_snap = json.loads(json.dumps(s1))
    s_snap["holdout_point_evaluations"][0]["tier_escalation_history"][0][
        "peak_rss_measurement_semantics"
    ] = "TIER_LOCAL_SNAPSHOT"
    g_sn, _ = _run_both_paths(s_snap)
    assert g_sn["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert g_sn["resource_compliance_status"] == "UNKNOWN"
    assert "RESOURCE_UNKNOWN" in g_sn["research_outcome_class"]
    assert "SURVIVAL" not in g_sn["completion_outcome_code"]
    assert g_sn["all_mathematical_and_numerical_checks_pass"] is False

    s_nomem = json.loads(json.dumps(s1))
    s_nomem["holdout_point_evaluations"][0]["tier_escalation_history"][0]["peak_rss_mb"] = None
    g_nm, _ = _run_both_paths(s_nomem)
    assert g_nm["resource_compliance_status"] == "UNKNOWN"
    assert "SURVIVAL" not in g_nm["completion_outcome_code"]
    assert g_nm["all_mathematical_and_numerical_checks_pass"] is False

    s_rss_ex = json.loads(json.dumps(s1))
    s_rss_ex["holdout_point_evaluations"][0]["tier_escalation_history"][0]["peak_rss_mb"] = 5000.0
    g_rx, _ = _run_both_paths(s_rss_ex)
    assert g_rx["resource_compliance_status"] == "EXCEEDED"
    assert "RESOURCE_EXCEEDED" in g_rx["research_outcome_class"]
    assert "SURVIVAL" not in g_rx["completion_outcome_code"]
    assert g_rx["all_mathematical_and_numerical_checks_pass"] is False

    s_sec_wall_ex = json.loads(json.dumps(s1))
    s_sec_wall_ex["holdout_point_evaluations"][0]["tier_escalation_history"][0][
        "tier_wall_seconds"
    ] = 500.0
    s_sec_wall_ex["holdout_point_evaluations"][0]["tier_escalation_history"][0][
        "cumulative_wall_seconds"
    ] = 500.0
    g_swx, _ = _run_both_paths(s_sec_wall_ex)
    assert g_swx["resource_compliance_status"] == "EXCEEDED"
    assert "RESOURCE_EXCEEDED" in g_swx["research_outcome_class"]
    assert "SURVIVAL" not in g_swx["completion_outcome_code"]
    assert g_swx["all_mathematical_and_numerical_checks_pass"] is False

    # Scenario 7: Prior decisive failure at Tier 0 followed by unresolved escalation at Tiers 1..2
    proto = json.loads(JOINT_PRIME_DILATION_PROTOCOL_PATH.read_text(encoding="utf-8"))
    probes = proto["frozen_candidate_probes"]
    rules = proto["numerical_settings_and_escalation_rules"]
    tbl_small = compute_selberg_centered_remainder_table_fast_arb(400, prec_bits=288)
    first_entry = proto["holdout_validation_schedule"]["holdout_entries"][0]
    sp_first = ExactScaleSpec.from_protocol_entry(first_entry)

    def _eval_fail_then_unresolved(spec, *, tier: int, resolved_settings):
        cut = certify_exact_scale_cutoffs(spec, base_prec_bits=256)
        yb = spec.evaluate_arb(256)
        if tier == 0:
            return {
                "cutoffs": cut,
                "observables": {
                    "Y_arb": yb,
                    "E_Y": arb("0.02"),
                    "D_tilde_Y": arb("0.03"),
                    "X_self_Y": arb("0.001"),
                    "J_Y": arb("0.504"),
                    "F_Y": arb("0.50"),  # Decisive FAIL on TC062-P0-F
                    "F_int_T_p2": arb("0.14155") + arb(0, arb("0.05")),  # Straddles -> escalates
                    "diag_int_T_p2": arb("-0.10"),
                    "offdiag_int_T_p2": arb("-0.01"),
                    "F_bnd_T_p2": arb("0.35"),
                    "F_int_T_p23": arb("-0.02"),
                    "diag_int_T_p23": arb("-0.03"),
                    "offdiag_int_T_p23": arb("0.01"),
                    "F_bnd_T_p23": arb("0.52"),
                    "log_Y_times_D_tilde": arb("0.14155"),
                },
            }
        z_strad = arb(0, arb("1.0"))
        return {
            "cutoffs": cut,
            "observables": {
                "Y_arb": yb,
                "E_Y": arb("0.02"),
                "D_tilde_Y": arb("0.03"),
                "X_self_Y": arb("0.001"),
                "J_Y": z_strad,
                "F_Y": z_strad,
                "F_int_T_p2": z_strad,
                "diag_int_T_p2": z_strad,
                "offdiag_int_T_p2": z_strad,
                "F_bnd_T_p2": z_strad,
                "F_int_T_p23": z_strad,
                "diag_int_T_p23": z_strad,
                "offdiag_int_T_p23": z_strad,
                "F_bnd_T_p23": z_strad,
                "log_Y_times_D_tilde": arb("0.14155"),
            },
        }

    row_esc = execute_tc062_holdout_point_with_escalation(
        str(first_entry["point_id"]),
        sp_first,
        probes,
        rules,
        selberg_table=tbl_small,
        evaluator_fn=_eval_fail_then_unresolved,
    )
    row_esc["grid_tier"] = str(first_entry["grid_tier"])
    row_esc["prior_exposure_status"] = str(first_entry["prior_exposure_status"])
    s7 = json.loads(json.dumps(s1))
    s7["holdout_point_evaluations"][0] = strip_enclosure_arb_for_json(row_esc)
    g7, _ = _run_both_paths(s7)
    assert g7["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert (
        g7["execution_and_certification_status"]
        == "PARTIAL_CERTIFICATION_REFUTED_WITH_UNRESOLVED_REMAINING_EVALUATIONS"
    )
    assert (
        g7["section_5_unseen_validation_and_interval_splits"]["global_candidate_outcomes"][
            "TC062-P0-F"
        ]
        == "REFUTED_BY_CERTIFIED_WITNESS"
    )
    assert (
        g7["section_5_unseen_validation_and_interval_splits"]["all_section_5_checks_pass"]
        is False
    )
    assert g7["all_mathematical_and_numerical_checks_pass"] is False
    assert "SURVIVAL" not in g7["completion_outcome_code"]
    assert "SURVIVED" not in g7["research_outcome_class"]


def test_tc062r2_interval_containment_exact_cutoff_partition_and_extra_branch_semantics(
    tc062_artifact: Dict[str, Any], tmp_path
) -> None:
    """Adversarial regression suite for `TASK-TC-062R2` §§2, 3, & 7 across BOTH generator and
    reprocessor paths:
    - `PASS`, `FAIL`, and `UNRESOLVED` union-to-branch containment (including partial overlap and
      non-margin observables `union_F_Y`);
    - Malformed bounds, cross-field discrepancy, and mismatched branch/union classifications;
    - Valid conservative union wider than minimal hull;
    - Valid feasible `FAIL` branch inside a containing `UNRESOLVED` union (mixed signs, complete
      branch certification);
    - Exact cutoff partition & boundary ownership on `[625 - 2^-12, 625 + 2^-12]` and
      `[2017/5, 20173/50]`, plus valid outward Arb padding;
    - Duplicate `625` branch replacing `(3126, 6, 6)` and missing each `exp(6)` branch in turn;
    - Wrong `D_eff`, altered prescribed endpoints, uncovered left/right endpoint, interior gap;
    - Possibly-empty conservative extra branch `(1808, 6, 6)` cannot independently certify refutation.
    """
    from tc.canonical_theta_correlation_bound import serialize_arb_certified
    from tc.mixed_arithmetic_covariance import strip_enclosure_arb_for_json

    flint_ctx.prec = 256
    pre_1_4 = (
        tc062_artifact["section_1_protocols_reassembly_and_complete_kernel"],
        tc062_artifact["section_2_disjoint_prime_decompositions_and_controls"],
        tc062_artifact["section_3_whole_line_contraction_obstruction"],
        tc062_artifact["section_4_quantitative_proof_attempt"],
    )
    s_base = json.loads(
        json.dumps(tc062_artifact["section_5_unseen_validation_and_interval_splits"])
    )

    def _ser(ball: arb) -> Dict[str, Any]:
        return strip_enclosure_arb_for_json(serialize_arb_certified(ball))

    def _q_arb(q: Fraction) -> arb:
        return arb(q.numerator) / arb(q.denominator)

    def _both(sec5_mut: Dict[str, Any], tag: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        g = generate_task_tc062_artifact(
            write_output=False,
            precomputed_sections_1_to_4=pre_1_4,
            section_5_override=sec5_mut,
        )
        art_tmp = json.loads(json.dumps(tc062_artifact))
        art_tmp["section_5_unseen_validation_and_interval_splits"] = json.loads(
            json.dumps(sec5_mut)
        )
        p_f = tmp_path / f"tc062r2_{tag}.json"
        p_f.write_text(json.dumps(art_tmp), encoding="utf-8")
        r = reprocess_task_tc062_metadata_and_stage_b(p_f, write_output=False)
        assert g["holdout_hypothesis_outcome"] == r["holdout_hypothesis_outcome"]
        assert g["execution_and_certification_status"] == r["execution_and_certification_status"]
        assert g["completion_outcome_code"] == r["completion_outcome_code"]
        assert (
            g["all_mathematical_and_numerical_checks_pass"]
            == r["all_mathematical_and_numerical_checks_pass"]
        )
        return g, r

    # 1. Exact cutoff partition & boundary ownership:
    p625 = derive_exact_interval_cutoff_partition(
        Fraction(2559999, 4096), Fraction(2560001, 4096)
    )
    assert p625["feasible_triples"] == [(3125, 6, 6), (3126, 6, 6)]
    assert p625["infeasible_triples_in_grid"] == []
    c625_0, c625_1 = p625["feasible_cells"]
    assert c625_0["upper_closed"] is True and c625_0["subdomain_notation"].endswith("625]")
    assert c625_1["lower_closed"] is False and c625_1["subdomain_notation"].startswith("(625,")

    pe6 = derive_exact_interval_cutoff_partition(Fraction(2017, 5), Fraction(20173, 50))
    assert pe6["feasible_triples"] == [(1808, 5, 5), (1809, 5, 5), (1809, 6, 6)]
    assert pe6["infeasible_triples_in_grid"] == [(1808, 6, 6)]
    ce6_0, ce6_1, ce6_2 = pe6["feasible_cells"]
    assert ce6_0["lower_closed"] is True and ce6_0["upper_closed"] is True
    assert ce6_1["lower_closed"] is False and ce6_1["upper_closed"] is False
    assert ce6_2["lower_closed"] is True and ce6_2["subdomain_notation"].startswith("[exp(6),")

    # 2. PASS union missing part of a branch (both margin M_P0_F and non-margin F_Y):
    s_pass_miss = json.loads(json.dumps(s_base))
    s_pass_miss["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["union_M_P0_F"] = _ser(arb("-0.6480", arb("1e-5")))
    g_pm, _ = _both(s_pass_miss, "pass_miss_m")
    assert g_pm["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_pm["all_mathematical_and_numerical_checks_pass"] is False

    s_fy_miss = json.loads(json.dumps(s_base))
    s_fy_miss["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["union_F_Y"] = _ser(arb("0.10", arb("1e-9")))
    g_fym, _ = _both(s_fy_miss, "fy_miss")
    assert g_fym["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_fym["all_mathematical_and_numerical_checks_pass"] is False

    # 3. UNRESOLVED union failing to contain a branch (even when overlapping on [-0.10, -0.05]):
    s_unres_miss = json.loads(json.dumps(s_base))
    sp_um = s_unres_miss["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_um["branches"][0]["M_P0_F"] = _ser(arb("-0.125", arb("0.075")))  # [-0.20, -0.05]
    sp_um["branches"][0]["TC062_P0_F_branch_classification"] = {"verdict": "PASS"}
    sp_um["union_M_P0_F"] = _ser(arb("0.0", arb("0.10")))  # [-0.10, +0.10] overlaps but misses [-0.20, -0.10)
    sp_um["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_um, _ = _both(s_unres_miss, "unres_partial_overlap")
    assert g_um["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_um["all_mathematical_and_numerical_checks_pass"] is False

    # 4. Malformed bounds & mismatched branch classification:
    s_mal = json.loads(json.dumps(s_base))
    bad_ball = dict(
        s_mal["continuous_straddling_interval_splits"][
            "interval_625_pm_2_neg12_across_T3125"
        ]["branches"][0]["M_P0_F"]
    )
    bad_ball["lower_dec"], bad_ball["upper_dec"] = bad_ball["upper_dec"], bad_ball["lower_dec"]
    s_mal["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["branches"][0]["M_P0_F"] = bad_ball
    g_mal, _ = _both(s_mal, "malformed_dec")
    assert g_mal["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"

    s_br_cls = json.loads(json.dumps(s_base))
    s_br_cls["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["branches"][0]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    g_bcls, _ = _both(s_br_cls, "bad_br_cls")
    assert g_bcls["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"

    # 5. Valid conservative union strictly wider than minimal branch hull + valid outward Y_sub_ball padding:
    s_wide = json.loads(json.dumps(s_base))
    sp_w = s_wide["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_w["union_M_P0_F"] = _ser(arb("-0.50", arb("0.30")))  # [-0.80, -0.20] strictly wider than ~[-0.652, -0.648]
    sp_w["branches"][0]["Y_sub_ball"] = _ser(
        _q_arb(Fraction(2559999, 4096) - Fraction(1, 10**6)).union(
            _q_arb(Fraction(625, 1) + Fraction(1, 10**6))
        )
    )
    sp_w["branches"][1]["Y_sub_ball"] = _ser(
        _q_arb(Fraction(625, 1) - Fraction(1, 10**6)).union(
            _q_arb(Fraction(2560001, 4096) + Fraction(1, 10**6))
        )
    )
    g_w, _ = _both(s_wide, "valid_conservative_wide")
    assert g_w["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert g_w["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"
    assert g_w["all_mathematical_and_numerical_checks_pass"] is True

    # 6. Fully resolved mixed-sign feasible branches (`PASS` + `FAIL`) inside a containing
    #    zero-crossing `UNRESOLVED` union -> consistent refutation AND complete branch certification:
    s_mixed = json.loads(json.dumps(s_base))
    sp_mx = s_mixed["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    b0_neg = arb("-0.650", arb("0.002"))
    b1_pos = arb("0.150", arb("0.005"))
    f0_arb = arb("0.070", arb("0.001"))
    f1_arb = arb("0.870", arb("0.005"))
    sp_mx["branches"][0]["evaluated_Y_interval_exact_fractions"] = ["2559999/4096", "625"]
    sp_mx["branches"][1]["evaluated_Y_interval_exact_fractions"] = ["625", "2560001/4096"]
    sp_mx["branches"][0]["F_Y"] = _ser(f0_arb)
    sp_mx["branches"][1]["F_Y"] = _ser(f1_arb)
    sp_mx["union_F_Y"] = _ser(f0_arb.union(f1_arb))
    sp_mx["branches"][0]["M_P0_F"] = _ser(b0_neg)
    sp_mx["branches"][1]["M_P0_F"] = _ser(b1_pos)
    sp_mx["branches"][0]["TC062_P0_F_branch_classification"] = {"verdict": "PASS"}
    sp_mx["branches"][1]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_mx["union_M_P0_F"] = _ser(b0_neg.union(b1_pos))
    sp_mx["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_mx, _ = _both(s_mixed, "mixed_sign_resolved_branches")
    assert g_mx["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert g_mx["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"
    assert (
        g_mx["section_5_unseen_validation_and_interval_splits"][
            "all_required_applicable_evaluations_resolved"
        ]
        is True
    )
    assert g_mx["all_mathematical_and_numerical_checks_pass"] is True

    # 7. Duplicate 625 branch replacing (3126, 6, 6) -> INCOMPLETE_OR_INVALID_COVERAGE:
    s_dup625 = json.loads(json.dumps(s_base))
    sp_d6 = s_dup625["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_d6["branches"][1] = json.loads(json.dumps(sp_d6["branches"][0]))
    sp_d6["T_range"] = [3125, 3125]
    g_d6, _ = _both(s_dup625, "dup_625_branch")
    assert g_d6["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert g_d6["execution_and_certification_status"] == "INCOMPLETE_HOLDOUT_COVERAGE"
    assert "SURVIVAL" not in g_d6["completion_outcome_code"]
    assert g_d6["all_mathematical_and_numerical_checks_pass"] is False

    # 8. Missing each exp(6)-interval branch in turn (`drop_idx in (0, 1, 2)`):
    for drop_idx in (0, 1, 2):
        s_de6 = json.loads(json.dumps(s_base))
        sp_e6 = s_de6["continuous_straddling_interval_splits"][
            "interval_403_40_to_403_46_across_e6"
        ]
        sp_e6["branches"].pop(drop_idx)
        sp_e6["active_branch_count"] = len(sp_e6["branches"])
        sp_e6["T_range"] = [
            min(b["T_fixed"] for b in sp_e6["branches"]),
            max(b["T_fixed"] for b in sp_e6["branches"]),
        ]
        sp_e6["D0_range"] = [
            min(b["D0_raw_fixed"] for b in sp_e6["branches"]),
            max(b["D0_raw_fixed"] for b in sp_e6["branches"]),
        ]
        g_de6, _ = _both(s_de6, f"drop_e6_{drop_idx}")
        assert g_de6["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
        assert g_de6["execution_and_certification_status"] == "INCOMPLETE_HOLDOUT_COVERAGE"
        assert g_de6["all_mathematical_and_numerical_checks_pass"] is False

    # 9. Wrong D_eff, altered prescribed endpoints, uncovered endpoint, and interior gap:
    s_deff = json.loads(json.dumps(s_base))
    s_deff["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["branches"][0]["D0_eff_fixed"] = 5
    g_deff, _ = _both(s_deff, "wrong_deff")
    assert g_deff["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_deff["all_mathematical_and_numerical_checks_pass"] is False

    s_alt_ep = json.loads(json.dumps(s_base))
    sp_ae = s_alt_ep["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_ae["Y_lo_fraction"] = "625"
    sp_ae["branches"] = [sp_ae["branches"][1]]
    sp_ae["active_branch_count"] = 1
    sp_ae["T_range"] = [3126, 3126]
    g_ae, _ = _both(s_alt_ep, "altered_endpoints")
    assert g_ae["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert g_ae["all_mathematical_and_numerical_checks_pass"] is False

    s_uncov_left = json.loads(json.dumps(s_base))
    s_uncov_left["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["branches"][0]["Y_sub_ball"] = _ser(
        _q_arb(Fraction(6249999, 10000)).union(_q_arb(Fraction(625, 1)))
    )  # 624.9999 > 624.999755859375 leaves left endpoint uncovered
    g_ul, _ = _both(s_uncov_left, "uncovered_left")
    assert g_ul["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    cov_ul = g_ul["section_5_unseen_validation_and_interval_splits"]["coverage_audit"][
        "interval_coverage_issues"
    ]
    assert any(i["issue_type"] == "UNCOVERED_LEFT_INTERVAL_ENDPOINT" for i in cov_ul)

    s_int_gap = json.loads(json.dumps(s_base))
    s_int_gap["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["branches"][0]["Y_sub_ball"] = _ser(
        _q_arb(Fraction(2559999, 4096)).union(_q_arb(Fraction(6249999, 10000)))
    )  # stops at 624.9999 < 625, leaving interior gap (624.9999, 625]
    g_ig, _ = _both(s_int_gap, "interior_gap")
    assert g_ig["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    cov_ig = g_ig["section_5_unseen_validation_and_interval_splits"]["coverage_audit"][
        "interval_coverage_issues"
    ]
    assert any(i["issue_type"] == "INTERIOR_SUBDOMAIN_GAP" for i in cov_ig)

    # 10. Possibly-empty conservative extra branch (1808, 6, 6) with FAIL margin CANNOT certify refutation:
    s_extra = json.loads(json.dumps(s_base))
    sp_ex = s_extra["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]
    extra_br = json.loads(json.dumps(sp_ex["branches"][0]))
    extra_br.pop("historical_domain_reconstruction", None)
    extra_br["T_fixed"] = 1808
    extra_br["D0_raw_fixed"] = 6
    extra_br["D0_eff_fixed"] = 6
    extra_br["branch_role"] = "POSSIBLY_EMPTY_CONSERVATIVE_BRANCH"
    ex_pos_m = arb("0.12", arb("0.005"))
    extra_br["M_P0_F"] = _ser(ex_pos_m)
    extra_br["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_ex["branches"].append(extra_br)
    sp_ex["active_branch_count"] = 4
    # Update union_M_P0_F to contain both negative feasible branches and positive extra branch:
    sp_ex["union_M_P0_F"] = _ser(arb("-0.60").union(ex_pos_m))
    sp_ex["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_ex, _ = _both(s_extra, "possibly_empty_extra_fail")
    assert g_ex["holdout_hypothesis_outcome"] == "UNRESOLVED_EVIDENCE"
    assert g_ex["holdout_hypothesis_outcome"] != "REFUTED_BY_CERTIFIED_WITNESS"
    assert "SURVIVAL" not in g_ex["completion_outcome_code"]
    assert g_ex["all_mathematical_and_numerical_checks_pass"] is False

    # Unannotated extra branch -> INCOMPLETE_OR_INVALID_COVERAGE:
    s_extra_unann = json.loads(json.dumps(s_extra))
    del s_extra_unann["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]["branches"][-1]["branch_role"]
    g_exu, _ = _both(s_extra_unann, "unannotated_extra")
    assert g_exu["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    # False admissible_witness_Y on infeasible extra branch -> CERTIFICATION_INTEGRITY_CONFLICT:
    s_extra_badw = json.loads(json.dumps(s_extra))
    s_extra_badw["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]["branches"][-1]["admissible_witness_Y"] = "80685/200"
    g_exbw, _ = _both(s_extra_badw, "false_witness_extra")
    assert g_exbw["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"

    # 11. Cross-representation forgery exploits (1A: wide dec over disjoint arb_ball_str; 1B: float
    #     narrowing zero-straddling ball to PASS; 1C: wide dec + positive arb_ball_str claiming FAIL
    #     over negative PASS branches; 1D: omitted float keys) -> ALL blocked with CERTIFICATION_INTEGRITY_CONFLICT:
    s_ex1a = json.loads(json.dumps(s_base))
    s_ex1a["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["union_M_P0_F"] = {
        "lower_dec": "-1000.0",
        "upper_dec": "0.0",
        "arb_ball_str": "[-0.10 +/- 0.001]",
        "mid_float": -0.10,
        "rad_float_outward": 0.002,
    }
    g_1a, _ = _both(s_ex1a, "exploit_1a_wide_dec_disjoint_bs")
    assert g_1a["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_1a["serialized_arb_self_check"]["all_enclose_original_256bit_arb_ball"] is False
    assert g_1a["all_mathematical_and_numerical_checks_pass"] is False

    s_ex1b = json.loads(json.dumps(s_base))
    forged_1b = _ser(arb("0", arb("1.0")))
    forged_1b["mid_float"] = -0.65
    forged_1b["rad_float_outward"] = 0.01
    s_ex1b["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["union_M_P0_F"] = forged_1b
    g_1b, _ = _both(s_ex1b, "exploit_1b_float_narrowed")
    assert g_1b["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_1b["serialized_arb_self_check"]["all_enclose_original_256bit_arb_ball"] is False
    assert g_1b["all_mathematical_and_numerical_checks_pass"] is False

    s_ex1c = json.loads(json.dumps(s_base))
    sp_1c = s_ex1c["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_1c["union_M_P0_F"] = {
        "lower_dec": "-1000.0",
        "upper_dec": "1000.0",
        "arb_ball_str": "[0.15 +/- 0.005]",
        "mid_float": 0.15,
        "rad_float_outward": 0.01,
    }
    sp_1c["TC062_P0_F_interval_classification"] = {"verdict": "FAIL"}
    g_1c, _ = _both(s_ex1c, "exploit_1c_fail_union_over_pass_branches")
    assert g_1c["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_1c["serialized_arb_self_check"]["all_enclose_original_256bit_arb_ball"] is False
    assert g_1c["all_mathematical_and_numerical_checks_pass"] is False

    s_ex1d = json.loads(json.dumps(s_base))
    no_fl_ball = dict(
        s_ex1d["continuous_straddling_interval_splits"][
            "interval_625_pm_2_neg12_across_T3125"
        ]["union_M_P0_F"]
    )
    del no_fl_ball["mid_float"]
    s_ex1d["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["union_M_P0_F"] = no_fl_ball
    g_1d, _ = _both(s_ex1d, "exploit_1d_missing_float_keys")
    assert g_1d["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_1d["serialized_arb_self_check"]["all_enclose_original_256bit_arb_ball"] is False

    # 12. Strict integer validation on T_range, D0_range, T_fixed, and active_branch_count (zero
    #     unhandled ValueError/TypeError and zero silent float/bool coercion):
    for bad_tag, mut_fn in (
        ("t_range_strings", lambda sp: sp.update({"T_range": ["bad", "val"]})),
        ("t_range_floats", lambda sp: sp.update({"T_range": [3125.9, 3126.9]})),
        ("d0_range_bools", lambda sp: sp.update({"D0_range": [True, 6]})),
        ("t_fixed_float", lambda sp: sp["branches"][0].update({"T_fixed": 3125.9})),
        ("active_cnt_float", lambda sp: sp.update({"active_branch_count": 2.0})),
    ):
        s_bad_int = json.loads(json.dumps(s_base))
        mut_fn(
            s_bad_int["continuous_straddling_interval_splits"][
                "interval_625_pm_2_neg12_across_T3125"
            ]
        )
        g_bi, _ = _both(s_bad_int, f"strict_int_{bad_tag}")
        assert g_bi["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
        assert g_bi["all_mathematical_and_numerical_checks_pass"] is False


def test_tc062r2_granular_resolution_partial_certification_and_out_of_domain(
    tc062_artifact: Dict[str, Any], tmp_path
) -> None:
    """Adversarial regression suite for `TASK-TC-062R2` §§4 & 7 across BOTH generator and
    reprocessor paths:
    - `FAIL` + unresolved different candidate -> `REFUTED_BY_CERTIFIED_WITNESS` +
      `PARTIAL_CERTIFICATION_REFUTED_WITH_UNRESOLVED_REMAINING_EVALUATIONS` (`all_pass = False`);
    - Globally refuted candidate with another `UNRESOLVED` point for that SAME candidate ->
      incomplete grid certification remains visible (`all_pass = False`);
    - Earlier decisive witness at Tier 0 + Tier 1 unresolved on that candidate while remaining
      candidates resolve at Tier 1 -> witness retained and `CERTIFIED_EVALUATION_COMPLETE`;
    - Out-of-domain (`Y < Y_0`) `"NOT_EVALUATED"` entries do not count as missing/unresolved, while
      evaluating an out-of-domain entry flags `OUT_OF_DOMAIN_EVALUATED`;
    - Independent `EXCEEDED` and `UNKNOWN` resource statuses on coherent refutation.
    """
    from tc.canonical_theta_correlation_bound import serialize_arb_certified
    from tc.mixed_arithmetic_covariance import strip_enclosure_arb_for_json

    flint_ctx.prec = 256
    pre_1_4 = (
        tc062_artifact["section_1_protocols_reassembly_and_complete_kernel"],
        tc062_artifact["section_2_disjoint_prime_decompositions_and_controls"],
        tc062_artifact["section_3_whole_line_contraction_obstruction"],
        tc062_artifact["section_4_quantitative_proof_attempt"],
    )
    s_base = json.loads(
        json.dumps(tc062_artifact["section_5_unseen_validation_and_interval_splits"])
    )
    pos_margin = strip_enclosure_arb_for_json(serialize_arb_certified(arb("0.25")))
    strad_margin = strip_enclosure_arb_for_json(serialize_arb_certified(arb(0, arb("0.02"))))

    def _both(sec5_mut: Dict[str, Any], tag: str, **ovr: Any) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        g = generate_task_tc062_artifact(
            write_output=False,
            precomputed_sections_1_to_4=pre_1_4,
            section_5_override=sec5_mut,
            **ovr,
        )
        art_tmp = json.loads(json.dumps(tc062_artifact))
        art_tmp["section_5_unseen_validation_and_interval_splits"] = json.loads(
            json.dumps(sec5_mut)
        )
        p_f = tmp_path / f"tc062r2_gran_{tag}.json"
        p_f.write_text(json.dumps(art_tmp), encoding="utf-8")
        r = reprocess_task_tc062_metadata_and_stage_b(
            p_f,
            write_output=False,
            holdout_entries_override=ovr.get("holdout_entries_override"),
        )
        assert g["holdout_hypothesis_outcome"] == r["holdout_hypothesis_outcome"]
        assert g["execution_and_certification_status"] == r["execution_and_certification_status"]
        assert g["completion_outcome_code"] == r["completion_outcome_code"]
        assert (
            g["all_mathematical_and_numerical_checks_pass"]
            == r["all_mathematical_and_numerical_checks_pass"]
        )
        return g, r

    # 1. FAIL on TC062-P-NEG-INT2 at point 0 + UNRESOLVED on TC062-P0-INT2 at point 2:
    s_diff_unres = json.loads(json.dumps(s_base))
    r0 = s_diff_unres["holdout_point_evaluations"][0]
    r0["accumulated_candidate_verdicts"]["TC062-P-NEG-INT2"] = "FAIL"
    r0["decisive_witnesses"]["TC062-P-NEG-INT2"]["verdict"] = "FAIL"
    r0["decisive_witnesses"]["TC062-P-NEG-INT2"]["certified_margin_enclosure"] = pos_margin
    r0["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["point_verdict"] = "FAIL"
    r0["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["margin_M_Y"] = pos_margin
    r2 = s_diff_unres["holdout_point_evaluations"][2]
    r2["accumulated_candidate_verdicts"]["TC062-P0-INT2"] = "UNRESOLVED"
    r2["decisive_witnesses"]["TC062-P0-INT2"] = None
    r2["last_tier_probe_evaluations"]["per_probe"]["TC062-P0-INT2"]["point_verdict"] = "UNRESOLVED"
    r2["last_tier_probe_evaluations"]["per_probe"]["TC062-P0-INT2"]["margin_M_Y"] = strad_margin
    g_du, _ = _both(s_diff_unres, "fail_plus_diff_unresolved")
    assert g_du["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert (
        g_du["execution_and_certification_status"]
        == "PARTIAL_CERTIFICATION_REFUTED_WITH_UNRESOLVED_REMAINING_EVALUATIONS"
    )
    assert g_du["section_5_unseen_validation_and_interval_splits"]["all_section_5_checks_pass"] is False
    assert g_du["all_mathematical_and_numerical_checks_pass"] is False

    # 2. Globally refuted candidate (`TC062-P-NEG-INT2` FAIL at point 0) with another UNRESOLVED
    #    point (point 4) for that SAME candidate (all other 5 candidates PASS everywhere!):
    s_same_unres = json.loads(json.dumps(s_base))
    r0s = s_same_unres["holdout_point_evaluations"][0]
    r0s["accumulated_candidate_verdicts"]["TC062-P-NEG-INT2"] = "FAIL"
    r0s["decisive_witnesses"]["TC062-P-NEG-INT2"]["verdict"] = "FAIL"
    r0s["decisive_witnesses"]["TC062-P-NEG-INT2"]["certified_margin_enclosure"] = pos_margin
    r0s["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["point_verdict"] = "FAIL"
    r0s["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["margin_M_Y"] = pos_margin
    r4s = s_same_unres["holdout_point_evaluations"][4]
    r4s["accumulated_candidate_verdicts"]["TC062-P-NEG-INT2"] = "UNRESOLVED"
    r4s["decisive_witnesses"]["TC062-P-NEG-INT2"] = None
    r4s["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["point_verdict"] = "UNRESOLVED"
    r4s["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["margin_M_Y"] = strad_margin
    g_su, _ = _both(s_same_unres, "same_candidate_other_point_unresolved")
    assert (
        g_su["section_5_unseen_validation_and_interval_splits"]["global_candidate_outcomes"][
            "TC062-P-NEG-INT2"
        ]
        == "REFUTED_BY_CERTIFIED_WITNESS"
    )
    assert g_su["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert (
        g_su["execution_and_certification_status"]
        == "PARTIAL_CERTIFICATION_REFUTED_WITH_UNRESOLVED_REMAINING_EVALUATIONS"
    )
    unres_pairs = g_su["section_5_unseen_validation_and_interval_splits"]["resolution_audit"][
        "unresolved_applicable_point_candidate_pairs"
    ]
    assert any(
        p["point_id"] == r4s["point_id"] and p["candidate_id"] == "TC062-P-NEG-INT2"
        for p in unres_pairs
    )
    assert g_su["all_mathematical_and_numerical_checks_pass"] is False

    # 3. Earlier decisive FAIL witness at Tier 0 + Tier 1 unresolved on that candidate while the
    #    escalating candidate resolves to PASS at Tier 1 -> witness retained AND grid complete:
    proto = json.loads(JOINT_PRIME_DILATION_PROTOCOL_PATH.read_text(encoding="utf-8"))
    probes = proto["frozen_candidate_probes"]
    rules = proto["numerical_settings_and_escalation_rules"]
    tbl_small = compute_selberg_centered_remainder_table_fast_arb(400, prec_bits=288)
    first_entry = proto["holdout_validation_schedule"]["holdout_entries"][0]
    sp_first = ExactScaleSpec.from_protocol_entry(first_entry)

    def _eval_tier0_fail_tier1_resolves_other(spec, *, tier: int, resolved_settings):
        cut = certify_exact_scale_cutoffs(spec, base_prec_bits=256)
        yb = spec.evaluate_arb(256)
        if tier == 0:
            return {
                "cutoffs": cut,
                "observables": {
                    "Y_arb": yb,
                    "E_Y": arb("0.02"),
                    "D_tilde_Y": arb("0.03"),
                    "X_self_Y": arb("0.001"),
                    "J_Y": arb("0.504"),
                    "F_Y": arb("0.50"),  # Decisive FAIL on TC062-P0-F at Tier 0
                    "F_int_T_p2": arb(0, arb("0.05")),  # Straddles 0 on TC062-P-NEG-INT2 -> escalates!
                    "diag_int_T_p2": arb("-0.10"),
                    "offdiag_int_T_p2": arb("-0.01"),
                    "F_bnd_T_p2": arb("0.35"),
                    "F_int_T_p23": arb("-0.02"),
                    "diag_int_T_p23": arb("-0.03"),
                    "offdiag_int_T_p23": arb("0.01"),
                    "F_bnd_T_p23": arb("0.52"),
                    "log_Y_times_D_tilde": arb("0.14155"),
                },
            }
        return {
            "cutoffs": cut,
            "observables": {
                "Y_arb": yb,
                "E_Y": arb("0.02"),
                "D_tilde_Y": arb("0.03"),
                "X_self_Y": arb("0.001"),
                "J_Y": arb("0.14155") + arb(0, arb("0.20")),
                "F_Y": arb("0.14155") + arb(0, arb("0.20")),  # Now UNRESOLVED at Tier 1!
                "F_int_T_p2": arb("-0.05"),  # Now resolved PASS at Tier 1!
                "diag_int_T_p2": arb("-0.10"),
                "offdiag_int_T_p2": arb("-0.01"),
                "F_bnd_T_p2": arb("0.35"),
                "F_int_T_p23": arb("-0.02"),
                "diag_int_T_p23": arb("-0.03"),
                "offdiag_int_T_p23": arb("0.01"),
                "F_bnd_T_p23": arb("0.52"),
                "log_Y_times_D_tilde": arb("0.14155"),
            },
        }

    row_ret = execute_tc062_holdout_point_with_escalation(
        str(first_entry["point_id"]),
        sp_first,
        probes,
        rules,
        selberg_table=tbl_small,
        evaluator_fn=_eval_tier0_fail_tier1_resolves_other,
    )
    row_ret["grid_tier"] = str(first_entry["grid_tier"])
    row_ret["prior_exposure_status"] = str(first_entry["prior_exposure_status"])
    s_ret = json.loads(json.dumps(s_base))
    s_ret["holdout_point_evaluations"][0] = strip_enclosure_arb_for_json(row_ret)
    g_ret, _ = _both(s_ret, "retained_witness_complete")
    assert g_ret["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert g_ret["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"
    assert g_ret["all_mathematical_and_numerical_checks_pass"] is True

    # 3b. Contradictory decisive witnesses across tiers (`FAIL` at Tier 0 vs `PASS` at Tier 1 on
    #     `TC062-P-NEG-INT2`) -> `CERTIFICATION_INTEGRITY_CONFLICT` across BOTH generator & reprocessor:
    def _eval_contradictory_across_tiers(spec, *, tier: int, resolved_settings):
        res_t = _eval_tier0_fail_tier1_resolves_other(spec, tier=tier, resolved_settings=resolved_settings)
        if tier == 0:
            # Make F_int_T_p2 = [+0.09155, +0.19155] > 0 (FAIL on TC062-P-NEG-INT2, UNRESOLVED on TC062-P0-INT2):
            res_t["observables"]["F_int_T_p2"] = arb("0.14155") + arb(0, arb("0.05"))
        return res_t

    row_contra = execute_tc062_holdout_point_with_escalation(
        str(first_entry["point_id"]),
        sp_first,
        probes,
        rules,
        selberg_table=tbl_small,
        evaluator_fn=_eval_contradictory_across_tiers,
    )
    row_contra["grid_tier"] = str(first_entry["grid_tier"])
    row_contra["prior_exposure_status"] = str(first_entry["prior_exposure_status"])
    s_contra = json.loads(json.dumps(s_base))
    s_contra["holdout_point_evaluations"][0] = strip_enclosure_arb_for_json(row_contra)
    g_contra, _ = _both(s_contra, "contradictory_tier_verdicts")
    assert g_contra["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert (
        g_contra["execution_and_certification_status"]
        == "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED"
    )
    assert g_contra["all_mathematical_and_numerical_checks_pass"] is False

    # 3c. Decisive last-tier `FAIL` margin masked as `accumulated_candidate_verdicts = "UNRESOLVED"`
    #     with `decisive_witnesses = None` -> `CERTIFICATION_INTEGRITY_CONFLICT` (never silently
    #     downgraded to `UNRESOLVED_EVIDENCE`):
    s_masked_lt = json.loads(json.dumps(s_base))
    r0_mlt = s_masked_lt["holdout_point_evaluations"][0]
    r0_mlt["accumulated_candidate_verdicts"]["TC062-P-NEG-INT2"] = "UNRESOLVED"
    r0_mlt["decisive_witnesses"]["TC062-P-NEG-INT2"] = None
    r0_mlt["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["point_verdict"] = "FAIL"
    r0_mlt["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["margin_M_Y"] = pos_margin
    g_mlt, _ = _both(s_masked_lt, "masked_decisive_last_tier_as_unresolved")
    assert g_mlt["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert (
        g_mlt["execution_and_certification_status"]
        == "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED"
    )
    assert g_mlt["all_mathematical_and_numerical_checks_pass"] is False

    # 4. Out-of-domain (`Y = 8 < 64`) entry handling:
    entries_with_ood = list(proto["holdout_validation_schedule"]["holdout_entries"]) + [
        {
            "point_id": "TC062-HO-SYNTH-OOD-Y8",
            "label": "8",
            "kind": "exact_rational",
            "rational_factor": "8/1",
            "exp_power": "0/1",
            "grid_tier": "synthetic_ood_test",
            "prior_exposure_status": "synthetic_test_only",
        }
    ]
    s_ood = json.loads(json.dumps(s_base))
    ood_row = json.loads(json.dumps(s_base["holdout_point_evaluations"][0]))
    ood_row["point_id"] = "TC062-HO-SYNTH-OOD-Y8"
    ood_row["label"] = "8"
    for cid_k in list(ood_row["accumulated_candidate_verdicts"].keys()):
        ood_row["accumulated_candidate_verdicts"][cid_k] = "NOT_EVALUATED"
        ood_row["decisive_witnesses"][cid_k] = None
    for pr_k in list(ood_row["last_tier_probe_evaluations"]["per_probe"].keys()):
        ood_row["last_tier_probe_evaluations"]["per_probe"][pr_k]["in_declared_domain"] = False
        ood_row["last_tier_probe_evaluations"]["per_probe"][pr_k]["point_verdict"] = "NOT_EVALUATED"
        ood_row["last_tier_probe_evaluations"]["per_probe"][pr_k]["margin_M_Y"] = None
    ood_row["last_tier_probe_evaluations"]["mechanism_kl1_sub_budgets"]["in_declared_domain"] = False
    ood_row["last_tier_probe_evaluations"]["mechanism_kl1_sub_budgets"]["diag_margin"] = None
    ood_row["last_tier_probe_evaluations"]["mechanism_kl1_sub_budgets"]["offdiag_margin"] = None
    s_ood["holdout_point_evaluations"].append(ood_row)
    g_ood, _ = _both(s_ood, "ood_not_evaluated_valid", holdout_entries_override=entries_with_ood)
    assert g_ood["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert g_ood["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"
    assert g_ood["all_mathematical_and_numerical_checks_pass"] is True

    # Out-of-domain probe falsely evaluated as PASS -> INCOMPLETE_OR_INVALID_COVERAGE:
    s_ood_bad = json.loads(json.dumps(s_ood))
    s_ood_bad["holdout_point_evaluations"][-1]["accumulated_candidate_verdicts"]["TC062-P0-F"] = "PASS"
    s_ood_bad["holdout_point_evaluations"][-1]["decisive_witnesses"]["TC062-P0-F"] = json.loads(
        json.dumps(s_base["holdout_point_evaluations"][0]["decisive_witnesses"]["TC062-P0-F"])
    )
    g_oodb, _ = _both(s_ood_bad, "ood_evaluated_violation", holdout_entries_override=entries_with_ood)
    assert g_oodb["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert g_oodb["all_mathematical_and_numerical_checks_pass"] is False

    # 5. Independent EXCEEDED and UNKNOWN resource statuses on coherent refutation:
    s_ref_rss_ex = json.loads(json.dumps(s_base))
    r0_re = s_ref_rss_ex["holdout_point_evaluations"][0]
    r0_re["accumulated_candidate_verdicts"]["TC062-P-NEG-INT2"] = "FAIL"
    r0_re["decisive_witnesses"]["TC062-P-NEG-INT2"]["verdict"] = "FAIL"
    r0_re["decisive_witnesses"]["TC062-P-NEG-INT2"]["certified_margin_enclosure"] = pos_margin
    r0_re["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["point_verdict"] = "FAIL"
    r0_re["last_tier_probe_evaluations"]["per_probe"]["TC062-P-NEG-INT2"]["margin_M_Y"] = pos_margin
    r0_re["tier_escalation_history"][0]["peak_rss_mb"] = 9000.0
    g_rre, _ = _both(s_ref_rss_ex, "refuted_rss_exceeded")
    assert g_rre["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert (
        g_rre["execution_and_certification_status"]
        == "CERTIFIED_EVALUATION_COMPLETE_RESOURCE_BUDGET_EXCEEDED"
    )
    assert g_rre["resource_compliance_status"] == "EXCEEDED"
    assert g_rre["all_mathematical_and_numerical_checks_pass"] is False


def test_tc062r2_stable_key_verdict_comparison_and_endpoint_strip_mathematics(
    tc062_artifact: Dict[str, Any], tmp_path
) -> None:
    """Verify `TASK-TC-062R2` §§5, 6A, & 6B:
    1. `compare_tc062_artifacts_by_stable_key` across unchanged, changed verdict (probe, KL1,
       in-scope control, Candidate A1/A2, continuous interval branch), unavailable/missing/renamed
       (`NOT_COMPARED` / `INCOMPLETE_COMPARISON` -> `None`, never `False`), and status-only
       classification corrections;
    2. `verify_beta_four_piece_endpoint_and_summed_strip_bound_arb` verifying all-`d|n` (`d = T`)
       identity, exact `+Delta M_{sq,2}(T)` omission error, `sum_{k<=T} |beta_Y(k)| <= C_beta T (log T)^2`,
       uniform `O_p(1)` strip bound, and naive `|U_p(T)| * max |beta_Y|` divergence.
    """
    from tc.canonical_theta_correlation_bound import serialize_arb_certified
    from tc.mixed_arithmetic_covariance import strip_enclosure_arb_for_json

    flint_ctx.prec = 256
    base_art = json.loads(json.dumps(tc062_artifact))

    # 1a. Unavailable prior -> NOT_COMPARED and None (never False):
    c_none = compare_tc062_artifacts_by_stable_key(
        base_art, None, baseline_commit=REVIEWED_TC062R_DELIVERED_TIP
    )
    assert c_none["comparison_status"] == "NOT_COMPARED"
    assert c_none["any_probe_kl1_control_or_candidate_verdict_changed"] is None

    # 1b. Unchanged results -> COMPLETE_COMPARED and False:
    c_same = compare_tc062_artifacts_by_stable_key(
        base_art, base_art, baseline_commit=REVIEWED_TC062R_DELIVERED_TIP
    )
    assert c_same["comparison_status"] == "COMPLETE_COMPARED"
    assert c_same["any_probe_kl1_control_or_candidate_verdict_changed"] is False
    assert c_same["changed_mathematical_verdicts_count"] == 0
    assert c_same["changed_numerical_enclosures_count"] == 0

    # 1c. Changed mathematical verdict across probe, control, Candidate A2, and interval branch
    #     (with coherent margin enclosures matching the changed verdicts):
    mut_v = json.loads(json.dumps(base_art))
    neg_m = strip_enclosure_arb_for_json(serialize_arb_certified(arb("-0.15")))
    pos_m = strip_enclosure_arb_for_json(serialize_arb_certified(arb("0.15")))
    mut_v["section_2_disjoint_prime_decompositions_and_controls"]["matched_control_F_grid_rows"][
        -1
    ]["TC062_P0_F_margin"] = neg_m
    mut_v["section_2_disjoint_prime_decompositions_and_controls"]["matched_control_F_grid_rows"][
        -1
    ]["TC062_P0_F_verdict"] = "PASS"
    mut_v["section_4_quantitative_proof_attempt"][
        "candidate_a2_unsigned_paired_block_majorant_refutation"
    ]["margin_Y64"] = neg_m
    mut_v["section_4_quantitative_proof_attempt"][
        "candidate_a2_unsigned_paired_block_majorant_refutation"
    ]["verdict"] = "SURVIVED_TESTED_POINTS"
    mut_v["section_5_unseen_validation_and_interval_splits"]["global_candidate_outcomes"][
        "KL1_int2_offdiag"
    ] = "REFUTED_BY_CERTIFIED_WITNESS"
    mut_v["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]["branches"][1][
        "evaluated_Y_interval_exact_fractions"
    ] = ["625", "2560001/4096"]
    mut_v["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]["branches"][1]["M_P0_F"] = pos_m

    c_chg = compare_tc062_artifacts_by_stable_key(
        mut_v, base_art, baseline_commit=REVIEWED_TC062R_DELIVERED_TIP
    )
    assert c_chg["comparison_status"] == "COMPLETE_COMPARED"
    assert c_chg["any_probe_kl1_control_or_candidate_verdict_changed"] is True
    assert c_chg["changed_mathematical_verdicts_count"] == 4
    changed_scopes = {x["scope"] for x in c_chg["changed_mathematical_verdicts"]}
    assert {
        "in_scope_controls",
        "candidate_and_section4_classifications",
        "kl1_diagnostics",
        "continuous_interval_classifications",
    }.issubset(changed_scopes)

    # 1d. Missing / renamed entry in current OR in prior (`cur_v - old_v`) -> INCOMPLETE_COMPARISON and None:
    mut_miss = json.loads(json.dumps(base_art))
    mut_miss["section_5_unseen_validation_and_interval_splits"][
        "holdout_point_evaluations"
    ].pop()
    c_miss = compare_tc062_artifacts_by_stable_key(
        mut_miss, base_art, baseline_commit=REVIEWED_TC062R_DELIVERED_TIP
    )
    assert c_miss["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_miss["any_probe_kl1_control_or_candidate_verdict_changed"] is None
    assert c_miss["missing_or_incomparable_entries_count"] > 0

    prior_miss_ctrl = json.loads(json.dumps(base_art))
    prior_miss_ctrl["section_2_disjoint_prime_decompositions_and_controls"][
        "matched_control_F_grid_rows"
    ].pop()
    c_miss_prior = compare_tc062_artifacts_by_stable_key(
        base_art, prior_miss_ctrl, baseline_commit=REVIEWED_TC062R_DELIVERED_TIP
    )
    assert c_miss_prior["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_miss_prior["any_probe_kl1_control_or_candidate_verdict_changed"] is None
    assert c_miss_prior["missing_or_incomparable_entries_count"] > 0

    # 1d-bis. Tampered stored verdict string contradicting its serialized margin enclosure ->
    #         flagged as CERTIFICATION_INTEGRITY_CONFLICT -> INCOMPLETE_COMPARISON and None:
    mut_tampered_v = json.loads(json.dumps(base_art))
    mut_tampered_v["section_2_disjoint_prime_decompositions_and_controls"][
        "matched_control_F_grid_rows"
    ][-1]["TC062_P0_F_verdict"] = "PASS"  # contradicts positive TC062_P0_F_margin!
    c_tamp = compare_tc062_artifacts_by_stable_key(
        mut_tampered_v, base_art, baseline_commit=REVIEWED_TC062R_DELIVERED_TIP
    )
    assert c_tamp["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_tamp["any_probe_kl1_control_or_candidate_verdict_changed"] is None

    # 1e. Status-only classification correction (0 mathematical verdict changes):
    mut_stat = json.loads(json.dumps(base_art))
    mut_stat["execution_and_certification_status"] = (
        "CERTIFIED_EVALUATION_COMPLETE_RESOURCE_TELEMETRY_UNKNOWN"
    )
    mut_stat["resource_compliance_status"] = "UNKNOWN"
    mut_stat["all_mathematical_and_numerical_checks_pass"] = False
    c_stat = compare_tc062_artifacts_by_stable_key(
        mut_stat, base_art, baseline_commit=REVIEWED_TC062R_DELIVERED_TIP
    )
    assert c_stat["comparison_status"] == "COMPLETE_COMPARED"
    assert c_stat["any_probe_kl1_control_or_candidate_verdict_changed"] is False
    assert c_stat["any_integrity_coverage_or_execution_classification_changed"] is True
    assert c_stat["corrected_integrity_coverage_or_execution_classifications_count"] >= 3

    # 2. Mathematical audit of §§6A & 6B (`verify_beta_four_piece_endpoint_and_summed_strip_bound_arb`):
    b_aud = verify_beta_four_piece_endpoint_and_summed_strip_bound_arb(prec_bits=256)
    assert b_aud["verified"] is True, b_aud
    assert b_aud["c_32_series_lt_7_verified"] is True
    for ep_row in b_aud["endpoint_d_eq_T_convention_checks"]:
        assert ep_row["full_divisors_identity_holds_1_to_T"] is True
        assert ep_row["truncated_d_le_T_minus_1_fails_at_n_eq_T"] is True
        assert ep_row["exact_n_eq_T_omission_equals_Delta_M_sq2_T"] is True
    for st_row in b_aud["strip_summed_vs_pointwise_checks"]:
        assert st_row["sum_abs_beta_le_C_beta_T_logT_sq"] is True
        assert st_row["bare_sup_le_tau52_p3"] is True
        assert st_row["strip_window_energy_le_uniform_Op1_bound"] is True
        if st_row["Y"] >= 16:
            assert st_row["naive_pointwise_times_card_exceeds_summed_bound"] is True


def test_tc062r3_refutation_domain_admissibility_and_boundary_ownership(
    tc062_artifact: Dict[str, Any], tmp_path
) -> None:
    """Adversarial regression suite for `TASK-TC-062R3` §2 across `audit_continuous_interval_split_certificate_tc062`,
    `generate_task_tc062_artifact`, and `reprocess_task_tc062_metadata_and_stage_b`:
    - 2A: Disjoint evaluation box `[2, 2]` on `(3125, 6, 6)` with positive `M_P0_F` / `M_P0` cannot refute;
    - 2B: Wrong boundary ownership `[625, 625]` on `(3126, 6, 6)` with positive `M_P0_F` / `M_P0` cannot refute;
    - Exact boundary ownership at `Y = 625` (`T = 3125` admissible vs `T = 3126` inadmissible);
    - Exact boundary ownership at `exp(6)` (`D0 = 6` owns equality, `D0 = 5` excluded);
    - Genuinely overlapping partial box with positive `M_P0_F` or `M_P0` refutes while coverage stays incomplete;
    - Witness satisfying cutoff predicates (`Y_w in A`) but outside certified `B` is rejected;
    - Witness in certified `B` (`Y_w in B`) but outside prescribed interval or cutoff domain (`Y_w notin A`) is rejected;
    - Four distinct admissibility statuses (`DISJOINT_EVALUATION_DOMAIN`, `EXCLUDED_BOUNDARY_ONLY_INTERSECTION`,
      `UNCERTIFIED_INTERSECTION`, `CERTIFIED_NONEMPTY_INTERSECTION`);
    - Apparent overlap supplied solely by outward serialization padding cannot certify a witness;
    - Valid mixed-sign branches under an `UNRESOLVED` union, live producing-path provenance, and repeated
      reprocessing semantic idempotence.
    """
    from tc.canonical_theta_correlation_bound import serialize_arb_certified
    from tc.liouville_square_dilation import _exact_arb_endpoints_as_fractions
    from tc.mixed_arithmetic_covariance import (
        evaluate_interval_via_cutoff_case_split_arb,
        strip_enclosure_arb_for_json,
    )

    flint_ctx.prec = 256
    pre_1_4 = (
        tc062_artifact["section_1_protocols_reassembly_and_complete_kernel"],
        tc062_artifact["section_2_disjoint_prime_decompositions_and_controls"],
        tc062_artifact["section_3_whole_line_contraction_obstruction"],
        tc062_artifact["section_4_quantitative_proof_attempt"],
    )
    s_base = json.loads(
        json.dumps(tc062_artifact["section_5_unseen_validation_and_interval_splits"])
    )

    def _ser(ball: arb) -> Dict[str, Any]:
        return strip_enclosure_arb_for_json(serialize_arb_certified(ball))

    def _q_arb(q: Fraction) -> arb:
        return arb(q.numerator) / arb(q.denominator)

    def _both(sec5_mut: Dict[str, Any], tag: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        g = generate_task_tc062_artifact(
            write_output=False,
            precomputed_sections_1_to_4=pre_1_4,
            section_5_override=sec5_mut,
        )
        art_tmp = json.loads(json.dumps(tc062_artifact))
        art_tmp["section_5_unseen_validation_and_interval_splits"] = json.loads(
            json.dumps(sec5_mut)
        )
        p_f = tmp_path / f"tc062r3_{tag}.json"
        p_f.write_text(json.dumps(art_tmp), encoding="utf-8")
        r = reprocess_task_tc062_metadata_and_stage_b(p_f, write_output=False)
        assert g["holdout_hypothesis_outcome"] == r["holdout_hypothesis_outcome"]
        assert g["execution_and_certification_status"] == r["execution_and_certification_status"]
        assert g["completion_outcome_code"] == r["completion_outcome_code"]
        assert (
            g["all_mathematical_and_numerical_checks_pass"]
            == r["all_mathematical_and_numerical_checks_pass"]
        )
        return g, r

    pos_m = arb("0.20", arb("0.005"))
    neg_m_wide = arb("-1.0").union(arb("-0.05"))
    pos_f = arb("0.92", arb("0.005"))
    pos_j = arb("0.96", arb("0.005"))

    # 1. Reproduction 2A: Disjoint evaluation box `[2, 2]` on `(3125, 6, 6)` (for BOTH `P0_F` and `P0`):
    s_2a = json.loads(json.dumps(s_base))
    sp_2a = s_2a["continuous_straddling_interval_splits"]["interval_625_pm_2_neg12_across_T3125"]
    sp_2a["branches"][0]["Y_sub_ball"] = _ser(arb(2))
    sp_2a["branches"][0]["F_Y"] = _ser(pos_f)
    sp_2a["union_F_Y"] = _ser(arb("-0.40").union(pos_f))
    sp_2a["branches"][0]["M_P0_F"] = _ser(pos_m)
    sp_2a["branches"][0]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_2a["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_2a["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    aud_2a = audit_continuous_interval_split_certificate_tc062(
        "interval_625_pm_2_neg12_across_T3125",
        sp_2a,
        prescribed_Y_lo=Fraction(2559999, 4096),
        prescribed_Y_hi=Fraction(2560001, 4096),
    )
    assert aud_2a["integrity_ok"] is True
    assert aud_2a["coverage_complete"] is False
    adm_2a = aud_2a["branch_domain_admissibility"][0]
    assert adm_2a["admissibility_status"] == "DISJOINT_EVALUATION_DOMAIN"
    assert adm_2a["can_certify_refutation"] is False
    assert aud_2a["probe_effective_verdicts"] == {
        "P0": "INCOMPLETE_OR_INVALID_COVERAGE",
        "TC062_P0_F": "INCOMPLETE_OR_INVALID_COVERAGE",
    }
    g_2a, _ = _both(s_2a, "repro_2a_disjoint_p0f")
    assert g_2a["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert g_2a["execution_and_certification_status"] == "INCOMPLETE_HOLDOUT_COVERAGE"
    assert g_2a["all_mathematical_and_numerical_checks_pass"] is False

    # Same disjoint `[2, 2]` with positive `M_P0` as well:
    s_2a_p0 = json.loads(json.dumps(s_2a))
    sp_2a_p0 = s_2a_p0["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_2a_p0["branches"][0]["J_Y"] = _ser(pos_j)
    sp_2a_p0["union_J_Y"] = _ser(arb("-1.0").union(pos_j))
    sp_2a_p0["branches"][0]["M_P0"] = _ser(pos_m)
    sp_2a_p0["branches"][0]["P0_branch_classification"] = {"verdict": "FAIL"}
    sp_2a_p0["union_M_P0"] = _ser(neg_m_wide.union(pos_m))
    sp_2a_p0["P0_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_2a_p0, _ = _both(s_2a_p0, "repro_2a_disjoint_p0_and_p0f")
    assert g_2a_p0["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    # 2. Reproduction 2B: Wrong boundary ownership `[625, 625]` on `(3126, 6, 6)` (`(625, 625 + 2^-12]`):
    s_2b = json.loads(json.dumps(s_base))
    sp_2b = s_2b["continuous_straddling_interval_splits"]["interval_625_pm_2_neg12_across_T3125"]
    sp_2b["branches"][1]["Y_sub_ball"] = _ser(arb(625))
    sp_2b["branches"][1]["F_Y"] = _ser(pos_f)
    sp_2b["union_F_Y"] = _ser(arb("-0.40").union(pos_f))
    sp_2b["branches"][1]["M_P0_F"] = _ser(pos_m)
    sp_2b["branches"][1]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_2b["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_2b["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    aud_2b = audit_continuous_interval_split_certificate_tc062(
        "interval_625_pm_2_neg12_across_T3125",
        sp_2b,
        prescribed_Y_lo=Fraction(2559999, 4096),
        prescribed_Y_hi=Fraction(2560001, 4096),
    )
    assert aud_2b["integrity_ok"] is True
    assert aud_2b["coverage_complete"] is False
    adm_2b = aud_2b["branch_domain_admissibility"][1]
    assert adm_2b["admissibility_status"] == "EXCLUDED_BOUNDARY_ONLY_INTERSECTION"
    assert adm_2b["can_certify_refutation"] is False
    assert aud_2b["probe_effective_verdicts"]["TC062_P0_F"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    g_2b, _ = _both(s_2b, "repro_2b_wrong_boundary_625_on_3126")
    assert g_2b["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert g_2b["execution_and_certification_status"] == "INCOMPLETE_HOLDOUT_COVERAGE"

    # 3. `Y = 625` IS admissible on `T = 3125` (`[625 - 2^-12, 625]` owns right endpoint `625`),
    #    certifying partial-domain refutation while overall coverage stays incomplete:
    s_625_ok = json.loads(json.dumps(s_base))
    sp_625_ok = s_625_ok["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_625_ok["branches"][0]["Y_sub_ball"] = _ser(arb(625))
    sp_625_ok["branches"][0]["F_Y"] = _ser(pos_f)
    sp_625_ok["union_F_Y"] = _ser(arb("-0.40").union(pos_f))
    sp_625_ok["branches"][0]["M_P0_F"] = _ser(pos_m)
    sp_625_ok["branches"][0]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_625_ok["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_625_ok["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    aud_625_ok = audit_continuous_interval_split_certificate_tc062(
        "interval_625_pm_2_neg12_across_T3125",
        sp_625_ok,
        prescribed_Y_lo=Fraction(2559999, 4096),
        prescribed_Y_hi=Fraction(2560001, 4096),
    )
    assert aud_625_ok["integrity_ok"] is True
    assert aud_625_ok["coverage_complete"] is False
    adm_625_0 = aud_625_ok["branch_domain_admissibility"][0]
    assert adm_625_0["admissibility_status"] == "CERTIFIED_NONEMPTY_INTERSECTION"
    assert adm_625_0["certified_witness_Y"] == "625"
    assert adm_625_0["complete_subdomain_coverage"] is False
    assert adm_625_0["can_certify_refutation"] is True
    assert aud_625_ok["probe_effective_verdicts"]["TC062_P0_F"] == "FAIL"
    g_625_ok, _ = _both(s_625_ok, "valid_625_endpoint_on_3125")
    assert g_625_ok["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert (
        g_625_ok["execution_and_certification_status"]
        == "CERTIFIED_REFUTATION_WITH_INCOMPLETE_REMAINING_GRID"
    )
    assert g_625_ok["all_mathematical_and_numerical_checks_pass"] is False

    # 4. Exact boundary ownership at `exp(6)`: `D0 = 6` (`(1809, 6, 6)`, `[exp(6), 20173/50]`) owns
    #    equality `Y = exp(6)`, whereas `D0 = 5` (`(1809, 5, 5)`, `(1808^(4/5), exp(6))`) does NOT:
    e6_ball = arb(6).exp()
    s_e6_d6 = json.loads(json.dumps(s_base))
    sp_e6_d6 = s_e6_d6["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]
    sp_e6_d6["branches"][2]["Y_sub_ball"] = _ser(e6_ball)
    sp_e6_d6["branches"][2]["evaluated_Y_symbolic_bounds"] = [["exp", 6], ["exp", 6]]
    sp_e6_d6["branches"][2]["F_Y"] = _ser(pos_f)
    sp_e6_d6["union_F_Y"] = _ser(arb("-0.40").union(pos_f))
    sp_e6_d6["branches"][2]["M_P0_F"] = _ser(pos_m)
    sp_e6_d6["branches"][2]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_e6_d6["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_e6_d6["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_e6_d6, _ = _both(s_e6_d6, "exp6_owned_by_D0_6")
    aud_e6_d6 = g_e6_d6["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_split_audits"]["interval_403_40_to_403_46_across_e6"]
    assert (
        aud_e6_d6["branch_domain_admissibility"][2]["admissibility_status"]
        == "CERTIFIED_NONEMPTY_INTERSECTION"
    )
    assert aud_e6_d6["branch_domain_admissibility"][2]["certified_witness_Y"] == "exp(6)"
    assert g_e6_d6["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert (
        g_e6_d6["execution_and_certification_status"]
        == "CERTIFIED_REFUTATION_WITH_INCOMPLETE_REMAINING_GRID"
    )

    s_e6_d5 = json.loads(json.dumps(s_base))
    sp_e6_d5 = s_e6_d5["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]
    sp_e6_d5["branches"][1]["Y_sub_ball"] = _ser(e6_ball)
    sp_e6_d5["branches"][1]["evaluated_Y_symbolic_bounds"] = [["exp", 6], ["exp", 6]]
    sp_e6_d5["branches"][1]["F_Y"] = _ser(pos_f)
    sp_e6_d5["union_F_Y"] = _ser(arb("-0.40").union(pos_f))
    sp_e6_d5["branches"][1]["M_P0_F"] = _ser(pos_m)
    sp_e6_d5["branches"][1]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_e6_d5["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_e6_d5["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_e6_d5, _ = _both(s_e6_d5, "exp6_excluded_from_D0_5")
    aud_e6_d5 = g_e6_d5["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_split_audits"]["interval_403_40_to_403_46_across_e6"]
    assert (
        aud_e6_d5["branch_domain_admissibility"][1]["admissibility_status"]
        == "EXCLUDED_BOUNDARY_ONLY_INTERSECTION"
    )
    assert aud_e6_d5["branch_domain_admissibility"][1]["can_certify_refutation"] is False
    assert g_e6_d5["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    # 5. Genuinely overlapping partial box `[625 + 2^-16, 625 + 2^-13]` on `(3126, 6, 6)` with
    #    positive `M_P0` ONLY (while `M_P0_F` stays `PASS`) ALSO refutes while coverage stays incomplete:
    part_ball = _q_arb(Fraction(625, 1) + Fraction(1, 2**16)).union(
        _q_arb(Fraction(625, 1) + Fraction(1, 2**13))
    )
    s_part_p0 = json.loads(json.dumps(s_base))
    sp_pp0 = s_part_p0["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_pp0["branches"][1]["Y_sub_ball"] = _ser(part_ball)
    sp_pp0["branches"][1]["J_Y"] = _ser(pos_j)
    sp_pp0["union_J_Y"] = _ser(arb("-1.0").union(pos_j))
    sp_pp0["branches"][1]["M_P0"] = _ser(pos_m)
    sp_pp0["branches"][1]["P0_branch_classification"] = {"verdict": "FAIL"}
    sp_pp0["union_M_P0"] = _ser(neg_m_wide.union(pos_m))
    sp_pp0["P0_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_pp0, _ = _both(s_part_p0, "partial_box_p0_refutation")
    assert g_pp0["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert (
        g_pp0["execution_and_certification_status"]
        == "CERTIFIED_REFUTATION_WITH_INCOMPLETE_REMAINING_GRID"
    )
    assert g_pp0["section_5_unseen_validation_and_interval_splits"]["coverage_complete"] is False
    assert (
        g_pp0["section_5_unseen_validation_and_interval_splits"][
            "continuous_straddling_interval_splits"
        ]["P0_continuous_interval_outcome"]
        == "REFUTED_BY_CERTIFIED_WITNESS"
    )

    # 6. Supplied witness in `A` (`Y_w = 625` on `(3125, 6, 6)`) but outside certified `B` (`[625 - 2^-12, 624.9999]`)
    #    is rejected with `CERTIFICATION_INTEGRITY_CONFLICT`:
    s_w_out_b = json.loads(json.dumps(s_base))
    sp_wb = s_w_out_b["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_wb["branches"][0]["Y_sub_ball"] = _ser(
        _q_arb(Fraction(2559999, 4096)).union(_q_arb(Fraction(6249999, 10000)))
    )
    sp_wb["branches"][0]["admissible_witness_Y"] = "625"
    g_wb, _ = _both(s_w_out_b, "witness_in_A_outside_B")
    assert g_wb["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert any(
        c["conflict_type"] == "INVALID_BRANCH_ADMISSIBLE_WITNESS"
        and c["reason"] == "WITNESS_NOT_CERTIFIED_IN_EVALUATION_DOMAIN_B"
        for c in g_wb["section_5_unseen_validation_and_interval_splits"][
            "detected_integrity_conflicts"
        ]
    )

    # 7. Supplied witness in certified `B` (`[624.9999, 625.0001]`) but outside `A` (`Y_w = 625` on `(3126, 6, 6)`
    #    and `Y_w = 626` outside prescribed interval) is rejected with `CERTIFICATION_INTEGRITY_CONFLICT`:
    s_w_out_a = json.loads(json.dumps(s_base))
    sp_wa = s_w_out_a["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_wa["branches"][1]["Y_sub_ball"] = _ser(
        _q_arb(Fraction(6249999, 10000)).union(_q_arb(Fraction(6250001, 10000)))
    )
    sp_wa["branches"][1]["admissible_witness_Y"] = "625"
    g_wa, _ = _both(s_w_out_a, "witness_in_B_outside_cutoff_A")
    assert g_wa["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert any(
        c["conflict_type"] == "INVALID_BRANCH_ADMISSIBLE_WITNESS"
        and c["reason"] == "WITNESS_OUTSIDE_ADMISSIBLE_SUBDOMAIN_A"
        for c in g_wa["section_5_unseen_validation_and_interval_splits"][
            "detected_integrity_conflicts"
        ]
    )

    s_w_out_iv = json.loads(json.dumps(s_base))
    sp_wiv = s_w_out_iv["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_wiv["branches"][1]["Y_sub_ball"] = _ser(
        _q_arb(Fraction(6250001, 10000)).union(_q_arb(Fraction(6265, 10)))
    )
    sp_wiv["branches"][1]["admissible_witness_Y"] = "626"
    g_wiv, _ = _both(s_w_out_iv, "witness_in_B_outside_prescribed_interval")
    assert g_wiv["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"

    # 8. Outward serialization padding alone CANNOT certify a witness, and all 4 admissibility
    #    statuses (`DISJOINT`, `EXCLUDED_BOUNDARY_ONLY`, `UNCERTIFIED_INTERSECTION`, `CERTIFIED_NONEMPTY`)
    #    are distinct:
    # (8a) `625 - 2^-200 < 625` serialized to 40-digit decimal / 53-bit float straddles `625`:
    s_pad_625 = json.loads(json.dumps(s_base))
    sp_p625 = s_pad_625["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_p625["branches"][1]["Y_sub_ball"] = _ser(arb(625) - arb(2) ** (-200))
    sp_p625["branches"][1]["F_Y"] = _ser(pos_f)
    sp_p625["union_F_Y"] = _ser(arb("-0.40").union(pos_f))
    sp_p625["branches"][1]["M_P0_F"] = _ser(pos_m)
    sp_p625["branches"][1]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_p625["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_p625["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_p625, _ = _both(s_pad_625, "outward_padding_only_across_625")
    aud_p625 = g_p625["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_split_audits"]["interval_625_pm_2_neg12_across_T3125"]
    adm_p625 = aud_p625["branch_domain_admissibility"][1]
    assert adm_p625["admissibility_status"] == "UNCERTIFIED_INTERSECTION"
    assert adm_p625["admissibility_reason"] == "UNCERTIFIED_OUTWARD_SERIALIZATION_PADDING_OVERLAP"
    assert adm_p625["can_certify_refutation"] is False
    assert g_p625["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    # (8b) Rational `q_minus < exp(6)` (`10^-42` below `exp(6)`) whose 40-digit decimal box spills above `exp(6)`:
    flint_ctx.prec = 512
    e6_lo_512, _ = _exact_arb_endpoints_as_fractions(arb(6).exp())
    q_below_e6 = Fraction((e6_lo_512.numerator * (10**42)) // e6_lo_512.denominator, 10**42)
    flint_ctx.prec = 256
    s_pad_e6 = json.loads(json.dumps(s_base))
    sp_pe6 = s_pad_e6["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]
    sp_pe6["branches"][2]["Y_sub_ball"] = _ser(_q_arb(q_below_e6))
    sp_pe6["branches"][2]["F_Y"] = _ser(pos_f)
    sp_pe6["union_F_Y"] = _ser(arb("-0.40").union(pos_f))
    sp_pe6["branches"][2]["M_P0_F"] = _ser(pos_m)
    sp_pe6["branches"][2]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_pe6["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_pe6["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_pe6, _ = _both(s_pad_e6, "outward_padding_only_across_exp6")
    aud_pe6 = g_pe6["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_split_audits"]["interval_403_40_to_403_46_across_e6"]
    assert (
        aud_pe6["branch_domain_admissibility"][2]["admissibility_status"]
        == "UNCERTIFIED_INTERSECTION"
    )
    assert g_pe6["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    # (8c) Swapping branch 0's `mag_t`-padded `Y_sub_ball` (`hi_dec = 625 + 9.09e-13`) onto branch 1 `(3126, 6, 6)`:
    s_swap_pad = json.loads(json.dumps(s_p625 if "s_p625" in locals() else s_pad_625))
    s_swap_pad["continuous_straddling_interval_splits"]["interval_625_pm_2_neg12_across_T3125"][
        "branches"
    ][1]["Y_sub_ball"] = json.loads(
        json.dumps(
            s_base["continuous_straddling_interval_splits"][
                "interval_625_pm_2_neg12_across_T3125"
            ]["branches"][0]["Y_sub_ball"]
        )
    )
    g_swp, _ = _both(s_swap_pad, "swapped_branch0_padded_box_onto_3126")
    aud_swp = g_swp["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_split_audits"]["interval_625_pm_2_neg12_across_T3125"]
    assert (
        aud_swp["branch_domain_admissibility"][1]["admissibility_status"]
        == "UNCERTIFIED_INTERSECTION"
    )
    assert g_swp["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    observed_statuses = {
        adm_2a["admissibility_status"],
        adm_2b["admissibility_status"],
        adm_p625["admissibility_status"],
        adm_625_0["admissibility_status"],
    }
    assert len(observed_statuses) == 4
    assert observed_statuses.issubset(set(BRANCH_ADMISSIBILITY_STATUSES))

    # 9. Live producing-path provenance (`evaluate_interval_via_cutoff_case_split_arb`) + semantic
    #    idempotence of repeated `reprocess_task_tc062_metadata_and_stage_b`:
    tbl_small = compute_selberg_centered_remainder_table_fast_arb(40, prec_bits=288)
    raw_16 = evaluate_interval_via_cutoff_case_split_arb(
        Fraction(16, 1) - Fraction(1, 4096),
        Fraction(16, 1) + Fraction(1, 4096),
        prec_bits=256,
        quad_tol_bits=110,
        selberg_table=tbl_small,
    )
    for br16 in raw_16["branches"]:
        ef16 = br16["evaluated_Y_interval_exact_fractions"]
        assert isinstance(ef16, list) and len(ef16) == 2
        assert Fraction(ef16[0]) <= Fraction(ef16[1])

    p_idem = tmp_path / "idem_tc062.json"
    p_idem.write_bytes(JOINT_PRIME_DILATION_ARTIFACT_PATH.read_bytes())
    r_idem_1 = reprocess_task_tc062_metadata_and_stage_b(p_idem, write_output=True)
    r_idem_2 = reprocess_task_tc062_metadata_and_stage_b(p_idem, write_output=True)
    c1 = json.loads(json.dumps(r_idem_1))
    c2 = json.loads(json.dumps(r_idem_2))
    ts1 = c1["provenance"].pop("tc062r4_reprocessed_at_utc")
    ts2 = c2["provenance"].pop("tc062r4_reprocessed_at_utc")
    assert isinstance(ts1, str) and isinstance(ts2, str)
    assert c1 == c2

    # 10. Contradictory duplicate cutoff branch (`(3125, 6, 6)` with `PASS` and overlapping `[625, 625]`
    #     with `FAIL`, in BOTH branch orders) -> `CERTIFICATION_INTEGRITY_CONFLICT` (never refutation),
    #     and disjoint-box duplicate `FAIL` -> `INCOMPLETE_OR_INVALID_COVERAGE` (never refutation):
    s_dup_contra = json.loads(json.dumps(s_base))
    sp_dc = s_dup_contra["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    dup_fail_br = json.loads(json.dumps(sp_dc["branches"][0]))
    dup_fail_br["Y_sub_ball"] = _ser(arb(625))
    dup_fail_br["F_Y"] = _ser(pos_f)
    dup_fail_br["M_P0_F"] = _ser(pos_m)
    dup_fail_br["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_dc["branches"].append(dup_fail_br)
    sp_dc["active_branch_count"] = 3
    sp_dc["union_F_Y"] = _ser(arb("-0.40").union(pos_f))
    sp_dc["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_dc["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_dc, _ = _both(s_dup_contra, "dup_branch_contradiction_pass_then_fail")
    assert g_dc["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_dc["holdout_hypothesis_outcome"] != "REFUTED_BY_CERTIFIED_WITNESS"
    assert any(
        c["conflict_type"] == "INTERVAL_SPLIT_DUPLICATE_BRANCH_CONTRADICTION"
        for c in g_dc["section_5_unseen_validation_and_interval_splits"][
            "detected_integrity_conflicts"
        ]
    )

    s_dup_contra_rev = json.loads(json.dumps(s_dup_contra))
    sp_dcr = s_dup_contra_rev["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_dcr["branches"] = list(reversed(sp_dcr["branches"]))
    g_dcr, _ = _both(s_dup_contra_rev, "dup_branch_contradiction_fail_then_pass")
    assert g_dcr["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"

    # 11. Zero-radius float (`rad_float_outward = 0.0`) on boundary-spilling `625 - 2^-200` ball
    #     is rejected across BOTH generator and reprocessor (never promoted to `SERIALIZED_ARB_EXACT_POINT`):
    s_rf0 = json.loads(json.dumps(s_pad_625))
    sp_rf0 = s_rf0["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_rf0["branches"][1]["Y_sub_ball"]["mid_float"] = 625.0
    sp_rf0["branches"][1]["Y_sub_ball"]["rad_float_outward"] = 0.0
    g_rf0, r_rf0 = _both(s_rf0, "zero_rad_float_outward_rejected")
    assert g_rf0["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"
    assert g_rf0["serialized_arb_self_check"]["all_enclose_original_256bit_arb_ball"] is False
    assert r_rf0["serialized_arb_self_check"]["all_enclose_original_256bit_arb_ball"] is False

    # 12. Arbitrarily narrow exact rational intersection (`width = 2^-3000`) produces a verified
    #     rational witness `Y_w in A cap B` without precision exhaustion:
    s_narrow = json.loads(json.dumps(s_base))
    sp_nar = s_narrow["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    q_nar_lo = Fraction(625, 1) + Fraction(1, 2**15)
    q_nar_hi = q_nar_lo + Fraction(1, 2**3000)
    sp_nar["branches"][1]["evaluated_Y_interval_exact_fractions"] = [
        f"{q_nar_lo.numerator}/{q_nar_lo.denominator}",
        f"{q_nar_hi.numerator}/{q_nar_hi.denominator}",
    ]
    sp_nar["branches"][1]["Y_sub_ball"] = _ser(_q_arb(q_nar_lo).union(_q_arb(q_nar_hi)))
    sp_nar["branches"][1]["F_Y"] = _ser(pos_f)
    sp_nar["union_F_Y"] = _ser(arb("-0.40").union(pos_f))
    sp_nar["branches"][1]["M_P0_F"] = _ser(pos_m)
    sp_nar["branches"][1]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_nar["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_nar["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    aud_nar = audit_continuous_interval_split_certificate_tc062(
        "interval_625_pm_2_neg12_across_T3125",
        sp_nar,
        prescribed_Y_lo=Fraction(2559999, 4096),
        prescribed_Y_hi=Fraction(2560001, 4096),
    )
    adm_nar = aud_nar["branch_domain_admissibility"][1]
    assert adm_nar["admissibility_status"] == "CERTIFIED_NONEMPTY_INTERSECTION"
    assert adm_nar["certified_witness_Y"] is not None
    q_wit_nar = Fraction(adm_nar["certified_witness_Y"])
    assert q_nar_lo < q_wit_nar < q_nar_hi


def test_tc062r3_deleted_renamed_and_retired_status_provenance_comparison(
    tc062_artifact: Dict[str, Any],
) -> None:
    """Regression suite for `TASK-TC-062R3` §3 (`compare_tc062_artifacts_by_stable_key`):
    - Deleted top-level `execution_and_certification_status` -> `INCOMPLETE_COMPARISON`, `None` (never `False`);
    - Deleted Section 5 `all_required_applicable_evaluations_resolved` -> `INCOMPLETE_COMPARISON`, `None`;
    - Renamed status field -> `INCOMPLETE_COMPARISON` with both removal and addition recorded;
    - Changed status value -> `COMPLETE_COMPARED` with status change isolated from verdict/enclosure changes;
    - Explicit optional retirement rule vs refusal to retire required status fields;
    - Unchanged baseline & actual historical comparisons (`TC062`, `TC062R`, `TC062R2`).
    """
    base = json.loads(json.dumps(tc062_artifact))

    # 1. Deleted top-level `execution_and_certification_status` (audit as supplied, never recreated):
    cur_del_top = json.loads(json.dumps(base))
    del cur_del_top["execution_and_certification_status"]
    c_del_top = compare_tc062_artifacts_by_stable_key(
        cur_del_top, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert "execution_and_certification_status" not in cur_del_top
    assert c_del_top["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_del_top["any_probe_kl1_control_or_candidate_verdict_changed"] is None
    assert c_del_top["any_numerical_enclosure_changed"] is None
    assert c_del_top["any_integrity_coverage_or_execution_classification_changed"] is None
    assert any(
        r["key"] == "top.execution_and_certification_status"
        and r["reason"] == "REMOVED_REQUIRED_STATUS_FIELD"
        for r in c_del_top["removed_status_or_schema_fields"]
    )
    assert any(
        m["key"] == "top.execution_and_certification_status"
        for m in c_del_top["missing_or_incomparable_entries"]
    )

    # 2. Deleted Section 5 `all_required_applicable_evaluations_resolved` (against BOTH prior with
    #    that field AND prior predating that field):
    cur_del_s5 = json.loads(json.dumps(base))
    del cur_del_s5["section_5_unseen_validation_and_interval_splits"][
        "all_required_applicable_evaluations_resolved"
    ]
    c_del_s5 = compare_tc062_artifacts_by_stable_key(
        cur_del_s5, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert (
        "all_required_applicable_evaluations_resolved"
        not in cur_del_s5["section_5_unseen_validation_and_interval_splits"]
    )
    assert c_del_s5["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_del_s5["any_integrity_coverage_or_execution_classification_changed"] is None
    assert any(
        r["key"] == "sec5.all_required_applicable_evaluations_resolved"
        and r["reason"] == "REMOVED_REQUIRED_STATUS_FIELD"
        for r in c_del_s5["removed_status_or_schema_fields"]
    )

    prior_without_s5_res = json.loads(json.dumps(base))
    del prior_without_s5_res["section_5_unseen_validation_and_interval_splits"][
        "all_required_applicable_evaluations_resolved"
    ]
    c_del_s5_vs_older = compare_tc062_artifacts_by_stable_key(
        cur_del_s5, prior_without_s5_res, baseline_commit=REVIEWED_TC062R_DELIVERED_TIP
    )
    assert c_del_s5_vs_older["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert any(
        r["key"] == "sec5.all_required_applicable_evaluations_resolved"
        and r["reason"] == "MISSING_REQUIRED_CURRENT_STATUS_FIELD"
        for r in c_del_s5_vs_older["removed_status_or_schema_fields"]
    )

    # 3. Renamed status field (`execution_and_certification_status` -> `execution_status_renamed`,
    #    and custom status field `experimental_status` -> `experimental_state`):
    cur_ren = json.loads(json.dumps(base))
    cur_ren["execution_status_renamed"] = cur_ren.pop("execution_and_certification_status")
    c_ren = compare_tc062_artifacts_by_stable_key(
        cur_ren, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_ren["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_ren["any_integrity_coverage_or_execution_classification_changed"] is None
    assert any(
        r["key"] == "top.execution_and_certification_status"
        for r in c_ren["removed_status_or_schema_fields"]
    )
    assert any(
        a["kind"] == "status_field" and a["key"] == "top.execution_status_renamed"
        for a in c_ren["schema_only_additions"]
    )

    prior_opt = json.loads(json.dumps(base))
    prior_opt["experimental_status"] = "ACTIVE"
    cur_opt_ren = json.loads(json.dumps(base))
    cur_opt_ren["experimental_state"] = "ACTIVE"
    c_opt_ren = compare_tc062_artifacts_by_stable_key(
        cur_opt_ren, prior_opt, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_opt_ren["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert any(
        r["key"] == "top.experimental_status" for r in c_opt_ren["removed_status_or_schema_fields"]
    )
    assert any(
        a["kind"] == "status_field" and a["key"] == "top.experimental_state"
        for a in c_opt_ren["schema_only_additions"]
    )

    # 4. Explicit retirement rule for an optional field vs refusal to retire a required status field:
    c_opt_retired = compare_tc062_artifacts_by_stable_key(
        base,
        prior_opt,
        baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP,
        explicitly_retired_optional_keys={
            "top.experimental_status": "RETIRED_OPTIONAL_DIAGNOSTIC_V2"
        },
    )
    assert c_opt_retired["comparison_status"] == "COMPLETE_COMPARED"
    assert c_opt_retired["retired_optional_fields_count"] == 1
    assert c_opt_retired["removed_status_or_schema_fields_count"] == 0
    assert c_opt_retired["any_integrity_coverage_or_execution_classification_changed"] is False

    c_req_cannot_retire = compare_tc062_artifacts_by_stable_key(
        cur_del_top,
        base,
        baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP,
        explicitly_retired_optional_keys={
            "top.execution_and_certification_status": "ATTEMPTED_REQUIRED_RETIREMENT"
        },
    )
    assert c_req_cannot_retire["comparison_status"] == "INCOMPLETE_COMPARISON"

    # 5. Changed status value isolated from verdict/enclosure/schema changes:
    cur_chg_val = json.loads(json.dumps(base))
    cur_chg_val["execution_and_certification_status"] = "UNRESOLVED_HOLDOUT_EVIDENCE"
    c_chg_val = compare_tc062_artifacts_by_stable_key(
        cur_chg_val, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_chg_val["comparison_status"] == "COMPLETE_COMPARED"
    assert c_chg_val["any_integrity_coverage_or_execution_classification_changed"] is True
    assert c_chg_val["any_probe_kl1_control_or_candidate_verdict_changed"] is False
    assert c_chg_val["any_numerical_enclosure_changed"] is False
    assert c_chg_val["removed_status_or_schema_fields_count"] == 0
    assert c_chg_val["schema_only_additions_count"] == 0

    # 6. Unchanged baseline & actual stored provenance comparisons:
    assert len(REQUIRED_CURRENT_TC062_STATUS_KEYS) >= 13
    c_unch = compare_tc062_artifacts_by_stable_key(
        base, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_unch["comparison_status"] == "COMPLETE_COMPARED"
    assert c_unch["any_probe_kl1_control_or_candidate_verdict_changed"] is False
    assert c_unch["any_numerical_enclosure_changed"] is False
    assert c_unch["any_integrity_coverage_or_execution_classification_changed"] is False
    assert c_unch["removed_status_or_schema_fields_count"] == 0

    comp_r4 = tc062_artifact["provenance"]["tc062r4_validation_and_verdict_comparison"]
    assert comp_r4["comparison_id"] == "TC062R4_VS_TC062R3_AS_SUPPLIED_STABLE_KEY_V1"
    assert comp_r4["baseline_commit"] == REVIEWED_TC062R3_DELIVERED_TIP
    assert comp_r4["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert comp_r4["enclosure_comparison_complete"] is True
    assert comp_r4["any_numerical_enclosure_changed_on_comparable_balls"] is False
    assert comp_r4["changed_numerical_enclosures_count"] == 0
    assert comp_r4["changed_mathematical_verdicts_count"] == 0
    assert comp_r4["raw_branch_margin_sign_verdicts_changed_count"] == 0
    assert comp_r4["branch_coverage_classifications_changed_count"] == 5
    assert comp_r4["any_integrity_coverage_or_execution_classification_changed"] is True
    assert comp_r4["removed_status_or_schema_fields_count"] == 0

    comp_r4_post = tc062_artifact["provenance"]["tc062r4_post_domain_recovery_verdict_comparison"]
    assert comp_r4_post["comparison_id"] == "TC062R4_VS_TC062R3_POST_DOMAIN_RECOVERY_STABLE_KEY_V1"
    assert comp_r4_post["baseline_commit"] == REVIEWED_TC062R3_DELIVERED_TIP
    assert comp_r4_post["comparison_status"] == "COMPLETE_COMPARED"
    assert comp_r4_post["any_probe_kl1_control_or_candidate_verdict_changed"] is False
    assert comp_r4_post["any_numerical_enclosure_changed"] is False
    assert comp_r4_post["removed_status_or_schema_fields_count"] == 0

    # 7. Overwriting required or optional status fields with `None` or wrong types is caught as
    #    `INCOMPLETE_COMPARISON` with `None` (never accepted as a valid present scalar):
    cur_null_top = json.loads(json.dumps(base))
    cur_null_top["execution_and_certification_status"] = None
    c_null_top = compare_tc062_artifacts_by_stable_key(
        cur_null_top, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_null_top["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_null_top["any_integrity_coverage_or_execution_classification_changed"] is None
    assert any(
        r["key"] == "top.execution_and_certification_status"
        and "NULL_OR_MALFORMED_REQUIRED_STATUS_FIELD" in r["reason"]
        for r in c_null_top["removed_status_or_schema_fields"]
    )

    cur_null_s5 = json.loads(json.dumps(base))
    cur_null_s5["section_5_unseen_validation_and_interval_splits"][
        "all_required_applicable_evaluations_resolved"
    ] = None
    c_null_s5 = compare_tc062_artifacts_by_stable_key(
        cur_null_s5, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_null_s5["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_null_s5["any_integrity_coverage_or_execution_classification_changed"] is None

    cur_bad_type = json.loads(json.dumps(base))
    cur_bad_type["section_5_unseen_validation_and_interval_splits"][
        "evaluated_unseen_point_count"
    ] = True
    c_bad_type = compare_tc062_artifacts_by_stable_key(
        cur_bad_type, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_bad_type["comparison_status"] == "INCOMPLETE_COMPARISON"

    # 8. Interval `P0` admissibility-driven refutation flip (`[625, 625]` refutes vs `[2, 2]` disjoint)
    #    and duplicate interval branch detection in `compare_tc062_artifacts_by_stable_key`:
    from tc.canonical_theta_correlation_bound import serialize_arb_certified
    from tc.mixed_arithmetic_covariance import strip_enclosure_arb_for_json

    flint_ctx.prec = 256
    pos_p0 = strip_enclosure_arb_for_json(serialize_arb_certified(arb("0.20", arb("0.005"))))
    art_p0_valid = json.loads(json.dumps(base))
    sp_p0_v = art_p0_valid["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]
    sp_p0_v["branches"][0]["Y_sub_ball"] = strip_enclosure_arb_for_json(
        serialize_arb_certified(arb(625))
    )
    sp_p0_v["branches"][0]["M_P0"] = pos_p0

    art_p0_disjoint = json.loads(json.dumps(art_p0_valid))
    art_p0_disjoint["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]["branches"][0]["Y_sub_ball"] = (
        strip_enclosure_arb_for_json(serialize_arb_certified(arb(2)))
    )

    c_p0_vs_base = compare_tc062_artifacts_by_stable_key(
        art_p0_valid, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_p0_vs_base["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_p0_vs_base["any_probe_kl1_control_or_candidate_verdict_changed"] is True

    art_p0_full = json.loads(json.dumps(base))
    art_p0_full["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]["branches"][0][
        "evaluated_Y_interval_exact_fractions"
    ] = ["2559999/4096", "625"]
    art_p0_full["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]["branches"][0]["M_P0"] = pos_p0
    c_p0_full_vs_base = compare_tc062_artifacts_by_stable_key(
        art_p0_full, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_p0_full_vs_base["comparison_status"] == "COMPLETE_COMPARED"
    assert c_p0_full_vs_base["any_probe_kl1_control_or_candidate_verdict_changed"] is True

    c_p0_flip = compare_tc062_artifacts_by_stable_key(
        art_p0_disjoint, art_p0_valid, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_p0_flip["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_p0_flip["any_probe_kl1_control_or_candidate_verdict_changed"] is None
    assert c_p0_flip["any_integrity_coverage_or_execution_classification_changed"] is True

    art_dup_iv = json.loads(json.dumps(base))
    sp_dup_iv = art_dup_iv["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]
    sp_dup_iv["branches"].append(json.loads(json.dumps(sp_dup_iv["branches"][0])))
    c_dup_iv = compare_tc062_artifacts_by_stable_key(
        art_dup_iv, base, baseline_commit=REVIEWED_TC062R2_DELIVERED_TIP
    )
    assert c_dup_iv["comparison_status"] == "INCOMPLETE_COMPARISON"
    assert c_dup_iv["any_probe_kl1_control_or_candidate_verdict_changed"] is None


def test_tc062r4_exact_evaluation_domain_coverage_and_legacy_recovery(
    tc062_artifact: Dict[str, Any], tmp_path
) -> None:
    """Focused regression matrix for `TASK-TC-062R4` §§2–5 across live FLINT/Arb + production
    `serialize_arb_certified`, `audit_continuous_interval_split_certificate_tc062`,
    `generate_task_tc062_artifact`, `reprocess_task_tc062_metadata_and_stage_b`,
    `reconstruct_tc062r_legacy_interval_domains`, and `compare_tc062_artifacts_by_stable_key`:
    1. Concrete `625` right-endpoint gap `B = [625 - 2^-12 - 2^-201, 625 - 2^-201]` (recording exact
       binary endpoints vs outward serialized endpoints separately) cannot certify full coverage or
       complete interval survival;
    2. Corresponding left-end gap hidden by outward 40-digit rounding is rejected as complete coverage;
    3. Coverage at `exp(6)` respects exact ownership and cannot be supplied solely by decimal padding
       or by the neighboring `(1809, 5, 5)` wrong-cutoff branch;
    4. Tiny interior gap (`2^-201`) cannot disappear through a rounded union (`evaluated_Y_subintervals_exact_fractions`
       and adjacent cutoff branches);
    5. Valid fully covering exact evaluation domains (`evaluated_Y_interval_exact_fractions`,
       `evaluated_Y_symbolic_bounds`, `B_inner`-padded balls, and live producing path) pass;
    6. Justified recovered legacy domains on all 5 branches pass with `0` numerical margin changes;
    7. Deleting or invalidating domain evidence on any branch cannot silently preserve complete coverage;
    8. `reconstruct_tc062r_legacy_interval_domains` refuses mismatched producer commit, mismatched
       timestamp, mismatched cutoff identity, modified `Y_sub_ball`, pre-existing explicit domain
       field, or `prec=53` serialization-collision impostor margins;
    9. Partial evaluated domain with admissible positive margin (`P0` and `P0_F`) still refutes while
       coverage stays incomplete;
    10. Nonempty partial evaluated domain inside `A` with only `PASS` margins supplies an admissible
        witness (`can_certify_refutation = True`) yet cannot establish survival on the uncovered region;
    11. Disjoint and excluded-boundary-only boxes remain unable to refute;
    12. Valid mixed-sign branch outcomes, earlier decisive witnesses, and separate `WITHIN` / `EXCEEDED`
        / `UNKNOWN` resource statuses retain their semantics;
    13. Repeated metadata processing is semantically idempotent modulo `provenance.tc062r4_reprocessed_at_utc`.
    """
    from tc.canonical_theta_correlation_bound import serialize_arb_certified
    from tc.liouville_square_dilation import _exact_arb_endpoints_as_fractions
    from tc.mixed_arithmetic_covariance import (
        evaluate_interval_via_cutoff_case_split_arb,
        strip_enclosure_arb_for_json,
    )

    assert len(BRANCH_COVERAGE_STATUSES) == 5
    assert len(HISTORICAL_TC062R_BRANCH_OBSERVABLE_SHA256) == 5

    pre_1_4 = (
        tc062_artifact["section_1_protocols_reassembly_and_complete_kernel"],
        tc062_artifact["section_2_disjoint_prime_decompositions_and_controls"],
        tc062_artifact["section_3_whole_line_contraction_obstruction"],
        tc062_artifact["section_4_quantitative_proof_attempt"],
    )
    s_base = json.loads(
        json.dumps(tc062_artifact["section_5_unseen_validation_and_interval_splits"])
    )

    def _ser(ball: arb) -> Dict[str, Any]:
        return strip_enclosure_arb_for_json(serialize_arb_certified(ball))

    def _q_arb(q: Fraction) -> arb:
        return arb(q.numerator) / arb(q.denominator)

    def _both(sec5_mut: Dict[str, Any], tag: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        g = generate_task_tc062_artifact(
            write_output=False,
            precomputed_sections_1_to_4=pre_1_4,
            section_5_override=sec5_mut,
        )
        art_tmp = json.loads(json.dumps(tc062_artifact))
        art_tmp["section_5_unseen_validation_and_interval_splits"] = json.loads(
            json.dumps(sec5_mut)
        )
        p_f = tmp_path / f"tc062r4_{tag}.json"
        p_f.write_text(json.dumps(art_tmp), encoding="utf-8")
        r = reprocess_task_tc062_metadata_and_stage_b(p_f, write_output=False)
        assert g["holdout_hypothesis_outcome"] == r["holdout_hypothesis_outcome"]
        assert g["execution_and_certification_status"] == r["execution_and_certification_status"]
        assert g["completion_outcome_code"] == r["completion_outcome_code"]
        assert (
            g["all_mathematical_and_numerical_checks_pass"]
            == r["all_mathematical_and_numerical_checks_pass"]
        )
        return g, r

    # 1. Section 2 & 5.1: Live Arb + production serializer reproduction on `[625 - 2^-12, 625 + 2^-12]`,
    #    branch `(3125, 6, 6)`, `A = [625 - 2^-12, 625]`, `B = [625 - 2^-12 - 2^-201, 625 - 2^-201]`:
    flint_ctx.prec = 256
    a_lo_q = Fraction(2559999, 4096)
    a_hi_q = Fraction(625, 1)
    b_right_gap_mid = arf((625 * (1 << 201) - (1 << 188) - 1, -201))  # 625 - 2^-13 - 2^-201
    B_right_gap = arb(b_right_gap_mid, arf(((1 << 31) - 1, -44)))  # exact rad = 2^-13
    bin_lo_q, bin_hi_q = _exact_arb_endpoints_as_fractions(B_right_gap)
    assert bin_lo_q == a_lo_q - Fraction(1, 1 << 201)
    assert bin_hi_q == a_hi_q - Fraction(1, 1 << 201)
    assert bin_hi_q < a_hi_q  # misses right endpoint 625 and interval (625 - 2^-201, 625]

    ser_right_gap = _ser(B_right_gap)
    ser_lo_dec_q = Fraction(ser_right_gap["lower_dec"])
    ser_hi_dec_q = Fraction(ser_right_gap["upper_dec"])
    ser_lo_fl_q = Fraction(ser_right_gap["mid_float"]) - Fraction(ser_right_gap["rad_float_outward"])
    ser_hi_fl_q = Fraction(ser_right_gap["mid_float"]) + Fraction(ser_right_gap["rad_float_outward"])
    # Record binary vs outward-serialized endpoints separately: outward 40-digit and float enclosures
    # BOTH cover `A = [625 - 2^-12, 625]`, yet binary `B_right_gap` misses `[625 - 2^-201, 625]`:
    assert ser_lo_dec_q < a_lo_q and ser_hi_dec_q > a_hi_q
    assert ser_lo_fl_q < a_lo_q and ser_hi_fl_q > a_hi_q

    s_repro_625 = json.loads(json.dumps(s_base))
    sp_r625 = s_repro_625["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_r625["branches"][0].pop("historical_domain_reconstruction", None)
    sp_r625["branches"][0]["Y_sub_ball"] = ser_right_gap
    aud_r625 = audit_continuous_interval_split_certificate_tc062(
        "interval_625_pm_2_neg12_across_T3125",
        sp_r625,
        prescribed_Y_lo=Fraction(2559999, 4096),
        prescribed_Y_hi=Fraction(2560001, 4096),
    )
    assert aud_r625["integrity_ok"] is True
    assert aud_r625["coverage_complete"] is False
    assert aud_r625["probe_effective_verdicts"] == {
        "P0": "INCOMPLETE_OR_INVALID_COVERAGE",
        "TC062_P0_F": "INCOMPLETE_OR_INVALID_COVERAGE",
    }
    adm_r625 = aud_r625["branch_domain_admissibility"][0]
    assert adm_r625["admissibility_status"] == "CERTIFIED_NONEMPTY_INTERSECTION"
    assert adm_r625["can_certify_refutation"] is True
    assert adm_r625["complete_subdomain_coverage"] is False
    assert adm_r625["coverage_status"] == "UNCERTIFIED_COVERAGE"
    assert any(
        i["issue_type"] == "UNCERTIFIED_BRANCH_SUBDOMAIN_COVERAGE"
        for i in aud_r625["coverage_issues"]
    )
    g_r625, _ = _both(s_repro_625, "repro_625_right_gap_no_exact")
    assert g_r625["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert g_r625["execution_and_certification_status"] == "INCOMPLETE_HOLDOUT_COVERAGE"
    assert "SURVIVAL" not in g_r625["completion_outcome_code"]
    assert g_r625["all_mathematical_and_numerical_checks_pass"] is False

    # Same `B_right_gap` with its exact binary endpoints explicitly supplied -> `PROVED_COVERAGE_GAP`:
    s_repro_625_ex = json.loads(json.dumps(s_repro_625))
    s_repro_625_ex["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["branches"][0]["evaluated_Y_interval_exact_fractions"] = [
        f"{bin_lo_q.numerator}/{bin_lo_q.denominator}",
        f"{bin_hi_q.numerator}/{bin_hi_q.denominator}",
    ]
    aud_r625_ex = audit_continuous_interval_split_certificate_tc062(
        "interval_625_pm_2_neg12_across_T3125",
        s_repro_625_ex["continuous_straddling_interval_splits"][
            "interval_625_pm_2_neg12_across_T3125"
        ],
        prescribed_Y_lo=Fraction(2559999, 4096),
        prescribed_Y_hi=Fraction(2560001, 4096),
    )
    assert aud_r625_ex["integrity_ok"] is True
    assert aud_r625_ex["coverage_complete"] is False
    assert aud_r625_ex["branch_domain_admissibility"][0]["coverage_status"] == "PROVED_COVERAGE_GAP"
    assert any(i["issue_type"] == "INTERIOR_SUBDOMAIN_GAP" for i in aud_r625_ex["coverage_issues"])
    g_r625_ex, _ = _both(s_repro_625_ex, "repro_625_right_gap_exact")
    assert g_r625_ex["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    # 2. Section 5.2: Corresponding left-end gap `B_left = [625 - 2^-12 + 2^-201, 625 + 2^-201]`
    #    hidden by outward 40-digit rounding:
    b_left_gap_mid = arf((625 * (1 << 201) - (1 << 188) + 1, -201))  # 625 - 2^-13 + 2^-201
    B_left_gap = arb(b_left_gap_mid, arf(((1 << 31) - 1, -44)))
    bl_lo_q, bl_hi_q = _exact_arb_endpoints_as_fractions(B_left_gap)
    assert bl_lo_q == a_lo_q + Fraction(1, 1 << 201) > a_lo_q
    assert bl_hi_q == a_hi_q + Fraction(1, 1 << 201) > a_hi_q
    ser_left_gap = _ser(B_left_gap)
    assert Fraction(ser_left_gap["lower_dec"]) < a_lo_q
    assert Fraction(ser_left_gap["upper_dec"]) > a_hi_q

    s_left_gap = json.loads(json.dumps(s_base))
    sp_lg = s_left_gap["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_lg["branches"][0].pop("historical_domain_reconstruction", None)
    sp_lg["branches"][0]["Y_sub_ball"] = ser_left_gap
    g_lg, _ = _both(s_left_gap, "left_gap_hidden_by_rounding")
    assert g_lg["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert (
        g_lg["section_5_unseen_validation_and_interval_splits"][
            "continuous_straddling_interval_splits"
        ]["interval_split_audits"]["interval_625_pm_2_neg12_across_T3125"][
            "branch_domain_admissibility"
        ][0]["coverage_status"]
        == "UNCERTIFIED_COVERAGE"
    )

    s_left_gap_ex = json.loads(json.dumps(s_left_gap))
    s_left_gap_ex["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["branches"][0]["evaluated_Y_interval_exact_fractions"] = [
        f"{bl_lo_q.numerator}/{bl_lo_q.denominator}",
        f"{bl_hi_q.numerator}/{bl_hi_q.denominator}",
    ]
    g_lg_ex, _ = _both(s_left_gap_ex, "left_gap_exact_proved")
    aud_lg_ex = g_lg_ex["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_split_audits"]["interval_625_pm_2_neg12_across_T3125"]
    assert aud_lg_ex["branch_domain_admissibility"][0]["coverage_status"] == "PROVED_COVERAGE_GAP"
    assert any(
        i["issue_type"] == "UNCOVERED_LEFT_INTERVAL_ENDPOINT" for i in aud_lg_ex["coverage_issues"]
    )

    # 3. Section 5.3: Coverage at `exp(6)` on `(1809, 6, 6)` (`A = [exp(6), 20173/50]`) respects
    #    exact ownership and cannot be supplied solely by decimal padding or neighboring `(1809, 5, 5)`:
    flint_ctx.prec = 220
    q_gt_e6 = _exact_arb_endpoints_as_fractions(arb(6).exp())[1]
    flint_ctx.prec = 512
    assert _q_arb(q_gt_e6) > arb(6).exp()
    flint_ctx.prec = 256
    mid_e6_q = q_gt_e6 + Fraction(1, 32)
    sh_e6 = mid_e6_q.denominator.bit_length() - 1
    B_e6_gap = arb(arf((mid_e6_q.numerator, -sh_e6)), arf(((1 << 31) - 1, -36)))  # rad = 2^-5
    e6_bin_lo, e6_bin_hi = _exact_arb_endpoints_as_fractions(B_e6_gap)
    assert e6_bin_lo == q_gt_e6 and e6_bin_hi > Fraction(20173, 50)
    ser_e6_gap = _ser(B_e6_gap)
    flint_ctx.prec = 512
    assert _q_arb(Fraction(ser_e6_gap["lower_dec"])) < arb(6).exp()
    flint_ctx.prec = 256

    s_e6_pad = json.loads(json.dumps(s_base))
    sp_e6p = s_e6_pad["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]
    # Widen neighboring `(1809, 5, 5)` well past `exp(6)` (`[403.42, 403.44]`, wrong cutoff `D0 = 5`):
    sp_e6p["branches"][1].pop("historical_domain_reconstruction", None)
    sp_e6p["branches"][1]["Y_sub_ball"] = _ser(
        _q_arb(Fraction(40342, 100)).union(_q_arb(Fraction(40344, 100)))
    )
    sp_e6p["branches"][1]["evaluated_Y_interval_exact_fractions"] = ["40342/100", "40344/100"]
    sp_e6p["branches"][2].pop("historical_domain_reconstruction", None)
    sp_e6p["branches"][2]["Y_sub_ball"] = ser_e6_gap
    g_e6p, _ = _both(s_e6_pad, "exp6_decimal_padding_and_neighbor_rejected")
    assert g_e6p["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    aud_e6p = g_e6p["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_split_audits"]["interval_403_40_to_403_46_across_e6"]
    assert aud_e6p["branch_domain_admissibility"][2]["complete_subdomain_coverage"] is False
    assert aud_e6p["branch_domain_admissibility"][2]["coverage_status"] == "UNCERTIFIED_COVERAGE"

    s_e6_pad_ex = json.loads(json.dumps(s_e6_pad))
    s_e6_pad_ex["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]["branches"][2]["evaluated_Y_interval_exact_fractions"] = [
        f"{e6_bin_lo.numerator}/{e6_bin_lo.denominator}",
        f"{e6_bin_hi.numerator}/{e6_bin_hi.denominator}",
    ]
    g_e6p_ex, _ = _both(s_e6_pad_ex, "exp6_exact_gap_rejected")
    aud_e6p_ex = g_e6p_ex["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_split_audits"]["interval_403_40_to_403_46_across_e6"]
    assert aud_e6p_ex["branch_domain_admissibility"][2]["coverage_status"] == "PROVED_COVERAGE_GAP"

    # 4. Section 5.4: Tiny interior gap (`2^-201`) cannot disappear through a rounded union
    #    (`evaluated_Y_subintervals_exact_fractions` inside one branch AND across adjacent branches):
    p1_hi = Fraction(625, 1) - Fraction(1, 8192) - Fraction(1, 1 << 201)
    p2_lo = Fraction(625, 1) - Fraction(1, 8192)
    b_hull = _q_arb(a_lo_q).union(_q_arb(a_hi_q))
    s_multi_gap = json.loads(json.dumps(s_base))
    sp_mg = s_multi_gap["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_mg["branches"][0].pop("historical_domain_reconstruction", None)
    sp_mg["branches"][0]["Y_sub_ball"] = _ser(b_hull)
    sp_mg["branches"][0]["evaluated_Y_subintervals_exact_fractions"] = [
        [f"{a_lo_q.numerator}/{a_lo_q.denominator}", f"{p1_hi.numerator}/{p1_hi.denominator}"],
        [f"{p2_lo.numerator}/{p2_lo.denominator}", "625"],
    ]
    g_mg, _ = _both(s_multi_gap, "multi_piece_tiny_interior_gap")
    assert g_mg["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    aud_mg = g_mg["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_split_audits"]["interval_625_pm_2_neg12_across_T3125"]
    assert aud_mg["branch_domain_admissibility"][0]["complete_subdomain_coverage"] is False
    assert aud_mg["branch_domain_admissibility"][0]["coverage_status"] == "PROVED_COVERAGE_GAP"
    assert (
        aud_mg["branch_domain_admissibility"][0]["coverage_reason"]
        == "UNBRIDGED_INTERIOR_GAP_IN_EVALUATED_PIECES"
    )
    assert any(i["issue_type"] == "INTERIOR_SUBDOMAIN_GAP" for i in aud_mg["coverage_issues"])

    # Touching multi-piece union WITHOUT gap (`hi_1 == lo_2`) passes cleanly:
    s_multi_ok = json.loads(json.dumps(s_multi_gap))
    s_multi_ok["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["branches"][0]["evaluated_Y_subintervals_exact_fractions"] = [
        [f"{a_lo_q.numerator}/{a_lo_q.denominator}", f"{p2_lo.numerator}/{p2_lo.denominator}"],
        [f"{p2_lo.numerator}/{p2_lo.denominator}", "625"],
    ]
    g_mok, _ = _both(s_multi_ok, "multi_piece_touching_valid")
    assert g_mok["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert g_mok["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"

    # 5. Section 5.5: Valid fully covering exact evaluation domain (`evaluated_Y_symbolic_bounds`
    #    on `exp(6)` + live `evaluate_interval_via_cutoff_case_split_arb` output) passes:
    s_sym_ok = json.loads(json.dumps(s_base))
    sp_sok = s_sym_ok["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]
    sp_sok["branches"][2].pop("historical_domain_reconstruction", None)
    e6_cov_ball = arb(6).exp().lower().union(_q_arb(Fraction(20173, 50)).upper())
    e6_cov_lo, e6_cov_hi = _exact_arb_endpoints_as_fractions(e6_cov_ball)
    sp_sok["branches"][2]["Y_sub_ball"] = _ser(e6_cov_ball)
    sp_sok["branches"][2]["evaluated_Y_interval_exact_fractions"] = [
        f"{e6_cov_lo.numerator}/{e6_cov_lo.denominator}",
        f"{e6_cov_hi.numerator}/{e6_cov_hi.denominator}",
    ]
    g_sok, _ = _both(s_sym_ok, "valid_exact_covering_exp6")
    assert g_sok["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert g_sok["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"
    assert g_sok["all_mathematical_and_numerical_checks_pass"] is True

    live_sp = evaluate_interval_via_cutoff_case_split_arb(
        Fraction(159, 10), Fraction(161, 10), prec_bits=128, quad_tol_bits=40
    )
    for br_live in live_sp["branches"]:
        ef_live = br_live["evaluated_Y_interval_exact_fractions"]
        ys_live_lo, ys_live_hi = _exact_arb_endpoints_as_fractions(br_live["Y_sub_ball"])
        assert ys_live_lo <= Fraction(ef_live[0]) <= Fraction(ef_live[1]) <= ys_live_hi

    # 6. Section 4 & 5.6: Justified recovered legacy domains on all 5 branches pass with `0`
    #    numerical margin changes:
    raw_tc062r3 = _load_git_json_artifact_or_none(
        REVIEWED_TC062R3_DELIVERED_TIP, "data/tc_joint_prime_dilation_signed_remainder.json"
    )
    assert raw_tc062r3 is not None
    p_unmig = tmp_path / "raw_tc062r3.json"
    p_unmig.write_text(json.dumps(raw_tc062r3), encoding="utf-8")
    r_unmig = reprocess_task_tc062_metadata_and_stage_b(p_unmig, write_output=False)
    assert r_unmig["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert r_unmig["execution_and_certification_status"] == "INCOMPLETE_HOLDOUT_COVERAGE"

    r_rec = reprocess_task_tc062_metadata_and_stage_b(
        p_unmig, write_output=False, reconstruct_legacy_interval_domains=True
    )
    assert r_rec["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert r_rec["execution_and_certification_status"] == "CERTIFIED_EVALUATION_COMPLETE"
    assert r_rec["all_mathematical_and_numerical_checks_pass"] is True
    rec_tbl = r_rec["provenance"]["tc062r4_legacy_domain_reconstruction_summary"][
        "five_branch_domain_evidence_table"
    ]
    assert len(rec_tbl) == 5
    assert all(
        row["pre_reconstruction_coverage_status"] == "UNCERTIFIED_COVERAGE"
        and row["margin_status"] == "PRESERVED_WITHOUT_RECOMPUTATION"
        and row["stored_Y_sub_ball_5field_exact_match"] is True
        for row in rec_tbl
    )
    comp_rec = compare_tc062_artifacts_by_stable_key(
        r_rec, raw_tc062r3, baseline_commit=REVIEWED_TC062R3_DELIVERED_TIP
    )
    assert comp_rec["changed_numerical_enclosures_count"] == 0
    assert comp_rec["enclosure_comparison_complete"] is True
    assert comp_rec["any_numerical_enclosure_changed_on_comparable_balls"] is False

    # 7. Section 5.7: Deleting or invalidating domain evidence on ANY of the 5 branches cannot
    #    silently preserve complete coverage across generator or `--reprocess-metadata`:
    branch_locs = [
        ("interval_625_pm_2_neg12_across_T3125", 0),
        ("interval_625_pm_2_neg12_across_T3125", 1),
        ("interval_403_40_to_403_46_across_e6", 0),
        ("interval_403_40_to_403_46_across_e6", 1),
        ("interval_403_40_to_403_46_across_e6", 2),
    ]
    for sk_loc, b_i in branch_locs:
        s_del_hdr = json.loads(json.dumps(s_base))
        s_del_hdr["continuous_straddling_interval_splits"][sk_loc]["branches"][b_i].pop(
            "historical_domain_reconstruction", None
        )
        g_dh, r_dh = _both(s_del_hdr, f"del_hdr_{sk_loc}_{b_i}")
        assert g_dh["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
        assert (
            "historical_domain_reconstruction"
            not in r_dh["section_5_unseen_validation_and_interval_splits"][
                "continuous_straddling_interval_splits"
            ][sk_loc]["branches"][b_i]
        )

        s_bad_hdr = json.loads(json.dumps(s_base))
        s_bad_hdr["continuous_straddling_interval_splits"][sk_loc]["branches"][b_i][
            "historical_domain_reconstruction"
        ]["reconstructed_sub_ball_exact_dyadic_fractions"] = ["2", "3"]
        g_bh, _ = _both(s_bad_hdr, f"bad_hdr_{sk_loc}_{b_i}")
        assert g_bh["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"

    # Also verify artifact-level producer commit mismatch invalidates `historical_domain_reconstruction`:
    art_wrong_prod = json.loads(json.dumps(tc062_artifact))
    art_wrong_prod["provenance"]["numerical_producing_git_commit"] = "0" * 40
    p_wp = tmp_path / "wrong_prod_hdr.json"
    p_wp.write_text(json.dumps(art_wrong_prod), encoding="utf-8")
    r_wp = reprocess_task_tc062_metadata_and_stage_b(p_wp, write_output=False)
    assert r_wp["holdout_hypothesis_outcome"] == "CERTIFICATION_INTEGRITY_CONFLICT"

    # 8. Section 4 & 5.8: `reconstruct_tc062r_legacy_interval_domains` refuses mismatched producer,
    #    mismatched timestamp, mismatched cutoff identity, modified `Y_sub_ball`, explicit domain
    #    field, or `prec=53` serialization-collision impostor margins:
    bad_p1 = json.loads(json.dumps(raw_tc062r3))
    bad_p1["provenance"]["numerical_producing_git_commit"] = "1" * 40
    with pytest.raises(ValueError, match="REFUSED_MISMATCHED_NUMERICAL_PRODUCER"):
        reconstruct_tc062r_legacy_interval_domains(bad_p1)

    bad_ts = json.loads(json.dumps(raw_tc062r3))
    bad_ts["generated_at_utc"] = "2026-11-18T00:00:00+00:00"
    with pytest.raises(ValueError, match="REFUSED_MISMATCHED_GENERATED_AT_UTC"):
        reconstruct_tc062r_legacy_interval_domains(bad_ts)

    bad_cut = json.loads(json.dumps(raw_tc062r3))
    bad_cut["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]["branches"][0]["T_fixed"] = 3124
    bad_cut["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]["T_range"] = [3124, 3126]
    with pytest.raises(ValueError, match="REFUSED"):
        reconstruct_tc062r_legacy_interval_domains(bad_cut)

    bad_ys = json.loads(json.dumps(raw_tc062r3))
    bad_ys["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]["branches"][0]["Y_sub_ball"] = ser_right_gap
    with pytest.raises(ValueError, match="REFUSED_MODIFIED_Y_SUB_BALL_RECORD"):
        reconstruct_tc062r_legacy_interval_domains(bad_ys)

    bad_exp = json.loads(json.dumps(raw_tc062r3))
    bad_exp["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_625_pm_2_neg12_across_T3125"]["branches"][0][
        "evaluated_Y_interval_exact_fractions"
    ] = ["2559999/4096", "625"]
    with pytest.raises(ValueError, match="REFUSED_MODIFIED_EXPLICIT_DOMAIN_FIELD"):
        reconstruct_tc062r_legacy_interval_domains(bad_exp)

    # Construct a genuine 256-bit Arb impostor interval `b_impostor != yr0` on `(1808, 5, 5)` whose
    # 53-bit `serialize_arb_certified(b_impostor)` matches `ser_53` across ALL 5 serialized fields,
    # and verify that observable SHA-256 linkage defeats the serialization collision:
    rep_1808 = _replay_historical_tc062r_sub_ball(
        Fraction(2017, 5), Fraction(20173, 50), 1808, 5
    )
    saved_pr = flint_ctx.prec
    try:
        flint_ctx.prec = 320
        sub_1808 = (arb(2017) / arb(5)).lower().union((arb(1808) ** (arb(4) / arb(5))).upper())
        flint_ctx.prec = 256
        yr_1808 = +sub_1808
        ym_18, ye_18 = yr_1808.mid().man_exp()
        flint_ctx.prec = 512
        b_impostor = (yr_1808 - arb(yr_1808.mid())) + arb(arf((ym_18 + 2, ye_18)))
        assert _exact_arb_endpoints_as_fractions(b_impostor) != _exact_arb_endpoints_as_fractions(
            yr_1808
        )
        flint_ctx.prec = 53
        ser_impostor = _ser(b_impostor)
    finally:
        flint_ctx.prec = saved_pr
    assert ser_impostor == rep_1808["ser_53"]  # identical 5-field rounded serialization!

    bad_imp = json.loads(json.dumps(raw_tc062r3))
    sp_imp = bad_imp["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_403_40_to_403_46_across_e6"]
    br_imp = sp_imp["branches"][0]
    br_imp["Y_sub_ball"] = ser_impostor
    br_imp["M_P0_F"] = _ser(arb("-0.641", arb("0.001")))
    sp_imp["union_M_P0_F"] = _ser(arb("-1.0").union(arb("-0.10")))
    with pytest.raises(ValueError, match="REFUSED_MODIFIED_OR_UNLINKED_BRANCH_OBSERVABLES"):
        reconstruct_tc062r_legacy_interval_domains(bad_imp)

    # 9 & 10. Sections 5.9 & 5.10: Nonempty partial evaluated domain inside `A` (`B_outer subseteq A`
    #         with NO exact-domain field, AND exact partial domain):
    #   - With `PASS` margins: supplies an admissible witness (`can_certify_refutation = True`) yet
    #     CANNOT establish complete coverage or survival (`INCOMPLETE_OR_INVALID_COVERAGE`);
    #   - With positive `FAIL` margin (`P0` and `P0_F`): refutes (`REFUTED_BY_CERTIFIED_WITNESS`)
    #     while coverage stays incomplete (`CERTIFIED_REFUTATION_WITH_INCOMPLETE_REMAINING_GRID`):
    flint_ctx.prec = 256
    B_sub_A = _q_arb(Fraction(625, 1) - Fraction(3, 16384)).union(
        _q_arb(Fraction(625, 1) - Fraction(1, 16384))
    )
    s_part_pass = json.loads(json.dumps(s_base))
    sp_pp = s_part_pass["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_pp["branches"][0].pop("historical_domain_reconstruction", None)
    sp_pp["branches"][0]["Y_sub_ball"] = _ser(B_sub_A)
    g_pp, _ = _both(s_part_pass, "partial_domain_only_pass_margins")
    aud_pp = g_pp["section_5_unseen_validation_and_interval_splits"][
        "continuous_straddling_interval_splits"
    ]["interval_split_audits"]["interval_625_pm_2_neg12_across_T3125"]
    assert aud_pp["branch_domain_admissibility"][0]["can_certify_refutation"] is True
    assert aud_pp["branch_domain_admissibility"][0]["complete_subdomain_coverage"] is False
    assert g_pp["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"
    assert g_pp["execution_and_certification_status"] == "INCOMPLETE_HOLDOUT_COVERAGE"
    assert "SURVIVAL" not in g_pp["completion_outcome_code"]

    # Tiny `B_tiny_in_A` (`403.41 +/- 2^-201` on `(1808, 5, 5)`, where `has_nonempty_inner = False`,
    # testing the pure `B_outer subseteq A` branch!):
    B_tiny_in_A = (arb(40341) / arb(100)) + arb(0, arf(((1 << 31) - 1, -232)))
    s_tiny_pass = json.loads(json.dumps(s_base))
    sp_tp = s_tiny_pass["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]
    sp_tp["branches"][0].pop("historical_domain_reconstruction", None)
    sp_tp["branches"][0]["Y_sub_ball"] = _ser(B_tiny_in_A)
    aud_tp = audit_continuous_interval_split_certificate_tc062(
        "interval_403_40_to_403_46_across_e6",
        sp_tp,
        prescribed_Y_lo=Fraction(2017, 5),
        prescribed_Y_hi=Fraction(20173, 50),
    )
    adm_tp = aud_tp["branch_domain_admissibility"][0]
    assert (
        adm_tp["admissibility_reason"]
        == "ENTIRE_OUTWARD_EVALUATION_ENCLOSURE_SUBSET_OF_ADMISSIBLE_SUBDOMAIN"
    )
    assert adm_tp["can_certify_refutation"] is True
    assert adm_tp["complete_subdomain_coverage"] is False
    assert adm_tp["coverage_status"] == "PROVED_COVERAGE_GAP"
    g_tp, _ = _both(s_tiny_pass, "tiny_subset_of_A_pass_margins")
    assert g_tp["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    # Same `B_tiny_in_A` with positive `M_P0_F` refutes while coverage stays incomplete:
    pos_m = arb("0.20", arb("0.005"))
    pos_f = arb("0.92", arb("0.005"))
    neg_m_wide = arb("-1.0").union(arb("-0.05"))
    s_tiny_fail = json.loads(json.dumps(s_tiny_pass))
    sp_tf = s_tiny_fail["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]
    sp_tf["branches"][0]["F_Y"] = _ser(pos_f)
    sp_tf["union_F_Y"] = _ser(arb("-1.0").union(pos_f))
    sp_tf["branches"][0]["M_P0_F"] = _ser(pos_m)
    sp_tf["branches"][0]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_tf["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_tf["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_tf, _ = _both(s_tiny_fail, "tiny_subset_of_A_fail_refutes")
    assert g_tf["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
    assert (
        g_tf["execution_and_certification_status"]
        == "CERTIFIED_REFUTATION_WITH_INCOMPLETE_REMAINING_GRID"
    )
    assert g_tf["section_5_unseen_validation_and_interval_splits"]["coverage_complete"] is False

    # 11. Section 5.11: Disjoint `[2, 2]` and excluded-boundary-only `[625, 625]` on `(3126, 6, 6)`
    #     remain unable to refute:
    s_disj = json.loads(json.dumps(s_tiny_fail))
    s_disj["continuous_straddling_interval_splits"][
        "interval_403_40_to_403_46_across_e6"
    ]["branches"][0]["Y_sub_ball"] = _ser(arb(2))
    g_disj, _ = _both(s_disj, "disjoint_box_cannot_refute")
    assert g_disj["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    s_excl = json.loads(json.dumps(s_base))
    sp_ex = s_excl["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]
    sp_ex["branches"][1].pop("historical_domain_reconstruction", None)
    sp_ex["branches"][1]["Y_sub_ball"] = _ser(arb(625))
    sp_ex["branches"][1]["F_Y"] = _ser(pos_f)
    sp_ex["union_F_Y"] = _ser(arb("-0.40").union(pos_f))
    sp_ex["branches"][1]["M_P0_F"] = _ser(pos_m)
    sp_ex["branches"][1]["TC062_P0_F_branch_classification"] = {"verdict": "FAIL"}
    sp_ex["union_M_P0_F"] = _ser(neg_m_wide.union(pos_m))
    sp_ex["TC062_P0_F_interval_classification"] = {"verdict": "UNRESOLVED"}
    g_excl, _ = _both(s_excl, "excluded_625_on_3126_cannot_refute")
    assert g_excl["holdout_hypothesis_outcome"] == "INCOMPLETE_OR_INVALID_COVERAGE"

    # 12. Section 5.12: Separate `WITHIN` / `EXCEEDED` / `UNKNOWN` resource statuses retain semantics:
    s_res_exc = json.loads(json.dumps(s_base))
    s_res_exc["holdout_point_evaluations"][0]["tier_escalation_history"][0][
        "peak_rss_mb"
    ] = 99999.0
    g_rexc, _ = _both(s_res_exc, "resource_exceeded")
    assert g_rexc["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert g_rexc["resource_compliance_status"] == "EXCEEDED"
    assert (
        g_rexc["execution_and_certification_status"]
        == "CERTIFIED_EVALUATION_COMPLETE_RESOURCE_BUDGET_EXCEEDED"
    )
    assert g_rexc["all_mathematical_and_numerical_checks_pass"] is False

    s_res_unk = json.loads(json.dumps(s_base))
    s_res_unk["holdout_point_evaluations"][0]["tier_escalation_history"][0][
        "peak_rss_measurement_semantics"
    ] = "TIER_LOCAL_SNAPSHOT"
    g_runk, _ = _both(s_res_unk, "resource_unknown")
    assert g_runk["holdout_hypothesis_outcome"] == "SURVIVED_TESTED_POINTS"
    assert g_runk["resource_compliance_status"] == "UNKNOWN"
    assert (
        g_runk["execution_and_certification_status"]
        == "CERTIFIED_EVALUATION_COMPLETE_RESOURCE_TELEMETRY_UNKNOWN"
    )
    assert g_runk["all_mathematical_and_numerical_checks_pass"] is False

    # 13. Section 5.13: Repeated metadata reprocessing is semantically idempotent modulo
    #     `provenance.tc062r4_reprocessed_at_utc`:
    p_id = tmp_path / "tc062r4_idem.json"
    p_id.write_bytes(JOINT_PRIME_DILATION_ARTIFACT_PATH.read_bytes())
    out_1 = reprocess_task_tc062_metadata_and_stage_b(p_id, write_output=True)
    out_2 = reprocess_task_tc062_metadata_and_stage_b(p_id, write_output=True)
    d_1 = json.loads(json.dumps(out_1))
    d_2 = json.loads(json.dumps(out_2))
    t_1 = d_1["provenance"].pop("tc062r4_reprocessed_at_utc")
    t_2 = d_2["provenance"].pop("tc062r4_reprocessed_at_utc")
    assert isinstance(t_1, str) and isinstance(t_2, str)
    assert d_1 == d_2




