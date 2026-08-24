"""Regression tests for architectural dependency boundaries and provenance verification."""

import copy
import hashlib
import json
import os
import pytest
from unittest.mock import patch

import certification
import research_runner
from research.handlers.base import HandlerDependencies
from research.handlers.registry import get_handler


def test_handler_execution_source_modules_includes_evaluator():
    """Verify that execution_source_modules contains both handler_modules and math_modules."""
    deps = HandlerDependencies(
        common_modules=["research_runner.py", "research/handlers/base.py"],
        handler_modules=["research/handlers/explicit_formula.py"],
        math_modules=["math_core.py", "reference_data.py"],
        material_packages=["mpmath", "flint", "numpy", "scipy"]
    )
    exec_mods = deps.execution_source_modules
    assert "research/handlers/explicit_formula.py" in exec_mods
    assert "math_core.py" in exec_mods
    assert "reference_data.py" in exec_mods
    assert "research_runner.py" not in exec_mods

    summ_mods = deps.summary_source_modules
    assert "research_runner.py" in summ_mods
    assert "research/handlers/base.py" in summ_mods
    assert "research/handlers/explicit_formula.py" in summ_mods


def test_certificate_mathematical_modules_includes_certification():
    """Verify that CERTIFICATE_MATHEMATICAL_MODULES contains certification.py."""
    assert "certification.py" in certification.CERTIFICATE_MATHEMATICAL_MODULES
    assert "math_core.py" in certification.CERTIFICATE_MATHEMATICAL_MODULES
    assert "reference_data.py" in certification.CERTIFICATE_MATHEMATICAL_MODULES
    assert "research_runner.py" not in certification.CERTIFICATE_MATHEMATICAL_MODULES


def test_evaluator_mutation_stales_execution():
    """Mutating evaluator logic in a handler module must mark historical execution stale."""
    exp_id = "centered-dilation-zero-map"
    r_dir = os.path.join(research_runner.RUNS_DIR, exp_id)
    manifest_p = os.path.join(r_dir, "manifest.json")
    if not os.path.exists(manifest_p):
        pytest.skip(f"Canonical run {exp_id} not found")

    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest_clean = copy.deepcopy(manifest)
    manifest_clean.pop("summary_provenance", None)
    ok, errors = research_runner.validate_manifest(manifest_clean, canonical_current=True)
    assert ok, f"Expected clean manifest to pass, got: {errors}"

    # Falsify evaluator code hash in manifest
    bad_manifest = copy.deepcopy(manifest_clean)
    for mod_info in bad_manifest.get("code_modules", []):
        if mod_info.get("path") == "research/handlers/centered_dilation.py":
            mod_info["sha256"] = "0" * 64
    bad_manifest["source_code_hashes"]["research/handlers/centered_dilation.py"] = "0" * 64

    ok_bad, err_bad = research_runner.validate_manifest(bad_manifest, canonical_current=True)
    assert not ok_bad
    assert len(err_bad) > 0


def test_math_module_mutation_stales_execution():
    """Mutating math_core.py must stale execution across all dependent runs."""
    exp_id = "centered-dilation-zero-map"
    r_dir = os.path.join(research_runner.RUNS_DIR, exp_id)
    manifest_p = os.path.join(r_dir, "manifest.json")
    if not os.path.exists(manifest_p):
        pytest.skip(f"Canonical run {exp_id} not found")

    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    bad_manifest = copy.deepcopy(manifest)
    for mod_info in bad_manifest.get("code_modules", []):
        if mod_info.get("path") == "math_core.py":
            mod_info["sha256"] = "f" * 64
    bad_manifest["source_code_hashes"]["math_core.py"] = "f" * 64
    bad_manifest.pop("summary_provenance", None)

    ok_bad, err_bad = research_runner.validate_manifest(bad_manifest, canonical_current=True)
    assert not ok_bad
    assert any("math_core.py" in e and "hash mismatch" in e for e in err_bad)


def test_certificate_math_mutation_stales_certificates():
    """Mathematical changes to certification.py must stale certificate validation."""
    cert_path = os.path.join(certification.ZEROS_DIR, "zero_00001.json")
    if not os.path.exists(cert_path):
        pytest.skip("Certificate zero_00001.json not found")

    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)

    # Valid certificate passes under canonical_current=True
    ok, errs = certification.verify_certificate(cert, canonical_current=True)
    assert ok, f"Expected certificate to pass, got: {errs}"

    # Falsify mathematical source hash
    bad_cert = copy.deepcopy(cert)
    bad_cert["source_code_hashes"]["math_core.py"] = "0" * 64
    bad_cert["certificate_hash"] = certification._sha256_canonical(bad_cert)

    ok_bad, errs_bad = certification.verify_certificate(bad_cert, canonical_current=True)
    assert not ok_bad
    assert any("math_core.py" in e for e in errs_bad)


