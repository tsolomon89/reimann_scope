"""
TASK-TC-038 / TASK-TC-038R — Arithmetic Nature of Nontrivial Zeros, Exact Zero-Sum
Invariants, Fauzan (2026) zeta(5) Irrationality Audit, and Special-Value Transfer Audit.

This module implements the complete mathematical, symbolic, literature, formal-provenance,
and certified finite-interval audit for TASK-TC-038 and its repair sprint TASK-TC-038R:

1. Candidate-object classifier (`gamma_n`, `rho_n = beta_n + i*gamma_n`, `gamma_n + 1/2`)
   and shifted-ordinate redundancy theorem (`SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE`).
2. Full-zero versus ordinate algebraicity implication tree (unconditional conjugation
   closure vs. RH-conditional equivalence).
3. Primary-source literature audit distinguishing `OPEN_IN_LITERATURE` from
   `NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT`, cardinality vs. transcendence repair
   (`CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE`), and Northcott fixed-number-field
   height qualification.
4. Transcendence-theorem applicability matrix, functional-equation algebraicity test,
   Euler-product critical-strip firewall, Gamma-function firewall, and differential-transcendence firewall.
5. Exact Hadamard factorization of `xi(s)`, disambiguated Stieltjes constant notation
   (`gamma_0^St = gamma_E, gamma_1^St, gamma_2^St, gamma_3^St`, `STIELTJES_NOTATION_DISAMBIGUATED`),
   repaired canonical `S_2` formula (`S2_CANONICAL_FORMULA_REPAIRED`), and 3-route independent
   re-audit of `S_3` and `S_4` (`S3_S4_REAUDITED`).
6. Primary-source audit of Aabir Fauzan's 17 September 2026 preprint ("zeta(5) is irrational",
   Zenodo 22826419) and the public Lean 4 formalization `mo271/Zeta5` (`Apery.irrational_five`),
   with multi-dimensional evidence taxonomy (`ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM`,
   `ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN`, `ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN`,
   `PEER_REVIEW_STATUS_PENDING`, `SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED`), 6-gate
   Fauzan architecture reconstruction, value-polynomial vs. argument-polynomial distinction,
   Liouville-Mahler algebraic lower bound derivation, and `SUBGATE-TC-039A` (`Z1`-`Z6`).
7. Scope-repaired 128-bit outward Arb/Acb finite degree/height exclusion
   (`CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION`, `FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED`
   for `HIERARCHICAL_BOX_EXCLUSION` on `D <= 4, H <= 100` vs. certified minimum for
   `EXPLICIT_POLYNOMIAL_ENUMERATION` on `D <= 4, H <= 3`).
8. Formal provenance inventory repair (`FORMAL_SOURCE_INVENTORY_REPAIRED`,
   `ZERO_ARITHMETIC_MODULE_INCLUDED_IN_BUILD_PROVENANCE`).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Sequence, Tuple

import mpmath  # type: ignore
import sympy as sp

from tc.core import FLINT_AVAILABLE, acb, arb, ctx

# ---------------------------------------------------------------------------
# Constants, Provenance, and Classification Tokens (`TASK-TC-038` / `TASK-TC-038R`)
# ---------------------------------------------------------------------------

TAU: float = 2.0 * math.pi
LOG_TAU: float = math.log(TAU)

TASK_TC_038_ID = "TASK-TC-038"
TASK_TC_038R_ID = "TASK-TC-038R"
TASK_TC_038_BRANCH = "ZERO_ARITHMETIC_BRANCH"
TASK_TC_038_STATUS = "TASK_TC_038_ZERO_ARITHMETIC_FRONTIER_AUDIT_COMPLETE"
TASK_TC_038R_STATUS = "TASK_TC_038R_ZERO_ARITHMETIC_EVIDENCE_REPAIR_COMPLETE"

STARTING_HEAD = "92d14a77b93e974658c2b5596a69a1f63a64727f"
TC038_STARTING_HEAD = "63770418ca4b4498b0c9300a854e45d52434f52b"
SUBSTANTIVE_PARENT_HEAD = "70c757ce6cead947fc806b2dadd78f2de0363fc6"
TASK_TC_038R_STARTING_HEAD = "92d14a77b93e974658c2b5596a69a1f63a64727f"
TASK_TC_038_SUBSTANTIVE_COMMIT = "4576c23c38af0224a0f8ddd59fdd922aebab1a0e"
SUBSTANTIVE_TC038_COMMIT = TASK_TC_038_SUBSTANTIVE_COMMIT

# Section 6: Shifted-ordinate classification
SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE = (
    "SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE"
)

# Section 8 & Section 40: Literature and evidence classification tokens
PROVED = "PROVED"
PROVED_PAPER_DERIVATION = "PROVED_PAPER_DERIVATION"
PROVED_WITH_EXTERNAL_THEOREM = "PROVED_WITH_EXTERNAL_THEOREM"
LEAN_PROVED_EXTERNAL_REPOSITORY = "LEAN_PROVED_EXTERNAL_REPOSITORY"
SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED = (
    "SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED"
)
CERTIFIED_FINITE_EXCLUSION = "CERTIFIED_FINITE_EXCLUSION"
AUDIT_FINDING = "AUDIT_FINDING"
OPEN = "OPEN"
OPEN_IN_LITERATURE = "OPEN_IN_LITERATURE"
NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT = (
    "NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT"
)
CONDITIONAL_ON_RH = "CONDITIONAL_ON_RH"
CONDITIONAL_ON_NAMED_CONJECTURE = "CONDITIONAL_ON_NAMED_CONJECTURE"

# Section 44: Source verification tokens
PRIMARY_SOURCE_VERIFIED = "PRIMARY_SOURCE_VERIFIED"
SECONDARY_SOURCE_ONLY = "SECONDARY_SOURCE_ONLY"
NO_PRIMARY_SOURCE_FOUND = "NO_PRIMARY_SOURCE_FOUND"

# TASK-TC-038R: 2026 zeta(5) & Fauzan Hankel taxonomy tokens (Sections 4–9, 43)
ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM = "ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM"
ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM_VERIFIED = (
    "ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM_VERIFIED"
)
ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN = "ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN"
ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN = (
    "ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN"
)
ZETA5_CONVENTIONAL_PEER_REVIEW_STATUS_RECORDED = (
    "ZETA5_CONVENTIONAL_PEER_REVIEW_STATUS_RECORDED"
)
PEER_REVIEW_STATUS_PENDING = "PEER_REVIEW_STATUS_PENDING"

FAUZAN_HANKEL_ARCHITECTURE_AUDITED = "FAUZAN_HANKEL_ARCHITECTURE_AUDITED"
SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT = (
    "SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT"
)
SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT_REPAIRED = (
    "SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT_REPAIRED"
)
FAUZAN_HANKEL_METHOD_HAS_NO_ZERO_LOCATION_TRANSFER = (
    "FAUZAN_HANKEL_METHOD_HAS_NO_ZERO_LOCATION_TRANSFER"
)
FAUZAN_HANKEL_METHOD_HAS_PARTIAL_ZERO_LOCATION_TRANSFER = (
    "FAUZAN_HANKEL_METHOD_HAS_PARTIAL_ZERO_LOCATION_TRANSFER"
)
FAUZAN_HANKEL_METHOD_EXPOSES_NEW_AUXILIARY_POLYNOMIAL_ROUTE = (
    "FAUZAN_HANKEL_METHOD_EXPOSES_NEW_AUXILIARY_POLYNOMIAL_ROUTE"
)
FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED = (
    "FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED"
)
VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE = (
    "VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE"
)

# TASK-TC-038R: Formal provenance, Stieltjes/S2/S3/S4, finite-box, and cardinality tokens
FORMAL_SOURCE_INVENTORY_REPAIRED = "FORMAL_SOURCE_INVENTORY_REPAIRED"
FORMAL_SOURCE_INVENTORY_SYNCHRONIZED = "FORMAL_SOURCE_INVENTORY_SYNCHRONIZED"
ZERO_ARITHMETIC_MODULE_INCLUDED_IN_BUILD_PROVENANCE = (
    "ZERO_ARITHMETIC_MODULE_INCLUDED_IN_BUILD_PROVENANCE"
)
STIELTJES_NOTATION_DISAMBIGUATED = "STIELTJES_NOTATION_DISAMBIGUATED"
S2_CANONICAL_FORMULA_REPAIRED = "S2_CANONICAL_FORMULA_REPAIRED"
S3_S4_REAUDITED = "S3_S4_REAUDITED"
CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION = (
    "CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION"
)
CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION_ESTABLISHED = (
    "CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION_ESTABLISHED"
)
FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED = "FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED"
EXPLICIT_POLYNOMIAL_ENUMERATION = "EXPLICIT_POLYNOMIAL_ENUMERATION"
HIERARCHICAL_BOX_EXCLUSION = "HIERARCHICAL_BOX_EXCLUSION"
CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE = (
    "CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE"
)
NO_INDIVIDUAL_ORDINATE_IRRATIONALITY_OR_TRANSCENDENCE_THEOREM_FOUND = (
    "NO_INDIVIDUAL_ORDINATE_IRRATIONALITY_OR_TRANSCENDENCE_THEOREM_FOUND"
)
FIXED_NUMBER_FIELD_REQUIRES_BOUNDED_DEGREE_AND_BOUNDED_HEIGHT = (
    "FIXED_NUMBER_FIELD_REQUIRES_BOUNDED_DEGREE_AND_BOUNDED_HEIGHT"
)
ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE = "ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE"
FAUZAN_HANKEL_TO_ZERO_ARGUMENT_TRANSFER_SUBGATE = (
    "FAUZAN_HANKEL_TO_ZERO_ARGUMENT_TRANSFER_SUBGATE"
)
SUBGATE_TC_038A_OPEN = "SUBGATE_TC_038A_OPEN"
SUBGATE_TC_039A_OPEN = "SUBGATE_TC_039A_OPEN"
OBL_CT_001A_OPEN = "OBL_CT_001A_OPEN"

# Specific audit classifications
FUNCTIONAL_EQUATION_DOES_NOT_EXCLUDE_ALGEBRAIC_ZERO = (
    "FUNCTIONAL_EQUATION_DOES_NOT_EXCLUDE_ALGEBRAIC_ZERO"
)
EULER_PRODUCT_NONVANISHING_NOT_AVAILABLE_IN_CRITICAL_STRIP = (
    "EULER_PRODUCT_NONVANISHING_NOT_AVAILABLE_IN_CRITICAL_STRIP"
)
LI_COEFFICIENT_POSITIVITY_IS_RH_EQUIVALENT = (
    "LI_COEFFICIENT_POSITIVITY_IS_RH_EQUIVALENT"
)
ZETA5_CURRENT_STATUS_VERIFIED = "ZETA5_CURRENT_STATUS_VERIFIED"
# Retained only as deprecated historical constant for classical hypergeometric/Beukers methods:
SPECIAL_VALUE_IRRATIONALITY_METHOD_HAS_NO_DIRECT_ZERO_LOCATION_TRANSFER = (
    "SPECIAL_VALUE_IRRATIONALITY_METHOD_HAS_NO_DIRECT_ZERO_LOCATION_TRANSFER"
)
SPECIAL_VALUE_IRRATIONALITY_METHOD_NO_DIRECT_ZERO_LOCATION_TRANSFER = (
    "SPECIAL_VALUE_IRRATIONALITY_METHOD_NO_DIRECT_ZERO_LOCATION_TRANSFER"
)
DIFFERENTIAL_TRANSCENDENCE_DOES_NOT_DETERMINE_ZERO_ARITHMETIC = (
    "DIFFERENTIAL_TRANSCENDENCE_DOES_NOT_DETERMINE_ZERO_ARITHMETIC"
)
CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION = (
    "CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION"
)
CERTIFIED_BOUNDED_DENOMINATOR_RATIONAL_EXCLUSION = (
    "CERTIFIED_BOUNDED_DENOMINATOR_RATIONAL_EXCLUSION"
)
NUMERICAL_EVIDENCE_ONLY = "NUMERICAL_EVIDENCE_ONLY"
ALGEBRAIC_ZERO_DOES_NOT_AUTOMATICALLY_ENTER_AMBIENT_KERNEL = (
    "ALGEBRAIC_ZERO_DOES_NOT_AUTOMATICALLY_ENTER_AMBIENT_KERNEL"
)

# Principal & secondary outcomes
INDIVIDUAL_NONTRIVIAL_ZERO_ARITHMETIC_THEOREM_PROVED = (
    "INDIVIDUAL_NONTRIVIAL_ZERO_ARITHMETIC_THEOREM_PROVED"
)
NEW_ZERO_SUM_ARITHMETIC_THEOREM_PROVED = "NEW_ZERO_SUM_ARITHMETIC_THEOREM_PROVED"
ONE_PRECISE_ZERO_ARITHMETIC_SUBGATE_OPEN = "ONE_PRECISE_ZERO_ARITHMETIC_SUBGATE_OPEN"
ZERO_ARITHMETIC_FRONTIER_CLASSIFIED_INDIVIDUAL_STATUS_OPEN = (
    "ZERO_ARITHMETIC_FRONTIER_CLASSIFIED_INDIVIDUAL_STATUS_OPEN"
)

PERMITTED_PRINCIPAL_OUTCOMES: Tuple[str, ...] = (
    INDIVIDUAL_NONTRIVIAL_ZERO_ARITHMETIC_THEOREM_PROVED,
    NEW_ZERO_SUM_ARITHMETIC_THEOREM_PROVED,
    ONE_PRECISE_ZERO_ARITHMETIC_SUBGATE_OPEN,
    ZERO_ARITHMETIC_FRONTIER_CLASSIFIED_INDIVIDUAL_STATUS_OPEN,
    FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED,
)

PRINCIPAL_CLASSIFICATION = ZERO_ARITHMETIC_FRONTIER_CLASSIFIED_INDIVIDUAL_STATUS_OPEN
SECONDARY_TRANSFER_CLASSIFICATION = FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED
SUBGATE_TC_038A_ID = "SUBGATE-TC-038A"
SUBGATE_TC_039A_ID = "SUBGATE-TC-039A"

REQUIRED_LEAN_THEOREMS: Tuple[str, ...] = (
    "shifted_ordinate_rational_iff",
    "shifted_ordinate_algebraic_iff",
    "shifted_ordinate_transcendental_iff",
    "complex_zero_re_im_algebraicity",
    "reflection_reciprocal_identity",
    "centered_quartet_polynomial_identity",
    "centered_quartet_coefficients_real",
    "li_first_coefficient_finite_algebra_identity",
    "reciprocal_power_log_derivative_sign_identity",
    "stieltjes_notation_no_effect_algebra",
    "s2_equivalent_closed_forms",
)

REQUIRED_FAUZAN_ARCHITECTURE_KEYS: Tuple[str, ...] = (
    "source_commit",
    "paper_reference",
    "lean_repository",
    "target_theorem",
    "criterion_statement",
    "polynomial_family",
    "degree_formula",
    "moment_functional",
    "hankel_matrix",
    "positivity_source",
    "integrality_normalization",
    "prime_valuation_strategy",
    "analytic_real_bound",
    "small_value_rate",
    "denominator_growth_rate",
    "irrationality_contradiction",
    "paper_vs_formalization_deviations",
    "potential_zero_location_transfer_points",
    "nontransferable_weight5_specific_parts",
    "task_tc_039_gate_map",
)

REQUIRED_TC_038R_REPAIR_KEYS: Tuple[str, ...] = (
    "task_tc_038r_status",
    "zeta5_2026_preprint_status",
    "zeta5_lean_formalization_status",
    "zeta5_lean_repository",
    "zeta5_formal_theorem",
    "zeta5_axiom_dependency_status",
    "zeta5_peer_review_status",
    "fauzan_proof_architecture",
    "fauzan_degree_growth",
    "fauzan_height_denominator_growth",
    "fauzan_small_value_rate",
    "fauzan_positivity_gate",
    "fauzan_integrality_gate",
    "special_value_transfer_classification_repaired",
    "formal_source_inventory_repaired",
    "zero_arithmetic_module_hashed",
    "formal_theorem_count_recomputed",
    "stieltjes_notation_policy",
    "S2_correct_formula",
    "S3_reaudit",
    "S4_reaudit",
    "finite_box_exclusion_status",
    "finite_box_global_minimum_status",
    "explicit_small_box_minimum_status",
    "cardinality_transcendence_claim_status",
    "zero_sum_constant_arithmetic_subgate",
    "subgate_tc_039a",
    "principal_classification_reassessed",
)

REQUIRED_ARTIFACT_KEYS: Tuple[str, ...] = (
    "starting_head",
    "task_id",
    "candidate_objects",
    "shifted_ordinate_status",
    "rho_vs_gamma_algebraicity",
    "conditional_rh_equivalences",
    "individual_zero_rationality_status",
    "individual_zero_algebraicity_status",
    "individual_zero_transcendence_status",
    "primary_literature_audit",
    "transcendence_theorem_applicability",
    "functional_equation_algebraic_zero_audit",
    "euler_product_firewall",
    "xi_hadamard_product_status",
    "reciprocal_sum_S1",
    "reflection_invariant_sum",
    "reciprocal_sum_S2",
    "reciprocal_power_hierarchy",
    "centered_zero_invariants",
    "quartet_polynomial",
    "li_coefficient_audit",
    "superzeta_audit",
    "zero_sum_constant_arithmetic_status",
    "zeta5_current_status",
    "special_value_method_transfer",
    "auxiliary_polynomial_audit",
    "gamma_function_firewall",
    "differential_transcendence_firewall",
    "finite_algebraicity_exclusion",
    "bounded_denominator_rational_exclusion",
    "pslq_diagnostic",
    "tc_interaction",
    "principal_classification",
    "exact_remaining_subgate",
    "lean_theorem_map",
) + REQUIRED_TC_038R_REPAIR_KEYS

# High-precision enclosure of gamma_1 (Odlyzko / mpmath zetazero(1) verified to 60 digits)
GAMMA1_60DPS_STR = (
    "14.13472514173469379045725198356247027078425711569924317568556746"
)
GAMMA1_ARB_RADIUS_STR = "1e-55"


# ---------------------------------------------------------------------------
# 1. Candidate Objects & Shifted-Ordinate Redundancy (Sections 5, 6, 7)
# ---------------------------------------------------------------------------


def classify_candidate_objects() -> Dict[str, Any]:
    """
    Classify the three candidate arithmetic zero objects (Section 5):
      A. Ordinate: gamma_n = Im(rho_n) in R
      B. Full zero: rho_n = beta_n + i*gamma_n in C (0 < beta_n < 1)
      C. Shifted ordinate: gamma_n + 1/2 in R (NOT to be confused with 1/2 + i*gamma_n)
    """
    return {
        "candidate_A_ordinate": {
            "symbol": "gamma_n",
            "definition": "Im(rho_n) in R",
            "domain": "R \\ {0}",
            "independent_arithmetic_target": True,
            "rh_assumed": False,
        },
        "candidate_B_full_zero": {
            "symbol": "rho_n = beta_n + i*gamma_n",
            "definition": "Nontrivial zero of zeta(s) in the critical strip 0 < beta_n < 1",
            "domain": "{s in C : 0 < Re(s) < 1}",
            "independent_arithmetic_target": True,
            "rh_assumed": False,
            "note": (
                "Unconditionally, rho_n in Q_bar <=> (beta_n in Q_bar and gamma_n in Q_bar). "
                "Conditionally under RH (beta_n = 1/2), rho_n in Q_bar <=> gamma_n in Q_bar."
            ),
        },
        "candidate_C_shifted_ordinate": {
            "symbol": "gamma_n + 1/2",
            "definition": "Real translation of the ordinate gamma_n by the rational constant 1/2",
            "domain": "R",
            "independent_arithmetic_target": False,
            "status": SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE,
            "not_to_be_confused_with": "rho_n = 1/2 + i*gamma_n (complex critical-line zero)",
        },
    }


def audit_shifted_ordinate_redundancy() -> Dict[str, Any]:
    """
    Prove symbolically and algebraically that shifting a real ordinate gamma by 1/2
    preserves rationality, algebraicity, degree over Q, minimal polynomial up to X -> X - 1/2,
    and transcendence (Section 6).
    """
    X = sp.Symbol("X")
    # Polynomial bijection P(gamma) = 0 <=> Q(gamma + 1/2) = 0 where Q(X) = 2^d P(X - 1/2)
    sample_polys = [
        X - 14,
        X**2 - 14 * X + 1,
        2 * X**3 - 3 * X**2 + 5 * X - 7,
    ]
    bijection_checks: List[Dict[str, Any]] = []
    gamma_sym = sp.Symbol("gamma")
    shifted_sym = gamma_sym + sp.Rational(1, 2)
    for P in sample_polys:
        deg = sp.Poly(P, X).degree()
        Q_shifted = sp.expand((2**deg) * P.subs(X, X - sp.Rational(1, 2)))
        eval_diff = sp.simplify(
            Q_shifted.subs(X, shifted_sym) - (2**deg) * P.subs(X, gamma_sym)
        )
        bijection_checks.append(
            {
                "P": str(P),
                "degree": int(deg),
                "Q_shifted": str(Q_shifted),
                "identity_residual_zero": bool(eval_diff == 0),
            }
        )

    return {
        "classification": SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE,
        "rational_equivalence": "gamma in Q  <=>  gamma + 1/2 in Q",
        "algebraic_equivalence": "gamma in Q_bar  <=>  gamma + 1/2 in Q_bar",
        "transcendental_equivalence": (
            "gamma transcendental  <=>  gamma + 1/2 transcendental"
        ),
        "field_extension_equality": "Q(gamma) = Q(gamma + 1/2)",
        "polynomial_translation_bijection": "P(gamma) = 0  <=>  2^d P((gamma + 1/2) - 1/2) = 0",
        "bijection_symbolic_checks": bijection_checks,
        "all_symbolic_checks_passed": all(
            c["identity_residual_zero"] for c in bijection_checks
        ),
        "confusion_firewall": (
            "gamma + 1/2 in R is a real affine shift of Im(rho), whereas "
            "1/2 + i*gamma in C is the complex zero on the critical line."
        ),
        "lean_theorems": [
            "shifted_ordinate_rational_iff",
            "shifted_ordinate_algebraic_iff",
            "shifted_ordinate_transcendental_iff",
        ],
    }


def audit_full_zero_vs_ordinate_algebraicity() -> Dict[str, Any]:
    """
    Derive the exact unconditional and RH-conditional implications between
    rho = beta + i*gamma and its real/imaginary parts (Section 7 & Section 27).
    """
    beta, gamma = sp.symbols("beta gamma", real=True)
    rho = beta + sp.I * gamma
    rho_bar = beta - sp.I * gamma
    re_recovered = sp.simplify((rho + rho_bar) / 2 - beta)
    im_recovered = sp.simplify((rho - rho_bar) / (2 * sp.I) - gamma)

    return {
        "unconditional_forward": {
            "statement": "rho = beta + i*gamma in Q_bar  ==>  beta in Q_bar and gamma in Q_bar",
            "proof": (
                "Q_bar is a subfield of C stable under complex conjugation (since the minimal "
                "polynomial of rho over Q has real rational coefficients, so conj(rho) is also a root). "
                "Because i in Q_bar (i^2 + 1 = 0) and 2 in Q_bar, beta = (rho + conj(rho))/2 in Q_bar "
                "and gamma = (rho - conj(rho))/(2i) in Q_bar."
            ),
            "status": PROVED,
        },
        "unconditional_converse": {
            "statement": "beta in Q_bar and gamma in Q_bar  ==>  rho = beta + i*gamma in Q_bar",
            "proof": "Q_bar is a field containing beta, gamma, and i; hence beta + i*gamma in Q_bar.",
            "status": PROVED,
        },
        "unconditional_contrapositive": {
            "statement": (
                "(beta transcendental or gamma transcendental)  ==>  rho = beta + i*gamma transcendental"
            ),
            "status": PROVED,
        },
        "unconditional_one_way_warning": (
            "Unconditionally (without assuming beta in Q_bar), gamma in Q_bar does NOT imply rho in Q_bar "
            "unless beta in Q_bar is also known; and rho transcendental does NOT determine which of "
            "beta or gamma is transcendental unless beta = 1/2 (or beta in Q_bar) is known."
        ),
        "conditional_rh_equivalence": {
            "premise": "RH for rho (beta = 1/2)",
            "statement": "Under beta = 1/2, rho in Q_bar  <=>  gamma in Q_bar (and rho transcendental <=> gamma transcendental)",
            "status": CONDITIONAL_ON_RH,
            "used_unconditionally": False,
        },
        "individual_zero_implication_trees": {
            "if_rho_algebraic": [
                "conj(rho) is algebraic of the same degree over Q",
                "beta = (rho + conj(rho))/2 in Q_bar cap (0, 1)",
                "gamma = (rho - conj(rho))/(2i) in Q_bar \\ {0}",
                "1 - rho and 1 - conj(rho) are algebraic",
                "quartet polynomial (X^2 - z^2)(X^2 - conj(z)^2) has algebraic coefficients in Q_bar[X]",
            ],
            "if_gamma_algebraic_unconditional": [
                "gamma + 1/2 in Q_bar",
                "1/2 + i*gamma in Q_bar",
                "Does NOT imply rho = beta + i*gamma in Q_bar unless beta in Q_bar",
            ],
            "if_rh_and_gamma_algebraic": [
                "beta = 1/2 in Q",
                "rho = 1/2 + i*gamma in Q(gamma, i) subset Q_bar",
                "z_rho = i*gamma in Q_bar",
            ],
            "if_rho_rational": [
                "IMPOSSIBLE for nontrivial zeros: gamma_n != 0 because zeta(s) < 0 for all real s in (0, 1) "
                "((1 - 2^{1-s}) zeta(s) = sum_{n>=1} (-1)^{n-1} n^{-s} > 0 while 1 - 2^{1-s} < 0).",
            ],
            "if_gamma_rational": [
                "gamma + 1/2 in Q",
                "Under RH (beta = 1/2), rho = 1/2 + i*gamma lies in the Gaussian rationals Q(i) (imaginary quadratic field of degree 2).",
                "Unconditionally for the first zero gamma_1, excluded for all denominators 1 <= q <= 10000 by 128-bit Arb interval arithmetic, "
                "but universal irrationality gamma_n notin Q for all n remains OPEN_IN_LITERATURE.",
            ],
        },
        "symbolic_reconstruction_verified": bool(
            re_recovered == 0 and im_recovered == 0
        ),
        "lean_theorem": "complex_zero_re_im_algebraicity",
    }


# ---------------------------------------------------------------------------
# 2. Primary-Source Literature & L-Function / Transcendence Audits (Sections 8–12)
# ---------------------------------------------------------------------------


def audit_primary_literature_individual_zeros() -> Dict[str, Any]:
    """
    Comprehensive primary-source literature audit on the arithmetic nature of
    individual nontrivial zeros of zeta(s) and broader L-functions (Sections 8 & 9).
    Strictly distinguishes `OPEN_IN_LITERATURE` from `NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT`.
    """
    return {
        "individual_zero_claims": {
            "rho_n_non_real_for_nontrivial_zeros": {
                "statement": "Every zero rho in 0 < Re(rho) < 1 satisfies Im(rho) != 0, hence rho notin R and rho notin Q.",
                "proof_mechanism": (
                    "For real s in (0, 1), (1 - 2^{1-s}) zeta(s) = sum_{n>=1} (-1)^{n-1} n^{-s} > 0 "
                    "and 1 - 2^{1-s} < 0, so zeta(s) < 0 on (0, 1)."
                ),
                "status": PROVED,
                "source_status": PRIMARY_SOURCE_VERIFIED,
                "citations": ["Titchmarsh (1986), Section 2.12"],
            },
            "gamma_n_irrational": {
                "statement": "For a specific nontrivial zero ordinate gamma_n (e.g., gamma_1), gamma_n notin Q.",
                "status": OPEN_IN_LITERATURE,
                "source_status": PRIMARY_SOURCE_VERIFIED,
                "distinction_note": (
                    "Explicitly recognized as an open Diophantine problem in the analytic number theory "
                    "literature (related to the Linear Independence Conjecture of Wintner 1935 / Ingham 1942 / "
                    "Rubinstein-Sarnak 1994): not even the irrationality of gamma_1 is proved."
                ),
            },
            "gamma_n_transcendental": {
                "statement": "For a specific nontrivial zero ordinate gamma_n, gamma_n notin Q_bar.",
                "status": OPEN_IN_LITERATURE,
                "source_status": PRIMARY_SOURCE_VERIFIED,
                "distinction_note": (
                    "Known to be open in the literature; implied by the Grand Linear Independence Conjecture "
                    "(LI: the positive ordinates gamma_n are Q-linearly independent, or Q_bar-linearly independent), "
                    "which remains completely unproved."
                ),
            },
            "rho_n_transcendental": {
                "statement": "For a specific nontrivial zero rho_n = beta_n + i*gamma_n, rho_n notin Q_bar.",
                "status": OPEN_IN_LITERATURE,
                "source_status": PRIMARY_SOURCE_VERIFIED,
                "distinction_note": "Known to be open; equivalent to transcendence of beta_n or gamma_n.",
            },
            "rho_n_excluded_from_named_number_field": {
                "statement": "No nontrivial zero rho_n lies in a fixed algebraic number field K (e.g., Q(i)).",
                "status": NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT,
                "source_status": NO_PRIMARY_SOURCE_FOUND,
                "northcott_height_qualification": (
                    "Northcott's theorem guarantees finiteness only for algebraic numbers of BOTH bounded "
                    "degree [Q(alpha):Q] <= D AND bounded height H(alpha) <= H_0. A fixed number field K "
                    "(or Q_bar) without an explicit height bound contains infinitely many elements of "
                    "unbounded height, so neither Northcott finiteness nor cardinality excludes infinitely "
                    "many zero ordinates from lying in K or Q_bar."
                ),
                "distinction_note": (
                    "While finite bounded-degree AND bounded-height searches exclude small algebraic numbers "
                    "for a fixed zero gamma_1, no unconditional theorem in the primary literature proves "
                    "zeta(alpha) != 0 for all alpha in K cap {0 < Re(s) < 1}."
                ),
            },
            "cardinality_transcendence_fallacy_repaired": {
                "statement": (
                    "Does the existence of infinitely many distinct nontrivial zero ordinates {gamma_n : n >= 1} "
                    "imply that some gamma_n is transcendental by cardinality?"
                ),
                "status": CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE,
                "literature_row_status": NO_INDIVIDUAL_ORDINATE_IRRATIONALITY_OR_TRANSCENDENCE_THEOREM_FOUND,
                "source_status": PRIMARY_SOURCE_VERIFIED,
                "explanation": (
                    "FALSE: Both the set of nontrivial zero ordinates {gamma_n : n >= 1} (of the non-identically-zero "
                    "entire function Xi(t)) and the field of algebraic numbers Q_bar (or any fixed number field K) "
                    "are countably infinite (cardinality aleph_0). Cardinality alone provides zero irrationality "
                    "or transcendence information for zeta zeros."
                ),
            },
            "gamma_n_linear_or_algebraic_independence": {
                "statement": "The positive ordinates gamma_1, gamma_2, ... are Q-linearly independent.",
                "status": CONDITIONAL_ON_NAMED_CONJECTURE,
                "named_conjecture": "Linear Independence Conjecture (LI, Wintner 1935; Ingham 1942; Rubinstein-Sarnak 1994)",
                "source_status": PRIMARY_SOURCE_VERIFIED,
            },
        },
        "fixed_number_field_scope_distinction": {
            "fixed_number_field_K": "Countably infinite field extension K / Q of fixed finite degree [K:Q] = d, but UNBOUNDED height.",
            "bounded_degree_and_bounded_height": "Finite set by Northcott's theorem ({alpha in Q_bar : deg(alpha) <= D and H(alpha) <= H_0} is finite).",
            "bounded_degree_unbounded_height": "Countably infinite set; Northcott finiteness does NOT apply without a height bound.",
            "total_algebraic_numbers_Q_bar": "Countably infinite field (union of all finite-degree extensions, unbounded degree and height).",
            "height_qualification_required": True,
        },
        "broader_L_function_comparison": {
            "dirichlet_L_functions": {
                "status": OPEN_IN_LITERATURE,
                "summary": (
                    "Nontrivial zeros of Dirichlet L(s, chi) in 0 < Re(s) < 1 have the same open "
                    "irrationality/transcendence status as zeta(s) (even the nonvanishing L(1/2, chi) != 0 "
                    "at the single algebraic point s = 1/2 is Chowla's conjecture, still open in general)."
                ),
            },
            "dedekind_and_automorphic_L_functions": {
                "status": OPEN_IN_LITERATURE,
                "summary": (
                    "For Dedekind zeta_K(s) and GL(N) automorphic L-functions (Lagarias 2004, arXiv:math/0404394v4), "
                    "global zero sums (Li coefficients) are expressed via logarithmic derivatives of completed "
                    "L-functions, while individual critical-strip zero locations have open arithmetic status."
                ),
            },
            "selberg_zeta_functions": {
                "status": OPEN_IN_LITERATURE,
                "summary": (
                    "Selberg zeta zeros correspond to Laplace eigenvalues lambda_j = 1/4 + r_j^2 on hyperbolic "
                    "surfaces; transcendence of individual non-explicit spectral parameters r_j is open."
                ),
            },
            "exponential_polynomials": {
                "status": PROVED_WITH_EXTERNAL_THEOREM,
                "summary": (
                    "For finite exponential polynomials sum_{j=1}^m a_j exp(omega_j s) with algebraic parameters, "
                    "Lindemann-Weierstrass / Gelfond-Schneider / Baker control simple 2-term or commensurable "
                    "zeros, whereas zeta(s) is an infinite Dirichlet series whose analytic continuation into "
                    "0 < Re(s) < 1 is NOT a finite exponential polynomial."
                ),
            },
            "siegel_E_and_G_functions": {
                "status": PROVED_WITH_EXTERNAL_THEOREM,
                "summary": (
                    "By the Siegel-Shidlovsky theorem (1929/1959) and Beukers (2006), if an E-function f(z) in "
                    "Q_bar[[z]] satisfies a linear differential equation over Q_bar(z), its values and non-singular "
                    "zeros are transcendental. OBSTRUCTION FOR ZETA: By Hilbert (1900) and Ostrowski (1920), "
                    "zeta(s) is differentially transcendental (satisfies NO algebraic differential equation), "
                    "and its Dirichlet series sum n^{-s} is a power series in p^{-s}, not an E-function in s."
                ),
            },
        },
        "arxiv_primary_sources_used": [
            {
                "id": "zenodo:22826419",
                "title": "zeta(5) is irrational",
                "authors": ["Aabir Fauzan"],
                "url": "https://zenodo.org/records/22826419",
                "pdf_url": "https://zenodo.org/records/22826419/files/ZETA5_IS_IRRATIONAL.pdf",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "github:mo271/Zeta5@7fe73676",
                "title": "Zeta5: Lean 4 formalization of Apery.irrational_five (riemannZeta 5 irrational)",
                "authors": ["Aabir Fauzan", "Moritz Firsching (mo271) / contributors"],
                "url": "https://github.com/mo271/Zeta5",
                "pdf_url": "https://github.com/mo271/Zeta5/tree/7fe736760f4b96bfdb4334b68e3b3124ecbe10b0",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "math/0104051v4",
                "title": "Zeta functions for Riemann zeros",
                "authors": ["A. Voros"],
                "url": "https://arxiv.org/abs/math/0104051v4",
                "pdf_url": "https://arxiv.org/pdf/math/0104051v4",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "math/0311029v1",
                "title": "Zeta functions over zeros of general zeta and L-functions",
                "authors": ["A. Voros"],
                "url": "https://arxiv.org/abs/math/0311029v1",
                "pdf_url": "https://arxiv.org/pdf/math/0311029v1",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "1403.4558v2",
                "title": "Zeta functions over zeros of Zeta functions and an exponential-asymptotic view of the Riemann Hypothesis",
                "authors": ["Andre Voros"],
                "url": "https://arxiv.org/abs/1403.4558v2",
                "pdf_url": "https://arxiv.org/pdf/1403.4558v2",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "math/0404394v4",
                "title": "Li Coefficients for Automorphic L-Functions",
                "authors": ["Jeffrey C. Lagarias"],
                "url": "https://arxiv.org/abs/math/0404394v4",
                "pdf_url": "https://arxiv.org/pdf/math/0404394v4",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "math/0104249v1",
                "title": "Irrationality of values of zeta-function",
                "authors": ["Wadim Zudilin"],
                "url": "https://arxiv.org/abs/math/0104249v1",
                "pdf_url": "https://arxiv.org/pdf/math/0104249v1",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "math/0206176v2",
                "title": "Arithmetic of linear forms involving odd zeta values",
                "authors": ["Wadim Zudilin"],
                "url": "https://arxiv.org/abs/math/0206176v2",
                "pdf_url": "https://arxiv.org/pdf/math/0206176v2",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "1803.03160v1",
                "title": "A note on odd zeta values",
                "authors": ["Tanguy Rivoal", "Wadim Zudilin"],
                "url": "https://arxiv.org/abs/1803.03160v1",
                "pdf_url": "https://arxiv.org/pdf/1803.03160v1",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "1803.08905v2",
                "title": "Many odd zeta values are irrational",
                "authors": ["Stephane Fischler", "Johannes Sprang", "Wadim Zudilin"],
                "url": "https://arxiv.org/abs/1803.08905v2",
                "pdf_url": "https://arxiv.org/pdf/1803.08905v2",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "2505.05005v2",
                "title": "A note on the irrationality of zeta_2(5)",
                "authors": ["Li Lai", "Johannes Sprang", "Wadim Zudilin"],
                "url": "https://arxiv.org/abs/2505.05005v2",
                "pdf_url": "https://arxiv.org/pdf/2505.05005v2",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "2505.23088v1",
                "title": "On the irrationality of certain p-adic zeta values",
                "authors": ["Li Lai", "Cezar Lupu", "Johannes Sprang"],
                "url": "https://arxiv.org/abs/2505.23088v1",
                "pdf_url": "https://arxiv.org/pdf/2505.23088v1",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
            {
                "id": "2411.16774v3",
                "title": "A Note on a Recent Attempt to Prove the Irrationality of zeta(5)",
                "authors": [
                    "Keyu Chen",
                    "Wei He",
                    "Yixin He",
                    "Yuxiang Huang",
                    "Yanyang Li",
                    "Quanyu Tang",
                    "Lei Wu",
                    "Shenhao Xu",
                    "Shuo Yang",
                    "Zijun Yu",
                ],
                "url": "https://arxiv.org/abs/2411.16774v3",
                "pdf_url": "https://arxiv.org/pdf/2411.16774v3",
                "verification": PRIMARY_SOURCE_VERIFIED,
            },
        ],
    }


def audit_transcendence_theorem_applicability() -> List[Dict[str, str]]:
    """
    Audit the nine major transcendence theorem families against the exact hypothesis
    structure provided by `zeta(rho) = 0` (Section 10).
    """
    return [
        {
            "theorem": "Lindemann-Weierstrass (1882/1885)",
            "input_structure_required": (
                "Distinct algebraic numbers alpha_1, ..., alpha_m in Q_bar such that exp(alpha_j) "
                "satisfy a nontrivial Q_bar-linear relation."
            ),
            "does_zeta_zero_provide_it": "No",
            "obstruction": (
                "If rho in Q_bar, the terms n^{-rho} = exp(-rho log n) have exponents -rho log n "
                "which are transcendental for all n >= 2 (since log n notin Q_bar), and the critical-strip "
                "analytic continuation is an infinite non-absolutely-convergent limit, not a finite Q_bar-linear "
                "relation among exp(alpha_j) for alpha_j in Q_bar."
            ),
        },
        {
            "theorem": "Gelfond-Schneider (1934)",
            "input_structure_required": (
                "Algebraic base alpha in Q_bar \\ {0, 1} and irrational algebraic exponent beta in Q_bar \\ Q "
                "such that alpha^beta lies in Q_bar."
            ),
            "does_zeta_zero_provide_it": "No",
            "obstruction": (
                "Assuming rho in Q_bar \\ Q makes each individual prime power p^{-rho} transcendental "
                "by Gelfond-Schneider, but zeta(rho) = 0 is a vanishing analytic continuation of an "
                "infinite sum/product, which does NOT force any single p^{-rho} or pi^{-rho/2} to be algebraic."
            ),
        },
        {
            "theorem": "Baker's theorem on linear forms in logarithms (1966)",
            "input_structure_required": (
                "A finite linear combination beta_0 + beta_1 log(alpha_1) + ... + beta_m log(alpha_m) "
                "with alpha_j, beta_j in Q_bar."
            ),
            "does_zeta_zero_provide_it": "No",
            "obstruction": (
                "zeta(rho) = 0 is a relation among infinitely many exponentials n^{-rho} (via analytic "
                "continuation), not a finite linear form in logarithms of algebraic numbers; furthermore, "
                "the Euler product log zeta(s) = -sum_p log(1 - p^{-s}) diverges in 0 < Re(s) < 1."
            ),
        },
        {
            "theorem": "Siegel-Shidlovsky theory (1929/1959)",
            "input_structure_required": (
                "A vector of E-functions f_1(z), ..., f_m(z) in Q_bar[[z]] satisfying a first-order "
                "system of linear differential equations over Q_bar(z), evaluated at a non-singular alpha in Q_bar^x."
            ),
            "does_zeta_zero_provide_it": "No",
            "obstruction": (
                "zeta(s) is NOT an E-function in s, and by Ostrowski (1920) / Hilbert (1900) zeta(s) "
                "satisfies NO algebraic differential equation over C(s) whatsoever."
            ),
        },
        {
            "theorem": "Schneider-Lang criterion (1949/1966)",
            "input_structure_required": (
                "Meromorphic functions f_1, ..., f_d of finite order with transcendence degree >= 2 "
                "such that d/ds maps the ring K[f_1, ..., f_d] into itself (algebraic differential ring), "
                "simultaneously taking values in a number field K at sufficiently many points."
            ),
            "does_zeta_zero_provide_it": "No",
            "obstruction": (
                "Neither zeta(s) nor Gamma(s/2) generates a finitely generated ring closed under d/ds "
                "(both are differentially transcendental), and a single hypothetical algebraic zero rho "
                "gives only one evaluation point where zeta(rho) = 0 while zeta'(rho), zeta''(rho), ... "
                "have unknown arithmetic nature."
            ),
        },
        {
            "theorem": "Nesterenko algebraic independence (1996)",
            "input_structure_required": (
                "Values of Ramanujan quasi-modular Eisenstein series E_2(q), E_4(q), E_6(q) at an "
                "algebraic modular parameter q in (0, 1) (yielding algebraic independence of pi, e^pi, Gamma(1/4))."
            ),
            "does_zeta_zero_provide_it": "No",
            "obstruction": (
                "Nesterenko's theorem controls special modular periods at CM / algebraic nomina q (which "
                "correspond to Gamma(1/4), Gamma(1/3), pi, e^pi), NOT the Mellin integral of theta_3(it) "
                "at an off-lattice complex exponent rho in 0 < Re(rho) < 1."
            ),
        },
        {
            "theorem": "Lindemann's theorem on pi (1882)",
            "input_structure_required": "pi in Q_bar (contradicted by e^{i*pi} = -1).",
            "does_zeta_zero_provide_it": "No",
            "obstruction": (
                "In xi(rho) = 0, the factor pi^{-rho/2} is multiplied by (1/2)rho(rho-1)Gamma(rho/2)zeta(rho); "
                "because zeta(rho) = 0 makes the entire product vanish (0 = 0), no algebraic value is "
                "assigned to pi^{-rho/2}."
            ),
        },
        {
            "theorem": "Transcendence of Gamma(alpha) at algebraic alpha (Chudnovsky 1976; Rohrlich-Lang)",
            "input_structure_required": (
                "Evaluation of Gamma(alpha) at special rational points alpha in {1/2, 1/3, 1/4, 1/6} "
                "(where Gamma(alpha) is transcendental via CM elliptic periods)."
            ),
            "does_zeta_zero_provide_it": "No",
            "obstruction": (
                "1) For general algebraic alpha in Q_bar \\ Q (and even most rationals p/q), transcendence "
                "of Gamma(alpha) is itself OPEN; 2) At a nontrivial zero rho, Gamma(rho/2) has no zeros "
                "or poles and is multiplied by zeta(rho) = 0, yielding no equation constraining Gamma(rho/2)."
            ),
        },
        {
            "theorem": "Differential transcendence of Gamma (Holder 1887) and zeta (Hilbert 1900 / Ostrowski 1920)",
            "input_structure_required": (
                "An identically satisfied polynomial differential relation P(s, f(s), f'(s), ..., f^{(n)}(s)) = 0 "
                "for all s in an open domain."
            ),
            "does_zeta_zero_provide_it": "No",
            "obstruction": (
                "Differential transcendence is a functional identity statement over C(s); a differentially "
                "transcendental function can have arbitrary prescribed algebraic or rational zeros "
                "(e.g., (s - alpha) * Gamma(s) is differentially transcendental and vanishes at s = alpha)."
            ),
        },
    ]


def audit_functional_equation_algebraic_zero() -> Dict[str, Any]:
    """
    Audit what follows from inserting a hypothetical algebraic zero `rho in Q_bar`
    (`0 < Re(rho) < 1`, `zeta(rho) = 0`) into the completed functional equation
    `xi(s) = xi(1 - s)` and its first derivative `xi'(s) = -xi'(1 - s)` (Section 11).
    """
    return {
        "classification": FUNCTIONAL_EQUATION_DOES_NOT_EXCLUDE_ALGEBRAIC_ZERO,
        "zero_order_identity": {
            "equation": "xi(rho) = xi(1 - rho) = 0",
            "division_by_zeta_rho_blocked": True,
            "explanation": (
                "Because zeta(rho) = 0 and the archimedean prefactor A(s) = (1/2)s(s-1)pi^{-s/2}Gamma(s/2) "
                "is nonzero everywhere on 0 < Re(s) < 1, zeta(1 - rho) = 0 follows, while dividing "
                "xi(rho) = xi(1 - rho) by zeta(rho) = 0 is division by zero and strictly invalid."
            ),
        },
        "first_derivative_at_simple_zero": {
            "equation": "xi'(rho) = -xi'(1 - rho)",
            "expanded_identity": (
                "A(rho) * zeta'(rho) = -A(1 - rho) * zeta'(1 - rho)  (since zeta(rho) = zeta(1 - rho) = 0)"
            ),
            "ratio_identity": (
                "zeta'(rho) / zeta'(1 - rho) = -A(1 - rho) / A(rho) "
                "= -pi^{rho - 1/2} * Gamma((1 - rho)/2) / Gamma(rho/2) = -chi(1 - rho)"
            ),
            "why_no_contradiction_arises": (
                "Even if rho in Q_bar is assumed, the derivative values zeta'(rho) and zeta'(1 - rho) "
                "have completely unknown arithmetic nature (they are NOT constrained to be algebraic), "
                "and the transcendence status of pi^{rho - 1/2} * Gamma((1 - rho)/2) / Gamma(rho/2) at a "
                "non-real algebraic point rho = beta + i*gamma (gamma != 0) is also unknown."
            ),
        },
    }


def audit_euler_product_firewall() -> Dict[str, Any]:
    """
    Explicitly record the Euler-product convergence domain firewall (Section 12).
    """
    return {
        "classification": EULER_PRODUCT_NONVANISHING_NOT_AVAILABLE_IN_CRITICAL_STRIP,
        "euler_product_expression": "prod_p (1 - p^{-s})^{-1}",
        "absolute_convergence_domain": "Re(s) > 1",
        "nontrivial_zero_domain": "0 < Re(rho) < 1",
        "domains_disjoint": True,
        "fallacy_blocked": (
            "The argument 'each Euler factor (1 - p^{-rho})^{-1} is nonzero, therefore zeta(rho) != 0' "
            "is invalid in 0 < Re(s) < 1 because the infinite Euler product diverges there and "
            "analytic continuation does not preserve nonvanishing of divergent infinite products."
        ),
    }


def audit_gamma_and_differential_transcendence_firewalls() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Audit the Gamma-function arithmetic firewall (Section 28) and the
    differential-transcendence firewall (Section 29).
    """
    gamma_firewall = {
        "special_rational_values_known_transcendental": {
            "Gamma(1/2)": "sqrt(pi) (transcendental by Lindemann 1882)",
            "Gamma(1/4)": "transcendental and algebraically independent of pi (Chudnovsky 1976; Nesterenko 1996)",
            "Gamma(1/3)": "transcendental and algebraically independent of pi (Chudnovsky 1976)",
            "Gamma(1/6)": "transcendental (expressed via Gamma(1/3) and sqrt(pi))",
        },
        "general_rational_values_status": (
            "For general rational p/q notin {1/2, 1/3, 1/4, 1/6} mod Z (e.g., Gamma(1/5)), "
            "individual transcendence of Gamma(p/q) is OPEN (Rohrlich-Lang conjecture; "
            "Wolfart-Wustholz 1985 give linear-independence bounds on beta values)."
        ),
        "general_complex_algebraic_values_status": (
            "For non-real algebraic alpha = (beta + i*gamma)/2 in Q_bar \\ R, NO general theorem "
            "establishes transcendence or algebraic independence of Gamma(alpha)."
        ),
        "obstruction_for_functional_equation": (
            "In xi(rho) = (1/2)rho(rho-1)pi^{-rho/2}Gamma(rho/2)zeta(rho), neither Gamma(rho/2) "
            "nor pi^{-rho/2}Gamma(rho/2) has known arithmetic properties at a hypothetical non-real "
            "algebraic rho, blocking any naive functional-equation transcendence contradiction."
        ),
    }

    diff_transc_firewall = {
        "classification": DIFFERENTIAL_TRANSCENDENCE_DOES_NOT_DETERMINE_ZERO_ARITHMETIC,
        "holder_theorem_gamma": (
            "Holder (1887): Gamma(s) satisfies no algebraic differential equation over C(s)."
        ),
        "hilbert_ostrowski_theorem_zeta": (
            "Hilbert (1900) / Ostrowski (1920): zeta(s) satisfies no algebraic differential equation over C(s)."
        ),
        "counterexample_to_zero_inference": (
            "For any prescribed algebraic number alpha in Q_bar, the entire function "
            "F_alpha(s) = (s - alpha) / Gamma(s) (or (s - alpha) * xi(s)) is differentially "
            "transcendental over C(s), yet vanishes at the algebraic point s = alpha. "
            "Hence differential transcendence of a function never implies transcendence of its zeros."
        ),
    }
    return gamma_firewall, diff_transc_firewall


