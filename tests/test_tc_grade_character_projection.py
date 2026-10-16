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
    DISTINCT_PAIR_CHARACTERS_PROVED_USING_DISTINCT_ZERO_DENSITY,
    FINITE_COMPLEX_GRADE_PROJECTOR_NO_GO_FORMALIZED,
    FINITE_GRADE_LAURENT_PROJECTOR_NO_GO,
    FINITE_ORDER_GRADE_DIFFERENTIAL_PROJECTOR_NO_GO,
    FOURIER_SELF_DUALITY_DISTINCT_FROM_MULTIPLICATIVE_INVERSION_EVENNESS,
    GRADE_CHARACTER_PROJECTION_DOES_NOT_ESCAPE_TRANSPORT_MOMENT_INCOMPATIBILITY,
    GRADE_CHARACTER_PROJECTION_INCOMPATIBLE_WITH_TESTED_TRANSPORT_ANSATZ,
    GRADE_ORTHOGONALITY_OUTSIDE_UNITARY_AXIS_IS_DISGUISED_RH_PREMISE,
    INFINITELY_MANY_DISTINCT_PAIR_CHARACTERS_PROVED,
    INVERSION_EVEN_MELLIN_WEIGHT_ZERO_FREE_STRIP_OPEN,
    LOG_TAU,
    OFF_CRITICAL_NONUNITARITY_BLOCKS_FOLNER_CHARACTER_PROJECTION,
    OFF_CRITICAL_NONUNITARITY_BLOCKS_GRADE_HAAR_PROJECTION,
    PERMITTED_PRINCIPAL_OUTCOMES,
    PRINCIPAL_CLASSIFICATION,
    REFLECTION_PAIR_STATIONARY_FOR_SESQUILINEAR_CORRELATION,
    REFLECTION_PROJECTION_HAS_NO_ARITHMETIC_SIGN_CONTRADICTION,
    REFLECTION_QUARTET_RADIAL_IDENTITY_PRESERVED,
    REFLECTION_WEIGHT_NONNEGATIVE_PROVED,
    REFLECTION_WEIGHT_STRICT_POSITIVITY_NOT_YET_PROVED,
    RELATIVE_GRADE_DIFFERENTIATION_NOT_PURE_RADIAL,
    RELATIVE_GRADE_REFLECTION_EXPONENT_REPAIRED,
    REQUIRED_LEAN_THEOREMS,
    SCALE_INVARIANT_ARITHMETIC_KERNEL_ERASES_COMMON_GRADE_CHARACTER,
    TASK_TC_037R_ID,
    TASK_TC_037R_STATUS,
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
    verify_distinct_zero_density_justification,
    verify_finite_complex_projector_no_go,
    verify_fourier_vs_multiplicative_inversion,
    verify_lean_theorem_identifiers,
    verify_relative_grade_reflection_algebra,
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


# ============================================================================
# TASK-TC-037R: 25 Required Evidence-Repair Verification Tests
# ============================================================================


def test_38_n_of_t_vs_n_dist_of_t_distinction_recorded() -> None:
    """38 (037R-1). N(T) (with multiplicity) vs N_dist(T) (distinct zeros) distinction recorded."""
    res = verify_distinct_zero_density_justification()
    assert "N(T)" in res["multiplicity_zero_count_definition"]
    assert "N_dist(T)" in res["distinct_zero_count_definition"]
    assert "WITH multiplicity" in res["why_N_T_alone_was_insufficient"]


def test_39_distinct_critical_line_zeros_justified_by_simple_zero_theorem() -> None:
    """39 (037R-2). Distinct critical-line zeros justified by simple-zero density theorem, not N(T) alone."""
    res = verify_distinct_zero_density_justification()
    assert res["status"] == DISTINCT_PAIR_CHARACTERS_PROVED_USING_DISTINCT_ZERO_DENSITY
    primary = res["primary_citations"][0]
    assert "Bui" in primary["authors"] and "Conrey" in primary["authors"] and "Young" in primary["authors"]
    assert primary["arxiv_id"] == "1002.4127v2"
    assert res["bcy_2011_simple_zero_proportion"] >= 0.4058
    assert all(row["distinct_zeros_exceed_vertical_progressions"] is True for row in res["sample_height_comparisons"])


