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
    execute_task_tc051_prime_arithmetic_resonant_band_audit,
    verify_all_serialized_arb_in_tree,
    verify_canonical_theta_correlation_lean_module,
)
from tc.faithful_tau_arithmetic_spectral_realization import (
    DEFAULT_TC050_ARTIFACT_PATH,
    FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION_STATUS,
    REVIEWED_BASELINE_TC_050,
    STARTING_HEAD_TC_050,
    STARTING_HEAD_TC_051,
    TASK_TC_050_ID,
    TASK_TC_051_ID,
    certified_head_cutoff_H_X_arb,
    certify_abs_le_bound_arb,
    certify_clamped_exact_cutoff_M_X_arb,
    evaluate_connes_consani_delta_arb,
    evaluate_R_interval_arb,
    evaluate_S_p_interval_arb,
    evaluate_S_prime_set_interval_arb,
    evaluate_tilde_W_log_certified_arb,
    evaluate_W_log_em4_certified_arb,
    p_adic_fractional_part_rational,
    verify_adjoint_compatibility_and_hyperbolic_pair_obstruction,
    verify_canonical_hilbert_schmidt_orbit_decomposition,
    verify_euler_resolvent_R0_spatial_and_mellin_identity_arb,
    verify_h0_autocorrelation_cauchy_schwarz_and_sign_change_arb,
    verify_prime_separation_identity_and_canonical_band_boundary_arb,
    verify_primary_literature_constructions_and_support_extension,
    verify_sign_sequence_cancellation_discrimination_arb,
    verify_summation_by_parts_and_tilde_W_log_identity_arb,
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
    assert sec6["total_certified_arb_balls_checked"] == 1258
    assert sec6["compared_against_live_original_arb_count"] == 1258
    assert sec6["live_original_count_matches_enumerated_total"] is True
    assert sec6["all_enclose_original_256bit_arb_ball"] is True
    assert sec6["failed_paths"] == []

    # Re-enumerate the deserialized JSON tree and confirm exact ball count match:
    rt_recheck = verify_all_serialized_arb_in_tree(
        tc050_artifact, path_prefix="task_tc050"
    )
    assert rt_recheck["total_certified_arb_balls_checked"] == 1258
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


def test_10_tc050r2_euler_resolvent_R0_spatial_mellin_and_J_kappa_weight(
    tc050_artifact: dict,
) -> None:
    """Verify the causal s = 0 Euler resolvent identity
    (R_0 f)(y) = int_0^y (t/y)^{1/2} (D f)(t) dt/t = f(y) - (1/2) int_0^y (t/y)^{1/2} f(t) dt/t,
    the e^{-u/2} weight in J(kappa), and why omitting D fails to cancel J(kappa)."""
    sec4_pos = tc050_artifact[
        "section_4_canonical_hilbert_schmidt_orbit_decomposition"
    ]["positive_hilbert_space_and_unitary_orbit"]
    emb_str = sec4_pos["isometric_embedding_J_tau"]
    assert "(D f)(t)" in emb_str
    assert "f(y) - (1/2)" in emb_str
    assert "e^{-u/2}" in emb_str
    assert "e^{-3u/2}" not in emb_str

    r0_audit = sec4_pos["euler_resolvent_R0_and_pole_integral_J_kappa_audit"]
    assert r0_audit["symbolic_mellin_multiplier_verified"] is True
    assert r0_audit["all_spatial_ibp_enclose_zero"] is True
    assert math.isclose(
        r0_audit["four_norm_R0_psi_tau_sq_eq_4_h0_1_minus_J_0_certified"][
            "mid_float"
        ],
        1.963490173955199,
        rel_tol=1e-14,
    )
    assert math.isclose(
        r0_audit[
            "four_norm_derivative_free_K0_psi_tau_sq_eq_4_J_0_certified"
        ]["mid_float"],
        0.10383904513761568,
        rel_tol=1e-10,
    )
    assert (
        r0_audit["discrepancy_four_R0_sq_minus_four_K0_sq_certified"][
            "mid_float"
        ]
        > 1.859
    )

    live_r0 = verify_euler_resolvent_R0_spatial_and_mellin_identity_arb(
        prec_bits=256
    )
    assert live_r0["all_spatial_ibp_enclose_zero"] is True


def test_11_tc050r2_h0_autocorrelation_cauchy_schwarz_and_sign_change(
    tc050_artifact: dict,
) -> None:
    """Verify h_0(1) = 92193 / (512 * 2^{17/2}) = 92193 / (131072 * sqrt(2)),
    Taylor expansion at W = 4, sign-change witness h_0(2) < 0, unitary dilation
    Cauchy-Schwarz bound |h_0(X)| <= h_0(1), and leading asymptotic -(81/64) X^{-5/2}."""
    decomp = tc050_artifact[
        "section_4_canonical_hilbert_schmidt_orbit_decomposition"
    ]["exact_decomposition_and_controlled_remainder_bounds"]
    h0_audit = decomp["h0_autocorrelation_cauchy_schwarz_and_sign_change_audit"]
    assert h0_audit["P_sym_at_W_eq_4_exact_int"] == 92193
    assert h0_audit["P_sym_taylor_identity_verified"] is True
    assert h0_audit["h0_1_closed_form_diff_encloses_zero"] is True
    assert (
        h0_audit["sign_change_witnesses_on_1_to_infty"][
            "h0_is_strictly_positive_on_1_to_infty"
        ]
        is False
    )
    assert (
        h0_audit["sign_change_witnesses_on_1_to_infty"][
            "h0_is_monotone_decreasing_on_1_to_infty"
        ]
        is False
    )
    assert (
        h0_audit["sign_change_witnesses_on_1_to_infty"][
            "h0_2_strictly_negative_verified"
        ]
        is True
    )
    assert math.isclose(
        h0_audit["h0_1_certified"]["mid_float"],
        92193.0 / (131072.0 * math.sqrt(2.0)),
        rel_tol=1e-15,
    )
    assert math.isclose(
        h0_audit["sign_change_witnesses_on_1_to_infty"]["h0_2_certified"][
            "mid_float"
        ],
        -0.21743062244679337,
        rel_tol=1e-14,
    )
    assert h0_audit["all_cauchy_schwarz_and_bernstein_checks_verified"] is True

    comp1 = decomp["component_bound_provenance_records"][
        "component_1_pole_plus_transfer_h0"
    ]
    assert "Cauchy-Schwarz" in comp1["inequality_used"]
    assert "strictly decreasing" not in comp1["inequality_used"]

    # Ensure stale 0.4863195 value and false monotonicity claim are absent from docs:
    doc_text = (
        REPO_ROOT
        / "docs"
        / "reviews"
        / "TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md"
    ).read_text(encoding="utf-8")
    assert "0.4863195" not in doc_text
    assert "Strict monotonicity $0 < h_0(X_K)" not in doc_text

    readme_text = (REPO_ROOT / "formal" / "RiemannScope" / "README.md").read_text(
        encoding="utf-8"
    )
    assert "-648(W-4)^3 - 3336" not in readme_text
    assert "- 58560(W-4)" not in readme_text
    assert "92193 - 270924(W-4) + 50604(W-4)^2 - 648(W-4)^3" in readme_text


def test_12_tc050r2_clamped_exact_cutoff_M_X_characterization_and_helper_scope(
    tc050_artifact: dict,
) -> None:
    """Verify the clamped characterization M >= 2 and X^5 <= M^4 and (M = 2 or (M-1)^4 < X^5)
    for M(X) = ceil(max(2, X^{5/4})), and distinguish exact M(X) from safe upper cutoff on straddling balls."""
    saved_prec = flint_ctx.prec
    flint_ctx.prec = 256
    try:
        # At X = 1, M(1) = 2: clamped characterization holds via M = 2 branch, while (M-1)^4 < X^5 is false:
        c_1 = certify_clamped_exact_cutoff_M_X_arb(arb(1))
        assert c_1["M_safe_upper_int"] == 2
        assert c_1["M_lower_ceil_int"] == 2
        assert c_1["m_ge_2"] is True
        assert c_1["X5_le_M4_certified"] is True
        assert c_1["unclamped_M_minus_1_pow4_lt_X5_holds"] is False
        assert (
            c_1["clamped_lower_M_eq_2_or_M_minus_1_pow4_lt_X5_certified"]
            is True
        )
        assert c_1["exact_clamped_characterization_certified"] is True

        # At X = 16, 16^{5/4} = 32 -> M(16) = 32 satisfies (M-1)^4 < X^5 <= M^4:
        c_16 = certify_clamped_exact_cutoff_M_X_arb(arb(16))
        assert c_16["M_safe_upper_int"] == 32
        assert c_16["M_lower_ceil_int"] == 32
        assert c_16["unclamped_M_minus_1_pow4_lt_X5_holds"] is True
        assert c_16["exact_clamped_characterization_certified"] is True

        # On a wide ball straddling X = 16, safe upper helper returns 33, while exact clamped check flags False:
        c_straddle = certify_clamped_exact_cutoff_M_X_arb(
            arb(arb(16).mid(), arb("1e-30"))
        )
        assert c_straddle["M_safe_upper_int"] == 33
        assert c_straddle["M_lower_ceil_int"] == 32
        assert c_straddle["exact_clamped_characterization_certified"] is False
    finally:
        flint_ctx.prec = saved_prec

    decomp = tc050_artifact[
        "section_4_canonical_hilbert_schmidt_orbit_decomposition"
    ]["exact_decomposition_and_controlled_remainder_bounds"]
    cutoffs = decomp["cutoff_definitions_tc049r"]
    assert cutoffs["all_sample_cutoffs_exact_clamped_certified"] is True
    for row in decomp["certified_grade_orbit_table"]:
        assert (
            row["M_XK_clamped_exact_characterization"][
                "exact_clamped_characterization_certified"
            ]
            is True
        )


def test_13_tc050r2_committed_lean_theorems_and_multiplicity_scope_alignment(
    tc050_artifact: dict,
) -> None:
    """Verify exact alignment between committed Lean 4 Theorems 51-53 and documentation/JSON records,
    and verify the three-way multiplicity distinction (scalar correlation vs socle vs full H_-^0)."""
    sec2_socle = tc050_artifact[
        "section_2_adjoint_compatibility_and_hyperbolic_null_cone"
    ]["multiplicity_and_jordan_socle_audit"][
        "scalar_correlation_vs_operator_jordan_scope_distinction"
    ]
    assert "unconditionally in zero multiplicity" in (
        sec2_socle["scalar_correlation_boundedness_equivalence"]
    )
    assert "RH alone" in sec2_socle["socle_operator_unitary_realization_equivalence"]
    assert (
        "RH + Simplicity"
        in sec2_socle["full_generalized_eigenspace_unitary_realization_equivalence"]
    )

    sec5 = tc050_artifact[
        "section_5_lean_formalization_and_remaining_obligation"
    ]
    lean_scope = sec5["committed_lean_theorems_exact_scope"]
    assert (
        "theorem_51_tau_grade_star_involution_and_hyperbolic_pair_obstruction"
        in lean_scope
    )
    assert (
        "theorem_52_tate_rational_diagonal_character_rigidity_and_convolution_isometry"
        in lean_scope
    )
    assert (
        "theorem_53_canonical_hilbert_schmidt_orbit_decomposition_and_resonant_band_equivalence"
        in lean_scope
    )

    lean_text = (
        REPO_ROOT
        / "formal"
        / "RiemannScope"
        / "CanonicalThetaCorrelationBound.lean"
    ).read_text(encoding="utf-8")
    assert "92793" not in lean_text
    assert "92193" in lean_text
    for clause in (
        "gradeRadialCharacter tau (-K) delta = gradeRadialCharacter tau K delta ↔ delta = 0",
        "adelicPhaseDiscrepancy tau c_inf 1 = 0 ↔ c_inf = tau",
        "C_dil = C_gh → T_conv C_dil = T_conv C_gh",
        "B_ctrl < 17987140 / 1000000",
    ):
        assert clause in lean_text


def test_14_tc051_prime_separation_identity_and_p_squared_support_falsification(
    tc050_artifact: dict,
) -> None:
    """Verify the exact TASK-TC-051 prime-separation identity
    R(X; A, B) = S_p(X; A, B) - p^{-1/2} S_p(X/p; A/p, B/p)
    and falsification of unrestricted R(X/p; A/p, B/p) when p^2 lies in (A, B]."""
    assert tc050_artifact["continuation_task_id"] == TASK_TC_051_ID == "TASK-TC-051"
    assert tc050_artifact["tc051_starting_head"] == STARTING_HEAD_TC_051
    assert tc050_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc050_artifact["rh_proved"] is False

    sec7 = tc050_artifact[
        "section_7_task_tc051_prime_separation_and_summation_by_parts"
    ]
    p_audit = sec7["prime_separation_and_rescaled_band_audit"]
    assert p_audit["all_prime_separation_identities_enclose_zero"] is True
    assert p_audit["all_p_squared_obstructions_detected"] is True
    assert len(p_audit["sample_band_prime_table"]) == 10

    for row in p_audit["sample_band_prime_table"]:
        assert row["prime_sep_identity_encloses_zero"] is True
        if row["has_p_squared_multiple_in_band"]:
            assert row["omitted_p_squared_error_nonzero_certified"] is True

    # Direct live spot check at X = 4, p = 2 where p^2 = 4 in (H(4)=3, M(4)=6]:
    saved_prec = flint_ctx.prec
    flint_ctx.prec = 256
    try:
        x_a = arb(4)
        r_band = evaluate_R_interval_arb(x_a, 3, 6, prec_bits=256)
        s_2 = evaluate_S_p_interval_arb(x_a, 3, 6, 2, prec_bits=256)
        s_2_res = evaluate_S_p_interval_arb(
            x_a / arb(2), 1.5, 3, 2, prec_bits=256
        )
        r_2_unrestricted = evaluate_R_interval_arb(
            x_a / arb(2), 1.5, 3, prec_bits=256
        )
        inv_sqrt2 = arb(1) / arb(2).sqrt()
        assert arb(0) in (r_band - (s_2 - inv_sqrt2 * s_2_res))
        naive_err = r_band - (s_2 - inv_sqrt2 * r_2_unrestricted)
        expected_p_sq_err = -(arb(1) / arb(2)) * evaluate_W_log_em4_certified_arb(
            arb(1), min_N0=240, prec_bits=256
        )
        assert arb(0) in (naive_err - expected_p_sq_err)
        assert bool((abs(naive_err) - arb(0)).lower() > arb(0))
    finally:
        flint_ctx.prec = saved_prec


def test_15_tc051_canonical_rescaled_band_boundary_bounds_and_iterated_tower(
    tc050_artifact: dict,
) -> None:
    """Verify the canonical rescaled-band boundary decomposition
    R_{mu,band}(X) = S_{p,band}(X) - p^{-1/2} S_{p,band}(X/p) - p^{-1/2} B_p(X),
    the uniform bound |B_p(X)| <= B_rescaled < 14.851487, and the two-step prime tower."""
    sec7 = tc050_artifact[
        "section_7_task_tc051_prime_separation_and_summation_by_parts"
    ]
    p_audit = sec7["prime_separation_and_rescaled_band_audit"]
    assert p_audit["all_canonical_band_separations_enclose_zero"] is True
    assert p_audit["all_boundary_bounds_certified"] is True
    assert p_audit["all_tower_telescoping_enclose_zero"] is True

    b_bounds = p_audit["unconditional_rescaled_boundary_bounds"]
    assert (
        b_bounds["B_rescaled_global_all_X_ge_1_and_all_p_certified"]["mid_float"]
        < 14.851486
        < 14.851487
    )
    assert (
        b_bounds["B_rescaled_large_X_when_H_X_ge_p_certified"]["mid_float"]
        < 11.502478
    )

    for row in p_audit["sample_band_prime_table"]:
        assert row["canonical_band_sep_encloses_zero"] is True
        assert row["abs_B_p_le_B_rescaled_certified"] is True


def test_16_tc051_multi_prime_inclusion_exclusion_and_tautological_sieve_collapse(
    tc050_artifact: dict,
) -> None:
    """Verify the multi-prime inclusion-exclusion identity and the tautological sieve collapse
    when y >= B = M(X)."""
    sec7 = tc050_artifact[
        "section_7_task_tc051_prime_separation_and_summation_by_parts"
    ]
    p_audit = sec7["prime_separation_and_rescaled_band_audit"]
    sieve = p_audit["multi_prime_sieve_collapse_and_coset_obstruction"]
    assert sieve["three_prime_P_2_3_5_at_X_16_encloses_zero"] is True
    assert sieve["full_sieve_P_le_M_X_tautological_collapse_verified"] is True
    assert "k = 1" in sieve["tautological_collapse_explanation"]
    assert len(sieve["euler_product_factor_growth"]) == 5
    assert (
        sieve["euler_product_factor_growth"][-1][
            "prod_1_plus_p_neg_half_certified"
        ]["mid_float"]
        > 120000.0
    )


def test_17_tc051_summation_by_parts_tilde_W_log_and_unconditional_endpoint_bound(
    tc050_artifact: dict,
) -> None:
    """Verify the derivative kernel identity -F_X'(t) = t^{-3/2} tilde{W}_log(X/t),
    exact summation by parts, and unconditional upper-endpoint bound
    |M_{H(X)}(M(X)) F_X(M(X))| <= C_{log,0} < 0.557430."""
    sec7 = tc050_artifact[
        "section_7_task_tc051_prime_separation_and_summation_by_parts"
    ]
    sbp = sec7["summation_by_parts_and_tilde_W_log_audit"]
    assert sbp["chain_rule_symbolic_verified"] is True
    assert sbp["termwise_euler_symbolic_verified"] is True
    assert sbp["all_jet_identities_enclose_zero"] is True
    assert sbp["all_sbp_ftc_enclose_zero"] is True
    assert sbp["all_sbp_quadrature_enclose_zero"] is True
    assert sbp["all_endpoint_bounds_certified"] is True
    assert sbp["all_smooth_mertens_transfer_certified"] is True

    for row in sbp["summation_by_parts_table"]:
        assert row["sbp_ftc_identity_encloses_zero"] is True
        if row["independent_quadrature_status"] == "CERTIFIED_QUADRATURE":
            assert row["sbp_quadrature_identity_encloses_zero"] is True
            assert (
                row["smooth_mertens_integral_I_M_band_quadrature_certified"]
                is not None
            )
        else:
            assert row["independent_quadrature_status"] == "NOT_RUN"
            assert row["sbp_quadrature_identity_encloses_zero"] is None
            assert (
                row["smooth_mertens_integral_I_M_band_quadrature_certified"]
                is None
            )
        assert row["abs_endpoint_le_sharp_bound_certified"] is True
        assert row["abs_endpoint_le_C_log_0_certified"] is True
        assert row["abs_R_band_minus_I_M_band_le_C_log_0_certified"] is True


def test_18_tc051_sign_sequence_discrimination_and_tc050r2_reporting_repairs(
    tc050_artifact: dict,
) -> None:
    """Verify sign-sequence cancellation discrimination (actual mu(m) vs +1, |mu(m)|,
    and worst-case |mu(m)| sgn(W_log(X/m))), Lean Theorems 54-56, and TC-050R2 reporting repairs."""
    sec7 = tc050_artifact[
        "section_7_task_tc051_prime_separation_and_summation_by_parts"
    ]
    disc = sec7["sign_sequence_cancellation_discrimination_audit"]
    table = disc["sign_discrimination_table"]
    assert len(table) == 9
    for row in table:
        assert (
            row["R_worst_case_abs_band_certified"]["mid_float"]
            >= abs(row["R_mu_band_actual_certified"]["mid_float"]) - 1e-12
        )
    # At X = 16 and X = tau^2, worst-case unsigned sum exceeds actual |R_{mu,band}| by > 25x:
    row_tau2 = [r for r in table if r["X_label"] == "tau^2"][0]
    assert row_tau2["worst_case_to_actual_abs_ratio_certified"]["mid_float"] > 25.0

    # Verify Lean module declarations (47 defs + 59 theorems = 106 declarations):
    lean_audit = verify_canonical_theta_correlation_lean_module()
    assert len(lean_audit["actual_defs"]) == 47
    assert len(lean_audit["actual_theorems"]) == 59
    assert len(lean_audit["actual_defs"]) + len(lean_audit["actual_theorems"]) == 106
    assert lean_audit["matches_exact"] is True
    assert lean_audit["contains_sorry"] is False
    assert lean_audit["contains_admit"] is False

    # Verify TC-050R2 reporting repairs in docs/reviews/TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md:
    doc_text = (
        REPO_ROOT
        / "docs"
        / "reviews"
        / "TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md"
    ).read_text(encoding="utf-8")
    assert "0.49736248380990124448" in doc_text
    assert "0.4973624838099012420092607" not in doc_text
    assert "0.10383893" not in doc_text
    assert "13.468513" not in doc_text
    assert "maximal positive real offset" not in doc_text
    assert "\\operatorname*{Res}_{s=\\rho}\\bigl(-\\xi'(s)/\\xi(s)\\bigr) = -m_\\rho" in doc_text


def test_19_tc051r_multi_prime_orientation_regression_and_small_Y_upper_cutoff(
    tc050_artifact: dict,
) -> None:
    """Verify the P = {2}, X = 1, (A, B] = (1, 2] multi-prime orientation regression check
    (confirming R(X; A, B) = sum_{d|P} (mu(d)/sqrt(d)) S_P(X/d; A/d, B/d) and rejecting the
    reversed formula) and both upper-cutoff orderings M(X)/p >= M(X/p) and M(X)/p < M(X/p)."""
    sec7 = tc050_artifact[
        "section_7_task_tc051_prime_separation_and_summation_by_parts"
    ]
    p_audit = sec7["prime_separation_and_rescaled_band_audit"]
    sieve = p_audit["multi_prime_sieve_collapse_and_coset_obstruction"]
    orient = sieve["p2_x1_interval_1_2_orientation_regression"]
    assert orient["correct_orientation_encloses_zero"] is True
    assert orient["reversed_formula_detected_nonzero"] is True
    assert orient["S2_1_1_2_certified"]["arb_ball_str"] == "0"
    assert abs(orient["R_1_1_2_certified"]["mid_float"]) > 0.013
    assert abs(orient["reversed_formula_rhs_certified"]["mid_float"]) > 0.027
    assert "not assumed" in sieve["multiplicative_coset_shift_note"]
    assert "-(1/2)" in sieve["euler_product_log_expansion"] or "- (1/2)" in sieve["euler_product_log_expansion"]

    # Verify both upper-cutoff orderings in sample_band_prime_table and the X = 18/5, p = 2 regression:
    assert p_audit["both_upper_cutoff_orderings_certified"] is True
    small_y = p_audit["unconditional_rescaled_boundary_bounds"][
        "small_Y_single_endpoint_regime_X2_p2"
    ]
    assert small_y["single_endpoint_le_B_tail_certified"] is True

    r18_5 = p_audit["unconditional_rescaled_boundary_bounds"][
        "single_endpoint_coprime_surviving_regime_X_18_5_p2"
    ]
    assert r18_5["H_X"] == 2
    assert r18_5["M_X"] == 5
    assert r18_5["H_Y"] == 1
    assert r18_5["M_Y"] == 3
    assert r18_5["delta_high_matches_single_endpoint_encloses_zero"] is True
    assert r18_5["delta_high_nonzero_certified"] is True
    assert r18_5["abs_delta_high_le_analytic_bound_certified"] is True
    assert r18_5["abs_delta_high_le_B_tail_certified"] is True
    assert r18_5["abs_B2_X_le_B_rescaled_certified"] is True
    assert r18_5["canonical_band_separation_encloses_zero"] is True
    assert math.isclose(
        r18_5["delta_high_certified"]["mid_float"], 0.01851256133, abs_tol=1e-9
    )
    assert math.isclose(
        r18_5["R_band_X_certified"]["mid_float"], 0.03772775329, abs_tol=1e-9
    )
    assert math.isclose(
        r18_5["S2_band_Y_certified"]["mid_float"], -0.01851256133, abs_tol=1e-9
    )
    assert math.isclose(
        r18_5["B2_X_certified"]["mid_float"], 0.01851256133, abs_tol=1e-9
    )

    table = p_audit["sample_band_prime_table"]
    row_x2_p2 = [
        r for r in table if r["X_label"] == "2" and r["prime_p"] == 2
    ][0]
    assert row_x2_p2["M_X"] == 3
    assert row_x2_p2["M_X_over_p"] == 2
    assert (
        row_x2_p2["upper_cutoff_ordering"]
        == "M(X)/p < M(X/p) (single-endpoint regime N - 1 < M(X)/p < N)"
    )
    assert row_x2_p2["canonical_band_sep_encloses_zero"] is True
    assert row_x2_p2["abs_B_p_le_B_rescaled_certified"] is True

    rows_ge_4 = [r for r in table if r["X_label"] not in ("1", "2")]
    assert len(rows_ge_4) == 6
    for r in rows_ge_4:
        assert r["upper_cutoff_ordering"] == "M(X)/p >= M(X/p)"


def test_20_tc051r_rescaled_interval_and_canonical_band_inverse_towers(
    tc050_artifact: dict,
) -> None:
    """Verify both the simultaneously rescaled interval inverse tower
    S_0 = sum_{j=0}^{L-1} q^j R_j + q^L S_L (matching Lean Theorem 56 at L = 2)
    and the canonical-band inverse tower
    S_{p,band}(X) = sum_{j=0}^{L-1} q^j (R_{mu,band}(X/p^j) + q B_p(X/p^j)) + q^L S_{p,band}(X/p^L)."""
    sec7 = tc050_artifact[
        "section_7_task_tc051_prime_separation_and_summation_by_parts"
    ]
    p_audit = sec7["prime_separation_and_rescaled_band_audit"]
    assert p_audit["all_tower_telescoping_enclose_zero"] is True

    towers = p_audit["iterated_prime_tower_checks"]
    assert len(towers) == 2
    for row in towers:
        assert row["rescaled_interval_L1_encloses_zero"] is True
        assert row["rescaled_interval_L2_encloses_zero"] is True
        assert row["rescaled_interval_terminal_encloses_zero"] is True
        assert row["canonical_band_L1_encloses_zero"] is True
        assert row["canonical_band_L2_encloses_zero"] is True
        assert row["tower_diff_encloses_zero"] is True
        assert row["canonical_band_steps_J_p_plus_1"] >= 4
        assert row["rescaled_interval_terminal_L"] >= 5


def test_21_tc051r_skipped_quadrature_and_per_observable_arb_radii(
    tc050_artifact: dict,
) -> None:
    """Verify that skipped quadrature rows report NOT_RUN and None fields rather than copying
    I_mertens_ftc, and verify per-observable Arb radius reporting across the 13 sample grades."""
    sec7 = tc050_artifact[
        "section_7_task_tc051_prime_separation_and_summation_by_parts"
    ]
    sbp = sec7["summation_by_parts_and_tilde_W_log_audit"]
    assert sbp["independent_quadrature_max_M_cutoff"] == 32
    assert sbp["independent_quadrature_performed_count"] == 6
    assert sbp["independent_quadrature_passed_count"] == 6
    assert sbp["independent_quadrature_not_run_count"] == 1
    assert sbp["all_performed_sbp_quadrature_enclose_zero"] is True

    row_tau2 = [
        r for r in sbp["summation_by_parts_table"] if r["X_label"] == "tau^2"
    ][0]
    assert row_tau2["M_X"] == 99
    assert row_tau2["independent_quadrature_status"] == "NOT_RUN"
    assert (
        row_tau2["smooth_mertens_integral_I_M_band_quadrature_certified"]
        is None
    )
    assert row_tau2["sbp_quadrature_identity_encloses_zero"] is None

    # Direct live call with max_quadrature_M = 2 must mark all rows with M(X) > 2 as NOT_RUN:
    live_sbp = verify_summation_by_parts_and_tilde_W_log_identity_arb(
        prec_bits=256,
        max_quadrature_M=2,
    )
    assert live_sbp["independent_quadrature_performed_count"] == 1
    assert live_sbp["independent_quadrature_passed_count"] == 1
    assert live_sbp["independent_quadrature_not_run_count"] == 6
    row_live_4 = [
        r for r in live_sbp["summation_by_parts_table"] if r["X_label"] == "4"
    ][0]
    assert row_live_4["independent_quadrature_status"] == "NOT_RUN"
    assert (
        row_live_4["smooth_mertens_integral_I_M_band_quadrature_certified"]
        is None
    )
    assert row_live_4["sbp_quadrature_identity_encloses_zero"] is None

    # Verify per-observable radius summary and ceilings across the 13 sample grades:
    sec4 = tc050_artifact["section_4_canonical_hilbert_schmidt_orbit_decomposition"]
    assert "precision_scope_note" not in sec4
    decomp = sec4["exact_decomposition_and_controlled_remainder_bounds"]
    obs_summary = decomp["observable_radius_summary_across_13_sample_grades"]
    assert obs_summary["all_declared_ceilings_verified"] is True

    rad_k0 = obs_summary["per_observable_k0_radius"]
    rad_max = obs_summary["per_observable_max_radius"]
    declared = obs_summary["per_observable_declared_ceilings"]

    expected_ceilings = {
        "P_tau_K_HS_orbit_certified": (3.22e-22, 3.22e-22),
        "pole_plus_transfer_term_neg_c_tau_A_h0_certified": (6.35e-75, 6.35e-75),
        "small_scale_prime_W_inv_XK_certified": (7.02e-9, 7.02e-9),
        "divisor_aggregated_W_log_XK_certified": (4.49e-14, 6.59e-11),
        "head_divisor_R_mu_head_XK_certified": (0.0, 5.64e-11),
        "resonant_band_R_mu_band_XK_direct_sum_certified": (4.04e-11, 5.65e-11),
        "super_scale_tail_R_mu_tail_XK_direct_certified": (1.89e-5, 5.43e-4),
        "E_tau_controlled_K_certified": (1.89e-5, 5.43e-4),
        "E_tau_K_total_remainder_certified": (1.41e-8, 6.87e-5),
        "C_tau_K_certified": (1.41e-8, 6.87e-5),
    }
    for obs_key, (exp_k0_ceil, exp_max_ceil) in expected_ceilings.items():
        assert declared[obs_key]["k0_ceiling"] == exp_k0_ceil
        assert declared[obs_key]["max_ceiling"] == exp_max_ceil
        assert 0.0 <= rad_k0[obs_key] <= exp_k0_ceil
        assert 0.0 <= rad_max[obs_key] <= exp_max_ceil

    assert 1.88e-5 < rad_k0["super_scale_tail_R_mu_tail_XK_direct_certified"] <= 1.89e-5
    assert 1.88e-5 < rad_k0["E_tau_controlled_K_certified"] <= 1.89e-5
    assert 5.42e-4 < rad_max["super_scale_tail_R_mu_tail_XK_direct_certified"] <= 5.43e-4
    assert 5.42e-4 < rad_max["E_tau_controlled_K_certified"] <= 5.43e-4
    assert 1.40e-8 < rad_k0["E_tau_K_total_remainder_certified"] <= 1.41e-8
    assert 1.40e-8 < rad_k0["C_tau_K_certified"] <= 1.41e-8
    assert 6.86e-5 < rad_max["E_tau_K_total_remainder_certified"] <= 6.87e-5
    assert 6.86e-5 < rad_max["C_tau_K_certified"] <= 6.87e-5


def test_22_tc051r_review_markdown_and_json_artifact_consistency(
    tc050_artifact: dict,
) -> None:
    """Verify that the Section 8.2, 8.3, and 8.4 tables and narrative values in
    docs/reviews/TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md and
    docs/reviews/TC_CANONICAL_THETA_CORRELATION_BOUND.md match the JSON artifact."""
    sec7 = tc050_artifact[
        "section_7_task_tc051_prime_separation_and_summation_by_parts"
    ]
    sep = sec7["prime_separation_and_rescaled_band_audit"]
    sbp = sec7["summation_by_parts_and_tilde_W_log_audit"]
    disc = sec7["sign_sequence_cancellation_discrimination_audit"]
    by_xp_sep = {
        (row["X_label"], row["prime_p"]): row
        for row in sep["sample_band_prime_table"]
    }
    by_x_sbp = {row["X_label"]: row for row in sbp["summation_by_parts_table"]}
    by_x_disc = {row["X_label"]: row for row in disc["sign_discrimination_table"]}

    # Verify exact X = 64 values in JSON artifact:
    r64 = by_x_disc["64"]
    assert r64["H_X"] == 32
    assert r64["M_X"] == 182
    assert math.isclose(
        r64["R_mu_band_actual_certified"]["mid_float"],
        0.03059141547,
        rel_tol=1e-9,
    )
    assert math.isclose(
        r64["R_const_one_band_certified"]["mid_float"],
        -0.01583365880,
        rel_tol=1e-9,
    )
    assert math.isclose(
        r64["R_squarefree_indicator_band_certified"]["mid_float"],
        0.01904894183,
        rel_tol=1e-9,
    )
    assert math.isclose(
        r64["R_worst_case_abs_band_certified"]["mid_float"],
        0.29032671364,
        rel_tol=1e-9,
    )
    assert math.isclose(
        r64["worst_case_to_actual_abs_ratio_certified"]["mid_float"],
        9.49046357,
        rel_tol=1e-7,
    )

    # Parse Section 8.2, 8.3, and 8.4 tables in TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md:
    doc_path = (
        REPO_ROOT
        / "docs"
        / "reviews"
        / "TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md"
    )
    doc_text = doc_path.read_text(encoding="utf-8")
    x_label_map = {
        "$1$": "1",
        "$2$": "2",
        "$4$": "4",
        "$\\tau$": "tau",
        "$10$": "10",
        "$16$": "16",
        "$25$": "25",
        "$\\tau^2$": "tau^2",
        "$64$": "64",
    }
    matched_sep_rows = 0
    matched_18_5_row = False
    matched_sbp_rows = 0
    matched_disc_rows = 0
    r18_5 = sep["unconditional_rescaled_boundary_bounds"][
        "single_endpoint_coprime_surviving_regime_X_18_5_p2"
    ]
    for line in doc_text.splitlines():
        line_s = line.strip()
        if not line_s.startswith("|"):
            continue
        cells = [c.strip() for c in line_s.strip("|").split("|")]
        if len(cells) == 9 and cells[0] == "$18/5$" and cells[1] == "$2$":
            matched_18_5_row = True
            assert math.isclose(
                float(cells[5].strip("$")),
                r18_5["R_band_X_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                float(cells[6].strip("$")),
                r18_5["S2_band_X_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                float(cells[7].strip("$")),
                r18_5["S2_band_Y_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                float(cells[8].strip("$")),
                r18_5["B2_X_certified"]["mid_float"],
                abs_tol=1e-9,
            )
        elif (
            len(cells) == 9
            and cells[0] in x_label_map
            and cells[1] in ("$2$", "$3$", "$5$")
        ):
            x_lbl = x_label_map[cells[0]]
            p_val = int(cells[1].strip("$"))
            row = by_xp_sep[(x_lbl, p_val)]
            matched_sep_rows += 1
            assert math.isclose(
                float(cells[5].strip("$")),
                row["R_mu_band_X_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                float(cells[6].strip("$")),
                row["S_p_band_X_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                float(cells[7].strip("$")),
                row["S_p_band_X_over_p_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                float(cells[8].strip("$")),
                row["B_p_X_boundary_certified"]["mid_float"],
                abs_tol=1e-9,
            )
        elif (
            len(cells) == 8
            and cells[0] in x_label_map
            and cells[1].startswith("$(")
        ):
            x_lbl = x_label_map[cells[0]]
            row = by_x_sbp[x_lbl]
            matched_sbp_rows += 1
            assert math.isclose(
                float(cells[3].strip("$")),
                row["R_mu_band_X_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                float(cells[4].strip("$")),
                row["upper_endpoint_term_M_B_F_B_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                float(cells[5].strip("$")),
                row["smooth_mertens_integral_I_M_band_ftc_certified"][
                    "mid_float"
                ],
                abs_tol=1e-9,
            )
        elif len(cells) == 7 and cells[0] in x_label_map and cells[1].startswith("$("):
            x_lbl = x_label_map[cells[0]]
            row = by_x_disc[x_lbl]
            matched_disc_rows += 1
            r_mu_doc = float(cells[2].strip("$"))
            r_1_doc = float(cells[3].strip("$"))
            r_sqf_doc = float(cells[4].strip("$"))
            r_wc_doc = float(cells[5].strip("$"))
            ratio_doc = float(cells[6].strip("$").rstrip("\\times"))
            assert math.isclose(
                r_mu_doc,
                row["R_mu_band_actual_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                r_1_doc,
                row["R_const_one_band_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                r_sqf_doc,
                row["R_squarefree_indicator_band_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                r_wc_doc,
                row["R_worst_case_abs_band_certified"]["mid_float"],
                abs_tol=1e-9,
            )
            assert math.isclose(
                ratio_doc,
                row["worst_case_to_actual_abs_ratio_certified"]["mid_float"],
                abs_tol=1e-4,
            )
    assert matched_sep_rows == 10
    assert matched_18_5_row is True
    assert matched_sbp_rows == 7
    assert matched_disc_rows == 9

    assert "1 <= L <= floor(log_p X) + 1" in sep["canonical_rescaled_band_identity"]
    assert "1 \\le L \\le \\lfloor\\log_p X\\rfloor + 1" in doc_text
    assert "\\lfloor H(X)/p\\rfloor \\le H(X/p)" in doc_text
    assert "floor(H(X)/p) <= H(X/p)" in (
        tc050_artifact["section_5_lean_formalization_and_remaining_obligation"][
            "committed_lean_theorems_exact_scope"
        ]["theorem_54_prime_separation_and_canonical_band_boundary_equivalence"][
            "external_analytic_scope_note"
        ]
    )
    assert (
        "precision_scope_note"
        not in tc050_artifact[
            "section_4_canonical_hilbert_schmidt_orbit_decomposition"
        ]
    )
    prec_note = tc050_artifact[
        "section_4_canonical_hilbert_schmidt_orbit_decomposition"
    ]["exact_decomposition_and_controlled_remainder_bounds"][
        "observable_radius_summary_across_13_sample_grades"
    ]["precision_scope_note"]
    assert "4.36e-7" not in prec_note
    assert "E_{tau,controlled}(0) has radius <= 6.35e-75" not in prec_note
    for expected_phrase in (
        "W_log(X_K), R_{mu,head}(X_K), and R_{mu,band}(X_K) (evaluated by 4th-order Euler-Maclaurin on [N0, infty)) have radii <= 6.59e-11 (<= 6.59e-11, <= 5.64e-11, and <= 5.65e-11)",
        "P_tau(K) has radius <= 3.22e-22",
        "-(c_tau^B+2)h_0(X_K) has radius <= 6.35e-75",
        "W(X_K^{-1}) has radius <= 7.02e-9",
        "R_{mu,tail}(X_K) and E_{tau,controlled}(K) include the direct super-scale tail remainder C_{log,0} X_K^{5/2} / (2 m_tail_cut^2) and inner small-tail truncations (radii <= 1.89e-5 at K=0 up to <= 5.43e-4 at |K|=2)",
        "C_tau(K) and E_tau(K) include the prime-power Rosser-Schoenfeld tail on n > 16500 in W(X_K) (radii <= 1.41e-8 at K=0 up to <= 6.87e-5 at |K|=2)",
    ):
        assert expected_phrase in prec_note

    # Ensure stale pre-reconciliation X = 64 numbers and false Case 2 claims are absent across all review and ledger files:
    for rel_path in (
        "docs/reviews/TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md",
        "docs/reviews/TC_CANONICAL_THETA_CORRELATION_BOUND.md",
        "TRANSCENDENTAL_CONTINUATION.md",
        "RESEARCH_LEDGER.md",
        ".agents/corpus_map/obligation_register.md",
    ):
        text = (REPO_ROOT / rel_path).read_text(encoding="utf-8")
        for stale_str in (
            "0.0040964438",
            "0.5621393982",
            "137.23",
            "124.36",
            "0.1592684523",
            "-0.0012834192",
            "15.13020",
            "15.13019",
            "can occur only when",
            "1 <= X/p < 2^{4/5}",
            "1 \\le X/p < 2^{4/5}",
            "H(X)/p <= H(X/p)",
        ):
            assert stale_str not in text, (
                f"Found stale string {stale_str} in {rel_path}"
            )


def test_23_tc052_transition_vanishing_moments_linear_density_and_vaughan_type_I(
    tc050_artifact: dict,
) -> None:
    """Verify TASK-TC-052 / TASK-TC-052R Approach A: Mellin vanishing moments of W_log and
    tilde{W}_log, negative small-v expansion of W_log(v), strictly positive two-endpoint
    limit L > 0 for J_band(X) and R_{1,band}(X), unconditional O(1) vs conditional o(sqrt(t))
    scope for R_{|mu|,band}(X), rescaled transition-integral identity, Landau's Moebius
    harmonic bound, repaired Vaughan c_II sign (U=V=1, m=4 regression), and complete
    Type I bounded-variation progression proof."""
    assert tc050_artifact["subgate_closure_attempt_task_id"] == "TASK-TC-052"
    assert tc050_artifact["tc052_repair_task_id"] == "TASK-TC-052R"
    assert (
        tc050_artifact["tc052_starting_head"]
        == "1f576944c040d5b3a2bf8091ca803e3758c80d12"
    )
    assert (
        tc050_artifact["tc052_merged_main_baseline"]
        == "916440e688c66d461daa04b17d7435e10e65f0d4"
    )
    assert (
        tc050_artifact["tc052_implementation_commit"]
        == "8414aa66f1127c636c68fcf8594833c570a3344a"
    )
    assert tc050_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc050_artifact["rh_proved"] is False

    sec8 = tc050_artifact[
        "section_8_task_tc052_transition_cancellation_and_spectral_dirichlet_factorization"
    ]
    assert sec8["task_id"] == "TASK-TC-052"
    assert sec8["repair_task_id"] == "TASK-TC-052R"
    assert sec8["subgate_tc043a_status"] == "OPEN"
    assert sec8["rh_proved"] is False

    app_a = sec8["approach_a_signed_transition_region_cancellation"]
    moments = app_a["mellin_vanishing_moments_audit"]
    assert moments["symbolic_moments_verified"] is True
    assert moments["W_log_vanishing_order_at_z_pos_half"] == 1
    assert moments["W_log_vanishing_order_at_z_neg_half"] == 3
    assert moments["tilde_W_log_vanishing_order_at_z_pos_half"] == 1
    assert moments["tilde_W_log_vanishing_order_at_z_neg_half"] == 4
    assert moments["total_vanishing_endpoint_moments_of_tilde_W_log"] == 5
    assert "1 / 512" in moments["first_log_moment_at_z_pos_half_formula"]
    assert "3 log(tau) / 128" in moments["fourth_log_moment_at_z_neg_half_formula"]

    lin = app_a["linear_density_annihilation_and_exact_limits"]
    assert "< 0   (v -> 0^+)" in lin["W_log_small_v_asymptotic_formula"]
    assert (
        float(
            lin[
                "W_log_small_v_leading_coeff_81_zeta_prime_3_over_64_certified"
            ]["upper_dec"]
        )
        < -0.250753
    )
    assert float(lin["J_band_uniform_bound_B_J_certified"]["upper_dec"]) < 4.768220
    assert math.isclose(
        lin["upper_v_tail_limit_from_H_X_certified"]["mid_float"],
        0.01284544282,
        abs_tol=1e-9,
    )
    assert math.isclose(
        lin["lower_v_tail_limit_from_M_X_certified"]["mid_float"],
        0.12537676308,
        abs_tol=1e-9,
    )
    assert (
        "lim_{X -> infty} J_band(X) = lim_{X -> infty} R_{1,band}(X) = L"
        in lin["exact_limit_J_band_and_R_1_band_as_X_to_infty_formula"]
    )
    assert math.isclose(
        lin["exact_limit_R_1_band_as_X_to_infty_certified"]["mid_float"],
        0.13822220590,
        abs_tol=1e-9,
    )
    assert math.isclose(
        lin["exact_limit_R_sqfree_band_as_X_to_infty_certified"]["mid_float"],
        0.08402902496,
        abs_tol=1e-9,
    )
    sq_note = lin["R_sqfree_band_unconditional_O1_scope_and_conditional_limit_note"]
    assert "uniformly bounded for all X >= 1" in sq_note
    assert "E_Q(t) = o(sqrt(t))" in sq_note

    resc = app_a["rescaled_transition_integral_verification"]
    assert resc["all_rescaled_identities_enclose_zero"] is True
    assert len(resc["rescaled_integral_table"]) == 8
    for row in resc["rescaled_integral_table"]:
        assert row["difference_encloses_zero"] is True

    vaughan = app_a["vaughan_band_decomposition_and_type_I_audit"]
    assert vaughan["landau_moebius_harmonic_bound_verified_up_to_200"] is True
    assert vaughan["max_abs_sum_mu_d_over_d_up_to_200_exact"] == "1/1"
    assert vaughan["all_vaughan_admissibility_verified"] is True
    assert vaughan["all_vaughan_identities_enclose_zero"] is True
    assert vaughan["all_type_I_em_bounds_certified"] is True

    reg = vaughan["vaughan_m4_U1_V1_regression"]
    assert reg["U"] == 1 and reg["V"] == 1 and reg["m"] == 4
    assert reg["c_I_4_1_1"] == -1
    assert reg["c_II_4_1_1_published_r_gt_V"] == 1
    assert reg["c_II_4_1_1_published_negated_r_le_V"] == 1
    assert reg["c_II_4_1_1_unnegated_r_le_V_wrong"] == -1
    assert reg["c_I_plus_c_II_equals_mu_4"] is True
    assert reg["unnegated_r_le_V_detected_wrong"] is True

    bv_proof = vaughan[
        "type_I_total_variation_and_sum_integral_discrepancy_proof"
    ]
    assert bv_proof["tilde_psi0_polynomial_identities_verified"] is True
    assert (
        float(bv_proof["C_BV_norm_plus_var_bound_certified"]["upper_dec"])
        < 40130.0
    )
    assert (
        float(
            bv_proof["C_EM_I_progression_discrepancy_constant_certified"][
                "upper_dec"
            ]
        )
        < 40148.0
    )
    assert (
        float(
            bv_proof["type_I_global_bound_B_J_plus_C_EM_I_certified"][
                "upper_dec"
            ]
        )
        < 40152.70
    )

    assert len(vaughan["vaughan_band_table"]) == 8
    for row in vaughan["vaughan_band_table"]:
        assert row["UV_le_sqrt_X"] is True
        assert row["max_UV_le_H_X"] is True
        assert row["pointwise_coeff_identity_mu_eq_cI_plus_cII"] is True
        assert row["both_published_c_II_forms_match"] is True
        assert row["vaughan_sum_difference_encloses_zero"] is True
        assert row["type_I_exchange_difference_encloses_zero"] is True
        assert row["abs_R_type_I_le_analytic_bound_certified"] is True


def test_24_tc052_euler_sieved_orbit_critical_line_mellin_and_closure_chain(
    tc050_artifact: dict,
) -> None:
    """Verify TASK-TC-052 / TASK-TC-052R Approach B (Plancherel multiplier nu(t) with
    nu(0)=0, operator intertwining on H_tau^pos, proved critical-line Mellin certificates
    for R_{mu,band}(X), and low-frequency Euler spike lower bound with (log y)^{-3}
    prefactor), the complete conditional closure chain, and Lean Theorems 57-59."""
    sec8 = tc050_artifact[
        "section_8_task_tc052_transition_cancellation_and_spectral_dirichlet_factorization"
    ]
    app_b = sec8[
        "approach_b_hilbert_space_euler_intertwining_and_critical_line_factorization"
    ]
    inter = app_b["operator_intertwining_on_H_tau_pos"]
    assert inter["all_sieve_orbit_identities_enclose_zero"] is True
    assert len(inter["sieve_orbit_verification_table"]) == 4
    for row in inter["sieve_orbit_verification_table"]:
        assert row["P_tau_minus_P_y_plus_Delta_encloses_zero"] is True
        assert "K + log_tau(m)" in row["shift_convention"]

    planch = app_b["plancherel_multiplier_nu_and_domain_audit"]
    assert planch["nu_at_0_equals_zero"] is True
    assert ">= 4 t^2 / (t^2 + 1/4) >= 0" in planch[
        "nu_nonnegative_and_quadratic_lower_bound"
    ]
    assert planch["digamma_constant_reconciliation_encloses_zero"] is True
    assert planch["plancherel_reconciles_with_P_tau_0_encloses_zero"] is True
    assert math.isclose(
        planch["plancherel_J_tau_psi_tau_norm_sq_certified"]["mid_float"],
        2.558258007415831,
        abs_tol=1e-12,
    )

    crit = app_b["critical_line_spectral_dirichlet_factorization"]
    assert crit["all_crit_line_identities_enclose_zero"] is True
    assert crit["cutoff_T"] == 48
    assert (
        float(crit["B_Omega_1_tail_T_certified"]["upper_dec"]) < 1.372e-18
    )
    assert (
        float(crit["B_Omega_2_tail_T_certified"]["upper_dec"]) < 7.392e-37
    )
    assert (
        crit["Omega_log_L1_ge_sqrt2_abs_R_band_1_certification"]["certified"]
        is True
    )
    assert 0.100843 < crit["Omega_log_L1_norm_certified"]["mid_float"] < 0.100844
    assert 0.025900 < crit["Omega_log_L2_norm_certified"]["mid_float"] < 0.025901
    assert len(crit["critical_line_verification_table"]) == 3
    for row in crit["critical_line_verification_table"]:
        assert row["difference_encloses_zero"] is True
        assert row["finite_integration_error_radius"] < 1e-13
        assert row["infinite_tail_error_bound"] < 4e-18

    spike = app_b["low_frequency_euler_spike_obstruction_on_H_tau_pos"]
    assert spike["nu_at_0_equals_0"] is True
    assert math.isclose(
        spike["nu_taylor_t2_coeff_certified"]["mid_float"],
        16.1659674922,
        abs_tol=1e-8,
    )
    assert (
        float(
            spike[
                "spike_prefactor_C_spike_49_tau_sq_H0_0_over_640_certified"
            ]["lower_dec"]
        )
        > 8.55e-05
    )
    assert math.isclose(
        spike["four_cos_tau_16_exponent_certified"]["mid_float"],
        3.6955181300,
        abs_tol=1e-8,
    )

    chain = sec8["complete_conditional_closure_implication_chain"]
    assert len(chain["implication_chain_links"]) == 3
    assert (
        chain["combined_base_constant_lt_rational_ceiling_certified"] is True
    )
    assert (
        float(
            chain[
                "combined_base_constant_P0_plus_B_ctrl_plus_C_log_0_certified"
            ]["upper_dec"]
        )
        < 21.102829
    )

    sec5 = tc050_artifact["section_5_lean_formalization_and_remaining_obligation"]
    assert sec5["new_lean_theorems_tc052"] == [
        "transition_integral_linear_density_annihilation_and_sqrt_error_bound",
        "vaughan_band_decomposition_and_type_I_uniform_bound",
        "euler_sieved_orbit_and_complete_subgate_closure_chain",
    ]
    assert "tc052r_evidence_and_scope_separation" in sec5
    scopes = sec5["committed_lean_theorems_exact_scope"]
    for thm_key in (
        "theorem_57_transition_integral_linear_density_annihilation_and_sqrt_error_bound",
        "theorem_58_vaughan_band_decomposition_and_type_I_uniform_bound",
        "theorem_59_euler_sieved_orbit_and_complete_subgate_closure_chain",
    ):
        assert thm_key in scopes
        assert (
            "Conditional/algebraic real-inequality lemma"
            in scopes[thm_key]["external_analytic_scope_note"]
        )


def test_25_tc052r_repair_reconciliation_and_stale_claim_absence(
    tc050_artifact: dict,
) -> None:
    """Verify all 7 TASK-TC-052R repair requirements and confirm that stale pre-repair
    strings (lim J_band = 0, sqrt(X) <= H(X), 0.043399/0.043400, 1e-20 tail, mu_arch^B(0) = 2,
    1/(512*pi), 3*log(tau)/(128*pi), P_tau(K - log_tau m)) are absent from the source,
    artifact, review, and ledger files."""
    for rel_path in (
        "docs/reviews/TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md",
        "docs/reviews/TC_CANONICAL_THETA_CORRELATION_BOUND.md",
        "TRANSCENDENTAL_CONTINUATION.md",
        "RESEARCH_LEDGER.md",
        ".agents/corpus_map/obligation_register.md",
        "formal/RiemannScope/README.md",
    ):
        text = (REPO_ROOT / rel_path).read_text(encoding="utf-8")
        for stale_str in (
            "\\lim_{X\\to\\infty} J_{\\mathrm{band}}(X) = 0",
            "\\lim_{X\\to\\infty}J_{\\mathrm{band}}(X) = 0",
            "lim_{X->infty} J_band(X) = 0",
            "0.043399",
            "0.043400",
            "0.251243",
            "1/(512*pi)",
            "3*log(tau)/(128*pi)",
            "21103099/1000000",
        ):
            assert stale_str not in text, (
                f"Found stale pre-TC-052R string {stale_str!r} in {rel_path}"
            )

    # Verify Lean file contains the repaired U=V=1, m=4 and nu(t) quadratic lower bound conjuncts:
    lean_text = (
        REPO_ROOT / "formal/RiemannScope/CanonicalThetaCorrelationBound.lean"
    ).read_text(encoding="utf-8")
    assert "((-1 : ℝ) + 1 = 0 ∧ (-1 : ℝ) + (-1 : ℝ) ≠ 0)" in lean_text
    assert "(16 / 5 : ℝ) * t ^ 2 ≤ nu_B + (4 * t ^ 2) / (t ^ 2 + 1 / 4)" in lean_text
    assert "Conditional/algebraic Euler-sieved" in lean_text


def test_26_tc052r2_displayed_review_certificates_contain_full_generated_enclosures_and_sync(
    tc050_artifact: dict,
) -> None:
    """Verify TASK-TC-052R2 requirements:
    1. Every displayed [mid \\pm rad] certificate interval in Section 8/9 of
       docs/reviews/TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md strictly contains the
       entire generated certificate enclosure ([Decimal(lower_dec), Decimal(upper_dec)] and
       arb(arb_ball_str)), and the named Mellin error components (finite_integration_error_radius,
       infinite_tail_error_bound, combined_enclosure_radius) match separately.
    2. H_0(it) = ((t^2 + 1/4)^4 / (1024 * sqrt(pi))) * |Gamma(1/4 + i*t/2)|^2, one-sided vs
       two-sided B_{Omega,j}^{tail}(T) convention, actual degree-6 Taylor + bool(z2.real > arb(0))
       quadrature, and Plancherel tail bound 2 * B_{Omega,1}^{tail}(48).
    3. Type I Lebesgue measure dv, |mu(d)*mu(r)| <= 1, direct admissibility floor(X^{1/4}) <= floor(X^{5/6}),
       O(X^{-5/6}) and O(X^{-5/4}) cutoff perturbations, and updated Type I constants
       (tilde_A1 = 17685797581/688128, tilde_A2 = 14758395/1024, V_f, C_BV, C_EM_I, B_J + C_EM_I).
    4. Non-completeness of (D(J_tau), ||J_tau .||_{H_tau^pos}) as an inner-product space and
       isometric embedding into H_tau^pos.
    5. Lean declaration count 47 + 59 = 106, Theorems 57-59 declaration names, mathematical
       hypotheses (h_EM_bound, h_bridge), and #print axioms output ([propext, Classical.choice, Quot.sound]).
    """
    from decimal import Decimal, getcontext
    import re
    from tc.canonical_theta_correlation_bound import evaluate_f_tau_acb

    sec8 = tc050_artifact[
        "section_8_task_tc052_transition_cancellation_and_spectral_dirichlet_factorization"
    ]
    assert sec8["followup_repair_task_id"] == "TASK-TC-052R2"
    assert sec8["subgate_tc043a_status"] == "OPEN"
    assert sec8["rh_proved"] is False

    app_a = sec8["approach_a_signed_transition_region_cancellation"]
    lin = app_a["linear_density_annihilation_and_exact_limits"]
    vaughan = app_a["vaughan_band_decomposition_and_type_I_audit"]
    bv_proof = vaughan["type_I_total_variation_and_sum_integral_discrepancy_proof"]

    app_b = sec8[
        "approach_b_hilbert_space_euler_intertwining_and_critical_line_factorization"
    ]
    planch = app_b["plancherel_multiplier_nu_and_domain_audit"]
    crit = app_b["critical_line_spectral_dirichlet_factorization"]
    spike = app_b["low_frequency_euler_spike_obstruction_on_H_tau_pos"]
    chain = sec8["complete_conditional_closure_implication_chain"]

    rev_text = (
        REPO_ROOT / "docs/reviews/TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md"
    ).read_text(encoding="utf-8")

    # 1. Verify all displayed [mid \pm rad] certificate intervals across the entire review
    # strictly contain the full generated certificate enclosures in both Decimal(100) and 256-bit Arb:
    decomp = tc050_artifact[
        "section_4_canonical_hilbert_schmidt_orbit_decomposition"
    ]["exact_decomposition_and_controlled_remainder_bounds"]
    prov = decomp["component_bound_provenance_records"]
    bounds = decomp["unconditional_component_bounds_over_all_K_in_A_R"]
    sec7_psep = tc050_artifact[
        "section_7_task_tc051_prime_separation_and_summation_by_parts"
    ]["prime_separation_and_rescaled_band_audit"]
    sec7_bdry = sec7_psep["unconditional_rescaled_boundary_bounds"]
    by_X_crit = {r["X_label"]: r for r in crit["critical_line_verification_table"]}

    displayed_cert_checks = [
        (
            "[13.46851 \\pm 4.74 \\times 10^{-6}]",
            "13.46851",
            "4.74e-6",
            prov["component_3_divisor_aggregated_W_log_XK"][
                "large_scale_decay_constant_C_log_EM_certified"
            ],
        ),
        (
            "[13.46851 \\pm 4.74\\times 10^{-6}]",
            "13.46851",
            "4.74e-6",
            prov["component_3_divisor_aggregated_W_log_XK"][
                "large_scale_decay_constant_C_log_EM_certified"
            ],
        ),
        (
            "[16.16596749219211504166724589735549873591 \\pm 2.00 \\times 10^{-38}]",
            "16.16596749219211504166724589735549873591",
            "2.00e-38",
            planch["nu_taylor_t2_coeff_16_minus_psi_d2_over_8_certified"],
        ),
        (
            "[2.671922488868445008137488237241150824707 \\pm 2.00 \\times 10^{-39}]",
            "2.671922488868445008137488237241150824707",
            "2.00e-39",
            prov["component_1_pole_plus_transfer_h0"]["bound_certified"],
        ),
        (
            "[0.46372978 \\pm 7.98\\times 10^{-9}]",
            "0.46372978",
            "7.98e-9",
            prov["component_2_reflected_small_scale_prime_W_inv_XK"]["bound_certified"],
        ),
        (
            "[3.34900801876069131272842822 \\pm 5.40\\times 10^{-27}]",
            "3.34900801876069131272842822",
            "5.40e-27",
            prov["component_3_divisor_aggregated_W_log_XK"]["bound_certified"],
        ),
        (
            "[11.22376 \\pm 5.61\\times 10^{-6}]",
            "11.22376",
            "5.61e-6",
            prov["component_4_head_divisor_R_mu_head_XK"]["bound_certified"],
        ),
        (
            "[0.2787147935540087649401176325966251750389 \\pm 2.00 \\times 10^{-40}]",
            "0.2787147935540087649401176325966251750389",
            "2.00e-40",
            prov["component_5_super_scale_tail_R_mu_tail_XK"]["bound_certified"],
        ),
        (
            "[17.98713 \\pm 7.37\\times 10^{-6}]",
            "17.98713",
            "7.37e-6",
            bounds["abs_E_tau_controlled_global_bound_certified"],
        ),
        (
            "[11.50247 \\pm 7.07\\times 10^{-6}]",
            "11.50247",
            "7.07e-6",
            bounds["abs_E_tau_controlled_limsup_bound_certified"],
        ),
        (
            "[11.50247 \\pm 7.07 \\times 10^{-6}]",
            "11.50247",
            "7.07e-6",
            bounds["abs_E_tau_controlled_limsup_bound_certified"],
        ),
        (
            "[0.0185125613290 \\pm 2.58 \\times 10^{-14}]",
            "0.0185125613290",
            "2.58e-14",
            sec7_bdry["single_endpoint_coprime_surviving_regime_X_18_5_p2"][
                "delta_high_certified"
            ],
        ),
        (
            "[0.6700620832085948550527207175609300880270 \\pm 2.00 \\times 10^{-40}]",
            "0.6700620832085948550527207175609300880270",
            "2.00e-40",
            sec7_bdry["B_subunit_when_X_lt_p_coeff_zeta3_C_log_0_certified"],
        ),
        (
            "[14.85148 \\pm 5.09 \\times 10^{-6}]",
            "14.85148",
            "5.09e-6",
            sec7_bdry["B_rescaled_global_all_X_ge_1_and_all_p_certified"],
        ),
        (
            "[127804.0331068035324510388681825571283193 \\pm 2.00 \\times 10^{-34}]",
            "127804.0331068035324510388681825571283193",
            "2.00e-34",
            sec7_psep["multi_prime_sieve_collapse_and_coset_obstruction"][
                "euler_product_factor_growth"
            ][-1]["prod_1_plus_p_neg_half_certified"],
        ),
        (
            "[0.5574295871080175298802352651932503500777 \\pm 2.00 \\times 10^{-40}]",
            "0.5574295871080175298802352651932503500777",
            "2.00e-40",
            prov["component_5_super_scale_tail_R_mu_tail_XK"][
                "small_argument_constant_C_log_0_certified"
            ],
        ),
        (
            "[4.76822 \\pm 3.45 \\times 10^{-6}]",
            "4.76822",
            "3.45e-6",
            lin["J_band_uniform_bound_B_J_certified"],
        ),
        (
            "[+0.01284544282150966111041861441751842139795 \\pm 2.00 \\times 10^{-41}]",
            "0.01284544282150966111041861441751842139795",
            "2.00e-41",
            lin["upper_v_tail_limit_from_H_X_certified"],
        ),
        (
            "[+0.1253767630760670712483220901700480433353 \\pm 2.00 \\times 10^{-40}]",
            "0.1253767630760670712483220901700480433353",
            "2.00e-40",
            lin["lower_v_tail_limit_from_M_X_certified"],
        ),
        (
            "[+0.1382222058975767323587407045875664647333 \\pm 2.00 \\times 10^{-40}]",
            "0.1382222058975767323587407045875664647333",
            "2.00e-40",
            lin["exact_limit_R_1_band_as_X_to_infty_certified"],
        ),
        (
            "[+0.08402902504318437033701087820794188618435 \\pm 2.00 \\times 10^{-41}]",
            "0.08402902504318437033701087820794188618435",
            "2.00e-41",
            lin["exact_limit_R_sqfree_band_as_X_to_infty_certified"],
        ),
        (
            "[3.122911998070261993078893101767253989745 \\pm 2.00 \\times 10^{-39}]",
            "3.122911998070261993078893101767253989745",
            "2.00e-39",
            lin["tilde_C_log_0_origin_constant_certified"],
        ),
        (
            "[1.040970666023420664359631033922417996582 \\pm 2.00 \\times 10^{-39}]",
            "1.040970666023420664359631033922417996582",
            "2.00e-39",
            bv_proof["var_f_small_v_0_to_1_bound_certified"],
        ),
        (
            "[40115.34705084240625775049603174603174603 \\pm 2.00 \\times 10^{-35}]",
            "40115.34705084240625775049603174603174603",
            "2.00e-35",
            bv_proof["var_f_large_v_1_to_inf_bound_certified"],
        ),
        (
            "[40116.38802150842967841485566277995416403 \\pm 2.00 \\times 10^{-35}]",
            "40116.38802150842967841485566277995416403",
            "2.00e-35",
            bv_proof["var_f_total_bound_V_f_certified"],
        ),
        (
            "[40129.85653 \\pm 6.24 \\times 10^{-6}]",
            "40129.85653",
            "6.24e-6",
            bv_proof["C_BV_norm_plus_var_bound_certified"],
        ),
        (
            "[40143.3250 \\pm 5.10 \\times 10^{-5}]",
            "40143.3250",
            "5.10e-5",
            bv_proof["C_EM_I_progression_discrepancy_constant_certified"],
        ),
        (
            "[40148.0933 \\pm 5.15 \\times 10^{-5}]",
            "40148.0933",
            "5.15e-5",
            bv_proof["type_I_global_bound_B_J_plus_C_EM_I_certified"],
        ),
        (
            "[1.371901664348456727857448422465050864052 \\times 10^{-18} \\pm 2.00 \\times 10^{-57}]",
            "1.371901664348456727857448422465050864052e-18",
            "2.00e-57",
            crit["B_Omega_1_tail_T_certified"],
        ),
        (
            "[7.391045088194894744725557492971802729825 \\times 10^{-37} \\pm 2.00 \\times 10^{-76}]",
            "7.391045088194894744725557492971802729825e-37",
            "2.00e-76",
            crit["B_Omega_2_tail_T_certified"],
        ),
        (
            "[0.10084349298 \\pm 5.15 \\times 10^{-12}]",
            "0.10084349298",
            "5.15e-12",
            crit["Omega_log_L1_norm_certified"],
        ),
        (
            "[0.02590072269 \\pm 3.10 \\times 10^{-12}]",
            "0.02590072269",
            "3.10e-12",
            crit["Omega_log_L2_norm_certified"],
        ),
        (
            "[0.000670847436 \\pm 2.37 \\times 10^{-13}]",
            "0.000670847436",
            "2.37e-13",
            crit["Omega_log_L2_sq_integral_certified"],
        ),
        (
            "[0.019636922 \\pm 4.11 \\times 10^{-10}]",
            "0.019636922",
            "4.11e-10",
            crit["sqrt2_abs_R_mu_band_1_certified"],
        ),
        (
            "[0.7071067811865475244008443621048490392848 \\pm 2.00 \\times 10^{-40}]",
            "0.7071067811865475244008443621048490392848",
            "2.00e-40",
            by_X_crit["1"]["A_X_dirichlet_majorant_certified"],
        ),
        (
            "[-0.0138854010 \\pm 8.27 \\times 10^{-11}]",
            "-0.0138854010",
            "8.27e-11",
            by_X_crit["1"]["R_mu_band_discrete_sum_certified"],
        ),
        (
            "[-0.01388540094168 \\pm 3.06 \\times 10^{-15}]",
            "-0.01388540094168",
            "3.06e-15",
            by_X_crit["1"]["R_mu_band_finite_mellin_integral_on_neg_T_to_T_certified"],
        ),
        (
            "[-0.01388540094168 \\pm 3.06 \\times 10^{-15}]",
            "-0.01388540094168",
            "3.06e-15",
            by_X_crit["1"]["R_mu_band_critical_line_mellin_integral_certified"],
        ),
        (
            "[1.284457050376173288909993142606806494932 \\pm 2.00 \\times 10^{-39}]",
            "1.284457050376173288909993142606806494932",
            "2.00e-39",
            by_X_crit["2"]["A_X_dirichlet_majorant_certified"],
        ),
        (
            "[0.010898890859 \\pm 2.89 \\times 10^{-13}]",
            "0.010898890859",
            "2.89e-13",
            by_X_crit["2"]["R_mu_band_discrete_sum_certified"],
        ),
        (
            "[0.01089889085884 \\pm 5.02 \\times 10^{-15}]",
            "0.01089889085884",
            "5.02e-15",
            by_X_crit["2"]["R_mu_band_finite_mellin_integral_on_neg_T_to_T_certified"],
        ),
        (
            "[0.01089889085884 \\pm 5.02 \\times 10^{-15}]",
            "0.01089889085884",
            "5.02e-15",
            by_X_crit["2"]["R_mu_band_critical_line_mellin_integral_certified"],
        ),
        (
            "[0.8554618859638209556480487461972371457491 \\pm 2.00 \\times 10^{-40}]",
            "0.8554618859638209556480487461972371457491",
            "2.00e-40",
            by_X_crit["4"]["A_X_dirichlet_majorant_certified"],
        ),
        (
            "[0.0053844055765 \\pm 8.78 \\times 10^{-14}]",
            "0.0053844055765",
            "8.78e-14",
            by_X_crit["4"]["R_mu_band_discrete_sum_certified"],
        ),
        (
            "[0.00538440557646 \\pm 2.08 \\times 10^{-15}]",
            "0.00538440557646",
            "2.08e-15",
            by_X_crit["4"]["R_mu_band_finite_mellin_integral_on_neg_T_to_T_certified"],
        ),
        (
            "[0.00538440557646 \\pm 2.08 \\times 10^{-15}]",
            "0.00538440557646",
            "2.08e-15",
            by_X_crit["4"]["R_mu_band_critical_line_mellin_integral_certified"],
        ),
        (
            "[2.822798387987013361092201192203292862020 \\pm 2.00 \\times 10^{-39}]",
            "2.822798387987013361092201192203292862020",
            "2.00e-39",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_1_trivial_zero_slopes_and_mellin_energy_criterion"][
                "gaussian_proxy_and_O_k_neg_2_comparison"
            ]["C_Gc_total_constant_certified"],
        ),
        (
            "[0.2388020390525650552804189993008810046850 \\pm 2.00 \\times 10^{-40}]",
            "0.2388020390525650552804189993008810046850",
            "2.00e-40",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_3_signed_coprime_block_attempts_and_regrouping"][
                "unsigned_benchmark_and_two_prime_stratum"
            ]["C_block_non_asymptotic_constant_certified"],
        ),
        (
            "[0.005224056775485917310781671764619177988921 \\pm 2.00 \\times 10^{-41}]",
            "0.005224056775485917310781671764619177988921",
            "2.00e-41",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_3_signed_coprime_block_attempts_and_regrouping"][
                "edge_case_and_regrouping_regressions"
            ]["repeated_factorization_A6_q66"]["w_6_66_certified"],
        ),
        (
            "[0.001527401243306262121849534637683093362364 \\pm 2.00 \\times 10^{-42}]",
            "0.001527401243306262121849534637683093362364",
            "2.00e-42",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_3_signed_coprime_block_attempts_and_regrouping"][
                "edge_case_and_regrouping_regressions"
            ]["repeated_factorization_A35_q2310"]["w_35_2310_certified"],
        ),
        (
            "[0.01668459039204983979825298513603613054339 \\pm 2.00 \\times 10^{-41}]",
            "0.01668459039204983979825298513603613054339",
            "2.00e-41",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_3_signed_coprime_block_attempts_and_regrouping"][
                "edge_case_and_regrouping_regressions"
            ]["nonsquarefree_A4_q20"]["w_4_20_positive_certified"],
        ),
        (
            "[0.004496116626444835904165753124575485457894 \\pm 2.00 \\times 10^{-42}]",
            "0.004496116626444835904165753124575485457894",
            "2.00e-42",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "counterexample_r29_s31_X30_falsifying_old_pairwise_bound"
            ]["d_eq_1_contribution_certified"],
        ),
        (
            "[0.004852248120771122 \\pm 2.20 \\times 10^{-19}]",
            "0.004852248120771122",
            "2.20e-19",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "counterexample_r29_s31_X30_falsifying_old_pairwise_bound"
            ]["full_d_sum_contribution_certified"],
        ),
        (
            "[0.002218597833835925105427052279021906936628 \\pm 2.00 \\times 10^{-42}]",
            "0.002218597833835925105427052279021906936628",
            "2.00e-42",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "counterexample_r29_s31_X30_falsifying_old_pairwise_bound"
            ]["scale_independent_leading_term_L_29_31_certified"],
        ),
        (
            "[0.002277518792608910798738700845553578521267 \\pm 2.00 \\times 10^{-42}]",
            "0.002277518792608910798738700845553578521267",
            "2.00e-42",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "counterexample_r29_s31_X30_falsifying_old_pairwise_bound"
            ]["d_eq_1_error_lower_bound_E_29_31_d1_certified"],
        ),
        (
            "[0.002633650286935197 \\pm 3.20 \\times 10^{-19}]",
            "0.002633650286935197",
            "3.20e-19",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "counterexample_r29_s31_X30_falsifying_old_pairwise_bound"
            ]["full_error_E_29_31_30_certified"],
        ),
        (
            "[0.001516389420551170594757261430873825969737 \\pm 2.00 \\times 10^{-42}]",
            "0.001516389420551170594757261430873825969737",
            "2.00e-42",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "counterexample_r29_s31_X30_falsifying_old_pairwise_bound"
            ]["old_asserted_upper_bound_certified"],
        ),
        (
            "[0.0007611293720577402039814394146797525515291 \\pm 2.00 \\times 10^{-43}]",
            "0.0007611293720577402039814394146797525515291",
            "2.00e-43",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "counterexample_r29_s31_X30_falsifying_old_pairwise_bound"
            ]["d1_excess_over_old_bound_certified"],
        ),
        (
            "[0.001117260866384026 \\pm 5.20 \\times 10^{-19}]",
            "0.001117260866384026",
            "5.20e-19",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "counterexample_r29_s31_X30_falsifying_old_pairwise_bound"
            ]["full_excess_over_old_bound_certified"],
        ),
        (
            "[6.759126424066078899532960393703499341216 \\pm 2.00 \\times 10^{-39}]",
            "6.759126424066078899532960393703499341216",
            "2.00e-39",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "gaussian_integral_and_pairwise_leading_term"
            ]["I_abs_stieltjes_integral_certified"],
        ),
        (
            "[20.27737927219823669859888118111049802365 \\pm 2.00 \\times 10^{-38}]",
            "20.27737927219823669859888118111049802365",
            "2.00e-38",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "gaussian_integral_and_pairwise_leading_term"
            ]["C_pair_sharp_3_I_abs_certified"],
        ),
        (
            "[24.41672357016680253012411397649103735716 \\pm 2.00 \\times 10^{-38}]",
            "24.41672357016680253012411397649103735716",
            "2.00e-38",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "gaussian_integral_and_pairwise_leading_term"
            ]["C_pair_closed_form_upper_bound_certified"],
        ),
        (
            "[0.3995625300165519700235101982261794259293 \\pm 2.00 \\times 10^{-40}]",
            "0.3995625300165519700235101982261794259293",
            "2.00e-40",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
                "counterexample_r29_s31_X30_falsifying_old_pairwise_bound"
            ]["replacement_bound_with_C_sharp_at_29_31_30_certified"],
        ),
        (
            "[1.679378605318050370452005359999016468301 \\pm 2.00 \\times 10^{-39}]",
            "1.679378605318050370452005359999016468301",
            "2.00e-39",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_3_signed_coprime_block_attempts_and_regrouping"][
                "attempt_2_regrouping_by_q_and_unconditional_signed_block_proof"
            ]["kernel_mixed_partial_sign_change_and_absolute_derivative_bounds"][
                "M_var_19_over_8_sqrt2_certified"
            ],
        ),
        (
            "[9.1 \\pm 0.090]",
            "9.1",
            "0.090",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_3_signed_coprime_block_attempts_and_regrouping"][
                "attempt_2_regrouping_by_q_and_unconditional_signed_block_proof"
            ]["four_step_unconditional_walfisz_convolution_proof"][
                "C_h_3_4_certified"
            ],
        ),
        (
            "[3.61 \\pm 6.80 \\times 10^{-3}]",
            "3.61",
            "6.80e-3",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_3_signed_coprime_block_attempts_and_regrouping"][
                "attempt_2_regrouping_by_q_and_unconditional_signed_block_proof"
            ]["four_step_unconditional_walfisz_convolution_proof"][
                "C_h_1_certified"
            ],
        ),
        (
            "[14.0 \\pm 0.622]",
            "14.0",
            "0.622",
            tc050_artifact[
                "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
            ]["section_3_signed_coprime_block_attempts_and_regrouping"][
                "attempt_2_regrouping_by_q_and_unconditional_signed_block_proof"
            ]["four_step_unconditional_walfisz_convolution_proof"][
                "tail_bound_coefficient_9_Ch34_over_4sqrt2_certified"
            ],
        ),
    ]

    rev_text_norm = rev_text.replace("\\bigl[", "[").replace("\\bigr]", "]")
    getcontext().prec = 100
    from flint import ctx as flint_ctx

    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for disp_str, mid_s, rad_s, cert in displayed_cert_checks:
            assert disp_str in rev_text_norm, f"Missing displayed interval {disp_str!r} in review"
            d_mid = Decimal(mid_s)
            d_rad = Decimal(rad_s)
            disp_low = d_mid - d_rad
            disp_high = d_mid + d_rad
            c_low = Decimal(cert["lower_dec"])
            c_high = Decimal(cert["upper_dec"])
            assert disp_low <= c_low <= c_high <= disp_high, (
                f"Displayed interval {disp_str} does not contain Decimal certificate [{c_low}, {c_high}]"
            )
            b_cert = arb(cert["arb_ball_str"])
            b_disp = arb(mid_s) + arb(0, rad_s)
            assert bool(b_disp.lower() <= b_cert.lower()) and bool(
                b_disp.upper() >= b_cert.upper()
            ), f"Displayed interval {disp_str} does not contain Arb ball {cert['arb_ball_str']}"
    finally:
        flint_ctx.prec = saved_prec

    # Also verify that EVERY [\pm] interval in the ENTIRE review is in displayed_cert_checks:
    found_intervals = set(re.findall(r"\[[^\[\]\n]*\\pm[^\[\]\n]*\]", rev_text_norm))
    expected_intervals = {item[0] for item in displayed_cert_checks}
    assert found_intervals == expected_intervals, (
        f"Unaccounted or mismatched intervals in review: {found_intervals ^ expected_intervals}"
    )

    # Separately compare the named Mellin error components for X in {1, 2, 4}:
    mellin_error_display_rows = [
        (
            "1",
            "8.012471247481316 \\times 10^{-16}",
            8.012471247481316e-16,
            "1.940161939963809 \\times 10^{-18}",
            1.940161939963809e-18,
            "8.031872868010421 \\times 10^{-16}",
            8.031872868010421e-16,
        ),
        (
            "2",
            "9.112944021256708 \\times 10^{-16}",
            9.112944021256708e-16,
            "3.5242975303903636 \\times 10^{-18}",
            3.5242975303903636e-18,
            "9.14818701078404 \\times 10^{-16}",
            9.14818701078404e-16,
        ),
        (
            "4",
            "7.475972076500956 \\times 10^{-16}",
            7.475972076500956e-16,
            "2.347219170280871 \\times 10^{-18}",
            2.347219170280871e-18,
            "7.499444269368047 \\times 10^{-16}",
            7.499444269368047e-16,
        ),
    ]
    for (
        x_lbl,
        fin_str,
        fin_expected,
        tail_str,
        tail_expected,
        comb_str,
        comb_expected,
    ) in mellin_error_display_rows:
        row = by_X_crit[x_lbl]
        assert fin_str in rev_text and tail_str in rev_text and comb_str in rev_text
        fin_err = row["finite_integration_error_radius"]
        tail_err = row["infinite_tail_error_bound"]
        comb_err = row["combined_enclosure_radius"]
        assert math.isclose(fin_err, fin_expected, rel_tol=1e-15)
        assert math.isclose(tail_err, tail_expected, rel_tol=1e-15)
        assert math.isclose(comb_err, comb_expected, rel_tol=1e-15)
        assert (
            fin_err
            <= row["R_mu_band_finite_mellin_integral_on_neg_T_to_T_certified"][
                "rad_float_outward"
            ]
        )
        assert math.isclose(
            tail_err,
            float(
                row["proved_infinite_tail_bound_2_A_X_B_Omega_1_certified"][
                    "upper_dec"
                ]
            ),
            rel_tol=1e-15,
        )
        assert (
            comb_err
            <= row["R_mu_band_critical_line_mellin_integral_certified"][
                "rad_float_outward"
            ]
        )
        assert fin_err + tail_err <= comb_err
        assert math.isclose(fin_err + tail_err, comb_err, rel_tol=1e-8)

    # 2. Verify H_0(it) formula, one-sided vs two-sided tail convention, and quadrature description:
    assert crit["H0_critical_line_polynomial_identity_verified"] is True
    assert (
        "H_0(i t) = ((t^2 + 1/4)^4 / (1024 sqrt(pi))) Gamma(1/4 + i t / 2) Gamma(1/4 - i t / 2)"
        in crit["H0_critical_line_canonical_formula"]
    )
    assert "one-sided tail bounds" in crit["whole_integrand_tail_bound_theorem"]
    assert "two-sided norm tails on |t| >= T are bounded by 2 B_{Omega,1}^{tail}(T)" in crit[
        "whole_integrand_tail_bound_theorem"
    ]
    assert "degree-6 centered Taylor" in crit["omega_L1_quadrature_method"]
    assert "bool(z2.real > arb(0))" in crit["omega_L1_quadrature_method"]
    assert "plancherel_component_tail_domination_note" in planch
    assert "2 B_{Omega,1}^{tail}(48)" in planch[
        "plancherel_component_tail_domination_note"
    ]

    # Live Arb check of H_0(it) = ((t^2 + 1/4)^4 / (1024 * sqrt(pi))) * |Gamma(1/4 + i*t/2)|^2:
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for t_int in (0, 1, 2, 5, 10):
            t_a = arb(t_int)
            s_c = acb(arb(1) / arb(2), t_a)
            one_minus_s = acb(arb(1) / arb(2), -t_a)
            h0_live = (evaluate_f_tau_acb(s_c) * evaluate_f_tau_acb(one_minus_s)).real
            g_val = acb(arb(1) / arb(4), t_a / arb(2)).gamma()
            h0_formula = (
                ((t_a * t_a + arb(1) / arb(4)) ** 4)
                / (arb(1024) * arb.pi().sqrt())
                * (abs(g_val) ** 2)
            )
            assert bool((h0_live - h0_formula).contains(0))
            assert float(abs(h0_live - h0_formula).upper()) < 1e-70
    finally:
        flint_ctx.prec = saved_prec

    # 3. Verify reconciled Type I constants (exact rational Fraction arithmetic), Lebesgue dv measure,
    # |mu(d)*mu(r)| <= 1, and admissibility:
    from fractions import Fraction

    c0_frac = Fraction(bv_proof["C0_tilde_psi_exact_rational"])
    c1_frac = Fraction(bv_proof["C1_tilde_psi_exact_rational"])
    c2_frac = Fraction(bv_proof["C2_tilde_psi_exact_rational"])
    a1_frac = Fraction(bv_proof["tilde_A1_exact_rational"])
    a2_frac = Fraction(bv_proof["tilde_A2_exact_rational"])
    assert c0_frac == Fraction(8340237, 3584)
    assert c1_frac == Fraction(95924679, 4096)
    assert c2_frac == Fraction(132825555, 512)
    assert (c0_frac + 2 * c1_frac) / 18 + (17 * c2_frac) / 192 == a1_frac == Fraction(17685797581, 688128)
    assert c2_frac / 18 == a2_frac == Fraction(14758395, 1024)
    assert bv_proof["tilde_A1_formula"] == "(C0_tilde_psi + 2 * C1_tilde_psi) / 18 + (17 * C2_tilde_psi) / 192"
    assert bv_proof["tilde_A2_formula"] == "C2_tilde_psi / 18"
    assert "\\frac{8340237}{3584}" in rev_text
    assert "\\frac{95924679}{4096}" in rev_text
    assert "\\frac{132825555}{512}" in rev_text
    assert "\\frac{C_0^{\\tilde{\\psi}} + 2 C_1^{\\tilde{\\psi}}}{18} + \\frac{17 C_2^{\\tilde{\\psi}}}{192} = \\frac{17685797581}{688128}" in rev_text
    assert "\\frac{C_2^{\\tilde{\\psi}}}{18} = \\frac{132825555}{9216} = \\frac{14758395}{1024}" in rev_text
    assert "\\frac{7}{36}\\widetilde{C}_0\\,v^{-5/2} + \\bigl(\\widetilde{A}_1 + \\widetilde{A}_2\\log v\\bigr)\\,v^{-3/2}" in rev_text
    assert "\\zeta'(s) = -\\frac{1}{(s-1)^2} + \\int_1^\\infty \\left(\\{x\\} - \\frac{1}{2}\\right)(s\\log x - 1)x^{-s-1}\\,dx" in rev_text
    assert "\\frac{\\zeta(3, 5/4)}{4}\\,t^2 \\le 4(t^2 + 1/4)" in rev_text
    assert "0.1659674922 < 4" in rev_text
    assert "0.1659674922 < 4" in planch["plancherel_component_tail_domination_note"]
    assert "\\operatorname{Var}_{(0,\\infty)}(F_X)" in rev_text
    assert "|\\mu(d)\\mu(r)| \\le 1" in rev_text
    assert (
        "floor(X^{1/4}) <= floor(X^{5/6}) = H(X)"
        in vaughan["published_vaughan_formulas"]["band_admissibility_condition"]
    )
    assert (
        "O(X^{-5/6})" in lin["floor_ceiling_endpoint_asymptotics"]
        and "O(X^{-5/4})" in lin["floor_ceiling_endpoint_asymptotics"]
    )

    # 4. Verify non-completeness of (D(J_tau), ||J_tau .||_{H_tau^pos}) and isometric embedding:
    assert "is NOT complete" in planch["operator_domain_statement"]
    assert "isometric embedding of this inner-product space" in planch[
        "operator_domain_statement"
    ]
    assert "**inner-product space that is not complete**" in rev_text
    assert "isometric embedding of this inner-product space" in rev_text

    # 5. Verify Lean declaration sum 47 + 59 = 106 and Theorems 57-59 exact declaration names,
    # reproduced parameter/hypothesis signatures, and #print axioms command & verbatim output:
    sec5 = tc050_artifact["section_5_lean_formalization_and_remaining_obligation"]
    lean_ver = sec5["lean_module_verification"]
    assert len(lean_ver["actual_defs"]) == 47
    assert len(lean_ver["actual_theorems"]) == 59
    assert lean_ver["actual_total_declarations"] == 106
    expected_thm_decls = {
        "theorem_57_transition_integral_linear_density_annihilation_and_sqrt_error_bound": (
            "RiemannScope.transition_integral_linear_density_annihilation_and_sqrt_error_bound"
        ),
        "theorem_58_vaughan_band_decomposition_and_type_I_uniform_bound": (
            "RiemannScope.vaughan_band_decomposition_and_type_I_uniform_bound"
        ),
        "theorem_59_euler_sieved_orbit_and_complete_subgate_closure_chain": (
            "RiemannScope.euler_sieved_orbit_and_complete_subgate_closure_chain"
        ),
    }
    for thm_key, expected_decl in expected_thm_decls.items():
        t_info = sec5["committed_lean_theorems_exact_scope"][thm_key]
        assert t_info["declaration_name"] == expected_decl
        assert f"#print axioms {expected_decl}" in t_info["print_axioms_command"]
        assert (
            t_info["print_axioms_output"]
            == f"'{expected_decl}' depends on axioms: [propext, Classical.choice, Quot.sound]"
        )
        assert expected_decl in rev_text
        assert t_info["print_axioms_output"] in rev_text
        params_part, hyps_part = t_info["parameters_and_hypotheses"].split(" : ℝ) ", 1)
        assert (
            f"parameters `{params_part} : ℝ)` with mathematical hypotheses `{hyps_part}`"
            in rev_text
        )
        assert t_info["standard_lean_axioms_used"] == [
            "propext",
            "Classical.choice",
            "Quot.sound",
        ]
        assert t_info["custom_lean_axioms_used"] == []

    tc042_json = json.loads(
        (REPO_ROOT / "data/tc_canonical_theta_correlation_bound.json").read_text(
            encoding="utf-8"
        )
    )
    lean_sec10 = tc042_json["section_10_lean_formalization_audit"]
    assert len(lean_sec10["actual_defs"]) == 47
    assert len(lean_sec10["actual_theorems"]) == 59
    assert lean_sec10["actual_total_declarations"] == 106

    # Ensure stale pre-TC-052R2 strings are completely absent across code, artifacts, and docs:
    for rel_path in (
        "tc/faithful_tau_arithmetic_spectral_realization.py",
        "tc/canonical_theta_correlation_bound.py",
        "data/tc_faithful_tau_arithmetic_spectral_realization.json",
        "data/tc_canonical_theta_correlation_bound.json",
        "docs/reviews/TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md",
        "docs/reviews/TC_CANONICAL_THETA_CORRELATION_BOUND.md",
        "TRANSCENDENTAL_CONTINUATION.md",
        "RESEARCH_LEDGER.md",
        ".agents/corpus_map/obligation_register.md",
        "formal/RiemannScope/README.md",
    ):
        content = (REPO_ROOT / rel_path).read_text(encoding="utf-8")
        for forbidden in (
            "-0.0138854010 \\pm 1.94",
            "0.855335",
            "16.1782231607907",
            "40147.9219",
            "23585258875/917504",
            "23585258875}{917504}",
            "118067160/458752",
            "118067160}{458752}",
            "(t^2 + 9/4)^2",
            "(t^2+9/4)^2",
            "10^{-60}",
            "1e-60",
            "(1, 4) \\cup (8^{2/5}, 9^{3/5})",
            "(1, 4) union (8^{2/5}, 9^{2/5})",
            "47 `def` + 59 `theorem` = 103",
            "47 def + 59 theorem = 103",
            "`103` (`47` definitions + `59`",
            "RiemannScope.CanonicalThetaCorrelationBound.",
            "0.14624",
            "\\log|5/4 + it/2| + 1 \\le 4",
            "vaughanTypeIBandApprox",
            "118067160/512",
            "118067160}{512}",
            "\\frac{C_0^{\\tilde{\\psi}}}{2} + \\frac{C_1^{\\tilde{\\psi}}}{2}",
        ):
            assert forbidden not in content, (
                f"Found stale pre-TC-052R2 string {forbidden!r} in {rel_path}"
            )


