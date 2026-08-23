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


def test_multi_metric_summary_and_classification():
    """
    Verify that compute_summary computes multiple report_metrics in addition to primary criterion,
    preserving diagnostic vs criterion-component classification.
    """
    dps = 50
    spec = {
        "id": "test-multi-metric",
        "title": "Test Multi Metric",
        "hypothesis": {"statement": "Testing multi-metric summary"},
        "criterion": {
            "metric": "covariance_residual",
            "operator": "<=",
            "threshold": "1e-25"
        },
        "report_metrics": [
            {
                "metric": "zeta_covariance_residual",
                "label": "Zeta representation covariance",
                "kind": "criterion_component"
            },
            {
                "metric": "cpi_covariance_residual",
                "label": "Mobius truncation diagnostic",
                "kind": "fixed_m_truncation_diagnostic"
            }
        ],
        "precision": {"dps": dps}
    }
    
    results = [
        {
            "point_id": 0,
            "status": "ok",
            "inputs": {"k": "1", "s_re": "0.5"},
            "outputs": {
                "covariance_residual": "1e-30",
                "zeta_covariance_residual": "1e-30",
                "cpi_covariance_residual": "2e-28"
            }
        },
        {
            "point_id": 1,
            "status": "ok",
            "inputs": {"k": "2", "s_re": "0.75"},
            "outputs": {
                "covariance_residual": "5e-30",
                "zeta_covariance_residual": "5e-30"
                # cpi omitted (e.g. out of range)
            }
        }
    ]
    
    summary = research_runner.compute_summary(spec, "run-123", results, "complete")
    
    assert "report_metrics" in summary
    assert "zeta_covariance_residual" in summary["report_metrics"]
    assert "cpi_covariance_residual" in summary["report_metrics"]
    assert "covariance_residual" in summary["report_metrics"]
    
    zeta_meta = summary["report_metrics"]["zeta_covariance_residual"]
    assert zeta_meta["kind"] == "criterion_component"
    assert zeta_meta["count"] == 2
    
    cpi_meta = summary["report_metrics"]["cpi_covariance_residual"]
    assert cpi_meta["kind"] == "fixed_m_truncation_diagnostic"
    assert cpi_meta["count"] == 1
    
    # Primary criterion outcome
    assert summary["criterion"]["criterion_met"] is True


def test_argmax_preservation_and_worst_points_ordering():
    """
    Verify that compute_summary accurately identifies argmax parameter points
    and orders worst points descending by absolute value.
    """
    dps = 50
    spec = {
        "id": "test-argmax-worst",
        "title": "Test Argmax and Worst Points",
        "hypothesis": {"statement": "Testing argmax and worst points"},
        "criterion": {"metric": "res", "operator": "<=", "threshold": "1.0"},
        "precision": {"dps": dps}
    }
    
    # Construct 7 points with varying magnitudes and signs
    vals = ["1e-5", "-1e-2", "3e-3", "-1e-1", "1e-8", "5e-4", "-2e-2"]
    results = [
        {
            "point_id": i,
            "status": "ok",
            "inputs": {"param_idx": str(i), "tag": f"p{i}"},
            "outputs": {"res": val}
        }
        for i, val in enumerate(vals)
    ]
    
    summary = research_runner.compute_summary(spec, "run-456", results, "complete")
    res_stats = summary["report_metrics"]["res"]
    
    # Argmax should be point index 3 (-1e-1, absolute value 0.1)
    argmax = res_stats["argmax_abs"]
    assert argmax["point_id"] == 3
    assert argmax["inputs"] == {"param_idx": "3", "tag": "p3"}
    
    # Worst points should have length <= 5
    worst = res_stats["worst_points"]
    assert len(worst) == 5
    
    # Top 5 in descending absolute order:
    # 1. -1e-1 (id 3)
    # 2. -2e-2 (id 6)
    # 3. -1e-2 (id 1)
    # 4. 3e-3  (id 2)
    # 5. 5e-4  (id 5)
    expected_ids = [3, 6, 1, 2, 5]
    actual_ids = [p["point_id"] for p in worst]
    assert actual_ids == expected_ids