def test_40_offcritical_delta_implies_nonunit_character_modulus() -> None:
    """40 (037R-3). Off-critical delta_{rho_0} != 0 implies |q_{rho_0,sigma_n}| = tau^{delta_{rho_0}} != 1."""
    delta_rho0 = 0.15
    gamma_rho0 = 14.134725141734693
    sample_gammas = [14.134725141734693, 21.022039638771555, 25.010857580145688, 30.424876125859513]
    for g in sample_gammas:
        lam = complex(delta_rho0, gamma_rho0 - g)
        q_val = cmath.exp(LOG_TAU * lam)
        assert abs(abs(q_val) - (TAU ** delta_rho0)) < 1e-15
        assert abs(abs(q_val) - 1.0) > 0.1
        assert abs(q_val - 1.0) > 0.1


def test_41_distinct_exponents_for_distinct_ordinates() -> None:
    """41 (037R-4). Distinct exponents lambda_{rho_0,sigma_n} verified for distinct gamma_n."""
    res = verify_distinct_zero_density_justification()
    assert "sigma_1 = sigma_2" in res["exponent_vs_character_distinction"]["exponent_distinctness_rule"]
    delta_rho0 = 0.15
    gamma_rho0 = 14.134725141734693
    sample_gammas = [14.134725141734693, 21.022039638771555, 25.010857580145688, 30.424876125859513]
    exps = [complex(delta_rho0, gamma_rho0 - g) for g in sample_gammas]
    for i in range(len(exps)):
        for j in range(i + 1, len(exps)):
            assert abs(exps[i] - exps[j]) > 1.0


def test_42_distinct_characters_under_vertical_period_spacing() -> None:
    """42 (037R-5). Distinct characters q_{rho_0,sigma_{n_k}} verified under spacing > 2*pi / log(tau)."""
    res = verify_distinct_zero_density_justification()
    assert res["legacy_status"] == INFINITELY_MANY_DISTINCT_PAIR_CHARACTERS_PROVED
    period = res["vertical_period_spacing"]
    assert abs(period - (2.0 * math.pi / LOG_TAU)) < 1e-15
    delta_rho0 = 0.15
    gamma_rho0 = 14.134725141734693
    # Subsequence with spacing > 2*pi / log(tau) ~ 3.41878
    subseq_gammas = [14.134725141734693, 21.022039638771555, 25.010857580145688, 30.424876125859513]
    for i in range(len(subseq_gammas) - 1):
        assert (subseq_gammas[i + 1] - subseq_gammas[i]) > period
    chars = [cmath.exp(LOG_TAU * complex(delta_rho0, gamma_rho0 - g)) for g in subseq_gammas]
    for i in range(len(chars)):
        for j in range(i + 1, len(chars)):
            assert abs(chars[i] - chars[j]) > 1e-4


def test_43_complex_polynomial_projector_no_go_in_lean() -> None:
    """43 (037R-6). Complex polynomial projector no-go theorem present in Lean over Polynomial C."""
    res = verify_finite_complex_projector_no_go()
    assert res["status"] == FINITE_COMPLEX_GRADE_PROJECTOR_NO_GO_FORMALIZED
    assert res["complex_laurent_lean_theorem"] == "finite_complex_polynomial_projector_root_no_go"
    assert res["polynomial_ring_in_lean"] == "Polynomial ℂ"
    assert res["sympy_complex_witness_check"]["Q_at_1_equals_1"] is True
    assert res["sympy_complex_witness_check"]["Q_at_w1_equals_0"] is True
    assert res["sympy_complex_witness_check"]["Q_at_w2_equals_0"] is True
    assert res["sympy_complex_witness_check"]["Q_at_third_distinct_complex_point_nonzero"] is True
    info = verify_lean_theorem_identifiers()
    assert "finite_complex_polynomial_projector_root_no_go" in info["declared_theorems"]


def test_44_complex_differential_projector_no_go_in_lean() -> None:
    """44 (037R-7). Complex differential projector no-go theorem present in Lean over Polynomial C."""
    res = verify_finite_complex_projector_no_go()
    assert res["differential_status"] == FINITE_ORDER_GRADE_DIFFERENTIAL_PROJECTOR_NO_GO
    assert res["complex_differential_lean_theorem"] == "finite_complex_differential_projector_root_no_go"
    info = verify_lean_theorem_identifiers()
    assert "finite_complex_differential_projector_root_no_go" in info["declared_theorems"]


