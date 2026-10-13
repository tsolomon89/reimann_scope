"""
Unit tests for TASK-TC-034: Infinitesimal Transport-Mismatch Curvature and
Non-Scalar Arithmetic Descent (`tc/transport_mismatch_curvature.py`).

Covers all 26 required verification gates in Section 24 of TASK-TC-034 plus
Lean 4 formalization alignment (`formal/RiemannScope/TransportMismatchCurvature.lean`).
"""

from __future__ import annotations

import math
from pathlib import Path
import pytest

from tc.transport_mismatch_curvature import (
    CLASSIFICATION_ARITHMETIC_INDEFINITE,
    CLASSIFICATION_COMPACT_SUPPORT_IMPOSSIBLE,
    CLASSIFICATION_CURVATURE_POSITIVITY_RH_EQUIVALENT,
    CLASSIFICATION_FINITE_ACCIDENTAL_ZERO,
    CLASSIFICATION_GENERIC_SCALE_CURVATURE,
    CLASSIFICATION_REDUCES_TO_EXISTING_OBL_CT_001A,
    CLASSIFICATION_SELECTED_BLOCK_ONLY,
    LOG_TAU,
    OUTCOME_A_FULL_BRIDGE,
    OUTCOME_B_ARITHMETIC_FLATNESS_NOT_IMPLIED,
    OUTCOME_C_COMPACT_SUPPORT_NO_GO,
    OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE,
    OUTCOME_E_WEIL_EQUIVALENCE,
    OUTCOME_G_REDUCES_TO_OBL_CT_001A,
    PRINCIPAL_CLASSIFICATION,
    TAU,
    audit_arithmetic_curvature_sign_firewall,
    audit_compact_support_homogeneity_no_go,
    audit_complete_spectral_curvature_and_firewalls,
    audit_finite_station_accidental_zero,
    audit_spectral_centering_and_pairings,
    audit_theta_mellin_nonscalar_fallback,
    audit_transport_mismatch_curvature,
    audit_weil_equivalence_firewall,
    evaluate_even_mismatch_defect,
    evaluate_euler_moments_A0_A1_A2,
    evaluate_exponential_mixture_curvature,
    evaluate_generic_base_mismatch_control,
    evaluate_homogeneous_kernel_control,
    evaluate_mellin_mismatch_scaling,
    evaluate_mismatch_derivatives_at_zero,
    evaluate_normalized_mismatch_energy,
    evaluate_reciprocal_pair_curvature,
    evaluate_transported_mismatch_kernel,
    reconcile_with_existing_curvature_transport,
)


def _sample_gaussian_log_kernel():
    """Return (f0, euler1_f0, euler2_f0) for F_0(x, y) = exp(-0.5 * (log(x*y / 16))^2)."""

    def f0(x: float, y: float) -> float:
        w = math.log((x * y) / 16.0)
        return math.exp(-0.5 * w * w)

    def euler1_f0(x: float, y: float) -> float:
        w = math.log((x * y) / 16.0)
        return (-2.0 * w) * math.exp(-0.5 * w * w)

    def euler2_f0(x: float, y: float) -> float:
        w = math.log((x * y) / 16.0)
        return (4.0 * w * w - 4.0) * math.exp(-0.5 * w * w)

    return f0, euler1_f0, euler2_f0


# 1. Compatibility point eta = 0 reproduces full transport
def test_01_compatibility_point_eta_zero_reproduces_full_transport():
    f0, _, _ = _sample_gaussian_log_kernel()
    m0 = evaluate_normalized_mismatch_energy(f0, K=0.0, eta=0.0, n_max=15)
    for K in [-2.0, -1.0, 0.5, 1.0, 2.0, 3.0]:
        mK = evaluate_normalized_mismatch_energy(f0, K=K, eta=0.0, n_max=15)
        assert abs(mK - m0) < 1e-12
    # Also check kernel evaluation at x = tau^K n, y = tau^K m with eta = 0, a = 0
    val_K = evaluate_transported_mismatch_kernel(
        f0, x=(TAU ** 2) * 3.0, y=(TAU ** 2) * 5.0, K=2.0, eta=0.0, a=0.0
    )
    val_0 = f0(3.0, 5.0)
    assert abs(val_K - val_0) < 1e-12