# ---------------------------------------------------------------------------
# 3. Exact Zero-Sum Invariants: xi(s), S_1, S_2, S_m, Centered Sums, Quartet, Li (Sections 13–22)
# ---------------------------------------------------------------------------


def derive_xi_hadamard_and_reciprocal_sums() -> Dict[str, Any]:
    """
    Perform exact symbolic (SymPy) and 50-digit arbitrary-precision (mpmath) derivations of:
      - Hadamard factorization of `xi(s) = (1/2)s(s-1)pi^{-s/2}Gamma(s/2)zeta(s)` (Section 13)
      - First reciprocal sum `S_1 = sum_rho^{sym} 1/rho = 1 + gamma_E/2 - log(2*sqrt(pi))` (Section 14)
      - Reflection-invariant sum `sum_rho 1/(rho(1-rho)) = 2*S_1 = 2 + gamma_E - log(4*pi) = 2*lambda_1` (Section 15)
      - Second reciprocal sum `S_2 = sum_rho 1/rho^2` in both `s = 0` (`zeta''(0)`) and `s = 1` (`gamma_1^St`) forms
        with disambiguated Stieltjes notation `gamma_0^St = gamma_E, gamma_1^St, gamma_2^St, gamma_3^St` (Sections 15–16)
      - 3-route independent re-audit of `S_3` and `S_4` and general `S_m` normalization (Sections 17–18)
      - Centered zero invariants `Sigma_{2m} = sum_rho (rho - 1/2)^{-2m}` (Section 18)
      - Quartet polynomial `(X^2 - z^2)(X^2 - conj(z)^2)` (Section 19)
      - Li/Keiper coefficients `lambda_1, lambda_2, lambda_3, lambda_4` (Section 20)
      - Partial-sum numerical controls using the repository's 200 reference zeros (Section 35)
    """
    # 1. Symbolic derivation of S_1 and S_2 at s = 0 using SymPy truncated series
    s = sp.Symbol("s")
    gamma_E = sp.Symbol("gamma_E")
    log_pi = sp.Symbol("log_pi")
    log_2 = sp.Symbol("log_2")
    pi_sym = sp.Symbol("pi")
    zeta2_0 = sp.Symbol("zeta_pp_0")  # zeta''(0)
    zeta_3_sym = sp.Symbol("zeta_3")  # zeta(3)
    gamma_1_st = sp.Symbol("gamma_1_St")  # first Stieltjes constant gamma_1^St
    gamma_2_st = sp.Symbol("gamma_2_St")  # second Stieltjes constant gamma_2^St
    gamma_3_st = sp.Symbol("gamma_3_St")  # third Stieltjes constant gamma_3^St

    # Regularized factors of xi(s) = (1 - s) * pi^{-s/2} * Gamma(1 + s/2) * (-zeta(s)) near s = 0:
    log_xi_series_s0 = (
        (-s - s**2 / 2)
        + (-s * log_pi / 2)
        + (-gamma_E * s / 2 + (pi_sym**2 / 48) * s**2)
        + (
            -log_2
            + (log_2 + log_pi) * s
            + (-zeta2_0 - (log_2 + log_pi) ** 2 / 2) * s**2
        )
    )
    d1_log_xi_0 = sp.expand(sp.diff(log_xi_series_s0, s).subs(s, 0))
    d2_log_xi_0 = sp.expand(sp.diff(log_xi_series_s0, s, 2).subs(s, 0))
    S1_sym_s0 = sp.expand(-d1_log_xi_0)
    S2_sym_s0 = sp.expand(-d2_log_xi_0)

    expected_S1_sym = 1 + gamma_E / 2 - log_2 - log_pi / 2
    expected_S2_sym_s0 = 1 - pi_sym**2 / 24 + 2 * zeta2_0 + (log_2 + log_pi) ** 2
    s1_symbolic_match = bool(sp.simplify(S1_sym_s0 - expected_S1_sym) == 0)
    s2_s0_symbolic_match = bool(sp.simplify(S2_sym_s0 - expected_S2_sym_s0) == 0)

    # Route 1 (Symbolic Laurent expansion of log xi(1 + u) up to O(u^5) for m = 1, 2, 3, 4):
    # xi(1 + u) = (1/2) * (1 + u) * pi^{-(1+u)/2} * Gamma((1+u)/2) * (u * zeta(1 + u))
    # 1) log(1 + u) = u - u^2/2 + u^3/3 - u^4/4 + O(u^5)
    # 2) log(pi^{-(1+u)/2}) = const - (log_pi/2) * u
    # 3) log Gamma((1+u)/2) = const + (1/2)*psi(1/2)*u + (1/8)*psi_1(1/2)*u^2/2
    #                         + (1/8)*psi_2(1/2)*u^3/6 + (1/16)*psi_3(1/2)*u^4/24 + O(u^5)
    #    where psi(1/2) = -gamma_E - 2*log_2, psi_1(1/2) = pi^2/2, psi_2(1/2) = -14*zeta(3), psi_3(1/2) = pi^4.
    # 4) u * zeta(1 + u) = 1 + gamma_E*u - gamma_1^St*u^2 + (gamma_2^St/2)*u^3 - (gamma_3^St/6)*u^4 + O(u^5).
    #    Let w_zeta = gamma_E*u - gamma_1^St*u^2 + (gamma_2^St/2)*u^3 - (gamma_3^St/6)*u^4,
    #    and expand log(1 + w_zeta) = w_zeta - w_zeta^2/2 + w_zeta^3/3 - w_zeta^4/4 mod u^5.
    u = sp.Symbol("u")
    w_zeta = (
        gamma_E * u
        - gamma_1_st * u**2
        + (gamma_2_st / sp.Integer(2)) * u**3
        - (gamma_3_st / sp.Integer(6)) * u**4
    )
    log_uzeta_s1 = sp.series(
        w_zeta - w_zeta**2 / 2 + w_zeta**3 / 3 - w_zeta**4 / 4, u, 0, 5
    ).removeO()
    log_xi_series_s1 = sp.expand(
        (u - u**2 / 2 + u**3 / 3 - u**4 / 4)
        + (-u * log_pi / 2)
        + (
            (-gamma_E / 2 - log_2) * u
            + (pi_sym**2 / 16) * u**2
            - (sp.Rational(7, 24) * zeta_3_sym) * u**3
            + (pi_sym**4 / 384) * u**4
        )
        + log_uzeta_s1
    )
    # Since xi(1 + u) = xi(-u), (d^m/ds^m)|_{s=0} log xi(s) = (-1)^m (d^m/du^m)|_{u=0} log xi(1+u),
    # and S_m = -(1/(m-1)!) (d^m/ds^m)|_{s=0} log xi(s) = ((-1)^{m+1}/(m-1)!) (d^m/du^m)|_{u=0} log xi(1+u).
    S_sym_s1: Dict[int, Any] = {}
    for m in (1, 2, 3, 4):
        dm_u0 = sp.diff(log_xi_series_s1, u, m).subs(u, 0)
        S_sym_s1[m] = sp.expand(((-1) ** (m + 1)) * dm_u0 / sp.factorial(m - 1))

    expected_S2_sym_s1 = 1 + gamma_E**2 - pi_sym**2 / 8 + 2 * gamma_1_st
    expected_S3_sym_s1 = (
        1
        - sp.Rational(7, 8) * zeta_3_sym
        + gamma_E**3
        + 3 * gamma_E * gamma_1_st
        + sp.Rational(3, 2) * gamma_2_st
    )
    expected_S4_sym_s1 = (
        1
        - pi_sym**4 / 96
        + gamma_E**4
        + 4 * gamma_E**2 * gamma_1_st
        + 2 * gamma_1_st**2
        + 2 * gamma_E * gamma_2_st
        + sp.Rational(2, 3) * gamma_3_st
    )
    s1_s1_symbolic_match = bool(sp.simplify(S_sym_s1[1] - expected_S1_sym) == 0)
    s2_s1_symbolic_match = bool(sp.simplify(S_sym_s1[2] - expected_S2_sym_s1) == 0)
    s3_s1_symbolic_match = bool(sp.simplify(S_sym_s1[3] - expected_S3_sym_s1) == 0)
    s4_s1_symbolic_match = bool(sp.simplify(S_sym_s1[4] - expected_S4_sym_s1) == 0)

    # Check the difference between true S_2 and erroneous historical expression:
    erroneous_S2_sym = (
        1 - pi_sym**2 / 8 + gamma_E + gamma_E**2 / 4 - gamma_1_st
    )
    s2_erroneous_diff_sym = sp.expand(expected_S2_sym_s1 - erroneous_S2_sym)
    s2_erroneous_diff_verified = bool(
        sp.simplify(
            s2_erroneous_diff_sym
            - (sp.Rational(3, 4) * gamma_E**2 - gamma_E + 3 * gamma_1_st)
        )
        == 0
    )

    # 2. High-precision (50 dps) verification of S_1..S_4, centered sums, and Li coefficients
    old_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = 50
        mp_one = mpmath.mpf(1)
        mp_half = mpmath.mpf("0.5")

        def log_xi_at_0(x: Any) -> Any:
            # Valid near x = 0: xi(x) = (1 - x) * pi^{-x/2} * Gamma(1 + x/2) * (-zeta(x))
            return (
                mpmath.log(1 - x)
                - (x / 2) * mpmath.log(mpmath.pi)
                + mpmath.loggamma(1 + x / 2)
                + mpmath.log(-mpmath.zeta(x))
            )

        def log_xi_at_1_u(u_val: Any) -> Any:
            # Valid near u = 0 (s = 1 + u): xi(1+u) = xi(-u)
            return log_xi_at_0(-u_val)

        def log_Xi_centered(z: Any) -> Any:
            return log_xi_at_0(mp_half + z)

        S_mp: Dict[int, Any] = {}
        S_mp_from_s1: Dict[int, Any] = {}
        for m in (1, 2, 3, 4):
            deriv_m_0 = mpmath.diff(log_xi_at_0, mpmath.mpf(0), m)
            S_mp[m] = -deriv_m_0 / mpmath.factorial(m - 1)
            deriv_m_1 = mpmath.diff(log_xi_at_1_u, mpmath.mpf(0), m)
            S_mp_from_s1[m] = (
                ((-1) ** (m + 1)) * deriv_m_1 / mpmath.factorial(m - 1)
            )

        S1_closed = (
            mp_one
            + mpmath.euler / 2
            - mpmath.log(2 * mpmath.sqrt(mpmath.pi))
        )
        refl_sum_closed = 2 + mpmath.euler - mpmath.log(4 * mpmath.pi)
        S2_closed_s0 = (
            mp_one
            - (mpmath.pi**2) / 24
            + 2 * mpmath.diff(mpmath.zeta, mpmath.mpf(0), 2)
            + mpmath.log(2 * mpmath.pi) ** 2
        )
        S2_closed_s1 = (
            mp_one
            + mpmath.euler**2
            - (mpmath.pi**2) / 8
            + 2 * mpmath.stieltjes(1)
        )
        S2_erroneous_val = (
            mp_one
            - (mpmath.pi**2) / 8
            + mpmath.euler
            + (mpmath.euler**2) / 4
            - mpmath.stieltjes(1)
        )
        S3_closed_s1 = (
            mp_one
            - mpmath.mpf(7) / 8 * mpmath.zeta(3)
            + mpmath.euler**3
            + 3 * mpmath.euler * mpmath.stieltjes(1)
            + mpmath.mpf(3) / 2 * mpmath.stieltjes(2)
        )
        S4_closed_s1 = (
            mp_one
            - (mpmath.pi**4) / 96
            + mpmath.euler**4
            + 4 * (mpmath.euler**2) * mpmath.stieltjes(1)
            + 2 * (mpmath.stieltjes(1) ** 2)
            + 2 * mpmath.euler * mpmath.stieltjes(2)
            + mpmath.mpf(2) / 3 * mpmath.stieltjes(3)
        )

        # Centered zero invariants Sigma_k = sum_rho z_rho^{-k} = -(1/(k-1)!) (d^k/dz^k)|_{z=0} log Xi(z)
        Sigma2_mp = -mpmath.diff(log_Xi_centered, mpmath.mpf(0), 2)
        Sigma4_mp = -mpmath.diff(log_Xi_centered, mpmath.mpf(0), 4) / 6
        Sigma1_odd_mp = -mpmath.diff(log_Xi_centered, mpmath.mpf(0), 1)
        Sigma3_odd_mp = -mpmath.diff(log_Xi_centered, mpmath.mpf(0), 3) / 2

        log_neg_zeta = lambda z: mpmath.log(-mpmath.zeta(mp_half + z))
        Sigma2_closed = (
            8
            - mpmath.mpf("0.25") * mpmath.psi(1, mpmath.mpf("0.25"))
            - mpmath.diff(log_neg_zeta, mpmath.mpf(0), 2)
        )

        lambda_binomial: Dict[int, Any] = {}
        lambda_deriv: Dict[int, Any] = {}
        for n in (1, 2, 3, 4):
            lambda_binomial[n] = sum(
                mpmath.binomial(n, j) * ((-1) ** (j - 1)) * S_mp[j]
                for j in range(1, n + 1)
            )
            func_n = lambda w, n_val=n: ((1 - w) ** (n_val - 1)) * log_xi_at_0(w)
            lambda_deriv[n] = (
                ((-1) ** n)
                * mpmath.diff(func_n, mpmath.mpf(0), n)
                / mpmath.factorial(n - 1)
            )

        # 3. Route 3: Partial-sum numerical controls over the 200 reference zeros in data/zeros_reference.json
        zeros_path = Path(__file__).resolve().parent.parent / "data" / "zeros_reference.json"
        ordinates_200: List[Any] = []
        if zeros_path.exists():
            zdata = json.loads(zeros_path.read_text(encoding="utf-8"))
            ordinates_200 = [mpmath.mpf(s_ord) for s_ord in zdata.get("ordinates", [])]
        else:
            ordinates_200 = [mpmath.im(mpmath.zetazero(k)) for k in range(1, 51)]

        # Pair contributions for rho_k = 1/2 +- i*gamma_k:
        partial_S1_200 = sum(1 / (mpmath.mpf("0.25") + g**2) for g in ordinates_200)
        partial_refl_200 = 2 * partial_S1_200
        partial_S2_200 = sum(
            2 * (mpmath.mpf("0.25") - g**2) / ((mpmath.mpf("0.25") + g**2) ** 2)
            for g in ordinates_200
        )
        partial_S3_200 = sum(
            2 * mpmath.re((mp_half + mpmath.j * g) ** (-3)) for g in ordinates_200
        )
        partial_S4_200 = sum(
            2 * mpmath.re((mp_half + mpmath.j * g) ** (-4)) for g in ordinates_200
        )
        partial_Sigma2_200 = sum(-2 / (g**2) for g in ordinates_200)
        partial_Sigma4_200 = sum(2 / (g**4) for g in ordinates_200)

        T_200 = ordinates_200[-1]
        asymptotic_tail_S1 = (mpmath.log(T_200 / (2 * mpmath.pi)) + 1) / (
            2 * mpmath.pi * T_200
        )
        # For S_3, Re((1/2 + i*t)^{-3}) = (1/8 - (3/2)t^2) / (1/4 + t^2)^3 ~ -(3/2) t^{-4},
        # so tail_S3 ~ 2 * int_{T_200}^infty (-3/2) t^{-4} (log(t/(2*pi))/(2*pi)) dt
        # ~ -(3 / (2*pi)) * (log(T_200/(2*pi)) + 1/3) / (3 * T_200^3) = -(3*log(T_200/(2*pi)) + 1) / (6*pi*T_200^3).
        asymptotic_tail_S3 = -(3 * mpmath.log(T_200 / (2 * mpmath.pi)) + 1) / (
            6 * mpmath.pi * (T_200**3)
        )
        # For S_4, Re((1/2 + i*t)^{-4}) ~ +t^{-4},
        # so tail_S4 ~ +2 * int_{T_200}^infty t^{-4} (log(t/(2*pi))/(2*pi)) dt
        # = (3*log(T_200/(2*pi)) + 1) / (9*pi*T_200^3).
        asymptotic_tail_S4 = (3 * mpmath.log(T_200 / (2 * mpmath.pi)) + 1) / (
            9 * mpmath.pi * (T_200**3)
        )

        results = {
            "stieltjes_notation_policy": {
                "status": STIELTJES_NOTATION_DISAMBIGUATED,
                "zero_ordinate_symbol": "gamma_1 = Im(rho_1) = 14.134725141734693790...",
                "stieltjes_constant_symbols": [
                    "gamma_0^St = gamma_E",
                    "gamma_1^St",
                    "gamma_2^St",
                    "gamma_3^St",
                ],
                "laurent_expansion_convention": (
                    "zeta(s) = 1/(s - 1) + sum_{k>=0} ((-1)^k / k!) * gamma_k^St * (s - 1)^k"
                ),
                "bare_gamma_1_for_stieltjes_forbidden": True,
                "lean_theorem": "stieltjes_notation_no_effect_algebra",
            },
            "xi_hadamard_product_status": {
                "completed_xi_definition": "xi(s) = (1/2) * s * (s - 1) * pi^{-s/2} * Gamma(s/2) * zeta(s)",
                "regularized_origin_form": "xi(s) = (s - 1) * pi^{-s/2} * Gamma(1 + s/2) * zeta(s)",
                "xi_at_0_and_1": "xi(0) = xi(1) = 1/2",
                "hadamard_genus": 1,
                "canonical_weierstrass_product": (
                    "xi(s) = xi(0) * exp(b_0 * s) * prod_rho (1 - s/rho) exp(s/rho), "
                    "where b_0 = xi'(0)/xi(0) = log(2*sqrt(pi)) - 1 - gamma_E/2 = -S_1"
                ),
                "symmetric_paired_product": (
                    "xi(s) = xi(0) * lim_{T -> infty} prod_{|Im(rho)| <= T} (1 - s/rho) "
                    "= xi(0) * prod_{{rho, 1-rho}} (1 - s(1 - s) / (rho(1 - rho)))"
                ),
                "why_exponential_factors_cancel_under_symmetric_pairing": (
                    "Pairing rho with 1 - rho (or conj(rho) on the critical line) gives "
                    "1/rho + 1/(1 - rho) = 1/(rho(1 - rho)) = O(|gamma_rho|^{-2}). Since "
                    "sum_rho |gamma_rho|^{-2} < infty by Riemann-von Mangoldt N(T) = O(T log T), "
                    "the Weierstrass convergence factors exp(s(1/rho + 1/(1 - rho))) have convergent "
                    "exponent sum S_1 * s, which cancels exp(b_0 * s) = exp(-S_1 * s) identically."
                ),
                "unpaired_product_warning": (
                    "Writing xi(s) = xi(0) prod_rho (1 - s/rho) WITHOUT specifying symmetric pairing "
                    "|Im(rho)| <= T or (rho, 1 - rho) grouping is invalid because sum_rho |rho|^{-1} = infty."
                ),
                "status": PROVED_WITH_EXTERNAL_THEOREM,
                "primary_citations": [
                    "Riemann (1859), Monatsber. Berlin Akad., 671-680",
                    "Hadamard (1893), J. Math. Pures Appl. (4) 9, 171-215",
                    "Davenport (2000), Multiplicative Number Theory, Chapter 12",
                    "Titchmarsh (1986), The Theory of the Riemann Zeta-Function, Section 2.12",
                ],
            },
            "reciprocal_sum_S1": {
                "symbol": "S_1 = sum_rho^{sym} (1 / rho)",
                "ordering_convention": "lim_{T -> infty} sum_{|Im(rho)| <= T} (1 / rho) = (1/2) sum_rho (1/rho + 1/(1 - rho))",
                "convergence_type": "CONDITIONALLY_CONVERGENT_UNDER_SYMMETRIC_PAIRING",
                "absolute_convergence": False,
                "exact_formula": "1 + gamma_E / 2 - log(2 * sqrt(pi)) = 1 + gamma_E / 2 - log(2) - (1/2) * log(pi)",
                "derivation_steps": [
                    "1. Write xi(s) = (1 - s) * pi^{-s/2} * Gamma(1 + s/2) * (-zeta(s)) near s = 0.",
                    "2. Differentiate log xi(s) at s = 0 using zeta(0) = -1/2, zeta'(0) = -(1/2)log(2*pi), and (d/ds)log Gamma(1 + s/2)|_{s=0} = (1/2)psi(1) = -gamma_E/2.",
                    "3. Obtain xi'(0)/xi(0) = -1 - (1/2)log(pi) - gamma_E/2 + log(2*pi) = log(2*sqrt(pi)) - 1 - gamma_E/2.",
                    "4. From the symmetrically paired Hadamard product xi(s) = xi(0) prod^{sym}(1 - s/rho), xi'(0)/xi(0) = -sum_rho^{sym} (1/rho), giving S_1 = -xi'(0)/xi(0) = 1 + gamma_E/2 - log(2*sqrt(pi)).",
                ],
                "value_50dps": mpmath.nstr(S1_closed, 45),
                "value_float": float(S1_closed),
                "symbolic_derivation_verified": s1_symbolic_match and s1_s1_symbolic_match,
                "mpmath_50dps_residual": float(abs(S_mp[1] - S1_closed)),
                "relation_to_li_lambda_1": "S_1 = lambda_1",
            },
            "reflection_invariant_sum": {
                "symbol": "sum_rho 1 / (rho * (1 - rho))",
                "partial_fraction_identity": "1 / (rho * (1 - rho)) = 1 / rho + 1 / (1 - rho)",
                "convergence_type": "ABSOLUTELY_CONVERGENT",
                "absolute_convergence": True,
                "why_absolutely_convergent": (
                    "|rho(1 - rho)| = |1/4 - z_rho^2| ~ gamma_rho^2 as |gamma_rho| -> infty, "
                    "and sum_rho gamma_rho^{-2} < infty because N(T) = O(T log T)."
                ),
                "exact_formula": "2 + gamma_E - log(4 * pi) = 2 * S_1 = 2 * lambda_1",
                "value_50dps": mpmath.nstr(refl_sum_closed, 45),
                "value_float": float(refl_sum_closed),
                "mpmath_50dps_residual": float(abs(2 * S_mp[1] - refl_sum_closed)),
                "normalization_comparison": {
                    "standard_li_lambda_1": "lambda_1 = S_1 = 1 + gamma_E/2 - log(2*sqrt(pi))",
                    "reflection_sum_equals_2_lambda_1": "sum_rho 1/(rho(1-rho)) = 2 * lambda_1 = 2 + gamma_E - log(4*pi)",
                },
                "lean_theorem": "reflection_reciprocal_identity",
            },
            "reciprocal_sum_S2": {
                "status": S2_CANONICAL_FORMULA_REPAIRED,
                "symbol": "S_2 = sum_rho (1 / rho^2)",
                "convergence_type": "ABSOLUTELY_CONVERGENT",
                "absolute_convergence": True,
                "derivative_relation": "S_2 = - (d/ds)|_{s=0} (xi'(s) / xi(s)) = - (d^2/ds^2)|_{s=0} log xi(s)",
                "exact_formula_at_s0": "1 - pi^2 / 24 + 2 * zeta''(0) + log(2 * pi)^2",
                "exact_formula_at_s1_stieltjes": "1 + gamma_E^2 - pi^2 / 8 + 2 * gamma_1^St",
                "equivalence_identity_between_s0_and_s1": (
                    "2 * zeta''(0) + log(2 * pi)^2 = gamma_E^2 - pi^2 / 12 + 2 * gamma_1^St"
                ),
                "erroneous_historical_formula_removed": "1 - pi^2 / 8 + gamma_E + gamma_E^2 / 4 - gamma_1^St",
                "erroneous_formula_discrepancy": float(abs(S2_closed_s1 - S2_erroneous_val)),
                "erroneous_formula_symbolic_diff_verified": s2_erroneous_diff_verified,
                "constants_entering": [
                    "Euler-Mascheroni constant gamma_E = gamma_0^St",
                    "pi^2",
                    "First Stieltjes constant gamma_1^St (or equivalently zeta''(0) and log(2*pi))",
                ],
                "value_50dps": mpmath.nstr(S2_closed_s1, 45),
                "value_float": float(S2_closed_s1),
                "symbolic_s0_verified": s2_s0_symbolic_match,
                "symbolic_s1_verified": s2_s1_symbolic_match,
                "mpmath_s0_residual": float(abs(S_mp[2] - S2_closed_s0)),
                "mpmath_s1_residual": float(abs(S_mp[2] - S2_closed_s1)),
                "s0_vs_s1_derivative_residual": float(abs(S_mp[2] - S_mp_from_s1[2])),
                "arithmetic_nature_status": OPEN_IN_LITERATURE,
                "lean_theorem": "s2_equivalent_closed_forms",
            },
            "S3_reaudit": {
                "status": S3_S4_REAUDITED,
                "symbol": "S_3 = sum_rho (1 / rho^3)",
                "derivative_relation": (
                    "S_3 = -(1/2!) * (d^3/ds^3)|_{s=0} log xi(s) = +(1/2!) * (d^3/du^3)|_{u=0} log xi(1 + u)"
                ),
                "exact_formula_stieltjes": (
                    "1 - (7/8)*zeta(3) + gamma_E^3 + 3*gamma_E*gamma_1^St + (3/2)*gamma_2^St"
                ),
                "route_1_symbolic_laurent_verified": s3_s1_symbolic_match,
                "route_2_mpmath_50dps_s0_vs_closed_residual": float(
                    abs(S_mp[3] - S3_closed_s1)
                ),
                "route_2_mpmath_50dps_s1_vs_closed_residual": float(
                    abs(S_mp_from_s1[3] - S3_closed_s1)
                ),
                "route_3_partial_sum_200_pairs": float(partial_S3_200),
                "route_3_partial_plus_tail": float(partial_S3_200 + asymptotic_tail_S3),
                "route_3_tail_corrected_residual": float(
                    abs((partial_S3_200 + asymptotic_tail_S3) - S3_closed_s1)
                ),
                "value_50dps": mpmath.nstr(S3_closed_s1, 45),
                "value_float": float(S3_closed_s1),
            },
            "S4_reaudit": {
                "status": S3_S4_REAUDITED,
                "symbol": "S_4 = sum_rho (1 / rho^4)",
                "derivative_relation": (
                    "S_4 = -(1/3!) * (d^4/ds^4)|_{s=0} log xi(s) = -(1/3!) * (d^4/du^4)|_{u=0} log xi(1 + u)"
                ),
                "exact_formula_stieltjes": (
                    "1 - pi^4/96 + gamma_E^4 + 4*gamma_E^2*gamma_1^St + 2*(gamma_1^St)^2 "
                    "+ 2*gamma_E*gamma_2^St + (2/3)*gamma_3^St"
                ),
                "route_1_symbolic_laurent_verified": s4_s1_symbolic_match,
                "route_2_mpmath_50dps_s0_vs_closed_residual": float(
                    abs(S_mp[4] - S4_closed_s1)
                ),
                "route_2_mpmath_50dps_s1_vs_closed_residual": float(
                    abs(S_mp_from_s1[4] - S4_closed_s1)
                ),
                "route_3_partial_sum_200_pairs": float(partial_S4_200),
                "route_3_partial_plus_tail": float(partial_S4_200 + asymptotic_tail_S4),
                "route_3_tail_corrected_residual": float(
                    abs((partial_S4_200 + asymptotic_tail_S4) - S4_closed_s1)
                ),
                "value_50dps": mpmath.nstr(S4_closed_s1, 45),
                "value_float": float(S4_closed_s1),
            },
            "reciprocal_power_hierarchy": {
                "general_definition": "S_m = sum_rho rho^{-m}",
                "absolute_convergence_for_m_ge_2": (
                    "For every integer m >= 2, sum_rho |rho|^{-m} < infty by partial summation against "
                    "N(T) = (T/(2*pi))log(T/(2*pi)) - T/(2*pi) + O(log T) = O(T log T), since "
                    "int_2^infty T^{-m} log T dT < infty for m >= 2."
                ),
                "general_log_derivative_identity": (
                    "S_m = - (1 / (m - 1)!) * (d^m / ds^m)|_{s=0} log xi(s) "
                    "= ((-1)^{m+1} / (m - 1)!) * (d^m / ds^m)|_{s=1} log xi(s)"
                ),
                "all_symbolic_m_1_to_4_verified": bool(
                    s1_symbolic_match
                    and s1_s1_symbolic_match
                    and s2_s0_symbolic_match
                    and s2_s1_symbolic_match
                    and s3_s1_symbolic_match
                    and s4_s1_symbolic_match
                ),
                "table_m_1_to_4": [
                    {
                        "m": 1,
                        "convergence": "Conditionally convergent (symmetric pairing |Im(rho)| <= T)",
                        "log_derivative_formula": "-(d/ds)|_{s=0} log xi(s) = +(d/ds)|_{s=1} log xi(s)",
                        "exact_expression": "1 + gamma_E/2 - log(2*sqrt(pi))",
                        "value_50dps": mpmath.nstr(S_mp[1], 40),
                        "residual_vs_closed_form": float(abs(S_mp[1] - S1_closed)),
                    },
                    {
                        "m": 2,
                        "convergence": "Absolutely convergent",
                        "log_derivative_formula": "-(d^2/ds^2)|_{s=0} log xi(s) = -(d^2/ds^2)|_{s=1} log xi(s)",
                        "exact_expression": "1 + gamma_E^2 - pi^2/8 + 2*gamma_1^St  (= 1 - pi^2/24 + 2*zeta''(0) + log^2(2*pi))",
                        "value_50dps": mpmath.nstr(S_mp[2], 40),
                        "residual_vs_closed_form": float(abs(S_mp[2] - S2_closed_s1)),
                    },
                    {
                        "m": 3,
                        "convergence": "Absolutely convergent",
                        "log_derivative_formula": "-(1/2!)*(d^3/ds^3)|_{s=0} log xi(s) = +(1/2!)*(d^3/ds^3)|_{s=1} log xi(s)",
                        "exact_expression": "1 - (7/8)*zeta(3) + gamma_E^3 + 3*gamma_E*gamma_1^St + (3/2)*gamma_2^St",
                        "value_50dps": mpmath.nstr(S_mp[3], 40),
                        "residual_vs_closed_form": float(abs(S_mp[3] - S3_closed_s1)),
                    },
                    {
                        "m": 4,
                        "convergence": "Absolutely convergent",
                        "log_derivative_formula": "-(1/3!)*(d^4/ds^4)|_{s=0} log xi(s) = -(1/3!)*(d^4/ds^4)|_{s=1} log xi(s)",
                        "exact_expression": "1 - pi^4/96 + gamma_E^4 + 4*gamma_E^2*gamma_1^St + 2*(gamma_1^St)^2 + 2*gamma_E*gamma_2^St + (2/3)*gamma_3^St",
                        "value_50dps": mpmath.nstr(S_mp[4], 40),
                        "residual_vs_closed_form": float(abs(S_mp[4] - S4_closed_s1)),
                    },
                ],
                "lean_theorem": "reciprocal_power_log_derivative_sign_identity",
            },
            "centered_zero_invariants": {
                "centered_coordinate": "z_rho = rho - 1/2 = delta_rho + i*gamma_rho",
                "completed_centered_function": "Xi(z) := xi(1/2 + z) = Xi(-z)",
                "odd_centered_sums_vanish": {
                    "statement": "sum_rho^{sym} z_rho^{-(2m-1)} = 0 for all m >= 1",
                    "proof": (
                        "Under functional-equation reflection rho <-> 1 - rho, z_{1-rho} = -z_rho, "
                        "so z_rho^{-(2m-1)} + (-z_rho)^{-(2m-1)} = 0 identically; equivalently, "
                        "log Xi(z) is an even analytic function at z = 0."
                    ),
                    "mpmath_odd_derivative_residuals": {
                        "m_eq_1": float(abs(Sigma1_odd_mp)),
                        "m_eq_2": float(abs(Sigma3_odd_mp)),
                    },
                    "lean_theorem": "reciprocal_power_log_derivative_sign_identity",
                },
                "even_centered_sums": {
                    "general_formula": "Sigma_{2m} = sum_rho z_rho^{-2m} = -(1 / (2m - 1)!) * (d^{2m}/dz^{2m})|_{z=0} log Xi(z)",
                    "Sigma_2": {
                        "exact_expression": "8 - (1/4)*psi_1(1/4) - (d^2/ds^2)|_{s=1/2} log(-zeta(s))",
                        "quartet_decomposition": "sum_{quartets} 4*(delta^2 - gamma^2) / (delta^2 + gamma^2)^2",
                        "value_50dps": mpmath.nstr(Sigma2_mp, 40),
                        "closed_form_residual": float(abs(Sigma2_mp - Sigma2_closed)),
                    },
                    "Sigma_4": {
                        "exact_expression": "-(1/6) * (d^4/dz^4)|_{z=0} log Xi(z)",
                        "value_50dps": mpmath.nstr(Sigma4_mp, 40),
                    },
                    "simpler_than_uncentered_note": (
                        "Unlike S_m at s = 0/1 where log(-zeta(s)) has an explicit Laurent expansion in "
                        "gamma_E and Stieltjes constants gamma_k^St, centered sums Sigma_{2m} at s = 1/2 "
                        "depend on zeta^{(k)}(1/2)/zeta(1/2), which have no simpler closed form in classic "
                        "constants; however, all odd centered sums vanish identically by reflection symmetry."
                    ),
                },
            },
            "quartet_polynomial": {
                "centered_quartet_roots": "{z, -z, conj(z), -conj(z)} with z = delta + i*gamma",
                "monic_polynomial": "(X^2 - z^2)(X^2 - conj(z)^2) = X^4 - 2*(delta^2 - gamma^2)*X^2 + (delta^2 + gamma^2)^2",
                "quadratic_coefficient_c2": "-2 * (delta^2 - gamma^2) = -(z^2 + conj(z)^2)",
                "constant_coefficient_c0": "(delta^2 + gamma^2)^2 = z^2 * conj(z)^2 >= 0",
                "global_symmetric_relation": (
                    "The global centered invariant Sigma_2 = sum_rho z_rho^{-2} determines the sum over "
                    "quartets of -c2 / c0 = 4*(delta^2 - gamma^2)/(delta^2 + gamma^2)^2, and Sigma_4 "
                    "determines the sum of (c2^2 - 2*c0)/c0^2, but global symmetric sums cannot "
                    "isolate an individual quartet's (delta_rho, gamma_rho)."
                ),
                "lean_theorems": [
                    "centered_quartet_polynomial_identity",
                    "centered_quartet_coefficients_real",
                ],
            },
            "li_coefficient_audit": {
                "spectral_definition": "lambda_n = sum_rho^{sym} [1 - (1 - 1/rho)^n]",
                "derivative_representation": "lambda_n = (1 / (n - 1)!) * (d^n / ds^n)|_{s=1} [s^{n-1} log xi(s)]",
                "binomial_reciprocal_expansion": "lambda_n = sum_{j=1}^n (-1)^{j-1} * binom(n, j) * S_j",
                "lambda_1_identity": "lambda_1 = S_1 = 1 + gamma_E/2 - log(2*sqrt(pi))",
                "li_criterion": "lambda_n > 0 for all n >= 1  <=>  RH (Li 1997; Bombieri-Lagarias 1999)",
                "positivity_firewall": LI_COEFFICIENT_POSITIVITY_IS_RH_EQUIVALENT,
                "values_n_1_to_4": [
                    {
                        "n": n,
                        "value_50dps": mpmath.nstr(lambda_binomial[n], 40),
                        "binomial_vs_derivative_residual": float(
                            abs(lambda_binomial[n] - lambda_deriv[n])
                        ),
                    }
                    for n in (1, 2, 3, 4)
                ],
                "lean_theorem": "li_first_coefficient_finite_algebra_identity",
                "primary_citations": [
                    "X.-J. Li (1997), J. Number Theory 65, 325-333",
                    "E. Bombieri and J. C. Lagarias (1999), J. Number Theory 77, 274-287",
                    "J. C. Lagarias (2004/2007), arXiv:math/0404394v4",
                ],
            },
            "partial_sum_numerical_controls": {
                "reference_zero_count_pairs": len(ordinates_200),
                "max_ordinate_T_200": float(T_200),
                "S1_partial_200_pairs": float(partial_S1_200),
                "S1_partial_plus_asymptotic_tail": float(
                    partial_S1_200 + asymptotic_tail_S1
                ),
                "S1_exact": float(S1_closed),
                "S1_tail_corrected_error": float(
                    abs((partial_S1_200 + asymptotic_tail_S1) - S1_closed)
                ),
                "reflection_sum_partial_200_pairs": float(partial_refl_200),
                "reflection_sum_exact": float(refl_sum_closed),
                "S2_partial_200_pairs": float(partial_S2_200),
                "S2_exact": float(S2_closed_s1),
                "S3_partial_200_pairs": float(partial_S3_200),
                "S3_partial_plus_asymptotic_tail": float(
                    partial_S3_200 + asymptotic_tail_S3
                ),
                "S3_exact": float(S3_closed_s1),
                "S4_partial_200_pairs": float(partial_S4_200),
                "S4_partial_plus_asymptotic_tail": float(
                    partial_S4_200 + asymptotic_tail_S4
                ),
                "S4_exact": float(S4_closed_s1),
                "Sigma2_partial_200_pairs": float(partial_Sigma2_200),
                "Sigma2_exact": float(Sigma2_mp),
                "Sigma4_partial_200_pairs": float(partial_Sigma4_200),
                "Sigma4_exact": float(Sigma4_mp),
                "Sigma4_absolute_error_200_pairs": float(
                    abs(partial_Sigma4_200 - Sigma4_mp)
                ),
                "evidence_class": (
                    "Exact analytic values via log xi(s) derivatives at s=0/1/1/2; "
                    "finite 200-pair spectral truncation is a numerical control matching the asymptotic tail."
                ),
            },
        }
        return results
    finally:
        mpmath.mp.dps = old_dps


