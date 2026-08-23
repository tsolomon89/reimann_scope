# Mathematical Obligation and Test Vector Register

This register details all unresolved proof obligations, mandatory deterministic test vectors, and falsification test standards required by the research harness.

## 1. Mandatory Contract Test Vectors (from `MATH_CONTRACT.md` §13)

| Vector ID | Name | Mathematical Parameters | Expected Symbolic / Numerical Output | Test Harness Module |
| :--- | :--- | :--- | :--- | :--- |
| `VEC-A` | Identity Transform | $K = 0$ | All scale factors equal $1$; $\Re(s') = 1/2$; $\rho' = \rho$. | `test_contract_identities.py::test_vector_a_identity` |
| `VEC-B` | Origin Dilation | $K = 1, \tau = 2\pi$ | $\Re(s') = \tau/2 = \pi$; Zero map $\rho' = \tau\rho$. | `test_contract_identities.py::test_vector_b_origin_dilation` |
| `VEC-C` | Centered Dilation | $K = 1, \tau = 2\pi$ | $\Re(s') = 1/2$; Zero map $\rho' = 1/2 + \tau(\rho - 1/2)$. | `test_contract_identities.py::test_vector_c_centered_dilation` |
| `VEC-D` | Inverse Kernel Lock | $A = 2, B = 1/2, C = D = 0$ | $AB = 1$; $\mathcal{Z}_{2,0,1/2,0}(s) = \zeta(s)$ identically. | `test_contract_identities.py::test_vector_d_inverse_kernel_lock` |
| `VEC-E` | Radial Centrifuge | $\delta = 10^{-4}, K = 100, \tau = 2\pi$ | $\log\|q_\rho^K\| = 0.01 \log\tau$; $\|q_\rho^K\| = \tau^{0.01}$. | `test_contract_identities.py::test_vector_e_radial_centrifuge` |
| `VEC-F` | On-Line Centrifuge | $\delta = 0, \forall K \in \mathbb{R}$ | $\|q_\rho^K\| = 1$; $\log\|q_\rho^K\| = 0$; $\frac{d}{dK}\log\|q_\rho^K\| = 0$. | `test_contract_identities.py::test_vector_f_online_centrifuge` |

---

## 2. Core Mathematical Trust Obligations (from `SPEC.md` §12)

| Obligation ID | Property | Mathematical Definition | Verification Method | Status |
| :--- | :--- | :--- | :--- | :--- |
| `OBL-001` | Generic $\zeta(s)$ Evaluation | High-precision certified evaluation across complex plane | Arb/Flint ball enclosure | `Verified in Harness` |
| `OBL-002` | Schwarz Reflection Symmetry | $\zeta(\bar s) = \overline{\zeta(s)}$ | Exact SymPy + Arb ball check at generic non-real $s$ | `Verified in Harness` |
| `OBL-003` | Functional Equation | $\xi(s) = \xi(1-s)$ where $\xi(s) = \frac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$ | Arbitrary precision error bound $|\xi(s) - \xi(1-s)| < 10^{-50}$ | `Verified in Harness` |
| `OBL-004` | Baseline Zero Discovery | Independent root bracket & refinement on $\Re(s)=1/2$ | Hardy $Z(t)$ sign change scanning + Newton/Arb solver | `Specified in Harness` |
| `OBL-005` | Zero Residual Guarantee | Enclosure of discovered roots $\gamma_n$ with $|\zeta(1/2+i\gamma_n)| < \varepsilon$ | Certified Arb evaluation at root | `Specified in Harness` |
| `OBL-006` | Explicit Formula Truncation | Prime reconstruction $J_N(x)$ and $\pi_N(x)$ convergence | Möbius inversion unit tests against known prime sieve | `Specified in Harness` |
| `OBL-007` | Single Zero Perturbation Response | Exact differential update $\Delta C_n(x) = C(x, \rho'_n) - C(x, \rho_n)$ | Unit test comparing delta update to full recomputation | `Specified in Harness` |
| `OBL-008` | Centrifuge Derivative Invariant | $\frac{d}{dK} \log \|q_\rho^K\| = \delta \log \tau$ | Exact symbolic derivation & numerical gradient test | `Verified in Harness` |
| `OBL-009` | Counterexample Falsification Control | Davenport-Heilbronn function fails on-line zero hypothesis | Numerical search finding off-line zeros for non-Euler zeta | `Verified in Harness` |
| `OBL-EF-003` | Projection Trap Resolution | Derive independent arithmetic or spectral representation of $\mathcal P_0(\mathcal D_\zeta)$ to deduce $\Delta\mathcal D_{\mathrm{rad}} = 0$ | Open global constraint derivation | `OPEN OBLIGATION` |


---

## 3. Retained Falsification Controls and Negative Probes

1. **Non-Euler Product Control (Davenport-Heilbronn)**:
   $$f(s) = \frac{1-i\kappa}{2} L(s, \chi_5) + \frac{1+i\kappa}{2} L(s, \bar\chi_5)$$
   Satisfies functional equation $f(s) = \chi(s) f(1-s)$ but has zeros off the critical line in the critical strip (e.g. at $\sigma \approx 0.808, t \approx 85.699$).
   *Purpose*: Proves that satisfying a functional equation and real-symmetry is insufficient to ensure all zeros are on the critical line without the Euler product.

2. **Off-Line Zero Amplification Control**:
   Artificially set $\delta = 10^{-3}$ and test $K = 50 \implies |q_\rho^K| = \tau^{0.05} \approx 1.0963 \neq 1$.
   *Purpose*: Proves that the centrifuge cleanly separates on-line ($\delta=0$) from off-line ($\delta \neq 0$) zeros.

3. **Dirichlet Divergence Control**:
   Evaluate partial sum $\sum_{n=1}^{1000} n^{-(0.5 + 14.134725i)}$ and compare with true $\zeta(0.5 + 14.134725i) = 0$.
   *Purpose*: Proves that naive Dirichlet summation in the critical strip produces massive truncation error and cannot be used as an analytic continuation.
