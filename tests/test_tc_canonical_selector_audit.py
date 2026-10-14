"""
Unit and regression tests for `TASK-TC-035` (`tc/canonical_selector_audit.py` and
`formal/RiemannScope/CanonicalSelectorAudit.lean`): Canonical Zeta Selector Principle
and Uniqueness Audit.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from tc.canonical_selector_audit import (
    ARB_CERTIFICATION_NOT_AVAILABLE,
    INVERSION_SYMMETRIC_NEG_CERTIFIED,
    INVERSION_SYMMETRIC_POS_CERTIFIED,
    INVERSION_SYMMETRY_SIGN_INDEFINITE_STATUS,
    LOG_GAUSSIAN_VARIANCE_THRESHOLD_PROVED,
    OBL_CT_001A_STATUS,
    PRINCIPAL_CLASSIFICATION,
    SECONDARY_TRILEMMA_CLASSIFICATION,
    SELECTOR_I_FUNCTIONAL_EQUATION_STATUS,
    SELECTOR_II_THETA_SELF_DUALITY_STATUS,
    SELECTOR_III_PRIME_ARCHIMEDEAN_STATUS,
    SELECTOR_IV_VARIATIONAL_EXTREMAL_STATUS,
    SELECTOR_V_OPERATOR_TRACE_STATUS,
    SELECTOR_VI_STRONG_NATURALITY_STATUS,
    TASK_TC_035_ID,
    TASK_TC_035_STATUS,
    TENSOR_SQUARE_REDUCTION_PROVED,
    THETA_GAUSSIAN_NEG_CERTIFIED,
    audit_canonical_zeta_selector,
    audit_selector_trilemma,
    audit_six_candidate_selectors,
    certify_canonical_theta_gaussian_curvature_arb,
    certify_inversion_symmetric_witness_arb,
    evaluate_inversion_symmetric_witness_jet,
    evaluate_log_gaussian_variance_threshold,
    evaluate_separable_tensor_square_reduction,
    get_selector_lean_theorem_map,
    log_symmetric_plateau_1d_euler_jet,
    log_symmetric_plateau_2d_euler_jet,
    verify_inversion_and_permutation_symmetries,
    verify_selector_lean_theorem_map_against_file,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_01_separable_tensor_square_curvature_reduction() -> None:
    """
    Verify Theorem 1 (`tensor_square_curvature_reduction`): for any separable kernel
    F_0(x, y) = f(x) f(y),
        A_0 = m_0^2,
        A_1 = 2 m_0 m_1,
        A_2 = 2 m_0 m_2 + 2 m_1^2,
        C_arith(f x f) = 2 m_0^2 (m_0 m_2 - m_1^2).
    """
    res = evaluate_separable_tensor_square_reduction()
    assert res.classification == TENSOR_SQUARE_REDUCTION_PROVED
    assert res.A0_abs_err < 1e-13
    assert res.A1_abs_err < 1e-12
    assert res.A2_abs_err < 1e-12
    assert res.curvature_identity_abs_err < 1e-10
    assert math.isclose(
        res.two_dim_curvature,
        2.0 * (res.m0 ** 2) * res.one_dim_curvature,
        rel_tol=1e-14,
    )


def test_02_log_inversion_symmetric_plateau_cutoff() -> None:
    """
    Verify the multiplicative-inversion-symmetric plateau cutoff X_inv around c_0 = 4:
    - identically 1 with zero Euler derivatives on [16/10.25, 10.25]^2 (covering all
      prime-power stations 2 <= n, m <= 10);
    - identically 0 outside (16/10.5, 10.5)^2 (excluding all stations >= 11 and <= 1);
    - invariant under x |-> 16 / x.
    """
    for n in (2, 3, 4, 5, 7, 8, 9):
        chi, d1, d2 = log_symmetric_plateau_1d_euler_jet(float(n), c0=4.0)
        assert chi == 1.0
        assert d1 == 0.0
        assert d2 == 0.0

    for ext in (1.0, 1.5, 10.5, 11.0, 13.0, 16.0):
        chi, d1, d2 = log_symmetric_plateau_1d_euler_jet(ext, c0=4.0)
        assert chi == 0.0
        assert d1 == 0.0
        assert d2 == 0.0

    # Check inversion symmetry on the smooth ramp (10.25, 10.5)
    for x in (10.30, 10.35, 10.40, 10.45):
        x_inv = 16.0 / x
        c1, e1, e2 = log_symmetric_plateau_1d_euler_jet(x, c0=4.0)
        c1_inv, e1_inv, e2_inv = log_symmetric_plateau_1d_euler_jet(x_inv, c0=4.0)
        assert 0.0 < c1 < 1.0
        assert abs(c1 - c1_inv) < 1e-14
        # Under x |-> 16/x, x d/dx changes sign and (x d/dx)^2 is invariant
        assert abs(e1 + e1_inv) < 1e-11
        assert math.isclose(e2, e2_inv, rel_tol=1e-12, abs_tol=1e-9)

    X0, EX, E2X = log_symmetric_plateau_2d_euler_jet(3.0, 7.0, c0=4.0)
    assert (X0, EX, E2X) == (1.0, 0.0, 0.0)


def test_03_inversion_and_permutation_symmetric_witnesses_arb() -> None:
    """
    Verify Selector I firewall: on the subspace of compactly supported smooth kernels
    F_0 in C_c^infty((0, infty)^2) that are simultaneously nonnegative, permutation-
    symmetric F(x, y) = F(y, x), and multiplicative-inversion-symmetric
    F(16/x, 16/y) = F(x, y), 128-bit Arb certifies both strictly negative and strictly
    positive complete arithmetic curvature.
    """
    sym = verify_inversion_and_permutation_symmetries(c0=4.0)
    assert sym["permutation_symmetric"] is True
    assert sym["inversion_symmetric"] is True
    assert sym["compactly_supported"] is True
    assert sym["nonnegative"] is True
    assert sym["active_station_set"] == [2, 3, 4, 5, 7, 8, 9]

    neg_cert = certify_inversion_symmetric_witness_arb("negative", prec_bits=128)
    assert neg_cert["certified"] is True
    assert neg_cert["status"] == INVERSION_SYMMETRIC_NEG_CERTIFIED
    assert neg_cert["is_complete_compact_support_sum"] is True
    assert neg_cert["curvature_enclosure"]["strictly_negative"] is True
    assert neg_cert["curvature_enclosure"]["strictly_positive"] is False
    assert neg_cert["zero_excluded"] is True
    assert neg_cert["curvature_enclosure"]["mid_display_float"] < -4379.0

    pos_cert = certify_inversion_symmetric_witness_arb("positive", prec_bits=128)
    assert pos_cert["certified"] is True
    assert pos_cert["status"] == INVERSION_SYMMETRIC_POS_CERTIFIED
    assert pos_cert["is_complete_compact_support_sum"] is True
    assert pos_cert["curvature_enclosure"]["strictly_positive"] is True
    assert pos_cert["curvature_enclosure"]["strictly_negative"] is False
    assert pos_cert["zero_excluded"] is True
    assert pos_cert["curvature_enclosure"]["mid_display_float"] > 25489.0

    fallback = certify_inversion_symmetric_witness_arb(
        "negative", force_flint_unavailable=True
    )
    assert fallback["certified"] is False
    assert fallback["status"] == ARB_CERTIFICATION_NOT_AVAILABLE


def test_04_canonical_theta_gaussian_negative_euler_curvature_arb() -> None:
    """
    Verify Selector II audit and Theorem 2 (`euler_chain_rule_second_deriv_curvature`):
    for the canonical Jacobi theta self-dual Gaussian Theta_1(x, y) = exp(-pi*(x^2 + y^2))
    at t = 1, the additive Bernstein variance 4*pi^2*(M_0*M_2 - M_1^2) > 0 is dominated
    by the negative multiplicative Euler chain-rule drift -4*pi*M_0*M_1 < 0 by 5 orders
    of magnitude, certifying C_arith(Theta_1) < 0 both on X_{15} and on the infinite
    prime-power lattice N_{>=2}^2.
    """
    theta_cert = certify_canonical_theta_gaussian_curvature_arb(
        t=1.0, N_cutoff=15, prec_bits=128
    )
    assert theta_cert["certified"] is True
    assert theta_cert["status"] == THETA_GAUSSIAN_NEG_CERTIFIED
    assert theta_cert["bernstein_term_positive"] is True
    assert theta_cert["drift_term_negative"] is True
    assert theta_cert["drift_dominates_bernstein"] is True
    assert theta_cert["chain_rule_identity_verified"] is True
    assert theta_cert["compact_support_curvature_enclosure"]["strictly_negative"] is True
    assert theta_cert["infinite_lattice_curvature_enclosure"]["strictly_negative"] is True
    assert theta_cert["zero_excluded"] is True

    fallback = certify_canonical_theta_gaussian_curvature_arb(
        force_flint_unavailable=True
    )
    assert fallback["certified"] is False
    assert fallback["status"] == ARB_CERTIFICATION_NOT_AVAILABLE


def test_05_multiplicative_log_gaussian_variance_threshold() -> None:
    """
    Verify Theorem 3 (`log_gaussian_curvature_identity`):
        C_arith(F_{alpha, w0}) = 16*alpha^2*(S_0*S_2 - S_1^2) - 8*alpha*S_0^2.
    """
    res_15 = evaluate_log_gaussian_variance_threshold(alpha=1.5)
    assert res_15.identity_abs_err < 1e-9
    assert res_15.arithmetic_curvature_direct < 0.0
    assert res_15.sign_regime == "SUBCRITICAL_VARIANCE_NEGATIVE_CURVATURE"

    res_005 = evaluate_log_gaussian_variance_threshold(alpha=0.05)
    assert res_005.identity_abs_err < 1e-9
    assert res_005.arithmetic_curvature_direct < 0.0


def test_06_six_candidate_selectors_and_trilemma() -> None:
    """
    Verify that all six candidate selector mechanisms are audited with explicit statuses,
    non-Boolean string classifications, and primary literature references, and that
    `OBL-CT-001A` remains `OPEN`.
    """
    selectors = audit_six_candidate_selectors()
    assert len(selectors) == 6
    expected_ids = [f"SELECTOR-{r}" for r in ("I", "II", "III", "IV", "V", "VI")]
    assert [s.selector_id for s in selectors] == expected_ids

    expected_classifications = [
        SELECTOR_I_FUNCTIONAL_EQUATION_STATUS,
        SELECTOR_II_THETA_SELF_DUALITY_STATUS,
        SELECTOR_III_PRIME_ARCHIMEDEAN_STATUS,
        SELECTOR_IV_VARIATIONAL_EXTREMAL_STATUS,
        SELECTOR_V_OPERATOR_TRACE_STATUS,
        SELECTOR_VI_STRONG_NATURALITY_STATUS,
    ]
    assert [s.classification for s in selectors] == expected_classifications

    for s in selectors:
        assert isinstance(s.selects_unique_test_kernel_status, str)
        assert isinstance(s.arithmetic_curvature_constraint_status, str)
        assert isinstance(s.spectral_positivity_or_isolation_status, str)
        assert len(s.primary_literature_references) >= 2

    trilemma = audit_selector_trilemma()
    assert trilemma["classification"] == SECONDARY_TRILEMMA_CLASSIFICATION
    assert trilemma["obl_ct_001a_status"] == "OPEN"
    assert len(trilemma["branches"]) == 3


def test_07_lean_theorem_map_exact_synchronization() -> None:
    """
    Verify that `formal/RiemannScope/CanonicalSelectorAudit.lean` contains the exact 16
    declarations (`1 def` + `15 theorem`s) listed in `get_selector_lean_theorem_map()`,
    with `0 sorry` and `0 admit`.
    """
    sync = verify_selector_lean_theorem_map_against_file()
    assert sync["matches_exact"] is True
    assert len(sync["actual_defs"]) == 1
    assert len(sync["actual_theorems"]) == 15
    assert sync["contains_sorry"] is False
    assert sync["contains_admit"] is False


def test_08_json_artifact_and_master_audit_consistency() -> None:
    """
    Verify that `data/tc_canonical_zeta_selector_audit.json` exists and matches the
    master audit entrypoint `audit_canonical_zeta_selector()`.
    """
    json_path = REPO_ROOT / "data" / "tc_canonical_zeta_selector_audit.json"
    assert json_path.exists(), f"Missing {json_path}"
    saved = json.loads(json_path.read_text(encoding="utf-8"))
    live = audit_canonical_zeta_selector()

    assert saved["task_id"] == TASK_TC_035_ID == "TASK-TC-035"
    assert saved["task_completion_status"] == TASK_TC_035_STATUS
    assert saved["principal_classification"] == PRINCIPAL_CLASSIFICATION
    assert saved["secondary_trilemma_classification"] == SECONDARY_TRILEMMA_CLASSIFICATION
    assert saved["obl_ct_001a_status"] == "OPEN"
    assert OBL_CT_001A_STATUS == "OBL_CT_001A_REMAINS_OPEN"
    assert saved["obl_ct_001a_completed"] is False
    assert saved["rh_claimed"] is False
    assert saved["candidate_selector_exhaustion_refutes_tc"] is False
    assert len(saved["arxiv_literature_retrieved"]) == 12
    assert (
        saved["inversion_and_permutation_symmetry_audit"]["classification"]
        == INVERSION_SYMMETRY_SIGN_INDEFINITE_STATUS
    )
    assert (
        saved["multiplicative_log_gaussian_variance_audit"]["classification"]
        == LOG_GAUSSIAN_VARIANCE_THRESHOLD_PROVED
    )
    assert saved["lean_theorem_map"]["module_theorem_count"] == 15
    assert saved["lean_theorem_map"]["repository_compiled_theorem_declarations"] == 580
    assert saved == live