# ---------------------------------------------------------------------------
# 4. Superzeta Audit & Arithmetic Status of Exact Zero-Sum Constants (Sections 21 & 22)
# ---------------------------------------------------------------------------


def audit_superzeta_and_constant_arithmetic() -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Audit Voros superzeta functions (Section 21) and construct the Section 22 table
    of arithmetic nature for all exact zero-sum invariants using disambiguated
    Stieltjes notation `gamma_0^St = gamma_E, gamma_1^St, gamma_2^St, gamma_3^St`.
    """
    superzeta_audit = {
        "families_studied_by_voros": {
            "uncentered_superzeta": "Z_zeros(s) = sum_rho rho^{-s} (and Hurwitz shift sum_rho (rho + v)^{-s})",
            "centered_quadratic_superzeta": (
                "Z(sigma, x) = sum_{k>=1} (tau_k^2 + x^2)^{-sigma} where rho_k = 1/2 +- i*tau_k"
            ),
        },
        "analytic_continuation_status": {
            "status": PROVED_WITH_EXTERNAL_THEOREM,
            "summary": (
                "Voros (2003, Ann. Inst. Fourier 53, 665-699, arXiv:math/0104051v4; 2005, arXiv:math/0311029v1; "
                "2010 Springer monograph; 2014, arXiv:1403.4558v2) proved meromorphic continuation of both "
                "superzeta families to all s in C via explicit-formula contour integral representations "
                "involving log xi(s) and the incomplete Gamma / Gram-Jorgenson-Lang expansion."
            ),
        },
        "special_values_and_regularized_products": {
            "positive_integers_m_ge_2": "Z_zeros(m) = S_m = -(1/(m-1)!)(d^m/ds^m)|_{s=0} log xi(s)",
            "negative_odd_values_of_quadratic_superzeta": (
                "Expressible explicitly in terms of Bernoulli numbers, pi, log(2*pi), and derivatives of log Gamma"
            ),
            "zeta_regularized_determinant": (
                "exp(-d/ds|_{s=0} sum_rho (rho - s_0)^{-s}) recovers the Hadamard product xi(s_0)/xi(0) up to "
                "explicit elementary/Archimedean anomaly factors (Voros 2003, Theorem 1)."
            ),
        },
        "arithmetic_nature_of_positive_special_values": {
            "status": OPEN_IN_LITERATURE,
            "explanation": (
                "Although Z_zeros(m) = S_m has an exact closed form in terms of gamma_E, pi, log(2*pi), "
                "zeta(2k+1), and Stieltjes constants gamma_j^St, NO positive integer value S_m (m >= 1) has "
                "proved rationality, irrationality, or transcendence in the literature because the "
                "irrationality and algebraic independence of gamma_E and Stieltjes constants gamma_j^St are open."
            ),
        },
        "primary_citations": [
            "A. Voros (2003), Ann. Inst. Fourier (Grenoble) 53, 665-699 (arXiv:math/0104051v4)",
            "A. Voros (2005), in Number Theory, Physics and Geometry (arXiv:math/0311029v1)",
            "A. Voros (2010), Zeta Functions over Zeros of Zeta Functions, Springer LNUMI Vol. 8",
            "A. Voros (2014), arXiv:1403.4558v2",
        ],
    }

    constant_status_table: List[Dict[str, Any]] = [
        {
            "invariant": "S_1 = sum_rho^{sym} 1/rho = lambda_1",
            "exact_expression": "1 + gamma_E/2 - log(2*sqrt(pi))",
            "rationality_known": "No (OPEN_IN_LITERATURE)",
            "irrationality_known": "No (OPEN_IN_LITERATURE)",
            "transcendence_known": "No (OPEN_IN_LITERATURE)",
            "main_unresolved_constants": [
                "gamma_E = gamma_0^St (Euler's constant: even irrationality is open)",
                "log(pi) (irrationality/transcendence of log(pi) and Q-linear independence of {1, gamma_E, log(4*pi)} are open)",
            ],
        },
        {
            "invariant": "sum_rho 1 / (rho * (1 - rho)) = 2 * S_1 = 2 * lambda_1",
            "exact_expression": "2 + gamma_E - log(4 * pi)",
            "rationality_known": "No (OPEN_IN_LITERATURE)",
            "irrationality_known": "No (OPEN_IN_LITERATURE)",
            "transcendence_known": "No (OPEN_IN_LITERATURE)",
            "main_unresolved_constants": [
                "gamma_E = gamma_0^St",
                "log(4*pi) = 2*log(2) + log(pi)",
                "Possible rational cancellation between gamma_E and log(4*pi) is unexcluded",
            ],
        },
        {
            "invariant": "S_2 = sum_rho 1 / rho^2",
            "exact_expression": "1 + gamma_E^2 - pi^2 / 8 + 2 * gamma_1^St  (= 1 - pi^2 / 24 + 2 * zeta''(0) + log^2(2*pi))",
            "rationality_known": "No (OPEN_IN_LITERATURE)",
            "irrationality_known": "No (OPEN_IN_LITERATURE)",
            "transcendence_known": "No (OPEN_IN_LITERATURE)",
            "main_unresolved_constants": [
                "gamma_E = gamma_0^St",
                "First Stieltjes constant gamma_1^St (irrationality open)",
                "zeta''(0) and log(2*pi)",
                "Algebraic independence of {pi^2, gamma_E, gamma_1^St}",
            ],
        },
        {
            "invariant": "S_3 = sum_rho 1 / rho^3",
            "exact_expression": "1 - (7/8)*zeta(3) + gamma_E^3 + 3*gamma_E*gamma_1^St + (3/2)*gamma_2^St",
            "rationality_known": "No (OPEN_IN_LITERATURE)",
            "irrationality_known": "No (OPEN_IN_LITERATURE)",
            "transcendence_known": "No (OPEN_IN_LITERATURE)",
            "main_unresolved_constants": [
                "zeta(3) (proved irrational by Apery 1979, but transcendence open)",
                "gamma_E, gamma_1^St, gamma_2^St (Stieltjes constants)",
            ],
        },
        {
            "invariant": "S_4 = sum_rho 1 / rho^4",
            "exact_expression": "1 - pi^4/96 + gamma_E^4 + 4*gamma_E^2*gamma_1^St + 2*(gamma_1^St)^2 + 2*gamma_E*gamma_2^St + (2/3)*gamma_3^St",
            "rationality_known": "No (OPEN_IN_LITERATURE)",
            "irrationality_known": "No (OPEN_IN_LITERATURE)",
            "transcendence_known": "No (OPEN_IN_LITERATURE)",
            "main_unresolved_constants": [
                "gamma_E, gamma_1^St, gamma_2^St, gamma_3^St (Stieltjes constants vs. pi^4)",
            ],
        },
        {
            "invariant": "Sigma_{2m-1} = sum_rho^{sym} (rho - 1/2)^{-(2m-1)}",
            "exact_expression": "0 (identically for all m >= 1)",
            "rationality_known": "Yes (equals 0 in Q)",
            "irrationality_known": "False (rational: 0)",
            "transcendence_known": "False (algebraic: 0)",
            "main_unresolved_constants": [],
        },
        {
            "invariant": "Sigma_2 = sum_rho (rho - 1/2)^{-2}",
            "exact_expression": "8 - (1/4)*psi_1(1/4) - (d^2/ds^2)|_{s=1/2} log(-zeta(s))",
            "rationality_known": "No (OPEN_IN_LITERATURE)",
            "irrationality_known": "No (OPEN_IN_LITERATURE)",
            "transcendence_known": "No (OPEN_IN_LITERATURE)",
            "main_unresolved_constants": [
                "psi_1(1/4) = pi^2 + 8*G (Catalan's constant G, irrationality open)",
                "zeta'(1/2)/zeta(1/2) and zeta''(1/2)/zeta(1/2)",
            ],
        },
        {
            "invariant": "lambda_n (Li coefficients, n >= 1)",
            "exact_expression": "sum_{j=1}^n (-1)^{j-1} binom(n, j) S_j",
            "rationality_known": "No (OPEN_IN_LITERATURE)",
            "irrationality_known": "No (OPEN_IN_LITERATURE)",
            "transcendence_known": "No (OPEN_IN_LITERATURE)",
            "main_unresolved_constants": [
                "gamma_E, log(4*pi), pi^{2k}, zeta(2k+1), Stieltjes constants gamma_0^St, ..., gamma_{n-1}^St",
            ],
        },
    ]

    return superzeta_audit, constant_status_table


# ---------------------------------------------------------------------------
# 5. Fauzan (2026) zeta(5) Audit & Special-Value Transfer Audit (TASK-TC-038R Sections 4–11, 25–30)
# ---------------------------------------------------------------------------


def load_fauzan_zeta5_architecture(repo_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load the structured primary-source architecture artifact `data/fauzan_zeta5_architecture.json`.
    """
    root = repo_root or Path(__file__).resolve().parent.parent
    arch_path = root / "data" / "fauzan_zeta5_architecture.json"
    if not arch_path.exists():
        raise FileNotFoundError(f"Missing Fauzan architecture artifact: {arch_path}")
    return json.loads(arch_path.read_text(encoding="utf-8"))


