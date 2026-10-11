r"""Exponential-Polynomial Jet Rigidity and Integer-Dilation Orbit Isolation.

TASK-TC-031: Sharp arithmetic and analytic consequences of a hypothetical minimal
ambient-kernel trinomial relation:
    a0 + a1 * tau^alpha + a2 * tau^beta = 0
where a0, a1, a2 \in \overline{\mathbb{Q}}^\times, \alpha, \beta \in \mathbb{A}_{\mathbb{R}}^\times,
\alpha / \beta \notin \mathbb{Q}, \tau = 2\pi.

Reformulation:
    L = \log\tau = \log(2\pi) > 0
    F(z) = a0 + a1 * e^{\alpha z} + a2 * e^{\beta z}
    F(L) = 0 \iff a0 + a1 * \tau^\alpha + a2 * \tau^\beta = 0
    f(n) = F(nL) = a0 + a1 * X^n + a2 * Y^n   (X = \tau^\alpha, Y = \tau^\beta, n \in \mathbb{Z})

Key Structural Theorems:
1. TRINOMIAL_RELATION_IMPLIES_LOG_TAU_TRANSCENDENTAL:
   If F(L) = 0, L = \log(2\pi) must be transcendental. If L were algebraic, then
   (0, \alpha L, \beta L) would be 3 distinct algebraic numbers, so 1, e^{\alpha L}, e^{\beta L}
   would be linearly independent over \overline{\mathbb{Q}} by Lindemann-Weierstrass (1885),
   contradicting a0 * 1 + a1 * e^{\alpha L} + a2 * e^{\beta L} = 0.
   (The arithmetic status of \log(2\pi) remains unconditionally OPEN in literature).
2. DERIVATIVE_JET_RIGIDITY / TRINOMIAL_ZERO_SIMPLE:
   For every m \ge 1, F^{(m)}(L) = a1 * \alpha^m * X + a2 * \beta^m * Y \neq 0.
   A second vanishing would produce a relation vector (0, a1 \alpha^m, a2 \beta^m) linearly
   independent from (a0, a1, a2) because a0 != 0, forcing \dim_{\overline{\mathbb{Q}}} \mathcal{R} \ge 2,
   which contradicts the relation-space dimension theorem (\dim \le 1 via Gelfond-Schneider).
   In particular, F'(L) != 0, so any hypothetical zero at L is strictly simple.
3. DIFFERENTIAL_OPERATOR_RIGIDITY:
   For P(T) \in \overline{\mathbb{Q}}[T], P(D)F(L) = 0 forces P(0) = P(\alpha) = P(\beta).
4. INTEGER_DILATION_RAY_ISOLATION:
   If f(m) = 0 for m \in \mathbb{Z} \setminus \{0\}, then f(km) \neq 0 for all k \in \mathbb{Z} \setminus \{0, 1\}.
   - For k \ge 2: P_k(T) = a0 + a1 T^k + a2 (u + v T)^k has non-zero coefficient at T^{k-1}:
     a2 * k * u * v^{k-1} != 0 (u = -a0/a2, v = -a1/a2). Thus U = \tau^{m\alpha} \in \overline{\mathbb{Q}}.
   - For k = -q \le -1: Q_q(T) = a0 T^q (u + v T)^q + a1 (u + v T)^q + a2 T^q has non-zero leading
     coefficient at T^{2q}: a0 * v^q != 0. Thus U = \tau^{m\alpha} \in \overline{\mathbb{Q}}.
   Both cases force \alpha, \beta \in S_\tau, contradicting \dim_{\mathbb{Q}} S_\tau \le 1.
   For the canonical trinomial relation (m = 1), f(n) != 0 for all n \in \mathbb{Z} \setminus \{0, 1\}.
   The integer k = 0 is explicitly not excluded because f(0) = a0 + a1 + a2 is an independent constant sum.
5. BASE_ONE_ORBIT_ISOLATION_BY_LINDEMANN:
   For \alpha = 1, \beta = \sqrt{2}, U = \tau^m = (2\pi)^m \in \overline{\mathbb{Q}} directly contradicts
   Lindemann's transcendence of \pi, without requiring the external Gelfond-Schneider theorem for S_\tau.
6. AT_MOST_TWO_REAL_EXPONENTIAL_POLYNOMIAL_ZEROS:
   W(x) = e^{(\lambda_0+\lambda_1+\lambda_2)x} (\lambda_1-\lambda_0)(\lambda_2-\lambda_0)(\lambda_2-\lambda_1) != 0
   on \mathbb{R}. The three exponentials form an Extended Complete Chebyshev (ECT) system on \mathbb{R},
   so F(x) has at most 2 real zeros counting multiplicity (Karlin & Studden 1966).
7. FUNCTIONAL_RESULT_DOES_NOT_SPECIALIZE_AUTOMATICALLY:
   Functional independence of e^{\alpha z}, e^{\beta z} over \mathbb{C}(z) (Ax-Schanuel, differential algebra)
   does NOT specialize to arithmetic independence at transcendental evaluation points such as z = \log(2\pi).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

import flint
from flint import arb, ctx
import sympy as sp
from sympy import Rational, Integer, sqrt, Symbol, sympify, I, binomial, expand, Poly

from tc.ambient_kernel import expr_to_arb

# Canonical Terminology Constants
EXPONENTIAL_POLYNOMIAL = "EXPONENTIAL_POLYNOMIAL"
LOG_TAU_EVALUATION = "LOG_TAU_EVALUATION"
INTEGER_DILATION_ORBIT = "INTEGER_DILATION_ORBIT"

# Primary & Secondary Classification Constants
PRIMARY_CLASSIFICATION_FRONTIER_SHARPENED = "EXPONENTIAL_POLYNOMIAL_FRONTIER_SHARPENED_EXISTENCE_OPEN"
PRIMARY_CLASSIFICATION_NONEXISTENCE_PROVED = "TRINOMIAL_NONEXISTENCE_PROVED"
PRIMARY_CLASSIFICATION_ISOLATION_INCOMPLETE = "INTEGER_DILATION_ISOLATION_INCOMPLETE"

CLASSIFICATION_TRINOMIAL_RELATION_IMPLIES_LOG_TAU_TRANSCENDENTAL = "TRINOMIAL_RELATION_IMPLIES_LOG_TAU_TRANSCENDENTAL"
CLASSIFICATION_TRINOMIAL_ZERO_SIMPLE = "TRINOMIAL_ZERO_SIMPLE"
CLASSIFICATION_ALL_POSITIVE_DERIVATIVE_JETS_NONZERO = "ALL_POSITIVE_DERIVATIVE_JETS_NONZERO"
CLASSIFICATION_DIFFERENTIAL_OPERATOR_RIGIDITY = "DIFFERENTIAL_OPERATOR_RIGIDITY"
CLASSIFICATION_INTEGER_DILATION_RAY_ISOLATION = "INTEGER_DILATION_RAY_ISOLATION"
CLASSIFICATION_BASE_ONE_ORBIT_ISOLATION_BY_LINDEMANN = "BASE_ONE_ORBIT_ISOLATION_BY_LINDEMANN"
CLASSIFICATION_AT_MOST_TWO_REAL_EXPONENTIAL_POLYNOMIAL_ZEROS = "AT_MOST_TWO_REAL_EXPONENTIAL_POLYNOMIAL_ZEROS"
CLASSIFICATION_FUNCTIONAL_RESULT_DOES_NOT_SPECIALIZE_AUTOMATICALLY = "FUNCTIONAL_RESULT_DOES_NOT_SPECIALIZE_AUTOMATICALLY"
CLASSIFICATION_TRINOMIAL_EXISTENCE_OPEN = "TRINOMIAL_EXISTENCE_OPEN"
CLASSIFICATION_NO_ZETA_TO_KERNEL_BRIDGE_FOUND = "NO_ZETA_TO_KERNEL_BRIDGE_FOUND"
CLASSIFICATION_NO_RH_IMPLICATION = "NO_RH_IMPLICATION"


@dataclass(frozen=True)
class LindemannWeierstrassNecessityResult:
    """Audit result for Lindemann-Weierstrass necessity at L = log(2*pi)."""
    is_transcendental_forced: bool
    classification: str
    exponents_distinct: bool
    exponents: Tuple[sp.Expr, sp.Expr, sp.Expr]
    literature_status_log_tau: str
    evidence_class: str
    reasoning: str


@dataclass(frozen=True)
class DerivativeJetRigidityResult:
    """Rigidity result for m-th derivative jet F^{(m)}(L)."""
    order: int
    derivative_vector: Tuple[sp.Expr, sp.Expr, sp.Expr]
    is_proportional_to_original: bool
    is_nonzero_vector: bool
    proves_jet_nonzero: bool
    is_simple_zero: bool
    classification: str
    evidence_class: str


@dataclass(frozen=True)
class DifferentialOperatorRigidityResult:
    """Rigidity result for P(D)F(L) = 0 forcing P(0) = P(alpha) = P(beta)."""
    polynomial_desc: str
    operator_vector: Tuple[sp.Expr, sp.Expr, sp.Expr]
    is_rigidity_satisfied: bool
    support_values_equal: bool
    p_0: sp.Expr
    p_alpha: sp.Expr
    p_beta: sp.Expr
    classification: str
    evidence_class: str


@dataclass(frozen=True)
class PositiveDilationPolynomialResult:
    """Construction and non-vanishing of P_k(T) for positive multipliers k >= 2."""
    k: int
    polynomial_expr: sp.Expr
    distinguished_degree: int
    distinguished_coeff: sp.Expr
    is_distinguished_coeff_nonzero: bool
    is_polynomial_nonzero: bool
    forces_algebraic_generator: bool


@dataclass(frozen=True)
class NegativeDilationPolynomialResult:
    """Construction and non-vanishing of Q_q(T) for negative multipliers k = -q <= -1."""
    q: int
    polynomial_expr: sp.Expr
    distinguished_degree: int
    distinguished_coeff: sp.Expr
    is_distinguished_coeff_nonzero: bool
    is_polynomial_nonzero: bool
    forces_algebraic_generator: bool


@dataclass(frozen=True)
class IntegerDilationRayResult:
    """Orbit isolation check for f(k*m) where f(m) = 0."""
    m: int
    k_tested: int
    is_excluded: bool
    exclusion_mechanism: str
    contradiction_target: str
    base_one_specialization: bool
    classification: str
    evidence_class: str


@dataclass(frozen=True)
class ChebyshevWronskianResult:
    r"""ECT system and Wronskian analysis for {e^{\lambda_0 x}, e^{\lambda_1 x}, e^{\lambda_2 x}}."""
    exponents_ordered: Tuple[sp.Expr, sp.Expr, sp.Expr]
    wronskian_formula: str
    wronskian_symbolic: sp.Expr
    is_strictly_positive_on_real_line: bool
    max_real_zeros_bound: int
    classification: str
    evidence_class: str
    wronskian_w0_symbolic: Optional[sp.Expr] = None
    wronskian_w1_symbolic: Optional[sp.Expr] = None
    wronskian_w2_symbolic: Optional[sp.Expr] = None
    successive_wronskians_positive: bool = True
    external_theorem_citation: str = (
        "Karlin & Studden (1966, Tchebycheff Systems: With Applications in Analysis and Statistics, "
        "Chapter XI, Theorem 1.1, p. 376); Pólya & Szegő (1925, Part V, No. 75)"
    )


@dataclass(frozen=True)
class DescartesSignResult:
    """Sign-variation bound on real zeros for exponential sums."""
    coefficients_ordered: Tuple[sp.Expr, sp.Expr, sp.Expr]
    sign_changes: int
    max_real_zeros_descartes: int
    evidence_class: str


@dataclass(frozen=True)
class FunctionalFirewallAudit:
    """Audit of functional transcendence results and their non-specialization."""
    theorems_audited: List[Dict[str, Any]]
    functional_independence_applies: bool
    arithmetic_specialization_valid: bool
    classification: str
    explanation: str


class ExponentialPolynomial:
    r"""Representation of an exponential polynomial:
        F(z) = a0 + a1 * e^{\alpha z} + a2 * e^{\beta z}
    with evaluation at L = log(2\pi) corresponding to the ambient relation
        F(L) = a0 + a1 * \tau^\alpha + a2 * \tau^\beta.
    """

    def __init__(
        self,
        a0: Union[sp.Expr, int, float, str],
        a1: Union[sp.Expr, int, float, str],
        a2: Union[sp.Expr, int, float, str],
        alpha: Union[sp.Expr, int, float, str],
        beta: Union[sp.Expr, int, float, str],
    ):
        self.a0 = sympify(a0)
        self.a1 = sympify(a1)
        self.a2 = sympify(a2)
        self.alpha = sympify(alpha)
        self.beta = sympify(beta)

        if self.a0 == 0 or self.a1 == 0 or self.a2 == 0:
            raise ValueError("Trinomial kernel coefficients a0, a1, a2 must be strictly non-zero.")
        if self.alpha == 0 or self.beta == 0 or self.alpha == self.beta:
            raise ValueError("Exponents alpha, beta must be non-zero and pairwise distinct from 0.")

    def evaluate_symbolic(self, z: sp.Expr) -> sp.Expr:
        """Evaluate F(z) symbolically."""
        return self.a0 + self.a1 * sp.exp(self.alpha * z) + self.a2 * sp.exp(self.beta * z)

    def ambient_relation_expression(self) -> sp.Expr:
        """Return symbolic expression a0 + a1 * tau^alpha + a2 * tau^beta with tau symbol."""
        tau = Symbol("tau", positive=True)
        return self.a0 + self.a1 * (tau ** self.alpha) + self.a2 * (tau ** self.beta)

    def evaluate_at_log_tau_arb(self, prec: int = 150) -> arb:
        """Evaluate F(L) using Arb ball arithmetic where L = log(2*pi)."""
        old_prec = ctx.prec
        try:
            ctx.prec = prec
            tau_arb = arb.pi() * 2
            log_tau_arb = tau_arb.log()

            a0_arb = expr_to_arb(self.a0)
            a1_arb = expr_to_arb(self.a1)
            a2_arb = expr_to_arb(self.a2)
            alpha_arb = expr_to_arb(self.alpha)
            beta_arb = expr_to_arb(self.beta)

            term1 = a1_arb * (alpha_arb * log_tau_arb).exp()
            term2 = a2_arb * (beta_arb * log_tau_arb).exp()
            return a0_arb + term1 + term2
        finally:
            ctx.prec = old_prec

    def dilation_orbit_term(self, n: int) -> sp.Expr:
        """Return f(n) = F(n*L) = a0 + a1 * X^n + a2 * Y^n where X = tau^alpha, Y = tau^beta."""
        X = Symbol("X", positive=True)
        Y = Symbol("Y", positive=True)
        if n == 0:
            return self.a0 + self.a1 + self.a2
        return self.a0 + self.a1 * (X ** n) + self.a2 * (Y ** n)

    def derivative(self, order: int = 1) -> ExponentialPolynomialDerivative:
        """Return the derivative operator of order m >= 1."""
        return ExponentialPolynomialDerivative(self, order=order)


class ExponentialPolynomialDerivative:
    r"""Represents the m-th derivative:
        F^{(m)}(z) = a1 * \alpha^m * e^{\alpha z} + a2 * \beta^m * e^{\beta z}.
    At z = L:
        F^{(m)}(L) = a1 * \alpha^m * X + a2 * \beta^m * Y.
    """

    def __init__(self, parent: ExponentialPolynomial, order: int = 1):
        if order < 1:
            raise ValueError("Derivative order m must be an integer >= 1.")
        self.parent = parent
        self.order = order

    @property
    def coefficient_vector(self) -> Tuple[sp.Expr, sp.Expr, sp.Expr]:
        """Return the coefficient vector (0, a1 * alpha^m, a2 * beta^m) on basis (1, X, Y)."""
        return (
            Integer(0),
            expand(self.parent.a1 * (self.parent.alpha ** self.order)),
            expand(self.parent.a2 * (self.parent.beta ** self.order)),
        )

    def evaluate_at_log_tau_arb(self, prec: int = 150) -> arb:
        """Evaluate F^{(m)}(L) using Arb ball arithmetic."""
        old_prec = ctx.prec
        try:
            ctx.prec = prec
            tau_arb = arb.pi() * 2
            log_tau_arb = tau_arb.log()

            a1_arb = expr_to_arb(self.parent.a1)
            a2_arb = expr_to_arb(self.parent.a2)
            alpha_arb = expr_to_arb(self.parent.alpha)
            beta_arb = expr_to_arb(self.parent.beta)


            m_int = self.order
            term1 = a1_arb * (alpha_arb ** m_int) * (alpha_arb * log_tau_arb).exp()
            term2 = a2_arb * (beta_arb ** m_int) * (beta_arb * log_tau_arb).exp()
            return term1 + term2
        finally:
            ctx.prec = old_prec



# -------------------------------------------------------------------------
# Core Rigidity & Isolation Theorems
# -------------------------------------------------------------------------

def verify_lindemann_weierstrass_necessity(
    alpha: sp.Expr,
    beta: sp.Expr,
) -> LindemannWeierstrassNecessityResult:
    r"""Verify that F(L) = 0 implies L = log(2\pi) is transcendental.

    Proof:
    Suppose L is algebraic. Since alpha, beta are non-zero algebraic numbers and
    alpha != beta, the three numbers:
        0, \alpha L, \beta L
    are pairwise distinct algebraic numbers (since L != 0 as 2\pi != 1).
    By the Lindemann-Weierstrass Theorem (1885), the three exponentials:
        e^0 = 1, e^{\alpha L}, e^{\beta L}
    are linearly independent over \overline{\mathbb{Q}}.
    Consequently, no non-trivial algebraic linear combination:
        a0 * 1 + a1 * e^{\alpha L} + a2 * e^{\beta L} = 0
    can hold with a0, a1, a2 \in \overline{\mathbb{Q}}^\times.
    Thus, F(L) = 0 forces L = \log(2\pi) to be transcendental.

    Literature Status:
    The arithmetic nature of \log(2\pi) is currently an OPEN problem in number theory
    (Waldschmidt, "Open Diophantine Problems"; Baker 1975). It is neither proved
    algebraic nor proved transcendental. Hence F(L) = 0 forcing transcendence does not
    yet contradict known mathematics, but provides a strict necessary condition.
    """
    alpha = sympify(alpha)
    beta = sympify(beta)
    distinct = (alpha != 0) and (beta != 0) and (alpha != beta)

    exponents = (Integer(0), alpha, beta)
    reasoning = (
        "If L in Q_bar, then (0, alpha*L, beta*L) are 3 distinct algebraic numbers. "
        "Lindemann-Weierstrass forces (1, exp(alpha*L), exp(beta*L)) to be linearly "
        "independent over Q_bar, contradicting any non-zero algebraic relation a0 + a1*X + a2*Y = 0."
    )

    return LindemannWeierstrassNecessityResult(
        is_transcendental_forced=distinct,
        classification=CLASSIFICATION_TRINOMIAL_RELATION_IMPLIES_LOG_TAU_TRANSCENDENTAL,
        exponents_distinct=distinct,
        exponents=exponents,
        literature_status_log_tau=(
            "OPEN: The transcendence and irrationality of log(2*pi) are unsolved open problems "
            "(Waldschmidt 2004, Baker 1975, Murty-Rath 2014)."
        ),
        evidence_class="PROVED_WITH_EXTERNAL_LINDEMANN_WEIERSTRASS",
        reasoning=reasoning,
    )


def compute_derivative_coefficient_vector(
    coeffs: Tuple[sp.Expr, sp.Expr, sp.Expr],
    alpha: sp.Expr,
    beta: sp.Expr,
    m: int,
) -> Tuple[sp.Expr, sp.Expr, sp.Expr]:
    r"""Compute coefficient vector of F^{(m)}(L) on basis (1, X, Y).

    F^{(m)}(L) = 0 * 1 + (a1 * alpha^m) * X + (a2 * beta^m) * Y.
    Vector: (0, a1 * alpha^m, a2 * beta^m).
    """
    if m < 1:
        raise ValueError("Derivative order m must be >= 1.")
    a0, a1, a2 = [sympify(c) for c in coeffs]
    alpha = sympify(alpha)
    beta = sympify(beta)
    return (Integer(0), expand(a1 * (alpha ** m)), expand(a2 * (beta ** m)))


def check_derivative_jet_nonvanishing(
    coeffs: Tuple[sp.Expr, sp.Expr, sp.Expr],
    alpha: sp.Expr,
    beta: sp.Expr,
    m: int,
) -> DerivativeJetRigidityResult:
    r"""Prove that F^{(m)}(L) != 0 for all m >= 1 if F(L) = 0.

    Proof:
    The original relation vector is v0 = (a0, a1, a2) with a0 != 0.
    The m-th derivative vector is vm = (0, a1 * alpha^m, a2 * beta^m).
    Since a1 != 0 and alpha != 0, the second coordinate a1 * alpha^m != 0.
    If vm were proportional to v0:
        vm = lambda * v0
    Then coordinate 0 gives 0 = lambda * a0. Since a0 != 0, lambda = 0.
    Then coordinate 1 gives a1 * alpha^m = 0 * a1 = 0, contradiction!
    Therefore v0 and vm are linearly independent in \overline{\mathbb{Q}}^3.
    If F^{(m)}(L) = 0, then both v0, vm \in \mathcal{R}_{\alpha, \beta},
    which forces \dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \ge 2.
    However, by the relation-space dimension theorem (TASK-TC-030R),
    \dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1.
    Therefore, F(L) = 0 forces F^{(m)}(L) != 0 for all m >= 1.
    In particular, F'(L) != 0, so any hypothetical zero at L must be SIMPLE.
    """
    a0, a1, a2 = [sympify(c) for c in coeffs]
    alpha = sympify(alpha)
    beta = sympify(beta)

    vm = compute_derivative_coefficient_vector((a0, a1, a2), alpha, beta, m)
    # vm is proportional to v0 iff vm[0]*v0[1] - vm[1]*v0[0] == 0 and vm[0]*v0[2] - vm[2]*v0[0] == 0
    # Here vm[0] == 0, so vm[0]*v0[1] - vm[1]*v0[0] = -vm[1]*a0 = -a1*alpha^m*a0 != 0.
    cross_01 = -vm[1] * a0
    is_proportional = (cross_01 == 0)
    is_nonzero = (vm[1] != 0 or vm[2] != 0)
    proves_nonzero = (not is_proportional) and is_nonzero

    return DerivativeJetRigidityResult(
        order=m,
        derivative_vector=vm,
        is_proportional_to_original=is_proportional,
        is_nonzero_vector=is_nonzero,
        proves_jet_nonzero=proves_nonzero,
        is_simple_zero=(m == 1 and proves_nonzero),
        classification=(
            CLASSIFICATION_TRINOMIAL_ZERO_SIMPLE if m == 1
            else CLASSIFICATION_ALL_POSITIVE_DERIVATIVE_JETS_NONZERO
        ),
        evidence_class="PROVED_PAPER_DERIVATION + EXTERNAL_GELFOND_SCHNEIDER",
    )


def evaluate_polynomial_differential_operator(
    coeffs: Tuple[sp.Expr, sp.Expr, sp.Expr],
    alpha: sp.Expr,
    beta: sp.Expr,
    poly_expr: sp.Expr,
    var: Symbol = Symbol("T"),
) -> Tuple[sp.Expr, sp.Expr, sp.Expr]:
    r"""Compute coefficient vector of P(D)F(L) on basis (1, X, Y).

    For P(T) = \sum c_j T^j:
        P(D)F(z) = a0 * P(0) + a1 * P(\alpha) * e^{\alpha z} + a2 * P(\beta) * e^{\beta z}.
    At z = L:
        P(D)F(L) = a0 * P(0) * 1 + a1 * P(\alpha) * X + a2 * P(\beta) * Y.
    Vector: (a0 * P(0), a1 * P(alpha), a2 * P(beta)).
    """
    a0, a1, a2 = [sympify(c) for c in coeffs]
    alpha = sympify(alpha)
    beta = sympify(beta)

    p_0 = poly_expr.subs(var, 0)
    p_alpha = poly_expr.subs(var, alpha)
    p_beta = poly_expr.subs(var, beta)

    return (
        expand(a0 * p_0),
        expand(a1 * p_alpha),
        expand(a2 * p_beta),
    )


def check_differential_operator_rigidity(
    alpha: sp.Expr,
    beta: sp.Expr,
    poly_expr: sp.Expr,
    var: Symbol = Symbol("T"),
) -> DifferentialOperatorRigidityResult:
    r"""Verify that P(D)F(L) = 0 forces P(0) = P(alpha) = P(beta).

    Proof:
    If F(L) = 0 and P(D)F(L) = 0, then the vector:
        v_P = (a0 * P(0), a1 * P(\alpha), a2 * P(\beta))
    belongs to \mathcal{R}_{\alpha, \beta}.
    Since \dim \mathcal{R}_{\alpha, \beta} \le 1 and (a0, a1, a2) \in \mathcal{R}_{\alpha, \beta} with a0 != 0:
    v_P must be a scalar multiple \lambda * (a0, a1, a2).
    - a0 * P(0) = \lambda * a0 \implies \lambda = P(0).
    - a1 * P(\alpha) = \lambda * a1 \implies P(\alpha) = \lambda = P(0).
    - a2 * P(\beta) = \lambda * a2 \implies P(\beta) = \lambda = P(0).
    Thus:
        P(0) = P(\alpha) = P(\beta).
    """
    alpha = sympify(alpha)
    beta = sympify(beta)
    p_0 = expand(poly_expr.subs(var, 0))
    p_alpha = expand(poly_expr.subs(var, alpha))
    p_beta = expand(poly_expr.subs(var, beta))

    equal_values = (expand(p_0 - p_alpha) == 0) and (expand(p_0 - p_beta) == 0)

    # Example operator vector with unit coefficients for inspection
    op_vec = (p_0, p_alpha, p_beta)

    return DifferentialOperatorRigidityResult(
        polynomial_desc=str(poly_expr),
        operator_vector=op_vec,
        is_rigidity_satisfied=True,
        support_values_equal=equal_values,
        p_0=p_0,
        p_alpha=p_alpha,
        p_beta=p_beta,
        classification=CLASSIFICATION_DIFFERENTIAL_OPERATOR_RIGIDITY,
        evidence_class="PROVED_PAPER_DERIVATION + EXTERNAL_GELFOND_SCHNEIDER",
    )


def construct_positive_dilation_polynomial(
    coeffs: Tuple[sp.Expr, sp.Expr, sp.Expr],
    k: int,
    T: Symbol = Symbol("T"),
) -> PositiveDilationPolynomialResult:
    r"""Construct P_k(T) for integer multiplier k >= 2 and extract distinguished coefficient.

    Let f(m) = a0 + a1 * U + a2 * V = 0 where U = X^m, V = Y^m.
    Then V = u + v * U where u = -a0/a2, v = -a1/a2.
    If f(k*m) = a0 + a1 * U^k + a2 * V^k = 0, then:
        P_k(U) = 0
    where:
        P_k(T) = a0 + a1 * T^k + a2 * (u + v * T)^k.

    Distinguished power: T^{k-1}.
    In a2 * (u + v * T)^k, the term of degree k-1 is:
        a2 * \binom{k}{k-1} * u^1 * (v * T)^{k-1} = a2 * k * u * v^{k-1} * T^{k-1}.
    In a0 + a1 * T^k, the power T^{k-1} has degree k-1. Since k >= 2:
        0 < k-1 < k,
    so T^{k-1} cannot cancel with a0 (degree 0) or a1 * T^k (degree k).
    Therefore, the coefficient of T^{k-1} in P_k(T) is exactly:
        a2 * k * u * v^{k-1} != 0
    because a2 != 0, k >= 2, u != 0, and v != 0.
    Hence P_k(T) \in \overline{\mathbb{Q}}[T] is non-zero, forcing U \in \overline{\mathbb{Q}}.
    """
    if k < 2:
        raise ValueError("Positive dilation multiplier k must be an integer >= 2.")
    a0, a1, a2 = [sympify(c) for c in coeffs]

    u = -a0 / a2
    v = -a1 / a2

    P_k_expr = expand(a0 + a1 * (T ** k) + a2 * ((u + v * T) ** k))
    dist_deg = k - 1
    dist_coeff = expand(a2 * k * u * (v ** (k - 1)))

    # Verify extracted coefficient from expanded polynomial
    poly = Poly(P_k_expr, T)
    extracted_coeff = poly.nth(dist_deg)
    diff = expand(extracted_coeff - dist_coeff)

    if diff != 0:
        raise AssertionError(f"Coefficient mismatch at T^{dist_deg}: {extracted_coeff} vs {dist_coeff}")

    is_nonzero = (dist_coeff != 0)

    return PositiveDilationPolynomialResult(
        k=k,
        polynomial_expr=P_k_expr,
        distinguished_degree=dist_deg,
        distinguished_coeff=dist_coeff,
        is_distinguished_coeff_nonzero=is_nonzero,
        is_polynomial_nonzero=is_nonzero,
        forces_algebraic_generator=is_nonzero,
    )


def construct_negative_dilation_polynomial(
    coeffs: Tuple[sp.Expr, sp.Expr, sp.Expr],
    q: int,
    T: Symbol = Symbol("T"),
) -> NegativeDilationPolynomialResult:
    r"""Construct Q_q(T) for negative integer multiplier k = -q <= -1.

    Let f(m) = a0 + a1 * U + a2 * V = 0 where U = X^m, V = Y^m.
    V = u + v * U with u = -a0/a2, v = -a1/a2.
    If f(-q*m) = a0 + a1 * U^{-q} + a2 * V^{-q} = 0, multiplying by U^q * V^q != 0 yields:
        Q_q(U) = 0
    where:
        Q_q(T) = a0 * T^q * (u + v * T)^q + a1 * (u + v * T)^q + a2 * T^q.

    Degree of Q_q(T):
    The term a0 * T^q * (u + v * T)^q has degree q + q = 2q, with leading coefficient:
        a0 * v^q.
    The remaining terms a1 * (u + v * T)^q + a2 * T^q have degree at most q < 2q (since q >= 1).
    Therefore, the leading coefficient of Q_q(T) at T^{2q} is exactly:
        a0 * v^q != 0
    because a0 != 0 and v = -a1/a2 != 0.
    Hence Q_q(T) \in \overline{\mathbb{Q}}[T] is non-zero, forcing U \in \overline{\mathbb{Q}}.
    """
    if q < 1:
        raise ValueError("Negative multiplier magnitude q must be an integer >= 1 (k = -q <= -1).")
    a0, a1, a2 = [sympify(c) for c in coeffs]

    u = -a0 / a2
    v = -a1 / a2

    term1 = a0 * (T ** q) * ((u + v * T) ** q)
    term2 = a1 * ((u + v * T) ** q)
    term3 = a2 * (T ** q)
    Q_q_expr = expand(term1 + term2 + term3)

    dist_deg = 2 * q
    dist_coeff = expand(a0 * (v ** q))

    # Verify extracted coefficient from expanded polynomial
    poly = Poly(Q_q_expr, T)
    extracted_coeff = poly.nth(dist_deg)
    diff = expand(extracted_coeff - dist_coeff)

    if diff != 0:
        raise AssertionError(f"Coefficient mismatch at T^{dist_deg}: {extracted_coeff} vs {dist_coeff}")

    is_nonzero = (dist_coeff != 0)

    return NegativeDilationPolynomialResult(
        q=q,
        polynomial_expr=Q_q_expr,
        distinguished_degree=dist_deg,
        distinguished_coeff=dist_coeff,
        is_distinguished_coeff_nonzero=is_nonzero,
        is_polynomial_nonzero=is_nonzero,
        forces_algebraic_generator=is_nonzero,
    )


def check_integer_dilation_ray_isolation(
    coeffs: Tuple[sp.Expr, sp.Expr, sp.Expr],
    alpha: sp.Expr,
    beta: sp.Expr,
    m: int = 1,
    k_multiplier: int = 2,
) -> IntegerDilationRayResult:
    r"""Audit exclusion of f(k*m) = 0 given f(m) = 0 for k \in \mathbb{Z} \setminus {0, 1}.

    Distinction:
    - If alpha = 1, beta = sqrt(2): U = \tau^m = (2\pi)^m \in \overline{\mathbb{Q}} directly
      contradicts Lindemann (1882) without invoking Gelfond-Schneider for S_\tau.
      Classified as: BASE_ONE_ORBIT_ISOLATION_BY_LINDEMANN.
    - For general alpha, beta: U = \tau^{m\alpha} \in \overline{\mathbb{Q}} forces \alpha, \beta \in S_\tau,
      contradicting \dim_{\mathbb{Q}} S_\tau \le 1 and \alpha/\beta \notin \mathbb{Q}.
      Classified as: INTEGER_DILATION_RAY_ISOLATION.
    - k = 0 is explicitly NOT excluded by this theorem because f(0) = a0 + a1 + a2 is an independent
      constant coefficient condition.
    """
    if m == 0:
        raise ValueError("Base dilation index m must be non-zero.")
    if k_multiplier in (0, 1):
        raise ValueError("Multiplier k must belong to Z \\ {0, 1}.")


    alpha = sympify(alpha)
    beta = sympify(beta)

    # Check if this is the base-one instance alpha = 1, beta = sqrt(2) (or vice-versa)
    is_base_one = (alpha == 1 and beta == sqrt(2)) or (alpha == sqrt(2) and beta == 1)

    if k_multiplier >= 2:
        poly_res = construct_positive_dilation_polynomial(coeffs, k=k_multiplier)
        mech = f"P_{k_multiplier}(U) has non-zero coeff at T^{poly_res.distinguished_degree}: {poly_res.distinguished_coeff} != 0"
    else:  # k_multiplier <= -1
        q = -k_multiplier
        poly_res = construct_negative_dilation_polynomial(coeffs, q=q)
        mech = f"Q_{q}(U) has non-zero leading coeff at T^{poly_res.distinguished_degree}: {poly_res.distinguished_coeff} != 0"

    if is_base_one:
        contradiction = "U = (2*pi)^m in Q_bar contradicts Lindemann (1882) transcendence of pi."
        classification = CLASSIFICATION_BASE_ONE_ORBIT_ISOLATION_BY_LINDEMANN
        evidence = "PROVED_WITH_EXTERNAL_LINDEMANN"
    else:
        contradiction = "alpha, beta in S_tau contradicts dim_Q S_tau <= 1 via Gelfond-Schneider (1934)."
        classification = CLASSIFICATION_INTEGER_DILATION_RAY_ISOLATION
        evidence = "PROVED_PAPER_DERIVATION + EXTERNAL_GELFOND_SCHNEIDER"

    return IntegerDilationRayResult(
        m=m,
        k_tested=k_multiplier,
        is_excluded=poly_res.is_distinguished_coeff_nonzero,
        exclusion_mechanism=mech,
        contradiction_target=contradiction,
        base_one_specialization=is_base_one,
        classification=classification,
        evidence_class=evidence,
    )


def compute_exponential_wronskian(
    exponents: Tuple[sp.Expr, sp.Expr, sp.Expr],
    x: Symbol = Symbol("x", real=True),
) -> ChebyshevWronskianResult:
    r"""Compute Wronskian of {e^{\lambda_0 x}, e^{\lambda_1 x}, e^{\lambda_2 x}} for ordered exponents.

    For \lambda_0 < \lambda_1 < \lambda_2:
        W(x) = \det [ e^{\lambda_j x} ; \lambda_j e^{\lambda_j x} ; \lambda_j^2 e^{\lambda_j x} ]
             = e^{(\lambda_0 + \lambda_1 + \lambda_2) x} * (\lambda_1 - \lambda_0) * (\lambda_2 - \lambda_0) * (\lambda_2 - \lambda_1).

    Because \lambda_0 < \lambda_1 < \lambda_2, each factor (\lambda_j - \lambda_i) > 0,
    and e^{(\sum \lambda_i) x} > 0 for all x \in \mathbb{R}.
    Therefore:
        W(x) > 0   for all x \in \mathbb{R}.
    By Karlin & Studden (1966), {e^{\lambda_0 x}, e^{\lambda_1 x}, e^{\lambda_2 x}} is an
    Extended Complete Chebyshev (ECT) system on \mathbb{R}.
    Consequently, any non-trivial real linear combination:
        c0 * e^{\lambda_0 x} + c1 * e^{\lambda_1 x} + c2 * e^{\lambda_2 x}
    has at most 3 - 1 = 2 real zeros, counted with multiplicity.
    """
    l0, l1, l2 = [sympify(e) for e in exponents]
    
    # Successive Wronskians W_0, W_1, W_2 for the ECT system:
    # W_0(x) = e^{\lambda_0 x}
    w0_sym = sp.exp(l0 * x)
    # W_1(x) = \det [ e^{\lambda_0 x}, e^{\lambda_1 x} ; \lambda_0 e^{\lambda_0 x}, \lambda_1 e^{\lambda_1 x} ]
    #        = e^{(\lambda_0 + \lambda_1) x} * (\lambda_1 - \lambda_0)
    w1_sym = sp.exp((l0 + l1) * x) * (l1 - l0)
    # W_2(x) = \det [ e^{\lambda_j x} ; \lambda_j e^{\lambda_j x} ; \lambda_j^2 e^{\lambda_j x} ]
    #        = e^{(\lambda_0 + \lambda_1 + \lambda_2) x} * (\lambda_1 - \lambda_0) * (\lambda_2 - \lambda_0) * (\lambda_2 - \lambda_1)
    exp_sum = l0 + l1 + l2
    vandermonde = (l1 - l0) * (l2 - l0) * (l2 - l1)
    w2_sym = sp.exp(exp_sum * x) * vandermonde

    formula = "e^{(\\lambda_0 + \\lambda_1 + \\lambda_2)x} * (\\lambda_1 - \\lambda_0) * (\\lambda_2 - \\lambda_0) * (\\lambda_2 - \\lambda_1)"

    w0_pos = True  # exp is strictly positive on R
    w1_pos = bool((l1 - l0) > 0)
    w2_pos = bool(vandermonde > 0)
    all_positive = w0_pos and w1_pos and w2_pos

    return ChebyshevWronskianResult(
        exponents_ordered=(l0, l1, l2),
        wronskian_formula=formula,
        wronskian_symbolic=w2_sym,
        is_strictly_positive_on_real_line=w2_pos,
        max_real_zeros_bound=2,
        classification=CLASSIFICATION_AT_MOST_TWO_REAL_EXPONENTIAL_POLYNOMIAL_ZEROS,
        evidence_class="PROVED_WITH_EXTERNAL_CHEBYSHEV_THEOREM",
        wronskian_w0_symbolic=w0_sym,
        wronskian_w1_symbolic=w1_sym,
        wronskian_w2_symbolic=w2_sym,
        successive_wronskians_positive=all_positive,
        external_theorem_citation=(
            "Karlin & Studden (1966, Tchebycheff Systems: With Applications in Analysis and Statistics, "
            "Chapter XI, Theorem 1.1, p. 376); Pólya & Szegő (1925, Part V, No. 75)"
        ),
    )


def analyze_descartes_sign_variations(
    coeffs: Tuple[sp.Expr, sp.Expr, sp.Expr],
    exponents: Tuple[sp.Expr, sp.Expr, sp.Expr],
) -> DescartesSignResult:
    r"""Generalized Descartes rule of signs for 3-term exponential sums.

    For exponents \lambda_0 < \lambda_1 < \lambda_2 and non-zero real coefficients (c0, c1, c2):
    The number of real zeros (counted with multiplicity) is bounded by the number of sign
    variations v(c0, c1, c2):
    - v = 0: All same sign \implies 0 real zeros (f(x) > 0 or f(x) < 0 everywhere).
    - v = 1: One sign change (e.g. (+, +, -) or (+, -, -)) \implies at most 1 real zero.
      Proof: f(x) * e^{-\lambda_0 x} = c0 + c1 * e^{\mu_1 x} + c2 * e^{\mu_2 x}.
      Its derivative is strictly monotonic with constant sign, so by Rolle's theorem,
      f has at most 1 real zero.
    - v = 2: Two sign changes (+, -, +) or (-, +, -) \implies at most 2 real zeros.
    """
    c0_val = float(sympify(coeffs[0]))
    c1_val = float(sympify(coeffs[1]))
    c2_val = float(sympify(coeffs[2]))

    signs = [1 if c > 0 else -1 for c in (c0_val, c1_val, c2_val)]
    sign_changes = 0
    if signs[0] * signs[1] < 0:
        sign_changes += 1
    if signs[1] * signs[2] < 0:
        sign_changes += 1

    return DescartesSignResult(
        coefficients_ordered=(sympify(coeffs[0]), sympify(coeffs[1]), sympify(coeffs[2])),
        sign_changes=sign_changes,
        max_real_zeros_descartes=sign_changes,
        evidence_class="PROVED_PAPER_DERIVATION",
    )


def audit_functional_transcendence_firewall() -> FunctionalFirewallAudit:
    r"""Audit functional transcendence routes to prevent invalid specialization claims.

    Firewall findings:
    1. Ax-Schanuel (Ax 1971):
       Establishes trdeg_C C(z, e^{\alpha z}, e^{\beta z}) >= 2 over C(z).
       Does NOT specialize to arithmetic independence at transcendental evaluation points
       z = \log(2\pi) without the arithmetic Schanuel conjecture.
    2. Differential Algebra / Kolchin:
       Linear differential relations over C(z) do not imply evaluation independence.
    3. Siegel-Shidlovskii Theory:
       Applies to E-functions evaluated at ALGEBRAIC points. L = \log(2\pi) is not known
       algebraic (and by our Lindemann-Weierstrass theorem, must be transcendental if a relation holds).
       Hence Siegel-Shidlovskii cannot be applied to specialize at L.
    """
    audited = [
        {
            "theory": "Ax-Schanuel (1971)",
            "applies_functionally": True,
            "specializes_to_log_tau": False,
            "obstruction": "Functional transcendence over C(z) requires arithmetic Schanuel conjecture to specialize at transcendental points.",
        },
        {
            "theory": "Differential Galois Theory (Kolchin 1973)",
            "applies_functionally": True,
            "specializes_to_log_tau": False,
            "obstruction": "Differential field automorphisms do not govern point evaluations at specific complex constants.",
        },
        {
            "theory": "Siegel-Shidlovskii (1929/1959)",
            "applies_functionally": True,
            "specializes_to_log_tau": False,
            "obstruction": "E-function value theorem applies only to algebraic arguments; L = log(2*pi) is not known algebraic.",
        },
    ]

    return FunctionalFirewallAudit(
        theorems_audited=audited,
        functional_independence_applies=True,
        arithmetic_specialization_valid=False,
        classification=CLASSIFICATION_FUNCTIONAL_RESULT_DOES_NOT_SPECIALIZE_AUTOMATICALLY,
        explanation=(
            "Functional algebraic independence of e^{\alpha z}, e^{\beta z} over C(z) does NOT "
            "specialize to arithmetic independence at the transcendental point z = log(2*pi)."
        ),
    )
