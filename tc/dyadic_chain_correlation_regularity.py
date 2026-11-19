r"""
TASK-TC-063: Dyadic-Chain Correlations and the Arithmetic Regularity Constraint
toward SUBGATE-TC-043A (EPIC-TC-042).

Implements, verifies, and certifies in 256-bit FLINT/Arb outward-rounded ball arithmetic:
- Circle constant convention: `tau` exclusively (`0` circle-half macros or glyphs).
- Grade variable convention: `K` reserved strictly for real-algebraic geometric grades `K in A_R`
  (`0` non-grade `K` underscore identifiers); complete signed kernel denoted `Hcal_Y`; grouped
  2-adic odd-chain kernel denoted `Kcal_Y`; complex arguments written `z = x + i*y` (`x, y` real,
  critical line `x = 1/2`); analytic scale `Y >= 2` kept a real variable throughout.

Sections:
1. Section 1 — Endpoint Regularity Contradiction, Premise Table, & Window-Base Analysis (§2):
   - Verifies immutability of all three frozen protocols (`TC-061`, `TC-062`, and `TC-063`) and
     preservation of all `885` `TC-062` and `3,208` `TC-061` certified Arb records.
   - Certifies `L_lambda(x + i*y) = zeta(2*x + 2*i*y) / zeta(x + i*y)` on `x > 1`, trivial-zero
     simultaneous numerator/denominator vanishing at `-2*n`, functional-equation reflection across
     `0 < x < 1`, and parameterized window-base `b > 1` vs `tau` invariance.
   - Records the complete declaration-level premise table (`PROVED_IN_LEAN`,
     `PROVED_ANALYTICALLY_OUTSIDE_LEAN`, `OPEN`).

2. Section 2 — Exact Odd-Part Decomposition (`Sigma_off = S_same + S_different`) & Edge Cases (§4):
   - Exhaustively verifies in exact `Fraction` arithmetic on `T in {0, 1, 2, 3, 5, 6, 7, 8, 14, 15,
     16, 31, 32, 48}` the unique `m = 4^j * u` odd-part bijection, empty/singleton chains, generic
     ordered-pair reindexing on a non-multiplicative sequence and non-symmetric kernel, and
     Liouville `lambda(4^j * u) = lambda(u)` parity invariance.
   - Independently cross-validates 2D `Hcal_Y` double sums against separate 1D quadrature evaluators
     for `S_same(Y)`, `S_different(Y)`, and `Sigma_off(Y; 2)` across `Y in {2, 4, 8, 16, 32, 64}`
     (separating `ALGEBRAIC_CONSISTENCY_CHECK` from `INDEPENDENT_DIRECT_NUMERICAL_VALIDATION`).

3. Section 3 — Uniform Same-Chain Bound, Feature Inner-Product Formula, & Matched Controls (§5, §7):
   - Verifies shifted-station disjointness `{m, 2*m} cap {n, 2*n} = empty` for `m != n in I_2(T)`
     and complete-kernel feature representation `Delta Hcal_Y(m, n) = <U_m, U_n>_Y - 4*<V_m, V_n>`
     (while certifying nonzero `m = n` discrepancy if self-collision terms were dropped on `m = n`).
   - Certifies explicit uniform constants `C_psi`, `C_g = 186*(tau - 1)`, and `C_same = 2*C_psi + 8*C_g`,
     and certifies `|S_same(Y)| <= (L(T) - 1)*(2*sum_psi + 8*sum_log2_G2) <= (L(T) - 1)*(2*C_psi + 8*C_g)
     <= C_same*(1 + log Y)` across `Y in {2, 4, 8, 16, 32, 64, 128, 256, 512, 1024}`.
   - Evaluates genuine Liouville arithmetic alongside matched finite-prime/unsigned controls
     (`unsigned_1`, `a2`, `a_3_5_7` recomputed with each control's own matched `z = 1` Laurent core)
     plus explicitly labeled `hybrid_a2_liouville` on `(S_same, S_different)` across `Y = 16..512`,
     certifying `REFUTED_BY_CERTIFIED_WITNESS` on `S_different` for all negative controls at `Y >= 64`.

4. Section 4 — Substantive Distinct-Chain Research Attempts (`Attempts A, B, C`) & Obstructions (§6):
   - Attempt A (Complete-Kernel Common-Factor Regrouping `u = g*r, v = g*t, gcd(r, t) = 1`):
     verifies exact primitive-pair regrouping, `J_{g*r}(T) = J_r(floor(T/g))`, coprime feature
     decoupling `c(2^a*g*r, 2^b*g*t) = c(g, g) + min(a, b)*(log 2)^2`, `p = 2` `smallOp` jump
     obstruction when `D_eff >= 1`, refutes `TC063-CAND-A1-PRIM-NONPOS` (`Pi_16^diff(5) > 0`,
     `Pi_64^diff(7) > 0`), and quantifies the `g = 1` chain-count Cauchy-Schwarz loss (`O(Y^{5/4}*log Y)`
     globally, `Theta(Y)` on resonant shells) and smooth-vs-rough prime-set iteration wall.
   - Attempt B (Quantitative Square-Projection & Selberg Compatibility):
     verifies exact odd-divisor square-projection `sum_{d in O(T)} Gcal_Y^(d)(X) = sum_{w=m^2 in O(T)} Ucal_w(X)`
     and odd-Mobius recovery, refutes `TC063-CAND-B1-SQPROJ-DIAG-DOM` via certified negative `d_1 != d_2`
     dilation cross-terms, and verifies the exact station-level Selberg decomposition of `psi_{Y, n}(X)`
     across `1 <= n <= T`.
   - Attempt C (Arithmetic-Restricted vs Arbitrary-Sign Quadratic Comparison):
     implements the constructive greedy `+-1` sign-extension witness from `A_odd(Y)` (matching Lean
     Theorem 5(3)), refutes `TC063-CAND-C1-ARB-SIGN` at `Y = 64`, and certifies the
     asymptotic `Omega(Y)` arbitrary-sign obstruction on `[4*Y, (43/10)*Y] subset [Y, tau*Y]`.

5. Section 5 — Frozen 10-Point Unseen `TC-063` Validation & Continuous Interval Case Splits (§7):
   - Evaluates all `10` unseen `TC-063` scales (`81 - 2^-12`, `81 + 2^-12`, `96`, `144`, `288`,
     `576`, `960`, `e^7*(1 - 2^-12)`, `e^7*(1 + 2^-12)`, `1408`) and both unseen continuous
     intervals (`[81 - 2^-12, 81 + 2^-12]` across `T = 243 -> 244` and `[1096.50, 1096.66]` across
     `T = 6310 -> 6311` and `e^7`) with exact binary evaluation-domain recording at creation,
     enforcing all `TC-062R4` admissibility, full-coverage, union-containment, escalation, and
     3-valued `PROCESS_LIFETIME_HIGH_WATER_MARK` resource rules.

6. Section 6 — Live Lean 4 Declaration Audit, Review Verifier, & Honest Gate Accounting (§8, §9):
   - Audits `formal/RiemannScope/DyadicChainCorrelationRegularity.lean`, verifies review enclosures
     and line anchors, and preserves `SUBGATE-TC-043A = OPEN`, `rh_proved = False`.
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
from tc.joint_prime_dilation_signed_remainder import (
    BRANCH_ADMISSIBILITY_STATUSES,
    BRANCH_COVERAGE_STATUSES,
    FROZEN_TC062_PROTOCOL_ID,
    FROZEN_TC062_PROTOCOL_REGISTRATION_COMMIT,
    FROZEN_TC062_PROTOCOL_SHA256,
    JOINT_PRIME_DILATION_ARTIFACT_PATH,
    JOINT_PRIME_DILATION_PROTOCOL_PATH,
    REVIEWED_TC062R_PRODUCING_COMMIT,
    _audit_serialized_margin_verdict_tc062,
    _compare_symbolic_cutoff_bound,
    _derive_exact_branch_admissible_subdomain,
    _evaluate_branch_domain_admissibility_tc062,
    _load_git_json_artifact_or_none,
    _parse_serialized_arb_enclosure_tc062,
    _serialized_union_contains_branch_tc062,
    build_complete_signed_kernel_evaluator_small_T,
    build_matched_control_complete_kernel_small_T,
    derive_exact_interval_cutoff_partition,
    evaluate_interior_paired_matrix_free_arb,
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
    _sci_or_latex_num_to_fraction,
    liouville_lambda_int,
    moebius_mu_int,
)
from tc.mixed_arithmetic_covariance import (
    CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME,
    CERTIFICATION_INTEGRITY_CONFLICT_VERDICT,
    CertificationIntegrityError,
    ExactScaleSpec,
    FROZEN_PROTOCOL_ID as TC061_FROZEN_PROTOCOL_ID,
    FROZEN_PROTOCOL_REGISTRATION_COMMIT as TC061_FROZEN_PROTOCOL_REGISTRATION_COMMIT,
    FROZEN_PROTOCOL_SHA256 as TC061_FROZEN_PROTOCOL_SHA256,
    MERGED_MAIN_BASELINE_TC061,
    MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH,
    POINT_MARGIN_VERDICTS,
    PROBE_GLOBAL_OUTCOMES,
    RECOGNIZED_PEAK_RSS_COVERING_SEMANTICS,
    RESOURCE_COMPLIANCE_STATUSES,
    _measure_process_rss_megabytes,
    aggregate_section_resource_compliance,
    certify_exact_scale_cutoffs,
    certified_ratio_with_positive_denominator,
    classify_probe_margin_arb,
    compute_complete_core_s_Y_and_beta_Y_arb,
    compute_selberg_centered_remainder_table_fast_arb,
    evaluate_control_matched_point_arb,
    evaluate_mixed_covariance_point_arb,
    evaluate_point_resource_compliance,
    evaluate_window_gram_G_Y_r_arb,
    resolve_protocol_quadrature_settings,
    strip_enclosure_arb_for_json,
    verify_frozen_protocol_immutability,
)
from tc.prime_chain_contraction import evaluate_phi_n_arb
from tc.signed_dilation_arithmetic_energy import (
    FORMAL_BUILD_REPORT_PATH,
    classify_arb_le_certificate,
    verify_section_epistemic_scope_metadata,
)

TASK_TC_063_ID = "TASK-TC-063"
PROPOSED_TC063_BRANCH = "task/tc-063-dyadic-chain-correlation-and-arithmetic-regularity"
ACCEPTED_TC062R4_DELIVERED_TIP = "d5a5758c8d661b178d53029053b6d29e204aca28"
ACCEPTED_TC062R4_VALIDATION_COMMIT = "2e48474d17e5223331606d1b8c86be4b937e7a8e"
PRESERVED_TC062R_PRODUCING_COMMIT = REVIEWED_TC062R_PRODUCING_COMMIT

FROZEN_TC063_PROTOCOL_ID = "TC063-DYADIC-CHAIN-CORRELATION-REGULARITY-PROTOCOL-V1"
FROZEN_TC063_PROTOCOL_REGISTRATION_COMMIT = "767ff30dcd605e82f7d855fb0b86ee59919eceb8"
FROZEN_TC063_PROTOCOL_SHA256 = "a5ced83b7aede12e5bcfc4c146a0edb57f7a668ad773098bff44c71e2471edff"

EXPECTED_TC061_ARTIFACT_SHA256 = "1dd8e539645f933c1fc6055f32a5dba4d4bef51a1a67d8ee35a9cdf81bfd49bc"
EXPECTED_TC062_ARTIFACT_SHA256 = "88e1e3afb1d8ef91fbc2fab6aa5e9e0e0d05f357c214c210fdbe669c163a2a14"

DYADIC_CHAIN_PROTOCOL_PATH = (
    REPO_ROOT / "data" / "tc_dyadic_chain_correlation_regularity_protocol.json"
)
DYADIC_CHAIN_ARTIFACT_PATH = (
    REPO_ROOT / "data" / "tc_dyadic_chain_correlation_regularity.json"
)
TC_063_REVIEW_DOC_PATH = (
    REPO_ROOT / "docs" / "reviews" / "TC_063_DYADIC_CHAIN_CORRELATION_AND_ARITHMETIC_REGULARITY.md"
)
TC_063_LEAN_MODULE_PATH = (
    REPO_ROOT / "formal" / "RiemannScope" / "DyadicChainCorrelationRegularity.lean"
)

EXPECTED_TC063_THEOREMS: List[str] = [
    "liouville_dirichlet_ratio_pole_contradiction_and_reflection_tc063",
    "exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063",
    "uniform_same_chain_hilbert_bound_and_closure_transfer_tc063",
    "odd_common_factor_primitive_regrouping_and_feature_decoupling_tc063",
    "odd_square_projection_selberg_split_and_sign_extension_obstruction_tc063",
]

PRESCRIBED_TC063_INTERVAL_SPLITS: Dict[str, Tuple[Fraction, Fraction]] = {
    "interval_81_pm_2_neg12_across_T243": (Fraction(331775, 4096), Fraction(331777, 4096)),
    "interval_1096_50_to_1096_66_across_T6310_and_e7": (
        Fraction(2193, 2),
        Fraction(54833, 50),
    ),
}

REQUIRED_TC063_INTERVAL_UNION_BRANCH_PAIRS: Tuple[Tuple[str, str], ...] = (
    ("union_E_Y", "E_Y"),
    ("union_D_tilde_Y", "D_tilde_Y"),
    ("union_log_Y_times_D_tilde", "log_Y_times_D_tilde"),
    ("union_Sigma_off_p2", "Sigma_off_p2"),
    ("union_S_same_Y", "S_same_Y"),
    ("union_S_different_Y", "S_different_Y"),
    ("union_M_P0_DIFF", "M_P0_DIFF"),
    ("union_M_P_NEG_DIFF", "M_P_NEG_DIFF"),
    ("union_M_SAME_LOC", "M_SAME_LOC"),
)

REQUIRED_CURRENT_TC063_STATUS_KEYS: Tuple[str, ...] = (
    "top.execution_and_certification_status",
    "top.holdout_hypothesis_outcome",
    "top.primary_log_saving_probe_outcome",
    "top.resource_compliance_status",
    "top.completion_outcome_code",
    "top.research_outcome_class",
    "top.all_mathematical_and_numerical_checks_pass",
    "top.parent_subgate_status",
    "top.rh_proved",
    "top.global_energy_improvement_claimed",
    "sec5.registered_unseen_point_count",
    "sec5.evaluated_unseen_point_count",
    "sec5.coverage_complete",
    "sec5.certification_integrity_ok",
    "sec5.all_required_applicable_evaluations_resolved",
    "sec5.all_section_5_checks_pass",
)


# ---------------------------------------------------------------------------
# 0. Dyadic-Chain Index Helpers, Greedy Sign Extension, & Protocol Immutability
# ---------------------------------------------------------------------------


def interior_two_adic_anchors(T: int) -> List[int]:
    """Return `I_2(T) := {m >= 1 : 2*m <= T and v_2(m) is even}`."""
    if T < 0:
        raise ValueError(f"T must be >= 0, got {T}")
    return [m for m in range(1, (T // 2) + 1) if prime_valuation_v_p(m, 2) % 2 == 0]


def odd_chain_parts_O_T(T: int) -> List[int]:
    """Return `O(T) := {u >= 1 : u odd and 2*u <= T}`."""
    if T < 0:
        raise ValueError(f"T must be >= 0, got {T}")
    return [u for u in range(1, (T // 2) + 1) if u % 2 == 1]


def dyadic_chain_exponents_J_u(u: int, T: int) -> List[int]:
    """Return `J_u(T) := {j >= 0 : 2 * 4^j * u <= T}` for `u >= 1`."""
    if u < 1:
        raise ValueError(f"u must be >= 1, got {u}")
    if T < 0:
        raise ValueError(f"T must be >= 0, got {T}")
    out: List[int] = []
    j = 0
    while 2 * (4 ** j) * u <= T:
        out.append(j)
        j += 1
    return out


def max_dyadic_chain_length_L(T: int) -> int:
    """Return `L(T) := max_{u in O(T)} |J_u(T)|` (`0` if `O(T)` is empty, i.e. `T < 2`)."""
    o_set = odd_chain_parts_O_T(T)
    if not o_set:
        return 0
    return max(len(dyadic_chain_exponents_J_u(u, T)) for u in o_set)


def odd_common_factor_gcd_set(T: int) -> List[int]:
    """Return `G_odd(T) := {g >= 1 : g odd and 6*g <= T}`."""
    if T < 0:
        raise ValueError(f"T must be >= 0, got {T}")
    return [g for g in range(1, (T // 6) + 1) if g % 2 == 1]


def greedy_sign_extension_witness(
    all_nodes: Sequence[int],
    seed_subset: Sequence[int],
    kernel_fn: Callable[[int, int], arb],
) -> Dict[int, int]:
    """Constructive deterministic `+-1` sign extension `eps : all_nodes -> {+1, -1}` fixing
    `eps[u] = +1` on `seed_subset` and extending one element `w in all_nodes \\ seed_subset` at a
    time by choosing `eps[w] = +1` if `mid(sum_{u in B} eps[u]*(H(w, u) + H(u, w))) >= 0` else `-1`
    (guaranteeing `sum_{u != v in all_nodes} eps[u]*eps[v]*H(u, v) >= sum_{u != v in seed_subset} H(u, v)`
    whenever the stepwise sums have certified or non-negative sign, verified directly in Arb).
    """
    seed_set = set(int(u) for u in seed_subset)
    ordered_nodes = [int(u) for u in all_nodes]
    if not seed_set.issubset(set(ordered_nodes)):
        raise ValueError("seed_subset must be a subset of all_nodes")
    eps: Dict[int, int] = {u: 1 for u in ordered_nodes if u in seed_set}
    active: List[int] = [u for u in ordered_nodes if u in seed_set]
    for w in ordered_nodes:
        if w in eps:
            continue
        cross = arb(0)
        for u in active:
            cross += arb(eps[u]) * (kernel_fn(w, u) + kernel_fn(u, w))
        sgn = 1 if float(cross.mid()) >= 0.0 else -1
        eps[w] = sgn
        active.append(w)
    return eps


def verify_frozen_tc063_protocol_immutability(
    protocol_path: Path = DYADIC_CHAIN_PROTOCOL_PATH,
) -> Dict[str, Any]:
    """Verify SHA-256 and git-commit ancestry of `data/tc_dyadic_chain_correlation_regularity_protocol.json`."""
    raw_bytes = protocol_path.read_bytes().replace(b"\r\n", b"\n")
    proto = json.loads(raw_bytes.decode("utf-8"))
    proto_without_hash = {k: v for k, v in proto.items() if k != "protocol_sha256"}
    canonical_bytes = json.dumps(
        proto_without_hash, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    computed_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
    recorded_sha256 = proto.get("protocol_sha256")
    hash_ok = bool(
        computed_sha256 == FROZEN_TC063_PROTOCOL_SHA256
        and recorded_sha256 == FROZEN_TC063_PROTOCOL_SHA256
    )

    git_blob_matches = False
    git_commit_is_ancestor = False
    try:
        proc_blob = subprocess.run(
            [
                "git",
                "show",
                f"{FROZEN_TC063_PROTOCOL_REGISTRATION_COMMIT}:data/tc_dyadic_chain_correlation_regularity_protocol.json",
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
                FROZEN_TC063_PROTOCOL_REGISTRATION_COMMIT,
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
        "protocol_path": "data/tc_dyadic_chain_correlation_regularity_protocol.json",
        "protocol_id": proto.get("protocol_id"),
        "expected_protocol_sha256": FROZEN_TC063_PROTOCOL_SHA256,
        "computed_protocol_sha256": computed_sha256,
        "recorded_protocol_sha256": recorded_sha256,
        "sha256_verified": hash_ok,
        "registration_commit": FROZEN_TC063_PROTOCOL_REGISTRATION_COMMIT,
        "git_blob_matches_registration_commit": git_blob_matches,
        "registration_commit_is_ancestor_of_head": git_commit_is_ancestor,
        "protocol_object": proto,
        "verified": bool(
            proto.get("protocol_id") == FROZEN_TC063_PROTOCOL_ID
            and hash_ok
            and git_blob_matches
            and git_commit_is_ancestor
        ),
    }


# ---------------------------------------------------------------------------
# 1. Separate 1D Quadrature Evaluators for S_same(Y) and S_different(Y)
# ---------------------------------------------------------------------------


def evaluate_same_and_chain_diag_1d_arb(
    Y_arb: arb,
    T_y: int,
    D0_eff: int,
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
    quad_tol_bits: int = 180,
    n_panels: int = 16,
    b_vec_override: Optional[Sequence[arb]] = None,
    eps_2: int = -1,
) -> Dict[str, arb]:
    """Evaluate `S_same(Y)` and `D_chain(Y) := sum_{u in O(T)} (||Ucal_u||_Y^2 - 4*||Vcal_u||^2)`
    directly via full-sum 1D `acb.integral` quadrature over `[Y, tau*Y]` (`0` Zone-1 truncation),
    using the exact odd-chain prime-power identity `c(2^a * u, 2^b * u) = c(u, u) + min(a, b)*(log 2)^2`
    to evaluate `||Vcal_u(X)||_{pp}^2` in `O(|J_u(T)|)` operations without a prime-power loop.
    """
    if prec_bits < 53:
        raise ValueError(f"prec_bits must be >= 53, got {prec_bits}")
    if eps_2 not in (-1, 1):
        raise ValueError(f"eps_2 must be -1 or +1, got {eps_2}")
    if T_y < 2:
        return {"S_same": arb(0), "D_chain": arb(0)}

    work_prec = prec_bits + 32
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = work_prec
        tau = _tau_arb()
        log_tau = tau.log()
        if b_vec_override is None:
            vecs = compute_complete_core_s_Y_and_beta_Y_arb(
                T_y, D0_eff, selberg_table["R_osc"], prec_bits=work_prec
            )
            b_c = [acb(0)] + [
                acb(arb(liouville_lambda_int(n)) * vecs["beta_Y"][n]) for n in range(1, T_y + 1)
            ]
        else:
            b_c = [acb(v) for v in b_vec_override]

        c_div = [arb(0)] * (T_y + 1)
        for q_p, a_e in prime_power_pairs_up_to(T_y):
            qa = q_p ** a_e
            lg2_q = arb(q_p).log() ** 2
            for mult in range(qa, T_y + 1, qa):
                c_div[mult] += lg2_q
        lg2_two_c = acb(arb(2).log() ** 2)
        eps_c = acb(eps_2)

        chains: List[Tuple[acb, List[Tuple[int, int]]]] = []
        active_stations_set: set[int] = set()
        for u in range(1, (T_y // 2) + 1, 2):
            pairs: List[Tuple[int, int]] = []
            j = 0
            while 2 * (4 ** j) * u <= T_y:
                m_j = (4 ** j) * u
                pairs.append((m_j, 2 * m_j))
                active_stations_set.add(m_j)
                active_stations_set.add(2 * m_j)
                j += 1
            chains.append((acb(c_div[u]), pairs))
        active_stations = [
            (k, acb(k) ** (-3), acb(-(arb(k * k) ** (-1))))
            for k in sorted(active_stations_set)
        ]

        Yc = acb(Y_arb)
        lgYc = acb(Y_arb.log())
        Yc_52 = Yc ** (acb(5) / acb(2))
        Yc_2 = Yc * Yc
        tol = arb(2) ** (-quad_tol_bits)

        S_same_acc = arb(0)
        D_chain_acc = arb(0)
        for j_p in range(n_panels):
            u_lo = log_tau * arb(j_p) / arb(n_panels)
            u_hi = log_tau * arb(j_p + 1) / arb(n_panels)
            node_cache: Dict[Tuple[str, str, bool], Tuple[acb, acb]] = {}
            is_point_Y = bool(Y_arb.rad() == arb(0))

            def _eval_both(u_var: acb, _an: bool) -> Optional[Tuple[acb, acb]]:
                lg = lgYc + u_var
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    return None
                key = (repr(u_var.real), repr(u_var.imag), _an) if is_point_Y else None
                if key is not None:
                    hit = node_cache.get(key)
                    if hit is not None:
                        return hit
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_var).exp()
                x2 = Yc_2 * (acb(2) * u_var).exp()
                ph = [acb(0)] * (T_y + 1)
                for k_i, inv_k3, neg_inv_k2 in active_stations:
                    ph[k_i] = x52 * inv_k3 * (x2 * neg_inv_k2).exp()

                same_u_part = acb(0)
                same_v_c_part = acb(0)
                same_v_2_part = acb(0)
                dch_u_part = acb(0)
                dch_v_c_part = acb(0)
                dch_v_2_part = acb(0)

                for c_u_c, pairs in chains:
                    L_u = len(pairs)
                    if L_u == 1:
                        m0, tm0 = pairs[0]
                        ph_m0 = ph[m0]
                        ph_tm0 = ph[tm0]
                        u0 = (acb(1) - b_c[m0] * inv_lg2) * ph_m0 + eps_c * (
                            acb(1) - b_c[tm0] * inv_lg2
                        ) * ph_tm0
                        dp0 = ph_m0 + eps_c * ph_tm0
                        dch_u_part += u0 * u0
                        dch_v_c_part += c_u_c * (dp0 * dp0)
                        dch_v_2_part += ph_tm0 * ph_tm0
                    else:
                        u_tot = acb(0)
                        u_diag = acb(0)
                        dp_tot = acb(0)
                        dp_diag = acb(0)
                        f_list: List[acb] = []
                        for m_j, tm_j in pairs:
                            ph_m = ph[m_j]
                            ph_tm = ph[tm_j]
                            uj = (acb(1) - b_c[m_j] * inv_lg2) * ph_m + eps_c * (
                                acb(1) - b_c[tm_j] * inv_lg2
                            ) * ph_tm
                            dpj = ph_m + eps_c * ph_tm
                            u_tot += uj
                            u_diag += uj * uj
                            dp_tot += dpj
                            dp_diag += dpj * dpj
                            f_list.append(ph_m)
                            f_list.append(eps_c * ph_tm)
                        u_tot_sq = u_tot * u_tot
                        dp_tot_sq = dp_tot * dp_tot
                        dch_u_part += u_tot_sq
                        same_u_part += u_tot_sq - u_diag
                        dch_v_c_part += c_u_c * dp_tot_sq
                        same_v_c_part += c_u_c * (dp_tot_sq - dp_diag)

                        R_u = 2 * L_u
                        suf = acb(0)
                        suf_sq_sum = acb(0)
                        for a_idx in range(R_u - 1, 0, -1):
                            suf += f_list[a_idx]
                            suf_sq_sum += suf * suf

                        j_min_diag = acb(0)
                        for j_idx, (m_j, tm_j) in enumerate(pairs):
                            dpj = ph[m_j] + eps_c * ph[tm_j]
                            phtm = ph[tm_j]
                            if j_idx > 0:
                                j_min_diag += acb(2 * j_idx) * (dpj * dpj)
                            j_min_diag += phtm * phtm
                        dch_v_2_part += suf_sq_sum
                        same_v_2_part += suf_sq_sum - j_min_diag

                same_val = same_u_part - acb(4) * (same_v_c_part + lg2_two_c * same_v_2_part) * inv_lg2
                dch_val = dch_u_part - acb(4) * (dch_v_c_part + lg2_two_c * dch_v_2_part) * inv_lg2
                out = (same_val, dch_val)
                if key is not None:
                    node_cache[key] = out
                return out

            def _int_i(idx: int) -> arb:
                def _cb(u_v: acb, _an: bool) -> acb:
                    r = _eval_both(u_v, _an)
                    if r is None:
                        nb = arb("nan")
                        return acb(nb, nb)
                    return r[idx]

                return acb.integral(_cb, acb(u_lo), acb(u_hi), rel_tol=tol, abs_tol=tol).real

            S_same_acc += _int_i(0)
            D_chain_acc += _int_i(1)

        flint_ctx.prec = prec_bits
        return {"S_same": +S_same_acc, "D_chain": +D_chain_acc}
    finally:
        flint_ctx.prec = saved


def evaluate_dyadic_chain_observables_matrix_free_arb(
    Y_arb: arb,
    T_y: int,
    D0_eff: int,
    ceil_tau_Y: int,
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
    quad_tol_bits: int = 160,
    use_three_zone: bool = True,
    n_panels: int = 16,
    zone1_ratio: int = 12,
) -> Dict[str, arb]:
    """Separately evaluate `S_same(Y)`, `S_different(Y)`, and `Sigma_off(Y; 2)` on a point or
    fixed-cutoff interval ball `Y_arb`:
      - `S_same_Y`: direct 1D quadrature over same-chain `j != k` pairs (`evaluate_same_and_chain_diag_1d_arb`);
      - `S_different_Y`: direct distinct-chain bilinear evaluation `W_int(Y) - D_chain(Y)` where
        `W_int(Y) = ||U_Y^{int}||_Y^2 - 4*D_tilde_{Omega_2^{int}}(Y)` and `D_chain(Y)` is the
        chain-diagonal integral;
      - `Sigma_off_p2`: inherited `F_int_T(Y; {2}) - diag_int_T(Y; {2})` from
        `evaluate_interior_paired_matrix_free_arb` (incorporating `X_self` and `diag_int_T`).
    """
    is_interval_ball = bool(Y_arb.rad() > arb(0))
    eff_tol = min(quad_tol_bits, 110) if is_interval_ball else quad_tol_bits
    mf_int = evaluate_interior_paired_matrix_free_arb(
        Y_arb,
        T_y,
        D0_eff,
        ceil_tau_Y,
        (2,),
        selberg_table,
        prec_bits=prec_bits,
        quad_tol_bits=eff_tol,
        use_three_zone=use_three_zone,
        n_panels_override=n_panels,
        zone1_ratio_threshold=zone1_ratio,
    )
    eff_panels = n_panels if use_three_zone else max(1, n_panels if n_panels > 1 else 4)
    ch_1d = evaluate_same_and_chain_diag_1d_arb(
        Y_arb,
        T_y,
        D0_eff,
        selberg_table,
        prec_bits=prec_bits,
        quad_tol_bits=eff_tol,
        n_panels=eff_panels,
    )
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        w_int = mf_int["V2_int_T"] - arb(4) * mf_int["D_tilde_omega_S"]
        s_same = ch_1d["S_same"]
        s_diff = +(w_int - ch_1d["D_chain"])
        sigma_off = mf_int["offdiag_int_T"]
        recon = +(s_same + s_diff)
        return {
            "F_int_T_p2": mf_int["F_int_T"],
            "Sigma_diag_p2": mf_int["diag_int_T"],
            "Sigma_off_p2": sigma_off,
            "S_same_Y": s_same,
            "S_different_Y": s_diff,
            "D_chain_Y": ch_1d["D_chain"],
            "reconstructed_Sigma_off": recon,
            "same_input_reconstruction_residual": +(recon - sigma_off),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 2. Section 1: Endpoint Contradiction, Premise Table, & Window-Base Analysis
# ---------------------------------------------------------------------------


def build_tc063_premise_and_dependency_table() -> List[Dict[str, Any]]:
    """Return the complete declaration-level premise table from `S_different(Y)` to the closing
    pole contradiction on `riemannZeta` (`Prompt §2`).
    """
    return [
        {
            "premise_id": "TC063-PREM-01-DISTINCT-ODD-CHAIN-BOUND",
            "stage": "Stage 0 (Open Arithmetic Target)",
            "statement": (
                "forall eta > 0, exists a_eta, b_eta >= 0, 0 < kappa_eta <= 2, Y_eta >= 2: "
                "forall real Y >= Y_eta, S_different(Y) <= a_eta * Y^eta + b_eta * (log Y)^(2 - kappa_eta) * D_tilde(Y)"
            ),
            "declaration_location": (
                "formal/RiemannScope/DyadicChainCorrelationRegularity.lean::canonicalDifferentOddChainSumS "
                "(MixedCovarianceClosureHypothesis)"
            ),
            "status": "OPEN",
            "gap_kind": "MISSING_MATHEMATICS",
        },
        {
            "premise_id": "TC063-PREM-02-SAME-CHAIN-ABSORPTION-AND-OFFDIAG-EQUIVALENCE",
            "stage": "Stage 1A (Exact Dyadic-Chain & Interior Equivalences)",
            "statement": (
                "Sigma_off(Y; 2) = S_same(Y) + S_different(Y), |S_same(Y)| <= (L(T)-1)*(2*C_psi + 8*C_g) "
                "<= C_same*(1 + log Y) for all real Y >= 2, and H(S_different, D_tilde) <-> H(Sigma_off(.; 2), D_tilde) "
                "<-> H(F_int_T(.; {2}), D_tilde) <-> H(F_{<=T}, D_tilde) <-> H(F, D_tilde) <-> H(J, D_tilde)"
            ),
            "declaration_location": (
                "formal/RiemannScope/DyadicChainCorrelationRegularity.lean::"
                "exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063, "
                "uniform_same_chain_hilbert_bound_and_closure_transfer_tc063; "
                "formal/RiemannScope/JointPrimeDilationSignedRemainder.lean::"
                "two_sided_interior_diag_bound_and_offdiag_equivalence_tc062r"
            ),
            "status": "PROVED_IN_LEAN",
            "gap_kind": "NONE",
        },
        {
            "premise_id": "TC063-PREM-03-ROUTE-D-FINITE-HORIZON-CONTRACTION-ALGEBRA",
            "stage": "Stage 1B (Conditional Route D Contraction Schema)",
            "statement": (
                "Given H(S_different, D_tilde) and analytic inputs P04..P07 below, "
                "forall eps > 0, exists C_eps >= 0, forall real Z >= 1, canonicalLiouvilleEnergyE(Z) <= C_eps * Z^eps"
            ),
            "declaration_location": (
                "formal/RiemannScope/DyadicChainCorrelationRegularity.lean::"
                "uniform_same_chain_hilbert_bound_and_closure_transfer_tc063; "
                "formal/RiemannScope/MixedArithmeticCovariance.lean::"
                "mixed_covariance_hypothesis_route_d_closure_transfer_tc061"
            ),
            "status": "PROVED_IN_LEAN",
            "gap_kind": "NONE_FOR_TRANSFER_IMPLICATION",
        },
        {
            "premise_id": "TC063-PREM-04-GLOBAL-LINEAR-ENERGY-ENVELOPE",
            "stage": "Stage 1B Input 1 (Global Linear Energy Majorant)",
            "statement": (
                "forall real Z >= 1, E(Z) = ||Q_{lambda, T(Z)}||_Z^2 <= M_lin * Z "
                "with M_lin = (tau - 1) * (1/2 + 2*(3/(2*e))^(3/2))^2 approx 9.2030868"
            ),
            "declaration_location": (
                "docs/reviews/TC_056_PRIME_CHAIN_CONTRACTION.md (Prop. 2.1); "
                "tc/coupled_scale_energy_bootstrap.py::verify_global_linear_energy_bound_arb"
            ),
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_kind": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-05-PRIME-POWER-DIRICHLET-WEIGHT-FINITENESS",
            "stage": "Stage 1B Input 2 (Weighted Prime-Power Mass)",
            "statement": (
                "forall delta > 0, sum_{p^k <= floor(Y)} (log p)^2 / (p^k)^(1 + delta) <= zeta''(1 + delta) < infty"
            ),
            "declaration_location": (
                "docs/reviews/TC_057_COUPLED_ARITHMETIC_SCALE_ENERGY_BOOTSTRAP.md (§5); "
                "docs/reviews/TC_059_POWER_LIFT_AND_PRIMITIVE_CORRELATION.md (§2)"
            ),
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_kind": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-06-SHIFTED-DIAGONAL-ENVELOPE-CUTOFF-BOUND",
            "stage": "Stage 1B Input 3 (Shifted Prime-Power Diagonal Comparison)",
            "statement": (
                "forall real Y >= Y_diag, D_tilde(Y) <= (2 / (log Y)^2) * sum_{p^k <= floor(Y)} "
                "((log p)^2 / p^k) * E_sup(Y / p^k) + C_cut (including Zone 1 cutoff perturbation)"
            ),
            "declaration_location": (
                "docs/reviews/TC_057_COUPLED_ARITHMETIC_SCALE_ENERGY_BOOTSTRAP.md (Theorem 6.1); "
                "tc/coupled_scale_energy_bootstrap.py; tc/mixed_arithmetic_covariance.py"
            ),
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_kind": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-07-KNOWN-COMPENSATED-PART-HORIZON-CONTRACTION",
            "stage": "Stage 1B Input 4 (Known Selberg/Drift Part ||A_Y||_Y^2 Contraction)",
            "statement": (
                "forall R >= Y >= Y_diag, ||A_Y||_Y^2 <= a_known * Y^(eps/4) + "
                "(B_drift / (log Y)^kappa_d) * G_eps(R) * Y^eps (building on Lean Abel/drift Theorem in TC-060)"
            ),
            "declaration_location": (
                "formal/RiemannScope/SignedDilationArithmeticEnergy.lean::"
                "second_order_drift_abel_and_small_divisor_contraction_tc060 (Abel/drift core in Lean); "
                "tc/signed_dilation_arithmetic_energy.py (assembled ||A_Y||_Y^2 bound outside Lean)"
            ),
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_kind": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-08-FINITE-TO-INFINITE-OBSERVABLE-CONVERGENCE",
            "stage": "Stage 2 (Infinite Observable Tail Convergence)",
            "statement": (
                "||Q_{lambda, infty} - Q_{lambda, T(Y)}||_Y <= B_tau = (tau^(5/2) * sqrt(log tau)) / 2 "
                "for all real Y >= 1, giving (forall eps > 0, ||Q_{lambda, T(Y)}||_Y^2 <= C_T * Y^eps) "
                "<-> (forall eps > 0, ||Q_{lambda, infty}||_Y^2 <= C_inf * Y^eps)"
            ),
            "declaration_location": (
                "docs/reviews/TC_058_SIMULTANEOUS_COMPATIBILITY_AND_COMBINED_ENERGY.md (§3); "
                "tc/simultaneous_compatibility_combined_energy.py (tail cap outside Lean); "
                "formal/RiemannScope/LiouvilleSquareDilation.lean#L7530-L7539 (bilateral transfer algebra in Lean)"
            ),
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_kind": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-09-WEIGHTED-NORM-AND-MELLIN-HOLOMORPHY-BRIDGE",
            "stage": "Stage 3 (Mellin Transform Identity & Holomorphic Extension)",
            "statement": (
                "Subpower window growth E_inf(Y) <<_eps Y^eps implies M_Q(w) = int_0^infty Q_{lambda, infty}(X) X^{-w} dX/X "
                "= (1/2)*Gamma(5/4 - w/2)*zeta(1 + 2*w)/zeta(1/2 + w) extends holomorphically to 0 < Re(w) < 5/2, "
                "hence L_lambda(z) = zeta(2*z)/zeta(z) extends holomorphically to x = Re(z) > 1/2"
            ),
            "declaration_location": (
                "docs/reviews/TC_LIOUVILLE_SQUARE_DILATION.md (Proposition 3.1); "
                "tc/liouville_square_dilation.py::verify_mellin_identity_and_analytic_bridge"
            ),
            "status": "PROVED_ANALYTICALLY_OUTSIDE_LEAN",
            "gap_kind": "MISSING_LEAN_FORMALIZATION_ONLY",
        },
        {
            "premise_id": "TC063-PREM-10-ACTUAL-ZETA-POLE-CONTRADICTION-AND-REFLECTION",
            "stage": "Stage 4 (Closing Pole Contradiction & Reflection on Actual riemannZeta)",
            "statement": (
                "On actual Mathlib riemannZeta (z = x + i*y): (1) L_lambda(z)*zeta(z) = zeta(2*z) != 0 on x > 1; "
                "(2) at trivial zeros -2*(n+1), both zeta(-2*(n+1)) = 0 and zeta(-4*(n+1)) = 0; "
                "(3) if F_hol continues zeta(2*z)/zeta(z) without poles to x > 1/2 (zeta(z)*F_hol(z) = zeta(2*z) "
                "for x > 1/2, z != 1), then zeta(x + i*y) != 0 for 1/2 < x < 1 (0 = zeta(rho)*F_hol(rho) = zeta(2*rho) != 0), "
                "and completedRiemannZeta(1 - z) = completedRiemannZeta(z) reflects 0 < x < 1/2 to 1/2 < 1 - x < 1, "
                "forcing x = 1/2 for every critical-strip zero"
            ),
            "declaration_location": (
                "formal/RiemannScope/DyadicChainCorrelationRegularity.lean::"
                "liouville_dirichlet_ratio_pole_contradiction_and_reflection_tc063"
            ),
            "status": "PROVED_IN_LEAN",
            "gap_kind": "NONE",
        },
    ]


def verify_section_1_protocols_endpoint_and_premise_chain(
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Verify immutability of all 3 frozen protocols (`TC-061`, `TC-062`, `TC-063`) + preserved
    `TC-062` `885`-ball artifact, and certify in 256-bit Arb/Acb:
      1. `zeta(z) * L_lambda(z) = zeta(2*z) != 0` on `x > 1` (`z = 3/2 + 2*i`, `z = 2 + 5*i`);
      2. Simultaneous trivial-zero vanishing `zeta(-2*n) = 0` and `zeta(-4*n) = 0` (`n in {1, 2, 3}`);
      3. Functional-equation reflection `completed_xi(1 - z) = completed_xi(z)` on `0 < x < 1/2`;
      4. Generic window-base `b > 1` (`b in {2, 3, tau}`) validity of the same-chain Hilbert bound.
    """
    chk_61 = verify_frozen_protocol_immutability()
    chk_62 = verify_frozen_tc062_protocol_immutability()
    chk_63 = verify_frozen_tc063_protocol_immutability()

    tc062_bytes = JOINT_PRIME_DILATION_ARTIFACT_PATH.read_bytes().replace(b"\r\n", b"\n")
    tc062_sha = hashlib.sha256(tc062_bytes).hexdigest()
    tc062_obj = json.loads(tc062_bytes.decode("utf-8"))
    tc062_balls = tc062_obj["serialized_arb_self_check"]["total_certified_arb_balls_checked"]
    tc062_preserved_ok = bool(
        tc062_sha == EXPECTED_TC062_ARTIFACT_SHA256
        and tc062_balls == 885
        and tc062_obj["provenance"]["numerical_producing_git_commit"]
        == PRESERVED_TC062R_PRODUCING_COMMIT
    )

    tc061_bytes = MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH.read_bytes().replace(b"\r\n", b"\n")
    tc061_sha = hashlib.sha256(tc061_bytes).hexdigest()
    tc061_obj = json.loads(tc061_bytes.decode("utf-8"))
    tc061_balls = tc061_obj["serialized_arb_self_check"]["total_certified_arb_balls_checked"]
    tc061_preserved_ok = bool(
        tc061_sha == EXPECTED_TC061_ARTIFACT_SHA256 and tc061_balls == 3208
    )

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        half_tau = tau / arb(2)

        # 1. Dirichlet product zeta(z)*L_lambda(z) = zeta(2*z) on x > 1:
        dirichlet_rows: List[Dict[str, Any]] = []
        dirichlet_ok = True
        N_dir = 4000
        for x_frac, y_int in ((Fraction(5, 2), 2), (Fraction(3, 1), 5)):
            x_b = _frac_to_arb(x_frac)
            y_b = arb(y_int)
            z_c = acb(x_b, y_b)
            z_2 = acb(arb(2)) * z_c
            zeta_z = z_c.zeta()
            zeta_2z = z_2.zeta()
            part_sum = acb(0)
            for n in range(1, N_dir + 1):
                part_sum += acb(liouville_lambda_int(n)) * (acb(n) ** (-z_c))
            # Tail |sum_{n > N} lambda(n) n^{-z}| <= int_N^infty t^{-x} dt = N^{1 - x} / (x - 1):
            tail_rad = ((arb(N_dir) ** (arb(1) - x_b)) / (x_b - arb(1))).upper()
            L_encl = acb(part_sum.real + arb(0, tail_rad), part_sum.imag + arb(0, tail_rad))
            prod_diff = zeta_z * L_encl - zeta_2z
            z2_abs = abs(zeta_2z)
            row_ok = bool(
                arb(0) in prod_diff.real
                and arb(0) in prod_diff.imag
                and z2_abs > arb("0.1")
            )
            dirichlet_ok = dirichlet_ok and row_ok
            dirichlet_rows.append(
                {
                    "x": f"{x_frac.numerator}/{x_frac.denominator}",
                    "y": y_int,
                    "partial_sum_cutoff_N": N_dir,
                    "abs_zeta_2z": serialize_arb_certified(z2_abs),
                    "product_residual_abs": serialize_arb_certified(abs(prod_diff)),
                    "zeta_2z_certified_nonzero": bool(z2_abs > arb(0)),
                    "verified": row_ok,
                }
            )

        # 2. Trivial-zero simultaneous vanishing at z = -2*n (n = 1, 2, 3):
        triv_rows: List[Dict[str, Any]] = []
        triv_ok = True
        for n_triv in (1, 2, 3):
            z_tr = acb(-2 * n_triv, 0)
            z_2tr = acb(-4 * n_triv, 0)
            v1 = z_tr.zeta()
            v2 = z_2tr.zeta()
            ok_t = bool(
                arb(0) in v1.real
                and arb(0) in v1.imag
                and abs(v1) < arb("1e-70")
                and arb(0) in v2.real
                and arb(0) in v2.imag
                and abs(v2) < arb("1e-70")
            )
            triv_ok = triv_ok and ok_t
            triv_rows.append(
                {
                    "n": n_triv,
                    "trivial_zero_z": -2 * n_triv,
                    "doubled_point_2z": -4 * n_triv,
                    "abs_zeta_z": serialize_arb_certified(abs(v1)),
                    "abs_zeta_2z": serialize_arb_certified(abs(v2)),
                    "both_numerator_and_denominator_vanish": ok_t,
                }
            )

        # 3. Completed zeta reflection Xi(1 - z) = Xi(z) using tau/2 (= half-turn):
        def _completed_xi_tau(z_in: acb) -> acb:
            return (
                acb(arb(1) / arb(2))
                * z_in
                * (z_in - acb(1))
                * (acb(half_tau) ** (-z_in / acb(2)))
                * (z_in / acb(2)).gamma()
                * z_in.zeta()
            )

        refl_rows: List[Dict[str, Any]] = []
        refl_ok = True
        for x_q, y_i in ((Fraction(1, 4), 3), (Fraction(3, 10), 14)):
            z_left = acb(_frac_to_arb(x_q), arb(y_i))
            z_right = acb(1) - z_left
            xi_l = _completed_xi_tau(z_left)
            xi_r = _completed_xi_tau(z_right)
            diff_xi = abs(xi_l - xi_r)
            r_ok = bool(diff_xi < arb("1e-65"))
            refl_ok = refl_ok and r_ok
            refl_rows.append(
                {
                    "left_strip_x": f"{x_q.numerator}/{x_q.denominator}",
                    "y": y_i,
                    "reflected_right_strip_x": f"{(1 - x_q).numerator}/{(1 - x_q).denominator}",
                    "completed_xi_reflection_abs_diff": serialize_arb_certified(diff_xi),
                    "verified": r_ok,
                }
            )

        # 4. Generic window-base b > 1 check for same-chain Hilbert bound at Y = 16 (T = 32):
        tbl_16 = compute_selberg_centered_remainder_table_fast_arb(80, prec_bits=prec_bits + 32)
        vecs_16 = compute_complete_core_s_Y_and_beta_Y_arb(32, 2, tbl_16["R_osc"], prec_bits=prec_bits)
        b_16 = [arb(0)] + [
            arb(liouville_lambda_int(n)) * vecs_16["beta_Y"][n] for n in range(1, 33)
        ]
        c_div_32 = [arb(0)] * 33
        for qp, ae in prime_power_pairs_up_to(32):
            qa = qp ** ae
            lg2q = arb(qp).log() ** 2
            for mult in range(qa, 33, qa):
                c_div_32[mult] += lg2q

        base_rows: List[Dict[str, Any]] = []
        base_ok = True
        for b_label, b_val in (("2", arb(2)), ("3", arb(3)), ("tau", tau)):
            lg_b = b_val.log()
            tol_b = arb(2) ** (-190)

            def _gram_base_b(m_i: int, n_i: int, r_pow: int, _lgb: arb = lg_b) -> arb:
                y_c = acb(16)
                lgy_c = acb(arb(16).log())

                def _cb(u_v: acb, _an: bool) -> acb:
                    lgx = lgy_c + u_v
                    if _an and not bool(lgx.real > arb(1) / arb(2)):
                        nb = arb("nan")
                        return acb(nb, nb)
                    xv = y_c * u_v.exp()
                    xv2 = xv * xv
                    xv5 = (xv ** acb(5))
                    pm = (acb(m_i) ** (-3)) * (-xv2 / acb(m_i * m_i)).exp()
                    pn = (acb(n_i) ** (-3)) * (-xv2 / acb(n_i * n_i)).exp()
                    num = xv5 * pm * pn
                    return num / (lgx ** r_pow) if r_pow > 0 else num

                return acb.integral(_cb, acb(0), acb(_lgb), rel_tol=tol_b, abs_tol=tol_b).real

            # Compute S_same_{16, b} and local Hilbert bound (L(32) - 1 = 2):
            s_same_b = arb(0)
            for u in odd_chain_parts_O_T(32):
                ju = dyadic_chain_exponents_J_u(u, 32)
                for j1 in ju:
                    for j2 in ju:
                        if j1 == j2:
                            continue
                        m1, n1 = (4 ** j1) * u, (4 ** j2) * u
                        d_val = arb(0)
                        for e1, m_s in ((1, m1), (-1, 2 * m1)):
                            for e2, n_s in ((1, n1), (-1, 2 * n1)):
                                g0 = _gram_base_b(m_s, n_s, 0)
                                g2 = _gram_base_b(m_s, n_s, 2)
                                g4 = _gram_base_b(m_s, n_s, 4)
                                h_mn = (
                                    g0
                                    - (b_16[m_s] + b_16[n_s] + arb(4) * c_div_32[math.gcd(m_s, n_s)]) * g2
                                    + (b_16[m_s] * b_16[n_s]) * g4
                                )
                                d_val += arb(e1 * e2) * h_mn
                        s_same_b += d_val

            psi_sum_b = arb(0)
            g2_sum_b = arb(0)
            for n_k in range(1, 33):
                g0k = _gram_base_b(n_k, n_k, 0)
                g2k = _gram_base_b(n_k, n_k, 2)
                g4k = _gram_base_b(n_k, n_k, 4)
                psi_sum_b += g0k - arb(2) * b_16[n_k] * g2k + (b_16[n_k] ** 2) * g4k
                g2_sum_b += (arb(n_k).log() ** 2) * g2k
            hilb_b = arb(2) * (arb(2) * psi_sum_b + arb(8) * g2_sum_b)
            margin_b = abs(s_same_b) - hilb_b
            b_row_ok = bool(margin_b < arb(0))
            base_ok = base_ok and b_row_ok
            base_rows.append(
                {
                    "window_base_label": b_label,
                    "Y": 16,
                    "T_Y": 32,
                    "L_T": 3,
                    "S_same_base_b": serialize_arb_certified(s_same_b),
                    "hilbert_bound_base_b": serialize_arb_certified(hilb_b),
                    "abs_S_same_minus_hilbert_bound": serialize_arb_certified(margin_b),
                    "verified": b_row_ok,
                }
            )

        premise_table = build_tc063_premise_and_dependency_table()
        return {
            "epistemic_statuses": [
                "CONCRETE_ANALYTIC_IN_LEAN",
                "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "CERTIFIED_FINITE_OBSERVATION",
                "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            ],
            "section_epistemic_scope_note": (
                "Mixed formal/analytic/certified section: Dirichlet product L_lambda(z)*zeta(z) = zeta(2*z) != 0 "
                "on x > 1, trivial-zero double vanishing at -2*(n+1), and the closing pole contradiction + "
                "completed-zeta reflection on actual Mathlib riemannZeta are CONCRETE_ANALYTIC_IN_LEAN "
                "(Lean Theorem 1); finite-to-infinite Q_{lambda,infty} tail and Mellin holomorphy bridge are "
                "ANALYTIC_PROVED_OUTSIDE_LEAN; protocol immutability and 256-bit Arb/Acb evaluations across "
                "Dirichlet, trivial-zero, reflection, and generic window-base b > 1 checks are "
                "CERTIFIED_FINITE_OBSERVATION; TC063-PREM-01 (distinct-chain bound on S_different) remains "
                "OPEN_CONJECTURE_OR_FAILED_CANDIDATE."
            ),
            "component_epistemic_map": {
                "actual_riemannZeta_dirichlet_pole_contradiction_and_reflection": "CONCRETE_ANALYTIC_IN_LEAN",
                "route_d_analytic_inputs_and_mellin_holomorphy_bridge": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "frozen_protocols_and_256bit_endpoint_base_checks": "CERTIFIED_FINITE_OBSERVATION",
                "distinct_odd_chain_signed_bound_target": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            },
            "lean_theorems": [
                "liouville_dirichlet_ratio_pole_contradiction_and_reflection_tc063",
            ],
            "preserved_tc061_protocol_immutability": {
                k: v for k, v in chk_61.items() if k != "protocol_object"
            },
            "preserved_tc062_protocol_immutability": {
                k: v for k, v in chk_62.items() if k != "protocol_object"
            },
            "frozen_tc063_protocol_immutability": {
                k: v for k, v in chk_63.items() if k != "protocol_object"
            },
            "preserved_tc062_artifact_integrity": {
                "artifact_path": "data/tc_joint_prime_dilation_signed_remainder.json",
                "sha256_lf": tc062_sha,
                "total_certified_arb_balls": tc062_balls,
                "numerical_producing_git_commit": tc062_obj["provenance"][
                    "numerical_producing_git_commit"
                ],
                "verified": tc062_preserved_ok,
            },
            "preserved_tc061_artifact_integrity": {
                "artifact_path": "data/tc_mixed_arithmetic_covariance.json",
                "sha256_lf": tc061_sha,
                "total_certified_arb_balls": tc061_balls,
                "verified": tc061_preserved_ok,
            },
            "tc_compatibility_principle_and_window_base_scope": {
                "common_arithmetic_object": (
                    "Single Liouville-Gaussian observable Q_{lambda, infty}(X) = sum_{n>=1} lambda(n)*phi_n(X) "
                    "encoding the multiplicative square-divisor relation (1 * lambda)(n) = 1_{square}(n) "
                    "(L_lambda(z)*zeta(z) = zeta(2*z))."
                ),
                "compatibility_law": (
                    "Simultaneous compatibility of 2-adic parity alternation lambda(2*m) = -lambda(m), "
                    "4-adic invariance lambda(4^j*u) = lambda(u), and all-prime Selberg second-order "
                    "compensation 2*P_Y - B_Y = Q_Y + A_Y."
                ),
                "constrained_quantity": (
                    "Subpower window energy E(Y) <= C_eps * Y^eps for all eps > 0, equivalently holomorphic "
                    "regularity of L_lambda(x + i*y) on x > 1/2 (strictly WITHOUT constructing an exact "
                    "zero-independent grade-invariant functional or positive spectral realization)."
                ),
                "window_base_dependence": (
                    "Every finite-window Gram identity, dyadic-chain split, same-chain Hilbert bound, "
                    "partition [1, infty) = cup_{k>=0} [b^k, b^{k+1}), Route D contraction, and Mellin bridge "
                    "holds for ANY real window base b > 1; fixing b = tau selects canonical rational-integer "
                    "grade tiling [tau^k, tau^{k+1}] (k in Z subset A_R) and Tate character normalization."
                ),
            },
            "premise_and_dependency_table": premise_table,
            "dirichlet_ratio_nonvanishing_checks": dirichlet_rows,
            "trivial_zero_double_vanishing_checks": triv_rows,
            "functional_equation_reflection_checks": refl_rows,
            "generic_window_base_hilbert_checks": base_rows,
            "all_section_1_checks_pass": bool(
                chk_61["verified"]
                and chk_62["verified"]
                and chk_63["verified"]
                and tc062_preserved_ok
                and tc061_preserved_ok
                and dirichlet_ok
                and triv_ok
                and refl_ok
                and base_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 3. Section 2: Exact Odd-Part Decomposition & Small-T / Direct Validations
# ---------------------------------------------------------------------------


def verify_odd_part_decomposition_exhaustive_exact() -> Dict[str, Any]:
    """Exhaustively verify in exact `Fraction` arithmetic across `T in (0, 1, 2, 3, 5, 6, 7, 8, 14,
    15, 16, 31, 32, 48)`:
      1. Empty (`T < 2`), singleton-only (`2 <= T < 8`), and multi-element (`T >= 8`) chain regimes;
      2. Bijection `(u, j) |-> 4^j * u` from `Sigma_{u in O(T)} J_u(T)` onto `I_2(T)` and exact
         ordered-pair partition `|I_2(T)|*(|I_2(T)| - 1) = N_same + N_different`;
      3. Generic ordered-pair reindexing on non-multiplicative `a(n) = n^2 - 3*n + 1` and
         non-symmetric `H(m, n) = (2*m + 5*n)/(m + n + 1)`;
      4. Liouville specialization `lambda(4^j * u) = lambda(u)` giving `Sigma_off = S_same + S_different`.
    """
    def _a_nonmult(n: int) -> Fraction:
        return Fraction(n * n - 3 * n + 1, 1)

    def _H_nonsym(m: int, n: int) -> Fraction:
        return Fraction(2 * m + 5 * n, m + n + 1)

    cutoffs = (0, 1, 2, 3, 5, 6, 7, 8, 14, 15, 16, 31, 32, 48)
    rows: List[Dict[str, Any]] = []
    all_ok = True
    for T_c in cutoffs:
        i2 = interior_two_adic_anchors(T_c)
        o_t = odd_chain_parts_O_T(T_c)
        l_t = max_dyadic_chain_length_L(T_c)
        generated_pairs = [(u, j, (4 ** j) * u) for u in o_t for j in dyadic_chain_exponents_J_u(u, T_c)]
        generated_m = [m_v for (_u, _j, m_v) in generated_pairs]
        bij_ok = bool(len(generated_m) == len(set(generated_m)) and sorted(generated_m) == i2)
        empty_ok = bool((len(o_t) == 0) == (T_c < 2))
        singleton_all_ok = bool(all(0 in dyadic_chain_exponents_J_u(u, T_c) for u in o_t))
        singleton_rule_ok = bool(
            all(
                (len(dyadic_chain_exponents_J_u(u, T_c)) == 1) == (T_c < 8 * u)
                for u in o_t
            )
        )

        n_same_pairs = sum(
            len(dyadic_chain_exponents_J_u(u, T_c)) * (len(dyadic_chain_exponents_J_u(u, T_c)) - 1)
            for u in o_t
        )
        n_diff_pairs = sum(
            len(dyadic_chain_exponents_J_u(u, T_c)) * len(dyadic_chain_exponents_J_u(v, T_c))
            for u in o_t
            for v in o_t
            if u != v
        )
        pair_count_ok = bool(len(i2) * max(0, len(i2) - 1) == n_same_pairs + n_diff_pairs)

        # Generic non-multiplicative sequence + non-symmetric H:
        gen_lhs = Fraction(0, 1)
        for m in i2:
            for n in i2:
                if m != n:
                    gen_lhs += _a_nonmult(m) * _a_nonmult(n) * _H_nonsym(m, n)
        gen_same = Fraction(0, 1)
        gen_diff = Fraction(0, 1)
        for u in o_t:
            ju = dyadic_chain_exponents_J_u(u, T_c)
            for j in ju:
                for k in ju:
                    if j != k:
                        m_jk, n_jk = (4 ** j) * u, (4 ** k) * u
                        gen_same += _a_nonmult(m_jk) * _a_nonmult(n_jk) * _H_nonsym(m_jk, n_jk)
            for v in o_t:
                if u != v:
                    jv = dyadic_chain_exponents_J_u(v, T_c)
                    for j in ju:
                        for k in jv:
                            m_jk, n_jk = (4 ** j) * u, (4 ** k) * v
                            gen_diff += _a_nonmult(m_jk) * _a_nonmult(n_jk) * _H_nonsym(m_jk, n_jk)
        gen_ok = bool(gen_lhs == gen_same + gen_diff)

        # Liouville sequence:
        lam_lhs = Fraction(0, 1)
        for m in i2:
            lm = liouville_lambda_int(m)
            for n in i2:
                if m != n:
                    lam_lhs += Fraction(lm * liouville_lambda_int(n), 1) * _H_nonsym(m, n)
        lam_same = Fraction(0, 1)
        lam_diff = Fraction(0, 1)
        for u in o_t:
            lu = liouville_lambda_int(u)
            ju = dyadic_chain_exponents_J_u(u, T_c)
            for j in ju:
                assert liouville_lambda_int((4 ** j) * u) == lu
                for k in ju:
                    if j != k:
                        lam_same += _H_nonsym((4 ** j) * u, (4 ** k) * u)
            for v in o_t:
                if u != v:
                    lv = liouville_lambda_int(v)
                    jv = dyadic_chain_exponents_J_u(v, T_c)
                    kcal_uv = sum(
                        (_H_nonsym((4 ** j) * u, (4 ** k) * v) for j in ju for k in jv),
                        Fraction(0, 1),
                    )
                    lam_diff += Fraction(lu * lv, 1) * kcal_uv
        lam_ok = bool(
            lam_lhs == lam_same + lam_diff and (T_c >= 8 or lam_same == Fraction(0, 1))
        )

        row_ok = bool(
            bij_ok and empty_ok and singleton_all_ok and singleton_rule_ok and pair_count_ok and gen_ok and lam_ok
        )
        all_ok = all_ok and row_ok
        rows.append(
            {
                "T": T_c,
                "anchor_count_I2": len(i2),
                "odd_chain_count_O_T": len(o_t),
                "max_chain_length_L_T": l_t,
                "ordered_same_chain_pairs": n_same_pairs,
                "ordered_different_chain_pairs": n_diff_pairs,
                "generic_nonmult_reindexing_exact": gen_ok,
                "liouville_chain_split_exact": lam_ok,
                "verified": row_ok,
            }
        )

    return {
        "cutoffs_tested": list(cutoffs),
        "sequence_generic": "a(n) = n^2 - 3*n + 1 (non-multiplicative)",
        "kernel_generic": "H(m, n) = (2*m + 5*n)/(m + n + 1) (non-symmetric)",
        "rows": rows,
        "verified": all_ok,
    }


def verify_section_2_odd_part_decomposition_and_cross_checks(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Verify exact odd-part decomposition (`§4`) both combinatorially on exhaustive small `T` and
    numerically in 256-bit Arb on `Y in {2, 4, 8, 16, 32, 64}` comparing 2D `Hcal_Y` double sums
    against separate 1D quadrature evaluators (`ALGEBRAIC_CONSISTENCY_CHECK` vs
    `INDEPENDENT_DIRECT_NUMERICAL_VALIDATION`).
    """
    exact_chk = verify_odd_part_decomposition_exhaustive_exact()
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(500, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 400
        else selberg_table
    )

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        scale_rows: List[Dict[str, Any]] = []
        scales_ok = True
        s_same_16 = arb(0)
        s_same_64 = arb(0)

        for y_val in (2, 4, 8, 16, 32, 64):
            sp = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            cut = certify_exact_scale_cutoffs(sp, base_prec_bits=prec_bits)
            T_y = cut["T_Y"]
            D0_eff = cut["D0_eff"]
            Y_b = arb(y_val)
            Hcal = build_complete_signed_kernel_evaluator_small_T(
                Y_b, T_y, D0_eff, tbl, prec_bits=prec_bits
            )

            def _dH(m_i: int, n_i: int) -> arb:
                return Hcal(m_i, n_i) - Hcal(2 * m_i, n_i) - Hcal(m_i, 2 * n_i) + Hcal(2 * m_i, 2 * n_i)

            i2 = interior_two_adic_anchors(T_y)
            o_t = odd_chain_parts_O_T(T_y)
            sigma_off_2d = arb(0)
            for m in i2:
                lm = liouville_lambda_int(m)
                for n in i2:
                    if m != n:
                        sigma_off_2d += arb(lm * liouville_lambda_int(n)) * _dH(m, n)

            s_same_2d = arb(0)
            s_diff_2d = arb(0)
            for u in o_t:
                lu = liouville_lambda_int(u)
                ju = dyadic_chain_exponents_J_u(u, T_y)
                for j in ju:
                    for k in ju:
                        if j != k:
                            s_same_2d += _dH((4 ** j) * u, (4 ** k) * u)
                for v in o_t:
                    if u != v:
                        lv = liouville_lambda_int(v)
                        jv = dyadic_chain_exponents_J_u(v, T_y)
                        kcal_uv = arb(0)
                        for j in ju:
                            for k in jv:
                                kcal_uv += _dH((4 ** j) * u, (4 ** k) * v)
                        s_diff_2d += arb(lu * lv) * kcal_uv

            alg_2d_res = (s_same_2d + s_diff_2d) - sigma_off_2d

            # Separate 1D quadrature evaluation:
            mf_1d = evaluate_dyadic_chain_observables_matrix_free_arb(
                Y_b,
                T_y,
                D0_eff,
                cut["ceil_tau_Y"],
                tbl,
                prec_bits=prec_bits,
                quad_tol_bits=220,
                use_three_zone=False,
                n_panels=4,
            )
            ind_same_diff = mf_1d["S_same_Y"] - s_same_2d
            ind_diff_diff = mf_1d["S_different_Y"] - s_diff_2d
            ind_sig_diff = mf_1d["Sigma_off_p2"] - sigma_off_2d

            if y_val == 16:
                s_same_16 = mf_1d["S_same_Y"]
            elif y_val == 64:
                s_same_64 = mf_1d["S_same_Y"]

            row_ok = bool(
                arb(0) in alg_2d_res
                and abs(alg_2d_res) < arb("1e-52")
                and arb(0) in mf_1d["same_input_reconstruction_residual"]
                and abs(mf_1d["same_input_reconstruction_residual"]) < arb("1e-52")
                and arb(0) in ind_same_diff
                and abs(ind_same_diff) < arb("1e-50")
                and arb(0) in ind_diff_diff
                and abs(ind_diff_diff) < arb("1e-50")
                and arb(0) in ind_sig_diff
                and abs(ind_sig_diff) < arb("1e-50")
            )
            scales_ok = scales_ok and row_ok
            scale_rows.append(
                {
                    "Y": y_val,
                    "T_Y": T_y,
                    "D0_eff": D0_eff,
                    "anchor_count_I2": len(i2),
                    "odd_chain_count_O_T": len(o_t),
                    "max_chain_length_L_T": max_dyadic_chain_length_L(T_y),
                    "Sigma_off_2d_kernel": serialize_arb_certified(sigma_off_2d),
                    "S_same_2d_kernel": serialize_arb_certified(s_same_2d),
                    "S_different_2d_kernel": serialize_arb_certified(s_diff_2d),
                    "S_same_1d_quadrature": serialize_arb_certified(mf_1d["S_same_Y"]),
                    "S_different_1d_quadrature": serialize_arb_certified(mf_1d["S_different_Y"]),
                    "Sigma_off_1d_quadrature": serialize_arb_certified(mf_1d["Sigma_off_p2"]),
                    "algebraic_consistency_check_2d_residual": serialize_arb_certified(alg_2d_res),
                    "algebraic_consistency_check_1d_residual": serialize_arb_certified(
                        mf_1d["same_input_reconstruction_residual"]
                    ),
                    "independent_validation_S_same_1d_minus_2d": serialize_arb_certified(
                        ind_same_diff
                    ),
                    "independent_validation_S_different_1d_minus_2d": serialize_arb_certified(
                        ind_diff_diff
                    ),
                    "independent_validation_Sigma_off_1d_minus_2d": serialize_arb_certified(
                        ind_sig_diff
                    ),
                    "verified": row_ok,
                }
            )

        sign_flip_ok = bool(s_same_16 > arb(0) and s_same_64 < arb(0))
        return {
            "epistemic_statuses": [
                "UNCONDITIONAL_FINITE_ARITHMETIC",
                "CONCRETE_ANALYTIC_IN_LEAN",
                "CERTIFIED_FINITE_OBSERVATION",
            ],
            "section_epistemic_scope_note": (
                "Mixed finite-arithmetic/formal/certified section: unique m = 4^j * u odd-part "
                "bijection, empty/singleton chain rules, and generic ordered-pair reindexing are "
                "UNCONDITIONAL_FINITE_ARITHMETIC; Liouville parity invariance and complete-kernel "
                "Sigma_off(Y; 2) = S_same(Y) + S_different(Y) are CONCRETE_ANALYTIC_IN_LEAN "
                "(Lean Theorem 2); 256-bit Arb cross-checks separating same-input algebraic "
                "consistency checks from independent 1D-vs-2D validations (plus certified sign "
                "change S_same(16) > 0 > S_same(64)) are CERTIFIED_FINITE_OBSERVATION."
            ),
            "component_epistemic_map": {
                "exhaustive_small_T_odd_part_bijection_and_generic_reindexing": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "complete_kernel_dyadic_chain_offdiag_split": "CONCRETE_ANALYTIC_IN_LEAN",
                "small_scale_2d_vs_1d_independent_cross_checks_and_S_same_sign_flip": "CERTIFIED_FINITE_OBSERVATION",
            },
            "lean_theorems": [
                "exact_odd_part_bijection_and_dyadic_chain_offdiag_split_tc063",
            ],
            "exhaustive_exact_reindexing": exact_chk,
            "complete_kernel_cross_validation_rows": scale_rows,
            "S_same_sign_change_certified": {
                "Y_16_positive": bool(s_same_16 > arb(0)),
                "Y_64_negative": bool(s_same_64 < arb(0)),
                "verified": sign_flip_ok,
            },
            "all_section_2_checks_pass": bool(
                exact_chk["verified"] and scales_ok and sign_flip_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 4. Section 3: Uniform Same-Chain Bound, Feature Formula, & Matched Controls
# ---------------------------------------------------------------------------


def compute_uniform_same_chain_constants_arb(
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
) -> Dict[str, arb]:
    """Compute certified 256-bit Arb enclosures of the explicit Lean uniform constants `C_phi`,
    `C_beta`, `C_psi = 2*C_phi + 8*C_beta`, `C_g = 186*(tau - 1)`, and `C_same = 2*C_psi + 8*C_g`
    at `(actualSelbergConstantCLam, actualSquarePoleConstantCHalf)`.
    """
    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        c_lam = selberg_table["c_lambda"]
        c_half = selberg_table["c_half_lambda"]
        c_phi = (tau - arb(1)) * (arb(27) / arb(8) + arb(2) * (tau ** 4))
        b0 = (arb(81) / arb(16)) + arb(18) + arb(4) * (abs(c_lam) + abs(c_half))
        c_sm = arb(4) + abs(c_lam) + abs(c_half)
        c_beta = (
            arb(16) * (c_lam * c_lam) * c_phi
            + (b0 * b0) * (tau - arb(1)) * (tau ** 4)
            + arb(16) * ((arb(8) + abs(c_half)) ** 2) * c_phi * arb(18785)
            + arb(1024) * c_phi * (c_sm * c_sm)
        )
        c_psi = arb(2) * c_phi + arb(8) * c_beta
        c_g = arb(186) * (tau - arb(1))
        c_same = arb(2) * c_psi + arb(8) * c_g
        return {
            "c_lambda": +c_lam,
            "c_half": +c_half,
            "C_phi": +c_phi,
            "C_beta": +c_beta,
            "C_psi": +c_psi,
            "C_g": +c_g,
            "C_same": +c_same,
        }
    finally:
        flint_ctx.prec = saved


def evaluate_control_dyadic_chain_split_arb(
    Y_int: int,
    mode: str,
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Evaluate `(S_same, S_different, D_tilde)` for `mode in ('liouville', 'unsigned_1', 'a2',
    'a_3_5_7', 'hybrid_a2_liouville')`, recomputing each true control's own `z = 1` Laurent core
    and its own `p = 2` pair sign `eps_2 in {-1, +1}`, while keeping `hybrid_a2_liouville`
    explicitly labeled as a hybrid diagnostic (`a2` outer signs + unchanged Liouville `beta_Y`).
    """
    if mode not in ("liouville", "unsigned_1", "a2", "a_3_5_7", "hybrid_a2_liouville"):
        raise ValueError(f"Unsupported mode {mode!r}")

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        sp = ExactScaleSpec(str(Y_int), "exact_rational", Fraction(Y_int, 1))
        cut = certify_exact_scale_cutoffs(sp, base_prec_bits=prec_bits)
        T_y = cut["T_Y"]
        D0_eff = cut["D0_eff"]
        Y_b = arb(Y_int)
        use_3z = T_y >= 512
        q_tol = 160 if use_3z else 220
        n_pan = 16 if use_3z else 4

        rc_1d = evaluate_control_matched_point_arb(Y_int, mode, selberg_table, prec_bits=prec_bits)
        d_tilde_ctrl = rc_1d["D_tilde_Y"]
        lg_d_ctrl = rc_1d["log_Y_times_D_tilde"]

        if mode == "liouville":
            mf = evaluate_dyadic_chain_observables_matrix_free_arb(
                Y_b,
                T_y,
                D0_eff,
                cut["ceil_tau_Y"],
                selberg_table,
                prec_bits=prec_bits,
                quad_tol_bits=q_tol,
                use_three_zone=use_3z,
                n_panels=n_pan,
            )
            return {
                "T_Y": T_y,
                "D0_eff": D0_eff,
                "eps_2": -1,
                "is_hybrid_diagnostic": False,
                "exact_matched_core": True,
                "S_same": mf["S_same_Y"],
                "S_different": mf["S_different_Y"],
                "D_tilde": d_tilde_ctrl,
                "log_Y_times_D_tilde": lg_d_ctrl,
            }

        # Build control or hybrid b_vec on 1 <= n <= T_y and outer sign a_seq:
        if mode == "hybrid_a2_liouville":
            eps_2 = -1
            a_seq = [0] + [finite_prime_parity_aS_int(n, (2,)) for n in range(1, T_y + 1)]
            vecs_l = compute_complete_core_s_Y_and_beta_Y_arb(
                T_y, D0_eff, selberg_table["R_osc"], prec_bits=prec_bits + 32
            )
            b_vec = [arb(0)] + [
                arb(liouville_lambda_int(n)) * vecs_l["beta_Y"][n] for n in range(1, T_y + 1)
            ]
        else:
            prime_set: Tuple[int, ...] = (
                () if mode == "unsigned_1" else ((2,) if mode == "a2" else (3, 5, 7))
            )
            eps_2 = -1 if (2 in prime_set) else 1
            a_seq = [0] + [finite_prime_parity_aS_int(n, prime_set) for n in range(1, 2 * T_y + 1)]
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
                R_S[d_i] = cum_w - (arb(2) * d_arb * arb(d_i).log() + c0_S * d_arb)
            s_S = [arb(0)] * (T_y + 1)
            for d_i in range(D0_eff + 1, T_y):
                L_d = T_y // d_i
                wd = R_S[d_i]
                for q in range(1, L_d + 1):
                    term = wd * arb(a_seq[q])
                    if d_i * q <= T_y:
                        s_S[d_i * q] += term
                    if (d_i + 1) * q <= T_y:
                        s_S[(d_i + 1) * q] -= term
            b_vec = [arb(0)] + [
                arb(a_seq[n]) * (s_S[n] - arb(a_seq[n]) * (arb(n).log() ** 2))
                for n in range(1, T_y + 1)
            ]

        ch_1d = evaluate_same_and_chain_diag_1d_arb(
            Y_b,
            T_y,
            D0_eff,
            selberg_table,
            prec_bits=prec_bits,
            quad_tol_bits=q_tol,
            n_panels=n_pan,
            b_vec_override=b_vec,
            eps_2=eps_2,
        )

        # Evaluate W_int_ctrl = ||sum_{n in Omega_2^int} a_seq[n]*psi_{ctrl,n}||_Y^2 - 4*D_tilde_{ctrl,Omega_2^int}:
        work_prec = prec_bits + 32
        flint_ctx.prec = work_prec
        tau = _tau_arb()
        log_tau = tau.log()
        in_om = [False] * (T_y + 1)
        for m in interior_two_adic_anchors(T_y):
            in_om[m] = True
            in_om[2 * m] = True
        om_stations = [
            (k, acb(a_seq[k]), acb(b_vec[k]), acb(k) ** (-3), acb(-(arb(k * k) ** (-1))))
            for k in range(1, T_y + 1)
            if in_om[k]
        ]
        pp_om: List[Tuple[acb, List[Tuple[int, acb]]]] = []
        for qp, ae in prime_power_pairs_up_to(T_y):
            qa = qp ** ae
            hits = [(k, acb(a_seq[k])) for k in range(qa, T_y + 1, qa) if in_om[k]]
            if hits:
                pp_om.append((acb(arb(qp).log() ** 2), hits))

        Yc = acb(Y_b)
        lgYc = acb(Y_b.log())
        Yc_52 = Yc ** (acb(5) / acb(2))
        Yc_2 = Yc * Yc
        tol = arb(2) ** (-q_tol)
        w_int_acc = arb(0)
        for j_p in range(n_pan):
            u_lo = log_tau * arb(j_p) / arb(n_pan)
            u_hi = log_tau * arb(j_p + 1) / arb(n_pan)

            def _w_cb(u_v: acb, _an: bool) -> acb:
                lg = lgYc + u_v
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_v).exp()
                x2 = Yc_2 * (acb(2) * u_v).exp()
                ph = [acb(0)] * (T_y + 1)
                u_sum = acb(0)
                for k_i, a_c, b_k, inv_k3, neg_inv_k2 in om_stations:
                    pk_v = x52 * inv_k3 * (x2 * neg_inv_k2).exp()
                    ph[k_i] = pk_v
                    u_sum += a_c * (acb(1) - b_k * inv_lg2) * pk_v
                d_sum = acb(0)
                for lg2_c, h_list in pp_om:
                    s_p = acb(0)
                    for k_i, a_c in h_list:
                        s_p += a_c * ph[k_i]
                    d_sum += lg2_c * (s_p * s_p)
                return (u_sum * u_sum) - acb(4) * d_sum * inv_lg2

            w_int_acc += acb.integral(_w_cb, acb(u_lo), acb(u_hi), rel_tol=tol, abs_tol=tol).real

        flint_ctx.prec = prec_bits
        s_diff_ctrl = +((+w_int_acc) - ch_1d["D_chain"])
        return {
            "T_Y": T_y,
            "D0_eff": D0_eff,
            "eps_2": eps_2,
            "is_hybrid_diagnostic": bool(mode == "hybrid_a2_liouville"),
            "exact_matched_core": bool(mode != "hybrid_a2_liouville"),
            "S_same": ch_1d["S_same"],
            "S_different": s_diff_ctrl,
            "D_tilde": d_tilde_ctrl,
            "log_Y_times_D_tilde": lg_d_ctrl,
        }
    finally:
        flint_ctx.prec = saved


def verify_section_3_same_chain_bound_and_matched_controls(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Verify shifted-station disjointness, complete-kernel `<U_m, U_n>_Y - 4*<V_m, V_n>` feature
    identity (plus certified `m = n` discrepancy when dropping self-collisions), explicit uniform
    same-chain Hilbert bounds across `Y = 2..1024`, and matched control / hybrid `S_different`
    refutations across `Y = 16..512` (`Prompt §5 & §7`).
    """
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(9000, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 8300
        else selberg_table
    )

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        consts = compute_uniform_same_chain_constants_arb(tbl, prec_bits=prec_bits)
        c_psi = consts["C_psi"]
        c_g = consts["C_g"]
        c_same = consts["C_same"]

        # 1. Exhaustive shifted-station disjointness on I_2(180) and feature formula at Y in {4, 8, 16}:
        i2_180 = interior_two_adic_anchors(180)
        shifted_180 = {2 * m for m in i2_180}
        disj_ok = bool(len(set(i2_180) & shifted_180) == 0)
        for m in i2_180:
            for n in i2_180:
                if m != n:
                    if len({m, 2 * m} & {n, 2 * n}) != 0:
                        disj_ok = False

        feature_ok = True
        diag_self_collision_needed_ok = False
        feature_rows: List[Dict[str, Any]] = []
        for y_val in (4, 8, 16):
            sp = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            cut = certify_exact_scale_cutoffs(sp, base_prec_bits=prec_bits)
            T_y = cut["T_Y"]
            D0_eff = cut["D0_eff"]
            Y_b = arb(y_val)
            Hcal = build_complete_signed_kernel_evaluator_small_T(
                Y_b, T_y, D0_eff, tbl, prec_bits=prec_bits
            )
            vecs = compute_complete_core_s_Y_and_beta_Y_arb(
                T_y, D0_eff, tbl["R_osc"], prec_bits=prec_bits
            )
            b_arr = [arb(0)] + [
                arb(liouville_lambda_int(n)) * vecs["beta_Y"][n] for n in range(1, T_y + 1)
            ]
            c_div = [arb(0)] * (T_y + 1)
            for qp, ae in prime_power_pairs_up_to(T_y):
                qa = qp ** ae
                lg2q = arb(qp).log() ** 2
                for mult in range(qa, T_y + 1, qa):
                    c_div[mult] += lg2q

            def _uv_pair(m_i: int, n_i: int) -> arb:
                u_ip = arb(0)
                v_ip = arb(0)
                for e1, a_s in ((1, m_i), (-1, 2 * m_i)):
                    for e2, b_s in ((1, n_i), (-1, 2 * n_i)):
                        g0 = evaluate_window_gram_G_Y_r_arb(Y_b, a_s, b_s, 0, prec_bits=prec_bits)
                        g2 = evaluate_window_gram_G_Y_r_arb(Y_b, a_s, b_s, 2, prec_bits=prec_bits)
                        g4 = evaluate_window_gram_G_Y_r_arb(Y_b, a_s, b_s, 4, prec_bits=prec_bits)
                        u_ip += arb(e1 * e2) * (
                            g0 - (b_arr[a_s] + b_arr[b_s]) * g2 + (b_arr[a_s] * b_arr[b_s]) * g4
                        )
                        v_ip += arb(e1 * e2) * c_div[math.gcd(a_s, b_s)] * g2
                return u_ip - arb(4) * v_ip

            i2_y = interior_two_adic_anchors(T_y)
            max_off_err = arb(0)
            for m in i2_y:
                for n in i2_y:
                    d_direct = (
                        Hcal(m, n) - Hcal(2 * m, n) - Hcal(m, 2 * n) + Hcal(2 * m, 2 * n)
                    )
                    d_feat = _uv_pair(m, n)
                    diff_mn = d_feat - d_direct
                    if m != n:
                        err_abs = abs(diff_mn)
                        if bool(err_abs.upper() > max_off_err.upper()):
                            max_off_err = err_abs
                        if not (arb(0) in diff_mn and err_abs < arb("1e-50")):
                            feature_ok = False
                    elif y_val == 16 and m == 3:
                        # At m = 3, 2*m = 6 is composite (2 * 3), so c_self(6) = 2*(log 2)*(log 3) > 0,
                        # forcing <U_3, U_3> - 4*<V_3, V_3> != Delta Hcal_16(3, 3)!
                        diag_self_collision_needed_ok = bool(not (arb(0) in diff_mn))

            feature_rows.append(
                {
                    "Y": y_val,
                    "T_Y": T_y,
                    "distinct_anchor_pairs_checked": len(i2_y) * max(0, len(i2_y) - 1),
                    "max_distinct_anchor_feature_abs_error": serialize_arb_certified(max_off_err),
                    "verified": bool(max_off_err < arb("1e-50")),
                }
            )

        # 2. Certify uniform same-chain Hilbert bounds across Y in {2, 4, 8, 16, 32, 64, 128, 256, 512, 1024}:
        same_bound_rows: List[Dict[str, Any]] = []
        same_bounds_ok = True
        for y_val in (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024):
            sp = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            cut = certify_exact_scale_cutoffs(sp, base_prec_bits=prec_bits)
            T_y = cut["T_Y"]
            D0_eff = cut["D0_eff"]
            Y_b = arb(y_val)
            l_t = max_dyadic_chain_length_L(T_y)
            ch_res = evaluate_same_and_chain_diag_1d_arb(
                Y_b,
                T_y,
                D0_eff,
                tbl,
                prec_bits=prec_bits,
                quad_tol_bits=180 if T_y >= 512 else 220,
                n_panels=16 if T_y >= 512 else 4,
            )
            s_same = ch_res["S_same"]

            # Evaluate local station sums via fast 1D integral:
            vecs = compute_complete_core_s_Y_and_beta_Y_arb(
                T_y, D0_eff, tbl["R_osc"], prec_bits=prec_bits + 32
            )
            b_c = [acb(0)] + [
                acb(arb(liouville_lambda_int(n)) * vecs["beta_Y"][n]) for n in range(1, T_y + 1)
            ]
            lg_n_sq = [acb(0)] + [acb(arb(n).log() ** 2) for n in range(1, T_y + 1)]
            st_consts = [(k, acb(k) ** (-3), acb(-(arb(k * k) ** (-1)))) for k in range(1, T_y + 1)]
            Yc = acb(Y_b)
            lgYc = acb(Y_b.log())
            Yc_52 = Yc ** (acb(5) / acb(2))
            Yc_2 = Yc * Yc
            log_tau = _tau_arb().log()
            tol_s = arb(2) ** (-170)

            def _loc_sums_cb(u_v: acb, _an: bool) -> acb:
                lg = lgYc + u_v
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_v).exp()
                x2 = Yc_2 * (acb(2) * u_v).exp()
                s_psi = acb(0)
                s_g2 = acb(0)
                for k_i, inv_k3, neg_inv_k2 in st_consts:
                    pk_v = x52 * inv_k3 * (x2 * neg_inv_k2).exp()
                    pk_sq = pk_v * pk_v
                    psi_k = (acb(1) - b_c[k_i] * inv_lg2) * pk_v
                    s_psi += psi_k * psi_k
                    s_g2 += lg_n_sq[k_i] * pk_sq * inv_lg2
                # Pack s_psi in real and s_g2 in imag? No, u_v can be non-real during acb.integral!
                return s_psi + acb(0) * s_g2

            def _g2_sums_cb(u_v: acb, _an: bool) -> acb:
                lg = lgYc + u_v
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_v).exp()
                x2 = Yc_2 * (acb(2) * u_v).exp()
                s_g2 = acb(0)
                for k_i, inv_k3, neg_inv_k2 in st_consts:
                    pk_v = x52 * inv_k3 * (x2 * neg_inv_k2).exp()
                    s_g2 += lg_n_sq[k_i] * (pk_v * pk_v) * inv_lg2
                return s_g2

            sum_psi = acb.integral(_loc_sums_cb, acb(0), acb(log_tau), rel_tol=tol_s, abs_tol=tol_s).real
            sum_g2 = acb.integral(_g2_sums_cb, acb(0), acb(log_tau), rel_tol=tol_s, abs_tol=tol_s).real

            bound_local = arb(l_t - 1) * (arb(2) * sum_psi + arb(8) * sum_g2)
            bound_unif_L = arb(l_t - 1) * c_same
            bound_unif_log = c_same * (arb(1) + Y_b.log())

            m_loc = abs(s_same) - bound_local
            m_unif = abs(s_same) - bound_unif_log
            _, ok_psi = classify_arb_le_certificate(sum_psi, c_psi)
            _, ok_g2 = classify_arb_le_certificate(sum_g2, c_g)
            _, ok_loc = classify_arb_le_certificate(abs(s_same), bound_local)
            _, ok_l_log = classify_arb_le_certificate(arb(l_t - 1), arb(1) + Y_b.log())
            _, ok_unif = classify_arb_le_certificate(bound_unif_L, bound_unif_log)

            row_s_ok = bool(ok_psi and ok_g2 and ok_loc and ok_l_log and ok_unif and l_t >= 1)
            same_bounds_ok = same_bounds_ok and row_s_ok
            same_bound_rows.append(
                {
                    "Y": y_val,
                    "T_Y": T_y,
                    "L_T": l_t,
                    "S_same_Y": serialize_arb_certified(s_same),
                    "sum_psi_sq_le_T": serialize_arb_certified(sum_psi),
                    "sum_log2_G2_le_T": serialize_arb_certified(sum_g2),
                    "local_hilbert_bound": serialize_arb_certified(bound_local),
                    "uniform_log_bound_C_same_1_plus_log_Y": serialize_arb_certified(bound_unif_log),
                    "local_margin_abs_S_same_minus_bound": serialize_arb_certified(m_loc),
                    "uniform_margin_abs_S_same_minus_bound": serialize_arb_certified(m_unif),
                    "verified": row_s_ok,
                }
            )

        # 3. Matched controls (`unsigned_1`, `a2`, `a_3_5_7`) + labeled `hybrid_a2_liouville` on Y = 16..512:
        #    First cross-check 1D control chain evaluator vs 2D `Hcal_ctrl` at Y = 16:
        ctrl_2d_cross_ok = True
        for m_chk in ("unsigned_1", "a2", "a_3_5_7"):
            ck16 = build_matched_control_complete_kernel_small_T(16, m_chk, tbl, prec_bits=prec_bits)
            r16_1d = evaluate_control_dyadic_chain_split_arb(16, m_chk, tbl, prec_bits=prec_bits)
            ep2 = -1 if (2 in ck16["prime_set"]) else 1
            H_c16 = ck16["Hcal_ctrl"]
            a_s16 = ck16["a_seq"]
            o16 = odd_chain_parts_O_T(ck16["T_Y"])
            ss_2d = arb(0)
            sd_2d = arb(0)
            for u in o16:
                ju = dyadic_chain_exponents_J_u(u, ck16["T_Y"])
                for j1 in ju:
                    for j2 in ju:
                        if j1 != j2:
                            m1, n1 = (4 ** j1) * u, (4 ** j2) * u
                            ss_2d += (
                                H_c16(m1, n1)
                                + arb(ep2) * H_c16(2 * m1, n1)
                                + arb(ep2) * H_c16(m1, 2 * n1)
                                + H_c16(2 * m1, 2 * n1)
                            )
                for v in o16:
                    if u != v:
                        jv = dyadic_chain_exponents_J_u(v, ck16["T_Y"])
                        kv = arb(0)
                        for j1 in ju:
                            for j2 in jv:
                                m1, n1 = (4 ** j1) * u, (4 ** j2) * v
                                kv += (
                                    H_c16(m1, n1)
                                    + arb(ep2) * H_c16(2 * m1, n1)
                                    + arb(ep2) * H_c16(m1, 2 * n1)
                                    + H_c16(2 * m1, 2 * n1)
                                )
                        sd_2d += arb(a_s16[u] * a_s16[v]) * kv
            if not (
                arb(0) in (r16_1d["S_same"] - ss_2d)
                and abs(r16_1d["S_same"] - ss_2d) < arb("1e-48")
                and arb(0) in (r16_1d["S_different"] - sd_2d)
                and abs(r16_1d["S_different"] - sd_2d) < arb("1e-48")
            ):
                ctrl_2d_cross_ok = False

        control_rows: List[Dict[str, Any]] = []
        controls_refuted_ok = True
        liouville_survived_ok = True
        for y_val in (16, 32, 64, 128, 256, 512):
            for mode in ("liouville", "unsigned_1", "a2", "a_3_5_7", "hybrid_a2_liouville"):
                rc = evaluate_control_dyadic_chain_split_arb(y_val, mode, tbl, prec_bits=prec_bits)
                margin_diff = rc["S_different"] - rc["log_Y_times_D_tilde"]
                cls_diff = classify_probe_margin_arb(margin_diff)
                if y_val >= 64:
                    if mode == "liouville" and cls_diff["verdict"] != "PASS":
                        liouville_survived_ok = False
                    if mode in ("unsigned_1", "a2", "a_3_5_7", "hybrid_a2_liouville") and (
                        cls_diff["verdict"] != "FAIL"
                    ):
                        controls_refuted_ok = False
                control_rows.append(
                    {
                        "Y": y_val,
                        "mode": mode,
                        "is_hybrid_diagnostic": rc["is_hybrid_diagnostic"],
                        "exact_matched_core": rc["exact_matched_core"],
                        "derived_p2_pair_sign_eps_2": rc["eps_2"],
                        "S_same_Y": serialize_arb_certified(rc["S_same"]),
                        "S_different_Y": serialize_arb_certified(rc["S_different"]),
                        "D_tilde_Y": serialize_arb_certified(rc["D_tilde"]),
                        "log_Y_times_D_tilde": serialize_arb_certified(rc["log_Y_times_D_tilde"]),
                        "S_different_over_log_Y_D_tilde": certified_ratio_with_positive_denominator(
                            rc["S_different"], rc["log_Y_times_D_tilde"], prec_bits=prec_bits
                        ),
                        "TC063_P0_DIFF_margin": serialize_arb_certified(margin_diff),
                        "TC063_P0_DIFF_verdict": cls_diff["verdict"],
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
                "Mixed formal/analytic/certified section: shifted-station disjointness, complete-kernel "
                "<U_m, U_n>_Y - 4*<V_m, V_n> feature representation, uniform constants C_psi and "
                "C_g = 186*(tau - 1), finite Hilbert inequality, |S_same(Y)| <= (L(T)-1)*(2*C_psi + 8*C_g) "
                "<= C_same*(1 + log Y) for all real Y >= 2, and two-way MixedCovarianceClosureHypothesis "
                "equivalence Sigma_off(.; 2) <-> S_different(.) are CONCRETE_ANALYTIC_IN_LEAN (Lean "
                "Theorem 3); matched z = 1 Laurent control cores are ANALYTIC_PROVED_OUTSIDE_LEAN; and "
                "256-bit Arb margin certifications on Y = 2..1024 plus matched control / labeled hybrid "
                "refutations on S_different across Y = 64..512 are CERTIFIED_FINITE_OBSERVATION."
            ),
            "component_epistemic_map": {
                "shifted_station_disjointness_on_distinct_anchors": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "uniform_same_chain_hilbert_bound_and_closure_equivalence": "CONCRETE_ANALYTIC_IN_LEAN",
                "matched_z1_laurent_control_cores": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "same_chain_margin_grid_and_control_S_different_refutations": "CERTIFIED_FINITE_OBSERVATION",
            },
            "lean_theorems": [
                "uniform_same_chain_hilbert_bound_and_closure_transfer_tc063",
            ],
            "uniform_constants": {
                k: serialize_arb_certified(v) for k, v in consts.items()
            },
            "shifted_station_disjointness_and_feature_checks": {
                "disjointness_verified_on_I2_180": disj_ok,
                "m_eq_n_self_collision_indispensability_certified_at_Y16_m3": diag_self_collision_needed_ok,
                "distinct_anchor_feature_rows": feature_rows,
                "verified": bool(disj_ok and feature_ok and diag_self_collision_needed_ok),
            },
            "same_chain_hilbert_bound_rows": same_bound_rows,
            "control_2d_vs_1d_cross_check_Y16_verified": ctrl_2d_cross_ok,
            "matched_control_and_hybrid_chain_rows": control_rows,
            "all_negative_controls_refuted_on_S_different_for_Y_ge_64": controls_refuted_ok,
            "all_section_3_checks_pass": bool(
                disj_ok
                and feature_ok
                and diag_self_collision_needed_ok
                and same_bounds_ok
                and ctrl_2d_cross_ok
                and controls_refuted_ok
                and liouville_survived_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 5. Section 4: Substantive Distinct-Chain Research Attempts (Attempts A, B, C)
# ---------------------------------------------------------------------------


def verify_section_4_distinct_chain_attempts_and_obstructions(
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute and certify all three substantive analytic attempts (`Attempts A, B, C`) on
    `S_different(Y)` (`Prompt §6`), verifying proved intermediate identities, certifying
    refutations of failed sub-candidates (`TC063-CAND-A1-PRIM-NONPOS`,
    `TC063-CAND-B1-SQPROJ-DIAG-DOM`, `TC063-CAND-C1-ARB-SIGN`), and recording the exact first
    uncontrolled term and order of magnitude in each route.
    """
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(2500, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 2100
        else selberg_table
    )

    saved = flint_ctx.prec
    try:
        flint_ctx.prec = prec_bits
        tau = _tau_arb()
        log_tau = tau.log()

        # ===================================================================
        # ATTEMPT A: Complete-Kernel Common-Factor Regrouping (u = g*r, v = g*t)
        # ===================================================================
        # 1. Exhaustive coprime prime-power feature decoupling check on 1 <= g, r, t <= 25, 0 <= a, b <= 3:
        c_div_700 = [arb(0)] * 701
        for qp, ae in prime_power_pairs_up_to(700):
            qa = qp ** ae
            lg2q = arb(qp).log() ** 2
            for mult in range(qa, 701, qa):
                c_div_700[mult] += lg2q
        lg2_2 = arb(2).log() ** 2

        decouple_ok = True
        decouple_count = 0
        for g in (1, 3, 5, 9, 15):
            for r in (1, 3, 5, 7, 11):
                for t in (1, 3, 5, 7, 11):
                    if math.gcd(r, t) != 1:
                        continue
                    for a_e in (0, 1, 2):
                        for b_e in (0, 1, 2):
                            m_v = (2 ** a_e) * g * r
                            n_v = (2 ** b_e) * g * t
                            if m_v <= 700 and n_v <= 700:
                                decouple_count += 1
                                if math.gcd(m_v, n_v) != (2 ** min(a_e, b_e)) * g:
                                    decouple_ok = False
                                rhs_c = c_div_700[g] + arb(min(a_e, b_e)) * lg2_2
                                diff_c = c_div_700[math.gcd(m_v, n_v)] - rhs_c
                                if not (diff_c == arb(0) or (arb(0) in diff_c and abs(diff_c) < arb("1e-70"))):
                                    decouple_ok = False

        # 2. Verify p = 2 smallOp jump obstruction when D_eff >= 1 (Y = 16, T = 32, D_eff = 2):
        #    Since p = 2 <= D_eff + 1 = 3, the large-prime jump formula b_{2m} - b_m fails at p = 2!
        vecs_16 = compute_complete_core_s_Y_and_beta_Y_arb(32, 2, tbl["R_osc"], prec_bits=prec_bits)
        b_16 = [arb(0)] + [
            arb(liouville_lambda_int(n)) * vecs_16["beta_Y"][n] for n in range(1, 33)
        ]
        M_drift = tbl["M_drift"]
        c_lam = tbl["c_lambda"]
        p2_jump_witnesses: List[Dict[str, Any]] = []
        for m_w in (1, 3, 5):
            lhs_j = b_16[2 * m_w] - b_16[m_w]
            # Naive large-prime formula (valid only for p > D_eff + 1):
            sum_u0 = arb(0)
            for u0 in range(1, m_w + 1):
                if m_w % u0 == 0:
                    delta_2u0 = M_drift[2 * u0] - M_drift[2 * u0 - 1]
                    sum_u0 += delta_2u0 * arb(liouville_lambda_int(u0))
            naive_rhs = (c_lam if is_perfect_square_int(m_w) else arb(0)) + sum_u0
            err_p2 = lhs_j - naive_rhs
            p2_jump_witnesses.append(
                {
                    "m": m_w,
                    "b_2m_minus_b_m_actual": serialize_arb_certified(lhs_j),
                    "misapplied_large_prime_formula_discrepancy": serialize_arb_certified(err_p2),
                    "nonzero_discrepancy_certified": bool(not (arb(0) in err_p2)),
                }
            )
        p2_smallop_obstruction_ok = all(w["nonzero_discrepancy_certified"] for w in p2_jump_witnesses)

        # 3. Complete-kernel primitive-pair regrouping S_different = sum_{g in G_odd(T)} Pi_Y^diff(g)
        #    on Y in {4, 8, 16, 32, 64} and refutation of TC063-CAND-A1-PRIM-NONPOS at Y = 16 (g = 5)
        #    and Y = 64 (g = 7):
        attempt_a_rows: List[Dict[str, Any]] = []
        attempt_a_reindexing_ok = True
        pi_16_g5 = arb(0)
        pi_64_g7 = arb(0)
        kcal_cache_by_y: Dict[int, Tuple[List[int], Dict[Tuple[int, int], arb]]] = {}

        for y_val in (4, 8, 16, 32, 64):
            sp = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            cut = certify_exact_scale_cutoffs(sp, base_prec_bits=prec_bits)
            T_y = cut["T_Y"]
            D0_eff = cut["D0_eff"]
            Y_b = arb(y_val)
            Hcal = build_complete_signed_kernel_evaluator_small_T(
                Y_b, T_y, D0_eff, tbl, prec_bits=prec_bits
            )

            def _dH(m_i: int, n_i: int) -> arb:
                return Hcal(m_i, n_i) - Hcal(2 * m_i, n_i) - Hcal(m_i, 2 * n_i) + Hcal(2 * m_i, 2 * n_i)

            o_t = odd_chain_parts_O_T(T_y)
            kcal_map: Dict[Tuple[int, int], arb] = {}
            s_diff_direct = arb(0)
            for u in o_t:
                lu = liouville_lambda_int(u)
                ju = dyadic_chain_exponents_J_u(u, T_y)
                for v in o_t:
                    if u == v:
                        continue
                    if (v, u) in kcal_map:
                        kv = kcal_map[(v, u)]
                    else:
                        jv = dyadic_chain_exponents_J_u(v, T_y)
                        kv = arb(0)
                        for j in ju:
                            for k in jv:
                                kv += _dH((4 ** j) * u, (4 ** k) * v)
                    kcal_map[(u, v)] = kv
                    s_diff_direct += arb(lu * liouville_lambda_int(v)) * kv
            kcal_cache_by_y[y_val] = (o_t, kcal_map)

            g_odd = odd_common_factor_gcd_set(T_y)
            tot_pi = arb(0)
            sector_entries: List[Dict[str, Any]] = []
            for g in g_odd:
                o_tg = odd_chain_parts_O_T(T_y // g)
                for r in o_tg:
                    if dyadic_chain_exponents_J_u(g * r, T_y) != dyadic_chain_exponents_J_u(r, T_y // g):
                        attempt_a_reindexing_ok = False
                pi_g = arb(0)
                for r in o_tg:
                    lr = liouville_lambda_int(r)
                    for t in o_tg:
                        if r != t and math.gcd(r, t) == 1:
                            pi_g += arb(lr * liouville_lambda_int(t)) * kcal_map[(g * r, g * t)]
                tot_pi += pi_g
                if y_val == 16 and g == 5:
                    pi_16_g5 = pi_g
                if y_val == 64 and g == 7:
                    pi_64_g7 = pi_g
                sector_entries.append(
                    {
                        "g": g,
                        "Pi_Y_diff_g": serialize_arb_certified(pi_g),
                        "certified_positive": bool(pi_g > arb(0)),
                    }
                )

            res_pi = tot_pi - s_diff_direct
            row_a_ok = bool(arb(0) in res_pi and abs(res_pi) < arb("1e-50"))
            attempt_a_reindexing_ok = attempt_a_reindexing_ok and row_a_ok
            attempt_a_rows.append(
                {
                    "Y": y_val,
                    "T_Y": T_y,
                    "G_odd_count": len(g_odd),
                    "S_different_direct": serialize_arb_certified(s_diff_direct),
                    "S_different_primitive_gcd_sum": serialize_arb_certified(tot_pi),
                    "primitive_minus_direct_residual": serialize_arb_certified(res_pi),
                    "positive_g_sectors": [e["g"] for e in sector_entries if e["certified_positive"]],
                    "sectors": sector_entries,
                    "verified": row_a_ok,
                }
            )

        cand_a1_refuted_ok = bool(pi_16_g5 > arb("7e-4") and pi_64_g7 > arb("1e-3"))

        # ===================================================================
        # ATTEMPT B: Quantitative Square-Projection & Selberg Compatibility
        # ===================================================================
        attempt_b_sq_rows: List[Dict[str, Any]] = []
        attempt_b_sq_ok = True
        cand_b1_refuted_ok = True
        for y_val in (8, 16, 32, 64):
            sp = ExactScaleSpec(str(y_val), "exact_rational", Fraction(y_val, 1))
            cut = certify_exact_scale_cutoffs(sp, base_prec_bits=prec_bits)
            T_y = cut["T_Y"]
            D0_eff = cut["D0_eff"]
            Y_b = arb(y_val)
            vecs = compute_complete_core_s_Y_and_beta_Y_arb(
                T_y, D0_eff, tbl["R_osc"], prec_bits=prec_bits
            )
            b_arr = [arb(0)] + [
                arb(liouville_lambda_int(n)) * vecs["beta_Y"][n] for n in range(1, T_y + 1)
            ]
            o_t = odd_chain_parts_O_T(T_y)

            # Pointwise check at X = sqrt(tau)*Y of BOTH:
            # (i) sum_{d in O(T)} Gcal_Y^(d)(X) == sum_{w=m^2 in O(T)} Ucal_w(X)
            # (ii) odd-Mobius recovery sum_{e in O(T)} mu(e)*S_{sq,Y}^(e)(X) == Gcal_Y^(1)(X):
            x_pt = Y_b * tau.sqrt()
            lg2_pt = x_pt.log() ** 2
            ucal_pt: Dict[int, arb] = {}
            for u in o_t:
                acc_u = arb(0)
                for j in dyadic_chain_exponents_J_u(u, T_y):
                    m1 = (4 ** j) * u
                    m2 = 2 * m1
                    p1 = (arb(1) - b_arr[m1] / lg2_pt) * evaluate_phi_n_arb(x_pt, m1, prec_bits=prec_bits)
                    p2 = (arb(1) - b_arr[m2] / lg2_pt) * evaluate_phi_n_arb(x_pt, m2, prec_bits=prec_bits)
                    acc_u += p1 - p2
                ucal_pt[u] = acc_u

            gcal_pt: Dict[int, arb] = {}
            for d in o_t:
                gcal_pt[d] = sum(
                    (arb(liouville_lambda_int(u)) * ucal_pt[d * u] for u in odd_chain_parts_O_T(T_y // d)),
                    arb(0),
                )
            lhs_sq = sum(gcal_pt.values(), arb(0))
            rhs_sq = sum((ucal_pt[w] for w in o_t if is_perfect_square_int(w)), arb(0))
            mob_rec = arb(0)
            for e_d in o_t:
                mu_e = moebius_mu_int(e_d)
                if mu_e != 0:
                    sq_e = sum(
                        (
                            ucal_pt[e_d * w]
                            for w in odd_chain_parts_O_T(T_y // e_d)
                            if is_perfect_square_int(w)
                        ),
                        arb(0),
                    )
                    mob_rec += arb(mu_e) * sq_e

            # Window-norm comparison: sum_{d in O(T)} ||Gcal_Y^(d)||_Y^2 vs ||S_{sq,Y}||_Y^2:
            b_c = [acb(v) for v in b_arr]
            st_all = [(k, acb(k) ** (-3), acb(-(arb(k * k) ** (-1)))) for k in range(1, T_y + 1)]
            chains_map = {
                u: [((4 ** j) * u, 2 * (4 ** j) * u) for j in dyadic_chain_exponents_J_u(u, T_y)]
                for u in o_t
            }
            d_lists = {
                d: [(u, acb(liouville_lambda_int(u))) for u in odd_chain_parts_O_T(T_y // d)]
                for d in o_t
            }
            sq_w = [w for w in o_t if is_perfect_square_int(w)]
            Yc = acb(Y_b)
            lgYc = acb(Y_b.log())
            Yc_52 = Yc ** (acb(5) / acb(2))
            Yc_2 = Yc * Yc
            tol_b = arb(2) ** (-175)

            def _diag_d_sq_cb(u_v: acb, _an: bool) -> acb:
                lg = lgYc + u_v
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_v).exp()
                x2 = Yc_2 * (acb(2) * u_v).exp()
                ph = [acb(0)] * (T_y + 1)
                for k_i, inv_k3, neg_inv_k2 in st_all:
                    ph[k_i] = x52 * inv_k3 * (x2 * neg_inv_k2).exp()
                uc = {}
                for u in o_t:
                    s_u = acb(0)
                    for m1, m2 in chains_map[u]:
                        s_u += (acb(1) - b_c[m1] * inv_lg2) * ph[m1] - (
                            acb(1) - b_c[m2] * inv_lg2
                        ) * ph[m2]
                    uc[u] = s_u
                tot_d = acb(0)
                for d in o_t:
                    gd = acb(0)
                    for u_sub, l_c in d_lists[d]:
                        gd += l_c * uc[d * u_sub]
                    tot_d += gd * gd
                return tot_d

            def _sq_norm_cb(u_v: acb, _an: bool) -> acb:
                lg = lgYc + u_v
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_v).exp()
                x2 = Yc_2 * (acb(2) * u_v).exp()
                s_sq = acb(0)
                for w in sq_w:
                    for m1, m2 in chains_map[w]:
                        ph1 = x52 * (acb(m1) ** (-3)) * (-x2 / acb(m1 * m1)).exp()
                        ph2 = x52 * (acb(m2) ** (-3)) * (-x2 / acb(m2 * m2)).exp()
                        s_sq += (acb(1) - b_c[m1] * inv_lg2) * ph1 - (
                            acb(1) - b_c[m2] * inv_lg2
                        ) * ph2
                return s_sq * s_sq

            sum_gcal_sq = acb.integral(
                _diag_d_sq_cb, acb(0), acb(log_tau), rel_tol=tol_b, abs_tol=tol_b
            ).real
            norm_s_sq = acb.integral(
                _sq_norm_cb, acb(0), acb(log_tau), rel_tol=tol_b, abs_tol=tol_b
            ).real
            cand_b1_margin = sum_gcal_sq - norm_s_sq

            if y_val >= 16 and not bool(cand_b1_margin > arb(0)):
                cand_b1_refuted_ok = False

            row_b_ok = bool(
                arb(0) in (lhs_sq - rhs_sq)
                and abs(lhs_sq - rhs_sq) < arb("1e-65")
                and arb(0) in (mob_rec - gcal_pt[1])
                and abs(mob_rec - gcal_pt[1]) < arb("1e-65")
            )
            attempt_b_sq_ok = attempt_b_sq_ok and row_b_ok
            attempt_b_sq_rows.append(
                {
                    "Y": y_val,
                    "T_Y": T_y,
                    "pointwise_sq_proj_residual": serialize_arb_certified(lhs_sq - rhs_sq),
                    "pointwise_odd_moebius_recovery_residual": serialize_arb_certified(
                        mob_rec - gcal_pt[1]
                    ),
                    "sum_d_Gcal_norm_sq": serialize_arb_certified(sum_gcal_sq),
                    "S_sq_Y_norm_sq": serialize_arb_certified(norm_s_sq),
                    "TC063_CAND_B1_margin_sum_d_minus_S_sq": serialize_arb_certified(
                        cand_b1_margin
                    ),
                    "off_diagonal_d1_ne_d2_dilation_sum": serialize_arb_certified(
                        norm_s_sq - sum_gcal_sq
                    ),
                    "verified": row_b_ok,
                }
            )

        # Station-level Selberg decomposition check of psi_{Y,n}(X) at Y = 16 (T = 32):
        s_smooth_16 = vecs_16["s_Y"]
        x_chk = arb(16) * tau.sqrt()
        lg_chk = x_chk.log()
        max_selberg_station_err = arb(0)
        for n_i in range(1, 33):
            ph_i = evaluate_phi_n_arb(x_chk, n_i, prec_bits=prec_bits)
            psi_direct = (arb(1) - b_16[n_i] / (lg_chk * lg_chk)) * ph_i
            psi_selberg = (
                (( (x_chk / arb(n_i)).log() / lg_chk ) ** 2)
                + arb(2) * (arb(n_i).log() / lg_chk)
                - arb(liouville_lambda_int(n_i)) * s_smooth_16[n_i] / (lg_chk * lg_chk)
            ) * ph_i
            err_s = abs(psi_direct - psi_selberg)
            if bool(err_s.upper() > max_selberg_station_err.upper()):
                max_selberg_station_err = err_s
        selberg_station_ok = bool(max_selberg_station_err < arb("1e-68"))

        # ===================================================================
        # ATTEMPT C: Constructive Greedy +-1 Sign-Extension & Omega(Y) Obstruction
        # ===================================================================
        # 1. At Y = 64 (T = 182, |O(T)| = 46), use exact 2D Kcal_64 from Attempt A and construct
        #    deterministic greedy +-1 witness seeded on A_odd(64) = {65, 67, ..., 91}:
        o64, kcal64 = kcal_cache_by_y[64]
        a_odd_64 = [u for u in o64 if 64 <= u <= 96]
        eps64 = greedy_sign_extension_witness(
            o64, a_odd_64, lambda u_i, v_i: kcal64.get((u_i, v_i), arb(0))
        )
        seed_sum_64 = arb(0)
        for u in a_odd_64:
            for v in a_odd_64:
                if u != v:
                    seed_sum_64 += kcal64[(u, v)]
        greedy_sum_64 = arb(0)
        for u in o64:
            for v in o64:
                if u != v:
                    greedy_sum_64 += arb(eps64[u] * eps64[v]) * kcal64[(u, v)]
        sp64 = ExactScaleSpec("64", "exact_rational", Fraction(64, 1))
        res64_1d = evaluate_mixed_covariance_point_arb(sp64, selberg_table=tbl)
        rhs_cand_c1_64 = arb(1) / arb(4) + arb(64).log() * res64_1d["D_tilde_Y"]
        margin_cand_c1_64 = greedy_sum_64 - rhs_cand_c1_64
        _, greedy_dom_seed_ok = classify_arb_le_certificate(seed_sum_64, greedy_sum_64)
        cand_c1_refuted_ok = bool(
            greedy_dom_seed_ok
            and all(v in (-1, 1) for v in eps64.values())
            and margin_cand_c1_64 > arb("0.2")
        )

        # 2. Certify asymptotic all-chain-length pointwise lower bound on subwindow
        #    [4*Y, (43/10)*Y] subset [Y, tau*Y] for u in [(9/5)*Y, (21/10)*Y] (`w = X/u in [40/21, 43/18]`):
        #    On w in [40/21, 43/18], -(Phi(w) - 2^(-1/2)*Phi(w/2)) - (1/2)*Phi(w/4) - w^(5/2)/4032 > c_chain > 0!
        w_lo = _frac_to_arb(Fraction(40, 21))
        w_hi = _frac_to_arb(Fraction(43, 18))
        # Upper bound on Phi(w) = w^(5/2)*exp(-w^2) on [w_lo, w_hi] (strictly decreasing since w_lo > sqrt(5/4)):
        phi_w_max = (w_lo ** (arb(5) / arb(2))) * (-(w_lo * w_lo)).exp()
        # Lower bound on 2^(-1/2)*Phi(w/2) on w/2 in [20/21, 43/36] (concave peak at sqrt(5/4) approx 1.11803,
        # so min on [20/21, 43/36] is attained at one of the two endpoints!):
        s1, s2 = w_lo / arb(2), w_hi / arb(2)
        p_s1 = (s1 ** (arb(5) / arb(2))) * (-(s1 * s1)).exp() / arb(2).sqrt()
        p_s2 = (s2 ** (arb(5) / arb(2))) * (-(s2 * s2)).exp() / arb(2).sqrt()
        half_phi_min = p_s1 if bool(p_s1.lower() <= p_s2.lower()) else p_s2
        # Upper bound on j = 1 term (1/2)*Phi(w/4) on w/4 <= 43/72 < 1 (increasing):
        s_j1 = w_hi / arb(4)
        j1_max = (arb(1) / arb(2)) * (s_j1 ** (arb(5) / arb(2))) * (-(s_j1 * s_j1)).exp()
        # Upper bound on j >= 2 geometric tail sum_{j>=2} 2^{-j} (w / 4^j)^(5/2) = w^(5/2) / 4032:
        j2_tail_max = (w_hi ** (arb(5) / arb(2))) / arb(4032)
        c_chain_pointwise = +(half_phi_min - phi_w_max - j1_max - j2_tail_max)
        omega_y_chain_const_ok = bool(
            _frac_to_arb(Fraction(43, 10)) < tau and c_chain_pointwise > arb("0.02")
        )

        return {
            "epistemic_statuses": [
                "UNCONDITIONAL_FINITE_ARITHMETIC",
                "CONCRETE_ANALYTIC_IN_LEAN",
                "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "CERTIFIED_FINITE_OBSERVATION",
                "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            ],
            "section_epistemic_scope_note": (
                "Mixed research-attempt section: odd common-factor primitive regrouping, coprime "
                "prime-power decoupling c(2^a*g*r, 2^b*g*t) = c(g, g) + min(a, b)*(log 2)^2, odd-divisor "
                "square-projection & odd-Mobius recovery, station-level Selberg decomposition, and "
                "constructive greedy +-1 sign-extension lower bound are CONCRETE_ANALYTIC_IN_LEAN "
                "(Lean Theorems 4 & 5); chain-count Cauchy-Schwarz loss quantification, smooth-vs-rough "
                "prime-set iteration analysis, and asymptotic Omega(Y) arbitrary-sign obstruction are "
                "ANALYTIC_PROVED_OUTSIDE_LEAN; 256-bit Arb refutations of TC063-CAND-A1-PRIM-NONPOS, "
                "TC063-CAND-B1-SQPROJ-DIAG-DOM, and TC063-CAND-C1-ARB-SIGN are CERTIFIED_FINITE_OBSERVATION; "
                "TC063-OBL-DISTINCT-ODD-CHAIN-CORRELATION remains OPEN_CONJECTURE_OR_FAILED_CANDIDATE."
            ),
            "component_epistemic_map": {
                "coprime_feature_decoupling_and_exhaustive_gcd_checks": "UNCONDITIONAL_FINITE_ARITHMETIC",
                "primitive_regrouping_square_projection_selberg_and_greedy_sign_extension": "CONCRETE_ANALYTIC_IN_LEAN",
                "cauchy_schwarz_chain_loss_and_asymptotic_omega_Y_sign_obstruction": "ANALYTIC_PROVED_OUTSIDE_LEAN",
                "certified_refutations_of_CAND_A1_CAND_B1_and_CAND_C1": "CERTIFIED_FINITE_OBSERVATION",
                "distinct_odd_chain_closure_obligation": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
            },
            "lean_theorems": [
                "odd_common_factor_primitive_regrouping_and_feature_decoupling_tc063",
                "odd_square_projection_selberg_split_and_sign_extension_obstruction_tc063",
            ],
            "attempt_A_common_factor_primitive_regrouping": {
                "coprime_feature_decoupling_tuples_checked": decouple_count,
                "coprime_feature_decoupling_verified": decouple_ok,
                "p2_smallop_jump_obstruction_witnesses_Y16": p2_jump_witnesses,
                "p2_smallop_jump_obstruction_certified": p2_smallop_obstruction_ok,
                "primitive_regrouping_rows": attempt_a_rows,
                "candidate_A1_prim_nonpos": {
                    "candidate_id": "TC063-CAND-A1-PRIM-NONPOS",
                    "outcome": "REFUTED_BY_CERTIFIED_WITNESS",
                    "smallest_invalid_premise": (
                        "Assumed fixed-g primitive odd-chain sum Pi_Y^diff(g) <= 0 for all odd g; "
                        "at g = 5, Y = 16 (O(floor(32/5)) = {1, 3}, lambda(1)*lambda(3) = -1), "
                        "-4*c(5,5)*G_16^[2] makes Kcal_16(5, 15) < 0 so Pi_16^diff(5) = -2*Kcal_16(5, 15) > 0."
                    ),
                    "witness_Y16_g5": serialize_arb_certified(pi_16_g5),
                    "witness_Y64_g7": serialize_arb_certified(pi_64_g7),
                    "refutation_certified": cand_a1_refuted_ok,
                },
                "first_uncontrolled_term_and_size": {
                    "term": "Pi_{Y,bare}^diff(1) = sum_{r != t in O(T), gcd(r,t)=1} lambda(r)*lambda(t)*<Phi_r, Phi_t>_Y",
                    "global_cauchy_schwarz_loss": "Loses (|O(T)| - 1) ~ (1/4)*Y^(5/4), yielding O(Y^(5/4) * log Y).",
                    "resonant_shell_cauchy_schwarz_loss": "Loses resonant odd-chain count |O_res(Y)| = Theta(Y), yielding Theta(Y).",
                    "iterated_prime_smooth_wall": (
                        "Grouping S-smooth chains for fixed finite prime set S gives O_S((log Y)^|S|) <<_eta Y^eta "
                        "on same-core fibers, whereas growing P <= c*log Y leaves Theta(Y / log log Y) P-rough chains "
                        "and P = T^(1/u) blows up fiber size Psi(T, P) = T^(rho_dB(u) + o(1))."
                    ),
                },
            },
            "attempt_B_square_projection_and_selberg_compatibility": {
                "square_projection_and_moebius_rows": attempt_b_sq_rows,
                "station_selberg_decomposition_max_abs_error_Y16": serialize_arb_certified(
                    max_selberg_station_err
                ),
                "station_selberg_decomposition_verified": selberg_station_ok,
                "candidate_B1_sqproj_diag_dom": {
                    "candidate_id": "TC063-CAND-B1-SQPROJ-DIAG-DOM",
                    "outcome": "REFUTED_BY_CERTIFIED_WITNESS",
                    "smallest_invalid_premise": (
                        "Assumed boundedness ||sum_{d in O(T)} Gcal_Y^(d)||_Y^2 = ||S_{sq,Y}||_Y^2 = O(1) "
                        "bounds sum_{d in O(T)} ||Gcal_Y^(d)||_Y^2 without off-diagonal d_1 != d_2 dilation "
                        "cross-terms; off-diagonal cross-terms are strictly negative at Y in {16, 32, 64}, "
                        "and triangle inequality on odd-Mobius recovery loses (sum_{e<=Y, 2 nmid e} |mu(e)|*e^(-1/2))^2 = Theta(Y)."
                    ),
                    "refutation_certified": cand_b1_refuted_ok,
                },
                "first_uncontrolled_term_and_size": {
                    "term": (
                        "Negative off-diagonal odd-divisor dilation cross-sum "
                        "-sum_{d_1 != d_2 in O(T)} <Gcal_Y^(d_1), Gcal_Y^(d_2)>_Y in "
                        "||Gcal_Y^(1)||_Y^2 = ||S_{sq,Y}||_Y^2 - sum_{d > 1 in O(T)} ||Gcal_Y^(d)||_Y^2 "
                        "- sum_{d_1 != d_2 in O(T)} <Gcal_Y^(d_1), Gcal_Y^(d_2)>_Y "
                        "(blocking a one-way upper bound on ||Gcal_Y^(1)||_Y^2 toward S_different(Y))"
                    ),
                    "unsigned_majorant_size": "Theta(Y) under odd-Mobius triangle inequality or unsigned prime-power majorization.",
                },
            },
            "attempt_C_arithmetic_restricted_vs_arbitrary_sign_comparison": {
                "candidate_C1_arbitrary_sign": {
                    "candidate_id": "TC063-CAND-C1-ARB-SIGN",
                    "outcome": "REFUTED_BY_CERTIFIED_WITNESS",
                    "smallest_invalid_premise": (
                        "Assumed off-diagonal grouped chain kernel Kcal_Y^off(u, v) satisfies the sublinear "
                        "bound uniformly over arbitrary +-1 sign vectors eps in {+-1}^{O(T)}; greedy +-1 "
                        "extension from resonant odd band A_odd(Y) refutes Y = 64 and forces Omega(Y) growth."
                    ),
                    "seed_band_A_odd_64_sum": serialize_arb_certified(seed_sum_64),
                    "greedy_pm1_witness_sum_Y64": serialize_arb_certified(greedy_sum_64),
                    "candidate_C1_rhs_budget_Y64": serialize_arb_certified(rhs_cand_c1_64),
                    "candidate_C1_margin_Y64": serialize_arb_certified(margin_cand_c1_64),
                    "all_chain_length_subwindow_constant_c_chain": serialize_arb_certified(
                        c_chain_pointwise
                    ),
                    "refutation_and_omega_Y_obstruction_certified": bool(
                        cand_c1_refuted_ok and omega_y_chain_const_ok
                    ),
                },
            },
            "all_section_4_checks_pass": bool(
                decouple_ok
                and p2_smallop_obstruction_ok
                and attempt_a_reindexing_ok
                and cand_a1_refuted_ok
                and attempt_b_sq_ok
                and cand_b1_refuted_ok
                and selberg_station_ok
                and cand_c1_refuted_ok
                and omega_y_chain_const_ok
            ),
        }
    finally:
        flint_ctx.prec = saved


# ---------------------------------------------------------------------------
# 6. Section 5: Frozen 10-Point Unseen Validation, Interval Splits, & Aggregator
# ---------------------------------------------------------------------------


def _parse_tc063_scale_spec(pt_entry: Dict[str, Any]) -> ExactScaleSpec:
    p_kind = pt_entry["kind"]
    q_fac = Fraction(pt_entry["rational_factor"])
    e_pow = Fraction(pt_entry["exp_power"])
    if p_kind == "exact_rational" and e_pow == 0:
        return ExactScaleSpec(pt_entry["label"], "exact_rational", q_fac, 0)
    if p_kind == "exact_symbolic_exp_rational" and e_pow.denominator == 1:
        return ExactScaleSpec(pt_entry["label"], "exp_k_times_rational", q_fac, int(e_pow.numerator))
    raise ValueError(f"Unsupported TC-063 scale entry: {pt_entry}")


def execute_tc063_holdout_point_with_escalation(
    point_entry: Dict[str, Any],
    protocol_obj: Dict[str, Any],
    selberg_table_base: Dict[str, Any],
) -> Dict[str, Any]:
    """Evaluate a single registered `TC-063` unseen validation point with tier escalation,
    decisive-witness retention, `CERTIFICATION_INTEGRITY_CONFLICT` detection, and 3-valued
    `PROCESS_LIFETIME_HIGH_WATER_MARK` resource compliance.
    """
    t0_wall = time.perf_counter()
    spec = _parse_tc063_scale_spec(point_entry)
    cut = certify_exact_scale_cutoffs(spec, base_prec_bits=256)
    T_y = cut["T_Y"]
    D0_eff = cut["D0_eff"]
    l_t = max_dyadic_chain_length_L(T_y)

    num_rules = protocol_obj["numerical_settings_and_escalation_rules"]
    res_limits = num_rules["resource_limits"]
    max_wall_s = float(res_limits["max_wall_seconds_per_point"])
    max_rss_mb = float(res_limits["max_rss_megabytes"])

    tier0_cfg = resolve_protocol_quadrature_settings(
        num_rules, T_y, cut["ceil_tau_Y"], escalation_tier=0
    )
    ladder = [tier0_cfg] + [
        resolve_protocol_quadrature_settings(
            num_rules, T_y, cut["ceil_tau_Y"], escalation_tier=int(st["tier"])
        )
        for st in num_rules["escalation_ladder_on_zero_straddling_margin"]
    ]

    probes = protocol_obj["frozen_candidate_probes"]
    decisive_acc: Dict[str, Dict[str, Any]] = {}
    conflict_records: List[Dict[str, Any]] = []
    tier_history: List[Dict[str, Any]] = []
    last_eval: Optional[Dict[str, Any]] = None

    for cfg in ladder:
        t_tier = time.perf_counter()
        used = cfg["used_settings"]
        prec_b = int(used["prec_bits"])
        q_tol = int(used["quad_tol_bits"])
        use_3z = cfg["quadrature_mode"] == "three_zone"
        n_pan = int(used["n_panels"])
        z1_rat = int(used["zone1_ratio_threshold_x_over_n"] or 12)

        tbl_use = (
            selberg_table_base
            if (prec_b <= 256 and len(selberg_table_base["R"]) > 2 * T_y + 4)
            else compute_selberg_centered_remainder_table_fast_arb(
                2 * T_y + 16, prec_bits=prec_b + 32
            )
        )
        saved_p = flint_ctx.prec
        try:
            flint_ctx.prec = prec_b
            y_ball = spec.evaluate_arb(prec_b)
            res_1d = evaluate_mixed_covariance_point_arb(
                spec,
                escalation_tier=int(cfg["escalation_tier"]),
                protocol_rules=num_rules,
                selberg_table=tbl_use,
            )
            mf_ch = evaluate_dyadic_chain_observables_matrix_free_arb(
                y_ball,
                T_y,
                D0_eff,
                cut["ceil_tau_Y"],
                tbl_use,
                prec_bits=prec_b,
                quad_tol_bits=q_tol,
                use_three_zone=use_3z,
                n_panels=n_pan,
                zone1_ratio=z1_rat,
            )
            # Local same-chain Hilbert bound:
            vecs = compute_complete_core_s_Y_and_beta_Y_arb(
                T_y, D0_eff, tbl_use["R_osc"], prec_bits=prec_b + 32
            )
            b_c = [acb(0)] + [
                acb(arb(liouville_lambda_int(n)) * vecs["beta_Y"][n]) for n in range(1, T_y + 1)
            ]
            lg_n_sq = [acb(0)] + [acb(arb(n).log() ** 2) for n in range(1, T_y + 1)]
            st_consts = [(k, acb(k) ** (-3), acb(-(arb(k * k) ** (-1)))) for k in range(1, T_y + 1)]
            Yc = acb(y_ball)
            lgYc = acb(y_ball.log())
            Yc_52 = Yc ** (acb(5) / acb(2))
            Yc_2 = Yc * Yc
            log_tau = _tau_arb().log()
            tol_loc = arb(2) ** (-min(q_tol, 175))

            def _psi_cb(u_v: acb, _an: bool) -> acb:
                lg = lgYc + u_v
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_v).exp()
                x2 = Yc_2 * (acb(2) * u_v).exp()
                acc = acb(0)
                for k_i, inv_k3, neg_inv_k2 in st_consts:
                    pk_v = x52 * inv_k3 * (x2 * neg_inv_k2).exp()
                    ps = (acb(1) - b_c[k_i] * inv_lg2) * pk_v
                    acc += ps * ps
                return acc

            def _g2_cb(u_v: acb, _an: bool) -> acb:
                lg = lgYc + u_v
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_v).exp()
                x2 = Yc_2 * (acb(2) * u_v).exp()
                acc = acb(0)
                for k_i, inv_k3, neg_inv_k2 in st_consts:
                    pk_v = x52 * inv_k3 * (x2 * neg_inv_k2).exp()
                    acc += lg_n_sq[k_i] * (pk_v * pk_v) * inv_lg2
                return acc

            sum_psi = acb.integral(_psi_cb, acb(0), acb(log_tau), rel_tol=tol_loc, abs_tol=tol_loc).real
            sum_g2 = acb.integral(_g2_cb, acb(0), acb(log_tau), rel_tol=tol_loc, abs_tol=tol_loc).real
            local_same_bound = arb(l_t - 1) * (arb(2) * sum_psi + arb(8) * sum_g2)

            lg_D = res_1d["log_Y_times_D_tilde"]
            s_same = mf_ch["S_same_Y"]
            s_diff = mf_ch["S_different_Y"]

            cand_margins: Dict[str, Tuple[arb, bool]] = {}
            for pr in probes:
                pid = pr["probe_id"]
                y0_b = _frac_to_arb(Fraction(pr["domain_threshold_Y0"]))
                in_dom = bool(y_ball >= y0_b)
                if pid == "TC063-P0-DIFF":
                    m_v = s_diff - lg_D
                elif pid == "TC063-P-HALF-DIFF":
                    m_v = s_diff - lg_D
                elif pid == "TC063-P-NEG-DIFF":
                    m_v = s_diff
                elif pid == "TC063-SAME-LOCAL-HILBERT":
                    m_v = abs(s_same) - local_same_bound
                else:
                    raise ValueError(f"Unknown TC-063 probe {pid!r}")
                cand_margins[pid] = (+m_v, in_dom)

            in_64 = bool(y_ball >= arb(64))
            cand_margins["KL1_same_chain"] = (+(s_same - (arb(1) / arb(4)) * lg_D), in_64)
            cand_margins["KL1_different_chain"] = (+(s_diff - (arb(3) / arb(4)) * lg_D), in_64)

            tier_verdicts: Dict[str, str] = {}
            for cid, (m_ball, in_dom) in cand_margins.items():
                if not in_dom:
                    tier_verdicts[cid] = "OUT_OF_DOMAIN_NOT_APPLICABLE"
                    continue
                cls_c = classify_probe_margin_arb(m_ball)
                verd = cls_c["verdict"]
                tier_verdicts[cid] = verd
                ser_m = serialize_arb_certified(m_ball)
                if verd in ("PASS", "FAIL"):
                    prev = decisive_acc.get(cid)
                    if prev is None:
                        decisive_acc[cid] = {
                            "verdict": verd,
                            "margin_M_Y": ser_m,
                            "decided_at_tier": int(cfg["escalation_tier"]),
                            "prec_bits": prec_b,
                        }
                    elif prev["verdict"] != verd:
                        conflict_records.append(
                            {
                                "candidate_id": cid,
                                "earlier_tier": prev["decided_at_tier"],
                                "earlier_verdict": prev["verdict"],
                                "earlier_margin": prev["margin_M_Y"],
                                "later_tier": int(cfg["escalation_tier"]),
                                "later_verdict": verd,
                                "later_margin": ser_m,
                            }
                        )

            rss_info = _measure_process_rss_megabytes()
            dt_tier = round(time.perf_counter() - t_tier, 6)
            cum_wall = round(time.perf_counter() - t0_wall, 6)
            tier_history.append(
                {
                    "tier": int(cfg["escalation_tier"]),
                    "prec_bits": prec_b,
                    "quad_tol_bits": q_tol,
                    "quadrature_mode": cfg["quadrature_mode"],
                    "n_panels": n_pan,
                    "elapsed_sec": dt_tier,
                    "tier_wall_seconds": dt_tier,
                    "cumulative_wall_seconds": max(dt_tier, cum_wall),
                    "current_rss_mb": rss_info["current_rss_mb"],
                    "peak_rss_mb": rss_info["peak_rss_mb"],
                    "peak_rss_measurement_semantics": rss_info["peak_rss_measurement_semantics"],
                    "tier_verdicts": tier_verdicts,
                }
            )
            last_eval = {
                "Y_ball": y_ball,
                "E_Y": res_1d["E_Y"],
                "D_tilde_Y": res_1d["D_tilde_Y"],
                "log_Y_times_D_tilde": lg_D,
                "F_int_T_p2": mf_ch["F_int_T_p2"],
                "Sigma_diag_p2": mf_ch["Sigma_diag_p2"],
                "Sigma_off_p2": mf_ch["Sigma_off_p2"],
                "S_same_Y": s_same,
                "S_different_Y": s_diff,
                "reconstructed_Sigma_off": mf_ch["reconstructed_Sigma_off"],
                "same_input_reconstruction_residual": mf_ch["same_input_reconstruction_residual"],
                "local_same_chain_hilbert_bound": +local_same_bound,
                "cand_margins": cand_margins,
            }
        finally:
            flint_ctx.prec = saved_p

        if conflict_records:
            break
        all_decided = all(
            (not in_d) or (cid in decisive_acc)
            for cid, (_m, in_d) in last_eval["cand_margins"].items()
        )
        if all_decided:
            break
        tot_wall_so_far = time.perf_counter() - t0_wall
        last_rss = tier_history[-1]["peak_rss_mb"]
        if tot_wall_so_far > max_wall_s or (last_rss is not None and last_rss > max_rss_mb):
            break

    assert last_eval is not None
    res_chk = evaluate_point_resource_compliance(
        tier_history,
        max_wall_sec=max_wall_s,
        max_rss_mb=max_rss_mb,
    )

    probe_evals: Dict[str, Any] = {}
    for pr in probes:
        pid = pr["probe_id"]
        m_last, in_dom = last_eval["cand_margins"][pid]
        if not in_dom:
            probe_evals[pid] = {
                "applicable_in_domain": False,
                "verdict": "OUT_OF_DOMAIN_NOT_APPLICABLE",
                "margin_M_Y": serialize_arb_certified(m_last),
            }
        elif any(c["candidate_id"] == pid for c in conflict_records):
            probe_evals[pid] = {
                "applicable_in_domain": True,
                "verdict": CERTIFICATION_INTEGRITY_CONFLICT_VERDICT,
                "margin_M_Y": serialize_arb_certified(m_last),
            }
        elif pid in decisive_acc:
            acc = decisive_acc[pid]
            probe_evals[pid] = {
                "applicable_in_domain": True,
                "verdict": acc["verdict"],
                "decided_at_tier": acc["decided_at_tier"],
                "margin_M_Y": acc["margin_M_Y"],
            }
        else:
            probe_evals[pid] = {
                "applicable_in_domain": True,
                "verdict": "UNRESOLVED",
                "margin_M_Y": serialize_arb_certified(m_last),
            }

    kl1_evals: Dict[str, Any] = {}
    for kid in ("KL1_same_chain", "KL1_different_chain"):
        m_last, in_dom = last_eval["cand_margins"][kid]
        if not in_dom:
            kl1_evals[kid] = {
                "applicable_in_domain": False,
                "verdict": "OUT_OF_DOMAIN_NOT_APPLICABLE",
                "margin_M_Y": serialize_arb_certified(m_last),
            }
        elif any(c["candidate_id"] == kid for c in conflict_records):
            kl1_evals[kid] = {
                "applicable_in_domain": True,
                "verdict": CERTIFICATION_INTEGRITY_CONFLICT_VERDICT,
                "margin_M_Y": serialize_arb_certified(m_last),
            }
        elif kid in decisive_acc:
            acc = decisive_acc[kid]
            kl1_evals[kid] = {
                "applicable_in_domain": True,
                "verdict": acc["verdict"],
                "decided_at_tier": acc["decided_at_tier"],
                "margin_M_Y": acc["margin_M_Y"],
            }
        else:
            kl1_evals[kid] = {
                "applicable_in_domain": True,
                "verdict": "UNRESOLVED",
                "margin_M_Y": serialize_arb_certified(m_last),
            }

    return {
        "point_id": point_entry["point_id"],
        "label": point_entry["label"],
        "kind": point_entry["kind"],
        "rational_factor": point_entry["rational_factor"],
        "exp_power": point_entry["exp_power"],
        "grid_tier": point_entry["grid_tier"],
        "prior_exposure_status": point_entry["prior_exposure_status"],
        "cutoffs": {
            "T_Y": T_y,
            "D0_raw": cut["D0_raw"],
            "D0_eff": D0_eff,
            "max_chain_length_L_T": l_t,
        },
        "Y_enclosure": serialize_arb_certified(last_eval["Y_ball"]),
        "E_Y": serialize_arb_certified(last_eval["E_Y"]),
        "D_tilde_Y": serialize_arb_certified(last_eval["D_tilde_Y"]),
        "log_Y_times_D_tilde": serialize_arb_certified(last_eval["log_Y_times_D_tilde"]),
        "F_int_T_p2": serialize_arb_certified(last_eval["F_int_T_p2"]),
        "Sigma_diag_p2": serialize_arb_certified(last_eval["Sigma_diag_p2"]),
        "Sigma_off_p2": serialize_arb_certified(last_eval["Sigma_off_p2"]),
        "S_same_Y": serialize_arb_certified(last_eval["S_same_Y"]),
        "S_different_Y": serialize_arb_certified(last_eval["S_different_Y"]),
        "reconstructed_Sigma_off_algebraic_check": serialize_arb_certified(
            last_eval["reconstructed_Sigma_off"]
        ),
        "same_input_reconstruction_residual": serialize_arb_certified(
            last_eval["same_input_reconstruction_residual"]
        ),
        "local_same_chain_hilbert_bound": serialize_arb_certified(
            last_eval["local_same_chain_hilbert_bound"]
        ),
        "probe_evaluations": probe_evals,
        "kl1_sub_budget_evaluations": kl1_evals,
        "tier_escalation_history": tier_history,
        "conflict_records": conflict_records,
        "resource_budget_check": res_chk,
    }


def evaluate_tc063_interval_via_cutoff_case_split_arb(
    interval_id: str,
    Y_lo_frac: Fraction,
    Y_hi_frac: Fraction,
    selberg_table: Dict[str, Any],
    *,
    prec_bits: int = 256,
) -> Dict[str, Any]:
    """Evaluate `S_same`, `S_different`, `Sigma_off(.; 2)`, `D_tilde`, and `TC-063` probe margins
    across a continuous interval `[Y_lo_frac, Y_hi_frac]` by splitting into all exact feasible
    `(T, D_0, D_eff)` cutoff cells (`derive_exact_interval_cutoff_partition`), recording the exact
    binary evaluated interval `evaluated_Y_interval_exact_fractions` at creation (`TASK-TC-062R4`).
    """
    part = derive_exact_interval_cutoff_partition(Y_lo_frac, Y_hi_frac)
    cells = part["feasible_cells"]
    if not cells:
        raise ValueError(f"Empty feasible cutoff partition on [{Y_lo_frac}, {Y_hi_frac}]")

    saved = flint_ctx.prec
    try:
        branches: List[Dict[str, Any]] = []
        union_balls: Dict[str, Optional[arb]] = {
            u_k: None for u_k, _ in REQUIRED_TC063_INTERVAL_UNION_BRANCH_PAIRS
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

            tau = _tau_arb()
            ceil_tau_hi = int(math.ceil(float((tau * y_sub).upper()))) + 2
            use_3z = t_c >= 512
            q_tol = 110
            n_pan = 16 if use_3z else 4

            # Evaluate E_Y and D_tilde_Y on fixed-(T, D0_raw) interval ball y_sub:
            from tc.mixed_arithmetic_covariance import evaluate_fixed_cutoff_on_Y_ball_arb

            base_br = evaluate_fixed_cutoff_on_Y_ball_arb(
                y_sub,
                t_c,
                d0_c,
                prec_bits=prec_bits,
                quad_tol_bits=q_tol,
                selberg_table=selberg_table,
            )
            mf_br = evaluate_dyadic_chain_observables_matrix_free_arb(
                y_sub,
                t_c,
                deff_c,
                ceil_tau_hi,
                selberg_table,
                prec_bits=prec_bits,
                quad_tol_bits=q_tol,
                use_three_zone=use_3z,
                n_panels=n_pan,
            )

            # Local Hilbert bound on y_sub:
            l_tc = max_dyadic_chain_length_L(t_c)
            vecs_br = compute_complete_core_s_Y_and_beta_Y_arb(
                t_c, deff_c, selberg_table["R_osc"], prec_bits=prec_bits + 32
            )
            b_c = [acb(0)] + [
                acb(arb(liouville_lambda_int(n)) * vecs_br["beta_Y"][n]) for n in range(1, t_c + 1)
            ]
            lg_n_sq = [acb(0)] + [acb(arb(n).log() ** 2) for n in range(1, t_c + 1)]
            st_consts = [(k, acb(k) ** (-3), acb(-(arb(k * k) ** (-1)))) for k in range(1, t_c + 1)]
            Yc = acb(y_sub)
            lgYc = acb(y_sub.log())
            Yc_52 = Yc ** (acb(5) / acb(2))
            Yc_2 = Yc * Yc
            log_tau = tau.log()
            tol_l = arb(2) ** (-min(q_tol, 170))

            def _psi_br_cb(u_v: acb, _an: bool) -> acb:
                lg = lgYc + u_v
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_v).exp()
                x2 = Yc_2 * (acb(2) * u_v).exp()
                acc = acb(0)
                for k_i, inv_k3, neg_inv_k2 in st_consts:
                    pk_v = x52 * inv_k3 * (x2 * neg_inv_k2).exp()
                    ps = (acb(1) - b_c[k_i] * inv_lg2) * pk_v
                    acc += ps * ps
                return acc

            def _g2_br_cb(u_v: acb, _an: bool) -> acb:
                lg = lgYc + u_v
                if _an and not bool(lg.real > arb(1) / arb(2)):
                    nb = arb("nan")
                    return acb(nb, nb)
                inv_lg2 = acb(1) / (lg * lg)
                x52 = Yc_52 * (acb(arb(5) / arb(2)) * u_v).exp()
                x2 = Yc_2 * (acb(2) * u_v).exp()
                acc = acb(0)
                for k_i, inv_k3, neg_inv_k2 in st_consts:
                    pk_v = x52 * inv_k3 * (x2 * neg_inv_k2).exp()
                    acc += lg_n_sq[k_i] * (pk_v * pk_v) * inv_lg2
                return acc

            sum_psi_br = acb.integral(
                _psi_br_cb, acb(0), acb(log_tau), rel_tol=tol_l, abs_tol=tol_l
            ).real
            sum_g2_br = acb.integral(
                _g2_br_cb, acb(0), acb(log_tau), rel_tol=tol_l, abs_tol=tol_l
            ).real
            loc_hilb_br = arb(l_tc - 1) * (arb(2) * sum_psi_br + arb(8) * sum_g2_br)

            m_p0_diff = +(mf_br["S_different_Y"] - base_br["log_Y_times_D_tilde"])
            m_neg_diff = +mf_br["S_different_Y"]
            m_same_loc = +(abs(mf_br["S_same_Y"]) - loc_hilb_br)

            br_obs_balls = {
                "E_Y": base_br["E_Y"],
                "D_tilde_Y": base_br["D_tilde_Y"],
                "log_Y_times_D_tilde": base_br["log_Y_times_D_tilde"],
                "Sigma_off_p2": mf_br["Sigma_off_p2"],
                "S_same_Y": mf_br["S_same_Y"],
                "S_different_Y": mf_br["S_different_Y"],
                "M_P0_DIFF": m_p0_diff,
                "M_P_NEG_DIFF": m_neg_diff,
                "M_SAME_LOC": m_same_loc,
            }
            for u_k, b_k in REQUIRED_TC063_INTERVAL_UNION_BRANCH_PAIRS:
                cur_u = union_balls[u_k]
                union_balls[u_k] = (
                    +br_obs_balls[b_k] if cur_u is None else +(cur_u.union(br_obs_balls[b_k]))
                )

            cls_p0 = classify_probe_margin_arb(m_p0_diff)
            cls_neg = classify_probe_margin_arb(m_neg_diff)
            cls_same = classify_probe_margin_arb(m_same_loc)

            br_entry: Dict[str, Any] = {
                "branch_role": "REQUIRED_FEASIBLE_SUBDOMAIN",
                "T_fixed": t_c,
                "D0_raw_fixed": d0_c,
                "D0_eff_fixed": deff_c,
                "required_subdomain_notation": cell["subdomain_notation"],
                "Y_sub_ball": serialize_arb_certified(y_sub),
                "evaluated_Y_interval_exact_fractions": [
                    f"{eval_lo_q.numerator}/{eval_lo_q.denominator}",
                    f"{eval_hi_q.numerator}/{eval_hi_q.denominator}",
                ],
                "evaluated_Y_mid_man_exp": [int(mid_me[0]), int(mid_me[1])],
                "evaluated_Y_rad_man_exp": [int(rad_me[0]), int(rad_me[1])],
                "domain_provenance_kind": "EVALUATED_AT_CREATION",
                "E_Y": serialize_arb_certified(br_obs_balls["E_Y"]),
                "D_tilde_Y": serialize_arb_certified(br_obs_balls["D_tilde_Y"]),
                "log_Y_times_D_tilde": serialize_arb_certified(br_obs_balls["log_Y_times_D_tilde"]),
                "Sigma_off_p2": serialize_arb_certified(br_obs_balls["Sigma_off_p2"]),
                "S_same_Y": serialize_arb_certified(br_obs_balls["S_same_Y"]),
                "S_different_Y": serialize_arb_certified(br_obs_balls["S_different_Y"]),
                "M_P0_DIFF": serialize_arb_certified(m_p0_diff),
                "M_P_NEG_DIFF": serialize_arb_certified(m_neg_diff),
                "M_SAME_LOC": serialize_arb_certified(m_same_loc),
                "TC063_P0_DIFF_branch_classification": cls_p0,
                "TC063_P_NEG_DIFF_branch_classification": cls_neg,
                "TC063_SAME_LOC_branch_classification": cls_same,
            }
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
        for u_k, _ in REQUIRED_TC063_INTERVAL_UNION_BRANCH_PAIRS:
            ub = union_balls[u_k]
            assert ub is not None
            out_rec[u_k] = serialize_arb_certified(ub)

        out_rec["TC063_P0_DIFF_interval_classification"] = classify_probe_margin_arb(
            union_balls["union_M_P0_DIFF"]
        )
        out_rec["TC063_P_NEG_DIFF_interval_classification"] = classify_probe_margin_arb(
            union_balls["union_M_P_NEG_DIFF"]
        )
        out_rec["TC063_SAME_LOC_interval_classification"] = classify_probe_margin_arb(
            union_balls["union_M_SAME_LOC"]
        )
        return out_rec
    finally:
        flint_ctx.prec = saved


def _dyadic_man_exp_to_fraction(man: int, exp: int) -> Fraction:
    return Fraction(man) * (1 << exp) if exp >= 0 else Fraction(man, 1 << (-exp))


_TC063_ALT_DOMAIN_KEYS = (
    "evaluated_Y_symbolic_bounds",
    "evaluated_Y_subintervals_exact_fractions",
    "evaluated_Y_inner_interval_exact_fractions",
    "evaluated_Y_inner_symbolic_bounds",
    "historical_domain_reconstruction",
)


def _verify_tc063_branch_binary_man_exp_consistency(
    br: Dict[str, Any],
    y_sub_parsed: Optional[Dict[str, Any]],
    triple: Tuple[int, int, int],
) -> List[Dict[str, Any]]:
    """Verify exact dyadic equality between `(evaluated_Y_mid_man_exp, evaluated_Y_rad_man_exp)`
    and `evaluated_Y_interval_exact_fractions`, outward enclosure by `Y_sub_ball` even when
    `evaluated_Y_interval_exact_fractions` is omitted, and absence of unlinked alternate domain
    provenance claims without full binary provenance (`R2-1`).
    """
    errs: List[Dict[str, Any]] = []
    has_ef = "evaluated_Y_interval_exact_fractions" in br
    has_mid = "evaluated_Y_mid_man_exp" in br
    has_rad = "evaluated_Y_rad_man_exp" in br
    has_alt = any(k_alt in br for k_alt in _TC063_ALT_DOMAIN_KEYS)
    if has_alt and not (has_ef and has_mid and has_rad):
        errs.append(
            {
                "conflict_type": "UNLINKED_ALTERNATE_DOMAIN_METADATA_WITHOUT_BINARY_PROVENANCE",
                "triple": list(triple),
            }
        )
        return errs
    if not (has_ef or has_mid or has_rad):
        return errs
    mid_me = br.get("evaluated_Y_mid_man_exp")
    rad_me = br.get("evaluated_Y_rad_man_exp")
    if (
        not (has_mid and has_rad)
        or not isinstance(mid_me, list)
        or len(mid_me) != 2
        or not all(isinstance(x, int) and not isinstance(x, bool) for x in mid_me)
        or not isinstance(rad_me, list)
        or len(rad_me) != 2
        or not all(isinstance(x, int) and not isinstance(x, bool) for x in rad_me)
        or rad_me[0] < 0
    ):
        errs.append(
            {
                "conflict_type": "MALFORMED_OR_INCOMPLETE_BINARY_DOMAIN_METADATA",
                "triple": list(triple),
            }
        )
        return errs
    try:
        mid_q = _dyadic_man_exp_to_fraction(mid_me[0], mid_me[1])
        rad_q = _dyadic_man_exp_to_fraction(rad_me[0], rad_me[1])
        lo_bin = mid_q - rad_q
        hi_bin = mid_q + rad_q
    except Exception:  # noqa: BLE001
        errs.append({"conflict_type": "UNPARSEABLE_BINARY_DOMAIN_FRACTIONS", "triple": list(triple)})
        return errs
    if lo_bin > hi_bin or y_sub_parsed is None or not (
        y_sub_parsed["c_lo"] <= lo_bin and hi_bin <= y_sub_parsed["c_hi"]
    ):
        errs.append(
            {
                "conflict_type": "Y_SUB_BALL_DOES_NOT_ENCLOSE_BINARY_EVALUATED_DOMAIN",
                "triple": list(triple),
            }
        )
        return errs
    if not has_ef:
        # Unlinked outward ball with valid enclosed binary `man_exp` and zero alternate domain
        # claims is handled downstream as an uncertified coverage gap (`TC-062R4`).
        return errs
    ef = br.get("evaluated_Y_interval_exact_fractions")
    if (
        not isinstance(ef, list)
        or len(ef) != 2
        or not all(isinstance(s, str) and s.strip() for s in ef)
    ):
        errs.append(
            {
                "conflict_type": "MALFORMED_OR_INCOMPLETE_BINARY_DOMAIN_METADATA",
                "triple": list(triple),
            }
        )
        return errs
    try:
        ef_lo = Fraction(ef[0])
        ef_hi = Fraction(ef[1])
    except Exception:  # noqa: BLE001
        errs.append({"conflict_type": "UNPARSEABLE_BINARY_DOMAIN_FRACTIONS", "triple": list(triple)})
        return errs
    if lo_bin != ef_lo or hi_bin != ef_hi:
        errs.append(
            {
                "conflict_type": "BINARY_MAN_EXP_EXACT_FRACTION_MISMATCH",
                "triple": list(triple),
                "man_exp_bounds": [str(lo_bin), str(hi_bin)],
                "recorded_exact_fractions": [str(ef_lo), str(ef_hi)],
            }
        )
    return errs


def audit_continuous_interval_split_certificate_tc063(
    split_key: str,
    split_obj: Dict[str, Any],
    *,
    cand_y0_by_id: Optional[Dict[str, Fraction]] = None,
) -> Dict[str, Any]:
    """Audit a serialized `TC-063` continuous interval split certificate under all `TC-062R4`
    integrity, binary `man_exp` consistency, union-containment, domain-threshold `Y0`
    witness-admissibility, and exact-coverage rules.
    """
    eff_y0: Dict[str, Fraction] = {
        "TC063-P0-DIFF": Fraction(64, 1),
        "TC063-P-HALF-DIFF": Fraction(16, 1),
        "TC063-P-NEG-DIFF": Fraction(64, 1),
        "TC063-SAME-LOCAL-HILBERT": Fraction(2, 1),
    }
    if cand_y0_by_id is not None:
        for k_id, v_q in cand_y0_by_id.items():
            if k_id in eff_y0:
                eff_y0[k_id] = Fraction(v_q)

    probe_map = (
        ("TC063-P0-DIFF", "M_P0_DIFF", "TC063_P0_DIFF_branch_classification"),
        ("TC063-P-HALF-DIFF", "M_P0_DIFF", "TC063_P0_DIFF_branch_classification"),
        ("TC063-P-NEG-DIFF", "M_P_NEG_DIFF", "TC063_P_NEG_DIFF_branch_classification"),
        ("TC063-SAME-LOCAL-HILBERT", "M_SAME_LOC", "TC063_SAME_LOC_branch_classification"),
    )

    conflicts: List[Dict[str, Any]] = []
    coverage_gaps: List[Dict[str, Any]] = []

    if split_key not in PRESCRIBED_TC063_INTERVAL_SPLITS:
        return {
            "certification_integrity_ok": False,
            "coverage_complete": False,
            "all_required_branches_resolved": False,
            "conflicts": [{"conflict_type": "UNKNOWN_INTERVAL_SPLIT_KEY", "split_key": split_key}],
            "coverage_gaps": [],
            "derived_probe_outcomes": {
                pid: CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME for pid, _, _ in probe_map
            },
        }

    exp_lo, exp_hi = PRESCRIBED_TC063_INTERVAL_SPLITS[split_key]
    try:
        rec_lo = Fraction(str(split_obj.get("Y_lo_fraction", "")))
        rec_hi = Fraction(str(split_obj.get("Y_hi_fraction", "")))
    except Exception:  # noqa: BLE001
        rec_lo, rec_hi = Fraction(-1, 1), Fraction(-2, 1)

    if rec_lo != exp_lo or rec_hi != exp_hi:
        coverage_gaps.append(
            {
                "gap_type": "ALTERED_PRESCRIBED_INTERVAL_ENDPOINTS",
                "expected": [str(exp_lo), str(exp_hi)],
                "recorded": [split_obj.get("Y_lo_fraction"), split_obj.get("Y_hi_fraction")],
            }
        )

    part = derive_exact_interval_cutoff_partition(exp_lo, exp_hi)
    req_triples = [tuple(c["cutoff_triple"]) for c in part["feasible_cells"]]

    # Per-probe effective domain `[max(exp_lo, Y0), exp_hi]` and required feasible cells:
    probe_eff_lo: Dict[str, Optional[Fraction]] = {}
    probe_req_triples: Dict[str, List[Tuple[int, int, int]]] = {}
    part_cache_by_lo: Dict[Fraction, List[Tuple[int, int, int]]] = {exp_lo: req_triples}
    for pid, _, _ in probe_map:
        lo_p = max(exp_lo, eff_y0[pid])
        if lo_p > exp_hi:
            probe_eff_lo[pid] = None
            probe_req_triples[pid] = []
        else:
            probe_eff_lo[pid] = lo_p
            if lo_p not in part_cache_by_lo:
                p_sub = derive_exact_interval_cutoff_partition(lo_p, exp_hi)
                part_cache_by_lo[lo_p] = [tuple(c["cutoff_triple"]) for c in p_sub["feasible_cells"]]
            probe_req_triples[pid] = part_cache_by_lo[lo_p]

    branches = split_obj.get("branches")
    if not isinstance(branches, list) or len(branches) == 0:
        coverage_gaps.append({"gap_type": "EMPTY_OR_MISSING_BRANCH_LIST"})
        branches = []

    if split_obj.get("active_branch_count") != len(branches):
        conflicts.append(
            {
                "conflict_type": "ACTIVE_BRANCH_COUNT_MISMATCH",
                "recorded": split_obj.get("active_branch_count"),
                "actual": len(branches),
            }
        )

    parsed_unions: Dict[str, Optional[Dict[str, Any]]] = {}
    for u_k, _ in REQUIRED_TC063_INTERVAL_UNION_BRANCH_PAIRS:
        u_p = _parse_serialized_arb_enclosure_tc062(split_obj.get(u_k))
        parsed_unions[u_k] = u_p
        if u_p is None:
            conflicts.append({"conflict_type": "MALFORMED_UNION_BALL", "field": u_k})

    seen_req: set[Tuple[int, int, int]] = set()
    req_branch_verdicts: Dict[str, Dict[Tuple[int, int, int], str]] = {
        pid: {} for pid, _, _ in probe_map
    }
    probe_covered_triples: Dict[str, set[Tuple[int, int, int]]] = {
        pid: set() for pid, _, _ in probe_map
    }
    admissible_fail_witnesses: Dict[str, List[Tuple[int, int, int]]] = {
        pid: [] for pid, _, _ in probe_map
    }

    checked_cls_fields_per_branch = (
        ("TC063-P0-DIFF", "M_P0_DIFF", "TC063_P0_DIFF_branch_classification"),
        ("TC063-P-NEG-DIFF", "M_P_NEG_DIFF", "TC063_P_NEG_DIFF_branch_classification"),
        ("TC063-SAME-LOCAL-HILBERT", "M_SAME_LOC", "TC063_SAME_LOC_branch_classification"),
    )

    for br in branches:
        if not isinstance(br, dict):
            conflicts.append({"conflict_type": "MALFORMED_BRANCH_ENTRY"})
            continue
        t_f = br.get("T_fixed")
        d0_f = br.get("D0_raw_fixed")
        deff_f = br.get("D0_eff_fixed")
        role = br.get("branch_role")
        if (
            not isinstance(t_f, int)
            or isinstance(t_f, bool)
            or not isinstance(d0_f, int)
            or isinstance(d0_f, bool)
            or not isinstance(deff_f, int)
            or isinstance(deff_f, bool)
            or deff_f != min(d0_f, max(0, t_f - 1))
        ):
            conflicts.append({"conflict_type": "INVALID_BRANCH_CUTOFF_TRIPLE"})
            continue

        triple = (t_f, d0_f, deff_f)
        if role not in ("REQUIRED_FEASIBLE_SUBDOMAIN", "POSSIBLY_EMPTY_CONSERVATIVE_BRANCH"):
            conflicts.append({"conflict_type": "UNRECOGNIZED_BRANCH_ROLE", "triple": list(triple)})
            continue

        if triple in req_triples:
            if role != "REQUIRED_FEASIBLE_SUBDOMAIN":
                conflicts.append({"conflict_type": "MISLABELED_REQUIRED_BRANCH", "triple": list(triple)})
            if triple in seen_req:
                conflicts.append({"conflict_type": "DUPLICATE_REQUIRED_BRANCH", "triple": list(triple)})
            seen_req.add(triple)

        # Check union containment across all 9 observable pairs:
        for u_k, b_k in REQUIRED_TC063_INTERVAL_UNION_BRANCH_PAIRS:
            b_p = _parse_serialized_arb_enclosure_tc062(br.get(b_k))
            u_p = parsed_unions[u_k]
            if b_p is None:
                conflicts.append(
                    {"conflict_type": "MALFORMED_BRANCH_BALL", "field": b_k, "triple": list(triple)}
                )
            elif u_p is not None and not _serialized_union_contains_branch_tc062(u_p, b_p):
                conflicts.append(
                    {
                        "conflict_type": "UNION_DOES_NOT_CONTAIN_BRANCH",
                        "union_field": u_k,
                        "branch_field": b_k,
                        "triple": list(triple),
                    }
                )

        y_sub_p = _parse_serialized_arb_enclosure_tc062(br.get("Y_sub_ball"))
        if y_sub_p is None:
            conflicts.append({"conflict_type": "MALFORMED_Y_SUB_BALL", "triple": list(triple)})
        bin_errs = _verify_tc063_branch_binary_man_exp_consistency(br, y_sub_p, triple)
        if bin_errs:
            conflicts.extend(bin_errs)

        dom_by_lo: Dict[Fraction, Dict[str, Any]] = {}
        dom_res = _evaluate_branch_domain_admissibility_tc062(
            br,
            y_sub_parsed=y_sub_p,
            prescribed_Y_lo=exp_lo,
            prescribed_Y_hi=exp_hi,
            cutoff_triple=triple,
            split_key=split_key,
        )
        dom_by_lo[exp_lo] = dom_res
        if dom_res["conflicts"]:
            conflicts.extend(dom_res["conflicts"])
        if triple in req_triples and not dom_res["complete_subdomain_coverage"]:
            coverage_gaps.append(
                {
                    "gap_type": "INCOMPLETE_BRANCH_EVALUATION_COVERAGE",
                    "triple": list(triple),
                    "coverage_status": dom_res["coverage_status"],
                    "coverage_reason": dom_res["coverage_reason"],
                }
            )

        branch_exp_verdict_by_field: Dict[str, Optional[str]] = {}
        for rep_pid, m_field, cls_field in checked_cls_fields_per_branch:
            cls_rec = br.get(cls_field)
            m_p = _parse_serialized_arb_enclosure_tc062(br.get(m_field))
            if not isinstance(cls_rec, dict) or m_p is None:
                conflicts.append(
                    {"conflict_type": "MALFORMED_BRANCH_MARGIN_CLASSIFICATION", "probe_id": rep_pid}
                )
                branch_exp_verdict_by_field[m_field] = None
                continue
            exp_v = (
                "PASS"
                if m_p["c_hi"] <= 0
                else ("FAIL" if m_p["c_lo"] > 0 else "UNRESOLVED")
            )
            if cls_rec.get("verdict") != exp_v:
                conflicts.append(
                    {
                        "conflict_type": "BRANCH_VERDICT_DISAGREES_WITH_MARGIN",
                        "probe_id": rep_pid,
                        "claimed": cls_rec.get("verdict"),
                        "expected": exp_v,
                    }
                )
            branch_exp_verdict_by_field[m_field] = exp_v

        for pid, m_field, _ in probe_map:
            exp_v_p = branch_exp_verdict_by_field.get(m_field)
            lo_p = probe_eff_lo[pid]
            if exp_v_p is None or lo_p is None:
                continue
            if lo_p not in dom_by_lo:
                dom_by_lo[lo_p] = _evaluate_branch_domain_admissibility_tc062(
                    br,
                    y_sub_parsed=y_sub_p,
                    prescribed_Y_lo=lo_p,
                    prescribed_Y_hi=exp_hi,
                    cutoff_triple=triple,
                    split_key=split_key,
                )
            dom_p = dom_by_lo[lo_p]
            if triple in probe_req_triples[pid]:
                req_branch_verdicts[pid][triple] = exp_v_p
                if dom_p["complete_subdomain_coverage"]:
                    probe_covered_triples[pid].add(triple)
            if exp_v_p == "FAIL" and dom_p["can_certify_refutation"] and not bin_errs:
                admissible_fail_witnesses[pid].append(triple)

    for req_t in req_triples:
        if req_t not in seen_req:
            coverage_gaps.append({"gap_type": "MISSING_REQUIRED_FEASIBLE_BRANCH", "triple": list(req_t)})

    # Audit union margin classifications:
    union_cls_map = (
        ("TC063-P0-DIFF", "union_M_P0_DIFF", "TC063_P0_DIFF_interval_classification"),
        ("TC063-P-NEG-DIFF", "union_M_P_NEG_DIFF", "TC063_P_NEG_DIFF_interval_classification"),
        ("TC063-SAME-LOCAL-HILBERT", "union_M_SAME_LOC", "TC063_SAME_LOC_interval_classification"),
    )
    for pid, u_m_field, u_cls_field in union_cls_map:
        u_cls = split_obj.get(u_cls_field)
        u_mp = parsed_unions[u_m_field]
        if not isinstance(u_cls, dict) or u_mp is None:
            conflicts.append(
                {"conflict_type": "MALFORMED_UNION_MARGIN_CLASSIFICATION", "probe_id": pid}
            )
            continue
        exp_uv = (
            "PASS"
            if u_mp["c_hi"] <= 0
            else ("FAIL" if u_mp["c_lo"] > 0 else "UNRESOLVED")
        )
        if u_cls.get("verdict") != exp_uv:
            conflicts.append(
                {
                    "conflict_type": "UNION_VERDICT_DISAGREES_WITH_MARGIN",
                    "probe_id": pid,
                    "claimed": u_cls.get("verdict"),
                    "expected": exp_uv,
                }
            )

    integrity_ok = len(conflicts) == 0
    coverage_ok = integrity_ok and len(coverage_gaps) == 0
    all_req_resolved = integrity_ok and all(
        req_t in req_branch_verdicts[pid]
        and req_branch_verdicts[pid][req_t] in ("PASS", "FAIL")
        for pid, _, _ in probe_map
        for req_t in probe_req_triples[pid]
    )

    derived_outcomes: Dict[str, str] = {}
    for pid, _, _ in probe_map:
        if not integrity_ok:
            derived_outcomes[pid] = CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
        elif probe_eff_lo[pid] is None:
            derived_outcomes[pid] = "OUT_OF_DOMAIN_NOT_APPLICABLE"
        elif len(admissible_fail_witnesses[pid]) > 0:
            derived_outcomes[pid] = "REFUTED_BY_CERTIFIED_WITNESS"
        elif (
            rec_lo == exp_lo
            and rec_hi == exp_hi
            and len(probe_req_triples[pid]) > 0
            and all(
                rt in probe_covered_triples[pid]
                and req_branch_verdicts[pid].get(rt) == "PASS"
                for rt in probe_req_triples[pid]
            )
        ):
            derived_outcomes[pid] = "SURVIVED_TESTED_POINTS"
        else:
            derived_outcomes[pid] = "UNRESOLVED/INCOMPLETE_COVERAGE"

    return {
        "certification_integrity_ok": integrity_ok,
        "coverage_complete": coverage_ok,
        "all_required_branches_resolved": all_req_resolved,
        "conflicts": conflicts,
        "coverage_gaps": coverage_gaps,
        "derived_probe_outcomes": derived_outcomes,
    }


def aggregate_tc063_section5_and_derive_outcomes(
    sec5_raw: Dict[str, Any],
    protocol_obj: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Shared `TC-063` Section 5 & top-level 6-dimension outcome aggregator (wired identically
    into generator and metadata reprocessor).
    """
    reg_points = protocol_obj["unseen_validation_schedule"]["points"]
    reg_ids = [p["point_id"] for p in reg_points]
    reg_pt_by_id = {p["point_id"]: p for p in reg_points}
    probes = protocol_obj["frozen_candidate_probes"]
    probe_ids = [p["probe_id"] for p in probes]
    all_cand_ids = probe_ids + ["KL1_same_chain", "KL1_different_chain"]
    cand_y0_by_id: Dict[str, Fraction] = {
        p["probe_id"]: Fraction(str(p["domain_threshold_Y0"])) for p in probes
    }
    cand_y0_by_id["KL1_same_chain"] = Fraction(64, 1)
    cand_y0_by_id["KL1_different_chain"] = Fraction(64, 1)

    eval_rows = sec5_raw.get("holdout_point_evaluations")
    if not isinstance(eval_rows, list):
        eval_rows = []

    conflicts: List[Dict[str, Any]] = []
    coverage_gaps: List[Dict[str, Any]] = []

    seen_pids: List[str] = []
    admissible_spec_y_by_pid: Dict[str, arb] = {}
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for row in eval_rows:
            if not isinstance(row, dict):
                conflicts.append({"conflict_type": "MALFORMED_HOLDOUT_ROW"})
                continue
            pid = row.get("point_id")
            if not isinstance(pid, str) or pid not in reg_pt_by_id:
                conflicts.append({"conflict_type": "UNREGISTERED_OR_MISSING_POINT_ID", "point_id": pid})
                continue
            if pid in seen_pids:
                conflicts.append({"conflict_type": "DUPLICATE_POINT_ID", "point_id": pid})
                continue
            seen_pids.append(pid)
            if row.get("conflict_records"):
                conflicts.extend(row["conflict_records"])

            spec = _parse_tc063_scale_spec(reg_pt_by_id[pid])
            spec_y = spec.evaluate_arb(256)
            exp_cut = certify_exact_scale_cutoffs(spec, base_prec_bits=256)
            y_enc = _parse_serialized_arb_enclosure_tc062(row.get("Y_enclosure"))
            if (
                y_enc is None
                or not bool(
                    _frac_to_arb(y_enc["c_lo"]) <= spec_y.lower()
                    and spec_y.upper() <= _frac_to_arb(y_enc["c_hi"])
                )
                or (y_enc["c_hi"] - y_enc["c_lo"]) > Fraction(1, 10 ** 20)
            ):
                conflicts.append({"conflict_type": "HOLDOUT_Y_ENCLOSURE_MISMATCH", "point_id": pid})
                continue
            row_cut = row.get("cutoffs")
            if (
                not isinstance(row_cut, dict)
                or row_cut.get("T_Y") != exp_cut["T_Y"]
                or row_cut.get("D0_raw") != exp_cut["D0_raw"]
                or row_cut.get("D0_eff") != exp_cut["D0_eff"]
            ):
                conflicts.append({"conflict_type": "HOLDOUT_CUTOFF_MISMATCH", "point_id": pid})
                continue
            obs_ball_ok = True
            for obs_f in (
                "E_Y",
                "D_tilde_Y",
                "log_Y_times_D_tilde",
                "F_int_T_p2",
                "Sigma_diag_p2",
                "Sigma_off_p2",
                "S_same_Y",
                "S_different_Y",
                "reconstructed_Sigma_off_algebraic_check",
                "same_input_reconstruction_residual",
                "local_same_chain_hilbert_bound",
            ):
                obs_p = _parse_serialized_arb_enclosure_tc062(row.get(obs_f))
                if obs_p is None or (
                    obs_f == "same_input_reconstruction_residual"
                    and not (obs_p["c_lo"] <= 0 <= obs_p["c_hi"])
                ):
                    conflicts.append(
                        {
                            "conflict_type": "MALFORMED_HOLDOUT_OBSERVABLE_BALL",
                            "point_id": pid,
                            "field": obs_f,
                        }
                    )
                    obs_ball_ok = False
            if not obs_ball_ok:
                continue
            admissible_spec_y_by_pid[pid] = spec_y
    finally:
        flint_ctx.prec = saved_prec

    for rid in reg_ids:
        if rid not in seen_pids:
            coverage_gaps.append({"gap_type": "MISSING_REGISTERED_POINT", "point_id": rid})

    # Audit point-level candidate margins:
    point_verdicts_by_cand: Dict[str, List[str]] = {cid: [] for cid in all_cand_ids}
    point_applicable_counts: Dict[str, int] = {cid: 0 for cid in all_cand_ids}
    saved_prec2 = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for row in eval_rows:
            if not isinstance(row, dict):
                continue
            pid = row.get("point_id")
            if pid not in admissible_spec_y_by_pid:
                continue
            spec_y = admissible_spec_y_by_pid[pid]
            pe = row.get("probe_evaluations")
            ke = row.get("kl1_sub_budget_evaluations")
            if not isinstance(pe, dict) or not isinstance(ke, dict):
                conflicts.append(
                    {"conflict_type": "MALFORMED_CANDIDATE_EVALUATION_CONTAINER", "point_id": pid}
                )
                continue
            for cid in all_cand_ids:
                container_c = pe if cid in probe_ids else ke
                if cid not in container_c:
                    coverage_gaps.append(
                        {"gap_type": "MISSING_CANDIDATE_EVALUATION", "point_id": pid, "candidate_id": cid}
                    )
                    continue
                rec_c = container_c.get(cid)
                if not isinstance(rec_c, dict):
                    conflicts.append(
                        {"conflict_type": "MALFORMED_CANDIDATE_EVALUATION_RECORD", "point_id": pid, "candidate_id": cid}
                    )
                    continue
                m_chk = _audit_serialized_margin_verdict_tc062(rec_c.get("margin_M_Y"))
                if m_chk == "CONFLICT":
                    conflicts.append(
                        {"conflict_type": "MALFORMED_CANDIDATE_MARGIN_BALL", "point_id": pid, "candidate_id": cid}
                    )
                    continue
                y0_b = _frac_to_arb(cand_y0_by_id[cid])
                exp_app = bool(spec_y >= y0_b)
                claimed_app = bool(rec_c.get("applicable_in_domain", False))
                if claimed_app != exp_app:
                    conflicts.append(
                        {
                            "conflict_type": "CANDIDATE_APPLICABILITY_DOMAIN_MISMATCH",
                            "point_id": pid,
                            "candidate_id": cid,
                            "claimed": claimed_app,
                            "expected": exp_app,
                        }
                    )
                    continue
                if not claimed_app:
                    if rec_c.get("verdict") != "OUT_OF_DOMAIN_NOT_APPLICABLE":
                        conflicts.append(
                            {"conflict_type": "OUT_OF_DOMAIN_VERDICT_CONFLICT", "candidate_id": cid}
                        )
                    continue
                point_applicable_counts[cid] += 1
                verd = rec_c.get("verdict")
                if verd == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT or verd != m_chk:
                    conflicts.append(
                        {
                            "conflict_type": "POINT_VERDICT_DISAGREES_WITH_MARGIN",
                            "point_id": pid,
                            "candidate_id": cid,
                            "claimed": verd,
                            "expected": m_chk,
                        }
                    )
                else:
                    point_verdicts_by_cand[cid].append(verd)
    finally:
        flint_ctx.prec = saved_prec2

    # Audit continuous interval case splits:
    splits_raw = sec5_raw.get("continuous_interval_case_splits")
    if not isinstance(splits_raw, dict):
        splits_raw = {}
        coverage_gaps.append({"gap_type": "MISSING_CONTINUOUS_INTERVAL_SPLITS"})

    interval_audits: Dict[str, Any] = {}
    for req_ik in PRESCRIBED_TC063_INTERVAL_SPLITS:
        if req_ik not in splits_raw or not isinstance(splits_raw[req_ik], dict):
            coverage_gaps.append({"gap_type": "MISSING_PRESCRIBED_INTERVAL_SPLIT", "interval_id": req_ik})
            continue
        ia = audit_continuous_interval_split_certificate_tc063(
            req_ik, splits_raw[req_ik], cand_y0_by_id=cand_y0_by_id
        )
        interval_audits[req_ik] = ia
        conflicts.extend(ia["conflicts"])
        coverage_gaps.extend(ia["coverage_gaps"])
    for extra_ik in splits_raw:
        if extra_ik not in PRESCRIBED_TC063_INTERVAL_SPLITS:
            conflicts.append({"conflict_type": "UNREGISTERED_INTERVAL_SPLIT", "interval_id": extra_ik})

    integrity_ok = len(conflicts) == 0
    coverage_complete = integrity_ok and len(coverage_gaps) == 0

    saved_prec3 = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        expected_applicable_points_by_cand: Dict[str, int] = {}
        for cid in all_cand_ids:
            y0_b = _frac_to_arb(cand_y0_by_id[cid])
            cnt_app = 0
            for p_entry in reg_points:
                sp_r = _parse_tc063_scale_spec(p_entry)
                if bool(sp_r.evaluate_arb(256) >= y0_b):
                    cnt_app += 1
            expected_applicable_points_by_cand[cid] = cnt_app
    finally:
        flint_ctx.prec = saved_prec3

    all_points_resolved = integrity_ok and all(
        (
            expected_applicable_points_by_cand[cid] == 0
            or (
                point_applicable_counts[cid] == expected_applicable_points_by_cand[cid]
                and len(point_verdicts_by_cand[cid]) == point_applicable_counts[cid]
                and all(v in ("PASS", "FAIL") for v in point_verdicts_by_cand[cid])
            )
        )
        for cid in all_cand_ids
    )
    all_intervals_resolved = integrity_ok and (
        len(interval_audits) == len(PRESCRIBED_TC063_INTERVAL_SPLITS)
        and all(ia["all_required_branches_resolved"] for ia in interval_audits.values())
    )
    all_req_resolved = bool(all_points_resolved and all_intervals_resolved)

    per_cand_outcomes: Dict[str, str] = {}
    for cid in all_cand_ids:
        if not integrity_ok:
            per_cand_outcomes[cid] = CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
            continue
        pt_fail = "FAIL" in point_verdicts_by_cand[cid]
        int_fail = any(
            ia["derived_probe_outcomes"].get(cid) == "REFUTED_BY_CERTIFIED_WITNESS"
            for ia in interval_audits.values()
        )
        if pt_fail or int_fail:
            per_cand_outcomes[cid] = "REFUTED_BY_CERTIFIED_WITNESS"
        elif (
            coverage_complete
            and point_applicable_counts[cid] == expected_applicable_points_by_cand[cid]
            and len(point_verdicts_by_cand[cid]) == expected_applicable_points_by_cand[cid]
            and all(v == "PASS" for v in point_verdicts_by_cand[cid])
            and len(interval_audits) == len(PRESCRIBED_TC063_INTERVAL_SPLITS)
            and all(
                (
                    ia["derived_probe_outcomes"].get(cid)
                    in ("SURVIVED_TESTED_POINTS", "OUT_OF_DOMAIN_NOT_APPLICABLE")
                    if cid in probe_ids
                    else True
                )
                for ia in interval_audits.values()
            )
            and (
                expected_applicable_points_by_cand[cid] > 0
                or any(
                    ia["derived_probe_outcomes"].get(cid) == "SURVIVED_TESTED_POINTS"
                    for ia in interval_audits.values()
                )
            )
        ):
            per_cand_outcomes[cid] = (
                "PROVED_UNIFORMLY"
                if cid == "TC063-SAME-LOCAL-HILBERT"
                else "SURVIVED_TESTED_POINTS"
            )
        else:
            per_cand_outcomes[cid] = "UNRESOLVED/INCOMPLETE_COVERAGE"

    # Resource compliance summary across evaluated rows:
    res_limits = protocol_obj.get("numerical_settings_and_escalation_rules", {}).get(
        "resource_limits", {}
    )
    max_wall_sec = float(res_limits.get("max_wall_seconds_per_point", 300.0))
    max_rss_mb = float(res_limits.get("max_rss_megabytes", 4096.0))
    res_checks: List[Dict[str, Any]] = []
    for row in eval_rows:
        if not isinstance(row, dict):
            continue
        if row.get("point_id") == "TC063-HO-UNSEEN-96":
            row["prior_exposure_audit_note"] = (
                "Y = 96 had a prior E(96) evaluation in TC-059 "
                "(data/tc_dyadic_power_lift_primitive_correlation.json), with 0 prior evaluations "
                "for D_tilde, J, F, Sigma_off, S_same, or S_different and 0 calibration usage."
            )
        hist = row.get("tier_escalation_history")
        if isinstance(hist, list) and len(hist) > 0:
            rc_p = evaluate_point_resource_compliance(
                hist,
                max_wall_sec=max_wall_sec,
                max_rss_mb=max_rss_mb,
            )
            row["resource_budget_check"] = rc_p
            res_checks.append(rc_p)
    res_summary = aggregate_section_resource_compliance(
        res_checks,
        registered_count=len(reg_ids),
        distinct_evaluated_count=len(seen_pids),
    )
    res_status = res_summary["overall_resource_budget_status"]

    open_cands = [c for c in all_cand_ids if c != "TC063-SAME-LOCAL-HILBERT"]
    refuted_cands = [c for c in all_cand_ids if per_cand_outcomes[c] == "REFUTED_BY_CERTIFIED_WITNESS"]
    survived_cands = [
        c for c in open_cands if per_cand_outcomes[c] == "SURVIVED_TESTED_POINTS"
    ]
    any_refuted = len(refuted_cands) > 0
    all_open_refuted = all(
        per_cand_outcomes[c] == "REFUTED_BY_CERTIFIED_WITNESS" for c in open_cands
    )
    any_unresolved_or_incomplete = any(
        per_cand_outcomes[c] == "UNRESOLVED/INCOMPLETE_COVERAGE" for c in all_cand_ids
    )
    all_survived = all(
        per_cand_outcomes[c] in ("SURVIVED_TESTED_POINTS", "PROVED_UNIFORMLY")
        for c in all_cand_ids
    )
    primary_p0_outcome = per_cand_outcomes.get(
        "TC063-P0-DIFF", "UNRESOLVED/INCOMPLETE_COVERAGE"
    )

    if not integrity_ok:
        exec_status = "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED"
        holdout_outcome = CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
        outcome_code = "BLOCKED_INTEGRITY_CONFLICT"
        sec5_pass = False
    elif all_open_refuted and not any_unresolved_or_incomplete:
        exec_status = "CERTIFIED_ALL_OPEN_CANDIDATES_REFUTED"
        holdout_outcome = "REFUTED_BY_CERTIFIED_WITNESS"
        outcome_code = "ALL_OPEN_HOLDOUT_CANDIDATES_REFUTED"
        sec5_pass = bool(
            per_cand_outcomes.get("TC063-SAME-LOCAL-HILBERT") == "PROVED_UNIFORMLY"
        )
    elif any_refuted and not any_unresolved_or_incomplete and coverage_complete and all_req_resolved:
        exec_status = "CERTIFIED_EVALUATION_COMPLETE"
        holdout_outcome = "MIXED_ZERO_SLACK_REFUTED_LOG_SAVING_SURVIVED"
        outcome_code = "SAME_CHAIN_PROVED_ZERO_SLACK_DIFF_REFUTED_LOG_SAVING_SURVIVED_OPEN"
        sec5_pass = bool(
            per_cand_outcomes.get("TC063-SAME-LOCAL-HILBERT") == "PROVED_UNIFORMLY"
        )
    elif any_refuted:
        exec_status = "PARTIAL_CERTIFICATION_REFUTED_WITH_UNRESOLVED_OR_INCOMPLETE_SIBLINGS"
        holdout_outcome = "PARTIAL_REFUTATION_WITH_UNRESOLVED_OR_INCOMPLETE_SIBLINGS"
        outcome_code = "PARTIAL_REFUTATION_INCOMPLETE_REMAINING"
        sec5_pass = False
    elif coverage_complete and all_req_resolved and all_survived:
        exec_status = "CERTIFIED_EVALUATION_COMPLETE"
        holdout_outcome = "SURVIVED_TESTED_POINTS"
        outcome_code = "SAME_CHAIN_PROVED_AND_DISTINCT_CHAIN_HOLDOUT_SURVIVED_OPEN"
        sec5_pass = True
    elif not coverage_complete:
        exec_status = "INCOMPLETE_HOLDOUT_COVERAGE"
        holdout_outcome = "UNRESOLVED/INCOMPLETE_COVERAGE"
        outcome_code = "INCOMPLETE_COVERAGE"
        sec5_pass = False
    else:
        exec_status = "UNRESOLVED_MARGIN_AFTER_ESCALATION"
        holdout_outcome = "UNRESOLVED/INCOMPLETE_COVERAGE"
        outcome_code = "UNRESOLVED_MARGIN"
        sec5_pass = False

    sec5_out = dict(sec5_raw)
    sec5_out.update(
        {
            "registered_unseen_point_count": len(reg_ids),
            "evaluated_unseen_point_count": len(seen_pids),
            "certification_integrity_ok": integrity_ok,
            "coverage_complete": coverage_complete,
            "all_required_applicable_evaluations_resolved": all_req_resolved,
            "per_candidate_mathematical_outcomes": per_cand_outcomes,
            "refuted_holdout_candidates": refuted_cands,
            "survived_holdout_candidates": survived_cands,
            "interval_split_audits": interval_audits,
            "integrity_conflicts": conflicts,
            "coverage_gaps": coverage_gaps,
            "prior_exposure_audit_disclosure": {
                "strictly_zero_prior_occurrences_count": 9,
                "single_observable_prior_occurrence_points": {
                    "TC063-HO-UNSEEN-96": (
                        "Y = 96 appeared in TC-059 grid_Y for E(96) only "
                        "(data/tc_dyadic_power_lift_primitive_correlation.json); 0 prior evaluations "
                        "for D_tilde, J, F, Sigma_off, S_same, or S_different and 0 calibration usage."
                    )
                },
            },
            "resource_compliance_summary": res_summary,
            "all_section_5_checks_pass": bool(sec5_pass),
        }
    )

    top_fields = {
        "execution_and_certification_status": exec_status,
        "holdout_hypothesis_outcome": holdout_outcome,
        "primary_log_saving_probe_outcome": primary_p0_outcome,
        "resource_compliance_status": res_status,
        "completion_outcome_code": outcome_code,
        "research_outcome_class": (
            f"SAME_CHAIN_UNIFORM_BOUND_PROVED_DISTINCT_CHAIN_{holdout_outcome}_RESOURCE_{res_status}"
        ),
    }
    return sec5_out, top_fields


def verify_section_5_unseen_validation_and_interval_splits(
    protocol_obj: Dict[str, Any],
    prec_bits: int = 256,
    selberg_table: Optional[Dict[str, Any]] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Execute all `10` frozen unseen `TC-063` validation points and both continuous interval
    case splits (`[81 - 2^-12, 81 + 2^-12]` and `[1096.50, 1096.66]`).
    """
    tbl = (
        compute_selberg_centered_remainder_table_fast_arb(18000, prec_bits=prec_bits + 32)
        if selberg_table is None or len(selberg_table["R"]) <= 17300
        else selberg_table
    )
    pts = protocol_obj["unseen_validation_schedule"]["points"]
    pt_rows = [execute_tc063_holdout_point_with_escalation(pt, protocol_obj, tbl) for pt in pts]

    splits_out: Dict[str, Any] = {}
    for ik, (ylo, yhi) in PRESCRIBED_TC063_INTERVAL_SPLITS.items():
        splits_out[ik] = evaluate_tc063_interval_via_cutoff_case_split_arb(
            ik, ylo, yhi, tbl, prec_bits=prec_bits
        )

    sec5_base = {
        "epistemic_statuses": [
            "CONCRETE_ANALYTIC_IN_LEAN",
            "ANALYTIC_PROVED_OUTSIDE_LEAN",
            "CERTIFIED_FINITE_OBSERVATION",
            "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        ],
        "section_epistemic_scope_note": (
            "Mixed formal/analytic/certified/open section: TC063-SAME-LOCAL-HILBERT is "
            "CONCRETE_ANALYTIC_IN_LEAN (Lean Theorem 3); exact cutoff-partition and 3-zone "
            "quadrature remainder bounds are ANALYTIC_PROVED_OUTSIDE_LEAN; 256-bit Arb point and "
            "interval evaluations on the 10 unseen TC-063 scales and 2 continuous straddling "
            "intervals are CERTIFIED_FINITE_OBSERVATION; universal S_different probes "
            "(TC063-P0-DIFF, TC063-P-HALF-DIFF, TC063-P-NEG-DIFF) remain "
            "OPEN_CONJECTURE_OR_FAILED_CANDIDATE (finite survival never proves universal bounds)."
        ),
        "component_epistemic_map": {
            "same_chain_local_hilbert_theorem_bound": "CONCRETE_ANALYTIC_IN_LEAN",
            "exact_interval_cutoff_partition_and_quadrature_bounds": "ANALYTIC_PROVED_OUTSIDE_LEAN",
            "ten_point_unseen_holdout_and_two_interval_enclosures": "CERTIFIED_FINITE_OBSERVATION",
            "universal_distinct_odd_chain_probes": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        },
        "holdout_point_evaluations": pt_rows,
        "continuous_interval_case_splits": splits_out,
    }
    return aggregate_tc063_section5_and_derive_outcomes(sec5_base, protocol_obj)


# ---------------------------------------------------------------------------
# 7. Section 6: Live Lean 4 Audit, Provenance Comparison, & Review Verifier
# ---------------------------------------------------------------------------


def extract_lean_declaration_spans_tc063(
    lean_path: Path = TC_063_LEAN_MODULE_PATH,
) -> Dict[str, Any]:
    """Extract live `def`, `theorem`, and `private theorem` line spans from
    `formal/RiemannScope/DyadicChainCorrelationRegularity.lean` and audit `0` `sorry`/`admit`/
    custom `axiom`/circle-half/`K_*` tokens.
    """
    if not lean_path.exists():
        return {
            "lean_file": "formal/RiemannScope/DyadicChainCorrelationRegularity.lean",
            "exists": False,
            "verified": False,
        }
    lines = lean_path.read_text(encoding="utf-8").splitlines()
    decl_re = re.compile(
        r"^\s*(?:noncomputable\s+)?(private\s+theorem|theorem|def|lemma)\s+([A-Za-z0-9_']+)"
    )
    decls: List[Dict[str, Any]] = []
    for idx, line in enumerate(lines, start=1):
        m = decl_re.match(line)
        if m:
            decls.append({"kind": m.group(1), "name": m.group(2), "start_line": idx})
    for i, d in enumerate(decls):
        end_l = (decls[i + 1]["start_line"] - 1) if (i + 1 < len(decls)) else len(lines)
        while end_l > d["start_line"] and (
            lines[end_l - 1].strip() == "" or lines[end_l - 1].strip().startswith("/--")
            or lines[end_l - 1].strip().startswith("/-!")
        ):
            end_l -= 1
        d["end_line"] = end_l

    raw_txt = "\n".join(lines)
    # Strip comments before scanning for sorry/admit/axiom:
    no_block = re.sub(r"/-.*?-/", "", raw_txt, flags=re.DOTALL)
    code_only = "\n".join(l.split("--")[0] for l in no_block.splitlines())
    sorry_hits = re.findall(r"\bsorry\b", code_only)
    admit_hits = re.findall(r"\badmit\b", code_only)
    axiom_hits = re.findall(r"^\s*axiom\b", code_only, flags=re.MULTILINE)
    p_tok = "p" + "i"
    pi_hits = [tok for tok in ("\\" + p_tok, "\u03c0", "Real." + p_tok) if tok in raw_txt]
    k_hits = [
        tok
        for tok in re.findall(r"\bK_[A-Za-z0-9_]+", raw_txt)
        if tok != "K_reserved_for_real_algebraic_geometric_grades_A_R"
    ]

    pub_theorems = [d["name"] for d in decls if d["kind"] == "theorem"]
    defs = [d["name"] for d in decls if d["kind"] == "def"]
    priv_theorems = [d["name"] for d in decls if d["kind"] in ("private theorem", "lemma")]

    build_rep_ok = False
    formal_producing_commit: Optional[str] = None
    total_project_public_theorems: Optional[int] = None
    if FORMAL_BUILD_REPORT_PATH.exists():
        brep = json.loads(FORMAL_BUILD_REPORT_PATH.read_text(encoding="utf-8"))
        live_mod_sha = hashlib.sha256(lean_path.read_bytes()).hexdigest()
        rec_mod_sha = brep.get("formal_source_hashes", {}).get(
            "formal/RiemannScope/DyadicChainCorrelationRegularity.lean"
        )
        build_rep_ok = bool(
            brep.get("status") == "passed"
            and brep.get("exit_code") == 0
            and rec_mod_sha == live_mod_sha
        )
        formal_producing_commit = brep.get("producing_git_commit")
        total_project_public_theorems = brep.get("total_theorems")

    expected_present = all(t in pub_theorems for t in EXPECTED_TC063_THEOREMS)
    return {
        "lean_file": "formal/RiemannScope/DyadicChainCorrelationRegularity.lean",
        "exists": True,
        "line_count": len(lines),
        "total_declarations": len(decls),
        "def_count": len(defs),
        "public_theorem_count": len(pub_theorems),
        "private_theorem_count": len(priv_theorems),
        "public_theorems": pub_theorems,
        "expected_theorems_all_present": expected_present,
        "declarations": decls,
        "sorry_count": len(sorry_hits),
        "admit_count": len(admit_hits),
        "custom_axiom_count": len(axiom_hits),
        "forbidden_pi_tokens": pi_hits,
        "forbidden_K_underscore_tokens": k_hits,
        "formal_build_report_pass": build_rep_ok,
        "formal_producing_git_commit": formal_producing_commit,
        "total_project_public_theorems": total_project_public_theorems,
        "verified": bool(
            expected_present
            and build_rep_ok
            and len(sorry_hits) == 0
            and len(admit_hits) == 0
            and len(axiom_hits) == 0
            and len(pi_hits) == 0
            and len(k_hits) == 0
        ),
    }


def verify_section_6_lean_audit_and_gate_accounting() -> Dict[str, Any]:
    lean_audit = extract_lean_declaration_spans_tc063()
    root_lean_txt = (REPO_ROOT / "formal" / "RiemannScope.lean").read_text(encoding="utf-8")
    imported_in_root = "import RiemannScope.DyadicChainCorrelationRegularity" in root_lean_txt
    return {
        "epistemic_statuses": [
            "CONCRETE_ANALYTIC_IN_LEAN",
            "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        ],
        "section_epistemic_scope_note": (
            "Formal verification and gate accounting section: all 5 public Lean 4 theorems in "
            "DyadicChainCorrelationRegularity.lean are CONCRETE_ANALYTIC_IN_LEAN (0 sorry, 0 admit, "
            "0 custom axioms, 0 circle-half or K_* tokens); SUBGATE-TC-043A and "
            "TC063-OBL-DISTINCT-ODD-CHAIN-CORRELATION remain OPEN_CONJECTURE_OR_FAILED_CANDIDATE "
            "(rh_proved = False)."
        ),
        "component_epistemic_map": {
            "dyadic_chain_correlation_regularity_lean_module": "CONCRETE_ANALYTIC_IN_LEAN",
            "subgate_tc_043a_and_distinct_odd_chain_obligation": "OPEN_CONJECTURE_OR_FAILED_CANDIDATE",
        },
        "lean_theorems": list(EXPECTED_TC063_THEOREMS),
        "lean_module_audit": lean_audit,
        "imported_in_root_RiemannScope_lean": imported_in_root,
        "gate_accounting": {
            "epic_id": EPIC_TC_042_ID,
            "parent_subgate": PARENT_SUBGATE_ID,
            "parent_subgate_status": "OPEN",
            "rh_proved": False,
            "global_energy_improvement_claimed": False,
            "closed_in_tc063": [
                "Exact odd-part decomposition Sigma_off(Y; 2) = S_same(Y) + S_different(Y) on complete Hcal_Y",
                "Uniform same-chain bound |S_same(Y)| <= (L(T)-1)*(2*C_psi + 8*C_g) <= C_same*(1 + log Y) for all real Y >= 2",
                "Two-way MixedCovarianceClosureHypothesis transfer Sigma_off(.; 2) <-> S_different(.)",
                "Actual Mathlib riemannZeta Dirichlet product, trivial-zero double vanishing, pole contradiction, and reflection",
                "Exact odd-gcd primitive regrouping, coprime feature decoupling, odd square-projection, and greedy +-1 sign-extension theorem",
            ],
            "refuted_subcandidates_in_tc063": [
                "TC063-CAND-A1-PRIM-NONPOS (Pi_16^diff(5) > 0, Pi_64^diff(7) > 0)",
                "TC063-CAND-B1-SQPROJ-DIAG-DOM (negative off-diagonal d_1 != d_2 dilation cross-terms)",
                "TC063-CAND-C1-ARB-SIGN (greedy +-1 witness at Y = 64 and asymptotic Omega(Y) lower bound)",
                "TC063-P-NEG-DIFF (zero-slack S_different(Y) <= 0 refuted on unseen Y >= 960 and [1096.50, 1096.66], while TC063-P0-DIFF survived 10/10 unseen points and both continuous intervals)",
                "Matched negative controls unsigned_1, a2, a_3_5_7 and labeled hybrid_a2_liouville on S_different for Y >= 64",
            ],
            "earliest_remaining_mathematical_premise": "TC063-OBL-DISTINCT-ODD-CHAIN-CORRELATION",
            "earliest_remaining_formalization_only_items": [
                "TC063-PREM-04 (global linear energy E(Z) <= M_lin * Z)",
                "TC063-PREM-05 (prime-power Dirichlet weight zeta''(1+delta) bound)",
                "TC063-PREM-06 (shifted diagonal cutoff comparison)",
                "TC063-PREM-07 (assembled ||A_Y||_Y^2 horizon contraction)",
                "TC063-PREM-08 (Q_{lambda,infty} tail cap B_tau)",
                "TC063-PREM-09 (Mellin holomorphy continuation M_Q(w) to 0 < Re(w) < 5/2)",
            ],
        },
        "all_section_6_checks_pass": bool(
            lean_audit["verified"]
            and lean_audit["formal_build_report_pass"]
            and imported_in_root
        ),
    }


_STATUS_LIKE_KEY_SUFFIXES: Tuple[str, ...] = (
    "_status",
    "_outcome",
    "_code",
    "_class",
    "_pass",
    "_complete",
    "_ok",
    "_resolved",
    "_proved",
    "_claimed",
    "_count",
)

_EXPECTED_STATUS_KEY_TYPES_TC063: Dict[str, str] = {
    "top.execution_and_certification_status": "str",
    "top.holdout_hypothesis_outcome": "str",
    "top.primary_log_saving_probe_outcome": "str",
    "top.resource_compliance_status": "str",
    "top.completion_outcome_code": "str",
    "top.research_outcome_class": "str",
    "top.all_mathematical_and_numerical_checks_pass": "bool",
    "top.parent_subgate_status": "str",
    "top.rh_proved": "bool",
    "top.global_energy_improvement_claimed": "bool",
    "sec5.registered_unseen_point_count": "int",
    "sec5.evaluated_unseen_point_count": "int",
    "sec5.coverage_complete": "bool",
    "sec5.certification_integrity_ok": "bool",
    "sec5.all_required_applicable_evaluations_resolved": "bool",
    "sec5.all_section_5_checks_pass": "bool",
}


def _check_strict_scalar_type(val: Any, kind: str) -> bool:
    if kind == "bool":
        return isinstance(val, bool)
    if kind == "int":
        return isinstance(val, int) and not isinstance(val, bool)
    if kind == "str":
        return isinstance(val, str) and len(val.strip()) > 0
    return False


def _collect_status_map_tc063(art: Dict[str, Any]) -> Dict[str, Any]:
    s5 = art.get("section_5_unseen_validation_and_interval_splits", {})
    if not isinstance(s5, dict):
        s5 = {}
    out: Dict[str, Any] = {}
    for k, v in art.items():
        if isinstance(k, str) and any(k.endswith(suf) for suf in _STATUS_LIKE_KEY_SUFFIXES):
            if not isinstance(v, (dict, list)):
                out[f"top.{k}"] = v
    for k, v in s5.items():
        if isinstance(k, str) and any(k.endswith(suf) for suf in _STATUS_LIKE_KEY_SUFFIXES):
            if not isinstance(v, (dict, list)):
                out[f"sec5.{k}"] = v
    for rk in REQUIRED_CURRENT_TC063_STATUS_KEYS:
        sc, fk = rk.split(".", 1)
        src = art if sc == "top" else s5
        if fk in src:
            out[rk] = src[fk]
    return out


def _collect_verdict_map_tc063(art: Dict[str, Any]) -> Tuple[Dict[str, str], List[str]]:
    """Collect all mathematical verdict keys across all 5 scopes (`sec5` global outcomes, `sec5`
    point verdicts, `sec5` interval outcomes & branch/union classifications, `sec3` matched-control
    verdicts, and `sec4` sub-candidate outcomes), flagging missing, malformed, or conflict sentinels.
    """
    verdicts: Dict[str, str] = {}
    issues: List[str] = []

    s3 = art.get("section_3_same_chain_bound_and_matched_controls")
    s4 = art.get("section_4_distinct_chain_attempts_and_obstructions")
    s5 = art.get("section_5_unseen_validation_and_interval_splits")
    if not isinstance(s3, dict) or not isinstance(s4, dict) or not isinstance(s5, dict):
        return {}, ["missing_section_dict"]

    # 1. Section 5 per-candidate outcomes:
    pco = s5.get("per_candidate_mathematical_outcomes")
    if not isinstance(pco, dict) or len(pco) == 0:
        issues.append("sec5.per_candidate_mathematical_outcomes")
    else:
        for cid, v in pco.items():
            if not isinstance(v, str) or v == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME:
                issues.append(f"sec5.per_candidate_mathematical_outcomes.{cid}")
            else:
                verdicts[f"sec5.outcome.{cid}"] = v

    # 2. Section 5 holdout point verdicts:
    pts = s5.get("holdout_point_evaluations")
    if not isinstance(pts, list) or len(pts) == 0:
        issues.append("sec5.holdout_point_evaluations")
    else:
        seen_p = set()
        for row in pts:
            if not isinstance(row, dict) or not isinstance(row.get("point_id"), str):
                issues.append("sec5.malformed_point_row")
                continue
            pid = row["point_id"]
            if pid in seen_p:
                issues.append(f"sec5.duplicate_point.{pid}")
                continue
            seen_p.add(pid)
            for grp_k in ("probe_evaluations", "kl1_sub_budget_evaluations"):
                grp = row.get(grp_k)
                if not isinstance(grp, dict):
                    issues.append(f"sec5.point.{pid}.{grp_k}")
                    continue
                for cid, rec in grp.items():
                    v = rec.get("verdict") if isinstance(rec, dict) else None
                    if not isinstance(v, str) or v == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT:
                        issues.append(f"sec5.point.{pid}.{cid}")
                    else:
                        verdicts[f"sec5.point.{pid}.{cid}"] = v

    # 3. Section 5 interval outcomes + branch/union classifications:
    ia_map = s5.get("interval_split_audits")
    sp_map = s5.get("continuous_interval_case_splits")
    if not isinstance(ia_map, dict) or not isinstance(sp_map, dict):
        issues.append("sec5.interval_maps")
    else:
        for ik in PRESCRIBED_TC063_INTERVAL_SPLITS:
            ia = ia_map.get(ik)
            sp = sp_map.get(ik)
            if not isinstance(ia, dict) or not isinstance(sp, dict):
                issues.append(f"sec5.interval.{ik}")
                continue
            dpo = ia.get("derived_probe_outcomes")
            if not isinstance(dpo, dict):
                issues.append(f"sec5.interval.{ik}.derived_probe_outcomes")
            else:
                for cid, v in dpo.items():
                    if not isinstance(v, str) or v == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME:
                        issues.append(f"sec5.interval.{ik}.outcome.{cid}")
                    else:
                        verdicts[f"sec5.interval.{ik}.outcome.{cid}"] = v
            for u_cls_k in (
                "TC063_P0_DIFF_interval_classification",
                "TC063_P_NEG_DIFF_interval_classification",
                "TC063_SAME_LOC_interval_classification",
            ):
                uc = sp.get(u_cls_k)
                uv = uc.get("verdict") if isinstance(uc, dict) else None
                if not isinstance(uv, str) or uv == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT:
                    issues.append(f"sec5.interval.{ik}.{u_cls_k}")
                else:
                    verdicts[f"sec5.interval.{ik}.{u_cls_k}"] = uv
            brs = sp.get("branches")
            if not isinstance(brs, list) or len(brs) == 0:
                issues.append(f"sec5.interval.{ik}.branches")
            else:
                seen_tr = set()
                for br in brs:
                    if not isinstance(br, dict):
                        issues.append(f"sec5.interval.{ik}.malformed_branch")
                        continue
                    tr = (br.get("T_fixed"), br.get("D0_raw_fixed"), br.get("D0_eff_fixed"))
                    if tr in seen_tr:
                        issues.append(f"sec5.interval.{ik}.duplicate_branch.{tr}")
                        continue
                    seen_tr.add(tr)
                    for b_cls_k in (
                        "TC063_P0_DIFF_branch_classification",
                        "TC063_P_NEG_DIFF_branch_classification",
                        "TC063_SAME_LOC_branch_classification",
                    ):
                        bc = br.get(b_cls_k)
                        bv = bc.get("verdict") if isinstance(bc, dict) else None
                        if not isinstance(bv, str) or bv == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT:
                            issues.append(f"sec5.interval.{ik}.branch.{tr}.{b_cls_k}")
                        else:
                            verdicts[f"sec5.interval.{ik}.branch.{tr}.{b_cls_k}"] = bv

    # 4. Section 3 matched-control and hybrid verdicts:
    c_rows = s3.get("matched_control_and_hybrid_chain_rows")
    if not isinstance(c_rows, list) or len(c_rows) == 0:
        issues.append("sec3.matched_control_and_hybrid_chain_rows")
    else:
        for cr in c_rows:
            if not isinstance(cr, dict):
                issues.append("sec3.malformed_control_row")
                continue
            yk, mk, cv = cr.get("Y"), cr.get("mode"), cr.get("TC063_P0_DIFF_verdict")
            if not isinstance(cv, str) or cv == CERTIFICATION_INTEGRITY_CONFLICT_VERDICT:
                issues.append(f"sec3.control.{yk}.{mk}")
            else:
                verdicts[f"sec3.control.{yk}.{mk}"] = cv

    # 5. Section 4 sub-candidate outcomes:
    s4_paths = (
        (
            "TC063-CAND-A1-PRIM-NONPOS",
            s4.get("attempt_A_common_factor_primitive_regrouping", {}).get("candidate_A1_prim_nonpos"),
        ),
        (
            "TC063-CAND-B1-SQPROJ-DIAG-DOM",
            s4.get("attempt_B_square_projection_and_selberg_compatibility", {}).get(
                "candidate_B1_sqproj_diag_dom"
            ),
        ),
        (
            "TC063-CAND-C1-ARB-SIGN",
            s4.get("attempt_C_arithmetic_restricted_vs_arbitrary_sign_comparison", {}).get(
                "candidate_C1_arbitrary_sign"
            ),
        ),
    )
    for cid4, rec4 in s4_paths:
        ov4 = rec4.get("outcome") if isinstance(rec4, dict) else None
        if not isinstance(ov4, str) or ov4 == CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME:
            issues.append(f"sec4.{cid4}")
        else:
            verdicts[f"sec4.{cid4}"] = ov4

    return verdicts, issues


def compare_tc063_artifacts_by_stable_key(
    current_art: Optional[Dict[str, Any]],
    prior_art: Optional[Dict[str, Any]],
    *,
    comparison_id: str = "TC063_SELF_CONSISTENCY_V1",
    retired_optional_fields: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """Compare two `TC-063` artifacts across all 5 mathematical verdict scopes AND the full union
    of status keys, enforcing strict runtime scalar types and detecting deleted/renamed/conflicted
    keys (`INCOMPLETE_COMPARISON` with `None` — never `False`).
    """
    if (
        current_art is None
        or not isinstance(current_art, dict)
        or prior_art is None
        or not isinstance(prior_art, dict)
    ):
        return {
            "comparison_id": comparison_id,
            "comparison_status": "NOT_COMPARED",
            "any_mathematical_verdict_changed": None,
            "any_status_classification_changed": None,
            "missing_status_keys": [],
            "removed_status_or_schema_fields": [],
        }

    retired_set = set(retired_optional_fields or ())
    cur_stat = _collect_status_map_tc063(current_art)
    pri_stat = _collect_status_map_tc063(prior_art)

    missing_or_bad_status: List[str] = []
    for rk in REQUIRED_CURRENT_TC063_STATUS_KEYS:
        exp_t = _EXPECTED_STATUS_KEY_TYPES_TC063[rk]
        if rk not in cur_stat or not _check_strict_scalar_type(cur_stat[rk], exp_t):
            missing_or_bad_status.append(rk)
        elif rk not in pri_stat or not _check_strict_scalar_type(pri_stat[rk], exp_t):
            missing_or_bad_status.append(rk)

    removed_extra = sorted(
        k
        for k in (set(pri_stat.keys()) - set(cur_stat.keys()))
        if k not in retired_set
    )
    added_extra = sorted(set(cur_stat.keys()) - set(pri_stat.keys()))
    for k_common in sorted(set(cur_stat.keys()) & set(pri_stat.keys())):
        vc, vp = cur_stat[k_common], pri_stat[k_common]
        if vc is None or vp is None or (type(vc) is not type(vp)):
            if k_common not in missing_or_bad_status:
                missing_or_bad_status.append(k_common)

    if missing_or_bad_status or removed_extra or added_extra:
        return {
            "comparison_id": comparison_id,
            "comparison_status": "INCOMPLETE_COMPARISON",
            "any_mathematical_verdict_changed": None,
            "any_status_classification_changed": None,
            "missing_status_keys": sorted(set(missing_or_bad_status + removed_extra + added_extra)),
            "removed_status_or_schema_fields": removed_extra,
        }

    cur_verdicts, cur_v_issues = _collect_verdict_map_tc063(current_art)
    pri_verdicts, pri_v_issues = _collect_verdict_map_tc063(prior_art)
    if cur_v_issues or pri_v_issues or set(cur_verdicts.keys()) != set(pri_verdicts.keys()):
        return {
            "comparison_id": comparison_id,
            "comparison_status": "INCOMPLETE_COMPARISON",
            "any_mathematical_verdict_changed": None,
            "any_status_classification_changed": None,
            "missing_status_keys": sorted(
                set(
                    cur_v_issues
                    + pri_v_issues
                    + list(set(cur_verdicts.keys()) ^ set(pri_verdicts.keys()))
                )
            ),
            "removed_status_or_schema_fields": [],
        }

    changed_math = [k for k in sorted(cur_verdicts) if cur_verdicts[k] != pri_verdicts[k]]
    changed_stat = [
        k for k in sorted(cur_stat) if cur_stat[k] != pri_stat[k]
    ]
    return {
        "comparison_id": comparison_id,
        "comparison_status": "COMPLETE_COMPARED",
        "comparable_verdict_key_count": len(cur_verdicts),
        "any_mathematical_verdict_changed": len(changed_math) > 0,
        "changed_mathematical_verdict_keys": changed_math,
        "any_status_classification_changed": len(changed_stat) > 0,
        "changed_status_keys": changed_stat,
        "missing_status_keys": [],
        "removed_status_or_schema_fields": [],
    }


def verify_tc063_review_enclosures_and_lean_anchors(
    artifact_dict: Dict[str, Any],
    review_path: Path = TC_063_REVIEW_DOC_PATH,
) -> Dict[str, Any]:
    """Verify every `<!-- tc-enclosure: ... -->` tag in `TC_063_...md` against `artifact_dict`,
    every `DyadicChainCorrelationRegularity.lean#L<a>-L<b>` line anchor against live Lean
    declaration spans (rejecting unknown declaration names), and all 10 holdout cutoff triples in
    the Section 7.2 review table.
    """
    if not review_path.exists():
        return {"review_exists": False, "verified": False}
    txt = review_path.read_text(encoding="utf-8")
    p_tok = "p" + "i"
    pi_hits = [tok for tok in ("\\" + p_tok, "\u03c0", "Real." + p_tok) if tok in txt]
    k_hits = [
        tok
        for tok in re.findall(r"\bK_[A-Za-z0-9_]+", txt)
        if tok != "K_reserved_for_real_algebraic_geometric_grades_A_R"
    ]

    enclosure_failures: List[str] = []
    enclosure_count = 0
    for m in _TC_ENCLOSURE_TAG_RE.finditer(txt):
        enclosure_count += 1
        obs_name, params_str, json_path = m.group(1), m.group(2), m.group(3)
        prefix = txt[max(0, m.start() - 260) : m.start()]
        b_matches = list(_ARB_BACKTICK_INTERVAL_RE.finditer(prefix))
        if not b_matches:
            enclosure_failures.append(f"{obs_name}: missing preceding Arb backtick interval")
            continue
        disp_str = b_matches[-1].group(0).strip("`")
        try:
            target, _ = _resolve_report_path_with_param_check(
                artifact_dict, json_path, params_str, obs_name
            )
            parsed_t = _parse_serialized_arb_enclosure_tc062(target)
            if parsed_t is None:
                enclosure_failures.append(f"{obs_name}: target serialized Arb ball malformed")
                continue
            d_lo, d_hi, _ = _parse_arb_ball_str_to_fractions(disp_str)
            if not (d_lo <= parsed_t["c_lo"] and parsed_t["c_hi"] <= d_hi):
                enclosure_failures.append(
                    f"{obs_name}: displayed {disp_str} does not enclose {target['arb_ball_str']}"
                )
        except Exception as exc:  # noqa: BLE001
            enclosure_failures.append(f"{obs_name} ({json_path}): {exc}")

    lean_spans = extract_lean_declaration_spans_tc063()
    span_map = {
        d["name"]: (d["start_line"], d["end_line"]) for d in lean_spans.get("declarations", [])
    }
    anchor_re = re.compile(
        r"\[`?([A-Za-z0-9_']+)`?\]\([^)]*DyadicChainCorrelationRegularity\.lean#L(\d+)-L(\d+)\)"
    )
    anchor_failures: List[str] = []
    anchor_count = 0
    for am in anchor_re.finditer(txt):
        anchor_count += 1
        d_name, l_s, l_e = am.group(1), int(am.group(2)), int(am.group(3))
        if d_name not in span_map:
            anchor_failures.append(
                f"{d_name}: declaration not found in DyadicChainCorrelationRegularity.lean"
            )
        else:
            exp_s, exp_e = span_map[d_name]
            if (l_s, l_e) != (exp_s, exp_e):
                anchor_failures.append(
                    f"{d_name}: review #L{l_s}-L{l_e} != live #L{exp_s}-L{exp_e}"
                )

    # Cross-check all 10 holdout cutoff triples `(T, D_eff, L)` in the review table:
    pt_cut_map = {
        r["point_id"]: (
            r["cutoffs"]["T_Y"],
            r["cutoffs"]["D0_eff"],
            r["cutoffs"]["max_chain_length_L_T"],
        )
        for r in artifact_dict.get("section_5_unseen_validation_and_interval_splits", {}).get(
            "holdout_point_evaluations", []
        )
        if isinstance(r, dict) and "point_id" in r and "cutoffs" in r
    }
    row_re = re.compile(
        r"\|\s*`(TC063-HO-[A-Z0-9-]+)`\s*\|[^|]+\|\s*`?\$\((\d+),\s*(\d+),\s*(\d+)\)\$`?\s*\|"
    )
    cutoff_failures: List[str] = []
    cutoff_checked = 0
    for rm in row_re.finditer(txt):
        cutoff_checked += 1
        pid_r = rm.group(1)
        got_tr = (int(rm.group(2)), int(rm.group(3)), int(rm.group(4)))
        if pid_r not in pt_cut_map:
            cutoff_failures.append(f"{pid_r}: unknown holdout point_id in review table")
        elif got_tr != pt_cut_map[pid_r]:
            cutoff_failures.append(
                f"{pid_r}: review table {got_tr} != certified {pt_cut_map[pid_r]}"
            )

    return {
        "review_exists": True,
        "enclosure_tags_checked": enclosure_count,
        "enclosure_failures": enclosure_failures,
        "lean_anchors_checked": anchor_count,
        "lean_anchor_failures": anchor_failures,
        "holdout_cutoffs_checked": cutoff_checked,
        "holdout_cutoff_failures": cutoff_failures,
        "forbidden_pi_tokens": pi_hits,
        "forbidden_K_underscore_tokens": k_hits,
        "verified": bool(
            enclosure_count >= 6
            and len(enclosure_failures) == 0
            and anchor_count >= 5
            and len(anchor_failures) == 0
            and cutoff_checked == 10
            and len(cutoff_failures) == 0
            and len(pi_hits) == 0
            and len(k_hits) == 0
        ),
    }


# ---------------------------------------------------------------------------
# 8. Full Artifact Generator & Metadata Reprocessor
# ---------------------------------------------------------------------------


def _get_git_head_commit() -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


def generate_task_tc063_artifact(
    output_path: Path = DYADIC_CHAIN_ARTIFACT_PATH,
    *,
    write_output: bool = True,
) -> Dict[str, Any]:
    """Generate the complete 256-bit Arb `TASK-TC-063` certificate artifact
    `data/tc_dyadic_chain_correlation_regularity.json`.
    """
    proto_chk = verify_frozen_tc063_protocol_immutability()
    if not proto_chk["verified"]:
        raise CertificationIntegrityError("Frozen TC-063 protocol immutability check failed!")
    proto_obj = proto_chk["protocol_object"]

    tbl = compute_selberg_centered_remainder_table_fast_arb(18000, prec_bits=288)
    sec1 = verify_section_1_protocols_endpoint_and_premise_chain(prec_bits=256)
    sec2 = verify_section_2_odd_part_decomposition_and_cross_checks(
        prec_bits=256, selberg_table=tbl
    )
    sec3 = verify_section_3_same_chain_bound_and_matched_controls(
        prec_bits=256, selberg_table=tbl
    )
    sec4 = verify_section_4_distinct_chain_attempts_and_obstructions(
        prec_bits=256, selberg_table=tbl
    )
    sec5, top_fields = verify_section_5_unseen_validation_and_interval_splits(
        proto_obj, prec_bits=256, selberg_table=tbl
    )
    sec6 = verify_section_6_lean_audit_and_gate_accounting()

    head_commit = _get_git_head_commit()
    gen_utc = datetime.now(timezone.utc).isoformat()
    formal_commit = (
        sec6["lean_module_audit"].get("formal_producing_git_commit")
        or PRESERVED_TC062R_PRODUCING_COMMIT
    )

    art: Dict[str, Any] = {
        "schema_version": "1.0.0",
        "task_id": TASK_TC_063_ID,
        "epic_id": EPIC_TC_042_ID,
        "parent_subgate": PARENT_SUBGATE_ID,
        "parent_subgate_status": "OPEN",
        "rh_proved": False,
        "global_energy_improvement_claimed": False,
        "circle_constant_convention": "tau_exclusively",
        "grade_variable_convention": "K_reserved_for_real_algebraic_geometric_grades_A_R",
        "sampled_zeta_zeros_used": 0,
        "generated_at_utc": gen_utc,
        **top_fields,
        "provenance": {
            "accepted_tc062r4_delivered_tip": ACCEPTED_TC062R4_DELIVERED_TIP,
            "accepted_tc062r4_validation_commit": ACCEPTED_TC062R4_VALIDATION_COMMIT,
            "preserved_tc062r_producing_commit": PRESERVED_TC062R_PRODUCING_COMMIT,
            "merged_main_baseline": MERGED_MAIN_BASELINE_TC061,
            "frozen_tc061_protocol_registration_commit": TC061_FROZEN_PROTOCOL_REGISTRATION_COMMIT,
            "frozen_tc061_protocol_sha256": TC061_FROZEN_PROTOCOL_SHA256,
            "frozen_tc062_protocol_registration_commit": FROZEN_TC062_PROTOCOL_REGISTRATION_COMMIT,
            "frozen_tc062_protocol_sha256": FROZEN_TC062_PROTOCOL_SHA256,
            "frozen_tc063_protocol_id": FROZEN_TC063_PROTOCOL_ID,
            "frozen_tc063_protocol_registration_commit": FROZEN_TC063_PROTOCOL_REGISTRATION_COMMIT,
            "frozen_tc063_protocol_sha256": FROZEN_TC063_PROTOCOL_SHA256,
            "numerical_producing_git_commit": head_commit,
            "validation_git_commit": head_commit,
            "formal_producing_git_commit": formal_commit,
        },
        "section_1_protocols_endpoint_and_premise_chain": sec1,
        "section_2_odd_part_decomposition_and_cross_checks": sec2,
        "section_3_same_chain_bound_and_matched_controls": sec3,
        "section_4_distinct_chain_attempts_and_obstructions": sec4,
        "section_5_unseen_validation_and_interval_splits": sec5,
        "section_6_lean_audit_and_gate_accounting": sec6,
    }

    arb_chk = verify_all_serialized_arb_in_tree(art)
    art["serialized_arb_self_check"] = arb_chk
    art["all_mathematical_and_numerical_checks_pass"] = bool(
        sec1["all_section_1_checks_pass"]
        and sec2["all_section_2_checks_pass"]
        and sec3["all_section_3_checks_pass"]
        and sec4["all_section_4_checks_pass"]
        and sec5["all_section_5_checks_pass"]
        and sec6["all_section_6_checks_pass"]
        and arb_chk["all_enclose_original_256bit_arb_ball"]
    )

    clean_art = strip_enclosure_arb_for_json(art)
    clean_art["provenance"]["self_verdict_comparison"] = compare_tc063_artifacts_by_stable_key(
        clean_art, clean_art
    )

    if write_output:
        txt_out = json.dumps(clean_art, indent=2, ensure_ascii=True) + "\n"
        p_tok = "p" + "i"
        for bad_tok in ("\\" + p_tok, "\u03c0", "Real." + p_tok, "const_" + p_tok, "math." + p_tok):
            if bad_tok in txt_out:
                raise RuntimeError(f"Forbidden token {bad_tok!r} in TC-063 artifact!")
        output_path.write_bytes(txt_out.encode("utf-8"))
    return clean_art


EXPECTED_TC063_FIXED_SECTION_BALL_COUNTS: Dict[str, int] = {
    "section_1_protocols_endpoint_and_premise_chain": 21,
    "section_2_odd_part_decomposition_and_cross_checks": 66,
    "section_3_same_chain_bound_and_matched_controls": 260,
    "section_4_distinct_chain_attempts_and_obstructions": 79,
}


def _expected_tc063_section_5_ball_count(sec5_obj: Any) -> Optional[int]:
    """Compute exact expected serialized Arb ball count for all present Section 5 rows,
    candidate evaluation records, and continuous interval splits/branches (`R2-2`).
    """
    if not isinstance(sec5_obj, dict):
        return None
    exp_cnt = 0
    rows = sec5_obj.get("holdout_point_evaluations")
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                return None
            # 1 `Y_enclosure` + 11 observable balls = 12 mandatory balls per present point row:
            exp_cnt += 12
            pe = row.get("probe_evaluations")
            ke = row.get("kl1_sub_budget_evaluations")
            if not isinstance(pe, dict) or not isinstance(ke, dict):
                return None
            exp_cnt += len(pe) + len(ke)
    splits = sec5_obj.get("continuous_interval_case_splits")
    if isinstance(splits, dict):
        for sp_obj in splits.values():
            if not isinstance(sp_obj, dict):
                return None
            # 9 union balls per present split + 10 balls (`Y_sub_ball` + 9 observables) per branch:
            exp_cnt += 9
            brs = sp_obj.get("branches")
            if isinstance(brs, list):
                for br in brs:
                    if not isinstance(br, dict):
                        return None
                    exp_cnt += 10
    return exp_cnt


def _audit_all_serialized_arb_balls_in_artifact(
    tree: Dict[str, Any],
    existing_self_chk: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Walk the entire serialized artifact and validate EVERY Arb ball via the 3-representation
    exact `Fraction` validator `_parse_serialized_arb_enclosure_tc062`, plus enforce exact
    per-section ball counts so silent `{}`/`None`/scalar ball replacement fails closed (`R2-2`).
    """
    req_keys = {"mid_float", "rad_float_outward", "lower_dec", "upper_dec", "arb_ball_str"}
    checked_paths: List[str] = []
    valid_paths_by_root: Dict[str, int] = {}
    failed_paths: List[str] = []

    def _walk(node: Any, cur_path: str) -> None:
        if isinstance(node, dict):
            if any(k in node for k in req_keys):
                if not req_keys.issubset(node.keys()):
                    checked_paths.append(cur_path)
                    failed_paths.append(cur_path)
                    return
                checked_paths.append(cur_path)
                if _parse_serialized_arb_enclosure_tc062(node) is None:
                    failed_paths.append(cur_path)
                else:
                    root_sec = cur_path.split(".", 1)[0].split("[", 1)[0]
                    valid_paths_by_root[root_sec] = valid_paths_by_root.get(root_sec, 0) + 1
                return
            for k, v in node.items():
                if k in ("enclosure_arb", "serialized_arb_self_check"):
                    continue
                _walk(v, f"{cur_path}.{k}" if cur_path else str(k))
        elif isinstance(node, (list, tuple)):
            for idx, item in enumerate(node):
                _walk(item, f"{cur_path}[{idx}]")

    _walk(tree, "")
    for sec_k, exp_n in EXPECTED_TC063_FIXED_SECTION_BALL_COUNTS.items():
        got_n = valid_paths_by_root.get(sec_k, 0)
        if got_n != exp_n:
            failed_paths.append(f"{sec_k}:expected_{exp_n}_certified_balls_got_{got_n}")
    exp_s5 = _expected_tc063_section_5_ball_count(
        tree.get("section_5_unseen_validation_and_interval_splits") if isinstance(tree, dict) else None
    )
    got_s5 = valid_paths_by_root.get("section_5_unseen_validation_and_interval_splits", 0)
    if exp_s5 is None or got_s5 != exp_s5:
        failed_paths.append(
            f"section_5_unseen_validation_and_interval_splits:expected_{exp_s5}_certified_balls_got_{got_s5}"
        )

    prev_live_cnt = (
        int(existing_self_chk["compared_against_live_original_arb_count"])
        if isinstance(existing_self_chk, dict)
        and isinstance(existing_self_chk.get("compared_against_live_original_arb_count"), int)
        else 0
    )
    live_matches = bool(prev_live_cnt == len(checked_paths) and len(failed_paths) == 0)
    return {
        "total_certified_arb_balls_checked": len(checked_paths),
        "compared_against_live_original_arb_count": prev_live_cnt if live_matches else 0,
        "live_original_count_matches_enumerated_total": live_matches,
        "all_enclose_original_256bit_arb_ball": bool(
            len(checked_paths) > 0 and len(failed_paths) == 0
        ),
        "failed_paths": failed_paths,
        "checked_paths": checked_paths,
    }


def _audit_section_1_serialized_checks(sec1_raw: Dict[str, Any]) -> Dict[str, Any]:
    """Re-verify Section 1 protocol/historical SHA-256 invariants and serialized Arb checks."""
    s1 = json.loads(json.dumps(sec1_raw))
    chk_61 = verify_frozen_protocol_immutability()
    chk_62 = verify_frozen_tc062_protocol_immutability()
    chk_63 = verify_frozen_tc063_protocol_immutability()

    tc062_bytes = JOINT_PRIME_DILATION_ARTIFACT_PATH.read_bytes().replace(b"\r\n", b"\n")
    tc062_sha = hashlib.sha256(tc062_bytes).hexdigest()
    tc062_obj = json.loads(tc062_bytes.decode("utf-8"))
    tc062_balls = tc062_obj["serialized_arb_self_check"]["total_certified_arb_balls_checked"]
    tc062_ok = bool(
        tc062_sha == EXPECTED_TC062_ARTIFACT_SHA256
        and tc062_balls == 885
        and tc062_obj["provenance"]["numerical_producing_git_commit"]
        == PRESERVED_TC062R_PRODUCING_COMMIT
    )
    tc061_bytes = MIXED_ARITHMETIC_COVARIANCE_ARTIFACT_PATH.read_bytes().replace(b"\r\n", b"\n")
    tc061_sha = hashlib.sha256(tc061_bytes).hexdigest()
    tc061_obj = json.loads(tc061_bytes.decode("utf-8"))
    tc061_balls = tc061_obj["serialized_arb_self_check"]["total_certified_arb_balls_checked"]
    tc061_ok = bool(tc061_sha == EXPECTED_TC061_ARTIFACT_SHA256 and tc061_balls == 3208)

    s1["preserved_tc062_artifact_integrity"] = {
        "artifact_path": "data/tc_joint_prime_dilation_signed_remainder.json",
        "sha256_lf": tc062_sha,
        "total_certified_arb_balls": tc062_balls,
        "numerical_producing_git_commit": tc062_obj["provenance"][
            "numerical_producing_git_commit"
        ],
        "verified": tc062_ok,
    }
    s1["preserved_tc061_artifact_integrity"] = {
        "artifact_path": "data/tc_mixed_arithmetic_covariance.json",
        "sha256_lf": tc061_sha,
        "total_certified_arb_balls": tc061_balls,
        "verified": tc061_ok,
    }

    dir_rows = s1.get("dirichlet_ratio_nonvanishing_checks", [])
    dir_ok = len(dir_rows) >= 2
    for dr in dir_rows:
        p_z2 = _parse_serialized_arb_enclosure_tc062(dr.get("abs_zeta_2z")) if isinstance(dr, dict) else None
        p_res = _parse_serialized_arb_enclosure_tc062(dr.get("product_residual_abs")) if isinstance(dr, dict) else None
        rok = bool(
            p_z2 is not None
            and p_res is not None
            and p_z2["c_lo"] > Fraction(1, 10)
            and p_res["c_lo"] <= 0 <= p_res["c_hi"]
        )
        if isinstance(dr, dict):
            dr["zeta_2z_certified_nonzero"] = bool(p_z2 is not None and p_z2["c_lo"] > 0)
            dr["verified"] = rok
        dir_ok = dir_ok and rok

    triv_rows = s1.get("trivial_zero_double_vanishing_checks", [])
    triv_ok = len(triv_rows) >= 3
    for tr in triv_rows:
        v1 = _parse_serialized_arb_enclosure_tc062(tr.get("abs_zeta_z")) if isinstance(tr, dict) else None
        v2 = _parse_serialized_arb_enclosure_tc062(tr.get("abs_zeta_2z")) if isinstance(tr, dict) else None
        tok = bool(
            v1 is not None
            and v2 is not None
            and v1["c_hi"] < Fraction(1, 10 ** 70)
            and v2["c_hi"] < Fraction(1, 10 ** 70)
        )
        if isinstance(tr, dict):
            tr["both_numerator_and_denominator_vanish"] = tok
        triv_ok = triv_ok and tok

    refl_rows = s1.get("functional_equation_reflection_checks", [])
    refl_ok = len(refl_rows) >= 2
    for rr in refl_rows:
         d_xi = _parse_serialized_arb_enclosure_tc062(
             rr.get("completed_xi_reflection_abs_diff")
         ) if isinstance(rr, dict) else None
         rok = bool(d_xi is not None and d_xi["c_hi"] < Fraction(1, 10 ** 65))
         if isinstance(rr, dict):
             rr["verified"] = rok
         refl_ok = refl_ok and rok

    base_rows = s1.get("generic_window_base_hilbert_checks", [])
    base_ok = len(base_rows) == 3
    for br in base_rows:
        mb = _parse_serialized_arb_enclosure_tc062(
            br.get("abs_S_same_minus_hilbert_bound")
        ) if isinstance(br, dict) else None
        bok = bool(mb is not None and mb["c_hi"] < 0)
        if isinstance(br, dict):
            br["verified"] = bok
        base_ok = base_ok and bok

    s1["all_section_1_checks_pass"] = bool(
        chk_61["verified"]
        and chk_62["verified"]
        and chk_63["verified"]
        and tc062_ok
        and tc061_ok
        and dir_ok
        and triv_ok
        and refl_ok
        and base_ok
    )
    return s1


def _audit_section_4_serialized_checks(sec4_raw: Dict[str, Any]) -> Dict[str, Any]:
    """Re-verify ALL Section 4 witness balls (`CAND-A1`, `CAND-B1`, `CAND-C1`, `p = 2` jump
    witnesses, primitive regrouping residuals, and square-projection residuals) directly from
    serialized 256-bit Arb enclosures without modifying any numerical Arb ball.
    """
    s4 = json.loads(json.dumps(sec4_raw))
    att_a = s4.get("attempt_A_common_factor_primitive_regrouping", {})
    att_b = s4.get("attempt_B_square_projection_and_selberg_compatibility", {})
    att_c = s4.get("attempt_C_arithmetic_restricted_vs_arbitrary_sign_comparison", {})
    cand_a1 = att_a.get("candidate_A1_prim_nonpos", {})
    cand_b1 = att_b.get("candidate_B1_sqproj_diag_dom", {})
    cand_c1 = att_c.get("candidate_C1_arbitrary_sign", {})

    if isinstance(att_b, dict) and isinstance(att_b.get("first_uncontrolled_term_and_size"), dict):
        att_b["first_uncontrolled_term_and_size"]["term"] = (
            "Negative off-diagonal odd-divisor dilation cross-sum "
            "-sum_{d_1 != d_2 in O(T)} <Gcal_Y^(d_1), Gcal_Y^(d_2)>_Y in "
            "||Gcal_Y^(1)||_Y^2 = ||S_{sq,Y}||_Y^2 - sum_{d > 1 in O(T)} ||Gcal_Y^(d)||_Y^2 "
            "- sum_{d_1 != d_2 in O(T)} <Gcal_Y^(d_1), Gcal_Y^(d_2)>_Y "
            "(blocking a one-way upper bound on ||Gcal_Y^(1)||_Y^2 toward S_different(Y))"
        )

    saved_p = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # Audit CAND-A1 witnesses:
        w16_p = _parse_serialized_arb_enclosure_tc062(cand_a1.get("witness_Y16_g5"))
        w64_p = _parse_serialized_arb_enclosure_tc062(cand_a1.get("witness_Y64_g7"))
        a1_ok = bool(
            w16_p is not None
            and w64_p is not None
            and w16_p["c_lo"] > Fraction(7, 10000)
            and w64_p["c_lo"] > Fraction(1, 1000)
        )
        if isinstance(cand_a1, dict):
            cand_a1["refutation_certified"] = a1_ok
            cand_a1["outcome"] = (
                "REFUTED_BY_CERTIFIED_WITNESS" if a1_ok else "UNRESOLVED/INCOMPLETE_COVERAGE"
            )

        # Audit CAND-B1 margins on Y >= 16:
        rows_b = att_b.get("square_projection_and_moebius_rows", [])
        b1_ok = isinstance(rows_b, list) and len(rows_b) >= 3
        b_rows_ok = isinstance(rows_b, list) and len(rows_b) > 0
        for rb in rows_b if isinstance(rows_b, list) else []:
            if not isinstance(rb, dict):
                b1_ok = False
                b_rows_ok = False
                continue
            m_b1 = _parse_serialized_arb_enclosure_tc062(rb.get("TC063_CAND_B1_margin_sum_d_minus_S_sq"))
            r_sq = _parse_serialized_arb_enclosure_tc062(rb.get("pointwise_sq_proj_residual"))
            r_mb = _parse_serialized_arb_enclosure_tc062(rb.get("pointwise_odd_moebius_recovery_residual"))
            if rb.get("Y", 0) >= 16 and (m_b1 is None or m_b1["c_lo"] <= 0):
                b1_ok = False
            rok_b = bool(
                r_sq is not None
                and r_mb is not None
                and r_sq["c_lo"] <= 0 <= r_sq["c_hi"]
                and r_mb["c_lo"] <= 0 <= r_mb["c_hi"]
            )
            rb["verified"] = rok_b
            b_rows_ok = b_rows_ok and rok_b
        if isinstance(cand_b1, dict):
            cand_b1["refutation_certified"] = b1_ok
            cand_b1["outcome"] = (
                "REFUTED_BY_CERTIFIED_WITNESS" if b1_ok else "UNRESOLVED/INCOMPLETE_COVERAGE"
            )

        # Audit CAND-C1 witnesses:
        seed_p = _parse_serialized_arb_enclosure_tc062(cand_c1.get("seed_band_A_odd_64_sum"))
        greedy_p = _parse_serialized_arb_enclosure_tc062(cand_c1.get("greedy_pm1_witness_sum_Y64"))
        margin_c1_p = _parse_serialized_arb_enclosure_tc062(cand_c1.get("candidate_C1_margin_Y64"))
        c_chain_p = _parse_serialized_arb_enclosure_tc062(
            cand_c1.get("all_chain_length_subwindow_constant_c_chain")
        )
        c1_ok = bool(
            seed_p is not None
            and greedy_p is not None
            and margin_c1_p is not None
            and c_chain_p is not None
            and seed_p["c_hi"] <= greedy_p["c_lo"]
            and margin_c1_p["c_lo"] > Fraction(1, 5)
            and c_chain_p["c_lo"] > Fraction(1, 50)
        )
    finally:
        flint_ctx.prec = saved_p

    if isinstance(cand_c1, dict):
        cand_c1["refutation_and_omega_Y_obstruction_certified"] = c1_ok
        cand_c1["outcome"] = (
            "REFUTED_BY_CERTIFIED_WITNESS" if c1_ok else "UNRESOLVED/INCOMPLETE_COVERAGE"
        )
    rows_a = att_a.get("primitive_regrouping_rows", [])
    a_rows_ok = isinstance(rows_a, list) and len(rows_a) > 0
    for ra in rows_a if isinstance(rows_a, list) else []:
        r_pi = _parse_serialized_arb_enclosure_tc062(ra.get("primitive_minus_direct_residual")) if isinstance(ra, dict) else None
        rok_a = bool(r_pi is not None and r_pi["c_lo"] <= 0 <= r_pi["c_hi"])
        if isinstance(ra, dict):
            ra["verified"] = rok_a
        a_rows_ok = a_rows_ok and rok_a

    selb_err = _parse_serialized_arb_enclosure_tc062(
        att_b.get("station_selberg_decomposition_max_abs_error_Y16")
    )
    selb_ok = bool(selb_err is not None and selb_err["c_hi"] < Fraction(1, 10 ** 65))
    if isinstance(att_b, dict):
        att_b["station_selberg_decomposition_verified"] = selb_ok

    s4["all_section_4_checks_pass"] = bool(
        att_a.get("coprime_feature_decoupling_verified", False)
        and att_a.get("p2_smallop_jump_obstruction_certified", False)
        and a_rows_ok
        and a1_ok
        and b_rows_ok
        and b1_ok
        and selb_ok
        and c1_ok
    )
    return s4


def _audit_section_2_serialized_checks(sec2_raw: Dict[str, Any]) -> Dict[str, Any]:
    """Re-verify all 66 serialized Arb balls and sign-change flags in Section 2 (`R2-2`)."""
    s2 = json.loads(json.dumps(sec2_raw)) if isinstance(sec2_raw, dict) else {}
    rows = s2.get("complete_kernel_cross_validation_rows")
    rows_ok = isinstance(rows, list) and len(rows) == 6
    y16_pos = False
    y64_neg = False
    req_ball_fields = (
        "Sigma_off_2d_kernel",
        "S_same_2d_kernel",
        "S_different_2d_kernel",
        "S_same_1d_quadrature",
        "S_different_1d_quadrature",
        "Sigma_off_1d_quadrature",
        "algebraic_consistency_check_2d_residual",
        "algebraic_consistency_check_1d_residual",
        "independent_validation_S_same_1d_minus_2d",
        "independent_validation_S_different_1d_minus_2d",
        "independent_validation_Sigma_off_1d_minus_2d",
    )
    zero_fields = req_ball_fields[6:]
    for r in rows if isinstance(rows, list) else []:
        if not isinstance(r, dict):
            rows_ok = False
            continue
        parsed_r = {f: _parse_serialized_arb_enclosure_tc062(r.get(f)) for f in req_ball_fields}
        rok = all(v is not None for v in parsed_r.values()) and all(
            parsed_r[zf] is not None and parsed_r[zf]["c_lo"] <= 0 <= parsed_r[zf]["c_hi"]
            for zf in zero_fields
        )
        r["verified"] = rok
        rows_ok = rows_ok and rok
        if r.get("Y") == 16 and parsed_r["S_same_1d_quadrature"] is not None:
            y16_pos = bool(parsed_r["S_same_1d_quadrature"]["c_lo"] > 0)
        if r.get("Y") == 64 and parsed_r["S_same_1d_quadrature"] is not None:
            y64_neg = bool(parsed_r["S_same_1d_quadrature"]["c_hi"] < 0)
    if isinstance(s2.get("S_same_sign_change_certified"), dict):
        s2["S_same_sign_change_certified"]["Y_16_positive"] = y16_pos
        s2["S_same_sign_change_certified"]["Y_64_negative"] = y64_neg
    ex_ok = bool(
        isinstance(s2.get("exhaustive_exact_reindexing"), dict)
        and s2["exhaustive_exact_reindexing"].get("verified", False)
    )
    s2["all_section_2_checks_pass"] = bool(ex_ok and rows_ok and y16_pos and y64_neg)
    return s2


def _audit_section_3_serialized_checks(sec3_raw: Dict[str, Any]) -> Dict[str, Any]:
    """Re-verify all 260 serialized Arb balls, Hilbert margins, and matched-control verdicts in Section 3 (`R2-2`)."""
    s3 = json.loads(json.dumps(sec3_raw)) if isinstance(sec3_raw, dict) else {}
    uc = s3.get("uniform_constants")
    uc_ok = isinstance(uc, dict) and all(
        _parse_serialized_arb_enclosure_tc062(uc.get(k)) is not None
        for k in ("c_lambda", "c_half", "C_phi", "C_beta", "C_psi", "C_g", "C_same")
    )
    fchk = s3.get("shifted_station_disjointness_and_feature_checks")
    feat_rows = fchk.get("distinct_anchor_feature_rows") if isinstance(fchk, dict) else None
    feat_ok = (
        isinstance(fchk, dict)
        and bool(fchk.get("disjointness_verified_on_I2_180", False))
        and bool(fchk.get("m_eq_n_self_collision_indispensability_certified_at_Y16_m3", False))
        and isinstance(feat_rows, list)
        and len(feat_rows) == 3
    )
    for fr in feat_rows if isinstance(feat_rows, list) else []:
        fp = (
            _parse_serialized_arb_enclosure_tc062(fr.get("max_distinct_anchor_feature_abs_error"))
            if isinstance(fr, dict)
            else None
        )
        feat_ok = feat_ok and bool(
            fp is not None and fp["c_lo"] <= 0 <= fp["c_hi"] and fp["c_hi"] < Fraction(1, 10 ** 50)
        )
    if isinstance(fchk, dict):
        fchk["verified"] = feat_ok

    same_rows = s3.get("same_chain_hilbert_bound_rows")
    same_ok = isinstance(same_rows, list) and len(same_rows) == 10
    for sr in same_rows if isinstance(same_rows, list) else []:
        if not isinstance(sr, dict):
            same_ok = False
            continue
        sp = {
            f: _parse_serialized_arb_enclosure_tc062(sr.get(f))
            for f in (
                "S_same_Y",
                "sum_psi_sq_le_T",
                "sum_log2_G2_le_T",
                "local_hilbert_bound",
                "uniform_log_bound_C_same_1_plus_log_Y",
                "local_margin_abs_S_same_minus_bound",
                "uniform_margin_abs_S_same_minus_bound",
            )
        }
        sok = (
            all(v is not None for v in sp.values())
            and sp["local_margin_abs_S_same_minus_bound"]["c_hi"] <= 0
            and sp["uniform_margin_abs_S_same_minus_bound"]["c_hi"] <= 0
        )
        sr["verified"] = sok
        same_ok = same_ok and sok

    ctrl_rows = s3.get("matched_control_and_hybrid_chain_rows")
    ctrl_ok = isinstance(ctrl_rows, list) and len(ctrl_rows) == 30
    neg_refuted_ok = True
    for cr in ctrl_rows if isinstance(ctrl_rows, list) else []:
        if not isinstance(cr, dict):
            ctrl_ok = False
            neg_refuted_ok = False
            continue
        rat_obj = cr.get("S_different_over_log_Y_D_tilde")
        cp = {
            f: _parse_serialized_arb_enclosure_tc062(cr.get(f))
            for f in (
                "S_same_Y",
                "S_different_Y",
                "D_tilde_Y",
                "log_Y_times_D_tilde",
                "TC063_P0_DIFF_margin",
            )
        }
        rp = (
            _parse_serialized_arb_enclosure_tc062(rat_obj.get("ratio"))
            if isinstance(rat_obj, dict)
            else None
        )
        if not all(v is not None for v in cp.values()) or rp is None:
            ctrl_ok = False
            neg_refuted_ok = False
            continue
        mp = cp["TC063_P0_DIFF_margin"]
        exp_cv = "PASS" if mp["c_hi"] <= 0 else ("FAIL" if mp["c_lo"] > 0 else "UNRESOLVED")
        if cr.get("TC063_P0_DIFF_verdict") != exp_cv:
            ctrl_ok = False
        if cr.get("Y", 0) >= 64:
            if cr.get("mode") == "liouville" and exp_cv != "PASS":
                ctrl_ok = False
            elif cr.get("mode") != "liouville" and exp_cv != "FAIL":
                neg_refuted_ok = False
    s3["all_negative_controls_refuted_on_S_different_for_Y_ge_64"] = neg_refuted_ok
    s3["all_section_3_checks_pass"] = bool(
        uc_ok
        and feat_ok
        and same_ok
        and bool(s3.get("control_2d_vs_1d_cross_check_Y16_verified", False))
        and ctrl_ok
        and neg_refuted_ok
    )
    return s3


def reprocess_task_tc063_metadata_and_lean_audit(
    artifact_path: Path = DYADIC_CHAIN_ARTIFACT_PATH,
    *,
    write_output: bool = True,
    validation_commit_override: Optional[str] = None,
    protocol_override: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Re-run full 674-ball serialized Arb validation, Section 1/2/3/4/5 validation, Section 6 live
    Lean declaration audit, and provenance synchronization on an existing `TC-063` artifact
    WITHOUT altering any numerical Arb ball or `numerical_producing_git_commit`.
    """
    existing = json.loads(Path(artifact_path).read_text(encoding="utf-8"))
    prov = existing.get("provenance")
    if (
        not isinstance(prov, dict)
        or not isinstance(prov.get("numerical_producing_git_commit"), str)
        or not prov["numerical_producing_git_commit"].strip()
        or not isinstance(existing.get("generated_at_utc"), str)
        or not existing["generated_at_utc"].strip()
    ):
        bad_out = dict(existing)
        bad_out["execution_and_certification_status"] = "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED"
        bad_out["holdout_hypothesis_outcome"] = CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
        bad_out["all_mathematical_and_numerical_checks_pass"] = False
        return bad_out

    if protocol_override is not None:
        proto_obj = protocol_override
    else:
        proto_chk = verify_frozen_tc063_protocol_immutability()
        if not proto_chk["verified"]:
            bad_p = dict(existing)
            bad_p["execution_and_certification_status"] = "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED"
            bad_p["holdout_hypothesis_outcome"] = CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
            bad_p["all_mathematical_and_numerical_checks_pass"] = False
            return bad_p
        proto_obj = proto_chk["protocol_object"]

    sec1_upd = _audit_section_1_serialized_checks(
        existing.get("section_1_protocols_endpoint_and_premise_chain", {})
    )
    sec2_upd = _audit_section_2_serialized_checks(
        existing.get("section_2_odd_part_decomposition_and_cross_checks", {})
    )
    sec3_upd = _audit_section_3_serialized_checks(
        existing.get("section_3_same_chain_bound_and_matched_controls", {})
    )
    sec4_upd = _audit_section_4_serialized_checks(
        existing.get("section_4_distinct_chain_attempts_and_obstructions", {})
    )
    sec5_upd, top_fields = aggregate_tc063_section5_and_derive_outcomes(
        existing.get("section_5_unseen_validation_and_interval_splits", {}), proto_obj
    )
    sec6_upd = verify_section_6_lean_audit_and_gate_accounting()

    val_commit = validation_commit_override or _get_git_head_commit()
    formal_commit = (
        sec6_upd["lean_module_audit"].get("formal_producing_git_commit")
        or prov.get("formal_producing_git_commit")
    )

    updated = dict(existing)
    updated.update(top_fields)
    new_prov = dict(prov)
    new_prov["validation_git_commit"] = val_commit
    new_prov["formal_producing_git_commit"] = formal_commit
    new_prov["reprocessed_at_utc"] = datetime.now(timezone.utc).isoformat()
    updated["provenance"] = new_prov
    updated["section_1_protocols_endpoint_and_premise_chain"] = sec1_upd
    updated["section_2_odd_part_decomposition_and_cross_checks"] = sec2_upd
    updated["section_3_same_chain_bound_and_matched_controls"] = sec3_upd
    updated["section_4_distinct_chain_attempts_and_obstructions"] = sec4_upd
    updated["section_5_unseen_validation_and_interval_splits"] = sec5_upd
    updated["section_6_lean_audit_and_gate_accounting"] = sec6_upd

    arb_rechk = _audit_all_serialized_arb_balls_in_artifact(
        updated, existing.get("serialized_arb_self_check")
    )
    updated["serialized_arb_self_check"] = arb_rechk
    if not arb_rechk["all_enclose_original_256bit_arb_ball"]:
        updated["execution_and_certification_status"] = "CERTIFICATION_INTEGRITY_CONFLICT_BLOCKED"
        updated["holdout_hypothesis_outcome"] = CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
        updated["primary_log_saving_probe_outcome"] = CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME

    updated["all_mathematical_and_numerical_checks_pass"] = bool(
        sec1_upd["all_section_1_checks_pass"]
        and sec2_upd["all_section_2_checks_pass"]
        and sec3_upd["all_section_3_checks_pass"]
        and sec4_upd["all_section_4_checks_pass"]
        and sec5_upd["all_section_5_checks_pass"]
        and sec6_upd["all_section_6_checks_pass"]
        and arb_rechk["all_enclose_original_256bit_arb_ball"]
        and updated["holdout_hypothesis_outcome"] != CERTIFICATION_INTEGRITY_CONFLICT_OUTCOME
    )
    updated["provenance"]["self_verdict_comparison"] = compare_tc063_artifacts_by_stable_key(
        updated, existing
    )

    if write_output:
        txt_out = json.dumps(updated, indent=2, ensure_ascii=True) + "\n"
        Path(artifact_path).write_bytes(txt_out.encode("utf-8"))
    return updated


if __name__ == "__main__":
    t_start = time.perf_counter()
    art_out = generate_task_tc063_artifact(write_output=True)
    dt_all = time.perf_counter() - t_start
    print(
        f"Generated {DYADIC_CHAIN_ARTIFACT_PATH.name} in {dt_all:.2f}s | "
        f"outcome={art_out['holdout_hypothesis_outcome']} | "
        f"resource={art_out['resource_compliance_status']} | "
        f"balls={art_out['serialized_arb_self_check']['total_certified_arb_balls_checked']} | "
        f"all_pass={art_out['all_mathematical_and_numerical_checks_pass']}"
    )