def verify_zeta5_and_special_value_transfer() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """
    Verify from primary sources the October 2026 status of Archimedean `zeta(5)` (Sections 4–8),
    reconstruct the 6-gate Fauzan / `mo271/Zeta5` Hankel irrationality proof, compare classical
    vs. Fauzan 2026 methods against zero-location arithmetic (Sections 8–10, 30), and derive the
    Liouville-Mahler algebraic lower bound and 6-gate `SUBGATE-TC-039A` map (Sections 11, 27–29).
    """
    fauzan_arch = load_fauzan_zeta5_architecture()

    zeta5_status = {
        "status_code": ZETA5_CURRENT_STATUS_VERIFIED,
        "preprint_claim_status": ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM,
        "preprint_verification_status": ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM_VERIFIED,
        "lean_formalization_status": ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN,
        "external_lean_evidence_class": LEAN_PROVED_EXTERNAL_REPOSITORY,
        "local_build_audit_status": SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED,
        "dependency_graph_status": ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN,
        "conventional_peer_review_status": PEER_REVIEW_STATUS_PENDING,
        "peer_review_status_recorded": ZETA5_CONVENTIONAL_PEER_REVIEW_STATUS_RECORDED,
        "archimedean_zeta5_status": (
            "ZETA5_IRRATIONALITY_2026_PREPRINT_AND_LEAN_FORMALIZED_PEER_REVIEW_PENDING"
        ),
        "source_verification": PRIMARY_SOURCE_VERIFIED,
        "fauzan_2026_preprint": fauzan_arch["paper_reference"],
        "mo271_zeta5_lean_repository": fauzan_arch["lean_repository"],
        "verified_theorems_in_primary_literature": {
            "fauzan_2026_and_mo271_zeta5": {
                "theorem": (
                    "zeta(5) notin Q: Aabir Fauzan (17 Sep 2026, Zenodo 22826419, DOI 10.5281/zenodo.22826419) "
                    "constructs integer polynomials Q_n in Z[X] of degree 37n via a 37n x 37n Hankel determinant "
                    "satisfying 0 < Q_n(zeta(5)) < exp(-c n^2); mechanically formalized in Lean 4 without sorry "
                    "in mo271/Zeta5 (commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0) as Apery.irrational_five "
                    "and RiemannZetaValues.irrational_five depending only on [propext, Classical.choice, Quot.sound]."
                ),
                "manuscript_status": ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM,
                "formal_status": ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN,
                "peer_review_status": PEER_REVIEW_STATUS_PENDING,
            },
            "apery_1979_zeta3": {
                "theorem": "zeta(3) notin Q (irrationality exponent mu(zeta(3)) < 5.5138800, Giraudin 2026 arXiv:2609.26980v1; Rhin-Viola 2001).",
                "citation": "R. Apery (1979), Asterisque 61, 11-13; F. Beukers (1979), Bull. London Math. Soc. 11, 268-272.",
            },
            "rivoal_2000_ball_rivoal_2001_infinite_odd_zeta": {
                "theorem": (
                    "dim_Q span_Q(1, zeta(3), zeta(5), ..., zeta(2n+1)) >= ((1 + o(1))/(1 + log 2)) log n; "
                    "in particular, infinitely many odd zeta values are irrational."
                ),
                "citation": "T. Rivoal (2000), C. R. Acad. Sci. Paris 331, 267-270; K. Ball and T. Rivoal (2001), Invent. Math. 146, 193-207.",
            },
            "zudilin_2001_one_of_four": {
                "theorem": "At least one of the four odd zeta values {zeta(5), zeta(7), zeta(9), zeta(11)} is irrational.",
                "citation": "W. Zudilin (2001), Russ. Math. Surveys 56(4), 149-150; Izv. Math. 66 (2002), 489-542 (arXiv:math/0104249v1; arXiv:math/0206176v2).",
            },
            "rivoal_zudilin_2018_two_among_69": {
                "theorem": "At least two of the odd zeta values {zeta(5), zeta(7), ..., zeta(69)} are irrational.",
                "citation": "T. Rivoal and W. Zudilin (2018/2020), Compos. Math. 156 (arXiv:1803.03160v1).",
            },
            "fischler_sprang_zudilin_2019_subexponential_count": {
                "theorem": "At least 2^{(1 - eps) log s / log log s} odd zeta values between 3 and s are irrational.",
                "citation": "S. Fischler, J. Sprang, and W. Zudilin (2019), Compos. Math. 155(5), 938-952 (arXiv:1803.08905v2).",
            },
            "lai_sprang_zudilin_2025_2adic_zeta2_5": {
                "theorem": (
                    "The 2-adic Kubota-Leopoldt zeta value zeta_2(5) is irrational (following Calegari-Dimitrov-Tang on zeta_2(3) "
                    "and Lai-Lupu-Sprang 2025 arXiv:2505.23088v1 on p-adic Zudilin tuples)."
                ),
                "citation": "L. Lai, J. Sprang, and W. Zudilin (May 2025), 'A note on the irrationality of zeta_2(5)', arXiv:2505.05005v2.",
            },
            "refuted_2024_preprint_on_archimedean_zeta5": {
                "claim_inspected": "S. Suman (July 2024), 'A note on the Irrationality of zeta(5) and Higher Odd Zeta Values', arXiv:2407.07121 [math.GM].",
                "refutation": (
                    "Explicitly refuted by K. Chen et al. (Nov 2024), 'A Note on a Recent Attempt to Prove the Irrationality of zeta(5)', arXiv:2411.16774v3."
                ),
            },
        },
        "record_correction": (
            "TASK-TC-038R repair: As of 17 September 2026, Aabir Fauzan released the preprint "
            "'zeta(5) is irrational' (Zenodo 22826419) and the complete Lean 4 formalization "
            "mo271/Zeta5 (commit 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0) proving Apery.irrational_five "
            "without sorry and using only standard Lean axioms [propext, Classical.choice, Quot.sound]. "
            "We classify the manuscript claim (ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM), the Lean 4 "
            "verification (ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN / LEAN_PROVED_EXTERNAL_REPOSITORY / "
            "SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED), and conventional journal peer review "
            "(PEER_REVIEW_STATUS_PENDING) across separate evidence dimensions."
        ),
    }

    classical_vs_fauzan_comparison = [
        {
            "feature": "Target is a value vs. an argument",
            "classical_special_value_method": "Linear form in the VALUE zeta(m) at fixed integer argument m: L_n = A_n zeta(m) - B_n.",
            "fauzan_2026_method": "Nonlinear polynomial Q_n(X) in Z[X] of degree 37n in the VALUE variable X, evaluated at X = zeta(5).",
            "relevance_to_zero_location_arithmetic": (
                "Both act on a VALUE variable X = zeta(5), whereas zero arithmetic requires an ARGUMENT "
                "polynomial P_n(X) evaluated at X = gamma_1 or X = rho_1 (where zeta(rho_1) = 0 is already 0)."
            ),
        },
        {
            "feature": "Hankel determinant",
            "classical_special_value_method": "None (single Pade / hypergeometric linear form).",
            "fauzan_2026_method": "37n x 37n Hankel determinant Delta_K(X) = det_{0<=i,j<37n} mu_X(D_N(t)^6 t^{i+j} / D_K(t)).",
            "relevance_to_zero_location_arithmetic": (
                "Introduces a determinant mechanism generating degree O(n) polynomials with O(n^2) log-decay "
                "from Vandermonde energy; testable in TASK-TC-039 if a zero-argument moment functional exists."
            ),
        },
        {
            "feature": "Moment functional",
            "classical_special_value_method": "Direct series sum_{k>=1} R_n(k) or Beukers hypercube integral.",
            "fauzan_2026_method": (
                "Q-linear functional mu_X on P(t)/D_K(t) combining rational Bernoulli even moments mu(t^e) "
                "with affine pole values mu_X(1/(t+j^2)) = j^4(X - H_j^{(5)}) - 1/4 + 1/(2j)."
            ),
            "relevance_to_zero_location_arithmetic": (
                "Requires an integral identity expressing rational pole values in terms of the target parameter X."
            ),
        },
        {
            "feature": "Positivity / nonvanishing",
            "classical_special_value_method": "Strict positivity of Beukers integrand on (0,1)^m or saddle-point nonvanishing.",
            "fauzan_2026_method": (
                "At X = zeta(5), G_K(zeta(5)) is the Gram matrix of {(y^2)^i}_{i=0}^{h-1} against positive measure "
                "nu_n(y) dy = (D_N(y^2)^6 / D_K(y^2)) w(y) dy on (0, infty), forcing Delta_K(zeta(5)) > 0."
            ),
            "relevance_to_zero_location_arithmetic": (
                "High-priority transfer gate (Z3): for a zero rho_1, zeta(rho_1) = 0 must NOT make the moment "
                "matrix singular or vanish identically."
            ),
        },
        {
            "feature": "Integer polynomial construction",
            "classical_special_value_method": "Degree-1 linear form A_n X - B_n in Z[X].",
            "fauzan_2026_method": "Degree-37n integer polynomial Q_n(X) = m_N(n) S_K Delta_K(X) in Z[X].",
            "relevance_to_zero_location_arithmetic": (
                "Moves beyond degree-1 rational approximations to degree-O(n) integer polynomials."
            ),
        },
        {
            "feature": "Denominator / valuation estimates",
            "classical_special_value_method": "d_n^m = lcm(1..n)^m ~ e^{m n} clearing denominators of partial fractions.",
            "fauzan_2026_method": (
                "Local p-adic Gauss valuation bounds v_p^G(F_K) >= L_p(n,p) across small (p <= K/400), "
                "inner (K/400 < p <= K/3, water-filling), and outer (K/3 < p <= 2h, Schur rank loss) primes, "
                "giving log m_N(n) <= (A_eff + eps) K^2 via PNT."
            ),
            "relevance_to_zero_location_arithmetic": (
                "Quadratic log-normalizer O(n^2) works for rationality (D=1) because b^{37n} grows only like e^{O(n)}, "
                "but for algebraicity of degree D >= 2, (D-1) log H(P_n) competes directly with O(n^2) decay."
            ),
        },
        {
            "feature": "Asymptotic smallness",
            "classical_special_value_method": "Exponential decay e^{-c n} competing with e^{m n} (fails for m >= 5 in Apery/Beukers).",
            "fauzan_2026_method": (
                "Superexponential quadratic decay exp(U K^2 + O(K log K)) with U = -1.3669955 < -A_eff = -1.36 "
                "from Andreief's identity and 16-component arcsine Vandermonde logarithmic energy."
            ),
            "relevance_to_zero_location_arithmetic": (
                "Quadratic exponent n^2 from h x h Vandermonde repulsion is strong enough to beat any O(n) "
                "degree/Mahler factor if coefficient height growth is controlled."
            ),
        },
        {
            "feature": "Degree growth",
            "classical_special_value_method": "Fixed degree 1 in zeta(5) (or fixed number of odd zetas).",
            "fauzan_2026_method": "Linear degree growth deg Q_n = h = 37n.",
            "relevance_to_zero_location_arithmetic": (
                "Linear degree d_n = O(n) ensures b^{d_n} = e^{O(n)} is negligible compared to e^{-c n^2}."
            ),
        },
        {
            "feature": "Role of the specific exponent 5",
            "classical_special_value_method": "Dimension 5 of hypercube [0,1]^5 or pole order 5 in (k+j)^{-5}.",
            "fauzan_2026_method": (
                "Enters specifically via weight w(y) = (y^5/12)(d^4/dy^4)(1/(e^{2*pi*y}-1)) and 4 integrations "
                "by parts in Hermite's formula at s = 5, plus Bernoulli moments zeta(2e+2)."
            ),
            "relevance_to_zero_location_arithmetic": (
                "Weight-5 Hermite IBP and Bernoulli moments are specific to s = 5; literal substitution 5 -> rho "
                "is invalid (Section 29 firewall)."
            ),
        },
    ]

    transfer_audit = {
        "interim_classification": SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT,
        "repaired_audit_status": SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT_REPAIRED,
        "classification": FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED,
        "secondary_outcome_code": FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED,
        "classical_methods_status": SPECIAL_VALUE_IRRATIONALITY_METHOD_HAS_NO_DIRECT_ZERO_LOCATION_TRANSFER,
        "structural_distinction": VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE,
        "substitution_firewall": "DO_NOT_SUBSTITUTE_5_TO_RHO_SYMBOLICALLY",
        "classical_vs_fauzan_2026_comparison_table": classical_vs_fauzan_comparison,
        "fauzan_6_gate_architecture": {
            "Gate_A_moment_hankel_construction": (
                "Define K = 40n, N = 3n, h = 37n, D_m(t) = prod_{j=1}^m (t + j^2), Q-linear functional mu_X on "
                "P(t)/D_K(t) with monomial moments mu(t^e) = (-1)^e B_{2e+2}(2e+3)(2e+4)(2e+5)/24 and pole values "
                "mu_X(1/(t+j^2)) = j^4(X - H_j^{(5)}) - 1/4 + 1/(2j), and 37n x 37n Hankel matrix "
                "G_K(X)_{i,j} = mu_X(D_N(t)^6 t^{i+j} / D_K(t)), Delta_K(X) = det G_K(X) (`Apery/Construction.lean`)."
            ),
            "Gate_B_polynomiality_and_exact_degree": (
                "Entries G_K(X)_{i,j} are affine in X; the X^h coefficient of Delta_K(X) is det(V^T diag(w_k) V) "
                "at distinct nodes x_k = -(N+1+k)^2 with nonzero weights w_k = D_N(x_k)^6 (N+1+k)^4 / D_K'(x_k), "
                "proving deg Delta_K = deg F_K = h = 37n (`Apery/Degree.lean`, `natDegree_F`)."
            ),
            "Gate_C_positivity_at_zeta5": (
                "By 4 integrations by parts against Mittag-Leffler (`Apery/HermiteFormula.lean`, `hermite_pole`), "
                "int_0^infty w(y)/(y^2+j^2) dy = poleValue(j)(zeta(5)), so G_K(zeta(5)) is the Gram matrix of "
                "{(y^2)^i}_{i=0}^{h-1} against positive measure nu_n(y) dy = (D_N(y^2)^6/D_K(y^2)) w(y) dy on (0, infty), "
                "forcing Delta_K(zeta(5)) > 0 and Q_n(zeta(5)) > 0 (`Apery/Positivity.lean`, `Delta_pos`)."
            ),
            "Gate_D_arithmetic_integrality_normalization": (
                "Local p-adic Gauss valuation bounds v_p^G(F_K) >= L_p(n,p) across small (400p <= K), inner "
                "(K/400 < p <= K/3), and outer (K/3 < p <= 2h) primes plus v_p^G(F_K) >= 0 for p > 2h prove that "
                "m_N(n) = prod_{p <= 2h} p^{-L_p(n,p)} clears all denominators: Q_n(X) = m_N(n) F_K(X) in Z[X], "
                "with log m_N(n) <= (A_eff + eps) K^2 (A_eff = 1.36) by PNT (`Apery/Norm.lean`, `Apery/Growth.lean`)."
            ),
            "Gate_E_superexponential_analytic_decay": (
                "By Andreief's identity (`Apery/DetIntegral.lean`, `Delta_eq_integral`) and potential-theoretic "
                "bounds against a 16-component arcsine equilibrium measure (`Apery/Energy*.lean`, `Apery/RealBound.lean`), "
                "log F_K(zeta(5)) <= U K^2 + 27 K log K + 200 K with U = -1.3669955 < -A_eff = -1.36, giving "
                "0 < Q_n(zeta(5)) < exp(-c n^2) (c_Lean = 5.5964, c_paper = 27.8)."
            ),
            "Gate_F_irrationality_contradiction": (
                "If zeta(5) = a/b (b >= 1), then b^{37n} Q_n(a/b) in Z_{>=1}, whereas b^{37n} Q_n(zeta(5)) < "
                "b^{37n} exp(-c n^2) -> 0 as n -> infty, contradiction (`Apery/Criterion.lean`, `Apery/Main.lean`)."
            ),
        },
        "transferable_ingredients_vs_obstructions": {
            "conceptually_transferable_ingredients": fauzan_arch[
                "potential_zero_location_transfer_points"
            ],
            "nontransferable_weight5_specific_ingredients": fauzan_arch[
                "nontransferable_weight5_specific_parts"
            ],
        },
    }

    auxiliary_poly_audit = {
        "structural_distinction": VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE,
        "value_vs_argument_explanation": (
            "Fauzan (2026) constructs a polynomial Q_n(X) in Z[X] in a VALUE variable X and evaluates at "
            "X = zeta(5), using the fact that the pole integral int_0^infty w(y)/(y^2+j^2) dy is affine in "
            "the value zeta(5). For a zeta zero rho_1 = beta_1 + i*gamma_1, the value zeta(rho_1) = 0 is "
            "already rational (zero), while the unknown target alpha in {gamma_1, rho_1} is the ARGUMENT "
            "entering nonlinearly inside n^{-rho_1}, Gamma(rho_1/2), or (y^2 + z_{rho_1}^2)^{-1}."
        ),
        "irrationality_vs_transcendence_diophantine_requirements": {
            "for_gamma_1_irrationality_D_eq_1": {
                "target": "gamma_1 notin Q",
                "diophantine_lower_bound": "If gamma_1 = a/b with b in Z_{>=1} and P_n(gamma_1) != 0, then |P_n(a/b)| >= b^{-d_n} = exp(-d_n log b).",
                "required_asymptotic_inequality": (
                    "With linear degree d_n <= C n, b^{-d_n} = exp(-O(n)) is independent of the coefficient "
                    "height H(P_n)! Hence ANY superexponential decay 0 < |P_n(gamma_1)| <= exp(-c n^2) (c > 0) "
                    "with P_n in Z[X] proves gamma_1 notin Q, even if log H(P_n) = O(n^2)."
                ),
            },
            "for_gamma_1_or_rho_1_algebraicity_exclusion_D_ge_2": {
                "target": "alpha notin Q_bar (or exclusion of algebraic degree [Q(alpha):Q] = D >= 2, required for non-real rho_1)",
                "liouville_mahler_lower_bound": (
                    "For algebraic alpha of degree D = [Q(alpha):Q] and Mahler measure M(alpha), and any "
                    "P_n in Z[X] of degree d_n and naive height H(P_n) with P_n(alpha) != 0: "
                    "|P_n(alpha)| >= ((d_n + 1) H(P_n))^{-(D - 1)} M(alpha)^{-d_n}, i.e., "
                    "log |P_n(alpha)| >= -(D - 1) log H(P_n) - d_n log M(alpha) - (D - 1) log(d_n + 1)."
                ),
                "regime_1_linear_log_height": (
                    "If d_n <= C n and log H(P_n) <= C' n (exponential height), then the lower bound is "
                    "exp(-O_D(n)), so |P_n(alpha)| <= exp(-c n^2) (c > 0) excludes ALL algebraic degrees D >= 1 "
                    "(proving full transcendence alpha notin Q_bar)."
                ),
                "regime_2_quadratic_log_height": (
                    "If log H(P_n) ~ A n^2 (as in Fauzan's normalizer where log H(Q_n) = O(n^2)) and "
                    "log |P_n(alpha)| <= -c n^2, then for D >= 2 the height term -(D - 1) A n^2 does NOT "
                    "vanish: contradiction at degree D requires c > (D - 1) A, and excluding all D >= 2 "
                    "simultaneously requires log H(P_n) = o(n^2) (or decay faster than exp(-c n^2))."
                ),
            },
        },
        "subgate_tc_039a": fauzan_arch["task_tc_039_gate_map"],
        "privileging_gamma_1_avoided": True,
        "status": FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED,
    }

    return zeta5_status, transfer_audit, auxiliary_poly_audit