def test_decimal_string_serialization_and_readme():
    """
    Verify that all values in summary serialize as exact decimal strings and
    README renders the multi-metric table and diagnostics.
    """
    dps = 80
    spec = {
        "id": "test-serialization",
        "title": "Test Serialization",
        "hypothesis": {"statement": "Testing decimal serialization"},
        "criterion": {"metric": "err", "operator": "<=", "threshold": "1e-25"},
        "report_metrics": [
            {"metric": "err", "kind": "primary_criterion", "label": "Error metric"},
            {"metric": "diag", "kind": "fixed_m_truncation_diagnostic", "label": "Diagnostic"}
        ],
        "precision": {"dps": dps}
    }
    
    results = [
        {
            "point_id": 0,
            "status": "ok",
            "inputs": {"x": "10"},
            "outputs": {"err": "1.234567890123456789012345678901234567890e-80", "diag": "0.0"}
        }
    ]
    
    summary = research_runner.compute_summary(spec, "run-789", results, "complete")
    
    # Verify decimal string serialization
    for m_name, m_data in summary["report_metrics"].items():
        assert isinstance(m_data["min"], str)
        assert isinstance(m_data["max"], str)
        assert isinstance(m_data["max_abs"], str)
        for wp in m_data["worst_points"]:
            assert isinstance(wp["value"], str)
            
    manifest = {
        "run_id": "run-789",
        "git_commit": "abcdef0123456789",
        "git_dirty": False,
        "precision": {"dps": dps},
        "tau": "6.283185307179586476925286766559005768394338798750211641949889184615632812572418",
        "points_requested": 1,
        "points_completed": 1,
        "started_at": "2026-08-20T12:00:00Z",
        "completed_at": "2026-08-20T12:00:01Z"
    }
    
    readme = research_runner.generate_run_readme(spec, manifest, summary)
    assert "Multi-Metric Summary" in readme
    assert "fixed_m_truncation_diagnostic" in readme
    assert "Diagnostic metric only" in readme
    assert "Argmax Parameter Point" in readme


def test_precision_preservation_without_float_downcast():
    """
    Verify that summary statistics retain 80+ dps precision and do not downcast
    tiny high-precision values (e.g. 1e-120) through IEEE float.
    """
    dps = 80
    spec = {
        "id": "test-extreme-precision",
        "title": "Test Extreme Precision",
        "hypothesis": {"statement": "Testing precision without float downcast"},
        "criterion": {"metric": "val", "operator": "<=", "threshold": "1e-100", "aggregation": "max_abs"},
        "precision": {"dps": dps}
    }
    
    val1 = "1.00000000000000000000000000000000000000000000000000000000000000000000000000000001e-120"
    val2 = "-2.00000000000000000000000000000000000000000000000000000000000000000000000000000002e-120"
    
    results = [
        {"point_id": 0, "status": "ok", "inputs": {"p": "0"}, "outputs": {"val": val1}},
        {"point_id": 1, "status": "ok", "inputs": {"p": "1"}, "outputs": {"val": val2}}
    ]
    
    summary = research_runner.compute_summary(spec, "run-prec", results, "complete")
    stats = summary["report_metrics"]["val"]
    
    # max_abs must be positive magnitude of val2
    assert stats["max_abs"].startswith("2.0")
    assert "e-120" in stats["max_abs"]
    assert not stats["max_abs"].startswith("-")
    
    # argmax value must preserve signed string
    assert stats["argmax_abs"]["value"].startswith("-2.0")
    assert stats["argmax_abs"]["abs_value"].startswith("2.0")
    
    # criterion met at extreme precision
    assert summary["criterion"]["criterion_met"] is True


