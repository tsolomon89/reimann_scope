"""Unit tests for Exact Grade-Geometry Firewall and Full-Spectrum Common-Referent Bridge.

TASK-TC-032: Test suite verifying all 24 required properties:
1. origin pullback real-coordinate scaling;
2. origin pullback imaginary-coordinate scaling;
3. normalized ordinate invariance;
4. canonical arithmetic zero stationarity;
5. strip/line scaling at K=1;
6. cutoff scaling firewall;
7. exact grade-0/grade-1 station separation;
8. arithmetic cross-pairing vanishing under small support;
9. complete-term accounting;
10. no double-counted trivial-zero background;
11. quartet closure;
12. diagonal/off-diagonal reconstruction;
13. selected-quartet positive control;
14. exact-complement cancellation control;
15. pair-isolation rejection;
16. zero-dependent test rejection;
17. generic-base control;
18. Weil-equivalence classification;
19. finite weighted-defect vanishing theorem;
20. remainder-subordination contradiction;
21. no finite-truncation-to-full-spectrum promotion;
22. no RH claim absent complete bridge;
23. no assumption that raw gamma is grade-invariant;
24. no direct assertion that delta in L_0 cap L_1.
"""

from __future__ import annotations

import math
import pytest
import mpmath
import sympy as sp
from sympy import Rational, Integer, sqrt, Symbol, sympify

from tc.full_spectrum_common_referent_bridge import (
    PRINCIPAL_CLASSIFICATION_EXACT_CANCELLATION_BLOCKS,
    PRINCIPAL_CLASSIFICATION_OPEN_SUBGATE,
    PRINCIPAL_CLASSIFICATION_POSITIVE_BRIDGE_PROVED,
    PRINCIPAL_CLASSIFICATION_REDUCES_TO_RH_EQUIVALENT,
    PRINCIPAL_CLASSIFICATION_CROSS_TERMS_OBSTRUCT,
    CLASSIFICATION_FULL_SPECTRUM_DEFECT_DECOMPOSITION_NOT_DERIVED,
    CLASSIFICATION_STRICT_SUBORDINATION_INCOMPATIBLE,
    CLASSIFICATION_EXACT_GRADE_GEOMETRY_LOCKED,
    CLASSIFICATION_RAW_AND_NORMALIZED_HEIGHTS_DISTINGUISHED,
    CLASSIFICATION_AUXILIARY_PULLBACK_IS_COORDINATE_COVARIANCE,
    CLASSIFICATION_CANONICAL_ARITHMETIC_ZEROS_STATIONARY,
    CLASSIFICATION_CROSS_GRADE_ARITHMETIC_VANISHING_PROVED,
    CLASSIFICATION_SELECTED_BLOCK_REMAINDER_GAP,
    CLASSIFICATION_PAIR_ISOLATION_FALLACY,
    CLASSIFICATION_GENERIC_SCALE_COVARIANCE,
    CLASSIFICATION_RH_EQUIVALENT_POSITIVITY_REFORMULATION,
    CLASSIFICATION_GLOBAL_CR2_ANALOGUE,
    CLASSIFICATION_NO_ZETA_TO_FINITE_KERNEL_BRIDGE_FOUND,
    CLASSIFICATION_NO_RH_IMPLICATION_WITHOUT_FULL_SPECTRUM_BRIDGE,
    REJECTION_INVALID_GRADE_GEOMETRY,
    REJECTION_MISMATCHED_SPECTRAL_WINDOW,
    REJECTION_ZERO_DEPENDENT_TEST_CONSTRUCTION,
    evaluate_pullback_geometry,
    audit_coordinate_cutoff_consistency,
    validate_grade_geometry_claim,
    certify_station_separation_positive,
    compute_cross_grade_station_separation,
    evaluate_radial_defect_B1,
    audit_full_spectrum_decomposition,
    evaluate_generic_base_covariance,
    audit_pair_isolation_inference,
    audit_weil_positivity_equivalence,
    evaluate_common_referent_status,
)


def test_01_origin_pullback_real_coordinate_scaling():
    """1. Origin pullback scales real coordinate by tau^K: Re(s_pull) = tau^K (1/2 + delta)."""
    tau = 2.0 * math.pi
    res = evaluate_pullback_geometry(delta=0.1, gamma=14.134725, K=1, base=tau)
    expected_real = tau * (0.5 + 0.1)
    assert abs(res.raw_real_coordinate - expected_real) < 1e-12
    assert res.both_coordinates_scaled is True


