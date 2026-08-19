---
trigger: always_on
description: Non-negotiable mathematical rigor standards, distinction between proof and computation, error bounding, anti-circularity, and counterexample controls.
---

# Mathematical Rigor Protocol

When operating within this repository, the agent must adhere strictly to these mathematical standards:

1. **Distinguish Proof from Computation**:
   - Numerical agreement (at any precision) is empirical evidence or falsification, **NEVER** formal mathematical proof.
   - Do not announce or report a proof, disproof, or novel theorem regarding the Riemann Hypothesis or related open problems without formal, independent, deductive verification.

2. **Exact Symbolic Priority**:
   - Perform exact algebraic and symbolic verification (using SymPy or exact rational arithmetic) before resorting to floating-point approximations.
   - For all numerical evaluations, explicitly declare working precision (decimal digits / bits), domain, truncation, and error bounds (e.g. Arb ball enclosures).

3. **Anti-Circularity and Equivalence Screening**:
   - Screen all arguments for hidden circular dependencies on the Riemann Hypothesis or its known equivalences (Weil positivity, Li's criterion $\lambda_n \ge 0$, Mertens conjecture bounds, Nyman-Beurling criterion, zero-free region assumptions).
   - Do not assume that $\tau = 2\pi$ implies any non-trivial automorphism $\zeta(\tau^K s) = \zeta(s)$.

4. **Counterexample Controls**:
   - Test candidate mechanisms and general assertions against standard counterexamples (e.g., Davenport-Heilbronn zeta function, Epstein zeta functions, and synthetic off-line zeros).
   - If a property fails when the Euler product is removed, explicitly identify the Euler product as an essential premise.

5. **Precise Attribution and Premise Tracking**:
   - Explicitly list every premise, hypothesis, and external theorem invoked in a derivation.
   - Cite authoritative literature (Riemann 1859, Hardy 1914, Davenport-Heilbronn 1936, Edwards 1974, Titchmarsh 1986).
