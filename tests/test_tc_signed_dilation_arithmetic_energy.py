"""Focused mathematical, falsification, formalization, and 256-bit Arb certification test suite
for TASK-TC-060 / TASK-TC-060R / TASK-TC-060R2: Signed Dilation Multipliers, Full-Core Scope,
Quantified Counterexamples, Certificate Scope, Analytic Justification, and Arithmetic Control of
the Complete Reconstruction.
"""

from __future__ import annotations

import copy
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
    AmbiguousCutoffError,
    CLOSEOUT_TC060R2_BRANCH,
    EXPECTED_TC060_THEOREMS,
    GLOBAL_CONSEQUENCE_CLASSES,
    INHERITED_FORMAL_PRODUCING_COMMIT,
    PROPOSED_TC060_BRANCH,
    REPAIR_TC060R_BRANCH,
    REVIEWED_TC059R2_HEAD,
    REVIEWED_TC059R2_IMPLEMENTATION,
    REVIEWED_TC060_HEAD,
    REVIEWED_TC060_IMPLEMENTATION,
    REVIEWED_TC060R_HEAD,
    REVIEWED_TC060R_IMPLEMENTATION,
    SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH,
    TASK_TC_060_ID,
    TASK_TC_060R_ID,
    TASK_TC_060R2_ID,
    TC_060_LEAN_MODULE_PATH,
    TC_060_REVIEW_DOC_PATH,
    certify_D0_small_divisor_cutoff,
    certify_T_canonical_cutoff,
    certify_ceil_from_arb_enclosure,
    certify_ceil_tau_Y_cutoff,
    certify_floor_from_arb_enclosure,
    certify_open_core_divisor_partition,
    classify_arb_le_certificate,
    classify_ceil_from_arb_enclosure,
    classify_floor_from_arb_enclosure,
    classify_interval_endpoints_le,
    compute_selberg_centered_remainder_table_arb,
    compute_smooth_basis_coefficients_arb,
    cutoff_level_blocks_exact,
    evaluate_adjacent_multiplier_m_d_acb,
    evaluate_c_half_square_pole_arb,
    evaluate_liouville_S_L_sum_arb,
    evaluate_qhat_L_closed_acb,
    evaluate_qhat_L_direct_quadrature_acb,
    evaluate_signed_gram_H_closed_arb,
    evaluate_smooth_jump_endpoint_reconstruction_arb,
    evaluate_square_pole_drift_M_arb,
    evaluate_weighted_window_kernel_K_quadrature_arb,
    verify_section_epistemic_scope_metadata,
    verify_subunit_finite_sum_row_metadata,
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
    assert tc060_artifact["task_id"] == TASK_TC_060R2_ID
    assert tc060_artifact["closed_out_repair_task_id"] == TASK_TC_060R_ID
    assert tc060_artifact["repaired_task_id"] == TASK_TC_060_ID
    assert tc060_artifact["parent_subgate"] == PARENT_SUBGATE_ID
    assert tc060_artifact["reviewed_merged_main_baseline"] == REVIEWED_MERGED_MAIN_BASELINE
    assert tc060_artifact["accepted_tc059r2_branch"] == ACCEPTED_TC059R2_BRANCH
    assert tc060_artifact["reviewed_tc059r2_implementation_commit"] == REVIEWED_TC059R2_IMPLEMENTATION
    assert tc060_artifact["reviewed_tc059r2_head_commit"] == REVIEWED_TC059R2_HEAD
    assert tc060_artifact["prior_tc059r_formal_producing_commit"] == INHERITED_FORMAL_PRODUCING_COMMIT
    assert tc060_artifact["reviewed_tc060_branch"] == PROPOSED_TC060_BRANCH
    assert tc060_artifact["reviewed_tc060_implementation_commit"] == REVIEWED_TC060_IMPLEMENTATION
    assert tc060_artifact["reviewed_tc060_head_commit"] == REVIEWED_TC060_HEAD
    assert tc060_artifact["reviewed_tc060r_branch"] == REPAIR_TC060R_BRANCH
    assert tc060_artifact["reviewed_tc060r_implementation_commit"] == REVIEWED_TC060R_IMPLEMENTATION
    assert tc060_artifact["reviewed_tc060r_head_commit"] == REVIEWED_TC060R_HEAD
    assert tc060_artifact["inherited_tc060r_formal_producing_commit"] == REVIEWED_TC060R_IMPLEMENTATION
    assert tc060_artifact["branch"] == CLOSEOUT_TC060R2_BRANCH
    fp = tc060_artifact["section_6_lean_formalization_audit"]["formal_build_report_provenance"]
    assert fp["producing_git_commit"] == REVIEWED_TC060R_IMPLEMENTATION
    assert fp["formal_build_status_in_tc060r2"] == "INHERITED_UNCHANGED_FROM_TC060R_FORMAL_COMMIT"
    assert tc060_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc060_artifact["rh_proved"] is False
    assert tc060_artifact["precision_bits"] == 256
    assert tc060_artifact["epistemic_categories_enforced"] == list(EPISTEMIC_CATEGORIES)
    assert tc060_artifact["global_consequence_classes_enforced"] == list(GLOBAL_CONSEQUENCE_CLASSES)
    assert "z = x + i*y" in tc060_artifact["complex_coordinate_convention"]
    assert "w = u + i*v" in tc060_artifact["complex_coordinate_convention"]

    arb_self = tc060_artifact["serialized_arb_self_check"]
    assert arb_self["all_enclose_original_256bit_arb_ball"] is True
    assert arb_self["total_certified_arb_balls_checked"] == 398

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
            == "ILLUSTRATIVE_SAMPLE_INSTANTIATION_OF_THEOREM_6_ABSTRACT_PARAMETER_NOT_FULL_KNOWN_BOUND"
        )
        assert float(th_row["B_pure_drift_analytic_upper"]["lower_dec"]) > float(
            th_row["B_drift_sample"]["upper_dec"]
        )
        assert (
            th_row["B_known_full_analytic_role"]
            == "COMBINES_B_DRIFT_AND_B_SMALL_VIA_UNCONDITIONAL_PNT_SUPREMUM_C_OSC_DISTINCT_FROM_B_SAMPLE"
        )
    assert tc060_artifact["serialized_arb_self_check"]["total_certified_arb_balls_checked"] == 398

    tiers = {r["consequence_class"]: r for r in sec4["global_consequence_classification"]}
    assert set(tiers.keys()) == set(GLOBAL_CONSEQUENCE_CLASSES)
    assert tiers["RELATIVE_CONTRACTION"]["status"] == (
        "PROVED_UNCONDITIONALLY_ON_SQUARE_POLE_DRIFT_AND_SMALL_DIVISORS"
    )
    assert "iff " not in tiers["FIXED_POWER_SAVING"]["scope"]
    assert "No exact-boundary converse" in tiers["FIXED_POWER_SAVING"]["scope"]
    assert "min(D_0(Y), T(Y)-1) < d <= T(Y)-1" in tiers["ALL_POSITIVE_EXPONENTS_CLOSURE"]["scope"]
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
    assert len(EXPECTED_TC060_THEOREMS) == 7
    assert "full_core_quantified_obstructions_and_w2_support_tc060r" in EXPECTED_TC060_THEOREMS
    assert lean_audit["formal_build_report_provenance"]["status"] == "passed"
    assert (
        lean_audit["formal_build_report_provenance"]["project_theorem_declarations_compiled"]
        >= 815
    )

    assert TC_060_REVIEW_DOC_PATH.exists(), f"Missing {TC_060_REVIEW_DOC_PATH}"
    rev_check = verify_tc060_review_displayed_enclosures(tc060_artifact, TC_060_REVIEW_DOC_PATH)
    assert rev_check["pi_macro_count"] == 0
    assert rev_check["pi_glyph_count"] == 0
    assert rev_check["untagged_count"] == 0
    assert rev_check["failed_count"] == 0
    assert rev_check["total_displayed_intervals_found"] >= 75
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


