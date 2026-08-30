# Falsification Review for Claim CLM-CT-026

**Claim ID**: `CLM-CT-026`  
**Reviewer Role**: Agent B — Falsification  
**Date**: August 30, 2026  

## Adversarial Stress Testing & Boundary Analysis

1. **Boundary at $a \to 1/2^+$**:
   As $a \to 1/2^+$, $\sigma \to 1^+$. The tail integral bound $\int_N^\infty (\log x) x^{-\sigma} dx \sim \frac{N^{1-\sigma}\log N}{\sigma-1} + \frac{N^{1-\sigma}}{(\sigma-1)^2}$ diverges as $\sigma \to 1^+$.
   However, for any fixed $a > 1/2$, $\sigma - 1 = a - 1/2 > 0$ is fixed and positive, guaranteeing rapid polynomial decay $O(N^{1/2-a}\log^3 N)$. The claim is strictly scoped to $a > 1/2$, so the boundary divergence at $a=1/2$ is correctly excluded.

2. **Window Integrability Check**:
   If $W$ had heavy tails (e.g. Cauchy distribution $W(t) \sim 1/t^2$), $\mu_2 = \int t^2 W(t) dt$ would diverge, causing failure of the interchange for $j=2$.
   The claim explicitly restricts $W \in \mathcal{S}(\mathbb{R})$ or $C_c^\infty(\mathbb{R})$, where all polynomial moments $\mu_k$ are finite.

3. **Numerical Quadrature vs Double Sum Truncation**:
   Tested in `math_core.py` at $a = 1.5, \sigma_W = 1.0$:
   - Truncation $N = 30$: double sum $= 2.65213324498402...$
   - Tail bound $= 14.1166...$
   - Continuous quadrature matches within the certified tail bound.
   - For $N = 100$, partial sum converges to $3.155411...$, within $< 0.1$ of the continuous limit.

4. **Conflation Audit**:
   Confirmed that the claim explicitly designates $F_0$ as the prime-side Dirichlet series $P(s)$, not the completed $\xi(s)$ function (satisfying Gate 1).

**Conclusion**: No counterexamples or invalid steps found within the stated hypotheses. Passed all falsification checks.
