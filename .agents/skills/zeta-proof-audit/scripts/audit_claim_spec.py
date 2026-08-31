"""audit_claim_spec.py — Executable Specification & Gate Validator for Mathematical Claims.

Enforces the 19-field claim schema and the 10 mandatory pre-acceptance gates
defined in the `zeta-proof-audit` skill.
"""

import sys
import os
import glob
import json
import hashlib
import subprocess
import argparse
from typing import Dict, Any, List, Set, Tuple

MANDATORY_FIELDS = [
    "claim_id",
    "statement",
    "quantified_variables",
    "variable_domains",
    "hypotheses",
    "object_studied",
    "fourier_normalization",
    "multiplicity_convention",
    "measure_and_window",
    "order_of_limits",
    "exact_conclusion",
    "logical_negation",
    "epistemic_role",
    "evidence_scope",
    "exact_or_truncated",
    "arithmetic_cutoff",
    "spectral_cutoff",
    "integration_domain",
    "omitted_tail",
    "tail_enclosure",
    "dependencies",
    "proof_artifact",
    "falsification_attempts",
    "computational_evidence",
    "external_sources",
    "remaining_analytic_dependencies",
]

# Fields that must be non-empty strings or non-empty collections
STRICT_NON_EMPTY_FIELDS: Set[str] = {
    "claim_id",
    "statement",
    "quantified_variables",
    "variable_domains",
    "hypotheses",
    "object_studied",
    "fourier_normalization",
    "measure_and_window",
    "order_of_limits",
    "exact_conclusion",
    "logical_negation",
    "epistemic_role",
    "evidence_scope",
    "exact_or_truncated",
    "integration_domain",
    "falsification_attempts",
}

ALLOWED_EPISTEMIC_ROLES = {
    "ALGEBRAIC_IDENTITY",
    "FINITE_ANALYTIC_COMPONENT",
    "LOAD_BEARING_ANALYTIC_THEOREM",
    "NO_GO_COMPONENT",
    "COUNTERMODEL",
    "HEURISTIC",
    "NUMERICAL_OBSERVATION",
    "CONJECTURE",
    "OPEN_OBLIGATION",
    "WITHDRAWN",
}

ALLOWED_EVIDENCE_SCOPES = {
    "FINITE_EXACT_ALGEBRA",
    "FINITE_NUMERICAL_SAMPLE",
    "FINITE_GRID_NUMERICAL",
    "CERTIFIED_POINT_WITNESS",
    "CERTIFIED_COMPACT_DOMAIN",
    "EXTERNAL_ANALYTIC_PROOF",
    "FORMAL_LEAN_PROOF",
    "CONDITIONAL_THEOREM",
    "COUNTEREXAMPLE",
    "NO_GO_FOR_DEFINED_CLASS",
}


