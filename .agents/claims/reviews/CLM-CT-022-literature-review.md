# Mathematical Audit Review: CLM-CT-022 (Literature Facet)

- **Claim ID**: `CLM-CT-022`
- **Claim Title**: Diagonal Cross-Term Exact Cancelling Variances
- **Review Facet**: Primary Literature Concordance & Citation Verification
- **Audit Session Provenance**:
  - *Session ID*: `8196eb63-c434-4dc2-8180-cfbeb4bf00be`
  - *Start SHA*: `3306315edaeb6934f57c28e97cf864bbe6cd92d0`
  - *Target Commit*: `79c1cb849925232d3080ffba0b26cfdf3a67732a`
  - *Inherited Context*: External mathematical literature citations
  - *Tools Used*: Literature mapping and citation cross-checking
  - *Cross-Facet Visibility*: Verification of mathematical boundaries from authoritative literature.

## 1. Primary Source Audit

1. **Titchmarsh (1986)**, *The Theory of the Riemann Zeta-Function*, 2nd ed. (revised by D. R. Heath-Brown), Oxford University Press:
   - *Theorem 2.1 (Domain of Absolute Convergence)*, pp. 11–13: The Dirichlet series for $-\zeta'/\zeta(s) = \sum_{n\ge 2}\Lambda(n)n^{-s}$ converges absolutely only in the half-plane $\Re(s) > 1$ ($\Re(z) = a > 1/2$). Inside the critical strip $0 < \Re(s) < 1$, the naive Dirichlet series diverges and cannot be evaluated termwise without analytic continuation.
   - *Applicability*: The diagonal formula $\mathfrak X_{\zeta,\mathrm{diag}}$ is mathematically defined as a Dirichlet series only for $a > 1/2$. The cancellation domain $a > 1/\log 2 \approx 1.442695$ is strictly within the domain of absolute convergence.

2. **Montgomery & Vaughan (1974)**, *"Hilbert's inequality"*, *J. London Math. Soc.* (2) 8, 73–82:
   - *Theorem 2 (Mean Value Bound for Dirichlet Polynomials)*:
     Provides an upper bound on the off-diagonal error over finite intervals $[0, T]$. This bound limits the magnitude of off-diagonal interactions but does not prove a specific off-diagonal total is non-zero.

3. **Edwards (1974)**, *Riemann's Zeta Function*, Academic Press:
   - *Chapter 1 (Hadamard Product Formula)*, pp. 15–21:
     The unconditional Hadamard identity for non-trivial zeros is $\sum_\rho \frac{1}{\rho(1-\rho)} = 2 + \gamma - \log(4\pi)$, where zeros are paired as $\lim_{T\to\infty} \sum_{|\Im(\rho)| < T}$.
     *Critical Epistemic Distinction*: The replacement $\rho(1-\rho) = |\rho|^2$ holds if and only if $\Re(\rho) = 1/2$. Citing $\sum 1/|\rho|^2 = 2+\gamma-\log(4\pi)$ is conditional on the Riemann Hypothesis.
