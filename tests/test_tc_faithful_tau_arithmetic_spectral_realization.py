"""
Unit and regression tests for TASK-TC-050 and TASK-TC-050R:
Construct the Faithful tau-Arithmetic Spectral Realization, Prove Adjoint Compatibility,
and Verify the Restored TC-049/TC-049R Head-Band-Tail Decomposition and Outward Certification.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import re

from flint import acb, arb, ctx as flint_ctx
import pytest

from tc.canonical_theta_correlation_bound import (
    REPO_ROOT,
    evaluate_h0_arb,
    execute_task_tc050_faithful_spectral_realization_audit,
    verify_all_serialized_arb_in_tree,
    verify_canonical_theta_correlation_lean_module,
)
from tc.faithful_tau_arithmetic_spectral_realization import (
    DEFAULT_TC050_ARTIFACT_PATH,
    FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION_STATUS,
    REVIEWED_BASELINE_TC_050,
    STARTING_HEAD_TC_050,
    TASK_TC_050_ID,
    certified_head_cutoff_H_X_arb,
    certify_abs_le_bound_arb,
    evaluate_connes_consani_delta_arb,
    p_adic_fractional_part_rational,
    verify_adjoint_compatibility_and_hyperbolic_pair_obstruction,
    verify_canonical_hilbert_schmidt_orbit_decomposition,
    verify_primary_literature_constructions_and_support_extension,
    verify_tau_joint_arithmetic_fourier_roles_and_transforms,
)
from tc.prime_euler_moebius_recovery import certified_coupled_cutoff_M_X_arb


@pytest.fixture(scope="module")
def tc050_artifact() -> dict:
    """Load the generated TASK-TC-050 artifact JSON."""
    assert DEFAULT_TC050_ARTIFACT_PATH.exists(), (
        f"Missing artifact {DEFAULT_TC050_ARTIFACT_PATH}; run "
        "`python -m tc.faithful_tau_arithmetic_spectral_realization`."
    )
    return json.loads(DEFAULT_TC050_ARTIFACT_PATH.read_text(encoding="utf-8"))


def test_01_tc050_metadata_and_status_integrity(tc050_artifact: dict) -> None:
    """Verify TASK-TC-050 task metadata, baseline preservation, and open SUBGATE-TC-043A status."""
    assert tc050_artifact["task_id"] == TASK_TC_050_ID == "TASK-TC-050"
    assert tc050_artifact["starting_head"] == STARTING_HEAD_TC_050
    assert tc050_artifact["reviewed_baseline"] == REVIEWED_BASELINE_TC_050
    assert (
        tc050_artifact["status"]
        == FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION_STATUS
    )
    assert tc050_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc050_artifact["rh_proved"] is False


def test_02_tate_rational_diagonal_and_prime_transform_intertwining(
    tc050_artifact: dict,
) -> None:
    """Verify Tate rational-diagonal character rigidity, semidirect intertwining between
    arithmetic shifts p * tau^K and analytic powers p^{tau^{-K}}, and CCM generator identity."""
    sec1 = tc050_artifact["section_1_tau_roles_and_prime_transformations"]
    roles = sec1["tau_coupled_roles_classification"]
    r1 = roles["role_1_tate_adelic_character_normalization"]
    assert r1["all_sample_rationals_verified"] is True
    assert len(r1["sample_rational_verifications"]) == 5
    for row in r1["sample_rational_verifications"]:
        assert row["p_integrality_verified"] is True
        assert row["adelic_character_product_encloses_1_at_c_inf_eq_tau"] is True

    # Independent check of p-adic fractional part decomposition on q = 37/60:
    q = Fraction(37, 60)
    parts = {p: p_adic_fractional_part_rational(q, p) for p in (2, 3, 5)}
    assert (q - sum(parts.values())).denominator == 1
    for p, part in parts.items():
        assert (q - part).denominator % p != 0

    # Verify arithmetic p * tau^K vs analytic p^{tau^{-K}} distinction and intertwining:
    trans = sec1["arithmetic_vs_analytic_prime_transformations"]
    assert trans["symbolic_intertwining_diff_1_zero"] is True
    assert trans["symbolic_intertwining_diff_2_zero"] is True
    assert len(trans["certified_station_comparisons"]) == 12
    assert all(
        row["certified_strictly_distinct"]
        for row in trans["certified_station_comparisons"]
    )

    # Verify Connes-Consani-Moscovici (arXiv:2511.22755 Lemma 7.1) generator identity f_tau = 8 h_CCM:
    ccm = sec1["connes_consani_moscovici_generator_identity"]
    assert ccm["symbolic_f_tau_minus_8_h_CCM_zero"] is True
    assert ccm["symbolic_h_CCM_hermite_decomposition_verified"] is True
    assert ccm["mellin_vanishing_at_s_0_and_1_verified"] is True


def test_03_adjoint_compatibility_hyperbolic_null_cone_and_jordan_socle(
    tc050_artifact: dict,
) -> None:
    """Verify star-involution compatibility chi_rho(V_K^*) = conj(chi_rho(V_K)) <-> Re(rho) = 1/2,
    off-critical hyperbolic pair exchange, and Jordan socle eigenvector for m_rho >= 1."""
    sec2 = tc050_artifact[
        "section_2_adjoint_compatibility_and_hyperbolic_null_cone"
    ]
    compat = sec2["character_compatibility_equivalence"]
    assert compat["multiplication_preserved_for_all_rho"] is True
    assert compat["star_ratio_identity_verified"] is True
    assert compat["functional_equation_partner_exchange_verified"] is True

    rows = compat["certified_mode_evaluations"]
    assert len(rows) == 16
    for row in rows:
        assert row["functional_equation_partner_exchange_encloses_zero"] is True
        if row["delta_label"] == "0":
            assert row["star_compatible_encloses_zero"] is True
            assert row["star_defect_strictly_positive_off_critical"] is False
        else:
            assert row["star_compatible_encloses_zero"] is False
            assert row["star_defect_strictly_positive_off_critical"] is True

    socle = sec2["multiplicity_and_jordan_socle_audit"]
    assert socle["no_simplicity_assumption_required"] is True
    assert len(socle["jordan_socle_verifications"]) == 3
    assert all(
        item["socle_vector_is_pure_eigenvector"]
        for item in socle["jordan_socle_verifications"]
    )


def test_04_primary_literature_constructions_and_connes_consani_delta(
    tc050_artifact: dict,
) -> None:
    """Verify Meyer convolution-trace invariance, Connes-Consani delta(rho) formula (arXiv:2006.13771
    Prop. 2.2 & eq. 2.18), separated-grade prime thresholds, and CCM Section 8 open steps."""
    sec3 = tc050_artifact["section_3_primary_literature_constructions_audit"]
    cc = sec3["connes_consani_2006_13771_compressed_scaling_trace"]

    # Check delta(1) = Si(4*pi)/(2*pi) + 2 = 2.2374848349418275...
    assert math.isclose(
        cc["delta_at_1_certified"]["mid_float"],
        2.2374848349418275,
        rel_tol=1e-14,
    )
    delta_grid = cc["certified_delta_grid_on_half_to_two"]
    assert len(delta_grid) == 7
    assert all(
        row["inversion_symmetry_diff_encloses_zero"] for row in delta_grid
    )
    # Check inversion symmetry values delta(1/2) == delta(2) and delta(2/3) == delta(3/2):
    by_rho = {row["rho_label"]: row for row in delta_grid}
    assert math.isclose(
        by_rho["1/2"]["delta_rho_certified"]["mid_float"],
        by_rho["2"]["delta_rho_certified"]["mid_float"],
        rel_tol=1e-15,
    )
    assert math.isclose(
        by_rho["2/3"]["delta_rho_certified"]["mid_float"],
        by_rho["3/2"]["delta_rho_certified"]["mid_float"],
        rel_tol=1e-15,
    )

    # Check separated-grade prime thresholds log(p)/log(tau):
    ext = cc["separated_grade_support_extension"]
    assert math.isclose(
        ext["threshold_K_for_prime_2_certified"]["mid_float"],
        math.log(2.0) / math.log(2.0 * math.pi),
        rel_tol=1e-14,
    )
    assert math.isclose(
        ext["threshold_K_for_prime_3_certified"]["mid_float"],
        math.log(3.0) / math.log(2.0 * math.pi),
        rel_tol=1e-14,
    )
    assert math.isclose(
        ext["threshold_K_for_prime_5_certified"]["mid_float"],
        math.log(5.0) / math.log(2.0 * math.pi),
        rel_tol=1e-14,
    )

    # Check Connes-Consani-Moscovici Section 8 two missing steps:
    ccm8 = sec3["connes_consani_moscovici_2511_22755_zeta_spectral_triples"]
    assert len(ccm8["section_8_two_missing_steps"]) == 2


def test_05_canonical_hilbert_schmidt_orbit_decomposition_and_symmetry(
    tc050_artifact: dict,
) -> None:
    """Verify C_tau(K) = P_tau(K) + E_tau(K) across all 13 positive and negative rational and
    irrational algebraic grades K in {0, +/-1/4, +/-1/2, +/-1, +/-sqrt(2), +/-3/2, +/-2}."""
    sec4 = tc050_artifact[
        "section_4_canonical_hilbert_schmidt_orbit_decomposition"
    ]
    pos = sec4["positive_hilbert_space_and_unitary_orbit"]
    assert pos["all_sample_grades_satisfy_HS_cauchy_schwarz"] is True

    p0_mid = pos["norm_B_0_HS_sq_eq_P_tau_0_certified"]["mid_float"]
    pB0_mid = pos["norm_A_tau_B_psi_tau_sq_certified"]["mid_float"]
    r0_mid = pos["four_norm_R0_psi_tau_sq_certified"]["mid_float"]
    assert math.isclose(p0_mid, 2.558258007415831, rel_tol=1e-14)
    assert math.isclose(pB0_mid, 0.5947678334606322, rel_tol=1e-14)
    assert math.isclose(r0_mid, 1.9634901739551989, rel_tol=1e-14)
    assert math.isclose(p0_mid, pB0_mid + r0_mid, rel_tol=1e-15)

    decomp = sec4["exact_decomposition_and_controlled_remainder_bounds"]
    assert decomp["all_orbit_reconstructions_enclose_zero"] is True
    table = decomp["certified_grade_orbit_table"]
    assert len(table) == 13
    by_k = {row["K_label"]: row for row in table}
    for k_pos, k_neg in (
        ("1/4", "-1/4"),
        ("1/2", "-1/2"),
        ("1", "-1"),
        ("sqrt(2)", "-sqrt(2)"),
        ("3/2", "-3/2"),
        ("2", "-2"),
    ):
        assert k_pos in by_k and k_neg in by_k
        assert by_k[k_pos]["abs_P_tau_K_le_P_tau_0"] is True
        assert by_k[k_neg]["abs_P_tau_K_le_P_tau_0"] is True
        assert by_k[k_pos]["reconstruction_encloses_zero"] is True
        assert by_k[k_neg]["reconstruction_encloses_zero"] is True
        assert math.isclose(
            by_k[k_pos]["P_tau_K_HS_orbit_certified"]["mid_float"],
            by_k[k_neg]["P_tau_K_HS_orbit_certified"]["mid_float"],
            rel_tol=1e-14,
        )
        assert math.isclose(
            by_k[k_pos]["C_tau_K_certified"]["mid_float"],
            by_k[k_neg]["C_tau_K_certified"]["mid_float"],
            rel_tol=1e-12,
        )


def test_06_lean_formalization_and_arb_roundtrip_verification(
    tc050_artifact: dict,
) -> None:
    """Verify Lean 4 module theorems 51-53 (0 sorry, 0 admit) and full-tree 256-bit Arb round-trip."""
    lean_live = verify_canonical_theta_correlation_lean_module()
    assert lean_live["exists"] is True
    assert lean_live["contains_sorry"] is False
    assert lean_live["contains_admit"] is False
    assert lean_live["matches_exact"] is True
    for thm_name in (
        "tau_grade_star_involution_and_hyperbolic_pair_obstruction",
        "tate_rational_diagonal_character_rigidity_and_convolution_isometry",
        "canonical_hilbert_schmidt_orbit_decomposition_and_resonant_band_equivalence",
    ):
        assert thm_name in lean_live["actual_theorems"]

    sec6 = tc050_artifact["section_6_certified_arb_roundtrip_verification"]
    assert sec6["total_certified_arb_balls_checked"] == 489
    assert sec6["compared_against_live_original_arb_count"] == 489
    assert sec6["live_original_count_matches_enumerated_total"] is True
    assert sec6["all_enclose_original_256bit_arb_ball"] is True
    assert sec6["failed_paths"] == []

    # Re-enumerate the deserialized JSON tree and confirm exact ball count match:
    rt_recheck = verify_all_serialized_arb_in_tree(
        tc050_artifact, path_prefix="task_tc050"
    )
    assert rt_recheck["total_certified_arb_balls_checked"] == 489
    assert (
        sec6["compared_against_live_original_arb_count"]
        == rt_recheck["total_certified_arb_balls_checked"]
    )


def test_07_tc050r_restored_cutoffs_and_certified_boundary_hygiene(
    tc050_artifact: dict,
) -> None:
    """Verify H(X) = floor(X^{5/6}) and M(X) = ceil(max(2, X^{5/4})) cutoffs,
    empty head sums for H(X) < 2, exact integer power boundaries, and rejection of
    balls straddling an integer power boundary."""
    saved_prec = flint_ctx.prec
    flint_ctx.prec = 256
    try:
        # Exact integer power test points:
        # X = 1 -> H(1) = 1, M(1) = 2
        assert certified_head_cutoff_H_X_arb(arb(1)) == 1
        assert certified_coupled_cutoff_M_X_arb(arb(1)) == 2
        # X = 16 -> 16^{5/6} = 2^{10/3} = 10.079... -> H(16) = 10; 16^{5/4} = 32 -> M(16) = 32
        assert certified_head_cutoff_H_X_arb(arb(16)) == 10
        assert certified_coupled_cutoff_M_X_arb(arb(16)) == 32
        # X = 64 -> 64^{5/6} = 32 -> H(64) = 32; 64^{5/4} = 181.019... -> M(64) = 182
        assert certified_head_cutoff_H_X_arb(arb(64)) == 32
        assert certified_coupled_cutoff_M_X_arb(arb(64)) == 182

        # Reject non-exact ball straddling X = 2^{6/5} where H(X) jumps from 1 to 2:
        x_boundary = arb(2) ** (arb(6) / arb(5))
        x_straddle_h = arb(x_boundary.mid(), arb("1e-10"))
        with pytest.raises(ValueError, match="Unable to certify unique integer floor"):
            certified_head_cutoff_H_X_arb(x_straddle_h)

        # Outward ceiling behavior of M(X) on ball straddling X = 16 (where 16^{5/4} = 32):
        x_straddle_m = arb(arb(16).mid(), arb("1e-10"))
        assert certified_coupled_cutoff_M_X_arb(x_straddle_m) == 33
        with pytest.raises(ValueError, match="X must be strictly positive"):
            certified_coupled_cutoff_M_X_arb(arb(0))
    finally:
        flint_ctx.prec = saved_prec

    # Check artifact grade table cutoffs and empty head sum handling on K in {0, +/-1/4}:
    decomp = tc050_artifact[
        "section_4_canonical_hilbert_schmidt_orbit_decomposition"
    ]["exact_decomposition_and_controlled_remainder_bounds"]
    expected_cutoffs = {
        "0": (1, 2, True),
        "1/4": (1, 2, True),
        "-1/4": (1, 2, True),
        "1/2": (2, 4, False),
        "-1/2": (2, 4, False),
        "1": (4, 10, False),
        "-1": (4, 10, False),
        "sqrt(2)": (8, 26, False),
        "-sqrt(2)": (8, 26, False),
        "3/2": (9, 32, False),
        "-3/2": (9, 32, False),
        "2": (21, 99, False),
        "-2": (21, 99, False),
    }
    for row in decomp["certified_grade_orbit_table"]:
        k_lbl = row["K_label"]
        exp_h, exp_m, exp_empty = expected_cutoffs[k_lbl]
        assert row["H_XK_eq_floor_XK_5_6"] == exp_h
        assert row["M_XK_eq_ceil_max_2_XK_5_4"] == exp_m
        assert row["head_sum_is_empty"] is exp_empty
        if exp_empty:
            assert row["head_divisor_R_mu_head_XK_certified"]["mid_float"] == 0.0
            assert row["head_divisor_R_mu_head_XK_certified"]["arb_ball_str"] == "0"


def test_08_tc050r_outward_rounded_inequality_certification_and_provenance(
    tc050_artifact: dict,
) -> None:
    """Verify outward-rounded inequality certification (rejecting weak overlap-only checks),
    direct band sum vs total Moebius tail enclosure, and 5-component bound provenance."""
    saved_prec = flint_ctx.prec
    flint_ctx.prec = 256
    try:
        # 1. Overlap-only pair where abs(val).lower() <= bound.upper() holds,
        #    but abs(val).upper() > bound.lower() must NOT be certified:
        val_overlap = arb(arb("1.0001"), arb("0.001"))  # [0.9991, 1.0011]
        bnd_overlap = arb(arb("1.0000"), arb("0.001"))  # [0.9990, 1.0010]
        res_overlap = certify_abs_le_bound_arb(val_overlap, bnd_overlap)
        assert res_overlap["weak_overlap_lower_le_upper"] is True
        assert res_overlap["outward_upper_le_lower"] is False
        assert res_overlap["certified"] is False
        assert res_overlap["certification_mode"] == "OUTWARD_UPPER_LE_LOWER"

        # 2. Strict outward-rounded enclosure abs(val).upper() <= bound.lower() must pass:
        val_strict = arb(arb("0.95"), arb("0.001"))
        bnd_strict = arb(arb("1.00"), arb("0.001"))
        res_strict = certify_abs_le_bound_arb(val_strict, bnd_strict)
        assert res_strict["outward_upper_le_lower"] is True
        assert res_strict["certified"] is True
        assert res_strict["certification_mode"] == "OUTWARD_UPPER_LE_LOWER"

        # 3. Exact self-equality on a positive ball at K = 0:
        ball_self = arb(arb("2.558258"), arb("1e-25"))
        res_self = certify_abs_le_bound_arb(
            -ball_self, ball_self, exact_self_equality=True
        )
        assert res_self["certified"] is True
        assert (
            res_self["certification_mode"]
            == "EXACT_ALGEBRAIC_SELF_EQUALITY_POSITIVE_BALL"
        )
        assert res_self["margin_bound_minus_abs_certified"]["arb_ball_str"] == "0"
    finally:
        flint_ctx.prec = saved_prec

    decomp = tc050_artifact[
        "section_4_canonical_hilbert_schmidt_orbit_decomposition"
    ]["exact_decomposition_and_controlled_remainder_bounds"]
    assert decomp["all_component_bounds_verified"] is True
    assert decomp["all_independent_tail_bounds_verified"] is True

    # Verify all 5 component provenance records exist and sum to B_ctrl < 17.987140:
    prov = decomp["component_bound_provenance_records"]
    expected_keys = (
        "component_1_pole_plus_transfer_h0",
        "component_2_reflected_small_scale_prime_W_inv_XK",
        "component_3_divisor_aggregated_W_log_XK",
        "component_4_head_divisor_R_mu_head_XK",
        "component_5_super_scale_tail_R_mu_tail_XK",
    )
    for key in expected_keys:
        assert key in prov
        for field in (
            "expression",
            "domain",
            "inequality_used",
            "provenance",
            "rounding_direction",
            "bound_certified",
        ):
            assert field in prov[key]

    bounds = decomp["unconditional_component_bounds_over_all_K_in_A_R"]
    b_ctrl_upper = float(
        bounds["abs_E_tau_controlled_global_bound_certified"]["upper_dec"]
    )
    b_limsup_upper = float(
        bounds["abs_E_tau_controlled_limsup_bound_certified"]["upper_dec"]
    )
    assert math.isclose(b_ctrl_upper, 17.987137364158494, rel_tol=1e-11)
    assert b_ctrl_upper < 17.987140
    assert math.isclose(b_limsup_upper, 11.502477068554061, rel_tol=1e-11)
    assert b_limsup_upper < 11.502478

    for row in decomp["certified_grade_orbit_table"]:
        assert (
            row["reconstruction_verification_type"]
            == "ALGEBRAIC_CONSISTENCY_CHECK"
        )
        tail_ver = row["independent_tail_enclosure_verification"]
        assert (
            tail_ver["verification_type"]
            == "INDEPENDENT_HEAD_BAND_VS_TOTAL_MOEBIUS_TAIL_ENCLOSURE_CHECK"
        )
        assert tail_ver["tail_from_diff_le_analytic_bound"]["certified"] is True
        assert tail_ver["tail_direct_le_analytic_bound"]["certified"] is True
        assert tail_ver["tail_diff_minus_direct_encloses_zero"] is True


def test_09_tc050r_markdown_review_table_matches_json_certificate(
    tc050_artifact: dict,
) -> None:
    """Verify that the 13-row grade table in docs/reviews/TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md
    matches the certified values in data/tc_faithful_tau_arithmetic_spectral_realization.json."""
    doc_path = REPO_ROOT / "docs" / "reviews" / "TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md"
    doc_text = doc_path.read_text(encoding="utf-8")

    decomp = tc050_artifact[
        "section_4_canonical_hilbert_schmidt_orbit_decomposition"
    ]["exact_decomposition_and_controlled_remainder_bounds"]
    by_k = {row["K_label"]: row for row in decomp["certified_grade_orbit_table"]}

    label_map = {
        "$-2$": "-2",
        "$-3/2$": "-3/2",
        "$-\\sqrt{2}$": "-sqrt(2)",
        "$-1$": "-1",
        "$-1/2$": "-1/2",
        "$-1/4$": "-1/4",
        "$0$": "0",
        "$+1/4$": "1/4",
        "$+1/2$": "1/2",
        "$+1$": "1",
        "$+\\sqrt{2}$": "sqrt(2)",
        "$+3/2$": "3/2",
        "$+2$": "2",
    }

    matched_rows = 0
    for line in doc_text.splitlines():
        line_s = line.strip()
        if not line_s.startswith("|"):
            continue
        cells = [c.strip() for c in line_s.strip("|").split("|")]
        if len(cells) != 9 or cells[0] not in label_map:
            continue
        k_lbl = label_map[cells[0]]
        row = by_k[k_lbl]
        matched_rows += 1

        xk_doc = float(cells[1].strip("$"))
        m_hm = re.fullmatch(r"\$\((\d+),\s*(\d+)\)\$", cells[2])
        assert m_hm is not None, f"Unexpected (H, M) cell format: {cells[2]}"
        h_doc, m_doc = int(m_hm.group(1)), int(m_hm.group(2))
        pk_doc = float(cells[3].strip("$"))
        head_doc = float(cells[4].strip("$"))
        band_doc = float(cells[5].strip("$"))
        ectrl_doc = float(cells[6].strip("$"))
        etot_doc = float(cells[7].strip("$"))
        ck_doc = float(cells[8].strip("$"))

        assert h_doc == row["H_XK_eq_floor_XK_5_6"]
        assert m_doc == row["M_XK_eq_ceil_max_2_XK_5_4"]
        assert math.isclose(
            xk_doc, row["X_K_eq_tau_abs_K_certified"]["mid_float"], abs_tol=1e-8
        )
        assert math.isclose(
            pk_doc, row["P_tau_K_HS_orbit_certified"]["mid_float"], abs_tol=1e-8
        )
        assert math.isclose(
            head_doc,
            row["head_divisor_R_mu_head_XK_certified"]["mid_float"],
            abs_tol=1e-8,
        )
        assert math.isclose(
            band_doc,
            row["resonant_band_R_mu_band_XK_direct_sum_certified"]["mid_float"],
            abs_tol=1e-8,
        )
        assert math.isclose(
            ectrl_doc,
            row["E_tau_controlled_K_certified"]["mid_float"],
            abs_tol=1e-8,
        )
        assert math.isclose(
            etot_doc,
            row["E_tau_K_total_remainder_certified"]["mid_float"],
            abs_tol=1e-8,
        )
        assert math.isclose(
            ck_doc, row["C_tau_K_certified"]["mid_float"], abs_tol=1e-8
        )

    assert matched_rows == 13

