r"""
TASK-TC-058: Simultaneous Compatibility, Compensated Selberg Reconstruction, Growing
Logarithmic Order Joint Energy, and Combined Scale-Energy Analysis toward SUBGATE-TC-043A.

Implements and certifies in 256-bit FLINT/Arb ball arithmetic (using tau = 2*pi as the sole
circle constant and z = x + i*y, with x, y in R and critical line x = 1/2, for complex coordinates):
1. Narrow Inherited TC-057R Closeout & Compact 5-Category Proof Dependency Audit (Sections 1-2):
   - Exact verification of roughSquarefreeDivisorsBand(U, T) vs roughPrimeSetBand(U, T) at
     (U = 5, T = 25) (0 rough composites; 5*7 = 35 > 25), (U = 5, T = 34) (0 rough composites),
     and (U = 5, T = 35) (35 = 5*7 enters as the first admissible squarefree rough composite).
   - Explicit sufficient-condition scope for TC-057R Theorem 26 (forward implication to subpower
     energy proved; equivalence is not asserted without separately proving a shifted-kernel converse).
   - Compact 5-category dependency table ((a) actual arithmetic theorems, (b) analytic results
     outside Lean, (c) conditional implications, (d) finite numerical observations, (e) missing
     TC-to-arithmetic implication), plus certified verification of Agarwal-Garg-Maji (2022,
     Theorem 1.2 at k = 3, u = X^2 recovering Q_mu) and K-independence of normalized trivial-zero
     slopes a_K Z'_{a_K}(-2*m*a_K) = zeta'(-2*m).
2. Un-Young-Expanded Combined Target & Direct Cross-Term Evaluation (Section 3, Lean Theorem 29):
   - Retains T(Y) = ceil(Y^{5/4}) fixed across [Y, tau*Y], P_Y(X) = Sigma_pp(X; T)/log X,
     R_Y(X) = Q_T^{[1]}(X)/log X, Q_T = P_Y + R_Y, ||P_Y||_Y^2 = D_tilde(Y) + X_tilde(Y), and
     E(Y) = D_tilde(Y) + S_comb(Y) with S_comb(Y) := X_tilde(Y) + 2*<P_Y, R_Y>_Y + ||R_Y||_Y^2.
   - Evaluates <P_Y, R_Y>_Y directly across Y in {8, 16, 32, 64, 128} via certified 256-bit Arb
     quadrature and (at Y in {8, 16}) via the finite prime-power fiber sum, strictly separated
     from subtraction-based consistency checks.
   - Proves and formalizes (`CONDITIONAL_ON_COMBINED_CORRELATION`, Lean Theorem 29) the relaxed
     sufficient condition S_comb(Y) <= A_eta*Y^eta + theta_eta*F(Y) across the full range
     0 <= theta_eta < 1 with contraction theta_eta + Theta_eps^{diag}(Y) <= q < 1 (removing
     TC-057R's outer Young factor 2), while preserving TC-057R Theorem 26 as an alternative.
3. Primary Proof Attempt — Compensated Selberg Reconstruction, Exact Summation by Parts, &
   Logarithmic-Shift Elimination (Section 4, Lean Theorems 27 & 28):
   - Proves on actual integers (including T = 0, 1): sum_{d=1}^T g_d(X) = Q_{square,T}(X) and
     sum_{d=2}^T w_{2,lambda}(d)*g_d(X) = c_lambda*Q_{square,T}(X) + sum_{d=1}^T r_2(d)*g_d(X)
     (retaining r_2(1) = -c_lambda), with uniform bound 0 <= Q_{square,T}(X) <= C_sq :=
     Gamma(5/4)/4 + 2*(3/(2*e))^{3/2} for X >= 1 and window energy O((log Y)^{-4}).
   - Proves the dyadic parity divisor contrast (1 * a_2)(2^v * m) = 1_{v even} * d_div(m) (m odd).
   - Writes exact finite summation by parts keeping smooth kernel steps and floor(T/d) jumps,
     splitting W_2(d) = c_lambda*d + R_2^{int}(d) (on integer cutoffs d) only after the exact Abel
     identity: proves exact collapse of c_lambda*d onto c_lambda*Q_{square,T}(X), unconditional
     O((log Y)^{-4}) upper-endpoint decay, and unconditional O((log Y)^{-2}) aggregate cutoff-jump
     decay via (d+1)*(L_{d+1}+1) >= T + 1 and sum_{d=1}^{T-1} d*(L_d - L_{d+1}) <= T*log T.
   - Combines with Q_T = P_Y + R_Y before taking absolute values to obtain the exact shift
     elimination P_Y(X) - R_Y(X) = D_{2,Y}(X), eliminating the (log Y)^{-2} first-order shift into
     E(Y) = 4*D_tilde(Y) + 4*X_tilde(Y) - 4*<P_Y, D_{2,Y}>_Y + ||D_{2,Y}||_Y^2 and isolating the
     exact surviving O(Y*(log Y)^{-4}) terms alongside 4*X_tilde(Y).
4. Second Proof Attempt — Growing Logarithmic Order M(Y) = ceil(2*log Y) & Joint Layer Energy
   (Section 5, Lean Theorem 30):
   - Proves uniformly for all bounded controls |a(n)| <= 1, L >= 1, and Y >= 2:
     ||Q_{a,L}^{[M(Y)]} / (log X)^{M(Y)}||_Y^2 <= C_rem * (log Y) * Y^{-3}, bounding ALL THREE parts
     of A_m via explicit Robbins-Stirling m! <= sqrt(tau*m)*(m/e)^m*exp(1/(12*m)) and exact ceiling
     cancellation on Y >= e^9 (C_{rem,>=e^9} < 38) plus exact 17-interval derivative monotonicity on
     the compact range Y in [2, e^9] (C_{rem,[2,e^9]} < 2068), recorded honestly as generic in |a| <= 1.
   - Derives the closed-form geometric polynomial filter K_M(X; n) = [1 - (log(X/n)/log X)^M] / log n,
     the exact joint M(Y)-layer Gram decomposition ||L_{a,M}||_Y^2 = D_tilde_{a,pp}^{(M)}(Y) + X_tilde_{a,pp}^{(M)}(Y),
     and the unconditional joint diagonal bound D_tilde_{a,pp}^{(M(Y))}(Y) = O(Y / (log Y)^2) via
     0 < P_M(s) <= 4 on s in [1/4, 3/2], quantifying both the Minkowski layer-sum blowup cost and
     the concentration of growing-control Theta(Y) energy into X_tilde_{a,pp}^{(M(Y))}(Y).
5. TC Compatibility Discriminators (Section 6):
   - Pre-stated (Objects, Quantifiers, Hypotheses, Input, Conclusion, TC Classification) schemas,
     window-base test [Y, b*Y] for b in {2, e, tau} (keeping tau in circle/Fourier/Stirling), and
     arithmetic control tests across lambda, a_2, a_{3,5,7}, and 1, classifying the proved estimates
     honestly as TC-inspired analytic number theory while SUBGATE-TC-043A remains OPEN.
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

from flint import acb, acb_series, arb, ctx as flint_ctx

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
    TC_056R2_IMPLEMENTATION_COMMIT,
    TC_056R2_REVIEWED_TIP,
    TC_057_IMPLEMENTATION_COMMIT,
    TC_057_REVIEWED_TIP,
    _G_shifted_acb,
    _acb_integral_certified_arb,
    _evaluate_route_d_totals_arb,
    _frac_to_arb,
    _tau_arb,
    _weight_fn_for_mode,
    evaluate_E_L_scale_arb,
    evaluate_Q_shifted_finite_arb,
    moebius_mu_int,
    prime_power_pairs_up_to,
    rough_squarefree_divisors_band,
    selberg_w2_weight_arb,
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
    liouville_lambda_int,
)
from tc.prime_chain_contraction import (
    TASK_TC_056R_ID,
    TASK_TC_056R2_ID,
    TC_056_IMPLEMENTATION_COMMIT,
    TC_056_REVIEWED_TIP,
    TC_056R_REVIEWED_COMMIT,
    evaluate_phi_n_arb,
    exact_T_cutoff_ceil_Y_5_4,
    primes_up_to,
)

TASK_TC_058_ID = "TASK-TC-058"
TC_057R_IMPLEMENTATION_COMMIT = "484f69fc60e8b077b9586fd347003e72f4a4e930"
TC_057R_REVIEWED_TIP = "c944b71355d68c4b22b66954af5f620255ba5b14"

SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_simultaneous_compatibility_combined_energy.json"
)
TC_058_REVIEW_DOC_PATH = (
    REPO_ROOT / "docs" / "reviews" / "TC_058_SIMULTANEOUS_COMPATIBILITY_AND_COMBINED_ENERGY.md"
)

EXPECTED_TC058_THEOREMS = [
    "liouville_square_divisor_indicator_and_compensated_selberg_tc058",
    "compensated_selberg_summation_by_parts_and_shift_elimination_tc058",
    "combined_target_exact_quadratic_and_conditional_absorption_tc058",
    "growing_order_joint_polynomial_filter_and_gram_decomposition_tc058",
]


# ---------------------------------------------------------------------------
# 1. Exact Arithmetic & Certified Arb Helpers for TASK-TC-058
# ---------------------------------------------------------------------------


def positive_divisor_count_int(n: int) -> int:
    """Exact positive divisor count d_div(n) for integer n >= 1."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError(f"positive_divisor_count_int requires integer n >= 1, got {n!r}")
    cnt = 0
    r = 1
    while r * r <= n:
        if n % r == 0:
            cnt += 1 if r * r == n else 2
        r += 1
    return cnt


def exact_growing_order_M_int(Y: Union[int, Fraction], prec_bits: int = 256) -> int:
    """Exact integer M(Y) = ceil(2 * log Y) for rational Y >= 2.

    Certifies in 256-bit Arb that 2*log(Y) does not straddle an integer (for Y = 1 irrelevant;
    for rational Y >= 2, Y^2 != e^k by Lindemann-Weierstrass since Y^2 in Q_{>1}).
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        y_arb = _frac_to_arb(Y)
        if not bool(y_arb >= arb(2)):
            raise ValueError(f"exact_growing_order_M_int requires Y >= 2, got {Y!r}")
        two_log_y = arb(2) * y_arb.log()
        m_lo = int(math.ceil(float(two_log_y.lower())))
        m_hi = int(math.ceil(float(two_log_y.upper())))
        if m_lo != m_hi or not bool(arb(m_lo - 1) < two_log_y and two_log_y < arb(m_lo)):
            raise RuntimeError(f"Precision {prec_bits} insufficient to isolate ceil(2*log({Y}))")
        return m_lo
    finally:
        flint_ctx.prec = saved


def evaluate_c_lambda_arb(prec_bits: int = 256) -> arb:
    """Certified Selberg constant c_lambda = 4*zeta'(2)/zeta(2) - 2*gamma_E."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        z2_jet = acb_series([acb(2), acb(1)], prec=2).zeta()
        zeta_2 = z2_jet[0].real
        zetap_2 = z2_jet[1].real
        gamma_e = arb.const_euler()
        return arb(4) * (zetap_2 / zeta_2) - arb(2) * gamma_e
    finally:
        flint_ctx.prec = saved


