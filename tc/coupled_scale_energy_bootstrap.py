r"""
TASK-TC-057 / TASK-TC-057R: Arithmetic Compatibility Across Scales, Complete Prime-Power
Certification, Scoped Obstruction Theorems, and Proved Conditional Correlation Transfer
toward SUBGATE-TC-043A.

Implements and certifies in 256-bit FLINT/Arb ball arithmetic (using tau = 2*pi as the sole
circle constant and z = x + i*y, with x, y in R and critical line x = 1/2, for complex coordinates):
1. Opening Baseline Cross-Checks, Complete Higher Prime-Power Certificate, & Monotone Scale-Envelope
   Boundedness (Sections 1-2):
   - Verification of local TC-056R2 opening repairs: exact integer-power small-Y cutoff partition
     on [2, 4) into [2, 3^{4/5}] -> (4, 3), (3^{4/5}, 4^{4/5}] -> (4, 4) (with 2^{8/5} = 4^{4/5}),
     (4^{4/5}, 5^{4/5}] -> (5, 5) (with Y = 7/2 -> (5, 5)), (5^{4/5}, 4) -> (5, 6); Stieltjes
     prime-sum remainder (with exact offset logarithmic integral li_2(t) = int_2^t dv/log v satisfying
     li_2(2) = 0) vs. the complete k >= 2 higher prime-power sum
     2*sum_{p<=u} [-log(1 - p^{-alpha}) - p^{-alpha}], independently cross-checked against finite
     series 2 <= k < K plus proved tail 2*r^K / [K*(1 - r)] and exact first-omitted-term witness
     at p = 2, k = 40; and U-product logarithmic slack 2*sqrt(c) = delta / (2*sqrt(2)) < delta / 2.
   - Monotone envelope F(Y) := sup_{1 <= Z <= Y} E(Z) (Y >= 1): local boundedness
     0 <= E_L(Z) <= M_lin * Z (M_lin := (tau - 1) * M_1^2) across discontinuous jumps of
     T(Z) = ceil(Z^{5/4}), with certified jump witness E_3(2^{4/5}) - E_2(2^{4/5}) != 0.
   - Abstract polylog bootstrap implication (`CONDITIONAL_ON_RECURSION`, Lean Theorem 21) and
     repaired Proposition 2.4 coefficient-mass localization algebra (Lean Theorem 26): total mass
     B_0*(log Y)^b on d >= U(Y) = c*(log Y)^a is an upper bound on Theta_sigma(Y), requiring
     quantitative mass localization near U(Y) for the lower barrier sigma < b / a, contrasted
     against the concentration negative control at d = floor(Y) where (log Y)^b * floor(Y)^{-sigma} -> 0.
2. Route A — General Moebius-Rough Prime-Filtration Descent (Section 3, Lean Theorem 22):
   - Exact finite identity for all U >= 2, T >= 0, X >= 0 and completely multiplicative a:
     Q_{a,T}(X) = S_{a,<U,T}(X) - sum_{U <= d <= T, d | N_{[U,T]}} (mu(d)*a(d)/sqrt(d)) Q_{a,floor(T/d)}(X/d).
   - Uniform Liouville sign mu(d)*lambda(d) = +1 across primes and composite squarefree rough
     divisors vs. 2-adic parity control a_2 sign alternation; super-sqrt(T) reduction at U = 42, T = 431;
     and proved prime-subset lower bound M_{A,sigma}(Y) >= (sum_{U<=p<=T(Y)} p^{-(1+sigma)/2})^2
     >>_sigma T(Y)^{1-sigma}/(log T(Y))^2 -> infty obstructing the homogeneous Cauchy-Schwarz majorant.
3. Route B & Route C — Logarithmic Prime-Power Descent, Narrowed Fixed-Span Non-Closure, and
   Second-Order Liouville-Selberg Summatory Derivation & Abel Majorant Obstruction (Section 4,
   Lean Theorem 23):
   - Exact prime-power identity sum_{1<=n<=T} a(n) log(n) (log(X/n))^m phi_n(X)
     = sum_{p^k<=T} a(p)^k log(p) p^{-k/2} Q_{a,floor(T/p^k)}^{[m]}(X/p^k) (including T = 0, 1),
     shift recurrence (log X) Q_T^{[m]}(X) = Sigma_pp^{[m]}(X) + Q_T^{[m+1]}(X), M-step telescope,
     linear independence of {(log w)^m w^{5/2} e^{-w^2}} ruling out exact closure in a fixed finite
     linear span (while M approx 2*log Y gives M!/[2^M*(log Y)^M] ~ sqrt(log Y)*Y^{-2}, leaving
     accumulated prime-power layers open), and uniform bound M_1^{[m]} via u^{3+m/2} <= u^{m+5/2}.
   - Second-order Selberg-type identity w_{2,a} = Lambda_a * log + Lambda_a * Lambda_a (with
     Dirichlet-series convergence on x > 1, z = x + i*y, restricted to bounded controls |a(n)| <= 1),
     complete PNT/Dirichlet-hyperbola summatory proof sum_{d<=u} w_{2,lambda}(d)
     = [4*zeta'(2)/zeta(2) - 2*gamma_E]*u + O(u*exp(-c''*sqrt(log u))) via Lambda_lambda = -Lambda + 2*B,
     and exact discrete Abel summation identity on 2 <= d <= b = floor(Y) whose specified
     triangle-inequality majorant is obstructed by its b = floor(Y) boundary term >> sqrt(Y).
4. Exact Cutoff Comparison, Scoped Linear Cutoff Bounds, Small-Scale Positivity, & Base-Scale
   Energy Floor (Section 5, Lean Theorem 25):
   - Explicit counterexample (Y = 9/4, d = 2): L_2 = floor(T(9/4)/2) = 1 < 2 = T(9/8) with
     Q_{lambda,1}(9/8) - Q_{lambda,2}(9/8) > 0 and E_1(9/8) != E_2(9/8); exact d >= 16 ordering
     L_d >= T(Y/d) and all-d bound E_{L_d}(W) <= 2 E(W) + ((tau^5 - 1)/10) max(16/d, 1).
   - Separate evaluation of actual signed aggregate linear cutoff error, Minkowski sum of individual
     error norms, and unsigned analytic majorant (asymp Y/(log Y)^2) vs. O(1) diagonal cutoff error.
   - Uniform small-scale positivity on w in (0, 1] and certified all-L base-scale energy floor
     inf_{W in [1,2], L >= 1} E_L(W) >= m_{all-L} > 0 via [2, tau] subset [W, tau W].
5. Route D — Direct Quadratic Prime-Power Expansion, Unconditional Diagonal Contraction, & Proved
   Conditional Same-Scale Absorption Transfer (Section 6, Lean Theorems 24 & 26):
   - Unconditional cross-scale diagonal inequality D_tilde_{lambda,pp}(Y) <= D_{lambda,pp}(Y)
     <= (2/(log Y)^2) sum_{p^k<=Y} ((log p)^2/p^k) F(Y/p^k) + C_{cut,diag} with all-epsilon
     contraction factor Theta_eps^{diag}(Y) < 2*zeta''(1+eps)/(log Y)^2 -> 0, plus complete proof
     and Lean 4 formalization (`CONDITIONAL_ON_SIGNED_CORRELATION`, Theorem 26) that the sufficient
     condition X_tilde_{lambda,pp}(Y) + E_{sh,1}(Y) <= A_eta Y^eta + theta_eta F(Y) (theta_eta in [0, 1/2))
     implies E(Y) <<_eps Y^eps via finite-horizon G_eps(R) = sup_{1<=Z<=R} E(Z)/Z^eps absorption
     (forward implication only; equivalence is not asserted without separately proving a shifted-kernel converse).
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import sys
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from flint import acb, acb_series, arb, ctx as flint_ctx

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tc.canonical_theta_correlation_bound import (
    EPIC_TC_042_ID,
    REPO_ROOT,
    serialize_arb_certified,
    verify_all_serialized_arb_in_tree,
)
from tc.liouville_square_dilation import (
    PRIOR_MERGED_MAIN_TC_053R,
    TASK_TC_054_ID,
    TASK_TC_054R_ID,
    TASK_TC_054R2_ID,
    TASK_TC_055_ID,
    TASK_TC_055R_ID,
    TASK_TC_055R2_ID,
    TASK_TC_056_ID,
    TC_054R2_MERGED_MAIN_BASELINE,
    TC_055R2_IMPLEMENTATION_COMMIT,
    TC_055R2_REVIEWED_TIP,
    _ARB_BACKTICK_INTERVAL_RE,
    _LATEX_PM_INTERVAL_RE,
    _TC_ENCLOSURE_TAG_RE,
    _parse_arb_ball_str_to_fractions,
    _resolve_report_path_with_param_check,
    _sci_or_latex_num_to_fraction,
    finite_prime_parity_aS_int,
    generate_P_smooth_up_to,
    inflate_arb_with_nonneg_bound,
    liouville_lambda_int,
    two_adic_parity_a2_int,
)
from tc.prime_chain_contraction import (
    TASK_TC_056R_ID,
    TASK_TC_056R2_ID,
    TC_056_IMPLEMENTATION_COMMIT,
    TC_056_REVIEWED_TIP,
    TC_056R_REVIEWED_COMMIT,
    evaluate_phi_n_arb,
    exact_T_cutoff_ceil_Y_5_4,
    exact_U0_cutoff_ceil_2_Y_5_8,
    is_prime_int,
    primes_up_to,
)

TASK_TC_057_ID = "TASK-TC-057"
TASK_TC_057R_ID = "TASK-TC-057R"
TC_056R2_IMPLEMENTATION_COMMIT = "add6930233ebe0c8adf50da0e8a0ae6f18561975"
TC_056R2_REVIEWED_TIP = "8c92e89c62bdb434d29d7143bacf50308aab78a1"
TC_057_IMPLEMENTATION_COMMIT = "05e7e0f728a0c758973b40c1605793ed9b40f75b"
TC_057_REVIEWED_TIP = "82d0ec52085c06e748982287694fb9272ff017d7"

COUPLED_SCALE_BOOTSTRAP_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_coupled_scale_energy_bootstrap.json"
)
TC_057_REVIEW_DOC_PATH = (
    REPO_ROOT / "docs" / "reviews" / "TC_057_COUPLED_ARITHMETIC_SCALE_ENERGY_BOOTSTRAP.md"
)


# ---------------------------------------------------------------------------
# 1. Exact Integer Arithmetic, Divisor Sets, & Certified Arb Helpers
# ---------------------------------------------------------------------------


def _tau_arb() -> arb:
    """Return circle constant tau = 2*pi in current FLINT precision."""
    return arb(2) * arb.pi()


def _frac_to_arb(val: Union[int, Fraction]) -> arb:
    f = Fraction(val)
    return arb(int(f.numerator)) / arb(int(f.denominator))


def moebius_mu_int(n: int) -> int:
    """Exact integer Moebius function mu(n) for n >= 1."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError(f"moebius_mu_int requires integer n >= 1, got {n!r}")
    if n == 1:
        return 1
    rem = n
    omega_cnt = 0
    p = 2
    while p * p <= rem:
        if rem % p == 0:
            rem //= p
            if rem % p == 0:
                return 0
            omega_cnt += 1
        p += 1 if p == 2 else 2
    if rem > 1:
        omega_cnt += 1
    return -1 if (omega_cnt & 1) else 1


def rough_squarefree_divisors_band(U: int, T: int) -> Tuple[int, ...]:
    """Return sorted tuple of squarefree divisors d | prod_{U <= p <= T} p with U <= d <= T."""
    if not isinstance(U, int) or isinstance(U, bool) or U < 2:
        raise ValueError(f"U must be int >= 2, got {U!r}")
    if not isinstance(T, int) or isinstance(T, bool) or T < 0:
        raise ValueError(f"T must be int >= 0, got {T!r}")
    if T < U:
        return ()
    rough_primes = [p for p in primes_up_to(T) if p >= U]
    acc: List[int] = []

    def _dfs(idx: int, cur: int) -> None:
        for j in range(idx, len(rough_primes)):
            nxt = cur * rough_primes[j]
            if nxt > T:
                break
            acc.append(nxt)
            _dfs(j + 1, nxt)

    _dfs(0, 1)
    acc.sort()
    return tuple(acc)


def prime_power_pairs_up_to(T: int) -> Tuple[Tuple[int, int], ...]:
    """Return sorted tuple of (p, k) with p prime, k >= 1, and p^k <= T."""
    if not isinstance(T, int) or isinstance(T, bool) or T < 0:
        raise ValueError(f"T must be int >= 0, got {T!r}")
    if T < 2:
        return ()
    out: List[Tuple[int, int]] = []
    for p in primes_up_to(T):
        pk = p
        k = 1
        while pk <= T:
            out.append((p, k))
            pk *= p
            k += 1
    return tuple(out)


def prime_power_base_and_exp(n: int) -> Optional[Tuple[int, int]]:
    """If n = p^k with p prime and k >= 1, return (p, k); otherwise None."""
    if n < 2:
        return None
    rem = n
    p = 2
    while p * p <= rem:
        if rem % p == 0:
            k = 0
            while rem % p == 0:
                rem //= p
                k += 1
            return (p, k) if rem == 1 else None
        p += 1 if p == 2 else 2
    return (rem, 1)


def _weight_fn_for_mode(mode: str) -> Callable[[int], int]:
    if mode == "liouville":
        return liouville_lambda_int
    if mode == "a2":
        return two_adic_parity_a2_int
    if mode == "a_3_5_7":
        return lambda n: finite_prime_parity_aS_int(n, (3, 5, 7))
    if mode == "unsigned_1":
        return lambda _n: 1
    raise ValueError(f"Unsupported weight mode: {mode!r}")


def evaluate_Q_shifted_finite_arb(
    X_val: Union[int, Fraction, arb],
    L: int,
    m_shift: int = 0,
    mode: str = "liouville",
    prec_bits: int = 256,
) -> arb:
    """Evaluate Q_{a,L}^{[m]}(X) = sum_{1 <= q <= L} a(q) (log(X/q))^m phi_q(X) in Arb."""
    if L < 0 or m_shift < 0:
        raise ValueError(f"Invalid L={L} or m_shift={m_shift}")
    w_fn = _weight_fn_for_mode(mode)
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        if L == 0:
            return arb(0)
        X_arb = X_val if isinstance(X_val, arb) else _frac_to_arb(X_val)
        if not (X_arb > arb(0)):
            if m_shift == 0 and X_arb == arb(0):
                return arb(0)
            raise ValueError("X_val must be strictly positive when m_shift >= 1")
        total = arb(0)
        for q in range(1, L + 1):
            aq = arb(w_fn(q))
            phi_q = evaluate_phi_n_arb(X_arb, q, prec_bits=prec_bits)
            if m_shift == 0:
                total += aq * phi_q
            else:
                lg_ratio = (X_arb / arb(q)).log()
                total += aq * (lg_ratio ** m_shift) * phi_q
        return total
    finally:
        flint_ctx.prec = saved


def evaluate_Q_smooth_below_U_arb(
    X_val: Union[int, Fraction, arb],
    U: int,
    T: int,
    mode: str = "liouville",
    prec_bits: int = 256,
) -> arb:
    """Evaluate S_{a,<U,T}(X) = sum_{1 <= n <= T, all p|n satisfy p < U} a(n) phi_n(X)."""
    w_fn = _weight_fn_for_mode(mode)
    primes_below = tuple(p for p in primes_up_to(max(0, U - 1)))
    smooth_ns = generate_P_smooth_up_to(primes_below, T) if T >= 1 else ()
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X_arb = X_val if isinstance(X_val, arb) else _frac_to_arb(X_val)
        if X_arb == arb(0):
            return arb(0)
        total = arb(0)
        for n in smooth_ns:
            total += arb(w_fn(n)) * evaluate_phi_n_arb(X_arb, n, prec_bits=prec_bits)
        return total
    finally:
        flint_ctx.prec = saved


def _acb_integral_certified_arb(
    integrand: Callable[[acb, bool], acb],
    a_pt: arb,
    b_pt: arb,
    prec_bits: int = 256,
) -> arb:
    """Certify int_{a_pt}^{b_pt} integrand(z) dz in FLINT ball arithmetic at working
    precision `prec_bits + 32` (defaulting `rel_tol` and `abs_tol` to `2^{-(prec_bits+32)}`)
    and round outward to `prec_bits`.
    """
    if a_pt == b_pt:
        return arb(0)
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits + 32
        res = acb.integral(
            integrand,
            acb(a_pt),
            acb(b_pt),
            eval_limit=500000,
        ).real
        flint_ctx.prec = prec_bits
        return +res
    finally:
        flint_ctx.prec = saved


