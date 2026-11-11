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
TASK_TC_055R_ID = "TASK-TC-055R"
TASK_TC_055R2_ID = "TASK-TC-055R2"
TASK_TC_056_ID = "TASK-TC-056"
TASK_TC_057_ID = "TASK-TC-057"
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
TC_055_IMPLEMENTATION_COMMIT = "c44df1ebfd10b8010e216214229a420ce8f3b5c2"
TC_055_REVIEWED_TIP = "07db77cf0ee62aa42e5c87b28a89a8f98eb3271e"
TC_055R_IMPLEMENTATION_COMMIT = "35b55405708ae7480263afc93e422b5626b1e134"
TC_055R_REVIEWED_TIP = "c6a685542c2dd584293b463272c4d95152907b3e"
TC_055R2_IMPLEMENTATION_COMMIT = "10f4f51246818e9d914113771ae906643dae9fa9"
TC_055R2_REVIEWED_TIP = "9a3755d977518ca6f0f1fb7ed3386e6a4a97d3ea"
TC_056R2_IMPLEMENTATION_COMMIT = "add6930233ebe0c8adf50da0e8a0ae6f18561975"
TC_056R2_REVIEWED_TIP = "8c92e89c62bdb434d29d7143bacf50308aab78a1"

LIOUVILLE_SQUARE_DILATION_LEAN_MODULE_PATH = (
    REPO_ROOT / "formal" / "RiemannScope" / "LiouvilleSquareDilation.lean"
)
LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_liouville_square_dilation.json"
)
TC_055_REVIEW_DOC_PATH = (
    REPO_ROOT / "docs" / "reviews" / "TC_055_SIMULTANEOUS_TAU_COMPATIBILITY.md"
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
        "pairing_counterexample_replacement_and_finite_reconstruction_tc055r",
        "smooth_coprime_positive_factorization_exists_unique_nat",
        "finite_smooth_coprime_cutoff_indexing_bijection_nat",
        "finite_liouville_reindexed_sum_and_excess_cutoff_identity_nat",
        "finite_gaussian_observable_reconstruction_and_weighted_cofactor_square",
        "finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056",
        "finite_alternating_unimodal_chain_contraction_tc056",
        "gaussian_prime_chain_unimodal_and_singleton_contraction_tc056",
        "mixed_interaction_decomposition_and_p_independence_tc056",
        "abstract_polylog_scale_bootstrap_and_weighted_contraction_tc057",
        "general_moebius_rough_prime_filtration_descent_tc057",
        "logarithmic_prime_power_descent_and_kernel_shift_tc057",
        "quadratic_prime_power_diagonal_off_diagonal_decomposition_tc057",
        "inherited_vs_canonical_cutoff_comparison_and_counterexample_tc057",
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
            "the finite integer coprimality sieve `actualPrimeExclusionSieveSum N_P n = ∑_{d ∣ gcd(n, N_P)} μ(d)^2 λ(n / d) = if n.Coprime N_P then liouvilleLambda n else 0` "
            "(infinite Dirichlet-series and operator-norm convergence are proved analytically outside Lean).",
        ),
        "prime_parity_control_multiplicative_and_moebius_separation_nat": (
            "actual_positive_integer_control_separation_theorem",
            "Genuinely arithmetic theorem over positive integers `p, q, m, n, d, r, s : ℕ` (`p.Prime`, `q.Prime`, `q ≠ p`) for "
            "single-prime parity `primeParityControl p n = (-1)^{v_p(n)}` and `twoAdicParityControl n = (-1)^{v_2(n)}`: proves complete multiplicativity, "
            "unit square, unconstrained common-factor cancellation, prime parity flip `a_p(p n) = -a_p(n)`, and concrete separation from "
            "`liouvilleLambda` and `actualFlatMoebiusSquareDivisorSum` at odd prime `n = 3` (`twoAdicParityControl 3 = 1 ≠ -1 = actualFlatMoebiusSquareDivisorSum 3`; "
            "infinite-series asymptotics of `Q_{a_2}(X)` and `E_{a_2}(Y)` are proved analytically outside Lean).",
        ),
        "near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing": (
            "conditional_finite_kernel_band_inequality_and_integer_sign_pairing_theorem",
            "Proves: (1) conditional on `hK : ∀ a b, 2 * K a b <= K a a + K b b` and `hBand : ∀ j < 2H + 1, bandSum j <= D_E`, the finite sum bounds "
            "`2 * ∑_{a < M} K a (a + h) <= ∑_{a < M} K a a + ∑_{a < M} K (a + h) (a + h)` and `∑_{j < 2H + 1} bandSum j <= (2H + 1) * D_E`, "
            "(2) for actual primes `p, q, r : ℕ` and `m ≠ 0`, `liouvilleLambda (p * m) = -liouvilleLambda m`, `liouvilleLambda (q * r * m) = liouvilleLambda m`, "
            "`liouvilleLambda (p * m) + liouvilleLambda (q * r * m) = 0`, and the paired sign-factorization identity "
            "`λ(p m) K_{pm} + λ(q r m) K_{qrm} = λ(m) (K_{qrm} - K_{pm})`, and "
            "(3) scalar rational constants `(3/8)*(1/8) = 3/64`, `(1/2)*(1 - 2/3) = 1/6`, and `(1/6)^2 = 1/36` "
            "(infinite-series kernel asymptotics and analytic kernel difference bounds are outside this theorem).",
        ),
        "pairing_counterexample_replacement_and_finite_reconstruction_tc055r": (
            "pointwise_kernel_amgm_counterexample_ratio_enclosure_and_scalar_truncation_algebra_theorem",
            "Proves (`TASK-TC-055R`, scoped to cutoff arithmetic, termwise multiplicativity, and scalar inequalities; "
            "see Theorems 13-16 below for the full smooth/coprime factorization bijection and finite-sum reconstruction): "
            "(1) unconditional pointwise factorized kernel integrand AM-GM identity and inequality "
            "`kernelPointwiseIntegrand g X4 a a + kernelPointwiseIntegrand g X4 b b - 2 * kernelPointwiseIntegrand g X4 a b = X4 * (g a - g b)^2 >= 0` for `X4 >= 0`, "
            "(2) exact arithmetic counterexample comparison refuting retired TC-055 Lemma 6.1 at `(Y, p, q, r, m, n) = (33, 11, 2, 5, 1, 11)` "
            "(conditional on `0 < K_11` and `K_10 < (1331/2890) * K_11`), "
            "(3) valid replacement two-sided kernel ratio enclosure implication `|K_a - K_b| <= max |L_low - 1| |L_high - 1| * K_b` (conditional on `0 <= K_b` and `L_low * K_b <= K_a <= L_high * K_b`), "
            "(4) non-integer cutoff counterexample at `u = 2.9` (`50/841 < 1/3^3 + 1/4^3 + 1/5^3 < 1/8`), repaired unimodal constant square `2 * (3/2)^3 = 27/4 < 3^3`, and `S = {3, 5, 7}` scalar product `(2/4)*(4/6)*(6/8) = 1/4`, and "
            "(5) pointwise cutoff equivalence `m * r <= T <-> r <= T / m` (`0 < m`), termwise Liouville multiplicativity `λ(m * r) * w(m * r) = λ(m) * (λ(r) * w(m * r))`, "
            "scalar tail energy algebra, and two-sided scalar quadratic L^2 transfer `v_full^2 <= 2 * v_T^2 + 2 * (v_full - v_T)^2 ∧ v_T^2 <= 2 * v_full^2 + 2 * (v_full - v_T)^2`.",
        ),
        "smooth_coprime_positive_factorization_exists_unique_nat": (
            "actual_positive_integer_smooth_coprime_factorization_theorem",
            "Unconditional arithmetic theorem (`TASK-TC-055R2` §3a) over `ℕ` for any finite prime set `P : Finset ℕ` (`∀ p ∈ P, p.Prime`, including `P = ∅`) and `n > 0`: "
            "proves `pSmoothPart P n * pCoprimePart P n = n`, `isPSmooth P (pSmoothPart P n)`, `Nat.Coprime (pCoprimePart P n) (primeProductModulus P)`, `0 < pCoprimePart P n`, "
            "and `∃! mr : ℕ × ℕ, mr.1 * mr.2 = n ∧ isPSmooth P mr.1 ∧ Nat.Coprime mr.2 (primeProductModulus P)` without assuming factorization as a hypothesis.",
        ),
        "finite_smooth_coprime_cutoff_indexing_bijection_nat": (
            "actual_finite_cutoff_indexing_bijection_and_boundary_theorem",
            "Unconditional finite indexing bijection (`TASK-TC-055R2` §3b) for `1 ≤ n ≤ T` (`T : ℕ`, `∀ p ∈ P, p.Prime`): proves `m * r ≤ T ↔ r ≤ T / m` (`0 < m`), "
            "characterizes membership in `smoothCoprimePairsUpTo P T`, establishes mutual two-sided inverse maps `n ↦ (pSmoothPart P n, pCoprimePart P n)` and `(m, r) ↦ m * r` "
            "between `Finset.Icc 1 T` and `smoothCoprimePairsUpTo P T` with equal cardinalities, and evaluates boundary/degenerate cases `T = 0`, `T = 1`, and `P = ∅`.",
        ),
        "finite_liouville_reindexed_sum_and_excess_cutoff_identity_nat": (
            "actual_reindexed_finite_liouville_sum_and_uncoupled_excess_theorem",
            "Unconditional finite-sum reconstruction theorem (`TASK-TC-055R2` §3c) for arbitrary weight `w : ℕ → ℝ`, `T : ℕ`, and finite prime set `P`: "
            "proves both smooth-outer (`∑_{m ≤ T, m ∈ S(P)} ∑_{1 ≤ r ≤ ⌊T/m⌋, gcd(r, N_P)=1} λ(m) λ(r) w(m r)`) and coprime-outer "
            "(`∑_{1 ≤ r ≤ T, gcd(r, N_P)=1} ∑_{m ≤ ⌊T/r⌋, m ∈ S(P)} λ(r) λ(m) w(m r)`) identities for `∑_{1 ≤ n ≤ T} λ(n) w(n)`, "
            "proves the exact excess sum `∑_{m ∈ S(P), m ≤ T} ∑_{r ∈ excessCoprimeFinset P m T} λ(m) λ(r) w(m r)` when `r ≤ T` replaces `r ≤ ⌊T/m⌋`, "
            "and proves vanishing of the excess at `P = ∅`, `T ≤ 1`, and `(P = {2}, T = 2)` alongside nonvanishing `= w 6` at `(P = {2}, T = 3)`.",
        ),
        "finite_gaussian_observable_reconstruction_and_weighted_cofactor_square": (
            "actual_finite_gaussian_reconstruction_and_pointwise_weighted_cofactor_square_theorem",
            "Unconditional finite Gaussian observable reconstruction theorem (`TASK-TC-055R2` §2 & §3c) for `0 ≤ X`, `T : ℕ`, and finite prime set `P`: "
            "discharges the `X^{5/2}` and `(m r)^{-3}` scaling identity to prove `finiteQLambda T X = ∑_{m ∈ S(P), m ≤ T} (λ(m)/√m) finiteQLambdaCoprime P (T/m) (X/m)`, "
            "`finiteQLambda T X = ∑_{1 ≤ r ≤ T, gcd(r, N_P)=1} cofactorFiberF P T r X` (`cofactorFiberF = (λ(r)/√r) finiteQLambdaSmooth P (T/r) (X/r)`), "
            "and the exact pointwise weighted square expansion `(finiteQLambda T X)^2 = ∑_r (1/r) Q_{λ,S(P),⌊T/r⌋}(X/r)^2 + ∑_r ∑_{s ≠ r} (λ(r)λ(s)/√(r s)) Q_{λ,S(P),⌊T/r⌋}(X/r) Q_{λ,S(P),⌊T/s⌋}(X/s)`, "
            "plus `finiteQLambda 0 X = 0` and `finiteQLambdaCoprime ∅ T X = finiteQLambda T X` (the `[Y, τ Y]` integral decomposition follows analytically outside Lean by finite linearity of the integral).",
        ),
        "finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056": (
            "actual_finite_prime_filtration_adjoining_and_pointwise_telescoping_theorem",
            "Unconditional finite prime-filtration theorem (`TASK-TC-056` §3) for any finite prime set `P : Finset ℕ` (`∀ q ∈ P, q.Prime`), prime `p ∉ P`, `T : ℕ`, and `X ≥ 0`: "
            "proves filtration endpoints `pointwiseGroupedEnergyV ∅ T X = pointwiseDiagonalD T X` and `pointwiseGroupedEnergyV (primesUpTo T) T X = (finiteQLambda T X)^2`, "
            "coupled prime-adjoining identity `cofactorFiberF (insert p P) T s X = ∑_{k ∈ admissiblePrimeExponents T p s} cofactorFiberF P T (s * p^k) X` (`gcd(s, N_{P∪{p}})=1`), "
            "stepwise identity `pointwiseDelta P p T X = 2 * ∑_s ∑_{k < l} cofactorFiberF P T (s * p^k) X * cofactorFiberF P T (s * p^l) X`, and ascending-prime list telescoping "
            "(the `[Y, τ Y]` integral transfer to `V_P(Y, T)` and `Δ_{P,p}(Y, T)` follows analytically outside Lean by finite linearity of the integral).",
        ),
        "finite_alternating_unimodal_chain_contraction_tc056": (
            "unconditional_finite_unimodal_alternating_chain_contraction_theorem",
            "Unconditional finite sequence theorem (`TASK-TC-056` §4) for any `K : ℕ` and nonnegative unimodal sequence `a : ℕ → ℝ` (`∀ k < K, 0 ≤ a k`, `IsUnimodalChain K a`): "
            "handles empty (`K = 0`), singleton (`K = 1`), ties, and zero extensions (`finiteChainMax 0 a = 0`), proving `|∑_{k < K} (-1)^k a k| ≤ finiteChainMax K a`, "
            "`(∑_{k < K} (-1)^k a k)^2 ≤ ∑_{k < K} (a k)^2`, strict-gap lower bound `min (a 0)^2 (a 1)^2 ≤ ∑_{k < K} (a k)^2 - (∑_{k < K} (-1)^k a k)^2` for `K ≥ 2`, and zero-extension invariance.",
        ),
        "gaussian_prime_chain_unimodal_and_singleton_contraction_tc056": (
            "actual_gaussian_prime_chain_unimodality_and_singleton_contraction_theorem",
            "Unconditional instantiation (`TASK-TC-056` §4) to the actual Gaussian prime-power chain `gaussianPrimeChain T p s m X k` (`p.Prime`, `s, m > 0`, `X ≥ 0`): "
            "proves consecutive admissible ratio identity `a_{k+1}/a_k = p^{-3} exp((X^2/(s m)^2) p^{-2k} (1 - p^{-2}))` and its monotonic decrease in `k`, "
            "proves `IsUnimodalChain (T + 1) (gaussianPrimeChain T p s m X)` unconditionally without assuming unimodality, proves chain sup/square contraction, "
            "and deduces `pointwiseGroupedEnergyV {p} T X ≤ pointwiseDiagonalD T X` with strict inequality `<` when `X > 0` and `p ≤ T` "
            "(strict integral inequality `V_{ {p} }(Y, T) < D_T(Y)` for `Y > 0, T ≥ p` follows analytically by continuity and positivity of `min(φ_1^2, φ_p^2)/X` on `[Y, τ Y]`).",
        ),
        "mixed_interaction_decomposition_and_p_independence_tc056": (
            "actual_mixed_interaction_decomposition_p_independence_and_shift_formula_theorem",
            "Unconditional decomposition and `P`-independence theorem (`TASK-TC-056` §5 & §6) for any finite prime set `P : Finset ℕ` (`∀ q ∈ P, q.Prime`), prime `p ∉ P`, `T : ℕ`, and `X ≥ 0`: "
            "proves `0 ≤ pointwiseContractionC P p T X`, `pointwiseMixedM ∅ p T X = 0`, exact decomposition `pointwiseDelta P p T X = pointwiseMixedM P p T X - pointwiseContractionC P p T X` "
            "(cancelling `λ(s)^2 = 1` and retaining ordered `m ≠ n` without an extra factor of `2`), equivalence with the ordered `k ≠ l` exponent expansion, "
            "`P`-independence `pointwiseContractionC P p T X = pointwiseContractionC ∅ p T X = pointwiseDiagonalD T X - pointwiseGroupedEnergyV {p} T X` via the `p`-free cofactor bijection `r = s * m`, "
            "and the exact alternating shift expansion `D_T - V_{ {p} } = 2 * ∑_{h ≥ 1, p^h ≤ T} (-1)^{h+1} ∑_{1 ≤ n ≤ ⌊T/p^h⌋} φ_n(X) φ_{n p^h}(X)`.",
        ),
        "abstract_polylog_scale_bootstrap_and_weighted_contraction_tc057": (
            "conditional_on_recursion_abstract_scale_bootstrap_lemma",
            "`CONDITIONAL_ON_RECURSION` real-induction lemma (`TASK-TC-057` §3): proves local boundedness and monotonicity of `monotoneScaleEnvelope E Y = sSup (E '' Set.Icc 1 Y)` from `0 ≤ E Z ≤ M_lin * Z`, "
            "justified `E`-to-`F` envelope passage when `Z / U_η Z` is nondecreasing, unconditional iteration from the assumed single-scale recursion hypothesis "
            "`∀ Y ≥ Y_star, monotoneScaleEnvelope E Y ≤ A_η * Y ^ η + B_η * monotoneScaleEnvelope E (Y / U_η Y)` (`B_η ≥ 0` arbitrary, NOT required `< 1`, provided `B_η * U_η Y ^ (-ε) ≤ 1 / 2` and `2 ≤ U_η Y ≤ Y`) "
            "yielding `E Y ≤ (F Y_star + 2 * A_η) * Y ^ ε` for all `Y ≥ 1`, plus single-step weighted multi-scale contraction (`∑ w_i u_i^{-sig} ≤ 1/2`) and weighted lower-bound obstruction (`m_0 > 0`); "
            "does NOT establish the recursion hypothesis for the actual Liouville energy.",
        ),
        "general_moebius_rough_prime_filtration_descent_tc057": (
            "actual_positive_integer_moebius_rough_descent_and_gaussian_scaling_theorem",
            "Unconditional finite arithmetic and Gaussian observable descent theorem (`TASK-TC-057` §4A, Route A) over actual positive integers (`2 ≤ U`, `T : ℕ`, `X ≥ 0`, multiplicative `a : ℕ → ℝ`): "
            "proves `smoothCutoffFinset (smoothPrimeSetBelow U) T = coprimeCutoffFinset (roughPrimeSetBand U T) T`, "
            "`finiteQGeneral a T X = finiteQSmoothBelow a U T X - ∑_{d ∈ roughSquarefreeDivisorsBand U T} (μ(d) a(d) / √d) finiteQGeneral a (T / d) (X / d)`, "
            "uniform Liouville rough sign `μ(d) λ(d) = 1` giving `-1/√d` across all `d ∈ roughSquarefreeDivisorsBand U T`, prime-only reduction when `T < U^2`, "
            "and concrete parity-control sign flip `μ(3) a_2(3) = -1 ≠ +1 = μ(15) a_2(15)` vs `μ(3) λ(3) = μ(15) λ(15) = 1`.",
        ),
        "logarithmic_prime_power_descent_and_kernel_shift_tc057": (
            "actual_positive_integer_mangoldt_liouville_descent_and_kernel_shift_theorem",
            "Unconditional finite arithmetic and shifted-Gaussian descent theorem (`TASK-TC-057` §4B, Route B) over actual positive integers (`a 1 = 1`, completely multiplicative `a`, `m, M, T : ℕ`, `X > 0`): "
            "proves `∑_{1 ≤ n ≤ T} a(n) (log n) (log(X/n))^r φ_n(X) = primePowerLogDescentSum a r T X`, Liouville instantiation over `primePowerPairsUpTo T` (with boundary `primePowerPairsUpTo 0 = primePowerPairsUpTo 1 = ∅`), "
            "shifted recurrence `(log X) * finiteQShifted a m T X = primePowerLogDescentSum a m T X + finiteQShifted a (m + 1) T X`, "
            "and `M`-fold telescoping for `log X ≠ 0`.",
        ),
        "quadratic_prime_power_diagonal_off_diagonal_decomposition_tc057": (
            "actual_positive_integer_quadratic_prime_power_decomposition_and_amgm_theorem",
            "Unconditional pointwise quadratic prime-power decomposition theorem (`TASK-TC-057` §4D, Route D) over actual positive integers (`T : ℕ`, `X > 0`): "
            "proves `((log X) * finiteQLambda T X - finiteQShifted λ 1 T X)^2 = ∑_{(p,k) ∈ primePowerPairsUpTo T} ((log p)^2 / p^k) finiteQLambda (T / p^k) (X / p^k)^2 + ∑_{pk1} ∑_{pk2 ≠ pk1} liouvillePrimePowerTerm T pk1 X * liouvillePrimePowerTerm T pk2 X` "
            "and the pointwise quadratic upper bound `finiteQLambda T X ^ 2 ≤ (2 / (log X)^2) (∑_{pk} liouvillePrimePowerTerm T pk X)^2 + (2 / (log X)^2) (finiteQShifted λ 1 T X)^2` for `log X ≠ 0` "
            "(the `[Y, τ Y]` integral transfer and unconditional `2 ζ''(1+ε)/(log Y)^2` diagonal contraction theorem are proved analytically outside Lean).",
        ),
        "inherited_vs_canonical_cutoff_comparison_and_counterexample_tc057": (
            "actual_cutoff_counterexample_ordering_and_small_scale_positivity_theorem",
            "Unconditional cutoff comparison, counterexample, and small-scale positivity theorem (`TASK-TC-057` §5): "
            "proves `u + 1 ≤ T / d → ⌈u⌉₊ ≤ T / d`, `canonicalCutoffT W ≤ inheritedCutoffL (W * d) d` for all `W ≥ 1` and `d ≥ 16`, "
            "all-`d` lower bound `(1/2) W^{5/4} d^{1/4} ≤ inheritedCutoffL (W * d) d` (`W ≥ 1`, `d ≥ 2`), "
            "concrete counterexample at `(Y = 9/4, d = 2)` where `inheritedCutoffL (9/4) 2 = 1 < 2 = canonicalCutoffT (9/8)` and `0 < finiteQLambda 1 (9/8) - finiteQLambda 2 (9/8)`, "
            "and uniform small-argument positivity `(1/24) w^{5/2} ≤ finiteQLambda L w` (`0 < finiteQLambda L w`) for all `L ≥ 1` and `0 < w ≤ 1`.",
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
                    "2. Exact square-divisor Möbius link sum_{d^2 | n} mu(n/d^2) = lambda(n): identifies D_lambda(s) = zeta(2s)/zeta(s), where the pole of zeta(2s) at s = 1/2 remains (producing the simple pole of M[Q_lambda](z) at z = 0), while the denominator pole of zeta(s) at s = 1 produces a simple zero of D_lambda(s) at s = 1 (D_lambda(1) = 0, unlike finite-prime parity controls a_S whose Dirichlet series have a simple pole at s = 1).",
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
                "pole_and_zero_locations_note": (
                    "In D_lambda(s) = zeta(2s) / zeta(s), the pole of zeta(2s) at s = 1/2 remains (giving the z = 0 pole of M[Q_lambda](z)), "
                    "while the denominator pole of zeta(s) at s = 1 produces a zero D_lambda(1) = 0. "
                    "A pole at s = 1/2 never cancels a pole at s = 1; the genuine cancellations are the removable 0/0 trivial-zero ratios "
                    "at negative even integers s = -2k (z_k = -(2k + 1/2))."
                ),
                "rows": trivial_zero_cancellation_rows,
                "all_trivial_zero_ratios_match_and_nonzero": all_trivial_zero_ratios_match,
            },
            "finite_prime_exclusion_and_inverse_rows": prime_exclusion_rows,
            "all_prime_exclusion_and_inverse_checks_hold": all_prime_exclusion_checks_ok,
        }
    finally:
        flint_ctx.prec = saved_prec


