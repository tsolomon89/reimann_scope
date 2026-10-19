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
    CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE,
    CERTIFIED_BOUNDED_DENOMINATOR_RATIONAL_EXCLUSION,
    CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION,
    CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION,
    CONDITIONAL_ON_RH,
    DIFFERENTIAL_TRANSCENDENCE_DOES_NOT_DETERMINE_ZERO_ARITHMETIC,
    EULER_PRODUCT_NONVANISHING_NOT_AVAILABLE_IN_CRITICAL_STRIP,
    EXPLICIT_POLYNOMIAL_ENUMERATION,
    FAUZAN_HANKEL_METHOD_EXPOSES_NEW_AUXILIARY_POLYNOMIAL_ROUTE,
    FAUZAN_HANKEL_METHOD_HAS_NO_ZERO_LOCATION_TRANSFER,
    FAUZAN_HANKEL_METHOD_HAS_PARTIAL_ZERO_LOCATION_TRANSFER,
    FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED,
    FIXED_NUMBER_FIELD_REQUIRES_BOUNDED_DEGREE_AND_BOUNDED_HEIGHT,
    FORMAL_SOURCE_INVENTORY_REPAIRED,
    FORMAL_SOURCE_INVENTORY_SYNCHRONIZED,
    FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED,
    FUNCTIONAL_EQUATION_DOES_NOT_EXCLUDE_ALGEBRAIC_ZERO,
    HIERARCHICAL_BOX_EXCLUSION,
    LEAN_PROVED_EXTERNAL_REPOSITORY,
    LI_COEFFICIENT_POSITIVITY_IS_RH_EQUIVALENT,
    NO_INDIVIDUAL_ORDINATE_IRRATIONALITY_OR_TRANSCENDENCE_THEOREM_FOUND,
    NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT,
    NUMERICAL_EVIDENCE_ONLY,
    OPEN_IN_LITERATURE,
    PEER_REVIEW_STATUS_PENDING,
    PERMITTED_PRINCIPAL_OUTCOMES,
    PRIMARY_SOURCE_VERIFIED,
    PRINCIPAL_CLASSIFICATION,
    REQUIRED_ARTIFACT_KEYS,
    REQUIRED_FAUZAN_ARCHITECTURE_KEYS,
    REQUIRED_LEAN_THEOREMS,
    REQUIRED_TC_038R_REPAIR_KEYS,
    S2_CANONICAL_FORMULA_REPAIRED,
    S3_S4_REAUDITED,
    SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE,
    SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED,
    SPECIAL_VALUE_IRRATIONALITY_METHOD_HAS_NO_DIRECT_ZERO_LOCATION_TRANSFER,
    SPECIAL_VALUE_IRRATIONALITY_METHOD_NO_DIRECT_ZERO_LOCATION_TRANSFER,
    SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT_REPAIRED,
    STIELTJES_NOTATION_DISAMBIGUATED,
    SUBGATE_TC_038A_ID,
    SUBGATE_TC_039A_ID,
    TASK_TC_038R_ID,
    TASK_TC_038R_STATUS,
    TASK_TC_038_BRANCH,
    TASK_TC_038_ID,
    VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE,
    ZERO_ARITHMETIC_MODULE_INCLUDED_IN_BUILD_PROVENANCE,
    ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE,
    ZETA5_CURRENT_STATUS_VERIFIED,
    ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN,
    ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM,
    ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN,
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
    load_fauzan_zeta5_architecture,
    run_pslq_diagnostic_control,
    verify_formal_source_inventory_provenance,
    verify_lean_theorem_identifiers,
    verify_zeta5_and_special_value_transfer,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
PERMITTED_TRANSFER_OUTCOMES = (
    FAUZAN_HANKEL_METHOD_HAS_NO_ZERO_LOCATION_TRANSFER,
    FAUZAN_HANKEL_METHOD_HAS_PARTIAL_ZERO_LOCATION_TRANSFER,
    FAUZAN_HANKEL_METHOD_EXPOSES_NEW_AUXILIARY_POLYNOMIAL_ROUTE,
    FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED,
)


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


