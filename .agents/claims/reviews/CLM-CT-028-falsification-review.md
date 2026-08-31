# Falsification Review for Claim CLM-CT-028

**Claim ID**: `CLM-CT-028`
**Reviewer Role**: Agent B — Adversarial Falsification & Scope Audit
**Status**: `FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_CLOSED`
**Date**: August 31, 2026 (Audit Repair Sprint)

## Adversarial Audit & Scope Verification

1. **Scope Distinction Audit**:
   - The claim specifically closes the fixed canonical Gaussian common-frame candidate instance at $(a=1.5, \sigma_W=1.0)$, for which $\mathfrak X_{\xi, W} > 0$ and $\mathcal V_2 > 0$ are certified strictly positive.
   - The claim does NOT assert closure of the entire mathematical category of all conceivable non-canonical or untuned window families. Whole-class closure remains open (`BILATERAL_GRADE_ROUTE_CLASS_CLOSURE_OPEN`).

2. **Weighted Adjoint Operator Verification with $2a^2$ Term**:
   - Audited the weighted adjoint operator identity for $L_a = (t-ia)\partial_t$ with weight $W(t)$:
     $$L_{a,W}^* = -\overline{b(t)}\partial_t - \left( 1 + \frac{W'(t)}{W(t)}\overline{b(t)} \right) = -(t+ia)\partial_t + t^2 + iat - 1.$$
   - Evaluated the second variation expansion:
     $$\|L_a g\|_W^2 + \Re\langle L_{a,W}^* g, L_a g\rangle_W = 2a^2 \int_{\mathbb R} W(t) |g'(t)|^2 dt - \Re \int_{\mathbb R} W(t) (1 - t^2 - iat) g(t) \overline{(t - ia) g'(t)} dt.$$
   - Both the norm term $2a^2 \int W |g'|^2 dt \approx 0.04658 > 0$ and the cross-term $\mathfrak X_{\xi, W} \approx 0.02317 > 0$ are strictly positive.
   - Verified that the coupling integral does not cancel the positive norm term.

3. **Equality-Case Analysis**:
   - For $\mathcal V_2 = 0$, $L_a g$ would have to satisfy an exact cancellation condition with $L_{a,W}^*$, which fails for the non-trivial meromorphic function $G = -\xi'/\xi$.

**Falsification Outcome**: The closure of the fixed candidate instance is sound and correctly bounded in scope.
