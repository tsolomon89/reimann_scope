"""
Unit and verification tests for `TASK-TC-037`:
Bigraded Character Projection, Reflection-Sector Isolation, and Transport-Compatibility Audit.
"""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path

from tc.grade_character_projection import (
    COMMON_SHIFT_PROJECTION_TRANSPORT_INCOMPATIBILITY,
    CONTINUOUS_GRADE_HAAR_PROJECTION_REQUIRES_UNITARY_CHARACTERS,
    FINITE_GRADE_LAURENT_PROJECTOR_NO_GO,
    FINITE_ORDER_GRADE_DIFFERENTIAL_PROJECTOR_NO_GO,
    GRADE_CHARACTER_PROJECTION_DOES_NOT_ESCAPE_TRANSPORT_MOMENT_INCOMPATIBILITY,
    GRADE_ORTHOGONALITY_OUTSIDE_UNITARY_AXIS_IS_DISGUISED_RH_PREMISE,
    LOG_TAU,
    OFF_CRITICAL_NONUNITARITY_BLOCKS_GRADE_HAAR_PROJECTION,
    PERMITTED_PRINCIPAL_OUTCOMES,
    PRINCIPAL_CLASSIFICATION,
    REFLECTION_PAIR_STATIONARY_FOR_SESQUILINEAR_CORRELATION,
    REFLECTION_PROJECTION_HAS_NO_ARITHMETIC_SIGN_CONTRADICTION,
    REQUIRED_LEAN_THEOREMS,
    SCALE_INVARIANT_ARITHMETIC_KERNEL_ERASES_COMMON_GRADE_CHARACTER,
    TAU,
    ZERO_DEPENDENT_GRADE_FILTER_REJECTED,
    audit_arithmetic_contradiction_gate,
    audit_common_shift_transport_compatibility,
    audit_complex_grade_loophole,
    audit_finite_differential_projector_no_go,
    audit_finite_laurent_projector_no_go,
    audit_generic_base_grade_projection_control,
    audit_inversion_even_state_control,
    audit_offcritical_diagonal_obstruction,
    audit_pontryagin_duality_firewall,
    audit_reflection_quartet_radial_identity,
    audit_relative_grade_alternative,
    audit_scale_invariant_ratio_kernel,
    audit_zero_dependent_filter_firewall,
    audit_zero_symmetry_group,
    build_grade_character_projection_report,
    check_reflection_stationarity,
    classify_second_leg_involutions,
    derive_grade_character_convention,
    evaluate_abel_poisson_average,
    evaluate_centered_zero_symmetries,
    evaluate_common_and_relative_grade_coordinates,
    evaluate_continuous_cesaro_average,
    evaluate_discrete_cesaro_average,
    evaluate_finite_differential_projector,
    evaluate_finite_laurent_projector,
    evaluate_gaussian_grade_average,
    evaluate_grade_character,
    evaluate_inversion_even_state_mellin,
    evaluate_reflection_quartet_polynomial,
    verify_lean_theorem_identifiers,
)


def test_01_zero_symmetry_table() -> None:
    """1. Zero symmetry table distinguishes I, C, F, R in uncentered and centered coordinates."""
    audit = audit_zero_symmetry_group()
    table = {row["symmetry"]: row for row in audit["table"]}
    assert set(table.keys()) == {"I", "C", "F", "R = F o C"}

    res = evaluate_centered_zero_symmetries(0.18, 21.022039638771555)
    assert res["consistency_max_residual"] < 1e-15
    assert abs(res["symmetries"]["I"]["z"]["re"] - 0.18) < 1e-15
    assert abs(res["symmetries"]["I"]["z"]["im"] - 21.022039638771555) < 1e-15
    assert abs(res["symmetries"]["C"]["z"]["re"] - 0.18) < 1e-15
    assert abs(res["symmetries"]["C"]["z"]["im"] + 21.022039638771555) < 1e-15
    assert abs(res["symmetries"]["F"]["z"]["re"] + 0.18) < 1e-15
    assert abs(res["symmetries"]["F"]["z"]["im"] + 21.022039638771555) < 1e-15
    assert abs(res["symmetries"]["R"]["z"]["re"] + 0.18) < 1e-15
    assert abs(res["symmetries"]["R"]["z"]["im"] - 21.022039638771555) < 1e-15


