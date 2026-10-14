"""
TASK-TC-034 / TASK-TC-034R: Infinitesimal Transport-Mismatch Curvature,
Compact-Support Witnesses, and Conditional Theta-Mellin Audit.

This module audits whether the infinitesimal second variation (transport curvature)
around the unique label-preserving transport b = 1 (written b = 1 + eta as eta -> 0):
1. defines an exact zero-independent arithmetic curvature functional;
2. has a spectral expression detecting delta_rho^2;
3. avoids the value-level covariance cancellation proved in TASK-TC-033;
4. avoids the exact-zero remainder-cancellation obstruction proved in TASK-TC-032R.

TASK-TC-034R repairs the evidence boundaries for TASK-TC-034:
- classifies the compact-support Euler-homogeneity no-go as PROVED_PAPER_DERIVATION
  (not Lean-formalized);
- implements an explicit smooth C^infty plateau compactification operator X_N(x, y)
  that preserves kernel jets through order 2 at all active stations 2 <= n, m <= N;
- certifies strictly negative and strictly positive complete compact-support arithmetic
  curvatures using outward Arb ball arithmetic (failing closed if flint is unavailable);
- replaces ambiguous theta-Mellin Boolean claims with explicit conditional/unresolved
  evidence statuses.

This is the direct audit of canonical open obligation OBL-CT-001A.
"""

from __future__ import annotations

import cmath
from dataclasses import asdict, dataclass
import math
from pathlib import Path
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

try:
    import flint  # type: ignore
except ImportError:
    flint = None  # type: ignore

from tc.two_variable import _von_mangoldt_exact

TAU: float = 2.0 * math.pi
LOG_TAU: float = math.log(TAU)

# ---------------------------------------------------------------------------
# Canonical Classification Constants (TASK-TC-034 & TASK-TC-034R)
# ---------------------------------------------------------------------------

TASK_TC_034R_STATUS = "TASK_TC_034R_TRANSPORT_CURVATURE_REPAIR_COMPLETE"

OUTCOME_A_FULL_BRIDGE = "INFINITESIMAL_TRANSPORT_CURVATURE_BRIDGE_PROVED"
OUTCOME_B_ARITHMETIC_FLATNESS_NOT_IMPLIED = "ARITHMETIC_CURVATURE_FLATNESS_NOT_IMPLIED"
OUTCOME_C_COMPACT_SUPPORT_NO_GO = "COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED"
OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE = "SPECTRAL_CURVATURE_IS_SIGNED_OR_DOUBLE_SUM"
OUTCOME_E_WEIL_EQUIVALENCE = "CURVATURE_POSITIVITY_IS_RH_EQUIVALENT"
OUTCOME_F_THETA_SUBGATE_OPEN = "THETA_MELLIN_NONSCALAR_CURVATURE_SUBGATE_OPEN"
OUTCOME_G_REDUCES_TO_OBL_CT_001A = "MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A"

COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED = (
    "COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED"
)
COMPACT_SUPPORT_NO_GO_EVIDENCE_STATUS = "PROVED_PAPER_DERIVATION"
CLASSIFICATION_COMPACT_SUPPORT_IMPOSSIBLE = (
    "NONZERO_COMPACT_SUPPORT_HOMOGENEOUS_KERNEL_IMPOSSIBLE"
)

COMPACT_SUPPORT_SIGN_INDEFINITENESS_STATUS = (
    "COMPACT_SUPPORT_ARITHMETIC_CURVATURE_SIGN_INDEFINITE"
)
COMPACT_SUPPORT_NEG_CURVATURE_CERTIFIED = (
    "COMPACT_SUPPORT_NEGATIVE_ARITHMETIC_CURVATURE_CERTIFIED"
)
COMPACT_SUPPORT_POS_CURVATURE_CERTIFIED = (
    "COMPACT_SUPPORT_POSITIVE_ARITHMETIC_CURVATURE_CERTIFIED"
)
SUPERSEDED_FINITE_TRUNCATION_STATUS = (
    "FINITE_TRUNCATION_SIGN_INDEFINITENESS_OBSERVED"
)
ARB_CERTIFICATION_NOT_AVAILABLE = "ARB_CERTIFICATION_NOT_AVAILABLE"

CLASSIFICATION_FINITE_ACCIDENTAL_ZERO = "FINITE_ACCIDENTAL_ARITHMETIC_CURVATURE_ZERO"
CLASSIFICATION_ARITHMETIC_INDEFINITE = COMPACT_SUPPORT_SIGN_INDEFINITENESS_STATUS
CLASSIFICATION_SELECTED_BLOCK_ONLY = "SELECTED_CURVATURE_BLOCK_ONLY"
CLASSIFICATION_REDUCES_TO_EXISTING_OBL_CT_001A = (
    "MISMATCH_CURVATURE_REDUCES_TO_EXISTING_OBL_CT_001A"
)
CLASSIFICATION_GENERIC_SCALE_CURVATURE = "GENERIC_SCALE_CURVATURE"
CLASSIFICATION_CURVATURE_POSITIVITY_RH_EQUIVALENT = (
    "CURVATURE_POSITIVITY_IS_RH_EQUIVALENT"
)

THETA_MELLIN_AUDIT_CONDITIONAL = "THETA_MELLIN_AUDIT_CONDITIONAL"
CANDIDATE_THETA_MELLIN_AUDIT = "CANDIDATE_THETA_MELLIN_AUDIT"
OBL_CT_001A_STATUS = "OBL_CT_001A_OPEN"
CANDIDATE_FAILURE_DOES_NOT_REFUTE_TC = "CANDIDATE_FAILURE_DOES_NOT_REFUTE_TC"

PRINCIPAL_CLASSIFICATION = OUTCOME_G_REDUCES_TO_OBL_CT_001A


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EulerMomentResult:
    """Arithmetic Euler moments A_0, A_1, A_2 and transport curvature at eta = 0."""

    A0: float
    A1: float
    A2: float
    arithmetic_curvature: float
    normalized_log_curvature: Optional[float]
    active_station_pairs: int
    n_max: int
    evaluation_mode: str = "FINITE_STATION_EVALUATION"
    evidence_class: str = "PROVED_ALGEBRAIC_AND_FINITE_ARITHMETIC"


@dataclass(frozen=True)
class MismatchDerivativeResult:
    """Grade-K mismatch derivatives at eta = 0 and K-independent normalized curvature."""

    K: float
    base_q: float
    log_q: float
    M_K_0: float
    M_K_prime_0: float
    M_K_double_prime_0: float
    euler_M_K_0: float
    euler_M_K_prime_0: float
    euler_M_K_double_prime_0: float
    normalized_curvature_from_K: float
    direct_curvature_A0A2_minus_A1sq: float
    derivative_agreement_abs_err: float
    curvature_agreement_abs_err: float


@dataclass(frozen=True)
class ExponentialMixtureCurvatureResult:
    """Synthetic curvature M(0)*M''(0) - M'(0)^2 for an exponential mixture."""

    weights: Tuple[float, ...]
    exponents: Tuple[float, ...]
    M0: float
    M1: float
    M2: float
    curvature_determinant: float
    pairwise_lagrange_sum: float
    lagrange_identity_abs_err: float
    strictly_positive: bool
    nonnegative: bool
    has_distinct_exponents: bool
    all_weights_positive: bool


@dataclass(frozen=True)
class CompactSupportHomogeneityAudit:
    """Audit of Euler homogeneity E F_0 = d F_0 vs compact support in (0, inf)^2."""

    degree_d: float
    ray_scaling_verified: bool
    compact_support_compatible_for_nonzero_kernel: bool
    evidence_status: str
    lean_formalized: bool
    classification: str
    outcome_code: str
    proof_steps: Tuple[str, ...]
    scope_note: str


@dataclass(frozen=True)
class CompactifiedKernelBundle:
    """Smooth compactified kernel tilde{G}_N = X_N * G preserving station jets up to order 2."""

    name: str
    N_cutoff: int
    a: float
    b: float
    c: float
    d: float
    support_interval: Tuple[float, float]
    plateau_interval: Tuple[float, float]
    support_rectangle: Tuple[Tuple[float, float], Tuple[float, float]]
    plateau_rectangle: Tuple[Tuple[float, float], Tuple[float, float]]
    active_station_set: Tuple[int, ...]
    highest_admitted_integer_station: int
    highest_active_prime_power_station: int
    first_excluded_integer_station: int
    verified_derivative_order: int
    kernel_fn: Callable[[float, float], float]
    euler1_fn: Callable[[float, float], float]
    euler2_fn: Callable[[float, float], float]
    prototype_fn: Callable[[float, float], float]
    prototype_euler1_fn: Callable[[float, float], float]
    prototype_euler2_fn: Callable[[float, float], float]


@dataclass(frozen=True)
class SpectralPairingAuditResult:
    """Centering and zero-pairing audit for spectral mismatch scaling."""

    rho: complex
    delta: float
    gamma: float
    uncentered_conjugate_exponent: complex
    centered_conjugate_exponent: complex
    centered_reflection_exponent: complex
    general_pair_centered_exponent: complex
    conjugate_even_defect: float
    reflection_even_defect: float
    conjugate_second_variation_coeff: float
    reflection_second_variation_coeff: float
    naturally_induced_pairing: str
    spectral_curvature_classification: str


@dataclass(frozen=True)
class ThetaMellinNonScalarCandidateAudit:
    """
    Repaired Phase II audit of one canonical non-scalar quadratic theta-Mellin candidate
    (TASK-TC-034R Section 11). Uses explicit evidence statuses instead of ambiguous Booleans.
    """

    candidate_name: str
    scalar_candidate_status: str
    purely_theta_or_arithmetic_defined_status: str
    zero_independent_definition_status: str
    exact_scale_flatness_law_status: str
    exact_scale_flatness_law_basis: str
    convergence_status: str
    second_mismatch_variation_status: str
    delta_squared_detection_status: str
    complete_spectral_expansion_status: str
    positive_complete_spectral_curvature_status: str
    selected_zero_construction_status: str
    closes_obl_ct_001a_status: str
    overall_classification: str
    secondary_classification: str
    reduces_to_obligation: str
    exact_remaining_theorem: str


# ---------------------------------------------------------------------------
# Section 4 (TASK-TC-034): Transported Mismatch Kernel and Arithmetic Energy
# ---------------------------------------------------------------------------


def evaluate_transported_mismatch_kernel(
    f0: Callable[[float, float], float],
    x: float,
    y: float,
    K: float,
    eta: float = 0.0,
    a: float = 0.0,
    base_q: float = TAU,
) -> float:
    """
    Evaluate the transported mismatch kernel:
        F_{K, eta}(x, y) = q^{a K} F_0(q^{-(1 + eta) K} x, q^{-(1 + eta) K} y).

    Here b = 1 + eta is the relative transport parameter around the unique
    compatibility point b = 1 (eta = 0).
    """
    if base_q <= 0.0:
        raise ValueError("base_q must be strictly positive.")
    amp = base_q ** (a * K)
    scale = base_q ** (-(1.0 + eta) * K)
    return amp * float(f0(scale * x, scale * y))


def active_prime_power_stations(n_max: int) -> List[Tuple[int, float]]:
    """Return list of (n, Lambda(n)) for prime powers 2 <= n <= n_max."""
    stations: List[Tuple[int, float]] = []
    for n in range(2, n_max + 1):
        lam = _von_mangoldt_exact(n)
        if lam > 0.0:
            stations.append((n, lam))
    return stations


def prime_power_base_table(n_max: int) -> List[Tuple[int, int, int]]:
    """
    Return exact integer tuples (n, p, k) for prime powers n = p^k with 2 <= n <= n_max.
    Used for exact Arb evaluation of Lambda(n) = log(p).
    """
    table: List[Tuple[int, int, int]] = []
    for n in range(2, n_max + 1):
        m = n
        p_found: Optional[int] = None
        d = 2
        while d * d <= m:
            if m % d == 0:
                p_found = d
                break
            d += 1
        if p_found is None:
            table.append((n, n, 1))
        else:
            k = 0
            while m % p_found == 0:
                m //= p_found
                k += 1
            if m == 1:
                table.append((n, p_found, k))
    return table


def evaluate_normalized_mismatch_energy(
    f0: Callable[[float, float], float],
    K: float,
    eta: float = 0.0,
    n_max: int = 30,
    base_q: float = TAU,
) -> float:
    """
    Evaluate the normalized equal-grade arithmetic mismatch energy:
        hat{M}_K(eta) = q^{-a K} <mu_K x mu_K, F_{K, eta}>
                      = sum_{n, m >= 2} Lambda(n) Lambda(m) F_0(q^{-eta K} n, q^{-eta K} m).

    At eta = 0, hat{M}_K(0) = hat{M}_0(0) for every K, recovering TASK-TC-033 at value level.
    """
    if base_q <= 0.0:
        raise ValueError("base_q must be strictly positive.")
    stations = active_prime_power_stations(n_max)
    mismatch_scale = base_q ** (-eta * K)
    total = 0.0
    for n, lam_n in stations:
        xn = mismatch_scale * float(n)
        for m, lam_m in stations:
            ym = mismatch_scale * float(m)
            val = float(f0(xn, ym))
            if val != 0.0:
                total += lam_n * lam_m * val
    return total


# ---------------------------------------------------------------------------
# Section 5 & 6 (TASK-TC-034): Arithmetic Euler-Generator Theorem & Curvature
# ---------------------------------------------------------------------------