def _G_shifted_acb(
    z: acb, L: int, m_shift: int, w_vals: Sequence[int], analytic: bool = False
) -> acb:
    """Evaluate G_{a,L}^{[m]}(z) = sum_{1 <= q <= L} a(q) q^{-3} (log(z/q))^m exp(-z^2/q^2) so Q = z^{5/2} G."""
    if L <= 0:
        return acb(0)
    s = acb(0)
    z2 = z * z
    for q in range(1, L + 1):
        q_c = acb(q)
        term = acb(w_vals[q]) * (q_c ** (-3)) * (-z2 / (q_c * q_c)).exp()
        if m_shift > 0:
            term = term * ((z / q_c).log(analytic=analytic) ** m_shift)
        s += term
    return s


def evaluate_E_L_window_arb(
    W_low: Union[int, Fraction, arb],
    W_high: Union[int, Fraction, arb],
    L: int,
    m_shift: int = 0,
    log_denom_power: int = 0,
    mode: str = "liouville",
    prec_bits: int = 256,
) -> arb:
    """Certify int_{W_low}^{W_high} (Q_{a,L}^{[m]}(X))^2 / (X * (log X)^{log_denom_power}) dX via acb.integral."""
    w_fn = _weight_fn_for_mode(mode)
    w_vals = [0] + [w_fn(q) for q in range(1, L + 1)]
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits + 32
        if L <= 0:
            return arb(0)
        a_pt = W_low if isinstance(W_low, arb) else _frac_to_arb(W_low)
        b_pt = W_high if isinstance(W_high, arb) else _frac_to_arb(W_high)
        if log_denom_power > 0 and not bool(a_pt > arb(1)):
            raise ValueError("log_denom_power > 0 requires W_low > 1 to avoid the pole at X = 1")

        def _integrand(z: acb, _analytic: bool) -> acb:
            g_val = _G_shifted_acb(z, L, m_shift, w_vals, analytic=_analytic)
            num = (z ** 4) * (g_val * g_val)
            if log_denom_power > 0:
                return num / (z.log(analytic=_analytic) ** log_denom_power)
            return num

        return _acb_integral_certified_arb(_integrand, a_pt, b_pt, prec_bits=prec_bits)
    finally:
        flint_ctx.prec = saved


