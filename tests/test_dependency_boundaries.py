"""Regression tests for architectural dependency boundaries and provenance verification."""

import copy
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
    assert "math_core.py" not in summ_mods


def test_certificate_mathematical_modules_includes_certification():
    """Verify that CERTIFICATE_MATHEMATICAL_MODULES and CERTIFICATE_MODULE_DEPENDENCIES track certification.py."""
    assert "certification.py" in certification.CERTIFICATE_MATHEMATICAL_MODULES
    for cert_type, mods in certification.CERTIFICATE_MODULE_DEPENDENCIES.items():
        assert "certification.py" in mods, f"Certificate type {cert_type} missing certification.py dependency"


def test_evaluator_mutation_stales_execution():
    """Mutating a handler's evaluator code must flag the experiment as stale_execution."""
    handler = get_handler("cross-height-distance-001")
    exec_mods = handler.declared_dependencies.execution_source_modules
    assert "research/handlers/cross_height.py" in exec_mods

    manifest = {
        "schema_version": "1.0.0",
        "experiment_id": "cross-height-distance-001",
        "title": "Cross-Height Distance",
        "experiment_spec_sha256": "a" * 64,
        "grid": {"total_points": 3},
        "source_code_hashes": {
            "research/handlers/cross_height.py": "0" * 64,  # Faked historical hash
            "transcendental.py": certification._get_source_code_hashes(modules=["transcendental.py"]).get("transcendental.py"),
            "reference_data.py": certification._get_source_code_hashes(modules=["reference_data.py"]).get("reference_data.py"),
        },
        "input_data_hashes": certification._get_input_data_hashes(),
        "data_provenance": [
            {"path": "data/" + k, "sha256": v} for k, v in certification._get_input_data_hashes().items()
        ],
        "runtime": {"packages": {"mpmath": research_runner.get_package_version("mpmath"), "flint": research_runner.get_package_version("flint")}},
        "status": "complete"
    }

    ok, errors = research_runner.validate_manifest(manifest, canonical_current=True)
    assert not ok
    assert any("Current source module 'research/handlers/cross_height.py' hash mismatch" in e for e in errors)


def test_math_module_mutation_stales_execution():
    """Mutating math_core.py must flag depending experiments as stale_execution."""
    handler = get_handler("grade-constraints-001")
    exec_mods = handler.declared_dependencies.execution_source_modules
    assert "math_core.py" in exec_mods

    manifest = {
        "schema_version": "1.0.0",
        "experiment_id": "grade-constraints-001",
        "title": "Grade Constraints",
        "experiment_spec_sha256": "a" * 64,
        "grid": {"total_points": 105},
        "source_code_hashes": {
            "math_core.py": "0" * 64,  # Faked historical hash
            "reference_data.py": certification._get_source_code_hashes(modules=["reference_data.py"]).get("reference_data.py"),
            "research/handlers/grade_constraints.py": certification._get_source_code_hashes(modules=["research/handlers/grade_constraints.py"]).get("research/handlers/grade_constraints.py"),
        },
        "input_data_hashes": certification._get_input_data_hashes(),
        "data_provenance": [
            {"path": "data/" + k, "sha256": v} for k, v in certification._get_input_data_hashes().items()
        ],
        "runtime": {"packages": {"mpmath": research_runner.get_package_version("mpmath"), "flint": research_runner.get_package_version("flint")}},
        "status": "complete"
    }

    ok, errors = research_runner.validate_manifest(manifest, canonical_current=True)
    assert not ok
    assert any("Current source module 'math_core.py' hash mismatch" in e for e in errors)


