# Independent Falsification Review: CLM-CT-022

- **Claim ID**: `CLM-CT-022`
- **Claim Title**: Diagonal Cross-Term Exact Cancelling Variances
- **Reviewer Role**: Independent Adversarial Falsification Workstream

## 1. Adversarial Challenge to Universal Non-Vanishing

The previously published claim asserted that $\mathfrak X_\zeta \ne 0$ for all $a > 0$ and all $v \ge 0$.
We constructed an exact algebraic counterexample:
$$v_*(a) = a^2 - a\frac{S_1(a)}{S_2(a)}$$
For $a = 2.0$, $v_*(a) \approx 1.9074455869720555 > 0$.
Evaluating the reported diagonal expression at $v = v_*(a)$ yields $\mathfrak X_\zeta(a, v_*(a)) = 0$ identically.
Evaluating at $v = v_*(a) \pm 0.1$ yields:
- $\mathfrak X_\zeta(a, v_*(a) - 0.1) > 0$
- $\mathfrak X_\zeta(a, v_*(a) + 0.1) < 0$
This proves strict zero-crossing and falsifies the universal non-vanishing assertion.

## 2. Dominance Argument Audit

The historical claim that $-a\log n$ dominates $(a^2 - v)(\log n)^2$ as $a \to \infty$ was audited and found false:
For fixed $n$ and fixed variance $v$, the quadratic $a^2$ term grows as $\mathcal O(a^2)$ while the linear $-a$ term grows as $\mathcal O(a)$. Thus $a^2$ strictly dominates as $a \to \infty$.

## 3. Truncation vs Infinite Enclosure Audit

The numerical value $v_*^{(2000)}(2) \approx 1.907445586187996$ is a truncated sum evaluation ($N = 2000$).
For the infinite sum ($N \to \infty$), $v_*^{(\infty)}(2) \approx 1.9074455869720555$.
The algebraic root formula $v_* = a^2 - a S_1/S_2$ is exact; truncated decimal values must not be presented as infinite exact certificates without rigorous tail enclosures. Power-logarithmic tail bounds are $\mathcal O(N^{-2a}(\log N)^3/a)$.
