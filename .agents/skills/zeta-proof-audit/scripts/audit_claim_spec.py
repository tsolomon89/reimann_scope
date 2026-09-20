"""audit_claim_spec.py — Executable Specification & Gate Validator for Mathematical Claims.

Enforces the 19-field claim schema and the 10 mandatory pre-acceptance gates
defined in the `zeta-proof-audit` skill.
"""

import sys
import os
import glob
import json
import re
import hashlib
import subprocess
import argparse
from typing import Dict, Any, List, Set, Tuple, Optional

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
    # Set missing evidence fields explicitly to UNKNOWN so missing information is exposed, never manufactured
    if "evidence_scope" not in normalized:
        normalized["evidence_scope"] = "UNKNOWN"
    if "exact_or_truncated" not in normalized:
        normalized["exact_or_truncated"] = "UNKNOWN"
    if "arithmetic_cutoff" not in normalized:
        normalized["arithmetic_cutoff"] = "UNKNOWN"
    if "spectral_cutoff" not in normalized:
        normalized["spectral_cutoff"] = "UNKNOWN"
    if "integration_domain" not in normalized:
        normalized["integration_domain"] = "UNKNOWN"
    if "omitted_tail" not in normalized:
        normalized["omitted_tail"] = "UNKNOWN"
    if "tail_enclosure" not in normalized:
        normalized["tail_enclosure"] = "UNKNOWN"
    return normalized


def audit_claim_specification(raw_spec: Dict[str, Any], repo_root: Optional[str] = None) -> Dict[str, Any]:
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
        val = spec.get(field)
        if field not in spec or val is None:
            violations.append(f"Missing mandatory field: '{field}'")
        elif val == "UNKNOWN":
            violations.append(f"Gate 10 [Evidence Classification] VIOLATION: Mandatory field '{field}' has unspecified value 'UNKNOWN'. Missing evidence cannot be manufactured.")
        elif field in STRICT_NON_EMPTY_FIELDS:
            if isinstance(val, (str, list, dict)) and len(val) == 0:
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
    fake_boundary_phrases = [
        "no boundary", "boundary not checked", "boundary omitted",
        "without boundary check", "without boundary audit", "without boundary analysis",
        "not investigated", "none (only sampled", "boundary audit pending", "no asymptotic",
        "boundary check not"
    ]
    is_fake_boundary = any(fp in fals_str for fp in fake_boundary_phrases)

    boundary_substance_terms = [
        "->", "\\to", "asymptotic", "dominance", "dominates", "limit",
        "expansion", "growth", "o(", "o(1)", "infinity", "\\infty",
        "boundary asymptotic", "extreme aspect", "power", "decay", "residue",
        "boundary limit", "endpoint", "tail", "envelope", ">=", "<=", "divergence"
    ]
    has_substantive_boundary = (not is_fake_boundary) and any(bt in fals_str for bt in boundary_substance_terms) and any(k in fals_str for k in ["boundary", "asymptotic", "limit", "dominance", "tail", "extreme"])

    needs_boundary = ("\\to" in stmt or "\\infty" in stmt or "limit" in stmt or "asymptotic" in stmt or
                      "domain" in stmt or "r" in int_domain.lower() or "[0," in str(spec.get("variable_domains", "")).lower() or
                      "\\forall" in stmt or "for all" in stmt or "order_of_limits" in spec)

    if is_fake_boundary:
        violations.append("Gate 5 [Dominance & Boundary] VIOLATION: Explicitly disclaimed or fake boundary check recorded.")
    elif not has_substantive_boundary:
        warnings.append("Gate 5 [Dominance & Boundary] WARNING: No explicit substantive boundary/asymptotic dominance audit recorded.")
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
                           "four blocks" in fals_str or "4-block" in fals_str or
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

    # Check 8C: Require substantive independent derivation or external literature verification
    has_external_literature = bool(spec.get("external_sources")) and any(
        (isinstance(s, dict) and s.get("source") and (s.get("theorem") or s.get("chapter") or s.get("page") or s.get("section"))) or
        (isinstance(s, str) and len(s) > 10 and any(k in s.lower() for k in ["theorem", "1859", "1914", "1936", "1974", "1986", "edwards", "titchmarsh", "hardy", "riemann"]))
        for s in spec.get("external_sources", [])
    )
    has_dual_derivation = (
        bool(proof_art and not proof_art.lower().startswith("none")) and
        bool(spec.get("computational_evidence")) and
        any(k in proof_art.lower() for k in ["sympy", "lean", "exact", "mathlib", "curvaturetransport.lean", "grade.lean"])
    )
    cid = str(spec.get("claim_id", "")).strip()
    review_path = os.path.join(repo_root or ".", ".agents", "claims", "reviews", f"{cid}-derivation-review.md")
    has_review_artifact = os.path.exists(review_path)

    if not (has_external_literature or has_dual_derivation or has_review_artifact):
        violations.append(
            "Gate 8 [Independent Derivation] VIOLATION: Claim lacks independent external verification "
            "(external peer-reviewed literature with citation/theorem), dual derivation paths (symbolic + verified computation), "
            "or an independent derivation review artifact in .agents/claims/reviews/."
        )
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

    # Check 10D: Dependency Graph Semantic Validity (Transitive Resolution & Cycle Detection)
    graph_violations = validate_dependency_graph(spec, repo_root=repo_root)
    violations.extend(graph_violations)

    if not any("Gate 10" in v for v in violations):
        passed_gates.append("Gate 10: Evidence Classification Audit")

    status = "FAIL" if violations else "PASS"
    schema_status = "FAIL" if any("Missing mandatory field" in v or "Empty mandatory field" in v or "UNKNOWN" in v for v in violations) else "PASS"

    cid = str(spec.get("claim_id", "")).strip()
    review_ok, review_msg, review_details = verify_independent_review(cid, spec, repo_root=repo_root)

    if status == "PASS" and review_ok:
        math_review_status = "INDEPENDENT_MATHEMATICAL_AUDIT_PASSED"
    elif status == "PASS":
        math_review_status = "AWAITING_INDEPENDENT_REVIEW"
    else:
        math_review_status = "FAIL"

    return {
        "status": status,
        "schema_validation": schema_status,
        "mathematical_review_status": math_review_status,
        "claim_id": spec.get("claim_id"),
        "passed_gates": passed_gates,
        "violations": violations,
        "warnings": warnings,
        "independent_review": review_details,
        "review_message": review_msg,
        "gate_summary": f"Passed {len(passed_gates)}/10 gates with {len(violations)} violations and {len(warnings)} warnings."
    }