def test_45_relative_grade_exponent_at_reflection_equals_minus_two_z() -> None:
    """45 (037R-8). Relative-grade exponent at sigma = 1 - conj(rho) equals -2*z_rho = -2*delta_rho - 2*i*gamma_rho."""
    res = verify_relative_grade_reflection_algebra(delta=0.18, gamma=14.134725141734693, d=0.35)
    assert res["exponent_repair_status"] == RELATIVE_GRADE_REFLECTION_EXPONENT_REPAIRED
    assert res["sympy_exact_checks"]["common_coeff_is_zero"] is True
    assert res["sympy_exact_checks"]["relative_coeff_equals_neg_2_z_rho"] is True
    assert res["sympy_exact_checks"]["full_exponent_equals_neg_2_d_z_rho"] is True
    assert res["numerical_sample"]["full_exponent_residual"] < 1e-14


def test_46_relative_grade_second_derivative_not_pure_radial() -> None:
    """46 (037R-9). Relative-grade second derivative equals 8*(log tau)^2*(delta^2 - gamma^2), not 8*(log tau)^2*delta^2."""
    delta = 0.15
    gamma = 14.134725141734693
    res = verify_relative_grade_reflection_algebra(delta=delta, gamma=gamma, d=0.25)
    assert res["differentiation_status"] == RELATIVE_GRADE_DIFFERENTIATION_NOT_PURE_RADIAL
    assert res["sympy_exact_checks"]["relative_quartet_equals_8_L2_delta2_minus_gamma2"] is True
    expected = 8.0 * (LOG_TAU ** 2) * (delta ** 2 - gamma ** 2)
    assert abs(res["numerical_sample"]["relative_second_derivative_quartet_value"] - expected) < 1e-12
    assert res["numerical_sample"]["relative_quartet_is_negative_for_delta_lt_gamma"] is True
    assert res["numerical_sample"]["arb_certified_negative"] is True


def test_47_reflection_quartet_curvature_polynomial_still_equals_8_delta_squared() -> None:
    """47 (037R-10). Reflection-quartet curvature polynomial P(z,-conj(z)) + P(conj(z),-z) still equals 8*delta^2."""
    delta = 0.15
    gamma = 14.134725141734693
    res = verify_relative_grade_reflection_algebra(delta=delta, gamma=gamma)
    assert res["curvature_polynomial_status"] == REFLECTION_QUARTET_RADIAL_IDENTITY_PRESERVED
    assert res["sympy_exact_checks"]["curvature_polynomial_quartet_equals_8_delta2"] is True
    p_res = evaluate_reflection_quartet_polynomial(delta=delta, gamma=gamma)
    assert abs(p_res["quartet_sum"]["re"] - 8.0 * (delta ** 2)) < 1e-14
    assert abs(p_res["quartet_sum"]["im"]) < 1e-14


def test_48_fourier_self_duality_distinguished_from_multiplicative_inversion_evenness() -> None:
    """48 (037R-11). Fourier self-duality of exp(-pi u^2) distinguished from multiplicative inversion-evenness."""
    res = verify_fourier_vs_multiplicative_inversion()
    assert (
        res["fourier_vs_inversion_status"]
        == FOURIER_SELF_DUALITY_DISTINCT_FROM_MULTIPLICATIVE_INVERSION_EVENNESS
    )
    assert "F tilde{g}_1 = tilde{g}_1" in res["fourier_self_duality_definition"]
    assert "u^{-1} Psi(u^{-1})" in res["multiplicative_inversion_definition"]


def test_49_raw_phi_t_mellin_nonvanishing_on_open_strip() -> None:
    """49 (037R-12). Raw hat{Phi_t^{(2)}}(z) is nonvanishing on -1/2 < Re(z) < 1/2."""
    diag = audit_offcritical_diagonal_obstruction(delta=0.15, gamma=14.134725141734693)
    assert diag["mellin_nonvanishing_in_open_strip"]["provably_nonzero_on_open_strip_0_lt_Re_s_lt_1"] is True
    assert diag["mellin_nonvanishing_in_open_strip"]["unsymmetrized_modulus"] > 0.0