def _is_prime_int(n: int) -> bool:
    """Exact integer primality test for small/moderate positive integers."""
    if n < 2:
        return False
    if n == 2:
        return True
    if (n & 1) == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def _least_prime_ge_int(start_n: int) -> int:
    """Return the smallest prime q >= start_n using exact integer arithmetic."""
    cand = max(2, int(start_n))
    while not _is_prime_int(cand):
        cand += 1
    return cand


def _exact_arb_point_to_fraction(pt_arb: arb) -> Fraction:
    """Convert a finite zero-radius `arb` endpoint (`ball.lower()` or `ball.upper()`)
    into its exact dyadic rational `Fraction(man * 2^exp)` without float conversion.
    """
    if not pt_arb.is_finite():
        raise ValueError(f"Non-finite Arb endpoint {pt_arb!r}")
    man_z, exp_z = pt_arb.man_exp()
    man = int(man_z)
    exp = int(exp_z)
    if man == 0:
        return Fraction(0, 1)
    if exp >= 0:
        return Fraction(man << exp, 1)
    return Fraction(man, 1 << (-exp))


def _exact_arb_endpoints_as_fractions(ball: arb) -> Tuple[Fraction, Fraction]:
    """Return exact mathematical dyadic-rational endpoints `(mid - rad, mid + rad)`
    of a finite `arb` ball, independent of the ambient `flint_ctx.prec` setting
    (unlike `ball.lower()` / `ball.upper()`, which round outward to `flint_ctx.prec`).
    """
    if not ball.is_finite():
        raise ValueError(f"Arb ball must be finite, got {ball!r}")
    mid_q = _exact_arb_point_to_fraction(ball.mid())
    rad_q = _exact_arb_point_to_fraction(ball.rad())
    return (mid_q - rad_q, mid_q + rad_q)


