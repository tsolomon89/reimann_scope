"""
Regression Test Suite for Infinitesimal Transport-Mismatch Curvature and Evidence Repair
(`TASK-TC-034` / `TASK-TC-034R`).

Verifies all 28 mandatory regression requirements from Section 17 of `TASK-TC-034R`,
as well as the exact Euler-generator curvature identities and spectral pairing audits
retained from `TASK-TC-034`.
"""

from __future__ import annotations

import json
from pathlib import Path

from tc.transport_mismatch_curvature import (
    ARB_CERTIFICATION_NOT_AVAILABLE,
    CLASSIFICATION_FINITE_ACCIDENTAL_ZERO,
    COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED,
    COMPACT_SUPPORT_NEG_CURVATURE_CERTIFIED,
    COMPACT_SUPPORT_NO_GO_EVIDENCE_STATUS,
    COMPACT_SUPPORT_POS_CURVATURE_CERTIFIED,
    COMPACT_SUPPORT_SIGN_INDEFINITENESS_STATUS,
    PRINCIPAL_CLASSIFICATION,
    SUPERSEDED_FINITE_TRUNCATION_STATUS,
    TASK_TC_034R_STATUS,
    THETA_MELLIN_AUDIT_CONDITIONAL,
    active_prime_power_stations,
    audit_arithmetic_curvature_sign_firewall,
    audit_compact_support_homogeneity_no_go,
    audit_complete_spectral_curvature_and_firewalls,
    audit_finite_station_accidental_zero,
    audit_spectral_centering_and_pairings,
    audit_theta_mellin_nonscalar_fallback,
    audit_transport_mismatch_curvature,
    audit_weil_equivalence_firewall,
    build_compact_negative_witness,
    build_compact_positive_witness,
    certify_compact_witness_curvature_arb,
    evaluate_euler_moments_A0_A1_A2,
    evaluate_exponential_mixture_curvature,
    evaluate_generic_base_mismatch_control,
    evaluate_homogeneous_kernel_control,
    evaluate_mellin_mismatch_scaling,
    evaluate_mismatch_derivatives_at_zero,
    evaluate_reciprocal_pair_curvature,
    get_lean_theorem_map,
    plateau_cutoff_1d_euler_jet,
    plateau_cutoff_1d_jet,
    plateau_cutoff_2d_euler_jet,
    reconcile_with_existing_curvature_transport,
    verify_lean_theorem_map_against_file,
    verify_station_jet_preservation,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = REPO_ROOT / "data" / "tc_transport_mismatch_curvature.json"
LEAN_FILE_PATH = REPO_ROOT / "formal" / "RiemannScope" / "TransportMismatchCurvature.lean"


def test_01_no_false_lean_reference_in_repo() -> None:
    """1. Repository contains no false Lean reference unless actually in TransportMismatchCurvature.lean."""
    false_ident = "compact_support_ray_" + "homogeneity_implies_zero"
    lean_text = LEAN_FILE_PATH.read_text(encoding="utf-8")
    assert false_ident not in lean_text

    search_dirs = [
        REPO_ROOT / "formal",
        REPO_ROOT / "tc",
        REPO_ROOT / "docs",
        REPO_ROOT / "data",
        REPO_ROOT / ".agents",
        REPO_ROOT / "tests",
    ]
    root_md_files = list(REPO_ROOT.glob("*.md"))
    offending_files: list[str] = []

    for f in root_md_files:
        if false_ident in f.read_text(encoding="utf-8", errors="ignore"):
            offending_files.append(str(f.relative_to(REPO_ROOT)))

    for d in search_dirs:
        for f in d.rglob("*"):
            if f.is_file() and f.suffix in {".md", ".lean", ".py", ".json"}:
                if false_ident in f.read_text(encoding="utf-8", errors="ignore"):
                    offending_files.append(str(f.relative_to(REPO_ROOT)))

    assert offending_files == [], f"False Lean reference found in: {offending_files}"


def test_02_compact_support_no_go_classified_as_paper_derivation() -> None:
    """2. Compact-support homogeneity no-go is classified as PROVED_PAPER_DERIVATION."""
    audit = audit_compact_support_homogeneity_no_go()
    assert audit.outcome_code == COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED
    assert audit.evidence_status == COMPACT_SUPPORT_NO_GO_EVIDENCE_STATUS
    assert audit.evidence_status == "PROVED_PAPER_DERIVATION"
    assert audit.lean_formalized is False
    assert audit.compact_support_compatible_for_nonzero_kernel is False
    assert len(audit.proof_steps) == 7


def test_03_plateau_cutoff_zero_outside_support() -> None:
    """3. Plateau cutoff vanishes for x <= a and x >= d."""
    a, b, c, d = 1.5, 1.75, 15.25, 15.5
    for x in [0.1, 0.5, 1.0, a, d, 16.0, 20.0, 100.0]:
        c0, c1, c2 = plateau_cutoff_1d_jet(x, a=a, b=b, c=c, d=d)
        assert c0 == 0.0
        assert c1 == 0.0
        assert c2 == 0.0

    for x in [1.0, 1.5, 15.5, 16.0]:
        for y in [2.0, 5.0, 16.0]:
            X0, EX, E2X = plateau_cutoff_2d_euler_jet(x, y, N_cutoff=15)
            assert X0 == 0.0
            assert EX == 0.0
            assert E2X == 0.0


def test_04_plateau_cutoff_one_on_active_station_interval() -> None:
    """4. Plateau cutoff equals 1 on [b, c]."""
    a, b, c, d = 1.5, 1.75, 15.25, 15.5
    for x in [b, 1.8, 2.0, 3.0, 5.0, 8.0, 13.0, 15.0, c]:
        c0, c1, c2 = plateau_cutoff_1d_jet(x, a=a, b=b, c=c, d=d)
        assert c0 == 1.0
        assert c1 == 0.0
        assert c2 == 0.0

    for n, _ in active_prime_power_stations(15):
        for m, _ in active_prime_power_stations(15):
            X0, _, _ = plateau_cutoff_2d_euler_jet(float(n), float(m), N_cutoff=15)
            assert X0 == 1.0


def test_05_first_cutoff_derivatives_vanish_at_active_stations() -> None:
    """5. First cutoff derivatives vanish at active stations 2 <= n <= N."""
    for n in range(2, 16):
        c0, c1, _ = plateau_cutoff_1d_euler_jet(float(n))
        assert c0 == 1.0
        assert c1 == 0.0
        for m in range(2, 16):
            _, EX, _ = plateau_cutoff_2d_euler_jet(float(n), float(m), N_cutoff=15)
            assert EX == 0.0


def test_06_second_cutoff_derivatives_vanish_at_active_stations() -> None:
    """6. Second cutoff derivatives vanish at active stations 2 <= n <= N."""
    for n in range(2, 16):
        _, _, c2 = plateau_cutoff_1d_euler_jet(float(n))
        assert c2 == 0.0
        for m in range(2, 16):
            _, _, E2X = plateau_cutoff_2d_euler_jet(float(n), float(m), N_cutoff=15)
            assert E2X == 0.0


def test_07_compactification_preserves_F_at_active_stations() -> None:
    """7. Compactification preserves F(n,m) at active stations."""
    for bundle in (build_compact_negative_witness(15), build_compact_positive_witness(15)):
        check = verify_station_jet_preservation(bundle)
        assert check["max_station_jet0_err"] == 0.0
        for n in bundle.active_station_set:
            for m in bundle.active_station_set:
                assert bundle.kernel_fn(float(n), float(m)) == bundle.prototype_fn(float(n), float(m))


def test_08_compactification_preserves_EF_at_active_stations() -> None:
    """8. Compactification preserves (E F)(n,m) at active stations."""
    for bundle in (build_compact_negative_witness(15), build_compact_positive_witness(15)):
        check = verify_station_jet_preservation(bundle)
        assert check["max_station_jet1_err"] == 0.0
        for n in bundle.active_station_set:
            for m in bundle.active_station_set:
                assert bundle.euler1_fn(float(n), float(m)) == bundle.prototype_euler1_fn(float(n), float(m))


def test_09_compactification_preserves_E2F_at_active_stations() -> None:
    """9. Compactification preserves (E^2 F)(n,m) at active stations."""
    for bundle in (build_compact_negative_witness(15), build_compact_positive_witness(15)):
        check = verify_station_jet_preservation(bundle)
        assert check["max_station_jet2_err"] == 0.0
        for n in bundle.active_station_set:
            for m in bundle.active_station_set:
                assert bundle.euler2_fn(float(n), float(m)) == bundle.prototype_euler2_fn(float(n), float(m))


def test_10_no_arithmetic_stations_outside_selected_complete_support() -> None:
    """10. No arithmetic stations exist outside [2, N]^2 within the compact support (1.5, 15.5)^2."""
    for bundle in (build_compact_negative_witness(15), build_compact_positive_witness(15)):
        check = verify_station_jet_preservation(bundle, extra_exterior_max=40)
        assert check["max_exterior_value_and_jet_abs"] == 0.0
        assert check["complete_sum_tail_difference_up_to_40"] == 0.0
        assert check["is_complete_compact_support_sum"] is True
        assert check["is_infinite_sum_truncation"] is False


def test_11_negative_witness_nonnegative_and_compactly_supported() -> None:
    """11. Negative witness is nonnegative and compactly supported."""
    bundle = build_compact_negative_witness(15)
    for x in [1.55, 1.65, 1.75, 2.0, 4.0, 8.0, 15.25, 15.35, 15.45]:
        for y in [1.55, 1.75, 3.0, 9.0, 15.35]:
            assert bundle.kernel_fn(x, y) > 0.0
    for x, y in [(1.5, 4.0), (15.5, 4.0), (4.0, 1.4), (4.0, 15.6), (20.0, 20.0)]:
        assert bundle.kernel_fn(x, y) == 0.0
        assert bundle.euler1_fn(x, y) == 0.0
        assert bundle.euler2_fn(x, y) == 0.0


def test_12_negative_witness_complete_curvature_enclosure_strictly_negative() -> None:
    """12. Negative witness complete arithmetic curvature enclosure has strictly negative upper bound."""
    cert = certify_compact_witness_curvature_arb("negative", N_cutoff=15)
    assert cert["certified"] is True
    assert cert["status"] == COMPACT_SUPPORT_NEG_CURVATURE_CERTIFIED
    assert cert["zero_excluded"] is True
    assert cert["sup_curvature_lt_zero"] is True
    c_enc = cert["curvature_enclosure"]
    assert c_enc["strictly_negative"] is True
    lo, hi = c_enc["outward_float_interval"]
    assert lo <= hi < -6442.0


def test_13_positive_witness_nonnegative_and_compactly_supported() -> None:
    """13. Positive witness is nonnegative and compactly supported."""
    bundle = build_compact_positive_witness(15)
    for x in [1.55, 1.65, 1.75, 2.0, 5.0, 11.0, 15.25, 15.35, 15.45]:
        for y in [1.55, 1.75, 3.0, 7.0, 15.35]:
            assert bundle.kernel_fn(x, y) > 0.0
    for x, y in [(1.5, 5.0), (15.5, 5.0), (5.0, 1.5), (5.0, 15.5), (25.0, 25.0)]:
        assert bundle.kernel_fn(x, y) == 0.0
        assert bundle.euler1_fn(x, y) == 0.0
        assert bundle.euler2_fn(x, y) == 0.0


def test_14_positive_witness_complete_curvature_enclosure_strictly_positive() -> None:
    """14. Positive witness complete arithmetic curvature enclosure has strictly positive lower bound."""
    cert = certify_compact_witness_curvature_arb("positive", N_cutoff=15)
    assert cert["certified"] is True
    assert cert["status"] == COMPACT_SUPPORT_POS_CURVATURE_CERTIFIED
    assert cert["zero_excluded"] is True
    assert cert["inf_curvature_gt_zero"] is True
    c_enc = cert["curvature_enclosure"]
    assert c_enc["strictly_positive"] is True
    lo, hi = c_enc["outward_float_interval"]
    assert 191887.0 < lo <= hi


def test_15_arb_failure_is_fail_closed() -> None:
    """15. Arb failure path is fail-closed (returns ARB_CERTIFICATION_NOT_AVAILABLE)."""
    res_neg = certify_compact_witness_curvature_arb(
        "negative", N_cutoff=15, force_flint_unavailable=True
    )
    assert res_neg["status"] == ARB_CERTIFICATION_NOT_AVAILABLE
    assert res_neg["certified"] is False
    assert res_neg["curvature_enclosure"] is None
    assert res_neg["zero_excluded"] is False

    res_pos = certify_compact_witness_curvature_arb(
        "positive", N_cutoff=15, force_flint_unavailable=True
    )
    assert res_pos["status"] == ARB_CERTIFICATION_NOT_AVAILABLE
    assert res_pos["certified"] is False


def test_16_display_floats_are_not_labelled_certificates() -> None:
    """16. Display floats are not labelled certificates."""
    sign_audit = audit_arithmetic_curvature_sign_firewall(N_cutoff=15)
    assert sign_audit["display_floats_are_certificates"] is False
    assert (
        sign_audit["negative_curvature_arb_enclosure"]["curvature_enclosure"][
            "display_float_is_certificate"
        ]
        is False
    )
    assert (
        sign_audit["positive_curvature_arb_enclosure"]["curvature_enclosure"][
            "display_float_is_certificate"
        ]
        is False
    )


def test_17_complete_compact_support_sum_distinguished_from_finite_truncation() -> None:
    """17. Complete compact-support sum is distinguished from finite truncation."""
    sign_audit = audit_arithmetic_curvature_sign_firewall(N_cutoff=15)
    assert sign_audit["is_complete_compact_support_evaluation"] is True
    assert sign_audit["is_infinite_sum_truncation"] is False
    assert sign_audit["superseded_classification"] == SUPERSEDED_FINITE_TRUNCATION_STATUS
    assert sign_audit["classification"] == COMPACT_SUPPORT_SIGN_INDEFINITENESS_STATUS

    hom_ctrl = evaluate_homogeneous_kernel_control()
    assert hom_ctrl["evaluation_mode"] == "FINITE_TRUNCATION_DIAGNOSTIC"
    assert hom_ctrl["is_compactly_supported"] is False


def test_18_accidental_zero_scope_is_explicit() -> None:
    """18. Accidental-zero witness scope is explicit."""
    acc = audit_finite_station_accidental_zero()
    assert acc["classification"] == CLASSIFICATION_FINITE_ACCIDENTAL_ZERO
    scope = acc["scope_specification"]
    assert (
        scope["complete_plateau_kernel_X3"]["evaluation_scope"]
        == "ONE_COMPACTLY_SUPPORTED_KERNEL_COMPLETE_SUPPORT"
    )
    assert abs(scope["complete_plateau_kernel_X3"]["arithmetic_curvature"]) == 0.0
    assert (
        scope["fixed_kernel_F_acc_restricted_vs_complete"]["restricted_subset_scope"]
        == "ONE_RESTRICTED_ARITHMETIC_WINDOW_OF_FIXED_KERNEL"
    )
    assert (
        scope["fixed_kernel_F_acc_restricted_vs_complete"]["complete_support_scope"]
        == "COMPLETE_SUPPORT_OF_SAME_FIXED_KERNEL"
    )
    assert acc["vanishes_on_selected_window"] is True
    assert acc["nonzero_on_complete_support_of_fixed_kernel"] is True


def test_19_theta_uncertain_fields_are_statuses_not_booleans() -> None:
    """19. Theta-Mellin uncertain fields are statuses, not Booleans."""
    theta = audit_theta_mellin_nonscalar_fallback()
    for field_name, val in theta.__dict__.items():
        assert not isinstance(val, bool), f"Theta field {field_name} is bool: {val!r}"
        assert isinstance(val, str)


def test_20_theta_convergence_not_marked_proved() -> None:
    """20. Theta convergence is not marked proved."""
    theta = audit_theta_mellin_nonscalar_fallback()
    assert theta.convergence_status == "CONDITIONAL_ON_REGULARIZATION"
    assert theta.second_mismatch_variation_status == "FORMAL_CANDIDATE_NOT_DERIVED"


def test_21_theta_complete_spectral_expansion_not_marked_proved() -> None:
    """21. Theta complete spectral expansion is not marked proved."""
    theta = audit_theta_mellin_nonscalar_fallback()
    assert theta.complete_spectral_expansion_status == "COMPLETE_EXPANSION_NOT_DERIVED"
    assert theta.secondary_classification == THETA_MELLIN_AUDIT_CONDITIONAL


def test_22_theta_delta_squared_limited_to_conjugate_block() -> None:
    """22. Theta delta_rho^2 detection is limited to the conjugate block."""
    theta = audit_theta_mellin_nonscalar_fallback()
    assert theta.delta_squared_detection_status == "DIAGONAL_CONJUGATE_BLOCK_ONLY"


def test_23_theta_positivity_classified_as_rh_equivalent() -> None:
    """23. Theta positivity is classified as RH-equivalent."""
    theta = audit_theta_mellin_nonscalar_fallback()
    assert theta.positive_complete_spectral_curvature_status == "RH_EQUIVALENT_IF_POSITIVE"
    assert theta.closes_obl_ct_001a_status == "FALSE"


def test_24_principal_classification_remains_mismatch_curvature_reduces_to_obl_ct_001a() -> None:
    """24. Principal classification remains MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A."""
    report = audit_transport_mismatch_curvature()
    assert report["principal_classification"] == PRINCIPAL_CLASSIFICATION
    assert report["principal_classification"] == "MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A"
    assert report["task_completion_status"] == TASK_TC_034R_STATUS


def test_25_obl_ct_001a_remains_open() -> None:
    """25. OBL-CT-001A remains OPEN."""
    report = audit_transport_mismatch_curvature()
    assert report["obl_ct_001a_status"] == "OPEN"
    assert report["obl_ct_001a_completed"] is False
    assert report["rh_claimed"] is False


def test_26_candidate_failure_does_not_refute_tc() -> None:
    """26. Candidate failure does not refute TC."""
    report = audit_transport_mismatch_curvature()
    assert report["candidate_failure_refutes_tc"] is False
    assert "NOT the general TC hypothesis" in report["hypothesis_fidelity"]["distinction"]


def test_27_actual_lean_theorem_identifiers_match_file() -> None:
    """27. Actual Lean theorem identifiers match TransportMismatchCurvature.lean."""
    check = verify_lean_theorem_map_against_file()
    assert check["matches_exact"] is True
    assert check["contains_sorry"] is False
    assert len(check["actual_defs"]) == 1
    assert len(check["actual_theorems"]) == 17

    lean_map = get_lean_theorem_map()
    assert lean_map["total_module_declarations"] == 18
    assert lean_map["module_def_count"] == 1
    assert lean_map["module_theorem_count"] == 17
    assert lean_map["repository_compiled_theorem_declarations"] == 565


def test_28_json_artifact_contains_all_required_repair_keys() -> None:
    """28. JSON artifact contains all required repair keys from Section 15 of TASK-TC-034R."""
    assert ARTIFACT_PATH.exists()
    data = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))

    required_section_15_keys = [
        "compact_support_no_go_evidence",
        "compactification_operator",
        "plateau_interval",
        "support_interval",
        "jet_preservation_order",
        "negative_witness",
        "negative_witness_complete_sum",
        "negative_curvature_arb_enclosure",
        "positive_witness",
        "positive_witness_complete_sum",
        "positive_curvature_arb_enclosure",
        "compact_support_sign_indefiniteness_status",
        "finite_accidental_zero_scope",
        "theta_definition_status",
        "theta_convergence_status",
        "theta_second_variation_status",
        "theta_delta_squared_status",
        "theta_complete_expansion_status",
        "theta_positivity_status",
        "theta_obl_ct_001a_status",
        "lean_theorem_map",
        "principal_classification",
    ]
    for key in required_section_15_keys:
        assert key in data, f"Missing required Section 15 key in JSON artifact: {key}"

    # Verify retained mathematical checks (Euler generator, Lagrange mixture, Mellin, centering, generic base)
    neg_bundle = build_compact_negative_witness(15)
    deriv_k1 = evaluate_mismatch_derivatives_at_zero(
        neg_bundle.kernel_fn,
        K=1.0,
        n_max=15,
        euler1_f0=neg_bundle.euler1_fn,
        euler2_f0=neg_bundle.euler2_fn,
    )
    deriv_k2 = evaluate_mismatch_derivatives_at_zero(
        neg_bundle.kernel_fn,
        K=2.0,
        n_max=15,
        euler1_f0=neg_bundle.euler1_fn,
        euler2_f0=neg_bundle.euler2_fn,
    )
    assert abs(deriv_k1.normalized_curvature_from_K - deriv_k2.normalized_curvature_from_K) < 1e-12

    mix = evaluate_exponential_mixture_curvature([1.5, 2.5, 0.75], [-0.4, 0.2, 0.9])
    assert mix.lagrange_identity_abs_err < 1e-14
    assert mix.strictly_positive is True

    recip = evaluate_reciprocal_pair_curvature(1.2, 0.8, 0.35)
    assert recip.strictly_positive is True

    mellin = evaluate_mellin_mismatch_scaling(
        s=complex(0.6, 14.13), t=complex(0.6, -14.13), K=1.0, eta=0.1, a=0.5
    )
    assert abs(mellin["net_normalized_exponent"] - 0.1 * 1.2) < 1e-14

    pairing = audit_spectral_centering_and_pairings()
    assert abs(pairing.centered_conjugate_exponent - 2.0 * pairing.delta) < 1e-14
    assert abs(pairing.centered_reflection_exponent - complex(0.0, 2.0 * pairing.gamma)) < 1e-14

    gen_base = evaluate_generic_base_mismatch_control()
    assert gen_base["holds_for_all_q_gt_1"] is True

    weil_fw = audit_weil_equivalence_firewall()
    assert weil_fw["global_spectral_form_positivity_is_rh_equivalent"] is True
    assert weil_fw["independent_proof_mechanism"] is False
