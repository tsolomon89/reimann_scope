"""tests/test_workflow.py — Tests for the Authoritative Workflow CLI (scripts/workflow.py)"""

from __future__ import annotations

import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts import workflow
import research_runner


def test_workflow_plan_canonical_structure():
    """Verify that plan_canonical_regeneration returns structured plan with all experiments."""
    plan = workflow.plan_canonical_regeneration()
    assert "head_commit" in plan
    assert "is_dirty" in plan
    assert "certificates" in plan
    assert "runs" in plan
    assert len(plan["runs"]) == 17
    assert all("experiment_id" in r and "points" in r for r in plan["runs"])


def test_workflow_validate_artifacts_read_only():
    """Verify validate_artifacts validates current artifacts without errors."""
    code = workflow.run_validate_artifacts(canonical_current=False)
    assert code == 0


def test_workflow_run_canonical_refuses_dirty_worktree(monkeypatch):
    """Verify run_canonical fails closed when worktree is dirty unless allow_dirty is passed."""
    monkeypatch.setattr(research_runner, "get_git_info", lambda: ("fakecommit123", True))
    code = workflow.run_canonical(allow_dirty=False)
    assert code == 1

    # When allow_dirty is True, mock runner calls to verify workflow orchestration
    monkeypatch.setattr(workflow.subprocess, "run", lambda *a, **kw: type("MockRes", (), {"returncode": 0})())
    monkeypatch.setattr(research_runner, "run_experiment", lambda sf, **kw: "centrifuge-slope-verification")
    monkeypatch.setattr(research_runner, "summarize_run", lambda r_id, **kw: {"status": "complete", "criterion": {"criterion_met": True, "observed": "0.0"}})
    monkeypatch.setattr(workflow, "run_validate_artifacts", lambda **kw: 0)
    code_allowed = workflow.run_canonical(allow_dirty=True, experiments=["centrifuge-slope-verification"])
    assert code_allowed == 0


def test_workflow_plan_inspects_component_states():
    """Verify inspect_canonical_state distinguishes execution and summary status."""
    state = workflow.inspect_canonical_state()
    assert "certificates" in state
    assert "formal_report" in state
    assert "runs" in state
    assert "total_execution_points" in state
    assert "total_resummarize_runs" in state
    assert len(state["runs"]) == 17
    for r in state["runs"]:
        assert r["overall_status"] in ("current", "stale_execution", "stale_summary", "missing", "invalid")
        assert r["execution_status"] in ("execution_current", "stale_execution", "missing", "invalid")
        assert r["summary_status"] in ("summary_current", "stale_summary", "missing", "invalid")


def test_workflow_selective_resummarize_without_rerun(monkeypatch):
    """Verify that when only summary is stale, run_canonical calls summarize_run and not run_experiment."""
    calls = []

    def mock_inspect(target_experiments=None):
        return {
            "head_commit": "fake_commit",
            "is_dirty": False,
            "certificates": {"status": "current", "stale_reasons": []},
            "formal_report": {"status": "current", "theorems": 19, "stale_reasons": []},
            "runs": [{
                "experiment_id": "explicit-formula-grade-covariance-001",
                "spec_file": "research/experiments/explicit-formula-grade-covariance-001.yaml",
                "points": 30,
                "execution_status": "execution_current",
                "summary_status": "stale_summary",
                "overall_status": "stale_summary",
                "needs_execution": False,
                "needs_summary": True,
                "reasons": ["Stale diagnostics"]
            }],
            "total_execution_points": 0,
            "total_resummarize_runs": 1
        }

    monkeypatch.setattr(workflow, "inspect_canonical_state", mock_inspect)
    monkeypatch.setattr(research_runner, "get_git_info", lambda: ("fake_commit", False))
    monkeypatch.setattr(research_runner, "run_experiment", lambda sf, **kw: calls.append(("run_experiment", sf)))
    monkeypatch.setattr(research_runner, "summarize_run", lambda r_id, **kw: calls.append(("summarize_run", r_id)) or {"status": "complete", "criterion": {}})
    monkeypatch.setattr(workflow, "run_validate_artifacts", lambda **kw: 0)

    code = workflow.run_canonical(allow_dirty=False)
    assert code == 0
    assert calls == [("summarize_run", "explicit-formula-grade-covariance-001")]
