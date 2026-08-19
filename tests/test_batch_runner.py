"""
tests/test_batch_runner.py — Comprehensive Tests for Batch Sweep Runner Infrastructure

Tests all requirements from EXPERIMENT_PROTOCOL.md and prompt:
- YAML validation
- Deterministic explicit/linear/log expansion
- Cartesian-product ordering
- Decimal-string precision preservation
- Stable point IDs
- Spec SHA hashing
- Git SHA and dirty-state capture
- Incremental JSONL persistence
- Incomplete-run semantics
- Resume and resume refusal for mismatched state
- Deterministic summaries and criterion evaluation
- Index updates
- Interactive-engine vs batch-engine equality
"""

import os
import json
import yaml
import shutil
import tempfile
import pytest
import mpmath

import research_runner
import math_core
import transforms


@pytest.fixture
def temp_research_env(tmp_path, monkeypatch):
    """Set up temporary research directory environment for isolated testing."""
    res_dir = tmp_path / "research"
    exp_dir = res_dir / "experiments"
    runs_dir = res_dir / "runs"
    exp_dir.mkdir(parents=True)
    runs_dir.mkdir(parents=True)
    
    index_file = res_dir / "index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump([], f)
        
    monkeypatch.setattr(research_runner, "RESEARCH_DIR", str(res_dir))
    monkeypatch.setattr(research_runner, "EXPERIMENTS_DIR", str(exp_dir))
    monkeypatch.setattr(research_runner, "RUNS_DIR", str(runs_dir))
    monkeypatch.setattr(research_runner, "INDEX_FILE", str(index_file))
    
    return {
        "root": tmp_path,
        "research": res_dir,
        "experiments": exp_dir,
        "runs": runs_dir,
        "index": index_file
    }


def test_spec_validation():
    """Verify spec validation accepts valid specs and rejects malformed specs."""
    valid_spec = {
        "schema_version": "1",
        "id": "test-exp-001",
        "title": "Test Valid Exp",
        "hypothesis": {"statement": "Test hypothesis"},
        "criterion": {"metric": "abs_slope_error", "operator": "<=", "threshold": "1e-30"},
        "engine": {"operation": "centrifuge"},
        "parameters": {
            "delta": {"kind": "explicit", "values": ["0.001"]}
        },
        "precision": {"dps": 80}
    }
    is_valid, err = research_runner.validate_spec(valid_spec)
    assert is_valid, f"Validation failed on valid spec: {err}"
    
    # Missing hypothesis
    bad_spec1 = dict(valid_spec)
    del bad_spec1["hypothesis"]
    is_valid, err = research_runner.validate_spec(bad_spec1)
    assert not is_valid
    
    # Invalid operator
    bad_spec2 = dict(valid_spec)
    bad_spec2["criterion"] = {"metric": "res", "operator": "APPROX", "threshold": "0.1"}
    is_valid, err = research_runner.validate_spec(bad_spec2)
    assert not is_valid
    
    # Unknown engine operation
    bad_spec3 = dict(valid_spec)
    bad_spec3["engine"] = {"operation": "non_existent_engine_op"}
    is_valid, err = research_runner.validate_spec(bad_spec3)
    assert not is_valid


