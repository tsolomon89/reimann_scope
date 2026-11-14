"""Focused mathematical, falsification, formalization, and 256-bit Arb certification test suite
for TASK-TC-060: Signed Dilation Multipliers and Arithmetic Control of the Complete Reconstruction.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re

from flint import acb, arb, ctx as flint_ctx
import pytest

import certification
from scripts import build_formal
from tc.canonical_theta_correlation_bound import REPO_ROOT
from tc.coupled_scale_energy_bootstrap import (
    _frac_to_arb,
    _tau_arb,
    evaluate_Q_shifted_finite_arb,
)
from tc.dyadic_power_lift_primitive_correlation import (
    EPISTEMIC_CATEGORIES,
    PARENT_SUBGATE_ID,
    REVIEWED_MERGED_MAIN_BASELINE,
    evaluate_Q_general_arb,
    is_perfect_square_int,
)
from tc.liouville_square_dilation import liouville_lambda_int
from tc.prime_chain_contraction import evaluate_phi_n_arb
import tc.signed_dilation_arithmetic_energy as tc060_mod
from tc.signed_dilation_arithmetic_energy import (
    ACCEPTED_TC059R2_BRANCH,
    EXPECTED_TC060_THEOREMS,
    GLOBAL_CONSEQUENCE_CLASSES,
    INHERITED_FORMAL_PRODUCING_COMMIT,
    PROPOSED_TC060_BRANCH,
    REVIEWED_TC059R2_HEAD,
    REVIEWED_TC059R2_IMPLEMENTATION,
    SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH,
    TASK_TC_060_ID,
    TC_060_LEAN_MODULE_PATH,
    TC_060_REVIEW_DOC_PATH,
    classify_arb_le_certificate,
    classify_interval_endpoints_le,
    compute_selberg_centered_remainder_table_arb,
    compute_smooth_basis_coefficients_arb,
    cutoff_level_blocks_exact,
    evaluate_adjacent_multiplier_m_d_acb,
    evaluate_c_half_square_pole_arb,
    evaluate_qhat_L_closed_acb,
    evaluate_qhat_L_direct_quadrature_acb,
    evaluate_signed_gram_H_closed_arb,
    evaluate_smooth_jump_endpoint_reconstruction_arb,
    evaluate_square_pole_drift_M_arb,
    evaluate_weighted_window_kernel_K_quadrature_arb,
    verify_tc060_review_displayed_enclosures,
)


@pytest.fixture(scope="module")
def tc060_artifact() -> dict:
    assert SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH.exists(), (
        f"Missing {SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH}"
    )
    return json.loads(
        SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH.read_text(encoding="utf-8")
    )


def test_artifact_metadata_provenance_and_epistemic_hygiene(tc060_artifact: dict) -> None:
    """Verify baseline provenance SHAs, gate status, tau-only convention, global consequence
    classes, and 256-bit Arb serialization self-check.
    """
    assert tc060_artifact["task_id"] == TASK_TC_060_ID
    assert tc060_artifact["parent_subgate"] == PARENT_SUBGATE_ID
    assert tc060_artifact["reviewed_merged_main_baseline"] == REVIEWED_MERGED_MAIN_BASELINE
    assert tc060_artifact["accepted_tc059r2_branch"] == ACCEPTED_TC059R2_BRANCH
    assert tc060_artifact["reviewed_tc059r2_implementation_commit"] == REVIEWED_TC059R2_IMPLEMENTATION
    assert tc060_artifact["reviewed_tc059r2_head_commit"] == REVIEWED_TC059R2_HEAD
    assert tc060_artifact["inherited_formal_producing_commit"] == INHERITED_FORMAL_PRODUCING_COMMIT
    assert tc060_artifact["branch"] == PROPOSED_TC060_BRANCH
    assert tc060_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc060_artifact["rh_proved"] is False
    assert tc060_artifact["precision_bits"] == 256
    assert tc060_artifact["epistemic_categories_enforced"] == list(EPISTEMIC_CATEGORIES)
    assert tc060_artifact["global_consequence_classes_enforced"] == list(GLOBAL_CONSEQUENCE_CLASSES)
    assert "z = x + i*y" in tc060_artifact["complex_coordinate_convention"]
    assert "w = u + i*v" in tc060_artifact["complex_coordinate_convention"]

    arb_self = tc060_artifact["serialized_arb_self_check"]
    assert arb_self["all_enclose_original_256bit_arb_ball"] is True
    assert arb_self["total_certified_arb_balls_checked"] >= 330

    for chk_path in (
        TC_060_LEAN_MODULE_PATH,
        REPO_ROOT / "tc" / "signed_dilation_arithmetic_energy.py",
        SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH,
        TC_060_REVIEW_DOC_PATH,
    ):
        txt = chk_path.read_text(encoding="utf-8")
        assert "\u03c0" not in txt, f"Forbidden Unicode circle-half glyph in {chk_path}"
        assert len(re.findall(r"\x5cpi(?![a-zA-Z])", txt)) == 0, (
            f"Forbidden LaTeX circle-half macro in {chk_path}"
        )


def test_section_1_noncircular_reassembly_boundary_guards_and_2T_spillover(
    tc060_artifact: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify Section 1: R(0)=0, R(1)=-c_lambda>0, T=0 phi_0 guard, T=1 endpoint identity,
    general T>=1 non-circularity reassembly, return to D_{2,T} = P_T - R_T, Y>=2 log-division guard,
    and exact 2T basis spillover alpha_T(2T) = c_lambda * lambda(T) != 0.
    """
    sec1 = tc060_artifact["section_1_exact_object_and_noncircular_reassembly"]
    assert sec1["all_section_1_checks_pass"] is True
    assert sec1["T_0_empty_without_phi_0_verified"] is True
    assert sec1["R_0_is_exact_zero"] is True
    assert sec1["R_1_strictly_positive"] is True

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tbl = compute_selberg_centered_remainder_table_arb(20, prec_bits=256)
        c_lam = tbl["c_lambda"]
        R = tbl["R"]
        assert R[0] == arb(0)
        assert bool(arb(0) in (R[1] - (-c_lam)) and R[1] > arb(0))

        # Guard: evaluate_phi_n_arb must never be called with n = 0 at T = 0
        orig_phi = tc060_mod.evaluate_phi_n_arb

        def _guarded_phi(X_val, n_val, *args, **kwargs):
            if n_val == 0:
                raise AssertionError("Forbidden evaluation of phi_0!")
            return orig_phi(X_val, n_val, *args, **kwargs)

        monkeypatch.setattr(tc060_mod, "evaluate_phi_n_arb", _guarded_phi)
        rec_0 = evaluate_smooth_jump_endpoint_reconstruction_arb(
            Fraction(7, 3), 0, R_table=R, prec_bits=256
        )
        assert all(v == arb(0) for v in rec_0.values())

        # Weighted log kernel must reject Y < 2
        with pytest.raises(ValueError, match="Y >= 2"):
            evaluate_weighted_window_kernel_K_quadrature_arb(Fraction(3, 2), 1, 1, prec_bits=256)

        # Independent out-of-grid reassembly check at X = 7/3 > 2, T = 9
        x_val = _frac_to_arb(Fraction(7, 3))
        T_val = 9
        rec_9 = evaluate_smooth_jump_endpoint_reconstruction_arb(
            x_val, T_val, R_table=R, prec_bits=256
        )
        rhs_9 = arb(0)
        q_sq_9 = arb(0)
        for n in range(1, T_val + 1):
            phi_n = evaluate_phi_n_arb(x_val, n, prec_bits=256)
            rhs_9 += arb(liouville_lambda_int(n)) * ((arb(n).log()) ** 2) * phi_n
            if is_perfect_square_int(n):
                q_sq_9 += phi_n
        rhs_9 -= c_lam * q_sq_9
        diff_9 = rec_9["total_reassembled"] - rhs_9
        assert bool(arb(0) in diff_9 and abs(diff_9) < arb("1e-70"))

        # Return to D_{2,9}(X) and Q_{lambda,9}(X) = 2*P_9(X) - D_{2,9}(X)
        lg_x = x_val.log()
        q_lam_9 = evaluate_Q_general_arb(x_val, T_val, coeff_fn=liouville_lambda_int, prec_bits=256)
        q_sh1 = evaluate_Q_shifted_finite_arb(x_val, T_val, m_shift=1, mode="liouville")
        q_sh2 = evaluate_Q_shifted_finite_arb(x_val, T_val, m_shift=2, mode="liouville")
        P_9 = q_lam_9 - q_sh1 / lg_x
        D2_9 = (c_lam * q_sq_9 + rec_9["total_reassembled"] - q_sh2) / (lg_x ** 2)
        assert bool(arb(0) in (q_lam_9 - (arb(2) * P_9 - D2_9)) and abs(q_lam_9 - (arb(2) * P_9 - D2_9)) < arb("1e-70"))

        # Exact 2T basis spillover alpha_T(2T) = c_lambda * lambda(T) != 0
        for T_sp in (2, 3, 5, 12):
            alpha = compute_smooth_basis_coefficients_arb(T_sp, R_table=R, prec_bits=256)
            expected_2T = c_lam * arb(liouville_lambda_int(T_sp))
            assert bool(arb(0) in (alpha[2 * T_sp] - expected_2T) and abs(alpha[2 * T_sp]) > arb(1))
            r_sm_basis = sum(
                (alpha[n] * evaluate_phi_n_arb(x_val, n, prec_bits=256) for n in range(1, 2 * T_sp + 1)),
                arb(0),
            )
            r_sm_direct = evaluate_smooth_jump_endpoint_reconstruction_arb(
                x_val, T_sp, R_table=R, prec_bits=256
            )["r_sm"]
            assert bool(arb(0) in (r_sm_basis - r_sm_direct) and abs(r_sm_basis - r_sm_direct) < arb("1e-70"))
    finally:
        flint_ctx.prec = saved


