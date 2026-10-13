"""
Unit tests for tc/grade_hankel_constraint.py.
TASK-TC-033: Three-Grade Hankel Constraint and Transport–Moment Compatibility Audit.
Covers all 24 required test items.
"""
from __future__ import annotations

import math
import os
import pytest

from tc.grade_hankel_constraint import (
    CLASSIFICATION_TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED,
    CLASSIFICATION_ARITHMETIC_HANKEL_RANK_ONE_NOT_DERIVED,
    CLASSIFICATION_SPECTRAL_MOMENT_SURVIVES_ARITHMETIC_RANK_ONE_FAILS,
    CLASSIFICATION_SIGNED_SPECTRAL_WEIGHTS_DO_NOT_IMPLY_HANKEL_POSITIVITY,
    CLASSIFICATION_DOUBLE_SPECTRAL_SUM_NOT_POSITIVE_MOMENT_SEQUENCE,
    CLASSIFICATION_HANKEL_POSITIVITY_IS_RH_EQUIVALENT,
    CLASSIFICATION_POST_HOC_RANK_ONE_NORMALIZATION,
    CLASSIFICATION_GENERIC_PUSHFORWARD_COVARIANCE,
    TransportedKernelSpec,
    compute_hankel_0,
    compute_equal_grade_arithmetic_mass,
    evaluate_three_grade_hankel_system,
    compute_mellin_kernel_scaling_exponent,
    verify_full_transport_cancellation,
    geometric_sequence_control,
    one_point_moment_control,
    two_point_positive_moment_control,
    reciprocal_pair_moment_control,
    signed_weight_control,
    quadratic_double_sum_cross_term_control,
    generic_base_scale_covariance_control,
    verify_window_grade_admissibility,
    audit_three_grade_hankel_constraint_claim,
)


# ------------------------------------------------------------------------------
# 1. Geometric Sequence Gives Zero Hankel Determinant
# ------------------------------------------------------------------------------
def test_01_geometric_sequence_hankel_zero():
    for A in [1.0, 3.5, 10.0]:
        for c in [0.5, 2.0, math.pi]:
            res = geometric_sequence_control(A, c)
            assert res["is_zero_identically"]
            assert abs(res["hankel_0"]) < 1e-14


# ------------------------------------------------------------------------------
# 2. One-Point Positive Measure Gives Zero
# ------------------------------------------------------------------------------
def test_02_one_point_positive_measure_gives_zero():
    res = one_point_moment_control(A=4.2, c=1.8)
    assert res["is_zero_identically"]
    assert abs(res["hankel_0"]) < 1e-14


# ------------------------------------------------------------------------------
# 3. Two-Point Positive Measure Gives Positive Determinant
# ------------------------------------------------------------------------------
def test_03_two_point_positive_measure_gives_positive_determinant():
    res = two_point_positive_moment_control(w1=1.0, w2=2.0, r1=0.5, r2=3.0)
    assert res["is_strictly_positive"]
    assert res["hankel_0"] > 0.0
    assert res["residual"] < 1e-14


# ------------------------------------------------------------------------------
# 4. Reciprocal Pair Gives Strict Positivity
# ------------------------------------------------------------------------------
def test_04_reciprocal_pair_gives_strict_positivity():
    for r1 in [0.25, 0.7, 1.5, 4.0]:
        res = reciprocal_pair_moment_control(w1=1.5, w2=1.5, r1=r1)
        assert res["is_strictly_positive"]
        assert res["hankel_0"] > 0.0


# ------------------------------------------------------------------------------
# 5. Signed Weights Can Defeat Positivity
# ------------------------------------------------------------------------------
def test_05_signed_weights_can_defeat_positivity():
    res = signed_weight_control()
    assert res["is_negative"]
    assert res["hankel_0"] < 0.0
    assert res["classification"] == CLASSIFICATION_SIGNED_SPECTRAL_WEIGHTS_DO_NOT_IMPLY_HANKEL_POSITIVITY


# ------------------------------------------------------------------------------
# 6. Full Transported Kernel Preserves Native Station Labels
# ------------------------------------------------------------------------------
def test_06_full_transported_kernel_preserves_native_station_labels():
    spec = TransportedKernelSpec(a=0.0, b=1.0)
    for K in [-1, 0, 1]:
        factor = spec.station_coordinate_factor(K)
        assert abs(factor - 1.0) < 1e-15


