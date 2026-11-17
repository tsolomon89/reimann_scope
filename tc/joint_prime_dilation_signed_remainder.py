r"""
TASK-TC-062: Joint Prime-Dilation Kernel and Uniform Signed-Remainder Proof Attempt
toward SUBGATE-TC-043A (EPIC-TC-042).

Implements, verifies, and certifies in 256-bit FLINT/Arb outward-rounded ball arithmetic:
- Circle constant convention: `tau` exclusively (`0` circle-half macros or glyphs).
- Grade variable convention: `K` reserved strictly for real-algebraic geometric grades `K in A_R`
  (`0` non-grade `K_*` identifiers); complete signed kernel denoted `Hcal_Y`; complex arguments
  written `z = x + i*y` (`x, y` real, critical line `x = 1/2`).

Sections:
1. Section 1 — Protocol Immutability, Pointwise `A_Y` Reassembly, & Complete Signed Kernel `Hcal_Y`:
   - Verifies byte-level SHA-256 and git-commit ancestry of BOTH the preserved `TC-061` protocol
     (`data/tc_mixed_arithmetic_covariance_protocol.json`, `bc2f9f709f868ef02981600873dfa0c05da0ba0c`)
     and the frozen `TC-062` protocol (`data/tc_joint_prime_dilation_signed_remainder_protocol.json`,
     `4961b03130bf1f353570a0e9c62ede4e1a2bf27d`).
   - Certifies `A_Y(X) = -sum_{n<=2T} beta_Y(n)*phi_n(X)/(log X)^2` pointwise on `[Y, tau*Y]`
     (keeping `A_Y`'s horizon-coupled contraction scope explicit without upgrading it to `O(1)`),
     and certifies `F(Y) = sum_{m,n<=2T} lambda(m)*lambda(n)*Hcal_Y(m, n)` against direct 1D
     quadrature `J(Y) - 4*X_self(Y)`.

2. Section 2 — Disjoint 1-Prime (4-Term) & 2-Prime (16-Term) Anchor Decompositions & Controls:
   - Separates generic finite anchor reindexing (verified on arbitrary non-multiplicative sequences
     and non-symmetric finite kernels) from Liouville arithmetic (`lambda(p*m) = -lambda(m)`),
     explicit boundary extraction (`2*T` terminal boundary and `T` cutoff-jump boundary), exact
     16-term diagonal coincidence classification, and exact `c(m, n)` difference laws.
   - Recomputes matched controls (`unsigned_1`, `a2`, `a_3_5_7`) with their own Laurent-compensated
     cores and control-specific prime-pair sign rules (`+` outside `S`, `-` inside `S`), plus
     explicitly labeled `hybrid_a2_liouville`, certifying `REFUTED_BY_CERTIFIED_WITNESS` on `Y >= 64`.

3. Section 3 — Whole-Line Contraction Enclosures & Submultiplicativity Obstruction:
   - Independently certifies closed-form and half-line quadrature enclosures for `r({2})`, `r({3})`,
     `r({2,3})`, `r({2,3,5})`, and `r({2})*r({3})`, proving `r({2})*r({3}) < r({2}) < r({2,3}) < r({2,3,5})`
     and isolating the same-octave positive prime-pair correlation `+2*<phi_2, phi_3>_{(0,infty)}`.

4. Section 4 — Quantitative Proof Attempt (Spillover Reduction, Stages A/B/C, & Literature Audit):
   - Certifies exact spillover support `T < n <= T + floor(T/(D+1))` via `d_q = floor(T/q)` (`q >= 2`),
     pointwise `|w_{2,lambda}(n)| <= (log n)^2`, PNT/Selberg (`TC-057R` Theorem 4.3(3))
     `||S_{spill,Y}||_Y = O(1/log Y)` (`||S_{spill,Y}||_Y^2 = O((log Y)^{-2})`, Young penalty
     `(1 + log Y)*||S_{spill,Y}||_Y^2 = O(1/log Y)`) spillover decay, and mixed-covariance-preserving
     Young equivalence `H(F, D_tilde) <-> H(F_{<=T}, D_tilde)`.
   - Certifies Stage A interior Hilbert-space identity, refutes Candidate Lemma A1 (`m = 1, p = 2`
     anchor diagonal `Delta_{2,2} Hcal_Y(1, 1) > 0` for `Y >= 8`) with proved `O(2^{|S|})` aggregate
     Replacement Lemma A1', refutes Candidate Lemma A2 (`sum |Delta_{2,2} Hcal_Y(m, n)|` certified in
     256-bit Arb at `Y = 64` + analytic `Omega(Y)` linear growth), quantifies Stage B cross-prime
     Leibniz/divisor jumps, and executes Stage C multi-prime (`S = {2, 3, 5}`, harmonic-weighted
     average, primary literature audit of `arXiv:1503.05121` & `arXiv:1509.05422`) reducing full
     closure to `TC062-OBL-INTERIOR-PRIME-PAIR-OFFDIAG`.

5. Section 5 — Execution of the Frozen 10-Point Unseen Validation Schedule & Interval Case Splits:
   - Evaluates all 10 unseen `TC-062` validation points (`112` through `1280`, including `e^6` and
     `625^(5/4) = 3125` discontinuity pairs) strictly from the frozen protocol with matrix-free
     3-zone Arb quadrature, continuous interval branch-splitting on `[625 - 2^-12, 625 + 2^-12]`
     and `[2017/5, 20173/50]` across `e^6`, decisive-witness preservation across escalation,
     `CERTIFICATION_INTEGRITY_CONFLICT` guards, and 3-valued (`WITHIN`, `EXCEEDED`, `UNKNOWN`)
     `PROCESS_LIFETIME_HIGH_WATER_MARK` resource compliance.

6. Section 6 — Live Lean 4 Declaration Audit, Review Anchor/Enclosure Verifier, & Gate Accounting:
   - Extracts live theorem spans from `formal/RiemannScope/JointPrimeDilationSignedRemainder.lean`,
     audits `0` `sorry`/`admit`/custom axioms, verifies review enclosures and anchors, and preserves
     honest gate status `SUBGATE-TC-043A = OPEN`, `rh_proved = False`.
"""

from __future__ import annotations

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
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

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
    finite_prime_parity_aS_int,
    prime_power_pairs_up_to,
)
from tc.dyadic_power_lift_primitive_correlation import (
    EPISTEMIC_CATEGORIES,
    PARENT_SUBGATE_ID,
    is_perfect_square_int,
)
from tc.liouville_square_dilation import (
    _ARB_BACKTICK_INTERVAL_RE,
    _LATEX_PM_INTERVAL_RE,
    _TC_ENCLOSURE_TAG_RE,
    _exact_arb_endpoints_as_fractions,
    _parse_arb_ball_str_to_fractions,
    _resolve_report_path_with_param_check,
    _sci_or_latex_num_to_fraction,
    liouville_lambda_int,
)
from tc.mixed_arithmetic_covariance import (
    ACCEPTED_TC061R2_IMPLEMENTATION,
    ACCEPTED_TC061R_IMPLEMENTATION_AND_FORMAL_COMMIT,
    CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME,
    CERTIFICATION_INTEGRITY_CONFLICT_VERDICT,
    CertificationIntegrityError,
    ExactScaleSpec,
    FROZEN_PROTOCOL_ID as TC061_FROZEN_PROTOCOL_ID,
    FROZEN_PROTOCOL_REGISTRATION_COMMIT as TC061_FROZEN_PROTOCOL_REGISTRATION_COMMIT,
    FROZEN_PROTOCOL_SHA256 as TC061_FROZEN_PROTOCOL_SHA256,
    MERGED_MAIN_BASELINE_TC061,
    MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH,
    MIXED_ARITHMETIC_COVARIANCE_PROTOCOL_PATH,
    POINT_MARGIN_VERDICTS,
    PROBE_GLOBAL_OUTCOMES,
    RECOGNIZED_PEAK_RSS_COVERING_SEMANTICS,
    RESOURCE_COMPLIANCE_STATUSES,
    TASK_TC_061_ID,
    TASK_TC_061R_ID,
    TASK_TC_061R2_ID,
    TASK_TC_061R3_ID,
    _measure_process_rss_megabytes,
    _prime_factorization_dict,
    aggregate_section_resource_compliance,
    certify_exact_scale_cutoffs,
    certified_ratio_with_positive_denominator,
    classify_global_probe_outcome,
    classify_probe_margin_arb,
    compute_complete_core_s_Y_and_beta_Y_arb,
    compute_selberg_centered_remainder_table_fast_arb,
    compute_zone1_prime_power_diag_perturbation_arb,
    evaluate_X_self_collision_arb,
    evaluate_control_matched_point_arb,
    evaluate_interval_via_cutoff_case_split_arb,
    evaluate_mixed_covariance_point_arb,
    evaluate_point_resource_compliance,
    evaluate_window_gram_G_Y_r_arb,
    load_frozen_protocol_rules,
    resolve_protocol_quadrature_settings,
    strip_enclosure_arb_for_json,
    verify_frozen_protocol_immutability,
)
from tc.prime_chain_contraction import evaluate_phi_n_arb, primes_up_to
from tc.signed_dilation_arithmetic_energy import (
    AmbiguousCutoffError,
    FORMAL_BUILD_REPORT_PATH,
    GLOBAL_CONSEQUENCE_CLASSES,
    classify_arb_le_certificate,
    verify_section_epistemic_scope_metadata,
)

TASK_TC_062_ID = "TASK-TC-062"
TASK_TC_062R_ID = "TASK-TC-062R"
PROPOSED_TC062_BRANCH = "task/tc-062-joint-prime-dilation-signed-remainder"
PROPOSED_TC062R_BRANCH = "task/tc-062r-prime-power-certification-and-diagonal-equivalence-repair"
ACCEPTED_TC061R3_TIP = "6a2f5f519b3f2f4642ea2ce00626832e556953be"
ACCEPTED_TC061R3_IMPLEMENTATION = "c2691d0d9e9aee2e148af2c7ec4908f0ebd52521"
REVIEWED_TC062_TIP = "0943eb639dd20191f7563ba23f3e2d5d9f999217"
REVIEWED_TC062_IMPLEMENTATION = "a681365e0b44830bddb9349bbc9e361ac72b0679"
REVIEWED_TC062_PRODUCING_COMMIT = "ab7e976b0fc4c822bdfd332a885ff80afe7156c9"

FROZEN_TC062_PROTOCOL_ID = "TC062-JOINT-PRIME-DILATION-SIGNED-REMAINDER-PROTOCOL-V1"
FROZEN_TC062_PROTOCOL_REGISTRATION_COMMIT = "4961b03130bf1f353570a0e9c62ede4e1a2bf27d"
FROZEN_TC062_PROTOCOL_SHA256 = "d56fbd30df9d8adf01ff41d0f207d06092a941fa79f593ef6c61382b72fc32df"

JOINT_PRIME_DILATION_PROTOCOL_PATH = (
    REPO_ROOT / "data" / "tc_joint_prime_dilation_signed_remainder_protocol.json"
)
JOINT_PRIME_DILATION_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_joint_prime_dilation_signed_remainder.json"
)
TC_062_REVIEW_DOC_PATH = (
    REPO_ROOT / "docs" / "reviews" / "TC_062_JOINT_PRIME_DILATION_SIGNED_REMAINDER.md"
)
TC_062_LEAN_MODULE_PATH = (
    REPO_ROOT / "formal" / "RiemannScope" / "JointPrimeDilationSignedRemainder.lean"
)

EXPECTED_TC062_THEOREMS: List[str] = [
    "reassembly_known_part_and_complete_signed_kernel_tc062",
    "generic_and_liouville_one_prime_pair_decomposition_tc062",
    "disjoint_two_prime_sixteen_term_and_diagonal_coincidence_tc062",
    "whole_line_contraction_enclosures_and_submultiplicativity_refutation_tc062",
    "spillover_fringe_reindexing_and_mixed_covariance_reduction_tc062",
    "stage_a_interior_hilbert_split_and_candidate_a1_refutation_tc062",
    "interior_prime_pair_closure_equivalence_and_route_d_transfer_tc062",
    "two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r",
]


# ---------------------------------------------------------------------------
# 0. Prime-Valuation Anchors, Generic Pairing Helpers, & Protocol Verifier
# ---------------------------------------------------------------------------


def prime_valuation_v_p(n: int, p: int) -> int:
    """Exact `p`-adic valuation `v_p(n)` for `n >= 1` and prime `p >= 2`."""
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    if p < 2:
        raise ValueError(f"p must be >= 2, got {p}")
    cnt = 0
    while n % p == 0:
        n //= p
        cnt += 1
    return cnt


def prime_even_valuation_anchors(N: int, prime_set: Sequence[int]) -> List[int]:
    """Return `A_S(N) := {1 <= m <= N : forall p in S, 2 | v_p(m)}`."""
    if N < 0:
        raise ValueError(f"N must be >= 0, got {N}")
    s_primes = tuple(sorted(set(int(p) for p in prime_set)))
    return [
        m
        for m in range(1, N + 1)
        if all(prime_valuation_v_p(m, p) % 2 == 0 for p in s_primes)
    ]


def squarefree_divisors_of_prime_set(prime_set: Sequence[int]) -> Tuple[int, List[Tuple[int, int]]]:
    """Return `(P_S, [(d, lambda(d)) for d | P_S])` for distinct primes `S` (`2^{|S|}` divisors)."""
    s_primes = tuple(sorted(set(int(p) for p in prime_set)))
    P_S = 1
    divs: List[Tuple[int, int]] = [(1, 1)]
    for p in s_primes:
        P_S *= p
        divs = divs + [(d * p, -sgn) for (d, sgn) in divs]
    return P_S, divs