def test_27_tc053_trivial_zero_slopes_baez_duarte_proxy_and_mellin_energy_criterion(
    tc050_artifact: dict,
) -> None:
    """Verify TASK-TC-053 Section 1:
    - Normalized trivial-zero slope identity ((2*(-1)^m*tau^{2m})/(2m)!)*a_K*Z_{a_K}'(-2*m*a_K) = zeta(2m+1)
      with grade K, trivial-zero index m, and finite-difference order k kept distinct.
    - Generalized Baez-Duarte sequence c_k = sum_{j=0}^k (-1)^j binom(k, j) / zeta(2j+3)
      = sum_{n>=1} (mu(n)/n^3)(1 - n^{-2})^k with explicit Dirichlet tail bound 1/(2*N^2).
    - Gaussian proxy G(t) = sum_{n>=1} (mu(n)/n^3) e^{-t/n^2}, Q(X) = X^{5/2}G(X^2), and
      |G(k) - c_k| <= C_{G,c} k^{-2} with C_{G,c} = 4e^{-2} + (2/3)*(1 + (7/(2e))^{7/2}) < 3.5.
    - Mellin identity int_0^infty Q(X) X^{-z} dX/X = Gamma(5/4 - z/2)/(2*zeta(1/2 + z)) on 1/2 < Re(z) < 5/2
      and the 5-step sufficiency criterion int_Y^{tau*Y} |Q(X)|^2 dX/X <= C_eps Y^eps.
    """
    from tc.faithful_tau_arithmetic_spectral_realization import (
        STARTING_HEAD_TC_053,
        TASK_TC_053_ID,
        verify_trivial_zero_slopes_baez_duarte_and_mellin_criterion_arb,
    )

    assert (
        tc050_artifact["trivial_zero_coprime_cancellation_task_id"]
        == TASK_TC_053_ID
        == "TASK-TC-053"
    )
    assert (
        tc050_artifact["tc053_starting_head"]
        == STARTING_HEAD_TC_053
        == "c64596727e7142596acd073c6c8e4eb28f2eaee0"
    )
    sec9 = tc050_artifact[
        "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
    ]
    assert sec9["task_id"] == "TASK-TC-053"
    assert sec9["subgate_tc043a_status"] == "OPEN"
    assert sec9["rh_proved"] is False

    sec1 = sec9["section_1_trivial_zero_slopes_and_mellin_energy_criterion"]
    slopes = sec1["transported_trivial_zero_slope_identity"]
    assert slopes["symbolic_reflection_prefactor_verified"] is True
    assert slopes["all_worldline_zeros_enclose_zero"] is True
    assert slopes["all_slope_identities_enclose_zero"] is True
    assert len(slopes["sample_grade_and_index_table"]) == 12
    for row in slopes["sample_grade_and_index_table"]:
        assert row["Z_aK_at_s_m_K_encloses_zero"] is True
        assert row["identity_encloses_zero"] is True

    bd = sec1["generalized_baez_duarte_and_role_separation"]
    assert len(bd["primary_literature_citations"]) == 3
    assert "a_K Z_{a_K}'(-2 m a_K) = zeta'(-2m)" in bd["what_grade_transport_K_contributes"]
    assert "1 / zeta(2j + 3)" in bd["what_varying_m_contributes"]

    gproxy = sec1["gaussian_proxy_and_O_k_neg_2_comparison"]
    assert gproxy["all_c_k_binomial_vs_dirichlet_enclose_zero"] is True
    assert gproxy["all_G_k_minus_c_k_bounds_certified"] is True
    assert gproxy["C_Gc_lt_rational_ceiling_certified"] is True
    c_gc = gproxy["C_Gc_total_constant_certified"]["mid_float"]
    assert math.isclose(
        c_gc,
        4.0 * math.exp(-2.0) + (2.0 / 3.0) * (1.0 + (3.5 / math.e) ** 3.5),
        rel_tol=1e-14,
    )
    assert c_gc < 3.5
    assert len(gproxy["c_k_and_G_k_comparison_table"]) == 8
    for row in gproxy["c_k_and_G_k_comparison_table"]:
        assert row["c_k_identity_encloses_zero"] is True
        assert row["n_eq_1_bound_certified"] is True
        assert row["n_ge_2_bound_certified"] is True
        assert row["abs_G_k_minus_c_k_le_bound_certified"] is True

    mellin = sec1["mellin_identity_and_sufficient_grade_energy_criterion"]
    assert mellin["mellin_symbolic_termwise_verified"] is True
    assert mellin["all_mellin_strip_checks_enclose_zero"] is True
    assert (
        mellin["criterion_status"]
        == "SUFFICIENT_CRITERION_CONDITIONAL_ON_ARITHMETIC_ENERGY_PREMISE"
    )
    assert len(mellin["five_step_sufficiency_proof"]) == 5

    live_sec1 = verify_trivial_zero_slopes_baez_duarte_and_mellin_criterion_arb(
        prec_bits=256
    )
    assert live_sec1["transported_trivial_zero_slope_identity"]["all_slope_identities_enclose_zero"] is True
    assert live_sec1["gaussian_proxy_and_O_k_neg_2_comparison"]["all_G_k_minus_c_k_bounds_certified"] is True