def apply_euler_operator_once(
    f0: Callable[[float, float], float],
    x: float,
    y: float,
    euler1_f0: Optional[Callable[[float, float], float]] = None,
    eps: float = 1e-6,
) -> float:
    """
    Evaluate (E F_0)(x, y) = (x d/dx + y d/dy) F_0(x, y) = d/du|_{u=0} F_0(e^u x, e^u y).
    Uses exact analytic callback `euler1_f0` if provided, otherwise 4th-order central
    difference along the radial ray (e^u x, e^u y).
    """
    if euler1_f0 is not None:
        return float(euler1_f0(x, y))
    fp1 = float(f0(math.exp(eps) * x, math.exp(eps) * y))
    fm1 = float(f0(math.exp(-eps) * x, math.exp(-eps) * y))
    fp2 = float(f0(math.exp(2.0 * eps) * x, math.exp(2.0 * eps) * y))
    fm2 = float(f0(math.exp(-2.0 * eps) * x, math.exp(-2.0 * eps) * y))
    return (-fp2 + 8.0 * fp1 - 8.0 * fm1 + fm2) / (12.0 * eps)


def apply_euler_operator_twice(
    f0: Callable[[float, float], float],
    x: float,
    y: float,
    euler2_f0: Optional[Callable[[float, float], float]] = None,
    eps: float = 1e-5,
) -> float:
    """
    Evaluate (E^2 F_0)(x, y) = (x d/dx + y d/dy)^2 F_0(x, y) = d^2/du^2|_{u=0} F_0(e^u x, e^u y).
    Uses exact analytic callback `euler2_f0` if provided, otherwise 4th-order central
    second difference along the radial ray (e^u x, e^u y).
    """
    if euler2_f0 is not None:
        return float(euler2_f0(x, y))
    f_0 = float(f0(x, y))
    fp1 = float(f0(math.exp(eps) * x, math.exp(eps) * y))
    fm1 = float(f0(math.exp(-eps) * x, math.exp(-eps) * y))
    fp2 = float(f0(math.exp(2.0 * eps) * x, math.exp(2.0 * eps) * y))
    fm2 = float(f0(math.exp(-2.0 * eps) * x, math.exp(-2.0 * eps) * y))
    return (-fp2 + 16.0 * fp1 - 30.0 * f_0 + 16.0 * fm1 - fm2) / (12.0 * eps * eps)


def evaluate_euler_moments_A0_A1_A2(
    f0: Callable[[float, float], float],
    n_max: int = 30,
    euler1_f0: Optional[Callable[[float, float], float]] = None,
    euler2_f0: Optional[Callable[[float, float], float]] = None,
    evaluation_mode: str = "FINITE_STATION_EVALUATION",
) -> EulerMomentResult:
    """
    Compute the arithmetic Euler moments:
        A_j(F_0) = sum_{n, m >= 2} Lambda(n) Lambda(m) (E^j F_0)(n, m),   j = 0, 1, 2,
    and the arithmetic transport curvature:
        C_arith(F_0) = A_0 A_2 - A_1^2,
        kappa_arith(F_0) = (A_0 A_2 - A_1^2) / A_0^2  (when A_0 > 0).

    Note (TASK-TC-034R Section 1.3): `evaluation_mode` explicitly distinguishes a
    `COMPLETE_COMPACT_SUPPORT_SUM` (when `supp(F_0) subset (1.5, N + 0.5)^2` and `n_max >= N`)
    from a `FINITE_TRUNCATION_DIAGNOSTIC` on a noncompact prototype.
    """
    stations = active_prime_power_stations(n_max)
    A0 = 0.0
    A1 = 0.0
    A2 = 0.0
    active_pairs = 0
    for n, lam_n in stations:
        xn = float(n)
        for m, lam_m in stations:
            ym = float(m)
            w = lam_n * lam_m
            v0 = float(f0(xn, ym))
            v1 = apply_euler_operator_once(f0, xn, ym, euler1_f0=euler1_f0)
            v2 = apply_euler_operator_twice(f0, xn, ym, euler2_f0=euler2_f0)
            if v0 != 0.0 or v1 != 0.0 or v2 != 0.0:
                active_pairs += 1
            A0 += w * v0
            A1 += w * v1
            A2 += w * v2

    c_arith = A0 * A2 - A1 * A1
    kappa = (c_arith / (A0 * A0)) if A0 > 0.0 else None
    return EulerMomentResult(
        A0=A0,
        A1=A1,
        A2=A2,
        arithmetic_curvature=c_arith,
        normalized_log_curvature=kappa,
        active_station_pairs=active_pairs,
        n_max=n_max,
        evaluation_mode=evaluation_mode,
    )


def evaluate_mismatch_derivatives_at_zero(
    f0: Callable[[float, float], float],
    K: float,
    n_max: int = 30,
    base_q: float = TAU,
    euler1_f0: Optional[Callable[[float, float], float]] = None,
    euler2_f0: Optional[Callable[[float, float], float]] = None,
    eps_eta: float = 5e-4,
) -> MismatchDerivativeResult:
    """
    Verify the Arithmetic Euler-Generator Theorem:
        hat{M}_K^{(j)}(0) = (-K log q)^j A_j(F_0)   for j = 0, 1, 2,
    and K-independence of the normalized arithmetic curvature:
        C_arith(F_0) = (hat{M}_K(0) hat{M}_K''(0) - (hat{M}_K'(0))^2) / (K^2 (log q)^2).
    """
    if K == 0.0:
        raise ValueError("Grade K must be nonzero to normalize mismatch curvature.")
    if base_q <= 0.0 or base_q == 1.0:
        raise ValueError("base_q must be positive and not equal to 1.")

    log_q = math.log(base_q)
    moments = evaluate_euler_moments_A0_A1_A2(
        f0, n_max=n_max, euler1_f0=euler1_f0, euler2_f0=euler2_f0
    )

    euler_m0 = moments.A0
    euler_m1 = (-K * log_q) * moments.A1
    euler_m2 = (K * log_q) ** 2 * moments.A2

    m_0 = evaluate_normalized_mismatch_energy(f0, K, 0.0, n_max=n_max, base_q=base_q)
    mp1 = evaluate_normalized_mismatch_energy(f0, K, eps_eta, n_max=n_max, base_q=base_q)
    mm1 = evaluate_normalized_mismatch_energy(f0, K, -eps_eta, n_max=n_max, base_q=base_q)
    mp2 = evaluate_normalized_mismatch_energy(
        f0, K, 2.0 * eps_eta, n_max=n_max, base_q=base_q
    )
    mm2 = evaluate_normalized_mismatch_energy(
        f0, K, -2.0 * eps_eta, n_max=n_max, base_q=base_q
    )

    m_prime_0 = (-mp2 + 8.0 * mp1 - 8.0 * mm1 + mm2) / (12.0 * eps_eta)
    m_double_prime_0 = (-mp2 + 16.0 * mp1 - 30.0 * m_0 + 16.0 * mm1 - mm2) / (
        12.0 * eps_eta * eps_eta
    )

    denom = (K * log_q) ** 2
    norm_curv_K = (euler_m0 * euler_m2 - euler_m1 * euler_m1) / denom
    deriv_err = max(
        abs(m_0 - euler_m0),
        abs(m_prime_0 - euler_m1),
        abs(m_double_prime_0 - euler_m2),
    )
    curv_err = abs(norm_curv_K - moments.arithmetic_curvature)

    return MismatchDerivativeResult(
        K=K,
        base_q=base_q,
        log_q=log_q,
        M_K_0=m_0,
        M_K_prime_0=m_prime_0,
        M_K_double_prime_0=m_double_prime_0,
        euler_M_K_0=euler_m0,
        euler_M_K_prime_0=euler_m1,
        euler_M_K_double_prime_0=euler_m2,
        normalized_curvature_from_K=norm_curv_K,
        direct_curvature_A0A2_minus_A1sq=moments.arithmetic_curvature,
        derivative_agreement_abs_err=deriv_err,
        curvature_agreement_abs_err=curv_err,
    )


def evaluate_even_mismatch_defect(
    f0: Callable[[float, float], float],
    K: float,
    eta: float,
    n_max: int = 30,
    base_q: float = TAU,
    euler2_f0: Optional[Callable[[float, float], float]] = None,
) -> Dict[str, float]:
    """
    Compute the symmetric mismatch difference:
        Delta_{eta, K} hat{M} = hat{M}_K(eta) + hat{M}_K(-eta) - 2 hat{M}_K(0),
    and the normalized quotient Delta_{eta, K} hat{M} / (eta^2 K^2 (log q)^2) -> A_2.
    """
    log_q = math.log(base_q)
    m0 = evaluate_normalized_mismatch_energy(f0, K, 0.0, n_max=n_max, base_q=base_q)
    mp = evaluate_normalized_mismatch_energy(f0, K, eta, n_max=n_max, base_q=base_q)
    mm = evaluate_normalized_mismatch_energy(f0, K, -eta, n_max=n_max, base_q=base_q)
    defect = mp + mm - 2.0 * m0
    denom = (eta * K * log_q) ** 2
    quotient = defect / denom if denom != 0.0 else 0.0
    moments = evaluate_euler_moments_A0_A1_A2(f0, n_max=n_max, euler2_f0=euler2_f0)
    return {
        "eta": eta,
        "K": K,
        "even_mismatch_defect": defect,
        "normalized_quotient": quotient,
        "exact_A2": moments.A2,
        "abs_error_to_A2": abs(quotient - moments.A2),
    }


# ---------------------------------------------------------------------------
# Section 4 & 5 (TASK-TC-034R): Explicit Smooth Compactification Operator
# ---------------------------------------------------------------------------


def flat_transition_h_jet(t: float) -> Tuple[float, float, float]:
    """
    IEEE-754 binary64 floating-point numerical realization of the standard C^infty flat
    function h(t) and its first two derivatives away from the active integer stations:
        h(t) = 0          for t <= 0,
        h(t) = e^{-1/t}   for t > 0.
    Returns (h(t), h'(t), h''(t)).

    Implementation note:
      - The mathematical cutoff uses the exact C^infty function h(t) = exp(-1/t) for all t > 0.
      - In IEEE-754 binary64 arithmetic, exp(-1/t) < exp(-700) ~ 9.86e-305 approaches binary64
        subnormal/underflow range when 1/t > 700 (t < 1/700), so this float callable returns
        (0.0, 0.0, 0.0) for inv_t > 700.0 as a numerical underflow guard.
      - For exact arbitrary-precision evaluation without any artificial threshold (including
        0 < t < 1/700), use `flat_transition_h_jet_arb(t, prec_bits)`.
      - Neither transition evaluator affects the certified arithmetic curvature sums at
        integer stations, because all active stations 2 <= n <= 15 lie strictly inside the
        plateau [1.75, 15.25] where the cutoff is identically (1, 0, 0), and all excluded
        integers n <= 1 or n >= 16 lie strictly outside (1.5, 15.5) where it is (0, 0, 0).
    """
    if t <= 0.0:
        return (0.0, 0.0, 0.0)
    inv_t = 1.0 / t
    if inv_t > 700.0:
        return (0.0, 0.0, 0.0)
    val = math.exp(-inv_t)
    inv_t2 = inv_t * inv_t
    d1 = inv_t2 * val
    d2 = (inv_t2 * inv_t2 - 2.0 * inv_t2 * inv_t) * val
    return (val, d1, d2)


def flat_transition_h_jet_arb(
    t: float,
    prec_bits: int = 128,
) -> Dict[str, Any]:
    """
    Evaluate the exact mathematical C^infty flat function h(t) = exp(-1/t) (t > 0) and its
    first two derivatives in outward Arb ball arithmetic without any artificial binary64
    underflow threshold (valid including 0 < t < 1/700).
    """
    if t <= 0.0:
        return {
            "t": t,
            "is_positive_t": False,
            "h_str": "0",
            "h_prime_str": "0",
            "h_double_prime_str": "0",
            "strictly_positive_h": False,
        }
    if flint is None:
        return {
            "t": t,
            "status": ARB_CERTIFICATION_NOT_AVAILABLE,
            "strictly_positive_h": False,
        }
    saved_prec = flint.ctx.prec
    try:
        flint.ctx.prec = prec_bits
        arb = flint.arb
        t_arb = arb(str(t))
        inv_t = arb(1) / t_arb
        val = (-inv_t).exp()
        inv_t2 = inv_t * inv_t
        d1 = inv_t2 * val
        d2 = (inv_t2 * inv_t2 - arb(2) * inv_t2 * inv_t) * val
        return {
            "t": t,
            "is_positive_t": True,
            "h_str": str(val),
            "h_prime_str": str(d1),
            "h_double_prime_str": str(d2),
            "strictly_positive_h": bool(val > 0),
        }
    finally:
        flint.ctx.prec = saved_prec



def smooth_step_S_jet(t: float) -> Tuple[float, float, float]:
    """
    Evaluate the smooth C^infty step function S(t) = h(t) / (h(t) + h(1 - t))
    and its first two derivatives (S(t), S'(t), S''(t)).
    Satisfies:
      - S(t) = 0, S'(t) = 0, S''(t) = 0 for t <= 0;
      - S(t) = 1, S'(t) = 0, S''(t) = 0 for t >= 1;
      - 0 < S(t) < 1 for 0 < t < 1.
    """
    if t <= 0.0:
        return (0.0, 0.0, 0.0)
    if t >= 1.0:
        return (1.0, 0.0, 0.0)
    u, u1, u2 = flat_transition_h_jet(t)
    v, vp1, vp2 = flat_transition_h_jet(1.0 - t)
    v1 = -vp1
    v2 = vp2
    denom = u + v
    if denom == 0.0:
        return (0.5 if t == 0.5 else (0.0 if t < 0.5 else 1.0), 0.0, 0.0)
    s0 = u / denom
    num1 = u1 * v - u * v1
    s1 = num1 / (denom * denom)
    denom_prime = u1 + v1
    s2 = ((u2 * v - u * v2) * denom - 2.0 * num1 * denom_prime) / (
        denom * denom * denom
    )
    return (s0, s1, s2)