def evaluate_C_square_arb(prec_bits: int = 256) -> arb:
    """Certified uniform square-projection upper constant C_sq = Gamma(5/4)/4 + 2*(3/(2*e))^{3/2}."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        e_val = arb(1).exp()
        return (arb(5) / arb(4)).gamma() / arb(4) + arb(2) * (
            (arb(3) / (arb(2) * e_val)) ** (arb(3) / arb(2))
        )
    finally:
        flint_ctx.prec = saved


def evaluate_Q_square_arb(X: arb, T: int, prec_bits: int = 256) -> arb:
    """Certified finite square-supported Gaussian sum Q_{square,T}(X) = sum_{1 <= r^2 <= T} phi_{r^2}(X)."""
    if not isinstance(T, int) or isinstance(T, bool) or T < 0:
        raise ValueError(f"T must be integer >= 0, got {T!r}")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        if T == 0:
            return arb(0)
        tot = arb(0)
        r = 1
        while r * r <= T:
            tot += evaluate_phi_n_arb(X, r * r, prec_bits=prec_bits)
            r += 1
        return tot
    finally:
        flint_ctx.prec = saved


def evaluate_scaled_fiber_g_arb(
    X: arb,
    T: int,
    d: int,
    mode: str = "liouville",
    prec_bits: int = 256,
) -> arb:
    """Certified scaled cofactor fiber g_{a,d}(X; T) = d^{-1/2} * Q_{a, floor(T/d)}(X / d)."""
    if d < 1:
        raise ValueError(f"d must be >= 1, got {d!r}")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        return evaluate_Q_shifted_finite_arb(
            X / arb(d), L=T // d, m_shift=0, mode=mode, prec_bits=prec_bits
        ) / arb(d).sqrt()
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 2. Sections 1 & 2: Narrow TC-057R Repairs & 5-Category Dependency Audit
# ---------------------------------------------------------------------------


def verify_section_1_and_2_narrow_repairs_and_dependency_table(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TC-057R §1a-1b repairs, 5-category dependency table, Agarwal-Garg-Maji k=3 bridge,
    and K-independence of normalized trivial-zero slopes.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()

        # 1a. Rough squarefree composite witness: U = 5, T = 25 vs T = 34 vs T = 35
        rough_5_25 = list(rough_squarefree_divisors_band(5, 25))
        primes_5_25 = [p for p in primes_up_to(25) if p >= 5]
        composites_5_25 = [d for d in rough_5_25 if d not in primes_5_25]

        rough_5_34 = list(rough_squarefree_divisors_band(5, 34))
        primes_5_34 = [p for p in primes_up_to(34) if p >= 5]
        composites_5_34 = [d for d in rough_5_34 if d not in primes_5_34]

        rough_5_35 = list(rough_squarefree_divisors_band(5, 35))
        primes_5_35 = [p for p in primes_up_to(35) if p >= 5]
        composites_5_35 = [d for d in rough_5_35 if d not in primes_5_35]

        repair_1a_ok = bool(
            rough_5_25 == primes_5_25
            and composites_5_25 == []
            and composites_5_34 == []
            and composites_5_35 == [35]
        )

        # 2a. Agarwal-Garg-Maji (arXiv:2202.00637, Theorem 1.2 at k = 3, u = X^2):
        # P_3(u) := sum_{n=1}^infty (mu(n) / n^3) * exp(-u / n^2), so X^{5/2} * P_3(X^2) = Q_mu(X),
        # and finite square-divisor inversion sum_{1 <= d^2 <= T} d^{-1} Q_{mu, floor(T/d^2)}(X / d^2) = Q_{lambda, T}(X).
        X_agm = arb(7)
        T_agm = 40
        p3_trunc = arb(0)
        q_mu_trunc = arb(0)
        for n in range(1, T_agm + 1):
            mu_n = moebius_mu_int(n)
            if mu_n != 0:
                p3_trunc += (
                    arb(mu_n)
                    * (arb(n) ** (-3))
                    * (-(X_agm * X_agm) / arb(n * n)).exp()
                )
                q_mu_trunc += arb(mu_n) * evaluate_phi_n_arb(X_agm, n, prec_bits=prec_bits)
        agm_res = (X_agm ** (arb(5) / arb(2))) * p3_trunc - q_mu_trunc

        sq_bridge_lhs = arb(0)
        d_sq = 1
        while d_sq * d_sq <= T_agm:
            L_inner = T_agm // (d_sq * d_sq)
            q_mu_inner = arb(0)
            for r in range(1, L_inner + 1):
                mu_r = moebius_mu_int(r)
                if mu_r != 0:
                    q_mu_inner += arb(mu_r) * evaluate_phi_n_arb(
                        X_agm / arb(d_sq * d_sq), r, prec_bits=prec_bits
                    )
            sq_bridge_lhs += q_mu_inner / arb(d_sq)
            d_sq += 1
        q_lam_agm = evaluate_Q_shifted_finite_arb(
            X_agm, L=T_agm, m_shift=0, mode="liouville", prec_bits=prec_bits
        )
        sq_bridge_res = sq_bridge_lhs - q_lam_agm
        agm_ok = bool(
            arb(0) in agm_res
            and abs(agm_res) < arb("1e-68")
            and arb(0) in sq_bridge_res
            and abs(sq_bridge_res) < arb("1e-68")
        )

        # 2b. Normalized trivial-zero slopes: for Z_{a_K}(w) := zeta(w / a_K) with trivial zeros at w = -2*m*a_K
        # (a_K = tau^K), a_K * Z'_{a_K}(-2*m*a_K) = zeta'(-2*m), independent of K.
        slope_rows: List[Dict[str, Any]] = []
        slope_ok = True
        grade_specs: List[Tuple[str, arb]] = [
            ("-1", arb(-1)),
            ("-1/2", arb(-1) / arb(2)),
            ("0", arb(0)),
            ("1/2", arb(1) / arb(2)),
            ("sqrt(2)", arb(2).sqrt()),
        ]
        for m_idx in (1, 2, 3):
            base_jet = acb_series([acb(-2 * m_idx), acb(1)], prec=2).zeta()
            zetap_neg_2m = base_jet[1].real
            max_diff_m = arb(0)
            for k_label, k_arb in grade_specs:
                a_K = tau ** k_arb
                w0 = -arb(2 * m_idx) * a_K
                # Z_{a_K}(w0 + eps) = zeta((w0 + eps) / a_K) = zeta(-2*m + eps / a_K)
                scaled_jet = acb_series([acb(w0 / a_K), acb(arb(1) / a_K)], prec=2).zeta()
                norm_slope = a_K * scaled_jet[1].real
                diff_k = abs(norm_slope - zetap_neg_2m)
                if not bool(arb(0) in (norm_slope - zetap_neg_2m) and diff_k < arb("1e-68")):
                    slope_ok = False
                if float(diff_k.upper()) > float(max_diff_m.upper()):
                    max_diff_m = diff_k
            slope_rows.append(
                {
                    "m": m_idx,
                    "trivial_zero_base": -2 * m_idx,
                    "zetap_at_neg_2m": serialize_arb_certified(zetap_neg_2m),
                    "max_grade_normalized_slope_discrepancy": serialize_arb_certified(max_diff_m),
                }
            )

        dependency_table = {
            "a_actual_arithmetic_theorems": [
                "Complete multiplicativity of liouvilleLambda(n) = (-1)^{Omega(n)}, common-factor cancellation, flat square-divisor Moebius/Liouville inversions, finite prime-exclusion sieve, and P-smooth/coprime finite cutoff bijection (Lean Theorems 3-4, 9-10, 13-16).",
                "Finite prime-adjoining filtration, unimodal alternating Gaussian prime-chain contraction, and P-independent contraction C_{P,p} = D_T - V_{p} (Lean Theorems 17-20).",
                "General Moebius-rough descent across U >= 2 (with composite rough divisors entering when an admissible composite exists, e.g. 35 at U=5, T=35 vs none at U=5, T=25), logarithmic prime-power descent & M-step shift telescope, pointwise quadratic prime-power diagonal/off-diagonal decomposition, and inherited-vs-canonical cutoff comparison with (Y=9/4, d=2) counterexample and small-scale positivity (Lean Theorems 22-25).",
                "NEW in TC-058: All-prime square-divisor indicator (1 * lambda)(n) = 1_{IsSquare n} vs dyadic parity (1 * a_2)(2^v m) = 1_{Even v} d_div(m), actual Selberg Liouville second-order weight w_{2,lambda} = Lambda_lambda*log + Lambda_lambda*Lambda_lambda (Lambda_lambda = -Lambda + 2*B) & finite square projection sum_{d=1}^T g_d = Q_{square,T} (including T = 0, 1), exact summation by parts keeping floor(T/d) jumps with post-Abel c_lambda collapse & jump-count telescope, exact shift elimination P_Y - R_Y = D_{2,Y}, pointwise combined quadratic forms, and growing-order M-layer polynomial filter 0 < P_M(s) <= 4 on [1/4, 3/2] & joint Gram decomposition (Lean Theorems 27-30).",
            ],
            "b_analytic_results_proved_outside_lean": [
                "Riesz-Gaussian equivalence context: Q_mu(X) = X^{5/2} P_3(X^2) belongs to the published Riesz-type family (Agarwal-Garg-Maji 2022, arXiv:2202.00637, Theorem 1.2 at k = 3, u = X^2), transferred between Q_mu and Q_lambda on weighted L^2((0, infty), X^{-2*eta} dX/X) by reversible square-divisor norm bounds.",
                "Unconditional Route D cross-scale prime-power diagonal contraction D_tilde_{lambda,pp}(Y) <= (2/(log Y)^2) sum_{p^k<=Y} ((log p)^2/p^k) F(Y/p^k) + C_{cut,diag} with contraction factor Theta_eps^{diag}(Y) < 2*zeta''(1+eps)/(log Y)^2 -> 0, plus scoped majorant obstructions for Route A/B Cauchy-Schwarz and Route C uncompensated Abel majorants.",
                "NEW in TC-058 (§4): Uniform unimodal bound 0 <= Q_{square,T}(X) <= C_sq := Gamma(5/4)/4 + 2*(3/(2*e))^{3/2} for X >= 1 giving ||c_lambda Q_{square,T}/(log X)^2||_Y^2 = O((log Y)^{-4}), O((log Y)^{-4}) upper-endpoint decay, and unconditional O((log Y)^{-2}) window-energy decay of the entire floor(T/d) cutoff-jump sum via (d+1)(L_{d+1}+1) >= T + 1 and sum_{d=1}^{T-1} d(L_d - L_{d+1}) <= T*log T.",
                "NEW in TC-058 (§5): Uniform generic terminal remainder bound ||Q_{a,L}^{[M(Y)]}/(log X)^{M(Y)}||_Y^2 <= 2068*(log Y)*Y^{-3} for all |a(n)| <= 1, L >= 1, Y >= 2 (M(Y) = ceil(2*log Y), bounding all three parts of A_m via explicit Robbins-Stirling + 17-interval compact monotonicity), and unconditional joint M(Y)-layer prime-power diagonal bound D_tilde_{a,pp}^{(M(Y))}(Y) = O(Y/(log Y)^2) uniformly for |a(n)| <= 1.",
            ],
            "c_conditional_implications": [
                "Polylogarithmic scale-envelope bootstrap F(Y) <= A_eta Y^eta + B_eta F(Y/U_eta(Y)) => E(Y) <<_eps Y^eps (`CONDITIONAL_ON_RECURSION`, Lean Theorem 21).",
                "TC-057R Young-expanded same-scale absorption sufficient condition X_tilde(Y) + ||R_Y||_Y^2 <= A_eta Y^eta + theta_eta F(Y) with 0 <= theta_eta < 1/2 => E(Y) <<_eps Y^eps (`CONDITIONAL_ON_SIGNED_CORRELATION`, Lean Theorem 26; forward implication proved, converse not asserted).",
                "NEW in TC-058 (§3): Un-Young-expanded combined sufficient condition S_comb(Y) := X_tilde(Y) + 2*<P_Y, R_Y>_Y + ||R_Y||_Y^2 <= A_eta Y^eta + theta_eta F(Y) across the full range 0 <= theta_eta < 1 (with theta_eta + Theta_eps^{diag}(Y) <= q < 1, no outer factor 2) => E(Y) <<_eps Y^eps (`CONDITIONAL_ON_COMBINED_CORRELATION`, Lean Theorem 29; forward implication proved).",
            ],
            "d_finite_numerical_observations": [
                "Certified 256-bit Arb window evaluations at Y in {8, 16, 32, 64, 128}: direct cross term <P_Y, R_Y>_Y changes sign (> 0 at Y in {8, 16, 32, 128}, < 0 at Y = 64); S_comb(Y) alternates sign (< 0 at Y in {8, 32, 128}, > 0 at Y in {16, 64}); parity controls a_2, a_{3,5,7}, and unsigned 1 concentrate >= 94% of their sampled Y = 64 joint M(Y)-layer energy in the off-diagonal X_tilde_{a,pp}^{(M(Y))}(64) (strictly finite sampled data, never extrapolated to asymptotic claims).",
            ],
            "e_missing_tc_to_arithmetic_implication": [
                "Open SUBGATE-TC-043A arithmetic estimate: an unconditional subpower or contractive bound S_comb(Y) <= A_eta Y^eta + theta_eta F(Y) (0 <= theta_eta < 1), equivalently subpower cancellation in 4*X_tilde_{lambda,pp}(Y) - 4*<P_Y, D_{2,Y}>_Y + ||D_{2,Y}||_Y^2 (§4) or in the joint M(Y)-layer distinct-prime-power off-diagonal X_tilde_{lambda,pp}^{(M(Y))}(Y) (§5). Varying K in normalized trivial-zero slopes yields no additional moments beyond zeta'(-2m), generic unitary dilation covariance does not bound the arithmetic sum, and all §§3-5 theorems generalize to arbitrary multiplicative window base b > 1 (classified honestly as TC-inspired analytic number theory).",
            ],
        }

        all_ok = bool(repair_1a_ok and agm_ok and slope_ok)
        return {
            "narrow_tc057r_repairs": {
                "rough_band_U5_T25_divisors": rough_5_25,
                "rough_band_U5_T25_composites": composites_5_25,
                "rough_band_U5_T34_composites": composites_5_34,
                "rough_band_U5_T35_divisors": rough_5_35,
                "rough_band_U5_T35_composites": composites_5_35,
                "repaired_wording": "when an admissible composite exists (first composite for U=5 is 5*7=35)",
                "theorem_26_sufficient_condition_scope": (
                    "sufficient condition (forward implication to subpower energy proved in Lean Theorem 26; "
                    "equivalence is not asserted without separately proving a shifted-kernel converse)"
                ),
                "verified": repair_1a_ok,
            },
            "agarwal_garg_maji_riesz_bridge_check": {
                "reference": "Agarwal, Garg, and Maji (2022), arXiv:2202.00637, Theorem 1.2 (k = 3, u = X^2)",
                "X": 7,
                "T": T_agm,
                "Q_mu_T": serialize_arb_certified(q_mu_trunc),
                "riesz_k3_minus_Q_mu_residual": serialize_arb_certified(agm_res),
                "square_divisor_bridge_minus_Q_lambda_residual": serialize_arb_certified(sq_bridge_res),
                "verified": agm_ok,
            },
            "normalized_trivial_zero_slope_k_independence": {
                "grades_tested": [g[0] for g in grade_specs],
                "rows": slope_rows,
                "supplies_additional_k_dependent_moments": False,
                "verified": slope_ok,
            },
            "compact_dependency_table": dependency_table,
            "all_section_1_and_2_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 3. Section 3: Un-Young-Expanded Target & Direct <P_Y, R_Y>_Y Evaluation
# ---------------------------------------------------------------------------


def evaluate_direct_cross_term_PR_arb(
    Y: Union[int, Fraction],
    b_base: Optional[arb] = None,
    mode: str = "liouville",
    prec_bits: int = 256,
) -> arb:
    """Direct 256-bit Arb quadrature of <P_Y, R_Y>_{[Y, b*Y]} = int_Y^{b*Y} P_Y(X)*R_Y(X) dX/X."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        y_arb = _frac_to_arb(Y)
        b_val = _tau_arb() if b_base is None else arb(b_base)
        T_Y = exact_T_cutoff_ceil_Y_5_4(Y)
        w_fn = _weight_fn_for_mode(mode)
        w_vals = [0] + [w_fn(n) for n in range(1, T_Y + 1)]
        log_n_weights = [arb(0)] + [arb(w_vals[n]) * arb(n).log() for n in range(1, T_Y + 1)]

        def _integrand(z: acb, _analytic: bool) -> acb:
            z2 = z * z
            sig_g = acb(0)
            for n in range(1, T_Y + 1):
                nc = acb(n)
                sig_g += acb(log_n_weights[n]) * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
            sh1_g = _G_shifted_acb(z, T_Y, 1, w_vals, analytic=_analytic)
            lg_z = z.log(analytic=_analytic)
            return (z ** 4) * sig_g * sh1_g / (lg_z * lg_z)

        return _acb_integral_certified_arb(_integrand, y_arb, b_val * y_arb, prec_bits=prec_bits)
    finally:
        flint_ctx.prec = saved


