"""Build and certify Lean 4 formalization for Riemann Scope.

Executes `lake build` in formal/ and emits formal/build_report.json containing:
- execution status and exit code
- producing git commit
- formal source hashes
- toolchain & lakefile hashes
- lake & lean version metadata
- canonical report self-hash
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

FORMAL_DIR = os.path.join(REPO_ROOT, "formal")
REPORT_PATH = os.path.join(FORMAL_DIR, "build_report.json")

FORMAL_SOURCE_FILES = [
    "formal/RiemannScope.lean",
    "formal/RiemannScope/Basic.lean",
    "formal/RiemannScope/Grade.lean",
    "formal/RiemannScope/TranscendentalContinuation.lean",
    "formal/RiemannScope/ZeroWorldline.lean",
    "formal/RiemannScope/RadialLeaf.lean",
    "formal/RiemannScope/ZeroCharacter.lean",
    "formal/RiemannScope/SymmetricDefect.lean",
    "formal/RiemannScope/Contradiction.lean",
]


def _hash_file(rel_path: str) -> str:
    full_path = os.path.join(REPO_ROOT, rel_path)
    if not os.path.exists(full_path):
        return "N/A"
    with open(full_path, "rb") as f:
        content = f.read().replace(b"\r\n", b"\n")
    return hashlib.sha256(content).hexdigest()


def get_formal_source_hashes() -> Dict[str, str]:
    hashes = {}
    for f in FORMAL_SOURCE_FILES:
        hashes[f] = _hash_file(f)
    return hashes


def build_formal(git_commit: Optional[str] = None) -> Tuple[bool, Dict[str, Any], List[str]]:
    """Execute lake build and write formal/build_report.json."""
    errors: List[str] = []

    # 1. Capture toolchain versions
    lake_ver = "UNKNOWN"
    lean_ver = "UNKNOWN"
    try:
        proc_lake = subprocess.run(["lake", "--version"], cwd=FORMAL_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc_lake.returncode == 0:
            lake_ver = proc_lake.stdout.strip()
    except Exception as e:
        errors.append(f"Failed executing 'lake --version': {e}")

    try:
        proc_lean = subprocess.run(["lean", "--version"], cwd=FORMAL_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc_lean.returncode == 0:
            lean_ver = proc_lean.stdout.strip()
    except Exception as e:
        errors.append(f"Failed executing 'lean --version': {e}")

    # 2. Execute lake build
    build_passed = False
    exit_code = -1
    build_stdout = ""
    build_stderr = ""
    try:
        proc_build = subprocess.run(["lake", "build"], cwd=FORMAL_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        exit_code = proc_build.returncode
        build_stdout = proc_build.stdout.strip()
        build_stderr = proc_build.stderr.strip()
        build_passed = (exit_code == 0)
        if not build_passed:
            errors.append(f"lake build failed (exit code {exit_code}): {build_stderr or build_stdout}")
    except Exception as e:
        errors.append(f"Failed executing 'lake build': {e}")

    # 3. Capture file hashes
    formal_hashes = get_formal_source_hashes()
    toolchain_hash = _hash_file("formal/lean-toolchain")
    lakefile_hash = _hash_file("formal/lakefile.toml")
    lake_manifest_hash = _hash_file("formal/lake-manifest.json")

    # 4. Resolve commit
    if not git_commit:
        try:
            git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, stderr=subprocess.DEVNULL).decode("utf-8").strip()
        except Exception:
            git_commit = "UNKNOWN"

    report = {
        "schema_version": "1.0.0",
        "report_type": "formal_build_report",
        "status": "passed" if build_passed else "failed",
        "command": "lake build",
        "exit_code": exit_code,
        "producing_git_commit": git_commit,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "lake_version": lake_ver,
        "lean_version": lean_ver,
        "formal_source_hashes": formal_hashes,
        "lean_toolchain_hash": toolchain_hash,
        "lakefile_hash": lakefile_hash,
        "lake_manifest_hash": lake_manifest_hash,
        "build_stdout": build_stdout,
        "build_stderr": build_stderr
    }

    # Canonical self-hash
    clean_rep = {k: v for k, v in report.items() if k != "report_hash"}
    report["report_hash"] = hashlib.sha256(json.dumps(clean_rep, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return build_passed, report, errors


def main():
    parser = argparse.ArgumentParser(description="Build Lean formalization and generate formal build report")
    parser.add_argument("--commit", type=str, default=None, help="Explicit producing commit SHA")
    args = parser.parse_args()

    print("=== Building Lean 4 Formalization (lake build) ===")
    ok, rep, errs = build_formal(git_commit=args.commit)
    if ok:
        print(f"[SUCCESS] Lean formalization built successfully. Report saved to formal/build_report.json")
        sys.exit(0)
    else:
        print(f"[FAILURE] Lean formalization build failed:")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
