"""Tests for TASK-TC-054: Liouville Square-Dilation Transfer, Unconstrained Common-Factor
Expansion, Transition Poisson Summation, and Separable Gaussian Decoupling.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from flint import arb, ctx as flint_ctx
import pytest

from certification import REQUIRED_FORMAL_SOURCES
from scripts.build_formal import FORMAL_SOURCE_FILES
from tc.canonical_theta_correlation_bound import REPO_ROOT, verify_all_serialized_arb_in_tree
from tc.liouville_square_dilation import (
    LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH,
    LIOUVILLE_SQUARE_DILATION_LEAN_MODULE_PATH,
    PRIOR_MERGED_MAIN_TC_053R,
    TASK_TC_054_ID,
    TC_053R2_IMPLEMENTATION_COMMIT,
    TC_053R2_REVIEWED_TIP,
    evaluate_1d_dyadic_sum_U_lambda_arb,
    evaluate_Q_arith_certified_arb,
    evaluate_d_sum_certified_arb,
    evaluate_decoupled_rectangular_block_B_AB_certified_arb,
    evaluate_hat_f_hypergeometric_certified_arb,
    evaluate_rectangular_block_B_AB_certified_arb,
    evaluate_square_dilation_transfer_certified_arb,
    execute_task_tc054_liouville_square_dilation_audit,
    liouville_lambda_int,
    omega_with_multiplicity_int,
    square_divisor_inverse_liouville_sum_int,
    square_divisor_moebius_sum_int,
    verify_euler_maclaurin_derivatives_and_constants_arb,
    verify_liouville_square_dilation_lean_module,
    verify_section_2_and_3_square_dilation_transfer,
    verify_section_4_unconstrained_common_factor_and_euler_maclaurin,
    verify_section_5_poisson_summation_at_transition,
    verify_section_6_transition_attacks_and_decoupling,
)
from tc.prime_euler_moebius_recovery import moebius_mu_int


def test_square_divisor_moebius_liouville_convolutions_and_common_factor_sign() -> None:
    """Verify lambda(n) = sum_{d^2 | n} mu(n/d^2), mu(n) = sum_{d^2 | n} mu(d) lambda(n/d^2)
    up to n = 200, and lambda(d r) lambda(d s) = lambda(r) lambda(s) for 1 <= d, r, s <= 30.
    """
    assert omega_with_multiplicity_int(1) == 0
    assert liouville_lambda_int(1) == 1
    assert liouville_lambda_int(2) == -1
    assert liouville_lambda_int(4) == 1
    assert liouville_lambda_int(8) == -1
    assert liouville_lambda_int(12) == -1
    assert liouville_lambda_int(36) == 1

    for n in range(1, 201):
        assert square_divisor_moebius_sum_int(n) == liouville_lambda_int(n), f"Forward failed at n={n}"
        assert square_divisor_inverse_liouville_sum_int(n) == moebius_mu_int(n), f"Inverse failed at n={n}"

    for d in [1, 2, 4, 6, 8, 9, 12, 16, 18, 25, 27, 30]:
        for r in range(1, 31):
            for s in range(1, 31):
                assert (
                    liouville_lambda_int(d * r) * liouville_lambda_int(d * s)
                    == liouville_lambda_int(r) * liouville_lambda_int(s)
                )


def test_section_2_and_3_square_dilation_transfer_and_norm_multipliers() -> None:
    """Verify direct vs square-dilation transfer evaluations of Q_mu(X) and Q_lambda(X)
    and weighted norm multipliers across sigma > 0.
    """
    sec23 = verify_section_2_and_3_square_dilation_transfer(prec_bits=256)
    assert sec23["square_divisor_convolution_audit"]["all_forward_lambda_eq_sum_mu_n_over_d2"] is True
    assert sec23["square_divisor_convolution_audit"]["all_inverse_mu_eq_sum_mu_d_lambda_n_over_d2"] is True
    assert (
        sec23["complete_multiplicativity_common_factor_audit"][
            "all_triples_satisfy_lambda_dr_lambda_ds_eq_lambda_r_lambda_s"
        ]
        is True
    )
    assert sec23["all_transfer_enclosures_contain_zero_difference"] is True

    rows = sec23["square_dilation_transfer_rows"]
    assert len(rows) == 6
    for row in rows:
        assert row["Q_mu_zero_in_difference"] is True
        assert row["Q_lambda_zero_in_difference"] is True
        assert row["abs_Q_mu_le_zeta3_X_5_2"] is True
        assert row["abs_Q_lambda_le_zeta3_X_5_2"] is True

    mult_rows = sec23["weighted_dilation_norm_equivalence"]["multiplier_table"]
    assert len(mult_rows) == 5
    for mrow in mult_rows:
        assert mrow["forward_multiplier_positive_finite"] is True
        assert mrow["reverse_multiplier_positive_finite"] is True


def test_section_4_euler_maclaurin_constants_and_subtransition_error_bounds() -> None:
    """Verify symbolic and 256-bit Arb derivatives f', f'', f^{(3)}, f^{(4)}, inflection
    points v_+/-, C_2, C_4, d-sum bounds, pairwise bounds, and coprime aggregate bounds.
    """
    sec4 = verify_section_4_unconstrained_common_factor_and_euler_maclaurin(prec_bits=256)
    em = sec4["euler_maclaurin_derivatives_and_constants"]
    assert em["sympy_derivative_identities_verified"] is True
    assert em["f_prime_v_minus_positive"] is True
    assert em["f_prime_v_plus_negative"] is True

    c2_low = float(em["C_2"]["lower_dec"])
    c2_high = float(em["C_2"]["upper_dec"])
    assert c2_low <= 1.851257667016958 <= c2_high

    c4_low = float(em["C_4"]["lower_dec"])
    c4_high = float(em["C_4"]["upper_dec"])
    assert c4_low <= 8.752371760035366 <= c4_high

    assert sec4["all_d_sum_em_bounds_hold"] is True
    assert sec4["all_pairwise_bounds_hold"] is True
    assert sec4["all_aggregate_bounds_hold"] is True


def test_section_5_transition_poisson_summation_and_sign_changes() -> None:
    """Verify exact Poisson summation formula and certified sign changes of hat{f}(xi)."""
    sec5 = verify_section_5_poisson_summation_at_transition(prec_bits=256)
    assert sec5["all_poisson_enclosures_contain_zero_difference"] is True

    witnesses = {w["xi_label"]: w for w in sec5["hat_f_sign_change_witnesses"]}
    assert witnesses["0"]["sign_strictly_certified"] is True
    assert float(witnesses["0"]["hat_f_xi"]["lower_dec"]) > 1.32934

    assert witnesses["1/2"]["expected_sign"] == "negative"
    assert witnesses["1/2"]["sign_strictly_certified"] is True
    assert float(witnesses["1/2"]["hat_f_xi"]["upper_dec"]) < -0.562854

    assert witnesses["1"]["expected_sign"] == "negative"
    assert witnesses["1"]["sign_strictly_certified"] is True
    assert float(witnesses["1"]["hat_f_xi"]["upper_dec"]) < -0.366836

    assert witnesses["3/2"]["expected_sign"] == "positive"
    assert witnesses["3/2"]["sign_strictly_certified"] is True
    assert float(witnesses["3/2"]["hat_f_xi"]["lower_dec"]) > 0.263617

    assert witnesses["2"]["expected_sign"] == "positive"
    assert witnesses["2"]["sign_strictly_certified"] is True
    assert float(witnesses["2"]["hat_f_xi"]["lower_dec"]) > 0.124712

    for prow in sec5["poisson_vs_direct_d_sum_rows"]:
        assert prow["zero_in_difference"] is True


def test_section_6_separable_gaussian_decoupling_and_dyadic_parity() -> None:
    """Verify rectangular-block separable Gaussian decoupling (Attack A) and dyadic
    parity annihilation/inversion (Attack B).
    """
    sec6 = verify_section_6_transition_attacks_and_decoupling(prec_bits=256)
    rect = sec6["rectangular_block_decomposition_and_decoupling"]
    assert rect["all_decoupled_blocks_match_direct"] is True
    assert rect["all_widely_unequal_bounds_hold"] is True

    att_a = sec6["attack_A_coprime_euler_series_and_separable_gaussian_replacement_theorem"]
    assert att_a["residue_at_z_0_strictly_negative"] is True
    for mrow in att_a["mellin_1d_rows"]:
        assert mrow["zero_in_difference"] is True
    for brow in att_a["bivariate_coprime_dirichlet_rows"]:
        assert brow["zero_in_difference"] is True

    att_b = sec6["attack_B_dyadic_parity_and_cross_scale_correlation"]
    assert att_b["all_dyadic_parity_identities_hold"] is True
    for drow in att_b["dyadic_parity_rows"]:
        assert drow["odd_sum_zero_in_difference"] is True
        assert drow["dyadic_inversion_zero_in_difference"] is True
        assert drow["pointwise_energy_zero_in_difference"] is True
    for orow in att_b["off_critical_mode_nonvanishing_rows"]:
        assert orow["strictly_positive_lower_bound"] is True


def test_lean_formalization_and_serialized_artifact_synchronization() -> None:
    """Verify formal/RiemannScope/LiouvilleSquareDilation.lean registration, theorem counts,
    and serialized artifact integrity.
    """
    rel_lean = "formal/RiemannScope/LiouvilleSquareDilation.lean"
    assert rel_lean in REQUIRED_FORMAL_SOURCES
    assert rel_lean in FORMAL_SOURCE_FILES
    root_lean = (REPO_ROOT / "formal" / "RiemannScope.lean").read_text(encoding="utf-8")
    assert "import RiemannScope.LiouvilleSquareDilation" in root_lean

    lean_info = verify_liouville_square_dilation_lean_module()
    assert lean_info["definition_count"] == 5
    assert lean_info["public_theorem_count"] == 5
    assert lean_info["private_helper_theorem_count"] == 1
    assert lean_info["total_declaration_count"] == 11
    assert lean_info["expected_public_theorems_present"] is True
    assert lean_info["sorry_count"] == 0
    assert lean_info["custom_axiom_count"] == 0

    assert LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH.exists()
    artifact = json.loads(LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert artifact["task_id"] == TASK_TC_054_ID
    assert artifact["prior_merged_main"] == PRIOR_MERGED_MAIN_TC_053R
    assert artifact["tc053r2_implementation_commit"] == TC_053R2_IMPLEMENTATION_COMMIT
    assert artifact["tc053r2_reviewed_tip"] == TC_053R2_REVIEWED_TIP
    assert artifact["subgate_tc043a_status"] == "OPEN"
    assert artifact["rh_proved"] is False
    live_rep = execute_task_tc054_liouville_square_dilation_audit(prec_bits=256)
    arb_check = verify_all_serialized_arb_in_tree(live_rep)
    assert arb_check["all_enclose_original_256bit_arb_ball"] is True
    assert arb_check["failed_paths"] == []


def test_tc054_review_and_state_synchronization() -> None:
    """Verify that docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md, .agents/research/state.json,
    and .agents/research/queue.json are synchronized with data/tc_liouville_square_dilation.json
    and keep SUBGATE-TC-043A OPEN and rh_proved False.
    """
    from decimal import Decimal, getcontext

    review_path = REPO_ROOT / "docs" / "reviews" / "TC_LIOUVILLE_SQUARE_DILATION.md"
    assert review_path.exists()
    review_text = review_path.read_text(encoding="utf-8")
    for token in [
        "1.851257667016958056850958359201349291641",
        "8.752371760035365551239039765015814873069",
        "-0.5628546550179851263755109492164491931001",
        "-0.3668367826642069184644449070564857828859",
        "0.2636171831500303372338138695632955698496",
        "0.1247126116325928138362162976104693467978",
        "liouville_complete_multiplicativity_and_common_factor_cancellation_nat",
        "prime_power_square_divisor_moebius_liouville_inversion_nat",
        "reversible_weighted_dilation_norm_and_grade_interval_equivalence",
        "euler_maclaurin_c2_and_subtransition_growing_range_exponent",
        "dyadic_parity_energy_and_off_critical_mode_nonvanishing",
    ]:
        assert token in review_text, f"Missing token {token!r} in TC_LIOUVILLE_SQUARE_DILATION.md"

    artifact = json.loads(LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH.read_text(encoding="utf-8"))
    em = artifact["section_4_unconstrained_common_factor_and_euler_maclaurin"][
        "euler_maclaurin_derivatives_and_constants"
    ]
    witnesses = {
        w["xi_label"]: w["hat_f_xi"]
        for w in artifact["section_5_transition_poisson_summation"]["hat_f_sign_change_witnesses"]
    }
    displayed_latex_checks = [
        ("[0.4211708612882846189067416640646506740997 \\pm 2.00 \\times 10^{-40}]", "0.4211708612882846189067416640646506740997", "2.00e-40", em["v_minus"]),
        ("[0.7327351635395962094861244517470714998819 \\pm 2.00 \\times 10^{-40}]", "0.7327351635395962094861244517470714998819", "2.00e-40", em["v_plus"]),
        ("[1.851257667016958056850958359201349291641 \\pm 2.00 \\times 10^{-39}]", "1.851257667016958056850958359201349291641", "2.00e-39", em["C_2"]),
        ("[8.752371760035365551239039765015814873069 \\pm 4.00 \\times 10^{-39}]", "8.752371760035365551239039765015814873069", "4.00e-39", em["C_4"]),
        (
            "[-0.1551682265483492584272379814757961069612 \\pm 2.00 \\times 10^{-40}]",
            "-0.1551682265483492584272379814757961069612",
            "2.00e-40",
            artifact["section_6_rectangular_blocks_and_transition_attacks"][
                "attack_A_coprime_euler_series_and_separable_gaussian_replacement_theorem"
            ]["residue_at_z_0_Gamma_5_4_over_4_zeta_1_2"],
        ),
    ]
    getcontext().prec = 100
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for disp_str, mid_s, rad_s, cert in displayed_latex_checks:
            assert disp_str in review_text, f"Missing displayed interval {disp_str!r} in TC_LIOUVILLE_SQUARE_DILATION.md"
            d_mid = Decimal(mid_s)
            d_rad = Decimal(rad_s)
            c_low = Decimal(cert["lower_dec"])
            c_high = Decimal(cert["upper_dec"])
            assert d_mid - d_rad <= c_low <= c_high <= d_mid + d_rad
            b_cert = arb(cert["arb_ball_str"])
            b_disp = arb(mid_s) + arb(0, rad_s)
            assert bool(b_disp.lower() <= b_cert.lower()) and bool(b_disp.upper() >= b_cert.upper())
        for xi_label, cert in witnesses.items():
            assert cert["arb_ball_str"] in review_text, f"Missing witness arb_ball_str for xi={xi_label}"
            b_cert = arb(cert["arb_ball_str"])
            assert bool(b_cert.lower() >= arb(cert["lower_dec"]).lower())
            assert bool(b_cert.upper() <= arb(cert["upper_dec"]).upper())
    finally:
        flint_ctx.prec = saved_prec

    state = json.loads((REPO_ROOT / ".agents" / "research" / "state.json").read_text(encoding="utf-8"))
    assert "data/tc_liouville_square_dilation.json" in state["linked_runs"]["campaign_artifacts"]

    queue = json.loads((REPO_ROOT / ".agents" / "research" / "queue.json").read_text(encoding="utf-8"))
    assert queue["active_task_id"] == "TASK-TC-054"
    tc054_entries = [t for t in queue["tasks"] if t["task_id"] == "TASK-TC-054"]
    assert len(tc054_entries) == 1
    assert tc054_entries[0]["status"] == "OPEN"
    assert tc054_entries[0]["review_status"] == "AWAITING_INDEPENDENT_REVIEW"

