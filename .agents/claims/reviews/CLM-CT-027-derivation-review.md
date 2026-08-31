# Derivation Review for Claim CLM-CT-027

**Claim ID**: `CLM-CT-027`
**Reviewer Role**: Agent A — Certified Enclosure & Independent Replay
**Status**: `FIXED_GAUSSIAN_COMMON_FRAME_CROSS_TERM_NONZERO`
**Date**: August 31, 2026 (Audit Repair Sprint)

> [!NOTE]
> **Historical Provenance Note**: This review supersedes the August 30, 2026 review. The claim classification is strictly determined by the outcome of two genuinely independent Arb ball arithmetic evaluations and a fully replayable certificate bundle (`CLM-CT-027-certificate.json`).

## Mathematical Derivation & Dual Enclosure Proof

1. **Completed Logarithmic Derivative**:
   The completed Riemann $\xi$-function $\xi(s) = \frac{1}{2} s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$ has logarithmic derivative $G(s) = -\xi'/\xi(s) = A(s) + P(s)$, where:
   $$A(s) = -\frac{1}{s} - \frac{1}{s-1} + \frac{1}{2}\log\pi - \frac{1}{2}\psi(s/2), \quad P(s) = -\frac{\zeta'}{\zeta}(s).$$

2. **Second Grade Variation Cross-Term & 4-Block Decomposition**:
   Along the line $s = 1/2 + a + it$ (with $z = a + it$), the second grade derivative is:
   $$\ddot G_0(t) = (\log\tau)^2 [z G'(s) + z^2 G''(s)] = \ddot A_0(t) + \ddot P_0(t).$$
   Under a real probability window $W(t)$, the real cross-term decomposes as:
   $$\mathfrak X_{\xi, W} = \Re\langle G_0, \ddot G_0\rangle_W = I_{PP} + I_{PA} + I_{AP} + I_{AA}.$$

3. **Dual Independent Evaluation Paths**:
   - **Path 1 (Direct Cauchy Contour on Completed $\xi$)**:
     Evaluates $G(s), G'(s), G''(s)$ via a 32-point circular Cauchy contour with radius $r = 0.3$ on `acb.zeta()` and polygamma functions in Arb.
     - Compact integral on $[-8, 8]$: $[0.0231722158 \pm 7.7 \times 10^{-47}]$
     - Quadrature remainder error: $\le \frac{16}{180}(0.04)^4(0.05) \le 1.14 \times 10^{-8}$ (derived from Simpson $M_4 \le 0.05$)
     - Real-line Gaussian tail ($|t| > 8$): $\le 2 \cdot \frac{1}{\sqrt{2\pi}} \int_8^\infty e^{-t^2/2} (38.4 t^2 + 6 t^3) dt \le 7.16 \times 10^{-12}$
     - Path 1 Total Enclosure: $[0.023172204, 0.023172227]$
     - Zero Excluded? **TRUE** ($0 \notin I_1$).
   - **Path 2 (Decomposed $A+P$ via Finite Dirichlet Series + $L^2(W)$ Tail Bound)**:
     Evaluates $A(s)$ via exact polygamma `acb.polygamma(0, 1, 2)` and $P(s)$ via finite Dirichlet sum $\sum_{n=2}^N \Lambda(n) n^{-s}$ ($N = 50000$), with the infinite Dirichlet tail independently enclosed via $L^2(W)$ Cauchy-Schwarz majorants $J_4(N, 4)$ and $J_6(N, 4)$.
     - Compact integral on $[-8, 8]$: $[0.02317242 \pm 1.5 \times 10^{-47}]$
     - Dirichlet tail bound: $\le \|G\|_W \|\ddot R_0\|_W \le 0.002265$
     - Path 2 Total Enclosure: $[0.0209073, 0.0254375]$
     - Zero Excluded? **TRUE** ($0 \notin I_2$).

4. **Interval Intersection & Classification**:
   $$I_1 \cap I_2 = [0.023172204, 0.023172227] \ne \emptyset, \quad 0 \notin I_1 \cap I_2.$$
   Because the verified interval is strictly positive and bounded away from zero, exact cross-term cancellation fails for this fixed Gaussian candidate instance.

**Assigned Classification**: `FIXED_GAUSSIAN_COMMON_FRAME_CROSS_TERM_NONZERO`.
