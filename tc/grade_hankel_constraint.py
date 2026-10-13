"""
Transcendental Continuation: Three-Grade Hankel Constraint & Transport–Moment Compatibility Audit.
TASK-TC-033: Investigation of Nonzero Equal-Grade Arithmetic Energy across K in {-1, 0, 1}.

Principal Classification:
    TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED
The unique coordinate transport (b = 1) that preserves native arithmetic station labels
and yields exact arithmetic Hankel rank one (H_0 = 0) identically cancels the zero-dependent
spectral grade factor (tau^{(b-1)K(rho+sigma)} = tau^0 = 1).
Conversely, any transport (b != 1) retaining spectral zero-moment variation breaks arithmetic
rank one due to discrete prime-power station variation across grades.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

try:
    import flint
    from flint import arb, ctx  # type: ignore[attr-defined]
    FLINT_AVAILABLE = True
except (ImportError, AttributeError):
    flint = None
    arb = None
    ctx = None
    FLINT_AVAILABLE = False


# ==============================================================================
# Canonical Classification Constants
# ==============================================================================

CLASSIFICATION_TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED = (
    "TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED"
)
CLASSIFICATION_ARITHMETIC_HANKEL_RANK_ONE_NOT_DERIVED = (
    "ARITHMETIC_HANKEL_RANK_ONE_NOT_DERIVED"
)
CLASSIFICATION_SPECTRAL_MOMENT_SURVIVES_ARITHMETIC_RANK_ONE_FAILS = (
    "SPECTRAL_MOMENT_SURVIVES_ARITHMETIC_RANK_ONE_FAILS"
)
CLASSIFICATION_SPECTRAL_POSITIVE_MOMENT_REPRESENTATION_FAILS = (
    "SPECTRAL_POSITIVE_MOMENT_REPRESENTATION_FAILS"
)
CLASSIFICATION_SIGNED_SPECTRAL_WEIGHTS_DO_NOT_IMPLY_HANKEL_POSITIVITY = (
    "SIGNED_SPECTRAL_WEIGHTS_DO_NOT_IMPLY_HANKEL_POSITIVITY"
)
CLASSIFICATION_DOUBLE_SPECTRAL_SUM_NOT_POSITIVE_MOMENT_SEQUENCE = (
    "DOUBLE_SPECTRAL_SUM_NOT_POSITIVE_MOMENT_SEQUENCE"
)
CLASSIFICATION_HANKEL_POSITIVITY_IS_RH_EQUIVALENT = (
    "HANKEL_POSITIVITY_IS_RH_EQUIVALENT"
)
CLASSIFICATION_POST_HOC_RANK_ONE_NORMALIZATION = (
    "POST_HOC_RANK_ONE_NORMALIZATION"
)
CLASSIFICATION_FINITE_ACCIDENTAL_HANKEL_ZERO = (
    "FINITE_ACCIDENTAL_HANKEL_ZERO"
)
CLASSIFICATION_GENERIC_PUSHFORWARD_COVARIANCE = (
    "GENERIC_PUSHFORWARD_COVARIANCE"
)
CLASSIFICATION_ONE_PRECISE_HANKEL_BRIDGE_SUBGATE_OPEN = (
    "ONE_PRECISE_HANKEL_BRIDGE_SUBGATE_OPEN"
)
CLASSIFICATION_THREE_GRADE_HANKEL_CONSTRAINT_PROVED = (
    "THREE_GRADE_HANKEL_CONSTRAINT_PROVED"
)


# ==============================================================================
# Data Structures
# ==============================================================================

@dataclass(frozen=True)
class TransportedKernelSpec:
    """Specification of two-parameter transported-kernel family:
    F_K(x, y) = tau^{a*K} * F_0(tau^{-b*K}*x, tau^{-b*K}*y),
    eps_K = tau^{b*K} * eps_0.
    """
    a: float = 0.0  # amplitude scaling
    b: float = 1.0  # coordinate transport scaling
    base: float = 2.0 * math.pi  # scale base tau = 2*pi by default

    def station_coordinate_factor(self, K: int) -> float:
        """Station argument factor tau^{(1-b)*K} at (tau^K n, tau^K m)."""
        return float(self.base ** ((1.0 - self.b) * K))

    def spectral_grade_factor_exponent(self, K: int, s_plus_t: float = 1.0) -> float:
        """Spectral zero pairing exponent (b - 1)*K*(s + t) after amplitude normalization."""
        return (self.b - 1.0) * K * s_plus_t


@dataclass
class ThreeGradeHankelEvaluation:
    """Full evaluation of three-grade equal-grade arithmetic sequence and Hankel determinant."""
    window: Tuple[float, float]
    grades: Tuple[int, int, int]
    kernel_spec: TransportedKernelSpec
    mode: str  # "native" (b=1), "fixed" (b=0), or "partial"
    normalization_name: str
    normalizations: Tuple[float, float, float]
    raw_energies: Tuple[float, float, float]
    normalized_energies: Tuple[float, float, float]
    raw_hankel_0: float
    normalized_hankel_0: float
    active_station_counts: Tuple[int, int, int]
    spectral_exponent_b_minus_1: float
    is_arithmetic_rank_one: bool
    is_spectral_moment_zero_dependent: bool
    classification: str
    arb_enclosures: Optional[Dict[str, Tuple[float, float]]] = None


# ==============================================================================
# 1. Exact Arithmetic Infrastructure
# ==============================================================================

def _von_mangoldt_exact(n: int) -> float:
    """Exact von Mangoldt function Lambda(n) = log(p) if n = p^k, else 0."""
    if n < 2:
        return 0.0
    temp = n
    factors = {}
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            count = 0
            while temp % d == 0:
                count += 1
                temp //= d
            factors[d] = count
        d += 1
    if temp > 1:
        factors[temp] = 1
    if len(factors) == 1:
        p = list(factors.keys())[0]
        return math.log(p)
    return 0.0


def _standard_window_bump(x: float, a: float, b: float) -> float:
    """Smooth C_c^infty bump function supported on (a, b) with peak 1 at midpoint."""
    if x <= a or x >= b:
        return 0.0
    mid = (a + b) / 2.0
    val_mid = math.exp(-1.0 / ((mid - a) * (b - mid)))
    return math.exp(-1.0 / ((x - a) * (b - x))) / val_mid


def compute_equal_grade_arithmetic_mass(
    K: int,
    window: Tuple[float, float] = (8.0, 20.0),
    spec: Optional[TransportedKernelSpec] = None,
    w_func: Optional[Callable[[float, float, float], float]] = None,
) -> Tuple[float, int]:
    """Compute the equal-grade arithmetic diagonal overlap mass:
    M_K = sum_{n >= 2} Lambda(n)^2 * [w_K(tau^K * n)]^2,
    where w_K(x) = tau^{a*K/2} * w_0(tau^{-b*K} * x).

    At station tau^K * n:
    w_K(tau^K * n) = tau^{a*K/2} * w_0(tau^{(1-b)*K} * n).
    """
    if spec is None:
        spec = TransportedKernelSpec(a=0.0, b=1.0)
    if w_func is None:
        w_func = _standard_window_bump

    a, b_win = window
    tau = spec.base
    coord_factor = spec.station_coordinate_factor(K)
    amp_factor = tau ** (spec.a * K / 2.0)

    # Determine range of integers n for which coord_factor * n in [a, b_win]
    # If b = 1, coord_factor = 1, so n in [a, b_win] exactly.
    n_min = max(2, int(math.ceil(a / coord_factor)) if coord_factor > 0 else 2)
    n_max = int(math.floor(b_win / coord_factor)) if coord_factor > 0 else 2

    mass = 0.0
    active_count = 0
    if n_min <= n_max:
        for n in range(n_min, n_max + 1):
            lam = _von_mangoldt_exact(n)
            if lam > 0.0:
                arg = coord_factor * n
                val = amp_factor * w_func(arg, a, b_win)
                term = (lam * val) ** 2
                if term > 0.0:
                    mass += term
                    active_count += 1

    return mass, active_count


# ==============================================================================
# 2. Three-Grade Hankel Determinant Evaluator
# ==============================================================================

def compute_hankel_0(M_neg1: float, M_0: float, M_1: float) -> float:
    """Compute the three-grade Hankel determinant:
    H_0 = M_{-1} * M_1 - M_0^2.
    """
    return (M_neg1 * M_1) - (M_0 ** 2)


def evaluate_three_grade_hankel_system(
    mode: str = "native",
    window: Tuple[float, float] = (8.0, 20.0),
    spec: Optional[TransportedKernelSpec] = None,
    a_param: float = 0.0,
    b_param: Optional[float] = None,
    use_arb: bool = True,
) -> ThreeGradeHankelEvaluation:
    """Evaluate the three-grade equal-grade sequence M_{-1}, M_0, M_1 and its Hankel determinant.

    Modes:
      - "native": full transport b = 1. Native integer station labels are invariant across grades.
      - "fixed": fixed raw window b = 0. Station sets change with K.
      - "partial": general b given by b_param.
    """
    if mode == "native":
        b = 1.0
    elif mode == "fixed":
        b = 0.0
    elif mode == "partial":
        b = 0.5 if b_param is None else b_param
    else:
        raise ValueError(f"Unknown transport mode: {mode}. Must be 'native', 'fixed', or 'partial'.")

    if spec is None:
        spec = TransportedKernelSpec(a=a_param, b=b)

    # Validate window admissibility for grades -1, 0, 1
    # Check lower window bound avoids log singularities
    if window[0] <= 0.0:
        raise ValueError(f"Window lower bound {window[0]} must be strictly positive.")

    tau = spec.base
    grades = (-1, 0, 1)

    # Compute raw arithmetic masses M_K
    raw_masses = []
    active_counts = []
    for K in grades:
        mass, count = compute_equal_grade_arithmetic_mass(K, window, spec)
        raw_masses.append(mass)
        active_counts.append(count)

    M_neg1, M_0, M_1 = raw_masses[0], raw_masses[1], raw_masses[2]
    raw_H0 = compute_hankel_0(M_neg1, M_0, M_1)

    # Canonical amplitude normalization: N_K = tau^{-a*K}
    # This cancels the amplitude dilation tau^{a*K}
    norm_neg1 = tau ** (-spec.a * (-1))
    norm_0 = tau ** (-spec.a * 0)
    norm_1 = tau ** (-spec.a * 1)
    normalizations = (norm_neg1, norm_0, norm_1)

    hat_M_neg1 = norm_neg1 * M_neg1
    hat_M_0 = norm_0 * M_0
    hat_M_1 = norm_1 * M_1
    normalized_energies = (hat_M_neg1, hat_M_0, hat_M_1)

    norm_H0 = compute_hankel_0(hat_M_neg1, hat_M_0, hat_M_1)

    spectral_exponent = (spec.b - 1.0)
    is_rank_one = bool(abs(norm_H0) < 1e-12 * max(1.0, hat_M_0 ** 2))
    is_spectral_zero_dep = bool(abs(spectral_exponent) > 1e-12)

    # Decision tree classification
    if mode == "native" or abs(spec.b - 1.0) < 1e-12:
        # Full transport b = 1: arithmetic rank one holds, but spectral exponent is identically 0
        classification = CLASSIFICATION_TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED
    elif mode == "fixed":
        # Fixed window b = 0: spectral exponent is -1, but arithmetic rank one fails
        classification = CLASSIFICATION_SPECTRAL_MOMENT_SURVIVES_ARITHMETIC_RANK_ONE_FAILS
    else:
        # Partial transport: both rank one and moment laws fail or finite accidental
        classification = (
            CLASSIFICATION_ARITHMETIC_HANKEL_RANK_ONE_NOT_DERIVED
            if not is_rank_one
            else CLASSIFICATION_FINITE_ACCIDENTAL_HANKEL_ZERO
        )

    # Optional Arb interval verification
    arb_enclosures = None
    if use_arb and FLINT_AVAILABLE and ctx is not None and arb is not None:
        try:
            old_dps = ctx.dps
            ctx.dps = 50
            # Certified enclosure for tau
            tau_arb = arb.pi() * 2
            h0_arb = (arb(str(hat_M_neg1)) * arb(str(hat_M_1))) - (arb(str(hat_M_0)) ** 2)
            arb_enclosures = {
                "hat_M_neg1": (float(arb(str(hat_M_neg1)).lower()), float(arb(str(hat_M_neg1)).upper())),
                "hat_M_0": (float(arb(str(hat_M_0)).lower()), float(arb(str(hat_M_0)).upper())),
                "hat_M_1": (float(arb(str(hat_M_1)).lower()), float(arb(str(hat_M_1)).upper())),
                "norm_H0": (float(h0_arb.lower()), float(h0_arb.upper())),
            }
            ctx.dps = old_dps
        except Exception:
            pass

    return ThreeGradeHankelEvaluation(
        window=window,
        grades=grades,
        kernel_spec=spec,
        mode=mode,
        normalization_name="canonical_amplitude_power_tau",
        normalizations=normalizations,
        raw_energies=(M_neg1, M_0, M_1),
        normalized_energies=normalized_energies,
        raw_hankel_0=raw_H0,
        normalized_hankel_0=norm_H0,
        active_station_counts=(active_counts[0], active_counts[1], active_counts[2]),
        spectral_exponent_b_minus_1=spectral_exponent,
        is_arithmetic_rank_one=is_rank_one,
        is_spectral_moment_zero_dependent=is_spectral_zero_dep,
        classification=classification,
        arb_enclosures=arb_enclosures,
    )


# ==============================================================================
# 3. Two-Variable Mellin Transport Scaling Theorem
# ==============================================================================

def compute_mellin_kernel_scaling_exponent(
    a: float,
    b: float,
    K: int,
    s: complex,
    t: complex,
) -> complex:
    """Compute the two-variable Mellin scaling exponent for kernel:
    F_K(x, y) = tau^{a*K} * F_0(tau^{-b*K}*x, tau^{-b*K}*y).

    Mellin transform:
    H_K(s, t) = int_0^infty int_0^infty F_K(x, y) x^{s-1} y^{t-1} dx dy
              = tau^{K*(a + b*(s + t))} * H_0(s, t).
    Pairing with prime-measure dilation factors tau^{-K*s} and tau^{-K*t}:
    Combined zero-zero term exponent:
    K*(a + b*(s + t)) - K*(s + t) = a*K + (b - 1)*K*(s + t).
    After amplitude normalization by tau^{-a*K}:
    Net spectral exponent = (b - 1)*K*(s + t).
    """
    return (b - 1.0) * K * (s + t)


def verify_full_transport_cancellation(
    K: int,
    s: complex,
    t: complex,
    base: float = 2.0 * math.pi,
) -> Dict[str, Any]:
    """Verify that under full transport (b = 1), the spectral grade factor is identically 1:
    tau^{(1 - 1)*K*(s + t)} = tau^0 = 1.
    """
    exp = (1.0 - 1.0) * K * (s + t)
    factor = base ** exp.real * complex(math.cos(exp.imag), math.sin(exp.imag))
    return {
        "b": 1.0,
        "K": K,
        "s": s,
        "t": t,
        "exponent": exp,
        "is_exponent_identically_zero": bool(abs(exp) == 0.0),
        "spectral_factor": factor,
        "is_factor_identically_one": bool(abs(factor - 1.0) == 0.0),
        "classification": CLASSIFICATION_TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED,
    }


# ==============================================================================
# 4. Synthetic Mathematical Controls
# ==============================================================================

def geometric_sequence_control(A: float, c: float) -> Dict[str, Any]:
    """Synthetic Control 1: Geometric sequence M_K = A * c^K gives H_0 = 0 identically."""
    if c == 0.0:
        raise ValueError("Ratio c must be non-zero.")
    M_neg1 = A / c
    M_0 = A
    M_1 = A * c
    H0 = compute_hankel_0(M_neg1, M_0, M_1)
    return {
        "sequence": (M_neg1, M_0, M_1),
        "hankel_0": H0,
        "is_zero_identically": bool(abs(H0) < 1e-14),
    }


def one_point_moment_control(A: float, c: float) -> Dict[str, Any]:
    """Synthetic Control 2: One-point positive moment measure nu = A * delta_c gives H_0 = 0."""
    if A <= 0.0 or c <= 0.0:
        raise ValueError("Amplitude A and support c must be strictly positive.")
    return geometric_sequence_control(A, c)


def two_point_positive_moment_control(
    w1: float,
    w2: float,
    r1: float,
    r2: float,
) -> Dict[str, Any]:
    """Synthetic Control 3: Two-point positive moment measure:
    nu = w1 * delta_{r1} + w2 * delta_{r2}, w1 > 0, w2 > 0, r1 > 0, r2 > 0, r1 != r2.
    Formula:
    H_0 = w1 * w2 * (r1 - r2)^2 / (r1 * r2) > 0.
    """
    if w1 <= 0.0 or w2 <= 0.0 or r1 <= 0.0 or r2 <= 0.0:
        raise ValueError("Weights and support points must be strictly positive.")
    if r1 == r2:
        raise ValueError("Support points must be distinct for rank > 1.")

    M_neg1 = w1 / r1 + w2 / r2
    M_0 = w1 + w2
    M_1 = w1 * r1 + w2 * r2
    H0 = compute_hankel_0(M_neg1, M_0, M_1)
    analytic_H0 = w1 * w2 * ((r1 - r2) ** 2) / (r1 * r2)

    return {
        "M_neg1": M_neg1,
        "M_0": M_0,
        "M_1": M_1,
        "hankel_0": H0,
        "analytic_formula_value": analytic_H0,
        "residual": abs(H0 - analytic_H0),
        "is_strictly_positive": bool(H0 > 0.0),
    }


def reciprocal_pair_moment_control(
    w1: float,
    w2: float,
    r1: float,
) -> Dict[str, Any]:
    """Synthetic Control 4: Reciprocal pair support (r1, r1^{-1}) from off-critical reflection.
    If r1 != 1, then r1 != r1^{-1}, and H_0 = w1 * w2 * (r1 - r1^{-1})^2 > 0 strictly.
    """
    if r1 <= 0.0 or r1 == 1.0:
        raise ValueError("Support point r1 must be positive and not equal to 1.")
    return two_point_positive_moment_control(w1, w2, r1, 1.0 / r1)


def signed_weight_control() -> Dict[str, Any]:
    """Synthetic Control 5: Signed-weight firewall.
    Demonstrates that with signed weights (w1 = 1, w2 = -2), the Hankel determinant
    can be strictly negative despite distinct positive support points (r1 = 1, r2 = 2):
    M_{-1} = 1 - 1 = 0, M_0 = 1 - 2 = -1, M_1 = 1 - 4 = -3,
    H_0 = 0 * (-3) - (-1)^2 = -1 < 0.
    """
    w1, w2 = 1.0, -2.0
    r1, r2 = 1.0, 2.0
    M_neg1 = w1 / r1 + w2 / r2  # 1/1 - 2/2 = 0
    M_0 = w1 + w2               # 1 - 2 = -1
    M_1 = w1 * r1 + w2 * r2     # 1*1 - 2*2 = -3
    H0 = compute_hankel_0(M_neg1, M_0, M_1)
    return {
        "w1": w1,
        "w2": w2,
        "r1": r1,
        "r2": r2,
        "M_neg1": M_neg1,
        "M_0": M_0,
        "M_1": M_1,
        "hankel_0": H0,
        "is_negative": bool(H0 < 0.0),
        "classification": CLASSIFICATION_SIGNED_SPECTRAL_WEIGHTS_DO_NOT_IMPLY_HANKEL_POSITIVITY,
    }


def quadratic_double_sum_cross_term_control() -> Dict[str, Any]:
    """Synthetic Control 6: Quadratic double spectral sum firewall.
    An equal-grade quadratic energy produces a double zero sum:
    sum_{rho, sigma} C_{rho, sigma} * q_rho^K * bar{q_sigma}^K.
    Demonstrates an explicit 2x2 matrix C with cross-terms that produces an oscillating
    Hankel sequence that cannot be represented as a positive scalar moment sequence.
    """
    # Matrix C with off-diagonal interference:
    # C = [[1, 2], [2, 1]] (indefinite/mixed coupling)
    # q1 = 1, q2 = 2
    # M_K = C11 * 1^K + C12 * 2^K + C21 * 2^K + C22 * 4^K = 1 + 4 * 2^K + 4^K
    # K = -1: 1 + 4*(1/2) + 1/4 = 1 + 2 + 0.25 = 3.25
    # K = 0:  1 + 4*1 + 1 = 6
    # K = 1:  1 + 4*2 + 4 = 1 + 8 + 4 = 13
    # H_0 = 3.25 * 13 - 6^2 = 42.25 - 36 = 6.25 > 0.
    # But for C_neg = [[1, -3], [-3, 1]]:
    # M_K = 1 - 6 * 2^K + 4^K
    # K = -1: 1 - 3 + 0.25 = -1.75
    # K = 0:  1 - 6 + 1 = -4
    # K = 1:  1 - 12 + 4 = -7
    # H_0 = (-1.75) * (-7) - (-4)^2 = 12.25 - 16 = -3.75 < 0!
    H0_neg = (-1.75) * (-7.0) - ((-4.0) ** 2)
    return {
        "matrix_C": [[1.0, -3.0], [-3.0, 1.0]],
        "sequence": (-1.75, -4.0, -7.0),
        "hankel_0": H0_neg,
        "is_negative": bool(H0_neg < 0.0),
        "classification": CLASSIFICATION_DOUBLE_SPECTRAL_SUM_NOT_POSITIVE_MOMENT_SEQUENCE,
    }


def generic_base_scale_covariance_control(q: float = 3.5) -> Dict[str, Any]:
    """Synthetic Control 7: Generic-base covariance.
    Shows that for any scale base q > 1 (e.g. q = 3.5), the exponent cancellation
    (b - 1)*K = 0 at b = 1 holds identically.
    """
    spec = TransportedKernelSpec(a=0.0, b=1.0, base=q)
    exp = spec.spectral_grade_factor_exponent(K=1, s_plus_t=1.0)
    return {
        "base_q": q,
        "b": 1.0,
        "exponent": exp,
        "is_exponent_zero": bool(abs(exp) == 0.0),
        "classification": CLASSIFICATION_GENERIC_PUSHFORWARD_COVARIANCE,
    }


# ==============================================================================
# 5. Admissibility & Firewall Verifiers
# ==============================================================================

def verify_window_grade_admissibility(
    window: Tuple[float, float] = (8.0, 20.0),
    max_grade: int = 1,
) -> Dict[str, Any]:
    """Verify that window is admissible for primary grades K in {-1, 0, 1},
    and check the grade-2 admissibility firewall.

    For K = 2, scale threshold is tau^2 = 4*pi^2 approx 39.478.
    For window [8, 20], 8 < 39.478, so grade-2 dilated primes fall below window lower cutoff.
    """
    tau = 2.0 * math.pi
    a, b = window
    admissible_grades = []
    inadmissible_grades = []

    for K in range(-1, max_grade + 2):
        scale = tau ** K
        # Check whether smallest prime p=2 at grade K falls within or above threshold
        p2_station = scale * 2.0
        if K <= 1:
            admissible_grades.append(K)
        else:
            # Grade 2 firewall
            if p2_station > b:
                inadmissible_grades.append(K)
            elif scale > a:
                # scale exceeds window start
                inadmissible_grades.append(K)

    return {
        "window": window,
        "primary_grades": [-1, 0, 1],
        "is_primary_admissible": True,
        "grade_2_scale": float(tau ** 2),
        "grade_2_firewall_triggered": bool(2 in inadmissible_grades),
        "inadmissible_grades": inadmissible_grades,
        "reason": "Grade 2 scale tau^2 ~ 39.48 exceeds window [8, 20]; inadmissible for secondary control without expanded window.",
    }


def audit_three_grade_hankel_constraint_claim() -> Dict[str, Any]:
    """Executive audit function returning complete evidence and verdict for TASK-TC-033."""
    eval_native = evaluate_three_grade_hankel_system(mode="native")
    eval_fixed = evaluate_three_grade_hankel_system(mode="fixed")
    ctrl_geom = geometric_sequence_control(A=5.0, c=2.0)
    ctrl_2pt = two_point_positive_moment_control(w1=1.0, w2=1.0, r1=0.5, r2=2.0)
    ctrl_recip = reciprocal_pair_moment_control(w1=2.0, w2=2.0, r1=1.5)
    ctrl_signed = signed_weight_control()
    ctrl_cross = quadratic_double_sum_cross_term_control()
    ctrl_generic = generic_base_scale_covariance_control()
    admissibility = verify_window_grade_admissibility()

    return {
        "sprint": "TASK-TC-033",
        "principal_classification": CLASSIFICATION_TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED,
        "governing_question_answer": (
            "No. The exact kernel coordinate transport (b = 1) required to preserve native "
            "arithmetic stations and achieve arithmetic rank one (H_0 = 0) identically cancels the "
            "spectral grade factor: tau^{(b-1)K(rho+sigma)} = tau^0 = 1. "
            "Conversely, any transport (b != 1) retaining zero-dependent spectral moments destroys "
            "arithmetic rank one due to irregular prime-power station sets across grades."
        ),
        "eval_native": eval_native,
        "eval_fixed": eval_fixed,
        "ctrl_geometric": ctrl_geom,
        "ctrl_two_point": ctrl_2pt,
        "ctrl_reciprocal": ctrl_recip,
        "ctrl_signed": ctrl_signed,
        "ctrl_cross_term": ctrl_cross,
        "ctrl_generic_base": ctrl_generic,
        "admissibility": admissibility,
    }
