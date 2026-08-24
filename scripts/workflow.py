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
    """Run fast operational tests and experiment spec validations."""
    print("=== [1/2] Validating Experiment Specifications ===")
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

    print("\n=== [2/2] Running Fast Operational Pytest Tier ===")
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
    print(f"[PASS] Formal build report verified: {formal_rep.get('total_theorems', 0)} theorems checked in Lean 4.")

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


def plan_canonical_regeneration() -> Dict[str, Any]:
    """Inspect and report which certificates and experiment runs are stale."""
    head_commit, is_dirty = research_runner.get_git_info()

    print(f"=== Planning Canonical Regeneration ===")
    print(f"Current Git HEAD: {head_commit} (Dirty: {is_dirty})")

    # 1. Inspect Certificates
    cert_plan: Dict[str, Any] = {"status": "up_to_date", "stale_reasons": []}
    rep_ok, rep, rep_errs = certification.load_verification_report(check_provenance=True, canonical_current=True)
    if not rep_ok:
        cert_plan["status"] = "stale"
        cert_plan["stale_reasons"] = rep_errs
    print(f"\nCertificates Status: {cert_plan['status'].upper()}")
    if cert_plan["stale_reasons"]:
        for r in cert_plan["stale_reasons"][:5]:
            print(f"  - {r}")

    # 2. Inspect Canonical Runs
    runs_dir = os.path.join(REPO_ROOT, "research", "runs")
    exp_dir = os.path.join(REPO_ROOT, "research", "experiments")
    specs = sorted(glob.glob(os.path.join(exp_dir, "*.yaml")))

    run_plans: List[Dict[str, Any]] = []
    total_stale_points = 0

    import yaml
    for sf in specs:
        with open(sf, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        exp_id = spec["id"]
        r_dir = os.path.join(runs_dir, exp_id)
        r_plan = {
            "experiment_id": exp_id,
            "status": "up_to_date",
            "points": len(research_runner.generate_parameter_grid(spec.get("parameters", {}), dps=spec.get("precision", {}).get("dps", 50))),
            "reasons": []
        }

        if not os.path.exists(r_dir):
            r_plan["status"] = "missing"
            r_plan["reasons"].append(f"Run directory '{r_dir}' not found on disk")
        else:
            ok, errs = research_runner.validate_run_bundle(r_dir, canonical_current=True)
            if not ok:
                r_plan["status"] = "stale"
                r_plan["reasons"] = errs

        if r_plan["status"] != "up_to_date":
            total_stale_points += r_plan["points"]
        run_plans.append(r_plan)

    print("\nCanonical Experiment Runs Plan:")
    for rp in run_plans:
        status_str = f"[{rp['status'].upper()}]"
        print(f"  {status_str:12s} {rp['experiment_id']} ({rp['points']} points)")
        if rp["reasons"]:
            for reason in rp["reasons"][:2]:
                print(f"      Reason: {reason}")

    print(f"\nSummary: {sum(1 for r in run_plans if r['status'] == 'up_to_date')}/{len(run_plans)} runs up-to-date.")
    if total_stale_points > 0:
        print(f"Regeneration required for {total_stale_points} points across {sum(1 for r in run_plans if r['status'] != 'up_to_date')} experiment(s).")
    else:
        print("All canonical runs are completely up-to-date with current disk implementation.")

    return {
        "head_commit": head_commit,
        "is_dirty": is_dirty,
        "certificates": cert_plan,
        "runs": run_plans,
        "total_stale_points": total_stale_points
    }


def run_canonical(allow_dirty: bool = False, experiments: Optional[List[str]] = None) -> int:
    """Execute planned canonical regeneration with clean-tree enforcement."""
    _, is_dirty = research_runner.get_git_info()
    if is_dirty and not allow_dirty:
        print("[ERROR] Working tree contains uncommitted changes. Cannot generate canonical artifacts bound to uncommitted state.")
        print("Please commit all changes or pass --allow-dirty for test runs.")
        return 1

    print("=== [1/3] Generating Mathematical Certificates ===")
    gen_cert_cmd = [sys.executable, os.path.join(REPO_ROOT, "scripts", "generate_certificates.py")]
    res = subprocess.run(gen_cert_cmd, cwd=REPO_ROOT)
    if res.returncode != 0:
        print("[FAIL] Certificate generation failed.")
        return res.returncode

    print("\n=== [2/3] Executing Canonical Experiment Sweeps ===")
    exp_dir = os.path.join(REPO_ROOT, "research", "experiments")
    target_specs = []
    if experiments:
        import yaml
        for e in experiments:
            candidates = [
                e,
                os.path.join(exp_dir, e),
                os.path.join(exp_dir, f"{e}.yaml"),
                os.path.join(exp_dir, f"{e.replace('-', '_')}.yaml"),
                os.path.join(exp_dir, f"{e.replace('_', '-')}.yaml"),
            ]
            found = None
            for cand in candidates:
                if os.path.exists(cand):
                    found = cand
                    break
            if not found:
                for sf in glob.glob(os.path.join(exp_dir, "*.yaml")):
                    with open(sf, "r", encoding="utf-8") as f:
                        s_data = yaml.safe_load(f)
                    if s_data and s_data.get("id") == e:
                        found = sf
                        break
            if found:
                target_specs.append(found)
            else:
                raise FileNotFoundError(f"Experiment spec for '{e}' not found in {exp_dir}")
    else:
        target_specs = sorted(glob.glob(os.path.join(exp_dir, "*.yaml")))

    for sf in target_specs:
        name = os.path.basename(sf)
        print(f"\n--- Running Canonical Sweep: {name} ---")
        run_id = research_runner.run_experiment(sf)
        summary = research_runner.summarize_run(run_id)
        c = summary.get("criterion", {})
        print(f"[{name}] {run_id}: status={summary.get('status')} criterion_met={c.get('criterion_met')} observed={c.get('observed')}")

    print("\n=== [3/3] Validating Regenerated Canonical Artifacts ===")
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
        sys.exit(run_canonical(allow_dirty=args.allow_dirty, experiments=args.experiments))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
