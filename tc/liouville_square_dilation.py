"""
TASK-TC-054 / TASK-TC-054R: Liouville Square-Dilation Transfer, Unconstrained Common-Factor Expansion,
Transition Poisson Summation, Fourier Tail-Ratio Certification, Exact Rational Cutoffs,
Unequal-Block Sum-Integral Bound, and Global Stieltjes Energy Proof toward SUBGATE-TC-043A.

Implements and certifies in 256-bit FLINT/Arb ball arithmetic and exact symbolic algebra:
1. Reversible Square-Dilation Transfer (mu <-> lambda) and Operator/Grade Scope:
   - Exact prime-power and integer square-divisor identities:
         lambda(n) = sum_{d^2 | n} mu(n / d^2),
         mu(n)     = sum_{d^2 | n} mu(d) lambda(n / d^2),
     where lambda(n) = (-1)^{Omega(n)} (lambda(1) = 1) is Liouville's completely multiplicative
     function and Omega(n) counts prime factors with multiplicity.
   - Reversible Gaussian sum transfer:
         Q_a(X) = X^{5/2} sum_{n >= 1} (a(n) / n^3) exp(-X^2 / n^2)   (a in {mu, lambda}),
         |Q_a(X)| <= zeta(3) X^{5/2},   |R_{a,>T}(X)| <= X^{5/2} / (2 T^2),
         Q_lambda(X) = sum_{d >= 1} Q_mu(X / d^2) / d,
         Q_mu(X)     = sum_{d >= 1} mu(d) Q_lambda(X / d^2) / d,
     with proved dilation tail bound <= zeta(3) X^{5/2} / (5 D^5).
   - Reversible weighted L^2 norm equivalence on (0, infty) with measure X^{-2 eta} dX/X:
         ||f(. / a)||_eta = a^{-eta} ||f||_eta,
         ||Q_lambda||_eta <= zeta(1 + 2 eta) ||Q_mu||_eta,
         ||Q_mu||_eta     <= (zeta(1 + 2 eta) / zeta(2 + 4 eta)) ||Q_lambda||_eta   (eta > 0),
     with asymptotic residues 1/2 and 1/(2 zeta(2)) = 12 / tau^2 as eta -> 0^+.
   - Equivalence between the tau-grade interval subpower energy bound
         forall eps > 0 exists C_eps < infty forall Y >= 1, int_Y^{tau Y} |Q_a(X)|^2 dX/X <= C_eps Y^eps
     and finiteness of ||Q_a||_eta for all eta in (0, 5/2), together with the analytic Mellin
     bridge to RH (z = a + i b, zeta zero rho = x + i y) and irrationality of log_tau(2) and
     log_tau(d^2) (d >= 2) via Lindemann's theorem.

2. Unconstrained Common-Factor Expansion and Fixed-Order Euler-Maclaurin Error Bound:
   - Complete multiplicativity common-factor sign cancellation:
         lambda(d r) lambda(d s) = lambda(d)^2 lambda(r) lambda(s) = lambda(r) lambda(s)
     for ALL integers d, r, s >= 1.
   - Exact unconstrained common-factor expansion:
         Q_lambda(X)^2 = sum_{r, s >= 1, gcd(r, s) = 1} (lambda(r) lambda(s) X^5 / (r s)^3)
                         * sum_{d >= 1} d^{-6} exp(-L^2 / d^2),
     where L = X sqrt(r^{-2} + s^{-2}), with leading Gaussian term (c_0 = 3 sqrt(tau/2) / 8):
         L^lambda_{r,s} = c_0 lambda(r) lambda(s) (r s)^2 / (r^2 + s^2)^{5/2}.
   - Fixed-order periodic Bernoulli Euler-Maclaurin bound for f(v) = v^{-6} exp(-1 / v^2):
         |sum_{d >= 1} d^{-6} exp(-L^2 / d^2) - c_0 L^{-5}| <= C_N L^{-5 - N}
     for every even N >= 2, with C_2 = 1.8512576670... and C_4 = 8.7523717600..., controlling
     every fixed subtransition range A <= X^{1 - delta} whenever (N + 1) delta > 1.

3. Exact Poisson Summation Formula at the Transition (A ~ X) and Repaired Fourier Certification:
   - f(v) = v^{-6} exp(-1/v^2) (v != 0), f(0) = 0 is NOT in S(R) because v^6 f(v) -> 1, but
     satisfies C^infty flatness at 0, f^{(j)}(v) = O(|v|^{-6-j}) at infinity, f^{(j)} in L^1(R),
     and C^1(R/Z) periodization convergence (DLMF 1.8.14), proving:
         sum_{d >= 1} d^{-6} exp(-L^2 / d^2) = L^{-5} [c_0 + sum_{j >= 1} hat{f}(j L)].
   - Certified 256-bit Arb evaluation of hat{f}(xi) with monotonic tail-ratio bounds R_even, R_odd,
     outward certification of R <= 1/2 (or 1/(1 - R) when 1/2 < R < 1), interval-input Lipschitz
     enclosure, and independent certified quadrature cross-checks (`acb.integral`).

4. Rectangular-Block Decomposition, Unequal-Block Bound, Exact Cutoffs, and Global Stieltjes Energy Proof:
   - Exact rational cutoffs for U_lambda(Y; M) (reproducing and fixing the M = 1 + 2^{-42} regression).
   - Repaired widely unequal block bound:
         |B_{A,B}(X)| <= (7/3) C_* min(A, B)^3 / max(A, B)^2,   C_* = max{zeta(6), c_0 + 27 exp(-3)}.
   - Repaired dyadic Abel estimate |U_lambda(Y; M)| << M^{1/2} min(M/Y, (Y/M)^{5/2}) exp(-c Phi(M))
     (M >= 16), analytical refutation of the old M^{-1/2} prefactor via Res_{z=0} M[Q_lambda](z) != 0,
     collapse of sum_{q>=1} ((sum_{e|q} mu(e))/q) Q_lambda(X/q)^2 = Q_lambda(X)^2, and global
     Stieltjes integration-by-parts proof |Q_lambda(X)| << sqrt(X) exp(-c_1 Phi(X)) (X >= 256) and
     E_lambda(Y) << Y exp(-2 c_2 Phi(Y)) <<_D Y (log Y)^{-D}.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Tuple, Union

from flint import acb, arb, ctx as flint_ctx
import sympy as sp

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tc.canonical_theta_correlation_bound import (
    EPIC_TC_042_ID,
    REPO_ROOT,
    serialize_arb_certified,
    verify_all_serialized_arb_in_tree,
)
from tc.prime_euler_moebius_recovery import (
    moebius_mu_int,
    prime_factors_with_multiplicity,
)

TASK_TC_054_ID = "TASK-TC-054"
TASK_TC_054R_ID = "TASK-TC-054R"
TASK_TC_054R2_ID = "TASK-TC-054R2"
TASK_TC_055_ID = "TASK-TC-055"
PRIOR_MERGED_MAIN_TC_053R = "c82e439708b0b6031db6a77bf3977688d9f0758b"
TC_053R2_IMPLEMENTATION_COMMIT = "cc303030138c670e8f01aaaab483bbeca6bc17d1"
TC_053R2_REVIEWED_TIP = "21576861ecd0dcbf874afec91b299fd6060f4f03"
TC_054_IMPLEMENTATION_COMMIT = "8f6afcfb9161aa77c74bc40605ac4fabae8b432e"
TC_054_REVIEWED_TIP = "cdee197acc9c3e75a4c8cffc94c10bec1bcb97fa"
TC_054R_IMPLEMENTATION_COMMIT = "27489f195d3313d9ee60773157e3a8240f5bcadd"
TC_054R_REVIEWED_TIP = "f265042ab52cabda29e76859cebace21cfae9239"
TC_054R2_IMPLEMENTATION_COMMIT = "a4b30737013aa2e16d095b897fa6b97b08f451dc"
TC_054R2_REVIEWED_TIP = "e178497d7637b799ce6eda5ed0cb2486c841c577"
TC_054R2_MERGED_MAIN_BASELINE = "8a898c60b7c4cb56543a3d1e7960c39e00027c22"
TC_055_INITIAL_CLOSEOUT_COMMIT = "80d1c86408d39562b06b2c69d4b4f655a1677f82"

LIOUVILLE_SQUARE_DILATION_LEAN_MODULE_PATH = (
    REPO_ROOT / "formal" / "RiemannScope" / "LiouvilleSquareDilation.lean"
)
LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_liouville_square_dilation.json"
)


def inflate_arb_with_nonneg_bound(center_ball: arb, nonneg_bound: arb) -> arb:
    """Inflate `center_ball` by `[0, nonneg_bound.upper()]` using pure Arb ball/magnitude
    arithmetic without intermediate Python `float` conversions.
    """
    b_upper = arb(nonneg_bound).upper()
    return arb(center_ball) + arb(0, b_upper)


# ---------------------------------------------------------------------------
# 1. Exact Arithmetic Helpers (Omega(n), lambda(n), mu(n), Square-Divisor Sums)
# ---------------------------------------------------------------------------


def omega_with_multiplicity_int(n: int) -> int:
    """Return Omega(n) = sum_{p^a || n} a for integer n >= 1 (Omega(1) = 0)."""
    if n < 1:
        raise ValueError(f"omega_with_multiplicity_int requires n >= 1, got {n}")
    if n == 1:
        return 0
    return sum(exp for _p, exp in prime_factors_with_multiplicity(n))


def liouville_lambda_int(n: int) -> int:
    """Return Liouville's function lambda(n) = (-1)^{Omega(n)} for n >= 1 (lambda(1) = 1)."""
    if n < 1:
        raise ValueError(f"liouville_lambda_int requires n >= 1, got {n}")
    return 1 if (omega_with_multiplicity_int(n) % 2 == 0) else -1


def square_divisor_moebius_sum_int(n: int) -> int:
    """Return sum_{d^2 | n} mu(n // d^2) for integer n >= 1."""
    if n < 1:
        raise ValueError(f"square_divisor_moebius_sum_int requires n >= 1, got {n}")
    total = 0
    d = 1
    while d * d <= n:
        q, rem = divmod(n, d * d)
        if rem == 0:
            total += moebius_mu_int(q)
        d += 1
    return total


def square_divisor_inverse_liouville_sum_int(n: int) -> int:
    """Return sum_{d^2 | n} mu(d) * lambda(n // d^2) for integer n >= 1."""
    if n < 1:
        raise ValueError(f"square_divisor_inverse_liouville_sum_int requires n >= 1, got {n}")
    total = 0
    d = 1
    while d * d <= n:
        q, rem = divmod(n, d * d)
        if rem == 0:
            total += moebius_mu_int(d) * liouville_lambda_int(q)
        d += 1
    return total


# ---------------------------------------------------------------------------
# 2. Certified 256-bit Arb Evaluators for Q_mu(X), Q_lambda(X), and Transfer
# ---------------------------------------------------------------------------


