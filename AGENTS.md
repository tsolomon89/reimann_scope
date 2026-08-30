# Riemann Scope: AI Agent Operations & Mathematical Claim Protocol

This file serves as the canonical operating manual and entrypoint for AI coding agents operating in `reimann_scope`.

## 1. Mandatory Pre-Acceptance Claim Audit System (`zeta-proof-audit`)

Every mathematical claim, theorem proposal, or status classification (`PROVED`, `CLOSED`, `FALSIFIED`, `NO_GO_COMPONENT`) **MUST** satisfy the 10 mandatory pre-acceptance gates defined in `.agents/skills/zeta-proof-audit/SKILL.md` before registration.

### Required Steps:
1. **Create Machine-Readable Claim Specification**:
   Write `.agents/claims/<CLAIM_ID>.json` conforming to the 19-field schema.
2. **Execute Automated Gate Validation**:
   ```bash
   python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --claim-file .agents/claims/<CLAIM_ID>.json
   ```
3. **Execute Register Cross-Checking**:
   ```bash
   python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --cross-check-register --repo-root .
   ```
4. **Enforce Dual Status Distinctions**:
   - `SPECIFICATION_SCHEMA_PASSED`: Automated structural validation of fields, types, and domains.
   - `INDEPENDENT_MATHEMATICAL_AUDIT_PASSED`: Fully verified mathematical proof, formal Lean verification, adversarial falsification review, and literature review.
5. **Grandfathered Legacy Manifest & Exceptional Baseline Migrations**:
   - Legacy unmigrated claims are anchored to the immutable git baseline commit (`82643cafd605492233c6c1e992b78c2c30d45f13`) in `.agents/corpus_map/legacy_claim_manifest.json`.
   - Any modification to a legacy claim or new claim proposal strictly requires a validated `.agents/claims/<CLAIM_ID>.json` specification.
   - Modifying `baseline_commit` or regenerating the legacy manifest is an **exceptional migration requiring explicit user authorization**. Agents must never advance the baseline commit autonomously.

## 2. Core Operational Rules

1. **Mathematical Rigor Protocol (`01-mathematical-rigor.md`)**:
   - High-precision numerical agreement is empirical evidence or falsification, **NEVER** formal mathematical proof.
   - Exact symbolic algebra (SymPy / Lean 4) has priority over floating-point approximations.
   - Screen all arguments for circular dependencies on the Riemann Hypothesis or its known equivalences.
2. **Corpus Integrity (`02-corpus-integrity.md`)**:
   - Preserve root specification documents (`MATH_CONTRACT.md`, `DECISIONS.md`, `DATA_PROVENANCE.md`, etc.).
   - Preserve native project notation ($\tau = 2\pi$, centered coordinate $z = s - 1/2 = a + it$).
3. **Research Protocol (`03-research-protocol.md`)**:
   - Distinct research modes: Setup/Ingestion, Exact Audit, Numerical/Falsification, and Assertion.
   - Baseline zero discovery independence from validation datasets.

## 3. Verification Workflow

Always verify repository health using the standard command tiers:
- **Fast Tier**: `python scripts/workflow.py check-fast`
- **Artifact Validation**: `python scripts/workflow.py validate-artifacts --current`
- **Formal Verification**: `lake build` (in `formal/`) and `python scripts/build_formal.py`
- **Canonical Plan Audit**: `python scripts/workflow.py plan-canonical`
