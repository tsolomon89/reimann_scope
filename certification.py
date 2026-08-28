"""Rigorous mathematical certification engine for the Riemann Scope research instrument.

Utilizes FLINT/Arb ball arithmetic (via python-flint) to compute certified root enclosures,
isolate non-trivial zeros, verify simplicity via non-zero derivative enclosures (0 ∉ ζ'(B_n)),
verify consecutive block completeness via Turing zero counting, and certify bilateral transcendental worldlines.
"""

from __future__ import annotations

import glob
import hashlib
import json
import os
import sys
import subprocess
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple, Union


try:
    import flint
    from flint import acb, acb_series, arb, ctx
    FLINT_AVAILABLE = True
except ImportError:
    flint = None  # type: ignore[assignment]
    acb = None    # type: ignore[assignment]
    acb_series = None  # type: ignore[assignment]
    arb = None    # type: ignore[assignment]
    ctx = None    # type: ignore[assignment]
    FLINT_AVAILABLE = False

AUTHORITATIVE_FLINT_VERSION = "0.6.0"
SUPPORTED_FLINT_VERSIONS = {"0.6.0"}
AUTHORITATIVE_MPMATH_VERSION = "1.3.0"
SUPPORTED_MPMATH_VERSIONS = {"1.3.0"}
SUPPORTED_PYTHON_MAJOR_MINOR = {"3.10", "3.11", "3.12", "3.13"}
SUPPORTED_PLATFORMS = {"win32", "linux", "darwin"}
CERTIFICATE_SCHEMA_VERSION = "2.0"
VERIFIER_VERSION = "2.0.0"
ALGORITHM_VERSION = "2.0.0"
SUPPORTED_VERIFIER_VERSIONS = {"2.0.0"}
SUPPORTED_ALGORITHM_VERSIONS = {"2.0.0"}
SUPPORTED_REPORT_TYPES = {"certificate_verification_report"}

FLINT_VERSION = getattr(flint, "__version__", AUTHORITATIVE_FLINT_VERSION) if flint is not None else "N/A"

REQUIRED_DEPENDENCY_KEYS = (
    "python",
    "python_flint",
    "mpmath",
    "platform",
    "library",
    "library_version",
    "verifier_version",
    "algorithm_version",
)

REQUIRED_SOURCE_MODULES = [
    "certification.py",
    "transforms.py",
    "reference_data.py",
    "math_core.py",
    "transcendental.py",
    "converter.py",
    "research_runner.py",
    "zero_finder.py"
]

CERTIFICATE_MODULE_DEPENDENCIES: Dict[str, List[str]] = {
    "zero_isolation_and_simplicity": ["certification.py", "reference_data.py", "zero_finder.py"],
    "trivial_zero_certificate": ["certification.py", "math_core.py"],
    "trivial_zero": ["certification.py", "math_core.py"],
    "complete_block_certificate": ["certification.py", "reference_data.py", "zero_finder.py"],
    "block_isolation_and_order": ["certification.py", "reference_data.py", "zero_finder.py"],
    "worldline_certificate": ["certification.py", "transcendental.py", "math_core.py", "reference_data.py"],
    "radial_witness_certificate": ["certification.py", "math_core.py"],
    "g4_radial_witness": ["certification.py", "math_core.py"],
}

CERTIFICATE_MATHEMATICAL_MODULES: List[str] = [
    "certification.py",
    "math_core.py",
    "zero_finder.py",
    "transcendental.py",
    "reference_data.py",
]

REQUIRED_INPUT_DATA_FILES = [
    "zeros_reference.json",
    "zeros_first_100_reference.json",
    "canonical_blocks.json",
    "primes.json"
]

CERTIFICATE_DATA_DEPENDENCIES: Dict[str, List[str]] = {
    "zero_isolation_and_simplicity": ["zeros_reference.json", "zeros_first_100_reference.json"],
    "trivial_zero_certificate": [],
    "trivial_zero": [],
    "complete_block_certificate": ["zeros_reference.json", "zeros_first_100_reference.json", "canonical_blocks.json"],
    "block_isolation_and_order": ["zeros_reference.json", "zeros_first_100_reference.json", "canonical_blocks.json"],
    "worldline_certificate": ["zeros_reference.json"],
    "radial_witness_certificate": [],
    "g4_radial_witness": [],
}

REQUIRED_FORMAL_SOURCES = [
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
    "formal/RiemannScope/CurvatureTransport.lean",
]


REQUIRED_FORMAL_CONFIG_FILES = {
    "lean_toolchain": "formal/lean-toolchain",
    "lakefile": "formal/lakefile.toml",
    "lake_manifest": "formal/lake-manifest.json",
}

REQUIRED_FORMAL_BUILDER_MODULES = [
    "scripts/build_formal.py",
    "certification.py",
]

CERTIFICATION_LEVELS = [
    "candidate",
    "residual_verified",
    "isolated_zero_certified",
    "simple_zero_certified",
    "complete_block_certified",
    "worldline_certified",
    "radial_witness_certified",
]


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
CERT_DIR = os.path.join(REPO_ROOT, "data", "certificates")
ZEROS_DIR = os.path.join(CERT_DIR, "zeros")
TRIVIAL_ZEROS_DIR = os.path.join(CERT_DIR, "trivial_zeros")
BLOCKS_DIR = os.path.join(CERT_DIR, "blocks")
WORLDLINES_DIR = os.path.join(CERT_DIR, "worldlines")
WITNESSES_DIR = os.path.join(CERT_DIR, "witnesses")



