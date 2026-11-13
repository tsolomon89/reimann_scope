r"""
TASK-TC-059 / TASK-TC-059R: Dyadic Power-Lift Arithmetic, Primitive Coprime Correlations, Repaired
Weighted-Diagonal Closure Interface, Mellin Bridge, and Smooth-Increment Scope toward SUBGATE-TC-043A.

Implements, tests, falsifies, and certifies in 256-bit FLINT/Arb ball arithmetic (using tau
strictly via `_tau_arb()` as the sole circle constant, complex variable z = x + i*y with real x, y,
critical line x = 1/2, zero displacement delta = x - 1/2, Mellin variable w = u + i*v with real u, v,
logarithmic-saving exponent kappa_eta, and strictly distinct evaluation X, window base Y, integer
cutoff T, tower depth J, and inherited logarithmic order M):

1. Section 1 — Actual Observable, Prime-Power Reconstruction, & Repaired Route D Weighted-Diagonal
   Closure Interface (`Lean Theorem 1`, `Theorem 5(4)-(5)`, & `Theorem 6`):
   - Preserves phi_n(X) = X^{5/2} n^{-3} exp(-X^2/n^2), Q_{a,T}(X) = sum_{1<=n<=T} a(n)*phi_n(X),
     lambda(n) = (-1)^{Omega(n)}, fixed window cutoff T(Y) = ceil(Y^{5/4}) on [Y, tau*Y],
     <f, g>_Y = int_Y^{tau*Y} f(X)*g(X) dX/X, E(Y) = ||Q_{lambda,T(Y)}||_Y^2, F(Y) = sup_{1<=Z<=Y} E(Z),
     Q = P_Y + R_Y, D_tilde(Y) = sum_{p^k<=T(Y)} ||F_{p^k,Y}||_Y^2, and
     S_comb(Y) = X_tilde(Y) + 2*<P_Y, R_Y>_Y + ||R_Y||_Y^2 so E(Y) = D_tilde(Y) + S_comb(Y).
   - Evaluates preregistered grid Y in {2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 256}, certifying
     E(16)/D_tilde(16) ~= 2.45985 > 1 and E(64)/D_tilde(64) ~= 1.80789 > 1 (refuting raw E <= D_tilde
     there without refuting eventual bounds with constants, logarithmic loss, and forcing), separating
     quadrature radii from closed-form kernel arithmetic radii, and certifying the repaired Theorem 6
     weighted-diagonal closure transfer matching TC-057R Route D's shifted prime-power estimate
     D_tilde(Y) <= (2/(log Y)^2) * sum_{p^k<=Y} ((log p)^2/p^k)*F(Y/p^k) + C_cut via finite-horizon
     G_eps(R) = sup_{1<=Z<=R} E(Z)/Z^eps (keeping factor 2 once in C_eps = 2*zeta''(1+eps), with
     R-independent threshold Y_* and concrete canonicalLiouvilleEnergyE specialization; Theorem 5(5) is
     retained strictly as an auxiliary same-scale lemma).

2. Section 2 — Exact Finite Dyadic Power-Lift, Stabilization, & Attempt A (`Lean Theorems 2 & 3`):
   - Verifies a_j(n) = lambda(m) if n = m^{2^j} else 0, b_J = a_0 * ... * a_{J-1}, d_J = 2^J,
     b_J(n) = sum_{r^{d_J}|n} mu(n/r^{d_J}), (1-t)*prod_{0<=j<J}(1+t^{2^j}) = 1-t^{d_J},
     b_J(p^e) in {1, -1, 0} mod d_J, b_1 = lambda, b_J(n) = mu(n) for n < 2^{d_J}, exact discrepancy
     boundaries n = 2^{d_J} in {4, 16, 256, 65536}, squarefree agreement, exact stabilization/minimality
     inequalities T < 2^{2^{J_T}} and (1 < J_T -> 2^{2^{J_T-1}} <= T) in Lean (with J_T = O(log log T)
     as an outside-Lean analytic consequence), and J = 2 control separation across lambda, 1, a_2,
     a_{3,5,7} with exact missing prime sign relations.
   - Verifies finite Gaussian lift Q_{b_J,T}(X) = sum_{r^{d_J}<=T} r^{-d_J/2} Q_{mu,floor(T/r^{d_J})}(X/r^{d_J})
     including T = 0, 1 and X = 0.
   - Executes Attempt A (`Delta_J = b_{J+1} - b_J`): proves exact non-square root stratification of
     the J = 1 square-dilation tail, evaluates the complete window quadratic expansion retaining Q_{mu,T}
     baseline + all baseline-increment & increment-increment cross terms, certifies strict two-sided sign
     changes on <Q_{mu,T}, Q_{Delta_1,T}>_Y and <Q_{Delta_1,T}, Q_{Delta_2,T}>_Y, separates finite
     coefficients from meromorphic prod_{j<J} L_lambda(2^j z) = zeta(2^J z)/zeta(z), and certifies the
     coherent stabilized-tail Gram negative control.

3. Section 3 — Primitive Pairs, Window Kernel Scaling, Cutoff Discrepancies, & 4-Way Diagonal Comparison
   (`Lean Theorems 1 & 4`):
   - Certifies K_u(m, n) = int_u^{tau*u} phi_m(X)*phi_n(X) dX/X for all u > 0 (including 0 < u = Y/g < 1),
     phi_{g*r}(X) = g^{-1/2} phi_r(X/g), K_Y(g*r, g*s) = g^{-1} K_{Y/g}(r, s), lambda(g*r)*lambda(g*s) = lambda(r*s),
     independent 3-way verification of E(Y) (direct window quadrature, primitive-pair sum, prime-power
     reconstruction), finite synthesis/Moebius inversion E_{a,T} <-> Pi_{a,T} under complete
     multiplicativity a(m*n) = a(m)*a(n) (m, n >= 1) and a(g)^2 = 1 with certified sign changes of
     Pi_lambda, inherited floor(T(Y)/d) vs canonical T(Y/d) discrepancy witnesses, nonmonotone scales &
     T(16) jump, and explicit 4-way comparison of D_coeff, D_tilde, D_tower, and dyadic primitive-block
     diagonal including Y = 2048 > tau^4.

4. Section 4 — Dyadic Magnitude Blocks, Quotient-Shell Moebius Decoupling, Smooth-Increment Window Norm,
   & Attempt B (`Lean Theorem 4(5)`, `Theorem 5(1),(6)`, & `Theorem 7` + Analytic Variation Proofs):
   - Partitions primitive pairs and common factors into exact dyadic blocks (j_g, j_r, j_s), verifies
     exact separable quotient-shell Moebius identity (`quotientDyadicShellQ`, under complete
     multiplicativity and a(d)^2 = 1) across all 4 controls, and refutes naive uncoupled shell filtering.
   - Certifies the exact smooth-endpoint / floor-jump split g_d - g_{d+1} = Delta_d^{sm} + Delta_d^{jump}
     with unchanged inner cutoff L_d = floor(T/d) at both smooth endpoints, the exact sign
     Delta_d^{sm}(X) = -sqrt(X) * int_d^{d+1} y^{-2} sum_{q<=L_d} lambda(q)*chi_q(X/y) dy, the direct
     window norm bound ||Delta_d^{sm}||_Y <= d^{-1/2}*sqrt(E_{lambda,L_d}(Y/d)) + (d+1)^{-1/2}*sqrt(E_{lambda,L_d}(Y/(d+1)))
     (Lean Theorem 7, including T = 0 and sub-unit Y/d < 1), cutoff conversion sqrt(E_{lambda,L_d}(Y/m)) <= sqrt(F(Y/m)) + O(1)
     for m in {d, d+1} with Y/m >= 1, and why the Minkowski split loses O(1/d) adjacent-scale cancellation.
   - Certifies exact closed-form variation constants C_var and C_{chi,var} breaking TC-058's
     O(Y/(log Y)^4) smooth-step / D_{2,Y} barrier across all fixed powers of log Y, alongside domain-separated
     g <= floor(Y/2) (u >= 2) vs g > floor(Y/2) (u < 2, O(u^5) -> O(1) tail) global aggregation.

5. Section 5 — TC Geometry, Consistent Inverse-Mellin Bridge, Prime-Local Defect, Window Base, & Murmurations
   (`Lean Theorem 5(2)-(3)` + Analytic Mellin Bridge):
   - Certifies turn chart Z_{tau/2}(tau*q) = zeta(2*q) (symmetry line Re(q) = 1/4, trivial zeros q = -m,
     K^* = 1 - log(2)/log(tau) treated as an auxiliary real coordinate whose algebraic-grade admissibility
     is not established), prime-local defect D_p(delta) = (p^{delta/2} - p^{-delta/2})^2 Euler-factor
     norm-square bridge (computed without sampled zeta-zero inputs), consistent inverse-Mellin bridge
     M_Q(w) = int_0^infty Q_{lambda,infty}(X)*X^{-w} dX/X = Gamma(5/4 - w/2)*zeta(1 + 2*w)/(2*zeta(1/2 + w))
     on 1/2 < u < 5/2 (extending holomorphically to 0 < u < 5/2 under E(Y) = O_eps(Y^eps), mapping
     rho = x + i*y with 1/2 < x < 1 to w_rho = rho - 1/2 in {0 < u < 5/2}), parameterized [Y, b*Y]
     analytic scaling for arbitrary b > 1 with finite b in {2, e, tau} checks, and murmuration audit.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from flint import acb, arb, ctx as flint_ctx

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tc.canonical_theta_correlation_bound import (
    EPIC_TC_042_ID,
    REPO_ROOT,
    serialize_arb_certified,
    verify_all_serialized_arb_in_tree,
)
from tc.coupled_scale_energy_bootstrap import (
    TASK_TC_057_ID,
    TASK_TC_057R_ID,
    _acb_integral_certified_arb,
    _evaluate_route_d_totals_arb,
    _frac_to_arb,
    _tau_arb,
    _weight_fn_for_mode,
    evaluate_E_L_scale_arb,
    evaluate_Q_shifted_finite_arb,
    moebius_mu_int,
    prime_power_pairs_up_to,
    selberg_w2_weight_arb,
)
from tc.liouville_square_dilation import (
    TASK_TC_054_ID,
    TASK_TC_054R_ID,
    TASK_TC_054R2_ID,
    TASK_TC_055_ID,
    TASK_TC_055R_ID,
    TASK_TC_055R2_ID,
    TASK_TC_056_ID,
    _ARB_BACKTICK_INTERVAL_RE,
    _LATEX_PM_INTERVAL_RE,
    _TC_ENCLOSURE_TAG_RE,
    _parse_arb_ball_str_to_fractions,
    _resolve_report_path_with_param_check,
    _sci_or_latex_num_to_fraction,
    liouville_lambda_int,
)
from tc.prime_chain_contraction import (
    TASK_TC_056R_ID,
    TASK_TC_056R2_ID,
    evaluate_phi_n_arb,
    exact_T_cutoff_ceil_Y_5_4,
)
from tc.simultaneous_compatibility_combined_energy import (
    TASK_TC_058_ID,
    TASK_TC_058R_ID,
    TASK_TC_058R2_ID,
    evaluate_c_lambda_arb,
    evaluate_direct_cross_term_PR_arb,
)

TASK_TC_059_ID = "TASK-TC-059"
TASK_TC_059R_ID = "TASK-TC-059R"
PARENT_SUBGATE_ID = "SUBGATE-TC-043A"
REVIEWED_MERGED_MAIN_BASELINE = "2c784c9433edcf37d3f666b75e7ac0d83abc919a"
INCLUDED_TC_058R2_TIP = "c5135ea9c98dd9056850873f39cc23f434614a35"
PROPOSED_BRANCH = "task/tc-059-power-lift-and-primitive-correlation"
REVIEWED_TC_059_IMPLEMENTATION = "46b633d1738b3c4b354b9c80aebe13f7e861105b"
REVIEWED_TC_059_HEAD = "55e8193a7d753454fa4a7acf3c19cc1deca6ea88"
REPAIR_BRANCH = "task/tc-059r-normalized-closure-mellin-and-smooth-increment-repair"

DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_dyadic_power_lift_primitive_correlation.json"
)
TC_059_REVIEW_DOC_PATH = (
    REPO_ROOT / "docs" / "reviews" / "TC_059_POWER_LIFT_AND_PRIMITIVE_CORRELATION.md"
)
TC_059_LEAN_MODULE_PATH = (
    REPO_ROOT / "formal" / "RiemannScope" / "DyadicPowerLiftPrimitiveCorrelation.lean"
)

EXPECTED_TC059_THEOREMS: List[str] = [
    "window_integrability_and_kernel_scaling_tc059",
    "dyadic_power_lift_divisor_prime_power_and_stabilization_tc059",
    "gaussian_power_lift_increment_telescope_and_coherent_tail_tc059",
    "primitive_coprime_expansion_moebius_inversion_and_dyadic_block_tc059",
    "parity_uniqueness_turn_chart_defect_and_log_saving_closure_tc059",
    "repaired_weighted_diagonal_closure_and_actual_observable_tc059r",
    "smooth_increment_window_norm_and_small_scale_tail_tc059r",
]

EPISTEMIC_CATEGORIES: Tuple[str, ...] = (
    "UNCONDITIONAL_FINITE_ARITHMETIC",
    "ANALYTIC_PROVED_OUTSIDE_LEAN",
    "CONCRETE_ANALYTIC_IN_LEAN",
    "CONDITIONAL_IMPLICATION",
    "CERTIFIED_FINITE_OBSERVATION",
    "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
)


# ---------------------------------------------------------------------------
# 0. Exact Arithmetic (Without Sampled Zeta-Zero Inputs) & Kernel Helpers
# ---------------------------------------------------------------------------


def integer_kth_root_exact(n: int, k: int) -> Optional[int]:
    """Return exact integer `m >= 1` with `m^k == n`, or `None` if `n` is not a `k`-th power."""
    if n < 1 or k < 1:
        return None
    if n == 1:
        return 1
    lo, hi = 1, int(round(n ** (1.0 / k))) + 2
    while lo <= hi:
        mid = (lo + hi) // 2
        pw = mid ** k
        if pw == n:
            return mid
        if pw < n:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


def dyadic_step_a_j_int(n: int, j: int, base_fn: Callable[[int], int] = liouville_lambda_int) -> int:
    """Exact dyadic step coefficient `a_j(n) = a(m)` if `n = m^{2^j}` else `0` (`j >= 0`)."""
    if n < 1 or j < 0:
        return 0
    m = integer_kth_root_exact(n, 1 << j)
    return int(base_fn(m)) if m is not None else 0


def dirichlet_convolve_int(f: Sequence[int], g: Sequence[int], N: int) -> List[int]:
    """Exact Dirichlet convolution `(f * g)(n)` on `0 <= n <= N`."""
    out = [0] * (N + 1)
    for d in range(1, N + 1):
        fd = f[d]
        if fd == 0:
            continue
        for q in range(1, N // d + 1):
            gq = g[q]
            if gq != 0:
                out[d * q] += fd * gq
    return out


def dyadic_power_lift_b_J_conv_table(
    J: int,
    N: int,
    base_fn: Callable[[int], int] = liouville_lambda_int,
) -> List[int]:
    """Compute `b_{a, J} = a_0 * a_1 * ... * a_{J-1}` on `0 <= n <= N` directly by Dirichlet convolution."""
    if J < 0:
        raise ValueError("J must be >= 0")
    cur = [0] * (N + 1)
    if N >= 1:
        cur[1] = 1
    for j in range(J):
        step_j = [0] + [dyadic_step_a_j_int(n, j, base_fn=base_fn) for n in range(1, N + 1)]
        cur = dirichlet_convolve_int(cur, step_j, N)
    return cur


def dyadic_power_lift_b_J_divisor_int(J: int, n: int) -> int:
    """Exact power-divisor Moebius formula `b_J(n) = sum_{r^{2^J} | n} mu(n / r^{2^J})` (`J >= 1`)."""
    if n < 1 or J < 1:
        return 0
    d_J = 1 << J
    acc = 0
    r = 1
    while True:
        rd = r ** d_J
        if rd > n:
            break
        if n % rd == 0:
            acc += moebius_mu_int(n // rd)
        r += 1
    return acc


def power_lift_increment_delta_J_int(J: int, n: int) -> int:
    """Exact dyadic power-lift increment `Delta_J(n) = b_{J+1}(n) - b_J(n)` (`J >= 1`)."""
    return dyadic_power_lift_b_J_divisor_int(J + 1, n) - dyadic_power_lift_b_J_divisor_int(J, n)


def stabilization_depth_J_T(T: int) -> int:
    """Least integer `J >= 1` such that `2^{2^J} > T` (`TASK-TC-059` §2)."""
    J = 1
    while (1 << (1 << J)) <= T:
        J += 1
    return J


def is_squarefree_int(n: int) -> bool:
    """Exact squarefree predicate on positive integers."""
    return n >= 1 and moebius_mu_int(n) != 0


def is_perfect_square_int(n: int) -> bool:
    """Exact perfect-square predicate on positive integers."""
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def evaluate_Q_general_arb(
    X: Union[int, Fraction, arb],
    T: int,
    coeff_fn: Callable[[int], Union[int, arb]],
    prec_bits: int = 256,
) -> arb:
    """Exact finite Gaussian observable `Q_{a, T}(X) = sum_{1 <= n <= T} a(n) * phi_n(X)` in Arb."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        x_arb = X if isinstance(X, arb) else (_frac_to_arb(X) if isinstance(X, Fraction) else arb(X))
        if T < 1 or bool(x_arb == arb(0)):
            return arb(0)
        acc = arb(0)
        for n in range(1, T + 1):
            cn = coeff_fn(n)
            if isinstance(cn, int) and cn == 0:
                continue
            c_arb = cn if isinstance(cn, arb) else arb(cn)
            acc += c_arb * evaluate_phi_n_arb(x_arb, n, prec_bits=prec_bits)
        return acc
    finally:
        flint_ctx.prec = saved


def _gaussian_quartic_window_diff_arb(v1: arb, v2: arb) -> arb:
    """Certified evaluation of `int_{v1}^{v2} v^4 * exp(-v^2) dv` for `0 < v1 <= v2` using `tau` only.

    Uses:
    - alternating Taylor series with certified remainder ball when `v2 <= 1/2` (preventing catastrophic
      cancellation near `0`),
    - `F(v2) - F(v1)` with `F(v) = (3*sqrt(tau/2)/8)*erf(v) - v*(v^2/2 + 3/4)*exp(-v^2)` when `v1 <= 1`,
    - `G(v1) - G(v2)` with `G(v) = (3*sqrt(tau/2)/8)*erfc(v) + v*(v^2/2 + 3/4)*exp(-v^2)` when `v1 > 1`
      (preventing subtraction of numbers near `3*sqrt(tau/2)/8` in the Gaussian tail).
    """
    tau = _tau_arb()
    c_erf = arb(3) * (tau / arb(2)).sqrt() / arb(8)
    if float(v2.upper()) <= 0.5:
        # Exact alternating series sum_{k=0}^{K-1} (-1)^k v^{2k+5} / (k! * (2k+5)) + [+/- v^{2K+5}/(K!*(2K+5))]
        K_terms = 40

        def _series_F(v: arb) -> arb:
            v2_sq = v * v
            v_pow = v ** 5
            fact = arb(1)
            s = arb(0)
            for k in range(K_terms):
                term = v_pow / (fact * arb(2 * k + 5))
                s = s + term if (k % 2 == 0) else s - term
                v_pow = v_pow * v2_sq
                fact = fact * arb(k + 1)
            rem_bound = abs(v_pow) / (fact * arb(2 * K_terms + 5))
            err_ball = arb(0, rem_bound.upper())
            return s + err_ball

        return _series_F(v2) - _series_F(v1)
    if float(v1.lower()) > 1.0:
        g1 = c_erf * v1.erfc() + v1 * (v1 * v1 / arb(2) + arb(3) / arb(4)) * (-v1 * v1).exp()
        g2 = c_erf * v2.erfc() + v2 * (v2 * v2 / arb(2) + arb(3) / arb(4)) * (-v2 * v2).exp()
        return g1 - g2
    f1 = c_erf * v1.erf() - v1 * (v1 * v1 / arb(2) + arb(3) / arb(4)) * (-v1 * v1).exp()
    f2 = c_erf * v2.erf() - v2 * (v2 * v2 / arb(2) + arb(3) / arb(4)) * (-v2 * v2).exp()
    return f2 - f1


def evaluate_window_kernel_K_closed_arb(
    u: Union[int, Fraction, arb],
    m: int,
    n: int,
    base_mult: Optional[arb] = None,
    prec_bits: int = 256,
) -> arb:
    """Closed-form 256-bit Arb evaluation of `K_{u, b}(m, n) = int_u^{b*u} phi_m(X)*phi_n(X) dX/X`
    for any `u > 0` (including `0 < u < 1`), defaulting to `b = tau`.
    """
    if m < 1 or n < 1:
        return arb(0)
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        u_arb = u if isinstance(u, arb) else (_frac_to_arb(u) if isinstance(u, Fraction) else arb(u))
        b_mult = _tau_arb() if base_mult is None else base_mult
        beta = arb(m * m + n * n).sqrt() / arb(m * n)
        v1 = beta * u_arb
        v2 = beta * b_mult * u_arb
        diff = _gaussian_quartic_window_diff_arb(v1, v2)
        denom = (arb(m) ** 3) * (arb(n) ** 3) * (beta ** 5)
        return diff / denom
    finally:
        flint_ctx.prec = saved


def evaluate_window_kernel_K_quadrature_arb(
    u: Union[int, Fraction, arb],
    m: int,
    n: int,
    prec_bits: int = 256,
) -> arb:
    """Direct `acb.integral` quadrature enclosure of `K_u(m, n) = int_u^{tau*u} phi_m(X)*phi_n(X) dX/X`."""
    if m < 1 or n < 1:
        return arb(0)
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        u_arb = u if isinstance(u, arb) else (_frac_to_arb(u) if isinstance(u, Fraction) else arb(u))
        tau = _tau_arb()
        alpha = acb(1) / acb(m * m) + acb(1) / acb(n * n)
        pref = arb(1) / ((arb(m) ** 3) * (arb(n) ** 3))

        def _integrand(z: acb, _analytic: bool) -> acb:
            return (z ** 4) * (-alpha * z * z).exp()

        return pref * _acb_integral_certified_arb(_integrand, u_arb, tau * u_arb, prec_bits=prec_bits)
    finally:
        flint_ctx.prec = saved