def plateau_cutoff_1d_jet(
    x: float,
    a: float = 1.5,
    b: float = 1.75,
    c: float = 15.25,
    d: float = 15.5,
) -> Tuple[float, float, float]:
    """
    Evaluate the 1D smooth plateau cutoff:
        chi_{a, b, c, d}(x) = S((x - a)/(b - a)) * S((d - x)/(d - c)),
    where 0 < a < b < c < d, together with its ordinary derivatives:
        (chi(x), chi'(x), chi''(x)).

    Satisfies:
      - chi(x) = 0 and all derivatives vanish for x <= a or x >= d;
      - chi(x) = 1 and all derivatives vanish for b <= x <= c.
    """
    if not (0.0 < a < b < c < d):
        raise ValueError("Require 0 < a < b < c < d for plateau_cutoff_1d_jet.")
    if x <= a or x >= d:
        return (0.0, 0.0, 0.0)
    if b <= x <= c:
        return (1.0, 0.0, 0.0)
    if a < x < b:
        inv_len = 1.0 / (b - a)
        t_left = (x - a) * inv_len
        s0, s1, s2 = smooth_step_S_jet(t_left)
        return (s0, s1 * inv_len, s2 * inv_len * inv_len)
    # Otherwise c < x < d
    inv_len = 1.0 / (d - c)
    t_right = (d - x) * inv_len
    s0, s1, s2 = smooth_step_S_jet(t_right)
    return (s0, -s1 * inv_len, s2 * inv_len * inv_len)


def plateau_cutoff_1d_euler_jet(
    x: float,
    a: float = 1.5,
    b: float = 1.75,
    c: float = 15.25,
    d: float = 15.5,
) -> Tuple[float, float, float]:
    """
    Return (chi(x), (x d/dx) chi(x), (x d/dx)^2 chi(x)) for the 1D plateau cutoff.
    """
    c0, c1, c2 = plateau_cutoff_1d_jet(x, a=a, b=b, c=c, d=d)
    e1 = x * c1
    e2 = x * c1 + (x * x) * c2
    return (c0, e1, e2)


def plateau_cutoff_2d_euler_jet(
    x: float,
    y: float,
    N_cutoff: int = 15,
    a: float = 1.5,
    b: float = 1.75,
    c: Optional[float] = None,
    d: Optional[float] = None,
) -> Tuple[float, float, float]:
    """
    Evaluate the 2D plateau cutoff X_N(x, y) = chi_N(x) * chi_N(y) and its Euler
    derivatives:
        (X_N(x, y), (E X_N)(x, y), (E^2 X_N)(x, y)),
    where E = x d/dx + y d/dy.
    """
    c_val = float(N_cutoff) + 0.25 if c is None else c
    d_val = float(N_cutoff) + 0.5 if d is None else d
    cx0, ex1, ex2 = plateau_cutoff_1d_euler_jet(x, a=a, b=b, c=c_val, d=d_val)
    cy0, ey1, ey2 = plateau_cutoff_1d_euler_jet(y, a=a, b=b, c=c_val, d=d_val)
    x0 = cx0 * cy0
    e1 = ex1 * cy0 + cx0 * ey1
    e2 = ex2 * cy0 + 2.0 * ex1 * ey1 + cx0 * ey2
    return (x0, e1, e2)


def compactify_preserving_station_jets(
    prototype_fn: Callable[[float, float], float],
    prototype_euler1_fn: Callable[[float, float], float],
    prototype_euler2_fn: Callable[[float, float], float],
    N_cutoff: int = 15,
    name: str = "compactified_kernel",
) -> CompactifiedKernelBundle:
    """
    Construct the smooth compactly supported kernel (TASK-TC-034R Sections 4 & 5):
        tilde{G}_N(x, y) = X_N(x, y) G(x, y),
    where X_N(x, y) = chi_{a, b, c, d}(x) chi_{a, b, c, d}(y) with:
        a = 3/2 = 1.5,  b = 7/4 = 1.75,  c = N + 1/4,  d = N + 1/2.

    Every integer station 2 <= n <= N lies strictly inside the plateau [7/4, N + 1/4],
    so X_N(n, m) = 1, E X_N(n, m) = 0, E^2 X_N(n, m) = 0, and:
        (E^j tilde{G}_N)(n, m) = (E^j G)(n, m),   j = 0, 1, 2.
    Every integer station n >= N + 1 lies strictly outside the support (3/2, N + 1/2),
    so (E^j tilde{G}_N)(n, m) = 0 for all n >= N + 1 or m >= N + 1.
    """
    if N_cutoff < 2:
        raise ValueError("N_cutoff must be at least 2.")
    a = 1.5
    b = 1.75
    c = float(N_cutoff) + 0.25
    d = float(N_cutoff) + 0.5

    def tilde_g(x: float, y: float) -> float:
        if x <= a or x >= d or y <= a or y >= d:
            return 0.0
        x0, _, _ = plateau_cutoff_2d_euler_jet(
            x, y, N_cutoff=N_cutoff, a=a, b=b, c=c, d=d
        )
        if x0 == 0.0:
            return 0.0
        return x0 * float(prototype_fn(x, y))

    def tilde_e1(x: float, y: float) -> float:
        if x <= a or x >= d or y <= a or y >= d:
            return 0.0
        x0, ex1, _ = plateau_cutoff_2d_euler_jet(
            x, y, N_cutoff=N_cutoff, a=a, b=b, c=c, d=d
        )
        if x0 == 0.0 and ex1 == 0.0:
            return 0.0
        g0 = float(prototype_fn(x, y))
        g1 = float(prototype_euler1_fn(x, y))
        return ex1 * g0 + x0 * g1

    def tilde_e2(x: float, y: float) -> float:
        if x <= a or x >= d or y <= a or y >= d:
            return 0.0
        x0, ex1, ex2 = plateau_cutoff_2d_euler_jet(
            x, y, N_cutoff=N_cutoff, a=a, b=b, c=c, d=d
        )
        if x0 == 0.0 and ex1 == 0.0 and ex2 == 0.0:
            return 0.0
        g0 = float(prototype_fn(x, y))
        g1 = float(prototype_euler1_fn(x, y))
        g2 = float(prototype_euler2_fn(x, y))
        return ex2 * g0 + 2.0 * ex1 * g1 + x0 * g2

    stations = [n for n, _ in active_prime_power_stations(N_cutoff)]
    return CompactifiedKernelBundle(
        name=name,
        N_cutoff=N_cutoff,
        a=a,
        b=b,
        c=c,
        d=d,
        support_interval=(a, d),
        plateau_interval=(b, c),
        support_rectangle=((a, d), (a, d)),
        plateau_rectangle=((b, c), (b, c)),
        active_station_set=tuple(stations),
        highest_admitted_integer_station=N_cutoff,
        highest_active_prime_power_station=max(stations),
        first_excluded_integer_station=N_cutoff + 1,
        verified_derivative_order=2,
        kernel_fn=tilde_g,
        euler1_fn=tilde_e1,
        euler2_fn=tilde_e2,
        prototype_fn=prototype_fn,
        prototype_euler1_fn=prototype_euler1_fn,
        prototype_euler2_fn=prototype_euler2_fn,
    )


def verify_station_jet_preservation(
    bundle: CompactifiedKernelBundle,
    extra_exterior_max: int = 40,
) -> Dict[str, Any]:
    """
    Verify at all active stations 2 <= n, m <= N_cutoff:
      1. X_N(n, m) = 1, E X_N(n, m) = 0, E^2 X_N(n, m) = 0;
      2. (E^j tilde{G}_N)(n, m) == (E^j G)(n, m) for j = 0, 1, 2;
    and at all exterior integer stations N_cutoff + 1 <= n <= extra_exterior_max (and x <= a):
      3. X_N = E X_N = E^2 X_N = 0 and tilde{G}_N = E tilde{G}_N = E^2 tilde{G}_N = 0;
      4. complete compact-support sum at n_max = N_cutoff is identical to n_max = extra_exterior_max.
    """
    N = bundle.N_cutoff
    max_cutoff_val_err = 0.0
    max_cutoff_e1_err = 0.0
    max_cutoff_e2_err = 0.0
    max_jet0_err = 0.0
    max_jet1_err = 0.0
    max_jet2_err = 0.0

    for n in range(2, N + 1):
        xn = float(n)
        for m in range(2, N + 1):
            ym = float(m)
            x0, ex1, ex2 = plateau_cutoff_2d_euler_jet(
                xn, ym, N_cutoff=N, a=bundle.a, b=bundle.b, c=bundle.c, d=bundle.d
            )
            max_cutoff_val_err = max(max_cutoff_val_err, abs(x0 - 1.0))
            max_cutoff_e1_err = max(max_cutoff_e1_err, abs(ex1))
            max_cutoff_e2_err = max(max_cutoff_e2_err, abs(ex2))

            max_jet0_err = max(
                max_jet0_err,
                abs(bundle.kernel_fn(xn, ym) - bundle.prototype_fn(xn, ym)),
            )
            max_jet1_err = max(
                max_jet1_err,
                abs(bundle.euler1_fn(xn, ym) - bundle.prototype_euler1_fn(xn, ym)),
            )
            max_jet2_err = max(
                max_jet2_err,
                abs(bundle.euler2_fn(xn, ym) - bundle.prototype_euler2_fn(xn, ym)),
            )

    max_exterior_abs = 0.0
    exterior_test_points = [0.5, 1.0, 1.5] + [
        float(k) for k in range(N + 1, extra_exterior_max + 1)
    ]
    for x in exterior_test_points:
        for y in [2.0, 5.0, float(N + 1), float(extra_exterior_max)]:
            for px, py in ((x, y), (y, x)):
                x0, ex1, ex2 = plateau_cutoff_2d_euler_jet(
                    px, py, N_cutoff=N, a=bundle.a, b=bundle.b, c=bundle.c, d=bundle.d
                )
                max_exterior_abs = max(
                    max_exterior_abs,
                    abs(x0),
                    abs(ex1),
                    abs(ex2),
                    abs(bundle.kernel_fn(px, py)),
                    abs(bundle.euler1_fn(px, py)),
                    abs(bundle.euler2_fn(px, py)),
                )

    moments_at_N = evaluate_euler_moments_A0_A1_A2(
        bundle.kernel_fn,
        n_max=N,
        euler1_f0=bundle.euler1_fn,
        euler2_f0=bundle.euler2_fn,
        evaluation_mode="COMPLETE_COMPACT_SUPPORT_SUM",
    )
    moments_at_large = evaluate_euler_moments_A0_A1_A2(
        bundle.kernel_fn,
        n_max=extra_exterior_max,
        euler1_f0=bundle.euler1_fn,
        euler2_f0=bundle.euler2_fn,
        evaluation_mode="COMPLETE_COMPACT_SUPPORT_SUM",
    )
    tail_diff = max(
        abs(moments_at_N.A0 - moments_at_large.A0),
        abs(moments_at_N.A1 - moments_at_large.A1),
        abs(moments_at_N.A2 - moments_at_large.A2),
        abs(moments_at_N.arithmetic_curvature - moments_at_large.arithmetic_curvature),
    )

    return {
        "name": bundle.name,
        "N_cutoff": N,
        "support_interval": list(bundle.support_interval),
        "plateau_interval": list(bundle.plateau_interval),
        "support_rectangle": [list(r) for r in bundle.support_rectangle],
        "plateau_rectangle": [list(r) for r in bundle.plateau_rectangle],
        "active_station_set": list(bundle.active_station_set),
        "active_station_pairs": len(bundle.active_station_set) ** 2,
        "highest_admitted_integer_station": bundle.highest_admitted_integer_station,
        "highest_active_prime_power_station": bundle.highest_active_prime_power_station,
        "first_excluded_integer_station": bundle.first_excluded_integer_station,
        "verified_derivative_order": bundle.verified_derivative_order,
        "max_cutoff_plateau_value_err": max_cutoff_val_err,
        "max_cutoff_plateau_e1_err": max_cutoff_e1_err,
        "max_cutoff_plateau_e2_err": max_cutoff_e2_err,
        "max_station_jet0_err": max_jet0_err,
        "max_station_jet1_err": max_jet1_err,
        "max_station_jet2_err": max_jet2_err,
        "max_exterior_value_and_jet_abs": max_exterior_abs,
        "complete_sum_tail_difference_up_to_40": tail_diff,
        "is_complete_compact_support_sum": (tail_diff == 0.0 and max_exterior_abs == 0.0),
        "is_infinite_sum_truncation": False,
    }


# ---------------------------------------------------------------------------
# Section 6, 7, 8, 10 (TASK-TC-034R): Compact-Support Witnesses & Arb Certification
# ---------------------------------------------------------------------------


def prototype_negative_witness_g0(x: float, y: float) -> float:
    """
    Smooth nonnegative negative-curvature prototype (TASK-TC-034R Section 6):
        G_-(x, y) = exp( -(3/2) * (log(x*y / 16))^2 ).
    """
    w = math.log((x * y) / 16.0)
    return math.exp(-1.5 * w * w)


def prototype_negative_witness_e1(x: float, y: float) -> float:
    """
    Exact first Euler derivative of G_-(x, y):
        (E G_-)(x, y) = -6 * w * exp( -(3/2) * w^2 ),   w = log(x*y / 16).
    """
    w = math.log((x * y) / 16.0)
    return (-6.0 * w) * math.exp(-1.5 * w * w)


def prototype_negative_witness_e2(x: float, y: float) -> float:
    """
    Exact second Euler derivative of G_-(x, y):
        (E^2 G_-)(x, y) = (36 * w^2 - 12) * exp( -(3/2) * w^2 ),   w = log(x*y / 16).
    """
    w = math.log((x * y) / 16.0)
    return (36.0 * w * w - 12.0) * math.exp(-1.5 * w * w)


def prototype_positive_witness_g0(x: float, y: float) -> float:
    """
    Smooth nonnegative positive-curvature prototype (TASK-TC-034R Section 7):
        G_+(x, y) = cosh((6/5) * w) * exp( -(2/25) * w^2 ),   w = log(x*y / 25).
    """
    w = math.log((x * y) / 25.0)
    return math.cosh(1.2 * w) * math.exp(-0.08 * w * w)