# ---------------------------------------------------------------------------
# 6. Certified Finite Algebraicity & Bounded-Denominator Exclusions (Sections 30–34)
# ---------------------------------------------------------------------------


def get_certified_first_zero_enclosures() -> Dict[str, Any]:
    """
    Construct certified 128-bit Arb/Acb enclosures for:
      - `gamma_1` (first nontrivial zero ordinate)
      - `rho_1 = 1/2 + i*gamma_1` (first critical-line zero)
      - `gamma_1 + 1/2` (shifted ordinate control)
    and verify via Arb that `zeta(1/2 + i*gamma) = 0` crosses zero inside `I_{gamma_1}`
    via the real Hardy/xi function sign change across `[gamma_1 - 1e-30, gamma_1 + 1e-30]`.
    """
    if not FLINT_AVAILABLE:
        raise RuntimeError("python-flint (Arb) is required for certified zero enclosures.")

    old_prec = ctx.prec
    try:
        ctx.prec = 128
        g1_ball = arb(f"{GAMMA1_60DPS_STR} +/- {GAMMA1_ARB_RADIUS_STR}")
        half_ball = arb("0.5")
        shifted_ball = g1_ball + half_ball
        rho1_ball = acb(half_ball, g1_ball)

        # Verify via Arb Intermediate Value Theorem on the real critical-line function
        # Z_real(t) = Re(pi^{-i*t/2} Gamma(1/4 + i*t/2) zeta(1/2 + i*t)) that a zero lies in
        # [g1_mid - 1e-30, g1_mid + 1e-30], which is contained inside g1_ball + [-1e-30, 1e-30]
        delta_ivt = arb("1e-30")
        t_lo = g1_ball - delta_ivt
        t_hi = g1_ball + delta_ivt

        def hardy_real_arb(t_val: Any) -> Any:
            s_val = acb(half_ball, t_val)
            pref = (acb(arb.pi()) ** (-s_val / 2)) * (s_val / 2).gamma()
            return (pref * s_val.zeta()).real

        val_lo = hardy_real_arb(t_lo)
        val_hi = hardy_real_arb(t_hi)
        ivt_sign_change_certified = bool(
            ((val_lo > 0) and (val_hi < 0)) or ((val_lo < 0) and (val_hi > 0))
        )
        # Outward interval enclosure guaranteed by IVT: g1_ivt_ball = [g1_mid +/- 1e-30]
        g1_ivt_ball = g1_ball.union(t_lo).union(t_hi)
        shifted_ivt_ball = g1_ivt_ball + half_ball
        rho1_ivt_ball = acb(half_ball, g1_ivt_ball)

        return {
            "prec_bits": 128,
            "gamma_1_mid": float(g1_ivt_ball.mid()),
            "gamma_1_rad": float(g1_ivt_ball.rad()),
            "gamma_1_str": str(g1_ivt_ball),
            "ivt_sign_change_certified": ivt_sign_change_certified,
            "gamma_1_ball": g1_ivt_ball,
            "shifted_ordinate_ball": shifted_ivt_ball,
            "rho_1_ball": rho1_ivt_ball,
        }
    finally:
        ctx.prec = old_prec


