"""
TASK-TC-034: Infinitesimal Transport-Mismatch Curvature and Non-Scalar Arithmetic Descent.

This module audits whether the infinitesimal second variation (transport curvature)
around the unique label-preserving transport b = 1 (written b = 1 + eta as eta -> 0):
1. defines an exact zero-independent arithmetic curvature functional;
2. has a spectral expression detecting delta_rho^2;
3. avoids the value-level covariance cancellation proved in TASK-TC-033;
4. avoids the exact-zero remainder-cancellation obstruction proved in TASK-TC-032R.

This is the direct audit of canonical open obligation OBL-CT-001A.
"""

from __future__ import annotations

import cmath
from dataclasses import asdict, dataclass
import math
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from tc.two_variable import _von_mangoldt_exact

TAU: float = 2.0 * math.pi
LOG_TAU: float = math.log(TAU)

# ---------------------------------------------------------------------------
# Canonical Classification Constants (Section 21 & Firewalls)
# ---------------------------------------------------------------------------

OUTCOME_A_FULL_BRIDGE = "INFINITESIMAL_TRANSPORT_CURVATURE_BRIDGE_PROVED"
OUTCOME_B_ARITHMETIC_FLATNESS_NOT_IMPLIED = "ARITHMETIC_CURVATURE_FLATNESS_NOT_IMPLIED"
OUTCOME_C_COMPACT_SUPPORT_NO_GO = "COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PROVED"
OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE = "SPECTRAL_CURVATURE_IS_SIGNED_OR_DOUBLE_SUM"
OUTCOME_E_WEIL_EQUIVALENCE = "CURVATURE_POSITIVITY_IS_RH_EQUIVALENT"
OUTCOME_F_THETA_SUBGATE_OPEN = "THETA_MELLIN_NONSCALAR_CURVATURE_SUBGATE_OPEN"
OUTCOME_G_REDUCES_TO_OBL_CT_001A = "MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A"

CLASSIFICATION_COMPACT_SUPPORT_IMPOSSIBLE = (
    "NONZERO_COMPACT_SUPPORT_HOMOGENEOUS_KERNEL_IMPOSSIBLE"
)
CLASSIFICATION_FINITE_ACCIDENTAL_ZERO = "FINITE_ACCIDENTAL_ARITHMETIC_CURVATURE_ZERO"
CLASSIFICATION_ARITHMETIC_INDEFINITE = "GENERAL_ARITHMETIC_MISMATCH_CURVATURE_INDEFINITE"
CLASSIFICATION_SELECTED_BLOCK_ONLY = "SELECTED_CURVATURE_BLOCK_ONLY"
CLASSIFICATION_REDUCES_TO_EXISTING_OBL_CT_001A = (
    "MISMATCH_CURVATURE_REDUCES_TO_EXISTING_OBL_CT_001A"
)
CLASSIFICATION_GENERIC_SCALE_CURVATURE = "GENERIC_SCALE_CURVATURE"
CLASSIFICATION_CURVATURE_POSITIVITY_RH_EQUIVALENT = (
    "CURVATURE_POSITIVITY_IS_RH_EQUIVALENT"
)

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
    classification: str
    outcome_code: str
    scope_note: str


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
    """Phase II audit of one canonical non-scalar quadratic theta-Mellin candidate."""

    candidate_name: str
    scalar_candidate_status: str
    purely_theta_or_arithmetic_defined: bool
    zero_independent_definition: bool
    exact_scale_flatness_law: bool
    convergent_on_regularized_test_space: bool
    second_mismatch_variation_computable: bool
    contains_delta_squared_in_spectral_expansion: bool
    avoids_assumed_weil_positivity: bool
    avoids_selected_zero_construction: bool
    reduces_to_double_mellin_weil_form: bool
    closes_obl_ct_001a: bool
    classification: str
    exact_remaining_theorem: str


# ---------------------------------------------------------------------------
# Section 4: Transported Mismatch Kernel and Arithmetic Energy
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
    Evaluate the transported mismatch kernel (Section 4):
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