# 20. Current status of zeta(5) and special-value transfer classification (repaired in TASK-TC-038R)
def test_20_zeta5_status_and_special_value_transfer() -> None:
    zeta5, transfer, aux = verify_zeta5_and_special_value_transfer()
    assert zeta5["status_code"] == ZETA5_CURRENT_STATUS_VERIFIED
    assert zeta5["lean_formalization_status"] == ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN
    assert zeta5["preprint_claim_status"] == ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM
    assert zeta5["conventional_peer_review_status"] == PEER_REVIEW_STATUS_PENDING
    assert zeta5["source_verification"] == PRIMARY_SOURCE_VERIFIED
    assert (
        transfer["repaired_audit_status"]
        == SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT_REPAIRED
    )
    assert (
        transfer["classification"]
        == FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED
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
    assert (
        res["exclusion_scope_status"]
        == CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION
    )
    assert (
        res["classification"]
        == CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION
    )
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

    assert data["task_id"] == TASK_TC_038R_ID
    assert data["parent_task_id"] == TASK_TC_038_ID
    assert data["task_tc_038r_status"] == TASK_TC_038R_STATUS
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


# =============================================================================
# TASK-TC-038R Required Tests (Section 37: 30 items)
# =============================================================================


# TC-038R Test 1: ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM present
def test_038r_01_zeta5_irrationality_2026_preprint_claim_present() -> None:
    arch = load_fauzan_zeta5_architecture(REPO_ROOT)
    assert (
        arch["evidence_classification"]["manuscript_claim"]
        == ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM
    )
    assert arch["paper_reference"]["doi"] == "10.5281/zenodo.22826419"


# TC-038R Test 2: ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN present
def test_038r_02_zeta5_irrationality_formalized_in_lean_present() -> None:
    arch = load_fauzan_zeta5_architecture(REPO_ROOT)
    ev = arch["evidence_classification"]
    assert ev["formal_verification"] == ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN
    assert ev["external_lean_status"] == LEAN_PROVED_EXTERNAL_REPOSITORY
    assert ev["local_build_audit_status"] == SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED


# TC-038R Test 3: mo271/Zeta5 repository and theorem Apery.irrational_five recorded
def test_038r_03_mo271_zeta5_and_apery_irrational_five_recorded() -> None:
    arch = load_fauzan_zeta5_architecture(REPO_ROOT)
    assert "mo271/Zeta5" in arch["lean_repository"]["repository_url"]
    assert "Apery.irrational_five" in arch["target_theorem"]["apery_main_theorem"]
    assert "riemannZeta 5" in arch["target_theorem"]["apery_main_theorem"]


# TC-038R Test 4: ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN recorded with standard Lean axioms
def test_038r_04_zeta5_formalization_dependency_graph_clean() -> None:
    arch = load_fauzan_zeta5_architecture(REPO_ROOT)
    assert (
        arch["evidence_classification"]["dependency_graph_status"]
        == ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN
    )
    assert arch["lean_repository"]["print_axioms_result"] == [
        "propext",
        "Classical.choice",
        "Quot.sound",
    ]
    assert arch["lean_repository"]["sorry_admit_audit"]["apery_directory_sorry_count"] == 0
    assert arch["lean_repository"]["sorry_admit_audit"]["apery_directory_admit_count"] == 0


# TC-038R Test 5: PEER_REVIEW_STATUS_PENDING recorded separately from formalization status
def test_038r_05_peer_review_status_pending_separate() -> None:
    arch = load_fauzan_zeta5_architecture(REPO_ROOT)
    ev = arch["evidence_classification"]
    assert ev["conventional_peer_review_status"] == PEER_REVIEW_STATUS_PENDING
    assert ev["conventional_peer_review_status"] != ev["formal_verification"]


# TC-038R Test 6: data/fauzan_zeta5_architecture.json exists and has all required keys
def test_038r_06_fauzan_zeta5_architecture_json_schema() -> None:
    path = REPO_ROOT / "data" / "fauzan_zeta5_architecture.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    for k in REQUIRED_FAUZAN_ARCHITECTURE_KEYS:
        assert k in data, f"Missing required Fauzan architecture key: {k}"


# TC-038R Test 7: Fauzan polynomial degree 37n and parameters K=40n, N=3n recorded
def test_038r_07_fauzan_polynomial_degree_and_parameters() -> None:
    arch = load_fauzan_zeta5_architecture(REPO_ROOT)
    params = arch["polynomial_family"]["parameters"]
    assert params["K"] == "40 * n"
    assert params["N"] == "3 * n"
    assert params["h"] == "K - N = 37 * n"
    assert "37n" in arch["degree_formula"]["exact_degree"]


# TC-038R Test 8: Fauzan small-value vs denominator-growth comparison recorded
def test_038r_08_fauzan_small_value_vs_denominator_growth() -> None:
    arch = load_fauzan_zeta5_architecture(REPO_ROOT)
    assert "139/5 = 27.8" in arch["small_value_rate"]["paper_rate"]
    assert "5.5964" in arch["small_value_rate"]["lean_formalized_rate"]
    assert "A_{\\mathrm{eff}} + U = -0.0069955 < 0" in arch["denominator_growth_rate"]["lean_constant"]


# TC-038R Test 9: VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE present
def test_038r_09_value_vs_argument_polynomial_architecture() -> None:
    _, transfer, aux = verify_zeta5_and_special_value_transfer()
    assert (
        transfer["structural_distinction"]
        == VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE
    )
    assert (
        aux["structural_distinction"]
        == VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE
    )


# TC-038R Test 10: FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED or permitted transfer classification present
def test_038r_10_fauzan_hankel_zero_location_transfer_classification() -> None:
    _, transfer, _ = verify_zeta5_and_special_value_transfer()
    assert transfer["classification"] in PERMITTED_TRANSFER_OUTCOMES
    assert (
        transfer["classification"]
        == FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED
    )
    assert (
        transfer["repaired_audit_status"]
        == SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT_REPAIRED
    )


# TC-038R Test 11: SUBGATE-TC-039A gate map Z1-Z6 present and complete
def test_038r_11_subgate_tc_039a_gate_map_complete() -> None:
    _, _, aux = verify_zeta5_and_special_value_transfer()
    sub = aux["subgate_tc_039a"]
    assert sub["subgate_id"] == SUBGATE_TC_039A_ID
    assert sub["status"] == "OPEN"
    gate_ids = [g["gate_id"] for g in sub["gates"]]
    assert gate_ids == ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6"]


# TC-038R Test 12: formal/RiemannScope/ZeroArithmeticInvariants.lean is in scripts/build_formal.py::FORMAL_SOURCE_FILES
def test_038r_12_zero_arithmetic_invariants_in_build_formal_sources() -> None:
    prov = verify_formal_source_inventory_provenance(REPO_ROOT)
    assert prov["zero_arithmetic_lean_file_in_inventories"] is True
    assert prov["missing_from_build_formal"] == []


# TC-038R Test 13: formal/RiemannScope/ZeroArithmeticInvariants.lean is in certification.py::REQUIRED_FORMAL_SOURCES
def test_038r_13_zero_arithmetic_invariants_in_certification_required_sources() -> None:
    prov = verify_formal_source_inventory_provenance(REPO_ROOT)
    assert prov["zero_arithmetic_lean_file_in_inventories"] is True
    assert prov["missing_from_certification"] == []


# TC-038R Test 14: Every local import RiemannScope.* in formal/RiemannScope.lean is present in both formal source lists
def test_038r_14_all_riemann_scope_imports_in_both_formal_source_lists() -> None:
    prov = verify_formal_source_inventory_provenance(REPO_ROOT)
    assert prov["synchronized"] is True
    assert prov["lists_match_exactly"] is True
    assert prov["status"] == FORMAL_SOURCE_INVENTORY_SYNCHRONIZED


# TC-038R Test 15: formal/RiemannScope/ZeroArithmeticInvariants.lean contains 0 sorry and 0 admit
def test_038r_15_zero_arithmetic_invariants_lean_zero_sorry_admit() -> None:
    lean_info = verify_lean_theorem_identifiers(REPO_ROOT)
    assert lean_info["sorry_count"] == 0
    assert lean_info["admit_count"] == 0


# TC-038R Test 16: Exact theorem count of ZeroArithmeticInvariants.lean matches reported count
def test_038r_16_zero_arithmetic_invariants_exact_theorem_count() -> None:
    lean_info = verify_lean_theorem_identifiers(REPO_ROOT)
    prov = verify_formal_source_inventory_provenance(REPO_ROOT)
    assert lean_info["theorem_declaration_count"] == 12
    assert lean_info["total_declaration_count"] == 12
    assert len(REQUIRED_LEAN_THEOREMS) == 11
    assert lean_info["all_required_present"] is True
    assert prov["zero_arithmetic_lean_theorem_count"] == 12
    assert prov["total_formal_theorem_count"] >= 626
    assert prov["total_formal_theorem_count"] == 647



# TC-038R Test 17: Stieltjes constants use disambiguated notation in code/artifact/report
def test_038r_17_stieltjes_notation_disambiguated() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    assert (
        sums["stieltjes_notation_policy"]["status"] == STIELTJES_NOTATION_DISAMBIGUATED
    )
    assert "gamma_1^St" in sums["reciprocal_sum_S2"]["exact_formula_at_s1_stieltjes"]
    assert "gamma_2^St" in sums["S3_reaudit"]["exact_formula_stieltjes"]
    assert "gamma_3^St" in sums["S4_reaudit"]["exact_formula_stieltjes"]
    review_text = (
        REPO_ROOT / "docs" / "reviews" / "TC_ZERO_ARITHMETIC_INVARIANTS.md"
    ).read_text(encoding="utf-8")
    assert STIELTJES_NOTATION_DISAMBIGUATED in review_text
    assert r"\gamma_1^{\mathrm{St}}" in review_text


# TC-038R Test 18: S_2 at s=0 and s=1 agree to <1e-45
def test_038r_18_s2_s0_and_s1_agreement_50dps() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    s2 = sums["reciprocal_sum_S2"]
    assert s2["status"] == S2_CANONICAL_FORMULA_REPAIRED
    assert s2["s0_vs_s1_derivative_residual"] < 1e-45
    assert s2["mpmath_s0_residual"] < 1e-45
    assert s2["mpmath_s1_residual"] < 1e-45


# TC-038R Test 19: Erroneous S_2 formula does not appear anywhere in canonical docs
def test_038r_19_erroneous_s2_formula_removed_from_canonical_docs() -> None:
    erroneous_fragments = [
        r"\frac{\gamma_{\mathrm{Euler}}^2}{4} - \gamma_1^{\mathrm{Stieltjes}}",
        r"\gamma_E^2/4 - \gamma_1",
    ]
    canonical_docs = [
        REPO_ROOT / "RESEARCH_HYPOTHESIS.md",
        REPO_ROOT / "RESEARCH_LEDGER.md",
        REPO_ROOT / "MATH_CONTRACT.md",
        REPO_ROOT / "TRANSCENDENTAL_CONTINUATION.md",
        REPO_ROOT / "docs" / "TC_CURRENT_CANONICAL_STATUS.md",
    ]
    for doc_path in canonical_docs:
        content = doc_path.read_text(encoding="utf-8")
        for frag in erroneous_fragments:
            assert frag not in content, f"Erroneous S_2 fragment {frag!r} found in {doc_path.name}"


# TC-038R Test 20: S_3 and S_4 symbolic/50-dps/partial-sum checks pass
def test_038r_20_s3_and_s4_reaudit_checks_pass() -> None:
    sums = derive_xi_hadamard_and_reciprocal_sums()
    s3 = sums["S3_reaudit"]
    s4 = sums["S4_reaudit"]
    assert s3["status"] == S3_S4_REAUDITED
    assert s3["route_1_symbolic_laurent_verified"] is True
    assert s3["route_2_mpmath_50dps_s0_vs_closed_residual"] < 1e-45
    assert s3["route_2_mpmath_50dps_s1_vs_closed_residual"] < 1e-45
    assert s3["route_3_tail_corrected_residual"] < 2e-6
    assert s4["status"] == S3_S4_REAUDITED
    assert s4["route_1_symbolic_laurent_verified"] is True
    assert s4["route_2_mpmath_50dps_s0_vs_closed_residual"] < 1e-45
    assert s4["route_2_mpmath_50dps_s1_vs_closed_residual"] < 1e-45
    assert s4["route_3_tail_corrected_residual"] < 1e-8


# TC-038R Test 21: Finite box D<=4, H<=100 exclusion passes for gamma_1, rho_1, and gamma_1 + 1/2
def test_038r_21_finite_box_d4_h100_exclusion_passes() -> None:
    artifact = json.loads(
        (REPO_ROOT / "data" / "tc_zero_arithmetic_invariants.json").read_text(
            encoding="utf-8"
        )
    )
    box = artifact["finite_algebraicity_exclusion"][
        "hierarchical_arb_box_certificate_D4_H100"
    ]
    assert box["number_of_primitive_polynomials_in_space"] == 158062321920
    assert box["gamma_1_certificate"]["certified"] is True
    assert box["shifted_ordinate_certificate"]["certified"] is True
    assert box["rho_1_certificate"]["certified"] is True


# TC-038R Test 22: Route A: FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED is present and no uncertified full-box global minimum is claimed
def test_038r_22_route_a_full_box_global_minimum_not_certified() -> None:
    artifact = json.loads(
        (REPO_ROOT / "data" / "tc_zero_arithmetic_invariants.json").read_text(
            encoding="utf-8"
        )
    )
    fa = artifact["finite_algebraicity_exclusion"]
    assert fa["global_minimum_scope_status"] == FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED
    box = fa["hierarchical_arb_box_certificate_D4_H100"]
    assert box["certification_method"] == HIERARCHICAL_BOX_EXCLUSION
    assert box["full_box_global_minimum_certified"] is False
    for key in (
        "gamma_1_certificate",
        "shifted_ordinate_certificate",
        "rho_1_certificate",
    ):
        assert (
            box[key]["global_minimum_scope"]
            == FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED
        )
        assert box[key]["full_box_global_minimum_certified"] is False
        assert "min_certified_lower_bound" not in box[key]


# TC-038R Test 23: Explicit small-box D<=4, H<=3 global minimum is certified
def test_038r_23_explicit_small_box_d4_h3_global_minimum_certified() -> None:
    artifact = json.loads(
        (REPO_ROOT / "data" / "tc_zero_arithmetic_invariants.json").read_text(
            encoding="utf-8"
        )
    )
    exp = artifact["finite_algebraicity_exclusion"][
        "explicit_individual_enumeration"
    ]
    assert exp["D"] == 4
    assert exp["H"] == 3
    assert exp["certification_method"] == EXPLICIT_POLYNOMIAL_ENUMERATION
    assert exp["number_of_polynomials_tested"] == 8160
    assert exp["full_box_global_minimum_certified"] is True
    assert exp["gamma_1_min_certified_abs_lower_bound"] > 11.0
    assert exp["shifted_ordinate_min_certified_abs_lower_bound"] > 11.5
    assert exp["rho_1_min_certified_abs_lower_bound"] > 14.0


# TC-038R Test 24: Bounded-denominator rational exclusion q<=10^4 passes
def test_038r_24_bounded_denominator_rational_exclusion_q10000() -> None:
    rat = certify_bounded_denominator_rational_exclusion(Q=10000)
    assert rat["max_denominator_Q"] == 10000
    assert rat["gamma_1"]["all_rationals_q_le_Q_excluded"] is True
    assert rat["shifted_ordinate_gamma_1_plus_half"]["all_rationals_q_le_Q_excluded"] is True


# TC-038R Test 25: PSLQ remains NUMERICAL_EVIDENCE_ONLY
def test_038r_25_pslq_remains_numerical_evidence_only() -> None:
    pslq = run_pslq_diagnostic_control(dps=60, max_degree=3)
    assert pslq["classification"] == NUMERICAL_EVIDENCE_ONLY
    assert pslq["is_proof_or_certificate"] is False


# TC-038R Test 26: Cardinality transcendence row is removed or replaced with CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE
def test_038r_26_cardinality_transcendence_repair() -> None:
    lit = audit_primary_literature_individual_zeros()
    card = lit["individual_zero_claims"]["cardinality_transcendence_fallacy_repaired"]
    assert (
        card["status"]
        == CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE
    )
    assert (
        card["literature_row_status"]
        == NO_INDIVIDUAL_ORDINATE_IRRATIONALITY_OR_TRANSCENDENCE_THEOREM_FOUND
    )
    review_text = (
        REPO_ROOT / "docs" / "reviews" / "TC_ZERO_ARITHMETIC_INVARIANTS.md"
    ).read_text(encoding="utf-8")
    assert CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE in review_text


# TC-038R Test 27: Fixed-number-field statements include bounded-height qualification
def test_038r_27_fixed_number_field_bounded_height_qualification() -> None:
    lit = audit_primary_literature_individual_zeros()
    nf = lit["individual_zero_claims"]["rho_n_excluded_from_named_number_field"]
    assert "bounded height" in nf["northcott_height_qualification"]
    assert lit["fixed_number_field_scope_distinction"]["height_qualification_required"] is True
    review_text = (
        REPO_ROOT / "docs" / "reviews" / "TC_ZERO_ARITHMETIC_INVARIANTS.md"
    ).read_text(encoding="utf-8")
    assert FIXED_NUMBER_FIELD_REQUIRES_BOUNDED_DEGREE_AND_BOUNDED_HEIGHT in review_text


# TC-038R Test 28: SUBGATE-TC-038A is scoped to zero-sum constants
def test_038r_28_subgate_tc_038a_scoped_to_zero_sum_constants() -> None:
    artifact = json.loads(
        (REPO_ROOT / "data" / "tc_zero_arithmetic_invariants.json").read_text(
            encoding="utf-8"
        )
    )
    sub38 = artifact["exact_remaining_subgate"]
    assert sub38["subgate_id"] == SUBGATE_TC_038A_ID
    assert (
        sub38["subgate_classification"] == ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE
    )


# TC-038R Test 29: OBL-CT-001A remains OPEN
def test_038r_29_obl_ct_001a_remains_open() -> None:
    artifact = json.loads(
        (REPO_ROOT / "data" / "tc_zero_arithmetic_invariants.json").read_text(
            encoding="utf-8"
        )
    )
    assert artifact["exact_remaining_subgate"]["obl_ct_001a_status"] == "OPEN"
    reassessed = artifact["principal_classification_reassessed"]
    assert reassessed["obl_ct_001a_status"] == "OBL_CT_001A_OPEN"
    assert reassessed["subgate_tc_038a_status"] == "SUBGATE_TC_038A_OPEN"
    assert reassessed["subgate_tc_039a_status"] == "SUBGATE_TC_039A_OPEN"


# TC-038R Test 30: data/tc_zero_arithmetic_invariants.json contains all required TASK-TC-038R keys
def test_038r_30_artifact_contains_all_tc_038r_repair_keys() -> None:
    artifact = json.loads(
        (REPO_ROOT / "data" / "tc_zero_arithmetic_invariants.json").read_text(
            encoding="utf-8"
        )
    )
    for k in REQUIRED_TC_038R_REPAIR_KEYS:
        assert k in artifact, f"Missing required TASK-TC-038R key: {k}"


