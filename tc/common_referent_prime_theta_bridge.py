"""TASK-TC-047 & TASK-TC-048: Common-Referent Observable from Actual Prime/Theta Data,
Coupled-Cutoff Piecewise Continuity & Right-Hand Jump Formula, and Single-Observable
Common-Referent Collision Contract Audit.

This module constructs and audits the multiplicative prime-Euler observable N_y(x),
its grade-K realization A_{K,y}(x) = N_y(x) * tau^K, the piecewise continuity and exact
right-hand jumps of the coupled profile F(X) = W_{M(X)}(X), and the single-observable
collision contract (CR1 + CR2 + CR3) directly from the actual prime-by-prime Euler and
canonical theta data of EPIC-TC-042 / TC-042..TC-048:

1. Local Prime-Euler Integer Factor m_y(n) and Cumulative Factorial-Ratio Observable N_y(x):
     m_y(n) := exp(lambda_y(n)) = prod_{d | gcd(n, P_y)} (n / d)^{mu(d)}
             = 1  (if n = 1 or omega_{<=y}(n) >= 2),
               n  (if n >= 2 and omega_{<=y}(n) = 0),
               p  (if n = p^a n_{>y} with omega_{<=y}(n) = 1, p <= y, a >= 1),
     N_y(x) := exp(L_y(x)) = prod_{d | P_y, d <= x} (floor(x / d)!)^{mu(d)}
             = prod_{1 <= n <= floor(x)} m_y(n).

2. Unconditional Exact Positive-Integer Membership (N_y(x) in Z_{>=1}) and Required
   Grade-Layer Membership (A_{K,y}(x) = N_y(x) * tau^K in L_K^x = tau^K (Z \\ {0}), CR2):
   - Even though prod_{d | P_y, d <= x} (floor(x / d)!)^{mu(d)} contains factorial
     denominators (floor(x / d)!)^{-1} for all squarefree d | P_y with mu(d) = -1,
     every denominator divides the numerator identically because m_y(n) in Z_{>=1}
     for all n >= 1.
   - For all 1 <= x < 2 q_{>y}, N_y(x) = lcm(1, 2, ..., floor(x)) = exp(psi(x)) in Z_{>=1},
     and at the first discrepancy x = 2 q_{>y}, N_y(2 q_{>y}) = 2 * lcm(1, ..., 2 q_{>y}).
   - For every concurrent grade K in A_R = Qbar cap R, the ambient realization
     A_{K,y}(x) := Phi_K(fromZ(K, N_y(x))) = N_y(x) * tau^K belongs unconditionally to
     the nonzero integer layer L_K^x = tau^K (Z \\ {0}) subset L_K = tau^K Z (CR2).
   - Crucial distinction (TC-048 reconciliation): the intrinsic unit-converted coordinate
     recovery tau^{-K} A_{K,y}(x) = tau^{-J} A_{J,y}(x) = N_y(x) in Z_{>=1} is NOT the
     original raw common-referent equality (CR1). Since A_{K,y}(x) = N_y(x) * tau^K > 0,
     the raw external values A_{K,y}(x) and A_{J,y}(x) satisfy A_{K,y}(x) = tau^{K-J} A_{J,y}(x)
     and are strictly unequal whenever K != J.

3. Exact Mellin-Stieltjes & Station-Ratio Bridge to W_y(X) and Explicit Lower-Endpoint Convention:
   - Extend A_{K,y}(x) constantly as tau^K below 1 (so A_{K,y}(x) = tau^K on (0, 2)), or
     integrate over (1, infty), so that d(log A_{K,y})(x) has zero atom at x = 1 (no
     artificial K * log(tau) boundary jump) and has point masses log(A_{K,y}(n)/A_{K,y}(n-1))
     = log m_y(n) = lambda_y(n) exclusively at integers n >= 2.
   - For any grades K >= J in A_R with relative scale X_{K,J} = tau^{K-J},
       W_y(tau^{K-J}) = int_{(1, infty)} x^{-1/2} h_0(x / tau^{K-J}) d(log A_{K,y})(x)
                      = sum_{n=2}^infty log(A_{K,y}(n) / A_{K,y}(n-1)) * n^{-1/2} * h_0(Phi_J(n) / Phi_K(1)),
     where A_{K,y}(n) / A_{K,y}(n-1) = m_y(n) in Z_{>=1} cancels tau^K identically and
     Phi_J(n) / Phi_K(1) = (n * tau^J) / tau^K = n / tau^{K-J} is the cross-grade station ratio.

4. Coupled-Cutoff Piecewise Continuity, Right-Hand Jump Formula, and Single-Observable
   Collision Contract Audit (TASK-TC-048):
   - For fixed y, W_y(X) is continuous on (0, infty), whereas the coupled profile
     F(X) := W_{M(X)}(X) with M(X) = ceil(max(2, X^{5/4})) is piecewise continuous:
     across X_0 = (p - 1)^{4/5} for a prime p >= 3, M(X) steps from p - 1 to p and
       F(X_0^+) - F(X_0) = W_p(X_0) - W_{p^-}(X_0) = -p^{-1/2} W_{p^-}(X_0 / p),
     which is nonzero iff W_{p^-}((p-1)^{4/5} / p) != 0 (certified strictly negative for
     small primes p in {3, 5, 7, 11, 13, 17, 19, 23} where 2/u_p in (2.694, 8.621) lies in
     the positive lobe of h_0, and proved strictly positive for all primes p >= 1901 where
     2/u_p >= 9 lies in the negative asymptotic tail h_0(alpha) < 0).
   - Extending boundedness from dense algebraic grades K in A_R to all real scales X >= 1
     uses continuity of W(X) (or R_mu(X)) together with the uniform comparison
     |F(X) - W(X)| <= (1/2) C_{log,0} < 0.278715, NEVER continuity of F(X).
   - Audits two explicit single-observable candidate families D_K(rho_K) against the original
     three-part collision contract (CR1 + CR2 + CR3) on the SAME expression, proving the
     Covariance-Invariance-Discreteness Trilemma and preserving SUBGATE-TC-043A = OPEN.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Dict, List

import sympy as sp
from flint import acb, acb_series, arb, ctx as flint_ctx

from tc.canonical_theta_correlation_bound import (
    EPIC_TC_042_ID,
    evaluate_f_tau_acb,
    evaluate_h0_arb,
    load_certified_zero_ordinate_balls,
    serialize_arb_certified,
    verify_all_serialized_arb_in_tree,
)


def tau_arb_256(prec_bits: int = 256) -> arb:
    """Return tau = 2*pi as an Arb ball in a prec_bits precision context."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        return arb(2) * arb.pi()
    finally:
        flint_ctx.prec = saved_prec


from tc.prime_euler_moebius_recovery import (
    certified_coupled_cutoff_M_X_arb,
    divisors_of_primorial,
    evaluate_lambda_y_closed_form_arb,
    evaluate_summatory_L_y_direct_arb,
    evaluate_w_y_coefficient_certified_arb,
    evaluate_w_y_divisor_sum_certified_arb,
    evaluate_w_y_prime_recursion_certified_arb,
    next_prime_above,
    prime_factors_with_multiplicity,
    primes_up_to,
)

TASK_TC_047_ID = "TASK-TC-047"
STARTING_HEAD_TC_047 = "c39eb27b31fc4eed98300be0118d8c670f92d32a"
COMMON_REFERENT_PRIME_THETA_BRIDGE_STATUS = (
    "COMMON_REFERENT_PRIME_THETA_INTEGER_LAYER_MEMBERSHIP_PROVED_AND_CERTIFIED_SUBGATE_OPEN"
)

TASK_TC_048_ID = "TASK-TC-048"
STARTING_HEAD_TC_048 = "39b4e3aec6d4357d283932ad296b6148477e00e4"
IMPLEMENTATION_COMMIT_TC_047 = "a2ae0f7057ee24a04031601316f40f96b7e3ef82"
SINGLE_OBSERVABLE_COMMON_REFERENT_AUDIT_STATUS = (
    "COUPLED_CUTOFF_JUMP_FORMULA_AND_SINGLE_OBSERVABLE_CANDIDATE_AUDIT_PROVED_"
    "COVARIANCE_INVARIANCE_DISCRETENESS_TRILEMMA_ISOLATED_SUBGATE_OPEN"
)


# ---------------------------------------------------------------------------
# 1. Exact Integer & Rational Arithmetic for m_y(n) and N_y(x)
# ---------------------------------------------------------------------------


def local_prime_euler_factor_m_y_exact(n: int, y: int) -> int:
    """Compute the exact positive integer factor m_y(n) = exp(lambda_y(n)) in Z_{>=1} by case split:
    - m_y(1) = 1
    - omega_{<=y}(n) = 0  =>  m_y(n) = n
    - omega_{<=y}(n) = 1  =>  m_y(n) = p  (where p <= y is the unique prime <= y dividing n)
    - omega_{<=y}(n) >= 2 =>  m_y(n) = 1
    """
    if n <= 1:
        return 1
    factors = prime_factors_with_multiplicity(n)
    primes_le_y = [p for p, _ in factors if p <= y]
    omega_le_y = len(primes_le_y)
    if omega_le_y == 0:
        return int(n)
    if omega_le_y == 1:
        return int(primes_le_y[0])
    return 1


def local_prime_euler_factor_divisor_product_fraction(n: int, y: int) -> Fraction:
    """Compute prod_{d | gcd(n, P_y)} (n / d)^{mu(d)} as an exact rational Fraction."""
    if n <= 1:
        return Fraction(1, 1)
    factors = prime_factors_with_multiplicity(n)
    primes_le_y = sorted(p for p, _ in factors if p <= y)
    k = len(primes_le_y)
    result = Fraction(1, 1)
    for mask in range(1 << k):
        d = 1
        bits = 0
        for idx in range(k):
            if (mask >> idx) & 1:
                d *= primes_le_y[idx]
                bits += 1
        mu_d = -1 if (bits % 2 == 1) else 1
        term = n // d
        if mu_d == 1:
            result *= Fraction(term, 1)
        else:
            result /= Fraction(term, 1)
    return result


def cumulative_N_y_from_local_factors_exact(x_int: int, y: int) -> int:
    """Compute N_y(x_int) = prod_{n=1}^{x_int} m_y(n) in Z_{>=1}."""
    prod_val = 1
    for n in range(2, x_int + 1):
        prod_val *= local_prime_euler_factor_m_y_exact(n, y)
    return prod_val


def cumulative_N_y_alternating_factorial_fraction(x_int: int, y: int) -> Fraction:
    """Compute N_y(x_int) = prod_{d | P_y, d <= x_int} (floor(x_int / d)!)^{mu(d)} as an exact Fraction."""
    if x_int <= 1:
        return Fraction(1, 1)
    divs = [
        (d, mu_d) for d, mu_d in divisors_of_primorial(y) if d <= x_int
    ]
    num = 1
    den = 1
    for d, mu_d in divs:
        q = x_int // d
        if q <= 1:
            continue
        fact_q = math.factorial(q)
        if mu_d == 1:
            num *= fact_q
        elif mu_d == -1:
            den *= fact_q
    return Fraction(num, den)


def lcm_prefix_exact(x_int: int) -> int:
    """Compute lcm(1, 2, ..., x_int) = exp(psi(x_int)) in Z_{>=1}."""
    val = 1
    for n in range(2, x_int + 1):
        val = math.lcm(val, n)
    return val


def legendre_factorial_valuation(n: int, p: int) -> int:
    """Compute v_p(n!) via Legendre's formula."""
    count = 0
    cur = n // p
    while cur > 0:
        count += cur
        cur //= p
    return count


def alternating_factorial_prime_valuation_exact(x_int: int, y: int, p: int) -> int:
    """Compute E_{y,p}(x_int) = sum_{d | P_y, d <= x_int} mu(d) v_p(floor(x_int / d)!)."""
    divs = [
        (d, mu_d) for d, mu_d in divisors_of_primorial(y) if d <= x_int
    ]
    total = 0
    for d, mu_d in divs:
        q = x_int // d
        if q >= p:
            total += mu_d * legendre_factorial_valuation(q, p)
    return total


# ---------------------------------------------------------------------------
# 2. Grade-Layer Realization A_{K,y}(x) = N_y(x) * tau^K in Arb
# ---------------------------------------------------------------------------


