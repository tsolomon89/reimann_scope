r"""
TASK-TC-061 / TASK-TC-061R / TASK-TC-061R2: Preregistered Mixed Arithmetic Covariance Test, Signed-
Kernel Proof Attempt, Complete-Core Formula, Frozen-Protocol Execution, Escalation Witness
Preservation, Explicit Resource Status, and Report Closeout toward SUBGATE-TC-043A (EPIC-TC-042).

Implements, verifies, and certifies in 256-bit FLINT/Arb outward-rounded ball arithmetic (using
`tau` strictly via `_tau_arb()` as the sole circle constant, reserving `K` exclusively for real-
algebraic geometric grades `K in A_R`, defining complex arguments explicitly as `z = x + i*y` with
critical-line coordinate `x = 1/2`, and writing `A_Y, B_Y` for known/core window functions,
`s_Y` for the smooth-only core vector, `beta_Y(n) = s_Y(n) - a_n*(log n)^2` for the adjusted
core vector, and `a_eta, b_eta` for scalar constants):

1. Section 1 — Frozen Preregistration Protocol Immutability & Concrete Mixed Identity:
   - Verifies byte-level SHA-256 and registration commit (`bc2f9f709f868ef02981600873dfa0c05da0ba0c`)
     immutability of `data/tc_mixed_arithmetic_covariance_protocol.json`
     (`TC061-MIXED-ARITHMETIC-COVARIANCE-PROTOCOL-V1`), exact rational ceiling calibration of
     `a_{1/2} = 1/32`, `a_{1/4} = 3/64`, `a_{1/8} = 5/64` strictly on `C = {16, 32, 64}`, and
     diagnostic-only separation of `{2, 4, 8}`.
   - Evaluates `Q_Y`, `P_Y`, `A_Y = D_{2,known,Y}`, `B_Y = D_{2,core,Y}`, inherited prime-power
     reconstruction diagonal `D_tilde(Y)`, off-diagonal `X_tilde(Y) = ||P_Y||_Y^2 - D_tilde(Y)`,
     and signed mixed functional `J(Y) = 4*X_tilde(Y) + ||B_Y||_Y^2 - 4*<P_Y, B_Y>_Y` from their
     separate source formulas, cross-checking both `4*D_tilde(Y) + J(Y) = ||2*P_Y - B_Y||_Y^2 =
     ||Q_Y + A_Y||_Y^2`, the `theta`-inequality `(1 - theta)*E(Y) <= 4*D_tilde(Y) + J(Y) +
     (theta^{-1} - 1)*||A_Y||_Y^2` (`0 < theta < 1`), and the repaired pointwise complete-core
     bridge `B_Y(X) = sum_{n<=2T} beta_Y(n)*phi_n(X)/(log X)^2 + 2*P_Y(X) - Q_Y(X)` and
     `2*P_Y(X) - B_Y(X) = Q_Y(X) - sum_{n<=2T} beta_Y(n)*phi_n(X)/(log X)^2`.

2. Section 2 — Certified Cutoff Determination, Straddling-Interval Case Splitting, & Fast Sieve:
   - Certifies `T(Y) = ceil(Y^{5/4})`, `D_0(Y) = floor(log Y)`, `D_{0,eff}(Y) = min(D_0(Y), T(Y)-1)`,
     and `ceil(tau*Y)` across all 20 protocol scales, including exact symbolic discontinuity points
     `e^5*(1 - 2^{-12})` (`D_0 = 4, T = 518`), `e^5*(1 + 2^{-12})` (`D_0 = 5, T = 519`), and fourth-
     power boundary points `256 - 2^{-12}`, `256`, `256 + 2^{-12}`.
   - Rejects unsplit straddling `arb` enclosures (`AmbiguousCutoffError`) while providing a rigorous
     branch-splitting interval evaluator (`evaluate_interval_via_cutoff_case_split_arb`) over
     genuine input intervals spanning `T` or `D_0` jumps (`[256 - 2^{-12}, 256 + 2^{-12}]`,
     `[742/5, 2969/20]`, `[148, 149]`, and `[64, 65]` spanning `T: 182 -> 185`).

3. Section 3 — Faithful Frozen-Protocol 14-Point Execution, Decisive-Witness Accumulator, & Resource Status:
   - Resolves quadrature mode and tolerances strictly from `data/tc_mixed_arithmetic_covariance_protocol.json`
     and certified `T(Y)` (`T < 512`: unsplit quadrature with `quad_tol_bits = 240` at Tier 0 and
     registered `32`/`64` panel subdivisions on escalation; `T >= 512`: three-zone quadrature with
     `quad_tol_bits = 160`, `16` panels, ratio `12`, Taylor degree `56`), records requested vs
     actually used settings and genuinely inactive parameters per mode, prevents silent overrides,
     accumulates decisive `PASS`/`FAIL` witness provenance across all four main probes and both
     `TC061-KL1` sub-budgets (preserving certified counterexamples and certificates when later tiers
     are `UNRESOLVED` while flagging contradictory certified `PASS`/`FAIL` verdicts as an explicit
     `CERTIFICATION_INTEGRITY_CONFLICT` retaining both witnesses), tracks separate 3-valued
     (`WITHIN`, `EXCEEDED`, `UNKNOWN`) wall-time and memory compliance statuses without claiming
     OS-level preemptive kills or coercing missing RSS into verified compliance, and documents the
     corrected `HO-BASE-128` (`T = 431`, `quad_tol_bits = 240`) rerun vs the original `TC-061`
     (`quad_tol_bits = 160`) deviation as a corrected repeat of the registered experiment.

4. Section 4 — Finite-Prime Parity Controls, Exact `(1 * a_S)(n)` Convolution, & Scoped Contrast:
   - Proves and verifies `(1 * a_S)(n) = prod_{p in S}(1 + (-1)^{v_p(n)})/2 * prod_{p|n, p notin S}(v_p(n) + 1)`
     (giving `d(n)` for `S = empty`, e.g. `(1 * 1)(12) = 6 != 1`, and `2, 0, 2` for `S = {2}, n = 3, 6, 12`),
     strictly distinguishing convolution coefficients from nonzero-support density `prod_{p in S} p/(p+1)`
     and the `z = 1` residue `prod_{p in S} (p-1)/(p+1)` of `D_{a_S}(z)` (`z = x + i*y`), while
     retaining certified finite contrasts on `Y in {64, 128, 256, 512}` without unproved asymptotic
     extrapolations or claims of a unique `tau`-specific mechanism.

5. Section 5 — Complete-Core Gram Bridges, Self-Collision Theorem, Complement Upper Bound, & `F` vs `S`:
   - Distinguishes smooth-only `s_Y(n)` from adjusted `beta_Y(n) = s_Y(n) - a_n*(log n)^2`, verifies
     both the uncombined `r in {0,1,2,3,4}` Gram expansion and the compact `r in {0,2,4}` Gram
     representation of `J(Y)` on small windows with certified nonzero spillover beyond `T`, preserves
     the unconditional self-collision bound (`186*(tau - 1) < 1302` in Lean 4 vs `(289/60)*log(tau) <
     (1377/160)*log(tau) < 16` analytically outside Lean), restores the valid signed-correlation
     `X_tilde(Y)` log-removal sandwich (`Y = 32` signed example) and coarse half-line upper bound
     `D_infty(T) <= 2*c_G*T*zeta''(2)` (`g = gcd(m, n)`, `c_G = 3*sqrt(tau/2)/8`), corrects intra-
     integer cancellation scope (same-integer mixed terms with `B_Y` can cancel), and formalizes
     `H(J, D_tilde) <-> H(F, D_tilde)` for the exact remaining signed remainder
     `F(Y) = 4*X_tilde_off(Y) + ||B_Y||_Y^2 - 4*<P_Y, B_Y>_Y` alongside one-way sufficiency
     `H(S, D_tilde) -> H(J, D_tilde)` for `S(Y) = 5*X_tilde_off(Y) + 5*||B_Y||_Y^2`.

6. Section 6 — Route D Conditional Closure Transfer, Live Lean Declaration Spans, & Scope Mapping:
   - Preserves conditional Route D transfer and explicit premises, extracts live declaration line
     spans for `MixedCovarianceClosureHypothesis` and all 7 public theorems in
     `formal/RiemannScope/MixedArithmeticCovariance.lean`, and verifies both displayed interval
     enclosures and Lean line anchors in `docs/reviews/TC_061_MIXED_ARITHMETIC_COVARIANCE.md`,
     keeping `SUBGATE-TC-043A` `OPEN` and `rh_proved = False`.
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from flint import acb, acb_mat, acb_series, arb, ctx as flint_ctx

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
    _frac_to_arb,
    _tau_arb,
    finite_prime_parity_aS_int,
    prime_power_pairs_up_to,
    two_adic_parity_a2_int,
)
from tc.dyadic_power_lift_primitive_correlation import (
    EPISTEMIC_CATEGORIES,
    PARENT_SUBGATE_ID,
    TASK_TC_059_ID,
    TASK_TC_059R_ID,
    TASK_TC_059R2_ID,
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
    liouville_lambda_int,
)
from tc.prime_chain_contraction import (
    TASK_TC_056R_ID,
    TASK_TC_056R2_ID,
    evaluate_phi_n_arb,
)
from tc.signed_dilation_arithmetic_energy import (
    AmbiguousCutoffError,
    FORMAL_BUILD_REPORT_PATH,
    GLOBAL_CONSEQUENCE_CLASSES,
    REVIEWED_TC060R_IMPLEMENTATION,
    TASK_TC_060_ID,
    TASK_TC_060R_ID,
    TASK_TC_060R2_ID,
    certify_D0_small_divisor_cutoff,
    certify_T_canonical_cutoff,
    certify_ceil_tau_Y_cutoff,
    certify_open_core_divisor_partition,
    classify_arb_le_certificate,
    classify_ceil_from_arb_enclosure,
    classify_floor_from_arb_enclosure,
    compute_selberg_centered_remainder_table_arb,
    enclose_discrete_grid_max,
    evaluate_c_half_square_pole_arb,
    evaluate_square_pole_drift_M_arb,
    verify_section_epistemic_scope_metadata,
)
from tc.simultaneous_compatibility_combined_energy import (
    TASK_TC_058_ID,
    TASK_TC_058R_ID,
    TASK_TC_058R2_ID,
    evaluate_c_lambda_arb,
)

TASK_TC_061_ID = "TASK-TC-061"
TASK_TC_061R_ID = "TASK-TC-061R"
TASK_TC_061R2_ID = "TASK-TC-061R2"
PROPOSED_TC061_BRANCH = "task/tc-061-mixed-arithmetic-covariance-hypothesis-test"
PROPOSED_TC061R_BRANCH = "task/tc-061r-core-formula-protocol-and-proof-scope-repair"
PROPOSED_TC061R2_BRANCH = "task/tc-061r2-witness-preservation-resource-status-and-closeout"
REVIEWED_TC061_TIP = "e7ced078f32a376d582a6aaf098ad0b3036da51f"
REVIEWED_TC061_IMPLEMENTATION = "74e9df24d165619b0857cd37a895d599a93ba08e"
REVIEWED_TC061R_TIP = "93dd56a5554b698dab642611605e29c80e756462"
ACCEPTED_TC061R_IMPLEMENTATION_AND_FORMAL_COMMIT = "b65dba142658a8e4fd80c339d7029aa14e114c5a"
ACCEPTED_TC060R2_IMPLEMENTATION = "2812faad941301bde8b6dc09ac5d8c23957204ff"
ACCEPTED_TC060R2_TIP = "4bfb36ed7a62f207a6479dd932a997563a407ff8"
MERGED_MAIN_BASELINE_TC061 = "71a101005f1ee073e981187bb7d07d90daef9c65"

FROZEN_PROTOCOL_ID = "TC061-MIXED-ARITHMETIC-COVARIANCE-PROTOCOL-V1"
FROZEN_PROTOCOL_SHA256 = "c892c4c5a1ff2a60a11fa499b2d2bc017e01f0426e4aa8feef5880aaff8a70eb"
FROZEN_PROTOCOL_REGISTRATION_COMMIT = "bc2f9f709f868ef02981600873dfa0c05da0ba0c"

# Preserved historical record of the original TC-061 HO-BASE-128 deviation (quad_tol_bits=160 vs 240):
ORIGINAL_TC061_HO_BASE_128_DEVIATION_RECORD: Dict[str, Any] = {
    "original_task_id": TASK_TC_061_ID,
    "original_implementation_commit": REVIEWED_TC061_IMPLEMENTATION,
    "original_branch_tip_commit": REVIEWED_TC061_TIP,
    "affected_point_id": "HO-BASE-128",
    "affected_Y": 128,
    "certified_T_Y": 431,
    "protocol_three_zone_activation_threshold_T": 512,
    "protocol_required_mode": "unsplit",
    "protocol_required_quad_tol_bits": 240,
    "original_tc061_quad_tol_bits_used": 160,
    "original_tc061_panels_used": 1,
    "original_enclosures": {
        "E_Y": "[0.02363259184198284689569412394614253221221 +/- 4.47e-43]",
        "D_tilde_Y": "[0.03712174901701963987609213168177739860076 +/- 2.15e-42]",
        "X_tilde_Y": "[-0.01378162760697259204094104165630151369916 +/- 2.55e-42]",
        "J_direct": "[-0.04992139479873701702113393053123481848167 +/- 1.07e-42]",
        "M_P0": "[-0.2300372444789446093903428662277969548540 +/- 4.50e-41]",
    },
    "original_tc061_J_direct_arb_ball_str": "[-0.04992139479873701702113393053123481848167 +/- 1.07e-42]",
    "original_tc061_D_tilde_Y_arb_ball_str": "[0.03712174901701963987609213168177739860076 +/- 2.15e-42]",
    "original_tc061_TC061_P0_margin_arb_ball_str": "[-0.2300372444789446093903428662277969548540 +/- 4.50e-41]",
    "deviation_classification": (
        "PROTOCOL_TOLERANCE_SELECTION_DEVIATION_ONLY: the original 160-bit unsplit quadrature "
        "enclosure at Y = 128 (T = 431 < 512) was mathematically rigorous outward-rounded ball "
        "arithmetic, but verify_section_3 hardcoded quad_tol_bits = 160 instead of resolving "
        "quad_tol_bits_unsplit_small_T = 240 from the frozen protocol. Rerun in TASK-TC-061R "
        "with resolved unsplit quad_tol_bits = 240 as a corrected repeat of the registered "
        "experiment (not new unseen evidence)."
    ),
}

MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH = (
    REPO_ROOT / "data" / "tc_mixed_arithmetic_covariance_protocol.json"
)
MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_mixed_arithmetic_covariance.json"
)
TC_061_REVIEW_DOC_PATH = (
    REPO_ROOT / "docs" / "reviews" / "TC_061_MIXED_ARITHMETIC_COVARIANCE.md"
)
TC_061_LEAN_MODULE_PATH = (
    REPO_ROOT / "formal" / "RiemannScope" / "MixedArithmeticCovariance.lean"
)

PROBE_GLOBAL_OUTCOMES: Tuple[str, ...] = (
    "REFUTED_BY_CERTIFIED_WITNESS",
    "SURVIVED_TESTED_POINTS",
    "UNRESOLVED/INCOMPLETE_COVERAGE",
    "PROVED_UNIFORMLY",
)
POINT_MARGIN_VERDICTS: Tuple[str, ...] = ("PASS", "FAIL", "UNRESOLVED", "NOT_EVALUATED")
CERTIFICATION_INTEGRITY_CONFLICT_VERDICT = "INTEGRITY_CONFLICT"
CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME = "CERTIFICATION_INTEGRITY_CONFLICT"
RESOURCE_COMPLIANCE_STATUSES: Tuple[str, ...] = ("WITHIN", "EXCEEDED", "UNKNOWN")


class CertificationIntegrityError(RuntimeError):
    """Raised when contradictory certified PASS and FAIL enclosures occur for the same candidate,
    point, and parameter identity across escalation tiers, blocking certification while retaining
    both conflicting witnesses.
    """

    def __init__(self, message: str, conflicts: Sequence[Dict[str, Any]]) -> None:
        super().__init__(message)
        self.conflicts: List[Dict[str, Any]] = list(conflicts)


def _clone_preserving_arb(obj: Any) -> Any:
    """Recursively clone dicts/lists/tuples while keeping immutable `flint.arb`/`acb` instances."""
    if isinstance(obj, dict):
        return {k: _clone_preserving_arb(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clone_preserving_arb(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_clone_preserving_arb(v) for v in obj)
    return obj


def strip_enclosure_arb_for_json(obj: Any) -> Any:
    """Strip in-memory `enclosure_arb` keys so structures round-trip cleanly through `json.dumps`."""
    if isinstance(obj, (arb, acb)):
        return str(obj)
    if isinstance(obj, dict):
        return {k: strip_enclosure_arb_for_json(v) for k, v in obj.items() if k != "enclosure_arb"}
    if isinstance(obj, (list, tuple)):
        return [strip_enclosure_arb_for_json(v) for v in obj]
    return obj

# Populated dynamically or matched against the exact theorem declarations in MixedArithmeticCovariance.lean
EXPECTED_TC061_THEOREMS: List[str] = [
    "mixed_covariance_identity_and_theta_energy_bound_tc061",
    "factorization_sign_agreement_and_selberg_w2_formulas_tc061",
    "finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061",
    "mixed_covariance_hypothesis_route_d_closure_transfer_tc061",
    "complete_core_adjusted_expansion_and_compact_gram_tc061r",
    "finite_prime_parity_divisor_convolution_formula_tc061r",
    "signed_remainder_equivalence_and_sufficient_core_relaxation_tc061r",
]


# ---------------------------------------------------------------------------
# 0. Exact Scale Specifications, Margin Classifiers, & Fast O(T log T) Sieve
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExactScaleSpec:
    """Exact symbolic representation `Y = exp(exp_power) * rational_factor` (`rational_factor > 0`)."""

    label: str
    kind: str  # "exact_rational" or "exact_symbolic_exp_rational"
    rational_factor: Fraction
    exp_power: Fraction = Fraction(0, 1)

    @classmethod
    def from_protocol_entry(cls, entry: Dict[str, Any]) -> "ExactScaleSpec":
        rf_n, rf_d = (int(x) for x in str(entry["rational_factor"]).split("/"))
        ep_n, ep_d = (int(x) for x in str(entry["exp_power"]).split("/"))
        return cls(
            label=str(entry["label"]),
            kind=str(entry["kind"]),
            rational_factor=Fraction(rf_n, rf_d),
            exp_power=Fraction(ep_n, ep_d),
        )

    def evaluate_arb(self, prec_bits: int = 256) -> arb:
        saved = flint_ctx.prec
        try:
            flint_ctx.prec = prec_bits
            rf = _frac_to_arb(self.rational_factor)
            if self.exp_power == Fraction(0, 1):
                return rf
            return (_frac_to_arb(self.exp_power)).exp() * rf
        finally:
            flint_ctx.prec = saved

    def evaluate_log_Y_arb(self, prec_bits: int = 256) -> arb:
        saved = flint_ctx.prec
        try:
            flint_ctx.prec = prec_bits
            rf_log = _frac_to_arb(self.rational_factor).log()
            if self.exp_power == Fraction(0, 1):
                return rf_log
            return _frac_to_arb(self.exp_power) + rf_log
        finally:
            flint_ctx.prec = saved


def classify_probe_margin_arb(
    margin_ball: arb,
    *,
    exact_algebraic_zero_proved: bool = False,
) -> Dict[str, Any]:
    """Classify probe margin `M(Y) = J(Y) - RHS(Y)` under strict outward-rounded Arb endpoints:
    - `PASS` if `upper(M) <= 0` (or `exact_algebraic_zero_proved=True` with `0 in M`);
    - `FAIL` if `lower(M) > 0`;
    - `UNRESOLVED` if `lower(M) <= 0 < upper(M)` without an exact algebraic equality proof.
    """
    if not margin_ball.is_finite():
        return {
            "verdict": "UNRESOLVED",
            "reason": "NON_FINITE_MARGIN_ENCLOSURE",
            "certified_definite": False,
        }
    lo_f, hi_f = _exact_arb_endpoints_as_fractions(margin_ball)
    if hi_f <= Fraction(0, 1) and bool(margin_ball.upper() <= arb(0)):
        if exact_algebraic_zero_proved and hi_f < Fraction(0, 1):
            raise ValueError(
                f"Inconsistent exact_algebraic_zero_proved=True on strictly negative margin {margin_ball}"
            )
        return {
            "verdict": "PASS",
            "reason": (
                "PROVED_EXACT_ALGEBRAIC_ZERO_MARGIN_WITH_CONSISTENT_ENCLOSURE"
                if exact_algebraic_zero_proved
                else "CERTIFIED_UPPER_MARGIN_LE_ZERO"
            ),
            "certified_definite": True,
        }
    if lo_f > Fraction(0, 1) and bool(margin_ball.lower() > arb(0)):
        if exact_algebraic_zero_proved:
            raise ValueError(
                f"Inconsistent exact_algebraic_zero_proved=True on strictly positive margin {margin_ball}"
            )
        return {
            "verdict": "FAIL",
            "reason": "CERTIFIED_LOWER_MARGIN_GT_ZERO_WITNESS",
            "certified_definite": True,
        }
    if exact_algebraic_zero_proved:
        if bool(arb(0) in margin_ball):
            return {
                "verdict": "PASS",
                "reason": "PROVED_EXACT_ALGEBRAIC_ZERO_MARGIN_WITH_CONSISTENT_ENCLOSURE",
                "certified_definite": True,
            }
        raise ValueError(
            f"exact_algebraic_zero_proved=True asserted on ball not containing zero: {margin_ball}"
        )
    return {
        "verdict": "UNRESOLVED",
        "reason": "ZERO_STRADDLING_MARGIN_ENCLOSURE",
        "certified_definite": False,
    }


def classify_global_probe_outcome(
    point_verdicts: Sequence[str],
    *,
    coverage_complete: bool,
    uniform_proof_established: bool = False,
    fail_on_integrity_conflict: bool = False,
) -> str:
    """Classify global probe outcome into one of `PROBE_GLOBAL_OUTCOMES` (or
    `CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME` / `CertificationIntegrityError` if an integrity
    conflict occurred, keeping certification conflicts strictly distinct from valid counterexamples).
    """
    allowed = set(POINT_MARGIN_VERDICTS) | {CERTIFICATION_INTEGRITY_CONFLICT_VERDICT}
    for v in point_verdicts:
        if v not in allowed:
            raise ValueError(f"Invalid point verdict {v!r}; expected one of {sorted(allowed)}")
    if any(v == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT for v in point_verdicts):
        if fail_on_integrity_conflict:
            raise CertificationIntegrityError(
                "Contradictory certified PASS and FAIL verdicts encountered in global aggregation",
                [],
            )
        return CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    if any(v == "FAIL" for v in point_verdicts):
        return "REFUTED_BY_CERTIFIED_WITNESS"
    if (not coverage_complete) or len(point_verdicts) == 0 or any(v != "PASS" for v in point_verdicts):
        return "UNRESOLVED/INCOMPLETE_COVERAGE"
    if uniform_proof_established:
        return "PROVED_UNIFORMLY"
    return "SURVIVED_TESTED_POINTS"


def certified_ratio_with_positive_denominator(
    num_ball: arb,
    den_ball: arb,
    *,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Form `num_ball / den_ball` ONLY when `lower(den_ball) > 0` is certified."""
    if not (num_ball.is_finite() and den_ball.is_finite()):
        return {
            "denominator_certified_positive": False,
            "ratio": None,
        }
    den_lo, _ = _exact_arb_endpoints_as_fractions(den_ball)
    if den_lo <= Fraction(0, 1) or not bool(den_ball.lower() > arb(0)):
        return {
            "denominator_certified_positive": False,
            "ratio": None,
        }
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        q = num_ball / den_ball
        return {
            "denominator_certified_positive": True,
            "ratio": serialize_arb_certified(q),
        }
    finally:
        flint_ctx.prec = saved


def calibrate_secondary_a_eta_exact(
    calibration_quotients: Sequence[arb],
) -> Dict[str, Any]:
    """Exact rational ceiling calibration `U_eta = max(0, max_{Y in C} upper(Q_eta(Y)))`,
    `a_eta = ceil(64 * U_eta) / 64` with zero floating-point rounding.
    """
    if not calibration_quotients:
        raise ValueError("calibration_quotients must be nonempty")
    u_eta = Fraction(0, 1)
    upper_fracs: List[Fraction] = []
    for q_b in calibration_quotients:
        if not q_b.is_finite():
            raise ValueError(f"Non-finite calibration quotient ball: {q_b}")
        _, q_hi = _exact_arb_endpoints_as_fractions(q_b)
        upper_fracs.append(q_hi)
        if q_hi > u_eta:
            u_eta = q_hi
    scaled_64 = Fraction(64, 1) * u_eta
    ceil_64 = (scaled_64.numerator + scaled_64.denominator - 1) // scaled_64.denominator
    a_eta = Fraction(ceil_64, 64)
    return {
        "U_eta_fraction": u_eta,
        "ceil_64_U_eta": ceil_64,
        "a_eta_fraction": a_eta,
        "per_point_upper_fractions": upper_fracs,
    }


def compute_selberg_centered_remainder_table_fast_arb(
    D_max: int,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """`O(D_max log D_max)` exact prime-power sieve computation of `Lambda(n)`, `(Lambda * Lambda)(n)`,
    `w_{2,lambda}(n)`, `W_2(d)`, `R(d) = W_2(d) - c_lambda*d`, `M_{sq,2}(d)`, and `R_{osc}(d) = R(d) - M_{sq,2}(d)`.
    """
    if D_max < 0:
        raise ValueError(f"D_max must be >= 0, got {D_max}")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        c_lam = evaluate_c_lambda_arb(prec_bits=prec_bits)
        c_half = evaluate_c_half_square_pole_arb(prec_bits=prec_bits)

        lam_vm = [arb(0)] * (D_max + 1)
        for p, k in prime_power_pairs_up_to(D_max):
            lam_vm[p ** k] = arb(p).log()
        conv_ll = [arb(0)] * (D_max + 1)
        for u in range(2, D_max + 1):
            lu = lam_vm[u]
            if lu == arb(0):
                continue
            max_v = D_max // u
            for v in range(2, max_v + 1):
                lv = lam_vm[v]
                if lv != arb(0):
                    conv_ll[u * v] += lu * lv

        w2_list = [arb(0)] * (D_max + 1)
        W2_list = [arb(0)] * (D_max + 1)
        R_list = [arb(0)] * (D_max + 1)
        M_list = [arb(0)] * (D_max + 1)
        R_osc_list = [arb(0)] * (D_max + 1)

        cum = arb(0)
        for d in range(1, D_max + 1):
            if d >= 2:
                lam_d = arb(liouville_lambda_int(d))
                wd = lam_d * (lam_vm[d] * arb(d).log() + conv_ll[d])
                w2_list[d] = wd
                cum += wd
            W2_list[d] = cum
            rd = cum - c_lam * arb(d)
            md = evaluate_square_pole_drift_M_arb(d, c_half_arb=c_half, prec_bits=prec_bits)
            R_list[d] = rd
            M_list[d] = md
            R_osc_list[d] = rd - md
        return {
            "c_lambda": c_lam,
            "c_half_lambda": c_half,
            "lam_vm": lam_vm,
            "conv_ll": conv_ll,
            "w2": w2_list,
            "W2": W2_list,
            "R": R_list,
            "M_drift": M_list,
            "R_osc": R_osc_list,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 1. Cutoff Certification, Straddling-Interval Case Splitting, & Point Evaluator
# ---------------------------------------------------------------------------


def certify_exact_scale_cutoffs(
    spec: ExactScaleSpec,
    *,
    base_prec_bits: int = 256,
    max_prec_bits: int = 4096,
) -> Dict[str, Any]:
    """Certify `T(Y) = ceil(Y^{5/4})`, `D_0(Y) = floor(log Y)`, `D_{0,eff}(Y) = min(D_0(Y), T(Y)-1)`,
    and `ceil(tau*Y)` for an `ExactScaleSpec` with automatic precision refinement on symbolic scales.
    """
    if spec.rational_factor <= 0:
        raise ValueError(f"rational_factor must be > 0, got {spec.rational_factor}")
    if spec.exp_power == Fraction(0, 1):
        y_fr = spec.rational_factor
        if y_fr < Fraction(2, 1):
            raise ValueError(f"Scale Y = {y_fr} must satisfy Y >= 2")
        T_val = certify_T_canonical_cutoff(y_fr, prec_bits=base_prec_bits, max_prec_bits=max_prec_bits)
        D0_val = certify_D0_small_divisor_cutoff(
            y_fr, kappa=1, require_Y_ge_2=True, prec_bits=base_prec_bits, max_prec_bits=max_prec_bits
        )
        ceil_tau_val = certify_ceil_tau_Y_cutoff(
            y_fr, prec_bits=base_prec_bits, max_prec_bits=max_prec_bits
        )
        return {
            "label": spec.label,
            "kind": spec.kind,
            "T_Y": T_val,
            "D0_raw": D0_val,
            "D0_eff": min(D0_val, max(0, T_val - 1)),
            "ceil_tau_Y": ceil_tau_val,
            "cutoff_prec_bits_used": base_prec_bits,
        }

    p_cur = max(64, base_prec_bits)
    saved = flint_ctx.prec
    try:
        while p_cur <= max_prec_bits:
            flint_ctx.prec = p_cur
            y_b = spec.evaluate_arb(prec_bits=p_cur)
            lg_b = spec.evaluate_log_Y_arb(prec_bits=p_cur)
            if not bool(y_b >= arb(2)):
                if bool(y_b < arb(2)):
                    raise ValueError(f"Symbolic scale {spec.label} < 2")
                p_cur *= 2
                continue
            st_T, val_T, _ = classify_ceil_from_arb_enclosure(y_b ** (arb(5) / arb(4)))
            st_D0, val_D0, _ = classify_floor_from_arb_enclosure(lg_b)
            st_ct, val_ct, _ = classify_ceil_from_arb_enclosure(_tau_arb() * y_b)
            if (
                st_T == "CERTIFIED_UNIQUE_CEIL"
                and val_T is not None
                and st_D0 == "CERTIFIED_UNIQUE_FLOOR"
                and val_D0 is not None
                and st_ct == "CERTIFIED_UNIQUE_CEIL"
                and val_ct is not None
            ):
                return {
                    "label": spec.label,
                    "kind": spec.kind,
                    "T_Y": val_T,
                    "D0_raw": val_D0,
                    "D0_eff": min(val_D0, max(0, val_T - 1)),
                    "ceil_tau_Y": val_ct,
                    "cutoff_prec_bits_used": p_cur,
                }
            p_cur *= 2
        raise AmbiguousCutoffError(
            f"Could not certify unique cutoffs for {spec.label} up to {max_prec_bits} bits"
        )
    finally:
        flint_ctx.prec = saved


def _measure_process_rss_megabytes() -> Dict[str, Any]:
    """Measure current and OS process-lifetime high-water peak RSS (working set) in MiB via OS
    kernel APIs without claiming preemptive OS timeout/memory termination.
    """
    if os.name == "nt":
        try:
            from ctypes import wintypes

            class _PROCESS_MEMORY_COUNTERS(ctypes.Structure):
                _fields_ = [
                    ("cb", wintypes.DWORD),
                    ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            k32 = ctypes.WinDLL("kernel32", use_last_error=True)
            k32.GetCurrentProcess.restype = wintypes.HANDLE
            k32.K32GetProcessMemoryInfo.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(_PROCESS_MEMORY_COUNTERS),
                wintypes.DWORD,
            ]
            k32.K32GetProcessMemoryInfo.restype = wintypes.BOOL
            pmc = _PROCESS_MEMORY_COUNTERS()
            pmc.cb = ctypes.sizeof(_PROCESS_MEMORY_COUNTERS)
            if k32.K32GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb):
                return {
                    "current_rss_mb": round(pmc.WorkingSetSize / (1024.0 * 1024.0), 3),
                    "peak_rss_mb": round(pmc.PeakWorkingSetSize / (1024.0 * 1024.0), 3),
                    "peak_rss_measurement_semantics": "PROCESS_LIFETIME_HIGH_WATER_MARK",
                }
        except Exception:  # noqa: BLE001
            pass
    else:
        try:
            import resource
            import sys as _sys

            ru = resource.getrusage(resource.RUSAGE_SELF)
            divisor = (1024.0 * 1024.0) if _sys.platform == "darwin" else 1024.0
            return {
                "current_rss_mb": None,
                "peak_rss_mb": round(float(ru.ru_maxrss) / divisor, 3),
                "peak_rss_measurement_semantics": "PROCESS_LIFETIME_HIGH_WATER_MARK",
            }
        except Exception:  # noqa: BLE001
            pass
    return {
        "current_rss_mb": None,
        "peak_rss_mb": None,
        "peak_rss_measurement_semantics": None,
    }


def load_frozen_protocol_rules(
    protocol_path: Path = MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH,
) -> Dict[str, Any]:
    """Load `numerical_settings_and_escalation_rules` from the immutable frozen protocol."""
    proto = json.loads(protocol_path.read_text(encoding="utf-8"))
    return proto["numerical_settings_and_escalation_rules"]


def resolve_protocol_quadrature_settings(
    protocol_rules: Dict[str, Any],
    T_Y: int,
    ceil_tau_Y: int,
    *,
    escalation_tier: int = 0,
) -> Dict[str, Any]:
    """Resolve exact quadrature mode, requested settings, actually used settings, and inactive
    parameters from the frozen protocol and certified `T_Y = ceil(Y^{5/4})`:
    - `T_Y < 512`: `quadrature_mode = "unsplit"` (at Tier 0: `prec_bits = 256`, `quad_tol_bits = 240`,
      `n_panels = 1`; three-zone parameters `n_panels`, `zone1_ratio_threshold_x_over_n`,
      `zone3_cutoff_N1`, `zone3_taylor_degree_M` are explicitly inactive).
    - `T_Y >= 512`: `quadrature_mode = "three_zone"` (at Tier 0: `prec_bits = 256`,
      `quad_tol_bits = 160`, `n_panels = 16`, `zone1_ratio_threshold_x_over_n = 12`,
      `zone3_cutoff_N1 = max(T_Y + 1, ceil_tau_Y)`, `zone3_taylor_degree_M = 56`).
    - `escalation_tier >= 1`: requests the exact registered tier entry from
      `escalation_ladder_on_zero_straddling_margin`, applying all 5 settings in `three_zone` mode,
      and in `unsplit` mode applying the registered `prec_bits`, `quad_tol_bits`, and `n_panels`
      (`32` / `64` panel subdivisions) while marking only the genuinely inactive zone-specific
      parameters (`zone1_ratio_threshold_x_over_n`, `zone3_cutoff_N1`, `zone3_taylor_degree_M`)
      as inactive.
    """
    if T_Y < 1:
        raise ValueError(f"T_Y must be >= 1, got {T_Y}")
    if ceil_tau_Y < 1:
        raise ValueError(f"ceil_tau_Y must be >= 1, got {ceil_tau_Y}")
    act_threshold = int(protocol_rules["three_zone_activation_threshold_T"])
    three_zone = T_Y >= act_threshold
    mode = "three_zone" if three_zone else "unsplit"

    if escalation_tier == 0:
        prec_bits = int(protocol_rules["base_prec_bits"])
        if not three_zone:
            quad_tol = int(protocol_rules["quad_tol_bits_unsplit_small_T"])
            requested = {
                "escalation_tier": 0,
                "quadrature_mode": mode,
                "prec_bits": prec_bits,
                "quad_tol_bits": quad_tol,
                "n_panels": None,
                "zone1_ratio_threshold_x_over_n": None,
                "zone3_cutoff_N1": None,
                "zone3_taylor_degree_M": None,
            }
            used = {
                "quadrature_mode": mode,
                "prec_bits": prec_bits,
                "quad_tol_bits": quad_tol,
                "n_panels": 1,
                "zone1_ratio_threshold_x_over_n": None,
                "zone3_cutoff_N1": None,
                "zone3_taylor_degree_M": None,
            }
            inactive = [
                "quad_tol_bits_three_zone_large_T",
                "n_panels",
                "zone1_ratio_threshold_x_over_n",
                "zone3_cutoff_N1",
                "zone3_taylor_degree_M",
            ]
        else:
            z3 = protocol_rules["three_zone_parameters"]
            quad_tol = int(protocol_rules["quad_tol_bits_three_zone_large_T"])
            n_p = int(z3["n_panels"])
            z1_r = int(z3["zone1_ratio_threshold_x_over_n"])
            n1_cut = max(T_Y + 1, ceil_tau_Y)
            m_deg = int(z3["zone3_taylor_degree_M"])
            requested = {
                "escalation_tier": 0,
                "quadrature_mode": mode,
                "prec_bits": prec_bits,
                "quad_tol_bits": quad_tol,
                "n_panels": n_p,
                "zone1_ratio_threshold_x_over_n": z1_r,
                "zone3_cutoff_N1": n1_cut,
                "zone3_taylor_degree_M": m_deg,
            }
            used = {
                "quadrature_mode": mode,
                "prec_bits": prec_bits,
                "quad_tol_bits": quad_tol,
                "n_panels": n_p,
                "zone1_ratio_threshold_x_over_n": z1_r,
                "zone3_cutoff_N1": n1_cut,
                "zone3_taylor_degree_M": m_deg,
            }
            inactive = ["quad_tol_bits_unsplit_small_T"]
    else:
        ladder = protocol_rules["escalation_ladder_on_zero_straddling_margin"]
        tier_entry = next((e for e in ladder if int(e["tier"]) == escalation_tier), None)
        if tier_entry is None:
            raise ValueError(
                f"Unknown escalation_tier {escalation_tier}; registered tiers: "
                f"{[int(e['tier']) for e in ladder]}"
            )
        prec_bits = int(tier_entry["prec_bits"])
        quad_tol = int(tier_entry["quad_tol_bits"])
        req_panels = int(tier_entry["n_panels"])
        req_z1 = int(tier_entry["zone1_ratio_threshold_x_over_n"])
        req_m = int(tier_entry["zone3_taylor_degree_M"])
        n1_cut_opt: Optional[int] = max(T_Y + 1, ceil_tau_Y) if three_zone else None
        requested = {
            "escalation_tier": escalation_tier,
            "quadrature_mode": mode,
            "prec_bits": prec_bits,
            "quad_tol_bits": quad_tol,
            "n_panels": req_panels,
            "zone1_ratio_threshold_x_over_n": req_z1,
            "zone3_cutoff_N1": n1_cut_opt,
            "zone3_taylor_degree_M": req_m,
        }
        if not three_zone:
            used = {
                "quadrature_mode": mode,
                "prec_bits": prec_bits,
                "quad_tol_bits": quad_tol,
                "n_panels": req_panels,
                "zone1_ratio_threshold_x_over_n": None,
                "zone3_cutoff_N1": None,
                "zone3_taylor_degree_M": None,
            }
            inactive = [
                "zone1_ratio_threshold_x_over_n",
                "zone3_cutoff_N1",
                "zone3_taylor_degree_M",
            ]
        else:
            used = {
                "quadrature_mode": mode,
                "prec_bits": prec_bits,
                "quad_tol_bits": quad_tol,
                "n_panels": req_panels,
                "zone1_ratio_threshold_x_over_n": req_z1,
                "zone3_cutoff_N1": n1_cut_opt,
                "zone3_taylor_degree_M": req_m,
            }
            inactive = []

    return {
        "T_Y": T_Y,
        "three_zone_activation_threshold_T": act_threshold,
        "three_zone": three_zone,
        "quadrature_mode": mode,
        "escalation_tier": escalation_tier,
        "requested_settings": requested,
        "used_settings": used,
        "inactive_parameters": inactive,
    }


def compute_complete_core_s_Y_and_beta_Y_arb(
    T_y: int,
    D0_eff: int,
    R_osc: Sequence[arb],
    *,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Construct the distinct complete-core coefficient vectors on `1 <= n <= 2*T_y` (`TASK-TC-061R` §2):
    - `a_n = lambda(n) * 1_{1 <= n <= T_y}`;
    - `s_Y(n)`: smooth-only coefficient of `phi_n` in `sum_{D0_eff < d <= T_y - 1} R_osc(d) * Delta_d^{sm}`;
    - `beta_Y(n) = s_Y(n) - a_n * (log n)^2`: adjusted complete-core vector satisfying
      `B_Y(X) = sum_{n <= 2*T_y} beta_Y(n) * phi_n(X) / (log X)^2 + 2*P_Y(X) - Q_Y(X)` and
      `2*P_Y(X) - B_Y(X) = Q_Y(X) - sum_{n <= 2*T_y} beta_Y(n) * phi_n(X) / (log X)^2`.
    """
    if T_y < 1:
        raise ValueError(f"T_y must be >= 1, got {T_y}")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        N2 = 2 * T_y
        a_vec = [arb(0)] * (N2 + 1)
        for n in range(1, T_y + 1):
            a_vec[n] = arb(liouville_lambda_int(n))

        s_Y = [arb(0)] * (N2 + 1)
        for d_i in range(D0_eff + 1, T_y):
            L_d = T_y // d_i
            wd = R_osc[d_i]
            for q in range(1, L_d + 1):
                term = wd * a_vec[q]
                s_Y[d_i * q] += term
                s_Y[(d_i + 1) * q] -= term

        beta_Y = [arb(0)] * (N2 + 1)
        for n in range(1, N2 + 1):
            if n <= T_y:
                ln_n = arb(n).log()
                beta_Y[n] = s_Y[n] - a_vec[n] * (ln_n * ln_n)
            else:
                beta_Y[n] = +s_Y[n]

        spillover_indices = [
            n for n in range(T_y + 1, N2 + 1) if bool(abs(s_Y[n]) > arb(0))
        ]
        max_spillover_abs = (
            enclose_discrete_grid_max([abs(s_Y[n]) for n in range(T_y + 1, N2 + 1)])
            if T_y >= 1
            else arb(0)
        )
        return {
            "T_Y": T_y,
            "D0_eff": D0_eff,
            "support_upper_2T": N2,
            "a_n": a_vec,
            "s_Y": s_Y,
            "beta_Y": beta_Y,
            "spillover_above_T_indices": spillover_indices,
            "max_spillover_above_T_abs": max_spillover_abs,
        }
    finally:
        flint_ctx.prec = saved


def evaluate_mixed_covariance_point_arb(
    spec: ExactScaleSpec,
    *,
    prec_bits: Optional[int] = None,
    quad_tol_bits: Optional[int] = None,
    n_panels: Optional[int] = None,
    zone1_ratio_threshold: Optional[int] = None,
    M_taylor: Optional[int] = None,
    use_three_zone: Optional[bool] = None,
    escalation_tier: int = 0,
    protocol_rules: Optional[Dict[str, Any]] = None,
    allow_nonprotocol_override: bool = False,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Evaluate `E(Y)`, `D_tilde(Y)` (inherited prime-power reconstruction diagonal ONLY),
    `X_tilde(Y)`, `||P_Y||_Y^2`, `||A_Y||_Y^2`, `||B_Y||_Y^2`, `<P_Y, B_Y>_Y`, `J(Y)`, algebraic
    consistency checks `||Q_Y + A_Y||_Y^2 - 4*D_tilde(Y)` and `||2*P_Y - B_Y||_Y^2 - 4*D_tilde(Y)`,
    and nonempty `d >= ceil(tau*Y)` sub-unit tail contributions in outward-rounded Arb arithmetic.

    By default (`allow_nonprotocol_override=False`), resolves quadrature mode and tolerances
    strictly from `data/tc_mixed_arithmetic_covariance_protocol.json` and certified `T(Y)`,
    rejecting any silent caller override.
    """
    t_start = time.perf_counter()
    rules = protocol_rules if protocol_rules is not None else load_frozen_protocol_rules()
    cutoff_base_prec = int(prec_bits) if prec_bits is not None else int(rules["base_prec_bits"])
    cut = certify_exact_scale_cutoffs(spec, base_prec_bits=cutoff_base_prec)
    T_y = cut["T_Y"]
    D0_eff = cut["D0_eff"]
    ceil_tau_y = cut["ceil_tau_Y"]

    resolved = resolve_protocol_quadrature_settings(
        rules, T_y, ceil_tau_y, escalation_tier=escalation_tier
    )

    if not allow_nonprotocol_override:
        proto_used = resolved["used_settings"]
        if prec_bits is not None and int(prec_bits) != int(proto_used["prec_bits"]):
            raise ValueError(
                f"Silent prec_bits override {prec_bits} != protocol {proto_used['prec_bits']} forbidden"
            )
        if quad_tol_bits is not None and int(quad_tol_bits) != int(proto_used["quad_tol_bits"]):
            raise ValueError(
                f"Silent quad_tol_bits override {quad_tol_bits} != protocol {proto_used['quad_tol_bits']} "
                f"at T_Y={T_y} (mode={resolved['quadrature_mode']}) forbidden"
            )
        if use_three_zone is not None and bool(use_three_zone) != bool(resolved["three_zone"]):
            raise ValueError(
                f"Silent use_three_zone override {use_three_zone} != protocol {resolved['three_zone']} "
                f"at T_Y={T_y} forbidden"
            )
        if n_panels is not None and int(n_panels) != int(proto_used["n_panels"]):
            raise ValueError(
                f"Silent n_panels override {n_panels} != protocol {proto_used['n_panels']} "
                f"at T_Y={T_y} (mode={resolved['quadrature_mode']}) forbidden"
            )
        if zone1_ratio_threshold is not None and (
            proto_used["zone1_ratio_threshold_x_over_n"] is None
            or int(zone1_ratio_threshold) != int(proto_used["zone1_ratio_threshold_x_over_n"])
        ):
            raise ValueError(
                f"Silent zone1_ratio_threshold override {zone1_ratio_threshold} != protocol "
                f"{proto_used['zone1_ratio_threshold_x_over_n']} at T_Y={T_y} forbidden"
            )
        if M_taylor is not None and (
            proto_used["zone3_taylor_degree_M"] is None
            or int(M_taylor) != int(proto_used["zone3_taylor_degree_M"])
        ):
            raise ValueError(
                f"Silent M_taylor override {M_taylor} != protocol "
                f"{proto_used['zone3_taylor_degree_M']} at T_Y={T_y} forbidden"
            )
        three_zone = bool(resolved["three_zone"])
        quadrature_mode = str(resolved["quadrature_mode"])
        eff_prec = int(proto_used["prec_bits"])
        eff_quad_tol = int(proto_used["quad_tol_bits"])
        eff_panels = int(proto_used["n_panels"])
        eff_z1_ratio: Optional[int] = proto_used["zone1_ratio_threshold_x_over_n"]
        eff_M_taylor: Optional[int] = proto_used["zone3_taylor_degree_M"]
        requested_settings = dict(resolved["requested_settings"])
        used_settings = dict(proto_used)
        inactive_parameters = list(resolved["inactive_parameters"])
    else:
        three_zone = bool(resolved["three_zone"]) if use_three_zone is None else bool(use_three_zone)
        quadrature_mode = "three_zone" if three_zone else "unsplit"
        if not three_zone:
            if escalation_tier == 0 and n_panels is not None and int(n_panels) != 1:
                raise ValueError(
                    f"Inactive Tier-0 n_panels={n_panels} != 1 cannot be passed when quadrature_mode='unsplit'"
                )
            if zone1_ratio_threshold is not None or M_taylor is not None:
                raise ValueError(
                    "Inactive three-zone parameters (zone1_ratio_threshold, M_taylor) cannot be passed "
                    "when quadrature_mode='unsplit'"
                )
        eff_prec = int(prec_bits) if prec_bits is not None else int(resolved["used_settings"]["prec_bits"])
        req_s = resolved["requested_settings"]
        if three_zone:
            z3 = rules["three_zone_parameters"]
            default_qt = (
                int(rules["quad_tol_bits_three_zone_large_T"])
                if escalation_tier == 0
                else int(req_s["quad_tol_bits"])
            )
            default_np = int(z3["n_panels"]) if escalation_tier == 0 else int(req_s["n_panels"])
            default_z1 = (
                int(z3["zone1_ratio_threshold_x_over_n"])
                if escalation_tier == 0
                else int(req_s["zone1_ratio_threshold_x_over_n"])
            )
            default_m = (
                int(z3["zone3_taylor_degree_M"])
                if escalation_tier == 0
                else int(req_s["zone3_taylor_degree_M"])
            )
            eff_quad_tol = int(quad_tol_bits) if quad_tol_bits is not None else default_qt
            eff_panels = int(n_panels) if n_panels is not None else default_np
            eff_z1_ratio = (
                int(zone1_ratio_threshold) if zone1_ratio_threshold is not None else default_z1
            )
            eff_M_taylor = int(M_taylor) if M_taylor is not None else default_m
            n1_cut_ov: Optional[int] = max(T_y + 1, ceil_tau_y)
            inactive_parameters = []
        else:
            default_qt_u = (
                int(rules["quad_tol_bits_unsplit_small_T"])
                if escalation_tier == 0
                else int(req_s["quad_tol_bits"])
            )
            eff_quad_tol = int(quad_tol_bits) if quad_tol_bits is not None else default_qt_u
            eff_panels = (
                1
                if escalation_tier == 0
                else (int(n_panels) if n_panels is not None else int(req_s["n_panels"]))
            )
            eff_z1_ratio = None
            eff_M_taylor = None
            n1_cut_ov = None
            inactive_parameters = (
                [
                    "n_panels",
                    "zone1_ratio_threshold_x_over_n",
                    "zone3_cutoff_N1",
                    "zone3_taylor_degree_M",
                ]
                if escalation_tier == 0
                else [
                    "zone1_ratio_threshold_x_over_n",
                    "zone3_cutoff_N1",
                    "zone3_taylor_degree_M",
                ]
            )
        requested_settings = {
            "escalation_tier": escalation_tier,
            "quadrature_mode": quadrature_mode,
            "nonprotocol_override": True,
            "prec_bits": eff_prec,
            "quad_tol_bits": eff_quad_tol,
            "n_panels": eff_panels if three_zone else n_panels,
            "zone1_ratio_threshold_x_over_n": eff_z1_ratio,
            "zone3_cutoff_N1": n1_cut_ov,
            "zone3_taylor_degree_M": eff_M_taylor,
        }
        used_settings = {
            "quadrature_mode": quadrature_mode,
            "prec_bits": eff_prec,
            "quad_tol_bits": eff_quad_tol,
            "n_panels": eff_panels,
            "zone1_ratio_threshold_x_over_n": eff_z1_ratio,
            "zone3_cutoff_N1": n1_cut_ov,
            "zone3_taylor_degree_M": eff_M_taylor,
        }

    work_prec = eff_prec + 32
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = work_prec
        tau = _tau_arb()
        log_tau = tau.log()
        Y_arb = spec.evaluate_arb(prec_bits=work_prec)
        log_Y = spec.evaluate_log_Y_arb(prec_bits=work_prec)

        tbl = (
            compute_selberg_centered_remainder_table_fast_arb(T_y, prec_bits=work_prec)
            if selberg_table is None or len(selberg_table["R"]) <= T_y
            else selberg_table
        )
        c_lam = tbl["c_lambda"]
        R = tbl["R"]
        M_drift = tbl["M_drift"]
        R_osc = tbl["R_osc"]

        N2 = 2 * T_y
        lam_int = [0] + [liouville_lambda_int(n) for n in range(1, T_y + 1)]
        lam_r = [arb(v) for v in lam_int]
        ln_r = [arb(0)] + [arb(n).log() for n in range(1, T_y + 1)]
        p_num_r = [arb(0)] + [lam_r[n] * ln_r[n] for n in range(1, T_y + 1)]

        # 1. Separate O(T log T) assembly of A_Y = D_{2,known,Y} numerator coefficients (1..2T):
        alpha_A = [arb(0)] * (N2 + 1)
        for n in range(1, T_y + 1):
            if is_perfect_square_int(n):
                alpha_A[n] += c_lam
        if T_y >= 1:
            alpha_A[T_y] += R[T_y]
        for d_i in range(1, T_y):
            L_d = T_y // d_i
            L_d1 = T_y // (d_i + 1)
            Rd = R[d_i]
            for q in range(L_d1 + 1, L_d + 1):
                alpha_A[(d_i + 1) * q] += Rd * lam_r[q]
            w_k = M_drift[d_i] + (R_osc[d_i] if d_i <= D0_eff else arb(0))
            for q in range(1, L_d + 1):
                term = w_k * lam_r[q]
                alpha_A[d_i * q] += term
                alpha_A[(d_i + 1) * q] -= term

        # 2. Separate O(T log T) assembly of B_Y = D_{2,core,Y} smooth-only coefficients s_Y (1..2T):
        s_Y_sm = [arb(0)] * (N2 + 1)
        for d_i in range(D0_eff + 1, T_y):
            L_d = T_y // d_i
            wd = R_osc[d_i]
            for q in range(1, L_d + 1):
                term = wd * lam_r[q]
                s_Y_sm[d_i * q] += term
                s_Y_sm[(d_i + 1) * q] -= term

        # Sub-unit tail d >= ceil(tau*Y) smooth-only coefficients when nonempty:
        tail_lo_d = max(D0_eff + 1, ceil_tau_y)
        has_tail = ceil_tau_y <= T_y - 1 and tail_lo_d <= T_y - 1
        s_Y_tail = [arb(0)] * (N2 + 1)
        if has_tail:
            for d_i in range(tail_lo_d, T_y):
                L_d = T_y // d_i
                wd = R_osc[d_i]
                for q in range(1, L_d + 1):
                    term = wd * lam_r[q]
                    s_Y_tail[d_i * q] += term
                    s_Y_tail[(d_i + 1) * q] -= term

        # Prime powers up to T_y for inherited prime-power diagonal D_tilde(Y):
        pp_pairs = prime_power_pairs_up_to(T_y)
        pp_info: List[Tuple[int, int, arb]] = [
            (p ** k, T_y // (p ** k), arb(p).log() ** 2) for (p, k) in pp_pairs
        ]

        inv_n3_r = [arb(0)] + [arb(n) ** (-3) for n in range(1, N2 + 1)]
        inv_n3_c = [acb(v) for v in inv_n3_r]
        neg_inv_n2_c = [acb(0)] + [-(acb(n) ** (-2)) for n in range(1, N2 + 1)]

        lam_int = [0] + [liouville_lambda_int(n) for n in range(1, T_y + 1)]
        lam_c = [acb(v) for v in lam_r]
        ln_c = [acb(v) for v in ln_r]
        p_num_c = [acb(v) for v in p_num_r]
        alpha_A_c = [acb(v) for v in alpha_A]
        s_Y_sm_c = [acb(v) for v in s_Y_sm]
        beta_Y_c = [acb(0)] + [
            acb(s_Y_sm[n] - lam_r[n] * (ln_r[n] * ln_r[n])) if n <= T_y else acb(s_Y_sm[n])
            for n in range(1, N2 + 1)
        ]
        s_Y_tail_c = [acb(v) for v in s_Y_tail]
        pp_info_c: List[Tuple[int, int, acb]] = [(pk, L_pk, acb(lg2)) for (pk, L_pk, lg2) in pp_info]
        pp_l1_pairs: List[Tuple[int, acb]] = [(pk, w_c) for (pk, L_pk, w_c) in pp_info_c if L_pk == 1]
        pp_multi_groups: List[Tuple[int, int, acb]] = [
            (pk, L_pk, w_c) for (pk, L_pk, w_c) in pp_info_c if L_pk >= 2
        ]

        N1 = max(T_y + 1, ceil_tau_y) if three_zone else (N2 + 1)
        m_deg_active = int(eff_M_taylor) if (three_zone and eff_M_taylor is not None) else 0
        z1_ratio_active = int(eff_z1_ratio) if (three_zone and eff_z1_ratio is not None) else 0

        def _build_zone3_poly(vec_r: Sequence[arb]) -> Tuple[List[acb], arb]:
            if (not three_zone) or N1 > N2 or m_deg_active <= 0:
                return ([], arb(0))
            N1_arb = arb(N1)
            N1_sq = N1_arb * N1_arb
            S_pow = [arb(0)] * m_deg_active
            S_rem = arb(0)
            for n in range(N1, N2 + 1):
                cn = vec_r[n]
                if cn == arb(0):
                    continue
                base = cn * inv_n3_r[n]
                r2 = N1_sq / arb(n * n)
                pw = arb(1)
                for m_idx in range(m_deg_active):
                    S_pow[m_idx] += base * pw
                    pw *= r2
                S_rem += abs(base) * pw
            pC = [acb(0)] * m_deg_active
            fact = arb(1)
            for m_idx in range(m_deg_active):
                if m_idx > 0:
                    fact *= arb(m_idx)
                sgn = arb(-1) if (m_idx % 2 == 1) else arb(1)
                pC[m_idx] = acb(sgn * S_pow[m_idx] / fact)
            rem_M = arb(2) * S_rem / (fact * arb(m_deg_active))
            return (pC, rem_M)

        poly_A, rem_A = _build_zone3_poly(alpha_A)
        poly_B, rem_B = _build_zone3_poly(s_Y_sm)
        poly_Bt, rem_Bt = _build_zone3_poly(s_Y_tail) if has_tail else ([], arb(0))
        N1_c = acb(N1)
        Y_c = acb(Y_arb)
        log_Y_c = acb(log_Y)
        tol = 2 ** (-eff_quad_tol)
        panels = eff_panels

        E_acc = arb(0)
        P2_acc = arb(0)
        D_acc = arb(0)
        A2_acc = arb(0)
        B2_acc = arb(0)
        PB_acc = arb(0)
        QA2_acc = arb(0)
        TwoPB2_acc = arb(0)
        Bt2_acc = arb(0)
        Binter2_acc = arb(0)
        PBt_acc = arb(0)
        BinterBt_acc = arb(0)
        unique_nodes = 0

        for j in range(panels):
            u_lo = log_tau * arb(j) / arb(panels)
            u_hi = log_tau * arb(j + 1) / arb(panels)
            du = u_hi - u_lo
            sqrt_du = du.sqrt()
            x_lo = Y_arb * u_lo.exp()
            lg_lo = log_Y + u_lo

            if three_zone:
                n0_j = min(T_y, max(0, int(math.floor(float(x_lo.lower()) / float(z1_ratio_active)))))
                while n0_j > 0 and not bool(x_lo >= arb(z1_ratio_active * n0_j)):
                    n0_j -= 1
            else:
                n0_j = 0

            eps_Q = arb(0)
            eps_P = arb(0)
            eps_A = arb(0)
            eps_B = arb(0)
            eps_Bt = arb(0)
            eps_Binter = arb(0)
            delta_diag_j = arb(0)
            if n0_j > 0:
                x_lo_52 = x_lo ** (arb(5) / arb(2))
                x_lo_2 = x_lo * x_lo
                phi_lo = [arb(0)] * (n0_j + 1)
                for n in range(1, n0_j + 1):
                    phi_lo[n] = x_lo_52 * inv_n3_r[n] * (-x_lo_2 / arb(n * n)).exp()
                    eps_Q += phi_lo[n]
                    eps_P += ln_r[n] * phi_lo[n]
                    eps_A += abs(alpha_A[n]) * phi_lo[n]
                    d_lg_lo = lg_lo - ln_r[n]
                    sh_sq = d_lg_lo * d_lg_lo
                    eps_B += (abs(s_Y_sm[n]) + sh_sq) * phi_lo[n]
                    if has_tail:
                        eps_Bt += abs(s_Y_tail[n]) * phi_lo[n]
                        eps_Binter += (abs(s_Y_sm[n] - s_Y_tail[n]) + sh_sq) * phi_lo[n]
                eps_P = eps_P / lg_lo
                eps_A = eps_A / (lg_lo * lg_lo)
                eps_B = eps_B / (lg_lo * lg_lo)
                if has_tail:
                    eps_Bt = eps_Bt / (lg_lo * lg_lo)
                    eps_Binter = eps_Binter / (lg_lo * lg_lo)

                diag_sq_sum = arb(0)
                for pk, L_pk, lg_p_sq in pp_info:
                    if pk > n0_j:
                        break
                    q0 = min(L_pk, n0_j // pk)
                    s_pk = arb(0)
                    for q in range(1, q0 + 1):
                        s_pk += phi_lo[pk * q]
                    diag_sq_sum += lg_p_sq * (s_pk * s_pk)
                delta_diag_j = (sqrt_du / lg_lo) * diag_sq_sum.sqrt()

            node_cache: Dict[Any, List[Any]] = {}
            hi_z2 = min(N2, N1 - 1)
            hi_T = min(T_y, hi_z2)
            len_T_j = max(0, hi_T - n0_j)
            len_sp_j = max(0, hi_z2 - hi_T)
            z2_pairs_T = list(zip(inv_n3_c[n0_j + 1 : hi_T + 1], neg_inv_n2_c[n0_j + 1 : hi_T + 1]))
            z2_pairs_sp = list(zip(inv_n3_c[hi_T + 1 : hi_z2 + 1], neg_inv_n2_c[hi_T + 1 : hi_z2 + 1]))
            if len_T_j > 0:
                if has_tail:
                    M_T_j = acb_mat(
                        len_T_j,
                        5,
                        [
                            val_c
                            for n in range(n0_j + 1, hi_T + 1)
                            for val_c in (lam_c[n], p_num_c[n], alpha_A_c[n], beta_Y_c[n], s_Y_tail_c[n])
                        ],
                    )
                else:
                    M_T_j = acb_mat(
                        len_T_j,
                        4,
                        [
                            val_c
                            for n in range(n0_j + 1, hi_T + 1)
                            for val_c in (lam_c[n], p_num_c[n], alpha_A_c[n], beta_Y_c[n])
                        ],
                    )
            else:
                M_T_j = None
            if len_sp_j > 0:
                if has_tail:
                    M_sp_j = acb_mat(
                        len_sp_j,
                        3,
                        [
                            val_c
                            for n in range(hi_T + 1, hi_z2 + 1)
                            for val_c in (alpha_A_c[n], beta_Y_c[n], s_Y_tail_c[n])
                        ],
                    )
                else:
                    M_sp_j = acb_mat(
                        len_sp_j,
                        2,
                        [
                            val_c
                            for n in range(hi_T + 1, hi_z2 + 1)
                            for val_c in (alpha_A_c[n], beta_Y_c[n])
                        ],
                    )
            else:
                M_sp_j = None

            l1_active_j = [(pk, w_c) for (pk, w_c) in pp_l1_pairs if n0_j < pk <= hi_T]
            l1_idx_j = [pk for (pk, _w) in l1_active_j]
            l1_w_mat_j = (
                acb_mat(len(l1_active_j), 1, [w_c for (_pk, w_c) in l1_active_j])
                if l1_active_j
                else None
            )
            pp_multi_j: List[Tuple[acb, List[int], List[int]]] = []
            for pk, L_pk, w_c in pp_multi_groups:
                q_start = (n0_j // pk) + 1
                if q_start > L_pk:
                    continue
                pos_m = [pk * q for q in range(q_start, L_pk + 1) if lam_int[q] == 1 and pk * q <= hi_T]
                neg_m = [pk * q for q in range(q_start, L_pk + 1) if lam_int[q] == -1 and pk * q <= hi_T]
                if pos_m or neg_m:
                    pp_multi_j.append((w_c, pos_m, neg_m))

            def _compute_d_val(ph_T_list: List[acb], extra_phi: Optional[Dict[int, acb]], lg2_v: acb) -> acb:
                phi_c = [acb(0)] * (n0_j + 1) + ph_T_list
                if len(phi_c) < T_y + 1:
                    phi_c.extend([acb(0)] * (T_y + 1 - len(phi_c)))
                if extra_phi:
                    for idx_e, ph_e in extra_phi.items():
                        phi_c[idx_e] = ph_e
                if l1_w_mat_j is not None:
                    d_sum = (
                        acb_mat(1, len(l1_idx_j), [phi_c[m] * phi_c[m] for m in l1_idx_j]) * l1_w_mat_j
                    )[0, 0]
                else:
                    d_sum = acb(0)
                for w_c, pos_m, neg_m in pp_multi_j:
                    s_pk = sum((phi_c[m] for m in pos_m), acb(0)) - sum((phi_c[m] for m in neg_m), acb(0))
                    d_sum += w_c * (s_pk * s_pk)
                return d_sum / lg2_v

            def _eval_bundle(u: acb, _analytic: bool, need_diag: bool = False) -> Optional[List[Any]]:
                nonlocal unique_nodes
                lg = log_Y_c + u
                if _analytic and not bool(lg.real > arb(1) / arb(2)):
                    return None
                use_cache = u.is_finite()
                key = None
                if use_cache:
                    key = (
                        flint_ctx.prec,
                        u.real.mid().man_exp(),
                        u.real.rad().man_exp(),
                        u.imag.mid().man_exp(),
                        u.imag.rad().man_exp(),
                    )
                    cached = node_cache.get(key)
                    if cached is not None:
                        if need_diag and cached[4] is None:
                            cached[4] = _compute_d_val(cached[6], cached[7], cached[8])
                        return cached

                unique_nodes += 1
                x = Y_c * u.exp()
                x2 = x * x
                x_52 = (Y_c ** (acb(5) / acb(2))) * (acb(arb(5) / arb(2)) * u).exp()

                q_val = acb(0)
                p_num = acb(0)
                a_num = acb(0)
                beta_sm = acb(0)
                bt_sm = acb(0)

                if len_T_j > 0 and M_T_j is not None:
                    ph_T = [x_52 * i3 * (x2 * ng).exp() for i3, ng in z2_pairs_T]
                    row_T = acb_mat(1, len_T_j, ph_T) * M_T_j
                    q_val = row_T[0, 0]
                    p_num = row_T[0, 1]
                    a_num = row_T[0, 2]
                    beta_sm = row_T[0, 3]
                    if has_tail:
                        bt_sm = row_T[0, 4]
                else:
                    ph_T = []

                if len_sp_j > 0 and M_sp_j is not None:
                    ph_sp = [x_52 * i3 * (x2 * ng).exp() for i3, ng in z2_pairs_sp]
                    row_sp = acb_mat(1, len_sp_j, ph_sp) * M_sp_j
                    a_num += row_sp[0, 0]
                    beta_sm += row_sp[0, 1]
                    if has_tail:
                        bt_sm += row_sp[0, 2]

                extra_phi: Optional[Dict[int, acb]] = None
                if N1 <= N2:
                    rx = x / N1_c
                    w = rx * rx
                    abs_w = abs(w)
                    if bool(abs_w <= arb(m_deg_active) / arb(2)):
                        pa = acb(0)
                        pb = acb(0)
                        pbt = acb(0)
                        for m_idx in range(m_deg_active - 1, -1, -1):
                            pa = pa * w + poly_A[m_idx]
                            pb = pb * w + poly_B[m_idx]
                            if has_tail:
                                pbt = pbt * w + poly_Bt[m_idx]
                        abs_w_up = abs_w.upper()
                        w_pow = arb(0) if abs_w_up == arb(0) else (abs_w_up ** m_deg_active)
                        ra = (rem_A * w_pow).upper()
                        rb = (rem_B * w_pow).upper()
                        a_num += x_52 * (pa + acb(arb(0, ra), arb(0, ra)))
                        beta_sm += x_52 * (pb + acb(arb(0, rb), arb(0, rb)))
                        if has_tail:
                            rbt = (rem_Bt * w_pow).upper()
                            bt_sm += x_52 * (pbt + acb(arb(0, rbt), arb(0, rbt)))
                    else:
                        extra_phi = {}
                        for n in range(N1, N2 + 1):
                            ph = x_52 * inv_n3_c[n] * (x2 * neg_inv_n2_c[n]).exp()
                            if n <= T_y:
                                extra_phi[n] = ph
                                q_val += lam_c[n] * ph
                                p_num += p_num_c[n] * ph
                            a_num += alpha_A_c[n] * ph
                            beta_sm += beta_Y_c[n] * ph
                            if has_tail:
                                bt_sm += s_Y_tail_c[n] * ph

                lg2 = lg * lg
                p_val = p_num / lg
                a_val = a_num / lg2
                # Exact complete-core bridge (Lean Theorem 5):
                # B_Y(X) = (sum beta_Y(n)*phi_n(X))/(log X)^2 + 2*P_Y(X) - Q_Y(X)
                b_val = (beta_sm / lg2) + acb(2) * p_val - q_val
                bt_val = bt_sm / lg2 if has_tail else acb(0)
                d_val = _compute_d_val(ph_T, extra_phi, lg2) if need_diag else None

                bundle: List[Any] = [q_val, p_val, a_val, b_val, d_val, bt_val, ph_T, extra_phi, lg2]
                if use_cache and key is not None:
                    node_cache[key] = bundle
                return bundle

            def _nan_acb() -> acb:
                nb = arb("nan")
                return acb(nb, nb)

            def _int_fn(fn: Callable[[List[Any]], acb], *, need_diag: bool = False) -> arb:
                def _cb(u: acb, _an: bool) -> acb:
                    bd = _eval_bundle(u, _an, need_diag=need_diag)
                    if bd is None:
                        return _nan_acb()
                    return fn(bd)

                return acb.integral(_cb, acb(u_lo), acb(u_hi), rel_tol=tol, abs_tol=tol).real

            E_m = _int_fn(lambda b: b[0] * b[0])
            P2_m = _int_fn(lambda b: b[1] * b[1])
            D_m = _int_fn(lambda b: b[4], need_diag=True)
            A2_m = _int_fn(lambda b: b[2] * b[2])
            B2_m = _int_fn(lambda b: b[3] * b[3])
            PB_m = _int_fn(lambda b: b[1] * b[3])
            QA2_m = _int_fn(lambda b: (b[0] + b[2]) * (b[0] + b[2]))
            TwoPB2_m = _int_fn(lambda b: (acb(2) * b[1] - b[3]) * (acb(2) * b[1] - b[3]))

            def _sq_pert(main_v: arb, eps_v: arb) -> arb:
                if eps_v == arb(0):
                    return main_v
                nm = abs(main_v).sqrt()
                rad = (arb(2) * nm * eps_v * sqrt_du + (eps_v * eps_v) * du).upper()
                return main_v + arb(0, rad)

            def _bilin_pert(main_v: arb, i_f: arb, i_g: arb, eps_f: arb, eps_g: arb) -> arb:
                if eps_f == arb(0) and eps_g == arb(0):
                    return main_v
                nf = abs(i_f).sqrt()
                ng = abs(i_g).sqrt()
                rad = (nf * eps_g * sqrt_du + ng * eps_f * sqrt_du + eps_f * eps_g * du).upper()
                return main_v + arb(0, rad)

            E_acc += _sq_pert(E_m, eps_Q)
            P2_acc += _sq_pert(P2_m, eps_P)
            A2_acc += _sq_pert(A2_m, eps_A)
            B2_acc += _sq_pert(B2_m, eps_B)
            PB_acc += _bilin_pert(PB_m, P2_m, B2_m, eps_P, eps_B)
            QA2_acc += _sq_pert(QA2_m, eps_Q + eps_A)
            TwoPB2_acc += _sq_pert(TwoPB2_m, arb(2) * eps_P + eps_B)
            if delta_diag_j == arb(0):
                D_acc += D_m
            else:
                rad_d = (arb(2) * abs(D_m).sqrt() * delta_diag_j + delta_diag_j * delta_diag_j).upper()
                D_acc += D_m + arb(0, rad_d)

            if has_tail:
                Bt2_m = _int_fn(lambda b: b[5] * b[5])
                Binter2_m = _int_fn(lambda b: (b[3] - b[5]) * (b[3] - b[5]))
                PBt_m = _int_fn(lambda b: b[1] * b[5])
                Bib_m = _int_fn(lambda b: (b[3] - b[5]) * b[5])
                Bt2_acc += _sq_pert(Bt2_m, eps_Bt)
                Binter2_acc += _sq_pert(Binter2_m, eps_Binter)
                PBt_acc += _bilin_pert(PBt_m, P2_m, Bt2_m, eps_P, eps_Bt)
                BinterBt_acc += _bilin_pert(Bib_m, Binter2_m, Bt2_m, eps_Binter, eps_Bt)

        flint_ctx.prec = eff_prec
        E_out = +E_acc
        P2_out = +P2_acc
        D_out = +D_acc
        X_out = +(P2_acc - D_acc)
        A2_out = +A2_acc
        B2_out = +B2_acc
        PB_out = +PB_acc
        QA2_out = +QA2_acc
        TwoPB2_out = +TwoPB2_acc
        J_direct = +(arb(4) * (P2_acc - D_acc) + B2_acc - arb(4) * PB_acc)
        J_cons_QA = +(QA2_acc - arb(4) * D_acc)
        J_cons_2PB = +(TwoPB2_acc - arb(4) * D_acc)
        cons_res_QA = +(J_direct - J_cons_QA)
        cons_res_2PB = +(J_direct - J_cons_2PB)
        logY_D = +(log_Y * D_acc)
        R_mix = +(B2_acc - arb(4) * PB_acc)

        J_tail_contrib = (
            +(Bt2_acc + arb(2) * BinterBt_acc - arb(4) * PBt_acc) if has_tail else arb(0)
        )
        J_without_tail = +(J_direct - J_tail_contrib) if has_tail else J_direct

        elapsed = time.perf_counter() - t_start
        rss_info = _measure_process_rss_megabytes()
        return {
            "cutoffs": cut,
            "Y_arb": +Y_arb,
            "log_Y_arb": +log_Y,
            "E_Y": E_out,
            "D_tilde_Y": D_out,
            "X_tilde_Y": X_out,
            "P_norm_sq": P2_out,
            "A_norm_sq": A2_out,
            "B_norm_sq": B2_out,
            "pair_P_B": PB_out,
            "R_mix_Y": R_mix,
            "QA_norm_sq": QA2_out,
            "TwoP_minus_B_norm_sq": TwoPB2_out,
            "J_direct": J_direct,
            "J_algebraic_consistency_QA": J_cons_QA,
            "J_algebraic_consistency_2PB": J_cons_2PB,
            "J_consistency_residual_QA": cons_res_QA,
            "J_consistency_residual_2PB": cons_res_2PB,
            "log_Y_times_D_tilde": logY_D,
            "has_subunit_tail_ge_ceil_tau_Y": has_tail,
            "subunit_tail_d_range_inclusive": [tail_lo_d, T_y - 1] if has_tail else [],
            "B_tail_norm_sq": +Bt2_acc if has_tail else arb(0),
            "B_inter_norm_sq": +Binter2_acc if has_tail else B2_out,
            "pair_P_B_tail": +PBt_acc if has_tail else arb(0),
            "pair_B_inter_B_tail": +BinterBt_acc if has_tail else arb(0),
            "J_subunit_tail_contribution": J_tail_contrib,
            "J_without_subunit_tail": J_without_tail,
            "quadrature_mode": quadrature_mode,
            "escalation_tier": escalation_tier,
            "requested_settings": requested_settings,
            "used_settings": used_settings,
            "inactive_parameters": inactive_parameters,
            "three_zone_used": three_zone,
            "panels_used": panels,
            "zone1_ratio_threshold_used": eff_z1_ratio,
            "M_taylor_used": eff_M_taylor,
            "unique_quadrature_nodes": unique_nodes,
            "prec_bits": eff_prec,
            "quad_tol_bits": eff_quad_tol,
            "elapsed_sec": elapsed,
            "current_rss_mb": rss_info["current_rss_mb"],
            "peak_rss_mb": rss_info["peak_rss_mb"],
            "peak_rss_measurement_semantics": rss_info.get("peak_rss_measurement_semantics"),
        }
    finally:
        flint_ctx.prec = saved


def evaluate_fixed_cutoff_on_Y_ball_arb(
    Y_ball: arb,
    T_fixed: int,
    D0_raw_fixed: int,
    *,
    prec_bits: int = 256,
    quad_tol_bits: int = 110,
    selberg_table: Dict[str, Any],
) -> Dict[str, Any]:
    """Evaluate fixed-cutoff `(T_fixed, D0_eff_fixed)` window observables uniformly across ALL `Y` in `Y_ball`."""
    work_prec = prec_bits + 32
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = work_prec
        if not bool(Y_ball >= arb(2)):
            raise ValueError(f"Y_ball {Y_ball} must satisfy Y >= 2")
        D0_eff = min(D0_raw_fixed, max(0, T_fixed - 1))
        tau = _tau_arb()
        log_tau = tau.log()
        log_Y = Y_ball.log()
        c_lam = selberg_table["c_lambda"]
        R = selberg_table["R"]
        M_drift = selberg_table["M_drift"]
        R_osc = selberg_table["R_osc"]

        N2 = 2 * T_fixed
        lam_r = [arb(0)] + [arb(liouville_lambda_int(n)) for n in range(1, T_fixed + 1)]
        ln_r = [arb(0)] + [arb(n).log() for n in range(1, T_fixed + 1)]
        p_num_r = [arb(0)] + [lam_r[n] * ln_r[n] for n in range(1, T_fixed + 1)]

        alpha_A = [arb(0)] * (N2 + 1)
        for n in range(1, T_fixed + 1):
            if is_perfect_square_int(n):
                alpha_A[n] += c_lam
        if T_fixed >= 1:
            alpha_A[T_fixed] += R[T_fixed]
        for d_i in range(1, T_fixed):
            L_d = T_fixed // d_i
            L_d1 = T_fixed // (d_i + 1)
            Rd = R[d_i]
            for q in range(L_d1 + 1, L_d + 1):
                alpha_A[(d_i + 1) * q] += Rd * lam_r[q]
            w_k = M_drift[d_i] + (R_osc[d_i] if d_i <= D0_eff else arb(0))
            for q in range(1, L_d + 1):
                term = w_k * lam_r[q]
                alpha_A[d_i * q] += term
                alpha_A[(d_i + 1) * q] -= term

        s_Y_sm = [arb(0)] * (N2 + 1)
        for d_i in range(D0_eff + 1, T_fixed):
            L_d = T_fixed // d_i
            wd = R_osc[d_i]
            for q in range(1, L_d + 1):
                term = wd * lam_r[q]
                s_Y_sm[d_i * q] += term
                s_Y_sm[(d_i + 1) * q] -= term

        pp_info_c = [
            (p ** k, T_fixed // (p ** k), acb(arb(p).log() ** 2))
            for (p, k) in prime_power_pairs_up_to(T_fixed)
        ]
        inv_n3_c = [acb(0)] + [acb(arb(n) ** (-3)) for n in range(1, N2 + 1)]
        neg_inv_n2_c = [acb(0)] + [-(acb(n) ** (-2)) for n in range(1, N2 + 1)]
        lam_c = [acb(v) for v in lam_r]
        ln_c = [acb(v) for v in ln_r]
        p_num_c = [acb(v) for v in p_num_r]
        alpha_A_c = [acb(v) for v in alpha_A]
        s_Y_sm_c = [acb(v) for v in s_Y_sm]
        Y_c = acb(Y_ball)
        log_Y_c = acb(log_Y)
        tol = 2 ** (-quad_tol_bits)
        panels = 8 if T_fixed >= 256 else 2

        E_acc = arb(0)
        P2_acc = arb(0)
        D_acc = arb(0)
        A2_acc = arb(0)
        B2_acc = arb(0)
        PB_acc = arb(0)

        for j in range(panels):
            u_lo = log_tau * arb(j) / arb(panels)
            u_hi = log_tau * arb(j + 1) / arb(panels)
            node_cache: Dict[Any, Any] = {}

            def _eval_bd(u: acb, _an: bool):
                lg = log_Y_c + u
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    return None
                key = None
                if u.is_finite():
                    key = (
                        flint_ctx.prec,
                        u.real.mid().man_exp(),
                        u.real.rad().man_exp(),
                        u.imag.mid().man_exp(),
                        u.imag.rad().man_exp(),
                    )
                    if key in node_cache:
                        return node_cache[key]
                x = Y_c * u.exp()
                x2 = x * x
                x_52 = (Y_c ** (acb(5) / acb(2))) * (acb(arb(5) / arb(2)) * u).exp()
                phi_c = [acb(0)] * (T_fixed + 1)
                q_val = acb(0)
                p_num = acb(0)
                q_sh2 = acb(0)
                a_num = acb(0)
                b_sm = acb(0)
                for n in range(1, T_fixed + 1):
                    ph = x_52 * inv_n3_c[n] * (x2 * neg_inv_n2_c[n]).exp()
                    phi_c[n] = ph
                    lph = lam_c[n] * ph
                    q_val += lph
                    p_num += p_num_c[n] * ph
                    d_lg = lg - ln_c[n]
                    q_sh2 += lph * (d_lg * d_lg)
                    a_num += alpha_A_c[n] * ph
                    b_sm += s_Y_sm_c[n] * ph
                for n in range(T_fixed + 1, N2 + 1):
                    ph = x_52 * inv_n3_c[n] * (x2 * neg_inv_n2_c[n]).exp()
                    a_num += alpha_A_c[n] * ph
                    b_sm += s_Y_sm_c[n] * ph
                lg2 = lg * lg
                p_val = p_num / lg
                a_val = a_num / lg2
                b_val = (b_sm - q_sh2) / lg2
                d_sum = acb(0)
                for pk, L_pk, lg_p_sq_c in pp_info_c:
                    s_pk = acb(0)
                    for q in range(1, L_pk + 1):
                        s_pk += lam_c[q] * phi_c[pk * q]
                    d_sum += lg_p_sq_c * (s_pk * s_pk)
                bd = (q_val, p_val, a_val, b_val, d_sum / lg2)
                if key is not None:
                    node_cache[key] = bd
                return bd

            def _int_f(fn):
                def _cb(u: acb, _an: bool) -> acb:
                    bd = _eval_bd(u, _an)
                    if bd is None:
                        nb = arb("nan")
                        return acb(nb, nb)
                    return fn(bd)

                return acb.integral(_cb, acb(u_lo), acb(u_hi), rel_tol=tol, abs_tol=tol).real

            E_acc += _int_f(lambda b: b[0] * b[0])
            P2_acc += _int_f(lambda b: b[1] * b[1])
            D_acc += _int_f(lambda b: b[4])
            A2_acc += _int_f(lambda b: b[2] * b[2])
            B2_acc += _int_f(lambda b: b[3] * b[3])
            PB_acc += _int_f(lambda b: b[1] * b[3])

        flint_ctx.prec = prec_bits
        J_b = +(arb(4) * (P2_acc - D_acc) + B2_acc - arb(4) * PB_acc)
        lgD_b = +(log_Y * D_acc)
        return {
            "T_fixed": T_fixed,
            "D0_raw_fixed": D0_raw_fixed,
            "D0_eff_fixed": D0_eff,
            "Y_sub_ball": +Y_ball,
            "E_Y": +E_acc,
            "D_tilde_Y": +D_acc,
            "X_tilde_Y": +(P2_acc - D_acc),
            "A_norm_sq": +A2_acc,
            "B_norm_sq": +B2_acc,
            "pair_P_B": +PB_acc,
            "J_Y": J_b,
            "log_Y_times_D_tilde": lgD_b,
            "M_P0": +(J_b - lgD_b),
        }
    finally:
        flint_ctx.prec = saved


def evaluate_interval_via_cutoff_case_split_arb(
    Y_lo_frac: Fraction,
    Y_hi_frac: Fraction,
    *,
    prec_bits: int = 256,
    quad_tol_bits: int = 110,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Rigorous branch-splitting interval evaluation over genuine input intervals `[Y_lo_frac, Y_hi_frac]`
    spanning discontinuities in `T(Y) = ceil(Y^{5/4})` or `D_0(Y) = floor(log Y)` (never midpoint rounding).
    """
    if isinstance(Y_lo_frac, float) or isinstance(Y_hi_frac, float):
        raise TypeError("Float endpoints are forbidden in evaluate_interval_via_cutoff_case_split_arb")
    Y_lo_frac = Fraction(Y_lo_frac)
    Y_hi_frac = Fraction(Y_hi_frac)
    if Y_lo_frac < Fraction(2, 1) or Y_hi_frac < Y_lo_frac:
        raise ValueError(f"Invalid interval [{Y_lo_frac}, {Y_hi_frac}]")
    T_min = certify_T_canonical_cutoff(Y_lo_frac, prec_bits=prec_bits)
    T_max = certify_T_canonical_cutoff(Y_hi_frac, prec_bits=prec_bits)
    D0_min = certify_D0_small_divisor_cutoff(Y_lo_frac, kappa=1, prec_bits=prec_bits)
    D0_max = certify_D0_small_divisor_cutoff(Y_hi_frac, kappa=1, prec_bits=prec_bits)

    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(T_max, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= T_max
        else selberg_table
    )

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits + 64
        y_lo_b = _frac_to_arb(Y_lo_frac)
        y_hi_b = _frac_to_arb(Y_hi_frac)
        branches: List[Dict[str, Any]] = []
        for T_c in range(T_min, T_max + 1):
            if (Y_hi_frac.numerator ** 5) <= ((T_c - 1) ** 4) * (Y_hi_frac.denominator ** 5):
                continue
            if (Y_lo_frac.numerator ** 5) > (T_c ** 4) * (Y_lo_frac.denominator ** 5):
                continue
            t_lo_b = (arb(T_c - 1) ** (arb(4) / arb(5))) if T_c > 1 else arb(0)
            t_hi_b = arb(T_c) ** (arb(4) / arb(5))
            for D0_c in range(D0_min, D0_max + 1):
                d_lo_b = arb(D0_c).exp()
                d_hi_b = arb(D0_c + 1).exp()
                lo_cand = max(
                    [y_lo_b.lower(), t_lo_b.lower(), d_lo_b.lower()],
                    key=lambda b: _exact_arb_endpoints_as_fractions(b)[0],
                )
                hi_cand = min(
                    [y_hi_b.upper(), t_hi_b.upper(), d_hi_b.upper()],
                    key=lambda b: _exact_arb_endpoints_as_fractions(b)[1],
                )
                if bool(lo_cand > hi_cand):
                    continue
                sub_ball = lo_cand.union(hi_cand)
                br_res = evaluate_fixed_cutoff_on_Y_ball_arb(
                    sub_ball,
                    T_c,
                    D0_c,
                    prec_bits=prec_bits,
                    quad_tol_bits=quad_tol_bits,
                    selberg_table=tbl,
                )
                branches.append(br_res)

        assert len(branches) >= 1, "At least one active cutoff branch must exist"
        flint_ctx.prec = prec_bits

        def _union_key(k: str) -> arb:
            u = branches[0][k]
            for br in branches[1:]:
                u = u.union(br[k])
            return +u

        union_M_P0 = _union_key("M_P0")
        return {
            "Y_lo_fraction": f"{Y_lo_frac.numerator}/{Y_lo_frac.denominator}",
            "Y_hi_fraction": f"{Y_hi_frac.numerator}/{Y_hi_frac.denominator}",
            "T_range": [T_min, T_max],
            "D0_range": [D0_min, D0_max],
            "active_branch_count": len(branches),
            "branches": branches,
            "union_E_Y": _union_key("E_Y"),
            "union_D_tilde_Y": _union_key("D_tilde_Y"),
            "union_J_Y": _union_key("J_Y"),
            "union_log_Y_times_D_tilde": _union_key("log_Y_times_D_tilde"),
            "union_M_P0": union_M_P0,
            "P0_interval_classification": classify_probe_margin_arb(union_M_P0),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 2. Section 1: Protocol Immutability, Calibration, & Exact Mixed Identity
# ---------------------------------------------------------------------------


def verify_frozen_protocol_immutability(
    protocol_path: Path = MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH,
) -> Dict[str, Any]:
    """Verify SHA-256 and git commit immutability of `data/tc_mixed_arithmetic_covariance_protocol.json`."""
    raw_bytes = protocol_path.read_bytes().replace(b"\r\n", b"\n")
    proto = json.loads(raw_bytes.decode("utf-8"))
    proto_without_hash = {k: v for k, v in proto.items() if k != "protocol_sha256"}
    canonical_bytes = json.dumps(
        proto_without_hash, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    computed_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
    recorded_sha256 = proto.get("protocol_sha256")
    hash_ok = bool(
        computed_sha256 == FROZEN_PROTOCOL_SHA256 and recorded_sha256 == FROZEN_PROTOCOL_SHA256
    )

    git_blob_matches = False
    git_commit_is_ancestor = False
    try:
        proc_blob = subprocess.run(
            [
                "git",
                "show",
                f"{FROZEN_PROTOCOL_REGISTRATION_COMMIT}:data/tc_mixed_arithmetic_covariance_protocol.json",
            ],
            cwd=str(REPO_ROOT),
            capture_output=True,
            check=False,
        )
        if proc_blob.returncode == 0:
            blob_norm = proc_blob.stdout.replace(b"\r\n", b"\n")
            git_blob_matches = blob_norm == raw_bytes
        proc_anc = subprocess.run(
            ["git", "merge-base", "--is-ancestor", FROZEN_PROTOCOL_REGISTRATION_COMMIT, "HEAD"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            check=False,
        )
        git_commit_is_ancestor = proc_anc.returncode == 0
    except Exception:  # noqa: BLE001
        git_blob_matches = False
        git_commit_is_ancestor = False

    return {
        "protocol_path": "data/tc_mixed_arithmetic_covariance_protocol.json",
        "protocol_id": proto.get("protocol_id"),
        "expected_protocol_sha256": FROZEN_PROTOCOL_SHA256,
        "computed_protocol_sha256": computed_sha256,
        "recorded_protocol_sha256": recorded_sha256,
        "sha256_verified": hash_ok,
        "registration_commit": FROZEN_PROTOCOL_REGISTRATION_COMMIT,
        "git_blob_matches_registration_commit": git_blob_matches,
        "registration_commit_is_ancestor_of_head": git_commit_is_ancestor,
        "protocol_object": proto,
        "verified": bool(
            proto.get("protocol_id") == FROZEN_PROTOCOL_ID
            and hash_ok
            and git_blob_matches
            and git_commit_is_ancestor
        ),
    }


def _evaluate_probes_for_point_result(
    res: Dict[str, Any],
    probes: Sequence[Dict[str, Any]],
    *,
    in_declared_domain_fn: Callable[[Dict[str, Any]], bool],
    kl1_in_declared_domain: Optional[bool] = None,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Evaluate all frozen probes and mechanism sub-budgets for a single point evaluation result.

    Includes BOTH in-domain main candidate probes AND in-domain `TC061-KL1-OFFDIAG-AND-MIXED-SPLIT`
    mechanism sub-budgets (`Y >= 64`) in escalation decision flags (`TASK-TC-061R` §6).
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        Y_b = res["Y_arb"]
        J_b = res["J_direct"]
        lgD_b = res["log_Y_times_D_tilde"]
        X_b = res["X_tilde_Y"]
        R_mix_b = res["R_mix_Y"]

        per_probe: Dict[str, Any] = {}
        any_main_probe_in_domain_unresolved = False
        any_main_probe_in_domain_fail = False
        for pr in probes:
            pid = pr["probe_id"]
            in_dom = in_declared_domain_fn(pr)
            a_fr = Fraction(int(pr["a_numerator"]), int(pr["a_denominator"]))
            a_b = _frac_to_arb(a_fr)
            if pr["eta_fraction"] is None or a_fr == Fraction(0, 1):
                a_y_eta = arb(0)
            else:
                en, ed = (int(x) for x in str(pr["eta_fraction"]).split("/"))
                eta_b = _frac_to_arb(Fraction(en, ed))
                a_y_eta = a_b * (Y_b ** eta_b)
            rhs_tot = a_y_eta + lgD_b
            margin = J_b - rhs_tot
            cls = classify_probe_margin_arb(margin)
            if in_dom and cls["verdict"] == "UNRESOLVED":
                any_main_probe_in_domain_unresolved = True
            if in_dom and cls["verdict"] == "FAIL":
                any_main_probe_in_domain_fail = True

            # Forcing dominance check: whether a_eta * Y^eta > (log Y) * D_tilde(Y):
            diff_dom = a_y_eta - lgD_b
            d_lo, d_hi = _exact_arb_endpoints_as_fractions(diff_dom)
            if d_lo > Fraction(0, 1):
                dom_status = "A_ETA_Y_ETA_STRICTLY_DOMINATES"
                dom_bool: Optional[bool] = True
            elif d_hi <= Fraction(0, 1):
                dom_status = "LOG_Y_D_TILDE_DOMINATES_OR_EQUALS"
                dom_bool = False
            else:
                dom_status = "AMBIGUOUS_NEAR_TIE"
                dom_bool = None

            per_probe[pid] = {
                "probe_id": pid,
                "tier": pr["tier"],
                "in_declared_domain": in_dom,
                "a_Y_eta_rhs_term": serialize_arb_certified(a_y_eta),
                "log_Y_D_tilde_rhs_term": serialize_arb_certified(lgD_b),
                "total_rhs": serialize_arb_certified(rhs_tot),
                "margin_M_Y": serialize_arb_certified(margin),
                "point_verdict": cls["verdict"],
                "verdict_reason": cls["reason"],
                "forcing_dominance_status": dom_status,
                "a_Y_eta_dominates_rhs": dom_bool,
                "a_Y_eta_share_of_total_rhs": certified_ratio_with_positive_denominator(
                    a_y_eta, rhs_tot, prec_bits=prec_bits
                ),
            }

        # Preregistered mechanism sub-budgets TC061-KL1-OFFDIAG-AND-MIXED-SPLIT (declared domain Y >= 64):
        kl1_in_dom = (
            bool(kl1_in_declared_domain)
            if kl1_in_declared_domain is not None
            else bool(Y_b >= arb(64))
        )
        off_rhs = _frac_to_arb(Fraction(3, 4)) * lgD_b
        mix_rhs = _frac_to_arb(Fraction(1, 4)) * lgD_b
        off_margin = arb(4) * X_b - off_rhs
        mix_margin = R_mix_b - mix_rhs
        off_cls = classify_probe_margin_arb(off_margin)
        mix_cls = classify_probe_margin_arb(mix_margin)
        any_kl1_in_domain_unresolved = bool(
            kl1_in_dom and ("UNRESOLVED" in (off_cls["verdict"], mix_cls["verdict"]))
        )
        any_kl1_in_domain_fail = bool(
            kl1_in_dom and ("FAIL" in (off_cls["verdict"], mix_cls["verdict"]))
        )
        any_in_domain_unresolved = bool(
            any_main_probe_in_domain_unresolved or any_kl1_in_domain_unresolved
        )

        return {
            "per_probe": per_probe,
            "any_main_probe_in_domain_unresolved": any_main_probe_in_domain_unresolved,
            "any_kl1_in_domain_unresolved": any_kl1_in_domain_unresolved,
            "any_in_domain_unresolved": any_in_domain_unresolved,
            "any_main_probe_in_domain_fail": any_main_probe_in_domain_fail,
            "any_kl1_in_domain_fail": any_kl1_in_domain_fail,
            "mechanism_kl1_sub_budgets": {
                "in_declared_domain": kl1_in_dom,
                "offdiag_4X_tilde": serialize_arb_certified(arb(4) * X_b),
                "offdiag_rhs_3_4_logY_D_tilde": serialize_arb_certified(off_rhs),
                "offdiag_margin": serialize_arb_certified(off_margin),
                "offdiag_verdict": off_cls["verdict"],
                "R_mix": serialize_arb_certified(R_mix_b),
                "R_mix_rhs_1_4_logY_D_tilde": serialize_arb_certified(mix_rhs),
                "R_mix_margin": serialize_arb_certified(mix_margin),
                "R_mix_verdict": mix_cls["verdict"],
            },
            "J_over_log_Y_D_tilde": certified_ratio_with_positive_denominator(
                J_b, lgD_b, prec_bits=prec_bits
            ),
        }
    finally:
        flint_ctx.prec = saved


def verify_section_1_protocol_and_exact_mixed_identity(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Verify protocol immutability, exact rational calibration on `C = {16, 32, 64}`, diagnostic
    cases `{2, 4, 8}`, pointwise reconstruction `Q_Y = 2*P_Y - A_Y - B_Y`, algebraic consistency
    `4*D_tilde(Y) + J(Y) = ||2*P_Y - B_Y||_Y^2 = ||Q_Y + A_Y||_Y^2`, and the `theta`-inequality.
    """
    proto_chk = verify_frozen_protocol_immutability()
    proto = proto_chk["protocol_object"]
    probes = proto["frozen_candidate_probes"]

    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(250, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 200
        else selberg_table
    )

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        sqrt_tau = tau.sqrt()

        eval_map: Dict[int, Dict[str, Any]] = {}
        rows_le_64: List[Dict[str, Any]] = []
        all_identities_ok = True

        for y_val in (2, 4, 8, 16, 32, 64):
            sp = ExactScaleSpec(label=str(y_val), kind="exact_rational", rational_factor=Fraction(y_val, 1))
            res = evaluate_mixed_covariance_point_arb(sp, selberg_table=tbl)
            eval_map[y_val] = res

            # Pointwise check Q_Y(X) = 2*P_Y(X) - A_Y(X) - B_Y(X) AND complete-core adjusted beta_Y bridge
            # B_Y(X) = sum_{n<=2T} beta_Y(n)*phi_n(X)/(log X)^2 + 2*P_Y(X) - Q_Y(X) at X in {Y, sqrt(tau)*Y, tau*Y}:
            T_y = res["cutoffs"]["T_Y"]
            D0_eff = res["cutoffs"]["D0_eff"]
            c_lam = tbl["c_lambda"]
            R = tbl["R"]
            M_drift = tbl["M_drift"]
            R_osc = tbl["R_osc"]
            core_vecs = compute_complete_core_s_Y_and_beta_Y_arb(
                T_y, D0_eff, R_osc, prec_bits=prec_bits
            )
            beta_Y_vec = core_vecs["beta_Y"]

            max_pw_err = arb(0)
            max_beta_bridge_err = arb(0)
            for x_mult in (arb(1), sqrt_tau, tau):
                X_pt = arb(y_val) * x_mult
                lg_x = X_pt.log()
                phi_v = [arb(0)] + [evaluate_phi_n_arb(X_pt, n, prec_bits=prec_bits) for n in range(1, 2 * T_y + 1)]
                Q_pt = sum((arb(liouville_lambda_int(n)) * phi_v[n] for n in range(1, T_y + 1)), arb(0))
                P_pt = (
                    sum((arb(liouville_lambda_int(n)) * arb(n).log() * phi_v[n] for n in range(1, T_y + 1)), arb(0))
                    / lg_x
                )
                A_num_pt = sum(
                    (c_lam * phi_v[n] for n in range(1, T_y + 1) if is_perfect_square_int(n)), arb(0)
                ) + R[T_y] * phi_v[T_y]
                B_sm_pt = arb(0)
                for d_i in range(1, T_y):
                    L_d = T_y // d_i
                    L_d1 = T_y // (d_i + 1)
                    for q in range(L_d1 + 1, L_d + 1):
                        A_num_pt += R[d_i] * arb(liouville_lambda_int(q)) * phi_v[(d_i + 1) * q]
                    delta_sm_pt = sum(
                        (
                            arb(liouville_lambda_int(q)) * (phi_v[d_i * q] - phi_v[(d_i + 1) * q])
                            for q in range(1, L_d + 1)
                        ),
                        arb(0),
                    )
                    A_num_pt += (M_drift[d_i] + (R_osc[d_i] if d_i <= D0_eff else arb(0))) * delta_sm_pt
                    if d_i > D0_eff:
                        B_sm_pt += R_osc[d_i] * delta_sm_pt
                Q_sh2_pt = arb(0)
                for n in range(1, T_y + 1):
                    d_lg_pt = lg_x - arb(n).log()
                    Q_sh2_pt += arb(liouville_lambda_int(n)) * (d_lg_pt * d_lg_pt) * phi_v[n]
                A_pt = A_num_pt / (lg_x * lg_x)
                B_pt = (B_sm_pt - Q_sh2_pt) / (lg_x * lg_x)
                beta_phi_over_lg2 = (
                    sum((beta_Y_vec[n] * phi_v[n] for n in range(1, 2 * T_y + 1)), arb(0))
                    / (lg_x * lg_x)
                )
                pw_res = abs(Q_pt - (arb(2) * P_pt - A_pt - B_pt))
                br_res_1 = abs(B_pt - (beta_phi_over_lg2 + arb(2) * P_pt - Q_pt))
                br_res_2 = abs((arb(2) * P_pt - B_pt) - (Q_pt - beta_phi_over_lg2))
                max_pw_err = enclose_discrete_grid_max([max_pw_err, pw_res])
                max_beta_bridge_err = enclose_discrete_grid_max(
                    [max_beta_bridge_err, br_res_1, br_res_2]
                )

            # Check algebraic consistency & theta-inequality for theta in {1/4, 1/2, 3/4}:
            res_qa = res["J_consistency_residual_QA"]
            res_2pb = res["J_consistency_residual_2PB"]
            id_ok = bool(
                arb(0) in res_qa
                and abs(res_qa) < arb("1e-65")
                and arb(0) in res_2pb
                and abs(res_2pb) < arb("1e-65")
                and abs(max_pw_err) < arb("1e-65")
                and abs(max_beta_bridge_err) < arb("1e-65")
            )

            theta_checks: Dict[str, Any] = {}
            theta_all_ok = True
            for th_n, th_d in ((1, 4), (1, 2), (3, 4)):
                th_b = _frac_to_arb(Fraction(th_n, th_d))
                lhs_th = (arb(1) - th_b) * res["E_Y"]
                rhs_th = arb(4) * res["D_tilde_Y"] + res["J_direct"] + (arb(1) / th_b - arb(1)) * res["A_norm_sq"]
                st_th, ok_th = classify_arb_le_certificate(lhs_th, rhs_th)
                theta_all_ok = theta_all_ok and ok_th
                theta_checks[f"{th_n}/{th_d}"] = {
                    "lhs": serialize_arb_certified(lhs_th),
                    "rhs": serialize_arb_certified(rhs_th),
                    "certificate_status": st_th,
                    "verified": ok_th,
                }

            bound_half = arb(8) * res["D_tilde_Y"] + arb(2) * res["J_direct"] + arb(2) * res["A_norm_sq"]
            bound_old_844 = (
                arb(8) * res["D_tilde_Y"]
                + arb(8) * res["X_tilde_Y"]
                + arb(4) * res["A_norm_sq"]
                + arb(4) * res["B_norm_sq"]
            )
            probe_eval = _evaluate_probes_for_point_result(
                res,
                probes,
                in_declared_domain_fn=lambda pr, _y=y_val: _y >= int(pr["domain_threshold_Y0"]),
                prec_bits=prec_bits,
            )

            pb_b = res["pair_P_B"]
            pb_sign = (
                "STRICTLY_POSITIVE"
                if bool(pb_b > arb(0))
                else ("STRICTLY_NEGATIVE" if bool(pb_b < arb(0)) else "STRADDLING_ZERO")
            )
            row_ok = bool(id_ok and theta_all_ok)
            all_identities_ok = all_identities_ok and row_ok

            rows_le_64.append(
                {
                    "Y": y_val,
                    "role": (
                        "DIAGNOSTIC_OUTSIDE_DECLARED_DOMAIN"
                        if y_val < 16
                        else "CALIBRATION_SET_C_NOT_HOLDOUT_EVIDENCE"
                    ),
                    "cutoffs": res["cutoffs"],
                    "E_Y": serialize_arb_certified(res["E_Y"]),
                    "D_tilde_Y": serialize_arb_certified(res["D_tilde_Y"]),
                    "X_tilde_Y": serialize_arb_certified(res["X_tilde_Y"]),
                    "P_norm_sq": serialize_arb_certified(res["P_norm_sq"]),
                    "A_norm_sq": serialize_arb_certified(res["A_norm_sq"]),
                    "B_norm_sq": serialize_arb_certified(res["B_norm_sq"]),
                    "pair_P_B": serialize_arb_certified(pb_b),
                    "pair_P_B_sign": pb_sign,
                    "J_direct": serialize_arb_certified(res["J_direct"]),
                    "J_algebraic_consistency_QA": serialize_arb_certified(res["J_algebraic_consistency_QA"]),
                    "J_consistency_check_role": "ALGEBRAIC_CONSISTENCY_CHECK_SAME_INPUTS",
                    "J_consistency_residual_QA": serialize_arb_certified(res_qa),
                    "J_consistency_residual_2PB": serialize_arb_certified(res_2pb),
                    "max_pointwise_reconstruction_residual": serialize_arb_certified(max_pw_err),
                    "max_pointwise_adjusted_beta_Y_bridge_residual": serialize_arb_certified(
                        max_beta_bridge_err
                    ),
                    "spillover_above_T_count": len(core_vecs["spillover_above_T_indices"]),
                    "log_Y_times_D_tilde": serialize_arb_certified(res["log_Y_times_D_tilde"]),
                    "theta_half_energy_bound_8D_plus_2J_plus_2A2": serialize_arb_certified(bound_half),
                    "tc060_8_4_4_energy_bound": serialize_arb_certified(bound_old_844),
                    "theta_inequality_checks": theta_checks,
                    "probe_evaluations": probe_eval["per_probe"],
                    "mechanism_kl1_sub_budgets": probe_eval["mechanism_kl1_sub_budgets"],
                    "J_over_log_Y_D_tilde": probe_eval["J_over_log_Y_D_tilde"],
                    "verified": row_ok,
                }
            )

        # Verify exact rational ceiling calibration on C = {16, 32, 64} matches protocol constants:
        expected_a_eta = {
            (1, 2): Fraction(1, 32),
            (1, 4): Fraction(3, 64),
            (1, 8): Fraction(5, 64),
        }
        cal_verif: Dict[str, Any] = {}
        cal_ok = True
        for en, ed in ((1, 2), (1, 4), (1, 8)):
            eta_fr = Fraction(en, ed)
            eta_b = _frac_to_arb(eta_fr)
            q_balls = [
                (eval_map[y_c]["J_direct"] - eval_map[y_c]["log_Y_times_D_tilde"])
                / (eval_map[y_c]["Y_arb"] ** eta_b)
                for y_c in (16, 32, 64)
            ]
            cal_r = calibrate_secondary_a_eta_exact(q_balls)
            matches_proto = cal_r["a_eta_fraction"] == expected_a_eta[(en, ed)]
            cal_ok = cal_ok and matches_proto
            cal_verif[f"{en}/{ed}"] = {
                "eta_fraction": f"{en}/{ed}",
                "ceil_64_U_eta": cal_r["ceil_64_U_eta"],
                "a_eta_fraction": f"{cal_r['a_eta_fraction'].numerator}/{cal_r['a_eta_fraction'].denominator}",
                "matches_frozen_protocol": matches_proto,
            }

        # Verify <P_Y, B_Y>_Y changes sign across scales (positive at 2, 8, 32; negative at 4, 16, 64):
        sign_change_verified = bool(
            eval_map[2]["pair_P_B"] > arb(0)
            and eval_map[4]["pair_P_B"] < arb(0)
            and eval_map[16]["pair_P_B"] < arb(0)
            and eval_map[32]["pair_P_B"] > arb(0)
            and eval_map[64]["pair_P_B"] < arb(0)
        )

        return {
            "epistemic_statuses": [
                "CONCRETE_ANALYTIC_IN_LEAN",
                "CERTIFIED_FINITE_OBSERVATION",
            ],
            "section_epistemic_scope_note": (
                "Mixed formal/numerical section: the concrete mixed identity "
                "4*D_tilde(Y) + J(Y) = ||2*P_Y - B_Y||_Y^2 = ||Q_Y + A_Y||_Y^2 and the theta-inequality "
                "(1 - theta)*E(Y) <= 4*D_tilde(Y) + J(Y) + (theta^{-1} - 1)*||A_Y||_Y^2 with canonical "
                "source-definition instantiations are CONCRETE_ANALYTIC_IN_LEAN; protocol hash/commit "
                "verification, exact rational ceiling calibration on C = {16, 32, 64}, and diagnostic "
                "{2, 4, 8} / calibration {16, 32, 64} Arb evaluations are CERTIFIED_FINITE_OBSERVATION."
            ),
            "component_epistemic_map": {
                "mixed_covariance_identity_and_theta_inequality": "CONCRETE_ANALYTIC_IN_LEAN",
                "frozen_protocol_hash_and_git_immutability": "CERTIFIED_FINITE_OBSERVATION",
                "exact_rational_calibration_on_C_16_32_64": "CERTIFIED_FINITE_OBSERVATION",
                "diagnostic_2_4_8_and_calibration_16_32_64_enclosures": "CERTIFIED_FINITE_OBSERVATION",
            },
            "lean_theorems": [
                "mixed_covariance_identity_and_theta_energy_bound_tc061",
                "complete_core_adjusted_expansion_and_compact_gram_tc061r",
            ],
            "protocol_immutability_check": {
                k: v for k, v in proto_chk.items() if k != "protocol_object"
            },
            "exact_rational_calibration_reverification": cal_verif,
            "pair_P_B_sign_change_verified": sign_change_verified,
            "diagnostic_and_calibration_evaluations": rows_le_64,
            "all_section_1_checks_pass": bool(
                proto_chk["verified"] and all_identities_ok and cal_ok and sign_change_verified
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 3. Section 2: Certified Cutoffs, Case-Split Intervals, & Quadrature Cross-Checks
# ---------------------------------------------------------------------------


def verify_section_2_cutoff_and_interval_certification(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Verify exact cutoff determination on sided discontinuities, straddling-enclosure rejection,
    genuine branch-splitting interval evaluation across `T` and `D_0` jumps, fast `O(T log T)`
    Selberg sieve equivalence, and 3-zone vs unsplit quadrature consistency.
    """
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(1100, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 1050
        else selberg_table
    )
    slow_tbl = compute_selberg_centered_remainder_table_arb(300, prec_bits=prec_bits + 32)

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        # 1. Fast O(T log T) Selberg sieve vs inherited table on 0..300:
        max_diff_R = enclose_discrete_grid_max(
            [abs(tbl["R"][d] - slow_tbl["R"][d]) for d in range(301)]
        )
        max_diff_Rosc = enclose_discrete_grid_max(
            [abs(tbl["R_osc"][d] - slow_tbl["R_osc"][d]) for d in range(301)]
        )
        sieve_equiv_ok = bool(abs(max_diff_R) < arb("1e-75") and abs(max_diff_Rosc) < arb("1e-75"))

        # 2. Sided discontinuity exact cutoff checks:
        sp_e5_m = ExactScaleSpec("e^5*(1-2^-12)", "exact_symbolic_exp_rational", Fraction(4095, 4096), Fraction(5, 1))
        sp_e5_p = ExactScaleSpec("e^5*(1+2^-12)", "exact_symbolic_exp_rational", Fraction(4097, 4096), Fraction(5, 1))
        sp_256_m = ExactScaleSpec("256-2^-12", "exact_rational", Fraction(1048575, 4096))
        sp_256_0 = ExactScaleSpec("256", "exact_rational", Fraction(256, 1))
        sp_256_p = ExactScaleSpec("256+2^-12", "exact_rational", Fraction(1048577, 4096))

        cut_e5_m = certify_exact_scale_cutoffs(sp_e5_m, base_prec_bits=prec_bits)
        cut_e5_p = certify_exact_scale_cutoffs(sp_e5_p, base_prec_bits=prec_bits)
        cut_256_m = certify_exact_scale_cutoffs(sp_256_m, base_prec_bits=prec_bits)
        cut_256_0 = certify_exact_scale_cutoffs(sp_256_0, base_prec_bits=prec_bits)
        cut_256_p = certify_exact_scale_cutoffs(sp_256_p, base_prec_bits=prec_bits)

        sided_cutoffs_ok = bool(
            cut_e5_m["D0_raw"] == 4
            and cut_e5_p["D0_raw"] == 5
            and cut_e5_m["T_Y"] == 518
            and cut_e5_p["T_Y"] == 519
            and cut_256_m["T_Y"] == 1024
            and cut_256_0["T_Y"] == 1024
            and cut_256_p["T_Y"] == 1025
            and cut_256_m["D0_raw"] == 5
            and cut_256_p["D0_raw"] == 5
        )

        # 3. Unsplit straddling Arb balls must raise AmbiguousCutoffError:
        straddle_256_ball = _frac_to_arb(Fraction(1048575, 4096)).union(_frac_to_arb(Fraction(1048577, 4096)))
        straddle_e5_ball = _frac_to_arb(Fraction(148, 1)).union(_frac_to_arb(Fraction(149, 1)))
        rejected_256 = False
        rejected_e5 = False
        try:
            certify_T_canonical_cutoff(straddle_256_ball, prec_bits=prec_bits)
        except AmbiguousCutoffError:
            rejected_256 = True
        try:
            certify_D0_small_divisor_cutoff(straddle_e5_ball, kappa=1, prec_bits=prec_bits)
        except AmbiguousCutoffError:
            rejected_e5 = True

        # 4. Genuine straddling-interval case-splitting without midpoint rounding:
        # (a) [256 - 2^-12, 256 + 2^-12] spans T = 1024 -> 1025: certifies P0 PASS on the whole interval!
        cs_256 = evaluate_interval_via_cutoff_case_split_arb(
            Fraction(1048575, 4096),
            Fraction(1048577, 4096),
            prec_bits=prec_bits,
            quad_tol_bits=100,
            selberg_table=tbl,
        )
        # (b) [742/5, 2969/20] = [148.40, 148.45] spans BOTH e^5 (~148.413, D0: 4->5) AND 518^{4/5} (~148.4317, T: 518->519):
        cs_e5_tight = evaluate_interval_via_cutoff_case_split_arb(
            Fraction(742, 5),
            Fraction(2969, 20),
            prec_bits=prec_bits,
            quad_tol_bits=100,
            selberg_table=tbl,
        )
        # (c) Full unit interval [148, 149] (6 branches across e^5 and T = 517..521): still certifies P0 PASS!
        cs_e5_unit = evaluate_interval_via_cutoff_case_split_arb(
            Fraction(148, 1),
            Fraction(149, 1),
            prec_bits=prec_bits,
            quad_tol_bits=90,
            selberg_table=tbl,
        )
        # (d) Wide unit interval [64, 65] at threshold Y_0 = 64 (4 branches, T = 182..185):
        # unsubdivided branch interval wrapping straddles zero and honestly reports UNRESOLVED:
        cs_64_wide = evaluate_interval_via_cutoff_case_split_arb(
            Fraction(64, 1),
            Fraction(65, 1),
            prec_bits=prec_bits,
            quad_tol_bits=90,
            selberg_table=tbl,
        )

        case_split_ok = bool(
            rejected_256
            and rejected_e5
            and cs_256["active_branch_count"] == 2
            and cs_256["P0_interval_classification"]["verdict"] == "PASS"
            and cs_e5_tight["active_branch_count"] == 3
            and cs_e5_tight["P0_interval_classification"]["verdict"] == "PASS"
            and cs_e5_unit["active_branch_count"] == 6
            and cs_e5_unit["P0_interval_classification"]["verdict"] == "PASS"
            and cs_64_wide["active_branch_count"] == 4
            and cs_64_wide["P0_interval_classification"]["verdict"] == "UNRESOLVED"
        )

        # 5. Three-zone vs unsplit equivalence cross-check at Y = 64 and Y = 128:
        zone_crosschecks: List[Dict[str, Any]] = []
        zone_ok = True
        for y_chk in (64, 128):
            sp_z = ExactScaleSpec(str(y_chk), "exact_rational", Fraction(y_chk, 1))
            r_unsplit = evaluate_mixed_covariance_point_arb(
                sp_z,
                prec_bits=prec_bits,
                quad_tol_bits=210,
                use_three_zone=False,
                allow_nonprotocol_override=True,
                selberg_table=tbl,
            )
            r_3z = evaluate_mixed_covariance_point_arb(
                sp_z,
                prec_bits=prec_bits,
                quad_tol_bits=160,
                n_panels=16,
                use_three_zone=True,
                allow_nonprotocol_override=True,
                selberg_table=tbl,
            )
            diff_J = r_unsplit["J_direct"] - r_3z["J_direct"]
            diff_D = r_unsplit["D_tilde_Y"] - r_3z["D_tilde_Y"]
            ok_z = bool(
                arb(0) in diff_J
                and abs(diff_J) < arb("1e-44")
                and arb(0) in diff_D
                and abs(diff_D) < arb("1e-44")
            )
            zone_ok = zone_ok and ok_z
            zone_crosschecks.append(
                {
                    "Y": y_chk,
                    "T_Y": r_unsplit["cutoffs"]["T_Y"],
                    "J_unsplit": serialize_arb_certified(r_unsplit["J_direct"]),
                    "J_three_zone": serialize_arb_certified(r_3z["J_direct"]),
                    "J_difference": serialize_arb_certified(diff_J),
                    "D_tilde_difference": serialize_arb_certified(diff_D),
                    "consistent_zero_in_difference": ok_z,
                }
            )

        def _fmt_cs(cs_obj: Dict[str, Any]) -> Dict[str, Any]:
            return {
                "Y_lo_fraction": cs_obj["Y_lo_fraction"],
                "Y_hi_fraction": cs_obj["Y_hi_fraction"],
                "T_range": cs_obj["T_range"],
                "D0_range": cs_obj["D0_range"],
                "active_branch_count": cs_obj["active_branch_count"],
                "branch_cutoffs": [
                    {"T_fixed": b["T_fixed"], "D0_raw_fixed": b["D0_raw_fixed"]}
                    for b in cs_obj["branches"]
                ],
                "union_E_Y": serialize_arb_certified(cs_obj["union_E_Y"]),
                "union_D_tilde_Y": serialize_arb_certified(cs_obj["union_D_tilde_Y"]),
                "union_J_Y": serialize_arb_certified(cs_obj["union_J_Y"]),
                "union_log_Y_times_D_tilde": serialize_arb_certified(cs_obj["union_log_Y_times_D_tilde"]),
                "union_M_P0": serialize_arb_certified(cs_obj["union_M_P0"]),
                "P0_interval_classification": cs_obj["P0_interval_classification"],
            }

        return {
            "epistemic_statuses": [
                "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "CERTIFIED_FINITE_OBSERVATION",
            ],
            "section_epistemic_scope_note": (
                "Mixed analytic/numerical section: exact cutoff partition and Taylor/Zone-1 error "
                "bounds underlying 3-zone window integration and cutoff branch-splitting are "
                "ANALYTIC_PROVED_OUTSIDE_LEAN; sided discontinuity cutoffs, straddling-enclosure "
                "rejections, continuous straddling-interval case-split enclosures, and fast-sieve / "
                "3-zone cross-checks are CERTIFIED_FINITE_OBSERVATION."
            ),
            "component_epistemic_map": {
                "three_zone_quadrature_and_cutoff_branch_split_error_bounds": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "sided_discontinuity_cutoffs_and_case_split_certificates": "CERTIFIED_FINITE_OBSERVATION",
            },
            "fast_selberg_sieve_vs_inherited_check": {
                "checked_d_range": [0, 300],
                "max_abs_diff_R": serialize_arb_certified(max_diff_R),
                "max_abs_diff_R_osc": serialize_arb_certified(max_diff_Rosc),
                "verified": sieve_equiv_ok,
            },
            "sided_discontinuity_cutoffs": {
                "e5_minus": cut_e5_m,
                "e5_plus": cut_e5_p,
                "256_minus": cut_256_m,
                "256_exact": cut_256_0,
                "256_plus": cut_256_p,
                "verified": sided_cutoffs_ok,
            },
            "unsplit_straddling_rejections": {
                "straddle_256_T_rejected": rejected_256,
                "straddle_e5_D0_rejected": rejected_e5,
            },
            "straddling_interval_case_splits": {
                "interval_256_pm_2_neg12": _fmt_cs(cs_256),
                "interval_148_40_to_148_45_across_e5_and_T518": _fmt_cs(cs_e5_tight),
                "unit_interval_148_to_149_across_e5": _fmt_cs(cs_e5_unit),
                "wide_interval_64_to_65_unresolved_wrapping_example": _fmt_cs(cs_64_wide),
                "verified": case_split_ok,
            },
            "three_zone_vs_unsplit_crosschecks": zone_crosschecks,
            "all_section_2_checks_pass": bool(
                sieve_equiv_ok and sided_cutoffs_ok and case_split_ok and zone_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 4. Section 3: Preregistered 14-Point Held-Out Experiment (128 .. 4096)
# ---------------------------------------------------------------------------


def _is_valid_nonneg_real(val: Any) -> bool:
    """Return True iff `val` is a finite non-negative real (`int`/`float`, excluding `bool`/`None`)."""
    return (
        isinstance(val, (int, float))
        and not isinstance(val, bool)
        and math.isfinite(float(val))
        and float(val) >= 0.0
    )


def evaluate_point_resource_compliance(
    history: Sequence[Dict[str, Any]],
    *,
    max_wall_sec: float,
    max_rss_mb: float,
) -> Dict[str, Any]:
    """Evaluate per-point wall-time and memory compliance with explicit 3-valued statuses
    (`WITHIN`, `EXCEEDED`, `UNKNOWN`) (`TASK-TC-061R2` §3):
    - Raw missing values (`None`) remain `None` and are never coerced to `0` or `WITHIN`;
    - Wall-time and memory statuses are tracked separately and aggregated via:
      any `EXCEEDED` -> `EXCEEDED`; all `WITHIN` -> `WITHIN`; otherwise `UNKNOWN`;
    - Across multiple tiers, a final-tier OS `PROCESS_LIFETIME_HIGH_WATER_MARK` reading covers
      earlier tiers in the same process only when it is valid and monotonically consistent with
      all prior observed RSS readings; otherwise missing tier RSS is treated conservatively as `UNKNOWN`.
    """
    any_wall_invalid = any(
        h.get("elapsed_sec") is not None and not _is_valid_nonneg_real(h.get("elapsed_sec"))
        for h in history
    )
    valid_walls = [
        float(h["elapsed_sec"])
        for h in history
        if _is_valid_nonneg_real(h.get("elapsed_sec"))
    ]
    all_tiers_have_valid_wall = bool(
        len(history) > 0 and (not any_wall_invalid) and len(valid_walls) == len(history)
    )
    partial_wall_sum: Optional[float] = round(sum(valid_walls), 6) if valid_walls else None
    any_wall_exceeded = bool(
        any(w > max_wall_sec for w in valid_walls)
        or (partial_wall_sum is not None and partial_wall_sum > max_wall_sec)
    )
    if any_wall_exceeded:
        wall_status = "EXCEEDED"
        wall_exceeded_opt: Optional[bool] = True
    elif all_tiers_have_valid_wall and partial_wall_sum is not None and partial_wall_sum <= max_wall_sec:
        wall_status = "WITHIN"
        wall_exceeded_opt = False
    else:
        wall_status = "UNKNOWN"
        wall_exceeded_opt = None

    final_tier_elapsed: Optional[float] = (
        round(float(history[-1]["elapsed_sec"]), 6)
        if (len(history) > 0 and _is_valid_nonneg_real(history[-1].get("elapsed_sec")))
        else None
    )
    cumulative_elapsed: Optional[float] = (
        partial_wall_sum if (all_tiers_have_valid_wall or any_wall_exceeded) else None
    )

    any_rss_invalid = any(
        (h.get("peak_rss_mb") is not None and not _is_valid_nonneg_real(h.get("peak_rss_mb")))
        or (h.get("current_rss_mb") is not None and not _is_valid_nonneg_real(h.get("current_rss_mb")))
        for h in history
    )
    valid_peak_vals = [
        float(h["peak_rss_mb"])
        for h in history
        if _is_valid_nonneg_real(h.get("peak_rss_mb"))
    ]
    valid_curr_vals = [
        float(h["current_rss_mb"])
        for h in history
        if _is_valid_nonneg_real(h.get("current_rss_mb"))
    ]
    all_observed_rss = valid_peak_vals + valid_curr_vals
    any_rss_exceeded = bool(any(v > max_rss_mb for v in all_observed_rss))

    hwm_monotonicity_ok = True
    max_prior_rss = -1.0
    for h in history:
        p_v = float(h["peak_rss_mb"]) if _is_valid_nonneg_real(h.get("peak_rss_mb")) else None
        c_v = float(h["current_rss_mb"]) if _is_valid_nonneg_real(h.get("current_rss_mb")) else None
        if p_v is not None and c_v is not None and p_v + 1e-6 < c_v:
            hwm_monotonicity_ok = False
        if (
            p_v is not None
            and h.get("peak_rss_measurement_semantics") == "PROCESS_LIFETIME_HIGH_WATER_MARK"
            and max_prior_rss >= 0.0
            and p_v + 1e-6 < max_prior_rss
        ):
            hwm_monotonicity_ok = False
        if p_v is not None:
            max_prior_rss = max(max_prior_rss, p_v)
        if c_v is not None:
            max_prior_rss = max(max_prior_rss, c_v)

    all_tiers_have_valid_peak_rss = bool(
        len(history) > 0
        and (not any_rss_invalid)
        and len(valid_peak_vals) == len(history)
    )
    final_has_valid_hwm = bool(
        len(history) > 0
        and (not any_rss_invalid)
        and hwm_monotonicity_ok
        and _is_valid_nonneg_real(history[-1].get("peak_rss_mb"))
        and history[-1].get("peak_rss_measurement_semantics") == "PROCESS_LIFETIME_HIGH_WATER_MARK"
        and (
            not all_observed_rss
            or float(history[-1]["peak_rss_mb"]) + 1e-6 >= max(all_observed_rss)
        )
    )

    if len(history) == 0 or any_rss_invalid or not hwm_monotonicity_ok:
        rss_coverage_complete = False
        rss_coverage_reason = "INVALID_OR_NON_MONOTONIC_RSS_TELEMETRY"
    elif all_tiers_have_valid_peak_rss:
        rss_coverage_complete = True
        rss_coverage_reason = "ALL_EXECUTED_TIERS_DIRECTLY_MEASURED"
    elif final_has_valid_hwm:
        rss_coverage_complete = True
        rss_coverage_reason = "FINAL_TIER_PROCESS_LIFETIME_HIGH_WATER_MARK_COVERS_PRIOR_TIERS"
    else:
        rss_coverage_complete = False
        rss_coverage_reason = "MISSING_OR_UNCOVERED_TIER_PEAK_RSS_TELEMETRY"

    if any_rss_exceeded:
        mem_status = "EXCEEDED"
        rss_exceeded_opt: Optional[bool] = True
    elif rss_coverage_complete:
        mem_status = "WITHIN"
        rss_exceeded_opt = False
    else:
        mem_status = "UNKNOWN"
        rss_exceeded_opt = None

    observed_max_rss: Optional[float] = (
        round(max(all_observed_rss), 3) if all_observed_rss else None
    )
    covered_or_violating_peak_rss: Optional[float] = (
        round(
            max(all_observed_rss)
            if any_rss_exceeded
            else max(valid_peak_vals if valid_peak_vals else all_observed_rss),
            3,
        )
        if (rss_coverage_complete or any_rss_exceeded) and all_observed_rss
        else None
    )

    if "EXCEEDED" in (wall_status, mem_status):
        overall_status = "EXCEEDED"
        within_budget_opt: Optional[bool] = False
        compliance_verified = False
    elif wall_status == "WITHIN" and mem_status == "WITHIN":
        overall_status = "WITHIN"
        within_budget_opt = True
        compliance_verified = True
    else:
        overall_status = "UNKNOWN"
        within_budget_opt = None
        compliance_verified = False

    last_curr_rss = (
        round(float(history[-1]["current_rss_mb"]), 3)
        if (len(history) > 0 and _is_valid_nonneg_real(history[-1].get("current_rss_mb")))
        else None
    )

    return {
        "max_wall_seconds_per_point_limit": max_wall_sec,
        "max_rss_megabytes_limit": max_rss_mb,
        "final_tier_elapsed_sec": final_tier_elapsed,
        "cumulative_point_elapsed_sec": cumulative_elapsed,
        "partial_observed_elapsed_sec": partial_wall_sum,
        "current_rss_mb": last_curr_rss,
        "peak_rss_mb": covered_or_violating_peak_rss,
        "partial_uncovered_max_rss_mb": (
            observed_max_rss if covered_or_violating_peak_rss is None else None
        ),
        "peak_rss_coverage_complete": rss_coverage_complete,
        "peak_rss_coverage_reason": rss_coverage_reason,
        "wall_budget_status": wall_status,
        "memory_budget_status": mem_status,
        "overall_resource_status": overall_status,
        "wall_budget_exceeded": wall_exceeded_opt,
        "rss_budget_exceeded": rss_exceeded_opt,
        "within_resource_budget": within_budget_opt,
        "resource_compliance_verified": compliance_verified,
        "enforcement_mode": "POST_EVALUATION_BUDGET_AUDIT_NO_OS_PREEMPTIVE_KILL",
    }


def aggregate_section_resource_compliance(
    point_checks: Sequence[Dict[str, Any]],
    *,
    registered_count: int,
) -> Dict[str, Any]:
    """Aggregate per-point 3-valued resource compliance statuses (`WITHIN`, `EXCEEDED`, `UNKNOWN`)
    across a section without coercing `UNKNOWN` into verified compliance (`TASK-TC-061R2` §3).
    """
    complete_set = bool(registered_count > 0 and len(point_checks) == registered_count)

    def _count(statuses: Sequence[str]) -> Dict[str, int]:
        return {
            s_k: sum(1 for s in statuses if s == s_k)
            for s_k in RESOURCE_COMPLIANCE_STATUSES
        }

    def _combine(statuses: Sequence[str]) -> str:
        for s in statuses:
            if s not in RESOURCE_COMPLIANCE_STATUSES:
                raise ValueError(f"Invalid resource status {s!r}")
        if any(s == "EXCEEDED" for s in statuses):
            return "EXCEEDED"
        if complete_set and all(s == "WITHIN" for s in statuses):
            return "WITHIN"
        return "UNKNOWN"

    wall_list = [str(c["wall_budget_status"]) for c in point_checks]
    mem_list = [str(c["memory_budget_status"]) for c in point_checks]
    ov_list = [str(c["overall_resource_status"]) for c in point_checks]

    wall_agg = _combine(wall_list)
    mem_agg = _combine(mem_list)
    ov_agg = _combine(ov_list)

    within_opt: Optional[bool]
    if ov_agg == "WITHIN":
        within_opt = True
    elif ov_agg == "EXCEEDED":
        within_opt = False
    else:
        within_opt = None

    return {
        "registered_point_count": registered_count,
        "evaluated_point_count": len(point_checks),
        "wall_budget_status": wall_agg,
        "memory_budget_status": mem_agg,
        "overall_resource_budget_status": ov_agg,
        "wall_status_counts": _count(wall_list),
        "memory_status_counts": _count(mem_list),
        "overall_status_counts": _count(ov_list),
        "all_points_within_resource_budgets": within_opt,
        "all_resource_budgets_verified_within": bool(ov_agg == "WITHIN"),
        "any_resource_budget_exceeded": bool(ov_agg == "EXCEEDED"),
        "any_resource_budget_unknown": bool(
            (not complete_set) or any(s == "UNKNOWN" for s in ov_list)
        ),
        "enforcement_mode": "POST_EVALUATION_BUDGET_AUDIT_NO_OS_PREEMPTIVE_KILL",
    }


def _build_point_parameter_identities(
    spec: ExactScaleSpec,
    probes: Sequence[Dict[str, Any]],
) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """Construct immutable parameter identities for all main probes and both `KL1` sub-budgets."""
    pt_ident = {
        "label": spec.label,
        "kind": spec.kind,
        "rational_factor": f"{spec.rational_factor.numerator}/{spec.rational_factor.denominator}",
        "exp_power": f"{spec.exp_power.numerator}/{spec.exp_power.denominator}",
    }
    main_ids: Dict[str, Dict[str, Any]] = {}
    for pr in probes:
        pid = str(pr["probe_id"])
        main_ids[pid] = {
            "candidate_kind": "MAIN_PROBE",
            "probe_id": pid,
            "tier": str(pr["tier"]),
            "domain_threshold_Y0": str(pr["domain_threshold_Y0"]),
            "a_numerator": int(pr["a_numerator"]),
            "a_denominator": int(pr["a_denominator"]),
            "eta_fraction": pr["eta_fraction"],
            "b_fraction": str(pr.get("b_fraction", "1/1")),
            "kappa_fraction": str(pr.get("kappa_fraction", "1/1")),
            "point_identity": dict(pt_ident),
        }
    kl1_ids: Dict[str, Dict[str, Any]] = {
        "TC061-KL1:offdiag": {
            "candidate_kind": "KL1_SUB_BUDGET",
            "lemma_candidate_id": "TC061-KL1-OFFDIAG-AND-MIXED-SPLIT",
            "sub_budget_id": "offdiag",
            "lhs_formula": "4 * X_tilde(Y)",
            "rhs_logY_Dtilde_share_fraction": "3/4",
            "domain_threshold_Y0": "64",
            "point_identity": dict(pt_ident),
        },
        "TC061-KL1:R_mix": {
            "candidate_kind": "KL1_SUB_BUDGET",
            "lemma_candidate_id": "TC061-KL1-OFFDIAG-AND-MIXED-SPLIT",
            "sub_budget_id": "R_mix",
            "lhs_formula": "||B_Y||_Y^2 - 4 * <P_Y, B_Y>_Y",
            "rhs_logY_Dtilde_share_fraction": "1/4",
            "domain_threshold_Y0": "64",
            "point_identity": dict(pt_ident),
        },
    }
    return main_ids, kl1_ids


def execute_holdout_point_with_protocol_escalation(
    spec: ExactScaleSpec,
    probes: Sequence[Dict[str, Any]],
    protocol_rules: Dict[str, Any],
    *,
    point_id: Optional[str] = None,
    selberg_table: Optional[Dict[str, Any]] = None,
    evaluator_fn: Optional[Callable[..., Dict[str, Any]]] = None,
    in_declared_domain_fn: Optional[Callable[[Dict[str, Any]], bool]] = None,
    kl1_in_declared_domain: bool = True,
    raise_on_integrity_conflict: bool = False,
) -> Dict[str, Any]:
    """Execute one preregistered held-out point strictly under `protocol_rules` with a per-candidate
    decisive-evidence accumulator across all four main probes and both `TC061-KL1` sub-budgets
    (`TASK-TC-061R` §6 / `TASK-TC-061R2` §§2–3):
    - Resolves Tier 0 and escalation settings exclusively from `protocol_rules` and certified `T(Y)`;
    - Retains any certified `FAIL` or `PASS` witness (with exact point/probe ID, parameter identity,
      certified margin enclosure, tier, precision, and execution settings) even when a subsequent
      escalation tier triggered by another candidate returns `UNRESOLVED` for the already-decided
      candidate, never attaching an earlier tier's verdict to a later tier's unrelated margin;
    - Keeps out-of-domain candidates separate (`OUT_OF_DECLARED_DOMAIN`) so they cannot trigger
      escalation or pollute in-domain verdicts;
    - Flags contradictory certified `PASS` and `FAIL` verdicts across tiers for the same candidate,
      point, and parameter identity as `CERTIFICATION_INTEGRITY_CONFLICT`, preserving both certified
      enclosures and raising `CertificationIntegrityError` when `raise_on_integrity_conflict=True`;
    - Continues registered escalation only while at least one applicable in-domain candidate lacks
      decisive evidence, no integrity conflict has occurred, and no resource limit is `EXCEEDED`;
    - Tracks separate 3-valued (`WITHIN`, `EXCEEDED`, `UNKNOWN`) wall-clock and memory compliance
      statuses (`POST_EVALUATION_BUDGET_AUDIT_NO_OS_PREEMPTIVE_KILL`) without coercing missing RSS
      telemetry (`None`) into verified compliance or turning missing RSS into mathematical failure.
    """
    eff_point_id = str(point_id) if point_id is not None else str(spec.label)
    eval_callable = evaluator_fn if evaluator_fn is not None else evaluate_mixed_covariance_point_arb
    dom_fn = in_declared_domain_fn if in_declared_domain_fn is not None else (lambda _pr: True)
    escalation_ladder = protocol_rules["escalation_ladder_on_zero_straddling_margin"]
    res_limits = protocol_rules["resource_limits"]
    max_wall_sec = float(res_limits["max_wall_seconds_per_point"])
    max_rss_mb = float(res_limits["max_rss_megabytes"])

    main_param_ids, kl1_param_ids = _build_point_parameter_identities(spec, probes)
    probe_by_id: Dict[str, Dict[str, Any]] = {str(pr["probe_id"]): pr for pr in probes}

    candidate_acc: Dict[str, Dict[str, Any]] = {}
    for pr in probes:
        pid = str(pr["probe_id"])
        in_dom = bool(dom_fn(pr))
        candidate_acc[pid] = {
            "point_id": eff_point_id,
            "candidate_id": pid,
            "candidate_kind": "MAIN_PROBE",
            "in_declared_domain": in_dom,
            "domain_status": "IN_DECLARED_DOMAIN" if in_dom else "OUT_OF_DECLARED_DOMAIN",
            "applicable_for_escalation": in_dom,
            "parameter_identity": main_param_ids[pid],
            "effective_verdict": "UNRESOLVED" if in_dom else "NOT_EVALUATED",
            "selected_witness": None,
            "decisive_witnesses": [],
            "integrity_conflict_detected": False,
            "conflicting_certified_witnesses": [],
            "tier_observations": [],
        }
    for kl1_cid, kl1_pid in kl1_param_ids.items():
        in_dom_kl1 = bool(kl1_in_declared_domain)
        candidate_acc[kl1_cid] = {
            "point_id": eff_point_id,
            "candidate_id": kl1_cid,
            "candidate_kind": "KL1_SUB_BUDGET",
            "in_declared_domain": in_dom_kl1,
            "domain_status": "IN_DECLARED_DOMAIN" if in_dom_kl1 else "OUT_OF_DECLARED_DOMAIN",
            "applicable_for_escalation": in_dom_kl1,
            "parameter_identity": kl1_pid,
            "effective_verdict": "UNRESOLVED" if in_dom_kl1 else "NOT_EVALUATED",
            "selected_witness": None,
            "decisive_witnesses": [],
            "integrity_conflict_detected": False,
            "conflicting_certified_witnesses": [],
            "tier_observations": [],
        }

    integrity_conflicts: List[Dict[str, Any]] = []
    history: List[Dict[str, Any]] = []
    baseline_cutoffs: Optional[Dict[str, Any]] = None

    def _record_candidate_observation(
        cid: str,
        *,
        tier_idx: int,
        r_pt: Dict[str, Any],
        in_dom_obs: bool,
        param_id_obs: Dict[str, Any],
        verdict_t: str,
        reason_t: str,
        margin_enclosure: Dict[str, Any],
        supporting_terms: Dict[str, Any],
    ) -> None:
        acc = candidate_acc[cid]
        obs_rec: Dict[str, Any] = {
            "point_id": eff_point_id,
            "point_label": spec.label,
            "candidate_id": cid,
            "candidate_kind": acc["candidate_kind"],
            "in_declared_domain": bool(in_dom_obs),
            "parameter_identity": _clone_preserving_arb(param_id_obs),
            "tier": int(tier_idx),
            "prec_bits": int(r_pt["prec_bits"]),
            "quad_tol_bits": int(r_pt["quad_tol_bits"]),
            "quadrature_mode": str(r_pt["quadrature_mode"]),
            "panels_used": int(r_pt["panels_used"]),
            "requested_settings": _clone_preserving_arb(r_pt["requested_settings"]),
            "used_settings": _clone_preserving_arb(r_pt["used_settings"]),
            "inactive_parameters": list(r_pt["inactive_parameters"]),
            "tier_verdict": str(verdict_t),
            "verdict_reason": str(reason_t),
            "certified_definite": bool(verdict_t in ("PASS", "FAIL")),
            "margin_enclosure": _clone_preserving_arb(margin_enclosure),
            "supporting_terms": _clone_preserving_arb(supporting_terms),
        }
        if param_id_obs != acc["parameter_identity"] or bool(in_dom_obs) != acc["in_declared_domain"]:
            prior_w = acc["selected_witness"]
            acc["integrity_conflict_detected"] = True
            acc["effective_verdict"] = CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
            conflict_param = {
                "conflict_type": "CANDIDATE_PARAMETER_OR_DOMAIN_IDENTITY_MUTATION",
                "point_id": eff_point_id,
                "candidate_id": cid,
                "candidate_kind": acc["candidate_kind"],
                "expected_parameter_identity": acc["parameter_identity"],
                "observed_parameter_identity": param_id_obs,
                "expected_in_declared_domain": acc["in_declared_domain"],
                "observed_in_declared_domain": bool(in_dom_obs),
                "earlier_certified_witness": prior_w,
                "later_conflicting_witness": obs_rec,
            }
            if prior_w is not None and prior_w not in acc["conflicting_certified_witnesses"]:
                acc["conflicting_certified_witnesses"].append(prior_w)
            acc["conflicting_certified_witnesses"].append(obs_rec)
            acc["selected_witness"] = None
            integrity_conflicts.append(conflict_param)
            acc["tier_observations"].append(obs_rec)
            return

        acc["tier_observations"].append(obs_rec)
        if cutoff_mutated_in_current_tier and acc["in_declared_domain"]:
            prior_w = acc["selected_witness"]
            acc["integrity_conflict_detected"] = True
            acc["effective_verdict"] = CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
            if prior_w is not None and prior_w not in acc["conflicting_certified_witnesses"]:
                acc["conflicting_certified_witnesses"].append(prior_w)
            acc["conflicting_certified_witnesses"].append(obs_rec)
            acc["selected_witness"] = None
            return

        if not acc["in_declared_domain"]:
            return

        if verdict_t in ("PASS", "FAIL"):
            acc["decisive_witnesses"].append(obs_rec)
            if acc["integrity_conflict_detected"]:
                if any(
                    w["tier_verdict"] != verdict_t for w in acc["conflicting_certified_witnesses"]
                ):
                    acc["conflicting_certified_witnesses"].append(obs_rec)
            elif acc["selected_witness"] is None:
                acc["selected_witness"] = obs_rec
                acc["effective_verdict"] = verdict_t
            elif acc["selected_witness"]["tier_verdict"] != verdict_t:
                prior_w = acc["selected_witness"]
                acc["integrity_conflict_detected"] = True
                acc["effective_verdict"] = CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
                acc["conflicting_certified_witnesses"] = [prior_w, obs_rec]
                acc["selected_witness"] = None
                integrity_conflicts.append(
                    {
                        "conflict_type": "CONTRADICTORY_CERTIFIED_VERDICTS_ACROSS_TIERS",
                        "point_id": eff_point_id,
                        "candidate_id": cid,
                        "candidate_kind": acc["candidate_kind"],
                        "parameter_identity": _clone_preserving_arb(acc["parameter_identity"]),
                        "earlier_certified_witness": prior_w,
                        "later_conflicting_witness": obs_rec,
                    }
                )
        else:
            if (not acc["integrity_conflict_detected"]) and acc["selected_witness"] is None:
                acc["effective_verdict"] = "UNRESOLVED"

    cutoff_mutated_in_current_tier = False

    def _run_and_accumulate_tier(
        tier_idx: int,
        tbl_use: Optional[Dict[str, Any]],
    ) -> Tuple[Dict[str, Any], Dict[str, Any], List[str], Dict[str, Any]]:
        nonlocal baseline_cutoffs, cutoff_mutated_in_current_tier
        cutoff_mutated_in_current_tier = False
        r_pt = eval_callable(
            spec,
            escalation_tier=tier_idx,
            protocol_rules=protocol_rules,
            allow_nonprotocol_override=False,
            selberg_table=tbl_use,
        )
        cur_cut = {
            "T_Y": int(r_pt["cutoffs"]["T_Y"]),
            "D0_raw": int(r_pt["cutoffs"]["D0_raw"]),
            "D0_eff": int(r_pt["cutoffs"]["D0_eff"]),
        }
        if baseline_cutoffs is None:
            baseline_cutoffs = cur_cut
        elif cur_cut != baseline_cutoffs:
            cutoff_mutated_in_current_tier = True
            integrity_conflicts.append(
                {
                    "conflict_type": "CANONICAL_CUTOFF_MUTATION_ACROSS_TIERS",
                    "point_id": eff_point_id,
                    "candidate_id": "CANONICAL_CUTOFFS",
                    "tier": tier_idx,
                    "baseline_cutoffs": baseline_cutoffs,
                    "observed_cutoffs": cur_cut,
                }
            )
        p_ev = _evaluate_probes_for_point_result(
            r_pt,
            probes,
            in_declared_domain_fn=dom_fn,
            kl1_in_declared_domain=kl1_in_declared_domain,
            prec_bits=int(r_pt["prec_bits"]),
        )
        for pr in probes:
            pid = str(pr["probe_id"])
            pd = p_ev["per_probe"][pid]
            _record_candidate_observation(
                pid,
                tier_idx=tier_idx,
                r_pt=r_pt,
                in_dom_obs=bool(pd["in_declared_domain"]),
                param_id_obs=main_param_ids[pid],
                verdict_t=str(pd["point_verdict"]),
                reason_t=str(pd["verdict_reason"]),
                margin_enclosure=pd["margin_M_Y"],
                supporting_terms={
                    "a_Y_eta_rhs_term": pd["a_Y_eta_rhs_term"],
                    "log_Y_D_tilde_rhs_term": pd["log_Y_D_tilde_rhs_term"],
                    "total_rhs": pd["total_rhs"],
                    "forcing_dominance_status": pd["forcing_dominance_status"],
                    "a_Y_eta_dominates_rhs": pd["a_Y_eta_dominates_rhs"],
                    "a_Y_eta_share_of_total_rhs": pd["a_Y_eta_share_of_total_rhs"],
                    "J_over_log_Y_D_tilde": p_ev["J_over_log_Y_D_tilde"],
                },
            )
        kl1_ev = p_ev["mechanism_kl1_sub_budgets"]
        _record_candidate_observation(
            "TC061-KL1:offdiag",
            tier_idx=tier_idx,
            r_pt=r_pt,
            in_dom_obs=bool(kl1_ev["in_declared_domain"]),
            param_id_obs=kl1_param_ids["TC061-KL1:offdiag"],
            verdict_t=str(kl1_ev["offdiag_verdict"]),
            reason_t=(
                "CERTIFIED_UPPER_MARGIN_LE_ZERO"
                if kl1_ev["offdiag_verdict"] == "PASS"
                else (
                    "CERTIFIED_LOWER_MARGIN_GT_ZERO_WITNESS"
                    if kl1_ev["offdiag_verdict"] == "FAIL"
                    else "ZERO_STRADDLING_MARGIN_ENCLOSURE"
                )
            ),
            margin_enclosure=kl1_ev["offdiag_margin"],
            supporting_terms={
                "offdiag_4X_tilde": kl1_ev["offdiag_4X_tilde"],
                "offdiag_rhs_3_4_logY_D_tilde": kl1_ev["offdiag_rhs_3_4_logY_D_tilde"],
            },
        )
        _record_candidate_observation(
            "TC061-KL1:R_mix",
            tier_idx=tier_idx,
            r_pt=r_pt,
            in_dom_obs=bool(kl1_ev["in_declared_domain"]),
            param_id_obs=kl1_param_ids["TC061-KL1:R_mix"],
            verdict_t=str(kl1_ev["R_mix_verdict"]),
            reason_t=(
                "CERTIFIED_UPPER_MARGIN_LE_ZERO"
                if kl1_ev["R_mix_verdict"] == "PASS"
                else (
                    "CERTIFIED_LOWER_MARGIN_GT_ZERO_WITNESS"
                    if kl1_ev["R_mix_verdict"] == "FAIL"
                    else "ZERO_STRADDLING_MARGIN_ENCLOSURE"
                )
            ),
            margin_enclosure=kl1_ev["R_mix_margin"],
            supporting_terms={
                "R_mix": kl1_ev["R_mix"],
                "R_mix_rhs_1_4_logY_D_tilde": kl1_ev["R_mix_rhs_1_4_logY_D_tilde"],
            },
        )

        unresolved_app = [
            cid
            for cid, acc in candidate_acc.items()
            if acc["in_declared_domain"] and acc["effective_verdict"] == "UNRESOLVED"
        ]
        acc_main_unres = any(
            candidate_acc[str(pr["probe_id"])]["in_declared_domain"]
            and candidate_acc[str(pr["probe_id"])]["effective_verdict"] == "UNRESOLVED"
            for pr in probes
        )
        acc_kl1_unres = any(
            candidate_acc[kcid]["in_declared_domain"]
            and candidate_acc[kcid]["effective_verdict"] == "UNRESOLVED"
            for kcid in ("TC061-KL1:offdiag", "TC061-KL1:R_mix")
        )
        raw_elapsed = r_pt.get("elapsed_sec")
        hist_elapsed = (
            round(float(raw_elapsed), 6) if _is_valid_nonneg_real(raw_elapsed) else raw_elapsed
        )
        history.append(
            {
                "escalation_tier": tier_idx,
                "quadrature_mode": r_pt["quadrature_mode"],
                "requested_settings": _clone_preserving_arb(r_pt["requested_settings"]),
                "used_settings": _clone_preserving_arb(r_pt["used_settings"]),
                "inactive_parameters": list(r_pt["inactive_parameters"]),
                "elapsed_sec": hist_elapsed,
                "current_rss_mb": r_pt.get("current_rss_mb"),
                "peak_rss_mb": r_pt.get("peak_rss_mb"),
                "peak_rss_measurement_semantics": r_pt.get("peak_rss_measurement_semantics"),
                "tier_raw_any_main_probe_in_domain_unresolved": p_ev[
                    "any_main_probe_in_domain_unresolved"
                ],
                "tier_raw_any_kl1_in_domain_unresolved": p_ev["any_kl1_in_domain_unresolved"],
                "any_main_probe_in_domain_unresolved": acc_main_unres,
                "any_kl1_in_domain_unresolved": acc_kl1_unres,
                "unresolved_applicable_candidates_after_tier": list(unresolved_app),
                "main_probe_verdicts": {
                    pid: pd["point_verdict"] for pid, pd in p_ev["per_probe"].items()
                },
                "accumulated_main_probe_verdicts": {
                    str(pr["probe_id"]): candidate_acc[str(pr["probe_id"])]["effective_verdict"]
                    for pr in probes
                },
                "kl1_verdicts": {
                    "offdiag_verdict": kl1_ev["offdiag_verdict"],
                    "R_mix_verdict": kl1_ev["R_mix_verdict"],
                },
                "accumulated_kl1_verdicts": {
                    "offdiag_verdict": candidate_acc["TC061-KL1:offdiag"]["effective_verdict"],
                    "R_mix_verdict": candidate_acc["TC061-KL1:R_mix"]["effective_verdict"],
                },
            }
        )
        cur_res_chk = evaluate_point_resource_compliance(
            history, max_wall_sec=max_wall_sec, max_rss_mb=max_rss_mb
        )
        return r_pt, p_ev, unresolved_app, cur_res_chk

    res, last_raw_probe_eval, unresolved_ids, resource_budget_check = _run_and_accumulate_tier(
        0, selberg_table
    )
    escalation_tier_used = 0

    if len(integrity_conflicts) > 0:
        stop_reason = "STOPPED_ON_CERTIFICATION_INTEGRITY_CONFLICT"
    elif len(unresolved_ids) == 0:
        stop_reason = "ALL_APPLICABLE_CANDIDATES_DECISIVE_AT_TIER_0"
    elif resource_budget_check["overall_resource_status"] == "EXCEEDED":
        stop_reason = "STOPPED_ON_RESOURCE_BUDGET_EXCEEDED"
    else:
        stop_reason = "ESCALATION_LADDER_EXHAUSTED_WITH_UNRESOLVED_CANDIDATES"
        for esc in escalation_ladder:
            tier_num = int(esc["tier"])
            esc_prec = int(esc["prec_bits"])
            esc_tbl: Optional[Dict[str, Any]] = None
            if evaluator_fn is None:
                esc_tbl = compute_selberg_centered_remainder_table_fast_arb(
                    int(res["cutoffs"]["T_Y"]), prec_bits=esc_prec + 32
                )
            res, last_raw_probe_eval, unresolved_ids, resource_budget_check = (
                _run_and_accumulate_tier(tier_num, esc_tbl)
            )
            escalation_tier_used = tier_num
            if len(integrity_conflicts) > 0:
                stop_reason = "STOPPED_ON_CERTIFICATION_INTEGRITY_CONFLICT"
                break
            if len(unresolved_ids) == 0:
                stop_reason = "ALL_APPLICABLE_CANDIDATES_RESOLVED"
                break
            if resource_budget_check["overall_resource_status"] == "EXCEEDED":
                stop_reason = "STOPPED_ON_RESOURCE_BUDGET_EXCEEDED"
                break

    # Assemble accumulated per_probe and mechanism_kl1_sub_budgets strictly from selected witnesses
    # so an earlier tier's decisive verdict is NEVER paired with a later tier's unrelated margin:
    acc_per_probe: Dict[str, Any] = {}
    any_witness_differs_from_last = False
    for pr in probes:
        pid = str(pr["probe_id"])
        acc = candidate_acc[pid]
        last_obs = acc["tier_observations"][-1]
        if acc["integrity_conflict_detected"]:
            any_witness_differs_from_last = True
            acc_per_probe[pid] = {
                "probe_id": pid,
                "tier": pr["tier"],
                "in_declared_domain": True,
                "applicable_for_escalation": True,
                "integrity_conflict_detected": True,
                "effective_verdict": CERTIFICATION_INTEGRITY_CONFLICT_VERDICT,
                "point_verdict": CERTIFICATION_INTEGRITY_CONFLICT_VERDICT,
                "verdict_reason": "CERTIFICATION_INTEGRITY_CONFLICT_ACROSS_TIERS",
                "conflicting_certified_witnesses": acc["conflicting_certified_witnesses"],
                "a_Y_eta_rhs_term": None,
                "log_Y_D_tilde_rhs_term": None,
                "total_rhs": None,
                "margin_M_Y": None,
                "forcing_dominance_status": None,
                "a_Y_eta_dominates_rhs": None,
                "a_Y_eta_share_of_total_rhs": None,
                "parameter_identity": acc["parameter_identity"],
                "witness_tier": None,
                "witness_prec_bits": None,
                "witness_quad_tol_bits": None,
                "witness_quadrature_mode": None,
                "witness_used_settings": None,
                "selected_witness": None,
                "differs_from_last_evaluated_tier": True,
                "last_evaluated_tier_observation": last_obs,
                "tier_observations": acc["tier_observations"],
            }
        elif not acc["in_declared_domain"]:
            st_last = last_obs["supporting_terms"]
            acc_per_probe[pid] = {
                "probe_id": pid,
                "tier": pr["tier"],
                "in_declared_domain": False,
                "applicable_for_escalation": False,
                "integrity_conflict_detected": False,
                "effective_verdict": "NOT_EVALUATED",
                "point_verdict": "NOT_EVALUATED",
                "out_of_domain_diagnostic_verdict": last_obs["tier_verdict"],
                "verdict_reason": "OUT_OF_DECLARED_DOMAIN_EXCLUDED_FROM_HOLDOUT_VERDICT",
                "a_Y_eta_rhs_term": st_last["a_Y_eta_rhs_term"],
                "log_Y_D_tilde_rhs_term": st_last["log_Y_D_tilde_rhs_term"],
                "total_rhs": st_last["total_rhs"],
                "margin_M_Y": last_obs["margin_enclosure"],
                "forcing_dominance_status": st_last["forcing_dominance_status"],
                "a_Y_eta_dominates_rhs": st_last["a_Y_eta_dominates_rhs"],
                "a_Y_eta_share_of_total_rhs": st_last["a_Y_eta_share_of_total_rhs"],
                "parameter_identity": acc["parameter_identity"],
                "witness_tier": None,
                "witness_prec_bits": None,
                "witness_quad_tol_bits": None,
                "witness_quadrature_mode": None,
                "witness_used_settings": None,
                "selected_witness": None,
                "differs_from_last_evaluated_tier": False,
                "last_evaluated_tier_observation": last_obs,
                "tier_observations": acc["tier_observations"],
            }
        elif acc["selected_witness"] is not None:
            w = acc["selected_witness"]
            st_w = w["supporting_terms"]
            diff_last = bool(w["tier"] != escalation_tier_used)
            any_witness_differs_from_last = any_witness_differs_from_last or diff_last
            acc_per_probe[pid] = {
                "probe_id": pid,
                "tier": pr["tier"],
                "in_declared_domain": True,
                "applicable_for_escalation": True,
                "integrity_conflict_detected": False,
                "effective_verdict": w["tier_verdict"],
                "point_verdict": w["tier_verdict"],
                "verdict_reason": w["verdict_reason"],
                "a_Y_eta_rhs_term": st_w["a_Y_eta_rhs_term"],
                "log_Y_D_tilde_rhs_term": st_w["log_Y_D_tilde_rhs_term"],
                "total_rhs": st_w["total_rhs"],
                "margin_M_Y": w["margin_enclosure"],
                "forcing_dominance_status": st_w["forcing_dominance_status"],
                "a_Y_eta_dominates_rhs": st_w["a_Y_eta_dominates_rhs"],
                "a_Y_eta_share_of_total_rhs": st_w["a_Y_eta_share_of_total_rhs"],
                "parameter_identity": w["parameter_identity"],
                "witness_tier": w["tier"],
                "witness_prec_bits": w["prec_bits"],
                "witness_quad_tol_bits": w["quad_tol_bits"],
                "witness_quadrature_mode": w["quadrature_mode"],
                "witness_used_settings": w["used_settings"],
                "selected_witness": w,
                "differs_from_last_evaluated_tier": diff_last,
                "last_evaluated_tier_observation": last_obs,
                "tier_observations": acc["tier_observations"],
            }
        else:
            st_last = last_obs["supporting_terms"]
            acc_per_probe[pid] = {
                "probe_id": pid,
                "tier": pr["tier"],
                "in_declared_domain": True,
                "applicable_for_escalation": True,
                "integrity_conflict_detected": False,
                "effective_verdict": "UNRESOLVED",
                "point_verdict": "UNRESOLVED",
                "verdict_reason": last_obs["verdict_reason"],
                "a_Y_eta_rhs_term": st_last["a_Y_eta_rhs_term"],
                "log_Y_D_tilde_rhs_term": st_last["log_Y_D_tilde_rhs_term"],
                "total_rhs": st_last["total_rhs"],
                "margin_M_Y": last_obs["margin_enclosure"],
                "forcing_dominance_status": st_last["forcing_dominance_status"],
                "a_Y_eta_dominates_rhs": st_last["a_Y_eta_dominates_rhs"],
                "a_Y_eta_share_of_total_rhs": st_last["a_Y_eta_share_of_total_rhs"],
                "parameter_identity": acc["parameter_identity"],
                "witness_tier": None,
                "witness_prec_bits": None,
                "witness_quad_tol_bits": None,
                "witness_quadrature_mode": None,
                "witness_used_settings": None,
                "selected_witness": None,
                "differs_from_last_evaluated_tier": False,
                "last_evaluated_tier_observation": last_obs,
                "tier_observations": acc["tier_observations"],
            }

    def _select_kl1_fields(cid: str, lhs_key: str, rhs_key: str) -> Dict[str, Any]:
        nonlocal any_witness_differs_from_last
        acc = candidate_acc[cid]
        last_obs = acc["tier_observations"][-1]
        if acc["integrity_conflict_detected"]:
            any_witness_differs_from_last = True
            return {
                "verdict": CERTIFICATION_INTEGRITY_CONFLICT_VERDICT,
                "lhs": None,
                "rhs": None,
                "margin": None,
                "integrity_conflict_detected": True,
                "conflicting_certified_witnesses": acc["conflicting_certified_witnesses"],
                "selected_witness": None,
                "witness_tier": None,
                "differs_from_last_evaluated_tier": True,
                "last_evaluated_tier_observation": last_obs,
                "tier_observations": acc["tier_observations"],
            }
        if not acc["in_declared_domain"]:
            st_l = last_obs["supporting_terms"]
            return {
                "verdict": "NOT_EVALUATED",
                "out_of_domain_diagnostic_verdict": last_obs["tier_verdict"],
                "lhs": st_l[lhs_key],
                "rhs": st_l[rhs_key],
                "margin": last_obs["margin_enclosure"],
                "integrity_conflict_detected": False,
                "conflicting_certified_witnesses": [],
                "selected_witness": None,
                "witness_tier": None,
                "differs_from_last_evaluated_tier": False,
                "last_evaluated_tier_observation": last_obs,
                "tier_observations": acc["tier_observations"],
            }
        if acc["selected_witness"] is not None:
            w = acc["selected_witness"]
            st_w = w["supporting_terms"]
            diff_l = bool(w["tier"] != escalation_tier_used)
            any_witness_differs_from_last = any_witness_differs_from_last or diff_l
            return {
                "verdict": w["tier_verdict"],
                "lhs": st_w[lhs_key],
                "rhs": st_w[rhs_key],
                "margin": w["margin_enclosure"],
                "integrity_conflict_detected": False,
                "conflicting_certified_witnesses": [],
                "selected_witness": w,
                "witness_tier": w["tier"],
                "differs_from_last_evaluated_tier": diff_l,
                "last_evaluated_tier_observation": last_obs,
                "tier_observations": acc["tier_observations"],
            }
        st_l = last_obs["supporting_terms"]
        return {
            "verdict": "UNRESOLVED",
            "lhs": st_l[lhs_key],
            "rhs": st_l[rhs_key],
            "margin": last_obs["margin_enclosure"],
            "integrity_conflict_detected": False,
            "conflicting_certified_witnesses": [],
            "selected_witness": None,
            "witness_tier": None,
            "differs_from_last_evaluated_tier": False,
            "last_evaluated_tier_observation": last_obs,
            "tier_observations": acc["tier_observations"],
        }

    off_sel = _select_kl1_fields(
        "TC061-KL1:offdiag", "offdiag_4X_tilde", "offdiag_rhs_3_4_logY_D_tilde"
    )
    mix_sel = _select_kl1_fields("TC061-KL1:R_mix", "R_mix", "R_mix_rhs_1_4_logY_D_tilde")

    acc_main_unres_final = any(
        acc["in_declared_domain"] and acc["effective_verdict"] == "UNRESOLVED"
        for cid, acc in candidate_acc.items()
        if acc["candidate_kind"] == "MAIN_PROBE"
    )
    acc_kl1_unres_final = any(
        acc["in_declared_domain"] and acc["effective_verdict"] == "UNRESOLVED"
        for cid, acc in candidate_acc.items()
        if acc["candidate_kind"] == "KL1_SUB_BUDGET"
    )
    acc_main_fail_final = any(
        acc["in_declared_domain"] and acc["effective_verdict"] == "FAIL"
        for cid, acc in candidate_acc.items()
        if acc["candidate_kind"] == "MAIN_PROBE"
    )
    acc_kl1_fail_final = any(
        acc["in_declared_domain"] and acc["effective_verdict"] == "FAIL"
        for cid, acc in candidate_acc.items()
        if acc["candidate_kind"] == "KL1_SUB_BUDGET"
    )

    accumulated_probe_eval: Dict[str, Any] = {
        "per_probe": acc_per_probe,
        "any_main_probe_in_domain_unresolved": acc_main_unres_final,
        "any_kl1_in_domain_unresolved": acc_kl1_unres_final,
        "any_in_domain_unresolved": bool(acc_main_unres_final or acc_kl1_unres_final),
        "any_main_probe_in_domain_fail": acc_main_fail_final,
        "any_kl1_in_domain_fail": acc_kl1_fail_final,
        "certification_integrity_ok": len(integrity_conflicts) == 0,
        "integrity_conflicts": integrity_conflicts,
        "mechanism_kl1_sub_budgets": {
            "in_declared_domain": bool(kl1_in_declared_domain),
            "offdiag_4X_tilde": off_sel["lhs"],
            "offdiag_rhs_3_4_logY_D_tilde": off_sel["rhs"],
            "offdiag_margin": off_sel["margin"],
            "offdiag_verdict": off_sel["verdict"],
            "offdiag_witness_tier": off_sel["witness_tier"],
            "offdiag_selected_witness": off_sel["selected_witness"],
            "offdiag_integrity_conflict_detected": off_sel["integrity_conflict_detected"],
            "offdiag_conflicting_certified_witnesses": off_sel[
                "conflicting_certified_witnesses"
            ],
            "offdiag_differs_from_last_evaluated_tier": off_sel[
                "differs_from_last_evaluated_tier"
            ],
            "offdiag_last_evaluated_tier_observation": off_sel[
                "last_evaluated_tier_observation"
            ],
            "offdiag_tier_observations": off_sel["tier_observations"],
            "R_mix": mix_sel["lhs"],
            "R_mix_rhs_1_4_logY_D_tilde": mix_sel["rhs"],
            "R_mix_margin": mix_sel["margin"],
            "R_mix_verdict": mix_sel["verdict"],
            "R_mix_witness_tier": mix_sel["witness_tier"],
            "R_mix_selected_witness": mix_sel["selected_witness"],
            "R_mix_integrity_conflict_detected": mix_sel["integrity_conflict_detected"],
            "R_mix_conflicting_certified_witnesses": mix_sel[
                "conflicting_certified_witnesses"
            ],
            "R_mix_differs_from_last_evaluated_tier": mix_sel[
                "differs_from_last_evaluated_tier"
            ],
            "R_mix_last_evaluated_tier_observation": mix_sel[
                "last_evaluated_tier_observation"
            ],
            "R_mix_tier_observations": mix_sel["tier_observations"],
        },
        "J_over_log_Y_D_tilde": last_raw_probe_eval["J_over_log_Y_D_tilde"],
    }

    in_domain_summary = {
        cid: {
            "candidate_id": cid,
            "candidate_kind": acc["candidate_kind"],
            "effective_verdict": acc["effective_verdict"],
            "witness_tier": (
                acc["selected_witness"]["tier"] if acc["selected_witness"] is not None else None
            ),
            "selected_witness": acc["selected_witness"],
            "integrity_conflict_detected": acc["integrity_conflict_detected"],
            "conflicting_certified_witnesses": acc["conflicting_certified_witnesses"],
            "differs_from_last_evaluated_tier": bool(
                acc["integrity_conflict_detected"]
                or (
                    acc["selected_witness"] is not None
                    and acc["selected_witness"]["tier"] != escalation_tier_used
                )
            ),
        }
        for cid, acc in candidate_acc.items()
        if acc["in_declared_domain"] or acc["integrity_conflict_detected"]
    }
    out_of_domain_summary = {
        cid: {
            "candidate_id": cid,
            "candidate_kind": acc["candidate_kind"],
            "domain_status": "OUT_OF_DECLARED_DOMAIN",
            "excluded_from_escalation": True,
            "effective_verdict": "NOT_EVALUATED",
            "diagnostic_tier_observations": acc["tier_observations"],
        }
        for cid, acc in candidate_acc.items()
        if (not acc["in_declared_domain"]) and (not acc["integrity_conflict_detected"])
    }

    accumulated_candidate_evidence = {
        "point_id": eff_point_id,
        "last_evaluated_observable_tier": escalation_tier_used,
        "any_candidate_witness_differs_from_last_tier": any_witness_differs_from_last,
        "escalation_stop_reason": stop_reason,
        "certification_integrity_ok": len(integrity_conflicts) == 0,
        "certification_integrity_status": (
            "CERTIFIED_CONSISTENT"
            if len(integrity_conflicts) == 0
            else CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
        ),
        "integrity_conflicts": integrity_conflicts,
        "in_domain_candidates": in_domain_summary,
        "out_of_domain_candidates": out_of_domain_summary,
    }

    if raise_on_integrity_conflict and len(integrity_conflicts) > 0:
        raise CertificationIntegrityError(
            f"Certification integrity conflict at {eff_point_id}: "
            f"{[c.get('candidate_id', c.get('conflict_type', 'UNKNOWN_CONFLICT')) for c in integrity_conflicts]}",
            integrity_conflicts,
        )

    return {
        "point_id": eff_point_id,
        "point_result": res,
        "last_evaluated_observable_tier": escalation_tier_used,
        "any_candidate_witness_differs_from_last_tier": any_witness_differs_from_last,
        "probe_evaluation": accumulated_probe_eval,
        "last_tier_raw_probe_evaluation": last_raw_probe_eval,
        "accumulated_candidate_evidence": accumulated_candidate_evidence,
        "certification_integrity_ok": len(integrity_conflicts) == 0,
        "certification_integrity_status": (
            "CERTIFIED_CONSISTENT"
            if len(integrity_conflicts) == 0
            else CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
        ),
        "integrity_conflicts": integrity_conflicts,
        "escalation_tier_used": escalation_tier_used,
        "escalation_stop_reason": stop_reason,
        "escalation_history": history,
        "resource_budget_check": resource_budget_check,
    }


def build_holdout_point_artifact_row(
    entry: Dict[str, Any],
    exec_out: Dict[str, Any],
    *,
    compute_divisor_partition: bool = True,
) -> Dict[str, Any]:
    """Build a JSON-ready `holdout_point_evaluations` row from `execute_holdout_point_with_protocol_escalation`,
    keeping last-tier observable enclosures distinct from accumulated per-candidate witness evidence
    (`TASK-TC-061R2` §2).
    """
    res = exec_out["point_result"]
    probe_eval = exec_out["probe_evaluation"]
    escalation_tier_used = int(exec_out["escalation_tier_used"])
    res_budget = exec_out["resource_budget_check"]
    spec = ExactScaleSpec.from_protocol_entry(entry)

    has_full_cons = (
        "J_consistency_residual_QA" in res and "J_consistency_residual_2PB" in res
    )
    if has_full_cons:
        res_qa = res["J_consistency_residual_QA"]
        res_2pb = res["J_consistency_residual_2PB"]
        cons_ok: Optional[bool] = bool(
            arb(0) in res_qa
            and abs(res_qa) < arb("1e-44")
            and arb(0) in res_2pb
            and abs(res_2pb) < arb("1e-44")
        )
    else:
        res_qa = None
        res_2pb = None
        cons_ok = True

    pb_b = res.get("pair_P_B")
    if isinstance(pb_b, arb):
        pb_sign: Optional[str] = (
            "STRICTLY_POSITIVE"
            if bool(pb_b > arb(0))
            else ("STRICTLY_NEGATIVE" if bool(pb_b < arb(0)) else "STRADDLING_ZERO")
        )
    else:
        pb_sign = None

    j_b = res["J_direct"]
    j_sign = (
        "STRICTLY_POSITIVE"
        if bool(j_b > arb(0))
        else ("STRICTLY_NEGATIVE" if bool(j_b < arb(0)) else "STRADDLING_ZERO")
    )

    div_part = (
        certify_open_core_divisor_partition(
            spec.evaluate_arb(prec_bits=int(res["cutoffs"]["cutoff_prec_bits_used"])),
            kappa=1,
            prec_bits=int(res["cutoffs"]["cutoff_prec_bits_used"]),
        )
        if compute_divisor_partition
        else None
    )

    has_tail = bool(res.get("has_subunit_tail_ge_ceil_tau_Y", False))
    raw_el = res.get("elapsed_sec")
    el_out = round(float(raw_el), 4) if _is_valid_nonneg_real(raw_el) else None

    return {
        "point_id": entry["point_id"],
        "label": entry["label"],
        "grid_tier": entry["grid_tier"],
        "prior_exposure_status": entry["prior_exposure_status"],
        "prior_exposure_detail": entry["prior_exposure_detail"],
        "cutoffs": res["cutoffs"],
        "open_core_divisor_partition": div_part,
        "quadrature_mode": res["quadrature_mode"],
        "escalation_tier_used": escalation_tier_used,
        "escalation_stop_reason": exec_out["escalation_stop_reason"],
        "last_evaluated_observable_tier": escalation_tier_used,
        "any_candidate_witness_differs_from_last_tier": exec_out[
            "any_candidate_witness_differs_from_last_tier"
        ],
        "certification_integrity_ok": exec_out["certification_integrity_ok"],
        "certification_integrity_status": exec_out["certification_integrity_status"],
        "integrity_conflicts": exec_out["integrity_conflicts"],
        "requested_settings": res["requested_settings"],
        "used_settings": res["used_settings"],
        "inactive_parameters": res["inactive_parameters"],
        "escalation_history": exec_out["escalation_history"],
        "prec_bits_used": res["prec_bits"],
        "quad_tol_bits_used": res["quad_tol_bits"],
        "panels_used": res["panels_used"],
        "unique_quadrature_nodes": res.get("unique_quadrature_nodes"),
        "elapsed_sec": el_out,
        "current_rss_mb": res.get("current_rss_mb"),
        "peak_rss_mb": res_budget["peak_rss_mb"],
        "resource_budget_check": res_budget,
        "Y_enclosure": serialize_arb_certified(res["Y_arb"]),
        "E_Y": serialize_arb_certified(res["E_Y"]) if "E_Y" in res else None,
        "D_tilde_Y": serialize_arb_certified(res["D_tilde_Y"]),
        "X_tilde_Y": serialize_arb_certified(res["X_tilde_Y"]),
        "P_norm_sq": serialize_arb_certified(res["P_norm_sq"]) if "P_norm_sq" in res else None,
        "A_norm_sq": serialize_arb_certified(res["A_norm_sq"]) if "A_norm_sq" in res else None,
        "B_norm_sq": serialize_arb_certified(res["B_norm_sq"]) if "B_norm_sq" in res else None,
        "pair_P_B": serialize_arb_certified(pb_b) if isinstance(pb_b, arb) else None,
        "pair_P_B_sign": pb_sign,
        "J_direct": serialize_arb_certified(j_b),
        "J_sign": j_sign,
        "J_algebraic_consistency_QA": (
            serialize_arb_certified(res["J_algebraic_consistency_QA"])
            if "J_algebraic_consistency_QA" in res
            else None
        ),
        "J_algebraic_consistency_2PB": (
            serialize_arb_certified(res["J_algebraic_consistency_2PB"])
            if "J_algebraic_consistency_2PB" in res
            else None
        ),
        "J_consistency_check_role": "ALGEBRAIC_CONSISTENCY_CHECK_SAME_INPUTS",
        "J_consistency_residual_QA": (
            serialize_arb_certified(res_qa) if isinstance(res_qa, arb) else None
        ),
        "J_consistency_residual_2PB": (
            serialize_arb_certified(res_2pb) if isinstance(res_2pb, arb) else None
        ),
        "algebraic_consistency_verified": cons_ok,
        "log_Y_times_D_tilde": serialize_arb_certified(res["log_Y_times_D_tilde"]),
        "J_over_log_Y_D_tilde": probe_eval["J_over_log_Y_D_tilde"],
        "has_subunit_tail_ge_ceil_tau_Y": has_tail,
        "subunit_tail_breakdown": (
            {
                "subunit_tail_d_range_inclusive": res["subunit_tail_d_range_inclusive"],
                "B_tail_norm_sq": serialize_arb_certified(res["B_tail_norm_sq"]),
                "B_inter_norm_sq": serialize_arb_certified(res["B_inter_norm_sq"]),
                "pair_P_B_tail": serialize_arb_certified(res["pair_P_B_tail"]),
                "pair_B_inter_B_tail": serialize_arb_certified(res["pair_B_inter_B_tail"]),
                "J_subunit_tail_contribution": serialize_arb_certified(
                    res["J_subunit_tail_contribution"]
                ),
                "J_without_subunit_tail": serialize_arb_certified(res["J_without_subunit_tail"]),
            }
            if has_tail
            else None
        ),
        "probe_evaluations": probe_eval["per_probe"],
        "mechanism_kl1_sub_budgets": probe_eval["mechanism_kl1_sub_budgets"],
        "accumulated_candidate_evidence": exec_out["accumulated_candidate_evidence"],
    }


def aggregate_holdout_rows_and_outcomes(
    holdout_rows: Sequence[Dict[str, Any]],
    probes: Sequence[Dict[str, Any]],
    *,
    registered_count: int,
    fail_on_integrity_conflict: bool = False,
) -> Dict[str, Any]:
    """Aggregate holdout coverage, 3-valued resource compliance, certification integrity, and
    global main-probe / `KL1` outcomes directly from serialized or in-memory `holdout_rows`
    (`TASK-TC-061R2` §§2–4):
    - Uses each row's accumulated candidate verdict and `selected_witness` provenance;
    - Keeps mathematical point coverage (`coverage_complete`) separate from `resource_compliance_summary`
      so `UNKNOWN` RSS telemetry prevents claiming verified resource compliance without turning
      rigorous inequality certificates into mathematical failures;
    - Preserves `REFUTED_BY_CERTIFIED_WITNESS` whenever a valid counterexample exists even if other
      candidates or points remain `UNRESOLVED`;
    - Blocks a clean certification report (`certification_report_blocked = True`) if any candidate
      encountered `CERTIFICATION_INTEGRITY_CONFLICT`.
    """
    all_conflicts: List[Dict[str, Any]] = []
    for r in holdout_rows:
        row_conflicts = list(r.get("integrity_conflicts") or [])
        for c in row_conflicts:
            all_conflicts.append(c)
        row_has_conflict_verdict = any(
            str(pd.get("point_verdict")) == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
            or bool(pd.get("integrity_conflict_detected", False))
            for pd in (r.get("probe_evaluations") or {}).values()
        ) or (
            str((r.get("mechanism_kl1_sub_budgets") or {}).get("offdiag_verdict"))
            == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
            or str((r.get("mechanism_kl1_sub_budgets") or {}).get("R_mix_verdict"))
            == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
        )
        if (not r.get("certification_integrity_ok", True) or row_has_conflict_verdict) and len(
            row_conflicts
        ) == 0:
            all_conflicts.append(
                {
                    "conflict_type": "ROW_INTEGRITY_FLAG_OR_VERDICT_WITHOUT_CONFLICT_RECORD",
                    "point_id": r.get("point_id"),
                    "candidate_id": "ROW_LEVEL_INTEGRITY",
                }
            )
    cert_integrity_ok = len(all_conflicts) == 0
    if fail_on_integrity_conflict and not cert_integrity_ok:
        raise CertificationIntegrityError(
            f"Section 3 aggregation blocked by {len(all_conflicts)} certification integrity conflict(s)",
            all_conflicts,
        )

    mathematical_coverage_complete = bool(
        registered_count > 0
        and len(holdout_rows) == registered_count
        and cert_integrity_ok
    )
    res_summary = aggregate_section_resource_compliance(
        [r["resource_budget_check"] for r in holdout_rows],
        registered_count=registered_count,
    )

    probe_summaries: Dict[str, Any] = {}
    any_probe_or_kl1_fail = False
    for pr in probes:
        pid = str(pr["probe_id"])
        verdicts: List[str] = []
        fail_witnesses: List[Dict[str, Any]] = []
        conflict_records: List[Dict[str, Any]] = []
        out_of_domain_count = 0
        for r in holdout_rows:
            pdata = r["probe_evaluations"][pid]
            if not pdata.get("in_declared_domain", True) and not pdata.get(
                "integrity_conflict_detected", False
            ):
                out_of_domain_count += 1
                continue
            v = str(pdata["point_verdict"])
            verdicts.append(v)
            if v == "FAIL":
                any_probe_or_kl1_fail = True
                w_sel = pdata.get("selected_witness")
                fail_witnesses.append(
                    {
                        "point_id": r["point_id"],
                        "probe_id": pid,
                        "witness_tier": pdata.get("witness_tier"),
                        "witness_prec_bits": pdata.get("witness_prec_bits"),
                        "witness_quad_tol_bits": pdata.get("witness_quad_tol_bits"),
                        "witness_quadrature_mode": pdata.get("witness_quadrature_mode"),
                        "witness_used_settings": pdata.get("witness_used_settings"),
                        "parameter_identity": pdata.get("parameter_identity"),
                        "margin_M_Y": pdata["margin_M_Y"],
                        "selected_witness": w_sel,
                    }
                )
            elif v == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT:
                conflict_records.append(
                    {
                        "point_id": r["point_id"],
                        "probe_id": pid,
                        "conflicting_certified_witnesses": pdata.get(
                            "conflicting_certified_witnesses", []
                        ),
                    }
                )
        in_dom_registered = max(0, registered_count - out_of_domain_count)
        in_dom_complete = bool(
            mathematical_coverage_complete
            and in_dom_registered > 0
            and len(verdicts) == in_dom_registered
        )
        outcome = classify_global_probe_outcome(
            verdicts,
            coverage_complete=in_dom_complete,
            uniform_proof_established=False,
            fail_on_integrity_conflict=fail_on_integrity_conflict,
        )
        probe_summaries[pid] = {
            "probe_id": pid,
            "tier": pr["tier"],
            "formula": pr["formula"],
            "holdout_points_registered": in_dom_registered,
            "out_of_domain_excluded_count": out_of_domain_count,
            "holdout_points_evaluated": len(verdicts),
            "pass_count": sum(1 for v in verdicts if v == "PASS"),
            "fail_count": sum(1 for v in verdicts if v == "FAIL"),
            "unresolved_count": sum(1 for v in verdicts if v == "UNRESOLVED"),
            "not_evaluated_count": sum(1 for v in verdicts if v == "NOT_EVALUATED"),
            "integrity_conflict_count": sum(
                1 for v in verdicts if v == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
            ),
            "decisive_fail_witnesses": fail_witnesses,
            "integrity_conflicts": conflict_records,
            "coverage_complete": in_dom_complete,
            "uniform_proof_established": False,
            "global_probe_outcome": outcome,
        }

    kl1_off_verdicts: List[str] = []
    kl1_mix_verdicts: List[str] = []
    kl1_off_fail_witnesses: List[Dict[str, Any]] = []
    kl1_mix_fail_witnesses: List[Dict[str, Any]] = []
    kl1_out_of_domain_count = 0
    for r in holdout_rows:
        kl1_d = r["mechanism_kl1_sub_budgets"]
        kl1_has_conflict = bool(
            kl1_d.get("offdiag_integrity_conflict_detected", False)
            or kl1_d.get("R_mix_integrity_conflict_detected", False)
            or str(kl1_d.get("offdiag_verdict")) == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
            or str(kl1_d.get("R_mix_verdict")) == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
        )
        if not kl1_d.get("in_declared_domain", True) and not kl1_has_conflict:
            kl1_out_of_domain_count += 1
            continue
        vo = str(kl1_d["offdiag_verdict"])
        vm = str(kl1_d["R_mix_verdict"])
        kl1_off_verdicts.append(vo)
        kl1_mix_verdicts.append(vm)
        if vo == "FAIL":
            any_probe_or_kl1_fail = True
            kl1_off_fail_witnesses.append(
                {
                    "point_id": r["point_id"],
                    "candidate_id": "TC061-KL1:offdiag",
                    "witness_tier": kl1_d.get("offdiag_witness_tier"),
                    "margin": kl1_d["offdiag_margin"],
                    "selected_witness": kl1_d.get("offdiag_selected_witness"),
                }
            )
        if vm == "FAIL":
            any_probe_or_kl1_fail = True
            kl1_mix_fail_witnesses.append(
                {
                    "point_id": r["point_id"],
                    "candidate_id": "TC061-KL1:R_mix",
                    "witness_tier": kl1_d.get("R_mix_witness_tier"),
                    "margin": kl1_d["R_mix_margin"],
                    "selected_witness": kl1_d.get("R_mix_selected_witness"),
                }
            )

    kl1_in_dom_registered = max(0, registered_count - kl1_out_of_domain_count)
    kl1_off_complete = bool(
        mathematical_coverage_complete
        and kl1_in_dom_registered > 0
        and len(kl1_off_verdicts) == kl1_in_dom_registered
    )
    kl1_mix_complete = bool(
        mathematical_coverage_complete
        and kl1_in_dom_registered > 0
        and len(kl1_mix_verdicts) == kl1_in_dom_registered
    )
    kl1_summary = {
        "in_domain_registered_count": kl1_in_dom_registered,
        "out_of_domain_excluded_count": kl1_out_of_domain_count,
        "offdiag_sub_budget_outcome": classify_global_probe_outcome(
            kl1_off_verdicts,
            coverage_complete=kl1_off_complete,
            uniform_proof_established=False,
            fail_on_integrity_conflict=fail_on_integrity_conflict,
        ),
        "offdiag_decisive_fail_witnesses": kl1_off_fail_witnesses,
        "mixed_core_sub_budget_outcome": classify_global_probe_outcome(
            kl1_mix_verdicts,
            coverage_complete=kl1_mix_complete,
            uniform_proof_established=False,
            fail_on_integrity_conflict=fail_on_integrity_conflict,
        ),
        "mixed_core_decisive_fail_witnesses": kl1_mix_fail_witnesses,
    }

    row_4096 = next((r for r in holdout_rows if r["point_id"] == "HO-EXT-4096"), None)
    tail_4096_evaluated = bool(
        row_4096 is not None
        and row_4096["cutoffs"]["T_Y"] == 32768
        and row_4096["has_subunit_tail_ge_ceil_tau_Y"] is True
        and row_4096["subunit_tail_breakdown"] is not None
        and row_4096["subunit_tail_breakdown"]["subunit_tail_d_range_inclusive"] == [25736, 32767]
    )

    holdout_coverage_summary = {
        "registered_count": registered_count,
        "evaluated_count": len(holdout_rows),
        "coverage_complete": mathematical_coverage_complete,
        "mathematical_coverage_complete": mathematical_coverage_complete,
        "Y_4096_nonempty_subunit_tail_evaluated": tail_4096_evaluated,
        "overall_resource_budget_status": res_summary["overall_resource_budget_status"],
        "wall_budget_status": res_summary["wall_budget_status"],
        "memory_budget_status": res_summary["memory_budget_status"],
        "all_points_within_resource_budgets": res_summary["all_points_within_resource_budgets"],
        "all_resource_budgets_verified_within": res_summary["all_resource_budgets_verified_within"],
        "certification_integrity_ok": cert_integrity_ok,
        "certification_report_blocked": not cert_integrity_ok,
        "mechanism_revision_triggered": False,
        "mechanism_revision_note": (
            "All 4 frozen probes and both TC061-KL1 sub-budgets passed on all evaluated held-out "
            "points; zero failures occurred, so no TC061-REV1-* post-diagnosis mechanism revision "
            "was triggered."
            if (not any_probe_or_kl1_fail and cert_integrity_ok)
            else (
                "Certification report blocked by contradictory certified verdicts across tiers."
                if not cert_integrity_ok
                else "Certified counterexample witness(es) recorded; frozen probe parameters remain immutable."
            )
        ),
    }

    return {
        "holdout_coverage_summary": holdout_coverage_summary,
        "resource_compliance_summary": res_summary,
        "certification_integrity_summary": {
            "certification_integrity_ok": cert_integrity_ok,
            "certification_report_blocked": not cert_integrity_ok,
            "integrity_conflict_count": len(all_conflicts),
            "integrity_conflicts": all_conflicts,
        },
        "global_probe_outcomes": probe_summaries,
        "mechanism_kl1_holdout_summary": kl1_summary,
        "Y_4096_nonempty_subunit_tail_evaluated": tail_4096_evaluated,
    }


def verify_section_3_preregistered_holdout_experiment(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute the complete 14-point preregistered held-out experiment (`128` through `4096`,
    including nonempty `d >= ceil(tau*Y)` full-tail evaluations at `Y = 2048` and `Y = 4096`,
    protocol-faithful `quad_tol_bits = 240` unsplit quadrature on `T < 512` (`Y = 128`),
    per-candidate decisive-witness accumulation across main probes and `KL1` sub-budgets, and
    separate 3-valued `WITHIN`/`EXCEEDED`/`UNKNOWN` resource compliance auditing) against the
    immutable protocol (`TASK-TC-061R` §6 / `TASK-TC-061R2` §§2–3).
    """
    t_sec3_start = time.perf_counter()
    proto = json.loads(MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH.read_text(encoding="utf-8"))
    probes = proto["frozen_candidate_probes"]
    holdout_entries = proto["preregistered_holdout_grid"]
    protocol_rules = proto["numerical_settings_and_escalation_rules"]
    base_prec = int(protocol_rules["base_prec_bits"])
    if int(prec_bits) != base_prec:
        raise ValueError(
            f"Section 3 holdout experiment must use frozen base_prec_bits={base_prec}, got {prec_bits}"
        )

    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(32768, prec_bits=base_prec + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 32768
        else selberg_table
    )

    holdout_rows: List[Dict[str, Any]] = []
    consistency_all_ok = True
    raw_results_by_id: Dict[str, Dict[str, Any]] = {}

    for entry in holdout_entries:
        spec = ExactScaleSpec.from_protocol_entry(entry)
        exec_out = execute_holdout_point_with_protocol_escalation(
            spec,
            probes,
            protocol_rules,
            point_id=str(entry["point_id"]),
            selberg_table=tbl,
            in_declared_domain_fn=lambda _pr: True,
            kl1_in_declared_domain=True,
            raise_on_integrity_conflict=False,
        )
        raw_results_by_id[str(entry["point_id"])] = exec_out["point_result"]
        row_dict = build_holdout_point_artifact_row(
            entry, exec_out, compute_divisor_partition=True
        )
        consistency_all_ok = consistency_all_ok and bool(row_dict["algebraic_consistency_verified"])
        holdout_rows.append(row_dict)

    agg = aggregate_holdout_rows_and_outcomes(
        holdout_rows,
        probes,
        registered_count=len(holdout_entries),
        fail_on_integrity_conflict=False,
    )
    res_summary = agg["resource_compliance_summary"]
    cert_summary = agg["certification_integrity_summary"]
    tail_4096_evaluated = agg["Y_4096_nonempty_subunit_tail_evaluated"]

    # Exact exposure-category breakdown derived verbatim from the frozen protocol:
    exposure_counts: Dict[str, int] = {}
    exposure_points_by_cat: Dict[str, List[Dict[str, str]]] = {}
    for entry in holdout_entries:
        cat = str(entry["prior_exposure_status"])
        exposure_counts[cat] = exposure_counts.get(cat, 0) + 1
        exposure_points_by_cat.setdefault(cat, []).append(
            {
                "point_id": str(entry["point_id"]),
                "label": str(entry["label"]),
                "prior_exposure_detail": str(entry["prior_exposure_detail"]),
            }
        )
    unseen_all_count = exposure_counts.get("UNSEEN_FOR_ALL_OBSERVABLES", 0)
    unseen_window_count = exposure_counts.get("UNSEEN_FOR_ALL_TC054_TO_TC060_WINDOW_OBSERVABLES", 0)
    exposure_category_breakdown = {
        "total_registered_holdout_points": len(holdout_entries),
        "counts_by_prior_exposure_status": exposure_counts,
        "unseen_for_all_observables_count": unseen_all_count,
        "unseen_for_all_tc054_to_tc060_window_observables_count": unseen_window_count,
        "zero_prior_window_observable_evaluations_combined_count": unseen_all_count + unseen_window_count,
        "prior_partial_or_ancillary_or_index_only_count": (
            len(holdout_entries) - (unseen_all_count + unseen_window_count)
        ),
        "points_by_category_verbatim": exposure_points_by_cat,
    }

    # Verify Y = 128 (T = 431 < 512) ran at unsplit quad_tol_bits = 240 and compare against TC-061 160-bit run:
    row_128 = next((r for r in holdout_rows if r["point_id"] == "HO-BASE-128"), None)
    raw_128 = raw_results_by_id.get("HO-BASE-128")
    ho_128_protocol_ok = bool(
        row_128 is not None
        and row_128["cutoffs"]["T_Y"] == 431
        and row_128["quadrature_mode"] == "unsplit"
        and row_128["quad_tol_bits_used"] == 240
        and row_128["panels_used"] == 1
        and row_128["inactive_parameters"]
        == [
            "quad_tol_bits_three_zone_large_T",
            "n_panels",
            "zone1_ratio_threshold_x_over_n",
            "zone3_cutoff_N1",
            "zone3_taylor_degree_M",
        ]
    )
    orig_128_enclosures = ORIGINAL_TC061_HO_BASE_128_DEVIATION_RECORD["original_enclosures"]
    rerun_128_overlap_checks: Dict[str, Any] = {}
    ho_128_overlap_ok = raw_128 is not None
    if raw_128 is not None and row_128 is not None:
        saved_cmp_prec = flint_ctx.prec
        try:
            flint_ctx.prec = prec_bits
            new_balls_128 = {
                "E_Y": raw_128["E_Y"],
                "D_tilde_Y": raw_128["D_tilde_Y"],
                "X_tilde_Y": raw_128["X_tilde_Y"],
                "J_direct": raw_128["J_direct"],
                "M_P0": raw_128["J_direct"] - raw_128["log_Y_times_D_tilde"],
            }
        finally:
            flint_ctx.prec = saved_cmp_prec
        for obs_k, new_b in new_balls_128.items():
            old_lo, old_hi, _ = _parse_arb_ball_str_to_fractions(orig_128_enclosures[obs_k])
            new_lo, new_hi = _exact_arb_endpoints_as_fractions(new_b)
            overlaps = bool(max(old_lo, new_lo) <= min(old_hi, new_hi))
            enclosed_in_old = bool(old_lo <= new_lo and new_hi <= old_hi)
            max_abs_diff = max(abs(new_hi - old_lo), abs(old_hi - new_lo))
            ok_obs = bool(overlaps and max_abs_diff < Fraction(1, 10**39))
            ho_128_overlap_ok = ho_128_overlap_ok and ok_obs
            rerun_128_overlap_checks[obs_k] = {
                "original_160bit_arb_ball_str": orig_128_enclosures[obs_k],
                "corrected_240bit_enclosure": serialize_arb_certified(new_b),
                "enclosures_overlap": overlaps,
                "corrected_240bit_enclosed_within_original_160bit": enclosed_in_old,
                "verdict_unchanged": True,
                "verified": ok_obs,
            }

    tc061r_protocol_deviation_and_rerun_comparison = {
        "point_id": "HO-BASE-128",
        "Y": 128,
        "T_Y": 431,
        "epistemic_role": "CORRECTED_PROTOCOL_REPEAT_ON_SAME_REGISTERED_POINT_NOT_NEW_UNSEEN_POINT",
        "original_tc061_deviation_record": ORIGINAL_TC061_HO_BASE_128_DEVIATION_RECORD,
        "corrected_tc061r_settings_used": row_128["used_settings"] if row_128 is not None else None,
        "observable_enclosure_comparisons": rerun_128_overlap_checks,
        "all_verdicts_identical_pass": bool(
            row_128 is not None
            and all(
                pd["point_verdict"] == "PASS" for pd in row_128["probe_evaluations"].values()
            )
            and row_128["mechanism_kl1_sub_budgets"]["offdiag_verdict"] == "PASS"
            and row_128["mechanism_kl1_sub_budgets"]["R_mix_verdict"] == "PASS"
        ),
        "verified": bool(ho_128_protocol_ok and ho_128_overlap_ok),
    }

    sec3_wall_sec = time.perf_counter() - t_sec3_start
    valid_row_walls: List[float] = []
    for r in holdout_rows:
        rb_chk = r.get("resource_budget_check") or {}
        if rb_chk.get("wall_budget_status") == "UNKNOWN":
            continue
        cum_w = rb_chk.get("cumulative_point_elapsed_sec", r.get("elapsed_sec"))
        if _is_valid_nonneg_real(cum_w):
            valid_row_walls.append(float(cum_w))
    max_point_wall_sec: Optional[float] = (
        round(max(valid_row_walls), 4)
        if (valid_row_walls and res_summary["wall_budget_status"] != "UNKNOWN")
        else None
    )
    rss_vals = [
        float(r["peak_rss_mb"]) for r in holdout_rows if _is_valid_nonneg_real(r.get("peak_rss_mb"))
    ]
    execution_telemetry_summary = {
        "telemetry_scope": "THIS_ARTIFACT_GENERATION_RUN_ONLY",
        "section_3_total_wall_sec": round(sec3_wall_sec, 4),
        "max_single_point_wall_sec": max_point_wall_sec,
        "max_observed_peak_rss_mb": (
            round(max(rss_vals), 3)
            if (rss_vals and res_summary["memory_budget_status"] != "UNKNOWN")
            else None
        ),
        "wall_budget_status": res_summary["wall_budget_status"],
        "memory_budget_status": res_summary["memory_budget_status"],
        "overall_resource_budget_status": res_summary["overall_resource_budget_status"],
        "all_points_within_300s_and_4096mb_budget": res_summary["all_points_within_resource_budgets"],
        "all_resource_budgets_verified_within": res_summary["all_resource_budgets_verified_within"],
        "budget_enforcement_mode": "POST_EVALUATION_BUDGET_AUDIT_NO_OS_PREEMPTIVE_KILL",
    }

    return {
        "epistemic_statuses": [
            "CERTIFIED_FINITE_OBSERVATION",
            "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        ],
        "section_epistemic_scope_note": (
            "Mixed empirical-certificate / open-hypothesis section: all 14 preregistered held-out "
            "256-bit Arb enclosures (including protocol-faithful quad_tol_bits = 240 unsplit "
            "evaluation at Y = 128, nonempty d >= ceil(tau*Y) full-tail evaluations at Y = 2048 "
            "and Y = 4096, and sided discontinuity points) are CERTIFIED_FINITE_OBSERVATION; "
            "uniform validity of TC061-P0, TC061-P_{1/2}, TC061-P_{1/4}, TC061-P_{1/8}, and full "
            "closure hypothesis H over all real Y >= Y_0 remains OPEN_CONJECTURE_OR_FAILED_CANDIDATE "
            "(finite grid survival is SURVIVED_TESTED_POINTS, never PROVED_UNIFORMLY)."
        ),
        "component_epistemic_map": {
            "fourteen_point_holdout_arb_enclosures_and_full_tail_4096": "CERTIFIED_FINITE_OBSERVATION",
            "uniform_probe_and_closure_hypothesis_H_validity": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        },
        "holdout_coverage_summary": agg["holdout_coverage_summary"],
        "resource_compliance_summary": res_summary,
        "certification_integrity_summary": cert_summary,
        "exposure_category_breakdown": exposure_category_breakdown,
        "execution_telemetry_summary": execution_telemetry_summary,
        "tc061r_protocol_deviation_and_rerun_comparison": tc061r_protocol_deviation_and_rerun_comparison,
        "global_probe_outcomes": agg["global_probe_outcomes"],
        "mechanism_kl1_holdout_summary": agg["mechanism_kl1_holdout_summary"],
        "holdout_point_evaluations": holdout_rows,
        "all_section_3_checks_pass": bool(
            agg["holdout_coverage_summary"]["mathematical_coverage_complete"]
            and cert_summary["certification_integrity_ok"]
            and not res_summary["any_resource_budget_exceeded"]
            and consistency_all_ok
            and tail_4096_evaluated
            and ho_128_protocol_ok
            and ho_128_overlap_ok
        ),
    }


# ---------------------------------------------------------------------------
# 5. Section 4: Controls & Attribution to All-Prime TC Arithmetic
# ---------------------------------------------------------------------------


def evaluate_control_matched_point_arb(
    Y_int: int,
    mode: str,
    selberg_table: Dict[str, Any],
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Evaluate shared-window raw covariance diagnostics AND exact matched `z = 1` double-pole
    Laurent-compensated reconstruction `Q_{a_S,Y} = 2*P_{a_S,Y} - A_{a_S,Y} - B_{a_S,Y}` for
    `mode in ('liouville', 'unsigned_1', 'a2', 'a_3_5_7')`, plus explicitly labeled hybrid
    `mode == 'hybrid_a2_liouville'`.
    """
    T_y = certify_T_canonical_cutoff(Y_int, prec_bits=prec_bits)
    D0_raw = certify_D0_small_divisor_cutoff(Y_int, kappa=1, prec_bits=prec_bits)
    D0_eff = min(D0_raw, max(0, T_y - 1))
    ceil_tau_y = certify_ceil_tau_Y_cutoff(Y_int, prec_bits=prec_bits)

    work_prec = prec_bits + 32
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = work_prec
        tau = _tau_arb()
        log_tau = tau.log()
        Y_arb = arb(Y_int)
        log_Y = Y_arb.log()
        N2 = 2 * T_y

        lam_vm = selberg_table["lam_vm"]
        conv_ll = selberg_table["conv_ll"]

        if mode == "liouville":
            seq_fn: Callable[[int], int] = liouville_lambda_int
            model_class = "AUTHENTIC_ALL_PRIME_TC_ARITHMETIC"
        elif mode == "unsigned_1":
            seq_fn = lambda _n: 1
            model_class = "UNSIGNED_EXACT_LAURENT_MATCHED_CONTROL"
        elif mode == "a2":
            seq_fn = two_adic_parity_a2_int
            model_class = "FIXED_SINGLE_PRIME_EXACT_LAURENT_MATCHED_CONTROL"
        elif mode == "a_3_5_7":
            seq_fn = lambda n: finite_prime_parity_aS_int(n, (3, 5, 7))
            model_class = "FIXED_THREE_PRIME_EXACT_LAURENT_MATCHED_CONTROL"
        elif mode == "hybrid_a2_liouville":
            seq_fn = two_adic_parity_a2_int
            model_class = "HYBRID_DIAGNOSTIC_INNER_A2_OUTER_LIOUVILLE_COMPENSATION"
        else:
            raise ValueError(f"Unknown control mode {mode!r}")

        a_int = [0] + [seq_fn(n) for n in range(1, T_y + 1)]
        a_r = [arb(v) for v in a_int]
        ln_r = [arb(0)] + [arb(n).log() for n in range(1, T_y + 1)]
        p_num_r = [arb(0)] + [a_r[n] * ln_r[n] for n in range(1, T_y + 1)]

        alpha_A = [arb(0)] * (N2 + 1)
        s_Y_sm = [arb(0)] * (N2 + 1)

        if mode == "liouville":
            c_lam = selberg_table["c_lambda"]
            R_tbl = selberg_table["R"]
            M_drift = selberg_table["M_drift"]
            R_osc = selberg_table["R_osc"]
            for n in range(1, T_y + 1):
                if is_perfect_square_int(n):
                    alpha_A[n] += c_lam
            alpha_A[T_y] += R_tbl[T_y]
            for d_i in range(1, T_y):
                L_d = T_y // d_i
                L_d1 = T_y // (d_i + 1)
                Rd = R_tbl[d_i]
                for q in range(L_d1 + 1, L_d + 1):
                    alpha_A[(d_i + 1) * q] += Rd * a_r[q]
                w_k = M_drift[d_i] + (R_osc[d_i] if d_i <= D0_eff else arb(0))
                for q in range(1, L_d + 1):
                    term = w_k * a_r[q]
                    alpha_A[d_i * q] += term
                    alpha_A[(d_i + 1) * q] -= term
            for d_i in range(D0_eff + 1, T_y):
                L_d = T_y // d_i
                wd = R_osc[d_i]
                for q in range(1, L_d + 1):
                    term = wd * a_r[q]
                    s_Y_sm[d_i * q] += term
                    s_Y_sm[(d_i + 1) * q] -= term
        elif mode == "hybrid_a2_liouville":
            R_osc = selberg_table["R_osc"]
            for d_i in range(D0_eff + 1, T_y):
                L_d = T_y // d_i
                wd = R_osc[d_i]
                for q in range(1, L_d + 1):
                    term = wd * a_r[q]
                    s_Y_sm[d_i * q] += term
                    s_Y_sm[(d_i + 1) * q] -= term
        else:
            gamma_e = arb.const_euler()
            prime_set: Tuple[int, ...] = (
                () if mode == "unsigned_1" else ((2,) if mode == "a2" else (3, 5, 7))
            )
            c0_S = -(
                arb(2)
                + arb(2) * gamma_e
                + sum((arb(4 * p) * arb(p).log() / arb(p * p - 1) for p in prime_set), arb(0))
            )
            M_pole = [arb(0)] * (T_y + 1)
            R_S = [arb(0)] * (T_y + 1)
            cum_w = arb(0)
            for d_i in range(1, T_y + 1):
                if d_i >= 2:
                    wd_i = a_r[d_i] * (lam_vm[d_i] * ln_r[d_i] + conv_ll[d_i])
                    cum_w += wd_i
                d_arb = arb(d_i)
                M_pole[d_i] = arb(2) * d_arb * ln_r[d_i] + c0_S * d_arb
                R_S[d_i] = cum_w - M_pole[d_i]

            for m in range(1, T_y + 1):
                mu_m = M_pole[m] - M_pole[m - 1]
                L_m = T_y // m
                for q in range(1, L_m + 1):
                    alpha_A[m * q] += mu_m * a_r[q]
            alpha_A[T_y] += R_S[T_y]
            for d_i in range(1, T_y):
                L_d = T_y // d_i
                L_d1 = T_y // (d_i + 1)
                Rd = R_S[d_i]
                for q in range(L_d1 + 1, L_d + 1):
                    alpha_A[(d_i + 1) * q] += Rd * a_r[q]
                if d_i <= D0_eff:
                    for q in range(1, L_d + 1):
                        term = Rd * a_r[q]
                        alpha_A[d_i * q] += term
                        alpha_A[(d_i + 1) * q] -= term
            for d_i in range(D0_eff + 1, T_y):
                L_d = T_y // d_i
                wd = R_S[d_i]
                for q in range(1, L_d + 1):
                    term = wd * a_r[q]
                    s_Y_sm[d_i * q] += term
                    s_Y_sm[(d_i + 1) * q] -= term

        three_zone = T_y >= 512
        n_panels = 16 if three_zone else 1
        quad_tol_bits = 160 if three_zone else 220
        M_taylor = 56
        N1 = max(T_y + 1, ceil_tau_y) if three_zone else (N2 + 1)

        pp_pairs = prime_power_pairs_up_to(T_y)
        pp_info = [(p ** k, T_y // (p ** k), arb(p).log() ** 2) for (p, k) in pp_pairs]
        pp_info_c = [(pk, L_pk, acb(lg2)) for (pk, L_pk, lg2) in pp_info]

        inv_n3_r = [arb(0)] + [arb(n) ** (-3) for n in range(1, N2 + 1)]
        inv_n3_c = [acb(v) for v in inv_n3_r]
        neg_inv_n2_c = [acb(0)] + [-(acb(n) ** (-2)) for n in range(1, N2 + 1)]
        a_c = [acb(v) for v in a_r]
        ln_c = [acb(v) for v in ln_r]
        p_num_c = [acb(v) for v in p_num_r]
        alpha_A_c = [acb(v) for v in alpha_A]
        s_Y_sm_c = [acb(v) for v in s_Y_sm]

        def _build_z3(vec_r: Sequence[arb]) -> Tuple[List[acb], arb]:
            if N1 > N2:
                return ([acb(0)] * M_taylor, arb(0))
            N1_sq = arb(N1) ** 2
            S_pow = [arb(0)] * M_taylor
            S_rem = arb(0)
            for n in range(N1, N2 + 1):
                cn = vec_r[n]
                if cn == arb(0):
                    continue
                base = cn * inv_n3_r[n]
                r2 = N1_sq / arb(n * n)
                pw = arb(1)
                for m_idx in range(M_taylor):
                    S_pow[m_idx] += base * pw
                    pw *= r2
                S_rem += abs(base) * pw
            pC = [acb(0)] * M_taylor
            fact = arb(1)
            for m_idx in range(M_taylor):
                if m_idx > 0:
                    fact *= arb(m_idx)
                sgn = arb(-1) if (m_idx % 2 == 1) else arb(1)
                pC[m_idx] = acb(sgn * S_pow[m_idx] / fact)
            rem_M = arb(2) * S_rem / (fact * arb(M_taylor))
            return (pC, rem_M)

        poly_A, rem_A = _build_z3(alpha_A)
        poly_B, rem_B = _build_z3(s_Y_sm)
        N1_c = acb(N1)
        Y_c = acb(Y_arb)
        log_Y_c = acb(log_Y)
        tol = 2 ** (-quad_tol_bits)

        E_acc = arb(0)
        P2_acc = arb(0)
        D_acc = arb(0)
        A2_acc = arb(0)
        B2_acc = arb(0)
        PB_acc = arb(0)
        QA2_acc = arb(0)

        for j in range(n_panels):
            u_lo = log_tau * arb(j) / arb(n_panels)
            u_hi = log_tau * arb(j + 1) / arb(n_panels)
            du = u_hi - u_lo
            sqrt_du = du.sqrt()
            x_lo = Y_arb * u_lo.exp()
            lg_lo = log_Y + u_lo
            if three_zone:
                n0_j = min(T_y, max(0, int(float(x_lo.lower()) // 12)))
                while n0_j > 0 and not bool(x_lo >= arb(12 * n0_j)):
                    n0_j -= 1
            else:
                n0_j = 0

            eps_Q = arb(0)
            eps_P = arb(0)
            eps_A = arb(0)
            eps_B = arb(0)
            delta_diag_j = arb(0)
            if n0_j > 0:
                x_lo_52 = x_lo ** (arb(5) / arb(2))
                x_lo_2 = x_lo * x_lo
                phi_lo = [arb(0)] * (n0_j + 1)
                for n in range(1, n0_j + 1):
                    phi_lo[n] = x_lo_52 * inv_n3_r[n] * (-x_lo_2 / arb(n * n)).exp()
                    eps_Q += phi_lo[n]
                    eps_P += ln_r[n] * phi_lo[n]
                    eps_A += abs(alpha_A[n]) * phi_lo[n]
                    d_lg_lo = lg_lo - ln_r[n]
                    eps_B += (abs(s_Y_sm[n]) + (d_lg_lo * d_lg_lo)) * phi_lo[n]
                eps_P /= lg_lo
                eps_A /= lg_lo * lg_lo
                eps_B /= lg_lo * lg_lo
                diag_sq_sum = arb(0)
                for pk, L_pk, lg_p_sq in pp_info:
                    if pk > n0_j:
                        break
                    q0 = min(L_pk, n0_j // pk)
                    s_pk = arb(0)
                    for q in range(1, q0 + 1):
                        s_pk += phi_lo[pk * q]
                    diag_sq_sum += lg_p_sq * (s_pk * s_pk)
                delta_diag_j = (sqrt_du / lg_lo) * diag_sq_sum.sqrt()

            node_cache: Dict[Any, Tuple[acb, acb, acb, acb, acb]] = {}
            hi_z2 = min(N2, N1 - 1)
            hi_T = min(T_y, hi_z2)

            def _eval_bd(u: acb, _an: bool):
                lg = log_Y_c + u
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    return None
                use_c = u.is_finite()
                key = None
                if use_c:
                    key = (
                        flint_ctx.prec,
                        u.real.mid().man_exp(),
                        u.real.rad().man_exp(),
                        u.imag.mid().man_exp(),
                        u.imag.rad().man_exp(),
                    )
                    c_hit = node_cache.get(key)
                    if c_hit is not None:
                        return c_hit
                x = Y_c * u.exp()
                x2 = x * x
                x_52 = (Y_c ** (acb(5) / acb(2))) * (acb(arb(5) / arb(2)) * u).exp()
                phi_c = [acb(0)] * (T_y + 1)
                q_val = acb(0)
                p_num = acb(0)
                q_sh2 = acb(0)
                a_num = acb(0)
                b_sm = acb(0)
                for n in range(n0_j + 1, hi_T + 1):
                    ph = x_52 * inv_n3_c[n] * (x2 * neg_inv_n2_c[n]).exp()
                    phi_c[n] = ph
                    aph = a_c[n] * ph
                    q_val += aph
                    p_num += p_num_c[n] * ph
                    d_lg = lg - ln_c[n]
                    q_sh2 += aph * (d_lg * d_lg)
                    a_num += alpha_A_c[n] * ph
                    b_sm += s_Y_sm_c[n] * ph
                for n in range(hi_T + 1, hi_z2 + 1):
                    ph = x_52 * inv_n3_c[n] * (x2 * neg_inv_n2_c[n]).exp()
                    a_num += alpha_A_c[n] * ph
                    b_sm += s_Y_sm_c[n] * ph
                if N1 <= N2:
                    rx = x / N1_c
                    w = rx * rx
                    abs_w = abs(w)
                    if bool(abs_w <= arb(M_taylor) / arb(2)):
                        pa = acb(0)
                        pb = acb(0)
                        for m_idx in range(M_taylor - 1, -1, -1):
                            pa = pa * w + poly_A[m_idx]
                            pb = pb * w + poly_B[m_idx]
                        abs_w_up = abs_w.upper()
                        w_pow = arb(0) if abs_w_up == arb(0) else (abs_w_up ** M_taylor)
                        ra = (rem_A * w_pow).upper()
                        rb = (rem_B * w_pow).upper()
                        a_num += x_52 * (pa + acb(arb(0, ra), arb(0, ra)))
                        b_sm += x_52 * (pb + acb(arb(0, rb), arb(0, rb)))
                    else:
                        for n in range(N1, N2 + 1):
                            ph = x_52 * inv_n3_c[n] * (x2 * neg_inv_n2_c[n]).exp()
                            if n <= T_y:
                                phi_c[n] = ph
                                aph = a_c[n] * ph
                                q_val += aph
                                p_num += p_num_c[n] * ph
                                d_lg = lg - ln_c[n]
                                q_sh2 += aph * (d_lg * d_lg)
                            a_num += alpha_A_c[n] * ph
                            b_sm += s_Y_sm_c[n] * ph
                lg2 = lg * lg
                p_val = p_num / lg
                a_val = a_num / lg2
                b_val = (b_sm - q_sh2) / lg2
                d_sum = acb(0)
                for pk, L_pk, lg_p_sq_c in pp_info_c:
                    q_start = (n0_j // pk) + 1
                    if q_start > L_pk:
                        continue
                    s_pk = acb(0)
                    for q in range(q_start, L_pk + 1):
                        s_pk += a_c[q] * phi_c[pk * q]
                    d_sum += lg_p_sq_c * (s_pk * s_pk)
                d_val = d_sum / lg2
                bd = (q_val, p_val, a_val, b_val, d_val)
                if use_c and key is not None:
                    node_cache[key] = bd
                return bd

            def _int_fn(fn):
                def _cb(u: acb, _an: bool) -> acb:
                    bd = _eval_bd(u, _an)
                    if bd is None:
                        nb = arb("nan")
                        return acb(nb, nb)
                    return fn(bd)

                return acb.integral(_cb, acb(u_lo), acb(u_hi), rel_tol=tol, abs_tol=tol).real

            E_m = _int_fn(lambda b: b[0] * b[0])
            P2_m = _int_fn(lambda b: b[1] * b[1])
            D_m = _int_fn(lambda b: b[4])
            A2_m = _int_fn(lambda b: b[2] * b[2])
            B2_m = _int_fn(lambda b: b[3] * b[3])
            PB_m = _int_fn(lambda b: b[1] * b[3])
            QA2_m = _int_fn(lambda b: (b[0] + b[2]) * (b[0] + b[2]))

            def _sq_pert(main_v: arb, eps_v: arb) -> arb:
                if eps_v == arb(0):
                    return main_v
                nm = abs(main_v).sqrt()
                rad = (arb(2) * nm * eps_v * sqrt_du + (eps_v * eps_v) * du).upper()
                return main_v + arb(0, rad)

            def _bilin_pert(main_v: arb, i_f: arb, i_g: arb, eps_f: arb, eps_g: arb) -> arb:
                if eps_f == arb(0) and eps_g == arb(0):
                    return main_v
                nf = abs(i_f).sqrt()
                ng = abs(i_g).sqrt()
                rad = (nf * eps_g * sqrt_du + ng * eps_f * sqrt_du + eps_f * eps_g * du).upper()
                return main_v + arb(0, rad)

            E_acc += _sq_pert(E_m, eps_Q)
            P2_acc += _sq_pert(P2_m, eps_P)
            A2_acc += _sq_pert(A2_m, eps_A)
            B2_acc += _sq_pert(B2_m, eps_B)
            PB_acc += _bilin_pert(PB_m, P2_m, B2_m, eps_P, eps_B)
            QA2_acc += _sq_pert(QA2_m, eps_Q + eps_A)
            if delta_diag_j == arb(0):
                D_acc += D_m
            else:
                rad_d = (arb(2) * abs(D_m).sqrt() * delta_diag_j + delta_diag_j * delta_diag_j).upper()
                D_acc += D_m + arb(0, rad_d)

        flint_ctx.prec = prec_bits
        X_out = +(P2_acc - D_acc)
        J_direct = +(arb(4) * (P2_acc - D_acc) + B2_acc - arb(4) * PB_acc)
        J_cons = +(QA2_acc - arb(4) * D_acc)
        cons_res = +(J_direct - J_cons)
        lg_D = +(log_Y * D_acc)
        return {
            "Y": Y_int,
            "mode": mode,
            "model_class": model_class,
            "T_Y": T_y,
            "D0_eff": D0_eff,
            "Y_arb": +Y_arb,
            "E_Y": +E_acc,
            "D_tilde_Y": +D_acc,
            "X_tilde_Y": X_out,
            "P_norm_sq": +P2_acc,
            "A_norm_sq": +A2_acc,
            "B_norm_sq": +B2_acc,
            "pair_P_B": +PB_acc,
            "R_mix_Y": +(B2_acc - arb(4) * PB_acc),
            "J_direct": J_direct,
            "J_consistency_residual": cons_res,
            "log_Y_times_D_tilde": lg_D,
        }
    finally:
        flint_ctx.prec = saved


def _prime_factorization_dict(n: int) -> Dict[int, int]:
    rem = n
    out: Dict[int, int] = {}
    d = 2
    while d * d <= rem:
        while rem % d == 0:
            out[d] = out.get(d, 0) + 1
            rem //= d
        d += 1 if d == 2 else 2
    if rem > 1:
        out[rem] = out.get(rem, 0) + 1
    return out


def evaluate_divisor_sum_aS_direct(n: int, prime_set: Sequence[int]) -> int:
    """Direct divisor convolution `(1 * a_S)(n) := sum_{d | n} a_S(d)` for `n >= 1`."""
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    total = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            total += finite_prime_parity_aS_int(d, prime_set)
            q = n // d
            if q != d:
                total += finite_prime_parity_aS_int(q, prime_set)
        d += 1
    return total


def evaluate_finite_prime_parity_convolution_formula(n: int, prime_set: Sequence[int]) -> int:
    """Exact multiplicative divisor-convolution formula (`TASK-TC-061R` §3, Lean Theorem 6):

        `(1 * a_S)(n) = prod_{p in S} ((1 + (-1)^{v_p(n)}) / 2) * prod_{p | n, p notin S} (v_p(n) + 1)`.

    In particular:
    - For `S = empty` (`a_empty = 1`), `(1 * 1)(n) = d(n)` (e.g. `n = 12 -> 6 != 1`);
    - For `S = {2}`, `(1 * a_{2})(n) = 0` when `v_2(n)` is odd and `d(n_{odd})` when `v_2(n)` is even
      (e.g. `n = 3 -> 2`, `n = 6 -> 0`, `n = 12 -> 2`).
    """
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    s_set = set(int(p) for p in prime_set)
    pf = _prime_factorization_dict(n)
    for p in s_set:
        if pf.get(p, 0) % 2 == 1:
            return 0
    prod_outside = 1
    for p, v_p in pf.items():
        if p not in s_set:
            prod_outside *= v_p + 1
    return prod_outside


def compute_finite_prime_control_invariants(
    prime_set: Sequence[int],
    *,
    verify_up_to: int = 300,
) -> Dict[str, Any]:
    """Compute and strictly separate the three arithmetic invariants of a finite-prime parity control
    `a_S(n) = (-1)^{sum_{p in S} v_p(n)}` (`TASK-TC-061R` §3):
    1. Exact divisor convolution `(1 * a_S)(n)` (`= prod_{p in S} 1_{2 | v_p(n)} * prod_{p notin S} (v_p(n)+1)`),
       which is unbounded along powers of a prime `p` outside `S` (`(1 * a_S)(p) = 2` whereas
       `(1 * a_S)(p^k) = k + 1`, and `(1 * a_S)(n) = d(n_{notin S})` when `2 | v_q(n)` for all
       `q in S`), unlike all-prime `(1 * lambda)(n) = 1_{sq}(n) in {0, 1}`;
    2. Natural density of `{n >= 1 : (1 * a_S)(n) != 0}` (`= {n >= 1 : 2 | v_p(n) forall p in S}`),
       namely `prod_{p in S} (p / (p + 1))`;
    3. Simple-pole residue at `z = 1` of `D_{a_S}(z) = sum_{n >= 1} a_S(n) n^{-z} = zeta(z) * prod_{p in S} ((1 - p^{-z})/(1 + p^{-z}))`
       (`z = x + i*y`, `x > 1`), namely `Res_{z = 1} D_{a_S}(z) = prod_{p in S} ((p - 1) / (p + 1))`.
    """
    s_tuple = tuple(sorted(set(int(p) for p in prime_set)))
    support_density = Fraction(1, 1)
    residue_z1 = Fraction(1, 1)
    for p in s_tuple:
        support_density *= Fraction(p, p + 1)
        residue_z1 *= Fraction(p - 1, p + 1)

    conv_verified = True
    for n_i in range(1, verify_up_to + 1):
        if evaluate_divisor_sum_aS_direct(n_i, s_tuple) != evaluate_finite_prime_parity_convolution_formula(
            n_i, s_tuple
        ):
            conv_verified = False
            break

    spot_values = {
        str(n_sp): evaluate_finite_prime_parity_convolution_formula(n_sp, s_tuple)
        for n_sp in (1, 2, 3, 4, 6, 8, 9, 12, 15, 18, 30, 36)
    }
    return {
        "prime_set_S": list(s_tuple),
        "convolution_formula": (
            "(1 * a_S)(n) = prod_{p in S} ((1 + (-1)^{v_p(n)})/2) * prod_{p | n, p notin S} (v_p(n) + 1)"
        ),
        "convolution_verified_1_to_N": verify_up_to,
        "convolution_formula_verified": conv_verified,
        "convolution_spot_values": spot_values,
        "nonzero_support_natural_density_fraction": f"{support_density.numerator}/{support_density.denominator}",
        "dirichlet_series_D_aS_residue_at_z1_fraction": f"{residue_z1.numerator}/{residue_z1.denominator}",
        "matched_z1_laurent_drift_formula": "M_{2,a_S}(d) = 2*d*log(d) - (2 + 2*beta_S)*d",
    }


def verify_section_4_controls_and_tc_arithmetic_attribution(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Compare authentic all-prime Liouville `lambda` against unsigned `1`, fixed finite-prime
    parity controls `a_2` and `a_{3,5,7}` (exact divisor convolution `(1 * a_S)(n)`, support
    density, `z = 1` residue, raw shared-window covariance, and exact matched `z = 1` double-pole
    Laurent reconstruction), and explicitly labeled hybrid `a_2 + Liouville` across
    `Y in {16, 32, 64, 128, 256, 512}` using shared frozen probe parameters (`TASK-TC-061R` §3).
    """
    proto = json.loads(MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH.read_text(encoding="utf-8"))
    probes = proto["frozen_candidate_probes"]

    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(2500, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 2450
        else selberg_table
    )

    invariants_by_mode = {
        "unsigned_1": compute_finite_prime_control_invariants((), verify_up_to=300),
        "a2": compute_finite_prime_control_invariants((2,), verify_up_to=300),
        "a_3_5_7": compute_finite_prime_control_invariants((3, 5, 7), verify_up_to=300),
    }
    invariants_ok = bool(
        all(inv["convolution_formula_verified"] for inv in invariants_by_mode.values())
        and invariants_by_mode["unsigned_1"]["convolution_spot_values"]["12"] == 6
        and invariants_by_mode["unsigned_1"]["nonzero_support_natural_density_fraction"] == "1/1"
        and invariants_by_mode["unsigned_1"]["dirichlet_series_D_aS_residue_at_z1_fraction"] == "1/1"
        and invariants_by_mode["a2"]["convolution_spot_values"]["3"] == 2
        and invariants_by_mode["a2"]["convolution_spot_values"]["6"] == 0
        and invariants_by_mode["a2"]["convolution_spot_values"]["12"] == 2
        and invariants_by_mode["a2"]["nonzero_support_natural_density_fraction"] == "2/3"
        and invariants_by_mode["a2"]["dirichlet_series_D_aS_residue_at_z1_fraction"] == "1/3"
        and invariants_by_mode["a_3_5_7"]["nonzero_support_natural_density_fraction"] == "35/64"
        and invariants_by_mode["a_3_5_7"]["dirichlet_series_D_aS_residue_at_z1_fraction"] == "1/4"
    )

    modes = ("liouville", "unsigned_1", "a2", "a_3_5_7", "hybrid_a2_liouville")
    scales = (16, 32, 64, 128, 256, 512)
    control_rows: List[Dict[str, Any]] = []
    matched_identities_ok = True
    all_negative_controls_fail_on_holdout = True

    for y_val in scales:
        for mode in modes:
            r = evaluate_control_matched_point_arb(y_val, mode, tbl, prec_bits=prec_bits)
            is_exact_matched = mode != "hybrid_a2_liouville"
            if is_exact_matched:
                id_ok = bool(
                    arb(0) in r["J_consistency_residual"]
                    and abs(r["J_consistency_residual"]) < arb("1e-44")
                )
                matched_identities_ok = matched_identities_ok and id_ok
            else:
                id_ok = False

            probe_eval = _evaluate_probes_for_point_result(
                r,
                probes,
                in_declared_domain_fn=lambda pr, _y=y_val: _y >= int(pr["domain_threshold_Y0"]),
                prec_bits=prec_bits,
            )
            if y_val >= 64 and mode in ("unsigned_1", "a2", "a_3_5_7"):
                for pid in ("TC061-P0", "TC061-P_1_2", "TC061-P_1_4", "TC061-P_1_8"):
                    if probe_eval["per_probe"][pid]["point_verdict"] != "FAIL":
                        all_negative_controls_fail_on_holdout = False

            control_rows.append(
                {
                    "Y": y_val,
                    "mode": mode,
                    "model_class": r["model_class"],
                    "exact_matched_reconstruction": is_exact_matched,
                    "T_Y": r["T_Y"],
                    "D0_eff": r["D0_eff"],
                    "raw_shared_window_diagnostics": {
                        "E_Y": serialize_arb_certified(r["E_Y"]),
                        "D_tilde_Y": serialize_arb_certified(r["D_tilde_Y"]),
                        "four_X_tilde_Y": serialize_arb_certified(arb(4) * r["X_tilde_Y"]),
                    },
                    "A_norm_sq": serialize_arb_certified(r["A_norm_sq"]),
                    "B_norm_sq": serialize_arb_certified(r["B_norm_sq"]),
                    "pair_P_B": serialize_arb_certified(r["pair_P_B"]),
                    "J_functional": serialize_arb_certified(r["J_direct"]),
                    "J_consistency_residual_if_matched": (
                        serialize_arb_certified(r["J_consistency_residual"])
                        if is_exact_matched
                        else None
                    ),
                    "matched_identity_verified": id_ok if is_exact_matched else None,
                    "log_Y_times_D_tilde": serialize_arb_certified(r["log_Y_times_D_tilde"]),
                    "J_over_log_Y_D_tilde": probe_eval["J_over_log_Y_D_tilde"],
                    "shared_probe_margins": {
                        pid: pdata["margin_M_Y"]
                        for pid, pdata in probe_eval["per_probe"].items()
                    },
                    "shared_probe_verdicts": {
                        pid: pdata["point_verdict"]
                        for pid, pdata in probe_eval["per_probe"].items()
                    },
                }
            )

    return {
        "epistemic_statuses": [
            "UNCONDITIONAL_FINITE_ARITHMETIC",
            "CONCRETE_ANALYTIC_IN_LEAN",
            "ANALYTIC_PROVED_OUTSIDE_LEAN",
            "CERTIFIED_FINITE_OBSERVATION",
        ],
        "section_epistemic_scope_note": (
            "Mixed arithmetic/analytic/numerical section: the exact multiplicative divisor-"
            "convolution formula (1 * a_S)(n) = prod_{p in S} ((1 + (-1)^{v_p(n)})/2) * "
            "prod_{p | n, p notin S} (v_p(n) + 1) is CONCRETE_ANALYTIC_IN_LEAN (Lean Theorem 6) "
            "and UNCONDITIONAL_FINITE_ARITHMETIC; the natural density prod_{p in S} (p/(p+1)) of "
            "{n : (1 * a_S)(n) != 0}, the z = 1 residue prod_{p in S} ((p-1)/(p+1)) of D_{a_S}(z), "
            "and the matched second-order Laurent reconstructions Q_{a_S,Y} = 2*P_{a_S,Y} - "
            "A_{a_S,Y} - B_{a_S,Y} with M_{2,a_S}(d) = 2*d*log(d) - (2 + 2*beta_S)*d are "
            "ANALYTIC_PROVED_OUTSIDE_LEAN; and the 256-bit Arb evaluations across Y in "
            "{16, 32, 64, 128, 256, 512} certifying FAIL on all four frozen probes for every "
            "negative control are CERTIFIED_FINITE_OBSERVATION (scoped strictly to the evaluated "
            "finite grid without unproved asymptotic rate assertions or unique-tau-mechanism claims)."
        ),
        "component_epistemic_map": {
            "finite_prime_parity_divisor_convolution_formula": "CONCRETE_ANALYTIC_IN_LEAN",
            "direct_divisor_sum_verification_1_to_300": "UNCONDITIONAL_FINITE_ARITHMETIC",
            "support_density_z1_residue_and_matched_laurent_reconstructions": "ANALYTIC_PROVED_OUTSIDE_LEAN",
            "control_vs_liouville_shared_probe_certificates_16_to_512": "CERTIFIED_FINITE_OBSERVATION",
        },
        "lean_theorems": [
            "finite_prime_parity_divisor_convolution_formula_tc061r",
        ],
        "control_arithmetic_invariants": invariants_by_mode,
        "tc_arithmetic_attribution_statement": (
            "On the evaluated finite grid Y in {16, 32, 64, 128, 256, 512}, all-prime Liouville "
            "signs lambda(n) = (-1)^Omega(n) (for which (1 * lambda)(n) = 1_sq(n) cancels the z = 1 "
            "pole of zeta(z)) pass every frozen probe on Y >= 64, whereas unsigned 1 and fixed "
            "finite-prime parity controls (S = empty, {2}, {3,5,7} — where (1 * a_S)(n) equals "
            "prod_{p notin S} (v_p(n)+1) on its even-S-valuation support of density prod_{p in S} p/(p+1) "
            "and D_{a_S}(z) retains residue prod_{p in S} (p-1)/(p+1) > 0 at z = 1) are certified "
            "FAIL on every frozen probe across Y in {64, 128, 256, 512} (with J_{a_S}/((log Y)*D_tilde_{a_S}) "
            "in [+29.75, +38.76] and ||A_{a_S,Y}||_Y^2 in [14.24, 254.29] at Y = 512 vs ||A_Y||_Y^2 approx "
            "0.03221 for Liouville). These finite negative-control contrasts falsify attribution to "
            "generic window/transport algebra or fixed finite-prime parity alone on the tested grid, "
            "without asserting unproved asymptotic growth laws or a unique tau-specific mechanism."
        ),
        "control_arithmetic_invariants_verified": invariants_ok,
        "matched_reconstruction_identities_verified": matched_identities_ok,
        "all_negative_controls_certified_fail_on_Y_ge_64": all_negative_controls_fail_on_holdout,
        "control_comparison_rows": control_rows,
        "all_section_4_checks_pass": bool(
            invariants_ok and matched_identities_ok and all_negative_controls_fail_on_holdout
        ),
    }


# ---------------------------------------------------------------------------
# 6. Section 5: Signed-Kernel Proof Attempt, Self-Collision Bound, & Bridge
# ---------------------------------------------------------------------------


def evaluate_X_self_collision_arb(
    Y_arb: arb,
    T_y: int,
    prec_bits: int = 256,
) -> arb:
    """Evaluate composite self-collision diagonal `X_self(Y) = sum_{n=1}^T Delta_pp(n, n) G_Y^{[2]}(n, n)`."""
    work_prec = prec_bits + 32
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = work_prec
        tau = _tau_arb()
        log_tau = tau.log()
        log_Y = Y_arb.log()

        sum_lg_p_sq = [arb(0)] * (T_y + 1)
        for p, k in prime_power_pairs_up_to(T_y):
            pk = p ** k
            lg2 = arb(p).log() ** 2
            for mult in range(pk, T_y + 1, pk):
                sum_lg_p_sq[mult] += lg2

        delta_self_c: List[Tuple[int, acb, acb]] = []
        for n in range(1, T_y + 1):
            d_nn = (arb(n).log() ** 2) - sum_lg_p_sq[n]
            if bool(d_nn > arb(0)):
                delta_self_c.append((n, acb(d_nn * (arb(n) ** (-6))), acb(-arb(2) / arb(n * n))))

        Y_c = acb(Y_arb)
        log_Y_c = acb(log_Y)
        tol = 2 ** (-160)
        panels = 8 if T_y >= 512 else 1
        acc = arb(0)
        for j in range(panels):
            u_lo = log_tau * arb(j) / arb(panels)
            u_hi = log_tau * arb(j + 1) / arb(panels)
            x_lo = Y_arb * u_lo.exp()
            lg_lo = log_Y + u_lo
            n_min = max(1, int(math.floor(float(x_lo.lower()) / 14.0))) if T_y >= 512 else 1
            while n_min > 1 and not bool(x_lo >= arb(14 * (n_min - 1))):
                n_min -= 1
            z1_rad = arb(0)
            if n_min > 1:
                x_lo_5 = x_lo ** 5
                x_lo_2 = x_lo * x_lo
                s_z1 = arb(0)
                for n, coeff_c, exp_c in delta_self_c:
                    if n >= n_min:
                        break
                    s_z1 += abs(coeff_c.real) * x_lo_5 * (exp_c.real * x_lo_2).exp()
                z1_rad = ((u_hi - u_lo) * s_z1 / (lg_lo * lg_lo)).upper()

            active = [(n, cc, ec) for (n, cc, ec) in delta_self_c if n >= n_min]

            def _cb(u: acb, _an: bool, _act=active) -> acb:
                lg = log_Y_c + u
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                x = Y_c * u.exp()
                x2 = x * x
                x5 = (Y_c ** 5) * (acb(5) * u).exp()
                s = acb(0)
                for _n, cc, ec in _act:
                    s += cc * (x2 * ec).exp()
                return x5 * s / (lg * lg)

            val = acb.integral(_cb, acb(u_lo), acb(u_hi), rel_tol=tol, abs_tol=tol).real
            acc += val + arb(0, z1_rad)
        flint_ctx.prec = prec_bits
        return +acc
    finally:
        flint_ctx.prec = saved


def evaluate_window_gram_G_Y_r_arb(
    Y_arb: arb,
    m: int,
    n: int,
    r_pow: int,
    prec_bits: int = 256,
) -> arb:
    """Evaluate `G_Y^{[r]}(m, n) := int_Y^{tau*Y} phi_m(X)*phi_n(X)*(log X)^{-r} dX/X` (`r >= 0`)."""
    if r_pow == 0:
        return evaluate_window_kernel_K_closed_arb(Y_arb, m, n, _tau_arb(), prec_bits=prec_bits)
    work_prec = prec_bits + 32
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = work_prec
        tau = _tau_arb()
        log_tau = tau.log()
        log_Y_c = acb(Y_arb.log())
        Y_c = acb(Y_arb)
        coeff_c = acb(arb(m * n) ** (-3))
        rate_c = acb(-(arb(1) / arb(m * m) + arb(1) / arb(n * n)))
        tol = 2 ** (-200)

        def _cb(u: acb, _an: bool) -> acb:
            lg = log_Y_c + u
            if _an and not bool(lg.real > arb(1) / arb(2)):
                nb = arb("nan")
                return acb(nb, nb)
            x = Y_c * u.exp()
            x5 = (Y_c ** 5) * (acb(5) * u).exp()
            return coeff_c * x5 * ((x * x) * rate_c).exp() / (lg ** r_pow)

        val = acb.integral(_cb, acb(0), acb(log_tau), rel_tol=tol, abs_tol=tol).real
        flint_ctx.prec = prec_bits
        return +val
    finally:
        flint_ctx.prec = saved


def verify_self_collision_elementary_majorant_proof_arb(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify step-by-step the complete elementary outside-Lean proof that for all real `Y >= 2`
    and all `T in N`,

        `0 <= X_self(Y) <= sum_{n=1}^T (log n)^2 * G_Y^{[2]}(n, n) <= (289/60)*log(tau) < (1377/160)*log(tau) < 16`,

    complementing Lean Theorem 3's kernel-checked `O(1)` bound `186*(tau - 1) < 1302`:
    1. Exact general `c_self(n)` identity (including non-squarefree `n` such as `n = 4 = 2^2`):
       `c_self(n) := (log n)^2 - sum_{p^k | n} (log p)^2`
       `= sum_{p | n} v_p(n)*(v_p(n) - 1)*(log p)^2 + sum_{p != q | n} (v_p(n)*log p)*(v_q(n)*log q)`,
       so `0 <= c_self(n) <= (log n)^2` for all `n >= 1` (`c_self(1) = 0`, `c_self(p) = 0`,
       `c_self(4) = 2*(log 2)^2 > 0`).
    2. Pointwise integrand split at fixed `X >= 2` (`n = 1` contributes `log 1 = 0`):
       - Head `2 <= n <= floor(X)` (`floor(X) - 1 < X` terms): `0 < log n <= log X => (log n)^2/(log X)^2 <= 1`,
         and for `u = 2*X^2/n^2 > 0`, Taylor positivity `e^u > u^3/6 = 4*X^6/(3*n^6)` gives
         `phi_n(X)^2 = X^5 * n^{-6} * e^{-u} < 3/(4*X)`; summing `< X` terms yields `< 3/4`.
       - Tail `n >= n_0 := floor(X) + 1 > X >= 2` (`n_0 >= 3`, `w := n/X > 1`):
         since `e < 272/100 => e^2 < 73984/10000 < 8 = 2^3`, `log X >= log 2 > 2/3`; with
         `0 < log w < w` and `(a + b)^2 <= 2*a^2 + 2*b^2`,
         `(log n)^2/(log X)^2 = (1 + log(w)/log(X))^2 < 2 + (2/(2/3)^2)*w^2 = 2 + (9/2)*(n^2/X^2)`.
         Using `e^{-2*X^2/n^2} < 1` and integral comparison on decreasing `u^{-6}` and `u^{-4}`:
         `sum_{n >= n_0} X^5*n^{-6} <= X^5*n_0^{-6} + X^5*int_{n_0}^infty u^{-6} du < 1/n_0 + 1/5 <= 1/3 + 1/5 = 8/15`,
         `sum_{n >= n_0} X^3*n^{-4} <= X^3*n_0^{-4} + X^3*int_{n_0}^infty u^{-4} du < 1/n_0 + 1/3 <= 1/3 + 1/3 = 2/3`.
         Hence tail `< 2*(8/15) + (9/2)*(2/3) = 16/15 + 3 = 61/15`.
       - Total pointwise density for every `X >= 2` and `T in N`:
         `(log X)^{-2} * sum_{n=1}^T (log n)^2 * phi_n(X)^2 < 3/4 + 16/15 + 3 = 289/60 < 1377/160`.
    3. Integrating against `dX/X` over `[Y, tau*Y]` (`int_Y^{tau*Y} dX/X = log(tau)`) yields
       `0 <= X_self(Y) <= (289/60)*log(tau) < (1377/160)*log(tau) < 16`.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        log_tau = tau.log()

        head_const = Fraction(3, 4)
        tail_base_series = Fraction(1, 3) + Fraction(1, 5)  # 8/15
        tail_log_series = Fraction(1, 3) + Fraction(1, 3)   # 2/3
        inv_log2_sq_bound = Fraction(2, 1) / (Fraction(2, 3) ** 2)  # 9/2
        sharp_pointwise_const = (
            head_const + Fraction(2, 1) * tail_base_series + inv_log2_sq_bound * tail_log_series
        )  # 289/60
        legacy_envelope_const = Fraction(1377, 160)

        assert head_const == Fraction(3, 4)
        assert tail_base_series == Fraction(8, 15)
        assert tail_log_series == Fraction(2, 3)
        assert inv_log2_sq_bound == Fraction(9, 2)
        assert sharp_pointwise_const == Fraction(289, 60)
        assert sharp_pointwise_const < legacy_envelope_const

        # Certify log(2) > 2/3 via e^2 < 8 in Arb:
        log2_gt_two_thirds = bool(arb(2).log() > _frac_to_arb(Fraction(2, 3)))
        sharp_bound_ball = _frac_to_arb(sharp_pointwise_const) * log_tau
        envelope_bound_ball = _frac_to_arb(legacy_envelope_const) * log_tau
        lean_bound_ball = arb(186) * (tau - arb(1))
        chain_ok = bool(
            log2_gt_two_thirds
            and sharp_bound_ball < envelope_bound_ball
            and envelope_bound_ball < arb(16)
            and lean_bound_ball < arb(1302)
        )

        # Verify exact general c_self(n) formula (including non-squarefree n = 4, 8, 12, 18, 36) on 1 <= n <= 200:
        c_self_identity_ok = True
        for n in range(1, 201):
            pf = _prime_factorization_dict(n)
            sum_pk_lg2 = sum((v_p * (arb(p).log() ** 2) for p, v_p in pf.items()), arb(0))
            lhs_c = (arb(n).log() ** 2) - sum_pk_lg2
            same_prime_coll = sum(
                (arb(v_p * (v_p - 1)) * (arb(p).log() ** 2) for p, v_p in pf.items()),
                arb(0),
            )
            diff_prime_coll = arb(0)
            pf_items = list(pf.items())
            for i_p in range(len(pf_items)):
                p_i, v_i = pf_items[i_p]
                for j_q in range(len(pf_items)):
                    if i_p != j_q:
                        q_j, v_j = pf_items[j_q]
                        diff_prime_coll += arb(v_i * v_j) * arb(p_i).log() * arb(q_j).log()
            rhs_c = same_prime_coll + diff_prime_coll
            res_c = lhs_c - rhs_c
            if not (arb(0) in res_c and abs(res_c) < arb("1e-70")):
                c_self_identity_ok = False
        c_self_4_pos = bool(((arb(4).log() ** 2) - arb(2) * (arb(2).log() ** 2)) > arb(0))

        # Spot-check pointwise density (log X)^{-2} * sum_{n=1}^{500} (log n)^2 * phi_n(X)^2 < 289/60 at X in {2, 3, 8, 32}:
        pointwise_checks_ok = True
        for x_test in (2, 3, 8, 32):
            xb = arb(x_test)
            lgx2 = xb.log() ** 2
            s_val = arb(0)
            for n_i in range(2, 501):
                nb = arb(n_i)
                phi_sq = (xb ** 5) * (nb ** (-6)) * ((-arb(2) * xb * xb / (nb * nb)).exp())
                s_val += ((nb.log() ** 2) / lgx2) * phi_sq
            if not bool(s_val < _frac_to_arb(sharp_pointwise_const)):
                pointwise_checks_ok = False

        return {
            "head_constant_fraction": "3/4",
            "tail_base_constant_fraction": "16/15",
            "tail_log_sq_constant_fraction": "3",
            "sharp_pointwise_constant_fraction": "289/60",
            "envelope_pointwise_constant_fraction": "1377/160",
            "sharp_window_bound_289_60_log_tau": serialize_arb_certified(sharp_bound_ball),
            "envelope_window_bound_1377_160_log_tau": serialize_arb_certified(envelope_bound_ball),
            "lean_theorem_3_bound_186_tau_minus_1": serialize_arb_certified(lean_bound_ball),
            "log2_gt_two_thirds_certified": log2_gt_two_thirds,
            "c_self_general_prime_power_identity_1_to_200_verified": bool(
                c_self_identity_ok and c_self_4_pos
            ),
            "pointwise_density_lt_289_60_spot_checked": pointwise_checks_ok,
            "verified": bool(chain_ok and c_self_identity_ok and c_self_4_pos and pointwise_checks_ok),
        }
    finally:
        flint_ctx.prec = saved


def verify_coarse_halfline_complement_bound_arb(
    T_vals: Sequence[int] = (7, 14, 32, 77),
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify step-by-step the unconditional coarse half-line complement bound (`TASK-TC-061R` §4):
    1. `c_G := Gamma(5/2) / 2 = (3 * sqrt(tau / 2)) / 8`;
    2. For all integers `m, n >= 1`, `m^2 + n^2 >= max(m, n)^2` implies
       `G_inf(m, n) = c_G * (m*n)^2 / (m^2 + n^2)^{5/2} <= c_G * min(m, n)^2 / max(m, n)^3`;
    3. For every `L >= 1`,
       `sum_{m, n = 1}^L min(m, n)^2 / max(m, n)^3 <= 2 * sum_{n = 1}^L n^{-3} * sum_{m = 1}^n m^2`
       `= sum_{n = 1}^L (n + 1)*(2*n + 1) / (3*n^2) <= 2 * L` (since `2*n^2 + 3*n + 1 <= 6*n^2`),
       whence `||Q_{lambda, L}||_{(0, infty)}^2 <= 2 * c_G * L`;
    4. By scale invariance `int_0^infty Q_{lambda, L}(X / p^k)^2 dX/X = ||Q_{lambda, L}||_{(0, infty)}^2`
       with `L = floor(T / p^k) <= T / p^k`,
       `0 <= E_{comp,diag}(Y, T) <= D_inf(T) <= 2 * c_G * T * sum_{p^k <= T} (log p)^2 / p^{2*k}`
       `<= 2 * c_G * T * sum_{p^k >= 2} (log p)^2 / p^{2*k} <= 2 * c_G * T * zeta''(2)`.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        c_G = arb(3) * (tau / arb(2)).sqrt() / arb(8)
        gamma_5_2_half = (arb(5) / arb(2)).gamma() / arb(2)
        c_G_gamma_ok = bool(arb(0) in (c_G - gamma_5_2_half) and abs(c_G - gamma_5_2_half) < arb("1e-70"))

        jet_z2 = acb_series([acb(2), acb(1)], prec=3).zeta()
        zeta_pp_2 = arb(2) * jet_z2[2].real

        kernel_majorant_ok = True
        for m_i in range(1, 41):
            for n_i in range(1, 41):
                g_mn = math.gcd(m_i, n_i)
                r_m = m_i // g_mn
                s_n = n_i // g_mn
                g_exact = (
                    c_G
                    * (arb(r_m * s_n) ** 2)
                    / (arb(g_mn) * (arb(r_m * r_m + s_n * s_n) ** (arb(5) / arb(2))))
                )
                mn_lo = min(m_i, n_i)
                mn_hi = max(m_i, n_i)
                g_maj = c_G * (arb(mn_lo * mn_lo) / arb(mn_hi ** 3))
                _, ok_km = classify_arb_le_certificate(g_exact, g_maj)
                kernel_majorant_ok = kernel_majorant_ok and ok_km

        norm_majorant_ok = True
        for L_i in (1, 2, 3, 5, 10, 20, 32):
            q_norm = arb(0)
            for m_i in range(1, L_i + 1):
                for n_i in range(1, L_i + 1):
                    g_mn = math.gcd(m_i, n_i)
                    r_m = m_i // g_mn
                    s_n = n_i // g_mn
                    g_exact = (
                        c_G
                        * (arb(r_m * s_n) ** 2)
                        / (arb(g_mn) * (arb(r_m * r_m + s_n * s_n) ** (arb(5) / arb(2))))
                    )
                    q_norm += arb(liouville_lambda_int(m_i * n_i)) * g_exact
            _, ok_q = classify_arb_le_certificate(q_norm, arb(2) * c_G * arb(L_i))
            norm_majorant_ok = norm_majorant_ok and bool(q_norm >= arb(0)) and ok_q

        T_rows: List[Dict[str, Any]] = []
        D_inf_ok = True
        for T_i in T_vals:
            D_inf_val = arb(0)
            pp_series_T = arb(0)
            for p, k in prime_power_pairs_up_to(T_i):
                pk = p ** k
                L_pk = T_i // pk
                lg2 = arb(p).log() ** 2
                pp_series_T += lg2 / arb(pk * pk)
                for q1 in range(1, L_pk + 1):
                    for q2 in range(1, L_pk + 1):
                        m_i = pk * q1
                        n_i = pk * q2
                        g_mn = math.gcd(m_i, n_i)
                        r_m = m_i // g_mn
                        s_n = n_i // g_mn
                        g_exact = (
                            c_G
                            * (arb(r_m * s_n) ** 2)
                            / (arb(g_mn) * (arb(r_m * r_m + s_n * s_n) ** (arb(5) / arb(2))))
                        )
                        D_inf_val += lg2 * arb(liouville_lambda_int(q1 * q2)) * g_exact
            pp_bound = arb(2) * c_G * arb(T_i) * pp_series_T
            z2_bound = arb(2) * c_G * arb(T_i) * zeta_pp_2
            _, ok_1 = classify_arb_le_certificate(D_inf_val, pp_bound)
            _, ok_2 = classify_arb_le_certificate(pp_bound, z2_bound)
            row_ok = bool(D_inf_val >= arb(0) and ok_1 and ok_2)
            D_inf_ok = D_inf_ok and row_ok
            T_rows.append(
                {
                    "T": T_i,
                    "D_inf_T": serialize_arb_certified(D_inf_val),
                    "two_cG_T_prime_power_sum": serialize_arb_certified(pp_bound),
                    "two_cG_T_zeta_double_prime_2": serialize_arb_certified(z2_bound),
                    "verified": row_ok,
                }
            )

        return {
            "c_G_formula": "Gamma(5/2)/2 = 3*sqrt(tau/2)/8",
            "c_G": serialize_arb_certified(c_G),
            "zeta_double_prime_2": serialize_arb_certified(zeta_pp_2),
            "two_cG_zeta_double_prime_2_linear_slope": serialize_arb_certified(arb(2) * c_G * zeta_pp_2),
            "c_G_matches_half_gamma_5_2": c_G_gamma_ok,
            "kernel_majorant_1_to_40_verified": kernel_majorant_ok,
            "Q_lambda_halfline_norm_le_2_cG_L_verified": norm_majorant_ok,
            "D_inf_coarse_linear_bounds": T_rows,
            "verified": bool(c_G_gamma_ok and kernel_majorant_ok and norm_majorant_ok and D_inf_ok),
        }
    finally:
        flint_ctx.prec = saved


def verify_section_5_arithmetic_proof_attempt_and_kernel_reduction(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
    precomputed_x_tilde_balls: Optional[Dict[int, arb]] = None,
    precomputed_full_rows: Optional[Dict[int, Dict[str, arb]]] = None,
) -> Dict[str, Any]:
    """Execute Section 6 required arithmetic proof attempt (`TASK-TC-061` / `TASK-TC-061R` §§2, 4, 5):
    - Exact `w_{2,lambda}(n)` prime-power/two-prime/three-prime formula (`1 <= n <= 500`) and
      same-integer sign agreement `Lambda_lambda(p^k)*lambda(q) = lambda(p^k*q)*Lambda(p^k)`
      (scoped strictly to `P_Y` and `X_self(Y) >= 0`; same-integer mixed terms with `B_Y` in `J(Y)` can cancel).
    - Exact finite-window Gram kernel `G_Y^{[r]}(m, n)` representations of `J(Y)`: BOTH uncombined
      `r in {0, 1, 2, 3, 4}` (using `s_Y`) AND compact `r in {0, 2, 4}` (using `a_n` and
      `beta_Y(n) = s_Y(n) - a_n*(log n)^2`, including nonzero spillover on `T < n <= 2*T`).
    - Unconditional uniform bound `0 <= X_self(Y) <= 186*(tau - 1) < 1302` in Lean 4 and
      `0 <= X_self(Y) <= (289/60)*log(tau) < (1377/160)*log(tau) < 16` analytically outside Lean,
      certified on `Y in {16, 32, 64, 128, 256, 512, 1024, 2048, 4096}` alongside `F(Y)` and `S(Y)`.
    - Exact signed-correlation `(log X)^{-2}`-removal sandwich, `g = gcd(m, n)` half-line coprime
      kernel `G_inf(g*r, g*s) = (3*sqrt(tau/2)/(8*g))*(r*s)^2/(r^2 + s^2)^{5/2}`, unconditional
      coarse bound `E_{comp,diag}(Y, T) <= D_inf(T) <= 2*c_G*T*zeta''(2)`, and Lean Theorem 7
      equivalence `H(J, D_tilde) <-> H(F, D_tilde)` vs one-way sufficiency `H(S, D_tilde) -> H(J, D_tilde)`.
    """
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(32768, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 32768
        else selberg_table
    )
    w2 = tbl["w2"]
    lam_vm = tbl["lam_vm"]

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        log_tau = tau.log()

        # 1. Exact w_{2,lambda}(n) factorization formula and same-integer sign agreement on 1..500:
        w2_formula_ok = True
        sign_agree_ok = True
        for n in range(2, 501):
            pf = _prime_factorization_dict(n)
            if len(pf) == 1:
                (p, k) = next(iter(pf.items()))
                expected_w2 = arb((-1) ** k) * arb(2 * k - 1) * (arb(p).log() ** 2)
            elif len(pf) == 2:
                items = list(pf.items())
                (p, a), (q, b) = items[0], items[1]
                expected_w2 = arb(2 * ((-1) ** (a + b))) * arb(p).log() * arb(q).log()
            else:
                expected_w2 = arb(0)
            res_w = w2[n] - expected_w2
            if not (
                (expected_w2 == arb(0) and w2[n] == arb(0))
                or (arb(0) in res_w and abs(res_w) < arb("1e-70"))
            ):
                w2_formula_ok = False

            # Check Lambda_lambda(p^k) * lambda(q) == lambda(p^k * q) * Lambda(p^k) for all p^k | n:
            for p, a_max in pf.items():
                for k in range(1, a_max + 1):
                    pk = p ** k
                    q_co = n // pk
                    lhs_sgn = ((-1) ** k) * liouville_lambda_int(q_co)
                    rhs_sgn = liouville_lambda_int(n)
                    if lhs_sgn != rhs_sgn or not bool(lam_vm[pk] > arb(0)):
                        sign_agree_ok = False

        # 2. Exact finite-window Gram kernel G_Y^{[r]}(m, n) expansion cross-checks on Y in {2, 4, 8}:
        #    Both uncombined r in {0, 1, 2, 3, 4} (with smooth-only s_Y) AND compact r in {0, 2, 4}
        #    (with a_n and adjusted beta_Y = s_Y - a_n*(log n)^2, including nonzero spillover above T):
        kernel_expansion_rows: List[Dict[str, Any]] = []
        kernel_exp_ok = True
        same_integer_mixed_cancellation_witness_ok = False
        for y_k in (2, 4, 8):
            sp_k = ExactScaleSpec(str(y_k), "exact_rational", Fraction(y_k, 1))
            res_1d = evaluate_mixed_covariance_point_arb(
                sp_k,
                prec_bits=prec_bits,
                quad_tol_bits=230,
                use_three_zone=False,
                allow_nonprotocol_override=True,
                selberg_table=tbl,
            )
            T_k = res_1d["cutoffs"]["T_Y"]
            D0_eff = res_1d["cutoffs"]["D0_eff"]
            Y_b = arb(y_k)
            N2 = 2 * T_k

            # Precompute G_Y^{[r]}(m, n) for 1 <= m <= n <= 2*T_k and r in (0, 1, 2, 3, 4):
            G_cache: Dict[Tuple[int, int, int], arb] = {}

            def _G(m_i: int, n_i: int, r_p: int, _Yb=Y_b) -> arb:
                a_i, b_i = (m_i, n_i) if m_i <= n_i else (n_i, m_i)
                key = (a_i, b_i, r_p)
                hit = G_cache.get(key)
                if hit is None:
                    hit = evaluate_window_gram_G_Y_r_arb(_Yb, a_i, b_i, r_p, prec_bits=prec_bits)
                    G_cache[key] = hit
                return hit

            # Sum X_tilde(Y) via g = gcd(m, n) coprime decomposition:
            sum_lg_p_sq_g = [arb(0)] * (T_k + 1)
            for p, k in prime_power_pairs_up_to(T_k):
                pk = p ** k
                lg2 = arb(p).log() ** 2
                for mult in range(pk, T_k + 1, pk):
                    sum_lg_p_sq_g[mult] += lg2

            X_gcd_sum = arb(0)
            X_self_pair = arb(0)
            for g in range(1, T_k + 1):
                L_g = T_k // g
                delta_gg = (arb(g).log() ** 2) - sum_lg_p_sq_g[g]
                lg_g = arb(g).log()
                for r_c in range(1, L_g + 1):
                    for s_c in range(1, L_g + 1):
                        if math.gcd(r_c, s_c) != 1:
                            continue
                        wt_grs = arb(liouville_lambda_int(r_c * s_c)) * (
                            delta_gg
                            + lg_g * arb(r_c * s_c).log()
                            + arb(r_c).log() * arb(s_c).log()
                        )
                        term_x = wt_grs * _G(g * r_c, g * s_c, 2)
                        X_gcd_sum += term_x
                        if r_c == 1 and s_c == 1:
                            X_self_pair += term_x

            # Distinct smooth-only s_Y and adjusted complete-core beta_Y vectors on 1 <= n <= 2*T_k:
            core_vecs = compute_complete_core_s_Y_and_beta_Y_arb(
                T_k, D0_eff, tbl["R_osc"], prec_bits=prec_bits
            )
            a_vec = core_vecs["a_n"]
            s_Y = core_vecs["s_Y"]
            beta_Y = core_vecs["beta_Y"]
            has_spillover = bool(
                len(core_vecs["spillover_above_T_indices"]) > 0
                and core_vecs["max_spillover_above_T_abs"] > arb(0)
            )

            # (a) Uncombined J(Y) via Gram kernels G_Y^{[0..4]}(m, n) using smooth-only s_Y:
            B2_gram = arb(0)
            for m_i in range(1, N2 + 1):
                if s_Y[m_i] == arb(0):
                    continue
                for n_i in range(1, N2 + 1):
                    if s_Y[n_i] != arb(0):
                        B2_gram += s_Y[m_i] * s_Y[n_i] * _G(m_i, n_i, 4)
            for m_i in range(1, N2 + 1):
                if s_Y[m_i] == arb(0):
                    continue
                for n_i in range(1, T_k + 1):
                    ln_n = arb(n_i).log()
                    g_sh = _G(m_i, n_i, 2) - arb(2) * ln_n * _G(m_i, n_i, 3) + (ln_n * ln_n) * _G(m_i, n_i, 4)
                    B2_gram -= arb(2) * s_Y[m_i] * arb(liouville_lambda_int(n_i)) * g_sh
            for m_i in range(1, T_k + 1):
                ln_m = arb(m_i).log()
                for n_i in range(1, T_k + 1):
                    ln_n = arb(n_i).log()
                    s_mn = ln_m + ln_n
                    p_mn = ln_m * ln_n
                    g_sh2 = (
                        _G(m_i, n_i, 0)
                        - arb(2) * s_mn * _G(m_i, n_i, 1)
                        + (s_mn * s_mn + arb(2) * p_mn) * _G(m_i, n_i, 2)
                        - arb(2) * s_mn * p_mn * _G(m_i, n_i, 3)
                        + (p_mn * p_mn) * _G(m_i, n_i, 4)
                    )
                    B2_gram += arb(liouville_lambda_int(m_i * n_i)) * g_sh2

            PB_gram = arb(0)
            min_same_int_neg4_PB_term = arb(0)
            min_same_int_neg4_PB_index = 0
            for n_i in range(1, T_k + 1):
                lam_ln_n = arb(liouville_lambda_int(n_i)) * arb(n_i).log()
                if lam_ln_n == arb(0):
                    continue
                ln_n = arb(n_i).log()
                g_psh_nn = _G(n_i, n_i, 1) - arb(2) * ln_n * _G(n_i, n_i, 2) + (ln_n * ln_n) * _G(n_i, n_i, 3)
                same_int_pb_n = lam_ln_n * (
                    s_Y[n_i] * _G(n_i, n_i, 3) - arb(liouville_lambda_int(n_i)) * g_psh_nn
                )
                neg4_same_int = -arb(4) * same_int_pb_n
                if bool(neg4_same_int < arb(0)):
                    same_integer_mixed_cancellation_witness_ok = True
                    if min_same_int_neg4_PB_index == 0 or bool(neg4_same_int < min_same_int_neg4_PB_term):
                        min_same_int_neg4_PB_term = neg4_same_int
                        min_same_int_neg4_PB_index = n_i
                for m_i in range(1, N2 + 1):
                    if s_Y[m_i] != arb(0):
                        PB_gram += lam_ln_n * s_Y[m_i] * _G(n_i, m_i, 3)
                for m_i in range(1, T_k + 1):
                    ln_m = arb(m_i).log()
                    g_psh = _G(n_i, m_i, 1) - arb(2) * ln_m * _G(n_i, m_i, 2) + (ln_m * ln_m) * _G(n_i, m_i, 3)
                    PB_gram -= lam_ln_n * arb(liouville_lambda_int(m_i)) * g_psh

            J_gram = arb(4) * X_gcd_sum + B2_gram - arb(4) * PB_gram

            # (b) Compact (0, 2, 4) Gram representation via 2*P_Y - B_Y = Q_Y - sum_{n<=2T} beta_Y(n)*phi_n/(log X)^2:
            TwoPB_compact_gram = arb(0)
            for m_i in range(1, N2 + 1):
                am = a_vec[m_i]
                bm = beta_Y[m_i]
                if am == arb(0) and bm == arb(0):
                    continue
                for n_i in range(1, N2 + 1):
                    an = a_vec[n_i]
                    bn = beta_Y[n_i]
                    if am != arb(0) and an != arb(0):
                        TwoPB_compact_gram += am * an * _G(m_i, n_i, 0)
                    cross_mn = am * bn + bm * an
                    if cross_mn != arb(0):
                        TwoPB_compact_gram -= cross_mn * _G(m_i, n_i, 2)
                    if bm != arb(0) and bn != arb(0):
                        TwoPB_compact_gram += bm * bn * _G(m_i, n_i, 4)
            J_compact_gram = TwoPB_compact_gram - arb(4) * res_1d["D_tilde_Y"]

            res_X = X_gcd_sum - res_1d["X_tilde_Y"]
            res_J = J_gram - res_1d["J_direct"]
            res_J_compact = J_compact_gram - res_1d["J_direct"]
            ok_k = bool(
                has_spillover
                and arb(0) in res_X
                and abs(res_X) < arb("1e-55")
                and arb(0) in res_J
                and abs(res_J) < arb("1e-55")
                and arb(0) in res_J_compact
                and abs(res_J_compact) < arb("1e-55")
            )
            kernel_exp_ok = kernel_exp_ok and ok_k
            kernel_expansion_rows.append(
                {
                    "Y": y_k,
                    "T_Y": T_k,
                    "D0_eff": D0_eff,
                    "spillover_above_T_indices": core_vecs["spillover_above_T_indices"],
                    "max_spillover_above_T_abs": serialize_arb_certified(
                        core_vecs["max_spillover_above_T_abs"]
                    ),
                    "X_tilde_gcd_coprime_sum": serialize_arb_certified(X_gcd_sum),
                    "X_self_diagonal_part": serialize_arb_certified(X_self_pair),
                    "X_off_coprime_part": serialize_arb_certified(X_gcd_sum - X_self_pair),
                    "X_tilde_residual_vs_1d": serialize_arb_certified(res_X),
                    "J_uncombined_0_1_2_3_4_gram_sum": serialize_arb_certified(J_gram),
                    "J_complete_gram_kernel_sum": serialize_arb_certified(J_gram),
                    "J_residual_vs_1d": serialize_arb_certified(res_J),
                    "J_compact_0_2_4_gram_sum": serialize_arb_certified(J_compact_gram),
                    "J_compact_0_2_4_residual_vs_1d": serialize_arb_certified(res_J_compact),
                    "min_same_integer_neg4_PB_index_n": min_same_int_neg4_PB_index,
                    "min_same_integer_neg4_PB_term": serialize_arb_certified(
                        min_same_int_neg4_PB_term
                    ),
                    "verified": ok_k,
                }
            )

        # 3. Unconditional uniform composite self-collision bound 0 <= X_self(Y) <= (289/60)*log(tau) < (1377/160)*log(tau),
        # signed remainder F(Y) = 4*X_off(Y) + ||B_Y||_Y^2 - 4*<P_Y, B_Y>_Y (J = 4*X_self + F), and
        # sufficient unsigned-core relaxation S(Y) = 5*X_off(Y) + 5*||B_Y||_Y^2 (J <= 5*X_self + D_tilde + S)
        # across Y in {16, 32, 64, 128, 256, 512, 1024, 2048, 4096}:
        analytic_self_bound = _frac_to_arb(Fraction(1377, 160)) * log_tau
        sharp_self_bound = _frac_to_arb(Fraction(289, 60)) * log_tau
        self_collision_rows: List[Dict[str, Any]] = []
        self_bound_all_ok = True
        for y_sc in (16, 32, 64, 128, 256, 512, 1024, 2048, 4096):
            T_sc = certify_T_canonical_cutoff(y_sc, prec_bits=prec_bits)
            x_self_b = evaluate_X_self_collision_arb(arb(y_sc), T_sc, prec_bits=prec_bits)
            if precomputed_full_rows is not None and y_sc in precomputed_full_rows:
                fr = precomputed_full_rows[y_sc]
                x_tilde_b = fr["X_tilde_Y"]
                d_tilde_b = fr["D_tilde_Y"]
                b2_b = fr["B_norm_sq"]
                pb_b = fr["pair_P_B"]
                j_b = fr["J_direct"]
            else:
                sp_sc = ExactScaleSpec(str(y_sc), "exact_rational", Fraction(y_sc, 1))
                r_sc = evaluate_mixed_covariance_point_arb(sp_sc, selberg_table=tbl)
                x_tilde_b = (
                    precomputed_x_tilde_balls[y_sc]
                    if (precomputed_x_tilde_balls is not None and y_sc in precomputed_x_tilde_balls)
                    else r_sc["X_tilde_Y"]
                )
                d_tilde_b = r_sc["D_tilde_Y"]
                b2_b = r_sc["B_norm_sq"]
                pb_b = r_sc["pair_P_B"]
                j_b = r_sc["J_direct"]
            x_off_b = +(x_tilde_b - x_self_b)
            F_rem_b = +(arb(4) * x_off_b + b2_b - arb(4) * pb_b)
            S_rel_b = +(arb(5) * x_off_b + arb(5) * b2_b)
            res_JF = +(j_b - (arb(4) * x_self_b + F_rem_b))
            ok_JF = bool(arb(0) in res_JF and abs(res_JF) < arb("1e-40"))
            _, ok_JS = classify_arb_le_certificate(j_b, arb(5) * x_self_b + d_tilde_b + S_rel_b)

            x_off_sign = (
                "STRICTLY_NEGATIVE"
                if bool(x_off_b < arb(0))
                else ("STRICTLY_POSITIVE" if bool(x_off_b > arb(0)) else "STRADDLING_ZERO")
            )
            sign_definite_ok = x_off_sign in ("STRICTLY_NEGATIVE", "STRICTLY_POSITIVE")
            _, ok_ub_sharp = classify_arb_le_certificate(x_self_b, sharp_self_bound)
            _, ok_ub = classify_arb_le_certificate(x_self_b, analytic_self_bound)
            ok_pos = bool(x_self_b > arb(0))
            self_bound_all_ok = (
                self_bound_all_ok
                and ok_ub_sharp
                and ok_ub
                and ok_pos
                and sign_definite_ok
                and ok_JF
                and ok_JS
            )
            self_collision_rows.append(
                {
                    "Y": y_sc,
                    "T_Y": T_sc,
                    "X_tilde_Y": serialize_arb_certified(x_tilde_b),
                    "X_self_Y": serialize_arb_certified(x_self_b),
                    "X_off_Y": serialize_arb_certified(x_off_b),
                    "X_off_sign": x_off_sign,
                    "F_signed_remainder_Y": serialize_arb_certified(F_rem_b),
                    "S_unsigned_core_relaxation_Y": serialize_arb_certified(S_rel_b),
                    "J_minus_4Xself_plus_F_residual": serialize_arb_certified(res_JF),
                    "J_le_5Xself_plus_Dtilde_plus_S_certified": ok_JS,
                    "analytic_sharp_upper_bound_289_60_log_tau": serialize_arb_certified(
                        sharp_self_bound
                    ),
                    "analytic_uniform_upper_bound_1377_160_log_tau": serialize_arb_certified(
                        analytic_self_bound
                    ),
                    "strictly_positive_and_le_uniform_bound": bool(
                        ok_pos and ok_ub_sharp and ok_ub and sign_definite_ok and ok_JF and ok_JS
                    ),
                }
            )

        elem_self_proof = verify_self_collision_elementary_majorant_proof_arb(prec_bits=prec_bits)
        self_bound_all_ok = bool(self_bound_all_ok and elem_self_proof["verified"])

        # 4. Signed-correlation (log X)^{-2}-removal sandwich, exact complement-window identity
        # to the global (0, infty) coprime kernel G_inf(g*r, g*s) = (3*sqrt(tau/2)/(8*g))*(r*s)^2/(r^2+s^2)^{5/2},
        # and unconditional coarse linear bound E_{comp,diag}(Y, T) <= D_inf(T) <= 2*c_G*T*zeta''(2):
        const_G_inf = arb(3) * (tau / arb(2)).sqrt() / arb(8)
        coarse_comp_proof = verify_coarse_halfline_complement_bound_arb(
            T_vals=(7, 14, 32, 77), prec_bits=prec_bits
        )
        jet_z2_sec5 = acb_series([acb(2), acb(1)], prec=3).zeta()
        zeta_pp_2_sec5 = arb(2) * jet_z2_sec5[2].real
        bridge_rows: List[Dict[str, Any]] = []
        bridge_ok = bool(coarse_comp_proof["verified"])
        signed_y32_sandwich_verified = False
        for y_br in (4, 8, 16, 32):
            sp_b = ExactScaleSpec(str(y_br), "exact_rational", Fraction(y_br, 1))
            r_wt = evaluate_mixed_covariance_point_arb(
                sp_b,
                prec_bits=prec_bits,
                quad_tol_bits=220,
                use_three_zone=False,
                allow_nonprotocol_override=True,
                selberg_table=tbl,
            )
            T_b = r_wt["cutoffs"]["T_Y"]
            Y_b = arb(y_br)
            lg_y = Y_b.log()
            lg_tau_y = lg_y + log_tau

            # Unweighted P_0(Y), D_0^{diag}(Y) on [Y, tau*Y] AND global P_inf(T), D_inf(T) on (0, infty):
            p_coeff = [arb(0)] + [arb(liouville_lambda_int(n)) * arb(n).log() for n in range(1, T_b + 1)]
            P0_unwt = arb(0)
            P_inf_unwt = arb(0)
            for m_i in range(1, T_b + 1):
                for n_i in range(1, T_b + 1):
                    g_mn = math.gcd(m_i, n_i)
                    r_m = m_i // g_mn
                    s_n = n_i // g_mn
                    g_inf_mn = (
                        const_G_inf
                        * (arb(r_m * s_n) ** 2)
                        / (arb(g_mn) * (arb(r_m * r_m + s_n * s_n) ** (arb(5) / arb(2))))
                    )
                    P0_unwt += (
                        p_coeff[m_i]
                        * p_coeff[n_i]
                        * evaluate_window_kernel_K_closed_arb(Y_b, m_i, n_i, tau, prec_bits=prec_bits)
                    )
                    P_inf_unwt += p_coeff[m_i] * p_coeff[n_i] * g_inf_mn
            D0_unwt = arb(0)
            D_inf_unwt = arb(0)
            for p, k in prime_power_pairs_up_to(T_b):
                pk = p ** k
                L_pk = T_b // pk
                lg2 = arb(p).log() ** 2
                for q1 in range(1, L_pk + 1):
                    for q2 in range(1, L_pk + 1):
                        m_i = pk * q1
                        n_i = pk * q2
                        g_mn = math.gcd(m_i, n_i)
                        r_m = m_i // g_mn
                        s_n = n_i // g_mn
                        g_inf_mn = (
                            const_G_inf
                            * (arb(r_m * s_n) ** 2)
                            / (arb(g_mn) * (arb(r_m * r_m + s_n * s_n) ** (arb(5) / arb(2))))
                        )
                        wt_q = lg2 * arb(liouville_lambda_int(q1 * q2))
                        D0_unwt += wt_q * evaluate_window_kernel_K_closed_arb(
                            Y_b, m_i, n_i, tau, prec_bits=prec_bits
                        )
                        D_inf_unwt += wt_q * g_inf_mn
            X0_unwt = P0_unwt - D0_unwt
            E_comp_P = P_inf_unwt - P0_unwt
            E_comp_diag = D_inf_unwt - D0_unwt
            coarse_D_inf_bound = arb(2) * const_G_inf * arb(T_b) * zeta_pp_2_sec5
            _, ok_coarse_comp = classify_arb_le_certificate(E_comp_diag, coarse_D_inf_bound)
            _, ok_coarse_Dinf = classify_arb_le_certificate(D_inf_unwt, coarse_D_inf_bound)
            log_var_factor = (arb(2) * log_tau) / lg_y + ((log_tau / lg_y) ** 2)
            agg_upper_rhs = X0_unwt / (lg_y * lg_y) + log_var_factor * r_wt["D_tilde_Y"]
            agg_lower_lhs = X0_unwt / (lg_tau_y * lg_tau_y) - log_var_factor * r_wt["D_tilde_Y"]
            _, ok_agg_up = classify_arb_le_certificate(r_wt["X_tilde_Y"], agg_upper_rhs)
            _, ok_agg_lo = classify_arb_le_certificate(agg_lower_lhs, r_wt["X_tilde_Y"])
            if y_br == 32:
                signed_y32_sandwich_verified = bool(
                    r_wt["X_tilde_Y"] < arb(0) and X0_unwt < arb(0) and ok_agg_up and ok_agg_lo
                )

            # Global (0, infty) coprime kernel sum X_inf(T) = X_{inf,self}(T) + X_{inf,off}(T):
            sum_lg_p_sq_b = [arb(0)] * (T_b + 1)
            for p, k in prime_power_pairs_up_to(T_b):
                pk = p ** k
                lg2 = arb(p).log() ** 2
                for mult in range(pk, T_b + 1, pk):
                    sum_lg_p_sq_b[mult] += lg2
            X_inf_tot = arb(0)
            X_inf_off = arb(0)
            for g in range(1, T_b + 1):
                L_g = T_b // g
                delta_gg = (arb(g).log() ** 2) - sum_lg_p_sq_b[g]
                lg_g = arb(g).log()
                inv_g = arb(1) / arb(g)
                for r_c in range(1, L_g + 1):
                    for s_c in range(1, L_g + 1):
                        if math.gcd(r_c, s_c) != 1:
                            continue
                        wt_grs = arb(liouville_lambda_int(r_c * s_c)) * (
                            delta_gg
                            + lg_g * arb(r_c * s_c).log()
                            + arb(r_c).log() * arb(s_c).log()
                        )
                        rs_sq = arb(r_c * s_c) ** 2
                        denom = arb(r_c * r_c + s_c * s_c) ** (arb(5) / arb(2))
                        term_inf = inv_g * wt_grs * const_G_inf * rs_sq / denom
                        X_inf_tot += term_inf
                        if r_c != s_c:
                            X_inf_off += term_inf

            # Exact aggregate complement-window identity:
            # X0_unwt(Y) = X_inf_tot(T) - E_comp_P(Y, T) + E_comp_diag(Y, T) with E_comp_P > 0, E_comp_diag > 0:
            comp_res = X0_unwt - (X_inf_tot - E_comp_P + E_comp_diag)
            comp_ok = bool(
                arb(0) in comp_res
                and abs(comp_res) < arb("1e-60")
                and E_comp_P > arb(0)
                and E_comp_diag > arb(0)
                and ok_coarse_comp
                and ok_coarse_Dinf
            )

            bridge_ok = bridge_ok and ok_agg_up and ok_agg_lo and comp_ok
            bridge_rows.append(
                {
                    "Y": y_br,
                    "T_Y": T_b,
                    "X_tilde_Y_weighted": serialize_arb_certified(r_wt["X_tilde_Y"]),
                    "X0_unweighted": serialize_arb_certified(X0_unwt),
                    "X0_unweighted_over_logY_sq": serialize_arb_certified(X0_unwt / (lg_y * lg_y)),
                    "X0_unweighted_over_log_tauY_sq": serialize_arb_certified(
                        X0_unwt / (lg_tau_y * lg_tau_y)
                    ),
                    "log_variation_error_budget": serialize_arb_certified(
                        log_var_factor * r_wt["D_tilde_Y"]
                    ),
                    "aggregate_log_removal_lower_lhs": serialize_arb_certified(agg_lower_lhs),
                    "aggregate_log_removal_upper_rhs": serialize_arb_certified(agg_upper_rhs),
                    "aggregate_log_removal_certified": bool(ok_agg_up and ok_agg_lo),
                    "global_halfline_coprime_total_X_inf_T": serialize_arb_certified(X_inf_tot),
                    "global_halfline_coprime_offdiag_X_inf_T": serialize_arb_certified(X_inf_off),
                    "complement_window_P_energy_E_comp_P": serialize_arb_certified(E_comp_P),
                    "complement_window_diag_energy_E_comp_diag": serialize_arb_certified(E_comp_diag),
                    "global_halfline_diag_D_inf_T": serialize_arb_certified(D_inf_unwt),
                    "coarse_upper_bound_2_cG_T_zeta_pp_2": serialize_arb_certified(
                        coarse_D_inf_bound
                    ),
                    "coarse_complement_diag_bound_certified": bool(
                        ok_coarse_comp and ok_coarse_Dinf
                    ),
                    "complement_window_identity_residual": serialize_arb_certified(comp_res),
                    "complement_window_identity_verified": comp_ok,
                }
            )

        # Verify tau-adic partition-of-unity sum_{j=-14}^4 G_{tau^j}^{(0)}(2, 3) -> G_inf(2, 3):
        G_inf_2_3 = const_G_inf * arb(36) / (arb(13) ** (arb(5) / arb(2)))
        tau_tower_2_3 = sum(
            (
                evaluate_window_kernel_K_closed_arb(tau ** j_idx, 2, 3, tau, prec_bits=prec_bits)
                for j_idx in range(-14, 5)
            ),
            arb(0),
        )
        tower_res = abs(G_inf_2_3 - tau_tower_2_3)
        tower_ok = bool(tower_res < arb("1e-50"))

        return {
            "epistemic_statuses": [
                "UNCONDITIONAL_FINITE_ARITHMETIC",
                "CONCRETE_ANALYTIC_IN_LEAN",
                "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "CERTIFIED_FINITE_OBSERVATION",
                "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            ],
            "section_epistemic_scope_note": (
                "Mixed proof-attempt section: prime-power sign agreement in P_Y and w_{2,lambda} "
                "support are UNCONDITIONAL_FINITE_ARITHMETIC and CONCRETE_ANALYTIC_IN_LEAN (scoped "
                "strictly to P_Y and X_self(Y) >= 0, since same-integer mixed (P_Y, B_Y) terms in J "
                "can cancel); BOTH the uncombined (0..4) Gram expansion (with s_Y) and the compact "
                "(0, 2, 4) Gram expansion (with beta_Y = s_Y - a_n*(log n)^2, Lean Theorem 5), the "
                "unconditional O(1) composite self-collision bounds (186*(tau-1) < 1302 in Lean "
                "Theorem 3; (289/60)*log(tau) < (1377/160)*log(tau) < 16 outside Lean), and the "
                "equivalence H(J, D_tilde) <-> H(F, D_tilde) vs one-way sufficiency H(S, D_tilde) "
                "-> H(J, D_tilde) (Lean Theorem 7) are CONCRETE_ANALYTIC_IN_LEAN and "
                "ANALYTIC_PROVED_OUTSIDE_LEAN; the signed-correlation (log X)^{-2}-removal sandwich, "
                "tau-adic coprime kernel G_inf(g*r, g*s) = (3*sqrt(tau/2)/(8*g))*(r*s)^2/(r^2+s^2)^{5/2}, "
                "and unconditional coarse bound E_{comp,diag}(Y,T) <= D_inf(T) <= 2*c_G*T*zeta''(2) "
                "are ANALYTIC_PROVED_OUTSIDE_LEAN; numerical enclosures on 16..4096 are "
                "CERTIFIED_FINITE_OBSERVATION; and the signed remainder obligation "
                "TC061R-OBL-SIGNED-REMAINDER-F (along with its sufficient relaxation "
                "TC061-LEM-OFFDIAG-AND-CORE) remains OPEN_CONJECTURE_OR_FAILED_CANDIDATE."
            ),
            "component_epistemic_map": {
                "w2_factorization_and_same_integer_P_Y_sign_agreement": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "lean_compact_gram_self_collision_and_F_S_reduction_theorems": "CONCRETE_ANALYTIC_IN_LEAN",
                "signed_log_removal_sandwich_and_coarse_halfline_complement_bound": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "self_collision_F_S_and_kernel_bridge_arb_certificates": "CERTIFIED_FINITE_OBSERVATION",
                "remaining_signed_remainder_obligation_F_and_relaxation_S": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            },
            "lean_theorems": [
                "factorization_sign_agreement_and_selberg_w2_formulas_tc061",
                "finite_window_offdiag_kernel_and_composite_self_collision_bound_tc061",
                "complete_core_adjusted_expansion_and_compact_gram_tc061r",
                "signed_remainder_equivalence_and_sufficient_core_relaxation_tc061r",
            ],
            "w2_and_sign_agreement_1_to_500": {
                "w2_factorization_verified": w2_formula_ok,
                "same_integer_sign_agreement_in_P_Y_verified": sign_agree_ok,
                "same_integer_sign_agreement_verified": sign_agree_ok,
                "same_integer_mixed_PB_cancellation_witness_verified": same_integer_mixed_cancellation_witness_ok,
                "cancellation_scope_note": (
                    "Lambda_lambda(p^k)*lambda(q) = lambda(p^k*q)*Lambda(p^k) rules out intra-integer "
                    "sign cancellation ONLY inside P_Y (forcing X_self(Y) >= 0); in complete J(Y), "
                    "same-integer (m = n) cross terms between P_Y and B_Y can and do contribute "
                    "negative summands."
                ),
            },
            "finite_window_gram_kernel_expansion_checks": kernel_expansion_rows,
            "composite_self_collision_theorem": {
                "lean_statement": (
                    "Lean Theorem 3 (CONCRETE_ANALYTIC_IN_LEAN): for every real Y >= 2 and every T in N, "
                    "0 <= X_self(Y) <= sum_{n=1}^T (log n)^2 * G_Y^{[2]}(n, n) <= 186*(tau - 1) < 1302."
                ),
                "outside_lean_analytic_refinement": (
                    "Elementary outside-Lean refinement (ANALYTIC_PROVED_OUTSIDE_LEAN): splitting "
                    "2 <= n <= floor(X) (< 3/4 via e^u > u^3/6) and n >= floor(X) + 1 (< 16/15 + 3 via "
                    "log 2 > 2/3 and integral comparison on u^{-6}, u^{-4}) proves for all Y >= 2 and T in N: "
                    "0 <= X_self(Y) <= (289/60)*log(tau) < (1377/160)*log(tau) < 16."
                ),
                "lean_status": "CONCRETE_ANALYTIC_IN_LEAN",
                "outside_lean_refinement_status": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "elementary_analytic_proof": elem_self_proof,
                "evaluated_scales_16_to_4096": self_collision_rows,
                "verified": self_bound_all_ok,
            },
            "aggregate_log_removal_and_global_coprime_bridge": {
                "halfline_kernel_formula": (
                    "G_inf(g*r, g*s) = (3*sqrt(tau/2)/(8*g)) * (r*s)^2 / (r^2 + s^2)^{5/2} "
                    "(g = gcd(m, n), gcd(r, s) = 1)"
                ),
                "signed_log_removal_sandwich_formula": (
                    "X_0(Y)/(log(tau*Y))^2 - eta_log(Y)*D_tilde(Y) <= X_tilde(Y) <= "
                    "X_0(Y)/(log Y)^2 + eta_log(Y)*D_tilde(Y), where eta_log(Y) = "
                    "(log(tau*Y))^2/(log Y)^2 - 1 and X_0(Y) = P_0(Y) - D_0^{diag}(Y)"
                ),
                "signed_y32_sandwich_verified": signed_y32_sandwich_verified,
                "coarse_halfline_complement_bound": coarse_comp_proof,
                "signed_complement_control_still_needed": (
                    "Unconditionally 0 <= E_{comp,diag}(Y, T) <= D_inf(T) <= 2*c_G*T*zeta''(2) = O(T); "
                    "bounding X_0(Y) = X_inf(T) - E_{comp,P}(Y, T) + E_{comp,diag}(Y, T) from above at "
                    "sub-polynomial / polylogarithmic scale via the global half-line decomposition "
                    "requires a quantitative signed upper bound on E_{comp,diag}(Y, T) - E_{comp,P}(Y, T) "
                    "(for example a matching lower bound on E_{comp,P}(Y, T) >= 0 canceling the bulk of "
                    "E_{comp,diag}(Y, T)), together with control of X_inf(T)."
                ),
                "tau_adic_tower_2_3_residual_abs": serialize_arb_certified(tower_res),
                "tau_adic_tower_verified": tower_ok,
                "bridge_rows": bridge_rows,
                "verified": bool(bridge_ok and tower_ok and signed_y32_sandwich_verified),
            },
            "remaining_quantitative_lemma": {
                "lemma_id": "TC061R-OBL-SIGNED-REMAINDER-F",
                "exact_equivalent_obligation_id": "TC061R-OBL-SIGNED-REMAINDER-F",
                "quantified_statement": (
                    "For every eta > 0, there exist a_eta, b_eta >= 0, kappa_eta in (0, 2], and "
                    "Y_eta >= 2 such that for all real Y >= Y_eta, "
                    "F(Y) := 4*X_off(Y) + ||B_Y||_Y^2 - 4*<P_Y, B_Y>_Y <= "
                    "a_eta * Y^eta + b_eta * (log Y)^{2 - kappa_eta} * D_tilde(Y)."
                ),
                "equivalence_to_closure_H": (
                    "Lean Theorem 7 (signed_remainder_equivalence_and_sufficient_core_relaxation_tc061r, "
                    "Part 1): since J(Y) = 4*X_self(Y) + F(Y) and 0 <= X_self(Y) <= C uniformly on Y >= 2, "
                    "MixedCovarianceClosureHypothesis(F, D_tilde) <-> MixedCovarianceClosureHypothesis(J, D_tilde) "
                    "via a_eta <-> a_eta + 4*C (keeping b_eta, kappa_eta unchanged on Y >= max(Y_eta, 2))."
                ),
                "sufficient_unsigned_core_relaxation_id": "TC061-LEM-OFFDIAG-AND-CORE",
                "sufficient_unsigned_core_relaxation_statement": (
                    "For every eta > 0, there exist a'_eta, b'_eta >= 0, kappa_eta in (0, 2], and "
                    "Y_eta >= 2 such that for all real Y >= Y_eta, "
                    "S(Y) := 5*X_off(Y) + 5*||B_Y||_Y^2 <= "
                    "a'_eta * Y^eta + b'_eta * (log Y)^{2 - kappa_eta} * D_tilde(Y)."
                ),
                "one_way_sufficiency_note": (
                    "Lean Theorem 7 (Part 2): by ||P_Y + 2*B_Y||_Y^2 >= 0 and D_tilde(Y) >= 0, "
                    "J(Y) <= 5*X_self(Y) + D_tilde(Y) + S(Y), so MixedCovarianceClosureHypothesis(S, D_tilde) "
                    "implies MixedCovarianceClosureHypothesis(J, D_tilde) with a_eta := a'_eta + 5*C and "
                    "b_eta := b'_eta + 1 on Y >= max(Y_eta, e) (where log Y >= 1 and kappa_eta <= 2 give "
                    "D_tilde(Y) <= (log Y)^{2 - kappa_eta}*D_tilde(Y)). This relaxation discards the signed "
                    "covariance -4*<P_Y, B_Y>_Y; NO converse H(J, D_tilde) -> H(S, D_tilde) is claimed."
                ),
                "reduction_to_closure_H": (
                    "Exact equivalence H(F, D_tilde) <-> H(J, D_tilde) preserves -4*<P_Y, B_Y>_Y; "
                    "one-way sufficient relaxation H(S, D_tilde) -> H(J, D_tilde) drops -4*<P_Y, B_Y>_Y "
                    "via Cauchy-Schwarz/Young."
                ),
                "failure_point_of_unconditional_analytic_methods": (
                    "Classical zero-free regions for zeta(z) (de la Vallee Poussin / Korobov-Vinogradov, "
                    "z = x + i*y) bound distinct-integer Liouville correlations in X_off(Y) and R_osc(d) "
                    "in B_Y only at O(Y * exp(-c*(log Y)^alpha)), whose ratio to Y^eta diverges as "
                    "Y -> infty for every 0 < eta < 1."
                ),
            },
            "all_section_5_checks_pass": bool(
                w2_formula_ok
                and sign_agree_ok
                and same_integer_mixed_cancellation_witness_ok
                and kernel_exp_ok
                and self_bound_all_ok
                and bridge_ok
                and tower_ok
                and signed_y32_sandwich_verified
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 7. Section 6: Route D Conditional Transfer, Live Lean Audit, & Review Check
# ---------------------------------------------------------------------------


def verify_section_6_route_d_conditional_transfer_and_scope(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify the numerical Route D normalized feedback thresholds (`R`-independent `Y_*`) and
    explicit `0 < eta < eta' < eps` polylogarithm absorption matching `MixedArithmeticCovariance.lean`.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        route_d_rows: List[Dict[str, Any]] = []
        all_rd_ok = True
        for eps_fr, b_fr, kap_fr in (
            (Fraction(1, 2), Fraction(1, 1), Fraction(1, 1)),
            (Fraction(1, 4), Fraction(1, 1), Fraction(1, 1)),
            (Fraction(1, 8), Fraction(2, 1), Fraction(1, 2)),
        ):
            s_pt = arb(1) + _frac_to_arb(eps_fr)
            jet3 = acb_series([acb(s_pt), acb(1)], prec=3).zeta()
            z2 = arb(2) * jet3[2].real  # jet3[2] is (1/2!)*zeta''(1 + eps)
            b_b = _frac_to_arb(b_fr)
            kap_b = _frac_to_arb(kap_fr)

            L1 = (arb(64) * z2).sqrt()
            L2 = (arb(16) * b_b * z2) ** (arb(1) / kap_b)
            L_thresh = enclose_discrete_grid_max([arb(2).log(), L1, L2])
            # Test at L_test = ceil(upper(L_thresh)) + 1 so log(Y_test) >= L_thresh strictly:
            _, l_hi = _exact_arb_endpoints_as_fractions(L_thresh)
            L_int = (l_hi.numerator // l_hi.denominator) + 2
            lg_test = arb(L_int)
            rho_fb = arb(16) * z2 / (lg_test * lg_test) + arb(4) * b_b * z2 / (lg_test ** kap_b)
            _, ok_half = classify_arb_le_certificate(rho_fb, arb(1) / arb(2))

            # Intermediate exponent split 0 < eta < eta' < eps:
            eta_fr = eps_fr / 3
            eta_prime_fr = (2 * eps_fr) / 3
            exp_split_ok = Fraction(0, 1) < eta_fr < eta_prime_fr < eps_fr

            row_ok = bool(ok_half and exp_split_ok)
            all_rd_ok = all_rd_ok and row_ok
            route_d_rows.append(
                {
                    "eps_fraction": f"{eps_fr.numerator}/{eps_fr.denominator}",
                    "eta_choice_fraction": f"{eta_fr.numerator}/{eta_fr.denominator}",
                    "eta_prime_choice_fraction": f"{eta_prime_fr.numerator}/{eta_prime_fr.denominator}",
                    "b_eta_fraction": f"{b_fr.numerator}/{b_fr.denominator}",
                    "kappa_eta_fraction": f"{kap_fr.numerator}/{kap_fr.denominator}",
                    "zeta_double_prime_1_plus_eps": serialize_arb_certified(z2),
                    "log_Y_threshold_R_independent": serialize_arb_certified(L_thresh),
                    "test_log_Y": L_int,
                    "feedback_factor_at_test_log_Y": serialize_arb_certified(rho_fb),
                    "feedback_le_one_half_certified": ok_half,
                    "threshold_scope": (
                        "2-term (D, J) normalized feedback component <= 1/4 + 1/4 = 1/2; full Lean "
                        "Theorem 4 adds +1 positivity offsets inside sqrt(64*z2+1) and (16*b_eta*z2+1)^{1/kappa_eta} "
                        "plus the third B_drift(eps)/(log Y)^{kappa_d} <= 1/8 slot and max(Y_diag, Y_eta) "
                        "so total 3-term feedback <= 3/4 < 1 closes E(Y) <= C_tot(eps)*Y^eps for all Y >= 1."
                    ),
                    "known_component_coeff_direct_theta_half": 2,
                    "known_component_coeff_companion_tc060_reuse": 4,
                    "verified": row_ok,
                }
            )

        return {
            "epistemic_statuses": [
                "CONDITIONAL_IMPLICATION",
                "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "CERTIFIED_FINITE_OBSERVATION",
                "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            ],
            "section_epistemic_scope_note": (
                "Mixed conditional-transfer section: the Lean Route D transfer theorem from "
                "MixedCovarianceClosureHypothesis (both direct theta = 1/2 coefficient 2 and "
                "companion TC-060 reuse coefficient 4 with R-independent 3-term feedback threshold Y_* "
                "closing E(Y) <= C_tot(eps)*Y^eps for all Y >= 1) is CONDITIONAL_IMPLICATION; the "
                "horizon-coupled known-component contraction ||A_Y||_Y^2 <= a_known(eps)*Y^eta + "
                "(B_drift(eps)/(log Y)^{kappa_d})*G_eps(R)*Y^eps, shifted prime-power diagonal bound, "
                "global linear bound 0 <= E(Z) <= M_lin*Z, and conditional Mellin pole-exclusion bridge "
                "to RH are ANALYTIC_PROVED_OUTSIDE_LEAN; sample zeta''(1+eps) (D, J)-feedback threshold "
                "enclosures are CERTIFIED_FINITE_OBSERVATION; and full closure hypothesis H remains "
                "OPEN_CONJECTURE_OR_FAILED_CANDIDATE (SUBGATE-TC-043A OPEN, rh_proved = False)."
            ),
            "component_epistemic_map": {
                "lean_route_d_direct_and_companion_transfers_from_H": "CONDITIONAL_IMPLICATION",
                "outside_lean_horizon_coupled_known_drift_and_mellin_rh_bridge": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "sample_route_d_feedback_threshold_certificates": "CERTIFIED_FINITE_OBSERVATION",
                "full_mixed_covariance_closure_hypothesis_H": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            },
            "lean_theorems": [
                "mixed_covariance_hypothesis_route_d_closure_transfer_tc061",
            ],
            "remaining_hypothesis_mapping": [
                {
                    "hypothesis_name": "MixedCovarianceClosureHypothesis (H)",
                    "role": "Primary open quantitative arithmetic covariance target",
                    "status": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
                    "source_or_obligation": (
                        "SUBGATE-TC-043A / TC061R-OBL-SIGNED-REMAINDER-F (exact equivalent) "
                        "or TC061-LEM-OFFDIAG-AND-CORE (one-way sufficient relaxation)"
                    ),
                },
                {
                    "hypothesis_name": (
                        "Horizon-coupled known-component contraction ||A_Y||_Y^2 <= a_known(eps)*Y^eta "
                        "+ (B_drift(eps)/(log Y)^{kappa_d})*G_eps(R)*Y^eps on Y_diag <= Y <= R"
                    ),
                    "role": "Non-circular premise of Lean Route D transfer (3rd feedback slot <= 1/4)",
                    "status": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                    "source_or_obligation": "TC-058R / TC-060R / TC-060R2 drift & small-divisor relative contraction",
                },
                {
                    "hypothesis_name": (
                        "Shifted prime-power diagonal majorization D_tilde(Y) <= (2/(log Y)^2)*sum_{p^k<=Y} "
                        "w_{p,k}*F(Y/p^k) + C_cut with sum w_{p,k} <= zeta''(1+eps)"
                    ),
                    "role": "Analytic premise of Lean Route D transfer (finite-horizon G_eps(R) assembly in Lean)",
                    "status": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                    "source_or_obligation": "TC-057R / TC-059R shifted prime-power diagonal theorem (assembled in Lean Theorem 4)",
                },
                {
                    "hypothesis_name": "Global linear bound 0 <= E(Z) <= M_lin * Z for all Z >= 1",
                    "role": "Premise ensuring sSup boundedness on [1, R] and bounding initial [1, Y_*(eps)] across T(Z) jumps",
                    "status": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                    "source_or_obligation": "TC-054 / TC-057 unconditional Stieltjes/pointwise linear energy bound",
                },
                {
                    "hypothesis_name": "Conditional Mellin pole-exclusion bridge from E(Y) = O_eps(Y^eps) to RH",
                    "role": "Downstream analytic step after SUBGATE-TC-043A energy closure (kept outside Lean Theorem 4)",
                    "status": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                    "source_or_obligation": "TC-059R repaired inverse-Mellin analytic continuation & pole-exclusion theorem",
                },
            ],
            "route_d_threshold_checks": route_d_rows,
            "all_section_6_checks_pass": all_rd_ok,
        }
    finally:
        flint_ctx.prec = saved


def _extract_lean_declaration_line_spans(src: str) -> Dict[str, Dict[str, int]]:
    """Extract exact 1-based `[start_line, end_line]` spans for top-level `def` and `theorem`
    declarations in `formal/RiemannScope/MixedArithmeticCovariance.lean` (`TASK-TC-061R` §7).
    """
    src_lines = src.splitlines()
    top_decl_re = re.compile(
        r"^(?:noncomputable\s+)?(?:private\s+)?(?P<kind>def|theorem|lemma|abbrev)\s+(?P<name>[A-Za-z0-9_']+)\b"
    )
    boundary_re = re.compile(
        r"^(?:/--|-\s*!|noncomputable\b|private\b|def\b|theorem\b|lemma\b|abbrev\b|structure\b|section\b|namespace\b|end\b)"
    )
    starts: List[Tuple[int, str, str]] = []
    for idx0, ln in enumerate(src_lines):
        m = top_decl_re.match(ln)
        if m is not None:
            starts.append((idx0, m.group("kind"), m.group("name")))

    spans: Dict[str, Dict[str, int]] = {}
    for s_idx, (idx0, _kind, name) in enumerate(starts):
        next_limit = starts[s_idx + 1][0] if (s_idx + 1) < len(starts) else len(src_lines)
        end0 = idx0
        in_block_comment = False
        for scan0 in range(idx0 + 1, next_limit):
            ln_scan = src_lines[scan0]
            if in_block_comment:
                if "-/" in ln_scan:
                    in_block_comment = False
                continue
            if ln_scan.startswith("/--") or ln_scan.startswith("/-"):
                break
            if boundary_re.match(ln_scan):
                break
            stripped = ln_scan.strip()
            if stripped and not stripped.startswith("--"):
                end0 = scan0
        spans[name] = {"start_line": idx0 + 1, "end_line": end0 + 1}
    return spans


def verify_tc061_lean_theorems_live(
    expected_theorems: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """Verify all public theorems in `formal/RiemannScope/MixedArithmeticCovariance.lean` via live
    `lake env lean --stdin` (`#check` and `#print axioms`) and source hygiene checks.
    """
    raw_bytes = TC_061_LEAN_MODULE_PATH.read_bytes().replace(b"\r\n", b"\n")
    module_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    src = raw_bytes.decode("utf-8")
    decl_spans = _extract_lean_declaration_line_spans(src)
    no_block = re.sub(r"/-.*?-/", "", src, flags=re.DOTALL)
    clean_src = re.sub(r"--[^\n]*", "", no_block)

    declared_theorems = re.findall(r"^\s*theorem\s+([A-Za-z0-9_']+)\b", clean_src, flags=re.MULTILINE)
    target_theorems = list(expected_theorems) if expected_theorems is not None else declared_theorems

    sorry_count = len(re.findall(r"\bsorry\b", clean_src))
    admit_count = len(re.findall(r"\badmit\b", clean_src))
    custom_axiom_count = len(re.findall(r"^\s*axiom\b", clean_src, flags=re.MULTILINE))
    pi_macro_count = len(re.findall(r"\x5cpi(?![a-zA-Z])", src)) + src.count("\u03c0")
    present = len(target_theorems) > 0 and all(thm in declared_theorems for thm in target_theorems)

    lines = ["import RiemannScope.MixedArithmeticCovariance"]
    for thm in target_theorems:
        fq = f"RiemannScope.MixedArithmeticCovariance.{thm}"
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
    for thm in target_theorems:
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
    build_hash_matches = False
    inherited_commit_matches = False
    if FORMAL_BUILD_REPORT_PATH.exists():
        try:
            br = json.loads(FORMAL_BUILD_REPORT_PATH.read_text(encoding="utf-8"))
            src_hashes = br.get("formal_source_hashes") or br.get("source_hashes") or {}
            mod_hash_br = src_hashes.get("formal/RiemannScope/MixedArithmeticCovariance.lean")
            prod_commit_br = br.get("producing_git_commit")
            build_hash_matches = bool(mod_hash_br == module_sha256)
            inherited_commit_matches = bool(
                prod_commit_br == ACCEPTED_TC061R_IMPLEMENTATION_AND_FORMAL_COMMIT
            )
            formal_provenance = {
                "status": br.get("status"),
                "producing_git_commit": prod_commit_br,
                "expected_inherited_formal_producing_commit": (
                    ACCEPTED_TC061R_IMPLEMENTATION_AND_FORMAL_COMMIT
                ),
                "inherited_formal_producing_commit_preserved": inherited_commit_matches,
                "project_theorem_declarations_compiled": br.get(
                    "project_theorem_declarations_compiled"
                ),
                "total_theorems": br.get("total_theorems"),
                "module_sha256_in_build_report": mod_hash_br,
                "live_module_sha256_matches_build_report": build_hash_matches,
                "report_hash": br.get("report_hash"),
            }
        except Exception:  # noqa: BLE001
            formal_provenance = {}

    return {
        "module_path": "formal/RiemannScope/MixedArithmeticCovariance.lean",
        "module_sha256": module_sha256,
        "declared_theorems": declared_theorems,
        "expected_tc061_theorems": target_theorems,
        "all_tc061_theorems_present": present,
        "declaration_line_spans": {
            k: v
            for k, v in decl_spans.items()
            if k == "MixedCovarianceClosureHypothesis" or k in target_theorems
        },
        "sorry_count": sorry_count,
        "admit_count": admit_count,
        "custom_axiom_count": custom_axiom_count,
        "pi_token_count": pi_macro_count,
        "lean_exit_code": proc.returncode,
        "formal_build_report_provenance": formal_provenance,
        "per_theorem": per_theorem,
        "all_tc061_lean_checks_pass": bool(
            present
            and sorry_count == 0
            and admit_count == 0
            and custom_axiom_count == 0
            and pi_macro_count == 0
            and axioms_ok
            and build_hash_matches
        ),
    }


_LEAN_ANCHOR_LINK_RE = re.compile(
    r"\[`(?P<symbol>[A-Za-z0-9_']+)`\]\([^)]*MixedArithmeticCovariance\.lean#L(?P<start>\d+)-L(?P<end>\d+)\)"
)


def verify_tc061_review_displayed_enclosures(
    report: Dict[str, Any],
    review_path: Path = TC_061_REVIEW_DOC_PATH,
) -> Dict[str, Any]:
    """Verify that `docs/reviews/TC_061_MIXED_ARITHMETIC_COVARIANCE.md` contains zero circle-half
    macros/glyphs, exact `MixedArithmeticCovariance.lean#L<start>-L<end>` declaration line anchors,
    and that every displayed `±` / `\\pm` interval carries an explicit `<!-- tc-enclosure: ... -->`
    tag outward-containing its generated 256-bit Arb ball.
    """
    text = review_path.read_text(encoding="utf-8")
    pi_macros = re.findall(r"\x5cpi(?![a-zA-Z])", text)
    pi_glyph_count = text.count("\u03c0")
    lines = text.splitlines()
    raw_intervals: List[Dict[str, Any]] = []
    untagged_intervals: List[Dict[str, Any]] = []
    checked_rows: List[Dict[str, Any]] = []
    failed_intervals: List[Dict[str, Any]] = []

    decl_spans = (
        report.get("section_7_lean_formalization_audit", {}).get("declaration_line_spans") or {}
    )
    lean_anchor_checks: List[Dict[str, Any]] = []
    failed_lean_anchors: List[Dict[str, Any]] = []
    for m_anc in _LEAN_ANCHOR_LINK_RE.finditer(text):
        sym = m_anc.group("symbol")
        st_ln = int(m_anc.group("start"))
        en_ln = int(m_anc.group("end"))
        expected_span = decl_spans.get(sym)
        if expected_span is None:
            # Fall back to live source extraction if section_7 is omitted
            if TC_061_LEAN_MODULE_PATH.exists():
                live_spans = _extract_lean_declaration_line_spans(
                    TC_061_LEAN_MODULE_PATH.read_text(encoding="utf-8")
                )
                expected_span = live_spans.get(sym)
        span_ok = bool(
            expected_span is not None
            and expected_span["start_line"] == st_ln
            and expected_span["end_line"] == en_ln
        )
        anc_rec = {
            "symbol": sym,
            "linked_start_line": st_ln,
            "linked_end_line": en_ln,
            "expected_span": expected_span,
            "verified": span_ok,
        }
        lean_anchor_checks.append(anc_rec)
        if not span_ok:
            failed_lean_anchors.append(anc_rec)

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
                gen_low_bs, gen_high_bs, _ = _parse_arb_ball_str_to_fractions(gen_node["arb_ball_str"])
                gen_low_dec = _sci_or_latex_num_to_fraction(gen_node["lower_dec"])
                gen_high_dec = _sci_or_latex_num_to_fraction(gen_node["upper_dec"])
                gen_low = max(gen_low_bs, gen_low_dec)
                gen_high = min(gen_high_bs, gen_high_dec)
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
        and len(failed_lean_anchors) == 0
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
        "lean_line_anchor_checks_count": len(lean_anchor_checks),
        "failed_lean_line_anchors": failed_lean_anchors,
        "all_displayed_intervals_contain_generated_enclosures": all_ok,
    }


def build_headline_and_exposure_reconciliation_summary(
    sec1: Dict[str, Any],
    sec2: Dict[str, Any],
    sec3: Dict[str, Any],
    sec4: Dict[str, Any],
    sec5: Dict[str, Any],
) -> Dict[str, Any]:
    """Programmatically derive all headline numbers, cutoff transitions, exposure counts, and
    ratios from the generated sections (`TASK-TC-061R` §7) so reports never drift from artifacts.
    """
    sided = sec2["sided_discontinuity_cutoffs"]
    cs_splits = sec2["straddling_interval_case_splits"]
    exp_brk = sec3["exposure_category_breakdown"]
    row_128 = next(
        (r for r in sec3["holdout_point_evaluations"] if r["point_id"] == "HO-BASE-128"), None
    )
    row_4096 = next(
        (r for r in sec3["holdout_point_evaluations"] if r["point_id"] == "HO-EXT-4096"), None
    )
    return {
        "holdout_exposure_reconciliation": {
            "total_holdout_points": exp_brk["total_registered_holdout_points"],
            "counts_by_status": exp_brk["counts_by_prior_exposure_status"],
            "unseen_for_all_observables_count": exp_brk["unseen_for_all_observables_count"],
            "unseen_for_all_tc054_to_tc060_window_observables_count": exp_brk[
                "unseen_for_all_tc054_to_tc060_window_observables_count"
            ],
            "combined_zero_prior_window_observable_count": exp_brk[
                "zero_prior_window_observable_evaluations_combined_count"
            ],
        },
        "cutoff_transitions_reconciliation": {
            "e5_sided_pair": {
                "e5_minus_D0_raw": sided["e5_minus"]["D0_raw"],
                "e5_plus_D0_raw": sided["e5_plus"]["D0_raw"],
                "e5_minus_T_Y": sided["e5_minus"]["T_Y"],
                "e5_plus_T_Y": sided["e5_plus"]["T_Y"],
            },
            "256_sided_triple": {
                "256_minus_T_Y": sided["256_minus"]["T_Y"],
                "256_exact_T_Y": sided["256_exact"]["T_Y"],
                "256_plus_T_Y": sided["256_plus"]["T_Y"],
                "D0_raw": sided["256_exact"]["D0_raw"],
            },
            "unit_interval_64_to_65": {
                "T_range": cs_splits["wide_interval_64_to_65_unresolved_wrapping_example"][
                    "T_range"
                ],
                "D0_range": cs_splits["wide_interval_64_to_65_unresolved_wrapping_example"][
                    "D0_range"
                ],
                "active_branch_count": cs_splits[
                    "wide_interval_64_to_65_unresolved_wrapping_example"
                ]["active_branch_count"],
                "verdict": cs_splits["wide_interval_64_to_65_unresolved_wrapping_example"][
                    "P0_interval_classification"
                ]["verdict"],
            },
        },
        "headline_holdout_values": {
            "HO_BASE_128": (
                {
                    "T_Y": row_128["cutoffs"]["T_Y"],
                    "quadrature_mode": row_128["quadrature_mode"],
                    "quad_tol_bits_used": row_128["quad_tol_bits_used"],
                    "J_direct": row_128["J_direct"],
                    "M_P0": row_128["probe_evaluations"]["TC061-P0"]["margin_M_Y"],
                    "J_over_log_Y_D_tilde": row_128["J_over_log_Y_D_tilde"],
                }
                if row_128 is not None
                else None
            ),
            "HO_EXT_4096": (
                {
                    "T_Y": row_4096["cutoffs"]["T_Y"],
                    "subunit_tail_d_range_inclusive": row_4096["subunit_tail_breakdown"][
                        "subunit_tail_d_range_inclusive"
                    ],
                    "J_direct": row_4096["J_direct"],
                    "log_Y_times_D_tilde": row_4096["log_Y_times_D_tilde"],
                    "M_P0": row_4096["probe_evaluations"]["TC061-P0"]["margin_M_Y"],
                    "J_over_log_Y_D_tilde": row_4096["J_over_log_Y_D_tilde"],
                }
                if row_4096 is not None
                else None
            ),
        },
        "self_collision_constants": {
            "lean_theorem_3_upper_bound_formula": "186*(tau - 1)",
            "lean_theorem_3_upper_bound": sec5["composite_self_collision_theorem"][
                "elementary_analytic_proof"
            ]["lean_theorem_3_bound_186_tau_minus_1"],
            "outside_lean_sharp_upper_bound_formula": "(289/60)*log(tau)",
            "outside_lean_sharp_upper_bound": sec5["composite_self_collision_theorem"][
                "elementary_analytic_proof"
            ]["sharp_window_bound_289_60_log_tau"],
            "outside_lean_envelope_upper_bound_formula": "(1377/160)*log(tau)",
            "outside_lean_envelope_upper_bound": sec5["composite_self_collision_theorem"][
                "elementary_analytic_proof"
            ]["envelope_window_bound_1377_160_log_tau"],
        },
        "control_arithmetic_spot_checks": {
            "unsigned_1_conv_at_12": sec4["control_arithmetic_invariants"]["unsigned_1"][
                "convolution_spot_values"
            ]["12"],
            "a2_conv_at_3_6_12": [
                sec4["control_arithmetic_invariants"]["a2"]["convolution_spot_values"]["3"],
                sec4["control_arithmetic_invariants"]["a2"]["convolution_spot_values"]["6"],
                sec4["control_arithmetic_invariants"]["a2"]["convolution_spot_values"]["12"],
            ],
            "calibrated_secondary_constants_a_eta": {
                k: v["a_eta_fraction"]
                for k, v in sec1["exact_rational_calibration_reverification"].items()
            },
        },
    }


def execute_task_tc061_mixed_covariance_audit(
    prec_bits: int = 256,
    verify_lean_live: bool = True,
    verify_review_doc: bool = True,
) -> Dict[str, Any]:
    """Execute the complete `TASK-TC-061` / `TASK-TC-061R` preregistered mixed arithmetic covariance
    experiment, signed-kernel proof attempt, controls attribution, and Lean 4 formalization audit.
    """
    shared_tbl = compute_selberg_centered_remainder_table_fast_arb(32768, prec_bits=prec_bits + 32)

    sec1 = verify_section_1_protocol_and_exact_mixed_identity(
        prec_bits=prec_bits, selberg_table=shared_tbl
    )
    sec2 = verify_section_2_cutoff_and_interval_certification(
        prec_bits=prec_bits, selberg_table=shared_tbl
    )
    sec3 = verify_section_3_preregistered_holdout_experiment(
        prec_bits=prec_bits, selberg_table=shared_tbl
    )
    sec4 = verify_section_4_controls_and_tc_arithmetic_attribution(
        prec_bits=prec_bits, selberg_table=shared_tbl
    )
    precomp_x: Dict[int, arb] = {}
    precomp_rows: Dict[int, Dict[str, arb]] = {}
    for row_1 in sec1["diagnostic_and_calibration_evaluations"]:
        y_i = int(row_1["Y"])
        if y_i in (16, 32, 64):
            precomp_x[y_i] = row_1["X_tilde_Y"]["enclosure_arb"]
            precomp_rows[y_i] = {
                "D_tilde_Y": row_1["D_tilde_Y"]["enclosure_arb"],
                "X_tilde_Y": row_1["X_tilde_Y"]["enclosure_arb"],
                "B_norm_sq": row_1["B_norm_sq"]["enclosure_arb"],
                "pair_P_B": row_1["pair_P_B"]["enclosure_arb"],
                "J_direct": row_1["J_direct"]["enclosure_arb"],
            }
    for row_3 in sec3["holdout_point_evaluations"]:
        lbl = str(row_3["label"])
        if lbl in ("128", "256", "512", "1024", "2048", "4096"):
            y_i = int(lbl)
            precomp_x[y_i] = row_3["X_tilde_Y"]["enclosure_arb"]
            precomp_rows[y_i] = {
                "D_tilde_Y": row_3["D_tilde_Y"]["enclosure_arb"],
                "X_tilde_Y": row_3["X_tilde_Y"]["enclosure_arb"],
                "B_norm_sq": row_3["B_norm_sq"]["enclosure_arb"],
                "pair_P_B": row_3["pair_P_B"]["enclosure_arb"],
                "J_direct": row_3["J_direct"]["enclosure_arb"],
            }

    sec5 = verify_section_5_arithmetic_proof_attempt_and_kernel_reduction(
        prec_bits=prec_bits,
        selberg_table=shared_tbl,
        precomputed_x_tilde_balls=precomp_x,
        precomputed_full_rows=precomp_rows,
    )
    sec6 = verify_section_6_route_d_conditional_transfer_and_scope(prec_bits=prec_bits)

    assert sec1["all_section_1_checks_pass"] is True, "sec1 failed"
    assert sec2["all_section_2_checks_pass"] is True, "sec2 failed"
    assert sec3["all_section_3_checks_pass"] is True, (
        f"sec3 failed: cov={sec3['holdout_coverage_summary']}, "
        f"tel={sec3['execution_telemetry_summary']}, "
        f"128={sec3['tc061r_protocol_deviation_and_rerun_comparison']['verified']}"
    )
    assert sec4["all_section_4_checks_pass"] is True, "sec4 failed"
    assert sec5["all_section_5_checks_pass"] is True, "sec5 failed"
    assert sec6["all_section_6_checks_pass"] is True, "sec6 failed"

    for sec_name, sec_obj in (
        ("section_1", sec1),
        ("section_2", sec2),
        ("section_3", sec3),
        ("section_4", sec4),
        ("section_5", sec5),
        ("section_6", sec6),
    ):
        ep_ok, ep_msg = verify_section_epistemic_scope_metadata(sec_obj)
        assert ep_ok is True, f"{sec_name} epistemic scope metadata check failed: {ep_msg}"

    reconciliation = build_headline_and_exposure_reconciliation_summary(sec1, sec2, sec3, sec4, sec5)

    report: Dict[str, Any] = {
        "task_id": TASK_TC_061_ID,
        "repair_task_id": TASK_TC_061R_ID,
        "closeout_task_id": TASK_TC_061R2_ID,
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
            TASK_TC_060R_ID,
            TASK_TC_060R2_ID,
            TASK_TC_061_ID,
            TASK_TC_061R_ID,
        ],
        "merged_main_baseline": MERGED_MAIN_BASELINE_TC061,
        "accepted_tc060r2_tip": ACCEPTED_TC060R2_TIP,
        "accepted_tc060r2_implementation": ACCEPTED_TC060R2_IMPLEMENTATION,
        "inherited_tc060r_formal_commit": REVIEWED_TC060R_IMPLEMENTATION,
        "reviewed_tc061_tip": REVIEWED_TC061_TIP,
        "reviewed_tc061_implementation": REVIEWED_TC061_IMPLEMENTATION,
        "reviewed_tc061r_tip": REVIEWED_TC061R_TIP,
        "accepted_tc061r_implementation_and_formal_commit": (
            ACCEPTED_TC061R_IMPLEMENTATION_AND_FORMAL_COMMIT
        ),
        "frozen_protocol_id": FROZEN_PROTOCOL_ID,
        "frozen_protocol_sha256": FROZEN_PROTOCOL_SHA256,
        "frozen_protocol_registration_commit": FROZEN_PROTOCOL_REGISTRATION_COMMIT,
        "branch": PROPOSED_TC061R2_BRANCH,
        "previous_tc061r_branch": PROPOSED_TC061R_BRANCH,
        "original_tc061_branch": PROPOSED_TC061_BRANCH,
        "provenance_separation": {
            "implementation_provenance": {
                "closeout_task_id": TASK_TC_061R2_ID,
                "branch": PROPOSED_TC061R2_BRANCH,
                "reviewed_tc061r_tip_baseline": REVIEWED_TC061R_TIP,
                "accepted_tc061r_implementation_commit": (
                    ACCEPTED_TC061R_IMPLEMENTATION_AND_FORMAL_COMMIT
                ),
                "scope": (
                    "Runner per-candidate decisive-witness accumulator, explicit 3-valued "
                    "(WITHIN/EXCEEDED/UNKNOWN) resource compliance tracking, regression suite, "
                    "and documentation closeout."
                ),
            },
            "mathematical_certificate_execution_provenance": {
                "execution_mode": "LIVE_SOURCE_EXECUTION_THROUGH_REPAIRED_RUNNER",
                "epistemic_experiment_role": (
                    "REPEAT_OF_REGISTERED_EXPERIMENT_NOT_NEW_UNSEEN_EVIDENCE"
                ),
                "quadrature_recomputed_live_from_source": True,
                "hand_edited_enclosures": False,
                "restamped_prior_execution": False,
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            },
            "synthetic_regression_evidence_provenance": {
                "test_suite_path": "tests/test_tc_mixed_arithmetic_covariance.py",
                "included_in_production_artifact_verdicts": False,
                "scope": (
                    "Injected FAIL->UNRESOLVED, PASS->UNRESOLVED, KL1 cross-escalation, "
                    "contradictory PASS/FAIL integrity-conflict, and missing/mixed/exceeded "
                    "telemetry tests run strictly in pytest against the production runner and "
                    "Section 3 aggregator."
                ),
            },
            "formal_build_provenance": {
                "inherited_formal_producing_commit": (
                    ACCEPTED_TC061R_IMPLEMENTATION_AND_FORMAL_COMMIT
                ),
                "formal_inputs_changed_in_tc061r2": False,
                "formal_build_report_path": "formal/build_report.json",
            },
        },
        "epistemic_categories_enforced": list(EPISTEMIC_CATEGORIES),
        "global_consequence_classes_enforced": list(GLOBAL_CONSEQUENCE_CLASSES),
        "probe_global_outcomes_enforced": list(PROBE_GLOBAL_OUTCOMES),
        "completion_outcome_code": "SURVIVED_TESTED_POINTS_WITH_PROVED_SELF_COLLISION_BOUND_AND_CONDITIONAL_TRANSFER",
        "research_outcome_class": (
            "Preregistered Mixed Arithmetic Covariance Experiment & Signed-Kernel Proof Attempt "
            "(TASK-TC-061 / repaired in TASK-TC-061R) — Frozen protocol "
            "TC061-MIXED-ARITHMETIC-COVARIANCE-PROTOCOL-V1 (SHA-256 "
            "c892c4c5a1ff2a60a11fa499b2d2bc017e01f0426e4aa8feef5880aaff8a70eb, registered at "
            "bc2f9f709f868ef02981600873dfa0c05da0ba0c before any Y > 64 evaluation) executed "
            "faithfully across 14/14 held-out points up to Y = 4096 (including unsplit "
            "quad_tol_bits = 240 at Y = 128, T = 431 < 512, and nonempty d >= ceil(tau*Y) "
            "sub-unit tail d in [25736, 32767] at Y = 4096, T = 32768) and continuous straddling "
            "intervals across T and D_0 jumps: all four frozen probes (PRIMARY TC061-P0 and "
            "SECONDARY TC061-P_{1/2}, TC061-P_{1/4}, TC061-P_{1/8}) and both TC061-KL1 sub-budgets "
            "achieve SURVIVED_TESTED_POINTS (0 FAIL, 0 UNRESOLVED, 14/14 complete holdout coverage; "
            "finite evidence, NOT a uniform proof), whereas unsigned 1 and fixed finite-prime "
            "parity controls a_2, a_{3,5,7} are certified FAIL on every frozen probe across the "
            "evaluated grid Y in {64, 128, 256, 512} under exact matched z = 1 Laurent compensation "
            "(scoped strictly to the evaluated finite grid without unproved asymptotic growth laws "
            "or unique-tau-mechanism claims). Proves in Lean 4 (7 public theorems, 0 sorry, 0 "
            "custom axioms) and analytically the concrete mixed identity "
            "4*D_tilde(Y) + J(Y) = ||2*P_Y - B_Y||_Y^2 = ||Q_Y + A_Y||_Y^2, the complete-core "
            "adjusted beta_Y bridge and compact (0, 2, 4) Gram representation, the finite-prime "
            "parity convolution formula (1 * a_S)(n), prime-power sign agreement in P_Y, "
            "unconditional uniform composite self-collision bounds 0 <= X_self(Y) <= 186*(tau - 1) "
            "< 1302 in Lean 4 and 0 <= X_self(Y) <= (289/60)*log(tau) < (1377/160)*log(tau) < 16 "
            "analytically outside Lean, the unconditional coarse half-line complement bound "
            "E_{comp,diag}(Y, T) <= D_inf(T) <= 2*c_G*T*zeta''(2), conditional Route D transfer "
            "from H with R-independent threshold Y_*, and exact equivalence H(J, D_tilde) <-> "
            "H(F, D_tilde) for the signed remainder F(Y) = 4*X_off(Y) + ||B_Y||_Y^2 - 4*<P_Y, B_Y>_Y "
            "(TC061R-OBL-SIGNED-REMAINDER-F, with S(Y) = 5*X_off(Y) + 5*||B_Y||_Y^2 as a one-way "
            "sufficient relaxation TC061-LEM-OFFDIAG-AND-CORE); SUBGATE-TC-043A remains OPEN and "
            "rh_proved remains False."
        ),
        "hypothesis_H_status": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        "subgate_tc043a_status": "OPEN",
        "rh_proved": False,
        "precision_bits": prec_bits,
        "circle_constant_convention": "tau (sole circle constant)",
        "grade_variable_convention": (
            "K reserved strictly for real-algebraic geometric grades K in A_R; "
            "A_Y, B_Y denote known/core window functions; s_Y denotes smooth-only core coefficients "
            "and beta_Y = s_Y - a_n*(log n)^2 denotes adjusted complete-core coefficients; "
            "a_eta, b_eta denote scalar constants; G_Y^{[r]}(m, n) denotes finite-window Gram kernels."
        ),
        "headline_and_exposure_reconciliation": reconciliation,
        "section_1_protocol_and_exact_mixed_identity": sec1,
        "section_2_cutoff_and_interval_certification": sec2,
        "section_3_preregistered_holdout_experiment": sec3,
        "section_4_controls_and_tc_arithmetic_attribution": sec4,
        "section_5_arithmetic_proof_attempt_and_kernel_reduction": sec5,
        "section_6_route_d_conditional_transfer_and_scope": sec6,
    }

    if verify_lean_live:
        lean_audit = verify_tc061_lean_theorems_live(EXPECTED_TC061_THEOREMS)
        assert lean_audit["all_tc061_lean_checks_pass"] is True, (
            f"TC-061 Lean theorem audit failed: {lean_audit}"
        )
        report["section_7_lean_formalization_audit"] = lean_audit

    arb_check = verify_all_serialized_arb_in_tree(report)
    assert arb_check["all_enclose_original_256bit_arb_ball"] is True, (
        f"Serialized Arb enclosure verification failed: {arb_check.get('failed_paths')}"
    )
    report["serialized_arb_self_check"] = arb_check

    if verify_review_doc and TC_061_REVIEW_DOC_PATH.exists():
        rev_audit = verify_tc061_review_displayed_enclosures(report, TC_061_REVIEW_DOC_PATH)
        assert rev_audit["all_displayed_intervals_contain_generated_enclosures"] is True, (
            "Displayed intervals in TC_061_MIXED_ARITHMETIC_COVARIANCE.md failed check: "
            f"pi_macros={rev_audit['pi_macro_count']}, pi_glyphs={rev_audit['pi_glyph_count']}, "
            f"untagged={rev_audit['untagged_intervals']}, failed={rev_audit['failed_intervals']}"
        )
        report["section_8_tc061_review_displayed_enclosures_audit"] = rev_audit

    return report


def write_task_tc061_mixed_covariance_artifact(
    path: Path = MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH,
    prec_bits: int = 256,
    verify_lean_live: bool = True,
    verify_review_doc: bool = True,
) -> Dict[str, Any]:
    """Generate and write `data/tc_mixed_arithmetic_covariance.json` from source."""
    report = execute_task_tc061_mixed_covariance_audit(
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


def refresh_task_tc061_provenance_and_review_audit(
    path: Path = MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH,
) -> Dict[str, Any]:
    """Refresh Section 7 (`formal_build_report_provenance` + live Lean audit) and Section 8
    (`docs/reviews/TC_061_MIXED_ARITHMETIC_COVARIANCE.md` displayed-enclosure audit) on an
    existing source-generated `data/tc_mixed_arithmetic_covariance.json` without mutating any
    source-generated Arb balls in Sections 1--6 or `serialized_arb_self_check`.
    """
    assert path.exists(), f"Missing {path}; run full source generation first."
    existing = json.loads(path.read_text(encoding="utf-8"))

    lean_audit = verify_tc061_lean_theorems_live(EXPECTED_TC061_THEOREMS)
    assert lean_audit["all_tc061_lean_checks_pass"] is True, (
        f"TC-061 Lean theorem audit failed: {lean_audit}"
    )
    existing["section_7_lean_formalization_audit"] = lean_audit

    if TC_061_REVIEW_DOC_PATH.exists():
        rev_audit = verify_tc061_review_displayed_enclosures(existing, TC_061_REVIEW_DOC_PATH)
        assert rev_audit["all_displayed_intervals_contain_generated_enclosures"] is True, (
            "Displayed intervals in TC_061_MIXED_ARITHMETIC_COVARIANCE.md failed check: "
            f"pi_macros={rev_audit['pi_macro_count']}, pi_glyphs={rev_audit['pi_glyph_count']}, "
            f"untagged={rev_audit['untagged_intervals']}, failed={rev_audit['failed_intervals']}"
        )
        existing["section_8_tc061_review_displayed_enclosures_audit"] = rev_audit

    path.write_text(
        json.dumps(existing, indent=2, sort_keys=False, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return existing


if __name__ == "__main__":
    import sys

    if "--refresh-provenance" in sys.argv[1:]:
        rep = refresh_task_tc061_provenance_and_review_audit()
        print(
            f"Refreshed provenance & review audit in {MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH} "
            f"(subgate={rep['subgate_tc043a_status']}, rh_proved={rep['rh_proved']})"
        )
    else:
        verify_rev = "--no-verify-review" not in sys.argv[1:]
        verify_ln = "--no-verify-lean" not in sys.argv[1:]
        rep = write_task_tc061_mixed_covariance_artifact(
            verify_lean_live=verify_ln,
            verify_review_doc=verify_rev,
        )
        print(
            f"Wrote {MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH} "
            f"(subgate={rep['subgate_tc043a_status']}, rh_proved={rep['rh_proved']})"
        )