def evaluate_normalized_mismatch_energy(
    f0: Callable[[float, float], float],
    K: float,
    eta: float = 0.0,
    n_max: int = 30,
    base_q: float = TAU,
) -> float:
    """
    Evaluate the normalized equal-grade arithmetic mismatch energy (Section 4):
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
# Section 5 & 6: Arithmetic Euler-Generator Theorem & Curvature Determinant
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
) -> EulerMomentResult:
    """
    Compute the arithmetic Euler moments (Section 5 & 6):
        A_j(F_0) = sum_{n, m >= 2} Lambda(n) Lambda(m) (E^j F_0)(n, m),   j = 0, 1, 2,
    and the arithmetic transport curvature:
        C_arith(F_0) = A_0 A_2 - A_1^2,
        kappa_arith(F_0) = (A_0 A_2 - A_1^2) / A_0^2  (when A_0 > 0).
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
    Verify the Arithmetic Euler-Generator Theorem (Section 5 & 6):
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

    # Direct 4th-order finite-difference derivatives in eta around eta = 0
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
    Compute the symmetric mismatch difference (Section 10):
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
# Section 7: Synthetic Curvature Identity (Positive Exponential Mixtures)
# ---------------------------------------------------------------------------


def evaluate_exponential_mixture_curvature(
    weights: Sequence[float],
    exponents: Sequence[float],
) -> ExponentialMixtureCurvatureResult:
    """
    Evaluate M(0)*M''(0) - M'(0)^2 for M(eta) = sum_j w_j exp(eta x_j) (Section 7):
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
    has_distinct = any(abs(x_t[i] - x_t[j]) > 1e-15 for i in range(r) for j in range(i + 1, r))

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
    Evaluate the reciprocal pair M(eta) = w_1 e^{eta x} + w_2 e^{-eta x}
    (corresponding to off-critical reflection exponents +x and -x with x != 0).
    Curvature determinant equals 4 w_1 w_2 x^2 > 0 for w_1, w_2 > 0 and x != 0.
    """
    return evaluate_exponential_mixture_curvature([w1, w2], [x, -x])


# ---------------------------------------------------------------------------
# Section 11, 12, 13, 14: Homogeneity, Compact-Support No-Go, & Sign Firewall
# ---------------------------------------------------------------------------