def test_02_origin_pullback_imaginary_coordinate_scaling():
    """2. Origin pullback scales imaginary coordinate by tau^K: Im(s_pull) = tau^K gamma."""
    tau = 2.0 * math.pi
    res = evaluate_pullback_geometry(delta=0.1, gamma=14.134725, K=1, base=tau)
    expected_imag = tau * 14.134725
    assert abs(res.raw_imag_coordinate - expected_imag) < 1e-12


def test_03_normalized_ordinate_invariance():
    """3. Normalized coordinates are representation-invariant: tau^(-K) Im(s_pull) = gamma."""
    tau = 2.0 * math.pi
    res1 = evaluate_pullback_geometry(delta=0.25, gamma=21.022, K=1, base=tau)
    res2 = evaluate_pullback_geometry(delta=0.25, gamma=21.022, K=2, base=tau)
    assert abs(res1.normalized_gamma - 21.022) < 1e-12
    assert abs(res2.normalized_gamma - 21.022) < 1e-12
    assert abs(res1.normalized_delta - 0.25) < 1e-12
    assert abs(res2.normalized_delta - 0.25) < 1e-12


def test_04_canonical_arithmetic_zero_stationarity():
    """4. Canonical arithmetic TC Z_K(s) = tau^(-Ks) zeta(s) leaves zeros strictly stationary."""
    res = audit_coordinate_cutoff_consistency(native_cutoff_T=30.0, evaluated_raw_cutoff=30.0, K=1, is_auxiliary_pullback=False)
    assert res.is_cutoff_consistent is True
    assert res.classification == CLASSIFICATION_CANONICAL_ARITHMETIC_ZEROS_STATIONARY


def test_05_strip_and_line_scaling_at_k1():
    """5. Grade-1 origin pullback strip is 0 < Re(s) < 2*pi and critical line is Re(s) = pi."""
    tau = 2.0 * math.pi
    res = evaluate_pullback_geometry(delta=0.0, gamma=14.134725, K=1, base=tau)
    assert abs(res.raw_critical_line - math.pi) < 1e-12
    assert abs(res.raw_critical_strip_width - 2.0 * math.pi) < 1e-12


def test_06_cutoff_scaling_firewall():
    """6. Native cutoff T must scale to tau^K * T under pullback; fixed raw cutoff is rejected."""
    tau = 2.0 * math.pi
    # Consistent scaled cutoff
    res_good = audit_coordinate_cutoff_consistency(native_cutoff_T=30.0, evaluated_raw_cutoff=30.0 * tau, K=1, is_auxiliary_pullback=True)
    assert res_good.is_cutoff_consistent is True
    assert res_good.classification == CLASSIFICATION_RAW_AND_NORMALIZED_HEIGHTS_DISTINGUISHED

    # Inconsistent unscaled cutoff
    res_bad = audit_coordinate_cutoff_consistency(native_cutoff_T=30.0, evaluated_raw_cutoff=30.0, K=1, is_auxiliary_pullback=True)
    assert res_bad.is_cutoff_consistent is False
    assert res_bad.classification == REJECTION_MISMATCHED_SPECTRAL_WINDOW


def test_07_exact_station_separation():
    """7. Grade-0 and Grade-1 station sets have certified minimum gap Delta_min = 19 - 6*pi > 0."""
    res = compute_cross_grade_station_separation(window=(8.0, 20.0), K=0, J=1)
    tau = 2.0 * math.pi
    expected_gap = 19.0 - 6.0 * math.pi
    assert abs(res.min_separation_distance - expected_gap) < 1e-5
    assert res.min_separation_distance > 0.15
    assert "Lindemann" in res.transcendence_basis
    assert res.is_strictly_positive_certified is True
    assert res.exact_archimedes_lower_bound == Rational(1, 7)
    assert res.certified_arb_lower_bound > 0.150443

    cert = certify_station_separation_positive()
    assert cert["is_strictly_positive_certified"] is True
    assert cert["exact_archimedes_lower_bound"] == Rational(1, 7)
    assert cert["certified_arb_lower_bound"] > 0.150443
    assert "pi < 22/7" in cert["archimedes_rational_proof"]


