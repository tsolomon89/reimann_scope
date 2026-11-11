r"""
TASK-TC-058 / TASK-TC-058R: Simultaneous Compatibility, Compensated Selberg Reconstruction,
Growing Logarithmic Order Joint Energy, Repaired Closure Criteria, and Combined Scale-Energy
Analysis toward SUBGATE-TC-043A.

Implements and certifies in 256-bit FLINT/Arb ball arithmetic (using tau = 2*pi as the sole
circle constant and z = x + i*y, with x, y in R and critical line x = 1/2, for complex coordinates;
preserving phi_n(X) = X^{5/2} n^{-3} exp(-X^2/n^2), Q_{a,T}(X), Q_{a,T}^{[m]}(X), T(Y) = ceil(Y^{5/4})
fixed across X in [Y, tau*Y], <f, g>_Y = int_Y^{tau*Y} f(X)g(X) dX/X, E(Y) = ||Q_{lambda,T(Y)}||_Y^2,
and F(Y) = sup_{1 <= Z <= Y} E(Z)):
1. Narrow Inherited TC-057R Closeout, Repaired Square-Dilation & Finite/Full Bridges, & Compact
   5-Category Proof Dependency Audit (Sections 1-2, Lean Theorem 31(1) & 31(5)):
   - Exact verification of roughSquarefreeDivisorsBand(U, T) vs roughPrimeSetBand(U, T) at
     (U = 5, T = 25) (0 rough composites; 5*7 = 35 > 25), (U = 5, T = 34) (0 rough composites),
     and (U = 5, T = 35) (35 = 5*7 enters as the first admissible squarefree rough composite).
   - Exact finite r^{-1} square-dilation identity Q_{lambda,T}(X) = sum_{r^2 <= T} r^{-1} Q_{mu,floor(T/r^2)}(X/r^2)
     (Lean Theorem 31(1), checked across T in {0, 1, 2, 15, 40, 100}) with T -> infty passage justified
     by absolute convergence sum_{r,n >= 1} phi_{r^2 n}(X) = zeta(6)*zeta(3)*X^{5/2} < infty, plus
     elementary uniform norm comparison ||Q_{a,infty} - Q_{a,T(Y)}||_Y <= B_tau := tau^{5/2}*sqrt(log tau)/2
     and bilateral O_eps(Y^eps) transfer (Lean Theorem 31(5)), replacing the retired exponential-tail claim.
   - Compact 5-category dependency table and K-independence of normalized trivial-zero slopes.
2. Un-Young-Expanded Combined Target, Direct <P_Y, R_Y>_Y Evaluation, & Repaired 4-Row Closure
   Implication Table (Section 3, Lean Theorems 26, 29, & 31(2)-(4)):
   - Retains P_Y, R_Y, Q_T = P_Y + R_Y, ||P_Y||_Y^2 = D_tilde(Y) + X_tilde(Y), and
     E(Y) = D_tilde(Y) + S_comb(Y) with S_comb(Y) := X_tilde(Y) + 2*<P_Y, R_Y>_Y + ||R_Y||_Y^2.
   - Evaluates <P_Y, R_Y>_Y directly across Y in {8, 16, 32, 64, 128} via certified 256-bit Arb
     quadrature and (at Y in {8, 16}) via the finite prime-power fiber sum.
   - Reconciles all four conditional closure targets via normalized finite-horizon absorption
     G_eps(R) = sup_{1 <= Z <= R} E(Z)/Z^eps:
     (i) TC-057R X_tilde + ||R_Y||_Y^2 (0 <= theta < 1/2, contraction 2*theta + 2*Theta_eps^{diag}),
     (ii) TC-058 S_comb (0 <= theta < 1, contraction theta + Theta_eps^{diag}),
     (iii) second-order T_2 (0 <= theta < 1, E = 4*D_tilde + T_2, contraction theta + 4*Theta_eps^{diag}),
     (iv) growing-order FULL joint Gram J_M = D_M + X_M (0 <= theta < 1, contraction (1+delta)*theta
          with delta = (1-theta)/2, valid at theta = 0), plus the abstract inference countermodel
          E = D = Y/(log Y)^2, X = r = 0 showing X_M alone does not close the gate without a new
          cross-scale contraction theorem for D_M.
3. Primary Proof Attempt — Compensated Selberg Reconstruction, Exact Summation by Parts, &
   Logarithmic-Shift Elimination (Section 4, Lean Theorems 27 & 28):
   - Proves sum_{d=1}^T g_d(X) = Q_{square,T}(X) and compensated Selberg split across all T >= 0,
     0 <= Q_{square,T}(X) <= C_sq := Gamma(5/4)/4 + 2*(3/(2*e))^{3/2} for X >= 1, and dyadic parity
     contrast (1 * a_2)(2^v m) = 1_{v even} d_div(m).
   - Proves O((log Y)^{-4}) upper-endpoint window energy via L_T = 1, g_T = phi_T, |R_2^{int}(T)| <= C_W*T
     (citing TC-057R Selberg/PNT asymptotic), and X^{5/2}/T(Y)^2 <= tau^{5/2}; proves O((log Y)^{-2})
     aggregate floor(T/d) jump energy; proves finite-cutoff smooth-step bound
     |Delta_d^{sm}(X)| <= C_sm*sqrt(X)/(d*(d+1)) < C_sm*sqrt(X)/d^2 giving O(Y*(log Y)^{-4}) normalized
     window energy because small d >= 1 prevent replacing exp(-c*sqrt(log d)) by a saving in Y; and
     isolates E(Y) = 4*D_tilde(Y) + T_2(Y).
4. Second Proof Attempt — Growing Logarithmic Order M(Y) = ceil(2*log Y) & Joint Layer Energy
   (Section 5, Lean Theorem 30):
   - Proves generic terminal-remainder bound ||Q_{a,L}^{[M(Y)]}/(log X)^{M(Y)}||_Y^2 <= 2068*(log Y)*Y^{-3}
     for all |a(n)| <= 1, L >= 1, Y >= 2, and joint diagonal majorant D_M(Y) = O(Y/(log Y)^2),
     distinguishing arbitrary |a| <= 1 bounds from multiplicative a(1)=1 prime-power reconstruction,
     recording live certified Y = 64 off-diagonal shares (~94.86%, ~85.03%, ~96.33%) with asymptotic
     rate 1 - O((log Y)^{-2}) for E_a(Y) asymp Y, and separating norm vs squared-norm nonmonotone
     finite strict triangle excess on Y in {8, 16, 32, 64}.
5. TC Compatibility Discriminators (Section 6):
   - Pre-stated schemas, [Y, b*Y] window-base test for b in {2, e, tau}, and arithmetic control tests,
     keeping SUBGATE-TC-043A OPEN and rh_proved False.
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
TASK_TC_058R_ID = "TASK-TC-058R"
TC_057R_IMPLEMENTATION_COMMIT = "484f69fc60e8b077b9586fd347003e72f4a4e930"
TC_057R_REVIEWED_TIP = "c944b71355d68c4b22b66954af5f620255ba5b14"
TC_058_IMPLEMENTATION_COMMIT = "d356b386cca8101ad8535d8bc881892f815e92f6"
TC_058_REVIEWED_TIP = "44a062dadc6a67ad51fcc41fe1f41bd4138007d1"

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
    "growing_order_and_second_order_conditional_absorption_and_finite_square_bridge_tc058r",
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


def evaluate_B_tau_cutoff_norm_bound_arb(prec_bits: int = 256) -> arb:
    """Certified uniform cutoff norm-difference bound B_tau = tau^{5/2} * sqrt(log tau) / 2."""
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        return (tau ** (arb(5) / arb(2))) * (tau.log().sqrt()) / arb(2)
    finally:
        flint_ctx.prec = saved


def evaluate_C_smooth_step_arb(prec_bits: int = 256) -> arb:
    """Certified unimodal derivative constant C_sm = 5/2 + 4*(5/(2*e))^{5/2} + 6*(3/(2*e))^{3/2}
    bounding |Delta_d^{sm}(X)| <= C_sm * sqrt(X) / (d*(d+1)) < C_sm * sqrt(X) / d^2.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        e_val = arb(1).exp()
        return (
            arb(5) / arb(2)
            + arb(4) * ((arb(5) / (arb(2) * e_val)) ** (arb(5) / arb(2)))
            + arb(6) * ((arb(3) / (arb(2) * e_val)) ** (arb(3) / arb(2)))
        )
    finally:
        flint_ctx.prec = saved


