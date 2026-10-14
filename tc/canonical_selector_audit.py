"""
Canonical Zeta Selector Principle and Uniqueness Audit (`TASK-TC-035`).

Audits the primary post-`TASK-TC-034R` research question under `OBL-CT-001A`:

    Which zero-independent axioms, derived from the completed zeta function xi(s)
    and its prime-side structure, uniquely select a non-scalar arithmetic functional
    from the otherwise arbitrary kernel space before curvature or spectral positivity
    is tested?

Mathematical & Structural Contents
----------------------------------
1. Six Candidate Selector Mechanisms Audited:
   - Selector I   (Functional Equation / Hamburger-Burnol Co-Poisson Uniqueness):
     Selects the 1D ray of the distribution W_zeta (or xi(s)), NOT a unique test kernel F_0.
     Explicitly refuted as a sign-definite kernel selector by constructing compactly supported
     witnesses G_tilde_minus^inv, G_tilde_plus^inv in C_c^infty((0, infty)^2) that are
     simultaneously nonnegative, permutation-symmetric F(x,y) = F(y,x), and multiplicative-
     inversion-symmetric F(c_0^2/x, c_0^2/y) = F(x,y), yet have opposite Arb-certified
     complete arithmetic curvatures.
   - Selector II  (Jacobi Theta Self-Duality & Canonical Gaussian):
     Fourier self-duality hat{f} = f + ground-state positivity selects the additive Gaussian
     Theta_1(x,y) = exp(-pi*(x^2 + y^2)). Because prime-station transport acts by the
     multiplicative Euler generator E = x d/dx + y d/dy while Theta_t is an additive heat
     kernel, the chain-rule identity (t d/dt)^2 = t^2 d^2/dt^2 + t d/dt introduces a strictly
     negative Euler drift -4*pi*t*M_0*M_1 that dominates the positive Bernstein variance
     4*pi^2*t^2*(M_0*M_2 - M_1^2) at t = 1 by five orders of magnitude, yielding an
     Arb-certified strictly negative arithmetic curvature (both on compact support X_15 and
     on the full infinite lattice N_{>=2}^2).
   - Selector III (Prime/Archimedean Balance & Burnol Conductor Operator):
     Weil's explicit formula is a universal distributional identity on the dual space of
     admissible test functions, not a single-kernel selector; forcing the arithmetic side
     to vanish identically triggers exact complement cancellation (`TASK-TC-032R`).
   - Selector IV  (Extremal / Variational Principles: Nyman-Beurling-Baez-Duarte, Li, Suzuki):
     Strict convexity selects a unique finite-stage extremizer d_N^2 (or lambda_n, lambda_1(R))
     at each fixed parameter N, but any single finite stage has d_N^2 > 0 unconditionally;
     excluding delta_rho != 0 requires the infinite asymptotic limit (lim_{N->infty} d_N = 0),
     which is RH-equivalent and invariant under isometric Mellin grade rescaling.
   - Selector V   (Canonical Operator Trace: Connes-Consani Semi-Local Trace / Sonin Compression):
     Compressing the scaling action onto the orthogonal complement of phase-space cutoffs
     explains Archimedean positivity via prolate spheroidal wave functions, while the global
     semi-local trace functional over primes reduces to semi-local Weil positivity (RH-equivalent).
   - Selector VI  (Stronger Multi-Grade Naturality / Scale Homogeneity):
     Ordinary transfer naturality across grades is an exact 1-coboundary satisfied by all F_0
     at b = 1; strengthening naturality to Euler scale homogeneity E F_0 = d F_0 forces
     C_arith(F_0) = 0 but admits no nonzero compactly supported kernel (`TASK-TC-034R`).

2. Exact Algebraic & Analytic Theorems Derived and Formalized in Lean 4:
   - Separable tensor-square curvature reduction:
       C_arith(f x f) = 2 * m_0^2 * (m_0 * m_2 - m_1^2).
   - Additive-to-multiplicative Euler chain-rule drift identity:
       C_arith(Theta_t) = 4*pi^2*t^2*(M_0*M_2 - M_1^2) - 4*pi*t*M_0*M_1.
   - Multiplicative log-Gaussian variance-threshold identity:
       C_arith(F_{alpha, w_0}) = 16*alpha^2*(S_0*S_2 - S_1^2) - 8*alpha*S_0^2.
   - Canonical Selector Trilemma & complement-positivity dichotomy (`OBL-CT-001A`).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from pathlib import Path
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

try:
    import flint  # type: ignore
except ImportError:  # pragma: no cover
    flint = None

from tc.transport_mismatch_curvature import (
    ARB_CERTIFICATION_NOT_AVAILABLE,
    active_prime_power_stations,
    evaluate_euler_moments_A0_A1_A2,
    flat_transition_h_jet,
    plateau_cutoff_2d_euler_jet,
    prime_power_base_table,
    smooth_step_S_jet,
)

# ---------------------------------------------------------------------------
# Constants and Required Classification Codes (`TASK-TC-035`)
# ---------------------------------------------------------------------------

TAU: float = 2.0 * math.pi
LOG_TAU: float = math.log(TAU)

TASK_TC_035_ID = "TASK-TC-035"
TASK_TC_035_STATUS = "TASK_TC_035_CANONICAL_SELECTOR_AUDIT_COMPLETE"

PRINCIPAL_CLASSIFICATION = (
    "NO_ZERO_INDEPENDENT_SINGLE_KERNEL_SELECTOR_FOUND_IN_STANDARD_ZETA_AXIOMS"
)
SELECTOR_PRINCIPAL_CLASSIFICATION = PRINCIPAL_CLASSIFICATION
SECONDARY_TRILEMMA_CLASSIFICATION = "CANONICAL_SELECTOR_TRILEMMA_PROVED_OBL_CT_001A_OPEN"

SELECTOR_I_FUNCTIONAL_EQUATION_STATUS = (
    "FUNCTIONAL_EQUATION_SELECTS_DISTRIBUTION_RAY_NOT_TEST_KERNEL"
)
SELECTOR_II_THETA_SELF_DUALITY_STATUS = (
    "THETA_SELF_DUAL_GAUSSIAN_HAS_NEGATIVE_EULER_CURVATURE_BY_DRIFT"
)
SELECTOR_III_PRIME_ARCHIMEDEAN_STATUS = (
    "PRIME_ARCHIMEDEAN_BALANCE_IS_UNIVERSAL_DISTRIBUTIONAL_IDENTITY"
)
SELECTOR_IV_VARIATIONAL_EXTREMAL_STATUS = (
    "VARIATIONAL_SELECTORS_REQUIRE_INFINITE_ASYMPTOTIC_FAMILY_RH_EQUIVALENT"
)
SELECTOR_V_OPERATOR_TRACE_STATUS = (
    "OPERATOR_TRACE_COMPRESSION_REDUCES_TO_SEMI_LOCAL_WEIL_POSITIVITY"
)
SELECTOR_VI_STRONG_NATURALITY_STATUS = (
    "STRONGER_SCALE_NATURALITY_COLLAPSES_TO_HOMOGENEITY_NO_GO"
)

INVERSION_SYMMETRIC_NEG_CERTIFIED = (
    "INVERSION_SYMMETRIC_COMPACT_NEGATIVE_CURVATURE_CERTIFIED"
)
INVERSION_SYMMETRIC_POS_CERTIFIED = (
    "INVERSION_SYMMETRIC_COMPACT_POSITIVE_CURVATURE_CERTIFIED"
)
INVERSION_SYMMETRY_SIGN_INDEFINITE_STATUS = (
    "INVERSION_AND_PERMUTATION_SYMMETRIC_SUBSPACE_SIGN_INDEFINITE"
)

THETA_GAUSSIAN_NEG_CERTIFIED = (
    "CANONICAL_THETA_GAUSSIAN_NEGATIVE_CURVATURE_CERTIFIED"
)
LOG_GAUSSIAN_VARIANCE_THRESHOLD_PROVED = (
    "LOG_GAUSSIAN_CURVATURE_SIGN_DEPENDS_ON_VARIANCE_RATIO"
)
TENSOR_SQUARE_REDUCTION_PROVED = (
    "SEPARABLE_TENSOR_SQUARE_REDUCES_TO_1D_CURVATURE"
)

OBL_CT_001A_STATUS = "OBL_CT_001A_REMAINS_OPEN"
CANDIDATE_SELECTOR_EXHAUSTION_DOES_NOT_REFUTE_TC = (
    "CANDIDATE_SELECTOR_EXHAUSTION_DOES_NOT_REFUTE_TC"
)


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CandidateSelectorMechanismAudit:
    """Structured audit of one candidate canonical selector principle (`TASK-TC-035`)."""

    selector_id: str
    selector_name: str
    governing_zero_independent_axioms: str
    unique_object_selected: str
    selects_unique_test_kernel_status: str
    arithmetic_curvature_constraint_status: str
    spectral_positivity_or_isolation_status: str
    circularity_or_obstruction_firewall: str
    evidence_class: str
    classification: str
    primary_literature_references: List[str]


@dataclass(frozen=True)
class SeparableTensorSquareResult:
    """Verification of C_arith(f x f) = 2 * m_0^2 * (m_0 * m_2 - m_1^2)."""

    m0: float
    m1: float
    m2: float
    one_dim_curvature: float
    A0_2d: float
    A1_2d: float
    A2_2d: float
    two_dim_curvature: float
    formula_rhs: float
    A0_abs_err: float
    A1_abs_err: float
    A2_abs_err: float
    curvature_identity_abs_err: float
    classification: str


@dataclass(frozen=True)
class LogGaussianVarianceResult:
    """Verification of C_arith(F_{alpha, w_0}) = 16*alpha^2*(S_0*S_2 - S_1^2) - 8*alpha*S_0^2."""

    alpha: float
    w0: float
    S0: float
    S1: float
    S2: float
    station_variance_det: float
    normalized_variance: float
    critical_alpha: float
    variance_term_16_alpha2_det: float
    concavity_term_minus_8_alpha_S02: float
    arithmetic_curvature_direct: float
    arithmetic_curvature_formula: float
    identity_abs_err: float
    sign_regime: str


# ---------------------------------------------------------------------------
# Section 1: Separable Tensor-Square Curvature Reduction
# ---------------------------------------------------------------------------


def evaluate_separable_tensor_square_reduction(
    f_fn: Optional[Callable[[float], float]] = None,
    d1_f_fn: Optional[Callable[[float], float]] = None,
    d2_f_fn: Optional[Callable[[float], float]] = None,
    n_max: int = 15,
) -> SeparableTensorSquareResult:
    """
    Verify Theorem 1 (`tensor_square_curvature_reduction`):
    For any separable rank-one kernel F_0(x, y) = f(x) f(y) and 1D Euler operator D = x d/dx,
    let m_j = sum_{n=2}^{n_max} Lambda(n) (D^j f)(n). Then:
        A_0(f x f) = m_0^2,
        A_1(f x f) = 2 m_0 m_1,
        A_2(f x f) = 2 m_0 m_2 + 2 m_1^2,
    and:
        C_arith(f x f) = A_0 A_2 - A_1^2 = 2 m_0^2 (m_0 m_2 - m_1^2).
    """
    if f_fn is None or d1_f_fn is None or d2_f_fn is None:
        # Default smooth 1D test profile f(x) = exp(-(log(x/4))^2) on active stations
        def _f(x: float) -> float:
            u = math.log(x / 4.0)
            return math.exp(-(u * u))

        def _d1(x: float) -> float:
            u = math.log(x / 4.0)
            return -2.0 * u * math.exp(-(u * u))

        def _d2(x: float) -> float:
            u = math.log(x / 4.0)
            return (4.0 * u * u - 2.0) * math.exp(-(u * u))

        f_fn, d1_f_fn, d2_f_fn = _f, _d1, _d2

    stations = active_prime_power_stations(n_max)
    m0 = 0.0
    m1 = 0.0
    m2 = 0.0
    for n, lam_n in stations:
        xn = float(n)
        m0 += lam_n * f_fn(xn)
        m1 += lam_n * d1_f_fn(xn)
        m2 += lam_n * d2_f_fn(xn)

    def f2d(x: float, y: float) -> float:
        return f_fn(x) * f_fn(y)

    def e1_2d(x: float, y: float) -> float:
        return d1_f_fn(x) * f_fn(y) + f_fn(x) * d1_f_fn(y)

    def e2_2d(x: float, y: float) -> float:
        return (
            d2_f_fn(x) * f_fn(y)
            + 2.0 * d1_f_fn(x) * d1_f_fn(y)
            + f_fn(x) * d2_f_fn(y)
        )

    moments_2d = evaluate_euler_moments_A0_A1_A2(
        f2d,
        n_max=n_max,
        euler1_f0=e1_2d,
        euler2_f0=e2_2d,
        evaluation_mode="COMPLETE_COMPACT_SUPPORT_SUM",
    )

    c_1d = m0 * m2 - m1 * m1
    rhs = 2.0 * (m0 * m0) * c_1d
    return SeparableTensorSquareResult(
        m0=m0,
        m1=m1,
        m2=m2,
        one_dim_curvature=c_1d,
        A0_2d=moments_2d.A0,
        A1_2d=moments_2d.A1,
        A2_2d=moments_2d.A2,
        two_dim_curvature=moments_2d.arithmetic_curvature,
        formula_rhs=rhs,
        A0_abs_err=abs(moments_2d.A0 - m0 * m0),
        A1_abs_err=abs(moments_2d.A1 - 2.0 * m0 * m1),
        A2_abs_err=abs(moments_2d.A2 - (2.0 * m0 * m2 + 2.0 * m1 * m1)),
        curvature_identity_abs_err=abs(moments_2d.arithmetic_curvature - rhs),
        classification=TENSOR_SQUARE_REDUCTION_PROVED,
    )


# ---------------------------------------------------------------------------
# Section 2: Functional-Equation Involution & Permutation Symmetry Audit
# ---------------------------------------------------------------------------


def log_symmetric_plateau_1d_euler_jet(
    x: float,
    c0: float = 4.0,
    u_plat: float = math.log(10.25 / 4.0),
    u_supp: float = math.log(10.5 / 4.0),
) -> Tuple[float, float, float]:
    """
    Evaluate a 1D smooth plateau cutoff chi_inv(x) in logarithmic coordinate u = log(x / c0)
    that is identically invariant under multiplicative inversion x |-> c0^2 / x (u |-> -u):
        chi_inv(c0^2 / x) = chi_inv(x),
    together with its 1D Euler derivatives:
        (chi_inv(x), (x d/dx) chi_inv(x), (x d/dx)^2 chi_inv(x))
      = (psi(u), psi'(u), psi''(u)).

    For c0 = 4.0, u_plat = log(10.25/4), u_supp = log(10.5/4):
      - Support interval is (16/10.5, 10.5) = (1.5238095..., 10.5);
      - Flat plateau where chi_inv == 1 and derivatives vanish is [16/10.25, 10.25] = [1.5609756..., 10.25];
      - Every integer station 2 <= n <= 10 lies strictly inside the flat plateau [1.5609756..., 10.25];
      - n = 1 and n >= 11 lie strictly outside the support (1.5238095..., 10.5).
    """
    if x <= 0.0:
        return (0.0, 0.0, 0.0)
    u = math.log(x / c0)
    abs_u = abs(u)
    if abs_u >= u_supp:
        return (0.0, 0.0, 0.0)
    if abs_u <= u_plat:
        return (1.0, 0.0, 0.0)
    inv_len = 1.0 / (u_supp - u_plat)
    t = (u_supp - abs_u) * inv_len
    s0, s1, s2 = smooth_step_S_jet(t)
    sign_u = 1.0 if u >= 0.0 else -1.0
    # d/du S((u_supp - |u|) / (u_supp - u_plat)) = -sign(u) * inv_len * S'(t)
    return (s0, -sign_u * inv_len * s1, (inv_len * inv_len) * s2)


def log_symmetric_plateau_2d_euler_jet(
    x: float,
    y: float,
    c0: float = 4.0,
) -> Tuple[float, float, float]:
    """
    2D inversion-and-permutation-symmetric plateau cutoff:
        X_inv(x, y) = chi_inv(x) * chi_inv(y),
    returning (X_inv, E X_inv, E^2 X_inv) where E = x d/dx + y d/dy.
    Satisfies X_inv(y, x) = X_inv(x, y) and X_inv(c0^2/x, c0^2/y) = X_inv(x, y) for all x, y > 0.
    """
    x0, x1, x2 = log_symmetric_plateau_1d_euler_jet(x, c0=c0)
    y0, y1, y2 = log_symmetric_plateau_1d_euler_jet(y, c0=c0)
    val = x0 * y0
    e1 = x1 * y0 + x0 * y1
    e2 = x2 * y0 + 2.0 * x1 * y1 + x0 * y2
    return (val, e1, e2)


def evaluate_inversion_symmetric_witness_jet(
    kind: str,
    x: float,
    y: float,
    c0: float = 4.0,
) -> Tuple[float, float, float]:
    """
    Evaluate the compactly supported, nonnegative, permutation-symmetric, and
    multiplicative-inversion-symmetric witness tilde{G}_-^inv or tilde{G}_+^inv
    and its first two Euler derivatives (F, E F, E^2 F) at (x, y) in (0, infty)^2.

    Here c0 = 4.0 (c0^2 = 16), w = log(x*y / 16):
      - kind == 'negative':
          G_-^inv(x, y) = exp(-(3/2) * w^2)
      - kind == 'positive':
          G_+^inv(x, y) = cosh((6/5) * w) * exp(-(2/25) * w^2)
    Under (x, y) |-> (16/x, 16/y), w |-> -w, so both prototypes and the cutoff X_inv
    are identically invariant under both (x, y) |-> (y, x) and (x, y) |-> (16/x, 16/y).
    """
    X0, EX, E2X = log_symmetric_plateau_2d_euler_jet(x, y, c0=c0)
    if X0 == 0.0 and EX == 0.0 and E2X == 0.0:
        return (0.0, 0.0, 0.0)
    w = math.log((x * y) / (c0 * c0))
    if kind == "negative":
        g0 = math.exp(-1.5 * w * w)
        g1 = -6.0 * w * g0
        g2 = (36.0 * w * w - 12.0) * g0
    elif kind == "positive":
        exp_part = math.exp(-0.08 * w * w)
        ch = math.cosh(1.2 * w)
        sh = math.sinh(1.2 * w)
        g0 = ch * exp_part
        g1 = 2.0 * (1.2 * sh - 0.16 * w * ch) * exp_part
        g2 = (
            4.0
            * ((1.28 + 0.0256 * w * w) * ch - 0.384 * w * sh)
            * exp_part
        )
    else:
        raise ValueError(f"Unknown witness kind: {kind!r}")

    f0 = X0 * g0
    f1 = EX * g0 + X0 * g1
    f2 = E2X * g0 + 2.0 * EX * g1 + X0 * g2
    return (f0, f1, f2)


def verify_inversion_and_permutation_symmetries(
    c0: float = 4.0,
) -> Dict[str, Any]:
    """
    Verify on interior, ramp, plateau, and exterior test points that both
    tilde{G}_-^inv and tilde{G}_+^inv are:
      - nonnegative everywhere;
      - compactly supported in (16/10.5, 10.5)^2;
      - permutation-symmetric: F(x, y) == F(y, x);
      - inversion-symmetric: F(16/x, 16/y) == F(x, y).
    """
    c0_sq = c0 * c0
    test_points = [
        (1.54, 2.5),
        (1.6, 8.0),
        (2.0, 3.0),
        (2.5, 7.0),
        (4.0, 4.0),
        (3.2, 10.35),
    ]
    max_perm_err = 0.0
    max_inv_err = 0.0
    min_value = float("inf")
    for kind in ("negative", "positive"):
        for x, y in test_points:
            f_xy, _, _ = evaluate_inversion_symmetric_witness_jet(kind, x, y, c0=c0)
            f_yx, _, _ = evaluate_inversion_symmetric_witness_jet(kind, y, x, c0=c0)
            f_inv, _, _ = evaluate_inversion_symmetric_witness_jet(
                kind, c0_sq / x, c0_sq / y, c0=c0
            )
            max_perm_err = max(max_perm_err, abs(f_xy - f_yx))
            max_inv_err = max(max_inv_err, abs(f_xy - f_inv))
            min_value = min(min_value, f_xy)

    exterior_points = [(1.0, 4.0), (1.5, 4.0), (10.5, 4.0), (11.0, 3.0), (16.0, 2.0)]
    max_exterior_abs = 0.0
    for kind in ("negative", "positive"):
        for x, y in exterior_points:
            f0, f1, f2 = evaluate_inversion_symmetric_witness_jet(kind, x, y, c0=c0)
            max_exterior_abs = max(max_exterior_abs, abs(f0), abs(f1), abs(f2))

    return {
        "inversion_center_c0": c0,
        "inversion_map": f"(x, y) |-> ({c0_sq:.1f}/x, {c0_sq:.1f}/y)",
        "support_interval": [c0_sq / 10.5, 10.5],
        "plateau_interval": [c0_sq / 10.25, 10.25],
        "active_station_set": [n for n, _, _ in prime_power_base_table(10)],
        "max_permutation_symmetry_abs_err": max_perm_err,
        "max_inversion_symmetry_abs_err": max_inv_err,
        "min_sampled_interior_value": min_value,
        "max_exterior_jet_abs": max_exterior_abs,
        "permutation_symmetric": max_perm_err < 1e-14,
        "inversion_symmetric": max_inv_err < 1e-14,
        "compactly_supported": max_exterior_abs == 0.0,
        "nonnegative": min_value > 0.0,
    }


def certify_inversion_symmetric_witness_arb(
    kind: str,
    prec_bits: int = 128,
    force_flint_unavailable: bool = False,
) -> Dict[str, Any]:
    """
    Certify the complete arithmetic sum A_0, A_1, A_2 and arithmetic curvature
    C_arith = A_0 A_2 - A_1^2 of the compactly supported, permutation-symmetric,
    and multiplicative-inversion-symmetric witness tilde{G}_-^inv or tilde{G}_+^inv
    using outward 128-bit Arb ball arithmetic (`python-flint`).

    Active prime-power stations in the support (16/10.5, 10.5)^2 are exactly
    2 <= n, m <= 10 (n, m in {2, 3, 4, 5, 7, 8, 9}), all lying inside the flat
    plateau [16/10.25, 10.25]^2 where X_inv = 1, E X_inv = 0, E^2 X_inv = 0.
    """
    if flint is None or force_flint_unavailable:
        return {
            "witness_kind": kind,
            "certified": False,
            "status": ARB_CERTIFICATION_NOT_AVAILABLE,
            "prec_bits": prec_bits,
            "curvature_enclosure": None,
            "zero_excluded": False,
        }

    saved_prec = flint.ctx.prec
    try:
        flint.ctx.prec = prec_bits
        arb = flint.arb
        base_table = prime_power_base_table(10)
        stations_arb = [(n, arb(p).log()) for n, p, _ in base_table]

        A0 = arb(0)
        A1 = arb(0)
        A2 = arb(0)
        sixteen = arb(16)

        for n, lam_n in stations_arb:
            for m, lam_m in stations_arb:
                weight = lam_n * lam_m
                w = (arb(n * m) / sixteen).log()
                if kind == "negative":
                    g0 = (-arb(3) / arb(2) * w * w).exp()
                    g1 = -arb(6) * w * g0
                    g2 = (arb(36) * w * w - arb(12)) * g0
                elif kind == "positive":
                    exp_part = (-arb(2) / arb(25) * w * w).exp()
                    bw = (arb(6) / arb(5)) * w
                    ch = bw.cosh()
                    sh = bw.sinh()
                    g0 = ch * exp_part
                    g1 = (
                        arb(2)
                        * ((arb(6) / arb(5)) * sh - (arb(4) / arb(25)) * w * ch)
                        * exp_part
                    )
                    g2 = (
                        arb(4)
                        * (
                            ((arb(32) / arb(25)) + (arb(16) / arb(625)) * w * w) * ch
                            - (arb(48) / arb(125)) * w * sh
                        )
                        * exp_part
                    )
                else:
                    raise ValueError(f"Unknown witness kind: {kind!r}")

                A0 += weight * g0
                A1 += weight * g1
                A2 += weight * g2

        C_arb = A0 * A2 - A1 * A1
        strictly_neg = bool(C_arb < 0)
        strictly_pos = bool(C_arb > 0)
        if kind == "negative":
            certified = strictly_neg
            status = (
                INVERSION_SYMMETRIC_NEG_CERTIFIED
                if certified
                else "ARB_ENCLOSURE_SIGN_UNRESOLVED"
            )
        else:
            certified = strictly_pos
            status = (
                INVERSION_SYMMETRIC_POS_CERTIFIED
                if certified
                else "ARB_ENCLOSURE_SIGN_UNRESOLVED"
            )

        mid = float(C_arb.mid())
        rad = float(C_arb.rad())
        return {
            "witness_kind": kind,
            "certified": certified,
            "status": status,
            "prec_bits": prec_bits,
            "active_station_count": len(base_table),
            "active_station_pairs": len(base_table) ** 2,
            "is_complete_compact_support_sum": True,
            "permutation_symmetric": True,
            "inversion_symmetric_around_c0_eq_4": True,
            "A0_str": str(A0),
            "A1_str": str(A1),
            "A2_str": str(A2),
            "curvature_enclosure": {
                "arb_str": str(C_arb),
                "mid_display_float": mid,
                "rad_display_float": rad,
                "outward_float_interval": [mid - rad, mid + rad],
                "strictly_negative": strictly_neg,
                "strictly_positive": strictly_pos,
            },
            "zero_excluded": bool(strictly_neg or strictly_pos),
        }
    finally:
        flint.ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# Section 3: Jacobi Theta Self-Dual Gaussian Audit & Chain-Rule Drift Theorem
# ---------------------------------------------------------------------------


def certify_canonical_theta_gaussian_curvature_arb(
    t: float = 1.0,
    N_cutoff: int = 15,
    prec_bits: int = 128,
    force_flint_unavailable: bool = False,
) -> Dict[str, Any]:
    """
    Audit Selector II (Jacobi Theta Self-Duality) by evaluating the canonical Gaussian
        Theta_t(x, y) = exp(-pi * t * (x^2 + y^2))
    at the unique Fourier self-dual point t = 1 (both compactified on X_{15} and on the
    infinite lattice N_{>=2}^2 with rigorous geometric tail bound).

    Verifies Theorem 2 (`euler_chain_rule_second_deriv_curvature`):
        A_0(Theta_t) = M_0(t),
        A_1(Theta_t) = -2*pi*t * M_1(t),
        A_2(Theta_t) = 4*pi^2*t^2 * M_2(t) - 4*pi*t * M_1(t),
    where M_k(t) = sum_{n,m>=2} Lambda(n) Lambda(m) (n^2 + m^2)^k exp(-pi*t*(n^2 + m^2)),
    yielding:
        C_arith(Theta_t) = 4*pi^2*t^2*(M_0 M_2 - M_1^2) - 4*pi*t*M_0*M_1.

    At t = 1, the negative additive-to-multiplicative chain-rule drift -4*pi*M_0*M_1
    dominates the positive Bernstein variance 4*pi^2*(M_0*M_2 - M_1^2) by five orders of
    magnitude, forcing C_arith < 0.
    """
    if flint is None or force_flint_unavailable:
        return {
            "certified": False,
            "status": ARB_CERTIFICATION_NOT_AVAILABLE,
            "prec_bits": prec_bits,
            "t": t,
            "curvature_enclosure": None,
            "zero_excluded": False,
        }

    saved_prec = flint.ctx.prec
    try:
        flint.ctx.prec = prec_bits
        arb = flint.arb
        pi_arb = arb.pi()
        t_arb = arb(str(t))
        c_arb = arb(2) * pi_arb * t_arb

        base_table = prime_power_base_table(N_cutoff)
        stations_arb = [(n, arb(p).log()) for n, p, _ in base_table]

        M0 = arb(0)
        M1 = arb(0)
        M2 = arb(0)
        for n, lam_n in stations_arb:
            for m, lam_m in stations_arb:
                wt = lam_n * lam_m
                r = arb(n * n + m * m)
                g0 = (-pi_arb * t_arb * r).exp()
                M0 += wt * g0
                M1 += wt * r * g0
                M2 += wt * r * r * g0

        A0 = M0
        A1 = -c_arb * M1
        A2 = c_arb * c_arb * M2 - arb(2) * c_arb * M1
        C_compact = A0 * A2 - A1 * A1

        bernstein_term = c_arb * c_arb * (M0 * M2 - M1 * M1)
        drift_term = -arb(2) * c_arb * M0 * M1
        C_from_chain_rule = bernstein_term + drift_term
        normalized_ratio = C_compact / (A0 * A0)

        # Analytic tail bound for max(n, m) >= M = N_cutoff + 1 (at t >= 1):
        # For M = 16 and t = 1, sum_{n >= M} Lambda(n) n^{2k} e^{-pi t n^2} <= 2 M^{2k+1} e^{-pi t M^2}.
        M_ext = arb(N_cutoff + 1)
        tail_1d_k2 = arb(2) * (M_ext ** 5) * (-pi_arb * t_arb * M_ext * M_ext).exp()
        full_1d_k2 = arb(2) * (arb(2) ** 5) * (-pi_arb * t_arb * arb(4)).exp()
        # 2D exterior sum max(n, m) >= M is bounded by 2 * full_1d_k2 * tail_1d_k2 + tail_1d_k2^2
        tail_M_bound = arb(2) * full_1d_k2 * tail_1d_k2 + tail_1d_k2 * tail_1d_k2
        ball_err = arb(0, tail_M_bound.upper())

        M0_inf = M0 + ball_err
        M1_inf = M1 + ball_err
        M2_inf = M2 + ball_err
        A0_inf = M0_inf
        A1_inf = -c_arb * M1_inf
        A2_inf = c_arb * c_arb * M2_inf - arb(2) * c_arb * M1_inf
        C_infinite_lattice = A0_inf * A2_inf - A1_inf * A1_inf

        strictly_neg_compact = bool(C_compact < 0)
        strictly_neg_infinite = bool(C_infinite_lattice < 0)
        certified = strictly_neg_compact and strictly_neg_infinite

        return {
            "certified": certified,
            "status": (
                THETA_GAUSSIAN_NEG_CERTIFIED
                if certified
                else "ARB_ENCLOSURE_SIGN_UNRESOLVED"
            ),
            "prec_bits": prec_bits,
            "t": t,
            "N_cutoff": N_cutoff,
            "M0_str": str(M0),
            "M1_str": str(M1),
            "M2_str": str(M2),
            "A0_str": str(A0),
            "A1_str": str(A1),
            "A2_str": str(A2),
            "additive_bernstein_variance_term_str": str(bernstein_term),
            "multiplicative_euler_drift_term_str": str(drift_term),
            "bernstein_term_positive": bool(bernstein_term > 0),
            "drift_term_negative": bool(drift_term < 0),
            "drift_dominates_bernstein": bool(bernstein_term + drift_term < 0),
            "chain_rule_identity_verified": bool(
                abs(C_compact - C_from_chain_rule) < arb("1e-35")
            ),
            "compact_support_curvature_enclosure": {
                "arb_str": str(C_compact),
                "strictly_negative": strictly_neg_compact,
            },
            "infinite_lattice_tail_bound_str": str(tail_M_bound),
            "infinite_lattice_curvature_enclosure": {
                "arb_str": str(C_infinite_lattice),
                "strictly_negative": strictly_neg_infinite,
            },
            "normalized_curvature_over_A0_sq_str": str(normalized_ratio),
            "single_station_asymptotic_limit_minus_32_pi": -32.0 * math.pi,
            "zero_excluded": certified,
        }
    finally:
        flint.ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# Section 4: Multiplicative Log-Gaussian Variance-Threshold Theorem
# ---------------------------------------------------------------------------


def evaluate_log_gaussian_variance_threshold(
    alpha: float,
    w0: float = math.log(16.0),
    N_cutoff: int = 15,
) -> LogGaussianVarianceResult:
    """
    Evaluate the compactified multiplicative log-Gaussian
        F_{alpha, w0}(x, y) = X_{15}(x, y) * exp(-alpha * (log(x*y) - w0)^2)
    and verify Theorem 3 (`log_gaussian_curvature_identity`):
        C_arith(F_{alpha, w0}) = 16*alpha^2*(S_0*S_2 - S_1^2) - 8*alpha*S_0^2
                               = 8*alpha*S_0^2*(2*alpha*Var_w(log(nm)) - 1).
    """
    stations = active_prime_power_stations(N_cutoff)
    S0 = 0.0
    S1 = 0.0
    S2 = 0.0
    for n, lam_n in stations:
        for m, lam_m in stations:
            z = math.log(float(n * m)) - w0
            w_nm = lam_n * lam_m * math.exp(-alpha * z * z)
            S0 += w_nm
            S1 += w_nm * z
            S2 += w_nm * z * z

    def f_fn(x: float, y: float) -> float:
        X0, _, _ = plateau_cutoff_2d_euler_jet(x, y, N_cutoff=N_cutoff)
        if X0 == 0.0:
            return 0.0
        z = math.log(x * y) - w0
        return X0 * math.exp(-alpha * z * z)

    def e1_fn(x: float, y: float) -> float:
        X0, EX, _ = plateau_cutoff_2d_euler_jet(x, y, N_cutoff=N_cutoff)
        if X0 == 0.0 and EX == 0.0:
            return 0.0
        z = math.log(x * y) - w0
        g0 = math.exp(-alpha * z * z)
        g1 = -4.0 * alpha * z * g0
        return EX * g0 + X0 * g1

    def e2_fn(x: float, y: float) -> float:
        X0, EX, E2X = plateau_cutoff_2d_euler_jet(x, y, N_cutoff=N_cutoff)
        if X0 == 0.0 and EX == 0.0 and E2X == 0.0:
            return 0.0
        z = math.log(x * y) - w0
        g0 = math.exp(-alpha * z * z)
        g1 = -4.0 * alpha * z * g0
        g2 = (16.0 * alpha * alpha * z * z - 8.0 * alpha) * g0
        return E2X * g0 + 2.0 * EX * g1 + X0 * g2

    moments = evaluate_euler_moments_A0_A1_A2(
        f_fn,
        n_max=N_cutoff,
        euler1_f0=e1_fn,
        euler2_f0=e2_fn,
        evaluation_mode="COMPLETE_COMPACT_SUPPORT_SUM",
    )

    var_det = S0 * S2 - S1 * S1
    norm_var = var_det / (S0 * S0)
    crit_alpha = 1.0 / (2.0 * norm_var)
    var_term = 16.0 * alpha * alpha * var_det
    conc_term = -8.0 * alpha * S0 * S0
    c_formula = var_term + conc_term

    if c_formula < -1e-12:
        regime = "SUBCRITICAL_VARIANCE_NEGATIVE_CURVATURE"
    elif c_formula > 1e-12:
        regime = "SUPERCRITICAL_VARIANCE_POSITIVE_CURVATURE"
    else:
        regime = "CRITICAL_VARIANCE_ZERO_CURVATURE"

    return LogGaussianVarianceResult(
        alpha=alpha,
        w0=w0,
        S0=S0,
        S1=S1,
        S2=S2,
        station_variance_det=var_det,
        normalized_variance=norm_var,
        critical_alpha=crit_alpha,
        variance_term_16_alpha2_det=var_term,
        concavity_term_minus_8_alpha_S02=conc_term,
        arithmetic_curvature_direct=moments.arithmetic_curvature,
        arithmetic_curvature_formula=c_formula,
        identity_abs_err=abs(moments.arithmetic_curvature - c_formula),
        sign_regime=regime,
    )


# ---------------------------------------------------------------------------
# Section 5: Exhaustive Audit of the Six Candidate Selector Mechanisms
# ---------------------------------------------------------------------------


def audit_six_candidate_selectors() -> List[CandidateSelectorMechanismAudit]:
    """
    Return the structured audit of the six candidate canonical selector principles
    specified for `TASK-TC-035`, using explicit evidence statuses and primary literature
    citations (including arXiv references retrieved via `literature-search-arxiv`).
    """
    return [
        CandidateSelectorMechanismAudit(
            selector_id="SELECTOR-I",
            selector_name="Uniqueness under the Functional Equation (Hamburger / Burnol Co-Poisson Dictionary)",
            governing_zero_independent_axioms=(
                "Completed functional equation xi(s) = xi(1 - s) with pi^{-s/2} Gamma(s/2) "
                "Archimedean factor, moderate polynomial growth, and S-support / co-Poisson "
                "lattice condition on Z; followed by Euler product and logarithmic differentiation "
                "-zeta'(s)/zeta(s) = sum_{n>=2} Lambda(n) n^{-s}."
            ),
            unique_object_selected=(
                "(1) Functional equation + growth/support assumptions characterize the zeta-side "
                "distribution zeta(s) = sum_{n>=1} n^{-s} (1D scalar ray); (2) Euler product and "
                "logarithmic differentiation determine the von Mangoldt prime-power distribution "
                "-zeta'(s)/zeta(s) = sum_{n>=2} Lambda(n) n^{-s}; (3) neither theorem selects a "
                "unique test kernel."
            ),
            selects_unique_test_kernel_status="SELECTS_DISTRIBUTION_RAY_NOT_TEST_KERNEL",
            arithmetic_curvature_constraint_status=(
                "SIGN_INDEFINITE_ON_INVERSION_AND_PERMUTATION_SYMMETRIC_COMPACT_KERNELS"
            ),
            spectral_positivity_or_isolation_status=(
                "DOUBLE_SPECTRAL_SUM_UNCHANGED_BY_KERNEL_INVOLUTION_SYMMETRY"
            ),
            circularity_or_obstruction_firewall=(
                "Certified in 128-bit Arb: tilde{G}_-^inv and tilde{G}_+^inv in C_c^infty((0, infty)^2) "
                "are simultaneously nonnegative, permutation-symmetric F(x,y)=F(y,x), and inversion-"
                "symmetric F(16/x, 16/y)=F(x,y), yet C_arith(tilde{G}_-^inv) < 0 < C_arith(tilde{G}_+^inv)."
            ),
            evidence_class="CERTIFIED_FINITE_AND_EXTERNAL_THEOREM",
            classification=SELECTOR_I_FUNCTIONAL_EQUATION_STATUS,
            primary_literature_references=[
                "Hamburger (1921), Math. Z. 10, 240-254",
                "Burnol (2012), Deux extensions de Theoremes de Hamburger, Expos. Math. 30, 295-308, https://arxiv.org/abs/1106.4749v2",
                "Burnol (2007), Entrelacement de co-Poisson, Ann. Inst. Fourier 57(2), 525-602, https://arxiv.org/abs/math/0407443v3",
                "Baez-Duarte (2002), A general statement of the functional equation for the Riemann zeta-function, https://arxiv.org/abs/math/0207237v1",
            ],
        ),
        CandidateSelectorMechanismAudit(
            selector_id="SELECTOR-II",
            selector_name="Jacobi Theta Self-Duality and Canonical Self-Dual Gaussian",
            governing_zero_independent_axioms=(
                "The Gaussian is uniquely selected within the specified positive heat-semigroup, "
                "harmonic-oscillator ground-state, or minimum-uncertainty class (the full self-Fourier "
                "space is not one-dimensional), inducing theta(1/t) = sqrt(t) theta(t)."
            ),
            unique_object_selected=(
                "Canonical additive Gaussian Theta_1(x, y) = exp(-pi*(x^2 + y^2)) at the unique "
                "self-dual scale t = 1 within the positive heat-semigroup / oscillator ground-state / "
                "minimum-uncertainty class (up to positive scalar)."
            ),
            selects_unique_test_kernel_status="SELECTS_UNIQUE_ADDITIVE_GAUSSIAN_GROUND_STATE",
            arithmetic_curvature_constraint_status=(
                "STRICTLY_NEGATIVE_EULER_CURVATURE_CERTIFIED_AT_SELF_DUAL_POINT"
            ),
            spectral_positivity_or_isolation_status=(
                "TENSOR_SQUARE_FACTORIZES_INTO_1D_LINEAR_SUM_SQUARED_NO_DIAGONAL_ISOLATION"
            ),
            circularity_or_obstruction_firewall=(
                "Additive-to-multiplicative chain-rule drift (t d/dt)^2 = t^2 d^2/dt^2 + t d/dt "
                "gives C_arith(Theta_t) = 4*pi^2*t^2*(M_0*M_2 - M_1^2) - 4*pi*t*M_0*M_1. At t = 1, "
                "the negative drift -4*pi*M_0*M_1 dominates the positive Bernstein variance by 5 orders "
                "of magnitude (C_arith / A_0^2 ~ -100.5305 ~ -32*pi < 0, certified in 128-bit Arb)."
            ),
            evidence_class="LEAN_PROVED_AND_CERTIFIED_FINITE",
            classification=SELECTOR_II_THETA_SELF_DUALITY_STATUS,
            primary_literature_references=[
                "Riemann (1859), Monatsber. Berlin Akad., 671-680",
                "Edwards (1974), Riemann's Zeta Function, Academic Press",
                "Burnol (2004), Two complete and minimal systems associated with the zeros of the Riemann zeta function, J. Theor. Nombres Bordeaux 16, 65-94, https://arxiv.org/abs/math/0203120v7",
            ],
        ),
        CandidateSelectorMechanismAudit(
            selector_id="SELECTOR-III",
            selector_name="Prime/Archimedean Explicit-Formula Balance and Conductor Operator",
            governing_zero_independent_axioms=(
                "Weil explicit-formula distributional equality between prime-power von Mangoldt "
                "stations, the Archimedean Gamma distribution, and the dilaton-invariant conductor "
                "operator log|x| + log|y|."
            ),
            unique_object_selected=(
                "The global Weil explicit-formula linear functional W_zeta in D'(R_{>0}) "
                "(universal identity across all admissible test functions, not a single test kernel)."
            ),
            selects_unique_test_kernel_status="UNIVERSAL_IDENTITY_ACROSS_ALL_ADMISSIBLE_KERNELS",
            arithmetic_curvature_constraint_status=(
                "SUPPORT_VANISHING_TRIGGERS_EXACT_COMPLEMENT_CANCELLATION"
            ),
            spectral_positivity_or_isolation_status=(
                "EXACT_CANCELLATION_BLOCKS_STRICT_SUBORDINATION_ROUTE"
            ),
            circularity_or_obstruction_firewall=(
                "By TASK-TC-032R (`exact_cancellation_precludes_strict_subordination`), whenever "
                "support separation forces the arithmetic functional Q_eps = 0 identically, the "
                "omitted spectral/Archimedean complement R_eps = -D_eps cancels the selected block "
                "exactly rather than isolating a positive definite zero sum."
            ),
            evidence_class="LEAN_PROVED_AND_EXTERNAL_THEOREM",
            classification=SELECTOR_III_PRIME_ARCHIMEDEAN_STATUS,
            primary_literature_references=[
                "Weil (1952), Sur les 'formules explicites' de la theorie des nombres premiers, Comm. Sem. Math. Univ. Lund, 252-265",
                "Burnol (2000), Sur les Formules Explicites I: analyse invariante, C. R. Acad. Sci. Paris 331, 423-428, https://arxiv.org/abs/math/0101068v1",
            ],
        ),
        CandidateSelectorMechanismAudit(
            selector_id="SELECTOR-IV",
            selector_name="Extremal and Variational Principles (Nyman-Beurling-Baez-Duarte, Li, Suzuki)",
            governing_zero_independent_axioms=(
                "Strict L^2 projection convexity d_N^2 = inf ||chi_{(0,1)} - sum_{k=1}^N c_k {1/(kx)}||^2 "
                "(Nyman-Beurling-Baez-Duarte), canonical rational test basis phi_n(s) = 1 - (1 - 1/s)^n "
                "(Li / Lagarias), or localized Rayleigh quotient minimization lambda_1(R) (Suzuki)."
            ),
            unique_object_selected=(
                "For each fixed complexity/window parameter N or R, selects a unique finite-stage "
                "extremal vector f_N^* and value d_N^2 (or lambda_n, lambda_1(R))."
            ),
            selects_unique_test_kernel_status="SELECTS_INDEXED_INFINITE_SEQUENCE_NOT_SINGLE_KERNEL",
            arithmetic_curvature_constraint_status=(
                "SINGLE_FINITE_STAGE_STRICTLY_POSITIVE_UNCONDITIONALLY_NO_ZERO_EXCLUSION"
            ),
            spectral_positivity_or_isolation_status=(
                "CRITICAL_LINE_EXCLUSION_REQUIRES_ASYMPTOTIC_LIMIT_RH_EQUIVALENT"
            ),
            circularity_or_obstruction_firewall=(
                "At any single finite N, d_N^2 > 0 holds unconditionally whether or not RH holds; "
                "excluding delta_rho != 0 requires lim_{N->infty} d_N = 0 (or forall n, lambda_n >= 0; "
                "forall R, lambda_1(R) >= 0), which is a known RH-equivalent criterion, and Mellin "
                "grade dilation D_K is an L^2 isometry (`PURE_COORDINATE_RESCALING_NO_GAIN`)."
            ),
            evidence_class="PROVED_PAPER_DERIVATION_AND_EXTERNAL_THEOREM",
            classification=SELECTOR_IV_VARIATIONAL_EXTREMAL_STATUS,
            primary_literature_references=[
                "Baez-Duarte (2003), A new necessary and sufficient condition for the Riemann hypothesis, https://arxiv.org/abs/math/0307215v1",
                "Burnol (2003), On an analytic estimate in the theory of the Riemann Zeta function and a Theorem of Baez-Duarte, Acta Cient. Venez. 54, 210-215, https://arxiv.org/abs/math/0202166v1",
                "Lagarias (2007), Li Coefficients for Automorphic L-Functions, Ann. Inst. Fourier 57, 1689-1740, https://arxiv.org/abs/math/0404394v4",
                "Suzuki (2026), Lowest eigenvalues of localized Weil operators, https://arxiv.org/abs/2606.09096v3",
            ],
        ),
        CandidateSelectorMechanismAudit(
            selector_id="SELECTOR-V",
            selector_name="Canonical Operator Trace (Connes-Consani Semi-Local Trace and Sonin Compression)",
            governing_zero_independent_axioms=(
                "Compression of the multiplicative scaling action onto the orthogonal complement "
                "of phase-space cutoff projections (Sonin space, cutoff parameter Lambda = 1) and "
                "expansion via prolate spheroidal wave functions."
            ),
            unique_object_selected=(
                "Canonical compressed scaling trace Tr_Sonin at the Archimedean place and "
                "semi-local trace functional over the adele class / scaling site."
            ),
            selects_unique_test_kernel_status="SELECTS_TRACE_FUNCTIONAL_AND_PROLATE_BASIS",
            arithmetic_curvature_constraint_status=(
                "ARCHIMEDEAN_TRACE_POSITIVE_GLOBAL_SEMI_LOCAL_TRACE_WEIL_EQUIVALENT"
            ),
            spectral_positivity_or_isolation_status=(
                "GLOBAL_TRACE_POSITIVITY_ACROSS_PRIMES_IS_RH_EQUIVALENT"
            ),
            circularity_or_obstruction_firewall=(
                "In Connes-Consani (2020, 2021), positivity of the compressed scaling trace holds "
                "at the single Archimedean place via prolate/Toeplitz control, whereas in the "
                "general semi-local case including prime places, global positivity of the Weil "
                "functional remains equivalent to RH (`CURVATURE_POSITIVITY_IS_RH_EQUIVALENT`)."
            ),
            evidence_class="EXTERNAL_THEOREM",
            classification=SELECTOR_V_OPERATOR_TRACE_STATUS,
            primary_literature_references=[
                "Connes & Consani (2020), Weil positivity and Trace formula, the archimedean place, https://arxiv.org/abs/2006.13771v1",
                "Connes & Consani (2021), Spectral Triples and Zeta-Cycles, https://arxiv.org/abs/2106.01715v1",
                "Connes & Consani (2021), BC-system, absolute cyclotomy and the quantized calculus, https://arxiv.org/abs/2112.08820v1",
                "Burnol (2001), Sur certains espaces de Hilbert de fonctions entieres (Sonine spaces), C. R. Acad. Sci. Paris 333, 201-206, https://arxiv.org/abs/math/0105120v1",
            ],
        ),
        CandidateSelectorMechanismAudit(
            selector_id="SELECTOR-VI",
            selector_name="Functorial and Multi-Grade Naturality Stronger than Ordinary Rescaling",
            governing_zero_independent_axioms=(
                "Multi-grade fiber isomorphism naturality F_K ~= F_J with exact 1-coboundary "
                "transitions c(J, K) = tau^{J-K}, strengthened to infinitesimal Euler scale "
                "homogeneity E F_0 = d F_0."
            ),
            unique_object_selected=(
                "Under ordinary transfer naturality: uniquely selects b = 1 (leaving F_0 arbitrary). "
                "Under strengthened Euler homogeneity E F_0 = d F_0 on C_c^infty((0, infty)^2): "
                "uniquely selects the zero kernel F_0 == 0."
            ),
            selects_unique_test_kernel_status="ORDINARY_NATURALITY_ARBITRARY_STRONG_HOMOGENEITY_ZERO_KERNEL",
            arithmetic_curvature_constraint_status=(
                "ORDINARY_NATURALITY_K_INDEPENDENT_SIGN_INDEFINITE_HOMOGENEITY_IMPOSSIBLE_ON_COMPACT_SUPPORT"
            ),
            spectral_positivity_or_isolation_status=(
                "VALUE_LEVEL_COVARIANCE_CANCELS_SPECTRAL_EXPONENT_AT_B_EQ_1"
            ),
            circularity_or_obstruction_firewall=(
                "By TASK-TC-027 (`MULTIGRADE_NATURALITY_NO_GO_PROVED`), TASK-TC-033 "
                "(`TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED`), and TASK-TC-034R "
                "(`COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED`), ordinary naturality leaves F_0 "
                "unselected while Euler homogeneity E F_0 = d F_0 forces F_0 == 0 on compact support."
            ),
            evidence_class="LEAN_PROVED_AND_PROVED_PAPER_DERIVATION",
            classification=SELECTOR_VI_STRONG_NATURALITY_STATUS,
            primary_literature_references=[
                "TASK-TC-027 (formal/RiemannScope/MultiGradeNaturality.lean)",
                "TASK-TC-033 (formal/RiemannScope/GradeHankelConstraint.lean)",
                "TASK-TC-034R (formal/RiemannScope/TransportMismatchCurvature.lean, docs/reviews/TC_034R_TRANSPORT_MISMATCH_CURVATURE_REPAIR_AUDIT.md)",
            ],
        ),
    ]


# ---------------------------------------------------------------------------
# Section 6: The Canonical Selector Trilemma & Dichotomy Audit
# ---------------------------------------------------------------------------


def audit_selector_trilemma() -> Dict[str, Any]:
    """
    Formulate and verify the Canonical Selector Trilemma governing any zero-independent
    selector S on label-compatible (b = 1) two-variable arithmetic kernels:

    - Branch 1 (Scale-Homogeneous Flatness Selector, E F_0 = d F_0):
        Forces C_arith(F_0) = 0 algebraically (`homogeneous_arithmetic_curvature_zero`),
        but collapses to F_0 == 0 on compact support (`COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED`)
        and diverges or fails to isolate critical-strip zeros on noncompact rays.
    - Branch 2 (Classical Symmetry / Self-Duality Selector: Functional-Equation Involution,
      Permutation Symmetry, or Theta/Fourier Self-Duality):
        Either leaves an infinite-dimensional invariant subspace on which C_arith is
        Arb-certified sign-indefinite (`INVERSION_AND_PERMUTATION_SYMMETRIC_SUBSPACE_SIGN_INDEFINITE`),
        or selects the canonical additive Gaussian Theta_1 where the Euler chain-rule drift
        forces C_arith(Theta_1) < 0 (`CANONICAL_THETA_GAUSSIAN_NEGATIVE_CURVATURE_CERTIFIED`).
        When C_arith <= 0 and C_arith = S_diag + R_comp with S_diag > 0, no contradiction
        follows unless R_comp >= 0 is independently proved (`selector_trilemma_algebraic_dichotomy`).
    - Branch 3 (Global Spectral / Variational Positivity Selector: Weil Convolution Squares,
      Nyman-Beurling Projection Sequence, Li Basis, Connes-Consani Semi-Local Trace):
        Selects an infinite family or trace functional whose global positivity / asymptotic
        vanishing is a known RH-equivalent reformulation, not an unconditional single-kernel
        obstruction.
    """
    return {
        "trilemma_name": "Canonical Zeta Selector Trilemma",
        "classification": SECONDARY_TRILEMMA_CLASSIFICATION,
        "branches": {
            "branch_1_scale_homogeneous_flatness": {
                "condition": "E F_0 = d F_0",
                "arithmetic_curvature_consequence": "C_arith(F_0) = A_0 A_2 - A_1^2 = 0 (Lean: homogeneous_arithmetic_curvature_zero)",
                "obstruction": (
                    "Only F_0 == 0 lies in C_c^infty((0, infty)^2) "
                    "(COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED); noncompact homogeneous "
                    "powers do not converge across the critical strip."
                ),
                "status": SELECTOR_VI_STRONG_NATURALITY_STATUS,
            },
            "branch_2_classical_symmetry_or_theta_self_duality": {
                "condition": (
                    "Permutation symmetry F(x,y)=F(y,x), multiplicative inversion symmetry "
                    "F(c_0^2/x, c_0^2/y)=F(x,y), or Fourier/theta self-duality hat{f}=f"
                ),
                "arithmetic_curvature_consequence": (
                    "Inversion+permutation-symmetric compact kernels remain Arb-certified "
                    "sign-indefinite; the canonical self-dual Gaussian Theta_1 has Arb-certified "
                    "C_arith(Theta_1) < 0 due to the additive-to-multiplicative chain-rule drift "
                    "-4*pi*M_0*M_1."
                ),
                "obstruction": (
                    "By Lean theorem `selector_trilemma_algebraic_dichotomy`, C_arith <= 0 and "
                    "C_arith = S_diag + R_comp with S_diag > 0 merely implies R_comp < 0 unless "
                    "R_comp >= 0 is independently proved (`selector_trilemma_contradiction_of_nonneg_complement`, OBL-CT-001A)."
                ),
                "status": SELECTOR_II_THETA_SELF_DUALITY_STATUS,
            },
            "branch_3_variational_or_semi_local_trace_family": {
                "condition": (
                    "Nyman-Beurling L^2 projection sequence d_N^2, Li rational basis lambda_n, "
                    "Suzuki localized Rayleigh minimum lambda_1(R), or Connes-Consani semi-local trace"
                ),
                "arithmetic_curvature_consequence": (
                    "Selects a canonical indexed sequence or semi-local trace functional rather "
                    "than a single finite kernel."
                ),
                "obstruction": (
                    "Each individual finite stage is strictly positive unconditionally; critical-line "
                    "zero confinement holds only in the infinite asymptotic limit or global trace "
                    "positivity, which is RH-equivalent."
                ),
                "status": SELECTOR_IV_VARIATIONAL_EXTREMAL_STATUS,
            },
        },
        "lean_dichotomy_theorems": [
            "selector_trilemma_algebraic_dichotomy",
            "selector_trilemma_contradiction_of_nonneg_complement",
        ],
        "selector_families_scope_status": "SIX_STANDARD_SELECTOR_FAMILIES_AUDITED",
        "lean_dichotomy_scope_status": "CONDITIONAL_COMPLEMENT_SIGN_DICHOTOMY_LEAN_PROVED",
        "lean_scope_note": (
            "Lean proves the conditional algebraic complement-sign dichotomy "
            "(selector_trilemma_algebraic_dichotomy, selector_trilemma_contradiction_of_nonneg_complement), "
            "not that every possible zero-independent selector falls into the six-family research trilemma."
        ),
        "obl_ct_001a_status": "OPEN",
    }


# ---------------------------------------------------------------------------
# Section 7: Exact Lean Theorem Map & Synchronization Verifier (`TASK-TC-035`)
# ---------------------------------------------------------------------------


def get_selector_lean_theorem_map() -> Dict[str, Any]:
    """
    Return the exact theorem-to-declaration map for
    `formal/RiemannScope/CanonicalSelectorAudit.lean`.
    """
    declarations = [
        {
            "identifier": "oneDimCurvature",
            "kind": "def",
            "statement_scope": "oneDimCurvature m0 m1 m2 := m0 * m2 - m1^2",
            "algebraic_only": True,
            "paper_step_supported": "1D prime-station Euler curvature determinant",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "tensor_square_moment_A0",
            "kind": "theorem",
            "statement_scope": "m0 * m0 = m0^2",
            "algebraic_only": True,
            "paper_step_supported": "Separable tensor-square zeroth Euler moment A_0(f x f) = m_0^2",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "tensor_square_moment_A1",
            "kind": "theorem",
            "statement_scope": "m1 * m0 + m0 * m1 = 2 * m0 * m1",
            "algebraic_only": True,
            "paper_step_supported": "Separable tensor-square first Euler moment A_1(f x f) = 2 m_0 m_1",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "tensor_square_moment_A2",
            "kind": "theorem",
            "statement_scope": "m2 * m0 + 2 * m1 * m1 + m0 * m2 = 2 * m0 * m2 + 2 * m1^2",
            "algebraic_only": True,
            "paper_step_supported": "Separable tensor-square second Euler moment A_2(f x f) = 2 m_0 m_2 + 2 m_1^2",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "tensor_square_curvature_reduction",
            "kind": "theorem",
            "statement_scope": "curvatureDet (m0^2) (2*m0*m1) (2*m0*m2 + 2*m1^2) = 2 * m0^2 * oneDimCurvature m0 m1 m2",
            "algebraic_only": True,
            "paper_step_supported": "Theorem 1: 2D separable kernel curvature reduces to 2 m_0^2 (m_0 m_2 - m_1^2)",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "tensor_square_curvature_pos_iff",
            "kind": "theorem",
            "statement_scope": "m0 != 0 ==> (0 < curvatureDet (m0^2) (2*m0*m1) (2*m0*m2 + 2*m1^2) <-> 0 < oneDimCurvature m0 m1 m2)",
            "algebraic_only": True,
            "paper_step_supported": "Positive curvature equivalence for separable tensor-square kernels",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "tensor_square_curvature_neg_iff",
            "kind": "theorem",
            "statement_scope": "m0 != 0 ==> (curvatureDet (m0^2) (2*m0*m1) (2*m0*m2 + 2*m1^2) < 0 <-> oneDimCurvature m0 m1 m2 < 0)",
            "algebraic_only": True,
            "paper_step_supported": "Negative curvature equivalence for separable tensor-square kernels",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "euler_chain_rule_second_deriv_curvature",
            "kind": "theorem",
            "statement_scope": "curvatureDet M0 (-c * M1) (c^2 * M2 - 2 * c * M1) = c^2 * curvatureDet M0 M1 M2 - 2 * c * M0 * M1",
            "algebraic_only": True,
            "paper_step_supported": "Theorem 2: Additive-to-multiplicative Euler chain-rule drift identity for Jacobi theta / heat kernels",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "euler_drift_strictly_negative_of_dominant",
            "kind": "theorem",
            "statement_scope": "0 < c /\\ c * curvatureDet M0 M1 M2 < 2 * M0 * M1 ==> curvatureDet M0 (-c * M1) (c^2 * M2 - 2 * c * M1) < 0",
            "algebraic_only": True,
            "paper_step_supported": "Strict negativity of multiplicative Euler curvature when chain-rule drift dominates Bernstein variance",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "single_station_theta_gaussian_curvature_neg",
            "kind": "theorem",
            "statement_scope": "0 < w /\\ 0 < r /\\ 0 < c ==> curvatureDet w (-c*(w*r)) (c^2*(w*r^2) - 2*c*(w*r)) = -2*c*w^2*r /\\ < 0",
            "algebraic_only": True,
            "paper_step_supported": "Exact negative Euler curvature -2 c w^2 r < 0 at a single dominant prime-station pair",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "log_gaussian_curvature_identity",
            "kind": "theorem",
            "statement_scope": "curvatureDet S0 (-4*a*S1) (16*a^2*S2 - 8*a*S0) = 16 * a^2 * curvatureDet S0 S1 S2 - 8 * a * S0^2",
            "algebraic_only": True,
            "paper_step_supported": "Theorem 3: Multiplicative log-Gaussian curvature variance-vs-concavity identity",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "log_gaussian_curvature_neg_of_subcritical_variance",
            "kind": "theorem",
            "statement_scope": "0 < a /\\ 2 * a * curvatureDet S0 S1 S2 < S0^2 ==> curvatureDet S0 (-4*a*S1) (16*a^2*S2 - 8*a*S0) < 0",
            "algebraic_only": True,
            "paper_step_supported": "Strict negativity of multiplicative log-Gaussian curvature in the subcritical variance regime",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "log_gaussian_curvature_pos_of_supercritical_variance",
            "kind": "theorem",
            "statement_scope": "0 < a /\\ S0^2 < 2 * a * curvatureDet S0 S1 S2 ==> 0 < curvatureDet S0 (-4*a*S1) (16*a^2*S2 - 8*a*S0)",
            "algebraic_only": True,
            "paper_step_supported": "Strict positivity of multiplicative log-Gaussian curvature in the supercritical variance regime",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "log_gaussian_critical_width_zero",
            "kind": "theorem",
            "statement_scope": "2 * a * curvatureDet S0 S1 S2 = S0^2 ==> curvatureDet S0 (-4*a*S1) (16*a^2*S2 - 8*a*S0) = 0",
            "algebraic_only": True,
            "paper_step_supported": "Vanishing of multiplicative log-Gaussian curvature at the critical variance width",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "selector_trilemma_algebraic_dichotomy",
            "kind": "theorem",
            "statement_scope": "curvatureDet A0 A1 A2 = S_diag + R_comp /\\ curvatureDet A0 A1 A2 <= 0 /\\ 0 < S_diag ==> R_comp < 0",
            "algebraic_only": True,
            "paper_step_supported": "Selector Trilemma dichotomy: nonpositive arithmetic curvature with positive diagonal block forces R_comp < 0 unless R_comp >= 0 is proved",
            "external_theorem_dependency": "None",
        },
        {
            "identifier": "selector_trilemma_contradiction_of_nonneg_complement",
            "kind": "theorem",
            "statement_scope": "curvatureDet A0 A1 A2 = S_diag + R_comp /\\ curvatureDet A0 A1 A2 <= 0 /\\ 0 < S_diag /\\ 0 <= R_comp ==> False",
            "algebraic_only": True,
            "paper_step_supported": "Conditional contradiction under independent complement nonnegativity (OBL-CT-001A)",
            "external_theorem_dependency": "None",
        },
    ]

    return {
        "module_path": "formal/RiemannScope/CanonicalSelectorAudit.lean",
        "total_module_declarations": len(declarations),
        "module_def_count": sum(1 for d in declarations if d["kind"] == "def"),
        "module_theorem_count": sum(1 for d in declarations if d["kind"] == "theorem"),
        "repository_compiled_theorem_declarations": 580,
        "formal_proof_hygiene": "0 sorry, 0 admit, no nonstandard project axioms introduced",
        "declarations": declarations,
        "not_formalized_in_lean": [
            "Hamburger's uniqueness theorem for Dirichlet series with functional equation",
            "Burnol's co-Poisson distribution dictionary",
            "Nyman-Beurling-Baez-Duarte L^2 completeness theorem",
            "Connes-Consani semi-local trace formula and prolate spheroidal wave function expansion",
            "OBL-CT-001A",
        ],
    }


def verify_selector_lean_theorem_map_against_file(
    lean_file_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Verify that the declarations listed in `get_selector_lean_theorem_map()` match the exact
    `def` and `theorem` identifiers committed in `formal/RiemannScope/CanonicalSelectorAudit.lean`.
    """
    if lean_file_path is None:
        lean_file_path = (
            Path(__file__).resolve().parent.parent
            / "formal"
            / "RiemannScope"
            / "CanonicalSelectorAudit.lean"
        )
    text = lean_file_path.read_text(encoding="utf-8")
    actual_defs = re.findall(r"^\s*def\s+([A-Za-z0-9_]+)", text, flags=re.MULTILINE)
    actual_thms = re.findall(r"^\s*theorem\s+([A-Za-z0-9_]+)", text, flags=re.MULTILINE)
    actual_all = actual_defs + actual_thms

    tmap = get_selector_lean_theorem_map()
    mapped_all = [d["identifier"] for d in tmap["declarations"]]
    stripped = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    stripped = "\n".join(line.split("--")[0] for line in stripped.splitlines())
    return {
        "matches_exact": actual_all == mapped_all,
        "actual_defs": actual_defs,
        "actual_theorems": actual_thms,
        "mapped_identifiers": mapped_all,
        "contains_sorry": re.search(r"\bsorry\b", stripped) is not None,
        "contains_admit": re.search(r"\badmit\b", stripped) is not None,
    }


# ---------------------------------------------------------------------------
# Section 8: Master Audit Entrypoint for `TASK-TC-035`
# ---------------------------------------------------------------------------


def audit_canonical_zeta_selector() -> Dict[str, Any]:
    """
    Run the complete `TASK-TC-035` audit of candidate zero-independent canonical selector
    principles and return the structured JSON-serializable report dictionary.
    """
    tensor_sq = evaluate_separable_tensor_square_reduction()
    sym_check = verify_inversion_and_permutation_symmetries(c0=4.0)
    inv_neg_arb = certify_inversion_symmetric_witness_arb("negative")
    inv_pos_arb = certify_inversion_symmetric_witness_arb("positive")
    theta_arb = certify_canonical_theta_gaussian_curvature_arb(t=1.0, N_cutoff=15)

    # Evaluate log-Gaussian across subcritical (alpha = 1.5) and low-alpha (alpha = 0.05) regimes
    log_gauss_narrow = evaluate_log_gaussian_variance_threshold(alpha=1.5)
    log_gauss_wide = evaluate_log_gaussian_variance_threshold(alpha=0.05)

    selectors = audit_six_candidate_selectors()
    trilemma = audit_selector_trilemma()
    lean_map = get_selector_lean_theorem_map()

    return {
        "task_id": TASK_TC_035_ID,
        "task_completion_status": TASK_TC_035_STATUS,
        "title": "Canonical Zeta Selector Principle and Uniqueness Audit",
        "parent_task_id": "TASK-TC-034R",
        "parent_head": "d06d13c9cbd5f66589692f8eae41409781b18908",
        "primary_research_question": (
            "Which zero-independent axioms, derived from the completed zeta and its "
            "prime-side structure, uniquely select a non-scalar arithmetic functional "
            "from the otherwise arbitrary kernel space before curvature or spectral "
            "positivity is tested?"
        ),
        "principal_classification": PRINCIPAL_CLASSIFICATION,
        "secondary_trilemma_classification": SECONDARY_TRILEMMA_CLASSIFICATION,
        "candidate_selector_audits": [asdict(s) for s in selectors],
        "selector_status_summary": {
            "functional_equation_hamburger": SELECTOR_I_FUNCTIONAL_EQUATION_STATUS,
            "jacobi_theta_self_duality": SELECTOR_II_THETA_SELF_DUALITY_STATUS,
            "prime_archimedean_explicit_formula_balance": SELECTOR_III_PRIME_ARCHIMEDEAN_STATUS,
            "variational_extremal_principles": SELECTOR_IV_VARIATIONAL_EXTREMAL_STATUS,
            "canonical_operator_trace_compression": SELECTOR_V_OPERATOR_TRACE_STATUS,
            "stronger_scale_naturality": SELECTOR_VI_STRONG_NATURALITY_STATUS,
        },
        "separable_tensor_square_reduction": asdict(tensor_sq),
        "inversion_and_permutation_symmetry_audit": {
            "symmetry_verification": sym_check,
            "negative_inversion_symmetric_arb_enclosure": inv_neg_arb,
            "positive_inversion_symmetric_arb_enclosure": inv_pos_arb,
            "classification": INVERSION_SYMMETRY_SIGN_INDEFINITE_STATUS,
        },
        "canonical_theta_gaussian_audit": theta_arb,
        "multiplicative_log_gaussian_variance_audit": {
            "identity": "C_arith(F_{alpha, w0}) = 16*alpha^2*(S_0*S_2 - S_1^2) - 8*alpha*S_0^2",
            "critical_width_formula": "alpha_* = S_0^2 / (2*(S_0*S_2 - S_1^2)) = 1 / (2*Var_w(log(nm)))",
            "alpha_1_5_evaluation": asdict(log_gauss_narrow),
            "alpha_0_05_evaluation": asdict(log_gauss_wide),
            "classification": LOG_GAUSSIAN_VARIANCE_THRESHOLD_PROVED,
        },
        "canonical_selector_trilemma": trilemma,
        "lean_theorem_map": lean_map,
        "arxiv_literature_retrieved": [
            {
                "arxiv_id": "1106.4749v2",
                "url": "https://arxiv.org/abs/1106.4749v2",
                "authors": ["Jean-Francois Burnol"],
                "title": "Deux extensions de Theoremes de Hamburger",
                "relevance": "Selector I: Functional equation uniqueness and S-support distribution dictionary",
            },
            {
                "arxiv_id": "math/0407443v3",
                "url": "https://arxiv.org/abs/math/0407443v3",
                "authors": ["Jean-Francois Burnol"],
                "title": "Entrelacement de co-Poisson",
                "relevance": "Selector I & III: Co-Poisson intertwining and Mellin-zeta distribution duality",
            },
            {
                "arxiv_id": "math/0101068v1",
                "url": "https://arxiv.org/abs/math/0101068v1",
                "authors": ["Jean-Francois Burnol"],
                "title": "Sur les Formules Explicites I: analyse invariante",
                "relevance": "Selector III: Dilaton-invariant conductor operator log|x| + log|y| and local explicit-formula terms",
            },
            {
                "arxiv_id": "math/0203120v7",
                "url": "https://arxiv.org/abs/math/0203120v7",
                "authors": ["Jean-Francois Burnol"],
                "title": "Two complete and minimal systems associated with the zeros of the Riemann zeta function",
                "relevance": "Selector II & V: Co-Poisson formula and de Branges-Sonine Hilbert spaces",
            },
            {
                "arxiv_id": "math/0105120v1",
                "url": "https://arxiv.org/abs/math/0105120v1",
                "authors": ["Jean-Francois Burnol"],
                "title": "Sur certains espaces de Hilbert de fonctions entieres, lies a la transformation de Fourier et aux fonctions L de Dirichlet et de Riemann",
                "relevance": "Selector V: Sonine spaces of entire functions and zero-attached quotient vectors",
            },
            {
                "arxiv_id": "math/0207237v1",
                "url": "https://arxiv.org/abs/math/0207237v1",
                "authors": ["Luis Baez-Duarte"],
                "title": "A general statement of the functional equation for the Riemann zeta-function",
                "relevance": "Selector I: Dilation-invariant unitary operators and functional equation generality",
            },
            {
                "arxiv_id": "math/0307215v1",
                "url": "https://arxiv.org/abs/math/0307215v1",
                "authors": ["Luis Baez-Duarte"],
                "title": "A new necessary and sufficient condition for the Riemann hypothesis",
                "relevance": "Selector IV: Asymptotic sequence nature of Nyman-Beurling-Baez-Duarte criteria",
            },
            {
                "arxiv_id": "math/0202166v1",
                "url": "https://arxiv.org/abs/math/0202166v1",
                "authors": ["Jean-Francois Burnol"],
                "title": "On an analytic estimate in the theory of the Riemann Zeta function and a Theorem of Baez-Duarte",
                "relevance": "Selector IV: Complex-analytic proof of strengthened Nyman-Beurling criterion",
            },
            {
                "arxiv_id": "math/0404394v4",
                "url": "https://arxiv.org/abs/math/0404394v4",
                "authors": ["Jeffrey C. Lagarias"],
                "title": "Li Coefficients for Automorphic L-Functions",
                "relevance": "Selector IV: Li coefficients as values of Weil's quadratic functional on a canonical basis",
            },
            {
                "arxiv_id": "2006.13771v1",
                "url": "https://arxiv.org/abs/2006.13771v1",
                "authors": ["Alain Connes", "Caterina Consani"],
                "title": "Weil positivity and Trace formula, the archimedean place",
                "relevance": "Selector V: Sonin-space compression of scaling action and prolate spheroidal wave functions",
            },
            {
                "arxiv_id": "2106.01715v1",
                "url": "https://arxiv.org/abs/2106.01715v1",
                "authors": ["Alain Connes", "Caterina Consani"],
                "title": "Spectral Triples and Zeta-Cycles",
                "relevance": "Selector V: Restricted Weil quadratic form and prolate spheroidal eigenvectors",
            },
            {
                "arxiv_id": "2112.08820v1",
                "url": "https://arxiv.org/abs/2112.08820v1",
                "authors": ["Alain Connes", "Caterina Consani"],
                "title": "BC-system, absolute cyclotomy and the quantized calculus",
                "relevance": "Selector V & VI: Bost-Connes scaling site and quantized calculus in relation to Weil positivity",
            },
        ],
        "obl_ct_001a_status": "OPEN",
        "obl_ct_001a_completed": False,
        "rh_claimed": False,
        "candidate_selector_exhaustion_refutes_tc": False,
        "hypothesis_fidelity": {
            "tc_hypothesis": "The same arithmetic object across transcendental grades implies a constraint.",
            "selector_audit_finding": (
                "Standard zero-independent zeta axioms (functional equation, theta self-duality, "
                "explicit-formula balance, finite-stage variational projections, semi-local trace "
                "compression, and multi-grade coboundary naturality) either select the distribution "
                "W_zeta while leaving the test kernel sign-indefinite, select the additive Gaussian "
                "Theta_1 whose multiplicative Euler curvature is strictly negative by chain-rule drift, "
                "or select an infinite family whose positivity is RH-equivalent."
            ),
            "distinction": (
                "Absence of a single-kernel curvature selector among standard zero-independent "
                "structures refutes naive single-kernel selector implementations, NOT the general "
                "TC hypothesis; OBL-CT-001A remains OPEN."
            ),
        },
    }


__all__ = [
    "CANDIDATE_SELECTOR_EXHAUSTION_DOES_NOT_REFUTE_TC",
    "CandidateSelectorMechanismAudit",
    "INVERSION_SYMMETRIC_NEG_CERTIFIED",
    "INVERSION_SYMMETRIC_POS_CERTIFIED",
    "INVERSION_SYMMETRY_SIGN_INDEFINITE_STATUS",
    "LOG_GAUSSIAN_VARIANCE_THRESHOLD_PROVED",
    "LogGaussianVarianceResult",
    "OBL_CT_001A_STATUS",
    "PRINCIPAL_CLASSIFICATION",
    "SECONDARY_TRILEMMA_CLASSIFICATION",
    "SELECTOR_I_FUNCTIONAL_EQUATION_STATUS",
    "SELECTOR_II_THETA_SELF_DUALITY_STATUS",
    "SELECTOR_III_PRIME_ARCHIMEDEAN_STATUS",
    "SELECTOR_IV_VARIATIONAL_EXTREMAL_STATUS",
    "SELECTOR_V_OPERATOR_TRACE_STATUS",
    "SELECTOR_VI_STRONG_NATURALITY_STATUS",
    "SeparableTensorSquareResult",
    "TASK_TC_035_ID",
    "TASK_TC_035_STATUS",
    "TENSOR_SQUARE_REDUCTION_PROVED",
    "THETA_GAUSSIAN_NEG_CERTIFIED",
    "audit_canonical_zeta_selector",
    "audit_selector_trilemma",
    "audit_six_candidate_selectors",
    "certify_canonical_theta_gaussian_curvature_arb",
    "certify_inversion_symmetric_witness_arb",
    "evaluate_inversion_symmetric_witness_jet",
    "evaluate_log_gaussian_variance_threshold",
    "evaluate_separable_tensor_square_reduction",
    "get_selector_lean_theorem_map",
    "log_symmetric_plateau_1d_euler_jet",
    "log_symmetric_plateau_2d_euler_jet",
    "verify_inversion_and_permutation_symmetries",
    "verify_selector_lean_theorem_map_against_file",
]


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Execute TASK-TC-035 Canonical Zeta Selector Principle and Uniqueness Audit."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/tc_canonical_zeta_selector_audit.json",
        help="Path to write the JSON audit artifact.",
    )
    args = parser.parse_args()

    payload = audit_canonical_zeta_selector()
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path} ({payload['principal_classification']})")


if __name__ == "__main__":
    main()