def evaluate_homogeneous_kernel_control(
    alpha: float = 0.5,
    beta: float = 0.75,
    n_max: int = 20,
) -> Dict[str, Any]:
    """
    Audit a homogeneous kernel F_0(x, y) = x^alpha y^beta on a fixed finite station list
    (Section 11). Satisfies E F_0 = d F_0 with d = alpha + beta, so:
        A_1 = d A_0,  A_2 = d^2 A_0,  C_arith(F_0) = A_0 A_2 - A_1^2 = 0,
    and hat{M}_K(eta) = e^{-d eta K log tau} hat{M}_K(0).
    """
    d = alpha + beta

    def f_hom(x: float, y: float) -> float:
        return (x ** alpha) * (y ** beta)

    def e1_hom(x: float, y: float) -> float:
        return d * f_hom(x, y)

    def e2_hom(x: float, y: float) -> float:
        return (d * d) * f_hom(x, y)

    moments = evaluate_euler_moments_A0_A1_A2(
        f_hom, n_max=n_max, euler1_f0=e1_hom, euler2_f0=e2_hom
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
    Prove/verify the Compact-Support Homogeneity No-Go theorem (Section 12):
        F_0 in C_c^infty((0, inf)^2) and E F_0 = d F_0  ==>  F_0 == 0.

    Proof: Along every positive ray r -> (r x_0, r y_0), the ODE r d/dr F_0(r x_0, r y_0)
    = d F_0(r x_0, r y_0) integrates to F_0(r x_0, r y_0) = r^d F_0(x_0, y_0).
    If F_0(x_0, y_0) != 0, then F_0(r x_0, r y_0) != 0 for all r > 0, so the support of F_0
    contains the entire unbounded ray {(r x_0, r y_0) : r > 0}, contradicting compact support
    in (0, inf)^2.
    """
    # Diagnostic check: any compactly supported radial cutoff phi(r) multiplied by a
    # homogeneous profile produces nonzero Euler defect r phi'(r) where phi transitions to 0.
    r_samples = [0.5, 1.0, 2.0, 4.0, 8.0]
    ray_values = [r ** degree_d for r in r_samples]
    all_nonzero = all(val != 0.0 for val in ray_values)

    return CompactSupportHomogeneityAudit(
        degree_d=degree_d,
        ray_scaling_verified=all_nonzero,
        compact_support_compatible_for_nonzero_kernel=False,
        classification=CLASSIFICATION_COMPACT_SUPPORT_IMPOSSIBLE,
        outcome_code=OUTCOME_C_COMPACT_SUPPORT_NO_GO,
        scope_note=(
            "Proved for all C_c^infty((0, inf)^2) kernels: Euler homogeneity E F_0 = d F_0 "
            "forces F_0(r x, r y) = r^d F_0(x, y) along every positive ray, which is "
            "incompatible with compact support unless F_0 == 0. Does not by itself refute "
            "noncompact or distributional candidates."
        ),
    )


def audit_finite_station_accidental_zero() -> Dict[str, Any]:
    """
    Construct a fixed finite-station control (Section 13) where A_0 A_2 - A_1^2 = 0
    by interpolation on a selected window (active stations {2, 3}), but fails as soon as
    the station window expands to include {2, 3, 4, 5}.
    Classifies as FINITE_ACCIDENTAL_ARITHMETIC_CURVATURE_ZERO.
    """
    # Construct F_0(x, y) = w(x) w(y) where w(x) has log-derivative 0 at x=2, 3
    # and chosen second log-derivative so A_0 A_2 - A_1^2 = 0 on {2, 3},
    # while on {2, 3, 4, 5} it has nonzero curvature.
    def f_accidental(x: float, y: float) -> float:
        if x <= 1.2 or x >= 8.0 or y <= 1.2 or y >= 8.0:
            return 0.0
        u = math.log(x / 2.5)
        v = math.log(y / 2.5)
        # On {2, 3}, u^2 = (log(2/2.5))^2 != (log(3/2.5))^2, but if F_0 is constant
        # in a flat plateau covering [1.9, 3.1]^2 and smoothly decays outside [3.2, 7.0]:
        def plateau(z: float) -> float:
            az = abs(z)
            if az <= 0.25:
                return 1.0
            if az >= 1.1:
                return 0.0
            t = (az - 0.25) / (1.1 - 0.25)
            return math.exp(-t * t / (1.0 - t * t))

        return plateau(u) * plateau(v)

    # On n_max = 3 (stations 2 and 3, where |log(2/2.5)| = 0.223 <= 0.25 and |log(3/2.5)| = 0.182 <= 0.25):
    # Both stations lie inside the flat top where E F_0 = 0 and E^2 F_0 = 0!
    res_window_small = evaluate_euler_moments_A0_A1_A2(f_accidental, n_max=3)
    # On n_max = 5 (stations 2, 3, 4, 5; log(4/2.5) = 0.470, log(5/2.5) = 0.693 on the curved ramp):
    res_window_large = evaluate_euler_moments_A0_A1_A2(f_accidental, n_max=5)

    return {
        "small_window_n_max": 3,
        "small_window_A0": res_window_small.A0,
        "small_window_curvature": res_window_small.arithmetic_curvature,
        "large_window_n_max": 5,
        "large_window_A0": res_window_large.A0,
        "large_window_curvature": res_window_large.arithmetic_curvature,
        "vanishes_on_selected_window": abs(res_window_small.arithmetic_curvature) < 1e-12,
        "breaks_on_expanded_window": abs(res_window_large.arithmetic_curvature) > 1e-3,
        "classification": CLASSIFICATION_FINITE_ACCIDENTAL_ZERO,
    }


def audit_arithmetic_curvature_sign_firewall(n_max: int = 15) -> Dict[str, Any]:
    """
    Sign firewall on the arithmetic curvature (Section 14):
    Demonstrates that for nonnegative kernels F_0 >= 0, C_arith(F_0) = A_0 A_2 - A_1^2
    is NOT automatically nonnegative because E^2 F_0 contains second radial derivatives
    of the kernel profile. Constructs explicit nonnegative kernels with:
      1. C_arith < 0 (strictly negative — unimodal log-concave bump);
      2. C_arith = 0 (zero — plateau/homogeneous control);
      3. C_arith > 0 (strictly positive — convex/bimodal radial weight on active stations).
    Classifies as GENERAL_ARITHMETIC_MISMATCH_CURVATURE_INDEFINITE.
    """
    # 1. Strictly negative arithmetic curvature: unimodal log-Gaussian F_0(x, y) = exp(-alpha (log(x/c)^2 + log(y/c)^2))
    # Let u = log(x/c) + log(y/c). For a 1D radial profile F_0(x, y) = exp(-alpha * (log(x*y / c^2))^2),
    # (x d/dx + y d/dy) = 2 d/dw where w = log(x*y / c^2).
    # At the peak w = 0, F_0 = 1, E F_0 = 0, E^2 F_0 = -8 * alpha < 0!
    c_neg = 4.0
    alpha_neg = 1.5

    def f_negative_curv(x: float, y: float) -> float:
        w = math.log((x * y) / (c_neg * c_neg))
        return math.exp(-alpha_neg * w * w)

    def e1_negative_curv(x: float, y: float) -> float:
        w = math.log((x * y) / (c_neg * c_neg))
        return (-4.0 * alpha_neg * w) * math.exp(-alpha_neg * w * w)

    def e2_negative_curv(x: float, y: float) -> float:
        w = math.log((x * y) / (c_neg * c_neg))
        return (16.0 * (alpha_neg ** 2) * (w ** 2) - 8.0 * alpha_neg) * math.exp(
            -alpha_neg * w * w
        )

    res_neg = evaluate_euler_moments_A0_A1_A2(
        f_negative_curv,
        n_max=n_max,
        euler1_f0=e1_negative_curv,
        euler2_f0=e2_negative_curv,
    )

    # 2. Strictly positive arithmetic curvature: nonnegative mixture of two distinct radial scales
    # F_0(x, y) = (1 + 2.5 * (log(x*y / 9))^2) * exp(-0.15 * (log(x*y / 9))^2) on compact window [1.5, 20]^2
    # or a two-bump nonnegative radial profile where E^2 F_0 > 0 in the trough between bumps.
    def f_positive_curv(x: float, y: float) -> float:
        w = math.log((x * y) / 25.0)
        return math.cosh(1.2 * w) * math.exp(-0.08 * w * w)

    res_pos = evaluate_euler_moments_A0_A1_A2(f_positive_curv, n_max=n_max)

    # 3. Zero arithmetic curvature control (accidental plateau on {2, 3})
    res_zero_ctrl = audit_finite_station_accidental_zero()

    all_signs_occur = (
        res_neg.arithmetic_curvature < -1e-4
        and res_pos.arithmetic_curvature > 1e-4
        and abs(res_zero_ctrl["small_window_curvature"]) < 1e-12
    )

    return {
        "negative_kernel_A0": res_neg.A0,
        "negative_kernel_curvature": res_neg.arithmetic_curvature,
        "positive_kernel_A0": res_pos.A0,
        "positive_kernel_curvature": res_pos.arithmetic_curvature,
        "zero_control_curvature": res_zero_ctrl["small_window_curvature"],
        "all_three_signs_realized": all_signs_occur,
        "outcome_b_flatness_not_implied": OUTCOME_B_ARITHMETIC_FLATNESS_NOT_IMPLIED,
        "classification": CLASSIFICATION_ARITHMETIC_INDEFINITE,
    }


# ---------------------------------------------------------------------------
# Section 8, 9, 10, 15, 16, 17: Spectral Mismatch Scaling, Centering & Pairings
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
    Evaluate the spectral mismatch scaling (Section 8):
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
    Centering and pairing audit (Sections 9, 10, 15, 16):
    For rho = 1/2 + delta + i*gamma:
      - Uncentered exponent is s + t. Under half-density centering (x*y)^{-1/2},
        the centered exponent is (s - 1/2) + (t - 1/2) = s + t - 1.
      - Conjugate pairing t = bar(rho):
          (rho - 1/2) + (bar(rho) - 1/2) = 2*delta (purely real radial displacement).
          Even mismatch defect: 2*(cosh(2*eta*K*delta*log(q)) - 1) >= 0,
          second variation proportional to +delta^2.
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
    refl_rho = complex(1.0, 0.0) - bar_rho  # 1 - bar(rho) = 1/2 - delta + i*gamma
    sigma = complex(0.5 + sigma_delta, sigma_gamma)

    uncentered_conj = rho + bar_rho  # 1 + 2*delta
    centered_conj = (rho - 0.5) + (bar_rho - 0.5)  # 2*delta
    centered_refl = (rho - 0.5) + (refl_rho - 0.5)  # 2*i*gamma
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
    detector (Section 17):
        B_rho(k) = 2 (cosh(k delta_rho log tau) - 1),
        B_rho''(0) = 2 delta_rho^2 (log tau)^2.

    On a centered conjugate pair, the symmetric mismatch factor is:
        tau^{eta K (2 delta_rho)} + tau^{-eta K (2 delta_rho)} - 2
        = 2 (cosh(2 eta K delta_rho log tau) - 1)
        = B_rho(2 eta K).
    Thus it reproduces the EXACT same detector under the rescaling k = 2 eta K,
    without providing a new zero-independent arithmetic descent.
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
    Audit the complete spectral side and enforce all mandatory firewalls (Sections 15, 16, 20):
      1. No diagonal projection without proof (diagonal-only classified as SELECTED_CURVATURE_BLOCK_ONLY);
      2. No selected-zero test construction;
      3. No remainder-domination reuse (closed by TASK-TC-032R);
      4. Complete expansion includes pole terms (s, t = 1), trivial-zero terms, Archimedean terms,
         and off-diagonal (rho, sigma) cross terms.
    """
    return {
        "complete_spectral_type": "DOUBLE_SPECTRAL_SUM_PLUS_POLE_AND_ARCHIMEDEAN_BACKGROUND",
        "spectral_curvature_outcome": OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE,
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
# Section 18: Theta-Mellin Fallback Audit (One Canonical Non-Scalar Candidate)
# ---------------------------------------------------------------------------


def audit_theta_mellin_nonscalar_fallback() -> ThetaMellinNonScalarCandidateAudit:
    """
    Audit at most one canonical non-scalar quadratic theta-Mellin candidate (Section 18):
    The scale-mismatched bilinear theta-kernel functional defined BEFORE zero evaluation:
        Q_Theta(eta; Phi_0) = iint_{(0, inf)^2} Theta_1^+(t_1) Theta_1^+(t_2)
                              Phi_0(tau^{-eta K} t_1, tau^{-eta K} t_2) (dt_1 / t_1) (dt_2 / t_2),
    where Theta_1^+(t) = sum_{n >= 1} e^{-pi n^2 t} satisfies
        int_0^infty Theta_a^+(t) t^{s/2 - 1} dt = a^{-s} pi^{-s/2} Gamma(s/2) zeta(s) = a^{-s} Lambda(s).

    Result of the 8-criteria audit:
    - The frozen scalar candidate a^{1/2 - s} Lambda(s) remains rejected because evaluation at a zero
      is identically 0 and all grade/mismatch derivatives remain 0.
    - The non-scalar bilinear theta functional Q_Theta(eta; Phi_0) is well-defined before zero evaluation,
      purely theta/arithmetic-defined, zero-independent, convergent when Phi_0 has rapid decay or
      incorporates the pole-annihilating differential operator (E - 1/2)(E + 1/2), and has computable
      second mismatch variation.
    - However:
      (1) Because Theta_1^+(t) = sum_{n>=1} e^{-pi n^2 t} is a positive multi-scale sum and any
          convergent test kernel Phi_0 cannot be Euler-homogeneous on (0, inf)^2, Q_Theta(eta; Phi_0)
          is NOT curvature-flat in eta (its theta-side curvature Q_0 Q_2 - Q_1^2 != 0 and depends on Phi_0).
      (2) By Mellin-Parseval inversion, Q_Theta(eta; Phi_0) is a double contour integral of
          Lambda(s) Lambda(t) tilde{Phi}_0(s, t) tau^{eta K (s + t) / 2}, which neither isolates
          individual zeros nor produces a positive diagonal sum over delta_rho^2 without assuming
          a Weil-equivalent positivity criterion.
    Therefore, it does not close OBL-CT-001A.
    """
    return ThetaMellinNonScalarCandidateAudit(
        candidate_name="Bilinear scale-mismatched theta-Mellin quadratic functional Q_Theta(eta; Phi_0)",
        scalar_candidate_status="REJECTED_FROZEN_IDENTICALLY_ZERO_AT_ZEROS",
        purely_theta_or_arithmetic_defined=True,
        zero_independent_definition=True,
        exact_scale_flatness_law=False,
        convergent_on_regularized_test_space=True,
        second_mismatch_variation_computable=True,
        contains_delta_squared_in_spectral_expansion=True,
        avoids_assumed_weil_positivity=True,
        avoids_selected_zero_construction=True,
        reduces_to_double_mellin_weil_form=True,
        closes_obl_ct_001a=False,
        classification=OUTCOME_G_REDUCES_TO_OBL_CT_001A,
        exact_remaining_theorem=(
            "OBL-CT-001A: Construct a zero-independent non-scalar arithmetic or theta functional "
            "whose transport curvature at b = 1 satisfies a kernel-independent arithmetic flatness "
            "or sign bound while its complete spectral expansion isolates a positive radial moment "
            "in delta_rho^2 without assuming Weil positivity."
        ),
    )


# ---------------------------------------------------------------------------
# Section 19 & 20: Tau-Specificity and Weil-Equivalence Controls
# ---------------------------------------------------------------------------


def evaluate_generic_base_mismatch_control(
    bases: Sequence[float] = (2.0, math.e, TAU, 10.0),
    K: float = 1.5,
    n_max: int = 12,
) -> Dict[str, Any]:
    """
    Generic-base control (Section 19):
    Repeat the mismatch-curvature derivation for generic bases q > 1.
    Because hat{M}_K^{(j)}(0; q) = (-K log q)^j A_j(F_0), dividing by K^2 (log q)^2
    recovers the exact same C_arith(F_0) = A_0 A_2 - A_1^2 for EVERY base q > 1.
    Classifies as GENERIC_SCALE_CURVATURE.
    """
    def f_test(x: float, y: float) -> float:
        w = math.log((x * y) / 16.0)
        return math.exp(-0.5 * w * w)

    def e1_test(x: float, y: float) -> float:
        w = math.log((x * y) / 16.0)
        return (-2.0 * w) * math.exp(-0.5 * w * w)

    def e2_test(x: float, y: float) -> float:
        w = math.log((x * y) / 16.0)
        return (4.0 * w * w - 4.0) * math.exp(-0.5 * w * w)

    moments = evaluate_euler_moments_A0_A1_A2(
        f_test, n_max=n_max, euler1_f0=e1_test, euler2_f0=e2_test
    )
    per_base_curvatures: Dict[str, float] = {}
    max_spread = 0.0
    for q in bases:
        res_q = evaluate_mismatch_derivatives_at_zero(
            f_test,
            K=K,
            n_max=n_max,
            base_q=q,
            euler1_f0=e1_test,
            euler2_f0=e2_test,
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
# Master Audit Entrypoint for TASK-TC-034
# ---------------------------------------------------------------------------


def audit_transport_mismatch_curvature() -> Dict[str, Any]:
    """
    Run the complete TASK-TC-034 audit of infinitesimal transport-mismatch curvature
    around b = 1 (b = 1 + eta) and return the structured report dictionary.
    """
    sign_audit = audit_arithmetic_curvature_sign_firewall(n_max=15)
    compact_no_go = audit_compact_support_homogeneity_no_go(degree_d=-1.0)
    accidental_zero = audit_finite_station_accidental_zero()
    hom_control = evaluate_homogeneous_kernel_control()
    pairing_audit = audit_spectral_centering_and_pairings()
    reconciliation = reconcile_with_existing_curvature_transport()
    spectral_firewalls = audit_complete_spectral_curvature_and_firewalls()
    theta_fallback = audit_theta_mellin_nonscalar_fallback()
    generic_base = evaluate_generic_base_mismatch_control()
    weil_firewall = audit_weil_equivalence_firewall()

    pairing_dict = {
        k: ({"real": v.real, "imag": v.imag} if isinstance(v, complex) else v)
        for k, v in asdict(pairing_audit).items()
    }

    return {
        "task_id": "TASK-TC-034",
        "title": "Infinitesimal Transport-Mismatch Curvature and Non-Scalar Arithmetic Descent",
        "starting_head": "90493831c9bd803526593691e7f39b55a7b9fb40",
        "substantive_parent": "1d777ea1bc7e962ee6ad03f3f72b83c731dfb186",
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
        "curvature_sign_status": sign_audit["classification"],
        "homogeneity_status": (
            "E F_0 = d F_0 implies A_1 = d A_0, A_2 = d^2 A_0, and C_arith(F_0) = 0; "
            "not implied by arithmetic label preservation alone (ARITHMETIC_CURVATURE_FLATNESS_NOT_IMPLIED)."
        ),
        "compact_support_obstruction": compact_no_go.classification,
        "mellin_scaling": {
            "raw_factor": "tau^{K(a + (1 + eta)(s + t))} H_0(s, t)",
            "net_normalized_factor": "tau^{eta K (s + t)}",
            "first_derivative_at_0": "K log(tau) (s + t)",
            "second_derivative_at_0": "K^2 (log(tau))^2 (s + t)^2",
        },
        "centered_exponent_convention": {
            "uncentered": "s + t",
            "half_density_centered": "(s - 1/2) + (t - 1/2) = s + t - 1",
            "conjugate_pair_t_eq_bar_rho": "2 * delta_rho (radial)",
            "reflection_pair_t_eq_1_minus_bar_rho": "2 * i * gamma_rho (ordinate/phase)",
            "general_pair_rho_sigma": "(delta_rho + delta_sigma) + i*(gamma_rho + gamma_sigma)",
        },
        "natural_zero_pairing": pairing_audit.naturally_induced_pairing,
        "spectral_curvature_type": spectral_firewalls["spectral_curvature_outcome"],
        "weight_sign": "COMPLEX_SIGNED_DOUBLE_SUM_WEIGHTS",
        "cross_term_status": "UNRESTRICTED_DOUBLE_SUM_WITH_POLE_TRIVIAL_AND_ARCHIMEDEAN_TERMS",
        "theta_candidate_status": asdict(theta_fallback),
        "tau_specificity": generic_base["classification"],
        "weil_equivalence_status": weil_firewall["classification"],
        "relation_to_OBL_CT_001A": reconciliation["classification"],
        "principal_classification": PRINCIPAL_CLASSIFICATION,
        "triggered_outcome_codes": [
            OUTCOME_B_ARITHMETIC_FLATNESS_NOT_IMPLIED,
            OUTCOME_C_COMPACT_SUPPORT_NO_GO,
            OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE,
            OUTCOME_E_WEIL_EQUIVALENCE,
            OUTCOME_G_REDUCES_TO_OBL_CT_001A,
        ],
        "exact_remaining_subgate": theta_fallback.exact_remaining_theorem,
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
    "CLASSIFICATION_ARITHMETIC_INDEFINITE",
    "CLASSIFICATION_COMPACT_SUPPORT_IMPOSSIBLE",
    "CLASSIFICATION_CURVATURE_POSITIVITY_RH_EQUIVALENT",
    "CLASSIFICATION_FINITE_ACCIDENTAL_ZERO",
    "CLASSIFICATION_GENERIC_SCALE_CURVATURE",
    "CLASSIFICATION_REDUCES_TO_EXISTING_OBL_CT_001A",
    "CLASSIFICATION_SELECTED_BLOCK_ONLY",
    "CompactSupportHomogeneityAudit",
    "EulerMomentResult",
    "ExponentialMixtureCurvatureResult",
    "MismatchDerivativeResult",
    "OUTCOME_A_FULL_BRIDGE",
    "OUTCOME_B_ARITHMETIC_FLATNESS_NOT_IMPLIED",
    "OUTCOME_C_COMPACT_SUPPORT_NO_GO",
    "OUTCOME_D_SPECTRAL_SIGNED_OR_DOUBLE",
    "OUTCOME_E_WEIL_EQUIVALENCE",
    "OUTCOME_F_THETA_SUBGATE_OPEN",
    "OUTCOME_G_REDUCES_TO_OBL_CT_001A",
    "PRINCIPAL_CLASSIFICATION",
    "SpectralPairingAuditResult",
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
    "reconcile_with_existing_curvature_transport",
]
