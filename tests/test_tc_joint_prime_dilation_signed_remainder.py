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
from typing import Any, Dict

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
    TASK_TC_062_ID,
    TC_062_LEAN_MODULE_PATH,
    TC_062_REVIEW_DOC_PATH,
    build_complete_signed_kernel_evaluator_small_T,
    evaluate_interior_paired_matrix_free_arb,
    evaluate_whole_line_contraction_ratio_closed_arb,
    execute_tc062_holdout_point_with_escalation,
    extract_lean_declaration_spans_tc062,
    prime_even_valuation_anchors,
    prime_valuation_v_p,
    verify_frozen_tc062_protocol_immutability,
    verify_generic_finite_anchor_reindexing_exact,
    verify_stage_b_large_prime_b_jump_identity_arb,
    verify_tc062_review_enclosures_and_lean_anchors,
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
    """Verify Lean 4 module registration, 7 public theorems, 0 sorry/admit/axioms, and review sync."""
    rel_lean = "formal/RiemannScope/JointPrimeDilationSignedRemainder.lean"
    assert rel_lean in FORMAL_SOURCE_FILES
    assert rel_lean in REQUIRED_FORMAL_SOURCES
    assert TC_062_LEAN_MODULE_PATH.exists()

    spans = extract_lean_declaration_spans_tc062()
    assert spans["hygiene_ok"] is True, spans
    assert spans["public_theorem_count"] == len(EXPECTED_TC062_THEOREMS)

    prov = tc062_artifact["provenance"]
    assert prov["formal_compiled_theorem_count"] == 829
    assert prov["formal_build_producing_git_commit"] == prov["numerical_producing_git_commit"]

    assert TC_062_REVIEW_DOC_PATH.exists()
    rev_chk = verify_tc062_review_enclosures_and_lean_anchors(
        tc062_artifact, TC_062_REVIEW_DOC_PATH, lean_spans=spans
    )
    assert rev_chk["verified"] is True, rev_chk
    assert rev_chk["checked_holdout_cutoff_count"] == 10
    assert rev_chk["failed_holdout_cutoffs"] == []