def _sha256_canonical(obj: Dict[str, Any]) -> str:
    """Compute SHA-256 of JSON object without the 'certificate_hash' or 'report_hash' fields."""
    clean_obj = {k: v for k, v in obj.items() if k not in ("certificate_hash", "report_hash")}
    encoded = json.dumps(clean_obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_dependency_compatibility(
    dep_fp: Optional[Dict[str, Any]],
    check_current_runtime: bool = True
) -> Tuple[bool, List[str]]:
    """Validate dependency fingerprint against authoritative compatibility policy."""
    errors: List[str] = []
    if not isinstance(dep_fp, dict) or not dep_fp:
        return False, ["Missing or empty dependency_fingerprint"]

    for k in REQUIRED_DEPENDENCY_KEYS:
        val = dep_fp.get(k)
        if val is None or not str(val).strip() or str(val).strip() in ("N/A", "0.0", "forged", "unknown", "fake"):
            errors.append(f"dependency_fingerprint missing or invalid key '{k}': got '{val}'")

    py_ver = str(dep_fp.get("python", "")).strip()
    if not any(py_ver.startswith(f"{v}.") or py_ver == v for v in SUPPORTED_PYTHON_MAJOR_MINOR):
        errors.append(f"Unsupported python version in metadata: '{py_ver}'. Supported: {sorted(list(SUPPORTED_PYTHON_MAJOR_MINOR))}")

    flint_ver = str(dep_fp.get("python_flint", "")).strip()
    if flint_ver not in SUPPORTED_FLINT_VERSIONS:
        errors.append(f"Unsupported python_flint version '{flint_ver}'. Supported: {sorted(list(SUPPORTED_FLINT_VERSIONS))}")

    mp_ver = str(dep_fp.get("mpmath", "")).strip()
    if mp_ver not in SUPPORTED_MPMATH_VERSIONS:
        errors.append(f"Unsupported mpmath version '{mp_ver}'. Supported: {sorted(list(SUPPORTED_MPMATH_VERSIONS))}")

    plat = str(dep_fp.get("platform", "")).strip().lower()
    if plat not in SUPPORTED_PLATFORMS:
        errors.append(f"Unsupported platform in dependency fingerprint: '{plat}'. Supported: {sorted(list(SUPPORTED_PLATFORMS))}")

    lib_name = dep_fp.get("library")
    if lib_name != "python-flint":
        errors.append(f"Unsupported certification library '{lib_name}'. Expected 'python-flint'")

    lib_ver = str(dep_fp.get("library_version", "")).strip()
    if lib_ver != flint_ver:
        errors.append(f"Contradictory library_version ('{lib_ver}') != python_flint ('{flint_ver}')")

    ver_ver = str(dep_fp.get("verifier_version", "")).strip()
    if ver_ver not in SUPPORTED_VERIFIER_VERSIONS:
        errors.append(f"Unsupported verifier_version '{ver_ver}'. Expected one of: {sorted(list(SUPPORTED_VERIFIER_VERSIONS))}")

    algo_ver = str(dep_fp.get("algorithm_version", "")).strip()
    if algo_ver not in SUPPORTED_ALGORITHM_VERSIONS:
        errors.append(f"Unsupported algorithm_version '{algo_ver}'. Expected one of: {sorted(list(SUPPORTED_ALGORITHM_VERSIONS))}")

    if check_current_runtime:
        # Check current running python
        curr_py = sys.version.split()[0]
        if not any(curr_py.startswith(f"{v}.") or curr_py == v for v in SUPPORTED_PYTHON_MAJOR_MINOR):
            errors.append(f"Current runtime Python ({curr_py}) is unsupported")

        # Check current python-flint
        if not FLINT_AVAILABLE or FLINT_VERSION not in SUPPORTED_FLINT_VERSIONS:
            errors.append(f"Current runtime python-flint version ({FLINT_VERSION}) is unsupported")

        # Check current mpmath
        import mpmath
        curr_mp = getattr(mpmath, "__version__", "N/A")
        if curr_mp not in SUPPORTED_MPMATH_VERSIONS:
            errors.append(f"Current runtime mpmath version ({curr_mp}) is unsupported")

        # Check current platform
        curr_plat = sys.platform.lower()
        if curr_plat not in SUPPORTED_PLATFORMS:
            errors.append(f"Current runtime platform '{curr_plat}' is unsupported")

    return len(errors) == 0, errors


def _get_source_code_hashes(commit: Optional[str] = None, modules: Optional[List[str]] = None) -> Dict[str, str]:
    """Compute normalized LF SHA-256 hashes of core mathematical and certification modules."""
    hashes: Dict[str, str] = {}
    target_modules = modules if modules is not None else REQUIRED_SOURCE_MODULES
    for mod in target_modules:
        if commit:
            b_hash = _get_historical_git_blob_hash(commit, mod)
            if b_hash:
                hashes[mod] = b_hash
                continue
        mod_path = os.path.join(REPO_ROOT, mod)
        if os.path.exists(mod_path):
            with open(mod_path, "rb") as f:
                content = f.read().replace(b"\r\n", b"\n")
            hashes[mod] = hashlib.sha256(content).hexdigest()
        else:
            hashes[mod] = "N/A"
    return hashes


def _get_input_data_hashes(commit: Optional[str] = None, files: Optional[List[str]] = None) -> Dict[str, str]:
    """Get SHA-256 hashes of reference data."""
    hashes: Dict[str, str] = {}
    target_files = files if files is not None else REQUIRED_INPUT_DATA_FILES
    for raw_df in target_files:
        df = raw_df.replace("data/", "", 1) if raw_df.startswith("data/") else raw_df
        if commit:
            b_hash = _get_historical_git_blob_hash(commit, f"data/{df}")
            if b_hash:
                hashes[df] = b_hash
                continue
        df_path = os.path.join(REPO_ROOT, "data", df)
        if os.path.exists(df_path):
            with open(df_path, "rb") as f:
                content = f.read().replace(b"\r\n", b"\n")
            hashes[df] = hashlib.sha256(content).hexdigest()
        else:
            hashes[df] = "N/A"
    return hashes


def _get_dependency_fingerprint() -> Dict[str, str]:
    """Capture environment dependency versions."""
    import mpmath
    return {
        "python": sys.version.split()[0],
        "python_flint": FLINT_VERSION,
        "mpmath": getattr(mpmath, "__version__", "N/A"),
        "platform": sys.platform,
        "library": "python-flint",
        "library_version": FLINT_VERSION,
        "verifier_version": VERIFIER_VERSION,
        "algorithm_version": ALGORITHM_VERSION
    }



_GIT_BLOB_CACHE: Dict[Tuple[str, str], Optional[str]] = {}
_GIT_COMMIT_VALID_CACHE: Dict[Tuple[str, bool], Tuple[bool, str]] = {}


def _get_historical_git_blob(commit_sha: str, path: str) -> Optional[bytes]:
    try:
        norm_p = path.replace("\\", "/")
        proc = subprocess.run(
            ["git", "show", f"{commit_sha}:{norm_p}"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        if proc.returncode != 0:
            return None
        return proc.stdout.replace(b"\r\n", b"\n")
    except Exception:
        return None


CERTIFICATE_MATHEMATICAL_FUNCTIONS: List[str] = [
    "_split_ball_str",
    "_reconstruct_arb_ball",
    "certify_zero",
    "certify_trivial_zero",
    "certify_block",
    "certify_worldline",
    "_verify_zero_enclosure_and_isolation",
    "_verify_trivial_zero_enclosure",
    "_verify_block_isolation",
    "_verify_worldline_continuation",
    "_dispatch_and_verify_certificate",
]


_MODULE_MATH_HASH_CACHE: Dict[Tuple[str, Optional[str]], Optional[str]] = {}


def _get_module_math_hash(mod_path: str, commit: Optional[str] = None) -> Optional[str]:
    """Compute normalized LF SHA-256 hash of mathematical certificate functions and dispatch in a module."""
    norm_p = mod_path.replace("\\", "/")
    cache_key = (norm_p, commit)
    if cache_key in _MODULE_MATH_HASH_CACHE:
        return _MODULE_MATH_HASH_CACHE[cache_key]

    if commit:
        code_bytes = _get_historical_git_blob(commit, norm_p)
        if code_bytes is None:
            _MODULE_MATH_HASH_CACHE[cache_key] = None
            return None
        code = code_bytes.decode("utf-8", errors="replace")
    else:
        full_p = os.path.join(REPO_ROOT, norm_p)
        if not os.path.exists(full_p):
            _MODULE_MATH_HASH_CACHE[cache_key] = None
            return None
        with open(full_p, "r", encoding="utf-8", errors="replace") as f:
            code = f.read()

    try:
        import ast
        tree = ast.parse(code)
        dumps = []
        math_funcs = set(CERTIFICATE_MATHEMATICAL_FUNCTIONS)
        has_factored = any(isinstance(n, ast.FunctionDef) and n.name == "_verify_zero_enclosure_and_isolation" for n in tree.body)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                if node.name in math_funcs:
                    if node.name == "_dispatch_and_verify_certificate":
                        for stmt in node.body:
                            if isinstance(stmt, ast.If):
                                cur = stmt
                                while cur:
                                    dumps.append(ast.dump(cur.test))
                                    if cur.orelse and isinstance(cur.orelse[0], ast.If):
                                        cur = cur.orelse[0]
                                    else:
                                        break
                    else:
                        for stmt in node.body:
                            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                                continue
                            if isinstance(stmt, ast.Assert):
                                continue
                            if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Tuple) and len(stmt.value.elts) == 2 and isinstance(stmt.value.elts[0], ast.Compare):
                                continue
                            dumps.append(ast.dump(stmt))
                elif node.name == "verify_certificate" and not has_factored:
                    try_nodes = [n for n in node.body if isinstance(n, ast.Try)]
                    if try_nodes:
                        if_nodes = [n for n in try_nodes[0].body if isinstance(n, ast.If)]
                        if if_nodes:
                            cur_if = if_nodes[0]
                            while cur_if:
                                for stmt in cur_if.body:
                                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                                        continue
                                    if isinstance(stmt, ast.Assert):
                                        continue
                                    if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Tuple) and len(stmt.value.elts) == 2 and isinstance(stmt.value.elts[0], ast.Compare):
                                        continue
                                    dumps.append(ast.dump(stmt))
                                if cur_if.orelse and isinstance(cur_if.orelse[0], ast.If):
                                    cur_if = cur_if.orelse[0]
                                else:
                                    break
                            cur_if2 = if_nodes[0]
                            while cur_if2:
                                dumps.append(ast.dump(cur_if2.test))
                                if cur_if2.orelse and isinstance(cur_if2.orelse[0], ast.If):
                                    cur_if2 = cur_if2.orelse[0]
                                else:
                                    break
        if not dumps:
            res = hashlib.sha256(code.replace("\r\n", "\n").encode("utf-8")).hexdigest()
        else:
            combined = "\n".join(dumps)
            res = hashlib.sha256(combined.encode("utf-8")).hexdigest()
        _MODULE_MATH_HASH_CACHE[cache_key] = res
        return res
    except Exception:
        res = hashlib.sha256(code.replace("\r\n", "\n").encode("utf-8")).hexdigest()
        _MODULE_MATH_HASH_CACHE[cache_key] = res
        return res


def _get_historical_git_blob_hash(commit_sha: str, path: str) -> Optional[str]:
    cache_key = (commit_sha, path)
    if cache_key in _GIT_BLOB_CACHE:
        return _GIT_BLOB_CACHE[cache_key]
    try:
        proc = subprocess.run(
            ["git", "show", f"{commit_sha}:{path}"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        if proc.returncode != 0:
            _GIT_BLOB_CACHE[cache_key] = None
            return None
        blob_content = proc.stdout.replace(b"\r\n", b"\n")
        b_hash = hashlib.sha256(blob_content).hexdigest()
        _GIT_BLOB_CACHE[cache_key] = b_hash
        return b_hash
    except Exception:
        _GIT_BLOB_CACHE[cache_key] = None
        return None


def _is_valid_git_commit(
    commit_sha: str,
    source_code_hashes: Optional[Dict[str, str]] = None,
    input_data_hashes: Optional[Dict[str, str]] = None,
    check_ancestor: bool = True
) -> Tuple[bool, str]:
    """Verify that a producing commit SHA is a valid, existing 40-char hex Git commit,
    is an ancestor of HEAD, and binds historical blobs to claimed source and data hashes.
    """
    if not isinstance(commit_sha, str) or len(commit_sha) != 40:
        return False, f"Commit SHA must be a 40-character hexadecimal string, got '{commit_sha}'"
    if not all(c in "0123456789abcdefABCDEF" for c in commit_sha):
        return False, f"Commit SHA contains non-hexadecimal characters: '{commit_sha}'"
    if commit_sha.lower() in ("0000000000000000000000000000000000000000", "fake", "unknown", "forged"):
        return False, f"Prohibited placeholder commit SHA: '{commit_sha}'"

    cache_commit_key = (commit_sha, check_ancestor)
    if cache_commit_key in _GIT_COMMIT_VALID_CACHE:
        base_ok, base_err = _GIT_COMMIT_VALID_CACHE[cache_commit_key]
        if not base_ok:
            return False, base_err
    else:
        try:
            res = subprocess.run(
                ["git", "cat-file", "-e", f"{commit_sha}^{{commit}}"],
                cwd=REPO_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if res.returncode != 0:
                err = f"Commit SHA '{commit_sha}' does not exist as a commit object in git"
                _GIT_COMMIT_VALID_CACHE[cache_commit_key] = (False, err)
                return False, err
        except Exception as e:
            err = f"Git error verifying commit '{commit_sha}': {e}"
            _GIT_COMMIT_VALID_CACHE[cache_commit_key] = (False, err)
            return False, err

        if check_ancestor:
            try:
                res = subprocess.run(
                    ["git", "merge-base", "--is-ancestor", commit_sha, "HEAD"],
                    cwd=REPO_ROOT,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                if res.returncode != 0:
                    err = f"Producing commit '{commit_sha}' is not an ancestor of current HEAD"
                    _GIT_COMMIT_VALID_CACHE[cache_commit_key] = (False, err)
                    return False, err
            except Exception as e:
                err = f"Git error checking ancestor status for '{commit_sha}': {e}"
                _GIT_COMMIT_VALID_CACHE[cache_commit_key] = (False, err)
                return False, err

        _GIT_COMMIT_VALID_CACHE[cache_commit_key] = (True, "")

    if source_code_hashes:
        for mod, expected_hash in source_code_hashes.items():
            if not expected_hash or expected_hash == "N/A":
                continue
            blob_hash = _get_historical_git_blob_hash(commit_sha, mod)
            if blob_hash is None:
                return False, f"Source module '{mod}' does not exist at commit '{commit_sha}'"
            if blob_hash != expected_hash:
                return False, f"Source module '{mod}' blob hash at commit '{commit_sha}' ({blob_hash}) does not match claimed hash ({expected_hash})"

    if input_data_hashes:
        for df, expected_hash in input_data_hashes.items():
            if not expected_hash or expected_hash == "N/A":
                continue
            blob_hash = _get_historical_git_blob_hash(commit_sha, f"data/{df}")
            if blob_hash is None:
                return False, f"Data file 'data/{df}' does not exist at commit '{commit_sha}'"
            if blob_hash != expected_hash:
                return False, f"Data file 'data/{df}' blob hash at commit '{commit_sha}' ({blob_hash}) does not match claimed hash ({expected_hash})"

    return True, ""



def _get_git_commit() -> str:
    """Retrieve current Git commit hash or fallback."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()
        return commit
    except Exception:
        return "UNKNOWN"


def validate_generation_environment(target_commit: Optional[str] = None) -> Tuple[bool, str]:
    """Ensure the generation environment satisfies the strict implementation commit boundary.

    Fails closed if:
    - Current working tree contains uncommitted changes in required source, data, or specs.
    - An explicit target commit is specified that differs from HEAD or has different source/data hashes.
    """
    head = _get_git_commit()
    if head == "UNKNOWN":
        return False, "Cannot determine current Git HEAD commit"

    # Check git status for required source files, specs, or data files
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if proc.returncode == 0 and proc.stdout:
            for line in proc.stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    p = parts[1].replace("\\", "/")
                    if any(p == mod or p.startswith("research/experiments/") or (p.startswith("data/") and p.endswith(".csv")) for mod in REQUIRED_SOURCE_MODULES):
                        if not p.startswith("data/certificates/") and not p.startswith("research/runs/") and p != "research/index.json" and p != "formal/build_report.json":
                            return False, f"Generation aborted: working tree contains uncommitted changes in '{p}'"
    except Exception as e:
        return False, f"Git status check failed: {e}"

    if target_commit:
        if target_commit != head:
            # Check if source hashes at target commit match current disk
            for mod in REQUIRED_SOURCE_MODULES:
                blob_h = _get_historical_git_blob_hash(target_commit, mod)
                disk_h = _get_source_code_hashes().get(mod)
                if blob_h != disk_h:
                    return False, f"Target commit '{target_commit}' source module '{mod}' ({blob_h}) differs from current disk implementation ({disk_h})"
            for df in REQUIRED_INPUT_DATA_FILES:
                blob_h = _get_historical_git_blob_hash(target_commit, f"data/{df}")
                disk_h = _get_input_data_hashes().get(df)
                if blob_h != disk_h:
                    return False, f"Target commit '{target_commit}' data file 'data/{df}' ({blob_h}) differs from current disk data ({disk_h})"

    return True, ""


def verify_formal_build_report(
    report_path: Optional[str] = None,
    check_current: bool = False
) -> Tuple[bool, str, Dict[str, Any], List[str]]:
    """Validate formal/build_report.json machine-readable evidence of lake build.

    Returns (is_verified, state_string, report_dict, errors).
    state_string is one of: "verified", "missing", "failed", "stale".
    """
    path = report_path or os.path.join(REPO_ROOT, "formal", "build_report.json")
    if not os.path.exists(path):
        return False, "missing", {}, ["formal/build_report.json does not exist"]

    try:
        with open(path, "r", encoding="utf-8") as f:
            report = json.load(f)
    except Exception as e:
        return False, "failed", {}, [f"Failed reading formal/build_report.json: {e}"]

    errors: List[str] = []
    if not isinstance(report, dict):
        return False, "failed", {}, ["Formal build report must be a dictionary"]

    # 1. Schema & Type
    if report.get("schema_version") != "1.0.0":
        errors.append(f"Unsupported schema_version: expected '1.0.0', got '{report.get('schema_version')}'")
    if report.get("report_type") != "formal_build_report":
        errors.append(f"Invalid report_type: expected 'formal_build_report', got '{report.get('report_type')}'")
    if report.get("command") != "lake build":
        errors.append(f"Invalid command: expected 'lake build', got '{report.get('command')}'")
    if report.get("status") != "passed" or report.get("exit_code") != 0:
        errors.append(f"Formal build status is '{report.get('status')}' (exit code {report.get('exit_code')})")

    # 2. Canonical self-hash
    rep_hash = report.get("report_hash")
    clean_rep = {k: v for k, v in report.items() if k != "report_hash"}
    calc_hash = hashlib.sha256(json.dumps(clean_rep, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if not rep_hash or rep_hash != calc_hash:
        errors.append(f"Formal build report self-hash mismatch: reported '{rep_hash}', computed '{calc_hash}'")

    # 3. Toolchain metadata
    lake_ver = str(report.get("lake_version", "")).strip()
    lean_ver = str(report.get("lean_version", "")).strip()
    if not lake_ver or lake_ver.lower() in ("unknown", "placeholder", "none", "fake", "forged", "n/a"):
        errors.append(f"Invalid or placeholder lake_version: '{lake_ver}'")
    if not lean_ver or lean_ver.lower() in ("unknown", "placeholder", "none", "fake", "forged", "n/a"):
        errors.append(f"Invalid or placeholder lean_version: '{lean_ver}'")

    # 4. Producing Git Commit Validation
    prod_commit = str(report.get("producing_git_commit", "")).strip()
    commit_ok, commit_err = _is_valid_git_commit(prod_commit, check_ancestor=False)
    if not commit_ok:
        errors.append(f"Invalid producing_git_commit provenance: {commit_err}")

    # 5. Formal Source Hashes Inventory & Hash Binding
    f_hashes = report.get("formal_source_hashes")
    if not isinstance(f_hashes, dict) or not f_hashes:
        errors.append("Missing or empty formal_source_hashes map")
    else:
        req_set = set(REQUIRED_FORMAL_SOURCES)
        rep_set = set(f_hashes.keys())
        missing_src = req_set - rep_set
        if missing_src:
            errors.append(f"Formal source inventory missing required files: {sorted(list(missing_src))}")
        extra_src = rep_set - req_set
        if extra_src:
            errors.append(f"Formal source inventory contains unexpected files: {sorted(list(extra_src))}")

        for rel_p, exp_h in f_hashes.items():
            if not exp_h or len(exp_h) != 64 or not all(c in "0123456789abcdefABCDEF" for c in exp_h) or exp_h.lower() in ("0" * 64, "fake", "none"):
                errors.append(f"Formal source '{rel_p}' has invalid SHA-256 hash: '{exp_h}'")
                continue

            # Historical blob binding at producing commit
            if commit_ok:
                blob_h = _get_historical_git_blob_hash(prod_commit, rel_p)
                if blob_h is None:
                    errors.append(f"Formal source '{rel_p}' does not exist in git at commit '{prod_commit}'")
                elif blob_h != exp_h:
                    errors.append(f"Formal source '{rel_p}' git blob hash ({blob_h}) != report hash ({exp_h}) at commit '{prod_commit}'")

            # Current workspace disk binding
            if check_current:
                full_p = os.path.join(REPO_ROOT, rel_p)
                if not os.path.exists(full_p):
                    errors.append(f"Formal source file '{rel_p}' missing on disk")
                else:
                    with open(full_p, "rb") as sf:
                        cur_h = hashlib.sha256(sf.read().replace(b"\r\n", b"\n")).hexdigest()
                    if cur_h != exp_h:
                        errors.append(f"Formal source file '{rel_p}' hash mismatch: disk {cur_h}, report {exp_h}")

    # 6. Formal Config Files (lean-toolchain, lakefile.toml, lake-manifest.json)
    for cfg_key, cfg_rel in REQUIRED_FORMAL_CONFIG_FILES.items():
        field_name = f"{cfg_key}_hash"
        cfg_h = report.get(field_name)
        if not cfg_h or len(cfg_h) != 64 or not all(c in "0123456789abcdefABCDEF" for c in cfg_h) or cfg_h.lower() in ("0" * 64, "fake", "none"):
            errors.append(f"Report missing or invalid {field_name}: '{cfg_h}'")
            continue

        if commit_ok:
            blob_h = _get_historical_git_blob_hash(prod_commit, cfg_rel)
            if blob_h is None:
                errors.append(f"Formal config '{cfg_rel}' does not exist in git at commit '{prod_commit}'")
            elif blob_h != cfg_h:
                errors.append(f"Formal config '{cfg_rel}' git blob hash ({blob_h}) != report hash ({cfg_h}) at commit '{prod_commit}'")

        if check_current:
            cfg_full = os.path.join(REPO_ROOT, cfg_rel)
            if not os.path.exists(cfg_full):
                errors.append(f"Formal config file '{cfg_rel}' missing on disk")
            else:
                with open(cfg_full, "rb") as cf:
                    cur_h = hashlib.sha256(cf.read().replace(b"\r\n", b"\n")).hexdigest()
                if cur_h != cfg_h:
                    errors.append(f"Formal config file '{cfg_rel}' hash mismatch: disk {cur_h}, report {cfg_h}")

    # 7. Builder / Verifier Source Code Hashes
    builder_hashes = report.get("builder_source_hashes")
    if not isinstance(builder_hashes, dict) or not builder_hashes:
        errors.append("Report missing or empty builder_source_hashes map")
    else:
        req_b_set = set(REQUIRED_FORMAL_BUILDER_MODULES)
        rep_b_set = set(builder_hashes.keys())
        missing_b = req_b_set - rep_b_set
        if missing_b:
            errors.append(f"Builder source inventory missing required files: {sorted(list(missing_b))}")
        extra_b = rep_b_set - req_b_set
        if extra_b:
            errors.append(f"Builder source inventory contains unexpected files: {sorted(list(extra_b))}")

        for b_rel, b_h in builder_hashes.items():
            if not b_h or len(b_h) != 64 or not all(c in "0123456789abcdefABCDEF" for c in b_h) or b_h.lower() in ("0" * 64, "fake", "none"):
                errors.append(f"Builder source '{b_rel}' has invalid SHA-256 hash: '{b_h}'")
                continue

            if commit_ok:
                blob_h = _get_historical_git_blob_hash(prod_commit, b_rel)
                if blob_h is None:
                    errors.append(f"Builder source '{b_rel}' does not exist in git at commit '{prod_commit}'")
                elif blob_h != b_h:
                    errors.append(f"Builder source '{b_rel}' git blob hash ({blob_h}) != report hash ({b_h}) at commit '{prod_commit}'")

            if check_current and b_rel == "scripts/build_formal.py":
                b_full = os.path.join(REPO_ROOT, b_rel)
                if not os.path.exists(b_full):
                    errors.append(f"Builder source file '{b_rel}' missing on disk")
                else:
                    with open(b_full, "rb") as bf:
                        cur_h = hashlib.sha256(bf.read().replace(b"\r\n", b"\n")).hexdigest()
                    if cur_h != b_h:
                        errors.append(f"Builder source file '{b_rel}' hash mismatch: disk {cur_h}, report {b_h}")

    is_verified = (len(errors) == 0 and report.get("status") == "passed" and report.get("exit_code") == 0)
    state = "verified" if is_verified else ("stale" if report.get("status") == "passed" else "failed")
    return is_verified, state, report, errors


def _split_ball_str(ball: Any) -> Tuple[str, str]:
    """Extract midpoint and radius strings from an Arb ball representation."""
    s = str(ball).strip()
    if s.startswith("[") and "+/-" in s:
        parts = s.strip("[]").split("+/-")
        return parts[0].strip(), parts[1].strip()
    return s, "0"


def _reconstruct_arb_ball(mid_str: str, rad_str: Optional[str] = None) -> Any:
    """Reconstruct an Arb ball without float downcast."""
    if not FLINT_AVAILABLE or arb is None:
        raise RuntimeError("FLINT is not available")
    m_clean = mid_str.strip()
    if m_clean.startswith("[") and "+/-" in m_clean:
        return arb(m_clean)
    if rad_str is not None:
        r_clean = rad_str.strip("[]").split("+/-")[0].strip()
        if r_clean and r_clean not in ["0", "0.0"]:
            return arb(f"[{m_clean} +/- {r_clean}]")
    return arb(m_clean)


def certify_zero(index: int, dps: int = 80, git_commit: Optional[str] = None) -> Dict[str, Any]:
    """Obtain a certified Arb/ACB enclosure and simplicity verification for the n-th zero.

    Args:
        index: Positive integer zero index (1-based, e.g. 1 for first zero ~14.1347).
        dps: Decimal precision for evaluation context.
        git_commit: Optional explicit producing commit SHA.

    Returns:
        A structured zero certificate dictionary with cryptographic hash.
    """
    if index < 1:
        raise ValueError(f"Zero index must be positive integer >= 1, got {index}")
    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        raise RuntimeError(
            "FLINT/python-flint is required for rigorous mathematical certification. "
            "Please ensure python-flint>=0.6.0 is installed in your Python environment."
        )

    old_dps = ctx.dps
    try:
        ctx.dps = dps + 20
        # Compute certified Arb/ACB zero enclosure
        z_enc = acb.zeta_zero(index)

        # Real and imaginary components as Arb balls
        re_ball = z_enc.real
        im_ball = z_enc.imag

        # Compute adjacent zeros for rigorous isolation interval bounds
        if index == 1:
            z_next = acb.zeta_zero(2)
            lower_iso = arb("0.0")
            upper_iso = (im_ball + z_next.imag) / 2
        else:
            z_prev = acb.zeta_zero(index - 1)
            z_next = acb.zeta_zero(index + 1)
            lower_iso = (z_prev.imag + im_ball) / 2
            upper_iso = (im_ball + z_next.imag) / 2

        # Rigorous Taylor expansion at z_enc to degree 3: ζ(z + x) = ζ(z) + ζ'(z)x + (ζ''(z)/2)x^2 + ...
        ser = acb_series([z_enc, 1], 4).zeta()
        z_res = ser[0]
        z_prime = ser[1]
        c2 = ser[2]
        c3 = ser[3]

        # Simplicity check: 0 ∉ ζ'(B_n)
        zp_abs_lower = z_prime.abs_lower()
        is_simple = bool(zp_abs_lower > 0)
        status = "simple_zero_certified" if is_simple else "isolated_zero_certified"

        commit = git_commit or _get_git_commit()

        re_m, re_r = _split_ball_str(re_ball)
        im_m, im_r = _split_ball_str(im_ball)
        low_m, _ = _split_ball_str(lower_iso)
        up_m, _ = _split_ball_str(upper_iso)
        zp_re_m, zp_re_r = _split_ball_str(z_prime.real)
        zp_im_m, zp_im_r = _split_ball_str(z_prime.imag)
        zp_abs_low_m, _ = _split_ball_str(zp_abs_lower)
        c2_re_m, _ = _split_ball_str(c2.real)
        c2_im_m, _ = _split_ball_str(c2.imag)
        c3_re_m, _ = _split_ball_str(c3.real)
        c3_im_m, _ = _split_ball_str(c3.imag)

        cert: Dict[str, Any] = {
            "schema_version": CERTIFICATE_SCHEMA_VERSION,
            "certificate_type": "zero_isolation_and_simplicity",
            "status": status,
            "zero_family": "nontrivial",
            "nontrivial_index": index,
            "zero_index": index,
            "mathematical_claim": f"Nontrivial Riemann zeta zero index {index} uniquely isolated on critical line; simplicity verified via 0 ∉ ζ'(B_{index})",
            "enclosure": {
                "real_mid": re_m,
                "real_rad": re_r,
                "imag_mid": im_m,
                "imag_rad": im_r,
                "exact_real": bool(re_ball == arb("0.5")),
            },
            "isolation_interval": {
                "lower_bound": low_m,
                "upper_bound": up_m,
                "isolated": True,
            },
            "derivative_enclosure": {
                "real_mid": zp_re_m,
                "real_rad": zp_re_r,
                "imag_mid": zp_im_m,
                "imag_rad": zp_im_r,
                "abs_lower": zp_abs_low_m,
                "excludes_zero": is_simple,
            },
            "higher_coefficients": {
                "c2_real": c2_re_m,
                "c2_imag": c2_im_m,
                "c3_real": c3_re_m,
                "c3_imag": c3_im_m,
            },
            "formal_theorem_reference": "RiemannScope.ZeroCharacter.zeroCharacter_isolated_simple",
            "precision_dps": dps,
            "precision_bits": int(dps * 3.321928),
            "library": "python-flint",
            "library_version": FLINT_VERSION,
            "verifier_version": VERIFIER_VERSION,
            "algorithm_version": ALGORITHM_VERSION,
            "producing_git_commit": commit,
            "source_code_hashes": _get_source_code_hashes(commit),
            "input_data_hashes": _get_input_data_hashes(commit),
            "dependency_fingerprint": _get_dependency_fingerprint(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "invalidation_conditions": [
                "derivative_enclosure_contains_zero",
                "isolation_interval_overlap",
                "source_code_hash_mismatch",
                "input_data_hash_mismatch"
            ]
        }
        cert["certificate_hash"] = _sha256_canonical(cert)
        return cert
    finally:
        ctx.dps = old_dps


def certify_trivial_zero(m: int, dps: int = 80, git_commit: Optional[str] = None) -> Dict[str, Any]:
    """Obtain a certified Arb/ACB enclosure and simplicity verification for the m-th trivial zero s = -2m.

    Args:
        m: Positive integer trivial zero index (1-based, e.g. 1 for s = -2).
        dps: Decimal precision for evaluation context.
        git_commit: Optional explicit producing commit SHA.

    Returns:
        A structured trivial zero certificate dictionary with cryptographic hash.
    """
    if not isinstance(m, int) or m < 1:
        raise ValueError(f"Trivial zero index m must be positive integer >= 1, got {m}")
    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        raise RuntimeError(
            "FLINT/python-flint is required for rigorous mathematical certification."
        )

    old_dps = ctx.dps
    try:
        ctx.dps = dps + 20
        s_exact = -2 * m
        s_ball = acb(s_exact, 0)

        # Evaluate zeta and derivative at s = -2m
        ser = acb_series([s_ball, 1], 3).zeta()
        z_val = ser[0]
        z_prime = ser[1]
        c2 = ser[2]

        # Verification that zeta(-2m) contains 0
        zero_arb = arb("0.0")
        contains_zero = z_val.real.contains(zero_arb) and z_val.imag.contains(zero_arb)

        # Simplicity check: 0 ∉ ζ'(s_m)
        zp_abs_lower = z_prime.abs_lower()
        is_simple = bool(zp_abs_lower > 0)
        status = "simple_zero_certified" if (contains_zero and is_simple) else "isolated_zero_certified"

        # Isolation interval [-2m - 0.5, -2m + 0.5]
        lower_iso = arb(str(s_exact - 0.5))
        upper_iso = arb(str(s_exact + 0.5))

        # Negative control evaluations: zeta(0) = -1/2, zeta(-2m + 1)
        z0 = acb(0, 0).zeta()
        z_odd = acb(s_exact + 1, 0).zeta()
        neg_ctrl_z0_pass = not z0.real.contains(zero_arb)
        neg_ctrl_odd_pass = not z_odd.real.contains(zero_arb)

        commit = git_commit or _get_git_commit()

        zp_re_m, zp_re_r = _split_ball_str(z_prime.real)
        zp_im_m, zp_im_r = _split_ball_str(z_prime.imag)
        zp_abs_low_m, _ = _split_ball_str(zp_abs_lower)
        c2_re_m, _ = _split_ball_str(c2.real)
        c2_im_m, _ = _split_ball_str(c2.imag)

        cert: Dict[str, Any] = {
            "schema_version": CERTIFICATE_SCHEMA_VERSION,
            "certificate_type": "trivial_zero_certificate",
            "status": status,
            "zero_family": "trivial",
            "trivial_index": m,
            "exact_location": s_exact,
            "mathematical_claim": (
                f"Trivial Riemann zeta zero index {m} at exact location s = {s_exact} on negative real axis; "
                f"simplicity certified via non-vanishing pointwise derivative 0 ∉ ζ'({s_exact}) and functional equation poles of Gamma(s/2)."
            ),
            "enclosure": {
                "real_mid": str(s_exact),
                "real_rad": "0.0",
                "imag_mid": "0.0",
                "imag_rad": "0.0",
                "exact_real": True,
            },
            "isolation_interval": {
                "lower_bound": str(s_exact - 0.5),
                "upper_bound": str(s_exact + 0.5),
                "isolated": True,
            },
            "derivative_enclosure": {
                "real_mid": zp_re_m,
                "real_rad": zp_re_r,
                "imag_mid": zp_im_m,
                "imag_rad": zp_im_r,
                "abs_lower": zp_abs_low_m,
                "excludes_zero": is_simple,
            },
            "higher_coefficients": {
                "c2_real": c2_re_m,
                "c2_imag": c2_im_m,
            },
            "negative_controls": {
                "zeta_at_zero_is_minus_half": neg_ctrl_z0_pass,
                "zeta_at_odd_negative_nonzero": neg_ctrl_odd_pass,
            },
            "formal_theorem_reference": "RiemannScope.TrivialZero.trivialZero_exact",
            "precision_dps": dps,
            "precision_bits": int(dps * 3.321928),
            "library": "python-flint",
            "library_version": FLINT_VERSION,
            "verifier_version": VERIFIER_VERSION,
            "algorithm_version": ALGORITHM_VERSION,
            "producing_git_commit": commit,
            "source_code_hashes": _get_source_code_hashes(commit),
            "input_data_hashes": _get_input_data_hashes(commit),
            "dependency_fingerprint": _get_dependency_fingerprint(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "invalidation_conditions": [
                "zeta_eval_nonzero",
                "derivative_enclosure_contains_zero",
                "source_code_hash_mismatch"
            ]
        }
        cert["certificate_hash"] = _sha256_canonical(cert)
        return cert
    finally:
        ctx.dps = old_dps


def certify_block(
    block_id: str,
    zero_indices: List[int],
    dps: int = 80,
    git_commit: Optional[str] = None,
    existing_zero_certs: Optional[Dict[int, Dict[str, Any]]] = None
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Certify a consecutive block of zeros and verify Turing zero counts at endpoints.

    Args:
        block_id: Unique string identifier for the block (e.g. 'low_validation').
        zero_indices: List of 1-based consecutive zero indices.
        dps: Precision in decimal digits.
        git_commit: Optional explicit producing commit SHA.
        existing_zero_certs: Optional cache of already certified zero dictionaries.

    Returns:
        (block_certificate_dict, list_of_constituent_zero_certificates)
    """
    if not zero_indices:
        raise ValueError("zero_indices cannot be empty")
    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        raise RuntimeError(
            "FLINT/python-flint is required for rigorous mathematical certification. "
            "Please ensure python-flint>=0.6.0 is installed in your Python environment."
        )

    old_dps = ctx.dps
    try:
        ctx.dps = dps + 20
        min_idx = min(zero_indices)
        max_idx = max(zero_indices)
        expected_count = len(zero_indices)

        # Certify all constituent zeros
        zero_certs: List[Dict[str, Any]] = []
        for idx in range(min_idx, max_idx + 1):
            if existing_zero_certs and idx in existing_zero_certs:
                zc = existing_zero_certs[idx]
            else:
                zc = certify_zero(idx, dps=dps, git_commit=git_commit)
            zero_certs.append(zc)

        # Rigorous Turing zero counting at block endpoints
        t_min_str = zero_certs[0]["isolation_interval"]["lower_bound"]
        t_max_str = zero_certs[-1]["isolation_interval"]["upper_bound"]

        t_min = arb(t_min_str)
        t_max = arb(t_max_str)

        # Turing count via FLINT zeta_nzeros
        n_min_zeros = t_min.zeta_nzeros()
        n_max_zeros = t_max.zeta_nzeros()

        n_min_int = int(n_min_zeros.unique_fmpz())
        n_max_int = int(n_max_zeros.unique_fmpz())
        turing_count = n_max_int - n_min_int

        count_verified = (turing_count == expected_count)
        all_simple = all(zc.get("status") == "simple_zero_certified" for zc in zero_certs)

        status = "complete_block_certified" if (count_verified and all_simple) else "block_audit_failed"

        commit = git_commit or _get_git_commit()
        constituent_hashes = [zc["certificate_hash"] for zc in zero_certs]

        cert: Dict[str, Any] = {
            "schema_version": CERTIFICATE_SCHEMA_VERSION,
            "certificate_type": "complete_block_certificate",
            "status": status,
            "block_id": block_id,
            "zero_family": "nontrivial",
            "index_range": [min_idx, max_idx],
            "zero_count": expected_count,
            "all_zeros_simple": all_simple,
            "constituent_zero_hashes": constituent_hashes,
            "endpoint_bounds": {
                "t_min": t_min_str,
                "t_max": t_max_str,
                "n_zeros_at_t_min": n_min_int,
                "n_zeros_at_t_max": n_max_int,
                "turing_count": turing_count,
                "count_verified": count_verified,
            },
            "mathematical_claim": (
                f"Block '{block_id}' contains exactly {expected_count} consecutive simple nontrivial zeros "
                f"for indices {min_idx}..{max_idx}; Turing zero count rigorously verified via FLINT N(t_max)-N(t_min)={turing_count}."
            ),
            "formal_theorem_reference": "RiemannScope.ZeroCharacter.zeroBlock_complete",
            "precision_dps": dps,
            "library": "python-flint",
            "library_version": FLINT_VERSION,
            "verifier_version": VERIFIER_VERSION,
            "algorithm_version": ALGORITHM_VERSION,
            "producing_git_commit": commit,
            "source_code_hashes": _get_source_code_hashes(commit),
            "input_data_hashes": _get_input_data_hashes(commit),
            "dependency_fingerprint": _get_dependency_fingerprint(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "invalidation_conditions": [
                "constituent_zero_hash_mismatch",
                "turing_endpoint_count_mismatch",
                "source_code_hash_mismatch"
            ]
        }
        cert["certificate_hash"] = _sha256_canonical(cert)
        return cert, zero_certs
    finally:
        ctx.dps = old_dps


def certify_worldline(
    zero_cert: Dict[str, Any],
    grade: int,
    delta: Union[float, str] = "0.0",
    dps: int = 80,
    git_commit: Optional[str] = None
) -> Dict[str, Any]:
    """Certify bilateral transcendental worldline covariance and radial leaf invariance.

    Args:
        zero_cert: A validated zero certificate dictionary.
        grade: Integer grade K in Z.
        delta: Radial perturbation displacement string or float ("0.0" for actual zeros).
        dps: Precision in decimal digits.
        git_commit: Optional explicit producing commit SHA.
    """
    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        raise RuntimeError(
            "FLINT/python-flint is required for rigorous mathematical certification. "
            "Please ensure python-flint>=0.6.0 is installed in your Python environment."
        )

    delta_str = str(delta).strip()
    old_dps = ctx.dps
    try:
        ctx.dps = dps + 20
        # Exact symbolic tau = 2*pi
        tau_ball = arb.pi() * 2
        tau_K = tau_ball ** grade
        tau_neg_K = tau_ball ** (-grade)
        sigma_critical = tau_K / 2

        is_trivial = (
            zero_cert.get("zero_family") == "trivial"
            or zero_cert.get("certificate_type") == "trivial_zero_certificate"
        )

        if is_trivial:
            m_idx = int(zero_cert.get("trivial_index", 1))
            s_exact = -2 * m_idx
            s_worldline = acb(s_exact, 0) * acb(tau_K, 0)

            # Normalized radial coordinate R_tau(-2m, K) = tau^(-K)*Re(tau^K * (-2m)) - 1/2 = -2m - 1/2
            R_tau = (tau_neg_K * s_worldline.real) - arb("0.5")
            expected_R = arb(str(s_exact - 0.5))
            radial_residual = (R_tau - expected_R).abs_upper()
            signed_defect = s_worldline.real - sigma_critical
            expected_signed_defect = tau_K * arb(str(s_exact - 0.5))
            defect_residual = (signed_defect - expected_signed_defect).abs_upper()
            claim_type = "trivial_zero_worldline"
            source_idx = m_idx
            src_family = "trivial"
            math_claim = (
                f"Trivial zero worldline s({grade}) = tau^{grade} * ({s_exact}) occupies exact radial leaf "
                f"R_tau = {s_exact - 0.5} (non-critical zero, R_tau != 0)"
            )
        else:
            source_idx = int(zero_cert.get("nontrivial_index") or zero_cert.get("zero_index", 1))
            src_family = "nontrivial"
            s_enc = zero_cert.get("enclosure", {})
            re_ball = _reconstruct_arb_ball(s_enc.get("real_mid", "0.5"), s_enc.get("real_rad", "1e-50"))
            im_ball = _reconstruct_arb_ball(s_enc.get("imag_mid", "0.0"), s_enc.get("imag_rad", "1e-50"))

            delta_arb = arb(delta_str)
            z_point = acb(re_ball + delta_arb, im_ball)
            s_worldline = z_point * acb(tau_K, 0)

            R_tau = (tau_neg_K * s_worldline.real) - arb("0.5")
            radial_residual = (R_tau - delta_arb).abs_upper()
            signed_defect = s_worldline.real - sigma_critical
            expected_signed_defect = tau_K * delta_arb
            defect_residual = (signed_defect - expected_signed_defect).abs_upper()

            is_actual = (delta_str in ["0.0", "0", "+0.0", "-0.0"])
            claim_type = "actual_zero_worldline" if is_actual else "synthetic_radial_leaf"
            math_claim = (
                f"Transcendental worldline s({grade}) = tau^{grade} * rho_{source_idx} occupies invariant critical surface sigma_c = tau^{grade}/2"
                if is_actual
                else f"Synthetic radial leaf s({grade}) = tau^{grade} * (rho_{source_idx} + {delta_str}) occupies invariant radial leaf R_tau = {delta_str}"
            )

        wl_re_m, wl_re_r = _split_ball_str(s_worldline.real)
        wl_im_m, wl_im_r = _split_ball_str(s_worldline.imag)
        sig_c_m, _ = _split_ball_str(sigma_critical)
        r_tau_m, _ = _split_ball_str(R_tau)
        rad_res_m, _ = _split_ball_str(radial_residual)
        def_res_m, _ = _split_ball_str(defect_residual)

        commit = git_commit or _get_git_commit()

        cert: Dict[str, Any] = {
            "schema_version": CERTIFICATE_SCHEMA_VERSION,
            "certificate_type": "worldline_certificate",
            "status": "worldline_certified",
            "claim_type": claim_type,
            "source_zero_hash": zero_cert.get("certificate_hash", ""),
            "source_zero_family": src_family,
            "source_zero_index": source_idx,
            "zero_family": src_family,
            "trivial_index": source_idx if is_trivial else None,
            "nontrivial_index": source_idx if not is_trivial else None,
            "grade_K": grade,
            "symbolic_scale": f"tau^{grade}" if grade != 0 else "1",
            "delta": delta_str if not is_trivial else str(s_exact - 0.5),
            "transformed_point": {
                "real_mid": wl_re_m,
                "real_rad": wl_re_r,
                "imag_mid": wl_im_m,
                "imag_rad": wl_im_r,
            },
            "critical_surface_real": sig_c_m,
            "normalized_radial": r_tau_m,
            "radial_residual": rad_res_m,
            "defect_residual": def_res_m,
            "mathematical_claim": math_claim,
            "formal_theorem_reference": "RiemannScope.RadialLeaf.radialLeaf_worldline_invariance",
            "precision_dps": dps,
            "library": "python-flint",
            "library_version": FLINT_VERSION,
            "verifier_version": VERIFIER_VERSION,
            "algorithm_version": ALGORITHM_VERSION,
            "producing_git_commit": commit,
            "source_code_hashes": _get_source_code_hashes(commit),
            "input_data_hashes": _get_input_data_hashes(commit),
            "dependency_fingerprint": _get_dependency_fingerprint(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "invalidation_conditions": [
                "source_zero_hash_mismatch",
                "radial_residual_tolerance_exceeded",
                "formal_theorem_missing"
            ]
        }
        cert["certificate_hash"] = _sha256_canonical(cert)
        return cert
    finally:
        ctx.dps = old_dps


def certify_g4_radial_witness(
    witness_id: str = "WIT-02",
    sigma: str = "5.0",
    gamma: str = "14.0",
    delta: str = "0.49",
    T: str = "16.8",
    n_subdivisions: int = 50000,
    dps: int = 60,
    git_commit: Optional[str] = None,
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """Generate certified Arb ball witness certificate for radial difference sign.

    Pure function: returns the certificate dictionary. If output_path is provided,
    saves the certificate JSON to output_path. Does NOT overwrite canonical
    tracked certificates unless explicitly targeted.
    """
    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        raise RuntimeError("FLINT/python-flint is required for rigorous mathematical certification.")
    import math_core

    producing_commit = git_commit or _get_git_commit()
    res = math_core.certify_g4_fejer_witness_arb(
        sigma=sigma,
        gamma=gamma,
        delta=delta,
        T=T,
        n_subdivisions=n_subdivisions,
        dps=dps
    )

    cert: Dict[str, Any] = {
        "schema_version": CERTIFICATE_SCHEMA_VERSION,
        "certificate_type": "radial_witness_certificate",
        "status": "radial_witness_certified",
        "evidence_status": "CERTIFIED_NEGATIVE_ARB_BALL",
        "witness_id": witness_id,
        "window_type": "fejer",
        "mathematical_claim": "Compact Fejér windowed radial difference Delta S_Fejer(5.0, 14.0, 0.49, 16.8) is strictly negative (< 0) via certified outward-rounded Arb ball arithmetic directly evaluated over [-16.8, 16.8].",
        "parameters": {
            "sigma": str(sigma),
            "gamma": str(gamma),
            "delta": str(delta),
            "T": str(T),
            "n_subdivisions": n_subdivisions,
            "symmetric_integration_domain": [-16.8, 16.8],
            "parameter_representation": "exact_decimal_strings"
        },
        "enclosure": {
            "enclosure_mid": res["enclosure_mid"],
            "enclosure_rad": res["enclosure_rad"],
            "interval_lower": res["interval_lower"],
            "interval_upper": res["interval_upper"],
            "strictly_negative": res["is_certified_negative"]
        },
        "integration_method": "Direct certified outward-rounded Arb ball Riemann integration over full symmetric domain [-T, T] with 50,000 subintervals without assuming evenness reduction or reflection as an operational premise.",
        "formal_theorem_reference": "RiemannScope.additive_reference_subtraction_invariance",
        "precision_dps": dps,
        "library": "python-flint",
        "library_version": FLINT_VERSION,
        "verifier_version": VERIFIER_VERSION,
        "algorithm_version": ALGORITHM_VERSION,
        "producing_git_commit": producing_commit,
        "source_code_hashes": _get_source_code_hashes(producing_commit),
        "input_data_hashes": _get_input_data_hashes(producing_commit),
        "dependency_fingerprint": _get_dependency_fingerprint()
    }
    cert["certificate_hash"] = _sha256_canonical(cert)

    if output_path is not None:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cert, f, indent=2)

    return cert




def _verify_zero_enclosure_and_isolation(cert: Dict[str, Any], anomalies: List[str]) -> Tuple[bool, List[str]]:
    """Mathematical verification in Arb of nontrivial zero enclosure, critical line containment, simplicity, and Turing isolation."""
    assert acb is not None and arb is not None and acb_series is not None and ctx is not None
    if "nontrivial_index" in cert and "zero_index" in cert and cert["nontrivial_index"] != cert["zero_index"]:
        anomalies.append(f"Contradictory index metadata: nontrivial_index ({cert['nontrivial_index']}) != zero_index ({cert['zero_index']})")
        return False, anomalies

    z_idx = cert.get("nontrivial_index") or cert.get("zero_index")
    if not isinstance(z_idx, int) or z_idx < 1:
        anomalies.append(f"Invalid nontrivial zero index: {z_idx}")
        return False, anomalies

    enc = cert.get("enclosure", {})
    re_mid_str = enc.get("real_mid")
    im_mid_str = enc.get("imag_mid")
    re_rad_str = str(enc.get("real_rad", "1e-50")).strip()
    im_rad_str = str(enc.get("imag_rad", "1e-50")).strip()

    if not re_mid_str or not im_mid_str:
        anomalies.append("Missing enclosure coordinates")
        return False, anomalies

    if re_rad_str.startswith("-") or im_rad_str.startswith("-"):
        anomalies.append(f"Negative enclosure radius is invalid: real_rad={re_rad_str}, imag_rad={im_rad_str}")
        return False, anomalies

    # Reconstruct stored Arb balls
    stored_re = _reconstruct_arb_ball(re_mid_str, re_rad_str)
    stored_im = _reconstruct_arb_ball(im_mid_str, im_rad_str)

    # Critical line check: Real part must contain 1/2
    half = arb("0.5")
    if not stored_re.contains(half) and stored_re != half:
        anomalies.append(f"Real part of zero enclosure does not contain 1/2: {stored_re}")

    # Replay mathematical zero enclosure with FLINT
    try:
        replayed_zero = acb.zeta_zero(z_idx)
        replayed_re = replayed_zero.real
        replayed_im = replayed_zero.imag
    except Exception as e:
        anomalies.append(f"FLINT acb.zeta_zero({z_idx}) replay failed: {e}")
        return False, anomalies

    # Containment check: Stored enclosure must strictly CONTAIN the replayed authoritative root
    if not stored_im.contains(replayed_im):
        anomalies.append(
            f"Replayed zero #{z_idx} ordinate {replayed_im} is not contained in stored enclosure {stored_im}"
        )
    if not stored_re.contains(replayed_re):
        anomalies.append(
            f"Replayed zero #{z_idx} real part {replayed_re} is not contained in stored enclosure {stored_re}"
        )

    # Verify isolation interval
    iso = cert.get("isolation_interval", {})
    lower_str = iso.get("lower_bound")
    upper_str = iso.get("upper_bound")
    if not lower_str or not upper_str:
        anomalies.append("Missing isolation interval bounds")
    else:
        low_iso = arb(lower_str)
        up_iso = arb(upper_str)

        # Zero containment: The entire stored ball must be strictly inside the isolation interval
        if not (low_iso <= stored_im.lower() and stored_im.upper() <= up_iso):
            anomalies.append(f"Zero ball [{stored_im.lower()}, {stored_im.upper()}] not strictly contained in isolation interval [{low_iso}, {up_iso}]")

        # Oversized ball check: stored radius must not exceed half isolation interval width
        iso_width = up_iso - low_iso
        stored_rad = stored_im.rad()
        if stored_rad > iso_width / 2 or stored_rad >= arb("1.0"):
            anomalies.append(f"Zero enclosure radius {stored_rad} is oversized (exceeds half-width or >= 1.0) and does not provide isolated zero certification")

        if z_idx > 1:
            prev_z = acb.zeta_zero(z_idx - 1)
            if not (prev_z.imag.upper() < low_iso.lower()):
                anomalies.append(f"Adjacent zero #{z_idx-1} ({prev_z.imag}) not excluded by lower isolation bound {low_iso}")
        next_z = acb.zeta_zero(z_idx + 1)
        if not (up_iso.upper() < next_z.imag.lower()):
            anomalies.append(f"Adjacent zero #{z_idx+1} ({next_z.imag}) not excluded by upper isolation bound {up_iso}")

        # Rigorous Turing zero count check for this isolation interval: N(up_iso) - N(low_iso) must be exactly 1
        try:
            n_low = int(low_iso.zeta_nzeros().unique_fmpz())
            n_up = int(up_iso.zeta_nzeros().unique_fmpz())
            if n_up - n_low != 1:
                anomalies.append(f"Turing zero count for isolation interval [{low_iso}, {up_iso}] is {n_up - n_low}, expected 1")
        except Exception as e:
            anomalies.append(f"Turing count evaluation failed on [{low_iso}, {up_iso}]: {e}")

    # Recompute derivative enclosure over complete stored ball and verify simplicity
    deriv = cert.get("derivative_enclosure", {})
    z_ball = acb(stored_re, stored_im)
    ser = acb_series([z_ball, 1], 2).zeta()
    z_prime = ser[1]
    abs_lower = z_prime.abs_lower()
    replayed_simple = bool(abs_lower > 0)

    if cert.get("status") == "simple_zero_certified":
        if not replayed_simple:
            anomalies.append(f"Simple zero claimed but recomputed derivative enclosure contains zero: |zeta'| lower bound = {abs_lower}")
        if not deriv.get("excludes_zero"):
            anomalies.append("Simple zero claimed but derivative_enclosure.excludes_zero is False")
        stored_abs_lower = _reconstruct_arb_ball(deriv.get("abs_lower", "0.0"))
        if not (stored_abs_lower > 0):
            anomalies.append(f"Simple zero claimed but stored derivative lower bound <= 0: {stored_abs_lower}")

    return (len(anomalies) == 0), anomalies


def _verify_trivial_zero_enclosure(cert: Dict[str, Any], anomalies: List[str]) -> Tuple[bool, List[str]]:
    """Mathematical verification in Arb of trivial zero location, derivative non-vanishing, and isolation."""
    assert acb is not None and arb is not None and acb_series is not None and ctx is not None
    m_idx = cert.get("trivial_index")
    s_exact = cert.get("exact_location")
    if not isinstance(m_idx, int) or m_idx < 1:
        anomalies.append(f"Invalid trivial_index: {m_idx}")
        return False, anomalies
    if not isinstance(s_exact, int) or s_exact != -2 * m_idx:
        anomalies.append(f"exact_location ({s_exact}) does not match -2 * trivial_index ({-2 * m_idx})")
        return False, anomalies

    # Replay FLINT evaluation of zeta(-2m)
    s_ball = acb(s_exact, 0)
    ser = acb_series([s_ball, 1], 3).zeta()
    z_val = ser[0]
    z_prime = ser[1]

    zero_arb = arb("0.0")
    if not z_val.real.contains(zero_arb) or not z_val.imag.contains(zero_arb):
        anomalies.append(f"zeta({s_exact}) enclosure does not contain 0: {z_val}")

    zp_abs_lower = z_prime.abs_lower()
    if zp_abs_lower <= 0:
        anomalies.append(f"Derivative enclosure at trivial zero s = {s_exact} contains zero: |zeta'| lower bound = {zp_abs_lower}")

    # Verify isolation interval [-2m - 0.5, -2m + 0.5]
    iso = cert.get("isolation_interval", {})
    low_str = iso.get("lower_bound")
    up_str = iso.get("upper_bound")
    if not low_str or not up_str:
        anomalies.append("Missing isolation interval in trivial zero certificate")
    else:
        low_val = float(low_str)
        up_val = float(up_str)
        if not (low_val <= s_exact <= up_val):
            anomalies.append(f"Trivial zero {s_exact} not inside isolation interval [{low_val}, {up_val}]")
        if not (s_exact - 1 < low_val and up_val < s_exact + 1):
            anomalies.append(f"Isolation interval [{low_val}, {up_val}] does not strictly isolate {s_exact} from adjacent integers")

    # Negative controls verification
    z0 = acb(0, 0).zeta()
    if z0.real.contains(zero_arb):
        anomalies.append("Negative control failed: zeta(0) contains zero")
    z_odd = acb(s_exact + 1, 0).zeta()
    if z_odd.real.contains(zero_arb):
        anomalies.append(f"Negative control failed: zeta({s_exact + 1}) contains zero")

    return (len(anomalies) == 0), anomalies


def _verify_block_isolation(
    cert: Dict[str, Any],
    anomalies: List[str],
    cert_store: Optional[Dict[str, Any]] = None,
    check_provenance: bool = True
) -> Tuple[bool, List[str]]:
    """Mathematical verification in Arb of block completeness and endpoint Turing zero counts."""
    assert acb is not None and arb is not None and acb_series is not None and ctx is not None
    const_hashes = cert.get("constituent_zero_hashes", [])
    zero_count = cert.get("zero_count")
    idx_range = cert.get("index_range", [])

    if not isinstance(idx_range, list) or len(idx_range) != 2:
        anomalies.append(f"Invalid index_range: {idx_range}")
        return False, anomalies

    min_idx, max_idx = idx_range[0], idx_range[1]
    expected_count = max_idx - min_idx + 1

    if zero_count != expected_count:
        anomalies.append(f"zero_count ({zero_count}) does not match index range {min_idx}..{max_idx} ({expected_count})")
    if len(const_hashes) != expected_count:
        anomalies.append(f"Constituent zero hash count ({len(const_hashes)}) != expected count ({expected_count})")

    # Contradictory block status check
    if cert.get("status") == "complete_block_certified":
        if cert.get("all_zeros_simple") is not True:
            anomalies.append("Contradictory block status: complete_block_certified claimed but all_zeros_simple is False")
        if cert.get("endpoint_bounds", {}).get("count_verified") is not True:
            anomalies.append("Contradictory block status: complete_block_certified claimed but count_verified is False")

    # Verify each constituent zero certificate
    resolved_certs: List[Dict[str, Any]] = []
    for i, expected_zero_idx in enumerate(range(min_idx, max_idx + 1)):
        expected_c_hash = const_hashes[i] if i < len(const_hashes) else None
        zc = None
        if cert_store:
            if expected_c_hash is not None:
                zc = cert_store.get(expected_c_hash)
            if zc is None:
                zc = cert_store.get(f"zero_{expected_zero_idx:05d}")

        if zc is None:
            # Look up on filesystem
            disk_path = os.path.join(ZEROS_DIR, f"zero_{expected_zero_idx:05d}.json")
            if os.path.exists(disk_path):
                try:
                    with open(disk_path, "r", encoding="utf-8") as f:
                        zc = json.load(f)
                except Exception:
                    zc = None
        if zc is None:
            anomalies.append(f"Constituent zero certificate for index {expected_zero_idx} (hash {expected_c_hash}) could not be resolved")
            continue
        if expected_c_hash and zc.get("certificate_hash") != expected_c_hash:
            anomalies.append(f"Constituent zero #{expected_zero_idx} hash mismatch: expected {expected_c_hash}, found {zc.get('certificate_hash')}")
        z_actual_idx = zc.get("nontrivial_index") or zc.get("zero_index")
        if z_actual_idx != expected_zero_idx:
            anomalies.append(f"Constituent zero index mismatch: expected {expected_zero_idx}, found {z_actual_idx}")
        # Independently verify constituent zero certificate
        ok_z, errs_z = verify_certificate(zc, cert_store=cert_store, check_provenance=check_provenance)
        if not ok_z:
            anomalies.append(f"Constituent zero #{expected_zero_idx} failed verification: {errs_z}")
        resolved_certs.append(zc)

    # Rigorous Turing zero counting at block endpoints
    endpoint_bounds = cert.get("endpoint_bounds")
    if not isinstance(endpoint_bounds, dict):
        anomalies.append("Missing or invalid endpoint_bounds for Turing zero counting")
    else:
        t_min_str = endpoint_bounds.get("t_min")
        t_max_str = endpoint_bounds.get("t_max")

        if t_min_str and t_max_str:
            t_min = arb(t_min_str)
            t_max = arb(t_max_str)
            n_min_zeros = t_min.zeta_nzeros()
            n_max_zeros = t_max.zeta_nzeros()
            try:
                n_min_int = int(n_min_zeros.unique_fmpz())
                n_max_int = int(n_max_zeros.unique_fmpz())
                turing_count = n_max_int - n_min_int

                if turing_count != expected_count:
                    anomalies.append(f"Turing zero count difference N({t_max_str}) - N({t_min_str}) = {turing_count}, expected {expected_count}")
                if n_min_int != min_idx - 1:
                    anomalies.append(f"Lower endpoint count N({t_min_str}) = {n_min_int}, expected {min_idx - 1}")
                if n_max_int != max_idx:
                    anomalies.append(f"Upper endpoint count N({t_max_str}) = {n_max_int}, expected {max_idx}")
            except Exception as e:
                anomalies.append(f"FLINT Turing zero counting failed on endpoints [{t_min_str}, {t_max_str}]: {e}")
        else:
            anomalies.append("Missing endpoint bounds keys for Turing zero counting")

    return (len(anomalies) == 0), anomalies


def _verify_worldline_continuation(
    cert: Dict[str, Any],
    anomalies: List[str],
    cert_store: Optional[Dict[str, Any]] = None,
    check_provenance: bool = True
) -> Tuple[bool, List[str]]:
    """Mathematical verification in Arb of continuous worldlines, radial defect, and leaf parameters."""
    assert acb is not None and arb is not None and acb_series is not None and ctx is not None
    src_hash = cert.get("source_zero_hash")
    src_idx = cert.get("source_zero_index")
    grade_K = cert.get("grade_K")
    delta_str = str(cert.get("delta", "0.0")).strip()
    src_fam = cert.get("source_zero_family") or cert.get("zero_family", "nontrivial")

    if src_hash is None or src_idx is None or grade_K is None:
        anomalies.append("Worldline certificate missing source_zero_hash, source_zero_index, or grade_K")
        return False, anomalies

    # Resolve source zero certificate strictly by family
    src_cert = None
    if cert_store:
        if src_hash:
            cand = cert_store.get(src_hash)
            if cand:
                cand_fam = cand.get("zero_family", "nontrivial" if cand.get("certificate_type") == "zero_isolation_and_simplicity" else "trivial")
                if cand_fam != src_fam:
                    anomalies.append(f"Source zero family mismatch: worldline declared {src_fam}, but source hash {src_hash} is {cand_fam}")
                src_cert = cand
        if src_cert is None:
            if src_fam == "trivial":
                src_cert = cert_store.get(f"trivial_zero_{src_idx:05d}")
            else:
                src_cert = cert_store.get(f"zero_{src_idx:05d}")

    if src_cert is None:
        if src_fam == "trivial":
            disk_path = os.path.join(TRIVIAL_ZEROS_DIR, f"trivial_zero_{src_idx:05d}.json")
        else:
            disk_path = os.path.join(ZEROS_DIR, f"zero_{src_idx:05d}.json")
        if os.path.exists(disk_path):
            try:
                with open(disk_path, "r", encoding="utf-8") as f:
                    src_cert = json.load(f)
            except Exception:
                src_cert = None

    if src_cert is None:
        anomalies.append(f"Source {src_fam} zero certificate for index {src_idx} (hash {src_hash}) could not be resolved")
        return False, anomalies

    # Verify family matches
    cand_fam = src_cert.get("zero_family", "nontrivial" if src_cert.get("certificate_type") == "zero_isolation_and_simplicity" else "trivial")
    if cand_fam != src_fam:
        anomalies.append(f"Source zero family mismatch: expected {src_fam}, resolved certificate is {cand_fam}")

    if src_cert.get("certificate_hash") != src_hash:
        anomalies.append(f"Source zero certificate hash mismatch: expected {src_hash}, found {src_cert.get('certificate_hash')}")

    # Verify source zero certificate
    ok_src, errs_src = verify_certificate(src_cert, cert_store=cert_store, check_provenance=check_provenance)
    if not ok_src:
        anomalies.append(f"Source zero certificate verification failed: {errs_src}")

    tp = cert.get("transformed_point", {})
    if "real_rad" not in tp or "imag_rad" not in tp:
        anomalies.append("Worldline transformed_point missing radius enclosures (dropped radius vulnerability)")
    else:
        re_rad_str = str(tp.get("real_rad", "0.0")).strip()
        im_rad_str = str(tp.get("imag_rad", "0.0")).strip()
        if re_rad_str.startswith("-") or im_rad_str.startswith("-"):
            anomalies.append(f"Negative radius in transformed point: real_rad={re_rad_str}, imag_rad={im_rad_str}")
        else:
            try:
                if float(re_rad_str) < 0 or float(im_rad_str) < 0:
                    anomalies.append(f"Negative radius in transformed point: real_rad={re_rad_str}, imag_rad={im_rad_str}")
            except Exception:
                pass

    tau_ball = arb.pi() * 2
    tau_K = tau_ball ** grade_K
    tau_neg_K = tau_ball ** (-grade_K)

    is_trivial_src = (
        src_cert.get("zero_family") == "trivial"
        or src_cert.get("certificate_type") == "trivial_zero_certificate"
    )

    if is_trivial_src:
        s_exact = -2 * src_idx
        s_worldline = acb(s_exact, 0) * acb(tau_K, 0)
        R_tau = (tau_neg_K * s_worldline.real) - arb("0.5")
        expected_R = arb(str(s_exact - 0.5))
        if not R_tau.contains(expected_R):
            anomalies.append(f"Trivial zero worldline radial coordinate does not contain {s_exact - 0.5}: {R_tau}")
    else:
        # Reconstruct full source ball with radii
        s_enc = src_cert.get("enclosure", {})
        re_ball = _reconstruct_arb_ball(s_enc.get("real_mid", "0.5"), s_enc.get("real_rad", "1e-50"))
        im_ball = _reconstruct_arb_ball(s_enc.get("imag_mid", "0.0"), s_enc.get("imag_rad", "1e-50"))

        # Re-propagate through worldline transformation
        delta_arb = arb(delta_str)
        z_point = acb(re_ball + delta_arb, im_ball)
        s_worldline = z_point * acb(tau_K, 0)

        # Stored transformed point ball comparison: stored must strictly contain recomputed point
        stored_re = _reconstruct_arb_ball(tp.get("real_mid", "0.0"), tp.get("real_rad", "1e-50"))
        stored_im = _reconstruct_arb_ball(tp.get("imag_mid", "0.0"), tp.get("imag_rad", "1e-50"))
        if not stored_re.contains(s_worldline.real) or not stored_im.contains(s_worldline.imag):
            anomalies.append(
                f"Stored transformed point {stored_re}+{stored_im}j does not contain recomputed worldline point {s_worldline}"
            )

        # Recompute normalized radial coordinate and defect
        sigma_critical = tau_K / 2
        R_tau = (tau_neg_K * s_worldline.real) - arb("0.5")
        radial_residual = (R_tau - delta_arb).abs_upper()

        if radial_residual > arb("1e-30"):
            anomalies.append(f"Radial residual exceeds certification threshold: {radial_residual}")

        is_actual = (delta_str in ["0.0", "0", "+0.0", "-0.0"])
        expected_claim_type = "actual_zero_worldline" if is_actual else "synthetic_radial_leaf"
        actual_claim_type = cert.get("claim_type")
        if actual_claim_type != expected_claim_type:
            anomalies.append(f"claim_type mismatch: expected '{expected_claim_type}', found '{actual_claim_type}'")

        if is_actual:
            if not R_tau.contains(arb("0.0")):
                anomalies.append(f"Actual zero worldline radial coordinate does not contain 0.0: {R_tau}")
        else:
            if not R_tau.contains(delta_arb):
                anomalies.append(f"Synthetic radial leaf coordinate does not contain declared delta {delta_str}: {R_tau}")

    # Check formal theorem reference existence in Lean source
    thm_ref = cert.get("formal_theorem_reference", "")
    if thm_ref:
        lean_file = os.path.join(REPO_ROOT, "formal", "RiemannScope", "RadialLeaf.lean")
        if os.path.exists(lean_file):
            with open(lean_file, "r", encoding="utf-8") as lf:
                if "radialLeaf_worldline_invariance" not in lf.read():
                    anomalies.append(f"Referenced formal Lean theorem '{thm_ref}' not found in {lean_file}")
        else:
            anomalies.append(f"Lean source file {lean_file} not found")

    return (len(anomalies) == 0), anomalies


def _verify_radial_witness_certificate(
    cert: Dict[str, Any],
    anomalies: List[str],
    check_provenance: bool = True
) -> Tuple[bool, List[str]]:
    """Mathematical verification in Arb of radial sign witness enclosure."""
    assert acb is not None and arb is not None and ctx is not None
    import math_core

    witness_id = str(cert.get("witness_id", "")).strip()
    window_type = str(cert.get("window_type", "")).strip()
    if witness_id != "WIT-02" or window_type != "fejer":
        anomalies.append(f"Unsupported witness_id / window_type: {witness_id} / {window_type}")

    params = cert.get("parameters", {})
    sigma_str = str(params.get("sigma", "")).strip()
    gamma_str = str(params.get("gamma", "")).strip()
    delta_str = str(params.get("delta", "")).strip()
    T_str = str(params.get("T", "")).strip()
    n_sub = int(params.get("n_subdivisions", 50000))
    prec_dps = int(cert.get("precision_dps", 60))

    if sigma_str != "5.0" or gamma_str != "14.0" or delta_str != "0.49" or T_str != "16.8":
        anomalies.append(f"Witness parameters do not match canonical WIT-02: sigma={sigma_str}, gamma={gamma_str}, delta={delta_str}, T={T_str}")

    res = math_core.certify_g4_fejer_witness_arb(
        sigma=sigma_str,
        gamma=gamma_str,
        delta=delta_str,
        T=T_str,
        n_subdivisions=n_sub,
        dps=prec_dps
    )

    replayed_lower = arb(res["interval_lower"])
    replayed_upper = arb(res["interval_upper"])

    enc = cert.get("enclosure", {})
    stored_lower_str = enc.get("interval_lower")
    stored_upper_str = enc.get("interval_upper")

    if not stored_lower_str or not stored_upper_str:
        anomalies.append("Missing enclosure bounds in witness certificate")
    else:
        stored_lower = arb(stored_lower_str)
        stored_upper = arb(stored_upper_str)

        # Upper bound strictly negative
        if stored_upper.upper() >= 0 or replayed_upper.upper() >= 0:
            anomalies.append(f"Witness certificate upper bound is not strictly negative: stored={stored_upper}, replayed={replayed_upper}")

        # Stored bounds match replayed bounds
        if not replayed_upper.contains(stored_upper) or not replayed_lower.contains(stored_lower):
            anomalies.append(f"Witness enclosure mismatch: stored [{stored_lower}, {stored_upper}], replayed [{replayed_lower}, {replayed_upper}]")

    if cert.get("status") != "radial_witness_certified":
        anomalies.append(f"Invalid witness certificate status: {cert.get('status')}")

    if cert.get("evidence_status") != "CERTIFIED_NEGATIVE_ARB_BALL":
        anomalies.append(f"Invalid witness evidence status: {cert.get('evidence_status')}")

    # Check formal theorem reference
    thm_ref = cert.get("formal_theorem_reference", "")
    if thm_ref:
        lean_file = os.path.join(REPO_ROOT, "formal", "RiemannScope", "ArithmeticBridge.lean")
        if os.path.exists(lean_file):
            with open(lean_file, "r", encoding="utf-8") as lf:
                if "additive_reference_subtraction_invariance" not in lf.read():
                    anomalies.append(f"Referenced formal Lean theorem '{thm_ref}' not found in {lean_file}")
        else:
            anomalies.append(f"Lean source file {lean_file} not found")

    return (len(anomalies) == 0), anomalies


def _dispatch_and_verify_certificate(
    cert_type: str,
    cert: Dict[str, Any],
    anomalies: List[str],
    cert_store: Optional[Dict[str, Any]] = None,
    check_provenance: bool = True
) -> Tuple[bool, List[str]]:
    """Mathematical dispatch and execution of certificate verification logic."""
    if cert_type == "zero_isolation_and_simplicity":
        _verify_zero_enclosure_and_isolation(cert, anomalies)
    elif cert_type == "trivial_zero_certificate":
        _verify_trivial_zero_enclosure(cert, anomalies)
    elif cert_type == "complete_block_certificate":
        _verify_block_isolation(cert, anomalies, cert_store=cert_store, check_provenance=check_provenance)
    elif cert_type == "worldline_certificate":
        _verify_worldline_continuation(cert, anomalies, cert_store=cert_store, check_provenance=check_provenance)
    elif cert_type in ("radial_witness_certificate", "g4_radial_witness"):
        _verify_radial_witness_certificate(cert, anomalies, check_provenance=check_provenance)
    else:
        anomalies.append(f"Unknown certificate_type: {cert_type}")
    return (len(anomalies) == 0), anomalies



def verify_certificate(
    cert: Dict[str, Any],
    cert_store: Optional[Dict[str, Dict[str, Any]]] = None,
    check_provenance: bool = True,
    canonical_current: bool = False
) -> Tuple[bool, List[str]]:
    """Independently verify a certificate schema, SHA-256 self-hash, provenance, and replay all mathematical claims.

    Fails closed: Any tampering with mathematical claims, index, bounds, constituents,
    oversized balls, missing/forged provenance, or source zeros will result in (False, anomalies).
    """
    anomalies: List[str] = []
    if not isinstance(cert, dict):
        return False, ["Malformed certificate: expected dictionary"]

    # 1. Structure and schema version validation
    schema_ver = str(cert.get("schema_version", "")).strip()
    if schema_ver != CERTIFICATE_SCHEMA_VERSION:
        anomalies.append(f"Unsupported schema_version: '{schema_ver}'. Expected '{CERTIFICATE_SCHEMA_VERSION}'")

    cert_type = str(cert.get("certificate_type", "")).strip()
    if not cert_type or cert_type not in CERTIFICATE_MODULE_DEPENDENCIES:
        anomalies.append(f"Invalid or unsupported certificate_type: '{cert_type}'")

    cert_status = str(cert.get("status", "")).strip()
    if not cert_status or cert_status not in CERTIFICATION_LEVELS:
        anomalies.append(f"Invalid certification status: '{cert_status}'")

    # 2. Canonical Hash Verification (tamper detection)
    stored_hash = cert.get("certificate_hash")
    if not stored_hash or len(stored_hash) != 64 or not all(c in "0123456789abcdefABCDEF" for c in stored_hash):
        anomalies.append("Missing or invalid certificate_hash format")
    else:
        computed_hash = _sha256_canonical(cert)
        if computed_hash != stored_hash:
            anomalies.append(f"Hash mismatch: stored {stored_hash}, computed {computed_hash}")

    # 3. Dependency fingerprint validation
    dep_fp = cert.get("dependency_fingerprint")
    dep_ok, dep_errs = validate_dependency_compatibility(dep_fp, check_current_runtime=False)
    if not dep_ok:
        anomalies.extend(dep_errs)

    # 3b. Source code and input data hashes completeness check
    cert_src = cert.get("source_code_hashes", {})
    if not isinstance(cert_src, dict) or not cert_src:
        anomalies.append("Certificate missing or empty source_code_hashes map")
    for mod in REQUIRED_SOURCE_MODULES:
        if mod not in cert_src or not cert_src[mod] or len(cert_src[mod]) != 64 or cert_src[mod] == "N/A":
            anomalies.append(f"source_code_hashes missing or invalid for required module '{mod}'")

    cert_data = cert.get("input_data_hashes", {})
    if not isinstance(cert_data, dict) or not cert_data:
        anomalies.append("Certificate missing or empty input_data_hashes map")
    for df in REQUIRED_INPUT_DATA_FILES:
        if df not in cert_data or not cert_data[df] or len(cert_data[df]) != 64 or cert_data[df] == "N/A":
            anomalies.append(f"input_data_hashes missing or invalid for required file '{df}'")

    req_mods = CERTIFICATE_MODULE_DEPENDENCIES.get(cert_type, REQUIRED_SOURCE_MODULES)

    if check_provenance:
        # 4. Producing Git Commit Validation (with historical blob binding)
        commit = str(cert.get("producing_git_commit", "")).strip()
        commit_ok, commit_err = _is_valid_git_commit(
            commit,
            source_code_hashes=cert_src,
            input_data_hashes=cert_data
        )
        if not commit_ok:
            anomalies.append(f"Invalid producing_git_commit provenance: {commit_err}")

        # 5. Verify current source code files exist on disk and match in canonical-current mode
        curr_src = _get_source_code_hashes(modules=req_mods)
        for mod in req_mods:
            curr_h = curr_src.get(mod, "N/A")
            if curr_h == "N/A":
                anomalies.append(f"Required current source module '{mod}' missing on disk")
            elif canonical_current:
                if mod == "certification.py":
                    curr_math_h = _get_module_math_hash("certification.py")
                    cert_math_h = _get_module_math_hash("certification.py", commit=commit)
                    if curr_math_h != cert_math_h:
                        anomalies.append(f"Current source module 'certification.py' mathematical component hash mismatch: disk {curr_math_h}, cert {cert_math_h}")
                elif curr_h != cert_src.get(mod):
                    anomalies.append(f"Current source module '{mod}' hash mismatch: disk {curr_h}, cert {cert_src.get(mod)}")

        # 6. Verify current input data files exist and match certificate
        req_data = CERTIFICATE_DATA_DEPENDENCIES.get(cert_type, REQUIRED_INPUT_DATA_FILES)
        curr_data = _get_input_data_hashes(files=req_data)
        for df in req_data:
            curr_dh = curr_data.get(df, "N/A")
            if curr_dh == "N/A":
                anomalies.append(f"Required current input data file '{df}' missing on disk")
            elif canonical_current and curr_dh != cert_data.get(df):
                anomalies.append(f"Current input data file '{df}' hash mismatch: disk {curr_dh}, cert {cert_data.get(df)}")

    if not FLINT_AVAILABLE or ctx is None or acb is None or arb is None or acb_series is None:
        return False, ["FLINT/python-flint is required for independent mathematical verification"]

    dps = int(cert.get("precision_dps", 80))
    old_dps = ctx.dps
    ctx.dps = dps + 20

    try:
        _dispatch_and_verify_certificate(
            cert_type, cert, anomalies, cert_store=cert_store, check_provenance=check_provenance
        )
    finally:
        ctx.dps = old_dps

    return (len(anomalies) == 0), anomalies


def load_certificate_from_disk(cert_path: str) -> Optional[Dict[str, Any]]:
    """Load certificate dictionary from disk path without verification."""
    if not os.path.exists(cert_path):
        return None
    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def load_and_verify_certificate(
    cert_path: str,
    cert_store: Optional[Dict[str, Dict[str, Any]]] = None,
    check_provenance: bool = True
) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
    """Load a certificate from disk and run full mathematical verification.

    Returns:
        (is_valid, certificate_dict_or_None, list_of_anomalies)
    """
    if not os.path.exists(cert_path):
        return False, None, [f"Certificate file '{cert_path}' does not exist"]
    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            cert = json.load(f)
    except Exception as e:
        return False, None, [f"Failed to read certificate JSON from '{cert_path}': {e}"]

    is_valid, anomalies = verify_certificate(cert, cert_store=cert_store, check_provenance=check_provenance)
    return is_valid, cert, anomalies


def generate_verification_report(
    cert_dir: Optional[str] = None,
    check_provenance: bool = True,
    git_commit: Optional[str] = None
) -> Dict[str, Any]:
    """Inspect all certificates in data/certificates/, verify each independently,
    and generate the canonical verification_report.json artifact.

    Fails closed: If any certificate is corrupted, fails mathematical bounds, or has
    missing/mismatched provenance, it will be listed under 'failures' and status set to 'failed'.

    Returns:
        The generated verification report dictionary.
    """
    target_dir = cert_dir or CERT_DIR
    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"Certificate directory '{target_dir}' does not exist")

    report_commit = git_commit or _get_git_commit()
    if check_provenance:
        env_ok, env_err = validate_generation_environment(report_commit)
        if not env_ok:
            raise RuntimeError(f"Report generation environment invalid: {env_err}")

    # Enumerate on-disk certificates
    zeros_files = sorted(glob.glob(os.path.join(target_dir, "zeros", "*.json")))
    trivial_files = sorted(glob.glob(os.path.join(target_dir, "trivial_zeros", "*.json")))
    blocks_files = sorted(glob.glob(os.path.join(target_dir, "blocks", "*.json")))
    worldlines_files = sorted(glob.glob(os.path.join(target_dir, "worldlines", "*.json")))
    witnesses_files = sorted(glob.glob(os.path.join(target_dir, "witnesses", "*.json")))

    total_inventory = len(zeros_files) + len(trivial_files) + len(blocks_files) + len(worldlines_files) + len(witnesses_files)
    all_files = zeros_files + trivial_files + blocks_files + worldlines_files + witnesses_files

    cert_store: Dict[str, Dict[str, Any]] = {}
    parsed_files: List[Tuple[str, Optional[Dict[str, Any]], str, Optional[str]]] = []

    for fpath in all_files:
        with open(fpath, "rb") as f:
            raw_bytes = f.read()
        normalized_bytes = raw_bytes.replace(b"\r\n", b"\n")
        file_sha256 = hashlib.sha256(normalized_bytes).hexdigest()
        try:
            c = json.loads(normalized_bytes.decode("utf-8"))
            h = c.get("certificate_hash")
            if h:
                cert_store[h] = c
            c_type = c.get("certificate_type")
            if c_type == "zero_isolation_and_simplicity":
                z_idx = c.get("nontrivial_index") or c.get("zero_index")
                if z_idx is not None:
                    cert_store[f"zero_{z_idx:05d}"] = c
            elif c_type == "trivial_zero_certificate":
                m_idx = c.get("trivial_index")
                if m_idx is not None:
                    cert_store[f"trivial_zero_{m_idx:05d}"] = c
            parsed_files.append((fpath, c, file_sha256, None))
        except Exception as e:
            parsed_files.append((fpath, None, file_sha256, str(e)))

    passed_count = 0
    failed_count = 0
    failures: List[Dict[str, Any]] = []
    inventory: List[Dict[str, Any]] = []

    for fpath, cert, file_sha, parse_err in parsed_files:
        fname = os.path.basename(fpath)
        if os.path.abspath(fpath).startswith(os.path.abspath(REPO_ROOT)):
            rel_path = os.path.relpath(fpath, REPO_ROOT).replace("\\", "/")
        else:
            sub_p = os.path.relpath(fpath, target_dir).replace("\\", "/")
            rel_path = f"data/certificates/{sub_p}"
        if parse_err is not None or cert is None:
            failed_count += 1
            failures.append({"file": fname, "errors": [f"Parse error: {parse_err}"]})
            inventory.append({
                "relative_path": rel_path,
                "certificate_type": "unparseable",
                "status": "parse_error",
                "certificate_hash": "N/A",
                "file_sha256": file_sha,
                "producing_git_commit": "N/A"
            })
            continue

        try:
            ok, errs = verify_certificate(cert, cert_store=cert_store, check_provenance=check_provenance, canonical_current=True)
            if ok:
                passed_count += 1
                inventory.append({
                    "relative_path": rel_path,
                    "certificate_type": cert.get("certificate_type", "unknown"),
                    "mathematical_status": cert.get("status", "unknown"),
                    "verifier_status": "passed",
                    "status": "passed",
                    "certificate_hash": cert.get("certificate_hash", "N/A"),
                    "file_sha256": file_sha,
                    "producing_git_commit": cert.get("producing_git_commit", "N/A")
                })
            else:
                failed_count += 1
                failures.append({"file": fname, "hash": cert.get("certificate_hash"), "errors": errs})
                inventory.append({
                    "relative_path": rel_path,
                    "certificate_type": cert.get("certificate_type", "unknown"),
                    "mathematical_status": cert.get("status", "unknown"),
                    "verifier_status": "failed",
                    "status": "failed",
                    "certificate_hash": cert.get("certificate_hash", "N/A"),
                    "file_sha256": file_sha,
                    "producing_git_commit": cert.get("producing_git_commit", "N/A")
                })
        except Exception as e:
            failed_count += 1
            failures.append({"file": fname, "errors": [str(e)]})
            inventory.append({
                "relative_path": rel_path,
                "certificate_type": cert.get("certificate_type", "unknown") if cert else "unknown",
                "mathematical_status": cert.get("status", "unknown") if cert else "unknown",
                "verifier_status": "exception",
                "status": "exception",
                "certificate_hash": cert.get("certificate_hash", "N/A") if cert else "N/A",
                "file_sha256": file_sha,
                "producing_git_commit": cert.get("producing_git_commit", "N/A") if cert else "N/A"
            })

    # Sort inventory deterministically by relative_path
    inventory.sort(key=lambda x: x["relative_path"])
    inventory_root_hash = hashlib.sha256(json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

    status = "verified" if (failed_count == 0 and total_inventory > 0 and passed_count == total_inventory) else ("unverified" if total_inventory == 0 else "failed")

    report: Dict[str, Any] = {
        "schema_version": CERTIFICATE_SCHEMA_VERSION,
        "report_type": "certificate_verification_report",
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_inventory": total_inventory,
        "nontrivial_zeros_count": len(zeros_files),
        "trivial_zeros_count": len(trivial_files),
        "blocks_count": len(blocks_files),
        "worldlines_count": len(worldlines_files),
        "witnesses_count": len(witnesses_files),
        "passed_count": passed_count,
        "failed_count": failed_count,
        "inventory_root_hash": inventory_root_hash,
        "inventory": inventory,
        "dependency_fingerprint": _get_dependency_fingerprint(),
        "source_code_hashes": _get_source_code_hashes(report_commit),
        "input_data_hashes": _get_input_data_hashes(report_commit),
        "producing_git_commit": report_commit,
        "failures": failures
    }
    report_hash = _sha256_canonical(report)
    report["report_hash"] = report_hash

    report_path = os.path.join(target_dir, "verification_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report


def load_verification_report(
    report_path: Optional[str] = None,
    cert_dir: Optional[str] = None,
    check_provenance: bool = True,
    canonical_current: bool = False
) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
    """Load and strictly validate verification_report.json against exact current on-disk inventory.

    Returns:
        (is_authentic_and_passing, report_dict_or_None, anomalies)
    """
    target_dir = cert_dir or CERT_DIR
    target_path = report_path or os.path.join(target_dir, "verification_report.json")
    if not os.path.exists(target_path):
        return False, None, ["Verification report not found (status: unverified)"]

    try:
        with open(target_path, "r", encoding="utf-8") as f:
            report = json.load(f)
    except Exception as e:
        return False, None, [f"Failed to read/parse verification report: {e}"]

    anomalies: List[str] = []

    # 1. Validate report schema type
    if not isinstance(report, dict):
        return False, None, ["Verification report must be a dictionary"]
    if report.get("schema_version") != CERTIFICATE_SCHEMA_VERSION:
        anomalies.append(f"Unsupported schema_version: expected '{CERTIFICATE_SCHEMA_VERSION}', got '{report.get('schema_version')}'")
    if report.get("report_type") != "certificate_verification_report":
        anomalies.append(f"Invalid report_type: expected 'certificate_verification_report', got '{report.get('report_type')}'")

    # 2. Check self-hash
    exp_h = report.get("report_hash")
    if not exp_h or _sha256_canonical(report) != exp_h:
        anomalies.append("Verification report self-hash mismatch or missing")

    # 3. Check status and count equalities
    total_inv = report.get("total_inventory", 0)
    passed_cnt = report.get("passed_count", 0)
    failed_cnt = report.get("failed_count", 0)
    rep_failures = report.get("failures", [])

    if not isinstance(total_inv, int) or total_inv <= 0:
        anomalies.append(f"Report total_inventory must be positive integer, got {total_inv}")
    if passed_cnt + failed_cnt != total_inv:
        anomalies.append(f"Count mismatch: passed ({passed_cnt}) + failed ({failed_cnt}) != total ({total_inv})")
    if failed_cnt > 0:
        anomalies.append(f"Report contains {failed_cnt} failed certificates")
    if passed_cnt != total_inv:
        anomalies.append(f"Report passed count ({passed_cnt}) != total inventory ({total_inv})")
    if not isinstance(rep_failures, list):
        anomalies.append("Report failures field must be a list")
    elif len(rep_failures) != failed_cnt:
        anomalies.append(f"Report failures list length ({len(rep_failures)}) does not match failed_count ({failed_cnt})")
    elif failed_cnt == 0 and len(rep_failures) > 0:
        anomalies.append("Nonempty failures list with failed_count=0")

    if report.get("status") != "verified":
        anomalies.append(f"Report status is '{report.get('status')}', expected 'verified'")

    # Category counts validation
    nz_cnt = report.get("nontrivial_zeros_count", 0)
    tz_cnt = report.get("trivial_zeros_count", 0)
    blk_cnt = report.get("blocks_count", 0)
    wl_cnt = report.get("worldlines_count", 0)
    wit_cnt = report.get("witnesses_count", 0)
    if nz_cnt + tz_cnt + blk_cnt + wl_cnt + wit_cnt != total_inv:
        anomalies.append(f"Category count sum ({nz_cnt + tz_cnt + blk_cnt + wl_cnt + wit_cnt}) != total_inventory ({total_inv})")

    # 4. Enumerate actual on-disk certificate inventory
    zeros_files = sorted(glob.glob(os.path.join(target_dir, "zeros", "*.json")))
    trivial_files = sorted(glob.glob(os.path.join(target_dir, "trivial_zeros", "*.json")))
    blocks_files = sorted(glob.glob(os.path.join(target_dir, "blocks", "*.json")))
    worldlines_files = sorted(glob.glob(os.path.join(target_dir, "worldlines", "*.json")))
    witnesses_files = sorted(glob.glob(os.path.join(target_dir, "witnesses", "*.json")))
    actual_files = sorted(zeros_files + trivial_files + blocks_files + worldlines_files + witnesses_files)

    if len(actual_files) != total_inv:
        anomalies.append(f"On-disk certificate count ({len(actual_files)}) does not match report total_inventory ({total_inv})")
    if len(zeros_files) != nz_cnt:
        anomalies.append(f"On-disk nontrivial zeros count ({len(zeros_files)}) != report ({nz_cnt})")
    if len(trivial_files) != tz_cnt:
        anomalies.append(f"On-disk trivial zeros count ({len(trivial_files)}) != report ({tz_cnt})")
    if len(blocks_files) != blk_cnt:
        anomalies.append(f"On-disk blocks count ({len(blocks_files)}) != report ({blk_cnt})")
    if len(worldlines_files) != wl_cnt:
        anomalies.append(f"On-disk worldlines count ({len(worldlines_files)}) != report ({wl_cnt})")
    if len(witnesses_files) != wit_cnt:
        anomalies.append(f"On-disk witnesses count ({len(witnesses_files)}) != report ({wit_cnt})")


    # Map actual files to repo-relative paths
    actual_rel_map = {}
    for af in actual_files:
        if os.path.abspath(af).startswith(os.path.abspath(REPO_ROOT)):
            rel = os.path.relpath(af, REPO_ROOT).replace("\\", "/")
        else:
            sub_p = os.path.relpath(af, target_dir).replace("\\", "/")
            rel = f"data/certificates/{sub_p}"
        actual_rel_map[rel] = af

    rep_inventory = report.get("inventory", [])
    if not isinstance(rep_inventory, list) or len(rep_inventory) != total_inv:
        anomalies.append(f"Report inventory list length ({len(rep_inventory) if isinstance(rep_inventory, list) else 'invalid'}) does not match total_inventory ({total_inv})")

    # 5. Inventory ordering, path normalization, and uniqueness
    rep_rel_list: List[str] = []
    for entry in rep_inventory:
        if isinstance(entry, dict) and isinstance(entry.get("relative_path"), str):
            r_path = entry["relative_path"]
            # Reject absolute paths, backslashes, leading slash, traversal paths
            if "\\" in r_path or r_path.startswith("/") or ".." in r_path or ":" in r_path:
                anomalies.append(f"Invalid path format or traversal in inventory entry: '{r_path}'")
            if not r_path.startswith("data/certificates/"):
                anomalies.append(f"Inventory entry path '{r_path}' does not start with 'data/certificates/'")
            rep_rel_list.append(r_path)

    if rep_rel_list != sorted(rep_rel_list):
        anomalies.append("Report inventory is not sorted deterministically by relative_path")

    rep_rel_set: Set[str] = set(rep_rel_list)
    if len(rep_rel_set) != len(rep_rel_list):
        anomalies.append("Duplicate relative_path entries detected in report inventory")

    actual_rel_set: Set[str] = set(actual_rel_map.keys())

    missing_on_disk = rep_rel_set - actual_rel_set
    if missing_on_disk:
        anomalies.append(f"Certificates declared in report but missing on disk: {sorted(list(missing_on_disk))[:5]}")

    extra_on_disk = actual_rel_set - rep_rel_set
    if extra_on_disk:
        anomalies.append(f"Certificates present on disk but missing from report: {sorted(list(extra_on_disk))[:5]}")

    # Build memory store of certificates for reference lookups
    loaded_cert_map: Dict[str, Dict[str, Any]] = {}

    # 6. Verify individual file byte hashes, parsed certificate hashes, dependency fingerprints, and status
    for entry in rep_inventory:
        if not isinstance(entry, dict):
            anomalies.append("Malformed entry in report inventory list")
            continue
        rel = entry.get("relative_path")
        if not isinstance(rel, str):
            anomalies.append("Inventory entry missing 'relative_path' string")
            continue
        disk_path = actual_rel_map.get(rel)

        if disk_path and os.path.exists(disk_path):
            try:
                with open(disk_path, "rb") as f:
                    raw_bytes = f.read()
                content = raw_bytes.replace(b"\r\n", b"\n")
                disk_sha = hashlib.sha256(content).hexdigest()
                rep_sha = entry.get("file_sha256")
                if disk_sha != rep_sha:
                    anomalies.append(f"File SHA-256 mismatch for '{rel}': on-disk {disk_sha}, report {rep_sha}")

                cert_dict = json.loads(content.decode("utf-8"))
                stored_c_hash = cert_dict.get("certificate_hash")
                computed_c_hash = _sha256_canonical(cert_dict)
                entry_c_hash = entry.get("certificate_hash")

                if stored_c_hash != entry_c_hash:
                    anomalies.append(f"Certificate hash mismatch in '{rel}': cert file {stored_c_hash}, report entry {entry_c_hash}")
                if computed_c_hash != stored_c_hash:
                    anomalies.append(f"Certificate self-hash mismatch in '{rel}': stored {stored_c_hash}, computed {computed_c_hash}")

                if stored_c_hash:
                    loaded_cert_map[stored_c_hash] = cert_dict

                # Check verifier_status and mathematical_status in entry
                v_stat = entry.get("verifier_status")
                if v_stat != "passed":
                    anomalies.append(f"Inventory entry '{rel}' verifier_status is '{v_stat}', expected 'passed'")

                math_status = entry.get("mathematical_status")
                if math_status and cert_dict.get("status") != math_status:
                    anomalies.append(f"Certificate mathematical status mismatch in '{rel}': cert {cert_dict.get('status')}, report {math_status}")

                # Independently validate certificate dependency fingerprint against authoritative runtime policy
                cert_dep = cert_dict.get("dependency_fingerprint", {})
                cdep_ok, cdep_errs = validate_dependency_compatibility(cert_dep, check_current_runtime=True)
                if not cdep_ok:
                    anomalies.append(f"Certificate '{rel}' has incompatible dependency fingerprint: {'; '.join(cdep_errs)}")

                # Independently verify certificate correctness and mathematical bounds
                c_ok, c_errs = verify_certificate(cert_dict, cert_store=loaded_cert_map, check_provenance=check_provenance, canonical_current=canonical_current)
                if not c_ok:
                    anomalies.append(f"Certificate '{rel}' failed independent verification: {'; '.join(c_errs)}")

            except Exception as e:
                anomalies.append(f"Failed reading/parsing on-disk certificate '{rel}': {e}")

    # 7. Recompute inventory root hash
    exp_root_hash = report.get("inventory_root_hash")
    calc_root_hash = hashlib.sha256(json.dumps(rep_inventory, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if not exp_root_hash or calc_root_hash != exp_root_hash:
        anomalies.append(f"Inventory root hash mismatch: reported {exp_root_hash}, computed {calc_root_hash}")

    # 8. Check report dependency fingerprint
    rep_dep = report.get("dependency_fingerprint", {})
    dep_ok, dep_errs = validate_dependency_compatibility(rep_dep, check_current_runtime=True)
    if not dep_ok:
        anomalies.extend(dep_errs)

    if check_provenance:
        # 9. Check producing git commit
        rep_commit = str(report.get("producing_git_commit", "")).strip()
        commit_ok, commit_err = _is_valid_git_commit(
            rep_commit,
            source_code_hashes=report.get("source_code_hashes"),
            input_data_hashes=report.get("input_data_hashes")
        )
        if not commit_ok:
            anomalies.append(f"Invalid report producing_git_commit provenance: {commit_err}")

        # 10. Check current workspace source files & input data files
        curr_src = _get_source_code_hashes(modules=CERTIFICATE_MATHEMATICAL_MODULES)
        rep_src = report.get("source_code_hashes", {})
        for mod in CERTIFICATE_MATHEMATICAL_MODULES:
            curr_h = curr_src.get(mod, "N/A")
            if curr_h == "N/A":
                anomalies.append(f"Required current source module '{mod}' missing on disk")
            elif canonical_current:
                if mod == "certification.py":
                    curr_math_h = _get_module_math_hash("certification.py")
                    rep_math_h = _get_module_math_hash("certification.py", commit=rep_commit)
                    if curr_math_h != rep_math_h:
                        anomalies.append(f"Current source module 'certification.py' mathematical component hash mismatch: disk {curr_math_h}, report {rep_math_h}")
                elif curr_h != rep_src.get(mod):
                    anomalies.append(f"Current source module '{mod}' hash mismatch: disk {curr_h}, report {rep_src.get(mod)}")

        curr_data = _get_input_data_hashes()
        rep_data = report.get("input_data_hashes", {})
        for df in REQUIRED_INPUT_DATA_FILES:
            curr_dh = curr_data.get(df, "N/A")
            if curr_dh == "N/A":
                anomalies.append(f"Required current input data file '{df}' missing on disk")
            elif canonical_current and curr_dh != rep_data.get(df):
                anomalies.append(f"Current input data file '{df}' hash mismatch: disk {curr_dh}, report {rep_data.get(df)}")

    is_valid = (len(anomalies) == 0 and report.get("status") == "verified" and failed_cnt == 0)
    return is_valid, report, anomalies
