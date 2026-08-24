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
    monkeypatch.setattr(research_runner, "run_experiment", lambda sf: "centrifuge-slope-verification")
    monkeypatch.setattr(research_runner, "summarize_run", lambda r_id: {"status": "complete", "criterion": {"criterion_met": True, "observed": "0.0"}})
    monkeypatch.setattr(workflow, "run_validate_artifacts", lambda **kw: 0)
    code_allowed = workflow.run_canonical(allow_dirty=True, experiments=["centrifuge-slope-verification"])
    assert code_allowed == 0
