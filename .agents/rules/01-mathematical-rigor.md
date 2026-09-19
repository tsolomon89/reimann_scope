---
trigger: always_on
description: Non-negotiable mathematical rigor standards, distinction between proof and computation, evidence classes, error bounding, anti-circularity, and counterexample controls.
---

# Mathematical Rigor Protocol

When operating within this repository, the agent must adhere strictly to these mathematical standards:

1. **Distinguish Proof from Computation**:
   - Numerical agreement (at any precision) is empirical evidence or falsification, **NEVER** formal mathematical proof.
   - Do not announce or report a proof, disproof, or novel theorem regarding the Riemann Hypothesis or related open problems without formal, independent, deductive verification.
   - A single test point, sign check, or empirical observation on a discrete grid never establishes positive definiteness or universal non-vanishing across an open domain or infinite family.

2. **Evidence Classes and Scoped Conclusions**:
   Every claim, conclusion, and artifact must be classified under an explicit evidence class:
   - `PROPOSED`: Mathematically defined proposition; evaluation pending.
   - `EMPIRICAL`: High-precision or floating-point numerical sampling. Scoped strictly to the evaluated sample set.
   - `NUMERICALLY_UNRESOLVED`: Inconclusive numerical check or precision-dominated residual. Creates an active research obligation.
   - `CERTIFIED_FINITE`: Certified ball enclosure (Arb) over a declared finite compact domain or point witness with complete error budget.
   - `PROVED_CONDITIONAL`: Deductive proof or formal Lean theorem subject to an explicitly exposed unproved premise.
   - `REFUTED_WITHIN_SCOPE`: Definite falsification or counterexample established for a declared candidate class.
   - `AWAITING_INDEPENDENT_REVIEW`: Derivation or calculation completed, awaiting independent adversarial review.
   Never promote a claim to a stronger status unless its specific mathematical and review requirements are fulfilled. Missing evidence remains missing.

3. **Exact Symbolic Priority and Rigorous Error Budgets**:
   - Perform exact algebraic and symbolic verification (using SymPy, exact rational arithmetic, or Lean 4) before resorting to floating-point approximations.
   - For all numerical evaluations, explicitly declare working precision (decimal digits / bits), domain, truncation, and error bounds.
   - When claiming a certified numerical bound or certificate, compute rigorous interval enclosures (Arb) accounting for discretization, truncation, quadrature, and rounding errors.

4. **Anti-Circularity and Equivalence Screening**:
   - Screen all arguments for hidden circular dependencies on the Riemann Hypothesis or its known equivalences (Weil positivity, Li's criterion $\lambda_n \ge 0$, Mertens conjecture bounds, Nyman-Beurling criterion, zero-free region assumptions).
   - Do not assume that $\tau = 2\pi$ implies any non-trivial automorphism $\zeta(\tau^K s) = \zeta(s)$.

5. **Counterexample Controls & Subspace Geometry**:
   - Test candidate mechanisms and general assertions against standard counterexamples (e.g., Davenport-Heilbronn zeta function, Epstein zeta functions, and synthetic off-line zeros).
   - If a property fails when the Euler product is removed, explicitly identify the Euler product as an essential premise.
   - Do not confuse column norm differences $|\|F_K\| - \|F_0\||$ with functional differences $\|F_K - F_0\|$, nor singular value stability with subspace direction stability when singular values cluster.

6. **Precise Attribution and Premise Tracking**:
   - Explicitly list every premise, hypothesis, and external theorem invoked in a derivation.
   - Cite authoritative literature (Riemann 1859, Hardy 1914, Davenport-Heilbronn 1936, Edwards 1974, Titchmarsh 1986).