def evaluate_E_L_scale_arb(
    W_val: Union[int, Fraction, arb],
    L: int,
    m_shift: int = 0,
    log_denom_power: int = 0,
    mode: str = "liouville",
    prec_bits: int = 256,
) -> arb:
    """Certify int_W^{tau*W} (Q_{a,L}^{[m]}(X))^2 / (X * (log X)^{log_denom_power}) dX."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        W_arb = W_val if isinstance(W_val, arb) else _frac_to_arb(W_val)
        return evaluate_E_L_window_arb(
            W_arb,
            _tau_arb() * W_arb,
            L=L,
            m_shift=m_shift,
            log_denom_power=log_denom_power,
            mode=mode,
            prec_bits=prec_bits,
        )
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 2. Section 1 & 2: Opening Repairs, Monotone Envelope, & Abstract Bootstrap
# ---------------------------------------------------------------------------


def _ceil_nth_root_exact_rational(num_pow: int, den_pow: int, root_k: int) -> int:
    """Compute ceil((num_pow / den_pow)^{1/root_k}) using strictly integer powers (zero floats)."""
    if num_pow <= 0 or den_pow <= 0 or root_k < 1:
        raise ValueError("Positive integers required")
    lo = 0
    hi = 1
    while (hi ** root_k) * den_pow < num_pow:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if (mid ** root_k) * den_pow >= num_pow:
            hi = mid
        else:
            lo = mid
    return hi


def exact_U0_T_pair_for_rational_Y(Y_frac: Union[int, Fraction]) -> Tuple[int, int]:
    """Exact integer-power evaluation of (U_0(Y), T(Y)) = (ceil(2 Y^{5/8}), ceil(Y^{5/4})) for rational Y > 0."""
    if isinstance(Y_frac, bool) or not isinstance(Y_frac, (int, Fraction)):
        raise TypeError(
            f"exact_U0_T_pair_for_rational_Y requires exact int or Fraction (no float/bool), got {Y_frac!r}"
        )
    f_val = Fraction(Y_frac)
    p = int(f_val.numerator)
    q = int(f_val.denominator)
    if p <= 0 or q <= 0:
        raise ValueError("Y_frac must be positive")
    # U_0(Y) = ceil((2^8 * p^5 / q^5)^{1/8}), T(Y) = ceil((p^5 / q^5)^{1/4})
    u0 = _ceil_nth_root_exact_rational((2 ** 8) * (p ** 5), q ** 5, 8)
    t_cut = _ceil_nth_root_exact_rational(p ** 5, q ** 5, 4)
    return (u0, t_cut)


def evaluate_complete_higher_prime_power_sum_arb(
    u: int,
    alpha_frac: Union[int, Fraction],
    prec_bits: int = 256,
) -> arb:
    """Evaluate the COMPLETE k >= 2 higher prime-power sum
    S_{pp,>=2}(u; alpha) := sum_{p <= u} sum_{k >= 2} (2 / k) p^{-k * alpha}
                          = 2 * sum_{p <= u} [-log(1 - p^{-alpha}) - p^{-alpha}]
    for rational alpha > 0 at working precision `prec_bits + 128`, rounded outward to `prec_bits`.
    """
    if not isinstance(u, int) or isinstance(u, bool) or u < 1:
        raise ValueError(f"u must be int >= 1, got {u!r}")
    alpha_f = Fraction(alpha_frac)
    if alpha_f <= 0:
        raise ValueError(f"alpha_frac must be strictly positive, got {alpha_frac!r}")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits + 128
        alpha_arb = _frac_to_arb(alpha_f)
        total = arb(0)
        for p in primes_up_to(u):
            r = arb(p) ** (-alpha_arb)
            total += arb(2) * (-((-r).log1p()) - r)
        flint_ctx.prec = prec_bits
        return +total
    finally:
        flint_ctx.prec = saved


def evaluate_higher_prime_power_series_with_tail_arb(
    u: int,
    alpha_frac: Union[int, Fraction],
    K_trunc: int,
    prec_bits: int = 256,
) -> Dict[str, arb]:
    """Independently evaluate the finite partial sum 2 <= k <= K_trunc - 1 together with the
    proved elementary geometric/log tail bound
        0 < sum_{p <= u} 2 * sum_{k >= K} r_p^k / k <= sum_{p <= u} 2 * r_p^K / [K * (1 - r_p)]
    (r_p = p^{-alpha} in (0, 1)), returning outward-rounded `prec_bits` Arb enclosures for:
    - `partial_sum_below_K`: sum_{p <= u} sum_{k=2}^{K-1} (2/k) p^{-k*alpha} (FINITE sum only),
    - `tail_upper_bound`: sum_{p <= u} 2 * p^{-K*alpha} / [K * (1 - p^{-alpha})],
    - `complete_sum_via_tail`: partial_sum_below_K.union(partial_sum_below_K + tail_upper_bound),
    - `first_omitted_p2_term`: (2 / K) * 2^{-K * alpha} when u >= 2 (else 0).
    """
    if not isinstance(u, int) or isinstance(u, bool) or u < 1:
        raise ValueError(f"u must be int >= 1, got {u!r}")
    if not isinstance(K_trunc, int) or isinstance(K_trunc, bool) or K_trunc < 2:
        raise ValueError(f"K_trunc must be int >= 2, got {K_trunc!r}")
    alpha_f = Fraction(alpha_frac)
    if alpha_f <= 0:
        raise ValueError(f"alpha_frac must be strictly positive, got {alpha_frac!r}")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits + 128
        alpha_arb = _frac_to_arb(alpha_f)
        partial = arb(0)
        tail_ub = arb(0)
        for p in primes_up_to(u):
            r = arb(p) ** (-alpha_arb)
            rk = r * r
            for k in range(2, K_trunc):
                partial += arb(2) * rk / arb(k)
                rk *= r
            # At loop exit, rk == r ** K_trunc
            tail_ub += (arb(2) * rk) / (arb(K_trunc) * (arb(1) - r))
        complete_encl = partial.union(partial + tail_ub)
        omitted_p2 = (
            (arb(2) * (arb(2) ** (-arb(K_trunc) * alpha_arb))) / arb(K_trunc)
            if u >= 2
            else arb(0)
        )
        flint_ctx.prec = prec_bits
        return {
            "partial_sum_below_K": +partial,
            "tail_upper_bound": +tail_ub,
            "complete_sum_via_tail": +complete_encl,
            "first_omitted_p2_term": +omitted_p2,
        }
    finally:
        flint_ctx.prec = saved


def verify_section_1_and_2_baseline_and_envelope(prec_bits: int = 256) -> Dict[str, Any]:
    """Verify TC-056R2/TC-057R opening repairs, complete higher prime-power certificate,
    envelope boundedness across jumps, and repaired Proposition 2.4 localization vs. negative control.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        e_val = arb(1).exp()

        # 1. Exact integer-power verification of [2, 4) small-Y cutoff partition
        # 2^{8/5} = 4^{4/5} <-> 2^8 = 4^4 = 256
        boundary_identity_2_8_5_eq_4_4_5 = (2 ** 8) == (4 ** 4)
        sample_pairs = {
            "Y_eq_2": exact_U0_T_pair_for_rational_Y(Fraction(2, 1)),
            "Y_eq_9_over_4": exact_U0_T_pair_for_rational_Y(Fraction(9, 4)),
            "Y_eq_5_over_2": exact_U0_T_pair_for_rational_Y(Fraction(5, 2)),
            "Y_eq_7_over_2": exact_U0_T_pair_for_rational_Y(Fraction(7, 2)),
            "Y_eq_15_over_4": exact_U0_T_pair_for_rational_Y(Fraction(15, 4)),
            "Y_eq_4": exact_U0_T_pair_for_rational_Y(Fraction(4, 1)),
        }
        expected_pairs = {
            "Y_eq_2": (4, 3),
            "Y_eq_9_over_4": (4, 3),
            "Y_eq_5_over_2": (4, 4),
            "Y_eq_7_over_2": (5, 5),
            "Y_eq_15_over_4": (5, 6),
            "Y_eq_4": (5, 6),
        }
        small_Y_partition_ok = (
            boundary_identity_2_8_5_eq_4_4_5 and sample_pairs == expected_pairs
        )

        # 2. Stieltjes prime-sum remainder (with offset logarithmic integral li_2(t) = int_2^t dv/log v
        #    so li_2(2) = 0 and E_{PNT,2}(2^-) = N_prime(2^-) - li_2(2) = 0) vs. GENUINE COMPLETE
        #    k >= 2 higher prime-power sum at eta = 1/4 (alpha = 1/2 + eta = 3/4; Euler-product regimes
        #    split at eta = 1/2, i.e. alpha = 1, NOT eta = 0).
        alpha_frac = Fraction(3, 4)
        alpha = arb(3) / arb(4)
        u_test = 1000
        prime_sum_u = arb(0)
        for p in primes_up_to(u_test):
            prime_sum_u += arb(p) ** (-alpha)

        # Genuine complete k >= 2 sum: 2 * sum_{p <= 1000} [-log(1 - p^{-3/4}) - p^{-3/4}]
        higher_pp_sum_u = evaluate_complete_higher_prime_power_sum_arb(
            u_test, alpha_frac, prec_bits=prec_bits
        )
        # Independent series-plus-proved-tail checks at K = 40 and K = 160
        check_K40 = evaluate_higher_prime_power_series_with_tail_arb(
            u_test, alpha_frac, K_trunc=40, prec_bits=prec_bits
        )
        check_K160 = evaluate_higher_prime_power_series_with_tail_arb(
            u_test, alpha_frac, K_trunc=160, prec_bits=prec_bits
        )
        # Exact rational witness for first omitted term at p = 2, k = 40:
        # 2 / (40 * 2^{30}) = 1 / (20 * 2^{30}) = 1 / 21474836480 > 4.65e-11
        exact_omitted_p2_k40_frac = Fraction(1, 20 * (2 ** 30))
        exact_omitted_p2_k40_arb = _frac_to_arb(exact_omitted_p2_k40_frac)
        omitted_tail_actual_K40 = higher_pp_sum_u - check_K40["partial_sum_below_K"]
        consistency_diff_K160 = higher_pp_sum_u - check_K160["complete_sum_via_tail"]

        stieltjes_main_int = _acb_integral_certified_arb(
            lambda z, _analytic: (
                z.pow(-acb(alpha), analytic=_analytic) / z.log(analytic=_analytic)
            ),
            arb(2),
            arb(u_test),
            prec_bits=prec_bits,
        )
        stieltjes_diff = prime_sum_u - stieltjes_main_int
        higher_pp_analytic_cap = (acb(arb(3) / arb(2)).zeta().real - arb(1)) / (
            arb(1) - arb(2) ** (-alpha)
        )
        higher_pp_margin = higher_pp_analytic_cap - higher_pp_sum_u
        higher_pp_ok = bool(
            higher_pp_margin > arb(0)
            and exact_omitted_p2_k40_arb > arb("4.65e-11")
            and omitted_tail_actual_K40 > exact_omitted_p2_k40_arb
            and omitted_tail_actual_K40 <= check_K40["tail_upper_bound"]
            and higher_pp_sum_u.overlaps(check_K40["complete_sum_via_tail"])
            and higher_pp_sum_u.overlaps(check_K160["complete_sum_via_tail"])
            and arb(0) in consistency_diff_K160
            and check_K160["tail_upper_bound"] < arb("1e-36")
        )

        # U-product logarithmic slack at delta = 1/2, c = delta^2 / 32 = 1 / 128
        delta_test = arb(1) / arb(2)
        c_log = (delta_test * delta_test) / arb(32)
        log_coeff_2_sqrt_c = arb(2) * c_log.sqrt()
        log_slack_margin = (delta_test / arb(2)) - log_coeff_2_sqrt_c
        log_slack_ok = bool(log_slack_margin > arb(0))

        # 3. Monotone envelope F(Y) local boundedness & certified cutoff jump at Z_0 = 2^{4/5}
        M_1 = arb(1) / arb(2) + arb(2) * ((arb(3) / (arb(2) * e_val)) ** (arb(3) / arb(2)))
        M_lin = (tau - arb(1)) * (M_1 * M_1)
        Z_jump = arb(2) ** (arb(4) / arb(5))
        E_2_at_jump = evaluate_E_L_scale_arb(Z_jump, L=2, mode="liouville", prec_bits=prec_bits)
        E_3_at_jump = evaluate_E_L_scale_arb(Z_jump, L=3, mode="liouville", prec_bits=prec_bits)
        jump_gap_abs = abs(E_3_at_jump - E_2_at_jump)
        jump_certified_nonzero = bool(jump_gap_abs > arb("1e-3"))
        envelope_bound_margin_jump = M_lin * Z_jump - E_3_at_jump
        envelope_bound_ok = bool(
            E_2_at_jump > arb(0)
            and E_3_at_jump > arb(0)
            and envelope_bound_margin_jump > arb(0)
            and jump_certified_nonzero
        )

        # 4. E-to-F smaller-scale monotonicity derivative factor at Z = e^4:
        # d/dZ log(Z / (log Z log log Z)^2) = (1/Z) * (1 - 2/log Z - 2/(log Z log log Z))
        Z_mono = arb(4).exp()
        lg_Z = Z_mono.log()
        lglg_Z = lg_Z.log()
        mono_factor_e4 = arb(1) - arb(2) / lg_Z - arb(2) / (lg_Z * lglg_Z)
        mono_e4_ok = bool(mono_factor_e4 > arb("0.1"))

        # 5. Abstract bootstrap witness with B_eta = 10 > 1 (showing B_eta < 1 is NOT needed)
        eta_w = arb(1) / arb(8)
        eps_w = arb(1) / arb(4)
        B_eta_w = arb(10)
        Y_star_log = arb(4096)
        U_at_Y_star = ((eta_w * eta_w) / arb(32)) * (
            (Y_star_log * Y_star_log.log()) ** 2
        )
        contraction_factor_B_gt_1 = B_eta_w * (U_at_Y_star ** (-eps_w))
        contraction_margin_half = arb("0.5") - contraction_factor_B_gt_1
        bootstrap_B_gt_1_ok = bool(
            U_at_Y_star > arb(2) and contraction_margin_half > arb(0)
        )

        # 6. Repaired Proposition 2.4 coefficient-mass localization vs. concentration negative control:
        # Total mass B_0*(log Y)^b (b = 1) on d >= U(Y) = (log Y)^2 (a = 2) gives ONLY an UPPER bound
        # Theta_sigma(Y) <= B_0*(log Y)^b * U(Y)^{-sigma}.
        # - Localized lower witness: if mass c_0*(log Y) (c_0 = 1) is localized on U(Y) <= d <= 2*U(Y)
        #   (kappa = 2), then at Y = exp(100), sigma = 1/4 < b/a = 1/2:
        #   Theta_{1/4}(Y) >= (log Y) * (2 * (log Y)^2)^{-1/4} = 10 * 2^{-1/4} > 8.4 > 1/2 (fails contraction),
        #   whereas at sigma = 3/4 > 1/2, the total-mass upper bound gives 100 * 100^{-3/2} = 1/10 < 1/2.
        # - Concentration negative control: the SAME total mass B_0*(log Y) = 100 concentrated at
        #   d_top = floor(exp(100)) >= exp(100)/2 has homogeneous factor at sigma = 1/4 < 1/2 bounded by
        #   100 * (exp(100)/2)^{-1/4} = 100 * 2^{1/4} * exp(-25) < 2e-9 << 1/2!
        logY_pen = arb(100)
        theta_subcrit_quarter = logY_pen * ((logY_pen ** 2) ** (-arb("0.25")))
        theta_localized_kappa2_lb_quarter = logY_pen * (
            (arb(2) * (logY_pen ** 2)) ** (-arb("0.25"))
        )
        theta_supercrit_three_quarters = logY_pen * ((logY_pen ** 2) ** (-arb("0.75")))
        theta_concentrated_at_floor_Y_ub_quarter = logY_pen * (
            (logY_pen.exp() / arb(2)) ** (-arb("0.25"))
        )
        penalty_barrier_ok = bool(
            theta_subcrit_quarter > arb(1)
            and theta_localized_kappa2_lb_quarter > arb(8)
            and arb("0.5") - theta_supercrit_three_quarters > arb(0)
            and theta_concentrated_at_floor_Y_ub_quarter < arb("1e-8")
        )

        all_ok = bool(
            small_Y_partition_ok
            and higher_pp_ok
            and log_slack_ok
            and envelope_bound_ok
            and mono_e4_ok
            and bootstrap_B_gt_1_ok
            and penalty_barrier_ok
        )
        return {
            "small_Y_partition_2_to_4": {
                "boundary_2_pow_8_5_eq_4_pow_4_5": boundary_identity_2_8_5_eq_4_4_5,
                "sample_U0_T_pairs": {k: list(v) for k, v in sample_pairs.items()},
                "small_Y_partition_verified": small_Y_partition_ok,
            },
            "stieltjes_vs_higher_prime_power_tail_u1000": {
                "u": u_test,
                "alpha": "3/4",
                "euler_product_regime_split_note": "alpha = 1/2 + eta splits at eta = 1/2 (alpha = 1): 0 < eta < 1/2, eta = 1/2, 1/2 < eta < 1",
                "li_normalization_note": "li_2(t) := int_2^t dv/log v satisfies li_2(2) = 0 and E_{PNT,2}(2^-) = N_prime(2^-) - li_2(2) = 0 (where N_prime(t) = #{p <= t : p prime})",
                "prime_sum_u": serialize_arb_certified(prime_sum_u),
                "stieltjes_main_integral": serialize_arb_certified(stieltjes_main_int),
                "stieltjes_remainder_diff": serialize_arb_certified(stieltjes_diff),
                "higher_prime_power_sum": serialize_arb_certified(higher_pp_sum_u),
                "higher_prime_power_analytic_cap": serialize_arb_certified(higher_pp_analytic_cap),
                "higher_prime_power_margin": serialize_arb_certified(higher_pp_margin),
                "finite_partial_sum_2_to_39_only": serialize_arb_certified(
                    check_K40["partial_sum_below_K"]
                ),
                "proved_tail_upper_bound_K40": serialize_arb_certified(
                    check_K40["tail_upper_bound"]
                ),
                "series_plus_proved_tail_enclosure_K40": serialize_arb_certified(
                    check_K40["complete_sum_via_tail"]
                ),
                "exact_omitted_p2_k40_term_fraction": f"{exact_omitted_p2_k40_frac.numerator}/{exact_omitted_p2_k40_frac.denominator}",
                "exact_omitted_p2_k40_term": serialize_arb_certified(
                    exact_omitted_p2_k40_arb
                ),
                "actual_omitted_tail_above_K39": serialize_arb_certified(
                    omitted_tail_actual_K40
                ),
                "proved_tail_upper_bound_K160": serialize_arb_certified(
                    check_K160["tail_upper_bound"]
                ),
                "series_plus_proved_tail_enclosure_K160": serialize_arb_certified(
                    check_K160["complete_sum_via_tail"]
                ),
                "u_product_log_coeff_at_delta_half": serialize_arb_certified(log_coeff_2_sqrt_c),
                "u_product_log_slack_margin": serialize_arb_certified(log_slack_margin),
            },
            "monotone_envelope_local_boundedness": {
                "M_1": serialize_arb_certified(M_1),
                "M_lin": serialize_arb_certified(M_lin),
                "Z_jump_2_pow_4_5": serialize_arb_certified(Z_jump),
                "E_2_at_Z_jump": serialize_arb_certified(E_2_at_jump),
                "E_3_at_Z_jump": serialize_arb_certified(E_3_at_jump),
                "jump_gap_abs": serialize_arb_certified(jump_gap_abs),
                "envelope_upper_bound_margin_at_jump": serialize_arb_certified(
                    envelope_bound_margin_jump
                ),
                "jump_certified_nonzero": jump_certified_nonzero,
            },
            "conditional_bootstrap_and_penalty_barrier": {
                "scope_label": "CONDITIONAL_ON_RECURSION",
                "smaller_scale_monotonicity_factor_at_exp4": serialize_arb_certified(
                    mono_factor_e4
                ),
                "B_eta_10_U_at_exp4096": serialize_arb_certified(U_at_Y_star),
                "B_eta_10_contraction_factor": serialize_arb_certified(
                    contraction_factor_B_gt_1
                ),
                "B_eta_10_margin_below_half": serialize_arb_certified(
                    contraction_margin_half
                ),
                "penalty_subcritical_sigma_quarter_at_exp100": serialize_arb_certified(
                    theta_subcrit_quarter
                ),
                "penalty_localized_kappa2_lower_bound_quarter_at_exp100": serialize_arb_certified(
                    theta_localized_kappa2_lb_quarter
                ),
                "penalty_supercritical_sigma_three_quarters_at_exp100": serialize_arb_certified(
                    theta_supercrit_three_quarters
                ),
                "concentration_negative_control_floor_Y_upper_bound_quarter_at_exp100": serialize_arb_certified(
                    theta_concentrated_at_floor_Y_ub_quarter
                ),
            },
            "all_section_1_and_2_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 3. Section 3: Route A — General Moebius-Rough Prime-Filtration Descent
# ---------------------------------------------------------------------------


def verify_section_3_route_a_moebius_rough_descent(prec_bits: int = 256) -> Dict[str, Any]:
    """Verify Route A exact identity across sub-sqrt(T) and super-sqrt(T) regimes, a_2 contrast, and CS obstruction."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        identity_cases = [
            ("U2_T6_liouville", 2, 6, Fraction(5, 2), "liouville"),
            ("U3_T30_liouville", 3, 30, Fraction(12, 1), "liouville"),
            ("U5_T431_Y128_liouville", 5, 431, Fraction(128, 1), "liouville"),
            ("U42_T431_Y128_super_sqrt_liouville", 42, 431, Fraction(128, 1), "liouville"),
            ("U3_T15_a2_control", 3, 15, Fraction(6, 1), "a2"),
            ("U5_T431_Y128_a2_control", 5, 431, Fraction(128, 1), "a2"),
        ]
        case_rows: List[Dict[str, Any]] = []
        all_id_ok = True
        for label, U, T, X_frac, mode in identity_cases:
            w_fn = _weight_fn_for_mode(mode)
            X_arb = _frac_to_arb(X_frac)
            q_lhs = evaluate_Q_shifted_finite_arb(X_arb, L=T, m_shift=0, mode=mode, prec_bits=prec_bits)
            s_smooth = evaluate_Q_smooth_below_U_arb(X_arb, U=U, T=T, mode=mode, prec_bits=prec_bits)
            divisors_d = rough_squarefree_divisors_band(U, T)
            rough_sum = arb(0)
            for d in divisors_d:
                coeff = arb(moebius_mu_int(d) * w_fn(d)) / arb(d).sqrt()
                q_sub = evaluate_Q_shifted_finite_arb(
                    X_arb / arb(d), L=T // d, m_shift=0, mode=mode, prec_bits=prec_bits
                )
                rough_sum += coeff * q_sub
            q_rhs = s_smooth - rough_sum
            residual = q_lhs - q_rhs
            ok = bool( arb(0) in residual and abs(residual) < arb("1e-68") )
            all_id_ok = all_id_ok and ok
            case_rows.append(
                {
                    "label": label,
                    "U": U,
                    "T": T,
                    "X": str(X_frac),
                    "mode": mode,
                    "rough_divisor_count": len(divisors_d),
                    "max_omega_in_rough_band": max(
                        (
                            sum(1 for p in primes_up_to(d) if d % p == 0)
                            for d in divisors_d
                        ),
                        default=0,
                    ),
                    "includes_three_prime_385": (385 in divisors_d),
                    "Q_lhs": serialize_arb_certified(q_lhs),
                    "S_smooth_below_U": serialize_arb_certified(s_smooth),
                    "rough_descent_sum": serialize_arb_certified(rough_sum),
                    "residual_lhs_minus_rhs": serialize_arb_certified(residual),
                    "identity_enclosed_at_zero": ok,
                }
            )

        # Verify super-sqrt(T) divisor set equality at U = 42, T = 431 (42^2 = 1764 > 431)
        super_sqrt_eq_primes = rough_squarefree_divisors_band(42, 431) == tuple(
            p for p in primes_up_to(431) if p >= 42
        )

        # Negative control: applying Liouville's uniform -1/sqrt(d) coefficient to a_2 at (U = 3, T = 15, X = 6)
        # fails because mu(3)*a_2(3) = -1 whereas mu(15)*a_2(15) = +1 (and prime terms flip sign!).
        X6 = arb(6)
        q_a2_15 = evaluate_Q_shifted_finite_arb(X6, L=15, m_shift=0, mode="a2", prec_bits=prec_bits)
        s_a2_3_15 = evaluate_Q_smooth_below_U_arb(X6, U=3, T=15, mode="a2", prec_bits=prec_bits)
        wrong_liouville_rough_a2 = arb(0)
        for d in rough_squarefree_divisors_band(3, 15):
            wrong_liouville_rough_a2 += (arb(1) / arb(d).sqrt()) * evaluate_Q_shifted_finite_arb(
                X6 / arb(d), L=15 // d, m_shift=0, mode="a2", prec_bits=prec_bits
            )
        wrong_a2_discrepancy = abs(q_a2_15 - (s_a2_3_15 - wrong_liouville_rough_a2))
        a2_falsifies_uniform_sign = bool(wrong_a2_discrepancy > arb("0.1"))

        # Optimal Cauchy-Schwarz homogeneous multiplier M_{A,sigma}(Y) = (sum_{d in R_{[U,T(Y)]}} d^{-(1+sigma)/2})^2
        # for the specified Cauchy-Schwarz majorant (distinguished from the actual signed rough-divisor sum).
        # Its PRIME SUBSET gives the proved lower bound:
        #   M_{A,sigma}(Y) >= M_{A,sigma}^{prime}(Y) := (sum_{U <= p <= T(Y)} p^{-(1+sigma)/2})^2
        #                  >>_sigma T(Y)^{1-sigma} / (log T(Y))^2 -> infty
        # for polylogarithmic U(Y) and 0 <= sigma < 1 (squarefree rough composites contribute strictly
        # positive excess when an admissible composite exists; note that T >= U^2 alone does not force
        # one, e.g. at U = 5, T = 25 none exists since 5^2 = 25 is not squarefree and the first
        # possible product is 5 * 7 = 35 > 25).
        u5_t25_no_squarefree_rough_composite = (
            rough_squarefree_divisors_band(5, 25)
            == tuple(p for p in primes_up_to(25) if p >= 5)
        )
        sigma_half = arb("0.5")
        cs_rows: List[Dict[str, Any]] = []
        cs_monotone_vals: List[arb] = []
        prime_lb_vals: List[arb] = []
        for Y_int in (32, 128, 512):
            T_int = exact_T_cutoff_ceil_Y_5_4(Y_int)
            divs = rough_squarefree_divisors_band(5, T_int)
            rough_primes = [p for p in primes_up_to(T_int) if p >= 5]
            s_d = arb(0)
            for d in divs:
                s_d += arb(d) ** (-(arb(1) + sigma_half) / arb(2))
            s_p = arb(0)
            for p in rough_primes:
                s_p += arb(p) ** (-(arb(1) + sigma_half) / arb(2))
            mult_homog = s_d * s_d
            prime_subset_lb = s_p * s_p
            cs_monotone_vals.append(mult_homog)
            prime_lb_vals.append(prime_subset_lb)
            cs_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_int,
                    "U": 5,
                    "sigma": "1/2",
                    "rough_divisor_count": len(divs),
                    "rough_prime_count": len(rough_primes),
                    "prime_subset_lower_bound": serialize_arb_certified(prime_subset_lb),
                    "composite_rough_excess_over_prime_subset": serialize_arb_certified(
                        mult_homog - prime_subset_lb
                    ),
                    "optimal_cs_homogeneous_multiplier": serialize_arb_certified(mult_homog),
                    "excess_over_contraction_threshold_half": serialize_arb_certified(
                        mult_homog - arb("0.5")
                    ),
                }
            )
        cs_obstruction_ok = bool(
            prime_lb_vals[0] > arb("0.5")
            and prime_lb_vals[1] > prime_lb_vals[0]
            and prime_lb_vals[2] > prime_lb_vals[1]
            and all(
                bool(m_full > m_pr)
                for m_full, m_pr in zip(cs_monotone_vals, prime_lb_vals)
            )
            and cs_monotone_vals[0] > arb(1)
            and cs_monotone_vals[1] > cs_monotone_vals[0]
            and cs_monotone_vals[2] > cs_monotone_vals[1]
        )

        all_ok = bool(
            all_id_ok
            and super_sqrt_eq_primes
            and u5_t25_no_squarefree_rough_composite
            and a2_falsifies_uniform_sign
            and cs_obstruction_ok
        )
        return {
            "route_a_identity_cases": case_rows,
            "super_sqrt_U42_T431_equals_primes": super_sqrt_eq_primes,
            "u5_t25_no_squarefree_rough_composite": u5_t25_no_squarefree_rough_composite,
            "a2_wrong_uniform_sign_discrepancy_U3_T15": serialize_arb_certified(
                wrong_a2_discrepancy
            ),
            "a2_falsifies_uniform_liouville_sign": a2_falsifies_uniform_sign,
            "optimal_cauchy_schwarz_divergence_sigma_half": cs_rows,
            "all_section_3_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 4. Section 4: Route B (Logarithmic Shift Hierarchy) & Route C (Selberg w_2)
# ---------------------------------------------------------------------------


def selberg_w2_weight_arb(d: int, mode: str = "liouville") -> arb:
    """Compute w_{2,a}(d) = Lambda_a(d)*log(d) + sum_{u*v = d} Lambda_a(u)*Lambda_a(v) for d >= 2."""
    w_fn = _weight_fn_for_mode(mode)
    # Collect prime-power divisors u | d with u >= 2
    total = arb(0)
    pe = prime_power_base_and_exp(d)
    if pe is not None:
        p, k = pe
        lam_d = arb(w_fn(p) ** k) * arb(p).log()
        total += lam_d * arb(d).log()
    # Convolution Lambda_a * Lambda_a(d): either d = p^k (k >= 2) or d = p^a * q^b (distinct primes p, q)
    for u in range(2, d):
        if d % u != 0:
            continue
        v = d // u
        pe_u = prime_power_base_and_exp(u)
        if pe_u is None:
            continue
        pe_v = prime_power_base_and_exp(v)
        if pe_v is None:
            continue
        pu, ku = pe_u
        pv, kv = pe_v
        lu = arb(w_fn(pu) ** ku) * arb(pu).log()
        lv = arb(w_fn(pv) ** kv) * arb(pv).log()
        total += lu * lv
    return total


def von_mangoldt_arb(n: int) -> arb:
    """Ordinary von Mangoldt function Lambda(n) = log p if n = p^k (k >= 1), else 0."""
    pe = prime_power_base_and_exp(n)
    if pe is None:
        return arb(0)
    return arb(pe[0]).log()


def square_mangoldt_B_arb(n: int) -> arb:
    """Square-supported Mangoldt weight B(n) = Lambda(sqrt(n)) if n = m^2 (m >= 2), else 0,
    so Lambda_lambda(n) = -Lambda(n) + 2*B(n).
    """
    if n < 4:
        return arb(0)
    r = math.isqrt(n)
    if r * r != n:
        return arb(0)
    return von_mangoldt_arb(r)


def selberg_w2_via_mangoldt_square_decomposition_arb(n: int) -> arb:
    """Evaluate w_{2,lambda}(n) via the PNT/hyperbola decomposition
    w_{2,lambda}(n) = (-Lambda(n)*log(n) + (Lambda*Lambda)(n))
                    + 2*(B(n)*log(n) - 2*(Lambda*B)(n)) + 4*(B*B)(n).
    """
    if n < 2:
        return arb(0)
    lg_n = arb(n).log()
    lam_n = von_mangoldt_arb(n)
    b_n = square_mangoldt_B_arb(n)
    conv_ll = arb(0)
    conv_lb = arb(0)
    conv_bb = arb(0)
    for u in range(2, n):
        if n % u != 0:
            continue
        v = n // u
        lu = von_mangoldt_arb(u)
        lv = von_mangoldt_arb(v)
        bu = square_mangoldt_B_arb(u)
        bv = square_mangoldt_B_arb(v)
        conv_ll += lu * lv
        conv_lb += lu * bv
        conv_bb += bu * bv
    return (
        (-lam_n * lg_n + conv_ll)
        + arb(2) * (b_n * lg_n - arb(2) * conv_lb)
        + arb(4) * conv_bb
    )


def verify_section_4_route_b_and_c_logarithmic_and_selberg(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify Route B exact prime-power identity, shift hierarchy, narrowed fixed-span non-closure
    (including u^{3+m/2} <= u^{m+5/2} and M approx 2*log Y ratio), and Route C Selberg decomposition
    plus exact discrete Abel summation identity and boundary-term majorant obstruction.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        e_val = arb(1).exp()

        # 1. Route B prime-power identity checks including T = 0 and T = 1, and controls
        route_b_cases = [
            ("T0_liouville", 0, Fraction(4, 1), 0, "liouville"),
            ("T1_liouville", 1, Fraction(4, 1), 0, "liouville"),
            ("T6_liouville", 6, Fraction(5, 2), 0, "liouville"),
            ("T14_liouville", 14, Fraction(8, 1), 0, "liouville"),
            ("T77_m1_liouville", 77, Fraction(32, 1), 1, "liouville"),
            ("T431_Y128_m0_liouville", 431, Fraction(128, 1), 0, "liouville"),
            ("T431_Y128_m2_liouville", 431, Fraction(128, 1), 2, "liouville"),
            ("T14_a2_control", 14, Fraction(8, 1), 0, "a2"),
            ("T14_a357_control", 14, Fraction(8, 1), 0, "a_3_5_7"),
            ("T14_unsigned_control", 14, Fraction(8, 1), 0, "unsigned_1"),
        ]
        rb_rows: List[Dict[str, Any]] = []
        all_rb_ok = True
        for label, T, X_frac, m_sh, mode in route_b_cases:
            w_fn = _weight_fn_for_mode(mode)
            X_arb = _frac_to_arb(X_frac)
            lhs = arb(0)
            for n in range(1, T + 1):
                term = (
                    arb(w_fn(n))
                    * arb(n).log()
                    * evaluate_phi_n_arb(X_arb, n, prec_bits=prec_bits)
                )
                if m_sh > 0:
                    term *= ((X_arb / arb(n)).log()) ** m_sh
                lhs += term
            rhs = arb(0)
            pp_pairs = prime_power_pairs_up_to(T)
            for p, k in pp_pairs:
                pk = p ** k
                coeff = (arb(w_fn(p) ** k) * arb(p).log()) / arb(pk).sqrt()
                q_sub = evaluate_Q_shifted_finite_arb(
                    X_arb / arb(pk), L=T // pk, m_shift=m_sh, mode=mode, prec_bits=prec_bits
                )
                rhs += coeff * q_sub
            res = lhs - rhs
            ok = bool(arb(0) in res and abs(res) < arb("1e-66"))
            if T in (0, 1):
                ok = ok and (lhs == arb(0)) and (rhs == arb(0)) and (len(pp_pairs) == 0)
            all_rb_ok = all_rb_ok and ok
            rb_rows.append(
                {
                    "label": label,
                    "T": T,
                    "X": str(X_frac),
                    "m_shift": m_sh,
                    "mode": mode,
                    "prime_power_pair_count": len(pp_pairs),
                    "lhs": serialize_arb_certified(lhs),
                    "rhs": serialize_arb_certified(rhs),
                    "residual": serialize_arb_certified(res),
                    "identity_verified": ok,
                }
            )

        # Negative control: applying Liouville (-1)^k formula to a_2 at T = 6, X = 4 fails at p = 3, 5
        X4 = arb(4)
        lhs_a2_6 = sum(
            (
                arb(two_adic_parity_a2_int(n))
                * arb(n).log()
                * evaluate_phi_n_arb(X4, n, prec_bits=prec_bits)
                for n in range(1, 7)
            ),
            arb(0),
        )
        wrong_liouville_pp_a2_6 = sum(
            (
                (arb((-1) ** k) * arb(p).log() / arb(p ** k).sqrt())
                * evaluate_Q_shifted_finite_arb(X4 / arb(p ** k), L=6 // (p ** k), m_shift=0, mode="a2", prec_bits=prec_bits)
                for p, k in prime_power_pairs_up_to(6)
            ),
            arb(0),
        )
        wrong_rb_a2_gap = abs(lhs_a2_6 - wrong_liouville_pp_a2_6)
        rb_a2_falsifies_neg1_k = bool(wrong_rb_a2_gap > arb("0.05"))

        # 2. Shift recurrence and M-step telescope at Y = 128, T = 431, X = 128, M = 4
        X128 = arb(128)
        lg128 = X128.log()
        q0_128 = evaluate_Q_shifted_finite_arb(X128, L=431, m_shift=0, mode="liouville", prec_bits=prec_bits)
        tele_sum = arb(0)
        shift_rows: List[Dict[str, Any]] = []
        shift_ok = True
        for m_ord in range(4):
            qm = evaluate_Q_shifted_finite_arb(X128, L=431, m_shift=m_ord, mode="liouville", prec_bits=prec_bits)
            qm1 = evaluate_Q_shifted_finite_arb(X128, L=431, m_shift=m_ord + 1, mode="liouville", prec_bits=prec_bits)
            sig_m = arb(0)
            for p, k in prime_power_pairs_up_to(431):
                pk = p ** k
                sig_m += (
                    (arb((-1) ** k) * arb(p).log() / arb(pk).sqrt())
                    * evaluate_Q_shifted_finite_arb(
                        X128 / arb(pk), L=431 // pk, m_shift=m_ord, mode="liouville", prec_bits=prec_bits
                    )
                )
            rec_res = lg128 * qm - (sig_m + qm1)
            ok_m = bool(arb(0) in rec_res and abs(rec_res) < arb("1e-65"))
            shift_ok = shift_ok and ok_m
            tele_sum += sig_m / (lg128 ** (m_ord + 1))
            shift_rows.append(
                {
                    "m": m_ord,
                    "Q_shifted_m": serialize_arb_certified(qm),
                    "Sigma_pp_m": serialize_arb_certified(sig_m),
                    "Q_shifted_m_plus_1": serialize_arb_certified(qm1),
                    "recurrence_residual": serialize_arb_certified(rec_res),
                }
            )
        q4_128 = evaluate_Q_shifted_finite_arb(X128, L=431, m_shift=4, mode="liouville", prec_bits=prec_bits)
        tele_res = q0_128 - (tele_sum + q4_128 / (lg128 ** 4))
        tele_ok = bool(arb(0) in tele_res and abs(tele_res) < arb("1e-66"))

        # 3. Kernel-shift uniform bound for all X >= 1 (using u^{3+m/2} <= u^{m+5/2} for u >= 1, m >= 1):
        #    m = 0: M_1^{[0]} = 1/2 + 2*(3/(2e))^{3/2}
        #    m >= 1: M_1^{[m]} = 2*((2m+5)/(4e))^{(2m+5)/4} + (m!/2^{m+1})*(1 + 1/e) + 2*(m/(3e))^m
        # Linear independence of {(log w)^m w^{5/2} e^{-w^2}}_{m>=0} rules out exact closure in a FIXED
        # finite linear span. It does NOT rule out Y-dependent growing truncation order M(Y): at
        # M = 2*log Y (illustrated at log Y = 10, M = 20), M! / [2^M * (log Y)^M] ~ sqrt(2*tau*log Y) * Y^{-2}
        # is small, while accumulated prime-power layers and uniform error control remain open.
        growth_rows: List[Dict[str, Any]] = []
        growth_ok = True
        for m_ord in range(0, 7):
            m_fact = arb(math.factorial(m_ord))
            if m_ord == 0:
                M_upper = arb(1) / arb(2) + arb(2) * (
                    (arb(3) / (arb(2) * e_val)) ** (arb(3) / arb(2))
                )
            else:
                t1 = arb(2) * (
                    (arb(2 * m_ord + 5) / (arb(4) * e_val))
                    ** (arb(2 * m_ord + 5) / arb(4))
                )
                t2 = (m_fact / (arb(2) ** (m_ord + 1))) * (arb(1) + arb(1) / e_val)
                t3 = arb(2) * ((arb(m_ord) / (arb(3) * e_val)) ** m_ord)
                M_upper = t1 + t2 + t3
            asymp_lb = m_fact / ((arb(2) ** (m_ord + 1)) * e_val)
            q_uns_norm = abs(
                evaluate_Q_shifted_finite_arb(
                    X128, L=431, m_shift=m_ord, mode="unsigned_1", prec_bits=prec_bits
                )
            ) / X128.sqrt()
            margin = M_upper - q_uns_norm
            growth_ok = growth_ok and bool(margin > arb(0))
            growth_rows.append(
                {
                    "m": m_ord,
                    "M_1_shifted_upper": serialize_arb_certified(M_upper),
                    "unsigned_asymptotic_factorial_lower": serialize_arb_certified(asymp_lb),
                    "sampled_unsigned_norm_X128_T431": serialize_arb_certified(q_uns_norm),
                    "upper_bound_margin_X128": serialize_arb_certified(margin),
                }
            )

        # Certify u^{3+m/2} <= u^{m+5/2} for u >= 1, m >= 1 (since (m+5/2) - (3+m/2) = (m-1)/2 >= 0)
        # and growing-order M = 2*log Y ratio at log Y = 10, M = 20:
        logY_grow = arb(10)
        M_grow = 20
        growing_order_ratio_M20 = arb(math.factorial(M_grow)) / (
            (arb(2) ** M_grow) * (logY_grow ** M_grow)
        )
        stirling_scale_sqrt_tau_2_logY_Y_neg2 = (
            (_tau_arb() * arb(2) * logY_grow).sqrt()
        ) * ((-arb(2) * logY_grow).exp())
        u_step_sample_diff_m2_u3 = (arb(3) ** (arb(2) + arb("2.5"))) - (
            arb(3) ** (arb(3) + arb(1))
        )
        growing_order_check_ok = bool(
            growing_order_ratio_M20 < arb("1e-7")
            and growing_order_ratio_M20 > stirling_scale_sqrt_tau_2_logY_Y_neg2
            and u_step_sample_diff_m2_u3 > arb(0)
        )

        # 4. Route C: Second-order Liouville-Selberg identity, Lambda_lambda = -Lambda + 2*B decomposition,
        #    and exact discrete Abel summation identity + boundary-term majorant obstruction
        rc_rows: List[Dict[str, Any]] = []
        rc_id_ok = True
        for mode in ("liouville", "a2", "unsigned_1"):
            w_fn = _weight_fn_for_mode(mode)
            T_rc = 77
            X_rc = arb(32)
            lhs_rc = sum(
                (
                    arb(w_fn(n))
                    * (arb(n).log() ** 2)
                    * evaluate_phi_n_arb(X_rc, n, prec_bits=prec_bits)
                    for n in range(1, T_rc + 1)
                ),
                arb(0),
            )
            rhs_rc = arb(0)
            for d in range(2, T_rc + 1):
                w2_d = selberg_w2_weight_arb(d, mode=mode)
                rhs_rc += (w2_d / arb(d).sqrt()) * evaluate_Q_shifted_finite_arb(
                    X_rc / arb(d), L=T_rc // d, m_shift=0, mode=mode, prec_bits=prec_bits
                )
            res_rc = lhs_rc - rhs_rc
            ok_rc = bool(arb(0) in res_rc and abs(res_rc) < arb("1e-66"))
            rc_id_ok = rc_id_ok and ok_rc
            rc_rows.append(
                {
                    "mode": mode,
                    "T": T_rc,
                    "X": "32",
                    "lhs": serialize_arb_certified(lhs_rc),
                    "rhs": serialize_arb_certified(rhs_rc),
                    "residual": serialize_arb_certified(res_rc),
                    "identity_verified": ok_rc,
                }
            )

        # Verify w_{2,lambda}(n) == (-Lambda + 2B)*log + (-Lambda + 2B)*(-Lambda + 2B) for all 2 <= n <= 200
        mangoldt_decomp_ok = True
        max_decomp_res = arb(0)
        for n_chk in range(2, 201):
            diff_n = abs(
                selberg_w2_weight_arb(n_chk, "liouville")
                - selberg_w2_via_mangoldt_square_decomposition_arb(n_chk)
            )
            mangoldt_decomp_ok = mangoldt_decomp_ok and bool(
                arb(0)
                in (
                    selberg_w2_weight_arb(n_chk, "liouville")
                    - selberg_w2_via_mangoldt_square_decomposition_arb(n_chk)
                )
                and diff_n < arb("1e-70")
            )
            if bool(diff_n > max_decomp_res):
                max_decomp_res = diff_n

        # Certified Selberg double-pole residue Res_{s=1}(D_lambda''(s)/D_lambda(s)) = 4*zeta'(2)/zeta(2) - 2*gamma_E
        z2_jet = acb_series([acb(2), acb(1)], prec=2).zeta()
        zeta_2 = z2_jet[0].real
        zeta_prime_2 = z2_jet[1].real
        gamma_e = arb.const_euler()
        c_sel_lambda = arb(4) * (zeta_prime_2 / zeta_2) - arb(2) * gamma_e

        # Summatory comparison at u = 400: (1/u)*sum_{d<=u} w_{2,lambda}(d) vs (1/(u log u))*sum_{d<=u} w_{2,a2}(d)
        u_sel = 400
        W2_prefix: Dict[int, arb] = {1: arb(0)}
        running_w2 = arb(0)
        for d_idx in range(2, u_sel + 1):
            running_w2 += selberg_w2_weight_arb(d_idx, "liouville")
            W2_prefix[d_idx] = running_w2
        sum_w2_lam = W2_prefix[u_sel]
        sum_w2_a2 = sum((selberg_w2_weight_arb(d, "a2") for d in range(2, u_sel + 1)), arb(0))
        avg_w2_lam = sum_w2_lam / arb(u_sel)
        avg_w2_a2_over_log = sum_w2_a2 / (arb(u_sel) * arb(u_sel).log())
        selberg_pole_contrast_ok = bool(
            c_sel_lambda < arb("-3.43")
            and avg_w2_lam < arb("-2.0")
            and avg_w2_a2_over_log > arb("1.0")
        )

        # Exact discrete Abel summation identity on 2 <= d <= b = floor(Y) (including boundary W_2(b)*g_b(X)
        # and cutoff jumps L_d -> L_{d+1}) and certified boundary-term lower bound of the specified
        # triangle-inequality majorant: |W_2(b)| * b^{-1/2} * sqrt(E_{L_b}(Y / b)).
        abel_rows: List[Dict[str, Any]] = []
        abel_all_ok = True
        for Y_abel_fr in (Fraction(16, 1), Fraction(32, 1), Fraction(65, 2), Fraction(64, 1)):
            b_floor = int(Y_abel_fr.numerator // Y_abel_fr.denominator)
            _, T_ab = exact_U0_T_pair_for_rational_Y(Y_abel_fr)
            X_ab = _frac_to_arb(Y_abel_fr)

            def _g_d(d_val: int, _T: int = T_ab, _X: arb = X_ab) -> arb:
                return evaluate_Q_shifted_finite_arb(
                    _X / arb(d_val),
                    L=_T // d_val,
                    m_shift=0,
                    mode="liouville",
                    prec_bits=prec_bits,
                ) / arb(d_val).sqrt()

            direct_block = sum((selberg_w2_weight_arb(d, "liouville") * _g_d(d) for d in range(2, b_floor + 1)), arb(0))
            boundary_val = W2_prefix[b_floor] * _g_d(b_floor)
            abel_step_sum = arb(0)
            decomposed_step_sum = arb(0)
            jump_count = 0
            for d in range(2, b_floor):
                L_d = T_ab // d
                L_d1 = T_ab // (d + 1)
                if L_d > L_d1:
                    jump_count += 1
                diff_direct = _g_d(d) - _g_d(d + 1)
                smooth_step = (
                    evaluate_Q_shifted_finite_arb(X_ab / arb(d), L=L_d, m_shift=0, mode="liouville", prec_bits=prec_bits)
                    / arb(d).sqrt()
                    - evaluate_Q_shifted_finite_arb(X_ab / arb(d + 1), L=L_d, m_shift=0, mode="liouville", prec_bits=prec_bits)
                    / arb(d + 1).sqrt()
                )
                cutoff_jump = arb(0)
                for n_jmp in range(L_d1 + 1, L_d + 1):
                    cutoff_jump += arb(liouville_lambda_int(n_jmp)) * evaluate_phi_n_arb(
                        X_ab / arb(d + 1), n_jmp, prec_bits=prec_bits
                    )
                cutoff_jump /= arb(d + 1).sqrt()
                abel_step_sum += W2_prefix[d] * diff_direct
                decomposed_step_sum += W2_prefix[d] * (smooth_step + cutoff_jump)

            abel_res = direct_block - (boundary_val + abel_step_sum)
            step_decomp_res = abel_step_sum - decomposed_step_sum
            L_b = T_ab // b_floor
            W_b_fr = Y_abel_fr / b_floor
            E_Lb_Wb = evaluate_E_L_scale_arb(W_b_fr, L=L_b, mode="liouville", prec_bits=prec_bits)
            boundary_majorant_l2 = (abs(W2_prefix[b_floor]) / arb(b_floor).sqrt()) * E_Lb_Wb.sqrt()
            lg_Y_ab = X_ab.log()
            boundary_majorant_norm_sq = (boundary_majorant_l2 * boundary_majorant_l2) / (
                lg_Y_ab ** 4
            )
            ok_ab = bool(
                arb(0) in abel_res
                and abs(abel_res) < arb("1e-65")
                and arb(0) in step_decomp_res
                and abs(step_decomp_res) < arb("1e-65")
                and jump_count > 0
                and boundary_majorant_l2 > arb("0.2")
                and boundary_majorant_norm_sq > arb("1e-4")
            )
            abel_all_ok = abel_all_ok and ok_ab
            abel_rows.append(
                {
                    "Y": str(Y_abel_fr),
                    "b_floor_Y": b_floor,
                    "T_Y": T_ab,
                    "L_b": L_b,
                    "Y_over_b": str(W_b_fr),
                    "nonzero_cutoff_jump_steps_below_b": jump_count,
                    "W2_at_b": serialize_arb_certified(W2_prefix[b_floor]),
                    "abel_identity_residual": serialize_arb_certified(abel_res),
                    "step_jump_decomposition_residual": serialize_arb_certified(step_decomp_res),
                    "E_Lb_at_Y_over_b": serialize_arb_certified(E_Lb_Wb),
                    "boundary_term_l2_majorant": serialize_arb_certified(boundary_majorant_l2),
                    "normalized_boundary_majorant_sq_over_log4": serialize_arb_certified(
                        boundary_majorant_norm_sq
                    ),
                }
            )

        all_ok = bool(
            all_rb_ok
            and rb_a2_falsifies_neg1_k
            and shift_ok
            and tele_ok
            and growth_ok
            and growing_order_check_ok
            and rc_id_ok
            and mangoldt_decomp_ok
            and selberg_pole_contrast_ok
            and abel_all_ok
        )
        return {
            "route_b_identity_cases": rb_rows,
            "a2_wrong_neg1_k_discrepancy_T6": serialize_arb_certified(wrong_rb_a2_gap),
            "a2_falsifies_liouville_neg1_k_formula": rb_a2_falsifies_neg1_k,
            "shift_hierarchy_Y128_T431": {
                "shift_steps_0_to_3": shift_rows,
                "M4_telescope_residual": serialize_arb_certified(tele_res),
                "telescope_verified": tele_ok,
            },
            "kernel_shift_factorial_growth_table": growth_rows,
            "narrowed_span_closure_and_growing_M_note": {
                "scope_note": "Linear independence of {(log w)^m w^{5/2} e^{-w^2}} rules out exact closure in a fixed finite span; growing M(Y) approx 2*log Y makes M!/[2^M*(log Y)^M] small, while accumulated prime-power layers and uniform bounds remain open.",
                "u_pow_m_plus_5_2_minus_u_pow_3_plus_m_2_at_m2_u3": serialize_arb_certified(
                    u_step_sample_diff_m2_u3
                ),
                "growing_order_ratio_M20_at_logY10": serialize_arb_certified(
                    growing_order_ratio_M20
                ),
                "stirling_reference_sqrt_2tau_logY_Y_neg2_at_logY10": serialize_arb_certified(
                    stirling_scale_sqrt_tau_2_logY_Y_neg2
                ),
            },
            "route_c_selberg_second_order": {
                "dirichlet_series_analytic_domain": "z = x + i*y (x, y in R) with x > 1 for bounded controls |a(n)| <= 1 (finite identities hold for all completely multiplicative a with a(1) = 1)",
                "identity_cases_T77": rc_rows,
                "mangoldt_square_B_decomposition_verified_2_to_200": mangoldt_decomp_ok,
                "mangoldt_square_B_max_abs_residual": serialize_arb_certified(max_decomp_res),
                "c_sel_lambda_residue_4_zetap2_over_zeta2_minus_2_gamma": serialize_arb_certified(
                    c_sel_lambda
                ),
                "u_summatory": u_sel,
                "sum_w2_lambda_over_u": serialize_arb_certified(avg_w2_lam),
                "sum_w2_a2_over_u_log_u": serialize_arb_certified(avg_w2_a2_over_log),
                "abel_summation_procedure_and_boundary_majorant": abel_rows,
            },
            "all_section_4_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 5. Section 5: Cutoff Mismatch, Small-Scale Positivity, & All-L Base Floor
# ---------------------------------------------------------------------------


def verify_section_5_cutoffs_small_scales_and_base_floor(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Certify (Y=9/4, d=2) counterexample, cutoff energy comparison, W<1 positivity, and all-L base floor."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        e_val = arb(1).exp()

        # 1. Counterexample (Y = 9/4, d = 2, W = 9/8): L_2 = 1 < 2 = T(9/8)
        _, T_9_4 = exact_U0_T_pair_for_rational_Y(Fraction(9, 4))
        _, T_9_8 = exact_U0_T_pair_for_rational_Y(Fraction(9, 8))
        L2_9_4 = T_9_4 // 2
        w_9_8 = _frac_to_arb(Fraction(9, 8))
        Q1_9_8 = evaluate_Q_shifted_finite_arb(w_9_8, L=1, m_shift=0, mode="liouville", prec_bits=prec_bits)
        Q2_9_8 = evaluate_Q_shifted_finite_arb(w_9_8, L=2, m_shift=0, mode="liouville", prec_bits=prec_bits)
        E1_9_8 = evaluate_E_L_scale_arb(w_9_8, L=1, mode="liouville", prec_bits=prec_bits)
        E2_9_8 = evaluate_E_L_scale_arb(w_9_8, L=2, mode="liouville", prec_bits=prec_bits)
        q_diff_9_8 = Q1_9_8 - Q2_9_8
        e_diff_abs_9_8 = abs(E1_9_8 - E2_9_8)
        counterexample_ok = bool(
            T_9_4 == 3
            and L2_9_4 == 1
            and T_9_8 == 2
            and L2_9_4 < T_9_8
            and q_diff_9_8 > arb(0)
            and e_diff_abs_9_8 > arb("8e-3")
        )

        # 2. Certified scalar cutoff energy bound for all W = Y/d >= 1, d >= 2:
        # Since L_d >= (1/2) W^{5/4} d^{1/4} and T(W) >= W^{5/4}, L_0 := min(L_d, T(W)) satisfies
        # L_0^4 >= (1/16)*max(d, 16?) -> specifically for d >= 16, L_d >= T(W) >= W^{5/4} so L_0 = T(W) >= W^{5/4},
        # while for 2 <= d <= 15, L_0^4 >= (d / 16) W^5.
        # Tail sum_{n > L_0} n^{-3} <= 1 / (2 L_0^2) (wait: for L_0 >= 1, sum_{n >= L_0 + 1} n^{-3} <= int_{L_0}^infty t^{-3} dt = 1 / (2 L_0^2)!),
        # so ||Q_{L_d} - Q_{T(W)}||_{L^2([W, tau W], dX/X)}^2 <= ((tau^5 - 1)/5) W^5 * (1 / (4 L_0^4))
        # = ((tau^5 - 1)/20) * max(16 / d, 1), and by Young (a + b)^2 <= 2 a^2 + 2 b^2:
        # E_{L_d}(W) <= 2 * E_{T(W)}(W) + ((tau^5 - 1)/10) * max(16 / d, 1).
        tau5_minus_1 = (tau ** 5) - arb(1)
        cutoff_cmp_samples = [
            (Fraction(9, 4), 2),
            (Fraction(16, 1), 2),
            (Fraction(16, 1), 3),
            (Fraction(64, 1), 5),
            (Fraction(64, 1), 16),
            (Fraction(128, 1), 2),
            (Fraction(128, 1), 17),
            (Fraction(128, 1), 31),
        ]
        cmp_rows: List[Dict[str, Any]] = []
        cmp_all_ok = True
        for Y_fr, d_int in cutoff_cmp_samples:
            _, T_Y = exact_U0_T_pair_for_rational_Y(Y_fr)
            W_fr = Y_fr / d_int
            _, T_W = exact_U0_T_pair_for_rational_Y(W_fr)
            L_d = T_Y // d_int
            E_Ld = evaluate_E_L_scale_arb(W_fr, L=L_d, mode="liouville", prec_bits=prec_bits)
            E_TW = evaluate_E_L_scale_arb(W_fr, L=T_W, mode="liouville", prec_bits=prec_bits)
            factor_d = arb(16) / arb(d_int) if d_int < 16 else arb(1)
            rhs_bound = arb(2) * E_TW + (tau5_minus_1 / arb(10)) * factor_d
            margin = rhs_bound - E_Ld
            ok_row = bool(margin > arb(0))
            if d_int >= 16:
                ok_row = ok_row and (L_d >= T_W)
            cmp_all_ok = cmp_all_ok and ok_row
            cmp_rows.append(
                {
                    "Y": str(Y_fr),
                    "d": d_int,
                    "W": str(W_fr),
                    "L_d": L_d,
                    "T_W": T_W,
                    "E_Ld_W": serialize_arb_certified(E_Ld),
                    "E_TW_W": serialize_arb_certified(E_TW),
                    "analytic_upper_bound": serialize_arb_certified(rhs_bound),
                    "outward_margin": serialize_arb_certified(margin),
                }
            )

        # 3. Sharp small-scale positivity constant on w in (0, 1]:
        # c_small := 1 + e^{-1} - zeta(3) > 4/25 = 0.16 > 1/24 > 0
        zeta_3 = acb(3).zeta().real
        c_small_sharp = arb(1) + (arb(-1).exp()) - zeta_3
        tau_pow_4 = tau ** 4
        # Certify at Y = 2048 > tau^4 (~1558.545), T(2048) = 13778, prime p = 13001 > tau * 2048 (~12867.96):
        # Here w = X / p <= (tau * 2048) / 13001 < 1 across the ENTIRE window X in [2048, tau * 2048]!
        Y_large = 2048
        T_large = exact_T_cutoff_ceil_Y_5_4(Y_large)
        p_small_scale = 13001
        L_p_large = T_large // p_small_scale  # 13778 // 13001 = 1
        W_p_large = Fraction(Y_large, p_small_scale)
        max_w_on_window = (tau * arb(Y_large)) / arb(p_small_scale)
        E_Lp_small_scale = evaluate_E_L_scale_arb(
            W_p_large, L=L_p_large, mode="liouville", prec_bits=prec_bits
        )
        # Analytic lower bound on E_L(W) when tau * W <= 1:
        # int_W^{tau W} (c_small * X^{5/2})^2 dX/X = c_small^2 * ((tau^5 - 1)/5) * W^5
        W_p_arb = _frac_to_arb(W_p_large)
        E_Lp_positivity_lb = (c_small_sharp * c_small_sharp) * (tau5_minus_1 / arb(5)) * (W_p_arb ** 5)
        small_scale_margin = E_Lp_small_scale - E_Lp_positivity_lb
        small_scale_ok = bool(
            c_small_sharp > arb(4) / arb(25)
            and arb(1) - max_w_on_window > arb(0)
            and E_Lp_positivity_lb > arb(0)
            and small_scale_margin > arb(0)
        )

        # 4. Certified all-L base-scale energy floor on W in [1, 2]:
        # Since [2, tau] subset [W, tau W] for EVERY W in [1, 2], E_L(W) >= I_L := int_2^{tau} Q_{lambda,L}(X)^2 dX/X.
        # For L >= L_0 = 20: on X in [2, tau], |Q_{lambda,L}(X) - Q_{lambda,L_0}(X)| <= X^{5/2} / (2 L_0^2)?
        # Wait: even simpler! By triangle inequality against L_0 = 20:
        # |Q_{lambda,L}(X) - Q_{lambda,20}(X)| <= X^{5/2} * sum_{n=21}^{L} n^{-3} <= X^{5/2} / (2 * 20^2) = X^{5/2} / 800!
        # Hence ||Q_{lambda,L} - Q_{lambda,20}||_{L^2([2,tau], dX/X)} <= sqrt((tau^5 - 32)/5) / 800!
        L0_base = 20
        I_table: Dict[int, arb] = {}
        for L_chk in range(1, L0_base + 1):
            I_table[L_chk] = evaluate_E_L_window_arb(
                2, tau, L=L_chk, mode="liouville", prec_bits=prec_bits
            )
        norm_I20 = I_table[L0_base].sqrt()
        tail_norm_after_20 = (((tau ** 5) - arb(32)) / arb(5)).sqrt() / arb(2 * (L0_base ** 2))
        tail_lb_after_20 = (norm_I20 - tail_norm_after_20) ** 2
        # Canonical W in [1, 2] uses only L in {1, 2, 3}
        m_base_canonical = I_table[1]
        for L_c in (2, 3):
            if bool(I_table[L_c] < m_base_canonical):
                m_base_canonical = I_table[L_c]
        # All-L >= 1 rigorous lower bound: min(I_1.lower(), ..., I_20.lower(), tail_lb_after_20.lower())
        candidates_lower_arb = [
            I_table[L_c].lower() for L_c in range(1, L0_base + 1)
        ] + [tail_lb_after_20.lower()]
        m_all_L_arb = candidates_lower_arb[0]
        for cand_lb in candidates_lower_arb[1:]:
            if bool(cand_lb < m_all_L_arb):
                m_all_L_arb = cand_lb
        base_floor_ok = bool(
            norm_I20 - tail_norm_after_20 > arb("0.2")
            and m_base_canonical > arb("8e-4")
            and m_all_L_arb > arb("8e-4")
        )

        # 5. Scoped linear cutoff replacement audit (Section 5.2 repair):
        # Define SEPARATELY:
        # (i) actual signed aggregate linear cutoff error ||E_{cut,lin}||_{L^2([Y, tau Y], dX/X)}^2,
        # (ii) squared Minkowski sum of individual L^2 cutoff error norms,
        # (iii) squared unsigned analytic majorant (asymp Y / (log Y)^2).
        # State ONLY the proved chain 0 <= (i) <= (ii) <= (iii); do NOT claim a Theta(Y/(log Y)^2)
        # lower bound on the signed aggregate error (actual signed cancellation remains unresolved).
        lin_cut_rows: List[Dict[str, Any]] = []
        lin_cut_all_ok = True
        for Y_lc in (32, 64):
            T_lc = exact_T_cutoff_ceil_Y_5_4(Y_lc)
            Y_lc_arb = arb(Y_lc)
            primes_lc = [p for p in primes_up_to(Y_lc) if p >= 5]
            prime_ranges: List[Tuple[int, int, int, int]] = []
            sum_indiv_norms = arb(0)
            sum_unsigned_maj = arb(0)
            for p_lc in primes_lc:
                L_p = T_lc // p_lc
                _, T_Wp = exact_U0_T_pair_for_rational_Y(Fraction(Y_lc, p_lc))
                lo_n = min(L_p, T_Wp) + 1
                hi_n = max(L_p, T_Wp)
                sgn_p = 1 if L_p >= T_Wp else -1
                prime_ranges.append((p_lc, lo_n, hi_n, sgn_p))
                if lo_n > hi_n:
                    indiv_norm = arb(0)
                else:
                    Wp_arb = Y_lc_arb / arb(p_lc)

                    def _indiv_diff_sq(
                        z: acb,
                        _analytic: bool,
                        _lo: int = lo_n,
                        _hi: int = hi_n,
                    ) -> acb:
                        dg = acb(0)
                        z2 = z * z
                        for n_k in range(_lo, _hi + 1):
                            nc = acb(n_k)
                            dg += (
                                acb(liouville_lambda_int(n_k))
                                * (nc ** (-3))
                                * (-z2 / (nc * nc)).exp()
                            )
                        return (z ** 4) * (dg * dg)

                    indiv_sq = _acb_integral_certified_arb(
                        _indiv_diff_sq,
                        Wp_arb,
                        tau * Wp_arb,
                        prec_bits=prec_bits,
                    )
                    indiv_norm = indiv_sq.sqrt()
                sum_indiv_norms += indiv_norm / arb(p_lc).sqrt()
                maj_factor_p = arb(16) / arb(p_lc) if p_lc < 16 else arb(1)
                indiv_maj = ((tau5_minus_1 / arb(20)) * maj_factor_p).sqrt()
                sum_unsigned_maj += indiv_maj / arb(p_lc).sqrt()

            def _agg_signed_diff_sq(
                z: acb,
                _analytic: bool,
                _pr: Sequence[Tuple[int, int, int, int]] = tuple(prime_ranges),
            ) -> acb:
                tot = acb(0)
                for p_lc, lo_n, hi_n, sgn_p in _pr:
                    if lo_n > hi_n:
                        continue
                    w_z = z / acb(p_lc)
                    w2 = w_z * w_z
                    dg = acb(0)
                    for n_k in range(lo_n, hi_n + 1):
                        nc = acb(n_k)
                        dg += (
                            acb(liouville_lambda_int(n_k))
                            * (nc ** (-3))
                            * (-w2 / (nc * nc)).exp()
                        )
                    tot += acb(sgn_p) * (acb(p_lc) ** (-3)) * dg
                return (z ** 4) * (tot * tot)

            signed_agg_sq = _acb_integral_certified_arb(
                _agg_signed_diff_sq,
                Y_lc_arb,
                tau * Y_lc_arb,
                prec_bits=prec_bits,
            )
            minkowski_sq = sum_indiv_norms * sum_indiv_norms
            unsigned_maj_sq = sum_unsigned_maj * sum_unsigned_maj
            ok_lc = bool(
                minkowski_sq - signed_agg_sq > arb(0)
                and unsigned_maj_sq - minkowski_sq > arb(0)
            )
            lin_cut_all_ok = lin_cut_all_ok and ok_lc
            lin_cut_rows.append(
                {
                    "Y": Y_lc,
                    "U": 5,
                    "T_Y": T_lc,
                    "actual_signed_aggregate_error_l2_sq": serialize_arb_certified(
                        signed_agg_sq
                    ),
                    "minkowski_sum_individual_error_norms_sq": serialize_arb_certified(
                        minkowski_sq
                    ),
                    "unsigned_analytic_majorant_sq": serialize_arb_certified(
                        unsigned_maj_sq
                    ),
                    "margin_minkowski_minus_signed_sq": serialize_arb_certified(
                        minkowski_sq - signed_agg_sq
                    ),
                    "margin_majorant_minus_minkowski_sq": serialize_arb_certified(
                        unsigned_maj_sq - minkowski_sq
                    ),
                }
            )

        all_ok = bool(
            counterexample_ok
            and cmp_all_ok
            and small_scale_ok
            and base_floor_ok
            and lin_cut_all_ok
        )
        return {
            "counterexample_Y_9_4_d_2": {
                "Y": "9/4",
                "d": 2,
                "W": "9/8",
                "T_Y": T_9_4,
                "L_2": L2_9_4,
                "T_W": T_9_8,
                "Q_lambda_1_at_9_8": serialize_arb_certified(Q1_9_8),
                "Q_lambda_2_at_9_8": serialize_arb_certified(Q2_9_8),
                "Q1_minus_Q2_at_9_8": serialize_arb_certified(q_diff_9_8),
                "E_1_at_9_8": serialize_arb_certified(E1_9_8),
                "E_2_at_9_8": serialize_arb_certified(E2_9_8),
                "abs_E1_minus_E2": serialize_arb_certified(e_diff_abs_9_8),
                "counterexample_certified": counterexample_ok,
            },
            "cutoff_energy_comparison_samples": cmp_rows,
            "linear_cutoff_replacement_three_quantities": {
                "scope_note": "Separates (i) actual signed aggregate error L^2 norm squared, (ii) squared Minkowski sum of individual error norms, and (iii) squared unsigned analytic majorant (~ Y/(log Y)^2); actual signed cancellation is left unresolved.",
                "samples": lin_cut_rows,
            },
            "small_scale_positivity": {
                "c_small_sharp_1_plus_exp_neg1_minus_zeta3": serialize_arb_certified(
                    c_small_sharp
                ),
                "tau_pow_4_threshold": serialize_arb_certified(tau_pow_4),
                "Y_large": Y_large,
                "T_large": T_large,
                "prime_p": p_small_scale,
                "max_X_over_p_on_window": serialize_arb_certified(max_w_on_window),
                "E_Lp_small_scale": serialize_arb_certified(E_Lp_small_scale),
                "positivity_analytic_lower_bound": serialize_arb_certified(
                    E_Lp_positivity_lb
                ),
                "outward_margin": serialize_arb_certified(small_scale_margin),
            },
            "base_scale_energy_floor_W_in_1_2": {
                "I_1_window_2_to_tau": serialize_arb_certified(I_table[1]),
                "I_2_window_2_to_tau": serialize_arb_certified(I_table[2]),
                "I_3_window_2_to_tau": serialize_arb_certified(I_table[3]),
                "I_20_window_2_to_tau": serialize_arb_certified(I_table[L0_base]),
                "tail_l2_norm_after_L20": serialize_arb_certified(tail_norm_after_20),
                "tail_energy_lower_bound_L_gt_20": serialize_arb_certified(tail_lb_after_20),
                "m_base_canonical_min_1_2_3": serialize_arb_certified(m_base_canonical),
                "m_all_L_rigorous_floor": serialize_arb_certified(m_all_L_arb),
            },
            "all_section_5_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 6. Section 6: Route D — Quadratic Prime-Power Diagonal Contraction & X_pp
# ---------------------------------------------------------------------------


def _evaluate_route_d_totals_arb(
    Y_int: int, mode: str, prec_bits: int = 256
) -> Dict[str, arb]:
    """Evaluate E_T(Y), E_shifted_1(Y), total ||Sigma_pp/log X||^2, weighted diagonal D_tilde, unweighted D_pp, and X_tilde."""
    w_fn = _weight_fn_for_mode(mode)
    T_Y = exact_T_cutoff_ceil_Y_5_4(Y_int)
    pp_pairs = prime_power_pairs_up_to(T_Y)
    w_vals = [0] + [w_fn(q) for q in range(1, T_Y + 1)]
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        Y_arb = arb(Y_int)
        lg_Y = Y_arb.log()

        E_main = evaluate_E_L_scale_arb(Y_int, L=T_Y, m_shift=0, log_denom_power=0, mode=mode, prec_bits=prec_bits)
        E_sh1 = evaluate_E_L_scale_arb(Y_int, L=T_Y, m_shift=1, log_denom_power=2, mode=mode, prec_bits=prec_bits)

        # Total prime-power square integral int_Y^{tau Y} (Sigma_{a,pp}(X) / log X)^2 dX/X
        # using Sigma_{a,pp}(X) = sum_{1<=n<=T} a(n) log(n) phi_n(X)
        log_n_weights = [arb(0)] + [arb(w_vals[n]) * arb(n).log() for n in range(1, T_Y + 1)]

        def _sig_sq_integrand(z: acb, _analytic: bool) -> acb:
            g_val = acb(0)
            z2 = z * z
            for n in range(1, T_Y + 1):
                n_c = acb(n)
                g_val += acb(log_n_weights[n]) * (n_c ** (-3)) * (-z2 / (n_c * n_c)).exp()
            lg_z = z.log(analytic=_analytic)
            return (z ** 4) * (g_val * g_val) / (lg_z * lg_z)

        E_sig_total = _acb_integral_certified_arb(
            _sig_sq_integrand,
            Y_arb,
            tau * Y_arb,
            prec_bits=prec_bits,
        )

        # Weighted diagonal D_tilde and unweighted upper diagonal D_pp (using log X >= log Y)
        D_tilde = arb(0)
        D_pp_unweighted = arb(0)
        D_pp_W_ge_1_canonical = arb(0)
        for p, k in pp_pairs:
            pk = p ** k
            L_pk = T_Y // pk
            lg_p_sq_over_pk = (arb(p).log() ** 2) / arb(pk)
            a_u = Y_arb / arb(pk)
            b_u = (tau * Y_arb) / arb(pk)
            pk_pf = acb(arb(pk) ** arb(-5))

            def _diag_integrand_X(
                z: acb, _analytic: bool, _L: int = L_pk, _pk: int = pk, _pf: acb = pk_pf
            ) -> acb:
                gu = _G_shifted_acb(z / acb(_pk), _L, 0, w_vals, analytic=_analytic)
                lg_z = z.log(analytic=_analytic)
                return (z ** 4) * _pf * (gu * gu) / (lg_z * lg_z)

            int_weighted = _acb_integral_certified_arb(
                _diag_integrand_X,
                Y_arb,
                tau * Y_arb,
                prec_bits=prec_bits,
            )
            int_unweighted = evaluate_E_L_window_arb(
                a_u, b_u, L=L_pk, m_shift=0, log_denom_power=0, mode=mode, prec_bits=prec_bits
            )
            D_tilde += lg_p_sq_over_pk * int_weighted
            D_pp_unweighted += lg_p_sq_over_pk * int_unweighted / (lg_Y * lg_Y)
            if pk <= Y_int:
                _, T_sub = exact_U0_T_pair_for_rational_Y(Fraction(Y_int, pk))
                E_canon = evaluate_E_L_window_arb(
                    a_u, b_u, L=T_sub, m_shift=0, log_denom_power=0, mode=mode, prec_bits=prec_bits
                )
                D_pp_W_ge_1_canonical += lg_p_sq_over_pk * E_canon / (lg_Y * lg_Y)

        X_tilde = E_sig_total - D_tilde
        return {
            "E_main": E_main,
            "E_sh1": E_sh1,
            "E_sig_total": E_sig_total,
            "D_tilde": D_tilde,
            "D_pp_unweighted": D_pp_unweighted,
            "D_pp_W_ge_1_canonical": D_pp_W_ge_1_canonical,
            "X_tilde": X_tilde,
        }
    finally:
        flint_ctx.prec = saved


def verify_section_6_route_d_diagonal_contraction_and_off_diagonal(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Certify Route D unconditional diagonal inequality, all-eps contraction Theta_eps^{diag} -> 0, and X_tilde sign split."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        zeta_3 = acb(3).zeta().real
        lg2 = arb(2).log()
        tau5_minus_1 = (tau ** 5) - arb(1)

        # 1. Explicit analytic constant C_{cut,diag} for all Y >= 2:
        # - On p^k <= Y (W = Y/p^k >= 1): E_{L_{p^k}}(W) <= 2 E(W) + (4*(tau^5 - 1)/5) (since max(16/d, 1) <= 8 for d >= 2).
        #   By elementary Chebyshev factorial bound sum_{p^k <= Y} (log p)/p^k <= 2 log Y (for all Y >= 2),
        #   sum_{p^k <= Y} (log p)^2 / p^k <= (log Y) * sum_{p^k <= Y} (log p)/p^k <= 2 (log Y)^2,
        #   so (1/(log Y)^2) * sum_{p^k <= Y} ((log p)^2/p^k) * (4*(tau^5 - 1)/5) <= 8*(tau^5 - 1)/5.
        # - On Y < p^k <= T(Y) (W = Y/p^k < 1): |Q_L(w)| <= zeta(3) * w^{5/2} => E_L(W) <= zeta(3)^2 * ((tau^5 - 1)/5) * W^5.
        #   And (1/(log Y)^2) * sum_{p^k > Y} ((log p)^2 / p^{6k}) * Y^5 <= (1/(log 2)^2) * int_Y^infty ...?
        #   Even cleaner & sharper for ALL Y >= 2:
        #   For p^k > Y >= 2, p^k >= 3 and W = Y/p^k < 1, so W^5 <= 1 and
        #   (1/(log Y)^2) * sum_{p^k > Y} ((log p)^2 / p^k) * W^5
        #   <= (Y^5 / (log 2)^2) * sum_{n >= 3} (log n)^2 / n^6? Wait: if Y is large, Y^5 * Y^{-5} = O(1)!
        #   Specifically, for p^k > Y: (log(p^k))^2 / p^{6k} <= ((log t)^2 / t^6)|_{t = p^k} since d/dt ((log t)^2 / t^6) < 0 for t > e^{1/3} ~ 1.396!
        #   Split off the single first integer ceil(Y) (or t >= Y):
        #   sum_{n > Y} (log n)^2 / n^6 <= (log(Y + 1))^2 / Y^6 + int_Y^infty (log t)^2 t^{-6} dt!
        #   Even simpler! Compare sum_{p^k > Y} ((log p)^2 / p^k) * (Y / p^k)^5 = Y^5 * sum_{p^k > Y} (log p)^2 / p^{6k}:
        #   For every integer n >= max(3, ceil(Y)), if n = ceil(Y) <= Y + 1, (log n)^2 / n^6 <= (2 log Y)^2 / Y^6 (for Y >= 2),
        #   and for all remaining n > Y + 1, (log n)^2 / n^6 <= int_{n-1}^n (log t)^2 / t^6 dt (since (log t)^2 / t^6 decreases on [2, infty))!
        #   Hence sum_{p^k > Y} (log p)^2 / p^{6k} <= sum_{n >= 3, n > Y} (log n)^2 / n^6
        #   <= (2 log Y)^2 / Y^6 + int_Y^infty (log t)^2 t^{-6} dt
        #   = 4 (log Y)^2 / Y^6 + Y^{-5} * ((log Y)^2 / 5 + 2*(log Y)/25 + 2/125)!
        #   Multiply by Y^5 / (log Y)^2 (with Y >= 2):
        #   <= 4 / Y + 1/5 + 2 / (25 log 2) + 2 / (125 (log 2)^2)
        #   <= 2 + 1/5 + 2 / (25 log 2) + 2 / (125 (log 2)^2)!
        small_tail_factor_cap = (
            arb(2)
            + arb(1) / arb(5)
            + arb(2) / (arb(25) * lg2)
            + arb(2) / (arb(125) * lg2 * lg2)
        )
        C_cut_diag = (arb(8) * tau5_minus_1 / arb(5)) + (
            (zeta_3 * zeta_3) * (tau5_minus_1 / arb(5)) * small_tail_factor_cap
        )

        # 2. Evaluate Route D across scales Y in {8, 16, 32, 64, 128} for Liouville
        #    (finite 5-scale certified observations; also verifies exact outer factor 2 in
        #    E(Y) <= 2*D_tilde(Y) + 2*X_tilde(Y) + 2*E_sh1(Y)).
        liouville_scale_rows: List[Dict[str, Any]] = []
        diag_bound_all_ok = True
        outer_factor_2_all_ok = True
        for Y_int in (8, 16, 32, 64, 128):
            vals = _evaluate_route_d_totals_arb(Y_int, mode="liouville", prec_bits=prec_bits)
            rhs_diag_bound = arb(2) * vals["D_pp_W_ge_1_canonical"] + C_cut_diag
            margin_tilde_le_unw = vals["D_pp_unweighted"] - vals["D_tilde"]
            margin_diag_cap = rhs_diag_bound - vals["D_pp_unweighted"]
            outer_2_rhs = (
                arb(2) * vals["D_tilde"]
                + arb(2) * vals["X_tilde"]
                + arb(2) * vals["E_sh1"]
            )
            margin_outer_2 = outer_2_rhs - vals["E_main"]
            ok_y = bool(margin_tilde_le_unw > arb(0) and margin_diag_cap > arb(0))
            ok_outer2 = bool(margin_outer_2 > arb(0))
            diag_bound_all_ok = diag_bound_all_ok and ok_y
            outer_factor_2_all_ok = outer_factor_2_all_ok and ok_outer2
            liouville_scale_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": exact_T_cutoff_ceil_Y_5_4(Y_int),
                    "E_T_Y": serialize_arb_certified(vals["E_main"]),
                    "E_shifted_1_Y": serialize_arb_certified(vals["E_sh1"]),
                    "E_Sigma_pp_over_log_sq": serialize_arb_certified(vals["E_sig_total"]),
                    "D_tilde_weighted": serialize_arb_certified(vals["D_tilde"]),
                    "D_pp_unweighted": serialize_arb_certified(vals["D_pp_unweighted"]),
                    "X_tilde_off_diagonal": serialize_arb_certified(vals["X_tilde"]),
                    "outer_factor_2_transfer_rhs": serialize_arb_certified(outer_2_rhs),
                    "margin_outer_factor_2_rhs_minus_E": serialize_arb_certified(
                        margin_outer_2
                    ),
                    "analytic_diagonal_bound_rhs": serialize_arb_certified(rhs_diag_bound),
                    "margin_D_pp_minus_D_tilde": serialize_arb_certified(margin_tilde_le_unw),
                    "margin_rhs_minus_D_pp": serialize_arb_certified(margin_diag_cap),
                }
            )

        # 3. Direct pair-by-pair off-diagonal quadrature cross-check at Y = 8, T = 14
        Y_pair_chk = 8
        T_pair_chk = exact_T_cutoff_ceil_Y_5_4(Y_pair_chk)
        pp_8 = prime_power_pairs_up_to(T_pair_chk)
        w_lam_8 = [0] + [liouville_lambda_int(q) for q in range(1, T_pair_chk + 1)]
        Y8_arb = arb(Y_pair_chk)
        pair_sum_8 = arb(0)
        for idx1 in range(len(pp_8)):
            p1, k1 = pp_8[idx1]
            pk1 = p1 ** k1
            L1 = T_pair_chk // pk1
            c1 = (arb((-1) ** k1) * arb(p1).log()) / arb(pk1).sqrt()
            for idx2 in range(idx1 + 1, len(pp_8)):
                p2, k2 = pp_8[idx2]
                pk2 = p2 ** k2
                L2 = T_pair_chk // pk2
                c2 = (arb((-1) ** k2) * arb(p2).log()) / arb(pk2).sqrt()

                pk_prod_pf = acb(arb(pk1 * pk2) ** (arb(-5) / arb(2)))

                def _pair_int(
                    z: acb,
                    _analytic: bool,
                    _pk1: int = pk1,
                    _L1: int = L1,
                    _pk2: int = pk2,
                    _L2: int = L2,
                    _pf: acb = pk_prod_pf,
                ) -> acb:
                    g1 = _G_shifted_acb(z / acb(_pk1), _L1, 0, w_lam_8, analytic=_analytic)
                    g2 = _G_shifted_acb(z / acb(_pk2), _L2, 0, w_lam_8, analytic=_analytic)
                    lg_z = z.log(analytic=_analytic)
                    return (z ** 4) * _pf * (g1 * g2) / (lg_z * lg_z)

                val_12 = _acb_integral_certified_arb(
                    _pair_int,
                    Y8_arb,
                    tau * Y8_arb,
                    prec_bits=prec_bits,
                )
                pair_sum_8 += arb(2) * c1 * c2 * val_12
        vals_8 = _evaluate_route_d_totals_arb(8, mode="liouville", prec_bits=prec_bits)
        pair_consistency_diff_8 = pair_sum_8 - vals_8["X_tilde"]
        pair_consistency_ok = bool(
            arb(0) in pair_consistency_diff_8
            and abs(pair_consistency_diff_8) < arb("1e-62")
        )

        # 4. Parity controls vs Liouville sign split on X_tilde at Y = 32 (T = 77) and Y = 128 (T = 431)
        control_comparison_rows: List[Dict[str, Any]] = []
        liouville_32 = _evaluate_route_d_totals_arb(32, mode="liouville", prec_bits=prec_bits)
        liouville_128 = _evaluate_route_d_totals_arb(128, mode="liouville", prec_bits=prec_bits)
        a2_32 = _evaluate_route_d_totals_arb(32, mode="a2", prec_bits=prec_bits)
        a2_128 = _evaluate_route_d_totals_arb(128, mode="a2", prec_bits=prec_bits)
        a357_32 = _evaluate_route_d_totals_arb(32, mode="a_3_5_7", prec_bits=prec_bits)
        uns_32 = _evaluate_route_d_totals_arb(32, mode="unsigned_1", prec_bits=prec_bits)
        for lbl, y_v, d_v in [
            ("liouville_Y32", 32, liouville_32),
            ("liouville_Y128", 128, liouville_128),
            ("a2_Y32", 32, a2_32),
            ("a2_Y128", 128, a2_128),
            ("a_3_5_7_Y32", 32, a357_32),
            ("unsigned_1_Y32", 32, uns_32),
        ]:
            control_comparison_rows.append(
                {
                    "label": lbl,
                    "Y": y_v,
                    "E_main": serialize_arb_certified(d_v["E_main"]),
                    "D_tilde": serialize_arb_certified(d_v["D_tilde"]),
                    "X_tilde": serialize_arb_certified(d_v["X_tilde"]),
                    "E_sh1": serialize_arb_certified(d_v["E_sh1"]),
                }
            )
        # Liouville X_tilde < 0 (destructive prime-power cancellation) vs unsigned_1 and a_2 at Y = 128 having X_tilde > 0!
        sign_split_ok = bool(
            liouville_32["X_tilde"] < arb(0)
            and liouville_128["X_tilde"] < arb(0)
            and a2_128["X_tilde"] > arb(0)
            and uns_32["X_tilde"] > arb(0)
        )

        # 5. Unconditional all-epsilon contraction factor Theta_eps^{diag}(Y) < 2*zeta''(1+eps)/(log Y)^2 -> 0
        # Using acb_series([1 + eps, 1], prec=3).zeta(): [zeta(s), zeta'(s), zeta''(s)/2] -> zeta''(s) = 2 * jet[2]
        contraction_rows: List[Dict[str, Any]] = []
        contraction_ok = True
        for eps_str, eps_fr, Y_thresh_log in [
            ("1/2", Fraction(1, 2), 16),
            ("1/4", Fraction(1, 4), 32),
            ("1/8", Fraction(1, 8), 64),
        ]:
            eps_arb = _frac_to_arb(eps_fr)
            s_pt = arb(1) + eps_arb
            jet3 = acb_series([acb(s_pt), acb(1)], prec=3).zeta()
            zeta_pp = arb(2) * jet3[2].real  # jet[2] is (1/2!)*zeta''(1+eps)
            lgY_th = arb(Y_thresh_log)
            analytic_cap = (arb(2) * zeta_pp) / (lgY_th * lgY_th)
            # Also evaluate finite Theta_eps^{diag}(128) = (2/(log 128)^2) * sum_{p^k <= 128} (log p)^2 / p^{k*(1+eps)}
            lg128 = arb(128).log()
            finite_theta_128 = arb(0)
            for p, k in prime_power_pairs_up_to(128):
                finite_theta_128 += (arb(p).log() ** 2) / (
                    arb(p ** k) ** (arb(1) + eps_arb)
                )
            finite_theta_128 = arb(2) * finite_theta_128 / (lg128 * lg128)
            cap_128 = (arb(2) * zeta_pp) / (lg128 * lg128)
            ok_c = bool(
                zeta_pp > arb(0)
                and cap_128 - finite_theta_128 > arb(0)
                and arb("0.5") - analytic_cap > arb(0)
            )
            contraction_ok = contraction_ok and ok_c
            contraction_rows.append(
                {
                    "epsilon": eps_str,
                    "zeta_second_deriv_1_plus_eps": serialize_arb_certified(zeta_pp),
                    "Theta_eps_diag_at_Y128": serialize_arb_certified(finite_theta_128),
                    "analytic_cap_at_Y128": serialize_arb_certified(cap_128),
                    "threshold_log_Y": Y_thresh_log,
                    "analytic_cap_at_threshold_below_half": serialize_arb_certified(
                        analytic_cap
                    ),
                    "margin_below_half_at_threshold": serialize_arb_certified(
                        arb("0.5") - analytic_cap
                    ),
                }
            )

        # 6. Conditional same-scale absorption parameter audit (`CONDITIONAL_ON_SIGNED_CORRELATION`, Theorem 26):
        # Preserve exact outer factor 2: E(Y) <= 2*D_tilde(Y) + 2*[X_tilde(Y) + E_sh1(Y)].
        # Under open hypothesis X_tilde(Y) + E_sh1(Y) <= A_eta * Y^eta + theta_eta * F(Y) with theta_eta in [0, 1/2):
        # at eps = 1/4, eta = 1/8, theta_eta = 3/8 (< 1/2), choose q = 7/8 in (2*theta_eta, 1) = (3/4, 1)
        # and log Y_* = 64. Note D_tilde(Y) <= D_pp(Y) <= (2/(log Y)^2) sum_{p^k<=Y} ((log p)^2/p^k) F(Y/p^k) + C_{cut,diag},
        # so 2*D_tilde(Y) contributes homogeneous factor 2*Theta_eps^{diag}(Y) < 4*zeta''(1+eps)/(log Y)^2!
        # Wait: let's track the exact factor 2 carefully:
        # Since D_tilde(Y) <= Theta_eps^{diag,1}(Y) * G_eps(R) * Y^eps + C_{cut,diag} where
        # Theta_eps^{diag}(Y) = (2/(log Y)^2) sum_{p^k<=Y} (log p)^2 / p^{k(1+eps)} < 2*zeta''(1+eps)/(log Y)^2,
        # multiplying by the outer factor 2 in E(Y) <= 2*D_tilde(Y) + 2*(X_tilde(Y) + E_sh1(Y)) gives
        # 2*theta_eta + 2*Theta_eps^{diag}(Y) < 2*theta_eta + 4*zeta''(1+eps)/(log Y)^2!
        eps_abs = arb(1) / arb(4)
        eta_abs = arb(1) / arb(8)
        theta_abs = arb(3) / arb(8)
        q_abs = arb(7) / arb(8)
        logY_star_abs = arb(64)
        jet3_quarter = acb_series([acb(arb(1) + eps_abs), acb(1)], prec=3).zeta()
        zeta_pp_quarter = arb(2) * jet3_quarter[2].real
        Theta_cap_at_Y_star = (arb(2) * zeta_pp_quarter) / (logY_star_abs * logY_star_abs)
        total_homog_cap_at_Y_star = arb(2) * theta_abs + arb(2) * Theta_cap_at_Y_star
        margin_below_q = q_abs - total_homog_cap_at_Y_star
        boundary_theta_half_total = arb(2) * arb("0.5") + arb(2) * Theta_cap_at_Y_star
        absorption_check_ok = bool(
            margin_below_q > arb(0)
            and arb(1) - q_abs > arb(0)
            and boundary_theta_half_total > arb(1)
        )

        all_ok = bool(
            diag_bound_all_ok
            and outer_factor_2_all_ok
            and pair_consistency_ok
            and sign_split_ok
            and contraction_ok
            and absorption_check_ok
        )
        return {
            "C_cut_diag_explicit_constant": serialize_arb_certified(C_cut_diag),
            "liouville_route_d_scale_sweep": liouville_scale_rows,
            "finite_observation_scope_note": "Liouville X_tilde sign changes across Y in {8, 16, 32, 64, 128} and parity-control a_2 values at Y in {32, 128} are certified finite observations at those sampled scales, not asymptotic zero-mean, O(1), or growth theorems.",
            "pair_by_pair_off_diagonal_check_Y8": {
                "pair_sum_X_tilde_Y8": serialize_arb_certified(pair_sum_8),
                "subtraction_X_tilde_Y8": serialize_arb_certified(vals_8["X_tilde"]),
                "difference": serialize_arb_certified(pair_consistency_diff_8),
                "consistency_verified": pair_consistency_ok,
            },
            "parity_control_sign_split": control_comparison_rows,
            "sign_split_liouville_neg_vs_controls_pos": sign_split_ok,
            "all_epsilon_diagonal_contraction_table": contraction_rows,
            "conditional_same_scale_absorption_parameters": {
                "scope_label": "CONDITIONAL_ON_SIGNED_CORRELATION",
                "open_hypothesis": "Sufficient condition (forward implication proved in Lean Theorem 26; converse/equivalence not asserted without a separate shifted-kernel estimate): for every eta > 0 there exist A_eta >= 0, theta_eta in [0, 1/2), and Y_eta >= 2 such that X_tilde_{lambda,pp}(Y) + E_{sh,1}(Y) <= A_eta * Y^eta + theta_eta * F(Y) for all Y >= Y_eta.",
                "sample_epsilon": "1/4",
                "sample_eta": "1/8",
                "sample_theta_eta": "3/8",
                "sample_q": "7/8",
                "sample_log_Y_star": 64,
                "Theta_quarter_cap_at_exp64": serialize_arb_certified(
                    Theta_cap_at_Y_star
                ),
                "two_theta_plus_two_Theta_cap_at_exp64": serialize_arb_certified(
                    total_homog_cap_at_Y_star
                ),
                "contraction_slack_q_minus_homog_cap": serialize_arb_certified(
                    margin_below_q
                ),
                "boundary_theta_half_homog_factor_exceeds_one": serialize_arb_certified(
                    boundary_theta_half_total
                ),
                "absorption_verified": absorption_check_ok,
            },
            "all_section_6_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 7. Review Document Displayed-Enclosure Verification & Artifact Generation
# ---------------------------------------------------------------------------


def verify_tc057_review_displayed_enclosures(
    report: Dict[str, Any],
    review_path: Path = TC_057_REVIEW_DOC_PATH,
) -> Dict[str, Any]:
    """Verify that EVERY displayed interval (`[mid +/- rad]` or `[mid \\pm rad]`) in
    `docs/reviews/TC_057_COUPLED_ARITHMETIC_SCALE_ENERGY_BOOTSTRAP.md` carries an explicit
    `<!-- tc-enclosure: observable="..." params="..." json_path="..." -->` tag, resolves to a
    generated 256-bit Arb ball in `report`, outward-contains that generated ball, and preserves
    strict sign whenever `0` is outside the generated ball.
    """
    text = review_path.read_text(encoding="utf-8")
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
        len(raw_intervals) > 0
        and len(untagged_intervals) == 0
        and len(failed_intervals) == 0
    )
    return {
        "review_path": str(review_path),
        "total_displayed_intervals_found": len(raw_intervals),
        "tagged_and_checked_count": len(checked_rows),
        "untagged_count": len(untagged_intervals),
        "failed_count": len(failed_intervals),
        "untagged_intervals": untagged_intervals,
        "failed_intervals": failed_intervals,
        "all_displayed_intervals_contain_generated_enclosures": all_ok,
    }


def execute_task_tc057_coupled_scale_bootstrap_audit(
    prec_bits: int = 256,
    verify_review_doc: bool = True,
) -> Dict[str, Any]:
    """Execute the complete TASK-TC-057 mathematical, counterexample, and certified 256-bit Arb audit."""
    sec1_2 = verify_section_1_and_2_baseline_and_envelope(prec_bits=prec_bits)
    sec3 = verify_section_3_route_a_moebius_rough_descent(prec_bits=prec_bits)
    sec4 = verify_section_4_route_b_and_c_logarithmic_and_selberg(prec_bits=prec_bits)
    sec5 = verify_section_5_cutoffs_small_scales_and_base_floor(prec_bits=prec_bits)
    sec6 = verify_section_6_route_d_diagonal_contraction_and_off_diagonal(prec_bits=prec_bits)

    assert sec1_2["all_section_1_and_2_checks_pass"] is True
    assert sec3["all_section_3_checks_pass"] is True
    assert sec4["all_section_4_checks_pass"] is True
    assert sec5["all_section_5_checks_pass"] is True
    assert sec6["all_section_6_checks_pass"] is True

    report: Dict[str, Any] = {
        "task_id": TASK_TC_057_ID,
        "repair_task_id": TASK_TC_057R_ID,
        "parent_epic": EPIC_TC_042_ID,
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
        ],
        "prior_merged_main": PRIOR_MERGED_MAIN_TC_053R,
        "tc054r2_merged_main_baseline": TC_054R2_MERGED_MAIN_BASELINE,
        "tc055r2_implementation_commit": TC_055R2_IMPLEMENTATION_COMMIT,
        "tc055r2_reviewed_tip": TC_055R2_REVIEWED_TIP,
        "tc056_implementation_commit": TC_056_IMPLEMENTATION_COMMIT,
        "tc056_reviewed_tip": TC_056_REVIEWED_TIP,
        "tc056r_reviewed_commit": TC_056R_REVIEWED_COMMIT,
        "tc056r2_implementation_commit": TC_056R2_IMPLEMENTATION_COMMIT,
        "tc056r2_reviewed_tip": TC_056R2_REVIEWED_TIP,
        "tc057_implementation_commit": TC_057_IMPLEMENTATION_COMMIT,
        "tc057_reviewed_tip": TC_057_REVIEWED_TIP,
        "branch": "task/tc-057r-tail-certification-obstruction-scope-and-transfer-proof-repair",
        "research_outcome_class": "Outcome B / Scoped Obstruction & Conditional Reduction (unconditional Route D cross-scale diagonal estimate with Theta_eps^{diag}(Y) -> 0, proved conditional same-scale absorption transfer, and precisely scoped majorant/fixed-span obstructions; SUBGATE-TC-043A remains OPEN)",
        "subgate_tc043a_status": "OPEN",
        "rh_proved": False,
        "precision_bits": prec_bits,
        "circle_constant_convention": "tau = 2*pi (sole circle constant)",
        "complex_coordinate_convention": "z = x + i*y (x, y in R; critical line x = 1/2)",
        "section_1_and_2_baseline_and_envelope": sec1_2,
        "section_3_route_a_moebius_rough_descent": sec3,
        "section_4_route_b_and_c_logarithmic_and_selberg": sec4,
        "section_5_cutoffs_small_scales_and_base_floor": sec5,
        "section_6_route_d_diagonal_contraction_and_off_diagonal": sec6,
        "evidence_classification": {
            "1_concrete_lean_theorems": [
                "abstract_polylog_scale_bootstrap_and_weighted_contraction_tc057 (Theorem 21 in formal/RiemannScope/LiouvilleSquareDilation.lean, 0 sorry, 0 custom axiom; CONDITIONAL_ON_RECURSION for the descent step): unconditional local boundedness & monotonicity of monotoneScaleEnvelope without continuity, E-to-F envelope passage, dyadic-height descent without B_eta < 1, weighted multi-scale contraction step, and homogeneous lower-bound obstruction.",
                "general_moebius_rough_prime_filtration_descent_tc057 (Theorem 22): exact general Moebius-rough descent across all U >= 2, uniform Liouville sign mu(d)*lambda(d) = +1 on roughSquarefreeDivisorsBand U T, super-sqrt(T) reduction to primes when T < U^2, and explicit a_2 sign contrast on {3, 15}.",
                "logarithmic_prime_power_descent_and_kernel_shift_tc057 (Theorem 23): exact finite logarithmic prime-power descent at every shift order m >= 0 (including T = 0, 1), Liouville (-1)^k specialization, shift recurrence (log X) Q_T^{[m]} = Sigma_pp^{[m]} + Q_T^{[m+1]}, and M-step telescope.",
                "quadratic_prime_power_diagonal_off_diagonal_decomposition_tc057 (Theorem 24): exact pointwise square decomposition into ((log p)^2 / p^k) Q_{floor(T/p^k)}(X/p^k)^2 diagonal plus pk_1 != pk_2 off-diagonal correlation, and Young domination bound.",
                "inherited_vs_canonical_cutoff_comparison_and_counterexample_tc057 (Theorem 25): exact d >= 16 cutoff ordering T(W) <= floor(T(W*d)/d), all-d >= 2 lower bound (1/2) W^{5/4} d^{1/4} <= floor(T(W*d)/d), explicit (Y = 9/4, d = 2) counterexample L_2 = 1 < 2 = T(9/8) with Q_{lambda,1}(9/8) - Q_{lambda,2}(9/8) > 0, and unconditional small-scale positivity finiteQLambda L w >= (1/24) w^{5/2} > 0 for all L >= 1, w in (0, 1].",
                "conditional_signed_correlation_same_scale_absorption_transfer_tc057r (Theorem 26; CONDITIONAL_ON_SIGNED_CORRELATION): local finiteness and envelope domination of normalizedScaleSupremum E eps R = sup_{1<=Z<=R} E(Z)/Z^eps without continuity or supremum attainment, complete finite-horizon same-scale absorption proof from E(Y) <= 2 D_tilde(Y) + 2 X_tilde(Y) + 2 E_sh1(Y) and X_tilde(Y) + E_sh1(Y) <= A_eta Y^eta + theta_eta F(Y) (theta_eta in [0, 1/2)) to E(Y) <<_eps Y^eps, boundary sharpness at theta = 1/2, and repaired Proposition 2.4 coefficient-mass localization vs. d_top >= Y/2 concentration negative control.",
            ],
            "2_analytic_theorems_proved_outside_lean": [
                "Stieltjes remainder O_eta(1 + u^{1-alpha} exp(-c' sqrt(log u))) for sum_{p<=u} p^{-alpha} (alpha = 1/2 + eta in (1/2, 1), regimes splitting at eta = 1/2, using li_2(t) = int_2^t dv/log v with li_2(2) = 0) distinct from the complete k >= 2 higher prime-power sum 2 sum_{p<=u} [-log(1 - p^{-alpha}) - p^{-alpha}], U-product slack 2*sqrt(c) = delta/(2*sqrt(2)) < delta/2, and exact 4-interval small-Y partition on [2, 4).",
                "Unconditional local boundedness 0 <= E_L(Z) <= (tau - 1) M_1^2 Z and smaller-scale argument monotonicity Z / (log Z log log Z)^2 strictly increasing for Z >= e^4; repaired Proposition 2.4 showing total mass B_0 (log Y)^b on d >= U(Y) = c (log Y)^a is an upper bound on Theta_sigma(Y), requiring quantitative localization on [U(Y), kappa U(Y)] for the lower barrier sigma < b / a (while equality sigma = b / a can contract if the constant < 1, and mass concentrated at floor(Y) gives (log Y)^b floor(Y)^{-sigma} -> 0).",
                "Sharp small-scale positivity Q_{lambda,L}(w) >= (1 + e^{-1} - zeta(3)) w^{5/2} > (4/25) w^{5/2} > (1/24) w^{5/2} on (0, 1] forcing Theta(Y / (log Y)^2) individual-norm squared energy on the W = Y/p < 1 band p in [ceil(tau Y), T(Y)] for Y > tau^4.",
                "All-d >= 2 scalar cutoff energy comparison E_{L_d}(W) <= 2 E(W) + ((tau^5 - 1)/10) max(16/d, 1) (W = Y/d >= 1), proving O(1) quadratic diagonal cutoff replacement cost while bounding the unsigned analytic majorant of linear prime-sum cutoff replacement at asymp Y / (log Y)^2 (leaving actual signed cancellation in the linear aggregate error unresolved).",
                "Linear independence of {(log w)^m w^{5/2} e^{-w^2}}_{m>=0} ruling out exact algebraic closure in any fixed finite linear span, together with uniform bound |Q_T^{[m]}(X)| <= M_1^{[m]} sqrt(X) (via u^{3+m/2} <= u^{m+5/2} on u >= 1, m >= 1) and asymptotic factorial lower bound >= m! / (2^{m+1} e) at fixed m (not ruling out finite vector-energy inequalities, other kernels, or Y-dependent M(Y) approx 2 log Y).",
                "Complete PNT and Dirichlet-hyperbola derivation of sum_{d<=x} w_{2,lambda}(d) = [4*zeta'(2)/zeta(2) - 2*gamma_E] x + O(x exp(-c'' sqrt(log x))) via Lambda_lambda = -Lambda + 2 B (with Dirichlet-series convergence on z = x + i y, x > 1, restricted to bounded controls |a(n)| <= 1), contrasted against +2 x log x + O(x) for parity controls a_S.",
                "Precisely scoped majorant obstructions proved via the certified all-L base-scale energy floor inf_{W in [1,2], L>=1} E_L(W) >= m_{all-L} > 0: Route A prime-subset lower bound M_{A,sigma}(Y) >= (sum_{U<=p<=T(Y)} p^{-(1+sigma)/2})^2 >>_sigma T(Y)^{1-sigma}/(log T(Y))^2 -> infty obstructing the homogeneous Cauchy-Schwarz majorant; Route B Cauchy-Schwarz multiplier divergence >>_sigma Y^{1-sigma}/(log Y)^2; and Route C obstruction of the specified discrete Abel triangle-inequality majorant via its b = floor(Y) boundary term |W_2(b)| b^{-1/2} sqrt(E_{L_b}(Y/b)) >> sqrt(Y) (normalized square >> Y/(log Y)^4), without lower-bounding the signed sums or ruling out compensated formulations.",
                "Unconditional Route D cross-scale prime-power diagonal inequality D_tilde_{lambda,pp}(Y) <= D_{lambda,pp}(Y) <= (2/(log Y)^2) sum_{p^k<=Y} ((log p)^2/p^k) F(Y/p^k) + C_{cut,diag} (all Y >= 2) whose homogeneous contraction factor satisfies Theta_eps^{diag}(Y) < 2*zeta''(1+eps)/(log Y)^2 -> 0 (not claiming D_tilde_{lambda,pp}(Y) itself tends to 0).",
            ],
            "3_conditional_implications_open_hypothesis": [
                "Polylogarithmic bootstrap implication (Theorem 21, CONDITIONAL_ON_RECURSION): IF F(Y) <= A_eta Y^eta + B_eta F(Y/U_eta(Y)) holds for all Y >= Y_eta with U_eta(Y) = c_eta (log Y log log Y)^2, THEN E(Y) <= F(Y) <<_eps Y^eps for every eps > 0.",
                "Route D same-scale absorption transfer (Theorem 26, CONDITIONAL_ON_SIGNED_CORRELATION): sufficient condition (forward implication to subpower energy proved; equivalence not asserted without separately proving the converse shifted-kernel estimate) — IF for every eta > 0 there exist A_eta >= 0, theta_eta in [0, 1/2), and Y_eta >= 2 such that X_tilde_{lambda,pp}(Y) + E_{sh,1}(Y) <= A_eta Y^eta + theta_eta F(Y) for all Y >= Y_eta, THEN combined with E(Y) <= 2 D_tilde_{lambda,pp}(Y) + 2 X_tilde_{lambda,pp}(Y) + 2 E_{sh,1}(Y) and Theta_eps^{diag}(Y) -> 0, finite-horizon absorption on G_eps(R) = sup_{1<=Z<=R} E(Z)/Z^eps proves E(Y) <<_eps Y^eps uniformly for all Y >= 1.",
            ],
            "4_certified_finite_computations": [
                (
                    "Complete k >= 2 higher prime-power enclosure "
                    "2 sum_{p<=1000} [-log(1 - p^{-3/4}) - p^{-3/4}] = "
                    f"{sec1_2['stieltjes_vs_higher_prime_power_tail_u1000']['higher_prime_power_sum']['arb_ball_str']} "
                    "cross-checked against K = 40 and K = 160 series-plus-proved-tail enclosures, strictly exceeding "
                    "the invalid uncertified k=2..39 partial sum by more than the exact first omitted term "
                    "1/(20 * 2^30) > 4.65e-11."
                ),
                "Discontinuous jump E_3(2^{4/5}) != E_2(2^{4/5}); counterexample (Y = 9/4, d = 2) Q_{lambda,1}(9/8) - Q_{lambda,2}(9/8) > 0 and E_1(9/8) != E_2(9/8); c_small = 1 + e^{-1} - zeta(3) = 0.165822538011... > 4/25 > 1/24; all-L base-scale energy floor m_{all-L} = I_1 = 0.000804166369... > 8e-4 > 0; Selberg residue c_{Sel,lambda} = -3.434275302181... < -3.43 < 0; C_{cut,diag} = 22312.6918412014...; Theta_eps^{diag}(128) and threshold caps for eps in {1/2, 1/4, 1/8}.",
                "Certified finite observations at sampled scales: Liouville X_tilde_{lambda,pp}(Y) changes sign across the five sampled scales Y in {8, 16, 32, 64, 128} (< 0 at Y in {8, 32, 128}, > 0 at Y in {16, 64}), whereas at sampled Y in {32, 128} the 2-adic parity control has X_tilde_{a_2,pp}(32) = +0.52015... and X_tilde_{a_2,pp}(128) = +3.93411... (reported strictly as finite sampled data, not asymptotic zero-mean, O(1), or growth claims).",
            ],
            "5_consistency_checks": [
                "Complete log-series prime-power sum vs K = 40 and K = 160 series + 2 r^K / [K(1 - r)] tail bounds; w_{2,lambda}(n) direct convolution vs (-Lambda + 2B) decomposition on 2 <= n <= 200; exact discrete Abel summation identity with floor(T/d) cutoff jumps on 2 <= d <= floor(Y); direct pair-by-pair off-diagonal quadrature vs subtraction E_Sigma_pp - D_tilde at Y = 8 (T = 14); Route A / Route B / Route C finite identity zero-enclosures across T = 0, 1, 6, 14, 15, 30, 77, 431 and M = 4 shift telescope.",
            ],
            "6_conjectures_and_falsified_candidates": [
                "Open target conjecture (SUBGATE-TC-043A): unconditional subpower bound E(Y) <<_eps Y^eps, or sufficient condition X_tilde_{lambda,pp}(Y) + E_{sh,1}(Y) <= A_eta Y^eta + theta_eta F(Y) (theta_eta in [0, 1/2); forward implication proved in Theorem 26, equivalence not asserted).",
                "Candidate I (Route A + homogeneous Cauchy-Schwarz majorant): specified Cauchy-Schwarz majorant falsified for contraction via prime-subset lower bound M_{A,sigma}(Y) >= M_{A,sigma}^{prime}(Y) >>_sigma T(Y)^{1-sigma}/(log T(Y))^2 -> infty (does not lower-bound the signed rough sum).",
                "Candidate II (Route B + fixed finite linear span closure / uncompensated Cauchy-Schwarz majorant): exact closure in a fixed finite span of {(log w)^m w^{5/2} e^{-w^2}} falsified by linear independence, and uncompensated Cauchy-Schwarz majorant diverges via m_{all-L} > 0 and W<1 positivity (growing-order M(Y) approx 2 log Y and vector-energy inequalities remain open).",
                "Candidate III (Route C + specified discrete Abel triangle-inequality majorant): uncompensated triangle-inequality majorant on 2 <= d <= b = floor(Y) falsified for power saving by its boundary term |W_2(b)| b^{-1/2} sqrt(E_{L_b}(Y/b)) >> sqrt(Y) (does not rule out compensated Abel formulations).",
                "Candidate IV (Monotone cutoff ordering L_d >= T(Y/d) for all d >= 2): falsified at (Y = 9/4, d = 2); unsigned majorant of linear cutoff replacement has square asymp Y/(log Y)^2 (actual signed cancellation unresolved), whereas quadratic diagonal cutoff replacement costs O(1).",
                "Parity controls a_2, a_{3,5,7}, and unsigned 1 falsify uniform Rough-Moebius sign (-1/sqrt(d)), (-1)^k prime-power sign, Selberg double-pole cancellation, and sampled negative X_tilde values.",
            ],
        },
    }

    arb_check = verify_all_serialized_arb_in_tree(report)
    assert arb_check["all_enclose_original_256bit_arb_ball"] is True, (
        f"Serialized Arb enclosure verification failed: {arb_check.get('failed_paths')}"
    )
    report["serialized_arb_self_check"] = arb_check
    if verify_review_doc and TC_057_REVIEW_DOC_PATH.exists():
        rev_audit = verify_tc057_review_displayed_enclosures(report, TC_057_REVIEW_DOC_PATH)
        assert rev_audit["all_displayed_intervals_contain_generated_enclosures"] is True, (
            "Displayed intervals in TC_057_COUPLED_ARITHMETIC_SCALE_ENERGY_BOOTSTRAP.md failed check: "
            f"untagged={rev_audit['untagged_intervals']}, failed={rev_audit['failed_intervals']}"
        )
        report["section_7_tc057_review_displayed_enclosures_audit"] = rev_audit
    return report


def write_task_tc057_coupled_scale_bootstrap_artifact(
    path: Path = COUPLED_SCALE_BOOTSTRAP_ARTIFACT_PATH,
    prec_bits: int = 256,
    verify_review_doc: bool = True,
) -> Dict[str, Any]:
    """Generate and write `data/tc_coupled_scale_energy_bootstrap.json`."""
    report = execute_task_tc057_coupled_scale_bootstrap_audit(
        prec_bits=prec_bits, verify_review_doc=verify_review_doc
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
    rep = write_task_tc057_coupled_scale_bootstrap_artifact()
    print(
        f"Wrote {COUPLED_SCALE_BOOTSTRAP_ARTIFACT_PATH} "
        f"(subgate={rep['subgate_tc043a_status']}, rh_proved={rep['rh_proved']})"
    )