# 2. First Euler derivative formula
def test_02_first_euler_derivative_formula():
    f0, e1, e2 = _sample_gaussian_log_kernel()
    moments = evaluate_euler_moments_A0_A1_A2(f0, n_max=15, euler1_f0=e1, euler2_f0=e2)
    for K in [-2.0, -1.0, 1.0, 2.5]:
        res = evaluate_mismatch_derivatives_at_zero(
            f0, K=K, n_max=15, euler1_f0=e1, euler2_f0=e2
        )
        expected_first = (-K * LOG_TAU) * moments.A1
        assert abs(res.euler_M_K_prime_0 - expected_first) < 1e-12
        assert abs(res.M_K_prime_0 - expected_first) < 1e-7


# 3. Second Euler derivative formula
def test_03_second_euler_derivative_formula():
    f0, e1, e2 = _sample_gaussian_log_kernel()
    moments = evaluate_euler_moments_A0_A1_A2(f0, n_max=15, euler1_f0=e1, euler2_f0=e2)
    for K in [-2.0, -1.0, 1.0, 2.5]:
        res = evaluate_mismatch_derivatives_at_zero(
            f0, K=K, n_max=15, euler1_f0=e1, euler2_f0=e2
        )
        expected_second = (K * LOG_TAU) ** 2 * moments.A2
        assert abs(res.euler_M_K_double_prime_0 - expected_second) < 1e-12
        assert abs(res.M_K_double_prime_0 - expected_second) < 1e-5
    # Also verify even mismatch defect limit Delta_{eta, K} / (eta^2 K^2 (log tau)^2) -> A_2
    even_defect = evaluate_even_mismatch_defect(
        f0, K=1.5, eta=5e-4, n_max=15, euler2_f0=e2
    )
    assert even_defect["abs_error_to_A2"] < 5e-4


# 4. Arithmetic curvature normalization is K-independent
def test_04_arithmetic_curvature_normalization_is_k_independent():
    f0, e1, e2 = _sample_gaussian_log_kernel()
    moments = evaluate_euler_moments_A0_A1_A2(f0, n_max=15, euler1_f0=e1, euler2_f0=e2)
    for K in [-3.0, -1.0, 0.5, 1.0, 2.0, 4.0]:
        res = evaluate_mismatch_derivatives_at_zero(
            f0, K=K, n_max=15, euler1_f0=e1, euler2_f0=e2
        )
        assert abs(res.normalized_curvature_from_K - moments.arithmetic_curvature) < 1e-10


# 5. Single exponential gives zero curvature
def test_05_single_exponential_gives_zero_curvature():
    res = evaluate_exponential_mixture_curvature(weights=[2.5], exponents=[1.37])
    assert abs(res.curvature_determinant) < 1e-15
    assert abs(res.pairwise_lagrange_sum) < 1e-15
    assert not res.strictly_positive


# 6. Two positive exponents give strict positive curvature
def test_06_two_positive_exponents_give_strict_positive_curvature():
    res = evaluate_exponential_mixture_curvature(
        weights=[1.2, 0.8], exponents=[-0.5, 1.1]
    )
    expected = 1.2 * 0.8 * ((-0.5 - 1.1) ** 2)
    assert abs(res.curvature_determinant - expected) < 1e-14
    assert res.lagrange_identity_abs_err < 1e-14
    assert res.strictly_positive


# 7. Reciprocal pair gives strict positive curvature
def test_07_reciprocal_pair_gives_strict_positive_curvature():
    res = evaluate_reciprocal_pair_curvature(w1=1.5, w2=2.0, x=0.35)
    expected = 4.0 * 1.5 * 2.0 * (0.35 ** 2)
    assert abs(res.curvature_determinant - expected) < 1e-14
    assert res.strictly_positive


# 8. Signed weights defeat positivity
def test_08_signed_weights_defeat_positivity():
    res = evaluate_exponential_mixture_curvature(weights=[1.0, -2.0], exponents=[0.0, 1.0])
    assert res.curvature_determinant == pytest.approx(-2.0, abs=1e-15)
    assert res.curvature_determinant < 0.0
    assert not res.nonnegative