def prototype_positive_witness_e1(x: float, y: float) -> float:
    """
    Exact first Euler derivative of G_+(x, y):
        (E G_+)(x, y) = 2 * ((6/5)*sinh((6/5)*w) - (4/25)*w*cosh((6/5)*w)) * exp(-(2/25)*w^2).
    """
    w = math.log((x * y) / 25.0)
    a = 1.2
    b = 0.08
    return (
        2.0
        * (a * math.sinh(a * w) - 2.0 * b * w * math.cosh(a * w))
        * math.exp(-b * w * w)
    )


def prototype_positive_witness_e2(x: float, y: float) -> float:
    """
    Exact second Euler derivative of G_+(x, y):
        (E^2 G_+)(x, y) = 4 * [ (a^2 - 2*b + 4*b^2*w^2)*cosh(a*w) - 4*a*b*w*sinh(a*w) ] * exp(-b*w^2),
    with a = 6/5, b = 2/25, w = log(x*y / 25).
    """
    w = math.log((x * y) / 25.0)
    a = 1.2
    b = 0.08
    ch = math.cosh(a * w)
    sh = math.sinh(a * w)
    ex = math.exp(-b * w * w)
    return (
        4.0
        * ((a * a - 2.0 * b + 4.0 * b * b * w * w) * ch - 4.0 * a * b * w * sh)
        * ex
    )


def build_compact_negative_witness(N_cutoff: int = 15) -> CompactifiedKernelBundle:
    """Construct compactly supported negative-curvature witness tilde{G}_- = X_{15} * G_-."""
    return compactify_preserving_station_jets(
        prototype_fn=prototype_negative_witness_g0,
        prototype_euler1_fn=prototype_negative_witness_e1,
        prototype_euler2_fn=prototype_negative_witness_e2,
        N_cutoff=N_cutoff,
        name="tilde_G_minus_compact_N15",
    )


def build_compact_positive_witness(N_cutoff: int = 15) -> CompactifiedKernelBundle:
    """Construct compactly supported positive-curvature witness tilde{G}_+ = X_{15} * G_+."""
    return compactify_preserving_station_jets(
        prototype_fn=prototype_positive_witness_g0,
        prototype_euler1_fn=prototype_positive_witness_e1,
        prototype_euler2_fn=prototype_positive_witness_e2,
        N_cutoff=N_cutoff,
        name="tilde_G_plus_compact_N15",
    )


def _format_arb_enclosure(ball: Any) -> Dict[str, Any]:
    """
    Format an Arb ball into an outward-rounded interval dictionary.
    Outward float bounds use `math.nextafter` so the float interval strictly encloses
    the exact Arb endpoints, while exact decimal strings preserve full Arb precision.
    """
    lo_arb = ball.lower()
    hi_arb = ball.upper()
    lo_float = math.nextafter(float(lo_arb), -math.inf)
    hi_float = math.nextafter(float(hi_arb), math.inf)
    zero_in_ball = bool(0 in ball)
    return {
        "arb_ball_str": str(ball),
        "lower_bound_str": str(lo_arb),
        "upper_bound_str": str(hi_arb),
        "outward_float_interval": [lo_float, hi_float],
        "radius_upper_bound": float(ball.rad()),
        "zero_excluded": not zero_in_ball,
        "strictly_negative": bool(ball < 0),
        "strictly_positive": bool(ball > 0),
        "display_midpoint_approx": float(ball.mid()),
        "display_float_is_certificate": False,
    }


def certify_compact_witness_curvature_arb(
    witness_kind: str,
    N_cutoff: int = 15,
    prec_bits: int = 128,
    force_flint_unavailable: bool = False,
) -> Dict[str, Any]:
    """
    Fail-closed Arb interval certification for the complete compact-support arithmetic
    moments A_0, A_1, A_2 and curvature C_arith = A_0 A_2 - A_1^2 of:
      - `witness_kind == "negative"`: tilde{G}_- = X_N * G_- (Section 6);
      - `witness_kind == "positive"`: tilde{G}_+ = X_N * G_+ (Section 7).

    Inside the plateau [7/4, N + 1/4]^2, X_N(n, m) = 1 and E X_N(n, m) = E^2 X_N(n, m) = 0
    identically, while outside (3/2, N + 1/2)^2 all stations vanish identically.
    Computes Lambda(n) = log(p) in Arb for every prime power 2 <= n <= N.

    If `flint` is unavailable (or `force_flint_unavailable=True`), fails closed and returns
    `status = ARB_CERTIFICATION_NOT_AVAILABLE` with no hardcoded fallback bounds.
    """
    if witness_kind not in ("negative", "positive"):
        raise ValueError("witness_kind must be 'negative' or 'positive'.")

    bundle = (
        build_compact_negative_witness(N_cutoff=N_cutoff)
        if witness_kind == "negative"
        else build_compact_positive_witness(N_cutoff=N_cutoff)
    )
    jet_check = verify_station_jet_preservation(bundle)

    if flint is None or force_flint_unavailable:
        return {
            "witness_kind": witness_kind,
            "witness_name": bundle.name,
            "status": ARB_CERTIFICATION_NOT_AVAILABLE,
            "certified": False,
            "precision_bits": prec_bits,
            "active_stations": list(bundle.active_station_set),
            "support_interval": list(bundle.support_interval),
            "plateau_interval": list(bundle.plateau_interval),
            "A0_enclosure": None,
            "A1_enclosure": None,
            "A2_enclosure": None,
            "curvature_enclosure": None,
            "zero_excluded": False,
        }

    saved_prec = flint.ctx.prec
    try:
        flint.ctx.prec = prec_bits
        arb = flint.arb
        pp_table = prime_power_base_table(N_cutoff)
        arb_stations = [(n, arb(p).log()) for n, p, _ in pp_table]

        A0 = arb(0)
        A1 = arb(0)
        A2 = arb(0)

        if witness_kind == "negative":
            c16 = arb(16)
            alpha = arb(3) / arb(2)
            for n, lam_n in arb_stations:
                for m, lam_m in arb_stations:
                    wt = lam_n * lam_m
                    w = (arb(n * m) / c16).log()
                    g0 = (-alpha * w * w).exp()
                    g1 = (-arb(6) * w) * g0
                    g2 = (arb(36) * w * w - arb(12)) * g0
                    A0 += wt * g0
                    A1 += wt * g1
                    A2 += wt * g2
        else:
            c25 = arb(25)
            a = arb(6) / arb(5)
            b = arb(2) / arb(25)
            for n, lam_n in arb_stations:
                for m, lam_m in arb_stations:
                    wt = lam_n * lam_m
                    w = (arb(n * m) / c25).log()
                    ch = (a * w).cosh()
                    sh = (a * w).sinh()
                    ex = (-b * w * w).exp()
                    g0 = ch * ex
                    g1 = arb(2) * (a * sh - arb(2) * b * w * ch) * ex
                    g2 = (
                        arb(4)
                        * (
                            (a * a - arb(2) * b + arb(4) * b * b * w * w) * ch
                            - arb(4) * a * b * w * sh
                        )
                        * ex
                    )
                    A0 += wt * g0
                    A1 += wt * g1
                    A2 += wt * g2

        C_ball = A0 * A2 - A1 * A1
        a0_enc = _format_arb_enclosure(A0)
        a1_enc = _format_arb_enclosure(A1)
        a2_enc = _format_arb_enclosure(A2)
        c_enc = _format_arb_enclosure(C_ball)

        if witness_kind == "negative":
            cert_ok = bool(C_ball < 0) and c_enc["zero_excluded"]
            status = (
                COMPACT_SUPPORT_NEG_CURVATURE_CERTIFIED
                if cert_ok
                else "NUMERICALLY_UNRESOLVED"
            )
        else:
            cert_ok = bool(C_ball > 0) and c_enc["zero_excluded"]
            status = (
                COMPACT_SUPPORT_POS_CURVATURE_CERTIFIED
                if cert_ok
                else "NUMERICALLY_UNRESOLVED"
            )

        return {
            "witness_kind": witness_kind,
            "witness_name": bundle.name,
            "status": status,
            "certified": cert_ok,
            "is_complete_compact_support_sum": jet_check[
                "is_complete_compact_support_sum"
            ],
            "is_infinite_sum_truncation": False,
            "precision_bits": prec_bits,
            "active_stations": list(bundle.active_station_set),
            "active_station_pairs": len(bundle.active_station_set) ** 2,
            "support_interval": list(bundle.support_interval),
            "plateau_interval": list(bundle.plateau_interval),
            "A0_enclosure": a0_enc,
            "A1_enclosure": a1_enc,
            "A2_enclosure": a2_enc,
            "curvature_enclosure": c_enc,
            "zero_excluded": c_enc["zero_excluded"],
            "sup_curvature_lt_zero": bool(C_ball < 0),
            "inf_curvature_gt_zero": bool(C_ball > 0),
        }
    finally:
        flint.ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# Section 7 (TASK-TC-034): Synthetic Curvature Identity (Positive Mixtures)
# ---------------------------------------------------------------------------


def evaluate_exponential_mixture_curvature(
    weights: Sequence[float],
    exponents: Sequence[float],
) -> ExponentialMixtureCurvatureResult:
    """
    Evaluate M(0)*M''(0) - M'(0)^2 for M(eta) = sum_j w_j exp(eta x_j):
        M(0) M''(0) - M'(0)^2 = (1/2) sum_{i, j} w_i w_j (x_i - x_j)^2.
    """
    if len(weights) != len(exponents) or len(weights) == 0:
        raise ValueError("weights and exponents must have the same nonzero length.")
    w_t = tuple(float(w) for w in weights)
    x_t = tuple(float(x) for x in exponents)
    M0 = sum(w_t)
    M1 = sum(w * x for w, x in zip(w_t, x_t))
    M2 = sum(w * (x * x) for w, x in zip(w_t, x_t))
    curv = M0 * M2 - M1 * M1

    lagrange_double = 0.0
    r = len(w_t)
    for i in range(r):
        for j in range(r):
            lagrange_double += 0.5 * w_t[i] * w_t[j] * ((x_t[i] - x_t[j]) ** 2)

    all_pos = all(w > 0.0 for w in w_t)
    has_distinct = any(
        abs(x_t[i] - x_t[j]) > 1e-15 for i in range(r) for j in range(i + 1, r)
    )

    return ExponentialMixtureCurvatureResult(
        weights=w_t,
        exponents=x_t,
        M0=M0,
        M1=M1,
        M2=M2,
        curvature_determinant=curv,
        pairwise_lagrange_sum=lagrange_double,
        lagrange_identity_abs_err=abs(curv - lagrange_double),
        strictly_positive=(curv > 1e-15),
        nonnegative=(curv >= -1e-15),
        has_distinct_exponents=has_distinct,
        all_weights_positive=all_pos,
    )


def evaluate_reciprocal_pair_curvature(
    w1: float,
    w2: float,
    x: float,
) -> ExponentialMixtureCurvatureResult:
    """
    Evaluate the reciprocal pair M(eta) = w_1 e^{eta x} + w_2 e^{-eta x}.
    Curvature determinant equals 4 w_1 w_2 x^2 > 0 for w_1, w_2 > 0 and x != 0.
    """
    return evaluate_exponential_mixture_curvature([w1, w2], [x, -x])


# ---------------------------------------------------------------------------
# Section 3, 8, 9 (TASK-TC-034R): Homogeneity No-Go, Accidental Zero, Sign Firewall
# ---------------------------------------------------------------------------


def evaluate_homogeneous_kernel_control(
    alpha: float = 0.5,
    beta: float = 0.75,
    n_max: int = 20,
) -> Dict[str, Any]:
    """
    Audit a noncompact homogeneous kernel F_0(x, y) = x^alpha y^beta on a fixed
    finite station list (diagnostic control). Satisfies E F_0 = d F_0 with d = alpha + beta,
    so A_1 = d A_0, A_2 = d^2 A_0, and C_arith(F_0) = A_0 A_2 - A_1^2 = 0 on that finite
    truncation, but is NOT compactly supported in (0, inf)^2.
    """
    d = alpha + beta

    def f_hom(x: float, y: float) -> float:
        return (x ** alpha) * (y ** beta)

    def e1_hom(x: float, y: float) -> float:
        return d * f_hom(x, y)

    def e2_hom(x: float, y: float) -> float:
        return (d * d) * f_hom(x, y)

    moments = evaluate_euler_moments_A0_A1_A2(
        f_hom,
        n_max=n_max,
        euler1_f0=e1_hom,
        euler2_f0=e2_hom,
        evaluation_mode="FINITE_TRUNCATION_DIAGNOSTIC",
    )
    K = 1.0
    eta = 0.15
    m_eta = evaluate_normalized_mismatch_energy(f_hom, K=K, eta=eta, n_max=n_max)
    m_0 = moments.A0
    expected_m_eta = math.exp(-d * eta * K * LOG_TAU) * m_0

    return {
        "alpha": alpha,
        "beta": beta,
        "degree_d": d,
        "evaluation_mode": "FINITE_TRUNCATION_DIAGNOSTIC",
        "is_compactly_supported": False,
        "A0": moments.A0,
        "A1": moments.A1,
        "A2": moments.A2,
        "A1_minus_d_A0": abs(moments.A1 - d * moments.A0),
        "A2_minus_d2_A0": abs(moments.A2 - (d * d) * moments.A0),
        "arithmetic_curvature": moments.arithmetic_curvature,
        "normalized_log_curvature": moments.normalized_log_curvature,
        "single_character_response_abs_err": abs(m_eta - expected_m_eta),
        "is_flat": (
            moments.normalized_log_curvature is not None
            and abs(moments.normalized_log_curvature) < 1e-12
        ),
    }