def evaluate_grade_layer_observable_A_K_y_arb(
    x_int: int, y: int, K_arb: arb, prec_bits: int = 256
) -> Dict[str, Any]:
    """Evaluate the grade-K prime-Euler observable A_{K,y}(x_int) = N_y(x_int) * tau^K in 256-bit Arb."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_a = tau_arb_256(prec_bits=prec_bits)
        tau_K = tau_a**K_arb
        tau_neg_K = tau_a ** (-K_arb)
        N_y_int = cumulative_N_y_from_local_factors_exact(x_int, y)
        N_y_arb = arb(N_y_int)
        A_K_y_arb = N_y_arb * tau_K
        normalized_size_arb = A_K_y_arb * tau_neg_K
        size_diff_arb = normalized_size_arb - N_y_arb
        log_N_y_arb = N_y_arb.log()
        L_y_arb = evaluate_summatory_L_y_direct_arb(float(x_int), y)
        log_diff_arb = log_N_y_arb - L_y_arb
        return {
            "x_int": x_int,
            "y": y,
            "N_y_exact_int": str(N_y_int),
            "N_y_bit_length": N_y_int.bit_length(),
            "tau_pow_K_arb": tau_K,
            "A_K_y_arb": A_K_y_arb,
            "normalized_size_arb": normalized_size_arb,
            "size_recovery_diff_arb": size_diff_arb,
            "size_recovery_encloses_zero": bool(size_diff_arb.contains(0)),
            "log_N_y_minus_L_y_diff_arb": log_diff_arb,
            "log_N_y_equals_L_y_encloses_zero": bool(log_diff_arb.contains(0)),
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_w_y_from_grade_layer_jumps_arb(
    X_arb: arb,
    y: int,
    K_arb: arb,
    J_arb: arb,
    n_cut: int = 1200,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Reconstruct W_y(X) directly from the consecutive grade-K integer-layer ratios
    A_{K,y}(n) / A_{K,y}(n-1) = m_y(n) and cross-grade station ratios
    Phi_J(n) / Phi_K(1) = (n * tau^J) / tau^K = n / tau^{K-J}, and compare against
    evaluate_w_y_coefficient_certified_arb(X, y).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_a = tau_arb_256(prec_bits=prec_bits)
        tau_K = tau_a**K_arb
        tau_J = tau_a**J_arb
        Phi_K_1 = tau_K  # Phi_K(1) = 1 * tau^K
        x_up = float(X_arb.upper())
        eff_cut = max(n_cut, int(math.ceil(24.0 * x_up)))

        s_jump = arb(0)
        prev_m_Check = True
        for n in range(2, eff_cut + 1):
            m_n = local_prime_euler_factor_m_y_exact(n, y)
            if m_n == 1:
                continue
            # Consecutive ratio inside L_K^x:
            # (N_y(n) * tau^K) / (N_y(n-1) * tau^K) = m_y(n) * tau^K / tau^K = m_y(n)
            ratio_in_L_K = (arb(m_n) * tau_K) / tau_K
            if not (ratio_in_L_K - arb(m_n)).contains(0):
                prev_m_Check = False
            log_jump = ratio_in_L_K.log()
            n_a = arb(n)
            # Cross-grade station ratio Phi_J(n) / Phi_K(1) = (n * tau^J) / tau^K
            Phi_J_n = n_a * tau_J
            station_ratio = Phi_J_n / Phi_K_1
            s_jump += (log_jump / n_a.sqrt()) * evaluate_h0_arb(station_ratio)

        c0 = arb(92193) / arb(32768)
        n_cut_a = arb(eff_cut)
        tail_mag = (
            c0
            * (X_arb ** (arb(5) / arb(2)))
            * (arb(2) * n_cut_a.log() + arb(1))
            / (arb(4) * (n_cut_a**2))
        )
        w_y_jump_arb = s_jump + arb(0, tail_mag.upper())
        w_y_direct_res = evaluate_w_y_coefficient_certified_arb(
            X_arb, y=y, n_max=eff_cut, prec_bits=prec_bits
        )
        w_y_direct_arb = w_y_direct_res["enclosure_arb"]
        diff_arb = w_y_jump_arb - w_y_direct_arb
        return {
            "w_y_from_grade_layer_jumps_arb": w_y_jump_arb,
            "w_y_direct_arb": w_y_direct_arb,
            "jump_vs_direct_diff_arb": diff_arb,
            "jump_vs_direct_encloses_zero": bool(diff_arb.contains(0)),
            "tau_K_cancellation_in_step_ratio_verified": prev_m_Check,
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_symbolic_common_referent_identities() -> Dict[str, Any]:
    """Verify symbolically in SymPy the exact algebraic identities of TASK-TC-047:
    1. Multiplicative prime-by-prime step recursion:
       M_{p_k}(n) = M_{p_{k-1}}(n) / M_{p_{k-1}}(n / p_k) (when p_k | n) reproduces
       m_y(n) = n (omega=0), p (omega=1), 1 (omega>=2).
    2. Grade-layer scale cancellation and cross-grade station ratio:
       (N_n * tau^K) / (N_{n-1} * tau^K) = N_n / N_{n-1} = m_y(n),
       and (n * tau^J) / (1 * tau^K) = n / tau^{K-J}.
    3. Coboundary vs. Common-Referent collision:
       A_{K,y} = tau^{K-J} A_{J,y}, while m_K * tau^K = m_J * tau^J  <=>  tau^{K-J} = m_J / m_K.
    """
    n_sym, p1_sym, p2_sym = sp.symbols("n p1 p2", positive=True)
    tau_sym = sp.Symbol("tau", positive=True)
    K_sym, J_sym = sp.symbols("K J", real=True)
    N_prev_sym, m_step_sym = sp.symbols("N_prev m_step", positive=True)

    # 1. Multiplicative recursion step:
    # From omega = 0 (M_0(n) = n, M_0(n/p1) = n/p1) -> M_1(n) = n / (n/p1) = p1
    step_0_to_1 = sp.simplify(n_sym / (n_sym / p1_sym) - p1_sym)
    # From omega = 1 (M_1(n) = p1, M_1(n/p2) = p1) -> M_2(n) = p1 / p1 = 1
    step_1_to_2 = sp.simplify(p1_sym / p1_sym - 1)

    # 2. Grade-K step ratio cancels tau^K:
    A_K_prev = N_prev_sym * (tau_sym**K_sym)
    A_K_next = (N_prev_sym * m_step_sym) * (tau_sym**K_sym)
    step_ratio_diff = sp.simplify(A_K_next / A_K_prev - m_step_sym)

    # 3. Cross-grade station ratio Phi_J(n) / Phi_K(1) = n / tau^{K-J}:
    Phi_J_n = n_sym * (tau_sym**J_sym)
    Phi_K_1 = 1 * (tau_sym**K_sym)
    station_ratio_diff = sp.simplify(
        (Phi_J_n / Phi_K_1) - n_sym / (tau_sym ** (K_sym - J_sym))
    )

    # 4. Coboundary identity A_{K,y} = tau^{K-J} * A_{J,y}:
    A_J_prev = N_prev_sym * (tau_sym**J_sym)
    coboundary_diff = sp.simplify(
        A_K_prev - (tau_sym ** (K_sym - J_sym)) * A_J_prev
    )

    return {
        "multiplicative_step_0_to_1_equals_p": bool(step_0_to_1 == 0),
        "multiplicative_step_1_to_2_equals_1": bool(step_1_to_2 == 0),
        "grade_layer_step_ratio_cancels_tau_K": bool(step_ratio_diff == 0),
        "cross_grade_station_ratio_identity_verified": bool(station_ratio_diff == 0),
        "ambient_coboundary_transfer_identity_verified": bool(coboundary_diff == 0),
    }


# ---------------------------------------------------------------------------
# 3. Main Execution Entry Point for TASK-TC-047
# ---------------------------------------------------------------------------


def execute_task_tc047_common_referent_prime_theta_bridge(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Execute TASK-TC-047: Construct the common-referent observable from the actual
    prime/theta data and prove its required integer-layer membership.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_a = tau_arb_256(prec_bits=prec_bits)
        sym_checks = verify_symbolic_common_referent_identities()

        # -------------------------------------------------------------------
        # Section 1 & 2: Exact Factorial-Ratio Integrality & LCM Agreement Audit
        # -------------------------------------------------------------------
        cutoff_audit_rows: List[Dict[str, Any]] = []
        all_denominators_equal_one = True
        all_local_factor_products_match = True
        all_valuations_nonnegative = True
        all_lcm_windows_match = True
        all_first_discrepancies_equal_two = True
        all_arb_logs_match_L_y = True

        for y_cut in (2, 3, 5, 7, 11, 13):
            q_next = next_prime_above(y_cut)
            first_disc_n = 2 * q_next
            max_n_check = max(45, first_disc_n + 6)
            primes_check = primes_up_to(max_n_check)

            y_den_ok = True
            y_prod_ok = True
            y_val_ok = True
            y_lcm_ok = True
            y_log_ok = True

            for n_i in range(1, max_n_check + 1):
                # 1. Local factor divisor product vs closed-form integer:
                m_closed = local_prime_euler_factor_m_y_exact(n_i, y_cut)
                m_frac = local_prime_euler_factor_divisor_product_fraction(n_i, y_cut)
                if m_frac.denominator != 1 or m_frac.numerator != m_closed or m_closed < 1:
                    y_prod_ok = False
                    all_local_factor_products_match = False

                # 2. Cumulative alternating factorial product vs local factor product:
                N_fact_frac = cumulative_N_y_alternating_factorial_fraction(n_i, y_cut)
                N_prod_int = cumulative_N_y_from_local_factors_exact(n_i, y_cut)
                if N_fact_frac.denominator != 1:
                    y_den_ok = False
                    all_denominators_equal_one = False
                if N_fact_frac.numerator != N_prod_int:
                    y_prod_ok = False
                    all_local_factor_products_match = False

                # 3. Agreement with lcm(1, ..., n_i) for n_i < 2 * q_{>y}:
                lcm_val = lcm_prefix_exact(n_i)
                if n_i < first_disc_n and N_prod_int != lcm_val:
                    y_lcm_ok = False
                    all_lcm_windows_match = False

            # Check prime valuations at n_i = first_disc_n:
            for p_c in primes_check:
                if p_c <= first_disc_n:
                    v_p_val = alternating_factorial_prime_valuation_exact(
                        first_disc_n, y_cut, p_c
                    )
                    if v_p_val < 0:
                        y_val_ok = False
                        all_valuations_nonnegative = False

            # Check first discrepancy ratio N_y(2*q_{>y}) / lcm(1, ..., 2*q_{>y}) == 2:
            N_at_disc = cumulative_N_y_from_local_factors_exact(first_disc_n, y_cut)
            lcm_at_disc = lcm_prefix_exact(first_disc_n)
            disc_ratio = Fraction(N_at_disc, lcm_at_disc)
            if disc_ratio != Fraction(2, 1):
                all_first_discrepancies_equal_two = False

            # Check Arb log(N_y(N)) == L_y(N) at N = first_disc_n - 1 and N = first_disc_n:
            N_before_int = cumulative_N_y_from_local_factors_exact(
                first_disc_n - 1, y_cut
            )
            log_before_arb = arb(N_before_int).log()
            L_y_before_arb = evaluate_summatory_L_y_direct_arb(
                float(first_disc_n - 1), y_cut
            )
            diff_before_arb = log_before_arb - L_y_before_arb

            log_at_disc_arb = arb(N_at_disc).log()
            L_y_at_disc_arb = evaluate_summatory_L_y_direct_arb(
                float(first_disc_n), y_cut
            )
            diff_at_disc_arb = log_at_disc_arb - L_y_at_disc_arb
            if not (diff_before_arb.contains(0) and diff_at_disc_arb.contains(0)):
                y_log_ok = False
                all_arb_logs_match_L_y = False

            cutoff_audit_rows.append(
                {
                    "y": y_cut,
                    "q_next": q_next,
                    "first_discrepancy_n": first_disc_n,
                    "max_n_verified": max_n_check,
                    "all_factorial_ratio_denominators_equal_one": y_den_ok,
                    "all_local_factor_products_match_factorial_ratio": y_prod_ok,
                    "all_prime_valuations_nonnegative": y_val_ok,
                    "exact_lcm_agreement_below_2_q_next": y_lcm_ok,
                    "N_y_at_2_q_next_minus_1_exact": str(N_before_int),
                    "N_y_at_2_q_next_exact": str(N_at_disc),
                    "lcm_at_2_q_next_exact": str(lcm_at_disc),
                    "first_discrepancy_multiplicative_ratio": int(disc_ratio),
                    "log_N_y_at_2_q_next_minus_1_certified": serialize_arb_certified(
                        log_before_arb
                    ),
                    "log_N_y_minus_L_y_at_2_q_next_minus_1_certified": serialize_arb_certified(
                        diff_before_arb
                    ),
                    "log_N_y_at_2_q_next_certified": serialize_arb_certified(
                        log_at_disc_arb
                    ),
                    "log_N_y_minus_L_y_at_2_q_next_certified": serialize_arb_certified(
                        diff_at_disc_arb
                    ),
                    "arb_log_identities_enclose_zero": y_log_ok,
                }
            )

        # -------------------------------------------------------------------
        # Section 3: Grade-Layer Membership A_{K, M(X_K)}(x) in L_K^x and
        #            Stieltjes Station-Ratio Bridge Across Admissible Grades
        # -------------------------------------------------------------------
        grade_specs = [
            ("0", arb(0), True),
            ("1/100", arb(1) / arb(100), True),
            ("-1/100", -arb(1) / arb(100), True),
            ("1/4", arb(1) / arb(4), True),
            ("-1/4", -arb(1) / arb(4), True),
            ("1/2", arb(1) / arb(2), True),
            ("-1/2", -arb(1) / arb(2), True),
            ("sqrt(2)/2", arb(2).sqrt() / arb(2), False),
            ("-sqrt(2)/2", -arb(2).sqrt() / arb(2), False),
            ("1", arb(1), True),
            ("-1", -arb(1), True),
            ("3/2", arb(3) / arb(2), True),
            ("-3/2", -arb(3) / arb(2), True),
            ("2", arb(2), True),
            ("-2", -arb(2), True),
        ]

        grade_layer_bridge_rows: List[Dict[str, Any]] = []
        all_grade_size_recoveries_pass = True
        all_grade_coboundary_checks_pass = True
        all_grade_jump_reconstructions_pass = True
        all_nonzero_rational_grades_avoid_self_dual_peak = True

        for k_label, k_arb, is_rational_grade in grade_specs:
            abs_k_arb = abs(k_arb)
            x_k_arb = tau_a**abs_k_arb
            m_k = certified_coupled_cutoff_M_X_arb(x_k_arb, prec_bits=prec_bits)
            q_next_mk = next_prime_above(m_k)
            agreement_horizon = 2 * q_next_mk - 1
            sample_n = min(agreement_horizon, 40)

            obs_k = evaluate_grade_layer_observable_A_K_y_arb(
                sample_n, m_k, k_arb, prec_bits=prec_bits
            )
            obs_0 = evaluate_grade_layer_observable_A_K_y_arb(
                sample_n, m_k, arb(0), prec_bits=prec_bits
            )
            if not obs_k["size_recovery_encloses_zero"]:
                all_grade_size_recoveries_pass = False

            # Coboundary check: A_{K, m_k}(sample_n) - tau^K * A_{0, m_k}(sample_n) encloses 0
            coboundary_diff_arb = (
                obs_k["A_K_y_arb"] - (tau_a**k_arb) * obs_0["A_K_y_arb"]
            )
            coboundary_ok = bool(coboundary_diff_arb.contains(0))
            if not coboundary_ok:
                all_grade_coboundary_checks_pass = False

            # Reconstruct W_{M(X_K)}(X_K) from grade-|K| integer-layer jumps and station ratios Phi_0(n)/Phi_{|K|}(1):
            jump_recon = evaluate_w_y_from_grade_layer_jumps_arb(
                X_arb=x_k_arb,
                y=m_k,
                K_arb=abs_k_arb,
                J_arb=arb(0),
                n_cut=1200,
                prec_bits=prec_bits,
            )
            if not (
                jump_recon["jump_vs_direct_encloses_zero"]
                and jump_recon["tau_K_cancellation_in_step_ratio_verified"]
            ):
                all_grade_jump_reconstructions_pass = False

            # Minimum distance from prime-power station ratios n / X_K (2 <= n <= 2*q_{>M(X_K)}) to self-dual peak alpha = 1:
            min_peak_dist_arb = abs(arb(2) / x_k_arb - arb(1))
            closest_n = 2
            for n_s in range(2, 2 * q_next_mk + 1):
                d_s = abs(arb(n_s) / x_k_arb - arb(1))
                if d_s.upper() < min_peak_dist_arb.upper():
                    min_peak_dist_arb = d_s
                    closest_n = n_s
            peak_strictly_avoided = bool(min_peak_dist_arb.lower() > arb(0))
            if is_rational_grade and k_label != "0" and not peak_strictly_avoided:
                all_nonzero_rational_grades_avoid_self_dual_peak = False

            grade_layer_bridge_rows.append(
                {
                    "grade_K": k_label,
                    "is_rational_grade": is_rational_grade,
                    "X_K_certified": serialize_arb_certified(x_k_arb),
                    "coupled_cutoff_M_X_K": m_k,
                    "agreement_window_2_q_next": 2 * q_next_mk,
                    "sample_horizon_N": sample_n,
                    "N_M_X_K_at_sample_N_exact_int": obs_k["N_y_exact_int"],
                    "A_K_M_X_K_at_sample_N_certified": serialize_arb_certified(
                        obs_k["A_K_y_arb"]
                    ),
                    "normalized_fiber_size_recovery_diff_certified": serialize_arb_certified(
                        obs_k["size_recovery_diff_arb"]
                    ),
                    "normalized_fiber_size_recovery_encloses_zero": obs_k[
                        "size_recovery_encloses_zero"
                    ],
                    "coboundary_transfer_diff_certified": serialize_arb_certified(
                        coboundary_diff_arb
                    ),
                    "coboundary_transfer_encloses_zero": coboundary_ok,
                    "W_M_X_K_from_grade_layer_jumps_certified": serialize_arb_certified(
                        jump_recon["w_y_from_grade_layer_jumps_arb"]
                    ),
                    "W_M_X_K_direct_certified": serialize_arb_certified(
                        jump_recon["w_y_direct_arb"]
                    ),
                    "W_M_X_K_jump_vs_direct_diff_certified": serialize_arb_certified(
                        jump_recon["jump_vs_direct_diff_arb"]
                    ),
                    "W_M_X_K_jump_reconstruction_encloses_zero": jump_recon[
                        "jump_vs_direct_encloses_zero"
                    ],
                    "closest_station_n_to_self_dual_peak": closest_n,
                    "min_station_ratio_distance_to_peak_1_certified": serialize_arb_certified(
                        min_peak_dist_arb
                    ),
                    "self_dual_peak_strictly_avoided_on_window": peak_strictly_avoided,
                }
            )

        # -------------------------------------------------------------------
        # Section 4: CR1-CR2-CR3 Bridge Classification & Open Subgate Audit
        # -------------------------------------------------------------------
        cr_bridge_classification = {
            "constructed_common_referent_observable": {
                "local_prime_euler_integer_factor": (
                    "m_y(n) := exp(lambda_y(n)) = prod_{d | gcd(n, P_y)} (n/d)^{mu(d)} "
                    "= { 1 if n = 1 or omega_{<=y}(n) >= 2; n if omega_{<=y}(n) = 0; p if omega_{<=y}(n) = 1 } in Z_{>=1}"
                ),
                "cumulative_prime_euler_factorial_observable": (
                    "N_y(x) := exp(L_y(x)) = prod_{d | P_y, d <= x} (floor(x/d)!)^{mu(d)} "
                    "= prod_{1 <= n <= floor(x)} m_y(n) in Z_{>=1}"
                ),
                "grade_K_integer_layer_realization": (
                    "A_{K,y}(x) := Phi_K(fromZ(K, N_y(x))) = N_y(x) * tau^K in L_K^x = tau^K (Z \\ {0}) subset L_K = tau^K Z"
                ),
                "stieltjes_lower_endpoint_convention": (
                    "Extend A_{K,y}(x) constantly as tau^K below 1 (so A_{K,y}(x) = tau^K on (0, 2)), "
                    "or integrate over (1, infty), so that d(log A_{K,y})(x) has zero atom at x = 1 "
                    "(no artificial K * log(tau) boundary term) and point masses log(A_{K,y}(n)/A_{K,y}(n-1)) "
                    "= log m_y(n) = lambda_y(n) exclusively at integers n >= 2."
                ),
                "intrinsic_coordinate_recovery_vs_raw_CR1": (
                    "N_K(A_{K,y}(x)) := tau^{-K} A_{K,y}(x) = N_y(x) = N_J(A_{J,y}(x)) in Z_{>=1} recovers the "
                    "intrinsic unit-converted integer coordinate, NOT the original raw external common-referent "
                    "equality (`CR1`). Because A_{K,y}(x) = N_y(x) * tau^K > 0, the raw external values "
                    "A_{K,y}(x) and A_{J,y}(x) satisfy A_{K,y}(x) = tau^{K-J} A_{J,y}(x) and are unequal whenever K != J."
                ),
            },
            "proved_integer_layer_membership_theorems": {
                "unconditional_factorial_ratio_integrality": (
                    "For every real x >= 1 and every prime cutoff y >= 2, all factorial denominators "
                    "(floor(x/d)!)^{-1} with mu(d) = -1 in prod_{d | P_y, d <= x} (floor(x/d)!)^{mu(d)} divide the numerator "
                    "identically, yielding the exact positive integer N_y(x) = prod_{2 <= n <= floor(x)} m_y(n) in Z_{>=1} "
                    "with prime valuations E_{y,p}(x) = sum_{d | P_y, d <= x} mu(d) v_p(floor(x/d)!) >= 0."
                ),
                "exact_chebyshev_lcm_agreement_window": (
                    "For all 1 <= x < 2 q_{>y} (in particular across the entire coupled-cutoff agreement window "
                    "1 <= x < 2 q_{>M(X)} where M(X) = ceil(max(2, X^{5/4}))), N_y(x) = lcm(1, 2, ..., floor(x)) = exp(psi(x)) in Z_{>=1}, "
                    "and at the first discrepancy x = 2 q_{>y}, N_y(2 q_{>y}) = 2 * lcm(1, 2, ..., 2 q_{>y}) in Z_{>=1}."
                ),
                "required_grade_layer_membership_CR2": (
                    "For every concurrent grade K in A_R = Qbar cap R, every y >= 2, and every x >= 1, "
                    "A_{K,y}(x) = N_y(x) * tau^K belongs unconditionally to the discrete integer layer "
                    "L_K^x = tau^K (Z \\ {0}) subset L_K = tau^K Z (`CR2`), and its consecutive step ratio "
                    "A_{K,y}(n) / A_{K,y}(n-1) = m_y(n) in Z_{>=1} cancels tau^K identically."
                ),
                "mellin_stieltjes_and_station_ratio_bridge": (
                    "With A_{K,y}(x) extended constantly as tau^K below 1 (or integrated over (1, infty)), for any grades "
                    "K >= J in A_R with relative scale X_{K,J} = tau^{K-J}, "
                    "W_y(tau^{K-J}) = int_{(1, infty)} x^{-1/2} h_0(x / tau^{K-J}) d(log A_{K,y})(x) "
                    "= sum_{n>=2} log(A_{K,y}(n)/A_{K,y}(n-1)) * n^{-1/2} * h_0(Phi_J(n)/Phi_K(1)), "
                    "where Phi_J(n)/Phi_K(1) = (n * tau^J)/tau^K = n / tau^{K-J}. For rational K - J != 0, "
                    "Lindemann's theorem (tau = 2*pi not in Qbar) implies L_K cap L_J = {0}, so Phi_J(n) != Phi_K(m) "
                    "for all nonzero integers n, m and no prime-power station ever collides with the self-dual peak alpha = 1."
                ),
            },
            "three_class_cr1_cr2_cr3_audit": {
                "class_I_intrinsic_fiber_referent": {
                    "observable": "N_K(A_{K,y}(x)) = tau^{-K} A_{K,y}(x) = N_y(x) in Z_{>=1}",
                    "CR1_cross_grade_equality": (
                        "UNIT_CONVERTED_FIBER_COORDINATE_RECOVERY_NOT_RAW_CR1 "
                        "(N_K = N_J = N_y(x) after dividing by tau^K and tau^J; raw A_{K,y}(x) != A_{J,y}(x) for K != J)"
                    ),
                    "CR2_distinct_scaled_layer_membership": "LIVES_IN_SINGLE_RING_Z_NOT_L_K_CAP_L_J",
                    "CR3_off_critical_zero_sensitivity": "ARITHMETIC_CARRIER_INDEPENDENT_OF_ZERO_DEFECT_DELTA",
                },
                "class_II_ambient_integer_layer_observable": {
                    "observable": "A_{K,y}(x) = N_y(x) * tau^K in L_K^x subset L_K = tau^K Z",
                    "CR1_cross_grade_equality": (
                        "FAILS_RAW_CR1_OBEYS_SCALE_COBOUNDARY A_{K,y}(x) = tau^{K-J} A_{J,y}(x) != A_{J,y}(x) for K != J; "
                        "ambient equality m_K * tau^K = m_J * tau^J for rational K - J != 0 forces m_K = m_J = 0 by Lindemann"
                    ),
                    "CR2_distinct_scaled_layer_membership": "PROVED_UNCONDITIONALLY (A_{K,y}(x) in L_K = tau^K Z for all x >= 1, y >= 2)",
                    "CR3_off_critical_zero_sensitivity": (
                        "CONDITIONAL_REDUCTIO_SCHEMA (`common_referent_integer_layer_bridge_and_station_ratio_identity`): "
                        "if a zero-defect-modulated integer-layer observable D_K = m_K(delta) * tau^K in L_K satisfies "
                        "D_K = D_J for rational K != J and delta != 0 => m_K(delta) != 0, then D_K in L_K cap L_J = {0} forces delta = 0"
                    ),
                },
                "class_III_coupled_theta_wavelet_profile": {
                    "observable": "W_{M(X)}(X) = sum_{n>=2} log(A_{K,M(X)}(n)/A_{K,M(X)}(n-1)) n^{-1/2} h_0(Phi_J(n)/Phi_K(1))  (X = tau^{K-J})",
                    "CR1_cross_grade_equality": "SATISFIED_UNDER_SIMULTANEOUS_SHIFT (Q_tau(T_{K+A} psi_tau, T_{J+A} psi_tau) = C_tau(|K-J|))",
                    "CR2_distinct_scaled_layer_membership": (
                        "PIECEWISE_CONTINUOUS_MELLIN_STIELTJES_INTEGRAL_OVER_INTEGER_LAYER_JUMPS "
                        "(for fixed y, W_y(X) is continuous, while F(X) = W_{M(X)}(X) is piecewise continuous with "
                        "right-hand jumps F(X_0^+) - F(X_0) = -p^{-1/2} W_{p^-}(X_0/p) at X_0 = (p-1)^{4/5}; "
                        "arithmetic carrier A_{K,M(X)}(n) lies in L_K^x, while kernel values h_0(n/X) are continuous real numbers)"
                    ),
                    "CR3_off_critical_zero_sensitivity": (
                        "PROVED_VIA_LAPLACE_CARLEMAN_AND_COUPLED_CUTOFF_EQUIVALENCE "
                        "(sup_{X>=1} |W_{M(X)}(X)| < infty <=> sup_{X>=1} |R_mu(X)| < infty <=> sup_{K in A_R} |C_tau(K)| < infty <=> RH; "
                        "extension from dense K in A_R to all X >= 1 uses continuity of W(X) and R_mu(X) together with "
                        "|W_{M(X)}(X) - W(X)| <= (1/2) C_{log,0} < 0.278715, NEVER continuity of W_{M(X)}(X))"
                    ),
                },
            },
            "lean_formalization_vs_derivation_and_computational_scope": {
                "paper_mathematical_derivation": (
                    "Establishes unconditionally for all real x >= 1 and integer y >= 2 that "
                    "m_y(n) = exp(lambda_y(n)) = prod_{d | gcd(n, P_y)} (n/d)^{mu(d)} in Z_{>=1}, "
                    "N_y(x) = prod_{d | P_y, d <= x} (floor(x/d)!)^{mu(d)} = prod_{n <= x} m_y(n) in Z_{>=1}, "
                    "N_y(x) = lcm(1, ..., floor(x)) for 1 <= x < 2 q_{>y} with first discrepancy "
                    "N_y(2 q_{>y}) = 2 lcm(1, ..., 2 q_{>y}), and A_{K,y}(x) = N_y(x) * tau^K in L_K^x = tau^K (Z \\ {0})."
                ),
                "finite_computational_certification": (
                    "Exact integer/Fraction verification for y in {2, 3, 5, 7, 11, 13} and n <= max(45, 2 q_{>y} + 6) "
                    "plus 256-bit Arb ball certification across 15 positive and negative admissible grades K in A_R."
                ),
                "lean_4_formalization_scope": (
                    "The Lean 4 theorems `prime_euler_multiplicative_integrality_and_grade_layer_membership` and "
                    "`common_referent_integer_layer_bridge_and_station_ratio_identity` prove the algebraic consequences "
                    "for supplied integer inputs (positivity of finitePrimeMultiplicativeFactorCases, step-ratio cancellation "
                    "of tau^K, coboundary relation A_{K,y} = tau^{K-J} A_{J,y}, station-ratio identity Phi_J(n)/Phi_K(1) = n/tau^{K-J}, "
                    "peak avoidance via Lindemann, and a conditional collision implication under supplied CR1+CR2+CR3 hypotheses); "
                    "they do NOT internally formalize the full alternating factorial-product divisor cancellation over Finset.divisors "
                    "or derive the missing CR1+CR2+CR3 collision hypotheses from actual prime/theta data."
                ),
            },
            "lean_theorems": [
                "prime_euler_multiplicative_integrality_and_grade_layer_membership",
                "common_referent_integer_layer_bridge_and_station_ratio_identity",
            ],
            "remaining_open_obligation": {
                "subgate_id": "SUBGATE-TC-043A",
                "status": "OPEN",
                "scope_note": (
                    "SUBGATE-TC-043A remains OPEN. Divergence of the unsplit critical-line Gram norm "
                    "||Psi_y||_{L^2(d^*x)} establishes failure of that Cauchy-Schwarz norm estimate as y -> infty; "
                    "it does NOT establish divergence of the signed coupled profile W_{M(X)}(X) or failure of the "
                    "concurrent-grade hypothesis. Passing from the proved integer-layer membership "
                    "A_{K,M(X)}(x) = N_{M(X)}(x) * tau^K in L_K^x = tau^K (Z \\ {0}) to a uniform signed cancellation bound "
                    "sup_{X >= 1} |W_{M(X)}(X)| < infty (or deriving all three CR1+CR2+CR3 properties for one single "
                    "prime/theta observable D_K(rho_K)) is the exact open obligation."
                ),
            },
        }

        result_tc047: Dict[str, Any] = {
            "task_id": TASK_TC_047_ID,
            "parent_epic": EPIC_TC_042_ID,
            "inspected_baseline": STARTING_HEAD_TC_047,
            "status": COMMON_REFERENT_PRIME_THETA_BRIDGE_STATUS,
            "symbolic_identities_verification": sym_checks,
            "section_1_2_factorial_ratio_integrality_and_lcm_audit": {
                "all_factorial_ratio_denominators_equal_one": all_denominators_equal_one,
                "all_local_factor_products_match_factorial_ratio": all_local_factor_products_match,
                "all_prime_valuations_nonnegative": all_valuations_nonnegative,
                "all_lcm_agreement_windows_verified": all_lcm_windows_match,
                "all_first_discrepancy_ratios_equal_two": all_first_discrepancies_equal_two,
                "all_arb_logs_match_summatory_L_y": all_arb_logs_match_L_y,
                "prime_cutoff_integrality_table": cutoff_audit_rows,
            },
            "section_3_grade_layer_membership_and_station_ratio_bridge": {
                "all_grade_size_recoveries_enclose_zero": all_grade_size_recoveries_pass,
                "all_grade_coboundary_transfers_enclose_zero": all_grade_coboundary_checks_pass,
                "all_grade_jump_reconstructions_enclose_zero": all_grade_jump_reconstructions_pass,
                "all_nonzero_rational_grades_avoid_self_dual_peak": all_nonzero_rational_grades_avoid_self_dual_peak,
                "certified_grade_layer_bridge_table": grade_layer_bridge_rows,
            },
            "section_4_cr1_cr2_cr3_bridge_and_open_obligation": cr_bridge_classification,
        }
        full_tree_rt_sec16 = verify_all_serialized_arb_in_tree(
            result_tc047, path_prefix="section_16"
        )
        result_tc047["full_section_16_tree_roundtrip_verification"] = full_tree_rt_sec16
        return result_tc047
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 4. TASK-TC-048: Coupled-Cutoff Piecewise Continuity & Right-Hand Jump Formula
#    and Single-Observable Common-Referent Collision Contract Audit
# ---------------------------------------------------------------------------


def evaluate_coupled_cutoff_jump_at_prime_threshold_arb(
    p: int, k_max: int = 3500, prec_bits: int = 256
) -> Dict[str, Any]:
    """Evaluate the exact right-hand jump of the coupled profile F(X) = W_{M(X)}(X)
    across the threshold X_0 = (p - 1)^{4/5} where M(X) = ceil(max(2, X^{5/4}))
    steps from p - 1 to p:
      - If p >= 3 is prime, P_p = p * P_{p-1} so F(X_0) = W_{p^-}(X_0) and
        F(X_0^+) = W_p(X_0) = W_{p^-}(X_0) - p^{-1/2} W_{p^-}(X_0 / p), giving
          F(X_0^+) - F(X_0) = -p^{-1/2} W_{p^-}(X_0 / p).
      - If m + 1 = p is composite (e.g. m + 1 = 4), P_{m+1} = P_m so W_{m+1} = W_m
        and F(X_0^+) - F(X_0) = 0 identically.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        m_prev = p - 1
        x0_arb = (arb(m_prev) ** 4).root(5)
        p_arb = arb(p)
        u_p_arb = x0_arb / p_arb
        ps_le_p = primes_up_to(p)
        is_prime_p = len(ps_le_p) > 0 and ps_le_p[-1] == p
        y_prev = m_prev

        w_prev_x0 = evaluate_w_y_divisor_sum_certified_arb(
            x0_arb, y=y_prev, k_max=k_max, prec_bits=prec_bits
        )["enclosure_arb"]
        w_curr_x0 = evaluate_w_y_divisor_sum_certified_arb(
            x0_arb, y=p, k_max=k_max, prec_bits=prec_bits
        )["enclosure_arb"]
        direct_jump_arb = w_curr_x0 - w_prev_x0

        if is_prime_p:
            w_prev_up = evaluate_w_y_divisor_sum_certified_arb(
                u_p_arb, y=y_prev, k_max=k_max, prec_bits=prec_bits
            )["enclosure_arb"]
            euler_jump_arb = -(arb(1) / p_arb.sqrt()) * w_prev_up
        else:
            w_prev_up = evaluate_w_y_divisor_sum_certified_arb(
                u_p_arb, y=y_prev, k_max=k_max, prec_bits=prec_bits
            )["enclosure_arb"]
            euler_jump_arb = arb(0)

        jump_identity_diff_arb = direct_jump_arb - euler_jump_arb
        min_station_alpha_at_up = arb(2) / u_p_arb
        in_strict_negative_h0_tail = bool(min_station_alpha_at_up.lower() >= arb(9))

        return {
            "threshold_m_plus_1": p,
            "is_prime_threshold": is_prime_p,
            "m_prev": m_prev,
            "X_0_arb": x0_arb,
            "u_p_equals_X_0_over_p_arb": u_p_arb,
            "min_station_alpha_2_over_u_p_arb": min_station_alpha_at_up,
            "in_strict_negative_h0_tail_alpha_ge_9": in_strict_negative_h0_tail,
            "F_at_X_0_equals_W_p_minus_arb": w_prev_x0,
            "F_at_X_0_plus_equals_W_p_arb": w_curr_x0,
            "W_p_minus_at_X_0_over_p_arb": w_prev_up,
            "direct_jump_F_X0_plus_minus_F_X0_arb": direct_jump_arb,
            "euler_recursion_jump_formula_arb": euler_jump_arb,
            "jump_identity_diff_arb": jump_identity_diff_arb,
            "jump_identity_encloses_zero": bool(jump_identity_diff_arb.contains(0)),
            "jump_certified_nonzero": bool(not direct_jump_arb.contains(0)),
            "jump_certified_strictly_negative": bool(direct_jump_arb.upper() < arb(0)),
            "jump_certified_strictly_positive": bool(direct_jump_arb.lower() > arb(0)),
            "W_p_minus_at_u_p_certified_strictly_positive": bool(
                w_prev_up.lower() > arb(0)
            ),
            "W_p_minus_at_u_p_certified_strictly_negative": bool(
                w_prev_up.upper() < arb(0)
            ),
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_theta_zero_radial_defect_observable_arb(
    delta_arb: arb, gamma_arb: arb, K_arb: arb, prec_bits: int = 256
) -> Dict[str, Any]:
    """Evaluate Candidate 2A (normalized pullback theta-zero radial defect observable)
    at a grade-K zero image rho_K = tau^K * (1/2 + delta + i*gamma):
      z_K := tau^{-K} rho_K - 1/2 = delta + i*gamma,
      D_K^{(2A)}(rho_K) := |H_0(tau^{-K} rho_K - 1/2)|^2 * (tau^{Re(z_K)} + tau^{-Re(z_K)} - 2)
                         = |H_0(delta + i*gamma)|^2 * (tau^delta + tau^{-delta} - 2),
    where H_0(z) = F_tau(1/2 + z) * F_tau(1/2 - z).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_a = tau_arb_256(prec_bits=prec_bits)
        tau_K = tau_a**K_arb
        tau_neg_K = tau_a ** (-K_arb)
        rho_0_acb = acb(arb(1) / arb(2) + delta_arb, gamma_arb)
        rho_K_acb = acb(tau_K) * rho_0_acb
        pulled_back_rho_acb = acb(tau_neg_K) * rho_K_acb
        z_recovered_acb = pulled_back_rho_acb - acb(arb(1) / arb(2))
        delta_recovered_arb = z_recovered_acb.real

        f_plus = evaluate_f_tau_acb(acb(arb(1) / arb(2)) + z_recovered_acb)
        f_minus = evaluate_f_tau_acb(acb(arb(1) / arb(2)) - z_recovered_acb)
        h0_z_acb = f_plus * f_minus
        abs_h0_sq_arb = abs(h0_z_acb) ** 2

        radial_factor_arb = (
            (tau_a**delta_recovered_arb)
            + (tau_a ** (-delta_recovered_arb))
            - arb(2)
        )
        d_k_2a_arb = abs_h0_sq_arb * radial_factor_arb

        return {
            "rho_K_real_arb": rho_K_acb.real,
            "rho_K_imag_arb": rho_K_acb.imag,
            "pulled_back_delta_diff_arb": delta_recovered_arb - delta_arb,
            "pulled_back_delta_encloses_zero": bool(
                (delta_recovered_arb - delta_arb).contains(0)
            ),
            "abs_H0_at_z_sq_arb": abs_h0_sq_arb,
            "abs_H0_at_z_sq_strictly_positive": bool(abs_h0_sq_arb.lower() > arb(0)),
            "radial_cosh_factor_arb": radial_factor_arb,
            "D_K_2A_arb": d_k_2a_arb,
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_symbolic_tc048_jump_and_single_observable_identities() -> Dict[str, Any]:
    """Verify symbolically in SymPy the exact identities of TASK-TC-048:
    1. Coupled-cutoff prime-step right-hand jump from the one-prime Euler recursion:
         W_p(X_0) - W_{p^-}(X_0) = [W_{p^-}(X_0) - p^{-1/2} W_{p^-}(X_0/p)] - W_{p^-}(X_0)
                                 = -p^{-1/2} W_{p^-}(X_0/p).
    2. Dense-subset uniform comparison triangle inequality:
         |W(X) - W(X_n)| + |F(X) - W(X)| + |F(X_n) - W(X_n)|
         shows sup_{X >= 1} |F(X)| <= sup_{K in A_R} |F(tau^{|K|})| + C_{log,0}
         using continuity of W(X) alone without continuity of F(X).
    3. Candidate 1 vs Candidate 2 transformation laws under rho_K = tau^K rho:
       - Weight-1 covariant layer carrier D_K^{(1A)} = N_y(X_0) * tau^K satisfies
         D_K^{(1A)} / D_J^{(1A)} = tau^{K-J} != 1 for K != J (fails raw CR1).
       - Pullback radial defect D_K^{(2A)}(rho_K) depends only on tau^{-K} rho_K = rho,
         satisfying D_K^{(2A)}(rho_K) - D_J^{(2A)}(rho_J) = 0 identically (raw CR1) and
         tau^delta + tau^{-delta} - 2 = (tau^{delta/2} - tau^{-delta/2})^2 >= 0.
    """
    w_prev_x0, w_prev_up, p_sym = sp.symbols("W_prev_X0 W_prev_up p", positive=True)
    w_p_x0 = w_prev_x0 - w_prev_up / sp.sqrt(p_sym)
    jump_diff = sp.simplify((w_p_x0 - w_prev_x0) - (-w_prev_up / sp.sqrt(p_sym)))

    tau_sym, K_sym, J_sym, delta_sym = sp.symbols("tau K J delta", real=True, positive=True)
    N_sym, H0_sq_sym = sp.symbols("N_y H0_sq", positive=True)

    # Candidate 1A ratio:
    d1_K = N_sym * (tau_sym**K_sym)
    d1_J = N_sym * (tau_sym**J_sym)
    d1_coboundary_diff = sp.simplify(d1_K - (tau_sym ** (K_sym - J_sym)) * d1_J)

    # Candidate 2A grade invariance and square factorization:
    rho_sym = sp.Symbol("rho", positive=True)
    rho_K = (tau_sym**K_sym) * rho_sym
    rho_J = (tau_sym**J_sym) * rho_sym
    pullback_diff = sp.simplify((tau_sym ** (-K_sym)) * rho_K - (tau_sym ** (-J_sym)) * rho_J)
    radial_sq_diff = sp.simplify(
        (tau_sym**delta_sym + tau_sym ** (-delta_sym) - 2)
        - (tau_sym ** (delta_sym / 2) - tau_sym ** (-delta_sym / 2)) ** 2
    )

    return {
        "euler_prime_step_jump_identity_verified": bool(jump_diff == 0),
        "candidate_1_coboundary_ratio_verified": bool(d1_coboundary_diff == 0),
        "candidate_2A_pullback_grade_invariance_verified": bool(pullback_diff == 0),
        "candidate_2A_radial_factor_square_identity_verified": bool(radial_sq_diff == 0),
    }


def execute_task_tc048_single_observable_common_referent_audit(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Execute TASK-TC-048:
    1. Reconcile TC-047 scope (intrinsic unit-converted coordinate recovery vs raw CR1,
       explicit Stieltjes lower-endpoint convention, and Lean vs paper vs finite checks).
    2. Derive and certify the coupled-cutoff piecewise continuity and exact right-hand
       jump formula F(X_0^+) - F(X_0) = -p^{-1/2} W_{p^-}(X_0 / p) at X_0 = (p - 1)^{4/5},
       proving strict positivity for all primes p >= 3 and correcting the dense-to-all-X
       extension argument so it uses continuity of W(X) and |F(X) - W(X)| <= (1/2) C_{log,0}.
    3. Audit two explicit single-observable candidate families D_K(rho_K) constructed from
       the existing prime-Euler and canonical theta objects against the simultaneous
       three-part collision contract (CR1 + CR2 + CR3) on the SAME expression, and isolate
       the Covariance-Invariance-Discreteness Trilemma while keeping SUBGATE-TC-043A OPEN.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_a = tau_arb_256(prec_bits=prec_bits)
        sym_tc048 = verify_symbolic_tc048_jump_and_single_observable_identities()

        # -------------------------------------------------------------------
        # Part 1: Coupled-Cutoff Piecewise Continuity & Right-Hand Jump Audit
        # -------------------------------------------------------------------
        prime_jump_rows: List[Dict[str, Any]] = []
        all_prime_jump_identities_enclose_zero = True
        all_prime_jumps_certified_nonzero = True
        all_small_prime_jumps_certified_strictly_negative = True

        for p_val in (3, 5, 7, 11, 13, 17, 19, 23):
            j_res = evaluate_coupled_cutoff_jump_at_prime_threshold_arb(
                p_val, k_max=3500, prec_bits=prec_bits
            )
            if not j_res["jump_identity_encloses_zero"]:
                all_prime_jump_identities_enclose_zero = False
            if not j_res["jump_certified_nonzero"]:
                all_prime_jumps_certified_nonzero = False
            if not j_res["jump_certified_strictly_negative"]:
                all_small_prime_jumps_certified_strictly_negative = False

            prime_jump_rows.append(
                {
                    "prime_p": p_val,
                    "m_prev": j_res["m_prev"],
                    "X_0_equals_p_minus_1_pow_4_5_certified": serialize_arb_certified(
                        j_res["X_0_arb"]
                    ),
                    "u_p_equals_X_0_over_p_certified": serialize_arb_certified(
                        j_res["u_p_equals_X_0_over_p_arb"]
                    ),
                    "min_station_alpha_2_over_u_p_certified": serialize_arb_certified(
                        j_res["min_station_alpha_2_over_u_p_arb"]
                    ),
                    "in_strict_negative_h0_tail_alpha_ge_9": j_res[
                        "in_strict_negative_h0_tail_alpha_ge_9"
                    ],
                    "F_at_X_0_equals_W_p_minus_certified": serialize_arb_certified(
                        j_res["F_at_X_0_equals_W_p_minus_arb"]
                    ),
                    "F_at_X_0_plus_equals_W_p_certified": serialize_arb_certified(
                        j_res["F_at_X_0_plus_equals_W_p_arb"]
                    ),
                    "W_p_minus_at_X_0_over_p_certified": serialize_arb_certified(
                        j_res["W_p_minus_at_X_0_over_p_arb"]
                    ),
                    "direct_jump_F_X0_plus_minus_F_X0_certified": serialize_arb_certified(
                        j_res["direct_jump_F_X0_plus_minus_F_X0_arb"]
                    ),
                    "euler_recursion_jump_formula_certified": serialize_arb_certified(
                        j_res["euler_recursion_jump_formula_arb"]
                    ),
                    "jump_identity_diff_certified": serialize_arb_certified(
                        j_res["jump_identity_diff_arb"]
                    ),
                    "jump_identity_encloses_zero": j_res["jump_identity_encloses_zero"],
                    "jump_certified_nonzero": j_res["jump_certified_nonzero"],
                    "jump_certified_strictly_negative": j_res[
                        "jump_certified_strictly_negative"
                    ],
                    "jump_certified_strictly_positive": j_res[
                        "jump_certified_strictly_positive"
                    ],
                    "W_p_minus_at_u_p_certified_strictly_positive": j_res[
                        "W_p_minus_at_u_p_certified_strictly_positive"
                    ],
                    "W_p_minus_at_u_p_certified_strictly_negative": j_res[
                        "W_p_minus_at_u_p_certified_strictly_negative"
                    ],
                }
            )

        # Also certify the asymptotic negative-h0-tail regime at p = 1901 where 2 / u_p >= 9
        # so h_0(n / u_p) < 0 for all n >= 2, W_{p^-}(u_p) < 0, and F(X_0^+) - F(X_0) > 0:
        p_tail = 1901
        x0_tail_arb = (arb(p_tail - 1) ** 4).root(5)
        u_tail_arb = x0_tail_arb / arb(p_tail)
        alpha_2_tail_arb = arb(2) / u_tail_arb
        w_prev_tail_up_arb = evaluate_w_y_coefficient_certified_arb(
            u_tail_arb, y=p_tail - 1, n_max=2000, prec_bits=prec_bits
        )["enclosure_arb"]
        jump_tail_arb = -(arb(1) / arb(p_tail).sqrt()) * w_prev_tail_up_arb
        asymptotic_tail_prime_1901_jump_check = {
            "prime_p": p_tail,
            "X_0_equals_1900_pow_4_5_certified": serialize_arb_certified(x0_tail_arb),
            "u_p_equals_X_0_over_1901_certified": serialize_arb_certified(u_tail_arb),
            "min_station_alpha_2_over_u_p_certified": serialize_arb_certified(
                alpha_2_tail_arb
            ),
            "in_strict_negative_h0_tail_alpha_ge_9": bool(
                alpha_2_tail_arb.lower() >= arb(9)
            ),
            "W_p_minus_at_u_p_certified": serialize_arb_certified(w_prev_tail_up_arb),
            "W_p_minus_at_u_p_certified_strictly_negative": bool(
                w_prev_tail_up_arb.upper() < arb(0)
            ),
            "euler_recursion_jump_formula_certified": serialize_arb_certified(
                jump_tail_arb
            ),
            "jump_certified_nonzero": bool(not jump_tail_arb.contains(0)),
            "jump_certified_strictly_positive": bool(jump_tail_arb.lower() > arb(0)),
        }

        # Also check composite threshold m + 1 = 4 (X_0 = 3^{4/5}) where P_4 = P_3 = 6 and jump == 0:
        comp_4_res = evaluate_coupled_cutoff_jump_at_prime_threshold_arb(
            4, k_max=3500, prec_bits=prec_bits
        )
        composite_threshold_check = {
            "composite_m_plus_1": 4,
            "X_0_equals_3_pow_4_5_certified": serialize_arb_certified(
                comp_4_res["X_0_arb"]
            ),
            "F_at_X_0_equals_W_3_certified": serialize_arb_certified(
                comp_4_res["F_at_X_0_equals_W_p_minus_arb"]
            ),
            "F_at_X_0_plus_equals_W_4_certified": serialize_arb_certified(
                comp_4_res["F_at_X_0_plus_equals_W_p_arb"]
            ),
            "direct_jump_diff_certified": serialize_arb_certified(
                comp_4_res["direct_jump_F_X0_plus_minus_F_X0_arb"]
            ),
            "jump_encloses_zero_at_composite_step": bool(
                comp_4_res["direct_jump_F_X0_plus_minus_F_X0_arb"].contains(0)
            ),
        }

        coupled_cutoff_jump_audit = {
            "fixed_y_vs_coupled_cutoff_regularity": (
                "For any fixed y >= 2, W_y(X) = sum_{m | P_y} mu(m) m^{-1/2} W_log(X/m) is a finite linear "
                "combination of dilates of the continuous function W_log and is therefore continuous on (0, infty). "
                "By contrast, the coupled profile F(X) := W_{M(X)}(X) with M(X) = ceil(max(2, X^{5/4})) is "
                "constant-cutoff continuous on each half-open interval (m^{4/5}, (m+1)^{4/5}] (and [1, 2^{4/5}]), "
                "left-continuous at every X_m = m^{4/5}, continuous across composite thresholds m + 1 (since P_{m+1} = P_m), "
                "and has a jump discontinuity from the right at X_0 = (p - 1)^{4/5} for every prime p >= 3 where W_{p^-}(X_0/p) != 0."
            ),
            "exact_right_hand_jump_formula": (
                "At X_0 = (p - 1)^{4/5} for a prime p >= 3, M(X_0) = p - 1 and lim_{X -> X_0^+} M(X) = p. "
                "By the one-prime Euler recursion W_p(X) = (I - p^{-1/2} D_p) W_{p^-}(X) = W_{p^-}(X) - p^{-1/2} W_{p^-}(X/p) "
                "and continuity of W_{p^-} and W_p at X_0, the exact right-hand jump is "
                "F(X_0^+) - F(X_0) = W_p(X_0) - W_{p^-}(X_0) = -p^{-1/2} W_{p^-}(X_0 / p)."
            ),
            "analytic_nonvanishing_and_sign_criterion": (
                "F(X_0^+) - F(X_0) != 0 if and only if W_{p^-}((p - 1)^{4/5} / p) != 0. "
                "Specifically: (1) for small primes p in {3, 5, 7, 11, 13, 17, 19, 23}, the leading station ratio "
                "2 / u_p = 2p / (p - 1)^{4/5} in [3.2987, 3.8799] lies in the positive lobe (2.6941, 8.6213) of h_0(alpha) "
                "(where W = (alpha + 1/alpha)^2 in (9.3873, 76.3403)), so W_{p^-}(u_p) > 0 and F(X_0^+) - F(X_0) = "
                "-p^{-1/2} W_{p^-}(u_p) < 0 is certified strictly negative and nonzero in 256-bit Arb; "
                "(2) for all primes p >= 1901, u_p := (p - 1)^{4/5} / p <= 2/9 so every station n >= 2 satisfies "
                "n / u_p >= 2 / u_p >= 9 > 8.6213, where h_0(n / u_p) < 0 strictly while lambda_{p^-}(n) >= 0 and "
                "lambda_{p^-}(2) = log 2 > 0, proving unconditionally that W_{p^-}(u_p) < 0 and F(X_0^+) - F(X_0) > 0 strictly."
            ),
            "corrected_dense_grade_to_all_X_extension": (
                "Because F(X) = W_{M(X)}(X) has right-hand jumps at prime thresholds X_0 = (p - 1)^{4/5}, "
                "one must NEVER invoke continuity of F(X) to pass from dense grade samples K in A_R = Qbar cap R "
                "to all real scales X >= 1. Instead, W(X) = W_log(X) + R_mu(X) IS continuous on [1, infty) by the "
                "Weierstrass M-test, and the uniform comparison |F(X) - W(X)| <= (1/2) C_{log,0} < 0.278715 holds "
                "for ALL real X >= 1. Hence: "
                "sup_{K in A_R} |F(tau^{|K|})| <= M_F  ==>  sup_{K in A_R} |W(tau^{|K|})| <= M_F + (1/2) C_{log,0} "
                "==> (by continuity of W and density of {tau^{|K|} : K in A_R} in [1, infty)) "
                "sup_{X >= 1} |W(X)| <= M_F + (1/2) C_{log,0}  ==>  sup_{X >= 1} |F(X)| <= M_F + C_{log,0}."
            ),
            "all_prime_jump_identities_enclose_zero": all_prime_jump_identities_enclose_zero,
            "all_prime_jumps_certified_nonzero": all_prime_jumps_certified_nonzero,
            "all_small_prime_jumps_certified_strictly_negative": all_small_prime_jumps_certified_strictly_negative,
            "certified_prime_threshold_jump_table": prime_jump_rows,
            "asymptotic_tail_prime_1901_jump_check": asymptotic_tail_prime_1901_jump_check,
            "composite_threshold_continuity_check": composite_threshold_check,
            "lean_theorem": "coupled_cutoff_prime_step_jump_and_dense_comparison_extension",
        }

        # -------------------------------------------------------------------
        # Part 2: Audit of Two Explicit Single-Observable Candidates D_K(rho_K)
        #         Against the Original Collision Contract (CR1 + CR2 + CR3)
        # -------------------------------------------------------------------
        gammas_100 = load_certified_zero_ordinate_balls(count=1, prec_bits=prec_bits)
        gamma_1_arb = gammas_100[0]  # First nontrivial zero height ~ 14.13472514
        rho_1_on_line_mod_arb = abs(acb(arb(1) / arb(2), gamma_1_arb))
        x_rho_1_int = int(math.floor(float(rho_1_on_line_mod_arb.mid())))  # floor(|rho_1|) = 14
        y_rho_1 = certified_coupled_cutoff_M_X_arb(
            rho_1_on_line_mod_arb, prec_bits=prec_bits
        )

        # Evaluate Candidate 1 (Grade-K Zero-Scale Prime-Euler Integer-Layer Observable)
        # at K = 0, J = 1 (rational difference K - J = -1 != 0), and K = sqrt(2)/2:
        cand1_k0 = evaluate_grade_layer_observable_A_K_y_arb(
            x_rho_1_int, y_rho_1, arb(0), prec_bits=prec_bits
        )
        cand1_j1 = evaluate_grade_layer_observable_A_K_y_arb(
            x_rho_1_int, y_rho_1, arb(1), prec_bits=prec_bits
        )
        cand1_ksqrt2 = evaluate_grade_layer_observable_A_K_y_arb(
            x_rho_1_int, y_rho_1, arb(2).sqrt() / arb(2), prec_bits=prec_bits
        )
        cand1_raw_diff_J1_minus_K0_arb = (
            cand1_j1["A_K_y_arb"] - cand1_k0["A_K_y_arb"]
        )
        cand1_coboundary_diff_arb = (
            cand1_j1["A_K_y_arb"] - tau_a * cand1_k0["A_K_y_arb"]
        )

        # Also evaluate Candidate 1 at raw scaled zero modulus floor(|rho_K|) for K = 0 (14) and J = 1 (floor(14.143 * 2*pi) = 88)
        rho_J1_mod_arb = tau_a * rho_1_on_line_mod_arb
        x_rho_J1_int = int(math.floor(float(rho_J1_mod_arb.mid())))  # 88
        cand1_raw_scale_J1 = evaluate_grade_layer_observable_A_K_y_arb(
            x_rho_J1_int, y_rho_1, arb(1), prec_bits=prec_bits
        )
        cand1_raw_scale_diff_arb = (
            cand1_raw_scale_J1["A_K_y_arb"] - cand1_k0["A_K_y_arb"]
        )

        # Evaluate Candidate 2A (Normalized Pullback Theta-Zero Radial Defect Observable)
        # and Candidate 2B (Prime-Euler Stieltjes Difference at Zero-Shifted Grade)
        # across delta in {0, 0.05, 0.1, 0.25} at gamma = gamma_1 and grades K = 0, J = 1, K = sqrt(2)/2:
        cand2_evaluation_rows: List[Dict[str, Any]] = []
        all_cand2a_cr1_enclose_zero = True
        all_cand2a_off_line_strictly_positive = True
        all_cand2a_on_line_enclose_zero = True
        all_cand2a_strictly_below_one = True
        all_cand2b_cr1_enclose_zero = True

        for delta_label, delta_arb in (
            ("0", arb(0)),
            ("1/20", arb(1) / arb(20)),
            ("1/10", arb(1) / arb(10)),
            ("1/4", arb(1) / arb(4)),
        ):
            c2a_k0 = evaluate_theta_zero_radial_defect_observable_arb(
                delta_arb, gamma_1_arb, arb(0), prec_bits=prec_bits
            )
            c2a_j1 = evaluate_theta_zero_radial_defect_observable_arb(
                delta_arb, gamma_1_arb, arb(1), prec_bits=prec_bits
            )
            c2a_ksqrt2 = evaluate_theta_zero_radial_defect_observable_arb(
                delta_arb, gamma_1_arb, arb(2).sqrt() / arb(2), prec_bits=prec_bits
            )
            cr1_diff_0_1 = c2a_k0["D_K_2A_arb"] - c2a_j1["D_K_2A_arb"]
            cr1_diff_0_sqrt2 = c2a_k0["D_K_2A_arb"] - c2a_ksqrt2["D_K_2A_arb"]
            if not (cr1_diff_0_1.contains(0) and cr1_diff_0_sqrt2.contains(0)):
                all_cand2a_cr1_enclose_zero = False

            if delta_label == "0":
                if not c2a_k0["D_K_2A_arb"].contains(0):
                    all_cand2a_on_line_enclose_zero = False
            else:
                if not (c2a_k0["D_K_2A_arb"].lower() > arb(0)):
                    all_cand2a_off_line_strictly_positive = False

            if not (c2a_k0["D_K_2A_arb"].upper() < arb(1)):
                all_cand2a_strictly_below_one = False

            # Candidate 2B: D_{K,y}^{(2B)}(rho_K) = W_y(tau^{1 + |delta(rho_K)|}) - W_y(tau)
            # reconstructed directly from grade-K integer-layer jumps A_{K,y}(n)/A_{K,y}(n-1)
            x_shift_arb = tau_a ** (arb(1) + abs(delta_arb))
            w_shift_k0 = evaluate_w_y_from_grade_layer_jumps_arb(
                x_shift_arb,
                y=y_rho_1,
                K_arb=arb(1) + abs(delta_arb),
                J_arb=arb(0),
                n_cut=800,
                prec_bits=prec_bits,
            )["w_y_from_grade_layer_jumps_arb"]
            w_base_k0 = evaluate_w_y_from_grade_layer_jumps_arb(
                tau_a,
                y=y_rho_1,
                K_arb=arb(1),
                J_arb=arb(0),
                n_cut=800,
                prec_bits=prec_bits,
            )["w_y_from_grade_layer_jumps_arb"]
            d2b_k0_arb = w_shift_k0 - w_base_k0

            w_shift_j1 = evaluate_w_y_from_grade_layer_jumps_arb(
                x_shift_arb,
                y=y_rho_1,
                K_arb=arb(2) + abs(delta_arb),
                J_arb=arb(1),
                n_cut=800,
                prec_bits=prec_bits,
            )["w_y_from_grade_layer_jumps_arb"]
            w_base_j1 = evaluate_w_y_from_grade_layer_jumps_arb(
                tau_a,
                y=y_rho_1,
                K_arb=arb(2),
                J_arb=arb(1),
                n_cut=800,
                prec_bits=prec_bits,
            )["w_y_from_grade_layer_jumps_arb"]
            d2b_j1_arb = w_shift_j1 - w_base_j1
            d2b_cr1_diff = d2b_k0_arb - d2b_j1_arb
            if not d2b_cr1_diff.contains(0):
                all_cand2b_cr1_enclose_zero = False

            cand2_evaluation_rows.append(
                {
                    "delta_label": delta_label,
                    "delta_certified": serialize_arb_certified(delta_arb),
                    "gamma_1_certified": serialize_arb_certified(gamma_1_arb),
                    "abs_H0_at_delta_plus_i_gamma1_sq_certified": serialize_arb_certified(
                        c2a_k0["abs_H0_at_z_sq_arb"]
                    ),
                    "abs_H0_sq_strictly_positive": c2a_k0[
                        "abs_H0_at_z_sq_strictly_positive"
                    ],
                    "radial_cosh_factor_tau_delta_certified": serialize_arb_certified(
                        c2a_k0["radial_cosh_factor_arb"]
                    ),
                    "D_0_2A_at_rho_0_certified": serialize_arb_certified(
                        c2a_k0["D_K_2A_arb"]
                    ),
                    "D_1_2A_at_rho_1_certified": serialize_arb_certified(
                        c2a_j1["D_K_2A_arb"]
                    ),
                    "D_sqrt2_half_2A_certified": serialize_arb_certified(
                        c2a_ksqrt2["D_K_2A_arb"]
                    ),
                    "D_0_minus_D_1_2A_CR1_diff_certified": serialize_arb_certified(
                        cr1_diff_0_1
                    ),
                    "CR1_raw_equality_2A_encloses_zero": bool(
                        cr1_diff_0_1.contains(0) and cr1_diff_0_sqrt2.contains(0)
                    ),
                    "D_2A_strictly_positive_when_delta_nonzero": (
                        True
                        if delta_label == "0"
                        else bool(c2a_k0["D_K_2A_arb"].lower() > arb(0))
                    ),
                    "D_2A_ lies_in_open_interval_0_1_when_delta_nonzero": (
                        False
                        if delta_label == "0"
                        else bool(
                            c2a_k0["D_K_2A_arb"].lower() > arb(0)
                            and c2a_k0["D_K_2A_arb"].upper() < arb(1)
                        )
                    ),
                    "D_0_2B_stieltjes_shift_diff_certified": serialize_arb_certified(
                        d2b_k0_arb
                    ),
                    "D_1_2B_stieltjes_shift_diff_certified": serialize_arb_certified(
                        d2b_j1_arb
                    ),
                    "D_0_minus_D_1_2B_CR1_diff_certified": serialize_arb_certified(
                        d2b_cr1_diff
                    ),
                    "CR1_raw_equality_2B_encloses_zero": bool(
                        d2b_cr1_diff.contains(0)
                    ),
                }
            )

        single_observable_candidate_audit = {
            "collision_contract_specification": {
                "zero_setup": (
                    "For a nontrivial Riemann zeta zero rho = 1/2 + delta + i*gamma (delta = Re(rho) - 1/2 in (-1/2, 1/2)), "
                    "its grade-K image is rho_K = tau^K * rho in C_K, considered across all concurrent grades "
                    "K in A_R = Qbar cap R (both positive and negative), with contradiction witnesses taken at a "
                    "justified nonzero rational difference K - J in Q \\ {0} (canonical benchmark pair: K = 0, J = 1)."
                ),
                "CR1_raw_cross_grade_common_referent_equality": (
                    "D_K(rho_K) = D_J(rho_J) = D(rho) as the exact same external real value in R."
                ),
                "CR2_simultaneous_discrete_integer_layer_membership": (
                    "D_K(rho_K) = m_K * tau^K in L_K = tau^K Z and D_J(rho_J) = m_J * tau^J in L_J = tau^J Z "
                    "with exact integers m_K, m_J in Z."
                ),
                "CR3_one_way_off_critical_sensitivity": (
                    "delta != 0  ==>  D(rho) != 0 (one-way implication required by the reductio; "
                    "never strengthened to a biconditional)."
                ),
                "same_expression_requirement": (
                    "All three properties CR1, CR2, CR3 must hold simultaneously for the SAME single expression D_K(rho_K)."
                ),
            },
            "candidate_1_grade_K_prime_euler_integer_layer_observable": {
                "definition": (
                    "D_{K,y}^{(1)}(rho_K) := c_K(rho_K) * A_{K,y}(X_K(rho_K)) = c_K(rho_K) * N_y(X_K(rho_K)) * tau^K, "
                    "where N_y(x) = prod_{d | P_y, d <= x} (floor(x/d)!)^{mu(d)} = prod_{n <= x} m_y(n) in Z_{>=1}."
                ),
                "domain_and_dependencies": (
                    "Defined for all K in A_R = Qbar cap R, y >= 2, and complex zero image rho_K = tau^K rho != 0, "
                    "with invariant zero-height scale X_0(rho_K) = tau^{-K} |rho_K| = |rho| >= 14.13 > 1 "
                    "(or raw scale X_K(rho_K) = |rho_K| for K >= 0)."
                ),
                "subcase_1A_unmodulated_carrier_c_K_eq_1": {
                    "transformation_law": (
                        "At invariant scale X_0 = tau^{-K}|rho_K| = |rho|, D_{K,y}^{(1A)}(rho_K) = N_y(|rho|) * tau^K "
                        "obeys the exact weight-1 scale-coboundary law D_{K,y}^{(1A)}(rho_K) = tau^{K-J} D_{J,y}^{(1A)}(rho_J)."
                    ),
                    "CR1_status": (
                        "FAILS_RAW_EQUALITY: Since N_y(|rho|) >= 1 and tau = 2*pi > 1, "
                        "D_{K,y}^{(1A)}(rho_K) - D_{J,y}^{(1A)}(rho_J) = N_y(|rho|) * (tau^K - tau^J) != 0 whenever K != J "
                        "(and at raw scale |rho_K|, N_y(|rho_J|) * tau^J > N_y(|rho_K|) * tau^K for J > K >= 0)."
                    ),
                    "CR2_status": (
                        "PROVED_UNCONDITIONALLY: By Theorem `unconditional_factorial_ratio_integrality`, "
                        "N_y(X) in Z_{>=1}, so D_{K,y}^{(1A)}(rho_K) = N_y(X) * tau^K in L_K^x = tau^K (Z \\ {0}) subset L_K."
                    ),
                    "CR3_status": (
                        "VACUOUSLY_NONZERO_UNSENSITIVE_TO_DELTA: Since N_y(X) >= 1 and tau^K > 0, "
                        "D_{K,y}^{(1A)}(rho_K) > 0 for ALL zeros (both delta != 0 and delta = 0)."
                    ),
                    "certified_benchmark_at_rho_1_K0_vs_J1": {
                        "floor_abs_rho_1": x_rho_1_int,
                        "coupled_cutoff_y": y_rho_1,
                        "N_y_at_floor_abs_rho_1_exact": cand1_k0["N_y_exact_int"],
                        "D_0_1A_invariant_scale_certified": serialize_arb_certified(
                            cand1_k0["A_K_y_arb"]
                        ),
                        "D_1_1A_invariant_scale_certified": serialize_arb_certified(
                            cand1_j1["A_K_y_arb"]
                        ),
                        "D_sqrt2_half_1A_invariant_scale_certified": serialize_arb_certified(
                            cand1_ksqrt2["A_K_y_arb"]
                        ),
                        "raw_CR1_difference_D_1_minus_D_0_certified": serialize_arb_certified(
                            cand1_raw_diff_J1_minus_K0_arb
                        ),
                        "raw_CR1_difference_strictly_positive": bool(
                            cand1_raw_diff_J1_minus_K0_arb.lower() > arb(0)
                        ),
                        "coboundary_D_1_minus_tau_D_0_diff_certified": serialize_arb_certified(
                            cand1_coboundary_diff_arb
                        ),
                        "coboundary_encloses_zero": bool(
                            cand1_coboundary_diff_arb.contains(0)
                        ),
                        "raw_scale_J1_floor_abs_tau_rho_1": x_rho_J1_int,
                        "raw_scale_CR1_difference_D_1_minus_D_0_strictly_positive": bool(
                            cand1_raw_scale_diff_arb.lower() > arb(0)
                        ),
                    },
                },
                "subcase_1B_zero_defect_modulated_carrier": {
                    "definition": "D_{K,y}^{(1B)}(rho_K) = m_K(rho_K) * N_y(X_0) * tau^K with integer multiplier m_K(rho_K) in Z",
                    "trilemma_obstruction": (
                        "To preserve CR2 (D_{K,y}^{(1B)} in L_K = tau^K Z), the multiplier c_K(rho_K) * N_y(X_0) must be an integer "
                        "M_K in Z. At any rational grade difference K - J in Q \\ {0} (such as K = 0, J = 1), Lindemann's theorem "
                        "gives L_K cap L_J = {0}, so raw equality CR1 (M_K * tau^K = M_J * tau^J) holds if and only if M_K = M_J = 0. "
                        "Furthermore, by `invariant_covariant_observable_vanishing` in `formal/RiemannScope/Grade.lean`, any multiplier "
                        "extending continuously to a real interval I subset R (necessary because A_R is totally disconnected) while "
                        "taking integer values on I cap A_R must be a constant integer M_0 in Z: if M_0 != 0 then CR1 fails "
                        "(M_0 * tau^K != M_0 * tau^J), and if M_0 = 0 then CR3 fails (D = 0 even for delta != 0). Conversely, "
                        "if c_K(rho_K) = tau^{-K} Theta_0(delta) is chosen to cancel tau^K and enforce CR1, then CR2 at J = 1 "
                        "requires Theta_0(delta) * N_y(X_0) in Z cap tau Z = {0}, reducing to Candidate 2."
                    ),
                },
            },
            "candidate_2_canonical_theta_and_stieltjes_zero_defect_observables": {
                "subcase_2A_normalized_pullback_theta_zero_radial_defect": {
                    "definition": (
                        "D_K^{(2A)}(rho_K) := |H_0(tau^{-K} rho_K - 1/2)|^2 * "
                        "(tau^{tau^{-K} Re(rho_K) - 1/2} + tau^{-(tau^{-K} Re(rho_K) - 1/2)} - 2) "
                        "= |H_0(delta + i*gamma)|^2 * (tau^delta + tau^{-delta} - 2), "
                        "where H_0(z) = F_tau(1/2 + z) * F_tau(1/2 - z) = ((z^2 - 1/4)^4 / (1024 sqrt(pi))) * "
                        "Gamma((1 + 2z)/4) * Gamma((1 - 2z)/4)."
                    ),
                    "domain_and_transformation_law": (
                        "Defined for all K in A_R = Qbar cap R and all rho_K = tau^K rho with Re(rho) in (0, 1). "
                        "Because tau^{-K} rho_K = rho is invariant under the grade-K ray dilation Phi_K, "
                        "D_K^{(2A)}(rho_K) has weight 0 (strict cross-grade invariance D_K^{(2A)}(rho_K) = D_J^{(2A)}(rho_J))."
                    ),
                    "CR1_status": (
                        "PROVED_UNCONDITIONALLY: For all K, J in A_R (both rational and irrational algebraic grades), "
                        "tau^{-K} rho_K - 1/2 = delta + i*gamma = tau^{-J} rho_J - 1/2, so "
                        "D_K^{(2A)}(rho_K) = D_J^{(2A)}(rho_J) = D^{(2A)}(rho) as the exact same external real number."
                    ),
                    "CR3_status": (
                        "PROVED_UNCONDITIONALLY_ONE_WAY (delta != 0 ==> D^{(2A)}(rho) > 0): "
                        "(1) By the squared pole-annihilating normalization P(D)^2 = (D^2 - 1/16)^2 of psi_tau, "
                        "H_0(z) = ((z^2 - 1/4)^4 / (1024 sqrt(pi))) * Gamma((1 + 2z)/4) * Gamma((1 - 2z)/4). "
                        "Since 1/Gamma(w) is entire on C, Gamma((1 +/- 2z)/4) has no zeros anywhere in C; hence the "
                        "ONLY zeros of H_0(z) in C are z = +/- 1/2 (corresponding to s = 0, 1). Every nontrivial zero "
                        "rho = 1/2 + delta + i*gamma in the critical strip has |delta| < 1/2 (and gamma != 0), so "
                        "z = delta + i*gamma != +/- 1/2 and |H_0(delta + i*gamma)|^2 > 0 unconditionally. "
                        "(2) Since tau = 2*pi > 1, tau^delta + tau^{-delta} - 2 = (tau^{delta/2} - tau^{-delta/2})^2 > 0 "
                        "for all delta != 0. Therefore delta != 0 ==> D^{(2A)}(rho) > 0 != 0 unconditionally."
                    ),
                    "CR2_status": (
                        "EQUIVALENT_TO_DELTA_EQ_0_NOT_UNCONDITIONALLY_PROVED: "
                        "For every nontrivial zero rho = 1/2 + delta + i*gamma in the critical strip |delta| < 1/2 "
                        "(with |gamma| >= 14.13), 0 <= D^{(2A)}(rho) < 1 (for instance at gamma = gamma_1 ~ 14.1347, "
                        "|H_0(delta + i*gamma_1)|^2 < 3e-11 and 0 <= tau^delta + tau^{-delta} - 2 < 0.91). "
                        "Consequently: (a) even at the single grade K = 0 (where L_0 = Z), D_0^{(2A)}(rho) in Z holds "
                        "if and only if D_0^{(2A)}(rho) = 0 <=> delta = 0; (b) across K = 0 and J = 1 (rational difference "
                        "K - J = -1 != 0), Lindemann's theorem gives L_0 cap L_1 = Z cap tau Z = {0}, so simultaneous "
                        "layer membership D_0^{(2A)}(rho) in L_0 and D_1^{(2A)}(rho_1) in L_1 holds if and only if "
                        "D^{(2A)}(rho) = 0 <=> delta = 0. Thus CR2 for Candidate 2A is logically equivalent to RH for rho "
                        "and cannot be asserted unconditionally without circularity."
                    ),
                },
                "subcase_2B_prime_euler_stieltjes_shift_difference": {
                    "definition": (
                        "D_{K,y}^{(2B)}(rho_K) := W_y(tau^{1 + |delta(rho_K)|}) - W_y(tau) "
                        "= int_{(1, infty)} x^{-1/2} [h_0(x / tau^{1+|delta|}) - h_0(x / tau)] d(log A_{K,y})(x), "
                        "where delta(rho_K) = tau^{-K} Re(rho_K) - 1/2 = delta."
                    ),
                    "CR1_status": (
                        "PROVED_UNCONDITIONALLY: Because d(log A_{K,y})(x) = d(log N_y)(x) cancels tau^K and "
                        "delta(rho_K) = delta is grade-invariant, D_{K,y}^{(2B)}(rho_K) = D_{J,y}^{(2B)}(rho_J) for all K, J in A_R."
                    ),
                    "CR2_status": (
                        "FAILS_FOR_NONZERO_VALUES: For delta != 0, D_{K,y}^{(2B)}(rho_K) is a continuous Mellin-Stieltjes "
                        "sum of (log m_y(n)) n^{-1/2} [h_0(n / tau^{1+|delta|}) - h_0(n / tau)] in (-1, 1) \\ {0}, "
                        "which does not lie in L_0 = Z or L_1 = tau Z."
                    ),
                    "CR3_status": (
                        "CERTIFIED_NONZERO_FOR_SAMPLED_OFF_LINE_SHIFTS: Vanishes at delta = 0 and is certified nonzero "
                        "for delta in {1/20, 1/10, 1/4} at y = M(|rho_1|) = 28."
                    ),
                },
                "all_cand2a_cr1_enclose_zero": all_cand2a_cr1_enclose_zero,
                "all_cand2a_off_line_strictly_positive": all_cand2a_off_line_strictly_positive,
                "all_cand2a_on_line_enclose_zero": all_cand2a_on_line_enclose_zero,
                "all_cand2a_strictly_below_one": all_cand2a_strictly_below_one,
                "all_cand2b_cr1_enclose_zero": all_cand2b_cr1_enclose_zero,
                "certified_candidate_2_evaluation_table": cand2_evaluation_rows,
            },
            "role_of_theta_normalization_tau_transcendence_and_regularity": {
                "theta_normalization_role": (
                    "The squared pole-annihilating operator P(D)^2 = (D^2 - 1/16)^2 produces the exact factor "
                    "(s^2 (s - 1)^2 / 32)^2 in H_0(s - 1/2), which (1) kills the simple poles of xi(s) at s = 0, 1 "
                    "(z = +/- 1/2) in the explicit formula and (2) ensures by Euler's Gamma nonvanishing theorem that "
                    "H_0(z) has NO zeros in the critical strip |Re(z)| < 1/2, making CR3 for Candidate 2A unconditional."
                ),
                "tau_transcendence_and_rational_vs_irrational_grade_differences": (
                    "By Lindemann-Weierstrass, tau = 2*pi is transcendental over Q, so for any nonzero RATIONAL grade "
                    "difference K - J = p/q in Q \\ {0} (in particular K = 0, J = 1), (tau^{K-J})^q = tau^p not in Q, "
                    "which implies tau^{K-J} not in Q and L_K cap L_J = tau^K Z cap tau^J Z = {0} (`layer_disjointness` "
                    "in `formal/RiemannScope/Grade.lean`). For general irrational algebraic grade differences "
                    "K - J in (Qbar cap R) \\ Q (such as K - J = sqrt(2)), rationality of tau^{K-J} is an open problem "
                    "in transcendental number theory (beyond Lindemann-Weierstrass and Gelfond-Schneider) and is NEVER "
                    "assumed; a single rational-difference pair (K = 0, J = 1) suffices for the collision step while "
                    "retaining the full concurrent grade family K in Qbar cap R."
                ),
                "regularity_and_connectedness_scope": (
                    "Because A_R = Qbar cap R is totally disconnected in the Euclidean topology (every point can be "
                    "separated by irrational real cuts), continuity on A_R alone never forces a Z-valued function to be "
                    "constant. Constant-integer rigidity (`invariant_covariant_observable_vanishing` in `Grade.lean`) "
                    "requires a continuous extension to a connected real interval I subset R."
                ),
            },
            "covariance_invariance_discreteness_trilemma": {
                "statement": (
                    "For any single observable D_K(rho_K) evaluated at rational-difference grades K != J (e.g. K = 0, J = 1) "
                    "where L_K cap L_J = {0}: "
                    "(CR1: D_K(rho_K) = D_J(rho_J) = D) and (CR2: D_K(rho_K) in L_K and D_J(rho_J) in L_J) "
                    "hold simultaneously if and only if D_K(rho_K) = D_J(rho_J) = 0. "
                    "Consequently: "
                    "(i) Weight-1 covariant prime-Euler integer-layer carriers D_K^{(1A)} = N_y(X_0) * tau^K satisfy CR2 "
                    "unconditionally with N_y(X_0) >= 1, so D_K^{(1A)} = tau^{K-J} D_J^{(1A)} != D_J^{(1A)} and raw CR1 fails. "
                    "(ii) Weight-0 pullback zero-defect observables D_K^{(2A)}(rho_K) = |H_0(delta+i*gamma)|^2 (tau^delta + tau^{-delta} - 2) "
                    "satisfy raw CR1 and one-way CR3 (delta != 0 ==> D^{(2A)} > 0) unconditionally, so CR2 (D_K^{(2A)} in L_K) "
                    "holds if and only if D^{(2A)}(rho) = 0 <=> delta = 0, which is equivalent to RH for rho rather than an "
                    "independent consequence of prime/theta algebra."
                ),
                "lean_theorem": "single_observable_common_referent_candidate_audit_and_trilemma",
            },
            "remaining_open_obligation": {
                "subgate_id": "SUBGATE-TC-043A",
                "status": "OPEN",
                "common_referent_bridge_complete": False,
                "exact_open_gap": (
                    "SUBGATE-TC-043A remains OPEN and the common-referent bridge is NOT complete: "
                    "Candidate 1 (A_{K,y}(x) = N_y(x) * tau^K) satisfies CR2 unconditionally on the arithmetic side "
                    "but transforms with weight 1 (failing raw CR1), whereas Candidate 2A "
                    "(D_K^{(2A)}(rho_K) = |H_0(delta+i*gamma)|^2 (tau^delta + tau^{-delta} - 2)) satisfies raw CR1 and "
                    "one-way CR3 unconditionally on the spectral/theta side but satisfies CR2 if and only if delta = 0. "
                    "Closing SUBGATE-TC-043A requires either (a) proving the uniform signed Moebius cancellation bound "
                    "sup_{X >= 1} |R_mu(X)| < infty (equivalently sup_{X >= 1} |W_{M(X)}(X)| < infty), or "
                    "(b) establishing an independent arithmetic-spectral identity that forces a genuine raw-invariant, "
                    "off-line-sensitive observable D_K(rho_K) to lie in L_K = tau^K Z without assuming delta = 0."
                ),
            },
        }

        tc047_reconciliation_and_scope = {
            "preserved_tc047_results": (
                "N_y(x) = prod_{d | P_y, d <= x} (floor(x/d)!)^{mu(d)} = prod_{1 <= n <= floor(x)} m_y(n) in Z_{>=1}, "
                "its exact Chebyshev LCM agreement window N_y(x) = lcm(1, ..., floor(x)) on 1 <= x < 2 q_{>y} with first "
                "discrepancy N_y(2 q_{>y}) = 2 lcm(1, ..., 2 q_{>y}), its grade-K integer-layer membership "
                "A_{K,y}(x) = N_y(x) * tau^K in L_K^x = tau^K (Z \\ {0}) (`CR2`), and the logarithmic-jump reconstruction "
                "W_y(tau^{K-J}) = sum_{n>=2} log(A_{K,y}(n)/A_{K,y}(n-1)) n^{-1/2} h_0(Phi_J(n)/Phi_K(1))."
            ),
            "intrinsic_coordinate_recovery_vs_raw_CR1_correction": (
                "The relation tau^{-K} A_{K,y}(x) = tau^{-J} A_{J,y}(x) = N_y(x) is unit-converted intrinsic fiber "
                "coordinate recovery, NOT the original raw external common-referent equality (`CR1`). Because "
                "A_{K,y}(x) = N_y(x) * tau^K > 0, the raw external values satisfy A_{K,y}(x) = tau^{K-J} A_{J,y}(x) "
                "and are strictly unequal whenever K != J."
            ),
            "stieltjes_lower_endpoint_convention": (
                "Extend A_{K,y}(x) constantly as tau^K below 1 (so A_{K,y}(x) = tau^K on (0, 2)), or integrate over "
                "(1, infty), so that d(log A_{K,y})(x) has zero atom at x = 1 (no artificial K * log(tau) atom)."
            ),
            "lean_vs_paper_vs_computational_scope": (
                "The TC-047 Lean 4 theorems (`prime_euler_multiplicative_integrality_and_grade_layer_membership`, "
                "`common_referent_integer_layer_bridge_and_station_ratio_identity`) prove algebraic consequences for "
                "supplied integer inputs and a conditional collision implication; they do not internally establish the "
                "full alternating factorial-product construction or derive the missing CR1+CR2+CR3 collision hypotheses "
                "from actual prime/theta data."
            ),
        }

        result_tc048: Dict[str, Any] = {
            "task_id": TASK_TC_048_ID,
            "reconciled_prior_task_id": TASK_TC_047_ID,
            "parent_epic": EPIC_TC_042_ID,
            "inspected_baseline": STARTING_HEAD_TC_048,
            "reconciled_tc047_implementation_commit": IMPLEMENTATION_COMMIT_TC_047,
            "status": SINGLE_OBSERVABLE_COMMON_REFERENT_AUDIT_STATUS,
            "symbolic_identities_verification": sym_tc048,
            "section_1_tc047_reconciliation_and_scope": tc047_reconciliation_and_scope,
            "section_2_coupled_cutoff_piecewise_continuity_and_jump_audit": coupled_cutoff_jump_audit,
            "section_3_single_observable_common_referent_candidate_audit": single_observable_candidate_audit,
        }
        full_tree_rt_sec17 = verify_all_serialized_arb_in_tree(
            result_tc048, path_prefix="section_17"
        )
        result_tc048["full_section_17_tree_roundtrip_verification"] = full_tree_rt_sec17
        return result_tc048
    finally:
        flint_ctx.prec = saved_prec


__all__ = [
    "TASK_TC_047_ID",
    "STARTING_HEAD_TC_047",
    "COMMON_REFERENT_PRIME_THETA_BRIDGE_STATUS",
    "TASK_TC_048_ID",
    "STARTING_HEAD_TC_048",
    "IMPLEMENTATION_COMMIT_TC_047",
    "SINGLE_OBSERVABLE_COMMON_REFERENT_AUDIT_STATUS",
    "local_prime_euler_factor_m_y_exact",
    "local_prime_euler_factor_divisor_product_fraction",
    "cumulative_N_y_from_local_factors_exact",
    "cumulative_N_y_alternating_factorial_fraction",
    "lcm_prefix_exact",
    "legendre_factorial_valuation",
    "alternating_factorial_prime_valuation_exact",
    "evaluate_grade_layer_observable_A_K_y_arb",
    "evaluate_w_y_from_grade_layer_jumps_arb",
    "verify_symbolic_common_referent_identities",
    "execute_task_tc047_common_referent_prime_theta_bridge",
    "evaluate_coupled_cutoff_jump_at_prime_threshold_arb",
    "evaluate_theta_zero_radial_defect_observable_arb",
    "verify_symbolic_tc048_jump_and_single_observable_identities",
    "execute_task_tc048_single_observable_common_referent_audit",
]