# 9. Homogeneous kernel gives zero arithmetic curvature
def test_09_homogeneous_kernel_gives_zero_arithmetic_curvature():
    hom = evaluate_homogeneous_kernel_control(alpha=0.4, beta=0.6, n_max=15)
    assert hom["is_flat"] is True
    assert abs(hom["arithmetic_curvature"]) < 1e-10
    assert hom["A1_minus_d_A0"] < 1e-12
    assert hom["A2_minus_d2_A0"] < 1e-12
    assert hom["single_character_response_abs_err"] < 1e-12


# 10. Nonzero compact-support homogeneous control fails
def test_10_nonzero_compact_support_homogeneous_control_fails():
    audit = audit_compact_support_homogeneity_no_go(degree_d=-1.0)
    assert audit.ray_scaling_verified is True
    assert audit.compact_support_compatible_for_nonzero_kernel is False
    assert audit.classification == CLASSIFICATION_COMPACT_SUPPORT_IMPOSSIBLE
    assert audit.outcome_code == OUTCOME_C_COMPACT_SUPPORT_NO_GO


# 11. Finite-station accidental zero classification
def test_11_finite_station_accidental_zero_classification():
    ctrl = audit_finite_station_accidental_zero()
    assert ctrl["vanishes_on_selected_window"] is True
    assert ctrl["breaks_on_expanded_window"] is True
    assert ctrl["classification"] == CLASSIFICATION_FINITE_ACCIDENTAL_ZERO


# 12. Fixed generic kernel may have positive curvature
def test_12_fixed_generic_kernel_may_have_positive_curvature():
    sign_audit = audit_arithmetic_curvature_sign_firewall(n_max=15)
    assert sign_audit["positive_kernel_A0"] > 0.0
    assert sign_audit["positive_kernel_curvature"] > 0.0


# 13. Fixed generic kernel may have negative curvature
def test_13_fixed_generic_kernel_may_have_negative_curvature():
    sign_audit = audit_arithmetic_curvature_sign_firewall(n_max=15)
    assert sign_audit["negative_kernel_A0"] > 0.0
    assert sign_audit["negative_kernel_curvature"] < 0.0
    assert sign_audit["all_three_signs_realized"] is True
    assert sign_audit["classification"] == CLASSIFICATION_ARITHMETIC_INDEFINITE
    assert sign_audit["outcome_b_flatness_not_implied"] == OUTCOME_B_ARITHMETIC_FLATNESS_NOT_IMPLIED


# 14. Mellin mismatch factor
def test_14_mellin_mismatch_factor():
    s = complex(0.62, 14.134725)
    t = complex(0.62, -14.134725)
    res = evaluate_mellin_mismatch_scaling(s=s, t=t, K=2.0, eta=0.1, a=1.0)
    expected_net_exp = 0.1 * 2.0 * (s + t)
    assert abs(res["net_normalized_exponent"] - expected_net_exp) < 1e-14
    assert abs(res["first_eta_derivative_at_0"] - 2.0 * LOG_TAU * (s + t)) < 1e-14
    assert abs(res["second_eta_derivative_at_0"] - (2.0 * LOG_TAU) ** 2 * ((s + t) ** 2)) < 1e-12


# 15. Centered conjugate pairing yields radial exponent
def test_15_centered_conjugate_pairing_yields_radial_exponent():
    delta = 0.14
    gamma = 14.134725
    audit = audit_spectral_centering_and_pairings(delta=delta, gamma=gamma, K=1.0, eta=0.1)
    assert abs(audit.centered_conjugate_exponent.real - 2.0 * delta) < 1e-15
    assert abs(audit.centered_conjugate_exponent.imag) < 1e-15
    assert audit.conjugate_even_defect > 0.0
    assert audit.conjugate_second_variation_coeff == pytest.approx(
        4.0 * (LOG_TAU ** 2) * (delta ** 2), rel=1e-14
    )


