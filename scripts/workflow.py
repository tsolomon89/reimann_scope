"""scripts/workflow.py — Authoritative Research-Instrument Workflow CLI

Exposes the recurring research and verification commands:
- check-fast: Run fast operational unit/integration tests and spec validations.
- check-numerical: Run slow arbitrary-precision numerical regression suite.
- validate-artifacts: Validate certificates, canonical bundles, and formal report without mutating state.
- plan-canonical: Inspect and report which canonical items are stale or need regeneration.
- run-canonical: Execute planned canonical regenerations with clean-tree enforcement.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
from typing import Dict, Any, List, Tuple, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import certification
import research_runner
from research.handlers.registry import get_handler, list_registered_handlers


def run_check_fast() -> int:
    """Run fast operational tests, claim spec audits, register cross-checks, and experiment spec validations."""
    print("=== [1/3] Validating Machine-Readable Mathematical Claim Specifications ===")
    claim_files = sorted(glob.glob(os.path.join(REPO_ROOT, ".agents", "claims", "*.json")))
    claim_errors = 0
    audit_claim_spec = None
    try:
        import importlib.util
        spec_script = os.path.join(REPO_ROOT, ".agents", "skills", "zeta-proof-audit", "scripts", "audit_claim_spec.py")
        if os.path.exists(spec_script):
            spec_mod = importlib.util.spec_from_file_location("audit_claim_spec", spec_script)
            audit_claim_spec = importlib.util.module_from_spec(spec_mod)
            spec_mod.loader.exec_module(audit_claim_spec)
    except Exception as e:
        print(f"[WARN] Could not load audit_claim_spec: {e}")

    if claim_files and audit_claim_spec:
        for cf in claim_files:
            cname = os.path.basename(cf)
            try:
                with open(cf, "r", encoding="utf-8") as f:
                    cspec = json.load(f)
                res = audit_claim_spec.audit_claim_specification(cspec)
                if res["status"] == "PASS":
                    print(f"[PASS] {cname} ({cspec.get('claim_id')}): 10/10 gates passed.")
                else:
                    print(f"[FAIL] {cname} ({cspec.get('claim_id')}): {len(res['violations'])} gate violations:")
                    for v in res["violations"]:
                        print(f"  - {v}")
                    claim_errors += 1
            except Exception as e:
                print(f"[FAIL] {cname}: Error reading claim: {e}")
                claim_errors += 1

        # Cross-check claim_register.md against .agents/claims/
        ok, reg_errors, reg_passed = audit_claim_spec.cross_check_claim_register(REPO_ROOT)
        if not ok:
            print("[FAIL] Claim register cross-check failed:")
            for re in reg_errors:
                print(f"  - {re}")
            claim_errors += len(reg_errors)
        else:
            print(f"[PASS] Claim register cross-check verified {len(reg_passed)} claims against audited specifications.")
    elif not claim_files:
        print("[INFO] No machine-readable claim specifications in .agents/claims/ (skipping).")

    if claim_errors > 0:
        print(f"\n[FAIL] {claim_errors} mathematical claim specification or register check(s) failed.")
        return 1

    print("\n=== [2/3] Validating Experiment Specifications ===")
    spec_files = sorted(glob.glob(os.path.join(REPO_ROOT, "research", "experiments", "*.yaml")))
    if not spec_files:
        print("[ERROR] No experiment specifications found in research/experiments/")
        return 1

    spec_errors = 0
    import yaml
    for sf in spec_files:
        name = os.path.basename(sf)
        try:
            with open(sf, "r", encoding="utf-8") as f:
                spec = yaml.safe_load(f)
            ok, err = research_runner.validate_spec(spec)
            if not ok:
                print(f"[FAIL] {name}: {err}")
                spec_errors += 1
            else:
                print(f"[PASS] {name}")
        except Exception as e:
            print(f"[FAIL] {name}: Parse error: {e}")
            spec_errors += 1

    if spec_errors > 0:
        print(f"\n[FAIL] {spec_errors} experiment specification(s) failed validation.")
        return 1

    print("\n=== [3/3] Running Fast Operational Pytest Tier ===")
    cmd = [sys.executable, "-m", "pytest", "-m", "not slow_numerical"]
    res = subprocess.run(cmd, cwd=REPO_ROOT)
    return res.returncode


def run_check_numerical() -> int:
    """Run slow arbitrary-precision numerical regression suite."""
    print("=== Running Slow Numerical Regression Suite ===")
    cmd = [sys.executable, "-m", "pytest", "-m", "slow_numerical"]
    res = subprocess.run(cmd, cwd=REPO_ROOT)
    return res.returncode


def run_validate_artifacts(canonical_current: bool = False) -> int:
    """Independently validate certificates, canonical run bundles, and formal report."""
    print("=== [1/3] Validating Mathematical Certificates & Verification Report ===")
    rep_ok, rep, rep_errs = certification.load_verification_report(
        check_provenance=True,
        canonical_current=canonical_current
    )
    if not rep_ok:
        print(f"[FAIL] Certificate verification report failed:")
        for err in rep_errs:
            print(f"  - {err}")
        return 1
    print(f"[PASS] Verified {rep.get('total_inventory', 0)} certificates in Arb (0 failures).")

    print("\n=== [2/3] Validating Formal Lean 4 Build Report ===")
    formal_ok, formal_state, formal_rep, formal_errs = certification.verify_formal_build_report(
        check_current=canonical_current
    )
    if not formal_ok:
        print(f"[FAIL] Formal build report invalid ({formal_state}):")
        for err in formal_errs:
            print(f"  - {err}")
        return 1
    thm_count = formal_rep.get("project_theorem_declarations_compiled", formal_rep.get("total_theorems", 0))
    print(f"[PASS] Formal build report verified: {thm_count} project theorem declarations compiled in Lean 4.")

    print("\n=== [3/3] Validating Canonical Experiment Run Bundles ===")
    runs_dir = os.path.join(REPO_ROOT, "research", "runs")
    run_dirs = sorted([
        d for d in glob.glob(os.path.join(runs_dir, "*"))
        if os.path.isdir(d) and not os.path.basename(d).startswith(".")
    ])

    if not run_dirs:
        print("[FAIL] No canonical run directories found in research/runs/")
        return 1

    run_errors = 0
    for r_dir in run_dirs:
        name = os.path.basename(r_dir)
        ok, errs = research_runner.validate_run_bundle(r_dir, canonical_current=canonical_current)
        if ok:
            print(f"[PASS] {name}")
        else:
            print(f"[FAIL] {name}:")
            for err in errs:
                print(f"  - {err}")
            run_errors += 1

    if run_errors > 0:
        print(f"\n[FAIL] {run_errors} canonical run bundle(s) failed validation.")
        return 1

    print("\n[SUCCESS] All mathematical certificates, formal theorems, and canonical runs validated successfully.")
    return 0


def inspect_canonical_state(target_experiments: Optional[List[str]] = None) -> Dict[str, Any]:
    """Component-level inspection of certificates, formal report, and experiment runs."""
    head_commit, is_dirty = research_runner.get_git_info()

    # 1. Inspect Certificates
    cert_state: Dict[str, Any] = {"status": "current", "stale_reasons": []}
    rep_ok, rep, rep_errs = certification.load_verification_report(check_provenance=True, canonical_current=True)
    if not rep_ok:
        cert_state["status"] = "stale"
        cert_state["stale_reasons"] = rep_errs

    # 2. Inspect Formal Build Report
    formal_state_dict: Dict[str, Any] = {"status": "current", "theorems": 0, "stale_reasons": []}
    formal_ok, f_state, f_rep, f_errs = certification.verify_formal_build_report(check_current=True)
    if not formal_ok:
        formal_state_dict["status"] = "stale"
        formal_state_dict["stale_reasons"] = f_errs
    else:
        formal_state_dict["theorems"] = f_rep.get("project_theorem_declarations_compiled", f_rep.get("total_theorems", 0))

    # 3. Inspect Canonical Experiment Runs
    runs_dir = os.path.join(REPO_ROOT, "research", "runs")
    exp_dir = os.path.join(REPO_ROOT, "research", "experiments")
    all_specs = sorted(glob.glob(os.path.join(exp_dir, "*.yaml")))

    run_plans: List[Dict[str, Any]] = []
    import yaml
    for sf in all_specs:
        with open(sf, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        exp_id = spec["id"]
        if target_experiments and exp_id not in target_experiments and sf not in target_experiments:
            continue

        r_dir = os.path.join(runs_dir, exp_id)
        points_count = len(research_runner.generate_parameter_grid(
            spec.get("parameters", {}),
            dps=spec.get("precision", {}).get("dps", 50)
        ))

        r_plan: Dict[str, Any] = {
            "experiment_id": exp_id,
            "spec_file": sf,
            "points": points_count,
            "execution_status": "execution_current",
            "summary_status": "summary_current",
            "overall_status": "current",
            "needs_execution": False,
            "needs_summary": False,
            "reasons": []
        }

        if not os.path.exists(r_dir):
            r_plan["execution_status"] = "missing"
            r_plan["summary_status"] = "missing"
            r_plan["overall_status"] = "missing"
            r_plan["needs_execution"] = True
            r_plan["needs_summary"] = True
            r_plan["reasons"].append(f"Run directory '{r_dir}' missing on disk")
        else:
            manifest_p = os.path.join(r_dir, "manifest.json")
            results_p = os.path.join(r_dir, "results.jsonl")
            if not os.path.exists(manifest_p) or not os.path.exists(results_p):
                r_plan["execution_status"] = "missing"
                r_plan["summary_status"] = "missing"
                r_plan["overall_status"] = "missing"
                r_plan["needs_execution"] = True
                r_plan["needs_summary"] = True
                r_plan["reasons"].append("Missing manifest.json or results.jsonl")
            else:
                ok, errs = research_runner.validate_run_bundle(r_dir, canonical_current=True)
                if not ok:
                    exec_errs = []
                    summ_errs = []
                    for e in errs:
                        if any(k in e for k in ["summary_provenance", "summarizer", "summary.json", "README.md", "diagnostics.json", "Diagnostics generation failed"]):
                            summ_errs.append(e)
                        else:
                            exec_errs.append(e)

                    if exec_errs:
                        r_plan["execution_status"] = "stale_execution"
                        r_plan["needs_execution"] = True
                        r_plan["needs_summary"] = True
                        r_plan["overall_status"] = "stale_execution"
                        r_plan["reasons"].extend(exec_errs)
                        if summ_errs:
                            r_plan["reasons"].extend(summ_errs)
                    elif summ_errs:
                        r_plan["execution_status"] = "execution_current"
                        r_plan["summary_status"] = "stale_summary"
                        r_plan["needs_execution"] = False
                        r_plan["needs_summary"] = True
                        r_plan["overall_status"] = "stale_summary"
                        r_plan["reasons"].extend(summ_errs)
                    else:
                        r_plan["execution_status"] = "stale_execution"
                        r_plan["needs_execution"] = True
                        r_plan["needs_summary"] = True
                        r_plan["overall_status"] = "stale_execution"
                        r_plan["reasons"].extend(errs)

        run_plans.append(r_plan)

    total_exec_points = sum(r["points"] for r in run_plans if r["needs_execution"])
    total_summ_runs = sum(1 for r in run_plans if r["needs_summary"] and not r["needs_execution"])

    return {
        "head_commit": head_commit,
        "is_dirty": is_dirty,
        "certificates": cert_state,
        "formal_report": formal_state_dict,
        "runs": run_plans,
        "total_execution_points": total_exec_points,
        "total_resummarize_runs": total_summ_runs
    }


def plan_canonical_regeneration() -> Dict[str, Any]:
    """Inspect and report which certificates and experiment runs are stale."""
    plan = inspect_canonical_state()

    print(f"=== Planning Canonical Regeneration ===")
    print(f"Current Git HEAD: {plan['head_commit']} (Dirty: {plan['is_dirty']})")

    # 1. Report Certificates
    print(f"\nCertificates Status: {plan['certificates']['status'].upper()}")
    if plan['certificates']['stale_reasons']:
        for r in plan['certificates']['stale_reasons'][:5]:
            print(f"  - {r}")

    # 2. Report Formal Build Report
    print(f"\nFormal Build Report Status: {plan['formal_report']['status'].upper()}")
    if plan['formal_report']['stale_reasons']:
        for r in plan['formal_report']['stale_reasons'][:5]:
            print(f"  - {r}")
    else:
        print(f"  - Compiled theorems: {plan['formal_report']['theorems']}")

    # 3. Report Canonical Runs
    print("\nCanonical Experiment Runs Plan:")
    for rp in plan["runs"]:
        status_str = f"[{rp['overall_status'].upper()}]"
        print(f"  {status_str:18s} {rp['experiment_id']} ({rp['points']} points)")
        if rp["reasons"]:
            for reason in rp["reasons"][:2]:
                print(f"      Reason: {reason}")

    current_count = sum(1 for r in plan["runs"] if r["overall_status"] == "current")
    total_count = len(plan["runs"])
    print(f"\nSummary: {current_count}/{total_count} runs up-to-date.")
    if plan["total_execution_points"] > 0 or plan["total_resummarize_runs"] > 0:
        print(f"Planned actions:")
        if plan["total_execution_points"] > 0:
            print(f"  - Numerical point sweeps: {plan['total_execution_points']} points across {sum(1 for r in plan['runs'] if r['needs_execution'])} experiment(s)")
        if plan["total_resummarize_runs"] > 0:
            print(f"  - Atomic resummarizations: {plan['total_resummarize_runs']} run(s) (reusing raw results)")
    else:
        print("All canonical runs are completely up-to-date with current disk implementation.")

    return plan


def run_canonical(
    allow_dirty: bool = False,
    experiments: Optional[List[str]] = None,
    all_runs: bool = False
) -> int:
    """Execute planned canonical regeneration with clean-tree enforcement."""
    _, is_dirty = research_runner.get_git_info()
    if is_dirty and not allow_dirty:
        print("[ERROR] Working tree contains uncommitted changes. Cannot generate canonical artifacts bound to uncommitted state.")
        print("Please commit all changes or pass --allow-dirty for test runs.")
        return 1

    if all_runs:
        print("=== [1/3] Generating Mathematical Certificates ===")
        gen_cert_cmd = [sys.executable, os.path.join(REPO_ROOT, "scripts", "generate_certificates.py")]
        res = subprocess.run(gen_cert_cmd, cwd=REPO_ROOT)
        if res.returncode != 0:
            print("[FAIL] Certificate generation failed.")
            return res.returncode

        print("\n=== [2/3] Executing All Canonical Experiment Sweeps ===")
        exp_dir = os.path.join(REPO_ROOT, "research", "experiments")
        target_specs = sorted(glob.glob(os.path.join(exp_dir, "*.yaml")))
        for sf in target_specs:
            name = os.path.basename(sf)
            print(f"\n--- Running Canonical Sweep: {name} ---")
            run_id = research_runner.run_experiment(sf, canonical_current=True)
            print(f"[{name}] {run_id}: completed and published.")

        print("\n=== [3/3] Validating Regenerated Canonical Artifacts ===")
        return run_validate_artifacts(canonical_current=True)

    # Default selective execution mode
    plan = inspect_canonical_state(target_experiments=experiments)

    print("=== Planned Selective Canonical Execution ===")
    print(f"Target experiments: {len(plan['runs'])}")
    print(f"Points to execute: {plan['total_execution_points']}")
    print(f"Runs to resummarize: {plan['total_resummarize_runs']}")

    if plan['total_execution_points'] == 0 and plan['total_resummarize_runs'] == 0 and plan['certificates']['status'] == 'current':
        print("\n[SUCCESS] All targeted canonical components are completely current. No regeneration needed.")
        return run_validate_artifacts(canonical_current=True)

    # 1. Certificates
    if plan["certificates"]["status"] != "current":
        print("\n=== Generating Stale Mathematical Certificates ===")
        gen_cert_cmd = [sys.executable, os.path.join(REPO_ROOT, "scripts", "generate_certificates.py")]
        res = subprocess.run(gen_cert_cmd, cwd=REPO_ROOT)
        if res.returncode != 0:
            print("[FAIL] Certificate generation failed.")
            return res.returncode

    # 2. Experiment runs
    for run in plan["runs"]:
        if run["needs_execution"]:
            name = os.path.basename(run["spec_file"])
            print(f"\n--- Executing Canonical Sweep: {name} ({run['points']} points) ---")
            run_id = research_runner.run_experiment(run["spec_file"], canonical_current=True)
            print(f"[{name}] {run_id}: sweep completed.")
        elif run["needs_summary"]:
            print(f"\n--- Resummarizing Canonical Run: {run['experiment_id']} (reusing results.jsonl) ---")
            summary = research_runner.summarize_run(run["experiment_id"], spec_path=run["spec_file"])
            c = summary.get("criterion", {})
            print(f"[{run['experiment_id']}] status={summary.get('status')} criterion_met={c.get('criterion_met')} observed={c.get('observed')}")

    print("\n=== Validating Regenerated Canonical Artifacts ===")
    return run_validate_artifacts(canonical_current=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Authoritative research workflow interface for Reimann Scope."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # check-fast
    subparsers.add_parser("check-fast", help="Run fast operational tests and experiment spec validations.")

    # check-numerical
    subparsers.add_parser("check-numerical", help="Run slow arbitrary-precision numerical regression suite.")

    # validate-artifacts
    val_parser = subparsers.add_parser("validate-artifacts", help="Validate all certificates, canonical bundles, and formal report.")
    val_parser.add_argument("--current", action="store_true", help="Enforce exact match against current disk source code.")

    # plan-canonical
    subparsers.add_parser("plan-canonical", help="Inspect and report which certificates/runs are stale.")

    # run-canonical
    run_parser = subparsers.add_parser("run-canonical", help="Execute canonical regeneration.")
    run_parser.add_argument("--allow-dirty", action="store_true", help="Allow running on dirty working tree (non-canonical test mode).")
    run_parser.add_argument("--experiments", nargs="+", help="Specific experiment IDs or YAML files to run.")
    run_parser.add_argument("--all", action="store_true", help="Force complete regeneration of all certificates and runs.")

    args = parser.parse_args()

    if args.command == "check-fast":
        sys.exit(run_check_fast())
    elif args.command == "check-numerical":
        sys.exit(run_check_numerical())
    elif args.command == "validate-artifacts":
        sys.exit(run_validate_artifacts(canonical_current=args.current))
    elif args.command == "plan-canonical":
        plan_canonical_regeneration()
        sys.exit(0)
    elif args.command == "run-canonical":
        sys.exit(run_canonical(allow_dirty=args.allow_dirty, experiments=args.experiments, all_runs=args.all))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
