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
    assert sec6["total_certified_arb_balls_checked"] == 798
    assert sec6["compared_against_live_original_arb_count"] == 798
    assert sec6["live_original_count_matches_enumerated_total"] is True
    assert sec6["all_enclose_original_256bit_arb_ball"] is True
    assert sec6["failed_paths"] == []

    # Re-enumerate the deserialized JSON tree and confirm exact ball count match:
    rt_recheck = verify_all_serialized_arb_in_tree(
        tc050_artifact, path_prefix="task_tc050"
    )
    assert rt_recheck["total_certified_arb_balls_checked"] == 798
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
    """Verify TASK-TC-052 Approach A: Mellin vanishing moments of W_log and tilde{W}_log,
    two-endpoint asymptotic limits for J_band(X), R_{1,band}(X), and R_{|mu|,band}(X),
    rescaled transition-integral identity, Landau's Moebius harmonic bound, and Vaughan
    band decomposition R_{mu,band}(X) = R_I(X; U, V) + R_{II}(X; U, V)."""
    assert tc050_artifact["subgate_closure_attempt_task_id"] == "TASK-TC-052"
    assert (
        tc050_artifact["tc052_starting_head"]
        == "1f576944c040d5b3a2bf8091ca803e3758c80d12"
    )
    assert tc050_artifact["subgate_tc043a_status"] == "OPEN"
    assert tc050_artifact["rh_proved"] is False

    sec8 = tc050_artifact[
        "section_8_task_tc052_transition_cancellation_and_spectral_dirichlet_factorization"
    ]
    assert sec8["task_id"] == "TASK-TC-052"
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

    lin = app_a["linear_density_annihilation_and_exact_limits"]
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

    resc = app_a["rescaled_transition_integral_verification"]
    assert resc["all_rescaled_identities_enclose_zero"] is True
    assert len(resc["rescaled_integral_table"]) == 8
    for row in resc["rescaled_integral_table"]:
        assert row["difference_encloses_zero"] is True

    vaughan = app_a["vaughan_band_decomposition_and_type_I_audit"]
    assert vaughan["landau_moebius_harmonic_bound_verified_up_to_200"] is True
    assert vaughan["max_abs_sum_mu_d_over_d_up_to_200_exact"] == "1/1"
    assert vaughan["all_vaughan_identities_enclose_zero"] is True
    assert len(vaughan["vaughan_band_table"]) == 8
    for row in vaughan["vaughan_band_table"]:
        assert row["UV_le_sqrt_X"] is True
        assert row["pointwise_coeff_identity_mu_eq_cI_plus_cII"] is True
        assert row["vaughan_sum_difference_encloses_zero"] is True
        assert row["type_I_exchange_difference_encloses_zero"] is True


def test_24_tc052_euler_sieved_orbit_critical_line_mellin_and_closure_chain(
    tc050_artifact: dict,
) -> None:
    """Verify TASK-TC-052 Approach B (operator intertwining on H_tau^pos, critical-line
    Mellin representation of R_{mu,band}(X), and low-frequency Euler spike lower bound),
    the complete conditional closure chain, and Lean Theorems 57-59."""
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

    crit = app_b["critical_line_spectral_dirichlet_factorization"]
    assert crit["all_crit_line_identities_enclose_zero"] is True
    assert len(crit["critical_line_verification_table"]) == 3
    for row in crit["critical_line_verification_table"]:
        assert row["difference_encloses_zero"] is True

    spike = app_b["low_frequency_euler_spike_obstruction_on_H_tau_pos"]
    assert math.isclose(
        spike["mu_arch_B_at_0_certified"]["mid_float"], 2.0, abs_tol=1e-15
    )
    assert float(spike["mu_arch_B_at_0_certified"]["lower_dec"]) > 1.999999999999999
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
    scopes = sec5["committed_lean_theorems_exact_scope"]
    for thm_key in (
        "theorem_57_transition_integral_linear_density_annihilation_and_sqrt_error_bound",
        "theorem_58_vaughan_band_decomposition_and_type_I_uniform_bound",
        "theorem_59_euler_sieved_orbit_and_complete_subgate_closure_chain",
    ):
        assert thm_key in scopes