def test_tc060r_full_open_core_scope_and_Y4096_nonempty_tail(tc060_artifact: dict) -> None:
    """Verify Repair 1: full open core min(D_0(Y), T(Y)-1) < d <= T(Y)-1 retains both the
    intermediate band and the sub-unit tail d >= ceil(tau*Y) (nonempty at Y = 4096 with 7032
    divisors [25736, 32767]), and Lemma B2's absolute majorant divided by Y^eps (0 < eps < 1)
    diverges as Y -> infinity.
    """
    sec4 = tc060_artifact["section_4_complete_energy_bridge_and_global_consequence"]
    part_rows = {r["Y"]: r for r in sec4["full_open_core_partition_checks"]}
    assert set(part_rows.keys()) == {2, 4, 16, 64, 4096}
    r4096 = part_rows[4096]
    assert r4096["T_Y"] == 32768
    assert r4096["D_0_raw"] == 8
    assert r4096["ceil_tau_Y"] == 25736
    assert r4096["full_open_core_range_inclusive"] == [9, 32767]
    assert r4096["full_open_core_count"] == 32759
    assert r4096["intermediate_band_within_open_core_inclusive"] == [9, 25735]
    assert r4096["intermediate_band_count"] == 25727
    assert r4096["sub_unit_tail_ge_ceil_tau_Y_within_open_core_inclusive"] == [25736, 32767]
    assert r4096["sub_unit_tail_count"] == 7032
    assert r4096["sub_unit_tail_nonempty"] is True
    assert r4096["both_intermediate_and_tail_retained_in_open_core"] is True

    # Independent Arb check that Y*(log Y)^{-4}*exp(-2*c_W*sqrt(log Y)) / Y^eps grows at eps = 1/4:
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        c_W = arb(1) / arb(10)
        eps = arb(1) / arb(4)
        vals = []
        for k_exp in (10, 20, 40):
            lg_y = arb(k_exp * k_exp)
            y_val = lg_y.exp()
            b2_over_y_eps = (
                (y_val ** (arb(1) - eps))
                * (lg_y ** (-4))
                * (-arb(2) * c_W * lg_y.sqrt()).exp()
            )
            vals.append(b2_over_y_eps)
        assert bool(vals[0].upper() < vals[1].lower() < vals[2].lower())
    finally:
        flint_ctx.prec = saved