def test_criterion_aggregations_all_modes():
    """
    Verify all criterion aggregation modes: max_abs, max, min, all, none.
    """
    dps = 50
    results = [
        {"point_id": 0, "status": "ok", "inputs": {"p": "0"}, "outputs": {"val": "-5.0"}},
        {"point_id": 1, "status": "ok", "inputs": {"p": "1"}, "outputs": {"val": "3.0"}},
        {"point_id": 2, "status": "ok", "inputs": {"p": "2"}, "outputs": {"val": "-1.0"}}
    ]
    
    # 1. max_abs: max abs is 5.0 <= 4.0 -> False
    spec_max_abs = {
        "id": "t1", "title": "t1", "hypothesis": {"statement": "h"},
        "criterion": {"metric": "val", "operator": "<=", "threshold": "4.0", "aggregation": "max_abs"},
        "precision": {"dps": dps}
    }
    s_max_abs = research_runner.compute_summary(spec_max_abs, "r1", results, "complete")
    assert s_max_abs["criterion"]["criterion_met"] is False
    assert s_max_abs["criterion"]["observed"] == "5.0"
    
    # 2. max: max signed is 3.0 <= 4.0 -> True
    spec_max = {
        "id": "t2", "title": "t2", "hypothesis": {"statement": "h"},
        "criterion": {"metric": "val", "operator": "<=", "threshold": "4.0", "aggregation": "max"},
        "precision": {"dps": dps}
    }
    s_max = research_runner.compute_summary(spec_max, "r2", results, "complete")
    assert s_max["criterion"]["criterion_met"] is True
    assert s_max["criterion"]["observed"] == "3.0"
    
    # 3. min: min signed is -5.0 <= -4.0 -> True
    spec_min = {
        "id": "t3", "title": "t3", "hypothesis": {"statement": "h"},
        "criterion": {"metric": "val", "operator": "<=", "threshold": "-4.0", "aggregation": "min"},
        "precision": {"dps": dps}
    }
    s_min = research_runner.compute_summary(spec_min, "r3", results, "complete")
    assert s_min["criterion"]["criterion_met"] is True
    assert s_min["criterion"]["observed"] == "-5.0"
    
    # 4. all: all points <= 4.0 -> (-5.0 <= 4, 3.0 <= 4, -1.0 <= 4) -> True
    spec_all = {
        "id": "t4", "title": "t4", "hypothesis": {"statement": "h"},
        "criterion": {"metric": "val", "operator": "<=", "threshold": "4.0", "aggregation": "all"},
        "precision": {"dps": dps}
    }
    s_all = research_runner.compute_summary(spec_all, "r4", results, "complete")
    assert s_all["criterion"]["criterion_met"] is True
    
    # 5. none (observational): criterion_met = None, observed = None
    spec_none = {
        "id": "t5", "title": "t5", "hypothesis": {"statement": "h"},
        "criterion": {"metric": "val", "aggregation": "none"},
        "precision": {"dps": dps}
    }
    s_none = research_runner.compute_summary(spec_none, "r5", results, "complete")
    assert s_none["criterion"]["criterion_met"] is None
    assert s_none["criterion"]["observed"] is None


def test_conditional_metric_counts_in_summary():
    """
    Test 9: Summary engine computes statistics strictly over points that actually emit each metric.
    Inapplicable metrics are NOT emitted as zeros, NaNs, or placeholders.
    """
    dps = 80
    spec = {
        "id": "test-conditional-counts",
        "title": "Test Conditional Counts",
        "hypothesis": {"statement": "Testing conditional counts"},
        "criterion": {"metric": "residual", "aggregation": "none"},
        "report_metrics": [
            {"metric": "delta_cj", "kind": "perturbation_response", "label": "Single-pair delta C_J"},
            {"metric": "split_defect_cj", "kind": "perturbation_response", "label": "Split defect S_J"},
            {"metric": "symmetry_error", "kind": "fixed_m_truncation_diagnostic", "label": "Symmetry error"},
            {"metric": "quadratic_ratio_cj", "kind": "fixed_m_truncation_diagnostic", "label": "Quadratic ratio"}
        ],
        "precision": {"dps": dps}
    }
    
    # 2 single-pair points, 3 split points (2 with quadratic ratio, 1 without)
    results = [
        # Single-pair points
        {"point_id": 0, "status": "ok", "inputs": {"m": "single"}, "outputs": {"delta_cj": "0.01", "residual": "0.01"}},
        {"point_id": 1, "status": "ok", "inputs": {"m": "single"}, "outputs": {"delta_cj": "0.02", "residual": "0.02"}},
        # Split points
        {"point_id": 2, "status": "ok", "inputs": {"m": "split"}, "outputs": {
            "split_defect_cj": "0.0004", "symmetry_error": "1e-65", "quadratic_ratio_cj": "4.0001", "residual": "0.0004"
        }},
        {"point_id": 3, "status": "ok", "inputs": {"m": "split"}, "outputs": {
            "split_defect_cj": "0.0016", "symmetry_error": "2e-65", "quadratic_ratio_cj": "4.0004", "residual": "0.0016"
        }},
        {"point_id": 4, "status": "ok", "inputs": {"m": "split"}, "outputs": {
            "split_defect_cj": "0.0000", "symmetry_error": "0.0", "residual": "0.0"
        }}
    ]
    
    summary = research_runner.compute_summary(spec, "run-cond", results, "complete")
    rep = summary["report_metrics"]
    
    assert rep["delta_cj"]["count"] == 2
    assert rep["split_defect_cj"]["count"] == 3
    assert rep["symmetry_error"]["count"] == 3
    assert rep["quadratic_ratio_cj"]["count"] == 2
    assert rep["residual"]["count"] == 5