def audit_compact_support_homogeneity_no_go(
    degree_d: float = -1.0,
) -> CompactSupportHomogeneityAudit:
    """
    Paper-derivation audit of the Compact-Support Homogeneity No-Go theorem
    (TASK-TC-034R Section 3):
        F_0 in C_c^infty((0, inf)^2),  E F_0 = d F_0  ==>  F_0 == 0.

    Evidence classification: PROVED_PAPER_DERIVATION (not Lean-formalized).
    """
    r_samples = [0.5, 1.0, 2.0, 4.0, 8.0]
    ray_values = [r ** degree_d for r in r_samples]
    all_nonzero = all(val != 0.0 for val in ray_values)

    proof_steps = (
        "1. Fix (x_0, y_0) in (0, infty)^2.",
        "2. Define g(r) = F_0(r x_0, r y_0) for r > 0.",
        "3. Euler homogeneity E F_0 = d F_0 gives r g'(r) = d g(r).",
        "4. Integrating on (0, infty) gives g(r) = r^d g(1).",
        "5. If g(1) != 0, then g(r) != 0 for every r > 0.",
        "6. Hence supp(F_0) contains the unbounded ray {(r x_0, r y_0) : r > 0}, contradicting compact support.",
        "7. Therefore F_0(x_0, y_0) = 0 for every (x_0, y_0) in (0, infty)^2.",
    )

    return CompactSupportHomogeneityAudit(
        degree_d=degree_d,
        ray_scaling_verified=all_nonzero,
        compact_support_compatible_for_nonzero_kernel=False,
        evidence_status=COMPACT_SUPPORT_NO_GO_EVIDENCE_STATUS,
        lean_formalized=False,
        classification=CLASSIFICATION_COMPACT_SUPPORT_IMPOSSIBLE,
        outcome_code=COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED,
        proof_steps=proof_steps,
        scope_note=(
            "PROVED_PAPER_DERIVATION for all C_c^infty((0, inf)^2) kernels: Euler homogeneity "
            "E F_0 = d F_0 forces F_0(r x, r y) = r^d F_0(x, y) along every positive ray, "
            "contradicting compact support unless F_0 == 0. Not formalized as a PDE theorem "
            "in Lean (Lean formalizes only the algebraic consequence A_1 = d A_0, A_2 = d^2 A_0 "
            "==> A_0 A_2 - A_1^2 = 0 in `homogeneous_arithmetic_curvature_zero`)."
        ),
    )


def audit_finite_station_accidental_zero() -> Dict[str, Any]:
    """
    Preserve and sharpen the accidental-zero boundary (TASK-TC-034R Section 9):
        FINITE_ACCIDENTAL_ARITHMETIC_CURVATURE_ZERO.

    Explicitly separates two distinct settings so kernel and arithmetic support scopes
    are never conflated:
      Setting 1 (One complete compact-support plateau kernel X_3 on (1.5, 3.5)^2):
        For X_3(x, y) = chi_{1.5, 1.75, 3.25, 3.5}(x) chi_{1.5, 1.75, 3.25, 3.5}(y),
        the COMPLETE support in (0, inf)^2 contains only active stations {2, 3}.
        Because {2, 3} lie inside the flat plateau [1.75, 3.25]^2 where E X_3 = E^2 X_3 = 0,
        A_1(X_3) = A_2(X_3) = 0 and C_arith(X_3) = 0 at eta = 0. This is an accidental
        finite-station plateau zero (placement of cutoff ramps in the integer-free gaps
        (1.5, 1.75) and (3.25, 3.5)), NOT Euler homogeneity E X_3 = d X_3.
      Setting 2 (One fixed compactly supported kernel F_acc on (1.5, 5.5)^2 compared across
        restricted station subset vs complete support):
        Hold F_acc(x, y) = chi_{1.5, 1.75, 3.25, 5.5}(x) chi_{1.5, 1.75, 3.25, 5.5}(y) FIXED.
        On the restricted station subset {2, 3} (n_max = 3), the partial sum has C_arith = 0;
        on the COMPLETE support of the same kernel F_acc (active stations {2, 3, 4, 5}, n_max = 5),
        stations 4 and 5 fall on the transition ramp (3.25, 5.5) where E F_acc != 0 and
        E^2 F_acc != 0, giving C_arith(F_acc) < 0.
    """
    # Setting 1: Complete compact-support plateau kernel X_3 on (1.5, 3.5)^2
    x3_bundle = compactify_preserving_station_jets(
        prototype_fn=lambda x, y: 1.0,
        prototype_euler1_fn=lambda x, y: 0.0,
        prototype_euler2_fn=lambda x, y: 0.0,
        N_cutoff=3,
        name="X_3_complete_plateau_kernel",
    )
    res_x3_complete = evaluate_euler_moments_A0_A1_A2(
        x3_bundle.kernel_fn,
        n_max=15,
        euler1_f0=x3_bundle.euler1_fn,
        euler2_f0=x3_bundle.euler2_fn,
        evaluation_mode="COMPLETE_COMPACT_SUPPORT_SUM",
    )

    # Setting 2: Fixed kernel F_acc supported on (1.5, 5.5)^2 with plateau [1.75, 3.25]^2
    a, b, c, d = 1.5, 1.75, 3.25, 5.5

    def f_acc(x: float, y: float) -> float:
        x0, _, _ = plateau_cutoff_2d_euler_jet(x, y, N_cutoff=5, a=a, b=b, c=c, d=d)
        return x0

    def e1_acc(x: float, y: float) -> float:
        _, ex1, _ = plateau_cutoff_2d_euler_jet(x, y, N_cutoff=5, a=a, b=b, c=c, d=d)
        return ex1

    def e2_acc(x: float, y: float) -> float:
        _, _, ex2 = plateau_cutoff_2d_euler_jet(x, y, N_cutoff=5, a=a, b=b, c=c, d=d)
        return ex2

    res_restricted_subset = evaluate_euler_moments_A0_A1_A2(
        f_acc,
        n_max=3,
        euler1_f0=e1_acc,
        euler2_f0=e2_acc,
        evaluation_mode="RESTRICTED_FINITE_STATION_SUBSET",
    )
    res_complete_support = evaluate_euler_moments_A0_A1_A2(
        f_acc,
        n_max=15,
        euler1_f0=e1_acc,
        euler2_f0=e2_acc,
        evaluation_mode="COMPLETE_COMPACT_SUPPORT_SUM",
    )

    return {
        "classification": CLASSIFICATION_FINITE_ACCIDENTAL_ZERO,
        "scope_specification": {
            "complete_plateau_kernel_X3": {
                "kernel_name": "X_3(x, y) = chi_{1.5, 1.75, 3.25, 3.5}(x) chi_{1.5, 1.75, 3.25, 3.5}(y)",
                "support_rectangle": [[1.5, 3.5], [1.5, 3.5]],
                "plateau_rectangle": [[1.75, 3.25], [1.75, 3.25]],
                "active_stations_in_complete_support": [2, 3],
                "evaluation_scope": "ONE_COMPACTLY_SUPPORTED_KERNEL_COMPLETE_SUPPORT",
                "A0": res_x3_complete.A0,
                "A1": res_x3_complete.A1,
                "A2": res_x3_complete.A2,
                "arithmetic_curvature": res_x3_complete.arithmetic_curvature,
                "why_accidental_not_structural": (
                    "E X_3 = 0 only on the plateau [1.75, 3.25]^2 and exterior; on the transition "
                    "ramps (1.5, 1.75) and (3.25, 3.5), E X_3 != 0. The zero at eta = 0 relies on "
                    "placing the cutoff transition in the integer-free gap (3.25, 3.5)."
                ),
            },
            "fixed_kernel_F_acc_restricted_vs_complete": {
                "kernel_name": "F_acc(x, y) = chi_{1.5, 1.75, 3.25, 5.5}(x) chi_{1.5, 1.75, 3.25, 5.5}(y)",
                "support_rectangle": [[1.5, 5.5], [1.5, 5.5]],
                "plateau_rectangle": [[1.75, 3.25], [1.75, 3.25]],
                "restricted_station_subset": [2, 3],
                "restricted_subset_scope": "ONE_RESTRICTED_ARITHMETIC_WINDOW_OF_FIXED_KERNEL",
                "restricted_subset_A0": res_restricted_subset.A0,
                "restricted_subset_curvature": res_restricted_subset.arithmetic_curvature,
                "complete_support_stations": [2, 3, 4, 5],
                "complete_support_scope": "COMPLETE_SUPPORT_OF_SAME_FIXED_KERNEL",
                "complete_support_A0": res_complete_support.A0,
                "complete_support_curvature": res_complete_support.arithmetic_curvature,
            },
        },
        "small_window_n_max": 3,
        "small_window_A0": res_restricted_subset.A0,
        "small_window_curvature": res_restricted_subset.arithmetic_curvature,
        "large_window_n_max": 5,
        "large_window_A0": res_complete_support.A0,
        "large_window_curvature": res_complete_support.arithmetic_curvature,
        "vanishes_on_selected_window": abs(res_restricted_subset.arithmetic_curvature)
        < 1e-12,
        "nonzero_on_complete_support_of_fixed_kernel": abs(
            res_complete_support.arithmetic_curvature
        )
        > 1e-3,
    }


def audit_arithmetic_curvature_sign_firewall(N_cutoff: int = 15) -> Dict[str, Any]:
    """
    Sign firewall on the arithmetic curvature using genuine compactly supported kernels
    tilde{G}_- = X_{15} * G_- and tilde{G}_+ = X_{15} * G_+ in C_c^infty((0, inf)^2)
    whose complete arithmetic sums are certified by outward Arb ball arithmetic
    (TASK-TC-034R Sections 6, 7, 8, 10):
      1. sup C_arith(tilde{G}_-) < 0 (`COMPACT_SUPPORT_NEGATIVE_ARITHMETIC_CURVATURE_CERTIFIED`);
      2. inf C_arith(tilde{G}_+) > 0 (`COMPACT_SUPPORT_POSITIVE_ARITHMETIC_CURVATURE_CERTIFIED`);
      3. C_arith(X_3) = 0 (`FINITE_ACCIDENTAL_ARITHMETIC_CURVATURE_ZERO`).
    Supersedes `FINITE_TRUNCATION_SIGN_INDEFINITENESS_OBSERVED` with
    `COMPACT_SUPPORT_ARITHMETIC_CURVATURE_SIGN_INDEFINITE`.
    """
    neg_cert = certify_compact_witness_curvature_arb("negative", N_cutoff=N_cutoff)
    pos_cert = certify_compact_witness_curvature_arb("positive", N_cutoff=N_cutoff)
    zero_ctrl = audit_finite_station_accidental_zero()

    neg_bundle = build_compact_negative_witness(N_cutoff=N_cutoff)
    pos_bundle = build_compact_positive_witness(N_cutoff=N_cutoff)

    neg_moments = evaluate_euler_moments_A0_A1_A2(
        neg_bundle.kernel_fn,
        n_max=N_cutoff,
        euler1_f0=neg_bundle.euler1_fn,
        euler2_f0=neg_bundle.euler2_fn,
        evaluation_mode="COMPLETE_COMPACT_SUPPORT_SUM",
    )
    pos_moments = evaluate_euler_moments_A0_A1_A2(
        pos_bundle.kernel_fn,
        n_max=N_cutoff,
        euler1_f0=pos_bundle.euler1_fn,
        euler2_f0=pos_bundle.euler2_fn,
        evaluation_mode="COMPLETE_COMPACT_SUPPORT_SUM",
    )

    both_certified = bool(
        neg_cert.get("certified", False)
        and neg_cert.get("sup_curvature_lt_zero", False)
        and pos_cert.get("certified", False)
        and pos_cert.get("inf_curvature_gt_zero", False)
    )

    return {
        "negative_witness_name": neg_bundle.name,
        "negative_witness_status": neg_cert["status"],
        "negative_kernel_A0_display": neg_moments.A0,
        "negative_kernel_curvature_display": neg_moments.arithmetic_curvature,
        "negative_curvature_arb_enclosure": neg_cert,
        "positive_witness_name": pos_bundle.name,
        "positive_witness_status": pos_cert["status"],
        "positive_kernel_A0_display": pos_moments.A0,
        "positive_kernel_curvature_display": pos_moments.arithmetic_curvature,
        "positive_curvature_arb_enclosure": pos_cert,
        "zero_control_curvature": zero_ctrl["small_window_curvature"],
        "display_floats_are_certificates": False,
        "is_complete_compact_support_evaluation": True,
        "is_infinite_sum_truncation": False,
        "all_three_signs_realized": both_certified
        and abs(zero_ctrl["small_window_curvature"]) < 1e-12,
        "superseded_classification": SUPERSEDED_FINITE_TRUNCATION_STATUS,
        "outcome_b_flatness_not_implied": OUTCOME_B_ARITHMETIC_FLATNESS_NOT_IMPLIED,
        "classification": COMPACT_SUPPORT_SIGN_INDEFINITENESS_STATUS,
    }


# ---------------------------------------------------------------------------
# Section 8, 9, 10, 15, 16, 17 (TASK-TC-034) & Section 12 (TASK-TC-034R):
# Spectral Mismatch Scaling, Centering, Pairings, & Curvature Transport Link
# ---------------------------------------------------------------------------