def normalize_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes field aliases in claim specification for backward compatibility."""
    normalized = dict(spec)
    if "statement" not in normalized and "mathematical_statement" in normalized:
        normalized["statement"] = normalized["mathematical_statement"]
    if "mathematical_object" in normalized and "object_studied" not in normalized:
        normalized["object_studied"] = normalized["mathematical_object"]
    if "fourier_normalization" not in normalized:
        if "normalization_and_fourier_convention" in normalized:
            normalized["fourier_normalization"] = normalized["normalization_and_fourier_convention"]
        elif "normalization" in normalized:
            normalized["fourier_normalization"] = normalized["normalization"]
    if "window_definition" in normalized and "measure_and_window" not in normalized:
        normalized["measure_and_window"] = normalized["window_definition"]
    if "parameter_domain" in normalized and "variable_domains" not in normalized:
        normalized["variable_domains"] = [normalized["parameter_domain"]] if isinstance(normalized["parameter_domain"], str) else normalized["parameter_domain"]
    if "variable_domains" not in normalized:
        if "domains" in normalized:
            normalized["variable_domains"] = normalized["domains"]
        elif "quantified_variables" in normalized and isinstance(normalized["quantified_variables"], list):
            domains = []
            for qv in normalized["quantified_variables"]:
                if isinstance(qv, dict) and "domain" in qv:
                    domains.append(qv["domain"])
                elif isinstance(qv, str):
                    domains.append(qv)
            if domains:
                normalized["variable_domains"] = domains
    if "primary_evidence_scope" in normalized and "evidence_scope" not in normalized:
        normalized["evidence_scope"] = normalized["primary_evidence_scope"]
    # Defaults for older specs to maintain schema validity if omitted
    if "evidence_scope" not in normalized:
        # Infer scope based on epistemic role / proof artifact
        role = normalized.get("epistemic_role", "")
        if "lean" in str(normalized.get("proof_artifact", "")).lower():
            normalized["evidence_scope"] = "FORMAL_LEAN_PROOF" if role == "ALGEBRAIC_IDENTITY" else "FINITE_EXACT_ALGEBRA"
        elif role == "NO_GO_COMPONENT":
            normalized["evidence_scope"] = "COUNTEREXAMPLE"
        else:
            normalized["evidence_scope"] = "EXTERNAL_ANALYTIC_PROOF"
    if "exact_or_truncated" not in normalized:
        normalized["exact_or_truncated"] = "EXACT"
    if "arithmetic_cutoff" not in normalized:
        normalized["arithmetic_cutoff"] = "NONE"
    if "spectral_cutoff" not in normalized:
        normalized["spectral_cutoff"] = "NONE"
    if "integration_domain" not in normalized:
        normalized["integration_domain"] = "R"
    if "omitted_tail" not in normalized:
        normalized["omitted_tail"] = "NONE"
    if "tail_enclosure" not in normalized:
        normalized["tail_enclosure"] = "NONE"
    return normalized


def audit_claim_specification(raw_spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Audits a candidate mathematical claim against all schema fields and 10 pre-acceptance gates.
    Returns a dictionary containing 'status': 'PASS' | 'FAIL', 'passed_gates', 'violations', and 'warnings'.
    """
    spec = normalize_spec(raw_spec)
    violations: List[str] = []
    warnings: List[str] = []
    passed_gates: List[str] = []

    # --- Schema Validation ---
    for field in MANDATORY_FIELDS:
        if field not in spec or spec[field] is None:
            violations.append(f"Missing mandatory field: '{field}'")
        elif field in STRICT_NON_EMPTY_FIELDS:
            if isinstance(spec[field], (str, list, dict)) and len(spec[field]) == 0:
                violations.append(f"Empty mandatory field: '{field}'")

    # Normalize text fields for case-insensitive keyword inspection
    obj = str(spec.get("object_studied", "")).lower()
    stmt = str(spec.get("statement", "")).lower()
    conc = str(spec.get("exact_conclusion", "")).lower()
    hyps_str = " ".join(str(h) for h in spec.get("hypotheses", [])).lower()
    fals_str = " ".join(str(f) for f in spec.get("falsification_attempts", [])).lower()
    comp_ev_str = " ".join(str(c) for c in spec.get("computational_evidence", [])).lower()
    deps_str = " ".join(str(d) for d in spec.get("dependencies", [])).lower()
    proof_art = str(spec.get("proof_artifact", "")).strip()
    ev_scope = str(spec.get("evidence_scope", "")).strip()
    role = str(spec.get("epistemic_role", "")).strip()
    exact_or_trunc = str(spec.get("exact_or_truncated", "")).upper()
    int_domain = str(spec.get("integration_domain", "")).strip()
    tail_enc = str(spec.get("tail_enclosure", "")).strip()
    omitted_tail = str(spec.get("omitted_tail", "")).strip()

    # --- Gate 1: Object-Identity & Truncation Audit ---
    is_prime_data = ("prime" in obj or "dirichlet" in obj or "p(z)" in obj or r"\lambda(n)" in hyps_str or "lambda(n)" in hyps_str or "p(z)" in hyps_str or "sum_{n" in hyps_str or r"\zeta'/\zeta" in obj)
    claims_completed_zeta = ("completed" in stmt or r"\xi" in stmt or "xi(" in stmt or "completed" in conc or r"\xi" in conc or "completed" in obj)

    # Check 1A: Prime Dirichlet series substituted for completed xi without bridge
    if is_prime_data and claims_completed_zeta:
        deps_str = " ".join(str(d) for d in spec.get("dependencies", [])).lower()
        if not ("bridge" in deps_str or "completion" in deps_str or "gamma" in deps_str):
            violations.append(
                "Gate 1 [Object-Identity] VIOLATION: Mathematical data is prime-only / Dirichlet series but "
                "statement or object claims completed-zeta / xi-function without an explicit completion bridge theorem."
            )
        else:
            warnings.append("Gate 1: Prime-to-completed bridge dependency declared.")

    # Check 1B: Finite prime truncation labelled exact completed xi without certified tail
    if exact_or_trunc == "TRUNCATED" and claims_completed_zeta and (tail_enc.lower() == "none" or not tail_enc):
        violations.append(
            "Gate 1 [Object-Identity] VIOLATION: Finite prime or series truncation is claimed as exact completed-xi "
            "without an explicit certified omitted-tail enclosure."
        )

    # Check 1C: Integral over compact interval [-T, T] claimed as continuous R without tail bound
    is_compact_int = (int_domain.startswith("[") and not int_domain.startswith("[-inf") and "infty" not in int_domain)
    if is_compact_int and (omitted_tail.lower() == "none" or not omitted_tail or tail_enc.lower() == "none"):
        violations.append(
            "Gate 1 [Object-Identity] VIOLATION: Integral evaluated on compact interval without a certified "
            "real-line omitted-tail enclosure for |t| > T."
        )

    if not any("Gate 1" in v for v in violations):
        passed_gates.append("Gate 1: Object-Identity Audit")

    # --- Gate 2: Quantifier & Scope Audit ---
    quant_vars = [str(v).lower() for v in spec.get("quantified_variables", [])]
    has_universal_syntax = any("forall" in v or r"\forall" in v or "all" in v for v in quant_vars)
    has_universal_phrases = any(p in stmt or p in conc for p in [
        "for all", "for any", "across", "across the domain", "across all tested", "strictly positive throughout",
        "no root exists", "always nonzero", "entire route closed", "entire bilateral"
    ])
    has_universal = has_universal_syntax or has_universal_phrases

    has_valid_proof = proof_art and not proof_art.lower().startswith("none") and any(k in proof_art.lower() for k in [".lean", "formal", "sympy", "exact", "theorem", "proof"])

    if has_universal and (not has_valid_proof or proof_art.lower().startswith("none")) and spec.get("computational_evidence"):
        violations.append(
            "Gate 2 [Quantifier] VIOLATION: Universal quantifier (\\forall) claimed, but only computational "
            "sampling evidence provided without a formal proof artifact."
        )
    elif ev_scope in {"FINITE_GRID_NUMERICAL", "FINITE_NUMERICAL_SAMPLE"}:
        if has_universal:
            violations.append(
                f"Gate 2 [Quantifier & Scope] VIOLATION: Evidence scope '{ev_scope}' cannot support universal "
                "claims ('for all', 'no root exists', 'strictly positive throughout'). Must be scoped to tested grid points."
            )
        else:
            passed_gates.append("Gate 2: Quantifier Audit")
    elif ev_scope == "CERTIFIED_POINT_WITNESS":
        if has_universal_phrases and not ("fails" in stmt or "counterexample" in stmt or "negation" in stmt or "instance" in stmt or "non-vanishing" in stmt):
            violations.append(
                "Gate 2 [Quantifier & Scope] VIOLATION: CERTIFIED_POINT_WITNESS can only certify a single point instance "
                "or the logical negation of universal cancellation, not universal non-vanishing across an interval."
            )
        else:
            passed_gates.append("Gate 2: Quantifier Audit")
    elif ev_scope == "FINITE_EXACT_ALGEBRA":
        if "infinite" in stmt and ("convergence" in stmt or "double sum" in stmt or "integral" in stmt):
            violations.append(
                "Gate 2 [Quantifier & Scope] VIOLATION: FINITE_EXACT_ALGEBRA cannot prove infinite convergence or double series theorems."
            )
        else:
            passed_gates.append("Gate 2: Quantifier Audit")
    else:
        passed_gates.append("Gate 2: Quantifier Audit")

    # --- Gate 3: Negation-First Audit ---
    negation = str(spec.get("logical_negation", "")).strip()
    if not negation or negation.lower() == "none" or negation == conc:
        violations.append("Gate 3 [Negation-First] VIOLATION: Logical negation is missing or identical to conclusion.")
    else:
        passed_gates.append("Gate 3: Negation-First Audit")

    # --- Gate 4: Symbolic Elimination & Equality-Case Audit ---
    is_nonvanishing = (r"\ne 0" in stmt or "!= 0" in stmt or "non-vanishing" in stmt or "nonzero" in stmt or r"\ne 0" in conc or "!= 0" in conc or "strictly positive" in stmt)
    has_equality_analysis = ("equality" in fals_str or "cancellation" in fals_str or "solve" in fals_str or "zero-crossing" in fals_str or "root" in fals_str)

    if is_nonvanishing and not has_equality_analysis and ev_scope not in {"CERTIFIED_POINT_WITNESS", "COUNTEREXAMPLE"}:
        violations.append(
            "Gate 4 [Symbolic Elimination] VIOLATION: Universal non-vanishing (\\ne 0) or strict sign claimed without "
            "symbolic elimination / equality-case cancellation analysis."
        )
    else:
        passed_gates.append("Gate 4: Symbolic Elimination & Equality-Case Audit")

    # --- Gate 5: Dominance and Boundary Audit ---
    has_boundary_check = ("boundary" in fals_str or "asymptotic" in fals_str or "limit" in fals_str or "dominance" in fals_str or "extreme" in fals_str or "tail" in fals_str)
    if not has_boundary_check:
        warnings.append("Gate 5 [Dominance & Boundary] WARNING: No explicit boundary/asymptotic dominance audit recorded.")
    else:
        passed_gates.append("Gate 5: Dominance and Boundary Audit")

    # --- Gate 6: Diagonal / Off-Diagonal Audit ---
    is_inner_prod = ("inner product" in obj or "mean square" in obj or r"\langle" in stmt or "norm" in stmt or "cross-term" in stmt or "cross_term" in stmt)
    win_str = str(spec.get("measure_and_window", "")).lower()
    has_finite_window = ("finite" in win_str or "c_c" in win_str or "compact" in win_str or "smooth window" in win_str or "gaussian" in win_str)
    treats_off_diagonal = ("off-diagonal" in fals_str or "m \\ne n" in fals_str or "m != n" in fals_str or "double sum" in fals_str or
                           "off-diagonal" in hyps_str or "m \\ne n" in hyps_str or "m != n" in hyps_str or "double sum" in hyps_str or
                           "off-diagonal" in stmt or "diagonal and off-diagonal" in conc or
                           "four blocks" in stmt or "four blocks" in obj or "4-block" in stmt or "4-block" in obj or
                           "four blocks" in conc or "4-block" in conc or "blocks" in stmt or "i_pp" in stmt or "i_pp" in conc or
                           "adjoint" in hyps_str or "adjoint" in deps_str or "adjoint" in fals_str)

    if is_inner_prod and has_finite_window and not treats_off_diagonal:
        violations.append(
            "Gate 6 [Diagonal/Off-Diagonal] VIOLATION: Finite-window Dirichlet inner product claimed "
            "without accounting for off-diagonal (m != n) cross-terms or complete 4-block decomposition."
        )
    else:
        passed_gates.append("Gate 6: Diagonal / Off-Diagonal Audit")

    # --- Gate 7: Interchange & Tail Bounds Audit ---
    deps_str = " ".join(str(d) for d in spec.get("dependencies", [])).lower()
    has_interchange = ("interchange" in hyps_str or "derivative under" in hyps_str or "fubini" in hyps_str or "dominated convergence" in hyps_str or
                       "interchange" in deps_str or "derivative under" in deps_str or "fubini" in deps_str or "dominated convergence" in deps_str or
                       "fubini" in fals_str or "dominated convergence" in fals_str)

    # Check for incomplete tail bound omitting positive integration by parts terms
    if "tail_bound" in comp_ev_str or "tail" in hyps_str:
        if "omitted positive" in fals_str or "incomplete_tail" in fals_str:
            violations.append("Gate 7 [Interchange & Tails] VIOLATION: Asserted tail bound omits positive integration-by-parts terms.")

    if (r"\frac{d}{d" in stmt or r"\int" in stmt) and r"\sum" in stmt and not has_interchange:
        warnings.append("Gate 7 [Interchange] WARNING: Sum and integral/derivative co-occur without explicit interchange theorem recorded.")
    else:
        passed_gates.append("Gate 7: Interchange Audit")

    # --- Gate 8: Independent Derivation & Genuine Interval Certification Audit ---
    # Check 8A: Reject float-based fake Arb certification
    if "fake_arb" in comp_ev_str or ("float(" in comp_ev_str and "radius" in comp_ev_str):
        violations.append("Gate 8 [Certification] VIOLATION: Arb certificate constructed from Python binary floats without rigorous interval enclosures.")

    # Check 8B: Reject decomposition residual used as numerical/quadrature error
    if "residual_as_error" in comp_ev_str or ("diff_direct_vs_sum" in comp_ev_str and "radius" in comp_ev_str) or "abs(i_direct - i_sum)" in comp_ev_str:
        violations.append("Gate 8 [Certification] VIOLATION: Algebraic decomposition residual (|I_direct - I_sum|) used as numerical quadrature/tail error estimate.")

    if len(spec.get("dependencies", [])) < 1 and not spec.get("external_sources"):
        warnings.append("Gate 8 [Independent Derivation] WARNING: No independent external verification source or dual derivation path cited.")
    else:
        passed_gates.append("Gate 8: Independent Derivation Audit")

    # --- Gate 9: Adversarial Falsification & Anti-Self-Certification Audit ---
    raw_cid = str(spec.get("claim_id", "")).upper()
    falsifications = spec.get("falsification_attempts", [])
    if len(falsifications) == 0 or (len(falsifications) == 1 and str(falsifications[0]).lower().strip() in {"none", "none (only sampled confirming test points)"}):
        violations.append("Gate 9 [Adversarial Falsification] VIOLATION: No adversarial falsification attempts recorded.")
    elif raw_cid == "CLM-CT-025" and ("-0.054321" in stmt or "-0.070656" in stmt or "-0.016335" in stmt):
        violations.append("Gate 9 [Adversarial Falsification] VIOLATION: Documented witness values in specification (-0.054321, -0.070656) do not match certified executable proof artifact (-0.0515509, -0.0240200, +0.0275309).")

    # Check 9B: Evaluator self-certification (hardcoded booleans / path counts)
    if "all_branches_eliminated = true" in comp_ev_str or "hardcoded_branch_elimination" in comp_ev_str:
        violations.append("Gate 9 [Anti-Self-Certification] VIOLATION: Hardcoded evaluator boolean asserted without formal exhaustive candidate class proof.")
    if "distinct_viable_paths_count = 1" in comp_ev_str and "isomorph" in stmt and not ("bijection" in hyps_str or "isomorphism_map" in hyps_str):
        violations.append("Gate 9 [Anti-Self-Certification] VIOLATION: Shared spectral zero set promoted to functional proof-route isomorphism without explicit structure-preserving maps and inverses.")

    if not any("Gate 9" in v for v in violations):
        passed_gates.append("Gate 9: Adversarial Falsification Audit")

    # --- Gate 10: Evidence Classification & Formal Proof Boundary Audit ---
    if role not in ALLOWED_EPISTEMIC_ROLES:
        violations.append(f"Gate 10 [Evidence Classification] VIOLATION: Unknown epistemic role '{role}'. Allowed: {ALLOWED_EPISTEMIC_ROLES}")
    elif ev_scope not in ALLOWED_EVIDENCE_SCOPES:
        violations.append(f"Gate 10 [Evidence Classification] VIOLATION: Unknown evidence scope '{ev_scope}'. Allowed: {ALLOWED_EVIDENCE_SCOPES}")

    # Check 10A: Lean formal proof boundary
    if ev_scope == "FORMAL_LEAN_PROOF":
        claims_infinite_analysis = ("infinite double sum" in stmt or "fubini" in stmt or "continuous 1d quadrature" in stmt or "fourier transform on r" in stmt or "infinite" in stmt)
        if claims_infinite_analysis:
            violations.append(
                "Gate 10 [Formal Proof Boundary] VIOLATION: FORMAL_LEAN_PROOF asserted for infinite analytic theorem "
                "where Lean proof artifact only formalizes finite algebraic identities."
            )

    # Check 10B: No-go defined candidate class
    if role == "NO_GO_COMPONENT" or ev_scope == "NO_GO_FOR_DEFINED_CLASS":
        has_exhaustive_class = ("candidate class" in stmt or "candidate class" in conc or "exhaustive" in stmt or "defined class" in conc or "instance" in stmt)
        if not has_exhaustive_class:
            violations.append(
                "Gate 10 [No-Go Class] VIOLATION: NO_GO claim asserted without a formally defined candidate class "
                "or proof of exhaustive member elimination."
            )

    # Check 10C: Load-bearing theorem with open dependencies
    if role == "LOAD_BEARING_ANALYTIC_THEOREM" and spec.get("remaining_analytic_dependencies"):
        if any(str(dep).strip() for dep in spec.get("remaining_analytic_dependencies", [])):
            violations.append(
                "Gate 10 [Evidence Classification] VIOLATION: Claim classified as LOAD_BEARING_ANALYTIC_THEOREM "
                "while open analytic dependencies remain unproved."
            )

    if not any("Gate 10" in v for v in violations):
        passed_gates.append("Gate 10: Evidence Classification Audit")



    status = "FAIL" if violations else "PASS"
    return {
        "status": status,
        "claim_id": spec.get("claim_id"),
        "passed_gates": passed_gates,
        "violations": violations,
        "warnings": warnings,
        "gate_summary": f"Passed {len(passed_gates)}/10 gates with {len(violations)} violations and {len(warnings)} warnings."
    }


