---
trigger: always_on
description: Mandatory corpus integrity, notation preservation, tau-scale conventions, and contradiction tracking.
---

# Corpus Integrity and Notation Preservation

1. **Root Document Preservation**:
   - Do not move, rename, delete, reorganize, or rewrite root Markdown files (`README.md`, `MATH_CONTRACT.md`, `DECISIONS.md`, `DATA_PROVENANCE.md`, `RIEMANN_MICROSCOPE_SPEC.md`, `EXPERIMENT_PROTOCOL.md`, `TRANSCENDENTAL_CONTINUATION.md`).
   - Ordinary Markdown files are research data and specifications; only `.agents/` configuration controls agent behavior.

2. **Preserve Project Notation**:
   - Maintain the project's native notation: $\tau = 2\pi$, centered coordinate $z = s - 1/2 = \delta + it$, and kernel deformation variables $(A, B, C, D)$.
   - Do not normalize away $\tau$-native or centered formulations in favor of conventional notation. Provide conventional formulations side-by-side as a verification reference when needed.

3. **Explicit Transformation Distinctions**:
   - Never conflate camera zoom, height sampling $s_K(u)$, origin coordinate dilation $s'=\tau^K s$, centered coordinate dilation $s'=1/2+\tau^K(s-1/2)$, argument transform $f_K(s)=\zeta(\tau^K s)$, or kernel transforms $\mathcal{Z}_{A,C,B,D}(s)$.
   - Maintain the Active Mathematics card semantics for every active transformation.

4. **No Suppression of Contradictions or Failures**:
   - Never silently resolve or conceal contradictions between documents; log them in `.agents/corpus_map/contradiction_register.md`.
   - Never rewrite a failed approach (such as naive Dirichlet series summation inside the critical strip) as though it remains viable.