def test_02_reflection_involution_R_squared_equals_I() -> None:
    """2. R = F o C = C o F is an involution satisfying R^2 = I."""
    for delta, gamma in [(0.0, 14.134725), (0.15, 21.02204), (-0.22, -25.010858)]:
        res = evaluate_centered_zero_symmetries(delta, gamma)
        assert res["R_squared_equals_I"] is True
        assert res["R_equals_F_compose_C"] is True
        assert res["R_equals_C_compose_F"] is True


def test_03_reflection_stationary_iff() -> None:
    """3. z_rho + conj(z_sigma) = 0 iff sigma = 1 - conj(rho)."""
    inv = classify_second_leg_involutions()
    assert inv["status"] == REFLECTION_PAIR_STATIONARY_FOR_SESQUILINEAR_CORRELATION

    # Stationary reflection pair: delta2 = -delta1, gamma2 = gamma1
    stat = check_reflection_stationarity(0.14, 14.134725, -0.14, 14.134725)
    assert stat["is_stationary"] is True
    assert stat["is_reflection_pair"] is True
    assert stat["stationary_iff_reflection_verified"] is True

    # Nonstationary diagonal off-critical pair: delta2 = delta1 != 0, gamma2 = gamma1
    nonstat_diag = check_reflection_stationarity(0.14, 14.134725, 0.14, 14.134725)
    assert nonstat_diag["is_stationary"] is False
    assert nonstat_diag["is_reflection_pair"] is False
    assert nonstat_diag["stationary_iff_reflection_verified"] is True

    # Nonstationary F-pair: delta2 = -delta1, gamma2 = -gamma1 != 0
    nonstat_f = check_reflection_stationarity(0.14, 14.134725, -0.14, -14.134725)
    assert nonstat_f["is_stationary"] is False
    assert nonstat_f["is_reflection_pair"] is False
    assert nonstat_f["stationary_iff_reflection_verified"] is True


def test_04_critical_zero_self_reflection() -> None:
    """4. On the critical line (delta = 0), rho = 1 - conj(rho) is self-reflected."""
    res = check_reflection_stationarity(0.0, 14.134725, 0.0, 14.134725)
    assert res["rho1_is_self_reflection"] is True
    assert res["self_reflection_iff_critical_verified"] is True
    assert res["is_stationary"] is True


def test_05_offcritical_zero_non_self_reflection() -> None:
    """5. Off the critical line (delta != 0), rho != 1 - conj(rho)."""
    for delta in (0.12, -0.08, 0.25):
        res = check_reflection_stationarity(delta, 14.134725, delta, 14.134725)
        assert res["rho1_is_self_reflection"] is False
        assert res["self_reflection_iff_critical_verified"] is True
        assert res["is_stationary"] is False


def test_06_exact_grade_character_modulus() -> None:
    """6. Exact grade-character modulus |chi_z(K)| = tau^{K delta} (= 1 iff delta = 0 for K != 0)."""
    conv = derive_grade_character_convention()
    assert conv["scale_base"] == "tau = 2*pi"

    c_crit = evaluate_grade_character(0.0, 14.134725, K=2.0)
    assert c_crit["is_unitary"] is True
    assert c_crit["amplitude_residual"] < 1e-15

    c_off = evaluate_grade_character(0.15, 14.134725, K=2.0)
    assert c_off["is_unitary"] is False
    assert abs(c_off["amplitude"] - (TAU ** (2.0 * 0.15))) < 1e-15
    assert c_off["amplitude_residual"] < 1e-15


def test_07_finite_laurent_projector_preserves_q_eq_1() -> None:
    """7. A normalized finite Laurent filter sum_{K=-N}^N c_K q^K preserves q = 1 when sum c_K = 1."""
    coeffs = {-2: 0.1, -1: 0.2, 0: 0.4, 1: 0.2, 2: 0.1}
    val = evaluate_finite_laurent_projector(coeffs, 1.0 + 0.0j)
    assert abs(val - 1.0) < 1e-15


def test_08_finite_laurent_projector_no_go_logic() -> None:
    """8. Finite Laurent projector no-go theorem and Riemann-von Mangoldt distinct-character proof."""
    audit = audit_finite_laurent_projector_no_go()
    assert audit["status"] == FINITE_GRADE_LAURENT_PROJECTOR_NO_GO
    dct = audit["distinct_character_theorem"]
    assert dct["status"] == "INFINITELY_MANY_DISTINCT_PAIR_CHARACTERS_PROVED"
    assert abs(dct["vertical_period_spacing"] - (2.0 * math.pi / LOG_TAU)) < 1e-15