def test_50_raw_phi_t_is_not_multiplicative_inversion_even() -> None:
    """50 (037R-13). Raw Phi_t^{(2)} is not multiplicative inversion-even (hat{Phi_1^{(2)}}(z) != hat{Phi_1^{(2)}}(-z))."""
    res = verify_fourier_vs_multiplicative_inversion()
    assert res["raw_phi_t1_inversion_even"] is False
    witness = res["raw_mellin_asymmetry_witness_at_t1"]
    assert witness["asymmetry_modulus_diff"] > 1e-12
    assert witness["arb_certified_nonzero_asymmetry"] is True


def test_51_symmetrized_psi_plus_mellin_even_symmetry() -> None:
    """51 (037R-14). Symmetrized hat{Psi_t^+}(z) satisfies hat{Psi_t^+}(-z) = hat{Psi_t^+}(z)."""
    res = verify_fourier_vs_multiplicative_inversion()
    assert res["symmetrized_psi_plus_inversion_even"] is True
    assert res["symmetrized_state_symmetry_witness"]["even_symmetry_residual"] < 1e-15


def test_52_reflection_weight_nonnegative() -> None:
    """52 (037R-15). Reflection weight w_+(rho) = |hat{Psi_t^+}(z_rho)|^2 >= 0."""
    res = verify_fourier_vs_multiplicative_inversion()
    assert res["reflection_weight_nonnegative_status"] == REFLECTION_WEIGHT_NONNEGATIVE_PROVED
    assert res["symmetrized_state_symmetry_witness"]["reflection_product_equals_modulus_squared_residual"] < 1e-15
    assert res["arb_point_weights_certified_positive"] is True


def test_53_strict_offcritical_positivity_for_psi_plus_classified_as_open() -> None:
    """53 (037R-16). Strict off-critical positivity for hat{Psi_t^+} is classified as open and critical-line sign change is certified."""
    res = verify_fourier_vs_multiplicative_inversion()
    assert res["reflection_weight_strict_positivity_status"] == REFLECTION_WEIGHT_STRICT_POSITIVITY_NOT_YET_PROVED
    assert res["symmetrized_mellin_zero_free_strip_status"] == INVERSION_EVEN_MELLIN_WEIGHT_ZERO_FREE_STRIP_OPEN
    sign_cert = res["critical_line_oscillation_zero_witness_at_t1"]
    assert sign_cert["hat_Psi_1_plus_at_i_gamma_a_re"] > 0.0
    assert sign_cert["hat_Psi_1_plus_at_i_gamma_b_re"] < 0.0
    assert sign_cert["opposite_signs_on_critical_line"] is True
    assert sign_cert["arb_certified_sign_change_in_open_strip"] is True


def test_54_folner_cesaro_terminology_replaces_raw_probability_haar() -> None:
    """54 (037R-17). Folner/Cesaro terminology replaces raw probability-Haar wording on noncompact Z and R."""
    report = build_grade_character_projection_report()
    assert report["folner_nonunitarity_obstruction_status"] == OFF_CRITICAL_NONUNITARITY_BLOCKS_FOLNER_CHARACTER_PROJECTION
    assert report["nonunitarity_status"]["folner_status"] == OFF_CRITICAL_NONUNITARITY_BLOCKS_FOLNER_CHARACTER_PROJECTION
    assert report["discrete_cesaro_status"]["folner_status"] == OFF_CRITICAL_NONUNITARITY_BLOCKS_FOLNER_CHARACTER_PROJECTION
    assert report["continuous_cesaro_status"]["folner_status"] == OFF_CRITICAL_NONUNITARITY_BLOCKS_FOLNER_CHARACTER_PROJECTION


def test_55_transport_incompatibility_scoped_to_tested_ansatz() -> None:
    """55 (037R-18). Transport incompatibility is explicitly scoped to the tested bigraded transport ansatz."""
    report = build_grade_character_projection_report()
    assert (
        report["tested_transport_incompatibility_status"]
        == GRADE_CHARACTER_PROJECTION_INCOMPATIBLE_WITH_TESTED_TRANSPORT_ANSATZ
    )
    assert (
        report["common_shift_transport_status"]["scoped_status"]
        == GRADE_CHARACTER_PROJECTION_INCOMPATIBLE_WITH_TESTED_TRANSPORT_ANSATZ
    )