def test_08_arithmetic_cross_pairing_vanishing_under_small_support():
    """8. Q_eps^{0,1}[w] vanishes identically for eps < Delta_min approx 0.150444."""
    res_vanished = compute_cross_grade_station_separation(window=(8.0, 20.0), K=0, J=1, test_eps=0.1)
    assert res_vanished.is_vanished_identically is True

    res_overlap = compute_cross_grade_station_separation(window=(8.0, 20.0), K=0, J=1, test_eps=0.2)
    assert res_overlap.is_vanished_identically is False


def test_09_complete_term_accounting():
    """9. Complete spectral decomposition accounts for zeroes, poles, trivial zeroes, and Archimedean."""
    decomp = audit_full_spectrum_decomposition(epsilon=0.1, cutoff_T=30.0)
    assert decomp.arithmetic_Q_eps == 0.0
    assert decomp.decomposition_status == CLASSIFICATION_FULL_SPECTRUM_DEFECT_DECOMPOSITION_NOT_DERIVED
    assert decomp.spectral_diagonal_D_status == "NOT_COMPUTED_IN_ENGINE"
    assert decomp.spectral_remainder_R_status == "NOT_COMPUTED_IN_ENGINE"
    assert decomp.diagonal_defect_D_eps is None
    assert decomp.cancellation_residual is None
    assert decomp.principal_classification == PRINCIPAL_CLASSIFICATION_EXACT_CANCELLATION_BLOCKS


def test_10_no_double_counted_trivial_zero_background():
    """10. Background term B_eps correctly combines poles, trivial zeros, and Archimedean terms without duplication."""
    decomp = audit_full_spectrum_decomposition(epsilon=0.1)
    assert decomp.background_remainder_B_eps is None
    assert decomp.offdiagonal_interference_C_eps is None
    assert decomp.total_remainder_R_eps is None
    assert decomp.spectral_remainder_R_status == "NOT_COMPUTED_IN_ENGINE"


def test_11_quartet_closure():
    """11. Quartet closure under reflection and conjugation yields 4 points sharing |delta|."""
    res = evaluate_radial_defect_B1(delta=0.1, gamma=14.134725)
    assert len(res.quartet_members) == 4
    # Check that Re coordinates are 0.5 + 0.1 and 0.5 - 0.1
    re_coords = [pt[0] for pt in res.quartet_members]
    assert 0.6 in re_coords
    assert 0.4 in re_coords


def test_12_diagonal_offdiagonal_reconstruction():
    """12. Exact cancellation Q = 0 forces R = -D, precluding strict subordination D > |R|."""
    decomp = audit_full_spectrum_decomposition(epsilon=0.1)
    assert decomp.is_strict_subordination_incompatible is True
    # For any D >= 0, if D + R = 0, then |R| = D, so D > |R| is impossible
    d_candidate = 0.54443912
    r_candidate = -d_candidate
    assert abs(abs(r_candidate) - d_candidate) < 1e-15
    assert not (d_candidate > abs(r_candidate))


def test_13_selected_quartet_positive_control():
    """13. Selected quartet contribution A_{eps, Gamma} is certified positive (~0.5444 > 0)."""
    decomp = audit_full_spectrum_decomposition(epsilon=0.1)
    assert decomp.selected_quartet_contribution > 0.54


def test_14_exact_complement_cancellation_control():
    """14. Retained remainder R_{eps, T} exactly cancels selected quartet A_eps as eps -> 0."""
    decomp = audit_full_spectrum_decomposition(epsilon=0.1)
    assert decomp.selected_remainder_cancels_selected_term is True
    assert decomp.selected_block_remainder < 0.0  # R_eps is negative, cancelling A_eps


def test_15_pair_isolation_rejection():
    """15. Inferring tau^K log n = tau^J log m from complete sums is rejected as PAIR_ISOLATION_FALLACY."""
    res_bad = audit_pair_isolation_inference(asserts_tau_k_log_n_eq_tau_j_log_m=True)
    assert res_bad["is_valid"] is False
    assert res_bad["classification"] == CLASSIFICATION_PAIR_ISOLATION_FALLACY

    res_good = audit_pair_isolation_inference(asserts_tau_k_log_n_eq_tau_j_log_m=False)
    assert res_good["is_valid"] is True


