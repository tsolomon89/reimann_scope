# Refresh Corpus Map Workflow

Use `/refresh-corpus-map` to inspect the root Markdown corpus, verify SHA-256 checksums, update document inventories, and check proof-obligation status.

## Ordered Execution Stages

1. **Scan Root Directory**:
   - Inspect all root `.md` files.
   - Compute line counts, byte sizes, and SHA-256 checksums.

2. **Update Inventory**:
   - Record updates in `.agents/corpus_map/inventory.md`.

3. **Validate Invariants**:
   - Verify that test vectors `VEC-A` through `VEC-F` remain synchronized with `MATH_CONTRACT.md`.
   - Update `.agents/corpus_map/obligation_register.md`.

4. **Integrity Test**:
   - Run the automated harness integrity test suite:
     `pytest .agents/verification/test_harness_integrity.py`