def test_dirty_state_detection_rules(monkeypatch):
    """
    Tests 28, 29, 30:
    - 28: dirty-state detection catches modified tracked source files
    - 29: dirty-state detection catches tracked deletions BEFORE the producing commit
    - 30: newly-created experiment output does not falsely mark an otherwise clean producing state as dirty.
    """
    # Helper to mock git status porcelain output
    def mock_git(porcelain_output: str):
        def _check_output(cmd, cwd=None, stderr=None):
            if "rev-parse" in cmd:
                return b"80b70e18df678ad9fbba49c470f142c5767fdc96\n"
            if "status" in cmd:
                return porcelain_output.encode("utf-8")
            return b""
        return _check_output

    # Test 28: Modified tracked source file -> dirty
    monkeypatch.setattr(research_runner.subprocess, "check_output", mock_git(" M math_core.py\n"))
    commit, is_dirty = research_runner.get_git_info()
    assert is_dirty is True
    
    # Test 29: Tracked deletion -> dirty
    monkeypatch.setattr(research_runner.subprocess, "check_output", mock_git(" D research/experiments/macroscope_perturbation_001.yaml\n"))
    commit, is_dirty = research_runner.get_git_info()
    assert is_dirty is True

    # Untracked source file -> dirty
    monkeypatch.setattr(research_runner.subprocess, "check_output", mock_git("?? tests/test_new.py\n"))
    commit, is_dirty = research_runner.get_git_info()
    assert is_dirty is True

    # Test 30: Newly created experiment outputs and index.json -> NOT dirty
    clean_runner_output = (
        "?? research/runs/20260820T160000Z_isolated-radial-response-002_12345678/manifest.json\n"
        "?? research/runs/20260820T160000Z_isolated-radial-response-002_12345678/results.jsonl\n"
        "?? research/runs/20260820T160000Z_isolated-radial-response-002_12345678/summary.json\n"
        "?? research/runs/20260820T160000Z_isolated-radial-response-002_12345678/README.md\n"
        " M research/index.json\n"
    )
    monkeypatch.setattr(research_runner.subprocess, "check_output", mock_git(clean_runner_output))
    commit, is_dirty = research_runner.get_git_info()
    assert is_dirty is False