def test_09_finite_differential_projector_no_go() -> None:
    """9. Finite differential projector no-go theorem and rational extension."""
    audit = audit_finite_differential_projector_no_go()
    assert audit["status"] == FINITE_ORDER_GRADE_DIFFERENTIAL_PROJECTOR_NO_GO
    # A polynomial symbol p(lambda) with p(0) = 1 of degree 2 can vanish at most at 2 distinct points
    poly_coeffs = [1.0, -1.5, 0.5]  # (1 - lambda)(1 - 0.5 lambda), roots at 1 and 2
    assert abs(evaluate_finite_differential_projector(poly_coeffs, 0.0) - 1.0) < 1e-15
    assert abs(evaluate_finite_differential_projector(poly_coeffs, 1.0)) < 1e-15
    assert abs(evaluate_finite_differential_projector(poly_coeffs, 2.0)) < 1e-15
    assert abs(evaluate_finite_differential_projector(poly_coeffs, 3.0)) > 0.1


def test_10_discrete_cesaro_kills_unitary_nontrivial_character() -> None:
    """10. Discrete Cesaro A_N(q) -> 0 as N -> infty for |q| = 1, q != 1."""
    q_unit = cmath.exp(1j * 1.2)
    a_1 = evaluate_discrete_cesaro_average(q_unit, N=1)
    a_200 = evaluate_discrete_cesaro_average(q_unit, N=200)
    assert a_1["regime"] == "unitary_nonstationary"
    assert a_1["closed_form_residual"] < 1e-14
    assert a_200["A_N_modulus"] <= 2.0 / ((2 * 200 + 1) * abs(q_unit - 1.0)) + 1e-14
    assert a_200["A_N_modulus"] < a_1["A_N_modulus"]
    assert a_200["A_N_modulus"] < 0.01


def test_11_discrete_cesaro_preserves_q_eq_1() -> None:
    """11. Discrete Cesaro A_N(1) = 1 for all N >= 0."""
    for n in (0, 1, 5, 25):
        res = evaluate_discrete_cesaro_average(1.0 + 0.0j, N=n)
        assert res["regime"] == "stationary_q_eq_1"
        assert abs(res["A_N"]["re"] - 1.0) < 1e-15
        assert abs(res["A_N"]["im"]) < 1e-15


def test_12_discrete_cesaro_diverges_for_q_gt_1() -> None:
    """12. Discrete Cesaro A_N(q) diverges exponentially for |q| > 1."""
    q_gt = 1.5 + 0.0j
    r5 = evaluate_discrete_cesaro_average(q_gt, N=5)
    r15 = evaluate_discrete_cesaro_average(q_gt, N=15)
    assert r5["regime"] == "nonunitary_divergent"
    assert r15["A_N_modulus"] > r5["A_N_modulus"] > 1.0


def test_13_bilateral_symmetry_exposes_q_lt_1_through_negative_grades() -> None:
    """13. Bilateral symmetry sum_{K=-N}^N q^K exposes 0 < |q| < 1 through negative grades K < 0."""
    q_gt = 1.7 + 0.0j
    q_lt = 1.0 / q_gt
    r_gt = evaluate_discrete_cesaro_average(q_gt, N=12)
    r_lt = evaluate_discrete_cesaro_average(q_lt, N=12)
    assert abs(r_gt["A_N_modulus"] - r_lt["A_N_modulus"]) < 1e-12
    assert r_lt["A_N_modulus"] > 10.0


def test_14_continuous_cesaro_formula() -> None:
    """14. Continuous Cesaro C_T(lambda) = sinh(T lambda) / (T lambda) and C_T(0) = 1."""
    c0 = evaluate_continuous_cesaro_average(0.0 + 0.0j, T=7.5)
    assert abs(c0["C_T"]["re"] - 1.0) < 1e-15
    lam = 0.2 + 1.1j
    T = 3.0
    c_lam = evaluate_continuous_cesaro_average(lam, T=T)
    expected = cmath.sinh(T * lam) / (T * lam)
    assert abs(complex(c_lam["C_T"]["re"], c_lam["C_T"]["im"]) - expected) < 1e-15


def test_15_continuous_cesaro_unitary_limit() -> None:
    """15. Continuous Cesaro C_T(i omega) -> 0 for nonzero real omega."""
    lam_unit = 2.5j
    c_5 = evaluate_continuous_cesaro_average(lam_unit, T=5.0)
    c_200 = evaluate_continuous_cesaro_average(lam_unit, T=200.0)
    assert c_5["regime"] == "unitary_imaginary_oscillatory"
    assert c_200["C_T_modulus"] < 0.005


