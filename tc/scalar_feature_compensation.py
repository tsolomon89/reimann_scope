r"""
TASK-TC-065: Arithmetic Scalar-Feature Compensation Across Squarefree Cores
toward SUBGATE-TC-043A (EPIC-TC-042).

Implements, verifies, and certifies in 256-bit FLINT/Arb outward-rounded ball arithmetic:
- Circle constant convention: `tau` exclusively (`0` circle-half macros or glyphs).
- Grade variable convention: `K` reserved strictly for real-algebraic geometric grades in `A_R`
  (`0` non-grade `K` underscore identifiers); complex arguments written `z = x + i*y` (`x, y` real,
  critical line `x = 1/2`); analytic scale `Y >= 2` kept a real variable throughout.
- Artifact key disambiguation: `damped_core_defect_Y` denotes the surviving damped target
  `D_core(Y) := S_core^scal(Y) - 4*||V_Y||_Y^2 = ||U_Y||_Y^2 - 4*||V_Y||_Y^2 - J_A(Y) = S_core(Y) - 4*J_B(Y)`.
  It is strictly distinct from the inherited TC-064 artifact key `D_core_Y`, which denotes the
  core Gram diagonal `sum_a (||A_a||_Y^2 - 4*||B_a^feat||_Y^2)`.

Sections:
1. Section 1 - Preserved Upstream Protocols/Payloads, Frozen TC-065 Protocol, & Premise Table:
   - Verifies immutability of all 5 frozen protocols (`TC-061`, `TC-062`, `TC-063`, `TC-064`, `TC-065`)
     and byte-for-byte preservation of all `3,208` (`TC-061`), `885` (`TC-062`), `688` (`TC-063R`),
     and `686` (`TC-064`) upstream certified Arb records.
   - Records the complete premise chain to RH (`PROVED_IN_LEAN`, `PROVED_ANALYTICALLY_OUTSIDE_LEAN`,
     `CONDITIONAL_PROVED_IN_LEAN`, `CERTIFIED_FINITE_OBSERVATION`, `REFUTED_CANDIDATE`, `OPEN`),
     including the direct Route D transfer for `E_lambda - 4*D_tilde` using only `PREM-04..06`,
     the nonzero `z -> 1` limit of the finite Euler multiplier `M_S(z)` vs zero limit of the
     modified Liouville quotient `L_{a_S}(z)`, and general window-base `w_0 > 1` scope.
2. Section 2 - Exact TC-064 Seen-Scale Reproduction (`SEEN_DERIVED_FROM_TC064_CERTIFICATES`),
   Exact Algebraic Identities (`EXACT_ALGEBRA`), & Independent Cross-Checks:
   - Reproduces `damped_core_defect_Y` at `Y in {512, 576, 960, 1408}` directly from exact recorded
     outward decimal endpoints in `data/tc_squarefree_core_correlation.json`, separating `||U_Y||^2`,
     `4*||V_Y||^2`, `||U_Y||^2 - 4*||V_Y||^2`, and the diagonal allowance `J_A(Y)`.
   - Exhaustively verifies paired-station partition `Omega_2(T) sqcup Phi_2(T)`, `sum_{Omega_2} lambda = 0`,
     odd prime-power channel vanishing for `p >= 3, 2*p^k > T`, odd square-lift parity criterion,
     pointwise telescoping of `openCoreSmoothCoeffS` on `1 <= n <= T`, `sum_{e|n} |w_{2,lambda}(e)| = (log n)^2`,
     and large-prime station disjointness above `floor(sqrt(T))`.
   - Independently cross-checks the unified 1D compensation evaluator against `TC-064` and `TC-061`
     evaluators at `Y in {16, 32, 64}` (`INDEPENDENT_DIRECT_NUMERICAL_VALIDATION`).
3. Section 3 - Seen-Scale Route 5 & Route 6 Mechanism Discovery & Controls (`SEEN_DISCOVERY`):
   - Evaluates Route 5 (`S1` unweighted `w = 1`, `S2` Mertens contractive `r = 1/2`, `S3` single-channel
     `2`-adic contractive `r = 1/2`, `S4` certified real-interval pointwise oracle residual lower bound)
     and Route 6 (`E1` full-cutoff vs paired-fringe, `E2` station-disjoint large-prime `p > sqrt(T)`,
     `E3` bare-Liouville vs shifted-dilation `E_lambda - 4*D_tilde`) on already-seen scales
     `Y in {16, 32, 64, 128, 256, 512}`, plus the unsigned `a(n) = 1` scaling control and
     explicitly labeled hybrid finite-prime-flip diagnostic `a_{3}(n)`.
4. Section 4 - Preregistered Unseen Validation (`8` Unseen Points + `3` Continuous Intervals / `10` Cells):
   - Evaluates all `8` unseen points and `3` cutoff-sensitive continuous intervals with exact binary
     evaluation-domain coverage (`TC-062R4` standard), complete Route 5 & Route 6 residual budgets,
     operator-norm and fringe-bound certificates, escalation ladder, and fail-closed outcome aggregation.
5. Section 5 - Live Lean 4 Audit, Review Consistency Verifier, & Honest Gate Accounting:
   - Audits `formal/RiemannScope/ScalarFeatureCompensation.lean` (`17` public defs, `5` public theorems,
     `0` sorry/admit/custom axioms, `845` total compiled theorems in `formal/build_report.json`),
     verifies review enclosures & anchors, and preserves `SUBGATE-TC-043A = OPEN`, `rh_proved = False`.
"""

from __future__ import annotations

import copy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

from flint import acb, arb, ctx as flint_ctx

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tc.canonical_theta_correlation_bound import (
    EPIC_TC_042_ID,
    REPO_ROOT,
    serialize_arb_certified,
    verify_all_serialized_arb_in_tree,
)
from tc.coupled_scale_energy_bootstrap import (
    _frac_to_arb,
    _tau_arb,
    prime_power_pairs_up_to,
)
from tc.dyadic_chain_correlation_regularity import (
    DYADIC_CHAIN_ARTIFACT_PATH,
    EXPECTED_TC061_ARTIFACT_SHA256,
    EXPECTED_TC062_ARTIFACT_SHA256,
    _get_git_head_commit,
    dyadic_chain_exponents_J_u,
    odd_chain_parts_O_T,
    verify_frozen_tc063_protocol_immutability,
)
from tc.dyadic_power_lift_primitive_correlation import PARENT_SUBGATE_ID
from tc.joint_prime_dilation_signed_remainder import (
    JOINT_PRIME_DILATION_ARTIFACT_PATH,
    _audit_serialized_margin_verdict_tc062,
    _evaluate_branch_domain_admissibility_tc062,
    _parse_serialized_arb_enclosure_tc062,
    _serialized_union_contains_branch_tc062,
    derive_exact_interval_cutoff_partition,
    prime_valuation_v_p,
    verify_frozen_tc062_protocol_immutability,
)
from tc.liouville_square_dilation import (
    _ARB_BACKTICK_INTERVAL_RE,
    _LATEX_PM_INTERVAL_RE,
    _TC_ENCLOSURE_TAG_RE,
    _exact_arb_endpoints_as_fractions,
    _parse_arb_ball_str_to_fractions,
    _resolve_report_path_with_param_check,
    liouville_lambda_int,
)
from tc.mixed_arithmetic_covariance import (
    CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME,
    CERTIFICATION_INTEGRITY_CONFLICT_VERDICT,
    ExactScaleSpec,
    MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH,
    _measure_process_rss_megabytes,
    aggregate_section_resource_compliance,
    certify_exact_scale_cutoffs,
    classify_probe_margin_arb,
    compute_complete_core_s_Y_and_beta_Y_arb,
    compute_selberg_centered_remainder_table_fast_arb,
    evaluate_fixed_cutoff_on_Y_ball_arb,
    evaluate_mixed_covariance_point_arb,
    evaluate_point_resource_compliance,
    strip_enclosure_arb_for_json,
    verify_frozen_protocol_immutability,
)
from tc.signed_dilation_arithmetic_energy import (
    FORMAL_BUILD_REPORT_PATH,
    verify_section_epistemic_scope_metadata,
)
from tc.squarefree_core_correlation import (
    EXPECTED_TC063R_ARTIFACT_SHA256,
    SQUAREFREE_CORE_ARTIFACT_PATH,
    SQUAREFREE_CORE_PROTOCOL_PATH,
    canonical_cutoff_T_of_Y_exact,
    evaluate_squarefree_core_observables_matrix_free_arb,
    odd_squarefree_core_and_root,
    odd_squarefree_cores_C_T,
    verify_frozen_tc064_protocol_immutability,
)

TASK_TC_065_ID = "TASK-TC-065"
PROPOSED_TC065_BRANCH = "task/tc-065-arithmetic-scalar-feature-compensation"
ACCEPTED_TC064R_TIP = "9c46ca4c3232afb9eef8b7871cd0fc365cdc3440"
REVIEWED_TC064_TIP = "7e61dfff4cd6a2f78471182a990c495970fda2b5"
REVIEWED_MAIN_BASELINE_TC065 = "bf3babfb7857e41c0ea53235d82a48181cefee84"
FORMAL_TC065_PRODUCER_COMMIT = "1c767f9e01d77c85c7c10ad6f1f9373409d83af7"

FROZEN_TC065_PROTOCOL_ID = "TC065-SCALAR-FEATURE-COMPENSATION-PROTOCOL-V1"
FROZEN_TC065_PROTOCOL_REGISTRATION_COMMIT = "bcddccf451e33486db42d013d1a645c319cb3bd8"
FROZEN_TC065_PROTOCOL_SHA256 = "2d1e9e5758f7f5a0192ee68d6251a801065dae78c2a2344632780e3a5ead10e7"

SCALAR_FEATURE_PROTOCOL_PATH = (
    REPO_ROOT / "data" / "tc_scalar_feature_compensation_protocol.json"
)
SCALAR_FEATURE_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_scalar_feature_compensation.json"
)
TC_065_REVIEW_DOC_PATH = (
    REPO_ROOT / "docs" / "reviews" / "TC_065_ARITHMETIC_SCALAR_FEATURE_COMPENSATION.md"
)
SCALAR_FEATURE_LEAN_REL = "formal/RiemannScope/ScalarFeatureCompensation.lean"
SCALAR_FEATURE_LEAN_PATH = REPO_ROOT / SCALAR_FEATURE_LEAN_REL

EXPECTED_TC065_THEOREMS: List[str] = [
    "damped_core_defect_and_closure_equivalence_tc065",
    "paired_station_partition_divisor_synthesis_and_telescoping_tc065",
    "arithmetic_synthesis_hilbert_budget_operator_norm_and_obstructions_tc065",
    "coupled_mode_expansion_uniform_fringe_bounds_and_orthogonality_tc065",
    "bare_liouville_shifted_dilation_closure_and_euler_limit_tc065",
]

EXPECTED_TC065_PUBLIC_DEFS: List[str] = [
    "coreTotalScalarProfileU",
    "coreTotalFeatureVectorV",
    "coreScalarDiagJA",
    "coreFeatureDiagJB",
    "coreDistinctScalarSumS",
    "dampedCoreDefectD",
    "canonicalDampedCoreDefectD",
    "pairedPrimePowerSumP",
    "pairedOpenCoreOscO",
    "pairedCutoffFringeScalarPhi",
    "fullFeatureVectorG",
    "fringeFeatureVectorG",
    "pointwiseSynthesisOp",
    "activePairedPrimePowers",
    "splitFeatureHighV",
    "splitFeatureLowV",
    "finiteEulerMultiplierM",
]

PRESCRIBED_TC065_INTERVAL_SPLITS: Dict[str, Tuple[Fraction, Fraction]] = {
    "interval_19_85_to_20_30_across_e3_and_T43_T44": (
        Fraction(397, 20),
        Fraction(203, 10),
    ),
    "interval_101_60_to_102_45_across_sqrtT18_and_p163": (
        Fraction(508, 5),
        Fraction(2049, 20),
    ),
    "interval_1558_50_to_1558_60_across_tau4_and_T9794": (
        Fraction(3117, 2),
        Fraction(7793, 5),
    ),
}

REQUIRED_TC065_INTERVAL_UNION_BRANCH_PAIRS: Tuple[Tuple[str, str], ...] = (
    ("union_E_Y", "E_Y"),
    ("union_D_tilde_Y", "D_tilde_Y"),
    ("union_log_Y_times_D_tilde", "log_Y_times_D_tilde"),
    ("union_U_norm_sq_Y", "U_norm_sq_Y"),
    ("union_four_V_norm_sq_Y", "four_V_norm_sq_Y"),
    ("union_J_A_Y", "J_A_Y"),
    ("union_damped_core_defect_Y", "damped_core_defect_Y"),
    ("union_U_sq_minus_4V_sq_Y", "U_sq_minus_4V_sq_Y"),
    ("union_E_minus_4Dtilde_Y", "E_minus_4Dtilde_Y"),
    ("union_M_P0_DAMPED", "M_P0_DAMPED"),
    ("union_M_P_NEG_DAMPED", "M_P_NEG_DAMPED"),
    ("union_M_P_UV_DOM", "M_P_UV_DOM"),
    ("union_M_P_E3_MAIN", "M_P_E3_MAIN"),
    ("union_M_FRINGE_FEAT", "M_FRINGE_FEAT"),
    ("union_S1_four_X_om", "S1_four_X_om"),
    ("union_S2_suff_bound", "S2_suff_bound"),
    ("union_S3_suff_bound", "S3_suff_bound"),
    ("union_E1_T_main", "E1_T_main"),
    ("union_E2_T_main", "E2_T_main"),
)


# ---------------------------------------------------------------------------
# 0. Exact Arithmetic & Protocol Immutability Helpers
# ---------------------------------------------------------------------------


def paired_station_partition(T: int) -> Tuple[List[int], List[int]]:
    """Return exact `(Omega_2(T), Phi_2(T))` partitioning `{1, ..., T}`:
      - `Omega_2(T) = {1 <= n <= T : Odd(v_2(n)) or 2*n <= T}` (`coveredInteriorStations 2 T`)
      - `Phi_2(T)   = {1 <= n <= T : Even(v_2(n)) and T < 2*n}` (`uncoveredCutoffStripStations 2 T`).
    """
    if T < 0:
        raise ValueError(f"T must be >= 0, got {T}")
    omega2: List[int] = []
    phi2: List[int] = []
    for n in range(1, T + 1):
        v2 = prime_valuation_v_p(n, 2)
        if (v2 % 2 == 1) or (2 * n <= T):
            omega2.append(n)
        else:
            phi2.append(n)
    return omega2, phi2


def active_paired_prime_powers(T: int) -> List[Tuple[int, int]]:
    """Return `activePairedPrimePowers T`: all `(p, k) in primePowerPairsUpTo(T)` dividing at least
    one element of `Omega_2(T)`.
    """
    omega2_set = set(paired_station_partition(T)[0])
    out: List[Tuple[int, int]] = []
    for p, k in prime_power_pairs_up_to(T):
        q = p ** k
        if any(n in omega2_set for n in range(q, T + 1, q)):
            out.append((p, k))
    return out


def _fraction_interval_to_arb(lo: Fraction, hi: Fraction, prec_bits: int = 256) -> arb:
    """Convert an exact rational interval `[lo, hi]` into an outward-rounded `arb` ball."""
    if lo > hi:
        raise ValueError(f"Inverted rational interval: {lo} > {hi}")
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits + 32
        b_lo = _frac_to_arb(lo)
        b_hi = _frac_to_arb(hi)
        b_u = b_lo.union(b_hi)
        flint_ctx.prec = prec_bits
        return +b_u
    finally:
        flint_ctx.prec = saved