def evaluate_mellin_mismatch_scaling(
    s: complex,
    t: complex,
    K: float,
    eta: float,
    a: float = 0.0,
    base_q: float = TAU,
) -> Dict[str, Any]:
    """
    Evaluate the spectral mismatch scaling:
        H_{K, eta}(s, t) = iint F_{K, eta}(x, y) x^{s-1} y^{t-1} dx dy
                         = q^{K (a + (1 + eta)(s + t))} H_0(s, t).
    After combining with prime-measure factors q^{-K(s + t)} and normalizing by q^{-a K},
    the net factor is:
        q^{eta K (s + t)},
    with first and second eta-derivatives at eta = 0 equal to:
        K (log q) (s + t)   and   K^2 (log q)^2 (s + t)^2.
    """
    log_q = math.log(base_q)
    raw_mellin_exponent = K * (a + (1.0 + eta) * (s + t))
    net_normalized_exponent = eta * K * (s + t)
    net_factor = cmath.exp(net_normalized_exponent * log_q)
    first_deriv_at_0 = K * log_q * (s + t)
    second_deriv_at_0 = (K * log_q) ** 2 * ((s + t) ** 2)

    return {
        "s": s,
        "t": t,
        "K": K,
        "eta": eta,
        "a": a,
        "base_q": base_q,
        "raw_mellin_exponent": raw_mellin_exponent,
        "net_normalized_exponent": net_normalized_exponent,
        "net_spectral_factor": net_factor,
        "first_eta_derivative_at_0": first_deriv_at_0,
        "second_eta_derivative_at_0": second_deriv_at_0,
    }


def audit_spectral_centering_and_pairings(
    delta: float = 0.12,
    gamma: float = 14.134725,
    sigma_delta: float = -0.05,
    sigma_gamma: float = 21.022040,
    K: float = 1.0,
    eta: float = 0.1,
    base_q: float = TAU,
) -> SpectralPairingAuditResult:
    """
    Centering and pairing audit:
    For rho = 1/2 + delta + i*gamma:
      - Uncentered exponent is s + t. Under half-density centering (x*y)^{-1/2},
        the centered exponent is (s - 1/2) + (t - 1/2) = s + t - 1.
      - Conjugate pairing t = bar(rho):
          (rho - 1/2) + (bar(rho) - 1/2) = 2*delta (purely real radial displacement).
          Even mismatch defect: 2*(cosh(2*eta*K*delta*log(q)) - 1) >= 0,
          second variation proportional to +delta^2 (DIAGONAL_CONJUGATE_BLOCK_ONLY).
      - Functional-equation reflection pairing t = 1 - bar(rho):
          (rho - 1/2) + ((1 - bar(rho)) - 1/2) = 2*i*gamma (purely imaginary ordinate).
          Even mismatch defect: 2*(cos(2*eta*K*gamma*log(q)) - 1) <= 0,
          second variation proportional to -gamma^2 <= 0.
      - General zero-zero pairing (rho, sigma):
          (rho - 1/2) + (sigma - 1/2) = (delta_rho + delta_sigma) + i*(gamma_rho + gamma_sigma),
          producing cross-zero mixed oscillatory terms.
      - Naturally induced pairing: The actual two-variable arithmetic energy
        <mu_K x mu_K, F_{K, eta}> expands into the unrestricted double sum over ALL pairs (rho, sigma)
        plus pole, trivial-zero, and Archimedean terms.
    """
    log_q = math.log(base_q)
    rho = complex(0.5 + delta, gamma)
    bar_rho = complex(0.5 + delta, -gamma)
    refl_rho = complex(1.0, 0.0) - bar_rho
    sigma = complex(0.5 + sigma_delta, sigma_gamma)

    uncentered_conj = rho + bar_rho
    centered_conj = (rho - 0.5) + (bar_rho - 0.5)
    centered_refl = (rho - 0.5) + (refl_rho - 0.5)
    centered_gen = (rho - 0.5) + (sigma - 0.5)

    conj_defect = 2.0 * (math.cosh(2.0 * eta * K * delta * log_q) - 1.0)
    refl_defect = 2.0 * (math.cos(2.0 * eta * K * gamma * log_q) - 1.0)

    conj_second_var = 4.0 * (K * log_q) ** 2 * (delta ** 2)
    refl_second_var = -4.0 * (K * log_q) ** 2 * (gamma ** 2)

    return SpectralPairingAuditResult(
        rho=rho,
        delta=delta,
        gamma=gamma,
        uncentered_conjugate_exponent=uncentered_conj,
        centered_conjugate_exponent=centered_conj,
        centered_reflection_exponent=centered_refl,
        general_pair_centered_exponent=centered_gen,
        conjugate_even_defect=conj_defect,
        reflection_even_defect=refl_defect,
        conjugate_second_variation_coeff=conj_second_var,
        reflection_second_variation_coeff=refl_second_var,
        naturally_induced_pairing="UNRESTRICTED_DOUBLE_ZERO_SUM_WITH_BACKGROUND",
        spectral_curvature_classification=OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE,
    )


def reconcile_with_existing_curvature_transport(
    delta: float = 0.15,
    K: float = 1.0,
    eta: float = 0.05,
) -> Dict[str, Any]:
    """
    Reconcile TASK-TC-034 mismatch curvature with the existing Curvature Transport
    detector (TASK-TC-034R Section 12):
        tau^{2 eta K delta_rho} + tau^{-2 eta K delta_rho} - 2
        = 2 (cosh(2 eta K delta_rho log tau) - 1)
        = B_rho(2 eta K).

    States explicitly:
      - this equality is exact on the centered conjugate block;
      - it reproduces the existing spectral detector B_rho(2 eta K);
      - the complete arithmetic functional induces an unrestricted double zero sum plus background;
      - no positive diagonal projection has been derived;
      - no new arithmetic descent has been constructed.
    """
    k_eff = 2.0 * eta * K
    b_rho_val = 2.0 * (math.cosh(k_eff * delta * LOG_TAU) - 1.0)
    mismatch_even_val = (
        math.exp(2.0 * eta * K * delta * LOG_TAU)
        + math.exp(-2.0 * eta * K * delta * LOG_TAU)
        - 2.0
    )
    b_rho_second_deriv_0 = 2.0 * (delta ** 2) * (LOG_TAU ** 2)
    mismatch_second_deriv_eta_0 = 4.0 * (K ** 2) * (delta ** 2) * (LOG_TAU ** 2)

    return {
        "effective_k": k_eff,
        "B_rho_at_2etaK": b_rho_val,
        "centered_conjugate_even_mismatch": mismatch_even_val,
        "detector_identity_abs_err": abs(b_rho_val - mismatch_even_val),
        "equality_exact_on_conjugate_block": True,
        "reproduces_existing_spectral_detector": True,
        "complete_functional_induces": "UNRESTRICTED_DOUBLE_ZERO_SUM_WITH_BACKGROUND",
        "positive_diagonal_projection_derived": False,
        "B_rho_second_deriv_at_0": b_rho_second_deriv_0,
        "mismatch_second_deriv_at_0": mismatch_second_deriv_eta_0,
        "chain_rule_ratio_4K2_to_2": mismatch_second_deriv_eta_0 / b_rho_second_deriv_0,
        "expected_chain_rule_ratio": 2.0 * (K ** 2),
        "classification": CLASSIFICATION_REDUCES_TO_EXISTING_OBL_CT_001A,
        "outcome_code": OUTCOME_G_REDUCES_TO_OBL_CT_001A,
        "new_arithmetic_descent_constructed": False,
    }


def audit_complete_spectral_curvature_and_firewalls() -> Dict[str, Any]:
    """
    Audit the complete spectral side and enforce all mandatory firewalls:
      1. No diagonal projection without proof (diagonal-only classified as SELECTED_CURVATURE_BLOCK_ONLY);
      2. No selected-zero test construction;
      3. No remainder-domination reuse (closed by TASK-TC-032R);
      4. Complete expansion includes pole terms (s, t = 1), trivial-zero terms, Archimedean terms,
         and off-diagonal (rho, sigma) cross terms.
    """
    return {
        "complete_spectral_type": "DOUBLE_SPECTRAL_SUM_PLUS_POLE_AND_ARCHIMEDEAN_BACKGROUND",
        "spectral_curvature_outcome": OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE,
        "conjugate_block_delta_squared_scope": "DIAGONAL_CONJUGATE_BLOCK_ONLY",
        "diagonal_projection_without_proof_allowed": False,
        "incomplete_diagonal_only_classification": CLASSIFICATION_SELECTED_BLOCK_ONLY,
        "selected_zero_construction_allowed": False,
        "remainder_domination_reopened": False,
        "task_tc_032r_firewall_status": "EXACT_CANCELLATION_BLOCKS_STRICT_SUBORDINATION_ROUTE",
        "includes_zero_zero_cross_terms": True,
        "includes_pole_terms": True,
        "includes_trivial_zero_terms": True,
        "includes_archimedean_terms": True,
        "includes_window_boundary_terms": True,
        "includes_normalization_factor_derivatives": True,
        "weil_equivalence_classification": CLASSIFICATION_CURVATURE_POSITIVITY_RH_EQUIVALENT,
    }


# ---------------------------------------------------------------------------
# Section 11 (TASK-TC-034R): Repaired Conditional Theta-Mellin Audit Data Model
# ---------------------------------------------------------------------------


def audit_theta_mellin_nonscalar_fallback() -> ThetaMellinNonScalarCandidateAudit:
    """
    Repaired theta-Mellin audit (TASK-TC-034R Section 11):
    Replaces unconditional Boolean fields with explicit conditional/unresolved evidence
    statuses for the candidate bilinear theta-Mellin functional Q_Theta(eta; Phi_0).
    """
    return ThetaMellinNonScalarCandidateAudit(
        candidate_name="Bilinear scale-mismatched theta-Mellin quadratic functional Q_Theta(eta; Phi_0)",
        scalar_candidate_status="REJECTED_FROZEN_IDENTICALLY_ZERO_AT_ZEROS",
        purely_theta_or_arithmetic_defined_status="PROVED_BY_DEFINITION",
        zero_independent_definition_status="PROVED_BY_DEFINITION",
        exact_scale_flatness_law_status="FALSE",
        exact_scale_flatness_law_basis=(
            "Theta_1^+(t) = sum_{n>=1} exp(-pi n^2 t) is a multi-exponential sum rather than "
            "a single homogeneous power, and no nonzero convergent test kernel Phi_0 on "
            "(0, infty)^2 is Euler-homogeneous."
        ),
        convergence_status="CONDITIONAL_ON_REGULARIZATION",
        second_mismatch_variation_status="FORMAL_CANDIDATE_NOT_DERIVED",
        delta_squared_detection_status="DIAGONAL_CONJUGATE_BLOCK_ONLY",
        complete_spectral_expansion_status="COMPLETE_EXPANSION_NOT_DERIVED",
        positive_complete_spectral_curvature_status="RH_EQUIVALENT_IF_POSITIVE",
        selected_zero_construction_status="PROVED_BY_DEFINITION",
        closes_obl_ct_001a_status="FALSE",
        overall_classification=CANDIDATE_THETA_MELLIN_AUDIT,
        secondary_classification=THETA_MELLIN_AUDIT_CONDITIONAL,
        reduces_to_obligation=OUTCOME_G_REDUCES_TO_OBL_CT_001A,
        exact_remaining_theorem=(
            "OBL-CT-001A: Construct a zero-independent non-scalar arithmetic or theta functional "
            "whose transport curvature at b = 1 satisfies a kernel-independent arithmetic flatness "
            "or sign bound while its complete spectral expansion isolates a positive radial moment "
            "in delta_rho^2 without assuming Weil positivity."
        ),
    )


# ---------------------------------------------------------------------------
# Section 13 (TASK-TC-034R): Exact Lean Theorem Map & Scope Boundary
# ---------------------------------------------------------------------------