def test_tc060r_singleton_block_a1_obstruction_w2_support_and_b1_unbounded_family(
    tc060_artifact: dict,
) -> None:
    """Verify Repairs 2, 3, and 4:
    - Exact singleton block I_T(T) = {1} at v = 0 gives ratio = 1 for all T >= 2.
    - Unconditional prime-power support: w_{2,lambda}(p) = -(log p)^2 and w_{2,lambda}(6p) = 0 (p >= 5).
    - Arbitrary-coefficient family d = 1, a = e_1 gives ||phi_1 - phi_2||_Y / ||phi_1||_Y >= exp(3Y^2/4)/8 - 1 -> inf.
    - Liouville finite witnesses are explicitly scoped to excluding C = 1 and C = 3.
    """
    sec3 = tc060_artifact["section_3_attempts_a_and_b_obstructions_and_drift_theorem"]
    obs_a1 = sec3["candidate_a1_obstruction_and_square_pole_drift"]
    sing = obs_a1["singleton_block_I_T_T_v0_obstruction"]
    assert sing["verified"] is True
    assert sing["all_I_T_T_equal_singleton_1"] is True
    assert sing["exact_singleton_ratio_at_v_0"] == 1

    w2_chk = obs_a1["unconditional_w2_prime_and_6p_support_checks"]
    assert w2_chk["exact_increment_identity_verified_1_to_2000"] is True
    assert w2_chk["prime_w2_equals_minus_log_p_sq_verified"] is True
    assert w2_chk["six_p_three_distinct_primes_w2_zero_verified"] is True

    b1 = sec3["attempt_b_product_compensation_and_candidate_b1_counterexamples"]
    fam_rows = b1["unbounded_arbitrary_coefficient_family_d1_e1_rows"]
    assert [r["Y"] for r in fam_rows] == [2, 3, 4, 8]
    for r in fam_rows:
        assert r["phi_1_window_norm_sq_positive"] is True
        assert r["directed_lower_bound_certified"] is True
        assert float(r["actual_scaled_ratio_norm_phi1_minus_phi2_over_norm_phi1"]["lower_dec"]) > float(
            r["analytic_lower_bound_exp_3Y2_4_over_8_minus_1"]["upper_dec"]
        )
    assert (
        b1["finite_diagnostics_role"]
        == "FINITE_DIAGNOSTIC_NOT_UNIVERSAL_CONSTANT_REFUTATION"
    )
    assert (
        b1["actual_liouville_witness_scope"]
        == "EXCLUDES_TESTED_CONSTANTS_C_EQ_1_AT_Y4_D1_T6_AND_C_EQ_3_AT_Y16_D5_T32_ONLY"
    )