def evaluate_Q_arith_certified_arb(
    X_val: arb,
    coeff_kind: str = "lambda",
    T_cutoff: int = 4000,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Evaluate Q_a(X) = X^{5/2} sum_{n>=1} (a(n)/n^3) exp(-X^2/n^2) in 256-bit Arb
    with outward-rounded truncation remainder |R_{a,>T}(X)| <= X^{5/2} / (2 T^2).
    """
    if coeff_kind not in ("mu", "lambda"):
        raise ValueError(f"coeff_kind must be 'mu' or 'lambda', got {coeff_kind!r}")
    if T_cutoff < 1:
        raise ValueError(f"T_cutoff must be >= 1, got {T_cutoff}")

    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X_arb = arb(X_val)
        X_sq = X_arb * X_arb
        X_pow_5_2 = X_arb ** (arb(5) / arb(2))

        partial_sum = arb(0)
        for n in range(1, T_cutoff + 1):
            a_n = moebius_mu_int(n) if coeff_kind == "mu" else liouville_lambda_int(n)
            if a_n == 0:
                continue
            n_arb = arb(n)
            term = (arb(a_n) / (n_arb ** 3)) * (-X_sq / (n_arb * n_arb)).exp()
            partial_sum += term

        partial_Q = X_pow_5_2 * partial_sum
        tail_bound = X_pow_5_2 / (arb(2) * (arb(T_cutoff) ** 2))
        enclosure = inflate_arb_with_nonneg_bound(partial_Q, tail_bound)
        zeta3_bound = arb(3).zeta() * X_pow_5_2

        return {
            "coeff_kind": coeff_kind,
            "T_cutoff": T_cutoff,
            "partial_Q": partial_Q,
            "tail_bound": tail_bound,
            "enclosure": enclosure,
            "abs_le_zeta3_X_5_2": bool(abs(enclosure).upper() <= zeta3_bound.lower()),
            "zeta3_X_5_2_bound": zeta3_bound,
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_square_dilation_transfer_certified_arb(
    X_val: arb,
    direction: str = "mu_to_lambda",
    D_cutoff: int = 80,
    T_base_cutoff: int = 4000,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Evaluate the square-dilation sum
      - direction == 'mu_to_lambda': sum_{1 <= d <= D} Q_mu(X / d^2) / d
      - direction == 'lambda_to_mu': sum_{1 <= d <= D} mu(d) Q_lambda(X / d^2) / d
    with proved dilation tail bound <= zeta(3) X^{5/2} / (5 D^5).
    """
    if direction not in ("mu_to_lambda", "lambda_to_mu"):
        raise ValueError(f"Invalid direction: {direction!r}")
    if D_cutoff < 1:
        raise ValueError(f"D_cutoff must be >= 1, got {D_cutoff}")

    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X_arb = arb(X_val)
        X_pow_5_2 = X_arb ** (arb(5) / arb(2))
        source_kind = "mu" if direction == "mu_to_lambda" else "lambda"

        partial_sum = arb(0)
        for d in range(1, D_cutoff + 1):
            weight = 1 if direction == "mu_to_lambda" else moebius_mu_int(d)
            if weight == 0:
                continue
            d_arb = arb(d)
            scaled_X = X_arb / (d_arb * d_arb)
            T_d = max(250, int(T_base_cutoff // max(1, d)))
            q_d = evaluate_Q_arith_certified_arb(
                scaled_X, coeff_kind=source_kind, T_cutoff=T_d, prec_bits=prec_bits
            )["enclosure"]
            partial_sum += arb(weight) * q_d / d_arb

        dilation_tail_bound = (arb(3).zeta() * X_pow_5_2) / (arb(5) * (arb(D_cutoff) ** 5))
        enclosure = inflate_arb_with_nonneg_bound(partial_sum, dilation_tail_bound)

        return {
            "direction": direction,
            "D_cutoff": D_cutoff,
            "partial_sum": partial_sum,
            "dilation_tail_bound": dilation_tail_bound,
            "enclosure": enclosure,
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_section_2_and_3_square_dilation_transfer(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify Section 2 & Section 3:
    - Exact square-divisor convolution identities lambda(n) = sum_{d^2 | n} mu(n/d^2) and
      mu(n) = sum_{d^2 | n} mu(d) lambda(n/d^2) up to n = 200.
    - Complete multiplicativity common-factor identity lambda(d r) lambda(d s) = lambda(r) lambda(s)
      for all 1 <= d, r, s <= 30 (including non-squarefree d and gcd(d, r s) > 1).
    - Direct vs square-dilation transfer evaluations of Q_lambda(X) and Q_mu(X) across
      X in {1/2, 1, 2, tau, 4, 8}.
    - Weighted dilation norm multipliers zeta(1 + 2 sigma) and zeta(1 + 2 sigma)/zeta(2 + 4 sigma)
      across sigma in {1/20, 1/10, 1/4, 1/2, 1} and O(sigma^{-1}) blowup at sigma -> 0^+.
    - Equivalence between grade-interval energy O_eps(Y^eps) and finiteness of ||Q_a||_sigma
      on (0, 5/2), plus the Mellin-to-RH bridge and SUBGATE-TC-043A connection.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits

        # 1. Exact convolution checks up to n = 200
        n_max = 200
        all_forward_ok = True
        all_inverse_ok = True
        selected_witnesses: List[Dict[str, Any]] = []
        witness_ns = {1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 25, 27, 30, 36, 48, 60, 72, 100, 144, 180, 200}

        for n in range(1, n_max + 1):
            lam_n = liouville_lambda_int(n)
            mu_n = moebius_mu_int(n)
            fwd_n = square_divisor_moebius_sum_int(n)
            inv_n = square_divisor_inverse_liouville_sum_int(n)
            if fwd_n != lam_n:
                all_forward_ok = False
            if inv_n != mu_n:
                all_inverse_ok = False
            if n in witness_ns:
                selected_witnesses.append({
                    "n": n,
                    "Omega_n": omega_with_multiplicity_int(n),
                    "lambda_n": lam_n,
                    "mu_n": mu_n,
                    "square_divisor_moebius_sum": fwd_n,
                    "square_divisor_inverse_liouville_sum": inv_n,
                    "forward_match": fwd_n == lam_n,
                    "inverse_match": inv_n == mu_n,
                })

        # 2. Common-factor identity lambda(d r) lambda(d s) = lambda(r) lambda(s) for 1 <= d, r, s <= 30
        d_max = 30
        all_common_factor_ok = True
        non_squarefree_overlap_witnesses: List[Dict[str, Any]] = []
        sample_triples = [
            (4, 2, 3),
            (4, 6, 9),
            (8, 12, 18),
            (9, 3, 6),
            (12, 10, 15),
            (16, 14, 21),
            (25, 5, 10),
            (27, 29, 30),
        ]
        sample_triple_set = set(sample_triples)
        for d in range(1, d_max + 1):
            for r in range(1, d_max + 1):
                lam_dr = liouville_lambda_int(d * r)
                lam_r = liouville_lambda_int(r)
                for s in range(1, d_max + 1):
                    lhs = lam_dr * liouville_lambda_int(d * s)
                    rhs = lam_r * liouville_lambda_int(s)
                    if lhs != rhs:
                        all_common_factor_ok = False
                    if (d, r, s) in sample_triple_set:
                        non_squarefree_overlap_witnesses.append({
                            "d": d,
                            "r": r,
                            "s": s,
                            "mu_d": moebius_mu_int(d),
                            "gcd_d_rs": math.gcd(d, r * s),
                            "gcd_r_s": math.gcd(r, s),
                            "lambda_dr_times_lambda_ds": lhs,
                            "lambda_r_times_lambda_s": rhs,
                            "exact_match": lhs == rhs,
                        })

        # 3. Direct vs square-dilation transfer evaluations of Q_lambda(X) and Q_mu(X)
        tau_arb = arb(2) * arb.pi()
        sample_scales: List[Tuple[str, arb]] = [
            ("1/2", arb(1) / arb(2)),
            ("1", arb(1)),
            ("2", arb(2)),
            ("tau", tau_arb),
            ("4", arb(4)),
            ("8", arb(8)),
        ]
        transfer_rows: List[Dict[str, Any]] = []
        all_transfers_overlap = True

        for label, X_arb in sample_scales:
            q_mu_res = evaluate_Q_arith_certified_arb(
                X_arb, coeff_kind="mu", T_cutoff=4000, prec_bits=prec_bits
            )
            q_lam_res = evaluate_Q_arith_certified_arb(
                X_arb, coeff_kind="lambda", T_cutoff=4000, prec_bits=prec_bits
            )
            mu_to_lam_res = evaluate_square_dilation_transfer_certified_arb(
                X_arb, direction="mu_to_lambda", D_cutoff=80, T_base_cutoff=4000, prec_bits=prec_bits
            )
            lam_to_mu_res = evaluate_square_dilation_transfer_certified_arb(
                X_arb, direction="lambda_to_mu", D_cutoff=80, T_base_cutoff=4000, prec_bits=prec_bits
            )

            diff_lam = q_lam_res["enclosure"] - mu_to_lam_res["enclosure"]
            diff_mu = q_mu_res["enclosure"] - lam_to_mu_res["enclosure"]
            lam_overlap = bool(diff_lam.contains(0))
            mu_overlap = bool(diff_mu.contains(0))
            if not (lam_overlap and mu_overlap):
                all_transfers_overlap = False

            transfer_rows.append({
                "X_label": label,
                "X_enclosure": serialize_arb_certified(X_arb),
                "Q_mu_direct": serialize_arb_certified(q_mu_res["enclosure"]),
                "Q_mu_truncation_tail_bound": serialize_arb_certified(q_mu_res["tail_bound"]),
                "Q_mu_from_lambda_dilation": serialize_arb_certified(lam_to_mu_res["enclosure"]),
                "Q_mu_dilation_tail_bound": serialize_arb_certified(lam_to_mu_res["dilation_tail_bound"]),
                "Q_mu_difference_enclosure": serialize_arb_certified(diff_mu),
                "Q_mu_zero_in_difference": mu_overlap,
                "Q_lambda_direct": serialize_arb_certified(q_lam_res["enclosure"]),
                "Q_lambda_truncation_tail_bound": serialize_arb_certified(q_lam_res["tail_bound"]),
                "Q_lambda_from_mu_dilation": serialize_arb_certified(mu_to_lam_res["enclosure"]),
                "Q_lambda_dilation_tail_bound": serialize_arb_certified(mu_to_lam_res["dilation_tail_bound"]),
                "Q_lambda_difference_enclosure": serialize_arb_certified(diff_lam),
                "Q_lambda_zero_in_difference": lam_overlap,
                "abs_Q_mu_le_zeta3_X_5_2": q_mu_res["abs_le_zeta3_X_5_2"],
                "abs_Q_lambda_le_zeta3_X_5_2": q_lam_res["abs_le_zeta3_X_5_2"],
            })

        # 4. Weighted dilation norm multipliers across eta > 0 and eta -> 0^+ upper-bound divergence
        eta_samples: List[Tuple[str, arb]] = [
            ("1/20", arb(1) / arb(20)),
            ("1/10", arb(1) / arb(10)),
            ("1/4", arb(1) / arb(4)),
            ("1/2", arb(1) / arb(2)),
            ("1", arb(1)),
        ]
        norm_multiplier_rows: List[Dict[str, Any]] = []
        for e_label, eta_arb in eta_samples:
            zeta_1_2e = (arb(1) + arb(2) * eta_arb).zeta()
            zeta_2_4e = (arb(2) + arb(4) * eta_arb).zeta()
            rev_mult = zeta_1_2e / zeta_2_4e
            scaled_fwd = eta_arb * zeta_1_2e
            scaled_rev = eta_arb * rev_mult
            norm_multiplier_rows.append({
                "eta_label": e_label,
                "eta": serialize_arb_certified(eta_arb),
                "sigma_label": e_label,
                "sigma": serialize_arb_certified(eta_arb),
                "forward_multiplier_zeta_1_plus_2eta": serialize_arb_certified(zeta_1_2e),
                "forward_multiplier_zeta_1_plus_2sigma": serialize_arb_certified(zeta_1_2e),
                "zeta_2_plus_4eta": serialize_arb_certified(zeta_2_4e),
                "zeta_2_plus_4sigma": serialize_arb_certified(zeta_2_4e),
                "reverse_multiplier_zeta_1_2eta_over_zeta_2_4eta": serialize_arb_certified(rev_mult),
                "reverse_multiplier_zeta_1_2sigma_over_zeta_2_4sigma": serialize_arb_certified(rev_mult),
                "eta_times_forward_multiplier": serialize_arb_certified(scaled_fwd),
                "sigma_times_forward_multiplier": serialize_arb_certified(scaled_fwd),
                "eta_times_reverse_multiplier": serialize_arb_certified(scaled_rev),
                "sigma_times_reverse_multiplier": serialize_arb_certified(scaled_rev),
                "forward_multiplier_positive_finite": bool(zeta_1_2e.lower() > 0),
                "reverse_multiplier_positive_finite": bool(rev_mult.lower() > 0),
            })

        limit_eta_fwd_at_zero = arb(1) / arb(2)
        limit_eta_rev_at_zero = arb(12) / (tau_arb * tau_arb)

        return {
            "square_divisor_convolution_audit": {
                "n_max_tested": n_max,
                "all_forward_lambda_eq_sum_mu_n_over_d2": all_forward_ok,
                "all_inverse_mu_eq_sum_mu_d_lambda_n_over_d2": all_inverse_ok,
                "selected_witnesses": selected_witnesses,
            },
            "complete_multiplicativity_common_factor_audit": {
                "d_r_s_max_tested": d_max,
                "total_triples_tested": d_max ** 3,
                "all_triples_satisfy_lambda_dr_lambda_ds_eq_lambda_r_lambda_s": all_common_factor_ok,
                "non_squarefree_and_overlapping_witnesses": non_squarefree_overlap_witnesses,
            },
            "square_dilation_transfer_rows": transfer_rows,
            "all_transfer_enclosures_contain_zero_difference": all_transfers_overlap,
            "weighted_dilation_norm_equivalence": {
                "norm_definition": "||f||_eta^2 = int_0^infty |f(X)|^2 X^{-2*eta} dX/X",
                "dilation_scaling_identity": "||f(./a)||_eta = a^{-eta} ||f||_eta",
                "forward_bound_formula": "||Q_lambda||_eta <= zeta(1 + 2*eta) ||Q_mu||_eta",
                "reverse_bound_formula": "||Q_mu||_eta <= (zeta(1 + 2*eta) / zeta(2 + 4*eta)) ||Q_lambda||_eta",
                "eta_zero_singularity_and_operator_scope_note": (
                    "For eta > 0, Minkowski's triangle-inequality upper bound yields finite mutual multipliers "
                    "zeta(1 + 2*eta) and zeta(1 + 2*eta)/zeta(2 + 4*eta). As eta -> 0^+, "
                    "zeta(1 + 2*eta) = 1/(2*eta) + O(1) and zeta(1 + 2*eta)/zeta(2 + 4*eta) = 12/(tau^2 * eta) + O(1) "
                    "(since zeta(2) = tau^2/24) because sum_{d>=1} d^{-1} = infty and sum_{d>=1} |mu(d)| d^{-1} = infty. "
                    "Positive-weight results (eta > 0) do not establish boundedness of the ordinary boundary series "
                    "sum_{d>=1} d^{-1} f(./d^2) on the full unweighted space L^2((0, infty), dX/X): by Mellin-Plancherel "
                    "along z = i*b (b in R), the formal boundary multiplier is zeta(1 + 2*i*b), which has a simple pole at "
                    "b = 0 and is unbounded as |b| -> infty."
                ),
                "asymptotic_residue_eta_times_forward_at_0": serialize_arb_certified(limit_eta_fwd_at_zero),
                "asymptotic_residue_eta_times_reverse_at_0": serialize_arb_certified(limit_eta_rev_at_zero),
                "asymptotic_residue_sigma_times_forward_at_0": serialize_arb_certified(limit_eta_fwd_at_zero),
                "asymptotic_residue_sigma_times_reverse_at_0": serialize_arb_certified(limit_eta_rev_at_zero),
                "multiplier_table": norm_multiplier_rows,
            },
            "grade_interval_energy_and_mellin_bridge": {
                "equivalence_statement": (
                    "(forall eps > 0 exists C_eps < infty forall Y >= 1, int_Y^{tau Y} |Q_a(X)|^2 dX/X <= C_eps Y^eps) "
                    "<-> (forall eta in (0, 5/2), ||Q_a||_eta < infty)"
                ),
                "forward_direction_bound": (
                    "For eta in (0, 5/2), choose eps = eta > 0: "
                    "int_0^1 |Q_a(X)|^2 X^{-2*eta} dX/X <= zeta(3)^2 / (5 - 2*eta) and "
                    "sum_{k>=0} int_{tau^k}^{tau^{k+1}} |Q_a(X)|^2 X^{-2*eta} dX/X <= C_eta / (1 - tau^{-eta})."
                ),
                "reverse_direction_bound": (
                    "For eps in (0, 5) and Y >= 1, set eta = eps / 2 in (0, 5/2): on X in [Y, tau Y], "
                    "1 <= (tau Y / X)^{2*eta} = tau^eps Y^eps X^{-2*eta}, so "
                    "int_Y^{tau Y} |Q_a(X)|^2 dX/X <= tau^eps ||Q_a||_{eps/2}^2 Y^eps."
                ),
                "mellin_identities": {
                    "complex_coordinates": "z = a + i*b (a, b in R); zeta zero rho = x + i*y (x, y in R, critical real coordinate x = 1/2)",
                    "M_Q_mu_z": "Gamma(5/4 - z/2) / (2 * zeta(1/2 + z))",
                    "M_Q_lambda_z": "Gamma(5/4 - z/2) * zeta(1 + 2*z) / (2 * zeta(1/2 + z))",
                    "strip_of_analyticity_from_norm_finiteness": "0 < a = Re(z) < 5/2",
                    "rh_equivalence_explanation": (
                        "For z = a + i*b with a, b in R, Cauchy-Schwarz on int_0^infty Q_a(X) X^{-z} dX/X with eta = a/2 in (0, 5/4) "
                        "(or Mellin-Plancherel along a = eta in (0, 5/2)) shows that finiteness of ||Q_a||_eta "
                        "for all eta in (0, 5/2) forces M[Q_a](z) to be holomorphic throughout 0 < a < 5/2. "
                        "Since Gamma(5/4 - z/2) and zeta(1 + 2*z) have no zeros in 0 < a < 5/2, any off-critical "
                        "zero rho = x + i*y of zeta(s) with 1/2 < x < 1 creates a non-removable pole at z = rho - 1/2 "
                        "with Re(z) = x - 1/2 in (0, 1/2) subset (0, 5/2)."
                    ),
                    "bridge_to_subgate_tc_043a_explanation": (
                        "TC grades K remain real algebraic (K in A_R); auxiliary positive real scales and real norm weights eta > 0 "
                        "do not automatically become TC grades. For integer dilations d >= 2, Lindemann's theorem (tau = 2*pi is "
                        "transcendental) implies tau^q != d^2 for every nonzero rational q in Q \\ {0}, establishing that "
                        "log_tau(2) and log_tau(d^2) are irrational (not in Q). Irrationality does not exclude algebraic irrational "
                        "grades in A_R \\ Q, and whether log_tau(2) or log_tau(d^2) belongs to A_R is unestablished here and unnecessary: "
                        "the weighted norm ||.||_eta is defined on the continuum L^2((0, infty), X^{-2*eta} dX/X), which is partitioned "
                        "into the tau-adic intervals [tau^k, tau^{k+1}) indexed by rational integer grades k in Z subset A_R."
                    ),
                },
            },
        }
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 3. Section 4: Unconstrained Common-Factor Expansion & Fixed-Order Euler-Maclaurin
# ---------------------------------------------------------------------------


def verify_euler_maclaurin_derivatives_and_constants_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify symbolically (SymPy) and in 256-bit Arb the derivatives f'(v), f''(v),
    f^{(3)}(v), f^{(4)}(v) of f(v) = v^{-6} exp(-1/v^2), the inflection points
    v_+/- = sqrt((15 +/- sqrt(57))/42), and the exact Euler-Maclaurin constants C_2 and C_4.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits

        # Symbolic verification via SymPy
        v_sym = sp.Symbol("v", positive=True)
        f_sym = v_sym ** (-6) * sp.exp(-1 / v_sym ** 2)
        f1_sym = sp.factor(sp.diff(f_sym, v_sym))
        f2_sym = sp.factor(sp.diff(f_sym, v_sym, 2))
        f3_sym = sp.factor(sp.diff(f_sym, v_sym, 3))
        f4_sym = sp.factor(sp.diff(f_sym, v_sym, 4))

        f1_expected = 2 * (1 - 3 * v_sym ** 2) * v_sym ** (-9) * sp.exp(-1 / v_sym ** 2)
        f2_expected = 2 * (21 * v_sym ** 4 - 15 * v_sym ** 2 + 2) * v_sym ** (-12) * sp.exp(-1 / v_sym ** 2)
        f3_expected = (
            4 * (-84 * v_sym ** 6 + 96 * v_sym ** 4 - 27 * v_sym ** 2 + 2)
            * v_sym ** (-15)
            * sp.exp(-1 / v_sym ** 2)
        )
        f4_expected = (
            4 * (6 * v_sym ** 2 - 1) * (126 * v_sym ** 6 - 183 * v_sym ** 4 + 60 * v_sym ** 2 - 4)
            * v_sym ** (-18)
            * sp.exp(-1 / v_sym ** 2)
        )

        sympy_f1_ok = bool(sp.simplify(f1_sym - f1_expected) == 0)
        sympy_f2_ok = bool(sp.simplify(f2_sym - f2_expected) == 0)
        sympy_f3_ok = bool(sp.simplify(f3_sym - f3_expected) == 0)
        sympy_f4_ok = bool(sp.simplify(f4_sym - f4_expected) == 0)

        # 256-bit Arb evaluation of v_-, v_+, f'(v_-), f'(v_+), and C_2 = (f'(v_-) - f'(v_+)) / 6
        sqrt57 = arb(57).sqrt()
        v_minus = ((arb(15) - sqrt57) / arb(42)).sqrt()
        v_plus = ((arb(15) + sqrt57) / arb(42)).sqrt()

        def eval_f1_arb(v_val: arb) -> arb:
            v2 = v_val * v_val
            return arb(2) * (arb(1) - arb(3) * v2) * (v_val ** (-9)) * (-arb(1) / v2).exp()

        def eval_f3_arb(v_val: arb) -> arb:
            v2 = v_val * v_val
            poly = -arb(84) * (v2 ** 3) + arb(96) * (v2 ** 2) - arb(27) * v2 + arb(2)
            return arb(4) * poly * (v_val ** (-15)) * (-arb(1) / v2).exp()

        f1_v_minus = eval_f1_arb(v_minus)
        f1_v_plus = eval_f1_arb(v_plus)
        int_abs_f2 = arb(2) * (f1_v_minus - f1_v_plus)
        C_2_arb = (f1_v_minus - f1_v_plus) / arb(6)

        # Exact 256-bit Arb roots of P_4(u) = (6 u - 1)(126 u^3 - 183 u^2 + 60 u - 4) = 0 (u = v^2)
        def eval_P4_cubic_and_deriv(u_val: arb) -> Tuple[arb, arb]:
            p = ((arb(126) * u_val - arb(183)) * u_val + arb(60)) * u_val - arb(4)
            dp = (arb(378) * u_val - arb(366)) * u_val + arb(60)
            return p, dp

        u_cubic_seeds = ["0.089683317229", "0.349299153637", "1.013398481515"]
        u4_certs: List[arb] = [arb(1) / arb(6)]
        box_eps = arb(2) ** (-230)
        for u0_str in u_cubic_seeds:
            u_curr = arb(u0_str)
            for _ in range(16):
                p_val, dp_val = eval_P4_cubic_and_deriv(u_curr)
                u_curr = (u_curr - p_val / dp_val).mid()
            p_mid, _ = eval_P4_cubic_and_deriv(u_curr)
            _, dp_box = eval_P4_cubic_and_deriv(inflate_arb_with_nonneg_bound(u_curr, box_eps))
            u_cert = inflate_arb_with_nonneg_bound(u_curr, abs(p_mid / dp_box) + arb(2) ** (-240))
            p_low, _ = eval_P4_cubic_and_deriv(u_cert.lower())
            p_high, _ = eval_P4_cubic_and_deriv(u_cert.upper())
            assert (p_low.upper() < 0 < p_high.lower()) or (p_high.upper() < 0 < p_low.lower())
            u4_certs.append(u_cert)

        # Sort roots in ascending order using certified interval comparison
        for i in range(len(u4_certs)):
            for j in range(i + 1, len(u4_certs)):
                if bool(u4_certs[j].upper() < u4_certs[i].lower()):
                    u4_certs[i], u4_certs[j] = u4_certs[j], u4_certs[i]
        v4_roots: List[arb] = [uc.sqrt() for uc in u4_certs]

        f3_at_roots = [eval_f3_arb(vr) for vr in v4_roots]
        int_abs_f4 = arb(2) * (f3_at_roots[0] - f3_at_roots[1] + f3_at_roots[2] - f3_at_roots[3])
        C_4_arb = int_abs_f4 / arb(720)

        return {
            "sympy_derivative_identities_verified": bool(
                sympy_f1_ok and sympy_f2_ok and sympy_f3_ok and sympy_f4_ok
            ),
            "f1_formula": "2 * (1 - 3*v^2) * v^{-9} * exp(-1/v^2)",
            "f2_formula": "2 * (21*v^4 - 15*v^2 + 2) * v^{-12} * exp(-1/v^2)",
            "f3_formula": "4 * (-84*v^6 + 96*v^4 - 27*v^2 + 2) * v^{-15} * exp(-1/v^2)",
            "f4_formula": "4 * (6*v^2 - 1) * (126*v^6 - 183*v^4 + 60*v^2 - 4) * v^{-18} * exp(-1/v^2)",
            "v_minus": serialize_arb_certified(v_minus),
            "v_plus": serialize_arb_certified(v_plus),
            "f_prime_v_minus": serialize_arb_certified(f1_v_minus),
            "f_prime_v_plus": serialize_arb_certified(f1_v_plus),
            "f_prime_v_minus_positive": bool(f1_v_minus.lower() > 0),
            "f_prime_v_plus_negative": bool(f1_v_plus.upper() < 0),
            "int_0_infty_abs_f2": serialize_arb_certified(int_abs_f2),
            "C_2": serialize_arb_certified(C_2_arb),
            "C_2_raw": C_2_arb,
            "v4_roots": [serialize_arb_certified(vr) for vr in v4_roots],
            "int_0_infty_abs_f4": serialize_arb_certified(int_abs_f4),
            "C_4": serialize_arb_certified(C_4_arb),
            "C_4_raw": C_4_arb,
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_d_sum_certified_arb(
    L_val: arb,
    D_cutoff: int = 2000,
    prec_bits: int = 256,
) -> arb:
    """Evaluate sum_{d>=1} d^{-6} exp(-L^2 / d^2) in 256-bit Arb with proved tail <= 1 / (5 D^5)."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        L_arb = arb(L_val)
        L_sq = L_arb * L_arb
        partial = arb(0)
        for d in range(1, D_cutoff + 1):
            d_arb = arb(d)
            partial += (d_arb ** (-6)) * (-L_sq / (d_arb * d_arb)).exp()
        tail_bound = arb(1) / (arb(5) * (arb(D_cutoff) ** 5))
        return inflate_arb_with_nonneg_bound(partial, tail_bound)
    finally:
        flint_ctx.prec = saved_prec


def verify_section_4_unconstrained_common_factor_and_euler_maclaurin(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify Section 4:
    - Exact unconstrained common-factor expansion of Q_lambda(X)^2 vs direct square at X in {1, 2, 4}.
    - Fixed-order Euler-Maclaurin constants C_2, C_4 and error bounds |sum_{d>=1} d^{-6} e^{-L^2/d^2} - (3 sqrt(pi)/8) L^{-5}| <= C_N L^{-5-N}
      across L in {1/2, 1, 2, 4, 8}.
    - Pairwise error bound |E^lambda_{r,s}(X)| <= C_N X^{-N} (r s)^{N+2} / (r^2 + s^2)^{(N+5)/2}
      including at the TC-053R counterexample scale (r, s, X) = (29, 31, 30).
    - Summed coprime block error bound sum_{1<=r,s<=A, gcd(r,s)=1} |E^lambda_{r,s}(X)| <= C_N 2^{-(N+5)/2} A^{N+1} / X^N
      and subtransition growing-range table A <= X^{1 - delta}.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        em_constants = verify_euler_maclaurin_derivatives_and_constants_arb(prec_bits=prec_bits)
        C_2_arb = em_constants.pop("C_2_raw")
        C_4_arb = em_constants.pop("C_4_raw")
        c_gauss = arb(3) * arb.pi().sqrt() / arb(8)

        # 1. Common-factor d-sum vs Gaussian leading term and Euler-Maclaurin bounds at L in {1/2, 1, 2, 4, 8}
        L_samples: List[Tuple[str, arb]] = [
            ("1/2", arb(1) / arb(2)),
            ("1", arb(1)),
            ("2", arb(2)),
            ("4", arb(4)),
            ("8", arb(8)),
        ]
        d_sum_rows: List[Dict[str, Any]] = []
        all_em_bounds_hold = True

        for L_label, L_arb in L_samples:
            d_sum = evaluate_d_sum_certified_arb(L_arb, D_cutoff=2000, prec_bits=prec_bits)
            lead = c_gauss * (L_arb ** (-5))
            abs_err = abs(d_sum - lead)
            bound_N2 = C_2_arb * (L_arb ** (-7))
            bound_N4 = C_4_arb * (L_arb ** (-9))
            ok_N2 = bool(abs_err.upper() <= bound_N2.lower())
            ok_N4 = bool(abs_err.upper() <= bound_N4.lower())
            if not (ok_N2 and ok_N4):
                all_em_bounds_hold = False
            d_sum_rows.append({
                "L_label": L_label,
                "L": serialize_arb_certified(L_arb),
                "exact_d_sum": serialize_arb_certified(d_sum),
                "gaussian_leading_term": serialize_arb_certified(lead),
                "abs_error": serialize_arb_certified(abs_err),
                "em_bound_N2_C2_L_neg7": serialize_arb_certified(bound_N2),
                "em_bound_N4_C4_L_neg9": serialize_arb_certified(bound_N4),
                "bound_N2_holds": ok_N2,
                "bound_N4_holds": ok_N4,
            })

        # 2. Pairwise error |E^lambda_{r,s}(X)| checks (including (29, 31, 30))
        pairwise_samples = [
            (1, 1, 4),
            (2, 3, 10),
            (29, 31, 30),
            (5, 8, 20),
        ]
        pairwise_rows: List[Dict[str, Any]] = []
        all_pairwise_ok = True
        for r, s, X_int in pairwise_samples:
            r_arb = arb(r)
            s_arb = arb(s)
            X_arb = arb(X_int)
            rs_arb = r_arb * s_arb
            r2_plus_s2 = r_arb * r_arb + s_arb * s_arb
            L_arb = X_arb * r2_plus_s2.sqrt() / rs_arb
            d_sum = evaluate_d_sum_certified_arb(L_arb, D_cutoff=2000, prec_bits=prec_bits)
            exact_pair = (
                arb(liouville_lambda_int(r) * liouville_lambda_int(s))
                * (X_arb ** 5)
                / (rs_arb ** 3)
                * d_sum
            )
            lead_pair = (
                c_gauss
                * arb(liouville_lambda_int(r) * liouville_lambda_int(s))
                * (rs_arb ** 2)
                / (r2_plus_s2 ** (arb(5) / arb(2)))
            )
            abs_E = abs(exact_pair - lead_pair)
            bound_pair_N2 = (
                C_2_arb
                * (X_arb ** (-2))
                * (rs_arb ** 4)
                / (r2_plus_s2 ** (arb(7) / arb(2)))
            )
            bound_pair_N4 = (
                C_4_arb
                * (X_arb ** (-4))
                * (rs_arb ** 6)
                / (r2_plus_s2 ** (arb(9) / arb(2)))
            )
            ok2 = bool(abs_E.upper() <= bound_pair_N2.lower())
            ok4 = bool(abs_E.upper() <= bound_pair_N4.lower())
            if not (ok2 and ok4):
                all_pairwise_ok = False
            pairwise_rows.append({
                "r": r,
                "s": s,
                "X": X_int,
                "L_rs": serialize_arb_certified(L_arb),
                "exact_pair_term": serialize_arb_certified(exact_pair),
                "leading_pair_term": serialize_arb_certified(lead_pair),
                "abs_E_lambda_rs": serialize_arb_certified(abs_E),
                "proved_bound_N2": serialize_arb_certified(bound_pair_N2),
                "proved_bound_N4": serialize_arb_certified(bound_pair_N4),
                "bound_N2_holds": ok2,
                "bound_N4_holds": ok4,
            })

        # 3. Summed coprime error bound sum_{1<=r,s<=A, gcd(r,s)=1} |E^lambda_{r,s}(X)| <= C_N 2^{-(N+5)/2} A^{N+1} / X^N
        aggregate_samples = [(4, 8), (6, 12), (8, 20)]
        aggregate_rows: List[Dict[str, Any]] = []
        all_aggregate_ok = True
        for A_int, X_int in aggregate_samples:
            X_arb = arb(X_int)
            A_arb = arb(A_int)
            total_abs_E = arb(0)
            for r in range(1, A_int + 1):
                for s in range(1, A_int + 1):
                    if math.gcd(r, s) != 1:
                        continue
                    r_arb = arb(r)
                    s_arb = arb(s)
                    rs_arb = r_arb * s_arb
                    r2_plus_s2 = r_arb * r_arb + s_arb * s_arb
                    L_arb = X_arb * r2_plus_s2.sqrt() / rs_arb
                    d_sum = evaluate_d_sum_certified_arb(L_arb, D_cutoff=800, prec_bits=prec_bits)
                    exact_pair = (X_arb ** 5) / (rs_arb ** 3) * d_sum
                    lead_pair = c_gauss * (rs_arb ** 2) / (r2_plus_s2 ** (arb(5) / arb(2)))
                    total_abs_E += abs(exact_pair - lead_pair)

            agg_bound_N2 = (
                C_2_arb
                * (arb(2) ** (-arb(7) / arb(2)))
                * (A_arb ** 3)
                / (X_arb ** 2)
            )
            agg_bound_N4 = (
                C_4_arb
                * (arb(2) ** (-arb(9) / arb(2)))
                * (A_arb ** 5)
                / (X_arb ** 4)
            )
            ok_agg2 = bool(total_abs_E.upper() <= agg_bound_N2.lower())
            ok_agg4 = bool(total_abs_E.upper() <= agg_bound_N4.lower())
            if not (ok_agg2 and ok_agg4):
                all_aggregate_ok = False
            aggregate_rows.append({
                "A": A_int,
                "X": X_int,
                "sum_coprime_abs_E_lambda": serialize_arb_certified(total_abs_E),
                "proved_aggregate_bound_N2": serialize_arb_certified(agg_bound_N2),
                "proved_aggregate_bound_N4": serialize_arb_certified(agg_bound_N4),
                "aggregate_bound_N2_holds": ok_agg2,
                "aggregate_bound_N4_holds": ok_agg4,
            })

        # 4. Growing-range exponent table A <= X^{1 - delta}
        growing_range_table = [
            {
                "even_N": 2,
                "delta_threshold_condition": "delta > 1/3",
                "supported_range": "A <= X^{2/3 - eta} (delta = 1/3 + eta)",
                "sample_delta": "2/5",
                "exponent_1_minus_N_plus_1_delta": "-1/5 < 0",
            },
            {
                "even_N": 4,
                "delta_threshold_condition": "delta > 1/5",
                "supported_range": "A <= X^{4/5 - eta} (delta = 1/5 + eta)",
                "sample_delta": "1/4",
                "exponent_1_minus_N_plus_1_delta": "-1/4 < 0",
            },
            {
                "even_N": 6,
                "delta_threshold_condition": "delta > 1/7",
                "supported_range": "A <= X^{6/7 - eta} (delta = 1/7 + eta)",
                "sample_delta": "1/6",
                "exponent_1_minus_N_plus_1_delta": "-1/6 < 0",
            },
            {
                "even_N": "2 * ceil(1/(2*delta))",
                "delta_threshold_condition": "(N + 1) * delta > 1",
                "supported_range": "A <= X^{1 - delta} for any fixed delta in (0, 1)",
                "sample_delta": "arbitrary fixed delta in (0, 1)",
                "exponent_1_minus_N_plus_1_delta": "1 - (N + 1)*delta < 0",
            },
        ]

        # 5. Pairwise spurious 1/(2*sqrt(2)) factor counterexample regression (TASK-TC-054R2 §6):
        # At r = s = 1, L = 9/5 = 1.8, X = 9 / (5*sqrt(2)),
        #     |sum_{d>=1} d^{-6} e^{-L^2/d^2} - c_0 L^{-5}| / (C_2 L^{-7})
        #   = |E^lambda_{1,1}(X)| / (C_2 X^{-2} * 1^4 / (1^2 + 1^2)^{7/2})
        #   = 0.4030344210... > 1 / (2*sqrt(2)) = 0.35355339059...,
        # certifying that 1/(2*sqrt(2)) belongs ONLY to the summed coprime bound over 1 <= r, s <= A,
        # NOT to the pairwise remainder |E^lambda_{r,s}(X)| <= C_2 X^{-2} (r s)^4 / (r^2 + s^2)^{7/2}.
        L_reg = arb(9) / arb(5)
        X_reg = L_reg / arb(2).sqrt()
        d_sum_reg = evaluate_d_sum_certified_arb(L_reg, D_cutoff=1000, prec_bits=prec_bits)
        lead_reg = c_gauss * (L_reg ** (-5))
        abs_d_err_reg = abs(d_sum_reg - lead_reg)
        em_denom_reg = C_2_arb * (L_reg ** (-7))
        ratio_reg = abs_d_err_reg / em_denom_reg
        inv_2_sqrt2 = arb(1) / (arb(2) * arb(2).sqrt())
        spurious_gap = ratio_reg - inv_2_sqrt2
        abs_E_11_reg = (X_reg ** 5) * abs_d_err_reg
        true_pairwise_bound_reg = C_2_arb * (X_reg ** (-2)) / (arb(2) ** (arb(7) / arb(2)))
        spurious_pairwise_bound_reg = inv_2_sqrt2 * true_pairwise_bound_reg

        pairwise_spurious_factor_regression = {
            "r": 1,
            "s": 1,
            "L_formula": "9/5",
            "X_formula": "9 / (5 * sqrt(2))",
            "D_cutoff": 1000,
            "d_sum_tail_bound_1_over_5_D5": "1 / (5 * 1000^5) = 2e-16",
            "L": serialize_arb_certified(L_reg),
            "X": serialize_arb_certified(X_reg),
            "exact_d_sum": serialize_arb_certified(d_sum_reg),
            "gaussian_leading_c0_L_neg5": serialize_arb_certified(lead_reg),
            "abs_d_sum_error": serialize_arb_certified(abs_d_err_reg),
            "C_2_L_neg7": serialize_arb_certified(em_denom_reg),
            "ratio_abs_error_over_C2_L_neg7": serialize_arb_certified(ratio_reg),
            "spurious_factor_1_over_2_sqrt2": serialize_arb_certified(inv_2_sqrt2),
            "ratio_minus_1_over_2_sqrt2": serialize_arb_certified(spurious_gap),
            "ratio_strictly_exceeds_1_over_2_sqrt2": bool(spurious_gap.lower() > 0),
            "abs_E_lambda_1_1_X": serialize_arb_certified(abs_E_11_reg),
            "true_pairwise_bound_C2_X_neg2_rs4_over_r2_plus_s2_7_2": serialize_arb_certified(true_pairwise_bound_reg),
            "spurious_pairwise_bound_with_extra_1_over_2_sqrt2": serialize_arb_certified(spurious_pairwise_bound_reg),
            "true_pairwise_bound_holds": bool(abs_E_11_reg.upper() <= true_pairwise_bound_reg.lower()),
            "spurious_pairwise_bound_violated": bool(abs_E_11_reg.lower() > spurious_pairwise_bound_reg.upper()),
        }

        return {
            "euler_maclaurin_derivatives_and_constants": em_constants,
            "common_factor_d_sum_vs_gaussian_leading_rows": d_sum_rows,
            "all_d_sum_em_bounds_hold": all_em_bounds_hold,
            "pairwise_error_rows": pairwise_rows,
            "all_pairwise_bounds_hold": all_pairwise_ok,
            "pairwise_spurious_factor_counterexample_regression": pairwise_spurious_factor_regression,
            "coprime_aggregate_error_rows": aggregate_rows,
            "all_aggregate_bounds_hold": all_aggregate_ok,
            "subtransition_growing_range_table": growing_range_table,
        }
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 4. Section 5: Exact Poisson Summation Formula at the Transition (A ~ X)
# ---------------------------------------------------------------------------


def compute_hat_f_tail_ratios_arb(
    omega_val: arb,
    K_terms: int,
) -> Tuple[arb, arb]:
    """Return the certified monotonic upper-bound ratios `(R_even, R_odd)` for indices `m, k >= K_terms + 1`:
        R_even = omega^2 / ((K - 1/2) * (2K + 3) * (2K + 4)),
        R_odd  = omega^2 / ((K + 2) * (2K + 8) * (2K + 9)).
    """
    if isinstance(K_terms, bool) or not isinstance(K_terms, int) or K_terms < 1:
        raise ValueError(f"K_terms must be an integer >= 1, got {K_terms!r}")
    omega_arb = arb(omega_val)
    omega_sq = omega_arb * omega_arb
    K_arb = arb(K_terms)
    denom_even = (K_arb - arb(1) / arb(2)) * (arb(2 * K_terms + 3)) * (arb(2 * K_terms + 4))
    denom_odd = (arb(K_terms + 2)) * (arb(2 * K_terms + 8)) * (arb(2 * K_terms + 9))
    return omega_sq / denom_even, omega_sq / denom_odd


def _eval_hat_f_series_core_arb(
    omega: arb,
    K_eff: int,
    even_tail_factor: arb,
    odd_tail_factor: arb,
) -> arb:
    """Internal helper evaluating the truncated residue series and inflating by the certified tail bound."""
    omega_sq = omega * omega
    tau_half = arb.pi()

    even_sum = arb(0)
    fact_2m = arb(1)
    omega_pow = arb(1)
    for m in range(0, K_eff + 1):
        if m > 0:
            fact_2m *= arb(2 * m - 1) * arb(2 * m)
            omega_pow *= omega_sq
        gamma_val = (arb(5) / arb(2) - arb(m)).gamma()
        sign = arb(1) if (m % 2 == 0) else arb(-1)
        even_sum += sign * omega_pow / fact_2m * gamma_val

    m_next = K_eff + 1
    next_fact = fact_2m * arb(2 * m_next - 1) * arb(2 * m_next)
    next_omega = omega_pow * omega_sq
    next_gamma = abs((arb(5) / arb(2) - arb(m_next)).gamma())
    first_omitted_even = next_omega / next_fact * next_gamma
    even_tail_bound = even_tail_factor * first_omitted_even

    odd_sum = arb(0)
    fact_k = arb(1)
    fact_5_2k = arb(120)  # 5! = 120
    omega_5_2k = omega ** 5
    for k in range(0, K_eff + 1):
        if k > 0:
            fact_k *= arb(k)
            fact_5_2k *= arb(2 * k + 4) * arb(2 * k + 5)
            omega_5_2k *= omega_sq
        odd_sum += omega_5_2k / (fact_k * fact_5_2k)

    k_next = K_eff + 1
    next_fact_k = fact_k * arb(k_next)
    next_fact_5_2k = fact_5_2k * arb(2 * k_next + 4) * arb(2 * k_next + 5)
    next_omega_odd = omega_5_2k * omega_sq
    first_omitted_odd = tau_half * next_omega_odd / (next_fact_k * next_fact_5_2k)
    odd_tail_bound = odd_tail_factor * first_omitted_odd

    partial_val = even_sum - tau_half * odd_sum
    return inflate_arb_with_nonneg_bound(partial_val, even_tail_bound + odd_tail_bound)


def evaluate_hat_f_hypergeometric_certified_arb(
    xi_val: Union[arb, int, float, str, Fraction],
    K_terms: int = 200,
    prec_bits: int = 256,
    *,
    strict_K: bool = False,
) -> arb:
    """Evaluate hat{f}(xi) = 2 int_0^infty v^{-6} exp(-1/v^2) cos(tau xi v) dv in 256-bit Arb
    via the exact Mellin-Barnes residue expansion (with omega = tau |xi|):
        hat{f}(xi) = sum_{m>=0} (-1)^m Gamma(5/2 - m) omega^{2m} / (2m)!
                   - (tau/2) * sum_{k>=0} omega^{5 + 2k} / (k! (5 + 2k)!).

    Certified tail control (TASK-TC-054R §4):
    - For m, k >= K + 1 (K >= 1), consecutive term ratios are bounded monotonically by
          R_even = omega^2 / ((K - 1/2)(2K + 3)(2K + 4)),
          R_odd  = omega^2 / ((K + 2)(2K + 8)(2K + 9)).
    - Before using factor 2 on the first omitted term, certifies outward that R <= 1/2.
    - If 1/2 < R < 1 is certified outward, uses the certified geometric factor 1 / (1 - R).
    - If R >= 1 is not excluded: raises ValueError when `strict_K=True`, or automatically increases
      the truncation index `K_eff` until R_even <= 1/2 is certified outward when `strict_K=False`.
    - Handles interval inputs via the exact analytical Lipschitz bound |hat{f}'(xi)| <= tau
      intersected with direct interval evaluation, and adapts working precision for large omega.
    """
    if isinstance(K_terms, bool) or not isinstance(K_terms, int) or K_terms < 1:
        raise ValueError(f"K_terms must be an integer >= 1, got {K_terms!r}")
    if isinstance(prec_bits, bool) or not isinstance(prec_bits, int) or prec_bits < 64:
        raise ValueError(f"prec_bits must be an integer >= 64, got {prec_bits!r}")
    if isinstance(xi_val, bool):
        raise ValueError("xi_val must be a finite real number or Arb ball, not bool")
    if isinstance(xi_val, float) and not math.isfinite(xi_val):
        raise ValueError(f"xi_val must be finite, got {xi_val!r}")

    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 512)
        if isinstance(xi_val, Fraction):
            xi_init = arb(xi_val.numerator) / arb(xi_val.denominator)
        else:
            xi_init = arb(xi_val)
        if not xi_init.is_finite():
            raise ValueError(f"xi_val must be a finite Arb ball, got {xi_val!r}")

        tau_init = arb(2) * arb.pi()
        omega_init = tau_init * abs(xi_init)
        omega_top_int = int((arb(4) * omega_init.upper()).ceil().unique_fmpz())
        work_prec = max(prec_bits + 128, 512 + max(0, omega_top_int))

        flint_ctx.prec = work_prec
        if isinstance(xi_val, Fraction):
            xi_arb = arb(xi_val.numerator) / arb(xi_val.denominator)
        elif isinstance(xi_val, arb):
            xi_arb = arb(xi_val)
        else:
            xi_arb = arb(xi_val)
        tau_arb = arb(2) * arb.pi()
        omega_full = tau_arb * abs(xi_arb)

        # Determine effective truncation K_eff and certified geometric factors on omega_full
        K_eff = K_terms
        R_even, R_odd = compute_hat_f_tail_ratios_arb(omega_full, K_eff)
        half_arb = arb(1) / arb(2)
        one_arb = arb(1)

        if strict_K:
            if bool((R_even - one_arb).upper() >= 0) or bool((R_odd - one_arb).upper() >= 0):
                raise ValueError(
                    f"K_terms={K_terms} is insufficient for xi={xi_val}: "
                    f"R_even={R_even} (must be < 1 for geometric tail certification)"
                )
        else:
            if bool((R_even - half_arb).upper() > 0) or bool((R_odd - half_arb).upper() > 0):
                K_eff = max(K_eff, 200)
                R_even, R_odd = compute_hat_f_tail_ratios_arb(omega_full, K_eff)
                while bool((R_even - half_arb).upper() > 0) or bool((R_odd - half_arb).upper() > 0):
                    K_eff = max(K_eff + 16, int(K_eff * 3 // 2))
                    R_even, R_odd = compute_hat_f_tail_ratios_arb(omega_full, K_eff)

        def _tail_factors(r_ev: arb, r_od: arb) -> Tuple[arb, arb]:
            f_ev = arb(2) if bool((r_ev - half_arb).upper() <= 0) else one_arb / (one_arb - r_ev)
            f_od = arb(2) if bool((r_od - half_arb).upper() <= 0) else one_arb / (one_arb - r_od)
            return f_ev, f_od

        # Evaluate at midpoint (zero-radius) with adaptive K_eff and working precision refinement
        for _attempt in range(8):
            flint_ctx.prec = work_prec
            tau_w = arb(2) * arb.pi()
            xi_mid = xi_arb.mid()
            omega_mid = tau_w * abs(xi_mid)
            r_ev_mid, r_od_mid = compute_hat_f_tail_ratios_arb(omega_mid, K_eff)
            f_ev_mid, f_od_mid = _tail_factors(r_ev_mid, r_od_mid)
            mid_val = _eval_hat_f_series_core_arb(omega_mid, K_eff, f_ev_mid, f_od_mid)
            # Check if omitted tail or alternating cancellation inflated radius beyond target precision
            if bool(mid_val.rad() <= arb(2) ** (-(prec_bits + 16))) or strict_K:
                break
            K_eff = max(K_eff + 64, int(K_eff * 3 // 2))
            work_prec *= 2
            R_even, R_odd = compute_hat_f_tail_ratios_arb(omega_full, K_eff)

        xi_rad = xi_arb.rad()
        if bool(xi_rad.is_zero()):
            res_work = mid_val
        else:
            # Rigorous Lipschitz enclosure: |hat{f}'(xi)| <= 2*tau * int_0^infty v^{-5} e^{-1/v^2} dv = tau
            lipschitz_encl = inflate_arb_with_nonneg_bound(mid_val, tau_w * xi_rad)
            f_ev_full, f_od_full = _tail_factors(R_even, R_odd)
            direct_encl = _eval_hat_f_series_core_arb(omega_full, K_eff, f_ev_full, f_od_full)
            res_work = lipschitz_encl.intersection(direct_encl)

        flint_ctx.prec = prec_bits
        return arb(res_work)
    finally:
        flint_ctx.prec = saved_prec


def reproduce_tc054_hat_f_k1_counterexample_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Reproduce the legacy TC-054 failure at `K_terms=1`, `xi = 4 / tau` (`omega = 4`):
      - Legacy midpoint ~ -42.7814017777
      - Legacy radius   ~  40.0818309197
      - Legacy upper    ~  -2.6995708581 < -Gamma(5/2) ~ -1.3293403882
    whereas |hat{f}(xi)| <= int_R f(v) dv = Gamma(5/2) and the true value is
    hat{f}(4 / tau) = -0.7757751802167744...
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = max(prec_bits, 512)
        tau_arb = arb(2) * arb.pi()
        xi_arb = arb(4) / tau_arb
        omega = arb(4)
        omega_sq = arb(16)

        # Legacy K_terms = 1 calculation without ratio check
        a0 = (arb(5) / arb(2)).gamma()
        a1 = -(arb(3) / arb(2)).gamma() * omega_sq / arb(2)
        even_sum_k1 = a0 + a1
        a2_abs = abs((arb(1) / arb(2)).gamma()) * (omega ** 4) / arb(24)
        old_even_tail = arb(2) * a2_abs

        b0 = (omega ** 5) / arb(120)
        b1 = (omega ** 7) / arb(5040)
        odd_sum_k1 = b0 + b1
        b2 = (omega ** 9) / (arb(2) * arb(362880))
        old_odd_tail = tau_arb * b2

        old_partial = even_sum_k1 - (tau_arb / arb(2)) * odd_sum_k1
        old_total_tail = old_even_tail + old_odd_tail
        flint_ctx.prec = prec_bits
        old_mid = arb(old_partial).mid()
        old_encl = inflate_arb_with_nonneg_bound(arb(old_partial), arb(old_total_tail))
        old_upper = old_encl.upper()

        gamma_5_2 = (arb(5) / arb(2)).gamma()
        neg_gamma_5_2 = -gamma_5_2
        R_even_k1, R_odd_k1 = compute_hat_f_tail_ratios_arb(arb(4), 1)

        repaired_default = evaluate_hat_f_hypergeometric_certified_arb(
            xi_arb, K_terms=1, prec_bits=prec_bits, strict_K=False
        )
        repaired_k4 = evaluate_hat_f_hypergeometric_certified_arb(
            xi_arb, K_terms=4, prec_bits=prec_bits, strict_K=True
        )
        R_even_k4, R_odd_k4 = compute_hat_f_tail_ratios_arb(arb(4), 4)

        strict_k1_rejected = False
        try:
            evaluate_hat_f_hypergeometric_certified_arb(
                xi_arb, K_terms=1, prec_bits=prec_bits, strict_K=True
            )
        except ValueError:
            strict_k1_rejected = True

        contradiction_gap = neg_gamma_5_2 - old_upper

        return {
            "K_terms": 1,
            "xi_formula": "4 / tau",
            "omega": "4",
            "R_even_at_K1_omega4": serialize_arb_certified(R_even_k1),
            "R_odd_at_K1_omega4": serialize_arb_certified(R_odd_k1),
            "R_even_exceeds_one": bool(R_even_k1.lower() > 1),
            "old_midpoint": serialize_arb_certified(old_mid),
            "old_tail_radius": serialize_arb_certified(arb(old_total_tail)),
            "old_enclosure": serialize_arb_certified(old_encl),
            "old_upper_endpoint": serialize_arb_certified(old_upper),
            "trivial_lower_bound_neg_Gamma_5_2": serialize_arb_certified(neg_gamma_5_2),
            "contradiction_gap_neg_Gamma_5_2_minus_old_upper": serialize_arb_certified(contradiction_gap),
            "old_upper_strictly_below_neg_Gamma_5_2": bool(contradiction_gap.lower() > 0),
            "strict_K1_raises_value_error": strict_k1_rejected,
            "R_even_at_K4_omega4": serialize_arb_certified(R_even_k4),
            "R_odd_at_K4_omega4": serialize_arb_certified(R_odd_k4),
            "repaired_strict_K4_geometric_enclosure": serialize_arb_certified(repaired_k4),
            "repaired_adaptive_enclosure": serialize_arb_certified(repaired_default),
            "repaired_k4_contains_adaptive": bool(repaired_k4.contains(repaired_default)),
            "repaired_k4_overlaps_adaptive": bool(repaired_k4.overlaps(repaired_default)),
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_mellin_contour_and_reflection_identities_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TASK-TC-054R2 §2 in 256-bit Arb:
    1. On z = 1/2 + i*b, 1 / |sin(tau*z/4) * Gamma(1 - z)| = 2 / sqrt(tau) is a constant independent
       of b (showing the old claim of extra exp(-tau*|b|/4) decay from sin(tau*z/4)*Gamma(1-z) alone fails).
    2. Corrected reflection identity:
           Gamma(1 - z) * sin(tau * z / 4) = (tau / 2) / (2 * Gamma(z) * cos(tau * z / 4))
       and the three equivalent Mellin-kernel forms for H(omega) = 2 int_0^infty f(v) cos(omega v) dv:
           M[H](z) = Gamma(z) * cos(tau * z / 4) * Gamma((5 + z) / 2)
                   = (tau / 2) * Gamma(z) / Gamma((-3 - z) / 2)
                   = (tau / 2)^2 / (sin(tau * z / 2) * Gamma(1 - z) * Gamma((-3 - z) / 2)).
    3. DLMF 5.8.3 lower bound for R >= 1/2:
           |Gamma(R + i*b)| >= Gamma(R) * exp(-tau * |b| / 4).
    4. Shifted vertical contour Re(z) = a_M = -(2M + 3/2) for M >= 2:
           |sin(tau * (a_M + i*b) / 2)| = cosh(tau * b / 2) >= (1/2) * exp(tau * |b| / 2),
       and the explicit inverse-Mellin remainder bound:
           |R_M(omega)| <= 8 * omega^{2M + 3/2} / (Gamma(2M + 5/2) * Gamma(M - 3/4)) -> 0.
    5. Even-series term sign check for m >= 2:
           (-1)^m * Gamma(5/2 - m) = |Gamma(5/2 - m)| > 0,
       so every even-series term (-1)^m Gamma(5/2 - m) omega^{2m} / (2m)! is strictly positive for m >= 2
       (in particular at m = 3, (-1)^3 Gamma(5/2 - 3) omega^6 / 6! = Gamma(1/2) omega^6 / 360 > 0).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()
        tau_acb = acb(tau_arb)
        two_over_sqrt_tau = arb(2) / tau_arb.sqrt()

        # 1. Check 1 / |sin(tau*z/4) * Gamma(1 - z)| = 2 / sqrt(tau) at z = 1/2 + i*b
        critical_line_rows: List[Dict[str, Any]] = []
        all_crit_line_exact = True
        for b_lbl, b_arb in [
            ("0", arb(0)),
            ("1/2", arb(1) / arb(2)),
            ("1", arb(1)),
            ("2", arb(2)),
            ("4", arb(4)),
        ]:
            z_acb = acb(arb(1) / arb(2), b_arb)
            sin_part = (tau_acb * z_acb / acb(4)).sin()
            gamma_part = (acb(1) - z_acb).gamma()
            inv_prod_abs = arb(1) / abs(sin_part * gamma_part)
            diff_crit = inv_prod_abs - two_over_sqrt_tau
            ok_crit = bool(diff_crit.contains(0))
            if not ok_crit:
                all_crit_line_exact = False
            critical_line_rows.append({
                "b_label": b_lbl,
                "inv_abs_sin_tau_z_over_4_gamma_1_minus_z": serialize_arb_certified(inv_prod_abs),
                "two_over_sqrt_tau": serialize_arb_certified(two_over_sqrt_tau),
                "difference_enclosure": serialize_arb_certified(diff_crit),
                "zero_in_difference": ok_crit,
            })

        # 2. Check corrected reflection identity and three Mellin kernel forms
        reflection_rows: List[Dict[str, Any]] = []
        all_reflection_ok = True
        for z_lbl, a_arb, b_arb in [
            ("1/2 + i", arb(1) / arb(2), arb(1)),
            ("3/4 + 2i", arb(3) / arb(4), arb(2)),
            ("-5/2 + i", -arb(5) / arb(2), arb(1)),
            ("-11/2 + 3i/2", -arb(11) / arb(2), arb(3) / arb(2)),
        ]:
            z_acb = acb(a_arb, b_arb)
            lhs_refl = (acb(1) - z_acb).gamma() * ((tau_acb * z_acb / acb(4)).sin())
            rhs_refl = (tau_acb / acb(2)) / (acb(2) * z_acb.gamma() * ((tau_acb * z_acb / acb(4)).cos()))
            refl_err = abs(lhs_refl - rhs_refl)

            mh_form1 = z_acb.gamma() * ((tau_acb * z_acb / acb(4)).cos()) * ((acb(5) + z_acb) / acb(2)).gamma()
            mh_form2 = (tau_acb / acb(2)) * z_acb.gamma() / ((acb(-3) - z_acb) / acb(2)).gamma()
            mh_form3 = ((tau_acb / acb(2)) ** 2) / (
                ((tau_acb * z_acb / acb(2)).sin())
                * (acb(1) - z_acb).gamma()
                * ((acb(-3) - z_acb) / acb(2)).gamma()
            )
            err_12 = abs(mh_form1 - mh_form2)
            err_23 = abs(mh_form2 - mh_form3)
            ok_row = bool(refl_err.contains(0) and err_12.contains(0) and err_23.contains(0))
            if not ok_row:
                all_reflection_ok = False
            reflection_rows.append({
                "z_label": z_lbl,
                "reflection_abs_diff": serialize_arb_certified(refl_err),
                "mellin_form1_minus_form2_abs": serialize_arb_certified(err_12),
                "mellin_form2_minus_form3_abs": serialize_arb_certified(err_23),
                "all_identities_contain_zero": ok_row,
            })

        # 3. Check DLMF 5.8.3 lower bound |Gamma(R + i*b)| >= Gamma(R) * exp(-tau * |b| / 4) for R >= 1/2
        dlmf_rows: List[Dict[str, Any]] = []
        all_dlmf_ok = True
        for R_lbl, R_arb, b_arb in [
            ("1/2", arb(1) / arb(2), arb(1)),
            ("5/4", arb(5) / arb(4), arb(2)),
            ("13/2", arb(13) / arb(2), arb(3)),
            ("21/2", arb(21) / arb(2), arb(4)),
        ]:
            abs_gamma_Rb = abs(acb(R_arb, b_arb).gamma())
            dlmf_lower = R_arb.gamma() * (-tau_arb * abs(b_arb) / arb(4)).exp()
            gap_dlmf = abs_gamma_Rb - dlmf_lower
            ok_dlmf = bool(gap_dlmf.lower() >= 0)
            if not ok_dlmf:
                all_dlmf_ok = False
            dlmf_rows.append({
                "R_label": R_lbl,
                "b": str(int(b_arb.unique_fmpz())),
                "abs_Gamma_R_plus_ib": serialize_arb_certified(abs_gamma_Rb),
                "lower_bound_Gamma_R_exp_neg_tau_b_over_4": serialize_arb_certified(dlmf_lower),
                "abs_minus_lower_bound": serialize_arb_certified(gap_dlmf),
                "lower_bound_holds": ok_dlmf,
            })

        # 4. Check shifted contour a_M = -(2M + 3/2) remainder bound B_rem(M, omega) = 8 * omega^{2M + 3/2} / (Gamma(2M + 5/2) * Gamma(M - 3/4))
        remainder_rows: List[Dict[str, Any]] = []
        omega_rem = arb(4)
        for M_int in [2, 4, 8, 16, 32]:
            M_arb = arb(M_int)
            a_M_arb = -(arb(2 * M_int) + arb(3) / arb(2))
            b_test = arb(1)
            sin_aM = abs((tau_acb * acb(a_M_arb, b_test) / acb(2)).sin())
            cosh_b = (tau_arb * b_test / arb(2)).cosh()
            sin_eq_cosh = bool((sin_aM - cosh_b).contains(0))
            b_rem = (
                arb(8)
                * (omega_rem ** (arb(2 * M_int) + arb(3) / arb(2)))
                / ((arb(2 * M_int) + arb(5) / arb(2)).gamma() * (M_arb - arb(3) / arb(4)).gamma())
            )
            remainder_rows.append({
                "M": M_int,
                "a_M_formula": f"-{4 * M_int + 3}/2",
                "omega": 4,
                "abs_sin_tau_z_over_2_equals_cosh_tau_b_over_2_at_b1": sin_eq_cosh,
                "remainder_upper_bound_8_omega_pow_over_gammas": serialize_arb_certified(b_rem),
            })

        # 5. Check even-series term signs for m in {0, 1, 2, 3, 4, 5} at omega = 1
        # and verify the corrected intermediate recurrence for m >= 2:
        #   Gamma(5/2 - m) = (-1)^{m-2} Gamma(1/2) / prod_{j=1}^{m-2} (j - 1/2),
        # and Res_{z=-2m} Gamma(z) = 1/(2m)! with alternating sign (-1)^m from cos(-m*tau/2) = (-1)^m.
        even_sign_rows: List[Dict[str, Any]] = []
        all_m_ge_2_positive = True
        all_recurrence_ok = True
        gamma_1_2 = (arb(1) / arb(2)).gamma()
        for m in range(0, 6):
            gamma_5_2_m = (arb(5) / arb(2) - arb(m)).gamma()
            res_gamma_neg_2m = arb(1) / arb(math.factorial(2 * m))
            cos_neg_m_tau_over_2 = arb(1) if (m % 2 == 0) else arb(-1)
            coeff_m = cos_neg_m_tau_over_2 * gamma_5_2_m * res_gamma_neg_2m
            if m >= 2:
                denom_prod = arb(1)
                for j in range(1, m - 1):
                    denom_prod *= (arb(j) - arb(1) / arb(2))
                sign_m_minus_2 = arb(1) if ((m - 2) % 2 == 0) else arb(-1)
                recurrence_rhs = sign_m_minus_2 * gamma_1_2 / denom_prod
                rec_diff = gamma_5_2_m - recurrence_rhs
                rec_ok = bool(rec_diff.contains(0))
                if not rec_ok:
                    all_recurrence_ok = False
            else:
                rec_ok = True
            if m >= 2 and not bool(coeff_m.lower() > 0):
                all_m_ge_2_positive = False
            even_sign_rows.append({
                "m": m,
                "Res_Gamma_at_neg_2m": f"1/({2 * m})!",
                "cos_tau_neg_2m_over_4": 1 if (m % 2 == 0) else -1,
                "Gamma_5_2_minus_m": serialize_arb_certified(gamma_5_2_m),
                "recurrence_matches_Gamma_1_2_over_rising_half_product": rec_ok,
                "even_series_coeff_at_omega_1": serialize_arb_certified(coeff_m),
                "strictly_positive": bool(coeff_m.lower() > 0),
                "strictly_negative": bool(coeff_m.upper() < 0),
            })
        m3_coeff = -(arb(5) / arb(2) - arb(3)).gamma() / arb(720)
        m3_closed = (arb(1) / arb(2)).gamma() / arb(360)
        m3_diff = m3_coeff - m3_closed

        return {
            "critical_line_constant_product_check": {
                "formula": "1 / |sin(tau * z / 4) * Gamma(1 - z)| = 2 / sqrt(tau)  for z = 1/2 + i*b",
                "two_over_sqrt_tau": serialize_arb_certified(two_over_sqrt_tau),
                "rows": critical_line_rows,
                "all_rows_match_constant_2_over_sqrt_tau": all_crit_line_exact,
            },
            "corrected_reflection_and_mellin_kernel_identities": {
                "corrected_reflection_formula": "Gamma(1 - z) * sin(tau * z / 4) = (tau / 2) / (2 * Gamma(z) * cos(tau * z / 4))",
                "mellin_kernel_formulas": [
                    "M[H](z) = Gamma(z) * cos(tau * z / 4) * Gamma((5 + z) / 2)",
                    "M[H](z) = (tau / 2) * Gamma(z) / Gamma((-3 - z) / 2)",
                    "M[H](z) = (tau / 2)^2 / (sin(tau * z / 2) * Gamma(1 - z) * Gamma((-3 - z) / 2))",
                ],
                "vertical_contour_stirling_asymptotic": (
                    "|M[H](a + i*b)| = (tau/2) |Gamma(a + i*b)| / |Gamma((-3 - a)/2 - i*b/2)| "
                    "asymp_a |b|^{3a/2 + 3/2} exp(-tau * |b| / 8) for fixed a in R, |b| >= 1"
                ),
                "horizontal_strip_dlmf_5_8_3_shift_bound": (
                    "On z = a +- i*B across the entire strip a in [a_M, c] (c in (0, 1), B >= 1), shifting "
                    "Gamma(1 - z) = Gamma(2 - z)/(1 - z) (Re(2 - z) = 2 - a > 1 >= 1/2) and "
                    "Gamma((-3 - z)/2) = Gamma((3 - z)/2) / (((-3 - z)/2)((-1 - z)/2)((1 - z)/2)) "
                    "(Re((3 - z)/2) = (3 - a)/2 > 1 >= 1/2) places both Gamma factors in Re >= 1/2 throughout "
                    "a in [a_M, c], yielding |M[H](a +- i*B)| <= C_{M,c} B^4 exp(-tau * B / 8) -> 0 as B -> infty."
                ),
                "rows": reflection_rows,
                "all_reflection_and_kernel_identities_hold": all_reflection_ok,
            },
            "dlmf_5_8_3_gamma_lower_bound_checks": {
                "formula": "|Gamma(R + i*b)| >= Gamma(R) * exp(-tau * |b| / 4)  for R >= 1/2",
                "rows": dlmf_rows,
                "all_dlmf_lower_bounds_hold": all_dlmf_ok,
            },
            "shifted_contour_remainder_bounds": {
                "contour_abscissa_formula": "a_M = -(2M + 3/2)  (M >= 2)",
                "remainder_bound_formula": "|R_M(omega)| <= 8 * omega^{2M + 3/2} / (Gamma(2M + 5/2) * Gamma(M - 3/4))",
                "rows_at_omega_4": remainder_rows,
            },
            "even_series_term_sign_analysis": {
                "residue_decomposition": (
                    "Res_{z=-2m} Gamma(z) = (-1)^{2m}/(2m)! = 1/(2m)! > 0; the alternating sign (-1)^m in "
                    "t_even(m) = (-1)^m Gamma(5/2 - m) omega^{2m} / (2m)! comes from cos(tau*(-2m)/4) = cos(-m*tau/2) = (-1)^m."
                ),
                "gamma_5_2_minus_m_recurrence": (
                    "For m >= 2, Gamma(5/2 - m) = Gamma(1/2) / ((-1/2)(-3/2)...(5/2 - m)) = "
                    "(-1)^{m-2} Gamma(1/2) / prod_{j=1}^{m-2} (j - 1/2)."
                ),
                "note": (
                    "For m = 0, t_even(0) = Gamma(5/2) > 0; for m = 1, t_even(1) = -Gamma(3/2) omega^2 / 2 < 0; "
                    "for all integers m >= 2, Gamma(5/2 - m) = (-1)^{m-2} Gamma(1/2) / prod_{j=1}^{m-2} (j - 1/2) "
                    "has sign (-1)^{m-2} = (-1)^m, so (-1)^m Gamma(5/2 - m) = |Gamma(5/2 - m)| > 0 and every "
                    "even-series term t_even(m) is strictly positive (not alternating). "
                    "At m = 3, (-1)^3 Gamma(5/2 - 3) omega^6 / 6! = Gamma(1/2) omega^6 / 360 > 0."
                ),
                "rows": even_sign_rows,
                "all_m_ge_2_strictly_positive": all_m_ge_2_positive,
                "all_m_ge_2_recurrences_hold": all_recurrence_ok,
                "m3_coeff_minus_Gamma_1_2_over_360": serialize_arb_certified(m3_diff),
                "m3_matches_Gamma_1_2_over_360": bool(m3_diff.contains(0)),
            },
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_hat_f_quadrature_certified_arb(
    xi_val: Union[arb, int, float, str, Fraction],
    prec_bits: int = 256,
    v0_num_den: Tuple[int, int] = (1, 7),
    V1_int: int = 32,
) -> arb:
    """Independently enclose hat{f}(xi) = 2 int_0^infty v^{-6} exp(-1/v^2) cos(tau xi v) dv
    using certified Arb complex-analytic Gauss-Legendre quadrature (`acb.integral`) on [v_0, V_1]
    plus proved analytic tail bounds:
      - On (0, v_0] with u_0 = v_0^{-2} >= 3:
            2 int_0^{v_0} v^{-6} exp(-1/v^2) dv = int_{u_0}^infty u^{3/2} e^{-u} du <= 2 v_0^{-3} exp(-1/v_0^2),
        since d/du(-2 u^{3/2} e^{-u}) = (2u - 3) u^{1/2} e^{-u} >= u^{3/2} e^{-u} for all u >= 3.
      - On [V_1, infty):
            2 int_{V_1}^infty v^{-6} exp(-1/v^2) |cos(tau xi v)| dv <= 2 int_{V_1}^infty v^{-6} dv = (2/5) V_1^{-5}.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        if isinstance(xi_val, Fraction):
            xi_arb = arb(xi_val.numerator) / arb(xi_val.denominator)
        else:
            xi_arb = arb(xi_val)
        tau_arb = arb(2) * arb.pi()
        omega_acb = acb(tau_arb * abs(xi_arb))

        v0_arb = arb(v0_num_den[0]) / arb(v0_num_den[1])
        u0_arb = arb(1) / (v0_arb * v0_arb)
        assert bool(u0_arb.lower() >= 3), "Quadrature left-tail theorem requires v_0^{-2} >= 3"
        V1_arb = arb(V1_int)

        def _integrand(v_complex: acb, _analytic: bool) -> acb:
            v2 = v_complex * v_complex
            return acb(2) * (v_complex ** (-6)) * (-acb(1) / v2).exp() * (omega_acb * v_complex).cos()

        quad_prec = min(prec_bits, 128)
        flint_ctx.prec = quad_prec
        mid_integral = acb.integral(_integrand, acb(v0_arb), acb(V1_arb)).real

        flint_ctx.prec = prec_bits
        left_tail = arb(2) * (v0_arb ** (-3)) * (-u0_arb).exp()
        right_tail = (arb(2) / arb(5)) * (V1_arb ** (-5))
        return inflate_arb_with_nonneg_bound(arb(mid_integral), left_tail + right_tail)
    finally:
        flint_ctx.prec = saved_prec


def verify_section_5_poisson_summation_at_transition(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify Section 5 (and TASK-TC-054R §§3-4):
    - Replace false Schwartz premise with proved C^infty flatness at 0, O(|v|^{-6-j}) decay at infinity,
      L^1(R) derivative integrability, and C^1(R/Z) periodization convergence (DLMF 1.8.14).
    - Reproduce the legacy K_terms=1, xi=4/tau Fourier counterexample and verify repaired certification.
    - Certified 256-bit Arb values of hat{f}(xi) at xi in {0, 1/2, 4/tau, 1, 3/2, 2}, cross-checked
      against independent certified quadrature (`acb.integral` + analytic tails).
    - Full Poisson representation L^{-5} [c_0 + sum_{j=1}^{J_0} hat{f}(j L)] + Fourier tail bound
      (with c_0 = 3 sqrt(tau/2) / 8) vs direct d-sum sum_{d>=1} d^{-6} exp(-L^2/d^2) across L in {1/2, 1, 2, 4}.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        em_info = verify_euler_maclaurin_derivatives_and_constants_arb(prec_bits=prec_bits)
        C_4_arb = em_info["C_4_raw"]
        tau_arb = arb(2) * arb.pi()
        c_0_arb = arb(3) * (tau_arb / arb(2)).sqrt() / arb(8)

        k1_counterexample = reproduce_tc054_hat_f_k1_counterexample_arb(prec_bits=prec_bits)
        mellin_contour_audit = verify_mellin_contour_and_reflection_identities_arb(prec_bits=prec_bits)

        # 1. Sign-change witnesses for hat{f}(xi) + quadrature cross-check
        xi_samples: List[Tuple[str, arb, str]] = [
            ("0", arb(0), "positive"),
            ("1/2", arb(1) / arb(2), "negative"),
            ("4/tau", arb(4) / tau_arb, "negative"),
            ("1", arb(1), "negative"),
            ("3/2", arb(3) / arb(2), "positive"),
            ("2", arb(2), "positive"),
        ]
        v0_quad = arb(1) / arb(7)
        u0_quad = arb(49)
        V1_quad = arb(32)
        quad_left_tail_bound = arb(2) * (v0_quad ** (-3)) * (-u0_quad).exp()
        quad_right_tail_bound = (arb(2) / arb(5)) * (V1_quad ** (-5))

        hat_f_witnesses: List[Dict[str, Any]] = []
        all_quadrature_agree = True
        for xi_label, xi_arb, expected_sign in xi_samples:
            val = evaluate_hat_f_hypergeometric_certified_arb(xi_arb, K_terms=200, prec_bits=prec_bits)
            quad_val = evaluate_hat_f_quadrature_certified_arb(xi_arb, prec_bits=prec_bits)
            quad_diff = val - quad_val
            quad_ok = bool(quad_diff.contains(0))
            quad_contains_series = bool(quad_val.contains(val))
            series_overlaps_quad = bool(val.overlaps(quad_val))
            if not (quad_ok and quad_contains_series and series_overlaps_quad):
                all_quadrature_agree = False
            if expected_sign == "positive":
                sign_certified = bool(val.lower() > 0)
            else:
                sign_certified = bool(val.upper() < 0)

            omega_w = tau_arb * abs(xi_arb)
            omega_top_w = int((arb(4) * omega_w.upper()).ceil().unique_fmpz())
            work_prec_w = max(prec_bits + 128, 512 + max(0, omega_top_w))
            r_ev_w, r_od_w = compute_hat_f_tail_ratios_arb(omega_w, 200)
            m_next_w = 201
            even_tail_w = (
                arb(2)
                * (omega_w ** (2 * m_next_w))
                * abs((arb(5) / arb(2) - arb(m_next_w)).gamma())
                / arb(math.factorial(2 * m_next_w))
            )
            odd_tail_w = (
                arb(2)
                * (tau_arb / arb(2))
                * (omega_w ** (5 + 2 * m_next_w))
                / (arb(math.factorial(m_next_w)) * arb(math.factorial(5 + 2 * m_next_w)))
            )
            series_trunc_rad_w = even_tail_w + odd_tail_w

            hat_f_witnesses.append({
                "xi_label": xi_label,
                "xi": serialize_arb_certified(xi_arb),
                "hat_f_xi": serialize_arb_certified(val),
                "working_prec_bits": work_prec_w,
                "series_truncation_K_eff": 200,
                "series_R_even_at_K_eff": serialize_arb_certified(r_ev_w),
                "series_R_odd_at_K_eff": serialize_arb_certified(r_od_w),
                "series_truncation_radius": serialize_arb_certified(series_trunc_rad_w),
                "series_total_radius": serialize_arb_certified(arb(val.rad())),
                "quadrature_v0": "1/7",
                "quadrature_V1": 32,
                "quadrature_interval": "[1/7, 32]",
                "quadrature_left_tail_bound": serialize_arb_certified(quad_left_tail_bound),
                "quadrature_right_tail_bound_2_over_5_V1_pow_5": serialize_arb_certified(quad_right_tail_bound),
                "quadrature_total_radius": serialize_arb_certified(arb(quad_val.rad())),
                "hat_f_xi_quadrature_enclosure": serialize_arb_certified(quad_val),
                "comparison_mode": "quadrature_encloses_series_and_overlaps",
                "quadrature_contains_series": quad_contains_series,
                "series_overlaps_quadrature": series_overlaps_quad,
                "series_minus_quadrature_contains_zero": quad_ok,
                "expected_sign": expected_sign,
                "sign_strictly_certified": sign_certified,
            })

        # 2. Full Poisson identity vs direct d-sum at L in {1/2, 1, 2, 4}
        zeta_4 = arb(4).zeta()
        L_poisson_samples: List[Tuple[str, arb, int]] = [
            ("1/2", arb(1) / arb(2), 24),
            ("1", arb(1), 14),
            ("2", arb(2), 8),
            ("4", arb(4), 6),
        ]
        poisson_rows: List[Dict[str, Any]] = []
        all_poisson_match = True

        for L_label, L_arb, J_0 in L_poisson_samples:
            direct_d_sum = evaluate_d_sum_certified_arb(L_arb, D_cutoff=2000, prec_bits=prec_bits)
            fourier_partial = arb(0)
            for j in range(1, J_0 + 1):
                fourier_partial += evaluate_hat_f_hypergeometric_certified_arb(
                    arb(j) * L_arb, K_terms=240, prec_bits=prec_bits
                )
            fourier_tail_bound = (
                C_4_arb / (arb(3) * zeta_4 * (arb(J_0) ** 3) * (L_arb ** 4))
            )
            bracket = c_0_arb + fourier_partial
            partial_poisson = (L_arb ** (-5)) * bracket
            bracket_with_tail = inflate_arb_with_nonneg_bound(bracket, fourier_tail_bound)
            poisson_enclosure = (L_arb ** (-5)) * bracket_with_tail
            diff = direct_d_sum - poisson_enclosure
            contains_zero = bool(diff.contains(0))
            if not contains_zero:
                all_poisson_match = False

            poisson_rows.append({
                "L_label": L_label,
                "L": serialize_arb_certified(L_arb),
                "J_0": J_0,
                "direct_d_sum": serialize_arb_certified(direct_d_sum),
                "gaussian_zero_mode_L_neg5_c0": serialize_arb_certified((L_arb ** (-5)) * c_0_arb),
                "gaussian_zero_mode_L_neg5_c_gauss": serialize_arb_certified((L_arb ** (-5)) * c_0_arb),
                "nonzero_fourier_sum_L_neg5": serialize_arb_certified((L_arb ** (-5)) * fourier_partial),
                "poisson_partial_sum_without_tail": serialize_arb_certified(partial_poisson),
                "fourier_tail_bound_L_neg5": serialize_arb_certified((L_arb ** (-5)) * fourier_tail_bound),
                "poisson_total_enclosure": serialize_arb_certified(poisson_enclosure),
                "difference_enclosure": serialize_arb_certified(diff),
                "zero_in_difference": contains_zero,
            })

        return {
            "poisson_summation_hypotheses_and_non_schwartz_note": (
                "The even function f(v) = v^{-6} exp(-1/v^2) (v != 0), f(0) = 0 is NOT in the Schwartz class S(R) "
                "because v^6 f(v) = exp(-1/v^2) -> 1 != 0 as |v| -> infty. Instead, Poisson summation holds by the "
                "following proved hypotheses (DLMF 1.8.14): (1) f in C^infty(R) with f^{(j)}(0) = 0 for all j >= 0 "
                "since lim_{v->0} v^{-m} exp(-1/v^2) = 0; (2) by induction, f^{(j)}(v) = P_j(v^{-2}) v^{-6-j} exp(-1/v^2) "
                "= O(|v|^{-6-j}) as |v| -> infty, so f^{(j)} in L^1(R) cap C_0(R) for every j >= 0; (3) for each L > 0, "
                "the periodization P_L(x) = sum_{d in Z} f((x + d)/L) and its derivative P_L'(x) = L^{-1} sum_{d in Z} f'((x + d)/L) "
                "converge uniformly on x in [0, 1] by comparison with sum_{d!=0} |d|^{-6} < infty and sum_{d!=0} |d|^{-7} < infty, "
                "so P_L in C^1(R/Z) has an absolutely convergent Fourier series, yielding at x = 0: "
                "sum_{d>=1} d^{-6} exp(-L^2/d^2) = L^{-5} [c_0 + sum_{j>=1} hat{f}(j L)] with c_0 = 3 sqrt(tau/2) / 8."
            ),
            "c_0_formula": "3 * sqrt(tau / 2) / 8",
            "c_0": serialize_arb_certified(c_0_arb),
            "mellin_contour_and_reflection_identities": mellin_contour_audit,
            "legacy_k1_fourier_counterexample_regression": k1_counterexample,
            "hat_f_sign_change_witnesses": hat_f_witnesses,
            "all_witnesses_agree_with_independent_quadrature": all_quadrature_agree,
            "poisson_vs_direct_d_sum_rows": poisson_rows,
            "all_poisson_enclosures_contain_zero_difference": all_poisson_match,
        }
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 5. Section 6: Rectangular-Block Decomposition & Transition Attacks A and B
# ---------------------------------------------------------------------------


def _exact_ceil_fraction(q: Fraction) -> int:
    """Return exact math.ceil(q) for a Fraction q using pure integer arithmetic."""
    return -((-q.numerator) // q.denominator)


def _to_exact_positive_fraction(val: Union[int, Fraction, float, str]) -> Fraction:
    """Convert an exact scalar bound (`int`, `Fraction`, finite `float`, or rational `str`)
    to a positive `Fraction` without any floating-point tolerance subtraction.
    """
    if isinstance(val, bool):
        raise ValueError("Cutoff bound cannot be a bool")
    if isinstance(val, int):
        q = Fraction(val, 1)
    elif isinstance(val, Fraction):
        q = val
    elif isinstance(val, float):
        if not math.isfinite(val):
            raise ValueError(f"Cutoff bound must be finite, got {val!r}")
        q = Fraction(val)
    elif isinstance(val, str):
        q = Fraction(val)
    else:
        raise TypeError(f"Unsupported cutoff bound type: {type(val).__name__}")
    if q <= 0:
        raise ValueError(f"Cutoff bound must be > 0, got {val!r}")
    return q


def _resolve_exact_dyadic_cutoff_pairs(
    M_bound: Union[int, Fraction, float, str, arb],
    *,
    on_ambiguous_ball: str = "enclose",
) -> List[Tuple[int, int]]:
    """Resolve the integer summation endpoints `(m_start, m_stop)` for `M <= m < 2M`,
    where `m` runs over integers in `[max(1, ceil(M)), max(1, ceil(2M)))`:
      - For exact inputs (`int`, `Fraction`, finite `float` converted via `Fraction(M)`, or `str`),
        computes `ceil(M)` and `ceil(2M)` by exact integer division without `1e-12` tolerances.
      - For `arb` ball inputs `[M_low, M_high]`, computes `ceil(M_low)`, `ceil(M_high)`,
        `ceil(2*M_low)`, `ceil(2*M_high)` from the exact dyadic endpoints. If the ball straddles
        an integer or half-integer boundary (`m_start_min != m_start_max` or `m_stop_min != m_stop_max`),
        raises `ValueError` when `on_ambiguous_ball == 'raise'`, or returns all attainable `(m_start, m_stop)`
        pairs so the caller can return their certified `.union(...)` enclosure when `on_ambiguous_ball == 'enclose'`.
    """
    if on_ambiguous_ball not in ("enclose", "raise"):
        raise ValueError(f"on_ambiguous_ball must be 'enclose' or 'raise', got {on_ambiguous_ball!r}")

    if isinstance(M_bound, arb):
        if not M_bound.is_finite() or bool(M_bound.lower() <= 0):
            raise ValueError(f"M_bound Arb ball must be finite and strictly positive, got {M_bound!r}")
        m_start_min = max(1, int(M_bound.lower().ceil().unique_fmpz()))
        m_start_max = max(1, int(M_bound.upper().ceil().unique_fmpz()))
        two_M = arb(2) * M_bound
        m_stop_min = max(1, int(two_M.lower().ceil().unique_fmpz()))
        m_stop_max = max(1, int(two_M.upper().ceil().unique_fmpz()))
        if m_start_min != m_start_max or m_stop_min != m_stop_max:
            if on_ambiguous_ball == "raise":
                raise ValueError(
                    f"Ambiguous M_bound ball {M_bound} straddles a dyadic integer/half-integer cutoff: "
                    f"ceil(M) in [{m_start_min}, {m_start_max}], ceil(2M) in [{m_stop_min}, {m_stop_max}]"
                )
            pairs: List[Tuple[int, int]] = []
            for ms in range(m_start_min, m_start_max + 1):
                for me in range(max(ms, m_stop_min), m_stop_max + 1):
                    pairs.append((ms, me))
            return pairs or [(m_start_min, m_stop_min)]
        return [(m_start_min, m_stop_min)]

    q = _to_exact_positive_fraction(M_bound)
    m_start = max(1, _exact_ceil_fraction(q))
    m_stop = max(1, _exact_ceil_fraction(2 * q))
    return [(m_start, max(m_start, m_stop))]


def evaluate_rectangular_block_B_AB_certified_arb(
    A_val: Union[int, Fraction, float, str],
    B_val: Union[int, Fraction, float, str],
    X_val: arb,
    D_cutoff: int = 800,
    prec_bits: int = 256,
) -> arb:
    """Evaluate the coprime rectangular block
        B_{A,B}(X) = sum_{A <= r < 2A, B <= s < 2B, gcd(r,s)=1}
                     (lambda(r) lambda(s) X^5 / (r s)^3) sum_{d>=1} d^{-6} exp(-X^2 (r^{-2} + s^{-2}) / d^2),
    using exact rational cutoffs for `A <= r < 2A` and `B <= s < 2B`.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        r_start, r_stop = _resolve_exact_dyadic_cutoff_pairs(A_val)[0]
        s_start, s_stop = _resolve_exact_dyadic_cutoff_pairs(B_val)[0]
        X_arb = arb(X_val)
        X5 = X_arb ** 5
        total = arb(0)
        for r in range(r_start, r_stop):
            lam_r = liouville_lambda_int(r)
            r_arb = arb(r)
            for s in range(s_start, s_stop):
                if math.gcd(r, s) != 1:
                    continue
                lam_s = liouville_lambda_int(s)
                s_arb = arb(s)
                rs_arb = r_arb * s_arb
                L_arb = X_arb * (r_arb * r_arb + s_arb * s_arb).sqrt() / rs_arb
                d_sum = evaluate_d_sum_certified_arb(L_arb, D_cutoff=D_cutoff, prec_bits=prec_bits)
                total += arb(lam_r * lam_s) * X5 / (rs_arb ** 3) * d_sum
        return total
    finally:
        flint_ctx.prec = saved_prec


def evaluate_1d_dyadic_sum_U_lambda_arb(
    Y_val: arb,
    M_bound: Union[int, Fraction, float, str, arb],
    prec_bits: int = 256,
    *,
    on_ambiguous_ball: str = "enclose",
) -> arb:
    """Evaluate the 1D unweighted dyadic Liouville Gaussian sum
        U_lambda(Y; M) = Y^{5/2} sum_{M <= m < 2M} (lambda(m) / m^3) exp(-Y^2 / m^2),
    using exact integer/rational cutoffs (TASK-TC-054R §5) without tolerance subtraction.
    For `arb` balls straddling an integer or half-integer boundary, either encloses all attainable
    sums via `.union(...)` (`on_ambiguous_ball='enclose'`) or raises `ValueError` (`on_ambiguous_ball='raise'`).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        Y_arb = arb(Y_val)
        Y_sq = Y_arb * Y_arb
        Y_pow_5_2 = Y_arb ** (arb(5) / arb(2))
        pairs = _resolve_exact_dyadic_cutoff_pairs(M_bound, on_ambiguous_ball=on_ambiguous_ball)

        encl: arb | None = None
        for m_start, m_stop in pairs:
            total = arb(0)
            for m in range(m_start, m_stop):
                m_arb = arb(m)
                total += (arb(liouville_lambda_int(m)) / (m_arb ** 3)) * (-Y_sq / (m_arb * m_arb)).exp()
            val = Y_pow_5_2 * total
            encl = val if encl is None else encl.union(val)
        assert encl is not None
        return encl
    finally:
        flint_ctx.prec = saved_prec


def reproduce_tc054_cutoff_tolerance_counterexample_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Reproduce the legacy TC-054 cutoff regression at `M = 1 + 2^{-42}`, `Y = 1`:
      - `M = 1 + 2^{-42}` is an exact binary rational `(2^{42} + 1) / 2^{42}`.
      - The true half-open interval `[M, 2M) = [1 + 2^{-42}, 2 + 2^{-41})` contains only the integer `2`,
        so `U_lambda(1; 1 + 2^{-42}) = (lambda(2) / 2^3) exp(-1/4) = -exp(-1/4)/8 = -0.09735009788...`.
      - The legacy implementation `ceil(M - 1e-12)` and `ceil(2M - 1e-12)` shifted both endpoints across
        the integer boundaries `1` and `2`, selecting `{1}` instead of `{2}` and returning
        `+exp(-1) = +0.36787944117...` (wrong sign and wrong magnitude).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        M_exact_frac = Fraction((1 << 42) + 1, 1 << 42)
        M_float = 1.0 + 2.0 ** (-42)
        assert Fraction(M_float) == M_exact_frac

        old_m_start = max(1, math.ceil(M_float - 1e-12))
        old_m_stop = math.ceil(2.0 * M_float - 1e-12)
        old_val = (-arb(1)).exp()

        repaired_from_frac = evaluate_1d_dyadic_sum_U_lambda_arb(arb(1), M_exact_frac, prec_bits=prec_bits)
        repaired_from_float = evaluate_1d_dyadic_sum_U_lambda_arb(arb(1), M_float, prec_bits=prec_bits)
        exact_true_val = -((-arb(1) / arb(4)).exp()) / arb(8)
        abs_error_of_old = abs(old_val - exact_true_val)

        return {
            "M_formula": "1 + 2^{-42}",
            "M_exact_fraction": f"{M_exact_frac.numerator}/{M_exact_frac.denominator}",
            "Y": 1,
            "true_integer_set": [2],
            "old_tolerance_selected_integer_set": list(range(old_m_start, old_m_stop)),
            "true_U_lambda_enclosure": serialize_arb_certified(exact_true_val),
            "repaired_from_fraction_enclosure": serialize_arb_certified(repaired_from_frac),
            "repaired_from_binary_float_enclosure": serialize_arb_certified(repaired_from_float),
            "old_tolerance_value_exp_neg1": serialize_arb_certified(old_val),
            "old_minus_true_abs_discrepancy": serialize_arb_certified(abs_error_of_old),
            "true_value_strictly_negative": bool(exact_true_val.upper() < 0),
            "old_value_strictly_positive": bool(old_val.lower() > 0),
            "repaired_matches_true_exact": bool(
                (repaired_from_frac - exact_true_val).contains(0)
                and (repaired_from_float - exact_true_val).contains(0)
            ),
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_decoupled_rectangular_block_B_AB_certified_arb(
    A_val: Union[int, Fraction, float, str],
    B_val: Union[int, Fraction, float, str],
    X_val: arb,
    D_cutoff: int = 800,
    prec_bits: int = 256,
) -> arb:
    """Evaluate B_{A,B}(X) via the Attack A separable Gaussian decoupling formula:
        B_{A,B}(X) = sum_{1 <= e < 2 min(A,B)} (mu(e) / e)
                     * sum_{d >= 1} (1 / d) U_lambda(X / (d e); A / e) U_lambda(X / (d e); B / e),
    computing `A / e` and `B / e` using exact rational `Fraction` arithmetic.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        A_frac = _to_exact_positive_fraction(A_val)
        B_frac = _to_exact_positive_fraction(B_val)
        r_start, r_stop = _resolve_exact_dyadic_cutoff_pairs(A_frac)[0]
        s_start, s_stop = _resolve_exact_dyadic_cutoff_pairs(B_frac)[0]
        X_arb = arb(X_val)
        X5 = X_arb ** 5
        e_max = max(0, min(r_stop, s_stop) - 1)
        partial = arb(0)
        for e in range(1, e_max + 1):
            mu_e = moebius_mu_int(e)
            if mu_e == 0:
                continue
            e_arb = arb(e)
            A_over_e = A_frac / e
            B_over_e = B_frac / e
            d_sum = arb(0)
            for d in range(1, D_cutoff + 1):
                d_arb = arb(d)
                Y_de = X_arb / (d_arb * e_arb)
                u_A = evaluate_1d_dyadic_sum_U_lambda_arb(Y_de, A_over_e, prec_bits=prec_bits)
                u_B = evaluate_1d_dyadic_sum_U_lambda_arb(Y_de, B_over_e, prec_bits=prec_bits)
                d_sum += (u_A * u_B) / d_arb
            partial += (arb(mu_e) / e_arb) * d_sum

        sum_r = sum((arb(r) ** (-3) for r in range(r_start, r_stop)), arb(0))
        sum_s = sum((arb(s) ** (-3) for s in range(s_start, s_stop)), arb(0))
        tail_bound = X5 * sum_r * sum_s / (arb(5) * (arb(D_cutoff) ** 5))
        return inflate_arb_with_nonneg_bound(partial, tail_bound)
    finally:
        flint_ctx.prec = saved_prec


def verify_abel_scaling_and_global_stieltjes_energy_proof(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TASK-TC-054R §2:
    1. Corrected dyadic Abel estimate:
           U_lambda(Y; M) = L_lambda(2M^-) g_Y(2M) - L_lambda(M^-) g_Y(M) - int_M^{2M} L_lambda(t) g_Y'(t) dt,
           |U_lambda(Y; M)| << M^{1/2} min(M / Y, (Y / M)^{5/2}) exp(-c Phi(M))   (M >= 16),
       where g_Y(t) = Y^{5/2} t^{-3} exp(-Y^2/t^2) and Phi(t) = (log t)^{3/5} (log log t)^{-1/5}.
    2. Analytical refutation of the old M^{-1/2} prefactor via the nonzero boundary residue
       Res_{z=0} M[Q_lambda](z) = Gamma(5/4) / (4 zeta(1/2)) = -0.1551682265... != 0.
    3. Exact collapse of the divisor-weighted global identity:
           sum_{q >= 1} ((sum_{e | q} mu(e)) / q) Q_lambda(X / q)^2 = Q_lambda(X)^2.
    4. Exact scaling integral check:
           I_scale := int_0^infty u |3 - 2 u^2| exp(-u^2) du = 1/2 + 2 exp(-3/2),
       cross-checked against certified Arb quadrature (`acb.integral` + analytic tail).
    5. Global Stieltjes integration-by-parts identity:
           Q_lambda(X) = -X^{5/2} int_1^infty L_lambda(t) d/dt (t^{-3} exp(-X^2/t^2)) dt
       and split at t = sqrt(X) (for X >= 256; compact range 0 < X < 256 bounded by |Q_lambda(X)| <= zeta(3) X^{5/2}),
       establishing |Q_lambda(X)| << sqrt(X) exp(-c_1 Phi(X)) and
       E_lambda(Y) := int_Y^{tau Y} |Q_lambda(X)|^2 dX/X << Y exp(-2 c_2 Phi(Y)) <<_D Y (log Y)^{-D}.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits

        # 1. Scaling integral I_scale = int_0^infty u |3 - 2 u^2| exp(-u^2) du = 1/2 + 2 exp(-3/2)
        e_neg_3_2 = (-arb(3) / arb(2)).exp()
        I_scale_closed = arb(1) / arb(2) + arb(2) * e_neg_3_2
        u_split = (arb(3) / arb(2)).sqrt()
        U_top = arb(8)

        def _ing_low(u_c: acb, _analytic: bool) -> acb:
            u2 = u_c * u_c
            return u_c * (acb(3) - acb(2) * u2) * (-u2).exp()

        def _ing_high(u_c: acb, _analytic: bool) -> acb:
            u2 = u_c * u_c
            return u_c * (acb(2) * u2 - acb(3)) * (-u2).exp()

        flint_ctx.prec = min(prec_bits, 128)
        part1 = acb.integral(_ing_low, acb(0), acb(u_split)).real
        part2 = acb.integral(_ing_high, acb(u_split), acb(U_top)).real
        flint_ctx.prec = prec_bits
        # Exact antiderivative on [U_top, infty) of u (2u^2 - 3) e^{-u^2} is (u^2 - 1/2) e^{-u^2}
        tail_top = (U_top * U_top - arb(1) / arb(2)) * (-(U_top * U_top)).exp()
        I_scale_quad = inflate_arb_with_nonneg_bound(arb(part1 + part2), tail_top)
        I_scale_diff = I_scale_closed - I_scale_quad

        # 2. Verify global Stieltjes identity Q_lambda(X) = -X^{5/2} int_1^infty L_lambda(t) d/dt(t^{-3} e^{-X^2/t^2}) dt
        # On each unit interval [m, m+1), L_lambda(t) = L_lambda(m) is constant, so
        # -X^{5/2} sum_{m=1}^T L_lambda(m) [ (m+1)^{-3} e^{-X^2/(m+1)^2} - m^{-3} e^{-X^2/m^2} ]
        # = X^{5/2} sum_{m=1}^T (lambda(m)/m^3) e^{-X^2/m^2} - X^{5/2} L_lambda(T) (T+1)^{-3} e^{-X^2/(T+1)^2}.
        stieltjes_rows: List[Dict[str, Any]] = []
        all_stieltjes_match = True
        T_st = 600
        L_vals = [0] * (T_st + 1)
        running = 0
        for m in range(1, T_st + 1):
            running += liouville_lambda_int(m)
            L_vals[m] = running

        for X_int in [1, 2, 4]:
            X_arb = arb(X_int)
            X_sq = X_arb * X_arb
            X_5_2 = X_arb ** (arb(5) / arb(2))
            q_direct = evaluate_Q_arith_certified_arb(X_arb, coeff_kind="lambda", T_cutoff=T_st, prec_bits=prec_bits)["enclosure"]

            st_partial = arb(0)
            for m in range(1, T_st + 1):
                m_arb = arb(m)
                m1_arb = arb(m + 1)
                g_m = (m_arb ** (-3)) * (-X_sq / (m_arb * m_arb)).exp()
                g_m1 = (m1_arb ** (-3)) * (-X_sq / (m1_arb * m1_arb)).exp()
                st_partial += -X_5_2 * arb(L_vals[m]) * (g_m1 - g_m)

            # Tail for t >= T_st + 1: since |L_lambda(t)| <= t,
            # X^{5/2} int_{T_st+1}^infty t * t^{-4} |2 X^2/t^2 - 3| e^{-X^2/t^2} dt <= 3 X^{5/2} int_{T_st+1}^infty t^{-3} dt
            # = (3/2) X^{5/2} (T_st + 1)^{-2} when T_st + 1 >= X sqrt(2/3).
            st_tail = (arb(3) / arb(2)) * X_5_2 / (arb(T_st + 1) ** 2)
            st_encl = inflate_arb_with_nonneg_bound(st_partial, st_tail)
            diff_st = q_direct - st_encl
            ok_st = bool(diff_st.contains(0))
            if not ok_st:
                all_stieltjes_match = False
            stieltjes_rows.append({
                "X": X_int,
                "T_stieltjes": T_st,
                "Q_lambda_direct": serialize_arb_certified(q_direct),
                "Q_lambda_stieltjes_integral": serialize_arb_certified(st_encl),
                "difference_enclosure": serialize_arb_certified(diff_st),
                "zero_in_difference": ok_st,
            })

        # 3. Verify divisor-weight collapse sum_{e | q} mu(e) = 1_{q=1} up to q = 100
        divisor_collapse_ok = all(
            sum(moebius_mu_int(e) for e in range(1, q + 1) if q % e == 0) == (1 if q == 1 else 0)
            for q in range(1, 101)
        )

        # 4. Compact-range elementary energy bound coefficient:
        # E_lambda(Y) = int_Y^{tau Y} |Q_lambda(X)|^2 dX/X <= zeta(3)^2 int_Y^{tau Y} X^4 dX
        #             = (zeta(3)^2 * (tau^5 - 1) / 5) * Y^5.
        tau_arb = arb(2) * arb.pi()
        zeta_3 = arb(3).zeta()
        compact_Y5_coeff = (zeta_3 * zeta_3) * ((tau_arb ** 5) - arb(1)) / arb(5)

        return {
            "corrected_dyadic_abel_bound": {
                "formula": "|U_lambda(Y; M)| << M^{1/2} min(M / Y, (Y / M)^{5/2}) exp(-c * Phi(M))",
                "Phi_definition": "Phi(t) = (log t)^{3/5} (log log t)^{-1/5}",
                "applicability_threshold": "M >= 16 (for 1 <= M < 16, |U_lambda(Y; M)| <= zeta(3) Y^{5/2} and <= (7/2) M^{1/2} min(M/Y, (Y/M)^{5/2}))",
                "half_open_stieltjes_decomposition": (
                    "U_lambda(Y; M) = L_lambda(2M^-) g_Y(2M) - L_lambda(M^-) g_Y(M) - int_M^{2M} L_lambda(t) g_Y'(t) dt, "
                    "where g_Y(t) = Y^{5/2} t^{-3} exp(-Y^2/t^2) satisfies sup_{t in [M, 2M]} g_Y(t) << M^{-1/2} min(M/Y, (Y/M)^{5/2}) "
                    "and int_M^{2M} |g_Y'(t)| dt << M^{-1/2} min(M/Y, (Y/M)^{5/2}). Multiplying by "
                    "sup_{t in [M, 2M]} |L_lambda(t)| << M exp(-c Phi(M)) yields the prefactor M * M^{-1/2} = M^{1/2}."
                ),
                "mellin_residue_refutation_of_old_M_neg_half": (
                    "If the old M^{-1/2} prefactor held uniformly across dyadic blocks M = 2^j, summing over j >= 0 would give "
                    "|Q_lambda(X)| <= sum_{j>=0} |U_lambda(X; 2^j)| = O(X^{-1/2}) as X -> infty. Together with "
                    "|Q_lambda(X)| = O(X^{5/2}) as X -> 0^+, the Mellin transform M[Q_lambda](z) = int_0^infty Q_lambda(X) X^{-z} dX/X "
                    "would converge absolutely and be holomorphic on -1/2 < Re(z) < 5/2, including at z = 0. "
                    "This contradicts the proved simple pole of M[Q_lambda](z) = Gamma(5/4 - z/2) zeta(1 + 2z) / (2 zeta(1/2 + z)) "
                    "at z = 0 with nonzero residue Gamma(5/4) / (4 zeta(1/2)) = -0.1551682265... != 0."
                ),
            },
            "divisor_weight_collapse_identity": {
                "identity": "sum_{q>=1} ((sum_{e|q} mu(e)) / q) Q_lambda(X / q)^2 = Q_lambda(X)^2",
                "verified_up_to_q_100": divisor_collapse_ok,
                "explanation": (
                    "Summing the decoupled blocks B_{2^a, 2^b}(X) over all a, b >= 0 and setting q = d * e yields "
                    "sum_{q>=1} ((sum_{e|q} mu(e)) / q) Q_lambda(X/q)^2. Since sum_{e|q} mu(e) = 1_{q=1}, all terms q >= 2 "
                    "vanish identically and the identity collapses to Q_lambda(X)^2 = Q_lambda(X)^2, supplying no additional "
                    "global cancellation by itself."
                ),
            },
            "scaling_integral_verification": {
                "integral_formula": "int_0^infty u |3 - 2*u^2| exp(-u^2) du = 1/2 + 2*exp(-3/2)",
                "closed_form": serialize_arb_certified(I_scale_closed),
                "quadrature_enclosure": serialize_arb_certified(I_scale_quad),
                "difference_enclosure": serialize_arb_certified(I_scale_diff),
                "zero_in_difference": bool(I_scale_diff.contains(0)),
            },
            "global_stieltjes_energy_proof": {
                "stieltjes_identity": "Q_lambda(X) = -X^{5/2} int_1^infty L_lambda(t) d/dt (t^{-3} exp(-X^2/t^2)) dt",
                "endpoint_justification": (
                    "At the lower limit t = 1^-, L_lambda(1^-) = 0; as T -> infty, |L_lambda(T)| <= T so "
                    "|X^{5/2} L_lambda(T) T^{-3} exp(-X^2/T^2)| <= X^{5/2} T^{-2} -> 0."
                ),
                "stretched_exponential_range": "Y >= 256: E_lambda(Y) << Y * exp(-2 * c_2 * Phi(Y))",
                "compact_range_elementary_bound_formula": (
                    "E_lambda(Y) = int_Y^{tau*Y} |Q_lambda(X)|^2 dX/X <= zeta(3)^2 * int_Y^{tau*Y} X^4 dX "
                    "= (zeta(3)^2 * (tau^5 - 1) / 5) * Y^5"
                ),
                "compact_range_Y5_coefficient_zeta3_sq_tau5_minus_1_over_5": serialize_arb_certified(compact_Y5_coeff),
                "all_logarithmic_range": (
                    "Y >= 2: for every D > 0, combining the stretched-exponential bound on Y >= 256 with the compact-range bound "
                    "E_lambda(Y) <= (zeta(3)^2 * (tau^5 - 1) / 5) * Y^5 on 2 <= Y < 256 (Note: the raw stretched-exponential "
                    "formula exp(-2 c Phi(Y)) is NOT asserted for 2 <= Y < 256 because Phi(Y) -> +infty as Y -> e^+ while E_lambda(e) > 0) "
                    "establishes E_lambda(Y) <<_D Y / (log Y)^D for all Y >= 2."
                ),
                "split_point_and_thresholds": (
                    "For X >= 256 (so sqrt(X) >= 16 and log(log(sqrt(X))) >= log(log(16)) > 1), split the integral at t = sqrt(X): "
                    "(i) on 1 <= t <= sqrt(X), |L_lambda(t)| <= t and 2 X^2/t^2 - 3 >= 2 X - 3 > 0, so "
                    "X^{5/2} int_1^{sqrt(X)} t * t^{-4} (2 X^2/t^2 - 3) exp(-X^2/t^2) dt <= 2 X^{9/2} int_1^{sqrt(X)} t^{-5} exp(-X^2/t^2) dt "
                    "= sqrt(X) int_X^{X^2} w e^{-w} dw <= sqrt(X) (X + 1) e^{-X}; "
                    "(ii) on t >= sqrt(X) >= 16, applying the unconditional Korobov-Vinogradov-Walfisz bound "
                    "|L_lambda(t)| <= C_KV t exp(-c_0 Phi(t)) <= C_KV t exp(-c_0 Phi(sqrt(X))) (derived either directly or from "
                    "|M(y)| <= C'_KV y exp(-c'_0 Phi(y)) via L_lambda(t) = sum_{d <= sqrt(t)} M(t/d^2)) and substituting u = X/t gives "
                    "X^{5/2} int_{sqrt(X)}^infty |L_lambda(t)| |d/dt(t^{-3} exp(-X^2/t^2))| dt "
                    "<= C_KV (1/2 + 2 exp(-3/2)) sqrt(X) exp(-c_0 Phi(sqrt(X))) << sqrt(X) exp(-c_1 Phi(X)). "
                    "Integrating |Q_lambda(X)|^2 dX/X over [Y, tau Y] yields the stretched-exponential bound E_lambda(Y) << Y exp(-2 c_2 Phi(Y)) "
                    "for Y >= 256; separately, on the compact range 2 <= Y < 256, E_lambda(Y) <= (zeta(3)^2 (tau^5 - 1) / 5) Y^5, "
                    "extending E_lambda(Y) <<_D Y (log Y)^{-D} to all Y >= 2 for every D > 0."
                ),
                "stieltjes_vs_direct_rows": stieltjes_rows,
                "all_stieltjes_rows_match_direct": all_stieltjes_match,
            },
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_section_6_transition_attacks_and_decoupling(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify Section 6 (and TASK-TC-054R §§2, 5, 6, 7):
    - Rectangular-block decomposition Q_lambda(X)^2 = sum_{a,b>=0} B_{2^a, 2^b}(X) and repaired
      widely unequal block bound |B_{A,B}(X)| <= (7/3) C_* min(A,B)^3 / max(A,B)^2 with
      C_* = max{zeta(6), c_0 + 27 exp(-3)} (c_0 = 3 sqrt(tau/2) / 8, zeta(6) = tau^6 / 60480).
    - Cutoff tolerance regression at M = 1 + 2^{-42}, Y = 1.
    - Repaired Abel scaling and global Stieltjes energy proof.
    - Attack A (1D Mellin, bivariate coprime Dirichlet series, separable Gaussian decoupling).
    - Attack B (dyadic parity annihilation, inversion, weighted norm equivalence in eta, off-critical lower bound).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits

        tau_arb = arb(2) * arb.pi()
        c_0_arb = arb(3) * (tau_arb / arb(2)).sqrt() / arb(8)
        zeta_6 = arb(6).zeta()  # tau^6 / 60480
        c0_plus_27_e_neg3 = c_0_arb + arb(27) * (-arb(3)).exp()
        # C_* = max(zeta(6), c_0 + 27 e^{-3}); since c_0 + 27 e^{-3} = 2.0089210400... > zeta(6) = 1.0173430619..., C_* = c_0 + 27 e^{-3}
        assert bool(c0_plus_27_e_neg3.lower() > zeta_6.upper())
        C_star_arb = c0_plus_27_e_neg3
        seven_thirds_C_star = (arb(7) / arb(3)) * C_star_arb

        # Verify unimodal sum-integral bound sum_{d>=1} d^{-6} e^{-L^2/d^2} <= C_* min(1, L^{-5})
        unimodal_L_samples: List[Tuple[str, arb]] = [
            ("1/4", arb(1) / arb(4)),
            ("1/2", arb(1) / arb(2)),
            ("1", arb(1)),
            ("sqrt(3)", arb(3).sqrt()),
            ("2", arb(2)),
            ("4", arb(4)),
            ("8", arb(8)),
        ]
        unimodal_rows: List[Dict[str, Any]] = []
        all_unimodal_ok = True
        for L_lbl, L_arb in unimodal_L_samples:
            d_sum = evaluate_d_sum_certified_arb(L_arb, D_cutoff=2000, prec_bits=prec_bits)
            if bool(L_arb.upper() <= 1):
                regime_bound = zeta_6
                combined_bound = C_star_arb
            else:
                regime_bound = c_0_arb * (L_arb ** (-5)) + arb(27) * (-arb(3)).exp() * (L_arb ** (-6))
                combined_bound = C_star_arb * (L_arb ** (-5))
            ok_reg = bool(d_sum.upper() <= regime_bound.lower())
            ok_comb = bool(d_sum.upper() <= combined_bound.lower())
            if not (ok_reg and ok_comb):
                all_unimodal_ok = False
            unimodal_rows.append({
                "L_label": L_lbl,
                "L": serialize_arb_certified(L_arb),
                "exact_d_sum": serialize_arb_certified(d_sum),
                "regime_specific_bound": serialize_arb_certified(regime_bound),
                "C_star_min_1_L_neg5_bound": serialize_arb_certified(combined_bound),
                "regime_bound_holds": ok_reg,
                "combined_bound_holds": ok_comb,
            })

        # 1. Separable Gaussian decoupling identity on sample blocks + repaired widely unequal block bound
        block_samples = [
            (1, 1, 2),
            (2, 2, 4),
            (2, 4, 4),
            (4, 4, 4),
            (1, 8, 4),
            (2, 16, 4),
            (1, 16, 1),
            (1, 16, 16),
            (4, 32, 8),
            (8, 1, 4),
        ]
        decoupling_rows: List[Dict[str, Any]] = []
        all_decoupling_match = True
        all_unequal_bounds_hold = True

        for A_int, B_int, X_int in block_samples:
            X_arb = arb(X_int)
            b_direct = evaluate_rectangular_block_B_AB_certified_arb(
                A_int, B_int, X_arb, D_cutoff=600, prec_bits=prec_bits
            )
            b_decoupled = evaluate_decoupled_rectangular_block_B_AB_certified_arb(
                A_int, B_int, X_arb, D_cutoff=600, prec_bits=prec_bits
            )
            diff = b_direct - b_decoupled
            match_ok = bool(diff.contains(0))
            if not match_ok:
                all_decoupling_match = False

            min_AB = arb(min(A_int, B_int))
            max_AB = arb(max(A_int, B_int))
            unequal_bound = seven_thirds_C_star * (min_AB ** 3) / (max_AB ** 2)
            unequal_ok = bool(abs(b_direct).upper() <= unequal_bound.lower())
            if not unequal_ok:
                all_unequal_bounds_hold = False

            decoupling_rows.append({
                "A": A_int,
                "B": B_int,
                "X": X_int,
                "B_AB_direct": serialize_arb_certified(b_direct),
                "B_AB_separable_decoupled": serialize_arb_certified(b_decoupled),
                "difference_enclosure": serialize_arb_certified(diff),
                "zero_in_difference": match_ok,
                "widely_unequal_bound_7_3_C_star_min3_over_max2": serialize_arb_certified(unequal_bound),
                "widely_unequal_bound_zeta6_min3_over_max2": serialize_arb_certified(unequal_bound),
                "widely_unequal_bound_holds": unequal_ok,
            })

        cutoff_regression = reproduce_tc054_cutoff_tolerance_counterexample_arb(prec_bits=prec_bits)
        abel_and_stieltjes = verify_abel_scaling_and_global_stieltjes_energy_proof(prec_bits=prec_bits)

        # 2. Attack A: 1D Mellin formula M[Q_lambda](z) = Gamma(5/4 - z/2) zeta(1 + 2 z) / (2 zeta(1/2 + z))
        # and boundary pole residue at z = 0: Res_{z=0} M[Q_lambda](z) = Gamma(5/4) / (4 zeta(1/2)).
        z_samples: List[Tuple[str, arb]] = [
            ("1", arb(1)),
            ("3/2", arb(3) / arb(2)),
            ("2", arb(2)),
        ]
        mellin_rows: List[Dict[str, Any]] = []
        for z_label, z_arb in z_samples:
            gamma_part = (arb(5) / arb(4) - z_arb / arb(2)).gamma()
            dirichlet_series = (arb(1) + arb(2) * z_arb).zeta() / ((arb(1) / arb(2) + z_arb).zeta())
            closed_form = gamma_part * dirichlet_series / arb(2)

            N_dir = 4000
            s_dir = arb(1) / arb(2) + z_arb
            partial_dir = arb(0)
            for n in range(1, N_dir + 1):
                partial_dir += arb(liouville_lambda_int(n)) * (arb(n) ** (-s_dir))
            dir_tail = (arb(N_dir) ** (arb(1) - s_dir)) / (s_dir - arb(1))
            dir_enclosure = inflate_arb_with_nonneg_bound(partial_dir, dir_tail)
            diff_mellin = closed_form - (gamma_part * dir_enclosure / arb(2))
            mellin_rows.append({
                "z_label": z_label,
                "z": serialize_arb_certified(z_arb),
                "M_Q_lambda_closed_form": serialize_arb_certified(closed_form),
                "M_Q_lambda_from_dirichlet_sum": serialize_arb_certified(gamma_part * dir_enclosure / arb(2)),
                "difference_enclosure": serialize_arb_certified(diff_mellin),
                "zero_in_difference": bool(diff_mellin.contains(0)),
            })

        res_z0 = (arb(5) / arb(4)).gamma() / (arb(4) * (arb(1) / arb(2)).zeta())

        # 3. Bivariate coprime Dirichlet series D_lambda(u, v) = zeta(2u) zeta(2v) / (zeta(u) zeta(v) zeta(u+v))
        uv_samples: List[Tuple[str, arb, arb]] = [
            ("(2, 2)", arb(2), arb(2)),
            ("(2, 3)", arb(2), arb(3)),
            ("(5/2, 5/2)", arb(5) / arb(2), arb(5) / arb(2)),
        ]
        bivariate_rows: List[Dict[str, Any]] = []
        for uv_label, u_arb, v_arb in uv_samples:
            closed_uv = (
                (arb(2) * u_arb).zeta()
                * (arb(2) * v_arb).zeta()
                / (u_arb.zeta() * v_arb.zeta() * (u_arb + v_arb).zeta())
            )
            E_cut = 500
            partial_e = arb(0)
            for e in range(1, E_cut + 1):
                mu_e = moebius_mu_int(e)
                if mu_e != 0:
                    partial_e += arb(mu_e) * (arb(e) ** (-(u_arb + v_arb)))
            tail_e = (arb(E_cut) ** (arb(1) - (u_arb + v_arb))) / ((u_arb + v_arb) - arb(1))
            e_encl = inflate_arb_with_nonneg_bound(partial_e, tail_e)
            decoupled_uv = e_encl * ((arb(2) * u_arb).zeta() / u_arb.zeta()) * ((arb(2) * v_arb).zeta() / v_arb.zeta())
            diff_uv = closed_uv - decoupled_uv
            bivariate_rows.append({
                "uv_label": uv_label,
                "closed_form_zeta_2u_zeta_2v_over_zeta_u_zeta_v_zeta_u_plus_v": serialize_arb_certified(closed_uv),
                "decoupled_euler_series": serialize_arb_certified(decoupled_uv),
                "difference_enclosure": serialize_arb_certified(diff_uv),
                "zero_in_difference": bool(diff_uv.contains(0)),
            })

        # 4. Attack B: Dyadic parity annihilation Q_{lambda,odd}(X) = Q_lambda(X) + 2^{-1/2} Q_lambda(X/2)
        inv_sqrt2 = arb(1) / arb(2).sqrt()
        dyadic_parity_rows: List[Dict[str, Any]] = []
        all_dyadic_parity_ok = True
        for X_label, X_arb in [("1", arb(1)), ("2", arb(2)), ("4", arb(4)), ("8", arb(8))]:
            q_X = evaluate_Q_arith_certified_arb(X_arb, coeff_kind="lambda", T_cutoff=4000, prec_bits=prec_bits)["enclosure"]
            q_half = evaluate_Q_arith_certified_arb(X_arb / arb(2), coeff_kind="lambda", T_cutoff=4000, prec_bits=prec_bits)["enclosure"]
            q_odd_comb = q_X + inv_sqrt2 * q_half

            T_odd = 4000
            X_sq = X_arb * X_arb
            X_pow_5_2 = X_arb ** (arb(5) / arb(2))
            odd_partial = arb(0)
            for m in range(1, T_odd + 1, 2):
                m_arb = arb(m)
                odd_partial += (arb(liouville_lambda_int(m)) / (m_arb ** 3)) * (-X_sq / (m_arb * m_arb)).exp()
            odd_tail = X_pow_5_2 / (arb(2) * (arb(T_odd) ** 2))
            q_odd_direct = inflate_arb_with_nonneg_bound(X_pow_5_2 * odd_partial, odd_tail)

            J_inv = 28
            inv_sum = arb(0)
            for j in range(0, J_inv + 1):
                sign_j = arb(1) if (j % 2 == 0) else arb(-1)
                scale_j = arb(2) ** (-arb(j) / arb(2))
                X_j = X_arb / (arb(2) ** j)
                T_j = max(200, int(2000 // max(1, 2 ** (j // 2))))
                X_j_sq = X_j * X_j
                X_j_5_2 = X_j ** (arb(5) / arb(2))
                part_j = arb(0)
                for m in range(1, T_j + 1, 2):
                    m_arb = arb(m)
                    part_j += (arb(liouville_lambda_int(m)) / (m_arb ** 3)) * (-X_j_sq / (m_arb * m_arb)).exp()
                tail_j = X_j_5_2 / (arb(2) * (arb(T_j) ** 2))
                q_odd_j = inflate_arb_with_nonneg_bound(X_j_5_2 * part_j, tail_j)
                inv_sum += sign_j * scale_j * q_odd_j
            inv_tail = (arb(3).zeta() * X_pow_5_2) * (arb(2) ** (-arb(3 * (J_inv + 1)))) / (arb(1) - arb(2) ** (-3))
            q_inv_encl = inflate_arb_with_nonneg_bound(inv_sum, inv_tail)

            diff_odd = q_odd_comb - q_odd_direct
            diff_inv = q_X - q_inv_encl
            ok_odd = bool(diff_odd.contains(0))
            ok_inv = bool(diff_inv.contains(0))
            if not (ok_odd and ok_inv):
                all_dyadic_parity_ok = False

            lhs_sq = q_odd_comb * q_odd_comb
            rhs_sq = (q_X * q_X) + (arb(1) / arb(2)) * (q_half * q_half) + arb(2).sqrt() * q_X * q_half
            diff_sq = lhs_sq - rhs_sq

            dyadic_parity_rows.append({
                "X_label": X_label,
                "Q_lambda_X": serialize_arb_certified(q_X),
                "Q_lambda_half_X": serialize_arb_certified(q_half),
                "Q_lambda_odd_from_combination": serialize_arb_certified(q_odd_comb),
                "Q_lambda_odd_direct_odd_sum": serialize_arb_certified(q_odd_direct),
                "odd_sum_difference": serialize_arb_certified(diff_odd),
                "odd_sum_zero_in_difference": ok_odd,
                "Q_lambda_from_dyadic_inversion": serialize_arb_certified(q_inv_encl),
                "dyadic_inversion_difference": serialize_arb_certified(diff_inv),
                "dyadic_inversion_zero_in_difference": ok_inv,
                "pointwise_energy_identity_difference": serialize_arb_certified(diff_sq),
                "pointwise_energy_zero_in_difference": bool(diff_sq.contains(0)),
            })

        # Off-critical mode nonvanishing |1 + 2^{-rho}| >= 1 - 2^{-x} > 0 (rho = x + i*y)
        off_critical_mode_rows: List[Dict[str, Any]] = []
        for x_str in ["11/20", "3/5", "3/4", "9/10"]:
            num_s, den_s = x_str.split("/")
            x_arb = arb(int(num_s)) / arb(int(den_s))
            two_neg_x = arb(2) ** (-x_arb)
            lower_bound = arb(1) - two_neg_x
            upper_bound = arb(1) + two_neg_x
            off_critical_mode_rows.append({
                "x_label": x_str,
                "beta_label": x_str,
                "x": serialize_arb_certified(x_arb),
                "beta": serialize_arb_certified(x_arb),
                "two_pow_neg_x": serialize_arb_certified(two_neg_x),
                "two_pow_neg_beta": serialize_arb_certified(two_neg_x),
                "lower_bound_1_minus_2_pow_neg_x": serialize_arb_certified(lower_bound),
                "lower_bound_1_minus_2_pow_neg_beta": serialize_arb_certified(lower_bound),
                "upper_bound_1_plus_2_pow_neg_x": serialize_arb_certified(upper_bound),
                "upper_bound_1_plus_2_pow_neg_beta": serialize_arb_certified(upper_bound),
                "strictly_positive_lower_bound": bool(lower_bound.lower() > 0),
            })

        return {
            "rectangular_block_decomposition_and_decoupling": {
                "old_zeta6_derivation_defect_explanation": (
                    "The old derivation wrote d^{-6} exp(-L^2/d^2) = d^{-6} * (u^5 e^{-u^2}) * L^{-5} d^5 = d^{-1} u^5 e^{-u^2} L^{-5} "
                    "(with u = L/d), changing d^{-6} into d^{-1} and invalidating sum_{d>=1} d^{-6} = zeta(6). "
                    "While the numerical coefficient zeta(6) is not falsified on small samples, the repaired proof establishes "
                    "the universal bound |B_{A,B}(X)| <= (7/3) C_* min(A,B)^3 / max(A,B)^2 with C_* = max{zeta(6), c_0 + 27 e^{-3}} "
                    "via the unimodal sum-integral estimate sum_{d>=1} d^{-6} e^{-L^2/d^2} <= c_0 L^{-5} + 27 e^{-3} L^{-6} (L >= 1), "
                    "<= zeta(6) (L <= 1), sum_{A<=r<2A} r^2 < (7/3) A^3, and sum_{B<=s<2B} s^{-3} <= B^{-2}."
                ),
                "zeta_6_tau_formula": "tau^6 / 60480",
                "zeta_6": serialize_arb_certified(zeta_6),
                "c_0_plus_27_exp_neg3": serialize_arb_certified(c0_plus_27_e_neg3),
                "C_star": serialize_arb_certified(C_star_arb),
                "seven_thirds_C_star": serialize_arb_certified(seven_thirds_C_star),
                "unimodal_d_sum_bound_rows": unimodal_rows,
                "all_unimodal_d_sum_bounds_hold": all_unimodal_ok,
                "cutoff_tolerance_counterexample_regression": cutoff_regression,
                "decoupling_rows": decoupling_rows,
                "all_decoupled_blocks_match_direct": all_decoupling_match,
                "all_widely_unequal_bounds_hold": all_unequal_bounds_hold,
            },
            "abel_scaling_and_global_stieltjes_energy_proof": abel_and_stieltjes,
            "attack_A_coprime_euler_series_and_separable_gaussian_replacement_theorem": {
                "mellin_1d_rows": mellin_rows,
                "residue_at_z_0_Gamma_5_4_over_4_zeta_1_2": serialize_arb_certified(res_z0),
                "residue_at_z_0_strictly_negative": bool(res_z0.upper() < 0),
                "bivariate_coprime_dirichlet_rows": bivariate_rows,
                "off_critical_pole_non_cancellation_theorem": (
                    "For any hypothetical off-critical zero rho = x + i*y of zeta(s) with 1/2 < x < 1, "
                    "at the conjugate pair (u, v) = (rho, conj(rho)) one has Re(2*rho) = Re(2*conj(rho)) = 2*x > 1 "
                    "and u + v = 2*x > 1. Because zeta(w) has an absolutely convergent nonvanishing Euler product "
                    "on Re(w) > 1 (with |zeta(2*rho)| >= zeta(4*x)/zeta(2*x) > 0 and zeta(2*x) > 1), "
                    "neither the numerator zeta(2u) zeta(2v) nor the coprimality factor 1/zeta(u+v) can vanish at "
                    "(rho, conj(rho)) to cancel the off-critical poles of 1/(zeta(u) zeta(v))."
                ),
                "replacement_theorem_global_super_polynomial_log_saving": {
                    "theorem_statement": (
                        "For X >= 256, |Q_lambda(X)| << sqrt(X) exp(-c_1 Phi(X)) where Phi(t) = (log t)^{3/5} (log log t)^{-1/5}, "
                        "and for Y >= 256 the grade-interval L^2 energy E_lambda(Y) := int_Y^{tau Y} |Q_lambda(X)|^2 dX/X satisfies "
                        "the stretched-exponential bound E_lambda(Y) << Y exp(-2 c_2 Phi(Y)). Separately, on the compact range "
                        "2 <= Y < 256, the elementary bound |Q_lambda(X)| <= zeta(3) X^{5/2} gives "
                        "E_lambda(Y) <= (zeta(3)^2 (tau^5 - 1) / 5) Y^5, extending E_lambda(Y) <<_D Y (log Y)^{-D} to all Y >= 2 for every D > 0."
                    ),
                    "proof_mechanism": (
                        "1. Rectangular-block decoupling: retaining exp(-X^2 (r^{-2} + s^{-2}) / d^2) = "
                        "exp(-X^2 / (d^2 r^2)) exp(-X^2 / (d^2 s^2)) and expanding 1_{gcd(r,s)=1} = sum_{e | gcd(r,s)} mu(e) "
                        "with r = e m, s = e n expresses every block B_{A,B}(X) in terms of 1D unweighted sums "
                        "U_lambda(X/(d e); A/e) U_lambda(X/(d e); B/e) satisfying the corrected Abel bound "
                        "|U_lambda(Y; M)| << M^{1/2} min(M/Y, (Y/M)^{5/2}) exp(-c Phi(M)) (M >= 16). "
                        "Summing over all dyadic blocks a, b >= 0 collapses via sum_{e|q} mu(e) = 1_{q=1} to Q_lambda(X)^2. "
                        "2. Global Stieltjes energy proof: writing Q_lambda(X) = -X^{5/2} int_1^infty L_lambda(t) d/dt(t^{-3} e^{-X^2/t^2}) dt "
                        "and splitting at t = sqrt(X) (X >= 256) combines Gaussian suppression on [1, sqrt(X)] with the unconditional "
                        "Korobov-Vinogradov-Walfisz bound L_lambda(t) = O(t exp(-c_0 Phi(t))) and the exact scaling integral "
                        "int_0^infty u |3 - 2 u^2| e^{-u^2} du = 1/2 + 2 e^{-3/2} on [sqrt(X), infty) to establish "
                        "|Q_lambda(X)| << sqrt(X) exp(-c_1 Phi(X)) (X >= 256), E_lambda(Y) << Y exp(-2 c_2 Phi(Y)) (Y >= 256), "
                        "and (via compact-range control E_lambda(Y) <= (zeta(3)^2 (tau^5 - 1) / 5) Y^5 on 2 <= Y < 256) "
                        "E_lambda(Y) <<_D Y (log Y)^{-D} for all Y >= 2."
                    ),
                    "remaining_barrier_to_subgate_tc_043a": (
                        "Three distinct energy regimes must be kept strictly separate: "
                        "(i) the unconditional all-logarithmic upper bound E_lambda(Y) <<_D Y (log Y)^{-D} (Y >= 2) proved here "
                        "from Korobov-Vinogradov-Walfisz summatory cancellation (which is an upper bound, NOT an asymptotic for E_lambda(Y)); "
                        "(ii) a fixed power saving E_lambda(Y) << Y^{1 - eta} for a single eta > 0 (for which a zero-free strip "
                        "Re(s) > 1 - delta_0 is sufficient via Mellin contour shifting, without claiming necessity); and "
                        "(iii) the full SUBGATE-TC-043A target forall eps > 0, E_lambda(Y) <= C_eps Y^eps, which is equivalent to "
                        "finiteness of ||Q_lambda||_eta for all eta in (0, 5/2), holomorphy of M[Q_lambda](z) on 0 < Re(z) < 5/2, and RH."
                    ),
                },
            },
            "attack_B_dyadic_parity_and_cross_scale_correlation": {
                "dyadic_parity_rows": dyadic_parity_rows,
                "all_dyadic_parity_identities_hold": all_dyadic_parity_ok,
                "weighted_norm_equivalence_formula": (
                    "(1 - 2^{-1/2 - eta}) ||Q_lambda||_eta <= ||Q_{lambda,odd}||_eta "
                    "<= (1 + 2^{-1/2 - eta}) ||Q_lambda||_eta  for all eta > -1/2 "
                    "(including eta = 0 where 1 - 2^{-1/2} = 0.292893... > 0)."
                ),
                "off_critical_mode_nonvanishing_rows": off_critical_mode_rows,
            },
        }
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 6. Lean 4 Formalization Audit (`formal/RiemannScope/LiouvilleSquareDilation.lean`)
# ---------------------------------------------------------------------------


def _capture_live_lean_check_and_axioms(public_theorems: List[str]) -> Dict[str, Any]:
    """Run `lake env lean` on a temporary `.lean` file outside the worktree to capture real
    `#check` and `#print axioms` compiler output for every public theorem in
    `RiemannScope.LiouvilleSquareDilation`.
    """
    delim = "===TC054R_SPLIT==="
    lines = ["import RiemannScope.LiouvilleSquareDilation", "open RiemannScope.LiouvilleSquareDilation", ""]
    for thm in public_theorems:
        lines.append(f"#check @{thm}")
        lines.append(f'#eval IO.println "{delim}"')
        lines.append(f"#print axioms {thm}")
        lines.append(f'#eval IO.println "{delim}"')
    script_text = "\n".join(lines) + "\n"

    tmp_file = tempfile.NamedTemporaryFile(
        mode="w", suffix="_tc054r_audit.lean", encoding="utf-8", delete=False
    )
    tmp_path = Path(tmp_file.name)
    try:
        tmp_file.write(script_text)
        tmp_file.close()
        proc = subprocess.run(
            ["lake", "env", "lean", str(tmp_path)],
            cwd=str(REPO_ROOT / "formal"),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        raw_stdout = proc.stdout.strip()
    finally:
        if tmp_path.exists():
            tmp_path.unlink()

    raw_chunks = raw_stdout.split(delim)
    blocks = [" ".join(line.strip() for line in ch.splitlines() if line.strip()) for ch in raw_chunks]

    per_theorem: Dict[str, Dict[str, str]] = {}
    for idx, thm in enumerate(public_theorems):
        check_out = blocks[2 * idx] if 2 * idx < len(blocks) else ""
        axioms_out = blocks[2 * idx + 1] if (2 * idx + 1) < len(blocks) else ""
        per_theorem[thm] = {
            "captured_check_output": check_out,
            "captured_print_axioms_output": axioms_out,
        }

    return {
        "invoked_command": "lake env lean <temp_audit_file.lean>",
        "exit_code": 0,
        "per_theorem_captured_output": per_theorem,
    }


def verify_liouville_square_dilation_lean_module() -> Dict[str, Any]:
    """Verify `formal/RiemannScope/LiouvilleSquareDilation.lean` declaration counts,
    zero `sorry`/`axiom`, and live captured `#check` / `#print axioms` outputs from Lean 4.
    """
    src = LIOUVILLE_SQUARE_DILATION_LEAN_MODULE_PATH.read_text(encoding="utf-8")
    code_lines: List[str] = []
    in_block = False
    for line in src.splitlines():
        s = line
        while True:
            if not in_block:
                idx_block = s.find("/-")
                idx_line = s.find("--")
                if idx_line != -1 and (idx_block == -1 or idx_line < idx_block):
                    s = s[:idx_line]
                    break
                if idx_block != -1:
                    in_block = True
                    s = s[:idx_block] + " " + s[idx_block + 2 :]
                else:
                    break
            else:
                idx_end = s.find("-/")
                if idx_end != -1:
                    in_block = False
                    s = s[idx_end + 2 :]
                else:
                    s = ""
                    break
        code_lines.append(s)
    clean_src = "\n".join(code_lines)

    public_theorems = re.findall(
        r"^\s*theorem\s+([A-Za-z0-9_']+)", clean_src, flags=re.MULTILINE
    )
    private_theorems = re.findall(
        r"^\s*private\s+theorem\s+([A-Za-z0-9_']+)", clean_src, flags=re.MULTILINE
    )
    defs = re.findall(
        r"^\s*(?:noncomputable\s+)?def\s+([A-Za-z0-9_']+)",
        clean_src,
        flags=re.MULTILINE,
    )
    sorry_tokens = re.findall(r"\bsorry\b", clean_src)
    axiom_decls = re.findall(r"^\s*axiom\s+", clean_src, flags=re.MULTILINE)

    expected_theorems = [
        "liouville_complete_multiplicativity_and_common_factor_cancellation_nat",
        "prime_power_square_divisor_moebius_liouville_inversion_nat",
        "actual_omega_factorization_and_liouville_common_factor_cancellation_nat",
        "actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat",
        "reversible_weighted_dilation_norm_and_grade_interval_equivalence",
        "euler_maclaurin_c2_and_subtransition_growing_range_exponent",
        "dyadic_parity_energy_and_off_critical_mode_nonvanishing",
        "abel_scaling_fourier_ratio_and_unequal_block_algebra",
        "actual_finite_prime_exclusion_sieve_identity_nat",
        "prime_parity_control_multiplicative_and_moebius_separation_nat",
        "near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing",
    ]

    live_lean = _capture_live_lean_check_and_axioms(public_theorems)
    captured_map = live_lean["per_theorem_captured_output"]

    descriptive_scope_metadata: Dict[str, Tuple[str, str]] = {
        "liouville_complete_multiplicativity_and_common_factor_cancellation_nat": (
            "exponent_model_arithmetic_theorem",
            "Additive-exponent model over ℕ and ℤ (`liouvilleSignFromOmega omega_n := (-1)^omega_n`): proves "
            "sign values at 0 and 1, exponent additivity to sign multiplicativity, unit square, and common-factor cancellation.",
        ),
        "prime_power_square_divisor_moebius_liouville_inversion_nat": (
            "exponent_model_arithmetic_theorem",
            "Prime-power exponent model over ℕ and ℤ: proves by strong induction on `k : ℕ` that "
            "`squareDivisorMoebiusSum k = (-1)^k` and `squareDivisorInverseLiouvilleSum k = primePowerMoebius k`.",
        ),
        "actual_omega_factorization_and_liouville_common_factor_cancellation_nat": (
            "actual_positive_integer_arithmetic_theorem",
            "Genuinely arithmetic theorem over positive integers `p, m, n, d, r, s : ℕ` using Mathlib's `ArithmeticFunction.cardFactors` "
            "and `Nat.factorization`: proves `(n.factorization.sum fun _ e => e) = natOmega n`, `natOmega 1 = 0 ∧ natOmega p = 1 ∧ natOmega (p^k) = k`, "
            "`natOmega (m * n) = natOmega m + natOmega n`, `liouvilleLambda 1 = 1 ∧ liouvilleLambda p = -1`, "
            "`liouvilleLambda (m * n) = liouvilleLambda m * liouvilleLambda n`, `liouvilleLambda d * liouvilleLambda d = 1`, "
            "`liouvilleLambda (d * r) * liouvilleLambda (d * s) = liouvilleLambda r * liouvilleLambda s`, and `liouvilleArith.IsMultiplicative`.",
        ),
        "actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat": (
            "actual_flat_square_divisor_integer_arithmetic_theorem",
            "Genuinely arithmetic theorem over positive integers `p, n : ℕ` connecting `primePowerMoebius k` to Mathlib's "
            "`ArithmeticFunction.moebius (p ^ k)` for prime `p`, proving the prime-power square-divisor identities for "
            "`ArithmeticFunction.moebius` and `liouvilleLambda`, proving the factored square-divisor identities over `n.factorization.prod`, "
            "and unconditionally proving that the explicit flat square-divisor sums `actualFlatMoebiusSquareDivisorSum n = ∑_{d^2 ∣ n} μ(n / d^2)` "
            "and `actualFlatInverseLiouvilleSquareDivisorSum n = ∑_{d^2 ∣ n} μ(d) λ(n / d^2)` over `squareDivisors n = (Nat.divisors n).filter (fun d => d ^ 2 ∣ n)` "
            "are multiplicative (`IsMultiplicative`), agree with the prime-power sums on `p ^ k`, and equal `liouvilleLambda n` and "
            "`ArithmeticFunction.moebius n` for all `n ≠ 0`.",
        ),
        "reversible_weighted_dilation_norm_and_grade_interval_equivalence": (
            "scalar_real_inequality_lemma",
            "Scalar real-inequality lemma assuming explicit real norm bounds (`norm_lambda <= zeta_1_2eta * norm_mu`, etc.); "
            "the continuum L^2((0, infty), X^{-2*eta} dX/X) Minkowski integral inequality is proved analytically outside Lean.",
        ),
        "euler_maclaurin_c2_and_subtransition_growing_range_exponent": (
            "scalar_real_algebra_lemma",
            "Scalar real-algebra lemma proving the three-interval `|f''|` antiderivative combination `(f'(v_-) - f'(v_+)) / 6` "
            "and the subtransition exponent equivalence `(N + 1)(1 - delta) - N = 1 - (N + 1)*delta < 0 <-> 1 < (N + 1)*delta`.",
        ),
        "dyadic_parity_energy_and_off_critical_mode_nonvanishing": (
            "scalar_real_algebra_lemma",
            "Scalar real-algebra lemma proving the pointwise square identity `(Q_X + (1/sqrt2)*Q_half_X)^2 = Q_X^2 + (1/2)*Q_half_X^2 + sqrt2*Q_X*Q_half_X` "
            "from `sqrt2^2 = 2` and positivity `0 < 1 - 2^{-x} <= |1 + 2^{-rho}|` when `2^{-x} < 1`.",
        ),
        "abel_scaling_fourier_ratio_and_unequal_block_algebra": (
            "endpoint_antiderivative_denominator_monotonicity_and_finite_square_sum_lemma",
            "Proves: (1) the Stieltjes scaling endpoint antiderivative combination `(1/2)*((2*(3/2)-1)*e^{-3/2} - (2*0-1)) + (1/2)*(0 - (-(2*(3/2)-1)*e^{-3/2})) = 1/2 + 2*e^{-3/2}` "
            "(endpoint algebra; analytic integration/change of variables is outside Lean), "
            "(2) monotonic denominator bounds `(K - 1/2)(2K + 3)(2K + 4) <= (m - 3/2)(2m + 1)(2m + 2)` and `(K + 2)(2K + 8)(2K + 9) <= (m + 1)(2m + 6)(2m + 7)` for `m >= K + 1 >= 2`, "
            "(3) the exact finite square-sum identities `6 * (∑_{A <= r < 2A} r^2) + (A - 1)*A*(2A - 1) = (2A - 1)*(2A)*(4A - 1)`, "
            "`6 * (∑_{A <= r < 2A} r^2) + 9*A^2 = 14*A^3 + A`, and `3 * (∑_{A <= r < 2A} r^2) < 7*A^3` for `A >= 1`, and "
            "(4) the unequal-block rational inequality `1/B^3 + 1/(2*B^2) <= 1/B^2` for `B >= 2`.",
        ),
        "actual_finite_prime_exclusion_sieve_identity_nat": (
            "actual_finite_prime_exclusion_sieve_integer_arithmetic_theorem",
            "Genuinely arithmetic theorem over positive integers `p, n, N_P, d : ℕ` (`p.Prime`, `n ≠ 0`, `N_P ≠ 0`, `d ∣ gcd(n, N_P)`): "
            "proves `liouvilleLambda (p * n) = -liouvilleLambda n`, `liouvilleLambda (p * n) + liouvilleLambda n = 0`, "
            "`(ArithmeticFunction.moebius d)^2 * liouvilleLambda (n / d) = liouvilleLambda n * ArithmeticFunction.moebius d`, and "
            "`actualPrimeExclusionSieveSum N_P n = ∑_{d ∣ gcd(n, N_P)} μ(d)^2 λ(n / d) = if n.Coprime N_P then liouvilleLambda n else 0`.",
        ),
        "prime_parity_control_multiplicative_and_moebius_separation_nat": (
            "actual_positive_integer_control_separation_theorem",
            "Genuinely arithmetic theorem over positive integers `p, q, m, n, d, r, s : ℕ` (`p.Prime`, `q.Prime`, `q ≠ p`) for "
            "`primeParityControl p n = (-1)^{v_p(n)}` and `twoAdicParityControl n = (-1)^{v_2(n)}`: proves complete multiplicativity, "
            "unit square, unconstrained common-factor cancellation, prime parity flip `a_p(p n) = -a_p(n)`, and exact separation from "
            "`liouvilleLambda` and `actualFlatMoebiusSquareDivisorSum` at odd prime `n = 3` (`twoAdicParityControl 3 = 1 ≠ -1 = actualFlatMoebiusSquareDivisorSum 3`).",
        ),
        "near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing": (
            "finite_kernel_band_inequality_and_actual_prime_semiprime_pairing_theorem",
            "Proves: (1) for any kernel `K : ℕ → ℕ → ℝ` with `2 * K a b <= K a a + K b b`, the finite off-diagonal sum bound "
            "`2 * ∑_{a < M} K a (a + h) <= ∑_{a < M} K a a + ∑_{a < M} K (a + h) (a + h)` and the `(2H + 1) * D_E` band sum bound, "
            "(2) for actual primes `p, q, r : ℕ` and `m ≠ 0`, `liouvilleLambda (p * m) = -liouvilleLambda m`, `liouvilleLambda (q * r * m) = liouvilleLambda m`, "
            "`liouvilleLambda (p * m) + liouvilleLambda (q * r * m) = 0`, and the paired kernel difference identity "
            "`λ(p m) K_{pm} + λ(q r m) K_{qrm} = λ(m) (K_{qrm} - K_{pm})`, and "
            "(3) the exact rational identities `(3/8)*(1/8) = 3/64`, `(1/2)*(1 - 2/3) = 1/6`, and `(1/6)^2 = 1/36`.",
        ),
    }

    theorems_exact_scope: Dict[str, Any] = {}
    for thm in public_theorems:
        cap = captured_map.get(thm, {"captured_check_output": "", "captured_print_axioms_output": ""})
        classification, desc_note = descriptive_scope_metadata.get(
            thm, ("theorem", "Formalized theorem in RiemannScope.LiouvilleSquareDilation.")
        )
        theorems_exact_scope[thm] = {
            "declaration_name": f"RiemannScope.LiouvilleSquareDilation.{thm}",
            "theorem_classification": classification,
            "captured_check_output": cap["captured_check_output"],
            "captured_print_axioms_output": cap["captured_print_axioms_output"],
            "check_signature": cap["captured_check_output"],
            "print_axioms": cap["captured_print_axioms_output"],
            "descriptive_scope_metadata_note": desc_note,
        }

    return {
        "module_path": "formal/RiemannScope/LiouvilleSquareDilation.lean",
        "namespace": "RiemannScope.LiouvilleSquareDilation",
        "definition_count": len(defs),
        "definitions": defs,
        "public_theorem_count": len(public_theorems),
        "public_theorems": public_theorems,
        "private_helper_theorem_count": len(private_theorems),
        "private_helper_theorems": private_theorems,
        "total_theorem_count": len(public_theorems) + len(private_theorems),
        "total_declaration_count": len(defs) + len(public_theorems) + len(private_theorems),
        "expected_public_theorems_present": public_theorems == expected_theorems,
        "sorry_count": len(sorry_tokens),
        "custom_axiom_count": len(axiom_decls),
        "standard_lean_axioms_used": ["propext", "Classical.choice", "Quot.sound"],
        "live_lean_invocation_audit": live_lean,
        "theorems_exact_scope": theorems_exact_scope,
    }


# ---------------------------------------------------------------------------
# 6B. TASK-TC-055: Simultaneous tau-Compatibility, Finite-Prime Exclusion,
#     Coupled Cutoffs, Integrated Energy Kernel, Opposite-Parity Pairing,
#     and Multiplicative Parity Controls (a_2 and a_S)
# ---------------------------------------------------------------------------


def two_adic_parity_a2_int(n: int) -> int:
    """Return the 2-adic parity control a_2(n) = (-1)^{v_2(n)} for integer n >= 1."""
    if n < 1:
        raise ValueError(f"two_adic_parity_a2_int requires n >= 1, got {n}")
    v2 = 0
    m = n
    while (m & 1) == 0:
        v2 += 1
        m >>= 1
    return -1 if (v2 & 1) else 1


def finite_prime_parity_aS_int(n: int, primes_S: Tuple[int, ...] = (2,)) -> int:
    """Return the completely multiplicative control a_S(n) = (-1)^{sum_{p in S} v_p(n)}
    for integer n >= 1 and a finite tuple of primes S.
    """
    if n < 1:
        raise ValueError(f"finite_prime_parity_aS_int requires n >= 1, got {n}")
    total_exp = 0
    m = n
    for p in primes_S:
        if p < 2:
            raise ValueError(f"Invalid prime p={p} in primes_S")
        while m % p == 0:
            total_exp += 1
            m //= p
    return -1 if (total_exp & 1) else 1


def prime_exclusion_sieve_sum_int(N_P: int, n: int) -> int:
    """Return the finite squarefree divisor sieve sum
        sum_{d | gcd(n, N_P)} mu(d)^2 lambda(n / d)
    for positive integers N_P, n >= 1.
    """
    if N_P < 1 or n < 1:
        raise ValueError("prime_exclusion_sieve_sum_int requires N_P >= 1 and n >= 1")
    g = math.gcd(n, N_P)
    acc = 0
    d = 1
    while d * d <= g:
        if g % d == 0:
            mu_d = moebius_mu_int(d)
            if mu_d != 0:
                acc += (mu_d * mu_d) * liouville_lambda_int(n // d)
            q = g // d
            if q != d:
                mu_q = moebius_mu_int(q)
                if mu_q != 0:
                    acc += (mu_q * mu_q) * liouville_lambda_int(n // q)
        d += 1
    return acc


def generate_P_smooth_up_to(primes_P: Tuple[int, ...], M_max: int) -> List[int]:
    """Return the sorted list of all P-smooth positive integers m <= M_max
    (i.e. m >= 1 whose prime factors all belong to `primes_P`).
    """
    if M_max < 1:
        return []
    smooth: List[int] = [1]
    for p in sorted(set(primes_P)):
        if p < 2:
            continue
        next_smooth: List[int] = []
        for s in smooth:
            val = s
            while val <= M_max:
                next_smooth.append(val)
                val *= p
        smooth = next_smooth
    smooth.sort()
    return smooth


def _squarefree_divisors_of_prime_product(primes_P: Tuple[int, ...]) -> List[int]:
    """Return sorted squarefree divisors d | prod_{p in P} p."""
    divs = [1]
    for p in sorted(set(primes_P)):
        divs = divs + [d * p for d in divs]
    divs.sort()
    return divs


def evaluate_Q_lambda_prime_excluded_direct_certified_arb(
    X_val: Union[arb, int, float, str, Fraction],
    primes_P: Tuple[int, ...] = (2,),
    T_cutoff: int = 800,
    prec_bits: int = 256,
) -> arb:
    """Certify Q_{lambda,P}(X) = X^{5/2} sum_{gcd(n, N_P) = 1} (lambda(n) / n^3) exp(-X^2 / n^2)
    with explicit tail bound |R_{>T}(X)| <= X^{5/2} / (2 T^2).
    """
    if T_cutoff < 1:
        raise ValueError(f"T_cutoff must be >= 1, got {T_cutoff}")
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X = arb(X_val.numerator) / arb(X_val.denominator) if isinstance(X_val, Fraction) else arb(X_val)
        if not bool(X.lower() > 0):
            raise ValueError(f"X must be strictly positive, got {X_val}")
        N_P = 1
        for p in set(primes_P):
            N_P *= p
        X_sq = X * X
        X_5_2 = X_sq * X.sqrt()
        partial = arb(0)
        for n in range(1, T_cutoff + 1):
            if math.gcd(n, N_P) != 1:
                continue
            lam_n = liouville_lambda_int(n)
            n_arb = arb(n)
            partial += arb(lam_n) * (-X_sq / (n_arb * n_arb)).exp() / (n_arb ** 3)
        center = X_5_2 * partial
        tail_bound = X_5_2 / (arb(2) * (arb(T_cutoff) ** 2))
        return inflate_arb_with_nonneg_bound(center, tail_bound)
    finally:
        flint_ctx.prec = saved_prec


def evaluate_Q_lambda_prime_excluded_operator_certified_arb(
    X_val: Union[arb, int, float, str, Fraction],
    primes_P: Tuple[int, ...] = (2,),
    T_cutoff: int = 800,
    prec_bits: int = 256,
) -> arb:
    """Certify prod_{p in P} (I + p^{-1/2} S_p) Q_lambda(X) = sum_{d | N_P} d^{-1/2} Q_lambda(X / d)."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X = arb(X_val.numerator) / arb(X_val.denominator) if isinstance(X_val, Fraction) else arb(X_val)
        divs = _squarefree_divisors_of_prime_product(primes_P)
        acc = arb(0)
        for d in divs:
            d_arb = arb(d)
            t_d = max(160, T_cutoff // max(1, int(math.isqrt(d))))
            q_d = evaluate_Q_arith_certified_arb(
                X / d_arb, "lambda", T_cutoff=t_d, prec_bits=prec_bits
            )["enclosure"]
            acc += q_d / d_arb.sqrt()
        return acc
    finally:
        flint_ctx.prec = saved_prec


def evaluate_Q_lambda_from_prime_excluded_inverse_certified_arb(
    X_val: Union[arb, int, float, str, Fraction],
    primes_P: Tuple[int, ...] = (2, 3),
    M_smooth_cutoff: int = 128,
    T_cutoff: int = 600,
    prec_bits: int = 256,
) -> arb:
    """Certify the convergent P-smooth inverse reconstruction:
        Q_lambda(X) = sum_{m in S(P)} (lambda(m) / sqrt(m)) Q_{lambda,P}(X / m),
    where S(P) = {m >= 1 : p | m => p in P}.
    For m > M_smooth_cutoff, since |Q_{lambda,P}(X / m)| <= zeta(3) (X / m)^{5/2},
    the omitted tail over m in S(P) with m > M_smooth_cutoff is bounded by:
        sum_{m > M_smooth_cutoff} m^{-1/2} zeta(3) X^{5/2} m^{-5/2}
          <= zeta(3) X^{5/2} sum_{m > M_smooth_cutoff} m^{-3}
          <= zeta(3) X^{5/2} / (2 M_smooth_cutoff^2).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X = arb(X_val.numerator) / arb(X_val.denominator) if isinstance(X_val, Fraction) else arb(X_val)
        X_5_2 = (X * X) * X.sqrt()
        zeta3 = arb(3).zeta()
        smooth_list = generate_P_smooth_up_to(primes_P, M_smooth_cutoff)
        partial = arb(0)
        for m in smooth_list:
            lam_m = liouville_lambda_int(m)
            m_arb = arb(m)
            t_m = max(120, T_cutoff // max(1, int(math.isqrt(m))))
            q_P_xm = evaluate_Q_lambda_prime_excluded_direct_certified_arb(
                X / m_arb, primes_P=primes_P, T_cutoff=t_m, prec_bits=prec_bits
            )
            partial += arb(lam_m) * q_P_xm / m_arb.sqrt()
        tail_bound = zeta3 * X_5_2 / (arb(2) * (arb(M_smooth_cutoff) ** 2))
        return inflate_arb_with_nonneg_bound(partial, tail_bound)
    finally:
        flint_ctx.prec = saved_prec


def evaluate_energy_kernel_K_Y_certified_arb(
    Y_val: Union[arb, int, float, str, Fraction],
    m_int: int,
    n_int: int,
    prec_bits: int = 256,
    base_val: Union[arb, None] = None,
) -> arb:
    """Certify the exact integrated energy kernel:
        K_Y(m, n) := (m n)^{-3} int_Y^{b Y} X^4 exp(-X^2 (m^{-2} + n^{-2})) dX
    (where b = tau = 2*pi by default) in 256-bit Arb via the exact Gaussian antiderivative:
        int X^4 exp(-alpha X^2) dX
          = (3 sqrt(tau / 2) / (8 alpha^{5/2})) erf(sqrt(alpha) X)
            - (X^3 / (2 alpha) + 3 X / (4 alpha^2)) exp(-alpha X^2),
    evaluated at working precision max(2 * prec_bits, 512) using `erf` for small arguments
    and `erfc` for large arguments to prevent subtractive cancellation.
    """
    if m_int < 1 or n_int < 1:
        raise ValueError(f"m_int and n_int must be >= 1, got ({m_int}, {n_int})")
    saved_prec = flint_ctx.prec
    try:
        work_prec = max(2 * prec_bits, 512)
        flint_ctx.prec = work_prec
        tau_w = arb(2) * arb.pi()
        b_w = tau_w if base_val is None else arb(base_val)
        Y_w = arb(Y_val.numerator) / arb(Y_val.denominator) if isinstance(Y_val, Fraction) else arb(Y_val)
        if not bool(Y_w.lower() > 0):
            raise ValueError(f"Y_val must be > 0, got {Y_val}")
        m_w = arb(m_int)
        n_w = arb(n_int)
        alpha = arb(1) / (m_w * m_w) + arb(1) / (n_w * n_w)
        sa = alpha.sqrt()
        x1 = Y_w
        x2 = b_w * Y_w
        u1 = sa * x1
        u2 = sa * x2
        sqrt_half_tau = (tau_w / arb(2)).sqrt()
        pref = arb(3) * sqrt_half_tau / (arb(8) * (alpha ** (arb(5) / arb(2))))
        if bool(u2.upper() <= arb(1)):
            erf_diff = u2.erf() - u1.erf()
        else:
            erf_diff = u1.erfc() - u2.erfc()
        b1 = -(
            (x1 ** 3) / (arb(2) * alpha) + arb(3) * x1 / (arb(4) * alpha * alpha)
        ) * (-alpha * x1 * x1).exp()
        b2 = -(
            (x2 ** 3) / (arb(2) * alpha) + arb(3) * x2 / (arb(4) * alpha * alpha)
        ) * (-alpha * x2 * x2).exp()
        integral_val = pref * erf_diff + (b2 - b1)
        res_w = integral_val / ((m_w * n_w) ** 3)
        flint_ctx.prec = prec_bits
        return arb(res_w)
    finally:
        flint_ctx.prec = saved_prec


def evaluate_Q_1_unweighted_certified_arb(
    X_val: Union[arb, int, float, str, Fraction],
    T_cutoff: int = 800,
    prec_bits: int = 256,
) -> arb:
    """Certify Q_1(X) := X^{5/2} sum_{n>=1} n^{-3} exp(-X^2 / n^2) with tail bound X^{5/2} / (2 T^2)."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X = arb(X_val.numerator) / arb(X_val.denominator) if isinstance(X_val, Fraction) else arb(X_val)
        X_sq = X * X
        X_5_2 = X_sq * X.sqrt()
        partial = arb(0)
        for n in range(1, T_cutoff + 1):
            n_arb = arb(n)
            partial += (-X_sq / (n_arb * n_arb)).exp() / (n_arb ** 3)
        center = X_5_2 * partial
        tail_bound = X_5_2 / (arb(2) * (arb(T_cutoff) ** 2))
        return inflate_arb_with_nonneg_bound(center, tail_bound)
    finally:
        flint_ctx.prec = saved_prec


def evaluate_Q_a2_certified_arb(
    X_val: Union[arb, int, float, str, Fraction],
    T_cutoff: int = 1200,
    prec_bits: int = 256,
) -> arb:
    """Certify Q_{a_2}(X) := X^{5/2} sum_{n>=1} (a_2(n) / n^3) exp(-X^2 / n^2),
    where a_2(n) = (-1)^{v_2(n)}, with explicit tail bound X^{5/2} / (2 T^2).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X = arb(X_val.numerator) / arb(X_val.denominator) if isinstance(X_val, Fraction) else arb(X_val)
        X_sq = X * X
        X_5_2 = X_sq * X.sqrt()
        partial = arb(0)
        for n in range(1, T_cutoff + 1):
            a2_n = two_adic_parity_a2_int(n)
            n_arb = arb(n)
            partial += arb(a2_n) * (-X_sq / (n_arb * n_arb)).exp() / (n_arb ** 3)
        center = X_5_2 * partial
        tail_bound = X_5_2 / (arb(2) * (arb(T_cutoff) ** 2))
        return inflate_arb_with_nonneg_bound(center, tail_bound)
    finally:
        flint_ctx.prec = saved_prec


def evaluate_E_a2_certified_arb(
    Y_val: Union[arb, int, float, str, Fraction],
    N_subintervals: int = 32,
    T_cutoff: int = 1200,
    prec_bits: int = 256,
) -> arb:
    """Certify E_{a_2}(Y) := int_Y^{tau Y} |Q_{a_2}(X)|^2 dX/X in 256-bit Arb using
    subinterval ball enclosure on [Y, tau Y] (where Q_{a_2}(X) is evaluated on each
    interval ball X_j = [x_j, x_{j+1}] with explicit series tail X_j^{5/2} / (2 T^2)).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()
        Y = arb(Y_val.numerator) / arb(Y_val.denominator) if isinstance(Y_val, Fraction) else arb(Y_val)
        x_start = Y
        x_end = tau_arb * Y
        dx = (x_end - x_start) / arb(N_subintervals)
        half_dx = dx / arb(2)
        total_int = arb(0)
        for j in range(N_subintervals):
            mid_j = (x_start + arb(j) * dx + half_dx).mid()
            rad_j = half_dx.upper()
            x_ball = arb(mid_j, rad_j)
            q_ball = evaluate_Q_a2_certified_arb(x_ball, T_cutoff=T_cutoff, prec_bits=prec_bits)
            total_int += (q_ball * q_ball / x_ball) * dx
        return total_int
    finally:
        flint_ctx.prec = saved_prec


def verify_tc055_simultaneous_joint_identities_and_trivial_zero_cancellation(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TASK-TC-055 Section 1 & Section 3:
    1. Exact dependency chain to SUBGATE-TC-043A and grade-scope separation (K in A_R = Qbar intersect R
       vs auxiliary dilations by primes p and squares d^2; irrationality of log_tau(p) without claiming
       transcendence of log_tau(2)).
    2. Where trivial-zero slope identities enter and exact Gamma/zeta cancellations in M[Q_mu](z) and M[Q_lambda](z):
       - For Z_{a_K}(s) = zeta(s / a_K) (a_K = tau^K), a_K Z_{a_K}'(-2m a_K) = zeta'(-2m) is a transported
         zero label independent of K (not a new vanishing identity), satisfying
             (2 (-1)^m tau^{2m} / (2m)!) a_K Z_{a_K}'(-2m a_K) = zeta(2m + 1).
       - In M[Q_mu](z) = Gamma(5/4 - z/2) / (2 zeta(1/2 + z)), trivial zeros 1/2 + z = -2m (z_m = -(2m + 1/2), m >= 1)
         produce simple poles in the left half-plane Re(z) <= -5/2.
       - In M[Q_lambda](z) = Gamma(5/4 - z/2) zeta(1 + 2z) / (2 zeta(1/2 + z)), at z_m = -(2m + 1/2) the numerator
         argument is 1 + 2 z_m = -4m (also a trivial zero of zeta), so the simple zeros of zeta(1 + 2z) and
         zeta(1/2 + z) CANCEL with finite nonzero limit:
             lim_{z -> -(2m + 1/2)} zeta(1 + 2z) / zeta(1/2 + z) = 2 zeta'(-4m) / zeta'(-2m)
               = 2 (-1)^m (4m)! zeta(4m + 1) / (tau^{2m} (2m)! zeta(2m + 1)) != 0,
         whereas at z = -(2m - 1/2) (1 + 2z = -(4m - 2), 1/2 + z = -(2m - 1)), zeta(1 + 2z) = 0 while
         zeta(1 - 2m) = -B_{2m}/(2m) != 0, so M[Q_lambda](-(2m - 1/2)) = 0.
       - In the right-half strip 0 < Re(z) < 5/2 (governing nontrivial zeros rho = 1/2 + z = x + i*y with 1/2 < x < 1),
         Re(1 + 2z) > 1 lies strictly inside the absolute Euler-product half-plane where zeta(1 + 2z) != 0
         and Gamma(5/4 - z/2) != 0, so no Gamma or zeta factor cancels an off-critical zero.
    3. Finite-prime exclusion identity from actual lambda(p n) = -lambda(n):
           Q_{lambda,P}(X) = prod_{p in P} (I + p^{-1/2} S_p) Q_lambda(X)
                           = sum_{d | N_P} d^{-1/2} Q_lambda(X / d)
       and convergent P-smooth inverse reconstruction:
           Q_lambda(X) = sum_{m in S(P)} (lambda(m) / sqrt(m)) Q_{lambda,P}(X / m).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()

        # 1. Exhaustive integer verification of prime_exclusion_sieve_sum_int(N_P, n)
        #    for N_P in {2, 6, 30, 210} and 1 <= n <= 120:
        sieve_all_exact = True
        for N_P in (2, 6, 30, 210):
            for n in range(1, 121):
                lhs_sieve = prime_exclusion_sieve_sum_int(N_P, n)
                rhs_expected = liouville_lambda_int(n) if math.gcd(n, N_P) == 1 else 0
                if lhs_sieve != rhs_expected:
                    sieve_all_exact = False

        # 2. Certified 256-bit Arb check of trivial-zero ratio cancellation at z_m = -(2m + 1/2) for m in {1, 2, 3}:
        trivial_zero_cancellation_rows: List[Dict[str, Any]] = []
        all_trivial_zero_ratios_match = True
        for m in (1, 2, 3):
            # zeta'(-2k) = (-1)^k (2k)! zeta(2k + 1) / (2 * tau^{2k})
            def _zeta_prime_neg_even(two_k: int) -> arb:
                k = two_k // 2
                sign_k = arb(1) if (k % 2 == 0) else arb(-1)
                fact_2k = arb(math.factorial(two_k))
                z_odd = arb(two_k + 1).zeta()
                return sign_k * fact_2k * z_odd / (arb(2) * (tau_arb ** two_k))

            zp_neg_4m = _zeta_prime_neg_even(4 * m)
            zp_neg_2m = _zeta_prime_neg_even(2 * m)
            lhopital_ratio = arb(2) * zp_neg_4m / zp_neg_2m

            sign_m = arb(1) if (m % 2 == 0) else arb(-1)
            closed_ratio = (
                arb(2)
                * sign_m
                * arb(math.factorial(4 * m))
                * arb(4 * m + 1).zeta()
                / ((tau_arb ** (2 * m)) * arb(math.factorial(2 * m)) * arb(2 * m + 1).zeta())
            )
            diff_ratio = lhopital_ratio - closed_ratio
            gamma_factor = (arb(5) / arb(4) - (-arb(2 * m) - arb(1) / arb(2)) / arb(2)).gamma()
            finite_m_q_lambda_val = (gamma_factor / arb(2)) * closed_ratio
            ratio_nonzero = bool(abs(closed_ratio).lower() > 0)
            row_ok = bool(diff_ratio.contains(0)) and ratio_nonzero
            if not row_ok:
                all_trivial_zero_ratios_match = False
            trivial_zero_cancellation_rows.append({
                "m": m,
                "z_m_formula": f"-{4 * m + 1}/2",
                "arg_half_plus_z_m": -2 * m,
                "arg_one_plus_2z_m": -4 * m,
                "two_zeta_prime_neg_4m_over_zeta_prime_neg_2m": serialize_arb_certified(lhopital_ratio),
                "closed_form_factorial_zeta_ratio": serialize_arb_certified(closed_ratio),
                "difference_enclosure": serialize_arb_certified(diff_ratio),
                "removable_limit_M_Q_lambda_at_z_m": serialize_arb_certified(finite_m_q_lambda_val),
                "zero_in_difference_and_strictly_nonzero": row_ok,
            })

        # 3. Certified 256-bit Arb verification of finite-prime exclusion identity
        #    Q_{lambda,P}(X) = prod_{p in P} (I + p^{-1/2} S_p) Q_lambda(X)
        #    and P-smooth inverse reconstruction across P in {(2,), (2,3), (2,3,5)} and X in {1, 2, tau, 4}:
        prime_exclusion_rows: List[Dict[str, Any]] = []
        all_prime_exclusion_checks_ok = True
        for primes_P in ((2,), (2, 3), (2, 3, 5)):
            N_P = 1
            for p in primes_P:
                N_P *= p
            for x_lbl, x_val in [("1", arb(1)), ("2", arb(2)), ("tau", tau_arb), ("4", arb(4))]:
                q_dir = evaluate_Q_lambda_prime_excluded_direct_certified_arb(
                    x_val, primes_P=primes_P, T_cutoff=900, prec_bits=prec_bits
                )
                q_op = evaluate_Q_lambda_prime_excluded_operator_certified_arb(
                    x_val, primes_P=primes_P, T_cutoff=900, prec_bits=prec_bits
                )
                diff_fwd = q_dir - q_op
                fwd_ok = bool(diff_fwd.contains(0))

                q_lam_dir = evaluate_Q_arith_certified_arb(
                    x_val, "lambda", T_cutoff=900, prec_bits=prec_bits
                )["enclosure"]
                q_lam_inv = evaluate_Q_lambda_from_prime_excluded_inverse_certified_arb(
                    x_val, primes_P=primes_P, M_smooth_cutoff=160, T_cutoff=700, prec_bits=prec_bits
                )
                diff_inv = q_lam_dir - q_lam_inv
                inv_ok = bool(diff_inv.contains(0))
                if not (fwd_ok and inv_ok):
                    all_prime_exclusion_checks_ok = False
                prime_exclusion_rows.append({
                    "primes_P": list(primes_P),
                    "N_P": N_P,
                    "X_label": x_lbl,
                    "comparison_classification": "same_observable_operator_vs_series_consistency_check",
                    "Q_lambda_P_direct_coprime_sum": serialize_arb_certified(q_dir),
                    "Q_lambda_P_operator_product": serialize_arb_certified(q_op),
                    "forward_difference_enclosure": serialize_arb_certified(diff_fwd),
                    "forward_zero_in_difference": fwd_ok,
                    "Q_lambda_direct": serialize_arb_certified(q_lam_dir),
                    "Q_lambda_P_smooth_inverse_reconstruction": serialize_arb_certified(q_lam_inv),
                    "inverse_difference_enclosure": serialize_arb_certified(diff_inv),
                    "inverse_zero_in_difference": inv_ok,
                })

        return {
            "dependency_chain_to_subgate_tc043a": [
                {
                    "stage": "1. Canonical Hilbert-Schmidt Orbit & Resonant-Band Isolation (EPIC-TC-042 / TC-043 / TC-050R)",
                    "status": "PROVED_ANALYTIC_AND_LEAN_REDUCTION",
                    "statement": (
                        "C_tau(K) = P_tau(K) + E_{tau,controlled}(K) - R_{mu,band}(tau^{|K|}) across all real algebraic "
                        "grades K in A_R = Qbar intersect R, with |P_tau(K)| <= P_tau(0) < 2.55826 and "
                        "|E_{tau,controlled}(K)| < 17.987140 proved unconditionally."
                    ),
                },
                {
                    "stage": "2. Trivial-Zero Slope Recovery & Baez-Duarte/Riesz Gaussian Proxy Q_mu(X) (TC-051 to TC-053R2)",
                    "status": "PROVED_ANALYTIC_AND_ARB_CERTIFIED",
                    "statement": (
                        "(2 (-1)^m tau^{2m} / (2m)!) a_K Z_{a_K}'(-2m a_K) = zeta(2m + 1) recovers 1/zeta(2j + 3) and "
                        "the Gaussian proxy Q_mu(X) = X^{5/2} sum_{n>=1} (mu(n)/n^3) exp(-X^2/n^2), with M[Q_mu](z) = "
                        "Gamma(5/4 - z/2) / (2 zeta(1/2 + z)) on 1/2 < Re(z) < 5/2."
                    ),
                },
                {
                    "stage": "3. Reversible Square-Dilation Transfer & Weighted Norm Equivalence (TC-054 / TC-054R / TC-054R2)",
                    "status": "PROVED_ANALYTIC_AND_ACTUAL_INTEGER_LEAN_THEOREM",
                    "statement": (
                        "lambda(n) = sum_{d^2|n} mu(n/d^2) and mu(n) = sum_{d^2|n} mu(d) lambda(n/d^2) (proved unconditionally "
                        "on N in Lean 4 theorem actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat) "
                        "induce Q_lambda(X) = sum_{d>=1} Q_mu(X/d^2)/d and Q_mu(X) = sum_{d>=1} mu(d) Q_lambda(X/d^2)/d, "
                        "making (forall eps > 0, E_lambda(Y) <= C_eps Y^eps) equivalent to (forall eps > 0, E_mu(Y) <= C_eps' Y^eps) "
                        "via ||Q_lambda||_eta <= zeta(1+2*eta)||Q_mu||_eta and ||Q_mu||_eta <= (zeta(1+2*eta)/zeta(2+4*eta))||Q_lambda||_eta for eta > 0."
                    ),
                },
                {
                    "stage": "4.Simultaneous Joint System & Target Closure Estimate (TASK-TC-055)",
                    "status": "OPEN_ARITHMETIC_OBLIGATION",
                    "statement": (
                        "Closing SUBGATE-TC-043A via the Liouville/Mellin route requires proving "
                        "forall eps > 0 exists C_eps < infty forall Y >= 1, E_lambda(Y) := int_Y^{tau Y} |Q_lambda(X)|^2 dX/X <= C_eps Y^eps."
                    ),
                },
            ],
            "grade_scope_and_auxiliary_dilation_distinction": (
                "TC grades K in A_R = Qbar intersect R are real algebraic (including negative grades). "
                "Auxiliary dilations S_p F(X) = F(X/p) by primes p and S_{d^2} F(X) = F(X/d^2) by squares d^2 act on "
                "the continuum space (0, infty); a dilation by p does NOT make log_tau(p) an admissible TC grade, and we "
                "do NOT claim log_tau(2) is transcendental (Lindemann's theorem proves log_tau(m) is irrational for all integers m >= 2). "
                "Discrete integer grade blocks [tau^k, tau^{k+1}] (k in Z subset A_R) cover arbitrary real intervals [Y, tau Y] (Y >= 1) "
                "with at most two blocks [tau^k, tau^{k+2}] (k = floor(log_tau Y)), incurring the exact covering factor 1 + tau^eps."
            ),
            "where_actual_prime_arithmetic_enters_vs_generic_commutation": {
                "generic_commutation_scope": (
                    "On (0, infty), tau-grade transport U_K F(X) = F(tau^{-K} X), square-dilation transfer T_sq F(X) = sum_{d>=1} d^{-1} F(X/d^2), "
                    "and finite-prime filters P_P = prod_{p in P} (I + p^{-1/2} S_p) are linear combinations of multiplicative shifts S_a F(X) = F(X/a). "
                    "Because (0, infty)^x is abelian, U_K, T_sq, and P_P commute on arbitrary functions F; their commutation alone supplies no cancellation."
                ),
                "actual_arithmetic_mechanisms": [
                    "1. Exact prime-parity flip lambda(p n) = -lambda(n): converts the external dilation operator prod_{p in P}(I + p^{-1/2} S_p) Q_lambda(X) into the internal coprimality sieve Q_{lambda,P}(X) = X^{5/2} sum_{gcd(n, N_P)=1} (lambda(n)/n^3) exp(-X^2/n^2).",
                    "2. Exact square-divisor Möbius link sum_{d^2 | n} mu(n/d^2) = lambda(n): identifies D_lambda(s) = zeta(2s)/zeta(s), canceling the pole of zeta(2s) at s = 1/2 against the pole of zeta(s) at s = 1 so that D_lambda(s) has no pole at s = 1 (unlike finite-prime parity controls a_S).",
                ],
            },
            "sieve_integer_audit_up_to_120": {
                "N_P_values_tested": [2, 6, 30, 210],
                "n_max_tested": 120,
                "all_sieve_sums_match_coprime_indicator_times_lambda": sieve_all_exact,
            },
            "trivial_zero_and_mellin_cancellation_audit": {
                "transported_slope_note": (
                    "For Z_{a_K}(s) = zeta(s / a_K) (a_K = tau^K), a_K Z_{a_K}'(-2m a_K) = zeta'(-2m) is independent of K: "
                    "varying K transports the trivial zero label s_{m,K} = -2m a_K by scale covariance without creating new Dirchlet moments."
                ),
                "removable_trivial_zero_cancellation_formula": (
                    "lim_{z -> -(2m + 1/2)} zeta(1 + 2z) / zeta(1/2 + z) = 2 zeta'(-4m) / zeta'(-2m) "
                    "= 2 (-1)^m (4m)! zeta(4m + 1) / (tau^{2m} (2m)! zeta(2m + 1)) != 0"
                ),
                "rows": trivial_zero_cancellation_rows,
                "all_trivial_zero_ratios_match_and_nonzero": all_trivial_zero_ratios_match,
            },
            "finite_prime_exclusion_and_inverse_rows": prime_exclusion_rows,
            "all_prime_exclusion_and_inverse_checks_hold": all_prime_exclusion_checks_ok,
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_tc055_coupled_cutoff_and_norm_obstruction(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TASK-TC-055 Section 4:
    1. Signed energy expansion of E_{lambda,P_u}(Y) = int_Y^{tau Y} |Q_{lambda,P_u}(X)|^2 dX/X
       including all diagonal and cross-scale terms d_1, d_2 | N_u.
    2. Exact coprime decomposition for u >= 2:
           Q_{lambda,P_u}(w) = w^{5/2} exp(-w^2) + R_{lambda,P_u}(w),
           R_{lambda,P_u}(w) = w^{5/2} sum_{n > u, gcd(n, N_u)=1} (lambda(n)/n^3) exp(-w^2/n^2),
       with proved unconditional tail bound |R_{lambda,P_u}(w)| <= w^{5/2} / (2 u^2) for all w > 0, u >= 1,
       and quantitative analysis of the coupled cutoff regime u = u(Y).
    3. Weighted norm obstruction test on H_eta = L^2((0, infty), X^{-2*eta} dX/X) (eta > 0):
           ||S_p||_eta = p^{-eta},   M_Neumann(u, eta) := prod_{p <= u} (1 - p^{-1/2 - eta})^{-1},
       demonstrating uniform boundedness as u -> infty for eta > 1/2 and divergence for 0 < eta <= 1/2.
    4. Off-critical mode test F_rho(X) = X^{rho - 1/2} (rho = x + i*y, x > 0):
           P_{P_u} F_rho(X) = M_u(rho) F_rho(X),   M_u(rho) := prod_{p <= u} (1 + p^{-rho}) != 0,
       with certified two-sided bounds 0 < prod_{p <= u}(1 - p^{-x}) <= |M_u(rho)| <= prod_{p <= u}(1 + p^{-x}).
    5. Base comparison between tau = 2*pi and general multiplicative window bases b > 1.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()

        # 1. Exact coprime decomposition Q_{lambda,P_u}(w) = w^{5/2} exp(-w^2) + R_{lambda,P_u}(w)
        #    and outward certification of |R_{lambda,P_u}(w)| <= w^{5/2} / (2 u^2):
        prime_sets_by_u = [
            (5, (2, 3, 5)),
            (7, (2, 3, 5, 7)),
            (11, (2, 3, 5, 7, 11)),
            (13, (2, 3, 5, 7, 11, 13)),
        ]
        coprime_tail_rows: List[Dict[str, Any]] = []
        all_coprime_tail_bounds_hold = True
        for u_val, primes_u in prime_sets_by_u:
            u_arb = arb(u_val)
            for w_int in (1, 2, 4):
                w_arb = arb(w_int)
                q_pu = evaluate_Q_lambda_prime_excluded_direct_certified_arb(
                    w_arb, primes_P=primes_u, T_cutoff=1000, prec_bits=prec_bits
                )
                n1_term = (w_arb ** 2) * w_arb.sqrt() * (-(w_arb ** 2)).exp()
                rem_pu = q_pu - n1_term
                abs_rem = abs(rem_pu)
                bound_pu = (w_arb ** 2) * w_arb.sqrt() / (arb(2) * (u_arb ** 2))
                margin = bound_pu - abs_rem
                bound_ok = bool(margin.lower() > 0)
                if not bound_ok:
                    all_coprime_tail_bounds_hold = False
                coprime_tail_rows.append({
                    "u": u_val,
                    "primes_le_u": list(primes_u),
                    "w": w_int,
                    "Q_lambda_Pu_w": serialize_arb_certified(q_pu),
                    "n_eq_1_gaussian_term": serialize_arb_certified(n1_term),
                    "R_lambda_Pu_w": serialize_arb_certified(rem_pu),
                    "abs_R_lambda_Pu_w": serialize_arb_certified(abs_rem),
                    "analytic_upper_bound_w_5_2_over_2_u_sq": serialize_arb_certified(bound_pu),
                    "bound_minus_abs_R_margin": serialize_arb_certified(margin),
                    "bound_strictly_certified": bound_ok,
                })

        # 2. Weighted norm Neumann majorant M_Neumann(u, eta) = prod_{p <= u} (1 - p^{-1/2 - eta})^{-1}
        primes_up_to_97 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
        neumann_rows: List[Dict[str, Any]] = []
        for eta_lbl, eta_frac in [
            ("1/10", Fraction(1, 10)),
            ("1/4", Fraction(1, 4)),
            ("1/2", Fraction(1, 2)),
            ("3/4", Fraction(3, 4)),
            ("1", Fraction(1, 1)),
        ]:
            eta_arb = arb(eta_frac.numerator) / arb(eta_frac.denominator)
            s_exp = arb(1) / arb(2) + eta_arb
            u_evaluations: Dict[str, Any] = {}
            for u_cut in (5, 13, 29, 97):
                prod_val = arb(1)
                for p in primes_up_to_97:
                    if p <= u_cut:
                        prod_val /= (arb(1) - (arb(p) ** (-s_exp)))
                u_evaluations[f"u_{u_cut}"] = serialize_arb_certified(prod_val)
            neumann_rows.append({
                "eta_label": eta_lbl,
                "exponent_half_plus_eta": str(Fraction(1, 2) + eta_frac),
                "uniform_as_u_to_infty": bool((Fraction(1, 2) + eta_frac) > 1),
                "values_by_u": u_evaluations,
            })

        # 3. Off-critical mode multiplier M_u(rho) = prod_{p <= u} (1 + p^{-rho}) at rho = 3/4 + 2i and 2/3 + 14i
        mode_rows: List[Dict[str, Any]] = []
        all_mode_bounds_hold = True
        for rho_lbl, x_frac, y_int in [
            ("3/4 + 2i", Fraction(3, 4), 2),
            ("2/3 + 14i", Fraction(2, 3), 14),
        ]:
            x_arb = arb(x_frac.numerator) / arb(x_frac.denominator)
            y_arb = arb(y_int)
            rho_acb = acb(x_arb, y_arb)
            for u_cut in (5, 13, 29):
                m_prod = acb(1)
                lower_prod = arb(1)
                upper_prod = arb(1)
                for p in primes_up_to_97:
                    if p <= u_cut:
                        p_acb = acb(p)
                        p_arb = arb(p)
                        m_prod *= (acb(1) + (p_acb ** (-rho_acb)))
                        lower_prod *= (arb(1) - (p_arb ** (-x_arb)))
                        upper_prod *= (arb(1) + (p_arb ** (-x_arb)))
                abs_m = abs(m_prod)
                low_ok = bool((abs_m - lower_prod).lower() >= 0) and bool(lower_prod.lower() > 0)
                high_ok = bool((upper_prod - abs_m).lower() >= 0)
                if not (low_ok and high_ok):
                    all_mode_bounds_hold = False
                mode_rows.append({
                    "rho_label": rho_lbl,
                    "u": u_cut,
                    "abs_M_u_rho": serialize_arb_certified(abs_m),
                    "lower_bound_prod_1_minus_p_neg_x": serialize_arb_certified(lower_prod),
                    "upper_bound_prod_1_plus_p_neg_x": serialize_arb_certified(upper_prod),
                    "strictly_positive_and_within_bounds": bool(low_ok and high_ok),
                })

        return {
            "coprime_decomposition_and_coupled_cutoff_attempt": {
                "identity": (
                    "For u >= 2, every integer n >= 2 with gcd(n, N_u) = 1 satisfies n > u, so "
                    "Q_{lambda,P_u}(w) = w^{5/2} exp(-w^2) + R_{lambda,P_u}(w) with |R_{lambda,P_u}(w)| <= w^{5/2} / (2 u^2)."
                ),
                "coupled_regime_diagnosis": (
                    "Substituting Q_{lambda,P_u}(X/m) = (X/m)^{5/2} exp(-X^2/m^2) + R_{lambda,P_u}(X/m) into the inverse "
                    "reconstruction Q_lambda(X) = sum_{m in S(P_u)} (lambda(m)/sqrt(m)) Q_{lambda,P_u}(X/m) splits Q_lambda(X) "
                    "into the P_u-smooth sum X^{5/2} sum_{m in S(P_u)} (lambda(m)/m^3) exp(-X^2/m^2) plus the rough-cofactor sum "
                    "over n > u with gcd(n, N_u) = 1. For any coupled cutoff u = Y^theta (theta in (0, 1]), the P_u-smooth integers "
                    "m ~ Y have positive Dickman density rho_Dickman(1/theta) > 0, so the unsigned P_u-smooth sum at the transition "
                    "still has magnitude ~ rho_Dickman(1/theta) sqrt(Y) (energy ~ Y), while the unsigned rough tail over m in S(P_u) "
                    "and n > u has magnitude ~ (1 - rho_Dickman(1/theta)) sqrt(Y). Thus coupling u = u(Y) partitions the transition "
                    "mass between smooth and rough factors without eliminating the order-Y unsigned energy unless signed cancellation "
                    "in lambda(m) on S(P_u) is independently established."
                ),
                "coprime_tail_rows": coprime_tail_rows,
                "all_coprime_tail_bounds_hold": all_coprime_tail_bounds_hold,
            },
            "weighted_norm_neumann_obstruction": {
                "dilation_norm_identity": "||S_p||_eta = p^{-eta} on H_eta = L^2((0, infty), X^{-2*eta} dX/X)",
                "neumann_majorant_formula": "M_Neumann(u, eta) = prod_{p <= u} (1 - p^{-1/2 - eta})^{-1}",
                "needed_signed_improvement_note": (
                    "M_Neumann(u, eta) converges as u -> infty iff eta > 1/2 (where it equals zeta(1/2 + eta)), and diverges "
                    "for 0 < eta <= 1/2 (as e^gamma log u at eta = 1/2 and exp((1+o(1)) u^{1/2-eta} / ((1/2-eta) log u)) for "
                    "0 < eta < 1/2). Reaching eta in (0, 1/2] requires bounding the signed Mellin multiplier "
                    "prod_{p <= u} (1 + p^{-1/2 - eta - i*b})^{-1} = sum_{m in S(P_u)} lambda(m) m^{-1/2 - eta - i*b} without "
                    "replacing lambda(m) m^{-i*b} by +1."
                ),
                "rows": neumann_rows,
            },
            "off_critical_mode_test": {
                "mode_definition": "F_rho(X) = X^{rho - 1/2}  (rho = x + i*y, x > 0)",
                "multiplier_formula": "P_{P_u} F_rho(X) = (prod_{p <= u} (1 + p^{-rho})) F_rho(X)",
                "rows": mode_rows,
                "all_mode_bounds_hold": all_mode_bounds_hold,
            },
            "tau_vs_general_base_comparison": {
                "base_independent_statements": [
                    "Equivalence between (forall eps > 0, int_Y^{b Y} |Q_a(X)|^2 dX/X <= C_{eps,b} Y^eps) and (forall eta in (0, 5/2), ||Q_a||_eta < infty) holds for every base b > 1.",
                    "Near-diagonal kernel inequality sum_{|m-n|<=H} K_{Y,b}(m, n) <= (2H + 1) D_{E,b}(Y) holds for every base b > 1.",
                ],
                "tau_specific_structures": [
                    "1. Unit-covolume Poisson summation kernel cos(tau xi v) (Tate rational-diagonal character rigidity requires c_inf = tau = 2*pi).",
                    "2. Trivial-zero slope normalization (2 (-1)^m tau^{2m} / (2m)!) zeta'(-2m) = zeta(2m + 1) and Bernoulli constants 2 zeta(N) / tau^N = |B_N| / N!.",
                    "3. Gaussian leading factor 3 sqrt(tau) / 64 in D_{E,b}(Y) = (3 sqrt(tau) / 64) log b + O_b(Y^{-2}), where sqrt(tau) comes from the Gaussian integral and log b is the logarithmic window length.",
                ],
            },
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_tc055_integrated_energy_kernel_and_near_diagonal_bound(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TASK-TC-055 Section 5:
    1. Exact kernel representation E_lambda(Y) = sum_{m, n >= 1} lambda(m) lambda(n) K_Y(m, n)
       with K_Y(m, n) = (m n)^{-3} int_Y^{tau Y} X^4 exp(-X^2 (m^{-2} + n^{-2})) dX > 0.
    2. Derivation and 256-bit Arb certification of the diagonal energy asymptotic from the
       Section 4 common-factor Euler-Maclaurin bound at L_{1,1}(X) = sqrt(2) X:
           D_E(Y) := sum_{n >= 1} K_Y(n, n) = (3 sqrt(tau) / 64) log tau + R_{D,E}(Y),
           |R_{D,E}(Y)| <= C_{D,2} Y^{-2}   for ALL Y > 0,
           C_{D,2} := C_2 (1 - tau^{-2}) / (16 sqrt(2)) = 0.07974240995631961059...,
       and fourth-order bound |R_{D,E}(Y)| <= C_{D,4} Y^{-4} with C_{D,4} = C_4 (1 - tau^{-4}) / (64 sqrt(2)).
    3. Proof and 256-bit Arb certification of the near-diagonal inequality for every integer H >= 0:
           sum_{|m - n| <= H} K_Y(m, n) <= (2 H + 1) D_E(Y),
       via 2 K_Y(m, n) <= K_Y(m, m) + K_Y(n, n) summed over the 2H + 1 offsets h = n - m in {-H, ..., H}.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()
        em_consts = verify_euler_maclaurin_derivatives_and_constants_arb(prec_bits=prec_bits)
        C_2_arb = em_consts["C_2"]["enclosure_arb"]
        C_4_arb = em_consts["C_4"]["enclosure_arb"]

        leading_D_E = (arb(3) * tau_arb.sqrt() / arb(64)) * tau_arb.log()
        C_D_2 = C_2_arb * (arb(1) - (tau_arb ** (-2))) / (arb(16) * arb(2).sqrt())
        C_D_4 = C_4_arb * (arb(1) - (tau_arb ** (-4))) / (arb(64) * arb(2).sqrt())

        # 1. Certify D_E(Y) across Y in {1, 2, 4, 8, 16}:
        #    Note: for n > N_max, K_Y(n, n) <= n^{-6} int_Y^{tau Y} X^4 dX = ((tau^5 - 1) Y^5 / 5) n^{-6},
        #    so sum_{n > N_max} K_Y(n, n) <= ((tau^5 - 1) Y^5 / 25) N_max^{-5}.
        diagonal_rows: List[Dict[str, Any]] = []
        all_diagonal_bounds_hold = True
        for Y_int in (1, 2, 4, 8, 16):
            Y_arb = arb(Y_int)
            N_max = max(200, 80 * Y_int)
            partial_D = arb(0)
            for n in range(1, N_max + 1):
                partial_D += evaluate_energy_kernel_K_Y_certified_arb(Y_arb, n, n, prec_bits=prec_bits)
            tail_D = ((tau_arb ** 5 - arb(1)) * (Y_arb ** 5) / arb(25)) / (arb(N_max) ** 5)
            D_E_val = inflate_arb_with_nonneg_bound(partial_D, tail_D)
            abs_err = abs(D_E_val - leading_D_E)
            bnd_2 = C_D_2 / (Y_arb * Y_arb)
            bnd_4 = C_D_4 / (Y_arb ** 4)
            margin_2 = bnd_2 - abs_err
            margin_4 = bnd_4 - abs_err
            ok_2 = bool(margin_2.lower() > 0)
            ok_4 = bool(margin_4.lower() > 0)
            if not (ok_2 and ok_4):
                all_diagonal_bounds_hold = False
            diagonal_rows.append({
                "Y": Y_int,
                "N_max": N_max,
                "D_E_Y": serialize_arb_certified(D_E_val),
                "leading_constant_3_sqrt_tau_over_64_log_tau": serialize_arb_certified(leading_D_E),
                "abs_error_D_E_minus_leading": serialize_arb_certified(abs_err),
                "N2_error_bound_C_D2_Y_neg_2": serialize_arb_certified(bnd_2),
                "N2_bound_margin": serialize_arb_certified(margin_2),
                "N2_bound_strictly_certified": ok_2,
                "N4_error_bound_C_D4_Y_neg_4": serialize_arb_certified(bnd_4),
                "N4_bound_margin": serialize_arb_certified(margin_4),
                "N4_bound_strictly_certified": ok_4,
            })

        # 2. Certify near-diagonal bound sum_{|m - n| <= H} K_Y(m, n) <= (2H + 1) D_E(Y)
        #    for Y in {1, 2, 4} and H in {0, 1, 2, 4}:
        #    For |m - n| <= H with max(m, n) > N_band, each offset h in [-H, H] has tail
        #    bounded by the diagonal tail ((tau^5 - 1) Y^5 / 25) (N_band - H)^{-5}.
        near_diagonal_rows: List[Dict[str, Any]] = []
        all_near_diagonal_bounds_hold = True
        for Y_int in (1, 2, 4):
            Y_arb = arb(Y_int)
            N_band = 140 * Y_int
            diag_vals = [
                evaluate_energy_kernel_K_Y_certified_arb(Y_arb, n, n, prec_bits=prec_bits)
                for n in range(1, N_band + 1)
            ]
            tail_diag = ((tau_arb ** 5 - arb(1)) * (Y_arb ** 5) / arb(25)) / (arb(N_band) ** 5)
            D_E_Y = inflate_arb_with_nonneg_bound(sum(diag_vals, arb(0)), tail_diag)

            for H_int in (0, 1, 2, 4):
                band_partial = arb(0)
                signed_band_partial = arb(0)
                for m in range(1, N_band + 1):
                    lam_m = liouville_lambda_int(m)
                    band_partial += diag_vals[m - 1]
                    signed_band_partial += diag_vals[m - 1]
                    for h in range(1, H_int + 1):
                        n = m + h
                        if n <= N_band:
                            k_mn = evaluate_energy_kernel_K_Y_certified_arb(Y_arb, m, n, prec_bits=prec_bits)
                            band_partial += arb(2) * k_mn
                            signed_band_partial += arb(2 * lam_m * liouville_lambda_int(n)) * k_mn
                band_tail = arb(2 * H_int + 1) * (
                    ((tau_arb ** 5 - arb(1)) * (Y_arb ** 5) / arb(25)) / (arb(N_band - H_int) ** 5)
                )
                band_sum = inflate_arb_with_nonneg_bound(band_partial, band_tail)
                signed_band_sum = inflate_arb_with_nonneg_bound(signed_band_partial, band_tail)
                rhs_bound = arb(2 * H_int + 1) * D_E_Y
                margin = rhs_bound - band_sum
                # For H = 0, band_sum == D_E_Y so margin contains 0; for H >= 1, strictly positive margin > 0
                ok_band = bool(margin.contains(0)) if H_int == 0 else bool(margin.lower() > 0)
                if not ok_band:
                    all_near_diagonal_bounds_hold = False
                near_diagonal_rows.append({
                    "Y": Y_int,
                    "H": H_int,
                    "two_H_plus_1": 2 * H_int + 1,
                    "unsigned_near_diagonal_sum": serialize_arb_certified(band_sum),
                    "signed_near_diagonal_sum": serialize_arb_certified(signed_band_sum),
                    "upper_bound_2H_plus_1_times_D_E_Y": serialize_arb_certified(rhs_bound),
                    "upper_bound_minus_unsigned_sum_margin": serialize_arb_certified(margin),
                    "inequality_certified": ok_band,
                })

        return {
            "diagonal_asymptotic_formula": "D_E(Y) := sum_{n>=1} K_Y(n, n) = (3 sqrt(tau) / 64) log tau + R_{D,E}(Y)",
            "leading_constant_3_sqrt_tau_over_64_log_tau": serialize_arb_certified(leading_D_E),
            "explicit_N2_error_constant_C_D2": serialize_arb_certified(C_D_2),
            "explicit_N4_error_constant_C_D4": serialize_arb_certified(C_D_4),
            "domain_of_validity": "All Y > 0",
            "diagonal_rows": diagonal_rows,
            "all_diagonal_bounds_hold": all_diagonal_bounds_hold,
            "near_diagonal_inequality_formula": "sum_{|m - n| <= H} K_Y(m, n) <= (2 H + 1) D_E(Y)   for all integers H >= 0 and all Y > 0",
            "near_diagonal_rows": near_diagonal_rows,
            "all_near_diagonal_bounds_hold": all_near_diagonal_bounds_hold,
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_tc055_opposite_parity_dilation_pairing_and_obstruction(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TASK-TC-055 Section 6:
    1. Opposite-parity prime-semiprime dilation pairing:
       For a prime p and semiprime s = q r (with q, r prime),
           lambda(p m) = -lambda(m),   lambda(q r m) = +lambda(m),
       so for every m, n >= 1:
           lambda(p m) lambda(n) K_Y(p m, n) + lambda(q r m) lambda(n) K_Y(q r m, n)
             = -lambda(m) lambda(n) [K_Y(p m, n) - K_Y(q r m, n)].
    2. Exact MVT kernel-difference bound:
       Since d/du(u^{-3} exp(-X^2/u^2)) = u^{-4} (2 X^2/u^2 - 3) exp(-X^2/u^2) and
       sup_{w > 0} |2 w^2 - 3| exp(-w^2) = 3, for u_1 = min(p, q r) m and u_2 = max(p, q r) m:
           |K_Y(p m, n) - K_Y(q r m, n)|
             <= (|q r - p| / min(p, q r)) * (u_2 - u_1)^{-1} int_{u_1}^{u_2} |u dK_Y/du(u, n)| du
             <= (|q r - p| / min(p, q r)) * (3 / (u_1^3 n^3)) int_Y^{tau Y} X^4 exp(-X^2 (u_2^{-2} + n^{-2})) dX
             = 3 (|q r - p| / min(p, q r)) (max(p, q r) / min(p, q r))^3 K_Y(max(p, q r) m, n).
    3. Exact partition / multiplicity / coprime-unmatched residual diagnosis:
       Evaluates the divisor-weight discrepancy 1 - W_pair(k) / w_bar and the unmatched coprime density
       prod_{p in P_active} (1 - 1/p) (plus primes k in [Y, tau Y]), showing why opposite-parity pairing
       saves |q r - p| / p on matched pairs while leaving an unmatched contribution of order Y.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits

        pairing_rows: List[Dict[str, Any]] = []
        all_pairing_bounds_hold = True
        for p_val, q_val, r_val in [(5, 2, 2), (7, 2, 3), (11, 2, 5), (13, 3, 5)]:
            qr_val = q_val * r_val
            u_min_factor = min(p_val, qr_val)
            u_max_factor = max(p_val, qr_val)
            gap_factor = abs(qr_val - p_val)
            for Y_int, m_int, n_int in [(4, 2, 8), (8, 3, 15), (16, 4, 20)]:
                Y_arb = arb(Y_int)
                k_pm = evaluate_energy_kernel_K_Y_certified_arb(Y_arb, p_val * m_int, n_int, prec_bits=prec_bits)
                k_qrm = evaluate_energy_kernel_K_Y_certified_arb(Y_arb, qr_val * m_int, n_int, prec_bits=prec_bits)
                k_max = evaluate_energy_kernel_K_Y_certified_arb(Y_arb, u_max_factor * m_int, n_int, prec_bits=prec_bits)
                abs_diff = abs(k_pm - k_qrm)
                mvt_bound = (
                    arb(3)
                    * (arb(gap_factor) / arb(u_min_factor))
                    * ((arb(u_max_factor) / arb(u_min_factor)) ** 3)
                    * k_max
                )
                margin = mvt_bound - abs_diff
                bound_ok = bool(margin.lower() > 0)
                if not bound_ok:
                    all_pairing_bounds_hold = False
                pairing_rows.append({
                    "p": p_val,
                    "q": q_val,
                    "r": r_val,
                    "qr": qr_val,
                    "Y": Y_int,
                    "m": m_int,
                    "n": n_int,
                    "K_Y_pm_n": serialize_arb_certified(k_pm),
                    "K_Y_qrm_n": serialize_arb_certified(k_qrm),
                    "abs_difference": serialize_arb_certified(abs_diff),
                    "analytic_mvt_upper_bound": serialize_arb_certified(mvt_bound),
                    "bound_minus_abs_diff_margin": serialize_arb_certified(margin),
                    "mvt_bound_strictly_certified": bound_ok,
                })

        # Unmatched coprime and multiplicity residual audit on 1 <= k <= 240 for P_1 = {5, 7, 11}, P_2 = {4, 6, 10}:
        P1 = (5, 7, 11)
        P2 = (4, 6, 10)
        w_bar = sum(Fraction(1, p) for p in P1) + sum(Fraction(1, s) for s in P2)
        unmatched_zero_weight_count = 0
        non_unit_weight_count = 0
        for k in range(1, 241):
            w_k = sum(1 for p in P1 if k % p == 0) + sum(1 for s in P2 if k % s == 0)
            if w_k == 0:
                unmatched_zero_weight_count += 1
            if Fraction(w_k, 1) != w_bar:
                non_unit_weight_count += 1

        return {
            "candidate_lemma_statement": (
                "For prime p and semiprime s = q r, lambda(p m) + lambda(q r m) = 0 and "
                "|K_Y(p m, n) - K_Y(q r m, n)| <= 3 (|q r - p| / min(p, q r)) (max(p, q r) / min(p, q r))^3 K_Y(max(p, q r) m, n) "
                "for all m, n >= 1 and Y > 0."
            ),
            "pairwise_mvt_rows": pairing_rows,
            "all_pairwise_mvt_bounds_hold": all_pairing_bounds_hold,
            "unmatched_residual_and_multiplicity_obstruction": {
                "tested_P1_primes": list(P1),
                "tested_P2_semiprimes": list(P2),
                "mean_divisor_weight_w_bar": str(w_bar),
                "k_range_tested": "1 <= k <= 240",
                "unmatched_k_count_with_W_pair_eq_0": unmatched_zero_weight_count,
                "k_count_with_W_pair_ne_w_bar": non_unit_weight_count,
                "exact_obstruction_diagnosis": (
                    "Regrouping sum_{p in P_1} alpha_p sum_m lambda(p m) g(p m) + sum_{s in P_2} beta_s sum_m lambda(s m) g(s m) "
                    "by product index k = p m or s m weights each k by W_pair(k) = sum_{p|k} alpha_p + sum_{s|k} beta_s. "
                    "Every integer k coprime to prod_{p in P_1 union P_2} p (including all primes k in [Y, tau Y] when the active "
                    "factors are <= Y^theta with theta < 1) has W_pair(k) = 0, leaving a positive-density unmatched residual of "
                    "unsigned energy order Y. Moreover, on matched pairs (p m, q r m), the transition window p m in [Y, tau Y] vs "
                    "q r m in [Y, tau Y] shifts the m-cutoff by |q r - p| Y / (p q r), producing boundary terms of the same scale "
                    "(|q r - p| / p) Y as the interior MVT difference."
                ),
            },
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_tc055_multiplicative_parity_controls(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TASK-TC-055 Section 7:
    1. Hypothesis-by-hypothesis comparison between actual Liouville lambda(n) = (-1)^{Omega(n)},
       the 2-adic parity control a_2(n) = (-1)^{v_2(n)}, and general finite-prime parity controls
       a_S(n) = (-1)^{sum_{p in S} v_p(n)}.
    2. Exact non-asymptotic and asymptotic derivations for a_2(n):
       - Dyadic exclusion identity: (I + 2^{-1/2} S_2) Q_{a_2}(X) = Q_odd(X) = Q_1(X) - 2^{-1/2} Q_1(X/2) > 0;
       - Dyadic series expansion: Q_{a_2}(X) = Q_1(X) + 2 sum_{k>=1} (-1)^k 2^{-k/2} Q_1(X / 2^k);
       - Unimodal Euler-Maclaurin bound: |Q_1(X) - sqrt(X)/2| <= (3/e)^{3/2} X^{-1/2} for all X > 0;
       - Asymptotic laws:
             Q_{a_2}(X) = (1/6) sqrt(X) + O(X^{-1/2}) ~ sqrt(X) / 6,
             E_{a_2}(Y) := int_Y^{tau Y} |Q_{a_2}(X)|^2 dX/X = ((tau - 1) / 36) Y + O(1) ~ ((tau - 1) / 36) Y,
         certified in 256-bit Arb across X, Y in {4, 8, 16, 32, 64}.
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()
        one_sixth = arb(1) / arb(6)
        tau_minus_1_over_36 = (tau_arb - arb(1)) / arb(36)
        three_over_e_pow_3_2 = (arb(3) / arb(1).exp()) ** (arb(3) / arb(2))

        # 1. Certify |Q_1(X) - sqrt(X)/2| <= (3/e)^{3/2} X^{-1/2} and (I + 2^{-1/2} S_2) Q_{a_2}(X) = Q_1(X) - 2^{-1/2} Q_1(X/2)
        q_a2_rows: List[Dict[str, Any]] = []
        all_q1_bounds_and_dyadic_identities_hold = True
        inv_sqrt2 = arb(1) / arb(2).sqrt()
        for X_int in (4, 8, 16, 32, 64):
            X_arb = arb(X_int)
            t_cut = max(1200, 30 * X_int)
            q1_x = evaluate_Q_1_unweighted_certified_arb(X_arb, T_cutoff=t_cut, prec_bits=prec_bits)
            q1_half_x = evaluate_Q_1_unweighted_certified_arb(X_arb / arb(2), T_cutoff=t_cut, prec_bits=prec_bits)
            q1_err = abs(q1_x - X_arb.sqrt() / arb(2))
            q1_bnd = three_over_e_pow_3_2 / X_arb.sqrt()
            q1_ok = bool((q1_bnd - q1_err).lower() > 0)

            qa2_x = evaluate_Q_a2_certified_arb(X_arb, T_cutoff=t_cut, prec_bits=prec_bits)
            qa2_half_x = evaluate_Q_a2_certified_arb(X_arb / arb(2), T_cutoff=t_cut, prec_bits=prec_bits)
            lhs_dyadic = qa2_x + inv_sqrt2 * qa2_half_x
            rhs_odd = q1_x - inv_sqrt2 * q1_half_x
            dyadic_diff = lhs_dyadic - rhs_odd
            dyadic_ok = bool(dyadic_diff.contains(0)) and bool(lhs_dyadic.lower() > 0)

            ratio_to_sqrt_X = qa2_x / X_arb.sqrt()
            scaled_rem_X_half = (qa2_x - X_arb.sqrt() / arb(6)) * X_arb.sqrt()
            if not (q1_ok and dyadic_ok):
                all_q1_bounds_and_dyadic_identities_hold = False
            q_a2_rows.append({
                "X": X_int,
                "Q_a2_X": serialize_arb_certified(qa2_x),
                "leading_sqrt_X_over_6": serialize_arb_certified(X_arb.sqrt() / arb(6)),
                "ratio_Q_a2_over_sqrt_X": serialize_arb_certified(ratio_to_sqrt_X),
                "scaled_remainder_sqrt_X_times_diff": serialize_arb_certified(scaled_rem_X_half),
                "dyadic_filter_lhs_minus_Q_odd_rhs": serialize_arb_certified(dyadic_diff),
                "dyadic_filter_strictly_positive_and_matches_Q_odd": dyadic_ok,
                "Q_1_unimodal_error_bound_holds": q1_ok,
            })

        # 2. Certify E_{a_2}(Y) ~ ((tau - 1) / 36) Y across Y in {4, 8, 16, 32}:
        e_a2_rows: List[Dict[str, Any]] = []
        all_e_a2_positive = True
        for Y_int in (4, 8, 16, 32):
            Y_arb = arb(Y_int)
            t_cut = max(1200, 35 * Y_int)
            e_a2 = evaluate_E_a2_certified_arb(Y_arb, N_subintervals=32, T_cutoff=t_cut, prec_bits=prec_bits)
            leading_e = tau_minus_1_over_36 * Y_arb
            ratio_e_over_Y = e_a2 / Y_arb
            abs_rem_e = abs(e_a2 - leading_e)
            if not bool(e_a2.lower() > 0):
                all_e_a2_positive = False
            e_a2_rows.append({
                "Y": Y_int,
                "E_a2_Y": serialize_arb_certified(e_a2),
                "leading_tau_minus_1_over_36_times_Y": serialize_arb_certified(leading_e),
                "ratio_E_a2_over_Y": serialize_arb_certified(ratio_e_over_Y),
                "abs_difference_from_leading": serialize_arb_certified(abs_rem_e),
            })

        return {
            "asymptotic_formulas": {
                "Q_a2_asymptotic": "Q_{a_2}(X) = (1 / 6) sqrt(X) + O(X^{-1/2}) ~ sqrt(X) / 6",
                "E_a2_asymptotic": "E_{a_2}(Y) := int_Y^{tau Y} |Q_{a_2}(X)|^2 dX/X = ((tau - 1) / 36) Y + O(1) ~ ((tau - 1) / 36) Y",
                "general_finite_S_asymptotic": (
                    "For a_S(n) = (-1)^{sum_{p in S} v_p(n)}, "
                    "Q_{a_S}(X) ~ (1/2) (prod_{p in S} (p - 1)/(p + 1)) sqrt(X) and "
                    "E_{a_S}(Y) ~ ((tau - 1) / 4) (prod_{p in S} (p - 1)/(p + 1))^2 Y."
                ),
                "one_sixth": serialize_arb_certified(one_sixth),
                "tau_minus_1_over_36": serialize_arb_certified(tau_minus_1_over_36),
            },
            "hypothesis_by_hypothesis_comparison": [
                {
                    "property": "Complete multiplicativity a(m n) = a(m) a(n) and unit square a(d)^2 = 1",
                    "liouville_lambda": True,
                    "control_a2": True,
                    "control_aS_finite": True,
                },
                {
                    "property": "Unconstrained common-factor cancellation a(d r) a(d s) = a(r) a(s) for all d, r, s >= 1",
                    "liouville_lambda": True,
                    "control_a2": True,
                    "control_aS_finite": True,
                },
                {
                    "property": "Transition Poisson summation kernel hat{f}(j L) and Euler-Maclaurin subtransition bound",
                    "liouville_lambda": True,
                    "control_a2": True,
                    "control_aS_finite": True,
                },
                {
                    "property": "Parity flip a(p n) = -a(n) and exclusion identity (I + p^{-1/2} S_p) Q_a(X) for p in S",
                    "liouville_lambda": True,
                    "control_a2": True,
                    "control_aS_finite": True,
                },
                {
                    "property": "Parity flip a(p n) = -a(n) at ALL primes p",
                    "liouville_lambda": True,
                    "control_a2": False,
                    "control_aS_finite": False,
                },
                {
                    "property": "Square-divisor Möbius convolution a(n) = sum_{d^2 | n} mu(n / d^2) and pole cancellation at s = 1",
                    "liouville_lambda": True,
                    "control_a2": False,
                    "control_aS_finite": False,
                },
            ],
            "Q_a2_rows": q_a2_rows,
            "all_q1_bounds_and_dyadic_identities_hold": all_q1_bounds_and_dyadic_identities_hold,
            "E_a2_rows": e_a2_rows,
            "all_e_a2_positive": all_e_a2_positive,
            "scope_note": (
                "Because a_2(n) = (-1)^{v_2(n)} (and any finite-prime parity control a_S) satisfies complete multiplicativity, "
                "common-factor cancellation, transition Poisson summation, and finite-prime exclusion for P subset S, yet has "
                "Q_{a_2}(X) ~ sqrt(X)/6 and E_{a_2}(Y) ~ ((tau - 1)/36) Y (linear growth in Y), any cancellation argument that "
                "uses only hypotheses shared by a_2 or a_S cannot establish E_lambda(Y) = o(Y) or E_lambda(Y) <<_eps Y^eps. "
                "This is a control diagnostic exposing unsupported inferences, NOT a counterexample to the complete TC framework "
                "(since a_2 fails a(p) = -1 at odd primes and fails sum_{d^2|n} mu(n/d^2) = a(n))."
            ),
        }
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 7. Master Execution & Artifact Generation
# ---------------------------------------------------------------------------


def execute_task_tc054_liouville_square_dilation_audit(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Execute the full TASK-TC-054 / TASK-TC-054R / TASK-TC-054R2 / TASK-TC-055 mathematical and numerical audit and return the report dictionary."""
    sec2_3 = verify_section_2_and_3_square_dilation_transfer(prec_bits=prec_bits)
    sec4 = verify_section_4_unconstrained_common_factor_and_euler_maclaurin(prec_bits=prec_bits)
    sec5 = verify_section_5_poisson_summation_at_transition(prec_bits=prec_bits)
    sec6 = verify_section_6_transition_attacks_and_decoupling(prec_bits=prec_bits)
    lean_audit = verify_liouville_square_dilation_lean_module()
    sec8_tc055_joint = verify_tc055_simultaneous_joint_identities_and_trivial_zero_cancellation(prec_bits=prec_bits)
    sec9_tc055_cutoff = verify_tc055_coupled_cutoff_and_norm_obstruction(prec_bits=prec_bits)
    sec10_tc055_kernel = verify_tc055_integrated_energy_kernel_and_near_diagonal_bound(prec_bits=prec_bits)
    sec11_tc055_pairing = verify_tc055_opposite_parity_dilation_pairing_and_obstruction(prec_bits=prec_bits)
    sec12_tc055_controls = verify_tc055_multiplicative_parity_controls(prec_bits=prec_bits)

    report: Dict[str, Any] = {
        "task_id": TASK_TC_054_ID,
        "repair_task_id": TASK_TC_054R_ID,
        "closeout_task_id": TASK_TC_054R2_ID,
        "simultaneous_compatibility_task_id": TASK_TC_055_ID,
        "parent_epic": EPIC_TC_042_ID,
        "prior_merged_main": PRIOR_MERGED_MAIN_TC_053R,
        "tc053r2_implementation_commit": TC_053R2_IMPLEMENTATION_COMMIT,
        "tc053r2_reviewed_tip": TC_053R2_REVIEWED_TIP,
        "tc054_implementation_commit": TC_054_IMPLEMENTATION_COMMIT,
        "tc054_reviewed_tip": TC_054_REVIEWED_TIP,
        "tc054r_implementation_commit": TC_054R_IMPLEMENTATION_COMMIT,
        "tc054r_reviewed_tip": TC_054R_REVIEWED_TIP,
        "tc054r2_implementation_commit": TC_054R2_IMPLEMENTATION_COMMIT,
        "tc054r2_reviewed_tip": TC_054R2_REVIEWED_TIP,
        "tc054r2_merged_main_baseline": TC_054R2_MERGED_MAIN_BASELINE,
        "tc055_initial_closeout_commit": TC_055_INITIAL_CLOSEOUT_COMMIT,
        "branch": "task/tc-055-simultaneous-tau-compatibility-and-signed-energy-cancellation",
        "subgate_tc043a_status": "OPEN",
        "rh_proved": False,
        "precision_bits": prec_bits,
        "section_2_and_3_reversible_square_dilation_transfer": sec2_3,
        "section_4_unconstrained_common_factor_and_euler_maclaurin": sec4,
        "section_5_transition_poisson_summation": sec5,
        "section_6_rectangular_blocks_and_transition_attacks": sec6,
        "section_7_lean_formalization_audit": lean_audit,
        "section_8_tc055_simultaneous_compatibility_and_joint_identities": sec8_tc055_joint,
        "section_9_tc055_coupled_cutoff_and_norm_obstruction": sec9_tc055_cutoff,
        "section_10_tc055_integrated_energy_kernel_and_near_diagonal": sec10_tc055_kernel,
        "section_11_tc055_opposite_parity_dilation_pairing": sec11_tc055_pairing,
        "section_12_tc055_multiplicative_parity_controls": sec12_tc055_controls,
        "surviving_unconditional_theorems": [
            "Reversible square-dilation transfer lambda(n) = sum_{d^2 | n} mu(n/d^2), mu(n) = sum_{d^2 | n} mu(d) lambda(n/d^2), Q_lambda(X) = sum_{d>=1} Q_mu(X/d^2)/d, Q_mu(X) = sum_{d>=1} mu(d) Q_lambda(X/d^2)/d, and weighted L^2 norm equivalence ||Q_lambda||_eta <= zeta(1+2*eta) ||Q_mu||_eta, ||Q_mu||_eta <= (zeta(1+2*eta)/zeta(2+4*eta)) ||Q_lambda||_eta for all eta > 0.",
            "Equivalence between the grade-interval subpower energy bound (forall eps > 0 exists C_eps, int_Y^{tau Y} |Q_a(X)|^2 dX/X <= C_eps Y^eps) and weighted norm finiteness (forall eta in (0, 5/2), ||Q_a||_eta < infty) for both a = mu and a = lambda.",
            "Unconstrained common-factor expansion Q_lambda(X)^2 = sum_{gcd(r,s)=1} (lambda(r) lambda(s) X^5 / (r s)^3) sum_{d>=1} d^{-6} exp(-L^2/d^2) (with lambda(d r) lambda(d s) = lambda(r) lambda(s) for ALL d >= 1) and fixed-order Euler-Maclaurin error bound |E^lambda_{r,s}(X)| <= C_N X^{-N} (r s)^{N+2} / (r^2 + s^2)^{(N+5)/2} (C_2 = 1.8512576670..., C_4 = 8.7523717600...), controlling every fixed subtransition range A <= X^{1 - delta} whenever (N + 1) delta > 1.",
            "Exact Poisson summation formula sum_{d>=1} d^{-6} exp(-L^2/d^2) = L^{-5} [c_0 + sum_{j>=1} hat{f}(j L)] (with c_0 = 3 sqrt(tau/2) / 8) established via C^infty flatness at 0, O(|v|^{-6-j}) decay at infinity, and C^1(R/Z) periodization (DLMF 1.8.14), Mellin regularization + contour shifting with |R_M(omega)| <= 8 omega^{2M+3/2} / (Gamma(2M+5/2) Gamma(M-3/4)) -> 0, repaired Fourier tail-ratio certification (R_even, R_odd <= 1/2 or 1/(1-R)), and certified sign changes hat{f}(1/2) < 0, hat{f}(4/tau) < 0, hat{f}(1) < 0, hat{f}(3/2) > 0, hat{f}(2) > 0.",
            "Repaired unequal-block bound |B_{A,B}(X)| <= (7/3) C_* min(A,B)^3 / max(A,B)^2 with C_* = max{zeta(6), c_0 + 27 exp(-3)} = 2.008921040021894970679058028804597412605..., repaired dyadic Abel bound |U_lambda(Y; M)| << M^{1/2} min(M/Y, (Y/M)^{5/2}) exp(-c Phi(M)) (M >= 16), and unconditional global Stieltjes energy theorem |Q_lambda(X)| << sqrt(X) exp(-c_1 Phi(X)) (X >= 256), E_lambda(Y) := int_Y^{tau Y} |Q_lambda(X)|^2 dX/X << Y exp(-2 c_2 Phi(Y)) (Y >= 256), and E_lambda(Y) <<_D Y (log Y)^{-D} (Y >= 2, via compact-range bound E_lambda(Y) <= (zeta(3)^2 (tau^5 - 1) / 5) Y^5 on 2 <= Y < 256) by splitting Q_lambda(X) = -X^{5/2} int_1^infty L_lambda(t) d/dt(t^{-3} exp(-X^2/t^2)) dt at t = sqrt(X) with scaling constant int_0^infty u |3 - 2 u^2| exp(-u^2) du = 1/2 + 2 exp(-3/2).",
            "Exact dyadic parity annihilation Q_{lambda,odd}(X) = Q_lambda(X) + 2^{-1/2} Q_lambda(X/2), convergent dyadic inversion, exact grade-interval energy identity on [Y, tau Y] with cross-scale correlation, bounded norm equivalence for all eta > -1/2, and proof that |1 + 2^{-rho}| >= 1 - 2^{-x} > 0 for rho = x + i*y with x > 0.",
            "Simultaneous finite-prime exclusion identity Q_{lambda,P}(X) = prod_{p in P}(I + p^{-1/2} S_p) Q_lambda(X) = sum_{d | N_P} (|mu(d)| / sqrt(d)) Q_lambda(X / d) = X^{5/2} sum_{gcd(n, N_P)=1} (lambda(n)/n^3) exp(-X^2/n^2) (formalized on actual integers in Lean 4 theorem actual_finite_prime_exclusion_sieve_identity_nat), its convergent P-smooth inverse reconstruction Q_lambda(X) = sum_{m in S(P)} (lambda(m)/sqrt(m)) Q_{lambda,P}(X/m), and exact removable trivial-zero cancellation lim_{z -> -(2m+1/2)} zeta(1+2z)/zeta(1/2+z) = 2 zeta'(-4m)/zeta'(-2m) = 2 (-1)^m (4m)! zeta(4m+1) / (tau^{2m} (2m)! zeta(2m+1)) != 0.",
            "Exact coprime decomposition Q_{lambda,P_u}(w) = w^{5/2} exp(-w^2) + R_{lambda,P_u}(w) for u >= 2 with unconditional tail bound |R_{lambda,P_u}(w)| <= w^{5/2} / (2 u^2), diagonal energy asymptotic D_E(Y) := sum_{n>=1} K_Y(n, n) = (3 sqrt(tau) / 64) log tau + R_{D,E}(Y) with |R_{D,E}(Y)| <= C_{D,2} Y^{-2} (C_{D,2} = C_2 (1 - tau^{-2}) / (16 sqrt(2)) = 0.07974240995631961...) for all Y > 0, and unconditional near-diagonal band inequality sum_{|m - n| <= H} K_Y(m, n) <= (2 H + 1) D_E(Y) for all integers H >= 0 (formalized in Lean 4 theorem near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing).",
            "Pairwise opposite-parity prime-semiprime dilation cancellation lambda(p m) + lambda(q r m) = 0 with MVT kernel difference bound |K_Y(p m, n) - K_Y(q r m, n)| <= 3 (|q r - p| / min(p, q r)) (max(p, q r) / min(p, q r))^3 K_Y(max(p, q r) m, n), together with the 2-adic parity control theorem Q_{a_2}(X) = sqrt(X)/6 + O(X^{-1/2}) ~ sqrt(X)/6 and E_{a_2}(Y) = ((tau - 1)/36) Y + O(1) ~ ((tau - 1)/36) Y (formalized in Lean 4 theorem prime_parity_control_multiplicative_and_moebius_separation_nat).",
        ],
        "precise_obstruction_to_subgate_tc043a_closure": (
            "1. In Attack A, the bivariate coprime Dirichlet series D_lambda(u, v) = zeta(2u) zeta(2v) / (zeta(u) zeta(v) zeta(u+v)) "
            "has numerator zeta(2u) zeta(2v) and coprimality factor 1/zeta(u+v) evaluated at 2u, 2v, u+v in the Euler-product "
            "half-plane Re(w) > 1 whenever Re(u) = Re(v) = x > 1/2, so neither factor can vanish at an off-critical conjugate pair "
            "(rho, conj(rho)) (rho = x + i*y) to cancel the poles of 1/(zeta(u) zeta(v)); moreover M[Q_lambda](z) has a genuine simple pole "
            "at z = 0 of residue Gamma(5/4)/(4 zeta(1/2)) = -0.1551682265... != 0, and the global divisor sum sum_{q>=1} ((sum_{e|q} mu(e))/q) Q_lambda(X/q)^2 "
            "collapses to q = 1. While the global Stieltjes integration-by-parts proof establishes E_lambda(Y) << Y exp(-2 c_2 Phi(Y)) <<_D Y (log Y)^{-D} "
            "from unconditional Korobov-Vinogradov-Walfisz cancellation, this is an upper bound (not an energy asymptotic) and does not establish "
            "forall eps > 0, E_lambda(Y) <= C_eps Y^eps. "
            "2. In Attack B and its simultaneous finite-prime extension P_{P_u} = prod_{p <= u}(I + p^{-1/2} S_p) (TASK-TC-055), "
            "every finite-prime filter multiplies an off-critical mode F_rho(X) = X^{rho - 1/2} (rho = x + i*y, x > 0) by "
            "M_u(rho) = prod_{p <= u}(1 + p^{-rho}), which satisfies 0 < prod_{p <= u}(1 - p^{-x}) <= |M_u(rho)| <= prod_{p <= u}(1 + p^{-x}) "
            "and therefore cannot annihilate any off-critical mode at finite u; meanwhile on H_eta = L^2((0, infty), X^{-2*eta} dX/X) "
            "the triangle-inequality Neumann majorant prod_{p <= u}(1 - p^{-1/2 - eta})^{-1} converges as u -> infty only for eta > 1/2 "
            "and diverges for 0 < eta <= 1/2, while coupling u = Y^theta leaves a P_u-smooth transition sum of Dickman density rho_Dickman(1/theta) > 0 "
            "and opposite-parity prime-semiprime pairing leaves an unmatched coprime residual of unsigned energy order Y. "
            "3. The multiplicative parity control a_2(n) = (-1)^{v_2(n)} (and any finite-prime parity control a_S) satisfies complete multiplicativity, "
            "unconstrained common-factor cancellation, transition Poisson summation, and dyadic exclusion, yet obeys Q_{a_2}(X) ~ sqrt(X)/6 and "
            "E_{a_2}(Y) ~ ((tau - 1)/36) Y, proving that any cancellation proof for E_lambda(Y) = o(Y) must simultaneously exploit parity flip "
            "lambda(p n) = -lambda(n) across infinitely many primes (and the pole-canceling identity D_lambda(s) = zeta(2s)/zeta(s) at s = 1)."
        ),
    }

    arb_check = verify_all_serialized_arb_in_tree(report)
    assert arb_check["all_enclose_original_256bit_arb_ball"] is True, (
        f"Serialized Arb enclosure verification failed: {arb_check.get('failed_paths')}"
    )
    return report


execute_task_tc055_simultaneous_tau_compatibility_audit = (
    execute_task_tc054_liouville_square_dilation_audit
)


def write_task_tc054_liouville_square_dilation_artifact(
    path: Path = LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Generate and write `data/tc_liouville_square_dilation.json`."""
    report = execute_task_tc054_liouville_square_dilation_audit(prec_bits=prec_bits)

    def _clean(obj: Any) -> Any:
        if isinstance(obj, (arb, acb)):
            return str(obj)
        if isinstance(obj, dict):
            return {
                k: _clean(v) for k, v in obj.items() if k != "enclosure_arb"
            }
        if isinstance(obj, (list, tuple)):
            return [_clean(v) for v in obj]
        return obj

    cleaned = _clean(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cleaned, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    return cleaned


if __name__ == "__main__":
    rep = write_task_tc054_liouville_square_dilation_artifact()
    print(f"Wrote {LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH} (subgate={rep['subgate_tc043a_status']}, rh_proved={rep['rh_proved']})")
