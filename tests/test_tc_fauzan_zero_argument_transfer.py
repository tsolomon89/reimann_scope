"""
Tests for TASK-TC-039: Fauzan Hankel Irrationality Architecture Transfer to
Zeta-Zero Arguments.

Covers all 42 required tests from Section 39 of the TASK-TC-039 specification,
plus full artifact schema and Lean theorem verification.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import pytest

from tc.fauzan_zero_argument_transfer import (
    DO_NOT_SUBSTITUTE_5_TO_RHO_SYMBOLICALLY,
    EXTERNAL_IMPORT_GRAPH_CONTAINS_SORRY_DECLARATIONS,
    FAUZAN_HANKEL_ARGUMENT_TRANSFER_BLOCKED_BY_TARGET_COUPLING_AND_FACTORIAL_MOMENT_DENOMINATORS,
    INTEGER_AUXILIARY_POLYNOMIAL_SUPERLINEAR_SMALLNESS_IMPLIES_IRRATIONAL,
    MULTIPOINT_PADE_ARGUMENT_POLYNOMIALIZATION_PROVED_BUT_FAILS_GATE_Z5_INTEGER_SMALLNESS,
    NEWTON_ARGUMENT_POLYNOMIALIZATION_PROVED,
    NEWTON_ARGUMENT_POLYNOMIAL_ROUTE_INSUFFICIENT_SMALLNESS,
    PRINCIPAL_CLASSIFICATION,
    RATIONALIZED_XI_RATIONAL_INTEGER_SAMPLING_PROVED,
    REQUIRED_ARTIFACT_KEYS,
    REQUIRED_LEAN_THEOREMS,
    SUBGATE_TC_039A_CLOSED_STATUS,
    SUBGATE_TC_040A_ID,
    TARGET_THEOREM_AXIOM_CLOSURE_EXCLUDES_SORRY_DECLARATIONS,
    TASK_TC_039_ID,
    Z1_ARGUMENT_TARGET_REPRESENTATION_PROVED,
    Z2_ALGEBRAIC_ARGUMENT_POLYNOMIALITY_PROVED,
    Z3_COFINAL_STRUCTURAL_NONVANISHING_PROVED_FOR_TWO_APPROXIMANT_NORM_SUM,
    Z4_DEGREE_AND_DENOMINATOR_COMPLEXITY_QUANTIFIED_FACTORIAL_DENOMINATOR_OBSTRUCTION,
    Z5_SUPERLINEAR_LOG_SMALLNESS_FAILED_IN_TESTED_NEWTON_PADE_HANKEL_CLASSES,
    Z6_NOT_REACHED_TERMINATED_AT_GATE_Z5,
    ZERO_DEPENDENT_CANDIDATE_REJECTED,
    audit_diophantine_irrationality_and_mahler_criteria,
    audit_firewalls_and_exclusions,
    audit_positive_hankel_determinants_and_coupling,
    audit_preflight_tc038r_repairs,
    clear_rational_polynomial_denominators,
    compute_rational_integer_samples_bernoulli,
    construct_ordinate_norm_polynomial,
    derive_positive_moment_sequence_and_differences,
    derive_rationalized_xi_metadata,
    lambert_stieltjes_hankel_determinant_exact,
    newton_polynomial_power_coeffs,
    solve_multipoint_pade_family,
    verify_fauzan_transfer_lean_theorems,
    verify_sample_generating_function,
)
from tc.zero_arithmetic_invariants import (
    verify_formal_source_inventory_provenance,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def artifact_data() -> dict:
    path = REPO_ROOT / "data" / "tc_fauzan_zero_argument_transfer.json"
    assert path.exists(), "data/tc_fauzan_zero_argument_transfer.json must exist"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def sample_dict() -> dict:
    return compute_rational_integer_samples_bernoulli(40)


@pytest.fixture(scope="module")
def rational_samples(sample_dict: dict) -> list[Fraction]:
    return sample_dict["samples_fraction_list"]


@pytest.fixture(scope="module")
def moment_diff_dict(rational_samples: list[Fraction]) -> dict:
    return derive_positive_moment_sequence_and_differences(25, rational_samples)


# 1. preflight external import/proof-dependency wording repaired
def test_01_preflight_external_import_and_axiom_closure_wording() -> None:
    preflight = audit_preflight_tc038r_repairs(REPO_ROOT)
    ext = preflight["external_lean_dependency_wording"]
    assert ext["repaired"] is True
    assert (
        ext["external_import_graph_status"]
        == EXTERNAL_IMPORT_GRAPH_CONTAINS_SORRY_DECLARATIONS
    )
    assert (
        ext["target_theorem_axiom_closure_status"]
        == TARGET_THEOREM_AXIOM_CLOSURE_EXCLUDES_SORRY_DECLARATIONS
    )
    assert ext["print_axioms_apery_irrational_five"] == [
        "propext",
        "Classical.choice",
        "Quot.sound",
    ]
    assert "outside the transitive dependency cone" not in ext["note"]


# 2. formal source count derived from inventory
def test_02_formal_source_count_derived_from_inventory() -> None:
    prov = verify_formal_source_inventory_provenance(REPO_ROOT)
    from certification import REQUIRED_FORMAL_SOURCES
    from scripts.build_formal import FORMAL_SOURCE_FILES

    assert prov["synchronized"] is True
    assert prov["build_formal_source_count"] == len(FORMAL_SOURCE_FILES)
    assert prov["certification_required_source_count"] == len(REQUIRED_FORMAL_SOURCES)
    assert prov["umbrella_imported_module_count"] == len(FORMAL_SOURCE_FILES) - 1
    assert "formal/RiemannScope/FauzanZeroArgumentTransfer.lean" in FORMAL_SOURCE_FILES
    assert (
        "formal/RiemannScope/FauzanZeroArgumentTransfer.lean"
        in REQUIRED_FORMAL_SOURCES
    )


# 3. external theorem identifiers correct
def test_03_external_theorem_identifiers_correct() -> None:
    preflight = audit_preflight_tc038r_repairs(REPO_ROOT)
    ids = preflight["external_theorem_identifiers"]
    assert ids["identifiers_verified"] is True
    assert ids["invented_irrational_zeta_five_absent"] is True
    assert set(ids["actual_identifiers"]) == {
        "Apery.irrational_five",
        "Apery.irrational_zeta5",
        "RiemannZetaValues.irrational_five",
    }
    assert preflight["canonical_numerical_consistency"]["s4_verified"] is True
    assert (
        preflight["canonical_numerical_consistency"]["bounded_denominator_verified"]
        is True
    )
    assert (
        preflight["canonical_numerical_consistency"]["explicit_D4_H3_rho1_verified"]
        is True
    )


# 4. rationalized-xi two formulas agree
def test_04_rationalized_xi_two_formulas_agree() -> None:
    meta = derive_rationalized_xi_metadata()
    defn = meta["definition"]
    assert defn["symbolic_equivalence_verified"] is True
    assert defn["max_numerical_discrepancy_60dps"] < 1e-55


# 5. removable singularity metadata at z = 1/2
def test_05_removable_singularity_metadata_at_half() -> None:
    meta = derive_rationalized_xi_metadata()
    ent = meta["entire_status"]
    assert ent["is_entire"] is True
    rem = ent["removable_singularity_at_z_eq_half"]
    assert rem["point"] == "z = 1/2"
    assert rem["value_R_half"] == "1/pi"
    assert abs(rem["value_R_half_float"] - (1.0 / math.pi)) < 1e-15


# 6. nontrivial zero maps to zero at z = rho / 2
def test_06_nontrivial_zero_maps_to_zero_at_rho_over_2() -> None:
    meta = derive_rationalized_xi_metadata()
    zm = meta["zero_mapping"]["primary_benchmark_target"]
    assert zm["alpha_1"] == "rho_1 / 2 = 1/4 + i*gamma_1 / 2"
    assert zm["R_alpha_1_equals_zero"] is True
    assert zm["arb_128bit_enclosure_contains_zero"] is True
    assert zm["arb_128bit_abs_upper_bound"] < 1e-12


# 7. a_0 = 1/2
def test_07_a0_equals_one_half(
    sample_dict: dict, rational_samples: list[Fraction]
) -> None:
    assert sample_dict["a_0_equals_one_half"] is True
    assert rational_samples[0] == Fraction(1, 2)


# 8. a_m Bernoulli formula for several exact m
def test_08_am_bernoulli_formula_exact_values(
    sample_dict: dict, rational_samples: list[Fraction]
) -> None:
    assert sample_dict["classification"] == RATIONALIZED_XI_RATIONAL_INTEGER_SAMPLING_PROVED
    assert sample_dict["symbolic_euler_zeta_agreement_0_to_12"] is True
    expected = {
        0: Fraction(1, 2),
        1: Fraction(1, 6),
        2: Fraction(1, 30),
        3: Fraction(1, 189),
        4: Fraction(1, 1350),
        5: Fraction(1, 10395),
        6: Fraction(691, 58046625),
        7: Fraction(2, 1403325),
        8: Fraction(3617, 21709437750),
    }
    for m, val in expected.items():
        assert rational_samples[m] == val, f"Mismatch at m={m}"


# 9. all tested a_m in Q and strictly positive
def test_09_all_tested_am_in_q_and_positive(rational_samples: list[Fraction]) -> None:
    for m, val in enumerate(rational_samples):
        assert isinstance(val, Fraction)
        assert val > 0, f"a_{m} must be strictly positive"


# 10. generating-function coefficients match a_m
def test_10_generating_function_coefficients_match_am() -> None:
    gf = verify_sample_generating_function(max_m=14)
    assert "t / (2 * sin^2(sqrt(t)))" in gf["generating_function_formula"]
    assert gf["symbolic_operator_identity_verified"] is True
    assert gf["all_taylor_coefficients_match"] is True


# 11. positive moment identity for b_m
def test_11_positive_moment_identity_for_bm(moment_diff_dict: dict) -> None:
    pm = moment_diff_dict["positive_moment_sequence"]
    assert pm["first_10_b_m"][0] == "1/6"
    assert pm["first_10_b_m"][1] == "1/90"
    assert pm["first_10_b_m"][2] == "1/945"
    assert pm["all_b_m_positive_rational"] is True
    assert moment_diff_dict["moment_measure"]["total_mass_b_0"] == "1/6"


# 12. finite-difference positivity for b_m
def test_12_finite_difference_positivity_for_bm(moment_diff_dict: dict) -> None:
    fd = moment_diff_dict["finite_difference_formula"]
    assert fd["b0_difference_all_strictly_positive_0_to_max_n"] is True
    assert fd["single_term_binomial_identity_verified"] is True
    assert fd["c_k_eq_Delta_k_a0_all_nonzero_0_to_max_n"] is True
    assert (
        moment_diff_dict["finite_difference_asymptotics"][
            "symbolic_antiderivative_cancellation_verified"
        ]
        is True
    )


# 13. Newton interpolation exact at nodes
def test_13_newton_interpolation_exact_at_nodes(
    rational_samples: list[Fraction], moment_diff_dict: dict
) -> None:
    c_k = moment_diff_dict["c_k_fractions"]
    for n in (1, 4, 8, 12):
        coeffs = newton_polynomial_power_coeffs(c_k, n)
        assert len(coeffs) == n + 1
        for m in range(n + 1):
            val = sum(coeffs[j] * (Fraction(m) ** j) for j in range(n + 1))
            assert val == rational_samples[m]


# 14. Newton coefficients rational
def test_14_newton_coefficients_rational(moment_diff_dict: dict) -> None:
    c_k = moment_diff_dict["c_k_fractions"]
    coeffs = newton_polynomial_power_coeffs(c_k, 10)
    assert all(isinstance(c, Fraction) for c in coeffs)
    clearing = clear_rational_polynomial_denominators(coeffs)
    assert clearing["lcm_denominator"] >= 1
    assert clearing["gcd_numerator_content"] >= 1
    assert all(isinstance(c, int) for c in clearing["primitive_integer_coeffs"])


# 15. Newton polynomial target-independent
def test_15_newton_polynomial_target_independent(artifact_data: dict) -> None:
    nf = artifact_data["newton_polynomial_family"]
    assert nf["classification"] == NEWTON_ARGUMENT_POLYNOMIALIZATION_PROVED
    assert nf["target_zero_independent"] is True
    assert nf["node_interpolation_exact_verified"] is True
    zf = artifact_data["zero_dependency_firewall"]
    assert zf["candidate_coefficients_depend_on_gamma1"] is False
    assert zf["candidate_coefficients_depend_on_zero_list"] is False
    assert zf["gamma1_used_only_for_evaluation"] is True


# 16. norm polynomial has rational coefficients
def test_16_norm_polynomial_has_rational_coefficients(moment_diff_dict: dict) -> None:
    c_k = moment_diff_dict["c_k_fractions"]
    coeffs = newton_polynomial_power_coeffs(c_k, 5)
    norm_info = construct_ordinate_norm_polynomial(coeffs)
    assert all(isinstance(c, Fraction) for c in norm_info["norm_rational_coeffs"])
    assert norm_info["odd_power_coefficients_all_zero"] is True


# 17. normalized norm polynomial integral
def test_17_normalized_norm_polynomial_integral(moment_diff_dict: dict) -> None:
    c_k = moment_diff_dict["c_k_fractions"]
    coeffs = newton_polynomial_power_coeffs(c_k, 5)
    norm_info = construct_ordinate_norm_polynomial(coeffs)
    assert norm_info["minimal_clearing_factor_C_n"] > 0
    assert norm_info["minimal_divides_universal"] is True
    assert all(isinstance(c, int) for c in norm_info["cleared_integer_coeffs"])
    assert any(c != 0 for c in norm_info["cleared_integer_coeffs"])


# 18. norm polynomial evaluates to squared modulus
def test_18_norm_polynomial_evaluates_to_squared_modulus(
    moment_diff_dict: dict,
) -> None:
    c_k = moment_diff_dict["c_k_fractions"]
    coeffs = newton_polynomial_power_coeffs(c_k, 4)
    norm_info = construct_ordinate_norm_polynomial(coeffs)
    norm_coeffs = norm_info["norm_rational_coeffs"]
    assert norm_info["degree_bound_2d_satisfied"] is True

    for y_test in (Fraction(0), Fraction(3, 2), Fraction(-7, 3), Fraction(14, 1)):
        norm_val = float(
            sum(norm_coeffs[k] * (y_test**k) for k in range(len(norm_coeffs)))
        )
        z_val = complex(0.25, 0.5 * float(y_test))
        poly_val = sum(float(coeffs[j]) * (z_val**j) for j in range(len(coeffs)))
        sq_mod = abs(poly_val) ** 2
        assert abs(norm_val - sq_mod) < 1e-11


# 19. consecutive Newton common-root lemma
def test_19_consecutive_newton_common_root_lemma(
    rational_samples: list[Fraction], moment_diff_dict: dict
) -> None:
    c_k = moment_diff_dict["c_k_fractions"]
    for n in range(1, 8):
        coeffs_n = newton_polynomial_power_coeffs(c_k, n)
        coeffs_np1 = newton_polynomial_power_coeffs(c_k, n + 1)
        assert c_k[n + 1] != 0
        for m in range(n + 1):
            val_n = sum(coeffs_n[j] * (Fraction(m) ** j) for j in range(n + 1))
            val_np1 = sum(
                coeffs_np1[j] * (Fraction(m) ** j) for j in range(n + 2)
            )
            assert val_n == rational_samples[m] > 0
            assert val_np1 == rational_samples[m] > 0


# 20. nonzero sample values at interpolation nodes
def test_20_nonzero_sample_values_at_interpolation_nodes(
    artifact_data: dict,
) -> None:
    nv = artifact_data["newton_nonvanishing_status"]
    assert nv["single_approximant_finite_arb_certified"] is True
    assert nv["consecutive_gcd_verified_n_le_40"] is True
    assert artifact_data["rational_integer_samples"]["all_samples_strictly_positive"] is True


# 21. two-approximant norm sum nonnegative
def test_21_two_approximant_norm_sum_nonnegative(
    moment_diff_dict: dict,
) -> None:
    c_k = moment_diff_dict["c_k_fractions"]
    coeffs_3 = newton_polynomial_power_coeffs(c_k, 3)
    coeffs_4 = newton_polynomial_power_coeffs(c_k, 4)
    norm_3 = construct_ordinate_norm_polynomial(coeffs_3)["norm_rational_coeffs"]
    norm_4 = construct_ordinate_norm_polynomial(coeffs_4)["norm_rational_coeffs"]
    for y_val in (-10.0, -1.5, 0.0, 2.5, 14.134725):
        v3 = sum(float(norm_3[k]) * (y_val**k) for k in range(len(norm_3)))
        v4 = sum(float(norm_4[k]) * (y_val**k) for k in range(len(norm_4)))
        assert v3 >= 0.0
        assert v4 >= 0.0
        assert v3 + v4 > 0.0


# 22. strict positivity only when common-root theorem proved
def test_22_strict_positivity_backed_by_common_root_theorem(
    artifact_data: dict,
) -> None:
    pos = artifact_data["two_approximant_positivity_status"]
    assert (
        pos["classification"]
        == "TWO_APPROXIMANT_STRICT_POSITIVITY_PROVED_ON_COFINAL_NONZERO_DIFFERENCE_SET"
    )
    assert (
        "newton_consecutive_no_common_root_of_nonzero_samples"
        in pos["strict_positivity_condition"]
    )
    assert "two_approximant_norm_sum_strict_pos" in pos["strict_positivity_condition"]
    assert pos["certified_for_all_n_0_to_200"] is True
    assert pos["cofinal_infinite_set_proved"] is True


# 23. Newton remainder identity
def test_23_newton_remainder_identity(artifact_data: dict) -> None:
    rem = artifact_data["newton_remainder_formula"]
    assert "N_n(alpha_1) = -(R(alpha_1) - N_n(alpha_1))" in rem["at_zero_alpha_1"]
    dom = artifact_data["newton_convergence_domain"]
    assert dom["converges_at_alpha_1"] is True
    assert dom["domain"] == "All of C (entire complex plane)"


# 24. Newton asymptotic evidence labelled correctly
def test_24_newton_asymptotic_evidence_labelled_correctly(
    artifact_data: dict,
) -> None:
    rate = artifact_data["newton_smallness_rate"]
    ratio = artifact_data["newton_irrationality_ratio"]
    assert "n^{1/3}" in rate["rational_polynomial_rate"]
    assert "does NOT tend to +infty" in ratio["asymptotic_rational_limit"]
    assert ratio["value_at_n_200_primitive_int"] < -10.0
    assert (
        artifact_data["newton_route_classification"]
        == NEWTON_ARGUMENT_POLYNOMIAL_ROUTE_INSUFFICIENT_SMALLNESS
    )


# 25. no numerical asymptotic promoted to proof
def test_25_no_numerical_asymptotic_promoted_to_proof(
    artifact_data: dict,
) -> None:
    num = artifact_data["numerical_evidence"]
    assert (
        num["evidence_scope"]
        == "NUMERICAL_RECONNAISSANCE_AND_CERTIFIED_FINITE_ENCLOSURES_ONLY_NEVER_ASYMPTOTIC_PROOF"
    )
    assert num["first_zero_certificate"]["ivt_sign_change_certified"] is True


# 26. rational irrationality criterion
def test_26_rational_irrationality_criterion() -> None:
    crit = audit_diophantine_irrationality_and_mahler_criteria()
    rat = crit["rational_irrationality_criterion"]
    assert (
        rat["classification"]
        == INTEGER_AUXILIARY_POLYNOMIAL_SUPERLINEAR_SMALLNESS_IMPLIES_IRRATIONAL
    )
    assert "rational_evaluation_integer_clearing" in rat["lean_theorems"]
    assert "superlinear_log_smallness_irrationality_schema" in rat["lean_theorems"]


# 27. Pade interpolation conditions exact
def test_27_pade_interpolation_conditions_exact(
    rational_samples: list[Fraction],
) -> None:
    for d_a, d_b in ((3, 3), (4, 3), (3, 4)):
        res = solve_multipoint_pade_family(d_a, d_b, rational_samples)
        assert res["interpolation_exact_on_all_nodes"] is True
        assert res["rank"] == d_a + d_b + 1
        assert res["nullspace_dimension"] == 1
        assert res["projectively_unique"] is True


# 28. Pade coefficients rational
def test_28_pade_coefficients_rational(rational_samples: list[Fraction]) -> None:
    res = solve_multipoint_pade_family(3, 3, rational_samples)
    assert all(isinstance(c, Fraction) for c in res["a_coeffs_b0_eq_1"])
    assert all(isinstance(c, Fraction) for c in res["b_coeffs_b0_eq_1"])
    assert all(isinstance(c, int) for c in res["primitive_integer_A_coeffs"])
    assert res["lcm_denominator_A_b0"] >= 1


# 29. Pade candidate independent of target zero
def test_29_pade_candidate_independent_of_target_zero(
    artifact_data: dict,
) -> None:
    ps = artifact_data["pade_degree_schedule"]
    assert set(ps["tested_schedules"]) == {"[n/n]", "[n/(n-1)]", "[(n-1)/n]"}
    assert artifact_data["pade_existence_status"]["status"] == "PROVED_FOR_ALL_N"
    zf = artifact_data["zero_dependency_firewall"]
    assert zf["candidate_coefficients_depend_on_gamma1"] is False
    assert zf["candidate_coefficients_depend_on_zero_list"] is False
    assert zf["gamma1_used_only_for_evaluation"] is True


# 30. Pade rank failure handled deterministically
def test_30_pade_rank_and_nullspace_handled_deterministically(
    artifact_data: dict,
) -> None:
    uniq = artifact_data["pade_uniqueness_status"]
    assert uniq["all_tested_ranks_full"] is True
    assert uniq["all_tested_interpolations_exact"] is True
    assert "fail_closed_policy" in uniq


# 31. Pade target residual identity
def test_31_pade_target_residual_identity(artifact_data: dict) -> None:
    res_form = artifact_data["pade_residual_formula"]
    assert (
        "pade_interpolation_zero_residual_identity"
        in res_form["zero_specialization_identity"]
    )
    assert (
        "E_n(alpha_1) = A_n(alpha_1) - R(alpha_1)*B_n(alpha_1) = A_n(alpha_1)"
        in res_form["zero_specialization_identity"]
    )


# 32. Pade smallness evidence scoped
def test_32_pade_smallness_evidence_scoped(artifact_data: dict) -> None:
    ratio = artifact_data["pade_irrationality_ratio"]
    assert ratio["at_n_25_diagonal_primitive_int"] < -100.0
    assert ratio["diverges_to_plus_infinity"] is False
    assert (
        artifact_data["pade_route_classification"]
        == MULTIPOINT_PADE_ARGUMENT_POLYNOMIALIZATION_PROVED_BUT_FAILS_GATE_Z5_INTEGER_SMALLNESS
    )


# 33. positive Hankel determinant for finite controls
def test_33_positive_hankel_determinant_for_finite_controls() -> None:
    hankel = audit_positive_hankel_determinants_and_coupling(max_n=8)
    ph = hankel["positive_hankel_determinant"]
    assert ph["all_strictly_positive_1_to_max_n"] is True
    assert ph["all_unit_fractions_num_eq_1"] is True
    assert ph["lambert_stieltjes_verified_1_to_max_n"] is True
    assert lambert_stieltjes_hankel_determinant_exact(1) == Fraction(1, 6)
    assert lambert_stieltjes_hankel_determinant_exact(2) == Fraction(1, 18900)
    d3 = lambert_stieltjes_hankel_determinant_exact(3)
    assert d3.numerator == 1 and d3 > 0


# 34. discrete Vandermonde determinant identity
def test_34_discrete_vandermonde_determinant_identity(
    artifact_data: dict,
) -> None:
    and_form = artifact_data["hankel_andreief_formula"]
    assert and_form["discrete_andreief_identity_verified"] is True


# 35. argument coupling distinguished from target-free Hankel positivity
def test_35_argument_coupling_distinguished_from_target_free_hankel_positivity(
    artifact_data: dict,
) -> None:
    ac = artifact_data["argument_coupling_status"]
    assert (
        artifact_data["hankel_route_classification"]
        == FAUZAN_HANKEL_ARGUMENT_TRANSFER_BLOCKED_BY_TARGET_COUPLING_AND_FACTORIAL_MOMENT_DENOMINATORS
    )
    assert "C1_divided_difference_resolvent" in ac
    assert "C2_conjugate_paired_ordinate_resolvent" in ac
    assert "C3_interpolation_hankel_hybrid" in ac


# 36. literal 5 |-> rho substitution rejected
def test_36_literal_5_to_rho_substitution_rejected() -> None:
    fw = audit_firewalls_and_exclusions()
    sub = fw["direct_fauzan_substitution_firewall"]
    assert sub["code"] == DO_NOT_SUBSTITUTE_5_TO_RHO_SYMBOLICALLY


# 37. exponential-polynomial output not misclassified as integer polynomial
def test_37_exponential_polynomial_not_misclassified_as_integer_polynomial() -> None:
    fw = audit_firewalls_and_exclusions()
    exp_fw = fw["exponential_polynomial_firewall"]
    assert exp_fw["enforced"] is True
    assert "NEVER classified as auxiliary integer polynomials" in exp_fw["explanation"]


# 38. algebraicity and irrationality criteria separated
def test_38_algebraicity_and_irrationality_criteria_separated() -> None:
    crit = audit_diophantine_irrationality_and_mahler_criteria()
    mahler = crit["algebraic_liouville_mahler_criterion"]
    assert "d_eq_1_vs_d_ge_2_distinction" in mahler
    assert (
        mahler["secondary_target_status"]
        == "NOT_ATTEMPTED_BEYOND_CRITERION_BECAUSE_IRRATIONALITY_ROUTE_TERMINATES_AT_GATE_Z5"
    )


# 39. no RH assumption
def test_39_no_rh_assumption(artifact_data: dict) -> None:
    assert artifact_data["rh_claimed"] is False
    fw = audit_firewalls_and_exclusions()
    assert fw["rh_assumed"] is False
    assert fw["zero_dependent_candidate_policy"] == ZERO_DEPENDENT_CANDIDATE_REJECTED


# 40. OBL-CT-001A remains open unless genuinely bridged
def test_40_obl_ct_001a_remains_open(artifact_data: dict) -> None:
    assert artifact_data["obl_ct_001a_status"] == "OPEN"
    assert (
        artifact_data["exact_remaining_subgate"]["parallel_subgate_tc_038a_status"]
        == "OPEN"
    )


# 41. earliest failed gate recorded
def test_41_earliest_failed_gate_recorded(artifact_data: dict) -> None:
    assert artifact_data["z1_status"] == Z1_ARGUMENT_TARGET_REPRESENTATION_PROVED
    assert artifact_data["z2_status"] == Z2_ALGEBRAIC_ARGUMENT_POLYNOMIALITY_PROVED
    assert (
        artifact_data["z3_status"]
        == Z3_COFINAL_STRUCTURAL_NONVANISHING_PROVED_FOR_TWO_APPROXIMANT_NORM_SUM
    )
    assert (
        artifact_data["z4_status"]
        == Z4_DEGREE_AND_DENOMINATOR_COMPLEXITY_QUANTIFIED_FACTORIAL_DENOMINATOR_OBSTRUCTION
    )
    assert (
        artifact_data["z5_status"]
        == Z5_SUPERLINEAR_LOG_SMALLNESS_FAILED_IN_TESTED_NEWTON_PADE_HANKEL_CLASSES
    )
    assert artifact_data["z6_status"] == Z6_NOT_REACHED_TERMINATED_AT_GATE_Z5
    assert artifact_data["earliest_failed_gate"] == "Z5"


# 42. principal classification consistent with evidence, schema complete, and Lean theorems verified
def test_42_principal_classification_schema_and_lean_theorems(
    artifact_data: dict,
) -> None:
    for key in REQUIRED_ARTIFACT_KEYS:
        assert key in artifact_data, f"Missing required artifact key: {key}"

    assert artifact_data["task_id"] == TASK_TC_039_ID
    assert artifact_data["principal_classification"] == PRINCIPAL_CLASSIFICATION
    sub = artifact_data["exact_remaining_subgate"]
    assert sub["subgate_tc_039a_status"] == SUBGATE_TC_039A_CLOSED_STATUS
    assert sub["next_subgate_id"] == SUBGATE_TC_040A_ID

    lean_info = verify_fauzan_transfer_lean_theorems(REPO_ROOT)
    assert lean_info["all_required_present"] is True
    assert lean_info["sorry_count"] == 0
    assert lean_info["admit_count"] == 0
    assert lean_info["nonstandard_axiom_count"] == 0
    for thm in REQUIRED_LEAN_THEOREMS:
        assert thm in lean_info["found_theorem_declarations"]