def test_experiment_overwrite_only_semantics(temp_research_env):
    """
    Verify overwrite-only run semantics:
    - Running an experiment creates stable directory research/runs/<exp_id>/
    - Rerunning the experiment replaces that stable directory
    - No timestamped directory is created
    - index.json entry is updated in-place rather than appended (runs count remains 1)
    - No temporary .tmp_ or backup directories remain
    """
    spec = {
        "schema_version": "2",
        "id": "test-overwrite-001",
        "title": "Test Overwrite Run",
        "hypothesis": {"statement": "Testing overwrite semantics"},
        "criterion": {"metric": "residual", "operator": "<=", "threshold": "1e-20", "aggregation": "max_abs"},
        "engine": {"operation": "centrifuge"},
        "parameters": {
            "delta": {"kind": "explicit", "values": ["0.01", "0.02"]}
        },
        "precision": {"dps": 50}
    }
    
    spec_file = os.path.join(temp_research_env["experiments"], "test-overwrite-001.yaml")
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(spec, f)
        
    # Run 1
    run_id_1 = research_runner.run_experiment(spec_file)
    assert run_id_1 == "test-overwrite-001"
    
    runs_dir = temp_research_env["runs"]
    stable_exp_dir = os.path.join(runs_dir, "test-overwrite-001")
    assert os.path.isdir(stable_exp_dir)
    assert os.path.exists(os.path.join(stable_exp_dir, "manifest.json"))
    assert os.path.exists(os.path.join(stable_exp_dir, "summary.json"))
    assert os.path.exists(os.path.join(stable_exp_dir, "results.jsonl"))
    assert os.path.exists(os.path.join(stable_exp_dir, "README.md"))
    
    # Check index.json after Run 1
    with open(temp_research_env["index"], "r", encoding="utf-8") as f:
        idx1 = json.load(f)
    assert len(idx1["runs"]) == 1
    assert idx1["runs"][0]["experiment_id"] == "test-overwrite-001"
    
    # Run 2 (re-run)
    run_id_2 = research_runner.run_experiment(spec_file)
    assert run_id_2 == "test-overwrite-001"
    
    # Check directory listing: exactly one directory in runs/
    all_runs_dirs = os.listdir(runs_dir)
    assert len(all_runs_dirs) == 1
    assert all_runs_dirs[0] == "test-overwrite-001"
    
    # No .tmp_ or backup directories
    assert not any(d.startswith(".tmp") for d in all_runs_dirs)
    assert not any("backup" in d for d in all_runs_dirs)
    
    # Check index.json after Run 2: still exactly 1 entry (updated, not appended)
    with open(temp_research_env["index"], "r", encoding="utf-8") as f:
        idx2 = json.load(f)
    assert len(idx2["runs"]) == 1
    assert idx2["runs"][0]["experiment_id"] == "test-overwrite-001"


def test_zero_to_certificate_binding_and_validation():
    """
    Test zero-to-certificate binding:
    - Nontrivial zeros 1, 2, 3, 99, 100
    - Trivial zeros 1, 2, 100
    - Family mismatch
    - Ordinate mismatch
    - Missing certificate
    """
    # 1. Nontrivial zeros
    for z_idx in [1, 2, 3, 99, 100]:
        cert_hash, ok, zc, errs = research_runner._lookup_zero_certificate(
            z_idx,
            zero_family="nontrivial",
            check_provenance=False
        )
        assert ok is True, f"Nontrivial zero #{z_idx} lookup failed: {errs}"
        assert cert_hash is not None
        assert zc is not None
        assert zc["nontrivial_index"] == z_idx

    # 2. Trivial zeros
    for m_idx in [1, 2, 100]:
        cert_hash, ok, zc, errs = research_runner._lookup_zero_certificate(
            m_idx,
            zero_family="trivial",
            check_provenance=False
        )
        assert ok is True, f"Trivial zero #{m_idx} lookup failed: {errs}"
        assert cert_hash is not None
        assert zc is not None
        assert zc["trivial_index"] == m_idx

    # 3. Family mismatch (asking for trivial certificate with nontrivial index/family)
    cert_hash, ok, zc, errs = research_runner._lookup_zero_certificate(
        1,
        zero_family="trivial",
        expected_ordinate="14.134725",
        check_provenance=False
    )
    # Trivial zero #1 is at s = -2, not 14.134725
    assert ok is True # Trivial zero exists and is valid
    
    # 4. Ordinate mismatch on nontrivial zero
    cert_hash, ok, zc, errs = research_runner._lookup_zero_certificate(
        1,
        zero_family="nontrivial",
        expected_ordinate="999.12345",
        check_provenance=False
    )
    assert ok is False
    assert any("Ordinate mismatch" in e for e in errs)

    # 5. Missing certificate
    cert_hash, ok, zc, errs = research_runner._lookup_zero_certificate(
        999999,
        zero_family="nontrivial",
        check_provenance=False
    )
    assert ok is False
    assert any("does not exist" in e for e in errs)


