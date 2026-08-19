# Riemann Hypothesis Equivalences & Circularity Screening Catalog

When auditing a mathematical argument or proposed lemma, verify that it does not smuggle in one of the following known equivalent statements or unproven assumptions.

## 1. Classical Analytic Equivalences

| Criterion | Formal Statement | Why Circular if Assumed |
| :--- | :--- | :--- |
| **Weil Positivity** | $\sum_{\rho} \hat{F}(\rho) \ge 0$ for all $F = f * f^*$ | Equivalent to RH (Weil 1952). Assuming positivity of explicit quadratic forms assumes RH. |
| **Li's Criterion** | $\lambda_n = \sum_\rho \left[1 - (1 - 1/\rho)^n\right] \ge 0 \quad \forall n \ge 1$ | Equivalent to RH (Li 1997, Keiper 1992). Assuming positivity of $\lambda_n$ assumes RH. |
| **Nyman-Beurling** | $\overline{\operatorname{span}}\left\{\rho_\alpha(x) = \{\alpha/x\} - \alpha\{1/x\} : 0 < \alpha \le 1\right\} = L^2(0, 1)$ | Distance $d_n \to 0$ in $L^2$ is strictly equivalent to RH (Beurling 1955, Nyman 1950). |
| **Mertens Bound** | $M(x) = \sum_{n \le x} \mu(n) = O(x^{1/2+\varepsilon}) \quad \forall \varepsilon > 0$ | Equivalent to RH (Littlewood 1912). |
| **PNT Error Bound** | $\psi(x) - x = O(x^{1/2}\log^2 x)$ or $\pi(x) - \operatorname{Li}(x) = O(x^{1/2}\log x)$ | Equivalent to RH (von Koch 1901). |
| **Zero-Free Region** | $\zeta(s) \neq 0$ for all $\Re(s) > 1/2$ | Direct definition/restatement of RH. |

---

## 2. Project-Specific Pitfalls & Pseudo-Symmetries

1. **Centrifuge Modulus Equivalence**:
   - Identity: $|q_\rho^K| = \tau^{K\delta}$.
   - Tautology: $|q_\rho^K| = 1 \iff \delta = 0$.
   - **Circularity trap**: Asserting that because $|q_\rho^K|=1$ on the critical line, all zeros must have $|q_\rho^K|=1$. The centrifuge measures off-line deviation; it does not prove $\delta=0$.

2. **Tau-Base Invariance**:
   - Fact: $\tau = 2\pi$ is a rotational base scale.
   - **False claim**: $\zeta(\tau^K s) = \zeta(s)$. Zeta does not possess scaling symmetry.

3. **Dirichlet Series in Critical Strip**:
   - Fact: $\sum_{n=1}^\infty n^{-s}$ converges only for $\Re(s) > 1$.
   - **False claim**: Applying Dirichlet series algebra directly inside $\Re(s) \in (0, 1)$ without analytic continuation.
