# Derivation Review for Claim CLM-CT-028

**Claim ID**: `CLM-CT-028`
**Reviewer Role**: Agent A — Operator Adjoint & Instance Closure
**Status**: `FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_CLOSED`
**Date**: September 1, 2026 (Audit Repair & Exact Certification Sprint)

> [!NOTE]
> **Historical Provenance Note**: This review supersedes earlier reviews. Because `CLM-CT-027` is now certified strictly positive ($\mathfrak X_{\xi, W} \in [0.023172135, 0.023172297] > 0$), the fixed canonical Gaussian common-frame candidate instance is rigorously closed (`FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_CLOSED`). Whole-class closure for arbitrary Schwartz windows remains open (`BILATERAL_GRADE_ROUTE_CLASS_CLOSURE_OPEN`).

## Mathematical Derivation & Weighted-Adjoint Operator

1. **First-Order Differential Generator**:
   Along the line $s = 1/2 + a + it$, $z = a + it$, the grade dilation vector field acting on $g(t) = G(1/2+a+it)$ is:
   $$L_a = (t - ia) \partial_t = b(t) \partial_t, \quad \text{where } b(t) = t - ia.$$
   Note that $g'(t) = i G'(s)$, so $L_a g(t) = (t - ia)(i G'(s)) = (a + it) G'(s) = z G'(s)$.

2. **Weighted Adjoint Operator in $L^2(W(t)dt)$**:
   For the weighted inner product $\langle f, g\rangle_W = \int_{\mathbb{R}} W(t) f(t) \overline{g(t)} dt$, integration by parts yields:
   $$L_{a,W}^* = -\overline{b(t)}\partial_t - q(t), \quad \text{where } q(t) = 1 + \frac{W'(t)}{W(t)}\overline{b(t)} = 1 + \frac{W'(t)}{W(t)}(t + ia).$$
   For the standard Gaussian window $W(t) = \frac{1}{\sqrt{2\pi}}e^{-t^2/2}$ with $\frac{W'(t)}{W(t)} = -t$:
   $$L_{a,W}^* = -(t + ia)\partial_t + t^2 + iat - 1.$$

3. **Second Variation Quadratic Expansion with $2a^2$ Term**:
   $$\|L_a g\|_W^2 = \int_{\mathbb R} W(t) |t - ia|^2 |g'(t)|^2 dt = \int_{\mathbb R} W(t) (t^2 + a^2) |g'(t)|^2 dt.$$
   $$\langle L_{a,W}^* g, L_a g\rangle_W = \int_{\mathbb R} W(t) [-\overline{b(t)} g'(t) - q(t) g(t)] \overline{b(t) g'(t)} dt.$$
   Taking the real part:
   $$\Re [ -\overline{b(t)}^2 |g'(t)|^2 ] = -(t^2 - a^2) |g'(t)|^2.$$
   Combining the norm and adjoint terms:
   $$\|L_a g\|_W^2 + \Re\langle L_{a,W}^* g, L_a g\rangle_W = 2a^2 \int_{\mathbb R} W(t) |g'(t)|^2 dt - \Re \int_{\mathbb R} W(t) (1 - t^2 - iat) g(t) \overline{(t - ia) g'(t)} dt.$$

4. **Instance Scope & Exact Closure**:
   - At the fixed instance $(a = 1.5, \sigma_W = 1.0)$, `CLM-CT-027` proves that $\mathfrak X_{\xi, W} \in [0.023172135, 0.023172297] > 0$ strictly.
   - Combined with strictly positive norm term $2 a^2 \int W |g'|^2 dt > 0$, the total second variation $\mathcal V_2 > 0$ strictly.
   - Therefore, arithmetic zero descent fails and this fixed candidate instance is closed: `FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_CLOSED`.
   - General non-canonical or untuned window families are not closed by this single instance witness; whole-class status remains `BILATERAL_GRADE_ROUTE_CLASS_CLOSURE_OPEN`.

**Assigned Classification**: `FIXED_GAUSSIAN_COMMON_FRAME_INSTANCE_CLOSED` (`NO_GO_FOR_DEFINED_CLASS`).