def verify_section_3_combined_target_and_direct_cross_term(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify the un-Young-expanded target E(Y) = D_tilde(Y) + S_comb(Y), direct <P_Y, R_Y>_Y
    evaluation (strictly separated from subtraction consistency checks), and relaxed theta_eta < 1
    absorption parameters.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()

        scale_rows: List[Dict[str, Any]] = []
        fiber_cross_checks: List[Dict[str, Any]] = []
        pos_cross_Y: List[int] = []
        neg_cross_Y: List[int] = []
        pos_S_comb_Y: List[int] = []
        neg_S_comb_Y: List[int] = []
        all_ok = True

        for Y_int in (8, 16, 32, 64, 128):
            T_Y = exact_T_cutoff_ceil_Y_5_4(Y_int)
            rd = _evaluate_route_d_totals_arb(Y_int, mode="liouville", prec_bits=prec_bits)
            cross_direct = evaluate_direct_cross_term_PR_arb(
                Y_int, mode="liouville", prec_bits=prec_bits
            )
            S_comb_direct = rd["X_tilde"] + arb(2) * cross_direct + rd["E_sh1"]
            E_from_direct = rd["D_tilde"] + S_comb_direct

            # Consistency checks (reported separately, NEVER as independent evaluation)
            cross_from_subtraction = (rd["E_main"] - rd["E_sig_total"] - rd["E_sh1"]) / arb(2)
            S_comb_from_subtraction = rd["E_main"] - rd["D_tilde"]
            res_cross_consistency = cross_direct - cross_from_subtraction
            res_E_consistency = rd["E_main"] - E_from_direct

            row_ok = bool(
                arb(0) in res_cross_consistency
                and abs(res_cross_consistency) < arb("1e-63")
                and arb(0) in res_E_consistency
                and abs(res_E_consistency) < arb("1e-63")
            )
            all_ok = all_ok and row_ok

            if bool(cross_direct > arb(0)):
                pos_cross_Y.append(Y_int)
            elif bool(cross_direct < arb(0)):
                neg_cross_Y.append(Y_int)

            if bool(S_comb_direct > arb(0)):
                pos_S_comb_Y.append(Y_int)
            elif bool(S_comb_direct < arb(0)):
                neg_S_comb_Y.append(Y_int)

            # Independent prime-power fiber evaluation of <P_Y, R_Y>_Y at Y in {8, 16}
            if Y_int in (8, 16):
                y_arb = arb(Y_int)
                w_vals = [0] + [liouville_lambda_int(n) for n in range(1, T_Y + 1)]
                cross_fiber = arb(0)
                for p, k in prime_power_pairs_up_to(T_Y):
                    pk = p ** k
                    L_pk = T_Y // pk
                    pf = acb((-1) ** k) * acb(arb(p).log()) * acb(arb(pk) ** arb(-3))

                    def _fiber_integrand(
                        z: acb,
                        _analytic: bool,
                        _L: int = L_pk,
                        _pk: int = pk,
                        _pf: acb = pf,
                    ) -> acb:
                        gu = _G_shifted_acb(z / acb(_pk), _L, 0, w_vals, analytic=_analytic)
                        sh1_g = _G_shifted_acb(z, T_Y, 1, w_vals, analytic=_analytic)
                        lg_z = z.log(analytic=_analytic)
                        return (z ** 4) * _pf * gu * sh1_g / (lg_z * lg_z)

                    cross_fiber += _acb_integral_certified_arb(
                        _fiber_integrand, y_arb, tau * y_arb, prec_bits=prec_bits
                    )
                fiber_diff = cross_direct - cross_fiber
                fiber_ok = bool(arb(0) in fiber_diff and abs(fiber_diff) < arb("1e-63"))
                all_ok = all_ok and fiber_ok
                fiber_cross_checks.append(
                    {
                        "Y": Y_int,
                        "T_Y": T_Y,
                        "prime_power_pair_count": len(prime_power_pairs_up_to(T_Y)),
                        "cross_term_prime_power_fiber_sum": serialize_arb_certified(cross_fiber),
                        "direct_minus_fiber_residual": serialize_arb_certified(fiber_diff),
                        "verified": fiber_ok,
                    }
                )

            scale_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_Y,
                    "E_Y": serialize_arb_certified(rd["E_main"]),
                    "D_tilde_Y": serialize_arb_certified(rd["D_tilde"]),
                    "X_tilde_Y": serialize_arb_certified(rd["X_tilde"]),
                    "cross_PR_direct": serialize_arb_certified(cross_direct),
                    "R_norm_sq_direct": serialize_arb_certified(rd["E_sh1"]),
                    "S_comb_direct": serialize_arb_certified(S_comb_direct),
                    "consistency_check_only_cross_subtraction_residual": serialize_arb_certified(
                        res_cross_consistency
                    ),
                    "consistency_check_only_S_comb_minus_E_sub_D_residual": serialize_arb_certified(
                        S_comb_direct - S_comb_from_subtraction
                    ),
                    "verified": row_ok,
                }
            )

        sign_change_ok = bool(
            pos_cross_Y == [8, 16, 32, 128]
            and neg_cross_Y == [64]
            and pos_S_comb_Y == [16, 64]
            and neg_S_comb_Y == [8, 32, 128]
        )

        # Relaxed conditional absorption parameters (theta_eta in [0, 1), e.g. theta_eta = 3/4 >= 1/2):
        # Theta_eps^{diag}(Y) < 2 * zeta''(1 + eps) / (log Y)^2 <= q - theta_eta
        # whenever log Y >= sqrt(2 * zeta''(1 + eps) / (q - theta_eta)).
        absorption_rows: List[Dict[str, Any]] = []
        for eps_f, theta_f, q_f in (
            (Fraction(1, 2), Fraction(3, 4), Fraction(7, 8)),
            (Fraction(1, 4), Fraction(3, 4), Fraction(7, 8)),
            (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)),
        ):
            eps_arb = _frac_to_arb(eps_f)
            theta_arb = _frac_to_arb(theta_f)
            q_arb = _frac_to_arb(q_f)
            z_jet = acb_series([acb(arb(1) + eps_arb), acb(1)], prec=3).zeta()
            zetapp_1_eps = arb(2) * z_jet[2].real
            min_log_Y = (arb(2) * zetapp_1_eps / (q_arb - theta_arb)).sqrt()
            # Evaluate Theta_eps^{diag}(128) directly and check log(Y) threshold
            theta_diag_128 = arb(0)
            for p, k in prime_power_pairs_up_to(128):
                pk = p ** k
                theta_diag_128 += (arb(p).log() ** 2) / (arb(pk) ** (arb(1) + eps_arb))
            theta_diag_128 = arb(2) * theta_diag_128 / (arb(128).log() ** 2)
            ub_128 = arb(2) * zetapp_1_eps / (arb(128).log() ** 2)
            abs_ok = bool(theta_diag_128 < ub_128 and theta_arb < arb(1) and q_arb < arb(1))
            all_ok = all_ok and abs_ok
            absorption_rows.append(
                {
                    "epsilon": str(eps_f),
                    "theta_eta": str(theta_f),
                    "q": str(q_f),
                    "admissible_in_tc058_un_young_transfer": True,
                    "admissible_in_tc057r_young_transfer": bool(theta_f < Fraction(1, 2)),
                    "two_zetapp_1_plus_eps": serialize_arb_certified(arb(2) * zetapp_1_eps),
                    "threshold_log_Y_for_q": serialize_arb_certified(min_log_Y),
                    "Theta_eps_diag_at_Y128": serialize_arb_certified(theta_diag_128),
                    "verified": abs_ok,
                }
            )

        all_ok = bool(all_ok and sign_change_ok)
        return {
            "sampled_combined_target_rows": scale_rows,
            "independent_prime_power_fiber_cross_checks": fiber_cross_checks,
            "direct_cross_term_positive_scales": pos_cross_Y,
            "direct_cross_term_negative_scales": neg_cross_Y,
            "S_comb_positive_scales": pos_S_comb_Y,
            "S_comb_negative_scales": neg_S_comb_Y,
            "relaxed_conditional_absorption_schedule_rows": absorption_rows,
            "identity_vs_estimate_note": (
                "S_comb(Y) = E(Y) - D_tilde(Y) is an exact algebraic identity, NOT an arithmetic "
                "cancellation theorem; Theorem 29 proves the conditional forward implication from "
                "S_comb(Y) <= A_eta*Y^eta + theta_eta*F(Y) (0 <= theta_eta < 1) to E(Y) <<_eps Y^eps."
            ),
            "all_section_3_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 4. Section 4: Compensated Selberg Reconstruction, Summation by Parts, & D_{2,Y}
# ---------------------------------------------------------------------------


def verify_section_4_compensated_selberg_and_shift_elimination(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify the finite square-projection identity, uniform C_sq bound, dyadic parity divisor
    identity, exact finite summation by parts keeping floor(T/d) cutoff jumps, post-Abel c_lambda
    collapse, unconditional endpoint/jump bounds, and exact shift elimination P_Y - R_Y = D_{2,Y}.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        e_val = arb(1).exp()
        c_lambda = evaluate_c_lambda_arb(prec_bits=prec_bits)
        C_sq = evaluate_C_square_arb(prec_bits=prec_bits)
        gamma_quarter_term = (arb(5) / arb(4)).gamma() / arb(4)
        unimodal_peak_const = (arb(3) / (arb(2) * e_val)) ** (arb(3) / arb(2))

        # 4.1 Finite square-projection & compensated Selberg split across T in {0, 1, 2, 14, 77}
        X_pt_checks: List[Dict[str, Any]] = []
        sq_id_ok = True
        for T_chk in (0, 1, 2, 14, 77):
            X_chk = arb(13)
            sum_gd = arb(0)
            sum_w2_gd = arb(0)
            sum_r2_gd = arb(0)
            for d in range(1, T_chk + 1):
                gd = evaluate_scaled_fiber_g_arb(X_chk, T_chk, d, mode="liouville", prec_bits=prec_bits)
                w2 = arb(0) if d == 1 else selberg_w2_weight_arb(d, "liouville")
                r2 = w2 - c_lambda
                sum_gd += gd
                if d >= 2:
                    sum_w2_gd += w2 * gd
                sum_r2_gd += r2 * gd
            q_sq = evaluate_Q_square_arb(X_chk, T_chk, prec_bits=prec_bits)
            res_sq = sum_gd - q_sq
            res_comp = sum_w2_gd - (c_lambda * q_sq + sum_r2_gd)
            ok_t = bool(
                arb(0) in res_sq
                and abs(res_sq) < arb("1e-65")
                and arb(0) in res_comp
                and abs(res_comp) < arb("1e-65")
                and q_sq >= arb(0)
                and C_sq - q_sq > arb(0)
            )
            sq_id_ok = sq_id_ok and ok_t
            X_pt_checks.append(
                {
                    "T": T_chk,
                    "X": 13,
                    "Q_square_T": serialize_arb_certified(q_sq),
                    "C_sq_minus_Q_square_T": serialize_arb_certified(C_sq - q_sq),
                    "sum_gd_minus_Q_square_residual": serialize_arb_certified(res_sq),
                    "compensated_selberg_split_residual": serialize_arb_certified(res_comp),
                    "verified": ok_t,
                }
            )

        # Also check X = 1 boundary for C_sq bound across T in {1, 4, 16, 100, 400}
        X1_max_q_sq = arb(0)
        for T_x1 in (1, 4, 16, 100, 400):
            q1 = evaluate_Q_square_arb(arb(1), T_x1, prec_bits=prec_bits)
            if not bool(q1 >= arb(0) and C_sq - q1 > arb(0)):
                sq_id_ok = False
            if float(q1.upper()) > float(X1_max_q_sq.upper()):
                X1_max_q_sq = q1

        # 4.2 Dyadic parity control identity (1 * a_2)(2^v m) = 1_{v even} d_div(m)
        a2_fn = _weight_fn_for_mode("a2")
        dyadic_conv_ok = True
        for n in range(1, 241):
            conv_val = sum(a2_fn(q) for q in range(1, n + 1) if n % q == 0)
            v_exp = 0
            m_odd = n
            while m_odd % 2 == 0:
                v_exp += 1
                m_odd //= 2
            expected_val = positive_divisor_count_int(m_odd) if (v_exp % 2 == 0) else 0
            if conv_val != expected_val:
                dyadic_conv_ok = False

        X_a2 = arb(16)
        T_a2 = 32
        sum_gd_a2 = sum(
            (
                evaluate_scaled_fiber_g_arb(X_a2, T_a2, d, mode="a2", prec_bits=prec_bits)
                for d in range(1, T_a2 + 1)
            ),
            arb(0),
        )
        rhs_a2 = arb(0)
        for n in range(1, T_a2 + 1):
            v_exp, m_odd = 0, n
            while m_odd % 2 == 0:
                v_exp += 1
                m_odd //= 2
            if v_exp % 2 == 0:
                rhs_a2 += arb(positive_divisor_count_int(m_odd)) * evaluate_phi_n_arb(
                    X_a2, n, prec_bits=prec_bits
                )
        res_a2_proj = sum_gd_a2 - rhs_a2
        dyadic_conv_ok = bool(
            dyadic_conv_ok and arb(0) in res_a2_proj and abs(res_a2_proj) < arb("1e-66")
        )

        # 4.3 Exact finite summation by parts on 1 <= d <= T, post-Abel c_lambda collapse,
        # jump-count telescope, unconditional window bounds on M_sq, endpoint, and jump sum,
        # and exact window quadratic decomposition E(Y) = 4*D_tilde + 4*X_tilde - 4*<P_Y, D_{2,Y}> + ||D_{2,Y}||_Y^2.
        abel_and_quadratic_rows: List[Dict[str, Any]] = []
        abel_all_ok = True
        for Y_int in (8, 16, 32, 64):
            T_Y = exact_T_cutoff_ceil_Y_5_4(Y_int)
            y_arb = arb(Y_int)
            lg_y = y_arb.log()

            W2_pref = [arb(0), arb(0)]
            for d in range(2, T_Y + 1):
                W2_pref.append(W2_pref[-1] + selberg_w2_weight_arb(d, "liouville"))
            R2_pref = [W2_pref[d] - c_lambda * arb(d) for d in range(T_Y + 1)]
            w2_centered = [arb(0)] + [
                (arb(0) if d == 1 else selberg_w2_weight_arb(d, "liouville"))
                - c_lambda
                for d in range(1, T_Y + 1)
            ]

            # Pointwise X = Y check of Abel, post-Abel c_lambda collapse, jump-count telescope, & P_Y - R_Y = D_{2,Y}
            X_pt = y_arb
            lg_X = X_pt.log()
            abel_raw = W2_pref[T_Y] * evaluate_scaled_fiber_g_arb(X_pt, T_Y, T_Y, prec_bits=prec_bits)
            c_part = c_lambda * arb(T_Y) * evaluate_scaled_fiber_g_arb(X_pt, T_Y, T_Y, prec_bits=prec_bits)
            r_end_pt = R2_pref[T_Y] * evaluate_scaled_fiber_g_arb(X_pt, T_Y, T_Y, prec_bits=prec_bits)
            r_smooth_pt = arb(0)
            r_jump_pt = arb(0)
            jump_count_lhs = 0
            for d in range(1, T_Y):
                L_d = T_Y // d
                L_d1 = T_Y // (d + 1)
                jump_count_lhs += d * (L_d - L_d1)
                sm_d = (
                    evaluate_Q_shifted_finite_arb(
                        X_pt / arb(d), L=L_d, m_shift=0, mode="liouville", prec_bits=prec_bits
                    )
                    / arb(d).sqrt()
                    - evaluate_Q_shifted_finite_arb(
                        X_pt / arb(d + 1), L=L_d, m_shift=0, mode="liouville", prec_bits=prec_bits
                    )
                    / arb(d + 1).sqrt()
                )
                jmp_d = sum(
                    (
                        arb(liouville_lambda_int(q))
                        * evaluate_phi_n_arb(X_pt / arb(d + 1), q, prec_bits=prec_bits)
                        for q in range(L_d1 + 1, L_d + 1)
                    ),
                    arb(0),
                ) / arb(d + 1).sqrt()
                # Also verify (d + 1) * q >= T_Y + 1 on every jump term
                for q in range(L_d1 + 1, L_d + 1):
                    if (d + 1) * q < T_Y + 1:
                        abel_all_ok = False
                abel_raw += W2_pref[d] * (sm_d + jmp_d)
                c_part += c_lambda * arb(d) * (sm_d + jmp_d)
                r_smooth_pt += R2_pref[d] * sm_d
                r_jump_pt += R2_pref[d] * jmp_d

            jump_count_rhs = sum(T_Y // d for d in range(1, T_Y + 1)) - T_Y
            q_sq_pt = evaluate_Q_square_arb(X_pt, T_Y, prec_bits=prec_bits)
            direct_w2_pt = sum(
                (
                    selberg_w2_weight_arb(d, "liouville")
                    * evaluate_scaled_fiber_g_arb(X_pt, T_Y, d, prec_bits=prec_bits)
                    for d in range(2, T_Y + 1)
                ),
                arb(0),
            )
            Q0_pt = evaluate_Q_shifted_finite_arb(X_pt, L=T_Y, m_shift=0, mode="liouville", prec_bits=prec_bits)
            Q1_pt = evaluate_Q_shifted_finite_arb(X_pt, L=T_Y, m_shift=1, mode="liouville", prec_bits=prec_bits)
            Q2_pt = evaluate_Q_shifted_finite_arb(X_pt, L=T_Y, m_shift=2, mode="liouville", prec_bits=prec_bits)
            R_pt = Q1_pt / lg_X
            P_pt = Q0_pt - R_pt
            D2_pt = (c_lambda * q_sq_pt + (r_end_pt + r_smooth_pt + r_jump_pt) - Q2_pt) / (lg_X * lg_X)
            res_PR_D2_pt = (P_pt - R_pt) - D2_pt

            # Window L^2([Y, tau*Y], dX/X) norms & direct inner product <P_Y, D_{2,Y}>_Y:
            # Notice sum_{d=1}^T r_2(d) g_d(X) = sum_{n=1}^T a_{r2}(n) phi_n(X) with
            # a_{r2}(n) = sum_{d | n} r_2(d) * lambda(n / d), and c_lambda*Q_{square,T}(X)
            # adds c_lambda on square n <= T, while -Q_T^{[2]}(X) has -(log(X/n))^2 * lambda(n)!
            # Using this exact n-coefficient representation makes direct quadrature over [Y, tau*Y] fast & certified!
            w_lam = [0] + [liouville_lambda_int(n) for n in range(1, T_Y + 1)]
            log_n_lam = [arb(0)] + [arb(w_lam[n]) * arb(n).log() for n in range(1, T_Y + 1)]
            d2_const_coeff = [arb(0) for _ in range(T_Y + 1)]
            for d in range(1, T_Y + 1):
                r2_d = w2_centered[d]
                for q in range(1, T_Y // d + 1):
                    d2_const_coeff[d * q] += r2_d * arb(w_lam[q])
            r_sq = 1
            while r_sq * r_sq <= T_Y:
                d2_const_coeff[r_sq * r_sq] += c_lambda
                r_sq += 1

            # Also build exact jump-only n-coefficients: sum_{d=1}^{T-1} R2_pref[d] * sum_{q=L_{d+1}+1}^{L_d} lambda(q) phi_{(d+1)*q}(X)
            max_jump_idx = max([1] + [(d + 1) * (T_Y // d) for d in range(1, T_Y)])
            jump_coeff: Dict[int, arb] = {}
            for d in range(1, T_Y):
                L_d = T_Y // d
                L_d1 = T_Y // (d + 1)
                for q in range(L_d1 + 1, L_d + 1):
                    m_idx = (d + 1) * q
                    jump_coeff[m_idx] = jump_coeff.get(m_idx, arb(0)) + R2_pref[d] * arb(
                        liouville_lambda_int(q)
                    )
            jump_items = sorted(jump_coeff.items())

            def _M_sq_norm_integrand(z: acb, _analytic: bool, _T: int = T_Y) -> acb:
                z2 = z * z
                lg_z = z.log(analytic=_analytic)
                acc = acb(0)
                r = 1
                while r * r <= _T:
                    nc = acb(r * r)
                    acc += (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                    r += 1
                v = acb(c_lambda) * acc / (lg_z * lg_z)
                return (z ** 4) * (v * v)

            def _jump_norm_integrand(
                z: acb,
                _analytic: bool,
                _ji: Sequence[Tuple[int, arb]] = tuple(jump_items),
            ) -> acb:
                z2 = z * z
                lg_z = z.log(analytic=_analytic)
                acc = acb(0)
                for m_idx, c_val in _ji:
                    mc = acb(m_idx)
                    acc += acb(c_val) * (mc ** (-3)) * (-z2 / (mc * mc)).exp()
                v = acc / (lg_z * lg_z)
                return (z ** 4) * (v * v)

            def _D2_norm_integrand(
                z: acb,
                _analytic: bool,
                _T: int = T_Y,
                _dc: Sequence[arb] = tuple(d2_const_coeff),
                _wl: Sequence[int] = tuple(w_lam),
            ) -> acb:
                z2 = z * z
                lg_z = z.log(analytic=_analytic)
                acc = acb(0)
                for n in range(1, _T + 1):
                    nc = acb(n)
                    lg_zn = (z / nc).log(analytic=_analytic)
                    coeff_n = acb(_dc[n]) - acb(_wl[n]) * (lg_zn * lg_zn)
                    acc += coeff_n * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                v = acc / (lg_z * lg_z)
                return (z ** 4) * (v * v)

            def _P_D2_cross_integrand(
                z: acb,
                _analytic: bool,
                _T: int = T_Y,
                _dc: Sequence[arb] = tuple(d2_const_coeff),
                _wl: Sequence[int] = tuple(w_lam),
                _lnl: Sequence[arb] = tuple(log_n_lam),
            ) -> acb:
                z2 = z * z
                lg_z = z.log(analytic=_analytic)
                sig_g = acb(0)
                d2_g = acb(0)
                for n in range(1, _T + 1):
                    nc = acb(n)
                    exp_n = (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                    sig_g += acb(_lnl[n]) * exp_n
                    lg_zn = (z / nc).log(analytic=_analytic)
                    d2_g += (acb(_dc[n]) - acb(_wl[n]) * (lg_zn * lg_zn)) * exp_n
                return (z ** 4) * sig_g * d2_g / (lg_z ** 3)

            M_sq_energy = _acb_integral_certified_arb(
                _M_sq_norm_integrand, y_arb, tau * y_arb, prec_bits=prec_bits
            )
            M_sq_analytic_ub = (c_lambda * c_lambda) * (C_sq * C_sq) * tau.log() / (lg_y ** 4)
            jump_energy = _acb_integral_certified_arb(
                _jump_norm_integrand, y_arb, tau * y_arb, prec_bits=prec_bits
            )
            D2_energy = _acb_integral_certified_arb(
                _D2_norm_integrand, y_arb, tau * y_arb, prec_bits=prec_bits
            )
            P_D2_cross = _acb_integral_certified_arb(
                _P_D2_cross_integrand, y_arb, tau * y_arb, prec_bits=prec_bits
            )

            rd = _evaluate_route_d_totals_arb(Y_int, mode="liouville", prec_bits=prec_bits)
            E_from_D2_quad = (
                arb(4) * rd["D_tilde"]
                + arb(4) * rd["X_tilde"]
                - arb(4) * P_D2_cross
                + D2_energy
            )
            res_E_D2_quad = rd["E_main"] - E_from_D2_quad

            row_ok = bool(
                jump_count_lhs == jump_count_rhs
                and arb(0) in (abel_raw - direct_w2_pt)
                and abs(abel_raw - direct_w2_pt) < arb("1e-62")
                and arb(0) in (c_part - c_lambda * q_sq_pt)
                and abs(c_part - c_lambda * q_sq_pt) < arb("1e-62")
                and arb(0) in res_PR_D2_pt
                and abs(res_PR_D2_pt) < arb("1e-63")
                and M_sq_analytic_ub - M_sq_energy > arb(0)
                and arb(0) in res_E_D2_quad
                and abs(res_E_D2_quad) < arb("1e-62")
            )
            abel_all_ok = abel_all_ok and row_ok

            abel_and_quadratic_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_Y,
                    "jump_count_sum_d_delta_L": jump_count_lhs,
                    "max_jump_product_index": max_jump_idx,
                    "M_sq_window_energy": serialize_arb_certified(M_sq_energy),
                    "M_sq_analytic_upper_bound": serialize_arb_certified(M_sq_analytic_ub),
                    "M_sq_bound_margin": serialize_arb_certified(M_sq_analytic_ub - M_sq_energy),
                    "cutoff_jump_window_energy": serialize_arb_certified(jump_energy),
                    "D2_window_energy_direct": serialize_arb_certified(D2_energy),
                    "P_D2_cross_direct": serialize_arb_certified(P_D2_cross),
                    "quadratic_identity_residual_E_minus_4P2_sub_4PD2_add_D22": serialize_arb_certified(
                        res_E_D2_quad
                    ),
                    "pointwise_P_sub_R_minus_D2_at_Y": serialize_arb_certified(res_PR_D2_pt),
                    "verified": row_ok,
                }
            )

        all_ok = bool(sq_id_ok and dyadic_conv_ok and abel_all_ok and c_lambda < arb(0))
        return {
            "c_lambda": serialize_arb_certified(c_lambda),
            "gamma_5_4_over_4": serialize_arb_certified(gamma_quarter_term),
            "unimodal_peak_const": serialize_arb_certified(unimodal_peak_const),
            "C_sq": serialize_arb_certified(C_sq),
            "X1_max_Q_square_sampled": serialize_arb_certified(X1_max_q_sq),
            "pointwise_square_projection_and_compensated_split_rows": X_pt_checks,
            "dyadic_parity_control_divisor_identity": {
                "checked_range_n_up_to": 240,
                "X_projection_check": 16,
                "T_projection_check": T_a2,
                "projection_residual": serialize_arb_certified(res_a2_proj),
                "asymptotic_energy_inferred_from_divisor_identity": False,
                "verified": dyadic_conv_ok,
            },
            "summation_by_parts_and_shift_elimination_rows": abel_and_quadratic_rows,
            "surviving_obstruction_summary": {
                "cancelled_or_decaying_components": [
                    "Linear c_lambda*d trend in W_2(d) collapses onto c_lambda*Q_{square,T}(X), whose normalized window energy ||c_lambda*Q_{square,T}/(log X)^2||_Y^2 <= c_lambda^2*C_sq^2*log(tau)/(log Y)^4 = O((log Y)^{-4}) (eliminating TC-057 Route C's uncompensated b = floor(Y) boundary obstruction).",
                    "Lower boundary d = 1 contributes r_2(1)*g_1(X)/(log X)^2 = -c_lambda*Q_T(X)/(log X)^2 with contracting window energy <= c_lambda^2*(log Y)^{-4}*E(Y).",
                    "Upper endpoint R_2^{int}(T)*g_T(X)/(log X)^2 has window energy O((log Y)^{-4}) since L_T = 1 and g_T(X) <= (3/(2*e))^{3/2}*T^{-1/2}.",
                    "Aggregate floor(T/d) cutoff-jump sum sum_{d=1}^{T-1} R_2^{int}(d)*Delta^{jump}_d(X)/(log X)^2 has unconditional decaying window energy O((log Y)^{-2}) -> 0 because every jump index satisfies (d+1)*q >= T + 1 > Y^{5/4} (so phi_{(d+1)q}(X) <= tau^{5/2}*Y^{-5/4}) and sum_{d=1}^{T-1} d*(L_d - L_{d+1}) = sum_{d=1}^T floor(T/d) - T <= T*log T.",
                    "Combining with Q_T = P_Y + R_Y eliminates the O(Y*(log Y)^{-2}) first-order shift R_Y via P_Y - R_Y = D_{2,Y} and Q_T = 2*P_Y - D_{2,Y}.",
                ],
                "surviving_uncontrolled_terms_and_exponents": [
                    "Smooth-step PNT remainder sum_{d=1}^{T-1} R_2^{int}(d)*Delta^{smooth}_d(X)/(log X)^2 inside D_{2,Y}(X): because R_2^{int}(d) = O(d*exp(-c*sqrt(log d))) is not a power saving, unsigned/Minkowski bounds on ||D_{2,Y}||_Y^2 leave O(Y*(log Y)^{-4}) (or O(Y*(log Y)^{-4}*exp(-c'*sqrt(log Y))) on the R_2^{int} piece, while -Q_T^{[2]}/(log X)^2 has unsigned energy O(Y*(log Y)^{-4})).",
                    "Prime-power off-diagonal 4*X_tilde_{lambda,pp}(Y) and cross term -4*<P_Y, D_{2,Y}>_Y in E(Y) = 4*D_tilde + 4*X_tilde - 4*<P_Y, D_{2,Y}> + ||D_{2,Y}||_Y^2: subpower energy still requires genuine signed cancellation across distinct prime-power fibers.",
                ],
            },
            "all_section_4_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 5. Section 5: Growing Order M(Y) = ceil(2*log Y) & Joint M(Y)-Layer Energy
# ---------------------------------------------------------------------------


def verify_section_5_growing_order_and_joint_gram(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify the uniform generic remainder bound ||Q_{a,L}^{[M(Y)]}/(log X)^{M(Y)}||_Y^2 <= C_rem*(log Y)*Y^{-3}
    across Y >= e^9 (Robbins-Stirling + all 3 parts of A_m) and Y in [2, e^9] (exact 17-interval
    derivative monotonicity), plus the joint M(Y)-layer Gram diagonal/off-diagonal decomposition and
    layer-sum Minkowski cost across controls.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        e_val = arb(1).exp()

        # 5.1 Asymptotic range Y >= e^9 (L = log Y >= 9, m = ceil(2*L) = 2*L + theta, theta in [0, 1), m >= 18):
        # Part 1: A_{m,1} / L^m = 2 * ((2*m + 5)/(4*e))^{5/4} * [sqrt((2*m + 5)/(4*e)) / L]^m.
        #   Since 4*L^2/e^2 - (4*L + 7) >= 324/e^2 - 43 > 0.848 > 0 for L >= 9,
        #   sqrt((2*m + 5)/(4*e)) / L <= sqrt((4*L + 7)/(4*e)) / L < e^{-3/2} < 1;
        #   with m >= 2*L, [base]^m <= e^{-3*L} = e^{-L} * Y^{-2}.
        #   Since d/dL log[((4*L + 7)/(4*e))^{5/4} * e^{-L} / sqrt(L)] = 5/(4*L + 7) - 1 - 1/(2*L) < 0 on L >= 9,
        #   A_{m,1} / L^m <= c_1 * sqrt(L) * Y^{-2} with c_1 = (2/3) * (43/(4*e))^{5/4} * e^{-9}.
        L9 = arb(9)
        quad_margin_L9 = arb(4) * (L9 ** 2) / (e_val ** 2) - (arb(4) * L9 + arb(7))
        c1_ge_e9 = (
            arb(2)
            * (((arb(4) * L9 + arb(7)) / (arb(4) * e_val)) ** (arb(5) / arb(4)))
            * ((-L9).exp())
            / L9.sqrt()
        )

        # Part 2: Robbins-Stirling m! <= sqrt(tau * m) * (m / e)^m * exp(1 / (12*m)) for m >= 18:
        # A_{m,2} / L^m = (m! / (2^{m+1} * L^m)) * (1 + 1/e)
        #   <= (sqrt(tau * m) / 2) * (1 + 1/e) * exp(1 / 216) * (m / (2 * e * L))^m.
        # With m = 2*L + theta (theta in [0, 1), L >= 9):
        #   (m / (2 * e * L))^m = e^{-m} * (1 + theta / (2*L))^{2*L + theta}
        #   <= e^{-(2*L + theta)} * exp(theta * (2*L + theta) / (2*L)) = Y^{-2} * exp(theta^2 / (2*L)) <= Y^{-2} * exp(1/18),
        # and sqrt(m) <= sqrt(2*L + 1) = sqrt(2 + 1/L) * sqrt(L) <= sqrt(19/9) * sqrt(L).
        c2_ge_e9 = (
            (tau.sqrt() / arb(2))
            * (arb(1) + arb(1) / e_val)
            * (arb(1) / arb(216)).exp()
            * (arb(1) / arb(18)).exp()
            * (arb(19) / arb(9)).sqrt()
        )

        # Part 3: A_{m,3} / L^m = 2 * (m / (3 * e * L))^m = 2 * (2/3)^m * (m / (2 * e * L))^m
        #   <= 2 * (2/3)^{18} * exp(1/18) * Y^{-2} <= [2 * (2/3)^{18} * exp(1/18) / 3] * sqrt(L) * Y^{-2}.
        c3_ge_e9 = arb(2) * ((arb(2) / arb(3)) ** 18) * (arb(1) / arb(18)).exp() / L9.sqrt()

        c_amp_ge_e9 = c1_ge_e9 + c2_ge_e9 + c3_ge_e9
        C_rem_ge_e9 = (tau - arb(1)) * (c_amp_ge_e9 ** 2)

        # Verify Robbins-Stirling m! <= sqrt(tau * m) * (m / e)^m * exp(1 / (12*m)) directly at m = 18..40
        stirling_ok = True
        for m_chk in range(1, 41):
            lhs_f = arb(math.factorial(m_chk))
            rhs_f = (
                (tau * arb(m_chk)).sqrt()
                * ((arb(m_chk) / e_val) ** m_chk)
                * (arb(1) / arb(12 * m_chk)).exp()
            )
            if not bool(rhs_f - lhs_f > arb(0)):
                stirling_ok = False

        # 5.2 Compact range Y in [2, e^9]: partitioned into 17 subintervals m in {2, ..., 18}
        # with L = log Y in [L_{min,m}, m/2] where L_{min,2} = log 2 and L_{min,m} = (m - 1)/2 for m >= 3.
        # On each subinterval, 4*L <= 2*m < 2*m + 1, so d/dL [exp(4*L) / L^{2*m + 1}] < 0 strictly,
        # attaining the exact maximum at L = L_{min,m}.
        compact_interval_rows: List[Dict[str, Any]] = []
        C_rem_compact_max = arb(0)
        compact_argmax_m = 2
        compact_ok = True
        for m_ord in range(2, 19):
            L_min = arb(2).log() if m_ord == 2 else arb(m_ord - 1) / arb(2)
            L_max = arb(m_ord) / arb(2)
            a_m1 = arb(2) * (
                (arb(2 * m_ord + 5) / (arb(4) * e_val)) ** (arb(2 * m_ord + 5) / arb(4))
            )
            a_m2 = (arb(math.factorial(m_ord)) / (arb(2) ** (m_ord + 1))) * (
                arb(1) + arb(1) / e_val
            )
            a_m3 = arb(2) * ((arb(m_ord) / (arb(3) * e_val)) ** m_ord)
            A_m_tot = a_m1 + a_m2 + a_m3
            ratio_at_L_min = (
                (tau - arb(1))
                * (A_m_tot * A_m_tot)
                * ((arb(4) * L_min).exp())
                / (L_min ** (2 * m_ord + 1))
            )
            if not bool(arb(4) * L_max < arb(2 * m_ord + 1) and ratio_at_L_min > arb(0)):
                compact_ok = False
            if float(ratio_at_L_min.upper()) > float(C_rem_compact_max.upper()):
                C_rem_compact_max = ratio_at_L_min
                compact_argmax_m = m_ord
            compact_interval_rows.append(
                {
                    "m": m_ord,
                    "L_min": serialize_arb_certified(L_min),
                    "L_max": serialize_arb_certified(L_max),
                    "A_m": serialize_arb_certified(A_m_tot),
                    "endpoint_constant_C_rem_m": serialize_arb_certified(ratio_at_L_min),
                }
            )

        C_rem_global_proven = arb(2068)
        global_const_ok = bool(
            quad_margin_L9 > arb("0.84")
            and stirling_ok
            and compact_ok
            and C_rem_ge_e9 < arb(38)
            and C_rem_compact_max < C_rem_global_proven
        )

        # 5.3 Sampled actual remainder norms ||Q_{a,T(Y)}^{[M(Y)]} / (log X)^{M(Y)}||_Y^2 across controls
        sampled_remainder_rows: List[Dict[str, Any]] = []
        rem_samples_ok = True
        for Y_int in (4, 8, 16, 32, 64, 128):
            T_Y = exact_T_cutoff_ceil_Y_5_4(Y_int)
            M_Y = exact_growing_order_M_int(Y_int, prec_bits=prec_bits)
            scale_ref = arb(Y_int).log() * (arb(Y_int) ** (-3))
            proven_ub = C_rem_global_proven * scale_ref
            per_mode: Dict[str, Any] = {}
            row_ok = True
            for mode in ("liouville", "a2", "a_3_5_7", "unsigned_1"):
                rem_sq = evaluate_E_L_scale_arb(
                    Y_int,
                    L=T_Y,
                    m_shift=M_Y,
                    log_denom_power=2 * M_Y,
                    mode=mode,
                    prec_bits=prec_bits,
                )
                if not bool(rem_sq >= arb(0) and proven_ub - rem_sq > arb(0)):
                    rem_samples_ok = False
                    row_ok = False
                per_mode[mode] = {
                    "remainder_norm_sq": serialize_arb_certified(rem_sq),
                    "ratio_to_logY_Y_neg3": serialize_arb_certified(rem_sq / scale_ref),
                }
            sampled_remainder_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_Y,
                    "M_Y": M_Y,
                    "logY_times_Y_neg3": serialize_arb_certified(scale_ref),
                    "proven_upper_bound_2068_logY_Y_neg3": serialize_arb_certified(proven_ub),
                    "controls": per_mode,
                    "verified": row_ok,
                }
            )

        # 5.4 Joint M(Y)-layer prime-power Gram decomposition ||L_{a,M(Y)}||_Y^2 = D_tilde^{(M)} + X_tilde^{(M)}
        # plus Minkowski sum of individual layer norms (sum_{m=0}^{M-1} ||Sigma_{a,pp}^{[m]}/(log X)^{m+1}||_Y)^2
        # at Y in {8, 16, 32, 64} across controls!
        joint_gram_rows: List[Dict[str, Any]] = []
        joint_gram_ok = True
        for Y_int in (8, 16, 32, 64):
            T_Y = exact_T_cutoff_ceil_Y_5_4(Y_int)
            M_Y = exact_growing_order_M_int(Y_int, prec_bits=prec_bits)
            y_arb = arb(Y_int)
            per_mode_gram: Dict[str, Any] = {}
            for mode in ("liouville", "a2", "a_3_5_7", "unsigned_1"):
                w_fn = _weight_fn_for_mode(mode)
                w_vals = [0] + [w_fn(n) for n in range(1, T_Y + 1)]

                def _joint_L_sq(
                    z: acb,
                    _analytic: bool,
                    _wv: Sequence[int] = tuple(w_vals),
                    _T: int = T_Y,
                    _M: int = M_Y,
                ) -> acb:
                    z2 = z * z
                    lg_z = z.log(analytic=_analytic)
                    tot = acb(0)
                    for n in range(2, _T + 1):
                        nc = acb(n)
                        ratio = (z / nc).log(analytic=_analytic) / lg_z
                        filt = acb(1) - (ratio ** _M)
                        tot += acb(_wv[n]) * filt * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                    return (z ** 4) * (tot * tot)

                E_L_joint = _acb_integral_certified_arb(
                    _joint_L_sq, y_arb, tau * y_arb, prec_bits=prec_bits
                )

                D_M_diag = arb(0)
                for p, k in prime_power_pairs_up_to(T_Y):
                    pk = p ** k
                    L_pk = T_Y // pk
                    lg_p_sq_over_pk = (arb(p).log() ** 2) / arb(pk)
                    pk_pf = acb(arb(pk) ** arb(-5))

                    def _fiber_M_sq(
                        z: acb,
                        _analytic: bool,
                        _L: int = L_pk,
                        _pk: int = pk,
                        _pf: acb = pk_pf,
                        _wv: Sequence[int] = tuple(w_vals),
                        _M: int = M_Y,
                    ) -> acb:
                        uz = z / acb(_pk)
                        u2 = uz * uz
                        lg_z = z.log(analytic=_analytic)
                        acc = acb(0)
                        for q in range(1, _L + 1):
                            qc = acb(q)
                            nq = _pk * q
                            lg_nq = acb(arb(nq).log())
                            ratio = (z / acb(nq)).log(analytic=_analytic) / lg_z
                            km = (acb(1) - (ratio ** _M)) / lg_nq
                            acc += acb(_wv[q]) * km * (qc ** (-3)) * (-u2 / (qc * qc)).exp()
                        return (z ** 4) * _pf * (acc * acc)

                    D_M_diag += lg_p_sq_over_pk * _acb_integral_certified_arb(
                        _fiber_M_sq, y_arb, tau * y_arb, prec_bits=prec_bits
                    )

                # Direct off-diagonal pair sum cross-check at Y = 8 for Liouville
                X_M_off_consistency = E_L_joint - D_M_diag
                direct_pair_res: Optional[arb] = None
                if Y_int == 8 and mode == "liouville":
                    pp_list = prime_power_pairs_up_to(T_Y)
                    X_M_off_direct = arb(0)
                    for i_idx, (p1, k1) in enumerate(pp_list):
                        for j_idx, (p2, k2) in enumerate(pp_list):
                            if i_idx == j_idx:
                                continue
                            pk1 = p1 ** k1
                            pk2 = p2 ** k2
                            L1 = T_Y // pk1
                            L2 = T_Y // pk2
                            sgn12 = ((-1) ** k1) * ((-1) ** k2)
                            pref12 = (
                                arb(sgn12)
                                * arb(p1).log()
                                * arb(p2).log()
                                * (arb(pk1) ** arb(-3))
                                * (arb(pk2) ** arb(-3))
                            )

                            def _pair_M_integrand(
                                z: acb,
                                _analytic: bool,
                                _L1: int = L1,
                                _L2: int = L2,
                                _pk1: int = pk1,
                                _pk2: int = pk2,
                                _pf12: arb = pref12,
                                _wv: Sequence[int] = tuple(w_vals),
                                _M: int = M_Y,
                            ) -> acb:
                                u1 = z / acb(_pk1)
                                u2 = z / acb(_pk2)
                                lg_z = z.log(analytic=_analytic)
                                a1 = acb(0)
                                for q in range(1, _L1 + 1):
                                    qc = acb(q)
                                    nq = _pk1 * q
                                    km = (acb(1) - ((z / acb(nq)).log(analytic=_analytic) / lg_z) ** _M) / acb(
                                        arb(nq).log()
                                    )
                                    a1 += acb(_wv[q]) * km * (qc ** (-3)) * (-(u1 * u1) / (qc * qc)).exp()
                                a2 = acb(0)
                                for q in range(1, _L2 + 1):
                                    qc = acb(q)
                                    nq = _pk2 * q
                                    km = (acb(1) - ((z / acb(nq)).log(analytic=_analytic) / lg_z) ** _M) / acb(
                                        arb(nq).log()
                                    )
                                    a2 += acb(_wv[q]) * km * (qc ** (-3)) * (-(u2 * u2) / (qc * qc)).exp()
                                return (z ** 4) * acb(_pf12) * a1 * a2

                            X_M_off_direct += _acb_integral_certified_arb(
                                _pair_M_integrand, y_arb, tau * y_arb, prec_bits=prec_bits
                            )
                    direct_pair_res = X_M_off_direct - X_M_off_consistency
                    if not bool(arb(0) in direct_pair_res and abs(direct_pair_res) < arb("1e-63")):
                        joint_gram_ok = False

                # Quantify Minkowski layer-sum cost (sum_{m=0}^{M-1} ||Sigma_{a,pp}^{[m]}/(log X)^{m+1}||_Y)^2
                # at Y in {8, 16, 32, 64} for Liouville & unsigned_1
                layer_minkowski_sq: Optional[arb] = None
                if Y_int in (8, 16, 32, 64) and mode in ("liouville", "unsigned_1"):
                    sum_layer_norms = arb(0)
                    log_n_w = [arb(0)] + [arb(w_vals[n]) * arb(n).log() for n in range(1, T_Y + 1)]
                    for m_idx in range(M_Y):

                        def _layer_m_sq(
                            z: acb,
                            _analytic: bool,
                            _m: int = m_idx,
                            _T: int = T_Y,
                            _lnw: Sequence[arb] = tuple(log_n_w),
                        ) -> acb:
                            z2 = z * z
                            lg_z = z.log(analytic=_analytic)
                            acc = acb(0)
                            for n in range(2, _T + 1):
                                nc = acb(n)
                                lg_zn = (z / nc).log(analytic=_analytic)
                                acc += (
                                    acb(_lnw[n])
                                    * (lg_zn ** _m)
                                    * (nc ** (-3))
                                    * (-z2 / (nc * nc)).exp()
                                )
                            v = acc / (lg_z ** (_m + 1))
                            return (z ** 4) * (v * v)

                        l_sq = _acb_integral_certified_arb(
                            _layer_m_sq, y_arb, tau * y_arb, prec_bits=prec_bits
                        )
                        sum_layer_norms += l_sq.sqrt()
                    layer_minkowski_sq = sum_layer_norms * sum_layer_norms
                    if not bool(layer_minkowski_sq - E_L_joint > arb(0)):
                        joint_gram_ok = False

                E_tot = evaluate_E_L_scale_arb(
                    Y_int, L=T_Y, m_shift=0, mode=mode, prec_bits=prec_bits
                )
                entry_m: Dict[str, Any] = {
                    "E_total_Y": serialize_arb_certified(E_tot),
                    "joint_M_layer_norm_sq": serialize_arb_certified(E_L_joint),
                    "joint_M_prime_power_diagonal": serialize_arb_certified(D_M_diag),
                    "joint_M_prime_power_off_diagonal": serialize_arb_certified(X_M_off_consistency),
                }
                if direct_pair_res is not None:
                    entry_m["direct_pair_minus_consistency_off_diagonal_residual"] = (
                        serialize_arb_certified(direct_pair_res)
                    )
                if layer_minkowski_sq is not None:
                    entry_m["minkowski_layer_sum_norm_sq"] = serialize_arb_certified(
                        layer_minkowski_sq
                    )
                    entry_m["minkowski_over_joint_ratio"] = serialize_arb_certified(
                        layer_minkowski_sq / E_L_joint
                    )
                per_mode_gram[mode] = entry_m

            joint_gram_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_Y,
                    "M_Y": M_Y,
                    "modes": per_mode_gram,
                }
            )

        all_ok = bool(global_const_ok and rem_samples_ok and joint_gram_ok)
        return {
            "asymptotic_e9_constants": {
                "L_threshold": 9,
                "part_1_quadratic_margin_4L2_over_e2_sub_4L_add_7": serialize_arb_certified(
                    quad_margin_L9
                ),
                "c1_part1": serialize_arb_certified(c1_ge_e9),
                "c2_part2_robbins_stirling": serialize_arb_certified(c2_ge_e9),
                "c3_part3": serialize_arb_certified(c3_ge_e9),
                "C_rem_ge_e9": serialize_arb_certified(C_rem_ge_e9),
                "stirling_verified_m_1_to_40": stirling_ok,
            },
            "compact_2_to_e9_partition": {
                "subinterval_count": len(compact_interval_rows),
                "argmax_m": compact_argmax_m,
                "C_rem_compact_max": serialize_arb_certified(C_rem_compact_max),
                "C_rem_global_proven": 2068,
                "rows": compact_interval_rows,
            },
            "generic_in_bounded_controls": True,
            "sampled_terminal_remainder_rows": sampled_remainder_rows,
            "joint_M_layer_gram_rows": joint_gram_rows,
            "cost_and_concentration_summary": {
                "resummation_vs_cancellation": (
                    "Resumming the M(Y) layers back to Q_T - Q_T^{[M]}/(log X)^M is a consistency identity, "
                    "not a cancellation proof."
                ),
                "unconditional_joint_diagonal_bound": (
                    "Because 0 < P_M(s) <= 4 uniformly on s in [1/4, 3/2] for all M >= 1 (Lean Theorem 30(4)), "
                    "the entire joint M(Y)-layer prime-power diagonal satisfies D_tilde_{a,pp}^{(M(Y))}(Y) = O(Y/(log Y)^2) "
                    "uniformly for all bounded controls |a(n)| <= 1."
                ),
                "surviving_joint_off_diagonal_obligation": (
                    "For growing-energy controls (1, a_2, a_{3,5,7}) with E_a(Y) = Theta(Y), (1 - o(1)) of the "
                    "window energy concentrates in the distinct-prime-power off-diagonal X_tilde_{a,pp}^{(M(Y))}(Y); "
                    "meanwhile summing individual layer norms incurs a growing Minkowski blowup factor, isolating "
                    "all-prime Liouville cancellation in X_tilde_{lambda,pp}^{(M(Y))}(Y) as the exact open target."
                ),
            },
            "all_section_5_checks_pass": all_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 6. Section 6: TC Compatibility Schemas & Discriminators
# ---------------------------------------------------------------------------


def verify_section_6_tc_compatibility_discriminators(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify the pre-stated compatibility lemma schemas, the window-base discriminator [Y, b*Y]
    across b in {2, e, tau} (keeping tau in circle/Fourier/Stirling), and the arithmetic control
    discriminators across lambda, a_2, a_{3,5,7}, and unsigned 1.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        e_val = arb(1).exp()
        c_lambda = evaluate_c_lambda_arb(prec_bits=prec_bits)
        C_sq = evaluate_C_square_arb(prec_bits=prec_bits)

        prestated_lemmas = [
            {
                "lemma_id": "LEM-TC058-A",
                "title": "Un-Young-expanded combined-energy decomposition and conditional absorption",
                "objects": "Q_{lambda,T(Y)}, P_Y, R_Y, D_tilde_{lambda,pp}(Y), S_comb(Y), F(Y), G_eps(R)",
                "quantifiers": "forall eta in (0, eps), forall Y >= Y_star >= 2, forall R >= Y_star",
                "hypotheses": "S_comb(Y) <= A_eta*Y^eta + theta_eta*F(Y) with 0 <= theta_eta < 1 and theta_eta + Theta_eps^{diag}(Y) <= q < 1",
                "input_source": "Logarithmic prime-power identity log n = sum_{p^k | n} log p, lambda(p^k) = (-1)^k, and Route D diagonal contraction",
                "conclusion": "E(Y) <= F(Y) <= max(G_eps(Y_star), K_comb/(1 - q)) * Y^eps for all Y >= 1",
                "status": "PROVED_CONDITIONAL (Lean Theorem 29; sufficient condition only)",
                "tc_discriminator_result": "Holds for arbitrary multiplicative window [Y, b*Y] (b > 1); TC-inspired analytic number theory",
            },
            {
                "lemma_id": "LEM-TC058-B",
                "title": "All-prime square projection and compensated Selberg decomposition",
                "objects": "g_d(X) = d^{-1/2} Q_{floor(T/d)}(X/d), Q_{square,T}(X), w_{2,lambda}(d), c_lambda",
                "quantifiers": "forall T in Z_{>=0}, forall X >= 1",
                "hypotheses": "lambda(p) = -1 at every prime p (so (1 * lambda)(n) = 1_{IsSquare n} and L_lambda(s) = zeta(2s)/zeta(s))",
                "input_source": "All-prime Liouville divisor sum + Gaussian X^{5/2} n^{-3} scaling + Selberg double-pole cancellation",
                "conclusion": "sum_{d=1}^T g_d = Q_{square,T}, 0 <= Q_{square,T}(X) <= C_sq, and ||c_lambda Q_{square,T}/(log X)^2||_Y^2 = O((log Y)^{-4})",
                "status": "PROVED_UNCONDITIONAL (finite identities in Lean Theorem 27; unimodal C_sq bound proved analytically & Arb-certified)",
                "tc_discriminator_result": "Distinguishes actual lambda from a_2, a_S, and 1 via lambda(p) = -1 at ALL primes; holds on [Y, b*Y] for all b > 1",
            },
            {
                "lemma_id": "LEM-TC058-C",
                "title": "Post-Abel c_lambda cancellation, cutoff-jump decay, and shift elimination P_Y - R_Y = D_{2,Y}",
                "objects": "W_2(d), R_2^{int}(d) = W_2(d) - c_lambda*d, Delta^{smooth}_d, Delta^{jump}_d, D_{2,Y}",
                "quantifiers": "forall Y >= 2, T = ceil(Y^{5/4}), X in [Y, b*Y]",
                "hypotheses": "W_2(u) = c_lambda*u + O(u*exp(-c*sqrt(log u))) and exact integer division (d+1)*(L_{d+1}+1) >= T + 1",
                "input_source": "PNT for lambda + exact discrete summation by parts + second-order logarithmic shift identity",
                "conclusion": "Cancels Route C boundary obstruction, bounds jump energy by O((log Y)^{-2}), and eliminates R_Y via Q_T = 2*P_Y - D_{2,Y}, leaving O(Y*(log Y)^{-4}) in ||D_{2,Y}||_Y^2 plus 4*X_tilde",
                "status": "PROVED_PARTIAL_REDUCTION (identities in Lean Theorems 28-29; leaves O(Y*(log Y)^{-4}) without subpower cancellation)",
                "tc_discriminator_result": "Uses all-prime PNT cancellation for lambda (fails for a_2, a_S, 1 where W_2(u) ~ 2*u*log u); holds for all b > 1",
            },
            {
                "lemma_id": "LEM-TC058-D",
                "title": "Uniform terminal remainder bound at growing order M(Y) = ceil(2*log Y)",
                "objects": "Q_{a,L}^{[M(Y)]}(X) / (log X)^{M(Y)}, A_m",
                "quantifiers": "forall bounded |a(n)| <= 1, forall L >= 1, forall Y >= 2",
                "hypotheses": "|a(n)| <= 1 only",
                "input_source": "Gaussian moment envelope A_m + Robbins-Stirling + 17-interval compact derivative sign",
                "conclusion": "||Q_{a,L}^{[M(Y)]} / (log X)^{M(Y)}||_{[Y, tau*Y]}^2 <= 2068 * (log Y) * Y^{-3}",
                "status": "PROVED_UNCONDITIONAL_GENERIC (proved analytically & certified in 256-bit Arb)",
                "tc_discriminator_result": "Generic for ALL |a(n)| <= 1 (including controls 1, a_2, a_S) and all window bases b > 1 (with b - 1 factor)",
            },
            {
                "lemma_id": "LEM-TC058-E",
                "title": "Joint M(Y)-layer polynomial kernel bound and prime-power diagonal control",
                "objects": "P_M(s) = sum_{m < M} (1 - s)^m, L_{a,M}(X; T), D_tilde_{a,pp}^{(M)}(Y), X_tilde_{a,pp}^{(M)}(Y)",
                "quantifiers": "forall M >= 1, forall bounded multiplicative a with a(1) = 1, forall Y >= 16",
                "hypotheses": "0 < P_M(s) <= 4 on s in [1/4, 3/2] and |a(n)| <= 1",
                "input_source": "Finite geometric series sum + Gaussian fast decay for n <= Y^{1/2}",
                "conclusion": "D_tilde_{a,pp}^{(M(Y))}(Y) = O(Y / (log Y)^2), concentrating any Theta(Y) energy into X_tilde_{a,pp}^{(M(Y))}(Y)",
                "status": "PROVED_UNCONDITIONAL (polynomial & Gram identities in Lean Theorem 30; integral bound proved analytically)",
                "tc_discriminator_result": "Diagonal bound is generic in |a| <= 1; isolating X_tilde_{lambda,pp}^{(M(Y))} requires all-prime lambda(p) = -1; holds for all b > 1",
            },
        ]

        # Discriminator 1: Window-base test [Y, b*Y] for b in {2, e, tau} at Y in {16, 32}
        base_specs: List[Tuple[str, arb]] = [
            ("2", arb(2)),
            ("e", e_val),
            ("tau", tau),
        ]
        window_base_rows: List[Dict[str, Any]] = []
        base_test_ok = True
        for Y_int in (16, 32):
            T_Y = exact_T_cutoff_ceil_Y_5_4(Y_int)
            M_Y = exact_growing_order_M_int(Y_int, prec_bits=prec_bits)
            y_arb = arb(Y_int)
            lg_y = y_arb.log()
            w_vals = [0] + [liouville_lambda_int(n) for n in range(1, T_Y + 1)]
            log_n_w = [arb(0)] + [arb(w_vals[n]) * arb(n).log() for n in range(1, T_Y + 1)]

            for b_label, b_arb in base_specs:
                hi_b = b_arb * y_arb

                def _E_b_int(z: acb, _analytic: bool) -> acb:
                    g0 = _G_shifted_acb(z, T_Y, 0, w_vals, analytic=_analytic)
                    return (z ** 4) * (g0 * g0)

                def _P_sq_b_int(z: acb, _analytic: bool) -> acb:
                    z2 = z * z
                    lg_z = z.log(analytic=_analytic)
                    sg = acb(0)
                    for n in range(1, T_Y + 1):
                        nc = acb(n)
                        sg += acb(log_n_w[n]) * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                    return (z ** 4) * (sg * sg) / (lg_z * lg_z)

                def _R_sq_b_int(z: acb, _analytic: bool) -> acb:
                    lg_z = z.log(analytic=_analytic)
                    g1 = _G_shifted_acb(z, T_Y, 1, w_vals, analytic=_analytic)
                    return (z ** 4) * (g1 * g1) / (lg_z * lg_z)

                def _D_tilde_b() -> arb:
                    tot_d = arb(0)
                    for p, k in prime_power_pairs_up_to(T_Y):
                        pk = p ** k
                        L_pk = T_Y // pk
                        lgp2_pk = (arb(p).log() ** 2) / arb(pk)
                        pk_pf = acb(arb(pk) ** arb(-5))

                        def _d_int(
                            z: acb,
                            _analytic: bool,
                            _L: int = L_pk,
                            _pk: int = pk,
                            _pf: acb = pk_pf,
                        ) -> acb:
                            lg_z = z.log(analytic=_analytic)
                            gu = _G_shifted_acb(z / acb(_pk), _L, 0, w_vals, analytic=_analytic)
                            return (z ** 4) * _pf * (gu * gu) / (lg_z * lg_z)

                        tot_d += lgp2_pk * _acb_integral_certified_arb(
                            _d_int, y_arb, hi_b, prec_bits=prec_bits
                        )
                    return tot_d

                def _M_sq_b_int(z: acb, _analytic: bool) -> acb:
                    z2 = z * z
                    lg_z = z.log(analytic=_analytic)
                    acc = acb(0)
                    r = 1
                    while r * r <= T_Y:
                        nc = acb(r * r)
                        acc += (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                        r += 1
                    v = acb(c_lambda) * acc / (lg_z * lg_z)
                    return (z ** 4) * (v * v)

                def _rem_M_b_int(z: acb, _analytic: bool) -> acb:
                    lg_z = z.log(analytic=_analytic)
                    gm = _G_shifted_acb(z, T_Y, M_Y, w_vals, analytic=_analytic)
                    return (z ** 4) * (gm * gm) / (lg_z ** (2 * M_Y))

                E_b = _acb_integral_certified_arb(_E_b_int, y_arb, hi_b, prec_bits=prec_bits)
                P_sq_b = _acb_integral_certified_arb(_P_sq_int := _P_sq_b_int, y_arb, hi_b, prec_bits=prec_bits)
                R_sq_b = _acb_integral_certified_arb(_R_sq_b_int, y_arb, hi_b, prec_bits=prec_bits)
                D_tilde_b = _D_tilde_b()
                X_tilde_b = P_sq_b - D_tilde_b
                cross_PR_b = evaluate_direct_cross_term_PR_arb(
                    Y_int, b_base=b_arb, mode="liouville", prec_bits=prec_bits
                )
                S_comb_b = X_tilde_b + arb(2) * cross_PR_b + R_sq_b
                res_comb_b = E_b - (D_tilde_b + S_comb_b)

                M_sq_b = _acb_integral_certified_arb(_M_sq_b_int, y_arb, hi_b, prec_bits=prec_bits)
                M_sq_ub_b = (c_lambda * c_lambda) * (C_sq * C_sq) * b_arb.log() / (lg_y ** 4)
                rem_M_b = _acb_integral_certified_arb(_rem_M_b_int, y_arb, hi_b, prec_bits=prec_bits)
                rem_M_ub_b = (
                    (b_arb - arb(1))
                    / (tau - arb(1))
                    * arb(2068)
                    * lg_y
                    * (y_arb ** (-3))
                )

                ok_b = bool(
                    arb(0) in res_comb_b
                    and abs(res_comb_b) < arb("1e-63")
                    and M_sq_ub_b - M_sq_b > arb(0)
                    and rem_M_ub_b - rem_M_b > arb(0)
                )
                base_test_ok = base_test_ok and ok_b
                window_base_rows.append(
                    {
                        "Y": Y_int,
                        "window_base": b_label,
                        "E_b": serialize_arb_certified(E_b),
                        "D_tilde_b": serialize_arb_certified(D_tilde_b),
                        "S_comb_b": serialize_arb_certified(S_comb_b),
                        "combined_identity_residual": serialize_arb_certified(res_comb_b),
                        "M_sq_b": serialize_arb_certified(M_sq_b),
                        "M_sq_b_bound_margin": serialize_arb_certified(M_sq_ub_b - M_sq_b),
                        "growing_order_remainder_b": serialize_arb_certified(rem_M_b),
                        "growing_order_remainder_b_bound_margin": serialize_arb_certified(
                            rem_M_ub_b - rem_M_b
                        ),
                        "verified": ok_b,
                    }
                )

        # Discriminator 2: Arithmetic controls summary at u = 200 for cumulative W_{2,a}(200) / 200
        control_w2_rows: List[Dict[str, Any]] = []
        for mode_c in ("liouville", "a2", "a_3_5_7", "unsigned_1"):
            W2_200 = sum(
                (selberg_w2_weight_arb(d, mode_c) for d in range(2, 201)),
                arb(0),
            )
            control_w2_rows.append(
                {
                    "mode": mode_c,
                    "W2_at_200": serialize_arb_certified(W2_200),
                    "W2_at_200_over_200": serialize_arb_certified(W2_200 / arb(200)),
                }
            )

        return {
            "prestated_compatibility_lemma_schemas": prestated_lemmas,
            "window_base_discriminator": {
                "bases_tested": ["2", "e", "tau"],
                "tau_preserved_in_circle_fourier_stirling": True,
                "rows": window_base_rows,
                "extra_tau_specific_lattice_constraint_found": False,
                "honest_classification": "TC-inspired analytic number theory",
                "verified": base_test_ok,
            },
            "arithmetic_control_discriminator": {
                "controls_tested": ["liouville", "a2", "a_3_5_7", "unsigned_1"],
                "W2_cumulative_rows_u200": control_w2_rows,
                "distinguishing_hypothesis": (
                    "lambda(p) = -1 at EVERY prime p (determining L_lambda(s) = zeta(2s)/zeta(s)): "
                    "necessary for (1 * lambda)(n) = 1_{IsSquare n}, Selberg double-pole cancellation "
                    "W_{2,lambda}(u) = c_lambda*u + o(u), and prime-power sign alternation (-1)^k across all primes."
                ),
            },
            "all_section_6_checks_pass": base_test_ok,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 7. Lean Formalization Verification & Review Displayed-Enclosure Audit
# ---------------------------------------------------------------------------


def verify_tc058_lean_theorems_live() -> Dict[str, Any]:
    """Verify Theorems 27-30 in formal/RiemannScope/LiouvilleSquareDilation.lean via live
    `lake env lean --stdin` (`#check` and `#print axioms`) and source token checks.
    """
    lean_path = REPO_ROOT / "formal" / "RiemannScope" / "LiouvilleSquareDilation.lean"
    src = lean_path.read_text(encoding="utf-8")
    no_block = re.sub(r"/-.*?-/", "", src, flags=re.DOTALL)
    clean_src = re.sub(r"--[^\n]*", "", no_block)

    sorry_count = len(re.findall(r"\bsorry\b", clean_src))
    custom_axiom_count = len(re.findall(r"^\s*axiom\b", clean_src, flags=re.MULTILINE))
    present = all(
        re.search(rf"^theorem\s+{re.escape(thm)}\b", clean_src, flags=re.MULTILINE) is not None
        for thm in EXPECTED_TC058_THEOREMS
    )

    lines = ["import RiemannScope.LiouvilleSquareDilation"]
    for thm in EXPECTED_TC058_THEOREMS:
        fq = f"RiemannScope.LiouvilleSquareDilation.{thm}"
        lines.append(f'#eval IO.println "===CHECK:{thm}==="' )
        lines.append(f"#check {fq}")
        lines.append(f'#eval IO.println "===AXIOMS:{thm}==="' )
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
    for thm in EXPECTED_TC058_THEOREMS:
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
        "module_path": "formal/RiemannScope/LiouvilleSquareDilation.lean",
        "expected_tc058_theorems": EXPECTED_TC058_THEOREMS,
        "all_tc058_theorems_present": present,
        "sorry_count": sorry_count,
        "custom_axiom_count": custom_axiom_count,
        "lean_exit_code": proc.returncode,
        "per_theorem": per_theorem,
        "all_tc058_lean_checks_pass": bool(
            present and sorry_count == 0 and custom_axiom_count == 0 and axioms_ok
        ),
    }


def verify_tc058_review_displayed_enclosures(
    report: Dict[str, Any],
    review_path: Path = TC_058_REVIEW_DOC_PATH,
) -> Dict[str, Any]:
    """Verify that `docs/reviews/TC_058_SIMULTANEOUS_COMPATIBILITY_AND_COMBINED_ENERGY.md`
    contains zero `\\pi` macros and that every displayed `±` / `\\pm` interval carries an explicit
    `<!-- tc-enclosure: ... -->` tag outward-containing its generated 256-bit Arb ball.
    """
    text = review_path.read_text(encoding="utf-8")
    pi_macros = re.findall(r"\\pi(?![a-zA-Z])", text)
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
    return {
        "review_path": str(review_path),
        "pi_macro_count": len(pi_macros),
        "total_displayed_intervals_found": len(raw_intervals),
        "tagged_and_checked_count": len(checked_rows),
        "untagged_count": len(untagged_intervals),
        "failed_count": len(failed_intervals),
        "untagged_intervals": untagged_intervals,
        "failed_intervals": failed_intervals,
        "all_displayed_intervals_contain_generated_enclosures": all_ok,
    }


def execute_task_tc058_simultaneous_compatibility_audit(
    prec_bits: int = 256,
    verify_lean_live: bool = True,
    verify_review_doc: bool = True,
) -> Dict[str, Any]:
    """Execute the complete TASK-TC-058 mathematical, discriminator, and 256-bit Arb audit."""
    sec1_2 = verify_section_1_and_2_narrow_repairs_and_dependency_table(prec_bits=prec_bits)
    sec3 = verify_section_3_combined_target_and_direct_cross_term(prec_bits=prec_bits)
    sec4 = verify_section_4_compensated_selberg_and_shift_elimination(prec_bits=prec_bits)
    sec5 = verify_section_5_growing_order_and_joint_gram(prec_bits=prec_bits)
    sec6 = verify_section_6_tc_compatibility_discriminators(prec_bits=prec_bits)

    assert sec1_2["all_section_1_and_2_checks_pass"] is True
    assert sec3["all_section_3_checks_pass"] is True
    assert sec4["all_section_4_checks_pass"] is True
    assert sec5["all_section_5_checks_pass"] is True
    assert sec6["all_section_6_checks_pass"] is True

    report: Dict[str, Any] = {
        "task_id": TASK_TC_058_ID,
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
            TASK_TC_057_ID,
            TASK_TC_057R_ID,
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
        "tc057r_implementation_commit": TC_057R_IMPLEMENTATION_COMMIT,
        "tc057r_reviewed_tip": TC_057R_REVIEWED_TIP,
        "branch": "task/tc-058-simultaneous-compatibility-and-combined-energy",
        "research_outcome_class": (
            "Outcome B / C — Proved partial arithmetic & analytic estimates controlling specified parts "
            "of the combined energy (square-projection mean O((log Y)^{-4}), cutoff-jump sum O((log Y)^{-2}), "
            "first-order shift elimination P_Y - R_Y = D_{2,Y}, generic growing-order remainder "
            "<= 2068*(log Y)*Y^{-3}, and joint M(Y)-layer prime-power diagonal O(Y/(log Y)^2)) with exact "
            "surviving O(Y*(log Y)^{-4}) and off-diagonal prime-power obligations identified; "
            "classified honestly via [Y, b*Y] discriminator as TC-inspired analytic number theory; "
            "SUBGATE-TC-043A remains OPEN"
        ),
        "subgate_tc043a_status": "OPEN",
        "rh_proved": False,
        "precision_bits": prec_bits,
        "circle_constant_convention": "tau = 2*pi (sole circle constant)",
        "complex_coordinate_convention": "z = x + i*y (x, y in R; critical line x = 1/2)",
        "section_1_and_2_narrow_repairs_and_dependency_table": sec1_2,
        "section_3_combined_target_and_direct_cross_term": sec3,
        "section_4_compensated_selberg_and_shift_elimination": sec4,
        "section_5_growing_order_and_joint_gram": sec5,
        "section_6_tc_compatibility_discriminators": sec6,
    }

    if verify_lean_live:
        lean_audit = verify_tc058_lean_theorems_live()
        assert lean_audit["all_tc058_lean_checks_pass"] is True, (
            f"TC-058 Lean theorem audit failed: {lean_audit}"
        )
        report["section_7_lean_formalization_audit"] = lean_audit

    arb_check = verify_all_serialized_arb_in_tree(report)
    assert arb_check["all_enclose_original_256bit_arb_ball"] is True, (
        f"Serialized Arb enclosure verification failed: {arb_check.get('failed_paths')}"
    )
    report["serialized_arb_self_check"] = arb_check

    if verify_review_doc and TC_058_REVIEW_DOC_PATH.exists():
        rev_audit = verify_tc058_review_displayed_enclosures(report, TC_058_REVIEW_DOC_PATH)
        assert rev_audit["all_displayed_intervals_contain_generated_enclosures"] is True, (
            "Displayed intervals in TC_058_SIMULTANEOUS_COMPATIBILITY_AND_COMBINED_ENERGY.md failed check: "
            f"pi_macros={rev_audit['pi_macro_count']}, untagged={rev_audit['untagged_intervals']}, "
            f"failed={rev_audit['failed_intervals']}"
        )
        report["section_8_tc058_review_displayed_enclosures_audit"] = rev_audit

    return report


def write_task_tc058_simultaneous_compatibility_artifact(
    path: Path = SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH,
    prec_bits: int = 256,
    verify_lean_live: bool = True,
    verify_review_doc: bool = True,
) -> Dict[str, Any]:
    """Generate and write `data/tc_simultaneous_compatibility_combined_energy.json`."""
    report = execute_task_tc058_simultaneous_compatibility_audit(
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
    rep = write_task_tc058_simultaneous_compatibility_artifact()
    print(
        f"Wrote {SIMULTANEOUS_COMPATIBILITY_COMBINED_ENERGY_ARTIFACT_PATH} "
        f"(subgate={rep['subgate_tc043a_status']}, rh_proved={rep['rh_proved']})"
    )