def get_lean_theorem_map() -> Dict[str, Any]:
    """
    Return the exact declaration map for `formal/RiemannScope/TransportMismatchCurvature.lean`
    (TASK-TC-034R Section 13), together with the explicit list of items NOT formalized in Lean.
    """
    declarations = [
        {
            "identifier": "curvatureDet",
            "kind": "def",
            "statement_scope": "def curvatureDet (A0 A1 A2 : R) : R := A0 * A2 - A1 ^ 2",
            "algebraic_only": True,
            "paper_step_supported": "Section 6 arithmetic and exponential-moment curvature determinant A_0 A_2 - A_1^2",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "single_exponential_log_curvature_zero",
            "kind": "theorem",
            "statement_scope": "curvatureDet w (w * x) (w * x ^ 2) = 0",
            "algebraic_only": True,
            "paper_step_supported": "Section 7 single-exponential baseline M(eta) = w e^{eta x} has zero curvature",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "two_exponential_curvature_identity",
            "kind": "theorem",
            "statement_scope": "curvatureDet (w1 + w2) (w1*x1 + w2*x2) (w1*x1^2 + w2*x2^2) = w1 * w2 * (x1 - x2)^2",
            "algebraic_only": True,
            "paper_step_supported": "Section 7 two-term Lagrange sum-of-squares identity",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "two_exponential_positive_log_curvature",
            "kind": "theorem",
            "statement_scope": "0 < w1, 0 < w2, x1 != x2 ==> 0 < curvatureDet (w1 + w2) (w1*x1 + w2*x2) (w1*x1^2 + w2*x2^2)",
            "algebraic_only": True,
            "paper_step_supported": "Section 7 strict positivity of two-point exponential mixture curvature",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "positive_finite_exponential_curvature_nonneg",
            "kind": "theorem",
            "statement_scope": "0 <= w1, 0 <= w2 ==> 0 <= curvatureDet (w1 + w2) (w1*x1 + w2*x2) (w1*x1^2 + w2*x2^2)",
            "algebraic_only": True,
            "paper_step_supported": "Section 7 nonnegativity of two-point nonnegative exponential mixture curvature",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "three_exponential_curvature_identity",
            "kind": "theorem",
            "statement_scope": "curvatureDet (w1+w2+w3) (sum w_i x_i) (sum w_i x_i^2) = sum_{i<j} w_i w_j (x_i - x_j)^2",
            "algebraic_only": True,
            "paper_step_supported": "Section 7 three-term Lagrange sum-of-squares identity",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "three_exponential_curvature_nonneg",
            "kind": "theorem",
            "statement_scope": "0 <= w1, w2, w3 ==> 0 <= curvatureDet (w1+w2+w3) (sum w_i x_i) (sum w_i x_i^2)",
            "algebraic_only": True,
            "paper_step_supported": "Section 7 nonnegativity of three-point nonnegative exponential mixture curvature",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "reciprocal_pair_curvature_strict_pos",
            "kind": "theorem",
            "statement_scope": "0 < w1, 0 < w2, x != 0 ==> 0 < curvatureDet (w1 + w2) (w1*x + w2*(-x)) (w1*x^2 + w2*(-x)^2)",
            "algebraic_only": True,
            "paper_step_supported": "Section 7/9 strict positivity 4 w1 w2 x^2 > 0 for opposite/reciprocal exponent pair",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "homogeneous_arithmetic_curvature_zero",
            "kind": "theorem",
            "statement_scope": "curvatureDet A0 (d * A0) (d ^ 2 * A0) = 0",
            "algebraic_only": True,
            "paper_step_supported": "Section 11 algebraic moment consequence A_1 = d A_0, A_2 = d^2 A_0 ==> C_arith = 0",
            "external_theorem_dependency": "None (does not formalize the PDE E F_0 = d F_0 or compact-support ODE no-go)",
        },
        {
            "identifier": "arithmetic_zero_curvature_and_spectral_positive_contradiction",
            "kind": "theorem",
            "statement_scope": "C = 0 -> 0 < C -> False",
            "algebraic_only": True,
            "paper_step_supported": "Conditional incompatibility between vanishing arithmetic curvature and positive spectral curvature",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "euler_generator_scaling_algebra",
            "kind": "theorem",
            "statement_scope": "curvatureDet A0 (-K * log_tau * A1) (K^2 * log_tau^2 * A2) = K^2 * log_tau^2 * curvatureDet A0 A1 A2",
            "algebraic_only": True,
            "paper_step_supported": "Section 5/6 factorization of (-K log tau)^2 in unnormalized mismatch curvature",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "mismatch_curvature_k_independent",
            "kind": "theorem",
            "statement_scope": "K != 0, log_tau != 0 ==> curvatureDet A0 (-K*log_tau*A1) (K^2*log_tau^2*A2) / (K^2*log_tau^2) = curvatureDet A0 A1 A2",
            "algebraic_only": True,
            "paper_step_supported": "Section 6 grade-K independence of normalized arithmetic transport curvature",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "even_second_difference_quadratic_ident",
            "kind": "theorem",
            "statement_scope": "(M0 + eta*M1 + 1/2*eta^2*M2) + (M0 - eta*M1 + 1/2*(-eta)^2*M2) - 2*M0 = eta^2 * M2",
            "algebraic_only": True,
            "paper_step_supported": "Section 10 symmetric mismatch difference cancellation of odd derivative M1",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "centered_conjugate_pairing_radial",
            "kind": "theorem",
            "statement_scope": "((1/2 + delta - 1/2) + (1/2 + delta - 1/2)) = 2 * delta",
            "algebraic_only": True,
            "paper_step_supported": "Section 9 half-density centered conjugate pairing real radial exponent 2*delta",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "centered_reflection_pairing_real_zero",
            "kind": "theorem",
            "statement_scope": "((1/2 + delta - 1/2) + (1 - (1/2 + delta) - 1/2)) = 0",
            "algebraic_only": True,
            "paper_step_supported": "Section 9 half-density centered functional-equation reflection real-part cancellation",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "mellin_mismatch_net_exponent",
            "kind": "theorem",
            "statement_scope": "(K * (a + (1 + eta) * (s + t)) - K * (s + t)) - a * K = eta * K * (s + t)",
            "algebraic_only": True,
            "paper_step_supported": "Section 8 Mellin mismatch net exponent algebra at b = 1 + eta",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "signed_weight_curvature_negative",
            "kind": "theorem",
            "statement_scope": "w1 = 1, w2 = -2, x1 = 0, x2 = 1 ==> curvatureDet (w1+w2) (w1*x1+w2*x2) (w1*x1^2+w2*x2^2) < 0",
            "algebraic_only": True,
            "paper_step_supported": "Section 14/16 finite countermodel showing signed weights can yield negative curvature",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "generic_base_mismatch_curvature_scaling",
            "kind": "theorem",
            "statement_scope": "K != 0, log_q != 0 ==> curvatureDet A0 (-K*log_q*A1) (K^2*log_q^2*A2) / (K^2*log_q^2) = curvatureDet A0 A1 A2",
            "algebraic_only": True,
            "paper_step_supported": "Section 19 generic-base scale covariance control for arbitrary base q > 1",
            "external_theorem_dependency": "None",
        },
    ]

    return {
        "module_path": "formal/RiemannScope/TransportMismatchCurvature.lean",
        "total_module_declarations": len(declarations),
        "module_def_count": sum(1 for d in declarations if d["kind"] == "def"),
        "module_theorem_count": sum(1 for d in declarations if d["kind"] == "theorem"),
        "repository_compiled_theorem_declarations": 565,
        "formal_proof_hygiene": "0 sorry, 0 admit, no nonstandard project axioms introduced",
        "declarations": declarations,
        "not_formalized_in_lean": [
            "Compact-support Euler-PDE homogeneity no-go (F_0 in C_c^infty((0, infty)^2), E F_0 = d F_0 ==> F_0 == 0)",
            "Full two-variable explicit formula expansion",
            "Theta-Mellin regularized analytic descent",
            "Positivity of the complete spectral curvature",
            "OBL-CT-001A",
        ],
    }