def test_56_subgate_tc_037a_does_not_assume_unproved_strict_weight_positivity() -> None:
    """56 (037R-19). SUBGATE-TC-037A does not assume unproved strict weight positivity."""
    report = build_grade_character_projection_report()
    subgate = report["exact_remaining_subgate"]
    assert subgate["subgate_id"] == "SUBGATE-TC-037A"
    assert subgate["status"] == "OPEN"
    assert "provably strictly positive" in subgate["precise_theorem_target"]
    assert "provably nonnegative >= 0" in subgate["precise_theorem_target"]


def test_57_repair_obl_ct_001a_remains_open() -> None:
    """57 (037R-20). OBL-CT-001A remains OPEN after TASK-TC-037R repair."""
    report = build_grade_character_projection_report()
    assert report["obl_ct_001a_status"] == "OPEN"


def test_58_repair_does_not_refute_tc() -> None:
    """58 (037R-21). Failure or repair of the projector candidate does not refute TC."""
    report = build_grade_character_projection_report()
    assert report["candidate_failure_refutes_tc"] is False


def test_59_repair_no_rh_proof_or_disproof_claimed() -> None:
    """59 (037R-22). No RH proof or disproof is claimed in TASK-TC-037R."""
    report = build_grade_character_projection_report()
    assert report["no_rh_claim"] is True
    assert report["task_id"] == TASK_TC_037R_ID
    assert report["task_status"] == TASK_TC_037R_STATUS


def test_60_lean_file_has_zero_sorry_and_zero_admit() -> None:
    """60 (037R-23). Lean file formal/RiemannScope/GradeCharacterProjection.lean has 0 sorry and 0 admit."""
    info = verify_lean_theorem_identifiers()
    assert info["sorry_count"] == 0
    assert info["admit_count"] == 0
    assert info["axiom_count"] == 0
    assert len(info["declared_theorems"]) == 17


def test_61_lean_theorem_names_in_docs_and_json_match_compiled_file() -> None:
    """61 (037R-24). All 17 Lean theorem names in docs and JSON artifact match the compiled Lean file."""
    info = verify_lean_theorem_identifiers()
    compiled_set = set(info["declared_theorems"])
    assert len(REQUIRED_LEAN_THEOREMS) == 17
    assert set(REQUIRED_LEAN_THEOREMS) == compiled_set

    root = Path(__file__).resolve().parent.parent
    artifact_data = json.loads((root / "data" / "tc_grade_character_projection.json").read_text(encoding="utf-8"))
    assert set(artifact_data["lean_theorem_map"]["declared_theorems"]) == compiled_set

    review_text = (root / "docs" / "reviews" / "TC_GRADE_CHARACTER_REFLECTION_PROJECTION.md").read_text(
        encoding="utf-8"
    )
    for thm in REQUIRED_LEAN_THEOREMS:
        assert thm in review_text, f"Missing theorem {thm} in review doc"


def test_62_json_artifact_contains_all_required_repair_keys() -> None:
    """62 (037R-25). JSON artifact contains all 22 required TASK-TC-037R repair keys from Section 22."""
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "tc_grade_character_projection.json"
    )
    data = json.loads(artifact_path.read_text(encoding="utf-8"))
    repair_keys = [
        "starting_head",
        "substantive_parent",
        "distinct_zero_count_definition",
        "distinct_zero_density_theorem_citation",
        "distinct_pair_characters_status",
        "finite_complex_polynomial_projector_lean_theorem",
        "finite_complex_differential_projector_lean_theorem",
        "folner_nonunitarity_obstruction_status",
        "relative_grade_reflection_exponent_formula",
        "relative_grade_second_derivative_quartet_formula",
        "relative_grade_differentiation_status",
        "reflection_quartet_polynomial_status",
        "fourier_self_duality_vs_multiplicative_inversion_status",
        "raw_phi_t1_inversion_even",
        "symmetrized_psi_plus_inversion_even",
        "symmetrized_mellin_zero_free_strip_status",
        "reflection_weight_nonnegative_status",
        "reflection_weight_strict_positivity_status",
        "tested_transport_incompatibility_status",
        "subgate_id",
        "obl_ct_001a_status",
        "principal_classification",
    ]
    for k in repair_keys:
        assert k in data, f"Missing repair key: {k}"