def test_parameter_expansion_and_cartesian_product():
    """Verify deterministic explicit, linear, log parameter expansion and Cartesian product."""
    dps = 50
    # Explicit
    exp_def = {"kind": "explicit", "values": ["0.1", "0.2", "0.3"]}
    expanded_exp = research_runner.expand_parameter(exp_def, dps=dps)
    assert expanded_exp == ["0.1", "0.2", "0.3"]
    
    # Linear with exact decimal values
    lin_def = {"kind": "linear", "start": "0.0", "stop": "1.0", "step": "0.25"}
    expanded_lin = research_runner.expand_parameter(lin_def, dps=dps)
    assert len(expanded_lin) == 5
    assert mpmath.mpf(expanded_lin[0]) == mpmath.mpf("0.0")
    assert mpmath.mpf(expanded_lin[-1]) == mpmath.mpf("1.0")
    
    # Log
    log_def = {"kind": "log", "base": "10", "exponents": ["-2", "-1", "0"]}
    expanded_log = research_runner.expand_parameter(log_def, dps=dps)
    assert len(expanded_log) == 3
    assert mpmath.mpf(expanded_log[0]) == mpmath.mpf("0.01")
    assert mpmath.mpf(expanded_log[1]) == mpmath.mpf("0.1")
    assert mpmath.mpf(expanded_log[2]) == mpmath.mpf("1.0")
    
    # Cartesian product ordering
    params_def = {
        "p1": {"kind": "explicit", "values": ["A", "B"]},
        "p2": {"kind": "explicit", "values": ["1", "2", "3"]}
    }
    grid = research_runner.generate_parameter_grid(params_def, dps=dps)
    assert len(grid) == 6
    assert grid[0] == {"p1": "A", "p2": "1"}
    assert grid[1] == {"p1": "A", "p2": "2"}
    assert grid[2] == {"p1": "A", "p2": "3"}
    assert grid[3] == {"p1": "B", "p2": "1"}
    assert grid[4] == {"p1": "B", "p2": "2"}
    assert grid[5] == {"p1": "B", "p2": "3"}


def test_spec_hashing_and_git_capture():
    """Verify spec SHA-256 hashing and git commit capture."""
    sample_text = "schema_version: '1'\nid: test\n"
    h1 = research_runner.hash_string(sample_text)
    h2 = research_runner.hash_string(sample_text)
    assert h1 == h2
    assert len(h1) == 64
    
    commit, is_dirty = research_runner.get_git_info()
    assert isinstance(commit, str)
    assert len(commit) > 0
    assert isinstance(is_dirty, bool)


