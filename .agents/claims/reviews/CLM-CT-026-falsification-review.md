# Falsification Review for Claim CLM-CT-026

**Claim ID**: `CLM-CT-026`
**Reviewer Role**: Agent B — Adversarial Falsification
**Status**: `EXTERNAL_ANALYTIC_PROOF`
**Date**: August 31, 2026 (Audit Repair Sprint)

## Adversarial Audit & Stress Testing

1. **Boundary Singularities ($a \to 1/2^+$)**:
   As $a \to 1/2^+$, $\sigma = 1/2+a \to 1^+$. The tail integrals $J_k(N, \sigma)$ scale as $\frac{N^{1-\sigma}}{(\sigma-1)^{k+1}}$.
   Stress testing verified that for any fixed $a > 1/2$, the tail integral decays polynomially in $N$, and the double sum converges absolutely.

2. **Integration-by-Parts Tail Formula Audit**:
   Audited the tail formulas for $J_0, J_1, J_2, J_3$. Confirmed that all positive integration-by-parts terms are included:
   $$J_1(N, \sigma) = \frac{N^{1-\sigma}}{\sigma-1}\log N + \frac{N^{1-\sigma}}{(\sigma-1)^2},$$
   $$J_2(N, \sigma) = \frac{N^{1-\sigma}}{\sigma-1}\log^2 N + \frac{2N^{1-\sigma}}{(\sigma-1)^2}\log N + \frac{2N^{1-\sigma}}{(\sigma-1)^3},$$
   $$J_3(N, \sigma) = \frac{N^{1-\sigma}}{\sigma-1}\log^3 N + \frac{3N^{1-\sigma}}{(\sigma-1)^2}\log^2 N + \frac{6N^{1-\sigma}}{(\sigma-1)^3}\log N + \frac{6N^{1-\sigma}}{(\sigma-1)^4}.$$
   No positive terms are omitted.

3. **Window Width Extremes**:
   Tested Gaussian window widths $\sigma_W \in \{0.1, 1.0, 10.0\}$. Verified that moments $\mu_0, \mu_1, \mu_2$ remain finite and that the double series-integral converges absolutely across all configurations.

**Falsification Outcome**: No counterexample or structural violation detected. The external analytic proof is sound.