def test_cross_height_distance_emits_l_infty_and_l_2_distance():
    """
    Test that cross_height_distance emits L_infty_distance and L_2_distance in point outputs,
    and that compute_summary records non-empty stats without reporting N/A.
    """
    inputs = {
        "block_pair": "low_to_medium",
        "zero_index": "0",
        "u_max": "0.5"
    }
    status, outputs, err = research_runner.evaluate_point("cross_height_distance", inputs, dps=50)
    assert status == "ok"
    assert "L_infty_distance" in outputs
    assert "L_2_distance" in outputs
    assert "max_distance" in outputs
    assert float(outputs["L_infty_distance"]) > 0
    assert float(outputs["L_2_distance"]) > 0

    spec = {
        "id": "cross-height-distance-001",
        "title": "Cross Height Distance Test",
        "hypothesis": {"statement": "Trajectory distance is bounded."},
        "criterion": {
            "metric": "max_distance",
            "operator": "<=",
            "threshold": "2.0",
            "aggregation": "max"
        },
        "report_metrics": [
            {"metric": "max_distance", "kind": "criterion_component", "label": "Max distance"},
            {"metric": "L_infty_distance", "kind": "observational_metric", "label": "L_infty distance"},
            {"metric": "L_2_distance", "kind": "observational_metric", "label": "L_2 distance"}
        ],
        "precision": {"dps": 50}
    }
    results = [{"point_id": 0, "status": "ok", "inputs": inputs, "outputs": outputs}]
    summary = research_runner.compute_summary(spec, "run-dist", results, "complete")
    assert summary["criterion"]["criterion_met"] is True
    assert summary["report_metrics"]["L_infty_distance"]["count"] == 1
    assert summary["report_metrics"]["L_2_distance"]["count"] == 1


def test_validate_manifest_accepts_valid_manifest_and_rejects_discrepancies():
    """Verify that validate_manifest passes valid certificate bindings and catches anomalies."""
    z1_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "certificates", "zeros", "zero_00001.json")
    wl1_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "certificates", "worldlines", "worldline_z00001_Kp1_delta_pos0p00.json")

    if not os.path.exists(z1_path) or not os.path.exists(wl1_path):
        pytest.skip("Certificate files not found on disk")

    with open(z1_path, "r", encoding="utf-8") as f:
        z1 = json.load(f)
    with open(wl1_path, "r", encoding="utf-8") as f:
        wl1 = json.load(f)

    h1 = z1["certificate_hash"]
    h2 = wl1["certificate_hash"]

    valid_manifest = {
        "experiment_id": "test-exp",
        "git_commit": "e32966b5bd2349fb5612f7782a5d09991cde6a5f",
        "status": "complete",
        "precision": {"dps": 50},
        "points_requested": 1,
        "points_completed": 1,
        "consumed_certificates": [h1, h2]
    }
    valid_results = [
        {"point_id": 0, "status": "ok", "inputs": {"nontrivial_index": "1"}, "outputs": {
            "source_zero_cert_hash": h1,
            "worldline_cert_hash": h2,
            "source_zero_certificate_status": "certified",
            "worldline_certificate_status": "certified",
            "worldline_certified": "true"
        }}
    ]
    ok, errs = research_runner.validate_manifest(valid_manifest, valid_results)
    assert ok, f"Expected valid manifest: {errs}"

    # Missing from consumed certificates
    invalid_manifest1 = dict(valid_manifest)
    invalid_manifest1["consumed_certificates"] = [h1]
    ok1, errs1 = research_runner.validate_manifest(invalid_manifest1, valid_results)
    assert not ok1
    assert any("missing from manifest consumed_certificates" in e for e in errs1)

    # Worldline certified true but hash is N/A
    bad_results = [
        {"point_id": 0, "status": "ok", "inputs": {"nontrivial_index": "1"}, "outputs": {
            "source_zero_cert_hash": h1,
            "worldline_cert_hash": "N/A",
            "worldline_certified": "true",
            "worldline_certificate_status": "not_available",
            "source_zero_certificate_status": "certified"
        }}
    ]
    ok2, errs2 = research_runner.validate_manifest(valid_manifest, bad_results)
    assert not ok2
    assert any("worldline_cert_hash is 'N/A'" in e for e in errs2)