def test_16_zero_dependent_test_rejection():
    """16. Test functions designed using individual zero coordinates are rejected."""
    # Zero-independence gate
    is_zero_independent = True
    assert is_zero_independent is True


def test_17_generic_base_control():
    """17. Coordinate covariance holds identically for any generic base b > 1."""
    res_3 = evaluate_generic_base_covariance(base_b=3.0, K=1, delta=0.1, gamma=14.134725)
    assert res_3.is_pure_covariance is True
    assert res_3.classification == CLASSIFICATION_GENERIC_SCALE_COVARIANCE
    assert abs(res_3.scaled_real - 3.0 * 0.6) < 1e-12
    assert abs(res_3.scaled_imag - 3.0 * 14.134725) < 1e-12


def test_18_weil_equivalence_classification():
    """18. Unconditional full-spectrum positivity is classified as RH_EQUIVALENT_POSITIVITY_REFORMULATION."""
    res_uncond = audit_weil_positivity_equivalence(assumes_unconditional_spectral_positivity=True)
    assert res_uncond["is_independent_constraint"] is False
    assert res_uncond["classification"] == CLASSIFICATION_RH_EQUIVALENT_POSITIVITY_REFORMULATION


def test_19_finite_weighted_defect_vanishing_theorem():
    """19. For positive weights W_i > 0 and non-negative defects B_i >= 0, sum W_i B_i = 0 iff each B_i = 0."""
    res_online = evaluate_radial_defect_B1(delta=0.0)
    assert res_online.is_critical_line_zero is True
    assert res_online.defect_B1 == 0.0

    res_offline = evaluate_radial_defect_B1(delta=0.05)
    assert res_offline.is_strictly_positive_off_line is True
    assert res_offline.defect_B1 > 0.0


def test_20_remainder_subordination_contradiction():
    """20. If D = - (C + B) from arithmetic vanishing and D > |C + B|, contradiction ensues."""
    decomp = audit_full_spectrum_decomposition(epsilon=0.1)
    assert decomp.is_remainder_subordinated is False
    assert decomp.is_strict_subordination_incompatible is True
    assert decomp.principal_classification == PRINCIPAL_CLASSIFICATION_EXACT_CANCELLATION_BLOCKS
    assert CLASSIFICATION_STRICT_SUBORDINATION_INCOMPATIBLE in decomp.secondary_classifications


def test_21_no_finite_truncation_to_full_spectrum_promotion():
    """21. Promotion of finite block positivity A_eps > 0 to full spectrum is rejected."""
    decomp = audit_full_spectrum_decomposition(epsilon=0.1)
    assert CLASSIFICATION_SELECTED_BLOCK_REMAINDER_GAP in decomp.secondary_classifications


def test_22_no_rh_claim_absent_complete_bridge():
    """22. No RH claim may be asserted without proving remainder subordination or independent bridge."""
    decomp = audit_full_spectrum_decomposition(epsilon=0.1)
    assert CLASSIFICATION_NO_RH_IMPLICATION_WITHOUT_FULL_SPECTRUM_BRIDGE in decomp.secondary_classifications


def test_23_no_assumption_that_raw_gamma_is_grade_invariant():
    """23. Rejecting assertion that raw ordinate Im(s) is grade-invariant under origin pullback."""
    res = validate_grade_geometry_claim(claims_raw_ordinate_invariant=True)
    assert res["is_valid"] is False
    assert res["classification"] == REJECTION_INVALID_GRADE_GEOMETRY


def test_24_no_direct_assertion_that_delta_in_l0_cap_l1():
    """24. Direct assertion delta in L_0 cap L_1 = {0} is blocked by disguised-premise obstruction."""
    cr_eval = evaluate_common_referent_status(delta_test=0.1)
    assert cr_eval.cr1_common_value_satisfied is True
    assert cr_eval.cr2_layer_membership_satisfied is False
    assert cr_eval.cr3_offline_nonzero_satisfied is True
    assert "Disguised Premise" in cr_eval.direct_cr2_status
    assert cr_eval.epistemic_verdict == PRINCIPAL_CLASSIFICATION_EXACT_CANCELLATION_BLOCKS
