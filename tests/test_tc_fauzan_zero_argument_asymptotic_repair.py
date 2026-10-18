"""
Tests for TASK-TC-039R: Newton/Pade/Hankel Asymptotic Repair, Gate-Z5 Lower-Envelope
Audit, and pi <-> tau Arithmetic-Normalization Analysis.

Covers all 40 required tests from Section 46 of the TASK-TC-039R specification,
plus full artifact schema and 17-theorem Lean formalization verification.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import pytest

from tc.fauzan_zero_argument_asymptotic_repair import (
    ALL_FAUZAN_TRANSFER_LEAN_THEOREMS,
    FIXED_RATIONAL_NORMALIZATION_GAUGES_EQUIVALENT_AT_LEADING_DIOPHANTINE_ORDER,
    FIXED_RATIONAL_NORMALIZATION_GAUGE_DOES_NOT_CHANGE_NEWTON_STRETCHED_EXPONENT,
    HANKEL_DETERMINANT_RATIONAL_GAUGE_SCALING_PROVED,
    MULTIPOINT_PADE_GATE_Z5_NEGATIVE_NUMERICAL_EVIDENCE,
    NEWTON_SERIES_IDENTITY_FOR_RATIONALIZED_XI_PROVED_WITHOUT_CARLSON,
    NEWTON_TWO_APPROXIMANT_ROUTE_RIGOROUSLY_FAILS_GATE_Z5,
    PI_TAU_NORMALIZATIONS_HAVE_IDENTICAL_ZERO_DIVISOR,
    RATIONAL_ZERO_PRESERVING_NORMALIZATION_GAUGE_FAMILY_PROVED,
    REQUIRED_TC039R_ARTIFACT_KEYS,
    REQUIRED_TC039R_LEAN_THEOREMS,
    SUBGATE_TC_039A_REPAIRED_STATUS,
    TASK_TC_039R_ID,
    TAU_ANALYTIC_NORMALIZATION_DISTINCT_FROM_TC_GRADE_ACTION,
    TAU_NORMALIZATION_EXPOSES_EVEN_ZETA_RATIONAL_CORE,
    TC039R_PRINCIPAL_CLASSIFICATION,
    audit_generating_functions_and_euler_transforms,
    audit_hankel_scaling_and_repaired_asymptotics,
    audit_newton_denominators_and_prime_valuations,
    audit_pade_evidence_scope_and_gauge_scaling,
    audit_pi_tau_normalizations_and_gauge_family,
    audit_saddle_asymptotics_and_two_step_lower_envelope,
    audit_variable_gauge_and_invariant_efficiency,
    compute_gauge_integer_samples,
    compute_gauge_positive_moments,
    saddle_decay_constant_kappa,
    saddle_phase_constant_omega,
    verify_direct_newton_series_identity_without_carlson,
    verify_tc039r_lean_theorems,
)
from tc.fauzan_zero_argument_transfer import (
    MULTIPOINT_PADE_ARGUMENT_POLYNOMIALIZATION_PROVED,
    SUBGATE_TC_040A_ID,
    lambert_stieltjes_hankel_determinant_exact,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def artifact_data() -> dict:
    path = REPO_ROOT / "data" / "tc_fauzan_zero_argument_asymptotic_repair.json"
    assert path.exists(), "data/tc_fauzan_zero_argument_asymptotic_repair.json must exist"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def norm_data() -> dict:
    return audit_pi_tau_normalizations_and_gauge_family(max_m=40)


@pytest.fixture(scope="module")
def gf_data() -> dict:
    return audit_generating_functions_and_euler_transforms(max_m=12)


@pytest.fixture(scope="module")
def hankel_data() -> dict:
    return audit_hankel_scaling_and_repaired_asymptotics(max_n=10)


# 1. tau = 2*pi
def test_01_tau_equals_two_pi(artifact_data: dict) -> None:
    assert artifact_data["tau_definition"] == "tau = 2*pi"
    for key in (
        "pi_form",
        "tau_form",
        "pi_tau_equivalence",
        "tau_first_simplification",
        "normalization_dependent_factors",
        "normalization_invariant_factors",
    ):
        assert key in artifact_data["pi_tau_policy"]


# 2. pi = tau / 2
def test_02_pi_equals_tau_over_two(artifact_data: dict) -> None:
    assert artifact_data["pi_as_tau_over_two"] == "pi = tau / 2"
    assert "pi = tau/2" in artifact_data["pi_tau_policy"]["pi_tau_equivalence"]


# 3. R_pi = 4^z R_tau
def test_03_r_pi_equals_four_pow_z_r_tau(norm_data: dict) -> None:
    scaling = norm_data["R_pi_tau_scaling"]
    assert scaling["identity"] == "R_pi(z) = 4^z * R_tau(z)"
    assert scaling["symbolic_verified"] is True
    assert scaling["arb_128bit_verified_at_alpha1"] is True
    assert norm_data["R_pi"]["symbolic_completed_xi_identity_verified"] is True
    assert norm_data["R_tau"]["symbolic_completed_xi_identity_verified"] is True


# 4. identical zero divisor
def test_04_identical_zero_divisor(norm_data: dict) -> None:
    zdiv = norm_data["zero_divisor_equivalence"]
    assert zdiv["classification"] == PI_TAU_NORMALIZATIONS_HAVE_IDENTICAL_ZERO_DIVISOR
    assert zdiv["arb_128bit_zero_at_alpha1_pi"] is True
    assert zdiv["arb_128bit_zero_at_alpha1_tau"] is True
    assert "pi_tau_zero_function_scaling" in zdiv["lean_theorems"]
    assert "rational_gauge_zero_divisor_invariant" in zdiv["lean_theorems"]


# 5. tau^{-2m} zeta(2m) rational formula
def test_05_tau_even_zeta_rational_core_formula(norm_data: dict) -> None:
    core = norm_data["tau_even_zeta_rational_core"]
    assert core["classification"] == TAU_NORMALIZATION_EXPOSES_EVEN_ZETA_RATIONAL_CORE
    assert core["symbolic_euler_verified_m_1_to_12"] is True
    assert (
        core["tau_form"]
        == "tau^{-2m} * zeta(2m) = (-1)^{m+1} * B_{2m} / (2 * (2m)!)"
    )


# 6. a_m^{(pi)} = 4^m a_m^{(tau)}
def test_06_am_pi_equals_four_pow_m_am_tau(norm_data: dict) -> None:
    assert norm_data["sample_scaling"]["verified_exact_0_to_max_m"] is True
    a_tau = norm_data["a_tau_list"]
    a_pi = norm_data["a_pi_list"]
    for m in range(len(a_tau)):
        assert a_pi[m] == (Fraction(4, 1) ** m) * a_tau[m]


# 7. both sample formulas exact
def test_07_both_sample_formulas_exact(norm_data: dict) -> None:
    a_tau = norm_data["a_tau_list"]
    a_pi = norm_data["a_pi_list"]
    assert a_tau[0] == Fraction(1, 2)
    assert a_tau[1] == Fraction(1, 24)
    assert a_tau[2] == Fraction(1, 480)
    assert a_tau[3] == Fraction(1, 12096)
    assert a_pi[0] == Fraction(1, 2)
    assert a_pi[1] == Fraction(1, 6)
    assert a_pi[2] == Fraction(1, 30)
    assert a_pi[3] == Fraction(1, 189)


# 8. A_pi(t) exact
def test_08_a_pi_ogf_exact(gf_data: dict) -> None:
    assert (
        gf_data["A_pi"]["formula"]
        == "A_pi(t) = sum_{m>=0} a_m^{(pi)} t^m = t / (2 * sin^2(sqrt(t)))"
    )
    assert gf_data["A_pi"]["taylor_verified_0_to_max_m"] is True


# 9. A_tau(t) exact
def test_09_a_tau_ogf_exact(gf_data: dict) -> None:
    assert (
        gf_data["A_tau"]["formula"]
        == "A_tau(t) = sum_{m>=0} a_m^{(tau)} t^m = t / (8 * sin^2(sqrt(t) / 2))"
    )
    assert gf_data["A_tau"]["taylor_verified_0_to_max_m"] is True


# 10. A_pi(t) = A_tau(4t)
def test_10_a_pi_equals_a_tau_of_4t(gf_data: dict) -> None:
    assert gf_data["A_c"]["pi_tau_scaling_identity"] == "A_pi(t) = A_tau(4 * t)"
    assert gf_data["A_c"]["pi_tau_scaling_verified"] is True


# 11. general A_c(t)
def test_11_general_a_c_ogf_and_euler_c_c(gf_data: dict, norm_data: dict) -> None:
    assert (
        gf_data["A_c"]["formula"]
        == "A_c(t) = A_tau(c * t) = (c * t) / (8 * sin^2(sqrt(c * t) / 2))"
    )
    assert gf_data["A_c"]["general_c_scaling_verified"] is True
    assert gf_data["C_pi"]["taylor_matches_forward_differences_0_to_10"] is True
    assert gf_data["C_tau"]["taylor_matches_forward_differences_0_to_10"] is True
    assert (
        norm_data["rational_gauge_family"]["classification"]
        == RATIONAL_ZERO_PRESERVING_NORMALIZATION_GAUGE_FAMILY_PROVED
    )


# 12. radius tau^2 / c
def test_12_radius_of_convergence_tau_sq_over_c(gf_data: dict) -> None:
    assert (
        gf_data["A_c"]["radius_of_convergence"]
        == "R_c = tau^2 / c = 4 * pi^2 / c"
    )
    assert abs(gf_data["A_tau"]["radius_float"] - 4.0 * gf_data["A_pi"]["radius_float"]) < 1e-12


# 13. positive tau moment identity
def test_13_positive_tau_moment_identity() -> None:
    b_tau = compute_gauge_positive_moments(Fraction(1, 1), max_m=15)
    assert b_tau[0] == Fraction(1, 24)
    assert b_tau[1] == Fraction(1, 1440)
    assert b_tau[2] == Fraction(1, 60480)
    assert all(b > 0 for b in b_tau)


# 14. b_m^{(pi)} = 4^{m+1} b_m^{(tau)}
def test_14_bm_pi_equals_four_pow_m_plus_1_bm_tau() -> None:
    b_tau = compute_gauge_positive_moments(Fraction(1, 1), max_m=20)
    b_pi = compute_gauge_positive_moments(Fraction(4, 1), max_m=20)
    for m in range(len(b_tau)):
        assert b_pi[m] == (Fraction(4, 1) ** (m + 1)) * b_tau[m]


# 15. exact Hankel scaling D_n^{(pi)} = 4^{n^2} D_n^{(tau)}
def test_15_exact_hankel_scaling_pi_vs_tau(hankel_data: dict) -> None:
    hs = hankel_data["hankel_pi_tau_scaling"]
    assert hs["classification"] == HANKEL_DETERMINANT_RATIONAL_GAUGE_SCALING_PROVED
    assert hs["verified_pi_tau_1_to_max_n"] is True
    for row in hankel_data["corrected_hankel_product"]["table"]:
        assert row["D_n_pi_equals_4_pow_n_sq_D_n_tau"] is True


# 16. general D_n^{(c)} = c^{n^2} D_n^{(tau)}
def test_16_general_hankel_scaling_c_pow_n_sq(hankel_data: dict) -> None:
    hs = hankel_data["hankel_pi_tau_scaling"]
    assert hs["verified_c2_tau_1_to_max_n"] is True
    for row in hankel_data["corrected_hankel_product"]["table"]:
        assert row["D_n_c2_equals_2_pow_n_sq_D_n_tau"] is True


# 17. corrected S-fraction determinant formula
def test_17_corrected_s_fraction_determinant_formula(hankel_data: dict) -> None:
    prod = hankel_data["corrected_hankel_product"]
    assert prod["verified_exact_1_to_max_n"] is True
    assert (
        "6^{-n} * prod_{j=1}^{n-1} [(4j - 1)*(4j + 1)^2*(4j + 3)]^{-(n - j)}"
        in prod["pi_product_formula"]
    )
    for n in range(1, 11):
        c0 = Fraction(1, 6)
        direct_prod = c0**n
        for j in range(1, n):
            direct_prod *= Fraction(
                1, (4 * j - 1) * ((4 * j + 1) ** 2) * (4 * j + 3)
            ) ** (n - j)
        assert direct_prod == lambert_stieltjes_hankel_determinant_exact(n)


# 18. D_1 = 1/6
def test_18_d1_equals_one_sixth(hankel_data: dict) -> None:
    hs = hankel_data["hankel_pi_tau_scaling"]
    assert hs["b_0_pi_exact"] == "1/6"
    assert hs["D_1_pi_exact"] == "1/6"
    assert hs["D_1_tau_exact"] == "1/24"
    assert lambert_stieltjes_hankel_determinant_exact(1) == Fraction(1, 6)


# 19. D_2 = 1/18900
def test_19_d2_equals_one_over_18900(hankel_data: dict) -> None:
    hs = hankel_data["hankel_pi_tau_scaling"]
    assert hs["D_2_pi_exact"] == "1/18900"
    assert hs["D_2_tau_exact"] == "1/4838400"
    assert lambert_stieltjes_hankel_determinant_exact(2) == Fraction(1, 18900)
    assert Fraction(1, 18900) == (Fraction(4, 1) ** 4) * Fraction(1, 4838400)


# 20. corrected subleading Hankel coefficient 4 log 2 - 3
def test_20_corrected_subleading_hankel_coefficient_4_log2_minus_3(
    hankel_data: dict,
) -> None:
    sub = hankel_data["hankel_subleading_constant"]
    assert sub["C_pi_c_eq_4_exact"] == "4 * log(2) - 3"
    assert abs(sub["C_pi_c_eq_4_float"] - (4.0 * math.log(2.0) - 3.0)) < 1e-15
    assert sub["C_tau_c_eq_1_exact"] == "6 * log(2) - 3"
    assert abs(sub["C_tau_c_eq_1_float"] - (6.0 * math.log(2.0) - 3.0)) < 1e-15
    assert (
        "(2*log(2) - 3)"
        not in hankel_data["corrected_hankel_asymptotic"]["pi_asymptotic"]
    )


# 21. C1 degree equals n^2
def test_21_c1_degree_equals_n_squared(hankel_data: dict) -> None:
    c1 = hankel_data["c1_degree_repair"]
    assert c1["exact_degree_in_X"] == "sum_{m=1}^{2n-1} min(m, 2n - m) = n^2"
    assert c1["verified_1_to_8"] is True


# 22. direct Newton identity does not rely only on integer interpolation uniqueness
def test_22_direct_newton_identity_without_integer_uniqueness_shortcut() -> None:
    res = verify_direct_newton_series_identity_without_carlson()
    proof = res["newton_identity_proof"]
    assert (
        proof["classification"]
        == NEWTON_SERIES_IDENTITY_FOR_RATIONALIZED_XI_PROVED_WITHOUT_CARLSON
    )
    assert proof["uses_integer_uniqueness_shortcut"] is False
    assert proof["subtracted_mode_identity_verified"] is True
    assert proof["uniform_mode_bound_verified"] is True
    assert proof["half_plane_test_point_z_0_8_plus_0_5i"]["tau_partial_sum_error_n_150"] < 1e-3
    assert proof["half_plane_test_point_z_0_8_plus_0_5i"]["pi_partial_sum_error_n_150"] < 1e-4


# 23. Carlson shortcut absent unless hypotheses proved
def test_23_carlson_shortcut_absent(artifact_data: dict) -> None:
    assert artifact_data["newton_identity_proof"]["uses_carlson_theorem"] is False
    assert artifact_data["newton_convergence_domain"]["carlson_invoked"] is False


# 24. saddle constant at c = 4 equals 3/2
def test_24_saddle_constant_at_c_eq_4_equals_three_halves(artifact_data: dict) -> None:
    assert abs(saddle_decay_constant_kappa(4.0) - 1.5) < 1e-15
    assert artifact_data["corrected_pi_decay_constant"]["kappa_pi_exact"] == "3/2"
    assert abs(artifact_data["corrected_pi_decay_constant"]["kappa_pi_float"] - 1.5) < 1e-15


# 25. no pi^{2/3} contamination
def test_25_no_pi_pow_2_over_3_contamination(artifact_data: dict) -> None:
    sp_info = artifact_data["saddle_points"]
    assert sp_info["pi_pow_2_over_3_contamination_present"] is False
    assert artifact_data["corrected_pi_decay_constant"]["spurious_pi_pow_2_3_removed"] is True
    assert "pi" not in sp_info["at_pi_c_eq_4"].split("~")[1].split("exp")[0]


# 26. saddle constant at c = 1 equals 3 / 2^{5/3}
def test_26_saddle_constant_at_c_eq_1_equals_three_over_two_pow_five_thirds(
    artifact_data: dict,
) -> None:
    expected = 3.0 / (2.0 ** (5.0 / 3.0))
    assert abs(saddle_decay_constant_kappa(1.0) - expected) < 1e-15
    assert artifact_data["tau_decay_constant"]["kappa_tau_exact"] == "3 / 2^{5/3}"
    assert abs(artifact_data["tau_decay_constant"]["kappa_tau_float"] - expected) < 1e-15


# 27. phase constant formula
def test_27_phase_constant_formula(artifact_data: dict) -> None:
    assert (
        artifact_data["saddle_phase_constant"]["formula"]
        == "omega(c) = (3 * sqrt(3) / 2^{5/3}) * c^{1/3} = sqrt(3) * kappa(c)"
    )
    for c_val in (0.25, 1.0, 2.0, 4.0, 9.0):
        assert (
            abs(
                saddle_phase_constant_omega(c_val)
                - math.sqrt(3.0) * saddle_decay_constant_kappa(c_val)
            )
            < 1e-15
        )


# 28. lower-envelope claim only emitted if proved
def test_28_lower_envelope_backed_by_phase_separation_proof(
    artifact_data: dict,
) -> None:
    env = artifact_data["newton_two_step_lower_envelope"]
    assert env["status"] == "PROVED_TWO_SIDED_STRETCHED_EXPONENTIAL_ENCLOSURE"
    assert env["phase_shift_between_tail_and_increment"] == "Delta_theta = pi / 3 (O(1) constant phase separation)"
    assert env["lean_theorem"] == "two_phase_cosine_square_lower_bound"
    # Verify one-loop saddle accuracy across validation rows
    val_rows = artifact_data["delta_n_a0_full_asymptotic"]["validation_rows"]
    assert all(
        r["one_loop_rel_error_pi"] < 5e-3 for r in val_rows if r["n"] in (80, 120, 200)
    )
    assert all(
        r["one_loop_rel_error_tau"] < 3e-2 for r in val_rows if r["n"] in (120, 200)
    )




# 29. upper bound not treated as lower bound
def test_29_upper_bound_not_treated_as_lower_bound(artifact_data: dict) -> None:
    env = artifact_data["newton_two_step_lower_envelope"]
    assert env["exponent_A_lower"] == 1.5
    assert abs(env["exponent_B_upper"] - (-1.0 / 6.0)) < 1e-15
    assert "C_1(c) * n^{-3/2}" in env["two_sided_bound"]
    assert "C_2(c) * n^{-1/6}" in env["two_sided_bound"]


# 30. fixed-gauge n^{1/3} exponent classification
def test_30_fixed_gauge_n_pow_1_3_exponent_classification(artifact_data: dict) -> None:
    z5 = artifact_data["z5_newton_status"]
    assert z5["classification"] == NEWTON_TWO_APPROXIMANT_ROUTE_RIGOROUSLY_FAILS_GATE_Z5
    assert (
        z5["fixed_gauge_classification"]
        == FIXED_RATIONAL_NORMALIZATION_GAUGE_DOES_NOT_CHANGE_NEWTON_STRETCHED_EXPONENT
    )


# 31. denominator equality not claimed from an upper bound
def test_31_denominator_equality_not_claimed_from_upper_bound(
    artifact_data: dict,
) -> None:
    pi_den = artifact_data["pi_newton_denominator_growth"]
    tau_den = artifact_data["tau_newton_denominator_growth"]
    assert pi_den["upper_bound_distinguished_from_equality"] is True
    assert tau_den["upper_bound_distinguished_from_equality"] is True
    assert pi_den["stirling_lcm_identity_verified_1_to_25"] is True
    assert "<= 3*n*log(n) + O(n)" in pi_den["unconditional_upper_bound"]
    assert ">= (5/2)*n*log(n) + O(n)" in pi_den["unconditional_kummer_lower_bound"]


# 32. pi/tau prime valuation difference localized initially at p = 2
def test_32_pi_tau_prime_valuation_difference_localized_at_p_eq_2(
    artifact_data: dict,
) -> None:
    pvc = artifact_data["prime_valuation_comparison"]
    assert pvc["odd_prime_sample_invariance_verified"] is True
    assert pvc["dyadic_sample_shift_verified"] is True
    assert pvc["lcm_odd_prime_invariance_1_to_max_n"] is True
    assert pvc["lcm_ratio_is_exact_power_of_2_1_to_max_n"] is True
    for row in pvc["valuation_table"]:
        assert row["v_3_L_n_pi"] == row["v_3_L_n_tau"]
        assert row["v_5_L_n_pi"] == row["v_5_L_n_tau"]
        assert row["v_2_diff_tau_minus_pi"] > 0


# 33. Pade finite evidence separated from asymptotic proof
def test_33_pade_finite_evidence_separated_from_asymptotic_proof(
    artifact_data: dict,
) -> None:
    pf = artifact_data["pade_finite_evidence"]
    pz5 = artifact_data["pade_z5_status"]
    assert (
        pf["polynomialization_classification"]
        == MULTIPOINT_PADE_ARGUMENT_POLYNOMIALIZATION_PROVED
    )
    assert (
        pf["gate_z5_evidence_classification"]
        == MULTIPOINT_PADE_GATE_Z5_NEGATIVE_NUMERICAL_EVIDENCE
    )
    assert pz5["z5_status"] == MULTIPOINT_PADE_GATE_Z5_NEGATIVE_NUMERICAL_EVIDENCE


# 34. no all-n Pade no-go absent theorem
def test_34_no_all_n_pade_nogo_absent_theorem(artifact_data: dict) -> None:
    pa = artifact_data["pade_asymptotic_status"]
    assert pa["all_n_no_go_claimed"] is False
    assert "OPEN_ANALYTIC_SUBPROBLEM" in pa["all_n_rank_and_height_theorem_status"]


# 35. variable gauge zero-independent
def test_35_variable_gauge_zero_independent(artifact_data: dict) -> None:
    vg = artifact_data["variable_gauge_audit"]
    assert vg["zero_independent_gauge_selection"] is True
    assert vg["variable_gauge_breaks_obstruction"] is False
    for row in vg["variable_gauge_reconnaissance_table"]:
        assert row["efficiency_E_n_primitive"] < 0.0


# 36. tau analytic normalization not equated to TC grade
def test_36_tau_analytic_normalization_not_equated_to_tc_grade(
    artifact_data: dict,
) -> None:
    fw = artifact_data["tc_grade_firewall"]
    assert (
        fw["classification"]
        == TAU_ANALYTIC_NORMALIZATION_DISTINCT_FROM_TC_GRADE_ACTION
    )
    assert fw["conflation_prohibited"] is True


# 37. no RH assumption
def test_37_no_rh_assumption(artifact_data: dict) -> None:
    assert artifact_data["rh_claimed"] is False


# 38. no irrationality claim unless Z5+Z6 genuinely close
def test_38_no_irrationality_claim(artifact_data: dict) -> None:
    assert (
        artifact_data["z5_newton_status"]["classification"]
        == NEWTON_TWO_APPROXIMANT_ROUTE_RIGOROUSLY_FAILS_GATE_Z5
    )
    assert (
        artifact_data["pade_z5_status"]["z5_status"]
        == MULTIPOINT_PADE_GATE_Z5_NEGATIVE_NUMERICAL_EVIDENCE
    )


# 39. OBL-CT-001A remains open
def test_39_obl_ct_001a_remains_open(artifact_data: dict) -> None:
    assert artifact_data["obl_ct_001a_status"] == "OPEN"
    assert (
        artifact_data["exact_next_subgate"]["parallel_subgate_tc_038a_status"]
        == "OPEN"
    )
    assert artifact_data["exact_next_subgate"]["next_subgate_id"] == SUBGATE_TC_040A_ID


# 40. canonical classifications match artifact, schema complete, and all 17 Lean theorems verified
def test_40_canonical_classifications_schema_and_lean_theorems(
    artifact_data: dict,
) -> None:
    for key in REQUIRED_TC039R_ARTIFACT_KEYS:
        assert key in artifact_data, f"Missing required TASK-TC-039R key: {key}"

    assert artifact_data["task_id"] == TASK_TC_039R_ID
    assert artifact_data["principal_classification"] == TC039R_PRINCIPAL_CLASSIFICATION
    assert artifact_data["subgate_tc_039a_status"] == SUBGATE_TC_039A_REPAIRED_STATUS
    assert (
        FIXED_RATIONAL_NORMALIZATION_GAUGES_EQUIVALENT_AT_LEADING_DIOPHANTINE_ORDER
        in artifact_data["principal_classification"]
    )

    lean_info = verify_tc039r_lean_theorems(REPO_ROOT)
    assert lean_info["all_tc039r_present"] is True
    assert lean_info["all_17_present"] is True
    assert lean_info["theorem_declaration_count"] == 17
    assert lean_info["sorry_count"] == 0
    assert lean_info["admit_count"] == 0
    assert lean_info["nonstandard_axiom_count"] == 0
    for thm in REQUIRED_TC039R_LEAN_THEOREMS:
        assert thm in lean_info["found_theorem_declarations"]
    for thm in ALL_FAUZAN_TRANSFER_LEAN_THEOREMS:
        assert thm in lean_info["found_theorem_declarations"]
