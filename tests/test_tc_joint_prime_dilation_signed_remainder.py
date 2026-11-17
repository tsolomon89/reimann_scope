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

from flint import arb, ctx as flint_ctx
import pytest

from certification import REQUIRED_FORMAL_SOURCES
from scripts.build_formal import FORMAL_SOURCE_FILES
from tc.dyadic_power_lift_primitive_correlation import EPISTEMIC_CATEGORIES, PARENT_SUBGATE_ID
from tc.joint_prime_dilation_signed_remainder import (
    ACCEPTED_TC061R3_IMPLEMENTATION,
    ACCEPTED_TC061R3_TIP,
    EXPECTED_TC062_THEOREMS,
    FROZEN_TC062_PROTOCOL_ID,
    FROZEN_TC062_PROTOCOL_REGISTRATION_COMMIT,
    FROZEN_TC062_PROTOCOL_SHA256,
    GLOBAL_CONSEQUENCE_CLASSES,
    JOINT_PRIME_DILATION_ARTIFACT_PATH,
    JOINT_PRIME_DILATION_PROTOCOL_PATH,
    REVIEWED_TC062_IMPLEMENTATION,
    REVIEWED_TC062_PRODUCING_COMMIT,
    REVIEWED_TC062_TIP,
    REVIEWED_TC062R_DELIVERED_TIP,
    REVIEWED_TC062R_PRODUCING_COMMIT,
    TASK_TC_062_ID,
    TASK_TC_062R_ID,
    TASK_TC_062R2_ID,
    TC_062_LEAN_MODULE_PATH,
    TC_062_REVIEW_DOC_PATH,
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

    assert tc062_artifact["repair_task_id"] == TASK_TC_062R_ID
    prov = tc062_artifact["provenance"]
    assert prov["reviewed_tc062_tip"] == REVIEWED_TC062_TIP
    assert prov["reviewed_tc062_implementation"] == REVIEWED_TC062_IMPLEMENTATION
    assert prov["prior_tc062_producing_commit"] == REVIEWED_TC062_PRODUCING_COMMIT
    assert prov["formal_compiled_theorem_count"] == 830
    assert prov["formal_build_producing_git_commit"] == prov["numerical_producing_git_commit"]
    inv62 = prov["tc062r_certificate_impact_inventory"]
    assert inv62["policy"] == "OPTION_A_FULL_RECOMPUTATION_WITH_REPAIRED_ZONE1_EVALUATORS"
    assert inv62["prior_tc062_baseline_commit"] == REVIEWED_TC062_TIP
    assert inv62["recomputed_producing_git_commit"] == prov["numerical_producing_git_commit"]
    assert inv62["candidate_a2_Y64_counterexample_unaffected"] is True
    assert inv62["any_probe_kl1_control_or_candidate_verdict_changed"] is False
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

    # 1c. Changed mathematical verdict across probe, control, Candidate A2, and interval branch:
    mut_v = json.loads(json.dumps(base_art))
    mut_v["section_2_disjoint_prime_decompositions_and_controls"]["matched_control_F_grid_rows"][
        -1
    ]["TC062_P0_F_verdict"] = "PASS"
    mut_v["section_4_quantitative_proof_attempt"][
        "candidate_a2_unsigned_paired_block_majorant_refutation"
    ]["verdict"] = "SURVIVED_TESTED_POINTS"
    mut_v["section_5_unseen_validation_and_interval_splits"]["global_candidate_outcomes"][
        "KL1_int2_offdiag"
    ] = "REFUTED_BY_CERTIFIED_WITNESS"
    pos_m = strip_enclosure_arb_for_json(serialize_arb_certified(arb("0.15")))
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

    # 1d. Missing / renamed entry -> INCOMPLETE_COMPARISON and None (never False):
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