def test_certificate_math_mutation_stales_certificates(tmp_path, monkeypatch):
    """Mutating mathematical functions in certification.py must cause load_verification_report to fail."""
    rep_path = os.path.join(certification.REPO_ROOT, "data", "certificates", "verification_report.json")
    if not os.path.exists(rep_path):
        pytest.skip("verification_report.json not found")

    with open(rep_path, "r", encoding="utf-8") as f:
        real_rep = json.load(f)

    # 1. Mutate report's source_code_hashes
    stale_rep = copy.deepcopy(real_rep)
    stale_rep["source_code_hashes"]["certification.py"] = "0" * 64

    tmp_file = str(tmp_path / "verification_report.json")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(stale_rep, f)

    is_val, rep, anomalies = certification.load_verification_report(tmp_file, canonical_current=True)
    assert not is_val
    assert any("certification.py" in a and "match" in a.lower() for a in anomalies)

    # 2. Mutate active math hash in memory
    monkeypatch.setattr(certification, "_get_module_math_hash", lambda mod, commit=None: "deadbeef" * 8 if not commit else "cafebeef" * 8)
    is_val2, rep2, anomalies2 = certification.load_verification_report(rep_path, canonical_current=True)
    assert not is_val2
    assert any("Current source module 'certification.py' mathematical component hash mismatch" in a for a in anomalies2)


def test_orchestration_change_stales_summary_only():
    """Changing research_runner.py must stale summary provenance without staling execution."""
    exp_id = "centered-dilation-zero-map"
    r_dir = os.path.join(research_runner.RUNS_DIR, exp_id)
    manifest_p = os.path.join(r_dir, "manifest.json")
    if not os.path.exists(manifest_p):
        pytest.skip(f"Canonical run {exp_id} not found")

    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Simulate runner file hash change in summary_provenance
    manifest.setdefault("summary_provenance", {}).setdefault("summarizer_source_hashes", {})
    manifest["summary_provenance"]["summarizer_source_hashes"]["research_runner.py"] = "0" * 64
    # Remove git commit check for this unit test of disk hash mismatch
    manifest["summary_provenance"].pop("summary_git_commit", None)

    ok, errors = research_runner.validate_manifest(manifest, canonical_current=True)
    assert not ok
    # Must report summarizer hash mismatch, NOT execution source mismatch
    assert any("Current summarizer source module 'research_runner.py' hash mismatch" in e for e in errors)
    assert not any("Current source module 'research_runner.py' hash mismatch" in e for e in errors)


def test_legacy_package_provenance_incomplete_policy():
    """Legacy boolean 'True' package version is rejected in current mode and flagged as anomaly historically."""
    exp_id = "centered-dilation-zero-map"
    r_dir = os.path.join(research_runner.RUNS_DIR, exp_id)
    manifest_p = os.path.join(r_dir, "manifest.json")
    if not os.path.exists(manifest_p):
        pytest.skip(f"Canonical run {exp_id} not found")

    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest_copy = copy.deepcopy(manifest)
    manifest_copy["runtime"]["packages"]["flint"] = True
    manifest_copy.pop("summary_provenance", None)

    # In canonical current mode: rejected
    ok_curr, err_curr = research_runner.validate_manifest(manifest_copy, canonical_current=True)
    assert not ok_curr
    assert any("legacy incomplete version" in e for e in err_curr)

    # In historical mode: accepted (legacy anomaly is non-fatal for historical archive)
    ok_hist, err_hist = research_runner.validate_manifest(manifest_copy, canonical_current=False)
    assert ok_hist, f"Expected ok_hist=True, got errors: {err_hist}"


def test_summary_commit_blob_binding_validation():
    """Summary provenance source hashes must match historical git blobs at summary_git_commit."""
    head_commit, _ = research_runner.get_git_info()
    manifest = {
        "schema_version": "1.0.0",
        "experiment_id": "centered-dilation-zero-map",
        "title": "Centered Dilation Zero Map",
        "experiment_spec_sha256": "a" * 64,
        "grid": {"total_points": 27},
        "source_code_hashes": certification._get_source_code_hashes(),
        "input_data_hashes": certification._get_input_data_hashes(),
        "data_provenance": [
            {"path": "data/" + k, "sha256": v} for k, v in certification._get_input_data_hashes().items()
        ],
        "runtime": {"packages": {"mpmath": research_runner.get_package_version("mpmath"), "flint": research_runner.get_package_version("flint")}},
        "summary_provenance": {
            "summary_sha256": "0" * 64,
            "readme_sha256": "0" * 64,
            "diagnostics_sha256": None,
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