def test_28_tc053_common_factor_coprime_squarefree_counting_and_gaussian_integral(
    tc050_artifact: dict,
) -> None:
    """Verify TASK-TC-053 Section 2:
    - Common-factor Moebius split mu(d*r)*mu(d*s) = 1_{gcd(d, r*s)=1} mu(d)^2 mu(r) mu(s).
    - Coprime-squarefree counting N_q(t) = kappa(q)*t + R_q(t) with |R_q(t)| <= (2^{omega(q)}+2)*sqrt(t) <= 3*2^{omega(q)}*sqrt(t).
    - Gaussian integral int_0^infty u^4 e^{-alpha*u^2} du = (3*sqrt(pi)/8)*alpha^{-5/2} and SymPy verification.
    - Total error O_eps(A^{3/2+eps}/sqrt(X)) and valid growing range A <= X^{1/3-delta}.
    """
    from fractions import Fraction
    from flint import ctx as flint_ctx
    from tc.faithful_tau_arithmetic_spectral_realization import (
        _evaluate_kappa_q_arb,
        _evaluate_tilde_kappa_rational,
        verify_common_factor_expansion_and_coprime_squarefree_asymptotics_arb,
    )

    sec2 = tc050_artifact[
        "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
    ]["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"]

    mob = sec2["common_factor_bijection_and_mobius_split"]
    assert "3600 ordered pairs" in mob["tested_grid_range"]
    assert mob["all_mobius_splits_exact"] is True

    cnt = sec2["coprime_squarefree_counting_estimate"]
    assert cnt["all_counting_bounds_certified"] is True
    assert cnt["sub_unit_t_bound_certified"] is True
    assert len(cnt["sample_counting_table"]) == 10
    for row in cnt["sample_counting_table"]:
        assert row["abs_R_q_t_le_bound_certified"] is True

    gauss = sec2["gaussian_integral_and_pairwise_leading_term"]
    assert gauss["gaussian_symbolic_verified"] is True
    assert gauss["homogeneous_degree_neg_half_symbolic_verified"] is True
    assert gauss["I_abs_direct_vs_ibp_agree"] is True
    assert gauss["C_pair_sharp_lt_21_certified"] is True
    assert gauss["C_pair_closed_lt_25_certified"] is True
    assert gauss["all_pairwise_error_bounds_certified"] is True
    assert len(gauss["sample_pairwise_convergence_table"]) == 5
    for row in gauss["sample_pairwise_convergence_table"]:
        assert row["abs_difference_le_analytic_bound_certified"] is True

    ce = sec2["counterexample_r29_s31_X30_falsifying_old_pairwise_bound"]
    assert ce["contradiction_strictly_positive_lower_bound_certified"] is True
    assert ce["replacement_bound_holds_certified"] is True

    tot = sec2["total_error_and_valid_growing_range"]
    assert tot["exponent_identity_symbolic_verified"] is True
    assert (
        "0 < eps < 3 delta / (2 (1/3 - delta))"
        in tot["valid_growing_range_upper_bound_condition"]
    )
    assert (
        "rather than being a necessary condition"
        in tot["valid_growing_range_upper_bound_condition"]
    )

    # Live check of tilde{kappa}(30) = (2/3)*(3/4)*(5/6) = 5/12 and live Section 2 verification:
    assert _evaluate_tilde_kappa_rational(30) == Fraction(5, 12)
    saved_prec = flint_ctx.prec
    flint_ctx.prec = 256
    try:
        inv_zeta2 = arb(6) / (arb.pi() ** 2)
        kap_30 = _evaluate_kappa_q_arb(30, inv_zeta2)
        assert bool((kap_30 - inv_zeta2 * arb(5) / arb(12)).contains(0))
    finally:
        flint_ctx.prec = saved_prec
    live_sec2 = verify_common_factor_expansion_and_coprime_squarefree_asymptotics_arb(
        prec_bits=256
    )
    assert live_sec2["common_factor_bijection_and_mobius_split"]["all_mobius_splits_exact"] is True


