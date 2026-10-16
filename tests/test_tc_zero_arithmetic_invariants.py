"""
Tests for TASK-TC-038: Arithmetic Nature of Nontrivial Zeros, Exact Zero-Sum
Invariants, and Special-Value Transfer Audit.

Covers all 26 required test cases from Section 42 of the TASK-TC-038 specification.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from tc.core import arb
from tc.grade_character_projection import (
    INVERSION_EVEN_MELLIN_ZERO_FREE_STRIP_FALSE,
    STRICT_REFLECTION_WEIGHT_AT_ZETA_ZERO_ORDINATES_OPEN,
    build_grade_character_projection_report,
)
from tc.zero_arithmetic_invariants import (
    ALGEBRAIC_ZERO_DOES_NOT_AUTOMATICALLY_ENTER_AMBIENT_KERNEL,
    CERTIFIED_BOUNDED_DENOMINATOR_RATIONAL_EXCLUSION,
    CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION,
    CONDITIONAL_ON_RH,
    DIFFERENTIAL_TRANSCENDENCE_DOES_NOT_DETERMINE_ZERO_ARITHMETIC,
    EULER_PRODUCT_NONVANISHING_NOT_AVAILABLE_IN_CRITICAL_STRIP,
    FUNCTIONAL_EQUATION_DOES_NOT_EXCLUDE_ALGEBRAIC_ZERO,
    LI_COEFFICIENT_POSITIVITY_IS_RH_EQUIVALENT,
    NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT,
    NUMERICAL_EVIDENCE_ONLY,
    OPEN_IN_LITERATURE,
    PERMITTED_PRINCIPAL_OUTCOMES,
    PRIMARY_SOURCE_VERIFIED,
    PRINCIPAL_CLASSIFICATION,
    REQUIRED_ARTIFACT_KEYS,
    REQUIRED_LEAN_THEOREMS,
    SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE,
    SPECIAL_VALUE_IRRATIONALITY_METHOD_HAS_NO_DIRECT_ZERO_LOCATION_TRANSFER,
    SPECIAL_VALUE_IRRATIONALITY_METHOD_NO_DIRECT_ZERO_LOCATION_TRANSFER,
    SUBGATE_TC_038A_ID,
    TASK_TC_038_BRANCH,
    TASK_TC_038_ID,
    ZETA5_CURRENT_STATUS_VERIFIED,
    audit_euler_product_firewall,
    audit_full_zero_vs_ordinate_algebraicity,
    audit_functional_equation_algebraic_zero,
    audit_gamma_and_differential_transcendence_firewalls,
    audit_primary_literature_individual_zeros,
    audit_shifted_ordinate_redundancy,
    audit_superzeta_and_constant_arithmetic,
    audit_tc_interaction,
    audit_transcendence_theorem_applicability,
    build_zero_arithmetic_invariants_report,
    certify_bounded_denominator_rational_exclusion,
    certify_finite_algebraicity_exclusion,
    classify_candidate_objects,
    count_primitive_polynomials_up_to,
    derive_xi_hadamard_and_reciprocal_sums,
    enumerate_normalized_primitive_polynomials,
    run_pslq_diagnostic_control,
    verify_lean_theorem_identifiers,
    verify_zeta5_and_special_value_transfer,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


# 1. Preflight TASK-TC-037R status update: INVERSION_EVEN_MELLIN_ZERO_FREE_STRIP_FALSE
def test_01_preflight_tc_037r_mellin_zero_free_strip_false() -> None:
    report_037r = build_grade_character_projection_report()
    assert (
        report_037r["symmetrized_mellin_zero_free_strip_status"]
        == INVERSION_EVEN_MELLIN_ZERO_FREE_STRIP_FALSE
    )
    assert (
        report_037r["strict_reflection_weight_at_zeta_zero_ordinates_status"]
        == STRICT_REFLECTION_WEIGHT_AT_ZETA_ZERO_ORDINATES_OPEN
    )


# 2. Preflight sign-change witness synchronization across code/artifact/report
def test_02_preflight_sign_change_witness_synchronization() -> None:
    artifact_037r_path = REPO_ROOT / "data" / "tc_grade_character_projection.json"
    artifact_037r = json.loads(artifact_037r_path.read_text(encoding="utf-8"))
    sc = artifact_037r["fourier_vs_multiplicative_inversion_audit"][
        "critical_line_oscillation_zero_witness_at_t1"
    ]
    assert sc["gamma_a"] == 0.25
    assert sc["gamma_b"] == 1.0
    assert sc["arb_certified_sign_change_in_open_strip"] is True

    review_037r = (
        REPO_ROOT / "docs" / "reviews" / "TC_GRADE_CHARACTER_REFLECTION_PROJECTION.md"
    ).read_text(encoding="utf-8")
    assert INVERSION_EVEN_MELLIN_ZERO_FREE_STRIP_FALSE in review_037r
    assert "0.005930018171819737" in review_037r
    assert "-0.01007544310514176" in review_037r


# 3. Shifted ordinate rationality equivalence
def test_03_shifted_ordinate_rationality_equivalence() -> None:
    res = audit_shifted_ordinate_redundancy()
    assert (
        res["classification"]
        == SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE
    )
    assert "gamma in Q  <=>  gamma + 1/2 in Q" in res["rational_equivalence"]
    assert res["all_symbolic_checks_passed"] is True


# 4. Shifted ordinate algebraicity/transcendence equivalence
def test_04_shifted_ordinate_algebraicity_and_transcendence_equivalence() -> None:
    candidates = classify_candidate_objects()
    cand_c = candidates["candidate_C_shifted_ordinate"]
    assert cand_c["independent_arithmetic_target"] is False
    assert (
        cand_c["status"] == SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE
    )
    res = audit_shifted_ordinate_redundancy()
    assert "gamma in Q_bar  <=>  gamma + 1/2 in Q_bar" in res["algebraic_equivalence"]
    assert (
        "gamma transcendental  <=>  gamma + 1/2 transcendental"
        in res["transcendental_equivalence"]
    )


# 5. Unconditional equivalence between algebraic rho = beta + i*gamma and algebraic (beta, gamma)
def test_05_unconditional_rho_vs_beta_gamma_algebraicity() -> None:
    res = audit_full_zero_vs_ordinate_algebraicity()
    assert res["unconditional_forward"]["status"] == "PROVED"
    assert res["unconditional_converse"]["status"] == "PROVED"
    assert res["symbolic_reconstruction_verified"] is True


# 6. Conditional RH equivalence marked conditional
def test_06_conditional_rh_equivalence_marked_conditional() -> None:
    res = audit_full_zero_vs_ordinate_algebraicity()
    cond = res["conditional_rh_equivalence"]
    assert cond["status"] == CONDITIONAL_ON_RH
    assert cond["used_unconditionally"] is False


# 7. Exact formula for S_1 = sum^{sym} 1/rho
def test_07_exact_formula_S1() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    s1 = sums["reciprocal_sum_S1"]
    assert s1["symbolic_derivation_verified"] is True
    assert s1["mpmath_50dps_residual"] < 1e-45
    assert abs(s1["value_float"] - 0.023095708966121033) < 1e-15


# 8. Exact formula and absolute convergence of sum 1/(rho(1 - rho)) = 2*S_1 = 2*lambda_1
def test_08_reflection_invariant_sum_formula_and_convergence() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    refl = sums["reflection_invariant_sum"]
    assert refl["absolute_convergence"] is True
    assert refl["mpmath_50dps_residual"] < 1e-45
    assert abs(refl["value_float"] - 2.0 * sums["reciprocal_sum_S1"]["value_float"]) < 1e-15


# 9. Exact formula for S_2 = sum 1/rho^2
def test_09_exact_formula_S2() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    s2 = sums["reciprocal_sum_S2"]
    assert s2["absolute_convergence"] is True
    assert s2["symbolic_s0_verified"] is True
    assert s2["symbolic_s1_verified"] is True
    assert s2["mpmath_s0_residual"] < 1e-45
    assert s2["mpmath_s1_residual"] < 1e-45


# 10. Reciprocal-power log-derivative recurrence for m = 1, 2, 3, 4
def test_10_reciprocal_power_hierarchy_m1_to_4() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    table = sums["reciprocal_power_hierarchy"]["table_m_1_to_4"]
    assert len(table) == 4
    for row in table:
        assert row["residual_vs_closed_form"] < 1e-44


# 11. Odd centered zero sums vanish by reflection symmetry
def test_11_odd_centered_zero_sums_vanish() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    odd = sums["centered_zero_invariants"]["odd_centered_sums_vanish"]
    assert odd["mpmath_odd_derivative_residuals"]["m_eq_1"] < 1e-45
    assert odd["mpmath_odd_derivative_residuals"]["m_eq_2"] < 1e-45


# 12. Even centered zero sum formulas for m = 1, 2 (Sigma_2, Sigma_4)
def test_12_even_centered_zero_sums() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    even = sums["centered_zero_invariants"]["even_centered_sums"]
    assert even["Sigma_2"]["closed_form_residual"] < 1e-44
    assert float(even["Sigma_2"]["value_50dps"]) < 0.0
    assert float(even["Sigma_4"]["value_50dps"]) > 0.0


# 13. Quartet polynomial identity (X^2 - z^2)(X^2 - conj(z)^2)
def test_13_quartet_polynomial_identity() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    qp = sums["quartet_polynomial"]
    assert "X^4 - 2*(delta^2 - gamma^2)*X^2 + (delta^2 + gamma^2)^2" in qp["monic_polynomial"]
    assert "centered_quartet_polynomial_identity" in qp["lean_theorems"]
    assert "centered_quartet_coefficients_real" in qp["lean_theorems"]


# 14. Li first coefficient identity lambda_1 = S_1 and derivative vs binomial agreement
def test_14_li_coefficients_identity_and_firewall() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    li = sums["li_coefficient_audit"]
    assert li["positivity_firewall"] == LI_COEFFICIENT_POSITIVITY_IS_RH_EQUIVALENT
    for entry in li["values_n_1_to_4"]:
        assert entry["binomial_vs_derivative_residual"] < 1e-44


# 15. Partial zero-sum numerical sanity against exact closed forms
def test_15_partial_zero_sum_numerical_controls() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    ctrl = sums["partial_sum_numerical_controls"]
    assert ctrl["reference_zero_count_pairs"] == 200
    assert ctrl["S1_tail_corrected_error"] < 2e-5
    assert ctrl["Sigma4_absolute_error_200_pairs"] < 1e-8


# 16. Transcendence theorem applicability matrix completeness
def test_16_transcendence_theorem_applicability_matrix() -> None:
    matrix = audit_transcendence_theorem_applicability()
    assert len(matrix) == 9
    for row in matrix:
        assert set(row.keys()) >= {
            "theorem",
            "input_structure_required",
            "does_zeta_zero_provide_it",
            "obstruction",
        }
        assert row["does_zeta_zero_provide_it"] == "No"


# 17. Functional-equation algebraic-zero test does not divide by zero
def test_17_functional_equation_algebraic_zero_no_zero_division() -> None:
    fe = audit_functional_equation_algebraic_zero()
    assert fe["classification"] == FUNCTIONAL_EQUATION_DOES_NOT_EXCLUDE_ALGEBRAIC_ZERO
    assert fe["zero_order_identity"]["division_by_zeta_rho_blocked"] is True


# 18. Euler-product critical-strip firewall
def test_18_euler_product_critical_strip_firewall() -> None:
    ep = audit_euler_product_firewall()
    assert (
        ep["classification"]
        == EULER_PRODUCT_NONVANISHING_NOT_AVAILABLE_IN_CRITICAL_STRIP
    )
    assert ep["domains_disjoint"] is True


# 19. Differential-transcendence firewall and Gamma-function firewall
def test_19_differential_transcendence_and_gamma_firewalls() -> None:
    gamma_fw, diff_fw = audit_gamma_and_differential_transcendence_firewalls()
    assert (
        diff_fw["classification"]
        == DIFFERENTIAL_TRANSCENDENCE_DOES_NOT_DETERMINE_ZERO_ARITHMETIC
    )
    assert "Gamma(1/4)" in gamma_fw["special_rational_values_known_transcendental"]


# 20. Current status of zeta(5) and special-value transfer classification
def test_20_zeta5_status_and_special_value_transfer() -> None:
    zeta5, transfer, aux = verify_zeta5_and_special_value_transfer()
    assert zeta5["status_code"] == ZETA5_CURRENT_STATUS_VERIFIED
    assert zeta5["archimedean_zeta5_individually_proved_irrational"] is False
    assert zeta5["archimedean_zeta5_status"] == OPEN_IN_LITERATURE
    assert zeta5["source_verification"] == PRIMARY_SOURCE_VERIFIED
    assert (
        transfer["classification"]
        == SPECIAL_VALUE_IRRATIONALITY_METHOD_HAS_NO_DIRECT_ZERO_LOCATION_TRANSFER
    )
    assert (
        transfer["secondary_outcome_code"]
        == SPECIAL_VALUE_IRRATIONALITY_METHOD_NO_DIRECT_ZERO_LOCATION_TRANSFER
    )
    assert aux["privileging_gamma_1_avoided"] is True


# 21. Normalized primitive polynomial enumeration (no zero polynomial, positive lead, coprime)
def test_21_normalized_primitive_polynomial_enumeration() -> None:
    polys = enumerate_normalized_primitive_polynomials(D=3, H=2)
    counts = count_primitive_polynomials_up_to(D=3, H=2)
    assert len(polys) == counts["total_primitive_polynomials"]
    for coeffs in polys:
        assert len(coeffs) >= 2
        assert coeffs[-1] >= 1
        assert max(abs(c) for c in coeffs) <= 2


# 22. Certified Arb exclusion for small-height polynomials at gamma_1, rho_1, and gamma_1 + 1/2
def test_22_certified_arb_finite_algebraicity_exclusion() -> None:
    res = certify_finite_algebraicity_exclusion(
        D_explicit=3, H_explicit=2, D_box=4, H_box=20
    )
    assert res["classification"] == CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION
    assert res["is_irrationality_proof"] is False
    assert res["is_transcendence_proof"] is False
    assert res["explicit_individual_enumeration"]["all_excluded"] is True
    assert (
        res["explicit_individual_enumeration"]["translated_control_max_residual"]
        < 1e-27
    )
    assert (
        res["hierarchical_arb_box_certificate_D4_H100"]["gamma_1_certificate"][
            "certified"
        ]
        is True
    )
    assert (
        res["hierarchical_arb_box_certificate_D4_H100"]["rho_1_certificate"][
            "certified"
        ]
        is True
    )


# 23. Fail-closed behavior if a polynomial interval contains 0 or enclosure is too wide
def test_23_certified_exclusion_fails_closed_on_wide_or_zero_interval() -> None:
    wide_ball = arb("14.1347 +/- 0.5")
    with pytest.raises(ValueError, match="failing closed"):
        certify_finite_algebraicity_exclusion(custom_enclosure=wide_ball)

    exact_root_ball = arb("2.0 +/- 1e-20")
    with pytest.raises(ValueError, match="contains 0; failing closed"):
        certify_finite_algebraicity_exclusion(custom_enclosure=exact_root_ball)


# 24. Bounded-denominator rational exclusion for gamma_1 and gamma_1 + 1/2
def test_24_bounded_denominator_rational_exclusion() -> None:
    rat = certify_bounded_denominator_rational_exclusion(Q=10000)
    assert rat["classification"] == CERTIFIED_BOUNDED_DENOMINATOR_RATIONAL_EXCLUSION
    assert rat["is_irrationality_proof"] is False
    assert rat["gamma_1"]["all_rationals_q_le_Q_excluded"] is True
    assert (
        rat["shifted_ordinate_gamma_1_plus_half"]["all_rationals_q_le_Q_excluded"]
        is True
    )
    assert rat["gamma_1"]["min_certified_distance_abs_gamma1_minus_p_over_q"] > 0.0


# 25. PSLQ diagnostic output is classified strictly as NUMERICAL_EVIDENCE_ONLY
def test_25_pslq_diagnostic_firewall() -> None:
    pslq = run_pslq_diagnostic_control(dps=60, max_degree=3)
    assert pslq["classification"] == NUMERICAL_EVIDENCE_ONLY
    assert pslq["is_proof_or_certificate"] is False


# 26. Artifact schema completeness and Lean theorem identifier presence
def test_26_artifact_schema_and_lean_identifiers() -> None:
    artifact_path = REPO_ROOT / "data" / "tc_zero_arithmetic_invariants.json"
    assert artifact_path.exists()
    data = json.loads(artifact_path.read_text(encoding="utf-8"))
    for k in REQUIRED_ARTIFACT_KEYS:
        assert k in data, f"Missing required artifact key: {k}"

    assert data["task_id"] == TASK_TC_038_ID
    assert data["principal_classification"] in PERMITTED_PRINCIPAL_OUTCOMES
    assert data["principal_classification"] == PRINCIPAL_CLASSIFICATION
    assert data["exact_remaining_subgate"]["subgate_id"] == SUBGATE_TC_038A_ID
    assert data["exact_remaining_subgate"]["branch"] == TASK_TC_038_BRANCH
    assert data["exact_remaining_subgate"]["obl_ct_001a_status"] == "OPEN"
    assert (
        data["tc_interaction"]["classification"]
        == ALGEBRAIC_ZERO_DOES_NOT_AUTOMATICALLY_ENTER_AMBIENT_KERNEL
    )

    lit = audit_primary_literature_individual_zeros()
    assert (
        lit["individual_zero_claims"]["rho_n_excluded_from_named_number_field"]["status"]
        == NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT
    )
    superzeta, const_table = audit_superzeta_and_constant_arithmetic()
    assert len(const_table) >= 7
    assert (
        superzeta["arithmetic_nature_of_positive_special_values"]["status"]
        == OPEN_IN_LITERATURE
    )

    lean_info = verify_lean_theorem_identifiers(REPO_ROOT)
    assert lean_info["all_required_present"] is True
    assert lean_info["sorry_count"] == 0
    assert lean_info["admit_count"] == 0
    for thm in REQUIRED_LEAN_THEOREMS:
        assert thm in lean_info["found_declarations"]