# 16. Reflection pairing yields ordinate exponent
def test_16_reflection_pairing_yields_ordinate_exponent():
    delta = 0.14
    gamma = 14.134725
    audit = audit_spectral_centering_and_pairings(delta=delta, gamma=gamma, K=1.0, eta=0.1)
    assert abs(audit.centered_reflection_exponent.real) < 1e-15
    assert abs(audit.centered_reflection_exponent.imag - 2.0 * gamma) < 1e-15
    assert audit.reflection_even_defect <= 0.0
    assert audit.reflection_second_variation_coeff == pytest.approx(
        -4.0 * (LOG_TAU ** 2) * (gamma ** 2), rel=1e-14
    )


# 17. General zero-zero pairing yields cross terms
def test_17_general_zero_zero_pairing_yields_cross_terms():
    audit = audit_spectral_centering_and_pairings(
        delta=0.12, gamma=14.134725, sigma_delta=-0.05, sigma_gamma=21.022040
    )
    assert abs(audit.general_pair_centered_exponent.real - (0.12 - 0.05)) < 1e-15
    assert abs(audit.general_pair_centered_exponent.imag - (14.134725 + 21.022040)) < 1e-12
    assert audit.naturally_induced_pairing == "UNRESTRICTED_DOUBLE_ZERO_SUM_WITH_BACKGROUND"
    assert audit.spectral_curvature_classification == OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE


# 18. No diagonal projection without proof
def test_18_no_diagonal_projection_without_proof():
    fw = audit_complete_spectral_curvature_and_firewalls()
    assert fw["diagonal_projection_without_proof_allowed"] is False
    assert fw["incomplete_diagonal_only_classification"] == CLASSIFICATION_SELECTED_BLOCK_ONLY
    assert fw["includes_zero_zero_cross_terms"] is True


# 19. No selected-zero test construction
def test_19_no_selected_zero_test_construction():
    fw = audit_complete_spectral_curvature_and_firewalls()
    assert fw["selected_zero_construction_allowed"] is False


# 20. No remainder-domination reuse
def test_20_no_remainder_domination_reuse():
    fw = audit_complete_spectral_curvature_and_firewalls()
    assert fw["remainder_domination_reopened"] is False
    assert fw["task_tc_032r_firewall_status"] == "EXACT_CANCELLATION_BLOCKS_STRICT_SUBORDINATION_ROUTE"
    assert fw["includes_pole_terms"] is True
    assert fw["includes_trivial_zero_terms"] is True
    assert fw["includes_archimedean_terms"] is True


# 21. Theta scalar candidate remains rejected
def test_21_theta_scalar_candidate_remains_rejected():
    theta = audit_theta_mellin_nonscalar_fallback()
    assert theta.scalar_candidate_status == "REJECTED_FROZEN_IDENTICALLY_ZERO_AT_ZEROS"


# 22. Theta non-scalar candidate evidence status
def test_22_theta_non_scalar_candidate_evidence_status():
    theta = audit_theta_mellin_nonscalar_fallback()
    assert theta.purely_theta_or_arithmetic_defined is True
    assert theta.zero_independent_definition is True
    assert theta.exact_scale_flatness_law is False
    assert theta.reduces_to_double_mellin_weil_form is True
    assert theta.closes_obl_ct_001a is False
    assert theta.classification == OUTCOME_G_REDUCES_TO_OBL_CT_001A


# 23. Generic-base classification
def test_23_generic_base_classification():
    gb = evaluate_generic_base_mismatch_control()
    assert gb["holds_for_all_q_gt_1"] is True
    assert gb["tau_specific_theorem_used_in_euler_curvature"] is False
    assert gb["classification"] == CLASSIFICATION_GENERIC_SCALE_CURVATURE


# 24. Weil-equivalence firewall
def test_24_weil_equivalence_firewall():
    wf = audit_weil_equivalence_firewall()
    assert wf["global_spectral_form_positivity_is_rh_equivalent"] is True
    assert wf["independent_proof_mechanism"] is False
    assert wf["classification"] == CLASSIFICATION_CURVATURE_POSITIVITY_RH_EQUIVALENT
    assert wf["outcome_e"] == OUTCOME_E_WEIL_EQUIVALENCE