def evaluate_finite_square_dilation_Q_mu_rhs_arb(
    X: arb,
    T: int,
    prec_bits: int = 256,
) -> arb:
    """Certified finite square-dilation sum sum_{1 <= r^2 <= T} r^{-1} Q_{mu, floor(T/r^2)}(X / r^2)."""
    if not isinstance(T, int) or isinstance(T, bool) or T < 0:
        raise ValueError(f"T must be integer >= 0, got {T!r}")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        if T == 0 or bool(X == arb(0)):
            return arb(0)
        tot = arb(0)
        r = 1
        while r * r <= T:
            L_inner = T // (r * r)
            x_scaled = X / arb(r * r)
            q_mu_inner = arb(0)
            for n in range(1, L_inner + 1):
                mu_n = moebius_mu_int(n)
                if mu_n != 0:
                    q_mu_inner += arb(mu_n) * evaluate_phi_n_arb(
                        x_scaled, n, prec_bits=prec_bits
                    )
            tot += q_mu_inner / arb(r)
            r += 1
        return tot
    finally:
        flint_ctx.prec = saved


def evaluate_window_tail_norm_and_full_energy_enclosure_arb(
    Y: int,
    mode: str = "liouville",
    N_trunc: int = 1200,
    prec_bits: int = 256,
) -> Dict[str, arb]:
    """Certified 256-bit Arb enclosures for E_{a,T(Y)}(Y), E_{a,infty}(Y), and ||Q_{a,infty} - Q_{a,T(Y)}||_Y.

    Splits Q_{a,infty} = Q_{a,N_trunc} + R_{>N_trunc} with N_trunc > T(Y), integrating Q_{a,N_trunc}
    and Q_{a,N_trunc} - Q_{a,T(Y)} by certified acb quadrature on [Y, tau*Y] and enclosing R_{>N_trunc}
    by the rigorous analytic bound ||R_{>N_trunc}||_Y <= B_N := (tau*Y)^{5/2}*sqrt(log tau) / (2*N_trunc^2).
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        y_arb = arb(Y)
        T_Y = exact_T_cutoff_ceil_Y_5_4(Y)
        if N_trunc <= T_Y:
            raise ValueError(f"N_trunc={N_trunc} must exceed T(Y)={T_Y}")
        w_fn = _weight_fn_for_mode(mode)
        w_vals = [0] + [w_fn(n) for n in range(1, N_trunc + 1)]

        E_T = evaluate_E_L_scale_arb(Y, L=T_Y, m_shift=0, mode=mode, prec_bits=prec_bits)
        E_N = evaluate_E_L_scale_arb(Y, L=N_trunc, m_shift=0, mode=mode, prec_bits=prec_bits)

        def _diff_sq_int(
            z: acb,
            _analytic: bool,
            _T: int = T_Y,
            _N: int = N_trunc,
            _wv: Sequence[int] = tuple(w_vals),
        ) -> acb:
            z2 = z * z
            acc = acb(0)
            for n in range(_T + 1, _N + 1):
                wn = _wv[n]
                if wn != 0:
                    nc = acb(n)
                    acc += acb(wn) * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
            return (z ** 4) * (acc * acc)

        diff_TN_sq = _acb_integral_certified_arb(
            _diff_sq_int, y_arb, tau * y_arb, prec_bits=prec_bits
        )
        norm_diff_TN = diff_TN_sq.sqrt()
        B_N = ((tau * y_arb) ** (arb(5) / arb(2))) * (tau.log().sqrt()) / (
            arb(2) * (arb(N_trunc) ** 2)
        )
        norm_N = E_N.sqrt()

        norm_diff_lo = norm_diff_TN - B_N
        if bool(norm_diff_lo < arb(0)):
            norm_diff_lo = arb(0)
        norm_diff_hi = norm_diff_TN + B_N
        norm_diff_enclosure = arb.union(norm_diff_lo, norm_diff_hi)

        norm_inf_lo = norm_N - B_N
        if bool(norm_inf_lo < arb(0)):
            norm_inf_lo = arb(0)
        norm_inf_hi = norm_N + B_N
        norm_inf_enclosure = arb.union(norm_inf_lo, norm_inf_hi)
        E_inf_enclosure = norm_inf_enclosure * norm_inf_enclosure

        return {
            "E_T": E_T,
            "E_N_trunc": E_N,
            "E_inf_enclosure": E_inf_enclosure,
            "norm_T": E_T.sqrt(),
            "norm_inf_enclosure": norm_inf_enclosure,
            "norm_diff_T_to_inf_enclosure": norm_diff_enclosure,
            "tail_trunc_bound_B_N": B_N,
        }
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
        # and exact finite r^{-1} square-dilation bridge (Lean Theorem 31(1)):
        #   Q_{lambda, T}(X) = sum_{1 <= r^2 <= T} r^{-1} Q_{mu, floor(T/r^2)}(X / r^2)
        # across T >= 0, X >= 0 (because phi_{r^2 n}(X) = r^{-1} phi_n(X / r^2)), with passage T -> infty
        # justified by absolute convergence sum_{r,n >= 1} phi_{r^2 n}(X) <= zeta(6) * zeta(3) * X^{5/2} < infty.
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

        sq_bridge_lhs = evaluate_finite_square_dilation_Q_mu_rhs_arb(
            X_agm, T_agm, prec_bits=prec_bits
        )
        q_lam_agm = evaluate_Q_shifted_finite_arb(
            X_agm, L=T_agm, m_shift=0, mode="liouville", prec_bits=prec_bits
        )
        sq_bridge_res = sq_bridge_lhs - q_lam_agm

        finite_sq_bridge_grid_rows: List[Dict[str, Any]] = []
        sq_grid_ok = True
        for T_sq in (0, 1, 2, 15, 40, 100):
            for X_sq_int in (0, 1, 7, 13):
                X_sq = arb(X_sq_int)
                rhs_val = evaluate_finite_square_dilation_Q_mu_rhs_arb(
                    X_sq, T_sq, prec_bits=prec_bits
                )
                lhs_val = (
                    arb(0)
                    if (T_sq == 0 or X_sq_int == 0)
                    else evaluate_Q_shifted_finite_arb(
                        X_sq, L=T_sq, m_shift=0, mode="liouville", prec_bits=prec_bits
                    )
                )
                res_val = rhs_val - lhs_val
                cell_ok = bool(arb(0) in res_val and abs(res_val) < arb("1e-65"))
                sq_grid_ok = sq_grid_ok and cell_ok
                if X_sq_int == 7 or T_sq in (0, 1, 100):
                    finite_sq_bridge_grid_rows.append(
                        {
                            "T": T_sq,
                            "X": X_sq_int,
                            "Q_lambda_T": serialize_arb_certified(lhs_val),
                            "finite_r_inv_square_dilation_rhs": serialize_arb_certified(rhs_val),
                            "residual": serialize_arb_certified(res_val),
                            "verified": cell_ok,
                        }
                    )

        zeta_6_times_zeta_3 = acb(6).zeta().real * acb(3).zeta().real
        agm_ok = bool(
            arb(0) in agm_res
            and abs(agm_res) < arb("1e-68")
            and arb(0) in sq_bridge_res
            and abs(sq_bridge_res) < arb("1e-68")
            and sq_grid_ok
            and zeta_6_times_zeta_3 > arb(1)
        )

        # 2a-bis. Finite/full cutoff comparison (TASK-TC-058R §4B):
        # For EVERY |a(n)| <= 1 and Y >= 1, on X in [Y, tau*Y]:
        #   |Q_{a,infty}(X) - Q_{a,T(Y)}(X)| <= X^{5/2} sum_{n > T(Y)} n^{-3} <= X^{5/2}/(2*T(Y)^2) <= tau^{5/2}/2,
        # hence ||Q_{a,infty} - Q_{a,T(Y)}||_Y <= B_tau := tau^{5/2}*sqrt(log tau)/2,
        # |sqrt(E_T) - sqrt(E_infty)| <= B_tau, and |E_T - E_infty| <= 2*B_tau*sqrt(E_infty) + B_tau^2,
        # giving bilateral O_eps(Y^eps) transfer without any unsupported exponential cutoff error claim.
        B_tau = evaluate_B_tau_cutoff_norm_bound_arb(prec_bits=prec_bits)
        pointwise_tail_cap = (tau ** (arb(5) / arb(2))) / arb(2)
        cutoff_comparison_rows: List[Dict[str, Any]] = []
        cutoff_comp_ok = True
        for Y_cf in (4, 8, 16):
            for mode_cf in ("liouville", "unsigned_1"):
                enc = evaluate_window_tail_norm_and_full_energy_enclosure_arb(
                    Y_cf, mode=mode_cf, N_trunc=1200, prec_bits=prec_bits
                )
                norm_diff = enc["norm_diff_T_to_inf_enclosure"]
                sqrt_diff = abs(enc["norm_T"] - enc["norm_inf_enclosure"])
                E_diff_abs = abs(enc["E_T"] - enc["E_inf_enclosure"])
                quad_transfer_rhs = (
                    arb(2) * B_tau * enc["norm_inf_enclosure"] + (B_tau * B_tau)
                )
                row_cf_ok = bool(
                    B_tau - norm_diff > arb(0)
                    and B_tau - sqrt_diff > arb(0)
                    and quad_transfer_rhs - E_diff_abs > arb(0)
                )
                if mode_cf == "unsigned_1":
                    # Diagnostic: for unsigned a = 1, ||Q_{1,infty} - Q_{1,T(Y)}||_Y is O(1) and bounded away from 0,
                    # diagnosing why generic |a| <= 1 arguments cannot yield exponential cutoff error (without
                    # disproving a stronger statement specific to lambda).
                    exp_ref = arb(Y_cf) * (-arb(2) * arb(Y_cf).sqrt() / (tau * tau)).exp()
                    row_cf_ok = bool(row_cf_ok and norm_diff > arb(1) and E_diff_abs > exp_ref)
                cutoff_comp_ok = cutoff_comp_ok and row_cf_ok
                cutoff_comparison_rows.append(
                    {
                        "Y": Y_cf,
                        "T_Y": exact_T_cutoff_ceil_Y_5_4(Y_cf),
                        "mode": mode_cf,
                        "E_T": serialize_arb_certified(enc["E_T"]),
                        "E_inf_enclosure": serialize_arb_certified(enc["E_inf_enclosure"]),
                        "norm_diff_T_to_inf_enclosure": serialize_arb_certified(norm_diff),
                        "B_tau_minus_norm_diff_margin": serialize_arb_certified(B_tau - norm_diff),
                        "abs_E_T_minus_E_inf_enclosure": serialize_arb_certified(E_diff_abs),
                        "quad_transfer_2Btau_sqrtEinf_add_Btau2_margin": serialize_arb_certified(
                            quad_transfer_rhs - E_diff_abs
                        ),
                        "verified": row_cf_ok,
                    }
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
                "TC-058 / TC-058R: All-prime square-divisor indicator (1 * lambda)(n) = 1_{IsSquare n} vs dyadic parity (1 * a_2)(2^v m) = 1_{Even v} d_div(m), actual Selberg Liouville second-order weight w_{2,lambda} = Lambda_lambda*log + Lambda_lambda*Lambda_lambda (Lambda_lambda = -Lambda + 2*B) & finite square projection sum_{d=1}^T g_d = Q_{square,T} (including T = 0, 1), exact summation by parts keeping floor(T/d) jumps with post-Abel c_lambda collapse & jump-count telescope, exact shift elimination P_Y - R_Y = D_{2,Y}, pointwise combined quadratic forms, growing-order M-layer polynomial filter 0 < P_M(s) <= 4 on [1/4, 3/2] & joint Gram decomposition, and exact finite r^{-1} square-dilation bridge Q_{lambda,T}(X) = sum_{r^2<=T} r^{-1} Q_{mu,floor(T/r^2)}(X/r^2) for all T >= 0, X >= 0 (Lean Theorems 27-31).",
            ],
            "b_analytic_results_proved_outside_lean": [
                "Riesz-Gaussian & finite/full cutoff bridges: Q_mu(X) = X^{5/2} P_3(X^2) belongs to the published Riesz-type family (Agarwal-Garg-Maji 2022, arXiv:2202.00637, Theorem 1.2 at k = 3, u = X^2); Q_lambda(X) = sum_{r>=1} r^{-1} Q_mu(X/r^2) follows from Lean Theorem 31(1) via absolute convergence sum_{r,n>=1} phi_{r^2 n}(X) = zeta(6)*zeta(3)*X^{5/2} < infty; and for all |a(n)| <= 1, Y >= 1, ||Q_{a,infty} - Q_{a,T(Y)}||_Y <= B_tau := tau^{5/2}*sqrt(log tau)/2 gives |E_T - E_infty| <= 2*B_tau*sqrt(E_infty) + B_tau^2 and bilateral O_eps(Y^eps) transfer (Lean Theorem 31(5)).",
                "Unconditional Route D cross-scale prime-power diagonal contraction D_tilde_{lambda,pp}(Y) <= (2/(log Y)^2) sum_{p^k<=Y} ((log p)^2/p^k) F(Y/p^k) + C_{cut,diag} with normalized finite-horizon absorption D_tilde(Y)/Y^eps <= Theta_eps^{diag}(Y)*G_eps(R) + C_{cut,diag}/Y^eps (Theta_eps^{diag}(Y) <= 2*zeta''(1+eps)/(log Y)^2 -> 0, G_eps(R) = sup_{1<=Z<=R} E(Z)/Z^eps), plus scoped majorant obstructions for Route A/B Cauchy-Schwarz and Route C uncompensated Abel majorants.",
                "TC-058 / TC-058R (§4): Uniform unimodal bound 0 <= Q_{square,T}(X) <= C_sq := Gamma(5/4)/4 + 2*(3/(2*e))^{3/2} for X >= 1 giving ||c_lambda Q_{square,T}/(log X)^2||_Y^2 = O((log Y)^{-4}); O((log Y)^{-4}) upper-endpoint window energy via L_T = 1, g_T = phi_T, |R_2^{int}(T)| <= C_W*T (from TC-057R Selberg/PNT asymptotic), and X^{5/2}/T(Y)^2 <= tau^{5/2}; unconditional O((log Y)^{-2}) aggregate floor(T/d) jump energy via (d+1)(L_{d+1}+1) >= T + 1 and sum_{d=1}^{T-1} d(L_d - L_{d+1}) <= T*log T; and finite-cutoff smooth-step derivative bound |Delta_d^{sm}(X)| <= C_sm*sqrt(X)/(d*(d+1)) < C_sm*sqrt(X)/d^2 (C_sm = 5/2 + 4*(5/(2*e))^{5/2} + 6*(3/(2*e))^{3/2}), yielding O(Y*(log Y)^{-4}) normalized window energy when small d >= 1 are included.",
                "TC-058 / TC-058R (§5): Uniform generic terminal remainder bound ||Q_{a,L}^{[M(Y)]}/(log X)^{M(Y)}||_Y^2 <= 2068*(log Y)*Y^{-3} for all |a(n)| <= 1, L >= 1, Y >= 2 (M(Y) = ceil(2*log Y), bounding all three parts of A_m via explicit Robbins-Stirling + 17-interval compact monotonicity), and unconditional joint M(Y)-layer prime-power diagonal bound D_M(Y) = O(Y/(log Y)^2) uniformly for |a(n)| <= 1 (while Q_{a,T} = L_{a,M,Y} + r_{a,M,Y} requires multiplicative a with a(1) = 1).",
            ],
            "c_conditional_implications": [
                "Polylogarithmic scale-envelope bootstrap F(Y) <= A_eta Y^eta + B_eta F(Y/U_eta(Y)) => E(Y) <<_eps Y^eps (`CONDITIONAL_ON_RECURSION`, Lean Theorem 21).",
                "TC-057R Young-expanded target X_tilde(Y) + ||R_Y||_Y^2 <= A_eta Y^eta + theta_eta F(Y) (0 <= theta_eta < 1/2, contraction 2*theta_eta + 2*Theta_eps^{diag}(Y)) => E(Y) <<_eps Y^eps (`CONDITIONAL_ON_SIGNED_CORRELATION`, Lean Theorem 26; forward implication only).",
                "TC-058 combined target S_comb(Y) := X_tilde(Y) + 2*<P_Y, R_Y>_Y + ||R_Y||_Y^2 <= A_eta Y^eta + theta_eta F(Y) (0 <= theta_eta < 1, contraction theta_eta + Theta_eps^{diag}(Y)) => E(Y) <<_eps Y^eps (`CONDITIONAL_ON_COMBINED_CORRELATION`, Lean Theorem 29; forward implication only).",
                "TC-058R second-order target T_2(Y) := 4*X_tilde(Y) - 4*<P_Y, D_{2,Y}>_Y + ||D_{2,Y}||_Y^2 <= A_eta Y^eta + theta_eta F(Y) (E = 4*D_tilde + T_2, 0 <= theta_eta < 1, contraction theta_eta + 4*Theta_eps^{diag}(Y)) => E(Y) <<_eps Y^eps (Lean Theorem 31(4); forward implication only).",
                "TC-058R growing-order FULL joint Gram target J_M(Y) := D_M(Y) + X_M(Y) <= A_eta Y^eta + theta_eta F(Y) (0 <= theta_eta < 1, Young parameter delta = (1 - theta_eta)/2 > 0, contraction q = (1 + delta)*theta_eta < 1 valid including theta_eta = 0) => E(Y) <<_eps Y^eps (Lean Theorem 31(3a); abstract countermodel E = D = Y/(log Y)^2, X = r = 0 in Lean Theorem 31(3b) proves bounding X_M alone is insufficient without a new cross-scale contraction theorem for D_M).",
            ],
            "d_finite_numerical_observations": [
                "Certified 256-bit Arb window evaluations at Y in {8, 16, 32, 64, 128}: direct cross term <P_Y, R_Y>_Y changes sign (> 0 at Y in {8, 16, 32, 128}, < 0 at Y = 64); S_comb(Y) alternates sign (< 0 at Y in {8, 32, 128}, > 0 at Y in {16, 64}); at Y = 64, live certified off-diagonal shares 100 * X_{a,M}(64) / J_{a,M}(64) are ~94.86% (a_2), ~85.03% (a_{3,5,7}), and ~96.33% (unsigned 1), consistent with asymptotic off-diagonal fraction 1 - O((log Y)^{-2}) when E_a(Y) asymp Y; sampled Liouville layer-sum norm and squared-norm ratios exhibit nonmonotone strict finite triangle excess on Y in {8, 16, 32, 64}.",
            ],
            "e_missing_tc_to_arithmetic_implication": [
                "Open SUBGATE-TC-043A arithmetic target: EITHER derive the fixed-order S_comb(Y) <= A_eta Y^eta + theta_eta F(Y) bound (0 <= theta_eta < 1, or T_2(Y) with 4*Theta_eps^{diag}) using the established fixed-order diagonal bootstrap, OR derive a subpower/contractive bound on the FULL growing-order Gram energy J_M(Y) = D_M(Y) + X_M(Y), OR first prove a new cross-scale contraction theorem for the growing-order diagonal D_M(Y) before using an off-diagonal-only X_M(Y) target. Varying K in normalized trivial-zero slopes yields no additional moments beyond zeta'(-2m), and all proved estimates hold for arbitrary multiplicative window base b > 1 (TC-inspired analytic number theory).",
            ],
        }

        all_ok = bool(repair_1a_ok and agm_ok and cutoff_comp_ok and slope_ok)
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
                "square_dilation_weight_exponent": -1,
                "square_dilation_scaling_identity": "phi_{r^2 n}(X) = r^{-1} phi_n(X / r^2)",
                "infinite_identity_justification": (
                    "Absolute convergence sum_{r >= 1, n >= 1} |mu(n)| phi_{r^2 n}(X) <= zeta(6)*zeta(3)*X^{5/2} < infty "
                    "justifies termwise T -> infty limit from Lean Theorem 31(1) finite identity."
                ),
                "zeta_6_times_zeta_3": serialize_arb_certified(zeta_6_times_zeta_3),
                "Q_mu_T": serialize_arb_certified(q_mu_trunc),
                "riesz_k3_minus_Q_mu_residual": serialize_arb_certified(agm_res),
                "square_divisor_bridge_minus_Q_lambda_residual": serialize_arb_certified(sq_bridge_res),
                "finite_square_bridge_grid_rows": finite_sq_bridge_grid_rows,
                "verified": agm_ok,
            },
            "finite_to_full_cutoff_comparison": {
                "pointwise_tail_cap_tau_5_2_over_2": serialize_arb_certified(pointwise_tail_cap),
                "B_tau_uniform_window_norm_bound": serialize_arb_certified(B_tau),
                "formula": "||Q_{a,infty} - Q_{a,T(Y)}||_Y <= B_tau := tau^{5/2}*sqrt(log tau)/2 for all |a(n)| <= 1, Y >= 1",
                "quadratic_energy_transfer": "|E_T - E_infty| <= 2*B_tau*sqrt(E_infty) + B_tau^2 (bilateral O_eps(Y^eps) transfer in Lean Theorem 31(5))",
                "unsigned_control_diagnostic_note": (
                    "For unsigned control a = 1, ||Q_{1,infty} - Q_{1,T(Y)}||_Y is O(1) and bounded away from 0 "
                    "(since exp(-X^2/n^2) -> 1 for n > T(Y) >> X), diagnosing why generic |a| <= 1 tail bounds "
                    "yield O(1) norm error rather than exponential decay; this does NOT disprove a stronger "
                    "cutoff-tail statement specific to lambda."
                ),
                "sampled_enclosure_rows": cutoff_comparison_rows,
                "verified": cutoff_comp_ok,
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
        # S_comb uses Theta_eps^{diag}(Y) < 2*zeta''(1 + eps)/(log Y)^2 <= q - theta_eta
        #   whenever log Y >= sqrt(2*zeta''(1 + eps)/(q - theta_eta));
        # T_2 uses 4*Theta_eps^{diag}(Y) < 8*zeta''(1 + eps)/(log Y)^2 <= q - theta_eta
        #   whenever log Y >= sqrt(8*zeta''(1 + eps)/(q - theta_eta)) = 2 * min_log_Y_S_comb.
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
            min_log_Y_T2 = (arb(8) * zetapp_1_eps / (q_arb - theta_arb)).sqrt()
            # Evaluate Theta_eps^{diag}(128) directly and check log(Y) threshold
            theta_diag_128 = arb(0)
            for p, k in prime_power_pairs_up_to(128):
                pk = p ** k
                theta_diag_128 += (arb(p).log() ** 2) / (arb(pk) ** (arb(1) + eps_arb))
            theta_diag_128 = arb(2) * theta_diag_128 / (arb(128).log() ** 2)
            ub_128 = arb(2) * zetapp_1_eps / (arb(128).log() ** 2)
            abs_ok = bool(
                theta_diag_128 < ub_128
                and arb(4) * theta_diag_128 < arb(4) * ub_128
                and abs(min_log_Y_T2 - arb(2) * min_log_Y) < arb("1e-66")
                and theta_arb < arb(1)
                and q_arb < arb(1)
            )
            all_ok = all_ok and abs_ok
            absorption_rows.append(
                {
                    "epsilon": str(eps_f),
                    "theta_eta": str(theta_f),
                    "q": str(q_f),
                    "admissible_in_tc058_un_young_transfer": True,
                    "admissible_in_tc057r_young_transfer": bool(theta_f < Fraction(1, 2)),
                    "two_zetapp_1_plus_eps": serialize_arb_certified(arb(2) * zetapp_1_eps),
                    "threshold_log_Y_for_S_comb_q": serialize_arb_certified(min_log_Y),
                    "threshold_log_Y_for_T2_4Theta_q": serialize_arb_certified(min_log_Y_T2),
                    "Theta_eps_diag_at_Y128": serialize_arb_certified(theta_diag_128),
                    "four_Theta_eps_diag_at_Y128": serialize_arb_certified(
                        arb(4) * theta_diag_128
                    ),
                    "verified": abs_ok,
                }
            )

        # Growing-order full-Gram Young schedule delta = (1 - theta_eta)/2 across theta_eta in {0, 1/2, 3/4}
        growing_young_rows: List[Dict[str, Any]] = []
        growing_young_ok = True
        for theta_f in (Fraction(0, 1), Fraction(1, 2), Fraction(3, 4)):
            delta_f = (Fraction(1, 1) - theta_f) / 2
            q_grow_f = (Fraction(1, 1) + delta_f) * theta_f
            one_minus_q_f = Fraction(1, 1) - q_grow_f
            rem_mult_f = Fraction(1, 1) + Fraction(1, 1) / delta_f
            row_gy_ok = bool(
                delta_f > 0
                and 0 <= q_grow_f < 1
                and one_minus_q_f == (Fraction(1, 1) - theta_f) * (Fraction(2, 1) - theta_f) / 2
            )
            growing_young_ok = growing_young_ok and row_gy_ok
            growing_young_rows.append(
                {
                    "theta_eta": str(theta_f),
                    "delta_young": str(delta_f),
                    "q_contraction_1_add_delta_mul_theta": str(q_grow_f),
                    "one_minus_q": str(one_minus_q_f),
                    "remainder_multiplier_1_add_inv_delta": str(rem_mult_f),
                    "verified": row_gy_ok,
                }
            )

        # Logical non-implication countermodel check (Lean Theorem 31(3b)):
        # Abstract nonnegative energies E(Y) = D(Y) = Y/(log Y)^2, X(Y) = r(Y) = 0 (Y >= 2) satisfy
        # E <= (1+delta)(D+X) + (1+1/delta)r, D = O(Y/(log Y)^2), X <= 0, r <= 2068*(log Y)*Y^{-3},
        # yet fail E(Y) <= M_c * Y^eps for every 0 < eps < 1 (witness t = 6*(M_c+1)/(1-eps)^2, Y = exp(t/(1-eps))).
        eps_cm = arb(1) / arb(2)
        M_cm = arb(10)
        t_cm = arb(6) * (M_cm + arb(1)) / ((arb(1) - eps_cm) ** 2)
        Y_cm = (t_cm / (arb(1) - eps_cm)).exp()
        E_cm = Y_cm / (Y_cm.log() ** 2)
        rhs_cm = M_cm * (Y_cm ** eps_cm)
        countermodel_ok = bool(Y_cm >= arb(2) and E_cm - rhs_cm > arb(0))

        closure_criteria_table = [
            {
                "route_id": "TC-057R_young_expanded",
                "target_observable": "X_tilde_{lambda,pp}(Y) + ||R_Y||_Y^2",
                "exact_decomposition": "E(Y) <= 2*D_tilde_{lambda,pp}(Y) + 2*(X_tilde_{lambda,pp}(Y) + ||R_Y||_Y^2)",
                "quantified_hypothesis": (
                    "forall eta > 0, exists A_eta >= 0, 0 <= theta_eta < 1/2, Y_eta >= 2: "
                    "forall Y >= Y_eta, X_tilde_{lambda,pp}(Y) + ||R_Y||_Y^2 <= A_eta*Y^eta + theta_eta*F(Y)"
                ),
                "contraction_coefficient": "2*theta_eta + 2*Theta_eps^{diag}(Y)",
                "parameter_and_horizon_setup": (
                    "Given eps > 0, choose 0 < eta < min(eps, 1) and Y_* >= Y_eta large enough that "
                    "2*theta_eta + 2*Theta_eps^{diag}(Y) <= q < 1 for all Y >= Y_*; compact [1, Y_*] "
                    "controlled by G_eps(Y_*) <= M_lin*Y_* inside G_eps(R) = sup_{1<=Z<=R} E(Z)/Z^eps."
                ),
                "implication_direction": "sufficient_forward_implication_only (converse not asserted)",
                "lean_theorem": "conditional_signed_correlation_same_scale_absorption_transfer_tc057r (Theorem 26)",
                "arithmetic_hypothesis_status": "OPEN",
            },
            {
                "route_id": "TC-058_combined_un_young",
                "target_observable": "S_comb(Y) = X_tilde_{lambda,pp}(Y) + 2*<P_Y, R_Y>_Y + ||R_Y||_Y^2",
                "exact_decomposition": "E(Y) = D_tilde_{lambda,pp}(Y) + S_comb(Y)",
                "quantified_hypothesis": (
                    "forall eta > 0, exists A_eta >= 0, 0 <= theta_eta < 1, Y_eta >= 2: "
                    "forall Y >= Y_eta, S_comb(Y) <= A_eta*Y^eta + theta_eta*F(Y)"
                ),
                "contraction_coefficient": "theta_eta + Theta_eps^{diag}(Y)",
                "parameter_and_horizon_setup": (
                    "Given eps > 0, choose 0 < eta < eps and Y_* >= Y_eta with theta_eta + Theta_eps^{diag}(Y) <= q < 1 "
                    "for all Y >= Y_*; compact [1, Y_*] controlled via G_eps(Y_*) inside G_eps(R)."
                ),
                "implication_direction": "sufficient_forward_implication_only (converse not asserted)",
                "lean_theorem": "combined_target_exact_quadratic_and_conditional_absorption_tc058 (Theorem 29)",
                "arithmetic_hypothesis_status": "OPEN",
            },
            {
                "route_id": "TC-058R_second_order_compensated",
                "target_observable": "T_2(Y) = 4*X_tilde_{lambda,pp}(Y) - 4*<P_Y, D_{2,Y}>_Y + ||D_{2,Y}||_Y^2",
                "exact_decomposition": "E(Y) = 4*D_tilde_{lambda,pp}(Y) + T_2(Y) (with S_comb(Y) = 3*D_tilde_{lambda,pp}(Y) + T_2(Y))",
                "quantified_hypothesis": (
                    "forall eta > 0, exists A_eta >= 0, 0 <= theta_eta < 1, Y_eta >= 2: "
                    "forall Y >= Y_eta, T_2(Y) <= A_eta*Y^eta + theta_eta*F(Y)"
                ),
                "contraction_coefficient": "theta_eta + 4*Theta_eps^{diag}(Y)",
                "parameter_and_horizon_setup": (
                    "Given eps > 0, choose 0 < eta < eps and Y_* >= Y_eta with theta_eta + 4*Theta_eps^{diag}(Y) <= q < 1 "
                    "(note exact factor 4 on Theta_eps^{diag}(Y)); compact [1, Y_*] controlled via G_eps(Y_*)."
                ),
                "implication_direction": "sufficient_forward_implication_only (converse not asserted)",
                "lean_theorem": "growing_order_and_second_order_conditional_absorption_and_finite_square_bridge_tc058r (Theorem 31(4))",
                "arithmetic_hypothesis_status": "OPEN",
            },
            {
                "route_id": "TC-058R_growing_order_full_gram",
                "target_observable": "J_M(Y) = ||L_{M,Y}||_Y^2 = D_M(Y) + X_M(Y) (M = ceil(2*log Y))",
                "exact_decomposition": "Q_T = L_{M,Y} + r_{M,Y}, E(Y) <= (1 + delta)*J_M(Y) + (1 + 1/delta)*||r_{M,Y}||_Y^2",
                "quantified_hypothesis": (
                    "forall eta > 0, exists A_eta >= 0, 0 <= theta_eta < 1, Y_eta >= 2: "
                    "forall Y >= Y_eta, J_M(Y) = D_M(Y) + X_M(Y) <= A_eta*Y^eta + theta_eta*F(Y)"
                ),
                "contraction_coefficient": "(1 + delta)*theta_eta with delta = (1 - theta_eta)/2 > 0 (valid at theta_eta = 0 where q = 0)",
                "parameter_and_horizon_setup": (
                    "Given eps > 0, choose 0 < eta < eps, Y_* = Y_eta >= 2, delta = (1 - theta_eta)/2 > 0 so "
                    "q = (1 + delta)*theta_eta = theta_eta*(3 - theta_eta)/2 < 1, and ||r_{M,Y}||_Y^2 <= 2068*(log Y)*Y^{-3} <= 2068*Y^{-2}; "
                    "K_grow = (1+delta)*A_eta*Y_*^{eta-eps} + (1+1/delta)*2068*Y_*^{-(2+eps)}, compact [1, Y_*] via G_eps(Y_*)."
                ),
                "implication_direction": (
                    "sufficient_forward_implication_only; X_M(Y) alone does NOT close the gate from D_M(Y) = O(Y/(log Y)^2) "
                    "unless a new cross-scale contraction theorem for D_M(Y) is separately proved"
                ),
                "lean_theorem": "growing_order_and_second_order_conditional_absorption_and_finite_square_bridge_tc058r (Theorem 31(2)-(3))",
                "arithmetic_hypothesis_status": "OPEN",
            },
        ]

        all_ok = bool(all_ok and sign_change_ok and growing_young_ok and countermodel_ok)
        return {
            "sampled_combined_target_rows": scale_rows,
            "independent_prime_power_fiber_cross_checks": fiber_cross_checks,
            "direct_cross_term_positive_scales": pos_cross_Y,
            "direct_cross_term_negative_scales": neg_cross_Y,
            "S_comb_positive_scales": pos_S_comb_Y,
            "S_comb_negative_scales": neg_S_comb_Y,
            "relaxed_conditional_absorption_schedule_rows": absorption_rows,
            "growing_order_young_schedule_rows": growing_young_rows,
            "closure_criteria_implication_table": closure_criteria_table,
            "logical_non_implication_countermodel": {
                "classification": "countermodel_to_inference_not_arithmetic_lambda_counterexample",
                "model_definition": "E(Y) = D(Y) = Y / (log Y)^2, X(Y) = 0, r(Y) = 0 for Y >= 2",
                "purpose": (
                    "Demonstrates logically why D_M(Y) = O(Y/(log Y)^2), ||r_{M,Y}||_Y^2 <= 2068*(log Y)*Y^{-3}, "
                    "and an off-diagonal-only bound X_M(Y) <= A_eta*Y^eta + theta_eta*F(Y) do NOT by themselves "
                    "imply E(Y) = O_eps(Y^eps): Y/(log Y)^2 exceeds M_c*Y^eps for every 0 < eps < 1."
                ),
                "sample_witness_eps_half_Mc_10": {
                    "epsilon": "1/2",
                    "M_c": 10,
                    "t_param": 264,
                    "log_Y_witness": 528,
                    "E_witness_minus_Mc_Y_eps_margin": serialize_arb_certified(E_cm - rhs_cm),
                    "verified": countermodel_ok,
                },
            },
            "identity_vs_estimate_note": (
                "S_comb(Y) = E(Y) - D_tilde(Y), E(Y) = 4*D_tilde(Y) + T_2(Y), and Q_T = L_{M,Y} + r_{M,Y} "
                "are exact algebraic identities, NOT arithmetic cancellation theorems; Theorems 26, 29, and 31 "
                "prove conditional forward implications via normalized finite-horizon absorption G_eps(R)."
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

        # 4.4 TASK-TC-058R §3A–3C focused boundary & finite-cutoff derivative checks
        # (analytic proofs hold for all parameters; finite checks below are regression witnesses):
        # (i) Upper endpoint: at T = T(Y) = ceil(Y^{5/4}), L_T = floor(T/T) = 1, g_T(X) = phi_T(X),
        #     and X^{5/2} / T(Y)^2 <= tau^{5/2} on X in [Y, tau*Y], hitting exact equality at Y in {1, 16, 81}.
        endpoint_boundary_rows: List[Dict[str, Any]] = []
        endpoint_checks_ok = True
        tau_5_2 = tau ** (arb(5) / arb(2))
        for Y_ep in (1, 2, 16, 81):
            T_ep = exact_T_cutoff_ceil_Y_5_4(Y_ep)
            L_T_ep = T_ep // T_ep
            X_lo = arb(Y_ep)
            X_hi = tau * arb(Y_ep)
            gT_lo = evaluate_scaled_fiber_g_arb(X_lo, T_ep, T_ep, mode="liouville", prec_bits=prec_bits)
            phiT_lo = evaluate_phi_n_arb(X_lo, T_ep, prec_bits=prec_bits)
            gT_hi = evaluate_scaled_fiber_g_arb(X_hi, T_ep, T_ep, mode="liouville", prec_bits=prec_bits)
            phiT_hi = evaluate_phi_n_arb(X_hi, T_ep, prec_bits=prec_bits)
            ratio_hi = (X_hi ** (arb(5) / arb(2))) / (arb(T_ep) ** 2)
            margin_hi = tau_5_2 - ratio_hi
            exact_boundary = Y_ep in (1, 16, 81)
            ep_ok = bool(
                L_T_ep == 1
                and arb(0) in (gT_lo - phiT_lo)
                and abs(gT_lo - phiT_lo) < arb("1e-66")
                and arb(0) in (gT_hi - phiT_hi)
                and abs(gT_hi - phiT_hi) < arb("1e-66")
                and (
                    (arb(0) in margin_hi and abs(margin_hi) < arb("1e-65"))
                    if exact_boundary
                    else (margin_hi > arb(0))
                )
            )
            endpoint_checks_ok = endpoint_checks_ok and ep_ok
            endpoint_boundary_rows.append(
                {
                    "Y": Y_ep,
                    "T_Y": T_ep,
                    "L_T": L_T_ep,
                    "exact_fourth_power_cutoff_boundary": exact_boundary,
                    "g_T_minus_phi_T_at_Y": serialize_arb_certified(gT_lo - phiT_lo),
                    "g_T_minus_phi_T_at_tau_Y": serialize_arb_certified(gT_hi - phiT_hi),
                    "X_hi_5_2_over_T_sq": serialize_arb_certified(ratio_hi),
                    "tau_5_2_minus_ratio_margin": serialize_arb_certified(margin_hi),
                    "verified": ep_ok,
                }
            )

        # (ii) Finite-cutoff smooth-step bound: |Delta_d^{sm}(X)| <= C_sm * sqrt(X) / (d*(d+1)) < C_sm * sqrt(X) / d^2
        #      where C_sm = 5/2 + 4*(5/(2*e))^{5/2} + 6*(3/(2*e))^{3/2} > 3*zeta(3).
        C_sm = evaluate_C_smooth_step_arb(prec_bits=prec_bits)
        three_zeta_3 = arb(3) * acb(3).zeta().real
        smooth_step_sample_rows: List[Dict[str, Any]] = []
        smooth_step_ok = bool(C_sm - three_zeta_3 > arb(0))
        for Y_sm in (8, 16, 32):
            T_sm = exact_T_cutoff_ceil_Y_5_4(Y_sm)
            for x_tag, X_sm in (("Y", arb(Y_sm)), ("tau*Y", tau * arb(Y_sm))):
                for d_sm in (1, 2, 3, 5, T_sm // 2, T_sm - 1):
                    L_d_sm = T_sm // d_sm
                    delta_sm_val = (
                        evaluate_Q_shifted_finite_arb(
                            X_sm / arb(d_sm), L=L_d_sm, m_shift=0, mode="liouville", prec_bits=prec_bits
                        )
                        / arb(d_sm).sqrt()
                        - evaluate_Q_shifted_finite_arb(
                            X_sm / arb(d_sm + 1), L=L_d_sm, m_shift=0, mode="liouville", prec_bits=prec_bits
                        )
                        / arb(d_sm + 1).sqrt()
                    )
                    abs_delta_sm = abs(delta_sm_val)
                    tight_ub = C_sm * X_sm.sqrt() / arb(d_sm * (d_sm + 1))
                    inv_d2_ub = C_sm * X_sm.sqrt() / arb(d_sm * d_sm)
                    ok_sm = bool(tight_ub - abs_delta_sm > arb(0) and inv_d2_ub - tight_ub > arb(0))
                    smooth_step_ok = smooth_step_ok and ok_sm
                    if d_sm in (1, T_sm - 1) and x_tag == "tau*Y":
                        smooth_step_sample_rows.append(
                            {
                                "Y": Y_sm,
                                "T_Y": T_sm,
                                "X_point": x_tag,
                                "d": d_sm,
                                "L_d": L_d_sm,
                                "abs_Delta_d_smooth": serialize_arb_certified(abs_delta_sm),
                                "C_sm_sqrtX_over_d_d_add_1_ub": serialize_arb_certified(tight_ub),
                                "bound_margin": serialize_arb_certified(tight_ub - abs_delta_sm),
                                "verified": ok_sm,
                            }
                        )

        all_ok = bool(
            sq_id_ok
            and dyadic_conv_ok
            and abel_all_ok
            and endpoint_checks_ok
            and smooth_step_ok
            and c_lambda < arb(0)
        )
        return {
            "c_lambda": serialize_arb_certified(c_lambda),
            "gamma_5_4_over_4": serialize_arb_certified(gamma_quarter_term),
            "unimodal_peak_const": serialize_arb_certified(unimodal_peak_const),
            "C_sq": serialize_arb_certified(C_sq),
            "C_sm_smooth_step_const": serialize_arb_certified(C_sm),
            "three_zeta_3_small_w_const": serialize_arb_certified(three_zeta_3),
            "X1_max_Q_square_sampled": serialize_arb_certified(X1_max_q_sq),
            "pointwise_square_projection_and_compensated_split_rows": X_pt_checks,
            "upper_endpoint_coupled_cutoff_checks": {
                "analytic_proof_scope": (
                    "All Y >= 2, X in [Y, tau*Y]: L_T = floor(T/T) = 1 => g_T(X) = phi_T(X) <= X^{5/2}/T^3; "
                    "|R_2^{int}(T)| <= C_W*T (TC-057R Selberg/PNT asymptotic) and T(Y)^2 >= Y^{5/2} yield "
                    "|R_2^{int}(T)*g_T(X)/(log X)^2| <= C_W*X^{5/2}/(T(Y)^2*(log Y)^2) <= C_W*tau^{5/2}/(log Y)^2, "
                    "giving O((log Y)^{-4}) window energy (finite rows below are boundary checks, not the proof)."
                ),
                "rows": endpoint_boundary_rows,
                "verified": endpoint_checks_ok,
            },
            "smooth_step_finite_cutoff_bound_checks": {
                "analytic_proof_scope": (
                    "All X > 0, T >= 2, 1 <= d <= T - 1: writing phi_q(X/y)/sqrt(y) = X^{5/2}*y^{-3}*q^{-3}*exp(-X^2/(y^2*q^2)) "
                    "and w = X/y > 0 gives d/dy [phi_q(X/y)/sqrt(y)] = (sqrt(X)/y^2)*w^2*q^{-3}*exp(-w^2/q^2)*(2*w^2/q^2 - 3); "
                    "bounding |d/dy sum_{q<=L_d} lambda(q)*phi_q(X/y)/sqrt(y)| <= C_sm*sqrt(X)/y^2 pointwise for all y > 0 "
                    "via unimodal sum-integral comparison with w^{-1} peaks (w > 1) and 3*zeta(3)*w^2 <= 3*zeta(3) < C_sm (0 < w <= 1) "
                    "and integrating over y in [d, d+1] proves |Delta_d^{sm}(X)| <= C_sm*sqrt(X)/(d*(d+1)) < C_sm*sqrt(X)/d^2."
                ),
                "sample_rows": smooth_step_sample_rows,
                "verified": smooth_step_ok,
            },
            "R2_int_linear_bound_provenance": (
                "Already established in TC-057R §4 Theorem 4.3(3) via the Selberg/PNT asymptotic "
                "W_2(u) = c_lambda*u + O(u*exp(-c*sqrt(log u))) (Dirichlet hyperbola cancellation of u*log u "
                "plus PNT for lambda, NOT Chebyshev's separate O(u*log u) majorants alone), covering all integer "
                "d >= 1 including d = 1 where R_2^{int}(1) = -c_lambda."
            ),
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
                    "Upper endpoint R_2^{int}(T)*g_T(X)/(log X)^2 has window energy O((log Y)^{-4}) because L_T = floor(T/T) = 1 gives g_T(X) = phi_T(X) <= X^{5/2}/T^3, and combining |R_2^{int}(T)| <= C_W*T (TC-057R Selberg/PNT asymptotic) with T(Y)^2 >= Y^{5/2} yields |R_2^{int}(T)*g_T(X)/(log X)^2| <= C_W*X^{5/2}/(T(Y)^2*(log Y)^2) <= C_W*tau^{5/2}/(log Y)^2 on X in [Y, tau*Y].",
                    "Aggregate floor(T/d) cutoff-jump sum sum_{d=1}^{T-1} R_2^{int}(d)*Delta^{jump}_d(X)/(log X)^2 has unconditional decaying window energy O((log Y)^{-2}) -> 0 because |R_2^{int}(d)| <= C_W*d (from TC-057R Selberg/PNT asymptotic, including d = 1), every jump index satisfies (d+1)*q >= T + 1 > Y^{5/4} (so phi_{(d+1)q}(X) <= tau^{5/2}*Y^{-5/4}), and sum_{d=1}^{T-1} d*(L_d - L_{d+1}) = sum_{d=1}^T floor(T/d) - T <= T*log T.",
                    "Combining with Q_T = P_Y + R_Y eliminates the O(Y*(log Y)^{-2}) first-order shift R_Y via P_Y - R_Y = D_{2,Y} and Q_T = 2*P_Y - D_{2,Y}.",
                ],
                "surviving_uncontrolled_terms_and_exponents": [
                    "Smooth-step PNT remainder sum_{d=1}^{T-1} R_2^{int}(d)*Delta^{smooth}_d(X)/(log X)^2 inside D_{2,Y}(X): on finite-cutoff fibers L_d = floor(T/d), |Delta^{smooth}_d(X)| <= C_sm*sqrt(X)/(d*(d+1)) < C_sm*sqrt(X)/d^2; because the sum begins at d = 1 (with |R_2^{int}(1)| = |c_lambda| and |R_2^{int}(d)| <= C'*d*exp(-c*sqrt(log d)) for d >= 2, where the PNT saving is in d rather than Y), the unsigned majorant yields only O(sqrt(X)) unnormalized and O(Y*(log Y)^{-4}) in normalized window energy (matching the unsigned order of -Q_T^{[2]}/(log X)^2). Failure of this unsigned majorant to prove subpower growth does not prove the signed expression grows.",
                    "Prime-power off-diagonal 4*X_tilde_{lambda,pp}(Y) and cross term -4*<P_Y, D_{2,Y}>_Y in E(Y) = 4*D_tilde + T_2 (with T_2 = 4*X_tilde - 4*<P_Y, D_{2,Y}> + ||D_{2,Y}||_Y^2 and conditional contraction coefficient theta_eta + 4*Theta_eps^{diag}(Y)): subpower energy still requires genuine signed cancellation across distinct prime-power fibers.",
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

                # Quantify Minkowski layer-sum triangle excess:
                # norm ratio (sum_{m=0}^{M-1} ||layer_m||_Y) / ||L_{a,M}||_Y vs squared-norm ratio
                # (sum_{m=0}^{M-1} ||layer_m||_Y)^2 / ||L_{a,M}||_Y^2 at Y in {8, 16, 32, 64}
                layer_minkowski_sq: Optional[arb] = None
                layer_minkowski_norm: Optional[arb] = None
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
                    layer_minkowski_norm = sum_layer_norms
                    layer_minkowski_sq = sum_layer_norms * sum_layer_norms
                    if not bool(
                        layer_minkowski_norm - E_L_joint.sqrt() > arb(0)
                        and layer_minkowski_sq - E_L_joint > arb(0)
                    ):
                        joint_gram_ok = False

                E_tot = evaluate_E_L_scale_arb(
                    Y_int, L=T_Y, m_shift=0, mode=mode, prec_bits=prec_bits
                )
                off_diag_ratio = X_M_off_consistency / E_L_joint
                off_diag_pct = arb(100) * off_diag_ratio
                diag_ratio = D_M_diag / E_L_joint
                entry_m: Dict[str, Any] = {
                    "E_total_Y": serialize_arb_certified(E_tot),
                    "joint_M_layer_norm_sq": serialize_arb_certified(E_L_joint),
                    "joint_M_prime_power_diagonal": serialize_arb_certified(D_M_diag),
                    "joint_M_prime_power_off_diagonal": serialize_arb_certified(X_M_off_consistency),
                    "diagonal_over_joint_ratio": serialize_arb_certified(diag_ratio),
                    "off_diagonal_over_joint_ratio": serialize_arb_certified(off_diag_ratio),
                    "off_diagonal_over_joint_pct": serialize_arb_certified(off_diag_pct),
                }
                if direct_pair_res is not None:
                    entry_m["direct_pair_minus_consistency_off_diagonal_residual"] = (
                        serialize_arb_certified(direct_pair_res)
                    )
                if layer_minkowski_sq is not None and layer_minkowski_norm is not None:
                    norm_ratio = layer_minkowski_norm / E_L_joint.sqrt()
                    sq_ratio = layer_minkowski_sq / E_L_joint
                    entry_m["minkowski_layer_sum_norm"] = serialize_arb_certified(
                        layer_minkowski_norm
                    )
                    entry_m["minkowski_norm_ratio_over_joint"] = serialize_arb_certified(
                        norm_ratio
                    )
                    entry_m["minkowski_layer_sum_norm_sq"] = serialize_arb_certified(
                        layer_minkowski_sq
                    )
                    entry_m["minkowski_sq_over_joint_ratio"] = serialize_arb_certified(
                        sq_ratio
                    )
                    entry_m["minkowski_over_joint_ratio"] = serialize_arb_certified(
                        sq_ratio
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

        # Verify live certified Y = 64 off-diagonal shares (~94.86% for a2, ~85.03% for a_3_5_7,
        # ~96.33% for unsigned_1) and nonmonotone strict finite triangle excess for Liouville!
        row_y64 = [r for r in joint_gram_rows if r["Y"] == 64][0]["modes"]
        pct_a2_64 = arb(row_y64["a2"]["off_diagonal_over_joint_pct"]["arb_ball_str"])
        pct_a357_64 = arb(row_y64["a_3_5_7"]["off_diagonal_over_joint_pct"]["arb_ball_str"])
        pct_u1_64 = arb(row_y64["unsigned_1"]["off_diagonal_over_joint_pct"]["arb_ball_str"])
        liouville_sq_ratios = [
            arb(r["modes"]["liouville"]["minkowski_sq_over_joint_ratio"]["arb_ball_str"])
            for r in joint_gram_rows
        ]
        liouville_norm_ratios = [
            arb(r["modes"]["liouville"]["minkowski_norm_ratio_over_joint"]["arb_ball_str"])
            for r in joint_gram_rows
        ]
        pct_and_nonmonotone_ok = bool(
            arb("94.85") < pct_a2_64 < arb("94.87")
            and arb("85.02") < pct_a357_64 < arb("85.04")
            and arb("96.32") < pct_u1_64 < arb("96.34")
            and all(bool(r_val > arb(1)) for r_val in liouville_norm_ratios)
            and all(bool(r_val > arb(1)) for r_val in liouville_sq_ratios)
            and bool(liouville_sq_ratios[1] > liouville_sq_ratios[2])
            and bool(liouville_norm_ratios[1] > liouville_norm_ratios[2])
        )
        joint_gram_ok = bool(joint_gram_ok and pct_and_nonmonotone_ok)

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
            "live_Y64_growing_control_off_diagonal_summary": {
                "a2_off_diagonal_pct_Y64": row_y64["a2"]["off_diagonal_over_joint_pct"],
                "a_3_5_7_off_diagonal_pct_Y64": row_y64["a_3_5_7"]["off_diagonal_over_joint_pct"],
                "unsigned_1_off_diagonal_pct_Y64": row_y64["unsigned_1"]["off_diagonal_over_joint_pct"],
                "liouville_sampled_triangle_excess_is_nonmonotone": True,
                "verified": pct_and_nonmonotone_ok,
            },
            "cost_and_concentration_summary": {
                "resummation_vs_cancellation": (
                    "Resumming the M(Y) layers back to Q_T - Q_T^{[M]}/(log X)^M is a consistency identity, "
                    "not a cancellation proof."
                ),
                "arbitrary_bounded_vs_multiplicative_hypotheses": (
                    "The terminal-remainder bound ||r_{a,M,Y}||_Y^2 <= 2068*(log Y)*Y^{-3} and the fiberwise "
                    "diagonal majorant D_M(Y) = O(Y/(log Y)^2) hold for arbitrary bounded coefficients |a(n)| <= 1; "
                    "the prime-power reconstruction Q_{a,T} = L_{a,M,Y} + r_{a,M,Y} and the resulting energy "
                    "concentration require completely multiplicative a with a(1) = 1 and |a(n)| <= 1."
                ),
                "unconditional_joint_diagonal_bound": (
                    "Because 0 < P_M(s) <= 4 uniformly on s in [1/4, 3/2] for all M >= 1 (Lean Theorem 30(4)), "
                    "the joint M(Y)-layer prime-power diagonal satisfies D_M(Y) = O(Y/(log Y)^2) uniformly for "
                    "all bounded |a(n)| <= 1; however O(Y/(log Y)^2) is NOT an all-eps subpower bound and has "
                    "not been proved to satisfy cross-scale contraction."
                ),
                "surviving_joint_gram_and_concentration_scope": (
                    "For multiplicative growing-energy controls (1, a_2, a_{3,5,7}) with E_a(Y) asymp Y, the "
                    "small terminal remainder ||r_{a,M,Y}||_Y^2 = O((log Y)*Y^{-3}) controls proximity to the FULL "
                    "joint Gram energy J_{a,M}(Y) = D_{a,M}(Y) + X_{a,M}(Y), while subtracting D_{a,M}(Y) = O(Y/(log Y)^2) "
                    "gives off-diagonal share X_{a,M}(Y)/J_{a,M}(Y) = 1 - O((log Y)^{-2}) (live Y = 64 shares: "
                    "~94.86% for a_2, ~85.03% for a_{3,5,7}, ~96.33% for 1). Sampled Liouville norm ratios "
                    "(sum_m ||layer_m||_Y)/||L_M||_Y and squared-norm ratios (sum_m ||layer_m||_Y)^2/||L_M||_Y^2 "
                    "establish nonmonotone finite strict triangle excess on Y in {8, 16, 32, 64} (not asymptotic "
                    "divergence). Closing SUBGATE-TC-043A along the growing-order route requires bounding the "
                    "FULL joint Gram energy J_M(Y) = D_M(Y) + X_M(Y) (or first proving a new cross-scale "
                    "contraction theorem for D_M(Y))."
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
                "objects": "W_2(d), R_2^{int}(d) = W_2(d) - c_lambda*d, Delta^{smooth}_d, Delta^{jump}_d, D_{2,Y}, T_2(Y)",
                "quantifiers": "forall Y >= 2, T = ceil(Y^{5/4}), X in [Y, b*Y]",
                "hypotheses": (
                    "|R_2^{int}(d)| <= C_W*d for all d >= 1 (from TC-057R Selberg/PNT asymptotic), "
                    "|R_2^{int}(d)| <= C'*d*exp(-c*sqrt(log d)) for d >= 2, and (d+1)*(L_{d+1}+1) >= T + 1"
                ),
                "input_source": "TC-057R Selberg/PNT asymptotic + exact discrete summation by parts + finite-cutoff smooth-step bound |Delta^{smooth}_d(X)| < C_sm*sqrt(X)/d^2 + second-order shift identity",
                "conclusion": (
                    "Cancels Route C boundary obstruction, bounds upper endpoint by O((log Y)^{-4}) (via L_T=1, g_T=phi_T, X^{5/2}/T(Y)^2 <= b^{5/2}) "
                    "and jump energy by O((log Y)^{-2}), and eliminates R_Y via Q_T = 2*P_Y - D_{2,Y}, leaving O(Y*(log Y)^{-4}) unsigned energy "
                    "in ||D_{2,Y}||_Y^2 (because small d >= 1 prevent replacing exp(-c*sqrt(log d)) by a saving in Y) and conditional contraction theta_eta + 4*Theta_eps^{diag}(Y) on T_2(Y)"
                ),
                "status": "PROVED_PARTIAL_REDUCTION (identities in Lean Theorems 28-29 & 31(4); leaves O(Y*(log Y)^{-4}) unsigned energy without subpower cancellation)",
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
                "title": "Joint M(Y)-layer polynomial kernel bound, prime-power diagonal majorant, and off-diagonal share",
                "objects": "P_M(s) = sum_{m < M} (1 - s)^m, L_{a,M}(X; T), J_{a,M}(Y) = D_{a,M}(Y) + X_{a,M}(Y)",
                "quantifiers": "forall M >= 1, forall bounded |a(n)| <= 1 (diagonal bound) and completely multiplicative a with a(1) = 1 (reconstruction), forall Y >= 16",
                "hypotheses": "0 < P_M(s) <= 4 on s in [1/4, 3/2] and |a(n)| <= 1 (plus multiplicativity of a for Q_{a,T} = L_{a,M,Y} + r_{a,M,Y})",
                "input_source": "Finite geometric series sum + Gaussian fast decay for n <= Y^{1/2}",
                "conclusion": (
                    "D_{a,M}(Y) = O(Y / (log Y)^2) uniformly for |a| <= 1, giving off-diagonal share "
                    "X_{a,M}(Y)/J_{a,M}(Y) = 1 - O((log Y)^{-2}) for multiplicative controls with E_a(Y) asymp Y; "
                    "bounding X_M(Y) alone does NOT close SUBGATE-TC-043A without bounding full J_M(Y) or proving a new contraction theorem for D_M(Y)"
                ),
                "status": "PROVED_UNCONDITIONAL (polynomial & Gram identities in Lean Theorem 30; integral bound proved analytically)",
                "tc_discriminator_result": "Diagonal majorant is generic in |a| <= 1; Q_{a,T} = L_{a,M,Y} + r_{a,M,Y} requires multiplicative a; holds for all b > 1",
            },
            {
                "lemma_id": "LEM-TC058R-F",
                "title": "Full growing-order Gram conditional absorption, logical non-implication countermodel, finite r^{-1} square bridge, and B_tau cutoff transfer",
                "objects": "J_M(Y) = D_M(Y) + X_M(Y), T_2(Y), Q_{lambda,T}(X), Q_{mu,floor(T/r^2)}(X/r^2), B_tau = tau^{5/2}*sqrt(log tau)/2",
                "quantifiers": "forall T >= 0, X >= 0 (square bridge); forall Y >= 1, |a(n)| <= 1 (B_tau); forall eta in (0, eps), 0 <= theta_eta < 1 (absorption)",
                "hypotheses": "J_M(Y) <= A_eta*Y^eta + theta_eta*F(Y) (or T_2(Y) <= A_eta*Y^eta + theta_eta*F(Y) with 4*Theta_eps^{diag})",
                "input_source": "Young inequality with delta = (1 - theta_eta)/2 + normalized finite-horizon absorption G_eps(R) + elementary n^{-3} tail sum",
                "conclusion": (
                    "J_M bound => E(Y) <<_eps Y^eps (valid including theta_eta = 0); abstract countermodel E = D = Y/(log Y)^2, X = r = 0 "
                    "refutes off-diagonal-only inference; Q_{lambda,T}(X) = sum_{r^2<=T} r^{-1} Q_{mu,floor(T/r^2)}(X/r^2); and "
                    "||Q_{a,infty} - Q_{a,T(Y)}||_Y <= B_tau yields bilateral O_eps(Y^eps) transfer"
                ),
                "status": "PROVED_CONDITIONAL_AND_BRIDGE (Lean Theorem 31 + analytic B_tau window tail bound)",
                "tc_discriminator_result": "Square bridge requires all-prime lambda(p) = -1; B_tau and absorption algebra generalize to any b > 1",
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
    """Verify Theorems 27-31 in formal/RiemannScope/LiouvilleSquareDilation.lean via live
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
        "repair_task_id": TASK_TC_058R_ID,
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
        "tc058_implementation_commit": TC_058_IMPLEMENTATION_COMMIT,
        "tc058_reviewed_tip": TC_058_REVIEWED_TIP,
        "branch": "task/tc-058r-closure-criteria-and-analytic-scope-repair",
        "research_outcome_class": (
            "Outcome B / C (TC-058R Repaired Baseline) — Preserves valid arithmetic & analytic estimates "
            "(square-projection mean O((log Y)^{-4}), upper endpoint O((log Y)^{-4}), cutoff-jump sum "
            "O((log Y)^{-2}), first-order shift elimination P_Y - R_Y = D_{2,Y}, smooth-step finite-cutoff "
            "majorant O(Y*(log Y)^{-4}), generic growing-order remainder <= 2068*(log Y)*Y^{-3}, joint "
            "M(Y)-layer diagonal majorant O(Y/(log Y)^2), finite r^{-1} square bridge, and B_tau finite/full "
            "norm transfer) and repairs all four conditional closure criteria (requiring full J_M = D_M + X_M "
            "rather than X_M alone unless a new diagonal contraction for D_M is proved); classified honestly "
            "via [Y, b*Y] discriminator as TC-inspired analytic number theory; SUBGATE-TC-043A remains OPEN"
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
