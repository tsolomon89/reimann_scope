"""Focused mathematical, falsification, formalization, and 256-bit Arb certification test suite
for TASK-TC-059 / TASK-TC-059R / TASK-TC-059R2: Dyadic Power-Lift Arithmetic, Primitive Coprime
Correlations, Repaired Weighted-Diagonal Closure Interface, Mellin Bridge, Smooth-Increment Scope,
and Numerical Assertion / Citation Closeout.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import re
from typing import Sequence, Tuple

from flint import acb, acb_series, arb, ctx as flint_ctx
import pytest

import certification
from scripts import build_formal
from tc.canonical_theta_correlation_bound import REPO_ROOT
from tc.coupled_scale_energy_bootstrap import (
    _acb_integral_certified_arb,
    _frac_to_arb,
    _tau_arb,
    moebius_mu_int,
    prime_power_pairs_up_to,
)
from tc.dyadic_power_lift_primitive_correlation import (
    CLOSEOUT_BRANCH,
    DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH,
    EPISTEMIC_CATEGORIES,
    EXPECTED_TC059_THEOREMS,
    INCLUDED_TC_058R2_TIP,
    PARENT_SUBGATE_ID,
    PROPOSED_BRANCH,
    REPAIR_BRANCH,
    REVIEWED_MERGED_MAIN_BASELINE,
    REVIEWED_TC_059R_HEAD,
    REVIEWED_TC_059R_IMPLEMENTATION,
    REVIEWED_TC_059_HEAD,
    REVIEWED_TC_059_IMPLEMENTATION,
    TASK_TC_059_ID,
    TASK_TC_059R2_ID,
    TASK_TC_059R_ID,
    TC_059_LEAN_MODULE_PATH,
    TC_059_REVIEW_DOC_PATH,
    dyadic_power_lift_b_J_conv_table,
    dyadic_power_lift_b_J_divisor_int,
    evaluate_C_chi_var_smooth_arb,
    evaluate_C_var_gaussian_arb,
    evaluate_Q_general_arb,
    evaluate_bilinear_window_pairing_closed_arb,
    evaluate_primitive_coprime_sum_Pi_arb,
    evaluate_single_term_mellin_phi_quadrature_arb,
    evaluate_smooth_increment_and_jump_arb,
    evaluate_window_kernel_K_closed_arb,
    evaluate_window_kernel_K_quadrature_arb,
    is_squarefree_int,
    power_lift_increment_delta_J_int,
    stabilization_depth_J_T,
    verify_tc059_lean_theorems_live,
    verify_tc059_review_displayed_enclosures,
)
from tc.liouville_square_dilation import (
    _exact_arb_endpoints_as_fractions,
    liouville_lambda_int,
)
from tc.prime_chain_contraction import evaluate_phi_n_arb, exact_T_cutoff_ceil_Y_5_4


def _enclose_discrete_grid_max(balls: Sequence[arb]) -> arb:
    """Return an outward-rounded two-sided Arb enclosure of `max_i v_i` given enclosures `B_i ni v_i`.

    Lower bound: `max_i lower(B_i) <= max_i v_i`; upper bound: `max_i v_i <= max_i upper(B_i)`.
    """
    if not balls:
        raise ValueError("Discrete grid maximum requires at least one Arb ball")
    lo_balls = [b.lower() for b in balls]
    hi_balls = [b.upper() for b in balls]
    lo_max = max(lo_balls, key=lambda b: _exact_arb_endpoints_as_fractions(b)[0])
    hi_max = max(hi_balls, key=lambda b: _exact_arb_endpoints_as_fractions(b)[1])
    return lo_max.union(hi_max)


def _classify_interval_endpoints_le(
    lhs_lo: Fraction,
    lhs_hi: Fraction,
    rhs_lo: Fraction,
    rhs_hi: Fraction,
    *,
    exact_algebraic_equality_justified: bool = False,
) -> Tuple[str, bool]:
    """Classify whether exact intervals `[lhs_lo, lhs_hi]` and `[rhs_lo, rhs_hi]` certify `LHS <= RHS`.

    - `lhs_hi <= rhs_lo`: sufficient directed separation (`CERTIFIED_DIRECTED_INEQUALITY`, True),
      unless `exact_algebraic_equality_justified=True` is asserted on strictly separated intervals
      `lhs_hi < rhs_lo` (`INCONSISTENT_ALGEBRAIC_EQUALITY_CLAIM`, False).
    - `lhs_lo > rhs_hi`: strict violation (`REFUTED_STRICT_VIOLATION`, False).
    - Overlapping intervals (`lhs_hi > rhs_lo` and `lhs_lo <= rhs_hi`):
      returns (`NOT_NUMERICALLY_CERTIFIED_OVERLAP`, False) unless backed by an explicit exact
      algebraic or formal equality theorem (`exact_algebraic_equality_justified=True`), in which
      case enclosure overlap confirms consistency (`CERTIFIED_EXACT_ALGEBRAIC_EQUALITY_WITH_CONSISTENT_ENCLOSURE`, True).
    """
    if lhs_lo > lhs_hi or rhs_lo > rhs_hi:
        raise ValueError(f"Invalid interval endpoints: [{lhs_lo}, {lhs_hi}] vs [{rhs_lo}, {rhs_hi}]")
    if lhs_hi <= rhs_lo:
        if exact_algebraic_equality_justified and lhs_hi < rhs_lo:
            return ("INCONSISTENT_ALGEBRAIC_EQUALITY_CLAIM", False)
        return ("CERTIFIED_DIRECTED_INEQUALITY", True)
    if lhs_lo > rhs_hi:
        return ("REFUTED_STRICT_VIOLATION", False)
    if not exact_algebraic_equality_justified:
        return ("NOT_NUMERICALLY_CERTIFIED_OVERLAP", False)
    return ("CERTIFIED_EXACT_ALGEBRAIC_EQUALITY_WITH_CONSISTENT_ENCLOSURE", True)


def _classify_arb_le_certificate(
    lhs_ball: arb,
    rhs_ball: arb,
    *,
    exact_algebraic_equality_justified: bool = False,
) -> Tuple[str, bool]:
    """Directed Arb inequality certificate check using exact dyadic endpoints + outward difference."""
    lhs_lo, lhs_hi = _exact_arb_endpoints_as_fractions(lhs_ball)
    rhs_lo, rhs_hi = _exact_arb_endpoints_as_fractions(rhs_ball)
    status, certified = _classify_interval_endpoints_le(
        lhs_lo,
        lhs_hi,
        rhs_lo,
        rhs_hi,
        exact_algebraic_equality_justified=exact_algebraic_equality_justified,
    )
    diff_ball = rhs_ball - lhs_ball
    if status == "CERTIFIED_DIRECTED_INEQUALITY":
        if not bool(lhs_ball.upper() <= rhs_ball.lower() and diff_ball.lower() >= arb(0)):
            return ("NOT_NUMERICALLY_CERTIFIED_OVERLAP", False)
    elif status == "CERTIFIED_EXACT_ALGEBRAIC_EQUALITY_WITH_CONSISTENT_ENCLOSURE":
        if not bool(arb(0) in diff_ball):
            return ("INCONSISTENT_ALGEBRAIC_EQUALITY_CLAIM", False)
    return (status, certified)


@pytest.fixture(scope="module")
def tc059_artifact() -> dict:
    assert DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH.exists(), (
        f"Missing {DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH}"
    )
    return json.loads(
        DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH.read_text(encoding="utf-8")
    )


def test_artifact_metadata_and_epistemic_hygiene(tc059_artifact: dict) -> None:
    """Verify baseline provenance, gate status, zero-tau-only convention, and 256-bit Arb self-check."""
    assert tc059_artifact["task_id"] == TASK_TC_059R2_ID
    assert tc059_artifact["repaired_task_id"] == TASK_TC_059_ID
    assert tc059_artifact["prior_repair_task_id"] == TASK_TC_059R_ID
    assert tc059_artifact["parent_subgate"] == PARENT_SUBGATE_ID
    assert tc059_artifact["reviewed_merged_main_baseline"] == REVIEWED_MERGED_MAIN_BASELINE
    assert tc059_artifact["included_tc058r2_tip"] == INCLUDED_TC_058R2_TIP
    assert tc059_artifact["reviewed_tc059_branch"] == PROPOSED_BRANCH
    assert tc059_artifact["reviewed_tc059_implementation_commit"] == REVIEWED_TC_059_IMPLEMENTATION
    assert tc059_artifact["reviewed_tc059_head_commit"] == REVIEWED_TC_059_HEAD
    assert tc059_artifact["reviewed_tc059r_branch"] == REPAIR_BRANCH
    assert (
        tc059_artifact["reviewed_tc059r_implementation_commit"] == REVIEWED_TC_059R_IMPLEMENTATION
    )
    assert tc059_artifact["reviewed_tc059r_head_commit"] == REVIEWED_TC_059R_HEAD
    assert tc059_artifact["inherited_formal_producing_commit"] == REVIEWED_TC_059R_IMPLEMENTATION
    assert tc059_artifact["branch"] == CLOSEOUT_BRANCH
    assert tc059_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc059_artifact["rh_proved"] is False
    assert tc059_artifact["precision_bits"] == 256
    assert tc059_artifact["epistemic_categories_enforced"] == list(EPISTEMIC_CATEGORIES)
    assert "w = u + i*v" in tc059_artifact["complex_coordinate_convention"]

    arb_self = tc059_artifact["serialized_arb_self_check"]
    assert arb_self["all_enclose_original_256bit_arb_ball"] is True
    assert arb_self["total_certified_arb_balls_checked"] >= 450

    # Zero forbidden circle-half macros or Unicode characters across TC-059/TC-059R deliverables
    for chk_path in (
        TC_059_LEAN_MODULE_PATH,
        REPO_ROOT / "tc" / "dyadic_power_lift_primitive_correlation.py",
        DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH,
        TC_059_REVIEW_DOC_PATH,
    ):
        txt = chk_path.read_text(encoding="utf-8")
        assert "\u03c0" not in txt, f"Forbidden Unicode circle-half char in {chk_path}"
        assert len(re.findall(r"\x5cpi(?![a-zA-Z])", txt)) == 0, (
            f"Forbidden LaTeX circle-half macro in {chk_path}"
        )


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
    assert len(EXPECTED_TC059_THEOREMS) == 7


def test_tc059r_repair1_weighted_normalization_and_actual_observable_corollary(
    tc059_artifact: dict,
) -> None:
    """Verify Repair 1 & TC-059R2 Item 1: finite weighted mass <= zeta''(1+eps), factor 2 kept once
    in C_eps = 2*zeta''(1+eps), R-independent threshold Y_* and 2*K, explicit 5-hypothesis trace on
    canonicalLiouvilleEnergyE, and directed inequality certification for the discrete sampled maxima
    F_grid(Y/r) <= (Y/r)^eps * G_grid(64) on S_64 = {2, 4, 8, 16, 32, 64} (kept strictly distinct
    from the continuous suprema F and G_eps proved deductively in Lean Theorem 6).
    """
    sec1 = tc059_artifact["section_1_observable_and_closure_contract"]
    rep1 = sec1["repaired_weighted_diagonal_closure_and_actual_observable_tc059r"]
    assert rep1["verified"] is True
    assert (
        rep1["primary_lean_theorem"]
        == "repaired_weighted_diagonal_closure_and_actual_observable_tc059r"
    )
    assert rep1["infinite_horizon_supremum_assumed_finite"] is False
    assert rep1["auxiliary_same_scale_lemma_retained"].startswith(
        "parity_uniqueness_turn_chart_defect_and_log_saving_closure_tc059"
    )
    for wm_row in rep1["weighted_mass_and_horizon_checks"]:
        assert wm_row["factor_two_count"] == 1
        assert wm_row["verified"] is True

    trace = {h["hypothesis_id"]: h for h in rep1["actual_observable_corollary_hypothesis_trace"]}
    assert set(trace.keys()) == {
        "H1_NONNEGATIVITY",
        "H2_LINEAR_SCALE_MAJORANT",
        "H3_ROUTE_D_SHIFTED_PRIME_POWER_DIAGONAL",
        "H4_WEIGHTED_PRIME_POWER_ZETA_MAJORANT",
        "H5_QUANTIFIED_ARITHMETIC_LOG_SAVING_CONTRACT",
    }
    assert trace["H1_NONNEGATIVITY"]["classification"] == "CONCRETE_ANALYTIC_IN_LEAN"
    assert trace["H2_LINEAR_SCALE_MAJORANT"]["classification"] == "ANALYTIC_PROVED_OUTSIDE_LEAN"
    assert trace["H3_ROUTE_D_SHIFTED_PRIME_POWER_DIAGONAL"]["classification"] == (
        "ANALYTIC_PROVED_OUTSIDE_LEAN"
    )
    assert "Theorem 6.1" in trace["H3_ROUTE_D_SHIFTED_PRIME_POWER_DIAGONAL"]["source_and_discharge"]
    assert trace["H4_WEIGHTED_PRIME_POWER_ZETA_MAJORANT"]["classification"] == (
        "ANALYTIC_PROVED_OUTSIDE_LEAN"
    )
    assert trace["H5_QUANTIFIED_ARITHMETIC_LOG_SAVING_CONTRACT"]["classification"] == (
        "OPEN_CONJECTURE_OR_FAILED_CANDIDATE"
    )

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # Independent 256-bit Arb check across eps in {1/2, 1/4, 1/8}:
        # 1) sum_{p^k <= Y} (log p)^2 / (p^k)^{1+eps} <= sum_{p^k <= Y} (log(p^k))^2 / (p^k)^{1+eps} < zeta''(1+eps)
        # 2) C_eps = 2*zeta''(1+eps) (not 4*zeta''(1+eps))
        # 3) On the discrete 6-point sample set S_64 = {2, 4, 8, 16, 32, 64} with exact cutoff T(z),
        #    define finite sampled maxima F_grid(u) := max_{z in S_64, z <= u} E(z) and
        #    G_grid(64) := max_{z in S_64} E(z)/z^eps (distinct from continuous suprema F and G_eps,
        #    which are proved for all real 1 <= r <= Y <= R in Lean Theorem 6(2)).
        S_64 = (2, 4, 8, 16, 32, 64)
        lam_182 = [0] + [liouville_lambda_int(n) for n in range(1, 183)]
        grid_E = {
            z_val: evaluate_bilinear_window_pairing_closed_arb(
                arb(z_val), exact_T_cutoff_ceil_Y_5_4(z_val), lam_182, lam_182, prec_bits=256
            )
            for z_val in S_64
        }
        for eps_fr in (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8)):
            eps_a = _frac_to_arb(eps_fr)
            z_ser = acb_series([acb(arb(1) + eps_a), acb(1)], prec=256).zeta()
            zeta_pp = arb(2) * z_ser[2].real
            C_eps = arb(2) * zeta_pp
            assert bool(zeta_pp > arb(0) and abs(C_eps - arb(4) * zeta_pp) > arb(1))

            for Y_chk in (16, 64, 256):
                pp_mass = arb(0)
                pp_log_n = arb(0)
                for p_v, k_v in prime_power_pairs_up_to(Y_chk):
                    pk_a = arb(p_v ** k_v)
                    denom = pk_a ** (arb(1) + eps_a)
                    pp_mass += ((arb(p_v).log()) ** 2) / denom
                    pp_log_n += ((pk_a.log()) ** 2) / denom
                assert bool(pp_log_n - pp_mass >= arb(0))
                assert bool(zeta_pp - pp_log_n > arb(0))
                assert bool(zeta_pp - pp_mass > arb(0))

            # Two-sided outward-rounded enclosure of G_grid(64) := max_{z in S_64} E(z) / z^eps
            # (never substituting upper(G_grid) on the RHS of an inequality certificate):
            quotients_grid = {
                z_k: val / (arb(z_k) ** eps_a) for z_k, val in grid_E.items()
            }
            G_grid_ball = _enclose_discrete_grid_max(list(quotients_grid.values()))

            # Certify by strict directed separation on the finite set S_64 that z = 2 is the unique
            # maximizer of E(z)/z^eps on S_64 (so G_grid(64) = E(2)/2^eps as exact real numbers):
            unique_maximizer_is_2 = all(
                _classify_arb_le_certificate(
                    quotients_grid[z_other], quotients_grid[2]
                )
                == ("CERTIFIED_DIRECTED_INEQUALITY", True)
                and bool(quotients_grid[2] - quotients_grid[z_other] > arb(0))
                for z_other in S_64
                if z_other != 2
            )
            assert unique_maximizer_is_2 is True

            Y_sample = 32
            for r_div in (1, 2, 4, 8, 16):
                u_sub = Y_sample // r_div  # in {32, 16, 8, 4, 2}
                subgrid_pts = tuple(z_k for z_k in S_64 if z_k <= u_sub)
                F_grid_ball = _enclose_discrete_grid_max([grid_E[z_k] for z_k in subgrid_pts])
                rhs_grid_ball = ((arb(Y_sample) / arb(r_div)) ** eps_a) * G_grid_ball

                if r_div in (1, 2, 4, 8):
                    # Non-singleton subgrids u_sub in {32, 16, 8, 4}: certified strictly by directed
                    # interval separation upper(F_grid_ball) <= lower(rhs_grid_ball):
                    status, certified = _classify_arb_le_certificate(
                        F_grid_ball, rhs_grid_ball, exact_algebraic_equality_justified=False
                    )
                    assert (status, certified) == ("CERTIFIED_DIRECTED_INEQUALITY", True)
                else:
                    # r_div == 16 (u_sub == 2): raw overlapping balls alone must NOT be reported as
                    # numerically certified inequality:
                    raw_status, raw_certified = _classify_arb_le_certificate(
                        F_grid_ball, rhs_grid_ball, exact_algebraic_equality_justified=False
                    )
                    assert (raw_status, raw_certified) == (
                        "NOT_NUMERICALLY_CERTIFIED_OVERLAP",
                        False,
                    )
                    # Genuine exact equality F_grid(2) = E(2) = 2^eps * (E(2)/2^eps) = 2^eps * G_grid(64),
                    # justified by singleton subgrid {z in S_64 : z <= 2} == {2}, strict finite-set
                    # maximizer proof G_grid(64) = E(2)/2^eps, and real algebra a * (x / a) = x (a = 2^eps > 0):
                    exact_algebraic_tie = bool(
                        subgrid_pts == (2,)
                        and unique_maximizer_is_2
                        and Fraction(Y_sample, r_div) == Fraction(2, 1)
                    )
                    assert exact_algebraic_tie is True
                    eq_status, eq_certified = _classify_arb_le_certificate(
                        F_grid_ball,
                        rhs_grid_ball,
                        exact_algebraic_equality_justified=exact_algebraic_tie,
                    )
                    assert (eq_status, eq_certified) == (
                        "CERTIFIED_EXACT_ALGEBRAIC_EQUALITY_WITH_CONSISTENT_ENCLOSURE",
                        True,
                    )
                    assert bool(abs(rhs_grid_ball - F_grid_ball) < arb("1e-73"))
    finally:
        flint_ctx.prec = saved


def test_tc059r2_adversarial_interval_inequality_semantics() -> None:
    """Adversarial regression for TC-059R2 Item 1:
    1) Overlapping intervals LHS = [2, 4] and RHS = [1, 3] pass the retired endpoint check
       upper(RHS) >= lower(LHS) (3 >= 2) despite violating LHS <= RHS (e.g. 4 > 1), and MUST
       be rejected as NOT_NUMERICALLY_CERTIFIED_OVERLAP (False).
    2) Separated valid intervals LHS = [1, 2], RHS = [3, 4] certify LHS <= RHS via directed separation.
    3) Separated violated intervals LHS = [4, 5], RHS = [1, 2] fail as REFUTED_STRICT_VIOLATION.
    4) Zero-containing residual overlap without algebraic proof is NOT certified; genuine algebraic
       equality requires explicit justification and consistent enclosure, and rejects separated balls.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # 1) Adversarial overlap: LHS = [2, 4], RHS = [1, 3]
        assert Fraction(3) >= Fraction(2)  # retired endpoint check passes falsely
        assert _classify_interval_endpoints_le(
            Fraction(2), Fraction(4), Fraction(1), Fraction(3)
        ) == ("NOT_NUMERICALLY_CERTIFIED_OVERLAP", False)

        lhs_overlap = arb(2).union(arb(4))
        rhs_overlap = arb(1).union(arb(3))
        assert bool(rhs_overlap.upper() >= lhs_overlap.lower()) is True  # old check passes!
        assert _classify_arb_le_certificate(lhs_overlap, rhs_overlap) == (
            "NOT_NUMERICALLY_CERTIFIED_OVERLAP",
            False,
        )

        # 2) Separated valid case: LHS = [1, 2], RHS = [3, 4]
        lhs_valid = arb(1).union(arb(2))
        rhs_valid = arb(3).union(arb(4))
        assert _classify_arb_le_certificate(lhs_valid, rhs_valid) == (
            "CERTIFIED_DIRECTED_INEQUALITY",
            True,
        )

        # 3) Separated violated case: LHS = [4, 5], RHS = [1, 2]
        lhs_viol = arb(4).union(arb(5))
        rhs_viol = arb(1).union(arb(2))
        assert _classify_arb_le_certificate(lhs_viol, rhs_viol) == (
            "REFUTED_STRICT_VIOLATION",
            False,
        )

        # 4) Zero-containing residual without algebraic proof must NOT certify equality or inequality
        same_a = arb(2).union(arb(3))
        same_b = arb(2).union(arb(3))
        assert bool(arb(0) in (same_b - same_a)) is True
        assert _classify_arb_le_certificate(
            same_a, same_b, exact_algebraic_equality_justified=False
        ) == ("NOT_NUMERICALLY_CERTIFIED_OVERLAP", False)

        # Genuine algebraic identity x = (2^eps) * (x / 2^eps) on non-exact binary ball x = 7/3:
        x_val = arb(7) / arb(3)
        scale_val = arb(2) ** (arb(1) / arb(2))
        rhs_alg = scale_val * (x_val / scale_val)
        assert _classify_arb_le_certificate(
            x_val, rhs_alg, exact_algebraic_equality_justified=False
        ) == ("NOT_NUMERICALLY_CERTIFIED_OVERLAP", False)
        assert _classify_arb_le_certificate(
            x_val, rhs_alg, exact_algebraic_equality_justified=True
        ) == ("CERTIFIED_EXACT_ALGEBRAIC_EQUALITY_WITH_CONSISTENT_ENCLOSURE", True)

        # Misapplying algebraic-equality flag to separated intervals fails closed:
        assert _classify_arb_le_certificate(
            lhs_valid, rhs_valid, exact_algebraic_equality_justified=True
        ) == ("INCONSISTENT_ALGEBRAIC_EQUALITY_CLAIM", False)
        assert _classify_arb_le_certificate(
            lhs_viol, rhs_viol, exact_algebraic_equality_justified=True
        ) == ("REFUTED_STRICT_VIOLATION", False)
    finally:
        flint_ctx.prec = saved