def test_16_continuous_cesaro_nonunitary_growth() -> None:
    """16. Continuous Cesaro |C_T(lambda)| grows exponentially when Re(lambda) != 0."""
    lam_nonunit = 0.35 + 1.2j
    c_5 = evaluate_continuous_cesaro_average(lam_nonunit, T=5.0)
    c_20 = evaluate_continuous_cesaro_average(lam_nonunit, T=20.0)
    assert c_5["regime"] == "nonunitary_exponential_growth"
    assert c_20["C_T_modulus"] > c_5["C_T_modulus"] * 10.0


def test_17_abel_convergence_annulus() -> None:
    """17. Bilateral Abel series converges iff r < |q| < 1/r and diverges as r -> 1^- for |q| != 1."""
    q_nonunit = 1.4 + 0.0j
    inside = evaluate_abel_poisson_average(q_nonunit, r=0.5)
    outside = evaluate_abel_poisson_average(q_nonunit, r=0.8)
    assert inside["series_converges_at_r"] is True
    assert outside["series_converges_at_r"] is False
    assert math.isinf(outside["A_r_modulus"])


def test_18_gaussian_average_exact_formula() -> None:
    """18. Normalized Gaussian grade average equals exp(T^2 lambda^2 / 2) and diverges on real lambda != 0."""
    lam_real = 0.4 + 0.0j
    g2 = evaluate_gaussian_grade_average(lam_real, T=2.0)
    g5 = evaluate_gaussian_grade_average(lam_real, T=5.0)
    assert abs(g2["G_T_modulus"] - math.exp(0.5 * 4.0 * 0.16)) < 1e-15
    assert g5["G_T_modulus"] > g2["G_T_modulus"] > 1.0
    assert g5["grows_as_T_increases"] is True


def test_19_offcritical_same_index_pair_has_q_tau_2delta() -> None:
    """19. Off-critical same-index diagonal pair (rho, rho) has q_{rho,rho} = tau^{2 delta_rho} != 1."""
    diag = audit_offcritical_diagonal_obstruction(delta=0.15, gamma=14.134725)
    assert diag["status"] == OFF_CRITICAL_NONUNITARITY_BLOCKS_GRADE_HAAR_PROJECTION
    assert diag["continuous_status"] == CONTINUOUS_GRADE_HAAR_PROJECTION_REQUIRES_UNITARY_CHARACTERS
    assert abs(diag["diagonal_character_q"] - (TAU ** 0.30)) < 1e-14
    assert diag["is_nonunitary"] is True


def test_20_corrected_mellin_weight_nonzero_in_open_critical_strip() -> None:
    """20. Corrected theta state Phi_t^{(2)} has nonzero Mellin weight across 0 < Re(s) < 1."""
    diag = audit_offcritical_diagonal_obstruction(delta=0.15, gamma=14.134725)
    m_info = diag["mellin_nonvanishing_in_open_strip"]
    assert m_info["provably_nonzero_on_open_strip_0_lt_Re_s_lt_1"] is True
    assert m_info["unsymmetrized_modulus"] > 0.0
    assert m_info["inversion_even_modulus_squared"] > 0.0


def test_21_inversion_even_state_symmetry() -> None:
    """21. Inversion-even state Psi_t^+ satisfies hat{Psi}^+(-z) = hat{Psi}^+(z) and reflection nonnegativity."""
    ctrl = audit_inversion_even_state_control()
    for key in ("sample_on_line", "sample_off_line"):
        sample = ctrl[key]
        assert sample["even_symmetry_residual"] < 1e-15
        assert sample["schwarz_conjugation_residual"] < 1e-15
        assert sample["reflection_product_equals_modulus_squared_residual"] < 1e-15
        assert sample["weight_nonnegative"] is True


def test_22_reflection_quartet_imaginary_cancellation() -> None:
    """22. On the reflection quartet {(rho, 1-conj(rho)), (conj(rho), 1-rho)}, +-4 i gamma cancels."""
    res = evaluate_reflection_quartet_polynomial(delta=0.15, gamma=14.134725)
    assert res["P_pair_formula_residual"] < 1e-14
    assert res["P_conj_pair_formula_residual"] < 1e-14
    assert res["quartet_sum_formula_residual"] < 1e-14
    assert res["imaginary_part_cancelled"] is True
    assert abs(res["quartet_sum"]["re"] - 8.0 * (0.15 ** 2)) < 1e-15


