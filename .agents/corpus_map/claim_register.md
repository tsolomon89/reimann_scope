# Mathematical Claim Register

This register catalogues every mathematical assertion, definition, identity, and claim in the research corpus, categorized with standardized claim-status labels.

## Standard Claim Status Labels
- `Definition`: Foundational definition or coordinate system.
- `Established external theorem`: Proven theorem from external mathematical literature.
- `Algebraic identity`: Exact symbolic identity holding by algebra.
- `Derived lemma`: Lemma derived rigorously within the contract.
- `Proposed lemma`: Proposed mathematical step pending full derivation/proof.
- `Conjecture`: Open mathematical conjecture (e.g. Riemann Hypothesis).
- `Numerical observation`: Empirical numerical data point or statistic (never to be called proof).
- `Heuristic`: Plausible intuitive or approximate mathematical argument.
- `Open proof obligation`: Unresolved formal requirement or implementation contract obligation.
- `Circular or potentially circular`: Claim that assumes an equivalent form of RH or assumes unproven symmetry.
- `Contradicted`: Statement in conflict with canonical documents or mathematical facts.
- `Falsified`: Statement proven false by counterexample.
- `Superseded`: Earlier decision or formulation replaced by an authoritative update.

---

## Claim Catalog

| ID | Statement / Claim | Source Document | Mathematical Formulation | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `CLM-001` | Full turn constant $\tau$ | `MATH_CONTRACT.md` §1 | $\tau = 2\pi$ | `Definition` | Rotational base scale. |
| `CLM-002` | Raw complex coordinate $s$ | `MATH_CONTRACT.md` §1 | $s = \sigma + it$ | `Definition` | Standard complex parameter for $\zeta(s)$. |
| `CLM-003` | Centered coordinate $z$ | `MATH_CONTRACT.md` §1 | $z = s - 1/2 = \delta + it$ | `Definition` | Offset from critical line $\sigma = 1/2$. |
| `CLM-004` | Riemann Hypothesis in centered coordinates | `SPEC.md` §2 | $\forall \rho \in \zeta^{-1}(0) \cap \mathbb{S}, \delta = \Re(\rho) - 1/2 = 0$ | `Conjecture` | The Riemann Hypothesis. $\mathbb{S}$ is critical strip. |
| `CLM-005` | Camera transformation invariance | `MATH_CONTRACT.md` §2 | $T_{\mathrm{camera}}(s) = s$ | `Algebraic identity` | Viewport transformation only; no math change. |
| `CLM-006` | Height sampling transformation | `MATH_CONTRACT.md` §3 | $s_K(u) = 1/2 + \delta + i(t_0 + \tau^K u)$ | `Definition` | Modifies ordinate sampling range; $\Re(s)=1/2+\delta$. |
| `CLM-007` | Origin coordinate dilation zero mapping | `MATH_CONTRACT.md` §4 | $s' = \tau^K s \implies \rho' = \tau^K \rho$ | `Algebraic identity` | For $f_K(s') = \zeta(s'/\tau^K)$, zeros scale by $\tau^K$. |
| `CLM-008` | Origin coordinate dilation critical line image | `MATH_CONTRACT.md` §4 | $\Re(s') = \tau^K/2$ | `Algebraic identity` | Critical line shifts under origin dilation. |
| `CLM-009` | $\tau$-dilation is not a zeta automorphism | `MATH_CONTRACT.md` §4 | $\zeta(\tau^K s) \neq \zeta(s)$ in general | `Established external theorem` | Dilating argument does not preserve zeta values. |
| `CLM-010` | Centered coordinate dilation zero mapping | `MATH_CONTRACT.md` §5 | $s' = 1/2 + \tau^K(s-1/2) \implies \rho' = 1/2 + \tau^K(\rho-1/2)$ | `Algebraic identity` | Fixes critical line $\Re(s') = 1/2$. |
| `CLM-011` | Argument transform zero mapping | `MATH_CONTRACT.md` §6 | $f_K(s) = \zeta(\tau^K s) \implies s_\rho = \rho/\tau^K$ | `Algebraic identity` | Critical zeros map to $\Re(s) = 1/(2\tau^K)$. |
| `CLM-012` | General arithmetic kernel continuation | `MATH_CONTRACT.md` §7 | $\mathcal{Z}_{A,C,B,D}(s) = e^{-C(Bs+D)}\zeta(A(Bs+D))$ | `Definition` | Canonical implementation across critical strip. |
| `CLM-013` | Transformed kernel zero mapping | `MATH_CONTRACT.md` §7 | $s_\rho = \frac{\rho/A - D}{B}$ ($AB \neq 0$) | `Algebraic identity` | Exact zero location for kernel deformation. |
| `CLM-014` | Inverse Scale Lock invariance | `MATH_CONTRACT.md` §8 | $AB = 1, C=D=0 \implies \mathcal{Z}_{A,0,1/A,0}(s) = \zeta(s)$ | `Algebraic identity` | Exponent pairing $(Bs)(A\log n) = s\log n$ is preserved. |
| `CLM-015` | Centered kernel mode invariance | `MATH_CONTRACT.md` §9 | $AB = 1 \implies \mathcal{Z}^{\mathrm{ctr}}_{A,1/A}(z) = \zeta(1/2+z)$ | `Algebraic identity` | Argument $1/2+ABz$ equals $1/2+z$. |
| `CLM-016` | Anisotropic centered map is non-holomorphic | `MATH_CONTRACT.md` §10 | $A_\delta \neq A_\gamma \implies$ non-holomorphic | `Derived lemma` | Violates Cauchy-Riemann equations. |
| `CLM-017` | Zero character centrifuge magnitude | `MATH_CONTRACT.md` §11 | $q_\rho = \tau^{\rho-1/2} \implies \|q_\rho\| = \tau^\delta$ | `Algebraic identity` | Exact modulus for $\rho = 1/2+\delta+i\gamma$. |
| `CLM-018` | Grade $K$ radial amplification | `MATH_CONTRACT.md` §11 | $\|q_\rho^K\| = \tau^{K\delta}$ | `Algebraic identity` | Exact radial scaling under real grade $K$. |
| `CLM-019` | Centrifuge log-slope identity | `MATH_CONTRACT.md` §11 | $\frac{d}{dK}\log\|q_\rho^K\| = \delta\log\tau$ | `Algebraic identity` | Rate of radial growth is proportional to $\delta$. |
| `CLM-020` | Critical line centrifuge invariance | `MATH_CONTRACT.md` §11 | $\delta = 0 \implies \|q_\rho^K\| = 1 \quad \forall K \in \mathbb{R}$ | `Algebraic identity` | Unimodular character for on-line zeros. |
| `CLM-021` | Truncated Riemann prime-power formula | `MATH_CONTRACT.md` §12 | $J_N(x) = \operatorname{Li}(x) - 2\Re\sum_{\rho}\operatorname{Li}(x^\rho) - \log 2 + \int_x^\infty \frac{du}{u(u^2-1)\log u}$ | `Established external theorem` | Truncated explicit formula (Riemann 1859, Edwards). |
| `CLM-022` | Prime staircase reconstruction via Möbius inversion | `MATH_CONTRACT.md` §12 | $\pi_N(x) = \sum_{m\ge1}\frac{\mu(m)}{m}J_N(x^{1/m})$ | `Established external theorem` | Exact Möbius inversion for prime counting. |
| `CLM-023` | Schwarz reflection principle for $\zeta$ | `SPEC.md` §12 | $\zeta(\bar s) = \overline{\zeta(s)}$ | `Established external theorem` | Real on real axis $\implies$ Schwarz reflection. |
| `CLM-024` | Riemann functional equation | `SPEC.md` §12 | $\pi^{-s/2}\Gamma(s/2)\zeta(s) = \pi^{-(1-s)/2}\Gamma((1-s)/2)\zeta(1-s)$ | `Established external theorem` | Global symmetry $\xi(s) = \xi(1-s)$. |
| `CLM-025` | Hardy $Z$-function real-valuedness | `SPEC.md` §6 | $Z(t) = e^{i\theta(t)}\zeta(1/2+it) \in \mathbb{R}$ for $t \in \mathbb{R}$ | `Established external theorem` | Enables stable 1D root-finding on critical line. |
| `CLM-026` | Dirichlet series divergence in critical strip | `DECISIONS.md` §2026-08-19 | $\sum_{n=1}^\infty n^{-s}$ diverges for $\Re(s) \le 1$ | `Established external theorem` | Using $\sum n^{-s}$ in critical strip is invalid. |
| `CLM-027` | Assertion that $\tau$-grade implies RH | Hypothetical / Anti-pattern | Claiming $\|q_\rho^K\|=1 \implies \delta=0$ proves RH | `Circular or potentially circular` | $\|q_\rho^K\|=1 \iff \delta=0$ is definition/tautology; does not prove $\delta=0$. |
| `CLM-028` | Davenport-Heilbronn counterexample | External / Control | $\exists f(s)$ with functional equation but zeros off $\Re(s)=1/2$ | `Established external theorem` | Davenport-Heilbronn (1936); demonstrates Euler product necessity. |
