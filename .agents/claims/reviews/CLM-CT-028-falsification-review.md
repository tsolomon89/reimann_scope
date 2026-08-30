# Falsification Review for Claim CLM-CT-028

**Claim ID**: `CLM-CT-028`  
**Reviewer Role**: Agent B — Falsification  
**Date**: August 30, 2026  

## Adversarial Stress Testing of Branch Elimination

1. **Attempted Survival of Branch 1**:
   Tested whether off-diagonal terms or rational pole terms could create cancellation: verified numerically and via Arb ball certification that $\mathfrak X_{\xi, W} > 0$ strictly, preventing cancellation under canonical windows.

2. **Attempted Survival of Branch 2**:
   Tested whether finite-$T$ boundary terms could prevent asymptotic vanishing: proved in Lean 4 (`finite_grade_pullback_second_difference_identity`) that $\mathcal{C}_{h, T}$ is a difference of scale evaluations that collapses to 0 as $T \to \infty$ whenever $\lim M_0(T)$ exists.

3. **Attempted Survival of Branch 3**:
   Tested whether arithmetic uniquely determines a window: the Euler product and prime support do not fix $v_*(a)$ without measuring the background moments, which is diagnostic rather than an independent bridge.

4. **Attempted Survival of Branch 4**:
   Tested whether Fourier normalization or gamma reflection could select $\tau = 2\pi$: the algebraic dilation curvature $2\delta^2(\log q)^2$ is strictly positive for every $q > 1$, confirming scale genericity.

**Conclusion**: No loophole or viable candidate survived the adversarial audit. The closure classification `BILATERAL_GRADE_ROUTE_CLOSED` is definitive.
