# Riemann Scope: AI Agent Workspace Operations

Canonical workspace operating manual for AI coding agents.

## Mandatory Mathematical Claim Audit (`zeta-proof-audit`)

Before proposing or transitioning any theorem-level mathematical claim:
1. Construct a 19-field JSON specification in `.agents/claims/<CLAIM_ID>.json`.
2. Validate the specification through the 10 gates via `.agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py`.
3. Verify that `python scripts/workflow.py check-fast` passes all claim, experiment, and operational tests.
4. Establish independent workstream reviews in `.agents/claims/reviews/`.
5. Comply with Policy B: unmigrated legacy claims are hash-pinned to baseline commit `82643cafd605492233c6c1e992b78c2c30d45f13` in `.agents/corpus_map/legacy_claim_manifest.json`. Baseline migrations require explicit user authorization.
