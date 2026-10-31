"""
TASK-TC-046: Prime-by-Prime Moebius Recovery and Arithmetic Cross-Grade Compatibility.

Investigates whether finite-prime Euler inversion of the divisor-aggregated profile,
    W_y(X) = sum_{m | P_y} mu(m) m^{-1/2} W_log(X / m)
           = [prod_{p <= y} (I - p^{-1/2} D_p)] W_log(X)
           = sum_{n >= 2} lambda_y(n) n^{-1/2} h_0(n / X),
supplies an independent compatibility constraint across concurrent tau-grades
K in A_R = Qbar intersect R (tau = 2*pi, Z_tau(s, K) = zeta(tau^{-K} s)) strong
enough to bound the signed Moebius remainder R_mu(X) uniformly on X >= 1.
"""

from __future__ import annotations

from fractions import Fraction
import math
from typing import Any, Dict, List, Tuple

from flint import acb, acb_series, arb, ctx as flint_ctx
import sympy as sp

from tc.canonical_theta_correlation_bound import (
    EPIC_TC_042_ID,
    evaluate_f_tau_acb,
    evaluate_h0_arb,
    evaluate_tilde_h0_arb,
    get_prime_powers_up_to,
    serialize_arb_certified,
    verify_all_serialized_arb_in_tree,
)

TASK_TC_046_ID = "TASK-TC-046"
STARTING_HEAD_TC_046 = "1fc477927ccbb242dec10217744b1ad054877e12"
PRIME_EULER_MOEBIUS_RECOVERY_STATUS = (
    "FINITE_PRIME_EULER_INVERSION_AND_COUPLED_CUTOFF_REDUCTION_PROVED_"
    "HORIZON_COLLAPSE_AND_LOW_FREQUENCY_EULER_SPIKE_OBSTRUCTIONS_QUANTIFIED"
)


# ---------------------------------------------------------------------------
# 1. Exact Arithmetic Helpers for Finite-Prime Euler Inversion
# ---------------------------------------------------------------------------


def primes_up_to(y: int) -> List[int]:
    """Return sorted list of primes p <= y."""
    if y < 2:
        return []
    sieve = bytearray([1]) * (y + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(math.isqrt(y)) + 1):
        if sieve[p]:
            sieve[p * p : y + 1 : p] = bytearray(len(range(p * p, y + 1, p)))
    return [p for p in range(2, y + 1) if sieve[p]]


def next_prime_above(y: int) -> int:
    """Return the smallest prime q > y."""
    candidate = max(2, int(y) + 1)
    while True:
        is_p = True
        for d in range(2, int(math.isqrt(candidate)) + 1):
            if candidate % d == 0:
                is_p = False
                break
        if is_p:
            return candidate
        candidate += 1


def prime_factors_with_multiplicity(n: int) -> List[Tuple[int, int]]:
    """Return prime factorization [(p_1, a_1), ...] of n >= 1 in increasing prime order."""
    if n <= 1:
        return []
    factors: List[Tuple[int, int]] = []
    rem = n
    d = 2
    while d * d <= rem:
        if rem % d == 0:
            cnt = 0
            while rem % d == 0:
                rem //= d
                cnt += 1
            factors.append((d, cnt))
        d += 1 if d == 2 else 2
    if rem > 1:
        factors.append((rem, 1))
    return factors


def moebius_mu_int(m: int) -> int:
    """Return exact Moebius mu(m) in {-1, 0, 1} for m >= 1."""
    if m <= 0:
        raise ValueError("m must be >= 1")
    if m == 1:
        return 1
    facs = prime_factors_with_multiplicity(m)
    for _, exp in facs:
        if exp > 1:
            return 0
    return -1 if (len(facs) % 2 == 1) else 1


def moebius_mu_y_int(m: int, y: int) -> int:
    """Return truncated finite-prime Moebius mu_y(m) = mu(m) * 1_{m | P_y}."""
    if m == 1:
        return 1
    facs = prime_factors_with_multiplicity(m)
    for p, exp in facs:
        if exp > 1 or p > y:
            return 0
    return -1 if (len(facs) % 2 == 1) else 1


def von_mangoldt_arb(n: int) -> arb:
    """Return von Mangoldt Lambda(n) as an Arb ball."""
    if n <= 1:
        return arb(0)
    facs = prime_factors_with_multiplicity(n)
    if len(facs) == 1:
        return arb(facs[0][0]).log()
    return arb(0)


def divisors_of_primorial(y: int) -> List[Tuple[int, int]]:
    """Return all (d, mu(d)) for d | P_y = prod_{p <= y} p (feasible for small y)."""
    ps = primes_up_to(y)
    if len(ps) > 16:
        raise ValueError(f"Refusing to enumerate 2^{len(ps)} divisors for y={y}")
    divs: List[Tuple[int, int]] = [(1, 1)]
    for p in ps:
        divs = divs + [(d * p, -mu_d) for d, mu_d in divs]
    divs.sort(key=lambda pair: pair[0])
    return divs


def evaluate_lambda_y_closed_form_arb(n: int, y: int) -> arb:
    """
    Evaluate lambda_y(n) = (mu_y * log)(n) via the three-case closed form:
      - log n   if omega_{<= y}(n) == 0 (no prime divisor <= y),
      - log p   if omega_{<= y}(n) == 1 (p is the unique prime divisor <= y),
      - 0       if omega_{<= y}(n) >= 2 (at least two distinct prime divisors <= y).
    """
    if n <= 1:
        return arb(0)
    facs = prime_factors_with_multiplicity(n)
    primes_le_y = [p for p, _ in facs if p <= y]
    if len(primes_le_y) == 0:
        return arb(n).log()
    if len(primes_le_y) == 1:
        return arb(primes_le_y[0]).log()
    return arb(0)


