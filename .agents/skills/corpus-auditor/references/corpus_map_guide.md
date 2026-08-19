# Corpus Map Reference & Audit Guide

## Purpose
This guide defines how to trace mathematical dependencies and verify claim provenance across the research corpus.

## Document Hierarchy
1. `RIEMANN_MICROSCOPE_SPEC.md` (`SPEC.md`): Top authority on functional, mathematical, and UI behavior.
2. `MATH_CONTRACT.md`: Implementation-level authority for exact formulas, transforms, invariants, and test vectors.
3. `DATA_PROVENANCE.md`: Authority on external datasets, checksums, and validation boundaries.
4. `DECISIONS.md`: Append-only record of accepted or superseded architectural and mathematical choices.

## Verification Checklist for Proposed Mathematical Modifications
- [ ] Does the change alter any defined coordinate mapping ($s, z, \delta, \gamma, \tau$)?
- [ ] Does the change conflate coordinate dilation ($s'=\tau^K s$) with argument scaling ($f(s)=\zeta(\tau^K s)$)?
- [ ] Does the change preserve Inverse Scale Lock ($AB=1$) in the Kernel Lab?
- [ ] Does the change preserve the exact centrifuge growth formula $\log |q_\rho^K| = K\delta\log\tau$?
- [ ] Has the claim been registered in `.agents/corpus_map/claim_register.md` with appropriate status?