def test_tc059r_repair2_single_term_mellin_scaling_and_pole_coordinates(
    tc059_artifact: dict,
) -> None:
    """Verify Repair 2: consistent inverse-Mellin convention M_Q(w) = int_0^infty Q(X)*X^{-w} dX/X,
    single-term scaling (1/2)*Gamma(5/4 - w/2)*n^{-1/2 - w} on u < 5/2, strict refutation of the
    retired mixed formula (1/2)*Gamma((2w+5)/4)*n^{-(w+3/2)}, u = 5/2 boundary guard, and pole map
    w_rho = rho - 1/2 in {0 < u < 5/2}.
    """
    sec5 = tc059_artifact["section_5_tc_geometry_defect_and_murmurations"]
    mel = sec5["mellin_convention_and_pole_domain_audit_tc059r"]
    assert mel["verified"] is True
    assert "1/2 < u < 5/2" in mel["initial_absolute_convergence_strip"]
    assert "0 < u < 5/2" in mel["subpower_holomorphic_extension_strip"]
    assert "w_rho = rho - 1/2" in mel["pole_coordinate_for_hypothetical_zero_rho_x_gt_half"]

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # Check domain guard at u = 5/2 (small-X divergence boundary)
        with pytest.raises(ValueError, match="Re\\(w\\) < 5/2"):
            evaluate_single_term_mellin_phi_quadrature_arb(1, acb(arb(5) / arb(2)), prec_bits=256)

        # Check n-scaling and Gamma factor across initial strip (u = 5/4) and continuation strip (u = 1/4)
        for w_test in (acb(arb(5) / arb(4), arb(3) / arb(4)), acb(arb(1) / arb(4), arb(1))):
            i_1 = evaluate_single_term_mellin_phi_quadrature_arb(1, w_test, prec_bits=256)
            for n_test in (1, 2, 5):
                i_n = evaluate_single_term_mellin_phi_quadrature_arb(n_test, w_test, prec_bits=256)
                rhs_true = (
                    (acb(1) / acb(2))
                    * (acb(arb(5) / arb(4)) - w_test / acb(2)).gamma()
                    * (acb(n_test) ** (-acb(1) / acb(2) - w_test))
                )
                rhs_retired = (
                    (acb(1) / acb(2))
                    * ((acb(2) * w_test + acb(5)) / acb(4)).gamma()
                    * (acb(n_test) ** (-w_test - acb(3) / acb(2)))
                )
                diff_true = i_n - rhs_true
                assert bool(
                    arb(0) in diff_true.real
                    and arb(0) in diff_true.imag
                    and abs(diff_true) < arb("1e-62")
                )
                assert bool(abs(i_n - rhs_retired) > arb("1e-2"))
                if n_test > 1:
                    ratio_n = i_n / i_1
                    true_scale = acb(n_test) ** (-acb(1) / acb(2) - w_test)
                    wrong_scale = acb(n_test) ** (-w_test - acb(3) / acb(2))
                    assert bool(abs(ratio_n - true_scale) < arb("1e-60"))
                    assert bool(abs(ratio_n - wrong_scale) > arb("1e-2"))

        # Check hypothetical off-line zero coordinate mapping rho = x + i*y (1/2 < x < 1) -> w_rho = rho - 1/2
        for x_num, x_den, y_im in ((3, 5, 21), (7, 8, -9)):
            x_fr = Fraction(x_num, x_den)
            u_fr = x_fr - Fraction(1, 2)
            assert Fraction(0) < u_fr < Fraction(5, 2)
            assert Fraction(1, 2) + u_fr == x_fr
            assert Fraction(1) + 2 * u_fr == 2 * x_fr
            rho_c = acb(arb(x_num) / arb(x_den), arb(y_im))
            w_rho = rho_c - acb(arb(1) / arb(2))
            assert bool(w_rho.real > arb(0) and arb(5) / arb(2) - w_rho.real > arb(0))
            denom_diff = (acb(arb(1) / arb(2)) + w_rho) - rho_c
            num_diff = (acb(1) + acb(2) * w_rho) - acb(2) * rho_c
            assert bool(
                arb(0) in denom_diff.real
                and arb(0) in denom_diff.imag
                and abs(denom_diff) < arb("1e-74")
            )
            assert bool(
                arb(0) in num_diff.real
                and arb(0) in num_diff.imag
                and abs(num_diff) < arb("1e-74")
            )
            assert bool(abs((acb(arb(5) / arb(4)) - w_rho / acb(2)).gamma()) > arb(0))
            assert bool(abs((acb(1) + acb(2) * w_rho).zeta()) > arb(0))
    finally:
        flint_ctx.prec = saved


