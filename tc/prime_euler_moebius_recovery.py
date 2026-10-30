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
    Compute the certified coupled prime cutoff M(X) = ceil(max(2, X^{5/4}))
    directly from the Arb ball enclosure of X^{5/4} = (X^5)^{1/4} without
    passing through binary64 float conversion.

    Certifies in Arb ball arithmetic that arb(M_X) >= X^{5/4} and
    arb(M_X)^2 >= X^{5/2}.
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


def evaluate_euler_spike_interval_gram_lower_bound_arb(
    y: int, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Certify the controlled-width frequency interval lower bound on the Euler-sieved
    seed Gram norm squared ||Psi_y||_{L^2(d^*x)}^2 across
      I_y := [t_{y,-}, t_{y,+}] = [7*pi / (8*log y), pi / log y],
      |I_y| = pi / (8*log y) > 0.

    Because for every prime p <= y and every t in [0, pi / log y] the phase
    t*log(p) lies in [0, pi] where sin(t*log p) >= 0, each factor
    g_p(t) = 1 + p^{-1} - 2*p^{-1/2}*cos(t*log p) is monotonically non-decreasing
    in t on I_y, so inf_{t in I_y} |E_y(it)|^2 = |E_y(i t_{y,-})|^2 exactly.
    Likewise H_0(it) is strictly increasing in |t| on [0, infty), so
    inf_{t in I_y} H_0(it) = H_0(i t_{y,-}) >= H_0(0) > 0.
    By Plancherel's identity and evenness of |E_y(it)|^2 H_0(it) on (-I_y) union I_y:
      ||Psi_y||_{L^2}^2 >= (2 / tau) int_{t_{y,-}}^{t_{y,+}} |E_y(it)|^2 H_0(it) dt
                        >= (2 |I_y| / tau) |E_y(i t_{y,-})|^2 H_0(i t_{y,-})
                        = (H_0(i t_{y,-}) / (8 log y)) |E_y(i t_{y,-})|^2
                        >= (H_0(0) / (8 log y)) |E_y(i t_{y,-})|^2.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        ps = primes_up_to(y)
        y_arb = arb(y)
        log_y_arb = y_arb.log()
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

        # Since 2 * |I_y| / tau = 2 * (pi / (8 log y)) / (2 pi) = 1 / (8 log y):
        gram_sq_lb_H0_0_arb = (
            H0_at_0_arb / (arb(8) * log_y_arb)
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
            "gram_sq_lb_H0_0_arb": gram_sq_lb_H0_0_arb,
            "gram_sq_lb_H0_minus_arb": gram_sq_lb_H0_minus_arb,
            "monotonicity_verified": bool(e_sq_at_minus_arb <= e_sq_at_plus_arb),
            "H0_monotonicity_verified": bool(
                H0_at_0_arb <= H0_at_minus_arb and H0_at_minus_arb <= H0_at_plus_arb
            ),
        }
    finally:
        flint_ctx.prec = saved_prec


def compute_coupled_cutoff_comparison_bound_arb(
    X: arb, prec_bits: int = 256
) -> Dict[str, Any]:
    """
    Compute the coupled prime cutoff M(X) = ceil(max(2, X^{5/4})) directly in Arb
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
                    "scale space (0, infty); the resulting continuous profile W_y(X) is then restricted to admissible grade "
                    "scales X = tau^{|K - L|} (K, L in A_R), where density of A_R in R and continuity of W_y imply "
                    "sup_{K in A_R} |W_y(tau^{|K|})| = sup_{X >= 1} |W_y(X)|."
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
        #     controlled-width frequency interval I_y = [t_{y,-}, t_{y,+}] = [7*pi / (8*log y), pi / log y]
        #     of width |I_y| = pi / (8*log y) in 256-bit Arb across y in {2, 5, 11, 31, 97, 199, 499, 997, 1999, 4999, 9973}
        f_half_acb = evaluate_f_tau_acb(acb(arb(1) / arb(2)))
        H0_at_0_arb = (f_half_acb * f_half_acb).real
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
            gram_lb_0_arb = spike_info["gram_sq_lb_H0_0_arb"]
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
                    "H0_at_i_t_y_certified": serialize_arb_certified(H0_plus_arb),
                    "H0_at_i_t_y_exceeds_H0_at_0": bool(H0_plus_arb >= H0_at_0_arb),
                    "interval_monotonicity_E_y_sq_and_H0_verified": bool(
                        spike_info["monotonicity_verified"]
                        and spike_info["H0_monotonicity_verified"]
                    ),
                    "integrated_gram_norm_sq_lower_bound_via_H0_0_certified": serialize_arb_certified(
                        gram_lb_0_arb
                    ),
                    "integrated_gram_norm_sq_lower_bound_via_H0_minus_certified": serialize_arb_certified(
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
                    "On the controlled-width frequency interval I_y := [t_{y,-}, t_{y,+}] = [7*pi / (8*log y), pi / log y] "
                    "of width |I_y| = pi / (8*log y) > 0, every prime p <= y and every t in [0, pi / log y] has phase "
                    "t*log(p) in [0, pi] where (d/dt)(1 + p^{-1} - 2*p^{-1/2}*cos(t*log p)) = 2*p^{-1/2}*(log p)*sin(t*log p) >= 0. "
                    "Thus |E_y(it)|^2 is monotonically non-decreasing in t on I_y, with exact interval minimum at the left endpoint: "
                    "inf_{t in I_y} |E_y(it)|^2 = |E_y(i t_{y,-})|^2 >= exp((4 + o(1)) sqrt(y) / log y) "
                    "(since every prime p in [y^{16/21}, y] has t*log(p) in [2*pi/3, pi] with -cos(t*log p) >= 1/2 throughout I_y), "
                    "while inf_{t in I_y} H_0(it) = H_0(i t_{y,-}) >= H_0(0) = F_tau(1/2)^2 = 2.82909344e-5 > 0. "
                    "Integrating over (-I_y) union I_y gives the rigorous integrated Gram-norm lower bound "
                    "||Psi_y||_{L^2(d^*x)}^2 >= (2/tau) int_{t_{y,-}}^{t_{y,+}} |E_y(it)|^2 H_0(it) dt "
                    ">= (2 |I_y| / tau) |E_y(i t_{y,-})|^2 H_0(i t_{y,-}) "
                    ">= (H_0(0) / (8 log y)) |E_y(i t_{y,-})|^2 = exp((4 + o(1)) sqrt(y) / log y) -> +infty as y -> infty "
                    "(reaching >= 153.39 at y = 9973). "
                    "Scope: this establishes divergence of the unsplit critical-line Cauchy-Schwarz / Gram-norm bound as y -> infty "
                    "(because keeping E_y(it) factored on Re(z) = 0 retains all 2^{pi(y)} divisors m | P_y up to P_y ~ e^y "
                    "without the right-shift spatial decay O((X/m)^{5/2}) that suppresses m > X); it does NOT establish failure "
                    "of the coupled profile W_{M(X)}(X) or of the broader concurrent-grade hypothesis."
                ),
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
            "coupled_cutoff_schedule": "y = M(X) := ceil(max(2, X^{5/4})) for X >= 1 (computed directly from Arb ball enclosure of (X^5)^{1/4} without float conversion)",
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
                "<==>  sup_{X >= 1} |W_{M(X)}(X)| < infty  <==>  sup_{X >= 1} |R_{mu, M(X)}(X)| < infty"
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
                "Quantified Dual Obstruction (Controlled-Width Coherent Euler Spike vs. Coupled-Cutoff Horizon Collapse): (1) On the critical line Re(z) = 0, holomorphy of M_X[W_y](z) = -E_y(z) H_0(z) zeta'(z+1/2) yields sup_{X > 0} |W_y(X)| <= ||Psi_y||_{L^2} N_{zeta',tau}, but on the controlled-width frequency interval I_y = [7*pi / (8*log y), pi / log y] of width |I_y| = pi / (8*log y), monotonicity of each prime factor proves inf_{t in I_y} |E_y(it)|^2 = |E_y(i t_{y,-})|^2 >= exp((4+o(1)) sqrt(y)/log y) and ||Psi_y||_{L^2}^2 >= (H_0(0)/(8 log y)) |E_y(i t_{y,-})|^2 -> +infty, establishing divergence of the unsplit Cauchy-Schwarz/Gram-norm bound (without refuting boundedness of the coupled profile W_{M(X)}(X) or the broader concurrent-grade hypothesis); (2) splitting at the coupled cutoff M(X) = ceil(max(2, X^{5/4})) bounds the m > M(X) tail by (1/2) C_{log,0} < 0.278715, but for y >= M(X) every squarefree m <= M(X) divides P_y, collapsing the m <= M(X) sum identically to W_log(X) + R_{mu, M(X)}(X).",
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


__all__ = [
    "TASK_TC_046_ID",
    "STARTING_HEAD_TC_046",
    "PRIME_EULER_MOEBIUS_RECOVERY_STATUS",
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
    "evaluate_euler_spike_interval_gram_lower_bound_arb",
    "compute_coupled_cutoff_comparison_bound_arb",
    "verify_symbolic_finite_prime_identities",
    "execute_task_tc046_prime_euler_moebius_recovery",
]