def test_tc060r_corrected_subunit_and_jump_log_Y_bounds(tc060_artifact: dict) -> None:
    """Verify Repair 5: uniform O(log Y) sub-unit tail bound and exact d = floor(T/q) reindexed
    drift-jump O(log Y) bound across Y in {2, 299/100, 4, 16, 64}.
    """
    sec3 = tc060_artifact["section_3_attempts_a_and_b_obstructions_and_drift_theorem"]
    sj_rows = sec3["drift_subunit_and_jump_reindexing_checks"]
    assert [r["Y_fraction"] for r in sj_rows] == ["2/1", "299/100", "4/1", "16/1", "64/1"]
    for row in sj_rows:
        assert "subunit_weighted_sum_lhs" not in row
        assert row["subunit_bound_certified"] is True
        assert row["drift_jump_bound_certified"] is True
        assert row["verified"] is True
        assert float(row["subunit_uniform_O_logY_rhs"]["lower_dec"]) > float(
            row["subunit_finite_weighted_sum_S_Y_T"]["upper_dec"]
        )
        assert float(row["drift_jump_O_logY_upper_bound"]["lower_dec"]) > float(
            row["drift_jump_window_norm"]["upper_dec"]
        )


def test_tc060r_certified_cutoff_protocol_D0_2_and_straddling_rejection(
    tc060_artifact: dict,
) -> None:
    """Verify Repair 6: certified cutoff protocol, D_0(2) = 0 in both Section 3 and Section 4,
    transitions across e, e^2, and 16, and explicit AmbiguousCutoffError on straddling enclosures.
    """
    sec3 = tc060_artifact["section_3_attempts_a_and_b_obstructions_and_drift_theorem"]
    repl_rows = {r["Y"]: r for r in sec3["informed_replacement_drift_and_small_divisor_rows"]}
    assert repl_rows[2]["D_0_Y"] == 0
    assert repl_rows[2]["small_divisor_slice_empty"] is True
    assert repl_rows[2]["r_sm_osc_small_d_le_D0_norm_sq"]["arb_ball_str"] == "0"

    sec4 = tc060_artifact["section_4_complete_energy_bridge_and_global_consequence"]
    comp_rows = {r["Y"]: r for r in sec4["complete_reconstruction_rows"]}
    assert comp_rows[2]["D_0_Y"] == 0
    assert comp_rows[2]["small_divisor_slice_empty"] is True
    assert comp_rows[2]["full_open_core_divisor_range_inclusive"] == [1, 2]

    sec5 = tc060_artifact["section_5_controls_schedule_and_directed_certificates"]
    cut_chk = sec5["certified_cutoff_protocol_checks"]
    assert cut_chk["verified"] is True
    assert cut_chk["D_0_at_Y_2"] == 0
    assert cut_chk["transition_around_e"] == {
        "below_e_27182818_over_1e7": 0,
        "symbolic_exact_e": 1,
        "above_e_27182819_over_1e7": 1,
    }
    assert cut_chk["transition_around_e_sq"] == {
        "below_e2_73890560_over_1e7": 1,
        "symbolic_exact_e2": 2,
        "above_e2_73890561_over_1e7": 2,
    }
    assert cut_chk["transition_around_Y_16_T"] == {
        "below_16_16383_over_1024": 32,
        "exact_16": 32,
        "above_16_16385_over_1024": 33,
    }

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        assert certify_D0_small_divisor_cutoff(2) == 0
        assert certify_D0_small_divisor_cutoff(Fraction(5, 2)) == 0
        assert certify_D0_small_divisor_cutoff(None, exact_log_Y=1) == 1
        assert certify_D0_small_divisor_cutoff(None, exact_log_Y=2) == 2
        assert certify_D0_small_divisor_cutoff(None, exact_log_Y=Fraction(7, 10), require_Y_ge_2=True) == 0
        assert certify_D0_small_divisor_cutoff(None, exact_log_Y=Fraction(1, 2), require_Y_ge_2=False) == 0
        with pytest.raises(ValueError):
            certify_D0_small_divisor_cutoff(None, exact_log_Y=Fraction(1, 2), require_Y_ge_2=True)
        with pytest.raises(ValueError):
            certify_D0_small_divisor_cutoff(None)
        with pytest.raises(ValueError):
            certify_D0_small_divisor_cutoff(3, exact_log_Y=1)
        assert certify_T_canonical_cutoff(Fraction(16383, 1024)) == 32
        assert certify_T_canonical_cutoff(16) == 32
        assert certify_T_canonical_cutoff(Fraction(16385, 1024)) == 33
        assert certify_ceil_tau_Y_cutoff(4096) == 25736
        p4096 = certify_open_core_divisor_partition(4096)
        assert p4096["sub_unit_tail_nonempty"] is True

        # Straddling balls must be classified as ambiguous and raise AmbiguousCutoffError:
        strad_floor = arb("4.9999").union(arb("5.0001"))
        assert classify_floor_from_arb_enclosure(strad_floor) == (
            "AMBIGUOUS_STRADDLING_ENCLOSURE",
            None,
            (4, 5),
        )
        with pytest.raises(AmbiguousCutoffError):
            certify_floor_from_arb_enclosure(strad_floor)

        strad_ceil = arb("31.9999").union(arb("32.0001"))
        assert classify_ceil_from_arb_enclosure(strad_ceil) == (
            "AMBIGUOUS_STRADDLING_ENCLOSURE",
            None,
            (32, 33),
        )
        with pytest.raises(AmbiguousCutoffError):
            certify_ceil_from_arb_enclosure(strad_ceil)

        with pytest.raises(AmbiguousCutoffError):
            certify_D0_small_divisor_cutoff(arb(1).exp())
    finally:
        flint_ctx.prec = saved


