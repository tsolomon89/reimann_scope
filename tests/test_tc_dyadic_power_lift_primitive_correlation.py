"""Focused mathematical, falsification, formalization, and 256-bit Arb certification test suite
for TASK-TC-059: Dyadic Power-Lift Arithmetic and Primitive Coprime Correlations.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import re

from flint import acb, arb, ctx as flint_ctx
import pytest

import certification
from scripts import build_formal
from tc.canonical_theta_correlation_bound import REPO_ROOT
from tc.coupled_scale_energy_bootstrap import (
    _acb_integral_certified_arb,
    _tau_arb,
    moebius_mu_int,
)
from tc.dyadic_power_lift_primitive_correlation import (
    DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH,
    EPISTEMIC_CATEGORIES,
    EXPECTED_TC059_THEOREMS,
    INCLUDED_TC_058R2_TIP,
    PARENT_SUBGATE_ID,
    PROPOSED_BRANCH,
    REVIEWED_MERGED_MAIN_BASELINE,
    TASK_TC_059_ID,
    TC_059_LEAN_MODULE_PATH,
    TC_059_REVIEW_DOC_PATH,
    dyadic_power_lift_b_J_conv_table,
    dyadic_power_lift_b_J_divisor_int,
    evaluate_C_chi_var_smooth_arb,
    evaluate_C_var_gaussian_arb,
    evaluate_Q_general_arb,
    evaluate_bilinear_window_pairing_closed_arb,
    evaluate_primitive_coprime_sum_Pi_arb,
    evaluate_window_kernel_K_closed_arb,
    evaluate_window_kernel_K_quadrature_arb,
    is_squarefree_int,
    power_lift_increment_delta_J_int,
    stabilization_depth_J_T,
    verify_tc059_lean_theorems_live,
    verify_tc059_review_displayed_enclosures,
)
from tc.liouville_square_dilation import liouville_lambda_int
from tc.prime_chain_contraction import evaluate_phi_n_arb, exact_T_cutoff_ceil_Y_5_4


@pytest.fixture(scope="module")
def tc059_artifact() -> dict:
    assert DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH.exists(), (
        f"Missing {DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH}"
    )
    return json.loads(
        DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH.read_text(encoding="utf-8")
    )


def test_artifact_metadata_and_epistemic_hygiene(tc059_artifact: dict) -> None:
    """Verify baseline provenance, gate status, zero-pi convention, and 256-bit Arb self-check."""
    assert tc059_artifact["task_id"] == TASK_TC_059_ID
    assert tc059_artifact["parent_subgate"] == PARENT_SUBGATE_ID
    assert tc059_artifact["reviewed_merged_main_baseline"] == REVIEWED_MERGED_MAIN_BASELINE
    assert tc059_artifact["included_tc058r2_tip"] == INCLUDED_TC_058R2_TIP
    assert tc059_artifact["branch"] == PROPOSED_BRANCH
    assert tc059_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc059_artifact["rh_proved"] is False
    assert tc059_artifact["precision_bits"] == 256
    assert tc059_artifact["epistemic_categories_enforced"] == list(EPISTEMIC_CATEGORIES)

    arb_self = tc059_artifact["serialized_arb_self_check"]
    assert arb_self["all_enclose_original_256bit_arb_ball"] is True
    assert arb_self["total_certified_arb_balls_checked"] >= 200


def test_section_1_observable_reconstruction_and_closure_contract(tc059_artifact: dict) -> None:
    """Verify preregistered grid E = D_tilde + S_comb, E/D_tilde > 1 at Y=16,64, separate radii,
    and conditional logarithmic-saving transfer schedules.
    """
    sec1 = tc059_artifact["section_1_observable_and_closure_contract"]
    assert sec1["all_section_1_checks_pass"] is True

    rows = sec1["preregistered_grid_rows"]
    ys = [r["Y"] for r in rows]
    assert ys == [2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 256]
    for r in rows:
        assert r["verified"] is True
        assert "closed_kernel_radius_str" in r
        assert "quadrature_radius_str" in r

    diag_hi = sec1["diagnostic_ratio_highlights"]
    assert diag_hi["raw_E_le_D_tilde_refuted_at_16_and_64"] is True
    assert diag_hi["eventual_closure_contract_refuted_by_samples"] is False
    assert float(diag_hi["E_16_over_D_tilde_16"]["lower_dec"]) > 2.45
    assert float(diag_hi["E_64_over_D_tilde_64"]["lower_dec"]) > 1.80

    scheds = sec1["conditional_log_saving_transfer_schedules"]
    assert [s["kappa_eta"] for s in scheds] == ["1/2", "1", "2"]
    for s in scheds:
        assert s["verified"] is True
        assert float(s["half_minus_feedback_margin"]["lower_dec"]) > 0.0
        assert float(s["polylog_bound_margin_at_Y16"]["lower_dec"]) > 0.0


def test_section_2_dyadic_power_lift_boundaries_controls_and_attempt_a(
    tc059_artifact: dict,
) -> None:
    """Verify exact dyadic power-lift arithmetic, discrepancy boundaries n=2^{2^J}, control
    separation at J=2, finite Gaussian lift (including T=0,1 and X=0), Attempt A sign changes,
    meromorphic removable zero at z=1, and coherent stabilized-tail negative control.
    """
    sec2 = tc059_artifact["section_2_dyadic_power_lift_and_attempt_a"]
    assert sec2["all_section_2_checks_pass"] is True

    # Direct arithmetic verification across J in {1, 2, 3, 4} and boundaries {4, 16, 256, 65536}
    for J, expected_bdry in ((1, 4), (2, 16), (3, 256), (4, 65536)):
        d_J = 1 << J
        assert (1 << d_J) == expected_bdry
        assert dyadic_power_lift_b_J_divisor_int(J, expected_bdry) == 1
        assert moebius_mu_int(expected_bdry) == 0
        assert power_lift_increment_delta_J_int(J, expected_bdry) == -1
        for n in range(1, min(expected_bdry, 300)):
            assert dyadic_power_lift_b_J_divisor_int(J, n) == moebius_mu_int(n)
            assert power_lift_increment_delta_J_int(J, n) == 0

    conv_3 = dyadic_power_lift_b_J_conv_table(3, 260, base_fn=liouville_lambda_int)
    for n in range(1, 261):
        assert conv_3[n] == dyadic_power_lift_b_J_divisor_int(3, n)
        if is_squarefree_int(n):
            assert conv_3[n] == moebius_mu_int(n)

    # Stabilization depth J_T edge cases
    assert stabilization_depth_J_T(0) == 1
    assert stabilization_depth_J_T(1) == 1
    assert stabilization_depth_J_T(3) == 1
    assert stabilization_depth_J_T(4) == 2
    assert stabilization_depth_J_T(15) == 2
    assert stabilization_depth_J_T(16) == 3
    assert stabilization_depth_J_T(255) == 3
    assert stabilization_depth_J_T(256) == 4

    # Control separation at J = 2: b_{a,2}(p^2) = a(p)*(a(p)+1)
    ctrl_rows = {r["mode"]: r for r in sec2["control_separation_J2_rows"]}
    assert ctrl_rows["liouville"]["b_a_2_at_p_sq"]["2"] == 0
    assert ctrl_rows["liouville"]["b_a_2_at_p_sq"]["3"] == 0
    assert ctrl_rows["unsigned_1"]["b_a_2_at_p_sq"]["2"] == 2
    assert ctrl_rows["a2"]["b_a_2_at_p_sq"]["2"] == 0
    assert ctrl_rows["a2"]["b_a_2_at_p_sq"]["3"] == 2
    assert ctrl_rows["a_3_5_7"]["b_a_2_at_p_sq"]["2"] == 2
    assert ctrl_rows["a_3_5_7"]["b_a_2_at_p_sq"]["3"] == 0
    assert ctrl_rows["a_3_5_7"]["b_a_2_at_p_sq"]["11"] == 2

    # Finite Gaussian lift edge cases (T=0, T=1, X=0) and active falsification of wrong exponent
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        assert evaluate_Q_general_arb(arb(5), 0, lambda n: dyadic_power_lift_b_J_divisor_int(2, n)) == arb(0)
        assert evaluate_Q_general_arb(arb(0), 20, lambda n: dyadic_power_lift_b_J_divisor_int(2, n)) == arb(0)
        q_t1 = evaluate_Q_general_arb(arb(3), 1, lambda n: dyadic_power_lift_b_J_divisor_int(2, n))
        assert bool(arb(0) in (q_t1 - evaluate_phi_n_arb(arb(3), 1, prec_bits=256)))

        # Active falsification at J = 2 (d_J = 4, true weight r^{-2}): wrong weight r^{-1} fails at T = 20, X = 7
        x7 = arb(7)
        lhs_j2 = evaluate_Q_general_arb(x7, 20, lambda n: dyadic_power_lift_b_J_divisor_int(2, n))
        true_rhs_j2 = arb(0)
        wrong_rhs_j2 = arb(0)
        for r in (1, 2):  # r^4 <= 20
            rd = r ** 4
            q_mu_sub = evaluate_Q_general_arb(x7 / arb(rd), 20 // rd, moebius_mu_int)
            true_rhs_j2 += q_mu_sub / arb(r ** 2)
            wrong_rhs_j2 += q_mu_sub / arb(r)
        assert bool(arb(0) in (lhs_j2 - true_rhs_j2) and abs(lhs_j2 - true_rhs_j2) < arb("1e-70"))
        assert bool(abs(lhs_j2 - wrong_rhs_j2) > arb("1e-3"))
    finally:
        flint_ctx.prec = saved

    # Attempt A sign changes and coherent negative control
    sc = sec2["attempt_a_certified_sign_change_scales"]
    assert sc["verified"] is True
    assert len(sc["cross_mu_Delta1_positive_Y"]) >= 1
    assert len(sc["cross_mu_Delta1_negative_Y"]) >= 1
    assert len(sc["cross_Delta1_Delta2_positive_Y"]) >= 1
    assert len(sc["cross_Delta1_Delta2_negative_Y"]) >= 1

    mero = sec2["meromorphic_tower_separation"]
    assert mero["verified"] is True
    assert mero["value_at_z1_removable_zero"] == "0"
    assert float(mero["derivative_at_removable_zero_z1_J2_zeta4"]["lower_dec"]) > 1.0823

    nc = sec2["coherent_stabilized_tail_negative_control_Y16_T32"]
    assert nc["verified"] is True
    assert nc["telescoping_orthogonality_gain"] is False


def test_section_3_primitive_pairs_subunit_scaling_cutoffs_and_four_diagonals(
    tc059_artifact: dict,
) -> None:
    """Verify sub-unit u = Y/g < 1 kernel scaling, 3-way E(Y) equality & Moebius inversion,
    cutoff discrepancy witnesses, nonmonotone scales, and 4-way diagonal comparison.
    """
    sec3 = tc059_artifact["section_3_primitive_pairs_and_diagonals"]
    assert sec3["all_section_3_checks_pass"] is True
    assert sec3["sub_unit_window_kernel_check_Y8_g12"]["verified"] is True
    assert sec3["Pi_lambda_sign_change_scales"]["verified"] is True
    assert len(sec3["Pi_lambda_sign_change_scales"]["positive_Y"]) >= 1
    assert len(sec3["Pi_lambda_sign_change_scales"]["negative_Y"]) >= 1

    # Check sub-unit u = 3/5 < 1 directly in 256-bit Arb
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        k_closed = evaluate_window_kernel_K_closed_arb(Fraction(3, 5), 2, 3, prec_bits=256)
        k_quad = evaluate_window_kernel_K_quadrature_arb(Fraction(3, 5), 2, 3, prec_bits=256)
        assert bool(arb(0) in (k_closed - k_quad) and abs(k_closed - k_quad) < arb("1e-65"))
    finally:
        flint_ctx.prec = saved

    disc_rows = sec3["inherited_vs_canonical_cutoff_discrepancy_rows"]
    assert len(disc_rows) == 2
    assert disc_rows[0]["Y"] == "9/4"
    assert disc_rows[0]["inherited_cutoff_floor_T_over_d"] == 1
    assert disc_rows[0]["canonical_cutoff_T_Y_over_d"] == 2
    assert disc_rows[1]["Y"] == "7"
    assert disc_rows[1]["inherited_cutoff_floor_T_over_d"] == 6
    assert disc_rows[1]["canonical_cutoff_T_Y_over_d"] == 5

    diag_rows = sec3["four_way_diagonal_comparison"]["rows"]
    row_2048 = next(r for r in diag_rows if r["Y"] == 2048)
    assert row_2048["exceeds_tau_pow_4"] is True
    row_64 = next(r for r in diag_rows if r["Y"] == 64)
    assert "D_coeff_m_eq_n" in row_64
    assert "D_tilde_prime_power" in row_64
    assert "D_tower_mu_plus_increments" in row_64
    assert "D_dyadic_primitive_shell_diagonal" in row_64


def test_section_4_quotient_shell_moebius_variation_constants_and_attempt_b(
    tc059_artifact: dict,
) -> None:
    """Verify separable quotient-shell Moebius decoupling vs naive shell failure, closed-form
    C_var and C_{chi,var} against direct Arb quadrature, and finite parity uniqueness.
    """
    sec4 = tc059_artifact["section_4_dyadic_blocks_and_attempt_b"]
    assert sec4["all_section_4_checks_pass"] is True

    for q_row in sec4["quotient_shell_moebius_decoupling_checks_Y16_T32"]:
        assert q_row["verified"] is True
        assert float(q_row["naive_uncoupled_shell_error"]["rad_float_outward"]) < abs(
            float(q_row["naive_uncoupled_shell_error"]["mid_float"])
        )

    # Independent quadrature cross-check of C_var and C_{chi,var} continuous integrals!
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        C_var = evaluate_C_var_gaussian_arb(prec_bits=256)
        C_chi = evaluate_C_chi_var_smooth_arb(prec_bits=256)
        assert bool(arb("1.314139") < C_var < arb("1.314140"))
        assert bool(arb("3.088792") < C_chi < arb("3.088793"))

        # Check int_0^infty (1/2)*|4*t^2 - 16*t + 9|*exp(-t) dt via split acb.integral at t_- and t_+
        s7 = arb(7).sqrt()
        tm = arb(2) - s7 / arb(2)
        tp = arb(2) + s7 / arb(2)
        i1 = _acb_integral_certified_arb(
            lambda z, _a: (arb(1) / arb(2)) * (acb(4) * z * z - acb(16) * z + acb(9)) * (-z).exp(),
            arb(0),
            tm,
            prec_bits=256,
        )
        i2 = _acb_integral_certified_arb(
            lambda z, _a: -(arb(1) / arb(2)) * (acb(4) * z * z - acb(16) * z + acb(9)) * (-z).exp(),
            tm,
            tp,
            prec_bits=256,
        )
        i3 = _acb_integral_certified_arb(
            lambda z, _a: (arb(1) / arb(2)) * (acb(4) * z * z - acb(16) * z + acb(9)) * (-z).exp(),
            tp,
            arb(80),
            prec_bits=256,
        )
        # Tail on [80, infty): (1/2)*(4*t^2)*exp(-t) integrated <= 2*(80^2 + 160 + 2)*exp(-80) < 1e-30
        c_chi_quad = (-arb(1) / arb(2)).exp() + i1 + i2 + i3
        assert bool(abs(C_chi - c_chi_quad) < arb("1e-30"))
    finally:
        flint_ctx.prec = saved

    # Finite parity uniqueness check: any perturbation on 1..T violates a(1)=1 or a(p*n)+a(n)=0
    T_uniq = 40
    a_test = [0] + [liouville_lambda_int(n) for n in range(1, T_uniq + 1)]
    a_test[12] += 1  # perturb at composite 12 = 2 * 6 = 3 * 4
    violations = [
        (p, n)
        for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
        for n in range(1, T_uniq // p + 1)
        if a_test[p * n] + a_test[n] != 0
    ]
    assert (2, 6) in violations and (3, 4) in violations


def test_section_5_turn_chart_defect_window_base_and_murmurations(tc059_artifact: dict) -> None:
    """Verify turn chart, prime-local defect Euler bridge (zero-free), [Y, b*Y] discriminator,
    and murmuration GRH screening.
    """
    sec5 = tc059_artifact["section_5_tc_geometry_defect_and_murmurations"]
    assert sec5["all_section_5_checks_pass"] is True
    assert sec5["turn_chart_audit"]["admissible_algebraic_grade_claimed"] is False
    assert sec5["turn_chart_audit"]["symmetry_line_Re_q"] == "1/4"
    for r in sec5["prime_local_defect_bridge"]["synthetic_sample_rows"]:
        assert r["zero_inputs_used"] is False
        assert r["verified"] is True

    wb = sec5["window_base_compatibility_discriminator_Y16_T32"]
    assert wb["additional_tau_grade_compatibility_identity_used"] is False
    assert [r["window_base_multiplier_b"] for r in wb["rows"]] == ["2", "e", "tau"]
    for r in wb["rows"]:
        assert r["verified"] is True

    for m_item in sec5["murmuration_hypothesis_audit"]:
        assert m_item["imported_into_unconditional_bounds"] is False


def test_lean_module_wiring_axioms_and_review_doc_enclosures(
    tc059_artifact: dict, tmp_path: Path
) -> None:
    """Verify Lean module registration across RiemannScope.lean, build_formal.py, and
    certification.py, live #print axioms hygiene, review doc displayed enclosures, and
    adversarial tampering rejection.
    """
    rel_lean = "formal/RiemannScope/DyadicPowerLiftPrimitiveCorrelation.lean"
    assert rel_lean in build_formal.FORMAL_SOURCE_FILES
    assert rel_lean in certification.REQUIRED_FORMAL_SOURCES
    umbrella_text = (REPO_ROOT / "formal" / "RiemannScope.lean").read_text(encoding="utf-8")
    assert "import RiemannScope.DyadicPowerLiftPrimitiveCorrelation" in umbrella_text

    lean_audit = tc059_artifact["section_6_lean_formalization_audit"]
    assert lean_audit["all_tc059_lean_checks_pass"] is True
    assert lean_audit["sorry_count"] == 0
    assert lean_audit["admit_count"] == 0
    assert lean_audit["custom_axiom_count"] == 0
    assert lean_audit["expected_tc059_theorems"] == EXPECTED_TC059_THEOREMS

    assert TC_059_REVIEW_DOC_PATH.exists(), f"Missing {TC_059_REVIEW_DOC_PATH}"
    rev_check = verify_tc059_review_displayed_enclosures(tc059_artifact, TC_059_REVIEW_DOC_PATH)
    assert rev_check["pi_macro_count"] == 0
    assert rev_check["untagged_count"] == 0
    assert rev_check["failed_count"] == 0
    assert rev_check["total_displayed_intervals_found"] >= 20
    assert rev_check["all_displayed_intervals_contain_generated_enclosures"] is True

    # Adversarial tampering controls on review doc verifier:
    orig_md = TC_059_REVIEW_DOC_PATH.read_text(encoding="utf-8")

    # (a) Injecting a forbidden circle-half macro must fail
    pi_tampered = tmp_path / "pi_tampered.md"
    pi_tampered.write_text(
        orig_md + "\nForbidden circle-half macro $\x5cpi$.\n", encoding="utf-8"
    )
    res_pi = verify_tc059_review_displayed_enclosures(tc059_artifact, pi_tampered)
    assert res_pi["pi_macro_count"] >= 1
    assert res_pi["all_displayed_intervals_contain_generated_enclosures"] is False

    # (b) Injecting an untagged interval must fail
    untagged_md = tmp_path / "untagged.md"
    untagged_md.write_text(orig_md + "\nUntagged `[1.23 +/- 1e-5]`.\n", encoding="utf-8")
    res_untag = verify_tc059_review_displayed_enclosures(tc059_artifact, untagged_md)
    assert res_untag["untagged_count"] >= 1
    assert res_untag["all_displayed_intervals_contain_generated_enclosures"] is False

    # (c) Corrupting a tagged midpoint must fail containment
    corrupt_md = tmp_path / "corrupt_mid.md"
    corrupt_text = re.sub(
        r"`\[1\.3141397[0-9]* \+/- [0-9.eE+-]+\]`",
        "`[9.9999999 +/- 1e-10]`",
        orig_md,
        count=1,
    )
    assert corrupt_text != orig_md
    corrupt_md.write_text(corrupt_text, encoding="utf-8")
    res_corrupt = verify_tc059_review_displayed_enclosures(tc059_artifact, corrupt_md)
    assert res_corrupt["failed_count"] >= 1
    assert res_corrupt["all_displayed_intervals_contain_generated_enclosures"] is False