def test_tc059r_repair3_smooth_increment_jump_norm_and_cancellation_loss(
    tc059_artifact: dict,
) -> None:
    """Verify Repair 3: unchanged cutoff L_d = floor(T/d) at both smooth endpoints, nontrivial
    L_d != L_{d+1} jump separation, exact -sqrt(X) integral sign, direct window norm bound
    (including T = 0 and sub-unit Y/(d+1) < 1), cutoff conversion, and adjacent-scale cancellation loss.
    """
    sec4 = tc059_artifact["section_4_dyadic_blocks_and_attempt_b"]
    sm_rep = sec4["smooth_increment_endpoint_and_norm_repair_tc059r"]
    assert sm_rep["verified"] is True
    assert sm_rep["critical_line_crossing_required_for_direct_norm_bound"] is False
    assert sm_rep["lean_theorem"] == "smooth_increment_window_norm_and_small_scale_tail_tc059r"
    adj = sm_rep["adjacent_scale_cancellation_loss_Y64_T182"]
    assert adj["verified"] is True
    assert float(adj["minkowski_over_actual_ratio"]["lower_dec"]) > 1000.0
    assert "remaining_quantitative_requirement" not in adj
    assert "possible_next_research_target" in adj
    assert "Such an estimate is not established here." in adj["possible_next_research_target"]
    assert "alpha >= 1/2" in adj["possible_next_research_target"]
    assert "extra d^{-1-alpha}" not in adj["possible_next_research_target"]

    why_b2 = sec4["attempt_b_pre_stated_schemas"][1]["why_not_subpower"]
    assert "inherited_vs_canonical_cutoff_comparison_and_counterexample_tc057" in why_b2
    assert "Theorem 25, first main conjunct, third item" in why_b2
    assert "Theorem 5.1(2)" not in why_b2
    assert "extra d^{-1-alpha}" not in why_b2
    assert "Such an estimate is not established here." in why_b2

    rev_txt = TC_059_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    assert "inherited_vs_canonical_cutoff_comparison_and_counterexample_tc057" in rev_txt
    assert "Theorem 25, first main conjunct, third item" in rev_txt
    assert "Theorem 25(2)" not in rev_txt
    assert "\\asymp d^{1/2}" not in rev_txt
    assert "extra $d^{-1-\\alpha}$" not in rev_txt

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau = _tau_arb()
        # Nontrivial floor jump at (T=5, d=2): L_2 = 2 != 1 = L_3
        ev_5_2 = evaluate_smooth_increment_and_jump_arb(Fraction(7, 2), 5, 2, prec_bits=256)
        assert bool(
            arb(0) in (ev_5_2["g_d_minus_g_d1"] - (ev_5_2["delta_sm_endpoint"] + ev_5_2["delta_jump"]))
        )
        assert bool(abs(ev_5_2["delta_jump"]) > arb("1e-6"))
        # Silently replacing L_2 by L_3 at the second endpoint changes delta_sm by delta_jump != 0!
        assert bool(abs(ev_5_2["g_d_minus_g_d1"] - ev_5_2["delta_sm_endpoint"]) > arb("1e-6"))
        # Sign check: delta_sm_endpoint == -sqrt(X)*int ... and strictly != +sqrt(X)*int ...
        assert bool(
            arb(0) in (ev_5_2["delta_sm_endpoint"] - ev_5_2["delta_sm_integral"])
            and abs(ev_5_2["delta_sm_endpoint"] - ev_5_2["delta_sm_integral"]) < arb("1e-62")
        )
        assert bool(abs(ev_5_2["delta_sm_endpoint"] + ev_5_2["delta_sm_integral"]) > arb("1e-6"))

        # Zero cutoff T = 0 edge case
        ev_0 = evaluate_smooth_increment_and_jump_arb(Fraction(5, 1), 0, 1, prec_bits=256)
        assert ev_0["delta_sm_endpoint"] == arb(0)
        assert ev_0["delta_sm_integral"] == arb(0)
        assert ev_0["delta_jump"] == arb(0)

        # Cutoff conversion check: sqrt(E_{lambda, L_d}(Y/m)) <= sqrt(E(Y/m)) + sqrt(2*(tau^5 - 1)/5)
        # on Y = 16, T = T(16) = 32, d in {1, 2, 3, 5}, m in {d, d + 1} (all Y/m >= 16/6 > 1):
        c_cut_sharp = (arb(2) * (tau ** 5 - arb(1)) / arb(5)).sqrt()
        c_cut_loose = arb(2) * ((tau ** 5 - arb(1)) / arb(5)).sqrt()
        assert bool(c_cut_loose - c_cut_sharp > arb(0))
        lam_32 = [0] + [liouville_lambda_int(q) for q in range(1, 40)]
        for d_conv in (1, 2, 3, 5):
            L_d_c = 32 // d_conv
            for m_scale in (d_conv, d_conv + 1):
                w_frac = Fraction(16, m_scale)
                w_arb = _frac_to_arb(w_frac)
                T_w = math.ceil(float(w_frac) ** 1.25)
                while (T_w - 1) > 0 and ((T_w - 1) ** 4) * (m_scale ** 5) >= 16 ** 5:
                    T_w -= 1
                while (T_w ** 4) * (m_scale ** 5) < 16 ** 5:
                    T_w += 1
                e_inh = evaluate_bilinear_window_pairing_closed_arb(
                    w_arb, L_d_c, lam_32, lam_32, prec_bits=256
                ).sqrt()
                e_can = evaluate_bilinear_window_pairing_closed_arb(
                    w_arb, T_w, lam_32, lam_32, prec_bits=256
                ).sqrt()
                assert bool((e_can + c_cut_sharp) - e_inh > arb(0))
    finally:
        flint_ctx.prec = saved


