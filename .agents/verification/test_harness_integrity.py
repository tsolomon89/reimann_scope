"""
Antigravity Harness Configuration Integrity Tests
Validates all YAML frontmatter, rule trigger modes, skill schemas, subagent tools,
JSON configurations, and guarantees root Markdown preservation.
"""

import os
import json
from pathlib import Path
import pytest

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = WORKSPACE_ROOT / ".agents"

VALID_TOOLS = {
    "run_command", "view_file", "write_to_file", "replace_file_content",
    "multi_replace_file_content", "list_dir", "grep_search", "search_web",
    "read_url_content", "browser_subagent", "generate_image", "schedule",
    "manage_task", "ask_question", "call_mcp_tool", "read_resource", "list_resources"
}

def parse_yaml_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    frontmatter_str = parts[1]
    # Simple YAML key-value parser
    frontmatter = {}
    current_key = None
    for line in frontmatter_str.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line and not line.startswith("-"):
            key, val = line.split(":", 1)
            current_key = key.strip()
            val = val.strip()
            if val:
                frontmatter[current_key] = val
            else:
                frontmatter[current_key] = []
        elif line.startswith("-") and current_key:
            if isinstance(frontmatter[current_key], list):
                frontmatter[current_key].append(line[1:].strip())
    return frontmatter

def test_skills_frontmatter_and_structure():
    skills_dir = AGENTS_DIR / "skills"
    assert skills_dir.exists(), "Skills directory must exist"
    for skill_path in skills_dir.iterdir():
        if skill_path.is_dir():
            skill_md = skill_path / "SKILL.md"
            assert skill_md.exists(), f"SKILL.md missing in {skill_path.name}"
            fm = parse_yaml_frontmatter(skill_md)
            assert "name" in fm, f"Skill {skill_path.name} missing 'name' in frontmatter"
            assert "description" in fm, f"Skill {skill_path.name} missing 'description' in frontmatter"
            assert fm["name"] == skill_path.name, f"Skill name '{fm['name']}' != folder name '{skill_path.name}'"

def test_rules_frontmatter_and_triggers():
    rules_dir = AGENTS_DIR / "rules"
    assert rules_dir.exists(), "Rules directory must exist"
    for rule_file in rules_dir.glob("*.md"):
        fm = parse_yaml_frontmatter(rule_file)
        assert "trigger" in fm, f"Rule {rule_file.name} missing 'trigger'"
        assert fm["trigger"] in ["always_on", "model_decision", "manual", "glob"], f"Invalid trigger '{fm['trigger']}' in {rule_file.name}"
        assert "description" in fm, f"Rule {rule_file.name} missing 'description'"

def test_custom_subagents_tools_and_schema():
    agents_dir = AGENTS_DIR / "agents"
    assert agents_dir.exists(), "Agents directory must exist"
    for agent_file in agents_dir.glob("*.md"):
        fm = parse_yaml_frontmatter(agent_file)
        assert "name" in fm, f"Agent {agent_file.name} missing 'name'"
        assert "description" in fm, f"Agent {agent_file.name} missing 'description'"
        assert "tools" in fm, f"Agent {agent_file.name} missing 'tools'"
        tools = fm["tools"]
        assert isinstance(tools, list) and len(tools) > 0, f"Agent {agent_file.name} must list permitted tools"
        for tool in tools:
            assert tool in VALID_TOOLS, f"Agent {agent_file.name} has invalid/unknown tool '{tool}'"

def test_workflows_exist():
    workflows_dir = AGENTS_DIR / "workflows"
    assert workflows_dir.exists(), "Workflows directory must exist"
    workflow_files = list(workflows_dir.glob("*.md"))
    assert len(workflow_files) >= 3, "Expected at least 3 standard workflows"

def test_hooks_json_valid():
    hooks_file = AGENTS_DIR / "hooks.json"
    if hooks_file.exists():
        with open(hooks_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict), "hooks.json must be a JSON object"

def test_root_markdown_files_preserved():
    expected_root_files = [
        "README.md", "MATH_CONTRACT.md", "DECISIONS.md",
        "DATA_PROVENANCE.md", "RIEMANN_MICROSCOPE_SPEC.md",
        "EXPERIMENT_PROTOCOL.md", "TRANSCENDENTAL_CONTINUATION.md"
    ]
    for filename in expected_root_files:
        file_path = WORKSPACE_ROOT / filename
        assert file_path.exists(), f"Root file {filename} must not be deleted or moved"
        assert file_path.stat().st_size > 0, f"Root file {filename} must not be empty"
