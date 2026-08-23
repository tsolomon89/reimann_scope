# Canonical Claim Register

Authoritative register of mathematical claims, formalization targets, and empirical assertions in `reimann_scope`.

| Claim ID | Formal Statement | Mathematical Layer | Epistemic Status | Reference Document | Formalization Target |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `CLM-TC-001` | Extended family $\mathcal{Z}_\tau(s, k) = \zeta(\tau^{-k}s)$ satisfies $\mathcal{Z}_\tau(s, 0) = \zeta(s)$ identically. | Transcendental Continuation | PROVED / EXACT | `TRANSCENDENTAL_CONTINUATION.md` | Lean 4 mathlib lemma |
| `CLM-TC-002` | Zero worldline $s_\rho(k) = \tau^k \rho$ satisfies $\mathcal{Z}_\tau(s_\rho(k), k) = 0$ for all $k \in \mathbb{R}$. | Transcendental Continuation | PROVED / EXACT | `TRANSCENDENTAL_CONTINUATION.md` | Lean 4 mathlib lemma |
| `CLM-TC-003` | Normalized radial coordinate $R_\tau(s_\rho(k), k) = \tau^{-k}\Re(s_\rho(k)) - 1/2 = \delta$ identically across all grades. | Radial Foliation | PROVED / EXACT | `TRANSCENDENTAL_CONTINUATION.md` | Lean 4 mathlib lemma |
| `CLM-TC-004` | Bilateral discrete defect $D_K(\rho) = (\tau^{K\delta} - 1)(1 - \tau^{-K\delta})$ satisfies $|D_K| = 4\sinh^2(K\delta\ln\tau / 2)$. | Grade Constraints | PROVED / EXACT | `MATH_CONTRACT.md` | Lean 4 mathlib lemma |
| `CLM-COV-001` | Under coupled dilation $s' = As, x' = x^{1/A}$, wave terms satisfy $C_J(x^{1/A}, A\rho) = C_J(x, \rho)$ identically. | Converter Gauge | PROVED / EXACT | `MATH_CONTRACT.md` | Lean 4 explicit formula theorem |
| `CLM-IKL-001` | Under inverse scale lock $AB=1, C=D=0$, Dirichlet kernel transform $\mathcal{Z}_{A,0,1/A,0}(s) = \zeta(s)$ identically. | Kernel Lab | PROVED / EXACT | `MATH_CONTRACT.md` | Lean 4 kernel theorem |
| `CLM-COH-001` | Derivative-normalized paths $P_n(u) = \zeta(s_n(u)) / [i\Delta_n\zeta'(\rho_n)]$ possess bounded Taylor shape coefficients $c_{2,n}, c_{3,n}$ across spectrum blocks. | Cross-Height Coherence | RETAINED (Empirical 80-dps) | `CROSS_HEIGHT_COHERENCE.md` | Asymptotic expansion lemma |
| `CLM-EF-001` | Grade-\(K\) explicit formula constraint \(\mathcal C_{K,j}[H] \equiv \mathcal C_0[H \circ a_K]\) is coordinate-redundant with native explicit formula evaluations. | Explicit Formula | PROVED / EXACT | `MATH_CONTRACT.md` §35 | Lean 4 / SymPy pullback identity |
| `CLM-EF-002` | Any prospective cross-grade joint arithmetic constraint operating without test-function dilation is an open candidate distinct from \(\mathcal C_{K,j}\). | Explicit Formula | OPEN / CANDIDATE | `MATH_CONTRACT.md` §35 | Rigidity theorem search |
| `CLM-EF-003` | Radial second-order Taylor response $\Delta\mathcal C_h[\mathcal O(\rho)] = -2\delta^2 h''(\gamma) + \mathcal O(\delta^4)$ is an exact finite synthetic sensitivity diagnostic; inferring global non-compensation is subject to the Projection Trap and remains open. | Explicit Formula | SENSITIVITY DIAGNOSTIC | `MATH_CONTRACT.md` §36 | Lean 4 Taylor lemma / OBL-EF-003 |
| `CLM-RH-001` | Exclusivity of radial leaf $R_\tau = 0$: all nontrivial zeros of $\zeta(s)$ have $\delta = 0$. | Central Programme | OPEN / CONJECTURED (RH) | `RESEARCH_HYPOTHESIS.md` | Global contradiction proof |