def test_tc060r_deleted_claims_absent_across_code_json_and_docs() -> None:
    """Verify none of the deleted/unsupported TC-060 claims survive as active assertions across
    Python, Lean, JSON, review report, and shared research registers.
    """
    forbidden_substrings = (
        "diverging as O((Y/d)^2)",
        "diverging as $O((Y/d)^2)$",
        "R(d) \\sim 4\\sqrt{d}\\log d",
        "R(d) ~ 4*sqrt(d)*log d",
        "= O(Y^{-1/2} \\log Y)",
        "= O(Y^{-1/2} log Y)",
        "= O(Y^{-5/8} \\log Y)",
        "= O(Y^{-5/8} log Y)",
        "has order $-1$ at $z = 1$ and order $+1$ at $z = 1/2$",
        "and Theorem 7 proves relative contraction",
        "zero-driven open core on D_0(Y) < d < ceil(tau*Y)",
        "zero-driven core on D_0(Y) < d < ceil(tau*Y)",
        "zero-driven core on $D_0(Y) < d < \\lceil\\tau Y\\rceil$",
        "zero-driven open core on $D_0(Y) < d < \\lceil\\tau Y\\rceil$",
    )
    checked_paths = (
        TC_060_LEAN_MODULE_PATH,
        REPO_ROOT / "tc" / "signed_dilation_arithmetic_energy.py",
        SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH,
        TC_060_REVIEW_DOC_PATH,
        REPO_ROOT / "formal" / "RiemannScope" / "README.md",
        REPO_ROOT / ".agents" / "research" / "queue.json",
        REPO_ROOT / ".agents" / "research" / "state.json",
        REPO_ROOT / ".agents" / "corpus_map" / "obligation_register.md",
        REPO_ROOT / "TRANSCENDENTAL_CONTINUATION.md",
        REPO_ROOT / "RESEARCH_LEDGER.md",
    )
    for path in checked_paths:
        txt = path.read_text(encoding="utf-8")
        for bad in forbidden_substrings:
            assert bad not in txt, f"Deleted TC-060 claim {bad!r} still present in {path}"


