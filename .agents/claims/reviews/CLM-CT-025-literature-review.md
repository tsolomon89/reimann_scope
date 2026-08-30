# Independent Literature Review: CLM-CT-025

- **Claim ID**: `CLM-CT-025`
- **Claim Title**: Finite Dirichlet Polynomial Inner Product Double-Sum Decomposition
- **Reviewer Role**: Independent Literature Workstream

## 1. Primary Source Audit

1. **Montgomery & Vaughan (1974)**, *"Hilbert's inequality"*, *J. London Math. Soc.* (2) 8, 73–82:
   - *Theorem 2*: If $\lambda_1 < \lambda_2 < \dots < \lambda_R$ and $\delta_r = \min_{s\ne r} |\lambda_r - \lambda_s|$, then:
     $$\int_0^T \left| \sum_{r=1}^R a_r e^{i\lambda_r t} \right|^2 dt = \sum_{r=1}^R |a_r|^2 (T + \frac{3\pi}{2}\theta \delta_r^{-1})$$
     with $|\theta| \le 1$.
   - *Direct Application to Riemann Scope*: For Dirichlet polynomials with $\lambda_n = -\log n$, the gap $\delta_n = \log(1 + 1/n) \sim 1/n$, so $\delta_n^{-1} \sim n$. This proves that over finite intervals, off-diagonal interaction terms scale as $\mathcal O(\sum n |a_n|^2)$ and do not vanish identically for finite $T$.

2. **Besicovitch (1932)**, *Almost Periodic Functions*, Cambridge University Press:
   - *Chapter I, Section 5 (Parseval Theorem in $B^2$ Space)*, pp. 24–31:
     For almost periodic functions $f(t) \sim \sum A_n e^{i\lambda_n t}$, the mean value is:
     $$\mathcal M\{f\} = \lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T f(t) dt$$
     with orthogonal relation $\mathcal M\{e^{i(\lambda_m - \lambda_n)t}\} = \delta_{m,n}$.
   - *Critical Distinction*: The Besicovitch mean operates strictly in the limit $T \to \infty$. A finite-window variance $\langle t^2 \rangle_W = \int t^2 W(t) dt < \infty$ does not commute with or survive the infinite Cesàro mean, because $\lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T t^2 dt = \infty$.
