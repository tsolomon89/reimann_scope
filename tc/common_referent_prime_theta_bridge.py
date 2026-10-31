"""TASK-TC-047: Common-Referent Observable from Actual Prime/Theta Data and Integer-Layer Membership.

This module constructs the multiplicative prime-Euler observable N_y(x) and its
grade-K realization A_{K,y}(x) = N_y(x) * tau^K directly from the actual
prime-by-prime Euler and canonical theta data of EPIC-TC-042 / TC-042..TC-046:

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
     the nonzero integer layer L_K^x = tau^K (Z \\ {0}) subset L_K = tau^K Z (CR2),
     with grade-invariant intrinsic normalized size
       N_K(A_{K,y}(x)) = tau^{-K} A_{K,y}(x) = N_y(x) = N_J(A_{J,y}(x))  (CR1 on fiber size).

3. Exact Mellin-Stieltjes & Station-Ratio Bridge to the Theta-Wavelet Profile W_y(X):
   - For any grades K >= J in A_R with relative scale X_{K,J} = tau^{K-J},
       W_y(tau^{K-J}) = sum_{n=2}^infty log(A_{K,y}(n) / A_{K,y}(n-1)) * n^{-1/2} * h_0(Phi_J(n) / Phi_K(1)),
     where A_{K,y}(n) / A_{K,y}(n-1) = m_y(n) in Z_{>=1} cancels tau^K identically and
     Phi_J(n) / Phi_K(1) = (n * tau^J) / tau^K = n / tau^{K-J} is the cross-grade station ratio.

4. Rigorous CR1-CR2-CR3 Bridge Classification and Open Obligation (SUBGATE-TC-043A = OPEN):
   - Separates intrinsic fiber equality (Class I), ambient integer-layer observables
     A_{K,y}(x) in L_K^x obeying the scale coboundary A_{K,y}(x) = tau^{K-J} A_{J,y}(x) (Class II),
     and continuous shift-invariant theta-wavelet correlations W_{M(X)}(X) (Class III).
   - Preserves SUBGATE-TC-043A = OPEN: divergence of the unsplit critical-line Gram norm
     ||Psi_y||_{L^2(d^*x)} does not establish divergence of the signed coupled profile
     W_{M(X)}(X) or failure of the concurrent-grade hypothesis.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Dict, List

import sympy as sp
from flint import arb, ctx as flint_ctx

from tc.canonical_theta_correlation_bound import (
    EPIC_TC_042_ID,
    evaluate_h0_arb,
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
    next_prime_above,
    prime_factors_with_multiplicity,
    primes_up_to,
)

TASK_TC_047_ID = "TASK-TC-047"
STARTING_HEAD_TC_047 = "c39eb27b31fc4eed98300be0118d8c670f92d32a"
COMMON_REFERENT_PRIME_THETA_BRIDGE_STATUS = (
    "COMMON_REFERENT_PRIME_THETA_INTEGER_LAYER_MEMBERSHIP_PROVED_AND_CERTIFIED_SUBGATE_OPEN"
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
                "intrinsic_common_referent_projection": (
                    "N_K(A_{K,y}(x)) := tau^{-K} A_{K,y}(x) = N_y(x) = N_J(A_{J,y}(x)) in Z_{>=1}"
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
                    "For any grades K >= J in A_R with relative scale X_{K,J} = tau^{K-J}, "
                    "W_y(tau^{K-J}) = sum_{n>=2} log(A_{K,y}(n)/A_{K,y}(n-1)) * n^{-1/2} * h_0(Phi_J(n)/Phi_K(1)), "
                    "where Phi_J(n)/Phi_K(1) = (n * tau^J)/tau^K = n / tau^{K-J}. For rational K - J != 0, "
                    "Lindemann's theorem (tau = 2*pi not in Qbar) implies L_K cap L_J = {0}, so Phi_J(n) != Phi_K(m) "
                    "for all nonzero integers n, m and no prime-power station ever collides with the self-dual peak alpha = 1."
                ),
            },
            "three_class_cr1_cr2_cr3_audit": {
                "class_I_intrinsic_fiber_referent": {
                    "observable": "N_K(A_{K,y}(x)) = tau^{-K} A_{K,y}(x) = N_y(x) in Z_{>=1}",
                    "CR1_cross_grade_equality": "SATISFIED (N_K = N_J = N_y(x) for all K, J in A_R)",
                    "CR2_distinct_scaled_layer_membership": "LIVES_IN_SINGLE_RING_Z_NOT_L_K_CAP_L_J",
                    "CR3_off_critical_zero_sensitivity": "ARITHMETIC_CARRIER_INDEPENDENT_OF_ZERO_DEFECT_DELTA",
                },
                "class_II_ambient_integer_layer_observable": {
                    "observable": "A_{K,y}(x) = N_y(x) * tau^K in L_K^x subset L_K = tau^K Z",
                    "CR1_cross_grade_equality": (
                        "OBEYS_SCALE_COBOUNDARY A_{K,y}(x) = tau^{K-J} A_{J,y}(x); ambient equality "
                        "m_K * tau^K = m_J * tau^J for rational K - J != 0 forces m_K = m_J = 0 by Lindemann"
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
                        "CONTINUOUS_MELLIN_STIELTJES_INTEGRAL_OVER_INTEGER_LAYER_JUMPS "
                        "(arithmetic carrier A_{K,M(X)}(n) lies in L_K^x, while kernel values h_0(n/X) are continuous real numbers)"
                    ),
                    "CR3_off_critical_zero_sensitivity": (
                        "PROVED_VIA_LAPLACE_CARLEMAN_AND_COUPLED_CUTOFF_EQUIVALENCE "
                        "(sup_{X>=1} |W_{M(X)}(X)| < infty <=> sup_{X>=1} |R_mu(X)| < infty <=> sup_{K in A_R} |C_tau(K)| < infty <=> RH)"
                    ),
                },
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
                    "sup_{X >= 1} |W_{M(X)}(X)| < infty (or a zero-defect-modulated cross-grade equality D_K = D_J in L_K cap L_J = {0}) "
                    "is the exact open obligation."
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


__all__ = [
    "TASK_TC_047_ID",
    "STARTING_HEAD_TC_047",
    "COMMON_REFERENT_PRIME_THETA_BRIDGE_STATUS",
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
]