def test_tc060r2_subunit_finite_sum_metadata_and_adversarial_rejection(
    tc060_artifact: dict,
) -> None:
    """Verify TASK-TC-060R2 Correction 1:
    - S_{Y,T(Y)} is explicitly labeled as a finite sum with lower-exclusive floor(Y) and
      upper-inclusive T(Y) cutoff metadata.
    - At Y = 64, T(64) = 182, S_{64,182} sums 118 terms (65 <= d <= 182).
    - The non-certified infinite-tail evaluation (~1.7956554120163753) is never exported as an
      Arb certificate in JSON or backticked Arb ball in the review document.
    - verify_subunit_finite_sum_row_metadata fails closed on legacy keys, infinite-sum relabeling,
      or mismatched cutoff bounds.
    """
    sec3 = tc060_artifact["section_3_attempts_a_and_b_obstructions_and_drift_theorem"]
    sj_rows = sec3["drift_subunit_and_jump_reindexing_checks"]
    for row in sj_rows:
        ok_meta, msg_meta = verify_subunit_finite_sum_row_metadata(row)
        assert ok_meta is True, msg_meta
        assert row["subunit_sum_kind"] == "FINITE_T_TRUNCATED_SUM_S_Y_T"
        assert row["subunit_sum_symbol"] == "S_{Y,T(Y)}"
        assert row["subunit_d_lower_exclusive"] == row["floor_Y"]
        assert row["subunit_d_upper_inclusive"] == row["T_Y"]
        assert row["subunit_d_term_count"] == row["T_Y"] - row["floor_Y"]
        assert row["subunit_d_range_inclusive"] == [row["floor_Y"] + 1, row["T_Y"]]

    r64 = sj_rows[4]
    assert r64["Y_fraction"] == "64/1"
    assert r64["subunit_d_lower_exclusive"] == 64
    assert r64["subunit_d_upper_inclusive"] == 182
    assert r64["subunit_d_term_count"] == 118
    assert r64["subunit_d_range_inclusive"] == [65, 182]

    json_txt = SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH.read_text(encoding="utf-8")
    assert "1.795655" not in json_txt
    assert "subunit_weighted_sum_lhs" not in json_txt

    rev_txt = TC_060_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    assert "S_{64,\\infty}" in rev_txt
    assert "1.7956554120163753" in rev_txt
    assert "`[1.795655" not in rev_txt

    # Adversarial fail-closed rejection checks:
    bad_legacy = copy.deepcopy(r64)
    bad_legacy["subunit_weighted_sum_lhs"] = bad_legacy["subunit_finite_weighted_sum_S_Y_T"]
    ok_leg, msg_leg = verify_subunit_finite_sum_row_metadata(bad_legacy)
    assert ok_leg is False and "Forbidden ambiguous" in msg_leg

    bad_inf = copy.deepcopy(r64)
    bad_inf["subunit_sum_symbol"] = "S_{Y,\\infty}"
    ok_inf, msg_inf = verify_subunit_finite_sum_row_metadata(bad_inf)
    assert ok_inf is False and "subunit_sum_symbol" in msg_inf

    bad_upper = copy.deepcopy(r64)
    bad_upper["subunit_d_upper_inclusive"] = 999
    ok_up, msg_up = verify_subunit_finite_sum_row_metadata(bad_upper)
    assert ok_up is False and "Cutoff mismatch" in msg_up

    bad_count = copy.deepcopy(r64)
    bad_count["subunit_d_term_count"] = 119
    ok_cnt, msg_cnt = verify_subunit_finite_sum_row_metadata(bad_count)
    assert ok_cnt is False and "Range/count mismatch" in msg_cnt