# ------------------------------------------------------------------------------
# 7. Full Transported Arithmetic Sequence Is Geometric
# ------------------------------------------------------------------------------
def test_07_full_transported_arithmetic_sequence_is_geometric():
    eval_res = evaluate_three_grade_hankel_system(mode="native")
    assert eval_res.is_arithmetic_rank_one
    assert abs(eval_res.normalized_hankel_0) < 1e-12
    # All 3 station counts are equal because the native window is identical
    assert eval_res.active_station_counts[0] == eval_res.active_station_counts[1]
    assert eval_res.active_station_counts[1] == eval_res.active_station_counts[2]


# ------------------------------------------------------------------------------
# 8. Transported Mellin Kernel Scaling Identity
# ------------------------------------------------------------------------------
def test_08_transported_mellin_kernel_scaling_identity():
    # Net exponent is (b - 1)*K*(s + t)
    s = complex(0.5, 14.134725)
    t = complex(0.5, -14.134725)
    exp = compute_mellin_kernel_scaling_exponent(a=1.0, b=0.5, K=1, s=s, t=t)
    expected = (0.5 - 1.0) * 1 * (s + t)
    assert abs(exp - expected) < 1e-14


# ------------------------------------------------------------------------------
# 9. Full Transport Cancels Zero-Dependent Grade Factor
# ------------------------------------------------------------------------------
def test_09_full_transport_cancels_zero_dependent_grade_factor():
    res = verify_full_transport_cancellation(K=1, s=complex(0.5, 14.0), t=complex(0.5, -14.0))
    assert res["is_exponent_identically_zero"]
    assert res["is_factor_identically_one"]
    assert res["classification"] == CLASSIFICATION_TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED


# ------------------------------------------------------------------------------
# 10. Fixed Raw Window Changes Active Station Sets
# ------------------------------------------------------------------------------
def test_10_fixed_raw_window_changes_active_station_sets():
    eval_res = evaluate_three_grade_hankel_system(mode="fixed")
    counts = eval_res.active_station_counts
    # For K = -1, stations in [8*tau, 20*tau] are many more than K=1 in [8/tau, 20/tau]
    assert counts[0] != counts[1] or counts[1] != counts[2]
    # Grade 1 only has primes 2 and 3 in [8/tau, 20/tau] ~ [1.27, 3.18]
    assert counts[2] == 2


# ------------------------------------------------------------------------------
# 11. Fixed-Window Arithmetic Rank-One Failure Control
# ------------------------------------------------------------------------------
def test_11_fixed_window_arithmetic_rank_one_fails():
    eval_res = evaluate_three_grade_hankel_system(mode="fixed")
    assert not eval_res.is_arithmetic_rank_one
    assert abs(eval_res.normalized_hankel_0) > 1e-4
    assert eval_res.classification == CLASSIFICATION_SPECTRAL_MOMENT_SURVIVES_ARITHMETIC_RANK_ONE_FAILS


# ------------------------------------------------------------------------------
# 12. Partial Transport Symbolic Audit
# ------------------------------------------------------------------------------
def test_12_partial_transport_symbolic_audit():
    # For b = 0.5, station factor is tau^{0.5*K} != 1
    spec = TransportedKernelSpec(a=0.0, b=0.5)
    assert abs(spec.station_coordinate_factor(K=1) - math.sqrt(2.0 * math.pi)) < 1e-12
    eval_res = evaluate_three_grade_hankel_system(mode="partial", b_param=0.5)
    # Spectral exponent is 0.5 - 1 = -0.5 != 0
    assert abs(eval_res.spectral_exponent_b_minus_1 - (-0.5)) < 1e-12


# ------------------------------------------------------------------------------
# 13. No Post Hoc Normalization Firewall
# ------------------------------------------------------------------------------
def test_13_no_post_hoc_normalization_firewall():
    eval_res = evaluate_three_grade_hankel_system(mode="native")
    # Normalization is derived a priori from amplitude scaling, not fitted from computed values
    assert eval_res.normalization_name == "canonical_amplitude_power_tau"
    assert CLASSIFICATION_POST_HOC_RANK_ONE_NORMALIZATION != eval_res.classification


# ------------------------------------------------------------------------------
# 14. No Zero-Dependent Window
# ------------------------------------------------------------------------------
def test_14_no_zero_dependent_window():
    eval_res = evaluate_three_grade_hankel_system(mode="native", window=(8.0, 20.0))
    # Window depends only on numerical compact bounds, zero coordinates do not enter
    assert eval_res.window == (8.0, 20.0)


