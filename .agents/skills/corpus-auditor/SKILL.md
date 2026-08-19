---
name: corpus-auditor
description: Audits mathematical claims, identities, and proof obligations against the durable corpus map and contract registers. Use when checking claim status, dependencies, contradictions, or obligation completion.
---

# Corpus Auditor Skill

This skill provides procedures for auditing mathematical claims, checking claim status, mapping dependencies, and identifying contradictions against the project's durable corpus map.

## Audit Procedure

1. **Locate Corpus Map**:
   - Check [.agents/corpus_map/inventory.md](../../corpus_map/inventory.md) for source document coverage.
   - Check [.agents/corpus_map/claim_register.md](../../corpus_map/claim_register.md) for existing registered claims.
   - Check [.agents/corpus_map/contradiction_register.md](../../corpus_map/contradiction_register.md) for known ambiguities.
   - Check [.agents/corpus_map/obligation_register.md](../../corpus_map/obligation_register.md) for open proof obligations.

2. **Standard Claim Status Assignment**:
   When evaluating a new claim, assign exactly one of the standard status labels:
   - `Definition`, `Established external theorem`, `Algebraic identity`, `Derived lemma`, `Proposed lemma`, `Conjecture`, `Numerical observation`, `Heuristic`, `Open proof obligation`, `Circular or potentially circular`, `Contradicted`, `Falsified`, `Superseded`.

3. **Check Contract Invariants**:
   - Verify if the claim impacts any of the 6 test vectors (`VEC-A` through `VEC-F`).
   - If an identity modifies coordinate transformations, verify it against `MATH_CONTRACT.md`.

For detailed reference on claim taxonomies and dependency tracing, see [references/corpus_map_guide.md](./references/corpus_map_guide.md).
