# Falsification Review for Claim CLM-CT-027

**Claim ID**: `CLM-CT-027`
**Reviewer Role**: Agent B — Adversarial Falsification & Replay Audit
**Status**: `FIXED_GAUSSIAN_COMMON_FRAME_CROSS_TERM_NONZERO`
**Date**: August 31, 2026 (Audit Repair Sprint)

## Adversarial Audit & Independent Certificate Replay

1. **Certificate Replay Audit**:
   Executed standalone replay script:
   ```bash
   python scripts/verify_crossterm_certificate.py
   ```
   - Path 1 (Direct Cauchy contour on completed $\xi$): Enclosure $[0.023172204, 0.023172227]$, $0 \notin I_1$.
     - Quadrature error derived from Simpson $M_4 \le 0.05$: $\le 1.14 \times 10^{-8}$.
     - Real-line tail derived from envelope $38.4 t^2 + 6 t^3$: $\le 7.16 \times 10^{-12}$.
   - Path 2 (Decomposed $A+P$ via finite Dirichlet sum $N=50000$ with $L^2(W)$ tail bound): Enclosure $[0.0209073, 0.0254375]$, $0 \notin I_2$.
     - Dirichlet tail independently bounded via $L^2(W)$ majorants $J_4(N, 4)$ and $J_6(N, 4)$: $\le 0.002265$.
   - Intersection: $[0.023172204, 0.023172227] \ne \emptyset$.
   - Certificate verified at `.agents/claims/certificates/CLM-CT-027-certificate.json`.

2. **Block Cancellation & Root Absence Audit**:
   - Evaluated 4-block values: $I_{PP} \approx +3.2646$, $I_{PA} \approx -3.2857$, $I_{AP} \approx -3.4233$, $I_{AA} \approx +3.4676$.
   - The Archimedean components $I_{AA} + I_{PA} + I_{AP}$ do not cancel the prime component $I_{PP}$ to zero.
   - The net sum $I_{\text{total}} \approx +0.02317 > 0$ is strictly positive.
   - Verified that no real root of the cross-term integrand or integral exists at $(a = 1.5, \sigma_W = 1.0)$.

3. **Gaussian Tail Enclosure Audit**:
   - The compact quadrature is evaluated on $[-8.0, 8.0]$.
   - For $|t| > 8$, $\frac{1}{\sqrt{2\pi}} \int_{8}^\infty e^{-t^2/2} (38.4 t^2 + 6 t^3) dt \le 7.16 \times 10^{-12}$.
   - The tail error is accounted for in the certified ball enclosure.

**Falsification Outcome**: Zero is strictly excluded from $\mathfrak X_{\xi, W}$ for this fixed instance. Exact cancellation is falsified.