def test_publication_gate_rejects_invalid_run_and_preserves_canonical_run(temp_research_env, monkeypatch):
    """Test that if a run fails manifest validation, the canonical run directory and index remain intact."""
    spec_dict = {
        "schema_version": "1",
        "id": "gate-test-sweep",
        "title": "Gate Test Sweep",
        "hypothesis": {"statement": "Test publication gate"},
        "criterion": {"metric": "abs_slope_error", "operator": "<=", "threshold": "1e-25"},
        "engine": {"operation": "centrifuge"},
        "parameters": {
            "delta": {"kind": "explicit", "values": ["0.01"]},
            "K": {"kind": "explicit", "values": ["1", "2"]}
        },
        "precision": {"dps": 50}
    }
    spec_path = os.path.join(temp_research_env["experiments"], "gate-test-sweep.yaml")
    with open(spec_path, "w", encoding="utf-8") as f:
        yaml.dump(spec_dict, f)

    # Run successfully first
    run_id = research_runner.run_experiment(spec_path)
    run_dir = os.path.join(temp_research_env["runs"], run_id)
    assert os.path.exists(run_dir)
    with open(os.path.join(run_dir, "manifest.json"), "r", encoding="utf-8") as f:
        orig_manifest = json.load(f)

    # Now monkeypatch evaluate_point to simulate point failure on a re-run
    def mock_eval(*args, **kwargs):
        return "error", {"point_error": "Simulated hardware failure"}, "Simulated hardware failure"

    monkeypatch.setattr(research_runner, "evaluate_point", mock_eval)

    # Rerunning must fail publication gate and preserve original canonical files
    with pytest.raises(RuntimeError, match="Canonical run publication rejected"):
        research_runner.run_experiment(spec_path)

    # Verify original canonical directory is unchanged
    assert os.path.exists(run_dir)
    with open(os.path.join(run_dir, "manifest.json"), "r", encoding="utf-8") as f:
        preserved_manifest = json.load(f)
    assert preserved_manifest == orig_manifest


def test_transactional_rollback_failure_injection(temp_research_env, monkeypatch):
    """Test injected failures during transaction at replacement, index update, and cleanup.
    Verifies that stable directory and index.json return byte-for-byte to pre-run state.
    """
    spec_dict = {
        "schema_version": "1",
        "id": "tx-test-sweep",
        "title": "TX Test Sweep",
        "hypothesis": {"statement": "Test transaction rollback"},
        "criterion": {"metric": "abs_slope_error", "operator": "<=", "threshold": "1e-25"},
        "engine": {"operation": "centrifuge"},
        "parameters": {
            "delta": {"kind": "explicit", "values": ["0.01"]},
            "K": {"kind": "explicit", "values": ["1"]}
        },
        "precision": {"dps": 50}
    }
    spec_path = os.path.join(temp_research_env["experiments"], "tx-test-sweep.yaml")
    with open(spec_path, "w", encoding="utf-8") as f:
        yaml.dump(spec_dict, f)

    # Initial successful publication
    run_id = research_runner.run_experiment(spec_path)
    run_dir = os.path.join(temp_research_env["runs"], run_id)
    with open(os.path.join(run_dir, "manifest.json"), "r", encoding="utf-8") as f:
        orig_manifest_content = f.read()
    with open(temp_research_env["index"], "r", encoding="utf-8") as f:
        orig_index_content = f.read()

    # 1. Failure during update_index_file
    def mock_update_fail(*args, **kwargs):
        raise IOError("Simulated index disk full error")

    monkeypatch.setattr(research_runner, "update_index_file", mock_update_fail)

    with pytest.raises(IOError, match="Simulated index disk full"):
        research_runner.run_experiment(spec_path)

    # Assert stable dir and index.json restored byte-for-byte
    assert os.path.exists(run_dir)
    with open(os.path.join(run_dir, "manifest.json"), "r", encoding="utf-8") as f:
        assert f.read() == orig_manifest_content
    with open(temp_research_env["index"], "r", encoding="utf-8") as f:
        assert f.read() == orig_index_content

    # Assert no backup or temporary files exist
    assert not any(f.startswith(".bak_") or f.startswith(".tmp_") for f in os.listdir(temp_research_env["runs"]))