def test_experiment_run_and_artifacts(temp_research_env):
    """Execute a small sweep and verify manifest.json, results.jsonl, summary.json, README.md."""
    spec_dict = {
        "schema_version": "1",
        "id": "centrifuge-test-sweep",
        "title": "Centrifuge Unit Test Sweep",
        "hypothesis": {"statement": "log|q_rho^K| is linear in K with slope delta*ln(tau)"},
        "criterion": {"metric": "abs_slope_error", "operator": "<=", "threshold": "1e-25"},
        "engine": {"operation": "centrifuge"},
        "parameters": {
            "delta": {"kind": "explicit", "values": ["0.001", "0.01"]},
            "gamma": {"kind": "explicit", "values": ["14.13472514173469379045725198356247027078425711569924317568556746"]},
            "K": {"kind": "explicit", "values": ["-10", "0", "10"]}
        },
        "precision": {"dps": 50},
        "outputs": {"retain_points": True}
    }

    spec_path = os.path.join(temp_research_env["experiments"], "centrifuge-test-sweep.yaml")
    with open(spec_path, "w", encoding="utf-8") as f:
        yaml.dump(spec_dict, f)
        
    run_id = research_runner.run_experiment(spec_path)
    run_dir = os.path.join(temp_research_env["runs"], run_id)
    
    # 1. Verify manifest.json
    manifest_path = os.path.join(run_dir, "manifest.json")
    assert os.path.exists(manifest_path)
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["status"] == "complete"
    assert manifest["points_requested"] == 6
    assert manifest["points_completed"] == 6
    assert "tau" in manifest
    assert manifest["git_commit"] is not None
    
    # 2. Verify results.jsonl
    results_path = os.path.join(run_dir, "results.jsonl")
    assert os.path.exists(results_path)
    lines = []
    with open(results_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                lines.append(json.loads(line))
    assert len(lines) == 6
    for i, pt in enumerate(lines):
        assert pt["point_id"] == i
        assert pt["status"] == "ok"
        assert "log_modulus" in pt["outputs"]
        
    # 3. Verify summary.json
    summary_path = os.path.join(run_dir, "summary.json")
    assert os.path.exists(summary_path)
    with open(summary_path, "r", encoding="utf-8") as f:
        summary = json.load(f)
    assert summary["status"] == "complete"
    assert summary["points_completed"] == 6
    assert summary["criterion"]["criterion_met"] is True
    assert "supports_rh" not in summary
    assert "proof_progress" not in summary
    
    # 4. Verify README.md
    readme_path = os.path.join(run_dir, "README.md")
    assert os.path.exists(readme_path)
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()
    assert "Centrifuge Unit Test Sweep" in readme
    assert "CRITERION MET" in readme
    
    # 5. Verify index.json
    runs = research_runner.list_runs()
    assert len(runs) == 1
    assert runs[0]["run_id"] == run_id
    assert runs[0]["criterion_met"] is True


def test_resume_and_refusal_semantics(temp_research_env):
    """Test resume execution skips completed points, and refuses mismatched state."""
    spec_dict = {
        "schema_version": "1",
        "id": "resume-test-sweep",
        "title": "Resume Test Sweep",
        "hypothesis": {"statement": "Test resume functionality"},
        "criterion": {"metric": "abs_slope_error", "operator": "<=", "threshold": "1e-25"},
        "engine": {"operation": "centrifuge"},
        "parameters": {
            "delta": {"kind": "explicit", "values": ["0.001", "0.01"]},
            "K": {"kind": "explicit", "values": ["1", "2", "3", "4"]}
        },
        "precision": {"dps": 50}
    }
    spec_path = os.path.join(temp_research_env["experiments"], "resume-test-sweep.yaml")
    with open(spec_path, "w", encoding="utf-8") as f:
        yaml.dump(spec_dict, f)
        
    # Simulate a partial run by running 1st time, then truncating results.jsonl to 3 points
    run_id = research_runner.run_experiment(spec_path)
    run_dir = os.path.join(temp_research_env["runs"], run_id)
    results_path = os.path.join(run_dir, "results.jsonl")
    
    with open(results_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 8
    
    # Truncate to 3 points and set status back to running
    with open(results_path, "w", encoding="utf-8") as f:
        f.writelines(lines[:3])
        
    manifest_path = os.path.join(run_dir, "manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    manifest["status"] = "running"
    manifest["points_completed"] = 3
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    # Resume the partial run
    resumed_run_id = research_runner.run_experiment(spec_path, resume_run_id=run_id)
    assert resumed_run_id == run_id
    
    with open(results_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    assert len(all_lines) == 8  # Appended the remaining 5 points
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        final_manifest = json.load(f)
    assert final_manifest["status"] == "complete"
    assert final_manifest["points_completed"] == 8
    
    # Test refusal when spec hash differs
    modified_spec_dict = dict(spec_dict)
    modified_spec_dict["title"] = "Modified Title Changes Hash"
    modified_spec_path = os.path.join(temp_research_env["experiments"], "modified-spec.yaml")
    with open(modified_spec_path, "w", encoding="utf-8") as f:
        yaml.dump(modified_spec_dict, f)
        
    with pytest.raises(ValueError, match="Spec hash mismatch"):
        research_runner.run_experiment(modified_spec_path, resume_run_id=run_id)


def test_interactive_engine_vs_batch_engine_parity():
    """
    Verify that point evaluation in research_runner produces the identical
    mathematical value as direct interactive module evaluation.
    """
    dps = 60
    delta_str = "0.005"
    k_str = "12.5"
    gamma_str = "14.134725141734693790457251983562"
    
    with mpmath.workdps(dps + 10):
        # 1. Batch runner evaluation
        inputs = {"delta": delta_str, "k": k_str, "gamma": gamma_str}
        status, outputs, err = research_runner.evaluate_point("centrifuge", inputs, dps=dps)
        assert status == "ok"
        batch_log_mod = mpmath.mpf(outputs["log_modulus"])
        
        # 2. Canonical math_core evaluation
        direct_log_mod = math_core.centrifuge_log_modulus(delta_str, k_str, dps=dps)
        
        assert abs(batch_log_mod - direct_log_mod) < mpmath.mpf("1e-50")

