r"""
TASK-TC-060 / TASK-TC-060R: Signed Dilation Multipliers, Arithmetic Control of the Complete
Reconstruction, and Full-Core / Quantified Counterexample / Certificate Repair toward SUBGATE-TC-043A.

Implements, tests, falsifies, and certifies in 256-bit FLINT/Arb ball arithmetic (using tau
strictly via `_tau_arb()` as the sole circle constant, complex variable z = x + i*y with real x, y,
critical line x = 1/2, zero displacement delta = x - 1/2, Fourier/Mellin frequency variable v in R
and complex w = u + i*v with real u, v, real algebraic geometric grades K kept strictly distinct
from auxiliary real log scales t = log X, frequencies v, and divisor shifts log d):

1. Section 1 — Exact Object Recovery, Source Endpoint Convention, & Non-Circularity Reassembly
   (`Lean Theorem 1: noncircular_reassembly_and_basis_stratification_tc060`):
   - Preserves phi_n(X) = X^{5/2} n^{-3} exp(-X^2/n^2), Q_{lambda,L}(X) = sum_{1<=n<=L} lambda(n)*phi_n(X),
     fixed window cutoff T(Y) = ceil(Y^{5/4}) on [Y, tau*Y], L_d = floor(T/d), and R(d) = W_2(d) - c_lambda*d
     (`R(0) = 0`, `R(1) = -c_lambda > 0`, `R(d) - R(d-1) = w_{2,lambda}(d) - c_lambda` for all `d >= 1`).
   - Preserves identical inner cutoff `L_d` at both endpoints of `Delta_d^{sm}(X) = d^{-1/2} Q_{lambda,L_d}(X/d) - (d+1)^{-1/2} Q_{lambda,L_d}(X/(d+1))`,
     keeping `Delta_d^{jump}(X)` separate, defining the `T = 0` empty reconstruction without evaluating `phi_0`,
     and verifying `T = 0, 1` and general `T >= 1` reassembly:
       `r_{sm,T} + r_{jump,T} + R(T)*phi_T = sum_{n<=T} lambda(n)*(log n)^2*phi_n - c_lambda*Q_{1_sq,T}`
     and exact return to `D_{2,Y} = P_Y - R_Y` (`Q_{lambda,T} = 2*P_Y - D_{2,Y}` on `Y >= 2`).
   - Verifies exact basis stratification `r_{sm,T}(X) = sum_{n=1}^{2T} alpha_T(n)*phi_n(X)` (`T >= 2`):
     `alpha_T(n) = lambda(n)*(log n)^2 - c_lambda*1_{sq}(n)` for `1 <= n <= T - 1`, `-R(T)` endpoint shift at
     `n = T`, and nonzero spillover onto `T + 1 <= n <= 2T` culminating in `alpha_T(2T) = c_lambda*lambda(T) != 0`.

2. Section 2 — Signed Dilation Fourier Representation, Sharp Multiplier Attainment, Cutoff Blocks, & Gram Kernel
   (`Analytic outside Lean` for finite-`L` Fourier/Gamma substitution + `Lean Theorems 2 & 3` for multiplier, blocks, & Gram):
   - Finite-cutoff Fourier transform (`t = log X`, `q_L(t) = Q_{lambda,L}(exp t)`), proved analytically outside Lean:
     `qhat_L(v) = (1/2) * Gamma(5/4 - i*v/2) * sum_{n<=L} lambda(n) * n^{-1/2 - i*v}`, cross-checked against
     direct real-line `acb.integral` quadrature with certified left/right improper analytic tail balls.
   - Adjacent dilation multiplier `m_d(v) = d^{-1/2} exp(-i*v*log d) - (d+1)^{-1/2} exp(-i*v*log(d+1))`:
     certifies elementary benchmark `|m_d(v)| <= min(d^{-1/2}+(d+1)^{-1/2}, sqrt(1/4+v^2) * int_d^{d+1} t^{-3/2} dt)`
     (valid for ALL `v in R` when retaining `(1+|v|)` / `sqrt(1/4+v^2)`) and exact unrestricted-frequency supremum
     attainment `|m_d(v_k(d))| = d^{-1/2} + (d+1)^{-1/2}` at `v_k(d) = (2k+1)*tau / (2*log(1 + 1/d))` (obstructing
     only a frequency-independent relative `O(1/d)` saving).
   - Exact level-set cutoff blocks `I_L(T) = {1<=d<T : floor(T/d) = L}` (`1 <= L <= T`), including empty blocks
     (`I_1(2) = empty`), singleton blocks for `d*(d+1) <= T` (and `I_T(T) = {1}` for all `T >= 2`),
     `N_blocks(T) = 2*sqrt(T) + O(1)` (never logarithmic), and `Fourier[r_{sm,T}(exp t)](v) = sum_{L=1}^T M_{L,T}(v)*qhat_L(v)`.
   - Real-space signed Gram kernel `H_{Y,b}(d, e)` and `(log X)^{-4}`-weighted kernel `H_{Y,b}^{wt}(d, e)` (`Y >= 2`,
     keeping `(log X)^{-2}` inside the window integral), cross-checked against direct window quadrature across
     integer and noninteger window bases `Y` and `b in {2, e, tau}` with directed log-sandwich bounds.

3. Section 3 — Quantitative Attempts A & B, Quantified Obstructions, & Residue-Defined `z = 1/2` Drift Theorem
   (`Lean Theorems 4, 5, & 7` + Outside-Lean Summation/Cutoff Proofs):
   - Attempt A: Gaussian Schwartz window majorant (`[log Y, log(bY)]`), global Plancherel vs local window energy,
     local-window low/high frequency cross-term non-orthogonality, closed-form all-`v` Gamma majorant,
     residue-defined `z = 1/2` drift model `M_{sq,2}(d) = 4*sqrt(d)*log(d) + c_{1/2,lambda}*sqrt(d)` (where
     `D_lambda(z) = zeta(2z)/zeta(z)` has a simple zero at `z = 1` and a simple pole at `z = 1/2`) and exact
     residual `R_{osc}(d) := R(d) - M_{sq,2}(d)` (`R(d) > 0` certified finitely on `1 <= d <= 2000` with `0` sign flips
     vs `178` sign flips of `R_{osc}`), and **exact singleton-block refutation of Candidate A1 as stated**
     (`I_T(T) = {1}` for `T >= 2`, `v = 0`, `R(1) = -c_lambda > 0`, `m_1(0) = 1 - 2^{-1/2} > 0` giving ratio `= 1`,
     refuting uniform `(log T)^{-1-delta}` decay across all `T >= T_0`, `L`, and allowed low frequencies).
   - Attempt B & Informed Replacement: certifies `dq = er` product compensation (`|H_{16}(8,1)| / H_{16}(8,8) > 2`),
     refutes Candidate B1 (`||Delta_d^{sm}(a)||_Y <= (C/d)*||g_{a,d}||_Y`) for **every fixed constant `C`** across
     arbitrary coefficients via the unbounded family `d = 1 < T(Y)` (`Y >= 2`), `a = e_1` (`phi_2(X)/phi_1(X) = exp(3*X^2/4)/8`,
     `||phi_1 - phi_2||_Y / ||phi_1||_Y >= exp(3*Y^2/4)/8 - 1 -> infty`), while keeping finite diagnostics (`819.07`,
     `2.87 < 3.74 < 5.30`) and actual Liouville witnesses (`2.975`, `3.081`, excluding `C = 1` and `C = 3` on their
     tested domains) strictly scoped; verifies unconditional `w_{2,lambda}` prime vs `6p` support (`w_{2,lambda}(p) = -(log p)^2`,
     `w_{2,lambda}(6p) = 0` for prime `p >= 5`); and proves the **Informed Replacement Split**
     `r_{sm,T} = r_{sm,T}^{drift} + r_{sm,<=min(D_0,T-1)}^{osc} + r_{sm,>min(D_0,T-1)}^{osc}` with certified floor
     determination (`D_0(Y) = floor(log Y)` at `kappa = 1`, so `D_0(2) = 0` gives an empty small-divisor slice),
     corrected `O(log Y)` sub-unit (`d > floor(Y)`) and reindexed drift-jump (`d = floor(T/q)`, `2 <= q <= T`)
     summations, and unconditional all-`eps` relative contraction on `r_{sm,T(Y)}^{drift}/(log X)^2` and `1 <= d <= min(D_0(Y), T(Y)-1)`.

4. Section 4 — Complete Reconstruction Energy Bridge & Full-Core Global Consequence Classification
   (`Lean Theorems 6 & 7`):
   - Tracks the complete reconstruction `Q_{lambda,T} = 2*P_Y - D_{2,known,Y} - D_{2,core,Y}` retaining the **full open core**
     `min(D_0(Y), T(Y)-1) < d <= T(Y)-1` inside `D_{2,core,Y} = (sum_{min(D_0,T-1)<d<=T-1} R_{osc}(d)*Delta_d^{sm} - Q_{lambda,T}^{[2]}) / (log X)^2`
     (including `d >= ceil(tau*Y)`, since Lemma B2's `O(Y*(log Y)^{-4}*exp(-2*c_W*sqrt(log Y)))` bound is only an
     absolute upper bound whose majorant divided by `Y^eps` grows without bound for `0 < eps < 1`, tested explicitly
     where nonempty at `Y = 4096`) and the full signed `8*X_tilde(Y) + 4*||D_{2,core,Y}||_Y^2`, keeping `B_drift`,
     `B_sample`, and `B_known` distinct, `SUBGATE-TC-043A` `OPEN`, and `rh_proved = False`.

5. Section 5 — Controls, Certified Cutoffs & Boundary Schedules, & Directed Interval Certificates:
   - Compares actual Liouville `lambda`, unsigned `1`, finite-prime parity controls `a_2` and `a_{3,5,7}` with their
     own derived second-order Laurent compensations `M_{2,a}(d)`, geometry-only controls, and an explicitly labeled
     hybrid diagnostic (`inner = a_2` with `R_lambda(d)`).
   - Enforces certified integer floor/ceiling determination (rejecting straddling enclosures), directed interval
     inequality certification (`upper(LHS) <= lower(RHS)`), and separation of numerical Rayleigh diagnostics.
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
    _acb_integral_certified_arb,
    _evaluate_route_d_totals_arb,
    _frac_to_arb,
    _tau_arb,
    _weight_fn_for_mode,
    evaluate_E_L_scale_arb,
    evaluate_Q_shifted_finite_arb,
    prime_power_pairs_up_to,
    selberg_w2_weight_arb,
)
from tc.dyadic_power_lift_primitive_correlation import (
    EPISTEMIC_CATEGORIES,
    PARENT_SUBGATE_ID,
    REVIEWED_MERGED_MAIN_BASELINE,
    REVIEWED_TC_059R_IMPLEMENTATION as INHERITED_FORMAL_PRODUCING_COMMIT,
    TASK_TC_059_ID,
    TASK_TC_059R_ID,
    TASK_TC_059R2_ID,
    evaluate_Q_general_arb,
    evaluate_bilinear_window_pairing_closed_arb,
    evaluate_window_kernel_K_closed_arb,
    is_perfect_square_int,
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
    _exact_arb_endpoints_as_fractions,
    _parse_arb_ball_str_to_fractions,
    _resolve_report_path_with_param_check,
    _sci_or_latex_num_to_fraction,
    finite_prime_parity_aS_int,
    liouville_lambda_int,
    two_adic_parity_a2_int,
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
)

TASK_TC_060_ID = "TASK-TC-060"
TASK_TC_060R_ID = "TASK-TC-060R"
ACCEPTED_TC059R2_BRANCH = "task/tc-059r2-numerical-assertion-and-report-closeout"
REVIEWED_TC059R2_IMPLEMENTATION = "25099194f7e951b0cea8ec9c4829249f7221ca56"
REVIEWED_TC059R2_HEAD = "779be2f9e68765815ceb54e4cfb9239596c5e06d"
PROPOSED_TC060_BRANCH = "task/tc-060-signed-dilation-multiplier-and-arithmetic-energy"
REVIEWED_TC060_IMPLEMENTATION = "f95dd15825b4637ff2ec7f22c6e987b9fe6ea6b4"
REVIEWED_TC060_HEAD = "240307a593b08ab43ffe975ffeb5d7789e5b9a51"
REPAIR_TC060R_BRANCH = "task/tc-060r-full-core-counterexample-and-proof-scope-repair"

SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_signed_dilation_arithmetic_energy.json"
)
TC_060_REVIEW_DOC_PATH = (
    REPO_ROOT / "docs" / "reviews" / "TC_060_SIGNED_DILATION_ARITHMETIC_ENERGY.md"
)
TC_060_LEAN_MODULE_PATH = (
    REPO_ROOT / "formal" / "RiemannScope" / "SignedDilationArithmeticEnergy.lean"
)
FORMAL_BUILD_REPORT_PATH = REPO_ROOT / "formal" / "build_report.json"

EXPECTED_TC060_THEOREMS: List[str] = [
    "noncircular_reassembly_and_basis_stratification_tc060",
    "adjacent_dilation_multiplier_and_cutoff_blocks_tc060",
    "signed_gram_kernel_and_log_weighted_quadratic_form_tc060",
    "gaussian_window_majorant_and_local_frequency_split_tc060",
    "second_order_drift_abel_and_small_divisor_contraction_tc060",
    "complete_reconstruction_drift_contraction_transfer_tc060",
    "full_core_quantified_obstructions_and_w2_support_tc060r",
]

GLOBAL_CONSEQUENCE_CLASSES: Tuple[str, ...] = (
    "ABSOLUTE_LOGARITHMIC_IMPROVEMENT",
    "FIXED_POWER_SAVING",
    "RELATIVE_CONTRACTION",
    "ALL_POSITIVE_EXPONENTS_CLOSURE",
)


class AmbiguousCutoffError(ValueError):
    """Raised when an interval enclosure straddles an integer cutoff boundary without an exact
    symbolic identity, so neither floor nor ceiling is uniquely determined by the input enclosure.
    """


# ---------------------------------------------------------------------------
# 0. Directed Interval Certification & Signed Dilation / Arithmetic Helpers
# ---------------------------------------------------------------------------


def enclose_discrete_grid_max(balls: Sequence[arb]) -> arb:
    """Return an outward-rounded two-sided Arb enclosure of `max_i v_i` given enclosures `B_i ni v_i`."""
    if not balls:
        raise ValueError("Discrete grid maximum requires at least one Arb ball")
    lo_balls = [b.lower() for b in balls]
    hi_balls = [b.upper() for b in balls]
    lo_max = max(lo_balls, key=lambda b: _exact_arb_endpoints_as_fractions(b)[0])
    hi_max = max(hi_balls, key=lambda b: _exact_arb_endpoints_as_fractions(b)[1])
    return lo_max.union(hi_max)


def classify_interval_endpoints_le(
    lhs_lo: Fraction,
    lhs_hi: Fraction,
    rhs_lo: Fraction,
    rhs_hi: Fraction,
    *,
    exact_algebraic_equality_justified: bool = False,
) -> Tuple[str, bool]:
    """Classify whether exact intervals `[lhs_lo, lhs_hi]` and `[rhs_lo, rhs_hi]` certify `LHS <= RHS`.

    - `lhs_hi <= rhs_lo`: directed separation (`CERTIFIED_DIRECTED_INEQUALITY`, True), unless
      `exact_algebraic_equality_justified=True` is asserted on strictly separated intervals
      `lhs_hi < rhs_lo` (`INCONSISTENT_ALGEBRAIC_EQUALITY_CLAIM`, False).
    - `lhs_lo > rhs_hi`: strict violation (`REFUTED_STRICT_VIOLATION`, False).
    - Overlapping intervals (`lhs_hi > rhs_lo` and `lhs_lo <= rhs_hi`): returns
      (`NOT_NUMERICALLY_CERTIFIED_OVERLAP`, False) unless backed by an explicit deductive algebraic
      or formal equality theorem (`exact_algebraic_equality_justified=True`), in which case enclosure
      overlap confirms consistency (`CERTIFIED_EXACT_ALGEBRAIC_EQUALITY_WITH_CONSISTENT_ENCLOSURE`, True).
    """
    if lhs_lo > lhs_hi or rhs_lo > rhs_hi:
        raise ValueError(f"Invalid interval endpoints: [{lhs_lo}, {lhs_hi}] vs [{rhs_lo}, {rhs_hi}]")
    if lhs_hi <= rhs_lo:
        if exact_algebraic_equality_justified and lhs_hi < rhs_lo:
            return ("INCONSISTENT_ALGEBRAIC_EQUALITY_CLAIM", False)
        return ("CERTIFIED_DIRECTED_INEQUALITY", True)
    if lhs_lo > rhs_hi:
        return ("REFUTED_STRICT_VIOLATION", False)
    if not exact_algebraic_equality_justified:
        return ("NOT_NUMERICALLY_CERTIFIED_OVERLAP", False)
    return ("CERTIFIED_EXACT_ALGEBRAIC_EQUALITY_WITH_CONSISTENT_ENCLOSURE", True)


def classify_arb_le_certificate(
    lhs_ball: arb,
    rhs_ball: arb,
    *,
    exact_algebraic_equality_justified: bool = False,
) -> Tuple[str, bool]:
    """Directed Arb inequality certificate check using exact dyadic endpoints + outward difference."""
    lhs_lo, lhs_hi = _exact_arb_endpoints_as_fractions(lhs_ball)
    rhs_lo, rhs_hi = _exact_arb_endpoints_as_fractions(rhs_ball)
    status, certified = classify_interval_endpoints_le(
        lhs_lo,
        lhs_hi,
        rhs_lo,
        rhs_hi,
        exact_algebraic_equality_justified=exact_algebraic_equality_justified,
    )
    diff_ball = rhs_ball - lhs_ball
    if status == "CERTIFIED_DIRECTED_INEQUALITY":
        if not bool(lhs_ball.upper() <= rhs_ball.lower() and diff_ball.lower() >= arb(0)):
            return ("NOT_NUMERICALLY_CERTIFIED_OVERLAP", False)
    elif status == "CERTIFIED_EXACT_ALGEBRAIC_EQUALITY_WITH_CONSISTENT_ENCLOSURE":
        if not bool(arb(0) in diff_ball):
            return ("INCONSISTENT_ALGEBRAIC_EQUALITY_CLAIM", False)
    return (status, certified)


def classify_floor_from_arb_enclosure(
    ball: arb,
) -> Tuple[str, Optional[int], Tuple[int, int]]:
    """Determine `floor(x)` from exact dyadic endpoints `[lo, hi]` of an `arb` ball.

    Returns `("CERTIFIED_UNIQUE_FLOOR", fl, (fl, fl))` iff `floor(lo) == floor(hi)`; otherwise
    returns `("AMBIGUOUS_STRADDLING_ENCLOSURE", None, (floor(lo), floor(hi)))` without ever picking
    a midpoint or uncertified endpoint.
    """
    if not ball.is_finite():
        raise AmbiguousCutoffError(f"Non-finite Arb ball in floor determination: {ball}")
    lo_f, hi_f = _exact_arb_endpoints_as_fractions(ball)
    fl_lo = lo_f.numerator // lo_f.denominator
    fl_hi = hi_f.numerator // hi_f.denominator
    if fl_lo == fl_hi:
        return ("CERTIFIED_UNIQUE_FLOOR", fl_lo, (fl_lo, fl_hi))
    return ("AMBIGUOUS_STRADDLING_ENCLOSURE", None, (fl_lo, fl_hi))


def certify_floor_from_arb_enclosure(ball: arb) -> int:
    """Return the unique certified floor of `ball`, or raise `AmbiguousCutoffError` if straddling."""
    status, val, cand = classify_floor_from_arb_enclosure(ball)
    if status != "CERTIFIED_UNIQUE_FLOOR" or val is None:
        raise AmbiguousCutoffError(
            f"Ambiguous floor for straddling Arb enclosure {ball}: candidate floors in [{cand[0]}, {cand[1]}]"
        )
    return val


def classify_ceil_from_arb_enclosure(
    ball: arb,
) -> Tuple[str, Optional[int], Tuple[int, int]]:
    """Determine `ceil(x)` from exact dyadic endpoints `[lo, hi]` of an `arb` ball."""
    if not ball.is_finite():
        raise AmbiguousCutoffError(f"Non-finite Arb ball in ceil determination: {ball}")
    lo_f, hi_f = _exact_arb_endpoints_as_fractions(ball)
    cl_lo = -((-lo_f.numerator) // lo_f.denominator)
    cl_hi = -((-hi_f.numerator) // hi_f.denominator)
    if cl_lo == cl_hi:
        return ("CERTIFIED_UNIQUE_CEIL", cl_lo, (cl_lo, cl_hi))
    return ("AMBIGUOUS_STRADDLING_ENCLOSURE", None, (cl_lo, cl_hi))


def certify_ceil_from_arb_enclosure(ball: arb) -> int:
    """Return the unique certified ceiling of `ball`, or raise `AmbiguousCutoffError` if straddling."""
    status, val, cand = classify_ceil_from_arb_enclosure(ball)
    if status != "CERTIFIED_UNIQUE_CEIL" or val is None:
        raise AmbiguousCutoffError(
            f"Ambiguous ceiling for straddling Arb enclosure {ball}: candidate ceilings in [{cand[0]}, {cand[1]}]"
        )
    return val


def certify_D0_small_divisor_cutoff(
    Y: Optional[Union[int, Fraction, arb]] = None,
    *,
    kappa: Union[int, Fraction] = 1,
    exact_log_Y: Optional[Union[int, Fraction]] = None,
    require_Y_ge_2: bool = True,
    prec_bits: int = 256,
    max_prec_bits: int = 4096,
) -> int:
    """Certify `D_0(Y) = floor((log Y)^{(4 - kappa) / 3})` (`kappa in (0, 1]`; `floor(log Y)` at `kappa = 1`)
    without floating-point integer selection.

    - Rejects `float` inputs (`TypeError`), missing inputs (`Y is None and exact_log_Y is None`),
      and conflicting dual inputs (`Y is not None and exact_log_Y is not None`).
    - If `exact_log_Y` is supplied (with `Y=None`, representing symbolic `Y = exp(exact_log_Y)` with
      rational `log Y >= 0`), certifies `exact_log_Y >= log(2)` via iterative Arb ball separation when
      `require_Y_ge_2=True`, then certifies `floor(exact_log_Y^{(4-kappa)/3})` via exact integer power bounds.
    - For exact `int` / `Fraction` `Y`: uses `log(1) = 0` at `Y = 1`; for `Y in Q_{>1}` and `kappa in Q cap (0, 1]`,
      `(log Y)^{(4-kappa)/3}` is never a positive integer (Lindemann-Weierstrass), so iterative Arb precision
      refinement certifies the unique floor via `certify_floor_from_arb_enclosure`.
    - For `arb` `Y`: preserves genuine input interval uncertainty `[lo, hi]` (`lo < hi`); refines working precision
      only to reduce `.log()` rounding slack, and raises `AmbiguousCutoffError` if the image straddles an integer.
    """
    if isinstance(Y, float) or isinstance(kappa, float) or isinstance(exact_log_Y, float):
        raise TypeError("Float inputs are forbidden in certified cutoff determination")
    if Y is None and exact_log_Y is None:
        raise ValueError("Must provide either Y or exact_log_Y in certify_D0_small_divisor_cutoff")
    if Y is not None and exact_log_Y is not None:
        raise ValueError("Pass Y=None when supplying exact_log_Y so Y and exact_log_Y cannot conflict")
    kap_f = Fraction(kappa)
    if not (Fraction(0, 1) < kap_f <= Fraction(1, 1)):
        raise ValueError(f"kappa must lie in (0, 1], got {kappa}")
    alpha = (Fraction(4, 1) - kap_f) / Fraction(3, 1)

    if exact_log_Y is not None:
        l_f = Fraction(exact_log_Y)
        if l_f < Fraction(0, 1):
            raise ValueError("exact_log_Y must be >= 0")
        if require_Y_ge_2:
            if l_f <= Fraction(0, 1):
                raise ValueError("exact_log_Y must satisfy exact_log_Y >= log(2) when require_Y_ge_2=True")
            p_cur = max(64, prec_bits)
            saved = flint_ctx.prec
            try:
                separated = False
                while p_cur <= max_prec_bits:
                    flint_ctx.prec = p_cur
                    l_b = _frac_to_arb(l_f)
                    lg2_b = arb(2).log()
                    if bool(l_b.upper() < lg2_b.lower()):
                        raise ValueError(
                            f"exact_log_Y = {l_f} < log(2) violates require_Y_ge_2=True (exp(exact_log_Y) < 2)"
                        )
                    if bool(l_b.lower() >= lg2_b.upper()):
                        separated = True
                        break
                    p_cur *= 2
                if not separated:
                    raise AmbiguousCutoffError(
                        f"Could not separate exact_log_Y = {l_f} from log(2) at {max_prec_bits} bits"
                    )
            finally:
                flint_ctx.prec = saved
        if l_f == Fraction(0, 1):
            return 0
        # Exact rational power (p / q) ** (a / b): k <= (p/q)^{a/b} < k + 1 <=> k^b q^a <= p^a < (k+1)^b q^a
        p_a = l_f.numerator ** alpha.numerator
        q_a = l_f.denominator ** alpha.numerator
        b_exp = alpha.denominator
        # Find k >= 0 with k^b * q_a <= p_a < (k + 1)^b * q_a via exact integer binary search:
        n_ratio = p_a // q_a
        lo_k, hi_k = 0, max(1, n_ratio)
        while lo_k < hi_k:
            mid_k = (lo_k + hi_k + 1) // 2
            if (mid_k ** b_exp) * q_a <= p_a:
                lo_k = mid_k
            else:
                hi_k = mid_k - 1
        assert (lo_k ** b_exp) * q_a <= p_a < ((lo_k + 1) ** b_exp) * q_a
        return lo_k

    if isinstance(Y, arb):
        if not Y.is_finite():
            raise AmbiguousCutoffError(f"Non-finite Y in D_0 certification: {Y}")
        lo_y, hi_y = _exact_arb_endpoints_as_fractions(Y)
        if lo_y == hi_y:
            return certify_D0_small_divisor_cutoff(
                lo_y,
                kappa=kap_f,
                require_Y_ge_2=require_Y_ge_2,
                prec_bits=prec_bits,
                max_prec_bits=max_prec_bits,
            )
        min_req = Fraction(2, 1) if require_Y_ge_2 else Fraction(1, 1)
        if lo_y < min_req:
            raise ValueError(f"Y enclosure {Y} falls below required domain {min_req}")
        p_cur = max(64, prec_bits)
        saved = flint_ctx.prec
        try:
            last_ball = None
            while p_cur <= max_prec_bits:
                flint_ctx.prec = p_cur
                lg_y = Y.log()
                expr_b = lg_y if alpha == Fraction(1, 1) else (lg_y ** _frac_to_arb(alpha))
                last_ball = expr_b
                st, val, _ = classify_floor_from_arb_enclosure(expr_b)
                if st == "CERTIFIED_UNIQUE_FLOOR" and val is not None:
                    return val
                p_cur *= 2
            assert last_ball is not None
            return certify_floor_from_arb_enclosure(last_ball)
        finally:
            flint_ctx.prec = saved

    y_frac = Fraction(Y)
    min_req = Fraction(2, 1) if require_Y_ge_2 else Fraction(1, 1)
    if y_frac < min_req:
        raise ValueError(f"Y = {y_frac} falls below required domain {min_req}")
    if y_frac == Fraction(1, 1):
        return 0
    p_cur = max(64, prec_bits)
    saved = flint_ctx.prec
    try:
        last_ball = None
        while p_cur <= max_prec_bits:
            flint_ctx.prec = p_cur
            y_b = _frac_to_arb(y_frac)
            lg_y = y_b.log()
            expr_b = lg_y if alpha == Fraction(1, 1) else (lg_y ** _frac_to_arb(alpha))
            last_ball = expr_b
            st, val, _ = classify_floor_from_arb_enclosure(expr_b)
            if st == "CERTIFIED_UNIQUE_FLOOR" and val is not None:
                return val
            p_cur *= 2
        assert last_ball is not None
        return certify_floor_from_arb_enclosure(last_ball)
    finally:
        flint_ctx.prec = saved


def certify_T_canonical_cutoff(
    Y: Union[int, Fraction, arb],
    *,
    prec_bits: int = 256,
    max_prec_bits: int = 4096,
) -> int:
    """Certify `T(Y) = ceil(Y^{5/4})` without floating-point integer selection.

    - Exact `int` / `Fraction` `Y >= 0`: uses pure integer arithmetic `(k - 1)^4 q^5 < p^5 <= k^4 q^5`
      (certifying exact fourth-power boundaries such as `Y = 16 -> 32` and `Y = 4096 -> 32768`).
    - Genuine `arb` ball `Y`: preserves input interval uncertainty and raises `AmbiguousCutoffError`
      if `Y^{5/4}` straddles an integer.
    """
    if isinstance(Y, float):
        raise TypeError("Float inputs are forbidden in certified cutoff determination")
    if isinstance(Y, arb):
        if not Y.is_finite():
            raise AmbiguousCutoffError(f"Non-finite Y in T(Y) certification: {Y}")
        lo_y, hi_y = _exact_arb_endpoints_as_fractions(Y)
        if lo_y == hi_y:
            return certify_T_canonical_cutoff(lo_y, prec_bits=prec_bits, max_prec_bits=max_prec_bits)
        if lo_y < Fraction(0, 1):
            raise ValueError(f"Y enclosure {Y} must be >= 0")
        p_cur = max(64, prec_bits)
        saved = flint_ctx.prec
        try:
            last_ball = None
            while p_cur <= max_prec_bits:
                flint_ctx.prec = p_cur
                expr_b = Y ** (arb(5) / arb(4))
                last_ball = expr_b
                st, val, _ = classify_ceil_from_arb_enclosure(expr_b)
                if st == "CERTIFIED_UNIQUE_CEIL" and val is not None:
                    return val
                p_cur *= 2
            assert last_ball is not None
            return certify_ceil_from_arb_enclosure(last_ball)
        finally:
            flint_ctx.prec = saved

    y_frac = Fraction(Y)
    if y_frac < Fraction(0, 1):
        raise ValueError(f"Y = {y_frac} must be >= 0")
    if y_frac == Fraction(0, 1):
        return 0
    p5 = y_frac.numerator ** 5
    q5 = y_frac.denominator ** 5
    n_floor = (p5 - 1) // q5
    k = math.isqrt(math.isqrt(n_floor)) + 1
    assert ((k - 1) ** 4) * q5 < p5 <= (k ** 4) * q5
    return k


def certify_ceil_tau_Y_cutoff(
    Y: Union[int, Fraction, arb],
    *,
    prec_bits: int = 256,
    max_prec_bits: int = 4096,
) -> int:
    """Certify `ceil(tau * Y)` without floating-point integer selection."""
    if isinstance(Y, float):
        raise TypeError("Float inputs are forbidden in certified cutoff determination")
    if isinstance(Y, arb):
        if not Y.is_finite():
            raise AmbiguousCutoffError(f"Non-finite Y in ceil(tau*Y) certification: {Y}")
        lo_y, hi_y = _exact_arb_endpoints_as_fractions(Y)
        if lo_y == hi_y:
            return certify_ceil_tau_Y_cutoff(lo_y, prec_bits=prec_bits, max_prec_bits=max_prec_bits)
        if lo_y < Fraction(0, 1):
            raise ValueError(f"Y enclosure {Y} must be >= 0")
        p_cur = max(64, prec_bits)
        saved = flint_ctx.prec
        try:
            last_ball = None
            while p_cur <= max_prec_bits:
                flint_ctx.prec = p_cur
                expr_b = _tau_arb() * Y
                last_ball = expr_b
                st, val, _ = classify_ceil_from_arb_enclosure(expr_b)
                if st == "CERTIFIED_UNIQUE_CEIL" and val is not None:
                    return val
                p_cur *= 2
            assert last_ball is not None
            return certify_ceil_from_arb_enclosure(last_ball)
        finally:
            flint_ctx.prec = saved

    y_frac = Fraction(Y)
    if y_frac < Fraction(0, 1):
        raise ValueError(f"Y = {y_frac} must be >= 0")
    if y_frac == Fraction(0, 1):
        return 0
    p_cur = max(64, prec_bits)
    saved = flint_ctx.prec
    try:
        last_ball = None
        while p_cur <= max_prec_bits:
            flint_ctx.prec = p_cur
            expr_b = _tau_arb() * _frac_to_arb(y_frac)
            last_ball = expr_b
            st, val, _ = classify_ceil_from_arb_enclosure(expr_b)
            if st == "CERTIFIED_UNIQUE_CEIL" and val is not None:
                return val
            p_cur *= 2
        assert last_ball is not None
        return certify_ceil_from_arb_enclosure(last_ball)
    finally:
        flint_ctx.prec = saved


def certify_open_core_divisor_partition(
    Y: Union[int, Fraction, arb],
    *,
    kappa: Union[int, Fraction] = 1,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """O(1) exact/certified partition of `{1, ..., T(Y)-1}` into the small-divisor slice
    `1 <= d <= min(D_0(Y), T(Y)-1)` and the **full open core** `min(D_0(Y), T(Y)-1) < d <= T(Y)-1`
    (matching Lean `openCoreOscShiftD2Part`), plus the internal intermediate-band / `d >= ceil(tau*Y)`
    sub-partition within the open core without allocating O(T^2) Gram arrays.
    """
    T_y = certify_T_canonical_cutoff(Y, prec_bits=prec_bits)
    D0_raw = certify_D0_small_divisor_cutoff(Y, kappa=kappa, require_Y_ge_2=True, prec_bits=prec_bits)
    ceil_tau_y = certify_ceil_tau_Y_cutoff(Y, prec_bits=prec_bits)
    max_d = max(0, T_y - 1)
    eff_D0 = min(D0_raw, max_d)

    small_lo, small_hi = 1, eff_D0
    small_count = max(0, small_hi - small_lo + 1)

    core_lo, core_hi = eff_D0 + 1, max_d
    core_count = max(0, core_hi - core_lo + 1)

    inter_lo = core_lo
    inter_hi = min(max_d, ceil_tau_y - 1)
    inter_count = max(0, inter_hi - inter_lo + 1)

    tail_lo = max(core_lo, ceil_tau_y)
    tail_hi = max_d
    tail_count = max(0, tail_hi - tail_lo + 1)

    partition_exact = bool(
        small_count + core_count == max_d
        and inter_count + tail_count == core_count
        and (tail_count == 0 or (inter_hi + 1 == tail_lo or inter_count == 0))
    )
    return {
        "T_Y": T_y,
        "D_0_raw": D0_raw,
        "effective_D_0_min_D0_Tm1": eff_D0,
        "ceil_tau_Y": ceil_tau_y,
        "full_divisor_count_1_to_Tm1": max_d,
        "small_slice_range_inclusive": [small_lo, small_hi] if small_count > 0 else [],
        "small_slice_count": small_count,
        "small_slice_is_empty": small_count == 0,
        "full_open_core_range_inclusive": [core_lo, core_hi] if core_count > 0 else [],
        "full_open_core_count": core_count,
        "intermediate_band_within_open_core_inclusive": [inter_lo, inter_hi] if inter_count > 0 else [],
        "intermediate_band_count": inter_count,
        "sub_unit_tail_ge_ceil_tau_Y_within_open_core_inclusive": (
            [tail_lo, tail_hi] if tail_count > 0 else []
        ),
        "sub_unit_tail_count": tail_count,
        "sub_unit_tail_nonempty": tail_count > 0,
        "both_intermediate_and_tail_retained_in_open_core": True,
        "partition_identities_verified": partition_exact,
    }


def _to_arb_val(x: Union[int, Fraction, arb], prec_bits: int = 256) -> arb:
    if isinstance(x, arb):
        return x
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        if isinstance(x, Fraction):
            return _frac_to_arb(x)
        return arb(x)
    finally:
        flint_ctx.prec = saved


def evaluate_c_half_square_pole_arb(prec_bits: int = 256) -> arb:
    """Certified 256-bit Arb evaluation of the `z = 1/2` square-pole constant in `R(d)`:
    `c_{1/2, lambda} = 4 * zeta'(1/2) / zeta(1/2) - 8 - 8 * gamma_E`.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        gamma_e = arb.const_euler()
        z_ser = acb_series([acb(arb(1) / arb(2)), acb(1)], prec=prec_bits).zeta()
        zeta_ratio_half = z_ser[1].real / z_ser[0].real
        return arb(4) * zeta_ratio_half - arb(8) - arb(8) * gamma_e
    finally:
        flint_ctx.prec = saved


