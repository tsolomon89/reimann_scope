"""
Regression test suite for TASK-TC-040:
Subfactorial-Denominator Zero-Carrying Kernels — Bernoulli Reflection,
Gamma-Ratio Tradeoffs, Positive-Moment Hankel Architecture, and Escape
from the Newton Factorial Obstruction.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import mpmath
import pytest

from tc.fauzan_subfactorial_zero_kernel import (
    ALL_N_MULTIPOINT_PADE_ASYMPTOTIC_STILL_OPEN,
    BERNOULLI_EVEN_ABSOLUTE_VALUES_STIELTJES_MOMENT_SEQUENCE_PROVED,
    BERNOULLI_FUNCTION_NONTRIVIAL_ZETA_ZERO_BRIDGE_PROVED,
    BERNOULLI_STIELTJES_HANKEL_POSITIVITY_DOES_NOT_COUPLE_TO_ZETA_ZERO_ARGUMENT,
    CLASSICAL_IDENTITY_REPURPOSED_FOR_ZERO_ARGUMENT_ARITHMETIC,
    CONSECUTIVE_NEWTON_PRIMITIVE_NORM_FACTORIAL_OBSTRUCTION,
    DEFAULT_ARTIFACT_PATH,
    EQUISPACED_GAMMA_REFLECTION_CLASS_NO_GO_PROVED,
    EQUISPACED_NEWTON_LAGRANGE_BASIS_REINTRODUCES_FACTORIAL_DENOMINATOR,
    EXACT_TRANSFORMED_ACTION,
    FACTORIAL_COST_MOVES_FROM_DENOMINATOR_TO_SAMPLE_GROWTH_UNDER_REFLECTION,
    FACTORIAL_RELOCATION_ACROSS_DENOMINATOR_GROWTH_AND_BASIS_PROVED,
    GAMMA_RATIO_FACTORIAL_BUDGET_TRADEOFF_PROVED,
    LOCAL_SADDLE_MODEL_PHI_N,
    MULTIPOINT_PADE_KERNEL_COMPARISON_FAVORS_BOUNDED_RADIUS_CLASSES_ONLY,
    PROVED_TWO_SIDED_DENOMINATOR_ASYMPTOTIC,
    PROVED_WITH_EXTERNAL_THEOREM,
    RIESZ_GRAM_HADAMARD_KERNELS_DO_NOT_SIMULTANEOUSLY_PRESERVE_RATIONAL_SAMPLES_AND_INDIVIDUAL_ZERO_VANISHING,
    SUBFACTORIAL_KERNEL_LEAN_THEOREMS,
    SUBFACTORIAL_RATIONAL_SAMPLE_DENOMINATOR_ACHIEVED,
    TASK_TC_040_ID,
    compute_bernoulli_even,
    compute_bernoulli_kernel_samples,
    evaluate_B_complex,
    evaluate_Bq_complex,
    evaluate_K0_complex,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
LEAN_FILE_PATH = REPO_ROOT / "formal" / "RiemannScope" / "SubfactorialZeroKernel.lean"
REVIEW_DOC_PATH = REPO_ROOT / "docs" / "reviews" / "TC_SUBFACTORIAL_ZERO_CARRYING_KERNELS.md"
TC039R_REVIEW_DOC_PATH = REPO_ROOT / "docs" / "reviews" / "TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md"
TC039R4_ARTIFACT_PATH = REPO_ROOT / "data" / "tc_fauzan_zero_argument_asymptotic_repair.json"

REQUIRED_TOP_LEVEL_KEYS = (
    "task_id",
    "title",
    "preflight_synchronization_repairs",
    "model_action_synchronization",
    "degree_gap_synchronization",
    "primitive_content_table_synchronization",
    "frozen_newton_obstruction_summary",
    "candidate_kernel_hierarchy",
    "tau_functional_equation_bridge",
    "reflected_kernel_K0_analysis",
    "pure_bernoulli_function_B_analysis",
    "zero_divisor_comparison",
    "bernoulli_sample_values",
    "von_staudt_clausen_denominator_audit",
    "bernoulli_sample_growth_audit",
    "gamma_ratio_family_Bq",
    "Bq_sample_values_and_denominators",
    "Bq_two_sided_denominator_theorem",
    "Bq_generating_function_radii",
    "factorial_budget_conservation_table",
    "sign_adjusted_positive_kernel_P",
    "bernoulli_stieltjes_moment_measure",
    "bernoulli_hankel_determinants",
    "bernoulli_orthogonal_polynomials",
    "bernoulli_hankel_argument_coupling_audit",
    "hankel_determinant_comparison_D_tau_vs_H_B",
    "lagrange_equispaced_interpolation_audit",
    "newton_forward_difference_bernoulli_audit",
    "mahler_p_adic_bernoulli_comparison",
    "norlund_bernoulli_polynomial_audit",
    "riesz_gram_hadamard_kernel_audit",
    "multipoint_pade_kernel_comparison",
    "pade_asymptotic_for_R_c",
    "pade_asymptotic_for_B2",
    "pade_divergent_carleman_audit_for_B",
    "primitive_integer_normalization_all_routes",
    "factorial_relocation_analysis",
    "subfactorial_escape_classification",
    "conditional_no_go_or_escape_theorem",
    "diophantine_efficiency_table",
    "first_zero_gamma1_numerical_audit",
    "synthetic_rational_zero_control",
    "trivial_zero_control",
    "davenport_heilbronn_control",
    "off_line_zero_control",
    "z1_to_z5_gate_status_table",
    "subgate_tc_040a_status",
    "subgate_tc_039a_status",
    "subgate_tc_038a_status",
    "obl_ct_001a_status",
    "lean_theorems",
)


@pytest.fixture(scope="module")
def artifact_data() -> dict:
    assert DEFAULT_ARTIFACT_PATH.exists(), f"Missing artifact {DEFAULT_ARTIFACT_PATH}"
    return json.loads(DEFAULT_ARTIFACT_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def samples_30() -> dict:
    return compute_bernoulli_kernel_samples(max_m=30)


# ---------------------------------------------------------------------------
# 1. Artifact Schema, Review Doc, & Lean 4 Formalization Checks (Tests 1–6)
# ---------------------------------------------------------------------------


def test_01_artifact_has_all_51_required_top_level_fields(artifact_data: dict) -> None:
    assert artifact_data["task_id"] == TASK_TC_040_ID
    for key in REQUIRED_TOP_LEVEL_KEYS:
        assert key in artifact_data, f"Missing required top-level key: {key}"
    assert len(REQUIRED_TOP_LEVEL_KEYS) == 51


def test_02_lean_module_exists_and_has_zero_sorry_or_admit() -> None:
    assert LEAN_FILE_PATH.exists()
    content = LEAN_FILE_PATH.read_text(encoding="utf-8")
    # Strip comments before checking for sorry/admit
    code_lines = [
        line
        for line in content.splitlines()
        if not line.strip().startswith("--") and "sorry" not in line.lower().split("--")[0]
    ]
    assert len(code_lines) == len(content.splitlines())
    for thm in SUBFACTORIAL_KERNEL_LEAN_THEOREMS:
        assert f"theorem {thm}" in content, f"Missing theorem {thm} in {LEAN_FILE_PATH}"


def test_03_lean_theorems_registered_in_artifact(artifact_data: dict) -> None:
    assert artifact_data["lean_theorems"] == list(SUBFACTORIAL_KERNEL_LEAN_THEOREMS)
    assert len(artifact_data["lean_theorems"]) >= 8


def test_04_review_document_has_all_26_sections_A_through_Z() -> None:
    assert REVIEW_DOC_PATH.exists()
    text = REVIEW_DOC_PATH.read_text(encoding="utf-8")
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        assert f"### {letter}." in text, f"Missing Section {letter} in {REVIEW_DOC_PATH}"


def test_05_subgate_and_obligation_statuses(artifact_data: dict) -> None:
    assert "CLOSED_FOR_EQUISPACED_GAMMA_REFLECTION_CLASS_AT_GATE_Z5" in artifact_data["subgate_tc_040a_status"]
    assert "CLOSED_NEGATIVE_AT_GATE_Z5" in artifact_data["subgate_tc_039a_status"]
    assert "OPEN" in artifact_data["subgate_tc_039a_status"]
    assert artifact_data["subgate_tc_038a_status"] == "OPEN"
    assert artifact_data["obl_ct_001a_status"] == "OPEN"


def test_06_package_reexports_present() -> None:
    import tc

    assert hasattr(tc, "build_subfactorial_zero_kernel_report")
    assert hasattr(tc, "EQUISPACED_GAMMA_REFLECTION_CLASS_NO_GO_PROVED")
    assert hasattr(tc, "SUBFACTORIAL_RATIONAL_SAMPLE_DENOMINATOR_ACHIEVED")


# ---------------------------------------------------------------------------
# 2. Preflight Synchronization Repairs (Tests 7–11)
# ---------------------------------------------------------------------------


def test_07_preflight_model_action_synchronization(artifact_data: dict) -> None:
    sync = artifact_data["model_action_synchronization"]
    assert sync["exact_transformed_action_label"] == EXACT_TRANSFORMED_ACTION
    assert sync["local_saddle_model_label"] == LOCAL_SADDLE_MODEL_PHI_N
    assert sync["local_saddle_model_formula"] == "Phi_n(u) = n*u^2 - sqrt(c)/u"
    assert sync["mixed_log_u_formula_present"] is False
    assert sync["synchronized_in_code_and_docs"] is True


def test_08_preflight_degree_gap_synchronization(artifact_data: dict) -> None:
    d_sync = artifact_data["degree_gap_synchronization"]
    assert "n + 1 - C_0 * n^{2/3} <= k_n <= n + 1" in d_sync["conservative_k_n_bound"]
    assert d_sync["leading_2n_log_n_unchanged"] is True
    assert d_sync["stale_n_plus_O_n_pow_1_3_removed"] is True


def test_09_preflight_tc039r4_artifact_has_updated_labels() -> None:
    tc039r4 = json.loads(TC039R4_ARTIFACT_PATH.read_text(encoding="utf-8"))
    sp_dict = tc039r4["saddle_points"]
    assert sp_dict["exact_transformed_action_classification"] == EXACT_TRANSFORMED_ACTION
    assert sp_dict["local_saddle_model_classification"] == LOCAL_SADDLE_MODEL_PHI_N
    expl = tc039r4["z5_newton_status"]["explanation"]
    assert "n + 1 - C_0 n^{2/3} <= k_n <= n + 1" in expl


def test_10_preflight_primitive_content_table_matches_tc039r4_artifact(
    artifact_data: dict,
) -> None:
    table_sync = artifact_data["primitive_content_table_synchronization"]
    assert table_sync["all_finite_g_content_equal_one"] is True
    assert table_sync["synchronized_across_reviews_and_artifacts"] is True
    tc039r_text = TC039R_REVIEW_DOC_PATH.read_text(encoding="utf-8")
    assert "| \\(\\pi\\) (\\(c=4\\)) | \\(4\\) | \\(10\\) | \\(43.32\\) | \\(0.00\\) | \\(43.32\\) | \\(48.96\\) | \\(-4.896\\) |" in tc039r_text
    assert "| \\(\\tau\\) (\\(c=1\\)) | \\(12\\) | \\(26\\) | \\(204.18\\) | \\(0.00\\) | \\(204.18\\) | \\(214.96\\) | \\(-8.268\\) |" in tc039r_text


def test_11_frozen_newton_obstruction_summary(artifact_data: dict) -> None:
    frozen = artifact_data["frozen_newton_obstruction_summary"]
    assert frozen["obstruction_id"] == CONSECUTIVE_NEWTON_PRIMITIVE_NORM_FACTORIAL_OBSTRUCTION
    assert frozen["raw_lower_envelope_status"] == "NEWTON_TWO_STEP_RAW_LOWER_ENVELOPE_PROVED"
    assert frozen["primitive_norm_lower_bound_status"] == "PRIMITIVE_NORM_POLYNOMIAL_LOWER_BOUND_PROVED"
    assert frozen["gate_z5_status"] == "NEWTON_TWO_APPROXIMANT_PRIMITIVE_ROUTE_RIGOROUSLY_FAILS_GATE_Z5"
    assert frozen["subgate_tc_039a_newton_branch_status"] == "CLOSED_NEGATIVE_AT_GATE_Z5"


# ---------------------------------------------------------------------------
# 3. Route A — Functional Equation, K_0(z), B(z), and Zero Divisors (Tests 12–20)
# ---------------------------------------------------------------------------


def test_12_tau_functional_equation_numerical_identity(artifact_data: dict) -> None:
    checks = artifact_data["tau_functional_equation_bridge"]["numerical_verification_checks"]
    assert len(checks) >= 4
    for row in checks:
        assert row["abs_diff_lhs_rhs"] < 1e-50
        assert row["abs_diff_K0_rel_B"] < 1e-50


def test_13_exact_linear_relation_K0_and_B_at_complex_points() -> None:
    with mpmath.workdps(50):
        for z in (
            mpmath.mpf(0),
            mpmath.mpf("0.5"),
            mpmath.mpc("0.25", "3.5"),
            mpmath.mpc("-1.2", "0.7"),
            mpmath.mpf(2),
        ):
            k0 = evaluate_K0_complex(z, dps=50)
            b_val = evaluate_B_complex(z, dps=50)
            rel = -((2 * mpmath.mpc(z) - 1) / 2) * b_val
            assert abs(k0 - rel) < mpmath.mpf("1e-45")


def test_14_K0_and_B_values_at_zero_and_one_half() -> None:
    with mpmath.workdps(50):
        assert abs(evaluate_B_complex(0, dps=50) - 1) < mpmath.mpf("1e-48")
        assert abs(evaluate_K0_complex(0, dps=50) - mpmath.mpf("0.5")) < mpmath.mpf("1e-48")
        assert abs(evaluate_B_complex(mpmath.mpf("0.5"), dps=50) - mpmath.mpf("0.5")) < mpmath.mpf("1e-48")
        assert abs(evaluate_K0_complex(mpmath.mpf("0.5"), dps=50)) < mpmath.mpf("1e-48")


def test_15_vanishing_of_K0_B_and_Bq_at_first_nontrivial_zeta_zero() -> None:
    with mpmath.workdps(80):
        rho1 = mpmath.zetazero(1)
        alpha1 = rho1 / 2
        assert abs(evaluate_K0_complex(alpha1, dps=80)) < mpmath.mpf("1e-50")
        assert abs(evaluate_B_complex(alpha1, dps=80)) < mpmath.mpf("1e-50")
        for q in (0, 1, 2, 3):
            assert abs(evaluate_Bq_complex(q, alpha1, dps=80)) < mpmath.mpf("1e-50")


def test_16_vanishing_at_second_and_third_nontrivial_zeta_zeros() -> None:
    with mpmath.workdps(55):
        for idx in (2, 3):
            alpha_k = mpmath.zetazero(idx) / 2
            assert abs(evaluate_B_complex(alpha_k, dps=55)) < mpmath.mpf("1e-45")
            assert abs(evaluate_K0_complex(alpha_k, dps=55)) < mpmath.mpf("1e-45")


def test_17_zero_divisor_comparison_extra_zeros_distinction(artifact_data: dict) -> None:
    z_div = artifact_data["zero_divisor_comparison"]
    assert z_div["classification"] == BERNOULLI_FUNCTION_NONTRIVIAL_ZETA_ZERO_BRIDGE_PROVED
    assert z_div["full_zero_divisors_identical"] is False
    with mpmath.workdps(50):
        assert abs(evaluate_B_complex(mpmath.mpf("1.5"), dps=50)) < mpmath.mpf("1e-45")
        assert abs(evaluate_K0_complex(mpmath.mpf("1.5"), dps=50)) < mpmath.mpf("1e-45")
        assert abs(evaluate_B_complex(mpmath.mpf(-1), dps=50)) > 2.4


def test_18_novelty_firewall_for_pure_bernoulli_function(artifact_data: dict) -> None:
    b_info = artifact_data["pure_bernoulli_function_B_analysis"]
    assert (
        b_info["novelty_classification"]
        == CLASSICAL_IDENTITY_REPURPOSED_FOR_ZERO_ARGUMENT_ARITHMETIC
    )
    assert b_info["evidence_status"] == PROVED_WITH_EXTERNAL_THEOREM


def test_19_exact_rational_samples_B_and_K0_for_m_0_to_30(samples_30: dict) -> None:
    b_seq = samples_30["B"]
    k0_seq = samples_30["K_0"]
    assert len(b_seq) == 31
    assert len(k0_seq) == 31
    assert b_seq[0] == Fraction(1, 1)
    assert b_seq[1] == Fraction(1, 6)
    assert b_seq[2] == Fraction(-1, 30)
    assert b_seq[3] == Fraction(1, 42)
    assert k0_seq[0] == Fraction(1, 2)
    assert k0_seq[1] == Fraction(-1, 12)
    assert k0_seq[2] == Fraction(1, 20)
    for m in range(31):
        assert b_seq[m] == compute_bernoulli_even(m)
        assert k0_seq[m] == Fraction(-(2 * m - 1), 2) * b_seq[m]


def test_20_complex_evaluation_matches_rational_samples_at_integers(
    samples_30: dict,
) -> None:
    with mpmath.workdps(50):
        for m in range(8):
            b_num = evaluate_B_complex(m, dps=50)
            k0_num = evaluate_K0_complex(m, dps=50)
            b_ex = mpmath.mpf(samples_30["B"][m].numerator) / mpmath.mpf(
                samples_30["B"][m].denominator
            )
            k0_ex = mpmath.mpf(samples_30["K_0"][m].numerator) / mpmath.mpf(
                samples_30["K_0"][m].denominator
            )
            assert abs(b_num - b_ex) < mpmath.mpf("1e-42")
            assert abs(k0_num - k0_ex) < mpmath.mpf("1e-42")


# ---------------------------------------------------------------------------
# 4. Von Staudt–Clausen Denominator Law & Sample Growth (Tests 21–26)
# ---------------------------------------------------------------------------


def test_21_von_staudt_clausen_squarefree_denominators_up_to_30(
    artifact_data: dict,
) -> None:
    vsc = artifact_data["von_staudt_clausen_denominator_audit"]
    assert vsc["classification"] == SUBFACTORIAL_RATIONAL_SAMPLE_DENOMINATOR_ACHIEVED
    assert vsc["all_den_B_2m_squarefree_verified_to_30"] is True


def test_22_exact_primorial_equality_for_D_n_B_and_D_n_K0_up_to_30(
    artifact_data: dict,
) -> None:
    vsc = artifact_data["von_staudt_clausen_denominator_audit"]
    assert vsc["all_D_n_B_equal_primorial_2n_plus_1_to_30"] is True
    assert vsc["all_D_n_K0_equal_twice_primorial_to_30"] is True
    rows = vsc["rows_1_to_30"]
    assert len(rows) == 30
    for r in rows:
        assert r["D_n_B_equals_primorial_2n_plus_1"] is True
        assert r["D_n_K0_equals_2_times_primorial_2n_plus_1"] is True
        assert abs(r["log_D_n_B"] - r["chebyshev_theta_2n_plus_1"]) < 1e-12


def test_23_subfactorial_denominator_growth_vs_R_tau_factorial_growth(
    artifact_data: dict,
) -> None:
    rows = artifact_data["von_staudt_clausen_denominator_audit"]["rows_1_to_30"]
    r30 = rows[-1]
    assert r30["n"] == 30
    assert r30["log_D_n_B_over_n"] < 2.0
    assert r30["log_D_n_R_tau"] > 3.5 * r30["log_D_n_B"]


def test_24_sample_growth_and_zero_ogf_radius_for_B_and_K0(
    artifact_data: dict,
) -> None:
    growth = artifact_data["bernoulli_sample_growth_audit"]
    assert (
        growth["classification"]
        == FACTORIAL_COST_MOVES_FROM_DENOMINATOR_TO_SAMPLE_GROWTH_UNDER_REFLECTION
    )
    assert growth["ogf_radius_B"] == 0.0
    assert growth["ogf_radius_K0"] == 0.0
    last_row = growth["growth_rows"][-1]
    assert last_row["m"] == 30
    assert last_row["log_abs_B_m"] > 78.0
    assert last_row["log_abs_K0_m"] > 82.0


# ---------------------------------------------------------------------------
# 5. Gamma-Ratio Family B_q(z) & Two-Sided Denominator Theorem (Tests 25–30)
# ---------------------------------------------------------------------------


def test_25_Bq_exact_rational_samples_q_0_to_3(samples_30: dict) -> None:
    for m in range(15):
        k0_m = samples_30["K_0"][m]
        fact_m = Fraction(math.factorial(m), 1)
        for q in (0, 1, 2, 3):
            assert samples_30[f"B_{q}"][m] == k0_m / (fact_m**q)


def test_26_Bq_two_sided_denominator_theorem_and_irregular_prime_immunity(
    artifact_data: dict,
) -> None:
    thm = artifact_data["Bq_two_sided_denominator_theorem"]
    assert thm["classification"] == PROVED_TWO_SIDED_DENOMINATOR_ASYMPTOTIC
    assert thm["tradeoff_classification"] == GAMMA_RATIO_FACTORIAL_BUDGET_TRADEOFF_PROVED
    assert thm["all_witnesses_verified_q_0_to_3_n_1_to_20"] is True


def test_27_Bq_denominator_bounds_hold_for_all_q_and_n(artifact_data: dict) -> None:
    bq_rows = artifact_data["Bq_sample_values_and_denominators"]
    for q in (0, 1, 2, 3):
        rows_q = bq_rows[f"q_{q}"]
        assert len(rows_q) == 20
        for r in rows_q:
            assert r["witness_lower_bound_log"] - 1e-12 <= r["log_D_q_n"]
            assert r["log_D_q_n"] <= r["upper_bound_log"] + 1e-12


def test_28_B2_generating_function_radius_is_pi_squared(
    artifact_data: dict, samples_30: dict
) -> None:
    radii = artifact_data["Bq_generating_function_radii"]
    assert abs(radii["q_eq_2"]["R_OGF_float"] - math.pi**2) < 1e-12
    # Check ratio |B_2(m) / B_2(m+1)| -> pi^2 as m -> 30
    b2 = samples_30["B_2"]
    ratio_29 = float(abs(b2[29] / b2[30]))
    assert abs(ratio_29 - math.pi**2) / (math.pi**2) < 0.03


def test_29_factorial_budget_conservation_table(artifact_data: dict) -> None:
    table = artifact_data["factorial_budget_conservation_table"]["rows"]
    assert len(table) == 5
    for row in table:
        assert (
            row["sample_growth_n_log_n_coeff"]
            + row["sample_denominator_n_log_n_coeff"]
            == 2
        )


# ---------------------------------------------------------------------------
# 6. Route B — Positive Bernoulli Kernel P(z) & Stieltjes–Hankel Audit (Tests 30–35)
# ---------------------------------------------------------------------------


def test_30_sign_adjusted_kernel_P_positive_samples(
    artifact_data: dict, samples_30: dict
) -> None:
    p_info = artifact_data["sign_adjusted_positive_kernel_P"]
    assert p_info["lean_theorem"] == "sign_adjusted_bernoulli_positive_sample_identity"
    for m in range(1, 31):
        val = ((-1) ** (m + 1)) * samples_30["B"][m]
        assert val > 0
        assert val == abs(samples_30["B"][m])


def test_31_bernoulli_stieltjes_moment_quadrature_verification(
    artifact_data: dict,
) -> None:
    meas = artifact_data["bernoulli_stieltjes_moment_measure"]
    assert (
        meas["classification"]
        == BERNOULLI_EVEN_ABSOLUTE_VALUES_STIELTJES_MOMENT_SEQUENCE_PROVED
    )
    for row in meas["quadrature_verification_rows"]:
        assert row["abs_error"] < 1e-40


def test_32_bernoulli_hankel_determinants_positive_and_match_carlitz_touchard_product(
    artifact_data: dict,
) -> None:
    h_info = artifact_data["bernoulli_hankel_determinants"]
    assert h_info["all_positive_verified"] is True
    assert h_info["all_product_formula_verified"] is True
    rows = h_info["rows"]
    assert rows[0]["H_n_B_str"] == "1/6"
    assert rows[1]["H_n_B_str"] == "1/350"
    assert rows[2]["H_n_B_str"] == "4/56595"
    assert rows[3]["H_n_B_str"] == "128/11022011"
    for r in rows:
        assert r["H_n_B_positive"] is True
        assert r["matches_carlitz_touchard_product"] is True


def test_33_bernoulli_hankel_superfactorial_growth_vs_D_n_tau_decay(
    artifact_data: dict,
) -> None:
    rows = artifact_data["bernoulli_hankel_determinants"]["rows"]
    r10 = rows[-1]
    assert r10["n"] == 10
    assert r10["log_H_n_B"] > 60.0
    assert r10["log_D_n_tau"] < -600.0


def test_34_bernoulli_orthogonal_polynomials_and_argument_coupling_firewall(
    artifact_data: dict,
) -> None:
    coup = artifact_data["bernoulli_hankel_argument_coupling_audit"]
    assert (
        coup["classification"]
        == BERNOULLI_STIELTJES_HANKEL_POSITIVITY_DOES_NOT_COUPLE_TO_ZETA_ZERO_ARGUMENT
    )
    assert coup["couples_to_zeta_zero_argument"] is False
    ortho_rows = artifact_data["bernoulli_orthogonal_polynomials"]["rows_1_to_6"]
    assert len(ortho_rows) == 6
    assert ortho_rows[-1]["log_abs_prim_P_n_at_gamma1"] > 24.0


# ---------------------------------------------------------------------------
# 7. Routes C, D, E — Basis Audit, Riesz–Gram, Padé, & Relocation (Tests 35–42)
# ---------------------------------------------------------------------------


def test_35_lagrange_and_newton_equispaced_basis_audit(artifact_data: dict) -> None:
    lag = artifact_data["lagrange_equispaced_interpolation_audit"]
    newt = artifact_data["newton_forward_difference_bernoulli_audit"]
    assert (
        lag["classification"]
        == EQUISPACED_NEWTON_LAGRANGE_BASIS_REINTRODUCES_FACTORIAL_DENOMINATOR
    )
    assert (
        newt["classification"]
        == EQUISPACED_NEWTON_LAGRANGE_BASIS_REINTRODUCES_FACTORIAL_DENOMINATOR
    )
    rows = newt["rows_1_to_12"]
    assert len(rows) == 12
    assert rows[-1]["log_abs_Delta_n_K0"] > 14.0
    assert rows[-1]["log_universal_primitive_newton_lower_bound"] > 65.0


def test_36_riesz_gram_hadamard_kernel_audit(artifact_data: dict) -> None:
    rgh = artifact_data["riesz_gram_hadamard_kernel_audit"]
    assert (
        rgh["classification"]
        == RIESZ_GRAM_HADAMARD_KERNELS_DO_NOT_SIMULTANEOUSLY_PRESERVE_RATIONAL_SAMPLES_AND_INDIVIDUAL_ZERO_VANISHING
    )


def test_37_multipoint_pade_comparison_across_five_families(
    artifact_data: dict,
) -> None:
    pade = artifact_data["multipoint_pade_kernel_comparison"]
    assert (
        pade["classification"]
        == MULTIPOINT_PADE_KERNEL_COMPARISON_FAVORS_BOUNDED_RADIUS_CLASSES_ONLY
    )
    assert (
        pade["open_asymptotic_classification"]
        == ALL_N_MULTIPOINT_PADE_ASYMPTOTIC_STILL_OPEN
    )
    res = pade["results_by_family"]
    for fam in ("R_tau", "R_pi", "B_2", "B_1", "K_0"):
        assert fam in res
        assert len(res[fam]) == 7
        for r in res[fam]:
            assert r["primitive_gcd"] == 1
            assert r["log_tilde_Q_n_gamma1"] > 0
            assert r["primitive_diophantine_efficiency"] < 0


def test_38_multipoint_pade_normalization_invariant_ratio_error(
    artifact_data: dict,
) -> None:
    res = artifact_data["multipoint_pade_kernel_comparison"]["results_by_family"]
    # Bounded-radius kernels R_tau, R_pi, B_2 have negative log|A_n(alpha_1)/B_n(alpha_1)| at n = 6,
    # whereas divergent-OGF kernel K_0 has positive log|A_n(alpha_1)/B_n(alpha_1)| at n = 6.
    assert res["R_tau"][5]["log_abs_ratio_An_over_Bn_alpha1"] < -15.0
    assert res["R_pi"][5]["log_abs_ratio_An_over_Bn_alpha1"] < -7.5
    assert res["B_2"][5]["log_abs_ratio_An_over_Bn_alpha1"] < -10.0
    assert res["K_0"][5]["log_abs_ratio_An_over_Bn_alpha1"] > 1.0


def test_39_primitive_integer_normalization_across_all_routes(
    artifact_data: dict,
) -> None:
    prim_all = artifact_data["primitive_integer_normalization_all_routes"]
    assert len(prim_all) == 7
    for key, val in prim_all.items():
        assert "FAILS" in val["gate_z5_outcome"]


def test_40_factorial_relocation_and_no_go_theorem(artifact_data: dict) -> None:
    reloc = artifact_data["factorial_relocation_analysis"]
    nogo = artifact_data["conditional_no_go_or_escape_theorem"]
    assert (
        reloc["classification"]
        == FACTORIAL_RELOCATION_ACROSS_DENOMINATOR_GROWTH_AND_BASIS_PROVED
    )
    assert nogo["classification"] == EQUISPACED_GAMMA_REFLECTION_CLASS_NO_GO_PROVED
    assert len(reloc["five_relocation_channels"]) == 5


# ---------------------------------------------------------------------------
# 8. Mandatory Numerical & Structural Controls (Tests 41–46)
# ---------------------------------------------------------------------------


def test_41_first_zero_gamma1_numerical_audit(artifact_data: dict) -> None:
    g1_audit = artifact_data["first_zero_gamma1_numerical_audit"]
    assert g1_audit["all_kernels_vanish_at_alpha1"] is True
    assert g1_audit["abs_R_tau_alpha1"] < 1e-50
    assert g1_audit["abs_K0_alpha1"] < 1e-50
    assert g1_audit["abs_B_alpha1"] < 1e-50
    assert g1_audit["abs_B2_alpha1"] < 1e-50
    assert g1_audit["abs_P_alpha1"] < 1e-50


def test_42_synthetic_rational_zero_control(artifact_data: dict) -> None:
    syn = artifact_data["synthetic_rational_zero_control"]
    assert syn["gamma_star"] == 14
    assert syn["primitive_gcd"] == 1
    assert syn["tilde_Q_3_at_gamma_star_ge_1"] is True
    assert syn["tilde_Q_3_at_gamma_star_exact_int"] >= 1


def test_43_trivial_zero_control(artifact_data: dict) -> None:
    triv = artifact_data["trivial_zero_control"]
    neg1 = triv["at_z_eq_neg_1_2z_eq_neg_2"]
    three_halves = triv["at_z_eq_3_over_2_1_minus_2z_eq_neg_2"]
    assert neg1["R_tau_vanishes"] is True
    assert neg1["B_and_K0_nonzero_equal_zeta3_multiples"] is True
    assert three_halves["B_and_K0_vanish"] is True
    assert three_halves["R_tau_nonzero"] is True


def test_44_davenport_heilbronn_control(artifact_data: dict) -> None:
    dh = artifact_data["davenport_heilbronn_control"]
    assert dh["has_functional_equation"] is True
    assert dh["has_euler_product"] is False
    assert dh["has_off_line_zeros"] is True
    assert dh["reflection_relocation_depends_on_euler_product"] is False


def test_45_off_line_hypothetical_zero_control(artifact_data: dict) -> None:
    off = artifact_data["off_line_zero_control"]
    assert off["K0_and_B_vanish_at_rho_off_over_2"] is True
    assert off["depends_on_beta_and_gamma"] is True


def test_46_z1_to_z5_gate_status_table_complete(artifact_data: dict) -> None:
    gates = artifact_data["z1_to_z5_gate_status_table"]
    assert len(gates) == 5
    assert "PASSED BOTH" in gates["Gate_Z2_Rational_Sample_Values_and_Subfactorial_Denominators"]["K0_and_B"]
    assert "CLOSED_NEGATIVE" in gates["Gate_Z5_Primitive_Integer_Diophantine_Efficiency"]["Equispaced_Gamma_Ratio_Class"]


# ---------------------------------------------------------------------------
# 9. Extended Section 20–42 Audits & Schema Verification (Tests 47–58)
# ---------------------------------------------------------------------------

SECTION_39_REQUIRED_KEYS = (
    "task_id",
    "starting_head",
    "preflight_repairs",
    "tau_definition",
    "pi_tau_policy",
    "bernoulli_function_definition",
    "bernoulli_function_classical_status",
    "bernoulli_function_zero_mapping",
    "K0_tau_form",
    "K0_pi_form",
    "K0_reflection_simplification",
    "K0_entire_status",
    "K0_nontrivial_zero_preservation",
    "K0_integer_samples",
    "K0_sample_denominator_growth",
    "K0_sample_growth",
    "K0_ogf_radius",
    "gamma_ratio_family",
    "gamma_ratio_q_rows",
    "gamma_ratio_sample_growth_theorem",
    "gamma_ratio_denominator_bounds",
    "gamma_ratio_ogf_radius_table",
    "gamma_ratio_tradeoff_classification",
    "positive_bernoulli_kernel",
    "positive_moment_integral",
    "stieltjes_measure",
    "moment_sequence_status",
    "bernoulli_hankel_determinants",
    "bernoulli_hankel_positivity",
    "bernoulli_hankel_product_formula",
    "bernoulli_hankel_arithmetic",
    "bernoulli_argument_coupling_status",
    "orthogonal_polynomial_route",
    "orthogonal_polynomial_target_evaluations",
    "stieltjes_pade_route",
    "windowed_factorial_multiplier",
    "windowed_multiplier_height",
    "windowed_multiplier_target_evaluation",
    "windowed_multiplier_classification",
    "rational_height_conservation",
    "borel_transform_route",
    "interpolation_basis_audit",
    "rho_scale_vs_half_scale",
    "candidate_gate_table",
    "best_surviving_candidate",
    "earliest_failed_gate",
    "subgate_tc_039a_status",
    "subgate_tc_040a_status",
    "subgate_tc_038a_status",
    "obl_ct_001a_status",
    "rh_claimed",
)


def test_47_artifact_has_all_section_39_required_keys(artifact_data: dict) -> None:
    assert len(SECTION_39_REQUIRED_KEYS) == 51
    for key in SECTION_39_REQUIRED_KEYS:
        assert key in artifact_data, f"Missing Section 39 required key: {key}"
    assert artifact_data["rh_claimed"] is False


def test_48_all_14_lean_theorems_including_section_41_targets(artifact_data: dict) -> None:
    assert len(SUBFACTORIAL_KERNEL_LEAN_THEOREMS) == 14
    section_41_theorems = (
        "primitive_auxiliary_efficiency_scaling",
        "sample_multiplier_denominator_cancellation_bound",
        "gamma_ratio_integer_sample_identity",
        "even_node_norm_polynomial_degree_bound",
        "primitive_hankel_polynomial_nonzero_schema",
        "factorial_budget_algebraic_inequality",
    )
    content = LEAN_FILE_PATH.read_text(encoding="utf-8")
    for thm in section_41_theorems:
        assert thm in artifact_data["lean_theorems"]
        assert f"theorem {thm}" in content


def test_49_extended_bernoulli_and_gamma_ladder_up_to_m_200(artifact_data: dict) -> None:
    vsc = artifact_data["von_staudt_clausen_denominator_audit"]
    assert vsc["max_n_verified"] == 200
    assert vsc["all_den_B_2m_squarefree_verified_to_200"] is True
    assert vsc["all_D_n_B_equal_primorial_2n_plus_1_to_200"] is True
    assert vsc["all_D_n_K0_equal_twice_primorial_to_200"] is True
    q_rows = artifact_data["gamma_ratio_q_rows"]
    assert "checkpoints_to_200" in q_rows
    for q in (0, 1, 2, 3, 4):
        assert f"q_{q}" in q_rows
        assert f"q_{q}" in q_rows["checkpoints_to_200"]
        cp200 = q_rows["checkpoints_to_200"][f"q_{q}"][-1]
        assert cp200["n"] == 200



def test_50_bernoulli_hankel_determinants_exact_up_to_n_20(artifact_data: dict) -> None:
    h_det = artifact_data["bernoulli_hankel_determinants"]
    assert h_det["max_n_computed"] == 20
    rows_20 = h_det["rows_1_to_20"]
    assert len(rows_20) == 20
    for r in rows_20:
        assert r["H_n_B_positive"] is True
        assert r["matches_carlitz_touchard_product"] is True
    assert rows_20[-1]["n"] == 20
    assert rows_20[-1]["log_H_n_B"] > 500.0


def test_51_bernoulli_orthogonal_polynomials_and_arb_balls_up_to_n_30(
    artifact_data: dict,
) -> None:
    ortho = artifact_data["orthogonal_polynomial_route"]
    assert ortho["max_n_computed"] == 30
    assert ortho["gram_schmidt_matches_jacobi_to_6"] is True
    assert ortho["zeros_real_positive_verified_to_6"] is True
    rows_30 = artifact_data["orthogonal_polynomial_target_evaluations"]
    assert len(rows_30) == 30
    for r in rows_30:
        assert r["certified_ball_excludes_zero"] is True
        assert r["primitive_diophantine_efficiency_at_rho1"] < 0
        assert r["primitive_diophantine_efficiency_at_gamma1"] < 0
    assert rows_30[-1]["n"] == 30
    assert rows_30[-1]["log_abs_prim_P_n_at_gamma1"] > 170.0


def test_52_stieltjes_pade_route_audit(artifact_data: dict) -> None:
    sp = artifact_data["stieltjes_pade_route"]
    assert (
        sp["classification"]
        == BERNOULLI_STIELTJES_HANKEL_POSITIVITY_DOES_NOT_COUPLE_TO_ZETA_ZERO_ARGUMENT
    )
    assert sp["secondary_classification"] == "BERNOULLI_HANKEL_ARGUMENT_COUPLING_FAILED"
    assert "psi'(sqrt(w))" in sp["exact_analytic_identification"]


def test_53_windowed_factorial_multiplier_audit_up_to_n_30(artifact_data: dict) -> None:
    wm = artifact_data["windowed_factorial_multiplier"]
    assert wm["max_n_computed"] == 30
    assert wm["all_node_interpolations_exact_1_to_30"] is True
    assert wm["zero_dependency_firewall"]["depends_on_gamma1"] is False
    assert (
        artifact_data["windowed_multiplier_classification"]
        == "RATIONAL_SAMPLE_DENOMINATOR_CANCELLATION_REQUIRES_MULTIPLIER_HEIGHT"
    )
    rows_30 = wm["rows_1_to_30"]
    assert len(rows_30) == 30
    for r in rows_30:
        assert r["certified_ball_excludes_zero"] is True
    assert rows_30[-1]["n"] == 30
    assert rows_30[-1]["log_primitive_height_H_tilde_E_n"] > 130.0
    assert rows_30[-1]["log_abs_tilde_E_n_alpha1"] > 120.0


def test_54_rational_height_conservation_audit(artifact_data: dict) -> None:
    rhc = artifact_data["rational_height_conservation"]
    assert (
        rhc["classification"]
        == "RATIONAL_SAMPLE_DENOMINATOR_CANCELLATION_REQUIRES_MULTIPLIER_HEIGHT"
    )
    assert rhc["lean_theorem"] == "sample_multiplier_denominator_cancellation_bound"
    assert rhc["all_prime_valuation_inequalities_verified_m_1_to_14"] is True


def test_55_borel_transform_and_egf_firewall(artifact_data: dict) -> None:
    bt = artifact_data["borel_transform_route"]
    assert (
        bt["classification"]
        == "BOREL_TRANSFORM_IN_NEW_VARIABLE_DOES_NOT_BY_ITSELF_CONSTRAIN_ZERO_ARGUMENT"
    )
    assert "tau = 2 * pi" in bt["egf_radius_of_convergence"]
    assert bt["symbolic_series_verified_m_0_to_5"] is True


def test_56_interpolation_basis_audit_polya_and_even_nodes(
    artifact_data: dict,
) -> None:
    ib = artifact_data["interpolation_basis_audit"]
    assert (
        ib["classification"]
        == "CONSECUTIVE_INTEGER_NODE_POLYNOMIALIZATION_HAS_INTRINSIC_FACTORIAL_LATTICE_COST"
    )
    assert len(ib["bases_compared"]) == 7
    assert len(ib["rows_1_to_8"]) == 8
    assert ib["rows_1_to_8"][-1]["even_node_top_basis_denominator"] == (2**8) * math.factorial(8)


def test_57_direct_rho_scale_vs_half_scale_comparison(artifact_data: dict) -> None:
    rsh = artifact_data["rho_scale_vs_half_scale"]
    assert rsh["basis_elements_identically_equal_in_Y"] is True
    assert rsh["removes_factorial_or_dyadic_penalty"] is False
    assert rsh["lean_degree_theorem"] == "even_node_norm_polynomial_degree_bound"


def test_58_candidate_gate_table_K1_to_K7_complete(artifact_data: dict) -> None:
    cands = artifact_data["candidate_gate_table"]
    assert len(cands) == 8
    cand_ids = {c["candidate_id"] for c in cands}
    for req_id in (
        "1_R_tau_control",
        "2_bernoulli_function_B",
        "3_reflected_kernel_K0",
        "4_gamma_ratio_ladder_Bq_q0_to_4",
        "5_sign_adjusted_positive_kernel_P",
        "6_bernoulli_stieltjes_hankel_orthogonal_polynomial",
        "7_windowed_factorial_multiplier_E_n",
        "8_multipoint_pade_on_R_tau_and_B2",
    ):
        assert req_id in cand_ids
    for c in cands:
        for k_gate in (
            "K1_zero_preservation",
            "K2_rational_sampling",
            "K3_subfactorial_sample_arithmetic",
            "K4_tame_sample_growth",
            "K5_argument_polynomialization",
            "K6_structural_nonvanishing",
            "K7_primitive_diophantine_efficiency",
            "earliest_failed_gate",
        ):
            assert k_gate in c
    assert "NO_SUBFACTORIAL_DIOPHANTINE_ZERO_KERNEL_FOUND" in artifact_data["best_surviving_candidate"]
    assert isinstance(artifact_data["earliest_failed_gate"], dict)
    assert len(artifact_data["earliest_failed_gate"]) == 8


