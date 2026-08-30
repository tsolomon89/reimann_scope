# Derivation Review for Claim CLM-CT-028

**Claim ID**: `CLM-CT-028`  
**Reviewer Role**: Agent A — Derivation  
**Date**: August 30, 2026  

## Mathematical Derivation & Branch Elimination

1. **Branch 1 (Static Common-Frame)**:
   - Object: $\mathfrak X_{\xi, W} = \Re\langle G_0, \ddot G_0\rangle_W$ with $G = -\xi'/\xi$.
   - Result: As derived in `CLM-CT-027`, for canonical Gaussian windows $W(t) = \frac{1}{\sqrt{2\pi}\sigma_W}e^{-t^2/(2\sigma_W^2)}$, $\mathfrak X_{\xi, W} > 0$ strictly across all tested parameter points ($+0.023932 > 0$ at $a=1.5, \sigma_W=1.0$).
   - Gate Failure: `FAIL_COMPLETED_XI_CROSS_TERM_CANCELLATION`.

2. **Branch 2 (Fully Grade-Covariant Pullback)**:
   - Object: $\mathcal{C}_{h, T} = \mathcal{M}_{0, \tau^h T} + \mathcal{M}_{0, \tau^{-h} T} - 2\mathcal{M}_{0, T}$.
   - Result: Under change of variables $t \mapsto \tau^{\pm h} t$, the variation is removed. As $T \to \infty$, $\lim_{T\to\infty} \mathcal{C}_{h, T} = 0$.
   - Gate Failure: `FAIL_GRADE_COORDINATE_REDUNDANCY`.

3. **Branch 3 (Window Tuning)**:
   - Object: Solving $v_*(a)$ such that $\mathfrak X_{\text{diag}}(a, v_*(a)) = 0$.
   - Result: Cancelling variances $v_*(a)$ depend on the background Dirichlet/Gamma moments, not independently forced by arithmetic or Euler product support.
   - Gate Failure: `FAIL_POSTHOC_WINDOW_TUNING`.

4. **Branch 4 (Scale Specificity)**:
   - Object: Dilation centering $z_k = q^k z$ with base $q > 1$.
   - Result: Curvature $B_{\rho, q}''(0) = 2\delta^2(\log q)^2 > 0$ holds for arbitrary $q > 1$ without specifically selecting $\tau = 2\pi$.
   - Gate Failure: `SCALE_GENERIC_NOT_TAU_SPECIFIC`.

**Conclusion**: All 4 canonical bilateral grade branches are eliminated. The entire bilateral grade route is closed (`BILATERAL_GRADE_ROUTE_CLOSED`).