def test_section_2_fourier_qhat_sharp_multiplier_cutoff_blocks_and_gram_kernels(
    tc060_artifact: dict,
) -> None:
    """Verify Section 2: finite-L Fourier identity against improper real-line quadrature + tails,
    elementary multiplier benchmark and exact odd-harmonic attainment, level-set blocks including
    empty I_1(2) and 63 blocks at T=1024, and unweighted/weighted Gram kernels across window bases.
    """
    sec2 = tc060_artifact["section_2_signed_dilation_fourier_and_gram_kernel"]
    assert sec2["all_section_2_checks_pass"] is True
    blk_rows = {r["T"]: r for r in sec2["cutoff_block_partition_checks"]}
    assert blk_rows[2]["empty_block_count"] == 1
    assert blk_rows[1024]["nonempty_block_count"] == 63
    assert blk_rows[1024]["sqrt_T_minus_1_lower_bound"] == 31
    assert blk_rows[1024]["partition_and_singleton_verified"] is True

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau = _tau_arb()

        # Out-of-grid Fourier identity check at (L = 7, v = 5/3)
        qhat_cl = evaluate_qhat_L_closed_acb(7, Fraction(5, 3), prec_bits=256)
        qhat_qu = evaluate_qhat_L_direct_quadrature_acb(7, Fraction(5, 3), prec_bits=256)
        diff_q = qhat_cl - qhat_qu
        assert bool(arb(0) in diff_q.real and arb(0) in diff_q.imag and abs(diff_q) < arb("1e-60"))

        # Sharp unrestricted-frequency odd-harmonic attainment |m_d(v_k(d))| = d^{-1/2} + (d+1)^{-1/2}
        for d_val in (1, 3, 10):
            sup_bound = arb(1) / arb(d_val).sqrt() + arb(1) / arb(d_val + 1).sqrt()
            step_log = (arb(1) + arb(1) / arb(d_val)).log()
            for k_harm in (0, 1, 2):
                v_k = arb(2 * k_harm + 1) * tau / (arb(2) * step_log)
                m_at_vk = abs(evaluate_adjacent_multiplier_m_d_acb(d_val, v_k, prec_bits=256))
                assert bool(arb(0) in (m_at_vk - sup_bound) and abs(m_at_vk - sup_bound) < arb("1e-70"))

            # Low-frequency benchmark check at v = 1/3
            v_low = arb(1) / arb(3)
            m_low = abs(evaluate_adjacent_multiplier_m_d_acb(d_val, v_low, prec_bits=256))
            int_t32 = arb(2) * (arb(1) / arb(d_val).sqrt() - arb(1) / arb(d_val + 1).sqrt())
            lip_bound = (arb(1) / arb(4) + v_low * v_low).sqrt() * int_t32
            assert bool(lip_bound < sup_bound and m_low <= lip_bound)

        # Level-set cutoff blocks exactness
        b2 = cutoff_level_blocks_exact(2)
        assert b2[1] == [] and b2[2] == [1]
        b10 = cutoff_level_blocks_exact(10)
        assert sorted(d for ds in b10.values() for d in ds) == list(range(1, 10))
        tbl_10 = compute_selberg_centered_remainder_table_arb(10, prec_bits=256)
        R10 = tbl_10["R"]
        v_chk = Fraction(3, 2)
        f_blocks = acb(0)
        for L_key, ds in b10.items():
            M_L = sum(
                (acb(R10[d]) * evaluate_adjacent_multiplier_m_d_acb(d, v_chk, prec_bits=256) for d in ds),
                acb(0),
            )
            f_blocks += M_L * evaluate_qhat_L_closed_acb(L_key, v_chk, prec_bits=256)
        f_direct = sum(
            (
                acb(R10[d])
                * evaluate_adjacent_multiplier_m_d_acb(d, v_chk, prec_bits=256)
                * evaluate_qhat_L_closed_acb(10 // d, v_chk, prec_bits=256)
                for d in range(1, 10)
            ),
            acb(0),
        )
        assert bool(
            arb(0) in (f_blocks - f_direct).real
            and arb(0) in (f_blocks - f_direct).imag
            and abs(f_blocks - f_direct) < arb("1e-70")
        )

        # Out-of-grid window base multiplier b = 7/4 at noninteger Y = 5/2, T = 4:
        b_7_4 = arb(7) / arb(4)
        y_5_2 = arb(5) / arb(2)
        gram_sum = arb(0)
        for d in range(1, 4):
            for e in range(1, 4):
                gram_sum += R10[d] * R10[e] * evaluate_signed_gram_H_closed_arb(
                    y_5_2, d, e, 4, base_mult=b_7_4, prec_bits=256
                )
        assert bool(gram_sum > arb(0))
    finally:
        flint_ctx.prec = saved


def test_section_3_gamma_majorant_obstructions_counterexamples_and_drift_contraction(
    tc060_artifact: dict,
) -> None:
    """Verify Section 3: all-v closed-form Gamma majorant, z = 1/2 square-pole drift obstruction
    (R(d) > 0 across 1..2000 with 0 flips vs 178 flips of R_osc), product compensation in H_16(8,1),
    rational & Liouville counterexamples to Candidate B1, and discrete Abel drift contraction.
    """
    sec3 = tc060_artifact["section_3_attempts_a_and_b_obstructions_and_drift_theorem"]
    assert sec3["all_section_3_checks_pass"] is True

    obs_a1 = sec3["candidate_a1_obstruction_and_square_pole_drift"]
    assert obs_a1["verified"] is True
    assert obs_a1["all_R_d_strictly_positive_1_to_2000"] is True
    assert obs_a1["R_d_sign_flips_1_to_2000"] == 0
    assert obs_a1["R_osc_sign_flips_1_to_2000"] == 178
    assert obs_a1["all_delta_drift_le_12_log_d1_over_sqrt_d_certified"] is True

    b1 = sec3["attempt_b_product_compensation_and_candidate_b1_counterexamples"]
    assert b1["verified"] is True
    assert b1["product_compensation_ratio_gt_2_certified"] is True
    assert float(b1["abs_H_16_8_1_over_H_16_8_8"]["lower_dec"]) > 2.26
    assert float(b1["steep_tail_Y16_d4_L2_a_1_0_scaled_ratio"]["lower_dec"]) > 819.0
    assert float(b1["resonant_bulk_Y16_d16_L2_scaled_ratio"]["upper_dec"]) < float(
        b1["resonant_bulk_Y16_d16_L3_scaled_ratio"]["lower_dec"]
    )
    assert float(b1["resonant_bulk_Y16_d16_L3_scaled_ratio"]["upper_dec"]) < float(
        b1["resonant_bulk_Y16_d16_L4_scaled_ratio"]["lower_dec"]
    )
    assert float(b1["actual_liouville_Y4_d1_T6_scaled_ratio"]["lower_dec"]) > 2.97
    assert float(b1["actual_liouville_Y16_d5_T32_scaled_ratio"]["lower_dec"]) > 3.08

    for d_row in sec3["informed_replacement_drift_and_small_divisor_rows"]:
        assert d_row["verified"] is True

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau = _tau_arb()
        c_half = evaluate_c_half_square_pole_arb(prec_bits=256)
        assert bool(-arb(2) < c_half < -arb(1))
        for d_chk in (2, 3, 5, 50):
            assert bool(evaluate_square_pole_drift_M_arb(d_chk, c_half_arb=c_half, prec_bits=256) > arb(0))
            delta_m = (
                evaluate_square_pole_drift_M_arb(d_chk, c_half_arb=c_half, prec_bits=256)
                - evaluate_square_pole_drift_M_arb(d_chk - 1, c_half_arb=c_half, prec_bits=256)
            )
            bound_m = arb(12) * arb(d_chk + 1).log() / arb(d_chk).sqrt()
            assert bool(bound_m - abs(delta_m) > arb(0))

        # Direct all-v Gamma majorant verification across v in {0, 1/2, 4, 25}:
        # exact algebraic equality at v = 0, strict directed inequality for v != 0.
        pref_g = (arb(2) ** (arb(3) / arb(2))) * (arb(5) / arb(4)).gamma()
        for v_num, v_den in ((0, 1), (1, 2), (4, 1), (25, 1)):
            v_a = arb(v_num) / arb(v_den)
            lhs_g = abs(acb(arb(5) / arb(4), -v_a / arb(2)).gamma())
            rhs_g = (
                pref_g
                * ((arb(1) / arb(16) + (v_a * v_a) / arb(4)) ** (arb(3) / arb(8)))
                / ((tau * v_a / arb(2)).cosh() ** (arb(1) / arb(4)))
            )
            if v_num == 0:
                assert bool(arb(0) in (rhs_g - lhs_g) and abs(rhs_g - lhs_g) < arb("1e-74"))
            else:
                assert bool(rhs_g.lower() > lhs_g.upper())
    finally:
        flint_ctx.prec = saved


def test_section_4_complete_energy_bridge_feedback_threshold_and_consequence_tiers(
    tc060_artifact: dict,
) -> None:
    """Verify Section 4: complete reconstruction upper bound, R-independent feedback threshold < 3/4,
    and honest 4-tier global consequence classification.
    """
    sec4 = tc060_artifact["section_4_complete_energy_bridge_and_global_consequence"]
    assert sec4["all_section_4_checks_pass"] is True
    for row in sec4["complete_reconstruction_rows"]:
        assert row["complete_upper_bound_certified"] is True
        assert float(row["eight_P_sq_plus_four_D2_known_sq_plus_four_D2_core_sq"]["lower_dec"]) > float(
            row["E_Y"]["upper_dec"]
        )

    for th_row in sec4["R_independent_feedback_threshold_rows"]:
        assert th_row["both_feedbacks_le_quarter_certified"] is True
        assert (
            th_row["B_drift_sample_role"]
            == "ILLUSTRATIVE_SAMPLE_INSTANTIATION_OF_THEOREM_6_ABSTRACT_B_DRIFT"
        )
        assert float(th_row["B_pure_drift_analytic_upper"]["lower_dec"]) > float(
            th_row["B_drift_sample"]["upper_dec"]
        )
    assert tc060_artifact["serialized_arb_self_check"]["total_certified_arb_balls_checked"] == 336

    tiers = {r["consequence_class"]: r for r in sec4["global_consequence_classification"]}
    assert set(tiers.keys()) == set(GLOBAL_CONSEQUENCE_CLASSES)
    assert tiers["RELATIVE_CONTRACTION"]["status"] == (
        "PROVED_UNCONDITIONALLY_ON_SQUARE_POLE_DRIFT_AND_SMALL_DIVISORS"
    )
    assert tiers["ALL_POSITIVE_EXPONENTS_CLOSURE"]["status"] == "OPEN"


def test_section_5_controls_hybrid_diagnostic_and_directed_interval_semantics(
    tc060_artifact: dict,
) -> None:
    """Verify Section 5: arithmetic controls vs explicitly labeled hybrid diagnostic, boundary
    schedule checks, and adversarial directed interval overlap rejection.
    """
    sec5 = tc060_artifact["section_5_controls_schedule_and_directed_certificates"]
    assert sec5["all_section_5_checks_pass"] is True

    ctrl_norms = sec5["control_window_smooth_norms_Y16_T32"]
    assert set(ctrl_norms.keys()) == {
        "actual_liouville_matching_R_lambda",
        "unsigned_ones_matching_R_1",
        "two_adic_parity_a2_matching_R_a2",
        "odd_prime_parity_a_3_5_7_matching_R_a357",
        "inner_a2_with_outer_liouville_R_lambda",
    }
    assert (
        ctrl_norms["inner_a2_with_outer_liouville_R_lambda"]["model_type"]
        == "HYBRID_DIAGNOSTIC_NOT_COMPETING_ARITHMETIC_MODEL"
    )
    assert sec5["boundary_schedule_checks"]["sub_unit_Y_over_d_lt_1_certified"] is True
    assert sec5["directed_interval_certificate_protocol_check"]["verified"] is True

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # Adversarial overlap [2, 4] vs [1, 3]: retired upper(RHS)>=lower(LHS) is True, must reject!
        lhs_ov = arb(2).union(arb(4))
        rhs_ov = arb(1).union(arb(3))
        assert bool(rhs_ov.upper() >= lhs_ov.lower()) is True
        assert classify_interval_endpoints_le(
            Fraction(2), Fraction(4), Fraction(1), Fraction(3)
        ) == ("NOT_NUMERICALLY_CERTIFIED_OVERLAP", False)
        assert classify_arb_le_certificate(lhs_ov, rhs_ov) == (
            "NOT_NUMERICALLY_CERTIFIED_OVERLAP",
            False,
        )
        assert classify_arb_le_certificate(arb(1).union(arb(2)), arb(3).union(arb(4))) == (
            "CERTIFIED_DIRECTED_INEQUALITY",
            True,
        )
        assert classify_arb_le_certificate(arb(4).union(arb(5)), arb(1).union(arb(2))) == (
            "REFUTED_STRICT_VIOLATION",
            False,
        )
        assert classify_arb_le_certificate(
            arb(1).union(arb(2)), arb(3).union(arb(4)), exact_algebraic_equality_justified=True
        ) == ("INCONSISTENT_ALGEBRAIC_EQUALITY_CLAIM", False)
    finally:
        flint_ctx.prec = saved


def test_lean_module_wiring_axioms_and_review_doc_enclosures(
    tc060_artifact: dict, tmp_path: Path
) -> None:
    """Verify Lean module registration across RiemannScope.lean, build_formal.py, and
    certification.py, live #print axioms hygiene, review doc displayed enclosures, and
    adversarial tampering rejection.
    """
    rel_lean = "formal/RiemannScope/SignedDilationArithmeticEnergy.lean"
    assert rel_lean in build_formal.FORMAL_SOURCE_FILES
    assert rel_lean in certification.REQUIRED_FORMAL_SOURCES
    umbrella_text = (REPO_ROOT / "formal" / "RiemannScope.lean").read_text(encoding="utf-8")
    assert "import RiemannScope.SignedDilationArithmeticEnergy" in umbrella_text

    lean_audit = tc060_artifact["section_6_lean_formalization_audit"]
    assert lean_audit["all_tc060_lean_checks_pass"] is True
    assert lean_audit["sorry_count"] == 0
    assert lean_audit["admit_count"] == 0
    assert lean_audit["custom_axiom_count"] == 0
    assert lean_audit["pi_token_count"] == 0
    assert lean_audit["expected_tc060_theorems"] == EXPECTED_TC060_THEOREMS
    assert len(EXPECTED_TC060_THEOREMS) == 6
    assert lean_audit["formal_build_report_provenance"]["status"] == "passed"
    assert (
        lean_audit["formal_build_report_provenance"]["project_theorem_declarations_compiled"]
        >= 808
    )

    assert TC_060_REVIEW_DOC_PATH.exists(), f"Missing {TC_060_REVIEW_DOC_PATH}"
    rev_check = verify_tc060_review_displayed_enclosures(tc060_artifact, TC_060_REVIEW_DOC_PATH)
    assert rev_check["pi_macro_count"] == 0
    assert rev_check["pi_glyph_count"] == 0
    assert rev_check["untagged_count"] == 0
    assert rev_check["failed_count"] == 0
    assert rev_check["total_displayed_intervals_found"] >= 70
    assert rev_check["all_displayed_intervals_contain_generated_enclosures"] is True

    # Adversarial tampering controls on review doc verifier:
    orig_md = TC_060_REVIEW_DOC_PATH.read_text(encoding="utf-8")

    # (a) Injecting a forbidden circle-half macro must fail
    pi_tampered = tmp_path / "pi_tampered.md"
    pi_tampered.write_text(
        orig_md + "\nForbidden circle-half macro $\x5cpi$.\n", encoding="utf-8"
    )
    res_pi = verify_tc060_review_displayed_enclosures(tc060_artifact, pi_tampered)
    assert res_pi["pi_macro_count"] >= 1
    assert res_pi["all_displayed_intervals_contain_generated_enclosures"] is False

    # (b) Injecting a forbidden Unicode circle-half glyph must fail
    glyph_tampered = tmp_path / "glyph_tampered.md"
    glyph_tampered.write_text(orig_md + "\nForbidden glyph \u03c0.\n", encoding="utf-8")
    res_glyph = verify_tc060_review_displayed_enclosures(tc060_artifact, glyph_tampered)
    assert res_glyph["pi_glyph_count"] >= 1
    assert res_glyph["all_displayed_intervals_contain_generated_enclosures"] is False

    # (c) Injecting an untagged interval must fail
    untagged_md = tmp_path / "untagged.md"
    untagged_md.write_text(orig_md + "\nUntagged `[1.23 +/- 1e-5]`.\n", encoding="utf-8")
    res_untag = verify_tc060_review_displayed_enclosures(tc060_artifact, untagged_md)
    assert res_untag["untagged_count"] >= 1
    assert res_untag["all_displayed_intervals_contain_generated_enclosures"] is False

    # (d) Corrupting a tagged midpoint must fail containment
    corrupt_md = tmp_path / "corrupt_mid.md"
    corrupt_text = re.sub(
        r"`\[-3\.4342753[0-9]* \+/- [0-9.eE+-]+\]`",
        "`[9.9999999 +/- 1e-10]`",
        orig_md,
        count=1,
    )
    assert corrupt_text != orig_md
    corrupt_md.write_text(corrupt_text, encoding="utf-8")
    res_corrupt = verify_tc060_review_displayed_enclosures(tc060_artifact, corrupt_md)
    assert res_corrupt["failed_count"] >= 1
    assert res_corrupt["all_displayed_intervals_contain_generated_enclosures"] is False
