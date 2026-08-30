# Mathematical Audit Review: CLM-CT-025 (Adversarial Falsification Facet)

- **Claim ID**: `CLM-CT-025`
- **Claim Title**: Finite Dirichlet Polynomial Inner Product Double-Sum Decomposition
- **Review Facet**: Adversarial Counterexample Search & Numerical Verification
- **Audit Review Provenance**:
  - *Review Type*: Structured Single-Agent Review (`STRUCTURED_SINGLE_AGENT_REVIEW_COMPLETED`)
  - *Session ID*: `8196eb63-c434-4dc2-8180-cfbeb4bf00be`
  - *Start SHA*: `3306315edaeb6934f57c28e97cf864bbe6cd92d0`
  - *Target Commit*: `615d24a37cccc1f4e9410a8c2b7d35092f99e873`
  - *Inherited Context*: `math_core.py`, `.agents/claims/CLM-CT-025.json`
  - *Tools Used*: Python 3.10 / mpmath (50-dps arbitrary precision), python-flint (Arb ball enclosures), 1D adaptive Gauss-Kronrod quadrature
  - *Isolation Conditions*: Single-agent multi-angle verification facet.

## 1. Concrete Non-Zero Certified Witness for Off-Diagonal Contribution

Under the documented formulas:
- **Parameters**: $N = 3$, $a = 1.5$, $\sigma_W = 1.0$, variance $v = 1.0$ under Schwartz Gaussian window $W(t) = \frac{1}{\sqrt{2\pi}}\exp(-t^2/2)$.
- **Prime Coefficients**: $c_2 = \frac{\log 2}{4} \approx 0.1732867951399863$, $c_3 = \frac{\log 3}{9} \approx 0.1220680371981881$.
- **Off-Diagonal Frequency**: $\xi_{2,3} = \log(2/3) \approx -0.4054651081081644$.

### Three Independent Concordant Evaluations (50 dps):
1. **Closed-Form Gaussian Fourier Evaluation**:
   $$\widehat W(\xi) = e^{-\xi^2/2}, \quad \widehat{tW}(\xi) = -i\xi e^{-\xi^2/2}, \quad \widehat{t^2W}(\xi) = (1-\xi^2)e^{-\xi^2/2}$$
   $$\mathcal I_{m,n}(W) = e^{-\xi_{mn}^2/2} \left[ (-a L_n + a^2 L_n^2) + \xi_{mn}(L_n - 2a L_n^2) - L_n^2 (1 - \xi_{mn}^2) \right]$$
2. **Direct Double-Sum Kernel Evaluation** (`math_core.finite_windowed_dirichlet_polynomial_inner_product`):
   - Diagonal Fragment: $\mathfrak X_{\mathrm{diag}} = -0.051550895340248184469...$
   - Complete Windowed Inner Product: $\mathfrak X_{\mathrm{full}} = -0.024020042430325337239...$
   - Off-Diagonal Total: $\mathfrak X_{\mathrm{offdiag}} = +0.027530852909922847230...$
3. **Direct Numerical 1D Quadrature**:
   $$\int_{-\infty}^\infty W(t) \Re(F_0(t) \overline{\ddot F_0(t)}) dt = -0.024020042430325337239...$$
   Agreement: $|\mathfrak X_{\mathrm{full}} - \text{Quad}| < 10^{-45}$.

### Arb Certified Outward-Rounded Enclosures:
- $\mathfrak X_{\mathrm{diag}} \in [-0.051550895340248 \pm 4.08\times 10^{-16}]$
- $\mathfrak X_{\mathrm{full}} \in [-0.02402004243033 \pm 5.50\times 10^{-15}]$
- $\mathfrak X_{\mathrm{offdiag}} \in [0.02753085290992 \pm 3.46\times 10^{-15}]$ strictly positive ($> 0$).

This certifies that off-diagonal terms are strictly non-zero for this explicit concrete witness and falsifies the assertion that finite window variance diagonalizes the inner product.

## 2. Window Non-Vanishing Invariant

- **Corrected Mathematical Invariant**:
  $$\boxed{\text{Finite windows do not force off-diagonal terms to vanish.}}$$
- Proving a non-zero total for a particular window requires a certified window-specific witness.