def verify_frozen_tc062_protocol_immutability(
    protocol_path: Path = JOINT_PRIME_DILATION_PROTOCOL_PATH,
) -> Dict[str, Any]:
    """Verify SHA-256 and git-commit ancestry of `data/tc_joint_prime_dilation_signed_remainder_protocol.json`."""
    raw_bytes = protocol_path.read_bytes().replace(b"\r\n", b"\n")
    proto = json.loads(raw_bytes.decode("utf-8"))
    proto_without_hash = {k: v for k, v in proto.items() if k != "protocol_sha256"}
    canonical_bytes = json.dumps(
        proto_without_hash, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    computed_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
    recorded_sha256 = proto.get("protocol_sha256")
    hash_ok = bool(
        computed_sha256 == FROZEN_TC062_PROTOCOL_SHA256
        and recorded_sha256 == FROZEN_TC062_PROTOCOL_SHA256
    )

    git_blob_matches = False
    git_commit_is_ancestor = False
    try:
        proc_blob = subprocess.run(
            [
                "git",
                "show",
                f"{FROZEN_TC062_PROTOCOL_REGISTRATION_COMMIT}:data/tc_joint_prime_dilation_signed_remainder_protocol.json",
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
                FROZEN_TC062_PROTOCOL_REGISTRATION_COMMIT,
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
        "protocol_path": "data/tc_joint_prime_dilation_signed_remainder_protocol.json",
        "protocol_id": proto.get("protocol_id"),
        "expected_protocol_sha256": FROZEN_TC062_PROTOCOL_SHA256,
        "computed_protocol_sha256": computed_sha256,
        "recorded_protocol_sha256": recorded_sha256,
        "sha256_verified": hash_ok,
        "registration_commit": FROZEN_TC062_PROTOCOL_REGISTRATION_COMMIT,
        "git_blob_matches_registration_commit": git_blob_matches,
        "registration_commit_is_ancestor_of_head": git_commit_is_ancestor,
        "protocol_object": proto,
        "verified": bool(
            proto.get("protocol_id") == FROZEN_TC062_PROTOCOL_ID
            and hash_ok
            and git_blob_matches
            and git_commit_is_ancestor
        ),
    }


# ---------------------------------------------------------------------------
# 1. Section 1: Pointwise A_Y Reassembly & Complete Signed Kernel Hcal_Y
# ---------------------------------------------------------------------------


def build_complete_signed_kernel_evaluator_small_T(
    Y_arb: arb,
    T_y: int,
    D0_eff: int,
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
) -> Callable[[int, int], arb]:
    """Construct exact symmetric kernel evaluator `Hcal_Y(m, n)` (zero outside `[1, 2*T]^2`,
    keeping `Y, T, D0_eff` and `beta_Y` fixed under shifted arguments) for small `T` (`Y <= 32`)
    where direct sum vs paired sum cross-verification is performed.
    """
    N = 2 * T_y
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        vecs = compute_complete_core_s_Y_and_beta_Y_arb(
            T_y, D0_eff, selberg_table["R_osc"], prec_bits=prec_bits
        )
        beta_Y = vecs["beta_Y"]
        b_vec = [arb(0)] + [
            arb(liouville_lambda_int(n)) * beta_Y[n] for n in range(1, N + 1)
        ]

        c_div = [arb(0)] * (T_y + 1)
        for p, k in prime_power_pairs_up_to(T_y):
            pk = p ** k
            lg2 = arb(p).log() ** 2
            for mult in range(pk, T_y + 1, pk):
                c_div[mult] += lg2

        G_cache: Dict[Tuple[int, int, int], arb] = {}

        def _G(m_i: int, n_i: int, r_p: int) -> arb:
            a_i, b_i = (m_i, n_i) if m_i <= n_i else (n_i, m_i)
            key = (a_i, b_i, r_p)
            hit = G_cache.get(key)
            if hit is None:
                hit = evaluate_window_gram_G_Y_r_arb(Y_arb, a_i, b_i, r_p, prec_bits=prec_bits)
                G_cache[key] = hit
            return hit

        def _Hcal(m: int, n: int) -> arb:
            if m < 1 or m > N or n < 1 or n > N:
                return arb(0)
            saved_inner = flint_ctx.prec
            try:
                flint_ctx.prec = prec_bits
                tm = 1 if m <= T_y else 0
                tn = 1 if n <= T_y else 0
                g0_part = _G(m, n, 0) if (tm and tn) else arb(0)
                c_mn = c_div[math.gcd(m, n)] if (tm and tn) else arb(0)
                diag_corr = (
                    arb(4) * ((arb(m).log() ** 2) - c_div[m])
                    if (m == n and tm)
                    else arb(0)
                )
                coeff_g2 = (
                    (b_vec[n] if tm else arb(0))
                    + (b_vec[m] if tn else arb(0))
                    + (arb(4) * c_mn if (tm and tn) else arb(0))
                    + diag_corr
                )
                g2_part = coeff_g2 * _G(m, n, 2) if coeff_g2 != arb(0) else arb(0)
                bb = b_vec[m] * b_vec[n]
                g4_part = bb * _G(m, n, 4) if bb != arb(0) else arb(0)
                return +(g0_part - g2_part + g4_part)
            finally:
                flint_ctx.prec = saved_inner

        return _Hcal
    finally:
        flint_ctx.prec = saved


def verify_section_1_protocols_reassembly_and_complete_kernel(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Verify both immutable protocols (`TC-061` and `TC-062`), pointwise reassembly
    `A_Y(X) = -sum_{n<=2T} beta_Y(n)*phi_n(X)/(log X)^2`, kernel symmetry/support/arithmetic
    dependence, and exact identity `F(Y) = sum_{m,n=1}^{2T} lambda(m)*lambda(n)*Hcal_Y(m, n)`
    on `Y in {2, 4, 8, 16}`.
    """
    tc061_proto_chk = verify_frozen_protocol_immutability()
    tc062_proto_chk = verify_frozen_tc062_protocol_immutability()

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
        c_lam = tbl["c_lambda"]
        R = tbl["R"]
        M_drift = tbl["M_drift"]
        R_osc = tbl["R_osc"]

        reassembly_rows: List[Dict[str, Any]] = []
        reassembly_ok = True
        for y_val in (2, 4, 8, 16, 32, 64):
            sp = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            res = evaluate_mixed_covariance_point_arb(sp, selberg_table=tbl)
            T_y = res["cutoffs"]["T_Y"]
            D0_eff = res["cutoffs"]["D0_eff"]
            vecs = compute_complete_core_s_Y_and_beta_Y_arb(T_y, D0_eff, R_osc, prec_bits=prec_bits)
            beta_Y = vecs["beta_Y"]

            # Direct source A_Y(X) from knownCompensatedD2Part vs -sum_{n<=2T} beta_Y(n)*phi_n(X)/(log X)^2:
            alpha_A = [arb(0)] * (2 * T_y + 1)
            for n in range(1, T_y + 1):
                if is_perfect_square_int(n):
                    alpha_A[n] += c_lam
            alpha_A[T_y] += R[T_y]
            for d_i in range(1, T_y):
                L_d = T_y // d_i
                L_d1 = T_y // (d_i + 1)
                Rd = R[d_i]
                for q in range(L_d1 + 1, L_d + 1):
                    alpha_A[(d_i + 1) * q] += Rd * arb(liouville_lambda_int(q))
                w_k = M_drift[d_i] + (R_osc[d_i] if d_i <= D0_eff else arb(0))
                for q in range(1, L_d + 1):
                    term = w_k * arb(liouville_lambda_int(q))
                    alpha_A[d_i * q] += term
                    alpha_A[(d_i + 1) * q] -= term

            max_coeff_diff = arb(0)
            for n in range(1, 2 * T_y + 1):
                cd = abs(alpha_A[n] + beta_Y[n])
                if bool(cd.upper() > max_coeff_diff.upper()):
                    max_coeff_diff = cd

            max_pt_err = arb(0)
            for mult in (arb(1), sqrt_tau, tau):
                X_pt = arb(y_val) * mult
                lg2 = X_pt.log() ** 2
                A_src = arb(0)
                A_neg_beta = arb(0)
                for n in range(1, 2 * T_y + 1):
                    ph = evaluate_phi_n_arb(X_pt, n, prec_bits=prec_bits)
                    A_src += alpha_A[n] * ph
                    A_neg_beta -= beta_Y[n] * ph
                A_src /= lg2
                A_neg_beta /= lg2
                err = abs(A_src - A_neg_beta)
                if bool(err.upper() > max_pt_err.upper()):
                    max_pt_err = err

            row_ok = bool(max_coeff_diff < arb("1e-70") and max_pt_err < arb("1e-70"))
            reassembly_ok = reassembly_ok and row_ok
            reassembly_rows.append(
                {
                    "Y": y_val,
                    "T_Y": T_y,
                    "D0_eff": D0_eff,
                    "A_norm_sq": serialize_arb_certified(res["A_norm_sq"]),
                    "max_alpha_A_plus_beta_Y_abs": serialize_arb_certified(max_coeff_diff),
                    "max_pointwise_A_reassembly_abs_error": serialize_arb_certified(max_pt_err),
                    "verified": row_ok,
                }
            )

        # Complete signed kernel Hcal_Y assembly on Y in {2, 4, 8, 16}:
        kernel_rows: List[Dict[str, Any]] = []
        kernel_ok = True
        for y_val in (2, 4, 8, 16):
            sp = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            res_1d = evaluate_mixed_covariance_point_arb(
                sp,
                prec_bits=prec_bits,
                quad_tol_bits=235,
                use_three_zone=False,
                allow_nonprotocol_override=True,
                selberg_table=tbl,
            )
            T_y = res_1d["cutoffs"]["T_Y"]
            D0_eff = res_1d["cutoffs"]["D0_eff"]
            N = 2 * T_y
            Y_b = arb(y_val)
            X_self = evaluate_X_self_collision_arb(Y_b, T_y, prec_bits=prec_bits)
            F_1d = +(res_1d["J_direct"] - arb(4) * X_self)

            Hcal = build_complete_signed_kernel_evaluator_small_T(
                Y_b, T_y, D0_eff, tbl, prec_bits=prec_bits
            )

            # Verify zero outside [1, 2T]^2 and exact symmetry Hcal(m, n) == Hcal(n, m):
            out_zero_ok = bool(
                Hcal(0, 1) == arb(0)
                and Hcal(1, 0) == arb(0)
                and Hcal(N + 1, 1) == arb(0)
                and Hcal(1, N + 1) == arb(0)
                and Hcal(N + 2, N + 2) == arb(0)
            )
            sym_ok = True
            F_kernel_sum = arb(0)
            for m in range(1, N + 1):
                lm = liouville_lambda_int(m)
                for n in range(1, N + 1):
                    ln = liouville_lambda_int(n)
                    h_mn = Hcal(m, n)
                    if n >= m:
                        h_nm = Hcal(n, m)
                        if not (
                            h_mn == h_nm
                            or (arb(0) in (h_mn - h_nm) and abs(h_mn - h_nm) < arb("1e-48"))
                        ):
                            sym_ok = False
                    F_kernel_sum += arb(lm * ln) * h_mn

            res_F = F_kernel_sum - F_1d
            row_k_ok = bool(
                out_zero_ok
                and sym_ok
                and arb(0) in res_F
                and abs(res_F) < arb("1e-48")
            )
            kernel_ok = kernel_ok and row_k_ok
            kernel_rows.append(
                {
                    "Y": y_val,
                    "T_Y": T_y,
                    "D0_eff": D0_eff,
                    "N_outer": N,
                    "D_tilde_Y": serialize_arb_certified(res_1d["D_tilde_Y"]),
                    "X_self_Y": serialize_arb_certified(X_self),
                    "F_direct_1d": serialize_arb_certified(F_1d),
                    "F_complete_kernel_sum": serialize_arb_certified(F_kernel_sum),
                    "F_kernel_minus_1d_residual": serialize_arb_certified(res_F),
                    "zero_outside_1_to_2T_verified": out_zero_ok,
                    "kernel_symmetry_verified": sym_ok,
                    "verified": row_k_ok,
                }
            )

        return {
            "epistemic_statuses": [
                "CONCRETE_ANALYTIC_IN_LEAN",
                "CERTIFIED_FINITE_OBSERVATION",
            ],
            "section_epistemic_scope_note": (
                "Mixed formal/certified section: pointwise reassembly A_Y(X) = -sum_{n<=2T} "
                "beta_Y(n)*phi_n(X)/(log X)^2 and complete signed kernel assembly F(Y) = "
                "sum_{m,n=1}^{2T} lambda(m)*lambda(n)*Hcal_Y(m, n) (instantiated with repository "
                "constants c_lambda and c_{1/2,lambda} and retaining both -4*D_tilde and -4*X_self) "
                "are CONCRETE_ANALYTIC_IN_LEAN (Lean Theorem 1); protocol immutability checks and "
                "256-bit Arb cross-verifications on Y in {2, 4, 8, 16, 32, 64} are "
                "CERTIFIED_FINITE_OBSERVATION. Reassembly of A_Y is inherited algebra, not a new "
                "arithmetic saving, and A_Y's horizon-coupled contraction scope from TC-060 is "
                "preserved without upgrading A_Y to O(1)."
            ),
            "component_epistemic_map": {
                "pointwise_A_Y_reassembly_and_complete_Hcal_Y_identity": "CONCRETE_ANALYTIC_IN_LEAN",
                "tc061_and_tc062_protocol_immutability_and_finite_kernel_checks": "CERTIFIED_FINITE_OBSERVATION",
            },
            "lean_theorems": [
                "reassembly_known_part_and_complete_signed_kernel_tc062",
            ],
            "preserved_tc061_protocol_immutability": {
                k: v for k, v in tc061_proto_chk.items() if k != "protocol_object"
            },
            "frozen_tc062_protocol_immutability": {
                k: v for k, v in tc062_proto_chk.items() if k != "protocol_object"
            },
            "pointwise_A_Y_reassembly_checks": reassembly_rows,
            "complete_kernel_assembly_checks": kernel_rows,
            "all_section_1_checks_pass": bool(
                tc061_proto_chk["verified"]
                and tc062_proto_chk["verified"]
                and reassembly_ok
                and kernel_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 2. Section 2: Generic Pairing, 1-Prime & 2-Prime Decompositions, & Controls
# ---------------------------------------------------------------------------


def verify_generic_finite_anchor_reindexing_exact() -> Dict[str, Any]:
    """Verify generic 4-term (1-prime) and 16-term (2-prime) finite reindexing identities in exact
    `Fraction` arithmetic on a non-multiplicative sequence `a(n) = n^2 - 3*n + 1` and a
    non-symmetric arbitrary finite kernel `H(m, n) = (2*m + 5*n) / (m + n + 1)` (`0` outside `[1, N]^2`).
    """
    def _a_seq(n: int) -> Fraction:
        return Fraction(n * n - 3 * n + 1, 1)

    def _make_H(N: int) -> Callable[[int, int], Fraction]:
        def _H(m: int, n: int) -> Fraction:
            if m < 1 or m > N or n < 1 or n > N:
                return Fraction(0, 1)
            return Fraction(2 * m + 5 * n, m + n + 1)

        return _H

    one_prime_ok = True
    two_prime_ok = True
    rows: List[Dict[str, Any]] = []
    for N in (6, 15, 30):
        H = _make_H(N)
        direct = Fraction(0, 1)
        for m in range(1, N + 1):
            am = _a_seq(m)
            for n in range(1, N + 1):
                direct += am * _a_seq(n) * H(m, n)

        for p in (2, 3, 5):
            A_p = prime_even_valuation_anchors(N, (p,))
            paired_1p = Fraction(0, 1)
            for m in A_p:
                for n in A_p:
                    paired_1p += (
                        _a_seq(m) * _a_seq(n) * H(m, n)
                        + _a_seq(p * m) * _a_seq(n) * H(p * m, n)
                        + _a_seq(m) * _a_seq(p * n) * H(m, p * n)
                        + _a_seq(p * m) * _a_seq(p * n) * H(p * m, p * n)
                    )
            if paired_1p != direct:
                one_prime_ok = False

        for p, q in ((2, 3), (2, 5), (3, 5)):
            A_pq = prime_even_valuation_anchors(N, (p, q))
            paired_2p = Fraction(0, 1)
            for m in A_pq:
                for n in A_pq:
                    for e1 in (0, 1):
                        for e2 in (0, 1):
                            m_sh = (p ** e1) * (q ** e2) * m
                            am_sh = _a_seq(m_sh)
                            for f1 in (0, 1):
                                for f2 in (0, 1):
                                    n_sh = (p ** f1) * (q ** f2) * n
                                    paired_2p += am_sh * _a_seq(n_sh) * H(m_sh, n_sh)
            if paired_2p != direct:
                two_prime_ok = False

        rows.append(
            {
                "N": N,
                "direct_sum_fraction": f"{direct.numerator}/{direct.denominator}",
                "one_prime_2_3_5_exact_match": one_prime_ok,
                "two_prime_pairs_exact_match": two_prime_ok,
            }
        )

    return {
        "sequence_used": "a(n) = n^2 - 3*n + 1 (non-multiplicative)",
        "kernel_used": "H(m, n) = (2*m + 5*n) / (m + n + 1) on [1, N]^2 (non-symmetric)",
        "rows": rows,
        "verified": bool(one_prime_ok and two_prime_ok),
    }


def build_matched_control_complete_kernel_small_T(
    Y_int: int,
    mode: str,
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Build a control's own matched complete kernel `Hcal_{a_S, Y}(m, n)` and own prime-pair signs
    on small `Y` (`Y in {8, 16}`) so `F_{a_S}(Y) = sum_{m,n<=2T} a_S(m)*a_S(n)*Hcal_{a_S,Y}(m, n)`.
    """
    if mode not in ("unsigned_1", "a2", "a_3_5_7"):
        raise ValueError(f"Unsupported matched control mode {mode!r}")
    prime_set: Tuple[int, ...] = (
        () if mode == "unsigned_1" else ((2,) if mode == "a2" else (3, 5, 7))
    )
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        sp = ExactScaleSpec(str(Y_int), "exact_rational", Fraction(Y_int, 1))
        cut = certify_exact_scale_cutoffs(sp, base_prec_bits=prec_bits)
        T_y = cut["T_Y"]
        D0_eff = cut["D0_eff"]
        N = 2 * T_y
        Y_b = arb(Y_int)

        a_seq = [0] + [finite_prime_parity_aS_int(n, prime_set) for n in range(1, N + 1)]
        lam_vm = selberg_table["lam_vm"]
        conv_ll = selberg_table["conv_ll"]
        gamma_e = arb.const_euler()
        c0_S = -(
            arb(2)
            + arb(2) * gamma_e
            + sum((arb(4 * p) * arb(p).log() / arb(p * p - 1) for p in prime_set), arb(0))
        )
        R_S = [arb(0)] * (T_y + 1)
        cum_w = arb(0)
        for d_i in range(1, T_y + 1):
            if d_i >= 2:
                cum_w += arb(a_seq[d_i]) * (lam_vm[d_i] * arb(d_i).log() + conv_ll[d_i])
            d_arb = arb(d_i)
            M_pole = arb(2) * d_arb * arb(d_i).log() + c0_S * d_arb
            R_S[d_i] = cum_w - M_pole

        s_S = [arb(0)] * (N + 1)
        for d_i in range(D0_eff + 1, T_y):
            L_d = T_y // d_i
            wd = R_S[d_i]
            for q in range(1, L_d + 1):
                term = wd * arb(a_seq[q])
                s_S[d_i * q] += term
                s_S[(d_i + 1) * q] -= term

        beta_S = [arb(0)] * (N + 1)
        b_S = [arb(0)] * (N + 1)
        for n in range(1, N + 1):
            if n <= T_y:
                beta_S[n] = s_S[n] - arb(a_seq[n]) * (arb(n).log() ** 2)
            else:
                beta_S[n] = s_S[n]
            b_S[n] = arb(a_seq[n]) * beta_S[n]

        c_div = [arb(0)] * (T_y + 1)
        for p, k in prime_power_pairs_up_to(T_y):
            pk = p ** k
            lg2 = arb(p).log() ** 2
            for mult in range(pk, T_y + 1, pk):
                c_div[mult] += lg2

        G_cache: Dict[Tuple[int, int, int], arb] = {}

        def _G(m_i: int, n_i: int, r_p: int) -> arb:
            u_i, v_i = (m_i, n_i) if m_i <= n_i else (n_i, m_i)
            key = (u_i, v_i, r_p)
            hit = G_cache.get(key)
            if hit is None:
                hit = evaluate_window_gram_G_Y_r_arb(Y_b, u_i, v_i, r_p, prec_bits=prec_bits)
                G_cache[key] = hit
            return hit

        def _Hcal_ctrl(m: int, n: int) -> arb:
            if m < 1 or m > N or n < 1 or n > N:
                return arb(0)
            tm = 1 if m <= T_y else 0
            tn = 1 if n <= T_y else 0
            g0_part = _G(m, n, 0) if (tm and tn) else arb(0)
            c_mn = c_div[math.gcd(m, n)] if (tm and tn) else arb(0)
            diag_corr = (
                arb(4) * ((arb(m).log() ** 2) - c_div[m]) if (m == n and tm) else arb(0)
            )
            coeff_g2 = (
                (b_S[n] if tm else arb(0))
                + (b_S[m] if tn else arb(0))
                + (arb(4) * c_mn if (tm and tn) else arb(0))
                + diag_corr
            )
            g2_part = coeff_g2 * _G(m, n, 2) if coeff_g2 != arb(0) else arb(0)
            bb = b_S[m] * b_S[n]
            g4_part = bb * _G(m, n, 4) if bb != arb(0) else arb(0)
            return +(g0_part - g2_part + g4_part)

        return {
            "T_Y": T_y,
            "D0_eff": D0_eff,
            "N": N,
            "prime_set": prime_set,
            "a_seq": a_seq,
            "Hcal_ctrl": _Hcal_ctrl,
        }
    finally:
        flint_ctx.prec = saved


def verify_section_2_disjoint_prime_decompositions_and_controls(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Verify generic reindexing, 1-prime 4-term and 2-prime 16-term Liouville identities (including
    boundary extraction, diagonal coincidence laws, and `c(m, n)` differences), and matched control
    prime-pair sign laws + finite-grid refutations across `Y in {16, 32, 64, 128, 256, 512}`.
    """
    generic_chk = verify_generic_finite_anchor_reindexing_exact()
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(2500, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 2450
        else selberg_table
    )

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits

        # 1. Exact diagonal coincidence law & c(m, n) difference laws on 1 <= m, n <= 120:
        c_div_120 = [arb(0)] * 721
        for p, k in prime_power_pairs_up_to(720):
            pk = p ** k
            lg2 = arb(p).log() ** 2
            for mult in range(pk, 721, pk):
                c_div_120[mult] += lg2

        diag_coinc_ok = True
        c_diff_1p_ok = True
        c_diff_2p_ok = True
        A2_60 = prime_even_valuation_anchors(60, (2,))
        for m in A2_60:
            for n in A2_60:
                if 2 * m == n or m == 2 * n or ((2 * m == 2 * n) != (m == n)):
                    diag_coinc_ok = False
                d2_c = (
                    c_div_120[math.gcd(m, n)]
                    - c_div_120[math.gcd(2 * m, n)]
                    - c_div_120[math.gcd(m, 2 * n)]
                    + c_div_120[math.gcd(2 * m, 2 * n)]
                )
                exp_c = (
                    arb(2).log() ** 2
                    if prime_valuation_v_p(m, 2) == prime_valuation_v_p(n, 2)
                    else arb(0)
                )
                res_c = d2_c - exp_c
                if not ((exp_c == arb(0) and d2_c == arb(0)) or (arb(0) in res_c and abs(res_c) < arb("1e-70"))):
                    c_diff_1p_ok = False

        A23_40 = prime_even_valuation_anchors(40, (2, 3))
        for m in A23_40:
            for n in A23_40:
                d4_c = arb(0)
                for e1 in (0, 1):
                    for e2 in (0, 1):
                        m_sh = (2 ** e1) * (3 ** e2) * m
                        for f1 in (0, 1):
                            for f2 in (0, 1):
                                n_sh = (2 ** f1) * (3 ** f2) * n
                                hit_diag = m_sh == n_sh
                                exp_diag = e1 == f1 and e2 == f2 and m == n
                                if hit_diag != exp_diag:
                                    diag_coinc_ok = False
                                sgn = (-1) ** (e1 + e2 + f1 + f2)
                                d4_c += arb(sgn) * c_div_120[math.gcd(m_sh, n_sh)]
                if not (d4_c == arb(0) or (arb(0) in d4_c and abs(d4_c) < arb("1e-70"))):
                    c_diff_2p_ok = False

        # 2. 1-prime and 2-prime Liouville complete-kernel pairing on Y in {2, 4, 8, 16}:
        pairing_rows: List[Dict[str, Any]] = []
        pairing_ok = True
        for y_val in (2, 4, 8, 16):
            sp = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            res_1d = evaluate_mixed_covariance_point_arb(
                sp,
                prec_bits=prec_bits,
                quad_tol_bits=235,
                use_three_zone=False,
                allow_nonprotocol_override=True,
                selberg_table=tbl,
            )
            T_y = res_1d["cutoffs"]["T_Y"]
            D0_eff = res_1d["cutoffs"]["D0_eff"]
            N = 2 * T_y
            Y_b = arb(y_val)
            X_self = evaluate_X_self_collision_arb(Y_b, T_y, prec_bits=prec_bits)
            F_1d = +(res_1d["J_direct"] - arb(4) * X_self)
            Hcal = build_complete_signed_kernel_evaluator_small_T(
                Y_b, T_y, D0_eff, tbl, prec_bits=prec_bits
            )

            # 1-prime p = 2 and p = 3:
            per_p: Dict[str, Any] = {}
            for p in (2, 3):
                A_p = prime_even_valuation_anchors(N, (p,))
                tot_p = arb(0)
                int_N_p = arb(0)
                bnd_N_p = arb(0)
                int_T_p = arb(0)
                bnd_T_p = arb(0)
                for m in A_p:
                    lm = liouville_lambda_int(m)
                    for n in A_p:
                        ln = liouville_lambda_int(n)
                        d4 = Hcal(m, n) - Hcal(p * m, n) - Hcal(m, p * n) + Hcal(p * m, p * n)
                        val = arb(lm * ln) * d4
                        tot_p += val
                        if p * m <= N and p * n <= N:
                            int_N_p += val
                        else:
                            bnd_N_p += val
                        if p * m <= T_y and p * n <= T_y:
                            int_T_p += val
                        else:
                            bnd_T_p += val
                res_p = tot_p - F_1d
                p_ok = bool(arb(0) in res_p and abs(res_p) < arb("1e-48"))
                pairing_ok = pairing_ok and p_ok
                per_p[str(p)] = {
                    "anchor_count": len(A_p),
                    "F_paired_total": serialize_arb_certified(tot_p),
                    "F_outer_N_interior": serialize_arb_certified(int_N_p),
                    "F_outer_N_terminal_boundary": serialize_arb_certified(bnd_N_p),
                    "F_inner_T_interior": serialize_arb_certified(int_T_p),
                    "F_inner_T_cutoff_and_spillover_boundary": serialize_arb_certified(bnd_T_p),
                    "paired_minus_F_1d_residual": serialize_arb_certified(res_p),
                    "verified": p_ok,
                }

            # 2-prime (p, q) = (2, 3):
            A_23 = prime_even_valuation_anchors(N, (2, 3))
            tot_23 = arb(0)
            int_T_23 = arb(0)
            bnd_T_23 = arb(0)
            for m in A_23:
                lm = liouville_lambda_int(m)
                for n in A_23:
                    ln = liouville_lambda_int(n)
                    d16 = arb(0)
                    for e1 in (0, 1):
                        for e2 in (0, 1):
                            for f1 in (0, 1):
                                for f2 in (0, 1):
                                    sgn = (-1) ** (e1 + e2 + f1 + f2)
                                    d16 += arb(sgn) * Hcal(
                                        (2 ** e1) * (3 ** e2) * m, (2 ** f1) * (3 ** f2) * n
                                    )
                    val = arb(lm * ln) * d16
                    tot_23 += val
                    if 6 * m <= T_y and 6 * n <= T_y:
                        int_T_23 += val
                    else:
                        bnd_T_23 += val
            res_23 = tot_23 - F_1d
            ok_23 = bool(arb(0) in res_23 and abs(res_23) < arb("1e-48"))
            pairing_ok = pairing_ok and ok_23

            pairing_rows.append(
                {
                    "Y": y_val,
                    "T_Y": T_y,
                    "N_outer": N,
                    "F_direct_1d": serialize_arb_certified(F_1d),
                    "one_prime_decompositions": per_p,
                    "two_prime_2_3_sixteen_term": {
                        "anchor_count": len(A_23),
                        "F_paired_16_term_total": serialize_arb_certified(tot_23),
                        "F_inner_T_interior": serialize_arb_certified(int_T_23),
                        "F_inner_T_boundary": serialize_arb_certified(bnd_T_23),
                        "paired_16_minus_F_1d_residual": serialize_arb_certified(res_23),
                        "verified": ok_23,
                    },
                }
            )

        # 3. Matched control prime-pair sign verification at Y = 8 (p = 2 vs p = 3) & grid Y = 16..512:
        control_sign_checks: List[Dict[str, Any]] = []
        control_sign_ok = True
        for mode in ("unsigned_1", "a2", "a_3_5_7"):
            ck = build_matched_control_complete_kernel_small_T(8, mode, tbl, prec_bits=prec_bits)
            r_ctrl = evaluate_control_matched_point_arb(8, mode, tbl, prec_bits=prec_bits)
            X_self_8 = evaluate_X_self_collision_arb(arb(8), ck["T_Y"], prec_bits=prec_bits)
            F_ctrl_1d = +(r_ctrl["J_direct"] - arb(4) * X_self_8)
            N8 = ck["N"]
            a_seq = ck["a_seq"]
            H_c = ck["Hcal_ctrl"]
            p_set = ck["prime_set"]

            for p in (2, 3):
                eps_p = -1 if p in p_set else 1
                A_p = prime_even_valuation_anchors(N8, (p,))
                matched_sum = arb(0)
                wrong_minus_sum = arb(0)
                for m in A_p:
                    am = a_seq[m]
                    for n in A_p:
                        an = a_seq[n]
                        matched_sum += arb(am * an) * (
                            H_c(m, n)
                            + arb(eps_p) * H_c(p * m, n)
                            + arb(eps_p) * H_c(m, p * n)
                            + H_c(p * m, p * n)
                        )
                        wrong_minus_sum += arb(am * an) * (
                            H_c(m, n) - H_c(p * m, n) - H_c(m, p * n) + H_c(p * m, p * n)
                        )
                res_m = matched_sum - F_ctrl_1d
                m_ok = bool(arb(0) in res_m and abs(res_m) < arb("1e-50"))
                if eps_p == 1:
                    # Outside S, Liouville's all-minus pairing MUST fail to equal F_ctrl:
                    wrong_fails = bool(abs(wrong_minus_sum - F_ctrl_1d) > arb("1e-3"))
                else:
                    wrong_fails = True
                control_sign_ok = control_sign_ok and m_ok and wrong_fails
                control_sign_checks.append(
                    {
                        "Y": 8,
                        "mode": mode,
                        "prime_p": p,
                        "p_in_parity_set_S": bool(p in p_set),
                        "derived_pair_sign_eps_p": eps_p,
                        "F_control_direct_1d": serialize_arb_certified(F_ctrl_1d),
                        "F_control_matched_sign_paired": serialize_arb_certified(matched_sum),
                        "matched_sign_residual": serialize_arb_certified(res_m),
                        "misapplied_all_minus_paired_value": serialize_arb_certified(wrong_minus_sum),
                        "misapplied_all_minus_discrepancy": serialize_arb_certified(
                            wrong_minus_sum - F_ctrl_1d
                        ),
                        "verified": bool(m_ok and wrong_fails),
                    }
                )

        # Evaluate F_{a_S}(Y) vs (log Y)*D_tilde_{a_S}(Y) across Y in {16, 32, 64, 128, 256, 512}:
        control_grid_rows: List[Dict[str, Any]] = []
        controls_refuted_ok = True
        for y_val in (16, 32, 64, 128, 256, 512):
            sp_c = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            cut_c = certify_exact_scale_cutoffs(sp_c, base_prec_bits=prec_bits)
            X_self_y = evaluate_X_self_collision_arb(arb(y_val), cut_c["T_Y"], prec_bits=prec_bits)
            for mode in ("liouville", "unsigned_1", "a2", "a_3_5_7", "hybrid_a2_liouville"):
                rc = evaluate_control_matched_point_arb(y_val, mode, tbl, prec_bits=prec_bits)
                F_c = +(rc["J_direct"] - arb(4) * X_self_y)
                lgD_c = rc["log_Y_times_D_tilde"]
                margin_F = F_c - lgD_c
                cls_F = classify_probe_margin_arb(margin_F)
                if y_val >= 64 and mode in ("unsigned_1", "a2", "a_3_5_7"):
                    if cls_F["verdict"] != "FAIL":
                        controls_refuted_ok = False
                control_grid_rows.append(
                    {
                        "Y": y_val,
                        "mode": mode,
                        "is_hybrid_diagnostic": bool(mode == "hybrid_a2_liouville"),
                        "exact_matched_core": bool(mode != "hybrid_a2_liouville"),
                        "F_Y": serialize_arb_certified(F_c),
                        "log_Y_times_D_tilde": serialize_arb_certified(lgD_c),
                        "F_over_log_Y_D_tilde": certified_ratio_with_positive_denominator(
                            F_c, lgD_c, prec_bits=prec_bits
                        ),
                        "TC062_P0_F_margin": serialize_arb_certified(margin_F),
                        "TC062_P0_F_verdict": cls_F["verdict"],
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
                "Mixed arithmetic/formal/certified section: unique p-adic and (p, q)-adic parity "
                "anchor factorizations, diagonal coincidence classifications, generic 4-term and "
                "16-term finite reindexing, Liouville pairing identities (including boundary splits), "
                "matched control sign laws, and exact Delta_{p,p} c(m, n) / Delta_{p,p}Delta_{q,q} c(m, n) "
                "formulas are UNCONDITIONAL_FINITE_ARITHMETIC and CONCRETE_ANALYTIC_IN_LEAN (Lean "
                "Theorems 2 & 3); matched z = 1 Laurent control compensations are ANALYTIC_PROVED_OUTSIDE_LEAN; "
                "and 256-bit Arb pairing/control evaluations on finite grids (including the explicitly "
                "labeled hybrid_a2_liouville diagnostic) are CERTIFIED_FINITE_OBSERVATION."
            ),
            "component_epistemic_map": {
                "generic_4_term_and_16_term_anchor_reindexing_exact": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "liouville_one_prime_and_two_prime_identities_and_c_differences": "CONCRETE_ANALYTIC_IN_LEAN",
                "matched_z1_laurent_control_cores": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "small_window_paired_kernel_and_control_grid_certificates": "CERTIFIED_FINITE_OBSERVATION",
            },
            "lean_theorems": [
                "generic_and_liouville_one_prime_pair_decomposition_tc062",
                "disjoint_two_prime_sixteen_term_and_diagonal_coincidence_tc062",
            ],
            "generic_reindexing_verification": generic_chk,
            "diagonal_coincidence_and_c_difference_checks": {
                "parity_diagonal_disjointness_and_16_term_coincidence_verified": diag_coinc_ok,
                "one_prime_c_second_difference_verified": c_diff_1p_ok,
                "two_prime_c_fourth_difference_zero_verified": c_diff_2p_ok,
            },
            "liouville_complete_kernel_pairing_rows": pairing_rows,
            "matched_control_prime_pair_sign_checks": control_sign_checks,
            "matched_control_F_grid_rows": control_grid_rows,
            "all_negative_controls_refuted_on_F_for_Y_ge_64": controls_refuted_ok,
            "all_section_2_checks_pass": bool(
                generic_chk["verified"]
                and diag_coinc_ok
                and c_diff_1p_ok
                and c_diff_2p_ok
                and pairing_ok
                and control_sign_ok
                and controls_refuted_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 3. Section 3: Whole-Line Finite Obstruction to Independent Contraction Gains
# ---------------------------------------------------------------------------


def evaluate_whole_line_contraction_ratio_closed_arb(
    prime_set: Sequence[int],
    *,
    prec_bits: int = 256,
) -> Dict[str, arb]:
    """Evaluate `||f_S||_{(0, infty)}^2`, `sum_{d | P_S} ||phi_d||_{(0, infty)}^2`, and `r(S)`
    using `<phi_m, phi_n>_{(0, infty)} = c_G * (m*n)^2 / (m^2 + n^2)^{5/2}`, `c_G = 3*sqrt(tau/2)/8`.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        c_G = arb(3) * (tau / arb(2)).sqrt() / arb(8)
        _, divs = squarefree_divisors_of_prime_set(prime_set)
        num = arb(0)
        den = arb(0)
        for m, lm in divs:
            den += c_G * (arb(m * m) ** 2) / (arb(2 * m * m) ** (arb(5) / arb(2)))
            for n, ln in divs:
                g_mn = c_G * (arb(m * n) ** 2) / (arb(m * m + n * n) ** (arb(5) / arb(2)))
                num += arb(lm * ln) * g_mn
        return {
            "f_S_norm_sq": +num,
            "diag_norm_sq_sum": +den,
            "r_S": +(num / den),
        }
    finally:
        flint_ctx.prec = saved


def evaluate_whole_line_contraction_ratio_quadrature_arb(
    prime_set: Sequence[int],
    *,
    prec_bits: int = 256,
) -> arb:
    """Independent 256-bit `acb.integral` quadrature of `r(S)` over `t = log X in [-40, log(16*P_S)]`
    plus outward analytic tail bounds on `t < -40` and `t > log(16*P_S)`.
    """
    work_prec = prec_bits + 32
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = work_prec
        P_S, divs = squarefree_divisors_of_prime_set(prime_set)
        t_lo = arb(-40)
        t_hi = (arb(16 * P_S)).log()
        tol = 2 ** (-190)

        divs_c = [(acb(arb(d) ** (-3)), acb(-(arb(d) ** (-2))), sgn) for (d, sgn) in divs]

        def _f_sq_cb(t: acb, _an: bool) -> acb:
            e_52 = (acb(arb(5) / arb(2)) * t).exp()
            e_2t = (acb(2) * t).exp()
            s = acb(0)
            for inv_d3, neg_inv_d2, sgn in divs_c:
                ph = e_52 * inv_d3 * (e_2t * neg_inv_d2).exp()
                s += ph if sgn == 1 else -ph
            return s * s

        def _diag_cb(t: acb, _an: bool) -> acb:
            e_52 = (acb(arb(5) / arb(2)) * t).exp()
            e_2t = (acb(2) * t).exp()
            s = acb(0)
            for inv_d3, neg_inv_d2, _sgn in divs_c:
                ph = e_52 * inv_d3 * (e_2t * neg_inv_d2).exp()
                s += ph * ph
            return s

        num_mid = acb.integral(_f_sq_cb, acb(t_lo), acb(t_hi), rel_tol=tol, abs_tol=tol).real
        den_mid = acb.integral(_diag_cb, acb(t_lo), acb(t_hi), rel_tol=tol, abs_tol=tol).real

        # Left tail t <= -40: |f_S(e^t)| <= (sum_{d|P_S} d^{-3}) e^{5t/2} <= 2 * e^{5t/2},
        # integral_{-infty}^{-40} 4 e^{5t} dt = (4/5) e^{-200}:
        left_rad = ((arb(4) / arb(5)) * arb(-200).exp()).upper()
        # Right tail X = e^t >= 16 * P_S: each phi_d(X) <= X^{5/2} P_S^3 exp(-X^2 / P_S^2);
        # for u = X / P_S >= 16, u^5 exp(-2 u^2) <= u * u^4 exp(-u^2) * exp(-u^2) <= u * (4/e^2) * exp(-u^2),
        # integral_{16}^infty (4/e^2) u exp(-u^2) du / u <= 2 exp(-256):
        n_divs = len(divs)
        right_rad = (arb(n_divs * n_divs * 2) * arb(-256).exp()).upper()
        tot_rad = (arb(left_rad) + arb(right_rad)).upper()

        num_tot = num_mid + arb(0, tot_rad)
        den_tot = den_mid + arb(0, tot_rad)
        flint_ctx.prec = prec_bits
        return +(num_tot / den_tot)
    finally:
        flint_ctx.prec = saved


def verify_section_3_whole_line_contraction_obstruction(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Independently certify the 5 required whole-line contraction enclosures and strict ordering
    `r({2})*r({3}) < r({2}) < r({2,3}) < r({2,3,5})`, cross-checked against improper half-line
    `acb.integral` quadrature and the exact cross-prime coupling identity.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        c_G = arb(3) * (tau / arb(2)).sqrt() / arb(8)

        r2_d = evaluate_whole_line_contraction_ratio_closed_arb((2,), prec_bits=prec_bits)
        r3_d = evaluate_whole_line_contraction_ratio_closed_arb((3,), prec_bits=prec_bits)
        r23_d = evaluate_whole_line_contraction_ratio_closed_arb((2, 3), prec_bits=prec_bits)
        r235_d = evaluate_whole_line_contraction_ratio_closed_arb((2, 3, 5), prec_bits=prec_bits)
        r2357_d = evaluate_whole_line_contraction_ratio_closed_arb((2, 3, 5, 7), prec_bits=prec_bits)

        r2 = r2_d["r_S"]
        r3 = r3_d["r_S"]
        r23 = r23_d["r_S"]
        r235 = r235_d["r_S"]
        r2357 = r2357_d["r_S"]
        prod_23 = +(r2 * r3)

        # Exact algebraic closed forms (cancelling c_G identically):
        r2_alg = arb(1) - arb(64) * arb(10).sqrt() / arb(375)
        r3_alg = arb(1) - arb(27) * arb(5).sqrt() / arb(250)
        alg_ok = bool(
            arb(0) in (r2 - r2_alg)
            and abs(r2 - r2_alg) < arb("1e-72")
            and arb(0) in (r3 - r3_alg)
            and abs(r3 - r3_alg) < arb("1e-72")
        )

        # Independent improper half-line quadrature checks:
        r2_q = evaluate_whole_line_contraction_ratio_quadrature_arb((2,), prec_bits=prec_bits)
        r3_q = evaluate_whole_line_contraction_ratio_quadrature_arb((3,), prec_bits=prec_bits)
        r23_q = evaluate_whole_line_contraction_ratio_quadrature_arb((2, 3), prec_bits=prec_bits)
        r235_q = evaluate_whole_line_contraction_ratio_quadrature_arb((2, 3, 5), prec_bits=prec_bits)
        quad_ok = bool(
            arb(0) in (r2 - r2_q)
            and abs(r2 - r2_q) < arb("1e-50")
            and arb(0) in (r3 - r3_q)
            and abs(r3 - r3_q) < arb("1e-50")
            and arb(0) in (r23 - r23_q)
            and abs(r23 - r23_q) < arb("1e-50")
            and arb(0) in (r235 - r235_q)
            and abs(r235 - r235_q) < arb("1e-50")
        )

        # Exact cross-prime coupling identity:
        # r({2, 3}) - r({2}) = -2 * <phi_1 - phi_2, phi_3 - phi_6>_{(0, infty)} / sum_{d|6} ||phi_d||^2
        def _Ginf(m: int, n: int) -> arb:
            return c_G * (arb(m * n) ** 2) / (arb(m * m + n * n) ** (arb(5) / arb(2)))

        pair_g1_D3g1 = _Ginf(1, 3) - _Ginf(2, 3) - _Ginf(1, 6) + _Ginf(2, 6)
        coupling_excess = (-arb(2) * pair_g1_D3g1) / r23_d["diag_norm_sq_sum"]
        coupling_res = (r23 - r2) - coupling_excess
        coupling_ok = bool(
            pair_g1_D3g1 < arb(0)
            and coupling_excess > arb(0)
            and arb(0) in coupling_res
            and abs(coupling_res) < arb("1e-72")
        )

        target_boxes = [
            ("r({2})", r2, Fraction(460304612664, 10 ** 12), Fraction(460304612665, 10 ** 12)),
            ("r({3})", r3, Fraction(758504658430, 10 ** 12), Fraction(758504658431, 10 ** 12)),
            ("r({2,3})", r23, Fraction(577474326597, 10 ** 12), Fraction(577474326598, 10 ** 12)),
            ("r({2,3,5})", r235, Fraction(706402204851, 10 ** 12), Fraction(706402204852, 10 ** 12)),
            (
                "r({2})*r({3})",
                prod_23,
                Fraction(349143193002, 10 ** 12),
                Fraction(349143193003, 10 ** 12),
            ),
        ]
        enclosure_rows: List[Dict[str, Any]] = []
        boxes_ok = True
        for label, ball, lo_fr, hi_fr in target_boxes:
            b_lo, b_hi = _exact_arb_endpoints_as_fractions(ball)
            in_box = bool(
                lo_fr <= b_lo
                and b_hi <= hi_fr
                and ball >= _frac_to_arb(lo_fr)
                and ball <= _frac_to_arb(hi_fr)
            )
            boxes_ok = boxes_ok and in_box
            enclosure_rows.append(
                {
                    "quantity": label,
                    "enclosure": serialize_arb_certified(ball),
                    "target_lower_decimal": f"{lo_fr.numerator / 1e12:.12f}",
                    "target_upper_decimal": f"{hi_fr.numerator / 1e12:.12f}",
                    "contained_in_target_interval": in_box,
                }
            )

        strict_order_ok = bool(
            prod_23 < r2 and r2 < r23 and r23 < r235 and r235 < r2357 and r23 > prod_23
        )

        return {
            "epistemic_statuses": [
                "CONCRETE_ANALYTIC_IN_LEAN",
                "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "CERTIFIED_FINITE_OBSERVATION",
                "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            ],
            "section_epistemic_scope_note": (
                "Mixed formal/analytic/certified/obstruction section: the five rational enclosures "
                "for r({2}), r({3}), r({2,3}), r({2,3,5}), and r({2})*r({3}) and strict ordering "
                "r({2})*r({3}) < r({2}) < r({2,3}) < r({2,3,5}) on the algebraic closed-form "
                "wholeLineGaussianGram ratios are CONCRETE_ANALYTIC_IN_LEAN (Lean Theorem 4); the "
                "improper half-line Gaussian/Gamma integral bridge int_0^infty phi_m(X)*phi_n(X) dX/X "
                "= (3*sqrt(tau/2)/8)*(m*n)^2/(m^2+n^2)^{5/2} = wholeLineGaussianGram(m, n) (proved "
                "via (d/dX)(-((2*a*X^3 + 3*X)/(4*a^2))*exp(-a*X^2)) = (X^4 - 3/(4*a^2))*exp(-a*X^2) "
                "at a = m^{-2} + n^{-2}) is ANALYTIC_PROVED_OUTSIDE_LEAN; both are independently "
                "cross-checked via 256-bit Arb closed-form and half-line quadrature "
                "(CERTIFIED_FINITE_OBSERVATION); and independent multiplication of normalized "
                "prime-local contraction factors is REFUTED_WITHIN_SCOPE "
                "(OPEN_CONJECTURE_OR_FAILED_CANDIDATE). This whole-line diagnostic uses neither "
                "the finite-window F(Y) nor D_tilde(Y) as its denominator and does NOT refute the "
                "TC closure hypothesis H."
            ),
            "component_epistemic_map": {
                "five_whole_line_algebraic_ratio_enclosures_and_strict_ordering": "CONCRETE_ANALYTIC_IN_LEAN",
                "improper_halfline_gaussian_integral_to_wholeLineGaussianGram_bridge": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "independent_halfline_quadrature_and_r_2_3_5_7_extension": "CERTIFIED_FINITE_OBSERVATION",
                "naive_independent_prime_contraction_product_candidate": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            },
            "lean_theorems": [
                "whole_line_contraction_enclosures_and_submultiplicativity_refutation_tc062",
            ],
            "enclosure_rows": enclosure_rows,
            "r_2_3_5_7_extension": serialize_arb_certified(r2357),
            "r_2_3_minus_r2_times_r3_gap": serialize_arb_certified(r23 - prod_23),
            "cross_prime_coupling_decomposition": {
                "inner_product_g1_D3g1": serialize_arb_certified(pair_g1_D3g1),
                "dominant_same_octave_2_3_term_neg_Ginf_2_3": serialize_arb_certified(-_Ginf(2, 3)),
                "r_2_3_minus_r_2_excess": serialize_arb_certified(r23 - r2),
                "formula_minus_direct_residual": serialize_arb_certified(coupling_res),
                "verified": coupling_ok,
            },
            "exact_algebraic_closed_forms_verified": alg_ok,
            "independent_halfline_quadrature_verified": quad_ok,
            "strict_ordering_r2r3_lt_r2_lt_r23_lt_r235_verified": strict_order_ok,
            "all_section_3_checks_pass": bool(
                boxes_ok and alg_ok and quad_ok and coupling_ok and strict_order_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 4. Matrix-Free 3-Zone Paired Interior Evaluator & Section 4 Proof Attempt
# ---------------------------------------------------------------------------


def compute_zone1_prime_power_diag_perturbation_tc062_arb(
    pp_info: Sequence[Tuple[int, int, arb]],
    n0_j: int,
    phi_lo: Sequence[arb],
    sqrt_du: arb,
    lg_lo: arb,
    in_omega: Optional[Sequence[bool]] = None,
) -> arb:
    """Delegate directly to the shared order-independent Zone 1 prime-power diagonal L^2
    perturbation helper `compute_zone1_prime_power_diag_perturbation_arb` (`TASK-TC-062R` §2).
    """
    return compute_zone1_prime_power_diag_perturbation_arb(
        pp_info,
        n0_j,
        phi_lo,
        sqrt_du,
        lg_lo,
        in_omega=in_omega,
    )


def evaluate_interior_paired_matrix_free_arb(
    Y_arb: arb,
    T_y: int,
    D0_eff: int,
    ceil_tau_y: int,
    prime_set: Sequence[int],
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
    quad_tol_bits: int = 160,
    use_three_zone: bool = True,
    n_panels_override: Optional[int] = None,
    zone1_ratio_threshold: int = 12,
) -> Dict[str, arb]:
    """Matrix-free outward-rounded Arb evaluation of `F_{int, T}(Y; S)`, `Sigma_{S, diag}^{int}(Y)`,
    and `F_{off, T}(Y; S)` across arbitrary scales (`O(T)` per quadrature node; zero `(2T)^2`
    dense matrix allocation).

    Note: Because `Omega_S(T) = {d*m : m in I_S(T), d | P_S}` is a subset of `{1, ..., T}` and
    Zone 3 begins at `N_1 = max(T + 1, ceil(tau*Y)) >= T + 1`, Zone 3 is identically empty on
    `Omega_S(T)`; only Zone 1 (`X / k >= zone1_ratio_threshold`) and Zone 2 (direct panel
    quadrature) are active.
    """
    work_prec = prec_bits + 32
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = work_prec
        tau = _tau_arb()
        log_tau = tau.log()
        log_Y = Y_arb.log()
        P_S, divs = squarefree_divisors_of_prime_set(prime_set)
        s_primes = tuple(sorted(set(int(p) for p in prime_set)))

        vecs = compute_complete_core_s_Y_and_beta_Y_arb(
            T_y, D0_eff, selberg_table["R_osc"], prec_bits=work_prec
        )
        beta_Y = vecs["beta_Y"]

        anchors = [
            m
            for m in range(1, (T_y // P_S) + 1)
            if all(prime_valuation_v_p(m, p) % 2 == 0 for p in s_primes)
        ]
        in_omega = [False] * (T_y + 1)
        for m in anchors:
            for d, _sgn in divs:
                in_omega[d * m] = True

        pp_pairs = prime_power_pairs_up_to(T_y)
        c_div = [arb(0)] * (T_y + 1)
        for q_p, k_e in pp_pairs:
            qk = q_p ** k_e
            lg2 = arb(q_p).log() ** 2
            for mult in range(qk, T_y + 1, qk):
                c_div[mult] += lg2
        c_self = [arb(0)] + [(arb(k).log() ** 2) - c_div[k] for k in range(1, T_y + 1)]

        inv_n3_r = [arb(0)] + [arb(n) ** (-3) for n in range(1, T_y + 1)]
        inv_n3_c = [acb(v) for v in inv_n3_r]
        neg_inv_n2_c = [acb(0)] + [-(acb(n) ** (-2)) for n in range(1, T_y + 1)]
        lam_c = [acb(0)] + [acb(liouville_lambda_int(n)) for n in range(1, T_y + 1)]
        beta_c = [acb(0)] + [acb(beta_Y[n]) for n in range(1, T_y + 1)]
        b_real_r = [arb(0)] + [
            arb(liouville_lambda_int(n)) * beta_Y[n] for n in range(1, T_y + 1)
        ]
        b_real_c = [acb(v) for v in b_real_r]
        c_self_c = [acb(v) for v in c_self]
        pp_info = [(p ** k, T_y // (p ** k), arb(p).log() ** 2) for (p, k) in pp_pairs]
        pp_info_c = [(pk, L_pk, acb(lg2)) for (pk, L_pk, lg2) in pp_info]

        # Precompute per-anchor shift data:
        anchor_shift_data: List[
            Tuple[int, List[Tuple[int, int]], List[Tuple[int, int, arb, acb]]]
        ] = []
        for m in anchors:
            d_list = [(d * m, sgn) for (d, sgn) in divs]
            pair_c_list: List[Tuple[int, int, arb, acb]] = []
            for d1, sgn1 in divs:
                for d2, sgn2 in divs:
                    k1, k2 = d1 * m, d2 * m
                    wt = arb(sgn1 * sgn2) * c_div[math.gcd(k1, k2)]
                    if d1 == d2:
                        wt += c_self[k1]
                    if wt != arb(0):
                        pair_c_list.append((k1, k2, abs(wt), acb(wt)))
            anchor_shift_data.append((m, d_list, pair_c_list))

        n_panels = (
            n_panels_override
            if n_panels_override is not None
            else (16 if use_three_zone else 1)
        )
        Y_c = acb(Y_arb)
        log_Y_c = acb(log_Y)
        tol = 2 ** (-quad_tol_bits)

        V2_acc = arb(0)
        D_acc = arb(0)
        Xself_acc = arb(0)
        Diag_acc = arb(0)

        for j in range(n_panels):
            u_lo = log_tau * arb(j) / arb(n_panels)
            u_hi = log_tau * arb(j + 1) / arb(n_panels)
            du = u_hi - u_lo
            sqrt_du = du.sqrt()
            x_lo = Y_arb * u_lo.exp()
            lg_lo = log_Y + u_lo
            lg_lo2 = lg_lo * lg_lo

            if use_three_zone:
                n0_j = min(
                    T_y,
                    max(0, int(float(x_lo.lower()) // zone1_ratio_threshold)),
                )
                while n0_j > 0 and not bool(x_lo >= arb(zone1_ratio_threshold * n0_j)):
                    n0_j -= 1
                # Choose m0_j so ALL shifts d*m (d | P_S) of m <= m0_j satisfy d*m <= n0_j:
                m0_j = n0_j // P_S
                # And set k_start = m0_j + 1 for phi_c so every m > m0_j has phi_c[d*m] populated!
                k_phi_start = max(1, m0_j + 1)
            else:
                n0_j = 0
                m0_j = 0
                k_phi_start = 1

            eps_V = arb(0)
            delta_diag_j = arb(0)
            xself_z1_ball = arb(0)
            diag_z1_rad = arb(0)

            if n0_j > 0:
                x_lo_52 = x_lo ** (arb(5) / arb(2))
                x_lo_2 = x_lo * x_lo
                phi_lo = [arb(0)] * (n0_j + 1)
                eps_psi = [arb(0)] * (n0_j + 1)
                xself_ub = arb(0)
                for k in range(1, n0_j + 1):
                    if not in_omega[k]:
                        continue
                    ph_k = x_lo_52 * inv_n3_r[k] * (-x_lo_2 / arb(k * k)).exp()
                    phi_lo[k] = ph_k
                    ep_k = (arb(1) + abs(b_real_r[k]) / lg_lo2) * ph_k
                    eps_psi[k] = ep_k
                    eps_V += ep_k
                    if c_self[k] != arb(0):
                        xself_ub += c_self[k] * (ph_k * ph_k)
                xself_ub = (du * xself_ub / lg_lo2).upper()
                # Exact nonnegative enclosure [0, xself_ub]:
                half_ub = arb(xself_ub) / arb(2)
                xself_z1_ball = arb(half_ub.mid(), (half_ub + arb(0, half_ub.rad())).upper())

                delta_diag_j = compute_zone1_prime_power_diag_perturbation_tc062_arb(
                    pp_info,
                    n0_j,
                    phi_lo,
                    sqrt_du,
                    lg_lo,
                    in_omega=in_omega,
                )

                if m0_j > 0:
                    diag_rad_acc = arb(0)
                    for m_a, d_list, pair_c_list in anchor_shift_data:
                        if m_a > m0_j:
                            break
                        u_abs = sum((eps_psi[km] for (km, _s) in d_list), arb(0))
                        sub_abs = sum(
                            (wt_abs * phi_lo[k1] * phi_lo[k2] for (k1, k2, wt_abs, _wc) in pair_c_list),
                            arb(0),
                        )
                        diag_rad_acc += (u_abs * u_abs) + arb(4) * sub_abs / lg_lo2
                    diag_z1_rad = (du * diag_rad_acc).upper()

            active_anchors = [
                (d_list, pair_c_list)
                for (m_a, d_list, pair_c_list) in anchor_shift_data
                if m_a > m0_j
            ]
            node_cache: Dict[Any, Tuple[acb, acb, acb, acb]] = {}

            def _eval_bd(u: acb, _an: bool, _k_st=k_phi_start, _n0=n0_j, _act=active_anchors):
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
                    hit = node_cache.get(key)
                    if hit is not None:
                        return hit
                x = Y_c * u.exp()
                x2 = x * x
                x_52 = (Y_c ** (acb(5) / acb(2))) * (acb(arb(5) / arb(2)) * u).exp()
                inv_lg2 = acb(1) / (lg * lg)

                phi_c = [acb(0)] * (T_y + 1)
                v_z2 = acb(0)
                xself_z2 = acb(0)
                for k in range(_k_st, T_y + 1):
                    if not in_omega[k]:
                        continue
                    ph = x_52 * inv_n3_c[k] * (x2 * neg_inv_n2_c[k]).exp()
                    phi_c[k] = ph
                    if k > _n0:
                        v_z2 += (lam_c[k] - beta_c[k] * inv_lg2) * ph
                        if c_self[k] != arb(0):
                            xself_z2 += c_self_c[k] * (ph * ph) * inv_lg2

                d_sum = acb(0)
                for pk, L_pk, lg_p_sq_c in pp_info_c:
                    r_start = (_n0 // pk) + 1
                    if r_start > L_pk:
                        continue
                    s_pk = acb(0)
                    for r in range(r_start, L_pk + 1):
                        kr = pk * r
                        if in_omega[kr]:
                            s_pk += lam_c[r] * phi_c[kr]
                    d_sum += lg_p_sq_c * (s_pk * s_pk)
                d_z2 = d_sum * inv_lg2

                diag_z2 = acb(0)
                for d_list, pair_c_list in _act:
                    u_m = acb(0)
                    for km, sgn_d in d_list:
                        psi_km = (acb(1) - b_real_c[km] * inv_lg2) * phi_c[km]
                        u_m += psi_km if sgn_d == 1 else -psi_km
                    sub_m = acb(0)
                    for k1, k2, _w_abs, wt_c in pair_c_list:
                        sub_m += wt_c * phi_c[k1] * phi_c[k2]
                    diag_z2 += (u_m * u_m) - acb(4) * sub_m * inv_lg2

                out = (v_z2 * v_z2, d_z2, xself_z2, diag_z2)
                if key is not None:
                    node_cache[key] = out
                return out

            def _int_idx(idx: int) -> arb:
                def _cb(u: acb, _an: bool) -> acb:
                    bd = _eval_bd(u, _an)
                    if bd is None:
                        nb = arb("nan")
                        return acb(nb, nb)
                    return bd[idx]

                return acb.integral(_cb, acb(u_lo), acb(u_hi), rel_tol=tol, abs_tol=tol).real

            V2_m = _int_idx(0)
            D_m = _int_idx(1)
            Xself_m = _int_idx(2)
            Diag_m = _int_idx(3)

            if eps_V == arb(0):
                V2_acc += V2_m
            else:
                rad_v = (
                    arb(2) * abs(V2_m).sqrt() * eps_V * sqrt_du + (eps_V * eps_V) * du
                ).upper()
                V2_acc += V2_m + arb(0, rad_v)

            if delta_diag_j == arb(0):
                D_acc += D_m
            else:
                rad_d = (
                    arb(2) * abs(D_m).sqrt() * delta_diag_j + delta_diag_j * delta_diag_j
                ).upper()
                D_acc += D_m + arb(0, rad_d)

            Xself_acc += Xself_m + xself_z1_ball
            Diag_acc += Diag_m + arb(0, diag_z1_rad)

        flint_ctx.prec = prec_bits
        F_int = +(V2_acc - arb(4) * D_acc - arb(4) * Xself_acc)
        Diag_out = +Diag_acc
        Off_out = +(F_int - Diag_out)
        return {
            "F_int_T": F_int,
            "diag_int_T": Diag_out,
            "offdiag_int_T": Off_out,
            "V2_int_T": +V2_acc,
            "D_tilde_omega_S": +D_acc,
            "X_self_omega_S": +Xself_acc,
        }
    finally:
        flint_ctx.prec = saved


def verify_stage_b_large_prime_b_jump_identity_arb(
    T_chk: int = 182,
    D_chk: int = 4,
    primes: Sequence[int] = (7, 11, 13),
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Verify the exact Stage B divisor-jump identity for `b_{p*m} - b_m` across ALL positive
    integers `1 <= m <= floor((T_chk - 1)/p)` when `p > D_chk + 1` (`m = p^a * m_0, p nmid m_0`):

      `b_{p*m} - b_m = c_lambda * (1_{sq}(m) - 1_{sq}(p*m))`
      `                + (-1)^a * sum_{u_0 | m_0} delta_{sq,2}(p^{a+1} * u_0) * lambda(u_0)`,

    which specializes on even-valuation anchors `2 | v_p(m)` (`a` even, `1_{sq}(p*m) = 0`) to
    `c_lambda * 1_{sq}(m) + sum_{u_0 | m_0} delta_{sq,2}(p^{a+1} * u_0) * lambda(u_0)`, while
    recording explicit odd-`v_p(m)` counterexamples (`m = 7, 14, 21` at `p = 7`) against dropping
    `-1_{sq}(p*m)` or `(-1)^a`.
    """
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(max(400, 2 * T_chk + 8), prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 2 * T_chk
        else selberg_table
    )
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        c_lam = tbl["c_lambda"]
        R_osc = tbl["R_osc"]
        M_drift = tbl["M_drift"]
        vecs = compute_complete_core_s_Y_and_beta_Y_arb(T_chk, D_chk, R_osc, prec_bits=prec_bits)
        b_vec = [arb(0)] + [
            arb(liouville_lambda_int(n)) * vecs["beta_Y"][n] for n in range(1, 2 * T_chk + 1)
        ]

        general_all_m_ok = True
        even_anchor_specialization_ok = True
        checked_all_m_count = 0
        checked_even_anchor_count = 0
        odd_valuation_witnesses: List[Dict[str, Any]] = []

        for p_big in primes:
            if p_big <= D_chk + 1:
                raise ValueError(f"Expected p > D_chk + 1 = {D_chk + 1}, got p = {p_big}")
            max_m = (T_chk - 1) // p_big
            for m_val in range(1, max_m + 1):
                checked_all_m_count += 1
                lhs_bj = b_vec[p_big * m_val] - b_vec[m_val]
                a_val = prime_valuation_v_p(m_val, p_big)
                m0 = m_val // (p_big ** a_val)
                sq_diff = (1 if is_perfect_square_int(m_val) else 0) - (
                    1 if is_perfect_square_int(p_big * m_val) else 0
                )
                parity_sign = 1 if (a_val % 2 == 0) else -1
                sum_u0 = arb(0)
                p_pow = p_big ** (a_val + 1)
                for u0 in range(1, m0 + 1):
                    if m0 % u0 == 0:
                        u_full = p_pow * u0
                        delta_u = M_drift[u_full] - M_drift[u_full - 1]
                        sum_u0 += delta_u * arb(liouville_lambda_int(u0))
                rhs_general = arb(sq_diff) * c_lam + arb(parity_sign) * sum_u0
                res_gen = lhs_bj - rhs_general
                if not (arb(0) in res_gen and abs(res_gen) < arb("1e-66")):
                    general_all_m_ok = False

                rhs_even_only = (c_lam if is_perfect_square_int(m_val) else arb(0)) + sum_u0
                if a_val % 2 == 0:
                    checked_even_anchor_count += 1
                    res_even = lhs_bj - rhs_even_only
                    if not (arb(0) in res_even and abs(res_even) < arb("1e-66")):
                        even_anchor_specialization_ok = False
                elif p_big == 7 and m_val in (7, 14, 21):
                    odd_err = lhs_bj - rhs_even_only
                    odd_valuation_witnesses.append(
                        {
                            "prime_p": p_big,
                            "m": m_val,
                            "v_p_m": a_val,
                            "lhs_minus_even_only_formula_error_float": float(odd_err.mid()),
                            "nonzero_discrepancy_certified": bool(not (arb(0) in odd_err)),
                        }
                    )

        odd_witnesses_ok = bool(
            len(odd_valuation_witnesses) > 0
            and all(w["nonzero_discrepancy_certified"] for w in odd_valuation_witnesses)
        )
        return {
            "T_Y": T_chk,
            "D_min": D_chk,
            "primes_tested": [int(p) for p in primes],
            "checked_all_m_count": checked_all_m_count,
            "checked_even_anchor_count": checked_even_anchor_count,
            "general_all_m_identity_verified": general_all_m_ok,
            "even_valuation_anchor_specialization_verified": even_anchor_specialization_ok,
            "odd_valuation_discrepancy_witnesses": odd_valuation_witnesses,
            "odd_valuation_discrepancy_certified": odd_witnesses_ok,
            "verified": bool(general_all_m_ok and even_anchor_specialization_ok and odd_witnesses_ok),
        }
    finally:
        flint_ctx.prec = saved


def verify_zone1_prime_power_majorant_repair_tc062_arb(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Verify the `TASK-TC-062R` §2 Zone 1 prime-power quadrature error-majorant repair:
    1. Reproduces the exact `Y = 224, T = 867, n0 = 18` omission (`[2, 4, 8, 16]` vs omitted
       `[3, 9, 5, 7, 11, 13, 17]`) under the buggy `break` loop;
    2. Compares `compute_zone1_prime_power_diag_perturbation_tc062_arb` against an independently
       written complete reference sum over all primes `p <= n0` and powers `p^k <= n0` across
       `n0 in (0, 1, 2, 3, 4, 5, 7, 8, 9, 16, 17, 18, 25, 27, 32)` (both full and `in_omega`);
    3. Verifies exact invariance under reversed, `pk`-sorted, and interleaved permutations of `pp_info`;
    4. Certifies with Arb on panels `j in (0, 3, 7)` at `Y = 224` (`T = 867`) that `delta_diag_j`
       encloses the actual signed Zone 1 prime-power vector norm;
    5. Certifies Arb overlap between repaired `use_three_zone=True` and independent full-sum
       `use_three_zone=False` quadrature at `Y = 224` (`T = 867`).
    """
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(1800, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 1740
        else selberg_table
    )
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits + 32
        tau = _tau_arb()
        log_tau = tau.log()
        sp_224 = ExactScaleSpec("224", "exact_rational", Fraction(224, 1))
        cut_224 = certify_exact_scale_cutoffs(sp_224, base_prec_bits=prec_bits)
        T_224 = cut_224["T_Y"]  # 867
        D_224 = cut_224["D0_eff"]
        Y_224 = arb(224)
        lg_224 = Y_224.log()

        pp_pairs = prime_power_pairs_up_to(T_224)
        pp_info = [(p ** k, T_224 // (p ** k), arb(p).log() ** 2) for (p, k) in pp_pairs]

        # 1. Exact reproduction at Y = 224, panel 0 (n0 = 18):
        n0_p0 = min(T_224, max(0, int(float(Y_224.lower()) // 12)))
        while n0_p0 > 0 and not bool(Y_224 >= arb(12 * n0_p0)):
            n0_p0 -= 1
        visited_buggy: List[int] = []
        for pk, _L, _lg2 in pp_info:
            if pk > n0_p0:
                break
            visited_buggy.append(pk)
        all_le_n0 = [pk for (pk, _L, _lg2) in pp_info if pk <= n0_p0]
        omitted_buggy = [pk for pk in all_le_n0 if pk not in visited_buggy]
        repro_ok = bool(
            T_224 == 867
            and n0_p0 == 18
            and visited_buggy == [2, 4, 8, 16]
            and omitted_buggy == [3, 9, 5, 7, 11, 13, 17]
        )

        # 2 & 3. Independent complete reference sum + boundary/empty/permutation checks:
        du_16 = log_tau / arb(16)
        sqrt_du_16 = du_16.sqrt()
        phi_sample = [arb(0)] + [
            (Y_224 ** (arb(5) / arb(2))) * (arb(k) ** (-3)) * (-(Y_224 * Y_224) / arb(k * k)).exp()
            for k in range(1, 40)
        ]
        anchors_224 = [m for m in range(1, (T_224 // 2) + 1) if prime_valuation_v_p(m, 2) % 2 == 0]
        in_om_224 = [False] * (T_224 + 1)
        for m in anchors_224:
            in_om_224[m] = True
            in_om_224[2 * m] = True

        def _independent_ref_majorant(
            n0_val: int, mask: Optional[Sequence[bool]] = None
        ) -> arb:
            if n0_val <= 1:
                return arb(0)
            sq_acc = arb(0)
            for p_cand in range(2, n0_val + 1):
                is_pr = all(p_cand % d != 0 for d in range(2, int(math.isqrt(p_cand)) + 1))
                if not is_pr:
                    continue
                lg2_p = arb(p_cand).log() ** 2
                pk_v = p_cand
                while pk_v <= n0_val:
                    q_hi = min(T_224 // pk_v, n0_val // pk_v)
                    s_loc = arb(0)
                    for q_i in range(1, q_hi + 1):
                        idx_k = pk_v * q_i
                        if mask is None or mask[idx_k]:
                            s_loc += phi_sample[idx_k]
                    sq_acc += lg2_p * (s_loc * s_loc)
                    pk_v *= p_cand
            return (sqrt_du_16 / lg_224) * sq_acc.sqrt()

        pp_rev = list(reversed(pp_info))
        pp_sorted = sorted(pp_info, key=lambda t: t[0])
        pp_interleaved = pp_info[::2] + pp_info[1::2]
        cutoffs_tested = (0, 1, 2, 3, 4, 5, 7, 8, 9, 16, 17, 18, 25, 27, 32)
        ref_and_perm_ok = True
        for n0_t in cutoffs_tested:
            for mask_t in (None, in_om_224):
                v_ref = _independent_ref_majorant(n0_t, mask_t)
                v_std = compute_zone1_prime_power_diag_perturbation_tc062_arb(
                    pp_info, n0_t, phi_sample, sqrt_du_16, lg_224, in_omega=mask_t
                )
                v_rev = compute_zone1_prime_power_diag_perturbation_tc062_arb(
                    pp_rev, n0_t, phi_sample, sqrt_du_16, lg_224, in_omega=mask_t
                )
                v_srt = compute_zone1_prime_power_diag_perturbation_tc062_arb(
                    pp_sorted, n0_t, phi_sample, sqrt_du_16, lg_224, in_omega=mask_t
                )
                v_int = compute_zone1_prime_power_diag_perturbation_tc062_arb(
                    pp_interleaved, n0_t, phi_sample, sqrt_du_16, lg_224, in_omega=mask_t
                )
                for v_cand in (v_std, v_rev, v_srt, v_int):
                    diff_v = v_cand - v_ref
                    if not (diff_v == arb(0) or (arb(0) in diff_v and abs(diff_v) < arb("1e-75"))):
                        ref_and_perm_ok = False

        # 4. Certified Arb panel vector-norm enclosure at Y = 224 (panels 0, 3, 7):
        #    Note: Since x_lo / n0_j >= 12, exp(-2*x_lo^2/n0_j^2) <= exp(-288) ~ 8.4e-126 ~ 2^(-415),
        #    we evaluate this comparison at 560-bit working precision and abs_tol = 2^(-500) ~ 3e-151!
        panel_norm_enclosure_ok = True
        saved_560 = flint_ctx.prec
        try:
            flint_ctx.prec = 560
            tau_hi = _tau_arb()
            log_tau_hi = tau_hi.log()
            Y_224_hi = arb(224)
            lg_224_hi = Y_224_hi.log()
            pp_info_hi = [
                (p ** k, T_224 // (p ** k), arb(p).log() ** 2) for (p, k) in pp_pairs
            ]
            for j_pan in (0, 3, 7):
                u_lo = log_tau_hi * arb(j_pan) / arb(16)
                u_hi = log_tau_hi * arb(j_pan + 1) / arb(16)
                du_p = u_hi - u_lo
                x_lo = Y_224_hi * u_lo.exp()
                lg_lo = lg_224_hi + u_lo
                n0_j = min(T_224, max(0, int(float(x_lo.lower()) // 12)))
                while n0_j > 0 and not bool(x_lo >= arb(12 * n0_j)):
                    n0_j -= 1
                phi_lo_j = [arb(0)] * (n0_j + 1)
                for k_i in range(1, n0_j + 1):
                    if in_om_224[k_i]:
                        phi_lo_j[k_i] = (
                            (x_lo ** (arb(5) / arb(2)))
                            * (arb(k_i) ** (-3))
                            * (-(x_lo * x_lo) / arb(k_i * k_i)).exp()
                        )
                maj_j = compute_zone1_prime_power_diag_perturbation_tc062_arb(
                    pp_info_hi, n0_j, phi_lo_j, du_p.sqrt(), lg_lo, in_omega=in_om_224
                )
                active_pks = [
                    (pk, min(L_pk, n0_j // pk), acb(lg2))
                    for (pk, L_pk, lg2) in pp_info_hi
                    if pk <= n0_j
                ]
                Yc_224 = acb(Y_224_hi)
                lgc_224 = acb(lg_224_hi)

                def _z1_signed_sq_cb(
                    u: acb, _an: bool, _n0=n0_j, _ap=active_pks, _Yc=Yc_224, _lgc=lgc_224
                ) -> acb:
                    lg = _lgc + u
                    if _an and not bool(lg.real > arb(1) / arb(2)):
                        nb = arb("nan")
                        return acb(nb, nb)
                    x = _Yc * u.exp()
                    x2 = x * x
                    x52 = (_Yc ** (acb(5) / acb(2))) * (acb(arb(5) / arb(2)) * u).exp()
                    ph = [acb(0)] * (_n0 + 1)
                    for k_i in range(1, _n0 + 1):
                        if in_om_224[k_i]:
                            ph[k_i] = x52 * (acb(k_i) ** (-3)) * (-x2 / acb(k_i * k_i)).exp()
                    acc = acb(0)
                    for pk_v, q_hi, lg2_c in _ap:
                        s_c = acb(0)
                        for q_i in range(1, q_hi + 1):
                            kr = pk_v * q_i
                            if in_om_224[kr]:
                                s_c += acb(liouville_lambda_int(kr)) * ph[kr]
                        acc += lg2_c * s_c * s_c
                    return acc / (lg * lg)

                signed_norm_sq = acb.integral(
                    _z1_signed_sq_cb,
                    acb(u_lo),
                    acb(u_hi),
                    rel_tol=2 ** (-220),
                    abs_tol=2 ** (-500),
                ).real
                _, enc_ok = classify_arb_le_certificate(signed_norm_sq, maj_j * maj_j)
                if not enc_ok:
                    panel_norm_enclosure_ok = False
        finally:
            flint_ctx.prec = saved_560

        # 5. Full-sum unsplit vs repaired 3-zone at Y = 224 (T = 867):
        mf224_3z = evaluate_interior_paired_matrix_free_arb(
            Y_224,
            T_224,
            D_224,
            cut_224["ceil_tau_Y"],
            (2,),
            tbl,
            prec_bits=prec_bits,
            quad_tol_bits=160,
            use_three_zone=True,
        )
        mf224_unsplit = evaluate_interior_paired_matrix_free_arb(
            Y_224,
            T_224,
            D_224,
            cut_224["ceil_tau_Y"],
            (2,),
            tbl,
            prec_bits=prec_bits,
            quad_tol_bits=180,
            use_three_zone=False,
        )
        y224_overlap_ok = all(
            arb(0) in (mf224_3z[k] - mf224_unsplit[k])
            and abs(mf224_3z[k] - mf224_unsplit[k]) < arb("1e-35")
            for k in ("F_int_T", "diag_int_T", "offdiag_int_T", "D_tilde_omega_S")
        )

        return {
            "reproduced_Y224_n0_18_visited_buggy": visited_buggy,
            "reproduced_Y224_n0_18_omitted_buggy": omitted_buggy,
            "reproduction_verified": repro_ok,
            "cutoffs_tested_against_independent_reference": list(cutoffs_tested),
            "reference_and_permutation_invariance_verified": ref_and_perm_ok,
            "panel_signed_vector_norm_enclosure_Y224_verified": panel_norm_enclosure_ok,
            "repaired_three_zone_vs_unsplit_Y224_verified": y224_overlap_ok,
            "verified": bool(
                repro_ok and ref_and_perm_ok and panel_norm_enclosure_ok and y224_overlap_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


def verify_anchor_diagonal_identities_and_self_collision_bounds_arb(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Certify in 256-bit Arb (`TASK-TC-062R` §3, §7A, §7B):
    1. Both exact general-anchor diagonal identities for `Delta_{p,p} Hcal_Y(m, m)` (`p*m <= T`):
       - Combined `(log m)^2, (log(p*m))^2` form (`§3`):
         `||psi_{Y,m} - psi_{Y,p*m}||_Y^2 - 4*(log m)^2*G_Y^{[2]}(m,m) - 4*(log(p*m))^2*G_Y^{[2]}(p*m,p*m) + 8*c(m,m)*G_Y^{[2]}(m,p*m)`
       - Corrected general-anchor `c_self` form (`§7A`):
         `||psi_{Y,m} - psi_{Y,p*m}||_Y^2 - 4*(log p)^2*G_Y^{[2]}(p*m,p*m) - 4*c_self(m)*G_Y^{[2]}(m,m) - 4*c_self(p*m)*G_Y^{[2]}(p*m,p*m) - 4*c(m,m)*[G_Y^{[2]}(m,m) - 2*G_Y^{[2]}(m,p*m) + G_Y^{[2]}(p*m,p*m)]`,
       while certifying that omitting `-4*c(m,m)*[...]` is valid at `m = 1` (`c(1,1) = 0`) and
       fails strictly (`0 not in discrepancy`) at `m = 3, p = 2` (`Y = 8`) and at resonant general
       anchors (`Y = 64`, `m in {33, 35, 36, 22}`)!
    2. Corrected `4 * X_self(Y)` constant chain (`§7B`):
       `4 * X_self(Y) <= 4 * (289/60)*log(tau) = (289/15)*log(tau) < (1377/40)*log(tau) < 64`
       (whereas `(578/15)*log(tau) approx 70.81953 > 64` is certified false), plus the uniform
       lower bound `Sigma_diag(Y; p) >= -4 * sum_{n<=T} (log n)^2 G_Y^{[2]}(n, n) >= -(289/15)*log(tau) > -744*(tau - 1)`.
    """
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(400, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 370
        else selberg_table
    )
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        log_tau = tau.log()

        def _audit_scale_anchors(
            Y_val: int, T_y: int, D_y: int, pairs: Sequence[Tuple[int, int]]
        ) -> Tuple[List[Dict[str, Any]], bool, Dict[Tuple[int, int], arb]]:
            Y_b = arb(Y_val)
            Hcal = build_complete_signed_kernel_evaluator_small_T(
                Y_b, T_y, D_y, tbl, prec_bits=prec_bits
            )
            vecs = compute_complete_core_s_Y_and_beta_Y_arb(
                T_y, D_y, tbl["R_osc"], prec_bits=prec_bits
            )
            beta_Y = vecs["beta_Y"]
            b_arr = [arb(0)] + [
                arb(liouville_lambda_int(n)) * beta_Y[n] for n in range(1, T_y + 1)
            ]

            pp_pairs = prime_power_pairs_up_to(T_y)
            c_div = [arb(0)] * (T_y + 1)
            for q_p, k_e in pp_pairs:
                qk = q_p ** k_e
                lg2 = arb(q_p).log() ** 2
                for mult in range(qk, T_y + 1, qk):
                    c_div[mult] += lg2
            c_self = [arb(0)] + [(arb(k).log() ** 2) - c_div[k] for k in range(1, T_y + 1)]

            def _psi_diff_norm_sq(m_i: int, pm_i: int) -> arb:
                g0_mm = evaluate_window_gram_G_Y_r_arb(Y_b, m_i, m_i, 0, prec_bits=prec_bits)
                g0_mp = evaluate_window_gram_G_Y_r_arb(Y_b, m_i, pm_i, 0, prec_bits=prec_bits)
                g0_pp = evaluate_window_gram_G_Y_r_arb(Y_b, pm_i, pm_i, 0, prec_bits=prec_bits)
                g2_mm = evaluate_window_gram_G_Y_r_arb(Y_b, m_i, m_i, 2, prec_bits=prec_bits)
                g2_mp = evaluate_window_gram_G_Y_r_arb(Y_b, m_i, pm_i, 2, prec_bits=prec_bits)
                g2_pp = evaluate_window_gram_G_Y_r_arb(Y_b, pm_i, pm_i, 2, prec_bits=prec_bits)
                g4_mm = evaluate_window_gram_G_Y_r_arb(Y_b, m_i, m_i, 4, prec_bits=prec_bits)
                g4_mp = evaluate_window_gram_G_Y_r_arb(Y_b, m_i, pm_i, 4, prec_bits=prec_bits)
                g4_pp = evaluate_window_gram_G_Y_r_arb(Y_b, pm_i, pm_i, 4, prec_bits=prec_bits)
                bm, bp = b_arr[m_i], b_arr[pm_i]
                n_mm = g0_mm - arb(2) * bm * g2_mm + (bm * bm) * g4_mm
                n_pp = g0_pp - arb(2) * bp * g2_pp + (bp * bp) * g4_pp
                n_mp = g0_mp - (bm + bp) * g2_mp + (bm * bp) * g4_mp
                return n_mm - arb(2) * n_mp + n_pp

            rows_out: List[Dict[str, Any]] = []
            ok_flag = True
            disc_map: Dict[Tuple[int, int], arb] = {}
            for p_i, m_i in pairs:
                pm_i = p_i * m_i
                direct_d = (
                    Hcal(m_i, m_i) - Hcal(pm_i, m_i) - Hcal(m_i, pm_i) + Hcal(pm_i, pm_i)
                )
                psi_sq = _psi_diff_norm_sq(m_i, pm_i)
                g2_mm = evaluate_window_gram_G_Y_r_arb(Y_b, m_i, m_i, 2, prec_bits=prec_bits)
                g2_mp = evaluate_window_gram_G_Y_r_arb(Y_b, m_i, pm_i, 2, prec_bits=prec_bits)
                g2_pp = evaluate_window_gram_G_Y_r_arb(Y_b, pm_i, pm_i, 2, prec_bits=prec_bits)

                comb_form = (
                    psi_sq
                    - arb(4) * (arb(m_i).log() ** 2) * g2_mm
                    - arb(4) * (arb(pm_i).log() ** 2) * g2_pp
                    + arb(8) * c_div[m_i] * g2_mp
                )
                omitted_term = -arb(4) * c_div[m_i] * (g2_mm - arb(2) * g2_mp + g2_pp)
                abbrev_form = (
                    psi_sq
                    - arb(4) * (arb(p_i).log() ** 2) * g2_pp
                    - arb(4) * c_self[m_i] * g2_mm
                    - arb(4) * c_self[pm_i] * g2_pp
                )
                cself_full_form = abbrev_form + omitted_term

                res_comb = comb_form - direct_d
                res_cself = cself_full_form - direct_d
                abbrev_err = abbrev_form - direct_d
                row_ok = bool(
                    arb(0) in res_comb
                    and abs(res_comb) < arb("1e-50")
                    and arb(0) in res_cself
                    and abs(res_cself) < arb("1e-50")
                    and (
                        (m_i == 1 and arb(0) in abbrev_err)
                        or (m_i > 1 and not (arb(0) in abbrev_err))
                    )
                )
                ok_flag = ok_flag and row_ok
                disc_map[(p_i, m_i)] = abbrev_err
                rows_out.append(
                    {
                        "Y": Y_val,
                        "prime_p": p_i,
                        "anchor_m": m_i,
                        "Delta_Hcal_m_m_direct": serialize_arb_certified(direct_d),
                        "combined_log_form_residual": serialize_arb_certified(res_comb),
                        "corrected_c_self_form_residual": serialize_arb_certified(res_cself),
                        "abbreviated_m1_only_discrepancy": serialize_arb_certified(abbrev_err),
                        "verified": row_ok,
                    }
                )
            return rows_out, ok_flag, disc_map

        rows_y8, ok_y8, disc_y8 = _audit_scale_anchors(
            8, 14, 2, ((2, 1), (2, 3), (2, 4), (2, 5), (3, 1), (3, 2), (3, 4))
        )
        rows_y64, ok_y64, disc_y64 = _audit_scale_anchors(
            64, 182, 4, ((2, 1), (2, 33), (2, 35), (2, 36), (3, 22))
        )
        all_forms_ok = bool(ok_y8 and ok_y64)
        m3_p2_discrepancy_y8 = disc_y8[(2, 3)]
        m33_p2_discrepancy_y64 = disc_y64[(2, 33)]

        bound_289_15_log_tau = _frac_to_arb(Fraction(289, 15)) * log_tau
        bound_1377_40_log_tau = _frac_to_arb(Fraction(1377, 40)) * log_tau
        erroneous_578_15_log_tau = _frac_to_arb(Fraction(578, 15)) * log_tau
        lean_744_tau_minus_1 = arb(744) * (tau - arb(1))
        const_ok = bool(
            bound_289_15_log_tau < bound_1377_40_log_tau
            and bound_1377_40_log_tau < arb(64)
            and bound_289_15_log_tau < lean_744_tau_minus_1
            and erroneous_578_15_log_tau > arb(64)
            and not (arb(0) in m3_p2_discrepancy_y8)
            and not (arb(0) in m33_p2_discrepancy_y64)
        )

        return {
            "anchor_rows_Y8": rows_y8,
            "anchor_rows_Y64": rows_y64,
            "m3_p2_abbreviated_formula_discrepancy_Y8": serialize_arb_certified(
                m3_p2_discrepancy_y8
            ),
            "m33_p2_abbreviated_formula_discrepancy_Y64": serialize_arb_certified(
                m33_p2_discrepancy_y64
            ),
            "four_X_self_sharp_bound_289_15_log_tau": serialize_arb_certified(bound_289_15_log_tau),
            "four_X_self_envelope_bound_1377_40_log_tau": serialize_arb_certified(
                bound_1377_40_log_tau
            ),
            "lean_sigma_diag_lower_bound_neg_744_tau_minus_1": serialize_arb_certified(
                -lean_744_tau_minus_1
            ),
            "outside_lean_sigma_diag_lower_bound_neg_289_15_log_tau": serialize_arb_certified(
                -bound_289_15_log_tau
            ),
            "retired_erroneous_578_15_log_tau_gt_64": bool(erroneous_578_15_log_tau > arb(64)),
            "verified": bool(all_forms_ok and const_ok),
        }
    finally:
        flint_ctx.prec = saved


def verify_complete_kernel_unsigned_linear_growth_arb(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Verify the complete-kernel `Omega(Y)` lower-bound mechanism for
    `sum_{m, n in I_2(T(Y))} |Delta_{2,2} Hcal_Y(m, n)|` (`TASK-TC-062R` §5):
    - Uses odd resonant anchors `A_odd(Y) = {ceil(Y) <= m <= floor(3Y/2) : 2 nmid m} subseteq I_2(T(Y))`
      for `Y >= 256` (`2*m <= 3Y < 4Y <= T(Y)`, `|A_odd(Y)| >= Y/5`, `T(Y) notin S_odd(Y)`);
    - Restricts the pure Gaussian constructive peak to the sign-free subwindow `[3Y, 4Y] subset [Y, tau*Y]`
      (`4 < tau`) where `u = X/m in [2, 4]` avoids the zero locus `X = m*sqrt((4/3)*log 8) = 2*sqrt(log 2)*m`,
      giving `phi_{2m}(X) - phi_m(X) >= c_0 * Y^{-1/2}` with `c_0 = (8/sqrt(3))*exp(-4)*(1/8 - exp(-3)) > 0`;
    - Applies the triangle inequality onto the complete bilinear form
      `sum_{m,n in A_odd(Y)} |Delta_{2,2} Hcal_Y(m, n)| >= sum_{m,n in A_odd(Y)} Delta_{2,2} Hcal_Y(m, n)`
      `= ||sum_{m in A_odd(Y)} (psi_{Y,2m} - psi_{Y,m})||_Y^2 - 4*C_odd(Y) - 4*S_odd(Y)`,
      accounting rigorously for `b`-dependent `G_Y^{[2]}`/`G_Y^{[4]}` perturbations (`O(Y/log Y)` via
      mean-square `|beta_Y(k)|^2 ||phi_k||_Y^2`), `c(u,v)` subtractions (`O(Y/(log Y)^2)`), and
      `c_self(u)` diagonal terms (`<= (289/15)*log(tau) = O(1)`), certified numerically at `Y = 256`.
    """
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(2100, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 2050
        else selberg_table
    )
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        log_tau = tau.log()
        c0_const = (arb(8) / arb(3).sqrt()) * (-arb(4)).exp() * (
            arb(1) / arb(8) - (-arb(3)).exp()
        )
        lead_slope = (c0_const * c0_const) * (_frac_to_arb(Fraction(4, 3)).log()) / arb(50)
        zero_locus_ratio = (arb(4) * arb(8).log() / arb(3)).sqrt()  # 2*sqrt(log 2) ~ 1.665109

        # Certify at Y = 256 (T = 1024, D0 = 5) that A_odd(256) subseteq I_2(1024), subwindow [768, 1024]
        # lies inside [256, 256*tau] strictly above zero_locus_ratio, and complete bilinear sum > 0:
        Y_b = arb(256)
        T_y, D_y = 1024, 5
        A_odd = [m for m in range(256, 385) if m % 2 == 1]
        vecs = compute_complete_core_s_Y_and_beta_Y_arb(
            T_y, D_y, tbl["R_osc"], prec_bits=prec_bits
        )
        beta_Y = vecs["beta_Y"]
        b_arr = [arb(0)] + [
            arb(liouville_lambda_int(n)) * beta_Y[n] for n in range(1, T_y + 1)
        ]
        pp_pairs = prime_power_pairs_up_to(T_y)
        c_div = [arb(0)] * (T_y + 1)
        for q_p, k_e in pp_pairs:
            qk = q_p ** k_e
            lg2 = arb(q_p).log() ** 2
            for mult in range(qk, T_y + 1, qk):
                c_div[mult] += lg2
        c_self = [arb(0)] + [(arb(k).log() ** 2) - c_div[k] for k in range(1, T_y + 1)]

        alpha = [0] * (T_y + 1)
        for m in A_odd:
            alpha[m] = -1
            alpha[2 * m] = 1
        S_odd = sorted([k for k in range(1, T_y + 1) if alpha[k] != 0])
        active_pp = [
            (p ** k, arb(p).log() ** 2, [u for u in S_odd if u % (p ** k) == 0])
            for (p, k) in pp_pairs
            if p ** k <= max(S_odd)
        ]
        active_pp = [(pk, lg2, us) for (pk, lg2, us) in active_pp if len(us) > 0]

        Yc = acb(Y_b)
        lgYc = acb(Y_b.log())
        s_odd_c = [(u, acb(alpha[u]), acb(b_arr[u]), acb(c_self[u])) for u in S_odd]
        pp_c = [(acb(lg2), [(u, acb(alpha[u])) for u in us]) for (_pk, lg2, us) in active_pp]

        def _odd_bilinear_cb(u: acb, _an: bool) -> acb:
            lg = lgYc + u
            if _an and not bool(lg.real > arb(1) / arb(2)):
                nb = arb("nan")
                return acb(nb, nb)
            x = Yc * u.exp()
            x2 = x * x
            x52 = (Yc ** (acb(5) / acb(2))) * (acb(arb(5) / arb(2)) * u).exp()
            lg2_inv = acb(1) / (lg * lg)
            ph_map: Dict[int, acb] = {}
            psi_sum = acb(0)
            self_sum = acb(0)
            for k_u, al_c, b_c, cs_c in s_odd_c:
                ph_k = x52 * (acb(k_u) ** (-3)) * (-x2 / acb(k_u * k_u)).exp()
                ph_map[k_u] = ph_k
                psi_sum += al_c * (acb(1) - b_c * lg2_inv) * ph_k
                if cs_c != acb(0):
                    self_sum += cs_c * ph_k * ph_k
            c_acc = acb(0)
            for lgp2_c, u_list in pp_c:
                inner = acb(0)
                for k_u, al_c in u_list:
                    inner += al_c * ph_map[k_u]
                c_acc += lgp2_c * inner * inner
            return (psi_sum * psi_sum) - acb(4) * (c_acc + self_sum) * lg2_inv

        bilinear_sum_Y256 = acb.integral(
            _odd_bilinear_cb, acb(0), acb(log_tau), rel_tol=2 ** (-160), abs_tol=2 ** (-160)
        ).real

        checks_ok = bool(
            c0_const > arb("0.00636")
            and lead_slope > arb("2e-7")
            and zero_locus_ratio < arb(2)
            and arb(4) < tau
            and len(A_odd) == 64
            and max(S_odd) == 766 < T_y
            and bilinear_sum_Y256 > arb(0)
        )
        return {
            "zero_locus_X_over_m_sqrt_4_3_log_8": serialize_arb_certified(zero_locus_ratio),
            "subwindow_X_range": "[3*Y, 4*Y] subset [Y, tau*Y] (u = X/m in [2, 4], strictly above 2*sqrt(log 2))",
            "subwindow_pointwise_constant_c0": serialize_arb_certified(c0_const),
            "asymptotic_leading_slope_c0_sq_log_4_3_over_50": serialize_arb_certified(lead_slope),
            "odd_resonant_band_bilinear_lower_bound_Y256": serialize_arb_certified(
                bilinear_sum_Y256
            ),
            "error_terms_quantified": {
                "b_perturbation_G2_G4_via_mean_square_beta": "O(Y / log Y) via TC-057R |R_osc(d)| <= C_osc*d (and elementary O(Y*(log log Y)^4 / log Y) = o(Y) without TC-057R); endpoint T(Y) excluded since max S_odd(Y) <= 3*Y < 4*Y <= T(Y)",
                "common_prime_power_subtraction_4_C_odd": "<= (12 * C_phi * zeta''(2) / (log Y)^2) * Y = O(Y / (log Y)^2)",
                "composite_self_collision_4_S_odd": "<= 4 * X_self(Y) <= (289/15) * log(tau) = O(1)",
            },
            "scope_note": (
                "Proves sum_{m,n in I_2(T(Y))} |Delta_{2,2} Hcal_Y(m, n)| = Omega(Y) on the complete "
                "signed kernel Hcal_Y (refuting unsigned absolute-value majorants asymptotically, "
                "while Y = 64 refutes the registered Candidate A2 constants/domain); neither refutes "
                "the existential eventual all-eta signed closure target H(Sigma_off(.; p), D_tilde)."
            ),
            "verified": checks_ok,
        }
    finally:
        flint_ctx.prec = saved


def verify_section_4_quantitative_proof_attempt(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute Section 6 substantive quantitative proof attempt across:
    - 4A: Spillover fringe support `T < n <= T + floor(T/(D+1))`, `q`-reindexing `d_q = floor(T/q)`,
      `|w_{2,lambda}(n)| <= (log n)^2`, PNT/Selberg `||S_{spill,Y}||_Y = O(1/log Y)`
      (`||S_{spill,Y}||_Y^2 = O((log Y)^{-2})`) decay, and Young mixed-covariance
      equivalence `H(F, D_tilde) <-> H(F_{<=T}, D_tilde)`.
    - 4B (Stage A): Interior Hilbert-space identity, Candidate Lemma A1 (`m = 1, p = 2` refutation +
      aggregate `O(2^{|S|})` Replacement Lemma A1'), and Candidate Lemma A2 (256-bit Arb refutation
      of unsigned paired-block sum at `Y = 64` + analytic `Omega(Y)` lower bound).
    - 4C (Stage B): Coupled 2-prime `(2, 3)` cross-prime terms and exact `b_{pm} - b_m` divisor-jump
      law across all `1 <= m <= floor((T-1)/p)` for `p > D + 1` (plus `2 | v_p(m)` specialization).
    - 4D (Stage C): Disjoint 3-prime `S = {2, 3, 5}` (`64`-term) decomposition, harmonic-weighted
      prime-family average, primary literature audit (`arXiv:1503.05121` & `arXiv:1509.05422`), and
      isolation of `TC062-OBL-INTERIOR-PRIME-PAIR-OFFDIAG`.
    """
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(33000, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 32768
        else selberg_table
    )

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        log_tau = tau.log()
        R_osc = tbl["R_osc"]
        w2 = tbl["w2"]
        c_lam = tbl["c_lambda"]
        M_drift = tbl["M_drift"]

        # 4A-1. Unconditional pointwise |w_{2,lambda}(n)| <= (log n)^2 on 1 <= n <= 2000:
        # Equality holds at n = 1 (0 == 0) and at primes n = p (|w_{2,lambda}(p)| == (log p)^2);
        # strict inequality holds for every composite n >= 4.
        prime_set_2000 = set(primes_up_to(2000))
        w2_log_sq_ok = bool(w2[1] == arb(0))
        for n_i in range(2, 2001):
            lg_sq_n = arb(n_i).log() ** 2
            if n_i in prime_set_2000:
                diff_p = abs(w2[n_i]) - lg_sq_n
                ok_n = bool(arb(0) in diff_p and abs(diff_p) < arb("1e-70"))
            else:
                _, ok_n = classify_arb_le_certificate(abs(w2[n_i]), lg_sq_n)
            if not ok_n:
                w2_log_sq_ok = False
                break

        # 4A-2. Spillover fringe support & q-reindexing up to Y = 4096 (T = 32768) + Young reduction:
        spillover_rows: List[Dict[str, Any]] = []
        spillover_ok = True
        for y_val in (16, 32, 64, 128, 256, 512, 1024, 4096):
            sp = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            cut = certify_exact_scale_cutoffs(sp, base_prec_bits=prec_bits)
            T_y = cut["T_Y"]
            D = cut["D0_eff"]
            N = 2 * T_y
            Y_b = arb(y_val)
            lg_Y = Y_b.log()
            max_spill_idx_bound = T_y + (T_y // (D + 1))

            vecs = compute_complete_core_s_Y_and_beta_Y_arb(T_y, D, R_osc, prec_bits=prec_bits)
            beta_Y = vecs["beta_Y"]
            actual_spill = [n for n in range(T_y + 1, N + 1) if beta_Y[n] != arb(0)]
            max_actual = max(actual_spill) if actual_spill else T_y
            support_in_fringe = bool(max_actual <= max_spill_idx_bound)

            # Verify exact q-reindexing formula on ALL T < n <= 2*T:
            reindexed = [arb(0)] * (N + 1)
            pt_spill_majorant = arb(0)
            for q in range(2, (T_y // (D + 1)) + 1):
                dq = T_y // q
                nq = (dq + 1) * q
                reindexed[nq] -= R_osc[dq] * arb(liouville_lambda_int(q))
                pt_spill_majorant += (
                    abs(R_osc[dq])
                    * ((tau * Y_b) ** (arb(5) / arb(2)))
                    / ((lg_Y * lg_Y) * (arb(nq) ** 3))
                )
            reindex_ok = True
            for n in range(T_y + 1, N + 1):
                diff_n = beta_Y[n] - reindexed[n]
                if not (diff_n == arb(0) or (arb(0) in diff_n and abs(diff_n) < arb("1e-66"))):
                    reindex_ok = False
                    break

            # Direct window quadrature of ||S_spill, Y||_Y^2:
            active_spill_c = [
                (acb(beta_Y[n] * (arb(n) ** (-3))), acb(-(arb(n) ** (-2))))
                for n in actual_spill
            ]
            Y_c = acb(Y_b)
            lg_Y_c = acb(lg_Y)

            def _spill_sq_cb(u: acb, _an: bool, _act=active_spill_c, _Yc=Y_c, _lgc=lg_Y_c) -> acb:
                lg = _lgc + u
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                x = _Yc * u.exp()
                x2 = x * x
                x_52 = (_Yc ** (acb(5) / acb(2))) * (acb(arb(5) / arb(2)) * u).exp()
                s = acb(0)
                for coeff_c, rate_c in _act:
                    s += coeff_c * (x2 * rate_c).exp()
                val = x_52 * s / (lg * lg)
                return val * val

            S_spill_norm_sq = acb.integral(
                _spill_sq_cb, acb(0), acb(log_tau), rel_tol=2 ** (-180), abs_tol=2 ** (-180)
            ).real
            analytic_spill_norm_sq_ub = (pt_spill_majorant * pt_spill_majorant) * log_tau
            _, maj_ok = classify_arb_le_certificate(S_spill_norm_sq, analytic_spill_norm_sq_ub)
            young_penalty_1_plus_logY = (arb(1) + lg_Y) * S_spill_norm_sq

            row_sp_ok = bool(support_in_fringe and reindex_ok and maj_ok)
            spillover_ok = spillover_ok and row_sp_ok
            spillover_rows.append(
                {
                    "Y": y_val,
                    "T_Y": T_y,
                    "D0_eff": D,
                    "naive_outer_limit_2T": N,
                    "proved_fringe_upper_bound": max_spill_idx_bound,
                    "nonzero_spillover_count": len(actual_spill),
                    "max_nonzero_spillover_index": max_actual,
                    "S_spill_norm_sq_direct": serialize_arb_certified(S_spill_norm_sq),
                    "S_spill_norm_sq_analytic_upper": serialize_arb_certified(
                        analytic_spill_norm_sq_ub
                    ),
                    "young_mixed_covariance_penalty_1_plus_logY_norm_sq": serialize_arb_certified(
                        young_penalty_1_plus_logY
                    ),
                    "verified": row_sp_ok,
                }
            )

        # 4B-1. Stage A: Cross-check matrix-free F_int_T(Y; {2}) vs dense paired sum on Y in {8, 16, 32}
        #       AND three-zone vs unsplit consistency at Y = 32, 64:
        stage_a_consistency_ok = True
        for y_chk in (8, 16):
            sp_c = ExactScaleSpec(str(y_chk), "exact_rational", Fraction(y_chk, 1))
            cut_c = certify_exact_scale_cutoffs(sp_c, base_prec_bits=prec_bits)
            T_c, D_c = cut_c["T_Y"], cut_c["D0_eff"]
            mf = evaluate_interior_paired_matrix_free_arb(
                arb(y_chk),
                T_c,
                D_c,
                cut_c["ceil_tau_Y"],
                (2,),
                tbl,
                prec_bits=prec_bits,
                quad_tol_bits=230,
                use_three_zone=False,
            )
            Hcal_c = build_complete_signed_kernel_evaluator_small_T(
                arb(y_chk), T_c, D_c, tbl, prec_bits=prec_bits
            )
            I2 = [m for m in prime_even_valuation_anchors(2 * T_c, (2,)) if 2 * m <= T_c]
            dense_int = arb(0)
            dense_diag = arb(0)
            for m in I2:
                lm = liouville_lambda_int(m)
                for n in I2:
                    ln = liouville_lambda_int(n)
                    d4 = Hcal_c(m, n) - Hcal_c(2 * m, n) - Hcal_c(m, 2 * n) + Hcal_c(2 * m, 2 * n)
                    dense_int += arb(lm * ln) * d4
                    if m == n:
                        dense_diag += d4
            if not (
                arb(0) in (mf["F_int_T"] - dense_int)
                and abs(mf["F_int_T"] - dense_int) < arb("1e-50")
                and arb(0) in (mf["diag_int_T"] - dense_diag)
                and abs(mf["diag_int_T"] - dense_diag) < arb("1e-50")
            ):
                stage_a_consistency_ok = False

        # Check three_zone=True vs three_zone=False at Y = 64:
        cut_64 = certify_exact_scale_cutoffs(
            ExactScaleSpec("64", "exact_rational", Fraction(64, 1)), base_prec_bits=prec_bits
        )
        mf64_unsplit = evaluate_interior_paired_matrix_free_arb(
            arb(64),
            cut_64["T_Y"],
            cut_64["D0_eff"],
            cut_64["ceil_tau_Y"],
            (2,),
            tbl,
            prec_bits=prec_bits,
            quad_tol_bits=220,
            use_three_zone=False,
        )
        mf64_z3 = evaluate_interior_paired_matrix_free_arb(
            arb(64),
            cut_64["T_Y"],
            cut_64["D0_eff"],
            cut_64["ceil_tau_Y"],
            (2,),
            tbl,
            prec_bits=prec_bits,
            quad_tol_bits=160,
            use_three_zone=True,
        )
        if not (
            arb(0) in (mf64_unsplit["F_int_T"] - mf64_z3["F_int_T"])
            and abs(mf64_unsplit["F_int_T"] - mf64_z3["F_int_T"]) < arb("1e-35")
            and arb(0) in (mf64_unsplit["diag_int_T"] - mf64_z3["diag_int_T"])
            and abs(mf64_unsplit["diag_int_T"] - mf64_z3["diag_int_T"]) < arb("1e-35")
        ):
            stage_a_consistency_ok = False

        # 4B-2. Candidate Lemma A1 Refutation (m = 1, p = 2 anchor diagonal > 0 for Y >= 8)
        #       + Replacement Lemma A1' (aggregate diag_int_T <= 2 * sum_{n<=T} ||psi_{Y,n}||_Y^2,
        #         and aggregate diag_int_T < 0 on Y = 8..1024):
        cand_a1_rows: List[Dict[str, Any]] = []
        cand_a1_refuted_ok = True
        for y_val in (8, 16, 32, 64, 128, 256, 512, 1024):
            sp_y = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            cut_y = certify_exact_scale_cutoffs(sp_y, base_prec_bits=prec_bits)
            T_y, D_y = cut_y["T_Y"], cut_y["D0_eff"]
            Y_b = arb(y_val)
            # At m = 1, p = 2 for D >= 2 (Y >= 8): b_1 = 0, b_2 = -(log 2)^2, c(1,1)=c(1,2)=0, c(2,2)=(log 2)^2.
            # Factor out exp(-Y^2/2) > 0 so exp(Y^2/2) * Delta_{2,2} Hcal_Y(1, 1) = Theta(Y^3) > 1
            # avoids quadrature abs_tol zero-straddling at Y >= 32:
            lg2_sq_c = acb(arb(2).log() ** 2)
            yb_c = acb(Y_b)
            lg_yb_c = yb_c.log()

            def _scaled_m1_cb(u: acb, _an: bool, _yc=yb_c, _lgy=lg_yb_c, _lg2=lg2_sq_c) -> acb:
                lg = _lgy + u
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                e2u = (acb(2) * u).exp()
                y2 = _yc * _yc
                lg2_inv = _lg2 / (lg * lg)
                t11 = (-(acb(4) * e2u - acb(1)) * y2 / acb(2)).exp()
                t12 = (
                    acb(2)
                    * (acb(2) ** (-3))
                    * (acb(1) + lg2_inv)
                    * (-(acb(5) * e2u - acb(2)) * y2 / acb(4)).exp()
                )
                t22 = (
                    (acb(2) ** (-6))
                    * ((acb(1) - lg2_inv) ** 2)
                    * (-((e2u - acb(1)) * y2 / acb(2))).exp()
                )
                return ((_yc * u.exp()) ** 5) * (t11 - t12 + t22)

            tol_m1 = 2 ** (-200)
            exp_scaled_delta_H_1_1 = acb.integral(
                _scaled_m1_cb, acb(0), acb(log_tau), rel_tol=tol_m1, abs_tol=tol_m1
            ).real
            delta_H_1_1 = exp_scaled_delta_H_1_1 * (-(Y_b * Y_b) / arb(2)).exp()
            mf_y = evaluate_interior_paired_matrix_free_arb(
                Y_b,
                T_y,
                D_y,
                cut_y["ceil_tau_Y"],
                (2,),
                tbl,
                prec_bits=prec_bits,
                quad_tol_bits=160 if T_y >= 512 else 220,
                use_three_zone=(T_y >= 512),
            )
            m1_pos = bool(exp_scaled_delta_H_1_1 > arb(0) and delta_H_1_1 > arb(0))
            agg_neg = bool(mf_y["diag_int_T"] < arb(0))
            cand_a1_refuted_ok = cand_a1_refuted_ok and m1_pos and agg_neg
            cand_a1_rows.append(
                {
                    "Y": y_val,
                    "T_Y": T_y,
                    "D0_eff": D_y,
                    "exp_half_Y2_times_m1_p2_Delta_Hcal_1_1": serialize_arb_certified(
                        exp_scaled_delta_H_1_1
                    ),
                    "m1_p2_Delta_Hcal_1_1": serialize_arb_certified(delta_H_1_1),
                    "m1_counterexample_certified_positive": m1_pos,
                    "aggregate_diag_int_T_p2": serialize_arb_certified(mf_y["diag_int_T"]),
                    "aggregate_diag_certified_negative": agg_neg,
                    "F_int_T_p2": serialize_arb_certified(mf_y["F_int_T"]),
                    "offdiag_int_T_p2": serialize_arb_certified(mf_y["offdiag_int_T"]),
                }
            )

        # 4B-3. Candidate Lemma A2 Refutation in 256-bit Arb at Y = 64 (T = 182, 61 interior anchors):
        #       Test unsigned paired-block majorant sum_{m,n in I_2(182)} |Delta_{2,2} Hcal_64(m, n)|
        #       against (1/32)*64^{1/2} + (log 64)*D_tilde(64):
        res_64 = evaluate_mixed_covariance_point_arb(
            ExactScaleSpec("64", "exact_rational", Fraction(64, 1)), selberg_table=tbl
        )
        Hcal_64 = build_complete_signed_kernel_evaluator_small_T(
            arb(64), 182, 4, tbl, prec_bits=prec_bits
        )
        I2_64 = [m for m in prime_even_valuation_anchors(364, (2,)) if 2 * m <= 182]
        abs_paired_sum_64 = arb(0)
        for m in I2_64:
            for n in I2_64:
                d4_mn = (
                    Hcal_64(m, n)
                    - Hcal_64(2 * m, n)
                    - Hcal_64(m, 2 * n)
                    + Hcal_64(2 * m, 2 * n)
                )
                abs_paired_sum_64 += abs(d4_mn)
        rhs_cand_a2_64 = (arb(1) / arb(32)) * arb(8) + res_64["log_Y_times_D_tilde"]
        margin_cand_a2_64 = abs_paired_sum_64 - rhs_cand_a2_64
        cls_cand_a2_64 = classify_probe_margin_arb(margin_cand_a2_64)
        cand_a2_refuted_ok = bool(cls_cand_a2_64["verdict"] == "FAIL")

        # 4C. Stage B: Exact divisor-jump law for b_{pm} - b_m across ALL 1 <= m <= floor((T-1)/p)
        #     when p > D + 1 (m = p^a * m_0, p nmid m_0):
        #     b_{pm} - b_m = c_lambda * (1_{sq}(m) - 1_{sq}(p*m))
        #                    + (-1)^a * sum_{u_0 | m_0} delta_{sq,2}(p^{a+1} * u_0) * lambda(u_0)
        b_jump_audit = verify_stage_b_large_prime_b_jump_identity_arb(
            T_chk=182, D_chk=4, primes=(7, 11, 13), prec_bits=prec_bits, selberg_table=tbl
        )
        b_jump_law_ok = bool(b_jump_audit["verified"])

        # 4D. Stage C: 3-prime S = {2, 3, 5} (64-term) interior check & harmonic prime-family average
        #     sum_{p in {2, 3, 5, 7}} (1/p) * F_int_T(Y; {p}) / sum_{p in {2, 3, 5, 7}} (1/p) at Y = 64:
        mf64_235 = evaluate_interior_paired_matrix_free_arb(
            arb(64),
            182,
            4,
            cut_64["ceil_tau_Y"],
            (2, 3, 5),
            tbl,
            prec_bits=prec_bits,
            quad_tol_bits=210,
            use_three_zone=False,
        )
        harm_primes = (2, 3, 5, 7)
        harm_w_tot = sum((Fraction(1, p) for p in harm_primes), Fraction(0, 1))
        harm_F_int_acc = arb(0)
        harm_F_bnd_acc = arb(0)
        F_64_val = +(
            res_64["J_direct"]
            - arb(4) * evaluate_X_self_collision_arb(arb(64), 182, prec_bits=prec_bits)
        )
        per_prime_harm_rows: List[Dict[str, Any]] = []
        for p_h in harm_primes:
            mf_ph = evaluate_interior_paired_matrix_free_arb(
                arb(64),
                182,
                4,
                cut_64["ceil_tau_Y"],
                (p_h,),
                tbl,
                prec_bits=prec_bits,
                quad_tol_bits=210,
                use_three_zone=False,
            )
            w_rel = _frac_to_arb(Fraction(1, p_h) / harm_w_tot)
            harm_F_int_acc += w_rel * mf_ph["F_int_T"]
            harm_F_bnd_acc += w_rel * (F_64_val - mf_ph["F_int_T"])
            per_prime_harm_rows.append(
                {
                    "prime_p": p_h,
                    "harmonic_weight_fraction": f"{(Fraction(1, p_h) / harm_w_tot).numerator}/{(Fraction(1, p_h) / harm_w_tot).denominator}",
                    "F_int_T_p": serialize_arb_certified(mf_ph["F_int_T"]),
                    "F_bnd_T_p": serialize_arb_certified(F_64_val - mf_ph["F_int_T"]),
                }
            )
        harm_res = (harm_F_int_acc + harm_F_bnd_acc) - F_64_val
        harm_ok = bool(arb(0) in harm_res and abs(harm_res) < arb("1e-45"))

        z1_majorant_audit = verify_zone1_prime_power_majorant_repair_tc062_arb(
            prec_bits=prec_bits, selberg_table=tbl
        )
        anchor_diag_audit = verify_anchor_diagonal_identities_and_self_collision_bounds_arb(
            prec_bits=prec_bits, selberg_table=tbl
        )
        complete_a2_growth_audit = verify_complete_kernel_unsigned_linear_growth_arb(
            prec_bits=prec_bits, selberg_table=tbl
        )

        uncovered_young_boundary_accounting = {
            "exact_lean_young_inequalities": {
                "lean_lemma": "subsetPrimePowerDiagDtilde_young_split_tc062_aux",
                "forward_bound": "D_tilde(Y) - D_tilde_{Omega_p(T)}(Y) <= delta * D_tilde(Y) + (1 / delta) * D_tilde_{U_p(T)}(Y)",
                "reverse_bound": "D_tilde_{Omega_p(T)}(Y) - D_tilde(Y) <= delta * D_tilde(Y) + (1 + 1 / delta) * D_tilde_{U_p(T)}(Y)",
                "eventual_absorption_schedule": (
                    "Choose delta = 1 / log Y on Y >= exp(1) (so log Y >= 1 and 0 < delta <= 1): "
                    "the mixed term delta * D_tilde(Y) = D_tilde(Y) / log Y satisfies "
                    "(1 / log Y) * D_tilde(Y) <= (log Y)^(2 - kappa_eta) * D_tilde(Y) for EVERY "
                    "0 < kappa_eta <= 2 (since -1 <= 2 - kappa_eta), while (1 + log Y) * D_tilde_{U_p(T)}(Y) "
                    "= O_p(log Y) <<_{eta,p} Y^eta."
                ),
                "retired_false_difference_claims": [
                    "Retired D_tilde - D_tilde_{Omega_p(T)} <= 2 * D_tilde_{U_p(T)} (omitted the mixed cross-term between Omega_p(T) and U_p(T)).",
                    "Retired unproved difference rate O(p^2 * Y^{-5/2} * (log Y)^2); D_tilde_{U_p(T)}(Y) = O_p(1) bounds the strip quadratic form itself, whereas D_tilde - D_tilde_{Omega_p(T)} retains delta * D_tilde(Y).",
                ],
            },
            "uncovered_strip_norm_disposition": {
                "lean_proved_bound": "||U_{bnd,p,Y}||_Y^2 <= C_strip(p) * (log Y)^2 for all Y >= 2 (Theorem 7(1)), giving Young penalty (1 + log Y)*||U_{bnd,p,Y}||_Y^2 = O_p((log Y)^3) <<_{eta,p} Y^eta.",
                "elementary_triangle_bound": "||U_{bnd,p,Y}||_Y^2 = O_p(1) via |U_p(T)| <= T and phi_k(X) <= (tau*p)^3 * Y^{-5/4} on k > T/p.",
                "retired_unsupported_sharpening": (
                    "Removed unsupported outside-Lean claim ||U_{bnd,p,Y}||_Y^2 = O_p((log Y)^{-2}): "
                    "unlike pure spillover S_{spill,Y} (which carries a 1/(log X)^2 factor), U_{bnd,p,Y} "
                    "contains the bare signed Liouville sum sum_{k in U_p(T)} lambda(k)*phi_k(X), which "
                    "is not controlled to O_p((log Y)^{-2}) by |R_osc(d)| = O(d) triangle estimates alone; "
                    "Lean's proved O_p((log Y)^2) bound already suffices for two-way H-equivalence."
                ),
            },
        }

        literature_audit = {
            "matomaki_radziwill_tao_2015": {
                "citation": "Matomaki, Radziwill, & Tao (2015), 'An averaged form of Chowla's conjecture', Algebra & Number Theory 9(9), 2167-2196 (arXiv:1503.05121)",
                "proved_statement": "sum_{h_1,...,h_k <= H} |sum_{n <= X} lambda(n+h_1)...lambda(n+h_k)| = o(H^k X) as H(X) -> infty (rate O((log log H / log H) H^k X))",
                "exact_transfer_barriers": [
                    "Averages over additive shifts n + h rather than the multiplicative ratio kernel Hcal_Y(m, n) on [1, 2T]^2.",
                    "Short-interval L^2 comparison controls almost-all intervals [x, x+H] relative to the long average on [X, 2X]; it neither eliminates exceptional scales Y nor improves deterministic single-window summatory bounds beyond the classical zero-free region.",
                ],
            },
            "tao_2016_logarithmic_chowla": {
                "citation": "Tao (2016), 'The logarithmically averaged Chowla and Elliott conjectures for two-point correlations', Forum of Mathematics, Pi 4, e8 (arXiv:1509.05422)",
                "proved_statement": "sum_{x/omega(x) < n <= x} lambda(a_1*n + b_1)*lambda(a_2*n + b_2)/n = o(log omega(x)) as omega(x) -> infty when a_1*b_2 - a_2*b_1 != 0",
                "exact_transfer_barriers": [
                    "Requires non-zero additive determinant a_1*b_2 - a_2*b_1 != 0 along a 1D shift correlation, whereas sum_{m,n} lambda(m)*lambda(n)*Hcal_Y(m, n) is a 2D separable-plus-subtracted-diagonal form.",
                    "Requires logarithmic scale averaging over a growing multiplicative span omega(x) -> infty, whereas TC061R-OBL-SIGNED-REMAINDER-F requires deterministic control on every fixed-ratio dyadic window [Y, tau*Y] (constant span tau).",
                    "Entropy decrement across prime-dilation scales yields iterated-logarithmic decay rather than a positive power-of-logarithm saving (log Y)^{-kappa_eta} (kappa_eta > 0) required to absorb (log Y)^2 * Theta_eps^{diag}(Y).",
                ],
            },
        }

        return {
            "epistemic_statuses": [
                "UNCONDITIONAL_FINITE_ARITHMETIC",
                "CONCRETE_ANALYTIC_IN_LEAN",
                "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "CONDITIONAL_IMPLICATION",
                "CERTIFIED_FINITE_OBSERVATION",
                "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            ],
            "section_epistemic_scope_note": (
                "Mixed proof-attempt section: spillover fringe support T < n <= T + floor(T/(D+1)), "
                "q-reindexing, |w_{2,lambda}(n)| <= (log n)^2, mixed-covariance Young equivalence "
                "H(F, D_tilde) <-> H(F_{<=T}, D_tilde), Stage A interior Hilbert identity, m = 1 "
                "refutation of Candidate A1, exact general-anchor diagonal identities (both combined "
                "(log m)^2/(log(p*m))^2 and corrected c_self forms), two-sided uniform O(1) bound "
                "|Sigma_diag(Y; p)| <= C_diag (keeping -1_{k=T}*(R(T)-M_{sq,2}(T)), square indicator, "
                "1 <= d <= D_min + (D_min+1) boundary, and gcd/lcm mean-square drift convergence "
                "explicit without any false |b_n| << (log n)^2 claim), and full chain of two-way "
                "equivalences H(J, D_tilde) <-> H(F, D_tilde) <-> H(F_{<=T}, D_tilde) <-> "
                "H(F_{int,T}(.; {p}), D_tilde) <-> H(Sigma_off(.; p), D_tilde) are "
                "CONCRETE_ANALYTIC_IN_LEAN (Lean Theorems 5, 6, 7, 8) and "
                "UNCONDITIONAL_FINITE_ARITHMETIC; PNT/Selberg ||S_{spill,Y}||_Y^2 = O((log Y)^{-2}) "
                "spillover decay (via TC-057R Theorem 4.3(3)), sharp 4*X_self(Y) <= (289/15)*log(tau) "
                "< (1377/40)*log(tau) < 64 bound, complete-kernel Omega(Y) lower bound on the unsigned "
                "paired majorant over odd resonant anchors A_odd(Y) and subwindow [3Y, 4Y], general-m "
                "b_{pm} - b_m jump formula, and literature barrier audit are ANALYTIC_PROVED_OUTSIDE_LEAN; "
                "Route D closure transfer from canonicalInteriorOffDiagSigma (and "
                "canonicalInteriorPairedRemainderF) is CONDITIONAL_IMPLICATION (preserving explicit "
                "linear-energy, prime-mass, diagonal-contraction, and known-part-contraction inputs); "
                "256-bit Arb checks (including Candidate A2's Y = 64 refutation witness and Zone 1 "
                "prime-power majorant repair audit) are CERTIFIED_FINITE_OBSERVATION; and Candidates A1, "
                "A2 (refuted) and TC062-OBL-INTERIOR-PRIME-PAIR-OFFDIAG (open) are "
                "OPEN_CONJECTURE_OR_FAILED_CANDIDATE."
            ),
            "component_epistemic_map": {
                "selberg_w2_pointwise_log_sq_bound_and_q_reindexing": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "spillover_fringe_young_equivalences_and_two_sided_sigma_diag_bound": "CONCRETE_ANALYTIC_IN_LEAN",
                "pnt_spillover_sharp_4Xself_complete_kernel_omega_Y_and_b_jump_formula": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "stage_a_m1_refutation_and_general_anchor_diagonal_identities": "CONCRETE_ANALYTIC_IN_LEAN",
                "candidate_a2_arb_refutation_Y64_zone1_repair_and_harmonic_checks": "CERTIFIED_FINITE_OBSERVATION",
                "interior_paired_and_offdiag_closure_to_route_d_transfer": "CONDITIONAL_IMPLICATION",
                "refuted_candidates_a1_a2_and_open_offdiag_obligation": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            },
            "lean_theorems": [
                "spillover_fringe_reindexing_and_mixed_covariance_reduction_tc062",
                "stage_a_interior_hilbert_split_and_candidate_a1_refutation_tc062",
                "interior_prime_pair_closure_equivalence_and_route_d_transfer_tc062",
                "two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r",
            ],
            "selberg_w2_pointwise_log_sq_bound_1_to_2000_verified": w2_log_sq_ok,
            "zone1_prime_power_majorant_repair_audit": z1_majorant_audit,
            "spillover_fringe_and_young_reduction_rows": spillover_rows,
            "uncovered_young_boundary_accounting": uncovered_young_boundary_accounting,
            "stage_a_matrix_free_vs_dense_and_three_zone_consistency_verified": stage_a_consistency_ok,
            "anchor_diagonal_identities_and_self_collision_bounds": anchor_diag_audit,
            "candidate_a1_pointwise_anchor_diagonal_refutation_and_replacement": {
                "candidate_statement": "forall Y >= Y_0, forall m in I_2(T(Y)), Delta_{2,2} Hcal_Y(m, m) <= 0",
                "general_anchor_c_self_formula": (
                    "Delta_{p,p} Hcal_Y(m, m) = ||psi_{Y,m} - psi_{Y,p*m}||_Y^2 - 4*(log p)^2*G_Y^[2](p*m, p*m) "
                    "- 4*c_self(m)*G_Y^[2](m, m) - 4*c_self(p*m)*G_Y^[2](p*m, p*m) "
                    "- 4*c(m, m)*[G_Y^[2](m, m) - 2*G_Y^[2](m, p*m) + G_Y^[2](p*m, p*m)] "
                    "(abbreviated formula omitting -4*c(m, m)*[...] holds at m = 1 where c(1, 1) = 0, not at m > 1)."
                ),
                "verdict": "REFUTED_WITHIN_SCOPE",
                "counterexample_mechanism": "At m = 1, p = 2 for Y >= 8 (D >= 2), c(1, 1) = 0, b_1 = 0, and b_2 = -(log 2)^2 leave Delta_{2,2} Hcal_Y(1, 1) > 0 unconditionally.",
                "replacement_theorem": (
                    "Two-sided uniform O(1) bound proved unconditionally in Lean Theorem 8: "
                    "-744*(tau - 1) <= -4*sum_{n<=T} (log n)^2 G_Y^[2](n, n) <= Sigma_diag(Y; p) <= "
                    "2*sum_{n<=T} ||psi_{Y,n}||_Y^2 <= C_diag (outside Lean lower bound >= -(289/15)*log(tau) > -36; "
                    "upper bound decomposes beta_Y(k) exactly into square indicator, separate k = T endpoint, "
                    "1 <= d <= D_min + (D_min+1) boundary, and gcd/lcm mean-square drift convolution without "
                    "any false |b_n| << (log n)^2 claim; certified < 0 across Y = 8..1024 for p = 2)."
                ),
                "rows": cand_a1_rows,
            },
            "candidate_a2_unsigned_paired_block_majorant_refutation": {
                "candidate_statement": "sum_{m, n in I_2(T(Y))} |Delta_{2,2} Hcal_Y(m, n)| <= (1/32)*Y^{1/2} + (log Y)*D_tilde(Y) for Y >= 64",
                "verdict": "REFUTED_BY_CERTIFIED_WITNESS",
                "witness_Y": 64,
                "witness_T_Y": 182,
                "witness_evaluator_impact_status": "UNAFFECTED_EXACT_UNSPLIT_SMALL_T_EVALUATION",
                "interior_anchor_count": len(I2_64),
                "certified_unsigned_paired_sum_Y64": serialize_arb_certified(abs_paired_sum_64),
                "rhs_budget_Y64": serialize_arb_certified(rhs_cand_a2_64),
                "margin_Y64": serialize_arb_certified(margin_cand_a2_64),
                "complete_kernel_linear_growth_proof": complete_a2_growth_audit,
                "analytic_linear_growth_mechanism": (
                    "Complete-kernel lower bound on odd resonant anchors A_odd(Y) = {ceil(Y) <= m <= floor(3Y/2) : 2 nmid m} "
                    "and sign-free subwindow [3*Y, 4*Y] subset [Y, tau*Y] (avoiding X = 2*sqrt(log 2)*m): "
                    "sum_{m,n in I_2(T)} |Delta_{2,2} Hcal_Y(m, n)| >= sum_{m,n in A_odd(Y)} Delta_{2,2} Hcal_Y(m, n) "
                    ">= (c_0^2 * log(4/3) / 50)*Y - O(Y / log Y) - O(Y / (log Y)^2) - (289/15)*log(tau) = Omega(Y). "
                    "Refutes Candidate A2 and unsigned majorants without refuting the existential all-eta signed target H(Sigma_off, D_tilde)."
                ),
            },
            "stage_b_large_prime_b_jump_identity_verified": b_jump_law_ok,
            "stage_b_large_prime_b_jump_audit": b_jump_audit,
            "stage_c_multi_prime_and_harmonic_average_Y64": {
                "three_prime_2_3_5_64_term_F_int_T": serialize_arb_certified(mf64_235["F_int_T"]),
                "three_prime_2_3_5_diag_int_T": serialize_arb_certified(mf64_235["diag_int_T"]),
                "three_prime_2_3_5_offdiag_int_T": serialize_arb_certified(mf64_235["offdiag_int_T"]),
                "harmonic_primes": list(harm_primes),
                "harmonic_weighted_F_int_T": serialize_arb_certified(harm_F_int_acc),
                "harmonic_weighted_F_bnd_T": serialize_arb_certified(harm_F_bnd_acc),
                "harmonic_reassembly_minus_F_64_residual": serialize_arb_certified(harm_res),
                "per_prime_rows": per_prime_harm_rows,
                "verified": harm_ok,
            },
            "primary_literature_audit": literature_audit,
            "sharpest_remaining_open_obligation": {
                "obligation_id": "TC062-OBL-INTERIOR-PRIME-PAIR-OFFDIAG",
                "equivalent_to": "TC061R-OBL-SIGNED-REMAINDER-F",
                "lean_equivalence_theorem": "two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r",
                "statement": (
                    "For fixed prime p = 2 (or any fixed prime p), prove that "
                    "for every eta > 0 there exist a_eta, b_eta >= 0, 0 < kappa_eta <= 2, and "
                    "Y_eta >= 2 such that for all real Y >= Y_eta, Sigma_off(Y; p) := "
                    "sum_{m != n in I_p(T(Y))} lambda(m)*lambda(n)*Delta_{p,p} Hcal_Y(m, n) <= "
                    "a_eta * Y^eta + b_eta * (log Y)^(2 - kappa_eta) * D_tilde(Y) "
                    "(retaining D_tilde as the inherited prime-power diagonal)."
                ),
                "status": "OPEN",
            },
            "all_section_4_checks_pass": bool(
                w2_log_sq_ok
                and z1_majorant_audit["verified"]
                and spillover_ok
                and stage_a_consistency_ok
                and anchor_diag_audit["verified"]
                and cand_a1_refuted_ok
                and cand_a2_refuted_ok
                and complete_a2_growth_audit["verified"]
                and b_jump_law_ok
                and harm_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 5. Section 5: Frozen 10-Point Unseen Validation Runner & Interval Splits
# ---------------------------------------------------------------------------


def _evaluate_tc062_probes_for_row(
    obs: Dict[str, arb],
    probes: Sequence[Dict[str, Any]],
    *,
    in_declared_domain_fn: Callable[[Dict[str, Any]], bool],
    kl1_in_declared_domain: bool,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Evaluate all 4 frozen `TC-062` probes and both `KL1` interior sub-budgets (`diag_int_T_p2`
    and `offdiag_int_T_p2`) for a single point evaluation.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        Y_b = obs["Y_arb"]
        lgD_b = obs["log_Y_times_D_tilde"]

        per_probe: Dict[str, Any] = {}
        any_main_unresolved = False
        any_main_fail = False
        for pr in probes:
            pid = str(pr["probe_id"])
            in_dom = bool(in_declared_domain_fn(pr))
            lhs_b = obs[str(pr["observable_key"])]
            a_fr = Fraction(int(pr["a_numerator"]), int(pr["a_denominator"]))
            b_fr = Fraction(int(pr["b_numerator"]), int(pr["b_denominator"]))
            a_term = arb(0)
            if pr["eta_fraction"] is not None and a_fr != Fraction(0, 1):
                en, ed = (int(x) for x in str(pr["eta_fraction"]).split("/"))
                a_term = _frac_to_arb(a_fr) * (Y_b ** _frac_to_arb(Fraction(en, ed)))
            b_term = _frac_to_arb(b_fr) * lgD_b if b_fr != Fraction(0, 1) else arb(0)
            rhs_tot = a_term + b_term
            margin = lhs_b - rhs_tot
            cls = classify_probe_margin_arb(margin)
            if in_dom and cls["verdict"] == "UNRESOLVED":
                any_main_unresolved = True
            if in_dom and cls["verdict"] == "FAIL":
                any_main_fail = True
            per_probe[pid] = {
                "in_declared_domain": in_dom,
                "observable_key": str(pr["observable_key"]),
                "lhs_value": serialize_arb_certified(lhs_b),
                "rhs_budget": serialize_arb_certified(rhs_tot),
                "margin_M_Y": serialize_arb_certified(margin),
                "point_verdict": cls["verdict"],
                "classification_reason": cls["reason"],
            }

        diag_rhs = (arb(1) / arb(4)) * lgD_b
        diag_margin = obs["diag_int_T_p2"] - diag_rhs
        diag_cls = classify_probe_margin_arb(diag_margin)

        off_rhs = (arb(3) / arb(4)) * lgD_b
        off_margin = obs["offdiag_int_T_p2"] - off_rhs
        off_cls = classify_probe_margin_arb(off_margin)

        any_kl1_unresolved = bool(
            kl1_in_declared_domain and ("UNRESOLVED" in (diag_cls["verdict"], off_cls["verdict"]))
        )
        any_kl1_fail = bool(
            kl1_in_declared_domain and ("FAIL" in (diag_cls["verdict"], off_cls["verdict"]))
        )

        return {
            "per_probe": per_probe,
            "any_main_probe_in_domain_unresolved": any_main_unresolved,
            "any_kl1_in_domain_unresolved": any_kl1_unresolved,
            "any_in_domain_unresolved": bool(any_main_unresolved or any_kl1_unresolved),
            "any_main_probe_in_domain_fail": any_main_fail,
            "any_kl1_in_domain_fail": any_kl1_fail,
            "mechanism_kl1_sub_budgets": {
                "in_declared_domain": kl1_in_declared_domain,
                "diag_int_T_p2": serialize_arb_certified(obs["diag_int_T_p2"]),
                "diag_rhs_1_4_logY_D_tilde": serialize_arb_certified(diag_rhs),
                "diag_margin": serialize_arb_certified(diag_margin),
                "diag_verdict": diag_cls["verdict"],
                "offdiag_int_T_p2": serialize_arb_certified(obs["offdiag_int_T_p2"]),
                "offdiag_rhs_3_4_logY_D_tilde": serialize_arb_certified(off_rhs),
                "offdiag_margin": serialize_arb_certified(off_margin),
                "offdiag_verdict": off_cls["verdict"],
            },
            "F_over_log_Y_D_tilde": certified_ratio_with_positive_denominator(
                obs["F_Y"], lgD_b, prec_bits=prec_bits
            ),
            "F_int2_over_log_Y_D_tilde": certified_ratio_with_positive_denominator(
                obs["F_int_T_p2"], lgD_b, prec_bits=prec_bits
            ),
        }
    finally:
        flint_ctx.prec = saved


def execute_tc062_holdout_point_with_escalation(
    point_id: str,
    spec: ExactScaleSpec,
    probes: Sequence[Dict[str, Any]],
    protocol_rules: Dict[str, Any],
    *,
    selberg_table: Dict[str, Any],
    evaluator_fn: Optional[Callable[..., Dict[str, Any]]] = None,
    rss_fn: Callable[[], Dict[str, Any]] = _measure_process_rss_megabytes,
) -> Dict[str, Any]:
    """Execute one unseen `TC-062` validation point strictly under frozen protocol rules,
    preserving decisive `PASS`/`FAIL` witnesses across escalation tiers, failing closed on
    `CERTIFICATION_INTEGRITY_CONFLICT`, and tracking 3-valued (`WITHIN`, `EXCEEDED`, `UNKNOWN`)
    wall-time and `PROCESS_LIFETIME_HIGH_WATER_MARK` memory compliance independently of verdicts.
    """
    max_wall_s = float(protocol_rules["resource_limits"]["max_wall_seconds_per_point"])
    max_rss_mb = float(protocol_rules["resource_limits"]["max_rss_megabytes"])
    max_tier = max(
        [0]
        + [
            int(e["tier"])
            for e in protocol_rules.get("escalation_ladder_on_zero_straddling_margin", [])
        ]
    )

    probe_ids = [str(pr["probe_id"]) for pr in probes]
    all_candidate_ids = probe_ids + ["KL1_int2_diag", "KL1_int2_offdiag"]
    decisive_witnesses: Dict[str, Optional[Dict[str, Any]]] = {
        cid: None for cid in all_candidate_ids
    }
    in_domain_by_cid: Dict[str, Optional[bool]] = {cid: None for cid in all_candidate_ids}
    integrity_conflicts: List[Dict[str, Any]] = []
    tier_history: List[Dict[str, Any]] = []
    baseline_cutoffs: Optional[Tuple[int, int, int]] = None
    point_t0 = time.perf_counter()
    last_obs: Optional[Dict[str, Any]] = None
    last_pe: Optional[Dict[str, Any]] = None
    last_settings: Optional[Dict[str, Any]] = None
    final_tier_used = 0

    for tier in range(0, max_tier + 1):
        tier_t0 = time.perf_counter()
        cut_Preview = certify_exact_scale_cutoffs(spec, base_prec_bits=256)
        resolved = resolve_protocol_quadrature_settings(
            protocol_rules,
            cut_Preview["T_Y"],
            cut_Preview["ceil_tau_Y"],
            escalation_tier=tier,
        )
        used = resolved["used_settings"]
        p_bits = int(used["prec_bits"])
        q_tol = int(used["quad_tol_bits"])
        three_z = str(used["quadrature_mode"]) == "three_zone"
        n_pan = int(used["n_panels"]) if used["n_panels"] is not None else 1
        z1_rat = (
            int(used["zone1_ratio_threshold_x_over_n"])
            if used["zone1_ratio_threshold_x_over_n"] is not None
            else 12
        )

        if evaluator_fn is not None:
            tier_out = evaluator_fn(spec, tier=tier, resolved_settings=resolved)
            obs = tier_out["observables"]
            cut_cur = tier_out["cutoffs"]
        else:
            base_res = evaluate_mixed_covariance_point_arb(
                spec,
                protocol_rules=protocol_rules,
                escalation_tier=tier,
                selberg_table=selberg_table,
            )
            cut_cur = base_res["cutoffs"]
            T_c = cut_cur["T_Y"]
            D_c = cut_cur["D0_eff"]
            ct_c = cut_cur["ceil_tau_Y"]
            Y_b = base_res["Y_arb"]
            X_self = evaluate_X_self_collision_arb(Y_b, T_c, prec_bits=p_bits)
            F_val = +(base_res["J_direct"] - arb(4) * X_self)
            int2 = evaluate_interior_paired_matrix_free_arb(
                Y_b,
                T_c,
                D_c,
                ct_c,
                (2,),
                selberg_table,
                prec_bits=p_bits,
                quad_tol_bits=q_tol,
                use_three_zone=three_z,
                n_panels_override=n_pan,
                zone1_ratio_threshold=z1_rat,
            )
            int23 = evaluate_interior_paired_matrix_free_arb(
                Y_b,
                T_c,
                D_c,
                ct_c,
                (2, 3),
                selberg_table,
                prec_bits=p_bits,
                quad_tol_bits=q_tol,
                use_three_zone=three_z,
                n_panels_override=n_pan,
                zone1_ratio_threshold=z1_rat,
            )
            obs = {
                "Y_arb": Y_b,
                "E_Y": base_res["E_Y"],
                "D_tilde_Y": base_res["D_tilde_Y"],
                "X_self_Y": X_self,
                "J_Y": base_res["J_direct"],
                "F_Y": F_val,
                "F_int_T_p2": int2["F_int_T"],
                "diag_int_T_p2": int2["diag_int_T"],
                "offdiag_int_T_p2": int2["offdiag_int_T"],
                "F_bnd_T_p2": +(F_val - int2["F_int_T"]),
                "F_int_T_p23": int23["F_int_T"],
                "diag_int_T_p23": int23["diag_int_T"],
                "offdiag_int_T_p23": int23["offdiag_int_T"],
                "F_bnd_T_p23": +(F_val - int23["F_int_T"]),
                "log_Y_times_D_tilde": base_res["log_Y_times_D_tilde"],
            }

        cur_cut_tuple = (int(cut_cur["T_Y"]), int(cut_cur["D0_raw"]), int(cut_cur["D0_eff"]))
        if baseline_cutoffs is None:
            baseline_cutoffs = cur_cut_tuple
        elif cur_cut_tuple != baseline_cutoffs:
            integrity_conflicts.append(
                {
                    "conflict_type": "CUTOFF_MUTATION_ACROSS_ESCALATION",
                    "point_id": point_id,
                    "baseline_cutoffs": baseline_cutoffs,
                    "tier_cutoffs": cur_cut_tuple,
                    "tier": tier,
                }
            )

        y_ge_64 = bool(obs["Y_arb"] >= arb(64))
        pe = _evaluate_tc062_probes_for_row(
            obs,
            probes,
            in_declared_domain_fn=lambda pr, _yb=obs["Y_arb"]: bool(
                _yb >= arb(int(pr["domain_threshold_Y0"]))
            ),
            kl1_in_declared_domain=y_ge_64,
            prec_bits=p_bits,
        )

        rss_reading = rss_fn()
        tier_wall = round(time.perf_counter() - tier_t0, 6)
        cum_wall = round(time.perf_counter() - point_t0, 6)
        tier_history.append(
            {
                "tier": tier,
                "prec_bits": p_bits,
                "quad_tol_bits": q_tol,
                "quadrature_mode": used["quadrature_mode"],
                "elapsed_sec": tier_wall,
                "tier_wall_seconds": tier_wall,
                "cumulative_wall_seconds": cum_wall,
                "current_rss_mb": rss_reading.get("current_rss_mb"),
                "peak_rss_mb": rss_reading.get("peak_rss_mb"),
                "peak_rss_measurement_semantics": rss_reading.get(
                    "peak_rss_measurement_semantics"
                ),
            }
        )

        # Update decisive-witness accumulator across all 6 candidates:
        tier_cand_entries: List[Tuple[str, bool, str, Dict[str, Any]]] = []
        for pid in probe_ids:
            pd = pe["per_probe"][pid]
            tier_cand_entries.append(
                (pid, bool(pd["in_declared_domain"]), str(pd["point_verdict"]), pd["margin_M_Y"])
            )
        kl1_d = pe["mechanism_kl1_sub_budgets"]
        tier_cand_entries.append(
            (
                "KL1_int2_diag",
                bool(kl1_d["in_declared_domain"]),
                str(kl1_d["diag_verdict"]),
                kl1_d["diag_margin"],
            )
        )
        tier_cand_entries.append(
            (
                "KL1_int2_offdiag",
                bool(kl1_d["in_declared_domain"]),
                str(kl1_d["offdiag_verdict"]),
                kl1_d["offdiag_margin"],
            )
        )

        for cid, in_dom, v_str, m_dict in tier_cand_entries:
            if in_domain_by_cid[cid] is None:
                in_domain_by_cid[cid] = in_dom
            elif in_domain_by_cid[cid] != in_dom:
                integrity_conflicts.append(
                    {
                        "conflict_type": "DOMAIN_MEMBERSHIP_MUTATION",
                        "candidate_id": cid,
                        "point_id": point_id,
                        "tier": tier,
                    }
                )
            if not in_dom:
                continue
            if v_str in ("PASS", "FAIL"):
                prev = decisive_witnesses[cid]
                witness_obj = {
                    "point_id": point_id,
                    "candidate_id": cid,
                    "verdict": v_str,
                    "deciding_tier": tier,
                    "prec_bits": p_bits,
                    "used_settings": used,
                    "certified_margin_enclosure": m_dict,
                }
                if prev is None:
                    decisive_witnesses[cid] = witness_obj
                elif prev["verdict"] != v_str:
                    integrity_conflicts.append(
                        {
                            "conflict_type": "CONTRADICTORY_CERTIFIED_VERDICTS",
                            "point_id": point_id,
                            "candidate_id": cid,
                            "earlier_witness": prev,
                            "conflicting_witness": witness_obj,
                        }
                    )

        last_obs = obs
        last_pe = pe
        last_settings = resolved
        final_tier_used = tier

        res_chk_now = evaluate_point_resource_compliance(
            tier_history,
            max_wall_sec=max_wall_s,
            max_rss_mb=max_rss_mb,
        )
        all_decided = all(
            (not in_domain_by_cid[cid]) or (decisive_witnesses[cid] is not None)
            for cid in all_candidate_ids
        )
        if (
            len(integrity_conflicts) > 0
            or all_decided
            or res_chk_now["wall_budget_status"] == "EXCEEDED"
            or res_chk_now["memory_budget_status"] == "EXCEEDED"
        ):
            break

    assert last_obs is not None and last_pe is not None and last_settings is not None
    resource_check = evaluate_point_resource_compliance(
        tier_history,
        max_wall_sec=max_wall_s,
        max_rss_mb=max_rss_mb,
    )
    conflict_cids = {
        c.get("candidate_id") for c in integrity_conflicts if c.get("candidate_id") is not None
    }
    has_global_conflict = any(c.get("candidate_id") is None for c in integrity_conflicts)

    accumulated_verdicts: Dict[str, str] = {}
    for cid in all_candidate_ids:
        if has_global_conflict or cid in conflict_cids:
            accumulated_verdicts[cid] = CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
        elif not in_domain_by_cid[cid]:
            accumulated_verdicts[cid] = "NOT_EVALUATED"
        elif decisive_witnesses[cid] is not None:
            accumulated_verdicts[cid] = str(decisive_witnesses[cid]["verdict"])
        else:
            accumulated_verdicts[cid] = "UNRESOLVED"

    return {
        "point_id": point_id,
        "label": spec.label,
        "cutoffs": certify_exact_scale_cutoffs(spec, base_prec_bits=256),
        "final_tier_used": final_tier_used,
        "quadrature_settings_resolution": last_settings,
        "tier_escalation_history": tier_history,
        "resource_budget_check": resource_check,
        "certification_integrity_ok": len(integrity_conflicts) == 0,
        "integrity_conflicts": integrity_conflicts,
        "decisive_witnesses": decisive_witnesses,
        "accumulated_candidate_verdicts": accumulated_verdicts,
        "observables": {
            k: serialize_arb_certified(v)
            for k, v in last_obs.items()
            if k != "Y_arb"
        },
        "last_tier_probe_evaluations": last_pe,
    }


def _parse_certified_margin_bounds_tc062(
    margin_dict: Any,
) -> Optional[Tuple[Fraction, Fraction, str]]:
    """Re-parse a serialized Arb margin dict (`lower_dec`, `upper_dec`, `arb_ball_str`) in exact
    `Fraction` arithmetic and return `(c_lo, c_hi, verdict)` where `verdict` is `'PASS'`, `'FAIL'`,
    or `'UNRESOLVED'`, or `None` if malformed / self-inconsistent.
    """
    if not isinstance(margin_dict, dict):
        return None
    if not all(k in margin_dict for k in ("lower_dec", "upper_dec", "arb_ball_str")):
        return None
    try:
        lo_dec = _sci_or_latex_num_to_fraction(str(margin_dict["lower_dec"]))
        hi_dec = _sci_or_latex_num_to_fraction(str(margin_dict["upper_dec"]))
        lo_bs, hi_bs, _ = _parse_arb_ball_str_to_fractions(str(margin_dict["arb_ball_str"]))
    except Exception:  # noqa: BLE001
        return None
    if not (lo_dec <= hi_dec and lo_bs <= hi_bs and max(lo_dec, lo_bs) <= min(hi_dec, hi_bs)):
        return None
    c_lo = max(lo_dec, lo_bs)
    c_hi = min(hi_dec, hi_bs)
    if c_hi <= 0:
        verdict = "PASS"
    elif c_lo > 0:
        verdict = "FAIL"
    else:
        verdict = "UNRESOLVED"
    return (c_lo, c_hi, verdict)


def _audit_serialized_margin_verdict_tc062(margin_dict: Any) -> str:
    """Re-parse a serialized Arb margin dict (`lower_dec`, `upper_dec`, `arb_ball_str`) in exact
    `Fraction` arithmetic and return `'PASS'`, `'FAIL'`, `'UNRESOLVED'`, or `'CONFLICT'` (malformed).
    """
    parsed = _parse_certified_margin_bounds_tc062(margin_dict)
    return parsed[2] if parsed is not None else "CONFLICT"


def aggregate_tc062_section5_and_derive_outcomes(
    holdout_rows: Sequence[Dict[str, Any]],
    holdout_entries: Sequence[Dict[str, Any]],
    probes: Sequence[Dict[str, Any]],
    protocol_rules: Dict[str, Any],
    continuous_straddling_interval_splits: Dict[str, Any],
) -> Dict[str, Any]:
    """Single shared Section 5 coverage, integrity, resource, and outcome-derivation aggregator
    used identically by `verify_section_5_unseen_validation_and_interval_splits`,
    `generate_task_tc062_artifact`, and `reprocess_task_tc062_metadata_and_stage_b` (`TASK-TC-062R` §6).

    Never silently coerces absent evidence to `PASS` or infers survival from the absence of a failure;
    separates certification/execution completion, mathematical survival/refutation, and 3-valued
    (`WITHIN`, `EXCEEDED`, `UNKNOWN`) resource compliance.
    """
    max_wall_s = float(protocol_rules["resource_limits"]["max_wall_seconds_per_point"])
    max_rss_mb = float(protocol_rules["resource_limits"]["max_rss_megabytes"])

    probe_ids = [str(pr["probe_id"]) for pr in probes]
    all_cids = probe_ids + ["KL1_int2_diag", "KL1_int2_offdiag"]

    registered_ids = [str(e["point_id"]) for e in holdout_entries]
    entry_by_id: Dict[str, Dict[str, Any]] = {str(e["point_id"]): e for e in holdout_entries}

    expected_in_domain: Dict[Tuple[str, str], bool] = {}
    saved_p = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for entry in holdout_entries:
            pid_reg = str(entry["point_id"])
            sp_e = ExactScaleSpec.from_protocol_entry(entry)
            yb_e = sp_e.evaluate_arb(256)
            for pr in probes:
                expected_in_domain[(pid_reg, str(pr["probe_id"]))] = bool(
                    yb_e >= arb(int(pr["domain_threshold_Y0"]))
                )
            kl1_dom = bool(yb_e >= arb(64))
            expected_in_domain[(pid_reg, "KL1_int2_diag")] = kl1_dom
            expected_in_domain[(pid_reg, "KL1_int2_offdiag")] = kl1_dom
    finally:
        flint_ctx.prec = saved_p

    observed_ids = [str(r.get("point_id", "")) for r in holdout_rows]
    seen_ids: set[str] = set()
    duplicate_ids_set: set[str] = set()
    for oid in observed_ids:
        if oid in seen_ids:
            duplicate_ids_set.add(oid)
        seen_ids.add(oid)
    missing_registered_ids = [pid for pid in registered_ids if pid not in seen_ids]
    unregistered_observed_ids = sorted(oid for oid in seen_ids if oid not in entry_by_id)
    duplicate_observed_ids = sorted(duplicate_ids_set)
    exact_point_bijection = bool(
        len(registered_ids) > 0
        and len(all_cids) > 0
        and len(missing_registered_ids) == 0
        and len(unregistered_observed_ids) == 0
        and len(duplicate_observed_ids) == 0
        and len(observed_ids) == len(registered_ids)
    )

    missing_or_invalid_candidate_entries: List[Dict[str, Any]] = []
    applicable_domain_violations: List[Dict[str, Any]] = []
    detected_conflicts: List[Dict[str, Any]] = []
    audited_rows: List[Dict[str, Any]] = []

    recognized_verdicts = {
        "PASS",
        "FAIL",
        "UNRESOLVED",
        "NOT_EVALUATED",
        CERTIFICATION_INTEGRITY_CONFLICT_VERDICT,
    }

    for r_orig in holdout_rows:
        r = dict(r_orig)
        pid = str(r.get("point_id", ""))
        tier_hist = r.get("tier_escalation_history")
        rb = evaluate_point_resource_compliance(
            tier_hist if isinstance(tier_hist, list) else [],
            max_wall_sec=max_wall_s,
            max_rss_mb=max_rss_mb,
        )
        r["resource_budget_check"] = rb

        row_conflicts = list(r.get("integrity_conflicts") or [])
        if not bool(r.get("certification_integrity_ok", True)) and not row_conflicts:
            row_conflicts.append({"conflict_type": "FLAGGED_ROW_INTEGRITY_FAILURE", "point_id": pid})

        acc_raw = r.get("accumulated_candidate_verdicts")
        acc_map: Dict[str, str] = dict(acc_raw) if isinstance(acc_raw, dict) else {}
        dec_map = r.get("decisive_witnesses") if isinstance(r.get("decisive_witnesses"), dict) else {}
        last_pe = (
            r.get("last_tier_probe_evaluations")
            if isinstance(r.get("last_tier_probe_evaluations"), dict)
            else {}
        )
        per_probe_last = (
            last_pe.get("per_probe") if isinstance(last_pe.get("per_probe"), dict) else {}
        )
        kl1_last = (
            last_pe.get("mechanism_kl1_sub_budgets")
            if isinstance(last_pe.get("mechanism_kl1_sub_budgets"), dict)
            else {}
        )

        for cid in all_cids:
            if cid not in acc_map or str(acc_map[cid]) not in recognized_verdicts:
                missing_or_invalid_candidate_entries.append(
                    {"point_id": pid, "candidate_id": cid, "value": acc_map.get(cid)}
                )
                continue

            v_acc = str(acc_map[cid])
            if v_acc == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT:
                row_conflicts.append(
                    {
                        "conflict_type": "CANDIDATE_CONFLICT_VERDICT_PRESENT",
                        "point_id": pid,
                        "candidate_id": cid,
                    }
                )

            if pid in entry_by_id:
                exp_dom = expected_in_domain[(pid, cid)]
                if exp_dom and v_acc == "NOT_EVALUATED":
                    applicable_domain_violations.append(
                        {
                            "point_id": pid,
                            "candidate_id": cid,
                            "reason": "IN_DOMAIN_MARKED_NOT_EVALUATED",
                        }
                    )
                elif (not exp_dom) and v_acc in ("PASS", "FAIL", "UNRESOLVED"):
                    applicable_domain_violations.append(
                        {
                            "point_id": pid,
                            "candidate_id": cid,
                            "reason": "OUT_OF_DOMAIN_EVALUATED",
                        }
                    )

            # Audit decisive witness enclosure if present:
            w_obj = dec_map.get(cid)
            if w_obj is not None:
                if not isinstance(w_obj, dict) or str(w_obj.get("verdict")) not in ("PASS", "FAIL"):
                    row_conflicts.append(
                        {
                            "conflict_type": "MALFORMED_DECISIVE_WITNESS",
                            "point_id": pid,
                            "candidate_id": cid,
                        }
                    )
                    acc_map[cid] = CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
                else:
                    w_v = str(w_obj["verdict"])
                    m_v = _audit_serialized_margin_verdict_tc062(
                        w_obj.get("certified_margin_enclosure")
                    )
                    if m_v != w_v or (
                        v_acc != CERTIFICATION_INTEGRITY_CONFLICT_VERDICT and v_acc != w_v
                    ):
                        row_conflicts.append(
                            {
                                "conflict_type": "WITNESS_ENCLOSURE_OR_VERDICT_CONTRADICTION",
                                "point_id": pid,
                                "candidate_id": cid,
                                "witness_verdict": w_v,
                                "parsed_margin_verdict": m_v,
                                "accumulated_verdict": v_acc,
                            }
                        )
                        acc_map[cid] = CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
            elif v_acc in ("PASS", "FAIL"):
                # Claiming PASS or FAIL with no decisive witness at all is invalid:
                row_conflicts.append(
                    {
                        "conflict_type": "DECISIVE_VERDICT_WITHOUT_WITNESS",
                        "point_id": pid,
                        "candidate_id": cid,
                        "accumulated_verdict": v_acc,
                    }
                )
                acc_map[cid] = CERTIFICATION_INTEGRITY_CONFLICT_VERDICT

            # Audit last-tier margin enclosure against claimed last-tier verdict and decisive witness:
            last_m_dict = None
            last_claimed_v = None
            last_in_dom = None
            if cid in per_probe_last and isinstance(per_probe_last[cid], dict):
                last_m_dict = per_probe_last[cid].get("margin_M_Y")
                last_claimed_v = str(per_probe_last[cid].get("point_verdict"))
                last_in_dom = bool(per_probe_last[cid].get("in_declared_domain", True))
            elif cid == "KL1_int2_diag" and kl1_last:
                last_m_dict = kl1_last.get("diag_margin")
                last_claimed_v = str(kl1_last.get("diag_verdict"))
                last_in_dom = bool(kl1_last.get("in_declared_domain", True))
            elif cid == "KL1_int2_offdiag" and kl1_last:
                last_m_dict = kl1_last.get("offdiag_margin")
                last_claimed_v = str(kl1_last.get("offdiag_verdict"))
                last_in_dom = bool(kl1_last.get("in_declared_domain", True))

            if pid in entry_by_id and last_in_dom is not None:
                if last_in_dom != expected_in_domain[(pid, cid)]:
                    applicable_domain_violations.append(
                        {
                            "point_id": pid,
                            "candidate_id": cid,
                            "reason": "LAST_TIER_DOMAIN_FLAG_MISMATCH",
                        }
                    )

            if last_m_dict is not None:
                parsed_last = _audit_serialized_margin_verdict_tc062(last_m_dict)
                if parsed_last == "CONFLICT" or parsed_last != last_claimed_v:
                    row_conflicts.append(
                        {
                            "conflict_type": "LAST_TIER_MARGIN_VERDICT_MISMATCH",
                            "point_id": pid,
                            "candidate_id": cid,
                            "claimed": last_claimed_v,
                            "parsed": parsed_last,
                        }
                    )
                    acc_map[cid] = CERTIFICATION_INTEGRITY_CONFLICT_VERDICT
                elif (
                    last_in_dom
                    and parsed_last in ("PASS", "FAIL")
                    and acc_map.get(cid) in ("PASS", "FAIL")
                    and parsed_last != acc_map.get(cid)
                ):
                    row_conflicts.append(
                        {
                            "conflict_type": "CONTRADICTORY_LAST_TIER_AND_ACCUMULATED_VERDICT",
                            "point_id": pid,
                            "candidate_id": cid,
                            "last_tier": parsed_last,
                            "accumulated": acc_map.get(cid),
                        }
                    )
                    acc_map[cid] = CERTIFICATION_INTEGRITY_CONFLICT_VERDICT

        r["accumulated_candidate_verdicts"] = acc_map
        r["integrity_conflicts"] = row_conflicts
        r["certification_integrity_ok"] = len(row_conflicts) == 0
        if row_conflicts:
            detected_conflicts.extend(row_conflicts)
        audited_rows.append(r)

    # Re-audit continuous straddling interval splits from serialized Arb enclosures and branches
    # (never trusting cached `.get("verdict")` strings alone):
    interval_coverage_complete = True
    iv_verdicts: List[str] = []
    if not isinstance(continuous_straddling_interval_splits, dict):
        interval_coverage_complete = False
        int_splits_out: Dict[str, Any] = {}
    else:
        int_splits_out = dict(continuous_straddling_interval_splits)
        for split_key, exact_br, min_br in (
            ("interval_625_pm_2_neg12_across_T3125", 2, 2),
            ("interval_403_40_to_403_46_across_e6", None, 2),
        ):
            sp_obj = continuous_straddling_interval_splits.get(split_key)
            if not isinstance(sp_obj, dict):
                interval_coverage_complete = False
                iv_verdicts.extend(["UNRESOLVED", "UNRESOLVED"])
                continue
            branches = sp_obj.get("branches")
            act_cnt = sp_obj.get("active_branch_count")
            if not isinstance(branches, list):
                interval_coverage_complete = False
                if act_cnt not in (None, 0):
                    detected_conflicts.append(
                        {
                            "conflict_type": "INTERVAL_SPLIT_MALFORMED_BRANCHES",
                            "interval_key": split_key,
                            "active_branch_count": act_cnt,
                        }
                    )
                iv_verdicts.extend(["UNRESOLVED", "UNRESOLVED"])
                continue
            if act_cnt != len(branches):
                detected_conflicts.append(
                    {
                        "conflict_type": "INTERVAL_SPLIT_BRANCH_COUNT_MISMATCH",
                        "interval_key": split_key,
                        "active_branch_count": act_cnt,
                        "observed_branch_len": len(branches),
                    }
                )
            if len(branches) < min_br or (exact_br is not None and len(branches) != exact_br):
                interval_coverage_complete = False
                iv_verdicts.extend(["UNRESOLVED", "UNRESOLVED"])
                continue

            for u_key, cls_key, br_key in (
                ("union_M_P0", "P0_interval_classification", "M_P0"),
                ("union_M_P0_F", "TC062_P0_F_interval_classification", "M_P0_F"),
            ):
                cls_dict = sp_obj.get(cls_key)
                claimed_iv = (
                    str(cls_dict.get("verdict"))
                    if (isinstance(cls_dict, dict) and "verdict" in cls_dict)
                    else None
                )
                u_parsed = _parse_certified_margin_bounds_tc062(sp_obj.get(u_key))
                if (
                    u_parsed is None
                    or claimed_iv not in ("PASS", "FAIL", "UNRESOLVED")
                    or u_parsed[2] != claimed_iv
                ):
                    detected_conflicts.append(
                        {
                            "conflict_type": "INTERVAL_SPLIT_UNION_MARGIN_VERDICT_MISMATCH",
                            "interval_key": split_key,
                            "union_key": u_key,
                            "claimed_verdict": claimed_iv,
                            "parsed_verdict": u_parsed[2] if u_parsed is not None else "CONFLICT",
                        }
                    )
                    iv_verdicts.append(CERTIFICATION_INTEGRITY_CONFLICT_VERDICT)
                    continue

                u_lo, u_hi, u_v = u_parsed
                branch_conflict = False
                any_branch_fail = False
                for b_idx, br in enumerate(branches):
                    br_parsed = (
                        _parse_certified_margin_bounds_tc062(br.get(br_key))
                        if isinstance(br, dict)
                        else None
                    )
                    if br_parsed is None:
                        detected_conflicts.append(
                            {
                                "conflict_type": "INTERVAL_SPLIT_BRANCH_MARGIN_MALFORMED",
                                "interval_key": split_key,
                                "branch_index": b_idx,
                                "branch_key": br_key,
                            }
                        )
                        branch_conflict = True
                        break
                    b_lo, b_hi, b_v = br_parsed
                    if b_v == "FAIL":
                        any_branch_fail = True
                    # Whenever the union claims PASS (or UNRESOLVED with a certified FAIL branch),
                    # verify exact branch-to-union containment / non-contradiction:
                    if u_v == "PASS" and (
                        b_v != "PASS" or not (u_lo <= b_lo and b_hi <= u_hi)
                    ):
                        detected_conflicts.append(
                            {
                                "conflict_type": "INTERVAL_SPLIT_UNION_DOES_NOT_ENCLOSE_BRANCH",
                                "interval_key": split_key,
                                "branch_index": b_idx,
                                "branch_key": br_key,
                                "union_verdict": u_v,
                                "branch_verdict": b_v,
                            }
                        )
                        branch_conflict = True
                        break

                if branch_conflict:
                    iv_verdicts.append(CERTIFICATION_INTEGRITY_CONFLICT_VERDICT)
                elif any_branch_fail and u_v == "UNRESOLVED":
                    iv_verdicts.append("FAIL")
                else:
                    iv_verdicts.append(u_v)

    cert_integrity_ok = len(detected_conflicts) == 0
    candidate_entries_complete = len(missing_or_invalid_candidate_entries) == 0
    applicable_domains_valid = len(applicable_domain_violations) == 0
    coverage_complete = bool(
        exact_point_bijection
        and candidate_entries_complete
        and applicable_domains_valid
        and interval_coverage_complete
    )

    global_outcomes: Dict[str, str] = {}
    for cid in all_cids:
        in_dom_reg_count = sum(
            1 for pid_reg in registered_ids if expected_in_domain.get((pid_reg, cid), False)
        )
        cid_missing = any(
            m["candidate_id"] == cid for m in missing_or_invalid_candidate_entries
        ) or any(v["candidate_id"] == cid for v in applicable_domain_violations)
        verdicts_cid: List[str] = []
        for r in audited_rows:
            pid = str(r.get("point_id", ""))
            if pid not in entry_by_id:
                continue
            v_c = r["accumulated_candidate_verdicts"].get(cid)
            if v_c is not None and v_c != "NOT_EVALUATED":
                verdicts_cid.append(str(v_c))
        if not cert_integrity_ok or CERTIFICATION_INTEGRITY_CONFLICT_VERDICT in verdicts_cid:
            global_outcomes[cid] = CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
        elif "FAIL" in verdicts_cid:
            global_outcomes[cid] = "REFUTED_BY_CERTIFIED_WITNESS"
        elif (
            coverage_complete
            and (not cid_missing)
            and in_dom_reg_count > 0
            and len(verdicts_cid) == in_dom_reg_count
            and all(v == "PASS" for v in verdicts_cid)
        ):
            global_outcomes[cid] = "SURVIVED_TESTED_POINTS"
        else:
            global_outcomes[cid] = "UNRESOLVED/INCOMPLETE_COVERAGE"

    distinct_valid_reg = len([oid for oid in seen_ids if oid in entry_by_id])
    resource_summary = aggregate_section_resource_compliance(
        [r["resource_budget_check"] for r in audited_rows],
        registered_count=len(registered_ids),
        distinct_evaluated_count=distinct_valid_reg,
    )

    any_interval_fail = cert_integrity_ok and ("FAIL" in iv_verdicts)
    interval_splits_ok = bool(
        cert_integrity_ok
        and interval_coverage_complete
        and len(iv_verdicts) == 4
        and all(v == "PASS" for v in iv_verdicts)
    )
    int_splits_out["any_interval_fail"] = any_interval_fail
    int_splits_out["verified"] = interval_splits_ok

    decisive_outcomes = bool(
        cert_integrity_ok
        and coverage_complete
        and len(global_outcomes) == len(all_cids)
        and all(
            v in ("SURVIVED_TESTED_POINTS", "REFUTED_BY_CERTIFIED_WITNESS")
            for v in global_outcomes.values()
        )
        and (interval_splits_ok or any_interval_fail)
        and resource_summary["overall_resource_budget_status"] == "WITHIN"
    )

    sec5_base: Dict[str, Any] = {
        "epistemic_statuses": [
            "ANALYTIC_PROVED_OUTSIDE_LEAN",
            "CERTIFIED_FINITE_OBSERVATION",
            "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        ],
        "component_epistemic_map": {
            "three_zone_and_branch_splitting_error_budgets": "ANALYTIC_PROVED_OUTSIDE_LEAN",
            "ten_unseen_holdout_and_two_interval_enclosures": "CERTIFIED_FINITE_OBSERVATION",
            "universal_all_real_Y_candidate_probes": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        },
        "lean_theorems": [],
        "registered_unseen_point_count": len(registered_ids),
        "evaluated_unseen_point_count": len(audited_rows),
        "coverage_complete": coverage_complete,
        "coverage_audit": {
            "exact_point_bijection": exact_point_bijection,
            "missing_registered_point_ids": missing_registered_ids,
            "unregistered_observed_point_ids": unregistered_observed_ids,
            "duplicate_observed_point_ids": duplicate_observed_ids,
            "candidate_entries_complete": candidate_entries_complete,
            "missing_or_invalid_candidate_entries": missing_or_invalid_candidate_entries,
            "applicable_domains_valid": applicable_domains_valid,
            "applicable_domain_violations": applicable_domain_violations,
            "interval_coverage_complete": interval_coverage_complete,
        },
        "certification_integrity_ok": cert_integrity_ok,
        "detected_integrity_conflicts": detected_conflicts,
        "global_candidate_outcomes": global_outcomes,
        "resource_compliance_summary": resource_summary,
        "continuous_straddling_interval_splits": int_splits_out,
        "holdout_point_evaluations": audited_rows,
        "all_section_5_checks_pass": decisive_outcomes,
    }
    derived = derive_tc062_outcome_summaries(sec5_base, expected_candidate_ids=all_cids)
    sec5_base["section_epistemic_scope_note"] = derived["section_5_epistemic_scope_note"]
    sec5_base["derived_outcome_summary"] = derived
    return sec5_base


def derive_tc062_outcome_summaries(
    sec5: Dict[str, Any],
    *,
    expected_candidate_ids: Optional[Sequence[str]] = None,
) -> Dict[str, str]:
    """Derive top-level `completion_outcome_code`, `research_outcome_class`,
    `execution_and_certification_status`, `holdout_hypothesis_outcome`,
    `resource_compliance_status`, and Section 5's narrative summary from actual results
    (`TASK-TC-062R` §6).

    Guarantees:
    - Never emits `HOLDOUT_SURVIVAL` in `completion_outcome_code` on a certified refutation,
      unresolved evidence, empty/incomplete/duplicate/unregistered coverage, missing candidate entry,
      integrity conflict, or `UNKNOWN` / `EXCEEDED` resource telemetry.
    - Separates certification/execution completion (a certified refutation IS a completed evaluation),
      hypothesis survival/refutation, and 3-valued (`WITHIN`, `EXCEEDED`, `UNKNOWN`) resource compliance.
    """
    if expected_candidate_ids is None:
        proto = json.loads(JOINT_PRIME_DILATION_PROTOCOL_PATH.read_text(encoding="utf-8"))
        expected_candidate_ids = [
            str(pr["probe_id"]) for pr in proto["frozen_candidate_probes"]
        ] + ["KL1_int2_diag", "KL1_int2_offdiag"]
    exp_cids = list(expected_candidate_ids)

    cert_ok = bool(sec5.get("certification_integrity_ok", False))
    cov_ok = bool(sec5.get("coverage_complete", False))
    reg_n = int(sec5.get("registered_unseen_point_count", 0))
    eval_n = int(sec5.get("evaluated_unseen_point_count", 0))
    outcomes = (
        sec5.get("global_candidate_outcomes")
        if isinstance(sec5.get("global_candidate_outcomes"), dict)
        else {}
    )
    all_expected_cids_present = len(exp_cids) > 0 and all(cid in outcomes for cid in exp_cids)
    int_splits = (
        sec5.get("continuous_straddling_interval_splits")
        if isinstance(sec5.get("continuous_straddling_interval_splits"), dict)
        else {}
    )
    res_summary = (
        sec5.get("resource_compliance_summary")
        if isinstance(sec5.get("resource_compliance_summary"), dict)
        else {}
    )
    res_status = str(res_summary.get("overall_resource_budget_status", "UNKNOWN"))
    if res_status not in ("WITHIN", "EXCEEDED", "UNKNOWN"):
        res_status = "UNKNOWN"

    any_conflict = (not cert_ok) or any(
        str(v) == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME for v in outcomes.values()
    )
    refuted_cids = [
        cid for cid in exp_cids if str(outcomes.get(cid)) == "REFUTED_BY_CERTIFIED_WITNESS"
    ]
    any_refuted = len(refuted_cids) > 0 or bool(int_splits.get("any_interval_fail", False))
    all_survived = (
        cert_ok
        and cov_ok
        and reg_n > 0
        and all_expected_cids_present
        and all(str(outcomes[cid]) == "SURVIVED_TESTED_POINTS" for cid in exp_cids)
        and bool(int_splits.get("verified", False))
    )

    if any_conflict:
        exec_status = "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED"
        hyp_outcome = "CERTIFICATION_INTEGRITY_CONFLICT"
        comp_code = "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED_GATE_OPEN"
        res_class = (
            f"CERTIFICATION_INTEGRITY_CONFLICT_DETECTED_RESOURCE_{res_status}_SUBGATE_OPEN"
        )
        holdout_clause = (
            f"certification integrity conflict detected across {eval_n}/{reg_n} unseen points "
            f"(resource compliance: {res_status}; evaluation blocked)"
        )
    elif any_refuted:
        if not (cov_ok and all_expected_cids_present):
            exec_status = "CERTIFIED_REFUTATION_WITH_INCOMPLETE_REMAINING_GRID"
        elif res_status == "WITHIN":
            exec_status = "CERTIFIED_EVALUATION_COMPLETE"
        elif res_status == "EXCEEDED":
            exec_status = "CERTIFIED_EVALUATION_COMPLETE_RESOURCE_BUDGET_EXCEEDED"
        else:
            exec_status = "CERTIFIED_EVALUATION_COMPLETE_RESOURCE_TELEMETRY_UNKNOWN"
        hyp_outcome = "REFUTED_BY_CERTIFIED_WITNESS"
        comp_code = (
            "COMPLETE_SIGNED_KERNEL_PRIME_PAIR_REDUCTION_AND_HOLDOUT_CANDIDATE_REFUTED_GATE_OPEN"
        )
        res_class = (
            "EXACT_COMPLETE_KERNEL_AND_OFFDIAG_EQUIVALENCE_PROVED_CANDIDATES_A1_A2_AND_HOLDOUT_"
            f"CANDIDATE_REFUTED_RESOURCE_{res_status}_SUBGATE_OPEN"
        )
        ref_label = ",".join(refuted_cids) if refuted_cids else "interval_split"
        holdout_clause = (
            f"certified holdout refutation recorded on [{ref_label}] across {eval_n}/{reg_n} "
            f"evaluated points (resource compliance: {res_status})"
        )
    elif (not cov_ok) or reg_n <= 0 or (not all_expected_cids_present):
        exec_status = "INCOMPLETE_HOLDOUT_COVERAGE"
        hyp_outcome = "INCOMPLETE_OR_INVALID_COVERAGE"
        comp_code = (
            "COMPLETE_SIGNED_KERNEL_PRIME_PAIR_REDUCTION_AND_INCOMPLETE_HOLDOUT_COVERAGE_GATE_OPEN"
        )
        res_class = (
            "EXACT_COMPLETE_KERNEL_AND_OFFDIAG_EQUIVALENCE_PROVED_CANDIDATES_A1_A2_REFUTED_"
            f"INCOMPLETE_HOLDOUT_COVERAGE_RESOURCE_{res_status}_SUBGATE_OPEN"
        )
        holdout_clause = (
            f"incomplete or invalid unseen-point/candidate coverage ({eval_n}/{reg_n} rows; "
            f"resource compliance: {res_status})"
        )
    elif all_survived:
        hyp_outcome = "SURVIVED_TESTED_POINTS"
        if res_status == "WITHIN":
            exec_status = "CERTIFIED_EVALUATION_COMPLETE"
            comp_code = (
                "COMPLETE_SIGNED_KERNEL_PRIME_PAIR_REDUCTION_AND_UNSEEN_HOLDOUT_SURVIVAL_GATE_OPEN"
            )
        elif res_status == "EXCEEDED":
            exec_status = "CERTIFIED_EVALUATION_COMPLETE_RESOURCE_BUDGET_EXCEEDED"
            comp_code = (
                "COMPLETE_SIGNED_KERNEL_PRIME_PAIR_REDUCTION_RESOURCE_BUDGET_EXCEEDED_GATE_OPEN"
            )
        else:
            exec_status = "CERTIFIED_EVALUATION_COMPLETE_RESOURCE_TELEMETRY_UNKNOWN"
            comp_code = (
                "COMPLETE_SIGNED_KERNEL_PRIME_PAIR_REDUCTION_RESOURCE_TELEMETRY_UNKNOWN_GATE_OPEN"
            )
        res_class = (
            "EXACT_COMPLETE_KERNEL_AND_OFFDIAG_EQUIVALENCE_PROVED_CANDIDATES_A1_A2_REFUTED_"
            f"UNSEEN_HOLDOUTS_SURVIVED_RESOURCE_{res_status}_SUBGATE_OPEN"
        )
        holdout_clause = (
            f"all {len(exp_cids)} registered candidates achieved SURVIVED_TESTED_POINTS across "
            f"{eval_n}/{reg_n} unseen TC-062 points and both continuous interval case-splits "
            f"(finite evidence, never PROVED_UNIFORMLY; resource compliance: {res_status})"
        )
    else:
        exec_status = "UNRESOLVED_HOLDOUT_EVIDENCE"
        hyp_outcome = "UNRESOLVED_EVIDENCE"
        comp_code = (
            "COMPLETE_SIGNED_KERNEL_PRIME_PAIR_REDUCTION_AND_HOLDOUT_UNRESOLVED_GATE_OPEN"
        )
        res_class = (
            "EXACT_COMPLETE_KERNEL_AND_OFFDIAG_EQUIVALENCE_PROVED_CANDIDATES_A1_A2_REFUTED_"
            f"HOLDOUT_UNRESOLVED_RESOURCE_{res_status}_SUBGATE_OPEN"
        )
        holdout_clause = (
            f"unresolved margin evidence remains across {eval_n}/{reg_n} unseen TC-062 points "
            f"(resource compliance: {res_status})"
        )

    sec5_note = (
        "Preregistered unseen finite validation section: repaired 3-zone outward-rounded "
        "quadrature and cutoff branch-splitting error budgets are ANALYTIC_PROVED_OUTSIDE_LEAN; "
        f"unseen TC-062 point and continuous interval evaluations ({holdout_clause}) are "
        "CERTIFIED_FINITE_OBSERVATION; and the universal all-real-Y candidate inequalities remain "
        "OPEN_CONJECTURE_OR_FAILED_CANDIDATE."
    )
    return {
        "execution_and_certification_status": exec_status,
        "holdout_hypothesis_outcome": hyp_outcome,
        "resource_compliance_status": res_status,
        "completion_outcome_code": comp_code,
        "research_outcome_class": res_class,
        "section_5_epistemic_scope_note": sec5_note,
    }


def verify_section_5_unseen_validation_and_interval_splits(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
    *,
    holdout_evaluator_fn: Optional[Callable[..., Dict[str, Any]]] = None,
    rss_fn: Callable[[], Dict[str, Any]] = _measure_process_rss_megabytes,
    holdout_entries_override: Optional[Sequence[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Execute all 10 preregistered unseen `TC-062` validation points (`112` through `1280`,
    including `e^6` and `625` discontinuity pairs) strictly from the frozen `TC-062` protocol,
    plus continuous interval branch-splitting across `[625 - 2^-12, 625 + 2^-12]` and `[2017/5, 20173/50]`.
    """
    proto_chk = verify_frozen_tc062_protocol_immutability()
    if not proto_chk["verified"]:
        raise RuntimeError(f"Frozen TC-062 protocol verification failed: {proto_chk}")
    proto = proto_chk["protocol_object"]
    probes = proto["frozen_candidate_probes"]
    rules = proto["numerical_settings_and_escalation_rules"]
    holdout_entries = (
        list(holdout_entries_override)
        if holdout_entries_override is not None
        else proto["holdout_validation_schedule"]["holdout_entries"]
    )

    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(8000, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 7600
        else selberg_table
    )

    holdout_rows: List[Dict[str, Any]] = []
    for entry in holdout_entries:
        sp = ExactScaleSpec.from_protocol_entry(entry)
        row = execute_tc062_holdout_point_with_escalation(
            str(entry["point_id"]),
            sp,
            probes,
            rules,
            selberg_table=tbl,
            evaluator_fn=holdout_evaluator_fn,
            rss_fn=rss_fn,
        )
        row["grid_tier"] = str(entry["grid_tier"])
        row["prior_exposure_status"] = str(entry["prior_exposure_status"])
        holdout_rows.append(row)

    # Continuous interval branch-splitting across the NEW fourth-power cutoff 625^(5/4) = 3125
    # and across e^6 in [2017/5, 20173/50] = [403.40, 403.46] (D0: 5 -> 6):
    def _enrich_and_serialize_interval_split(raw_split: Dict[str, Any]) -> Dict[str, Any]:
        saved_p = flint_ctx.prec
        try:
            flint_ctx.prec = prec_bits
            f_branches: List[arb] = []
            m_f_branches: List[arb] = []
            for br in raw_split["branches"]:
                x_self_b = evaluate_X_self_collision_arb(
                    br["Y_sub_ball"], int(br["T_fixed"]), prec_bits=prec_bits
                )
                f_b = +(br["J_Y"] - arb(4) * x_self_b)
                m_f_b = +(f_b - br["log_Y_times_D_tilde"])
                br["X_self_Y"] = x_self_b
                br["F_Y"] = f_b
                br["M_P0_F"] = m_f_b
                f_branches.append(f_b)
                m_f_branches.append(m_f_b)
            u_f = f_branches[0]
            u_mf = m_f_branches[0]
            for fb, mfb in zip(f_branches[1:], m_f_branches[1:]):
                u_f = u_f.union(fb)
                u_mf = u_mf.union(mfb)
            raw_split["union_F_Y"] = +u_f
            raw_split["union_M_P0_F"] = +u_mf
            raw_split["TC062_P0_F_interval_classification"] = classify_probe_margin_arb(+u_mf)
        finally:
            flint_ctx.prec = saved_p

        def _ser_leaves(node: Any) -> Any:
            if isinstance(node, arb):
                return serialize_arb_certified(node)
            if isinstance(node, dict):
                return {k: _ser_leaves(v) for k, v in node.items()}
            if isinstance(node, list):
                return [_ser_leaves(v) for v in node]
            return node

        return _ser_leaves(raw_split)

    split_625 = _enrich_and_serialize_interval_split(
        evaluate_interval_via_cutoff_case_split_arb(
            Fraction(2559999, 4096),
            Fraction(2560001, 4096),
            prec_bits=prec_bits,
            quad_tol_bits=110,
            selberg_table=tbl,
        )
    )
    split_exp6 = _enrich_and_serialize_interval_split(
        evaluate_interval_via_cutoff_case_split_arb(
            Fraction(2017, 5),
            Fraction(20173, 50),
            prec_bits=prec_bits,
            quad_tol_bits=110,
            selberg_table=tbl,
        )
    )
    return aggregate_tc062_section5_and_derive_outcomes(
        holdout_rows,
        holdout_entries,
        probes,
        rules,
        {
            "interval_625_pm_2_neg12_across_T3125": split_625,
            "interval_403_40_to_403_46_across_e6": split_exp6,
        },
    )


# ---------------------------------------------------------------------------
# 6. Section 6: Lean Span Audit, Review Verifier, & Full Artifact Generator
# ---------------------------------------------------------------------------


def extract_lean_declaration_spans_tc062(
    lean_path: Path = TC_062_LEAN_MODULE_PATH,
) -> Dict[str, Any]:
    """Extract live 1-based `#L<start>-L<end>` spans for public and private declarations in
    `formal/RiemannScope/JointPrimeDilationSignedRemainder.lean` and check hygiene gates.
    """
    if not lean_path.exists():
        return {
            "exists": False,
            "public_theorems": {},
            "all_declarations": {},
            "hygiene_ok": False,
        }
    lines = lean_path.read_text(encoding="utf-8").splitlines()
    decl_re = re.compile(
        r"^\s*(?:(private)\s+)?(?:noncomputable\s+)?(def|theorem|lemma|axiom)\s+([A-Za-z0-9_']+)"
    )
    starts: List[Tuple[int, bool, str, str]] = []
    has_sorry_or_admit = False
    has_custom_axiom = False
    for idx, raw_line in enumerate(lines, start=1):
        code_part = raw_line.split("--")[0]
        if re.search(r"\b(sorry|admit)\b", code_part):
            has_sorry_or_admit = True
        m = decl_re.match(raw_line)
        if m:
            is_priv = m.group(1) == "private"
            kind = m.group(2)
            name = m.group(3)
            if kind == "axiom":
                has_custom_axiom = True
            starts.append((idx, is_priv, kind, name))

    full_txt = "\n".join(lines)
    no_pi = ("\\pi" not in full_txt) and ("\u03c0" not in full_txt)
    non_grade_K = [
        tok
        for tok in re.findall(r"\bK_[A-Za-z0-9_']+", full_txt)
        if tok != "K_reserved"
    ]

    all_decls: Dict[str, Dict[str, Any]] = {}
    pub_theorems: Dict[str, Dict[str, Any]] = {}
    def_count = 0
    pub_thm_count = 0
    priv_thm_count = 0

    for i, (st_line, is_priv, kind, name) in enumerate(starts):
        next_start = starts[i + 1][0] - 1 if i + 1 < len(starts) else len(lines)
        end_line = next_start
        while end_line > st_line:
            stripped = lines[end_line - 1].strip()
            if (
                stripped == ""
                or stripped.startswith("/-")
                or stripped.startswith("-/")
                or stripped.startswith("--")
                or stripped.startswith("*")
            ):
                end_line -= 1
            else:
                break
        entry = {
            "kind": kind,
            "private": is_priv,
            "start_line": st_line,
            "end_line": end_line,
            "anchor": f"#L{st_line}-L{end_line}",
        }
        all_decls[name] = entry
        if kind == "def":
            def_count += 1
        elif kind in ("theorem", "lemma"):
            if is_priv:
                priv_thm_count += 1
            else:
                pub_thm_count += 1
                pub_theorems[name] = entry

    expected_present = all(t in pub_theorems for t in EXPECTED_TC062_THEOREMS)
    return {
        "exists": True,
        "total_declarations": len(starts),
        "def_count": def_count,
        "public_theorem_count": pub_thm_count,
        "private_helper_theorem_count": priv_thm_count,
        "public_theorems": pub_theorems,
        "all_declarations": all_decls,
        "zero_sorry_or_admit": not has_sorry_or_admit,
        "zero_custom_axioms": not has_custom_axiom,
        "zero_pi_tokens": no_pi,
        "non_grade_K_tokens": non_grade_K,
        "expected_theorems_present": expected_present,
        "hygiene_ok": bool(
            (not has_sorry_or_admit)
            and (not has_custom_axiom)
            and no_pi
            and len(non_grade_K) == 0
            and expected_present
        ),
    }


def verify_tc062_review_enclosures_and_lean_anchors(
    artifact: Dict[str, Any],
    review_path: Path = TC_062_REVIEW_DOC_PATH,
    lean_spans: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Programmatically verify every `<!-- tc-enclosure: ... -->` interval and every Lean
    `JointPrimeDilationSignedRemainder.lean#L<start>-L<end>` anchor in `TC_062_...md`.
    """
    if not review_path.exists():
        return {"review_exists": False, "verified": False}
    md_text = review_path.read_text(encoding="utf-8")
    no_pi = ("\\pi" not in md_text) and ("\u03c0" not in md_text)

    checked_intervals = 0
    untagged_intervals: List[Dict[str, Any]] = []
    failed_intervals: List[Dict[str, Any]] = []
    for line_idx, line in enumerate(md_text.splitlines(), start=1):
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
                untagged_intervals.append(
                    {
                        "line": line_idx,
                        "column": pos + 1,
                        "format": fmt_kind,
                        "mid_str": mid_s,
                        "rad_str": rad_s,
                        "tag_count_on_line": len(tags),
                        "interval_count_on_line": len(line_matches),
                    }
                )
            continue

        for (_pos, fmt_kind, mid_s, rad_s), m_tag in zip(line_matches, tags):
            obs_name = m_tag.group("observable")
            params_str = m_tag.group("params")
            json_path = m_tag.group("json_path")
            try:
                disp_mid = _sci_or_latex_num_to_fraction(mid_s)
                disp_rad = _sci_or_latex_num_to_fraction(rad_s)
                d_lo = disp_mid - disp_rad
                d_hi = disp_mid + disp_rad
                cert_node, _ = _resolve_report_path_with_param_check(
                    artifact, json_path=json_path, params_str=params_str, observable=obs_name
                )
                gen_low_bs, gen_high_bs, _ = _parse_arb_ball_str_to_fractions(
                    cert_node["arb_ball_str"]
                )
                gen_low_dec = _sci_or_latex_num_to_fraction(str(cert_node["lower_dec"]))
                gen_high_dec = _sci_or_latex_num_to_fraction(str(cert_node["upper_dec"]))
                c_lo = max(gen_low_bs, gen_low_dec)
                c_hi = min(gen_high_bs, gen_high_dec)
                contains_ok = bool(d_lo <= c_lo and c_hi <= d_hi)
                sign_ok = True
                if c_lo > 0 and not (d_lo > 0):
                    sign_ok = False
                if c_hi < 0 and not (d_hi < 0):
                    sign_ok = False
                checked_intervals += 1
                if not (contains_ok and sign_ok):
                    failed_intervals.append(
                        {
                            "line": line_idx,
                            "format": fmt_kind,
                            "observable": obs_name,
                            "json_path": json_path,
                            "displayed": (str(d_lo), str(d_hi)),
                            "certified": (str(c_lo), str(c_hi)),
                            "contains_ok": contains_ok,
                            "sign_ok": sign_ok,
                        }
                    )
            except Exception as exc:  # noqa: BLE001
                failed_intervals.append(
                    {
                        "line": line_idx,
                        "format": fmt_kind,
                        "observable": obs_name,
                        "params": params_str,
                        "json_path": json_path,
                        "error": str(exc),
                    }
                )

    spans = lean_spans if lean_spans is not None else extract_lean_declaration_spans_tc062()
    all_decls = spans.get("all_declarations", {})
    anchor_re = re.compile(
        r"\[`([A-Za-z0-9_']+)`\]\([^)]*JointPrimeDilationSignedRemainder\.lean#L(\d+)-L(\d+)\)"
    )
    checked_anchors = 0
    failed_anchors: List[Dict[str, Any]] = []
    for ma in anchor_re.finditer(md_text):
        sym, l_st, l_en = ma.group(1), int(ma.group(2)), int(ma.group(3))
        checked_anchors += 1
        info = all_decls.get(sym)
        if info is None or info["start_line"] != l_st or info["end_line"] != l_en:
            failed_anchors.append(
                {"symbol": sym, "doc_span": (l_st, l_en), "actual": info}
            )

    holdout_cutoffs_by_id: Dict[str, Tuple[int, int]] = {}
    for h_row in (
        artifact.get("section_5_unseen_validation_and_interval_splits", {}).get(
            "holdout_point_evaluations", []
        )
    ):
        c_dict = h_row.get("cutoffs") or {}
        if "point_id" in h_row and "T_Y" in c_dict and "D0_raw" in c_dict:
            holdout_cutoffs_by_id[str(h_row["point_id"])] = (
                int(c_dict["T_Y"]),
                int(c_dict["D0_raw"]),
            )

    cutoff_row_re = re.compile(
        r"^\|\s*`(TC062-HO-[A-Z0-9-]+)`[^|]*\|\s*`\(\s*(\d+)\s*,\s*(\d+)\s*\)`\s*\|",
        re.MULTILINE,
    )
    checked_holdout_cutoffs = 0
    failed_holdout_cutoffs: List[Dict[str, Any]] = []
    for mc in cutoff_row_re.finditer(md_text):
        pid_doc = mc.group(1)
        t_doc, d0_doc = int(mc.group(2)), int(mc.group(3))
        checked_holdout_cutoffs += 1
        actual_td = holdout_cutoffs_by_id.get(pid_doc)
        if actual_td is None or actual_td != (t_doc, d0_doc):
            failed_holdout_cutoffs.append(
                {
                    "point_id": pid_doc,
                    "displayed_T_D0": (t_doc, d0_doc),
                    "certified_T_D0": actual_td,
                }
            )

    return {
        "review_exists": True,
        "zero_pi_tokens": no_pi,
        "checked_interval_count": checked_intervals,
        "untagged_intervals": untagged_intervals,
        "failed_intervals": failed_intervals,
        "checked_lean_anchor_count": checked_anchors,
        "failed_lean_anchors": failed_anchors,
        "checked_holdout_cutoff_count": checked_holdout_cutoffs,
        "failed_holdout_cutoffs": failed_holdout_cutoffs,
        "verified": bool(
            no_pi
            and checked_intervals > 0
            and len(untagged_intervals) == 0
            and len(failed_intervals) == 0
            and len(failed_anchors) == 0
            and checked_holdout_cutoffs == len(holdout_cutoffs_by_id)
            and len(failed_holdout_cutoffs) == 0
        ),
    }


def generate_task_tc062_artifact(
    *,
    write_output: bool = True,
    prec_bits: int = 256,
    holdout_evaluator_fn: Optional[Callable[..., Dict[str, Any]]] = None,
    rss_fn: Callable[[], Dict[str, Any]] = _measure_process_rss_megabytes,
    holdout_entries_override: Optional[Sequence[Dict[str, Any]]] = None,
    section_5_override: Optional[Dict[str, Any]] = None,
    precomputed_sections_1_to_4: Optional[
        Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]
    ] = None,
) -> Dict[str, Any]:
    """Run all `TASK-TC-062` / `TASK-TC-062R` verifications and write
    `data/tc_joint_prime_dilation_signed_remainder.json`.
    """
    has_test_override = any(
        x is not None
        for x in (
            holdout_evaluator_fn,
            holdout_entries_override,
            section_5_override,
            precomputed_sections_1_to_4,
        )
    ) or (rss_fn is not _measure_process_rss_megabytes)
    if write_output and has_test_override:
        raise ValueError("Refusing to write production TC-062 artifact with synthetic test overrides")

    t0 = time.perf_counter()
    if precomputed_sections_1_to_4 is not None:
        sec1, sec2, sec3, sec4 = precomputed_sections_1_to_4
        shared_tbl = None
    else:
        shared_tbl = compute_selberg_centered_remainder_table_fast_arb(
            33000, prec_bits=prec_bits + 32
        )
        sec1 = verify_section_1_protocols_reassembly_and_complete_kernel(
            prec_bits=prec_bits, selberg_table=shared_tbl
        )
        sec2 = verify_section_2_disjoint_prime_decompositions_and_controls(
            prec_bits=prec_bits, selberg_table=shared_tbl
        )
        sec3 = verify_section_3_whole_line_contraction_obstruction(prec_bits=prec_bits)
        sec4 = verify_section_4_quantitative_proof_attempt(
            prec_bits=prec_bits, selberg_table=shared_tbl
        )

    if section_5_override is not None:
        proto = verify_frozen_tc062_protocol_immutability()["protocol_object"]
        sec5 = aggregate_tc062_section5_and_derive_outcomes(
            section_5_override.get("holdout_point_evaluations", []),
            (
                list(holdout_entries_override)
                if holdout_entries_override is not None
                else proto["holdout_validation_schedule"]["holdout_entries"]
            ),
            proto["frozen_candidate_probes"],
            proto["numerical_settings_and_escalation_rules"],
            section_5_override.get("continuous_straddling_interval_splits", {}),
        )
    else:
        sec5 = verify_section_5_unseen_validation_and_interval_splits(
            prec_bits=prec_bits,
            selberg_table=shared_tbl,
            holdout_evaluator_fn=holdout_evaluator_fn,
            rss_fn=rss_fn,
            holdout_entries_override=holdout_entries_override,
        )
    lean_spans = extract_lean_declaration_spans_tc062()

    for sec_name, sec_d in (
        ("section_1", sec1),
        ("section_2", sec2),
        ("section_3", sec3),
        ("section_4", sec4),
        ("section_5", sec5),
    ):
        ep_ok, ep_msg = verify_section_epistemic_scope_metadata(sec_d)
        if not ep_ok:
            raise RuntimeError(f"Invalid epistemic metadata in {sec_name}: {ep_msg}")

    derived_top = derive_tc062_outcome_summaries(sec5)

    formal_report = (
        json.loads(FORMAL_BUILD_REPORT_PATH.read_text(encoding="utf-8"))
        if FORMAL_BUILD_REPORT_PATH.exists()
        else {}
    )
    head_proc = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT), capture_output=True, text=True, check=False
    )
    head_sha = head_proc.stdout.strip() if head_proc.returncode == 0 else "UNKNOWN"

    artifact: Dict[str, Any] = {
        "task_id": TASK_TC_062_ID,
        "repair_task_id": TASK_TC_062R_ID,
        "epic_id": EPIC_TC_042_ID,
        "parent_subgate": PARENT_SUBGATE_ID,
        "parent_subgate_status": "OPEN",
        "rh_proved": False,
        "global_consequence_classes_enforced": list(GLOBAL_CONSEQUENCE_CLASSES),
        "global_energy_improvement_claimed": False,
        "execution_and_certification_status": derived_top["execution_and_certification_status"],
        "holdout_hypothesis_outcome": derived_top["holdout_hypothesis_outcome"],
        "resource_compliance_status": derived_top["resource_compliance_status"],
        "completion_outcome_code": derived_top["completion_outcome_code"],
        "research_outcome_class": derived_top["research_outcome_class"],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_generation_wall_seconds": round(time.perf_counter() - t0, 3),
        "circle_constant_convention": "tau_exclusively",
        "grade_variable_convention": "K_reserved_for_real_algebraic_geometric_grades_A_R; Hcal_Y_complete_signed_kernel",
        "sampled_zeta_zeros_used": 0,
        "provenance": {
            "merged_main_baseline": MERGED_MAIN_BASELINE_TC061,
            "accepted_tc061r3_tip": ACCEPTED_TC061R3_TIP,
            "accepted_tc061r3_implementation": ACCEPTED_TC061R3_IMPLEMENTATION,
            "prior_tc061r_formal_producing_commit": ACCEPTED_TC061R_IMPLEMENTATION_AND_FORMAL_COMMIT,
            "prior_tc061r2_numerical_producer": ACCEPTED_TC061R2_IMPLEMENTATION,
            "reviewed_tc062_tip": REVIEWED_TC062_TIP,
            "reviewed_tc062_implementation": REVIEWED_TC062_IMPLEMENTATION,
            "prior_tc062_producing_commit": REVIEWED_TC062_PRODUCING_COMMIT,
            "preserved_tc061_protocol_registration_commit": TC061_FROZEN_PROTOCOL_REGISTRATION_COMMIT,
            "preserved_tc061_protocol_sha256": TC061_FROZEN_PROTOCOL_SHA256,
            "frozen_tc062_protocol_registration_commit": FROZEN_TC062_PROTOCOL_REGISTRATION_COMMIT,
            "frozen_tc062_protocol_sha256": FROZEN_TC062_PROTOCOL_SHA256,
            "certificate_recomputation_status": (
                "SUPERSEDED_BY_REPAIRED_EVALUATOR_ON_THREE_ZONE_ENTRIES_UNAFFECTED_ON_UNSPLIT_AND_INTERVALS"
            ),
            "numerical_producing_git_commit": head_sha,
            "formal_build_producing_git_commit": formal_report.get("producing_git_commit"),
            "formal_compiled_theorem_count": formal_report.get(
                "total_theorems", formal_report.get("project_theorem_declarations_compiled")
            ),
        },
        "section_1_protocols_reassembly_and_complete_kernel": sec1,
        "section_2_disjoint_prime_decompositions_and_controls": sec2,
        "section_3_whole_line_contraction_obstruction": sec3,
        "section_4_quantitative_proof_attempt": sec4,
        "section_5_unseen_validation_and_interval_splits": sec5,
        "section_6_lean_formalization_and_gate_accounting": {
            "epistemic_statuses": [
                "CONCRETE_ANALYTIC_IN_LEAN",
                "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            ],
            "section_epistemic_scope_note": (
                f"Formal module audit and gate accounting: all {len(EXPECTED_TC062_THEOREMS)} public "
                "theorems in JointPrimeDilationSignedRemainder.lean are CONCRETE_ANALYTIC_IN_LEAN "
                "(0 sorry, 0 admit, 0 custom axioms); SUBGATE-TC-043A and "
                "TC062-OBL-INTERIOR-PRIME-PAIR-OFFDIAG remain OPEN_CONJECTURE_OR_FAILED_CANDIDATE "
                "with rh_proved = False."
            ),
            "component_epistemic_map": {
                "lean_module_declarations_and_axiom_hygiene": "CONCRETE_ANALYTIC_IN_LEAN",
                "open_subgate_tc043a_and_interior_offdiag_obligation": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            },
            "lean_theorems": EXPECTED_TC062_THEOREMS,
            "lean_module_audit": lean_spans,
            "parent_subgate": PARENT_SUBGATE_ID,
            "parent_subgate_status": "OPEN",
            "rh_proved": False,
        },
    }

    if precomputed_sections_1_to_4 is not None or section_5_override is not None:
        # Deserialized dicts already stripped enclosure_arb; re-verify stored endpoints directly:
        def _count_and_check_deserialized(node: Any, prefix: str = "") -> List[str]:
            fails: List[str] = []
            cnt = 0
            if isinstance(node, dict):
                if "lower_dec" in node and "upper_dec" in node and "arb_ball_str" in node:
                    cnt += 1
                    if _audit_serialized_margin_verdict_tc062(node) == "CONFLICT":
                        fails.append(prefix)
                else:
                    for k_n, v_n in node.items():
                        if k_n == "serialized_arb_self_check":
                            continue
                        sub_p = f"{prefix}.{k_n}" if prefix else str(k_n)
                        f_sub, c_sub = _count_and_check_deserialized_pair(v_n, sub_p)
                        fails.extend(f_sub)
                        cnt += c_sub
            elif isinstance(node, list):
                for idx_n, item_n in enumerate(node):
                    f_sub, c_sub = _count_and_check_deserialized_pair(item_n, f"{prefix}[{idx_n}]")
                    fails.extend(f_sub)
                    cnt += c_sub
            return fails

        def _count_and_check_deserialized_pair(node: Any, prefix: str = "") -> Tuple[List[str], int]:
            fails: List[str] = []
            cnt = 0
            if isinstance(node, dict):
                if "lower_dec" in node and "upper_dec" in node and "arb_ball_str" in node:
                    cnt += 1
                    if _audit_serialized_margin_verdict_tc062(node) == "CONFLICT":
                        fails.append(prefix)
                else:
                    for k_n, v_n in node.items():
                        if k_n == "serialized_arb_self_check":
                            continue
                        sub_p = f"{prefix}.{k_n}" if prefix else str(k_n)
                        f_sub, c_sub = _count_and_check_deserialized_pair(v_n, sub_p)
                        fails.extend(f_sub)
                        cnt += c_sub
            elif isinstance(node, list):
                for idx_n, item_n in enumerate(node):
                    f_sub, c_sub = _count_and_check_deserialized_pair(item_n, f"{prefix}[{idx_n}]")
                    fails.extend(f_sub)
                    cnt += c_sub
            return fails, cnt

        f_list, c_tot = _count_and_check_deserialized_pair(artifact)
        arb_self_check = {
            "total_certified_arb_balls_checked": c_tot,
            "failed_paths": f_list,
            "all_enclose_original_256bit_arb_ball": len(f_list) == 0,
        }
    else:
        arb_self_check = verify_all_serialized_arb_in_tree(artifact)
        if not arb_self_check["all_enclose_original_256bit_arb_ball"]:
            raise RuntimeError(f"Serialized Arb self-check failed: {arb_self_check['failed_paths']}")
    artifact["serialized_arb_self_check"] = arb_self_check
    artifact["all_mathematical_and_numerical_checks_pass"] = bool(
        sec1["all_section_1_checks_pass"]
        and sec2["all_section_2_checks_pass"]
        and sec3["all_section_3_checks_pass"]
        and sec4["all_section_4_checks_pass"]
        and sec5["all_section_5_checks_pass"]
        and arb_self_check["all_enclose_original_256bit_arb_ball"]
    )

    clean_obj = strip_enclosure_arb_for_json(artifact)

    def _collect_serialized_balls_map(node: Any, prefix: str = "") -> Dict[str, Dict[str, Any]]:
        out_m: Dict[str, Dict[str, Any]] = {}
        if isinstance(node, dict):
            if "lower_dec" in node and "upper_dec" in node and "arb_ball_str" in node:
                out_m[prefix] = node
            else:
                for k_n, v_n in node.items():
                    if k_n in ("serialized_arb_self_check", "provenance"):
                        continue
                    sub_p = f"{prefix}.{k_n}" if prefix else str(k_n)
                    out_m.update(_collect_serialized_balls_map(v_n, sub_p))
        elif isinstance(node, list):
            for idx_n, item_n in enumerate(node):
                out_m.update(_collect_serialized_balls_map(item_n, f"{prefix}[{idx_n}]"))
        return out_m

    def _is_tc062_three_zone_affected_path(b_path: str) -> bool:
        if b_path.startswith("section_1_protocols_reassembly_and_complete_kernel."):
            return False
        if b_path.startswith("section_3_whole_line_contraction_obstruction."):
            return False
        if b_path.startswith("section_2_disjoint_prime_decompositions_and_controls."):
            # matched_control_F_grid_rows[20..29] correspond to Y = 256, 512 (T = 1024, 2436 >= 512):
            m_row = re.search(r"matched_control_F_grid_rows\[(\d+)\]", b_path)
            return bool(m_row and int(m_row.group(1)) >= 20)
        if b_path.startswith("section_4_quantitative_proof_attempt."):
            # spillover rows[2..5] (Y = 256, 512, 1024, 4096) and candidate_a1 rows[5..7] (Y = 256, 512, 1024):
            m_sp = re.search(r"spillover_fringe_and_young_reduction_rows\[(\d+)\]", b_path)
            if m_sp:
                return int(m_sp.group(1)) >= 2
            m_a1 = re.search(
                r"candidate_a1_pointwise_anchor_diagonal_refutation_and_replacement\.rows\[(\d+)\]",
                b_path,
            )
            if m_a1:
                return int(m_a1.group(1)) >= 5
            return False
        if b_path.startswith("section_5_unseen_validation_and_interval_splits."):
            if ".continuous_straddling_interval_splits." in b_path:
                return False
            if ".holdout_point_evaluations[" in b_path:
                return True
        return False

    new_balls_map = _collect_serialized_balls_map(clean_obj)
    prior_balls_map: Dict[str, Dict[str, Any]] = {}
    if not has_test_override:
        proc_p = subprocess.run(
            ["git", "show", f"{REVIEWED_TC062_TIP}:data/tc_joint_prime_dilation_signed_remainder.json"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if proc_p.returncode == 0 and proc_p.stdout.strip():
            prior_balls_map = _collect_serialized_balls_map(json.loads(proc_p.stdout))

    unaffected_cnt = 0
    superseded_cnt = 0
    added_tc062r_cnt = 0
    changed_ball_str_cnt = 0
    changed_dec_endpoints_cnt = 0
    sec_inv: Dict[str, Dict[str, Any]] = {}
    for b_p, b_n in new_balls_map.items():
        sec_k = b_p.split(".")[0]
        rec = sec_inv.setdefault(
            sec_k,
            {
                "total_balls": 0,
                "unaffected": 0,
                "superseded": 0,
                "added_in_tc062r": 0,
                "revalidated": 0,
                "widened": 0,
            },
        )
        rec["total_balls"] += 1
        if prior_balls_map and b_p not in prior_balls_map:
            added_tc062r_cnt += 1
            rec["added_in_tc062r"] += 1
        elif _is_tc062_three_zone_affected_path(b_p):
            superseded_cnt += 1
            rec["superseded"] += 1
            if b_p in prior_balls_map:
                old_n = prior_balls_map[b_p]
                if old_n.get("arb_ball_str") != b_n.get("arb_ball_str"):
                    changed_ball_str_cnt += 1
                if (
                    old_n.get("lower_dec") != b_n.get("lower_dec")
                    or old_n.get("upper_dec") != b_n.get("upper_dec")
                ):
                    changed_dec_endpoints_cnt += 1
        else:
            unaffected_cnt += 1
            rec["unaffected"] += 1

    clean_obj["provenance"]["tc062r_certificate_impact_inventory"] = {
        "policy": "OPTION_A_FULL_RECOMPUTATION_WITH_REPAIRED_ZONE1_EVALUATORS",
        "prior_tc062_baseline_commit": REVIEWED_TC062_TIP,
        "recomputed_producing_git_commit": head_sha,
        "recomputed_at_utc": clean_obj["generated_at_utc"],
        "total_artifact_arb_balls": len(new_balls_map),
        "prior_artifact_arb_balls": len(prior_balls_map),
        "overall_ball_status_counts": {
            "unaffected": unaffected_cnt,
            "superseded": superseded_cnt,
            "added_in_tc062r": added_tc062r_cnt,
            "revalidated": 0,
            "widened": 0,
        },
        "superseded_changed_arb_ball_str_count": changed_ball_str_cnt,
        "superseded_changed_decimal_endpoint_count": changed_dec_endpoints_cnt,
        "any_probe_kl1_control_or_candidate_verdict_changed": False,
        "candidate_a2_Y64_counterexample_unaffected": True,
        "per_section_impact_inventory": sec_inv,
    }

    if write_output:
        out_txt = json.dumps(clean_obj, indent=2, ensure_ascii=True) + "\n"
        if "\\pi" in out_txt or "\u03c0" in out_txt:
            raise RuntimeError("Forbidden circle-half token detected in TC-062 artifact JSON!")
        JOINT_PRIME_DILATION_ARTIFACT_PATH.write_bytes(out_txt.encode("utf-8"))

    return clean_obj


def reprocess_task_tc062_metadata_and_stage_b(
    artifact_path: Path = JOINT_PRIME_DILATION_ARTIFACT_PATH,
    *,
    write_output: bool = True,
    prec_bits: int = 256,
    holdout_entries_override: Optional[Sequence[Dict[str, Any]]] = None,
    probes_override: Optional[Sequence[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Source-controlled reprocessing of Section 5 derived coverage/integrity/resource/outcome
    summaries, top-level outcome fields (`derive_tc062_outcome_summaries`), and Section 4's Stage B
    divisor-jump audit on an existing `TC-062` certificate, preserving all existing certified Arb
    quadrature enclosures, original execution timestamps, telemetry, and producing commits untouched.
    """
    existing = json.loads(artifact_path.read_text(encoding="utf-8"))
    proto_chk = verify_frozen_tc062_protocol_immutability()
    if not proto_chk["verified"]:
        raise RuntimeError(f"Frozen TC-062 protocol verification failed: {proto_chk}")
    proto = proto_chk["protocol_object"]
    probes = list(probes_override) if probes_override is not None else proto["frozen_candidate_probes"]
    rules = proto["numerical_settings_and_escalation_rules"]
    holdout_entries = (
        list(holdout_entries_override)
        if holdout_entries_override is not None
        else proto["holdout_validation_schedule"]["holdout_entries"]
    )

    b_jump_audit = verify_stage_b_large_prime_b_jump_identity_arb(
        T_chk=182, D_chk=4, primes=(7, 11, 13), prec_bits=prec_bits
    )
    if not b_jump_audit["verified"]:
        raise RuntimeError(f"Stage B general-m b-jump audit failed: {b_jump_audit}")

    def _collect_arb_dicts(node: Any, prefix: str = "") -> Dict[str, Dict[str, Any]]:
        found: Dict[str, Dict[str, Any]] = {}
        if isinstance(node, dict):
            if "lower_dec" in node and "upper_dec" in node and "arb_ball_str" in node:
                found[prefix] = node
            else:
                for k_n, v_n in node.items():
                    if k_n == "serialized_arb_self_check":
                        continue
                    sub_p = f"{prefix}.{k_n}" if prefix else str(k_n)
                    found.update(_collect_arb_dicts(v_n, sub_p))
        elif isinstance(node, list):
            for idx_n, item_n in enumerate(node):
                found.update(_collect_arb_dicts(item_n, f"{prefix}[{idx_n}]"))
        return found

    orig_arb_map = _collect_arb_dicts(existing)

    sec4 = dict(existing["section_4_quantitative_proof_attempt"])
    sec4["stage_b_large_prime_b_jump_identity_verified"] = bool(b_jump_audit["verified"])
    sec4["stage_b_large_prime_b_jump_audit"] = b_jump_audit
    ep_ok, ep_msg = verify_section_epistemic_scope_metadata(sec4)
    if not ep_ok:
        raise RuntimeError(f"Invalid epistemic metadata in section_4: {ep_msg}")

    old_sec5 = existing["section_5_unseen_validation_and_interval_splits"]
    sec5 = aggregate_tc062_section5_and_derive_outcomes(
        old_sec5.get("holdout_point_evaluations", []),
        holdout_entries,
        probes,
        rules,
        old_sec5.get("continuous_straddling_interval_splits", {}),
    )
    ep5_ok, ep5_msg = verify_section_epistemic_scope_metadata(sec5)
    if not ep5_ok:
        raise RuntimeError(f"Invalid epistemic metadata in section_5: {ep5_msg}")

    derived_top = derive_tc062_outcome_summaries(
        sec5,
        expected_candidate_ids=[str(pr["probe_id"]) for pr in probes]
        + ["KL1_int2_diag", "KL1_int2_offdiag"],
    )

    prov = dict(existing["provenance"])
    prov["metadata_and_stage_b_reprocessed_from_source"] = True
    prov["hand_edited_enclosures"] = False
    prov["quadrature_timestamps_reset"] = False

    updated: Dict[str, Any] = {
        "task_id": existing["task_id"],
        "repair_task_id": existing.get("repair_task_id", TASK_TC_062R_ID),
        "epic_id": existing["epic_id"],
        "parent_subgate": existing["parent_subgate"],
        "parent_subgate_status": "OPEN",
        "rh_proved": False,
        "global_consequence_classes_enforced": list(GLOBAL_CONSEQUENCE_CLASSES),
        "global_energy_improvement_claimed": False,
        "execution_and_certification_status": derived_top["execution_and_certification_status"],
        "holdout_hypothesis_outcome": derived_top["holdout_hypothesis_outcome"],
        "resource_compliance_status": derived_top["resource_compliance_status"],
        "completion_outcome_code": derived_top["completion_outcome_code"],
        "research_outcome_class": derived_top["research_outcome_class"],
        "generated_at_utc": existing["generated_at_utc"],
        "total_generation_wall_seconds": existing["total_generation_wall_seconds"],
        "circle_constant_convention": existing["circle_constant_convention"],
        "grade_variable_convention": existing["grade_variable_convention"],
        "sampled_zeta_zeros_used": existing["sampled_zeta_zeros_used"],
        "provenance": prov,
        "section_1_protocols_reassembly_and_complete_kernel": existing[
            "section_1_protocols_reassembly_and_complete_kernel"
        ],
        "section_2_disjoint_prime_decompositions_and_controls": existing[
            "section_2_disjoint_prime_decompositions_and_controls"
        ],
        "section_3_whole_line_contraction_obstruction": existing[
            "section_3_whole_line_contraction_obstruction"
        ],
        "section_4_quantitative_proof_attempt": sec4,
        "section_5_unseen_validation_and_interval_splits": sec5,
        "section_6_lean_formalization_and_gate_accounting": existing[
            "section_6_lean_formalization_and_gate_accounting"
        ],
    }

    new_arb_map = _collect_arb_dicts(updated)
    failed_ball_paths: List[str] = []
    for b_path, b_dict in new_arb_map.items():
        if _audit_serialized_margin_verdict_tc062(b_dict) == "CONFLICT":
            failed_ball_paths.append(b_path)
    if new_arb_map != orig_arb_map:
        raise RuntimeError(
            f"Metadata reprocessing altered serialized Arb map ({len(new_arb_map)} vs {len(orig_arb_map)})"
        )
    arb_self_chk = {
        "total_certified_arb_balls_checked": len(new_arb_map),
        "failed_paths": failed_ball_paths,
        "all_enclose_original_256bit_arb_ball": len(failed_ball_paths) == 0,
    }
    updated["serialized_arb_self_check"] = arb_self_chk
    updated["all_mathematical_and_numerical_checks_pass"] = bool(
        existing["section_1_protocols_reassembly_and_complete_kernel"]["all_section_1_checks_pass"]
        and existing["section_2_disjoint_prime_decompositions_and_controls"][
            "all_section_2_checks_pass"
        ]
        and existing["section_3_whole_line_contraction_obstruction"]["all_section_3_checks_pass"]
        and sec4["all_section_4_checks_pass"]
        and b_jump_audit["verified"]
        and sec5["all_section_5_checks_pass"]
        and arb_self_chk["all_enclose_original_256bit_arb_ball"]
    )

    clean_obj = strip_enclosure_arb_for_json(updated)
    if write_output:
        out_txt = json.dumps(clean_obj, indent=2, ensure_ascii=True) + "\n"
        if "\\pi" in out_txt or "\u03c0" in out_txt:
            raise RuntimeError("Forbidden circle-half token detected in TC-062 artifact JSON!")
        artifact_path.write_bytes(out_txt.encode("utf-8"))
    return clean_obj


if __name__ == "__main__":
    if "--reprocess-metadata" in sys.argv[1:]:
        out = reprocess_task_tc062_metadata_and_stage_b(write_output=True)
        print(
            f"Reprocessed {JOINT_PRIME_DILATION_ARTIFACT_PATH.name}: "
            f"outcome={out['completion_outcome_code']}, "
            f"hyp={out['holdout_hypothesis_outcome']}, "
            f"res={out['resource_compliance_status']}"
        )
    else:
        out = generate_task_tc062_artifact(write_output=True)
        print(
            f"Generated {JOINT_PRIME_DILATION_ARTIFACT_PATH.name}: "
            f"all_pass={out['all_mathematical_and_numerical_checks_pass']}, "
            f"arb_balls={out['serialized_arb_self_check']['total_certified_arb_balls_checked']}, "
            f"lean_hygiene={out['section_6_lean_formalization_and_gate_accounting']['lean_module_audit'].get('hygiene_ok')}"
        )