def test_23_reflection_quartet_radial_nonnegativity() -> None:
    """23. Quartet radial contribution 8 m_rho^2 |hat{Psi}^+(z_rho)|^2 delta_rho^2 is nonnegative and > 0 off-line."""
    audit = audit_reflection_quartet_radial_identity()
    assert audit["sample_off_critical"]["weighted_quartet_nonnegative"] is True
    assert audit["sample_off_critical"]["weighted_quartet_radial_value"] > 0.0
    assert audit["sample_on_critical"]["weighted_quartet_radial_value"] == 0.0


def test_24_no_zero_dependent_coefficients() -> None:
    """24. Zero-dependent grade filters are rejected by the Section 26 firewall."""
    rejected = audit_zero_dependent_filter_firewall("weierstrass_zero_product_filter", depends_on_zeros=True)
    assert rejected["status"] == ZERO_DEPENDENT_GRADE_FILTER_REJECTED
    assert rejected["admissible_as_tc_proof_mechanism"] is False

    admissible = audit_zero_dependent_filter_firewall("cesaro_average", depends_on_zeros=False)
    assert admissible["admissible_as_tc_proof_mechanism"] is True


def test_25_common_shift_transport_b_eq_1_audit() -> None:
    """25. Preserving cross-grade arithmetic station labels under common shift r forces b = 1."""
    coords = evaluate_common_and_relative_grade_coordinates(0.0, 1.0)
    assert coords["reconstruction_error"] < 1e-15
    audit = audit_common_shift_transport_compatibility()
    assert audit["status"] == COMMON_SHIFT_PROJECTION_TRANSPORT_INCOMPATIBILITY
    assert audit["required_b_for_arithmetic_preservation"] == 1.0


def test_26_spectral_factor_cancellation_at_full_transport() -> None:
    """26. At full transport b = 1, the zero-dependent common-shift spectral exponent (b-1)r(s+t) vanishes."""
    audit = audit_common_shift_transport_compatibility(r=2.5, a=1.0)
    assert abs(audit["at_b_eq_1_zero_dependent_exponent"]["re"]) < 1e-15
    assert abs(audit["at_b_eq_1_zero_dependent_exponent"]["im"]) < 1e-15
    assert audit["common_shift_spectral_character_survives_at_b_eq_1"] is False


def test_27_b_ne_1_arithmetic_compatibility_loss() -> None:
    """27. For b != 1 (e.g. b = 0), the spectral common-shift exponent survives but arithmetic support separation is lost."""
    audit = audit_common_shift_transport_compatibility(r=1.5, a=0.0)
    assert audit["arithmetic_support_separation_survives_at_b_ne_1"] is False
    assert abs(audit["b_eq_0_sample_zero_dependent_exponent"]["re"]) > 0.1


def test_28_ratio_kernel_common_shift_cancellation() -> None:
    """28. Scale-invariant ratio kernels phi(x/y) concentrate on s + t = 0 and erase the common-shift character."""
    audit = audit_scale_invariant_ratio_kernel()
    assert audit["status"] == SCALE_INVARIANT_ARITHMETIC_KERNEL_ERASES_COMMON_GRADE_CHARACTER
    assert audit["common_shift_character_survives"] is False


def test_29_relative_grade_fallback_evidence_scope() -> None:
    """29. Relative-grade alternative d = J - K audits finite-cutoff vs full-spectrum Diophantine gaps."""
    audit = audit_relative_grade_alternative()
    assert audit["status"] == "RELATIVE_GRADE_SMOOTH_UNIFORM_GAP_FAILS_ON_FULL_SPECTRUM"
    gaps = [row["min_log_gap_d1"] for row in audit["diophantine_log_gap_shrinking"]]
    # As station cutoff increases from 15 to 200, min |log(n/m) - log(2*pi)| shrinks
    assert gaps[-1] < gaps[0]


def test_30_no_arithmetic_sign_contradiction_without_proof() -> None:
    """30. Same-sign nonnegativity on sesquilinear correlations yields no arithmetic-spectral contradiction."""
    gate = audit_arithmetic_contradiction_gate()
    assert gate["status"] == REFLECTION_PROJECTION_HAS_NO_ARITHMETIC_SIGN_CONTRADICTION
    assert gate["sesquilinear_correlation_G_C"]["yields_contradiction"] is False