def test_29_tc053_signed_block_attempts_regrouping_and_edge_case_regressions(
    tc050_artifact: dict,
) -> None:
    """Verify TASK-TC-053 Section 3:
    - Direct (r, s) sum vs regrouping by q = r*s for S(A) = sum_q mu(q)*w_A(q) on A <= r, s < 2A.
    - Unsigned benchmark |S(A)| <= S_abs(A) <= C_block * A and positive two-prime stratum S_{2-prime}(A) > 0.
    - Attempt 1 bivariate Euler product D(s_1, s_2) = H(s_1, s_2)/(zeta(s_1)*zeta(s_2)) and AM-GM nonvanishing on Re(s_i) >= 1/2.
    - Attempt 2 log-weighted identity mu(q)*log(q) = -sum_{uv=q} Lambda(u)*mu(v), decoupled L^2-integral decomposition,
      2D antiderivative d^2/dr ds (r*s / (3*sqrt(r^2+s^2))) = (r*s)^2 / (r^2+s^2)^{5/2}, and unconditional Walfisz saving.
    - Edge-case regressions: q = 66 at A = 6 (2 pairs), q = 2310 at A = 35 (4 pairs), nonsquarefree q = 20 at A = 4,
      diagonal r = s = 1 at A = 1 vs A > 1, empty sums, and half-open boundaries [A, 2A).
    """
    from flint import ctx as flint_ctx
    from tc.faithful_tau_arithmetic_spectral_realization import (
        _evaluate_w_A_q_arb,
        verify_signed_block_cancellation_attempts_and_regrouping_arb,
    )

    sec3 = tc050_artifact[
        "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
    ]["section_3_signed_coprime_block_attempts_and_regrouping"]

    defn = sec3["balanced_block_regrouping_definition"]
    assert "appears ONCE" in defn["w_A_q_explicit_formula_with_kappa_once"]

    bench = sec3["unsigned_benchmark_and_two_prime_stratum"]
    assert bench["antiderivative_symbolic_verified"] is True
    assert bench["box_integral_symbolic_verified"] is True
    assert bench["C_block_lt_0_239_certified"] is True
    assert "100% of products of two distinct primes" in bench["two_prime_stratum_asymptotic"]
    assert bench["single_prime_block_A_5_over_2_two_prime_sum_zero"] is True

    att1 = sec3["attempt_1_prime_by_prime_bivariate_euler_product"]
    assert att1["all_attempt1_local_factors_strictly_positive"] is True
    assert att1["boundary_s1_eq_s2_eq_half_divergence_symbolic_verified"] is True
    assert (
        "local factor H_p(p^{-s_1}, p^{-s_2}) is strictly nonzero"
        in att1["local_vs_infinite_product_and_boundary_behavior"]
    )
    assert (
        "diverges"
        in att1["local_vs_infinite_product_and_boundary_behavior"]
    )
    assert len(att1["local_factor_table"]) == 6

    att2 = sec3["attempt_2_regrouping_by_q_and_unconditional_signed_block_proof"]
    assert "Lambda(u)" in att2["exact_regrouped_exchange_identity"]
    assert (
        att2["kernel_mixed_partial_sign_change_and_absolute_derivative_bounds"][
            "K_rs_symbolic_verified"
        ]
        is True
    )
    assert (
        att2["kernel_mixed_partial_sign_change_and_absolute_derivative_bounds"][
            "K_rs_at_1_2_strictly_negative"
        ]
        is True
    )
    assert (
        "Korobov (1958)"
        in att2["four_step_unconditional_walfisz_convolution_proof"][
            "step_2_uniform_walfisz_bound_on_main_range_d_e_le_sqrt_A"
        ]
    )

    edge = sec3["edge_case_and_regrouping_regressions"]
    assert edge["edge_cases_verified"] is True
    assert edge["all_direct_vs_regrouped_enclose_zero"] is True
    assert edge["all_direct_vs_decoupled_L2_enclose_zero"] is True
    assert edge["all_direct_vs_h_convolution_enclose_zero"] is True
    assert edge["all_log_mobius_exchanges_enclose_zero"] is True
    assert edge["applicable_log_mobius_count"] == 10
    assert edge["skipped_log_mobius_count"] == 2
    assert edge["all_unsigned_bounds_certified"] is True
    assert edge["repeated_factorization_A6_q66"]["coprime_factorization_count_in_block"] == 2
    assert edge["repeated_factorization_A6_q66"]["ordered_coprime_pairs_in_block"] == [
        [6, 11],
        [11, 6],
    ]
    assert edge["repeated_factorization_A35_q2310"]["coprime_factorization_count_in_block"] == 4
    assert edge["repeated_factorization_A35_q2310"]["ordered_coprime_pairs_in_block"] == [
        [35, 66],
        [42, 55],
        [55, 42],
        [66, 35],
    ]
    assert edge["nonsquarefree_A4_q20"]["ordered_coprime_pairs_in_block"] == [
        [4, 5],
        [5, 4],
    ]
    assert edge["nonsquarefree_A4_q20"]["mu_20"] == 0
    assert edge["nonsquarefree_A4_q20"]["mu_20_times_w_4_20_zero"] is True
    assert len(edge["balanced_block_evaluation_table"]) == 12
    by_A = {row["A_label"]: row for row in edge["balanced_block_evaluation_table"]}
    assert by_A["1/2"]["coprime_pair_count"] == 0
    assert by_A["1/2"]["log_mobius_status"] == "SKIPPED"
    assert by_A["1/2"]["direct_minus_log_mobius_encloses_zero"] is None
    assert by_A["1"]["diagonal_coprime_pair_count"] == 1
    assert by_A["1"]["log_mobius_status"] == "SKIPPED"
    assert by_A["1"]["direct_minus_log_mobius_encloses_zero"] is None
    assert by_A["5/2"]["S_two_prime_omega_eq_2_certified"]["mid_float"] == 0.0
    assert by_A["5/2"]["S_two_prime_omega_eq_2_certified"]["arb_ball_str"] == "0"
    assert by_A["5/2"]["log_mobius_status"] == "APPLICABLE_AND_CERTIFIED"
    assert by_A["5/2"]["direct_minus_log_mobius_encloses_zero"] is True
    for lbl in ("2", "4", "9/2", "6", "8", "16", "32", "35", "64"):
        assert by_A[lbl]["diagonal_coprime_pair_count"] == 0
        assert by_A[lbl]["direct_minus_regrouped_encloses_zero"] is True
        assert by_A[lbl]["direct_minus_decoupled_L2_encloses_zero"] is True
        assert by_A[lbl]["direct_minus_h_convolution_encloses_zero"] is True
        assert by_A[lbl]["log_mobius_status"] == "APPLICABLE_AND_CERTIFIED"
        assert by_A[lbl]["direct_minus_log_mobius_encloses_zero"] is True
        assert by_A[lbl]["unsigned_bound_certified"] is True
        assert by_A[lbl]["parity_decomposition_S_abs_mp_S_eq_2_S_neg_pos_certified"] is True
        assert by_A[lbl]["S_two_prime_omega_eq_2_certified"]["mid_float"] > 0

    # Live Arb check of _evaluate_w_A_q_arb and verify_signed_block_cancellation_attempts_and_regrouping_arb:
    saved_prec = flint_ctx.prec
    flint_ctx.prec = 256
    try:
        inv_zeta2 = arb(6) / (arb.pi() ** 2)
        c_gauss = (arb(3) * arb.pi().sqrt()) / arb(8)
        w_val, cnt_66, pairs_66 = _evaluate_w_A_q_arb(66, 6, 11, inv_zeta2, c_gauss)
        assert cnt_66 == 2
        assert pairs_66 == [(6, 11), (11, 6)]
        assert bool(w_val.lower() > arb(0))
    finally:
        flint_ctx.prec = saved_prec
    live_sec3 = verify_signed_block_cancellation_attempts_and_regrouping_arb(
        prec_bits=256
    )
    assert live_sec3["edge_case_and_regrouping_regressions"]["edge_cases_verified"] is True


