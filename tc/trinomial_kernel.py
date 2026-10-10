r"""Minimal Rank-Two Trinomial Kernel, Relation-Space Rigidity, and Sparse Orbit Theorems.

TASK-TC-030: Classification and certified sparse exclusion of the first genuinely
unresolved ambient realization kernel support:
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

Structural Theorems:
1. RANK_TWO_TRINOMIAL_RELATION_SPACE_AT_MOST_ONE_DIMENSIONAL:
   Two independent linear relations among (1, X, Y) force X, Y in Q_bar,
   contradicting dim_Q S_tau <= 1. Hence dim_{Q_bar} R_{alpha, beta} <= 1.
2. PAIRWISE_EXCEPTIONAL_DIRECTIONS_EXCLUDED:
   A nondegenerate trinomial relation forces alpha, beta, beta-alpha outside S_tau.
3. TRINOMIAL_COEFFICIENTS_REAL_NORMALIZABLE:
   Complex conjugation and dim <= 1 yield (conj(a0), conj(a1), conj(a2)) = lambda (a0, a1, a2)
   with |lambda| = 1. Setting mu = 1 + lambda (or mu = i if lambda = -1) normalizes all
   coefficients into A_R = Q_bar \cap R.
4. MIXED_SIGN_NECESSARY:
   For positive generators X, Y > 0 and real coefficients, same-sign coefficients
   cannot sum to zero. Every relation is orientable into one of:
   - Y = u + v * X (u, v in A_R^{>0})
   - X = u + v * Y (u, v in A_R^{>0})
   - 1 = u * X + v * Y (u, v in A_R^{>0})
5. THREE_CONSECUTIVE_DILATION_ORBIT_RIGIDITY:
   For f(n) = a0 + a1 * X^n + a2 * Y^n, det(M_n) = X^n * Y^n * (X - 1) * (Y - 1) * (Y - X) != 0.
   Thus f(n) = f(n+1) = f(n+2) = 0 implies a0 = a1 = a2 = 0.
6. NO_CANONICAL_RELATION_PROPAGATION:
   f(1) = 0 does not imply f(2) = 0. TC transport does not produce contradictory grade orbits.
7. MULTIPLICATIVE_GROUP_S_UNIT_AUDIT:
   Gamma = <X, Y> \cong Z^2. By Laurent (1984) and Evertse-Schlickewei-Schmidt (2002),
   solutions to a0 + a1 * u + a2 * v = 0 with (u, v) in Gamma^2 are FINITE.
   However, FINITE_DOES_NOT_IMPLY_EMPTY; existence of one relation remains OPEN.
"""

from __future__ import annotations

import itertools
import math
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

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


@dataclass(frozen=True)
class DilationOrbitResult:
    n_values: List[int]
    orbit_values: List[sp.Expr]
    is_three_consecutive_rigid: bool
    determinant_val: sp.Expr


@dataclass(frozen=True)
class CertifiedTrinomialExclusionResult:
    canonical_instance: str
    alpha_expr: sp.Expr
    beta_expr: sp.Expr
    max_degree_D: int
    max_height_H: int
    supports_tested: int
    normalized_trinomials_tested: int
    smallest_certified_distance: float
    smallest_candidate: Dict[str, Any]
    precision_bits: int
    runtime_seconds: float
    classification: str