def test_31_weil_equivalence_firewall() -> None:
    """31. Treating nonunitary grade characters by Fourier orthogonality is flagged as a disguised RH premise."""
    pf = audit_pontryagin_duality_firewall()
    assert pf["status"] == GRADE_ORTHOGONALITY_OUTSIDE_UNITARY_AXIS_IS_DISGUISED_RH_PREMISE
    cg = audit_complex_grade_loophole()
    assert cg["status"] == "NO_FIXED_COMPLEX_GRADE_CONTOUR_UNITARIZES_SPECTRUM"
    assert all(row["both_zero"] is False for row in cg["sample_angle_audit"])


def test_32_generic_base_control() -> None:
    """32. Generic-base q > 1 control confirms projection algebra holds for all q > 1."""
    gb = audit_generic_base_grade_projection_control()
    assert gb["status"] == "GRADE_PROJECTION_ALGEBRA_HOLDS_FOR_ALL_BASES_Q_GT_1"
    assert gb["tau_specific_on_spectral_projection_side"] is False
    assert all(r["diagonal_nonunitary_for_delta_ne_0"] is True for r in gb["records"])


def test_33_obl_ct_001a_remains_open_unless_full_bridge() -> None:
    """33. OBL-CT-001A remains OPEN and principal classification is in the permitted list."""
    report = build_grade_character_projection_report()
    assert report["obl_ct_001a_status"] == "OPEN"
    assert report["principal_classification"] == PRINCIPAL_CLASSIFICATION
    assert report["principal_classification"] in PERMITTED_PRINCIPAL_OUTCOMES
    assert (
        report["principal_classification"]
        == GRADE_CHARACTER_PROJECTION_DOES_NOT_ESCAPE_TRANSPORT_MOMENT_INCOMPATIBILITY
    )


def test_34_candidate_failure_does_not_refute_tc() -> None:
    """34. Failure of the grade-character reflection projector candidate does not refute TC."""
    report = build_grade_character_projection_report()
    assert report["candidate_failure_refutes_tc"] is False


def test_35_no_rh_claim() -> None:
    """35. No proof or disproof of the Riemann Hypothesis is claimed."""
    report = build_grade_character_projection_report()
    assert report["no_rh_claim"] is True


def test_36_actual_lean_theorem_identifiers_match_formal_file() -> None:
    """36. All 11 required Lean theorem identifiers exist in GradeCharacterProjection.lean with 0 sorry/admit."""
    info = verify_lean_theorem_identifiers()
    assert info["all_required_present"] is True
    assert info["missing_theorems"] == []
    assert info["sorry_count"] == 0
    assert info["admit_count"] == 0
    assert info["axiom_count"] == 0
    for name in REQUIRED_LEAN_THEOREMS:
        assert name in info["declared_theorems"]


def test_37_json_artifact_contains_all_required_keys() -> None:
    """37. Machine-readable artifact data/tc_grade_character_projection.json contains all 38 required keys."""
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "tc_grade_character_projection.json"
    )
    assert artifact_path.exists()
    data = json.loads(artifact_path.read_text(encoding="utf-8"))
    required_keys = [
        "starting_head",
        "corrected_theta_state_used",
        "centered_zero_symmetries",
        "grade_character_convention",
        "bigraded_functional",
        "second_leg_involution_table",
        "common_shift_parameter",
        "relative_grade_parameter",
        "pair_character_formula",
        "reflection_stationary_iff",
        "finite_laurent_projector_status",
        "finite_differential_projector_status",
        "distinct_character_theorem_status",
        "riemann_von_mangoldt_dependency",
        "discrete_cesaro_status",
        "continuous_cesaro_status",
        "abel_status",
        "gaussian_average_status",
        "offcritical_diagonal_character",
        "nonunitarity_status",
        "inversion_even_state_status",
        "reflection_quartet_formula",
        "reflection_weight_sign_status",
        "cross_grade_arithmetic_zero_status",
        "common_shift_transport_status",
        "spectral_signal_survival_status",
        "ratio_kernel_status",
        "relative_grade_fallback_status",
        "arithmetic_projected_value_status",
        "spectral_projected_value_status",
        "contradiction_status",
        "weil_equivalence_status",
        "zero_dependency_firewall",
        "generic_base_status",
        "obl_ct_001a_status",
        "principal_classification",
        "exact_remaining_subgate",
        "lean_theorem_map",
    ]
    for k in required_keys:
        assert k in data, f"Missing required key: {k}"