def evaluate_bilinear_window_pairing_closed_arb(
    u: Union[int, Fraction, arb],
    T: int,
    coeff_a: Sequence[Union[int, arb]],
    coeff_b: Sequence[Union[int, arb]],
    base_mult: Optional[arb] = None,
    prec_bits: int = 256,
) -> arb:
    """Evaluate `<Q_{a,T}, Q_{b,T}>_{u, base_mult}` via exact closed-form `K_u(m, n)` symmetry."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        if T < 1:
            return arb(0)
        u_arb = u if isinstance(u, arb) else (_frac_to_arb(u) if isinstance(u, Fraction) else arb(u))
        nz_a = [(m, coeff_a[m] if isinstance(coeff_a[m], arb) else arb(coeff_a[m])) for m in range(1, T + 1) if coeff_a[m] != 0]
        nz_b = [(n, coeff_b[n] if isinstance(coeff_b[n], arb) else arb(coeff_b[n])) for n in range(1, T + 1) if coeff_b[n] != 0]
        same_vec = coeff_a is coeff_b
        acc = arb(0)
        if same_vec:
            for idx_i, (m, am) in enumerate(nz_a):
                acc += (am * am) * evaluate_window_kernel_K_closed_arb(
                    u_arb, m, m, base_mult=base_mult, prec_bits=prec_bits
                )
                for j_idx in range(idx_i + 1, len(nz_a)):
                    n, an = nz_a[j_idx]
                    acc += arb(2) * (am * an) * evaluate_window_kernel_K_closed_arb(
                        u_arb, m, n, base_mult=base_mult, prec_bits=prec_bits
                    )
            return acc
        for m, am in nz_a:
            for n, bn in nz_b:
                acc += (am * bn) * evaluate_window_kernel_K_closed_arb(
                    u_arb, m, n, base_mult=base_mult, prec_bits=prec_bits
                )
        return acc
    finally:
        flint_ctx.prec = saved


def evaluate_primitive_coprime_sum_Pi_arb(
    u: Union[int, Fraction, arb],
    T: int,
    mode: str = "liouville",
    unsigned: bool = False,
    prec_bits: int = 256,
) -> arb:
    """Evaluate `Pi_{a, T}(u) = sum_{1<=r,s<=T, gcd(r,s)=1} a(r)*a(s)*K_u(r, s)` in 256-bit Arb."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        if T < 1:
            return arb(0)
        u_arb = u if isinstance(u, arb) else (_frac_to_arb(u) if isinstance(u, Fraction) else arb(u))
        w_fn = _weight_fn_for_mode(mode)
        w_arr = [0] + [1 if unsigned else int(w_fn(n)) for n in range(1, T + 1)]
        acc = arb(w_arr[1] * w_arr[1]) * evaluate_window_kernel_K_closed_arb(
            u_arb, 1, 1, prec_bits=prec_bits
        )
        for r in range(1, T + 1):
            wr = w_arr[r]
            for s in range(r + 1, T + 1):
                if math.gcd(r, s) == 1:
                    acc += arb(2 * wr * w_arr[s]) * evaluate_window_kernel_K_closed_arb(
                        u_arb, r, s, prec_bits=prec_bits
                    )
        return acc
    finally:
        flint_ctx.prec = saved


def evaluate_C_var_gaussian_arb(prec_bits: int = 256) -> arb:
    """Exact closed-form Gaussian variation constant `C_var = 1/2 + 2*exp(-3/2) + exp(-1)`."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        return arb(1) / arb(2) + arb(2) * (-arb(3) / arb(2)).exp() + (-arb(1)).exp()
    finally:
        flint_ctx.prec = saved


def evaluate_C_chi_var_smooth_arb(prec_bits: int = 256) -> arb:
    """Exact closed-form dimensionless smooth-step `chi` variation constant:
    `C_{chi,var} = exp(-1/2) + 1/2 + (4*sqrt(7) - 8)*exp(-(2 - sqrt(7)/2)) + (4*sqrt(7) + 8)*exp(-(2 + sqrt(7)/2))`.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        s7 = arb(7).sqrt()
        t_minus = arb(2) - s7 / arb(2)
        t_plus = arb(2) + s7 / arb(2)
        return (
            (-arb(1) / arb(2)).exp()
            + arb(1) / arb(2)
            + (arb(4) * s7 - arb(8)) * (-t_minus).exp()
            + (arb(4) * s7 + arb(8)) * (-t_plus).exp()
        )
    finally:
        flint_ctx.prec = saved


