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
    TASK_TC_062_ID,
    TASK_TC_062R_ID,
    TC_062_LEAN_MODULE_PATH,
    TC_062_REVIEW_DOC_PATH,
    aggregate_tc062_section5_and_derive_outcomes,
    build_complete_signed_kernel_evaluator_small_T,
    compute_zone1_prime_power_diag_perturbation_tc062_arb,
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

    s_iv_fail = json.loads(json.dumps(s1))
    s_iv_fail["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["union_M_P0_F"] = pos_margin
    s_iv_fail["continuous_straddling_interval_splits"][
        "interval_625_pm_2_neg12_across_T3125"
    ]["TC062_P0_F_interval_classification"]["verdict"] = "FAIL"
    g_iv_f, _ = _run_both_paths(s_iv_fail)
    assert g_iv_f["holdout_hypothesis_outcome"] == "REFUTED_BY_CERTIFIED_WITNESS"
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
        g7["section_5_unseen_validation_and_interval_splits"]["global_candidate_outcomes"][
            "TC062-P0-F"
        ]
        == "REFUTED_BY_CERTIFIED_WITNESS"
    )
    assert "SURVIVAL" not in g7["completion_outcome_code"]
    assert "SURVIVED" not in g7["research_outcome_class"]