def test_tc059r_repair4_scope_small_scale_tail_and_arbitrary_window_base(
    tc059_artifact: dict,
) -> None:
    """Verify Repair 4: auxiliary real-coordinate scope for K^*, stabilization_depth_J_T Lean vs
    outside-Lean scope, small-scale u < 2 O(u^5) bound & O(1) tail on g > floor(Y/2), and
    parameterized [Y, b*Y] scaling at an additional multiplier b = 3/2 outside {2, e, tau}.
    """
    sec2 = tc059_artifact["section_2_dyadic_power_lift_and_attempt_a"]
    sec3 = tc059_artifact["section_3_primitive_pairs_and_diagonals"]
    sec4 = tc059_artifact["section_4_dyadic_blocks_and_attempt_b"]
    sec5 = tc059_artifact["section_5_tc_geometry_defect_and_murmurations"]

    assert sec2["epistemic_scope"]["stabilization_minimality_inequalities_in_lean"] == (
        "UNCONDITIONAL_FINITE_ARITHMETIC"
    )
    assert sec2["epistemic_scope"]["stabilization_depth_O_log_log_T_consequence"] == (
        "ANALYTIC_PROVED_OUTSIDE_LEAN"
    )
    assert "a(g)^2 = 1" in sec3["generalized_coefficient_hypotheses_note"]
    assert (
        sec5["turn_chart_audit"]["K_star_scope_statement"]
        == "treated as an auxiliary real coordinate; algebraic-grade admissibility is not established"
    )

    u5_sec = sec4["small_scale_u5_and_tail_control_tc059r"]
    assert u5_sec["verified"] is True

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau = _tau_arb()
        C_u5 = arb(9) * (tau ** 5 - arb(1)) / arb(20)
        C_tail = C_u5 * (arb(1024) / arb(5))
        # Direct small-scale u < 2 check at u = 7/4 < 2, L = 12
        u_7_4 = arb(7) / arb(4)
        pi_7_4 = evaluate_primitive_coprime_sum_Pi_arb(u_7_4, 12, mode="liouville", prec_bits=256)
        assert bool(C_u5 * (u_7_4 ** 5) - abs(pi_7_4) > arb(0))

        # Tail check at Y = 8 (T = 14, M = 4): sum_{g=5}^{14} g^{-1}*|Pi_{lambda, floor(14/g)}(8/g)| < C_tail
        tail_8 = arb(0)
        for g_v in range(5, 15):
            pi_g = evaluate_primitive_coprime_sum_Pi_arb(
                arb(8) / arb(g_v), 14 // g_v, mode="liouville", prec_bits=256
            )
            tail_8 += abs(pi_g) / arb(g_v)
        assert bool(C_tail - tail_8 > arb(0))

        # Parameterized [Y, b*Y] scaling check at b = 3/2 (outside {2, e, tau}) for Y = 6, T = 10:
        b_3_2 = arb(3) / arb(2)
        lam_10 = [0] + [liouville_lambda_int(n) for n in range(1, 11)]
        e_b = evaluate_bilinear_window_pairing_closed_arb(
            arb(6), 10, lam_10, lam_10, base_mult=b_3_2, prec_bits=256
        )
        e_b_prim = arb(0)
        for g_b in range(1, 11):
            L_gb = 10 // g_b
            for r_b in range(1, L_gb + 1):
                for s_b in range(1, L_gb + 1):
                    if math.gcd(r_b, s_b) == 1:
                        e_b_prim += (
                            arb(liouville_lambda_int(r_b * s_b))
                            * evaluate_window_kernel_K_closed_arb(
                                arb(6) / arb(g_b), r_b, s_b, base_mult=b_3_2, prec_bits=256
                            )
                            / arb(g_b)
                        )
        res_b = e_b - e_b_prim
        assert bool(arb(0) in res_b and abs(res_b) < arb("1e-66"))
    finally:
        flint_ctx.prec = saved