# 25. No RH claim without full bridge
def test_25_no_rh_claim_without_full_bridge():
    report = audit_transport_mismatch_curvature()
    assert report["rh_claimed"] is False
    assert report["obl_ct_001a_completed"] is False
    assert report["principal_classification"] == PRINCIPAL_CLASSIFICATION
    assert report["principal_classification"] != OUTCOME_A_FULL_BRIDGE
    reconcil = reconcile_with_existing_curvature_transport()
    assert reconcil["classification"] == CLASSIFICATION_REDUCES_TO_EXISTING_OBL_CT_001A
    assert reconcil["new_arithmetic_descent_constructed"] is False


# 26. No claim that candidate failure refutes TC
def test_26_no_claim_that_candidate_failure_refutes_tc():
    report = audit_transport_mismatch_curvature()
    assert report["candidate_failure_refutes_tc"] is False
    assert "NOT the general TC hypothesis" in report["hypothesis_fidelity"]["distinction"]


# 27. Lean 4 module theorem alignment check
def test_27_lean_formalization_alignment():
    lean_file = (
        Path(__file__).resolve().parent.parent
        / "formal"
        / "RiemannScope"
        / "TransportMismatchCurvature.lean"
    )
    assert lean_file.exists()
    content = lean_file.read_text(encoding="utf-8")
    required_theorems = [
        "single_exponential_log_curvature_zero",
        "two_exponential_positive_log_curvature",
        "positive_finite_exponential_curvature_nonneg",
        "reciprocal_pair_curvature_strict_pos",
        "homogeneous_arithmetic_curvature_zero",
        "arithmetic_zero_curvature_and_spectral_positive_contradiction",
        "euler_generator_scaling_algebra",
        "mismatch_curvature_k_independent",
        "even_second_difference_quadratic_ident",
        "signed_weight_curvature_negative",
        "generic_base_mismatch_curvature_scaling",
    ]
    for thm in required_theorems:
        assert f"theorem {thm}" in content
    assert "sorry" not in content


# 28. Artifact and review document completeness
def test_28_artifact_and_review_completeness():
    import json

    repo_root = Path(__file__).resolve().parent.parent
    artifact_path = repo_root / "data" / "tc_transport_mismatch_curvature.json"
    review_path = repo_root / "docs" / "reviews" / "TC_TRANSPORT_MISMATCH_CURVATURE.md"
    assert artifact_path.exists()
    assert review_path.exists()

    data = json.loads(artifact_path.read_text(encoding="utf-8"))
    required_keys = [
        "starting_head",
        "mismatch_parameter",
        "transported_kernel",
        "arithmetic_derivative_formulas",
        "euler_operator",
        "arithmetic_curvature",
        "curvature_sign_status",
        "homogeneity_status",
        "compact_support_obstruction",
        "mellin_scaling",
        "centered_exponent_convention",
        "natural_zero_pairing",
        "spectral_curvature_type",
        "weight_sign",
        "cross_term_status",
        "theta_candidate_status",
        "tau_specificity",
        "weil_equivalence_status",
        "relation_to_OBL_CT_001A",
        "principal_classification",
        "exact_remaining_subgate",
    ]
    for key in required_keys:
        assert key in data

    review_text = review_path.read_text(encoding="utf-8")
    required_sections = [
        "### A. TASK-TC-033 transport–moment incompatibility",
        "### B. Hypothesis versus implementation",
        "### C. Relative transport parameter",
        "### D. Arithmetic Euler derivatives",
        "### E. Arithmetic curvature determinant",
        "### F. Positive exponential curvature identity",
        "### G. Mellin-side mismatch derivatives",
        "### H. Centering and pairing audit",
        "### I. Homogeneous-kernel candidate",
        "### J. Compact-support homogeneity obstruction",
        "### K. Complete spectral curvature",
        "### L. Off-diagonal and background terms",
        "### M. Existing Curvature Transport reconciliation",
        "### N. Theta–Mellin fallback",
        "### O. Tau-specificity",
        "### P. Weil-equivalence audit",
        "### Q. Principal classification",
        "### R. Exact next theorem, if any",
    ]
    for sec in required_sections:
        assert sec in review_text