def test_orchestration_change_stales_summary_only():
    """Modifying research_runner.py must invalidate summary_provenance but leave execution intact."""
    exp_id = "centered-dilation-zero-map"
    r_dir = os.path.join(research_runner.RUNS_DIR, exp_id)
    manifest_p = os.path.join(r_dir, "manifest.json")
    if not os.path.exists(manifest_p):
        pytest.skip(f"Canonical run {exp_id} not found")

    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Verify that research_runner.py is in summary_source_modules and NOT in execution_source_modules
    handler = get_handler(exp_id)
    exec_mods = handler.declared_dependencies.execution_source_modules
    summ_mods = handler.declared_dependencies.summary_source_modules
    assert "research_runner.py" not in exec_mods
    assert "research_runner.py" in summ_mods

    # If research_runner.py hash is mutated in summary_provenance, summary validation fails
    bad_manifest = copy.deepcopy(manifest)
    if "summary_provenance" in bad_manifest:
        bad_manifest["summary_provenance"]["summarizer_source_hashes"]["research_runner.py"] = "0" * 64
        ok_bad, err_bad = research_runner.validate_manifest(bad_manifest, canonical_current=True)
        assert not ok_bad
        assert any("research_runner.py" in e and "hash mismatch" in e for e in err_bad)


def test_legacy_package_provenance_incomplete_policy():
    """Boolean package values in historical manifests fail canonical-current mode and are caught."""
    exp_id = "centered-dilation-zero-map"
    r_dir = os.path.join(research_runner.RUNS_DIR, exp_id)
    manifest_p = os.path.join(r_dir, "manifest.json")
    if not os.path.exists(manifest_p):
        pytest.skip(f"Canonical run {exp_id} not found")

    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    legacy_manifest = copy.deepcopy(manifest)
    legacy_manifest["runtime"]["packages"] = {"mpmath": "1.3.0", "flint": True}  # type: ignore[dict-item]
    legacy_manifest.pop("summary_provenance", None)

    # In canonical-current mode, boolean version must be rejected
    ok_curr, err_curr = research_runner.validate_manifest(legacy_manifest, canonical_current=True)
    assert not ok_curr
    assert any("incomplete provenance" in e or "boolean rather than exact" in e for e in err_curr)

    # In historical mode, boolean version is accepted
    ok_hist, err_hist = research_runner.validate_manifest(legacy_manifest, canonical_current=False)
    assert ok_hist, f"Expected historical mode to accept legacy manifest, got: {err_hist}"


def test_summary_commit_blob_binding_validation():
    """Summary source hashes must match the exact Git blob at summary_git_commit."""
    head_commit, _ = research_runner.get_git_info()
    manifest = {
        "schema_version": "1.0.0",
        "experiment_id": "mock-run",
        "title": "Mock Run",
        "git_commit": head_commit,
        "producing_git_commit": head_commit,
        "experiment_spec_sha256": "0" * 64,
        "grid": {"total_points": 1},
        "dependency_fingerprint": certification._get_dependency_fingerprint(),
        "code_modules": [],
        "source_code_hashes": {},
        "input_data_hashes": {},
        "data_provenance": [],
        "runtime": {"packages": {"mpmath": "1.3.0", "flint": "0.6.0"}},
        "summary_provenance": {
            "summary_git_commit": head_commit,
            "summarized_at": "2026-08-24T20:00:00Z",
            "summarizer_source_hashes": {
                "research_runner.py": "0" * 64  # Falsified hash that does not match commit blob
            }
        },
        "status": "complete"
    }

    ok, errors = research_runner.validate_manifest(manifest, canonical_current=False)
    assert not ok
    assert any("git blob hash" in e and "!= recorded summary hash" in e for e in errors)


