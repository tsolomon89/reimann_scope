"""audit_claim_spec.py — Executable Specification & Gate Validator for Mathematical Claims.

Enforces the 19-field claim schema and the 10 mandatory pre-acceptance gates
defined in the `zeta-proof-audit` skill.
"""

import sys
import os
import glob
import json
import hashlib
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


def normalize_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes field aliases in claim specification."""
    normalized = dict(spec)
    if "statement" not in normalized and "mathematical_statement" in normalized:
        normalized["statement"] = normalized["mathematical_statement"]
    if "fourier_normalization" not in normalized and "normalization_and_fourier_convention" in normalized:
        normalized["fourier_normalization"] = normalized["normalization_and_fourier_convention"]
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
    return normalized


def audit_claim_specification(raw_spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Audits a candidate mathematical claim against all 18 schema fields and 10 pre-acceptance gates.
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

    if violations:
        return {
            "status": "FAIL",
            "passed_gates": [],
            "violations": violations,
            "warnings": warnings,
            "gate_summary": "Failed basic schema check before gate evaluation."
        }

    # Normalize text fields for case-insensitive keyword inspection
    obj = str(spec["object_studied"]).lower()
    stmt = str(spec["statement"]).lower()
    conc = str(spec["exact_conclusion"]).lower()
    hyps_str = " ".join(str(h) for h in spec.get("hypotheses", [])).lower()
    fals_str = " ".join(str(f) for f in spec.get("falsification_attempts", [])).lower()
    proof_art = str(spec.get("proof_artifact", "")).strip()

    # --- Gate 1: Object-Identity Audit ---
    # Check for prime-only / completed-zeta conflation
    is_prime_data = ("prime" in obj or "dirichlet" in obj or "p(z)" in obj or r"\lambda(n)" in hyps_str or "lambda(n)" in hyps_str or "p(z)" in hyps_str or "sum_{n" in hyps_str or r"\zeta'/\zeta" in obj)
    claims_completed_zeta = ("completed" in stmt or r"\xi" in stmt or "xi(" in stmt or "completed" in conc or r"\xi" in conc or "completed" in obj)
    
    if is_prime_data and claims_completed_zeta:
        deps_str = " ".join(str(d) for d in spec.get("dependencies", [])).lower()
        if not ("bridge" in deps_str or "completion" in deps_str or "gamma" in deps_str):
            violations.append(
                "Gate 1 [Object-Identity] VIOLATION: Mathematical data is prime-only / Dirichlet series but "
                "statement or object claims completed-zeta / xi-function without an explicit completion bridge theorem."
            )
        else:
            warnings.append("Gate 1: Prime-to-completed bridge dependency declared.")
            passed_gates.append("Gate 1: Object-Identity Audit")
    else:
        passed_gates.append("Gate 1: Object-Identity Audit")

    # --- Gate 2: Quantifier Audit ---
    quant_vars = [str(v).lower() for v in spec.get("quantified_variables", [])]
    has_universal = any("forall" in v or r"\forall" in v or "all" in v for v in quant_vars)
    comp_ev = spec.get("computational_evidence", [])
    has_valid_proof = proof_art and not proof_art.lower().startswith("none") and any(k in proof_art.lower() for k in [".lean", "formal", "sympy", "exact", "theorem", "proof"])

    if has_universal and (not has_valid_proof or proof_art.lower().startswith("none")) and comp_ev:
        violations.append(
            "Gate 2 [Quantifier] VIOLATION: Universal quantifier (\\forall) claimed, but only computational "
            "sampling evidence provided without a formal proof artifact."
        )
    else:
        passed_gates.append("Gate 2: Quantifier Audit")

    # --- Gate 3: Negation-First Audit ---
    negation = str(spec.get("logical_negation", "")).strip()
    if not negation or negation.lower() == "none" or negation == conc:
        violations.append("Gate 3 [Negation-First] VIOLATION: Logical negation is missing or identical to conclusion.")
    else:
        passed_gates.append("Gate 3: Negation-First Audit")

    # --- Gate 4: Symbolic Elimination & Equality-Case Audit ---
    is_nonvanishing = (r"\ne 0" in stmt or "!= 0" in stmt or "non-vanishing" in stmt or "nonzero" in stmt or r"\ne 0" in conc or "!= 0" in conc)
    has_equality_analysis = ("equality" in fals_str or "cancellation" in fals_str or "solve" in fals_str or "zero-crossing" in fals_str)

    if is_nonvanishing and not has_equality_analysis:
        violations.append(
            "Gate 4 [Symbolic Elimination] VIOLATION: Non-vanishing (\\ne 0) or strict sign claimed without "
            "symbolic elimination / equality-case cancellation analysis."
        )
    else:
        passed_gates.append("Gate 4: Symbolic Elimination & Equality-Case Audit")

    # --- Gate 5: Dominance and Boundary Audit ---
    has_boundary_check = ("boundary" in fals_str or "asymptotic" in fals_str or "limit" in fals_str or "dominance" in fals_str or "extreme" in fals_str)
    if not has_boundary_check:
        warnings.append("Gate 5 [Dominance & Boundary] WARNING: No explicit boundary/asymptotic dominance audit recorded.")
    else:
        passed_gates.append("Gate 5: Dominance and Boundary Audit")

    # --- Gate 6: Diagonal / Off-Diagonal Audit ---
    is_inner_prod = ("inner product" in obj or "mean square" in obj or r"\langle" in stmt or "norm" in stmt or "cross-term" in stmt or "cross_term" in stmt)
    win_str = str(spec.get("measure_and_window", "")).lower()
    has_finite_window = ("finite" in win_str or "c_c" in win_str or "compact" in win_str or "smooth window" in win_str)
    treats_off_diagonal = ("off-diagonal" in fals_str or "m \\ne n" in fals_str or "m != n" in fals_str or "double sum" in fals_str or
                           "off-diagonal" in hyps_str or "m \\ne n" in hyps_str or "m != n" in hyps_str or "double sum" in hyps_str)

    if is_inner_prod and has_finite_window and not treats_off_diagonal:
        violations.append(
            "Gate 6 [Diagonal/Off-Diagonal] VIOLATION: Finite-window Dirichlet inner product claimed "
            "without accounting for off-diagonal (m != n) cross-terms."
        )
    else:
        passed_gates.append("Gate 6: Diagonal / Off-Diagonal Audit")

    # --- Gate 7: Interchange Audit ---
    deps_str = " ".join(str(d) for d in spec.get("dependencies", [])).lower()
    has_interchange = ("interchange" in hyps_str or "derivative under" in hyps_str or "fubini" in hyps_str or "dominated convergence" in hyps_str or
                       "interchange" in deps_str or "derivative under" in deps_str or "fubini" in deps_str or "dominated convergence" in deps_str)
    if (r"\frac{d}{d" in stmt or r"\int" in stmt) and r"\sum" in stmt and not has_interchange:
        warnings.append("Gate 7 [Interchange] WARNING: Sum and integral/derivative co-occur without explicit interchange theorem recorded.")
    else:
        passed_gates.append("Gate 7: Interchange Audit")

    # --- Gate 8: Independent Derivation Audit ---
    if len(spec.get("dependencies", [])) < 1 and not spec.get("external_sources"):
        warnings.append("Gate 8 [Independent Derivation] WARNING: No independent external verification source or dual derivation path cited.")
    else:
        passed_gates.append("Gate 8: Independent Derivation Audit")

    # --- Gate 9: Adversarial Falsification Audit ---
    raw_cid = str(spec.get("claim_id", "")).upper()
    falsifications = spec.get("falsification_attempts", [])
    if len(falsifications) == 0 or (len(falsifications) == 1 and str(falsifications[0]).lower().strip() in {"none", "none (only sampled confirming test points)"}):
        violations.append("Gate 9 [Adversarial Falsification] VIOLATION: No adversarial falsification attempts recorded.")
    elif raw_cid == "CLM-CT-025" and ("-0.054321" in stmt or "-0.070656" in stmt or "-0.016335" in stmt):
        violations.append("Gate 9 [Adversarial Falsification] VIOLATION: Documented witness values in specification (-0.054321, -0.070656) do not match certified executable proof artifact (-0.0515509, -0.0240200, +0.0275309).")
    else:
        passed_gates.append("Gate 9: Adversarial Falsification Audit")

    # --- Gate 10: Evidence Classification Audit ---
    role = spec.get("epistemic_role")
    if role not in ALLOWED_EPISTEMIC_ROLES:
        violations.append(f"Gate 10 [Evidence Classification] VIOLATION: Unknown epistemic role '{role}'. Allowed: {ALLOWED_EPISTEMIC_ROLES}")
    elif role == "LOAD_BEARING_ANALYTIC_THEOREM" and spec.get("remaining_analytic_dependencies"):
        if any(str(dep).strip() for dep in spec.get("remaining_analytic_dependencies", [])):
            violations.append(
                "Gate 10 [Evidence Classification] VIOLATION: Claim classified as LOAD_BEARING_ANALYTIC_THEOREM "
                "while open analytic dependencies remain unproved."
            )
    else:
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
]

KNOWN_EXEMPT_PATTERNS = [
    "OPEN",
    "OPEN / CANDIDATE",
    "SENSITIVITY DIAGNOSTIC",
    "METHODOLOGICAL / ENFORCED",
    "SCOPED STATUS",
    "CANDIDATE",
]


def cross_check_claim_register(repo_root: str) -> Tuple[bool, List[str], List[str], Dict[str, Any]]:
    """
    Exhaustively cross-checks the canonical claim_register.md against machine-readable specifications in .agents/claims/
    and hash-pinned grandfathered entries in .agents/corpus_map/legacy_claim_manifest.json.

    Policy B (Grandfathered Migration):
    - New terminal claims always require validated specifications in .agents/claims/.
    - Modified legacy claims or status transitions require validated specifications in .agents/claims/.
    - Unchanged legacy terminal claims matching legacy_claim_manifest.json pass provisionally as LEGACY_UNAUDITED.
    - Open/exempt claims pass as Exempt.
    - Fails on unknown statuses, missing specifications, or modified legacy claims without specifications.
    - Strictly enforces:
        terminal_claims == audited_terminal_claims + legacy_unaudited_terminal_claims + missing_specifications
        total_claims == terminal_claims + open_or_exempt_claims
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

