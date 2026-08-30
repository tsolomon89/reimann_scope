# Mathematical Audit Review: CLM-CT-025 (Literature Facet)

- **Claim ID**: `CLM-CT-025`
- **Claim Title**: Finite Dirichlet Polynomial Inner Product Double-Sum Decomposition
- **Review Facet**: Primary Literature Concordance & Citation Verification
- **Audit Session Provenance**:
  - *Session ID*: `8196eb63-c434-4dc2-8180-cfbeb4bf00be`
  - *Start SHA*: `3306315edaeb6934f57c28e97cf864bbe6cd92d0`
  - *Target Commit*: `79c1cb849925232d3080ffba0b26cfdf3a67732a`
  - *Inherited Context*: External mathematical literature
  - *Tools Used*: Literature mapping and citation cross-checking
  - *Cross-Facet Visibility*: Theoretical bounds on Dirichlet polynomial mean values.

## 1. Primary Source Audit

1. **Montgomery & Vaughan (1974)**, *"Hilbert's inequality"*, *J. London Math. Soc.* (2) 8, 73–82:
   - *Theorem 2 (Mean Value Bound for Dirichlet Polynomials)*:
     For well-spaced exponents with gap $\delta_r = \min_{s\ne r} |\lambda_r - \lambda_s|$:
     $$\int_0^T \left| \sum_{r=1}^R a_r e^{i\lambda_r t} \right|^2 dt = \sum_{r=1}^R |a_r|^2 (T + \frac{3\pi}{2}\theta \delta_r^{-1})$$
     with $|\theta| \le 1$.
   - *Epistemic Precision*: This theorem supplies an upper bound $\mathcal O(\sum n |a_n|^2)$ on off-diagonal interference over $[0, T]$. It does not prove that a specific off-diagonal sum is non-zero. Strict non-vanishing requires a certified witness (e.g. the $N=3$ numerical witness in `CLM-CT-025-falsification-review.md`).

2. **Besicovitch (1932)**, *Almost Periodic Functions*, Cambridge University Press:
   - *Chapter I, Section 5 (Parseval Theorem in $B^2$ Space)*, pp. 24–31:
     For almost periodic functions $f(t) \sim \sum A_n e^{i\lambda_n t}$, the mean value is:
     $$\mathcal M\{f\} = \lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T f(t) dt$$
     with orthogonal relation $\mathcal M\{e^{i(\lambda_m - \lambda_n)t}\} = \delta_{m,n}$.
   - *Critical Distinction*: The Besicovitch mean operates strictly in the limit $T \to \infty$. A finite-window variance $\langle t^2 \rangle_W = \int t^2 W(t) dt < \infty$ does not commute with or survive the infinite Cesàro mean, because $\lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T t^2 dt = \infty$.