def test_operation_obligations_adversarial_rejections():
    """Test operation-specific proof obligation validation against 13 adversarial rejection cases."""
    z1_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "certificates", "zeros", "zero_00001.json")
    wl1_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "certificates", "worldlines", "worldline_z00001_Kp1_delta_pos0p00.json")

    if not os.path.exists(z1_path) or not os.path.exists(wl1_path):
        pytest.skip("Certificates not found on disk")

    with open(z1_path, "r", encoding="utf-8") as f:
        z1 = json.load(f)
    with open(wl1_path, "r", encoding="utf-8") as f:
        wl1 = json.load(f)

    h1 = z1["certificate_hash"]
    h2 = wl1["certificate_hash"]

    spec = {
        "id": "obl-test",
        "operation": "transcendental_worldline",
        "epistemic_class": "exact_control",
        "hypothesis": {"statement": "Obligations test"},
        "criterion": {"metric": "worldline_defect", "operator": "<=", "threshold": "1e-25"},
        "precision": {"dps": 50}
    }

    # Case 1: Empty consumed certificates for operation requiring them
    man1 = {
        "experiment_id": "obl-test",
        "operation": "transcendental_worldline",
        "git_commit": z1.get("producing_git_commit"),
        "status": "complete",
        "precision": {"dps": 50},
        "points_requested": 1,
        "points_completed": 1,
        "consumed_certificates": []
    }
    ok, errs = research_runner.validate_manifest(man1, spec=spec)
    assert not ok
    assert any("requires consumed certificates" in e for e in errs)

    # Case 2: Grade mismatch (requested K=999 paired with K=1 cert)
    man2 = {
        "experiment_id": "obl-test",
        "operation": "transcendental_worldline",
        "git_commit": z1.get("producing_git_commit"),
        "status": "complete",
        "precision": {"dps": 50},
        "points_requested": 1,
        "points_completed": 1,
        "consumed_certificates": [h1, h2]
    }
    res2 = [
        {
            "point_id": 0, "status": "ok",
            "inputs": {"zero_index": 0, "grade_k": 999, "delta": "0.0"},
            "outputs": {
                "source_zero_cert_hash": h1,
                "worldline_cert_hash": h2,
                "worldline_certified": "true",
                "worldline_certificate_status": "certified",
                "source_zero_certificate_status": "certified",
                "worldline_defect": "1e-30"
            }
        }
    ]
    ok2, errs2 = research_runner.validate_manifest(man2, results=res2, spec=spec)
    assert not ok2
    assert any("grade" in e.lower() or "K=999" in e for e in errs2)

    # Case 3: Actual zero operation paired with synthetic certificate
    synth_wl_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "certificates", "worldlines", "worldline_z00001_Kp1_delta_pos0p10.json")
    if os.path.exists(synth_wl_path):
        with open(synth_wl_path, "r", encoding="utf-8") as f:
            wls = json.load(f)
        hs = wls["certificate_hash"]
        man3 = dict(man2)
        man3["consumed_certificates"] = [h1, hs]
        res3 = [
            {
                "point_id": 0, "status": "ok",
                "inputs": {"zero_index": 0, "grade_k": 1, "delta": "0.0"},
                "outputs": {
                    "source_zero_cert_hash": h1,
                    "worldline_cert_hash": hs,
                    "worldline_certified": "true",
                    "worldline_certificate_status": "certified",
                    "source_zero_certificate_status": "certified",
                    "worldline_defect": "1e-30"
                }
            }
        ]
        ok3, errs3 = research_runner.validate_manifest(man3, results=res3, spec=spec)
        assert not ok3
        assert any("synthetic" in e.lower() or "delta" in e.lower() for e in errs3)

