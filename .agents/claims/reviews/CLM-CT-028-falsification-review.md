# Falsification Review for Claim CLM-CT-028

**Claim ID**: `CLM-CT-028`
**Reviewer Role**: Agent B — Candidate Class & Falsification Audit
**Status**: `FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_CLOSED`
**Date**: September 1, 2026 (Audit Repair & Exact Certification Sprint)

## Candidate Class & Instance Falsification Audit

1. **Adjoint Identity Audit**:
   - Audited the weighted-adjoint derivation $L_{a,W}^* = -(t+ia)\partial_t + t^2 + iat - 1$.
   - Verified that the term $2a^2 \int W |g'|^2 dt > 0$ is strictly positive for any non-constant holomorphic $g$.
   - Confirmed that operator identity alone does not prove non-vanishing of the coupling integral; coupling positivity is certified by `CLM-CT-027`.

2. **Defined Candidate Class Audit**:
   - The candidate class comprises bilateral grade dilation variations on completed $\xi$ under fixed windows.
   - For the canonical Gaussian instance $(a=1.5, \sigma_W=1.0)$, certified $\mathfrak X_{\xi, W} > 0$ and $\mathcal V_2 > 0$ strictly refute arithmetic zero descent.

3. **Whole-Class Scope Limitation**:
   - The closure applies strictly to the fixed canonical instance.
   - Arbitrary Schwartz or tuned windows remain classified as `BILATERAL_GRADE_ROUTE_CLASS_CLOSURE_OPEN`.

**Falsification Outcome**: Candidate instance closed (`FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_CLOSED`).