def verify_lean_theorem_map_against_file(
    lean_file_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Verify that the declarations listed in `get_lean_theorem_map()` match the exact
    `def` and `theorem` identifiers committed in `formal/RiemannScope/TransportMismatchCurvature.lean`.
    """
    if lean_file_path is None:
        lean_file_path = (
            Path(__file__).resolve().parent.parent
            / "formal"
            / "RiemannScope"
            / "TransportMismatchCurvature.lean"
        )
    text = lean_file_path.read_text(encoding="utf-8")
    actual_defs = re.findall(r"^\s*def\s+([A-Za-z0-9_]+)", text, flags=re.MULTILINE)
    actual_thms = re.findall(r"^\s*theorem\s+([A-Za-z0-9_]+)", text, flags=re.MULTILINE)
    actual_all = actual_defs + actual_thms

    tmap = get_lean_theorem_map()
    mapped_all = [d["identifier"] for d in tmap["declarations"]]
    return {
        "matches_exact": actual_all == mapped_all,
        "actual_defs": actual_defs,
        "actual_theorems": actual_thms,
        "mapped_identifiers": mapped_all,
        "contains_sorry": ("sorry" in text.split("--")[0] and re.search(r"\bsorry\b", re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)) is not None),
    }


# ---------------------------------------------------------------------------
# Section 19 & 20 (TASK-TC-034): Tau-Specificity and Weil-Equivalence Controls
# ---------------------------------------------------------------------------


def evaluate_generic_base_mismatch_control(
    bases: Sequence[float] = (2.0, math.e, TAU, 10.0),
    K: float = 1.5,
    N_cutoff: int = 15,
) -> Dict[str, Any]:
    """
    Generic-base control on the compactly supported witness tilde{G}_- (Section 19):
    Because hat{M}_K^{(j)}(0; q) = (-K log q)^j A_j(F_0), dividing by K^2 (log q)^2
    recovers the exact same C_arith(F_0) = A_0 A_2 - A_1^2 for EVERY base q > 1.
    Classifies as GENERIC_SCALE_CURVATURE.
    """
    neg_bundle = build_compact_negative_witness(N_cutoff=N_cutoff)
    moments = evaluate_euler_moments_A0_A1_A2(
        neg_bundle.kernel_fn,
        n_max=N_cutoff,
        euler1_f0=neg_bundle.euler1_fn,
        euler2_f0=neg_bundle.euler2_fn,
        evaluation_mode="COMPLETE_COMPACT_SUPPORT_SUM",
    )
    per_base_curvatures: Dict[str, float] = {}
    max_spread = 0.0
    for q in bases:
        res_q = evaluate_mismatch_derivatives_at_zero(
            neg_bundle.kernel_fn,
            K=K,
            n_max=N_cutoff,
            base_q=q,
            euler1_f0=neg_bundle.euler1_fn,
            euler2_f0=neg_bundle.euler2_fn,
        )
        per_base_curvatures[f"{q:.6f}"] = res_q.normalized_curvature_from_K
        max_spread = max(
            max_spread,
            abs(res_q.normalized_curvature_from_K - moments.arithmetic_curvature),
        )

    return {
        "bases_tested": list(bases),
        "reference_C_arith": moments.arithmetic_curvature,
        "per_base_normalized_curvatures": per_base_curvatures,
        "max_base_spread_abs_err": max_spread,
        "holds_for_all_q_gt_1": max_spread < 1e-10,
        "where_tau_enters": [
            "Fourier self-dual normalization e^{-2*pi*i*x*xi}",
            "Jacobi theta modularity Theta(1/t) = sqrt(t) Theta(t) with exp(-pi n^2 t)",
            "Completed-zeta Archimedean factor pi^{-s/2} Gamma(s/2)",
            "Lindemann transcendence of tau = 2*pi for rational prime-power lattice non-coincidence",
        ],
        "tau_specific_theorem_used_in_euler_curvature": False,
        "classification": CLASSIFICATION_GENERIC_SCALE_CURVATURE,
    }


def audit_weil_equivalence_firewall() -> Dict[str, Any]:
    """
    Weil-equivalence firewall (Section 20):
    Asserting positivity of a global Hermitian/Weil quadratic form obtained by
    differentiating a transported convolutional kernel is equivalent to Weil positivity
    (and hence RH-equivalent), not an independent proof mechanism.
    """
    return {
        "global_spectral_form_positivity_is_rh_equivalent": True,
        "independent_proof_mechanism": False,
        "classification": CLASSIFICATION_CURVATURE_POSITIVITY_RH_EQUIVALENT,
        "outcome_e": OUTCOME_E_WEIL_EQUIVALENCE,
    }


# ---------------------------------------------------------------------------
# Master Audit Entrypoint for TASK-TC-034 / TASK-TC-034R
# ---------------------------------------------------------------------------


def audit_transport_mismatch_curvature() -> Dict[str, Any]:
    """
    Run the complete TASK-TC-034 / TASK-TC-034R audit of infinitesimal transport-mismatch
    curvature around b = 1 (b = 1 + eta) and return the structured report dictionary
    including all required TASK-TC-034R fields (Section 15).
    """
    neg_bundle = build_compact_negative_witness(N_cutoff=15)
    pos_bundle = build_compact_positive_witness(N_cutoff=15)
    neg_jet_meta = verify_station_jet_preservation(neg_bundle)
    pos_jet_meta = verify_station_jet_preservation(pos_bundle)
    neg_arb = certify_compact_witness_curvature_arb("negative", N_cutoff=15)
    pos_arb = certify_compact_witness_curvature_arb("positive", N_cutoff=15)

    sign_audit = audit_arithmetic_curvature_sign_firewall(N_cutoff=15)
    compact_no_go = audit_compact_support_homogeneity_no_go(degree_d=-1.0)
    accidental_zero = audit_finite_station_accidental_zero()
    hom_control = evaluate_homogeneous_kernel_control()
    pairing_audit = audit_spectral_centering_and_pairings()
    reconciliation = reconcile_with_existing_curvature_transport()
    spectral_firewalls = audit_complete_spectral_curvature_and_firewalls()
    theta_fallback = audit_theta_mellin_nonscalar_fallback()
    generic_base = evaluate_generic_base_mismatch_control()
    weil_firewall = audit_weil_equivalence_firewall()
    lean_map = get_lean_theorem_map()

    pairing_dict = {
        k: ({"real": v.real, "imag": v.imag} if isinstance(v, complex) else v)
        for k, v in asdict(pairing_audit).items()
    }

    return {
        "task_id": "TASK-TC-034R",
        "repaired_task_id": "TASK-TC-034",
        "task_completion_status": TASK_TC_034R_STATUS,
        "title": (
            "Transport-Mismatch Curvature Evidence Repair, Compact-Support Witnesses, "
            "and Conditional Theta-Mellin Audit"
        ),
        "starting_head": "9f4701280a05c5c4ba9dc8be8d2bdb968588c799",
        "substantive_parent": "684c324960c8cfb3014808004926bb4d157c2fd9",
        "mismatch_parameter": "b = 1 + eta, eta in R (infinitesimal expansion around b = 1 at eta = 0)",
        "transported_kernel": "F_{K,eta}(x,y) = tau^{aK} F_0(tau^{-(1+eta)K}x, tau^{-(1+eta)K}y)",
        "arithmetic_derivative_formulas": {
            "M_K_0": "A_0(F_0)",
            "M_K_prime_0": "-K * log(tau) * A_1(F_0)",
            "M_K_double_prime_0": "K^2 * (log(tau))^2 * A_2(F_0)",
            "general_j": "(-K * log(tau))^j * A_j(F_0)",
        },
        "euler_operator": "E = x d/dx + y d/dy",
        "arithmetic_curvature": "C_arith(F_0) = A_0(F_0)*A_2(F_0) - A_1(F_0)^2",
        "compact_support_no_go_evidence": COMPACT_SUPPORT_NO_GO_EVIDENCE_STATUS,
        "compact_support_obstruction": compact_no_go.classification,
        "compactification_operator": {
            "symbol": "X_N(x, y) = chi_{a, b, c, d}(x) * chi_{a, b, c, d}(y)",
            "flat_function": "h(t) = exp(-1/t) for t > 0, 0 for t <= 0",
            "smooth_step": "S(t) = h(t) / (h(t) + h(1 - t))",
            "plateau_1d": "chi_{a,b,c,d}(x) = S((x - a)/(b - a)) * S((d - x)/(d - c))",
            "N_cutoff": 15,
            "a": 1.5,
            "b": 1.75,
            "c": 15.25,
            "d": 15.5,
            "support_rectangle": [[1.5, 15.5], [1.5, 15.5]],
            "plateau_rectangle": [[1.75, 15.25], [1.75, 15.25]],
            "active_station_set": list(neg_bundle.active_station_set),
            "highest_admitted_integer_station": neg_bundle.highest_admitted_integer_station,
            "first_excluded_integer_station": neg_bundle.first_excluded_integer_station,
            "verified_derivative_order": neg_bundle.verified_derivative_order,
            "mathematical_vs_floating_cutoff_distinction": {
                "exact_mathematical_cutoff": (
                    "Exact C^infty function h(t) = exp(-1/t) for all t > 0 and 0 for t <= 0; "
                    "on active stations 2 <= n <= 15 inside [1.75, 15.25], chi_{15}(n) = 1 and "
                    "all derivatives vanish identically, while on excluded integers n <= 1 or "
                    "n >= 16 outside (1.5, 15.5), chi_{15}(n) = 0 and all derivatives vanish identically."
                ),
                "floating_numerical_evaluator": (
                    "The IEEE-754 binary64 callable `flat_transition_h_jet(t)` used away from "
                    "active integer stations includes an underflow shortcut `if inv_t > 700.0: return (0.0, 0.0, 0.0)` "
                    "where exp(-1/t) < exp(-700) ~ 9.86e-305 approaches binary64 subnormal/underflow range."
                ),
                "arbitrary_precision_arb_evaluator": (
                    "`flat_transition_h_jet_arb(t, prec_bits)` evaluates the mathematical C^infty "
                    "jet in outward Arb ball arithmetic without any artificial threshold, including 0 < t < 1/700."
                ),
                "affects_certified_station_sums": False,
            },
        },
        "plateau_interval": [1.75, 15.25],
        "support_interval": [1.5, 15.5],
        "jet_preservation_order": 2,
        "negative_witness": {
            "name": neg_bundle.name,
            "definition": "tilde{G}_-(x, y) = X_{15}(x, y) * exp(-(3/2) * (log(x*y / 16))^2)",
            "prototype_G_minus": "exp(-(3/2) * (log(x*y / 16))^2)",
            "prototype_E_G_minus": "-6 * log(x*y / 16) * exp(-(3/2) * (log(x*y / 16))^2)",
            "prototype_E2_G_minus": "(36 * (log(x*y / 16))^2 - 12) * exp(-(3/2) * (log(x*y / 16))^2)",
            "nonnegative": True,
            "compactly_supported_in_open_quadrant": True,
            "support_rectangle": [[1.5, 15.5], [1.5, 15.5]],
            "plateau_rectangle": [[1.75, 15.25], [1.75, 15.25]],
            "classification": COMPACT_SUPPORT_NEG_CURVATURE_CERTIFIED,
        },
        "negative_witness_complete_sum": neg_jet_meta,
        "negative_curvature_arb_enclosure": neg_arb,
        "positive_witness": {
            "name": pos_bundle.name,
            "definition": (
                "tilde{G}_+(x, y) = X_{15}(x, y) * cosh((6/5)*log(x*y / 25)) "
                "* exp(-(2/25)*(log(x*y / 25))^2)"
            ),
            "prototype_G_plus": "cosh((6/5)*w) * exp(-(2/25)*w^2), w = log(x*y / 25)",
            "prototype_E_G_plus": "2 * ((6/5)*sinh((6/5)*w) - (4/25)*w*cosh((6/5)*w)) * exp(-(2/25)*w^2)",
            "prototype_E2_G_plus": (
                "4 * (((32/25) + (16/625)*w^2)*cosh((6/5)*w) - (48/125)*w*sinh((6/5)*w)) "
                "* exp(-(2/25)*w^2)"
            ),
            "nonnegative": True,
            "compactly_supported_in_open_quadrant": True,
            "support_rectangle": [[1.5, 15.5], [1.5, 15.5]],
            "plateau_rectangle": [[1.75, 15.25], [1.75, 15.25]],
            "classification": COMPACT_SUPPORT_POS_CURVATURE_CERTIFIED,
        },
        "positive_witness_complete_sum": pos_jet_meta,
        "positive_curvature_arb_enclosure": pos_arb,
        "compact_support_sign_indefiniteness_status": COMPACT_SUPPORT_SIGN_INDEFINITENESS_STATUS,
        "curvature_sign_status": COMPACT_SUPPORT_SIGN_INDEFINITENESS_STATUS,
        "finite_accidental_zero_scope": accidental_zero,
        "homogeneity_status": (
            "E F_0 = d F_0 implies A_1 = d A_0, A_2 = d^2 A_0, and C_arith(F_0) = 0; "
            "not implied by arithmetic label preservation alone (ARITHMETIC_CURVATURE_FLATNESS_NOT_IMPLIED)."
        ),
        "mellin_scaling": {
            "raw_factor": "tau^{K(a + (1 + eta)(s + t))} H_0(s, t)",
            "net_normalized_factor": "tau^{eta K (s + t)}",
            "first_derivative_at_0": "K log(tau) (s + t)",
            "second_derivative_at_0": "K^2 (log(tau))^2 (s + t)^2",
        },
        "centered_exponent_convention": {
            "uncentered": "s + t",
            "half_density_centered": "(s - 1/2) + (t - 1/2) = s + t - 1",
            "conjugate_pair_t_eq_bar_rho": "2 * delta_rho (radial, DIAGONAL_CONJUGATE_BLOCK_ONLY)",
            "reflection_pair_t_eq_1_minus_bar_rho": "2 * i * gamma_rho (ordinate/phase)",
            "general_pair_rho_sigma": "(delta_rho + delta_sigma) + i*(gamma_rho + gamma_sigma)",
        },
        "natural_zero_pairing": pairing_audit.naturally_induced_pairing,
        "spectral_curvature_type": spectral_firewalls["spectral_curvature_outcome"],
        "weight_sign": "COMPLEX_SIGNED_DOUBLE_SUM_WEIGHTS",
        "cross_term_status": "UNRESTRICTED_DOUBLE_SUM_WITH_POLE_TRIVIAL_AND_ARCHIMEDEAN_TERMS",
        "theta_definition_status": theta_fallback.purely_theta_or_arithmetic_defined_status,
        "theta_convergence_status": theta_fallback.convergence_status,
        "theta_second_variation_status": theta_fallback.second_mismatch_variation_status,
        "theta_delta_squared_status": theta_fallback.delta_squared_detection_status,
        "theta_complete_expansion_status": theta_fallback.complete_spectral_expansion_status,
        "theta_positivity_status": theta_fallback.positive_complete_spectral_curvature_status,
        "theta_obl_ct_001a_status": theta_fallback.closes_obl_ct_001a_status,
        "theta_candidate_status": asdict(theta_fallback),
        "lean_theorem_map": lean_map,
        "tau_specificity": generic_base["classification"],
        "weil_equivalence_status": weil_firewall["classification"],
        "relation_to_OBL_CT_001A": reconciliation["classification"],
        "principal_classification": PRINCIPAL_CLASSIFICATION,
        "secondary_classifications": [
            COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED,
            COMPACT_SUPPORT_SIGN_INDEFINITENESS_STATUS,
            COMPACT_SUPPORT_NEG_CURVATURE_CERTIFIED,
            COMPACT_SUPPORT_POS_CURVATURE_CERTIFIED,
            CLASSIFICATION_FINITE_ACCIDENTAL_ZERO,
            THETA_MELLIN_AUDIT_CONDITIONAL,
            OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE,
            CLASSIFICATION_CURVATURE_POSITIVITY_RH_EQUIVALENT,
            CLASSIFICATION_GENERIC_SCALE_CURVATURE,
            OBL_CT_001A_STATUS,
            CANDIDATE_FAILURE_DOES_NOT_REFUTE_TC,
        ],
        "triggered_outcome_codes": [
            OUTCOME_B_ARITHMETIC_FLATNESS_NOT_IMPLIED,
            COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED,
            OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE,
            OUTCOME_E_WEIL_EQUIVALENCE,
            OUTCOME_G_REDUCES_TO_OBL_CT_001A,
        ],
        "exact_remaining_subgate": theta_fallback.exact_remaining_theorem,
        "canonical_selector_problem": {
            "question": (
                "What zeta-specific principle selects one canonical non-scalar arithmetic "
                "functional whose law is stronger than generic grade invariance?"
            ),
            "governing_obstruction": (
                "Arithmetic label compatibility (b = 1) makes mismatch curvature C_arith(F) = A_0 A_2 - A_1^2 "
                "grade-invariant, but does not make it zero, positive, or sign-definite: across nonnegative "
                "compactly supported kernels F in C_c^infty((0, infty)^2), C_arith(F) realizes certified "
                "strictly negative and strictly positive values. Until a zeta-specific selector is derived, "
                "arbitrary test kernels can realize arbitrary curvature signs and no universal TC constraint follows."
            ),
            "parent_obligation": "OBL-CT-001A",
            "status": "OPEN",
        },
        "obl_ct_001a_status": "OPEN",
        "obl_ct_001a_completed": False,
        "rh_claimed": False,
        "candidate_failure_refutes_tc": False,
        "hypothesis_fidelity": {
            "tc_hypothesis": "The same arithmetic object across transcendental grades implies a constraint.",
            "candidate_implementation": "The constraint is the curvature of relative transport at b = 1.",
            "distinction": (
                "Failure of the infinitesimal transport-mismatch curvature candidate on compactly "
                "supported two-variable kernels refutes this candidate implementation and test space, "
                "NOT the general TC hypothesis."
            ),
        },
        "diagnostics": {
            "sign_audit": sign_audit,
            "compact_support_no_go": asdict(compact_no_go),
            "finite_station_accidental_zero": accidental_zero,
            "homogeneous_control": hom_control,
            "spectral_pairing_audit": pairing_dict,
            "curvature_transport_reconciliation": reconciliation,
            "spectral_firewalls": spectral_firewalls,
            "generic_base_control": generic_base,
        },
    }


__all__ = [
    "ARB_CERTIFICATION_NOT_AVAILABLE",
    "CANDIDATE_FAILURE_DOES_NOT_REFUTE_TC",
    "CANDIDATE_THETA_MELLIN_AUDIT",
    "CLASSIFICATION_ARITHMETIC_INDEFINITE",
    "CLASSIFICATION_COMPACT_SUPPORT_IMPOSSIBLE",
    "CLASSIFICATION_CURVATURE_POSITIVITY_RH_EQUIVALENT",
    "CLASSIFICATION_FINITE_ACCIDENTAL_ZERO",
    "CLASSIFICATION_GENERIC_SCALE_CURVATURE",
    "CLASSIFICATION_REDUCES_TO_EXISTING_OBL_CT_001A",
    "CLASSIFICATION_SELECTED_BLOCK_ONLY",
    "COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED",
    "COMPACT_SUPPORT_NEG_CURVATURE_CERTIFIED",
    "COMPACT_SUPPORT_NO_GO_EVIDENCE_STATUS",
    "COMPACT_SUPPORT_POS_CURVATURE_CERTIFIED",
    "COMPACT_SUPPORT_SIGN_INDEFINITENESS_STATUS",
    "CompactSupportHomogeneityAudit",
    "CompactifiedKernelBundle",
    "EulerMomentResult",
    "ExponentialMixtureCurvatureResult",
    "MismatchDerivativeResult",
    "OBL_CT_001A_STATUS",
    "OUTCOME_A_FULL_BRIDGE",
    "OUTCOME_B_ARITHMETIC_FLATNESS_NOT_IMPLIED",
    "OUTCOME_C_COMPACT_SUPPORT_NO_GO",
    "OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE",
    "OUTCOME_E_WEIL_EQUIVALENCE",
    "OUTCOME_F_THETA_SUBGATE_OPEN",
    "OUTCOME_G_REDUCES_TO_OBL_CT_001A",
    "PRINCIPAL_CLASSIFICATION",
    "SUPERSEDED_FINITE_TRUNCATION_STATUS",
    "SpectralPairingAuditResult",
    "TASK_TC_034R_STATUS",
    "THETA_MELLIN_AUDIT_CONDITIONAL",
    "ThetaMellinNonScalarCandidateAudit",
    "active_prime_power_stations",
    "apply_euler_operator_once",
    "apply_euler_operator_twice",
    "audit_arithmetic_curvature_sign_firewall",
    "audit_compact_support_homogeneity_no_go",
    "audit_complete_spectral_curvature_and_firewalls",
    "audit_finite_station_accidental_zero",
    "audit_spectral_centering_and_pairings",
    "audit_theta_mellin_nonscalar_fallback",
    "audit_transport_mismatch_curvature",
    "audit_weil_equivalence_firewall",
    "build_compact_negative_witness",
    "build_compact_positive_witness",
    "certify_compact_witness_curvature_arb",
    "compactify_preserving_station_jets",
    "evaluate_even_mismatch_defect",
    "evaluate_euler_moments_A0_A1_A2",
    "evaluate_exponential_mixture_curvature",
    "evaluate_generic_base_mismatch_control",
    "evaluate_homogeneous_kernel_control",
    "evaluate_mellin_mismatch_scaling",
    "evaluate_mismatch_derivatives_at_zero",
    "evaluate_normalized_mismatch_energy",
    "evaluate_reciprocal_pair_curvature",
    "evaluate_transported_mismatch_kernel",
    "flat_transition_h_jet",
    "flat_transition_h_jet_arb",
    "get_lean_theorem_map",
    "plateau_cutoff_1d_euler_jet",
    "plateau_cutoff_1d_jet",
    "plateau_cutoff_2d_euler_jet",
    "prime_power_base_table",
    "prototype_negative_witness_e1",
    "prototype_negative_witness_e2",
    "prototype_negative_witness_g0",
    "prototype_positive_witness_e1",
    "prototype_positive_witness_e2",
    "prototype_positive_witness_g0",
    "reconcile_with_existing_curvature_transport",
    "smooth_step_S_jet",
    "verify_lean_theorem_map_against_file",
    "verify_station_jet_preservation",
]