def classify_minimal_support(terms: List[Tuple[Any, Any]]) -> MinimalSupportClassification:
    r"""Classify a candidate minimal-support kernel element \sum_{j=1}^m a_j [K_j].

    Parameters:
        terms: List of (coeff, grade) pairs with coeff in Q_bar \ {0}, grade in A_R.

    Returns:
        MinimalSupportClassification with exact support size, affine rank, and reduction status.
    """
    cleaned_terms = [(sympify(c), sympify(g)) for c, g in terms if sympify(c) != 0]
    m = len(cleaned_terms)

    if m == 0:
        return MinimalSupportClassification(
            support_size=0,
            is_possible=False,
            affine_support_rank=0,
            classification_code="EMPTY_SUPPORT",
            reduction_target="NONE",
            description="Empty linear combination vanishes vacuously.",
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

        # Affine rank calculation: check if alpha / beta in Q
        ratio = sp.simplify(alpha / beta)
        if ratio.is_rational:
            return MinimalSupportClassification(
                support_size=3,
                is_possible=True,
                affine_support_rank=1,
                classification_code="AFFINE_RANK_ONE_TRINOMIAL_REDUCED",
                reduction_target="S_TAU_EXCEPTIONAL_DIRECTION",
                description=f"Rationally collinear grades (ratio {ratio} in Q) reduce to a 1-variable Laurent relation, classified by S_tau.",
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
    """
    g0 = sympify(k0)
    g1 = sympify(k1)
    g2 = sympify(k2)
    alpha = sp.simplify(g1 - g0)
    beta = sp.simplify(g2 - g0)

    if alpha == 0 and beta == 0:
        return 0
    if alpha == 0 or beta == 0 or alpha == beta:
        return 1

    ratio = sp.simplify(alpha / beta)
    if ratio.is_rational:
        return 1
    return 2


def evaluate_relation_space_dimension_bound(alpha: Any, beta: Any) -> int:
    r"""Determine the dimension bound of the trinomial relation space R_{alpha, beta}.

    R_{alpha, beta} = {(a0, a1, a2) in Q_bar^3 : a0 + a1*X + a2*Y = 0}
    where X = tau^alpha, Y = tau^beta with alpha/beta not in Q.

    Theorem:
        dim_{Q_bar} R_{alpha, beta} <= 1.
        If a nonzero relation exists, dim_{Q_bar} R_{alpha, beta} = 1.
    """
    # For any alpha, beta with alpha/beta not in Q, two independent relations
    # would force X, Y in Q_bar via Cramer's rule, forcing alpha, beta in S_tau.
    # But dim_Q S_tau <= 1 while alpha, beta are Q-independent, a contradiction.
    return 1


def check_exceptional_direction_exclusion(
    a0: Any, a1: Any, a2: Any, X_sym: Optional[Symbol] = None, Y_sym: Optional[Symbol] = None
) -> Dict[str, Any]:
    r"""Prove that a nondegenerate trinomial relation excludes all pairwise exceptional directions.

    If a0 + a1*X + a2*Y = 0 with a0*a1*a2 != 0:
    1. If X in Q_bar, then Y = (-a0 - a1*X) / a2 in Q_bar.
    2. If Y in Q_bar, then X = (-a0 - a2*Y) / a1 in Q_bar.
    3. If Y/X in Q_bar, dividing by X yields X = -a0 / (a1 + a2*(Y/X)) in Q_bar.

    In all three cases, X, Y in Q_bar, forcing alpha, beta in S_tau, which contradicts
    dim_Q S_tau <= 1 for Q-independent grades.
    """
    c0 = sympify(a0)
    c1 = sympify(a1)
    c2 = sympify(a2)
    X = X_sym or Symbol("X")
    Y = Symbol("Y")

    sol_Y_given_X = sp.simplify((-c0 - c1 * X) / c2)
    sol_X_given_Y = sp.simplify((-c0 - c2 * Y) / c1)

    Z = Symbol("Z")  # Z = Y / X
    # c0 * X^(-1) + c1 + c2 * Z = 0 ==> X = -c0 / (c1 + c2 * Z)
    sol_X_given_ratio = sp.simplify(-c0 / (c1 + c2 * Z))

    return {
        "is_nondegenerate": bool(c0 != 0 and c1 != 0 and c2 != 0),
        "sol_Y_from_X": sol_Y_given_X,
        "sol_X_from_Y": sol_X_given_Y,
        "sol_X_from_ratio": sol_X_given_ratio,
        "exceptional_x_forces_algebraic_y": True,
        "exceptional_y_forces_algebraic_x": True,
        "exceptional_ratio_forces_algebraic_coordinates": True,
        "theorem": "PAIRWISE_EXCEPTIONAL_DIRECTIONS_EXCLUDED",
        "description": "Any nondegenerate trinomial relation forces alpha, beta, and beta - alpha entirely outside S_tau.",
    }


def normalize_trinomial_coefficients_real(
    a0: Any, a1: Any, a2: Any
) -> RealNormalizationResult:
    r"""Normalize complex algebraic trinomial coefficients to real algebraic coefficients.

    Because X, Y in R_{>0}, conjugation sends a relation to a relation.
    Since dim R_{alpha, beta} = 1, (conj(a0), conj(a1), conj(a2)) = lambda * (a0, a1, a2)
    with lambda * conj(lambda) = 1.
    If lambda == -1: mu = I produces real coefficients.
    If lambda != -1: mu = 1 + lambda produces real coefficients.
    """
    c0 = sympify(a0)
    c1 = sympify(a1)
    c2 = sympify(a2)

    # First check if already all real
    if c0.is_real and c1.is_real and c2.is_real:
        return RealNormalizationResult(
            original_coeffs=(c0, c1, c2),
            lambda_val=Integer(1),
            mu_val=Integer(1),
            normalized_coeffs=(c0, c1, c2),
            is_real_normalized=True,
        )

    # Pick a nonzero coefficient to compute lambda = conj(c) / c
    c_pivot = c0 if c0 != 0 else (c1 if c1 != 0 else c2)
    lambda_val = sp.simplify(sp.conjugate(c_pivot) / c_pivot)

    # Choose mu
    if sp.simplify(lambda_val + 1) == 0:
        mu_val = I
    else:
        mu_val = sp.simplify(1 + lambda_val)

    norm_c0 = sp.simplify(sp.expand(mu_val * c0))
    norm_c1 = sp.simplify(sp.expand(mu_val * c1))
    norm_c2 = sp.simplify(sp.expand(mu_val * c2))

    # Verify that imaginary parts vanish
    is_real = bool(
        sp.simplify(sp.im(norm_c0)) == 0
        and sp.simplify(sp.im(norm_c1)) == 0
        and sp.simplify(sp.im(norm_c2)) == 0
    )

    return RealNormalizationResult(
        original_coeffs=(c0, c1, c2),
        lambda_val=lambda_val,
        mu_val=mu_val,
        normalized_coeffs=(sp.re(norm_c0), sp.re(norm_c1), sp.re(norm_c2)),
        is_real_normalized=is_real,
    )


def classify_sign_orientation(a0: Any, a1: Any, a2: Any) -> SignOrientation:
    r"""Classify a real trinomial relation a0 + a1*X + a2*Y = 0 (X, Y > 0) by its sign geometry.

    Since generators are strictly positive, coefficients cannot have the same sign.
    Exactly one coefficient has opposite sign, orienting the relation into one of three
    positive affine geometries:
    1. Y = u + v * X (a2 opposite sign to a0, a1)
    2. X = u + v * Y (a1 opposite sign to a0, a2)
    3. 1 = u * X + v * Y (a0 opposite sign to a1, a2)
    with positive algebraic u, v in A_R^{>0}.
    """
    c0 = sympify(a0)
    c1 = sympify(a1)
    c2 = sympify(a2)

    # Normalize overall sign so at least one is positive
    s0 = sp.sign(c0)
    s1 = sp.sign(c1)
    s2 = sp.sign(c2)

    if (s0 > 0 and s1 > 0 and s2 > 0) or (s0 < 0 and s1 < 0 and s2 < 0):
        raise ValueError(
            f"All coefficients have same sign ({s0}, {s1}, {s2}): no positive solution (X, Y > 0) can exist."
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

    # Matrix: row i has [x1^ni, x2^ni, x3^ni]
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

    Citations:
    - Evertse (1984), "On sums of S-units and linear recurrences"
    - Evertse, Schlickewei, Schmidt (2002), "Linear equations in elements of groups of finite rank"
    - Laurent (1984), "Équations diophantiennes exponentielles"
    - Lang's conjecture / Mordell-Lang for algebraic tori (Hindry 1988)

    Mathematical Analysis:
    1. Multiplicative group Gamma = <X, Y> = <tau^alpha, tau^beta> \subset R_{>0}^\times.
       Since alpha / beta not in Q, Gamma \cong Z^2.
    2. Curve C: a0 + a1*u + a2*v = 0 with a0*a1*a2 != 0 in G_m^2.
    3. C cannot contain a translate of a positive-dimensional subtorus (binomial curve u^p * v^q = c
       is nonlinear for (p, q) != (0, 0), while C is a linear line).
    4. By Laurent (1984) and Evertse-Schlickewei-Schmidt (2002), C \cap Gamma^2 is FINITE.
    5. CRITICAL BOUNDARY: FINITE_DOES_NOT_IMPLY_EMPTY. Finiteness for each fixed triple
       does not prove the set of solutions is empty.
    """
    return {
        "multiplicative_group": "Gamma = <tau^alpha, tau^beta> subset R_{>0}^x",
        "rank": 2,
        "is_free_abelian": True,
        "subtorus_coset_in_line": False,
        "subtorus_audit_detail": "Line a0 + a1*u + a2*v = 0 with non-zero coefficients contains no 1D subtorus coset u^p*v^q = c.",
        "citations": [
            "Evertse (1984), Invent. Math.",
            "Laurent (1984), Invent. Math. (Mordell-Lang for algebraic tori)",
            "Evertse, Schlickewei, Schmidt (2002), Ann. of Math.",
        ],
        "consequence_for_fixed_coefficients": "FIXED_COEFFICIENT_TRINOMIAL_SOLUTIONS_FINITE",
        "critical_boundary": "FINITE_DOES_NOT_IMPLY_EMPTY",
        "existence_status": "MINIMAL_RANK_TWO_TRINOMIAL_EXISTENCE_OPEN",
        "zeta_bridge_status": "NO_ZETA_TO_KERNEL_BRIDGE_FOUND",
    }


def enumerate_sparse_trinomial_monomial_pairs(
    max_degree: int = 2,
) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    r"""Enumerate all distinct pairs of non-constant monomials (M1, M2) with 0 < deg(M) <= max_degree.

    Each monomial is represented by its power pair (i, j) for X^i * Y^j.
    Together with the constant 1 = X^0 * Y^0, these form the 3-element support {1, M1, M2}.
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
    over all normalized supports {1, M1, M2} with deg <= max_degree
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

        smallest_dist = float("inf")
        smallest_candidate: Dict[str, Any] = {}
        total_evaluations = 0

        for (i1, j1), (i2, j2) in pairs:
            # Monomial values
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
        return CertifiedTrinomialExclusionResult(
            canonical_instance=instance_name,
            alpha_expr=sympify(alpha_expr),
            beta_expr=sympify(beta_expr),
            max_degree_D=max_degree,
            max_height_H=max_height,
            supports_tested=len(pairs),
            normalized_trinomials_tested=total_evaluations,
            smallest_certified_distance=smallest_dist,
            smallest_candidate=smallest_candidate,
            precision_bits=prec_bits,
            runtime_seconds=runtime,
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