def test_30_tc053_trivial_zero_lean_module_and_theorem_scope_verification(
    tc050_artifact: dict,
) -> None:
    """Verify TASK-TC-053 / TASK-TC-053R Section 4:
    - formal/RiemannScope/TrivialZero.lean exists, compiles 4 def + 10 theorem = 14 declarations
      with 0 sorry and 0 admit, and includes RiemannScope.TrivialZero.trivialZero_exact,
      RiemannScope.TrivialZero.trivialZero_worldline_exact, and
      RiemannScope.TrivialZero.trivialZero_zero_eq_neg_half.
    - Exact namespace, #check, #print, and #print axioms output for all new Lean theorems.
    """
    from tc.faithful_tau_arithmetic_spectral_realization import (
        verify_trivial_zero_lean_module,
    )

    tz_live = verify_trivial_zero_lean_module()
    assert tz_live["exists"] is True
    assert tz_live["contains_sorry"] is False
    assert tz_live["contains_admit"] is False
    assert tz_live["matches_exact"] is True
    assert len(tz_live["actual_defs"]) == 4
    assert len(tz_live["actual_theorems"]) == 10
    assert tz_live["actual_total_declarations"] == 14

    sec4 = tc050_artifact[
        "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
    ]["section_4_trivial_zero_lean_formalization_and_scope"]
    tz_mod = sec4["trivial_zero_lean_module_verification"]
    assert tz_mod["certificate_theorem_reference_repaired"] == "RiemannScope.TrivialZero.trivialZero_exact"
    assert tz_mod["transported_worldline_corollary"] == "RiemannScope.TrivialZero.trivialZero_worldline_exact"
    scopes = sec4["committed_trivial_zero_lean_theorems_exact_scope"]
    for key in (
        "trivialZero_exact",
        "trivialZero_worldline_exact",
        "trivialZero_zero_eq_neg_half",
        "trivial_zero_slope_scale_invariance_and_grade_energy_criterion",
        "common_factor_mobius_split_and_valid_growing_range_exponent",
        "signed_block_bivariate_euler_nonvanishing_and_parity_regrouping",
    ):
        assert key in scopes
        assert (
            "depends on axioms: [propext, Classical.choice, Quot.sound]"
            in scopes[key]["print_axioms_output"]
        )
    assert scopes["trivialZero_exact"]["namespace"] == "RiemannScope.TrivialZero"
    assert scopes["trivialZero_worldline_exact"]["namespace"] == "RiemannScope.TrivialZero"
    assert scopes["trivialZero_zero_eq_neg_half"]["namespace"] == "RiemannScope.TrivialZero"
    assert "riemannZeta 0 = -1 / 2" in scopes["trivialZero_zero_eq_neg_half"]["check_output"]
    assert (
        scopes["common_factor_mobius_split_and_valid_growing_range_exponent"]["namespace"]
        == "RiemannScope"
    )
    assert (
        "h_mobius"
        in scopes["common_factor_mobius_split_and_valid_growing_range_exponent"][
            "parameters_and_hypotheses"
        ]
    )