def test_tc060r2_section_epistemic_scope_and_no_invented_mixed_category(
    tc060_artifact: dict,
) -> None:
    """Verify TASK-TC-060R2 Correction 2:
    - Exactly the 6 established EPISTEMIC_CATEGORIES remain enforced (no 7th 'MIXED' category).
    - Blanket singular 'epistemic_status' is removed from Sections 1-5 and replaced by
      'epistemic_statuses' matching 'component_epistemic_map'.
    - verify_section_epistemic_scope_metadata rejects blanket 'CONCRETE_ANALYTIC_IN_LEAN' on
      mixed sections, invented 'MIXED' categories, and list/map mismatches.
    """
    assert len(EPISTEMIC_CATEGORIES) == 6
    assert "MIXED" not in EPISTEMIC_CATEGORIES

    section_keys = (
        "section_1_exact_object_and_noncircular_reassembly",
        "section_2_signed_dilation_fourier_and_gram_kernel",
        "section_3_attempts_a_and_b_obstructions_and_drift_theorem",
        "section_4_complete_energy_bridge_and_global_consequence",
        "section_5_controls_schedule_and_directed_certificates",
    )
    for sk in section_keys:
        sec_obj = tc060_artifact[sk]
        assert "epistemic_status" not in sec_obj
        ok_sec, msg_sec = verify_section_epistemic_scope_metadata(sec_obj)
        assert ok_sec is True, f"{sk}: {msg_sec}"

    sec2 = tc060_artifact["section_2_signed_dilation_fourier_and_gram_kernel"]
    assert set(sec2["epistemic_statuses"]) == {
        "UNCONDITIONAL_FINITE_ARITHMETIC",
        "CONCRETE_ANALYTIC_IN_LEAN",
        "ANALYTIC_PROVED_OUTSIDE_LEAN",
        "CERTIFIED_FINITE_OBSERVATION",
    }
    assert (
        sec2["component_epistemic_map"]["qhat_L_finite_cutoff_gamma_identity_and_improper_tails"]
        == "ANALYTIC_PROVED_OUTSIDE_LEAN"
    )
    assert (
        sec2["component_epistemic_map"][
            "adjacent_dilation_multiplier_benchmark_and_odd_harmonic_attainment"
        ]
        == "CONCRETE_ANALYTIC_IN_LEAN"
    )

    # Adversarial fail-closed rejection checks:
    bad_blanket = copy.deepcopy(sec2)
    bad_blanket["epistemic_status"] = "CONCRETE_ANALYTIC_IN_LEAN"
    ok_bl, msg_bl = verify_section_epistemic_scope_metadata(bad_blanket)
    assert ok_bl is False and "Mixed section cannot claim blanket" in msg_bl

    bad_mixed = copy.deepcopy(sec2)
    bad_mixed["epistemic_statuses"] = [*sec2["epistemic_statuses"], "MIXED"]
    ok_mx, msg_mx = verify_section_epistemic_scope_metadata(bad_mixed)
    assert ok_mx is False and "Invalid epistemic category" in msg_mx

    bad_mismatch = copy.deepcopy(sec2)
    bad_mismatch["epistemic_statuses"] = ["CONCRETE_ANALYTIC_IN_LEAN"]
    ok_mm, msg_mm = verify_section_epistemic_scope_metadata(bad_mismatch)
    assert ok_mm is False and "does not match component_epistemic_map" in msg_mm


def test_tc060r2_square_supported_gaussian_phi1_identity_and_review_hygiene() -> None:
    """Verify TASK-TC-060R2 Correction 3:
    - phi_{m^2}(X) = m^{-1} * phi_1(X / m^2), so Q_{1_sq,T}(X) = sum_{m^2 <= T} m^{-1}*phi_1(X/m^2).
    - For T >= 4, the erroneous substitution sum_{m^2 <= T} m^{-1}*phi_m(X/m^2) strictly disagrees.
    - No occurrence of varphi_m(X/m^2) or varphi_m(X / m^2) remains in the review report.
    """
    rev_txt = TC_060_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    assert "\\varphi_m(X / m^2)" not in rev_txt
    assert "\\varphi_m(X/m^2)" not in rev_txt
    assert "\\varphi_1(X/m^2)" in rev_txt

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for T_val, x_frac in (
            (1, Fraction(7, 3)),
            (4, Fraction(5, 2)),
            (9, Fraction(11, 3)),
            (16, Fraction(13, 2)),
            (25, Fraction(19, 2)),
        ):
            x_a = _frac_to_arb(x_frac)
            q_sq_direct = arb(0)
            for n in range(1, T_val + 1):
                if is_perfect_square_int(n):
                    q_sq_direct += evaluate_phi_n_arb(x_a, n, prec_bits=256)

            q_sq_phi1 = arb(0)
            q_sq_buggy_phim = arb(0)
            m = 1
            while m * m <= T_val:
                m_a = arb(m)
                x_scaled = x_a / (m_a * m_a)
                phi_m2 = evaluate_phi_n_arb(x_a, m * m, prec_bits=256)
                term_phi1 = evaluate_phi_n_arb(x_scaled, 1, prec_bits=256) / m_a
                assert bool(arb(0) in (phi_m2 - term_phi1) and abs(phi_m2 - term_phi1) < arb("1e-70"))
                q_sq_phi1 += term_phi1
                q_sq_buggy_phim += evaluate_phi_n_arb(x_scaled, m, prec_bits=256) / m_a
                m += 1

            diff_ok = q_sq_direct - q_sq_phi1
            assert bool(arb(0) in diff_ok and abs(diff_ok) < arb("1e-70"))
            if T_val >= 4:
                diff_bug = q_sq_direct - q_sq_buggy_phim
                assert bool(abs(diff_bug).lower() > arb("1e-6"))
    finally:
        flint_ctx.prec = saved