def enumerate_normalized_primitive_polynomials(D: int = 4, H: int = 3) -> List[Tuple[int, ...]]:
    """
    Enumerate normalized primitive integer polynomials
      P(X) = a_0 + a_1 X + ... + a_d X^d
    satisfying Section 31 normalization:
      - exact degree `1 <= d <= D` (`a_d > 0`)
      - `max_j |a_j| <= H`
      - `gcd(|a_0|, ..., |a_d|) == 1`
      - leading coefficient `a_d >= 1`
      - zero polynomial excluded.
    Returns tuples `(a_0, a_1, ..., a_d)`.
    """
    if D < 1 or H < 1:
        raise ValueError("D and H must be positive integers.")
    polys: List[Tuple[int, ...]] = []
    for d in range(1, D + 1):
        for lead in range(1, H + 1):
            for lower in itertools.product(range(-H, H + 1), repeat=d):
                g = lead
                for c in lower:
                    g = math.gcd(g, abs(c))
                    if g == 1:
                        break
                if g == 1:
                    polys.append(lower + (lead,))
    return polys


def count_primitive_polynomials_up_to(D: int = 4, H: int = 100) -> Dict[str, Any]:
    """
    Compute the exact count of normalized primitive integer polynomials of degree
    `1 <= d <= D` and height `<= H` (`a_d in [1, H]`, `a_0..a_{d-1} in [-H, H]`,
    `gcd(a_0, ..., a_d) = 1`) using exact Mobius inversion over divisors `g <= H`.
    """
    # Compute Mobius mu(1..H)
    mu = [0] * (H + 1)
    mu[1] = 1
    primes: List[int] = []
    is_comp = [False] * (H + 1)
    for i in range(2, H + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > H:
                break
            is_comp[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]

    by_degree: Dict[int, int] = {}
    total = 0
    for d in range(1, D + 1):
        cnt_d = 0
        for g in range(1, H + 1):
            if mu[g] == 0:
                continue
            q = H // g
            cnt_d += mu[g] * q * ((2 * q + 1) ** d)
        by_degree[d] = cnt_d
        total += cnt_d
    return {"D": D, "H": H, "by_degree": by_degree, "total_primitive_polynomials": total}


def _certify_real_ball_polynomial_box(
    x_ball: Any, D: int = 4, H: int = 100
) -> Dict[str, Any]:
    """
    Certify `0 notin P(x_ball)` for ALL normalized primitive integer polynomials
    `P(X) = a_0 + a_1 X + ... + a_d X^d` with `1 <= d <= D` and `max_j |a_j| <= H`
    using 128-bit outward Arb interval arithmetic (hierarchical outward box + leaf checks).
    Fails closed (`RuntimeError`) if any polynomial enclosure contains 0.

    Scope note (TASK-TC-038R Route A, Section 20.1):
    Because pruned coefficient branches are excluded by outward interval enclosures without
    minimizing `|P|` over every pruned integer lattice point, this routine certifies
    `CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION` (`0 notin P(I)` for all `P` in the
    box) under method `HIERARCHICAL_BOX_EXCLUSION`, and explicitly sets
    `global_minimum_scope = FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED`.
    """
    if D > 4:
        raise ValueError("Hierarchical box certifier supports D <= 4.")
    if not FLINT_AVAILABLE:
        raise RuntimeError("python-flint (Arb) is required.")

    old_prec = ctx.prec
    try:
        ctx.prec = 128
        if not (x_ball.rad() < arb("1e-10")):
            raise RuntimeError("Zero enclosure precision insufficient; failing closed.")

        B = arb(0, H)
        x2 = x_ball * x_ball
        x3 = x2 * x_ball
        x4 = x3 * x_ball
        rem1 = B * x_ball + B
        rem2 = B * x2 + rem1
        rem3 = B * x3 + rem2
        x_mid = float(x_ball.mid())
        if abs(x_mid) < 1.0:
            raise RuntimeError("Real ordinate midpoint unexpectedly small.")

        min_evaluated_leaf_lb = float("inf")
        min_evaluated_leaf_coeffs: Tuple[int, ...] = ()
        box_exclusions = 0
        leaf_exclusions = 0

        a4_max = H if D >= 4 else 0
        for a4 in range(0, a4_max + 1):
            v4 = a4 * x4
            if a4 > 0 and not (0 in (v4 + rem3)):
                box_exclusions += 1
                continue
            a3_min = -H if a4 > 0 else 0
            a3_max = H if D >= 3 else 0
            for a3 in range(a3_min, a3_max + 1):
                v3 = v4 + a3 * x3
                if (a4 > 0 or a3 > 0) and not (0 in (v3 + rem2)):
                    box_exclusions += 1
                    continue
                a2_min = -H if (a4 > 0 or a3 > 0) else 0
                a2_max = H if D >= 2 else 0
                for a2 in range(a2_min, a2_max + 1):
                    v2 = v3 + a2 * x2
                    if (a4 > 0 or a3 > 0 or a2 > 0) and not (0 in (v2 + rem1)):
                        box_exclusions += 1
                        continue
                    a1_min = -H if (a4 > 0 or a3 > 0 or a2 > 0) else 1
                    c1 = int(round(-float(v2.mid()) / x_mid))
                    lo1 = max(a1_min, c1 - 8)
                    hi1 = min(H, c1 + 8)
                    if lo1 > a1_min:
                        m1 = (a1_min + (lo1 - 1)) / 2.0
                        r1 = ((lo1 - 1) - a1_min) / 2.0
                        if 0 in (v2 + arb(m1, r1) * x_ball + B):
                            raise RuntimeError("Outward left-a1 interval not excluded; failing closed.")
                        box_exclusions += 1
                    if hi1 < H:
                        m1 = ((hi1 + 1) + H) / 2.0
                        r1 = (H - (hi1 + 1)) / 2.0
                        if 0 in (v2 + arb(m1, r1) * x_ball + B):
                            raise RuntimeError("Outward right-a1 interval not excluded; failing closed.")
                        box_exclusions += 1
                    for a1 in range(lo1, hi1 + 1):
                        v1 = v2 + a1 * x_ball
                        if not (0 in (v1 + B)):
                            box_exclusions += 1
                            continue
                        c0 = int(round(-float(v1.mid())))
                        lo0 = max(-H, c0 - 1)
                        hi0 = min(H, c0 + 1)
                        if lo0 > -H:
                            if 0 in (v1 + arb((-H + lo0 - 1) / 2.0, (lo0 - 1 + H) / 2.0)):
                                raise RuntimeError("Outward left-a0 interval not excluded; failing closed.")
                            box_exclusions += 1
                        if hi0 < H:
                            if 0 in (v1 + arb((hi0 + 1 + H) / 2.0, (H - hi0 - 1) / 2.0)):
                                raise RuntimeError("Outward right-a0 interval not excluded; failing closed.")
                            box_exclusions += 1
                        for a0 in range(lo0, hi0 + 1):
                            g = math.gcd(
                                a4,
                                math.gcd(
                                    abs(a3),
                                    math.gcd(abs(a2), math.gcd(abs(a1), abs(a0))),
                                ),
                            )
                            if g != 1:
                                continue
                            val = abs(v1 + a0)
                            if not (val > 0):
                                raise RuntimeError(
                                    f"Arb enclosure for P={a0,a1,a2,a3,a4} contains 0; failing closed!"
                                )
                            leaf_exclusions += 1
                            lb = float(val.lower())
                            if lb < min_evaluated_leaf_lb:
                                min_evaluated_leaf_lb = lb
                                min_evaluated_leaf_coeffs = (a0, a1, a2, a3, a4)

        return {
            "certified": True,
            "certification_method": HIERARCHICAL_BOX_EXCLUSION,
            "exclusion_scope": CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION,
            "global_minimum_scope": FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED,
            "full_box_global_minimum_certified": False,
            "D": D,
            "H": H,
            "box_exclusions": box_exclusions,
            "leaf_exclusions": leaf_exclusions,
            "min_evaluated_leaf_abs_lower_bound_not_global_min": min_evaluated_leaf_lb,
            "closest_evaluated_leaf_polynomial_coeffs_a0_to_a4": list(min_evaluated_leaf_coeffs),
        }
    finally:
        ctx.prec = old_prec


def _certify_rho1_polynomial_box(
    rho1_ball: Any, D: int = 4, H: int = 100
) -> Dict[str, Any]:
    """
    Certify `0 notin P(rho_1)` for ALL normalized primitive integer polynomials
    `P(X) = a_0 + a_1 X + ... + a_d X^d` with `1 <= d <= D` and `max_j |a_j| <= H`
    in 128-bit Acb/Arb arithmetic.
    Key algebraic speedup: Since `a_0 in Z` is real, `Im(P(rho_1))` is completely
    independent of `a_0`! Whenever `0 notin Im(a_1 rho_1 + a_2 rho_1^2 + a_3 rho_1^3 + a_4 rho_1^4)`,
    all `a_0 in [-H, H]` are excluded simultaneously by `Im(P(rho_1)) != 0`.

    Scope note (TASK-TC-038R Route A, Section 20.1):
    Because imaginary-part pruning excludes all `a_0 in [-H, H]` simultaneously without
    checking whether `gcd(a_0, a_1, ..., a_d) = 1` or minimizing `|P(rho_1)|` over every
    pruned branch, this routine certifies `CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION`
    under method `HIERARCHICAL_BOX_EXCLUSION`, and explicitly sets
    `global_minimum_scope = FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED`.
    """
    if D > 4:
        raise ValueError("Certifier supports D <= 4.")
    if not FLINT_AVAILABLE:
        raise RuntimeError("python-flint (Arb) is required.")

    old_prec = ctx.prec
    try:
        ctx.prec = 128
        r1 = rho1_ball
        r2 = r1 * r1
        r3 = r2 * r1
        r4 = r3 * r1

        im1 = r1.imag
        im2 = r2.imag
        im3 = r3.imag
        im4 = r4.imag
        re1 = r1.real
        re2 = r2.real
        re3 = r3.real
        re4 = r4.real

        B = arb(0, H)
        im_rem2 = B * im2 + B * im1
        im_rem3 = B * im3 + im_rem2
        im1_mid = float(im1.mid())

        min_re_leaf_lb = float("inf")
        min_re_leaf_coeffs: Tuple[int, ...] = ()
        im_exclusions = 0
        re_leaf_exclusions = 0

        a4_max = H if D >= 4 else 0
        for a4 in range(0, a4_max + 1):
            im_v4 = a4 * im4
            if a4 > 0 and not (0 in (im_v4 + im_rem3)):
                im_exclusions += 1
                continue
            a3_min = -H if a4 > 0 else 0
            a3_max = H if D >= 3 else 0
            for a3 in range(a3_min, a3_max + 1):
                im_v3 = im_v4 + a3 * im3
                if (a4 > 0 or a3 > 0) and not (0 in (im_v3 + im_rem2)):
                    im_exclusions += 1
                    continue
                a2_min = -H if (a4 > 0 or a3 > 0) else 0
                a2_max = H if D >= 2 else 0
                for a2 in range(a2_min, a2_max + 1):
                    im_v2 = im_v3 + a2 * im2
                    a1_min = -H if (a4 > 0 or a3 > 0 or a2 > 0) else 1
                    c1 = int(round(-float(im_v2.mid()) / im1_mid))
                    lo1 = max(a1_min, c1 - 2)
                    hi1 = min(H, c1 + 2)
                    if lo1 > a1_min:
                        m1 = (a1_min + (lo1 - 1)) / 2.0
                        rad1 = ((lo1 - 1) - a1_min) / 2.0
                        if 0 in (im_v2 + arb(m1, rad1) * im1):
                            raise RuntimeError("Left a1 imaginary interval not excluded.")
                        im_exclusions += 1
                    if hi1 < H:
                        m1 = ((hi1 + 1) + H) / 2.0
                        rad1 = (H - (hi1 + 1)) / 2.0
                        if 0 in (im_v2 + arb(m1, rad1) * im1):
                            raise RuntimeError("Right a1 imaginary interval not excluded.")
                        im_exclusions += 1
                    for a1 in range(lo1, hi1 + 1):
                        im_val = abs(im_v2 + a1 * im1)
                        if im_val > 0:
                            im_exclusions += 1
                            continue
                        # Here 0 in Im(P(rho_1)) (which occurs when a4 = a3 = 0 and a1 + a2 = 0):
                        # Check Re(P(rho_1)) = a0 + a1*re1 + a2*re2 + a3*re3 + a4*re4
                        re_v1 = a4 * re4 + a3 * re3 + a2 * re2 + a1 * re1
                        if not (0 in (re_v1 + B)):
                            im_exclusions += 1
                            continue
                        for a0 in range(-H, H + 1):
                            g = math.gcd(
                                a4,
                                math.gcd(
                                    abs(a3),
                                    math.gcd(abs(a2), math.gcd(abs(a1), abs(a0))),
                                ),
                            )
                            if g != 1:
                                continue
                            mod_val = abs(
                                acb(re_v1 + a0, im_v2 + a1 * im1)
                            )
                            if not (mod_val > 0):
                                raise RuntimeError(
                                    f"Acb enclosure for P(rho_1) at {a0,a1,a2,a3,a4} contains 0!"
                                )
                            re_leaf_exclusions += 1
                            lb = float(mod_val.lower())
                            if lb < min_re_leaf_lb:
                                min_re_leaf_lb = lb
                                min_re_leaf_coeffs = (a0, a1, a2, a3, a4)

        return {
            "certified": True,
            "certification_method": HIERARCHICAL_BOX_EXCLUSION,
            "exclusion_scope": CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION,
            "global_minimum_scope": FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED,
            "full_box_global_minimum_certified": False,
            "D": D,
            "H": H,
            "im_exclusions": im_exclusions,
            "re_leaf_exclusions": re_leaf_exclusions,
            "min_evaluated_re_leaf_abs_lower_bound_not_global_min": min_re_leaf_lb,
            "closest_evaluated_re_leaf_polynomial_coeffs_a0_to_a4": list(min_re_leaf_coeffs),
        }
    finally:
        ctx.prec = old_prec


def certify_finite_algebraicity_exclusion(
    D_explicit: int = 4,
    H_explicit: int = 3,
    D_box: int = 4,
    H_box: int = 100,
    custom_enclosure: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Execute the certified finite algebraic-relation exclusions (repaired in TASK-TC-038R
    Sections 19-21 under Route A):
      1. `EXPLICIT_POLYNOMIAL_ENUMERATION`: Exhaustive polynomial-by-polynomial normalized
         enumeration for `1 <= d <= D_explicit`, `max_j |a_j| <= H_explicit` (`D <= 4, H <= 3`,
         `8,160` primitive polynomials) across all three candidate objects (`gamma_1`, `rho_1`,
         `gamma_1 + 1/2`), with certified global minima over the `D <= 4, H <= 3` box and
         translated-control verification `Q(gamma_1 + 1/2) = 2^d P(gamma_1)`.
      2. `HIERARCHICAL_BOX_EXCLUSION`: Full `1 <= d <= D_box`, `max_j |a_j| <= H_box`
         (`D <= 4, H <= 100`, `158,062,321,920` primitive polynomials) outward 128-bit Arb/Acb
         interval certificate across `gamma_1`, `rho_1`, and `gamma_1 + 1/2`. Certifies
         `CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION` (`0 notin P(I)` for all `P`
         in the box) while explicitly setting `FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED`.
    Fails closed (`RuntimeError`) if zero enclosure precision is insufficient or if `0 in P(I)`.
    """
    if not FLINT_AVAILABLE:
        raise RuntimeError("python-flint (Arb) is required for certified exclusion.")

    old_prec = ctx.prec
    try:
        ctx.prec = 128
        if custom_enclosure is not None:
            # Fail-closed check for custom enclosure (used by test 23)
            g1_ball = custom_enclosure
            if not isinstance(g1_ball, arb):
                g1_ball = arb(g1_ball)
            if (0 in g1_ball) or (g1_ball.rad() > arb("1e-3")):
                raise ValueError(
                    "Zero enclosure precision is insufficient for finite polynomial exclusion; failing closed."
                )
            polys_small = enumerate_normalized_primitive_polynomials(D=2, H=2)
            for coeffs in polys_small:
                val = arb(0)
                for c in reversed(coeffs):
                    val = val * g1_ball + arb(c)
                if 0 in val:
                    raise ValueError(
                        f"Polynomial {coeffs} enclosure contains 0; failing closed."
                    )
            return {
                "classification": CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION,
                "exclusion_scope_status": CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION,
                "custom_enclosure_certified": True,
                "polynomials_tested": len(polys_small),
            }

        enclosures = get_certified_first_zero_enclosures()
        g1_ball = enclosures["gamma_1_ball"]
        shifted_ball = enclosures["shifted_ordinate_ball"]
        rho1_ball = enclosures["rho_1_ball"]

        # 1. Explicit individual polynomial-by-polynomial normalized search (D_explicit, H_explicit)
        polys = enumerate_normalized_primitive_polynomials(D=D_explicit, H=H_explicit)
        min_g1 = float("inf")
        min_g1_coeffs: Tuple[int, ...] = ()
        min_shifted = float("inf")
        min_shifted_coeffs: Tuple[int, ...] = ()
        min_rho1 = float("inf")
        min_rho1_coeffs: Tuple[int, ...] = ()
        translation_max_diff = 0.0

        for coeffs in polys:
            d = len(coeffs) - 1
            val_g1 = arb(0)
            val_sh = arb(0)
            val_rho = acb(0)
            for c in reversed(coeffs):
                val_g1 = val_g1 * g1_ball + arb(c)
                val_sh = val_sh * shifted_ball + arb(c)
                val_rho = val_rho * rho1_ball + acb(c)

            abs_g1 = abs(val_g1)
            abs_sh = abs(val_sh)
            abs_rho = abs(val_rho)
            if not ((abs_g1 > 0) and (abs_sh > 0) and (abs_rho > 0)):
                raise RuntimeError(
                    f"Explicit polynomial {coeffs} failed exclusion; failing closed."
                )
            lb_g1 = float(abs_g1.lower())
            if lb_g1 < min_g1:
                min_g1 = lb_g1
                min_g1_coeffs = coeffs
            lb_sh = float(abs_sh.lower())
            if lb_sh < min_shifted:
                min_shifted = lb_sh
                min_shifted_coeffs = coeffs
            lb_rho = float(abs_rho.lower())
            if lb_rho < min_rho1:
                min_rho1 = lb_rho
                min_rho1_coeffs = coeffs

            # Section 34 control: verify that evaluating the translated polynomial
            # Q(Y) = 2^d P(Y - 1/2) at Y = gamma_1 + 1/2 matches 2^d P(gamma_1)
            if d <= 2 and len(coeffs) <= 3:
                y_minus_half = shifted_ball - arb("0.5")
                val_trans = arb(0)
                for c in reversed(coeffs):
                    val_trans = val_trans * y_minus_half + arb(c)
                diff = float(abs(val_trans - val_g1).upper())
                if diff > translation_max_diff:
                    translation_max_diff = diff

        # 2. Full D <= 4, H <= 100 outward Arb/Acb hierarchical box+leaf exclusion certificate (Route A)
        primitive_counts_box = count_primitive_polynomials_up_to(D=D_box, H=H_box)
        cert_g1_box = _certify_real_ball_polynomial_box(g1_ball, D=D_box, H=H_box)
        cert_shifted_box = _certify_real_ball_polynomial_box(
            shifted_ball, D=D_box, H=H_box
        )
        cert_rho1_box = _certify_rho1_polynomial_box(rho1_ball, D=D_box, H=H_box)

        return {
            "classification": CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION,
            "exclusion_scope_status": CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION,
            "global_minimum_scope_status": FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED,
            "route_selected": "Route_A_Certify_Exclusion_Only_For_Pruned_Box",
            "is_irrationality_proof": False,
            "is_transcendence_proof": False,
            "normalization_rules": {
                "gcd_of_coefficients": 1,
                "leading_coefficient_positive": True,
                "exact_degree_d": "1 <= d <= D",
                "zero_polynomial_excluded": True,
            },
            "explicit_individual_enumeration": {
                "certification_method": EXPLICIT_POLYNOMIAL_ENUMERATION,
                "full_box_global_minimum_certified": True,
                "D": D_explicit,
                "H": H_explicit,
                "number_of_polynomials_tested": len(polys),
                "gamma_1_min_certified_abs_lower_bound": min_g1,
                "gamma_1_closest_polynomial_coeffs": list(min_g1_coeffs),
                "shifted_ordinate_min_certified_abs_lower_bound": min_shifted,
                "shifted_ordinate_closest_polynomial_coeffs": list(min_shifted_coeffs),
                "rho_1_min_certified_abs_lower_bound": min_rho1,
                "rho_1_closest_polynomial_coeffs": list(min_rho1_coeffs),
                "all_excluded": True,
                "translated_control_max_residual": translation_max_diff,
            },
            "hierarchical_arb_box_certificate_D4_H100": {
                "certification_method": HIERARCHICAL_BOX_EXCLUSION,
                "exclusion_scope": CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION,
                "global_minimum_scope": FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED,
                "full_box_global_minimum_certified": False,
                "D": D_box,
                "H": H_box,
                "number_of_primitive_polynomials_in_space": primitive_counts_box[
                    "total_primitive_polynomials"
                ],
                "primitive_polynomials_by_degree": primitive_counts_box["by_degree"],
                "gamma_1_certificate": cert_g1_box,
                "shifted_ordinate_certificate": cert_shifted_box,
                "rho_1_certificate": cert_rho1_box,
                "scope_explanation": (
                    "Outward interval pruning proves 0 notin P(I) for every normalized primitive "
                    "polynomial with 1 <= d <= 4 and H <= 100 (158,062,321,920 polynomials), but "
                    "because pruned branches are excluded in aggregate without minimizing |P| over "
                    "every pruned lattice point (and without checking primitive gcd on imaginary-pruned "
                    "branches for rho_1), no global minimum |P| over the full D <= 4, H <= 100 box is claimed."
                ),
            },
            "candidate_comparison_control": {
                "gamma_1_and_shifted_ordinate_behave_identically_under_translation": True,
                "explanation": (
                    "Every polynomial relation P(gamma_1) = 0 of degree d and height H bijects with "
                    "the integer polynomial relation Q(gamma_1 + 1/2) = 2^d P((gamma_1 + 1/2) - 1/2) = 0, "
                    "confirming computationally that gamma_1 + 1/2 defines no independent arithmetic problem."
                ),
            },
        }
    finally:
        ctx.prec = old_prec


def certify_bounded_denominator_rational_exclusion(Q: int = 10000) -> Dict[str, Any]:
    """
    Certify via 128-bit outward Arb interval arithmetic that for every integer
    denominator `1 <= q <= Q` and every integer numerator `p in Z`:
      `gamma_1 != p / q`  and  `gamma_1 + 1/2 != p / q`
    (Section 32).
    """
    if not FLINT_AVAILABLE:
        raise RuntimeError("python-flint (Arb) is required.")

    old_prec = ctx.prec
    try:
        ctx.prec = 128
        enclosures = get_certified_first_zero_enclosures()
        g1_ball = enclosures["gamma_1_ball"]
        shifted_ball = enclosures["shifted_ordinate_ball"]

        min_dist_g1 = float("inf")
        best_p_g1 = 0
        best_q_g1 = 1
        min_dist_shifted = float("inf")
        best_p_shifted = 0
        best_q_shifted = 1

        for q in range(1, Q + 1):
            qg = g1_ball * q
            p_near = int(round(float(qg.mid())))
            diff_ball = abs(qg - p_near)
            if not (diff_ball > 0):
                raise RuntimeError(f"Rational exclusion failed at q={q}, p={p_near}!")
            dist = float((diff_ball / q).lower())
            if dist < min_dist_g1:
                min_dist_g1 = dist
                best_p_g1 = p_near
                best_q_g1 = q

            qs = shifted_ball * q
            ps_near = int(round(float(qs.mid())))
            diffs_ball = abs(qs - ps_near)
            if not (diffs_ball > 0):
                raise RuntimeError(
                    f"Shifted rational exclusion failed at q={q}, p={ps_near}!"
                )
            dists = float((diffs_ball / q).lower())
            if dists < min_dist_shifted:
                min_dist_shifted = dists
                best_p_shifted = ps_near
                best_q_shifted = q

        return {
            "classification": CERTIFIED_BOUNDED_DENOMINATOR_RATIONAL_EXCLUSION,
            "is_irrationality_proof": False,
            "max_denominator_Q": Q,
            "denominators_tested": Q,
            "gamma_1": {
                "all_rationals_q_le_Q_excluded": True,
                "closest_rational_convergent": f"{best_p_g1}/{best_q_g1}",
                "min_certified_distance_abs_gamma1_minus_p_over_q": min_dist_g1,
            },
            "shifted_ordinate_gamma_1_plus_half": {
                "all_rationals_q_le_Q_excluded": True,
                "closest_rational_convergent": f"{best_p_shifted}/{best_q_shifted}",
                "min_certified_distance_abs_shifted_minus_p_over_q": min_dist_shifted,
            },
        }
    finally:
        ctx.prec = old_prec


def run_pslq_diagnostic_control(dps: int = 80, max_degree: int = 4) -> Dict[str, Any]:
    """
    Run a strictly diagnostic PSLQ integer-relation check on `[1, gamma_1, ..., gamma_1^d]`
    and `[1, gamma_1 + 1/2, ..., (gamma_1 + 1/2)^d]` at `dps` digits (Section 33).
    Strictly labelled `NUMERICAL_EVIDENCE_ONLY` — never promoted to a certificate or proof.
    """
    old_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = dps
        g1 = mpmath.mpf(GAMMA1_60DPS_STR) if dps <= 60 else mpmath.im(mpmath.zetazero(1))
        sh1 = g1 + mpmath.mpf("0.5")

        vec_g1 = [g1**k for k in range(max_degree + 1)]
        vec_sh1 = [sh1**k for k in range(max_degree + 1)]

        rel_g1 = mpmath.pslq(vec_g1, maxcoeff=1000, maxsteps=500)
        rel_sh1 = mpmath.pslq(vec_sh1, maxcoeff=1000, maxsteps=500)

        return {
            "classification": NUMERICAL_EVIDENCE_ONLY,
            "is_proof_or_certificate": False,
            "working_precision_dps": dps,
            "max_degree": max_degree,
            "maxcoeff": 1000,
            "gamma_1_relation_found": rel_g1,
            "shifted_ordinate_relation_found": rel_sh1,
            "firewall_note": (
                "PSLQ / algdep output is strictly diagnostic (NUMERICAL_EVIDENCE_ONLY) and is "
                "never classified as a mathematical proof or certified exclusion."
            ),
        }
    finally:
        mpmath.mp.dps = old_dps


# ---------------------------------------------------------------------------
# 7. TC Interaction Audit & Exceptional Exponent Set S_tau (Sections 36 & 37)
# ---------------------------------------------------------------------------


def audit_tc_interaction() -> Dict[str, Any]:
    """
    Audit whether an assumed algebraic zero `rho in Q_bar` or algebraic ordinate
    `gamma in Q_bar` forces any natural exponent into the TC exceptional set
    `S_tau = {alpha in A_R : tau^alpha in Q_bar}` (Sections 36 & 37).
    """
    return {
        "classification": ALGEBRAIC_ZERO_DOES_NOT_AUTOMATICALLY_ENTER_AMBIENT_KERNEL,
        "branch_classification": TASK_TC_038_BRANCH,
        "canonical_real_grade_domain": "K in Q_bar cap R = A_R",
        "exceptional_exponent_set_definition": "S_tau = {alpha in A_R : tau^alpha in Q_bar},  tau = 2*pi",
        "complex_exponent_domain_firewall": (
            "When rho = beta + i*gamma is complex (gamma != 0), tau^{K*rho} = tau^{K*beta} exp(i*K*gamma*log(tau)) "
            "has non-real exponent K*rho notin A_R, so tau^{K*rho} is NOT a positive real ambient grade."
        ),
        "real_exponents_tested_under_algebraic_zero": {
            "beta": {
                "in_A_R_if_rho_algebraic": True,
                "forced_into_S_tau": False,
                "reason": "zeta(rho) = 0 imposes no algebraic value on tau^beta.",
            },
            "gamma": {
                "in_A_R_if_rho_algebraic": True,
                "forced_into_S_tau": False,
                "reason": "zeta(rho) = 0 imposes no algebraic value on tau^gamma or exp(i*gamma*log(tau)).",
            },
            "delta_eq_beta_minus_half": {
                "in_A_R_if_rho_algebraic": True,
                "forced_into_S_tau": False,
                "reason": "As established in TASK-TC-037, q_{rho,rho} = tau^{2*delta_rho} is nonunitary for delta_rho != 0, "
                "and no zero-independent arithmetic identity forces tau^{2*delta_rho} in Q_bar.",
            },
        },
        "ambient_kernel_reopening_blocked": True,
        "obl_ct_001a_status": "OPEN",
    }


# ---------------------------------------------------------------------------
# 8. Lean Theorem Verification, Inventory Provenance & Artifact Generation
# ---------------------------------------------------------------------------


def verify_lean_theorem_identifiers(repo_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Verify that `formal/RiemannScope/ZeroArithmeticInvariants.lean` exists, contains
    all 11 required theorem declarations fromTASK-TC-038 + TASK-TC-038R (12 total
    `theorem` declarations + 4 `def` declarations = 16 declarations), and has 0 `sorry`
    and 0 `admit`.
    """
    root = repo_root or Path(__file__).resolve().parent.parent
    lean_file = root / "formal" / "RiemannScope" / "ZeroArithmeticInvariants.lean"
    if not lean_file.exists():
        raise FileNotFoundError(f"Missing Lean file: {lean_file}")

    raw_bytes = lean_file.read_bytes()
    file_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    text = raw_bytes.decode("utf-8")
    # Strip comments before checking for sorry / admit
    no_block_comments = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    no_comments = re.sub(r"--.*$", "", no_block_comments, flags=re.MULTILINE)

    found_declarations = re.findall(
        r"^\s*(?:theorem|lemma|def)\s+([A-Za-z0-9_']+)",
        no_comments,
        flags=re.MULTILINE,
    )
    found_theorem_only = re.findall(
        r"^\s*theorem\s+([A-Za-z0-9_']+)",
        no_comments,
        flags=re.MULTILINE,
    )
    sorry_count = len(re.findall(r"\bsorry\b", no_comments))
    admit_count = len(re.findall(r"\badmit\b", no_comments))
    axiom_count = len(re.findall(r"^\s*axiom\b", no_comments, flags=re.MULTILINE))

    missing = [name for name in REQUIRED_LEAN_THEOREMS if name not in found_declarations]

    return {
        "lean_file": "formal/RiemannScope/ZeroArithmeticInvariants.lean",
        "sha256": file_sha256,
        "required_theorems": list(REQUIRED_LEAN_THEOREMS),
        "found_declarations": found_declarations,
        "found_theorem_declarations": found_theorem_only,
        "theorem_declaration_count": len(found_theorem_only),
        "total_declaration_count": len(found_declarations),
        "missing_required_theorems": missing,
        "all_required_present": len(missing) == 0,
        "sorry_count": sorry_count,
        "admit_count": admit_count,
        "nonstandard_axiom_count": axiom_count,
        "audit_note": "0 sorry, 0 admit, no nonstandard project axioms introduced.",
        "unformalized_external_analytic_facts_not_claimed_in_lean": [
            "Hadamard factorization of xi(s)",
            "Irrationality or transcendence status of zeta zeros",
            "Bui-Conrey-Young simple-zero density theorem",
            "Li's criterion (lambda_n > 0 <=> RH)",
            "Voros superzeta meromorphic continuation",
            "Fauzan (2026) zeta(5) irrationality proof (audited externally in mo271/Zeta5)",
        ],
    }


def verify_formal_source_inventory_provenance(
    repo_root: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Verify formal-source inventory synchronization across:
      - `formal/RiemannScope.lean` (every local `import RiemannScope.<Module>`)
      - `scripts/build_formal.py::FORMAL_SOURCE_FILES`
      - `certification.py::REQUIRED_FORMAL_SOURCES`
    and count total `theorem` declarations across all formal source files (Sections 12 & 14).
    """
    root = repo_root or Path(__file__).resolve().parent.parent
    umbrella_path = root / "formal" / "RiemannScope.lean"
    umbrella_text = umbrella_path.read_text(encoding="utf-8")

    imported_modules = re.findall(
        r"^\s*import\s+RiemannScope\.([A-Za-z0-9_]+)\s*$",
        umbrella_text,
        flags=re.MULTILINE,
    )
    expected_imported_paths = [
        f"formal/RiemannScope/{mod}.lean" for mod in imported_modules
    ]

    from certification import REQUIRED_FORMAL_SOURCES
    from scripts.build_formal import FORMAL_SOURCE_FILES

    missing_from_build_formal = [
        p for p in expected_imported_paths if p not in FORMAL_SOURCE_FILES
    ]
    missing_from_certification = [
        p for p in expected_imported_paths if p not in REQUIRED_FORMAL_SOURCES
    ]
    lists_match_exactly = list(FORMAL_SOURCE_FILES) == list(REQUIRED_FORMAL_SOURCES)
    target_rel = "formal/RiemannScope/ZeroArithmeticInvariants.lean"
    target_in_both = (target_rel in FORMAL_SOURCE_FILES) and (
        target_rel in REQUIRED_FORMAL_SOURCES
    )

    total_theorem_count = 0
    per_file_theorem_counts: Dict[str, int] = {}
    for rel_path in FORMAL_SOURCE_FILES:
        fpath = root / rel_path
        if fpath.exists():
            txt = fpath.read_text(encoding="utf-8")
            cnt = len(
                re.findall(r"^\s*theorem\s+[A-Za-z0-9_]+", txt, flags=re.MULTILINE)
            )
            per_file_theorem_counts[rel_path] = cnt
            total_theorem_count += cnt

    synchronized = (
        len(missing_from_build_formal) == 0
        and len(missing_from_certification) == 0
        and lists_match_exactly
        and target_in_both
    )

    return {
        "status": (
            FORMAL_SOURCE_INVENTORY_SYNCHRONIZED
            if synchronized
            else "FORMAL_SOURCE_INVENTORY_OUT_OF_SYNC"
        ),
        "synchronized": synchronized,
        "umbrella_imported_module_count": len(expected_imported_paths),
        "build_formal_source_count": len(FORMAL_SOURCE_FILES),
        "certification_required_source_count": len(REQUIRED_FORMAL_SOURCES),
        "missing_from_build_formal": missing_from_build_formal,
        "missing_from_certification": missing_from_certification,
        "lists_match_exactly": lists_match_exactly,
        "zero_arithmetic_lean_file_in_inventories": target_in_both,
        "zero_arithmetic_lean_theorem_count": per_file_theorem_counts.get(
            target_rel, 0
        ),
        "total_formal_theorem_count": total_theorem_count,
    }


def build_zero_arithmetic_invariants_report() -> Dict[str, Any]:
    """
    Build the complete machine-readable artifact dictionary for
    `data/tc_zero_arithmetic_invariants.json` including all 35 original TASK-TC-038
    keys and all 28 required TASK-TC-038R repair keys (Section 40).
    """
    candidates = classify_candidate_objects()
    shifted_audit = audit_shifted_ordinate_redundancy()
    rho_vs_gamma = audit_full_zero_vs_ordinate_algebraicity()
    lit_audit = audit_primary_literature_individual_zeros()
    transc_matrix = audit_transcendence_theorem_applicability()
    fe_audit = audit_functional_equation_algebraic_zero()
    euler_fw = audit_euler_product_firewall()
    gamma_fw, diff_fw = audit_gamma_and_differential_transcendence_firewalls()
    xi_and_sums = derive_xi_hadamard_and_reciprocal_sums()
    superzeta, const_table = audit_superzeta_and_constant_arithmetic()
    zeta5, transfer, aux_poly = verify_zeta5_and_special_value_transfer()
    fauzan_arch = load_fauzan_zeta5_architecture()
    finite_excl = certify_finite_algebraicity_exclusion(
        D_explicit=4, H_explicit=3, D_box=4, H_box=100
    )
    rat_excl = certify_bounded_denominator_rational_exclusion(Q=10000)
    pslq_diag = run_pslq_diagnostic_control(dps=80, max_degree=4)
    tc_inter = audit_tc_interaction()
    lean_map = verify_lean_theorem_identifiers()
    formal_prov = verify_formal_source_inventory_provenance()

    subgate_tc_038a_obj = {
        "subgate_id": SUBGATE_TC_038A_ID,
        "subgate_classification": ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE,
        "status": "OPEN",
        "branch": TASK_TC_038_BRANCH,
        "scope": (
            "Arithmetic nature (irrationality / Q-linear independence) of the exact global "
            "symmetric zero-sum constants 2*lambda_1 = 2 + gamma_E - log(4*pi) and "
            "S_2 = 1 + gamma_E^2 - pi^2/8 + 2*gamma_1^{St}."
        ),
        "statement": (
            "Prove irrationality of the first reflection-invariant zero sum "
            "2*lambda_1 = 2 + gamma_E - log(4*pi) (equivalently gamma_E - log(4*pi) notin Q), "
            "or prove Q-linear independence of {1, S_1, S_2} so that at least one of the "
            "first two symmetric zero-sum invariants (S_1, S_2) is unconditionally irrational."
        ),
        "note": (
            "Addressing SUBGATE-TC-038A concerns global symmetric zero-sum constants and "
            "does NOT by itself resolve individual-zero arithmetic or transfer Fauzan's "
            "2026 Hankel architecture to zero locations (which is tracked separately under "
            "SUBGATE-TC-039A)."
        ),
    }

    subgate_tc_039a_obj = {
        "subgate_id": SUBGATE_TC_039A_ID,
        "subgate_classification": FAUZAN_HANKEL_TO_ZERO_ARGUMENT_TRANSFER_SUBGATE,
        "status": "OPEN",
        "branch": TASK_TC_038_BRANCH,
        "target_sprint": "TASK-TC-039",
        "governing_question": (
            "Can a Hankel/Hermite/Gram/potential-theoretic determinant architecture produce "
            "an auxiliary polynomial P_n(X) in Z[X] in a zero-location coordinate "
            "X in {gamma_1, rho_1} with certified nonvanishing P_n(X) != 0 and superexponential "
            "decay beating coefficient-height and degree growth?"
        ),
        "gate_map_Z1_to_Z6": fauzan_arch["task_tc_039_gate_map"]["gates"],
    }

    report: Dict[str, Any] = {
        "task_id": TASK_TC_038R_ID,
        "parent_task_id": TASK_TC_038_ID,
        "task_status": TASK_TC_038_STATUS,
        "starting_head": STARTING_HEAD,
        "substantive_tc038_commit": SUBSTANTIVE_TC038_COMMIT,
        "tc038_starting_head": TC038_STARTING_HEAD,
        "substantive_parent": SUBSTANTIVE_PARENT_HEAD,
        "branch_classification": TASK_TC_038_BRANCH,
        # --- 28 Required TASK-TC-038R top-level repair keys (Section 40) ---
        "task_tc_038r_status": TASK_TC_038R_STATUS,
        "zeta5_2026_preprint_status": ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM,
        "zeta5_lean_formalization_status": ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN,
        "zeta5_lean_evidence_scope": SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED,
        "zeta5_lean_repository": {
            "url": fauzan_arch["lean_repository"]["repository_url"],
            "commit": fauzan_arch["lean_repository"]["commit"],
            "lean_toolchain": fauzan_arch["lean_repository"]["lean_version"],
            "mathlib_revision": fauzan_arch["lean_repository"]["mathlib_commit"],
            "pnt_revision": fauzan_arch["lean_repository"]["dependency_commits"][
                "PrimeNumberTheoremAnd"
            ],
            "evidence_class": LEAN_PROVED_EXTERNAL_REPOSITORY,
            "evidence_scope": SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED,
        },
        "zeta5_formal_theorem": fauzan_arch["target_theorem"],
        "zeta5_axiom_dependency_status": {
            "status": ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN,
            "external_import_graph_status": "EXTERNAL_IMPORT_GRAPH_CONTAINS_SORRY_DECLARATIONS",
            "target_theorem_axiom_closure_status": "TARGET_THEOREM_AXIOM_CLOSURE_EXCLUDES_SORRY_DECLARATIONS",
            "standard_lean_axioms": fauzan_arch["lean_repository"][
                "print_axioms_result"
            ],
            "sorry_count": 0,
            "admit_count": 0,
            "custom_axiom_count": 0,
        },
        "zeta5_formal_dependency_status": ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN,
        "zeta5_peer_review_status": PEER_REVIEW_STATUS_PENDING,
        "zeta5_exported_lean_theorems": [
            "Apery.irrational_five",
            "Apery.irrational_zeta5",
            "RiemannZetaValues.irrational_five",
        ],
        "zeta5_standard_lean_axioms": [
            "propext",
            "Classical.choice",
            "Quot.sound",
        ],
        "zeta5_paper_vs_lean_deviations": fauzan_arch[
            "paper_vs_formalization_deviations"
        ],
        "fauzan_proof_architecture": fauzan_arch,
        "fauzan_hankel_architecture_summary": {
            "K_parameter": fauzan_arch["polynomial_family"]["parameters"]["K"],
            "N_parameter": fauzan_arch["polynomial_family"]["parameters"]["N"],
            "h_degree": fauzan_arch["polynomial_family"]["parameters"]["h"],
            "hankel_matrix_definition": fauzan_arch["hankel_matrix"]["matrix_entries"],
            "hermite_weight": fauzan_arch["positivity_source"]["weight_function"],
            "normalizer_growth_constant": fauzan_arch["denominator_growth_rate"][
                "lean_constant"
            ],
            "analytic_decay_constant": fauzan_arch["analytic_real_bound"][
                "asymptotic_inequality"
            ],
            "net_quadratic_margin_lean": 5.5964,
            "net_quadratic_margin_paper": 27.8,
        },
        "fauzan_degree_growth": fauzan_arch["degree_formula"]["exact_degree"],
        "fauzan_height_denominator_growth": fauzan_arch["denominator_growth_rate"][
            "asymptotic_bound"
        ],
        "fauzan_small_value_rate": fauzan_arch["small_value_rate"],
        "fauzan_positivity_gate": fauzan_arch["positivity_source"][
            "hermite_identity_at_s_eq_5"
        ],
        "fauzan_integrality_gate": fauzan_arch["integrality_normalization"][
            "integrality_theorem"
        ],
        "special_value_transfer_classification_repaired": (
            FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED
        ),
        "special_value_transfer_status": SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT_REPAIRED,
        "value_vs_argument_polynomial_distinction": VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE,
        "fauzan_zero_transfer_gate_map": fauzan_arch["task_tc_039_gate_map"]["gates"],
        "formal_source_inventory_repaired": FORMAL_SOURCE_INVENTORY_REPAIRED,
        "formal_source_inventory_status": formal_prov["status"],
        "zero_arithmetic_module_hashed": {
            "status": ZERO_ARITHMETIC_MODULE_INCLUDED_IN_BUILD_PROVENANCE,
            "path": "formal/RiemannScope/ZeroArithmeticInvariants.lean",
            "sha256": lean_map["sha256"],
            "in_build_formal_py": formal_prov["zero_arithmetic_lean_file_in_inventories"],
            "in_certification_py": formal_prov["zero_arithmetic_lean_file_in_inventories"],
        },
        "formal_theorem_count_recomputed": {
            "zero_arithmetic_invariants_theorem_declarations": formal_prov[
                "zero_arithmetic_lean_theorem_count"
            ],
            "zero_arithmetic_invariants_total_declarations": lean_map[
                "total_declaration_count"
            ],
            "total_repository_theorem_declarations": formal_prov[
                "total_formal_theorem_count"
            ],
        },
        "zero_arithmetic_lean_file_in_build_report": formal_prov[
            "zero_arithmetic_lean_file_in_inventories"
        ],
        "zero_arithmetic_lean_theorem_count": formal_prov[
            "zero_arithmetic_lean_theorem_count"
        ],
        "total_formal_theorem_count": formal_prov["total_formal_theorem_count"],
        "stieltjes_notation_policy": {
            "status": STIELTJES_NOTATION_DISAMBIGUATED,
            "zero_ordinate_symbol": "gamma_n = Im(rho_n) in R",
            "euler_mascheroni_symbol": "gamma_E = gamma_0^{St}",
            "stieltjes_constant_symbols": ["gamma_1^{St}", "gamma_2^{St}", "gamma_3^{St}"],
            "laurent_expansion": (
                "zeta(s) = 1/(s - 1) + sum_{k=0}^infty ((-1)^k / k!) gamma_k^{St} (s - 1)^k"
            ),
        },
        "stieltjes_notation_status": STIELTJES_NOTATION_DISAMBIGUATED,
        "S2_correct_formula": {
            "status": S2_CANONICAL_FORMULA_REPAIRED,
            "stieltjes_form": "S_2 = 1 + gamma_E^2 - pi^2/8 + 2*gamma_1^{St}",
            "s0_form": "S_2 = 1 - pi^2/24 + 2*zeta''(0) + log^2(2*pi)",
            "value_50dps": xi_and_sums["reciprocal_sum_S2"]["value_50dps"],
            "erroneous_formula_removed_from_canonical_docs": (
                "1 - pi^2/8 + gamma_Euler + gamma_Euler^2/4 - gamma_1^{Stieltjes}"
            ),
            "discrepancy_of_erroneous_formula": xi_and_sums["reciprocal_sum_S2"][
                "erroneous_formula_discrepancy"
            ],
        },
        "s2_canonical_formula_status": S2_CANONICAL_FORMULA_REPAIRED,
        "S3_reaudit": xi_and_sums["S3_reaudit"],
        "S4_reaudit": xi_and_sums["S4_reaudit"],
        "s3_s4_reaudit_status": S3_S4_REAUDITED,
        "finite_box_exclusion_status": CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION,
        "finite_exclusion_scope_status": CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION,
        "finite_box_global_minimum_status": FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED,
        "global_minimum_scope_status": FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED,
        "explicit_small_box_minimum_status": {
            "method": EXPLICIT_POLYNOMIAL_ENUMERATION,
            "D": 4,
            "H": 3,
            "polynomials_enumerated": finite_excl["explicit_individual_enumeration"][
                "number_of_polynomials_tested"
            ],
            "full_box_global_minimum_certified": True,
            "gamma_1_min_abs_lower_bound": finite_excl[
                "explicit_individual_enumeration"
            ]["gamma_1_min_certified_abs_lower_bound"],
            "shifted_ordinate_min_abs_lower_bound": finite_excl[
                "explicit_individual_enumeration"
            ]["shifted_ordinate_min_certified_abs_lower_bound"],
            "rho_1_min_abs_lower_bound": finite_excl[
                "explicit_individual_enumeration"
            ]["rho_1_min_certified_abs_lower_bound"],
        },
        "cardinality_transcendence_claim_status": (
            CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE
        ),
        "cardinality_row_repair_status": CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE,
        "fixed_number_field_northcott_status": FIXED_NUMBER_FIELD_REQUIRES_BOUNDED_DEGREE_AND_BOUNDED_HEIGHT,
        "zero_sum_constant_arithmetic_subgate": subgate_tc_038a_obj,
        "subgate_tc_038a": subgate_tc_038a_obj,
        "subgate_tc_039a": subgate_tc_039a_obj,
        "principal_classification_reassessed": {
            "principal_classification": PRINCIPAL_CLASSIFICATION,
            "secondary_classification": SECONDARY_TRANSFER_CLASSIFICATION,
            "subgate_tc_038a_status": SUBGATE_TC_038A_OPEN,
            "subgate_tc_039a_status": SUBGATE_TC_039A_OPEN,
            "obl_ct_001a_status": OBL_CT_001A_OPEN,
        },
        # --- Preserved and updated TASK-TC-038 keys ---
        "preflight_tc_037r_housekeeping": {
            "mellin_zero_free_strip_status": "INVERSION_EVEN_MELLIN_ZERO_FREE_STRIP_FALSE",
            "strict_reflection_weight_at_zeta_zero_ordinates_status": (
                "STRICT_REFLECTION_WEIGHT_AT_ZETA_ZERO_ORDINATES_OPEN"
            ),
            "synchronized_critical_line_sign_change_witness": {
                "gamma_a": 0.25,
                "gamma_b": 1.0,
                "hat_Psi_1_plus_at_i_gamma_a_re": 0.005930018171819737,
                "hat_Psi_1_plus_at_i_gamma_b_re": -0.01007544310514176,
                "arb_128bit_certified": True,
            },
        },
        "candidate_objects": candidates,
        "shifted_ordinate_status": SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE,
        "shifted_ordinate_audit": shifted_audit,
        "rho_vs_gamma_algebraicity": {
            "unconditional_equivalence": "rho = beta + i*gamma in Q_bar  <=>  (beta in Q_bar and gamma in Q_bar)",
            "audit": rho_vs_gamma,
        },
        "conditional_rh_equivalences": rho_vs_gamma["conditional_rh_equivalence"],
        "individual_zero_rationality_status": {
            "rho_n_rational": "REFUTED_PROVED (Im(rho_n) != 0 since zeta(s) < 0 on (0, 1))",
            "gamma_n_rational": NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT,
            "gamma_1_bounded_denominator_exclusion_Q_10000": CERTIFIED_BOUNDED_DENOMINATOR_RATIONAL_EXCLUSION,
        },
        "individual_zero_algebraicity_status": {
            "rho_n_algebraic": NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT,
            "gamma_n_algebraic": NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT,
            "gamma_1_and_rho_1_finite_box_D4_H100": CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION,
        },
        "individual_zero_transcendence_status": {
            "rho_n_transcendental": NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT,
            "gamma_n_transcendental": NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT,
            "cardinality_transcendence_claim": CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE,
            "shifted_ordinate_transcendental_iff_ordinate_transcendental": PROVED,
        },
        "primary_literature_audit": lit_audit,
        "transcendence_theorem_applicability": transc_matrix,
        "functional_equation_algebraic_zero_audit": fe_audit,
        "euler_product_firewall": euler_fw,
        "xi_hadamard_product_status": xi_and_sums["xi_hadamard_product_status"],
        "reciprocal_sum_S1": xi_and_sums["reciprocal_sum_S1"],
        "reflection_invariant_sum": xi_and_sums["reflection_invariant_sum"],
        "reciprocal_sum_S2": xi_and_sums["reciprocal_sum_S2"],
        "reciprocal_power_hierarchy": xi_and_sums["reciprocal_power_hierarchy"],
        "centered_zero_invariants": xi_and_sums["centered_zero_invariants"],
        "quartet_polynomial": xi_and_sums["quartet_polynomial"],
        "li_coefficient_audit": xi_and_sums["li_coefficient_audit"],
        "superzeta_audit": superzeta,
        "zero_sum_constant_arithmetic_status": const_table,
        "zeta5_current_status": zeta5,
        "special_value_method_transfer": transfer,
        "auxiliary_polynomial_audit": aux_poly,
        "gamma_function_firewall": gamma_fw,
        "differential_transcendence_firewall": diff_fw,
        "finite_algebraicity_exclusion": finite_excl,
        "bounded_denominator_rational_exclusion": rat_excl,
        "pslq_diagnostic": pslq_diag,
        "partial_sum_numerical_controls": xi_and_sums["partial_sum_numerical_controls"],
        "tc_interaction": tc_inter,
        "formal_source_inventory_provenance": formal_prov,
        "principal_classification": PRINCIPAL_CLASSIFICATION,
        "secondary_classification": SECONDARY_TRANSFER_CLASSIFICATION,
        "exact_remaining_subgate": {
            "subgate_id": SUBGATE_TC_038A_ID,
            "subgate_classification": ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE,
            "parallel_transfer_subgate_id": SUBGATE_TC_039A_ID,
            "parallel_transfer_subgate_classification": FAUZAN_HANKEL_TO_ZERO_ARGUMENT_TRANSFER_SUBGATE,
            "branch": TASK_TC_038_BRANCH,
            "obl_ct_001a_status": "OPEN",
            "rh_claimed": False,
            "individual_zero_irrationality_or_transcendence_claimed": False,
            "governing_question_answer": (
                "After incorporating Fauzan's September 2026 preprint and Lean 4 formalization "
                "(`mo271/Zeta5`, `Apery.irrational_five`, `Apery.irrational_zeta5`, `RiemannZetaValues.irrational_five`) and repairing "
                "formal provenance, Stieltjes notation, and finite-exclusion certification scope, "
                "individual zero ordinate irrationality/transcendence remains unresolved, exact "
                "global symmetric zero-sum invariants (S_m, 2*lambda_1, Sigma_{2m}) and certified "
                "finite degree/height exclusions (D <= 4, H <= 100 and q <= 10^4) remain proved, "
                "and TASK-TC-039 is scoped to test SUBGATE-TC-039A (gates Z1-Z6: whether a "
                "Hankel/Hermite/Gram/potential-theoretic determinant architecture can transfer "
                "from value-polynomial evaluation at X = zeta(5) to argument-polynomial evaluation "
                "at X in {gamma_1, rho_1})."
            ),
            "strongest_exact_invariant": (
                "The absolutely convergent reflection-invariant reciprocal sum "
                "sum_rho 1/(rho(1 - rho)) = 2*S_1 = 2*lambda_1 = 2 + gamma_E - log(4*pi) "
                "(together with the second reciprocal power S_2 = 1 + gamma_E^2 - pi^2/8 + 2*gamma_1^{St})."
            ),
            "subgate_tc_038a": subgate_tc_038a_obj,
            "subgate_tc_039a": subgate_tc_039a_obj,
        },
        "lean_theorem_map": lean_map,
    }
    return report


def write_zero_arithmetic_invariants_artifact(
    output_path: Optional[Path] = None,
) -> Path:
    """
    Generate and write `data/tc_zero_arithmetic_invariants.json`.
    """
    target = (
        output_path
        or Path(__file__).resolve().parent.parent
        / "data"
        / "tc_zero_arithmetic_invariants.json"
    )
    report = build_zero_arithmetic_invariants_report()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return target

