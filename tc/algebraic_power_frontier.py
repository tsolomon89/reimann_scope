r"""Algebraic Power Frontier and Unconditional Rank-Two Classification.

TASK-TC-029: Systematic investigation of the unconditional rank-two algebraic-power frontier
for generators X = tau^alpha, Y = tau^beta (where tau = 2*pi, alpha/beta not in Q).

Special Families:
1. CANONICAL_MINIMAL_RANK_TWO_BASE_ONE: (1, sqrt(2))
2. CANONICAL_MINIMAL_RANK_TWO_INCOMMENSURABLE_RADICALS: (sqrt(2), sqrt(3))
3. QUADRATIC_CONJUGATE_PAIR: (a + b*sqrt(d), a - b*sqrt(d)) with a, b in Q \ {0}
4. GENERAL_RANK_TWO_ALGEBRAIC_PAIR: arbitrary Q-independent algebraic grades.

Structural Reductions:
- Trace/Norm Product Law:
    For conjugate exponents alpha = a + b*sqrt(d), alpha' = a - b*sqrt(d):
    X * X' = tau^(alpha + alpha') = tau^(2*a) = (2*pi)^(2*a).
    If 2*a = p/q in Q \ {0}, then (X * X')^q = (2*pi)^p.
    By Lindemann's theorem (1882), (2*pi)^p is transcendental, hence X * X' is
    UNCONDITIONALLY TRANSCENDENTAL over Q (never algebraic).
    This yields an exact algebraic relation over Q_bar(2*pi), while remaining
    unconditionally open over Q_bar alone.
- Monomial Reductions:
    For any (m, n) in Z^2 \ {(0,0)}, M_{m,n} = X^m * Y^n = tau^(m*alpha + n*beta).
    If m*alpha + n*beta = p/q in Q \ {0}:
        M_{m,n} is UNCONDITIONALLY TRANSCENDENTAL by Lindemann (1882).
    If m*alpha + n*beta is irrational:
        M_{m,n} in Q_bar <==> m*alpha + n*beta in S_tau.
        Reduces strictly to the rank-1 classification set S_tau (dim_Q S_tau <= 1).
- Linear Binomial Relations:
    c1 * X + c2 * Y = 0 (c1, c2 in Q_bar \ {0}) forces Y / X = tau^(beta - alpha) in Q_bar.
    If beta - alpha in Q \ {0}, unconditionally impossible by Lindemann.
    If beta - alpha not in Q, reduces to beta - alpha in S_tau.
- Certified Finite Exclusions:
    Certified interval arithmetic (python-flint Arb) excludes non-zero polynomials
    P(X, Y) in Z[X, Y] over declared finite degree and height bounds without midpoint leakage.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import flint
from flint import arb, arb_poly, ctx
import sympy as sp
from sympy import Rational, Integer, sqrt, Symbol

from tc.ambient_kernel import (
    expr_to_arb,
    compute_rational_support_rank,
    CANONICAL_MINIMAL_RANK_TWO_OPEN_INSTANCE,
)


PAIR_TYPE_BASE_ONE = "CANONICAL_MINIMAL_RANK_TWO_BASE_ONE"
PAIR_TYPE_INCOMMENSURABLE_RADICALS = "CANONICAL_MINIMAL_RANK_TWO_INCOMMENSURABLE_RADICALS"
PAIR_TYPE_QUADRATIC_CONJUGATES = "QUADRATIC_CONJUGATE_PAIR"
PAIR_TYPE_GENERAL = "GENERAL_RANK_TWO_ALGEBRAIC_PAIR"


@dataclass(frozen=True)
class PairClassificationResult:
    pair_type: str
    alpha_expr: sp.Expr
    beta_expr: sp.Expr
    rational_support_rank: int
    is_base_one: bool
    is_quadratic_conjugate: bool
    trace_val: Optional[sp.Rational]
    norm_val: Optional[sp.Rational]
    description: str


def classify_rank_two_pair(alpha: sp.Expr, beta: sp.Expr) -> PairClassificationResult:
    """Classify a pair of algebraic grades (alpha, beta) into canonical rank-two families."""
    alpha_sym = sp.sympify(alpha)
    beta_sym = sp.sympify(beta)

    # Check rational rank of {0, alpha, beta}
    rank, _ = compute_rational_support_rank([sp.Integer(0), alpha_sym, beta_sym])
    if rank != 2:
        raise ValueError(
            f"Expected rational support rank 2, but got rank {rank} for alpha={alpha_sym}, beta={beta_sym}."
        )

    # Check Base-One: alpha == 1 or beta == 1
    if alpha_sym == sp.Integer(1) or beta_sym == sp.Integer(1):
        irr = beta_sym if alpha_sym == sp.Integer(1) else alpha_sym
        return PairClassificationResult(
            pair_type=PAIR_TYPE_BASE_ONE,
            alpha_expr=alpha_sym,
            beta_expr=beta_sym,
            rational_support_rank=2,
            is_base_one=True,
            is_quadratic_conjugate=False,
            trace_val=None,
            norm_val=None,
            description=f"Base-one canonical rank-two instance (1, {irr}).",
        )

    # Check Quadratic Conjugate: alpha = a + b*sqrt(d), beta = a - b*sqrt(d)
    diff = sp.simplify(alpha_sym - beta_sym)
    total = sp.simplify(alpha_sym + beta_sym)
    if total.is_rational and not diff.is_rational:
        # Trace is rational, difference is irrational
        # Check if product is also rational (norm)
        prod = sp.simplify(alpha_sym * beta_sym)
        if prod.is_rational:
            return PairClassificationResult(
                pair_type=PAIR_TYPE_QUADRATIC_CONJUGATES,
                alpha_expr=alpha_sym,
                beta_expr=beta_sym,
                rational_support_rank=2,
                is_base_one=False,
                is_quadratic_conjugate=True,
                trace_val=sp.Rational(total),
                norm_val=sp.Rational(prod),
                description=(
                    f"Quadratic conjugate pair in Q(sqrt(d)) with rational trace {total} "
                    f"and rational norm {prod}."
                ),
            )

    # Check Incommensurable Radicals: alpha = sqrt(d1), beta = sqrt(d2)
    # where d1, d2 are positive square-free integers
    def _is_simple_sqrt(e: sp.Expr) -> Optional[int]:
        if isinstance(e, sp.Pow) and e.exp == sp.Rational(1, 2) and e.base.is_integer:
            return int(e.base)
        return None

    d1 = _is_simple_sqrt(alpha_sym)
    d2 = _is_simple_sqrt(beta_sym)
    if d1 is not None and d2 is not None:
        return PairClassificationResult(
            pair_type=PAIR_TYPE_INCOMMENSURABLE_RADICALS,
            alpha_expr=alpha_sym,
            beta_expr=beta_sym,
            rational_support_rank=2,
            is_base_one=False,
            is_quadratic_conjugate=False,
            trace_val=None,
            norm_val=None,
            description=f"Incommensurable radicals canonical instance (sqrt({d1}), sqrt({d2})).",
        )

    return PairClassificationResult(
        pair_type=PAIR_TYPE_GENERAL,
        alpha_expr=alpha_sym,
        beta_expr=beta_sym,
        rational_support_rank=2,
        is_base_one=False,
        is_quadratic_conjugate=False,
        trace_val=None,
        norm_val=None,
        description=f"General rank-two algebraic pair ({alpha_sym}, {beta_sym}).",
    )


@dataclass(frozen=True)
class QuadraticConjugateProductResult:
    alpha: sp.Expr
    beta: sp.Expr
    trace: sp.Rational
    p: int
    q: int
    relation_over_qbar_tau: str
    product_transcendence_status: str
    product_algebraicity_status: str
    evidence_class: str


def evaluate_quadratic_conjugate_product(
    alpha: sp.Expr, beta: sp.Expr
) -> QuadraticConjugateProductResult:
    """Analyze the trace and product law for a quadratic conjugate pair.

    For alpha = a + b*sqrt(d) and beta = a - b*sqrt(d):
    alpha + beta = 2*a = p/q in Q.
    Then X * X' = tau^(alpha + beta) = tau^(p/q) = (2*pi)^(p/q).
    Equivalently: (X * X')^q = (2*pi)^p.
    By Lindemann (1882), (2*pi)^p is transcendental for p != 0,
    so X * X' is UNCONDITIONALLY TRANSCENDENTAL (never algebraic).
    """
    cls = classify_rank_two_pair(alpha, beta)
    if not cls.is_quadratic_conjugate or cls.trace_val is None:
        raise ValueError(f"Pair ({alpha}, {beta}) is not a quadratic conjugate pair.")

    trace = cls.trace_val
    if trace == 0:
        raise ValueError(
            f"Pure imaginary / traceless conjugate pair alpha + beta = 0 has rational rank 1, not 2."
        )

    p = int(trace.p)
    q = int(trace.q)

    relation = f"(X * X')^{q} = (2*pi)^{p}"
    return QuadraticConjugateProductResult(
        alpha=cls.alpha_expr,
        beta=cls.beta_expr,
        trace=trace,
        p=p,
        q=q,
        relation_over_qbar_tau=relation,
        product_transcendence_status="PROVED_TRANSCENDENTAL_LINDEMANN",
        product_algebraicity_status="REFUTED_WITHIN_SCOPE",
        evidence_class="CERTIFIED_EXACT_DEDUCTION",
    )


@dataclass(frozen=True)
class MonomialReductionResult:
    alpha: sp.Expr
    beta: sp.Expr
    m: int
    n: int
    combined_exponent: sp.Expr
    is_rational: bool
    status: str
    algebraic_relation_possible: bool
    explanation: str


def analyze_monomial_relation(
    alpha: sp.Expr, beta: sp.Expr, m: int, n: int
) -> MonomialReductionResult:
    r"""Analyze the arithmetic nature of a Laurent monomial X^m * Y^n = tau^(m*alpha + n*beta).

    For (m, n) != (0, 0):
    1. If m*alpha + n*beta = p/q in Q \ {0}:
       tau^(p/q) = (2*pi)^(p/q) is UNCONDITIONALLY TRANSCENDENTAL by Lindemann (1882).
       Therefore X^m * Y^n cannot be algebraic: no algebraic monomial relation of this grade exists.
    2. If m*alpha + n*beta is irrational:
       X^m * Y^n in Q_bar <==> m*alpha + n*beta in S_tau.
       Reduces strictly to the rank-1 classification set S_tau (dim_Q S_tau <= 1).
    """
    if m == 0 and n == 0:
        raise ValueError("Monomial exponents (m, n) cannot both be zero.")

    alpha_sym = sp.sympify(alpha)
    beta_sym = sp.sympify(beta)
    comb = sp.simplify(m * alpha_sym + n * beta_sym)

    if comb.is_rational:
        p = int(comb.p)
        q = int(comb.q)
        return MonomialReductionResult(
            alpha=alpha_sym,
            beta=beta_sym,
            m=m,
            n=n,
            combined_exponent=comb,
            is_rational=True,
            status="PROVED_TRANSCENDENTAL_LINDEMANN",
            algebraic_relation_possible=False,
            explanation=(
                f"Combined exponent m*alpha + n*beta = {comb} is rational and non-zero. "
                f"By Lindemann (1882), tau^({p}/{q}) = (2*pi)^({p}/{q}) is proved transcendental. "
                f"Hence X^{m} * Y^{n} is unconditionally transcendental and cannot equal an algebraic number."
            ),
        )
    else:
        return MonomialReductionResult(
            alpha=alpha_sym,
            beta=beta_sym,
            m=m,
            n=n,
            combined_exponent=comb,
            is_rational=False,
            status="REDUCES_TO_S_TAU",
            algebraic_relation_possible=True,  # only if combined_exponent in S_tau
            explanation=(
                f"Combined exponent m*alpha + n*beta = {comb} is irrational. "
                f"X^{m} * Y^{n} is algebraic if and only if {comb} in S_tau. "
                f"By Gelfond-Schneider, dim_Q S_tau <= 1. Under Schanuel, S_tau = {{0}}."
            ),
        )


def get_sharp_unconditional_boundary_matrix() -> Dict[str, Any]:
    """Return the structured boundary matrix comparing unconditional vs conditional knowledge across ranks 0, 1, and 2."""
    return {
        "framework": "Riemann Scope: Unconditional Rank-Two Algebraic-Power Frontier",
        "reference_base": "tau = 2*pi",
        "ranks": {
            "rank_0": {
                "support_type": "Identical grades (Delta_K = 0)",
                "unconditional_status": "PROVED_EXACT_EQUIVALENCE",
                "mathematical_mechanism": "Trivial coefficient cancellation: sum c_i * tau^K0 = (sum c_i) * tau^K0 = 0 <==> sum c_i = 0.",
                "open_questions": None,
            },
            "rank_1_rational": {
                "support_type": "Rational grades alpha = p/q in Q without {0}",
                "unconditional_status": "PROVED_INJECTIVE_LINDEMANN",
                "mathematical_mechanism": "Lindemann (1882): pi is transcendental ==> (2*pi)^(p/q) is transcendental ==> ev_tau is injective on Q*alpha.",
                "open_questions": None,
            },
            "rank_1_irrational": {
                "support_type": "Single irrational grade alpha in (Q_bar without Q)",
                "unconditional_status": "EXACTLY_CLASSIFIED_BY_S_TAU",
                "mathematical_mechanism": "ev_tau has non-trivial kernel on Q*alpha <==> alpha in S_tau. Gelfond-Schneider forces dim_Q S_tau <= 1. Conditionally S_tau = {0}.",
                "open_questions": "Whether S_tau = {0} unconditionally (Baker-type open problem for transcendental base 2*pi).",
            },
            "rank_2_linear_binomial": {
                "support_type": "Two generators c1 * X + c2 * Y = 0 (c1, c2 in Q_bar without {0})",
                "unconditional_status": "PARTIALLY_PROVED_LINDEMANN_AND_REDUCED",
                "mathematical_mechanism": (
                    "Y / X = tau^(beta - alpha) in Q_bar. "
                    "If beta - alpha in Q without {0}, UNCONDITIONALLY IMPOSSIBLE by Lindemann. "
                    "If beta - alpha not in Q, reduces strictly to beta - alpha in S_tau."
                ),
                "open_questions": "Only irrational differences beta - alpha outside Q.",
            },
            "rank_2_monomial": {
                "support_type": "Laurent monomials X^m * Y^n = tau^(m*alpha + n*beta)",
                "unconditional_status": "PARTIALLY_PROVED_LINDEMANN_AND_REDUCED",
                "mathematical_mechanism": (
                    "If m*alpha + n*beta in Q without {0}, UNCONDITIONALLY TRANSCENDENTAL by Lindemann (1882). "
                    "If m*alpha + n*beta not in Q, reduces strictly to m*alpha + n*beta in S_tau."
                ),
                "open_questions": "Monomials with irrational combined exponents.",
            },
            "rank_2_quadratic_conjugate_product": {
                "support_type": "Quadratic conjugate pair (a + b*sqrt(d), a - b*sqrt(d))",
                "unconditional_status": "PROVED_TRANSCENDENTAL_LINDEMANN_OVER_QBAR_TAU",
                "mathematical_mechanism": (
                    "Trace law: X * X' = tau^(2*a) = (2*pi)^(p/q). "
                    "Unconditionally transcendental by Lindemann (1882). "
                    "Gives exact algebraic relation over Q_bar(2*pi): (X * X')^q - (2*pi)^p = 0. "
                    "Transcendence degree over Q_bar(2*pi) is at most 1."
                ),
                "open_questions": "Algebraic independence of X, X' over Q_bar alone.",
            },
            "rank_2_general_polynomial": {
                "support_type": "General polynomial P(X, Y) in Q_bar[X, Y] for alpha/beta not in Q",
                "unconditional_status": "OPEN_FRONTIER_WITH_CERTIFIED_FINITE_EXCLUSIONS",
                "mathematical_mechanism": (
                    "Unconditional: Open in modern transcendental number theory (Four/Six Exponentials "
                    "trivially satisfied by e and 2*pi without constraining tau^alpha). "
                    "Certified finite exclusion by Arb ball arithmetic on any compact coefficient/degree box. "
                    "Conditional: PROVED_CONDITIONAL_SCHANUEL (ev_tau injective on every finite algebraic-grade support)."
                ),
                "open_questions": "Unconditional algebraic independence of (2*pi, (2*pi)^sqrt(2)) and ((2*pi)^sqrt(2), (2*pi)^sqrt(3)).",
            },
        },
    }


def certify_rank_two_polynomial_exclusion(
    alpha: sp.Expr,
    beta: sp.Expr,
    max_degree: int = 2,
    height_bound: int = 2,
    dps: int = 100,
) -> Dict[str, Any]:
    """Rigorously certify non-vanishing of all integer polynomials P(X, Y) != 0

    up to max_degree and height_bound for X = tau^alpha, Y = tau^beta using Arb ball arithmetic.
    Fails closed: raises ValueError if any ball contains zero or precision is insufficient.
    """
    ctx.dps = dps

    alpha_arb = expr_to_arb(alpha)
    beta_arb = expr_to_arb(beta)

    tau_arb = arb.pi() * 2
    log_tau = tau_arb.log()

    X = (alpha_arb * log_tau).exp()
    Y = (beta_arb * log_tau).exp()

    # Precompute powers
    X_pows = [arb(1)]
    for _ in range(max_degree):
        X_pows.append(X_pows[-1] * X)

    Y_pows = [arb(1)]
    for _ in range(max_degree):
        Y_pows.append(Y_pows[-1] * Y)

    total_tested = 0
    min_lower_bound = None

    coeffs_range = list(range(-height_bound, height_bound + 1))
    monomial_indices = [
        (i, j)
        for i in range(max_degree + 1)
        for j in range(max_degree + 1)
        if i + j <= max_degree
    ]
    num_monomials = len(monomial_indices)

    # Enumerate non-zero coefficient vectors
    for c_tuple in itertools.product(coeffs_range, repeat=num_monomials):
        if all(c == 0 for c in c_tuple):
            continue

        val = arb(0)
        for c, (i, j) in zip(c_tuple, monomial_indices):
            if c != 0:
                val += arb(c) * X_pows[i] * Y_pows[j]

        # Rigorous lower bound on |val|
        lower_bnd = val.abs_lower()
        if lower_bnd <= 0:
            raise ValueError(
                f"CERTIFICATION_FAILED: Polynomial with coefficients {c_tuple} "
                f"has ball {val} containing zero at dps={dps}."
            )

        float_lower = float(lower_bnd)
        if min_lower_bound is None or float_lower < min_lower_bound:
            min_lower_bound = float_lower

        total_tested += 1

    return {
        "alpha": str(alpha),
        "beta": str(beta),
        "max_degree": max_degree,
        "height_bound": height_bound,
        "dps": dps,
        "total_polynomials_tested": total_tested,
        "min_rigorous_lower_bound": min_lower_bound,
        "status": "CERTIFIED_FINITE_RELATION_EXCLUSION",
        "evidence_class": "CERTIFIED_FINITE",
    }
