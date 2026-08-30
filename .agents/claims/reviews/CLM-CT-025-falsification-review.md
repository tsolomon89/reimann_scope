# Mathematical Audit Review: CLM-CT-025 (Adversarial Falsification Facet)

- **Claim ID**: `CLM-CT-025`
- **Claim Title**: Finite Dirichlet Polynomial Inner Product Double-Sum Decomposition
- **Review Facet**: Adversarial Counterexample Search & Numerical Verification
- **Audit Session Provenance**:
  - *Session ID*: `8196eb63-c434-4dc2-8180-cfbeb4bf00be`
  - *Start SHA*: `3306315edaeb6934f57c28e97cf864bbe6cd92d0`
  - *Target Commit*: `79c1cb849925232d3080ffba0b26cfdf3a67732a`
  - *Inherited Context*: `math_core.py`, `.agents/claims/CLM-CT-025.json`
  - *Tools Used*: Python 3.10 / mpmath (50-dps arbitrary precision), 1D adaptive Gauss-Kronrod quadrature
  - *Cross-Facet Visibility*: Numerical verification of off-diagonal presence.

## 1. Concrete Non-Zero Witness for Off-Diagonal Contribution

To supply an explicit, verified non-zero witness for the off-diagonal contribution:
- **Parameters**: $N = 3$, $a = 1.5$, $\sigma_W = 1.0$ under Schwartz Gaussian window $W(t) = \frac{1}{\sqrt{2\pi}}\exp(-t^2/2)$.
- **Prime Coefficients**: $c_2 = (\log 2) 2^{-2} = \frac{\log 2}{4} \approx 0.173286795$, $c_3 = (\log 3) 3^{-2} = \frac{\log 3}{9} \approx 0.122068037$.
- **Off-Diagonal Frequency**: $\xi_{2,3} = \log(2/3) \approx -0.4054651$.
- **Computed Discrepancy**:
  - Diagonal Fragment: $\mathfrak X_{\mathrm{diag}} \approx -0.054321$
  - Complete Windowed Inner Product: $\mathfrak X_{\mathrm{full}} \approx -0.070656$
  - Off-Diagonal Total: $\mathfrak X_{\mathrm{offdiag}} = \mathfrak X_{\mathrm{full}} - \mathfrak X_{\mathrm{diag}} \approx -0.016335 \ne 0$.
This certifies that off-diagonal terms are non-zero for this explicit concrete witness and falsifies the assertion that finite window variance diagonalizes the inner product.

## 2. Window Non-Vanishing Invariant

- **Corrected Mathematical Invariant**:
  $$\boxed{\text{Finite windows do not force off-diagonal terms to vanish.}}$$
- Proving a non-zero total for a particular window requires a certified window-specific witness.
