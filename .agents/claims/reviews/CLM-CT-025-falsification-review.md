# Independent Falsification Review: CLM-CT-025

- **Claim ID**: `CLM-CT-025`
- **Claim Title**: Finite Dirichlet Polynomial Inner Product Double-Sum Decomposition
- **Reviewer Role**: Independent Adversarial Falsification Workstream

## 1. Falsification of "Finite-Window Diagonalization"

A prospective assertion might claim that setting the window variance $\langle t^2 \rangle_W = v$ diagonalizes a finite-window Dirichlet inner product:
$$\langle F_0, \ddot F_0 \rangle_W \stackrel{?}{=} \mathfrak X_{\mathrm{diag}}(a, v)$$

We tested this hypothesis against certified numerical quadrature on finite Dirichlet polynomials with $N \in \{2, 3, 5, 15\}$ under:
1. Schwartz Gaussian: $W(t) = \frac{1}{\sqrt{2\pi}\sigma_W}\exp(-t^2/(2\sigma_W^2))$,
2. Smooth Compact Bump: $W(t) = C_M \exp(-1/(1-(t/M)^2))\mathbf 1_{|t| < M}$.

### Falsification Result:
For all tested finite configurations, the off-diagonal discrepancy:
$$\mathfrak X_{\mathrm{offdiag}} = (\log\tau)^2 \Re \sum_{m\ne n} c_m \overline{c_n} \mathcal I_{m,n}(W) \ne 0$$
is strictly non-zero (e.g. $|\mathfrak X_{\mathrm{offdiag}}| > 10^{-4}$ for $a = 1.5, \sigma_W = 1.0$).
This falsifies the assertion that finite-window variance diagonalizes the inner product.

## 2. Window Non-Vanishing Clarification

We reject the stronger unproved claim that $\widehat W(\log(m/n)) \ne 0$ for all possible finite windows and all $m\ne n$.
- **Corrected Mathematical Invariant**:
  $$\boxed{\text{Finite windows do not force off-diagonal terms to vanish.}}$$
- Proving a non-zero total for a particular window requires a certified window-specific witness.