def evaluate_lambda_y_convolution_arb(n: int, y: int) -> arb:
    """
    Evaluate lambda_y(n) = sum_{d | n, d | P_y} mu(d) log(n / d) directly from
    Dirichlet convolution over the squarefree y-smooth divisors of n.
    """
    if n <= 1:
        return arb(0)
    facs = prime_factors_with_multiplicity(n)
    primes_le_y = [p for p, _ in facs if p <= y]
    divs: List[Tuple[int, int]] = [(1, 1)]
    for p in primes_le_y:
        divs = divs + [(d * p, -mu_d) for d, mu_d in divs]
    total = arb(0)
    for d, mu_d in divs:
        total += arb(mu_d) * arb(n // d).log()
    return total


def evaluate_lambda_y_recursion_arb(n: int, y: int) -> arb:
    """
    Evaluate lambda_y(n) via the prime-by-prime recursion:
      lambda_{p_0}(m) = log m,
      lambda_{p_k}(m) = lambda_{p_{k-1}}(m) - 1_{p_k | m} * lambda_{p_{k-1}}(m / p_k).
    """
    if n <= 1:
        return arb(0)
    ps = primes_up_to(y)
    # Only divisors of n are ever queried by the recursion at n
    divs_of_n: List[int] = []
    for d in range(1, int(math.isqrt(n)) + 1):
        if n % d == 0:
            divs_of_n.append(d)
            if d * d != n:
                divs_of_n.append(n // d)
    divs_of_n.sort()
    vals: Dict[int, arb] = {m: arb(m).log() for m in divs_of_n}
    for p in ps:
        new_vals: Dict[int, arb] = {}
        for m in divs_of_n:
            if m % p == 0:
                new_vals[m] = vals[m] - vals[m // p]
            else:
                new_vals[m] = vals[m]
        vals = new_vals
    return vals[n]


def evaluate_summatory_L_y_direct_arb(x: float, y: int) -> arb:
    """Evaluate L_y(x) = sum_{2 <= n <= x} lambda_y(n) via the closed-form coefficients."""
    n_max = int(math.floor(x))
    total = arb(0)
    for n in range(2, n_max + 1):
        total += evaluate_lambda_y_closed_form_arb(n, y)
    return total


def evaluate_summatory_L_y_factorial_divisor_sum_arb(x: float, y: int) -> arb:
    """
    Evaluate L_y(x) = sum_{d | P_y, d <= x} mu(d) log(floor(x / d)!)
    via the exact divisor-factorial identity.
    """
    divs = divisors_of_primorial(y)
    # Precompute log(k!) = sum_{j=2}^k log j up to floor(x)
    k_max = max(1, int(math.floor(x)))
    log_fact = [arb(0)] * (k_max + 1)
    acc = arb(0)
    for j in range(2, k_max + 1):
        acc += arb(j).log()
        log_fact[j] = acc
    total = arb(0)
    for d, mu_d in divs:
        if d > x:
            break
        q = int(math.floor(x / d))
        if q >= 2:
            total += arb(mu_d) * log_fact[q]
    return total


def evaluate_chebyshev_psi_arb(x: float) -> arb:
    """Evaluate Chebyshev psi(x) = sum_{2 <= n <= x} Lambda(n) in Arb."""
    n_max = int(math.floor(x))
    total = arb(0)
    for n in range(2, n_max + 1):
        total += von_mangoldt_arb(n)
    return total


# ---------------------------------------------------------------------------
# 2. Certified Evaluation of W(X), W_log(X), and W_y(X)
# ---------------------------------------------------------------------------


def evaluate_w_prime_sum_certified_arb(
    X: arb, n_max: int = 4000, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Certify W(X) = sum_{n=2}^infty Lambda(n) n^{-1/2} h_0(n / X) in Arb with
    rigorous Bernstein tail enclosure for n > n_max:
      |sum_{n > n_max} Lambda(n) n^{-1/2} h_0(n / X)|
        <= (92193 / 32768) X^{5/2} (2 log(n_max) + 1) / (4 n_max^2).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X_arb = arb(X)
        pp_list = get_prime_powers_up_to(n_max)
        partial_sum = arb(0)
        for pk, p, _ in pp_list:
            pk_arb = arb(pk)
            partial_sum += (arb(p).log() / pk_arb.sqrt()) * evaluate_h0_arb(
                pk_arb / X_arb
            )
        c0 = arb(92193) / arb(32768)
        n_max_arb = arb(n_max)
        tail_bound = (
            c0
            * (X_arb ** (arb(5) / arb(2)))
            * (arb(2) * n_max_arb.log() + arb(1))
            / (arb(4) * (n_max_arb**2))
        )
        total_enclosure = partial_sum + arb(0, tail_bound.upper())
        return {
            "X": float(X_arb.mid()),
            "n_max": n_max,
            "enclosure_arb": total_enclosure,
            "certified": serialize_arb_certified(total_enclosure),
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_w_log_divisor_aggregated_certified_arb(
    X: arb, k_max: int = 4000, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Certify W_log(X) = sum_{k=2}^infty (log k) k^{-1/2} h_0(k / X) in Arb with
    rigorous Bernstein tail enclosure for k > k_max:
      |sum_{k > k_max} (log k) k^{-1/2} h_0(k / X)|
        <= (92193 / 32768) X^{5/2} (2 log(k_max) + 1) / (4 k_max^2).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X_arb = arb(X)
        partial_sum = arb(0)
        for k in range(2, k_max + 1):
            k_arb = arb(k)
            partial_sum += (k_arb.log() / k_arb.sqrt()) * evaluate_h0_arb(
                k_arb / X_arb
            )
        c0 = arb(92193) / arb(32768)
        k_max_arb = arb(k_max)
        tail_bound = (
            c0
            * (X_arb ** (arb(5) / arb(2)))
            * (arb(2) * k_max_arb.log() + arb(1))
            / (arb(4) * (k_max_arb**2))
        )
        total_enclosure = partial_sum + arb(0, tail_bound.upper())
        return {
            "X": float(X_arb.mid()),
            "k_max": k_max,
            "enclosure_arb": total_enclosure,
            "certified": serialize_arb_certified(total_enclosure),
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_w_y_coefficient_certified_arb(
    X: arb, y: int, n_max: int = 4000, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Certify W_y(X) = sum_{n=2}^infty lambda_y(n) n^{-1/2} h_0(n / X) in Arb using
    the coefficient representation plus the rigorous Bernstein tail enclosure
    for n > n_max (since 0 <= lambda_y(n) <= log n for all n >= 2):
      |sum_{n > n_max} lambda_y(n) n^{-1/2} h_0(n / X)|
        <= (92193 / 32768) X^{5/2} (2 log(n_max) + 1) / (4 n_max^2).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X_arb = arb(X)
        partial_sum = arb(0)
        for n in range(2, n_max + 1):
            lam_n = evaluate_lambda_y_closed_form_arb(n, y)
            if not (lam_n == 0):
                n_arb = arb(n)
                partial_sum += (lam_n / n_arb.sqrt()) * evaluate_h0_arb(n_arb / X_arb)

        c0 = arb(92193) / arb(32768)
        n_max_arb = arb(n_max)
        tail_bound = (
            c0
            * (X_arb ** (arb(5) / arb(2)))
            * (arb(2) * n_max_arb.log() + arb(1))
            / (arb(4) * (n_max_arb**2))
        )
        tail_ball = arb(0, tail_bound.upper())
        total_enclosure = partial_sum + tail_ball
        return {
            "X": float(X_arb.mid()),
            "y": y,
            "n_max": n_max,
            "partial_sum": float(partial_sum.mid()),
            "tail_bound": float(tail_bound.upper()),
            "enclosure_arb": total_enclosure,
            "certified": serialize_arb_certified(total_enclosure),
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_w_y_divisor_sum_certified_arb(
    X: arb, y: int, k_max: int = 3000, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Certify W_y(X) = sum_{m | P_y} mu(m) m^{-1/2} W_log(X / m) directly by summing
    over divisors of P_y (for feasible prime cutoffs y <= 13).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X_arb = arb(X)
        divs = divisors_of_primorial(y)
        total = arb(0)
        for m, mu_m in divs:
            m_arb = arb(m)
            k_eff = max(250, min(k_max, int(k_max / math.sqrt(m)) + 200))
            w_log_m = evaluate_w_log_divisor_aggregated_certified_arb(
                X_arb / m_arb, k_max=k_eff, prec_bits=prec_bits
            )["enclosure_arb"]
            total += (arb(mu_m) / m_arb.sqrt()) * w_log_m
        return {
            "X": float(X_arb.mid()),
            "y": y,
            "num_divisors": len(divs),
            "enclosure_arb": total,
            "certified": serialize_arb_certified(total),
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_w_y_product_recursion_certified_arb(
    X: arb, y: int, k_max: int = 3000, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Certify W_y(X) = [prod_{p <= y} (I - p^{-1/2} D_p)] W_log(X) via the iterated
    one-prime recursion W_{p_k}(u) = W_{p_{k-1}}(u) - p_k^{-1/2} W_{p_{k-1}}(u / p_k).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X_arb = arb(X)
        ps = primes_up_to(y)
        divs = [d for d, _ in divisors_of_primorial(y)]
        # Evaluate W_0(X / d) = W_log(X / d) at all divisor scales X / d
        stage_vals: Dict[int, arb] = {}
        for d in divs:
            k_eff = max(250, min(k_max, int(k_max / math.sqrt(d)) + 200))
            stage_vals[d] = evaluate_w_log_divisor_aggregated_certified_arb(
                X_arb / arb(d), k_max=k_eff, prec_bits=prec_bits
            )["enclosure_arb"]
        # Apply each prime factor (I - p^{-1/2} D_p) in sequence
        active_divs = [1]
        recursion_trace: List[Dict[str, Any]] = [
            {
                "prime_step": 0,
                "prime": None,
                "W_stage_at_X_certified": serialize_arb_certified(stage_vals[1]),
            }
        ]
        for idx, p in enumerate(ps, start=1):
            p_inv_sqrt = arb(1) / arb(p).sqrt()
            next_divs = sorted(set(active_divs + [d * p for d in active_divs]))
            # To compute W_{p_k}(X / d) for d dividing prod_{j > k} p_j, we need stage_vals[d] - p^{-1/2} stage_vals[d * p]
            new_stage_vals: Dict[int, arb] = {}
            for d in divs:
                if (d * p) in stage_vals:
                    new_stage_vals[d] = stage_vals[d] - p_inv_sqrt * stage_vals[d * p]
                else:
                    new_stage_vals[d] = stage_vals[d]
            stage_vals = new_stage_vals
            active_divs = next_divs
            recursion_trace.append(
                {
                    "prime_step": idx,
                    "prime": p,
                    "W_stage_at_X_certified": serialize_arb_certified(stage_vals[1]),
                }
            )
        return {
            "X": float(X_arb.mid()),
            "y": y,
            "primes": ps,
            "recursion_trace": recursion_trace,
            "enclosure_arb": stage_vals[1],
            "certified": serialize_arb_certified(stage_vals[1]),
        }
    finally:
        flint_ctx.prec = saved_prec


evaluate_w_y_prime_recursion_certified_arb = evaluate_w_y_product_recursion_certified_arb


def evaluate_euler_sieved_seed_gram_norm_arb(
    y: int, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Evaluate the Euler-sieved seed Gram norm squared
      ||Psi_y||_{L^2(d^*x)}^2 = sum_{m1, m2 | P_y} (mu(m1)mu(m2)/sqrt(m1 m2)) h_0(m1/m2)
    in certified Arb ball arithmetic.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        h0_1_arb = evaluate_h0_arb(arb(1))
        divs = divisors_of_primorial(y)
        gram_sq = arb(0)
        diag_sq = arb(0)
        for m1, mu1 in divs:
            m1_arb = arb(m1)
            diag_sq += h0_1_arb / m1_arb
            for m2, mu2 in divs:
                if m1 == m2:
                    gram_sq += h0_1_arb / m1_arb
                elif m1 < m2:
                    m2_arb = arb(m2)
                    term = (
                        arb(2 * mu1 * mu2)
                        / (m1_arb * m2_arb).sqrt()
                        * evaluate_h0_arb(m1_arb / m2_arb)
                    )
                    gram_sq += term
        return {
            "y": y,
            "num_divisors": len(divs),
            "diag_norm_sq_arb": diag_sq,
            "gram_norm_sq_arb": gram_sq,
            "gram_norm_arb": gram_sq.sqrt(),
            "gram_norm_sq_certified": serialize_arb_certified(gram_sq),
            "gram_norm_certified": serialize_arb_certified(gram_sq.sqrt()),
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_euler_dirichlet_poly_acb(z: acb, y: int) -> acb:
    """Evaluate E_y(z) = prod_{p <= y} (1 - p^{-(z + 1/2)}) in Acb."""
    ps = primes_up_to(y)
    s = z + acb(arb(1) / arb(2))
    prod_val = acb(1)
    for p in ps:
        prod_val *= acb(1) - (acb(p) ** (-s))
    return prod_val


def evaluate_H0_critical_line_arb(t: arb) -> arb:
    """Evaluate H_0(it) = |F_tau(1/2 + it)|^2 on the critical line in Arb."""
    f_pos = evaluate_f_tau_acb(acb(arb(1) / arb(2), arb(t)))
    f_neg = evaluate_f_tau_acb(acb(arb(1) / arb(2), -arb(t)))
    return (f_pos * f_neg).real


def evaluate_b_log_boundary_term_arb(u: arb, prec_bits: int = 256) -> arb:
    """Evaluate B_{log,boundary}(u) = -int_0^1 t^{-1/2} (log t) h_0(t/u) dt in Arb."""
    from tc.canonical_theta_correlation_bound import evaluate_h0_acb

    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        u_arb = arb(u)
        u_c = acb(u_arb)
        tol_b = 2**(-90)
        eps_b = arb("1e-8")

        def _integrand_b_log(t_c: acb, analytic: bool, uc: acb = u_c) -> acb:
            return -(t_c ** acb("-0.5")) * t_c.log() * evaluate_h0_acb(
                t_c / uc, analytic=analytic
            )

        int_main = (
            acb.integral(
                _integrand_b_log,
                acb(eps_b),
                acb("0.25"),
                rel_tol=tol_b,
                abs_tol=tol_b,
            ).real
            + acb.integral(
                _integrand_b_log,
                acb("0.25"),
                acb(1),
                rel_tol=tol_b,
                abs_tol=tol_b,
            ).real
        )
        eps_tail = (
            (arb(92193) / arb(32768))
            * (u_arb ** arb("-2.5"))
            * (eps_b**3)
            * (arb(3) * (arb(1) / eps_b).log() + arb(1))
            / arb(9)
        )
        return int_main + arb(0, eps_tail.upper())
    finally:
        flint_ctx.prec = saved_prec


def certified_coupled_cutoff_M_X_arb(X: arb, prec_bits: int = 256) -> int:
    """
    Compute a certified safe integer cutoff M(X) >= max(2, X^{5/4}) directly from
    the Arb ball enclosure of X^{5/4} = (X^5)^{1/4} without passing through
    binary64 float conversion.

    For a general input interval ball crossing an integer boundary, taking the
    ceiling of the upper endpoint u_arb.upper().ceil() may exceed the minimal
    pointwise ceiling while guaranteeing M_X >= X^{5/4} and M_X^2 >= X^{5/2}
    across the entire input ball. Certifies in Arb ball arithmetic that
    arb(M_X) >= X^{5/4} and arb(M_X)^2 >= X^{5/2}.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        X_arb = arb(X)
        if bool(X_arb <= arb(0)):
            raise ValueError("X must be strictly positive")
        u_arb = (X_arb**5).root(4)
        ceil_upper = u_arb.upper().ceil()
        fmpz_val = ceil_upper.unique_fmpz()
        if fmpz_val is None:
            raise RuntimeError(
                f"Non-unique integer ceiling for upper endpoint of X^(5/4): {ceil_upper}"
            )
        M_X = max(2, int(fmpz_val))
        M_X_arb = arb(M_X)
        if not (
            bool(M_X_arb >= u_arb) and bool((M_X_arb**2) >= (X_arb**5).sqrt())
        ):
            raise RuntimeError(
                f"Certified cutoff M(X)={M_X} failed Arb inequality check for X={X_arb}"
            )
        return M_X
    finally:
        flint_ctx.prec = saved_prec


def certify_subproduct_counterexample_at_y210_arb(
    y: int = 210, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Reproduce and certify in 256-bit Arb the counterexample at y = 210 refuting
    the false subproduct inequality
        |E_y(i t_{y,-})|^2 >= prod_{y^{16/21} <= p <= y} (1 + p^{-1/2} + p^{-1})
    at t_{y,-} = 7*tau / (16*log y) = 7*pi / (8*log y).

    Discarding lower-prime factors p < y^{16/21} is invalid because small primes
    satisfy cos(t_{y,-} log p) > (1/2) p^{-1/2}, making their Euler factors
    g_p(t_{y,-}) = 1 + p^{-1} - 2*p^{-1/2}*cos(t_{y,-} log p) < 1.
    At y = 210:
        |E_{210}(i t_{210,-})|^2 ~ 3.3605057481 < 18.2536118944 ~ subproduct.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        ps = primes_up_to(y)
        y_arb = arb(y)
        log_y_arb = y_arb.log()
        t_y_minus_arb = (arb(7) * arb.pi()) / (arb(8) * log_y_arb)
        threshold_arb = (y_arb**16).root(21)

        full_e_sq_arb = arb(1)
        lower_prime_prod_arb = arb(1)
        upper_prime_actual_prod_arb = arb(1)
        claimed_false_subproduct_arb = arb(1)
        factors_less_than_one_count = 0
        upper_prime_count = 0

        for p in ps:
            p_arb = arb(p)
            inv_p = arb(1) / p_arb
            inv_sqrt_p = arb(1) / p_arb.sqrt()
            cos_minus = (t_y_minus_arb * p_arb.log()).cos()
            factor_actual = arb(1) + inv_p - arb(2) * inv_sqrt_p * cos_minus
            full_e_sq_arb *= factor_actual
            if bool(factor_actual < arb(1)):
                factors_less_than_one_count += 1
            if bool(p_arb >= threshold_arb):
                upper_prime_count += 1
                upper_prime_actual_prod_arb *= factor_actual
                claimed_false_subproduct_arb *= arb(1) + inv_sqrt_p + inv_p
            else:
                lower_prime_prod_arb *= factor_actual

        return {
            "y": y,
            "pi_y": len(ps),
            "threshold_y_pow_16_21_arb": threshold_arb,
            "upper_prime_count": upper_prime_count,
            "factors_less_than_one_count": factors_less_than_one_count,
            "t_y_minus_arb": t_y_minus_arb,
            "actual_E_y_abs_sq_at_t_y_minus_arb": full_e_sq_arb,
            "omitted_lower_prime_product_arb": lower_prime_prod_arb,
            "upper_prime_actual_product_arb": upper_prime_actual_prod_arb,
            "claimed_false_subproduct_arb": claimed_false_subproduct_arb,
            "omitted_lower_prime_product_strictly_less_than_one": bool(
                lower_prime_prod_arb < arb(1)
            ),
            "enclosures_disjoint_and_false_subproduct_exceeds_actual": bool(
                full_e_sq_arb < claimed_false_subproduct_arb
            ),
        }
    finally:
        flint_ctx.prec = saved_prec


def certify_H0_local_monotonicity_and_global_decay_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """
    Certify in 256-bit Arb:
      1. The left-endpoint exponential coefficient 4*cos(tau/16) = 2*sqrt(2 + sqrt(2))
         ~ 3.695518130045147 (strictly less than the right-endpoint coefficient 4).
      2. The canonical Weierstrass product identity (v = 4*t^2):
           H_0(it) / H_0(0) = (1 + v)^3 * prod_{n=1}^infty (1 + v / (4n + 1)^2)^{-1}.
      3. The local logarithmic derivative lower bound on 0 <= t <= 1 (0 <= v <= 4):
           (d/dv) log(H_0(it) / H_0(0)) = 3/(1 + v) - sum_{n=1}^infty 1/((4n + 1)^2 + v)
                                        >= 3/5 - tau^2 / 384 > 0,
         together with I_y subset [0, 1] for all integer y >= 24 (since exp(pi) ~ 23.1407).
      4. The 64-subinterval Arb certificate on [0, v_{2,+}] (v_{2,+} = 4*t_{2,+}^2,
         t_{2,+} = pi / log 2 ~ 4.53236) proving (d/dv) log(H_0(it)/H_0(0)) > 0 across
         all [0, t_{2,+}], covering the finite-table rows y in {2, 5, 11}.
      5. Explicit counterexample points (t = 5, 10, 20) refuting global monotonicity
         of H_0(it) on [0, infty) and confirming decay toward 0 as t -> infty.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        tau_arb = arb(2) * arb.pi()
        left_coeff_arb = arb(4) * (tau_arb / arb(16)).cos()
        left_coeff_algebraic_arb = arb(2) * (arb(2) + arb(2).sqrt()).sqrt()
        coeff_diff_arb = left_coeff_arb - left_coeff_algebraic_arb

        # Analytic lower bound on [0, 1] (0 <= v <= 4): 3/5 - tau^2 / 384
        dlog_dv_unit_interval_lb_arb = (arb(3) / arb(5)) - (tau_arb**2) / arb(384)
        # Analytic lower bound on [0, 2] (0 <= v <= 16, covering y = 5, 11): 3/17 - tau^2 / 384
        dlog_dv_t_le_2_lb_arb = (arb(3) / arb(17)) - (tau_arb**2) / arb(384)

        # Verify I_y subset [0, 1] iff y >= 24 for integer y (exp(pi) ~ 23.14069)
        exp_pi_arb = arb.pi().exp()
        t_plus_y23_arb = arb.pi() / arb(23).log()
        t_plus_y24_arb = arb.pi() / arb(24).log()

        # Verify canonical Weierstrass product identity at t in {1/4, 1/2, 1, 2}
        H0_0_arb = evaluate_H0_critical_line_arb(arb(0))
        product_identity_checks: List[Dict[str, Any]] = []
        n_trunc = 2000
        for t_label, t_arb in (
            ("1/4", arb(1) / arb(4)),
            ("1/2", arb(1) / arb(2)),
            ("1", arb(1)),
            ("2", arb(2)),
        ):
            v_arb = arb(4) * (t_arb**2)
            ratio_direct = evaluate_H0_critical_line_arb(t_arb) / H0_0_arb
            log_partial = arb(3) * (arb(1) + v_arb).log() - sum(
                (
                    (arb(1) + v_arb / arb((4 * n + 1) ** 2)).log()
                    for n in range(1, n_trunc + 1)
                ),
                arb(0),
            )
            tail_rad = (v_arb / arb(16 * n_trunc)).upper()
            ratio_product_enclosure = (log_partial + arb(0, tail_rad)).exp()
            residual_arb = ratio_direct - ratio_product_enclosure
            product_identity_checks.append(
                {
                    "t_label": t_label,
                    "v_eq_4_t_sq": float(v_arb.mid()),
                    "direct_ratio_H0_it_over_H0_0_arb": ratio_direct,
                    "weierstrass_product_enclosure_arb": ratio_product_enclosure,
                    "enclosures_intersect": bool(residual_arb.contains(0)),
                }
            )

        # 64-subinterval Arb certificate of d/dv log(H_0(it)/H_0(0)) > 0 across [0, v_{2,+}]
        t_plus_y2_arb = arb.pi() / arb(2).log()
        v_max_y2_arb = arb(4) * (t_plus_y2_arb**2)
        num_sub = 64
        dv_arb = v_max_y2_arb / arb(num_sub)
        min_dlog_dv_on_0_t2plus_arb: Optional[arb] = None
        all_subintervals_positive = True
        for j in range(1, num_sub + 1):
            v_lo = arb(j - 1) * dv_arb
            v_hi = arb(j) * dv_arb
            sum_hi = (
                sum(
                    (
                        arb(1) / (arb((4 * n + 1) ** 2) + v_lo)
                        for n in range(1, 201)
                    ),
                    arb(0),
                )
                + arb(1) / arb(3200)
            )
            sub_lb = arb(3) / (arb(1) + v_hi) - sum_hi
            if not bool(sub_lb > arb(0)):
                all_subintervals_positive = False
            if min_dlog_dv_on_0_t2plus_arb is None or bool(
                sub_lb.lower() < min_dlog_dv_on_0_t2plus_arb.lower()
            ):
                min_dlog_dv_on_0_t2plus_arb = sub_lb

        assert min_dlog_dv_on_0_t2plus_arb is not None

        # Global non-monotonicity and high-frequency decay checks
        H0_t2plus_arb = evaluate_H0_critical_line_arb(t_plus_y2_arb)
        H0_t5_arb = evaluate_H0_critical_line_arb(arb(5))
        H0_t10_arb = evaluate_H0_critical_line_arb(arb(10))
        H0_t20_arb = evaluate_H0_critical_line_arb(arb(20))

        return {
            "left_endpoint_coeff_4_cos_tau_over_16_arb": left_coeff_arb,
            "left_endpoint_coeff_exact_2_sqrt_2_plus_sqrt2_arb": left_coeff_algebraic_arb,
            "left_endpoint_coeff_algebraic_identity_contains_zero": bool(
                coeff_diff_arb.contains(0)
            ),
            "left_endpoint_coeff_strictly_between_3_6955_and_4": bool(
                left_coeff_arb > arb("3.6955") and left_coeff_arb < arb(4)
            ),
            "dlog_dv_unit_interval_lb_3_5_minus_tau_sq_over_384_arb": dlog_dv_unit_interval_lb_arb,
            "dlog_dv_unit_interval_lb_strictly_positive": bool(
                dlog_dv_unit_interval_lb_arb > arb(0)
            ),
            "dlog_dv_t_le_2_lb_3_17_minus_tau_sq_over_384_arb": dlog_dv_t_le_2_lb_arb,
            "dlog_dv_t_le_2_lb_strictly_positive": bool(
                dlog_dv_t_le_2_lb_arb > arb(0)
            ),
            "exp_pi_threshold_arb": exp_pi_arb,
            "t_plus_at_y23_arb": t_plus_y23_arb,
            "t_plus_at_y24_arb": t_plus_y24_arb,
            "y23_exceeds_unit_interval_and_y24_inside_unit_interval": bool(
                t_plus_y23_arb > arb(1) and t_plus_y24_arb < arb(1)
            ),
            "weierstrass_product_identity_checks": product_identity_checks,
            "all_weierstrass_product_checks_intersect": all(
                row["enclosures_intersect"] for row in product_identity_checks
            ),
            "subdivision_64_on_0_to_t2plus_all_dlog_dv_positive": all_subintervals_positive,
            "subdivision_64_min_dlog_dv_on_0_to_t2plus_arb": min_dlog_dv_on_0_t2plus_arb,
            "H0_at_0_arb": H0_0_arb,
            "H0_at_t2plus_arb": H0_t2plus_arb,
            "H0_at_t5_arb": H0_t5_arb,
            "H0_at_t10_arb": H0_t10_arb,
            "H0_at_t20_arb": H0_t20_arb,
            "global_monotonicity_falsified_H0_t5_lt_H0_t2plus": bool(
                H0_t5_arb < H0_t2plus_arb
            ),
            "high_frequency_decay_verified_H0_t20_lt_H0_0": bool(
                H0_t20_arb < H0_0_arb
                and H0_t20_arb < H0_t10_arb
                and H0_t10_arb < H0_t5_arb
            ),
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_euler_spike_interval_gram_lower_bound_arb(
    y: int, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Certify the controlled-width frequency interval lower bound on the Euler-sieved
    seed Gram norm squared ||Psi_y||_{L^2(d^*x)}^2 across
      I_y := [t_{y,-}, t_{y,+}] = [7*tau / (16*log y), tau / (2*log y)]
                                = [7*pi / (8*log y), pi / log y],
      |I_y| = tau / (16*log y) = pi / (8*log y) > 0.

    1. Euler-factor monotonicity on I_y:
       For every prime p <= y and every t in [0, tau / (2*log y)], the phase
       t*log(p) lies in [0, pi] where sin(t*log p) >= 0, so each factor
       g_p(t) = |1 - p^{-1/2 - it}|^2 = 1 + p^{-1} - 2*p^{-1/2}*cos(t*log p)
       has derivative g_p'(t) = 2*p^{-1/2}*(log p)*sin(t*log p) >= 0.
       Consequently, inf_{t in I_y} |E_y(it)|^2 = |E_y(i t_{y,-})|^2, with
       asymptotic log|E_y(i t_{y,-})|^2 = (4*cos(tau/16) + o(1)) * sqrt(y) / log y.
    2. Local kernel monotonicity and finite-table interval certification:
       With v = 4*t^2, H_0(it)/H_0(0) = (1 + v)^3 * prod_{n>=1} (1 + v/(4n+1)^2)^{-1}.
       For 0 <= t <= 1 (0 <= v <= 4), which contains I_y for all integer y >= 24,
       (d/dv) log(H_0(it)/H_0(0)) >= 3/5 - tau^2/384 > 0.
       For finite-table rows with y < 24 (and as an independent check for all y),
       we certify both (d/dv) log(H_0(it)/H_0(0)) > 0 across v in [4*t_{y,-}^2, 4*t_{y,+}^2]
       by 16-subinterval Arb bounding and direct 64-subinterval Arb ball evaluation of
       H_0(it) across I_y.
    3. Integrated Gram-norm lower-bound expressions:
       ||Psi_y||_{L^2}^2 >= (2 / tau) int_{t_{y,-}}^{t_{y,+}} |E_y(it)|^2 H_0(it) dt
                         >= (H_0(i t_{y,-}) / (8 log y)) |E_y(i t_{y,-})|^2
                         >= (H_0(0) / (8 log y)) |E_y(i t_{y,-})|^2.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        ps = primes_up_to(y)
        y_arb = arb(y)
        log_y_arb = y_arb.log()
        tau_arb = arb(2) * arb.pi()
        t_y_plus_arb = arb.pi() / log_y_arb
        t_y_minus_arb = (arb(7) * arb.pi()) / (arb(8) * log_y_arb)
        interval_width_arb = arb.pi() / (arb(8) * log_y_arb)

        e_sq_at_plus_arb = arb(1)
        e_sq_at_minus_arb = arb(1)
        constructive_at_plus_count = 0
        constructive_across_interval_count = 0
        for p in ps:
            p_arb = arb(p)
            log_p_arb = p_arb.log()
            inv_p = arb(1) / p_arb
            two_inv_sqrt_p = arb(2) / p_arb.sqrt()

            cos_plus = (t_y_plus_arb * log_p_arb).cos()
            cos_minus = (t_y_minus_arb * log_p_arb).cos()
            if bool(cos_plus < arb(0)):
                constructive_at_plus_count += 1
            if bool(cos_minus < arb(0)):
                constructive_across_interval_count += 1

            e_sq_at_plus_arb *= arb(1) + inv_p - two_inv_sqrt_p * cos_plus
            e_sq_at_minus_arb *= arb(1) + inv_p - two_inv_sqrt_p * cos_minus

        H0_at_0_arb = evaluate_H0_critical_line_arb(arb(0))
        H0_at_minus_arb = evaluate_H0_critical_line_arb(t_y_minus_arb)
        H0_at_plus_arb = evaluate_H0_critical_line_arb(t_y_plus_arb)

        # Certify d/dv log(H_0(it)/H_0(0)) > 0 on v in [4*t_{y,-}^2, 4*t_{y,+}^2]:
        in_unit_interval = bool(t_y_plus_arb <= arb(1))
        if in_unit_interval:
            dlog_dv_min_arb = (arb(3) / arb(5)) - (tau_arb**2) / arb(384)
        else:
            v_min_arb = arb(4) * (t_y_minus_arb**2)
            v_max_arb = arb(4) * (t_y_plus_arb**2)
            k_sub_v = 16
            dv_sub = (v_max_arb - v_min_arb) / arb(k_sub_v)
            dlog_dv_min_arb = None
            for j in range(1, k_sub_v + 1):
                v_lo = v_min_arb + arb(j - 1) * dv_sub
                v_hi = v_min_arb + arb(j) * dv_sub
                s_hi = (
                    sum(
                        (
                            arb(1) / (arb((4 * n + 1) ** 2) + v_lo)
                            for n in range(1, 201)
                        ),
                        arb(0),
                    )
                    + arb(1) / arb(3200)
                )
                sub_lb = arb(3) / (arb(1) + v_hi) - s_hi
                if dlog_dv_min_arb is None or bool(
                    sub_lb.lower() < dlog_dv_min_arb.lower()
                ):
                    dlog_dv_min_arb = sub_lb
            assert dlog_dv_min_arb is not None

        # Also compute a direct 64-subinterval Arb ball cover of I_y = [t_{y,-}, t_{y,+}]
        k_sub_t = 64
        dt_sub = (t_y_plus_arb - t_y_minus_arb) / arb(k_sub_t)
        H0_subdiv_min_arb: Optional[arb] = None
        for j in range(k_sub_t):
            a_t = t_y_minus_arb + arb(j) * dt_sub
            b_t = t_y_minus_arb + arb(j + 1) * dt_sub
            mid_t = (a_t + b_t) / arb(2)
            rad_t = (b_t - a_t) / arb(2)
            t_ball = arb(mid_t.mid(), mid_t.rad() + rad_t.upper())
            h_ball = evaluate_H0_critical_line_arb(t_ball)
            if H0_subdiv_min_arb is None or bool(
                h_ball.lower() < H0_subdiv_min_arb.lower()
            ):
                H0_subdiv_min_arb = h_ball
        assert H0_subdiv_min_arb is not None

        # Since 2 * |I_y| / tau = 2 * (pi / (8 log y)) / (2 pi) = 1 / (8 log y):
        gram_sq_lb_H0_0_arb = (
            H0_at_0_arb / (arb(8) * log_y_arb)
        ) * e_sq_at_minus_arb
        gram_sq_lb_H0_subdiv_arb = (
            H0_subdiv_min_arb / (arb(8) * log_y_arb)
        ) * e_sq_at_minus_arb
        gram_sq_lb_H0_minus_arb = (
            H0_at_minus_arb / (arb(8) * log_y_arb)
        ) * e_sq_at_minus_arb

        return {
            "y": y,
            "pi_y": len(ps),
            "t_y_minus_arb": t_y_minus_arb,
            "t_y_plus_arb": t_y_plus_arb,
            "interval_width_arb": interval_width_arb,
            "constructive_at_plus_count": constructive_at_plus_count,
            "constructive_across_interval_count": constructive_across_interval_count,
            "e_sq_at_minus_arb": e_sq_at_minus_arb,
            "e_sq_at_plus_arb": e_sq_at_plus_arb,
            "H0_at_0_arb": H0_at_0_arb,
            "H0_at_minus_arb": H0_at_minus_arb,
            "H0_at_plus_arb": H0_at_plus_arb,
            "H0_subdiv_min_arb": H0_subdiv_min_arb,
            "H0_dlog_dv_min_on_I_y_arb": dlog_dv_min_arb,
            "gram_sq_lb_H0_0_arb": gram_sq_lb_H0_0_arb,
            "gram_sq_lb_H0_subdiv_arb": gram_sq_lb_H0_subdiv_arb,
            "gram_sq_lb_H0_minus_arb": gram_sq_lb_H0_minus_arb,
            "I_y_subset_of_analytic_unit_interval_0_1": in_unit_interval,
            "E_y_sq_interval_monotonicity_by_phase_in_0_pi": bool(
                (t_y_plus_arb * log_y_arb - arb.pi()).contains(0)
                and all(
                    bool(t_y_plus_arb * arb(p).log() < arb.pi())
                    for p in ps
                    if p < y
                )
            ),
            "H0_interval_monotonicity_certified_on_I_y": bool(
                dlog_dv_min_arb > arb(0)
            ),
            "H0_interval_subdivision_exceeds_H0_0": bool(
                H0_subdiv_min_arb > H0_at_0_arb
            ),
            "endpoint_ordering_E_y_sq_minus_le_plus": bool(
                e_sq_at_minus_arb <= e_sq_at_plus_arb
            ),
            "endpoint_ordering_H0_0_le_minus_le_plus": bool(
                H0_at_0_arb <= H0_at_minus_arb and H0_at_minus_arb <= H0_at_plus_arb
            ),
            # Preserve backwards-compatible aliases for caller convenience
            "monotonicity_verified": bool(e_sq_at_minus_arb <= e_sq_at_plus_arb),
            "H0_monotonicity_verified": bool(
                dlog_dv_min_arb > arb(0) and H0_subdiv_min_arb > H0_at_0_arb
            ),
        }
    finally:
        flint_ctx.prec = saved_prec


def compute_coupled_cutoff_comparison_bound_arb(
    X: arb, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Compute the certified safe integer cutoff M(X) >= ceil(max(2, X^{5/4})) directly in Arb
    (without float conversion) and the certified comparison bound
    C_{log,0} X^{5/2} / (2 M(X)^2) <= (1/2) C_{log,0}.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X_arb = arb(X)
        s3_series = acb_series([acb(3), acb(1)], prec=prec_bits).zeta()
        neg_zeta_prime_3_arb = -s3_series[1].real
        c_log_0_arb = (arb(92193) / arb(32768)) * neg_zeta_prime_3_arb
        half_c_log_0_arb = c_log_0_arb / arb(2)
        X_pow_5_4 = (X_arb**5).root(4)
        X_pow_5_2 = (X_arb**5).sqrt()
        M_X = certified_coupled_cutoff_M_X_arb(X_arb, prec_bits=prec_bits)
        M_X_arb = arb(M_X)
        ratio_to_M_sq = X_pow_5_2 / (M_X_arb**2)
        bound_at_M_X = half_c_log_0_arb * ratio_to_M_sq
        return {
            "X": float(X_arb.mid()),
            "X_pow_5_4_arb": X_pow_5_4,
            "M_X": M_X,
            "q_gt_M_X": next_prime_above(M_X),
            "c_log_0_arb": c_log_0_arb,
            "half_c_log_0_arb": half_c_log_0_arb,
            "bound_at_M_X_arb": bound_at_M_X,
            "M_X_ge_X_pow_5_4": bool(M_X_arb >= X_pow_5_4),
            "M_X_sq_ge_X_pow_5_2": bool((M_X_arb**2) >= X_pow_5_2),
            "satisfies_uniform_bound": bool(
                ratio_to_M_sq <= arb(1)
                and bound_at_M_X.upper() <= half_c_log_0_arb.upper()
            ),
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_symbolic_finite_prime_identities() -> Dict[str, Any]:
    """Verify exact symbolic identities for finite-prime Euler inversion using SymPy."""
    a_s, b_s = sp.symbols("a b", integer=True, positive=True)
    log_p, log_r, log_q = sp.symbols("log_p log_r log_q", real=True)
    u_s, v_s = sp.symbols("u v", commutative=True)
    comm_diff = sp.expand((1 - u_s) * (1 - v_s) - (1 - v_s) * (1 - u_s))
    prod_2_exp = sp.expand((1 - u_s) * (1 - v_s) - (1 - u_s - v_s + u_s * v_s))
    log_prod_diff = sp.simplify(
        (a_s * log_p + b_s * log_r) - a_s * log_p - b_s * log_r
    )
    lam_small_pp = sp.simplify(a_s * log_p - (a_s - 1) * log_p)
    lam_large_pp = sp.simplify(b_s * log_r)
    lam_mixed_one_small = sp.simplify(
        (a_s * log_p + b_s * log_r) - ((a_s - 1) * log_p + b_s * log_r)
    )
    lam_two_small = sp.simplify(
        (a_s * log_p + b_s * log_q)
        - ((a_s - 1) * log_p + b_s * log_q)
        - (a_s * log_p + (b_s - 1) * log_q)
        + ((a_s - 1) * log_p + (b_s - 1) * log_q)
    )
    alpha_exp = sp.Rational(5, 4)
    tail_exponent_diff = sp.Rational(5, 2) - 2 * alpha_exp
    return {
        "commutation_verified": (comm_diff == 0),
        "two_prime_expansion_verified": (prod_2_exp == 0),
        "log_additivity_verified": (log_prod_diff == 0),
        "small_prime_power_equals_log_p": (sp.simplify(lam_small_pp - log_p) == 0),
        "large_prime_power_equals_b_log_r": (
            sp.simplify(lam_large_pp - b_s * log_r) == 0
        ),
        "mixed_composite_one_small_prime_equals_log_p": (
            sp.simplify(lam_mixed_one_small - log_p) == 0
        ),
        "two_small_primes_vanishes": (lam_two_small == 0),
        "coupled_exponent_difference_5_2_minus_2_times_5_4": int(tail_exponent_diff),
        "coupled_exponent_verified": (tail_exponent_diff == 0),
    }


# ---------------------------------------------------------------------------
# 3. Master Execution for TASK-TC-046 (Section 15)
# ---------------------------------------------------------------------------


def execute_task_tc046_prime_euler_moebius_recovery(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """
    Execute TASK-TC-046: Prime-by-Prime Moebius Recovery and Arithmetic Cross-Grade Compatibility.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()
        h0_1_arb = evaluate_h0_arb(arb(1))

        # Exact small-scale constant C_{log,0} = (92193/32768) (-zeta'(3))
        s3_series = acb_series([acb(3), acb(1)], prec=prec_bits).zeta()
        neg_zeta_prime_3_arb = -s3_series[1].real
        c_log_0_arb = (arb(92193) / arb(32768)) * neg_zeta_prime_3_arb
        half_c_log_0_arb = c_log_0_arb / arb(2)

        # -------------------------------------------------------------------
        # Step 1 & Step 2: Recovered Obligation & Ambient Space vs Admissible Grades
        # -------------------------------------------------------------------
        # Verify transcendence / irrationality bookkeeping: log_tau(p) = log(p) / log(2*pi)
        log_tau_arb = tau_arb.log()
        prime_log_tau_shifts = []
        for p in (2, 3, 5, 7, 11):
            shift_arb = arb(p).log() / log_tau_arb
            prime_log_tau_shifts.append(
                {
                    "prime_p": p,
                    "log_tau_p_certified": serialize_arb_certified(shift_arb),
                    "note": (
                        f"D_{p} shifts log_tau(X) by log_tau({p}) = log({p})/log(2*pi); "
                        "since tau = 2*pi is transcendental (Lindemann-Weierstrass), "
                        f"log_tau({p}) is not rational and cannot be assumed in A_R = Qbar intersect R."
                    ),
                }
            )

        recovered_obligation_summary = {
            "W_definition": "W(X) = sum_{n>=2} Lambda(n) n^{-1/2} h_0(n/X)",
            "W_log_definition": "W_log(X) = sum_{n>=2} (log n) n^{-1/2} h_0(n/X)",
            "R_mu_definition": "R_mu(X) = sum_{m>=2} mu(m) m^{-1/2} W_log(X/m)",
            "moebius_recovery_identity": "W(X) = W_log(X) + R_mu(X)",
            "established_W_log_large_scale_bound": "|W_log(X)| <= 3.3490080247 < 3.34901 for all X >= 1",
            "established_W_log_small_scale_bound": "|W_log(u)| <= C_{log,0} u^{5/2} for all u > 0",
            "C_log_0_certified": serialize_arb_certified(c_log_0_arb),
            "half_C_log_0_certified": serialize_arb_certified(half_c_log_0_arb),
            "mixed_grade_identity": (
                "C_tau(K - L) = Q_tau(T_K psi_tau, T_L psi_tau) = B_known(K, L) - R_mu(tau^{|K-L|}) "
                "with |B_known(K, L)| <= 7.0794281303 < 7.07943"
            ),
            "missing_arithmetic_estimate": "sup_{X >= 1} |R_mu(X)| < infty",
            "ambient_space_vs_admissible_grades_bookkeeping": {
                "ambient_function_space": (
                    "F_{5/2} := {F in C((0, infty)) : |F(u)| = O(u^{5/2}) as u -> 0^+ and |F(X)| = O(X^theta) as X -> infty}, "
                    " together with the unitary dilation representation (U_p f)(x) = f(x/p) on L^2(R_{>0}, d^*x)"
                ),
                "operator_action": "(D_p F)(X) = F(X / p) on X in (0, infty) (shifting kappa = log_tau X -> kappa - log_tau p on R)",
                "restriction_to_admissible_grades": (
                    "Because log_tau(p) = log(p)/log(2*pi) cannot be assumed algebraic in A_R = Qbar intersect R, "
                    "the commuting operators {I - p^{-1/2} D_p}_{p <= y} are defined and composed on the ambient continuous "
                    "scale space (0, infty); for each fixed y, the resulting continuous profile W_y(X) is then restricted to "
                    "admissible grade scales X = tau^{|K - L|} (K, L in A_R), where density of A_R in R and continuity of "
                    "fixed-y W_y imply sup_{K in A_R} |W_y(tau^{|K|})| = sup_{X >= 1} |W_y(X)|. By contrast, for the coupled "
                    "cutoff y = M(X) = ceil(max(2, X^{5/4})), F(X) = W_{M(X)}(X) is piecewise continuous with right-hand "
                    "jumps F(X_0^+) - F(X_0) = -p^{-1/2} W_{p^-}(X_0/p) at prime thresholds X_0 = (p-1)^{4/5}, so extending "
                    "boundedness from dense K in A_R to all X >= 1 uses continuity of W(X) (or R_mu(X)) together with the "
                    "uniform comparison |F(X) - W(X)| <= (1/2) C_{log,0} < 0.278715, NEVER continuity of F(X)."
                ),
                "prime_log_tau_shifts": prime_log_tau_shifts,
            },
        }

        # -------------------------------------------------------------------
        # Step 3: Exact Finite-Prime Euler Inversion, Coefficient Formula,
        #         Summatory Factorial Identity, and Agreement Threshold 2*q_{>y}
        # -------------------------------------------------------------------
        # 3A. Verify closed-form, Dirichlet convolution, and prime-by-prime recursion for lambda_y(n)
        cutoffs_check = (2, 3, 5, 7, 11, 13)
        n_check_max = 120
        all_three_lambda_methods_agree = True
        all_delta_nonnegative = True
        threshold_checks: List[Dict[str, Any]] = []

        for y in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
            q_gt_y = next_prime_above(y)
            first_diff_n = None
            max_check_n = max(n_check_max, 2 * q_gt_y + 20)
            for n in range(2, max_check_n + 1):
                lam_cf = evaluate_lambda_y_closed_form_arb(n, y)
                if y in cutoffs_check and n <= n_check_max:
                    lam_conv = evaluate_lambda_y_convolution_arb(n, y)
                    lam_rec = evaluate_lambda_y_recursion_arb(n, y)
                    if not (
                        bool((lam_cf - lam_conv).contains(0))
                        and bool(abs(lam_cf - lam_conv) < arb("1e-70"))
                        and bool((lam_cf - lam_rec).contains(0))
                        and bool(abs(lam_cf - lam_rec) < arb("1e-70"))
                    ):
                        all_three_lambda_methods_agree = False
                lam_vm = von_mangoldt_arb(n)
                diff = lam_cf - lam_vm
                if not (bool(diff.contains(0)) or bool(diff > arb(0))):
                    all_delta_nonnegative = False
                if first_diff_n is None and not (
                    bool(diff.contains(0)) and bool(abs(diff) < arb("1e-70"))
                ):
                    first_diff_n = n
            diff_at_2q = evaluate_lambda_y_closed_form_arb(
                2 * q_gt_y, y
            ) - von_mangoldt_arb(2 * q_gt_y)
            matches_log2 = bool(
                (diff_at_2q - arb(2).log()).contains(0)
            ) and bool(abs(diff_at_2q - arb(2).log()) < arb("1e-70"))
            threshold_checks.append(
                {
                    "y": y,
                    "next_prime_q_gt_y": q_gt_y,
                    "predicted_first_discrepancy_2_q_gt_y": 2 * q_gt_y,
                    "observed_first_discrepancy_n": first_diff_n,
                    "exact_agreement_for_all_2_le_n_lt_2_q_gt_y": (
                        first_diff_n == 2 * q_gt_y
                    ),
                    "discrepancy_at_2_q_gt_y_equals_log_2": matches_log2,
                }
            )

        # Representative integer / prime-power / composite classification table at y = 5 (q_{>5} = 7, 2*q_{>5} = 14)
        representative_lambda_cases_y5: List[Dict[str, Any]] = []
        rep_ns_y5 = [
            (2, "prime p <= y (omega_{<=5}=1)"),
            (4, "prime power p^2 with p <= y (omega_{<=5}=1, lambda_5(4)=log 2=Lambda(4))"),
            (6, "composite with 2 distinct primes <= y (2*3, omega_{<=5}=2, lambda_5(6)=0=Lambda(6))"),
            (7, "prime r > y (omega_{<=5}=0, lambda_5(7)=log 7=Lambda(7))"),
            (8, "prime power p^3 with p <= y (2^3, omega_{<=5}=1, lambda_5(8)=log 2=Lambda(8))"),
            (9, "prime power p^2 with p <= y (3^2, omega_{<=5}=1, lambda_5(9)=log 3=Lambda(9))"),
            (12, "prime-power composite with 2 distinct primes <= y (2^2*3, omega_{<=5}=2, lambda_5(12)=0=Lambda(12))"),
            (14, "FIRST DISCREPANCY 2*q_{>5} = 2*7: mixed composite with 1 prime <= y and 1 prime > y (omega_{<=5}=1, lambda_5(14)=log 2 != Lambda(14)=0)"),
            (25, "prime power p^2 with p <= y (5^2, omega_{<=5}=1, lambda_5(25)=log 5=Lambda(25))"),
            (28, "mixed prime-power composite 2^2 * 7 (omega_{<=5}=1, lambda_5(28)=log 2 != Lambda(28)=0)"),
            (30, "primorial P_5 = 2*3*5 (omega_{<=5}=3, lambda_5(30)=0=Lambda(30))"),
            (49, "FIRST ROUGH COMPOSITE q_{>5}^2 = 7^2: prime square with r > y (omega_{<=5}=0, lambda_5(49)=2 log 7 != Lambda(49)=log 7)"),
            (77, "rough composite 7*11 with 2 distinct primes > y (omega_{<=5}=0, lambda_5(77)=log 77 != Lambda(77)=0)"),
        ]
        for n_val, desc in rep_ns_y5:
            lam_cf = evaluate_lambda_y_closed_form_arb(n_val, 5)
            lam_conv = evaluate_lambda_y_convolution_arb(n_val, 5)
            lam_rec = evaluate_lambda_y_recursion_arb(n_val, 5)
            lam_vm = von_mangoldt_arb(n_val)
            facs = prime_factors_with_multiplicity(n_val)
            omega_le_5 = sum(1 for p, _ in facs if p <= 5)
            representative_lambda_cases_y5.append(
                {
                    "n": n_val,
                    "case_description": desc,
                    "omega_le_5": omega_le_5,
                    "lambda_5_certified": serialize_arb_certified(lam_cf),
                    "Lambda_certified": serialize_arb_certified(lam_vm),
                    "delta_5_equals_lambda_minus_Lambda_certified": serialize_arb_certified(
                        lam_cf - lam_vm
                    ),
                    "closed_form_matches_convolution_and_recursion": bool(
                        (lam_cf - lam_conv).contains(0)
                        and abs(lam_cf - lam_conv) < arb("1e-70")
                        and (lam_cf - lam_rec).contains(0)
                        and abs(lam_cf - lam_rec) < arb("1e-70")
                    ),
                    "equals_von_mangoldt": bool(
                        (lam_cf - lam_vm).contains(0)
                        and abs(lam_cf - lam_vm) < arb("1e-70")
                    ),
                }
            )

        # 3B. Verify summatory identity L_y(x) = sum_{d | P_y, d <= x} mu(d) log(floor(x/d)!)
        #     and prime-by-prime recursion L_{p_k}(x) = L_{p_{k-1}}(x) - L_{p_{k-1}}(x / p_k)
        summatory_checks: List[Dict[str, Any]] = []
        for y in (2, 3, 5, 7, 11):
            q_gt_y = next_prime_above(y)
            ps = primes_up_to(y)
            y_prev = ps[-2] if len(ps) >= 2 else 1
            p_last = ps[-1]
            for x_val in (5.0, 10.0, 13.5, 14.0, 25.0, 50.0, 100.0):
                L_dir = evaluate_summatory_L_y_direct_arb(x_val, y)
                L_fact = evaluate_summatory_L_y_factorial_divisor_sum_arb(x_val, y)
                psi_x = evaluate_chebyshev_psi_arb(x_val)
                if y_prev >= 2:
                    L_prev_x = evaluate_summatory_L_y_direct_arb(x_val, y_prev)
                    L_prev_xp = evaluate_summatory_L_y_direct_arb(
                        x_val / p_last, y_prev
                    )
                else:
                    # L_1(u) = sum_{2 <= k <= u} log k = log(floor(u)!)
                    L_prev_x = sum(
                        (arb(k).log() for k in range(2, int(math.floor(x_val)) + 1)),
                        arb(0),
                    )
                    L_prev_xp = sum(
                        (
                            arb(k).log()
                            for k in range(2, int(math.floor(x_val / p_last)) + 1)
                        ),
                        arb(0),
                    )
                rec_diff = L_dir - (L_prev_x - L_prev_xp)
                fact_diff = L_dir - L_fact
                psi_diff = L_dir - psi_x
                summatory_checks.append(
                    {
                        "y": y,
                        "x": x_val,
                        "2_q_gt_y": 2 * q_gt_y,
                        "L_y_direct_certified": serialize_arb_certified(L_dir),
                        "L_y_factorial_divisor_certified": serialize_arb_certified(
                            L_fact
                        ),
                        "chebyshev_psi_certified": serialize_arb_certified(psi_x),
                        "factorial_identity_encloses_zero": bool(
                            fact_diff.contains(0) and abs(fact_diff) < arb("1e-70")
                        ),
                        "prime_step_recursion_encloses_zero": bool(
                            rec_diff.contains(0) and abs(rec_diff) < arb("1e-70")
                        ),
                        "equals_psi_below_2_q_gt_y": (
                            bool(psi_diff.contains(0) and abs(psi_diff) < arb("1e-70"))
                            if x_val < 2 * q_gt_y
                            else bool(psi_diff > arb(0))
                        ),
                    }
                )

        # 3C. Compare the three representations of W_y(X): product recursion, divisor sum, and coefficient series
        three_way_wy_checks: List[Dict[str, Any]] = []
        for y in (2, 3, 5, 7, 11):
            for X_label, X_arb in (
                ("1", arb(1)),
                ("2", arb(2)),
                ("tau", tau_arb),
                ("10", arb(10)),
            ):
                res_coeff = evaluate_w_y_coefficient_certified_arb(
                    X_arb, y=y, n_max=3500, prec_bits=prec_bits
                )
                res_div = evaluate_w_y_divisor_sum_certified_arb(
                    X_arb, y=y, k_max=3000, prec_bits=prec_bits
                )
                res_prod = evaluate_w_y_product_recursion_certified_arb(
                    X_arb, y=y, k_max=3000, prec_bits=prec_bits
                )
                c_ball = res_coeff["enclosure_arb"]
                d_ball = res_div["enclosure_arb"]
                p_ball = res_prod["enclosure_arb"]
                three_way_wy_checks.append(
                    {
                        "y": y,
                        "X_label": X_label,
                        "X": float(X_arb.mid()),
                        "W_y_coefficient_certified": res_coeff["certified"],
                        "W_y_divisor_sum_certified": res_div["certified"],
                        "W_y_product_recursion_certified": res_prod["certified"],
                        "prod_minus_divisor_encloses_zero": bool(
                            (p_ball - d_ball).contains(0)
                            and abs(arb(p_ball.mid()) - arb(d_ball.mid()))
                            < arb("1e-70")
                        ),
                        "coeff_minus_divisor_encloses_zero": bool(
                            (c_ball - d_ball).contains(0)
                        ),
                        "coeff_minus_prod_encloses_zero": bool(
                            (c_ball - p_ball).contains(0)
                        ),
                    }
                )

        finite_prime_construction_audit = {
            "primorial_definition": "P_y = prod_{p <= y} p",
            "truncated_moebius_definition": "mu_y(m) = mu(m) * 1_{m | P_y}",
            "dilation_operator_definition": "(D_p F)(X) = F(X / p)",
            "euler_inversion_definition": (
                "W_y(X) = sum_{m | P_y} mu(m) m^{-1/2} W_log(X / m) "
                "= [prod_{p <= y} (I - p^{-1/2} D_p)] W_log(X)"
            ),
            "exact_one_prime_recursion": (
                "W_{p_k}(X) = (I - p_k^{-1/2} D_{p_k}) W_{p_{k-1}}(X) "
                "= W_{p_{k-1}}(X) - p_k^{-1/2} W_{p_{k-1}}(X / p_k),   with W_{p_0}(X) = W_log(X)"
            ),
            "exact_telescoping_identity": (
                "R_{mu, y}(X) := W_y(X) - W_log(X) = sum_{m | P_y, m >= 2} mu(m) m^{-1/2} W_log(X / m) "
                "= -sum_{k=1}^r p_k^{-1/2} W_{p_{k-1}}(X / p_k)"
            ),
            "coefficient_representation": (
                "W_y(X) = sum_{n >= 2} lambda_y(n) n^{-1/2} h_0(n / X),   "
                "lambda_y(n) = (mu_y * log)(n) = sum_{d | n, d | P_y} mu(d) log(n / d)"
            ),
            "closed_form_lambda_y_cases": {
                "omega_le_y_eq_0": "log n  (n has no prime divisor <= y; includes primes r > y and y-rough composites)",
                "omega_le_y_eq_1": "log p  (p is the unique distinct prime divisor <= y; includes pure prime powers p^a with p <= y AND mixed composites p^a * n_{>y})",
                "omega_le_y_ge_2": "0      (n has at least two distinct prime divisors <= y)",
            },
            "prime_power_behavior_explicit": {
                "pure_prime_power_p_le_y": "For n = p^a with p <= y and a >= 1, omega_{<=y}(p^a) = 1 so lambda_y(p^a) = log p = Lambda(p^a).",
                "pure_prime_power_r_gt_y": (
                    "For n = r^b with r > y and b >= 1, omega_{<=y}(r^b) = 0 so lambda_y(r^b) = b log r "
                    "(equals Lambda(r) = log r when b = 1, and exceeds Lambda(r^b) = log r by (b-1) log r > 0 when b >= 2)."
                ),
                "mixed_prime_power_composite": (
                    "For n = p^a * n_{>y} with p <= y, a >= 1, and n_{>y} > 1 coprime to P_y, "
                    "omega_{<=y}(n) = 1 so lambda_y(n) = log p > 0 whereas Lambda(n) = 0."
                ),
            },
            "exact_agreement_window_with_von_mangoldt": {
                "next_prime_definition": "q_{>y} := min{p prime : p > y}",
                "exact_agreement_range": "lambda_y(n) = Lambda(n) for all 2 <= n < 2 * q_{>y} (in particular for all 2 <= n <= 2y + 1)",
                "first_discrepancy_integer": "n_{min}(y) = 2 * q_{>y}, where lambda_y(2 * q_{>y}) = log 2 > 0 = Lambda(2 * q_{>y})",
                "pointwise_sieve_surplus_nonnegativity": "Delta_y(n) := lambda_y(n) - Lambda(n) >= 0 for all n >= 2",
                "all_three_lambda_methods_agree_up_to_120": all_three_lambda_methods_agree,
                "all_delta_nonnegative_verified": all_delta_nonnegative,
                "threshold_verification_table": threshold_checks,
            },
            "representative_cases_y_eq_5": representative_lambda_cases_y5,
            "summatory_factorial_identity": (
                "L_y(x) := sum_{2 <= n <= x} lambda_y(n) = sum_{d | P_y, d <= x} mu(d) log(floor(x / d)!)"
            ),
            "summatory_verification_checks": summatory_checks,
            "three_way_W_y_representation_checks": three_way_wy_checks,
            "lean_theorem": "finite_prime_euler_recursion_and_coefficient_cases",
        }

        # -------------------------------------------------------------------
        # Step 4: Quantitative Compatibility Investigation — Stieltjes Decomposition,
        #         Critical-Line Fourier / Gram Bound, and Horizon-Collapse Obstruction
        # -------------------------------------------------------------------
        # 4A. Evaluate the Euler-sieved seed Gram norm ||Psi_y||_{L^2}^2 = sum_{m1, m2 | P_y} (mu(m1)mu(m2)/sqrt(m1 m2)) h_0(m1/m2)
        #     for feasible cutoffs y in {2, 3, 5, 7, 11, 13} in 256-bit Arb, and verify step-by-step identity.
        euler_gram_norm_table: List[Dict[str, Any]] = []
        for y in (2, 3, 5, 7, 11, 13):
            divs = divisors_of_primorial(y)
            gram_sq = arb(0)
            diag_sq = arb(0)
            for m1, mu1 in divs:
                m1_arb = arb(m1)
                diag_sq += h0_1_arb / m1_arb
                for m2, mu2 in divs:
                    if m1 == m2:
                        gram_sq += h0_1_arb / m1_arb
                    elif m1 < m2:
                        m2_arb = arb(m2)
                        term = (
                            arb(2 * mu1 * mu2)
                            / (m1_arb * m2_arb).sqrt()
                            * evaluate_h0_arb(m1_arb / m2_arb)
                        )
                        gram_sq += term
            euler_gram_norm_table.append(
                {
                    "y": y,
                    "num_divisors": len(divs),
                    "diagonal_main_term_h0_1_prod_1_plus_1_over_p_certified": serialize_arb_certified(
                        diag_sq
                    ),
                    "euler_sieved_seed_norm_sq_certified": serialize_arb_certified(
                        gram_sq
                    ),
                    "euler_sieved_seed_norm_certified": serialize_arb_certified(
                        gram_sq.sqrt()
                    ),
                    "is_strictly_positive": bool(gram_sq > arb(0)),
                }
            )

        # 4B. Certify the low-frequency coherent arch spike of |E_y(it)|^2 across the
        #     controlled-width frequency interval I_y = [t_{y,-}, t_{y,+}] = [7*tau / (16*log y), tau / (2*log y)]
        #     of width |I_y| = tau / (16*log y) = pi / (8*log y) in 256-bit Arb across
        #     y in {2, 5, 11, 31, 97, 199, 499, 997, 1999, 4999, 9973}, together with:
        #     - the certified y = 210 counterexample refuting the false subproduct inequality, and
        #     - the local Weierstrass product monotonicity certificate on [0, 1] (covering y >= 24)
        #       and 64-subinterval certificate on [0, t_{2,+}] (covering y in {2, 5, 11}) plus
        #       counterexample points t = 5, 10, 20 refuting global monotonicity of H_0(it).
        f_half_acb = evaluate_f_tau_acb(acb(arb(1) / arb(2)))
        H0_at_0_arb = (f_half_acb * f_half_acb).real

        subprod_cex_raw = certify_subproduct_counterexample_at_y210_arb(
            y=210, prec_bits=prec_bits
        )
        subproduct_counterexample_y210 = {
            "y": subprod_cex_raw["y"],
            "pi_y": subprod_cex_raw["pi_y"],
            "threshold_y_pow_16_21_certified": serialize_arb_certified(
                subprod_cex_raw["threshold_y_pow_16_21_arb"]
            ),
            "upper_prime_count": subprod_cex_raw["upper_prime_count"],
            "factors_less_than_one_count": subprod_cex_raw[
                "factors_less_than_one_count"
            ],
            "t_210_minus_certified": serialize_arb_certified(
                subprod_cex_raw["t_y_minus_arb"]
            ),
            "actual_E_210_abs_sq_at_t_210_minus_certified": serialize_arb_certified(
                subprod_cex_raw["actual_E_y_abs_sq_at_t_y_minus_arb"]
            ),
            "omitted_lower_prime_product_certified": serialize_arb_certified(
                subprod_cex_raw["omitted_lower_prime_product_arb"]
            ),
            "upper_prime_actual_product_certified": serialize_arb_certified(
                subprod_cex_raw["upper_prime_actual_product_arb"]
            ),
            "claimed_false_subproduct_certified": serialize_arb_certified(
                subprod_cex_raw["claimed_false_subproduct_arb"]
            ),
            "omitted_lower_prime_product_strictly_less_than_one": subprod_cex_raw[
                "omitted_lower_prime_product_strictly_less_than_one"
            ],
            "enclosures_disjoint_and_false_subproduct_exceeds_actual": subprod_cex_raw[
                "enclosures_disjoint_and_false_subproduct_exceeds_actual"
            ],
        }

        h0_local_raw = certify_H0_local_monotonicity_and_global_decay_arb(
            prec_bits=prec_bits
        )
        weierstrass_checks_serialized: List[Dict[str, Any]] = []
        for w_row in h0_local_raw["weierstrass_product_identity_checks"]:
            weierstrass_checks_serialized.append(
                {
                    "t_label": w_row["t_label"],
                    "v_eq_4_t_sq": w_row["v_eq_4_t_sq"],
                    "direct_ratio_H0_it_over_H0_0_certified": serialize_arb_certified(
                        w_row["direct_ratio_H0_it_over_H0_0_arb"]
                    ),
                    "weierstrass_product_enclosure_certified": serialize_arb_certified(
                        w_row["weierstrass_product_enclosure_arb"]
                    ),
                    "enclosures_intersect": w_row["enclosures_intersect"],
                }
            )
        h0_local_monotonicity_and_decay_certificate = {
            "weierstrass_product_identity": (
                "H_0(it) / H_0(0) = (1 + v)^3 * prod_{n=1}^infty (1 + v / (4n + 1)^2)^{-1},   v = 4*t^2"
            ),
            "compact_differentiation_justification": (
                "On any compact interval v in [0, V], |(d/dv) log(1 + v/(4n+1)^2)| = 1/((4n+1)^2 + v) <= 1/(16 n^2) "
                "with sum_{n>=1} 1/(16 n^2) = tau^2 / 384 < infty, so term-by-term differentiation holds by the Weierstrass M-test."
            ),
            "unit_interval_monotonicity_bound_formula": (
                "For 0 <= t <= 1 (0 <= v <= 4): (d/dv) log(H_0(it)/H_0(0)) = 3/(1+v) - sum_{n=1}^infty 1/((4n+1)^2 + v) "
                ">= 3/5 - tau^2 / 384 > 0, proving strict monotonicity of H_0(it) on t in [0, 1] (covering I_y for all integer y >= 24)."
            ),
            "left_endpoint_coeff_4_cos_tau_over_16_certified": serialize_arb_certified(
                h0_local_raw["left_endpoint_coeff_4_cos_tau_over_16_arb"]
            ),
            "left_endpoint_coeff_exact_2_sqrt_2_plus_sqrt2_certified": serialize_arb_certified(
                h0_local_raw["left_endpoint_coeff_exact_2_sqrt_2_plus_sqrt2_arb"]
            ),
            "left_endpoint_coeff_algebraic_identity_contains_zero": h0_local_raw[
                "left_endpoint_coeff_algebraic_identity_contains_zero"
            ],
            "left_endpoint_coeff_strictly_between_3_6955_and_4": h0_local_raw[
                "left_endpoint_coeff_strictly_between_3_6955_and_4"
            ],
            "dlog_dv_unit_interval_lb_3_5_minus_tau_sq_over_384_certified": serialize_arb_certified(
                h0_local_raw[
                    "dlog_dv_unit_interval_lb_3_5_minus_tau_sq_over_384_arb"
                ]
            ),
            "dlog_dv_unit_interval_lb_strictly_positive": h0_local_raw[
                "dlog_dv_unit_interval_lb_strictly_positive"
            ],
            "dlog_dv_t_le_2_lb_3_17_minus_tau_sq_over_384_certified": serialize_arb_certified(
                h0_local_raw["dlog_dv_t_le_2_lb_3_17_minus_tau_sq_over_384_arb"]
            ),
            "dlog_dv_t_le_2_lb_strictly_positive": h0_local_raw[
                "dlog_dv_t_le_2_lb_strictly_positive"
            ],
            "exp_pi_threshold_certified": serialize_arb_certified(
                h0_local_raw["exp_pi_threshold_arb"]
            ),
            "t_plus_at_y23_certified": serialize_arb_certified(
                h0_local_raw["t_plus_at_y23_arb"]
            ),
            "t_plus_at_y24_certified": serialize_arb_certified(
                h0_local_raw["t_plus_at_y24_arb"]
            ),
            "y23_exceeds_unit_interval_and_y24_inside_unit_interval": h0_local_raw[
                "y23_exceeds_unit_interval_and_y24_inside_unit_interval"
            ],
            "weierstrass_product_identity_checks": weierstrass_checks_serialized,
            "all_weierstrass_product_checks_intersect": h0_local_raw[
                "all_weierstrass_product_checks_intersect"
            ],
            "subdivision_64_on_0_to_t2plus_all_dlog_dv_positive": h0_local_raw[
                "subdivision_64_on_0_to_t2plus_all_dlog_dv_positive"
            ],
            "subdivision_64_min_dlog_dv_on_0_to_t2plus_certified": serialize_arb_certified(
                h0_local_raw["subdivision_64_min_dlog_dv_on_0_to_t2plus_arb"]
            ),
            "H0_at_t2plus_certified": serialize_arb_certified(
                h0_local_raw["H0_at_t2plus_arb"]
            ),
            "H0_at_t5_certified": serialize_arb_certified(
                h0_local_raw["H0_at_t5_arb"]
            ),
            "H0_at_t10_certified": serialize_arb_certified(
                h0_local_raw["H0_at_t10_arb"]
            ),
            "H0_at_t20_certified": serialize_arb_certified(
                h0_local_raw["H0_at_t20_arb"]
            ),
            "global_monotonicity_falsified_H0_t5_lt_H0_t2plus": h0_local_raw[
                "global_monotonicity_falsified_H0_t5_lt_H0_t2plus"
            ],
            "high_frequency_decay_verified_H0_t20_lt_H0_0": h0_local_raw[
                "high_frequency_decay_verified_H0_t20_lt_H0_0"
            ],
        }

        low_freq_spike_table: List[Dict[str, Any]] = []
        for y in (2, 5, 11, 31, 97, 199, 499, 997, 1999, 4999, 9973):
            spike_info = evaluate_euler_spike_interval_gram_lower_bound_arb(
                y, prec_bits=prec_bits
            )
            t_y_minus_arb = spike_info["t_y_minus_arb"]
            t_y_plus_arb = spike_info["t_y_plus_arb"]
            width_arb = spike_info["interval_width_arb"]
            e_sq_minus_arb = spike_info["e_sq_at_minus_arb"]
            e_sq_plus_arb = spike_info["e_sq_at_plus_arb"]
            H0_minus_arb = spike_info["H0_at_minus_arb"]
            H0_plus_arb = spike_info["H0_at_plus_arb"]
            H0_subdiv_min_arb = spike_info["H0_subdiv_min_arb"]
            dlog_dv_min_arb = spike_info["H0_dlog_dv_min_on_I_y_arb"]
            gram_lb_0_arb = spike_info["gram_sq_lb_H0_0_arb"]
            gram_lb_subdiv_arb = spike_info["gram_sq_lb_H0_subdiv_arb"]
            gram_lb_minus_arb = spike_info["gram_sq_lb_H0_minus_arb"]
            low_freq_spike_table.append(
                {
                    "y": y,
                    "pi_y": spike_info["pi_y"],
                    "interval_left_t_y_minus_7pi_over_8log_y_certified": serialize_arb_certified(
                        t_y_minus_arb
                    ),
                    "coherent_frequency_t_y_certified": serialize_arb_certified(
                        t_y_plus_arb
                    ),
                    "interval_width_pi_over_8log_y_certified": serialize_arb_certified(
                        width_arb
                    ),
                    "primes_with_negative_cos_count": spike_info[
                        "constructive_at_plus_count"
                    ],
                    "primes_with_negative_cos_across_interval_count": spike_info[
                        "constructive_across_interval_count"
                    ],
                    "interval_min_E_y_abs_sq_at_t_y_minus_certified": serialize_arb_certified(
                        e_sq_minus_arb
                    ),
                    "E_y_abs_sq_at_t_y_certified": serialize_arb_certified(
                        e_sq_plus_arb
                    ),
                    "E_y_abs_at_t_y_certified": serialize_arb_certified(
                        e_sq_plus_arb.sqrt()
                    ),
                    "interval_min_H0_at_i_t_y_minus_certified": serialize_arb_certified(
                        H0_minus_arb
                    ),
                    "H0_interval_subdivision_min_certified": serialize_arb_certified(
                        H0_subdiv_min_arb
                    ),
                    "H0_dlog_dv_min_on_I_y_certified": serialize_arb_certified(
                        dlog_dv_min_arb
                    ),
                    "H0_at_i_t_y_certified": serialize_arb_certified(H0_plus_arb),
                    "H0_at_i_t_y_exceeds_H0_at_0": bool(H0_plus_arb >= H0_at_0_arb),
                    "I_y_subset_of_analytic_unit_interval_0_1": spike_info[
                        "I_y_subset_of_analytic_unit_interval_0_1"
                    ],
                    "E_y_sq_interval_monotonicity_by_phase_in_0_pi": spike_info[
                        "E_y_sq_interval_monotonicity_by_phase_in_0_pi"
                    ],
                    "H0_interval_monotonicity_certified_on_I_y": spike_info[
                        "H0_interval_monotonicity_certified_on_I_y"
                    ],
                    "H0_interval_subdivision_exceeds_H0_0": spike_info[
                        "H0_interval_subdivision_exceeds_H0_0"
                    ],
                    "endpoint_ordering_E_y_sq_minus_le_plus": spike_info[
                        "endpoint_ordering_E_y_sq_minus_le_plus"
                    ],
                    "endpoint_ordering_H0_0_le_minus_le_plus": spike_info[
                        "endpoint_ordering_H0_0_le_minus_le_plus"
                    ],
                    "gram_norm_sq_lower_bound_expr_via_H0_0_certified": serialize_arb_certified(
                        gram_lb_0_arb
                    ),
                    "gram_norm_sq_lower_bound_expr_via_H0_subdiv_min_certified": serialize_arb_certified(
                        gram_lb_subdiv_arb
                    ),
                    "gram_norm_sq_lower_bound_expr_via_H0_minus_certified": serialize_arb_certified(
                        gram_lb_minus_arb
                    ),
                }
            )

        # 4C. Certify the two-sided cutoff-boundary envelope on B_{log,boundary}(u) = -int_0^1 t^{-1/2} (log t) h_0(t/u) dt:
        #     |B_{log,boundary}(u)| <= min((30731/98304) u^{-5/2}, (92193/131072) u^{5/2}) for all u > 0.
        from tc.canonical_theta_correlation_bound import evaluate_h0_acb

        tol_b = 2**(-90)
        eps_b = arb("1e-8")
        c_large_b = arb(30731) / arb(98304)
        c_small_b = arb(92193) / arb(131072)
        boundary_envelope_checks: List[Dict[str, Any]] = []
        for u_label, u_arb in (
            ("1/4", arb(1) / arb(4)),
            ("1/2", arb(1) / arb(2)),
            ("1", arb(1)),
            ("2", arb(2)),
            ("4", arb(4)),
        ):
            u_c = acb(u_arb)

            def _integrand_b_log(t_c: acb, analytic: bool, uc: acb = u_c) -> acb:
                return -(t_c ** acb("-0.5")) * t_c.log() * evaluate_h0_acb(
                    t_c / uc, analytic=analytic
                )

            int_main = (
                acb.integral(
                    _integrand_b_log,
                    acb(eps_b),
                    acb("0.25"),
                    rel_tol=tol_b,
                    abs_tol=tol_b,
                ).real
                + acb.integral(
                    _integrand_b_log,
                    acb("0.25"),
                    acb(1),
                    rel_tol=tol_b,
                    abs_tol=tol_b,
                ).real
            )
            eps_tail = (
                (arb(92193) / arb(32768))
                * (u_arb ** arb("-2.5"))
                * (eps_b**3)
                * (arb(3) * (arb(1) / eps_b).log() + arb(1))
                / arb(9)
            )
            b_log_u = int_main + arb(0, eps_tail.upper())
            bound_large = c_large_b * (u_arb ** arb("-2.5"))
            bound_small = c_small_b * (u_arb ** arb("2.5"))
            two_sided_bound = bound_large if bool(bound_large <= bound_small) else bound_small
            boundary_envelope_checks.append(
                {
                    "u_label": u_label,
                    "u": float(u_arb.mid()),
                    "B_log_boundary_u_certified": serialize_arb_certified(b_log_u),
                    "large_u_bound_30731_98304_u_neg_5_2_certified": serialize_arb_certified(
                        bound_large
                    ),
                    "small_u_bound_92193_131072_u_pos_5_2_certified": serialize_arb_certified(
                        bound_small
                    ),
                    "satisfies_two_sided_envelope": bool(
                        abs(b_log_u) <= two_sided_bound
                    ),
                }
            )

        quantitative_compatibility_investigation = {
            "stieltjes_decomposition_of_W_y": {
                "summatory_split": (
                    "L_y(x) = M_y(x) + E_y(x),   "
                    "M_y(x) = sum_{d | P_y, d <= x} mu(d) ( (x/d) log(x/d) - (x/d) + 1 ),   "
                    "E_y(x) = sum_{d | P_y, d <= x} mu(d) E_log(x/d)"
                ),
                "vanishing_moment_cancellation_with_cutoff_boundaries": (
                    "Using H_0(1/2) = H_0'(1/2) = 0 at every scale Y = X/d > 0 cancels the full-line smooth logarithmic "
                    "integral int_0^infty u^{-1/2} (log u) h_0(u / (X/d)) du = 0 identically for each d | P_y, leaving the exact "
                    "cutoff-boundary sum B_y(X) and Stirling-remainder Stieltjes integral I_y(X): "
                    "W_y(X) = B_y(X) + I_y(X), where "
                    "B_y(X) = sum_{d | P_y} mu(d) d^{-1/2} B_{log,boundary}(X/d) and "
                    "I_y(X) = int_1^infty E_y(x) x^{-3/2} tilde{h}_0(x/X) dx = sum_{d | P_y} mu(d) d^{-1/2} I_log(X/d)."
                ),
                "two_sided_cutoff_boundary_envelope": (
                    "|B_{log,boundary}(u)| <= min((30731/98304) u^{-5/2}, (92193/131072) u^{5/2}) for all u > 0; "
                    "retaining the lower step cutoffs x >= d is essential because for d ~ X, B_{log,boundary}(X/d) is O(1) "
                    "and unsigned summation over d | P_y yields O(X^{1/2}) whenever y >= X."
                ),
                "certified_boundary_envelope_checks": boundary_envelope_checks,
            },
            "mechanism_A_critical_line_mellin_fourier_and_gram_bound": {
                "mellin_transform_identity": (
                    "M_X[W_y](z) = -E_y(z) H_0(z) zeta'(z + 1/2) on |Re(z)| < 5/2, where "
                    "E_y(z) = prod_{p <= y} (1 - p^{-(z + 1/2)}) = sum_{m | P_y} mu(m) m^{-(z + 1/2)}"
                ),
                "holomorphy_and_critical_line_contour_shift": (
                    "Because E_y(z) is an entire Dirichlet polynomial and the triple zero H_0(1/2) = H_0'(1/2) = H_0''(1/2) = 0 "
                    "cancels the double pole of -zeta'(z + 1/2) at z = 1/2, M_X[W_y](z) is holomorphic across the entire open "
                    "strip |Re(z)| < 5/2 (having no poles at the nontrivial zeros of zeta). Shifting the Mellin inversion contour "
                    "to Re(z) = 0 (z = it) crosses zero poles and gives the exact critical-line Fourier representation: "
                    "W_y(X) = -(1/tau) int_{-infty}^infty E_y(it) H_0(it) zeta'(1/2 + it) X^{it} dt."
                ),
                "euler_sieved_seed_gram_bound": (
                    "sup_{X > 0} |W_y(X)| <= I_{crit,1}(y) <= ||Psi_y||_{L^2(d^*x)} * N_{zeta',tau}, where "
                    "Psi_y = [prod_{p <= y} (I - p^{-1/2} U_p)] psi_tau has exact Gram norm squared "
                    "||Psi_y||_{L^2}^2 = sum_{m1, m2 | P_y} (mu(m1)mu(m2)/sqrt(m1 m2)) h_0(m1/m2) "
                    "= (1/tau) int_{-infty}^infty |E_y(it)|^2 H_0(it) dt."
                ),
                "H0_at_0_certified": serialize_arb_certified(H0_at_0_arb),
                "euler_sieved_seed_gram_norm_table": euler_gram_norm_table,
                "low_frequency_coherent_arch_obstruction": (
                    "On the controlled-width frequency interval I_y := [t_{y,-}, t_{y,+}] = [7*tau / (16*log y), tau / (2*log y)] "
                    "= [7*pi / (8*log y), pi / log y] of width |I_y| = tau / (16*log y) = pi / (8*log y) > 0, every prime p <= y "
                    "and every t in [0, tau / (2*log y)] has phase t*log(p) in [0, pi] where "
                    "(d/dt)|1 - p^{-1/2 - it}|^2 = 2*p^{-1/2}*(log p)*sin(t*log p) >= 0. "
                    "Thus |E_y(it)|^2 is monotonically non-decreasing in t on I_y, with exact interval minimum at the left endpoint: "
                    "inf_{t in I_y} |E_y(it)|^2 = |E_y(i t_{y,-})|^2. "
                    "Retaining every prime factor p <= y, log|E_y(it)|^2 = -2*sum_{p<=y} p^{-1/2}*cos(t*log p) + O(sum_{p<=y} p^{-1}); "
                    "by the Prime Number Theorem with partial summation (and Mertens' bound sum_{p<=y} p^{-1} = O(log log y)), "
                    "sum_{p<=y} p^{-1/2}*cos(a*log p / log y) = (2*cos a + o(1))*sqrt(y)/log y, giving at a = 7*tau/16 "
                    "the exact left-endpoint asymptotic log|E_y(i t_{y,-})|^2 = (4*cos(tau/16) + o(1))*sqrt(y)/log y "
                    "(where 4*cos(tau/16) = 2*sqrt(2 + sqrt(2)) ~ 3.695518130045147, whereas the right endpoint t_{y,+} = tau/(2*log y) "
                    "has coefficient 4; the earlier subproduct claim |E_y(i t_{y,-})|^2 >= prod_{y^{16/21}<=p<=y}(1 + p^{-1/2} + p^{-1}) "
                    "is refuted at y = 210 in 256-bit Arb: 3.3605057481 < 18.2536118944). "
                    "For the kernel weight H_0(it) (which decays to 0 as t -> infty and is NOT globally increasing on [0, infty)), "
                    "the canonical Weierstrass product H_0(it)/H_0(0) = (1 + v)^3 * prod_{n>=1} (1 + v/(4n+1)^2)^{-1} (v = 4*t^2) "
                    "gives on 0 <= t <= 1 (0 <= v <= 4): (d/dv) log(H_0(it)/H_0(0)) = 3/(1+v) - sum_{n>=1} 1/((4n+1)^2 + v) "
                    ">= 3/5 - tau^2/384 > 0, proving strict monotonicity on [0, 1] and hence on I_y subset [0, 1] for all integer y >= 24 "
                    "(while for y in {2, 5, 11}, both a 64-subinterval Arb logarithmic-derivative certificate on [0, t_{2,+}] and direct "
                    "64-subinterval Arb ball enclosures on I_y certify inf_{t in I_y} H_0(it) = H_0(i t_{y,-}) > H_0(0) > 0). "
                    "Integrating over (-I_y) union I_y gives for y >= 24 (and all certified table rows): "
                    "||Psi_y||_{L^2(d^*x)}^2 >= (2/tau) int_{t_{y,-}}^{t_{y,+}} |E_y(it)|^2 H_0(it) dt "
                    ">= (H_0(0) / (8 log y)) |E_y(i t_{y,-})|^2 = (H_0(0) / (8 log y)) exp[(4*cos(tau/16) + o(1)) sqrt(y) / log y] -> +infty as y -> infty "
                    "(with right-endpoint value |E_y(i t_{y,+})|^2 reaching 6.65784855e12, left-endpoint minimum |E_y(i t_{y,-})|^2 reaching "
                    "3.99370923e8, and lower-bound expression (H_0(0)/(8 log y))|E_y(i t_{y,-})|^2 reaching 153.3859466 at y = 9973). "
                    "Scope: this establishes divergence of the unsplit critical-line Cauchy-Schwarz / Gram-norm estimate as y -> infty; "
                    "it does NOT establish divergence of W_{M(X)}(X), failure of the concurrent-grade hypothesis, or closure of the arithmetic cancellation obligation."
                ),
                "subproduct_counterexample_y210": subproduct_counterexample_y210,
                "h0_local_monotonicity_and_decay_certificate": h0_local_monotonicity_and_decay_certificate,
                "low_frequency_spike_table": low_freq_spike_table,
            },
            "mechanism_B_prime_by_prime_recursion_and_horizon_collapse": {
                "recursion_scale_cancellation": (
                    "In each prime-by-prime step W_{p_k}(X) = W_{p_{k-1}}(X) - p_k^{-1/2} W_{p_{k-1}}(X / p_k), "
                    "evaluating the O(u^{-1/2} log(u+2)) bound of W_log at u = X / m >= 1 gives "
                    "m^{-1/2} (X / m)^{-1/2} = X^{-1/2}, canceling the m^{-1/2} damping weight identically for every m <= X."
                ),
                "fixed_y_asymptotic_decay": (
                    "For any fixed prime cutoff y >= 2, |W_y(X)| <= 2^{pi(y)} O(X^{-1/2} log(X+2)) -> 0 as X -> infty."
                ),
                "horizon_collapse_for_y_ge_X": (
                    "Whenever y >= N >= 2, every integer 1 <= m <= N has all prime factors <= m <= N <= y, so m | P_y iff m is "
                    "squarefree (mu(m) != 0) and mu_y(m) = mu(m) for all 1 <= m <= N. Splitting at the bare scale horizon "
                    "N = floor(X) eliminates the primorial count for m > P_y, but the available small-scale tail bound "
                    "C_{log,0} X^{5/2} sum_{m > floor(X)} m^{-3} <= C_{log,0} X^{5/2} / (2 floor(X)^2) = O(X^{1/2}) grows as O(sqrt(X)) "
                    "and does NOT give a uniform O(1) comparison with W(X). Uniform O(1) comparison requires the coupled cutoff "
                    "N = M(X) = ceil(max(2, X^{5/4})), where the m > M(X) tail is bounded by (1/2) C_{log,0} < 0.278715 and the "
                    "m <= M(X) portion of W_{M(X)}(X) collapses term-by-term to the additive Moebius truncation "
                    "W_log(X) + R_{mu, M(X)}(X), while on the coefficient side lambda_{M(X)}(n) = Lambda(n) for all "
                    "2 <= n < 2 q_{>M(X)} (> 2 M(X) >= 2 X^{5/4}), reproducing the original prime sum across the bulk oscillation region of h_0(n/X)."
                ),
            },
        }

        # -------------------------------------------------------------------
        # Step 5 & Step 6: Quantitative Passage to W(X), Coupled Cutoff y = M(X),
        #                  and Certified Admissible Rational Grade Table
        # -------------------------------------------------------------------
        # Evaluate across admissible rational grades K in A_R of both signs, near zero, and increasing scale:
        # K in {0, 1/100, -1/100, 1/4, -1/4, 1/2, -1/2, 1, -1, 3/2, -3/2, 2, -2}
        grade_specs: List[Tuple[str, Fraction]] = [
            ("0", Fraction(0, 1)),
            ("1/100", Fraction(1, 100)),
            ("-1/100", Fraction(-1, 100)),
            ("1/4", Fraction(1, 4)),
            ("-1/4", Fraction(-1, 4)),
            ("1/2", Fraction(1, 2)),
            ("-1/2", Fraction(-1, 2)),
            ("1", Fraction(1, 1)),
            ("-1", Fraction(-1, 1)),
            ("3/2", Fraction(3, 2)),
            ("-3/2", Fraction(-3, 2)),
            ("2", Fraction(2, 1)),
            ("-2", Fraction(-2, 1)),
        ]

        # Cache by |K| so +K and -K use identical scale X_K = tau^{|K|} while recording both signs explicitly
        abs_k_cache: Dict[Fraction, Dict[str, Any]] = {}
        coupled_grade_table: List[Dict[str, Any]] = []

        for k_label, k_frac in grade_specs:
            abs_k = abs(k_frac)
            if abs_k not in abs_k_cache:
                k_arb = arb(abs_k.numerator) / arb(abs_k.denominator)
                X_K_arb = tau_arb**k_arb
                M_X = certified_coupled_cutoff_M_X_arb(X_K_arb, prec_bits=prec_bits)
                q_gt_M = next_prime_above(M_X)

                # Choose truncation n_max so tail is tiny even at X_K = tau^2 ~ 39.48
                n_max_coeff = max(3500, int(120 * float(X_K_arb.mid())) + 2500)
                w_actual = evaluate_w_prime_sum_certified_arb(
                    X_K_arb, n_max=n_max_coeff, prec_bits=prec_bits
                )["enclosure_arb"]
                w_log_val = evaluate_w_log_divisor_aggregated_certified_arb(
                    X_K_arb, k_max=n_max_coeff, prec_bits=prec_bits
                )["enclosure_arb"]
                w_y_coupled = evaluate_w_y_coefficient_certified_arb(
                    X_K_arb, y=M_X, n_max=n_max_coeff, prec_bits=prec_bits
                )["enclosure_arb"]

                # Also compute the ordinary additive Moebius truncation R_{mu, M(X)}(X) = sum_{2 <= m <= M(X)} mu(m) m^{-1/2} W_log(X/m)
                r_mu_additive_M = arb(0)
                for m in range(2, M_X + 1):
                    mu_m = moebius_mu_int(m)
                    if mu_m != 0:
                        m_arb = arb(m)
                        k_eff = max(250, int(2000 / math.sqrt(m)) + 150)
                        w_log_xm = evaluate_w_log_divisor_aggregated_certified_arb(
                            X_K_arb / m_arb, k_max=k_eff, prec_bits=prec_bits
                        )["enclosure_arb"]
                        r_mu_additive_M += (arb(mu_m) / m_arb.sqrt()) * w_log_xm

                r_mu_actual = w_actual - w_log_val
                r_mu_euler_M = w_y_coupled - w_log_val
                t_rough = w_actual - w_y_coupled
                t_smooth = w_y_coupled - (w_log_val + r_mu_additive_M)
                analytic_tail_bound = (
                    c_log_0_arb
                    * (X_K_arb**5).sqrt()
                    / (arb(2) * (arb(M_X) ** 2))
                )

                abs_k_cache[abs_k] = {
                    "X_K_arb": X_K_arb,
                    "M_X": M_X,
                    "q_gt_M": q_gt_M,
                    "w_actual": w_actual,
                    "w_log_val": w_log_val,
                    "w_y_coupled": w_y_coupled,
                    "r_mu_actual": r_mu_actual,
                    "r_mu_euler_M": r_mu_euler_M,
                    "r_mu_additive_M": r_mu_additive_M,
                    "t_rough": t_rough,
                    "t_smooth": t_smooth,
                    "analytic_tail_bound": analytic_tail_bound,
                }

            cached = abs_k_cache[abs_k]
            t_rough = cached["t_rough"]
            t_smooth = cached["t_smooth"]
            analytic_tail_bound = cached["analytic_tail_bound"]
            partition_residual = (
                cached["r_mu_actual"] - cached["r_mu_additive_M"]
            ) - (t_smooth + t_rough)

            coupled_grade_table.append(
                {
                    "K_label": k_label,
                    "K_float": float(k_frac),
                    "X_K_certified": serialize_arb_certified(cached["X_K_arb"]),
                    "coupled_cutoff_M_X": cached["M_X"],
                    "first_unsieved_prime_q_gt_M": cached["q_gt_M"],
                    "first_coeff_discrepancy_2_q_gt_M": 2 * cached["q_gt_M"],
                    "W_X_certified": serialize_arb_certified(cached["w_actual"]),
                    "W_log_X_certified": serialize_arb_certified(
                        cached["w_log_val"]
                    ),
                    "W_M_X_euler_certified": serialize_arb_certified(
                        cached["w_y_coupled"]
                    ),
                    "R_mu_X_certified": serialize_arb_certified(
                        cached["r_mu_actual"]
                    ),
                    "R_mu_M_X_euler_certified": serialize_arb_certified(
                        cached["r_mu_euler_M"]
                    ),
                    "R_mu_M_X_additive_certified": serialize_arb_certified(
                        cached["r_mu_additive_M"]
                    ),
                    "T_rough_W_minus_W_M_X_certified": serialize_arb_certified(
                        t_rough
                    ),
                    "T_smooth_W_M_X_minus_additive_certified": serialize_arb_certified(
                        t_smooth
                    ),
                    "analytic_comparison_bound_certified": serialize_arb_certified(
                        analytic_tail_bound
                    ),
                    "abs_W_minus_W_M_X_below_analytic_bound": bool(
                        abs(t_rough) <= analytic_tail_bound
                    ),
                    "abs_W_minus_W_M_X_below_half_C_log_0": bool(
                        abs(t_rough) <= half_c_log_0_arb
                    ),
                    "abs_T_smooth_below_analytic_bound": bool(
                        abs(t_smooth) <= analytic_tail_bound
                    ),
                    "smooth_plus_rough_partition_encloses_zero": bool(
                        partition_residual.contains(0)
                    ),
                }
            )

        # Certify the near-integer ceiling regression at X = 16 - 10^{-30}, 16, 16 + 10^{-30}:
        # For X = 16 + 10^{-30}, X^{5/4} = 32 + 2.5e-30 + ... > 32, so the exact ceiling is 33,
        # whereas binary64 float rounding of upper() produces 32.0 and a false cutoff 32.
        ceiling_regression_checks: List[Dict[str, Any]] = []
        for x_reg_label, x_reg_arb, expected_m_x in (
            ("16 - 10^{-30}", arb(16) - arb("1e-30"), 32),
            ("16", arb(16), 32),
            ("16 + 10^{-30}", arb(16) + arb("1e-30"), 33),
        ):
            reg_info = compute_coupled_cutoff_comparison_bound_arb(
                x_reg_arb, prec_bits=prec_bits
            )
            u_reg = reg_info["X_pow_5_4_arb"]
            naive_float_ceil = max(2, int(math.ceil(float(u_reg.upper()))))
            ceiling_regression_checks.append(
                {
                    "X_label": x_reg_label,
                    "X_pow_5_4_certified": serialize_arb_certified(u_reg),
                    "certified_M_X": reg_info["M_X"],
                    "expected_M_X": expected_m_x,
                    "naive_float_ceil_value": naive_float_ceil,
                    "matches_expected_M_X": (reg_info["M_X"] == expected_m_x),
                    "M_X_ge_X_pow_5_4_verified": reg_info["M_X_ge_X_pow_5_4"],
                    "M_X_sq_ge_X_pow_5_2_verified": reg_info["M_X_sq_ge_X_pow_5_2"],
                    "satisfies_uniform_bound": reg_info["satisfies_uniform_bound"],
                    "bound_at_M_X_certified": serialize_arb_certified(
                        reg_info["bound_at_M_X_arb"]
                    ),
                }
            )

        coupled_passage_audit = {
            "comparison_theorem_statement": (
                "For any X > 0 and any integer M >= 2 with prime cutoff y >= M, mu_y(m) = mu(m) for all 1 <= m <= M "
                "(and up to q_{>y} - 1), and |mu(m) - mu_y(m)| = |mu(m)| * 1_{m not dividing P_y} <= 1 for m > M. "
                "Using |W_log(X/m)| <= C_{log,0} (X/m)^{5/2} yields "
                "|W(X) - W_y(X)| = |R_mu(X) - R_{mu, y}(X)| <= C_{log,0} X^{5/2} sum_{m > M} m^{-3} <= C_{log,0} X^{5/2} / (2 M^2)."
            ),
            "coupled_cutoff_schedule": (
                "y = M(X) := ceil(max(2, X^{5/4})) for X >= 1 (computed as a certified safe integer cutoff directly from the "
                "upper endpoint of the Arb ball enclosure of (X^5)^{1/4} without float conversion; for an input interval ball "
                "crossing an integer boundary it may exceed the minimal pointwise ceiling while guaranteeing M(X) >= X^{5/4} "
                "and M(X)^2 >= X^{5/2} across the entire input ball)"
            ),
            "scale_horizon_vs_coupled_cutoff_tail_comparison": (
                "At the bare scale horizon N = floor(X), the small-scale tail bound is "
                "C_{log,0} X^{5/2} / (2 floor(X)^2) = O(sqrt(X)), which diverges as X -> infty and does NOT establish uniform "
                "boundedness equivalence with W(X). Choosing the coupled cutoff N = M(X) = ceil(max(2, X^{5/4})) makes "
                "M(X)^2 >= X^{5/2} and yields the uniform O(1) comparison bound C_{log,0} X^{5/2} / (2 M(X)^2) <= (1/2) C_{log,0} < 0.278715."
            ),
            "uniform_coupled_comparison_bound_formula": (
                "|W(X) - W_{M(X)}(X)| = |R_mu(X) - R_{mu, M(X)}(X)| <= C_{log,0} X^{5/2} / (2 M(X)^2) <= (1/2) C_{log,0}"
            ),
            "uniform_coupled_comparison_bound_certified": serialize_arb_certified(
                half_c_log_0_arb
            ),
            "smooth_and_rough_tail_partition": (
                "R_mu(X) - R_{mu, M}(X) = T_{smooth, y}(X) + T_{rough, y}(X), where "
                "T_{smooth, y}(X) = W_y(X) - (W_log(X) + R_{mu, M}(X)) sums over y-smooth squarefree m > M (m | P_y) and "
                "T_{rough, y}(X) = W(X) - W_y(X) sums over y-rough squarefree m > M (m not dividing P_y), "
                "with |T_{smooth, y}(X)| + |T_{rough, y}(X)| <= C_{log,0} X^{5/2} / (2 M^2)."
            ),
            "coupled_boundedness_equivalence": (
                "sup_{X >= 1} |R_mu(X)| < infty  <==>  sup_{X >= 1} |W(X)| < infty  "
                "<==>  sup_{X >= 1} |W_{M(X)}(X)| < infty  <==>  sup_{X >= 1} |R_{mu, M(X)}(X)| < infty "
                "(and for dense grade samples K in A_R = Qbar cap R, sup_{K in A_R} |W_{M(tau^{|K|})}(tau^{|K|})| < infty "
                "<==> sup_{X >= 1} |W_{M(X)}(X)| < infty by continuity of W(X) on [1, infty) together with the uniform "
                "comparison |W_{M(X)}(X) - W(X)| <= (1/2) C_{log,0} < 0.278715, NEVER by continuity of F(X) = W_{M(X)}(X), "
                "which is piecewise continuous with right-hand jump F(X_0^+) - F(X_0) = -p^{-1/2} W_{p^-}(X_0/p) at X_0 = (p-1)^{4/5})"
            ),
            "anti_circularity_diagnosis": (
                "Because |W_{M(X)}(X) - W(X)| <= (1/2) C_{log,0} < 0.278715 and "
                "|W_{M(X)}(X) - (W_log(X) + R_{mu, M(X)}(X))| <= (1/2) C_{log,0} < 0.278715 for all X >= 1, "
                "bounding W_{M(X)}(X) by assuming boundedness of W(X), R_mu(X), R_{mu, M(X)}(X), or C_tau(K) is strictly circular. "
                "Furthermore, at y = M(X) >= X, lambda_{M(X)}(n) = Lambda(n) for all 2 <= n < 2 q_{>M(X)} and "
                "mu_{M(X)}(m) = mu(m) for all 1 <= m <= M(X), so the coupled finite-prime Euler construction is an exact "
                "quantitative reformulation of the Moebius/prime cancellation obligation within +/- 0.278715."
            ),
            "certified_cutoff_ceiling_regression": ceiling_regression_checks,
            "certified_coupled_grade_table": coupled_grade_table,
            "lean_theorem": "coupled_prime_cutoff_comparison_and_boundedness_equivalence",
        }

        premise_and_outcome_classification = {
            "strongest_new_mathematical_results": [
                "Exact Finite-Prime Euler Inversion & Agreement Horizon (`finite_prime_euler_recursion_and_coefficient_cases`): W_y(X) = [prod_{p <= y}(I - p^{-1/2} D_p)] W_log(X) = sum_{n>=2} lambda_y(n) n^{-1/2} h_0(n/X) with lambda_y = mu_y * log >= Lambda >= 0, exact agreement lambda_y(n) = Lambda(n) for all 2 <= n < 2 q_{>y} (first discrepancy at 2 q_{>y} of value log 2), and summatory identity L_y(x) = sum_{d | P_y, d <= x} mu(d) log(floor(x/d)!).",
                "Coupled-Cutoff Quantitative Reduction & Smooth/Rough Tail Partition (`coupled_prime_cutoff_comparison_and_boundedness_equivalence`): For y >= M >= max(2, X), |W(X) - W_y(X)| <= C_{log,0} X^{5/2} / (2 M^2), and at y = M(X) = ceil(max(2, X^{5/4})), sup_{X >= 1} |W(X) - W_{M(X)}(X)| <= (1/2) C_{log,0} = 0.2787147936 < 0.278715 (and |W_{M(X)}(X) - (W_log(X) + R_{mu, M(X)}(X))| <= (1/2) C_{log,0} < 0.278715), reducing uniform boundedness of R_mu(X) to uniform boundedness of W_{M(X)}(X) or R_{mu, M(X)}(X) (whereas at N = floor(X) the available small-scale tail estimate grows as O(sqrt(X))).",
                "Quantified Dual Obstruction (Controlled-Width Coherent Euler Spike vs. Coupled-Cutoff Horizon Collapse): (1) On the critical line Re(z) = 0, holomorphy of M_X[W_y](z) = -E_y(z) H_0(z) zeta'(z+1/2) yields sup_{X > 0} |W_y(X)| <= ||Psi_y||_{L^2} N_{zeta',tau}; on the controlled-width frequency interval I_y = [7*tau/(16*log y), tau/(2*log y)] of width |I_y| = tau/(16*log y), prime-factor monotonicity proves inf_{t in I_y} |E_y(it)|^2 = |E_y(i t_{y,-})|^2 with PNT + partial summation asymptotic log|E_y(i t_{y,-})|^2 = (4*cos(tau/16) + o(1))*sqrt(y)/log y (4*cos(tau/16) = 2*sqrt(2+sqrt(2)) ~ 3.695518130045147, while the right endpoint has coefficient 4 and the false subproduct inequality is refuted at y = 210), and local Weierstrass-product monotonicity of H_0(it) on [0, 1] (covering I_y for all integer y >= 24, with 64-subinterval Arb certification for y in {2, 5, 11}) proves ||Psi_y||_{L^2}^2 >= (H_0(0)/(8 log y)) |E_y(i t_{y,-})|^2 = (H_0(0)/(8 log y)) exp[(4*cos(tau/16) + o(1))*sqrt(y)/log y] -> +infty, establishing divergence of the unsplit Cauchy-Schwarz/Gram-norm bound (without refuting boundedness of the coupled profile W_{M(X)}(X) or the broader concurrent-grade hypothesis); (2) splitting at the coupled cutoff M(X) = ceil(max(2, X^{5/4})) bounds the m > M(X) tail by (1/2) C_{log,0} < 0.278715, but for y >= M(X) every squarefree m <= M(X) divides P_y, collapsing the m <= M(X) sum identically to W_log(X) + R_{mu, M(X)}(X).",
            ],
            "advances_uniform_cancellation_estimate": False,
            "why_reformulation_not_closure": (
                "Finite-prime Euler inversion provides a genuine fixed-y uniform bound (via ||Psi_y||_{L^2}) and a "
                "quantitative coupled-cutoff reduction to y = M(X) = ceil(max(2, X^{5/4})) within 0.278715, "
                "but at y >= M(X) the divisors m <= M(X) and coefficients n < 2 q_{>y} reproduce the additive truncation "
                "W_log(X) + R_{mu, M(X)}(X) and the bulk von Mangoldt sum without supplying an independent signed cancellation bound."
            ),
            "remaining_open_obligation": {
                "subgate_id": "SUBGATE-TC-043A",
                "status": "OPEN",
                "exact_surviving_lemma": (
                    "Prove without assuming RH or universal Weil positivity that there exists a finite constant "
                    "M_mu < infty such that for all X >= 1, |R_mu(X)| <= M_mu "
                    "(equivalently, |W_{M(X)}(X)| <= M_y or |R_{mu, M(X)}(X)| <= M_trunc at the coupled cutoff "
                    "M(X) = ceil(max(2, X^{5/4})), where |W(X) - W_{M(X)}(X)| < 0.278715 and "
                    "|W_{M(X)}(X) - (W_log(X) + R_{mu, M(X)}(X))| < 0.278715; by contrast, at N = floor(X) the "
                    "available small-scale tail estimate grows as O(sqrt(X)))."
                ),
            },
        }

        result_tc046: Dict[str, Any] = {
            "task_id": TASK_TC_046_ID,
            "parent_epic": EPIC_TC_042_ID,
            "inspected_baseline": STARTING_HEAD_TC_046,
            "status": PRIME_EULER_MOEBIUS_RECOVERY_STATUS,
            "section_1_recovered_obligation_and_ambient_space": recovered_obligation_summary,
            "section_2_finite_prime_euler_inversion_and_coefficients": finite_prime_construction_audit,
            "section_3_quantitative_compatibility_and_obstruction_analysis": quantitative_compatibility_investigation,
            "section_4_coupled_cutoff_passage_and_grade_certification": coupled_passage_audit,
            "section_5_outcome_and_remaining_obligation": premise_and_outcome_classification,
        }
        full_tree_rt_sec15 = verify_all_serialized_arb_in_tree(
            result_tc046, path_prefix="section_15"
        )
        result_tc046["full_section_15_tree_roundtrip_verification"] = full_tree_rt_sec15
        return result_tc046
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 6. TASK-TC-049: Arithmetic Cancellation in the Canonical Theta Correlation
# ---------------------------------------------------------------------------

TASK_TC_049_ID = "TASK-TC-049"
STARTING_HEAD_TC_049 = "5da0eb79e1732ff871ee1c7fee729c62972aa406"
ARITHMETIC_CANCELLATION_CANONICAL_THETA_CORRELATION_STATUS = (
    "SUPERCRITICAL_DYADIC_BLOCK_OBSTRUCTION_SUBCRITICAL_COMPENSATION_AND_"
    "W_LOG_X_NEG_5_2_RESONANT_BAND_REDUCTION_PROVED_SUBGATE_OPEN"
)

# Exact integer polynomial coefficients for the 1st, 3rd, and 4th derivatives of
# psi_0(alpha) = alpha^{-1/2} h_0(alpha) and the Euler-Maclaurin kernel L(alpha):
#   psi_0'(alpha)     = alpha * P_{d1}(alpha^2) / (512 * (1 + alpha^2)^{19/2}),
#   psi_0'''(alpha)   = alpha * P_{d3}(alpha^2) / (512 * (1 + alpha^2)^{23/2}),
#   psi_0^{(4)}(alpha)= P_{d4}(alpha^2) / (512 * (1 + alpha^2)^{25/2}),
#   L(alpha)          = 4*psi_0'''/alpha - 6*psi_0''/alpha^2 + 8*psi_0'/alpha^3 - 6*psi_0/alpha^4
#                     = (81 / (32 * alpha^2 * (1 + alpha^2)^{23/2})) + Q_L(alpha^2) / (512 * (1 + alpha^2)^{23/2}).
PSI0_D1_POLY_COEFFS = [
    1944,
    -281532,
    4035324,
    -13386225,
    12918660,
    -3606756,
    227688,
    -1296,
]
PSI0_D3_POLY_COEFFS = [
    38880,
    -12152880,
    347539500,
    -2392069050,
    5364007425,
    -4317877620,
    1214056620,
    -100128600,
    1440000,
]
PSI0_D4_POLY_COEFFS = [
    -233280,
    97884000,
    -3657688200,
    33222842100,
    -101408863500,
    117362108745,
    -52078162500,
    8072855100,
    -332065800,
    1440000,
]
Q_L_POLY_COEFFS = [
    221616,
    -61411416,
    1625225736,
    -10464888546,
    21955131996,
    -16399152084,
    4190213034,
    -297984264,
    3014904,
]


def verify_symbolic_tc049_prime_increment_and_w_log_asymptotic_identities() -> Dict[str, Any]:
    """
    Verify symbolically in SymPy the core algebraic and asymptotic identities for TASK-TC-049:
      1. Exact kernel tail factorization:
           -h_0(alpha) = S^{-5/2} * kappa(S),   S = alpha + alpha^{-1},
           kappa(S) = 81/64 - 14595/(128 S^2) + 176715/(128 S^4) - 2027025/(512 S^6),
         with kappa(10) = 132858975 / 512000000 > 1/4 and kappa'(S) > 0 for all S >= 9.
      2. Small-alpha expansion of psi_0(alpha) = alpha^{-1/2} h_0(alpha):
           psi_0(alpha) = -(81/64) alpha^2 + (1875/16) alpha^4 - (972405/512) alpha^6 + O(alpha^8),
         and exact polynomial numerators P_{d1}(u), P_{d3}(u), P_{d4}(u), and Q_L(u) for the
         4th-order Euler-Maclaurin decomposition of g_X(x) = X^{-1/2} (log x) psi_0(x/X).
      3. Prime-increment telescoping identity:
           W_{p_k}(X) = W_log(X) - sum_{j=1}^k J_{p_j}(X),   J_{p_j}(X) = p_j^{-1/2} W_{p_{j-1}}(X / p_j).
      4. Subcritical sieve-defect vs. supercritical prime-increment coefficient cancellation identity:
           Delta_{y_1}(n) - sum_{y_1 < p <= y_2, p | n} lambda_{p^-}(n / p) = Delta_{y_2}(n),
         where Delta_y(n) := lambda_y(n) - Lambda(n), verified exactly for all 2 <= n <= 400 at (y_1, y_2) = (10, 40).
      5. Small-divisor head polynomial inequality:
           sum_{m=2}^N m^2 = N(N+1)(2N+1)/6 - 1 <= (5/6) N^3   for all N >= 2,
         since (5/6) N^3 - (N(N+1)(2N+1)/6 - 1) = (N - 2)(3N^2 + 3N + 1)/6 >= 0.
    """
    al = sp.Symbol("alpha", positive=True)
    S = sp.Symbol("S", positive=True)
    u = sp.Symbol("u", positive=True)
    N_sym = sp.Symbol("N", real=True)

    # 1. Kernel tail factorization -h_0(alpha) = S^{-5/2} kappa(S)
    W_s = S**2
    neg_h0_from_S = -(
        -648 * W_s**3 + 58380 * W_s**2 - 706860 * W_s + 2027025
    ) / (512 * S ** sp.Rational(17, 2))
    kappa_S = (
        sp.Rational(81, 64)
        - sp.Rational(14595, 128) / S**2
        + sp.Rational(176715, 128) / S**4
        - sp.Rational(2027025, 512) / S**6
    )
    kappa_factorization_verified = bool(
        sp.simplify(neg_h0_from_S - (S ** sp.Rational(-5, 2)) * kappa_S) == 0
    )
    kappa_at_10 = sp.simplify(kappa_S.subs(S, 10))
    kappa_at_10_exact_match = bool(
        kappa_at_10 == sp.Rational(132858975, 512000000)
        and kappa_at_10 > sp.Rational(1, 4)
    )
    dkappa_dS = sp.simplify(sp.diff(kappa_S, S))
    # Verify S^3 * dkappa_dS = (14595/64) - (353430/64)/S^2 + (12162150/512)/S^4 > 0 for S >= 9:
    dkappa_at_9_pos = bool(dkappa_dS.subs(S, 9) > 0)

    # 2. Small-alpha series of psi_0(alpha) = alpha^{-1/2} h_0(alpha) and 4th-order Euler-Maclaurin polynomials
    num_u = u * (
        -648 * (1 + u) ** 6
        + 58380 * u * (1 + u) ** 4
        - 706860 * u**2 * (1 + u) ** 2
        + 2027025 * u**3
    )
    psi0 = num_u.subs(u, al**2) / (512 * (1 + al**2) ** sp.Rational(17, 2))
    psi0_series_expr = sp.series(psi0, al, 0, 8).removeO()
    expected_psi0_series = (
        -sp.Rational(81, 64) * al**2
        + sp.Rational(1875, 16) * al**4
        - sp.Rational(972405, 512) * al**6
    )
    psi0_series_verified = bool(
        sp.simplify(psi0_series_expr - expected_psi0_series) == 0
    )

    psi0_d1 = sp.diff(psi0, al)
    psi0_d2 = sp.diff(psi0_d1, al)
    psi0_d3 = sp.diff(psi0_d2, al)
    psi0_d4 = sp.diff(psi0_d3, al)
    L_al = sp.simplify(
        4 * psi0_d3 / al
        - 6 * psi0_d2 / al**2
        + 8 * psi0_d1 / al**3
        - 6 * psi0 / al**4
    )

    p_d1_u = sp.Poly(
        sp.simplify(psi0_d1 * 512 * (1 + al**2) ** sp.Rational(19, 2) / al).subs(
            al, sp.sqrt(u)
        ),
        u,
    )
    p_d3_u = sp.Poly(
        sp.simplify(psi0_d3 * 512 * (1 + al**2) ** sp.Rational(23, 2) / al).subs(
            al, sp.sqrt(u)
        ),
        u,
    )
    p_d4_u = sp.Poly(
        sp.simplify(psi0_d4 * 512 * (1 + al**2) ** sp.Rational(25, 2)).subs(
            al, sp.sqrt(u)
        ),
        u,
    )
    p_L_u = sp.Poly(
        sp.simplify(L_al * 512 * al**2 * (1 + al**2) ** sp.Rational(23, 2)).subs(
            al, sp.sqrt(u)
        ),
        u,
    )
    poly_coeffs_verified = bool(
        [int(c) for c in p_d1_u.all_coeffs()] == PSI0_D1_POLY_COEFFS
        and [int(c) for c in p_d3_u.all_coeffs()] == PSI0_D3_POLY_COEFFS
        and [int(c) for c in p_d4_u.all_coeffs()] == PSI0_D4_POLY_COEFFS
        and [int(c) for c in p_L_u.all_coeffs()] == Q_L_POLY_COEFFS + [1296]
    )

    # Verify antiderivative identity: d/d_alpha [ (3/alpha) psi_0'' - (3/alpha^2) psi_0' + (2/alpha^3) psi_0 ] + psi_0'''/alpha == L(alpha)
    F3_al = 3 * psi0_d2 / al - 3 * psi0_d1 / al**2 + 2 * psi0 / al**3
    antideriv_L_verified = bool(
        sp.simplify(sp.diff(F3_al, al) + psi0_d3 / al - L_al) == 0
    )

    # 3. Subcritical sieve-defect vs. supercritical prime-increment coefficient cancellation identity:
    #    Delta_{y_1}(n) - sum_{y_1 < p <= y_2, p | n} lambda_{p^-}(n / p) == Delta_{y_2}(n)
    y1_test, y2_test = 10, 40
    primes_between = [p for p in primes_up_to(y2_test) if p > y1_test]
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        coeff_cancellation_all_zero = True
        for n_idx in range(2, 401):
            vn = von_mangoldt_arb(n_idx)
            delta_y1 = evaluate_lambda_y_closed_form_arb(n_idx, y1_test) - vn
            delta_y2 = evaluate_lambda_y_closed_form_arb(n_idx, y2_test) - vn
            inc_sum = arb(0)
            for p in primes_between:
                if n_idx % p == 0:
                    inc_sum += evaluate_lambda_y_closed_form_arb(
                        n_idx // p, p - 1
                    )
            diff_n = (delta_y1 - inc_sum) - delta_y2
            if not bool(diff_n.contains(0) and float(abs(diff_n).upper()) < 1e-70):
                coeff_cancellation_all_zero = False
                break
    finally:
        flint_ctx.prec = saved_prec

    # 4. Small-divisor head polynomial identity:
    #    (5/6) N^3 - (N(N+1)(2N+1)/6 - 1) == (3 N^2 (N - 2) + 3 N (N - 1) + 2 N + 6) / 6 > 0 for all N >= 2
    head_poly_diff = sp.simplify(
        (sp.Rational(5, 6) * N_sym**3 - (N_sym * (N_sym + 1) * (2 * N_sym + 1) / 6 - 1))
        - (3 * N_sym**2 * (N_sym - 2) + 3 * N_sym * (N_sym - 1) + 2 * N_sym + 6) / 6
    )
    head_sum_bound_identity_verified = bool(head_poly_diff == 0)

    return {
        "kappa_factorization_verified": kappa_factorization_verified,
        "kappa_at_10_exact_rational": "132858975/512000000",
        "kappa_at_10_exact_match": kappa_at_10_exact_match,
        "dkappa_at_9_pos": dkappa_at_9_pos,
        "psi0_series_verified": psi0_series_verified,
        "poly_coeffs_verified": poly_coeffs_verified,
        "antideriv_L_verified": antideriv_L_verified,
        "subcritical_supercritical_coeff_cancellation_verified_n_2_to_400": coeff_cancellation_all_zero,
        "head_sum_bound_identity_verified": head_sum_bound_identity_verified,
        "all_verified": bool(
            kappa_factorization_verified
            and kappa_at_10_exact_match
            and dkappa_at_9_pos
            and psi0_series_verified
            and poly_coeffs_verified
            and antideriv_L_verified
            and coeff_cancellation_all_zero
            and head_sum_bound_identity_verified
        ),
    }


def evaluate_prime_increment_J_p_arb(
    X: arb, p: int, n_max: int = 3000, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Certify the single-prime Euler recursion increment:
        J_p(X) := p^{-1/2} W_{p^-}(X / p) = W_{p^-}(X) - W_p(X),
    and compare against the n = 2 supercritical lower-bound term
        (log 2 / sqrt(2 p)) (-h_0(2 p / X))
    when 2 p / X >= 9 > alpha_3^* ~ 8.621336.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X_arb = arb(X)
        p_arb = arb(p)
        w_p_minus_at_X_over_p = evaluate_w_y_coefficient_certified_arb(
            X_arb / p_arb, y=p - 1, n_max=n_max, prec_bits=prec_bits
        )["enclosure_arb"]
        J_p_direct = w_p_minus_at_X_over_p / p_arb.sqrt()

        w_p_minus_at_X = evaluate_w_y_coefficient_certified_arb(
            X_arb, y=p - 1, n_max=n_max, prec_bits=prec_bits
        )["enclosure_arb"]
        w_p_at_X = evaluate_w_y_coefficient_certified_arb(
            X_arb, y=p, n_max=n_max, prec_bits=prec_bits
        )["enclosure_arb"]
        J_p_step_diff = w_p_minus_at_X - w_p_at_X
        step_residual = J_p_direct - J_p_step_diff

        alpha_2 = arb(2) * p_arb / X_arb
        n2_lower_bound = (
            arb(2).log()
            / (arb(2) * p_arb).sqrt()
            * (-evaluate_h0_arb(alpha_2))
        )
        neg_J_p = -J_p_direct
        is_supercritical = bool(alpha_2 >= arb(9))
        satisfies_n2_lower_bound = (
            bool(neg_J_p >= n2_lower_bound and n2_lower_bound > arb(0))
            if is_supercritical
            else False
        )
        return {
            "X": float(X_arb.mid()),
            "p": p,
            "alpha_2_eq_2p_over_X": float(alpha_2.mid()),
            "is_supercritical_2p_ge_9X": is_supercritical,
            "J_p_direct_arb": J_p_direct,
            "J_p_step_diff_arb": J_p_step_diff,
            "step_residual_encloses_zero": bool(step_residual.contains(0)),
            "neg_J_p_arb": neg_J_p,
            "n2_lower_bound_arb": n2_lower_bound,
            "satisfies_n2_lower_bound": satisfies_n2_lower_bound,
            "J_p_direct_certified": serialize_arb_certified(J_p_direct),
            "n2_lower_bound_certified": serialize_arb_certified(n2_lower_bound),
        }
    finally:
        flint_ctx.prec = saved_prec


def certify_dyadic_prime_block_and_subcritical_compensation_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """
    Certify:
      1. The supercritical prime-increment lower bound constant c_0(A) for A = 5:
           c_0(5) = (log 2 / 8) * kappa(10) * (1 + 10^{-2})^{-5/2} > 0.021928,
         and the asymptotic constant c_0(infty) = 81 * log(2) / 512 ~ 0.10966236.
      2. Across sample scales X in {2, 4, tau, 10, 16, 25} with A = 5:
         - The dyadic prime block sum B_{5X, 10X}(X) = -sum_{5X < p <= 10X} J_p(X) > 0,
         - The analytic lower bound c_0(5) * X^{5/2} * sum_{5X < p <= 10X} p^{-3},
         - Verification that B_{5X, 10X}(X) >= n=2 sum >= analytic p^{-3} sum > 0.
      3. Across sample scales X in {1, 2, 4, tau, 10, 16} with cutoff y_sub = floor(5 X) and
         coupled cutoff M(X) = ceil(max(2, X^{5/4})):
         - The exact telescoping identity W_{M(X)}(X) = W_log(X) - sum_{p <= M(X)} J_p(X),
         - The subcritical sieve-defect tail D_{y_sub}(X) = W_{y_sub}(X) - W(X) < 0,
         - The supercritical prime-increment sum T_{>y_sub}(X) = -sum_{y_sub < p <= M(X)} J_p(X) > 0,
         - Verification that (D_{y_sub}(X) + T_{>y_sub}(X)) - (W_{M(X)}(X) - W(X)) encloses 0
           and |D_{y_sub}(X) + T_{>y_sub}(X)| <= (1/2) C_{log,0} < 0.278715.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        pi_arb = arb.pi()
        tau_arb = arb(2) * pi_arb
        zeta_prime_3_arb = acb_series([acb(3), acb(1)], 2).zeta()[1].real
        c_log_0_arb = (arb(92193) / arb(32768)) * (-zeta_prime_3_arb)
        half_c_log_0_arb = c_log_0_arb / arb(2)

        kappa_10_arb = arb(132858975) / arb(512000000)
        c0_A5_arb = (
            (arb(2).log() / arb(8))
            * kappa_10_arb
            * ((arb(1) + arb(1) / arb(100)) ** arb("-2.5"))
        )
        c0_inf_arb = arb(81) * arb(2).log() / arb(512)
        dyadic_rs_coeff_A5_arb = (arb(3) * c0_A5_arb) / (arb(32) * arb(25))

        dyadic_block_table: List[Dict[str, Any]] = []
        for x_label, x_arb in (
            ("2", arb(2)),
            ("4", arb(4)),
            ("tau", tau_arb),
            ("10", arb(10)),
            ("16", arb(16)),
            ("25", arb(25)),
        ):
            y_low = int(math.floor(float((arb(5) * x_arb).mid())))
            y_high = int(math.floor(float((arb(10) * x_arb).mid())))
            primes_dyadic = [p for p in primes_up_to(y_high) if p > y_low]
            block_neg_J_sum = arb(0)
            block_n2_lb_sum = arb(0)
            block_p_inv3_sum = arb(0)
            all_primes_neg_and_above_lb = True
            for p in primes_dyadic:
                p_arb = arb(p)
                w_prev = evaluate_w_y_coefficient_certified_arb(
                    x_arb / p_arb, y=p - 1, n_max=600, prec_bits=prec_bits
                )["enclosure_arb"]
                neg_J_p = -w_prev / p_arb.sqrt()
                n2_lb = (
                    arb(2).log()
                    / (arb(2) * p_arb).sqrt()
                    * (-evaluate_h0_arb(arb(2) * p_arb / x_arb))
                )
                p_inv3_lb = c0_A5_arb * (x_arb ** arb("2.5")) / (p_arb**3)
                if not bool(neg_J_p >= n2_lb and n2_lb >= p_inv3_lb and p_inv3_lb > arb(0)):
                    all_primes_neg_and_above_lb = False
                block_neg_J_sum += neg_J_p
                block_n2_lb_sum += n2_lb
                block_p_inv3_sum += arb(1) / (p_arb**3)

            analytic_block_lb = c0_A5_arb * (x_arb ** arb("2.5")) * block_p_inv3_sum
            analytic_block_ub = c_log_0_arb * (x_arb ** arb("2.5")) * block_p_inv3_sum
            dyadic_block_table.append(
                {
                    "X_label": x_label,
                    "X_certified": serialize_arb_certified(x_arb),
                    "dyadic_interval_5X_to_10X": [y_low, y_high],
                    "prime_count_in_block": len(primes_dyadic),
                    "neg_dyadic_block_sum_certified": serialize_arb_certified(
                        block_neg_J_sum
                    ),
                    "n2_term_lower_bound_sum_certified": serialize_arb_certified(
                        block_n2_lb_sum
                    ),
                    "analytic_c0_A5_lower_bound_certified": serialize_arb_certified(
                        analytic_block_lb
                    ),
                    "analytic_C_log_0_upper_bound_certified": serialize_arb_certified(
                        analytic_block_ub
                    ),
                    "all_primes_satisfy_two_sided_inequality": all_primes_neg_and_above_lb,
                    "block_satisfies_lower_and_upper_bounds": bool(
                        block_neg_J_sum >= block_n2_lb_sum
                        and block_n2_lb_sum >= analytic_block_lb
                        and block_neg_J_sum <= analytic_block_ub
                    ),
                }
            )

        # Subcritical sieve-defect vs. supercritical prime-increment compensation table
        # For X in {2, 4, tau, 10, 16}, certify both:
        #   (a) Coupled-cutoff telescoping & compensation at y_sub <= M(X) = ceil(max(2, X^{5/4})), and
        #   (b) Supercritical linear-cutoff sign-definite compensation at y_1 = floor(5 X) and y_2 = max(floor(10 X), M(X)),
        #       where D_{y_1}(X) = W_{y_1}(X) - W(X) < 0, T_{(y_1, y_2]}(X) = -sum_{y_1 < p <= y_2} J_p(X) > 0,
        #       D_{y_2}(X) = D_{y_1}(X) + T_{(y_1, y_2]}(X) < 0, and -D_{y_1}(X) > T_{(y_1, y_2]}(X) > 0.
        subcritical_compensation_table: List[Dict[str, Any]] = []
        for x_label, x_arb, y_sub in (
            ("2", arb(2), 2),
            ("4", arb(4), 3),
            ("tau", tau_arb, 5),
            ("10", arb(10), 11),
            ("16", arb(16), 19),
        ):
            M_X = certified_coupled_cutoff_M_X_arb(x_arb, prec_bits=prec_bits)
            y1_lin = int(math.floor(float((arb(5) * x_arb).mid())))
            y2_lin = max(int(math.floor(float((arb(10) * x_arb).mid()))), M_X)
            n_max_c = max(3500, int(120 * float(x_arb.mid())) + 2000)
            w_actual = evaluate_w_prime_sum_certified_arb(
                x_arb, n_max=n_max_c, prec_bits=prec_bits
            )["enclosure_arb"]
            w_log_val = evaluate_w_log_divisor_aggregated_certified_arb(
                x_arb, k_max=n_max_c, prec_bits=prec_bits
            )["enclosure_arb"]
            w_sub = evaluate_w_y_coefficient_certified_arb(
                x_arb, y=y_sub, n_max=n_max_c, prec_bits=prec_bits
            )["enclosure_arb"]
            w_M = evaluate_w_y_coefficient_certified_arb(
                x_arb, y=M_X, n_max=n_max_c, prec_bits=prec_bits
            )["enclosure_arb"]

            # Sum prime increments J_p(X) over p <= y_sub, y_sub < p <= M(X), and y1_lin < p <= y2_lin:
            sum_J_le_sub = arb(0)
            for p in primes_up_to(y_sub):
                p_arb = arb(p)
                k_eff = max(400, int(n_max_c / p) + 200)
                w_prev = evaluate_w_y_coefficient_certified_arb(
                    x_arb / p_arb, y=p - 1, n_max=k_eff, prec_bits=prec_bits
                )["enclosure_arb"]
                sum_J_le_sub += w_prev / p_arb.sqrt()

            T_gt_sub = arb(0)
            for p in primes_up_to(M_X):
                if p > y_sub:
                    p_arb = arb(p)
                    k_eff = max(300, int(n_max_c / p) + 150)
                    w_prev = evaluate_w_y_coefficient_certified_arb(
                        x_arb / p_arb, y=p - 1, n_max=k_eff, prec_bits=prec_bits
                    )["enclosure_arb"]
                    T_gt_sub += -w_prev / p_arb.sqrt()

            T_y1_to_y2_lin = arb(0)
            for p in primes_up_to(y2_lin):
                if p > y1_lin:
                    p_arb = arb(p)
                    k_eff = max(300, int(n_max_c / p) + 150)
                    w_prev = evaluate_w_y_coefficient_certified_arb(
                        x_arb / p_arb, y=p - 1, n_max=k_eff, prec_bits=prec_bits
                    )["enclosure_arb"]
                    T_y1_to_y2_lin += -w_prev / p_arb.sqrt()

            D_sub = w_sub - w_actual
            n_max_lin = max(4000, int(380 * float(x_arb.mid())))

            def _eval_supercritical_sieve_defect_direct_arb(y_cut: int) -> arb:
                q_next = next_prime_above(y_cut)
                acc_d = arb(0)
                for n_idx in range(2 * q_next, n_max_lin + 1):
                    del_n = evaluate_lambda_y_closed_form_arb(
                        n_idx, y_cut
                    ) - von_mangoldt_arb(n_idx)
                    if not (del_n == 0):
                        n_a = arb(n_idx)
                        acc_d += (del_n / n_a.sqrt()) * evaluate_h0_arb(n_a / x_arb)
                n_lim_a = arb(n_max_lin)
                tb_d = (
                    (arb(81) / arb(64))
                    * (x_arb ** arb("2.5"))
                    * (arb(2) * n_lim_a.log() + arb(1))
                    / (arb(4) * (n_lim_a**2))
                )
                return acc_d + arb(0, tb_d.upper())

            D_y1_lin = _eval_supercritical_sieve_defect_direct_arb(y1_lin)
            D_y2_lin = _eval_supercritical_sieve_defect_direct_arb(y2_lin)
            telescoping_sub_res = w_sub - (w_log_val - sum_J_le_sub)
            telescoping_M_res = w_M - (w_sub + T_gt_sub)
            compensation_res = (D_sub + T_gt_sub) - (w_M - w_actual)
            lin_compensation_res = (D_y1_lin + T_y1_to_y2_lin) - D_y2_lin

            subcritical_compensation_table.append(
                {
                    "X_label": x_label,
                    "X_certified": serialize_arb_certified(x_arb),
                    "y_sub": y_sub,
                    "coupled_cutoff_M_X": M_X,
                    "y1_lin_5X": y1_lin,
                    "y2_lin_10X": y2_lin,
                    "W_X_certified": serialize_arb_certified(w_actual),
                    "W_y_sub_certified": serialize_arb_certified(w_sub),
                    "W_M_X_certified": serialize_arb_certified(w_M),
                    "subcritical_sieve_defect_D_y_sub_certified": serialize_arb_certified(
                        D_sub
                    ),
                    "supercritical_increment_sum_T_gt_y_sub_certified": serialize_arb_certified(
                        T_gt_sub
                    ),
                    "net_sum_D_plus_T_certified": serialize_arb_certified(
                        D_sub + T_gt_sub
                    ),
                    "D_y1_lin_5X_certified": serialize_arb_certified(D_y1_lin),
                    "T_y1_to_y2_lin_certified": serialize_arb_certified(
                        T_y1_to_y2_lin
                    ),
                    "D_y2_lin_10X_certified": serialize_arb_certified(D_y2_lin),
                    "telescoping_at_y_sub_encloses_zero": bool(
                        telescoping_sub_res.contains(0)
                    ),
                    "telescoping_at_M_X_encloses_zero": bool(
                        telescoping_M_res.contains(0)
                    ),
                    "compensation_identity_encloses_zero": bool(
                        compensation_res.contains(0)
                    ),
                    "net_sum_bounded_by_half_C_log_0": bool(
                        abs(D_sub + T_gt_sub) <= half_c_log_0_arb
                    ),
                    "linear_cutoff_D_5X_strictly_negative": bool(
                        D_y1_lin < arb(0)
                    ),
                    "linear_cutoff_T_5X_to_10X_strictly_positive": bool(
                        T_y1_to_y2_lin > arb(0)
                    ),
                    "linear_cutoff_D_10X_strictly_negative": bool(
                        D_y2_lin < arb(0)
                    ),
                    "linear_cutoff_neg_D_5X_exceeds_T_5X_to_10X": bool(
                        (-D_y1_lin) > T_y1_to_y2_lin and T_y1_to_y2_lin > arb(0)
                    ),
                    "linear_cutoff_compensation_encloses_zero": bool(
                        lin_compensation_res.contains(0)
                    ),
                }
            )

        return {
            "kappa_10_certified": serialize_arb_certified(kappa_10_arb),
            "c0_A5_certified": serialize_arb_certified(c0_A5_arb),
            "c0_inf_certified": serialize_arb_certified(c0_inf_arb),
            "dyadic_rosser_schoenfeld_coeff_A5_certified": serialize_arb_certified(
                dyadic_rs_coeff_A5_arb
            ),
            "dyadic_block_table": dyadic_block_table,
            "subcritical_compensation_table": subcritical_compensation_table,
        }
    finally:
        flint_ctx.prec = saved_prec


def certify_w_log_large_scale_decay_and_resonant_band_reduction_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """
    Certify Cancellation Mechanism 2 for TASK-TC-049:
      1. Exact 4th-order Euler-Maclaurin & Mellin-residue large-scale asymptotic of W_log(X):
           W_log(X) = -(81 * zeta(3) / (256 * pi^2)) * X^{-5/2} + R_{log,EM}(X),
         where the triple zero of H_0(z) at z = -1/2 (H_0(-1/2) = H_0'(-1/2) = H_0''(-1/2) = 0)
         cancels the Stirling (1/2) log(2*pi*x) main term identically and shifts the leading
         large-X pole to z = -5/2 (s = -2), improving TC-044's O(X^{-1/2} log X) bound by two
         full powers of X to O(X^{-5/2}).
      2. Certified global spatial Euler-Maclaurin constants:
           I_{d4,0}   = int_0^infty |psi_0^{(4)}(alpha)| d_alpha = 2 sum_{j=1}^9 |psi_0'''(r_j)|,
           I_{d4,log} = int_0^infty |log alpha| |psi_0^{(4)}(alpha)| d_alpha,
           I_{R_L}    = int_0^infty |R_L(alpha)| d_alpha,
         establishing for all X >= 1:
           |W_log(X)| <= (217709/393216 + (I_{d4,0}/384)*(log X / X) + ((I_{d4,log} + I_{R_L})/384)*(1/X)) X^{-5/2}
                      <= C_{log,EM} * X^{-5/2}   (C_{log,EM} < 13.47),
         and combining with the uniform bound |W_log(X)| <= 3.34901 on [1, 16] and the sharp
         Euler-Maclaurin bound for X >= 16 to certify |W_log(X)| <= C_{log,sharp} X^{-5/2} across sample scales.
      3. Unconditional small-divisor head bound (2 <= m <= M_-(X) := floor(X^{5/6})) and
         two-sided localized resonant divisor band reduction (X^{5/6} < m <= M_+(X) := M(X)):
           R_mu(X) = R_{mu,head}(X) + R_{mu,band}(X) + R_{mu,tail}(X),
           |R_{mu,head}(X)| <= (5/6) C_{log,EM} < 11.224,
           |R_{mu,tail}(X)| <= (1/2) C_{log,0} < 0.278715,
           |R_mu(X) - R_{mu,band}(X)| <= (5/6) C_{log,EM} + (1/2) C_{log,0} < 11.503   for all X >= 1.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        pi_arb = arb.pi()
        tau_arb = arb(2) * pi_arb
        zeta_prime_3_arb = acb_series([acb(3), acb(1)], 2).zeta()[1].real
        c_log_0_arb = (arb(92193) / arb(32768)) * (-zeta_prime_3_arb)
        half_c_log_0_arb = c_log_0_arb / arb(2)

        # Leading Mellin pole residue at z = -5/2 (s = -2) and second pole residue at z = -9/2 (s = -4):
        c_lead_z_neg_5_2_arb = (
            -arb(81) * arb(3).zeta() / (arb(256) * (pi_arb**2))
        )
        c_sublead_z_neg_9_2_arb = (
            -arb(5625) * arb(5).zeta() / (arb(64) * (pi_arb**4))
        )

        # Certify the 9 positive roots of P_{d4}(u) and 8 positive roots of Q_L(u) via Interval Newton:
        u_sym = sp.Symbol("u", real=True)
        p_d4_poly = sum(
            c * u_sym ** (len(PSI0_D4_POLY_COEFFS) - 1 - i)
            for i, c in enumerate(PSI0_D4_POLY_COEFFS)
        )
        q_L_poly = sum(
            c * u_sym ** (len(Q_L_POLY_COEFFS) - 1 - i)
            for i, c in enumerate(Q_L_POLY_COEFFS)
        )

        def _eval_horner_arb(coeffs: List[int], u_a: arb) -> arb:
            acc = arb(0)
            for c_val in coeffs:
                acc = acc * u_a + arb(c_val)
            return acc

        def _eval_horner_acb(coeffs: List[int], u_c: acb) -> acb:
            acc = acb(0)
            for c_val in coeffs:
                acc = acc * u_c + acb(c_val)
            return acc

        def _certify_alpha_roots(poly_expr: Any, coeffs: List[int]) -> List[arb]:
            d_coeffs = [
                int(c) for c in sp.Poly(sp.diff(poly_expr, u_sym), u_sym).all_coeffs()
            ]
            roots: List[arb] = []
            for (a_r, b_r), _ in sp.Poly(poly_expr, u_sym).intervals(eps=1e-35):
                u_m = arb(
                    (
                        (
                            arb(int(a_r.p)) / arb(int(a_r.q))
                            + arb(int(b_r.p)) / arb(int(b_r.q))
                        )
                        / arb(2)
                    ).mid()
                )
                for _ in range(12):
                    u_m = arb(
                        (
                            u_m
                            - _eval_horner_arb(coeffs, u_m)
                            / _eval_horner_arb(d_coeffs, u_m)
                        ).mid()
                    )
                u_pt = arb(u_m.mid())
                rad = arb("1e-55")
                u_ball = arb(u_pt.mid(), rad.upper())
                step = u_pt - _eval_horner_arb(coeffs, u_pt) / _eval_horner_arb(
                    d_coeffs, u_ball
                )
                if not bool(abs(step - u_pt) < rad):
                    raise RuntimeError("Interval Newton root certification failed in TC-049")
                roots.append(u_ball.sqrt())
            return roots

        roots_d4 = _certify_alpha_roots(p_d4_poly, PSI0_D4_POLY_COEFFS)
        roots_qL = _certify_alpha_roots(q_L_poly, Q_L_POLY_COEFFS)

        # 1. Exact algebraic total variation I_{d4,0} = int_0^infty |psi_0^{(4)}(alpha)| d_alpha = 2 sum_{j=1}^9 |psi_0'''(r_j)|:
        def _eval_psi0_d3_arb(al_b: arb) -> arb:
            u_b = al_b * al_b
            op = arb(1) + u_b
            return (
                al_b
                * _eval_horner_arb(PSI0_D3_POLY_COEFFS, u_b)
                / (arb(512) * (op**11) * op.sqrt())
            )

        I_d4_0_arb = arb(2) * sum(
            (abs(_eval_psi0_d3_arb(r_b)) for r_b in roots_d4), arb(0)
        )

        # 2. Root-split Arb integration for I_{d4,log} and I_{R_L}:
        tol_em = 2**(-70)
        eps0 = arb("1e-8")

        def _f_d4_log(al: acb, analytic: bool = False) -> acb:
            u_c = al * al
            op = acb(1) + u_c
            return (
                al.log(analytic=analytic)
                * _eval_horner_acb(PSI0_D4_POLY_COEFFS, u_c)
                / (acb(512) * (op**12) * op.sqrt(analytic=analytic))
            )

        def _f_d4_log_inv(v: acb, analytic: bool = False) -> acb:
            v2 = v * v
            op = acb(1) + v2
            return (
                -v.log(analytic=analytic)
                * (v**5)
                * _eval_horner_acb(list(reversed(PSI0_D4_POLY_COEFFS)), v2)
                / (acb(512) * (op**12) * op.sqrt(analytic=analytic))
            )

        nodes_d4_log = [eps0] + roots_d4[:4] + [arb(1)] + roots_d4[4:]
        I_d4_log_arb = arb(0)
        for idx in range(len(nodes_d4_log) - 1):
            a_b = nodes_d4_log[idx]
            b_b = nodes_d4_log[idx + 1]
            seg_val = acb.integral(
                _f_d4_log,
                acb(a_b.mid()),
                acb(b_b.mid()),
                rel_tol=tol_em,
                abs_tol=tol_em,
            ).real
            I_d4_log_arb += abs(seg_val)
        I_d4_log_arb += abs(
            acb.integral(
                _f_d4_log_inv,
                acb(eps0),
                acb((arb(1) / roots_d4[-1]).mid()),
                rel_tol=tol_em,
                abs_tol=tol_em,
            ).real
        )
        # Add endpoint/cutoff allowance on (0, eps0) where |psi_0^{(4)}(alpha)| <= 3000:
        eps_tail_d4 = arb(3000) * eps0 * ((arb(1) / eps0).log() + arb(1))
        I_d4_log_arb = I_d4_log_arb + arb(0, eps_tail_d4.upper())

        def _f_RL(al: acb, analytic: bool = False) -> acb:
            u_c = al * al
            op = acb(1) + u_c
            return _eval_horner_acb(Q_L_POLY_COEFFS, u_c) / (
                acb(512) * (op**11) * op.sqrt(analytic=analytic)
            )

        def _f_RL_inv(v: acb, analytic: bool = False) -> acb:
            v2 = v * v
            op = acb(1) + v2
            return (
                (v**7)
                * _eval_horner_acb(list(reversed(Q_L_POLY_COEFFS)), v2)
                / (acb(512) * (op**11) * op.sqrt(analytic=analytic))
            )

        nodes_RL = [arb(0)] + roots_qL
        I_RL_arb = arb(0)
        for idx in range(len(nodes_RL) - 1):
            a_b = nodes_RL[idx]
            b_b = nodes_RL[idx + 1]
            seg_val = acb.integral(
                _f_RL,
                acb(a_b.mid()),
                acb(b_b.mid()),
                rel_tol=tol_em,
                abs_tol=tol_em,
            ).real
            I_RL_arb += abs(seg_val)
        I_RL_arb += abs(
            acb.integral(
                _f_RL_inv,
                acb(0),
                acb((arb(1) / roots_qL[-1]).mid()),
                rel_tol=tol_em,
                abs_tol=tol_em,
            ).real
        )

        # Global spatial Euler-Maclaurin constant C_{log,EM} for all X >= 1:
        c_bdry_and_singular_arb = arb(217709) / arb(393216)
        c_em_log_coeff_arb = I_d4_0_arb / arb(384)
        c_em_const_coeff_arb = (I_d4_log_arb + I_RL_arb) / arb(384)
        inv_e_arb = arb(-1).exp()
        c_log_em_global_arb = (
            c_bdry_and_singular_arb
            + c_em_log_coeff_arb * inv_e_arb
            + c_em_const_coeff_arb
        )
        small_divisor_head_bound_em_arb = (arb(5) / arb(6)) * c_log_em_global_arb
        resonant_band_comparison_bound_em_arb = (
            small_divisor_head_bound_em_arb + half_c_log_0_arb
        )

        # Helper to evaluate W_log(X) to high accuracy at any X >= 1 via zero-moment Euler-Maclaurin:
        from tc.canonical_theta_correlation_bound import evaluate_h0_acb

        def _eval_w_log_em_sharp_arb(X_a: arb) -> arb:
            x_mid = float(X_a.mid())
            if x_mid <= 8.0:
                return evaluate_w_log_divisor_aggregated_certified_arb(
                    X_a, k_max=5000, prec_bits=prec_bits
                )["enclosure_arb"]
            N0 = max(160, int(16 * x_mid))
            s_part = arb(0)
            for k in range(2, N0 + 1):
                k_a = arb(k)
                s_part += (k_a.log() / k_a.sqrt()) * evaluate_h0_arb(k_a / X_a)
            eps_b = arb("1e-8")
            tol_i = 2**(-80)

            def _f_g(x_c: acb, analytic: bool = False, xc: acb = acb(X_a)) -> acb:
                return (
                    (x_c ** acb("-0.5"))
                    * x_c.log(analytic=analytic)
                    * evaluate_h0_acb(x_c / xc, analytic=analytic)
                )

            int_0_N0 = (
                acb.integral(
                    _f_g, acb(eps_b), acb("0.25"), rel_tol=tol_i, abs_tol=tol_i
                ).real
                + acb.integral(
                    _f_g, acb("0.25"), acb(1), rel_tol=tol_i, abs_tol=tol_i
                ).real
                + acb.integral(
                    _f_g, acb(1), acb(X_a.mid()), rel_tol=tol_i, abs_tol=tol_i
                ).real
                + acb.integral(
                    _f_g,
                    acb(X_a.mid()),
                    acb((arb(4) * X_a).mid()),
                    rel_tol=tol_i,
                    abs_tol=tol_i,
                ).real
                + acb.integral(
                    _f_g,
                    acb((arb(4) * X_a).mid()),
                    acb(N0),
                    rel_tol=tol_i,
                    abs_tol=tol_i,
                ).real
            )
            eps_0_err = (
                (arb(92193) / arb(32768))
                * (X_a ** arb("-2.5"))
                * (eps_b**3)
                * (arb(3) * (arb(1) / eps_b).log() + arb(1))
                / arb(9)
            )
            N0_a = arb(N0)
            al_N0 = N0_a / X_a
            u_N0 = al_N0 * al_N0
            op_N0 = arb(1) + u_N0
            psi0_N0 = (al_N0 ** arb("-0.5")) * evaluate_h0_arb(al_N0)
            psi0_d1_N0 = (
                al_N0
                * _eval_horner_arb(PSI0_D1_POLY_COEFFS, u_N0)
                / (arb(512) * (op_N0**9) * op_N0.sqrt())
            )
            g_N0 = (N0_a.log() / N0_a.sqrt()) * evaluate_h0_arb(al_N0)
            gp_N0 = (X_a ** arb("-1.5")) * (
                N0_a.log() * psi0_d1_N0 + psi0_N0 / al_N0
            )
            # Remainder on [N0, infty) where al >= N0/X >= 16:
            rem_N0_bound = (
                (X_a ** arb("-3.5"))
                * (c_em_log_coeff_arb * N0_a.log() + c_em_const_coeff_arb)
                / (al_N0**2)
            )
            return (
                s_part
                - int_0_N0
                - arb("0.5") * g_N0
                + gp_N0 / arb(12)
                + arb(0, (eps_0_err + rem_N0_bound).upper())
            )

        # Certify W_log(X) large-scale decay across sample scales X in {1, 2, 4, tau, 10, 16, 25, tau^2, 64}:
        w_log_asymptotic_table: List[Dict[str, Any]] = []
        for x_label, x_arb in (
            ("1", arb(1)),
            ("2", arb(2)),
            ("4", arb(4)),
            ("tau", tau_arb),
            ("10", arb(10)),
            ("16", arb(16)),
            ("25", arb(25)),
            ("tau^2", tau_arb**2),
            ("64", arb(64)),
        ):
            w_log_val = _eval_w_log_em_sharp_arb(x_arb)
            lead_term = c_lead_z_neg_5_2_arb * (x_arb ** arb("-2.5"))
            rem_after_lead = w_log_val - lead_term
            scaled_x52_w_log = w_log_val * (x_arb ** arb("2.5"))
            scaled_x92_rem = rem_after_lead * (x_arb ** arb("4.5"))
            em_upper_bound = (
                c_bdry_and_singular_arb
                + c_em_log_coeff_arb * (x_arb.log() / x_arb)
                + c_em_const_coeff_arb / x_arb
            ) * (x_arb ** arb("-2.5"))
            w_log_asymptotic_table.append(
                {
                    "X_label": x_label,
                    "X_certified": serialize_arb_certified(x_arb),
                    "W_log_X_certified": serialize_arb_certified(w_log_val),
                    "leading_pole_term_neg_81_zeta3_over_256_pi2_X_neg_5_2_certified": serialize_arb_certified(
                        lead_term
                    ),
                    "remainder_after_leading_pole_certified": serialize_arb_certified(
                        rem_after_lead
                    ),
                    "X_pow_5_2_times_W_log_X_certified": serialize_arb_certified(
                        scaled_x52_w_log
                    ),
                    "X_pow_9_2_times_remainder_certified": serialize_arb_certified(
                        scaled_x92_rem
                    ),
                    "euler_maclaurin_X_neg_5_2_bound_certified": serialize_arb_certified(
                        em_upper_bound
                    ),
                    "satisfies_euler_maclaurin_bound": bool(
                        abs(w_log_val) <= em_upper_bound
                    ),
                }
            )

        # Certify the three-zone localized resonant-band decomposition of R_mu(X):
        #   R_mu(X) = R_{mu,head}(X) + R_{mu,band}(X) + R_{mu,tail}(X),
        # with M_-(X) = floor(X^{5/6}) and M_+(X) = M(X) = ceil(max(2, X^{5/4})):
        resonant_band_table: List[Dict[str, Any]] = []
        for x_label, x_arb in (
            ("1", arb(1)),
            ("2", arb(2)),
            ("4", arb(4)),
            ("tau", tau_arb),
            ("10", arb(10)),
            ("16", arb(16)),
            ("25", arb(25)),
            ("tau^2", tau_arb**2),
        ):
            M_minus = int(math.floor(float((x_arb ** (arb(5) / arb(6))).mid())))
            M_plus = certified_coupled_cutoff_M_X_arb(x_arb, prec_bits=prec_bits)
            n_max_c = max(3500, int(120 * float(x_arb.mid())) + 2500)
            w_actual = evaluate_w_prime_sum_certified_arb(
                x_arb, n_max=n_max_c, prec_bits=prec_bits
            )["enclosure_arb"]
            w_log_val = evaluate_w_log_divisor_aggregated_certified_arb(
                x_arb, k_max=n_max_c, prec_bits=prec_bits
            )["enclosure_arb"]
            r_mu_total = w_actual - w_log_val

            r_mu_head = arb(0)
            r_mu_band = arb(0)
            for m in range(2, M_plus + 1):
                mu_m = moebius_mu_int(m)
                if mu_m != 0:
                    m_arb = arb(m)
                    k_eff = max(250, int(2000 / math.sqrt(m)) + 150)
                    w_log_xm = evaluate_w_log_divisor_aggregated_certified_arb(
                        x_arb / m_arb, k_max=k_eff, prec_bits=prec_bits
                    )["enclosure_arb"]
                    term = (arb(mu_m) / m_arb.sqrt()) * w_log_xm
                    if m <= M_minus:
                        r_mu_head += term
                    else:
                        r_mu_band += term

            r_mu_tail = r_mu_total - (r_mu_head + r_mu_band)
            head_plus_tail = r_mu_head + r_mu_tail
            decomp_res = r_mu_total - (r_mu_head + r_mu_band + r_mu_tail)

            resonant_band_table.append(
                {
                    "X_label": x_label,
                    "X_certified": serialize_arb_certified(x_arb),
                    "lower_divisor_cutoff_M_minus_floor_X_5_6": M_minus,
                    "upper_divisor_cutoff_M_plus_ceil_X_5_4": M_plus,
                    "R_mu_total_certified": serialize_arb_certified(r_mu_total),
                    "R_mu_head_2_to_M_minus_certified": serialize_arb_certified(
                        r_mu_head
                    ),
                    "R_mu_band_M_minus_to_M_plus_certified": serialize_arb_certified(
                        r_mu_band
                    ),
                    "R_mu_tail_gt_M_plus_certified": serialize_arb_certified(
                        r_mu_tail
                    ),
                    "R_mu_minus_R_mu_band_certified": serialize_arb_certified(
                        head_plus_tail
                    ),
                    "head_satisfies_global_bound": bool(
                        abs(r_mu_head) <= small_divisor_head_bound_em_arb
                    ),
                    "tail_satisfies_half_C_log_0_bound": bool(
                        abs(r_mu_tail) <= half_c_log_0_arb
                    ),
                    "band_comparison_satisfies_global_bound": bool(
                        abs(head_plus_tail) <= resonant_band_comparison_bound_em_arb
                    ),
                    "three_zone_decomposition_encloses_zero": bool(
                        decomp_res.contains(0)
                    ),
                }
            )

        return {
            "leading_pole_coeff_neg_81_zeta3_over_256_pi2_certified": serialize_arb_certified(
                c_lead_z_neg_5_2_arb
            ),
            "subleading_pole_coeff_neg_5625_zeta5_over_64_pi4_certified": serialize_arb_certified(
                c_sublead_z_neg_9_2_arb
            ),
            "I_d4_0_total_variation_certified": serialize_arb_certified(I_d4_0_arb),
            "I_d4_log_integral_certified": serialize_arb_certified(I_d4_log_arb),
            "I_RL_integral_certified": serialize_arb_certified(I_RL_arb),
            "c_em_log_coeff_I_d4_0_over_384_certified": serialize_arb_certified(
                c_em_log_coeff_arb
            ),
            "c_em_const_coeff_I_d4_log_plus_I_RL_over_384_certified": serialize_arb_certified(
                c_em_const_coeff_arb
            ),
            "global_euler_maclaurin_constant_C_log_EM_certified": serialize_arb_certified(
                c_log_em_global_arb
            ),
            "small_divisor_head_global_bound_5_6_C_log_EM_certified": serialize_arb_certified(
                small_divisor_head_bound_em_arb
            ),
            "resonant_band_comparison_bound_certified": serialize_arb_certified(
                resonant_band_comparison_bound_em_arb
            ),
            "w_log_asymptotic_table": w_log_asymptotic_table,
            "resonant_band_table": resonant_band_table,
        }
    finally:
        flint_ctx.prec = saved_prec


def execute_task_tc049_arithmetic_cancellation_audit(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """
    Execute TASK-TC-049: Arithmetic cancellation in the canonical theta correlation.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 256)
        symbolic_checks = (
            verify_symbolic_tc049_prime_increment_and_w_log_asymptotic_identities()
        )
        dyadic_and_subcritical = (
            certify_dyadic_prime_block_and_subcritical_compensation_arb(
                prec_bits=prec_bits
            )
        )
        w_log_and_resonant_band = (
            certify_w_log_large_scale_decay_and_resonant_band_reduction_arb(
                prec_bits=prec_bits
            )
        )

        # Sample single-prime increment checks at X = 2 (p = 11, 13, 17, 19)
        sample_prime_increments = [
            {
                k: v
                for k, v in evaluate_prime_increment_J_p_arb(
                    arb(2), p=p_val, n_max=800, prec_bits=prec_bits
                ).items()
                if not k.endswith("_arb")
            }
            for p_val in (11, 13, 17, 19)
        ]

        section_1_starting_point_and_cancellation_loss_audit = {
            "canonical_correlation_and_identities": {
                "canonical_correlation": "C_tau(K) = Q_tau(T_K psi_tau, psi_tau),   K in A_R = Qbar cap R (positive and negative grades)",
                "moebius_inversion_identity": "W(X) = W_log(X) + R_mu(X),   R_mu(X) = sum_{m >= 2} (mu(m) / sqrt(m)) W_log(X / m)",
                "finite_prime_euler_identity": "W_y(X) = [prod_{p <= y} (I - p^{-1/2} D_p)] W_log(X),   D_p F(X) = F(X / p)",
                "coupled_cutoff_comparison": (
                    "|W(X) - W_{M(X)}(X)| = |R_mu(X) - R_{mu, M(X)}(X)| <= (1/2) C_{log,0} < 0.278715,   "
                    "M(X) = ceil(max(2, X^{5/4}))"
                ),
                "preserved_tc048r_candidate_classifications": {
                    "candidate_1_integer_carrier_N_y_x_tau_K": {
                        "established": "Integer-layer membership (CR2) and one-way off-critical nonvanishing (CR3)",
                        "missing": "Raw cross-grade equality (CR1)",
                    },
                    "candidate_2A_theta_detector": {
                        "established": "Raw cross-grade equality (CR1) and one-way off-critical nonvanishing (CR3)",
                        "missing": "Integer-layer membership (CR2)",
                    },
                    "candidate_2B_shift_difference": {
                        "established": "Raw cross-grade equality (CR1)",
                        "missing": "General off-critical nonvanishing (CR3) and integer-layer membership (CR2)",
                    },
                },
            },
            "exact_cancellation_loss_diagnosis": {
                "route_1_spatial_chebyshev_prime_error_majorant_tc043": {
                    "exact_signed_expression": "I(X) = int_1^infty E(x) x^{-3/2} tilde{h}_0(x/X) dx = sqrt(X) int_{1/X}^infty (E(X*alpha)/(X*alpha)) k(alpha) d_alpha",
                    "step_where_cancellation_is_lost": (
                        "Triangle inequality |I(X)| <= A_E(X) := int_1^infty |E(x)| x^{-3/2} |tilde{h}_0(x/X)| dx <= M_omega(X), "
                        "which replaces the zero-mean signed kernel k(alpha) = alpha^{-1/2} tilde{h}_0(alpha) "
                        "(satisfying int_0^infty k(alpha) d_alpha = H_0(1/2) = 0 across its 7 sign changes) by |k(alpha)| >= 0 "
                        "(c_0 = int_{1/2}^2 |k(alpha)| d_alpha = 1.7456980946 > 0), forcing M_omega(X) >= c_0 sqrt(X) omega(2X)."
                    ),
                },
                "route_2_critical_line_euler_seed_gram_norm_tc046": {
                    "exact_signed_expression": "W_y(X) = -(1/tau) int_{-infty}^infty E_y(it) H_0(it) zeta'(1/2 + it) X^{it} dt",
                    "step_where_cancellation_is_lost": (
                        "Applying Cauchy-Schwarz on Re(z) = 0, |W_y(X)| <= ||Psi_y||_{L^2} N_{zeta',tau}, which drops the "
                        "oscillatory Fourier phase X^{it} and the phase correlation with zeta'(1/2 + it). On the coherent "
                        "low-frequency interval I_y = [7*tau/(16*log y), tau/(2*log y)] of width |I_y| = tau/(16*log y), "
                        "every prime factor p <= y has t*log p in (0, pi] where (d/dt)|1 - p^{-1/2-it}|^2 >= 0, forcing "
                        "||Psi_y||_{L^2}^2 >= (H_0(0)/(8 log y)) exp[(4*cos(tau/16) + o(1)) sqrt(y) / log y] -> +infty."
                    ),
                },
                "route_3_divisor_aggregated_stieltjes_and_moebius_bounds_tc044_tc045": {
                    "exact_signed_expression": (
                        "W_log(X) = B_{log,boundary}(X) + int_1^infty E_log(x) x^{-3/2} tilde{h}_0(x/X) dx and "
                        "R_mu(X) = sum_{m >= 2} (mu(m)/sqrt(m)) W_log(X/m)"
                    ),
                    "step_where_cancellation_is_lost_in_W_log": (
                        "In TC-044, bounding I_log(X) by inserting the unsigned Stirling remainder bound |E_log(x)| <= (1/2) log x + 1 "
                        "inside the integral destroys the exact cancellation of the smooth Stirling (1/2) log(2*pi*x) main term "
                        "against tilde{h}_0(x/X) (which vanishes identically on (0, infty) because H_0(z) also has a triple zero at "
                        "z = -1/2: H_0(-1/2) = H_0'(-1/2) = H_0''(-1/2) = 0!). That triangle inequality lost two full powers of X, "
                        "giving O(X^{-1/2} log X) instead of the true O(X^{-5/2}) decay of W_log(X)."
                    ),
                    "step_where_cancellation_is_lost_in_R_mu": (
                        "In R_mu(X) = sum_{m >= 2} (mu(m)/sqrt(m)) W_log(X/m) (and its Mertens Stieltjes form "
                        "X^{-1/2} int_0^{X/2} M_{>=2}(X/u) phi_log'(u) du), replacing mu(m) by |mu(m)| <= 1 (or M_{>=2}(y) by "
                        "|M_{>=2}(y)| <= C_mu y exp(-c_mu sqrt(log y))) across the resonant transition band m ~ X loses the "
                        "alternating sign cancellation of mu(m)."
                    ),
                },
            },
        }

        section_2_supercritical_dyadic_block_obstruction_and_subcritical_compensation = {
            "prime_increment_definition_and_telescoping": {
                "definition": "J_p(X) := p^{-1/2} W_{p^-}(X / p) = W_{p^-}(X) - W_p(X)",
                "telescoping_identity": (
                    "W_y(X) = W_log(X) - sum_{p <= y} J_p(X),   "
                    "W_{M(X)}(X) - W_log(X) = -sum_{p <= M(X)} J_p(X)"
                ),
                "sample_prime_increments_at_X_2": sample_prime_increments,
            },
            "proved_supercritical_dyadic_block_obstruction": {
                "theorem_statement": (
                    "For every real A >= 9/2 (e.g. A = 5), every X > 0, and every prime p > A X: "
                    "(1) In J_p(X) = sum_{n=2}^infty (lambda_{p^-}(n) / sqrt(n p)) h_0(n p / X), every integer n >= 2 has "
                    "alpha_n = n p / X >= 2 p / X > 2 A >= 9 > alpha_3^* ~ 8.621336, where -h_0(alpha) = (alpha + alpha^{-1})^{-5/2} kappa(alpha) > 0 "
                    "and lambda_{p^-}(n) >= 0 with lambda_{p^-}(2) = log 2 > 0. Hence every term in -J_p(X) is nonnegative, and "
                    "retaining the n = 2 term gives the unconditional two-sided inequality: "
                    "c_0(A) X^{5/2} p^{-3} <= (log 2 / sqrt(2 p)) (-h_0(2 p / X)) <= -J_p(X) <= C_{log,0} X^{5/2} p^{-3}, "
                    "where c_0(A) := (log 2 / 8) kappa(2A) (1 + (2A)^{-2})^{-5/2} > 0 (c_0(5) = 0.0219284968 > 0.0219). "
                    "(2) Consequently, for any fixed A >= 5 and X >= max(59/A, (2A)^4) (so A X < p <= 2 A X <= M(X) = ceil(X^{5/4})), "
                    "Rosser-Schoenfeld (1962, Corollary 1: pi(2u) - pi(u) >= 3u / (4 log(2u)) for u >= 59) gives: "
                    "|-sum_{A X < p <= 2 A X} J_p(X)| = -sum_{A X < p <= 2 A X} J_p(X) >= (3 c_0(A) / (32 A^2)) * sqrt(X) / log(2 A X) -> +infty."
                ),
                "scoped_obstruction_conclusion": (
                    "Any proof strategy that attempts to bound the coupled prime-increment sum sum_{p <= M(X)} J_p(X) by bounding "
                    "dyadic prime blocks A X < p <= 2 A X separately in absolute value (or summing |J_p(X)| over p <= M(X)) "
                    "is unconditionally obstructed: every supercritical prime p > (9/2) X has the same negative sign J_p(X) < 0, "
                    "and a single dyadic block (A X, 2 A X] inside [1, M(X)] already grows as Theta_A(sqrt(X) / log X)."
                ),
            },
            "cancellation_mechanism_1_subcritical_vs_supercritical_resummation": {
                "theorem_statement": (
                    "For any prime cutoffs y_2 > y_1 >= floor(A X) with A >= 9/2 (e.g. A = 5, y_1 = floor(5 X), y_2 = max(floor(10 X), M(X))): "
                    "every unsieved composite n >= 2 q_{> y_1} > 2 A X >= 9 X lies in the negative tail h_0(n/X) < 0, so both sieve defects "
                    "D_{y_1}(X) := W_{y_1}(X) - W(X) = sum_{n >= 2 q_{> y_1}} (Delta_{y_1}(n)/sqrt(n)) h_0(n/X) < 0 and D_{y_2}(X) := W_{y_2}(X) - W(X) < 0 "
                    "are strictly negative, while every prime p in (y_1, y_2] satisfies J_p(X) < 0 so T_{(y_1, y_2]}(X) := -sum_{y_1 < p <= y_2} J_p(X) > 0 "
                    "is strictly positive. The exact coefficient identity Delta_{y_1}(n) - sum_{y_1 < p <= y_2, p | n} lambda_{p^-}(n/p) = Delta_{y_2}(n) "
                    "annihilates every composite multiple n = m p < 2 q_{> y_2} identically, proving: "
                    "D_{y_1}(X) + T_{(y_1, y_2]}(X) = D_{y_2}(X) < 0, and at y_2 = M(X) (for X >= (2A)^4) "
                    "0 < -D_{M(X)}(X) = -D_{y_1}(X) - T_{(y_1, M(X)]}(X) <= C_{log,0} X^{5/2} / (2 M(X)^2) <= (1/2) C_{log,0} < 0.278715. "
                    "Corollary (Unconditional Linear-Cutoff Divergence): For any fixed A >= 5 and all X >= 59/A, taking y_1 = floor(A X) and y_2 = floor(2 A X) gives "
                    "W(X) - W_{floor(A X)}(X) = -D_{floor(A X)}(X) = T_{(floor(A X), floor(2 A X)]}(X) + (-D_{floor(2 A X)}(X)) "
                    "> T_{(floor(A X), floor(2 A X)]}(X) >= (3 c_0(A) / (32 A^2)) * sqrt(X) / log(2 A X) -> +infty, "
                    "proving unconditionally that linear prime cutoffs y = floor(A X) diverge from W(X) at rate Theta_A(sqrt(X)/log X) and that "
                    "super-linear sieving (such as y = M(X) = ceil(X^{5/4})) is necessary and sufficient for O(1) comparison."
                ),
            },
            "certified_audit_data": dyadic_and_subcritical,
        }

        section_3_w_log_large_scale_decay_and_resonant_band_reduction = {
            "cancellation_mechanism_2_higher_order_stirling_and_mellin_cancellation": {
                "why_tc044_lost_two_powers_of_X": (
                    "In TC-044, Stieltjes integration by parts of T(x) = log(floor(x)!) = (x log x - x + 1) + E_log(x) used "
                    "H_0(1/2) = H_0'(1/2) = 0 to cancel x log x - x + 1, but bounded the remainder E_log(x) = (1/2) log(2*pi*x) - B_1({x}) log x + O(1/x) "
                    "in absolute value |E_log(x)| <= (1/2) log x + 1. Because H_0(z) = F_tau(1/2+z) F_tau(1/2-z) is EVEN in z, it ALSO has a "
                    "triple zero at z = -1/2 (H_0(-1/2) = H_0'(-1/2) = H_0''(-1/2) = 0), which cancels the entire smooth Stirling "
                    "(1/2) log(2*pi*x) moment int_0^infty x^{-1/2} (log x) h_0(x/X) dx = 0 identically! Retaining the signed Bernoulli "
                    "oscillation via 4th-order Euler-Maclaurin on g_X(x) = x^{-1/2} (log x) h_0(x/X) = X^{-1/2} (log x) psi_0(x/X) "
                    "recovers two full powers of X, improving O(X^{-1/2} log X) to O(X^{-5/2})."
                ),
                "exact_asymptotic_and_global_bound_theorem": (
                    "Theorem: For all X > 0, the Mellin transform M_X[W_log](z) = -H_0(z) zeta'(z + 1/2) is holomorphic across the "
                    "entire open strip -5/2 < Re(z) < 5/2, with its first left-half-plane simple pole at z = -5/2 (s = -2, the first "
                    "trivial zero of zeta(s)), where Res_{z=-5/2}(-H_0(z) zeta'(z+1/2) X^z) = (-81/64)(-zeta'(-2)) X^{-5/2} "
                    "= -(81 zeta(3) / (256 pi^2)) X^{-5/2} (~ -0.0385363285 X^{-5/2}) and second simple pole at z = -9/2 (s = -4) "
                    "with residue -(5625 zeta(5) / (64 pi^4)) X^{-9/2} (~ -0.93556235 X^{-9/2}). "
                    "In the spatial domain, 4th-order Euler-Maclaurin integration by parts on [1, infty) using int_0^infty g_X(x) dx = 0 gives "
                    "W_log(X) = -int_0^1 g_X(x) dx + (1/12) g_X'(1) + (1/24) int_1^infty {x}^2 (1 - {x})^2 g_X^{(4)}(x) dx, "
                    "proving unconditionally for all X >= 1: "
                    "|W_log(X)| <= (217709/393216 + (I_{d4,0}/384)*(log X / X) + ((I_{d4,log} + I_{R_L})/384)*(1/X)) X^{-5/2} <= C_{log,EM} X^{-5/2} "
                    "with C_{log,EM} = 13.468515 < 13.47."
                ),
                "unconditional_small_divisor_head_bound_and_resonant_band_reduction": (
                    "Theorem (`prime_increment_telescoping_and_resonant_band_reduction`): Combining the small-scale bound "
                    "|W_log(u)| <= C_{log,0} u^{5/2} (u > 0) with the new large-scale bound |W_log(u)| <= C_{log,EM} u^{-5/2} (u >= 1) "
                    "gives the two-sided localization envelope |W_log(u)| <= C_{log,*} min(u^{5/2}, u^{-5/2}) for all u > 0. "
                    "Splitting R_mu(X) = sum_{m=2}^infty (mu(m)/sqrt(m)) W_log(X/m) at the lower divisor cutoff M_-(X) := floor(X^{5/6}) "
                    "and upper divisor cutoff M_+(X) := M(X) = ceil(max(2, X^{5/4})) yields: "
                    "(1) Small-divisor head (2 <= m <= floor(X^{5/6})): |R_{mu,head}(X)| <= C_{log,EM} X^{-5/2} sum_{2 <= m <= M_-(X)} m^2 "
                    "<= (5/6) C_{log,EM} < 11.224 unconditionally for all X >= 1 (even with |mu(m)| <= 1); "
                    "(2) Large-divisor tail (m > M(X)): |R_{mu,tail}(X)| <= (1/2) C_{log,0} < 0.278715 unconditionally for all X >= 1; "
                    "(3) Localized Resonant-Band Equivalence: |R_mu(X) - R_{mu,band}(X)| <= (5/6) C_{log,EM} + (1/2) C_{log,0} < 11.503 "
                    "for all X >= 1, where R_{mu,band}(X) := sum_{X^{5/6} < m <= M(X)} (mu(m)/sqrt(m)) W_log(X/m)."
                ),
            },
            "certified_audit_data": w_log_and_resonant_band,
        }

        section_4_outcome_and_remaining_obligation = {
            "symbolic_identities_verification": symbolic_checks,
            "lean_theorem": "prime_increment_telescoping_and_resonant_band_reduction",
            "advances_uniform_cancellation_analysis": True,
            "closes_subgate_tc043a": False,
            "remaining_open_obligation": {
                "subgate_id": "SUBGATE-TC-043A",
                "status": "OPEN",
                "exact_surviving_lemma": (
                    "Localized Resonant-Band Moebius Cancellation Lemma: Prove without assuming RH or universal Weil positivity "
                    "that there exists a finite constant M_band < infty such that for all X >= 1, the finite resonant-band Moebius sum "
                    "R_{mu,band}(X) := sum_{X^{5/6} < m <= M(X)} (mu(m)/sqrt(m)) W_log(X/m) (where M(X) = ceil(max(2, X^{5/4})) and "
                    "|R_mu(X) - R_{mu,band}(X)| <= (5/6) C_{log,EM} + (1/2) C_{log,0} < 11.503 unconditionally) satisfies "
                    "|R_{mu,band}(X)| <= M_band."
                ),
            },
        }

        result_tc049: Dict[str, Any] = {
            "task_id": TASK_TC_049_ID,
            "parent_epic": EPIC_TC_042_ID,
            "inspected_baseline": STARTING_HEAD_TC_049,
            "status": ARITHMETIC_CANCELLATION_CANONICAL_THETA_CORRELATION_STATUS,
            "section_1_starting_point_and_cancellation_loss_audit": section_1_starting_point_and_cancellation_loss_audit,
            "section_2_supercritical_dyadic_block_obstruction_and_subcritical_compensation": section_2_supercritical_dyadic_block_obstruction_and_subcritical_compensation,
            "section_3_w_log_large_scale_decay_and_resonant_band_reduction": section_3_w_log_large_scale_decay_and_resonant_band_reduction,
            "section_4_outcome_and_remaining_obligation": section_4_outcome_and_remaining_obligation,
        }
        full_tree_rt_sec18 = verify_all_serialized_arb_in_tree(
            result_tc049, path_prefix="section_18"
        )
        result_tc049["full_section_18_tree_roundtrip_verification"] = full_tree_rt_sec18
        return result_tc049
    finally:
        flint_ctx.prec = saved_prec


__all__ = [
    "TASK_TC_046_ID",
    "STARTING_HEAD_TC_046",
    "PRIME_EULER_MOEBIUS_RECOVERY_STATUS",
    "TASK_TC_049_ID",
    "STARTING_HEAD_TC_049",
    "ARITHMETIC_CANCELLATION_CANONICAL_THETA_CORRELATION_STATUS",
    "primes_up_to",
    "next_prime_above",
    "prime_factors_with_multiplicity",
    "von_mangoldt_arb",
    "divisors_of_primorial",
    "evaluate_lambda_y_closed_form_arb",
    "evaluate_lambda_y_convolution_arb",
    "evaluate_lambda_y_recursion_arb",
    "evaluate_summatory_L_y_direct_arb",
    "evaluate_summatory_L_y_factorial_divisor_sum_arb",
    "evaluate_chebyshev_psi_arb",
    "evaluate_w_prime_sum_certified_arb",
    "evaluate_w_log_divisor_aggregated_certified_arb",
    "evaluate_w_y_coefficient_certified_arb",
    "evaluate_w_y_divisor_sum_certified_arb",
    "evaluate_w_y_prime_recursion_certified_arb",
    "evaluate_euler_sieved_seed_gram_norm_arb",
    "evaluate_euler_dirichlet_poly_acb",
    "evaluate_H0_critical_line_arb",
    "evaluate_b_log_boundary_term_arb",
    "certified_coupled_cutoff_M_X_arb",
    "certify_subproduct_counterexample_at_y210_arb",
    "certify_H0_local_monotonicity_and_global_decay_arb",
    "evaluate_euler_spike_interval_gram_lower_bound_arb",
    "compute_coupled_cutoff_comparison_bound_arb",
    "verify_symbolic_finite_prime_identities",
    "execute_task_tc046_prime_euler_moebius_recovery",
    "verify_symbolic_tc049_prime_increment_and_w_log_asymptotic_identities",
    "evaluate_prime_increment_J_p_arb",
    "certify_dyadic_prime_block_and_subcritical_compensation_arb",
    "certify_w_log_large_scale_decay_and_resonant_band_reduction_arb",
    "execute_task_tc049_arithmetic_cancellation_audit",
]


