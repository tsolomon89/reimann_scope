r"""Minimal Rank-Two Trinomial Kernel, Relation-Space Rigidity, and Sparse Orbit Theorems.

TASK-TC-030 / TASK-TC-030R: Classification, relation-space rigidity, and certified sparse
exclusion of the first genuinely unresolved ambient realization kernel support:
    a0 + a1 * tau^alpha + a2 * tau^beta = 0
where a0, a1, a2 in Q_bar^\times, alpha, beta in A_R, and alpha / beta not in Q.

Mathematical Hierarchy:
- r = 0: Trivial coefficient cancellation.
- r = 1: Classified by S_tau (dim_Q S_tau <= 1 via Baker / Gelfond-Schneider).
- Support size 1: a0 * tau^K0 = 0 is impossible for a0 != 0 and tau > 0.
- Support size 2: Factoring tau^K0 reduces to tau^theta in Q_bar (rank-one S_tau).
- Support size 3:
    - Affine rank 1 (alpha/beta in Q): reduces to one-variable Laurent polynomial,
      hence to S_tau.
    - Affine rank 2 (alpha/beta not in Q): FIRST_OPEN_KERNEL_SUPPORT.

Structural Theorems & Evidence Alignment:
1. RANK_TWO_TRINOMIAL_RELATION_SPACE_AT_MOST_ONE_DIMENSIONAL:
   Two independent relations force (1, X, Y) into a 1-dimensional nullspace over Q_bar,
   forcing X, Y in Q_bar via Cramer's rule. This requires alpha, beta in S_tau.
   By external Gelfond-Schneider (Baker 1975), dim_Q S_tau <= 1, contradicting Q-independence.
   Evidence: PROVED_PAPER_DERIVATION + PROVED_WITH_EXTERNAL_GELFOND_SCHNEIDER.
   Lean Core: trinomial_two_relations_cramer proves coordinate solvability for Delta_0 != 0.
2. PAIRWISE_EXCEPTIONAL_DIRECTIONS_EXCLUDED:
   A nondegenerate relation forces alpha, beta, beta-alpha outside S_tau.
   Evidence: LEAN_PROVED_SOLVING_IDENTITIES feeding PROVED_PAPER_DERIVATION + EXTERNAL_GELFOND_SCHNEIDER.
3. TRINOMIAL_COEFFICIENTS_REAL_NORMALIZABLE:
   Direct elementary proof: complex conjugation and dim <= 1 yield conj(a_j) = lambda * a_j with
   |lambda| = 1. Choosing mu = 1 + lambda (or mu = I if lambda = -1) normalizes all coefficients
   into A_R = Q_bar \cap R.
   Evidence: PROVED_PAPER_DERIVATION.
4. MIXED_SIGN_NECESSARY:
   For positive generators X, Y > 0 and real coefficients, same-sign coefficients
   cannot sum to zero. Every relation is orientable into one of:
   - Y = u + v * X (u, v in A_R^{>0})
   - X = u + v * Y (u, v in A_R^{>0})
   - 1 = u * X + v * Y (u, v in A_R^{>0})
   Evidence: LEAN_PROVED (trinomial_same_sign_pos_impossible, trinomial_same_sign_neg_impossible).
5. THREE_CONSECUTIVE_DILATION_ORBIT_RIGIDITY:
   For f(n) = a0 + a1 * X^n + a2 * Y^n, det(M_n) = X^n * Y^n * (X - 1) * (Y - 1) * (Y - X) != 0.
   Thus f(n) = f(n+1) = f(n+2) = 0 implies a0 = a1 = a2 = 0.
   Evidence: LEAN_PROVED (trinomial_three_consecutive_orbit_rigidity).
6. NO_CANONICAL_ORBIT_VANISHING_PROPAGATION:
   f(1) = 0 does not force f(2) = 0, f(3) = 0, or any further orbit vanishing.
7. MULTIPLICATIVE_GROUP_THEOREMS:
   - Base group: Gamma_0 = <X, Y> \cong Z^2 (rank 2).
   - Solution group for (u, v): Gamma_0 x Gamma_0 (rank 4).
   - Diagonal orbit: Delta_{alpha, beta} (rank 1).
   - By Laurent (1984) and Evertse-Schlickewei-Schmidt (2002), solutions for fixed coefficients
     are FINITE. However, FINITE_DOES_NOT_IMPLY_EMPTY; existence of one relation remains OPEN.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import flint
from flint import arb, ctx
import sympy as sp
from sympy import Rational, Integer, sqrt, Symbol, sympify, I

from tc.ambient_kernel import (
    expr_to_arb,
    compute_rational_support_rank,
    CANONICAL_MINIMAL_RANK_TWO_OPEN_INSTANCE,
)


# Canonical Instance Definitions
CANONICAL_INSTANCE_BASE_ONE = "BASE_ONE_INSTANCE"
CANONICAL_INSTANCE_RADICAL_PAIR = "RADICAL_PAIR_INSTANCE"

# Support Universe Constants for Degree <= 3 Box
SUPPORT_BOX_TOTAL_MONOMIALS = 10  # 1, X, Y, X^2, XY, Y^2, X^3, X^2Y, XY^2, Y^3
SUPPORT_BOX_TOTAL_THREE_MONOMIAL_SUBSETS = 120  # comb(10, 3)
SUPPORT_BOX_CONSTANT_ANCHORED_SUPPORTS = 36  # comb(9, 2)
SUPPORT_BOX_AFFINE_RANK_TWO_SUPPORTS = 30
SUPPORT_BOX_AFFINE_RANK_ONE_CONTROLS = 6
NORMALIZED_COEFFICIENTS_PER_SUPPORT = 2523  # height H=10 primitive mixed-sign triples


@dataclass(frozen=True)
class MinimalSupportClassification:
    support_size: int
    is_possible: bool
    affine_support_rank: int
    classification_code: str
    reduction_target: str
    description: str


@dataclass(frozen=True)
class SignOrientation:
    orientation_type: str  # "Y_AFFINE_X", "X_AFFINE_Y", "ONE_AFFINE_XY"
    u: sp.Expr
    v: sp.Expr
    description: str


@dataclass(frozen=True)
class RealNormalizationResult:
    original_coeffs: Tuple[sp.Expr, sp.Expr, sp.Expr]
    lambda_val: sp.Expr
    mu_val: sp.Expr
    normalized_coeffs: Tuple[sp.Expr, sp.Expr, sp.Expr]
    is_real_normalized: bool
    proof_method: str = "DIRECT_ELEMENTARY_CONJUGATE_PHASE_NORMALIZATION"


@dataclass(frozen=True)
class DilationOrbitResult:
    n_values: List[int]
    orbit_values: List[sp.Expr]
    is_three_consecutive_rigid: bool
    determinant_val: sp.Expr


@dataclass(frozen=True)
class RelationSpaceDimensionBound:
    alpha: sp.Expr
    beta: sp.Expr
    is_rationally_independent: bool
    assumes_external_gelfond_schneider: bool
    dimension_bound: int
    theorem_conclusion: str
    evidence_class: str
    status: str
    description: str


@dataclass(frozen=True)
class CertifiedTrinomialExclusionResult:
    canonical_instance: str
    alpha_expr: sp.Expr
    beta_expr: sp.Expr
    max_degree_D: int
    max_height_H: int
    all_three_monomial_subsets_in_box: int
    constant_anchored_supports_tested: int
    affine_rank_two_supports_tested: int
    affine_rank_one_control_supports: int
    normalized_coefficients_per_support: int
    rank_two_candidates_certified: int
    rank_one_control_candidates_certified: int
    total_candidates_certified: int
    smallest_certified_distance: float
    smallest_candidate: Dict[str, Any]
    precision_bits: int
    runtime_seconds: float
    certificate_scope: str
    classification: str


def canonicalize_group_algebra_terms(
    terms: List[Tuple[Any, Any]]
) -> List[Tuple[sp.Expr, sp.Expr]]:
    r"""Canonicalize a formal sum \sum a_j [K_j] in the group algebra \overline{\mathbb{Q}}[\mathbb{A}_\mathbb{R}].

    Steps:
    1. Converts each coefficient and grade to exact symbolic form (sp.sympify).
    2. Groups all terms having the same grade (via sp.simplify(g1 - g2) == 0).
    3. Sums coefficients within each grade.
    4. Simplifies coefficient sums exactly (sp.simplify).
    5. Removes grades whose combined coefficient is exactly zero.
    6. Sorts remaining grades deterministically by (evalf, string).
    """
    grouped: List[Tuple[sp.Expr, sp.Expr]] = []  # (coeff_sum, canonical_grade)
    for c, g in terms:
        c_sym = sp.simplify(sympify(c))
        g_sym = sp.simplify(sympify(g))
        found = False
        for idx, (c_acc, g_acc) in enumerate(grouped):
            if sp.simplify(g_sym - g_acc) == 0:
                grouped[idx] = (sp.simplify(c_acc + c_sym), g_acc)
                found = True
                break
        if not found:
            grouped.append((c_sym, g_sym))

    cleaned: List[Tuple[sp.Expr, sp.Expr]] = []
    for c_sum, g_can in grouped:
        c_simp = sp.simplify(c_sum)
        if c_simp != 0:
            cleaned.append((c_simp, g_can))

    # Deterministic sort
    cleaned.sort(
        key=lambda item: (
            float(item[1].evalf()) if item[1].is_number and item[1].evalf().is_real else 0.0,
            str(item[1]),
            str(item[0]),
        )
    )
    return cleaned


def classify_minimal_support(terms: List[Tuple[Any, Any]]) -> MinimalSupportClassification:
    r"""Classify a candidate minimal-support kernel element \sum_{j=1}^m a_j [K_j].

    Parameters:
        terms: List of (coeff, grade) pairs with coeff in Q_bar, grade in A_R.

    Returns:
        MinimalSupportClassification with exact support size, affine rank, and reduction status.
    """
    cleaned_terms = canonicalize_group_algebra_terms(terms)
    m = len(cleaned_terms)

    if m == 0:
        return MinimalSupportClassification(
            support_size=0,
            is_possible=False,
            affine_support_rank=0,
            classification_code="EMPTY_SUPPORT",
            reduction_target="NONE",
            description="Empty linear combination vanishes vacuously after coefficient cancellation.",
        )

    if m == 1:
        c0, k0 = cleaned_terms[0]
        return MinimalSupportClassification(
            support_size=1,
            is_possible=False,
            affine_support_rank=0,
            classification_code="SUPPORT_SIZE_ONE_IMPOSSIBLE",
            reduction_target="NONE",
            description=f"Single-term sum {c0}*tau^{k0} = 0 is impossible because tau > 0 and {c0} != 0.",
        )

    if m == 2:
        (c0, k0), (c1, k1) = cleaned_terms
        diff = sp.simplify(k1 - k0)
        return MinimalSupportClassification(
            support_size=2,
            is_possible=True,
            affine_support_rank=1 if diff != 0 else 0,
            classification_code="SUPPORT_SIZE_TWO_RANK_ONE_REDUCED",
            reduction_target="S_TAU_EXCEPTIONAL_DIRECTION",
            description=f"Two-term relation factors to tau^({diff}) = -({c0})/({c1}) in Q_bar, classified by S_tau.",
        )

    if m == 3:
        (c0, k0), (c1, k1), (c2, k2) = cleaned_terms
        alpha = sp.simplify(k1 - k0)
        beta = sp.simplify(k2 - k0)

        if alpha == 0 or beta == 0 or alpha == beta:
            return MinimalSupportClassification(
                support_size=3,
                is_possible=True,
                affine_support_rank=1,
                classification_code="DEGENERATE_THREE_TERM_REPEATED_GRADE",
                reduction_target="S_TAU_EXCEPTIONAL_DIRECTION",
                description="Repeated grade collapses support to size <= 2.",
            )

        # Affine rank calculation: fail-closed via compute_rational_support_rank
        rank = compute_affine_support_rank_trinomial(k0, k1, k2)
        if rank == 1:
            return MinimalSupportClassification(
                support_size=3,
                is_possible=True,
                affine_support_rank=1,
                classification_code="AFFINE_RANK_ONE_TRINOMIAL_REDUCED",
                reduction_target="S_TAU_EXCEPTIONAL_DIRECTION",
                description="Rationally collinear grades reduce to a 1-variable Laurent relation, classified by S_tau.",
            )

        # Genuine affine rank two
        return MinimalSupportClassification(
            support_size=3,
            is_possible=True,
            affine_support_rank=2,
            classification_code="FIRST_OPEN_KERNEL_SUPPORT",
            reduction_target="MINIMAL_RANK_TWO_TRINOMIAL_FRONTIER",
            description="Three nonzero terms of affine rational rank two: the first genuinely unresolved kernel support.",
        )

    # General m > 3
    grades = [g for _, g in cleaned_terms]
    rank, _ = compute_rational_support_rank(grades)
    return MinimalSupportClassification(
        support_size=m,
        is_possible=True,
        affine_support_rank=rank,
        classification_code="HIGHER_SUPPORT_CLASS",
        reduction_target="OPEN",
        description=f"Support size {m} with affine rank {rank}.",
    )


def compute_affine_support_rank_trinomial(k0: Any, k1: Any, k2: Any) -> int:
    """Compute the affine rational rank of three grades {k0, k1, k2}.

    The affine rational rank is dim_Q span_Q {k1 - k0, k2 - k0}.
    Uses compute_rational_support_rank to establish exact rank over Q.
    Fails closed with ValueError("EXACT_AFFINE_RANK_UNRESOLVED: ...") if unresolved.
    """
    g0 = sympify(k0)
    g1 = sympify(k1)
    g2 = sympify(k2)
    try:
        rank, _ = compute_rational_support_rank([g0, g1, g2], base_grade=g0)
        return rank
    except Exception as e:
        raise ValueError(
            f"EXACT_AFFINE_RANK_UNRESOLVED: unable to compute exact affine rational rank for grades [{g0}, {g1}, {g2}]: {e}"
        ) from e


def derive_relation_space_dimension_bound(
    alpha: Any, beta: Any, assume_gelfond_schneider: bool = True
) -> RelationSpaceDimensionBound:
    r"""Derive the dimension bound of the trinomial relation space R_{alpha, beta}.

    R_{alpha, beta} = {(a0, a1, a2) in Q_bar^3 : a0 + a1*X + a2*Y = 0}
    where X = tau^alpha, Y = tau^beta with alpha/beta not in Q.

    Theorem:
        dim_{Q_bar} R_{alpha, beta} <= 1.
    Evidence Class:
        PROVED_PAPER_DERIVATION + PROVED_WITH_EXTERNAL_GELFOND_SCHNEIDER.
    Lean Core:
        trinomial_two_relations_cramer proves coordinate solvability under a nonzero minor.
    """
    a_sym = sympify(alpha)
    b_sym = sympify(beta)

    # Establish rational independence
    try:
        rank = compute_affine_support_rank_trinomial(0, a_sym, b_sym)
        is_q_indep = bool(rank == 2)
    except Exception:
        return RelationSpaceDimensionBound(
            alpha=a_sym,
            beta=b_sym,
            is_rationally_independent=False,
            assumes_external_gelfond_schneider=assume_gelfond_schneider,
            dimension_bound=-1,
            theorem_conclusion="UNRESOLVED",
            evidence_class="UNRESOLVED_RATIONAL_INDEPENDENCE",
            status="UNRESOLVED",
            description="Could not resolve rational independence of alpha and beta.",
        )

    if not is_q_indep:
        return RelationSpaceDimensionBound(
            alpha=a_sym,
            beta=b_sym,
            is_rationally_independent=False,
            assumes_external_gelfond_schneider=assume_gelfond_schneider,
            dimension_bound=-1,
            theorem_conclusion="RATIONALLY_DEPENDENT_REDUCES_TO_RANK_ONE",
            evidence_class="REDUCED_TO_S_TAU",
            status="RESOLVED_DEPENDENT",
            description="Grades alpha, beta are collinear over Q; relation reduces to single-variable S_tau.",
        )

    return RelationSpaceDimensionBound(
        alpha=a_sym,
        beta=b_sym,
        is_rationally_independent=True,
        assumes_external_gelfond_schneider=assume_gelfond_schneider,
        dimension_bound=1,
        theorem_conclusion="AT_MOST_ONE_DIMENSIONAL",
        evidence_class="PROVED_PAPER_DERIVATION_PLUS_EXTERNAL_GELFOND_SCHNEIDER",
        status="RESOLVED",
        description=(
            "Two independent relations force (1, X, Y) into a 1-dimensional nullspace over Q_bar, "
            "forcing X, Y in Q_bar via Cramer's rule. This requires alpha, beta in S_tau. "
            "By external Gelfond-Schneider, dim_Q S_tau <= 1, contradicting Q-independence. "
            "Therefore dim_{Q_bar} R_{alpha, beta} <= 1."
        ),
    )


def evaluate_relation_space_dimension_bound(alpha: Any, beta: Any) -> int:
    r"""Backward-compatible helper returning the integer dimension bound (1)."""
    bound_res = derive_relation_space_dimension_bound(alpha, beta)
    if bound_res.dimension_bound < 0:
        raise ValueError(f"Relation space dimension unresolved: {bound_res.description}")
    return bound_res.dimension_bound


def solve_two_relations_algebraic_coordinates(
    r1: Tuple[Any, Any, Any], r2: Tuple[Any, Any, Any]
) -> Dict[str, Any]:
    r"""Solve for algebraic coordinates (X, Y) given two Q_bar-independent relations.

    Handles all possible nonzero 2x2 minors of the 2x3 matrix:
        M = [[a0, a1, a2],
             [b0, b1, b2]]

    Invariant proof:
    1. rank(M) = 2 over Q_bar because r1, r2 are linearly independent.
    2. The 1D right nullspace of M is spanned by the vector of signed minors:
       v = (Delta_0, -Delta_1, Delta_2)
       where:
         Delta_0 = a1*b2 - a2*b1  (columns 1, 2)
         Delta_1 = a0*b2 - a2*b0  (columns 0, 2)
         Delta_2 = a0*b1 - a1*b0  (columns 0, 1)
    3. If (1, X, Y)^T is in the nullspace, then (1, X, Y)^T = c * v for some c in C^x.
       In particular, 1 = c * Delta_0, so Delta_0 != 0 and c = 1 / Delta_0.
    4. Therefore, X = -Delta_1 / Delta_0 in Q_bar, and Y = Delta_2 / Delta_0 in Q_bar.
    """
    a0, a1, a2 = sympify(r1[0]), sympify(r1[1]), sympify(r1[2])
    b0, b1, b2 = sympify(r2[0]), sympify(r2[1]), sympify(r2[2])

    delta_0 = sp.simplify(a1 * b2 - a2 * b1)
    delta_1 = sp.simplify(a0 * b2 - a2 * b0)
    delta_2 = sp.simplify(a0 * b1 - a1 * b0)

    is_rank_2 = bool(delta_0 != 0 or delta_1 != 0 or delta_2 != 0)
    if not is_rank_2:
        raise ValueError("COEFFICIENT_VECTORS_DEPENDENT: rows do not form a rank-2 matrix")

    # If delta_0 == 0, then any nullspace vector has first coordinate 0,
    # meaning (1, X, Y) CANNOT be in the nullspace.
    if delta_0 == 0:
        return {
            "is_rank_2": True,
            "delta_0": delta_0,
            "delta_1": delta_1,
            "delta_2": delta_2,
            "solution_exists_with_first_coord_one": False,
            "proof": "Delta_0 = 0 implies all nullspace vectors have first coordinate 0, so (1, X, Y) cannot satisfy both relations.",
        }

    sol_X = sp.simplify(-delta_1 / delta_0)
    sol_Y = sp.simplify(delta_2 / delta_0)
    return {
        "is_rank_2": True,
        "delta_0": delta_0,
        "delta_1": delta_1,
        "delta_2": delta_2,
        "solution_exists_with_first_coord_one": True,
        "sol_X": sol_X,
        "sol_Y": sol_Y,
        "coordinates_algebraic": True,
        "proof_method": "INVARIANT_NULLSPACE_AND_CRAMER_SOLVING",
    }


def check_exceptional_direction_exclusion(
    a0: Any, a1: Any, a2: Any, X_sym: Optional[Symbol] = None, Y_sym: Optional[Symbol] = None
) -> Dict[str, Any]:
    r"""Prove that a nondegenerate trinomial relation excludes all pairwise exceptional directions.

    If a0 + a1*X + a2*Y = 0 with a0*a1*a2 != 0:
    1. If X in Q_bar, then Y = (-a0 - a1*X) / a2 in Q_bar (Lean: trinomial_exceptional_x_forces_exceptional_y).
    2. If Y in Q_bar, then X = (-a0 - a2*Y) / a1 in Q_bar (Lean: trinomial_exceptional_y_forces_exceptional_x).
    3. If Y/X in Q_bar, dividing by X yields X = -a0 / (a1 + a2*(Y/X)) in Q_bar
       (Lean: trinomial_exceptional_ratio_forces_exceptional_coordinates).
       If a1 + a2*(Y/X) == 0, then a0 = -X*(a1 + a2*(Y/X)) = 0, which contradicts nondegeneracy.

    In all three cases, X, Y in Q_bar, forcing alpha, beta in S_tau, which contradicts
    dim_Q S_tau <= 1 for Q-independent grades.
    """
    c0 = sympify(a0)
    c1 = sympify(a1)
    c2 = sympify(a2)

    if c0 == 0 or c1 == 0 or c2 == 0:
        raise ValueError(
            f"DEGENERATE_COEFFICIENT_VECTOR: all coefficients must be nonzero, got ({c0}, {c1}, {c2})"
        )

    X = X_sym if X_sym is not None else Symbol("X")
    Y = Y_sym if Y_sym is not None else Symbol("Y")

    sol_Y_given_X = sp.simplify((-c0 - c1 * X) / c2)
    sol_X_given_Y = sp.simplify((-c0 - c2 * Y) / c1)

    Z = Symbol("Z")  # Z = Y / X
    # c0 + X * (c1 + c2 * Z) = 0 ==> X = -c0 / (c1 + c2 * Z)
    sol_X_given_ratio = sp.simplify(-c0 / (c1 + c2 * Z))
    ratio_denom = sp.simplify(c1 + c2 * Z)

    return {
        "is_nondegenerate": True,
        "sol_Y_from_X": sol_Y_given_X,
        "sol_X_from_Y": sol_X_given_Y,
        "sol_X_from_ratio": sol_X_given_ratio,
        "ratio_denominator": ratio_denom,
        "ratio_denominator_zero_forces_a0_zero": True,
        "algebraicity_closure_inference": "X in Q_bar <=> Y in Q_bar <=> Y/X in Q_bar via field operations in Q_bar",
        "external_s_tau_contradiction": "dim_Q S_tau <= 1 (Gelfond-Schneider) excludes Q-independent alpha, beta in S_tau",
        "evidence_class": "LEAN_PROVED_SOLVING_IDENTITIES_FEEDING_PAPER_PLUS_GELFOND_SCHNEIDER",
        "assumptions": [
            "a0 * a1 * a2 != 0 (nondegeneracy)",
            "alpha / beta not in Q (Q-independence)",
            "dim_Q S_tau <= 1 (external Baker / Gelfond-Schneider theorem)",
        ],
        "theorem": "PAIRWISE_EXCEPTIONAL_DIRECTIONS_EXCLUDED",
        "description": "Any nondegenerate trinomial relation forces alpha, beta, and beta - alpha entirely outside S_tau.",
    }


def normalize_trinomial_coefficients_real(
    a0: Any, a1: Any, a2: Any
) -> RealNormalizationResult:
    r"""Normalize complex algebraic trinomial coefficients to real algebraic coefficients.

    Direct elementary proof:
    Because generators X, Y in R_{>0}, complex conjugation sends any relation to another relation:
        conj(a0) + conj(a1)*X + conj(a2)*Y = 0.
    Since dim R_{alpha, beta} <= 1, the conjugate vector must be proportional to (a0, a1, a2):
        conj(a_j) = lambda * a_j  for all j, with lambda * conj(lambda) = 1.
    Choosing the phase multiplier:
        mu = 1 + lambda  (if lambda != -1)
        mu = I           (if lambda == -1)
    satisfies:
        conj(mu * a_j) = conj(mu) * conj(a_j)
                       = (1 + conj(lambda)) * (lambda * a_j)
                       = (lambda + lambda * conj(lambda)) * a_j
                       = (lambda + 1) * a_j
                       = mu * a_j.
    Thus mu * a_j is strictly invariant under complex conjugation and hence real algebraic.

    Fails closed with ValueError("COEFFICIENT_VECTOR_NOT_CONJUGATE_PROPORTIONAL") if
    the coefficients do not satisfy conjugate proportionality.
    """
    c0 = sympify(a0)
    c1 = sympify(a1)
    c2 = sympify(a2)

    if c0 == 0 and c1 == 0 and c2 == 0:
        raise ValueError("ALL_COEFFICIENTS_ZERO: cannot normalize trivial coefficient vector")

    # Check if already all real
    if (
        sp.simplify(sp.im(c0)) == 0
        and sp.simplify(sp.im(c1)) == 0
        and sp.simplify(sp.im(c2)) == 0
    ):
        return RealNormalizationResult(
            original_coeffs=(c0, c1, c2),
            lambda_val=Integer(1),
            mu_val=Integer(1),
            normalized_coeffs=(c0, c1, c2),
            is_real_normalized=True,
            proof_method="DIRECT_ELEMENTARY_CONJUGATE_PHASE_NORMALIZATION",
        )

    # Pick a nonzero coefficient as pivot to compute candidate lambda = conj(c) / c
    c_pivot = c0 if c0 != 0 else (c1 if c1 != 0 else c2)
    lambda_val = sp.simplify(sp.conjugate(c_pivot) / c_pivot)

    # Verify |lambda| == 1
    norm_sq = sp.simplify(lambda_val * sp.conjugate(lambda_val))
    if norm_sq != 1:
        raise ValueError(
            f"COEFFICIENT_VECTOR_NOT_CONJUGATE_PROPORTIONAL: lambda={lambda_val} does not satisfy |lambda|=1"
        )

    # Verify that every nonzero coefficient satisfies conj(c) == lambda * c
    coeffs = [c0, c1, c2]
    for idx, c in enumerate(coeffs):
        if c != 0:
            diff = sp.simplify(sp.conjugate(c) - lambda_val * c)
            if diff != 0:
                raise ValueError(
                    f"COEFFICIENT_VECTOR_NOT_CONJUGATE_PROPORTIONAL: coefficient {idx} ({c}) does not satisfy conj(c) = lambda * c"
                )

    # Choose mu
    if sp.simplify(lambda_val + 1) == 0:
        mu_val = I
    else:
        mu_val = sp.simplify(1 + lambda_val)

    norm_c0 = sp.simplify(sp.expand(mu_val * c0))
    norm_c1 = sp.simplify(sp.expand(mu_val * c1))
    norm_c2 = sp.simplify(sp.expand(mu_val * c2))

    # Verify that imaginary parts vanish exactly
    im0 = sp.simplify(sp.im(norm_c0))
    im1 = sp.simplify(sp.im(norm_c1))
    im2 = sp.simplify(sp.im(norm_c2))

    if im0 != 0 or im1 != 0 or im2 != 0:
        raise ValueError(
            f"COEFFICIENT_VECTOR_NOT_CONJUGATE_PROPORTIONAL: transformed coefficients ({norm_c0}, {norm_c1}, {norm_c2}) have nonzero imaginary parts ({im0}, {im1}, {im2})"
        )

    return RealNormalizationResult(
        original_coeffs=(c0, c1, c2),
        lambda_val=lambda_val,
        mu_val=mu_val,
        normalized_coeffs=(norm_c0, norm_c1, norm_c2),
        is_real_normalized=True,
        proof_method="DIRECT_ELEMENTARY_CONJUGATE_PHASE_NORMALIZATION",
    )


def classify_sign_orientation(a0: Any, a1: Any, a2: Any) -> SignOrientation:
    r"""Classify a real trinomial relation a0 + a1*X + a2*Y = 0 (X, Y > 0) by its sign geometry.

    Since generators are strictly positive, real coefficients cannot have the same sign.
    Exactly one coefficient has opposite sign, orienting the relation into one of three
    positive affine geometries:
    1. Y = u + v * X (a2 opposite sign to a0, a1)
    2. X = u + v * Y (a1 opposite sign to a0, a2)
    3. 1 = u * X + v * Y (a0 opposite sign to a1, a2)
    with positive algebraic u, v in A_R^{>0}.

    Fails closed if coefficients are zero, non-real, or of ambiguous sign.
    """
    c0 = sympify(a0)
    c1 = sympify(a1)
    c2 = sympify(a2)

    if c0 == 0 or c1 == 0 or c2 == 0:
        raise ValueError(f"DEGENERATE_COEFFICIENT: zero coefficient in ({c0}, {c1}, {c2})")

    if (
        sp.simplify(sp.im(c0)) != 0
        or sp.simplify(sp.im(c1)) != 0
        or sp.simplify(sp.im(c2)) != 0
    ):
        raise ValueError(f"NON_REAL_COEFFICIENT: coefficients must be real, got ({c0}, {c1}, {c2})")

    s0 = sp.sign(c0)
    s1 = sp.sign(c1)
    s2 = sp.sign(c2)

    if not (s0.is_number and s1.is_number and s2.is_number):
        raise ValueError(f"UNRESOLVED_COEFFICIENT_SIGN: signs cannot be determined symbolically for ({c0}, {c1}, {c2})")

    if (s0 > 0 and s1 > 0 and s2 > 0) or (s0 < 0 and s1 < 0 and s2 < 0):
        raise ValueError(
            f"SAME_SIGN_COEFFICIENTS_IMPOSSIBLE: all coefficients have same sign ({s0}, {s1}, {s2}): no positive solution (X, Y > 0) can exist."
        )

    # Identify the odd sign
    # Case 1: c2 has opposite sign to c0 and c1 ==> c0 + c1*X = -c2*Y ==> Y = (-c0/c2) + (-c1/c2)*X
    if (s2 != s0) and (s0 == s1):
        u = sp.simplify(-c0 / c2)
        v = sp.simplify(-c1 / c2)
        return SignOrientation(
            orientation_type="Y_AFFINE_X",
            u=u,
            v=v,
            description="Orientation Y = u + v * X with positive algebraic u, v.",
        )

    # Case 2: c1 has opposite sign to c0 and c2 ==> c0 + c2*Y = -c1*X ==> X = (-c0/c1) + (-c2/c1)*Y
    if (s1 != s0) and (s0 == s2):
        u = sp.simplify(-c0 / c1)
        v = sp.simplify(-c2 / c1)
        return SignOrientation(
            orientation_type="X_AFFINE_Y",
            u=u,
            v=v,
            description="Orientation X = u + v * Y with positive algebraic u, v.",
        )

    # Case 3: c0 has opposite sign to c1 and c2 ==> -c0 = c1*X + c2*Y ==> 1 = (-c1/c0)*X + (-c2/c0)*Y
    u = sp.simplify(-c1 / c0)
    v = sp.simplify(-c2 / c0)
    return SignOrientation(
        orientation_type="ONE_AFFINE_XY",
        u=u,
        v=v,
        description="Orientation 1 = u * X + v * Y with positive algebraic u, v.",
    )


def evaluate_dilation_orbit(
    a0: Any, a1: Any, a2: Any, X: Any, Y: Any, grades: List[int]
) -> Dict[int, sp.Expr]:
    r"""Evaluate the common grade-dilation orbit f(n) = a0 + a1 * X^n + a2 * Y^n."""
    c0 = sympify(a0)
    c1 = sympify(a1)
    c2 = sympify(a2)
    x_val = sympify(X)
    y_val = sympify(Y)

    orbit = {}
    for n in grades:
        val = sp.simplify(c0 + c1 * (x_val**n) + c2 * (y_val**n))
        orbit[n] = val
    return orbit


def consecutive_orbit_determinant(X: Any, Y: Any, n: int = 0) -> sp.Expr:
    r"""Compute the 3x3 consecutive dilation matrix determinant:
        det [ 1,   X^n,       Y^n       ]
            [ 1,   X^(n+1),   Y^(n+1)   ]
            [ 1,   X^(n+2),   Y^(n+2)   ]
        = X^n * Y^n * (X - 1) * (Y - 1) * (Y - X).
    """
    x = sympify(X)
    y = sympify(Y)
    det_val = sp.simplify((x**n) * (y**n) * (x - 1) * (y - 1) * (y - x))
    return det_val


def check_three_consecutive_rigidity(
    a0: Any, a1: Any, a2: Any, X: Any, Y: Any, n: int = 0
) -> Dict[str, Any]:
    r"""Verify that f(n) = f(n+1) = f(n+2) = 0 forces a0 = a1 = a2 = 0 for distinct positive 1, X, Y."""
    x = sympify(X)
    y = sympify(Y)
    det_expr = consecutive_orbit_determinant(x, y, n)
    is_det_nonzero = bool(x != 1 and y != 1 and x != y and x != 0 and y != 0)

    return {
        "determinant_expr": det_expr,
        "is_determinant_nonzero": is_det_nonzero,
        "forces_trivial_coefficients": is_det_nonzero,
        "theorem": "THREE_CONSECUTIVE_DILATION_ORBIT_RIGIDITY",
        "description": "A nonzero trinomial vector cannot vanish on three consecutive dilation grades.",
    }


def generalized_vandermonde_determinant(
    bases: Tuple[float, float, float], powers: Tuple[int, int, int]
) -> float:
    r"""Evaluate the 3x3 generalized Vandermonde determinant for bases 0 < X1 < X2 < X3 and powers n1 < n2 < n3.

    By Descartes' rule of signs / Chebyshev system theory, this determinant is strictly positive.
    """
    x1, x2, x3 = bases
    n1, n2, n3 = powers

    r1 = [x1**n1, x2**n1, x3**n1]
    r2 = [x1**n2, x2**n2, x3**n2]
    r3 = [x1**n3, x2**n3, x3**n3]

    det_val = (
        r1[0] * (r2[1] * r3[2] - r2[2] * r3[1])
        - r1[1] * (r2[0] * r3[2] - r2[2] * r3[0])
        + r1[2] * (r2[0] * r3[1] - r2[1] * r3[0])
    )
    return det_val


def audit_multiplicative_group_theorems() -> Dict[str, Any]:
    r"""Primary-source literature audit of finite-rank multiplicative group theorems.

    Distinguishes the relevant groups:
    1. Base multiplicative group:
       Gamma_0 = <X, Y> = <tau^alpha, tau^beta> \subset R_{>0}^\times.
       For alpha/beta not in Q, Gamma_0 \cong Z^2 (rank 2).
    2. Ambient solution group for a0 + a1*u + a2*v = 0:
       Independently varying (u, v) in Gamma_0 x Gamma_0 lives in a rank-4 group.
    3. Diagonal dilation orbit:
       Delta_{alpha, beta} = {(X^n, Y^n) : n in Z} is a rank-1 cyclic subgroup.

    Citations & Theorems:
    - Laurent (1984), "Équations diophantiennes exponentielles", Invent. Math.
    - Evertse, Schlickewei, Schmidt (2002), "Linear equations in elements of groups of finite rank", Ann. of Math.
    - Hindry (1988), Autour d'une conjecture de Serge Lang.

    Consequences:
    - Line a0 + a1*u + a2*v = 0 in G_m^2 contains no 1D translate of an algebraic subtorus.
    - By Laurent/ESS, solutions (u, v) in Gamma_0 x Gamma_0 for fixed coefficients are FINITE.
    - CRITICAL BOUNDARY: FINITE_DOES_NOT_IMPLY_EMPTY.
    - NO_CANONICAL_ORBIT_VANISHING_PROPAGATION:
      f(1) = 0 does not force f(2) = 0, f(3) = 0, or any further orbit vanishing.
    """
    return {
        "base_multiplicative_group": "Gamma_0 = <tau^alpha, tau^beta> subset R_{>0}^x",
        "base_group_rank": 2,
        "is_base_group_free_abelian": True,
        "solution_ambient_group": "Gamma_0 x Gamma_0",
        "solution_group_rank": 4,
        "diagonal_dilation_orbit": "Delta_{alpha, beta} = {(X^n, Y^n) : n in Z}",
        "diagonal_orbit_rank": 1,
        "subtorus_coset_in_line": False,
        "subtorus_audit_detail": (
            "Line a0 + a1*u + a2*v = 0 with nonzero algebraic coefficients contains no 1D subtorus coset u^p*v^q = c in G_m^2."
        ),
        "citations": [
            "Evertse (1984), Invent. Math.",
            "Laurent (1984), Invent. Math. (Mordell-Lang for algebraic tori)",
            "Evertse, Schlickewei, Schmidt (2002), Ann. of Math.",
        ],
        "consequence_for_fixed_coefficients": "FIXED_COEFFICIENT_TRINOMIAL_SOLUTIONS_FINITE",
        "critical_boundary": "FINITE_DOES_NOT_IMPLY_EMPTY",
        "diagonal_orbit_vanishing_bound": "At most 2 distinct integer zeros for nonzero (a0, a1, a2) via generalized Vandermonde",
        "orbit_propagation_statement": "NO_CANONICAL_ORBIT_VANISHING_PROPAGATION",
        "orbit_propagation_description": "f(1) = 0 does not force f(2) = 0, f(3) = 0, or any further orbit vanishing.",
        "existence_status": "MINIMAL_RANK_TWO_TRINOMIAL_EXISTENCE_OPEN",
        "zeta_bridge_status": "NO_ZETA_TO_KERNEL_BRIDGE_FOUND",
    }


def enumerate_sparse_trinomial_monomial_pairs(
    max_degree: int = 2,
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    r"""Enumerate all distinct pairs of non-constant monomials (M1, M2) with 0 < deg(M) <= max_degree.

    Each monomial is represented by its power pair (i, j) for X^i * Y^j.
    Together with the constant 1 = X^0 * Y^0, these form the 3-element support {1, M1, M2}.
    For max_degree=3: 9 nonconstant monomials yield comb(9, 2) = 36 constant-anchored supports.
    """
    monomials: List[Tuple[int, int]] = []
    for d in range(1, max_degree + 1):
        for i in range(d + 1):
            j = d - i
            monomials.append((i, j))

    pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    for idx1 in range(len(monomials)):
        for idx2 in range(idx1 + 1, len(monomials)):
            pairs.append((monomials[idx1], monomials[idx2]))
    return pairs


def partition_monomial_supports_by_rank(
    pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]]
) -> Tuple[List[Tuple[Tuple[int, int], Tuple[int, int]]], List[Tuple[Tuple[int, int], Tuple[int, int]]]]:
    r"""Partition constant-anchored supports {1, M1, M2} into affine rank-one controls and rank-two supports.

    For M1 = X^i1 Y^j1 and M2 = X^i2 Y^j2 with constant anchor 1 = X^0 Y^0:
    The affine rank is dim_Q span_Q {(i1, j1), (i2, j2)}:
    - Rank 1 if i1 * j2 - i2 * j1 == 0 (collinear exponent vectors, e.g. both on X-axis or both on Y-axis).
    - Rank 2 if i1 * j2 - i2 * j1 != 0.

    For max_degree=3 (36 pairs):
    - 6 pairs are affine rank one (3 on X-axis, 3 on Y-axis).
    - 30 pairs are genuine affine rank two.
    """
    rank_one: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    rank_two: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

    for p in pairs:
        (i1, j1), (i2, j2) = p
        det = i1 * j2 - i2 * j1
        if det == 0:
            rank_one.append(p)
        else:
            rank_two.append(p)

    return rank_one, rank_two


def enumerate_normalized_coefficients(
    max_height: int = 5,
) -> List[Tuple[int, int, int]]:
    r"""Enumerate normalized integer coefficient triples (a0, a1, a2) up to max_height.

    Normalization conditions:
    1. 1 <= a0 <= max_height (canonical positive sign for a0 to avoid overall sign duplication)
    2. 1 <= |a1|, |a2| <= max_height
    3. a0 * a1 * a2 != 0 (nondegenerate)
    4. gcd(a0, |a1|, |a2|) == 1 (primitive)
    5. Mixed signs: cannot have all positive or all negative (since X, Y > 0).
       Since a0 > 0, at least one of a1, a2 must be negative.
    """
    results: List[Tuple[int, int, int]] = []
    for a0 in range(1, max_height + 1):
        for a1 in range(-max_height, max_height + 1):
            if a1 == 0:
                continue
            for a2 in range(-max_height, max_height + 1):
                if a2 == 0:
                    continue
                # Mixed sign check: since a0 > 0, cannot have a1 > 0 and a2 > 0
                if a1 > 0 and a2 > 0:
                    continue
                # Primitive gcd check
                g = math.gcd(a0, math.gcd(abs(a1), abs(a2)))
                if g != 1:
                    continue
                results.append((a0, a1, a2))
    return results


def certify_sparse_trinomial_exclusion(
    instance_name: str,
    alpha_expr: Any,
    beta_expr: Any,
    max_degree: int = 2,
    max_height: int = 5,
    prec_bits: int = 128,
) -> CertifiedTrinomialExclusionResult:
    r"""Perform a certified sparse trinomial exclusion search using Arb ball arithmetic.

    Evaluates:
        V = a0 + a1 * (X^i1 * Y^j1) + a2 * (X^i2 * Y^j2)
    over all normalized constant-anchored supports {1, M1, M2} with deg <= max_degree
    and primitive mixed-sign integer coefficients ||a||_inf <= max_height.

    Rigorous certification rules:
    - Never uses midpoint as certified distance.
    - Uses interval lower bound: abs(V).abs_lower() > 0.
    - If 0 in V, reports failure/inconclusive.
    - Fails closed on unsupported expressions.
    """
    t0 = time.time()
    old_prec = ctx.prec
    try:
        ctx.prec = prec_bits

        # Exact Arb generator evaluation
        tau_arb = 2 * arb.pi()
        alpha_arb = expr_to_arb(alpha_expr)
        beta_arb = expr_to_arb(beta_expr)

        X_arb = tau_arb**alpha_arb
        Y_arb = tau_arb**beta_arb

        pairs = enumerate_sparse_trinomial_monomial_pairs(max_degree)
        coeffs = enumerate_normalized_coefficients(max_height)

        r1_supports, r2_supports = partition_monomial_supports_by_rank(pairs)

        smallest_dist = float("inf")
        smallest_candidate: Dict[str, Any] = {}
        total_evaluations = 0

        for (i1, j1), (i2, j2) in pairs:
            m1_val = (X_arb**i1) * (Y_arb**j1)
            m2_val = (X_arb**i2) * (Y_arb**j2)

            for a0, a1, a2 in coeffs:
                total_evaluations += 1
                v = arb(a0) + arb(a1) * m1_val + arb(a2) * m2_val

                # Certified distance lower bound
                if 0 in v:
                    raise RuntimeError(
                        f"Inconclusive ball enclosure at prec={prec_bits} for {a0} + {a1}*M1 + {a2}*M2"
                    )

                lb = float(v.abs_lower())
                if lb <= 0.0:
                    raise RuntimeError(
                        f"Zero lower bound encountered for {a0} + {a1}*M1 + {a2}*M2"
                    )

                if lb < smallest_dist:
                    smallest_dist = lb
                    smallest_candidate = {
                        "a0": a0,
                        "a1": a1,
                        "a2": a2,
                        "m1": (i1, j1),
                        "m2": (i2, j2),
                        "distance_lb": lb,
                    }

        runtime = time.time() - t0
        all_box_subsets = math.comb(math.comb(max_degree + 2, 2), 3) if max_degree >= 2 else len(pairs)
        return CertifiedTrinomialExclusionResult(
            canonical_instance=instance_name,
            alpha_expr=sympify(alpha_expr),
            beta_expr=sympify(beta_expr),
            max_degree_D=max_degree,
            max_height_H=max_height,
            all_three_monomial_subsets_in_box=all_box_subsets,
            constant_anchored_supports_tested=len(pairs),
            affine_rank_two_supports_tested=len(r2_supports),
            affine_rank_one_control_supports=len(r1_supports),
            normalized_coefficients_per_support=len(coeffs),
            rank_two_candidates_certified=len(r2_supports) * len(coeffs),
            rank_one_control_candidates_certified=len(r1_supports) * len(coeffs),
            total_candidates_certified=total_evaluations,
            smallest_certified_distance=smallest_dist,
            smallest_candidate=smallest_candidate,
            precision_bits=prec_bits,
            runtime_seconds=runtime,
            certificate_scope="constant-anchored sparse trinomial campaign",
            classification="CERTIFIED_FINITE_TRINOMIAL_EXCLUSION",
        )

    finally:
        ctx.prec = old_prec


def evaluate_exact_control_relation(
    X_val: Any,
    Y_val: Any,
    m1_pows: Tuple[int, int],
    m2_pows: Tuple[int, int],
    a0: int,
    a1: int,
    a2: int,
    prec_bits: int = 128,
) -> Dict[str, Any]:
    r"""Evaluate an exact synthetic control relation to verify that machinery recovers zero.

    For synthetic controls such as Y = 1 + X or Y = X^2:
    The certified ball must contain 0, proving that the certificate engine does not
    falsely certify nonvanishing on true relations.
    """
    old_prec = ctx.prec
    try:
        ctx.prec = prec_bits
        x_arb = arb(X_val) if not isinstance(X_val, arb) else X_val
        y_arb = arb(Y_val) if not isinstance(Y_val, arb) else Y_val

        i1, j1 = m1_pows
        i2, j2 = m2_pows

        m1 = (x_arb**i1) * (y_arb**j1)
        m2 = (x_arb**i2) * (y_arb**j2)

        v = arb(a0) + arb(a1) * m1 + arb(a2) * m2
        contains_zero = 0 in v
        return {
            "ball": str(v),
            "contains_zero": contains_zero,
            "abs_lower": float(v.abs_lower()),
            "status": "RELATION_DETECTED" if contains_zero else "EXCLUDED",
            "control_passed": contains_zero,
        }
    finally:
        ctx.prec = old_prec