def test_evaluator_helper_source_mutation_stales_execution():
    """Real source mutation inside a top-level helper must change its evaluator hash and stale execution."""
    handler_file = "research/handlers/cross_height.py"
    certification._MODULE_MATH_HASH_CACHE.clear()
    research_runner._EVALUATOR_SOURCE_HASH_CACHE.clear()

    orig_hash = research_runner._get_evaluator_source_hash(handler_file)
    assert orig_hash is not None

    full_p = os.path.join(research_runner.REPO_ROOT, handler_file)
    with open(full_p, "r", encoding="utf-8") as f:
        src = f.read()

    assert 'if zero_family == "trivial":' in src
    mutated_src = src.replace(
        'if zero_family == "trivial":',
        'if zero_family == "MUTATED_TRIVIAL_HELPER":'
    )
    assert mutated_src != src

    import ast
    tree = ast.parse(mutated_src)
    summary_methods = {
        "compute_summary", "generate_summary", "compute_diagnostics", "generate_diagnostics", "has_diagnostics"
    }
    exec_segments = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            body_segments = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name in summary_methods:
                    continue
                seg = ast.get_source_segment(mutated_src, item)
                if seg:
                    body_segments.append(seg)
            exec_segments.append(f"class {node.name}:\n" + "\n".join(body_segments))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name not in summary_methods:
                seg = ast.get_source_segment(mutated_src, node)
                if seg:
                    exec_segments.append(seg)
        else:
            seg = ast.get_source_segment(mutated_src, node)
            if seg:
                exec_segments.append(seg)
    combined = "\n\n".join(s.replace("\r\n", "\n").strip() for s in exec_segments if s.strip())
    mutated_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()

    assert mutated_hash != orig_hash, "AST extraction failed to detect helper source mutation"


def test_handler_compute_summary_mutation_preserves_execution_and_stales_summary():
    """Mutating compute_summary changes raw module hash (staling summary) but preserves evaluator execution hash."""
    handler_file = "research/handlers/explicit_formula.py"
    certification._MODULE_MATH_HASH_CACHE.clear()
    research_runner._EVALUATOR_SOURCE_HASH_CACHE.clear()

    orig_eval_hash = research_runner._get_evaluator_source_hash(handler_file)
    assert orig_eval_hash is not None

    full_p = os.path.join(research_runner.REPO_ROOT, handler_file)
    with open(full_p, "r", encoding="utf-8") as f:
        src = f.read()

    assert '"prime_power_cutoff": 50000,' in src
    mutated_src = src.replace(
        '"prime_power_cutoff": 50000,',
        '"prime_power_cutoff": 99999,'
    )
    assert mutated_src != src

    import ast
    tree = ast.parse(mutated_src)
    summary_methods = {
        "compute_summary", "generate_summary", "compute_diagnostics", "generate_diagnostics", "has_diagnostics"
    }
    exec_segments = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            body_segments = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name in summary_methods:
                    continue
                seg = ast.get_source_segment(mutated_src, item)
                if seg:
                    body_segments.append(seg)
            exec_segments.append(f"class {node.name}:\n" + "\n".join(body_segments))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name not in summary_methods:
                seg = ast.get_source_segment(mutated_src, node)
                if seg:
                    exec_segments.append(seg)
        else:
            seg = ast.get_source_segment(mutated_src, node)
            if seg:
                exec_segments.append(seg)
    combined = "\n\n".join(s.replace("\r\n", "\n").strip() for s in exec_segments if s.strip())
    mutated_eval_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()

    assert mutated_eval_hash == orig_eval_hash, "compute_summary mutation should NOT stale execution"

    orig_raw_hash = hashlib.sha256(src.replace("\r\n", "\n").encode("utf-8")).hexdigest()
    mutated_raw_hash = hashlib.sha256(mutated_src.replace("\r\n", "\n").encode("utf-8")).hexdigest()
    assert mutated_raw_hash != orig_raw_hash, "Raw module hash must change on compute_summary mutation"


def test_certificate_verification_branch_source_mutation_stales_math_hash():
    """Real source mutation inside a certificate verification branch must change the math hash."""
    certification._MODULE_MATH_HASH_CACHE.clear()
    orig_hash = certification._get_module_math_hash("certification.py")
    assert orig_hash is not None

    for fn_name in (
        "_verify_zero_enclosure_and_isolation",
        "_verify_trivial_zero_enclosure",
        "_verify_block_isolation",
        "_verify_worldline_continuation",
        "_dispatch_and_verify_certificate",
    ):
        assert fn_name in certification.CERTIFICATE_MATHEMATICAL_FUNCTIONS

    full_p = os.path.join(certification.REPO_ROOT, "certification.py")
    with open(full_p, "r", encoding="utf-8") as f:
        src = f.read()

    assert "if not stored_im.contains(replayed_im):" in src
    mutated_src = src.replace(
        "if not stored_im.contains(replayed_im):",
        "if stored_im.contains(replayed_im):  # MUTATED_BRANCH_CHECK"
    )
    assert mutated_src != src

    import ast
    tree = ast.parse(mutated_src)
    dumps = []
    math_funcs = set(certification.CERTIFICATE_MATHEMATICAL_FUNCTIONS)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in math_funcs:
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
    mutated_hash = hashlib.sha256("\n".join(dumps).encode("utf-8")).hexdigest()
    assert mutated_hash != orig_hash, "AST extraction failed to detect verification branch source mutation"