def evaluate_square_pole_drift_M_arb(
    d: int,
    c_half_arb: Optional[arb] = None,
    prec_bits: int = 256,
) -> arb:
    """Deterministic `z = 1/2` square-pole drift `M_{sq,2}(d) = 4*sqrt(d)*log(d) + c_{1/2,lambda}*sqrt(d)`
    for `d >= 1` (`0` at `d = 0`).
    """
    if d < 0:
        raise ValueError("d must be >= 0")
    if d == 0:
        return arb(0)
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        ch = evaluate_c_half_square_pole_arb(prec_bits) if c_half_arb is None else c_half_arb
        d_arb = arb(d)
        sd = d_arb.sqrt()
        return arb(4) * sd * d_arb.log() + ch * sd
    finally:
        flint_ctx.prec = saved


def compute_selberg_centered_remainder_table_arb(
    T_max: int,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Compute certified tables of `w_{2,lambda}(d)`, `W_2(d)`, `R(d) = W_2(d) - c_lambda*d`,
    `M_{sq,2}(d)`, and `R_{osc}(d) = R(d) - M_{sq,2}(d)` on `0 <= d <= T_max`.
    """
    if T_max < 0:
        raise ValueError("T_max must be >= 0")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        c_lam = evaluate_c_lambda_arb(prec_bits)
        c_half = evaluate_c_half_square_pole_arb(prec_bits)
        w2 = [arb(0)] * (T_max + 1)
        W2 = [arb(0)] * (T_max + 1)
        R = [arb(0)] * (T_max + 1)
        M_drift = [arb(0)] * (T_max + 1)
        R_osc = [arb(0)] * (T_max + 1)
        cum = arb(0)
        for d in range(1, T_max + 1):
            if d >= 2:
                wd = selberg_w2_weight_arb(d, mode="liouville")
                w2[d] = wd
                cum = cum + wd
            W2[d] = cum
            R[d] = cum - c_lam * arb(d)
            md = evaluate_square_pole_drift_M_arb(d, c_half_arb=c_half, prec_bits=prec_bits)
            M_drift[d] = md
            R_osc[d] = R[d] - md
        return {
            "c_lambda": c_lam,
            "c_half_lambda": c_half,
            "w2": w2,
            "W2": W2,
            "R": R,
            "M_drift": M_drift,
            "R_osc": R_osc,
        }
    finally:
        flint_ctx.prec = saved


def evaluate_smooth_jump_endpoint_reconstruction_arb(
    X: Union[int, Fraction, arb],
    T: int,
    R_table: Optional[Sequence[arb]] = None,
    inner_coeff_fn: Callable[[int], int] = liouville_lambda_int,
    prec_bits: int = 256,
) -> Dict[str, arb]:
    """Evaluate `r_{sm,T}(X)`, `r_{jump,T}(X)`, and `End_T(X)` from source definitions:
    - At `T = 0`, returns `0` for all components without ever calling `evaluate_phi_n_arb(..., 0)`.
    - At `T >= 1`, evaluates `r_{sm,T} = sum_{d=1}^{T-1} R(d)*Delta_d^{sm}`,
      `r_{jump,T} = sum_{d=1}^{T-1} R(d)*Delta_d^{jump}`, and `End_T = R(T)*phi_T(X)*a(1)` (`a(1)=1`).
    """
    if T < 0:
        raise ValueError("T must be >= 0")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        if T == 0:
            z0 = arb(0)
            return {
                "r_sm": z0,
                "r_jump": z0,
                "endpoint": z0,
                "total_reassembled": z0,
            }
        x_arb = _to_arb_val(X, prec_bits=prec_bits)
        R_seq = (
            compute_selberg_centered_remainder_table_arb(T, prec_bits=prec_bits)["R"]
            if R_table is None
            else R_table
        )
        r_sm = arb(0)
        r_jump = arb(0)
        for d in range(1, T):
            L_d = T // d
            L_d1 = T // (d + 1)
            d_arb = arb(d)
            d1_arb = arb(d + 1)
            q_ld_at_d = evaluate_Q_general_arb(
                x_arb / d_arb, L_d, coeff_fn=inner_coeff_fn, prec_bits=prec_bits
            )
            q_ld_at_d1 = evaluate_Q_general_arb(
                x_arb / d1_arb, L_d, coeff_fn=inner_coeff_fn, prec_bits=prec_bits
            )
            q_ld1_at_d1 = evaluate_Q_general_arb(
                x_arb / d1_arb, L_d1, coeff_fn=inner_coeff_fn, prec_bits=prec_bits
            )
            delta_sm = q_ld_at_d / d_arb.sqrt() - q_ld_at_d1 / d1_arb.sqrt()
            delta_jump = (q_ld_at_d1 - q_ld1_at_d1) / d1_arb.sqrt()
            r_sm += R_seq[d] * delta_sm
            r_jump += R_seq[d] * delta_jump
        endpt = R_seq[T] * arb(inner_coeff_fn(1)) * evaluate_phi_n_arb(x_arb, T, prec_bits=prec_bits)
        return {
            "r_sm": r_sm,
            "r_jump": r_jump,
            "endpoint": endpt,
            "total_reassembled": r_sm + r_jump + endpt,
        }
    finally:
        flint_ctx.prec = saved


def compute_smooth_basis_coefficients_arb(
    T: int,
    R_table: Optional[Sequence[arb]] = None,
    inner_coeff_fn: Callable[[int], int] = liouville_lambda_int,
    prec_bits: int = 256,
) -> List[arb]:
    """Compute exact `phi_n(X)` basis coefficients `alpha_T(n)` (`0 <= n <= 2*T`) of `r_{sm,T}(X)`."""
    if T < 0:
        raise ValueError("T must be >= 0")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        alpha = [arb(0)] * (2 * T + 1)
        if T <= 1:
            return alpha
        R_seq = (
            compute_selberg_centered_remainder_table_arb(T, prec_bits=prec_bits)["R"]
            if R_table is None
            else R_table
        )
        for d in range(1, T):
            Rd = R_seq[d]
            L_d = T // d
            for q in range(1, L_d + 1):
                aq = arb(inner_coeff_fn(q))
                alpha[d * q] += Rd * aq
                alpha[(d + 1) * q] -= Rd * aq
        return alpha
    finally:
        flint_ctx.prec = saved


def evaluate_qhat_L_closed_acb(
    L: int,
    v: Union[int, Fraction, arb],
    coeff_fn: Callable[[int], int] = liouville_lambda_int,
    prec_bits: int = 256,
) -> acb:
    """Closed-form finite-cutoff Fourier transform:
    `qhat_L(v) = (1/2) * Gamma(5/4 - i*v/2) * sum_{n=1}^L a(n) * n^{-1/2 - i*v}`.
    """
    if L < 1:
        return acb(0)
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        v_arb = _to_arb_val(v, prec_bits=prec_bits)
        gamma_arg = acb(arb(5) / arb(4), -v_arb / arb(2))
        gamma_val = gamma_arg.gamma()
        dir_sum = acb(0)
        exp_w = acb(-arb(1) / arb(2), -v_arb)
        for n in range(1, L + 1):
            an = coeff_fn(n)
            if an != 0:
                dir_sum += acb(an) * (acb(n) ** exp_w)
        return (acb(1) / acb(2)) * gamma_val * dir_sum
    finally:
        flint_ctx.prec = saved


def evaluate_qhat_L_direct_quadrature_acb(
    L: int,
    v: Union[int, Fraction, arb],
    coeff_fn: Callable[[int], int] = liouville_lambda_int,
    prec_bits: int = 256,
) -> acb:
    """Direct certified real-line Fourier integral `int_{-infty}^{+infty} q_L(t) exp(-i*v*t) dt`
    for `|a(n)| <= 1` (`L >= 1`):
    - Truncates to `[t_lo, t_hi]` with `t_lo = -80` and `t_hi = log(18*L)`;
    - Certified left tail on `(-infty, t_lo]`: `|q_L(t)| <= (sum_{n<=L} n^{-3}) exp(5t/2) <= (3/2) exp(5t/2)`
      implies `|int_{-infty}^{t_lo} ...| <= (3/5) exp(5*t_lo/2)`;
    - Certified right tail on `[t_hi, +infty)` (`X = exp(t) >= 18*L >= 18*n`): using `(X/n)^2 exp(-(X/n)^2/4) <= 4/e`,
      `|int_{t_hi}^{+infty} ...| <= (sum_{n<=L} n^{-1/2}) * (8/(3*e)) * exp(-243)`.
    """
    if L < 1:
        return acb(0)
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        v_arb = _to_arb_val(v, prec_bits=prec_bits)
        v_c = acb(v_arb)
        coeffs = [0] + [int(coeff_fn(n)) for n in range(1, L + 1)]
        if any(abs(c) > 1 for c in coeffs[1:]):
            raise ValueError("Analytic tail majorant assumes |a(n)| <= 1")
        t_lo = arb(-80)
        t_hi = arb(18 * L).log()

        def _integrand(t_c: acb, _analytic: bool) -> acb:
            x_c = t_c.exp()
            x2 = x_c * x_c
            x_5_2 = (acb(arb(5) / arb(2)) * t_c).exp()
            acc = acb(0)
            for n in range(1, L + 1):
                cn = coeffs[n]
                if cn != 0:
                    nc = acb(n)
                    acc += acb(cn) * (nc ** (-3)) * (-x2 / (nc * nc)).exp()
            return x_5_2 * acc * (acb(0, -1) * v_c * t_c).exp()

        mid_int = acb.integral(
            _integrand,
            acb(t_lo),
            acb(t_hi),
            rel_tol=2 ** (-prec_bits + 14),
            abs_tol=2 ** (-prec_bits + 14),
        )
        left_rad = (arb(3) / arb(5)) * (arb(5) * t_lo / arb(2)).exp()
        sum_inv_sqrt = sum((arb(1) / arb(n).sqrt() for n in range(1, L + 1)), arb(0))
        right_rad = sum_inv_sqrt * (arb(8) / (arb(3) * arb(1).exp())) * (-arb(243)).exp()
        tot_rad = (left_rad + right_rad).upper()
        tail_ball = acb(arb(0, tot_rad), arb(0, tot_rad))
        return mid_int + tail_ball
    finally:
        flint_ctx.prec = saved


def evaluate_adjacent_multiplier_m_d_acb(
    d: int,
    v: Union[int, Fraction, arb],
    prec_bits: int = 256,
) -> acb:
    """Adjacent dilation multiplier `m_d(v) = d^{-1/2} exp(-i*v*log d) - (d+1)^{-1/2} exp(-i*v*log(d+1))`."""
    if d < 1:
        raise ValueError("d must be >= 1")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        v_arb = _to_arb_val(v, prec_bits=prec_bits)
        d_arb = arb(d)
        d1_arb = arb(d + 1)
        t1 = acb(arb(1) / d_arb.sqrt()) * acb(arb(0), -v_arb * d_arb.log()).exp()
        t2 = acb(arb(1) / d1_arb.sqrt()) * acb(arb(0), -v_arb * d1_arb.log()).exp()
        return t1 - t2
    finally:
        flint_ctx.prec = saved


def cutoff_level_blocks_exact(T: int) -> Dict[int, List[int]]:
    """Exact cutoff level-set blocks `I_L(T) = {1 <= d < T : T // d == L}` for `1 <= L <= T`
    (retaining empty blocks explicitly).
    """
    if T < 0:
        raise ValueError("T must be >= 0")
    blocks: Dict[int, List[int]] = {L: [] for L in range(1, T + 1)}
    for d in range(1, T):
        L = T // d
        blocks[L].append(d)
    return blocks


def evaluate_signed_gram_H_closed_arb(
    Y: Union[int, Fraction, arb],
    d: int,
    e: int,
    T: int,
    base_mult: Optional[arb] = None,
    inner_coeff_fn: Callable[[int], int] = liouville_lambda_int,
    prec_bits: int = 256,
) -> arb:
    """Closed-form evaluation of `H_{Y, b}(d, e) = <Delta_d^{sm}, Delta_e^{sm}>_{Y, b}`."""
    if d < 1 or e < 1 or T < 1:
        return arb(0)
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        y_arb = _to_arb_val(Y, prec_bits=prec_bits)
        L_d = T // d
        L_e = T // e
        if L_d < 1 or L_e < 1:
            return arb(0)
        acc = arb(0)
        for q in range(1, L_d + 1):
            aq = inner_coeff_fn(q)
            if aq == 0:
                continue
            for r in range(1, L_e + 1):
                ar = inner_coeff_fn(r)
                if ar == 0:
                    continue
                k00 = evaluate_window_kernel_K_closed_arb(
                    y_arb, d * q, e * r, base_mult=base_mult, prec_bits=prec_bits
                )
                k10 = evaluate_window_kernel_K_closed_arb(
                    y_arb, (d + 1) * q, e * r, base_mult=base_mult, prec_bits=prec_bits
                )
                k01 = evaluate_window_kernel_K_closed_arb(
                    y_arb, d * q, (e + 1) * r, base_mult=base_mult, prec_bits=prec_bits
                )
                k11 = evaluate_window_kernel_K_closed_arb(
                    y_arb, (d + 1) * q, (e + 1) * r, base_mult=base_mult, prec_bits=prec_bits
                )
                acc += arb(aq * ar) * (k00 - k10 - k01 + k11)
        return acc
    finally:
        flint_ctx.prec = saved


def evaluate_weighted_window_kernel_K_quadrature_arb(
    Y: Union[int, Fraction, arb],
    m: int,
    n: int,
    base_mult: Optional[arb] = None,
    prec_bits: int = 256,
) -> arb:
    """Certified quadrature of `K_{Y, b}^{wt}(m, n) = int_Y^{b*Y} phi_m(X)*phi_n(X) dX / (X * (log X)^4)`
    for `Y >= 2` and `b > 1` (keeping `(log X)^{-2}` inside the integral).
    """
    if m < 1 or n < 1:
        return arb(0)
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        y_arb = _to_arb_val(Y, prec_bits=prec_bits)
        if not bool(y_arb >= arb(2)):
            raise ValueError("Weighted log kernel requires Y >= 2 so log X > 0 on [Y, b*Y]")
        b_mult = _tau_arb() if base_mult is None else base_mult
        alpha = acb(1) / acb(m * m) + acb(1) / acb(n * n)
        pref = arb(1) / ((arb(m) ** 3) * (arb(n) ** 3))

        def _integrand(z: acb, _analytic: bool) -> acb:
            if _analytic and not bool(z.real > arb(1)):
                nan_b = arb("nan")
                return acb(nan_b, nan_b)
            lg = z.log(analytic=_analytic)
            return (z ** 4) * (-alpha * z * z).exp() / (lg ** 4)

        return pref * _acb_integral_certified_arb(_integrand, y_arb, b_mult * y_arb, prec_bits=prec_bits)
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 1. Section 1: Exact Object Recovery & Non-Circularity Reassembly
# ---------------------------------------------------------------------------


def verify_section_1_exact_object_and_noncircular_reassembly(prec_bits: int = 256) -> Dict[str, Any]:
    """Verify `R(0)=0`, `R(1)=-c_lambda`, `T=0, 1` boundary conventions (never calling `phi_0`),
    general `T >= 1` reassembly, exact match to `D_{2,Y} = P_Y - R_Y`, and `1 <= n <= 2T` basis
    stratification of `r_{sm,T}`.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tbl = compute_selberg_centered_remainder_table_arb(80, prec_bits=prec_bits)
        c_lam = tbl["c_lambda"]
        R = tbl["R"]
        w2 = tbl["w2"]

        # Verify R(0) = 0, R(1) = -c_lambda > 0, and R(d) - R(d-1) = w_{2,lambda}(d) - c_lambda:
        r0_exact = R[0] == arb(0)
        r1_diff = R[1] - (-c_lam)
        r1_pos = bool(R[1] > arb(0))
        inc_max_res = arb(0)
        inc_ok = bool(r0_exact and arb(0) in r1_diff and abs(r1_diff) < arb("1e-74") and r1_pos)
        for d in range(1, 65):
            res_d = (R[d] - R[d - 1]) - (w2[d] - c_lam)
            if not bool(arb(0) in res_d and abs(res_d) < arb("1e-72")):
                inc_ok = False
            if bool(abs(res_d) > inc_max_res):
                inc_max_res = abs(res_d)

        # Explicitly guard against phi_0 evaluation at T = 0:
        phi0_guard_ok = True
        rec_T0 = evaluate_smooth_jump_endpoint_reconstruction_arb(
            Fraction(5, 2), 0, R_table=R, prec_bits=prec_bits
        )
        if not all(rec_T0[k] == arb(0) for k in ("r_sm", "r_jump", "endpoint", "total_reassembled")):
            phi0_guard_ok = False

        # T = 1 check: r_sm = 0, r_jump = 0, endpoint = -c_lambda * phi_1(X) = 0 - c_lambda * Q_{1_sq, 1}(X)
        x_t1 = _frac_to_arb(Fraction(5, 2))
        rec_T1 = evaluate_smooth_jump_endpoint_reconstruction_arb(
            x_t1, 1, R_table=R, prec_bits=prec_bits
        )
        phi1_x = evaluate_phi_n_arb(x_t1, 1, prec_bits=prec_bits)
        t1_res = rec_T1["total_reassembled"] - (-c_lam * phi1_x)
        t1_ok = bool(
            rec_T1["r_sm"] == arb(0)
            and rec_T1["r_jump"] == arb(0)
            and arb(0) in t1_res
            and abs(t1_res) < arb("1e-74")
        )

        # General T >= 1 reassembly and D_{2,Y} = P_Y - R_Y audit across integer & noninteger X >= 2:
        reassembly_rows: List[Dict[str, Any]] = []
        reassembly_ok = True
        test_cases = (
            (1, Fraction(2, 1)),
            (2, Fraction(5, 2)),
            (5, Fraction(4, 1)),
            (16, Fraction(33, 4)),
            (32, Fraction(16, 1)),
            (64, Fraction(65, 2)),
        )
        for T_val, x_frac in test_cases:
            x_arb = _frac_to_arb(x_frac)
            lg_x = x_arb.log()
            rec = evaluate_smooth_jump_endpoint_reconstruction_arb(
                x_arb, T_val, R_table=R, prec_bits=prec_bits
            )
            selberg_sum_rhs = arb(0)
            q_sq_rhs = arb(0)
            for n in range(1, T_val + 1):
                phi_n = evaluate_phi_n_arb(x_arb, n, prec_bits=prec_bits)
                ln = arb(n).log()
                selberg_sum_rhs += arb(liouville_lambda_int(n)) * (ln * ln) * phi_n
                if is_perfect_square_int(n):
                    q_sq_rhs += phi_n
            expected_rhs = selberg_sum_rhs - c_lam * q_sq_rhs
            reasm_res = rec["total_reassembled"] - expected_rhs

            # Relate directly to D_{2,T}(X) = P_T(X) - R_T(X) and Q_{lambda,T}(X) = 2*P_T(X) - D_{2,T}(X):
            q_lam = evaluate_Q_general_arb(x_arb, T_val, coeff_fn=liouville_lambda_int, prec_bits=prec_bits)
            q_sh1 = evaluate_Q_shifted_finite_arb(x_arb, T_val, m_shift=1, mode="liouville", prec_bits=prec_bits)
            q_sh2 = evaluate_Q_shifted_finite_arb(x_arb, T_val, m_shift=2, mode="liouville", prec_bits=prec_bits)
            R_term = q_sh1 / lg_x
            P_term = q_lam - R_term
            D2_from_reasm = (
                c_lam * q_sq_rhs + rec["r_sm"] + rec["r_jump"] + rec["endpoint"] - q_sh2
            ) / (lg_x * lg_x)
            d2_res = (P_term - R_term) - D2_from_reasm
            q_elim_res = q_lam - (arb(2) * P_term - D2_from_reasm)
            row_ok = bool(
                arb(0) in reasm_res
                and abs(reasm_res) < arb("1e-68")
                and arb(0) in d2_res
                and abs(d2_res) < arb("1e-68")
                and arb(0) in q_elim_res
                and abs(q_elim_res) < arb("1e-68")
            )
            reassembly_ok = reassembly_ok and row_ok
            reassembly_rows.append(
                {
                    "T": T_val,
                    "X_fraction": f"{x_frac.numerator}/{x_frac.denominator}",
                    "r_sm": serialize_arb_certified(rec["r_sm"]),
                    "r_jump": serialize_arb_certified(rec["r_jump"]),
                    "endpoint_R_T_phi_T": serialize_arb_certified(rec["endpoint"]),
                    "reassembly_residual": serialize_arb_certified(reasm_res),
                    "D2_from_reassembly": serialize_arb_certified(D2_from_reasm),
                    "P_minus_R_minus_D2_residual": serialize_arb_certified(d2_res),
                    "Q_minus_2P_plus_D2_residual": serialize_arb_certified(q_elim_res),
                    "verified": row_ok,
                }
            )

        # Basis stratification check on T in {2, 8, 32}:
        strat_rows: List[Dict[str, Any]] = []
        strat_ok = True
        for T_s in (2, 8, 32):
            alpha = compute_smooth_basis_coefficients_arb(T_s, R_table=R, prec_bits=prec_bits)
            x_chk = arb(max(2, T_s // 2))
            r_sm_direct = evaluate_smooth_jump_endpoint_reconstruction_arb(
                x_chk, T_s, R_table=R, prec_bits=prec_bits
            )["r_sm"]
            r_sm_basis = sum(
                (
                    alpha[n] * evaluate_phi_n_arb(x_chk, n, prec_bits=prec_bits)
                    for n in range(1, 2 * T_s + 1)
                ),
                arb(0),
            )
            basis_res = r_sm_direct - r_sm_basis
            max_head_res = arb(0)
            head_ok = True
            for n in range(1, T_s):
                sq_ind = arb(1) if is_perfect_square_int(n) else arb(0)
                exp_n = arb(liouville_lambda_int(n)) * (arb(n).log() ** 2) - c_lam * sq_ind
                dn = alpha[n] - exp_n
                if not bool(arb(0) in dn and abs(dn) < arb("1e-70")):
                    head_ok = False
                if bool(abs(dn) > max_head_res):
                    max_head_res = abs(dn)
            sq_T = arb(1) if is_perfect_square_int(T_s) else arb(0)
            exp_T = arb(liouville_lambda_int(T_s)) * (arb(T_s).log() ** 2) - c_lam * sq_T - R[T_s]
            res_T = alpha[T_s] - exp_T
            exp_2T = c_lam * arb(liouville_lambda_int(T_s))
            res_2T = alpha[2 * T_s] - exp_2T
            top_nonzero = bool(abs(alpha[2 * T_s]) > arb(3))
            ok_s = bool(
                head_ok
                and arb(0) in basis_res
                and abs(basis_res) < arb("1e-68")
                and arb(0) in res_T
                and abs(res_T) < arb("1e-70")
                and arb(0) in res_2T
                and abs(res_2T) < arb("1e-70")
                and top_nonzero
            )
            strat_ok = strat_ok and ok_s
            strat_rows.append(
                {
                    "T": T_s,
                    "max_head_1_to_Tm1_selberg_match_residual": serialize_arb_certified(max_head_res),
                    "alpha_at_T_endpoint_shift_residual": serialize_arb_certified(res_T),
                    "alpha_at_2T": serialize_arb_certified(alpha[2 * T_s]),
                    "alpha_at_2T_minus_c_lambda_lambda_T_residual": serialize_arb_certified(res_2T),
                    "basis_sum_vs_r_sm_residual": serialize_arb_certified(basis_res),
                    "top_spillover_2T_strictly_nonzero": top_nonzero,
                    "verified": ok_s,
                }
            )

        all_sec1 = bool(inc_ok and phi0_guard_ok and t1_ok and reassembly_ok and strat_ok)
        return {
            "epistemic_status": "CONCRETE_ANALYTIC_IN_LEAN",
            "lean_theorem": "noncircular_reassembly_and_basis_stratification_tc060",
            "c_lambda": serialize_arb_certified(c_lam),
            "R_0_is_exact_zero": r0_exact,
            "R_1_equals_minus_c_lambda": serialize_arb_certified(R[1]),
            "R_1_strictly_positive": r1_pos,
            "increment_max_residual_1_to_64": serialize_arb_certified(inc_max_res),
            "T_0_empty_without_phi_0_verified": phi0_guard_ok,
            "T_1_boundary_residual": serialize_arb_certified(t1_res),
            "reassembly_and_D2_rows": reassembly_rows,
            "basis_stratification_rows": strat_rows,
            "noncircularity_audit_conclusion": (
                "Reassembling r_{sm,T} + r_{jump,T} + R(T)*phi_T returns identically to "
                "sum_{n<=T} lambda(n)*(log n)^2*phi_n - c_lambda*Q_{1_sq,T}; on 1 <= n <= T - 1, r_{sm,T} "
                "carries the exact un-cancelled Selberg coefficient while spilling onto T + 1 <= n <= 2T "
                "with unique top coefficient alpha_T(2T) = c_lambda*lambda(T) != 0. Exact return to D_{2,Y} "
                "is a consistency audit, not a new cancellation theorem."
            ),
            "all_section_1_checks_pass": all_sec1,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 2. Section 2: Signed Dilation Fourier, Multiplier Attainment, Blocks, & Gram
# ---------------------------------------------------------------------------


def verify_section_2_signed_dilation_fourier_and_gram_kernel(prec_bits: int = 256) -> Dict[str, Any]:
    """Verify finite-cutoff `qhat_L(v)` against certified improper real-line quadrature, certify the
    adjacent dilation multiplier benchmark & unrestricted-frequency attainment, verify exact cutoff
    blocks `I_L(T)` & `Fourier[r_sm(exp t)](v)`, and cross-check `H_{Y,b}` and `H_{Y,b}^{wt}`.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        tbl = compute_selberg_centered_remainder_table_arb(40, prec_bits=prec_bits)
        R = tbl["R"]

        # 2A. Finite-cutoff qhat_L(v) closed form vs direct t-quadrature + certified analytic tails:
        qhat_rows: List[Dict[str, Any]] = []
        qhat_ok = True
        for L_val, v_frac in (
            (1, Fraction(0, 1)),
            (4, Fraction(1, 3)),
            (8, Fraction(3, 2)),
            (12, Fraction(-5, 2)),
            (16, Fraction(4, 1)),
        ):
            qh_closed = evaluate_qhat_L_closed_acb(L_val, v_frac, prec_bits=prec_bits)
            qh_quad = evaluate_qhat_L_direct_quadrature_acb(L_val, v_frac, prec_bits=prec_bits)
            diff_c = qh_closed - qh_quad
            abs_diff = abs(diff_c)
            ok_q = bool(
                arb(0) in diff_c.real
                and arb(0) in diff_c.imag
                and abs_diff < arb("1e-65")
            )
            qhat_ok = qhat_ok and ok_q
            qhat_rows.append(
                {
                    "L": L_val,
                    "v_fraction": f"{v_frac.numerator}/{v_frac.denominator}",
                    "qhat_closed_re": serialize_arb_certified(qh_closed.real),
                    "qhat_closed_im": serialize_arb_certified(qh_closed.imag),
                    "qhat_quadrature_re": serialize_arb_certified(qh_quad.real),
                    "qhat_quadrature_im": serialize_arb_certified(qh_quad.imag),
                    "abs_closed_minus_quadrature_residual": serialize_arb_certified(abs_diff),
                    "verified": ok_q,
                }
            )

        # 2B. Adjacent dilation multiplier benchmark + sharp unrestricted-frequency attainment:
        mult_bench_rows: List[Dict[str, Any]] = []
        mult_ok = True
        for d_val in (1, 2, 4, 16, 64):
            d_arb = arb(d_val)
            d1_arb = arb(d_val + 1)
            int_t_m32 = arb(2) * (arb(1) / d_arb.sqrt() - arb(1) / d1_arb.sqrt())
            sup_bound = arb(1) / d_arb.sqrt() + arb(1) / d1_arb.sqrt()
            for v_frac in (Fraction(0, 1), Fraction(1, 4), Fraction(2, 1), Fraction(12, 1)):
                v_arb = _frac_to_arb(v_frac)
                md_abs = abs(evaluate_adjacent_multiplier_m_d_acb(d_val, v_arb, prec_bits=prec_bits))
                deriv_bound = (arb(1) / arb(4) + v_arb * v_arb).sqrt() * int_t_m32
                rhs_min = sup_bound if bool(sup_bound < deriv_bound) else deriv_bound
                eq_at_v0 = v_frac == Fraction(0, 1)
                cert_status, cert_pass = classify_arb_le_certificate(
                    md_abs, rhs_min, exact_algebraic_equality_justified=eq_at_v0
                )
                mult_ok = mult_ok and cert_pass
                if d_val in (1, 16) and v_frac in (Fraction(0, 1), Fraction(1, 4), Fraction(12, 1)):
                    mult_bench_rows.append(
                        {
                            "d": d_val,
                            "v_fraction": f"{v_frac.numerator}/{v_frac.denominator}",
                            "abs_m_d": serialize_arb_certified(md_abs),
                            "benchmark_min_rhs": serialize_arb_certified(rhs_min),
                            "certificate_status": cert_status,
                            "verified": cert_pass,
                        }
                    )

        attainment_rows: List[Dict[str, Any]] = []
        for d_val in (1, 2, 8, 32, 128):
            d_arb = arb(d_val)
            d1_arb = arb(d_val + 1)
            sup_exact = arb(1) / d_arb.sqrt() + arb(1) / d1_arb.sqrt()
            lg_ratio = (d1_arb / d_arb).log()
            for k_int in (0, 1, -1):
                v_res = arb(2 * k_int + 1) * tau / (arb(2) * lg_ratio)
                md_res_abs = abs(evaluate_adjacent_multiplier_m_d_acb(d_val, v_res, prec_bits=prec_bits))
                att_diff = md_res_abs - sup_exact
                ok_att = bool(arb(0) in att_diff and abs(att_diff) < arb("1e-70"))
                mult_ok = mult_ok and ok_att
                if k_int == 0:
                    attainment_rows.append(
                        {
                            "d": d_val,
                            "v_0_d": serialize_arb_certified(v_res),
                            "abs_m_d_at_v_0": serialize_arb_certified(md_res_abs),
                            "d_inv_sqrt_plus_d1_inv_sqrt": serialize_arb_certified(sup_exact),
                            "attainment_residual": serialize_arb_certified(att_diff),
                            "verified": ok_att,
                        }
                    )

        # 2C. Cutoff level-set blocks I_L(T) & Fourier[r_sm(exp t)](v) = sum_{L=1}^T M_{L,T}(v)*qhat_L(v):
        block_rows: List[Dict[str, Any]] = []
        blocks_ok = True
        for T_b in (1, 2, 6, 32, 1024):
            blks = cutoff_level_blocks_exact(T_b)
            all_d = [d for L in range(1, T_b + 1) for d in blks[L]]
            nonempty_cnt = sum(1 for L in range(1, T_b + 1) if len(blks[L]) > 0)
            empty_cnt = sum(1 for L in range(1, T_b + 1) if len(blks[L]) == 0)
            part_ok = sorted(all_d) == list(range(1, T_b)) and len(all_d) == len(set(all_d))
            singleton_ok = all(
                len(blks[T_b // d]) == 1 and blks[T_b // d] == [d]
                for d in range(1, T_b)
                if d * (d + 1) <= T_b
            )
            sqrt_lb = max(0, math.isqrt(T_b) - 1)
            cnt_ok = nonempty_cnt >= sqrt_lb
            ok_b = bool(part_ok and singleton_ok and cnt_ok)
            if T_b == 2:
                ok_b = bool(ok_b and blks[1] == [] and blks[2] == [1])
            blocks_ok = blocks_ok and ok_b
            block_rows.append(
                {
                    "T": T_b,
                    "nonempty_block_count": nonempty_cnt,
                    "empty_block_count": empty_cnt,
                    "sqrt_T_minus_1_lower_bound": sqrt_lb,
                    "partition_and_singleton_verified": ok_b,
                }
            )

        # Direct Fourier transform cross-check of r_{sm,T}(exp t) at T = 10 across frequencies v:
        T_four = 10
        blks_10 = cutoff_level_blocks_exact(T_four)
        alpha_10 = compute_smooth_basis_coefficients_arb(T_four, R_table=R, prec_bits=prec_bits)
        fourier_rsm_rows: List[Dict[str, Any]] = []
        for v_frac in (Fraction(0, 1), Fraction(3, 4), Fraction(-2, 1)):
            v_arb = _frac_to_arb(v_frac)
            v_c = acb(v_arb)
            # Block multiplier sum sum_{L=1}^T M_{L,T}(v) * qhat_L(v):
            block_sum = acb(0)
            for L_val in range(1, T_four + 1):
                m_L = acb(0)
                for d_val in blks_10[L_val]:
                    m_L += acb(R[d_val]) * evaluate_adjacent_multiplier_m_d_acb(
                        d_val, v_arb, prec_bits=prec_bits
                    )
                block_sum += m_L * evaluate_qhat_L_closed_acb(L_val, v_arb, prec_bits=prec_bits)

            # Independent direct t-quadrature of r_{sm,10}(exp t) * exp(-i*v*t) on [-80, log(36*T)] + certified tails:
            t_lo = arb(-80)
            t_hi = arb(36 * T_four).log()
            alpha_10_c = [acb(a) for a in alpha_10]
            max_abs_alpha = enclose_discrete_grid_max([abs(a) for a in alpha_10[1:]])

            def _rsm_four_integrand(t_c: acb, _analytic: bool, _vc: acb = v_c) -> acb:
                x_c = t_c.exp()
                x2 = x_c * x_c
                x_5_2 = (acb(arb(5) / arb(2)) * t_c).exp()
                acc = acb(0)
                for n in range(1, 2 * T_four + 1):
                    nc = acb(n)
                    acc += alpha_10_c[n] * (nc ** (-3)) * (-x2 / (nc * nc)).exp()
                return x_5_2 * acc * (acb(0, -1) * _vc * t_c).exp()

            mid_f = acb.integral(
                _rsm_four_integrand,
                acb(t_lo),
                acb(t_hi),
                rel_tol=2 ** (-prec_bits + 14),
                abs_tol=2 ** (-prec_bits + 14),
            )
            l_rad = max_abs_alpha * (arb(3) / arb(5)) * (arb(5) * t_lo / arb(2)).exp()
            s_isq = sum((arb(1) / arb(n).sqrt() for n in range(1, 2 * T_four + 1)), arb(0))
            r_rad = max_abs_alpha * s_isq * (arb(8) / (arb(3) * arb(1).exp())) * (-arb(243)).exp()
            tot_r = (l_rad + r_rad).upper()
            quad_f = mid_f + acb(arb(0, tot_r), arb(0, tot_r))
            diff_f = block_sum - quad_f
            ok_f = bool(
                arb(0) in diff_f.real
                and arb(0) in diff_f.imag
                and abs(diff_f) < arb("1e-62")
            )
            blocks_ok = blocks_ok and ok_f
            fourier_rsm_rows.append(
                {
                    "T": T_four,
                    "v_fraction": f"{v_frac.numerator}/{v_frac.denominator}",
                    "block_multiplier_sum_re": serialize_arb_certified(block_sum.real),
                    "block_multiplier_sum_im": serialize_arb_certified(block_sum.imag),
                    "direct_t_quadrature_re": serialize_arb_certified(quad_f.real),
                    "direct_t_quadrature_im": serialize_arb_certified(quad_f.imag),
                    "abs_residual": serialize_arb_certified(abs(diff_f)),
                    "verified": ok_f,
                }
            )

        # 2D. Real-space signed Gram kernel H_{Y,b} and weighted (log X)^{-4} kernel H_{Y,b}^{wt}
        # across integer & noninteger Y >= 2 and b in {2, e, tau}:
        gram_rows: List[Dict[str, Any]] = []
        gram_ok = True
        base_specs = (
            ("2", arb(2)),
            ("e", arb(1).exp()),
            ("tau", tau),
        )
        for Y_frac, T_g in (
            (Fraction(2, 1), 3),
            (Fraction(5, 2), 4),
            (Fraction(4, 1), 6),
            (Fraction(8, 1), 14),
        ):
            y_arb = _frac_to_arb(Y_frac)
            alpha_g = compute_smooth_basis_coefficients_arb(T_g, R_table=R, prec_bits=prec_bits)
            alpha_g_c = [acb(a) for a in alpha_g]
            for b_label, b_val in base_specs:
                if Y_frac != Fraction(4, 1) and b_label != "tau":
                    continue
                # Closed-form Gram double sum sum_{d,e<T} R(d)*R(e)*H_{Y,b}(d, e):
                gram_unwt = arb(0)
                for d_i in range(1, T_g):
                    gram_unwt += (R[d_i] ** 2) * evaluate_signed_gram_H_closed_arb(
                        y_arb, d_i, d_i, T_g, base_mult=b_val, prec_bits=prec_bits
                    )
                    for e_j in range(d_i + 1, T_g):
                        gram_unwt += (
                            arb(2)
                            * R[d_i]
                            * R[e_j]
                            * evaluate_signed_gram_H_closed_arb(
                                y_arb, d_i, e_j, T_g, base_mult=b_val, prec_bits=prec_bits
                            )
                        )

                # Direct window quadrature of ||r_{sm,T}||_{Y,b}^2 and ||r_{sm,T}/(log X)^2||_{Y,b}^2:
                def _unwt_int(z: acb, _analytic: bool, _Tg: int = T_g, _ac: Sequence[acb] = alpha_g_c) -> acb:
                    z2 = z * z
                    s = acb(0)
                    for n in range(1, 2 * _Tg + 1):
                        nc = acb(n)
                        s += _ac[n] * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                    return (z ** 4) * s * s

                def _wt_int(z: acb, _analytic: bool, _Tg: int = T_g, _ac: Sequence[acb] = alpha_g_c) -> acb:
                    if _analytic and not bool(z.real > arb(1)):
                        nan_b = arb("nan")
                        return acb(nan_b, nan_b)
                    z2 = z * z
                    lg = z.log(analytic=_analytic)
                    s = acb(0)
                    for n in range(1, 2 * _Tg + 1):
                        nc = acb(n)
                        s += _ac[n] * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                    return (z ** 4) * s * s / (lg ** 4)

                quad_unwt = _acb_integral_certified_arb(_unwt_int, y_arb, b_val * y_arb, prec_bits=prec_bits)
                quad_wt = _acb_integral_certified_arb(_wt_int, y_arb, b_val * y_arb, prec_bits=prec_bits)

                # Weighted kernel expansion via K_{Y,b}^{wt}(m, n):
                gram_wt = arb(0)
                nz_idx = [m for m in range(1, 2 * T_g + 1) if not (alpha_g[m] == arb(0))]
                for idx_i, m_val in enumerate(nz_idx):
                    am = alpha_g[m_val]
                    gram_wt += (am * am) * evaluate_weighted_window_kernel_K_quadrature_arb(
                        y_arb, m_val, m_val, base_mult=b_val, prec_bits=prec_bits
                    )
                    for m2_val in nz_idx[idx_i + 1 :]:
                        gram_wt += (
                            arb(2)
                            * am
                            * alpha_g[m2_val]
                            * evaluate_weighted_window_kernel_K_quadrature_arb(
                                y_arb, m_val, m2_val, base_mult=b_val, prec_bits=prec_bits
                            )
                        )

                unwt_res = gram_unwt - quad_unwt
                wt_res = gram_wt - quad_wt
                sand_lo = gram_unwt / ((b_val * y_arb).log() ** 4)
                sand_hi = gram_unwt / (y_arb.log() ** 4)
                _, lo_cert = classify_arb_le_certificate(sand_lo, quad_wt)
                _, hi_cert = classify_arb_le_certificate(quad_wt, sand_hi)
                ok_g = bool(
                    arb(0) in unwt_res
                    and abs(unwt_res) < arb("1e-64")
                    and arb(0) in wt_res
                    and abs(wt_res) < arb("1e-62")
                    and lo_cert
                    and hi_cert
                )
                gram_ok = gram_ok and ok_g
                gram_rows.append(
                    {
                        "Y_fraction": f"{Y_frac.numerator}/{Y_frac.denominator}",
                        "base_b": b_label,
                        "T": T_g,
                        "r_sm_norm_sq_gram": serialize_arb_certified(gram_unwt),
                        "r_sm_norm_sq_quadrature": serialize_arb_certified(quad_unwt),
                        "unweighted_gram_minus_quadrature_residual": serialize_arb_certified(unwt_res),
                        "weighted_r_sm_norm_sq_gram": serialize_arb_certified(gram_wt),
                        "weighted_r_sm_norm_sq_quadrature": serialize_arb_certified(quad_wt),
                        "weighted_gram_minus_quadrature_residual": serialize_arb_certified(wt_res),
                        "log_sandwich_lower_bound": serialize_arb_certified(sand_lo),
                        "log_sandwich_upper_bound": serialize_arb_certified(sand_hi),
                        "directed_log_sandwich_certified": bool(lo_cert and hi_cert),
                        "verified": ok_g,
                    }
                )

        return {
            "epistemic_status": "CONCRETE_ANALYTIC_IN_LEAN",
            "section_epistemic_scope_note": (
                "Mixed analytic/formal/numerical section: finite-cutoff qhat_L(v) Gamma substitution and "
                "improper tail bounds are ANALYTIC_PROVED_OUTSIDE_LEAN; multiplier benchmark/attainment, "
                "cutoff-block partition/sqrt(T) count, and unweighted/log-weighted Gram quadratic forms "
                "are formalized in Lean Theorems 2 & 3; quadrature cross-checks are CERTIFIED_FINITE_OBSERVATION."
            ),
            "component_epistemic_map": {
                "qhat_L_finite_cutoff_gamma_identity_and_improper_tails": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "adjacent_dilation_multiplier_benchmark_and_odd_harmonic_attainment": "CONCRETE_ANALYTIC_IN_LEAN",
                "level_set_cutoff_blocks_and_sqrt_T_lower_bound": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "signed_and_log_weighted_gram_kernels_and_log_sandwich": "CONCRETE_ANALYTIC_IN_LEAN",
                "quadrature_and_sample_cross_checks": "CERTIFIED_FINITE_OBSERVATION",
            },
            "lean_theorems": [
                "adjacent_dilation_multiplier_and_cutoff_blocks_tc060",
                "signed_gram_kernel_and_log_weighted_quadratic_form_tc060",
            ],
            "multiplier_frequency_scope_note": (
                "The derivative-form bound |m_d(v)| <= sqrt(1/4 + v^2) * int_d^{d+1} t^{-3/2} dt retains "
                "its explicit (1 + |v|) / sqrt(1/4 + v^2) factor and holds for ALL real frequencies v; "
                "odd-harmonic attainment |m_d(v_k(d))| = d^{-1/2} + (d+1)^{-1/2} obstructs only a "
                "frequency-independent relative O(1/d) saving."
            ),
            "qhat_finite_cutoff_checks": qhat_rows,
            "multiplier_benchmark_checks": mult_bench_rows,
            "multiplier_sharp_attainment_checks": attainment_rows,
            "cutoff_block_partition_checks": block_rows,
            "fourier_r_sm_block_checks": fourier_rsm_rows,
            "signed_gram_and_weighted_kernel_checks": gram_rows,
            "all_section_2_checks_pass": bool(qhat_ok and mult_ok and blocks_ok and gram_ok),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 3. Section 3: Attempts A & B, Proved Obstructions, & Square-Pole Drift
# ---------------------------------------------------------------------------


def verify_section_3_attempts_a_and_b_obstructions_and_drift_theorem(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Execute Attempt A and Attempt B quantitatively:
    - Attempt A: Gaussian window localization vs global Plancherel, local low/high frequency split
      cross term, closed-form all-`v` Gamma inequality, residue-defined `z = 1/2` drift model `M_{sq,2}(d)`
      and exact residual `R_{osc}(d) = R(d) - M_{sq,2}(d)` (`R(d) > 0` certified finitely on `1..2000`
      vs `178` sign flips of `R_{osc}`), and exact singleton-block refutation of Candidate A1 as stated
      (`I_T(T) = {1}` for `T >= 2` at `v = 0` giving exact ratio `= 1`).
    - Attempt B & Informed Replacement: `dq = er` product compensation, unbounded arbitrary-coefficient
      family `d = 1, a = e_1` refuting Candidate B1 for every fixed constant `C` (plus scoped finite
      diagnostics and actual Liouville exclusions of `C = 1` and `C = 3`), unconditional `w_{2,lambda}`
      prime vs `6p` support (`w_{2,lambda}(p) = -(log p)^2`, `w_{2,lambda}(6p) = 0` for prime `p >= 5`),
      certified `O(log Y)` drift sub-unit and jump-reindexing checks, discrete Abel identity for
      `r_{sm,T}^{drift}`, directed increment bound `|delta_{sq,2}(d)| <= 12*log(d+1)/sqrt(d)`, and
      evaluation of `r_{sm,T}^{drift}`, `r_{sm,<=min(D_0,T-1)}^{osc}`, and `r_{sm,>min(D_0,T-1)}^{osc}`
      using certified canonical `D_0(Y) = floor(log Y)` (including `D_0(2) = 0` empty small slice).
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        tbl = compute_selberg_centered_remainder_table_arb(2000, prec_bits=prec_bits)
        c_lam = tbl["c_lambda"]
        w2 = tbl["w2"]
        R = tbl["R"]
        M_drift = tbl["M_drift"]
        R_osc = tbl["R_osc"]
        c_half = tbl["c_half_lambda"]

        # 3A-1. Closed-form all-v Gamma(5/4 - i*v/2) inequality check:
        g54 = (arb(5) / arb(4)).gamma()
        pref_gam = (arb(2) ** (arb(3) / arb(2))) * g54
        gamma_rows: List[Dict[str, Any]] = []
        gamma_ok = True
        for v_frac in (
            Fraction(0, 1),
            Fraction(1, 4),
            Fraction(1, 2),
            Fraction(1, 1),
            Fraction(2, 1),
            Fraction(5, 1),
            Fraction(10, 1),
            Fraction(20, 1),
        ):
            v_arb = _frac_to_arb(v_frac)
            lhs_g = abs(acb(arb(5) / arb(4), -v_arb / arb(2)).gamma())
            rhs_g = (
                pref_gam
                * ((arb(1) / arb(16) + (v_arb * v_arb) / arb(4)) ** (arb(3) / arb(8)))
                / ((tau * v_arb / arb(2)).cosh() ** (arb(1) / arb(4)))
            )
            eq_v0 = v_frac == Fraction(0, 1)
            st_g, ok_g = classify_arb_le_certificate(
                lhs_g, rhs_g, exact_algebraic_equality_justified=eq_v0
            )
            gamma_ok = gamma_ok and ok_g
            gamma_rows.append(
                {
                    "v_fraction": f"{v_frac.numerator}/{v_frac.denominator}",
                    "abs_gamma_5_4_minus_iv_half": serialize_arb_certified(lhs_g),
                    "closed_form_cosh_majorant": serialize_arb_certified(rhs_g),
                    "certificate_status": st_g,
                    "verified": ok_g,
                }
            )

        # 3A-2. Global Plancherel int_0^infty |r_sm|^2 dX/X vs local window ||r_sm||_Y^2:
        const_K_inf = arb(3) * (tau / arb(2)).sqrt() / arb(8)
        loc_vs_glob_rows: List[Dict[str, Any]] = []
        loc_ok = True
        for Y_int in (2, 4, 8, 16, 32, 64):
            y_arb = arb(Y_int)
            T_y = certify_T_canonical_cutoff(Y_int, prec_bits=prec_bits)
            alpha_y = compute_smooth_basis_coefficients_arb(T_y, R_table=R, prec_bits=prec_bits)
            nz = [m for m in range(1, 2 * T_y + 1) if not (alpha_y[m] == arb(0))]
            glob_sq = arb(0)
            loc_sq = arb(0)
            for idx_i, m_val in enumerate(nz):
                cm = alpha_y[m_val]
                mm = arb(m_val * m_val)
                glob_sq += cm * cm * const_K_inf * (mm * mm) / ((arb(2) * mm) ** (arb(5) / arb(2)))
                loc_sq += cm * cm * evaluate_window_kernel_K_closed_arb(y_arb, m_val, m_val, tau, prec_bits=prec_bits)
                for n_val in nz[idx_i + 1 :]:
                    cn = alpha_y[n_val]
                    mn = arb(m_val * n_val)
                    nn = arb(n_val * n_val)
                    glob_sq += arb(2) * cm * cn * const_K_inf * (mn * mn) / ((mm + nn) ** (arb(5) / arb(2)))
                    loc_sq += arb(2) * cm * cn * evaluate_window_kernel_K_closed_arb(
                        y_arb, m_val, n_val, tau, prec_bits=prec_bits
                    )
            endpt_glob = (R[T_y] ** 2) * const_K_inf / ((arb(2) ** (arb(5) / arb(2))) * arb(T_y))
            _, dom_cert = classify_arb_le_certificate(loc_sq, glob_sq)
            # Gaussian Schwartz majorant integral on [Y, tau*Y]:
            t0 = y_arb.log() + tau.log() / arb(2)
            delta_tau = tau.log() / arb(2)
            e_val = arb(1).exp()
            alpha_c = [acb(a) for a in alpha_y]

            def _schwartz_loc_int(
                z: acb,
                _analytic: bool,
                _Ty: int = T_y,
                _ac: Sequence[acb] = alpha_c,
                _t0: arb = t0,
                _dt: arb = delta_tau,
            ) -> acb:
                if _analytic and not bool(z.real > arb(0)):
                    nan_b = arb("nan")
                    return acb(nan_b, nan_b)
                z2 = z * z
                lg = z.log(analytic=_analytic)
                s = acb(0)
                for n in range(1, 2 * _Ty + 1):
                    nc = acb(n)
                    s += _ac[n] * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                w_maj = acb(e_val) * (-((lg - acb(_t0)) ** 2) / acb(_dt * _dt)).exp()
                return w_maj * (z ** 4) * s * s

            schwartz_win = _acb_integral_certified_arb(
                _schwartz_loc_int, y_arb, tau * y_arb, prec_bits=prec_bits
            )
            _, maj_cert = classify_arb_le_certificate(loc_sq, schwartz_win)
            row_lk = bool(dom_cert and maj_cert and endpt_glob > arb(0))
            loc_ok = loc_ok and row_lk
            loc_vs_glob_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_y,
                    "local_window_r_sm_norm_sq": serialize_arb_certified(loc_sq),
                    "schwartz_window_majorant_on_I_Y": serialize_arb_certified(schwartz_win),
                    "global_plancherel_L2_0_infty": serialize_arb_certified(glob_sq),
                    "global_endpoint_R_T_phi_T_norm_sq": serialize_arb_certified(endpt_glob),
                    "local_le_schwartz_and_global_certified": row_lk,
                }
            )

        # 3A-3. Exact singleton-block obstruction to Candidate A1 as stated + finite certified
        # observation of R(d) > 0 on 1 <= d <= 2000 vs R_osc(d) sign changes + directed increment bound:
        m_1_at_0_c = evaluate_adjacent_multiplier_m_d_acb(1, 0, prec_bits=prec_bits)
        m_1_at_0 = m_1_at_0_c.real
        M_T_T_at_0 = R[1] * m_1_at_0
        singleton_ratio_at_0 = abs(M_T_T_at_0) / (abs(R[1]) * abs(m_1_at_0))
        singleton_T_samples = (2, 3, 6, 32, 182, 1024)
        singleton_blocks_verified = all(
            cutoff_level_blocks_exact(T_chk)[T_chk] == [1] for T_chk in singleton_T_samples
        )
        singleton_ratio_exact_1 = bool(
            m_1_at_0_c.imag == arb(0)
            and R[1] > arb(0)
            and m_1_at_0 > arb(0)
            and M_T_T_at_0 > arb(0)
            and arb(1) in singleton_ratio_at_0
            and abs(singleton_ratio_at_0 - arb(1)) < arb("1e-74")
            and singleton_blocks_verified
        )

        all_R_pos_2000 = True
        all_M_pos_from_2 = True
        all_delta_drift_le_12 = True
        max_delta_ratio_balls: List[arb] = []
        osc_sign_flips = 0
        prev_osc_sign = 0
        delta_R_osc_id_ok = True
        for d_i in range(1, 2001):
            if not bool(R[d_i] > arb(0)):
                all_R_pos_2000 = False
            if d_i >= 2 and not bool(M_drift[d_i] > arb(0)):
                all_M_pos_from_2 = False
            delta_m = abs(M_drift[d_i] - M_drift[d_i - 1])
            scale_d = arb(d_i + 1).log() / arb(d_i).sqrt()
            max_delta_ratio_balls.append(delta_m / scale_d)
            _, ok_dm = classify_arb_le_certificate(delta_m, arb(12) * scale_d)
            if not ok_dm:
                all_delta_drift_le_12 = False
            # Exact increment identity: Delta R_osc(d) = w_{2,lambda}(d) - c_lambda - delta_{sq,2}(d)
            lhs_dro = R_osc[d_i] - R_osc[d_i - 1]
            rhs_dro = w2[d_i] - c_lam - (M_drift[d_i] - M_drift[d_i - 1])
            if not bool(arb(0) in (lhs_dro - rhs_dro) and abs(lhs_dro - rhs_dro) < arb("1e-65")):
                delta_R_osc_id_ok = False
            ro = R_osc[d_i]
            s_cur = 1 if bool(ro > arb(0)) else (-1 if bool(ro < arb(0)) else 0)
            if s_cur != 0 and prev_osc_sign != 0 and s_cur != prev_osc_sign:
                osc_sign_flips += 1
            if s_cur != 0:
                prev_osc_sign = s_cur

        max_delta_ratio_enc = enclose_discrete_grid_max(max_delta_ratio_balls)
        min_R_1_2000 = -enclose_discrete_grid_max([-R[d_i] for d_i in range(1, 2001)])
        osc_d10_pos = bool(R_osc[10] > arb(0))
        osc_d13_neg = bool(R_osc[13] < arb(0))

        # 3A-4. Unconditional w_{2,lambda} prime vs 6*p support & Delta R_osc(n) arithmetic (Item 4):
        prime_w2_ok = True
        six_p_zero_ok = True
        w2_support_rows: List[Dict[str, Any]] = []
        for p_chk in (2, 3, 5, 7, 11, 13, 97, 331):
            res_wp = w2[p_chk] + (arb(p_chk).log() ** 2)
            if not bool(arb(0) in res_wp and abs(res_wp) < arb("1e-72")):
                prime_w2_ok = False
            if p_chk >= 5:
                n_6p = 6 * p_chk
                is_zero_6p = w2[n_6p] == arb(0)
                if not is_zero_6p:
                    six_p_zero_ok = False
                if p_chk in (5, 97, 331):
                    delta_ro_p = R_osc[p_chk] - R_osc[p_chk - 1]
                    delta_ro_6p = R_osc[n_6p] - R_osc[n_6p - 1]
                    w2_support_rows.append(
                        {
                            "p": p_chk,
                            "six_p": n_6p,
                            "w2_at_p": serialize_arb_certified(w2[p_chk]),
                            "w2_at_p_plus_log_p_sq_residual": serialize_arb_certified(res_wp),
                            "w2_at_6p_exact_zero": is_zero_6p,
                            "Delta_R_osc_at_p": serialize_arb_certified(delta_ro_p),
                            "Delta_R_osc_at_6p": serialize_arb_certified(delta_ro_6p),
                            "Delta_R_osc_at_6p_minus_neg_c_lambda": serialize_arb_certified(
                                delta_ro_6p - (-c_lam)
                            ),
                        }
                    )

        drift_obs_ok = bool(
            singleton_ratio_exact_1
            and all_R_pos_2000
            and all_M_pos_from_2
            and all_delta_drift_le_12
            and delta_R_osc_id_ok
            and prime_w2_ok
            and six_p_zero_ok
            and osc_d10_pos
            and osc_d13_neg
            and osc_sign_flips >= 150
        )

        # 3B-1. Product compensation in H_Y(d, e) at (Y, T) = (16, 32), (d, e) = (8, 1):
        H_16_8_1 = evaluate_signed_gram_H_closed_arb(16, 8, 1, 32, base_mult=tau, prec_bits=prec_bits)
        H_16_8_8 = evaluate_signed_gram_H_closed_arb(16, 8, 8, 32, base_mult=tau, prec_bits=prec_bits)
        comp_ratio_8_1 = abs(H_16_8_1) / H_16_8_8
        _, comp_gt_2 = classify_arb_le_certificate(arb(2), comp_ratio_8_1)

        # 3B-2. Certified unbounded arbitrary-coefficient family d = 1, a = e_1 refuting Candidate B1
        # for EVERY fixed constant C, alongside scoped finite diagnostics and Liouville witnesses:
        def _eval_scaled_ratio_for_rational_vec(
            Y_val: int, d_val: int, rat_vec: Sequence[Fraction]
        ) -> arb:
            y_a = arb(Y_val)
            L_v = len(rat_vec)
            a_v = [_frac_to_arb(fr) for fr in rat_vec]
            g_sq = arb(0)
            d_sq = arb(0)
            for q in range(1, L_v + 1):
                for r in range(1, L_v + 1):
                    k00 = evaluate_window_kernel_K_closed_arb(y_a, d_val * q, d_val * r, tau, prec_bits=prec_bits)
                    k10 = evaluate_window_kernel_K_closed_arb(
                        y_a, (d_val + 1) * q, d_val * r, tau, prec_bits=prec_bits
                    )
                    k01 = evaluate_window_kernel_K_closed_arb(
                        y_a, d_val * q, (d_val + 1) * r, tau, prec_bits=prec_bits
                    )
                    k11 = evaluate_window_kernel_K_closed_arb(
                        y_a, (d_val + 1) * q, (d_val + 1) * r, tau, prec_bits=prec_bits
                    )
                    w = a_v[q - 1] * a_v[r - 1]
                    g_sq += w * k00
                    d_sq += w * (k00 - k10 - k01 + k11)
            return arb(d_val) * (d_sq / g_sq).sqrt()

        unbounded_b1_family_rows: List[Dict[str, Any]] = []
        unbounded_b1_ok = True
        for Y_fam in (2, 3, 4, 8):
            T_fam = certify_T_canonical_cutoff(Y_fam, prec_bits=prec_bits)
            L_1_fam = T_fam // 1
            e1_vec = [Fraction(1, 1)] + [Fraction(0, 1)] * (L_1_fam - 1)
            y_fa = arb(Y_fam)
            g_norm_sq = evaluate_window_kernel_K_closed_arb(y_fa, 1, 1, tau, prec_bits=prec_bits)
            actual_ratio = _eval_scaled_ratio_for_rational_vec(Y_fam, 1, e1_vec)
            analytic_lb = (arb(3 * Y_fam * Y_fam) / arb(4)).exp() / arb(8) - arb(1)
            _, lb_cert = classify_arb_le_certificate(analytic_lb, actual_ratio)
            denom_pos = bool(g_norm_sq > arb(0) and T_fam > 1 and L_1_fam >= 1 and analytic_lb > arb(0))
            row_fb_ok = bool(denom_pos and lb_cert)
            unbounded_b1_ok = unbounded_b1_ok and row_fb_ok
            unbounded_b1_family_rows.append(
                {
                    "Y": Y_fam,
                    "d": 1,
                    "T_Y": T_fam,
                    "L_1_inherited_length": L_1_fam,
                    "phi_1_window_norm_sq_positive": bool(g_norm_sq > arb(0)),
                    "phi_1_window_norm_sq": serialize_arb_certified(g_norm_sq),
                    "analytic_lower_bound_exp_3Y2_4_over_8_minus_1": serialize_arb_certified(analytic_lb),
                    "actual_scaled_ratio_norm_phi1_minus_phi2_over_norm_phi1": serialize_arb_certified(
                        actual_ratio
                    ),
                    "directed_lower_bound_certified": lb_cert,
                    "verified": row_fb_ok,
                }
            )

        ce_steep_16_4 = _eval_scaled_ratio_for_rational_vec(16, 4, [Fraction(1, 1), Fraction(0, 1)])
        ce_res_L2 = _eval_scaled_ratio_for_rational_vec(16, 16, [Fraction(1, 1), Fraction(-80917, 73927)])
        ce_res_L3 = _eval_scaled_ratio_for_rational_vec(
            16, 16, [Fraction(1, 1), Fraction(-164577, 75331), Fraction(124981, 71498)]
        )
        ce_res_L4 = _eval_scaled_ratio_for_rational_vec(
            16,
            16,
            [
                Fraction(1, 1),
                Fraction(-299041, 73171),
                Fraction(221183, 25141),
                Fraction(-533944, 83909),
            ],
        )
        ce_liouville_Y4_d1 = _eval_scaled_ratio_for_rational_vec(
            4, 1, [Fraction(liouville_lambda_int(q), 1) for q in range(1, 7)]
        )
        ce_liouville_Y16_d5 = _eval_scaled_ratio_for_rational_vec(
            16, 5, [Fraction(liouville_lambda_int(q), 1) for q in range(1, 7)]
        )
        _, ok_steep = classify_arb_le_certificate(arb(800), ce_steep_16_4)
        _, ok_res23 = classify_arb_le_certificate(ce_res_L2, ce_res_L3)
        _, ok_res34 = classify_arb_le_certificate(ce_res_L3, ce_res_L4)
        _, ok_res4_gt5 = classify_arb_le_certificate(arb(5), ce_res_L4)
        _, ok_liouv4_gt29 = classify_arb_le_certificate(_frac_to_arb(Fraction(297, 100)), ce_liouville_Y4_d1)
        _, ok_liouv16_gt3 = classify_arb_le_certificate(_frac_to_arb(Fraction(308, 100)), ce_liouville_Y16_d5)
        cand_b1_refuted_ok = bool(
            unbounded_b1_ok
            and ok_steep
            and ok_res23
            and ok_res34
            and ok_res4_gt5
            and ok_liouv4_gt29
            and ok_liouv16_gt3
        )

        # 3B-3. Informed replacement within the same representation (including Y = 2 with D_0(2) = 0):
        # r_{sm,T} = r_{sm,T}^{drift} + r_{sm,<=min(D_0,T-1)}^{osc} + r_{sm,>min(D_0,T-1)}^{osc}!
        replacement_rows: List[Dict[str, Any]] = []
        repl_ok = True
        for Y_int in (2, 4, 8, 16, 32, 64):
            y_arb = arb(Y_int)
            T_y = certify_T_canonical_cutoff(Y_int, prec_bits=prec_bits)
            D0_y = min(T_y - 1, certify_D0_small_divisor_cutoff(Y_int, kappa=1, prec_bits=prec_bits))

            # Verify pointwise Abel identity for r_{sm,T}^{drift} at X = Y:
            r_drift_direct = arb(0)
            r_drift_abel_steps = arb(0)
            r_drift_jumps = arb(0)
            for d_i in range(1, T_y + 1):
                L_d = T_y // d_i
                d_a = arb(d_i)
                g_d = (
                    evaluate_Q_general_arb(
                        y_arb / d_a, L_d, coeff_fn=liouville_lambda_int, prec_bits=prec_bits
                    )
                    / d_a.sqrt()
                )
                r_drift_abel_steps += (M_drift[d_i] - M_drift[d_i - 1]) * g_d
                if d_i < T_y:
                    d1_a = arb(d_i + 1)
                    L_d1 = T_y // (d_i + 1)
                    q_same = (
                        evaluate_Q_general_arb(
                            y_arb / d1_a, L_d, coeff_fn=liouville_lambda_int, prec_bits=prec_bits
                        )
                        / d1_a.sqrt()
                    )
                    q_next = (
                        evaluate_Q_general_arb(
                            y_arb / d1_a, L_d1, coeff_fn=liouville_lambda_int, prec_bits=prec_bits
                        )
                        / d1_a.sqrt()
                    )
                    r_drift_direct += M_drift[d_i] * (g_d - q_same)
                    r_drift_jumps += M_drift[d_i] * (q_same - q_next)
            r_drift_end = M_drift[T_y] * evaluate_phi_n_arb(y_arb, T_y, prec_bits=prec_bits)
            abel_res = r_drift_direct - (r_drift_abel_steps - r_drift_end - r_drift_jumps)

            # Evaluate local unweighted window norms of r_sm, r_sm^{drift}, r_{sm,<=D_0}^{osc}, r_{sm,>D_0}^{osc}
            # via exact phi_n basis expansion and K_Y(m, n):
            def _norm_sq_from_outer_weights(weights_seq: Sequence[arb], d_lo: int, d_hi: int) -> arb:
                if d_hi < d_lo:
                    return arb(0)
                coeff_m = [arb(0)] * (2 * T_y + 1)
                for d_i in range(d_lo, min(d_hi + 1, T_y)):
                    wd = weights_seq[d_i]
                    L_d = T_y // d_i
                    for q in range(1, L_d + 1):
                        lq = arb(liouville_lambda_int(q))
                        coeff_m[d_i * q] += wd * lq
                        coeff_m[(d_i + 1) * q] -= wd * lq
                return evaluate_bilinear_window_pairing_closed_arb(
                    y_arb, 2 * T_y, coeff_m, coeff_m, base_mult=tau, prec_bits=prec_bits
                )

            norm_tot = _norm_sq_from_outer_weights(R, 1, T_y - 1)
            norm_drift = _norm_sq_from_outer_weights(M_drift, 1, T_y - 1)
            norm_osc_small = _norm_sq_from_outer_weights(R_osc, 1, D0_y)
            norm_osc_core = _norm_sq_from_outer_weights(R_osc, D0_y + 1, T_y - 1)
            lg_y4 = y_arb.log() ** 4

            ok_r = bool(
                arb(0) in abel_res
                and abs(abel_res) < arb("1e-68")
                and norm_tot >= arb(0)
                and norm_drift >= arb(0)
                and (norm_osc_small == arb(0) if D0_y == 0 else norm_osc_small >= arb(0))
                and norm_osc_core >= arb(0)
            )
            repl_ok = repl_ok and ok_r
            replacement_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_y,
                    "D_0_Y": D0_y,
                    "small_divisor_slice_empty": D0_y == 0,
                    "drift_abel_pointwise_residual_at_Y": serialize_arb_certified(abel_res),
                    "r_sm_total_norm_sq": serialize_arb_certified(norm_tot),
                    "r_sm_drift_norm_sq": serialize_arb_certified(norm_drift),
                    "r_sm_drift_weighted_upper_bound_over_logY4": serialize_arb_certified(
                        norm_drift / lg_y4
                    ),
                    "r_sm_osc_small_d_le_D0_norm_sq": serialize_arb_certified(norm_osc_small),
                    "r_sm_osc_core_d_gt_D0_norm_sq": serialize_arb_certified(norm_osc_core),
                    "verified": ok_r,
                }
            )

        # 3B-4. Corrected O(log Y) sub-unit summation & drift-jump reindexing verification (Item 5):
        c_win_5 = ((tau ** 5 - arb(1)) / arb(5)).sqrt()
        subunit_and_jump_rows: List[Dict[str, Any]] = []
        sub_jump_ok = True
        for y_sub_frac in (
            Fraction(2, 1),
            Fraction(299, 100),
            Fraction(4, 1),
            Fraction(16, 1),
            Fraction(64, 1),
        ):
            y_s = _frac_to_arb(y_sub_frac)
            T_s = certify_T_canonical_cutoff(y_sub_frac, prec_bits=prec_bits)
            m_fl = y_sub_frac.numerator // y_sub_frac.denominator
            sub_lhs = (y_s ** (arb(5) / arb(2))) * sum(
                (arb(d_s + 1).log() / (arb(d_s) ** (arb(7) / arb(2))) for d_s in range(m_fl + 1, T_s + 1)),
                arb(0),
            )
            sub_rhs = ((arb(3) / arb(2)) ** (arb(5) / arb(2))) * (
                (arb(2) / arb(5)) * y_s.log() + arb(1) / arb(2)
            )
            _, ok_sub = classify_arb_le_certificate(sub_lhs, sub_rhs)

            # Exact drift-jump reindexing d = floor(T/q) for 2 <= q <= T:
            jump_d_sum = arb(0)
            for d_j in range(1, T_s):
                L_d = T_s // d_j
                L_d1 = T_s // (d_j + 1)
                for q_j in range(L_d1 + 1, L_d + 1):
                    jump_d_sum += (
                        M_drift[d_j]
                        * arb(liouville_lambda_int(q_j))
                        * evaluate_phi_n_arb(y_s, (d_j + 1) * q_j, prec_bits=prec_bits)
                    )
            jump_q_reindexed = arb(0)
            jump_coeff_vec = [arb(0)] * (2 * T_s + 1)
            for q_j in range(2, T_s + 1):
                d_adm = T_s // q_j
                term_wt = M_drift[d_adm] * arb(liouville_lambda_int(q_j))
                jump_q_reindexed += term_wt * evaluate_phi_n_arb(y_s, (d_adm + 1) * q_j, prec_bits=prec_bits)
                jump_coeff_vec[(d_adm + 1) * q_j] += term_wt
            reidx_res = jump_d_sum - jump_q_reindexed
            jump_win_norm = evaluate_bilinear_window_pairing_closed_arb(
                y_s, 2 * T_s, jump_coeff_vec, jump_coeff_vec, base_mult=tau, prec_bits=prec_bits
            ).sqrt()
            jump_olog_rhs = (
                arb(8)
                * c_win_5
                * (y_s ** (arb(5) / arb(2)))
                * arb(T_s).log()
                / arb(T_s * T_s)
            )
            _, ok_jmp = classify_arb_le_certificate(jump_win_norm, jump_olog_rhs)
            ok_sj_row = bool(
                ok_sub and arb(0) in reidx_res and abs(reidx_res) < arb("1e-68") and ok_jmp
            )
            sub_jump_ok = sub_jump_ok and ok_sj_row
            subunit_and_jump_rows.append(
                {
                    "Y_fraction": f"{y_sub_frac.numerator}/{y_sub_frac.denominator}",
                    "floor_Y": m_fl,
                    "T_Y": T_s,
                    "subunit_weighted_sum_lhs": serialize_arb_certified(sub_lhs),
                    "subunit_uniform_O_logY_rhs": serialize_arb_certified(sub_rhs),
                    "subunit_bound_certified": ok_sub,
                    "drift_jump_reindexing_residual_at_Y": serialize_arb_certified(reidx_res),
                    "drift_jump_window_norm": serialize_arb_certified(jump_win_norm),
                    "drift_jump_O_logY_upper_bound": serialize_arb_certified(jump_olog_rhs),
                    "drift_jump_bound_certified": ok_jmp,
                    "verified": ok_sj_row,
                }
            )

        return {
            "epistemic_status": "ANALYTIC_PROVED_OUTSIDE_LEAN",
            "section_epistemic_scope_note": (
                "Mixed section: Gaussian window majorant, local low/high cross-term split, Gauss-product "
                "polynomial inequality, discrete Abel identity, |delta_{sq,2}(d)| <= 12*log(d+1)/sqrt(d), "
                "finite small-divisor weighted bound, singleton-block A1 obstruction, d=1/e_1 B1 lower bound, "
                "w_{2,lambda}(p)/w_{2,lambda}(6p) support, and drift-jump reindexing are formalized in Lean "
                "Theorems 4, 5, & 7; Euler reflection/Gauss product Gamma majorant, z=1/2 Laurent residue "
                "derivation of M_{sq,2}(d), and all-eps summation/cutoff contractions of r_sm^{drift} and "
                "r_{sm,<=D_0}^{osc} are ANALYTIC_PROVED_OUTSIDE_LEAN; finite R(d)/R_osc(d) sign counts and "
                "finite B1 sample ratios are CERTIFIED_FINITE_OBSERVATION."
            ),
            "component_epistemic_map": {
                "gaussian_window_majorant_and_local_frequency_split": "CONCRETE_ANALYTIC_IN_LEAN",
                "all_v_closed_form_gamma_majorant": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "z_half_laurent_residue_drift_model_M_sq_2": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "candidate_a1_singleton_block_I_T_T_v0_refutation": "CONCRETE_ANALYTIC_IN_LEAN",
                "finite_R_d_positivity_and_R_osc_sign_flips_1_to_2000": "CERTIFIED_FINITE_OBSERVATION",
                "candidate_b1_unbounded_family_d1_e1_refutation": "CONCRETE_ANALYTIC_IN_LEAN",
                "candidate_b1_finite_diagnostics_and_liouville_constant_exclusions": "CERTIFIED_FINITE_OBSERVATION",
                "w2_prime_and_6p_unconditional_support": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "drift_abel_split_and_increment_bound": "CONCRETE_ANALYTIC_IN_LEAN",
                "all_eps_drift_and_small_divisor_relative_contractions": "ANALYTIC_PROVED_OUTSIDE_LEAN",
            },
            "lean_theorems": [
                "gaussian_window_majorant_and_local_frequency_split_tc060",
                "second_order_drift_abel_and_small_divisor_contraction_tc060",
                "full_core_quantified_obstructions_and_w2_support_tc060r",
            ],
            "attempt_a_gamma_closed_form_checks": gamma_rows,
            "attempt_a_localization_vs_global_plancherel": loc_vs_glob_rows,
            "candidate_a1_obstruction_and_square_pole_drift": {
                "candidate_statement": (
                    "Candidate A1 (as stated): Uniformly over all T >= T_0, level-set blocks 1 <= L <= T, "
                    "and low frequencies |v| <= Omega(Y), intra-block sign cancellation of R(d) = W_2(d) - c_lambda*d "
                    "across I_L(T) satisfies |M_{L,T}(v)| <= C*(log T)^{-1-delta} * sum_{d in I_L(T)} |R(d)|*|m_d(v)| "
                    "for fixed C >= 0, delta > 0 without subtracting M_{sq,2}(d)."
                ),
                "verdict": "REFUTED_AS_STATED_UNIFORMLY_OVER_ALL_BLOCKS_BY_SINGLETON_I_T_T_AT_V_ZERO",
                "obstruction_scope": (
                    "For every T >= 2 (including along canonical T(Y) -> infty), I_T(T) = {1} is a singleton block; "
                    "at v = 0 (always in |v| <= Omega(Y)), R(1) = -c_lambda > 0 and m_1(0) = 1 - 1/sqrt(2) > 0, "
                    "so |M_{T,T}(0)| / sum_{d in I_T(T)} |R(d)|*|m_d(0)| = 1 identically, contradicting "
                    "C*(log T)^{-1-delta} -> 0. Refutes the all-block uniform candidate as stated, not every "
                    "estimate on selected multi-element blocks or the complete signed sum."
                ),
                "M_sq_2_model_role": (
                    "RESIDUE_DEFINED_Z_HALF_DRIFT_MODEL (D_lambda(z) = zeta(2z)/zeta(z) has a simple zero at "
                    "z = 1 and a simple pole at z = 1/2; local residue does not by itself establish a global "
                    "Perron asymptotic or eventual positivity of R(d))"
                ),
                "R_osc_residual_role": "EXACT_DRIFT_SUBTRACTED_RESIDUAL_R_MINUS_M_SQ_2",
                "singleton_block_I_T_T_v0_obstruction": {
                    "tested_T_values": list(singleton_T_samples),
                    "all_I_T_T_equal_singleton_1": singleton_blocks_verified,
                    "R_1_equals_minus_c_lambda": serialize_arb_certified(R[1]),
                    "m_1_at_v_0": serialize_arb_certified(m_1_at_0),
                    "M_T_T_at_v_0": serialize_arb_certified(M_T_T_at_0),
                    "exact_singleton_ratio_at_v_0": 1,
                    "singleton_ratio_ball_check": serialize_arb_certified(singleton_ratio_at_0),
                    "verified": singleton_ratio_exact_1,
                },
                "c_half_lambda": serialize_arb_certified(c_half),
                "finite_observation_scope": "CERTIFIED_FINITE_OBSERVATION_ON_INTEGERS_1_TO_2000_ONLY",
                "all_R_d_strictly_positive_1_to_2000": all_R_pos_2000,
                "min_R_d_on_1_to_2000": serialize_arb_certified(min_R_1_2000),
                "R_d_sign_flips_1_to_2000": 0,
                "R_osc_at_10": serialize_arb_certified(R_osc[10]),
                "R_osc_at_13": serialize_arb_certified(R_osc[13]),
                "R_osc_at_2000": serialize_arb_certified(R_osc[2000]),
                "R_osc_sign_flips_1_to_2000": osc_sign_flips,
                "all_delta_drift_le_12_log_d1_over_sqrt_d_certified": all_delta_drift_le_12,
                "max_delta_drift_ratio_1_to_2000": serialize_arb_certified(max_delta_ratio_enc),
                "unconditional_w2_prime_and_6p_support_checks": {
                    "exact_increment_identity_verified_1_to_2000": delta_R_osc_id_ok,
                    "prime_w2_equals_minus_log_p_sq_verified": prime_w2_ok,
                    "six_p_three_distinct_primes_w2_zero_verified": six_p_zero_ok,
                    "sample_rows": w2_support_rows,
                    "unconditional_scope_note": (
                        "Delta R_osc(n) = w_{2,lambda}(n) - c_lambda - delta_{sq,2}(n) has "
                        "Delta R_osc(p) ~ -(log p)^2 on primes p and Delta R_osc(6p) -> -c_lambda != 0 on "
                        "n = 6p (prime p >= 5) unconditionally from prime-power support of Lambda_lambda; "
                        "these pointwise discrete increment sizes do not diagnose off-critical zeros."
                    ),
                },
                "verified": drift_obs_ok,
            },
            "attempt_b_product_compensation_and_candidate_b1_counterexamples": {
                "H_16_8_1": serialize_arb_certified(H_16_8_1),
                "H_16_8_8": serialize_arb_certified(H_16_8_8),
                "abs_H_16_8_1_over_H_16_8_8": serialize_arb_certified(comp_ratio_8_1),
                "product_compensation_ratio_gt_2_certified": comp_gt_2,
                "candidate_b1_statement": (
                    "Candidate B1: Uniform relative derivative gain ||Delta_d^{sm}(a)||_Y <= (C / d) * ||g_{a, d}||_Y "
                    "for an absolute constant C > 0 independent of Y >= 2, 1 <= d < T(Y), L >= 1, and coefficients a."
                ),
                "candidate_b1_verdict": (
                    "REFUTED_FOR_EVERY_FIXED_C_ON_ARBITRARY_COEFFICIENTS_BY_UNBOUNDED_D1_E1_FAMILY"
                ),
                "candidate_b1_refutation_scope": (
                    "At d = 1 < T(Y) (Y >= 2) and a = e_1 (supported at q = 1 on 1 <= q <= L_1), "
                    "phi_2(X)/phi_1(X) = exp(3*X^2/4)/8 gives ||phi_1 - phi_2||_Y / ||phi_1||_Y >= "
                    "exp(3*Y^2/4)/8 - 1 -> infty as Y -> infty, refuting every fixed C in the stated "
                    "geometry-only inequality. Finite steep-tail/resonant-bulk ratios are retained strictly "
                    "as finite diagnostics, and actual Liouville witnesses are scoped strictly to excluding "
                    "the tested constants C = 1 and C = 3 on their stated domains (not refuting a "
                    "Liouville-specific inequality with controlled arithmetic forcing)."
                ),
                "unbounded_arbitrary_coefficient_family_d1_e1_rows": unbounded_b1_family_rows,
                "finite_diagnostics_role": "FINITE_DIAGNOSTIC_NOT_UNIVERSAL_CONSTANT_REFUTATION",
                "steep_tail_Y16_d4_L2_a_1_0_scaled_ratio": serialize_arb_certified(ce_steep_16_4),
                "resonant_bulk_Y16_d16_L2_scaled_ratio": serialize_arb_certified(ce_res_L2),
                "resonant_bulk_Y16_d16_L3_scaled_ratio": serialize_arb_certified(ce_res_L3),
                "resonant_bulk_Y16_d16_L4_scaled_ratio": serialize_arb_certified(ce_res_L4),
                "actual_liouville_witness_scope": (
                    "EXCLUDES_TESTED_CONSTANTS_C_EQ_1_AT_Y4_D1_T6_AND_C_EQ_3_AT_Y16_D5_T32_ONLY"
                ),
                "actual_liouville_Y4_d1_T6_scaled_ratio": serialize_arb_certified(ce_liouville_Y4_d1),
                "actual_liouville_Y16_d5_T32_scaled_ratio": serialize_arb_certified(ce_liouville_Y16_d5),
                "verified": bool(comp_gt_2 and cand_b1_refuted_ok),
            },
            "informed_replacement_drift_and_small_divisor_rows": replacement_rows,
            "drift_subunit_and_jump_reindexing_checks": subunit_and_jump_rows,
            "all_section_3_checks_pass": bool(
                gamma_ok
                and loc_ok
                and drift_obs_ok
                and comp_gt_2
                and cand_b1_refuted_ok
                and repl_ok
                and sub_jump_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 4. Section 4: Complete Energy Bridge & Global Consequence Classification
# ---------------------------------------------------------------------------


def verify_section_4_complete_energy_bridge_and_global_consequence(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Track the complete reconstruction `Q_{lambda,T} = 2*P_Y - D_{2,known,Y} - D_{2,core,Y}`
    retaining the full open core `min(D_0(Y), T(Y)-1) < d <= T(Y)-1` (including `d >= ceil(tau*Y)`),
    certify the `R`-independent threshold contraction for `G_eps(R)` keeping `B_drift`, `B_sample`,
    and `B_known` distinct, and classify global consequences across the four required tiers.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        tbl = compute_selberg_centered_remainder_table_arb(420, prec_bits=prec_bits)
        c_lam = tbl["c_lambda"]
        R = tbl["R"]
        M_drift = tbl["M_drift"]
        R_osc = tbl["R_osc"]

        complete_rows: List[Dict[str, Any]] = []
        comp_ok = True
        for Y_int in (2, 4, 8, 16, 32, 64):
            y_arb = arb(Y_int)
            T_y = certify_T_canonical_cutoff(Y_int, prec_bits=prec_bits)
            D0_raw = certify_D0_small_divisor_cutoff(Y_int, kappa=1, prec_bits=prec_bits)
            D0_y = min(T_y - 1, D0_raw)

            E_tot = evaluate_E_L_scale_arb(y_arb, L=T_y, mode="liouville", prec_bits=prec_bits)
            rd = _evaluate_route_d_totals_arb(Y_int, mode="liouville", prec_bits=prec_bits)
            D_tilde = rd["D_tilde"]
            X_tilde = rd["X_tilde"]
            P_norm_sq = D_tilde + X_tilde

            # Build phi_n coefficients (1 <= n <= 2*T_y) for the numerator of D_{2,known,Y}:
            # c_lam*Q_{sq,T} + R(T)*phi_T + r_{jump,T} + r_{sm,T}^{drift} + r_{sm,<=min(D_0,T-1)}^{osc}
            known_num_coeff = [arb(0)] * (2 * T_y + 1)
            for n in range(1, T_y + 1):
                if is_perfect_square_int(n):
                    known_num_coeff[n] += c_lam
            known_num_coeff[T_y] += R[T_y]
            for d_i in range(1, T_y):
                L_d = T_y // d_i
                L_d1 = T_y // (d_i + 1)
                for q in range(L_d1 + 1, L_d + 1):
                    known_num_coeff[(d_i + 1) * q] += R[d_i] * arb(liouville_lambda_int(q))
                w_known_sm = M_drift[d_i] + (R_osc[d_i] if d_i <= D0_y else arb(0))
                for q in range(1, L_d + 1):
                    lq = arb(liouville_lambda_int(q))
                    known_num_coeff[d_i * q] += w_known_sm * lq
                    known_num_coeff[(d_i + 1) * q] -= w_known_sm * lq

            core_sm_coeff = [arb(0)] * (2 * T_y + 1)
            for d_i in range(D0_y + 1, T_y):
                L_d = T_y // d_i
                wd = R_osc[d_i]
                for q in range(1, L_d + 1):
                    lq = arb(liouville_lambda_int(q))
                    core_sm_coeff[d_i * q] += wd * lq
                    core_sm_coeff[(d_i + 1) * q] -= wd * lq

            kn_c = [acb(c) for c in known_num_coeff]
            cs_c = [acb(c) for c in core_sm_coeff]
            lam_c = [acb(0)] + [acb(liouville_lambda_int(n)) for n in range(1, T_y + 1)]
            ln_c = [acb(0)] + [acb(arb(n).log()) for n in range(1, T_y + 1)]

            def _known_wt_int(z: acb, _analytic: bool, _Ty: int = T_y, _kc: Sequence[acb] = kn_c) -> acb:
                if _analytic and not bool(z.real > arb(1)):
                    nan_b = arb("nan")
                    return acb(nan_b, nan_b)
                z2 = z * z
                lg = z.log(analytic=_analytic)
                s = acb(0)
                for n in range(1, 2 * _Ty + 1):
                    nc = acb(n)
                    s += _kc[n] * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                return (z ** 4) * s * s / (lg ** 4)

            def _core_wt_int(
                z: acb,
                _analytic: bool,
                _Ty: int = T_y,
                _cc: Sequence[acb] = cs_c,
                _lc: Sequence[acb] = lam_c,
                _lnc: Sequence[acb] = ln_c,
            ) -> acb:
                if _analytic and not bool(z.real > arb(1)):
                    nan_b = arb("nan")
                    return acb(nan_b, nan_b)
                z2 = z * z
                lg = z.log(analytic=_analytic)
                s_core = acb(0)
                for n in range(1, 2 * _Ty + 1):
                    nc = acb(n)
                    s_core += _cc[n] * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                q_sh2 = acb(0)
                for n in range(1, _Ty + 1):
                    nc = acb(n)
                    q_sh2 += _lc[n] * ((lg - _lnc[n]) ** 2) * (nc ** (-3)) * (-z2 / (nc * nc)).exp()
                diff_num = s_core - q_sh2
                return (z ** 4) * diff_num * diff_num / (lg ** 4)

            D2_known_norm_sq = _acb_integral_certified_arb(
                _known_wt_int, y_arb, tau * y_arb, prec_bits=prec_bits
            )
            D2_core_norm_sq = _acb_integral_certified_arb(
                _core_wt_int, y_arb, tau * y_arb, prec_bits=prec_bits
            )
            rhs_complete_bound = arb(8) * P_norm_sq + arb(4) * D2_known_norm_sq + arb(4) * D2_core_norm_sq
            _, bound_cert = classify_arb_le_certificate(E_tot, rhs_complete_bound)
            comp_ok = comp_ok and bound_cert
            complete_rows.append(
                {
                    "Y": Y_int,
                    "T_Y": T_y,
                    "D_0_Y": D0_y,
                    "small_divisor_slice_empty": D0_y == 0,
                    "full_open_core_divisor_range_inclusive": [D0_y + 1, T_y - 1],
                    "E_Y": serialize_arb_certified(E_tot),
                    "D_tilde_Y": serialize_arb_certified(D_tilde),
                    "X_tilde_Y": serialize_arb_certified(X_tilde),
                    "D2_known_norm_sq": serialize_arb_certified(D2_known_norm_sq),
                    "D2_core_open_norm_sq": serialize_arb_certified(D2_core_norm_sq),
                    "eight_P_sq_plus_four_D2_known_sq_plus_four_D2_core_sq": serialize_arb_certified(
                        rhs_complete_bound
                    ),
                    "complete_upper_bound_certified": bound_cert,
                }
            )

        # Partition-only full-core checks including Y = 4096 where d >= ceil(tau*Y) is nonempty (Item 1):
        partition_rows: List[Dict[str, Any]] = []
        part_all_ok = True
        for Y_part in (2, 4, 16, 64, 4096):
            p_info = certify_open_core_divisor_partition(Y_part, kappa=1, prec_bits=prec_bits)
            p_info["Y"] = Y_part
            if Y_part <= 64:
                part_all_ok = part_all_ok and (p_info["sub_unit_tail_nonempty"] is False)
            if Y_part == 2:
                part_all_ok = part_all_ok and (
                    p_info["D_0_raw"] == 0 and p_info["small_slice_is_empty"] is True
                )
            if Y_part == 4096:
                part_all_ok = part_all_ok and (
                    p_info["T_Y"] == 32768
                    and p_info["D_0_raw"] == 8
                    and p_info["ceil_tau_Y"] == 25736
                    and p_info["full_open_core_range_inclusive"] == [9, 32767]
                    and p_info["intermediate_band_within_open_core_inclusive"] == [9, 25735]
                    and p_info["sub_unit_tail_ge_ceil_tau_Y_within_open_core_inclusive"]
                    == [25736, 32767]
                    and p_info["sub_unit_tail_nonempty"] is True
                    and p_info["sub_unit_tail_count"] == 7032
                )
            part_all_ok = part_all_ok and p_info["partition_identities_verified"]
            partition_rows.append(p_info)

        # R-independent feedback contraction threshold verification (matching Lean Theorem 6),
        # keeping B_drift, B_sample, and B_known strictly distinct:
        horizon_rows: List[Dict[str, Any]] = []
        hor_ok = True
        for eps_num, eps_den in ((1, 2), (1, 4)):
            eps_c = arb(eps_num) / arb(eps_den)
            z_ser = acb_series([acb(arb(1) + eps_c), acb(1)], prec=prec_bits).zeta()
            zeta2_eps = arb(2) * z_ser[2].real
            z_half_ser = acb_series([acb(arb(1) + eps_c / arb(2)), acb(1)], prec=prec_bits).zeta()
            z_1p_half_eps = z_half_ser[0].real
            minus_z_prime_half_eps = -z_half_ser[1].real
            B_pure_drift_analytic_upper = arb(288) * (
                (minus_z_prime_half_eps + z_1p_half_eps) ** 2
            )
            B_drift_sample = arb(576) * (z_1p_half_eps ** 2)
            lg_thresh_diag = (arb(64) * zeta2_eps + arb(1)).sqrt()
            lg_thresh_drift = arb(16) * B_drift_sample + arb(1)
            lg_Y_star = lg_thresh_diag if bool(lg_thresh_diag > lg_thresh_drift) else lg_thresh_drift
            if bool(lg_Y_star < arb(1)):
                lg_Y_star = arb(1)
            fb_diag_at_star = arb(16) * zeta2_eps / (lg_Y_star ** 2)
            fb_drift_at_star = arb(4) * B_drift_sample / lg_Y_star
            _, ok_d1 = classify_arb_le_certificate(fb_diag_at_star, arb(1) / arb(4))
            _, ok_d2 = classify_arb_le_certificate(fb_drift_at_star, arb(1) / arb(4))
            hor_ok = hor_ok and ok_d1 and ok_d2
            horizon_rows.append(
                {
                    "eps": f"{eps_num}/{eps_den}",
                    "zeta_double_prime_1_plus_eps": serialize_arb_certified(zeta2_eps),
                    "B_pure_drift_analytic_upper_role": (
                        "ANALYTIC_PURE_DRIFT_CONSTANT_288_MINUS_ZETA_PRIME_PLUS_ZETA_SQ"
                    ),
                    "B_pure_drift_analytic_upper": serialize_arb_certified(
                        B_pure_drift_analytic_upper
                    ),
                    "B_drift_sample_role": (
                        "ILLUSTRATIVE_SAMPLE_INSTANTIATION_OF_THEOREM_6_ABSTRACT_PARAMETER_NOT_FULL_KNOWN_BOUND"
                    ),
                    "B_drift_sample": serialize_arb_certified(B_drift_sample),
                    "B_known_full_analytic_role": (
                        "COMBINES_B_DRIFT_AND_B_SMALL_VIA_UNCONDITIONAL_PNT_SUPREMUM_C_OSC_DISTINCT_FROM_B_SAMPLE"
                    ),
                    "R_independent_log_Y_star": serialize_arb_certified(lg_Y_star),
                    "diag_feedback_16_zeta2_over_logY2_at_Y_star": serialize_arb_certified(
                        fb_diag_at_star
                    ),
                    "drift_feedback_4_B_over_logY_at_Y_star": serialize_arb_certified(
                        fb_drift_at_star
                    ),
                    "both_feedbacks_le_quarter_certified": bool(ok_d1 and ok_d2),
                    "horizons_R_sharing_identical_threshold": [64, 256, 1024, 4096],
                }
            )

        global_consequence_matrix = [
            {
                "consequence_class": "ABSOLUTE_LOGARITHMIC_IMPROVEMENT",
                "status": "PROVED_UNCONDITIONALLY_AND_REFINED",
                "scope": (
                    "All-order O_A(Y / (log Y)^A) control of ||r_{sm,T}||_Y^2 / (log Y)^4 established via "
                    "Selberg PNT + C_{chi,var} (TC-059), refined in TC-060/TC-060R by decomposing R(d) = "
                    "M_{sq,2}(d) + R_{osc}(d) into the residue-defined z = 1/2 drift model M_{sq,2}(d) "
                    "and the exact residual R_{osc}(d)."
                ),
            },
            {
                "consequence_class": "FIXED_POWER_SAVING",
                "status": "NOT_PROVED_UNCONDITIONALLY",
                "scope": (
                    "Forward Abelian/continuation implication proved analytically outside Lean: if "
                    "|R_{osc}(d)| = O(d^{1-delta}) for some delta in (0, 1/2], then on Re(z) > 1 - delta >= 1/2 "
                    "both sum_{d>=1} delta_{sq,2}(d)*d^{-z} and sum_{d>=1} R_{osc}(d)*(d^{-z} - (d+1)^{-z}) "
                    "converge absolutely and locally uniformly, extending D_lambda''(z)/D_lambda(z) - c_lambda*zeta(z) "
                    "holomorphically to Re(z) > 1 - delta and ruling out zeros rho_0 of zeta(z) there (where "
                    "Re(2*rho_0) > 1 => zeta(2*rho_0) != 0 would leave an uncancelled double pole "
                    "m_{rho_0}*(m_{rho_0}+1)/(z - rho_0)^2). No exact-boundary converse is claimed from "
                    "local poles alone."
                ),
            },
            {
                "consequence_class": "RELATIVE_CONTRACTION",
                "status": "PROVED_UNCONDITIONALLY_ON_SQUARE_POLE_DRIFT_AND_SMALL_DIVISORS",
                "scope": (
                    "Proved analytically outside Lean using TC-060 Theorem 5's discrete Abel identity, "
                    "increment bound |delta_{sq,2}(d)| <= 12*log(d+1)/sqrt(d), and finite weighted small-divisor "
                    "inequality together with TC-057 Theorem 25 (first main conjunct, third item) cutoff lower "
                    "bounds, inherited TC-059R Theorem 7's smooth-increment window norm estimate, and TC-057R's "
                    "PNT bound |R_{osc}(d)| <= C_{osc}*d: for every eps > 0, R >= 2, and 2 <= Y <= R, "
                    "||r_{sm,T(Y)}^{drift}/(log X)^2||_Y^2 <= (B_{drift}(eps)/(log Y)^4)*G_eps(R)*Y^eps + C_{drift}(eps) "
                    "and ||r_{sm,<=min(D_0,T-1)}^{osc}/(log X)^2||_Y^2 <= O((log Y)^{-kappa})*G_eps(R)*Y^eps + C_{small}(eps)."
                ),
            },
            {
                "consequence_class": "ALL_POSITIVE_EXPONENTS_CLOSURE",
                "status": "OPEN",
                "scope": (
                    "SUBGATE-TC-043A remains OPEN and rh_proved remains False: closing E(Y) = O_eps(Y^eps) "
                    "via Theorem 6 requires controlling the full signed open quantity "
                    "8*X_tilde(Y) + 4*||D_{2,core,T(Y)}||_Y^2, where "
                    "D_{2,core,T(Y)}(X) = (sum_{min(D_0(Y), T(Y)-1) < d <= T(Y)-1} R_{osc}(d)*Delta_d^{sm}(X) "
                    "- Q_{lambda,T(Y)}^{[2]}(X)) / (log X)^2 retains ALL d up to T(Y) - 1 (including d >= ceil(tau*Y), "
                    "because Lemma B2's O(Y*(log Y)^{-4}*exp(-2*c_W*sqrt(log Y))) bound is only an absolute upper "
                    "bound whose majorant divided by Y^eps grows without bound for fixed 0 < eps < 1)."
                ),
            },
        ]

        return {
            "epistemic_status": "CONDITIONAL_IMPLICATION",
            "section_epistemic_scope_note": (
                "Mixed section: the lossless decomposition Q_{lambda,T} = 2*P_T - D_{2,known,T} - D_{2,core,T} "
                "and (8, 4, 4) window energy inequality are unconditional in Lean Theorem 6(1)-(2), and full-core "
                "intermediate/tail retention is unconditional in Lean Theorem 7(1); the R-independent finite-horizon "
                "absorption is a CONDITIONAL_IMPLICATION in Lean Theorem 6(3) assuming the Route D diagonal, "
                "known-D_2, and open-core hypotheses."
            ),
            "component_epistemic_map": {
                "lossless_known_vs_full_core_decomposition_and_8_4_4_inequality": "CONCRETE_ANALYTIC_IN_LEAN",
                "full_core_intermediate_and_tail_partition_retention": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "R_independent_finite_horizon_feedback_absorption": "CONDITIONAL_IMPLICATION",
                "complete_reconstruction_and_sample_threshold_evaluations": "CERTIFIED_FINITE_OBSERVATION",
            },
            "lean_theorems": [
                "complete_reconstruction_drift_contraction_transfer_tc060",
                "full_core_quantified_obstructions_and_w2_support_tc060r",
            ],
            "full_open_core_formula": (
                "D_{2,core,T(Y)}(X) = [sum_{min(D_0(Y), T(Y)-1) < d <= T(Y)-1} R_{osc}(d)*Delta_d^{sm}(X) "
                "- Q_{lambda,T(Y)}^{[2]}(X)] / (log X)^2, T(Y) = ceil(Y^{5/4}), Y >= 2; sufficient open "
                "closure target retains signed 8*X_tilde(Y) + 4*||D_{2,core,T(Y)}||_Y^2."
            ),
            "complete_reconstruction_rows": complete_rows,
            "full_open_core_partition_checks": partition_rows,
            "R_independent_feedback_threshold_rows": horizon_rows,
            "global_consequence_classification": global_consequence_matrix,
            "all_section_4_checks_pass": bool(comp_ok and part_all_ok and hor_ok),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 5. Section 5: Controls, Schedule Boundaries, & Directed Certificates
# ---------------------------------------------------------------------------


def verify_section_5_controls_schedule_and_directed_certificates(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Compare actual Liouville `lambda`, unsigned `1`, finite-prime parity controls `a_2` & `a_{3,5,7}`
    (each with its own derived second-order Laurent compensation), geometry-only controls, and an
    explicitly labeled hybrid diagnostic; verify overlap rejection and schedule boundary cases.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        gamma_e = arb.const_euler()
        tbl = compute_selberg_centered_remainder_table_arb(600, prec_bits=prec_bits)
        R_lam = tbl["R"]
        R_osc_lam = tbl["R_osc"]

        # 5A. Control cumulative second-order remainder comparison at d in {50, 200, 600}:
        c0_one = -(arb(2) + arb(2) * gamma_e)
        c0_a2 = -(arb(2) + arb(2) * gamma_e + (arb(8) / arb(3)) * arb(2).log())
        c0_a357 = -(
            arb(2)
            + arb(2) * gamma_e
            + sum((arb(4 * p) * arb(p).log() / arb(p * p - 1) for p in (3, 5, 7)), arb(0))
        )
        w_one = arb(0)
        w_a2 = arb(0)
        w_a357 = arb(0)
        control_cum_rows: List[Dict[str, Any]] = []
        ctrl_ok = True
        for d_i in range(2, 601):
            w_one += selberg_w2_weight_arb(d_i, mode="unsigned_1")
            w_a2 += selberg_w2_weight_arb(d_i, mode="a2")
            w_a357 += selberg_w2_weight_arb(d_i, mode="a_3_5_7")
            if d_i in (50, 200, 600):
                d_a = arb(d_i)
                sd = d_a.sqrt()
                rem_one = w_one - (arb(2) * d_a * d_a.log() + c0_one * d_a)
                rem_a2 = w_a2 - (arb(2) * d_a * d_a.log() + c0_a2 * d_a)
                rem_a357 = w_a357 - (arb(2) * d_a * d_a.log() + c0_a357 * d_a)
                ok_d = bool(
                    abs(rem_one) / sd < arb(25)
                    and abs(rem_a2) / sd < arb(25)
                    and abs(rem_a357) / sd < arb(25)
                )
                ctrl_ok = ctrl_ok and ok_d
                control_cum_rows.append(
                    {
                        "d": d_i,
                        "liouville_R_d_first_order": serialize_arb_certified(R_lam[d_i]),
                        "liouville_R_osc_d_after_square_pole_drift": serialize_arb_certified(
                            R_osc_lam[d_i]
                        ),
                        "unsigned_1_compensated_remainder": serialize_arb_certified(rem_one),
                        "a2_compensated_remainder": serialize_arb_certified(rem_a2),
                        "a_3_5_7_compensated_remainder": serialize_arb_certified(rem_a357),
                        "verified": ok_d,
                    }
                )

        # 5B. Window smooth-remainder energy comparison across actual models + explicitly labeled
        # hybrid diagnostic (inner = a_2, outer = R_lambda(d)):
        Y_ctrl = arb(16)
        T_ctrl = exact_T_cutoff_ceil_Y_5_4(16)  # 32

        def _window_rsm_norm_for_model(
            outer_R: Sequence[arb], inner_fn: Callable[[int], int]
        ) -> arb:
            c_vec = [arb(0)] * (2 * T_ctrl + 1)
            for d_i in range(1, T_ctrl):
                wd = outer_R[d_i]
                L_d = T_ctrl // d_i
                for q in range(1, L_d + 1):
                    aq = arb(inner_fn(q))
                    c_vec[d_i * q] += wd * aq
                    c_vec[(d_i + 1) * q] -= wd * aq
            return evaluate_bilinear_window_pairing_closed_arb(
                Y_ctrl, 2 * T_ctrl, c_vec, c_vec, base_mult=tau, prec_bits=prec_bits
            )

        # Build exact compensated R_{a}(d) on 0 <= d <= T_ctrl for unsigned_1, a_2, a_{3,5,7}:
        R_one_tbl = [arb(0)] * (T_ctrl + 1)
        R_a2_tbl = [arb(0)] * (T_ctrl + 1)
        R_a357_tbl = [arb(0)] * (T_ctrl + 1)
        cu_1, cu_2, cu_357 = arb(0), arb(0), arb(0)
        for d_i in range(1, T_ctrl + 1):
            if d_i >= 2:
                cu_1 += selberg_w2_weight_arb(d_i, mode="unsigned_1")
                cu_2 += selberg_w2_weight_arb(d_i, mode="a2")
                cu_357 += selberg_w2_weight_arb(d_i, mode="a_3_5_7")
            d_a = arb(d_i)
            R_one_tbl[d_i] = cu_1 - (arb(2) * d_a * d_a.log() + c0_one * d_a)
            R_a2_tbl[d_i] = cu_2 - (arb(2) * d_a * d_a.log() + c0_a2 * d_a)
            R_a357_tbl[d_i] = cu_357 - (arb(2) * d_a * d_a.log() + c0_a357 * d_a)

        norm_liouv = _window_rsm_norm_for_model(R_lam, liouville_lambda_int)
        norm_one = _window_rsm_norm_for_model(R_one_tbl, lambda _n: 1)
        norm_a2 = _window_rsm_norm_for_model(R_a2_tbl, two_adic_parity_a2_int)
        norm_a357 = _window_rsm_norm_for_model(
            R_a357_tbl, lambda n: finite_prime_parity_aS_int(n, (3, 5, 7))
        )
        norm_hybrid_diag = _window_rsm_norm_for_model(R_lam, two_adic_parity_a2_int)

        # 5C. Boundary schedule cases (d = T - 1 near T, sub-unit Y / d < 1, noninteger Y = 5/2):
        # Sub-unit d >= ceil(tau * Y) check at Y = 8 (T = 14): no sub-unit d >= ceil(8*tau)=51, whereas at
        # Y = 64 (T = 182), ceil(64*tau) = 403 > 182; check Y / d < 1 on d in [Y + 1, T - 1] (e.g. Y = 8, d = 13):
        y8 = arb(8)
        T8 = certify_T_canonical_cutoff(8, prec_bits=prec_bits)  # 14, d = 13 has Y/d = 8/13 < 1 and d = T - 1!
        H_8_13_13 = evaluate_signed_gram_H_closed_arb(y8, 13, 13, T8, base_mult=tau, prec_bits=prec_bits)
        sub_unit_arg_8_13 = y8 / arb(13)
        _, sub_unit_lt1 = classify_arb_le_certificate(sub_unit_arg_8_13, arb(1))

        # 5D. Certified cutoff determination protocol checks (Item 6: D_0(2)=0 empty slice, nonboundary
        # samples, cutoff transitions on both sides of e, e^2, and 16, straddling enclosure rejection,
        # and Y = 4096 nonempty d >= ceil(tau*Y) full-core partition):
        d0_at_2 = certify_D0_small_divisor_cutoff(2, kappa=1, prec_bits=prec_bits)
        part_at_2 = certify_open_core_divisor_partition(2, kappa=1, prec_bits=prec_bits)
        part_at_4096 = certify_open_core_divisor_partition(4096, kappa=1, prec_bits=prec_bits)
        d0_below_e = certify_D0_small_divisor_cutoff(Fraction(27182818, 10000000), kappa=1, prec_bits=prec_bits)
        d0_above_e = certify_D0_small_divisor_cutoff(Fraction(27182819, 10000000), kappa=1, prec_bits=prec_bits)
        d0_exact_e_sym = certify_D0_small_divisor_cutoff(None, kappa=1, exact_log_Y=1, prec_bits=prec_bits)
        d0_below_e2 = certify_D0_small_divisor_cutoff(Fraction(73890560, 10000000), kappa=1, prec_bits=prec_bits)
        d0_above_e2 = certify_D0_small_divisor_cutoff(Fraction(73890561, 10000000), kappa=1, prec_bits=prec_bits)
        d0_exact_e2_sym = certify_D0_small_divisor_cutoff(None, kappa=1, exact_log_Y=2, prec_bits=prec_bits)
        T_below_16 = certify_T_canonical_cutoff(Fraction(16383, 1024), prec_bits=prec_bits)
        T_exact_16 = certify_T_canonical_cutoff(Fraction(16, 1), prec_bits=prec_bits)
        T_above_16 = certify_T_canonical_cutoff(Fraction(16385, 1024), prec_bits=prec_bits)
        d0_nonboundary = {
            str(y_nb): certify_D0_small_divisor_cutoff(y_nb, kappa=1, prec_bits=prec_bits)
            for y_nb in (Fraction(5, 2), 3, 4, 8, 16, 32, 64)
        }

        straddle_int_st, straddle_int_val, straddle_int_cand = classify_floor_from_arb_enclosure(
            arb(5, arb("1e-10"))
        )
        straddle_e_ball = arb(1).exp()
        straddle_e_st, straddle_e_val, straddle_e_cand = classify_floor_from_arb_enclosure(
            straddle_e_ball.log()
        )
        straddle_16_ball = arb(16, arb("1e-12"))
        straddle_16_st, straddle_16_val, straddle_16_cand = classify_ceil_from_arb_enclosure(
            straddle_16_ball ** (arb(5) / arb(4))
        )
        straddle_exceptions_raised = True
        for fn_call in (
            lambda: certify_floor_from_arb_enclosure(arb(5, arb("1e-10"))),
            lambda: certify_D0_small_divisor_cutoff(straddle_e_ball, kappa=1, prec_bits=prec_bits),
            lambda: certify_T_canonical_cutoff(straddle_16_ball, prec_bits=prec_bits),
        ):
            try:
                fn_call()
                straddle_exceptions_raised = False
            except AmbiguousCutoffError:
                pass

        cutoff_proto_ok = bool(
            d0_at_2 == 0
            and part_at_2["small_slice_is_empty"] is True
            and part_at_2["full_open_core_range_inclusive"] == [1, 2]
            and d0_nonboundary == {"5/2": 0, "3": 1, "4": 1, "8": 2, "16": 2, "32": 3, "64": 4}
            and d0_below_e == 0
            and d0_above_e == 1
            and d0_exact_e_sym == 1
            and d0_below_e2 == 1
            and d0_above_e2 == 2
            and d0_exact_e2_sym == 2
            and T_below_16 == 32
            and T_exact_16 == 32
            and T_above_16 == 33
            and straddle_int_st == "AMBIGUOUS_STRADDLING_ENCLOSURE"
            and straddle_int_val is None
            and straddle_int_cand == (4, 5)
            and straddle_e_st == "AMBIGUOUS_STRADDLING_ENCLOSURE"
            and straddle_e_val is None
            and straddle_e_cand == (0, 1)
            and straddle_16_st == "AMBIGUOUS_STRADDLING_ENCLOSURE"
            and straddle_16_val is None
            and straddle_16_cand == (32, 33)
            and straddle_exceptions_raised
            and part_at_4096["sub_unit_tail_nonempty"] is True
            and part_at_4096["sub_unit_tail_ge_ceil_tau_Y_within_open_core_inclusive"] == [25736, 32767]
        )

        # 5E. Directed interval certification self-tests (overlap MUST return False unless algebraically justified):
        ov_ball_a = arb(10, arb("1e-20"))
        ov_ball_b = arb(10, arb("1e-20"))
        ov_status, ov_cert = classify_arb_le_certificate(
            ov_ball_a, ov_ball_b, exact_algebraic_equality_justified=False
        )
        ov_alg_status, ov_alg_cert = classify_arb_le_certificate(
            ov_ball_a, ov_ball_b, exact_algebraic_equality_justified=True
        )
        sep_status, sep_cert = classify_arb_le_certificate(arb(1), arb(2))
        viol_status, viol_cert = classify_arb_le_certificate(arb(3), arb(2))
        cert_self_ok = bool(
            ov_status == "NOT_NUMERICALLY_CERTIFIED_OVERLAP"
            and ov_cert is False
            and ov_alg_status == "CERTIFIED_EXACT_ALGEBRAIC_EQUALITY_WITH_CONSISTENT_ENCLOSURE"
            and ov_alg_cert is True
            and sep_status == "CERTIFIED_DIRECTED_INEQUALITY"
            and sep_cert is True
            and viol_status == "REFUTED_STRICT_VIOLATION"
            and viol_cert is False
        )

        return {
            "epistemic_status": "CERTIFIED_FINITE_OBSERVATION",
            "control_cumulative_remainder_rows": control_cum_rows,
            "control_window_smooth_norms_Y16_T32": {
                "actual_liouville_matching_R_lambda": {
                    "model_type": "AUTHENTIC_ARITHMETIC_MODEL",
                    "norm_sq": serialize_arb_certified(norm_liouv),
                },
                "unsigned_ones_matching_R_1": {
                    "model_type": "CONTROL_ARITHMETIC_MODEL",
                    "norm_sq": serialize_arb_certified(norm_one),
                },
                "two_adic_parity_a2_matching_R_a2": {
                    "model_type": "FINITE_PRIME_CONTROL_MODEL",
                    "norm_sq": serialize_arb_certified(norm_a2),
                },
                "odd_prime_parity_a_3_5_7_matching_R_a357": {
                    "model_type": "FINITE_PRIME_CONTROL_MODEL",
                    "norm_sq": serialize_arb_certified(norm_a357),
                },
                "inner_a2_with_outer_liouville_R_lambda": {
                    "model_type": "HYBRID_DIAGNOSTIC_NOT_COMPETING_ARITHMETIC_MODEL",
                    "norm_sq": serialize_arb_certified(norm_hybrid_diag),
                },
            },
            "boundary_schedule_checks": {
                "Y": 8,
                "T_Y": T8,
                "d_near_T_and_sub_unit": 13,
                "Y_over_d": serialize_arb_certified(sub_unit_arg_8_13),
                "sub_unit_Y_over_d_lt_1_certified": sub_unit_lt1,
                "H_8_13_13": serialize_arb_certified(H_8_13_13),
                "H_8_13_13_strictly_positive": bool(H_8_13_13 > arb(0)),
            },
            "certified_cutoff_protocol_checks": {
                "D_0_at_Y_2": d0_at_2,
                "Y_2_small_slice_empty": part_at_2["small_slice_is_empty"],
                "Y_2_full_open_core_range": part_at_2["full_open_core_range_inclusive"],
                "nonboundary_D_0_samples": d0_nonboundary,
                "transition_around_e": {
                    "below_e_27182818_over_1e7": d0_below_e,
                    "symbolic_exact_e": d0_exact_e_sym,
                    "above_e_27182819_over_1e7": d0_above_e,
                },
                "transition_around_e_sq": {
                    "below_e2_73890560_over_1e7": d0_below_e2,
                    "symbolic_exact_e2": d0_exact_e2_sym,
                    "above_e2_73890561_over_1e7": d0_above_e2,
                },
                "transition_around_Y_16_T": {
                    "below_16_16383_over_1024": T_below_16,
                    "exact_16": T_exact_16,
                    "above_16_16385_over_1024": T_above_16,
                },
                "straddling_enclosure_rejections": {
                    "ball_around_5_status": straddle_int_st,
                    "ball_around_5_candidates": list(straddle_int_cand),
                    "arb_exp_1_around_e_status": straddle_e_st,
                    "arb_exp_1_candidates": list(straddle_e_cand),
                    "ball_around_16_T_status": straddle_16_st,
                    "ball_around_16_T_candidates": list(straddle_16_cand),
                    "all_ambiguous_raise_AmbiguousCutoffError": straddle_exceptions_raised,
                },
                "Y_4096_nonempty_tail_partition": part_at_4096,
                "verified": cutoff_proto_ok,
            },
            "directed_interval_certificate_protocol_check": {
                "overlap_without_algebraic_proof_status": ov_status,
                "overlap_without_algebraic_proof_certified": ov_cert,
                "overlap_with_algebraic_proof_status": ov_alg_status,
                "overlap_with_algebraic_proof_certified": ov_alg_cert,
                "strict_separation_status": sep_status,
                "strict_violation_status": viol_status,
                "verified": cert_self_ok,
            },
            "all_section_5_checks_pass": bool(
                ctrl_ok
                and norm_liouv > arb(0)
                and norm_one > arb(0)
                and norm_a2 > arb(0)
                and norm_a357 > arb(0)
                and norm_hybrid_diag > arb(0)
                and sub_unit_lt1
                and H_8_13_13 > arb(0)
                and cutoff_proto_ok
                and cert_self_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 6. Live Lean 4 Axiom Audit & Review Displayed-Enclosure Verification
# ---------------------------------------------------------------------------


def verify_tc060_lean_theorems_live() -> Dict[str, Any]:
    """Verify all 7 public theorems in `formal/RiemannScope/SignedDilationArithmeticEnergy.lean`
    via live `lake env lean --stdin` (`#check` and `#print axioms`) and source token checks.
    """
    import hashlib

    raw_bytes = TC_060_LEAN_MODULE_PATH.read_bytes().replace(b"\r\n", b"\n")
    module_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    src = raw_bytes.decode("utf-8")
    no_block = re.sub(r"/-.*?-/", "", src, flags=re.DOTALL)
    clean_src = re.sub(r"--[^\n]*", "", no_block)

    sorry_count = len(re.findall(r"\bsorry\b", clean_src))
    admit_count = len(re.findall(r"\badmit\b", clean_src))
    custom_axiom_count = len(re.findall(r"^\s*axiom\b", clean_src, flags=re.MULTILINE))
    pi_macro_count = len(re.findall(r"\x5cpi(?![a-zA-Z])", src)) + src.count("\u03c0")
    present = all(
        re.search(rf"^theorem\s+{re.escape(thm)}\b", clean_src, flags=re.MULTILINE) is not None
        for thm in EXPECTED_TC060_THEOREMS
    )

    lines = ["import RiemannScope.SignedDilationArithmeticEnergy"]
    for thm in EXPECTED_TC060_THEOREMS:
        fq = f"RiemannScope.SignedDilationArithmeticEnergy.{thm}"
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
    for thm in EXPECTED_TC060_THEOREMS:
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

    formal_provenance: Dict[str, Any] = {}
    if FORMAL_BUILD_REPORT_PATH.exists():
        try:
            br = json.loads(FORMAL_BUILD_REPORT_PATH.read_text(encoding="utf-8"))
            src_hashes = br.get("formal_source_hashes") or br.get("source_hashes") or {}
            formal_provenance = {
                "status": br.get("status"),
                "producing_git_commit": br.get("producing_git_commit"),
                "project_theorem_declarations_compiled": br.get(
                    "project_theorem_declarations_compiled"
                ),
                "total_theorems": br.get("total_theorems"),
                "module_sha256_in_build_report": src_hashes.get(
                    "formal/RiemannScope/SignedDilationArithmeticEnergy.lean"
                ),
                "report_hash": br.get("report_hash"),
            }
        except Exception:  # noqa: BLE001
            formal_provenance = {}

    return {
        "module_path": "formal/RiemannScope/SignedDilationArithmeticEnergy.lean",
        "module_sha256": module_sha256,
        "expected_tc060_theorems": EXPECTED_TC060_THEOREMS,
        "all_tc060_theorems_present": present,
        "sorry_count": sorry_count,
        "admit_count": admit_count,
        "custom_axiom_count": custom_axiom_count,
        "pi_token_count": pi_macro_count,
        "lean_exit_code": proc.returncode,
        "formal_build_report_provenance": formal_provenance,
        "per_theorem": per_theorem,
        "all_tc060_lean_checks_pass": bool(
            present
            and sorry_count == 0
            and admit_count == 0
            and custom_axiom_count == 0
            and pi_macro_count == 0
            and axioms_ok
        ),
    }


def verify_tc060_review_displayed_enclosures(
    report: Dict[str, Any],
    review_path: Path = TC_060_REVIEW_DOC_PATH,
) -> Dict[str, Any]:
    """Verify that `docs/reviews/TC_060_SIGNED_DILATION_ARITHMETIC_ENERGY.md` contains zero
    circle-half macros/glyphs and that every displayed `±` / `\\pm` interval carries an explicit
    `<!-- tc-enclosure: ... -->` tag outward-containing its generated 256-bit Arb ball.
    """
    text = review_path.read_text(encoding="utf-8")
    pi_macros = re.findall(r"\x5cpi(?![a-zA-Z])", text)
    pi_glyph_count = text.count("\u03c0")
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
        and pi_glyph_count == 0
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
        "pi_glyph_count": pi_glyph_count,
        "total_displayed_intervals_found": len(raw_intervals),
        "tagged_and_checked_count": len(checked_rows),
        "untagged_count": len(untagged_intervals),
        "failed_count": len(failed_intervals),
        "untagged_intervals": untagged_intervals,
        "failed_intervals": failed_intervals,
        "all_displayed_intervals_contain_generated_enclosures": all_ok,
    }


def execute_task_tc060_signed_dilation_audit(
    prec_bits: int = 256,
    verify_lean_live: bool = True,
    verify_review_doc: bool = True,
) -> Dict[str, Any]:
    """Execute the complete TASK-TC-060 / TASK-TC-060R mathematical, falsification, Lean, and 256-bit Arb audit."""
    sec1 = verify_section_1_exact_object_and_noncircular_reassembly(prec_bits=prec_bits)
    sec2 = verify_section_2_signed_dilation_fourier_and_gram_kernel(prec_bits=prec_bits)
    sec3 = verify_section_3_attempts_a_and_b_obstructions_and_drift_theorem(prec_bits=prec_bits)
    sec4 = verify_section_4_complete_energy_bridge_and_global_consequence(prec_bits=prec_bits)
    sec5 = verify_section_5_controls_schedule_and_directed_certificates(prec_bits=prec_bits)

    assert sec1["all_section_1_checks_pass"] is True
    assert sec2["all_section_2_checks_pass"] is True
    assert sec3["all_section_3_checks_pass"] is True
    assert sec4["all_section_4_checks_pass"] is True
    assert sec5["all_section_5_checks_pass"] is True

    report: Dict[str, Any] = {
        "task_id": TASK_TC_060R_ID,
        "repaired_task_id": TASK_TC_060_ID,
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
            TASK_TC_059R_ID,
            TASK_TC_059R2_ID,
            TASK_TC_060_ID,
        ],
        "reviewed_merged_main_baseline": REVIEWED_MERGED_MAIN_BASELINE,
        "accepted_tc059r2_branch": ACCEPTED_TC059R2_BRANCH,
        "reviewed_tc059r2_implementation_commit": REVIEWED_TC059R2_IMPLEMENTATION,
        "reviewed_tc059r2_head_commit": REVIEWED_TC059R2_HEAD,
        "prior_tc059r_formal_producing_commit": INHERITED_FORMAL_PRODUCING_COMMIT,
        "reviewed_tc060_branch": PROPOSED_TC060_BRANCH,
        "reviewed_tc060_implementation_commit": REVIEWED_TC060_IMPLEMENTATION,
        "reviewed_tc060_head_commit": REVIEWED_TC060_HEAD,
        "branch": REPAIR_TC060R_BRANCH,
        "epistemic_categories_enforced": list(EPISTEMIC_CATEGORIES),
        "global_consequence_classes_enforced": list(GLOBAL_CONSEQUENCE_CLASSES),
        "completion_outcome_code": "OUTCOME_B_AND_C_REPAIRED_FULL_CORE_QUANTIFIED_OBSTRUCTIONS_AND_DRIFT_CONTRACTION",
        "research_outcome_class": (
            "Repaired Full-Core Scope, Quantified Counterexamples, Certified Cutoffs, & Partial Arithmetic "
            "Relative-Contraction Theorem (TASK-TC-060R repairing TASK-TC-060, Outcome B/C) — Preserves "
            "exact finite-L Fourier block-multiplier representation (outside Lean) and real-space signed / "
            "(log X)^{-4}-weighted Gram kernels H_{Y,b}, H_{Y,b}^{wt}; proves in Lean 4 (0 sorry, 0 custom "
            "axioms, 7 public theorems in SignedDilationArithmeticEnergy.lean) non-circular reassembly & "
            "2T basis spillover, sharp unrestricted-frequency multiplier attainment (obstructing only a "
            "frequency-independent relative O(1/d) saving while retaining the all-v (1+|v|) derivative bound) "
            "and sqrt(T) cutoff-block lower bound, weighted Gram quadratic forms & log sandwiches, Gaussian "
            "window majorants & Gauss-product Gamma monotonicity, discrete Abel re-summation of M_{sq,2}(d) & "
            "finite small-divisor weighted bounds, R-independent complete-energy feedback transfer, and "
            "TC-060R's full-core intermediate/tail retention, singleton-block I_T(T)={1} Candidate A1 "
            "refutation at v=0, arbitrary-coefficient d=1/e_1 Candidate B1 exponential lower bound, "
            "w_{2,lambda}(p)/w_{2,lambda}(6p) unconditional support, and drift-jump floor(T/q) reindexing; "
            "proves outside Lean all-eps relative contraction of r_{sm,T(Y)}^{drift}/(log X)^2 (with corrected "
            "O(log Y) sub-unit and jump sums) and 1 <= d <= min(D_0(Y), T(Y)-1) (with certified D_0(2) = 0); "
            "and retains the full remaining open core min(D_0(Y), T(Y)-1) < d <= T(Y)-1 inside D_{2,core,T(Y)} "
            "(including d >= ceil(tau*Y)) alongside signed 8*X_tilde(Y) + 4*||D_{2,core,T(Y)}||_Y^2, keeping "
            "SUBGATE-TC-043A OPEN and rh_proved False."
        ),
        "subgate_tc043a_status": "OPEN",
        "rh_proved": False,
        "precision_bits": prec_bits,
        "circle_constant_convention": "tau (sole circle constant)",
        "complex_coordinate_convention": (
            "z = x + i*y (x, y real; critical line x = 1/2; displacement delta = x - 1/2); "
            "Fourier/Mellin w = u + i*v (u, v real); real algebraic grades K distinct from "
            "auxiliary log scales t = log X, frequencies v, and divisor shifts log d"
        ),
        "section_1_exact_object_and_noncircular_reassembly": sec1,
        "section_2_signed_dilation_fourier_and_gram_kernel": sec2,
        "section_3_attempts_a_and_b_obstructions_and_drift_theorem": sec3,
        "section_4_complete_energy_bridge_and_global_consequence": sec4,
        "section_5_controls_schedule_and_directed_certificates": sec5,
    }

    if verify_lean_live:
        lean_audit = verify_tc060_lean_theorems_live()
        assert lean_audit["all_tc060_lean_checks_pass"] is True, (
            f"TC-060 Lean theorem audit failed: {lean_audit}"
        )
        report["section_6_lean_formalization_audit"] = lean_audit

    arb_check = verify_all_serialized_arb_in_tree(report)
    assert arb_check["all_enclose_original_256bit_arb_ball"] is True, (
        f"Serialized Arb enclosure verification failed: {arb_check.get('failed_paths')}"
    )
    report["serialized_arb_self_check"] = arb_check

    if verify_review_doc and TC_060_REVIEW_DOC_PATH.exists():
        rev_audit = verify_tc060_review_displayed_enclosures(report, TC_060_REVIEW_DOC_PATH)
        assert rev_audit["all_displayed_intervals_contain_generated_enclosures"] is True, (
            "Displayed intervals in TC_060_SIGNED_DILATION_ARITHMETIC_ENERGY.md failed check: "
            f"pi_macros={rev_audit['pi_macro_count']}, pi_glyphs={rev_audit['pi_glyph_count']}, "
            f"untagged={rev_audit['untagged_intervals']}, failed={rev_audit['failed_intervals']}"
        )
        report["section_7_tc060_review_displayed_enclosures_audit"] = rev_audit

    return report


def write_task_tc060_signed_dilation_artifact(
    path: Path = SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH,
    prec_bits: int = 256,
    verify_lean_live: bool = True,
    verify_review_doc: bool = True,
) -> Dict[str, Any]:
    """Generate and write `data/tc_signed_dilation_arithmetic_energy.json`."""
    report = execute_task_tc060_signed_dilation_audit(
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
        json.dumps(cleaned, indent=2, sort_keys=False, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return cleaned


if __name__ == "__main__":
    rep = write_task_tc060_signed_dilation_artifact()
    print(
        f"Wrote {SIGNED_DILATION_ARITHMETIC_ENERGY_ARTIFACT_PATH} "
        f"(subgate={rep['subgate_tc043a_status']}, rh_proved={rep['rh_proved']})"
    )
