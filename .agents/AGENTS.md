# Riemann Scope: AI Agent Workspace Operations

Canonical workspace operating manual for AI coding agents.

This manual enforces the rules established in root [AGENTS.md](file:///C:/Development/Projects/reimann_scope/AGENTS.md). All agents must strictly comply with the Root Rule:

> **An unresolved or failed mathematical check creates a research obligation. It does not authorize a success claim, a universal obstruction claim, or termination of the mission. Structural validation does not establish mathematical truth. Consequential conclusions must identify their exact evidence and scope and pass the applicable independent review. Missing evidence remains missing. Agents must continue deriving, computing, falsifying, or refining while meaningful authorized work and execution resources remain.**

## Mandatory Mathematical Claim Audit (`zeta-proof-audit`)

Before proposing or transitioning any theorem-level mathematical claim:
1. **Construct Machine-Readable Claim Specification**:
   Write `.agents/claims/<CLAIM_ID>.json` conforming to the schema and declaring exact quantifiers, scope, and evidence class.
2. **Validate via Executable Gate Audit**:
   ```bash
   python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --claim-file .agents/claims/<CLAIM_ID>.json
   ```
3. **Verify Repository Health and Regression Tests**:
   ```bash
   python scripts/workflow.py check-fast
   ```
4. **Independent Derivation Review**:
   Establish an independent review artifact in `.agents/claims/reviews/<CLAIM_ID>-derivation-review.md`. The review must record the exact proposition, input digests, adversarial challenges, attempted zero-crossings, resolution, and remaining obligations. Self-review or automated producer flags are strictly invalid.
5. **Grandfathered Legacy Policy (Policy B)**:
   Unmigrated legacy claims are hash-pinned to baseline commit `82643cafd605492233c6c1e992b78c2c30d45f13` in `.agents/corpus_map/legacy_claim_manifest.json`. Baseline migrations require explicit user authorization. Grandfathering never counts as independent verification.