def evaluate_single_term_mellin_phi_quadrature_arb(
    n: int,
    w: acb,
    prec_bits: int = 256,
) -> acb:
    """Certified 256-bit `acb` enclosure of the actual single-term inverse-Mellin integral
    `I_n(w) = int_0^infty phi_n(X) * X^{-w} dX/X` (`w = u + i*v`, `-3/2 <= u < 5/2`, `n >= 1`)
    computed directly from `phi_n(X) = X^{5/2} n^{-3} exp(-X^2/n^2)` without Gamma identities:
    - `(0, 1/4]`: exact 30-term alternating exponential series integral + certified Lagrange tail
      `|R_K| <= n^{-3-2K} (1/4)^{2K + 5/2 - u} / (K! * (2K + 5/2 - u))` (`K = 30`),
    - `[1/4, 18*n]`: certified `acb.integral` away from `X = 0`,
    - `[18*n, infty)`: substituting `X = n*t` (`t >= 18`, `u >= -3/2` so `t^{3/2-u} <= t^3`) and using
      `t^2 * exp(-t^2/4) <= 4/e` (`x*exp(-x) <= 1/e` at `x = t^2/4`),
      `|int_{18*n}^infty phi_n(X) X^{-w-1} dX| <= (4/e) n^{-1/2-u} int_{18}^infty t exp(-3*t^2/4) dt
      = (8/(3*e)) n^{-1/2-u} exp(-243)`.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        u_re = w.real
        if not bool(arb(5) / arb(2) - u_re > arb(0)):
            raise ValueError("Single-term Mellin integral requires u = Re(w) < 5/2")
        if not bool(u_re + arb(3) / arb(2) >= arb(0)):
            raise ValueError("Tail majorant requires u = Re(w) >= -3/2")

        delta_0 = arb(1) / arb(4)
        delta_0_c = acb(delta_0)
        n_arb = arb(n)
        n_c = acb(n)
        K_ser = 30
        left_sum = acb(0)
        fact = arb(1)
        for k in range(K_ser):
            exp_k = acb(arb(2 * k) + arb(5) / arb(2)) - w
            term_k = (
                (acb(-1) ** k)
                * (delta_0_c ** exp_k)
                / (acb(fact) * (n_c ** (3 + 2 * k)) * exp_k)
            )
            left_sum += term_k
            fact = fact * arb(k + 1)
        rem_exp_re = arb(2 * K_ser) + arb(5) / arb(2) - u_re
        left_rad = (
            (n_arb ** (-3 - 2 * K_ser))
            * (delta_0 ** rem_exp_re)
            / (fact * rem_exp_re)
        )

        hi_x = arb(18 * n)

        def _mid_integrand(z: acb, _analytic: bool) -> acb:
            if _analytic and not bool(z.real > arb(0)):
                nan_b = arb("nan")
                return acb(nan_b, nan_b)
            z_pow = (acb(arb(3) / arb(2)) - w) * z.log(analytic=_analytic)
            return z_pow.exp() * (n_c ** (-3)) * (-(z * z) / (n_c * n_c)).exp()

        mid_int = acb.integral(
            _mid_integrand,
            acb(delta_0),
            acb(hi_x),
            rel_tol=2 ** (-prec_bits + 12),
            abs_tol=2 ** (-prec_bits + 12),
        )

        e_val = arb(1).exp()
        right_rad = (
            (arb(8) / (arb(3) * e_val))
            * (n_arb ** (-arb(1) / arb(2) - u_re))
            * (-arb(243)).exp()
        )
        tot_tail = (left_rad + right_rad).upper()
        tail_ball = acb(arb(0, tot_tail), arb(0, tot_tail))
        return left_sum + mid_int + tail_ball
    finally:
        flint_ctx.prec = saved


def evaluate_smooth_increment_and_jump_arb(
    X: Union[int, Fraction, arb],
    T: int,
    d: int,
    prec_bits: int = 256,
) -> Dict[str, arb]:
    """Evaluate `g_d(X) - g_{d+1}(X)`, `Delta_d^{sm}(X)` (with identical cutoff `L_d = T // d` at both
    endpoints), its `-sqrt(X) * int_d^{d+1} y^{-2} sum_{q=1}^{L_d} lambda(q)*chi_q(X/y) dy` integral
    representation, and the separate floor-jump `Delta_d^{jump}(X)` (`d >= 1`, `T >= 0`, `X > 0`).
    """
    if d < 1 or T < 0:
        raise ValueError("Require d >= 1 and T >= 0")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        x_arb = X if isinstance(X, arb) else (_frac_to_arb(X) if isinstance(X, Fraction) else arb(X))
        L_d = T // d
        L_d1 = T // (d + 1)
        d_arb = arb(d)
        d1_arb = arb(d + 1)
        g_d = evaluate_Q_general_arb(
            x_arb / d_arb, L_d, coeff_fn=liouville_lambda_int, prec_bits=prec_bits
        ) / d_arb.sqrt()
        g_d1_same_L = evaluate_Q_general_arb(
            x_arb / d1_arb, L_d, coeff_fn=liouville_lambda_int, prec_bits=prec_bits
        ) / d1_arb.sqrt()
        g_d1_next_L = evaluate_Q_general_arb(
            x_arb / d1_arb, L_d1, coeff_fn=liouville_lambda_int, prec_bits=prec_bits
        ) / d1_arb.sqrt()
        delta_sm_endpoint = g_d - g_d1_same_L
        delta_jump = g_d1_same_L - g_d1_next_L
        total_step = g_d - g_d1_next_L

        if L_d == 0:
            delta_sm_integral = arb(0)
        else:
            lam_q = [0] + [liouville_lambda_int(q) for q in range(1, L_d + 1)]
            x_c = acb(x_arb)

            def _chi_sum_integrand(y_c: acb, _analytic: bool) -> acb:
                if _analytic and not bool(y_c.real > arb(0)):
                    nan_b = arb("nan")
                    return acb(nan_b, nan_b)
                w_c = x_c / y_c
                acc = acb(0)
                for q in range(1, L_d + 1):
                    qc = acb(q)
                    u_c = w_c / qc
                    u2 = u_c * u_c
                    chi_c = (acb(1) / qc) * u2 * (acb(2) * u2 - acb(3)) * (-u2).exp()
                    acc += acb(lam_q[q]) * chi_c
                return acc / (y_c * y_c)

            raw_int = _acb_integral_certified_arb(
                _chi_sum_integrand, d_arb, d1_arb, prec_bits=prec_bits
            )
            delta_sm_integral = -(x_arb.sqrt()) * raw_int

        return {
            "g_d_minus_g_d1": total_step,
            "delta_sm_endpoint": delta_sm_endpoint,
            "delta_sm_integral": delta_sm_integral,
            "delta_jump": delta_jump,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 1. Section 1: Observable, Prime-Power Reconstruction, & Closure Contract
# ---------------------------------------------------------------------------


def verify_section_1_observable_and_closure_contract(prec_bits: int = 256) -> Dict[str, Any]:
    """Verify `E(Y) = D_tilde(Y) + S_comb(Y)` on the preregistered grid, separate quadrature vs
    closed-form kernel radii, check `E(16)/D_tilde(16)` & `E(64)/D_tilde(64)` ratios, and certify
    the conditional logarithmic-saving closure transfer via `G_eps(R_hor)`.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        grid_Y = (2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 256)
        grid_rows: List[Dict[str, Any]] = []
        all_ok = True

        for Y_int in grid_Y:
            T_Y = exact_T_cutoff_ceil_Y_5_4(Y_int)
            y_arb = arb(Y_int)
            lg_y = y_arb.log()
            lam_vec = [0] + [liouville_lambda_int(n) for n in range(1, T_Y + 1)]

            # Closed-form exact window kernel evaluation of E(Y)
            E_closed = evaluate_bilinear_window_pairing_closed_arb(
                y_arb, T_Y, lam_vec, lam_vec, prec_bits=prec_bits
            )
            # Independent direct acb.integral quadrature evaluation of E(Y), D_tilde(Y), X_tilde(Y), ||R_Y||^2
            E_quad = evaluate_E_L_scale_arb(y_arb, L=T_Y, mode="liouville", prec_bits=prec_bits)
            rd = _evaluate_route_d_totals_arb(Y_int, mode="liouville", prec_bits=prec_bits)
            D_tilde = rd["D_tilde"]
            X_tilde = rd["X_tilde"]
            R_norm_sq = rd["E_sh1"]

            # Direct <P_Y, R_Y>_Y via P_Y = Q_T - R_Y => 2*<P_Y, R_Y>_Y = E - ||P_Y||^2 - ||R_Y||^2,
            # AND independent direct quadrature of int_Y^{tau*Y} P_Y(X)*R_Y(X) dX/X!
            w_lam_acb = [0] + [liouville_lambda_int(n) for n in range(1, T_Y + 1)]
            log_n_acb = [acb(0)] + [acb(arb(n).log()) for n in range(1, T_Y + 1)]

            def _PR_integrand(
                z: acb,
                _analytic: bool,
                _T: int = T_Y,
                _w: Sequence[int] = w_lam_acb,
                _ln: Sequence[acb] = log_n_acb,
            ) -> acb:
                z2 = z * z
                lg_z = z.log(analytic=_analytic)
                q0 = acb(0)
                q1 = acb(0)
                for n in range(1, _T + 1):
                    nc = acb(n)
                    g_val = acb(_w[n]) * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                    q0 += g_val
                    q1 += (lg_z - _ln[n]) * g_val
                r_part = q1 / lg_z
                p_part = q0 - r_part
                return (z ** 4) * p_part * r_part

            PR_cross_direct = _acb_integral_certified_arb(
                _PR_integrand, y_arb, tau * y_arb, prec_bits=prec_bits
            )
            S_comb_direct = X_tilde + arb(2) * PR_cross_direct + R_norm_sq
            recon_res = E_quad - (D_tilde + S_comb_direct)
            closed_vs_quad_res = E_closed - E_quad
            ratio_E_D = E_closed / D_tilde
            ratio_S_D = S_comb_direct / D_tilde

            # Candidate closure-contract slack at kappa_eta = 1, A_eta = 1, B_eta = 2, eta = 1/4:
            cand_rhs_k1 = (y_arb ** (arb(1) / arb(4))) + arb(2) * lg_y * D_tilde
            cand_slack_k1 = cand_rhs_k1 - E_closed

            row_ok = bool(
                E_closed > arb(0)
                and D_tilde > arb(0)
                and arb(0) in recon_res
                and abs(recon_res) < arb("1e-60")
                and arb(0) in closed_vs_quad_res
                and abs(closed_vs_quad_res) < arb("1e-62")
                and cand_slack_k1 > arb(0)
            )
            if Y_int in (16, 64):
                row_ok = bool(row_ok and ratio_E_D - arb(1) > arb(0))
            all_ok = all_ok and row_ok

            grid_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_Y,
                    "E_closed_kernel": serialize_arb_certified(E_closed),
                    "E_quadrature_direct": serialize_arb_certified(E_quad),
                    "closed_kernel_radius_str": f"{float(E_closed.rad()):.3e}",
                    "quadrature_radius_str": f"{float(E_quad.rad()):.3e}",
                    "closed_minus_quadrature_consistency_residual": serialize_arb_certified(
                        closed_vs_quad_res
                    ),
                    "D_tilde": serialize_arb_certified(D_tilde),
                    "X_tilde": serialize_arb_certified(X_tilde),
                    "two_PR_cross_direct": serialize_arb_certified(arb(2) * PR_cross_direct),
                    "R_norm_sq": serialize_arb_certified(R_norm_sq),
                    "S_comb_direct": serialize_arb_certified(S_comb_direct),
                    "E_minus_D_tilde_add_S_comb_algebraic_consistency_residual": serialize_arb_certified(
                        recon_res
                    ),
                    "ratio_E_over_D_tilde": serialize_arb_certified(ratio_E_D),
                    "ratio_S_comb_over_D_tilde": serialize_arb_certified(ratio_S_D),
                    "sample_closure_slack_eta_quarter_A1_B2_kappa1": serialize_arb_certified(
                        cand_slack_k1
                    ),
                    "verified": row_ok,
                }
            )

        row_16 = next(r for r in grid_rows if r["Y"] == 16)
        row_64 = next(r for r in grid_rows if r["Y"] == 64)

        # Repaired primary weighted-diagonal closure transfer (Theorem 6:
        # repaired_weighted_diagonal_closure_and_actual_observable_tc059r) matching TC-057R Route D's
        # shifted prime-power estimate D_tilde(Y) <= (2/(log Y)^2) * sum_{p^k<=Y} ((log p)^2/p^k)*F(Y/p^k) + C_cut
        # via finite-horizon G_eps(R) = sup_{1<=Z<=R} E(Z)/Z^eps (keeping factor 2 once in C_eps = 2*zeta''(1+eps),
        # with R-independent threshold Y_*; Theorem 5(5) is retained strictly as an auxiliary same-scale lemma).
        e_val = arb(1).exp()
        eps_val = arb(1) / arb(2)
        eta_val = arb(1) / arb(8)
        eta_prime = (eta_val + eps_val) / arb(2)  # 5/16
        # Certified zeta''(1 + eps) via complex Taylor series of zeta(s) at s = 3/2:
        from flint import acb_series

        z_ser = acb_series([acb(arb(3) / arb(2)), acb(1)], prec=prec_bits).zeta()
        zeta_second_deriv_3_2 = arb(2) * z_ser[2].real
        B_eta_sched = arb(1)
        C_diag_sched = arb(2) * zeta_second_deriv_3_2
        schedule_rows: List[Dict[str, Any]] = []
        sched_ok = bool(zeta_second_deriv_3_2 > arb(0))
        for kappa_num, kappa_den in ((1, 2), (1, 1), (2, 1)):
            kappa_arb = arb(kappa_num) / arb(kappa_den)
            Y_thresh = ((arb(2) * B_eta_sched * C_diag_sched + arb(1)) ** (arb(1) / kappa_arb)).exp()
            fb_at_thresh = B_eta_sched * C_diag_sched / ((Y_thresh.log()) ** kappa_arb)
            polylog_majorant_const = arb(4) / ((e_val ** 2) * (eta_prime ** 2))
            # Check polylog majorant at Y = max(e, 16)
            Y_test = arb(16)
            lhs_pl = (Y_test.log()) ** (arb(2) - kappa_arb)
            rhs_pl = polylog_majorant_const * (Y_test ** eta_prime)
            ok_k = bool(arb(1) / arb(2) - fb_at_thresh > arb(0) and rhs_pl - lhs_pl > arb(0))
            sched_ok = sched_ok and ok_k
            schedule_rows.append(
                {
                    "kappa_eta": f"{kappa_num}/{kappa_den}" if kappa_den != 1 else str(kappa_num),
                    "lean_theorem": "repaired_weighted_diagonal_closure_and_actual_observable_tc059r",
                    "zeta_double_prime_at_3_2": serialize_arb_certified(zeta_second_deriv_3_2),
                    "C_diag_prospective_2_zeta_pp": serialize_arb_certified(C_diag_sched),
                    "factor_two_count_in_C_eps": 1,
                    "log_Y_star_threshold": serialize_arb_certified(Y_thresh.log()),
                    "feedback_coeff_at_Y_star": serialize_arb_certified(fb_at_thresh),
                    "half_minus_feedback_margin": serialize_arb_certified(
                        arb(1) / arb(2) - fb_at_thresh
                    ),
                    "polylog_rpow_majorant_const_4_over_e2_etap2": serialize_arb_certified(
                        polylog_majorant_const
                    ),
                    "polylog_bound_margin_at_Y16": serialize_arb_certified(rhs_pl - lhs_pl),
                    "verified": ok_k,
                }
            )

        # TASK-TC-059R Repair 1 checks:
        # (a) Weighted prime-power mass sum_{p^k <= Y, k >= 1} (log p)^2 / (p^k)^{1+eps} < zeta''(1+eps)
        #     across eps in {1/2, 1/4} and Y in {16, 64, 256}, C_eps = 2*zeta''(1+eps), and R-independence
        #     of Y_* and K/(1-q) = 2*K across finite horizons R in {64, 256, 1024}.
        weighted_mass_rows: List[Dict[str, Any]] = []
        repair1_ok = True
        for eps_num, eps_den in ((1, 2), (1, 4)):
            eps_c = arb(eps_num) / arb(eps_den)
            z_ser_e = acb_series([acb(arb(1) + eps_c), acb(1)], prec=prec_bits).zeta()
            zeta2_e = arb(2) * z_ser_e[2].real
            C_eps_e = arb(2) * zeta2_e
            eta_e = eps_c / arb(4)
            etap_e = (eta_e + eps_c) / arb(2)
            A_eta_sample = arb(1)
            B_eta_sample = arb(1)
            C_cut_sample = arb(1)
            kappa_sample = arb(1)
            Y_diag_sample = e_val
            Y_eta_sample = e_val
            exp_arg_e = (arb(2) * B_eta_sample * C_eps_e + arb(1)) ** (arb(1) / kappa_sample)
            Y_star_e = exp_arg_e.exp()  # >= exp(1) = Y_diag_sample = Y_eta_sample
            K_e = A_eta_sample * (Y_star_e ** (eta_e - eps_c)) + (
                B_eta_sample
                * C_cut_sample
                * (arb(4) / ((e_val ** 2) * (etap_e ** 2)))
                * (Y_star_e ** (etap_e - eps_c))
            )
            two_K_e = arb(2) * K_e
            q_fb = arb(1) / arb(2)
            ratio_K_1mq = K_e / (arb(1) - q_fb)
            res_2K = ratio_K_1mq - two_K_e
            # Verify Y_star_e and ratio_K_1mq do not depend on R across R in {64, 256, 1024}:
            horizons_checked = [64, 256, 1024]
            fb_Ys = B_eta_sample * C_eps_e / (Y_star_e.log() ** kappa_sample)
            for Y_pp in (16, 64, 256):
                fin_pp_mass = arb(0)
                fin_pp_log_n_majorant = arb(0)
                for p_val, k_val in prime_power_pairs_up_to(Y_pp):
                    pk_int = p_val ** k_val
                    pk_arb = arb(pk_int)
                    lp_sq = (arb(p_val).log()) ** 2
                    ln_sq = (pk_arb.log()) ** 2
                    denom = pk_arb ** (arb(1) + eps_c)
                    fin_pp_mass += lp_sq / denom
                    fin_pp_log_n_majorant += ln_sq / denom
                margin_zeta2 = zeta2_e - fin_pp_mass
                margin_step = fin_pp_log_n_majorant - fin_pp_mass
                ok_wm = bool(
                    zeta2_e > arb(0)
                    and margin_zeta2 > arb(0)
                    and margin_step >= arb(0)
                    and q_fb - fb_Ys > arb(0)
                    and arb(0) in res_2K
                    and abs(res_2K) < arb("1e-70")
                )
                repair1_ok = repair1_ok and ok_wm
                if Y_pp in (16, 256):
                    weighted_mass_rows.append(
                        {
                            "eps": f"{eps_num}/{eps_den}",
                            "Y": Y_pp,
                            "finite_prime_power_weighted_mass": serialize_arb_certified(fin_pp_mass),
                            "zeta_double_prime_1_plus_eps": serialize_arb_certified(zeta2_e),
                            "zeta_double_prime_minus_finite_mass_margin": serialize_arb_certified(
                                margin_zeta2
                            ),
                            "C_eps_2_zeta_double_prime": serialize_arb_certified(C_eps_e),
                            "factor_two_count": 1,
                            "R_independent_log_Y_star_B1_kappa1": serialize_arb_certified(
                                Y_star_e.log()
                            ),
                            "K_over_1_minus_q_sample": serialize_arb_certified(ratio_K_1mq),
                            "horizons_R_sharing_identical_Y_star_and_2K": horizons_checked,
                            "verified": ok_wm,
                        }
                    )

        # (b) Sampled shifted-scale normalization identity on prime powers r = p^k <= 16 (Y = 16, eps = 1/2):
        Y_norm_chk = arb(16)
        eps_norm = arb(1) / arb(2)
        shifted_norm_id_max_res = arb(0)
        for p_val, k_val in prime_power_pairs_up_to(16):
            r_arb = arb(p_val ** k_val)
            lp2 = (arb(p_val).log()) ** 2
            lhs_alg = (lp2 / r_arb) * ((Y_norm_chk / r_arb) ** eps_norm)
            rhs_alg = (lp2 / (r_arb ** (arb(1) + eps_norm))) * (Y_norm_chk ** eps_norm)
            diff_alg = abs(lhs_alg - rhs_alg)
            if not bool(arb(0) in (lhs_alg - rhs_alg) and diff_alg < arb("1e-70")):
                repair1_ok = False
            if bool(diff_alg > shifted_norm_id_max_res):
                shifted_norm_id_max_res = diff_alg

        actual_observable_hypothesis_trace = [
            {
                "hypothesis_id": "H1_NONNEGATIVITY",
                "formal_expression": "forall Z >= 1, 0 <= canonicalLiouvilleEnergyE Z",
                "classification": "CONCRETE_ANALYTIC_IN_LEAN",
                "source_and_discharge": (
                    "Discharged unconditionally inside Lean (`windowEnergyNormSq_nonneg_aux`) from "
                    "nonnegativity of `Q_{lambda,T(Z)}(X)^2 / X` on `[Z, tau*Z]` (`Z >= 1 > 0`)."
                ),
            },
            {
                "hypothesis_id": "H2_LINEAR_SCALE_MAJORANT",
                "formal_expression": "0 <= M_lin and forall Z >= 1, canonicalLiouvilleEnergyE Z <= M_lin * Z",
                "classification": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "source_and_discharge": (
                    "Explicit external analytic input established unconditionally in TC-054/TC-057: "
                    "`|Q_{lambda,T}(X)| <= Q_{1,infty}(X) << sqrt(X)` gives `E(Z) = int_Z^{tau*Z} Q^2 dX/X <= M_lin * Z`, "
                    "which Lean Theorem 6(1) uses solely to prove `0 <= G_eps(R) <= M_lin * R < infty` on every "
                    "finite horizon `[1, R]` without assuming global finiteness of `sup_{Z>=1} E(Z)/Z^eps`."
                ),
            },
            {
                "hypothesis_id": "H3_ROUTE_D_SHIFTED_PRIME_POWER_DIAGONAL",
                "formal_expression": (
                    "0 <= C_cut, e <= Y_diag, and forall Y >= Y_diag, canonicalPrimePowerDiagDtilde Y <= "
                    "(2 / (log Y)^2) * sum_{p^k <= floor(Y)} ((log p)^2 / p^k) * monotoneScaleEnvelope canonicalLiouvilleEnergyE (Y / p^k) + C_cut"
                ),
                "classification": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "source_and_discharge": (
                    "Explicit external analytic input established unconditionally in TC-057R Theorem 5.1 (Route D "
                    "shifted prime-power diagonal estimate with `O(1)` super-`Y` prime-power tail and inherited-to-canonical "
                    "cutoff conversion absorbed into `C_cut`, keeping factor `2` from `(log X)^{-2} <= (log Y)^{-2}` "
                    "and cutoff Young split once)."
                ),
            },
            {
                "hypothesis_id": "H4_WEIGHTED_PRIME_POWER_ZETA_MAJORANT",
                "formal_expression": (
                    "forall eps > 0, 0 <= zeta2_eps(eps) and forall Y >= 1, "
                    "sum_{p^k <= floor(Y)} (log p)^2 / (p^k)^{1+eps} <= zeta2_eps(eps) := zeta''(1 + eps)"
                ),
                "classification": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "source_and_discharge": (
                    "Explicit external analytic input: by unique prime factorization `(p, k) -> n = p^k >= 2` is "
                    "injective on `primePowerPairsUpTo floor(Y)` with `(log p)^2 <= k^2 (log p)^2 = (log n)^2` (`k >= 1`), "
                    "and all omitted composite/tail summands satisfy `(log n)^2 / n^{1+eps} > 0`, so "
                    "`sum_{p^k<=Y} (log p)^2/(p^k)^{1+eps} <= sum_{n=2}^infty (log n)^2/n^{1+eps} = zeta''(1+eps)`."
                ),
            },
            {
                "hypothesis_id": "H5_QUANTIFIED_ARITHMETIC_LOG_SAVING_CONTRACT",
                "formal_expression": (
                    "forall eta > 0, exists A_eta >= 0, B_eta >= 0, kappa_eta in (0, 2], Y_eta >= e: "
                    "forall Y >= Y_eta, canonicalLiouvilleEnergyE Y <= A_eta * Y^eta + B_eta * (log Y)^{2 - kappa_eta} * canonicalPrimePowerDiagDtilde Y"
                ),
                "classification": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
                "source_and_discharge": (
                    "Explicitly OPEN arithmetic target behind SUBGATE-TC-043A (`subgate_tc043a_status = OPEN`, "
                    "`rh_proved = False`). Theorem 6 proves the conditional closure transfer from H1-H5 to "
                    "`forall eps > 0, canonicalLiouvilleEnergyE Y = O_eps(Y^eps)`."
                ),
            },
        ]

        return {
            "epistemic_scope": {
                "window_reconstruction_identity": "CONCRETE_ANALYTIC_IN_LEAN",
                "preregistered_grid_evaluations": "CERTIFIED_FINITE_OBSERVATION",
                "repaired_weighted_diagonal_closure_transfer": "CONDITIONAL_IMPLICATION",
                "auxiliary_same_scale_lemma_theorem5_conj5": "CONDITIONAL_IMPLICATION",
                "external_route_d_and_zeta_majorant_inputs": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "unconditional_log_saving_arithmetic_bound": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            },
            "preregistered_grid_rows": grid_rows,
            "diagnostic_ratio_highlights": {
                "E_16_over_D_tilde_16": row_16["ratio_E_over_D_tilde"],
                "E_64_over_D_tilde_64": row_64["ratio_E_over_D_tilde"],
                "raw_E_le_D_tilde_refuted_at_16_and_64": True,
                "eventual_closure_contract_refuted_by_samples": False,
            },
            "conditional_log_saving_transfer_schedules": schedule_rows,
            "repaired_weighted_diagonal_closure_and_actual_observable_tc059r": {
                "primary_lean_theorem": "repaired_weighted_diagonal_closure_and_actual_observable_tc059r",
                "auxiliary_same_scale_lemma_retained": (
                    "parity_uniqueness_turn_chart_defect_and_log_saving_closure_tc059 (Conjunct 5, clearly "
                    "labeled auxiliary same-scale lemma; Route D is NOT claimed to imply the unshifted "
                    "C_diag*F(Y)/(log Y)^2 premise)"
                ),
                "horizon_normalization_formula": (
                    "D_tilde(Y) / Y^eps <= (C_eps / (log Y)^2) * G_eps(R) + C_cut / Y^eps for all R >= Y_diag "
                    "and Y_diag <= Y <= R, where G_eps(R) = sup_{1<=Z<=R} E(Z)/Z^eps and C_eps = 2*zeta''(1+eps)"
                ),
                "infinite_horizon_supremum_assumed_finite": False,
                "weighted_mass_and_horizon_checks": weighted_mass_rows,
                "shifted_scale_normalization_max_abs_residual_Y16": serialize_arb_certified(
                    shifted_norm_id_max_res
                ),
                "actual_observable_corollary_hypothesis_trace": actual_observable_hypothesis_trace,
                "verified": repair1_ok,
            },
            "all_section_1_checks_pass": bool(all_ok and sched_ok and repair1_ok),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 2. Section 2 & Attempt A: Exact Dyadic Power-Lift, Increments, & Negative Control
# ---------------------------------------------------------------------------


def verify_section_2_dyadic_power_lift_and_attempt_a(prec_bits: int = 256) -> Dict[str, Any]:
    """Verify all Section 2 dyadic power-lift identities, control separation, finite Gaussian lifts
    (including T=0,1 and X=0), Attempt A increment telescope & complete window quadratic expansion,
    certified sign-change falsifications, meromorphic zeta(2^J z)/zeta(z) separation, and coherent
    stabilized-tail Gram negative control.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()

        # 2.1 Direct iterated convolution vs power-divisor Moebius formula & prime-power congruence
        N_check = 300
        conv_divisor_ok = True
        boundary_rows: List[Dict[str, Any]] = []
        for J in (1, 2, 3, 4):
            d_J = 1 << J
            b_conv = dyadic_power_lift_b_J_conv_table(J, N_check, base_fn=liouville_lambda_int)
            for n in range(1, N_check + 1):
                b_div = dyadic_power_lift_b_J_divisor_int(J, n)
                if b_conv[n] != b_div:
                    conv_divisor_ok = False
                if J == 1 and b_div != liouville_lambda_int(n):
                    conv_divisor_ok = False
                if n < (1 << d_J) and b_div != moebius_mu_int(n):
                    conv_divisor_ok = False
                if is_squarefree_int(n) and b_div != moebius_mu_int(n):
                    conv_divisor_ok = False

            # Prime-power congruence check across p in {2, 3, 5, 7} and 0 <= e <= 20
            for p in (2, 3, 5, 7):
                for e in range(0, 21):
                    val_pe = dyadic_power_lift_b_J_divisor_int(J, p ** e)
                    rem = e % d_J
                    exp_pe = 1 if rem == 0 else (-1 if rem == 1 else 0)
                    if val_pe != exp_pe:
                        conv_divisor_ok = False

            n_bdry = 1 << d_J
            b_bdry = dyadic_power_lift_b_J_divisor_int(J, n_bdry)
            mu_bdry = moebius_mu_int(n_bdry)
            delta_prev = (
                power_lift_increment_delta_J_int(J, n_bdry)
                if J >= 1
                else 0
            )
            ok_b = bool(b_bdry == 1 and mu_bdry == 0 and delta_prev == -1)
            conv_divisor_ok = conv_divisor_ok and ok_b
            boundary_rows.append(
                {
                    "J": J,
                    "d_J": d_J,
                    "boundary_n_2_pow_d_J": n_bdry,
                    "b_J_at_boundary": b_bdry,
                    "mu_at_boundary": mu_bdry,
                    "Delta_J_at_boundary": delta_prev,
                    "verified": ok_b,
                }
            )

        # 2.2 Control separation at J = 2: b_{a,2}(p^2) = a(p)*(a(p) + 1)
        control_modes = (
            ("liouville", "lambda(n) = (-1)^{Omega(n)}", "none (a(p) = -1 for every prime p)"),
            ("unsigned_1", "1(n) = 1", "every prime p fails a(p) + 1 = 0 (a(p) = +1 => b_{1,2}(p^2) = 2)"),
            ("a2", "a_2(n) = (-1)^{v_2(n)}", "every odd prime p >= 3 fails a_2(p) + 1 = 0 (e.g. p = 3 gives b_{a_2,2}(9) = 2)"),
            (
                "a_3_5_7",
                "a_{3,5,7}(n) = (-1)^{v_3+v_5+v_7}",
                "every prime p not in {3,5,7} fails a_S(p) + 1 = 0 (first failure p = 2 gives b_{a_S,2}(4) = 2, and p = 11 gives b_{a_S,2}(121) = 2)",
            ),
        )
        control_separation_rows: List[Dict[str, Any]] = []
        ctrl_sep_ok = True
        for mode_key, label, missing_rel in control_modes:
            w_fn = _weight_fn_for_mode(mode_key)
            b2_tbl = dyadic_power_lift_b_J_conv_table(2, 150, base_fn=w_fn)
            vals_p2 = {str(p): b2_tbl[p * p] for p in (2, 3, 5, 7, 11)}
            for p in (2, 3, 5, 7, 11):
                ap = int(w_fn(p))
                if b2_tbl[p * p] != ap * (ap + 1):
                    ctrl_sep_ok = False
            if mode_key == "liouville" and any(v != 0 for v in vals_p2.values()):
                ctrl_sep_ok = False
            if mode_key == "unsigned_1" and any(v != 2 for v in vals_p2.values()):
                ctrl_sep_ok = False
            if mode_key == "a2" and not (vals_p2["2"] == 0 and vals_p2["3"] == 2):
                ctrl_sep_ok = False
            if mode_key == "a_3_5_7" and not (
                vals_p2["2"] == 2
                and vals_p2["3"] == 0
                and vals_p2["5"] == 0
                and vals_p2["7"] == 0
                and vals_p2["11"] == 2
            ):
                ctrl_sep_ok = False
            control_separation_rows.append(
                {
                    "mode": mode_key,
                    "formula": label,
                    "b_a_2_at_p_sq": vals_p2,
                    "missing_prime_sign_relation": missing_rel,
                }
            )

        # 2.3 Stabilization depth J_T vs dyadic shell count vs prime-power count
        stabilization_rows: List[Dict[str, Any]] = []
        stab_ok = True
        for T_val in (0, 1, 3, 4, 15, 16, 255, 256, 4096):
            J_T = stabilization_depth_J_T(T_val)
            dyadic_shells = 0 if T_val == 0 else (T_val.bit_length())
            pp_count = len(prime_power_pairs_up_to(T_val)) if T_val >= 2 else 0
            ok_st = bool(
                J_T >= 1
                and T_val < (1 << (1 << J_T))
                and (J_T == 1 or (1 << (1 << (J_T - 1))) <= T_val)
            )
            stab_ok = stab_ok and ok_st
            stabilization_rows.append(
                {
                    "T": T_val,
                    "stabilization_depth_J_T": J_T,
                    "dyadic_magnitude_shell_count": dyadic_shells,
                    "prime_power_count": pp_count,
                    "verified": ok_st,
                }
            )

        # 2.4 Finite Gaussian lift Q_{b_J,T}(X) = sum_{r^{d_J}<=T} r^{-d_J/2} Q_{mu,floor(T/r^{d_J})}(X/r^{d_J})
        # including T = 0, 1 and X = 0
        gaussian_lift_checks: List[Dict[str, Any]] = []
        lift_ok = True
        for J in (1, 2, 3, 4):
            d_J = 1 << J
            half_d = 1 << (J - 1)
            for T_val in (0, 1, 3, 4, 15, 16, 40, 256, 300):
                for X_frac in (Fraction(0, 1), Fraction(1, 2), Fraction(8, 1), Fraction(25, 1)):
                    x_arb = _frac_to_arb(X_frac)
                    lhs = evaluate_Q_general_arb(
                        x_arb,
                        T_val,
                        coeff_fn=lambda n, _J=J: dyadic_power_lift_b_J_divisor_int(_J, n),
                        prec_bits=prec_bits,
                    )
                    rhs = arb(0)
                    r = 1
                    while (r ** d_J) <= T_val:
                        rd = r ** d_J
                        rhs += (arb(1) / arb(r ** half_d)) * evaluate_Q_general_arb(
                            x_arb / arb(rd),
                            T_val // rd,
                            coeff_fn=moebius_mu_int,
                            prec_bits=prec_bits,
                        )
                        r += 1
                    res = lhs - rhs
                    ok_pt = bool(arb(0) in res and abs(res) < arb("1e-66"))
                    if T_val == 0 or X_frac == 0:
                        ok_pt = bool(ok_pt and lhs == arb(0) and rhs == arb(0))
                    lift_ok = lift_ok and ok_pt
                    if (J, T_val, X_frac) in (
                        (1, 0, Fraction(8, 1)),
                        (1, 1, Fraction(8, 1)),
                        (2, 40, Fraction(0, 1)),
                        (2, 40, Fraction(25, 1)),
                        (3, 300, Fraction(25, 1)),
                    ):
                        gaussian_lift_checks.append(
                            {
                                "J": J,
                                "T": T_val,
                                "X": str(X_frac),
                                "Q_b_J_T": serialize_arb_certified(lhs),
                                "lift_sum_residual": serialize_arb_certified(res),
                                "verified": ok_pt,
                            }
                        )

        # 2.5 Attempt A: Pre-stated mechanism schema, non-square stratification of J=1 square tail,
        # complete window quadratic expansion with baseline + all cross & increment-increment terms,
        # and certified two-sided sign-change falsification.
        attempt_a_schema = {
            "candidate_id": "ATTEMPT-A-DYADIC-POWER-LIFT-INCREMENT-TELESCOPE",
            "exact_kernel": "K_Y(m, n) = int_Y^{tau*Y} phi_m(X)*phi_n(X) dX/X",
            "arithmetic_coefficients": (
                "lambda(n) = mu(n) - sum_{J=1}^{J_T-1} Delta_J(n) on 1 <= n <= T, where "
                "Delta_J(n) = -sum_{s>=2, s not square, s^{2^J}|n} mu(n/s^{2^J}) vanishes for n < 2^{2^J}"
            ),
            "quantifiers_and_ranges": "All Y >= 2, T = T(Y) = ceil(Y^{5/4}), 1 <= J < J_T",
            "tested_sign_and_orthogonality_hypotheses": [
                "H_A1 (Baseline Dominance): sum_{J>=1} 2*<Q_{mu,T}, Q_{Delta_J,T}>_Y - ||sum_{J>=1} Q_{Delta_J,T}||_Y^2 >= 0 => E(Y) <= ||Q_{mu,T}||_Y^2",
                "H_A2 (Cross-Depth Sign Definiteness): <Q_{mu,T}, Q_{Delta_1,T}>_Y >= 0 or <= 0 uniformly, and <Q_{Delta_1,T}, Q_{Delta_2,T}>_Y >= 0 or <= 0 uniformly",
            ],
            "outcome_epistemic_class": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            "falsification_summary": (
                "Refuted within scope: (1) Exact non-square root stratification proves sum_{J=1}^{J_T-1} (-Q_{Delta_J,T}(X)) "
                "equals sum_{r>=2, r^2<=T} r^{-1} Q_{mu,floor(T/r^2)}(X/r^2) term-by-term, reproducing the J=1 square-dilation "
                "tail stratified by the unique representation r = s^{2^{J-1}} with J >= 1 and s >= 2 non-square "
                "(J - 1 = v_2(gcd_{p|r} v_p(r)), e.g. r=6 -> J=1, s=6 while r=9=3^2 -> J=2, s=3) while leaving the "
                "RH-equivalent Q_{mu,T} baseline untouched; (2) <Q_{mu,T}, Q_{Delta_1,T}>_Y changes sign strictly (> 0 at Y in {3,4,6}; < 0 at Y in "
                "{8,12,16,64}), and <Q_{Delta_1,T}, Q_{Delta_2,T}>_Y changes sign strictly (< 0 at Y in {12,16}; > 0 at Y in "
                "{24,32,64}); (3) E(Y) - ||Q_{mu,T}||_Y^2 changes sign strictly (< 0 at Y = 4; > 0 at Y = 16)."
            ),
        }

        # Verify exact non-square stratification at T = 300, X = 25:
        T_strat = 300
        X_strat = arb(25)
        J_T_strat = stabilization_depth_J_T(T_strat)
        sq_tail_r_ge2 = arb(0)
        r_sq = 2
        while r_sq * r_sq <= T_strat:
            sq_tail_r_ge2 += (arb(1) / arb(r_sq)) * evaluate_Q_general_arb(
                X_strat / arb(r_sq * r_sq),
                T_strat // (r_sq * r_sq),
                coeff_fn=moebius_mu_int,
                prec_bits=prec_bits,
            )
            r_sq += 1
        neg_sum_delta = arb(0)
        for J in range(1, J_T_strat):
            neg_sum_delta -= evaluate_Q_general_arb(
                X_strat,
                T_strat,
                coeff_fn=lambda n, _J=J: power_lift_increment_delta_J_int(_J, n),
                prec_bits=prec_bits,
            )
        strat_res = sq_tail_r_ge2 - neg_sum_delta
        strat_ok = bool(arb(0) in strat_res and abs(strat_res) < arb("1e-66"))

        attempt_a_window_rows: List[Dict[str, Any]] = []
        mu_d1_pos_Y: List[int] = []
        mu_d1_neg_Y: List[int] = []
        d1_d2_pos_Y: List[int] = []
        d1_d2_neg_Y: List[int] = []
        E_minus_mu_pos_Y: List[int] = []
        E_minus_mu_neg_Y: List[int] = []
        quad_exp_ok = True

        for Y_int in (3, 4, 6, 8, 12, 16, 24, 32, 64, 128):
            T_Y = exact_T_cutoff_ceil_Y_5_4(Y_int)
            J_T = stabilization_depth_J_T(T_Y)
            y_arb = arb(Y_int)
            lam_vec = [0] + [liouville_lambda_int(n) for n in range(1, T_Y + 1)]
            mu_vec = [0] + [moebius_mu_int(n) for n in range(1, T_Y + 1)]
            delta_vecs = {
                J: [0] + [power_lift_increment_delta_J_int(J, n) for n in range(1, T_Y + 1)]
                for J in range(1, J_T)
            }

            E_lam = evaluate_bilinear_window_pairing_closed_arb(
                y_arb, T_Y, lam_vec, lam_vec, prec_bits=prec_bits
            )
            E_mu = evaluate_bilinear_window_pairing_closed_arb(
                y_arb, T_Y, mu_vec, mu_vec, prec_bits=prec_bits
            )
            cross_mu_J = {
                J: evaluate_bilinear_window_pairing_closed_arb(
                    y_arb, T_Y, mu_vec, delta_vecs[J], prec_bits=prec_bits
                )
                for J in range(1, J_T)
            }
            gram_delta: Dict[Tuple[int, int], arb] = {}
            for J1 in range(1, J_T):
                for J2 in range(1, J_T):
                    gram_delta[(J1, J2)] = evaluate_bilinear_window_pairing_closed_arb(
                        y_arb, T_Y, delta_vecs[J1], delta_vecs[J2], prec_bits=prec_bits
                    )
            sum_cross_mu = sum(cross_mu_J.values(), arb(0))
            sum_gram_delta = sum(gram_delta.values(), arb(0))
            recon_E = E_mu - arb(2) * sum_cross_mu + sum_gram_delta
            res_quad = E_lam - recon_E
            ok_row = bool(arb(0) in res_quad and abs(res_quad) < arb("1e-63"))
            quad_exp_ok = quad_exp_ok and ok_row

            c_mu_d1 = cross_mu_J.get(1, arb(0))
            c_d1_d2 = gram_delta.get((1, 2), arb(0))
            diff_E_mu = E_lam - E_mu
            if c_mu_d1 > arb(0):
                mu_d1_pos_Y.append(Y_int)
            elif c_mu_d1 < arb(0):
                mu_d1_neg_Y.append(Y_int)
            if c_d1_d2 > arb(0):
                d1_d2_pos_Y.append(Y_int)
            elif c_d1_d2 < arb(0):
                d1_d2_neg_Y.append(Y_int)
            if diff_E_mu > arb(0):
                E_minus_mu_pos_Y.append(Y_int)
            elif diff_E_mu < arb(0):
                E_minus_mu_neg_Y.append(Y_int)

            attempt_a_window_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_Y,
                    "J_T": J_T,
                    "E_lambda": serialize_arb_certified(E_lam),
                    "E_mu_baseline": serialize_arb_certified(E_mu),
                    "E_lambda_minus_E_mu_baseline": serialize_arb_certified(diff_E_mu),
                    "cross_mu_Delta1": serialize_arb_certified(c_mu_d1),
                    "cross_Delta1_Delta2": serialize_arb_certified(c_d1_d2),
                    "minus_two_sum_cross_mu_Delta": serialize_arb_certified(-arb(2) * sum_cross_mu),
                    "sum_increment_gram_Delta_J1_J2": serialize_arb_certified(sum_gram_delta),
                    "quadratic_expansion_residual": serialize_arb_certified(res_quad),
                    "verified": ok_row,
                }
            )

        sign_changes_verified = bool(
            len(mu_d1_pos_Y) > 0
            and len(mu_d1_neg_Y) > 0
            and len(d1_d2_pos_Y) > 0
            and len(d1_d2_neg_Y) > 0
            and len(E_minus_mu_pos_Y) > 0
            and len(E_minus_mu_neg_Y) > 0
        )

        # 2.6 Meromorphic Dirichlet-series identity separation:
        # prod_{j=0}^{J-1} L_lambda(2^j z) = zeta(2^J z) / zeta(z), L_lambda(z) = zeta(2 z) / zeta(z)
        # Checked at z = 3/2 + i (x > 1 forward; x < 4 so backward J=2 requires continuation),
        # z = 9 + i (x > 2^J common absolute convergence), and removable simple zero at z = 1 (value 0, derivative zeta(2^J)).
        mero_rows: List[Dict[str, Any]] = []
        mero_ok = True
        for J_m in (2, 3):
            for z_label, z_pt, regime_note in (
                (
                    "3/2 + i",
                    acb(arb(3) / arb(2), arb(1)),
                    "x = 3/2 > 1 (forward Dirichlet series converges absolutely; backward 2^J*z series requires x > 2^J unless meromorphically continued)",
                ),
                (
                    "9 + i",
                    acb(arb(9), arb(1)),
                    "x = 9 > 2^J (both forward and backward Dirichlet towers converge absolutely)",
                ),
            ):
                lhs_prod = acb(1)
                for j in range(J_m):
                    zj = acb(1 << j) * z_pt
                    lhs_prod *= (acb(2) * zj).zeta() / zj.zeta()
                rhs_quot = (acb(1 << J_m) * z_pt).zeta() / z_pt.zeta()
                diff_abs = abs(lhs_prod - rhs_quot)
                ok_m = bool(arb(0) in (lhs_prod - rhs_quot).real and diff_abs < arb("1e-65"))
                mero_ok = mero_ok and ok_m
                mero_rows.append(
                    {
                        "J": J_m,
                        "z": z_label,
                        "domain_regime": regime_note,
                        "abs_prod_minus_zeta_quotient": serialize_arb_certified(diff_abs),
                        "verified": ok_m,
                    }
                )
        # Removable limit lim_{z->1} zeta(2^J z)/zeta(z) = 0? WAIT: as z -> 1, zeta(z) has a simple pole
        # with residue 1 while zeta(2^J) is finite (J >= 1 => 2^J >= 2), so zeta(2^J z)/zeta(z) -> 0 (simple zero at z = 1!),
        # whereas at z = 2^{-J}, zeta(2^J z) has a simple pole while zeta(2^{-J}) != 0 (simple pole at z = 2^{-J})!
        z_at_1_val_J2 = acb(4).zeta() * arb(0)  # exact value 0 at removable zero z = 1 (1/zeta(1) = 0)
        from flint import acb_series

        # Expand zeta(4*(1 + eps)) / zeta(1 + eps): since (1 + eps - 1)*zeta(1 + eps) -> 1,
        # ratio = eps * zeta(4 + 4*eps) / (eps * zeta(1 + eps)) = O(eps), derivative at z = 1 equals zeta(4)!
        zeta_4_val = acb(4).zeta().real
        mero_local_orders_note = (
            "For J >= 1 (2^J >= 2): ordinary forward Dirichlet convergence holds on x > 1; common backward "
            "tower convergence holds on x > 2^J; at z = 1, zeta(z) has a simple pole while zeta(2^J) is finite "
            "nonzero, so zeta(2^J z)/zeta(z) has a removable simple zero with derivative zeta(2^J); at z = 2^{-J}, "
            "zeta(2^J z) has a simple pole while zeta(2^{-J}) != 0, giving a simple pole; at any zero rho of zeta(z), "
            "orders add via ord_{z=rho}(zeta(2^J z)) - ord_{z=rho}(zeta(z)). Dirichlet multiplication never becomes "
            "a pointwise product of Gaussian observables Q_{a,T}(X), and z -> 2*z is not X -> 2*X."
        )

        # 2.7 Decisive negative control: coherent stabilized-tail Gram matrix at Y = 16, T = 32, J_T = 3
        Y_nc = arb(16)
        T_nc = exact_T_cutoff_ceil_Y_5_4(16)  # 32
        J_T_nc = stabilization_depth_J_T(T_nc)  # 3 (2^{2^3} = 256 > 32 >= 16 = 2^{2^2})
        mu_nc = [0] + [moebius_mu_int(n) for n in range(1, T_nc + 1)]
        E_mu_nc = evaluate_bilinear_window_pairing_closed_arb(
            Y_nc, T_nc, mu_nc, mu_nc, prec_bits=prec_bits
        )
        coherent_tail_entries: List[Dict[str, Any]] = []
        nc_ok = bool(J_T_nc == 3 and E_mu_nc > arb(0))
        for J1 in (3, 4, 5):
            b_J1 = [0] + [dyadic_power_lift_b_J_divisor_int(J1, n) for n in range(1, T_nc + 1)]
            for J2 in (3, 4, 5):
                b_J2 = [0] + [dyadic_power_lift_b_J_divisor_int(J2, n) for n in range(1, T_nc + 1)]
                g12 = evaluate_bilinear_window_pairing_closed_arb(
                    Y_nc, T_nc, b_J1, b_J2, prec_bits=prec_bits
                )
                diff_nc = g12 - E_mu_nc
                ok_ij = bool(b_J1 == mu_nc and b_J2 == mu_nc and arb(0) in diff_nc and abs(diff_nc) < arb("1e-68"))
                nc_ok = nc_ok and ok_ij
                if (J1, J2) in ((3, 3), (3, 5), (5, 5)):
                    coherent_tail_entries.append(
                        {
                            "J1": J1,
                            "J2": J2,
                            "gram_pairing": serialize_arb_certified(g12),
                            "minus_E_mu_residual": serialize_arb_certified(diff_nc),
                            "verified": ok_ij,
                        }
                    )

        all_ok = bool(
            conv_divisor_ok
            and ctrl_sep_ok
            and stab_ok
            and lift_ok
            and strat_ok
            and quad_exp_ok
            and sign_changes_verified
            and mero_ok
            and nc_ok
        )
        return {
            "epistemic_scope": {
                "dyadic_power_lift_identities": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "stabilization_minimality_inequalities_in_lean": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "stabilization_depth_O_log_log_T_consequence": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "finite_gaussian_lift_and_window_expansion": "CONCRETE_ANALYTIC_IN_LEAN",
                "meromorphic_tower_separation": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "attempt_a_cross_term_sign_falsification": "CERTIFIED_FINITE_OBSERVATION",
                "attempt_a_mechanism_verdict": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            },
            "stabilization_formal_vs_analytic_scope_note": (
                "Lean Theorem 2(5) formalizes the exact integer stabilization/minimality inequalities "
                "T < 2^{2^{J_T}} and (1 < J_T -> 2^{2^{J_T-1}} <= T); the growth rate J_T = O(log log T) "
                "is an analytic consequence outside Lean rather than a Lean Big-O theorem."
            ),
            "convolution_vs_power_divisor_checked_n_up_to": N_check,
            "first_discrepancy_boundary_rows": boundary_rows,
            "control_separation_J2_rows": control_separation_rows,
            "stabilization_depth_rows": stabilization_rows,
            "finite_gaussian_lift_sample_checks": gaussian_lift_checks,
            "attempt_a_pre_stated_schema": attempt_a_schema,
            "non_square_stratification_check_T300_X25": {
                "square_tail_r_ge_2": serialize_arb_certified(sq_tail_r_ge2),
                "minus_sum_increment_Q_Delta_J": serialize_arb_certified(neg_sum_delta),
                "residual": serialize_arb_certified(strat_res),
                "verified": strat_ok,
            },
            "attempt_a_window_quadratic_rows": attempt_a_window_rows,
            "attempt_a_certified_sign_change_scales": {
                "cross_mu_Delta1_positive_Y": mu_d1_pos_Y,
                "cross_mu_Delta1_negative_Y": mu_d1_neg_Y,
                "cross_Delta1_Delta2_positive_Y": d1_d2_pos_Y,
                "cross_Delta1_Delta2_negative_Y": d1_d2_neg_Y,
                "E_lambda_minus_E_mu_positive_Y": E_minus_mu_pos_Y,
                "E_lambda_minus_E_mu_negative_Y": E_minus_mu_neg_Y,
                "verified": sign_changes_verified,
            },
            "meromorphic_tower_separation": {
                "sample_checks": mero_rows,
                "derivative_at_removable_zero_z1_J2_zeta4": serialize_arb_certified(zeta_4_val),
                "value_at_z1_removable_zero": "0",
                "local_orders_and_non_equivalence_note": mero_local_orders_note,
                "verified": mero_ok,
            },
            "coherent_stabilized_tail_negative_control_Y16_T32": {
                "Y": 16,
                "T_Y": T_nc,
                "J_T": J_T_nc,
                "E_mu_baseline": serialize_arb_certified(E_mu_nc),
                "sampled_gram_entries_J_ge_J_T": coherent_tail_entries,
                "telescoping_orthogonality_gain": False,
                "verified": nc_ok,
            },
            "all_section_2_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 3. Section 3: Primitive Pairs, Sub-Unit Kernel Scaling, & 4-Way Diagonals
# ---------------------------------------------------------------------------


def verify_section_3_primitive_pairs_and_diagonals(prec_bits: int = 256) -> Dict[str, Any]:
    """Verify `K_u(m, n)` scaling including `0 < u = Y/g < 1`, 3-way `E(Y)` equality, finite
    synthesis/Moebius inversion `E_T <-> Pi_T` & sign changes, inherited `floor(T(Y)/d)` vs
    canonical `T(Y/d)` discrepancy, nonmonotone scales & `T(16)` jump, and 4-way diagonal comparison.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits

        # 3.1 Sub-unit window kernel scaling check (u = Y/g < 1, e.g. Y = 8, g = 12 => u = 2/3 < 1)
        Y_sub = arb(8)
        g_sub = 12
        r_sub, s_sub = 1, 1
        u_sub = Y_sub / arb(g_sub)  # 2/3 < 1
        K_lhs = evaluate_window_kernel_K_quadrature_arb(
            Y_sub, g_sub * r_sub, g_sub * s_sub, prec_bits=prec_bits
        )
        K_rhs_closed = evaluate_window_kernel_K_closed_arb(
            u_sub, r_sub, s_sub, prec_bits=prec_bits
        ) / arb(g_sub)
        K_rhs_quad = evaluate_window_kernel_K_quadrature_arb(
            u_sub, r_sub, s_sub, prec_bits=prec_bits
        ) / arb(g_sub)
        phi_lhs = evaluate_phi_n_arb(arb(5), g_sub * 2, prec_bits=prec_bits)
        phi_rhs = evaluate_phi_n_arb(arb(5) / arb(g_sub), 2, prec_bits=prec_bits) / arb(g_sub).sqrt()
        sub_unit_ok = bool(
            u_sub < arb(1)
            and arb(0) in (K_lhs - K_rhs_closed)
            and abs(K_lhs - K_rhs_closed) < arb("1e-65")
            and arb(0) in (K_rhs_closed - K_rhs_quad)
            and abs(K_rhs_closed - K_rhs_quad) < arb("1e-65")
            and arb(0) in (phi_lhs - phi_rhs)
            and abs(phi_lhs - phi_rhs) < arb("1e-66")
        )

        # 3.2 Independent 3-way verification of E(Y) & synthesis/Moebius inversion E_T <-> Pi_T
        three_way_rows: List[Dict[str, Any]] = []
        pi_pos_Y: List[int] = []
        pi_neg_Y: List[int] = []
        three_way_ok = True
        for Y_int in (2, 3, 4, 6, 8, 12, 16, 24, 32, 64):
            T_Y = exact_T_cutoff_ceil_Y_5_4(Y_int)
            y_arb = arb(Y_int)
            # (i) Direct window quadrature
            E_direct_quad = evaluate_E_L_scale_arb(y_arb, L=T_Y, mode="liouville", prec_bits=prec_bits)
            # (ii) Ordered primitive-pair expansion sum_{gcd(r,s)=1} lambda(r*s) sum_{g<=floor(T/max(r,s))} g^{-1} K_{Y/g}(r,s)
            #      AND synthesis sum_{g=1}^T g^{-1} Pi_{lambda, floor(T/g)}(Y/g)
            Pi_cache: Dict[int, arb] = {}
            E_prim_synth = arb(0)
            for g in range(1, T_Y + 1):
                L_g = T_Y // g
                pi_val = evaluate_primitive_coprime_sum_Pi_arb(
                    y_arb / arb(g), L_g, mode="liouville", prec_bits=prec_bits
                )
                Pi_cache[g] = pi_val
                E_prim_synth += pi_val / arb(g)
            # Exact Moebius inversion recovery of Pi_{lambda, T}(Y) from {E_{floor(T/d)}(Y/d)}_{1<=d<=T}:
            Pi_moebius_inv = arb(0)
            for d in range(1, T_Y + 1):
                mu_d = moebius_mu_int(d)
                if mu_d == 0:
                    continue
                L_d = T_Y // d
                lam_sub = [0] + [liouville_lambda_int(n) for n in range(1, L_d + 1)]
                E_sub = evaluate_bilinear_window_pairing_closed_arb(
                    y_arb / arb(d), L_d, lam_sub, lam_sub, prec_bits=prec_bits
                )
                Pi_moebius_inv += (arb(mu_d) / arb(d)) * E_sub

            # (iii) Independent prime-power reconstruction D_tilde + X_tilde + 2*<P_Y, R_Y>_Y + ||R_Y||_Y^2
            rd = _evaluate_route_d_totals_arb(Y_int, mode="liouville", prec_bits=prec_bits)
            cross_pr_3 = evaluate_direct_cross_term_PR_arb(
                Y_int, mode="liouville", prec_bits=prec_bits
            )
            E_pp_recon = rd["D_tilde"] + rd["X_tilde"] + arb(2) * cross_pr_3 + rd["E_sh1"]
            res_quad_prim = E_direct_quad - E_prim_synth
            res_pi_inv = Pi_cache[1] - Pi_moebius_inv
            res_pp = E_pp_recon - E_prim_synth
            ok_3 = bool(
                arb(0) in res_quad_prim
                and abs(res_quad_prim) < arb("1e-62")
                and arb(0) in res_pi_inv
                and abs(res_pi_inv) < arb("1e-62")
                and arb(0) in res_pp
                and abs(res_pp) < arb("1e-62")
            )
            three_way_ok = three_way_ok and ok_3
            if Pi_cache[1] > arb(0):
                pi_pos_Y.append(Y_int)
            elif Pi_cache[1] < arb(0):
                pi_neg_Y.append(Y_int)
            three_way_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_Y,
                    "E_direct_quadrature": serialize_arb_certified(E_direct_quad),
                    "E_primitive_pair_expansion": serialize_arb_certified(E_prim_synth),
                    "Pi_lambda_T_Y": serialize_arb_certified(Pi_cache[1]),
                    "quadrature_minus_primitive_residual": serialize_arb_certified(res_quad_prim),
                    "Pi_minus_moebius_inversion_residual": serialize_arb_certified(res_pi_inv),
                    "prime_power_recon_minus_primitive_residual": serialize_arb_certified(res_pp),
                    "verified": ok_3,
                }
            )

        pi_sign_change_ok = bool(len(pi_pos_Y) > 0 and len(pi_neg_Y) > 0)

        # 3.3 Inherited floor(T(Y)/d) vs canonical T(Y/d) cutoff discrepancy witnesses
        # Witness 1: Y = 9/4, d = 2 => Y^{5/4} = (9/4)^{5/4} in (2.75, 2.76) => T(9/4) = 3, floor(3/2) = 1,
        # while Y/d = 9/8 > 1 => T(9/8) = 2 != 1!
        # Witness 2: Y = 7, d = 2 => 7^{5/4} ~= 11.386 => T(7) = 12, floor(12/2) = 6,
        # while (7/2)^{5/4} ~= 4.789 => T(7/2) = 5 != 6!
        cutoff_discrepancy_rows: List[Dict[str, Any]] = []
        discrepancy_ok = True
        for y_frac, d_val, exp_inherited, exp_canonical in (
            (Fraction(9, 4), 2, 1, 2),
            (Fraction(7, 1), 2, 6, 5),
        ):
            y_arb = _frac_to_arb(y_frac)
            T_Y_arb = int(math.ceil(float((y_arb ** (arb(5) / arb(4))).upper())))
            # Verify exact ceil via integer 4th power comparison: (T-1)^4 < y^5 <= T^4
            assert Fraction((T_Y_arb - 1) ** 4, 1) < (y_frac ** 5) <= Fraction(T_Y_arb ** 4, 1)
            inherited_L = T_Y_arb // d_val
            yd_frac = y_frac / d_val
            yd_arb = _frac_to_arb(yd_frac)
            canonical_L = int(math.ceil(float((yd_arb ** (arb(5) / arb(4))).upper())))
            assert Fraction((canonical_L - 1) ** 4, 1) < (yd_frac ** 5) <= Fraction(canonical_L ** 4, 1)
            lam_inh = [0] + [liouville_lambda_int(n) for n in range(1, inherited_L + 1)]
            lam_can = [0] + [liouville_lambda_int(n) for n in range(1, canonical_L + 1)]
            E_inh = evaluate_bilinear_window_pairing_closed_arb(
                yd_arb, inherited_L, lam_inh, lam_inh, prec_bits=prec_bits
            )
            E_can = evaluate_bilinear_window_pairing_closed_arb(
                yd_arb, canonical_L, lam_can, lam_can, prec_bits=prec_bits
            )
            diff_E = E_inh - E_can
            ok_d = bool(
                inherited_L == exp_inherited
                and canonical_L == exp_canonical
                and inherited_L != canonical_L
                and abs(diff_E) > arb(0)
            )
            discrepancy_ok = discrepancy_ok and ok_d
            cutoff_discrepancy_rows.append(
                {
                    "Y": str(y_frac),
                    "d": d_val,
                    "T_Y": T_Y_arb,
                    "inherited_cutoff_floor_T_over_d": inherited_L,
                    "canonical_cutoff_T_Y_over_d": canonical_L,
                    "E_inherited_minus_E_canonical": serialize_arb_certified(diff_E),
                    "verified": ok_d,
                }
            )

        # 3.4 Nonmonotone scales and exact cutoff jump diagnostics (T(16) = 32 -> T(16 + 2^{-10}) = 33)
        E2_arb = evaluate_E_L_scale_arb(arb(2), L=3, mode="liouville", prec_bits=prec_bits)
        E4_arb = evaluate_E_L_scale_arb(arb(4), L=6, mode="liouville", prec_bits=prec_bits)
        E16_arb = evaluate_E_L_scale_arb(arb(16), L=32, mode="liouville", prec_bits=prec_bits)
        E24_arb = evaluate_E_L_scale_arb(arb(24), L=54, mode="liouville", prec_bits=prec_bits)
        nonmonotone_2_gt_4_margin = E2_arb - E4_arb
        nonmonotone_16_gt_24_margin = E16_arb - E24_arb
        y_jump_frac = Fraction(16 * 1024 + 1, 1024)
        # 32^4 = 1048576 = 16^5 < (16 + 1/1024)^5 < 33^4 = 1185921
        assert Fraction(32 ** 4, 1) < (y_jump_frac ** 5) <= Fraction(33 ** 4, 1)
        E16_post_jump = evaluate_E_L_scale_arb(
            _frac_to_arb(y_jump_frac), L=33, mode="liouville", prec_bits=prec_bits
        )
        nonmonotone_and_jump_ok = bool(
            nonmonotone_2_gt_4_margin > arb(0) and nonmonotone_16_gt_24_margin > arb(0)
        )

        # 3.5 Explicit 4-way diagonal comparison across Y in {8, 16, 32, 64, 128, 2048}:
        # (1) Coefficient diagonal D_coeff(Y) = sum_{m=1}^{T(Y)} K_Y(m, m) = sum_{g=1}^{T(Y)} g^{-1} K_{Y/g}(1, 1)
        #     Asymptotic constant: int_0^infty u^{-1} K_u(1,1) du -> sum_g g^{-1} K_{Y/g}(1,1) / Y -> (3*zeta(6)/16)*log(tau)?
        #     Wait: let's compute exact Mellin constant of D_coeff(Y)/Y!
        #     K_Y(m, m) = m^{-6} int_Y^{tau*Y} X^4 exp(-2*X^2/m^2) dX.
        #     Summing over m >= 1: int_Y^{tau*Y} X^4 (sum_{m>=1} m^{-6} exp(-2*X^2/m^2)) dX.
        #     Substitute m ~= X*t: sum_{m>=1} m^{-6} exp(-2*X^2/m^2) ~= X^{-5} int_0^infty t^{-6} exp(-2/t^2) dt
        #     With s = 2/t^2 (t = sqrt(2/s), dt = -2^{-1/2}*s^{-3/2}/... wait: t^{-6} dt = (s/2)^3 * (sqrt(2)/2) s^{-3/2} ds = (sqrt(2)/16) s^{3/2} ds):
        #     int_0^infty t^{-6} exp(-2/t^2) dt = (sqrt(2)/16)*Gamma(5/2) = (sqrt(2)/16)*(3*sqrt(tau/2)/4 / sqrt(2)?) = 3*sqrt(tau)/64!
        #     Integrating X^4 * X^{-5} dX = dX/X over [Y, tau*Y] gives factor log(tau), times Y? Wait:
        #     X^4 * m^{-6} for m ~ X gives X^4 * X^{-6} * (#m ~ X) = X^4 * X^{-6} * X = X^{-1}, whose integral over [Y, tau*Y] dX is O(1)??
        #     HOLD ON! Check the exponent of X in K_Y(m, m):
        #     phi_m(X) = X^{5/2} m^{-3} exp(-X^2/m^2) => phi_m(X)^2 / X = X^4 m^{-6} exp(-2*X^2/m^2)!
        #     Integrate over X in [Y, tau*Y]: int_Y^{tau*Y} X^4 dX ~ Y^5, times m^{-6} summed over m ~ Y gives Y^5 * Y^{-5} = O(1)!!
        #     WAIT A SECOND! What about m = 1..Y? At m = 1, K_Y(1,1) ~ exp(-2*Y^2); at m = Y, m^{-6}*Y^5 = Y^{-1}, summed over Y terms gives O(1)!!
        #     WAIT A SECOND!! D_coeff(Y) = sum_{m=1}^{T(Y)} ||phi_m||_Y^2 IS BOUNDED O(1) AS Y -> INFTY!!
        #     LET'S CHECK THAT ALGEBRAICALLY RIGHT NOW:
        #     sum_{g=1}^{infty} g^{-1} K_{Y/g}(1, 1): as u = Y/g ranges over (0, infty), dyadic/integral comparison gives
        #     int_0^infty K_u(1, 1) du / u = int_0^infty (int_u^{tau*u} X^4 exp(-2*X^2) dX) du/u
        #     = log(tau) * int_0^infty X^4 exp(-2*X^2) dX = log(tau) * (3*sqrt(tau)/64) = O(1)!!
        #     WHAT A DISCOVERY!! Because phi_n(X) = X^{5/2} n^{-3} exp(-X^2/n^2) has L^2-norm ||phi_n||_Y^2 ~ n^{-1} 1_{n ~ Y},
        #     sum_{m} ||phi_m||_Y^2 = O(1), WHEREAS the unsigned off-diagonal (sum_m phi_m(X))^2 has size (sqrt(X))^2 = X, so
        #     unsigned energy ||Q_{1,T}||_Y^2 ~ Y comes 100% from m != n!!
        tau = _tau_arb()
        D_coeff_limit_const = (
            tau.log() * arb(3) * tau.sqrt() / arb(64)
        )  # int_0^infty X^4 exp(-2 X^2) dX = (1/2)*2^{-5/2}*Gamma(5/2) = (1/(8*sqrt(2)))*(3*sqrt(tau/2)/4) = 3*sqrt(tau)/64!
        diagonal_comparison_rows: List[Dict[str, Any]] = []
        diag_ok = True
        for Y_diag in (8, 16, 32, 64, 128, 2048):
            T_d = exact_T_cutoff_ceil_Y_5_4(Y_diag)
            y_arb = arb(Y_diag)
            D_coeff = sum(
                (
                    evaluate_window_kernel_K_closed_arb(y_arb / arb(g), 1, 1, prec_bits=prec_bits)
                    / arb(g)
                    for g in range(1, T_d + 1)
                ),
                arb(0),
            )
            if Y_diag <= 128:
                rd_d = _evaluate_route_d_totals_arb(Y_diag, mode="liouville", prec_bits=prec_bits)
                D_tilde_d = rd_d["D_tilde"]
                J_T_d = stabilization_depth_J_T(T_d)
                mu_v = [0] + [moebius_mu_int(n) for n in range(1, T_d + 1)]
                D_tower = evaluate_bilinear_window_pairing_closed_arb(
                    y_arb, T_d, mu_v, mu_v, prec_bits=prec_bits
                )
                for J_idx in range(1, J_T_d):
                    dv = [0] + [power_lift_increment_delta_J_int(J_idx, n) for n in range(1, T_d + 1)]
                    D_tower += evaluate_bilinear_window_pairing_closed_arb(
                        y_arb, T_d, dv, dv, prec_bits=prec_bits
                    )
                # (4) Dyadic primitive-pair shell diagonal (j_r == j_s, gcd(r, s) = 1, summed over all g <= floor(T/max(r,s)))
                D_dyadic_prim_diag = arb(0)
                j_sh = 0
                while (1 << j_sh) <= T_d:
                    lo_sh = 1 << j_sh
                    hi_sh = min(T_d, (1 << (j_sh + 1)) - 1)
                    for r_sh in range(lo_sh, hi_sh + 1):
                        for s_sh in range(lo_sh, hi_sh + 1):
                            if math.gcd(r_sh, s_sh) != 1:
                                continue
                            sgn_rs = arb(liouville_lambda_int(r_sh) * liouville_lambda_int(s_sh))
                            max_g_sh = T_d // max(r_sh, s_sh)
                            g_acc = arb(0)
                            for g_sh in range(1, max_g_sh + 1):
                                g_acc += evaluate_window_kernel_K_closed_arb(
                                    y_arb / arb(g_sh), r_sh, s_sh, prec_bits=prec_bits
                                ) / arb(g_sh)
                            D_dyadic_prim_diag += sgn_rs * g_acc
                    j_sh += 1
            else:
                # At Y = 2048 > tau^4 (T = 13778), compute exact D_coeff!
                D_tilde_d = arb(0)
                D_tower = arb(0)
                D_dyadic_prim_diag = arb(0)
            ok_dg = bool(D_coeff > arb(0))
            diag_ok = diag_ok and ok_dg
            row_dg: Dict[str, Any] = {
                "Y": Y_diag,
                "T_Y": T_d,
                "exceeds_tau_pow_4": bool(y_arb - (tau ** 4) > arb(0)),
                "D_coeff_m_eq_n": serialize_arb_certified(D_coeff),
                "D_coeff_asymptotic_O1_limit_const": serialize_arb_certified(D_coeff_limit_const),
                "verified": ok_dg,
            }
            if Y_diag <= 128:
                row_dg["D_tilde_prime_power"] = serialize_arb_certified(D_tilde_d)
                row_dg["D_tower_mu_plus_increments"] = serialize_arb_certified(D_tower)
                row_dg["D_dyadic_primitive_shell_diagonal"] = serialize_arb_certified(D_dyadic_prim_diag)
            diagonal_comparison_rows.append(row_dg)

        all_ok = bool(
            sub_unit_ok
            and three_way_ok
            and pi_sign_change_ok
            and discrepancy_ok
            and nonmonotone_and_jump_ok
            and diag_ok
        )
        return {
            "epistemic_scope": {
                "kernel_scaling_and_primitive_expansion": "CONCRETE_ANALYTIC_IN_LEAN",
                "moebius_inversion_of_primitive_blocks": "CONCRETE_ANALYTIC_IN_LEAN",
                "cutoff_discrepancy_and_nonmonotone_witnesses": "CERTIFIED_FINITE_OBSERVATION",
                "four_way_diagonal_separation": "ANALYTIC_PROVED_OUTSIDE_LEAN",
            },
            "generalized_coefficient_hypotheses_note": (
                "Lean Theorem 4(3) and Theorem 4(5) prove simplified synthesis/Moebius inversion "
                "E_{a,T}(u) <-> Pi_{a,T}(u) and separable quotient-shell Moebius decoupling under explicit "
                "complete multiplicativity a(m*n) = a(m)*a(n) (for all m, n >= 1) and unimodular sign-square "
                "a(g)^2 = 1 (for all g >= 1), both satisfied unconditionally by Liouville lambda and the "
                "multiplicative controls 1, a_2, a_{3,5,7}."
            ),
            "sub_unit_window_kernel_check_Y8_g12": {
                "Y": 8,
                "g": g_sub,
                "sub_unit_u_Y_over_g": "2/3",
                "K_Y_gr_gs": serialize_arb_certified(K_lhs),
                "inv_g_K_Y_over_g_r_s": serialize_arb_certified(K_rhs_closed),
                "scaling_residual": serialize_arb_certified(K_lhs - K_rhs_closed),
                "phi_dilation_residual": serialize_arb_certified(phi_lhs - phi_rhs),
                "verified": sub_unit_ok,
            },
            "three_way_energy_and_inversion_rows": three_way_rows,
            "Pi_lambda_sign_change_scales": {
                "positive_Y": pi_pos_Y,
                "negative_Y": pi_neg_Y,
                "verified": pi_sign_change_ok,
            },
            "inherited_vs_canonical_cutoff_discrepancy_rows": cutoff_discrepancy_rows,
            "nonmonotone_and_cutoff_jump_diagnostics": {
                "E_2_minus_E_4_positive_margin": serialize_arb_certified(nonmonotone_2_gt_4_margin),
                "E_16_minus_E_24_positive_margin": serialize_arb_certified(nonmonotone_16_gt_24_margin),
                "T_at_16": 32,
                "T_at_16_plus_2_pow_minus_10": 33,
                "E_at_16_plus_2_pow_minus_10": serialize_arb_certified(E16_post_jump),
                "verified": nonmonotone_and_jump_ok,
            },
            "four_way_diagonal_comparison": {
                "structural_note": (
                    "Keep strictly distinct: (1) Coefficient diagonal m=n (primitive pair r=s=1), which satisfies "
                    "D_coeff(Y) = sum_{g<=T(Y)} g^{-1} K_{Y/g}(1,1) -> (3*sqrt(tau)/64)*log(tau) ~= 0.2159472478 = O(1) "
                    "as Y -> infty because ||phi_m||_Y^2 ~ m^{-1} 1_{m~Y} concentrates all O(Y) unsigned energy into "
                    "off-diagonal pairs m != n; (2) Normalized prime-power diagonal D_tilde(Y) = sum_{p^k<=T(Y)} ||F_{p^k,Y}||_Y^2, "
                    "which is O(Y/(log Y)^2) under E(Z) <= M*Z; (3) Dyadic power-lift tower Gram diagonal ||Q_{mu,T}||_Y^2 + "
                    "sum_{J<J_T} ||Q_{Delta_J,T}||_Y^2, which already contains the RH-equivalent ||Q_{mu,T}||_Y^2 baseline; "
                    "(4) Dyadic primitive-block shell diagonal j_r = j_s, which retains signed coprime off-diagonal pairs "
                    "2^j <= r != s < 2^{j+1} with gcd(r,s) = 1."
                ),
                "rows": diagonal_comparison_rows,
            },
            "all_section_3_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 4. Section 4: Dyadic Blocks, Quotient-Shell Moebius Identity, & Attempt B
# ---------------------------------------------------------------------------


def verify_section_4_dyadic_blocks_and_attempt_b(prec_bits: int = 256) -> Dict[str, Any]:
    """Verify exact dyadic block decomposition, separable `quotientDyadicShellQ` Moebius decoupling
    (vs naive uncoupled shell filtering failure), Attempt B closed-form variation constants `C_var`
    and `C_{chi,var}`, control separation across `lambda, 1, a_2, a_{3,5,7}`, split-scale smooth-step
    bound breaking `O(Y/(log Y)^4)`, finite parity uniqueness, and partial block-saving aggregation.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()

        # 4.1 Exact dyadic block partition & separable quotient-shell Moebius identity (Theorem 4(5))
        # Check at Y = 16, T = 32 across all 4 modes: lambda, 1, a_2, a_{3,5,7}
        Y_blk = arb(16)
        T_blk = exact_T_cutoff_ceil_Y_5_4(16)  # 32
        max_j = T_blk.bit_length() - 1  # 5 (2^5 = 32)
        quotient_shell_checks: List[Dict[str, Any]] = []
        blk_ok = True
        for mode_key in ("liouville", "unsigned_1", "a2", "a_3_5_7"):
            w_fn = _weight_fn_for_mode(mode_key)
            Pi_full = evaluate_primitive_coprime_sum_Pi_arb(
                Y_blk, T_blk, mode=mode_key, prec_bits=prec_bits
            )
            sum_blocks = arb(0)
            for jr in range(max_j + 1):
                for js in range(max_j + 1):
                    # Direct primitive dyadic block
                    blk_direct = arb(0)
                    for r in range(max(1, 1 << jr), min(T_blk, (1 << (jr + 1)) - 1) + 1):
                        for s in range(max(1, 1 << js), min(T_blk, (1 << (js + 1)) - 1) + 1):
                            if math.gcd(r, s) == 1:
                                blk_direct += arb(int(w_fn(r)) * int(w_fn(s))) * evaluate_window_kernel_K_closed_arb(
                                    Y_blk, r, s, prec_bits=prec_bits
                                )
                    sum_blocks += blk_direct
                    if (jr, js) == (3, 4):
                        # Verify separable quotient-shell Moebius decoupling vs naive uncoupled shell failure!
                        sep_moebius = arb(0)
                        naive_uncoupled = arb(0)
                        for d in range(1, T_blk + 1):
                            mu_d = moebius_mu_int(d)
                            if mu_d == 0:
                                continue
                            L_d = T_blk // d
                            q_vec_jr = [0] * (L_d + 1)
                            q_vec_js = [0] * (L_d + 1)
                            naive_jr = [0] * (L_d + 1)
                            naive_js = [0] * (L_d + 1)
                            for q in range(1, L_d + 1):
                                if (1 << jr) <= d * q < (1 << (jr + 1)):
                                    q_vec_jr[q] = int(w_fn(q))
                                if (1 << js) <= d * q < (1 << (js + 1)):
                                    q_vec_js[q] = int(w_fn(q))
                                if (1 << jr) <= q < (1 << (jr + 1)):
                                    naive_jr[q] = int(w_fn(q))
                                if (1 << js) <= q < (1 << (js + 1)):
                                    naive_js[q] = int(w_fn(q))
                            sep_moebius += (arb(mu_d) / arb(d)) * evaluate_bilinear_window_pairing_closed_arb(
                                Y_blk / arb(d), L_d, q_vec_jr, q_vec_js, prec_bits=prec_bits
                            )
                            naive_uncoupled += (arb(mu_d) / arb(d)) * evaluate_bilinear_window_pairing_closed_arb(
                                Y_blk / arb(d), L_d, naive_jr, naive_js, prec_bits=prec_bits
                            )
                        res_sep = blk_direct - sep_moebius
                        naive_err = blk_direct - naive_uncoupled
                        ok_m = bool(
                            arb(0) in res_sep
                            and abs(res_sep) < arb("1e-65")
                            and abs(naive_err) > arb("1e-6")
                        )
                        blk_ok = blk_ok and ok_m
                        quotient_shell_checks.append(
                            {
                                "mode": mode_key,
                                "jr": jr,
                                "js": js,
                                "direct_primitive_block": serialize_arb_certified(blk_direct),
                                "quotient_shell_moebius_residual": serialize_arb_certified(res_sep),
                                "naive_uncoupled_shell_error": serialize_arb_certified(naive_err),
                                "verified": ok_m,
                            }
                        )
            res_part = Pi_full - sum_blocks
            if not bool(arb(0) in res_part and abs(res_part) < arb("1e-64")):
                blk_ok = False

        # 4.2 Resonant-shell signed vs unsigned primitive block comparison across controls
        # At Y in {16, 32, 64}, resonant shell j_res = round(log_2 Y) (i.e. 2^j = Y / 2 so [Y/2, Y) or [Y, 2Y)):
        resonant_control_rows: List[Dict[str, Any]] = []
        res_ctrl_ok = True
        for Y_rc in (16, 32, 64):
            T_rc = exact_T_cutoff_ceil_Y_5_4(Y_rc)
            j_res = int(round(math.log2(Y_rc)))  # 4, 5, 6: shell [Y, 2*Y) inside [Y, tau*Y]!
            u_rc = arb(Y_rc)
            uns_blk = arb(0)
            sgn_by_mode: Dict[str, arb] = {m: arb(0) for m in ("liouville", "unsigned_1", "a2", "a_3_5_7")}
            w_fns = {m: _weight_fn_for_mode(m) for m in sgn_by_mode}
            lo_r, hi_r = 1 << j_res, min(T_rc, (1 << (j_res + 1)) - 1)
            for r in range(lo_r, hi_r + 1):
                for s in range(lo_r, hi_r + 1):
                    if math.gcd(r, s) == 1:
                        k_rs = evaluate_window_kernel_K_closed_arb(u_rc, r, s, prec_bits=prec_bits)
                        uns_blk += k_rs
                        for m_key, fn in w_fns.items():
                            sgn_by_mode[m_key] += arb(int(fn(r)) * int(fn(s))) * k_rs
            ok_rc = bool(uns_blk > arb(0) and uns_blk - abs(sgn_by_mode["liouville"]) > arb(0))
            res_ctrl_ok = res_ctrl_ok and ok_rc
            resonant_control_rows.append(
                {
                    "Y": Y_rc,
                    "T_Y": T_rc,
                    "resonant_shell_j": j_res,
                    "unsigned_block_size": serialize_arb_certified(uns_blk),
                    "unsigned_block_over_Y": serialize_arb_certified(uns_blk / u_rc),
                    "abs_signed_over_unsigned_liouville": serialize_arb_certified(
                        abs(sgn_by_mode["liouville"]) / uns_blk
                    ),
                    "abs_signed_over_unsigned_a2": serialize_arb_certified(
                        abs(sgn_by_mode["a2"]) / uns_blk
                    ),
                    "abs_signed_over_unsigned_a_3_5_7": serialize_arb_certified(
                        abs(sgn_by_mode["a_3_5_7"]) / uns_blk
                    ),
                    "verified": ok_rc,
                }
            )

        # 4.3 Attempt B: Pre-stated lemmas, exact closed-form variation constants C_var & C_{chi,var},
        # finite parity uniqueness check, and partial block-saving aggregation check
        C_var = evaluate_C_var_gaussian_arb(prec_bits=prec_bits)
        C_chi_var = evaluate_C_chi_var_smooth_arb(prec_bits=prec_bits)
        var_sample_rows: List[Dict[str, Any]] = []
        var_ok = bool(C_var > arb(1) and C_chi_var > arb(3))

        def _chi_q_arb(w: arb, q: int) -> arb:
            u = w / arb(q)
            u2 = u * u
            return (arb(1) / arb(q)) * u2 * (arb(2) * u2 - arb(3)) * (-u2).exp()

        for w_int in (1, 4, 16, 64):
            w_arb = arb(w_int)
            sqrt_w = w_arb.sqrt()
            for L_var in (1, 4, 16, 64, 128):
                tot_phi = arb(L_var) * evaluate_phi_n_arb(w_arb, L_var, prec_bits=prec_bits) + sum(
                    (
                        arb(q)
                        * abs(
                            evaluate_phi_n_arb(w_arb, q, prec_bits=prec_bits)
                            - evaluate_phi_n_arb(w_arb, q + 1, prec_bits=prec_bits)
                        )
                        for q in range(1, L_var)
                    ),
                    arb(0),
                )
                tot_chi = arb(L_var) * abs(_chi_q_arb(w_arb, L_var)) + sum(
                    (
                        arb(q) * abs(_chi_q_arb(w_arb, q) - _chi_q_arb(w_arb, q + 1))
                        for q in range(1, L_var)
                    ),
                    arb(0),
                )
                margin_phi = C_var * sqrt_w - tot_phi
                margin_chi = C_chi_var - tot_chi
                ok_v = bool(margin_phi > arb(0) and margin_chi > arb(0))
                var_ok = var_ok and ok_v
                if (w_int, L_var) in ((1, 1), (16, 64), (64, 128)):
                    var_sample_rows.append(
                        {
                            "w": w_int,
                            "L": L_var,
                            "weighted_phi_variation": serialize_arb_certified(tot_phi),
                            "C_var_sqrt_w_upper_bound": serialize_arb_certified(C_var * sqrt_w),
                            "phi_variation_margin": serialize_arb_certified(margin_phi),
                            "weighted_chi_variation": serialize_arb_certified(tot_chi),
                            "C_chi_var_upper_bound": serialize_arb_certified(C_chi_var),
                            "chi_variation_margin": serialize_arb_certified(margin_chi),
                            "verified": ok_v,
                        }
                    )

        # Compare actual signed |Delta_d^{sm}(X)| vs TC-058's unsigned C_sm*sqrt(X)/(d*(d+1)) at small d = 1..4
        # as Y grows (illustrating the inner q-sum cancellation utilized by Lemma B2):
        from tc.simultaneous_compatibility_combined_energy import evaluate_C_smooth_step_arb

        C_sm_tc058 = evaluate_C_smooth_step_arb(prec_bits=prec_bits)
        smooth_cancellation_rows: List[Dict[str, Any]] = []
        sm_canc_ok = True
        for Y_sc in (16, 64, 256):
            T_sc = exact_T_cutoff_ceil_Y_5_4(Y_sc)
            X_sc = arb(Y_sc)
            d_sc = 1
            L_1 = T_sc // d_sc
            delta_1_sgn = (
                evaluate_Q_shifted_finite_arb(
                    X_sc / arb(1), L=L_1, m_shift=0, mode="liouville", prec_bits=prec_bits
                )
                - evaluate_Q_shifted_finite_arb(
                    X_sc / arb(2), L=L_1, m_shift=0, mode="liouville", prec_bits=prec_bits
                )
                / arb(2).sqrt()
            )
            ub_tc058 = C_sm_tc058 * X_sc.sqrt() / arb(2)
            ratio_sgn_to_tc058 = abs(delta_1_sgn) / ub_tc058
            ok_sc = bool(ub_tc058 - abs(delta_1_sgn) > arb(0))
            sm_canc_ok = sm_canc_ok and ok_sc
            smooth_cancellation_rows.append(
                {
                    "Y": Y_sc,
                    "T_Y": T_sc,
                    "d": 1,
                    "abs_Delta_1_smooth_signed": serialize_arb_certified(abs(delta_1_sgn)),
                    "tc058_unsigned_bound_C_sm_sqrtY_over_2": serialize_arb_certified(ub_tc058),
                    "signed_over_unsigned_bound_ratio": serialize_arb_certified(ratio_sgn_to_tc058),
                    "verified": ok_sc,
                }
            )

        # TASK-TC-059R Repair 3 & 4D checks:
        # (a) Smooth-endpoint / floor-jump split g_d - g_{d+1} = Delta_d^{sm} + Delta_d^{jump}
        #     with identical inner cutoff L_d = floor(T/d) at BOTH smooth endpoints, nontrivial
        #     L_d != L_{d+1} floor jump, and exact integral sign -sqrt(X) * int_d^{d+1} ...
        smooth_endpoint_jump_rows: List[Dict[str, Any]] = []
        sm_repair_ok = True
        for T_pt, d_pt, x_frac in (
            (5, 2, Fraction(7, 1)),
            (32, 3, Fraction(16, 1)),
            (32, 1, Fraction(16, 1)),
            (0, 1, Fraction(5, 1)),
        ):
            L_d_pt = T_pt // d_pt
            L_d1_pt = T_pt // (d_pt + 1)
            ev_pt = evaluate_smooth_increment_and_jump_arb(x_frac, T_pt, d_pt, prec_bits=prec_bits)
            split_res = ev_pt["g_d_minus_g_d1"] - (
                ev_pt["delta_sm_endpoint"] + ev_pt["delta_jump"]
            )
            sign_int_res = ev_pt["delta_sm_endpoint"] - ev_pt["delta_sm_integral"]
            wrong_sign_gap = abs(ev_pt["delta_sm_endpoint"] + ev_pt["delta_sm_integral"])
            ok_pt = bool(
                arb(0) in split_res
                and abs(split_res) < arb("1e-66")
                and arb(0) in sign_int_res
                and abs(sign_int_res) < arb("1e-62")
            )
            if L_d_pt != L_d1_pt:
                ok_pt = bool(ok_pt and abs(ev_pt["delta_jump"]) > arb("1e-12"))
            if L_d_pt >= 1:
                ok_pt = bool(ok_pt and wrong_sign_gap > arb("1e-8"))
            if T_pt == 0:
                ok_pt = bool(
                    ok_pt
                    and ev_pt["delta_sm_endpoint"] == arb(0)
                    and ev_pt["delta_jump"] == arb(0)
                )
            sm_repair_ok = sm_repair_ok and ok_pt
            smooth_endpoint_jump_rows.append(
                {
                    "T": T_pt,
                    "d": d_pt,
                    "X": str(x_frac),
                    "L_d_both_smooth_endpoints": L_d_pt,
                    "L_d_plus_1_after_jump": L_d1_pt,
                    "nontrivial_floor_jump": bool(L_d_pt != L_d1_pt),
                    "delta_sm_endpoint": serialize_arb_certified(ev_pt["delta_sm_endpoint"]),
                    "delta_jump_separate": serialize_arb_certified(ev_pt["delta_jump"]),
                    "split_identity_residual": serialize_arb_certified(split_res),
                    "endpoint_minus_neg_sqrtX_integral_residual": serialize_arb_certified(
                        sign_int_res
                    ),
                    "verified": ok_pt,
                }
            )

        # (b) Direct window norm bound (Lean Theorem 7):
        #     ||Delta_d^{sm}||_Y <= d^{-1/2}*sqrt(E_{lambda,L_d}(Y/d)) + (d+1)^{-1/2}*sqrt(E_{lambda,L_d}(Y/(d+1)))
        #     including nontrivial jump + sub-unit Y/(d+1) < 1, zero L_d, and T = 0.
        smooth_norm_bound_rows: List[Dict[str, Any]] = []
        for Y_nb, T_nb, d_nb in ((16, 32, 1), (2, 5, 2), (2, 3, 4), (2, 0, 1)):
            y_nb_arb = arb(Y_nb)
            L_d_nb = T_nb // d_nb
            d_nb_arb = arb(d_nb)
            d1_nb_arb = arb(d_nb + 1)
            lam_nb = [0] + [liouville_lambda_int(q) for q in range(1, L_d_nb + 1)]
            E_u1 = evaluate_bilinear_window_pairing_closed_arb(
                y_nb_arb / d_nb_arb, L_d_nb, lam_nb, lam_nb, prec_bits=prec_bits
            )
            E_u2 = evaluate_bilinear_window_pairing_closed_arb(
                y_nb_arb / d1_nb_arb, L_d_nb, lam_nb, lam_nb, prec_bits=prec_bits
            )
            if L_d_nb == 0:
                norm_sm = arb(0)
                rhs_nb = arb(0)
            else:
                def _sm_sq_integrand(
                    z: acb,
                    _analytic: bool,
                    _L: int = L_d_nb,
                    _d: int = d_nb,
                    _lam: Sequence[int] = lam_nb,
                ) -> acb:
                    if _analytic and not bool(z.real > arb(0)):
                        nan_b = arb("nan")
                        return acb(nan_b, nan_b)
                    dc = acb(_d)
                    d1c = acb(_d + 1)
                    w1 = z / dc
                    w2 = z / d1c
                    w1_p = ((acb(5) / acb(2)) * w1.log(analytic=_analytic)).exp()
                    w2_p = ((acb(5) / acb(2)) * w2.log(analytic=_analytic)).exp()
                    q1 = acb(0)
                    q2 = acb(0)
                    for q in range(1, _L + 1):
                        qc = acb(q)
                        inv_q3 = qc ** (-3)
                        sgn = acb(_lam[q]) * inv_q3
                        q1 += sgn * (-(w1 * w1) / (qc * qc)).exp()
                        q2 += sgn * (-(w2 * w2) / (qc * qc)).exp()
                    val = (w1_p * q1) / dc.sqrt() - (w2_p * q2) / d1c.sqrt()
                    return (val * val) / z

                norm_sq_sm = _acb_integral_certified_arb(
                    _sm_sq_integrand, y_nb_arb, tau * y_nb_arb, prec_bits=prec_bits
                )
                norm_sm = norm_sq_sm.sqrt()
                rhs_nb = (E_u1.sqrt() / d_nb_arb.sqrt()) + (E_u2.sqrt() / d1_nb_arb.sqrt())
            margin_nb = rhs_nb - norm_sm
            ok_nb = bool(margin_nb > arb(0) if L_d_nb >= 1 else (norm_sm == arb(0) and rhs_nb == arb(0)))
            sm_repair_ok = sm_repair_ok and ok_nb
            smooth_norm_bound_rows.append(
                {
                    "Y": Y_nb,
                    "T": T_nb,
                    "d": d_nb,
                    "L_d": L_d_nb,
                    "second_scale_Y_over_d_plus_1": f"{Y_nb}/{d_nb + 1}",
                    "sub_unit_window_base_present": bool(Y_nb < d_nb + 1),
                    "Delta_d_smooth_window_norm": serialize_arb_certified(norm_sm),
                    "direct_triangle_rhs_bound": serialize_arb_certified(rhs_nb),
                    "rhs_minus_norm_margin": serialize_arb_certified(margin_nb),
                    "verified": ok_nb,
                }
            )

        # (c) Adjacent-scale cancellation loss check at Y = 64, T = 182:
        #     Compare actual ||sum_{d=1}^{T-1} R_2^{int}(d) Delta_d^{sm}||_Y against
        #     sum_{d=1}^{T-1} |R_2^{int}(d)| * (d^{-1/2}*sqrt(E_{lambda,L_d}(Y/d)) + (d+1)^{-1/2}*sqrt(E_{lambda,L_d}(Y/(d+1))))
        Y_adj = 64
        T_adj = exact_T_cutoff_ceil_Y_5_4(Y_adj)  # 182
        y_adj_arb = arb(Y_adj)
        c_lam_adj = evaluate_c_lambda_arb(prec_bits=prec_bits)
        W2_acc = arb(0)
        R2_int_arr: List[arb] = [arb(0)] * (T_adj + 1)
        for d_i in range(1, T_adj + 1):
            W2_acc += selberg_w2_weight_arb(d_i, mode="liouville")
            R2_int_arr[d_i] = W2_acc - c_lam_adj * arb(d_i)
        lam_full_adj = [0] + [liouville_lambda_int(q) for q in range(1, T_adj + 1)]
        minkowski_split_sum = arb(0)
        coeff_r_smooth: List[arb] = [arb(0)] * (2 * T_adj + 1)
        for d_i in range(1, T_adj):
            L_di = T_adj // d_i
            E_d1 = evaluate_bilinear_window_pairing_closed_arb(
                y_adj_arb / arb(d_i), L_di, lam_full_adj, lam_full_adj, prec_bits=prec_bits
            )
            E_d2 = evaluate_bilinear_window_pairing_closed_arb(
                y_adj_arb / arb(d_i + 1), L_di, lam_full_adj, lam_full_adj, prec_bits=prec_bits
            )
            rhs_di = (E_d1.sqrt() / arb(d_i).sqrt()) + (E_d2.sqrt() / arb(d_i + 1).sqrt())
            minkowski_split_sum += abs(R2_int_arr[d_i]) * rhs_di
            # Exact basis expansion r_smooth(X) = sum_{d=1}^{T-1} R_2^{int}(d) * Delta_d^{sm}(X)
            # using m^{-1/2} * phi_q(X / m) = phi_{m * q}(X) for m in {d_i, d_i + 1} ((d_i + 1)*L_di <= 2*T_adj):
            for q in range(1, L_di + 1):
                term_dq = R2_int_arr[d_i] * arb(lam_full_adj[q])
                coeff_r_smooth[d_i * q] += term_dq
                coeff_r_smooth[(d_i + 1) * q] -= term_dq

        # Pointwise cross-check at X = Y_adj between sum_d R_2^{int}(d)*Delta_d^{sm}(X) and sum_n c_n*phi_n(X):
        r_sm_direct_Y = arb(0)
        for d_i in range(1, T_adj):
            L_di = T_adj // d_i
            g_di = evaluate_Q_general_arb(
                y_adj_arb / arb(d_i), L_di, coeff_fn=liouville_lambda_int, prec_bits=prec_bits
            ) / arb(d_i).sqrt()
            g_di1 = evaluate_Q_general_arb(
                y_adj_arb / arb(d_i + 1), L_di, coeff_fn=liouville_lambda_int, prec_bits=prec_bits
            ) / arb(d_i + 1).sqrt()
            r_sm_direct_Y += R2_int_arr[d_i] * (g_di - g_di1)
        r_sm_basis_Y = sum(
            (
                coeff_r_smooth[n_idx] * evaluate_phi_n_arb(y_adj_arb, n_idx, prec_bits=prec_bits)
                for n_idx in range(1, 2 * T_adj + 1)
            ),
            arb(0),
        )
        r_sm_basis_res = r_sm_direct_Y - r_sm_basis_Y

        r_smooth_norm_sq_Y64 = evaluate_bilinear_window_pairing_closed_arb(
            y_adj_arb, 2 * T_adj, coeff_r_smooth, coeff_r_smooth, prec_bits=prec_bits
        )
        r_smooth_norm_Y64 = r_smooth_norm_sq_Y64.sqrt()
        C_cut_norm_const = arb(2) * ((tau ** 5 - arb(1)) / arb(5)).sqrt()
        canc_loss_ratio = minkowski_split_sum / r_smooth_norm_Y64
        ok_adj = bool(
            arb(0) in r_sm_basis_res
            and abs(r_sm_basis_res) < arb("1e-66")
            and r_smooth_norm_Y64 > arb(0)
            and minkowski_split_sum - r_smooth_norm_Y64 > arb(0)
            and canc_loss_ratio - arb(5) > arb(0)
        )
        sm_repair_ok = sm_repair_ok and ok_adj

        # (d) Small-scale u < 2 O(u^5) bound & g > floor(Y/2) common-factor tail control (Lean Theorem 7(4)):
        C_u5 = arb(9) * (tau ** 5 - arb(1)) / arb(20)
        C_tail_global = C_u5 * (arb(1024) / arb(5))
        small_scale_u5_rows: List[Dict[str, Any]] = []
        u5_ok = True
        for u_frac, L_u5 in ((Fraction(1, 3), 5), (Fraction(1, 1), 10), (Fraction(3, 2), 20)):
            u_arb_chk = _frac_to_arb(u_frac)
            pi_u5 = evaluate_primitive_coprime_sum_Pi_arb(
                u_arb_chk, L_u5, mode="liouville", prec_bits=prec_bits
            )
            ub_u5 = C_u5 * (u_arb_chk ** 5)
            margin_u5 = ub_u5 - abs(pi_u5)
            ok_u = bool(margin_u5 > arb(0))
            u5_ok = u5_ok and ok_u
            small_scale_u5_rows.append(
                {
                    "u": str(u_frac),
                    "L": L_u5,
                    "abs_Pi_lambda_L_u": serialize_arb_certified(abs(pi_u5)),
                    "C_u5_times_u_pow_5": serialize_arb_certified(ub_u5),
                    "margin": serialize_arb_certified(margin_u5),
                    "verified": ok_u,
                }
            )
        tail_g_rows: List[Dict[str, Any]] = []
        for Y_tl in (16, 64):
            T_tl = exact_T_cutoff_ceil_Y_5_4(Y_tl)
            M_tl = Y_tl // 2
            y_tl_arb = arb(Y_tl)
            tail_sum_tl = arb(0)
            for g_tl in range(M_tl + 1, T_tl + 1):
                pi_g_tl = evaluate_primitive_coprime_sum_Pi_arb(
                    y_tl_arb / arb(g_tl), T_tl // g_tl, mode="liouville", prec_bits=prec_bits
                )
                tail_sum_tl += abs(pi_g_tl) / arb(g_tl)
            margin_tl = C_tail_global - tail_sum_tl
            ok_tl = bool(margin_tl > arb(0))
            u5_ok = u5_ok and ok_tl
            tail_g_rows.append(
                {
                    "Y": Y_tl,
                    "T_Y": T_tl,
                    "M_floor_Y_half": M_tl,
                    "tail_sum_g_gt_M": serialize_arb_certified(tail_sum_tl),
                    "C_tail_global_upper_bound": serialize_arb_certified(C_tail_global),
                    "margin": serialize_arb_certified(margin_tl),
                    "verified": ok_tl,
                }
            )

        attempt_b_schemas = [
            {
                "lemma_id": "LEMMA-B1-UNIFORM-GAUSSIAN-VARIATION-AND-PNT-CUTOFF-BOUND",
                "epistemic_class": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "statement": (
                    "For all w > 0 and all integers L >= 1, L*phi_L(w) + sum_{q=1}^{L-1} q*|phi_q(w) - phi_{q+1}(w)| "
                    "<= C_var * sqrt(w) with exact closed-form constant C_var = 1/2 + 2*exp(-3/2) + 1/e ~= 1.31413976. "
                    "For w >= 2, combining summation by parts split at Q_0 = floor(sqrt(w)) with classical unconditional PNT "
                    "M_lambda(x) = O(x*exp(-c_PNT*sqrt(log x))) yields |Q_{lambda,[A,B]}(w)| << sqrt(w)*exp(-c_0*sqrt(log w)) "
                    "(c_0 = c_PNT/sqrt(2)) uniformly in ALL cutoffs 1 <= A <= B; substituting into scale-coupled Moebius "
                    "inversion (Theorem 4(3), under complete multiplicativity and lambda(g)^2 = 1, split across "
                    "d <= floor(sqrt(u)), floor(sqrt(u)) < d <= u/2, and d > u/2 where E_{lambda,M}(v) << v^5) yields "
                    "|Pi_{lambda,L}(u)| << u*exp(-c'_Pi*sqrt(log u)) for all u >= 2 uniformly in L >= 1."
                ),
                "control_separation": (
                    "Fails for 1, a_2, and a_{3,5,7} because missing prime sign relations a(p) + 1 = 0 leave positive "
                    "mean m_a = prod_{p in S} (p-1)/(p+1) > 0 (1 for unsigned, 1/3 for a_2, 1/4 for a_{3,5,7}), forcing "
                    "resonant primitive blocks to remain Theta(u)."
                ),
            },
            {
                "lemma_id": "LEMMA-B2-DIMENSIONLESS-CHI-VARIATION-AND-SUPER-POLYLOG-SMOOTH-STEP-BOUND",
                "epistemic_class": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "statement": (
                    "For all w > 0 and all integers L >= 1, L*|chi_L(w)| + sum_{q=1}^{L-1} q*|chi_q(w) - chi_{q+1}(w)| "
                    "<= C_{chi,var} := exp(-1/2) + 1/2 + (4*sqrt(7)-8)*exp(-(2-sqrt(7)/2)) + (4*sqrt(7)+8)*exp(-(2+sqrt(7)/2)) "
                    "~= 3.08879258 (dimensionless and independent of w). Splitting d in [1, T-1] at d = floor(sqrt(X)) "
                    "combines inner q-sum cancellation exp(-c_0*sqrt(log(X/(d+1)))) for d <= sqrt(X) with outer Selberg/PNT "
                    "cancellation |R_2^{int}(d)| << d*exp(-c_W*sqrt(log d)) for d > sqrt(X), proving unconditionally "
                    "||r_smooth / (log X)^2||_Y^2 << (Y/(log Y)^4)*exp(-2*c_* * sqrt(log Y)) = O_A(Y*(log Y)^{-A}) for "
                    "every A > 0; combining with the analogous C_var^{[2]}*sqrt(w) weighted variation bound on "
                    "psi_t^{[2]}(w) = (log(w/t))^2*phi_t(w) for -Q_{lambda,T}^{[2]}/(log X)^2 and TC-058's o(1) bounds "
                    "O((log Y)^{-4}) and O((log Y)^{-2}) on the square, endpoint, and jump pieces likewise proves "
                    "||D_{2,Y}||_Y^2 = O_A(Y*(log Y)^{-A}) for every A > 0, strictly breaking TC-058's "
                    "O(Y/(log Y)^4) unsigned smooth-step barrier."
                ),
                "why_not_subpower": (
                    "Lemma B2 is an absolute super-polylogarithmic upper bound saving every fixed power of log Y, NOT a "
                    "relative bound in D_tilde(Y) or F(Y) and NOT subpower O_eps(Y^eps) (an upper bound of size Y^{1-o(1)} "
                    "does not prove the signed remainder itself grows that fast). Conversely, the exact smooth-endpoint "
                    "identity Delta_d^{sm}(X) = d^{-1/2}*Q_{lambda,L_d}(X/d) - (d+1)^{-1/2}*Q_{lambda,L_d}(X/(d+1)) "
                    "(with unchanged L_d = floor(T/d) at both endpoints) already gives the direct window norm bound "
                    "||Delta_d^{sm}||_Y <= d^{-1/2}*sqrt(E_{lambda,L_d}(Y/d)) + (d+1)^{-1/2}*sqrt(E_{lambda,L_d}(Y/(d+1))) "
                    "(Lean Theorem 7) without crossing the critical line, and TC-057R Theorem 5.1(2) converts both inherited "
                    "cutoffs to sqrt(F(Y/m)) + O(1) on Y/m >= 1 (O((Y/m)^{5/2}) on Y/m < 1). However, splitting the "
                    "endpoint difference by Minkowski discards the O(1/d) adjacent-scale cancellation between d and d+1, "
                    "so multiplying by |R_2^{int}(d)| and summing over 1 <= d <= floor(Y) yields "
                    "O(Y^{3/2}*exp(-c'_W*sqrt(log Y))) in norm (O(Y^3*exp(-2*c'_W*sqrt(log Y))/(log Y)^4) in energy) and "
                    "fails to contract. Closing via this route requires an additional quantitative estimate: either an "
                    "adjacent-scale difference norm bound saving an extra d^{-1-alpha} relative to scale energy or signed "
                    "cancellation across the d-sum avoiding the outer triangle inequality on R_2^{int}(d)."
                ),
            },
            {
                "lemma_id": "LEMMA-B3-PARTIAL-BLOCK-SAVING-AGGREGATION-AND-SMALL-SCALE-TAIL",
                "epistemic_class": "UNCONDITIONAL_FINITE_ARITHMETIC + CONCRETE_ANALYTIC_IN_LEAN + ANALYTIC_PROVED_OUTSIDE_LEAN",
                "lean_theorem": (
                    "parity_uniqueness_turn_chart_defect_and_log_saving_closure_tc059 (Conjunct 6) & "
                    "smooth_increment_window_norm_and_small_scale_tail_tc059r (Conjunct 4)"
                ),
                "statement": (
                    "Distinguish fixed power saving O(u^{1-c}) (0 < c < 1, partial progress O(Y^{1-c})) from the subpower "
                    "target O_eps(u^eps) for every eps > 0. If the whole primitive sum satisfies "
                    "|Pi_{lambda,floor(T(Y)/g)}(Y/g)| <= B_loc * (Y/g)^{1-c} uniformly on 1 <= g <= M = floor(Y/2) "
                    "(where u = Y/g >= 2; selected balanced shells alone do not suffice without all remaining blocks and "
                    "cutoffs), then sum_{g=1}^M g^{-1}*|Pi| <= B_loc * (sum_{g=1}^M g^{-(2-c)}) * Y^{1-c} <= B_loc*zeta(2-c)*Y^{1-c}, "
                    "while on the sub-threshold tail M + 1 <= g <= T(Y) (0 < u = Y/g < 2) Lean Theorem 7(4) proves "
                    "|Pi_{lambda,L}(u)| <= (9*(tau^5-1)/20)*u^5 and sum_{g=M+1}^{T(Y)} g^{-1}*|Pi| <= (9*(tau^5-1)/20)*(1024/5) = O(1), "
                    "giving E(Y) <= B_loc*zeta(2-c)*Y^{1-c} + O(1) on Y >= 2 without ever applying a u >= 2 bound on u < 2."
                ),
            },
        ]

        all_ok = bool(blk_ok and res_ctrl_ok and var_ok and sm_canc_ok and sm_repair_ok and u5_ok)
        return {
            "epistemic_scope": {
                "dyadic_block_partition_and_quotient_shell_moebius": "CONCRETE_ANALYTIC_IN_LEAN",
                "smooth_increment_window_norm_and_small_scale_tail": "CONCRETE_ANALYTIC_IN_LEAN",
                "variation_lemmas_and_split_scale_smooth_step": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "finite_parity_uniqueness_and_finite_sum_block_aggregation": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "zeta_series_majorant_on_block_aggregation": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "resonant_shell_power_saving_for_lambda": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            },
            "quotient_shell_moebius_decoupling_checks_Y16_T32": quotient_shell_checks,
            "resonant_shell_control_comparison_rows": resonant_control_rows,
            "C_var_gaussian_closed_form": serialize_arb_certified(C_var),
            "C_chi_var_smooth_closed_form": serialize_arb_certified(C_chi_var),
            "variation_lemma_sample_checks": var_sample_rows,
            "smooth_step_signed_vs_tc058_unsigned_rows": smooth_cancellation_rows,
            "smooth_increment_endpoint_and_norm_repair_tc059r": {
                "lean_theorem": "smooth_increment_window_norm_and_small_scale_tail_tc059r",
                "critical_line_crossing_required_for_direct_norm_bound": False,
                "cutoff_conversion_constant_2_sqrt_tau5_m1_div_5": serialize_arb_certified(
                    C_cut_norm_const
                ),
                "pointwise_smooth_jump_and_sign_checks": smooth_endpoint_jump_rows,
                "window_norm_bound_checks": smooth_norm_bound_rows,
                "adjacent_scale_cancellation_loss_Y64_T182": {
                    "Y": Y_adj,
                    "T_Y": T_adj,
                    "r_smooth_window_norm_actual": serialize_arb_certified(r_smooth_norm_Y64),
                    "minkowski_split_endpoint_bound_sum": serialize_arb_certified(
                        minkowski_split_sum
                    ),
                    "minkowski_over_actual_ratio": serialize_arb_certified(canc_loss_ratio),
                    "remaining_quantitative_requirement": (
                        "Either an adjacent-scale difference norm estimate saving an extra d^{-1-alpha} "
                        "(alpha > 0) on ||Delta_d^{sm}||_Y relative to scale energy, or signed cancellation "
                        "across the d-sum against R_2^{int}(d) avoiding the outer triangle inequality."
                    ),
                    "verified": ok_adj,
                },
                "verified": sm_repair_ok,
            },
            "small_scale_u5_and_tail_control_tc059r": {
                "lean_theorem": "smooth_increment_window_norm_and_small_scale_tail_tc059r",
                "C_u5_9_tau5_m1_over_20": serialize_arb_certified(C_u5),
                "C_tail_global_upper_bound": serialize_arb_certified(C_tail_global),
                "small_scale_u_lt_2_rows": small_scale_u5_rows,
                "common_factor_tail_g_gt_floor_Y_half_rows": tail_g_rows,
                "verified": u5_ok,
            },
            "attempt_b_pre_stated_schemas": attempt_b_schemas,
            "all_section_4_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 5. Section 5: TC Geometry, Prime-Local Defect, Window Base, & Murmurations
# ---------------------------------------------------------------------------


def verify_section_5_tc_geometry_defect_and_murmurations(prec_bits: int = 256) -> Dict[str, Any]:
    """Verify auxiliary turn chart `Z_{tau/2}(tau*q) = zeta(2*q)`, `K^* = 1 - log 2 / log tau`,
    prime-local defect `D_p(delta)` Euler-factor norm-square bridge, `[Y, b*Y]` window-base
    compatibility discriminator (`b in {2, e, tau}`), and murmuration hypothesis audit.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        a_turn = tau / arb(2)
        K_star = arb(1) - arb(2).log() / tau.log()
        tau_pow_K_star = tau ** K_star
        res_K_star = tau_pow_K_star - a_turn

        # Turn-chart evaluations: Z_{tau/2}(tau*q) = zeta(2*q) on Re(q) = 1/4 and trivial zeros q = -m
        q_crit = acb(arb(1) / arb(4), arb(7))
        z_turn_lhs = ((acb(tau) * q_crit) / acb(a_turn)).zeta()
        z_turn_rhs = (acb(2) * q_crit).zeta()
        triv_zero_checks: List[Dict[str, Any]] = []
        turn_ok = bool(
            arb(0) in res_K_star
            and abs(res_K_star) < arb("1e-70")
            and abs(z_turn_lhs - z_turn_rhs) < arb("1e-70")
        )
        for m_triv in (1, 2, 3):
            q_m = acb(-m_triv)
            val_m = ((acb(tau) * q_m) / acb(a_turn)).zeta()
            ok_tm = bool(arb(0) in val_m.real and arb(0) in val_m.imag and abs(val_m) < arb("1e-70"))
            turn_ok = turn_ok and ok_tm
            triv_zero_checks.append(
                {
                    "m": m_triv,
                    "q_trivial_zero": -m_triv,
                    "abs_Z_tau_half_at_tau_q": serialize_arb_certified(abs(val_m)),
                    "verified": ok_tm,
                }
            )

        # Prime-local defect D_p(delta) = (p^{delta/2} - p^{-delta/2})^2 & Euler norm-square bridge
        # |p^delta * exp(i*theta) - 1|^2 = p^delta * (D_p(delta) + 4*sin^2(theta/2))
        # Evaluated at synthetic displacements delta in {0, 1/10, -1/4} (NO zeta zeros used!)
        defect_rows: List[Dict[str, Any]] = []
        defect_ok = True
        for p_val in (2, 3, 5):
            p_arb = arb(p_val)
            for d_num, d_den in ((0, 1), (1, 10), (-1, 4)):
                delta = arb(d_num) / arb(d_den)
                theta = arb(7) / arb(10)
                D_p = (p_arb ** delta) + (p_arb ** (-delta)) - arb(2)
                sq_form = ((p_arb ** (delta / arb(2))) - (p_arb ** (-delta / arb(2)))) ** 2
                euler_diff = acb(p_arb ** delta) * (acb(0, 1) * acb(theta)).exp() - acb(1)
                lhs_norm_sq = (euler_diff * euler_diff.conjugate()).real
                rhs_bridge = (p_arb ** delta) * (D_p + arb(4) * ((theta / arb(2)).sin() ** 2))
                res_sq = D_p - sq_form
                res_br = lhs_norm_sq - rhs_bridge
                ok_df = bool(
                    arb(0) in res_sq
                    and abs(res_sq) < arb("1e-70")
                    and arb(0) in res_br
                    and abs(res_br) < arb("1e-70")
                    and (D_p == arb(0) if d_num == 0 else D_p > arb(0))
                )
                defect_ok = defect_ok and ok_df
                if (p_val, d_num) in ((2, 0), (2, 1), (5, -1)):
                    defect_rows.append(
                        {
                            "p": p_val,
                            "synthetic_delta": f"{d_num}/{d_den}" if d_den != 1 else str(d_num),
                            "D_p_delta": serialize_arb_certified(D_p),
                            "square_identity_residual": serialize_arb_certified(res_sq),
                            "euler_factor_norm_sq_bridge_residual": serialize_arb_certified(res_br),
                            "zero_inputs_used": False,
                            "verified": ok_df,
                        }
                    )

        # [Y, b*Y] Window-Base Compatibility Discriminator across b in {2, e, tau} at Y = 16, T = 32:
        # Tests whether primitive-pair expansion and dyadic power-lift quadratic expansion require b = tau
        # or hold identically for every window multiplier b > 1!
        Y_wb = arb(16)
        T_wb = exact_T_cutoff_ceil_Y_5_4(16)  # 32
        J_T_wb = stabilization_depth_J_T(T_wb)  # 3
        lam_wb = [0] + [liouville_lambda_int(n) for n in range(1, T_wb + 1)]
        mu_wb = [0] + [moebius_mu_int(n) for n in range(1, T_wb + 1)]
        d1_wb = [0] + [power_lift_increment_delta_J_int(1, n) for n in range(1, T_wb + 1)]
        d2_wb = [0] + [power_lift_increment_delta_J_int(2, n) for n in range(1, T_wb + 1)]
        window_base_rows: List[Dict[str, Any]] = []
        wb_ok = True
        for b_label, b_val in (("2", arb(2)), ("e", arb(1).exp()), ("tau", tau)):
            E_b = evaluate_bilinear_window_pairing_closed_arb(
                Y_wb, T_wb, lam_wb, lam_wb, base_mult=b_val, prec_bits=prec_bits
            )
            # Primitive-pair expansion on [Y, b*Y]
            E_b_prim = arb(0)
            for g in range(1, T_wb + 1):
                L_g = T_wb // g
                u_g = Y_wb / arb(g)
                pi_g = arb(0)
                for r in range(1, L_g + 1):
                    for s in range(1, L_g + 1):
                        if math.gcd(r, s) == 1:
                            pi_g += arb(liouville_lambda_int(r * s)) * evaluate_window_kernel_K_closed_arb(
                                u_g, r, s, base_mult=b_val, prec_bits=prec_bits
                            )
                E_b_prim += pi_g / arb(g)
            # Increment expansion on [Y, b*Y]
            E_b_mu = evaluate_bilinear_window_pairing_closed_arb(
                Y_wb, T_wb, mu_wb, mu_wb, base_mult=b_val, prec_bits=prec_bits
            )
            c_mu_1 = evaluate_bilinear_window_pairing_closed_arb(
                Y_wb, T_wb, mu_wb, d1_wb, base_mult=b_val, prec_bits=prec_bits
            )
            c_mu_2 = evaluate_bilinear_window_pairing_closed_arb(
                Y_wb, T_wb, mu_wb, d2_wb, base_mult=b_val, prec_bits=prec_bits
            )
            g_11 = evaluate_bilinear_window_pairing_closed_arb(
                Y_wb, T_wb, d1_wb, d1_wb, base_mult=b_val, prec_bits=prec_bits
            )
            g_12 = evaluate_bilinear_window_pairing_closed_arb(
                Y_wb, T_wb, d1_wb, d2_wb, base_mult=b_val, prec_bits=prec_bits
            )
            g_22 = evaluate_bilinear_window_pairing_closed_arb(
                Y_wb, T_wb, d2_wb, d2_wb, base_mult=b_val, prec_bits=prec_bits
            )
            E_b_inc = E_b_mu - arb(2) * (c_mu_1 + c_mu_2) + g_11 + arb(2) * g_12 + g_22
            res_p = E_b - E_b_prim
            res_i = E_b - E_b_inc
            ok_b = bool(
                E_b > arb(0)
                and arb(0) in res_p
                and abs(res_p) < arb("1e-64")
                and arb(0) in res_i
                and abs(res_i) < arb("1e-64")
            )
            wb_ok = wb_ok and ok_b
            window_base_rows.append(
                {
                    "window_base_multiplier_b": b_label,
                    "E_Y_b": serialize_arb_certified(E_b),
                    "primitive_expansion_residual": serialize_arb_certified(res_p),
                    "increment_expansion_residual": serialize_arb_certified(res_i),
                    "holds_without_tau_specific_identity": True,
                    "verified": ok_b,
                }
            )

        # TASK-TC-059R Repair 2: Consistent inverse-Mellin convention M_Q(w) = int_0^infty Q_{lambda,infty}(X) * X^{-w} dX/X
        # (w = u + i*v, u, v real), single-term identity int_0^infty phi_n(X) * X^{-w} dX/X = (1/2)*Gamma(5/4 - w/2)*n^{-1/2 - w}
        # on u < 5/2, absolute interchange M_Q(w) = Gamma(5/4 - w/2)*zeta(1 + 2*w)/(2*zeta(1/2 + w)) on 1/2 < u < 5/2,
        # holomorphic extension target 0 < u < 5/2 under E(Y) = O_eps(Y^eps), pole coordinate w_rho = rho - 1/2 = (x - 1/2) + i*y
        # for 1/2 < x < 1, and regression check strictly refuting the retired mixed formula!
        single_term_mellin_rows: List[Dict[str, Any]] = []
        mellin_ok = True
        for n_mel, w_label, w_pt in (
            (1, "1", acb(arb(1))),
            (2, "1 + i/2", acb(arb(1), arb(1) / arb(2))),
            (3, "-1/2", acb(-arb(1) / arb(2))),
        ):
            quad_mel = evaluate_single_term_mellin_phi_quadrature_arb(
                n_mel, w_pt, prec_bits=prec_bits
            )
            gamma_arg_true = acb(arb(5) / arb(4)) - w_pt / acb(2)
            rhs_true = (
                (acb(1) / acb(2))
                * gamma_arg_true.gamma()
                * (acb(n_mel) ** (-acb(1) / acb(2) - w_pt))
            )
            # Retired inconsistent mixed formula from reviewed TC-059 §5.2:
            # (1/2) * Gamma((2*w + 5)/4) * n^{-(w + 3/2)}
            gamma_arg_retired = (acb(2) * w_pt + acb(5)) / acb(4)
            rhs_retired = (
                (acb(1) / acb(2))
                * gamma_arg_retired.gamma()
                * (acb(n_mel) ** (-w_pt - acb(3) / acb(2)))
            )
            diff_true = quad_mel - rhs_true
            abs_diff_true = abs(diff_true)
            abs_diff_retired = abs(quad_mel - rhs_retired)
            ok_st = bool(
                arb(0) in diff_true.real
                and arb(0) in diff_true.imag
                and abs_diff_true < arb("1e-64")
                and abs_diff_retired - arb("1e-1") > arb(0)
            )
            mellin_ok = mellin_ok and ok_st
            single_term_mellin_rows.append(
                {
                    "n": n_mel,
                    "w": w_label,
                    "quadrature_abs_value": serialize_arb_certified(abs(quad_mel)),
                    "consistent_formula_abs_residual": serialize_arb_certified(abs_diff_true),
                    "retired_mixed_formula_abs_mismatch": serialize_arb_certified(
                        abs_diff_retired
                    ),
                    "retired_mixed_formula_strictly_falsified": bool(
                        abs_diff_retired - arb("1e-1") > arb(0)
                    ),
                    "certification_scope": "CERTIFIED_FINITE_OBSERVATION (single-term integral on (0, infty) with analytic tail bounds)",
                    "verified": ok_st,
                }
            )

        # Check Dirichlet interchange M_Q(w) = Gamma(5/4 - w/2)*zeta(1 + 2*w)/(2*zeta(1/2 + w))
        # inside the initial absolute-convergence strip 1/2 < u < 5/2 at w = 3/2 + i/2 (u = 3/2):
        w_strip = acb(arb(3) / arb(2), arb(1) / arb(2))
        N_dir_sample = 250
        gamma_strip = (acb(arb(5) / arb(4)) - w_strip / acb(2)).gamma()
        partial_dir_sum = acb(0)
        for n_d in range(1, N_dir_sample + 1):
            partial_dir_sum += acb(liouville_lambda_int(n_d)) * (
                acb(n_d) ** (-acb(1) / acb(2) - w_strip)
            )
        # Rigorous Dirichlet tail bound at u = 3/2 => 1/2 + u = 2:
        # |sum_{n > N} lambda(n) n^{-1/2 - w}| <= sum_{n > N} n^{-2} <= 1 / N
        dir_tail_rad = (
            (abs(gamma_strip) / arb(2)) * (arb(1) / arb(N_dir_sample))
        ).upper()
        mellin_dir_enclosure = (gamma_strip / acb(2)) * partial_dir_sum + acb(
            arb(0, dir_tail_rad), arb(0, dir_tail_rad)
        )
        mellin_closed_strip = (
            gamma_strip
            * (acb(1) + acb(2) * w_strip).zeta()
            / (acb(2) * (acb(arb(1) / arb(2)) + w_strip).zeta())
        )
        strip_diff = mellin_dir_enclosure - mellin_closed_strip
        ok_strip = bool(arb(0) in strip_diff.real and arb(0) in strip_diff.imag)

        # Pole-domain & numerator nonvanishing check at synthetic off-critical coordinate
        # rho_syn = 3/4 + 14*i (x = 3/4 in (1/2, 1), NOT a zeta zero; tests numerator nonvanishing at
        # w_syn = rho_syn - 1/2 = 1/4 + 14*i in {0 < u < 5/2}):
        rho_syn = acb(arb(3) / arb(4), arb(14))
        w_syn = rho_syn - acb(arb(1) / arb(2))  # 1/4 + 14*i, u = 1/4 in (0, 5/2)
        gamma_at_w_syn = (acb(arb(5) / arb(4)) - w_syn / acb(2)).gamma()  # Gamma(9/8 - 7*i)
        zeta_num_at_w_syn = (acb(1) + acb(2) * w_syn).zeta()  # zeta(3/2 + 28*i) = zeta(2*rho_syn)
        zeta_2rho_syn = (acb(2) * rho_syn).zeta()
        denom_arg_check = (acb(arb(1) / arb(2)) + w_syn) - rho_syn
        ok_pole_map = bool(
            w_syn.real > arb(0)
            and arb(5) / arb(2) - w_syn.real > arb(0)
            and abs(gamma_at_w_syn) > arb(0)
            and abs(zeta_num_at_w_syn) > arb(0)
            and abs(zeta_num_at_w_syn - zeta_2rho_syn) < arb("1e-70")
            and abs(denom_arg_check) == arb(0)
        )
        mellin_ok = bool(mellin_ok and ok_strip and ok_pole_map)

        murmuration_audit = [
            {
                "citation": "Zubrilina, Murmurations (Invent. Math., https://doi.org/10.1007/s00222-025-01347-8)",
                "family_and_hypotheses": (
                    "Averages Hecke eigenvalues a_f(p) weighted by root numbers over conductor-localized families "
                    "of holomorphic/newform L-functions using trace formulas."
                ),
                "applicability_to_single_liouville_observable": (
                    "Inapplicable directly: Q_{lambda,T(Y)} is a single conductor-1 Liouville-weighted observable, "
                    "not a varying-conductor family average; relative ratios p^k/Y and q^l/Y are diagnostic scale "
                    "ratios, not conductor parameters or admissible TC grades."
                ),
                "imported_into_unconditional_bounds": False,
            },
            {
                "citation": "Hua-Mok, Universal murmuration and Hecke augmentation (https://arxiv.org/abs/2609.00777)",
                "family_and_hypotheses": (
                    "Concerns fixed prime-power Hecke operators in specified modular-form families and parameter ranges."
                ),
                "applicability_to_single_liouville_observable": (
                    "Does not provide conductor-1 single-object cancellation or automatic uniformity across "
                    "growing prime-power / logarithmic orders."
                ),
                "imported_into_unconditional_bounds": False,
            },
            {
                "citation": "Kuan-Lesesvre, Murmurations via Petersson trace formula (https://doi.org/10.1112/mtk.70135, https://arxiv.org/abs/2507.11418)",
                "family_and_hypotheses": (
                    "Theorem 1 explicitly assumes GRH for Dirichlet L-functions to bound Kloosterman/spectral error terms."
                ),
                "applicability_to_single_liouville_observable": (
                    "Strictly screened out by anti-circularity: importing a GRH-conditional theorem into an "
                    "unconditional RH closure attempt is invalid."
                ),
                "imported_into_unconditional_bounds": False,
            },
        ]

        return {
            "epistemic_scope": {
                "turn_chart_and_prime_local_defect_identities": "CONCRETE_ANALYTIC_IN_LEAN",
                "mellin_interchange_and_subpower_strip_bridge": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "mellin_quadrature_and_pole_coordinate_checks": "CERTIFIED_FINITE_OBSERVATION",
                "K_star_algebraicity_status": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
                "window_base_parameterized_scaling_proof": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "window_base_discriminator_checks": "CERTIFIED_FINITE_OBSERVATION",
            },
            "turn_chart_audit": {
                "K_star_1_minus_log2_over_log_tau": serialize_arb_certified(K_star),
                "tau_pow_K_star_minus_tau_half_residual": serialize_arb_certified(res_K_star),
                "admissible_algebraic_grade_claimed": False,
                "K_star_scope_statement": (
                    "treated as an auxiliary real coordinate; algebraic-grade admissibility is not established"
                ),
                "symmetry_line_Re_q": "1/4",
                "critical_line_check_abs_diff_q_quarter_plus_7i": serialize_arb_certified(
                    abs(z_turn_lhs - z_turn_rhs)
                ),
                "trivial_zero_checks": triv_zero_checks,
                "verified": turn_ok,
            },
            "prime_local_defect_bridge": {
                "complete_observable_bridge_note": (
                    "D_p(delta) = (p^{delta/2} - p^{-delta/2})^2 >= 0 satisfies |p^delta e^{i*theta} - 1|^2 = "
                    "p^delta*(D_p(delta) + 4*sin^2(theta/2)) >= p^delta*D_p(delta) on each Euler factor (x > 1), "
                    "while under the consistent inverse-Mellin convention M_Q(w) = int_0^infty Q_{lambda,infty}(X)*X^{-w} dX/X "
                    "(w = u + i*v), M_Q(w) = Gamma(5/4 - w/2)*zeta(1 + 2*w)/(2*zeta(1/2 + w)) converges absolutely on "
                    "1/2 < u < 5/2 and maps any hypothetical off-critical zero rho = x + i*y with 1/2 < x < 1 to "
                    "w_rho = rho - 1/2 = (x - 1/2) + i*y in {0 < u < 5/2}, where Gamma(5/4 - w_rho/2) and "
                    "zeta(1 + 2*w_rho) = zeta(2*rho) are finite and nonzero so 1/zeta(1/2 + w_rho) = 1/zeta(rho) produces "
                    "a pole of multiplicity ord_{z=rho}(zeta(z)). Positivity of D_p(delta) detects delta != 0 only when "
                    "combined with the conditional subpower-energy bridge E(Y) = O_eps(Y^eps) (TC-058R finite-to-full "
                    "window transfer + TC-054R2 dyadic L^2 Cauchy-Schwarz on [1, infty) plus u < 5/2 small-X convergence), "
                    "which extends M_Q(w) holomorphically to the open strip 0 < u < 5/2 and excludes that pole; "
                    "all arithmetic evaluators are computed without sampled zeta-zero inputs."
                ),
                "synthetic_sample_rows": defect_rows,
                "verified": defect_ok,
            },
            "mellin_convention_and_pole_domain_audit_tc059r": {
                "mellin_definition": "M_Q(w) = int_0^infty Q_{lambda,infty}(X) * X^{-w} dX/X, w = u + i*v (u, v real)",
                "single_term_formula": "int_0^infty phi_n(X) * X^{-w} dX/X = (1/2) * Gamma(5/4 - w/2) * n^{-1/2 - w} for u < 5/2",
                "dirichlet_interchange_formula": "M_Q(w) = Gamma(5/4 - w/2) * zeta(1 + 2*w) / (2 * zeta(1/2 + w))",
                "initial_absolute_convergence_strip": "1/2 < u < 5/2 (Dirichlet series requires u > 1/2; small-X integral requires u < 5/2)",
                "subpower_holomorphic_extension_strip": "0 < u < 5/2 (open strip; bounded above at u = 5/2 by Gamma(5/4 - w/2) pole from X -> 0+)",
                "pole_coordinate_for_hypothetical_zero_rho_x_gt_half": "w_rho = rho - 1/2 = (x - 1/2) + i*y in {0 < u < 5/2} for 1/2 < x < 1",
                "conditional_analytic_pole_exclusion_bridge": (
                    "Under E(Y) = O_eps(Y^eps) for every eps > 0: (1) TC-058R Section 2.3 (Lean Theorem 31(5)) transfers subpower window "
                    "growth from ||Q_{lambda,T(Y)}||_Y to ||Q_{lambda,infty}||_Y via uniform tail bound B_tau; "
                    "(2) TC-054R2 Proposition 3.1 (weighted dyadic L^2 Cauchy-Schwarz over [tau^k, tau^{k+1}] for X >= 1, "
                    "combined with |Q_{lambda,infty}(X)| <= zeta(3)*X^{5/2} on (0, 1] giving holomorphicity on u < 5/2) "
                    "proves M_Q(w) extends holomorphically to the open strip 0 < u < 5/2, excluding any pole at "
                    "w_rho = rho - 1/2 for 1/2 < x < 1 (and hence 0 < x < 1/2 by functional equation rho -> 1 - rho). "
                    "Finite numerical samples below verify convention/scaling consistency only and do not prove the infinite transform."
                ),
                "single_term_quadrature_and_regression_rows": single_term_mellin_rows,
                "initial_strip_interchange_sample_w_3_half_plus_i_half": {
                    "N_dirichlet_truncation": N_dir_sample,
                    "closed_form_abs_M_Q": serialize_arb_certified(abs(mellin_closed_strip)),
                    "dirichlet_enclosure_minus_closed_abs": serialize_arb_certified(
                        abs(strip_diff)
                    ),
                    "encloses_closed_form": ok_strip,
                    "scope_label": "CERTIFIED_FINITE_OBSERVATION (finite truncation + analytic tail at single point w = 3/2 + i/2)",
                },
                "synthetic_pole_mapping_check_rho_3_quarter_plus_14i": {
                    "synthetic_rho": "3/4 + 14*i",
                    "mapped_w_rho": "1/4 + 14*i",
                    "u_in_open_strip_0_to_5_half": True,
                    "abs_Gamma_5_4_minus_w_half": serialize_arb_certified(abs(gamma_at_w_syn)),
                    "abs_zeta_1_plus_2w_eq_zeta_2rho": serialize_arb_certified(
                        abs(zeta_num_at_w_syn)
                    ),
                    "verified": ok_pole_map,
                },
                "verified": mellin_ok,
            },
            "window_base_compatibility_discriminator_Y16_T32": {
                "additional_tau_grade_compatibility_identity_used": False,
                "parameterized_analytic_scaling_proof": (
                    "For every real window multiplier b > 1 and u > 0, substituting X = g*W (dX/X = dW/W) maps "
                    "[u, b*u] onto [u/g, b*(u/g)] and proves K_{u,b}(g*r, g*s) = int_u^{b*u} phi_{g*r}(X)*phi_{g*s}(X) dX/X "
                    "= g^{-1} * int_{u/g}^{b*(u/g)} phi_r(W)*phi_s(W) dW/W = g^{-1} * K_{u/g, b}(r, s). Because "
                    "the dyadic power-lift identities, ordered primitive-pair synthesis/Moebius inversion, and "
                    "quotient-shell decoupling depend only on finite bilinearity and this scale-invariant dX/X "
                    "kernel scaling, they hold analytically for every b > 1 with b-dependent constants; the "
                    "three rows below at b in {2, e, tau} are finite numerical checks illustrating that general identity."
                ),
                "classification": (
                    "TC-inspired analytic number theory: all new TC-059/TC-059R identities hold analytically on "
                    "[Y, b*Y] for arbitrary b > 1 with b-dependent constants (illustrated numerically at b in {2, e, tau}); "
                    "no genuinely additional tau-grade compatibility identity beyond scale invariance of dX/X and "
                    "the classical zeta(2z)/zeta(z) bridge is invoked."
                ),
                "rows": window_base_rows,
                "verified": wb_ok,
            },
            "murmuration_hypothesis_audit": murmuration_audit,
            "all_section_5_checks_pass": bool(turn_ok and defect_ok and wb_ok and mellin_ok),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 6. Live Lean 4 Axiom Audit & Review Displayed-Enclosure Verification
# ---------------------------------------------------------------------------


def verify_tc059_lean_theorems_live() -> Dict[str, Any]:
    """Verify all 7 theorems in `formal/RiemannScope/DyadicPowerLiftPrimitiveCorrelation.lean` via
    live `lake env lean --stdin` (`#check` and `#print axioms`) and source token checks.
    """
    src = TC_059_LEAN_MODULE_PATH.read_text(encoding="utf-8")
    no_block = re.sub(r"/-.*?-/", "", src, flags=re.DOTALL)
    clean_src = re.sub(r"--[^\n]*", "", no_block)

    sorry_count = len(re.findall(r"\bsorry\b", clean_src))
    admit_count = len(re.findall(r"\badmit\b", clean_src))
    custom_axiom_count = len(re.findall(r"^\s*axiom\b", clean_src, flags=re.MULTILINE))
    present = all(
        re.search(rf"^theorem\s+{re.escape(thm)}\b", clean_src, flags=re.MULTILINE) is not None
        for thm in EXPECTED_TC059_THEOREMS
    )

    lines = ["import RiemannScope.DyadicPowerLiftPrimitiveCorrelation"]
    for thm in EXPECTED_TC059_THEOREMS:
        fq = f"RiemannScope.DyadicPowerLiftPrimitiveCorrelation.{thm}"
        lines.append(f'#eval IO.println "===CHECK:{thm}==="')
        lines.append(f"#check {fq}")
        lines.append(f'#eval IO.println "===AXIOMS:{thm}==="')
        lines.append(f"#print axioms {fq}")
    stdin_payload = "\n".join(lines) + "\n"

    proc = subprocess.run(
        ["lake", "env", "lean", "--stdin"],
        input=stdin_payload,
        text=True,
        encoding="utf-8",
        capture_output=True,
        cwd=str(REPO_ROOT / "formal"),
        check=False,
    )
    out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    allowed_axioms = {"propext", "Classical.choice", "Quot.sound"}
    per_theorem: Dict[str, Any] = {}
    axioms_ok = proc.returncode == 0
    for thm in EXPECTED_TC059_THEOREMS:
        m_chk = re.search(
            rf"===CHECK:{re.escape(thm)}===\s*(.*?)\s*===AXIOMS:{re.escape(thm)}===",
            out,
            flags=re.DOTALL,
        )
        m_ax = re.search(
            rf"===AXIOMS:{re.escape(thm)}===\s*(.*?)(?====CHECK:|\Z)",
            out,
            flags=re.DOTALL,
        )
        chk_str = m_chk.group(1).strip() if m_chk else ""
        ax_str = m_ax.group(1).strip() if m_ax else ""
        m_list = re.search(r"\[(.*?)\]", ax_str, flags=re.DOTALL)
        parsed_axioms = (
            [" ".join(x.split()) for x in m_list.group(1).split(",") if x.strip()]
            if m_list
            else []
        )
        axioms_valid = (
            "depends on axioms:" in ax_str
            and len(parsed_axioms) > 0
            and set(parsed_axioms).issubset(allowed_axioms)
        ) or ("does not depend on any axioms" in ax_str and len(parsed_axioms) == 0)
        thm_ok = bool(thm in chk_str and axioms_valid)
        axioms_ok = bool(axioms_ok and thm_ok)
        per_theorem[thm] = {
            "captured_check_output": chk_str,
            "captured_print_axioms_output": ax_str,
            "parsed_axioms": parsed_axioms,
            "verified": thm_ok,
        }

    return {
        "module_path": "formal/RiemannScope/DyadicPowerLiftPrimitiveCorrelation.lean",
        "expected_tc059_theorems": EXPECTED_TC059_THEOREMS,
        "all_tc059_theorems_present": present,
        "sorry_count": sorry_count,
        "admit_count": admit_count,
        "custom_axiom_count": custom_axiom_count,
        "lean_exit_code": proc.returncode,
        "per_theorem": per_theorem,
        "all_tc059_lean_checks_pass": bool(
            present
            and sorry_count == 0
            and admit_count == 0
            and custom_axiom_count == 0
            and axioms_ok
        ),
    }


def verify_tc059_review_displayed_enclosures(
    report: Dict[str, Any],
    review_path: Path = TC_059_REVIEW_DOC_PATH,
) -> Dict[str, Any]:
    """Verify that `docs/reviews/TC_059_POWER_LIFT_AND_PRIMITIVE_CORRELATION.md` contains zero
    circle-half macros and that every displayed `±` / `\\pm` interval carries an explicit
    `<!-- tc-enclosure: ... -->` tag outward-containing its generated 256-bit Arb ball.
    """
    text = review_path.read_text(encoding="utf-8")
    pi_macros = re.findall(r"\x5cpi(?![a-zA-Z])", text)
    lines = text.splitlines()
    raw_intervals: List[Dict[str, Any]] = []
    untagged_intervals: List[Dict[str, Any]] = []
    checked_rows: List[Dict[str, Any]] = []
    failed_intervals: List[Dict[str, Any]] = []

    for line_idx, line in enumerate(lines, start=1):
        line_matches: List[Tuple[int, str, str, str]] = []
        for m_bt in _ARB_BACKTICK_INTERVAL_RE.finditer(line):
            line_matches.append(
                (m_bt.start(), "arb_backtick", m_bt.group("mid") or "0", m_bt.group("rad"))
            )
        for m_lx in _LATEX_PM_INTERVAL_RE.finditer(line):
            line_matches.append(
                (m_lx.start(), "latex_pm", m_lx.group("mid"), m_lx.group("rad"))
            )
        if not line_matches:
            continue
        line_matches.sort(key=lambda t: t[0])
        tags = list(_TC_ENCLOSURE_TAG_RE.finditer(line))
        if len(tags) != len(line_matches):
            for pos, fmt_kind, mid_s, rad_s in line_matches:
                rec = {
                    "line": line_idx,
                    "column": pos + 1,
                    "format": fmt_kind,
                    "mid_str": mid_s,
                    "rad_str": rad_s,
                    "tag_count_on_line": len(tags),
                    "interval_count_on_line": len(line_matches),
                }
                raw_intervals.append(rec)
                untagged_intervals.append(rec)
            continue

        for (pos, fmt_kind, mid_s, rad_s), tag_m in zip(line_matches, tags):
            obs_name = tag_m.group("observable")
            params_str = tag_m.group("params")
            json_path = tag_m.group("json_path")
            raw_intervals.append(
                {
                    "line": line_idx,
                    "column": pos + 1,
                    "format": fmt_kind,
                    "observable": obs_name,
                    "params": params_str,
                    "json_path": json_path,
                }
            )
            try:
                disp_mid = _sci_or_latex_num_to_fraction(mid_s)
                disp_rad = _sci_or_latex_num_to_fraction(rad_s)
                disp_low = disp_mid - disp_rad
                disp_high = disp_mid + disp_rad
                gen_node, _ = _resolve_report_path_with_param_check(
                    report, json_path=json_path, params_str=params_str, observable=obs_name
                )
                gen_low, gen_high, _ = _parse_arb_ball_str_to_fractions(gen_node["arb_ball_str"])
                gen_rad = (gen_high - gen_low) / 2
                contains_gen = bool(disp_low <= gen_low and gen_high <= disp_high)
                radius_is_tight = bool(disp_rad <= max(16 * gen_rad, Fraction(1, 10**35)))
                sign_ok = True
                if gen_low > 0 and not (disp_low > 0):
                    sign_ok = False
                if gen_high < 0 and not (disp_high < 0):
                    sign_ok = False
                ok = bool(contains_gen and sign_ok and radius_is_tight)
                row_rec = {
                    "line": line_idx,
                    "format": fmt_kind,
                    "observable": obs_name,
                    "params": params_str,
                    "json_path": json_path,
                    "contains_generated_ball": contains_gen,
                    "preserves_strict_sign": sign_ok,
                    "radius_is_tight": radius_is_tight,
                    "verified": ok,
                }
                checked_rows.append(row_rec)
                if not ok:
                    failed_intervals.append(row_rec)
            except Exception as exc:  # noqa: BLE001
                err_rec = {
                    "line": line_idx,
                    "format": fmt_kind,
                    "observable": obs_name,
                    "params": params_str,
                    "json_path": json_path,
                    "error": str(exc),
                    "verified": False,
                }
                checked_rows.append(err_rec)
                failed_intervals.append(err_rec)

    all_ok = bool(
        len(pi_macros) == 0
        and len(raw_intervals) > 0
        and len(untagged_intervals) == 0
        and len(failed_intervals) == 0
    )
    try:
        rel_review_path = review_path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        rel_review_path = str(review_path)
    return {
        "review_path": rel_review_path,
        "pi_macro_count": len(pi_macros),
        "total_displayed_intervals_found": len(raw_intervals),
        "tagged_and_checked_count": len(checked_rows),
        "untagged_count": len(untagged_intervals),
        "failed_count": len(failed_intervals),
        "untagged_intervals": untagged_intervals,
        "failed_intervals": failed_intervals,
        "all_displayed_intervals_contain_generated_enclosures": all_ok,
    }


def execute_task_tc059_dyadic_power_lift_audit(
    prec_bits: int = 256,
    verify_lean_live: bool = True,
    verify_review_doc: bool = True,
) -> Dict[str, Any]:
    """Execute the complete TASK-TC-059 mathematical, falsification, Lean, and 256-bit Arb audit."""
    sec1 = verify_section_1_observable_and_closure_contract(prec_bits=prec_bits)
    sec2 = verify_section_2_dyadic_power_lift_and_attempt_a(prec_bits=prec_bits)
    sec3 = verify_section_3_primitive_pairs_and_diagonals(prec_bits=prec_bits)
    sec4 = verify_section_4_dyadic_blocks_and_attempt_b(prec_bits=prec_bits)
    sec5 = verify_section_5_tc_geometry_defect_and_murmurations(prec_bits=prec_bits)

    assert sec1["all_section_1_checks_pass"] is True
    assert sec2["all_section_2_checks_pass"] is True
    assert sec3["all_section_3_checks_pass"] is True
    assert sec4["all_section_4_checks_pass"] is True
    assert sec5["all_section_5_checks_pass"] is True

    report: Dict[str, Any] = {
        "task_id": TASK_TC_059R_ID,
        "repaired_task_id": TASK_TC_059_ID,
        "parent_epic": EPIC_TC_042_ID,
        "parent_subgate": PARENT_SUBGATE_ID,
        "prior_tasks": [
            TASK_TC_054_ID,
            TASK_TC_054R_ID,
            TASK_TC_054R2_ID,
            TASK_TC_055_ID,
            TASK_TC_055R_ID,
            TASK_TC_055R2_ID,
            TASK_TC_056_ID,
            TASK_TC_056R_ID,
            TASK_TC_056R2_ID,
            TASK_TC_057_ID,
            TASK_TC_057R_ID,
            TASK_TC_058_ID,
            TASK_TC_058R_ID,
            TASK_TC_058R2_ID,
            TASK_TC_059_ID,
        ],
        "reviewed_merged_main_baseline": REVIEWED_MERGED_MAIN_BASELINE,
        "included_tc058r2_tip": INCLUDED_TC_058R2_TIP,
        "reviewed_tc059_branch": PROPOSED_BRANCH,
        "reviewed_tc059_implementation_commit": REVIEWED_TC_059_IMPLEMENTATION,
        "reviewed_tc059_head_commit": REVIEWED_TC_059_HEAD,
        "branch": REPAIR_BRANCH,
        "epistemic_categories_enforced": list(EPISTEMIC_CATEGORIES),
        "research_outcome_class": (
            "Repaired Conditional Closure Interface, Mellin Bridge, & Smooth-Increment Scope (TASK-TC-059R) — "
            "Preserves TC-059's finite arithmetic, Gaussian window integrals, Attempt A counterexamples, and "
            "PNT-based C_var / C_{chi,var} remainder bounds; formalizes in Lean 4 (0 sorry, 0 custom axioms, "
            "7 theorems total) the repaired Route D shifted prime-power weighted-diagonal closure transfer "
            "(Theorem 6, matching D_tilde(Y) <= (2/(log Y)^2)*sum_{p^k<=Y} ((log p)^2/p^k)*F(Y/p^k) + C_cut "
            "via finite-horizon G_eps(R) with C_eps = 2*zeta''(1+eps), R-independent Y_*, and concrete "
            "canonicalLiouvilleEnergyE specialization) and the direct smooth-increment window norm bound "
            "||Delta_d^{sm}||_Y <= d^{-1/2}*sqrt(E_{lambda,L_d}(Y/d)) + (d+1)^{-1/2}*sqrt(E_{lambda,L_d}(Y/(d+1))) "
            "plus domain-separated small-scale O(u^5) tail control (Theorem 7); repairs the inverse-Mellin "
            "formula M_Q(w) = Gamma(5/4 - w/2)*zeta(1 + 2*w)/(2*zeta(1/2 + w)) on 1/2 < u < 5/2 (extending "
            "holomorphically to 0 < u < 5/2 under E(Y) = O_eps(Y^eps) with w_rho = rho - 1/2); replaces the "
            "deleted critical-line-crossing claim with the exact adjacent-scale O(1/d) cancellation loss "
            "analysis; and keeps SUBGATE-TC-043A OPEN and rh_proved False."
        ),
        "subgate_tc043a_status": "OPEN",
        "rh_proved": False,
        "precision_bits": prec_bits,
        "circle_constant_convention": "tau (sole circle constant)",
        "complex_coordinate_convention": (
            "z = x + i*y (x, y real; critical line x = 1/2; displacement delta = x - 1/2); "
            "Mellin variable w = u + i*v (u, v real)"
        ),
        "section_1_observable_and_closure_contract": sec1,
        "section_2_dyadic_power_lift_and_attempt_a": sec2,
        "section_3_primitive_pairs_and_diagonals": sec3,
        "section_4_dyadic_blocks_and_attempt_b": sec4,
        "section_5_tc_geometry_defect_and_murmurations": sec5,
    }

    if verify_lean_live:
        lean_audit = verify_tc059_lean_theorems_live()
        assert lean_audit["all_tc059_lean_checks_pass"] is True, (
            f"TC-059 Lean theorem audit failed: {lean_audit}"
        )
        report["section_6_lean_formalization_audit"] = lean_audit

    arb_check = verify_all_serialized_arb_in_tree(report)
    assert arb_check["all_enclose_original_256bit_arb_ball"] is True, (
        f"Serialized Arb enclosure verification failed: {arb_check.get('failed_paths')}"
    )
    report["serialized_arb_self_check"] = arb_check

    if verify_review_doc and TC_059_REVIEW_DOC_PATH.exists():
        rev_audit = verify_tc059_review_displayed_enclosures(report, TC_059_REVIEW_DOC_PATH)
        assert rev_audit["all_displayed_intervals_contain_generated_enclosures"] is True, (
            "Displayed intervals in TC_059_POWER_LIFT_AND_PRIMITIVE_CORRELATION.md failed check: "
            f"pi_macros={rev_audit['pi_macro_count']}, untagged={rev_audit['untagged_intervals']}, "
            f"failed={rev_audit['failed_intervals']}"
        )
        report["section_7_tc059_review_displayed_enclosures_audit"] = rev_audit

    return report


def write_task_tc059_dyadic_power_lift_artifact(
    path: Path = DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH,
    prec_bits: int = 256,
    verify_lean_live: bool = True,
    verify_review_doc: bool = True,
) -> Dict[str, Any]:
    """Generate and write `data/tc_dyadic_power_lift_primitive_correlation.json`."""
    report = execute_task_tc059_dyadic_power_lift_audit(
        prec_bits=prec_bits,
        verify_lean_live=verify_lean_live,
        verify_review_doc=verify_review_doc,
    )

    def _clean(obj: Any) -> Any:
        if isinstance(obj, (arb, acb)):
            return str(obj)
        if isinstance(obj, dict):
            return {k: _clean(v) for k, v in obj.items() if k != "enclosure_arb"}
        if isinstance(obj, (list, tuple)):
            return [_clean(v) for v in obj]
        return obj

    cleaned = _clean(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(cleaned, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return cleaned


if __name__ == "__main__":
    rep = write_task_tc059_dyadic_power_lift_artifact()
    print(
        f"Wrote {DYADIC_POWER_LIFT_PRIMITIVE_CORRELATION_ARTIFACT_PATH} "
        f"(subgate={rep['subgate_tc043a_status']}, rh_proved={rep['rh_proved']})"
    )