DEFAULT_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))


def _git_commit_exists(commit_sha: str, root_dir: Optional[str] = None) -> bool:
    """Verifies whether a commit SHA actually exists in the git repository."""
    if not commit_sha or str(commit_sha).lower() == "unknown":
        return False
    candidate_roots = [d for d in [root_dir, DEFAULT_REPO_ROOT] if d and os.path.exists(d)]
    for candidate in candidate_roots:
        try:
            res = subprocess.run(
                ["git", "rev-parse", "--verify", "--quiet", f"{commit_sha}^{{commit}}"],
                cwd=candidate,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            if res.returncode == 0:
                return True
            if "not a git repository" not in res.stderr.lower():
                return False
        except Exception:
            continue
    return False

SUBSTANTIVE_SPEC_KEYS = [
    "claim_id",
    "statement",
    "mathematical_statement",
    "quantified_variables",
    "quantifiers",
    "variable_domains",
    "hypotheses",
    "object_studied",
    "mathematical_object",
    "fourier_normalization",
    "multiplicity_convention",
    "measure_and_window",
    "order_of_limits",
    "exact_conclusion",
    "logical_negation",
    "epistemic_role",
    "evidence_scope",
    "claimed_scope",
    "evidence_class",
    "exact_or_truncated",
    "arithmetic_cutoff",
    "spectral_cutoff",
    "integration_domain",
    "omitted_tail",
    "tail_enclosure",
    "dependencies",
    "dependency_claim_ids",
    "remaining_analytic_dependencies",
    "open_obligations",
    "external_analytic_obligations",
    "source_file",
    "source_reference",
    "verification_commands",
    "verification_command",
    "external_sources",
    "external_references",
    "falsification_attempts",
    "falsification_tests",
    "tolerances",
    "parameters",
    "boundary_cases_analyzed",
    "acceptance_criteria",
]


def compute_claim_substantive_manifest(
    spec: Dict[str, Any],
    repo_root: Optional[str] = None
) -> Tuple[Dict[str, Any], str]:
    """
    Computes a canonical substantive content manifest for a mathematical claim,
    covering the mathematical payload, hypotheses, scope, parameters,
    and cryptographic SHA256 digests of all declared evidence files on disk.

    Separates mutable review/status metadata (status, review_status, git_commit,
    reviewer, author, review_message, etc.) to prevent circular hashing.
    """
    if repo_root is None:
        repo_root = DEFAULT_REPO_ROOT

    substantive_payload: Dict[str, Any] = {}
    for key in SUBSTANTIVE_SPEC_KEYS:
        if key in spec and spec[key] is not None:
            substantive_payload[key] = spec[key]

    evidence_digests: Dict[str, str] = {}

    # Proof artifact
    proof_art = str(spec.get("proof_artifact", "")).strip()
    if proof_art and proof_art.lower() != "none":
        raw_path = proof_art.split()[0].strip()
        abs_proof = os.path.normpath(raw_path) if os.path.isabs(raw_path) else os.path.normpath(os.path.join(repo_root, raw_path))
        if os.path.exists(abs_proof) and os.path.isfile(abs_proof):
            with open(abs_proof, "rb") as pf:
                evidence_digests[raw_path] = hashlib.sha256(pf.read()).hexdigest()
        else:
            evidence_digests[raw_path] = "FILE_MISSING"

    # Computational evidence
    comp_ev = spec.get("computational_evidence", [])
    if isinstance(comp_ev, list):
        for item in comp_ev:
            if isinstance(item, str) and item.strip():
                raw_item = item.strip()
                if ":" in raw_item:
                    if len(raw_item) > 2 and raw_item[1] == ":" and (raw_item[2] in ("\\", "/")):
                        drive = raw_item[:2]
                        rest = raw_item[2:]
                        clean_path = drive + (rest.split(":", 1)[0].strip() if ":" in rest else rest)
                    else:
                        clean_path = raw_item.split(":", 1)[0].strip()
                else:
                    clean_path = raw_item

                if clean_path:
                    abs_ev = os.path.normpath(clean_path) if os.path.isabs(clean_path) else os.path.normpath(os.path.join(repo_root, clean_path))
                    if os.path.exists(abs_ev) and os.path.isfile(abs_ev):
                        with open(abs_ev, "rb") as ef:
                            evidence_digests[clean_path] = hashlib.sha256(ef.read()).hexdigest()
                    else:
                        evidence_digests[clean_path] = "FILE_MISSING"

    # Declared source dependencies (from "dependencies", "source_code_dependencies", "source_dependencies")
    src_deps = spec.get("dependencies", []) + spec.get("source_code_dependencies", []) + spec.get("source_dependencies", [])
    source_dependency_digests: Dict[str, str] = {}
    if isinstance(src_deps, list):
        for item in src_deps:
            if isinstance(item, str) and item.strip():
                raw_item = item.strip()
                clean_path = raw_item.split(":", 1)[0].strip()
                if clean_path and not clean_path.startswith("CLM-") and ("." in os.path.basename(clean_path)):
                    abs_dep = os.path.normpath(clean_path) if os.path.isabs(clean_path) else os.path.normpath(os.path.join(repo_root, clean_path))
                    if os.path.exists(abs_dep) and os.path.isfile(abs_dep):
                        with open(abs_dep, "rb") as df:
                            source_dependency_digests[clean_path] = hashlib.sha256(df.read()).hexdigest()
                    else:
                        source_dependency_digests[clean_path] = "FILE_MISSING"

    manifest = {
        "claim_id": str(spec.get("claim_id", "")).strip(),
        "substantive_payload": substantive_payload,
        "evidence_digests": evidence_digests,
        "source_dependency_digests": source_dependency_digests
    }

    canonical_json = json.dumps(manifest, sort_keys=True, indent=2)
    manifest_sha256 = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
    return manifest, manifest_sha256


def verify_independent_review(
    claim_id: str,
    spec: Dict[str, Any],
    repo_root: Optional[str] = None
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Verifies that a claim has an independent mathematical review artifact in .agents/claims/reviews/.
    Enforces that:
    1. The review artifact exists at .agents/claims/reviews/<claim_id>-derivation-review.md.
    2. The review is independent: rejects author self-review (author matching reviewer,
       review declaring itself as author self-review, or self-certification).
    3. The review contains required substantive sections:
       - Derivation / proof evaluation with substantive analytical content.
       - Objections / adversarial challenges / falsification attempts.
       - Clear resolution / verdict.
    4. The review verdict MUST be evaluated:
       - Explicitly rejects negative verdicts and refusals (REJECTED, FAILED, DISAPPROVED, INVALID,
         UNSOUND, FATAL CIRCULARITY, INCORRECT, UNRESOLVED, CONTRADICTED, DO NOT ACCEPT, NOT ACCEPTED).
       - Requires a structured positive approval verdict (PASSED, APPROVED, ACCEPTED,
         VERIFIED, CONFIRMED, PROVED, FORMALIZED, VALID, CERTIFIED).
    5. Content-Manifest Binding:
       - Review MUST be explicitly bound to the recomputed SHA256 of the substantive content manifest.
       - Any change in claim statement, hypotheses, parameters, evidence, or declared source dependencies invalidates the review.
       - Missing evidence files on disk strictly fail validation.
       - Declared commit SHAs must exist in git; stale review commits are rejected.
    """
    if not claim_id or claim_id == "UNKNOWN":
        return False, "No claim ID specified", {}

    if repo_root is None:
        repo_root = DEFAULT_REPO_ROOT

    reviews_dir = os.path.join(repo_root, ".agents", "claims", "reviews")
    review_file = os.path.join(reviews_dir, f"{claim_id}-derivation-review.md")

    if not os.path.exists(review_file):
        return False, f"Missing independent review artifact at '{review_file}'", {}

    try:
        with open(review_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read review artifact: {e}", {}

    content_lower = content.lower()

    # 1. Explicit negative verdict / fatal circularity / refusal / unresolved objection detection
    negative_patterns = [
        r'\b(?:resolution|verdict|status|conclusion|assigned classification)\s*[:*`]+\s*(?:`?(?:REJECTED|FAILED|DISAPPROVED|INVALID|UNRESOLVED|CONTRADICTED|FATAL|UNSOUND|PENDING|NOT APPROVED|NOT PASSED|UNAPPROVED|INCONCLUSIVE|OPEN|DO NOT ACCEPT|NOT ACCEPTED|REFUSED)\b)',
        r'\b(?:verdict|resolution|status)\s*[:*`]+\s*[^\n\r]*\b(?:not approved|not passed|unapproved|rejected|failed|pending|inconclusive|unresolved|do not accept|not accepted|refused)\b',
        r'\bderivation\s*[:*`]+\s*(?:`?(?:INCORRECT|FALSE|UNSOUND|INVALID|FATAL|INCOMPLETE|PENDING)\b)',
        r'\bobjections?\s*[:*`]+\s*(?:`?(?:FATAL|UNRESOLVED|UNANSWERED|BLOCKING|FATAL CIRCULARITY|NOT EVALUATED)\b)',
        r'\b(?:blocking\s+objection|unresolved\s+objection)\b',
        r'\b(?:objections?|challenges?)\s*[:*`]+\s*(?:(?!\b(?:no|none|not|zero|without)\b)[^\n\r])*\b(?:unresolved|blocking|open|fatal)\b',
        r'\[\s*unresolved\s*\]',
        r'\[\s*blocking\s*\]',
        r'\bdo not accept\b',
        r'\bnot accepted\b',
        r'\bdo not approve\b'
    ]
    for pat in negative_patterns:
        neg_m = re.search(pat, content, re.IGNORECASE)
        if neg_m:
            return False, f"Review artifact recorded negative verdict or fatal objection: '{neg_m.group(0).strip()}'", {}

    # Check explicit structured verdict/resolution line for refusal phrases
    m_verdict = re.search(r'(?:##\s*[^#\n\r]*\b(?:verdict|resolution)\b[^\n\r]*\n+|\b(?:verdict|resolution|conclusion)\s*[:*`]+\s*)([^\n\r]+)', content, re.IGNORECASE)
    if m_verdict:
        v_clause = m_verdict.group(1).strip()
        verdict_refusal_patterns = [
            r'\bdo\s+not\s+accept\b',
            r'\bnot\s+accepted\b',
            r'\bcannot\s+accept\b',
            r'\bdo\s+not\s+approve\b',
            r'\bnot\s+approved\b',
            r'\bdisapproved?\b',
            r'\brejected?\b',
            r'\brefused?\b',
            r'\brefusal\b',
            r'\bfailed\b',
            r'\bdo\s+not\s+pass\b',
            r'\bnot\s+passed\b',
            r'\bunapproved\b',
            r'\bnot\s+verified\b',
            r'\bunverified\b',
            r'\bnot\s+proved\b',
            r'\bunproved\b',
            r'\bnot\s+confirmed\b',
            r'\bunconfirmed\b',
            r'\bnot\s+formalized\b',
            r'\bunformalized\b',
            r'\bnot\s+certified\b',
            r'\buncertified\b',
            r'\binvalid\b',
            r'\bunsound\b'
        ]
        if any(re.search(pat, v_clause, re.IGNORECASE) for pat in verdict_refusal_patterns):
            return False, f"Review artifact recorded explicit refusal or negative verdict: '{m_verdict.group(0).strip()}'", {}

        # Detect negated approval in the verdict clause (e.g. 'not verified', 'fails to be proved')
        neg_m = re.search(r'\b(?:not|never|fails?\s+to\s+be|cannot\s+be|non)\s+([a-z]+)', v_clause, re.IGNORECASE)
        if neg_m:
            w_after = neg_m.group(1).lower()
            if any(w in w_after for w in ["passed", "approved", "accepted", "verified", "confirmed", "proved", "formalized", "valid", "certified"]):
                return False, f"Review artifact recorded negated approval: '{m_verdict.group(0).strip()}'", {}

    # Check for substantive sections (reject placeholder / pending content)
    m_deriv = re.search(r'(?:##\s*[^#\n\r]*derivation[^\n\r]*|\bderivation\s*[:*`]+)\s*([^\n\r]+)', content, re.IGNORECASE)
    if m_deriv:
        d_val = m_deriv.group(1).strip().lower()
        if d_val in ["pending.", "pending", "none.", "none", "not evaluated.", "not evaluated", "tbd", "unverified"]:
            return False, f"Review derivation section is non-substantive: '{m_deriv.group(1).strip()}'", {}

    m_obj = re.search(r'(?:##\s*[^#\n\r]*objection[^\n\r]*|\bobjections?\s*[:*`]+)\s*([^\n\r]+)', content, re.IGNORECASE)
    if m_obj:
        o_val = m_obj.group(1).strip().lower()
        if o_val in ["not evaluated.", "not evaluated", "none.", "none", "pending.", "pending", "tbd"]:
            return False, f"Review objections section is non-substantive: '{m_obj.group(1).strip()}'", {}

    # 2. Author self-review / self-certification detection
    author = str(spec.get("author", "")).strip().lower()
    producer = str(spec.get("producer", "")).strip().lower()
    owner = str(spec.get("owner", "")).strip().lower()

    rev_m = re.search(r'(?:reviewer|auditor|reviewed by|evaluator)\s*(?:role)?\s*[:*`]+\s*([^\n\r*`]+)', content, re.IGNORECASE)
    reviewer_text = rev_m.group(1).strip().lower() if rev_m else ""
    auth_m = re.search(r'(?:claim author|author|producer|owner)\s*[:*`]+\s*([^\n\r*`]+)', content, re.IGNORECASE)
    author_text = auth_m.group(1).strip().lower() if auth_m else ""

    if not reviewer_text or reviewer_text in ["none", "pending", "not evaluated", "unknown", "n/a", "tbd"]:
        return False, "Review artifact lacks explicit reviewer identity / role", {}

    if reviewer_text:
        if author and (author in reviewer_text or reviewer_text in author):
            return False, f"Self-review detected: claim author '{spec.get('author')}' matches reviewer '{rev_m.group(1).strip()}'", {}
        if producer and (producer in reviewer_text or reviewer_text in producer):
            return False, f"Self-review detected: claim producer '{spec.get('producer')}' matches reviewer '{rev_m.group(1).strip()}'", {}
        if owner and (owner in reviewer_text or reviewer_text in owner):
            return False, f"Self-review detected: claim owner '{spec.get('owner')}' matches reviewer '{rev_m.group(1).strip()}'", {}
        if author_text and (author_text in reviewer_text or reviewer_text in author_text):
            return False, f"Self-review detected: review author '{auth_m.group(1).strip()}' matches reviewer '{rev_m.group(1).strip()}'", {}

    if any(k in content_lower for k in ["self-review", "self review", "self-certification", "self certification", "author review"]):
        return False, "Self-certification detected: review must be independent", {}

    # 3. Check for required substantive sections
    has_derivation = any(k in content_lower for k in ["derivation", "proof", "analytical", "symbolic", "mathematical"])
    has_objections = any(k in content_lower for k in ["objection", "adversarial", "challenge", "falsification", "counterexample", "zero-crossing", "barrier", "obstruction", "rigidity"])
    has_resolution = any(k in content_lower for k in ["resolution", "conclusion", "verified", "status", "proved", "confirmed", "formalized", "verdict", "assigned classification"])

    if not has_derivation:
        return False, "Review artifact lacks derivation / proof evaluation section", {}
    if not has_objections:
        return False, "Review artifact lacks objections / adversarial challenge / falsification section", {}
    if not has_resolution:
        return False, "Review artifact lacks clear resolution / conclusion section", {}

    # 4. Require explicit positive approval verdict
    if m_verdict:
        v_clause = m_verdict.group(1).strip().lower()
        has_approval_word = any(w in v_clause for w in ["passed", "approved", "accepted", "verified", "confirmed", "formally proved", "proved", "formalized", "valid", "certified"])
        if not has_approval_word:
            return False, f"Review artifact verdict line lacks explicit positive approval: '{m_verdict.group(0).strip()}'", {}
    else:
        positive_patterns = [
            r'\b(?:resolution|verdict|conclusion)\s*[:*`]+\s*[^\n\r]*\b(?<!not\s)(?<!un)(?:passed|approved|accepted|verified|confirmed|formally proved|proved|formalized|valid)\b',
            r'##\s*[^#\n\r]*\b(?:verdict|resolution|formalization)\b[^\n\r]*\n+[^\n\r]*\b(?<!not\s)(?<!un)(?:passed|approved|accepted|verified|confirmed|formally proved|proved|formalized|valid)\b',
            r'\bthe claim is verified\b',
            r'\bformally proved in lean\b',
            r'\bformalized\b',
            r'\bverified successfully\b',
            r'\b\*\*PASSED\*\*\b'
        ]
        if not any(re.search(p, content, re.IGNORECASE) for p in positive_patterns):
            return False, "Review artifact lacks explicit positive approval verdict (e.g. PASSED, APPROVED, ACCEPTED, VERIFIED)", {}

    # 5. Commit verification: verify commits exist if declared
    m_commit = re.search(r'(?:target commit|commit sha|commit|sha|start sha)\s*[:*`]+\s*([0-9a-fA-F]{7,40})', content, re.IGNORECASE)
    rev_commit = m_commit.group(1).lower() if m_commit else ""
    spec_commit = str(spec.get("git_commit", "")).strip().lower() if spec else ""

    if rev_commit and spec_commit and spec_commit != "unknown":
        if not (rev_commit.startswith(spec_commit) or spec_commit.startswith(rev_commit)):
            return False, f"Stale review detected: review commit '{rev_commit}' does not match claim specification commit '{spec_commit}'", {}

    if rev_commit:
        if not _git_commit_exists(rev_commit, repo_root):
            return False, f"Nonexistent commit '{rev_commit}': declared review commit does not exist in git repository", {}

    if spec_commit and spec_commit != "unknown":
        if not _git_commit_exists(spec_commit, repo_root):
            return False, f"Nonexistent commit '{spec_commit}': declared claim specification git_commit does not exist in git repository", {}

    # 6. Canonical Content Manifest Binding
    manifest, actual_manifest_sha = compute_claim_substantive_manifest(spec, repo_root)

    # Check for missing evidence files on disk
    missing_ev = [f for f, h in manifest.get("evidence_digests", {}).items() if h == "FILE_MISSING"]
    if missing_ev:
        return False, f"Declared evidence file(s) missing on disk: {', '.join(missing_ev)}", {}

    # Extract declared reviewed manifest SHA256 from the review artifact
    m_manifest = re.search(
        r'(?:reviewed-manifest-sha256|reviewed manifest digest|manifest sha256|substantive manifest digest|manifest digest|claim hash|spec hash)\s*[:*`]+\s*(?:sha256:)?([0-9a-fA-F]{64})',
        content,
        re.IGNORECASE
    )

    if not m_manifest:
        return False, (
            "Review artifact is not bound to canonical substantive content manifest. "
            "Requires explicit 'Reviewed-Manifest-SHA256: <64-hex>' binding matching recomputed substantive manifest."
        ), {}

    declared_manifest_sha = m_manifest.group(1).lower()
    if declared_manifest_sha != actual_manifest_sha.lower():
        return False, (
            f"Wrong claim hash / substantive manifest digest mismatch: review specifies '{declared_manifest_sha}' "
            f"but current recomputed substantive manifest digest is '{actual_manifest_sha}' "
            f"(substantive claim fields or declared evidence files have been modified or deleted)."
        ), {}

    details = {
        "review_file": review_file,
        "manifest_sha256": actual_manifest_sha,
        "is_manifest_bound": True,
        "has_objections": has_objections,
        "has_derivation": has_derivation,
        "has_resolution": has_resolution,
        "reviewer_text": reviewer_text,
        "author_text": author_text
    }
    return True, "Independent review verified successfully", details


def resolve_dependency_claim(dep_id: str, repo_root: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Resolves a claim ID to its JSON specification dict or register metadata."""
    if repo_root is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.abspath(os.path.join(current_dir, "..", "..", "..", ".."))

    claims_dir = os.path.join(repo_root, ".agents", "claims")
    json_path = os.path.join(claims_dir, f"{dep_id}.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    reg_path = os.path.join(repo_root, ".agents", "corpus_map", "claim_register.md")
    if os.path.exists(reg_path):
        try:
            with open(reg_path, "r", encoding="utf-8") as f:
                content = f.read()
            m = re.search(r'\|\s*`' + re.escape(dep_id) + r'`\s*\|([^|]+)\|([^|]+)\|([^|]+)\|', content)
            if m:
                status = m.group(3).strip()
                return {"claim_id": dep_id, "status": status, "is_from_register": True}
        except Exception:
            pass
    return None


def is_non_terminal_claim(claim_info: Dict[str, Any]) -> Tuple[bool, str]:
    """Determines whether a resolved claim info is non-terminal / open / pending."""
    role = str(claim_info.get("epistemic_role", "")).strip()
    scope = str(claim_info.get("evidence_scope", "")).strip()
    status = str(claim_info.get("status", "")).strip()
    conc = str(claim_info.get("exact_conclusion", "")).strip()
    stmt = str(claim_info.get("statement", "")).strip()

    if role in {"OPEN_OBLIGATION", "NUMERICAL_OBSERVATION", "CONJECTURE", "HEURISTIC"}:
        return True, f"epistemic role '{role}'"
    if scope in {"FINITE_NUMERICAL_SAMPLE", "CONDITIONAL_THEOREM"}:
        return True, f"evidence scope '{scope}'"

    for pat in ["PENDING", "OPEN", "CONJECTURE", "UNPROVED", "POSITIVE_NUMERICAL_EVIDENCE", "NUMERICAL_OBSERVATION"]:
        if pat in status.upper():
            return True, f"status '{status}' contains '{pat}'"
    return False, "terminal"


def validate_dependency_graph(spec: Dict[str, Any], repo_root: Optional[str] = None) -> List[str]:
    """
    Traverses dependency claim IDs, resolves them against repository specs/register,
    detects cycles, and rejects terminal claims depending on non-terminal claims.
    """
    violations: List[str] = []
    root_id = str(spec.get("claim_id", "UNKNOWN")).strip()
    role = str(spec.get("epistemic_role", "")).strip()
    conc = str(spec.get("exact_conclusion", "")).lower()

    is_terminal_role = role in {"NO_GO_COMPONENT", "LOAD_BEARING_ANALYTIC_THEOREM", "ALGEBRAIC_IDENTITY"}
    ev_scope = str(spec.get("evidence_scope", "")).strip()
    is_terminal_scope = ev_scope in {"CERTIFIED_POINT_WITNESS", "CERTIFIED_COMPACT_DOMAIN"}
    is_terminal_assertion = ("closed" in conc or "proved" in conc or "falsified" in conc) and not ("open" in conc or "pending" in conc)
    is_root_terminal = is_terminal_role or is_terminal_scope or is_terminal_assertion

    # 1. Textual dependency check for explicit non-terminal qualifiers
    if is_root_terminal:
        for dep in spec.get("dependencies", []):
            dep_str = str(dep).lower()
            if "pending" in dep_str or "unproved" in dep_str or "open" in dep_str:
                violations.append(
                    f"Gate 10 [Dependency Semantic Validity] VIOLATION: Claim asserts terminal closure/proof, "
                    f"but depends on pending premise '{dep}'."
                )

    # 2. Extract dependency IDs from explicit field or dependency text
    dep_ids: List[str] = list(spec.get("dependency_claim_ids", []))
    if not dep_ids:
        for dep in spec.get("dependencies", []):
            matches = re.findall(r'\b(CLM-[A-Z0-9\-]+)\b', str(dep))
            for m in matches:
                if m != root_id and m not in dep_ids:
                    dep_ids.append(m)

    def dfs(current_id: str, current_spec: Dict[str, Any], path: List[str], visited_in_path: Set[str]):
        next_deps: List[str] = list(current_spec.get("dependency_claim_ids", []))
        if not next_deps:
            for dep in current_spec.get("dependencies", []):
                matches = re.findall(r'\b(CLM-[A-Z0-9\-]+)\b', str(dep))
                for m in matches:
                    if m != current_id and m not in next_deps:
                        next_deps.append(m)

        for dep_id in next_deps:
            if dep_id in visited_in_path:
                cycle_str = " -> ".join(path + [dep_id])
                violations.append(f"Gate 10 [Dependency Cycle] VIOLATION: Dependency cycle detected in claim graph: {cycle_str}")
                continue

            dep_info = resolve_dependency_claim(dep_id, repo_root)
            if dep_info is None:
                violations.append(f"Gate 10 [Dependency Resolution] VIOLATION: Dependency claim ID '{dep_id}' referenced by '{current_id}' could not be resolved.")
                continue

            is_non_term, reason = is_non_terminal_claim(dep_info)
            if is_root_terminal and is_non_term:
                path_str = " -> ".join(path + [dep_id])
                violations.append(
                    f"Gate 10 [Dependency Semantic Validity] VIOLATION: Terminal claim '{root_id}' "
                    f"depends on non-terminal claim '{dep_id}' ({reason}) via path {path_str}."
                )

            dfs(dep_id, dep_info, path + [dep_id], visited_in_path | {dep_id})

    dfs(root_id, spec, [root_id], {root_id})
    return violations


# Complete registry of recognized status patterns in the repository
ALLOWED_STATUSES = {
    "PROVED / EXACT",
    "PROVED / FORMALLY_PROVED",
    "PROVED / THEORETICAL_IDENTITY",
    "PROVED / ASYMPTOTIC_THEOREM",
    "PROVED / PROVED_UNDER_HYPOTHESIS",
    "PROVED / EMPIRICAL_EXACT_MATCH",
    "RETAINED (EMPIRICAL 80-DPS) / NUMERICAL_VALIDATION",
    "PROVED / ANALYTIC_APPROXIMATION",
    "PROVED / ASYMPTOTIC_BOUND",
    "DIAGONAL_CROSS_TERM_HAS_EXACT_CANCELLING_VARIANCES",
    "FULL_WINDOWED_ZETA_CROSS_TERM_DERIVED",
    "KNOWN_RH_EQUIVALENCE",
    "INTERNALLY_REDERIVED",
    "PROVED SPECTRAL EQUIVALENCE",
    "OPEN / CONJECTURED (RH)",
    "OPEN / FORMALIZATION_PENDING",
    "DISPROVED / FALSIFIED",
    "SPECIFICATION_SCHEMA_PASSED",
    "INDEPENDENT_MATHEMATICAL_AUDIT_PASSED",
    "EXTERNAL_ANALYTIC_PROOF",
    "FIXED_GAUSSIAN_COMMON_FRAME_CROSS_TERM_NONZERO",
    "FIXED_GAUSSIAN_COMMON_FRAME_CROSS_TERM_POSITIVE_NUMERICAL_EVIDENCE",
    "CERTIFIED_POINT_WITNESS_PENDING",
    "CERTIFIED_POINT_WITNESS",
    "CERTIFIED_COMPACT_DOMAIN",
    "BILATERAL_GRADE_ROUTE_CLASS_CLOSURE_OPEN",
    "FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_OPEN",
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
    "CERTIFIED_POINT_WITNESS",
    "CERTIFIED_COMPACT_DOMAIN",
    "FIXED_GAUSSIAN_COMMON_FRAME_CROSS_TERM_NONZERO",
    "FIXED_GAUSSIAN_COMMON_FRAME_CROSS_TERM_POSITIVE_NUMERICAL_EVIDENCE",
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
    "CERTIFIED_POINT_WITNESS_PENDING",
    "BILATERAL_GRADE_ROUTE_CLASS_CLOSURE_OPEN",
    "FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_OPEN",
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
                res = audit_claim_specification(spec, repo_root=repo_root)
                if res["status"] == "PASS":
                    audited_terminal_claims += 1
                    passed.append(f"{raw_cid} (Status: {status}) -> SPECIFICATION_SCHEMA_PASSED (10/10 gates).")
                    if "INDEPENDENT_MATHEMATICAL_AUDIT_PASSED" in status_upper and res["mathematical_review_status"] != "INDEPENDENT_MATHEMATICAL_AUDIT_PASSED":
                        errors.append(f"UNVERIFIED_MATHEMATICAL_AUDIT_VIOLATION: Claim {raw_cid} asserts INDEPENDENT_MATHEMATICAL_AUDIT_PASSED, but independent review failed: {res.get('review_message')}")
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