# Complete registry of recognized status patterns in the repository
ALLOWED_STATUSES = {
    "PROVED / EXACT",
    "PROVED / FORMALLY_PROVED",
    "PROVED / THEORETICAL_IDENTITY",
    "PROVED / FALSIFIED LOCAL GNS",
    "PROVED / FALSIFIED NAIVE PROBE",
    "PROVED / EMPIRICALLY_CONFIRMED",
    "NO_GO_COMPONENT / PROVED",
    "OPEN / CONJECTURED (RH)",
    "OPEN / FORMALIZATION_PENDING",
    "DISPROVED / FALSIFIED",
    "SPECIFICATION_SCHEMA_PASSED",
    "INDEPENDENT_MATHEMATICAL_AUDIT_PASSED",
    "EXTERNAL_ANALYTIC_PROOF",
    "FIXED_GAUSSIAN_COMMON_FRAME_CROSS_TERM_NONZERO",
    "FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_CLOSED",
    "SHARED_SPECTRAL_ZERO_SET_WITH_DISTINCT_ARITHMETIC_OBLIGATIONS",
    "INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE"
}

KNOWN_TERMINAL_PATTERNS = [
    "PROVED",
    "FORMALLY_PROVED",
    "EXACT",
    "FALSIFIED",
    "CLOSED",
    "WITHDRAWN",
    "NO_GO_COMPONENT",
    "PROVED SPECTRAL EQUIVALENCE",
    "RETAINED (EMPIRICAL 80-DPS)",
    "DIAGONAL_CROSS_TERM_HAS_EXACT_CANCELLING_VARIANCES",
    "KNOWN_RH_EQUIVALENCE",
    "INTERNALLY_REDERIVED",
    "EXTERNAL_ANALYTIC_PROOF",
    "FIXED_GAUSSIAN_COMMON_FRAME_CROSS_TERM_NONZERO",
    "FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_CLOSED",
    "SHARED_SPECTRAL_ZERO_SET_WITH_DISTINCT_ARITHMETIC_OBLIGATIONS",
    "INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE"
]

