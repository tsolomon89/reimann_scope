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
    "formal/RiemannScope/RadialDefect.lean",
    "formal/RiemannScope/TranscendentalContinuation.lean",
    "formal/RiemannScope/ZeroWorldline.lean",
    "formal/RiemannScope/RadialLeaf.lean",
    "formal/RiemannScope/ZeroCharacter.lean",
    "formal/RiemannScope/SymmetricDefect.lean",
    "formal/RiemannScope/Contradiction.lean",
    "formal/RiemannScope/ArithmeticBridge.lean",
]


REQUIRED_BUILDER_FILES = [
    "scripts/build_formal.py",
    "certification.py",
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


def get_builder_source_hashes() -> Dict[str, str]:
    hashes = {}
    for f in REQUIRED_BUILDER_FILES:
        hashes[f] = _hash_file(f)
    return hashes


import re


def count_project_theorems() -> int:
    """Count the number of project theorem declarations across formal source files."""
    count = 0
    pattern = re.compile(r'^\s*theorem\s+([A-Za-z0-9_]+)', re.MULTILINE)
    for src in FORMAL_SOURCE_FILES:
        p = os.path.join(REPO_ROOT, src)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()
            count += len(pattern.findall(content))
    return count


def _is_formal_env_dirty() -> Tuple[bool, List[str]]:
    """Check if any formal source, config, or builder file is dirty in git."""
    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        dirty_files = []
        for line in status.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            parts = line_str.split(None, 1)
            if len(parts) < 2:
                dirty_files.append(line_str)
                continue
            p = parts[1].strip().strip('"').replace("\\", "/")
            if p in ("research/index.json", "formal/build_report.json") or p.startswith("research/runs/") or p.startswith("data/certificates/"):
                continue
            dirty_files.append(p)
        return len(dirty_files) > 0, dirty_files
    except Exception as e:
        return False, []


def build_formal(git_commit: Optional[str] = None, allow_dirty: bool = False) -> Tuple[bool, Dict[str, Any], List[str]]:
    """Execute lake build and write formal/build_report.json."""
    errors: List[str] = []

    # 1. Resolve and validate git commit
    try:
        current_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, stderr=subprocess.DEVNULL).decode("utf-8").strip()
    except Exception as e:
        current_head = "UNKNOWN"
        errors.append(f"Failed resolving HEAD commit: {e}")

    if git_commit:
        if git_commit != current_head:
            errors.append(f"Requested commit '{git_commit}' does not match checked-out HEAD '{current_head}'")
    else:
        git_commit = current_head

    if not git_commit or len(git_commit) != 40 or git_commit.lower() in ("0" * 40, "unknown", "fake", "forged"):
        errors.append(f"Invalid git commit SHA: '{git_commit}'")

    # 2. Check worktree cleanliness for formal and builder files
    is_dirty, dirty_list = _is_formal_env_dirty()
    if is_dirty and not allow_dirty:
        errors.append(f"Worktree is dirty for source/formal files: {dirty_list}")

    # 3. Capture toolchain versions
    lake_ver = "UNKNOWN"
    lean_ver = "UNKNOWN"
    try:
        proc_lake = subprocess.run(["lake", "--version"], cwd=FORMAL_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc_lake.returncode == 0:
            lake_ver = proc_lake.stdout.strip()
        else:
            errors.append(f"lake --version failed with exit code {proc_lake.returncode}")
    except Exception as e:
        errors.append(f"Failed executing 'lake --version': {e}")

    try:
        proc_lean = subprocess.run(["lean", "--version"], cwd=FORMAL_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc_lean.returncode == 0:
            lean_ver = proc_lean.stdout.strip()
        else:
            errors.append(f"lean --version failed with exit code {proc_lean.returncode}")
    except Exception as e:
        errors.append(f"Failed executing 'lean --version': {e}")

    if not lake_ver or lake_ver.lower() in ("unknown", "placeholder", "none", "fake", "forged", "n/a"):
        errors.append(f"Invalid or placeholder lake_version: '{lake_ver}'")
    if not lean_ver or lean_ver.lower() in ("unknown", "placeholder", "none", "fake", "forged", "n/a"):
        errors.append(f"Invalid or placeholder lean_version: '{lean_ver}'")

    # 4. Check existence of all required formal and builder files
    formal_hashes = get_formal_source_hashes()
    for f, h in formal_hashes.items():
        if h == "N/A":
            errors.append(f"Required formal source file missing on disk: '{f}'")

    toolchain_hash = _hash_file("formal/lean-toolchain")
    if toolchain_hash == "N/A":
        errors.append("formal/lean-toolchain missing on disk")

    lakefile_hash = _hash_file("formal/lakefile.toml")
    if lakefile_hash == "N/A":
        errors.append("formal/lakefile.toml missing on disk")

    lake_manifest_hash = _hash_file("formal/lake-manifest.json")
    if lake_manifest_hash == "N/A":
        errors.append("formal/lake-manifest.json missing on disk")

    builder_hashes = get_builder_source_hashes()
    for f, h in builder_hashes.items():
        if h == "N/A":
            errors.append(f"Required builder source module missing on disk: '{f}'")

    # 5. Execute lake build
    build_passed = False
    exit_code = -1
    build_stdout = ""
    build_stderr = ""
    if not errors:
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
    else:
        build_passed = False
        exit_code = -1

    theorems_count = count_project_theorems()
    report = {
        "schema_version": "1.0.0",
        "report_type": "formal_build_report",
        "status": "passed" if (build_passed and len(errors) == 0) else "failed",
        "command": "lake build",
        "exit_code": exit_code,
        "producing_git_commit": git_commit,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "lake_version": lake_ver,
        "lean_version": lean_ver,
        "project_theorem_declarations_compiled": theorems_count,
        "total_theorems": theorems_count,
        "formal_source_hashes": formal_hashes,
        "lean_toolchain_hash": toolchain_hash,
        "lakefile_hash": lakefile_hash,
        "lake_manifest_hash": lake_manifest_hash,
        "builder_source_hashes": builder_hashes,
        "build_stdout": build_stdout,
        "build_stderr": build_stderr
    }

    # Canonical self-hash
    clean_rep = {k: v for k, v in report.items() if k != "report_hash"}
    report["report_hash"] = hashlib.sha256(json.dumps(clean_rep, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return (build_passed and len(errors) == 0), report, errors


def main():
    parser = argparse.ArgumentParser(description="Build Lean formalization and generate formal build report")
    parser.add_argument("--commit", type=str, default=None, help="Explicit producing commit SHA")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow generating report on dirty working tree")
    args = parser.parse_args()

    print("=== Building Lean 4 Formalization (lake build) ===")
    ok, rep, errs = build_formal(git_commit=args.commit, allow_dirty=args.allow_dirty)
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
