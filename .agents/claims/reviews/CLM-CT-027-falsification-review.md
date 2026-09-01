# Falsification Review for Claim CLM-CT-027

**Claim ID**: `CLM-CT-027`
**Reviewer Role**: Agent B — Adversarial Falsification & Remainder Audit
**Status**: `FIXED_GAUSSIAN_COMMON_FRAME_CROSS_TERM_NONZERO`
**Date**: September 1, 2026 (Audit Repair & Exact Certification Sprint)

## Adversarial Audit & Remainder Verification

1. **Taylor Remainder Audit**:
   - Audited the degree $M=24$ Taylor expansion on subintervals of width $h = 0.04$ ($h/2 = 0.02$).
   - Cauchy disk radius $r = 0.05$ ensures holomorphy of $\xi(s)$ and $G(s)$ in the disk.
   - Proved majorant bound $M_k \le W_{\max}(t_m) \times 4.60 \times |\ddot G_0|$ guarantees Cauchy remainder enclosure $\le 8.04 \times 10^{-8}$.
   - Verified that the polynomial integral $+0.0231722$ dominates the total remainder $8.04 \times 10^{-8}$ by more than 5 orders of magnitude.

2. **Real-Line Tail Audit**:
   - Audited constants $c_2 = 15.0$ and $c_3 = 1.5$ from rational pole estimates, Binet digamma bounds, and absolute Dirichlet derivative sums.
   - Proved Gaussian moment integrals $\int_8^\infty t^2 e^{-t^2/2} dt \le 8.125 e^{-32}$ and $\int_8^\infty t^3 e^{-t^2/2} dt = 66 e^{-32}$.
   - Verified real-line tail error $\le 2.24 \times 10^{-12}$.

3. **Replay Validation**:
   - Replayed `scripts/verify_crossterm_certificate.py` and validated certificate `.agents/claims/certificates/CLM-CT-027-certificate.json`.
   - Verified $0 \notin [0.023172135, 0.023172297]$.

**Falsification Outcome**: Zero cancellation is strictly refuted for this fixed candidate instance.