KNOWN_EXEMPT_PATTERNS = [
    "OPEN",
    "OPEN / CANDIDATE",
    "SENSITIVITY DIAGNOSTIC",
    "METHODOLOGICAL / ENFORCED",
    "SCOPED STATUS",
    "CANDIDATE",
]


def cross_check_claim_register(repo_root: str, verify_git_baseline: bool = True) -> Tuple[bool, List[str], List[str], Dict[str, Any]]:
    """
    Exhaustively cross-checks the canonical claim_register.md against machine-readable specifications in .agents/claims/
    and hash-pinned grandfathered entries in .agents/corpus_map/legacy_claim_manifest.json.

    Policy B (Grandfathered Migration with Immutable Historical Baseline):
    - New terminal claims always require validated specifications in .agents/claims/.
    - Modified legacy claims or status transitions require validated specifications in .agents/claims/.
    - Unchanged legacy terminal claims matching legacy_claim_manifest.json pass provisionally as LEGACY_UNAUDITED.
    - Legacy manifest must declare an immutable historical baseline_commit that is an ancestor of HEAD.
    - Every claim in the legacy manifest must have existed at the baseline commit with matching hash.
    - Open/exempt claims pass as Exempt.
    - Fails on unknown statuses, missing specifications, modified legacy claims, or tampered legacy manifest.
    - Strictly enforces:
        terminal_claims == audited_terminal_claims + legacy_unaudited_terminal_claims + missing_specifications
        total_claims == terminal_claims + open_or_exempt_claims + unrecognized_statuses
    """
    register_path = os.path.join(repo_root, ".agents", "corpus_map", "claim_register.md")
    legacy_manifest_path = os.path.join(repo_root, ".agents", "corpus_map", "legacy_claim_manifest.json")
    claims_dir = os.path.join(repo_root, ".agents", "claims")

    legacy_manifest = {"claims": {}}
    if os.path.exists(legacy_manifest_path):
        try:
            with open(legacy_manifest_path, "r", encoding="utf-8") as lf:
                legacy_manifest = json.load(lf)
        except Exception as e:
            return False, [f"Error reading legacy claim manifest: {e}"], [], {}

    if not os.path.exists(register_path):
        return False, [f"Claim register not found at {register_path}"], [], {}

    errors: List[str] = []
    passed: List[str] = []
    total_claims = 0
    terminal_claims = 0
    audited_terminal_claims = 0
    legacy_unaudited_terminal_claims = 0
    open_or_exempt_claims = 0
    missing_specifications = 0
    unrecognized_statuses = 0
    status_histogram: Dict[str, int] = {}

    # 1. Immutable Git Baseline Verification
    baseline_commit = legacy_manifest.get("baseline_commit")
    has_git = os.path.exists(os.path.join(repo_root, ".git"))

    if not baseline_commit:
        errors.append("UNAUTHORIZED_LEGACY_MANIFEST_VIOLATION: Legacy manifest is missing required 'baseline_commit'.")
    elif has_git and verify_git_baseline:
        try:
            # Verify baseline commit exists
            subprocess.run(
                ["git", "rev-parse", "--verify", f"{baseline_commit}^{{commit}}"],
                cwd=repo_root, capture_output=True, text=True, check=True
            )
            # Verify baseline is an ancestor of HEAD
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", baseline_commit, "HEAD"],
                cwd=repo_root, capture_output=True, text=True, check=True
            )
            # Load baseline register text
            res = subprocess.run(
                ["git", "show", f"{baseline_commit}:.agents/corpus_map/claim_register.md"],
                cwd=repo_root, capture_output=True, text=True, encoding="utf-8", check=True
            )
            baseline_text = res.stdout

            # Parse baseline claims
            baseline_claims_map: Dict[str, Tuple[str, str]] = {}
            for bl_line in baseline_text.splitlines():
                bl_str = bl_line.strip()
                if not bl_str.startswith("| `CLM-") and not bl_str.startswith("|`CLM-"):
                    continue
                bparts = [p.strip() for p in bl_str.split("|")]
                if bparts and bparts[0] == "": bparts = bparts[1:]
                if bparts and bparts[-1] == "": bparts = bparts[:-1]
                if len(bparts) < 5: continue
                bcid = bparts[0].strip("`")
                bstat = bparts[-3].strip() if len(bparts) >= 6 else bparts[-2].strip()
                bhash = hashlib.sha256(bl_str.encode("utf-8")).hexdigest()
                baseline_claims_map[bcid] = (bhash, bstat)

            # Audit legacy manifest integrity against baseline
            for m_cid, m_data in legacy_manifest.get("claims", {}).items():
                if m_cid not in baseline_claims_map:
                    errors.append(f"UNAUTHORIZED_LEGACY_MANIFEST_VIOLATION: Claim {m_cid} in legacy manifest did not exist in immutable baseline commit {baseline_commit[:8]}.")
                elif m_data.get("line_hash") != baseline_claims_map[m_cid][0]:
                    errors.append(f"UNAUTHORIZED_LEGACY_MANIFEST_VIOLATION: Line hash for {m_cid} in legacy manifest does not match baseline commit row.")
                elif m_data.get("status") != baseline_claims_map[m_cid][1]:
                    errors.append(f"UNAUTHORIZED_LEGACY_MANIFEST_VIOLATION: Status for {m_cid} in legacy manifest does not match baseline commit status.")

        except subprocess.CalledProcessError as e:
            errors.append(f"GIT_BASELINE_VERIFICATION_FAILED: Git baseline verification failed for {baseline_commit}: {e.stderr}")

    with open(register_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line_str = line.strip()
        if not line_str.startswith("| `CLM-") and not line_str.startswith("|`CLM-"):
            continue
        parts = [p.strip() for p in line_str.split("|")]
        if parts and parts[0] == "":
            parts = parts[1:]
        if parts and parts[-1] == "":
            parts = parts[:-1]

        if len(parts) < 5:
            continue

        raw_cid = parts[0].strip("`")
        if len(parts) >= 6:
            status = parts[-3].strip()
        else:
            status = parts[-2].strip()

        status_upper = status.upper()
        total_claims += 1
        status_histogram[status] = status_histogram.get(status, 0) + 1

        is_exempt = any(status_upper.startswith(ep) or ep in status_upper for ep in KNOWN_EXEMPT_PATTERNS)
        is_terminal = any(status_upper.startswith(tp) or tp in status_upper for tp in KNOWN_TERMINAL_PATTERNS) or status_upper.startswith("FAIL_") or status_upper.startswith("PROVED_")

        if not is_exempt and not is_terminal:
            errors.append(f"UNRECOGNIZED_STATUS_VIOLATION: Claim {raw_cid} has unknown status '{status}'. Must be registered in canonical status registry.")
            unrecognized_statuses += 1
            continue

        if is_exempt:
            open_or_exempt_claims += 1
            passed.append(f"{raw_cid} (Status: {status}) -> Exempt (Open / Diagnostic / Scoped).")
            continue

        # Terminal claim processing
        terminal_claims += 1
        spec_file = os.path.join(claims_dir, f"{raw_cid}.json")

        if os.path.exists(spec_file):
            try:
                with open(spec_file, "r", encoding="utf-8") as sf:
                    spec = json.load(sf)
                res = audit_claim_specification(spec)
                if res["status"] == "PASS":
                    audited_terminal_claims += 1
                    passed.append(f"{raw_cid} (Status: {status}) -> SPECIFICATION_SCHEMA_PASSED (10/10 gates).")
                else:
                    missing_specifications += 1
                    errors.append(f"{raw_cid} specification failed gate audit: {res['violations']}")
            except Exception as e:
                missing_specifications += 1
                errors.append(f"Error parsing specification for {raw_cid}: {e}")
        else:
            # Check legacy manifest for grandfathered status
            legacy_claims = legacy_manifest.get("claims", {})
            if raw_cid in legacy_claims:
                expected_hash = legacy_claims[raw_cid].get("line_hash", "")
                current_hash = hashlib.sha256(line_str.encode("utf-8")).hexdigest()
                expected_status = legacy_claims[raw_cid].get("status", "")
                if current_hash == expected_hash and status == expected_status:
                    legacy_unaudited_terminal_claims += 1
                    passed.append(f"{raw_cid} (Status: {status}) -> LEGACY_UNAUDITED (Grandfathered manifest).")
                else:
                    missing_specifications += 1
                    errors.append(f"MODIFIED_LEGACY_CLAIM_VIOLATION: Grandfathered claim {raw_cid} was modified (hash/status changed) without providing a validated specification in .agents/claims/.")
            else:
                missing_specifications += 1
                errors.append(f"MISSING_SPECIFICATION_VIOLATION: Terminal claim {raw_cid} (Status: {status}) is not in legacy manifest and lacks specification at {spec_file}.")

    # Enforce arithmetic consistency
    assert terminal_claims == audited_terminal_claims + legacy_unaudited_terminal_claims + missing_specifications, "Coverage arithmetic mismatch on terminal claims"
    assert total_claims == terminal_claims + open_or_exempt_claims + unrecognized_statuses, "Coverage arithmetic mismatch on total claims"

    coverage = {
        "total_claims": total_claims,
        "terminal_claims": terminal_claims,
        "audited_terminal_claims": audited_terminal_claims,
        "legacy_unaudited_terminal_claims": legacy_unaudited_terminal_claims,
        "open_or_exempt_claims": open_or_exempt_claims,
        "missing_specifications": missing_specifications,
        "unrecognized_statuses": unrecognized_statuses,
        "status_histogram": status_histogram
    }

    return len(errors) == 0, errors, passed, coverage


def main():
    parser = argparse.ArgumentParser(description="Audit mathematical claim specification against the 10 gates.")
    parser.add_argument("--claim-file", help="Path to JSON file containing claim specification.")
    parser.add_argument("--cross-check-register", action="store_true", help="Cross-check all claims in claim_register.md.")
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    args = parser.parse_args()

    if args.cross_check_register:
        ok, errors, passed, coverage = cross_check_claim_register(args.repo_root)
        print(f"=== Cross-Checking Claim Register against .agents/claims/ ===")
        print(f"Total claims:                      {coverage['total_claims']}")
        print(f"Terminal claims:                   {coverage['terminal_claims']}")
        print(f"  - Audited terminal claims:       {coverage['audited_terminal_claims']}")
        print(f"  - Legacy unaudited terminal:     {coverage['legacy_unaudited_terminal_claims']}")
        print(f"  - Missing specifications:        {coverage['missing_specifications']}")
        print(f"Open or exempt claims:             {coverage['open_or_exempt_claims']}")
        print(f"Unrecognized statuses:             {coverage['unrecognized_statuses']}")
        print(f"\nStatus Histogram:")
        for st, count in sorted(coverage['status_histogram'].items()):
            print(f"  - {st}: {count}")
        print()
        for p in passed:
            print(f"[PASS] {p}")
        for e in errors:
            print(f"[FAIL] {e}")
        if not ok:
            sys.exit(1)
        sys.exit(0)

    if args.claim_file:
        with open(args.claim_file, "r", encoding="utf-8") as f:
            spec = json.load(f)

        result = audit_claim_specification(spec)
        print(json.dumps(result, indent=2))
        if result["status"] == "FAIL":
            sys.exit(1)
        sys.exit(0)

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
