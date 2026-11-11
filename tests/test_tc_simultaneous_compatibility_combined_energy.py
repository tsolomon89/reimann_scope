"""Regression and mathematical verification suite for TASK-TC-058:
Simultaneous Arithmetic Compatibility and Combined Scale Energy.

Verifies:
1. Narrow TC-057R repairs (§1): (U=5, T=25) vs T=35 rough squarefree composite witness
   ("when an admissible composite exists") and "sufficient condition" wording for Theorem 26.
2. Reconstructed 5-category dependency table & known context (§2): Agarwal-Garg-Maji (k=3, u=X^2)
   Riesz-Gaussian bridge and K-independence of normalized trivial-zero slopes across algebraic
   and negative grades.
3. Concrete combined-energy target (§3): direct 256-bit Arb quadrature of <P_Y, R_Y>_Y and
   independent prime-power fiber evaluation (strictly separated from subtraction consistency
   identities), plus relaxed theta_eta in [0, 1) conditional absorption without outer factor 2.
4. Compensated Selberg reconstruction (§4): finite square projection across T >= 0 (including
   T = 0, 1), uniform C_sq bound for X >= 1, dyadic parity divisor identity, exact discrete
   summation by parts keeping floor(T/d) jumps, post-Abel c_lambda collapse retaining integer
   W_2(d) - c_lambda*d, jump-count telescope, unconditional O((log Y)^{-2}) jump decay, and
   exact first-shift elimination P_Y - R_Y = D_{2,Y}.
5. Growing order M(Y) = ceil(2*log Y) & joint M(Y)-layer energy (§5): explicit Robbins-Stirling
   bound across all 3 parts of A_m on Y >= e^9 (< 38) + 17-interval compact [2, e^9] derivative
   sign bound (< 2068), generic in |a(n)| <= 1, plus joint M(Y)-layer polynomial filter
   0 < P_M(s) <= 4 on [1/4, 3/2], O(Y/(log Y)^2) joint diagonal bound, Minkowski layer-sum cost,
   and growing-control off-diagonal concentration.
6. TC compatibility discriminators (§6): pre-stated lemma schemas, window-base test [Y, b*Y]
   for b in {2, e, tau} (keeping tau in circle/Fourier/Stirling), arithmetic controls
   (lambda, a_2, a_{3,5,7}, 1), and honest classification as TC-inspired analytic number theory.
7. Formal Lean 4 Theorems 27-30, zero \\pi macros, generator-backed displayed enclosures, and
   negative tampering controls.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re

from flint import arb, ctx as flint_ctx
import pytest

from tc.canonical_theta_correlation_bound import REPO_ROOT, verify_all_serialized_arb_in_tree
from tc.coupled_scale_energy_bootstrap import rough_squarefree_divisors_band
from tc.simultaneous_compatibility_combined_energy import (
    EXPECTED_TC058_THEOREMS,
    SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH,
    TASK_TC_058_ID,
    TC_057R_IMPLEMENTATION_COMMIT,
    TC_057R_REVIEWED_TIP,
    TC_058_REVIEW_DOC_PATH,
    evaluate_C_square_arb,
    evaluate_Q_square_arb,
    evaluate_c_lambda_arb,
    evaluate_direct_cross_term_PR_arb,
    evaluate_scaled_fiber_g_arb,
    exact_growing_order_M_int,
    positive_divisor_count_int,
    verify_section_1_and_2_narrow_repairs_and_dependency_table,
    verify_section_3_combined_target_and_direct_cross_term,
    verify_section_4_compensated_selberg_and_shift_elimination,
    verify_section_5_growing_order_and_joint_gram,
    verify_section_6_tc_compatibility_discriminators,
    verify_tc058_lean_theorems_live,
    verify_tc058_review_displayed_enclosures,
)


@pytest.fixture(scope="module")
def tc058_artifact() -> dict:
    assert SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH.exists(), (
        f"Missing {SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH}"
    )
    return json.loads(
        SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH.read_text(encoding="utf-8")
    )


def test_section_1_and_2_narrow_repairs_and_dependency_table(tc058_artifact: dict) -> None:
    """Verify §1 narrow TC-057R repairs and §2 5-category dependency audit + known context."""
    assert tc058_artifact["task_id"] == TASK_TC_058_ID
    assert tc058_artifact["tc057r_implementation_commit"] == TC_057R_IMPLEMENTATION_COMMIT
    assert tc058_artifact["tc057r_reviewed_tip"] == TC_057R_REVIEWED_TIP
    assert tc058_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc058_artifact["rh_proved"] is False

    # Direct live check of §1a: U = 5, T = 25 has NO rough squarefree composite; 35 enters at T = 35
    assert list(rough_squarefree_divisors_band(5, 25)) == [5, 7, 11, 13, 17, 19, 23]
    assert list(rough_squarefree_divisors_band(5, 34)) == [5, 7, 11, 13, 17, 19, 23, 29, 31]
    assert 35 in rough_squarefree_divisors_band(5, 35)

    # Check TC-057R source and review wording repairs
    tc057_py = (REPO_ROOT / "tc" / "coupled_scale_energy_bootstrap.py").read_text(encoding="utf-8")
    tc057_md = (
        REPO_ROOT / "docs" / "reviews" / "TC_057_COUPLED_ARITHMETIC_SCALE_ENERGY_BOOTSTRAP.md"
    ).read_text(encoding="utf-8")
    assert "when an admissible composite exists" in tc057_py
    assert "when an admissible composite exists" in tc057_md
    assert "whenever T >= U^2" not in tc057_py
    assert "whenever $T \\ge U^2$" not in tc057_md
    assert "sufficient condition" in tc057_py
    assert "sufficient condition" in tc057_md

    sec12 = verify_section_1_and_2_narrow_repairs_and_dependency_table(prec_bits=256)
    assert sec12["all_section_1_and_2_checks_pass"] is True
    assert sec12["narrow_tc057r_repairs"]["rough_band_U5_T25_composites"] == []
    assert sec12["narrow_tc057r_repairs"]["rough_band_U5_T34_composites"] == []
    assert sec12["narrow_tc057r_repairs"]["rough_band_U5_T35_composites"] == [35]
    assert sec12["agarwal_garg_maji_riesz_bridge_check"]["verified"] is True
    assert (
        sec12["normalized_trivial_zero_slope_k_independence"][
            "supplies_additional_k_dependent_moments"
        ]
        is False
    )
    assert sec12["normalized_trivial_zero_slope_k_independence"]["verified"] is True

    dep = sec12["compact_dependency_table"]
    assert set(dep.keys()) == {
        "a_actual_arithmetic_theorems",
        "b_analytic_results_proved_outside_lean",
        "c_conditional_implications",
        "d_finite_numerical_observations",
        "e_missing_tc_to_arithmetic_implication",
    }
    for cat_items in dep.values():
        assert len(cat_items) >= 1


def test_section_3_combined_target_direct_cross_term_and_relaxed_absorption(
    tc058_artifact: dict,
) -> None:
    """Verify §3 direct <P_Y, R_Y>_Y evaluation, prime-power fiber cross-check, sign changes,
    and relaxed theta_eta in [0, 1) conditional absorption.
    """
    sec3 = tc058_artifact["section_3_combined_target_and_direct_cross_term"]
    assert sec3["all_section_3_checks_pass"] is True
    assert sec3["direct_cross_term_positive_scales"] == [8, 16, 32, 128]
    assert sec3["direct_cross_term_negative_scales"] == [64]
    assert sec3["S_comb_positive_scales"] == [16, 64]
    assert sec3["S_comb_negative_scales"] == [8, 32, 128]
    assert "identity, NOT an arithmetic cancellation theorem" in sec3["identity_vs_estimate_note"]

    # Live direct quadrature check at Y = 8 and Y = 64
    c8 = evaluate_direct_cross_term_PR_arb(8, mode="liouville", prec_bits=256)
    c64 = evaluate_direct_cross_term_PR_arb(64, mode="liouville", prec_bits=256)
    assert bool(c8 > arb(0))
    assert bool(c64 < arb(0))

    for f_row in sec3["independent_prime_power_fiber_cross_checks"]:
        assert f_row["verified"] is True

    abs_rows = sec3["relaxed_conditional_absorption_schedule_rows"]
    assert any(
        r["admissible_in_tc058_un_young_transfer"] is True
        and r["admissible_in_tc057r_young_transfer"] is False
        for r in abs_rows
    )


def test_section_4_compensated_selberg_summation_by_parts_and_shift_elimination(
    tc058_artifact: dict,
) -> None:
    """Verify §4 square projection (including T=0,1), uniform C_sq bound, dyadic divisor identity,
    summation by parts keeping floor(T/d) jumps, and P_Y - R_Y = D_{2,Y}.
    """
    sec4 = tc058_artifact["section_4_compensated_selberg_and_shift_elimination"]
    assert sec4["all_section_4_checks_pass"] is True

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        c_lam = evaluate_c_lambda_arb(prec_bits=256)
        C_sq = evaluate_C_square_arb(prec_bits=256)
        assert bool(c_lam < arb("-3.43")) and bool(c_lam > arb("-3.44"))
        assert bool(C_sq > arb("1.046")) and bool(C_sq < arb("1.047"))

        # Boundary T = 0 and T = 1 checks for sum_{d=1}^T g_d(X) = Q_{square,T}(X)
        assert bool(evaluate_Q_square_arb(arb(5), 0, prec_bits=256) == arb(0))
        q_sq_1 = evaluate_Q_square_arb(arb(5), 1, prec_bits=256)
        g1_1 = evaluate_scaled_fiber_g_arb(arb(5), 1, 1, prec_bits=256)
        assert bool(arb(0) in (q_sq_1 - g1_1))
        assert bool(C_sq - evaluate_Q_square_arb(arb(1), 500, prec_bits=256) > arb(0))
    finally:
        flint_ctx.prec = saved

    assert positive_divisor_count_int(1) == 1
    assert positive_divisor_count_int(15) == 4
    assert positive_divisor_count_int(36) == 9
    assert (
        sec4["dyadic_parity_control_divisor_identity"][
            "asymptotic_energy_inferred_from_divisor_identity"
        ]
        is False
    )
    assert sec4["dyadic_parity_control_divisor_identity"]["verified"] is True

    rows = sec4["summation_by_parts_and_shift_elimination_rows"]
    assert [r["Y"] for r in rows] == [8, 16, 32, 64]
    for r in rows:
        assert r["verified"] is True
        assert r["jump_count_sum_d_delta_L"] == sum(
            r["T_Y"] // d for d in range(1, r["T_Y"] + 1)
        ) - r["T_Y"]
        assert r["max_jump_product_index"] >= r["T_Y"] + 1
        assert float(r["M_sq_bound_margin"]["lower_dec"]) > 0.0


def test_section_5_growing_order_remainder_and_joint_gram(tc058_artifact: dict) -> None:
    """Verify §5 uniform remainder bound (all 3 parts of A_m + compact [2, e^9]) and joint Gram."""
    assert exact_growing_order_M_int(2) == 2
    assert exact_growing_order_M_int(8) == 5
    assert exact_growing_order_M_int(64) == 9
    assert exact_growing_order_M_int(Fraction(9, 4)) == 2

    sec5 = tc058_artifact["section_5_growing_order_and_joint_gram"]
    assert sec5["all_section_5_checks_pass"] is True
    assert sec5["generic_in_bounded_controls"] is True
    assert sec5["asymptotic_e9_constants"]["stirling_verified_m_1_to_40"] is True
    assert float(sec5["asymptotic_e9_constants"]["C_rem_ge_e9"]["upper_dec"]) < 38.0

    comp = sec5["compact_2_to_e9_partition"]
    assert comp["subinterval_count"] == 17
    assert comp["C_rem_global_proven"] == 2068
    assert float(comp["C_rem_compact_max"]["upper_dec"]) < 2068.0

    for s_row in sec5["sampled_terminal_remainder_rows"]:
        assert s_row["verified"] is True

    gram_rows = sec5["joint_M_layer_gram_rows"]
    assert len(gram_rows) == 4
    for gr in gram_rows:
        assert float(gr["modes"]["liouville"]["minkowski_over_joint_ratio"]["lower_dec"]) > 1.06
    y64_modes = next(r["modes"] for r in gram_rows if r["Y"] == 64)
    assert float(y64_modes["liouville"]["minkowski_over_joint_ratio"]["lower_dec"]) > 1.11
    for ctrl in ("a2", "a_3_5_7", "unsigned_1"):
        off_val = float(y64_modes[ctrl]["joint_M_prime_power_off_diagonal"]["lower_dec"])
        tot_val = float(y64_modes[ctrl]["joint_M_layer_norm_sq"]["upper_dec"])
        assert off_val / tot_val > 0.84


def test_section_6_tc_discriminators_and_honest_classification(tc058_artifact: dict) -> None:
    """Verify §6 pre-stated schemas, [Y, b*Y] window-base test, and control discriminators."""
    sec6 = tc058_artifact["section_6_tc_compatibility_discriminators"]
    assert sec6["all_section_6_checks_pass"] is True

    schemas = sec6["prestated_compatibility_lemma_schemas"]
    assert len(schemas) == 5
    required_schema_keys = {
        "lemma_id",
        "title",
        "objects",
        "quantifiers",
        "hypotheses",
        "input_source",
        "conclusion",
        "status",
        "tc_discriminator_result",
    }
    for s in schemas:
        assert required_schema_keys.issubset(s.keys())

    wb = sec6["window_base_discriminator"]
    assert wb["bases_tested"] == ["2", "e", "tau"]
    assert wb["tau_preserved_in_circle_fourier_stirling"] is True
    assert wb["extra_tau_specific_lattice_constraint_found"] is False
    assert wb["honest_classification"] == "TC-inspired analytic number theory"
    assert wb["verified"] is True


def test_section_7_lean_theorems_readme_sync_and_enclosure_tampering_controls(
    tc058_artifact: dict, tmp_path: Path
) -> None:
    """Verify Lean Theorems 27-30, README synchronization, zero \\pi macros, generator-backed
    displayed enclosures in TC_058_SIMULTANEOUS_COMPATIBILITY_AND_COMBINED_ENERGY.md, and
    negative tampering controls.
    """
    lean_src = (REPO_ROOT / "formal" / "RiemannScope" / "LiouvilleSquareDilation.lean").read_text(
        encoding="utf-8"
    )
    readme_src = (REPO_ROOT / "formal" / "RiemannScope" / "README.md").read_text(encoding="utf-8")

    expected_new_defs = (
        "positiveDivisorCount",
        "squareVonMangoldtB",
        "liouvilleVonMangoldt",
        "selbergLiouvilleWeight2",
        "scaledLiouvilleFiberG",
        "finiteQSquare",
        "selbergCumulativeW2",
        "selbergCenteredRemainderInt",
        "scaledFiberSmoothStep",
        "scaledFiberCutoffJump",
        "normalizedPrimePowerTermP",
        "normalizedFirstShiftTermR",
        "compensatedSelbergResidualD2",
        "pointwisePrimePowerDiagNorm",
        "pointwisePrimePowerOffDiagNorm",
        "pointwiseCombinedResidualS",
        "growingLogOrderM",
        "growingLogFilterPoly",
        "jointLayerKernelFilter",
        "jointPrimePowerFiber",
    )
    for dname in expected_new_defs:
        assert re.search(rf"^(?:noncomputable\s+)?def\s+{dname}\b", lean_src, flags=re.MULTILINE)
        assert f"`{dname}`" in readme_src

    for thm in EXPECTED_TC058_THEOREMS:
        assert re.search(rf"^theorem\s+{thm}\b", lean_src, flags=re.MULTILINE)
        assert f"`{thm}`" in readme_src

    lean_live = verify_tc058_lean_theorems_live()
    assert lean_live["all_tc058_lean_checks_pass"] is True
    assert lean_live["sorry_count"] == 0
    assert lean_live["custom_axiom_count"] == 0
    expected_std_axioms = {"propext", "Classical.choice", "Quot.sound"}
    for thm in EXPECTED_TC058_THEOREMS:
        assert set(lean_live["per_theorem"][thm]["parsed_axioms"]) == expected_std_axioms
        assert (
            set(
                tc058_artifact["section_7_lean_formalization_audit"]["per_theorem"][thm][
                    "parsed_axioms"
                ]
            )
            == expected_std_axioms
        )

    arb_self = tc058_artifact["serialized_arb_self_check"]
    assert arb_self["total_certified_arb_balls_checked"] >= 380
    assert arb_self["live_original_count_matches_enumerated_total"] is True
    assert arb_self["all_enclose_original_256bit_arb_ball"] is True
    assert arb_self["failed_paths"] == []

    assert TC_058_REVIEW_DOC_PATH.exists()
    rev_check = verify_tc058_review_displayed_enclosures(tc058_artifact, TC_058_REVIEW_DOC_PATH)
    assert rev_check["pi_macro_count"] == 0
    assert rev_check["untagged_count"] == 0
    assert rev_check["failed_count"] == 0
    assert rev_check["total_displayed_intervals_found"] >= 15
    assert rev_check["all_displayed_intervals_contain_generated_enclosures"] is True

    orig_text = TC_058_REVIEW_DOC_PATH.read_text(encoding="utf-8")

    # Tamper 1: inject forbidden \pi macro
    p_pi = tmp_path / "tamper_pi.md"
    p_pi.write_text(orig_text + "\nForbidden circle constant $\\pi$.\n", encoding="utf-8")
    res_pi = verify_tc058_review_displayed_enclosures(tc058_artifact, p_pi)
    assert res_pi["pi_macro_count"] >= 1
    assert res_pi["all_displayed_intervals_contain_generated_enclosures"] is False

    # Tamper 2: inject untagged interval
    p_untag = tmp_path / "tamper_untag.md"
    p_untag.write_text(orig_text + "\nUntagged `[1.0464 +/- 1.0e-3]`.\n", encoding="utf-8")
    res_untag = verify_tc058_review_displayed_enclosures(tc058_artifact, p_untag)
    assert res_untag["untagged_count"] >= 1
    assert res_untag["all_displayed_intervals_contain_generated_enclosures"] is False

    # Tamper 3: inject wrong midpoint on C_sq
    p_bad = tmp_path / "tamper_bad_mid.md"
    p_bad.write_text(
        orig_text
        + '\nWrong `[2.0464331771475893 +/- 1.0e-12]` <!-- tc-enclosure: observable="C_sq" params="" json_path="section_4_compensated_selberg_and_shift_elimination.C_sq" -->\n',
        encoding="utf-8",
    )
    res_bad = verify_tc058_review_displayed_enclosures(tc058_artifact, p_bad)
    assert res_bad["failed_count"] >= 1
    assert res_bad["all_displayed_intervals_contain_generated_enclosures"] is False

    # Tamper 4: inject overly wide interval on C_sq
    p_wide = tmp_path / "tamper_wide.md"
    p_wide.write_text(
        orig_text
        + '\nWide `[1.0464331771475893 +/- 0.5]` <!-- tc-enclosure: observable="C_sq" params="" json_path="section_4_compensated_selberg_and_shift_elimination.C_sq" -->\n',
        encoding="utf-8",
    )
    res_wide = verify_tc058_review_displayed_enclosures(tc058_artifact, p_wide)
    assert res_wide["failed_count"] >= 1
    assert res_wide["all_displayed_intervals_contain_generated_enclosures"] is False