def test_certificate_dispatch_source_mutation_stales_math_hash():
    """Real source mutation in the verification dispatch routing must change the math hash."""
    certification._MODULE_MATH_HASH_CACHE.clear()
    orig_hash = certification._get_module_math_hash("certification.py")
    assert orig_hash is not None

    full_p = os.path.join(certification.REPO_ROOT, "certification.py")
    with open(full_p, "r", encoding="utf-8") as f:
        src = f.read()

    assert 'if cert_type == "zero_isolation_and_simplicity":' in src
    mutated_src = src.replace(
        'if cert_type == "zero_isolation_and_simplicity":',
        'if cert_type == "MUTATED_INVALID_TYPE":'
    )
    assert mutated_src != src

    import ast
    tree = ast.parse(mutated_src)
    dumps = []
    math_funcs = set(certification.CERTIFICATE_MATHEMATICAL_FUNCTIONS)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in math_funcs:
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
    mutated_hash = hashlib.sha256("\n".join(dumps).encode("utf-8")).hexdigest()
    assert mutated_hash != orig_hash, "AST extraction failed to detect certificate dispatch source mutation"


def test_canonical_package_contract_independent_of_verifier_env():
    """Package verification checks canonical contract, not verifier's host Python packages."""
    exp_id = "centered-dilation-zero-map"
    r_dir = os.path.join(research_runner.RUNS_DIR, exp_id)
    manifest_p = os.path.join(r_dir, "manifest.json")
    if not os.path.exists(manifest_p):
        pytest.skip(f"Canonical run {exp_id} not found")

    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Valid canonical packages
    manifest_copy = copy.deepcopy(manifest)
    manifest_copy["runtime"]["packages"] = {"mpmath": "1.3.0", "flint": "0.6.0"}
    manifest_copy["provenance_completeness"] = "complete"
    manifest_copy["missing_material_versions"] = []
    manifest_copy.pop("summary_provenance", None)

    ok, errors = research_runner.validate_manifest(manifest_copy, canonical_current=True)
    assert ok, f"Expected manifest to pass with canonical contract, got: {errors}"

    # Invalid unsupported package version in canonical mode
    manifest_bad = copy.deepcopy(manifest)
    manifest_bad["runtime"]["packages"] = {"mpmath": "9.9.9", "flint": "0.6.0"}
    manifest_bad.pop("summary_provenance", None)
    ok_bad, err_bad = research_runner.validate_manifest(manifest_bad, canonical_current=True)
    assert not ok_bad
    assert any("mpmath" in e and "outside supported versions" in e for e in err_bad)


def test_legacy_incomplete_provenance_explicit_policy():
    """Explicit formula runs with legacy_incomplete provenance pass when declared and fail when undeclared."""
    exp_id = "explicit-formula-grade-covariance-001"
    r_dir = os.path.join(research_runner.RUNS_DIR, exp_id)
    manifest_p = os.path.join(r_dir, "manifest.json")
    if not os.path.exists(manifest_p):
        pytest.skip(f"Canonical run {exp_id} not found")

    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # 1. Declared legacy incomplete: passes
    manifest_declared = copy.deepcopy(manifest)
    manifest_declared["runtime"]["packages"] = {"mpmath": "1.3.0", "flint": "0.6.0"}
    manifest_declared["provenance_completeness"] = "legacy_incomplete"
    manifest_declared["missing_material_versions"] = ["numpy", "scipy"]
    manifest_declared.pop("summary_provenance", None)

    ok_decl, err_decl = research_runner.validate_manifest(manifest_declared, canonical_current=True)
    assert ok_decl, f"Expected declared legacy incomplete to pass, got: {err_decl}"

    # 2. Undeclared (marked complete while missing numpy/scipy): fails
    manifest_undeclared = copy.deepcopy(manifest_declared)
    manifest_undeclared["provenance_completeness"] = "complete"
    manifest_undeclared["missing_material_versions"] = []
    manifest_undeclared.pop("summary_provenance", None)

    ok_undecl, err_undecl = research_runner.validate_manifest(manifest_undeclared, canonical_current=True)
    assert not ok_undecl
    assert any("numpy" in e and "incomplete provenance" in e for e in err_undecl)