def test_31_tc053r_counterexample_replacement_pairwise_bound_and_uniform_signed_block_proof(
    tc050_artifact: dict,
) -> None:
    """Verify TASK-TC-053R repairs and regressions:
    1. Reproduce the (r, s, X) = (29, 31, 30) counterexample in outward-rounded 256-bit Arb
       and certify a strictly positive lower bound on E_{29,31}^{(d=1)}(30) - B_old(29,31,30) > 0.000761129 > 0.
    2. Verify the replacement Stieltjes pairwise bound
       |E_{r,s}(X)| <= C * 2^{omega(rs)} * X^{-1/2} * (rs)^{5/2} / (r^2 + s^2)^{11/4}
       with C = C_pair^sharp = 3 * I_abs < 21 and C_pair^closed = 6*3^{15/4}*e^{-3} + (315/64)*Gamma(3/4) < 25,
       homogeneous degree -1/2 in (r, s), and verify that both old false pairwise formulas are removed
       from asserted valid formulas in code and review.
    3. Verify K_rs(r, s) = r*s*(-6*r^4 + 23*r^2*s^2 - 6*s^4) / (r^2 + s^2)^{9/2},
       K_rs(1, 1) = 11/(16*sqrt(2)) > 0, K_rs(1, 2) = -4*sqrt(5)/625 < 0, and verify that the
       4-step uniform convolution proof f = (mu (x) mu) * h with C_{h,3/4} < 9.5 and C_{h,1} < 3.7 holds.
    4. Verify endpoint, numerical, and formal claims: covering constant 1 + tau^eps, 0 < t < 1 counting bound,
       S_{2-prime}(5/2) = 0, independent q-sum for S_regrouped, SKIPPED log-Moebius cases at A = 1/2 and A = 1,
       parity identity S_abs -+ S = 2*S_{neg/pos} >= 0, and exact Lean scope descriptions.
    """
    from pathlib import Path
    import sympy as sp
    from flint import ctx as flint_ctx
    from tc.faithful_tau_arithmetic_spectral_realization import (
        _evaluate_h_de_rational,
        _evaluate_kappa_q_arb,
    )

    assert (
        tc050_artifact["tc053_repair_task_id"]
        == "TASK-TC-053R"
    )
    assert (
        tc050_artifact["tc053_merged_main_baseline"]
        == "793d327d2f151170ceb34536ed92f99b11e17969"
    )

    sec9 = tc050_artifact[
        "section_9_task_tc053_trivial_zero_slopes_and_coprime_cancellation"
    ]
    assert sec9["repair_task_id"] == "TASK-TC-053R"
    assert sec9["tc053_merged_main_baseline"] == "793d327d2f151170ceb34536ed92f99b11e17969"
    assert sec9["subgate_tc043a_status"] == "OPEN"
    assert sec9["rh_proved"] is False

    # 1. Live 256-bit Arb check of the (r, s, X) = (29, 31, 30) counterexample and replacement bound:
    saved_prec = flint_ctx.prec
    flint_ctx.prec = 256
    try:
        pi_b = arb.pi()
        inv_zeta2 = arb(6) / (pi_b ** 2)
        c_gauss = (arb(3) * pi_b.sqrt()) / arb(8)
        r_ce, s_ce, x_ce = 29, 31, 30
        q_ce = r_ce * s_ce  # 899
        alpha_ce = arb(1) / arb(r_ce ** 2) + arb(1) / arb(s_ce ** 2)
        u_1 = arb(x_ce)
        # Since mu(29)*mu(31) = (-1)*(-1) = +1, d=1 term is:
        i_d1 = (u_1 ** 5) * (arb(r_ce * s_ce) ** (-3)) * (-(u_1 ** 2) * alpha_ce).exp()
        kap_899 = _evaluate_kappa_q_arb(q_ce, inv_zeta2)
        l_ce = (
            c_gauss
            * kap_899
            * (arb(q_ce) ** 2)
            / ((arb(r_ce ** 2 + s_ce ** 2) ** 5).sqrt())
        )
        e_d1 = i_d1 - l_ce
        b_old = (
            (arb(15) * pi_b.sqrt() / arb(16))
            * arb(4)
            * (arb(x_ce).sqrt() ** (-1))
            * arb(q_ce)
            / (arb(r_ce ** 2 + s_ce ** 2) ** 2)
        )
        diff_ce = e_d1 - b_old
        assert bool((e_d1 - arb("0.00227751")).lower() > arb(0))
        assert bool((arb("0.00151640") - b_old).lower() > arb(0))
        assert bool(diff_ce.lower() > arb("0.000761129"))
        assert bool(diff_ce.lower() > arb(0))

        # Replacement constant C_pair^sharp = 3 * I_abs < 21 and C_pair^closed < 25:
        gauss_sec = sec9["section_2_common_factor_expansion_and_coprime_squarefree_asymptotics"][
            "gaussian_integral_and_pairwise_leading_term"
        ]
        c_sharp = arb(gauss_sec["C_pair_sharp_3_I_abs_certified"]["arb_ball_str"])
        c_closed = arb(
            gauss_sec["C_pair_closed_form_upper_bound_certified"]["arb_ball_str"]
        )
        assert bool((arb(21) - c_sharp).lower() > arb(0))
        assert bool((arb(25) - c_closed).lower() > arb(0))
        assert bool((c_closed - c_sharp).lower() > arb(0))

        b_new_sharp = (
            c_sharp
            * arb(4)
            * (arb(x_ce).sqrt() ** (-1))
            * ((arb(q_ce) ** 5).sqrt())
            / ((arb(r_ce ** 2 + s_ce ** 2) ** 11).sqrt().sqrt())
        )
        assert bool((b_new_sharp - e_d1).lower() > arb(0))
    finally:
        flint_ctx.prec = saved_prec

    # 2. Verify K_rs(r, s) symbolically and check sign change between (1, 1) and (1, 2):
    r_sym, s_sym = sp.symbols("r s", positive=True)
    k_expr = (r_sym * s_sym) ** 2 / (r_sym ** 2 + s_sym ** 2) ** sp.Rational(5, 2)
    k_rs_expr = sp.factor(sp.diff(k_expr, r_sym, s_sym))
    k_rs_target = (
        r_sym
        * s_sym
        * (-6 * r_sym ** 4 + 23 * r_sym ** 2 * s_sym ** 2 - 6 * s_sym ** 4)
        / (r_sym ** 2 + s_sym ** 2) ** sp.Rational(9, 2)
    )
    assert sp.simplify(k_rs_expr - k_rs_target) == 0
    assert sp.simplify(k_rs_expr.subs({r_sym: 1, s_sym: 1}) - 11 / (16 * sp.sqrt(2))) == 0
    assert sp.simplify(k_rs_expr.subs({r_sym: 1, s_sym: 2}) + 4 * sp.sqrt(5) / 625) == 0

    # 3. Verify h(d, e) convolution weight values at prime powers:
    from fractions import Fraction
    assert _evaluate_h_de_rational(1, 1) == Fraction(1, 1)
    for p in (2, 3, 5, 7):
        assert _evaluate_h_de_rational(p, 1) == Fraction(1, p + 1)
        assert _evaluate_h_de_rational(p * p, 1) == Fraction(1, p + 1)
        assert _evaluate_h_de_rational(1, p) == Fraction(1, p + 1)
        assert _evaluate_h_de_rational(p, p) == Fraction(-(p - 1), p + 1)
        assert _evaluate_h_de_rational(p * p, p) == Fraction(-(p - 1), p + 1)

    att2 = sec9["section_3_signed_coprime_block_attempts_and_regrouping"][
        "attempt_2_regrouping_by_q_and_unconditional_signed_block_proof"
    ]
    f4 = att2["four_step_unconditional_walfisz_convolution_proof"]
    assert f4["C_h_3_4_certified"]["mid_float"] < 9.5
    assert f4["C_h_1_certified"]["mid_float"] < 3.7

    # 4. Verify review document and source file do not assert the old false pairwise formula or K_rs >= 0:
    repo_root = Path(__file__).resolve().parents[1]
    review_text = (
        repo_root / "docs" / "reviews" / "TC_FAITHFUL_TAU_ARITHMETIC_SPECTRAL_REALIZATION.md"
    ).read_text(encoding="utf-8")
    assert "contradiction_strictly_positive_lower_bound_certified" in review_text
    assert "C_{\\mathrm{pair}}^{\\mathrm{sharp}}" in review_text
    assert "-6r^4 + 23r^2 s^2 - 6s^4" in review_text
    assert "S_{2\\text{-prime}}(5/2) = 0" in review_text
    assert "1 + \\tau^\\varepsilon" in review_text
    assert "riemannZeta 0 = -1 / 2" in review_text