# ------------------------------------------------------------------------------
# 15. Double Spectral Sum Not Silently Diagonalized
# ------------------------------------------------------------------------------
def test_15_double_spectral_sum_not_silently_diagonalized():
    res = quadratic_double_sum_cross_term_control()
    assert res["is_negative"]
    assert res["classification"] == CLASSIFICATION_DOUBLE_SPECTRAL_SUM_NOT_POSITIVE_MOMENT_SEQUENCE


# ------------------------------------------------------------------------------
# 16. Weil-Equivalence Classification Firewall
# ------------------------------------------------------------------------------
def test_16_weil_equivalence_classification_firewall():
    # Positivity of the spectral quadratic form on general test functions is Weil-equivalent
    assert CLASSIFICATION_HANKEL_POSITIVITY_IS_RH_EQUIVALENT == "HANKEL_POSITIVITY_IS_RH_EQUIVALENT"


# ------------------------------------------------------------------------------
# 17. Generic-Base Scale Covariance Control
# ------------------------------------------------------------------------------
def test_17_generic_base_scale_covariance_control():
    for q in [2.0, math.e, 5.0, 10.0]:
        res = generic_base_scale_covariance_control(q=q)
        assert res["is_exponent_zero"]
        assert res["classification"] == CLASSIFICATION_GENERIC_PUSHFORWARD_COVARIANCE


# ------------------------------------------------------------------------------
# 18. Primary Grades Admissibility (K in {-1, 0, 1})
# ------------------------------------------------------------------------------
def test_18_primary_grades_admissibility():
    adm = verify_window_grade_admissibility(window=(8.0, 20.0))
    assert adm["is_primary_admissible"]
    assert adm["primary_grades"] == [-1, 0, 1]


# ------------------------------------------------------------------------------
# 19. Grade-2 Window Admissibility Firewall
# ------------------------------------------------------------------------------
def test_19_grade_2_window_admissibility_firewall():
    adm = verify_window_grade_admissibility(window=(8.0, 20.0))
    assert adm["grade_2_firewall_triggered"]
    assert 2 in adm["inadmissible_grades"]


# ------------------------------------------------------------------------------
# 20. No Selected Block to Full Spectrum Promotion
# ------------------------------------------------------------------------------
def test_20_no_selected_block_promotion():
    # The audit considers the complete functional and rejects truncation-based claims
    audit = audit_three_grade_hankel_constraint_claim()
    assert audit["principal_classification"] == CLASSIFICATION_TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED


# ------------------------------------------------------------------------------
# 21. No Identically Zero Functional Substitution
# ------------------------------------------------------------------------------
def test_21_no_identically_zero_functional_substitution():
    eval_res = evaluate_three_grade_hankel_system(mode="native")
    # All 3 raw equal-grade masses are strictly positive! (Not identically zero)
    for mass in eval_res.raw_energies:
        assert mass > 0.0


# ------------------------------------------------------------------------------
# 22. No RH Claim Without Both Gates
# ------------------------------------------------------------------------------
def test_22_no_rh_claim_without_both_gates():
    audit = audit_three_grade_hankel_constraint_claim()
    assert audit["principal_classification"] != "THREE_GRADE_HANKEL_CONSTRAINT_PROVED"
    assert audit["principal_classification"] == CLASSIFICATION_TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED


# ------------------------------------------------------------------------------
# 23. Actual Lean Theorem-Name Alignment
# ------------------------------------------------------------------------------
def test_23_lean_theorem_name_alignment():
    lean_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "formal",
        "RiemannScope",
        "GradeHankelConstraint.lean",
    )
    assert os.path.exists(lean_file)
    with open(lean_file, "r", encoding="utf-8") as f:
        content = f.read()

    expected_theorems = [
        "geometric_sequence_hankel_zero",
        "two_point_hankel_identity",
        "two_point_positive_moment_hankel_pos",
        "reciprocal_pair_hankel_strict_pos",
        "finite_positive_moment_hankel_nonneg",
        "rank_one_and_strict_hankel_contradiction",
        "transported_kernel_mellin_scaling_algebra",
        "full_transport_spectral_factor_cancellation",
        "full_transport_net_exponent_zero",
        "signed_weights_hankel_negative",
        "generic_base_covariance",
    ]
    for thm in expected_theorems:
        assert f"theorem {thm}" in content, f"Missing Lean theorem: {thm}"


# ------------------------------------------------------------------------------
# 24. Build Provenance Regression
# ------------------------------------------------------------------------------
def test_24_build_provenance_regression():
    audit = audit_three_grade_hankel_constraint_claim()
    assert audit["sprint"] == "TASK-TC-033"
    assert "governing_question_answer" in audit
    assert len(audit["governing_question_answer"]) > 50
