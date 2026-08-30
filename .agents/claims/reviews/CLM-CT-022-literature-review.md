# Independent Literature Review: CLM-CT-022

- **Claim ID**: `CLM-CT-022`
- **Claim Title**: Diagonal Cross-Term Exact Cancelling Variances
- **Reviewer Role**: Independent Literature Workstream

## 1. Primary Source Audit

1. **Titchmarsh (1986)**, *The Theory of the Riemann Zeta-Function*, 2nd ed. (revised by D. R. Heath-Brown), Oxford University Press:
   - *Theorem 2.1 (Domain of Absolute Convergence)*, pp. 11–13: The Dirichlet series for $-\zeta'/\zeta(s) = \sum_{n\ge 2}\Lambda(n)n^{-s}$ converges absolutely only in the half-plane $\Re(s) > 1$ ($\Re(z) = a > 1/2$). Inside the critical strip $0 < \Re(s) < 1$, the naive Dirichlet series diverges and cannot be evaluated termwise without analytic continuation.
   - *Applicability*: The diagonal formula $\mathfrak X_{\zeta,\mathrm{diag}}$ is mathematically defined as a Dirichlet series only for $a > 1/2$. The cancellation domain $a > 1/\log 2 \approx 1.442695$ is strictly within the domain of absolute convergence.

2. **Montgomery & Vaughan (1974)**, *"Hilbert's inequality"*, *J. London Math. Soc.* (2) 8, 73–82:
   - *Theorem 1 & 2 (Mean Value Estimates for Dirichlet Polynomials)*:
     Shows that for any finite Dirichlet polynomial $\sum_{n\le N} a_n n^{-it}$, the mean square over $[0, T]$ contains the diagonal term $T \sum |a_n|^2$ and bounded off-diagonal terms $\mathcal O(\sum n |a_n|^2)$.
   - *Applicability*: Confirms that finite-interval integration does not automatically eliminate off-diagonal terms.

3. **Edwards (1974)**, *Riemann's Zeta Function*, Academic Press:
   - *Chapter 1 (Hadamard Product Formula)*, pp. 15–21:
     The unconditional Hadamard identity for non-trivial zeros is $\sum_\rho \frac{1}{\rho(1-\rho)} = 2 + \gamma - \log(4\pi)$, where zeros are paired as $\lim_{T\to\infty} \sum_{|\Im(\rho)| < T}$.
     *Critical Epistemic Distinction*: The replacement $\rho(1-\rho) = |\rho|^2$ holds if and only if $\Re(\rho) = 1/2$. Citing $\sum 1/|\rho|^2 = 2+\gamma-\log(4\pi)$ is conditional on the Riemann Hypothesis.