def exact_floor_and_least_prime_strictly_above(
    u_val: Union[int, Fraction, str, arb],
) -> Tuple[int, int]:
    """Return `(floor(u), q_{>u})` where `q_{>u}` is the least prime strictly greater than `u`,
    computed strictly by exact integer / rational / dyadic-endpoint arithmetic (`TASK-TC-055R2` §5).

    - Binary `float` inputs are rejected (`TypeError`) so `3 +/- 2^{-100}` can never collapse to `3.0`.
    - Because an integer `n` satisfies `n > u` iff `n >= floor(u) + 1`, the least prime strictly
      above real `u` is `_least_prime_ge_int(max(2, floor(u) + 1))`.
    - For an `arb` ball `[u_low, u_high]`, exact dyadic rational floors `floor(u_low)` and
      `floor(u_high)` are compared; if `floor(u_low) != floor(u_high)` (the ball crosses an
      integer boundary), `ValueError` is raised rather than classifying by the midpoint.
    """
    if isinstance(u_val, bool) or isinstance(u_val, float):
        raise TypeError(
            f"Binary float/bool cutoff {u_val!r} is disallowed; pass int, Fraction, exact string, or arb."
        )
    if isinstance(u_val, arb):
        q_low, q_high = _exact_arb_endpoints_as_fractions(u_val)
        if q_low < 0:
            raise ValueError(f"Cutoff u must be >= 0, got {u_val!r}")
        floor_low = int(q_low.numerator // q_low.denominator)
        floor_high = int(q_high.numerator // q_high.denominator)
        if floor_low != floor_high:
            raise ValueError(
                f"Ambiguous cutoff Arb ball {u_val} crosses integer boundary between "
                f"floor={floor_low} and floor={floor_high}; midpoint classification is disallowed."
            )
        u_floor = floor_low
    elif isinstance(u_val, int):
        if u_val < 0:
            raise ValueError(f"Cutoff u must be >= 0, got {u_val!r}")
        u_floor = int(u_val)
    elif isinstance(u_val, (Fraction, str)):
        q = u_val if isinstance(u_val, Fraction) else Fraction(u_val)
        if q < 0:
            raise ValueError(f"Cutoff u must be >= 0, got {u_val!r}")
        u_floor = int(q.numerator // q.denominator)
    else:
        raise TypeError(f"Unsupported cutoff type: {type(u_val).__name__}")
    q_gt_u = _least_prime_ge_int(max(2, u_floor + 1))
    return u_floor, q_gt_u


def enclose_unrestricted_tail_floor_bound_arb(
    u_ball: arb,
    prec_bits: int = 256,
) -> arb:
    """Return a rigorous enclosure covering `1 / (2 floor(u)^2)` across EVERY `u` in `u_ball` (`u >= 1`),
    even when `u_ball` straddles one or more integer boundaries (taking `.union(...)` over all
    attainable `floor(u)` in `[floor(u_low), floor(u_high)]`, never classifying by midpoint).
    """
    q_low, q_high = _exact_arb_endpoints_as_fractions(u_ball)
    if q_low < 1:
        raise ValueError(f"Analytic floor bound requires u >= 1 across the entire ball, got {u_ball!r}")
    floor_low = int(q_low.numerator // q_low.denominator)
    floor_high = int(q_high.numerator // q_high.denominator)
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        low_val = arb(1) / (arb(2) * (arb(floor_high) ** 2))
        high_val = arb(1) / (arb(2) * (arb(floor_low) ** 2))
        return low_val.union(high_val)
    finally:
        flint_ctx.prec = saved_prec


def _exact_ceil_five_fourths_fraction(q: Fraction) -> int:
    """Return `T = ceil(q^{5/4})` for exact rational `q = p / d >= 1` using the exact
    integer-power predicate `(T - 1)^4 * d^5 < p^5 <= T^4 * d^5` without floats.
    """
    if q < 1:
        raise ValueError(f"T(Y) = ceil(Y^{{5/4}}) requires Y >= 1, got {q}")
    p5 = q.numerator ** 5
    d5 = q.denominator ** 5
    # Binary search T >= 1 with T^4 * d^5 >= p^5:
    lo = 1
    hi = 1 << (((p5.bit_length() - max(1, d5.bit_length()) + 4) // 4) + 2)
    while (hi ** 4) * d5 < p5:
        hi <<= 1
    while lo < hi:
        mid = (lo + hi) // 2
        if (mid ** 4) * d5 >= p5:
            hi = mid
        else:
            lo = mid + 1
    T = lo
    assert ((T - 1) ** 4) * d5 < p5 <= (T ** 4) * d5
    return T


def exact_ceil_five_fourths_power(
    Y_val: Union[int, Fraction, str, arb],
) -> int:
    """Return `T(Y) := ceil(Y^{5/4})` for `Y >= 1` via the exact integer-power predicate
        `(T - 1)^4 < Y^5 <= T^4`
    (`TASK-TC-055R2` §5), rejecting `float` inputs and rejecting `arb` balls that straddle
    a fourth-power boundary `(T - 1)^4 < Y^5 <= T^4` (`T_low != T_high`).
    Note: `T(1) = 1`, which is explicitly distinct from `M(Y) := ceil(max(2, Y^{5/4}))` (`M(1) = 2`).
    """
    if isinstance(Y_val, bool) or isinstance(Y_val, float):
        raise TypeError(
            f"Binary float/bool schedule input {Y_val!r} is disallowed; pass int, Fraction, exact string, or arb."
        )
    if isinstance(Y_val, arb):
        q_low, q_high = _exact_arb_endpoints_as_fractions(Y_val)
        if q_low < 1:
            raise ValueError(f"T(Y) = ceil(Y^{{5/4}}) requires Y >= 1, got {Y_val!r}")
        T_low = _exact_ceil_five_fourths_fraction(q_low)
        T_high = _exact_ceil_five_fourths_fraction(q_high)
        if T_low != T_high:
            raise ValueError(
                f"Ambiguous schedule Arb ball {Y_val} straddles fifth-fourth power boundary "
                f"between T={T_low} and T={T_high}; midpoint classification is disallowed."
            )
        return T_low
    if isinstance(Y_val, int):
        return _exact_ceil_five_fourths_fraction(Fraction(Y_val, 1))
    if isinstance(Y_val, (Fraction, str)):
        q = Y_val if isinstance(Y_val, Fraction) else Fraction(Y_val)
        return _exact_ceil_five_fourths_fraction(q)
    raise TypeError(f"Unsupported schedule input type: {type(Y_val).__name__}")


def exact_ceil_max_two_five_fourths_power(
    Y_val: Union[int, Fraction, str, arb],
) -> int:
    """Explicit companion convention `M(Y) := ceil(max(2, Y^{5/4})) = max(2, T(Y))` (`Y >= 1`),
    kept separate from `T(Y) = ceil(Y^{5/4})` (`T(1) = 1` vs `M(1) = 2`).
    """
    return max(2, exact_ceil_five_fourths_power(Y_val))


def verify_tc055_coupled_cutoff_and_norm_obstruction(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TASK-TC-055 Section 4, TASK-TC-055R Sections 4-5, and TASK-TC-055R2 Section 5 & Section 7:
    1. Signed energy expansion of E_{lambda,P_u}(Y) = int_Y^{tau Y} |Q_{lambda,P_u}(X)|^2 dX/X
       including all diagonal and cross-scale terms d_1, d_2 | N_u.
    2. Exact coprime decomposition for u >= 2 and exact rational / dyadic-endpoint floor & next-prime bounds:
           Q_{lambda,P_u}(w) = w^{5/2} exp(-w^2) + R_{lambda,P_u}(w),
           R_{lambda,P_u}(w) = w^{5/2} sum_{n > u, gcd(n, N_u)=1} (lambda(n)/n^3) exp(-w^2/n^2).
       Reproduces the non-integer cutoff counterexample at u = 2.9 and proves the distinct labeled bounds:
         - Unrestricted floor bound (u >= 1): sum_{n > u} n^{-3} <= 1 / (2 floor(u)^2);
         - Shifted-integral next-prime coprime bound (u >= 2): sum_{n > u, gcd(n,N_u)=1} n^{-3} <= 1 / (2 (q_{>u} - 1)^2);
         - First-term-split next-prime coprime bound (u >= 2): sum_{n > u, gcd(n,N_u)=1} n^{-3} <= 1 / q_{>u}^3 + 1 / (2 q_{>u}^2).
       Certifies both decimal boundary inputs (2.9, 3.0, 3.1, 4.9, 5.0, 5.1) AND exact 2^{-100} perturbations
       (3 - 2^{-100}, 3, 3 + 2^{-100}, 5 - 2^{-100}, 5, 5 + 2^{-100}), plus rejection of boundary-crossing Arb balls
       and exact integer-power schedule predicates `(T - 1)^4 < Y^5 <= T^4` for `T(Y) = ceil(Y^{5/4})` (`T(1) = 1`).
    3. Exact full-space operator norm theorem on H_eta = L^2((0, infty), X^{-2*eta} dX/X) (eta > 0):
           ||P_u^{-1}||_{H_eta -> H_eta}
             = sup_{b in R} prod_{p <= u} |1 + p^{-1/2 - eta} exp(-i b log p)|^{-1}
             = prod_{p <= u} (1 - p^{-1/2 - eta})^{-1},
       with Kronecker witness `b_* = 2513 * tau / (2 * log 2)` (`k_odd = 2513` is already odd).
    4. Off-critical mode test F_rho(X) = X^{rho - 1/2} (rho = x + i*y, x > 0).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()

        # 1. Non-integer cutoff counterexample at u = 2.9 (29/10) and boundary tests:
        u_29 = arb(29) / arb(10)
        false_bound_29 = arb(1) / (arb(2) * (u_29 ** 2))  # 50 / 841
        exact_tail_29 = arb(3).zeta() - arb(1) - arb(1) / arb(8)
        three_term_tail_29 = arb(1) / arb(27) + arb(1) / arb(64) + arb(1) / arb(125)
        violation_margin_full = exact_tail_29 - false_bound_29
        violation_margin_3terms = three_term_tail_29 - false_bound_29
        floor_bound_29 = arb(1) / (arb(2) * (arb(2) ** 2))  # 1 / 8
        u29_counterexample_certified = bool(
            violation_margin_full.lower() > 0
            and violation_margin_3terms.lower() > 0
            and (floor_bound_29 - exact_tail_29).lower() > 0
        )

        boundary_cutoff_rows: List[Dict[str, Any]] = []
        all_repaired_boundary_cutoffs_hold = True
        two_pow_100 = 1 << 100
        boundary_inputs = [
            ("2.9", Fraction(29, 10)),
            ("3.0", Fraction(3, 1)),
            ("3.1", Fraction(31, 10)),
            ("4.9", Fraction(49, 10)),
            ("5.0", Fraction(5, 1)),
            ("5.1", Fraction(51, 10)),
            ("3 - 2^{-100}", Fraction(3 * two_pow_100 - 1, two_pow_100)),
            ("3", Fraction(3, 1)),
            ("3 + 2^{-100}", Fraction(3 * two_pow_100 + 1, two_pow_100)),
            ("5 - 2^{-100}", Fraction(5 * two_pow_100 - 1, two_pow_100)),
            ("5", Fraction(5, 1)),
            ("5 + 2^{-100}", Fraction(5 * two_pow_100 + 1, two_pow_100)),
        ]
        for u_str, u_frac in boundary_inputs:
            u_arb = arb(u_frac.numerator) / arb(u_frac.denominator)
            u_floor, q_gt_u = exact_floor_and_least_prime_strictly_above(u_frac)
            u_floor_arb_check, q_gt_u_arb_check = exact_floor_and_least_prime_strictly_above(u_arb)
            arb_exact_match = (u_floor_arb_check == u_floor) and (q_gt_u_arb_check == q_gt_u)
            primes_le_u = tuple(p for p in (2, 3, 5, 7, 11, 13) if p <= u_floor)
            unrestricted_tail = arb(3).zeta() - sum(
                (arb(1) / (arb(n) ** 3) for n in range(1, u_floor + 1)), arb(0)
            )
            naive_real_bound = arb(1) / (arb(2) * (u_arb ** 2))
            repaired_floor_bound = arb(1) / (arb(2) * (arb(u_floor) ** 2))
            floor_ok = bool((repaired_floor_bound - unrestricted_tail).lower() > 0)
            naive_ok = bool((naive_real_bound - unrestricted_tail).lower() > 0)

            # Certified coprime tail |R_{lambda,P_u}(w)| at w = 2 against all 3 distinct labeled formulas:
            w_arb = arb(2)
            q_pu = evaluate_Q_lambda_prime_excluded_direct_certified_arb(
                w_arb, primes_P=primes_le_u, T_cutoff=1000, prec_bits=prec_bits
            )
            n1_term = (w_arb ** 2) * w_arb.sqrt() * (-(w_arb ** 2)).exp()
            abs_rem = abs(q_pu - n1_term)
            w_5_2 = (w_arb ** 2) * w_arb.sqrt()
            coprime_bound_floor = w_5_2 / (arb(2) * (arb(u_floor) ** 2))
            coprime_bound_q_minus_1_sq = w_5_2 / (arb(2) * (arb(q_gt_u - 1) ** 2))
            coprime_bound_q_split = w_5_2 * (
                arb(1) / (arb(q_gt_u) ** 3) + arb(1) / (arb(2) * (arb(q_gt_u) ** 2))
            )
            coprime_ok = bool(
                arb_exact_match
                and (coprime_bound_floor - abs_rem).lower() > 0
                and (coprime_bound_q_minus_1_sq - abs_rem).lower() > 0
                and (coprime_bound_q_split - abs_rem).lower() > 0
            )
            if not (floor_ok and coprime_ok):
                all_repaired_boundary_cutoffs_hold = False
            boundary_cutoff_rows.append({
                "u_label": u_str,
                "u_floor": u_floor,
                "primes_le_u": list(primes_le_u),
                "least_prime_strictly_above_u": q_gt_u,
                "exact_fraction_and_256bit_arb_agree": arb_exact_match,
                "unrestricted_tail_sum_n_gt_u_n_neg_3": serialize_arb_certified(unrestricted_tail),
                "naive_1_over_2_u_sq": serialize_arb_certified(naive_real_bound),
                "naive_bound_holds_for_unrestricted_tail": naive_ok,
                "repaired_1_over_2_floor_u_sq": serialize_arb_certified(repaired_floor_bound),
                "repaired_floor_bound_strictly_certified": floor_ok,
                "abs_R_lambda_Pu_at_w_2": serialize_arb_certified(abs_rem),
                "coprime_bound_w_5_2_over_2_floor_u_sq": serialize_arb_certified(coprime_bound_floor),
                "coprime_bound_w_5_2_over_2_q_minus_1_sq": serialize_arb_certified(coprime_bound_q_minus_1_sq),
                "coprime_bound_w_5_2_times_q_neg_3_plus_1_over_2_q_sq": serialize_arb_certified(coprime_bound_q_split),
                "coprime_bound_using_least_prime_q_gt_u": serialize_arb_certified(coprime_bound_q_split),
                "coprime_tail_bounds_strictly_certified": coprime_ok,
            })

        # Ambiguous boundary-crossing Arb ball test (midpoint = 3, straddling [3 - 2^{-100}, 3 + 2^{-100}])
        # and exact schedule T(Y) = ceil(Y^{5/4}) boundary audit:
        straddling_u_ball = arb(3, arb(2) ** (-100))
        ambiguous_u_rejected = False
        try:
            exact_floor_and_least_prime_strictly_above(straddling_u_ball)
        except ValueError:
            ambiguous_u_rejected = True
        straddling_floor_enclosure = enclose_unrestricted_tail_floor_bound_arb(straddling_u_ball, prec_bits=prec_bits)
        straddling_enclosure_covers_both = bool(
            straddling_floor_enclosure.contains(arb(1) / arb(8))
            and straddling_floor_enclosure.contains(arb(1) / arb(18))
        )

        schedule_boundary_cases = [
            ("1", Fraction(1, 1), 1, 2),
            ("1 + 2^{-100}", Fraction(two_pow_100 + 1, two_pow_100), 2, 2),
            ("16 - 2^{-100}", Fraction(16 * two_pow_100 - 1, two_pow_100), 32, 32),
            ("16", Fraction(16, 1), 32, 32),
            ("16 + 2^{-100}", Fraction(16 * two_pow_100 + 1, two_pow_100), 33, 33),
            ("81 - 2^{-100}", Fraction(81 * two_pow_100 - 1, two_pow_100), 243, 243),
            ("81", Fraction(81, 1), 243, 243),
            ("81 + 2^{-100}", Fraction(81 * two_pow_100 + 1, two_pow_100), 244, 244),
        ]
        schedule_boundary_rows: List[Dict[str, Any]] = []
        all_schedule_boundaries_exact = True
        for y_lbl, y_frac, expected_T, expected_M in schedule_boundary_cases:
            y_arb_pt = arb(y_frac.numerator) / arb(y_frac.denominator)
            T_frac = exact_ceil_five_fourths_power(y_frac)
            T_arb_pt = exact_ceil_five_fourths_power(y_arb_pt)
            M_frac = exact_ceil_max_two_five_fourths_power(y_frac)
            pred_ok = (
                T_frac == expected_T
                and T_arb_pt == expected_T
                and M_frac == expected_M
                and ((T_frac - 1) ** 4) * (y_frac.denominator ** 5)
                < (y_frac.numerator ** 5)
                <= (T_frac ** 4) * (y_frac.denominator ** 5)
            )
            if not pred_ok:
                all_schedule_boundaries_exact = False
            schedule_boundary_rows.append({
                "Y_label": y_lbl,
                "T_Y_ceil_Y_5_4": T_frac,
                "M_Y_ceil_max_2_Y_5_4": M_frac,
                "exact_power_predicate_and_arb_point_match": pred_ok,
            })

        straddling_Y_ball = arb(16, arb(2) ** (-100))
        ambiguous_Y_rejected = False
        try:
            exact_ceil_five_fourths_power(straddling_Y_ball)
        except ValueError:
            ambiguous_Y_rejected = True
        if not (ambiguous_u_rejected and straddling_enclosure_covers_both and ambiguous_Y_rejected and all_schedule_boundaries_exact):
            all_repaired_boundary_cutoffs_hold = False

        # 2. Exact coprime decomposition Q_{lambda,P_u}(w) = w^{5/2} exp(-w^2) + R_{lambda,P_u}(w)
        #    for integer u in {5, 7, 11, 13} (where floor(u) = u and q_{>u} >= u + 2):
        prime_sets_by_u = [
            (5, (2, 3, 5)),
            (7, (2, 3, 5, 7)),
            (11, (2, 3, 5, 7, 11)),
            (13, (2, 3, 5, 7, 11, 13)),
        ]
        coprime_tail_rows: List[Dict[str, Any]] = []
        all_coprime_tail_bounds_hold = True
        for u_val, primes_u in prime_sets_by_u:
            u_floor = int(u_val)
            u_floor_arb = arb(u_floor)
            for w_int in (1, 2, 4):
                w_arb = arb(w_int)
                q_pu = evaluate_Q_lambda_prime_excluded_direct_certified_arb(
                    w_arb, primes_P=primes_u, T_cutoff=1000, prec_bits=prec_bits
                )
                n1_term = (w_arb ** 2) * w_arb.sqrt() * (-(w_arb ** 2)).exp()
                rem_pu = q_pu - n1_term
                abs_rem = abs(rem_pu)
                bound_pu = (w_arb ** 2) * w_arb.sqrt() / (arb(2) * (u_floor_arb ** 2))
                margin = bound_pu - abs_rem
                bound_ok = bool(margin.lower() > 0)
                if not bound_ok:
                    all_coprime_tail_bounds_hold = False
                coprime_tail_rows.append({
                    "u": u_val,
                    "u_floor": u_floor,
                    "primes_le_u": list(primes_u),
                    "w": w_int,
                    "Q_lambda_Pu_w": serialize_arb_certified(q_pu),
                    "n_eq_1_gaussian_term": serialize_arb_certified(n1_term),
                    "R_lambda_Pu_w": serialize_arb_certified(rem_pu),
                    "abs_R_lambda_Pu_w": serialize_arb_certified(abs_rem),
                    "analytic_upper_bound_w_5_2_over_2_floor_u_sq": serialize_arb_certified(bound_pu),
                    "bound_minus_abs_R_margin": serialize_arb_certified(margin),
                    "bound_strictly_certified": bound_ok,
                })

        # 3. Exact full-space operator norm ||P_u^{-1}||_{H_eta -> H_eta} = prod_{p <= u} (1 - p^{-1/2 - eta})^{-1}
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

        # Concrete Kronecker simultaneous phase-alignment witness for P = {2, 3, 5} at eta = 1/4:
        # Scan odd harmonic integers k_odd in {1, 3, ..., 3999} directly so b_* = k_odd * tau / (2 * log 2)
        # makes exp(-i b_* log 2) = -1 (note k_odd = 2513 is already the odd integer, NOT 2*2513 + 1):
        eta_kron = arb(1) / arb(4)
        s_kron = arb(1) / arb(2) + eta_kron
        exact_sup_235 = arb(1)
        for p in (2, 3, 5):
            exact_sup_235 /= (arb(1) - (arb(p) ** (-s_kron)))
        best_k = 1
        best_cos_sum = 10.0
        log2_f = math.log(2.0)
        log3_f = math.log(3.0)
        log5_f = math.log(5.0)
        for k_odd in range(1, 4000, 2):
            b_f = k_odd * math.pi / log2_f
            c_sum = math.cos(b_f * log3_f) + math.cos(b_f * log5_f)
            if c_sum < best_cos_sum:
                best_cos_sum = c_sum
                best_k = k_odd
        b_witness_arb = arb(best_k) * (tau_arb / arb(2)) / arb(2).log()
        m_witness_acb = acb(1)
        for p in (2, 3, 5):
            phase_p = acb(0, -b_witness_arb * arb(p).log()).exp()
            m_witness_acb /= (acb(1) + (acb(p) ** (-acb(s_kron))) * phase_p)
        abs_m_witness = abs(m_witness_acb)
        ratio_witness_to_sup = abs_m_witness / exact_sup_235
        kronecker_witness_ok = bool(
            (best_k % 2 == 1)
            and (exact_sup_235 - abs_m_witness).lower() >= 0
            and (ratio_witness_to_sup - arb("0.999")).lower() > 0
        )

        # 4. Off-critical mode multiplier M_u(rho) = prod_{p <= u} (1 + p^{-rho}) at rho = 3/4 + 2i and 2/3 + 14i
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
            "non_integer_cutoff_counterexample_and_boundary_repair": {
                "falsified_assertion": "sum_{n > u} n^{-3} <= 1 / (2 u^2) for arbitrary real u >= 1",
                "counterexample_u": "2.9 (29/10)",
                "exact_unrestricted_tail_at_2_9": serialize_arb_certified(exact_tail_29),
                "three_term_lower_bound_n_3_4_5": serialize_arb_certified(three_term_tail_29),
                "claimed_1_over_2_u_sq_at_2_9": serialize_arb_certified(false_bound_29),
                "violation_margin_exact_minus_claimed": serialize_arb_certified(violation_margin_full),
                "violation_margin_3terms_minus_claimed": serialize_arb_certified(violation_margin_3terms),
                "repaired_floor_bound_1_over_2_floor_u_sq": serialize_arb_certified(floor_bound_29),
                "u29_counterexample_and_floor_repair_certified": u29_counterexample_certified,
                "repaired_formulas": {
                    "general_tail_for_real_u_ge_1": "sum_{n > u} n^{-3} = sum_{n >= floor(u) + 1} n^{-3} <= 1 / (2 floor(u)^2)",
                    "coprime_shifted_integral_bound_u_ge_2": "sum_{n > u, gcd(n, N_u)=1} n^{-3} <= sum_{n >= q_{>u}} n^{-3} <= 1 / (2 (q_{>u} - 1)^2) <= 1 / (2 floor(u)^2)",
                    "coprime_first_term_split_bound_u_ge_2": "sum_{n > u, gcd(n, N_u)=1} n^{-3} <= 1 / q_{>u}^3 + 1 / (2 q_{>u}^2) < 1 / u^3 + 1 / (2 u^2)",
                },
                "ambiguous_boundary_arb_ball_handling": {
                    "tested_u_ball": "[3 - 2^{-100}, 3 + 2^{-100}] (midpoint = 3)",
                    "discrete_decision_rejected_without_midpoint_classification": ambiguous_u_rejected,
                    "union_floor_bound_enclosure": serialize_arb_certified(straddling_floor_enclosure),
                    "union_enclosure_covers_1_over_8_and_1_over_18": straddling_enclosure_covers_both,
                    "tested_Y_ball": "[16 - 2^{-100}, 16 + 2^{-100}] (midpoint = 16)",
                    "discrete_schedule_decision_rejected": ambiguous_Y_rejected,
                },
                "schedule_T_Y_exact_power_predicate_audit": {
                    "T_Y_definition": "T(Y) := ceil(Y^{5/4}) characterized for Y >= 1 by (T - 1)^4 < Y^5 <= T^4 (in particular T(1) = 1)",
                    "M_Y_companion_convention": "M(Y) := ceil(max(2, Y^{5/4})) = max(2, T(Y)) (M(1) = 2 != T(1) = 1)",
                    "rows": schedule_boundary_rows,
                    "all_schedule_boundaries_exact": all_schedule_boundaries_exact,
                },
                "boundary_cutoff_rows": boundary_cutoff_rows,
                "all_repaired_boundary_cutoffs_hold": all_repaired_boundary_cutoffs_hold,
            },
            "coprime_decomposition_and_coupled_cutoff_attempt": {
                "identity": (
                    "For u >= 2, every integer n >= 2 with gcd(n, N_u) = 1 satisfies n >= q_{>u} >= floor(u) + 1 > u, so "
                    "Q_{lambda,P_u}(w) = w^{5/2} exp(-w^2) + R_{lambda,P_u}(w) with "
                    "|R_{lambda,P_u}(w)| <= w^{5/2} / (2 (q_{>u} - 1)^2) <= w^{5/2} / (2 floor(u)^2) and "
                    "|R_{lambda,P_u}(w)| <= w^{5/2} (1/q_{>u}^3 + 1/(2 q_{>u}^2))."
                ),
                "coupled_regime_diagnosis": (
                    "Substituting Q_{lambda,P_u}(X/m) = (X/m)^{5/2} exp(-X^2/m^2) + R_{lambda,P_u}(X/m) into the inverse "
                    "reconstruction Q_lambda(X) = sum_{m in S(P_u)} (lambda(m)/sqrt(m)) Q_{lambda,P_u}(X/m) splits Q_lambda(X) "
                    "into the P_u-smooth sum X^{5/2} sum_{m in S(P_u)} (lambda(m)/m^3) exp(-X^2/m^2) plus the nonsmooth sum "
                    "(integers n = m r >= 2 with m in S(P_u) and P_u-rough cofactor r >= q_{>u}, gcd(r, N_u) = 1, i.e., integers "
                    "having AT LEAST ONE prime factor > u; this strictly contains the P_u-rough integers m = 1, r >= q_{>u} whose "
                    "prime factors ALL exceed u). For any coupled cutoff u = Y^theta (theta in (0, 1)), P_u-smooth integers n ~ Y "
                    "have Dickman density rho_Dickman(1/theta) > 0, nonsmooth integers n ~ Y have Dickman-complement density "
                    "1 - rho_Dickman(1/theta) > 0 (carrying the order-Y unsigned residual via mixed smooth-rough composites), "
                    "whereas P_u-rough integers n ~ Y (gcd(n, N_u) = 1) have Buchstab density ~ omega_Buchstab(1/theta) / (theta log Y)."
                ),
                "coprime_tail_rows": coprime_tail_rows,
                "all_coprime_tail_bounds_hold": all_coprime_tail_bounds_hold,
            },
            "exact_full_space_operator_norm_obstruction": {
                "operator_norm_theorem": (
                    "For every finite prime cutoff u >= 2 and every eta > 0 on H_eta = L^2((0, infty), X^{-2*eta} dX/X): "
                    "||P_u^{-1}||_{H_eta -> H_eta} = sup_{b in R} prod_{p <= u} |1 + p^{-1/2 - eta} exp(-i b log p)|^{-1} "
                    "= prod_{p <= u} (1 - p^{-1/2 - eta})^{-1}."
                ),
                "five_step_analytic_proof": [
                    "1. Logarithmic unitary identification: U_eta : H_eta -> L^2(R, dt), (U_eta F)(t) = exp(-eta t) F(exp(t)) is a surjective unitary isomorphism with ||U_eta F||_{L^2(R)} = ||F||_{H_eta} and U_eta S_p U_eta^{-1} = p^{-eta} T_{log p}, where (T_a g)(t) = g(t - a).",
                    "2. Fourier multiplier representation: Under the unitary Fourier-Plancherel transform F : L^2(R, dt) -> L^2(R, db/tau), F U_eta P_u^{-1} U_eta^{-1} F^{-1} is multiplication by m_{u,eta}(b) = prod_{p <= u} (1 + p^{-1/2 - eta} exp(-i b log p))^{-1}.",
                    "3. Essential supremum equals supremum: Because b |-> m_{u,eta}(b) is continuous on R and every nonempty open interval in R has positive Lebesgue measure, ||m_{u,eta}||_{L^infty(R)} = ess sup_{b in R} |m_{u,eta}(b)| = sup_{b in R} |m_{u,eta}(b)|.",
                    "4. Upper bound: By the reverse triangle inequality |1 + p^{-1/2 - eta} exp(-i b log p)| >= 1 - p^{-1/2 - eta} > 0 for every p <= u and b in R, so sup_{b in R} |m_{u,eta}(b)| <= prod_{p <= u} (1 - p^{-1/2 - eta})^{-1}.",
                    "5. Matching lower bound via Kronecker's theorem: By the Fundamental Theorem of Arithmetic, {log p : p <= u} are linearly independent over Q. By continuous Kronecker simultaneous approximation (see Aoyama-Nakamura, arXiv:1204.4043, p. 9, Lemma 2.7), the curve {(exp(-i b log p))_{p <= u} : b in R} is dense in the torus T^{pi(u)}, so (-1, ..., -1) lies in its closure and sup_{b in R} |m_{u,eta}(b)| >= prod_{p <= u} (1 - p^{-1/2 - eta})^{-1}.",
                ],
                "research_implication_and_scope_distinction": (
                    "Because ||P_u^{-1}||_{H_eta -> H_eta} = prod_{p <= u} (1 - p^{-1/2 - eta})^{-1} is an EXACT equality on the full space H_eta, "
                    "uniform full-space inverse norms diverge as u -> infty for all 0 < eta <= 1/2, and NO 'signed improvement' of the full-space "
                    "operator norm on H_eta exists. Closing SUBGATE-TC-043A cannot proceed via a universal inverse-filter norm on H_eta; it must "
                    "exploit the specific structure of the arithmetic input Q_lambda (which does not concentrate its energy exclusively at Kronecker "
                    "resonant frequencies). This full-space operator obstruction does not disprove TC, RH, or boundedness of Q_lambda."
                ),
                "kronecker_phase_alignment_witness_P_2_3_5_eta_1_4": {
                    "odd_harmonic_index_k_odd": best_k,
                    "odd_multiple_of_half_tau_over_log2": best_k,
                    "b_witness_formula": f"{best_k} * tau / (2 * log 2)",
                    "indexing_convention_note": (
                        f"k_odd = {best_k} is already the odd harmonic integer in range(1, 4000, 2), "
                        f"so b_* = {best_k} * tau / (2 * log 2) (NOT (2 * {best_k} + 1) * tau / (2 * log 2))."
                    ),
                    "b_witness": serialize_arb_certified(b_witness_arb),
                    "abs_m_u_eta_at_b_witness": serialize_arb_certified(abs_m_witness),
                    "exact_supremum_prod_1_minus_p_neg_3_4_inv": serialize_arb_certified(exact_sup_235),
                    "ratio_witness_to_exact_supremum": serialize_arb_certified(ratio_witness_to_sup),
                    "witness_exceeds_99_9_percent_of_supremum": kronecker_witness_ok,
                },
                "rows": neumann_rows,
            },
            "weighted_norm_neumann_obstruction": {
                "dilation_norm_identity": "||S_p||_eta = p^{-eta} on H_eta = L^2((0, infty), X^{-2*eta} dX/X)",
                "exact_operator_norm_formula": "||P_u^{-1}||_{H_eta -> H_eta} = sup_{b in R} prod_{p <= u} |1 + p^{-1/2 - eta} exp(-i b log p)|^{-1} = prod_{p <= u} (1 - p^{-1/2 - eta})^{-1}",
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
    """Verify TASK-TC-055 Section 5 & TASK-TC-055R Section 5 (Full Off-Diagonal Domain & H=0 Identity Classification):
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
       with H = 0 explicitly classified as an exact algebraic identity (sum_{|m-n|<=0} K_Y(m,n) == D_E(Y))
       and H >= 1 certified by strictly positive outward Arb margin.
    4. Full energy domain note: removing |m - n| <= H leaves the entire off-diagonal domain |m - n| > H
       across all m, n >= 1; truncating to 1 <= m, n <= T(Y) requires the explicit tail energy bound
       int_Y^{tau Y} |Q_lambda(X) - Q_{lambda,T}(X)|^2 dX/X <= (tau^5 - 1) Y^5 / (20 T^4).
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
                if H_int == 0:
                    verification_kind = "exact_algebraic_identity"
                    ok_band = bool((band_partial - sum(diag_vals, arb(0))).contains(0)) and bool(margin.contains(0))
                else:
                    verification_kind = "certified_strict_inequality"
                    ok_band = bool(margin.lower() > 0)
                if not ok_band:
                    all_near_diagonal_bounds_hold = False
                near_diagonal_rows.append({
                    "Y": Y_int,
                    "H": H_int,
                    "two_H_plus_1": 2 * H_int + 1,
                    "verification_classification": verification_kind,
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
            "full_off_diagonal_domain_note": (
                "Removing the near-diagonal band |m - n| <= H leaves the full off-diagonal domain "
                "{(m, n) in Z_{>=1}^2 : |m - n| > H} across all scales (not merely m, n ~ Y). "
                "Localizing to 1 <= m, n <= T(Y) with T(Y) = ceil(Y^{5/4}) requires the proved finite-truncation "
                "tail energy bound int_Y^{tau Y} |Q_lambda(X) - Q_{lambda,T}(X)|^2 dX/X <= (tau^5 - 1) Y^5 / (20 T^4) <= (tau^5 - 1) / 20."
            ),
            "near_diagonal_rows": near_diagonal_rows,
            "all_near_diagonal_bounds_hold": all_near_diagonal_bounds_hold,
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_tc055_opposite_parity_dilation_pairing_and_obstruction(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TASK-TC-055 Section 6, TASK-TC-055R Sections 2/3/5, and TASK-TC-055R2 Sections 6/7:
    1. Opposite-parity prime-semiprime dilation sign pairing (preserved):
       For a prime p and semiprime s = q r (with q, r prime),
           lambda(p m) = -lambda(m),   lambda(q r m) = +lambda(m),
       so for every m, n >= 1:
           lambda(p m) lambda(n) K_Y(p m, n) + lambda(q r m) lambda(n) K_Y(q r m, n)
             = -lambda(m) lambda(n) [K_Y(p m, n) - K_Y(q r m, n)].
    2. Reproduction and retirement of the false uniform pairing bound (TC-055 Lemma 6.1):
       At (Y, p, q, r, m, n) = (33, 11, 2, 5, 1, 11) (a = q r m = 10, b = p m = 11),
       the retired formula claimed |K_{33}(11, 11) - K_{33}(10, 11)| / K_{33}(11, 11) <= 3993 / 10000 = 0.3993,
       whereas direct 256-bit Arb evaluation gives K_{33}(11, 11) = 1.01455519480741885677e-8...,
       K_{33}(10, 11) = 1.83203018490220578045e-9..., normalized difference = 0.8194252817117595...,
       and the elementary floating-point-free proof shows K_{33}(10, 11) / K_{33}(11, 11) <= (1331/1000) exp(-189/100) < 1331/2890,
       so |K_{33}(11, 11) - K_{33}(10, 11)| / K_{33}(11, 11) > 1559/2890 > 3993/10000.
    3. Valid replacement bounds for all Y > 0, 0 < a <= b, n > 0 (r_0 = b/a >= 1, Delta = a^{-2} - b^{-2} >= 0):
       (A) Exact integrand-ratio kernel enclosure:
               r_0^3 exp(-(tau Y)^2 Delta) K_Y(b, n) <= K_Y(a, n) <= r_0^3 exp(-Y^2 Delta) K_Y(b, n),
               |K_Y(a, n) - K_Y(b, n)| <= max(|r_0^3 exp(-(tau Y)^2 Delta) - 1|, |r_0^3 exp(-Y^2 Delta) - 1|) K_Y(b, n).
       (B) Transition relative-gap bound (retaining the full (b/a)^3 factor):
               |K_Y(a, n) - K_Y(b, n)| <= ((b - a) / a) (b / a)^3 (3 + 2 tau^2 Y^2 / a^2) K_Y(b, n).
           For a >= c Y (c > 0), the coefficient is ((b - a)/a)(b/a)^3 (3 + 2 tau^2 / c^2); obtaining a uniform
           O((b - a)/a) factor additionally requires a bounded ratio 1 <= b / a <= R (small/bounded-gap regime).
    4. Exact separation of densities, frequencies, and integer classes (TASK-TC-055R2 §6):
       - For P_1 = {5, 7, 11}, P_2 = {4, 6, 10}, N = lcm(5, 7, 11, 4, 6, 10) = 4620:
         * Natural density of integers coprime to N = 4620: prod_{p | 4620}(1 - 1/p) = 16/77;
         * Finite sample coprime frequency on 1 <= k <= 240: 50/240 = 5/24;
         * Periodic natural density of zero pairing weight W_pair(k) = 0 (mod 4620): 32/77;
         * Finite sample zero-pairing-weight frequency on 1 <= k <= 240: 101/240 (NOT the coprime density 16/77).
       - Strict separation of P-smooth integers (every prime factor in P), P-rough integers (every prime factor
         outside P), and nonsmooth integers (at least one prime factor outside P); order-Y unsigned residual for
         u = Y^theta comes from nonsmooth integers (density 1 - rho_Dickman(1/theta) > 0), whereas positive
         prime-prime energy (~ Y / (log Y)^2) is NOT a lower bound for total signed energy E_lambda(Y).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()

        # 1. Reproduce the (Y=33, p=11, q=2, r=5, m=1, n=11) counterexample to retired TC-055 Lemma 6.1:
        Y_ce = arb(33)
        k_11_11 = evaluate_energy_kernel_K_Y_certified_arb(Y_ce, 11, 11, prec_bits=prec_bits)
        k_10_11 = evaluate_energy_kernel_K_Y_certified_arb(Y_ce, 10, 11, prec_bits=prec_bits)
        abs_diff_ce = abs(k_11_11 - k_10_11)
        actual_norm_diff_ce = abs_diff_ce / k_11_11
        claimed_norm_bound_ce = arb(3993) / arb(10000)  # 0.3993
        claimed_abs_bound_ce = claimed_norm_bound_ce * k_11_11
        violation_norm_margin_ce = actual_norm_diff_ce - claimed_norm_bound_ce
        violation_abs_margin_ce = abs_diff_ce - claimed_abs_bound_ce

        # Elementary floating-point-free contradiction steps:
        # 33^2 * (1/10^2 - 1/11^2) = 1089 * 21 / 12100 = 189 / 100
        exp_neg_189_100 = (-arb(189) / arb(100)).exp()
        ratio_upper_analytic = (arb(1331) / arb(1000)) * exp_neg_189_100
        rational_majorant_1331_2890 = arb(1331) / arb(2890)
        rational_lower_diff_1559_2890 = arb(1559) / arb(2890)
        elementary_contradiction_ok = bool(
            (rational_majorant_1331_2890 - ratio_upper_analytic).lower() > 0
            and (rational_lower_diff_1559_2890 - claimed_norm_bound_ce).lower() > 0
            and (actual_norm_diff_ce - rational_lower_diff_1559_2890).lower() > 0
            and violation_norm_margin_ce.lower() > 0
            and violation_abs_margin_ce.lower() > 0
        )

        # 2. Certify both valid replacement bounds across all 5 required regimes:
        #    (comparable_transition_scale, large_Y_over_a_subtransition, unequal_indices, tiny_relative_gap, zero_gap_a_eq_b)
        test_cases_replacement = [
            ("comparable_transition_scale", 4, 8, 10, 8),
            ("comparable_transition_scale", 8, 18, 21, 15),
            ("comparable_transition_scale", 16, 40, 44, 20),
            ("large_Y_over_a_counterexample", 33, 10, 11, 11),
            ("large_Y_over_a_subtransition", 20, 4, 5, 10),
            ("widely_unequal_indices", 6, 4, 15, 25),
            ("tiny_relative_gap", 10, 100, 101, 100),
            ("zero_gap_a_eq_b", 8, 12, 12, 15),
        ]
        replacement_rows: List[Dict[str, Any]] = []
        all_replacement_bounds_hold = True
        for regime_lbl, Y_int, a_int, b_int, n_int in test_cases_replacement:
            Y_arb = arb(Y_int)
            a_arb = arb(a_int)
            b_arb = arb(b_int)
            r0_arb = b_arb / a_arb
            r0_cubed = r0_arb ** 3
            delta_arb = arb(1) / (a_arb * a_arb) - arb(1) / (b_arb * b_arb)
            L_low = r0_cubed * (-((tau_arb * Y_arb) ** 2) * delta_arb).exp()
            L_high = r0_cubed * (-(Y_arb * Y_arb) * delta_arb).exp()
            ratio_factor_max = arb(
                max(abs(L_low - arb(1)).upper(), abs(L_high - arb(1)).upper())
            )
            rel_gap_factor = (
                ((b_arb - a_arb) / a_arb)
                * r0_cubed
                * (arb(3) + arb(2) * ((tau_arb * Y_arb) ** 2) / (a_arb * a_arb))
            )

            k_a = evaluate_energy_kernel_K_Y_certified_arb(Y_arb, a_int, n_int, prec_bits=prec_bits)
            k_b = evaluate_energy_kernel_K_Y_certified_arb(Y_arb, b_int, n_int, prec_bits=prec_bits)
            abs_diff = abs(k_a - k_b)
            ratio_bound_val = ratio_factor_max * k_b
            rel_gap_bound_val = rel_gap_factor * k_b

            if a_int == b_int:
                ver_kind = "exact_algebraic_zero_identity"
                two_sided_ok = bool(a_int == b_int and (b_int - a_int) == 0)
                ratio_diff_ok = two_sided_ok
                rel_gap_ok = two_sided_ok
            else:
                ver_kind = "certified_strict_inequality"
                two_sided_ok = bool(
                    (k_a - L_low * k_b).lower() > 0 and (L_high * k_b - k_a).lower() > 0
                )
                ratio_diff_ok = bool((ratio_bound_val - abs_diff).lower() > 0)
                rel_gap_ok = bool((rel_gap_bound_val - abs_diff).lower() > 0)

            if not (two_sided_ok and ratio_diff_ok and rel_gap_ok):
                all_replacement_bounds_hold = False

            replacement_rows.append({
                "regime": regime_lbl,
                "Y": Y_int,
                "a": a_int,
                "b": b_int,
                "n": n_int,
                "b_over_a_cubed": str(Fraction(b_int, a_int) ** 3),
                "verification_classification": ver_kind,
                "K_Y_a_n": serialize_arb_certified(k_a),
                "K_Y_b_n": serialize_arb_certified(k_b),
                "abs_difference": serialize_arb_certified(abs_diff),
                "two_sided_ratio_lower_L_low_times_K_b": serialize_arb_certified(L_low * k_b),
                "two_sided_ratio_upper_L_high_times_K_b": serialize_arb_certified(L_high * k_b),
                "two_sided_ratio_enclosure_holds": two_sided_ok,
                "integrand_ratio_diff_upper_bound": serialize_arb_certified(ratio_bound_val),
                "integrand_ratio_diff_margin": serialize_arb_certified(ratio_bound_val - abs_diff),
                "integrand_ratio_diff_bound_holds": ratio_diff_ok,
                "transition_relative_gap_upper_bound": serialize_arb_certified(rel_gap_bound_val),
                "transition_relative_gap_margin": serialize_arb_certified(rel_gap_bound_val - abs_diff),
                "transition_relative_gap_bound_holds": rel_gap_ok,
            })

        # 3. Exact coprime density vs finite-sample zero-pairing-weight frequency audit
        #    for P_1 = {5, 7, 11}, P_2 = {4, 6, 10}, N = lcm(5, 7, 11, 4, 6, 10) = 4620:
        P1 = (5, 7, 11)
        P2 = (4, 6, 10)
        N_lcm = 1
        for x_factor in P1 + P2:
            N_lcm = math.lcm(N_lcm, x_factor)
        prime_divisors_N = tuple(p for p in range(2, N_lcm + 1) if _is_prime_int(p) and (N_lcm % p == 0))
        natural_coprime_density_frac = Fraction(1, 1)
        for p in prime_divisors_N:
            natural_coprime_density_frac *= Fraction(p - 1, p)

        # Full fundamental period 1 <= k <= N_lcm = 4620 exact counts:
        period_coprime_count = sum(1 for k in range(1, N_lcm + 1) if math.gcd(k, N_lcm) == 1)
        period_zero_w_pair_count = sum(
            1
            for k in range(1, N_lcm + 1)
            if (sum(1 for p in P1 if k % p == 0) + sum(1 for s in P2 if k % s == 0)) == 0
        )
        periodic_coprime_density_check = Fraction(period_coprime_count, N_lcm)
        periodic_zero_w_pair_density_frac = Fraction(period_zero_w_pair_count, N_lcm)

        w_bar = sum(Fraction(1, p) for p in P1) + sum(Fraction(1, s) for s in P2)
        sample_N_240 = 240
        unmatched_zero_weight_count_240 = 0
        coprime_to_N_count_240 = 0
        non_unit_weight_count = 0
        for k in range(1, sample_N_240 + 1):
            w_k = sum(1 for p in P1 if k % p == 0) + sum(1 for s in P2 if k % s == 0)
            if w_k == 0:
                unmatched_zero_weight_count_240 += 1
            if math.gcd(k, N_lcm) == 1:
                coprime_to_N_count_240 += 1
            if Fraction(w_k, 1) != w_bar:
                non_unit_weight_count += 1

        # Exact three-way classification check on 1 <= n <= 120 for P_demo = (2, 3, 5):
        P_demo = (2, 3, 5)
        N_demo = 30
        smooth_set_120 = set(generate_P_smooth_up_to(P_demo, 120))
        rough_set_120 = {n for n in range(1, 121) if math.gcd(n, N_demo) == 1}
        nonsmooth_set_120 = {n for n in range(1, 121) if n not in smooth_set_120}
        mixed_smooth_rough_120 = nonsmooth_set_120 - rough_set_120

        density_separation_ok = bool(
            N_lcm == 4620
            and prime_divisors_N == (2, 3, 5, 7, 11)
            and natural_coprime_density_frac == Fraction(16, 77)
            and periodic_coprime_density_check == natural_coprime_density_frac
            and periodic_zero_w_pair_density_frac == Fraction(32, 77)
            and coprime_to_N_count_240 == 50
            and unmatched_zero_weight_count_240 == 101
            and Fraction(unmatched_zero_weight_count_240, sample_N_240) != natural_coprime_density_frac
            and len(smooth_set_120) + len(nonsmooth_set_120) == 120
            and (rough_set_120 - {1}).issubset(nonsmooth_set_120)
            and (14 in mixed_smooth_rough_120)
        )

        return {
            "preserved_opposite_parity_sign_identity": (
                "For any prime p and semiprime s = q r (with q, r prime) and any integer m >= 1: "
                "lambda(p m) = -lambda(m), lambda(q r m) = +lambda(m), lambda(p m) + lambda(q r m) = 0, and "
                "lambda(p m) K_Y(p m, n) + lambda(q r m) K_Y(q r m, n) = -lambda(m) (K_Y(p m, n) - K_Y(q r m, n))."
            ),
            "retired_tc055_lemma61_counterexample": {
                "classification": "falsified_legacy_assertion",
                "retired_formula": (
                    "|K_Y(p m, n) - K_Y(q r m, n)| <= 3 (|q r - p| / min(p, q r)) (max(p, q r) / min(p, q r))^3 K_Y(max(p, q r) m, n)"
                ),
                "counterexample_parameters": {
                    "Y": 33,
                    "p": 11,
                    "q": 2,
                    "r": 5,
                    "qr": 10,
                    "m": 1,
                    "n": 11,
                },
                "K_33_11_11": serialize_arb_certified(k_11_11),
                "K_33_10_11": serialize_arb_certified(k_10_11),
                "abs_diff_K_33_11_11_minus_K_33_10_11": serialize_arb_certified(abs_diff_ce),
                "actual_normalized_difference": serialize_arb_certified(actual_norm_diff_ce),
                "retired_claimed_normalized_upper_bound_3993_over_10000": serialize_arb_certified(claimed_norm_bound_ce),
                "normalized_violation_margin_actual_minus_claimed": serialize_arb_certified(violation_norm_margin_ce),
                "absolute_violation_margin_actual_minus_claimed": serialize_arb_certified(violation_abs_bound_ce := violation_abs_margin_ce),
                "elementary_floating_point_free_contradiction": {
                    "exponent_lower_bound_33_sq_times_delta": "189/100 = 1.89",
                    "analytic_ratio_upper_bound_1331_over_1000_exp_neg_189_over_100": serialize_arb_certified(ratio_upper_analytic),
                    "rational_majorant_1331_over_2890": serialize_arb_certified(rational_majorant_1331_2890),
                    "rational_lower_bound_on_normalized_diff_1559_over_2890": serialize_arb_certified(rational_lower_diff_1559_2890),
                    "inequality_chain": (
                        "K_{33}(10,11)/K_{33}(11,11) <= (1331/1000) exp(-189/100) < 1331/2890 "
                        "=> |K_{33}(11,11) - K_{33}(10,11)| / K_{33}(11,11) > 1559/2890 > 3993/10000"
                    ),
                },
                "original_error_explanation": (
                    "In |g_X'(u)| = u^{-4} |2 X^2 / u^2 - 3| exp(-X^2 / u^2) (w = X/u), bounding |(2 w^2 - 3) exp(-w^2)| <= 3 "
                    "consumes the Gaussian factor exp(-w^2) = exp(-X^2 / u^2) and does NOT permit retaining a second Gaussian factor "
                    "exp(-X^2 / u_2^2) afterward. Retaining exp(-X^2 / b^2) for u in [a, b] requires bounding |2 X^2 / u^2 - 3| "
                    "without the Gaussian, which introduces the scale factor 3 + 2 tau^2 Y^2 / a^2."
                ),
                "counterexample_strictly_certified": elementary_contradiction_ok,
            },
            "valid_replacement_bounds": {
                "domain": "All Y > 0, 0 < a <= b, n > 0 (with r_0 = b/a >= 1, Delta = a^{-2} - b^{-2} >= 0)",
                "two_sided_integrand_ratio_enclosure": (
                    "r_0^3 exp(-(tau Y)^2 Delta) K_Y(b, n) <= K_Y(a, n) <= r_0^3 exp(-Y^2 Delta) K_Y(b, n)"
                ),
                "integrand_ratio_difference_bound": (
                    "|K_Y(a, n) - K_Y(b, n)| <= max(|r_0^3 exp(-(tau Y)^2 Delta) - 1|, |r_0^3 exp(-Y^2 Delta) - 1|) K_Y(b, n)"
                ),
                "transition_relative_gap_bound": (
                    "|K_Y(a, n) - K_Y(b, n)| <= ((b - a) / a) (b / a)^3 (3 + 2 tau^2 Y^2 / a^2) K_Y(b, n)"
                ),
                "useful_regime_and_non_saving_caveat": (
                    "For a >= c Y (c > 0), the relative-gap bound has explicit transition-restricted coefficient "
                    "((b - a)/a)(b/a)^3 (3 + 2 tau^2 / c^2), retaining the full (b/a)^3 factor. A uniform O((b - a)/a) K_Y(b, n) "
                    "statement holds ONLY when BOTH a >= c Y AND the ratio 1 <= b / a <= R is bounded (small/bounded-gap regime: "
                    "coeff <= R^3 (3 + 2 tau^2 / c^2)). This pairwise kernel inequality is NOT a global energy saving by itself "
                    "because its coefficient, divisor summation multiplicities, unmatched terms, and window boundary shifts must "
                    "all be bounded simultaneously."
                ),
                "rows": replacement_rows,
                "all_replacement_bounds_hold": all_replacement_bounds_hold,
            },
            "unmatched_residual_and_multiplicity_obstruction": {
                "tested_P1_primes": list(P1),
                "tested_P2_semiprimes": list(P2),
                "lcm_modulus_N": N_lcm,
                "prime_divisors_of_N": list(prime_divisors_N),
                "natural_coprime_density_prod_1_minus_1_over_p": f"{natural_coprime_density_frac.numerator}/{natural_coprime_density_frac.denominator}",
                "periodic_zero_pairing_weight_natural_density_mod_4620": f"{periodic_zero_w_pair_density_frac.numerator}/{periodic_zero_w_pair_density_frac.denominator}",
                "mean_divisor_weight_w_bar": str(w_bar),
                "k_range_tested": "1 <= k <= 240",
                "finite_sample_coprime_to_N_count_1_to_240": coprime_to_N_count_240,
                "finite_sample_coprime_to_N_frequency_unreduced": f"{coprime_to_N_count_240}/{sample_N_240}",
                "finite_sample_coprime_to_N_frequency_reduced": str(Fraction(coprime_to_N_count_240, sample_N_240)),
                "unmatched_k_count_with_W_pair_eq_0": unmatched_zero_weight_count_240,
                "finite_sample_zero_pairing_weight_frequency_1_to_240": f"{unmatched_zero_weight_count_240}/{sample_N_240}",
                "k_count_with_W_pair_ne_w_bar": non_unit_weight_count,
                "density_and_class_separation_verified": density_separation_ok,
                "integer_class_definitions_and_partition_audit_P_2_3_5_up_to_120": {
                    "P_smooth_definition": "S(P) = {n >= 1 : every prime factor p | n belongs to P}",
                    "P_rough_definition": "{n >= 1 : gcd(n, N_P) = 1, i.e., every prime factor p | n lies outside P}",
                    "nonsmooth_definition": "Z_{>=1} \\ S(P) = {n >= 1 : at least one prime factor p | n lies outside P}",
                    "P_smooth_count_1_to_120": len(smooth_set_120),
                    "P_rough_count_1_to_120": len(rough_set_120),
                    "nonsmooth_count_1_to_120": len(nonsmooth_set_120),
                    "mixed_smooth_rough_composite_count_1_to_120": len(mixed_smooth_rough_120),
                },
                "fixed_vs_growing_factor_set_separation": {
                    "fixed_finite_factor_set": (
                        "For P_1 = {5, 7, 11}, P_2 = {4, 6, 10}, N = lcm(5, 7, 11, 4, 6, 10) = 4620 has prime divisors {2, 3, 5, 7, 11} "
                        "and natural coprime density prod_{p | 4620}(1 - 1/p) = 16/77 (50/240 = 5/24 on 1 <= k <= 240), whereas the "
                        "zero-pairing-weight set {k : W_pair(k) = 0} (neither divisible by 5, 7, 11 nor by 4, 6) has periodic natural "
                        "density (8/12) * (48/77) = 32/77 mod 4620 and finite sample frequency 101/240 on 1 <= k <= 240."
                    ),
                    "growing_factor_set_and_unmatched_primes_scale": (
                        "For a growing cutoff u = Y^theta (0 < theta < 1), the three integer classes have distinct densities: "
                        "(i) Y^theta-smooth integers have Dickman density rho_Dickman(1/theta) in (0, 1); "
                        "(ii) Y^theta-rough integers (every prime factor > Y^theta) have Buchstab density ~ omega_Buchstab(1/theta) / (theta log Y) "
                        "(decaying as 1/log Y, NOT positive constant density); in particular, unmatched primes p in [Y, tau Y] have count "
                        "pi(tau Y) - pi(Y) ~ (tau - 1) Y / log Y and prime-prime transition sum scale Y / (log Y)^2 (which is a restricted "
                        "positive sub-sum, NOT a lower bound for the total signed energy E_lambda(Y) because prime-composite and "
                        "composite-composite cross terms carry opposite signs); "
                        "(iii) nonsmooth integers (at least one prime factor > Y^theta, comprising Y^theta-rough integers > 1 together "
                        "with mixed smooth-rough composites n = m r with m > 1 smooth and r > 1 rough) have positive Dickman complement "
                        "density 1 - rho_Dickman(1/theta) > 0, accounting for the order-Y unsigned residual."
                    ),
                },
            },
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_Q_aS_certified_arb(
    X_val: Union[arb, int, float, str, Fraction],
    primes_S: Tuple[int, ...] = (3, 5, 7),
    T_cutoff: int = 1200,
    prec_bits: int = 256,
) -> arb:
    """Certify Q_{a_S}(X) := X^{5/2} sum_{n>=1} (a_S(n) / n^3) exp(-X^2 / n^2)
    with explicit integer-cutoff tail bound X^{5/2} / (2 T^2).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X = arb(X_val.numerator) / arb(X_val.denominator) if isinstance(X_val, Fraction) else arb(X_val)
        X_sq = X * X
        X_5_2 = X_sq * X.sqrt()
        partial = arb(0)
        for n in range(1, T_cutoff + 1):
            a_n = finite_prime_parity_aS_int(n, primes_S=primes_S)
            n_arb = arb(n)
            partial += arb(a_n) * (-X_sq / (n_arb * n_arb)).exp() / (n_arb ** 3)
        center = X_5_2 * partial
        tail_bound = X_5_2 / (arb(2) * (arb(T_cutoff) ** 2))
        return inflate_arb_with_nonneg_bound(center, tail_bound)
    finally:
        flint_ctx.prec = saved_prec


def evaluate_Q_a2_dyadic_series_certified_arb(
    X_val: Union[arb, int, float, str, Fraction],
    K_dyadic: int = 24,
    T_cutoff: int = 1200,
    dyadic_coeff: Union[arb, int] = 2,
    prec_bits: int = 256,
) -> arb:
    """Evaluate the dyadic expansion
        Q_{a_2}(X) = Q_1(X) + 2 * sum_{k >= 1} (-1)^k 2^{-k/2} Q_1(X / 2^k)
    with explicit small-scale series tail bound `|dyadic_coeff| * zeta(3) * X^{5/2} * 8^{-K_dyadic} / 7`.
    The parameter `dyadic_coeff` defaults to the exact coefficient `2` (`TASK-TC-055R2` §4)
    and allows regression tests to verify directly that substituting `sqrt(2)` fails.
    """
    if K_dyadic < 1:
        raise ValueError(f"K_dyadic must be >= 1, got {K_dyadic}")
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X = arb(X_val.numerator) / arb(X_val.denominator) if isinstance(X_val, Fraction) else arb(X_val)
        coeff_arb = dyadic_coeff if isinstance(dyadic_coeff, arb) else arb(dyadic_coeff)
        q0 = evaluate_Q_1_unweighted_certified_arb(X, T_cutoff=T_cutoff, prec_bits=prec_bits)
        acc = arb(0)
        inv_sqrt2 = arb(1) / arb(2).sqrt()
        pow_inv_sqrt2 = arb(1)
        pow_two = arb(1)
        for k in range(1, K_dyadic + 1):
            pow_inv_sqrt2 *= inv_sqrt2
            pow_two *= arb(2)
            sign_k = arb(-1) if (k % 2 == 1) else arb(1)
            t_k = max(120, T_cutoff // max(1, 1 << (k // 2)))
            qk = evaluate_Q_1_unweighted_certified_arb(X / pow_two, T_cutoff=t_k, prec_bits=prec_bits)
            acc += sign_k * pow_inv_sqrt2 * qk
        center = q0 + coeff_arb * acc
        X_5_2 = (X * X) * X.sqrt()
        tail_bound = (
            abs(coeff_arb)
            * arb(3).zeta()
            * X_5_2
            / (arb(7) * (arb(8) ** K_dyadic))
        )
        return inflate_arb_with_nonneg_bound(center, tail_bound)
    finally:
        flint_ctx.prec = saved_prec


def verify_tc055_multiplicative_parity_controls(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify TASK-TC-055 Section 7, TASK-TC-055R Sections 5/8, and TASK-TC-055R2 Section 4:
    1. Hypothesis-by-hypothesis comparison between actual Liouville lambda(n) = (-1)^{Omega(n)},
       the 2-adic parity control a_2(n) = (-1)^{v_2(n)}, and general finite-prime parity controls
       a_S(n) = (-1)^{sum_{p in S} v_p(n)}.
    2. Exact dyadic identity with coefficient 2 (NOT sqrt(2)):
           Q_{a_2}(X) = Q_1(X) + 2 sum_{k >= 1} (-1)^k 2^{-k/2} Q_1(X / 2^k).
       - Exact unimodal constant:
             C_{1,uni} := 2 (3 / (2 e))^{3/2} = (1 / sqrt(2)) (3 / e)^{3/2} = 0.81983255788372007678... < (3 / e)^{3/2}.
         Summing the first-order unimodal error O(w^{-1/2}) over 1 <= k <= floor(log_2 X) yields
             Q_{a_2}(X) = sqrt(X)/6 + O(X^{-1/2} log X),   E_{a_2}(Y) = ((tau - 1)/36) Y + O(log Y).
       - Second-order periodic Bernoulli Euler-Maclaurin bound |Q_1(w) - sqrt(w)/2| <= 3 w^{-3/2} (w > 0):
         Splitting at L = floor(log_2 X) for ALL X >= 1 (including L = 0 on 1 <= X < 2, where the 1 <= k <= L sum is empty):
           * k = 0 error: |Q_1(X) - sqrt(X)/2| <= 3 X^{-3/2} <= 3 X^{-1/2};
           * Large-scale error 1 <= k <= L:
                 2 sum_{k=1}^L 2^{-k/2} * 3 (X/2^k)^{-3/2} = 6 X^{-3/2} sum_{k=1}^L 2^k <= 12 X^{-1/2};
           * Omitted main-term tail k > L:
                 2 sum_{k > L} 2^{-k/2} (1/2) sqrt(X/2^k) = sqrt(X) 2^{-L} <= 2 X^{-1/2};
           * Small-scale tail k > L (using |Q_1(w)| <= zeta(3) w^{5/2}):
                 2 zeta(3) X^{5/2} sum_{k > L} 8^{-k} = (2 zeta(3) / 7) X^{5/2} 8^{-L} <= (16 zeta(3) / 7) X^{-1/2}.
         Summing all four contributions gives the conservative certified constant:
             C_{a_2} := 3 + 12 + 2 + (16/7) zeta(3) = 17 + (16/7) zeta(3) = 19.7475586357933605...
         (Note: the audit invalidates the prior 14.84231228 derivation, which erroneously substituted sqrt(2)
         for the dyadic coefficient 2; it does not claim that 14.84231228 is numerically false.)
       - Energy remainder derived directly from |Q_{a_2}(X) - sqrt(X)/6| <= C_{a_2} X^{-1/2} for all Y >= 1:
             |E_{a_2}(Y) - ((tau - 1)/36) Y| <= (C_{a_2} log tau)/3 + C_{a_2}^2 (1 - tau^{-1}) Y^{-1}
                                             <= C_{E,a_2} := (C_{a_2} log tau)/3 + C_{a_2}^2 (1 - tau^{-1}) = O(1).
    3. Multi-prime control S = {3, 5, 7} (scoped strictly to established mean and leading asymptotics):
       Control mean prod_{p in {3,5,7}} (p - 1)/(p + 1) = (2/4)*(4/6)*(6/8) = 1/4, giving leading asymptotics
           Q_{a_{3,5,7}}(X) ~ sqrt(X)/8,   E_{a_{3,5,7}}(Y) ~ ((tau - 1)/64) Y
       (stronger O(X^{-1/2}) / O(1) multi-prime remainder bounds are not claimed here).
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()
        one_sixth = arb(1) / arb(6)
        tau_minus_1_over_36 = (tau_arb - arb(1)) / arb(36)
        three_over_e_pow_3_2 = (arb(3) / arb(1).exp()) ** (arb(3) / arb(2))
        exact_C1_unimodal = arb(2) * ((arb(3) / (arb(2) * arb(1).exp())) ** (arb(3) / arb(2)))
        alt_C1_unimodal = three_over_e_pow_3_2 / arb(2).sqrt()

        c_k0 = arb(3)
        c_large_scale = arb(12)
        c_omitted_main_tail = arb(2)
        c_small_scale_tail = (arb(16) / arb(7)) * arb(3).zeta()
        C_a2_second_order = c_k0 + c_large_scale + c_omitted_main_tail + c_small_scale_tail
        C_E_a2_uniform_O1 = (
            (C_a2_second_order * tau_arb.log()) / arb(3)
            + (C_a2_second_order * C_a2_second_order) * (arb(1) - (arb(1) / tau_arb))
        )

        unimodal_constant_repair_ok = bool(
            (exact_C1_unimodal - alt_C1_unimodal).contains(0)
            and (three_over_e_pow_3_2 - exact_C1_unimodal).lower() > 0
            and (C_a2_second_order - (arb(17) + (arb(16) / arb(7)) * arb(3).zeta())).contains(0)
        )

        # 1. Certify |Q_1(X) - sqrt(X)/2| <= C_{1,uni} X^{-1/2}, |Q_1(X) - sqrt(X)/2| <= 3 X^{-3/2},
        #    |Q_{a_2}(X) - sqrt(X)/6| <= C_{a_2} X^{-1/2}, exact dyadic series with coefficient 2 (vs false sqrt(2)),
        #    and (I + 2^{-1/2} S_2) Q_{a_2}(X) = Q_1(X) - 2^{-1/2} Q_1(X/2) across X in {1, 2, 4, 8, 16, 32, 64}
        #    (explicitly covering L = floor(log_2 X) = 0 at X = 1):
        q_a2_rows: List[Dict[str, Any]] = []
        all_q1_bounds_and_dyadic_identities_hold = True
        inv_sqrt2 = arb(1) / arb(2).sqrt()
        for X_int in (1, 2, 4, 8, 16, 32, 64):
            L_split = int(X_int).bit_length() - 1  # exact floor(log_2 X_int) for integer X_int >= 1
            X_arb = arb(X_int)
            t_cut = max(1600, 80 * X_int)
            q1_x = evaluate_Q_1_unweighted_certified_arb(X_arb, T_cutoff=t_cut, prec_bits=prec_bits)
            q1_half_x = evaluate_Q_1_unweighted_certified_arb(X_arb / arb(2), T_cutoff=t_cut, prec_bits=prec_bits)
            q1_err = abs(q1_x - X_arb.sqrt() / arb(2))
            q1_bnd_uni = exact_C1_unimodal / X_arb.sqrt()
            q1_bnd_em2 = arb(3) / (X_arb * X_arb.sqrt())
            q1_ok = bool((q1_bnd_uni - q1_err).lower() > 0 and (q1_bnd_em2 - q1_err).lower() > 0)

            qa2_x = evaluate_Q_a2_certified_arb(X_arb, T_cutoff=t_cut, prec_bits=prec_bits)
            qa2_dyadic_coeff2 = evaluate_Q_a2_dyadic_series_certified_arb(
                X_arb, K_dyadic=24, T_cutoff=t_cut, dyadic_coeff=2, prec_bits=prec_bits
            )
            qa2_dyadic_wrong_sqrt2 = evaluate_Q_a2_dyadic_series_certified_arb(
                X_arb, K_dyadic=24, T_cutoff=t_cut, dyadic_coeff=arb(2).sqrt(), prec_bits=prec_bits
            )
            dyadic_series_diff = qa2_x - qa2_dyadic_coeff2
            wrong_sqrt2_gap = abs(qa2_x - qa2_dyadic_wrong_sqrt2)
            dyadic_coeff2_consistency_ok = bool(
                dyadic_series_diff.contains(0) and wrong_sqrt2_gap.lower() > 0
            )

            qa2_half_x = evaluate_Q_a2_certified_arb(X_arb / arb(2), T_cutoff=t_cut, prec_bits=prec_bits)
            lhs_dyadic = qa2_x + inv_sqrt2 * qa2_half_x
            rhs_odd = q1_x - inv_sqrt2 * q1_half_x
            dyadic_diff = lhs_dyadic - rhs_odd
            dyadic_ok = bool(dyadic_diff.contains(0)) and bool(lhs_dyadic.lower() > 0)

            qa2_err = abs(qa2_x - X_arb.sqrt() / arb(6))
            qa2_em2_bnd = C_a2_second_order / X_arb.sqrt()
            qa2_em2_margin = qa2_em2_bnd - qa2_err
            qa2_em2_ok = bool(qa2_em2_margin.lower() > 0)

            ratio_to_sqrt_X = qa2_x / X_arb.sqrt()
            scaled_rem_X_half = (qa2_x - X_arb.sqrt() / arb(6)) * X_arb.sqrt()
            if not (q1_ok and dyadic_ok and qa2_em2_ok and dyadic_coeff2_consistency_ok):
                all_q1_bounds_and_dyadic_identities_hold = False
            q_a2_rows.append({
                "X": X_int,
                "L_eq_floor_log2_X": L_split,
                "Q_a2_X": serialize_arb_certified(qa2_x),
                "Q_a2_dyadic_series_coeff_2": serialize_arb_certified(qa2_dyadic_coeff2),
                "direct_minus_dyadic_coeff_2_consistency": serialize_arb_certified(dyadic_series_diff),
                "erroneous_sqrt2_dyadic_series_discrepancy": serialize_arb_certified(wrong_sqrt2_gap),
                "dyadic_coeff_2_verified_and_sqrt2_refuted": dyadic_coeff2_consistency_ok,
                "leading_sqrt_X_over_6": serialize_arb_certified(X_arb.sqrt() / arb(6)),
                "ratio_Q_a2_over_sqrt_X": serialize_arb_certified(ratio_to_sqrt_X),
                "scaled_remainder_sqrt_X_times_diff": serialize_arb_certified(scaled_rem_X_half),
                "second_order_em_bound_C_a2_X_neg_half": serialize_arb_certified(qa2_em2_bnd),
                "second_order_em_bound_margin": serialize_arb_certified(qa2_em2_margin),
                "second_order_em_bound_holds": qa2_em2_ok,
                "dyadic_filter_lhs_minus_Q_odd_rhs": serialize_arb_certified(dyadic_diff),
                "dyadic_filter_strictly_positive_and_matches_Q_odd": dyadic_ok,
                "Q_1_exact_unimodal_and_em2_bounds_hold": q1_ok,
            })

        # 2. Certify E_{a_2}(Y) = ((tau - 1) / 36) Y + R_{E,a_2}(Y) with explicit derived bound
        #    |R_{E,a_2}(Y)| <= (C_{a_2} log tau)/3 + C_{a_2}^2 (1 - tau^{-1}) Y^{-1} across Y in {1, 4, 8, 16, 32}:
        e_a2_rows: List[Dict[str, Any]] = []
        all_e_a2_positive = True
        all_e_a2_remainder_bounds_hold = True
        for Y_int in (1, 4, 8, 16, 32):
            Y_arb = arb(Y_int)
            t_cut = max(1200, 35 * Y_int)
            e_a2 = evaluate_E_a2_certified_arb(Y_arb, N_subintervals=32, T_cutoff=t_cut, prec_bits=prec_bits)
            leading_e = tau_minus_1_over_36 * Y_arb
            ratio_e_over_Y = e_a2 / Y_arb
            abs_rem_e = abs(e_a2 - leading_e)
            derived_e_rem_bnd = (
                (C_a2_second_order * tau_arb.log()) / arb(3)
                + (C_a2_second_order * C_a2_second_order) * (arb(1) - (arb(1) / tau_arb)) / Y_arb
            )
            e_rem_margin = derived_e_rem_bnd - abs_rem_e
            cap_minus_derived = (
                (C_a2_second_order * C_a2_second_order)
                * (arb(1) - (arb(1) / tau_arb))
                * (arb(Y_int - 1) / Y_arb)
            )
            rem_bnd_ok = bool(e_rem_margin.lower() > 0) and bool(cap_minus_derived.lower() >= 0)
            if not bool(e_a2.lower() > 0):
                all_e_a2_positive = False
            if not rem_bnd_ok:
                all_e_a2_remainder_bounds_hold = False
            e_a2_rows.append({
                "Y": Y_int,
                "E_a2_Y": serialize_arb_certified(e_a2),
                "leading_tau_minus_1_over_36_times_Y": serialize_arb_certified(leading_e),
                "ratio_E_a2_over_Y": serialize_arb_certified(ratio_e_over_Y),
                "abs_difference_from_leading": serialize_arb_certified(abs_rem_e),
                "derived_pointwise_to_energy_remainder_bound": serialize_arb_certified(derived_e_rem_bnd),
                "derived_energy_remainder_margin": serialize_arb_certified(e_rem_margin),
                "derived_energy_remainder_bound_holds": rem_bnd_ok,
            })

        # 3. Certify S = {3, 5, 7} multi-prime parity control and complete finite-S DCT/BCT leading asymptotic proof (`TASK-TC-056` §2):
        mean_357_frac = Fraction(2, 4) * Fraction(4, 6) * Fraction(6, 8)
        abs_conv_357_frac = Fraction(4, 2) * Fraction(6, 4) * Fraction(8, 6)  # prod_{p in S} (p + 1) / (p - 1) = 4
        lead_Q_357_frac = Fraction(1, 2) * mean_357_frac  # 1/8
        lead_E_357_arb = (tau_arb - arb(1)) / arb(64)
        zeta3_arb = arb(3).zeta()
        M_1_global_majorant = arb(1) / arb(2) + exact_C1_unimodal  # 1/2 + 2 * (3/(2e))^{3/2} = 1.31983256...
        M_1_exceeds_zeta3 = bool((M_1_global_majorant - zeta3_arb).lower() > 0)

        def _dirichlet_b_S_int(d_val: int, primes_S: Tuple[int, ...]) -> int:
            """Compute b_S(d) = (mu * a_S)(d) = sum_{e | d} mu(e) a_S(d / e)."""
            acc_b = 0
            e = 1
            while e * e <= d_val:
                if d_val % e == 0:
                    acc_b += moebius_mu_int(e) * finite_prime_parity_aS_int(d_val // e, primes_S=primes_S)
                    qe = d_val // e
                    if qe != e:
                        acc_b += moebius_mu_int(qe) * finite_prime_parity_aS_int(d_val // qe, primes_S=primes_S)
                e += 1
            return acc_b

        convolution_aS_checks_ok = True
        for test_S in ((2,), (3, 5, 7)):
            smooth_set_S = set(generate_P_smooth_up_to(test_S, 250))
            for n_test in range(1, 251):
                b_val = _dirichlet_b_S_int(n_test, test_S)
                if n_test not in smooth_set_S and b_val != 0:
                    convolution_aS_checks_ok = False
                # Check (1 * b_S)(n_test) == a_S(n_test)
                conv_sum = 0
                dv = 1
                while dv * dv <= n_test:
                    if n_test % dv == 0:
                        conv_sum += _dirichlet_b_S_int(dv, test_S)
                        qdv = n_test // dv
                        if qdv != dv:
                            conv_sum += _dirichlet_b_S_int(qdv, test_S)
                    dv += 1
                if conv_sum != finite_prime_parity_aS_int(n_test, primes_S=test_S):
                    convolution_aS_checks_ok = False
            for p_in_S in test_S:
                for k_exp in (1, 2, 3):
                    pk_val = p_in_S ** k_exp
                    if pk_val <= 250:
                        expected_b_pk = 2 * ((-1) ** k_exp)
                        if _dirichlet_b_S_int(pk_val, test_S) != expected_b_pk:
                            convolution_aS_checks_ok = False

        q_357_at_16 = evaluate_Q_aS_certified_arb(arb(16), primes_S=(3, 5, 7), T_cutoff=1200, prec_bits=prec_bits)
        q_357_at_64 = evaluate_Q_aS_certified_arb(arb(64), primes_S=(3, 5, 7), T_cutoff=2000, prec_bits=prec_bits)
        s357_control_ok = bool(
            mean_357_frac == Fraction(1, 4)
            and abs_conv_357_frac == Fraction(4, 1)
            and lead_Q_357_frac == Fraction(1, 8)
            and M_1_exceeds_zeta3
            and convolution_aS_checks_ok
            and q_357_at_16.lower() > 0
            and q_357_at_64.lower() > 0
        )

        return {
            "unimodal_and_second_order_euler_maclaurin_constants": {
                "exact_C1_unimodal_2_times_3_over_2e_pow_3_2": serialize_arb_certified(exact_C1_unimodal),
                "equivalent_1_over_sqrt2_times_3_over_e_pow_3_2": serialize_arb_certified(alt_C1_unimodal),
                "strict_upper_3_over_e_pow_3_2": serialize_arb_certified(three_over_e_pow_3_2),
                "unimodal_constant_repair_certified": unimodal_constant_repair_ok,
                "first_order_unimodal_supported_bounds": {
                    "Q_a2_from_unimodal_only": "Q_{a_2}(X) = (1 / 6) sqrt(X) + O(X^{-1/2} log X)",
                    "E_a2_from_unimodal_only": "E_{a_2}(Y) = ((tau - 1) / 36) Y + O(log Y)",
                },
                "second_order_euler_maclaurin_recovery": {
                    "exact_dyadic_identity": "Q_{a_2}(X) = Q_1(X) + 2 sum_{k >= 1} (-1)^k 2^{-k/2} Q_1(X / 2^k)",
                    "Q_1_second_order_bound": "|Q_1(w) - sqrt(w)/2| <= (w^{5/2}/12) int_0^infty |h_w''(t)| dt <= 3 w^{-3/2}  (forall w > 0)",
                    "dyadic_split_cutoff": "L = floor(log_2 X) >= 0 for all X >= 1 (including L = 0 on 1 <= X < 2, where sum_{k=1}^L is empty = 0)",
                    "k_eq_0_error": "|Q_1(X) - sqrt(X)/2| <= 3 X^{-3/2} <= 3 X^{-1/2}  (X >= 1)",
                    "large_scale_sum_1_le_k_le_L": "2 sum_{k=1}^L 2^{-k/2} * 3 (X/2^k)^{-3/2} = 6 X^{-3/2} sum_{k=1}^L 2^k = 6 X^{-3/2} (2^{L+1} - 2) <= 12 X^{-1/2}",
                    "omitted_main_term_tail_k_gt_L": "2 sum_{k > L} 2^{-k/2} (1/2) sqrt(X/2^k) = sqrt(X) 2^{-L} <= 2 X^{-1/2}",
                    "small_scale_tail_k_gt_L": "2 zeta(3) X^{5/2} sum_{k > L} 8^{-k} = (2 zeta(3) / 7) X^{5/2} 8^{-L} <= (16 zeta(3) / 7) X^{-1/2}",
                    "component_constants": {
                        "c_k0": "3",
                        "c_large_scale_1_le_k_le_L": "12",
                        "c_omitted_main_tail_k_gt_L": "2",
                        "c_small_scale_tail_k_gt_L_formula": "(16 / 7) * zeta(3)",
                        "c_small_scale_tail_k_gt_L": serialize_arb_certified(c_small_scale_tail),
                    },
                    "explicit_C_a2_formula": "17 + (16 / 7) * zeta(3)",
                    "explicit_C_a2_constant": serialize_arb_certified(C_a2_second_order),
                    "audit_note_on_retired_14_84231228_derivation": (
                        "The prior TC-055R derivation obtained 3 + 7*sqrt(2) + (8*sqrt(2)/7)*zeta(3) = 14.8423122796888... "
                        "by erroneously substituting sqrt(2) for the coefficient 2 in Q_{a_2}(X) = Q_1(X) + 2 sum_{k>=1} (-1)^k 2^{-k/2} Q_1(X/2^k). "
                        "The audit invalidates that derivation and replaces it with the proved constant C_{a_2} = 17 + (16/7)*zeta(3) = 19.74755863579336...; "
                        "it does not establish that the smaller numerical bound is false."
                    ),
                    "derived_energy_remainder_formula": (
                        "For Y >= 1, writing Q_{a_2}(X) = sqrt(X)/6 + rho_2(X) with |rho_2(X)| <= C_{a_2} X^{-1/2} gives "
                        "| |Q_{a_2}(X)|^2 - X/36 | <= (C_{a_2}/3) + C_{a_2}^2 X^{-1}, hence "
                        "|E_{a_2}(Y) - ((tau - 1)/36) Y| <= (C_{a_2} log tau)/3 + C_{a_2}^2 (1 - tau^{-1}) Y^{-1} <= C_{E,a_2} = O(1)."
                    ),
                    "explicit_C_E_a2_uniform_O1_cap_for_Y_ge_1": serialize_arb_certified(C_E_a2_uniform_O1),
                    "recovered_sharp_bounds": "Q_{a_2}(X) = (1 / 6) sqrt(X) + O(X^{-1/2}) and E_{a_2}(Y) = ((tau - 1) / 36) Y + O(1)",
                },
            },
            "asymptotic_formulas": {
                "Q_a2_asymptotic": "Q_{a_2}(X) = (1 / 6) sqrt(X) + O(X^{-1/2}) ~ sqrt(X) / 6 (for X >= 1, with |Q_{a_2}(X) - sqrt(X)/6| <= C_{a_2} X^{-1/2})",
                "E_a2_asymptotic": "E_{a_2}(Y) := int_Y^{tau Y} |Q_{a_2}(X)|^2 dX/X = ((tau - 1) / 36) Y + O(1) ~ ((tau - 1) / 36) Y (for Y >= 1)",
                "general_finite_S_asymptotic": (
                    "For any finite prime set S and a_S(n) = (-1)^{sum_{p in S} v_p(n)}, writing a_S = 1 * b_S (b_S = mu * a_S, "
                    "supported on S(S) with b_S(1) = 1 and b_S(p^k) = 2 (-1)^k for p in S, k >= 1) gives "
                    "sum_{d in S(S)} |b_S(d)| / d = prod_{p in S} (p + 1)/(p - 1) =: A_S < infty and "
                    "sum_{d in S(S)} b_S(d) / d = prod_{p in S} (p - 1)/(p + 1) =: m_S. Because |Q_1(w)| / sqrt(w) <= zeta(3) w^2 <= zeta(3) "
                    "on (0, 1] and |Q_1(w)| / sqrt(w) <= 1/2 + C_{1,uni} w^{-1} <= 1/2 + C_{1,uni} =: M_1 on [1, infty) with zeta(3) < M_1, "
                    "sup_{w > 0} |Q_1(w)| / sqrt(w) <= M_1 < infty globally. Dominated Convergence on "
                    "Q_{a_S}(X) / sqrt(X) = sum_{d in S(S)} (b_S(d) / d) (Q_1(X / d) / sqrt(X / d)) proves Q_{a_S}(X) / sqrt(X) -> m_S / 2, "
                    "and Bounded Convergence on E_{a_S}(Y) / Y = int_1^tau |Q_{a_S}(Y u) / sqrt(Y u)|^2 du (dominated by A_S^2 M_1^2) proves "
                    "E_{a_S}(Y) / Y -> ((tau - 1) / 4) m_S^2 as Y -> infty "
                    "(quantitative O(X^{-1/2}) and O(1) error bounds are proved here for S = {2}; multi-prime O(X^{-1/2})/O(1) remainders are not claimed)."
                ),
                "finite_S_dominated_convergence_majorant": {
                    "b_S_formula": "b_S = mu * a_S supported on S(S), b_S(1) = 1, b_S(p^k) = 2 (-1)^k (p in S, k >= 1), b_S(p^k) = 0 (p not in S, k >= 1)",
                    "abs_dirichlet_norm_A_S_formula": "sum_{d in S(S)} |b_S(d)| / d = prod_{p in S} (1 + 2/(p - 1)) = prod_{p in S} (p + 1) / (p - 1) < infty",
                    "signed_dirichlet_mean_m_S_formula": "sum_{d in S(S)} b_S(d) / d = prod_{p in S} (1 - 2/(p + 1)) = prod_{p in S} (p - 1) / (p + 1)",
                    "M_1_global_supremum_formula": "M_1 := 1/2 + C_{1,uni} = 1/2 + 2 * (3 / (2 * e))^{3/2} > zeta(3)",
                    "M_1_global_supremum_majorant": serialize_arb_certified(M_1_global_majorant),
                    "zeta_3": serialize_arb_certified(zeta3_arb),
                    "M_1_strictly_exceeds_zeta_3": M_1_exceeds_zeta3,
                    "convolution_aS_eq_1_star_bS_verified_up_to_250": convolution_aS_checks_ok,
                    "S_3_5_7_abs_norm_A_S": str(abs_conv_357_frac),
                },
                "one_sixth": serialize_arb_certified(one_sixth),
                "tau_minus_1_over_36": serialize_arb_certified(tau_minus_1_over_36),
                "control_S_3_5_7": {
                    "primes_S": [3, 5, 7],
                    "euler_factor_mean_prod_p_minus_1_over_p_plus_1": str(mean_357_frac),
                    "leading_Q_aS_over_sqrt_X_coefficient": str(lead_Q_357_frac),
                    "leading_Q_aS_asymptotic_statement": "Q_{a_{3,5,7}}(X) ~ sqrt(X) / 8",
                    "leading_E_aS_over_Y_coefficient_formula": "(tau - 1) / 64",
                    "leading_E_aS_asymptotic_statement": "E_{a_{3,5,7}}(Y) ~ ((tau - 1) / 64) Y",
                    "remainder_scope_note": (
                        "Preserves mean 1/4 and leading asymptotics Q_{a_S}(X) ~ sqrt(X)/8, E_{a_S}(Y) ~ ((tau - 1)/64) Y; "
                        "does NOT claim unproved multi-prime O(X^{-1/2}) or O(1) error terms."
                    ),
                    "leading_E_aS_over_Y_coefficient": serialize_arb_certified(lead_E_357_arb),
                    "Q_a_357_at_16": serialize_arb_certified(q_357_at_16),
                    "ratio_Q_a_357_over_sqrt_16": serialize_arb_certified(q_357_at_16 / arb(4)),
                    "Q_a_357_at_64": serialize_arb_certified(q_357_at_64),
                    "ratio_Q_a_357_over_sqrt_64": serialize_arb_certified(q_357_at_64 / arb(8)),
                    "s357_control_certified": s357_control_ok,
                },
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
                    "property": "Square-divisor Möbius convolution a(n) = sum_{d^2 | n} mu(n / d^2) and D_a(1) = 0 (vs simple pole at s = 1)",
                    "liouville_lambda": True,
                    "control_a2": False,
                    "control_aS_finite": False,
                },
            ],
            "Q_a2_rows": q_a2_rows,
            "all_q1_bounds_and_dyadic_identities_hold": all_q1_bounds_and_dyadic_identities_hold,
            "E_a2_rows": e_a2_rows,
            "all_e_a2_positive": all_e_a2_positive,
            "all_e_a2_remainder_bounds_hold": all_e_a2_remainder_bounds_hold,
            "scope_note": (
                "Because a_2(n) = (-1)^{v_2(n)} (and any finite-prime parity control a_S) satisfies complete multiplicativity, "
                "common-factor cancellation, transition Poisson summation, and finite-prime exclusion for P subset S, yet has "
                "Q_{a_2}(X) ~ sqrt(X)/6 and E_{a_2}(Y) ~ ((tau - 1)/36) Y (linear growth in Y), any cancellation argument that "
                "uses only hypotheses shared by a_2 or a_S cannot establish E_lambda(Y) = o(Y) or E_lambda(Y) <<_eps Y^eps. "
                "This is a control diagnostic exposing unsupported inferences, NOT a counterexample to the complete TC framework "
                "(since a_2 and a_S fail a(p) = -1 at primes outside S and fail sum_{d^2|n} mu(n/d^2) = a(n))."
            ),
        }
    finally:
        flint_ctx.prec = saved_prec


def evaluate_Q_lambda_finite_T_certified_arb(
    X_val: Union[arb, int, float, str, Fraction],
    T_int: int,
    prec_bits: int = 256,
) -> arb:
    """Evaluate the exact finite truncated sum
        Q_{lambda,T}(X) := X^{5/2} sum_{1 <= n <= T} lambda(n) n^{-3} exp(-X^2 / n^2)
    for integer T >= 1 in 256-bit Arb (no infinite-tail inflation).
    """
    if T_int < 0:
        raise ValueError(f"T_int must be >= 0, got {T_int}")
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X = arb(X_val.numerator) / arb(X_val.denominator) if isinstance(X_val, Fraction) else arb(X_val)
        if T_int == 0:
            return arb(0)
        X_sq = X * X
        X_5_2 = X_sq * X.sqrt()
        acc = arb(0)
        for n in range(1, T_int + 1):
            lam_n = liouville_lambda_int(n)
            n_arb = arb(n)
            acc += arb(lam_n) * (-X_sq / (n_arb * n_arb)).exp() / (n_arb ** 3)
        return X_5_2 * acc
    finally:
        flint_ctx.prec = saved_prec


def evaluate_Q_lambda_P_finite_L_certified_arb(
    X_val: Union[arb, int, float, str, Fraction],
    primes_P: Tuple[int, ...],
    L_int: int,
    prec_bits: int = 256,
) -> arb:
    """Evaluate the exact finite P-coprime truncated sum
        Q_{lambda,P,L}(X) := X^{5/2} sum_{1 <= r <= L, gcd(r, N_P) = 1} lambda(r) r^{-3} exp(-X^2 / r^2)
    for integer L >= 0 in 256-bit Arb.
    """
    if L_int < 0:
        raise ValueError(f"L_int must be >= 0, got {L_int}")
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        X = arb(X_val.numerator) / arb(X_val.denominator) if isinstance(X_val, Fraction) else arb(X_val)
        if L_int == 0:
            return arb(0)
        N_P = 1
        for p in set(primes_P):
            N_P *= p
        X_sq = X * X
        X_5_2 = X_sq * X.sqrt()
        acc = arb(0)
        for r in range(1, L_int + 1):
            if math.gcd(r, N_P) != 1:
                continue
            lam_r = liouville_lambda_int(r)
            r_arb = arb(r)
            acc += arb(lam_r) * (-X_sq / (r_arb * r_arb)).exp() / (r_arb ** 3)
        return X_5_2 * acc
    finally:
        flint_ctx.prec = saved_prec


def evaluate_Q_lambda_S_P_smooth_finite_L_certified_arb(
    w_val: Union[arb, int, float, str, Fraction],
    primes_P: Tuple[int, ...],
    L_int: int,
    prec_bits: int = 256,
) -> arb:
    """Evaluate the explicit P-smooth finite observable (`TASK-TC-055R2` §2):
        Q_{lambda,S(P),L}(w) := w^{5/2} sum_{m <= L, m in S(P)} lambda(m) m^{-3} exp(-w^2 / m^2)
    for w > 0 and nonnegative integer L >= 0 in 256-bit Arb.
    """
    if L_int < 0:
        raise ValueError(f"L_int must be >= 0, got {L_int}")
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        w = arb(w_val.numerator) / arb(w_val.denominator) if isinstance(w_val, Fraction) else arb(w_val)
        if not bool(w.lower() > 0):
            raise ValueError(f"w_val must be > 0, got {w_val}")
        if L_int == 0:
            return arb(0)
        smooth_m = generate_P_smooth_up_to(primes_P, L_int)
        if not smooth_m:
            return arb(0)
        w_sq = w * w
        w_5_2 = w_sq * w.sqrt()
        acc = arb(0)
        for m in smooth_m:
            lam_m = liouville_lambda_int(m)
            m_arb = arb(m)
            acc += arb(lam_m) * (-w_sq / (m_arb * m_arb)).exp() / (m_arb ** 3)
        return w_5_2 * acc
    finally:
        flint_ctx.prec = saved_prec


def evaluate_weighted_cofactor_energy_independent_fibers_arb(
    Y_val: Union[arb, int, float, str, Fraction],
    T_int: int,
    primes_P: Tuple[int, ...],
    prec_bits: int = 256,
) -> Dict[str, arb]:
    """Genuinely independent evaluation of the weighted cofactor energy decomposition (`TASK-TC-055R2` §2)
    directly from the smooth-fiber observables `Q_{lambda,S(P),floor(T/r)}(X/r)` integrated over `[Y, tau Y]`
    via `acb.integral` (Gauss-Legendre complex-ellipse ball quadrature), WITHOUT using `K_Y(m, n)`:
      - `E_same_r_weighted`:
            sum_{1 <= r <= T, gcd(r, N_P)=1} (1 / r) int_Y^{tau Y} |Q_{lambda,S(P),floor(T/r)}(X/r)|^2 dX/X,
      - `E_diff_r_weighted_ordered`:
            sum_{r != s, 1 <= r, s <= T, gcd(r s, N_P)=1} (lambda(r) lambda(s) / sqrt(r s))
                int_Y^{tau Y} Q_{lambda,S(P),floor(T/r)}(X/r) Q_{lambda,S(P),floor(T/s)}(X/s) dX/X,
      - `E_diff_r_weighted_unordered_times_2`:
            2 * sum_{1 <= r < s <= T, gcd(r s, N_P)=1} (lambda(r) lambda(s) / sqrt(r s))
                int_Y^{tau Y} Q_{lambda,S(P),floor(T/r)}(X/r) Q_{lambda,S(P),floor(T/s)}(X/s) dX/X,
      - `E_same_r_unweighted_erroneous`:
            sum_{1 <= r <= T, gcd(r, N_P)=1} int_Y^{tau Y} |Q_{lambda,S(P),floor(T/r)}(X/r)|^2 dX/X  (missing 1/r),
      - `E_diff_r_unweighted_erroneous`:
            sum_{r != s, 1 <= r, s <= T, gcd(r s, N_P)=1} lambda(r) lambda(s)
                int_Y^{tau Y} Q_{lambda,S(P),floor(T/r)}(X/r) Q_{lambda,S(P),floor(T/s)}(X/s) dX/X  (missing 1/sqrt(r s)).
    Note: On real `X in [Y, tau Y] subset (0, infty)`, `Q_{lambda,S(P),L}(X/r)` is real-valued, so
    `|Q_{lambda,S(P),L}(X/r)|^2 = (Q_{lambda,S(P),L}(X/r))^2`, whose analytic continuation to `{Re(z) > 0}`
    is integrated directly by `acb.integral`.
    """
    if T_int < 0:
        raise ValueError(f"T_int must be >= 0, got {T_int}")
    saved_prec = flint_ctx.prec
    try:
        work_prec = max(prec_bits + 32, 288)
        flint_ctx.prec = work_prec
        tau_w = arb(2) * arb.pi()
        Y_w = arb(Y_val.numerator) / arb(Y_val.denominator) if isinstance(Y_val, Fraction) else arb(Y_val)
        if not bool(Y_w.lower() > 0):
            raise ValueError(f"Y_val must be > 0, got {Y_val}")
        if T_int == 0:
            flint_ctx.prec = prec_bits
            z0 = arb(0)
            return {
                "E_same_r_weighted": z0,
                "E_diff_r_weighted_ordered": z0,
                "E_diff_r_weighted_unordered_times_2": z0,
                "E_total_weighted_fiber": z0,
                "E_same_r_unweighted_erroneous": z0,
                "E_diff_r_unweighted_erroneous": z0,
            }

        N_P = 1
        for p in set(primes_P):
            N_P *= p
        coprime_r_list = [r for r in range(1, T_int + 1) if math.gcd(r, N_P) == 1]
        smooth_terms_by_r: Dict[int, List[Tuple[acb, acb]]] = {}
        for r in coprime_r_list:
            L_r = T_int // r
            sm_list = generate_P_smooth_up_to(primes_P, L_r)
            terms_r: List[Tuple[acb, acb]] = []
            for m in sm_list:
                lam_m = liouville_lambda_int(m)
                m_acb = acb(m)
                terms_r.append((acb(lam_m) / (m_acb ** 3), m_acb * m_acb))
            smooth_terms_by_r[r] = terms_r

        def _eval_smooth_fiber_acb(z_complex: acb, r_val: int) -> acb:
            terms_r = smooth_terms_by_r[r_val]
            if not terms_r:
                return acb(0)
            w_c = z_complex / acb(r_val)
            w_sq = w_c * w_c
            w_5_2 = w_sq * w_c.sqrt()
            s_acc = acb(0)
            for coeff_m, m_sq in terms_r:
                s_acc += coeff_m * (-w_sq / m_sq).exp()
            return w_5_2 * s_acc

        a_end = acb(Y_w)
        b_end = acb(tau_w * Y_w)
        nan_acb = acb(arb("nan"), arb("nan"))

        same_integrals: Dict[int, arb] = {}
        for r in coprime_r_list:
            def _same_integrand(z_c: acb, analytic: bool, r_fix: int = r) -> acb:
                if analytic and not bool(z_c.real.lower() > 0):
                    return nan_acb
                qr = _eval_smooth_fiber_acb(z_c, r_fix)
                return (qr * qr) / z_c

            same_integrals[r] = acb.integral(_same_integrand, a_end, b_end).real

        pair_integrals: Dict[Tuple[int, int], arb] = {}
        for idx_i, r in enumerate(coprime_r_list):
            for s in coprime_r_list[idx_i + 1:]:
                def _cross_integrand(
                    z_c: acb, analytic: bool, r_fix: int = r, s_fix: int = s
                ) -> acb:
                    if analytic and not bool(z_c.real.lower() > 0):
                        return nan_acb
                    qr = _eval_smooth_fiber_acb(z_c, r_fix)
                    qs = _eval_smooth_fiber_acb(z_c, s_fix)
                    return (qr * qs) / z_c

                val_rs = acb.integral(_cross_integrand, a_end, b_end).real
                pair_integrals[(r, s)] = val_rs
                pair_integrals[(s, r)] = val_rs

        e_same_weighted = arb(0)
        e_same_unweighted_bug = arb(0)
        for r in coprime_r_list:
            e_same_weighted += same_integrals[r] / arb(r)
            e_same_unweighted_bug += same_integrals[r]

        e_diff_weighted_ordered = arb(0)
        e_diff_unweighted_bug = arb(0)
        for r in coprime_r_list:
            lam_r = liouville_lambda_int(r)
            for s in coprime_r_list:
                if r == s:
                    continue
                lam_s = liouville_lambda_int(s)
                sign_rs = arb(lam_r * lam_s)
                int_rs = pair_integrals[(r, s)]
                e_diff_weighted_ordered += sign_rs * int_rs / arb(r * s).sqrt()
                e_diff_unweighted_bug += sign_rs * int_rs

        e_diff_weighted_unordered_2x = arb(0)
        for idx_i, r in enumerate(coprime_r_list):
            lam_r = liouville_lambda_int(r)
            for s in coprime_r_list[idx_i + 1:]:
                lam_s = liouville_lambda_int(s)
                e_diff_weighted_unordered_2x += (
                    arb(2 * lam_r * lam_s) * pair_integrals[(r, s)] / arb(r * s).sqrt()
                )

        flint_ctx.prec = prec_bits
        return {
            "E_same_r_weighted": arb(e_same_weighted),
            "E_diff_r_weighted_ordered": arb(e_diff_weighted_ordered),
            "E_diff_r_weighted_unordered_times_2": arb(e_diff_weighted_unordered_2x),
            "E_total_weighted_fiber": arb(e_same_weighted + e_diff_weighted_ordered),
            "E_same_r_unweighted_erroneous": arb(e_same_unweighted_bug),
            "E_diff_r_unweighted_erroneous": arb(e_diff_unweighted_bug),
        }
    finally:
        flint_ctx.prec = saved_prec


def verify_tc055r_finite_truncation_and_signed_energy_attempt(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Execute TASK-TC-055R Section 6 & TASK-TC-055R2 Sections 2, 3, 5, and 8:
    1. Exact finite smooth-cofactor and coprime-cofactor reconstructions for T >= 0 and arbitrary finite P:
           Q_{lambda,T}(X) = sum_{m in S(P), m <= T} (lambda(m) / sqrt(m)) Q_{lambda,P,floor(T/m)}(X / m)
                           = sum_{1 <= r <= T, gcd(r, N_P)=1} F_r(X),
           F_r(X) := (lambda(r) / sqrt(r)) Q_{lambda,S(P),floor(T/r)}(X / r)
       (derived from X^{5/2} (m r)^{-3} = r^{-1/2} (X/r)^{5/2} m^{-3}), together with the exact excess sum
       over floor(T/m) < r <= T (gcd(r, N_P)=1) when r <= T replaces r <= floor(T/m) — covering empty P,
       T = 0, T = 1, (P = {2}, T = 2) where the excess vanishes, certified nonzero Gaussian excess examples
       ((P = {2}, T = 3), (24, {2,3}), (36, {2,3,5}), (50, {2,3,5,7})), and an explicit sign-cancellation
       witness at (T = 5, P = {2}, w = 1) where the excess index set has 4 pairs yet the excess sum is 0.
    2. Finite-truncation grade-interval tail energy bound for Y >= 1 and exact T(Y) = ceil(Y^{5/4}):
           R_tail(Y, T) := int_Y^{tau Y} |Q_lambda(X) - Q_{lambda,T}(X)|^2 dX/X <= (tau^5 - 1) Y^5 / (20 T^4),
       uniformly bounded by (tau^5 - 1) / 20 = 489.5814956564503252... = O(1) at T(Y) = ceil(Y^{5/4})
       (using exact integer-power predicate (T - 1)^4 < Y^5 <= T^4, including Y = 1, T(1) = 1), together with
       both directions of the squared L^2 transfer:
           E_lambda(Y) <= 2 E_{lambda,T(Y)}(Y) + 2 R_tail(Y, T(Y)),
           E_{lambda,T(Y)}(Y) <= 2 E_lambda(Y) + 2 R_tail(Y, T(Y)).
    3. Repaired weighted cofactor energy decomposition (with 1/r and lambda(r)lambda(s)/sqrt(r s)) and
       genuinely independent smooth-fiber quadrature check (`TASK-TC-055R2` §2):
           E_{same-r}(Y; T, P) = sum_{1 <= r <= T, gcd(r, N_P)=1} (1 / r)
               int_Y^{tau Y} |Q_{lambda,S(P),floor(T/r)}(X / r)|^2 dX/X >= 0,
           E_{diff-r}(Y; T, P) = sum_{r != s, 1 <= r, s <= T, gcd(r s, N_P)=1} (lambda(r) lambda(s) / sqrt(r s))
               int_Y^{tau Y} Q_{lambda,S(P),floor(T/r)}(X / r) Q_{lambda,S(P),floor(T/s)}(X / s) dX/X
             = 2 sum_{1 <= r < s <= T, gcd(r s, N_P)=1} (lambda(r) lambda(s) / sqrt(r s))
               int_Y^{tau Y} Q_{lambda,S(P),floor(T/r)}(X / r) Q_{lambda,S(P),floor(T/s)}(X / s) dX/X
       (observables are real; cross sum uses ordered pairs r != s, whereas unordered pairs r < s carry factor 2),
       with E_{lambda,T}(Y) = E_{same-r} + E_{diff-r}, verified by independent `acb.integral` smooth-fiber
       integration and regression at (Y = 4, T = 6, P = {2, 3}):
         - Correct weighted E_{same-r} = 0.0487892768943856650468243231271522938...
         - Erroneous unweighted sum    = 0.1209268815654658371618758542627537259...
    """
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau_arb = arb(2) * arb.pi()
        uniform_tail_cap = (tau_arb ** 5 - arb(1)) / arb(20)

        # 1. Verify exact finite reconstructions (both m-outer and r-outer) and exact uncoupled excess sum
        #    across degenerate zero-excess cases AND certified nonzero-excess cases:
        finite_reconstruction_rows: List[Dict[str, Any]] = []
        all_finite_reconstructions_match = True
        test_recon_cases = [
            (0, (2, 3), 4, False),
            (1, (2, 3), 4, False),
            (6, (), 4, False),
            (2, (2,), 4, False),
            (3, (2,), 4, True),
            (24, (2, 3), 4, True),
            (36, (2, 3, 5), 6, True),
            (50, (2, 3, 5, 7), 8, True),
        ]
        for T_int, primes_P, X_int, expect_nonzero_excess in test_recon_cases:
            X_arb = arb(X_int)
            q_T_direct = evaluate_Q_lambda_finite_T_certified_arb(X_arb, T_int=T_int, prec_bits=prec_bits)
            smooth_m_list = generate_P_smooth_up_to(primes_P, T_int)
            N_P = 1
            for p in primes_P:
                N_P *= p

            recon_exact_by_m = arb(0)
            recon_common_L_eq_T = arb(0)
            boundary_correction = arb(0)
            excess_pair_count = 0
            X_sq = X_arb * X_arb
            X_5_2 = X_sq * X_arb.sqrt()
            for m in smooth_m_list:
                lam_m = liouville_lambda_int(m)
                m_arb = arb(m)
                L_m = T_int // m
                q_inner_Lm = evaluate_Q_lambda_P_finite_L_certified_arb(
                    X_arb / m_arb, primes_P=primes_P, L_int=L_m, prec_bits=prec_bits
                )
                q_inner_T = evaluate_Q_lambda_P_finite_L_certified_arb(
                    X_arb / m_arb, primes_P=primes_P, L_int=T_int, prec_bits=prec_bits
                )
                recon_exact_by_m += arb(lam_m) * q_inner_Lm / m_arb.sqrt()
                recon_common_L_eq_T += arb(lam_m) * q_inner_T / m_arb.sqrt()
                for r in range(L_m + 1, T_int + 1):
                    if math.gcd(r, N_P) != 1:
                        continue
                    excess_pair_count += 1
                    mr = m * r
                    mr_arb = arb(mr)
                    boundary_correction += (
                        arb(lam_m * liouville_lambda_int(r))
                        * X_5_2
                        * (-X_sq / (mr_arb * mr_arb)).exp()
                        / (mr_arb ** 3)
                    )

            # Also verify the r-regrouped weighted cofactor representation:
            # Q_{lambda,T}(X) = sum_{1 <= r <= T, gcd(r, N_P)=1} (lambda(r)/sqrt(r)) Q_{lambda,S(P),floor(T/r)}(X/r)
            recon_exact_by_r = arb(0)
            ptwise_same_r_weighted = arb(0)
            ptwise_diff_r_weighted = arb(0)
            coprime_r_list = [r for r in range(1, T_int + 1) if math.gcd(r, N_P) == 1]
            q_smooth_by_r: Dict[int, arb] = {}
            for r in coprime_r_list:
                lam_r = liouville_lambda_int(r)
                r_arb = arb(r)
                q_sm_r = evaluate_Q_lambda_S_P_smooth_finite_L_certified_arb(
                    X_arb / r_arb, primes_P=primes_P, L_int=(T_int // r), prec_bits=prec_bits
                )
                q_smooth_by_r[r] = q_sm_r
                recon_exact_by_r += arb(lam_r) * q_sm_r / r_arb.sqrt()
                ptwise_same_r_weighted += (q_sm_r * q_sm_r) / r_arb
            for r in coprime_r_list:
                lam_r = liouville_lambda_int(r)
                for s in coprime_r_list:
                    if r == s:
                        continue
                    lam_s = liouville_lambda_int(s)
                    ptwise_diff_r_weighted += (
                        arb(lam_r * lam_s)
                        * q_smooth_by_r[r]
                        * q_smooth_by_r[s]
                        / arb(r * s).sqrt()
                    )

            diff_exact_m = q_T_direct - recon_exact_by_m
            diff_exact_r = q_T_direct - recon_exact_by_r
            diff_ptwise_sq = (q_T_direct * q_T_direct) - (ptwise_same_r_weighted + ptwise_diff_r_weighted)
            common_minus_exact = recon_common_L_eq_T - q_T_direct
            diff_boundary_check = common_minus_exact - boundary_correction
            if expect_nonzero_excess:
                excess_regime_ok = bool(excess_pair_count > 0 and abs(common_minus_exact).lower() > 0)
            else:
                excess_regime_ok = bool(excess_pair_count == 0 and common_minus_exact.contains(0))

            row_ok = bool(
                diff_exact_m.contains(0)
                and diff_exact_r.contains(0)
                and diff_ptwise_sq.contains(0)
                and diff_boundary_check.contains(0)
                and excess_regime_ok
            )
            if not row_ok:
                all_finite_reconstructions_match = False
            finite_reconstruction_rows.append({
                "T": T_int,
                "primes_P": list(primes_P),
                "X": X_int,
                "excess_index_pair_count": excess_pair_count,
                "expected_nonzero_excess": expect_nonzero_excess,
                "verification_classification": (
                    "numerical_enclosure_consistency_check_exact_equality_proved_in_lean"
                ),
                "Q_lambda_T_direct": serialize_arb_certified(q_T_direct),
                "Q_lambda_T_m_dependent_inner_cutoff_floor_T_over_m": serialize_arb_certified(recon_exact_by_m),
                "Q_lambda_T_r_regrouped_weighted_cofactor_sum": serialize_arb_certified(recon_exact_by_r),
                "direct_minus_m_dependent_difference": serialize_arb_certified(diff_exact_m),
                "direct_minus_r_regrouped_difference": serialize_arb_certified(diff_exact_r),
                "pointwise_sq_minus_weighted_same_plus_diff_r": serialize_arb_certified(diff_ptwise_sq),
                "common_cutoff_L_eq_T_sum": serialize_arb_certified(recon_common_L_eq_T),
                "common_cutoff_minus_exact_discrepancy": serialize_arb_certified(common_minus_exact),
                "explicit_hyperbolic_boundary_sum_T_lt_mr_le_mT": serialize_arb_certified(boundary_correction),
                "discrepancy_minus_boundary_sum": serialize_arb_certified(diff_boundary_check),
                "exact_identity_and_excess_regime_verified": row_ok,
                "exact_identity_and_nonzero_common_cutoff_error_verified": bool(
                    row_ok and (abs(common_minus_exact).lower() > 0 if expect_nonzero_excess else True)
                ),
            })

        # Explicit integer cancellation witness for uncoupled excess:
        # At T = 5, P = {2}, S({2}) cap [1, 5] = {1, 2, 4}; excess pairs (m, r) with floor(5/m) < r <= 5, gcd(r, 2) = 1
        # are (2, 3), (2, 5), (4, 3), (4, 5) -> products 6, 10, 12, 20 with lambda = +1, +1, -1, -1.
        # For constant weight w(n) = 1, the uncoupled excess sum is +1 + 1 - 1 - 1 = 0 despite 4 excess pairs!
        cancel_T = 5
        cancel_P = (2,)
        cancel_pairs = []
        cancel_excess_sum_unit_weight = 0
        for m_c in generate_P_smooth_up_to(cancel_P, cancel_T):
            for r_c in range((cancel_T // m_c) + 1, cancel_T + 1):
                if r_c % 2 == 1:
                    term_sign = liouville_lambda_int(m_c) * liouville_lambda_int(r_c)
                    cancel_pairs.append({"m": m_c, "r": r_c, "mr": m_c * r_c, "lambda_mr": term_sign})
                    cancel_excess_sum_unit_weight += term_sign
        cancellation_witness_ok = bool(len(cancel_pairs) == 4 and cancel_excess_sum_unit_weight == 0)

        # 2. Certify finite truncation tail energy bound int_Y^{tau Y} |Q_lambda(X) - Q_{lambda,T}(X)|^2 dX/X <= (tau^5 - 1) Y^5 / (20 T^4)
        #    for Y in {1, 2, 4, 8} at exact T(Y) = ceil(Y^{5/4}) (including T(1) = 1) and T = 2 * ceil(Y^{5/4}):
        tail_energy_rows: List[Dict[str, Any]] = []
        all_tail_energy_bounds_hold = True
        for Y_int in (1, 2, 4, 8):
            Y_arb = arb(Y_int)
            T_sched = exact_ceil_five_fourths_power(Y_int)
            for T_label, T_val in [("ceil(Y^{5/4})", T_sched), ("2*ceil(Y^{5/4})", 2 * T_sched)]:
                T_arb = arb(T_val)
                analytic_tail_bound = ((tau_arb ** 5 - arb(1)) * (Y_arb ** 5)) / (arb(20) * (T_arb ** 4))
                N_sub = 16
                dx = (tau_arb * Y_arb - Y_arb) / arb(N_sub)
                half_dx = dx / arb(2)
                actual_tail_int = arb(0)
                for j in range(N_sub):
                    mid_j = (Y_arb + arb(j) * dx + half_dx).mid()
                    x_ball = arb(mid_j, half_dx.upper())
                    q_full = evaluate_Q_arith_certified_arb(x_ball, "lambda", T_cutoff=600, prec_bits=prec_bits)["enclosure"]
                    q_T = evaluate_Q_lambda_finite_T_certified_arb(x_ball, T_int=T_val, prec_bits=prec_bits)
                    diff_q = q_full - q_T
                    actual_tail_int += (diff_q * diff_q / x_ball) * dx
                margin = analytic_tail_bound - actual_tail_int
                cap_minus_analytic = uniform_tail_cap * (arb(T_val ** 4 - Y_int ** 5) / arb(T_val ** 4))
                cap_ok = bool(Y_int ** 5 <= T_val ** 4) and bool(cap_minus_analytic.lower() >= 0)
                row_ok = bool(margin.lower() > 0) and cap_ok
                if not row_ok:
                    all_tail_energy_bounds_hold = False
                tail_energy_rows.append({
                    "Y": Y_int,
                    "T_schedule": T_label,
                    "T": T_val,
                    "exact_predicate_holds": bool(((T_sched - 1) ** 4) < (Y_int ** 5) <= (T_sched ** 4)),
                    "actual_tail_energy_integral": serialize_arb_certified(actual_tail_int),
                    "analytic_upper_bound_tau5_minus_1_Y5_over_20_T4": serialize_arb_certified(analytic_tail_bound),
                    "uniform_O1_cap_tau5_minus_1_over_20": serialize_arb_certified(uniform_tail_cap),
                    "bound_minus_actual_margin": serialize_arb_certified(margin),
                    "strict_bound_and_uniform_cap_hold": row_ok,
                })

        # 3. Substantive signed energy decomposition on E_{lambda,T(Y)}(Y) with prime cutoff P_u,
        #    cross-checked against genuinely independent `acb.integral` weighted-fiber evaluations:
        signed_attempt_rows: List[Dict[str, Any]] = []
        all_signed_decompositions_consistent = True
        y4_t6_p23_regression: Dict[str, Any] = {}
        for Y_int, expected_T_int, primes_u in [
            (4, 6, (2, 3)),
            (8, 14, (2, 3, 5)),
            (12, 23, (2, 3, 5, 7)),
        ]:
            T_int = exact_ceil_five_fourths_power(Y_int)
            assert T_int == expected_T_int
            Y_arb = arb(Y_int)
            N_u = 1
            for p in primes_u:
                N_u *= p

            # (A) Original kernel-matrix grouping K_Y(a, b) for 1 <= a, b <= T_int:
            K_mat: Dict[Tuple[int, int], arb] = {}
            for a in range(1, T_int + 1):
                for b in range(a, T_int + 1):
                    kv = evaluate_energy_kernel_K_Y_certified_arb(Y_arb, a, b, prec_bits=prec_bits)
                    K_mat[(a, b)] = kv
                    K_mat[(b, a)] = kv

            smooth_part: Dict[int, int] = {}
            coprime_part: Dict[int, int] = {}
            for n in range(1, T_int + 1):
                m_c = 1
                r_c = n
                for p in primes_u:
                    while r_c % p == 0:
                        m_c *= p
                        r_c //= p
                smooth_part[n] = m_c
                coprime_part[n] = r_c

            E_signed_T = arb(0)
            E_unsigned_T = arb(0)
            D_diag_T = arb(0)
            E_same_r = arb(0)
            E_diff_r = arb(0)
            E_smooth_diag = arb(0)
            E_smooth_cross = arb(0)

            for a in range(1, T_int + 1):
                lam_a = liouville_lambda_int(a)
                D_diag_T += K_mat[(a, a)]
                for b in range(1, T_int + 1):
                    lam_b = liouville_lambda_int(b)
                    term_unsigned = K_mat[(a, b)]
                    term_signed = arb(lam_a * lam_b) * term_unsigned
                    E_unsigned_T += term_unsigned
                    E_signed_T += term_signed
                    if coprime_part[a] == coprime_part[b]:
                        E_same_r += term_signed
                    else:
                        E_diff_r += term_signed
                    if smooth_part[a] == smooth_part[b]:
                        E_smooth_diag += term_signed
                    else:
                        E_smooth_cross += term_signed

            # (B) Genuinely independent smooth-fiber quadrature evaluation (without K_mat):
            fiber_eval = evaluate_weighted_cofactor_energy_independent_fibers_arb(
                Y_arb, T_int=T_int, primes_P=primes_u, prec_bits=prec_bits
            )
            fiber_same_diff = E_same_r - fiber_eval["E_same_r_weighted"]
            fiber_diff_ordered_diff = E_diff_r - fiber_eval["E_diff_r_weighted_ordered"]
            fiber_ordered_vs_unordered_diff = (
                fiber_eval["E_diff_r_weighted_ordered"]
                - fiber_eval["E_diff_r_weighted_unordered_times_2"]
            )
            fiber_total_diff = E_signed_T - fiber_eval["E_total_weighted_fiber"]
            unweighted_same_bug_margin = fiber_eval["E_same_r_unweighted_erroneous"] - E_same_r

            decomp_r_diff = E_signed_T - (E_same_r + E_diff_r)
            decomp_m_diff = E_signed_T - (E_smooth_diag + E_smooth_cross)
            cancellation_ratio = E_signed_T / E_unsigned_T
            row_ok = bool(
                decomp_r_diff.contains(0)
                and decomp_m_diff.contains(0)
                and fiber_same_diff.contains(0)
                and fiber_diff_ordered_diff.contains(0)
                and fiber_ordered_vs_unordered_diff.contains(0)
                and fiber_total_diff.contains(0)
                and unweighted_same_bug_margin.lower() > 0
                and E_signed_T.lower() >= 0
                and E_same_r.lower() >= 0
                and (E_unsigned_T - E_signed_T).lower() > 0
            )
            if not row_ok:
                all_signed_decompositions_consistent = False

            if (Y_int, T_int, primes_u) == (4, 6, (2, 3)):
                y4_t6_p23_regression = {
                    "Y": 4,
                    "T": 6,
                    "primes_P": [2, 3],
                    "coprime_cofactors_r": [1, 5],
                    "weighted_E_same_r_kernel_grouping": serialize_arb_certified(E_same_r),
                    "weighted_E_same_r_independent_fiber_quadrature": serialize_arb_certified(
                        fiber_eval["E_same_r_weighted"]
                    ),
                    "kernel_minus_independent_fiber_consistency": serialize_arb_certified(fiber_same_diff),
                    "erroneous_unweighted_E_same_r_omitting_1_over_r": serialize_arb_certified(
                        fiber_eval["E_same_r_unweighted_erroneous"]
                    ),
                    "unweighted_minus_weighted_discrepancy": serialize_arb_certified(unweighted_same_bug_margin),
                    "weighted_E_diff_r_ordered_independent_fiber": serialize_arb_certified(
                        fiber_eval["E_diff_r_weighted_ordered"]
                    ),
                    "erroneous_unweighted_E_diff_r_omitting_1_over_sqrt_rs": serialize_arb_certified(
                        fiber_eval["E_diff_r_unweighted_erroneous"]
                    ),
                    "omitted_weight_strictly_detected": bool(
                        unweighted_same_bug_margin.lower() > 0
                        and abs(fiber_eval["E_diff_r_unweighted_erroneous"] - E_diff_r).lower() > 0
                    ),
                }

            signed_attempt_rows.append({
                "Y": Y_int,
                "T_eq_ceil_Y_5_4": T_int,
                "primes_u": list(primes_u),
                "comparison_classification": (
                    "kernel_partition_and_independent_fiber_quadrature_consistency_check"
                ),
                "E_signed_T_Y": serialize_arb_certified(E_signed_T),
                "E_unsigned_T_Y": serialize_arb_certified(E_unsigned_T),
                "diagonal_sum_D_T_Y": serialize_arb_certified(D_diag_T),
                "signed_to_unsigned_ratio": serialize_arb_certified(cancellation_ratio),
                "E_same_coprime_cofactor_r1_eq_r2": serialize_arb_certified(E_same_r),
                "E_same_r_independent_weighted_fiber_quadrature": serialize_arb_certified(
                    fiber_eval["E_same_r_weighted"]
                ),
                "E_same_r_erroneous_unweighted_fiber": serialize_arb_certified(
                    fiber_eval["E_same_r_unweighted_erroneous"]
                ),
                "E_same_r_kernel_minus_independent_fiber": serialize_arb_certified(fiber_same_diff),
                "E_diff_coprime_cofactor_r1_ne_r2": serialize_arb_certified(E_diff_r),
                "E_diff_r_independent_weighted_fiber_ordered": serialize_arb_certified(
                    fiber_eval["E_diff_r_weighted_ordered"]
                ),
                "E_diff_r_independent_weighted_fiber_unordered_times_2": serialize_arb_certified(
                    fiber_eval["E_diff_r_weighted_unordered_times_2"]
                ),
                "E_diff_r_kernel_minus_independent_fiber": serialize_arb_certified(
                    fiber_diff_ordered_diff
                ),
                "E_smooth_diagonal_m1_eq_m2": serialize_arb_certified(E_smooth_diag),
                "E_smooth_cross_m1_ne_m2": serialize_arb_certified(E_smooth_cross),
                "coprime_decomposition_zero_in_diff": bool(decomp_r_diff.contains(0)),
                "smooth_decomposition_zero_in_diff": bool(decomp_m_diff.contains(0)),
                "independent_weighted_fiber_consistency_holds": bool(
                    fiber_same_diff.contains(0)
                    and fiber_diff_ordered_diff.contains(0)
                    and fiber_ordered_vs_unordered_diff.contains(0)
                    and fiber_total_diff.contains(0)
                ),
                "strict_sign_cancellation_below_unsigned": row_ok,
            })

        # Certify fixed-P smooth-fiber sparsity constants (`TASK-TC-056` §2):
        # sup_{x > 0} x^{5/2 - eta} exp(-x^2) = ((5 - 2*eta) / (4 * e))^{(5 - 2*eta) / 4} for 0 <= eta < 5/2.
        e_arb = arb(1).exp()
        c_eta_0_sparsity = ((arb(5) / (arb(4) * e_arb)) ** (arb(5) / arb(4)))
        c_eta_quarter_sparsity = ((arb(9) / (arb(8) * e_arb)) ** (arb(9) / arb(8)))
        sparsity_constants_positive = bool(
            c_eta_0_sparsity.lower() > 0 and c_eta_quarter_sparsity.lower() > 0
        )

        return {
            "exact_finite_reconstruction_theorem": {
                "finite_prime_set_hypothesis": (
                    "Explicitly quantified over any finite set of primes P (`P : Finset Nat`, `forall p in P, p.Prime`, "
                    "including P = empty with N_empty = 1, S(empty) = {1}, and N_P = prod_{p in P} p)."
                ),
                "smooth_outer_formula": (
                    "For every integer T >= 0, finite set of primes P, and X > 0: "
                    "Q_{lambda,T}(X) = sum_{m in S(P), m <= T} (lambda(m) / sqrt(m)) Q_{lambda,P,floor(T/m)}(X / m)."
                ),
                "coprime_outer_weighted_cofactor_formula": (
                    "For every integer T >= 0, finite set of primes P, and X > 0: "
                    "Q_{lambda,T}(X) = sum_{1 <= r <= T, gcd(r, N_P)=1} F_r(X), where "
                    "F_r(X) = (lambda(r) / sqrt(r)) Q_{lambda,S(P),floor(T/r)}(X / r) and "
                    "Q_{lambda,S(P),L}(w) = w^{5/2} sum_{m <= L, m in S(P)} lambda(m) m^{-3} exp(-w^2 / m^2) "
                    "(derived from X^{5/2} (m r)^{-3} = r^{-1/2} (X / r)^{5/2} m^{-3})."
                ),
                "formula": (
                    "For every integer T >= 0, finite set of primes P, and X > 0: "
                    "Q_{lambda,T}(X) = sum_{m in S(P), m <= T} (lambda(m) / sqrt(m)) Q_{lambda,P,floor(T/m)}(X / m) "
                    "= sum_{1 <= r <= T, gcd(r, N_P)=1} (lambda(r) / sqrt(r)) Q_{lambda,S(P),floor(T/r)}(X / r)."
                ),
                "inner_cutoff_dependence_and_exact_excess_note": (
                    "Because 1 <= n = m r <= T with m in S(P) and gcd(r, N_P) = 1 is equivalent to 1 <= m <= T and "
                    "1 <= r <= floor(T / m) for any finite set of primes P, replacing r <= floor(T / m) by an uncoupled cutoff "
                    "r <= T adds the exact excess sum sum_{m in S(P), m <= T} sum_{floor(T/m) < r <= T, gcd(r, N_P)=1} lambda(m) lambda(r) w(m r) "
                    "(formalized in Lean 4 theorem finite_liouville_reindexed_sum_and_excess_cutoff_identity_nat). "
                    "This excess is NOT universally nonzero: it vanishes identically when P = empty, T <= 1, or "
                    "(P = {2}, T = 2), and can also vanish by sign cancellation (e.g. T = 5, P = {2}, w = 1); "
                    "at (P = {2}, T = 3) the excess equals w(6), which is nonzero whenever w(6) != 0, including the "
                    "strictly positive Gaussian case w(n) = phi_n(X) = X^{5/2} n^{-3} exp(-X^2 / n^2) > 0 (X > 0), and "
                    "for the Gaussian observable at (24, {2,3}), (36, {2,3,5}), (50, {2,3,5,7}) it is also certified strictly nonzero."
                ),
                "uncoupled_cutoff_cancellation_witness_T5_P2_unit_weight": {
                    "T": cancel_T,
                    "primes_P": list(cancel_P),
                    "weight": "w(n) = 1",
                    "excess_pairs": cancel_pairs,
                    "excess_sum_value": cancel_excess_sum_unit_weight,
                    "nonempty_excess_index_set_cancels_to_zero": cancellation_witness_ok,
                },
                "rows": finite_reconstruction_rows,
                "all_finite_reconstructions_match": bool(
                    all_finite_reconstructions_match and cancellation_witness_ok and sparsity_constants_positive
                ),
            },
            "finite_truncation_tail_energy_and_L2_transfer": {
                "pointwise_tail_bound": "|Q_lambda(X) - Q_{lambda,T}(X)| <= X^{5/2} / (2 T^2)  for all integer T >= 1 and X > 0",
                "grade_interval_tail_energy_bound": (
                    "R_tail(Y, T) := int_Y^{tau Y} |Q_lambda(X) - Q_{lambda,T}(X)|^2 dX/X <= (tau^5 - 1) Y^5 / (20 T^4)"
                ),
                "schedule_choice": (
                    "T(Y) := ceil(Y^{5/4}) >= Y^{5/4} (Y >= 1, resolved via exact predicate (T-1)^4 < Y^5 <= T^4 with T(1) = 1), "
                    "giving R_tail(Y, T(Y)) <= (tau^5 - 1) / 20 = 489.5814956564503252... = O(1)"
                ),
                "L2_transfer_inequalities": (
                    "E_lambda(Y) <= 2 E_{lambda,T(Y)}(Y) + 2 R_tail(Y, T(Y)) and "
                    "E_{lambda,T(Y)}(Y) <= 2 E_lambda(Y) + 2 R_tail(Y, T(Y)), so "
                    "(forall eps > 0, E_lambda(Y) <<_eps Y^eps) <-> (forall eps > 0, E_{lambda,T(Y)}(Y) <<_eps Y^eps)."
                ),
                "surviving_joint_energy_target": (
                    "For every eps > 0, there exists C_eps < infty such that for every Y >= 1, "
                    "0 <= E_{lambda,T(Y)}(Y) = sum_{1 <= m, n <= T(Y)} lambda(m) lambda(n) K_Y(m, n) "
                    "= E_{same-r}(Y; T(Y), P) + E_{diff-r}(Y; T(Y), P) <= C_eps Y^eps."
                ),
                "rows": tail_energy_rows,
                "all_tail_energy_bounds_hold": all_tail_energy_bounds_hold,
            },
            "signed_energy_attempt_on_finite_reconstruction": {
                "decomposition_formulas": {
                    "coprime_cofactor_split": (
                        "E_{lambda,T}(Y) = E_{same-r}(Y; T, P_u) + E_{diff-r}(Y; T, P_u) (observables real, Y >= 1), where "
                        "E_{same-r}(Y; T, P_u) = sum_{1 <= r <= T, gcd(r, N_u)=1} (1 / r) "
                        "int_Y^{tau Y} |Q_{lambda,S(P_u),floor(T/r)}(X / r)|^2 dX/X >= 0, and "
                        "E_{diff-r}(Y; T, P_u) = sum_{r != s, 1 <= r, s <= T, gcd(r s, N_u)=1} (lambda(r) lambda(s) / sqrt(r s)) "
                        "int_Y^{tau Y} Q_{lambda,S(P_u),floor(T/r)}(X / r) Q_{lambda,S(P_u),floor(T/s)}(X / s) dX/X "
                        "= 2 sum_{1 <= r < s <= T, gcd(r s, N_u)=1} (lambda(r) lambda(s) / sqrt(r s)) "
                        "int_Y^{tau Y} Q_{lambda,S(P_u),floor(T/r)}(X / r) Q_{lambda,S(P_u),floor(T/s)}(X / s) dX/X "
                        "(ordered pairs r != s carry weight lambda(r)lambda(s)/sqrt(rs); unordered pairs r < s carry factor 2)."
                    ),
                    "smooth_factor_split": "E_{lambda,T}(Y) = E_{smooth-diag}(Y; T, P_u) + E_{smooth-cross}(Y; T, P_u)",
                    "formal_vs_analytic_status": (
                        "Pointwise weighted cofactor decomposition |Q_{lambda,T}(X)|^2 = same-r + diff-r is formally proved "
                        "in Lean 4 theorem finite_gaussian_observable_reconstruction_and_weighted_cofactor_square; its "
                        "integrated identity on [Y, tau Y] follows analytically by finite linearity of the Riemann/Lebesgue integral."
                    ),
                },
                "weighted_cofactor_regression_Y4_T6_P_2_3": y4_t6_p23_regression,
                "proved_partial_saving_on_fixed_smooth_fibers": (
                    "For any fixed finite set of primes P, both contour shifting of D_{S(P)}(s) = prod_{p in P}(1 + p^{-s})^{-1} "
                    "and direct termwise sparsity give |Q_{lambda,S(P),L}(w)| <= Q_{1,S(P),L}(w) <= c_eta w^eta prod_{p in P}(1 - p^{-1/2 - eta})^{-1} "
                    "for every 0 <= eta < 5/2 (where c_eta = sup_{x > 0} x^{5/2 - eta} exp(-x^2) = ((5 - 2*eta)/(4*e))^{(5 - 2*eta)/4}, uniformly in L >= 0). "
                    "Because this exact O_{P,eta}(w^eta) power saving already holds for unsigned unit weights +1 from the sparsity of S(P) and "
                    "convergence of sum_{m in S(P)} m^{-1/2 - eta} = prod_{p in P}(1 - p^{-1/2 - eta})^{-1} < infty, fixed-P smooth-fiber decay "
                    "is a sparsity/absolute-convergence bound and NOT by itself a new signed cancellation theorem."
                ),
                "fixed_P_smooth_fiber_sparsity_constants": {
                    "c_eta_formula": "c_eta = ((5 - 2*eta) / (4 * e))^{(5 - 2*eta) / 4} for 0 <= eta < 5/2",
                    "c_0_sparsity_constant": serialize_arb_certified(c_eta_0_sparsity),
                    "c_quarter_sparsity_constant": serialize_arb_certified(c_eta_quarter_sparsity),
                    "unsigned_smooth_bound": (
                        "|Q_{lambda,S(P),L}(w)| <= Q_{1,S(P),L}(w) <= c_eta w^eta prod_{p in P} (1 - p^{-1/2 - eta})^{-1} "
                        "(holds for unsigned +1 weights solely by sparsity of S(P), uniformly in L >= 0)"
                    ),
                },
                "exact_two_part_obstruction_preventing_all_eps_closure": (
                    "When attempting to promote the fixed-u smooth-fiber bound to an unconditional bound E_{lambda,T(Y)}(Y) <<_eps Y^eps "
                    "by choosing u = u(Y) (while preserving the combined signed sum E_{same-r} + E_{diff-r}): "
                    "(1) If u >= T(Y) = ceil(Y^{5/4}) so that gcd(r, N_u) = 1 forces r = 1 and E_{diff-r} = 0, then on the contour "
                    "Re(1/2 + z) = eta in (0, 1/2) (or in the unsigned sparsity product at exponent eta in (0, 1)) the finite Euler product "
                    "has exact Kronecker supremum prod_{p <= u}(1 - p^{-eta})^{-1} = exp((1 + o_eta(1)) u^{1-eta} / ((1-eta) log u)), which grows "
                    "super-polynomially in Y, while finite truncation m <= T(Y) couples the Mellin integral to the Perron hyperbolic kernel (T/m)^w / w; "
                    "(2) Requiring prod_{p <= u}(1 - p^{-eta})^{-1} <= Y^eps for fixed 0 < eta < 1 means (u^{1-eta} / ((1-eta) log u))(1 + o_eta(1)) <= eps log Y: "
                    "here u(Y) << (log Y)^{1/(1-eta)} is a sufficient-only condition, whereas u(Y) = c * (log Y * log log Y)^{1/(1-eta)} satisfies "
                    "u(Y)^{1-eta} / ((1-eta) log u(Y)) = c^{1-eta} (1 + o_{eta,c}(1)) log Y and IS admissible whenever 0 < c < eps^{1/(1-eta)} (c^{1-eta} < eps), "
                    "making u(Y) = O_{eta,eps}((log Y * log log Y)^{1/(1-eta)}) (limsup <= eps^{1/(1-eta)}) the exact necessary polylogarithmic scale. "
                    "Even at that maximal admissible scale u(Y) = (log Y)^{O_eta(1)} << T(Y), almost all integers n <= T(Y) have large P_u-coprime cofactors r > u, "
                    "so the combined sum E_{same-r}(Y; T(Y), P_u) + E_{diff-r}(Y; T(Y), P_u) retains the unfactored primes p > u across distinct cofactors."
                ),
                "rows": signed_attempt_rows,
                "all_signed_decompositions_consistent": all_signed_decompositions_consistent,
            },
        }
    finally:
        flint_ctx.prec = saved_prec


# ---------------------------------------------------------------------------
# 7. Generator-Backed Review Interval Verification & Master Artifact Execution
# ---------------------------------------------------------------------------


_ARB_BACKTICK_INTERVAL_RE = re.compile(
    r"`\[(?:(?P<mid>[+-]?\d+(?:\.\d+)?(?:e[+-]?\d+)?)\s*)?\+/-\s*(?P<rad>\d+(?:\.\d+)?(?:e[+-]?\d+)?)\]`"
)
_LATEX_PM_INTERVAL_RE = re.compile(
    r"(?:\\bigl)?\[(?P<mid>[+-]?\d+(?:\.\d+)?(?:\s*\\times\s*10\^\{[+-]?\d+\})?)"
    r"\s*\\pm\s*(?P<rad>\d+(?:\.\d+)?(?:\s*\\times\s*10\^\{[+-]?\d+\})?)(?:\\bigr)?\]"
)
_TC_ENCLOSURE_TAG_RE = re.compile(
    r"<!--\s*tc-enclosure:\s*observable=\"(?P<observable>[^\"]+)\"\s+"
    r"params=\"(?P<params>[^\"]*)\"\s+"
    r"json_path=\"(?P<json_path>[^\"]+)\"\s*-->"
)
_FLINT_ARB_BALL_STR_RE = re.compile(
    r"^\[(?:(?P<mid>[+-]?\d+(?:\.\d+)?(?:e[+-]?\d+)?)\s*)?\+/-\s*(?P<rad>\d+(?:\.\d+)?(?:e[+-]?\d+)?)\]$"
)


def _sci_or_latex_num_to_fraction(num_str: str) -> Fraction:
    """Convert an exact decimal, scientific (`1.23e-8`), or LaTeX (`1.23 \\times 10^{-8}`)
    string into its exact `Fraction` without binary floating-point conversion.
    """
    cleaned = (num_str or "0").strip()
    if not cleaned:
        return Fraction(0)
    cleaned = re.sub(r"\s*\\times\s*10\^\{([+-]?\d+)\}", r"e\1", cleaned)
    return Fraction(cleaned)


def _parse_arb_ball_str_to_fractions(arb_ball_str: str) -> Tuple[Fraction, Fraction, Fraction]:
    """Parse FLINT's certified `arb_ball_str` (`[mid +/- rad]`, `[+/- rad]`, or exact decimal)
    into exact rational `(low, high, rad)` without binary float conversion.
    """
    s = arb_ball_str.strip()
    m = _FLINT_ARB_BALL_STR_RE.match(s)
    if m is not None:
        mid_f = Fraction(m.group("mid")) if m.group("mid") else Fraction(0)
        rad_f = Fraction(m.group("rad"))
        return mid_f - rad_f, mid_f + rad_f, rad_f
    exact_f = Fraction(s)
    return exact_f, exact_f, Fraction(0)


def _resolve_report_path_with_param_check(
    report: Dict[str, Any],
    json_path: str,
    params_str: str,
    observable: str,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Resolve `json_path` inside `report` (supporting dict keys and list selectors like
    `rows[Y=4]` or `rows[m=1]`) and verify that every `key=val` binding in `params_str`
    matches the resolved context dictionary / parameter fields, and `observable` matches
    the terminal field name (or declared observable identifier).
    """
    cur: Any = report
    context_params: Dict[str, Any] = {}
    segments = json_path.split(".")
    last_key = segments[-1]
    for seg in segments:
        m_sel = re.fullmatch(r"([A-Za-z0-9_]+)\[([^\]]+)\]", seg)
        if m_sel:
            list_key, pred_raw = m_sel.group(1), m_sel.group(2)
            if not isinstance(cur, dict) or list_key not in cur:
                raise KeyError(f"Missing list key {list_key!r} while resolving {json_path!r}")
            seq = cur[list_key]
            if not isinstance(seq, list):
                raise TypeError(f"Expected list at {list_key!r} in {json_path!r}")
            if re.fullmatch(r"\d+", pred_raw.strip()):
                idx = int(pred_raw.strip())
                cur = seq[idx]
            else:
                preds = [p.strip().split("=", 1) for p in pred_raw.split(",") if p.strip()]
                matches = []
                for item in seq:
                    if not isinstance(item, dict):
                        continue
                    if all(str(item.get(k.strip())) == v.strip() for k, v in preds):
                        matches.append(item)
                if len(matches) != 1:
                    raise KeyError(
                        f"Selector {seg!r} in {json_path!r} matched {len(matches)} rows (expected 1)"
                    )
                cur = matches[0]
            if isinstance(cur, dict):
                for k_item, v_item in cur.items():
                    if not isinstance(v_item, (dict, list)):
                        context_params[k_item] = v_item
        else:
            if not isinstance(cur, dict) or seg not in cur:
                raise KeyError(f"Missing key {seg!r} while resolving {json_path!r}")
            parent_dict = cur
            for k_item, v_item in parent_dict.items():
                if not isinstance(v_item, (dict, list)):
                    context_params[k_item] = v_item
                elif k_item == "counterexample_parameters" and isinstance(v_item, dict):
                    context_params.update(v_item)
            cur = parent_dict[seg]

    if not isinstance(cur, dict) or "lower_dec" not in cur or "upper_dec" not in cur:
        raise ValueError(f"Resolved node at {json_path!r} is not a serialized Arb dictionary")

    if not observable or (observable != last_key and last_key not in observable and observable not in last_key):
        raise ValueError(
            f"Observable mismatch: tag observable={observable!r} does not match terminal field {last_key!r}"
        )

    if params_str.strip():
        for binding in params_str.split(";"):
            binding = binding.strip()
            if not binding:
                continue
            p_key, p_val = binding.split("=", 1)
            p_key = p_key.strip()
            p_val = p_val.strip()
            if p_key not in context_params:
                raise KeyError(
                    f"Parameter {p_key!r} declared on {json_path!r} not found in resolved context {sorted(context_params.keys())}"
                )
            actual_val_str = str(context_params[p_key])
            if actual_val_str != p_val:
                raise ValueError(
                    f"Parameter mismatch on {json_path!r}: expected {p_key}={p_val!r}, got {actual_val_str!r}"
                )

    return cur, context_params


def verify_tc055_review_displayed_enclosures(
    report: Dict[str, Any],
    review_path: Path = TC_055_REVIEW_DOC_PATH,
) -> Dict[str, Any]:
    """Generator-backed verification of EVERY displayed certified interval in
    `docs/reviews/TC_055_SIMULTANEOUS_TAU_COMPATIBILITY.md` (`TASK-TC-055R2` §7):
    - Scans all backtick Arb balls `` `[mid +/- rad]` `` and LaTeX intervals `` `[mid \\pm rad]` ``
      across the entire review document.
    - Requires 100% tag coverage: every displayed certified interval must be immediately followed
      by `<!-- tc-enclosure: observable="..." params="..." json_path="..." -->` (zero untagged intervals).
    - Resolves `json_path` directly against the live/generated `report` (no second hardcoded list of
      expected decimal strings), checks observable and parameter bindings, and verifies by exact
      rational endpoint comparison that `[disp_mid - disp_rad, disp_mid + disp_rad]` contains the
      generated enclosure `[lower_dec, upper_dec]` while remaining tightly bounded (`disp_rad <= max(16 * gen_rad, 10^{-35})`).
    """
    text = Path(review_path).read_text(encoding="utf-8")
    raw_intervals: List[Tuple[int, int, str, str, str]] = []
    for m_bt in _ARB_BACKTICK_INTERVAL_RE.finditer(text):
        raw_intervals.append((m_bt.start(), m_bt.end(), "arb_backtick", m_bt.group("mid"), m_bt.group("rad")))
    for m_lx in _LATEX_PM_INTERVAL_RE.finditer(text):
        raw_intervals.append((m_lx.start(), m_lx.end(), "latex_pm", m_lx.group("mid"), m_lx.group("rad")))
    raw_intervals.sort(key=lambda item: item[0])

    checked_rows: List[Dict[str, Any]] = []
    untagged_intervals: List[Dict[str, Any]] = []
    failed_intervals: List[Dict[str, Any]] = []

    for start_pos, end_pos, fmt_kind, mid_s, rad_s in raw_intervals:
        line_no = text.count("\n", 0, start_pos) + 1
        tail_window = text[end_pos: end_pos + 600]
        m_tag = _TC_ENCLOSURE_TAG_RE.match(tail_window.lstrip(" $.,;)}"))
        if m_tag is None:
            untagged_intervals.append({
                "line": line_no,
                "format": fmt_kind,
                "displayed": text[start_pos:end_pos],
            })
            continue

        obs_name = m_tag.group("observable")
        params_str = m_tag.group("params")
        json_path = m_tag.group("json_path")
        try:
            target_node, resolved_ctx = _resolve_report_path_with_param_check(
                report=report,
                json_path=json_path,
                params_str=params_str,
                observable=obs_name,
            )
            disp_mid = _sci_or_latex_num_to_fraction(mid_s or "0")
            disp_rad = _sci_or_latex_num_to_fraction(rad_s)
            disp_low = disp_mid - disp_rad
            disp_high = disp_mid + disp_rad

            gen_low, gen_high, gen_rad = _parse_arb_ball_str_to_fractions(target_node["arb_ball_str"])
            contains_generated = bool(disp_low <= gen_low and disp_high >= gen_high)
            if "enclosure_arb" in target_node and isinstance(target_node["enclosure_arb"], arb):
                exact_low, exact_high = _exact_arb_endpoints_as_fractions(target_node["enclosure_arb"])
                contains_generated = bool(
                    contains_generated and disp_low <= exact_low and disp_high >= exact_high
                )
            tight_radius_cap = max(gen_rad * 16, Fraction(1, 10 ** 35))
            radius_is_tight = bool(disp_rad <= tight_radius_cap)
            ok = bool(contains_generated and radius_is_tight)
            rec = {
                "line": line_no,
                "format": fmt_kind,
                "observable": obs_name,
                "params": params_str,
                "json_path": json_path,
                "contains_generated_enclosure": contains_generated,
                "radius_is_tight": radius_is_tight,
                "verified": ok,
            }
            checked_rows.append(rec)
            if not ok:
                failed_intervals.append(rec)
        except Exception as exc:
            err_rec = {
                "line": line_no,
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


def execute_task_tc054_liouville_square_dilation_audit(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Execute the full TASK-TC-054 / TASK-TC-054R / TASK-TC-054R2 / TASK-TC-055 / TASK-TC-055R / TASK-TC-055R2 mathematical and numerical audit and return the report dictionary."""
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
    sec13_tc055r_finite = verify_tc055r_finite_truncation_and_signed_energy_attempt(prec_bits=prec_bits)

    report: Dict[str, Any] = {
        "task_id": TASK_TC_054_ID,
        "repair_task_id": TASK_TC_054R_ID,
        "closeout_task_id": TASK_TC_054R2_ID,
        "simultaneous_compatibility_task_id": TASK_TC_055_ID,
        "simultaneous_compatibility_repair_task_id": TASK_TC_055R_ID,
        "simultaneous_compatibility_closeout_task_id": TASK_TC_055R2_ID,
        "prime_chain_contraction_task_id": TASK_TC_056_ID,
        "coupled_scale_energy_bootstrap_task_id": TASK_TC_057_ID,
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
        "tc055_implementation_commit": TC_055_IMPLEMENTATION_COMMIT,
        "tc055_reviewed_tip": TC_055_REVIEWED_TIP,
        "tc055r_implementation_commit": TC_055R_IMPLEMENTATION_COMMIT,
        "tc055r_reviewed_tip": TC_055R_REVIEWED_TIP,
        "tc055r2_implementation_commit": TC_055R2_IMPLEMENTATION_COMMIT,
        "tc055r2_reviewed_tip": TC_055R2_REVIEWED_TIP,
        "tc056r2_implementation_commit": TC_056R2_IMPLEMENTATION_COMMIT,
        "tc056r2_reviewed_tip": TC_056R2_REVIEWED_TIP,
        "branch": "task/tc-057-coupled-arithmetic-scale-energy-bootstrap",
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
        "section_13_tc055r_finite_truncation_and_signed_energy_attempt": sec13_tc055r_finite,
        "claim_classification_map": {
            "unconditional_finite_arithmetic_theorems_proved_in_lean": [
                "smooth_coprime_positive_factorization_exists_unique_nat: unique positive factorization n = m * r with m P-smooth (in S(P)) and gcd(r, N_P) = 1 for arbitrary Finset P of primes (including empty P).",
                "finite_smooth_coprime_cutoff_indexing_bijection_nat: finite cutoff bijection {1 <= n <= T} <-> {(m, r) : m in S(P), m <= T, 1 <= r <= floor(T/m), gcd(r, N_P) = 1}, handling T = 0, T = 1, P = empty, and empty inner sums.",
                "finite_liouville_reindexed_sum_and_excess_cutoff_identity_nat: arbitrary-weight reindexed finite Liouville sum sum_{1<=n<=T} lambda(n) w(n) = sum_{m<=T, m in S(P)} sum_{1<=r<=floor(T/m), gcd(r, N_P)=1} lambda(m) lambda(r) w(m r) = sum_{1<=r<=T, gcd(r, N_P)=1} sum_{m<=floor(T/r), m in S(P)} lambda(r) lambda(m) w(m r), plus exact uncoupled excess identity when r <= T replaces r <= floor(T/m) (vanishing at P = empty, T <= 1, and (P = {2}, T = 2), and equal to w(6) at (P = {2}, T = 3)).",
                "finite_gaussian_observable_reconstruction_and_weighted_cofactor_square: instantiation to the finite Gaussian observable proving Q_{lambda,T}(X) = sum_{m<=T, m in S(P)} (lambda(m)/sqrt(m)) Q_{lambda,P,floor(T/m)}(X/m) = sum_{1<=r<=T, gcd(r, N_P)=1} (lambda(r)/sqrt(r)) Q_{lambda,S(P),floor(T/r)}(X/r) and pointwise weighted square decomposition (Q_{lambda,T}(X))^2 = sum_{r} (1/r) (Q_{lambda,S(P),floor(T/r)}(X/r))^2 + sum_{r != s} (lambda(r)lambda(s)/sqrt(r s)) Q_{lambda,S(P),floor(T/r)}(X/r) Q_{lambda,S(P),floor(T/s)}(X/s).",
                "actual_omega_factorization_and_liouville_common_factor_cancellation_nat, actual_prime_power_and_factored_square_divisor_moebius_liouville_inversion_nat, actual_finite_prime_exclusion_sieve_identity_nat, prime_parity_control_multiplicative_and_moebius_separation_nat: actual positive-integer Möbius-Liouville square-divisor inversions, finite-prime sieve, and parity control separation.",
                "abel_scaling_fourier_ratio_and_unequal_block_algebra, near_diagonal_kernel_bound_and_opposite_parity_dilation_pairing, pairing_counterexample_replacement_and_finite_reconstruction_tc055r: finite square-sum algebra, Fourier ratio denominator monotonicity, rational counterexample 3993/10000 < 1559/2890, and scalar kernel-ratio implications from explicit kernel-ratio hypotheses.",
            ],
            "universal_analytic_proofs_supplied_in_review": [
                "Reversible weighted L^2 norm equivalence between Q_mu and Q_lambda on H_eta (eta > 0) and equivalence with grade-interval subpower energy.",
                "Non-Schwartz C^1(R/Z) Poisson summation formula for sum_{d>=1} d^{-6} exp(-L^2/d^2), Mellin regularization + DLMF 5.8.3 contour shift, and global Stieltjes bound E_lambda(Y) <<_D Y / (log Y)^D (Y >= 2).",
                "Exact full-space inverse operator norm ||P_u^{-1}||_{H_eta -> H_eta} = prod_{p <= u} (1 - p^{-1/2 - eta})^{-1} via Q-linear independence of prime logarithms and continuous Kronecker simultaneous approximation.",
                "Floor-guarded tail bound sum_{n > u} n^{-3} <= 1 / (2 floor(u)^2) (u >= 1), least-prime coprime tail bounds (u >= 2), diagonal asymptotic D_E(Y), near-diagonal band inequality, two-sided integrand-ratio and transition relative-gap kernel bounds (with full (b/a)^3 factor), explicit C_{a_2} = 17 + (16/7)*zeta(3) remainder proof for Q_{a_2}(X) and E_{a_2}(Y), leading asymptotics for a_S (S = {3,5,7}), truncation tail energy bound R_tail(Y, T) <= (tau^5 - 1) Y^5 / (20 T^4) with two-sided L^2 transfer, and integrated weighted cofactor decomposition E_{lambda,T}(Y) = E_{same-r} + E_{diff-r}.",
            ],
            "certified_evaluations_at_specified_inputs": [
                "256-bit Arb enclosures of Fourier sign-change witnesses hat{f}(xi) at xi in {0, 1/2, 4/tau, 1, 3/2, 2} and legacy K_terms=1 refutation.",
                "256-bit Arb certifications of non-integer cutoff counterexample u = 2.9, exact dyadic rational boundary cutoffs u = 3 +- 2^{-100} and u = 5 +- 2^{-100}, Kronecker phase-alignment witness b_* = 2513 * tau / (2 * log 2), and retired pairing counterexample at (Y=33, p=11, q=2, r=5, m=1, n=11) with K_{33}(11,11) = 1.01455519480741885677e-8... and K_{33}(10,11) = 1.83203018490220578045e-9....",
                "256-bit Arb certifications of C_{a_2} = 17 + (16/7)*zeta(3) across X in {1, 2, 4, 8, 16, 32, 64}, derived E_{a_2}(Y) remainder bounds across Y in {1, 4, 8, 16, 32}, nonzero Gaussian uncoupled-cutoff excess witnesses, and weighted vs erroneous unweighted same-cofactor energy at (Y=4, T=6, P={2,3}) (0.048789276894385665... vs 0.120926881565465837...).",
            ],
            "algebraic_and_numerical_consistency_checks": [
                "Interval-overlap / zero-in-residual checks comparing direct coprime sums against operator products P_P Q_lambda(X), direct Q_{a_2}(X) against its coefficient-2 dyadic expansion, finite reconstructions against direct Q_{lambda,T}(X), and kernel-matrix cofactor grouping against independent `acb.integral` smooth-fiber quadrature (exact equality rests on the proved Lean/analytic identities, not on interval overlap).",
            ],
            "conditional_implications_and_unresolved_estimates": [
                "Conditional equivalence: SUBGATE-TC-043A <-> (forall eps > 0 exists C_eps < infty forall Y >= 1, 0 <= E_{lambda,T(Y)}(Y) = E_{same-r} + E_{diff-r} <= C_eps Y^eps) <-> RH.",
                "Unresolved target estimate: proving forall eps > 0 exists C_eps < infty forall Y >= 1, E_{lambda,T(Y)}(Y) <= C_eps Y^eps uniformly in Y without discarding cross-cofactor cancellation (SUBGATE-TC-043A remains OPEN; rh_proved remains false).",
            ],
        },
        "surviving_unconditional_theorems": [
            "Reversible square-dilation transfer lambda(n) = sum_{d^2 | n} mu(n/d^2), mu(n) = sum_{d^2 | n} mu(d) lambda(n/d^2), Q_lambda(X) = sum_{d>=1} Q_mu(X/d^2)/d, Q_mu(X) = sum_{d>=1} mu(d) Q_lambda(X/d^2)/d, and weighted L^2 norm equivalence ||Q_lambda||_eta <= zeta(1+2*eta) ||Q_mu||_eta, ||Q_mu||_eta <= (zeta(1+2*eta)/zeta(2+4*eta)) ||Q_lambda||_eta for all eta > 0.",
            "Equivalence between the grade-interval subpower energy bound (forall eps > 0 exists C_eps, int_Y^{tau Y} |Q_a(X)|^2 dX/X <= C_eps Y^eps) and weighted norm finiteness (forall eta in (0, 5/2), ||Q_a||_eta < infty) for both a = mu and a = lambda.",
            "Unconstrained common-factor expansion Q_lambda(X)^2 = sum_{gcd(r,s)=1} (lambda(r) lambda(s) X^5 / (r s)^3) sum_{d>=1} d^{-6} exp(-L^2/d^2) (with lambda(d r) lambda(d s) = lambda(r) lambda(s) for ALL d >= 1) and fixed-order Euler-Maclaurin error bound |E^lambda_{r,s}(X)| <= C_N X^{-N} (r s)^{N+2} / (r^2 + s^2)^{(N+5)/2} (C_2 = 1.8512576670..., C_4 = 8.7523717600...), controlling every fixed subtransition range A <= X^{1 - delta} whenever (N + 1) delta > 1.",
            "Exact Poisson summation formula sum_{d>=1} d^{-6} exp(-L^2/d^2) = L^{-5} [c_0 + sum_{j>=1} hat{f}(j L)] (with c_0 = 3 sqrt(tau/2) / 8) established via C^infty flatness at 0, O(|v|^{-6-j}) decay at infinity, and C^1(R/Z) periodization (DLMF 1.8.14), Mellin regularization + contour shifting with |R_M(omega)| <= 8 omega^{2M+3/2} / (Gamma(2M+5/2) Gamma(M-3/4)) -> 0, repaired Fourier tail-ratio certification (R_even, R_odd <= 1/2 or 1/(1-R)), and certified sign changes hat{f}(1/2) < 0, hat{f}(4/tau) < 0, hat{f}(1) < 0, hat{f}(3/2) > 0, hat{f}(2) > 0.",
            "Repaired unequal-block bound |B_{A,B}(X)| <= (7/3) C_* min(A,B)^3 / max(A,B)^2 with C_* = max{zeta(6), c_0 + 27 exp(-3)} = 2.008921040021894970679058028804597412605..., repaired dyadic Abel bound |U_lambda(Y; M)| << M^{1/2} min(M/Y, (Y/M)^{5/2}) exp(-c Phi(M)) (M >= 16), and unconditional global Stieltjes energy theorem |Q_lambda(X)| << sqrt(X) exp(-c_1 Phi(X)) (X >= 256), E_lambda(Y) := int_Y^{tau Y} |Q_lambda(X)|^2 dX/X << Y exp(-2 c_2 Phi(Y)) (Y >= 256), and E_lambda(Y) <<_D Y (log Y)^{-D} (Y >= 2, via compact-range bound E_lambda(Y) <= (zeta(3)^2 (tau^5 - 1) / 5) Y^5 on 2 <= Y < 256) by splitting Q_lambda(X) = -X^{5/2} int_1^infty L_lambda(t) d/dt(t^{-3} exp(-X^2/t^2)) dt at t = sqrt(X) with scaling constant int_0^infty u |3 - 2 u^2| exp(-u^2) du = 1/2 + 2 exp(-3/2).",
            "Exact dyadic parity annihilation Q_{lambda,odd}(X) = Q_lambda(X) + 2^{-1/2} Q_lambda(X/2), convergent dyadic inversion, exact grade-interval energy identity on [Y, tau Y] with cross-scale correlation, bounded norm equivalence for all eta > -1/2, and proof that |1 + 2^{-rho}| >= 1 - 2^{-x} > 0 for rho = x + i*y with x > 0.",
            "Simultaneous finite-prime exclusion identity Q_{lambda,P}(X) = prod_{p in P}(I + p^{-1/2} S_p) Q_lambda(X) = sum_{d | N_P} (|mu(d)| / sqrt(d)) Q_lambda(X / d) = X^{5/2} sum_{gcd(n, N_P)=1} (lambda(n)/n^3) exp(-X^2/n^2) (integer sieve formalized in Lean 4 theorem actual_finite_prime_exclusion_sieve_identity_nat), its convergent P-smooth inverse reconstruction Q_lambda(X) = sum_{m in S(P)} (lambda(m)/sqrt(m)) Q_{lambda,P}(X/m), and exact removable trivial-zero cancellation lim_{z -> -(2m+1/2)} zeta(1+2z)/zeta(1/2+z) = 2 zeta'(-4m)/zeta'(-2m) = 2 (-1)^m (4m)! zeta(4m+1) / (tau^{2m} (2m)! zeta(2m+1)) != 0.",
            "Exact coprime decomposition Q_{lambda,P_u}(w) = w^{5/2} exp(-w^2) + R_{lambda,P_u}(w) for real u >= 2 with exact rational/dyadic-endpoint floor and least-prime tail bounds |R_{lambda,P_u}(w)| <= w^{5/2} / (2 floor(u)^2), |R_{lambda,P_u}(w)| <= w^{5/2} / (2 (q_{>u} - 1)^2), and |R_{lambda,P_u}(w)| <= w^{5/2} (1/q_{>u}^3 + 1/(2 q_{>u}^2)), exact full-space operator norm equality ||P_u^{-1}||_{H_eta -> H_eta} = sup_{b in R} prod_{p <= u} |1 + p^{-1/2 - eta} exp(-i b log p)|^{-1} = prod_{p <= u} (1 - p^{-1/2 - eta})^{-1} via continuous Kronecker simultaneous approximation (witness b_* = 2513 * tau / (2 * log 2)), diagonal energy asymptotic D_E(Y) := sum_{n>=1} K_Y(n, n) = (3 sqrt(tau) / 64) log tau + R_{D,E}(Y) with |R_{D,E}(Y)| <= C_{D,2} Y^{-2} (C_{D,2} = C_2 (1 - tau^{-2}) / (16 sqrt(2)) = 0.07974240995631961...) for all Y > 0, and unconditional near-diagonal band inequality sum_{|m - n| <= H} K_Y(m, n) <= (2 H + 1) D_E(Y) for all integers H >= 0 (retaining the full complementary off-diagonal domain |m - n| > H).",
            "Opposite-parity prime-semiprime sign identity lambda(p m) + lambda(q r m) = 0, valid replacement kernel enclosures r_0^3 exp(-(tau Y)^2 Delta) K_Y(b, n) <= K_Y(a, n) <= r_0^3 exp(-Y^2 Delta) K_Y(b, n), |K_Y(a, n) - K_Y(b, n)| <= max(|r_0^3 exp(-(tau Y)^2 Delta) - 1|, |r_0^3 exp(-Y^2 Delta) - 1|) K_Y(b, n), and |K_Y(a, n) - K_Y(b, n)| <= ((b - a)/a)(b/a)^3 (3 + 2 tau^2 Y^2 / a^2) K_Y(b, n) for all 0 < a <= b (uniform O((b-a)/a) when both a >= c Y and 1 <= b/a <= R), repaired 2-adic parity control constant C_{a_2} = 17 + (16/7) zeta(3) = 19.74755863579336... giving Q_{a_2}(X) = sqrt(X)/6 + O(X^{-1/2}) (X >= 1) and E_{a_2}(Y) = ((tau - 1)/36) Y + O(1) (Y >= 1), leading asymptotics Q_{a_{3,5,7}}(X) ~ sqrt(X)/8 and E_{a_{3,5,7}}(Y) ~ ((tau - 1)/64) Y (mean 1/4), and full Lean-formalized finite smooth-coprime factorization bijection, arbitrary-weight reindexed Liouville sum, exact uncoupled-cutoff excess identity, Gaussian observable reconstruction, and weighted cofactor energy decomposition E_{lambda,T}(Y) = E_{same-r} + E_{diff-r} with 1/r and lambda(r)lambda(s)/sqrt(rs) weights and two-sided L^2 tail transfer at exact T(Y) = ceil(Y^{5/4}).",
        ],
        "precise_obstruction_to_subgate_tc043a_closure": (
            "1. In Attack A, the bivariate coprime Dirichlet series D_lambda(u, v) = zeta(2u) zeta(2v) / (zeta(u) zeta(v) zeta(u+v)) "
            "has numerator zeta(2u) zeta(2v) and coprimality factor 1/zeta(u+v) evaluated at 2u, 2v, u+v in the Euler-product "
            "half-plane Re(w) > 1 whenever Re(u) = Re(v) = x > 1/2, so neither factor can vanish at an off-critical conjugate pair "
            "(rho, conj(rho)) (rho = x + i*y) to cancel the poles of 1/(zeta(u) zeta(v)); moreover in D_lambda(s) = zeta(2s)/zeta(s) "
            "the pole of zeta(2s) at s = 1/2 remains (giving the z = 0 simple pole of M[Q_lambda](z) of residue Gamma(5/4)/(4 zeta(1/2)) = -0.1551682265... != 0), "
            "while the denominator pole of zeta(s) at s = 1 produces a zero D_lambda(1) = 0. While the global Stieltjes integration-by-parts proof "
            "establishes E_lambda(Y) << Y exp(-2 c_2 Phi(Y)) <<_D Y (log Y)^{-D}, this is an upper bound and does not establish "
            "forall eps > 0, E_lambda(Y) <= C_eps Y^eps. "
            "2. In Attack B and its simultaneous finite-prime extension P_u = prod_{p <= u}(I + p^{-1/2} S_p) (TASK-TC-055 / TASK-TC-055R / TASK-TC-055R2), "
            "every finite-prime filter multiplies an off-critical mode F_rho(X) = X^{rho - 1/2} (rho = x + i*y, x > 0) by "
            "M_u(rho) = prod_{p <= u}(1 + p^{-rho}) with 0 < prod_{p <= u}(1 - p^{-x}) <= |M_u(rho)| <= prod_{p <= u}(1 + p^{-x}), "
            "and on the full weighted space H_eta = L^2((0, infty), X^{-2*eta} dX/X) the inverse operator norm equals "
            "||P_u^{-1}||_{H_eta -> H_eta} = sup_{b in R} prod_{p <= u}|1 + p^{-1/2 - eta} exp(-i b log p)|^{-1} = prod_{p <= u}(1 - p^{-1/2 - eta})^{-1} "
            "EXACTLY by Q-linear independence of prime logarithms and continuous Kronecker simultaneous approximation (diverging as u -> infty "
            "for all 0 < eta <= 1/2, so no full-space signed multiplier norm improvement exists). "
            "3. Under the proved two-sided L^2 truncation transfer at exact T(Y) = ceil(Y^{5/4}) (R_tail(Y, T(Y)) <= (tau^5 - 1)/20 = O(1)), "
            "SUBGATE-TC-043A is equivalent to the finite joint-energy target: forall eps > 0 exists C_eps < infty forall Y >= 1, "
            "0 <= E_{lambda,T(Y)}(Y) = E_{same-r}(Y; T(Y), P_u) + E_{diff-r}(Y; T(Y), P_u) <= C_eps Y^eps (retaining the signed cross-cofactor sum "
            "with weights 1/r and lambda(r)lambda(s)/sqrt(rs)). Taking u >= T(Y) eliminates E_{diff-r} (forcing r = 1) but incurs the super-polynomial "
            "Kronecker Euler-product norm prod_{p <= u}(1 - p^{-eta})^{-1} and hyperbolic inner-cutoff floor(T/m) boundary coupling, while keeping u "
            "small leaves the combined signed sum E_{same-r} + E_{diff-r} over unfactored primes p > u unresolved."
        ),
    }

    arb_check = verify_all_serialized_arb_in_tree(report)
    assert arb_check["all_enclose_original_256bit_arb_ball"] is True, (
        f"Serialized Arb enclosure verification failed: {arb_check.get('failed_paths')}"
    )
    review_enclosures_audit = verify_tc055_review_displayed_enclosures(report)
    assert review_enclosures_audit["all_displayed_intervals_contain_generated_enclosures"] is True, (
        "Displayed intervals in TC_055_SIMULTANEOUS_TAU_COMPATIBILITY.md failed generator-backed check: "
        f"untagged={review_enclosures_audit['untagged_intervals']}, "
        f"failed={review_enclosures_audit['failed_intervals']}"
    )
    report["section_14_tc055r2_review_displayed_enclosures_audit"] = review_enclosures_audit
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
    path.write_text(
        json.dumps(cleaned, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return cleaned


if __name__ == "__main__":
    rep = write_task_tc054_liouville_square_dilation_artifact()
    print(f"Wrote {LIOUVILLE_SQUARE_DILATION_ARTIFACT_PATH} (subgate={rep['subgate_tc043a_status']}, rh_proved={rep['rh_proved']})")
