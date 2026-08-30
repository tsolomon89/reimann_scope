# Mathematical Audit Review: CLM-CT-022 (Adversarial Falsification Facet)

- **Claim ID**: `CLM-CT-022`
- **Claim Title**: Diagonal Cross-Term Exact Cancelling Variances
- **Review Facet**: Adversarial Counterexample Search & Numerical Verification
- **Audit Session Provenance**:
  - *Session ID*: `8196eb63-c434-4dc2-8180-cfbeb4bf00be`
  - *Start SHA*: `3306315edaeb6934f57c28e97cf864bbe6cd92d0`
  - *Target Commit*: `79c1cb849925232d3080ffba0b26cfdf3a67732a`
  - *Inherited Context*: `math_core.py`, `.agents/claims/CLM-CT-022.json`
  - *Tools Used*: Python 3.10 / mpmath (50-dps arbitrary precision), Arb ball enclosures
  - *Cross-Facet Visibility*: Evaluated purely from adversarial falsification objective.

## 1. Adversarial Challenge to Universal Non-Vanishing

The previously published claim asserted that $\mathfrak X_\zeta \ne 0$ for all $a > 0$ and all $v \ge 0$.
We constructed an exact algebraic counterexample:
$$v_*(a) = a^2 - a\frac{S_1(a)}{S_2(a)}$$
For $a = 2.0$, $v_*^{(2000)}(2) \approx 1.907445586187996 > 0$ (truncated value) and $v_*^{(\infty)}(2) \approx 1.9074455869720555$ (asymptotic estimate, classified as `NUMERICAL_EVIDENCE`).
Evaluating the reported diagonal expression at $v = v_*(a)$ yields $\mathfrak X_\zeta(a, v_*(a)) = 0$ identically.
Evaluating at $v = v_*(a) \pm 0.1$ yields:
- $\mathfrak X_\zeta(a, v_*(a) - 0.1) > 0$
- $\mathfrak X_\zeta(a, v_*(a) + 0.1) < 0$
This proves strict zero-crossing and falsifies the universal non-vanishing assertion.

## 2. Dominance Argument Audit

The historical claim that $-a\log n$ dominates $(a^2 - v)(\log n)^2$ as $a \to \infty$ was audited and found false:
For fixed $n$ and fixed variance $v$, the quadratic $a^2$ term grows as $\mathcal O(a^2)$ while the linear $-a$ term grows as $\mathcal O(a)$. Thus $a^2$ strictly dominates as $a \to \infty$.

## 3. Truncation vs Infinite Enclosure Audit

The algebraic root formula $v_* = a^2 - a S_1/S_2$ is exact; truncated decimal values must not be presented as infinite exact certificates without rigorous tail enclosures. Power-logarithmic tail bounds with complete integration by parts satisfy:
$$\text{Tail}_{S_1}(N, a) \le \frac{N^{-2a}}{2a} \left[ (\log N)^3 + \frac{3(\log N)^2}{2a} + \frac{6\log N}{(2a)^2} + \frac{6}{(2a)^3} \right]$$
$$\text{Tail}_{S_2}(N, a) \le \frac{N^{-2a}}{2a} \left[ (\log N)^4 + \frac{4(\log N)^3}{2a} + \frac{12(\log N)^2}{(2a)^2} + \frac{24\log N}{(2a)^3} + \frac{24}{(2a)^4} \right]$$
for $N \ge \exp(4/(1+2a))$.