def test_tc060r2_constant_1_liouville_S_L_bound_and_subunit_gd_window_norm() -> None:
    """Verify TASK-TC-060R2 Correction 4:
    - S_L(a) = sum_{1 <= q <= L} lambda(q) q^{-3} exp(-a/q^2) satisfies -1/2 <= S_L(a) <= 1,
      hence |S_L(a)| <= 1 across all L >= 0 and a >= 0.
    - g_d(X) = d^{-1/2} Q_{lambda,L_d}(X/d) = X^{5/2} d^{-3} S_{L_d}((X/d)^2) satisfies
      ||g_d||_Y <= sqrt((tau^5 - 1)/5) * Y^{5/2} * d^{-3} on sub-unit scales d > floor(Y).
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau = _tau_arb()
        half = arb(1) / arb(2)
        for L_val in (0, 1, 2, 3, 4, 10, 50):
            for a_frac in (
                Fraction(0, 1),
                Fraction(1, 16),
                Fraction(1, 4),
                Fraction(1, 1),
                Fraction(4, 1),
                Fraction(25, 1),
            ):
                s_val = evaluate_liouville_S_L_sum_arb(L_val, a_frac, prec_bits=256)
                if L_val == 1 and a_frac == 0:
                    assert s_val == arb(1)
                elif L_val == 0:
                    assert s_val == arb(0)
                else:
                    assert bool(s_val.upper() < arb(1))
                    assert bool(s_val.lower() > -half)
                    assert bool(abs(s_val).upper() < arb(1))

        # Direct sub-unit g_d(X) identity and window norm check at (Y=4, T=6, d=5) and (Y=16, T=32, d=17):
        pref_norm = ((tau ** 5 - arb(1)) / arb(5)).sqrt()
        for Y_int, T_int, d_int in ((4, 6, 5), (16, 32, 17)):
            L_d = T_int // d_int
            x_probe = arb(Y_int) * arb(3) / arb(2)
            gd_direct = (
                evaluate_Q_general_arb(
                    x_probe / arb(d_int), L_d, coeff_fn=liouville_lambda_int, prec_bits=256
                )
                / arb(d_int).sqrt()
            )
            gd_via_SL = (
                (x_probe ** (arb(5) / arb(2)))
                * (arb(d_int) ** (-3))
                * evaluate_liouville_S_L_sum_arb(
                    L_d, (x_probe / arb(d_int)) ** 2, prec_bits=256
                )
            )
            assert bool(arb(0) in (gd_direct - gd_via_SL) and abs(gd_direct - gd_via_SL) < arb("1e-68"))

            def _gd_sq_integrand(z_var: acb, _analytic: bool) -> acb:
                # z_var in [0, 1], X = Y * exp(z_var * log(tau))
                lg_tau = tau.log()
                x_c = acb(Y_int) * (z_var * acb(lg_tau)).exp()
                tot = acb(0)
                for q in range(1, L_d + 1):
                    n_q = d_int * q
                    tot += (
                        acb(liouville_lambda_int(q))
                        * (x_c ** acb(arb(5) / arb(2)))
                        * acb(arb(n_q) ** (-3))
                        * (-(x_c * x_c) / acb(n_q * n_q)).exp()
                    )
                return tot * tot * acb(lg_tau)

            gd_norm_sq = acb.integral(_gd_sq_integrand, acb(0), acb(1), rel_tol=2 ** (-220)).real
            gd_norm = gd_norm_sq.sqrt()
            rhs_bound = pref_norm * (arb(Y_int) ** (arb(5) / arb(2))) * (arb(d_int) ** (-3))
            assert bool(rhs_bound.lower() > gd_norm.upper())
    finally:
        flint_ctx.prec = saved