def verify_frozen_tc065_protocol_immutability(
    protocol_path: Path = SCALAR_FEATURE_PROTOCOL_PATH,
) -> Dict[str, Any]:
    """Verify SHA-256 and git-commit ancestry of `data/tc_scalar_feature_compensation_protocol.json`."""
    raw_bytes = protocol_path.read_bytes().replace(b"\r\n", b"\n")
    proto = json.loads(raw_bytes.decode("utf-8"))
    proto_without_hash = {k: v for k, v in proto.items() if k != "protocol_sha256"}
    canonical_bytes = json.dumps(
        proto_without_hash, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    computed_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
    recorded_sha256 = proto.get("protocol_sha256")
    hash_ok = bool(
        computed_sha256 == FROZEN_TC065_PROTOCOL_SHA256
        and recorded_sha256 == FROZEN_TC065_PROTOCOL_SHA256
    )

    git_blob_matches = False
    git_commit_is_ancestor = False
    try:
        proc_blob = subprocess.run(
            [
                "git",
                "show",
                f"{FROZEN_TC065_PROTOCOL_REGISTRATION_COMMIT}:data/tc_scalar_feature_compensation_protocol.json",
            ],
            cwd=str(REPO_ROOT),
            capture_output=True,
            check=False,
        )
        if proc_blob.returncode == 0:
            git_blob_matches = proc_blob.stdout.replace(b"\r\n", b"\n") == raw_bytes
        proc_anc = subprocess.run(
            [
                "git",
                "merge-base",
                "--is-ancestor",
                FROZEN_TC065_PROTOCOL_REGISTRATION_COMMIT,
                "HEAD",
            ],
            cwd=str(REPO_ROOT),
            capture_output=True,
            check=False,
        )
        git_commit_is_ancestor = proc_anc.returncode == 0
    except Exception:  # noqa: BLE001
        git_blob_matches = False
        git_commit_is_ancestor = False

    return {
        "protocol_path": "data/tc_scalar_feature_compensation_protocol.json",
        "protocol_id": proto.get("protocol_id"),
        "expected_protocol_sha256": FROZEN_TC065_PROTOCOL_SHA256,
        "computed_protocol_sha256": computed_sha256,
        "recorded_protocol_sha256": recorded_sha256,
        "sha256_verified": hash_ok,
        "registration_commit": FROZEN_TC065_PROTOCOL_REGISTRATION_COMMIT,
        "git_blob_matches_registration_commit": git_blob_matches,
        "registration_commit_is_ancestor_of_head": git_commit_is_ancestor,
        "protocol_object": proto,
        "verified": bool(
            proto.get("protocol_id") == FROZEN_TC065_PROTOCOL_ID
            and hash_ok
            and git_blob_matches
            and git_commit_is_ancestor
        ),
    }


def _sha256_lf(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


# ---------------------------------------------------------------------------
# 1. Core 256-Bit Outward-Rounded Arb Evaluators for Route 5 & Route 6
# ---------------------------------------------------------------------------


def compute_fringe_feature_theorem_bound_arb(
    Y_arb: arb,
    w0_arb: Optional[arb] = None,
    *,
    prec_bits: int = 256,
) -> arb:
    """Evaluate the Lean-proved unconditional general-base fringe feature norm upper bound
    `(8192 * w0^5 * log w0) / (log Y)^2 + (324 * w0^5 * log w0) / Y^(5/4)` (`Y >= 2, w0 > 1`).
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits + 32
        w0 = _tau_arb() if w0_arb is None else +w0_arb
        w5_lg = (w0 ** 5) * w0.log()
        lg_y = Y_arb.log()
        term1 = (arb(8192) * w5_lg) / (lg_y * lg_y)
        term2 = (arb(324) * w5_lg) / (Y_arb ** (arb(5) / arb(4)))
        flint_ctx.prec = prec_bits
        return +(term1 + term2)
    finally:
        flint_ctx.prec = saved


def evaluate_scalar_feature_compensation_1d_arb(
    Y_arb: arb,
    T_y: int,
    D0_eff: int,
    selberg_table: Dict[str, Any],
    *,
    r_contraction: Fraction = Fraction(1, 2),
    prec_bits: int = 256,
    quad_tol_bits: int = 160,
    n_panels: int = 16,
) -> Dict[str, arb]:
    """Evaluate all complete-observable Route 5 and Route 6 inner products and norms in ONE shared
    256-bit outward-rounded FLINT/Arb `acb.integral` quadrature pass on `[Y, tau*Y]` (valid for
    both exact point `Y_arb` and fixed-cutoff interval balls `Y_arb` with `Y >= 2`).

    Computes:
      - Core observables: `U_norm_sq_Y`, `V_norm_sq_Y`, `four_V_norm_sq_Y`, `J_A_Y`, `J_B_Y`,
        `U_sq_minus_4V_sq_Y`, `damped_core_defect_Y`, `S_core_Y`, `E_Y`, `D_tilde_Y`,
        `log_Y_times_D_tilde`, `E_minus_4Dtilde_Y`, `J_T_Y`, `Q_T_plus_A_T_norm_sq`.
      - Route 5 (`S1` unweighted `w = 1`, `S2` Mertens contractive `r`, `S3` single-channel `p=2, k=1`):
        complete residual budgets, contraction slacks, sufficient bounds, and algebraic residuals.
      - Route 6 (`E1` full-cutoff vs paired-fringe, `E2` large-prime `p > sqrt(T)` vs `p^k <= sqrt(T)`,
        `E3` bare-Liouville vs shifted-dilation): `T_main`, `T_cross`, `T_rem`, fringe norms,
        Lean fringe theorem bound, and algebraic residuals.
    """
    if T_y < 1:
        raise ValueError(f"T_y must be >= 1, got {T_y}")

    saved = flint_ctx.prec
    try:
        work = prec_bits + 40
        flint_ctx.prec = work
        tau = _tau_arb()
        log_tau = tau.log()
        sqrt_T = math.isqrt(T_y)
        r_arb = _frac_to_arb(r_contraction)
        r_acb = acb(r_arb)
        r_sq = r_arb * r_arb
        one_minus_r_sq = arb(1) - r_sq

        vecs = compute_complete_core_s_Y_and_beta_Y_arb(
            T_y, D0_eff, selberg_table["R_osc"], prec_bits=work
        )
        N2 = 2 * T_y
        lam_int = [0] + [liouville_lambda_int(n) for n in range(1, T_y + 1)]
        lam_acb = [acb(x) for x in lam_int]
        beta_acb = [acb(0)] + [acb(vecs["beta_Y"][n]) for n in range(1, N2 + 1)]
        log_n_acb = [acb(0)] + [acb(arb(n).log()) for n in range(1, T_y + 1)]

        omega2_list, phi2_list = paired_station_partition(T_y)
        omega2_set = set(omega2_list)

        # Core station lists for J_A and J_B
        cores = odd_squarefree_cores_C_T(T_y)
        core_idx = {a: i for i, a in enumerate(cores)}
        n_cores = len(cores)
        core_stations: List[List[int]] = [[] for _ in range(n_cores)]
        st_to_ci: Dict[int, int] = {}
        for u in odd_chain_parts_O_T(T_y):
            _, a_c, _ = odd_squarefree_core_and_root(u)
            ci = core_idx[a_c]
            for j in dyadic_chain_exponents_J_u(u, T_y):
                m_j = (4 ** j) * u
                core_stations[ci].append(m_j)
                core_stations[ci].append(2 * m_j)
                st_to_ci[m_j] = ci
                st_to_ci[2 * m_j] = ci

        pp_list = prime_power_pairs_up_to(T_y)
        # Mertens normalization M_pp(T) = sqrt(sum_{p^k <= T} (log p)^2 / p^k)
        m_pp_sq = arb(0)
        mertens_st_arb = [arb(0)] * (T_y + 1)
        # Prepack prime-power channel structures
        pp_packed: List[
            Tuple[
                bool,  # is_gt_sqrt_T
                bool,  # is_p2_k1
                acb,  # log(p)
                acb,  # log(p)^2
                List[int],  # om_pos (lam = +1)
                List[int],  # om_neg (lam = -1)
                List[int],  # fr_pos (lam = +1)
                List[int],  # fr_neg (lam = -1)
                List[Tuple[List[int], List[int]]],  # per-core (pos, neg) inside Omega_2
            ]
        ] = []
        for p, k in pp_list:
            q = p ** k
            lp_arb = arb(p).log()
            lp2_arb = lp_arb * lp_arb
            m_pp_sq += lp2_arb / arb(q)
            wt_st = lp2_arb / arb(q).sqrt()
            om_pos: List[int] = []
            om_neg: List[int] = []
            fr_pos: List[int] = []
            fr_neg: List[int] = []
            by_ci: Dict[int, Tuple[List[int], List[int]]] = {}
            for mult in range(q, T_y + 1, q):
                mertens_st_arb[mult] += wt_st
                is_pos = lam_int[mult] == 1
                if mult in omega2_set:
                    if is_pos:
                        om_pos.append(mult)
                    else:
                        om_neg.append(mult)
                    ci_h = st_to_ci[mult]
                    pair_c = by_ci.get(ci_h)
                    if pair_c is None:
                        pair_c = ([], [])
                        by_ci[ci_h] = pair_c
                    if is_pos:
                        pair_c[0].append(mult)
                    else:
                        pair_c[1].append(mult)
                else:
                    if is_pos:
                        fr_pos.append(mult)
                    else:
                        fr_neg.append(mult)
            pp_packed.append(
                (
                    q > sqrt_T,
                    (p == 2 and k == 1),
                    acb(lp_arb),
                    acb(lp2_arb),
                    om_pos,
                    om_neg,
                    fr_pos,
                    fr_neg,
                    list(by_ci.values()),
                )
            )
        m_pp_arb = m_pp_sq.sqrt() if bool(m_pp_sq > arb(0)) else arb(1)
        s2_scale_acb = r_acb / acb(m_pp_arb)
        mertens_st_acb = [acb(x) for x in mertens_st_arb]

        # Precompute station constants for phi_n(X)
        # Note: spillover n in (T, 2T] only needed where beta_Y[n] != 0
        spill_active = [n for n in range(T_y + 1, N2 + 1) if bool(vecs["beta_Y"][n] != arb(0))]
        all_needed_n = list(range(1, T_y + 1)) + spill_active
        st_consts = [
            (n, acb(n) ** (-3), acb(-(arb(n * n) ** (-1)))) for n in all_needed_n
        ]

        # 24 integrands evaluated from one shared node_cache per panel:
        # 0: U_om^2
        # 1: V_om^2 (sum_{pk} V_om_pk^2)
        # 2: J_A (sum_a A_a^2)
        # 3: J_B (sum_a sum_{pk} B_{a,pk}^2)
        # 4: E_Y (Q_T^2)
        # 5: D_tilde_Y (sum_{pk} G_T_pk^2)
        # 6: P_om^2
        # 7: O_om^2
        # 8: P_om * O_om
        # 9: LV_s2^2
        # 10: R_s2^2
        # 11: LV_s2 * R_s2
        # 12: LV_s3^2
        # 13: R_s3^2
        # 14: LV_s3 * R_s3
        # 15: U_main_e1^2 = (Q_T + A_T)^2
        # 16: U_rem_e1^2 = (Fringe + Spill)^2
        # 17: U_main_e1 * U_rem_e1
        # 18: V_fr^2 = sum_{pk} G_{Phi_2, pk}^2
        # 19: sum_{pk} G_T_pk * (-G_{Phi_2, pk})
        # 20: P_gt^2
        # 21: V_gt^2
        # 22: P_gt * (2*P_le - O_om)
        # 23: (2*P_le - O_om)^2
        # 24: Q_T * U_rem_e3  (U_rem_e3 = U_om - Q_T)
        # 25: U_rem_e3^2
        # 26: V_le^2
        n_int = 27
        Yc = acb(Y_arb)
        lgYc = acb(Y_arb.log())
        Yc_52 = Yc ** (acb(5) / acb(2))
        Yc_2 = Yc * Yc
        is_interval_ball = bool(Y_arb.rad() > arb(0))
        eff_tol = min(quad_tol_bits, 110) if is_interval_ball else quad_tol_bits
        tol = arb(2) ** (-eff_tol)

        accs = [arb(0) for _ in range(n_int)]
        for jp in range(n_panels):
            u_lo = log_tau * arb(jp) / arb(n_panels)
            u_hi = log_tau * arb(jp + 1) / arb(n_panels)
            node_cache: Dict[Any, Tuple[acb, ...]] = {}

            def _eval_all(u_var: acb, _an: bool) -> Optional[Tuple[acb, ...]]:
                lg = lgYc + u_var
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    return None
                key = (
                    (
                        flint_ctx.prec,
                        u_var.real.mid().man_exp(),
                        u_var.real.rad().man_exp(),
                        u_var.imag.mid().man_exp(),
                        u_var.imag.rad().man_exp(),
                        _an,
                    )
                    if u_var.is_finite()
                    else None
                )
                if key is not None:
                    hit = node_cache.get(key)
                    if hit is not None:
                        return hit

                inv_lg = acb(1) / lg
                inv_lg2 = inv_lg * inv_lg
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_var).exp()
                x2 = Yc_2 * (acb(2) * u_var).exp()

                ph = [acb(0)] * (N2 + 1)
                for n_i, inv_n3, neg_inv_n2 in st_consts:
                    ph[n_i] = x52 * inv_n3 * (x2 * neg_inv_n2).exp()

                psi_s = [acb(0)] * (T_y + 1)
                q_t = acb(0)
                for n_i in range(1, T_y + 1):
                    p_n = ph[n_i]
                    l_n = lam_acb[n_i]
                    q_t += l_n * p_n
                    psi_s[n_i] = (l_n - beta_acb[n_i] * inv_lg2) * p_n

                u_om = acb(0)
                p_om_raw = acb(0)
                lv_s2_raw = acb(0)
                for n_i in omega2_list:
                    u_om += psi_s[n_i]
                    lp_n = lam_acb[n_i] * ph[n_i]
                    p_om_raw += log_n_acb[n_i] * lp_n
                    lv_s2_raw += mertens_st_acb[n_i] * lp_n
                p_om = p_om_raw * inv_lg
                o_om = acb(2) * p_om - u_om
                lv_s2 = s2_scale_acb * lv_s2_raw * inv_lg
                r_s2 = u_om - acb(2) * lv_s2

                u_fr = acb(0)
                for n_i in phi2_list:
                    u_fr += psi_s[n_i]
                u_sp = acb(0)
                for n_i in spill_active:
                    u_sp -= beta_acb[n_i] * ph[n_i]
                u_sp *= inv_lg2
                u_rem_e1 = -(u_fr + u_sp)
                u_main_e1 = u_om - u_rem_e1  # = Q_T + A_T
                u_rem_e3 = u_om - q_t

                ja_val = acb(0)
                for st_l in core_stations:
                    sa = acb(0)
                    for st_n in st_l:
                        sa += psi_s[st_n]
                    ja_val += sa * sa

                v2_om_raw = acb(0)
                v2_full_raw = acb(0)
                v2_fr_raw = acb(0)
                vip_ff_raw = acb(0)
                v2_gt_raw = acb(0)
                v2_le_raw = acb(0)
                jb_raw = acb(0)
                p_gt_raw = acb(0)
                lv_s3 = acb(0)

                for (
                    is_gt,
                    is_p2,
                    lp_c,
                    lp2_c,
                    om_pos,
                    om_neg,
                    fr_pos,
                    fr_neg,
                    ci_list,
                ) in pp_packed:
                    s_om = acb(0)
                    for n_i in om_pos:
                        s_om += ph[n_i]
                    for n_i in om_neg:
                        s_om -= ph[n_i]
                    s_fr = acb(0)
                    for n_i in fr_pos:
                        s_fr += ph[n_i]
                    for n_i in fr_neg:
                        s_fr -= ph[n_i]
                    s_full = s_om + s_fr

                    sq_om = lp2_c * (s_om * s_om)
                    v2_om_raw += sq_om
                    v2_full_raw += lp2_c * (s_full * s_full)
                    v2_fr_raw += lp2_c * (s_fr * s_fr)
                    vip_ff_raw += lp2_c * (s_full * (-s_fr))
                    if is_gt:
                        v2_gt_raw += sq_om
                        p_gt_raw += lp_c * s_om
                    else:
                        v2_le_raw += sq_om
                    if is_p2:
                        lv_s3 = r_acb * lp_c * s_om * inv_lg

                    if ci_list:
                        sub_b = acb(0)
                        for c_pos, c_neg in ci_list:
                            sb = acb(0)
                            for n_i in c_pos:
                                sb += ph[n_i]
                            for n_i in c_neg:
                                sb -= ph[n_i]
                            sub_b += sb * sb
                        jb_raw += lp2_c * sub_b

                r_s3 = u_om - acb(2) * lv_s3
                p_gt = p_gt_raw * inv_lg
                p_le = p_om - p_gt
                u_rem_e2 = acb(2) * p_le - o_om

                out = (
                    u_om * u_om,
                    v2_om_raw * inv_lg2,
                    ja_val,
                    jb_raw * inv_lg2,
                    q_t * q_t,
                    v2_full_raw * inv_lg2,
                    p_om * p_om,
                    o_om * o_om,
                    p_om * o_om,
                    lv_s2 * lv_s2,
                    r_s2 * r_s2,
                    lv_s2 * r_s2,
                    lv_s3 * lv_s3,
                    r_s3 * r_s3,
                    lv_s3 * r_s3,
                    u_main_e1 * u_main_e1,
                    u_rem_e1 * u_rem_e1,
                    u_main_e1 * u_rem_e1,
                    v2_fr_raw * inv_lg2,
                    vip_ff_raw * inv_lg2,
                    p_gt * p_gt,
                    v2_gt_raw * inv_lg2,
                    p_gt * u_rem_e2,
                    u_rem_e2 * u_rem_e2,
                    q_t * u_rem_e3,
                    u_rem_e3 * u_rem_e3,
                    v2_le_raw * inv_lg2,
                )
                if key is not None:
                    node_cache[key] = out
                return out

            for idx in range(n_int):
                def _cb(uv: acb, _an: bool, _i: int = idx) -> acb:
                    res = _eval_all(uv, _an)
                    if res is None:
                        nb = arb("nan")
                        return acb(nb, nb)
                    return res[_i]

                accs[idx] += acb.integral(
                    _cb, acb(u_lo), acb(u_hi), rel_tol=tol, abs_tol=tol
                ).real

        flint_ctx.prec = prec_bits
        (
            u_sq,
            v_sq,
            ja,
            jb,
            e_y,
            d_tilde,
            p_om_sq,
            o_om_sq,
            ip_po,
            lv_s2_sq,
            r_s2_sq,
            ip_s2,
            lv_s3_sq,
            r_s3_sq,
            ip_s3,
            u_m1_sq,
            u_r1_sq,
            ip_u1,
            v_fr_sq,
            ip_v1,
            p_gt_sq,
            v_gt_sq,
            ip_pgt_rem,
            u_r2_sq,
            ip_q_r3,
            u_r3_sq,
            v_le_sq,
        ) = [+a for a in accs]

        four_v_sq = +(arb(4) * v_sq)
        u_minus_4v = +(u_sq - four_v_sq)
        damped_defect = +(u_minus_4v - ja)
        s_core = +(damped_defect + arb(4) * jb)
        lg_y = Y_arb.log()
        lg_dt = +(lg_y * d_tilde)
        e_minus_4dt = +(e_y - arb(4) * d_tilde)
        j_t = +(u_m1_sq - arb(4) * d_tilde)

        # Route 5 S1 (w = 1)
        s1_four_x = +(arb(4) * (p_om_sq - v_sq))
        s1_recon = +(s1_four_x + o_om_sq - arb(4) * ip_po - ja)
        s1_res = +(s1_recon - damped_defect)

        # Route 5 S2 (Mertens r)
        s2_slack = +(arb(4) * (v_sq - lv_s2_sq))
        s2_recon = +(arb(4) * ip_s2 + r_s2_sq - ja - s2_slack)
        s2_res = +(s2_recon - damped_defect)
        s2_suff = +(r_s2_sq / one_minus_r_sq - ja)

        # Route 5 S3 (p = 2, k = 1, r)
        s3_slack = +(arb(4) * (v_sq - lv_s3_sq))
        s3_recon = +(arb(4) * ip_s3 + r_s3_sq - ja - s3_slack)
        s3_res = +(s3_recon - damped_defect)
        s3_suff = +(r_s3_sq / one_minus_r_sq - ja)

        # Route 6 E1 (Full vs Fringe+Spill)
        e1_main = +j_t
        e1_cross = +(arb(2) * ip_u1 - arb(8) * ip_v1)
        e1_rem = +(u_r1_sq - arb(4) * v_fr_sq - ja)
        e1_res = +((e1_main + e1_cross + e1_rem) - damped_defect)
        fringe_thm_bd = compute_fringe_feature_theorem_bound_arb(Y_arb, prec_bits=prec_bits)
        m_fringe_feat = +(v_fr_sq - fringe_thm_bd)

        # Route 6 E2 (p > sqrt(T) vs p^k <= sqrt(T), <V_gt, V_le> = 0 identically)
        e2_4pgt = +(arb(4) * p_gt_sq)
        e2_4vgt = +(arb(4) * v_gt_sq)
        e2_main = +(e2_4pgt - e2_4vgt)
        e2_cross = +(arb(4) * ip_pgt_rem)
        e2_rem = +(u_r2_sq - arb(4) * v_le_sq - ja)
        e2_res = +((e2_main + e2_cross + e2_rem) - damped_defect)

        # Route 6 E3 (Bare Liouville Q_T vs shifted-dilation G_T)
        e3_main = +e_minus_4dt
        e3_cross = +(arb(2) * ip_q_r3 - arb(8) * ip_v1)
        e3_rem = +(u_r3_sq - arb(4) * v_fr_sq - ja)
        e3_res = +((e3_main + e3_cross + e3_rem) - damped_defect)

        # Probe margins
        m_p0_damped = +(damped_defect - lg_dt)
        m_p_neg_damped = +damped_defect
        m_p_uv_dom = +u_minus_4v
        m_p_e3_main = +e_minus_4dt

        return {
            "U_norm_sq_Y": u_sq,
            "V_norm_sq_Y": v_sq,
            "four_V_norm_sq_Y": four_v_sq,
            "J_A_Y": ja,
            "J_B_Y": jb,
            "U_sq_minus_4V_sq_Y": u_minus_4v,
            "damped_core_defect_Y": damped_defect,
            "S_core_Y": s_core,
            "E_Y": e_y,
            "D_tilde_Y": d_tilde,
            "log_Y_times_D_tilde": lg_dt,
            "E_minus_4Dtilde_Y": e_minus_4dt,
            "J_T_Y": j_t,
            "Q_T_plus_A_T_norm_sq": u_m1_sq,
            "S1_P_om_norm_sq": p_om_sq,
            "S1_O_om_norm_sq": o_om_sq,
            "S1_minus_4_ip_P_O": +(-arb(4) * ip_po),
            "S1_four_X_om": s1_four_x,
            "S1_budget_residual": s1_res,
            "S2_M_pp_T": +m_pp_arb,
            "S2_LV_norm_sq": lv_s2_sq,
            "S2_R_norm_sq": r_s2_sq,
            "S2_4_ip_LV_R": +(arb(4) * ip_s2),
            "S2_slack_4_Vsq_minus_LVsq": s2_slack,
            "S2_suff_bound": s2_suff,
            "S2_budget_residual": s2_res,
            "S3_LV_norm_sq": lv_s3_sq,
            "S3_R_norm_sq": r_s3_sq,
            "S3_4_ip_LV_R": +(arb(4) * ip_s3),
            "S3_slack_4_Vsq_minus_LVsq": s3_slack,
            "S3_suff_bound": s3_suff,
            "S3_budget_residual": s3_res,
            "E1_T_main": e1_main,
            "E1_T_cross": e1_cross,
            "E1_T_rem": e1_rem,
            "E1_U_rem_norm_sq": u_r1_sq,
            "E1_V_rem_norm_sq": v_fr_sq,
            "E1_fringe_feat_thm_bound": fringe_thm_bd,
            "E1_budget_residual": e1_res,
            "E2_four_P_gt_sq": e2_4pgt,
            "E2_four_V_gt_sq": e2_4vgt,
            "E2_T_main": e2_main,
            "E2_T_cross": e2_cross,
            "E2_T_rem": e2_rem,
            "E2_budget_residual": e2_res,
            "E3_T_main": e3_main,
            "E3_T_cross": e3_cross,
            "E3_T_rem": e3_rem,
            "E3_budget_residual": e3_res,
            "M_P0_DAMPED": m_p0_damped,
            "M_P_NEG_DAMPED": m_p_neg_damped,
            "M_P_UV_DOM": m_p_uv_dom,
            "M_P_E3_MAIN": m_p_e3_main,
            "M_FRINGE_FEAT": m_fringe_feat,
        }
    finally:
        flint_ctx.prec = saved


def certify_pointwise_oracle_residual_lower_bound_arb(
    Y_arb: arb,
    T_y: int,
    D0_eff: int,
    selberg_table: Dict[str, Any],
    *,
    r_val: Fraction = Fraction(1, 1),
    n_subintervals: int = 128,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Compute a 100% rigorous real-interval Arb lower bound on the pointwise oracle residual
    `I_oracle(Y, r) := int_Y^{tau*Y} max(0, |U_Y(X)| - 2*r*|V_Y(X)|_{l^2})^2 dX/X`
    by partitioning `u in [0, log tau]` into `n_subintervals` real intervals `I_j` and summing
    `(max(0, lower(|U_Y(I_j)| - 2*r*sqrt(sum_{pk} V_{Y,pk}(I_j)^2))))^2 * |I_j|`.

    Does NOT pass non-analytic `max(0, ...)` to complex quadrature; any certified positive lower
    bound (`lower > 0`) proves zero-residual pointwise synthesis with `||L_Y||_op <= r` is
    impossible at scale `Y` even for an arbitrary oracle weight vector.
    """
    saved = flint_ctx.prec
    try:
        work = prec_bits + 32
        flint_ctx.prec = work
        tau = _tau_arb()
        log_tau = tau.log()
        r_arb = _frac_to_arb(r_val)
        vecs = compute_complete_core_s_Y_and_beta_Y_arb(
            T_y, D0_eff, selberg_table["R_osc"], prec_bits=work
        )
        lam_int = [0] + [liouville_lambda_int(n) for n in range(1, T_y + 1)]
        lam_arb = [arb(x) for x in lam_int]
        beta_arb = [arb(0)] + [+vecs["beta_Y"][n] for n in range(1, T_y + 1)]
        omega2_list, _ = paired_station_partition(T_y)
        omega2_set = set(omega2_list)

        pp_om: List[Tuple[arb, List[int], List[int]]] = []
        for p, k in prime_power_pairs_up_to(T_y):
            q = p ** k
            pos_l = [n for n in range(q, T_y + 1, q) if n in omega2_set and lam_int[n] == 1]
            neg_l = [n for n in range(q, T_y + 1, q) if n in omega2_set and lam_int[n] == -1]
            if pos_l or neg_l:
                pp_om.append((arb(p).log() ** 2, pos_l, neg_l))

        st_consts = [(n, arb(n) ** (-3), -(arb(n * n) ** (-1))) for n in omega2_list]

        def _eval_gap_on_u_ball(u_b: arb) -> Tuple[arb, arb]:
            X_b = Y_arb * u_b.exp()
            lg_b = X_b.log()
            inv_lg2_b = arb(1) / (lg_b * lg_b)
            x52_b = X_b ** (arb(5) / arb(2))
            x2_b = X_b * X_b

            ph_b = [arb(0)] * (T_y + 1)
            u_v = arb(0)
            for n_i, inv_n3, neg_inv_n2 in st_consts:
                p_n = x52_b * inv_n3 * (x2_b * neg_inv_n2).exp()
                ph_b[n_i] = p_n
                u_v += (lam_arb[n_i] - beta_arb[n_i] * inv_lg2_b) * p_n

            v2_raw_b = arb(0)
            for lp2_a, pos_l, neg_l in pp_om:
                s_c = arb(0)
                for n_i in pos_l:
                    s_c += ph_b[n_i]
                for n_i in neg_l:
                    s_c -= ph_b[n_i]
                v2_raw_b += lp2_a * (s_c * s_c)
            v2_b = v2_raw_b * inv_lg2_b
            v_norm_b = v2_b.nonnegative_part().sqrt()
            return abs(u_v) - arb(2) * r_arb * v_norm_b, X_b

        # Exact zero-radius dyadic partition 0 = g_0 < g_1 < ... < g_N <= log(tau)
        # guarantees pairwise interior-disjoint closed subintervals inside [0, log(tau)].
        grid_u: List[arb] = [arb(0)]
        for j in range(1, n_subintervals):
            grid_u.append((log_tau * arb(j) / arb(n_subintervals)).mid())
        grid_u.append(log_tau.lower())

        lb_total = arb(0)
        certified_positive_subintervals = 0
        best_witness: Optional[Dict[str, Any]] = None
        best_gap_lo = arb(0)

        for j in range(n_subintervals):
            u_lo = grid_u[j]
            u_hi = grid_u[j + 1]
            if not bool(u_hi > u_lo):
                continue
            u_mid = ((u_lo + u_hi) / arb(2)).mid()
            half_w = (u_hi - u_lo) / arb(2)

            # First evaluate full bin [u_lo, u_hi]; if interval dependency bloat hides a positive peak,
            # test the exact midpoint and certify a strictly contained exact-dyadic sub-window
            # [a_sub, b_sub] inside [u_lo, u_hi]. Since the integrand is nonnegative everywhere and
            # bins are pairwise interior-disjoint inside [0, log(tau)], summing over any sub-window
            # inside each bin is a 100% rigorous lower bound.
            u_ball = u_lo.union(u_hi)
            gap, X_ball = _eval_gap_on_u_ball(u_ball)
            eff_du = u_hi - u_lo
            if not bool(gap > arb(0)):
                gap_mid, _ = _eval_gap_on_u_ball(u_mid)
                if bool(gap_mid > arb(0)):
                    h_cur = half_w
                    for _ in range(10):
                        h_cur = h_cur / arb(4)
                        a_sub = (u_mid - h_cur).mid()
                        b_sub = (u_mid + h_cur).mid()
                        if not (bool(a_sub >= u_lo) and bool(b_sub <= u_hi) and bool(b_sub > a_sub)):
                            break
                        u_sub = a_sub.union(b_sub)
                        gap_sub, X_sub = _eval_gap_on_u_ball(u_sub)
                        if bool(gap_sub > arb(0)):
                            u_ball = u_sub
                            gap = gap_sub
                            X_ball = X_sub
                            eff_du = b_sub - a_sub
                            break

            if bool(gap > arb(0)):
                certified_positive_subintervals += 1
                gap_lo = gap.lower()
                lb_total += (gap_lo * gap_lo) * eff_du.lower()
                if bool(gap_lo > best_gap_lo):
                    best_gap_lo = gap_lo
                    flint_ctx.prec = prec_bits
                    best_witness = {
                        "subinterval_index": j,
                        "n_subintervals": n_subintervals,
                        "u_interval_ball": serialize_arb_certified(+u_ball),
                        "X_interval_ball": serialize_arb_certified(+X_ball),
                        "abs_U_minus_2r_V_l2": serialize_arb_certified(+gap),
                    }
                    flint_ctx.prec = work

        flint_ctx.prec = prec_bits
        lb_out = +lb_total
        certified_nonzero = bool(lb_out > arb(0))
        return {
            "r_fraction": f"{r_val.numerator}/{r_val.denominator}",
            "n_subintervals": n_subintervals,
            "certified_positive_subintervals": certified_positive_subintervals,
            "oracle_residual_lower_bound": serialize_arb_certified(lb_out),
            "certified_strictly_positive": certified_nonzero,
            "verdict_for_zero_residual_contractive_pointwise_synthesis": (
                "FAIL" if certified_nonzero else "UNRESOLVED"
            ),
            "best_subinterval_witness": best_witness,
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 2. Section 1: Protocols, Upstream Preservation, & Complete Premise Table
# ---------------------------------------------------------------------------


def _build_tc065_premise_and_dependency_table() -> List[Dict[str, str]]:
    """Exact premise and dependency table connecting TASK-TC-065 to the RH contradiction endpoint."""
    return [
        {
            "premise_id": "TC065-PREM-01-DAMPED-CORE-COMPENSATION-TARGET",
            "stage": "Stage 0 (Open Surviving Signed-Compensation Target)",
            "statement": (
                "MixedCovarianceClosureHypothesis(D_core, D_tilde): forall eta > 0, exists A_eta, B_eta >= 0, "
                "0 < kappa_eta <= 2, Y_eta >= 2: forall real Y >= Y_eta, "
                "D_core(Y) = ||U_Y||_Y^2 - 4*||V_Y||_Y^2 - J_A(Y) <= A_eta * Y^eta + B_eta * (log Y)^(2 - kappa_eta) * D_tilde(Y)"
            ),
            "location": "formal/RiemannScope/ScalarFeatureCompensation.lean::canonicalDampedCoreDefectD",
            "status": "OPEN",
            "gap_classification": "MISSING_MATHEMATICS",
        },
        {
            "premise_id": "TC065-PREM-02-DAMPED-CORE-EXACT-EQUIVALENCE-AND-FRINGE-BOUNDS",
            "stage": "Stage 1A (Damped-Target Identity, Paired-Station Synthesis, Telescoping, & Uniform Fringe Bounds)",
            "statement": (
                "For all real Y >= 2: D_core(Y) = ||U_Y||^2 - 4*||V_Y||^2 - J_A(Y), S_core(Y) = D_core(Y) + 4*J_B(Y), "
                "H(D_core, D_tilde) <-> H(S_core, D_tilde); U_Y = 2*P_{Omega_2} - O_{Omega_2} = Q_T + A_T - S_spill - Phi_fringe; "
                "for all w_0 > 1 and Y >= 2, ||G_{Phi_2}||_{Y,w_0}^2 <= (8192*w_0^5*log w_0)/(log Y)^2 + (324*w_0^5*log w_0)/Y^(5/4), "
                "giving | ||V_Y||_Y - sqrt(D_tilde(Y)) | <= O(1/log Y); and ||Phi_fringe||_Y^2 <= C_fr = O(1)"
            ),
            "location": (
                "formal/RiemannScope/ScalarFeatureCompensation.lean::"
                "damped_core_defect_and_closure_equivalence_tc065, "
                "paired_station_partition_divisor_synthesis_and_telescoping_tc065, "
                "coupled_mode_expansion_uniform_fringe_bounds_and_orthogonality_tc065"
            ),
            "status": "PROVED_IN_LEAN",
            "gap_classification": "NONE",
        },
        {
            "premise_id": "TC065-PREM-03-SYNTHESIS-OPERATOR-NORM-AND-OBSTRUCTIONS",
            "stage": "Stage 1B (Route 5 Synthesis Budget, Exact Operator Norm, & Pointwise Obstructions)",
            "statement": (
                "Exact Hilbert budget D_core = 4<L_Y V_Y, R_Y> + ||R_Y||^2 - J_A - 4(||V_Y||^2 - ||L_Y V_Y||^2), "
                "strict-contraction bound D_core <= ||R_Y||^2/(1 - r^2) - J_A (0 <= r < 1), "
                "exact pointwise operator norm bound & constant-weight tightness, channel-weight dilution "
                "(sqrt(|P_act|) - r)^2 <= sum (1 - w)^2, and pointwise oracle residual lower bound"
            ),
            "location": (
                "formal/RiemannScope/ScalarFeatureCompensation.lean::"
                "arithmetic_synthesis_hilbert_budget_operator_norm_and_obstructions_tc065"
            ),
            "status": "PROVED_IN_LEAN",
            "gap_classification": "NONE",
        },
        {
            "premise_id": "TC065-PREM-04-DIRECT-E-MINUS-4DTILDE-CLOSURE-TRANSFER",
            "stage": "Stage 1C (Conditional Direct Route D Transfer for E_lambda - 4*D_tilde Using Only PREM-04..06)",
            "statement": (
                "Given MixedCovarianceClosureHypothesis(E_lambda - 4*D_tilde, D_tilde) and TC063-PREM-04..06 "
                "(without requiring TC063-PREM-07 on ||A_T||^2), forall eps > 0, exists C_eps >= 0, "
                "forall Z >= 1, canonicalLiouvilleEnergyE(Z) <= C_eps * Z^eps (and converse holds unconditionally)"
            ),
            "location": (
                "formal/RiemannScope/ScalarFeatureCompensation.lean::"
                "bare_liouville_shifted_dilation_closure_and_euler_limit_tc065"
            ),
            "status": "CONDITIONAL_PROVED_IN_LEAN",
            "gap_classification": "NONE_FOR_TRANSFER_IMPLICATION",
        },
        {
            "premise_id": "TC064-PREM-03-ROUTE-D-FINITE-HORIZON-CONTRACTION-ALGEBRA",
            "stage": "Stage 1D (Conditional Route D Contraction Schema from D_core / S_core)",
            "statement": (
                "Given H(D_core, D_tilde) <-> H(S_core, D_tilde) and analytic inputs TC063-PREM-04..07, "
                "forall eps > 0, exists C_eps >= 0, forall real Z >= 1, canonicalLiouvilleEnergyE(Z) <= C_eps * Z^eps"
            ),
            "location": (
                "formal/RiemannScope/SquarefreeCoreCorrelation.lean::"
                "uniform_same_core_hilbert_bound_and_closure_transfer_tc064"
            ),
            "status": "CONDITIONAL_PROVED_IN_LEAN",
            "gap_classification": "NONE_FOR_TRANSFER_IMPLICATION",
        },
        {
            "premise_id": "TC063-PREM-04-GLOBAL-LINEAR-ENERGY-ENVELOPE",
            "stage": "Stage 1 Input 1 (Global Linear Energy Majorant)",
            "statement": "forall real Z >= 1, E(Z) = ||Q_{lambda, T(Z)}||_Z^2 <= M_lin * Z",
            "location": "docs/reviews/TC_056_PRIME_CHAIN_CONTRACTION.md (Prop. 2.1)",
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_classification": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-05-PRIME-POWER-DIRICHLET-WEIGHT-FINITENESS",
            "stage": "Stage 1 Input 2 (Weighted Prime-Power Mass)",
            "statement": "forall delta > 0, sum_{p^k <= floor(Y)} (log p)^2 / (p^k)^(1 + delta) <= sum_{n >= 2} (log n)^2 / n^(1 + delta) = zeta''(1 + delta) < infty",
            "location": "docs/reviews/TC_057_COUPLED_ARITHMETIC_SCALE_ENERGY_BOOTSTRAP.md (§5); docs/reviews/TC_063_DYADIC_CHAIN_CORRELATION_AND_ARITHMETIC_REGULARITY.md (§9 Erratum)",
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_classification": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-06-SHIFTED-DIAGONAL-ENVELOPE-CUTOFF-BOUND",
            "stage": "Stage 1 Input 3 (Shifted Prime-Power Diagonal Comparison)",
            "statement": "forall real Y >= Y_diag, D_tilde(Y) <= (2 / (log Y)^2) * sum_{p^k <= floor(Y)} ((log p)^2 / p^k) * E_sup(Y / p^k) + C_cut",
            "location": "docs/reviews/TC_057_COUPLED_ARITHMETIC_SCALE_ENERGY_BOOTSTRAP.md (Thm. 6.1)",
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_classification": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-07-KNOWN-COMPENSATED-PART-HORIZON-CONTRACTION",
            "stage": "Stage 1 Input 4 (Known Selberg/Drift Part ||A_Y||_Y^2 Contraction; bypassed on direct E_lambda - 4*D_tilde route)",
            "statement": "forall R >= Y >= Y_diag, ||A_Y||_Y^2 <= a_known * Y^(eps/4) + (B_drift / (log Y)^kappa_d) * G_eps(R) * Y^eps",
            "location": "formal/RiemannScope/SignedDilationArithmeticEnergy.lean::second_order_drift_abel_and_small_divisor_contraction_tc060",
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_classification": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-08-FINITE-TO-INFINITE-OBSERVABLE-CONVERGENCE",
            "stage": "Stage 2 (Infinite Observable Tail Convergence)",
            "statement": "||Q_{a, infty} - Q_{a, T(Y)}||_Y <= B_tau = (tau^(5/2)*sqrt(log tau))/2 for |a(n)| <= 1 and Y >= 1, giving E_a <<_eps Y^eps <-> E_{a, infty} <<_eps Y^eps",
            "location": "formal/RiemannScope/SquarefreeCoreCorrelation.lean::finite_euler_factor_dirichlet_multiplier_and_dilation_equivalence_tc064",
            "status": "PROVED_IN_LEAN",
            "gap_classification": "NONE",
        },
        {
            "premise_id": "TC063-PREM-09-MELLIN-HOLOMORPHIC-CONTINUATION-BRIDGE",
            "stage": "Stage 3 (Mellin Analytic Continuation to x > 1/2)",
            "statement": "(forall eps > 0, E_{lambda, infty}(Y) <= C_eps * Y^eps) ==> L_lambda(x + i*y) = zeta(2*x + 2*i*y)/zeta(x + i*y) extends holomorphically to x > 1/2",
            "location": "docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md (Prop. 3.1)",
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_classification": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-10-ACTUAL-ZETA-POLE-CONTRADICTION-AND-REFLECTION",
            "stage": "Stage 4 (Actual Mathlib riemannZeta Pole Contradiction & Functional Reflection)",
            "statement": "Given pole-free holomorphic continuation F_hol of L_lambda(x + i*y) to x > 1/2, any zero rho = x + i*y with 1/2 < x < 1 yields 0 = zeta(rho)*F_hol(rho) = zeta(2*rho) != 0, and 0 < x < 1/2 reflects via completedRiemannZeta to 1 - rho",
            "location": "formal/RiemannScope/DyadicChainCorrelationRegularity.lean::liouville_dirichlet_ratio_pole_contradiction_and_reflection_tc063",
            "status": "CONDITIONAL_PROVED_IN_LEAN",
            "gap_classification": "NONE_FOR_TRANSFER_IMPLICATION",
        },
        {
            "premise_id": "TC065-PREM-11-FINITE-EULER-MULTIPLIER-VS-QUOTIENT-LIMIT-AT-1",
            "stage": "Incidental Clarification (Section 9 Limit Scope at x + i*y = 1)",
            "statement": (
                "For any fixed finite set S of odd primes, the finite Euler multiplier "
                "M_S(z) = prod_{q in S} (1 + q^(-z))/(1 - q^(-z)) has nonzero limit prod_{q in S} (q + 1)/(q - 1) != 0 "
                "as z -> 1, while the modified Liouville quotient L_{a_S}(z) = (zeta(2*z)/zeta(z))*M_S(z) -> 0 as z -> 1, z != 1"
            ),
            "location": "formal/RiemannScope/ScalarFeatureCompensation.lean::bare_liouville_shifted_dilation_closure_and_euler_limit_tc065",
            "status": "PROVED_IN_LEAN",
            "gap_classification": "NONE",
        },
    ]


def verify_section_1_protocols_and_premise_chain() -> Dict[str, Any]:
    """Verify all five frozen protocols, upstream artifact preservation, and premise chain."""
    p61 = verify_frozen_protocol_immutability()
    p62 = verify_frozen_tc062_protocol_immutability()
    p63 = verify_frozen_tc063_protocol_immutability()
    p64 = verify_frozen_tc064_protocol_immutability()
    p65 = verify_frozen_tc065_protocol_immutability()

    proto_obj = p65["protocol_object"]
    exp_hashes = proto_obj["baseline_provenance"]["upstream_source_hashes_sha256"]
    upstream_checks = {
        "tc061_artifact_sha256_preserved": _sha256_lf(MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH)
        == EXPECTED_TC061_ARTIFACT_SHA256,
        "tc062_artifact_sha256_preserved": _sha256_lf(JOINT_PRIME_DILATION_ARTIFACT_PATH)
        == EXPECTED_TC062_ARTIFACT_SHA256,
        "tc063r_artifact_sha256_preserved": _sha256_lf(DYADIC_CHAIN_ARTIFACT_PATH)
        == EXPECTED_TC063R_ARTIFACT_SHA256,
        "tc064_artifact_sha256_preserved": _sha256_lf(SQUAREFREE_CORE_ARTIFACT_PATH)
        == exp_hashes["data/tc_squarefree_core_correlation.json"],
        "tc064_lean_sha256_preserved": _sha256_lf(
            REPO_ROOT / "formal" / "RiemannScope" / "SquarefreeCoreCorrelation.lean"
        )
        == exp_hashes["formal/RiemannScope/SquarefreeCoreCorrelation.lean"],
    }

    all_ok = bool(
        p61["verified"]
        and p62["verified"]
        and p63["verified"]
        and p64["verified"]
        and p65["verified"]
        and all(upstream_checks.values())
    )
    return {
        "component_epistemic_map": {
            "frozen_protocols": "UNCONDITIONAL_FINITE_ARITHMETIC",
            "upstream_preservation_checks": "UNCONDITIONAL_FINITE_ARITHMETIC",
            "window_base_and_scaling_scope": "CONCRETE_ANALYTIC_IN_LEAN",
            "premise_and_dependency_table": "CONDITIONAL_IMPLICATION",
        },
        "epistemic_statuses": [
            "UNCONDITIONAL_FINITE_ARITHMETIC",
            "CONCRETE_ANALYTIC_IN_LEAN",
            "CONDITIONAL_IMPLICATION",
        ],
        "section_epistemic_scope_note": (
            "Verifies immutability of all five frozen protocols (TC-061 through TC-065) and byte-for-byte "
            "preservation of all upstream certified artifacts. Records the exact premise chain from "
            "TC065-PREM-01 to the RH pole contradiction while keeping SUBGATE-TC-043A OPEN."
        ),
        "frozen_protocols": {
            "TC061": {k: v for k, v in p61.items() if k != "protocol_object"},
            "TC062": {k: v for k, v in p62.items() if k != "protocol_object"},
            "TC063": {k: v for k, v in p63.items() if k != "protocol_object"},
            "TC064": {k: v for k, v in p64.items() if k != "protocol_object"},
            "TC065": {k: v for k, v in p65.items() if k != "protocol_object"},
        },
        "upstream_preservation_checks": upstream_checks,
        "window_base_and_scaling_scope": {
            "window_base_generality": (
                "All finite-set arithmetic identities (paired-station partition, odd prime-power vanishing "
                "above T/2, square-lift parity, pointwise telescoping of s_Y(n), sum_{e|n} |w_2(e)| = (log n)^2, "
                "large-prime station disjointness) are window-independent; the fringe feature norm bound "
                "||G_{Phi_2}||_{Y, w_0}^2 <= (8192*w_0^5*log w_0)/(log Y)^2 + (324*w_0^5*log w_0)/Y^(5/4) "
                "is formally proved in Lean for every real window base w_0 > 1 (paramWindowNormSq Y w_0) "
                "and specialized to w_0 = tau. No result in TASK-TC-065 relies on any tau-specific transcendence property."
            ),
            "scaling_distinction_carried_forward": (
                "Fixed square dilation n |-> b^2*n gives phi_{b^2*n}(X) = b^(-1)*phi_n(X/b^2) on the bare "
                "Gaussian while changing supports and adjusted beta_Y terms on complete profiles psi_{Y,n}; "
                "running-index squaring n |-> n^2 yields zeta(2*x + 2*i*y) on x > 1/2; Liouville convolution "
                "1 * lambda = 1_square yields zeta(x + i*y)*L_lambda(x + i*y) = zeta(2*x + 2*i*y); "
                "tau^K grade transport parameterizes the integration window [Y, tau*Y]."
            ),
            "carried_forward_tc064r_corrections": (
                "Carries forward Attempt 1 (common-factor/coprime GCD sectors & signed log-GCD identity) "
                "and Attempt 2 (prime-toggle involution & exact resonant boundary {a in C_res(Y) : p nmid a} "
                "under strict 2*p*Y > T(Y)), A_a / B_a^feat profile notation, withdrawal of the unproved "
                "full-profile p^(-3) comparison, aggregate-only large-g tail bound, and the Section 9 limit "
                "clarification (finite Euler multiplier M_S(z) has nonzero limit prod_{q in S} (q+1)/(q-1) != 0 "
                "as z -> 1, while the modified Liouville quotient L_{a_S}(z) -> 0 as z -> 1, z != 1)."
            ),
        },
        "premise_and_dependency_table": _build_tc065_premise_and_dependency_table(),
        "all_section_1_checks_pass": all_ok,
    }


# ---------------------------------------------------------------------------
# 3. Section 2: Exact TC-064 Seen-Scale Reproduction, Exact Algebra, & 1D Cross-Checks
# ---------------------------------------------------------------------------


def derive_tc064_seen_damped_defects_exact(
    tc064_artifact_path: Path = SQUAREFREE_CORE_ARTIFACT_PATH,
    *,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Reproduce `damped_core_defect_Y = S_core_Y - 4*J_B_Y` at `Y in {512, 576, 960, 1408}`
    directly from the exact outward decimal endpoints recorded in `data/tc_squarefree_core_correlation.json`,
    measuring `||U_Y||^2`, `4*||V_Y||^2`, `||U_Y||^2 - 4*||V_Y||^2`, and the diagonal allowance `J_A(Y)`
    separately. Explicitly labeled `SEEN_DERIVED_FROM_TC064_CERTIFICATES`.
    """
    data = json.loads(tc064_artifact_path.read_text(encoding="utf-8"))
    rows_in = data["section_4_distinct_core_attempts_seen_diagnostics_and_euler_robustness"][
        "seen_scale_mechanism_diagnostics"
    ]
    out_rows: List[Dict[str, Any]] = []
    all_ok = True
    for row in rows_in:
        Y = int(row["Y"])
        sc_lo, sc_hi = Fraction(row["S_core_Y"]["lower_dec"]), Fraction(row["S_core_Y"]["upper_dec"])
        ss_lo, ss_hi = (
            Fraction(row["S_core_scalar_Y"]["lower_dec"]),
            Fraction(row["S_core_scalar_Y"]["upper_dec"]),
        )
        sf_lo, sf_hi = (
            Fraction(row["S_core_feature_Y"]["lower_dec"]),
            Fraction(row["S_core_feature_Y"]["upper_dec"]),
        )
        ja_lo, ja_hi = (
            Fraction(row["unsigned_diagnostic_sum_A_norm_sq"]["lower_dec"]),
            Fraction(row["unsigned_diagnostic_sum_A_norm_sq"]["upper_dec"]),
        )
        jb_lo, jb_hi = (
            Fraction(row["unsigned_diagnostic_sum_Bfeat_norm_sq"]["lower_dec"]),
            Fraction(row["unsigned_diagnostic_sum_Bfeat_norm_sq"]["upper_dec"]),
        )
        ld_lo, ld_hi = (
            Fraction(row["log_Y_times_D_tilde"]["lower_dec"]),
            Fraction(row["log_Y_times_D_tilde"]["upper_dec"]),
        )

        # Exact rational interval arithmetic on outward endpoints:
        dcore_lo = sc_lo - 4 * jb_hi
        dcore_hi = sc_hi - 4 * jb_lo
        u2_lo = ss_lo + ja_lo
        u2_hi = ss_hi + ja_hi
        v4_lo = 4 * jb_lo - sf_hi
        v4_hi = 4 * jb_hi - sf_lo
        uv_diff_lo = u2_lo - v4_hi
        uv_diff_hi = u2_hi - v4_lo
        # Cross-check D_core from (||U||^2 - 4||V||^2) - J_A
        dcore_alt_lo = uv_diff_lo - ja_hi
        dcore_alt_hi = uv_diff_hi - ja_lo
        overlap_ok = bool(dcore_lo <= dcore_alt_hi and dcore_alt_lo <= dcore_hi)
        neg_dcore = bool(dcore_hi < 0)
        neg_uv = bool(uv_diff_hi < 0)

        dcore_arb = _fraction_interval_to_arb(dcore_lo, dcore_hi, prec_bits=prec_bits)
        u2_arb = _fraction_interval_to_arb(u2_lo, u2_hi, prec_bits=prec_bits)
        v4_arb = _fraction_interval_to_arb(v4_lo, v4_hi, prec_bits=prec_bits)
        uv_arb = _fraction_interval_to_arb(uv_diff_lo, uv_diff_hi, prec_bits=prec_bits)
        ja_arb = _fraction_interval_to_arb(ja_lo, ja_hi, prec_bits=prec_bits)
        jb4_arb = _fraction_interval_to_arb(4 * jb_lo, 4 * jb_hi, prec_bits=prec_bits)
        ld_arb = _fraction_interval_to_arb(ld_lo, ld_hi, prec_bits=prec_bits)

        saved = flint_ctx.prec
        try:
            flint_ctx.prec = prec_bits
            ratio_uv = +(u2_arb / v4_arb)
            ja_share = +(ja_arb / (-dcore_arb))
            m_p0 = +(dcore_arb - ld_arb)
        finally:
            flint_ctx.prec = saved

        row_ok = bool(overlap_ok and neg_dcore and neg_uv and bool(m_p0 < arb(0)))
        all_ok = all_ok and row_ok
        out_rows.append(
            {
                "Y": Y,
                "T_Y": int(row["T_Y"]),
                "D0_eff": int(row["D0_eff"]),
                "exposure_label": "SEEN_DERIVED_FROM_TC064_CERTIFICATES",
                "damped_core_defect_Y": serialize_arb_certified(dcore_arb),
                "U_norm_sq_Y": serialize_arb_certified(u2_arb),
                "four_V_norm_sq_Y": serialize_arb_certified(v4_arb),
                "U_sq_minus_4V_sq_Y": serialize_arb_certified(uv_arb),
                "J_A_Y": serialize_arb_certified(ja_arb),
                "four_J_B_Y": serialize_arb_certified(jb4_arb),
                "U_sq_over_4V_sq": serialize_arb_certified(ratio_uv),
                "J_A_negativity_share_of_damped_defect": serialize_arb_certified(ja_share),
                "M_P0_DAMPED": serialize_arb_certified(m_p0),
                "damped_core_defect_strictly_negative": neg_dcore,
                "U_sq_minus_4V_sq_strictly_negative": neg_uv,
                "dual_formula_intervals_consistent": overlap_ok,
                "verified": row_ok,
            }
        )

    return {
        "exposure_label": "SEEN_DERIVED_FROM_TC064_CERTIFICATES",
        "source_artifact": "data/tc_squarefree_core_correlation.json",
        "key_disambiguation": (
            "Derived damped_core_defect_Y = S_core_Y - 4*J_B_Y = ||U_Y||^2 - 4*||V_Y||^2 - J_A_Y "
            "directly from recorded outward endpoints; strictly distinct from inherited core Gram diagonal D_core_Y."
        ),
        "rows": out_rows,
        "all_rows_verified": all_ok,
    }


def verify_exact_tc065_algebraic_identities() -> Dict[str, Any]:
    """Exhaustive exact integer / `Fraction` / 256-bit Arb checks of the arithmetic identities
    in Theorem 2 and Theorem 4 (`role = EXACT_ALGEBRA`).
    """
    # 1. Paired-station partition, zero-sum, odd prime-power vanishing above T/2, large-prime disjointness
    partition_cutoffs = [1, 2, 3, 6, 10, 18, 32, 64, 77]
    for T in partition_cutoffs:
        om, ph = paired_station_partition(T)
        assert sorted(om + ph) == list(range(1, T + 1))
        assert set(om).isdisjoint(ph)
        # Check against odd_chain_parts + dyadic_chain_exponents
        om_chain = set()
        for u in odd_chain_parts_O_T(T):
            for j in dyadic_chain_exponents_J_u(u, T):
                om_chain.add((4 ** j) * u)
                om_chain.add(2 * (4 ** j) * u)
        assert set(om) == om_chain
        assert sum(liouville_lambda_int(n) for n in om) == 0
        assert sum(liouville_lambda_int(n) for n in ph) == sum(
            liouville_lambda_int(n) for n in range(1, T + 1)
        )
        # Odd prime-power vanishing above T/2
        for p, k in prime_power_pairs_up_to(T):
            if p >= 3 and 2 * (p ** k) > T:
                assert not any(n in om_chain for n in range(p ** k, T + 1, p ** k))
        # Large-prime station disjointness above floor(sqrt(T))
        sT = math.isqrt(T)
        large_primes = [p for p, k in prime_power_pairs_up_to(T) if k == 1 and p > sT]
        seen_n: set[int] = set()
        for p in large_primes:
            for mult in range(p, T + 1, p):
                assert mult not in seen_n
                seen_n.add(mult)

    # 2. Exact pointwise telescoping of openCoreSmoothCoeffS across T, D0, n
    telescoping_cases = 0
    for T in [1, 2, 3, 6, 10, 18, 32]:
        lam = [0] + [liouville_lambda_int(n) for n in range(1, T + 1)]
        R_osc = [Fraction(0)] + [Fraction(d * d + 5 * d + 11, d + 3) for d in range(1, T + 1)]
        for D0 in [0, 1, 2, 3, T - 1, T + 1]:
            D_eff = min(D0, T - 1)
            s_dir = [Fraction(0)] * (2 * T + 1)
            for d in range(D_eff + 1, T):
                for q in range(1, (T // d) + 1):
                    s_dir[d * q] += R_osc[d] * lam[q]
                    s_dir[(d + 1) * q] -= R_osc[d] * lam[q]
            for n in range(1, T + 1):
                val = Fraction(0)
                for e in range(D_eff + 2, min(n, T - 1) + 1):
                    if n % e == 0:
                        val += lam[n // e] * (R_osc[e] - R_osc[e - 1])
                if D_eff + 1 <= T - 1 and n % (D_eff + 1) == 0:
                    val += lam[n // (D_eff + 1)] * R_osc[D_eff + 1]
                if n == T and D_eff + 1 <= T - 1:
                    val -= R_osc[T - 1]
                assert val == s_dir[n]
                telescoping_cases += 1

    # 3. Odd prime-power square-lift parity criterion across (p, m, r, a, b)
    parity_cases = 0
    for p in [3, 5, 7]:
        for m in [1, 2]:
            for r in [0, 1, 2]:
                for a in [1, 3, 5, 7, 15, 21]:
                    for b in [1, 3, 5, 9, 15]:
                        n = (2 ** r) * a * (b * b)
                        lhs_even = (n % (p ** (2 * m)) == 0)
                        rhs_even = (b % (p ** m) == 0)
                        assert lhs_even == rhs_even
                        lhs_odd = (n % (p ** (2 * m - 1)) == 0)
                        rhs_odd = ((a % p == 0) and (b % (p ** (m - 1)) == 0)) or (
                            (a % p != 0) and (b % (p ** m) == 0)
                        )
                        assert lhs_odd == rhs_odd
                        parity_cases += 1

    # 4. Exact divisor identity sum_{e | n} |w_{2,lambda}(e)| = (log n)^2 in 256-bit Arb for 1 <= n <= 120
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        vm = [arb(0)] * 121
        for p, k in prime_power_pairs_up_to(120):
            vm[p ** k] = arb(p).log()
        w2_abs = [arb(0)] * 121
        for e in range(1, 121):
            conv = arb(0)
            for a in range(1, e + 1):
                if e % a == 0:
                    conv += vm[a] * vm[e // a]
            w2_abs[e] = vm[e] * arb(e).log() + conv
        max_w2_res = arb(0)
        for n in range(1, 121):
            tot = arb(0)
            for e in range(1, n + 1):
                if n % e == 0:
                    tot += w2_abs[e]
            res = tot - (arb(n).log() ** 2)
            assert res.contains(arb(0))
            max_w2_res = max_w2_res.union(abs(res))
    finally:
        flint_ctx.prec = saved

    return {
        "role": "EXACT_ALGEBRA",
        "partition_cutoffs_checked": partition_cutoffs,
        "telescoping_triples_checked": telescoping_cases,
        "square_lift_parity_cases_checked": parity_cases,
        "w2_abs_sum_checked_up_to_n": 120,
        "w2_abs_sum_max_residual": serialize_arb_certified(max_w2_res),
        "verified": True,
    }


def verify_section_2_reproduction_algebra_and_cross_checks(
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Run Section 2: TC-064 seen-scale reproduction, exact algebra, and independent 1D cross-checks."""
    seen_rep = derive_tc064_seen_damped_defects_exact(prec_bits=prec_bits)
    exact_alg = verify_exact_tc065_algebraic_identities()

    # Independent cross-validation against TC-064 and TC-061 evaluators at Y in {16, 32, 64}
    cross_rows: List[Dict[str, Any]] = []
    all_cross_ok = True
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        for Y in (16, 32, 64):
            spec = ExactScaleSpec(
                label=str(Y),
                kind="exact_rational",
                rational_factor=Fraction(Y, 1),
                exp_power=Fraction(0, 1),
            )
            cut = certify_exact_scale_cutoffs(spec, base_prec_bits=prec_bits)
            T_y, D0_eff, ceil_tY = cut["T_Y"], cut["D0_eff"], cut["ceil_tau_Y"]
            Y_b = arb(Y)

            new_ev = evaluate_scalar_feature_compensation_1d_arb(
                Y_b, T_y, D0_eff, selberg_table, prec_bits=prec_bits, quad_tol_bits=160, n_panels=8
            )
            old64 = evaluate_squarefree_core_observables_matrix_free_arb(
                Y_b,
                T_y,
                D0_eff,
                ceil_tY,
                selberg_table,
                prec_bits=prec_bits,
                quad_tol_bits=160,
                use_three_zone=False,
                n_panels=8,
            )
            old61 = evaluate_mixed_covariance_point_arb(
                spec, escalation_tier=0, selberg_table=selberg_table
            )

            dcore_from_old64 = +(old64["S_core_Y"] - arb(4) * old64["sum_Bfeat_norm_sq"])
            diff_dcore = +(new_ev["damped_core_defect_Y"] - dcore_from_old64)
            diff_score = +(new_ev["S_core_Y"] - old64["S_core_Y"])
            diff_ja = +(new_ev["J_A_Y"] - old64["sum_A_norm_sq"])
            diff_jb = +(new_ev["J_B_Y"] - old64["sum_Bfeat_norm_sq"])
            diff_e = +(new_ev["E_Y"] - old61["E_Y"])
            diff_dt = +(new_ev["D_tilde_Y"] - old61["D_tilde_Y"])
            diff_j = +(new_ev["J_T_Y"] - old61["J_direct"])

            tol_chk = arb(10) ** (-30)
            row_ok = all(
                bool(abs(d) < tol_chk)
                for d in (
                    diff_dcore,
                    diff_score,
                    diff_ja,
                    diff_jb,
                    diff_e,
                    diff_dt,
                    diff_j,
                    new_ev["S1_budget_residual"],
                    new_ev["S2_budget_residual"],
                    new_ev["S3_budget_residual"],
                    new_ev["E1_budget_residual"],
                    new_ev["E2_budget_residual"],
                    new_ev["E3_budget_residual"],
                )
            )
            all_cross_ok = all_cross_ok and row_ok
            cross_rows.append(
                {
                    "Y": Y,
                    "T_Y": T_y,
                    "D0_eff": D0_eff,
                    "role": "INDEPENDENT_DIRECT_NUMERICAL_VALIDATION",
                    "exposure_label": "SEEN_HISTORICAL_CALIBRATION_SCALE",
                    "damped_core_defect_Y": serialize_arb_certified(new_ev["damped_core_defect_Y"]),
                    "damped_core_defect_diff_vs_tc064": serialize_arb_certified(diff_dcore),
                    "S_core_diff_vs_tc064": serialize_arb_certified(diff_score),
                    "J_A_diff_vs_tc064": serialize_arb_certified(diff_ja),
                    "J_B_diff_vs_tc064": serialize_arb_certified(diff_jb),
                    "E_Y_diff_vs_tc061": serialize_arb_certified(diff_e),
                    "D_tilde_diff_vs_tc061": serialize_arb_certified(diff_dt),
                    "J_T_diff_vs_tc061": serialize_arb_certified(diff_j),
                    "verified": row_ok,
                }
            )
    finally:
        flint_ctx.prec = saved

    return {
        "component_epistemic_map": {
            "seen_derived_from_tc064_certificates": "CERTIFIED_FINITE_OBSERVATION",
            "exact_algebraic_identity_checks": "UNCONDITIONAL_FINITE_ARITHMETIC",
            "independent_evaluator_cross_checks": "CERTIFIED_FINITE_OBSERVATION",
        },
        "epistemic_statuses": [
            "CERTIFIED_FINITE_OBSERVATION",
            "UNCONDITIONAL_FINITE_ARITHMETIC",
        ],
        "section_epistemic_scope_note": (
            "Reproduces damped_core_defect_Y at Y in {512, 576, 960, 1408} strictly from recorded "
            "TC-064 outward decimal endpoints (SEEN_DERIVED_FROM_TC064_CERTIFICATES), exhaustively "
            "checks exact algebraic identities, and cross-validates the new unified 1D Arb evaluator "
            "against independent TC-064 and TC-061 evaluators at Y in {16, 32, 64}."
        ),
        "seen_derived_from_tc064_certificates": seen_rep,
        "exact_algebraic_identity_checks": exact_alg,
        "independent_evaluator_cross_checks": cross_rows,
        "all_section_2_checks_pass": bool(
            seen_rep["all_rows_verified"] and exact_alg["verified"] and all_cross_ok
        ),
    }


# ---------------------------------------------------------------------------
# 4. Section 3: Seen-Scale Route 5 & Route 6 Discovery + Unsigned & Hybrid Controls
# ---------------------------------------------------------------------------


def evaluate_bare_sequence_energy_and_diag_arb(
    Y: int,
    seq_vals: Sequence[int],
    *,
    prec_bits: int = 256,
    quad_tol_bits: int = 160,
    n_panels: int = 8,
) -> Dict[str, arb]:
    """Evaluate bare-Gaussian energy `E_a(Y) = ||Q_{a,T}||_Y^2` and grouped prime-power diagonal
    `D_tilde_a(Y) = sum_{p^k <= T} ||G_{a,T,(p,k)}||_Y^2` in 256-bit Arb for any integer sequence
    `seq_vals[1..T]` (used for the `a(n) = 1` unsigned control and `a_{3}(n)` finite-prime flip control).
    """
    T_y = canonical_cutoff_T_of_Y_exact(Y)
    saved = flint_ctx.prec
    try:
        work = prec_bits + 32
        flint_ctx.prec = work
        tau = _tau_arb()
        log_tau = tau.log()
        a_acb = [acb(0)] + [acb(int(seq_vals[n])) for n in range(1, T_y + 1)]
        pp_packed = [
            (acb(arb(p).log() ** 2), list(range(p ** k, T_y + 1, p ** k)))
            for p, k in prime_power_pairs_up_to(T_y)
        ]
        st_consts = [(n, acb(n) ** (-3), acb(-(arb(n * n) ** (-1)))) for n in range(1, T_y + 1)]

        Yc = acb(arb(Y))
        lgYc = acb(arb(Y).log())
        Yc_52 = Yc ** (acb(5) / acb(2))
        Yc_2 = Yc * Yc
        tol = arb(2) ** (-quad_tol_bits)
        accs = [arb(0), arb(0)]

        for jp in range(n_panels):
            u_lo = log_tau * arb(jp) / arb(n_panels)
            u_hi = log_tau * arb(jp + 1) / arb(n_panels)
            cache: Dict[Any, Tuple[acb, acb]] = {}

            def _ev(u_var: acb, _an: bool) -> Optional[Tuple[acb, acb]]:
                lg = lgYc + u_var
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    return None
                key = (
                    (
                        flint_ctx.prec,
                        u_var.real.mid().man_exp(),
                        u_var.real.rad().man_exp(),
                        u_var.imag.mid().man_exp(),
                        u_var.imag.rad().man_exp(),
                        _an,
                    )
                    if u_var.is_finite()
                    else None
                )
                if key is not None and key in cache:
                    return cache[key]
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_var).exp()
                x2 = Yc_2 * (acb(2) * u_var).exp()
                ph = [acb(0)] * (T_y + 1)
                q_s = acb(0)
                for n_i, inv_n3, neg_inv_n2 in st_consts:
                    pn = x52 * inv_n3 * (x2 * neg_inv_n2).exp()
                    ph[n_i] = pn
                    q_s += a_acb[n_i] * pn
                dt_raw = acb(0)
                for lp2_c, mults in pp_packed:
                    s_c = acb(0)
                    for n_i in mults:
                        s_c += a_acb[n_i] * ph[n_i]
                    dt_raw += lp2_c * (s_c * s_c)
                out = (q_s * q_s, dt_raw * inv_lg2)
                if key is not None:
                    cache[key] = out
                return out

            for idx in range(2):
                def _cb(uv: acb, _an: bool, _i: int = idx) -> acb:
                    r = _ev(uv, _an)
                    if r is None:
                        nb = arb("nan")
                        return acb(nb, nb)
                    return r[_i]

                accs[idx] += acb.integral(_cb, acb(u_lo), acb(u_hi), rel_tol=tol, abs_tol=tol).real

        flint_ctx.prec = prec_bits
        e_a, dt_a = +accs[0], +accs[1]
        four_dt = +(arb(4) * dt_a)
        ratio = +(e_a / four_dt)
        diff = +(e_a - four_dt)
        return {
            "E_seq_Y": e_a,
            "D_tilde_seq_Y": dt_a,
            "four_D_tilde_seq_Y": four_dt,
            "E_minus_4Dtilde_seq_Y": diff,
            "E_over_4Dtilde_seq_Y": ratio,
        }
    finally:
        flint_ctx.prec = saved


def run_section_3_seen_discovery_and_controls_arb(
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Certify Route 5 (`S1, S2, S3, S4`) and Route 6 (`E1, E2, E3`) budgets on already-seen
    discovery scales `Y in {64, 128, 256, 512}`, plus the unsigned `a(n) = 1` scaling-obstruction
    control and finite-prime-flip `a_{3}(n)` diagnostic control (explicitly labeled SEEN / CONTROL).
    """
    seen_rows: List[Dict[str, Any]] = []
    for Y in (64, 128, 256, 512):
        T_y = canonical_cutoff_T_of_Y_exact(Y)
        D0_eff = min(int(math.floor(math.log(Y))), T_y - 1)
        Y_b = arb(Y)
        ev = evaluate_scalar_feature_compensation_1d_arb(
            Y_b, T_y, D0_eff, selberg_table, prec_bits=prec_bits, quad_tol_bits=160, n_panels=12
        )
        orc = certify_pointwise_oracle_residual_lower_bound_arb(
            Y_b, T_y, D0_eff, selberg_table, r_val=Fraction(1, 1), n_subintervals=128, prec_bits=prec_bits
        )
        pp_tot = len(prime_power_pairs_up_to(T_y))
        pp_act = len(active_paired_prime_powers(T_y))
        saved_p = flint_ctx.prec
        try:
            flint_ctx.prec = prec_bits
            s1_op_arb = arb(pp_tot).sqrt()
            s1_act_arb = arb(pp_act).sqrt()
        finally:
            flint_ctx.prec = saved_p
        seen_rows.append(
            {
                "Y": Y,
                "T_Y": T_y,
                "D0_eff": D0_eff,
                "sqrt_T_Y": math.isqrt(T_y),
                "prime_power_count": pp_tot,
                "active_paired_prime_power_count": pp_act,
                "exposure_label": "SEEN_DISCOVERY_NOT_UNSEEN_VALIDATION",
                "U_norm_sq_Y": serialize_arb_certified(ev["U_norm_sq_Y"]),
                "four_V_norm_sq_Y": serialize_arb_certified(ev["four_V_norm_sq_Y"]),
                "J_A_Y": serialize_arb_certified(ev["J_A_Y"]),
                "J_B_Y": serialize_arb_certified(ev["J_B_Y"]),
                "damped_core_defect_Y": serialize_arb_certified(ev["damped_core_defect_Y"]),
                "U_sq_minus_4V_sq_Y": serialize_arb_certified(ev["U_sq_minus_4V_sq_Y"]),
                "E_minus_4Dtilde_Y": serialize_arb_certified(ev["E_minus_4Dtilde_Y"]),
                "S1_op_norm_exact": serialize_arb_certified(s1_op_arb),
                "S1_active_op_norm_exact": serialize_arb_certified(s1_act_arb),
                "S1_four_X_om": serialize_arb_certified(ev["S1_four_X_om"]),
                "S1_O_om_norm_sq": serialize_arb_certified(ev["S1_O_om_norm_sq"]),
                "S1_minus_4_ip_P_O": serialize_arb_certified(ev["S1_minus_4_ip_P_O"]),
                "S1_budget_residual": serialize_arb_certified(ev["S1_budget_residual"]),
                "S2_LV_norm_sq": serialize_arb_certified(ev["S2_LV_norm_sq"]),
                "S2_R_norm_sq": serialize_arb_certified(ev["S2_R_norm_sq"]),
                "S2_4_ip_LV_R": serialize_arb_certified(ev["S2_4_ip_LV_R"]),
                "S2_slack_4_Vsq_minus_LVsq": serialize_arb_certified(ev["S2_slack_4_Vsq_minus_LVsq"]),
                "S2_suff_bound": serialize_arb_certified(ev["S2_suff_bound"]),
                "S2_budget_residual": serialize_arb_certified(ev["S2_budget_residual"]),
                "S3_LV_norm_sq": serialize_arb_certified(ev["S3_LV_norm_sq"]),
                "S3_R_norm_sq": serialize_arb_certified(ev["S3_R_norm_sq"]),
                "S3_4_ip_LV_R": serialize_arb_certified(ev["S3_4_ip_LV_R"]),
                "S3_slack_4_Vsq_minus_LVsq": serialize_arb_certified(ev["S3_slack_4_Vsq_minus_LVsq"]),
                "S3_suff_bound": serialize_arb_certified(ev["S3_suff_bound"]),
                "S3_budget_residual": serialize_arb_certified(ev["S3_budget_residual"]),
                "S4_oracle_r1": orc,
                "E1_T_main": serialize_arb_certified(ev["E1_T_main"]),
                "E1_T_cross": serialize_arb_certified(ev["E1_T_cross"]),
                "E1_T_rem": serialize_arb_certified(ev["E1_T_rem"]),
                "E1_U_rem_norm_sq": serialize_arb_certified(ev["E1_U_rem_norm_sq"]),
                "E1_V_rem_norm_sq": serialize_arb_certified(ev["E1_V_rem_norm_sq"]),
                "E1_fringe_feat_thm_bound": serialize_arb_certified(ev["E1_fringe_feat_thm_bound"]),
                "M_FRINGE_FEAT": serialize_arb_certified(ev["M_FRINGE_FEAT"]),
                "E2_four_P_gt_sq": serialize_arb_certified(ev["E2_four_P_gt_sq"]),
                "E2_four_V_gt_sq": serialize_arb_certified(ev["E2_four_V_gt_sq"]),
                "E2_T_main": serialize_arb_certified(ev["E2_T_main"]),
                "E2_T_cross": serialize_arb_certified(ev["E2_T_cross"]),
                "E2_T_rem": serialize_arb_certified(ev["E2_T_rem"]),
                "E3_T_main": serialize_arb_certified(ev["E3_T_main"]),
                "E3_T_cross": serialize_arb_certified(ev["E3_T_cross"]),
                "E3_T_rem": serialize_arb_certified(ev["E3_T_rem"]),
            }
        )

    # Controls: unsigned a(n) = 1 (proves sequence-blind contractive synthesis fails on alpha > 0)
    # and finite-prime-flip a_{3}(n) = lambda(n)*(-1)^{v_3(n)} (bare-observable Euler-robustness diagnostic)
    unsigned_rows: List[Dict[str, Any]] = []
    flip3_rows: List[Dict[str, Any]] = []
    for Y in (32, 64, 128, 256):
        T_y = canonical_cutoff_T_of_Y_exact(Y)
        seq_one = [0] + [1] * T_y
        u_ev = evaluate_bare_sequence_energy_and_diag_arb(Y, seq_one, prec_bits=prec_bits)
        unsigned_rows.append(
            {
                "Y": Y,
                "T_Y": T_y,
                "control_role": "UNSIGNED_POSITIVE_MEAN_CONTROL_a_eq_1",
                "E_seq_Y": serialize_arb_certified(u_ev["E_seq_Y"]),
                "four_D_tilde_seq_Y": serialize_arb_certified(u_ev["four_D_tilde_seq_Y"]),
                "E_minus_4Dtilde_seq_Y": serialize_arb_certified(u_ev["E_minus_4Dtilde_seq_Y"]),
                "E_over_4Dtilde_seq_Y": serialize_arb_certified(u_ev["E_over_4Dtilde_seq_Y"]),
                "feature_dominated": bool(u_ev["E_minus_4Dtilde_seq_Y"] <= arb(0)),
            }
        )
        seq_a3 = [0] + [
            liouville_lambda_int(n) * ((-1) ** prime_valuation_v_p(n, 3))
            for n in range(1, T_y + 1)
        ]
        f_ev = evaluate_bare_sequence_energy_and_diag_arb(Y, seq_a3, prec_bits=prec_bits)
        flip3_rows.append(
            {
                "Y": Y,
                "T_Y": T_y,
                "control_role": "BARE_FINITE_EULER_FLIP_DIAGNOSTIC_a3_NOT_COMPLETE_BETA_SYSTEM",
                "E_seq_Y": serialize_arb_certified(f_ev["E_seq_Y"]),
                "four_D_tilde_seq_Y": serialize_arb_certified(f_ev["four_D_tilde_seq_Y"]),
                "E_minus_4Dtilde_seq_Y": serialize_arb_certified(f_ev["E_minus_4Dtilde_seq_Y"]),
                "E_over_4Dtilde_seq_Y": serialize_arb_certified(f_ev["E_over_4Dtilde_seq_Y"]),
            }
        )

    # Verify concrete seen-scale refutations on all 6 registered Route 5 & Route 6 candidates:
    # S1: 4*X_om > 0 at Y = 64, 128, 256, 512
    # S2: S2_suff_bound > 0 at Y = 256, 512
    # S3: S3_suff_bound > 0 at Y = 256, 512
    # S4: oracle_r1 certified strictly positive at Y = 128, 256, 512
    # E1: E1_T_main = J_T > 0 at Y = 64
    # E2: E2_T_main > 0 at Y = 64, 128, 256, 512
    by_y = {r["Y"]: r for r in seen_rows}
    seen_refutations = {
        "S1_noncontraction_seen_witness_Y64": bool(
            Fraction(by_y[64]["S1_four_X_om"]["lower_dec"]) > 0
        ),
        "S2_mertens_bound_refuted_seen_witness_Y256": bool(
            Fraction(by_y[256]["S2_suff_bound"]["lower_dec"]) > 0
        ),
        "S3_p2_bound_refuted_seen_witness_Y256": bool(
            Fraction(by_y[256]["S3_suff_bound"]["lower_dec"]) > 0
        ),
        "S4_oracle_zero_residual_refuted_seen_witness_Y256": bool(
            by_y[256]["S4_oracle_r1"]["certified_strictly_positive"]
        ),
        "E1_main_nonpos_refuted_seen_witness_Y64": bool(
            Fraction(by_y[64]["E1_T_main"]["lower_dec"]) > 0
        ),
        "E2_large_prime_main_refuted_seen_witness_Y64": bool(
            Fraction(by_y[64]["E2_T_main"]["lower_dec"]) > 0
        ),
        "unsigned_a1_ratio_exceeds_4_at_Y256": bool(
            Fraction(unsigned_rows[-1]["E_over_4Dtilde_seq_Y"]["lower_dec"]) > 4
        ),
    }

    return {
        "component_epistemic_map": {
            "seen_discovery_rows": "CERTIFIED_FINITE_OBSERVATION",
            "unsigned_control_a_eq_1_rows": "CERTIFIED_FINITE_OBSERVATION",
            "bare_finite_euler_flip_a3_rows": "CERTIFIED_FINITE_OBSERVATION",
            "seen_refutation_checks": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        },
        "epistemic_statuses": [
            "CERTIFIED_FINITE_OBSERVATION",
            "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        ],
        "section_epistemic_scope_note": (
            "All scales in Section 3 were previously exposed in TC-061..TC-064 and are strictly "
            "discovery diagnostics and controls (NEVER unseen validation). Bare sequence controls "
            "(a(n) = 1 and a_3(n)) evaluate bare E_a vs 4*D_tilde_a without substituting Liouville beta_Y."
        ),
        "seen_discovery_rows": seen_rows,
        "unsigned_control_a_eq_1_rows": unsigned_rows,
        "bare_finite_euler_flip_a3_rows": flip3_rows,
        "seen_refutation_checks": seen_refutations,
        "all_section_3_checks_pass": all(seen_refutations.values()),
    }


# ---------------------------------------------------------------------------
# 5. Section 4: Preregistered Unseen Validation (`8` Points + `3` Intervals / `10` Cells)
# ---------------------------------------------------------------------------


def evaluate_tc065_unseen_point_with_escalation(
    point_cfg: Dict[str, Any],
    protocol_obj: Dict[str, Any],
    selberg_table: Dict[str, Any],
) -> Dict[str, Any]:
    """Evaluate a single preregistered unseen `TC-065` point across the protocol escalation ladder."""
    spec = ExactScaleSpec(
        label=point_cfg["label"],
        kind=point_cfg["kind"],
        rational_factor=Fraction(point_cfg["rational_factor"]),
        exp_power=Fraction(point_cfg["exp_power"]),
    )
    pol = protocol_obj["precision_quadrature_and_resource_policy"]
    ladder = pol["escalation_ladder"]
    res_limits = pol["resource_limits"]
    max_wall_s = float(res_limits["max_wall_seconds_per_point"])
    max_rss_mb = float(res_limits["max_rss_megabytes"])

    t0_wall = time.perf_counter()
    escalation_trace: List[Dict[str, Any]] = []
    last_row: Optional[Dict[str, Any]] = None

    for tier_cfg in ladder:
        tier = int(tier_cfg["tier"])
        eff_prec = int(tier_cfg["prec_bits"])
        eff_tol = int(tier_cfg["point_quad_tol_bits"])
        eff_pan = int(tier_cfg["n_panels"])
        t0 = time.perf_counter()

        cut = certify_exact_scale_cutoffs(spec, base_prec_bits=eff_prec)
        T_y, D0_raw, D0_eff, ceil_tY = (
            cut["T_Y"],
            cut["D0_raw"],
            cut["D0_eff"],
            cut["ceil_tau_Y"],
        )

        saved = flint_ctx.prec
        try:
            flint_ctx.prec = eff_prec + 32
            y_b = _frac_to_arb(spec.rational_factor) * (_frac_to_arb(spec.exp_power).exp())
            flint_ctx.prec = eff_prec
            y_b = +y_b

            ev = evaluate_scalar_feature_compensation_1d_arb(
                y_b,
                T_y,
                D0_eff,
                selberg_table,
                r_contraction=Fraction(1, 2),
                prec_bits=eff_prec,
                quad_tol_bits=eff_tol,
                n_panels=eff_pan,
            )
            orc = certify_pointwise_oracle_residual_lower_bound_arb(
                y_b,
                T_y,
                D0_eff,
                selberg_table,
                r_val=Fraction(1, 1),
                n_subintervals=128 if tier == 0 else 256,
                prec_bits=eff_prec,
            )

            verdicts = {
                "TC065-P0-DAMPED": classify_probe_margin_arb(ev["M_P0_DAMPED"])["verdict"],
                "TC065-P-NEG-DAMPED": classify_probe_margin_arb(ev["M_P_NEG_DAMPED"])["verdict"],
                "TC065-P-UV-DOM": classify_probe_margin_arb(ev["M_P_UV_DOM"])["verdict"],
                "TC065-P-E3-MAIN": classify_probe_margin_arb(ev["M_P_E3_MAIN"])["verdict"],
                "TC065-THM-FRINGE-FEAT-BOUND": classify_probe_margin_arb(ev["M_FRINGE_FEAT"])["verdict"],
                "TC065-CAND-S1-UNWEIGHTED-CONTRACTION": classify_probe_margin_arb(ev["S1_four_X_om"])["verdict"],
                "TC065-CAND-S2-MERTENS-SUFF-BOUND": classify_probe_margin_arb(ev["S2_suff_bound"])["verdict"],
                "TC065-CAND-S3-P2-SUFF-BOUND": classify_probe_margin_arb(ev["S3_suff_bound"])["verdict"],
                "TC065-CAND-S4-POINTWISE-ZERO-RESIDUAL": orc[
                    "verdict_for_zero_residual_contractive_pointwise_synthesis"
                ],
                "TC065-CAND-E1-MAIN-NONPOS": classify_probe_margin_arb(ev["E1_T_main"])["verdict"],
                "TC065-CAND-E2-LARGE-PRIME-MAIN-NONPOS": classify_probe_margin_arb(ev["E2_T_main"])["verdict"],
            }

            elapsed = round(time.perf_counter() - t0, 6)
            cum_wall = round(time.perf_counter() - t0_wall, 6)
            rss_info = _measure_process_rss_megabytes()
            escalation_trace.append(
                {
                    "tier": tier,
                    "prec_bits": eff_prec,
                    "quad_tol_bits": eff_tol,
                    "n_panels": eff_pan,
                    "elapsed_sec": elapsed,
                    "tier_wall_seconds": elapsed,
                    "cumulative_wall_seconds": max(elapsed, cum_wall),
                    "current_rss_mb": rss_info["current_rss_mb"],
                    "peak_rss_mb": rss_info["peak_rss_mb"],
                    "peak_rss_measurement_semantics": rss_info.get(
                        "peak_rss_measurement_semantics"
                    ),
                    "verdicts": dict(verdicts),
                }
            )
            res_comp = evaluate_point_resource_compliance(
                escalation_trace, max_wall_sec=max_wall_s, max_rss_mb=max_rss_mb
            )

            pp_tot = len(prime_power_pairs_up_to(T_y))
            pp_act = len(active_paired_prime_powers(T_y))
            last_row = {
                "point_id": point_cfg["point_id"],
                "label": point_cfg["label"],
                "kind": point_cfg["kind"],
                "rational_factor": point_cfg["rational_factor"],
                "exp_power": point_cfg["exp_power"],
                "grid_tier": point_cfg["grid_tier"],
                "prior_exposure_status": point_cfg["prior_exposure_status"],
                "Y_ball": serialize_arb_certified(y_b),
                "T_Y": T_y,
                "D0_raw": D0_raw,
                "D0_eff": D0_eff,
                "ceil_tau_Y": ceil_tY,
                "sqrt_T_Y": math.isqrt(T_y),
                "squarefree_core_count_C_T": len(odd_squarefree_cores_C_T(T_y)),
                "prime_power_count": pp_tot,
                "active_paired_prime_power_count": pp_act,
                "escalation_tier_used": tier,
                "escalation_trace": list(escalation_trace),
                "E_Y": serialize_arb_certified(ev["E_Y"]),
                "D_tilde_Y": serialize_arb_certified(ev["D_tilde_Y"]),
                "log_Y_times_D_tilde": serialize_arb_certified(ev["log_Y_times_D_tilde"]),
                "U_norm_sq_Y": serialize_arb_certified(ev["U_norm_sq_Y"]),
                "V_norm_sq_Y": serialize_arb_certified(ev["V_norm_sq_Y"]),
                "four_V_norm_sq_Y": serialize_arb_certified(ev["four_V_norm_sq_Y"]),
                "J_A_Y": serialize_arb_certified(ev["J_A_Y"]),
                "J_B_Y": serialize_arb_certified(ev["J_B_Y"]),
                "U_sq_minus_4V_sq_Y": serialize_arb_certified(ev["U_sq_minus_4V_sq_Y"]),
                "damped_core_defect_Y": serialize_arb_certified(ev["damped_core_defect_Y"]),
                "S_core_Y": serialize_arb_certified(ev["S_core_Y"]),
                "E_minus_4Dtilde_Y": serialize_arb_certified(ev["E_minus_4Dtilde_Y"]),
                "J_T_Y": serialize_arb_certified(ev["J_T_Y"]),
                "S1_op_norm_exact": serialize_arb_certified(arb(pp_tot).sqrt()),
                "S1_active_op_norm_exact": serialize_arb_certified(arb(pp_act).sqrt()),
                "S1_four_X_om": serialize_arb_certified(ev["S1_four_X_om"]),
                "S1_O_om_norm_sq": serialize_arb_certified(ev["S1_O_om_norm_sq"]),
                "S1_minus_4_ip_P_O": serialize_arb_certified(ev["S1_minus_4_ip_P_O"]),
                "S1_budget_residual": serialize_arb_certified(ev["S1_budget_residual"]),
                "S2_LV_norm_sq": serialize_arb_certified(ev["S2_LV_norm_sq"]),
                "S2_R_norm_sq": serialize_arb_certified(ev["S2_R_norm_sq"]),
                "S2_4_ip_LV_R": serialize_arb_certified(ev["S2_4_ip_LV_R"]),
                "S2_slack_4_Vsq_minus_LVsq": serialize_arb_certified(ev["S2_slack_4_Vsq_minus_LVsq"]),
                "S2_suff_bound": serialize_arb_certified(ev["S2_suff_bound"]),
                "S2_budget_residual": serialize_arb_certified(ev["S2_budget_residual"]),
                "S3_LV_norm_sq": serialize_arb_certified(ev["S3_LV_norm_sq"]),
                "S3_R_norm_sq": serialize_arb_certified(ev["S3_R_norm_sq"]),
                "S3_4_ip_LV_R": serialize_arb_certified(ev["S3_4_ip_LV_R"]),
                "S3_slack_4_Vsq_minus_LVsq": serialize_arb_certified(ev["S3_slack_4_Vsq_minus_LVsq"]),
                "S3_suff_bound": serialize_arb_certified(ev["S3_suff_bound"]),
                "S3_budget_residual": serialize_arb_certified(ev["S3_budget_residual"]),
                "S4_oracle_r1": orc,
                "E1_T_main": serialize_arb_certified(ev["E1_T_main"]),
                "E1_T_cross": serialize_arb_certified(ev["E1_T_cross"]),
                "E1_T_rem": serialize_arb_certified(ev["E1_T_rem"]),
                "E1_U_rem_norm_sq": serialize_arb_certified(ev["E1_U_rem_norm_sq"]),
                "E1_V_rem_norm_sq": serialize_arb_certified(ev["E1_V_rem_norm_sq"]),
                "E1_fringe_feat_thm_bound": serialize_arb_certified(ev["E1_fringe_feat_thm_bound"]),
                "E1_budget_residual": serialize_arb_certified(ev["E1_budget_residual"]),
                "E2_four_P_gt_sq": serialize_arb_certified(ev["E2_four_P_gt_sq"]),
                "E2_four_V_gt_sq": serialize_arb_certified(ev["E2_four_V_gt_sq"]),
                "E2_T_main": serialize_arb_certified(ev["E2_T_main"]),
                "E2_T_cross": serialize_arb_certified(ev["E2_T_cross"]),
                "E2_T_rem": serialize_arb_certified(ev["E2_T_rem"]),
                "E2_budget_residual": serialize_arb_certified(ev["E2_budget_residual"]),
                "E3_T_main": serialize_arb_certified(ev["E3_T_main"]),
                "E3_T_cross": serialize_arb_certified(ev["E3_T_cross"]),
                "E3_T_rem": serialize_arb_certified(ev["E3_T_rem"]),
                "E3_budget_residual": serialize_arb_certified(ev["E3_budget_residual"]),
                "M_P0_DAMPED": serialize_arb_certified(ev["M_P0_DAMPED"]),
                "M_P_NEG_DAMPED": serialize_arb_certified(ev["M_P_NEG_DAMPED"]),
                "M_P_UV_DOM": serialize_arb_certified(ev["M_P_UV_DOM"]),
                "M_P_E3_MAIN": serialize_arb_certified(ev["M_P_E3_MAIN"]),
                "M_FRINGE_FEAT": serialize_arb_certified(ev["M_FRINGE_FEAT"]),
                "probe_verdicts": verdicts,
                "elapsed_sec": elapsed,
                "current_rss_mb": rss_info["current_rss_mb"],
                "peak_rss_mb": rss_info["peak_rss_mb"],
                "peak_rss_measurement_semantics": rss_info.get("peak_rss_measurement_semantics"),
                "resource_compliance": res_comp,
            }
            # Escalate only if any primary/secondary/theorem probe (excluding S4 oracle) is UNRESOLVED
            non_oracle_verdicts = [
                v for k, v in verdicts.items() if k != "TC065-CAND-S4-POINTWISE-ZERO-RESIDUAL"
            ]
            if "UNRESOLVED" not in non_oracle_verdicts:
                break
        finally:
            flint_ctx.prec = saved

    assert last_row is not None
    return last_row


def evaluate_tc065_continuous_interval_split_arb(
    interval_id: str,
    Y_lo_frac: Fraction,
    Y_hi_frac: Fraction,
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Evaluate all TC-065 damped-core, Route 5, and Route 6 observables across `[Y_lo_frac, Y_hi_frac]`
    by splitting into all exact feasible `(T, D_0, D_eff)` cells and recording certified binary
    evaluation-domain coverage (`TC-062R4` standard) and fixed discrete class counts.
    """
    part = derive_exact_interval_cutoff_partition(Y_lo_frac, Y_hi_frac)
    cells = part["feasible_cells"]
    if not cells:
        raise ValueError(f"Empty feasible cutoff partition on [{Y_lo_frac}, {Y_hi_frac}]")

    saved = flint_ctx.prec
    try:
        branches: List[Dict[str, Any]] = []
        union_balls: Dict[str, Optional[arb]] = {
            u_k: None for u_k, _ in REQUIRED_TC065_INTERVAL_UNION_BRANCH_PAIRS
        }

        for cell in cells:
            t_c = int(cell["T_fixed"])
            d0_c = int(cell["D0_raw_fixed"])
            deff_c = int(cell["D0_eff_fixed"])

            flint_ctx.prec = prec_bits + 64
            y_lo_b = _frac_to_arb(Y_lo_frac)
            y_hi_b = _frac_to_arb(Y_hi_frac)
            t_lo_b = (arb(t_c - 1) ** (arb(4) / arb(5))) if t_c > 1 else arb(0)
            t_hi_b = arb(t_c) ** (arb(4) / arb(5))
            d_lo_b = arb(d0_c).exp()
            d_hi_b = arb(d0_c + 1).exp()
            lo_cand = max(
                [y_lo_b.lower(), t_lo_b.lower(), d_lo_b.lower()],
                key=lambda b: _exact_arb_endpoints_as_fractions(b)[0],
            )
            hi_cand = min(
                [y_hi_b.upper(), t_hi_b.upper(), d_hi_b.upper()],
                key=lambda b: _exact_arb_endpoints_as_fractions(b)[1],
            )
            sub_ball_hi = lo_cand.union(hi_cand)

            flint_ctx.prec = prec_bits
            y_sub = +sub_ball_hi
            eval_lo_q, eval_hi_q = _exact_arb_endpoints_as_fractions(y_sub)
            mid_me = y_sub.mid().man_exp()
            rad_me = y_sub.rad().man_exp()

            n_pan = 16 if t_c >= 1024 else (8 if t_c >= 200 else 4)
            ev_br = evaluate_scalar_feature_compensation_1d_arb(
                y_sub,
                t_c,
                deff_c,
                selberg_table,
                r_contraction=Fraction(1, 2),
                prec_bits=prec_bits,
                quad_tol_bits=110,
                n_panels=n_pan,
            )

            for u_k, b_k in REQUIRED_TC065_INTERVAL_UNION_BRANCH_PAIRS:
                cur_u = union_balls[u_k]
                union_balls[u_k] = +ev_br[b_k] if cur_u is None else +(cur_u.union(ev_br[b_k]))

            br_entry: Dict[str, Any] = {
                "branch_role": "REQUIRED_FEASIBLE_SUBDOMAIN",
                "T_fixed": t_c,
                "D0_raw_fixed": d0_c,
                "D0_eff_fixed": deff_c,
                "sqrt_T_fixed": math.isqrt(t_c),
                "squarefree_core_count_C_fixed": len(odd_squarefree_cores_C_T(t_c)),
                "active_paired_prime_power_count_fixed": len(active_paired_prime_powers(t_c)),
                "required_subdomain_notation": cell["subdomain_notation"],
                "Y_sub_ball": serialize_arb_certified(y_sub),
                "evaluated_Y_interval_exact_fractions": [
                    f"{eval_lo_q.numerator}/{eval_lo_q.denominator}",
                    f"{eval_hi_q.numerator}/{eval_hi_q.denominator}",
                ],
                "evaluated_Y_mid_man_exp": [int(mid_me[0]), int(mid_me[1])],
                "evaluated_Y_rad_man_exp": [int(rad_me[0]), int(rad_me[1])],
                "domain_provenance_kind": "EVALUATED_AT_CREATION",
            }
            for _, b_k in REQUIRED_TC065_INTERVAL_UNION_BRANCH_PAIRS:
                br_entry[b_k] = serialize_arb_certified(ev_br[b_k])
            br_entry["TC065_P0_DAMPED_branch_classification"] = classify_probe_margin_arb(
                ev_br["M_P0_DAMPED"]
            )["verdict"]
            br_entry["TC065_P_NEG_DAMPED_branch_classification"] = classify_probe_margin_arb(
                ev_br["M_P_NEG_DAMPED"]
            )["verdict"]
            br_entry["TC065_P_UV_DOM_branch_classification"] = classify_probe_margin_arb(
                ev_br["M_P_UV_DOM"]
            )["verdict"]
            br_entry["TC065_P_E3_MAIN_branch_classification"] = classify_probe_margin_arb(
                ev_br["M_P_E3_MAIN"]
            )["verdict"]
            br_entry["TC065_FRINGE_FEAT_branch_classification"] = classify_probe_margin_arb(
                ev_br["M_FRINGE_FEAT"]
            )["verdict"]
            br_entry["TC065_S1_branch_classification"] = classify_probe_margin_arb(
                ev_br["S1_four_X_om"]
            )["verdict"]
            br_entry["TC065_E2_branch_classification"] = classify_probe_margin_arb(
                ev_br["E2_T_main"]
            )["verdict"]

            y_parsed = _parse_serialized_arb_enclosure_tc062(
                strip_enclosure_arb_for_json(br_entry["Y_sub_ball"])
            )
            dom_audit = _evaluate_branch_domain_admissibility_tc062(
                br_entry,
                y_sub_parsed=y_parsed,
                prescribed_Y_lo=Y_lo_frac,
                prescribed_Y_hi=Y_hi_frac,
                cutoff_triple=(t_c, d0_c, deff_c),
                split_key=interval_id,
            )
            br_entry["branch_domain_audit"] = {
                "admissibility_status": dom_audit["admissibility_status"],
                "coverage_status": dom_audit["coverage_status"],
                "complete_subdomain_coverage": dom_audit["complete_subdomain_coverage"],
                "can_certify_refutation": dom_audit["can_certify_refutation"],
                "domain_evidence_source": dom_audit["domain_evidence_source"],
            }
            branches.append(br_entry)

        out_rec: Dict[str, Any] = {
            "interval_id": interval_id,
            "Y_lo_fraction": f"{Y_lo_frac.numerator}/{Y_lo_frac.denominator}",
            "Y_hi_fraction": f"{Y_hi_frac.numerator}/{Y_hi_frac.denominator}",
            "T_range": list(part["T_range"]),
            "D0_range": list(part["D0_range"]),
            "active_branch_count": len(branches),
            "branches": branches,
        }
        for u_k, _ in REQUIRED_TC065_INTERVAL_UNION_BRANCH_PAIRS:
            ub = union_balls[u_k]
            assert ub is not None
            out_rec[u_k] = serialize_arb_certified(ub)

        out_rec["TC065_P0_DAMPED_interval_classification"] = classify_probe_margin_arb(
            union_balls["union_M_P0_DAMPED"]
        )["verdict"]
        out_rec["TC065_P_NEG_DAMPED_interval_classification"] = classify_probe_margin_arb(
            union_balls["union_M_P_NEG_DAMPED"]
        )["verdict"]
        out_rec["TC065_P_UV_DOM_interval_classification"] = classify_probe_margin_arb(
            union_balls["union_M_P_UV_DOM"]
        )["verdict"]
        out_rec["TC065_P_E3_MAIN_interval_classification"] = classify_probe_margin_arb(
            union_balls["union_M_P_E3_MAIN"]
        )["verdict"]
        out_rec["TC065_FRINGE_FEAT_interval_classification"] = classify_probe_margin_arb(
            union_balls["union_M_FRINGE_FEAT"]
        )["verdict"]
        out_rec["TC065_S1_interval_classification"] = classify_probe_margin_arb(
            union_balls["union_S1_four_X_om"]
        )["verdict"]
        out_rec["TC065_E2_interval_classification"] = classify_probe_margin_arb(
            union_balls["union_E2_T_main"]
        )["verdict"]
        return out_rec
    finally:
        flint_ctx.prec = saved


def _interval_overlap_frac_tc065(a: Dict[str, Any], b_lo: Fraction, b_hi: Fraction) -> bool:
    return bool(a["c_lo"] <= b_hi and b_lo <= a["c_hi"])


def aggregate_tc065_section4_and_derive_outcomes(
    point_rows: Sequence[Dict[str, Any]],
    interval_splits: Dict[str, Dict[str, Any]],
    protocol_obj: Dict[str, Any],
) -> Dict[str, Any]:
    """Fail-closed audit and aggregation over all registered TC-065 unseen points and continuous
    interval splits (enforcing TC-062R4 binary-domain coverage, operand consistency, and union checks).
    """
    sched = protocol_obj["unseen_validation_schedule"]
    expected_point_ids = [p["point_id"] for p in sched["points"]]
    expected_intervals = {
        iv["interval_id"]: (Fraction(iv["Y_lo_fraction"]), Fraction(iv["Y_hi_fraction"]))
        for iv in sched["prescribed_continuous_interval_splits"]
    }
    conflicts: List[Dict[str, Any]] = []

    row_by_id: Dict[str, Dict[str, Any]] = {}
    for row in point_rows:
        pid = row.get("point_id")
        if pid in row_by_id:
            conflicts.append({"conflict_type": "DUPLICATE_POINT_ID", "point_id": pid})
        row_by_id[str(pid)] = row

    missing_points = [pid for pid in expected_point_ids if pid not in row_by_id]
    if missing_points:
        conflicts.append({"conflict_type": "MISSING_UNSEEN_POINTS", "missing": missing_points})

    probe_keys_and_margins = (
        ("TC065-P0-DAMPED", "M_P0_DAMPED"),
        ("TC065-P-NEG-DAMPED", "M_P_NEG_DAMPED"),
        ("TC065-P-UV-DOM", "M_P_UV_DOM"),
        ("TC065-P-E3-MAIN", "M_P_E3_MAIN"),
        ("TC065-THM-FRINGE-FEAT-BOUND", "M_FRINGE_FEAT"),
        ("TC065-CAND-S1-UNWEIGHTED-CONTRACTION", "S1_four_X_om"),
        ("TC065-CAND-S2-MERTENS-SUFF-BOUND", "S2_suff_bound"),
        ("TC065-CAND-S3-P2-SUFF-BOUND", "S3_suff_bound"),
        ("TC065-CAND-E1-MAIN-NONPOS", "E1_T_main"),
        ("TC065-CAND-E2-LARGE-PRIME-MAIN-NONPOS", "E2_T_main"),
    )

    verdict_buckets: Dict[str, List[str]] = {k: [] for k, _ in probe_keys_and_margins}
    verdict_buckets["TC065-CAND-S4-POINTWISE-ZERO-RESIDUAL"] = []

    for pid in expected_point_ids:
        row = row_by_id.get(pid)
        if row is None:
            continue
        pv = row.get("probe_verdicts", {})
        # Operand consistency on point: M_P0_DAMPED = damped_core_defect_Y - log_Y_times_D_tilde
        dc_p = _parse_serialized_arb_enclosure_tc062(row.get("damped_core_defect_Y"))
        ld_p = _parse_serialized_arb_enclosure_tc062(row.get("log_Y_times_D_tilde"))
        m0_p = _parse_serialized_arb_enclosure_tc062(row.get("M_P0_DAMPED"))
        if (
            dc_p is None
            or ld_p is None
            or m0_p is None
            or not _interval_overlap_frac_tc065(
                m0_p, dc_p["c_lo"] - ld_p["c_hi"], dc_p["c_hi"] - ld_p["c_lo"]
            )
        ):
            conflicts.append({"conflict_type": "POINT_MARGIN_OPERAND_MISMATCH", "point_id": pid, "margin": "M_P0_DAMPED"})
        # Operand consistency: damped_core_defect_Y = U_sq_minus_4V_sq_Y - J_A_Y
        uv_p = _parse_serialized_arb_enclosure_tc062(row.get("U_sq_minus_4V_sq_Y"))
        ja_p = _parse_serialized_arb_enclosure_tc062(row.get("J_A_Y"))
        if (
            dc_p is None
            or uv_p is None
            or ja_p is None
            or not _interval_overlap_frac_tc065(
                dc_p, uv_p["c_lo"] - ja_p["c_hi"], uv_p["c_hi"] - ja_p["c_lo"]
            )
        ):
            conflicts.append({"conflict_type": "POINT_DAMPED_IDENTITY_MISMATCH", "point_id": pid})

        for pk, mk in probe_keys_and_margins:
            claimed = pv.get(pk)
            derived_v = _audit_serialized_margin_verdict_tc062(row.get(mk))
            if derived_v == "CONFLICT" or claimed != derived_v:
                conflicts.append(
                    {
                        "conflict_type": "POINT_VERDICT_MISMATCH",
                        "point_id": pid,
                        "probe_id": pk,
                        "claimed": claimed,
                        "derived": derived_v,
                    }
                )
            verdict_buckets[pk].append(derived_v)

        orc = row.get("S4_oracle_r1", {})
        lb_p = _parse_serialized_arb_enclosure_tc062(orc.get("oracle_residual_lower_bound"))
        if lb_p is None:
            orc_v = "CONFLICT"
            conflicts.append({"conflict_type": "MALFORMED_ORACLE_LOWER_BOUND", "point_id": pid})
        else:
            orc_fail = bool(lb_p["c_lo"] > 0)
            orc_v = "FAIL" if orc_fail else "UNRESOLVED"
            if pv.get("TC065-CAND-S4-POINTWISE-ZERO-RESIDUAL") != orc_v:
                conflicts.append(
                    {
                        "conflict_type": "POINT_ORACLE_VERDICT_MISMATCH",
                        "point_id": pid,
                        "claimed": pv.get("TC065-CAND-S4-POINTWISE-ZERO-RESIDUAL"),
                        "derived": orc_v,
                    }
                )
        verdict_buckets["TC065-CAND-S4-POINTWISE-ZERO-RESIDUAL"].append(orc_v)

    # Audit continuous intervals
    interval_probe_map = (
        ("TC065-P0-DAMPED", "union_M_P0_DAMPED", "M_P0_DAMPED", "TC065_P0_DAMPED_interval_classification", "TC065_P0_DAMPED_branch_classification", Fraction(20, 1)),
        ("TC065-P-NEG-DAMPED", "union_M_P_NEG_DAMPED", "M_P_NEG_DAMPED", "TC065_P_NEG_DAMPED_interval_classification", "TC065_P_NEG_DAMPED_branch_classification", Fraction(20, 1)),
        ("TC065-P-UV-DOM", "union_M_P_UV_DOM", "M_P_UV_DOM", "TC065_P_UV_DOM_interval_classification", "TC065_P_UV_DOM_branch_classification", Fraction(20, 1)),
        ("TC065-P-E3-MAIN", "union_M_P_E3_MAIN", "M_P_E3_MAIN", "TC065_P_E3_MAIN_interval_classification", "TC065_P_E3_MAIN_branch_classification", Fraction(20, 1)),
        ("TC065-THM-FRINGE-FEAT-BOUND", "union_M_FRINGE_FEAT", "M_FRINGE_FEAT", "TC065_FRINGE_FEAT_interval_classification", "TC065_FRINGE_FEAT_branch_classification", Fraction(2, 1)),
        ("TC065-CAND-S1-UNWEIGHTED-CONTRACTION", "union_S1_four_X_om", "S1_four_X_om", "TC065_S1_interval_classification", "TC065_S1_branch_classification", Fraction(20, 1)),
        ("TC065-CAND-E2-LARGE-PRIME-MAIN-NONPOS", "union_E2_T_main", "E2_T_main", "TC065_E2_interval_classification", "TC065_E2_branch_classification", Fraction(20, 1)),
    )

    total_branches = 0
    for iv_id, (y_lo_f, y_hi_f) in expected_intervals.items():
        iv = interval_splits.get(iv_id)
        if iv is None:
            conflicts.append({"conflict_type": "MISSING_INTERVAL_SPLIT", "interval_id": iv_id})
            continue
        part = derive_exact_interval_cutoff_partition(y_lo_f, y_hi_f)
        req_triples = [
            (int(c["T_fixed"]), int(c["D0_raw_fixed"]), int(c["D0_eff_fixed"]))
            for c in part["feasible_cells"]
        ]
        branches = iv.get("branches", [])
        total_branches += len(branches)
        got_triples = [
            (int(b["T_fixed"]), int(b["D0_raw_fixed"]), int(b["D0_eff_fixed"]))
            for b in branches
        ]
        if sorted(got_triples) != sorted(req_triples):
            conflicts.append(
                {
                    "conflict_type": "INTERVAL_BRANCH_PARTITION_MISMATCH",
                    "interval_id": iv_id,
                    "expected": req_triples,
                    "got": got_triples,
                }
            )
        union_parsed = {
            u_k: _parse_serialized_arb_enclosure_tc062(iv.get(u_k))
            for u_k, _ in REQUIRED_TC065_INTERVAL_UNION_BRANCH_PAIRS
        }
        for b in branches:
            triple = (int(b["T_fixed"]), int(b["D0_raw_fixed"]), int(b["D0_eff_fixed"]))
            yp = _parse_serialized_arb_enclosure_tc062(b.get("Y_sub_ball"))
            da = _evaluate_branch_domain_admissibility_tc062(
                b,
                y_sub_parsed=yp,
                prescribed_Y_lo=y_lo_f,
                prescribed_Y_hi=y_hi_f,
                cutoff_triple=triple,
                split_key=iv_id,
            )
            if (
                not da["complete_subdomain_coverage"]
                or da["admissibility_status"] != "CERTIFIED_NONEMPTY_INTERSECTION"
                or da["coverage_status"] != "CERTIFIED_COMPLETE_COVERAGE"
            ):
                conflicts.append(
                    {
                        "conflict_type": "INCOMPLETE_BRANCH_DOMAIN_COVERAGE",
                        "interval_id": iv_id,
                        "cutoff_triple": triple,
                        "admissibility_status": da["admissibility_status"],
                        "coverage_status": da["coverage_status"],
                    }
                )
            for u_k, b_k in REQUIRED_TC065_INTERVAL_UNION_BRANCH_PAIRS:
                u_p = union_parsed.get(u_k)
                b_p = _parse_serialized_arb_enclosure_tc062(b.get(b_k))
                if (
                    u_p is None
                    or b_p is None
                    or not _serialized_union_contains_branch_tc062(u_p, b_p)
                ):
                    conflicts.append(
                        {
                            "conflict_type": "UNION_DOES_NOT_CONTAIN_BRANCH",
                            "interval_id": iv_id,
                            "union_key": u_k,
                            "branch_key": b_k,
                        }
                    )
            for pk, _, bk, _, br_cls_k, y0_thresh in interval_probe_map:
                derived_b = _audit_serialized_margin_verdict_tc062(b.get(bk))
                if derived_b == "CONFLICT" or b.get(br_cls_k) != derived_b:
                    conflicts.append(
                        {
                            "conflict_type": "BRANCH_VERDICT_MISMATCH",
                            "interval_id": iv_id,
                            "branch_key": bk,
                            "claimed": b.get(br_cls_k),
                            "derived": derived_b,
                        }
                    )
                if derived_b == "FAIL" and not da["can_certify_refutation"]:
                    conflicts.append(
                        {
                            "conflict_type": "UNCERTIFIED_REFUTATION_ON_INADMISSIBLE_BRANCH",
                            "interval_id": iv_id,
                            "branch_key": bk,
                            "cutoff_triple": triple,
                        }
                    )
                # Only count branches whose evaluated domain meets [y0_thresh, infty)
                if yp is not None and yp["c_hi"] >= y0_thresh:
                    # For a FAIL verdict to certify refutation on [y0_thresh, infty), require
                    # c_lo >= y0_thresh (guaranteed admissible point >= y0_thresh); otherwise conservative UNRESOLVED.
                    if derived_b == "FAIL" and yp["c_lo"] < y0_thresh:
                        verdict_buckets[pk].append("UNRESOLVED")
                    else:
                        verdict_buckets[pk].append(derived_b)
        for pk, uk, _, iv_cls_k, _, y0_thresh in interval_probe_map:
            derived_u = _audit_serialized_margin_verdict_tc062(iv.get(uk))
            if derived_u == "CONFLICT" or iv.get(iv_cls_k) != derived_u:
                conflicts.append(
                    {
                        "conflict_type": "INTERVAL_UNION_VERDICT_MISMATCH",
                        "interval_id": iv_id,
                        "probe_id": pk,
                        "claimed": iv.get(iv_cls_k),
                        "derived": derived_u,
                    }
                )
            if y_lo_f >= y0_thresh:
                verdict_buckets[pk].append(derived_u)

    def _derive_probe_outcome(vlist: Sequence[str]) -> str:
        if conflicts:
            return CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
        if "FAIL" in vlist:
            return "REFUTED_BY_CERTIFIED_WITNESS"
        if vlist and all(v == "PASS" for v in vlist):
            return "SURVIVED_TESTED_POINTS"
        return "INCONCLUSIVE"

    probe_outcomes = {pk: _derive_probe_outcome(vlist) for pk, vlist in verdict_buckets.items()}
    res_limits = protocol_obj["precision_quadrature_and_resource_policy"]["resource_limits"]
    point_res_checks = [
        r["resource_compliance"]
        for r in point_rows
        if isinstance(r.get("resource_compliance"), dict)
    ]
    res_agg = aggregate_section_resource_compliance(
        point_res_checks,
        registered_count=len(expected_point_ids),
        distinct_evaluated_count=len(row_by_id),
    )
    total_wall_sec = round(
        sum(float(r.get("elapsed_sec", 0.0)) for r in point_rows), 6
    )
    max_total_wall_s = float(res_limits["max_total_wall_seconds"])
    res_status = str(res_agg["overall_resource_budget_status"])
    if total_wall_sec > max_total_wall_s:
        res_status = "EXCEEDED"
    res_agg["total_points_wall_seconds"] = total_wall_sec
    res_agg["max_total_wall_seconds"] = max_total_wall_s
    res_agg["resource_compliance_status"] = res_status

    integrity_ok = len(conflicts) == 0
    coverage_complete = len(missing_points) == 0 and len(interval_splits) == len(expected_intervals)
    # Require structural/coverage/resource integrity + proved theorem bound survival; do NOT
    # prejudge unproved empirical probe verdicts as pass/fail requirements.
    all_ok = bool(
        integrity_ok
        and coverage_complete
        and res_status == "WITHIN"
        and probe_outcomes["TC065-THM-FRINGE-FEAT-BOUND"] == "SURVIVED_TESTED_POINTS"
    )
    return {
        "registered_unseen_point_count": len(expected_point_ids),
        "evaluated_unseen_point_count": len(row_by_id),
        "registered_continuous_interval_count": len(expected_intervals),
        "evaluated_continuous_interval_count": len(interval_splits),
        "total_continuous_interval_branches": total_branches,
        "coverage_complete": coverage_complete,
        "certification_integrity_ok": integrity_ok,
        "certification_integrity_conflicts": conflicts,
        "probe_outcomes": probe_outcomes,
        "primary_damped_log_saving_outcome": probe_outcomes["TC065-P0-DAMPED"],
        "resource_compliance": res_agg,
        "resource_compliance_status": res_status,
        "all_section_4_checks_pass": all_ok,
    }


def run_section_4_unseen_validation_and_interval_splits(
    protocol_obj: Dict[str, Any],
    selberg_table: Dict[str, Any],
) -> Dict[str, Any]:
    """Execute all preregistered TC-065 unseen point evaluations and continuous interval splits."""
    sched = protocol_obj["unseen_validation_schedule"]
    point_rows = [
        evaluate_tc065_unseen_point_with_escalation(p_cfg, protocol_obj, selberg_table)
        for p_cfg in sched["points"]
    ]
    interval_splits: Dict[str, Dict[str, Any]] = {}
    for iv_cfg in sched["prescribed_continuous_interval_splits"]:
        iv_id = iv_cfg["interval_id"]
        interval_splits[iv_id] = evaluate_tc065_continuous_interval_split_arb(
            iv_id,
            Fraction(iv_cfg["Y_lo_fraction"]),
            Fraction(iv_cfg["Y_hi_fraction"]),
            selberg_table,
            prec_bits=256,
        )
    agg = aggregate_tc065_section4_and_derive_outcomes(point_rows, interval_splits, protocol_obj)
    return {
        "component_epistemic_map": {
            "holdout_point_evaluations": "CERTIFIED_FINITE_OBSERVATION",
            "continuous_interval_case_splits": "CERTIFIED_FINITE_OBSERVATION",
            "probe_outcomes": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        },
        "epistemic_statuses": [
            "CERTIFIED_FINITE_OBSERVATION",
            "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        ],
        "section_epistemic_scope_note": (
            "Evaluates 8 genuinely unseen TC-065 scales and 3 genuinely unseen cutoff-sensitive "
            "continuous intervals (10 feasible sub-cells) frozen in TC065-SCALAR-FEATURE-COMPENSATION-PROTOCOL-V1 "
            "prior to evaluation. Finite survival never proves a universal bound or RH."
        ),
        "holdout_point_evaluations": point_rows,
        "continuous_interval_case_splits": interval_splits,
        **agg,
    }


# ---------------------------------------------------------------------------
# 6. Section 5: Live Lean 4 Audit, Review Consistency Verifier, & Gate Accounting
# ---------------------------------------------------------------------------


def verify_section_5_lean_audit_and_gate_accounting() -> Dict[str, Any]:
    """Live audit of `formal/RiemannScope/ScalarFeatureCompensation.lean` and `formal/build_report.json`."""
    lean_text = SCALAR_FEATURE_LEAN_PATH.read_text(encoding="utf-8")
    pub_thms = re.findall(r"^theorem\s+([A-Za-z0-9_]+)", lean_text, flags=re.MULTILINE)
    priv_thms = re.findall(r"^private\s+theorem\s+([A-Za-z0-9_]+)", lean_text, flags=re.MULTILINE)
    pub_defs = re.findall(r"^(?:noncomputable\s+)?def\s+([A-Za-z0-9_]+)", lean_text, flags=re.MULTILINE)

    sorry_hits = re.findall(r"\b(?:sorry|admit)\b", lean_text)
    axiom_hits = re.findall(r"^axiom\s+", lean_text, flags=re.MULTILINE)
    banned_pi = re.findall(r"(?i)\bpi\b|Real\.pi|[πΠ]", lean_text)
    banned_k = re.findall(r"\bK_[A-Za-z0-9_]*", lean_text)

    build_report = json.loads(FORMAL_BUILD_REPORT_PATH.read_text(encoding="utf-8"))
    lean_sha = _sha256_lf(SCALAR_FEATURE_LEAN_PATH)
    recorded_sha = build_report.get("formal_source_hashes", {}).get(SCALAR_FEATURE_LEAN_REL)
    build_ok = bool(
        build_report.get("status") == "passed"
        and build_report.get("exit_code") == 0
        and recorded_sha == lean_sha
        and int(build_report.get("total_theorems", 0)) >= 845
    )

    lean_audit = {
        "lean_file": SCALAR_FEATURE_LEAN_REL,
        "lean_file_sha256": lean_sha,
        "public_definition_names": pub_defs,
        "public_definition_count": len(pub_defs),
        "public_theorem_names": pub_thms,
        "public_theorem_count": len(pub_thms),
        "private_helper_theorem_count": len(priv_thms),
        "sorry_or_admit_count": len(sorry_hits),
        "custom_axiom_count": len(axiom_hits),
        "banned_circle_tokens": banned_pi,
        "banned_non_grade_K_tokens": banned_k,
        "formal_build_report_producing_commit": build_report.get("producing_git_commit"),
        "formal_build_report_total_theorems": build_report.get("total_theorems"),
        "formal_build_report_verified": build_ok,
    }
    all_ok = bool(
        pub_thms == EXPECTED_TC065_THEOREMS
        and pub_defs == EXPECTED_TC065_PUBLIC_DEFS
        and len(sorry_hits) == 0
        and len(axiom_hits) == 0
        and len(banned_pi) == 0
        and len(banned_k) == 0
        and build_ok
    )
    return {
        "component_epistemic_map": {
            "lean_module_audit": "CONCRETE_ANALYTIC_IN_LEAN",
            "parent_subgate_status": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        },
        "epistemic_statuses": [
            "CONCRETE_ANALYTIC_IN_LEAN",
            "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        ],
        "section_epistemic_scope_note": (
            "Live audit of ScalarFeatureCompensation.lean against formal/build_report.json. "
            "Preserves SUBGATE-TC-043A = OPEN, rh_proved = False, and global_energy_improvement_claimed = False."
        ),
        "lean_module_audit": lean_audit,
        "parent_subgate": PARENT_SUBGATE_ID,
        "parent_subgate_status": "OPEN",
        "rh_proved": False,
        "global_energy_improvement_claimed": False,
        "all_section_5_checks_pass": all_ok,
    }


def _audit_all_serialized_arb_balls_in_tc065_artifact(
    tree: Dict[str, Any],
) -> Dict[str, Any]:
    """Walk the entire TC-065 artifact and validate EVERY serialized Arb ball via the exact
    3-representation `Fraction` validator `_parse_serialized_arb_enclosure_tc062`. When live
    `enclosure_arb` objects are still attached (at artifact creation time), also verify via
    `verify_all_serialized_arb_in_tree` that every serialized ball encloses its live 256-bit Arb ball.
    """
    live_res = verify_all_serialized_arb_in_tree(tree)
    live_check_ok = bool(live_res["all_enclose_original_256bit_arb_ball"])
    live_check_count = int(live_res["compared_against_live_original_arb_count"])
    req_keys = {"mid_float", "rad_float_outward", "lower_dec", "upper_dec", "arb_ball_str"}
    checked_paths: List[str] = []
    counts_by_section: Dict[str, int] = {}
    failed_paths: List[str] = [f"LIVE_ROUNDTRIP:{p}" for p in live_res.get("failed_paths", [])]

    def _walk(node: Any, cur_path: str) -> None:
        if isinstance(node, dict):
            if any(k in node for k in req_keys):
                if not req_keys.issubset(node.keys()):
                    checked_paths.append(cur_path)
                    failed_paths.append(f"{cur_path}:MISSING_KEYS")
                    return
                checked_paths.append(cur_path)
                if _parse_serialized_arb_enclosure_tc062(node) is None:
                    failed_paths.append(f"{cur_path}:INVALID_3REP_ENCLOSURE")
                else:
                    root_sec = cur_path.split(".", 1)[0].split("[", 1)[0]
                    counts_by_section[root_sec] = counts_by_section.get(root_sec, 0) + 1
                return
            for k, v in node.items():
                if k in ("enclosure_arb", "serialized_arb_self_check"):
                    continue
                _walk(v, f"{cur_path}.{k}" if cur_path else str(k))
        elif isinstance(node, (list, tuple)):
            for idx, item in enumerate(node):
                _walk(item, f"{cur_path}[{idx}]")

    _walk(tree, "")
    all_ok = bool(len(checked_paths) > 0 and len(failed_paths) == 0 and live_check_ok)
    return {
        "total_certified_arb_balls_checked": len(checked_paths),
        "live_arb_enclosure_checked_count": int(live_check_count),
        "live_arb_enclosure_check_passed": bool(live_check_ok),
        "counts_by_section": counts_by_section,
        "failed_paths": failed_paths,
        "verified": all_ok,
    }


def verify_tc065_review_document_consistency(
    artifact: Dict[str, Any],
    review_path: Path = TC_065_REVIEW_DOC_PATH,
) -> Dict[str, Any]:
    """Verify 100% of displayed Arb enclosures in `TC_065` review markdown against JSON via
    `<!-- tc-enclosure: ... -->` tags, zero untagged intervals, valid Lean `#L...` anchors,
    zero circle-half tokens, and honest open-gate guardrails.
    """
    md_text = review_path.read_text(encoding="utf-8")
    raw_tag_comment_count = len(re.findall(r"<!--\s*tc-enclosure:", md_text))
    matched_tag_count = 0
    tagged_checked = 0
    failed_tags: List[str] = []
    fake_padding_hits: List[str] = []
    tag_spans: List[Tuple[int, int]] = []

    for m in re.finditer(
        r"`(\[[^`\]]*\+/-[^`\]]+\])`\s*<!--\s*tc-enclosure:\s*observable=\"([^\"]+)\"\s*params=\"([^\"]*)\"\s*json_path=\"([^\"]+)\"\s*-->",
        md_text,
    ):
        matched_tag_count += 1
        disp_str, obs_name, params_s, jpath = m.group(1), m.group(2), m.group(3), m.group(4)
        tag_spans.append((m.start(1), m.end(1)))
        parts_pm = disp_str.strip("[]").split("+/-")
        mid_part = parts_pm[0].strip().lstrip("+-")
        rad_part = parts_pm[1].strip().lstrip("+-") if len(parts_pm) > 1 else ""
        sig_digits = len(mid_part.replace(".", "").split("e")[0].lstrip("0"))
        rad_digits = len(rad_part.replace(".", "").split("e")[0].lstrip("0"))
        if sig_digits > 45 or rad_digits > 16:
            fake_padding_hits.append(jpath)
        try:
            target, _parent = _resolve_report_path_with_param_check(
                artifact, jpath, params_s, obs_name
            )
            gen_lo = Fraction(target["lower_dec"])
            gen_hi = Fraction(target["upper_dec"])
            disp_lo, disp_hi, *_ = _parse_arb_ball_str_to_fractions(disp_str)
            tagged_checked += 1
            if not (disp_lo <= gen_lo and gen_hi <= disp_hi):
                failed_tags.append(f"{obs_name}@{jpath}")
        except Exception as exc:  # noqa: BLE001
            failed_tags.append(f"{obs_name}@{jpath}:{exc}")

    if matched_tag_count != raw_tag_comment_count:
        failed_tags.append(
            f"unmatched_tc_enclosure_comments:matched_{matched_tag_count}_of_{raw_tag_comment_count}"
        )

    # Detect untagged intervals (including zero-centered `[+/- rad]` and LaTeX `\pm`)
    untagged: List[str] = []
    for m_raw in re.finditer(r"`(\[[^`\]]*\+/-[^`\]]+\])`", md_text):
        if (m_raw.start(1), m_raw.end(1)) not in tag_spans:
            untagged.append(m_raw.group(1))
    for m_ltx in re.finditer(r"(\[[+-]?(?:\d|\s)*\\pm[^\]\n]+\])", md_text):
        untagged.append(m_ltx.group(1))

    # Verify Lean #L... anchors
    lean_anchor_re = re.compile(
        r"\(\.\./\.\./(formal/RiemannScope/[A-Za-z0-9_]+\.lean)#L(\d+)(?:-L(\d+))?\)"
    )
    bad_anchors: List[str] = []
    anchor_count = 0
    for am in lean_anchor_re.finditer(md_text):
        anchor_count += 1
        rel_p = am.group(1)
        l1 = int(am.group(2))
        l2 = int(am.group(3)) if am.group(3) else l1
        fp = REPO_ROOT / rel_p
        if not fp.exists():
            bad_anchors.append(f"{rel_p}:MISSING")
            continue
        nlines = len(fp.read_text(encoding="utf-8").splitlines())
        if not (1 <= l1 <= l2 <= nlines):
            bad_anchors.append(f"{rel_p}#L{l1}-L{l2}:OUT_OF_RANGE({nlines})")

    # Guardrails: zero circle-half tokens, zero non-grade K_ tokens, zero false closure claims
    p_tok = "p" + "i"
    banned_circle = [
        tok
        for tok in ("\\" + p_tok, "\u03c0", "Real." + p_tok, "const_" + p_tok, "math." + p_tok)
        if tok in md_text
    ]
    banned_k = re.findall(r"\bK_[A-Za-z0-9_]+", md_text)
    guardrail_errors: List[str] = []
    if banned_circle:
        guardrail_errors.append(f"BANNED_CIRCLE_HALF_TOKENS:{banned_circle}")
    if banned_k:
        guardrail_errors.append(f"BANNED_NON_GRADE_K_TOKENS:{banned_k[:5]}")
    if re.search(r"rh_proved\s*=\s*true", md_text, flags=re.IGNORECASE):
        guardrail_errors.append("FALSE_RH_PROVED_TRUE")
    if re.search(r"SUBGATE-TC-043A\s*=\s*CLOSED", md_text, flags=re.IGNORECASE):
        guardrail_errors.append("FALSE_SUBGATE_CLOSED")
    if "damped_core_defect_Y" not in md_text or "SEEN_DERIVED_FROM_TC064_CERTIFICATES" not in md_text:
        guardrail_errors.append("MISSING_REQUIRED_CANONICAL_LABELS")
    if fake_padding_hits:
        guardrail_errors.append(f"FAKE_PRECISION_PADDING:{fake_padding_hits[:5]}")

    expected_balls = int(artifact["serialized_arb_self_check"]["total_certified_arb_balls_checked"])
    if f"`{expected_balls}`" not in md_text and str(expected_balls) not in md_text:
        guardrail_errors.append(f"MISSING_TOTAL_BALL_COUNT:{expected_balls}")

    verified = bool(
        raw_tag_comment_count >= 40
        and matched_tag_count == raw_tag_comment_count
        and len(failed_tags) == 0
        and len(untagged) == 0
        and anchor_count >= 5
        and len(bad_anchors) == 0
        and len(guardrail_errors) == 0
    )
    return {
        "review_path": str(review_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "raw_tag_comment_count": raw_tag_comment_count,
        "matched_tag_count": matched_tag_count,
        "tagged_and_checked_count": tagged_checked,
        "failed_tags": failed_tags,
        "untagged_intervals": untagged,
        "lean_anchor_count": anchor_count,
        "bad_lean_anchors": bad_anchors,
        "guardrail_errors": guardrail_errors,
        "verified": verified,
    }


# ---------------------------------------------------------------------------
# 7. Full Artifact Generation & Verification Entrypoint
# ---------------------------------------------------------------------------


def generate_task_tc065_artifact(
    output_path: Path = SCALAR_FEATURE_ARTIFACT_PATH,
) -> Dict[str, Any]:
    """Generate and self-audit `data/tc_scalar_feature_compensation.json`."""
    sec1 = verify_section_1_protocols_and_premise_chain()
    proto_obj = verify_frozen_tc065_protocol_immutability()["protocol_object"]

    max_T = max(
        [canonical_cutoff_T_of_Y_exact(512)]
        + [
            int(p["expected_cutoffs"]["T_Y"])
            for p in proto_obj["unseen_validation_schedule"]["points"]
        ]
        + [
            max(c[0] for c in iv["expected_feasible_cells"])
            for iv in proto_obj["unseen_validation_schedule"]["prescribed_continuous_interval_splits"]
        ]
    )
    selberg_table = compute_selberg_centered_remainder_table_fast_arb(max_T, prec_bits=320)

    sec2 = verify_section_2_reproduction_algebra_and_cross_checks(selberg_table, prec_bits=256)
    sec3 = run_section_3_seen_discovery_and_controls_arb(selberg_table, prec_bits=256)
    sec4 = run_section_4_unseen_validation_and_interval_splits(proto_obj, selberg_table)
    sec5 = verify_section_5_lean_audit_and_gate_accounting()

    num_commit = _get_git_head_commit()
    build_report = json.loads(FORMAL_BUILD_REPORT_PATH.read_text(encoding="utf-8"))

    all_pass = bool(
        sec1["all_section_1_checks_pass"]
        and sec2["all_section_2_checks_pass"]
        and sec3["all_section_3_checks_pass"]
        and sec4["all_section_4_checks_pass"]
        and sec5["all_section_5_checks_pass"]
    )

    artifact: Dict[str, Any] = {
        "schema_version": "1.0.0",
        "task_id": TASK_TC_065_ID,
        "epic_id": EPIC_TC_042_ID,
        "parent_subgate": PARENT_SUBGATE_ID,
        "proposed_branch": PROPOSED_TC065_BRANCH,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "circle_constant_convention": "tau_exclusively",
        "execution_and_certification_status": (
            "CERTIFIED_COMPLETE_NO_UNRESOLVED_CONFLICTS"
            if all_pass
            else "CERTIFICATION_INCOMPLETE_OR_FAILED"
        ),
        "primary_damped_log_saving_outcome": sec4["primary_damped_log_saving_outcome"],
        "resource_compliance_status": sec4["resource_compliance_status"],
        "completion_outcome_code": (
            "SCALAR_FEATURE_COMPENSATION_PROOF_ATTEMPT_COMPLETED_SUBGATE_OPEN"
            if all_pass
            else "INCOMPLETE"
        ),
        "research_outcome_class": (
            "NEW_UNCONDITIONAL_FRINGE_OPERATOR_AND_OBSTRUCTION_THEOREMS_PROVED_GATE_OPEN"
        ),
        "parent_subgate_status": "OPEN",
        "rh_proved": False,
        "global_energy_improvement_claimed": False,
        "provenance": {
            "accepted_tc064r_tip": ACCEPTED_TC064R_TIP,
            "reviewed_tc064_tip": REVIEWED_TC064_TIP,
            "reviewed_main_baseline": REVIEWED_MAIN_BASELINE_TC065,
            "protocol_registration_commit": FROZEN_TC065_PROTOCOL_REGISTRATION_COMMIT,
            "protocol_sha256": FROZEN_TC065_PROTOCOL_SHA256,
            "formal_producing_git_commit": build_report.get("producing_git_commit"),
            "numerical_producing_git_commit": num_commit,
            "validation_git_commit": num_commit,
            "formal_build_report_hash": build_report.get("report_hash"),
        },
        "section_1_protocols_and_premise_chain": sec1,
        "section_2_seen_reproduction_algebra_and_cross_checks": sec2,
        "section_3_seen_discovery_and_controls": sec3,
        "section_4_unseen_validation_and_interval_splits": sec4,
        "section_5_lean_audit_and_gate_accounting": sec5,
        "all_mathematical_and_numerical_checks_pass": all_pass,
    }

    arb_audit = _audit_all_serialized_arb_balls_in_tc065_artifact(artifact)
    scope_results = {
        k: verify_section_epistemic_scope_metadata(artifact[k])
        for k in (
            "section_1_protocols_and_premise_chain",
            "section_2_seen_reproduction_algebra_and_cross_checks",
            "section_3_seen_discovery_and_controls",
            "section_4_unseen_validation_and_interval_splits",
            "section_5_lean_audit_and_gate_accounting",
        )
    }
    scope_ok = all(ok for ok, _ in scope_results.values())
    artifact["serialized_arb_self_check"] = {
        **arb_audit,
        "epistemic_scope_metadata_verified": scope_ok,
        "epistemic_scope_details": {k: msg for k, (_, msg) in scope_results.items()},
    }
    artifact["all_mathematical_and_numerical_checks_pass"] = bool(
        all_pass and arb_audit["verified"] and scope_ok
    )
    if not artifact["all_mathematical_and_numerical_checks_pass"]:
        artifact["execution_and_certification_status"] = "CERTIFICATION_INCOMPLETE_OR_FAILED"

    clean_artifact = strip_enclosure_arb_for_json(artifact)
    output_path.write_text(
        json.dumps(clean_artifact, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )
    return clean_artifact


if __name__ == "__main__":
    art = generate_task_tc065_artifact()
    print(
        json.dumps(
            {
                "task_id": art["task_id"],
                "all_pass": art["all_mathematical_and_numerical_checks_pass"],
                "total_arb_balls": art["serialized_arb_self_check"][
                    "total_certified_arb_balls_checked"
                ],
                "probe_outcomes": art["section_4_unseen_validation_and_interval_splits"][
                    "probe_outcomes"
                ],
                "resource_compliance": art["resource_compliance_status"],
            },
            indent=2,
        )
    )
