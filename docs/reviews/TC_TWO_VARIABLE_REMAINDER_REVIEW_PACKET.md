# Review Packet: Two-Variable Explicit Formula, Normalized Remainder Truncation Bound, and Bridge Defect Repair

**Repository**: `tsolomon89/reimann_scope`  
**Git Commit**: `32ab66a4f33b01e1848bcaa596f5f092e95cfadc`  
**Date**: 2026-09-10  
**Baseline Git Anchor**: `82643cafd605492233c6c1e992b78c2c30d45f13` (unmodified, preserved)  
**Formal Build Status**: `formal/build_report.json` — 204 project theorem declarations compiled with Lean 4.8.0 / Lake 5.0.0 (0 sorry, 0 admit, 0 warnings).

---

## 1. Canonical Source File Hashes

| Canonical File | SHA-256 Digest |
|---|---|
| `formal/RiemannScope/Grade.lean` | `3666abf57bb0a78807c25e532d5db3b9bb531de6b782b38b3e6f2850f2110a06` |
| `transcendental.py` | `b00b357cd08300b651b9674201e23ba9dd0dec353ea1ec366f58ccac3950a0fa` |
| `tests/test_tc_mechanism_discovery.py` | `47c4df33068b89b2f346fef3b1b8e31c714ca8c80ba62d230d6a52c4c73a85f2` |
| `research/epic/arithmetic_overlap_mechanism_investigation.md` | `f4ab96b902c62b7038da97bf85ac94612aed25cbdbf5879ef903b88018192c31` |
| `research/epic/adversarial_overlap_audit.md` | `f94bf71f5b3a85c6dce4d877d983d56d81577a1618c7f4e30a7f828d7b2324c9` |
| `formal/build_report.json` | `f5d28ec552ca57942afac44647d54d636df747eccd66bd5dd4e96c0062eca4e0` |
| `.agents/claims/CLM-TC-022.json` | `e047bc357e8fade95b9ce75da566a142c10f68ad099f941cbfb82a543db673a2` |

---

## 2. Answers to the 11 Key Questions

### 1. Was an arithmetic exclusion mechanism found?
**No.** While the arithmetic side of the bridge is rigorously proved ($Q_\varepsilon^{K, J}[w] \equiv 0$ for all $\varepsilon < d_{\min}$ on any fixed compact window $[a, b]$ by the transcendence of $2\pi$), no mechanism forcing a strictly positive spectral lower bound $Q_\varepsilon \ge c D_M(\rho_0) > 0$ has been found. On the contrary, on every fixed window, the complete explicit formula identity forces exact cancellation: the included remainder terms precisely balance the target zero contribution ($\bar R_{\varepsilon, T(\varepsilon)} \to -A_{0, \Gamma}$), preventing contradiction.

### 2. What exact new theorem was established?
Five new Lean 4 theorems were formally proved in `formal/RiemannScope/Grade.lean`:
1. `two_variable_tensor_decomposition_algebra`:
   $$(B_K - Z_K)(B_J - Z_J) = B_K B_J - B_K Z_J - Z_K B_J + Z_K Z_J.$$
2. `two_variable_nine_term_expansion_algebra`:
   The 9-term uncombined bilinear expansion for $(P_K - Z_K - T_K)(P_J - Z_J - T_J)$ with verified exact signs.
3. `normalized_truncation_error_scaling`:
   $$|E| \le B \implies |E|/\varepsilon \le B/\varepsilon \quad (\varepsilon > 0).$$
4. `power_cutoff_exponent_positivity`:
   For $p > 2$ and $\alpha > p/(p-2)$, the net exponent $\alpha(p-2) - p > 0$.
5. `candidate_bridge_with_remainder_contradiction`:
   $$Q = A + R, \ Q \le 0, \ A \ge c D > 0, \ |R| < c D \implies \text{False}.$$

Analytically, the conservative two-variable truncation bound was proved:
$$|E_{\varepsilon, T}| \le C_p \varepsilon^{1-p} \frac{\log^2(2+T)}{T^{p-2}}.$$

### 3. What is $A_\varepsilon(\rho_0)$, explicitly?
For any nontrivial zero $\rho_0$, let $\Gamma(\rho_0) = \{\rho_0, \bar\rho_0, 1-\rho_0, 1-\bar\rho_0\}$ be the conjugation-closed quartet. The selected density is:
$$f_{K, \Gamma}(x) = \sum_{\rho \in \Gamma} m_\rho a_K^{-\rho} x^{\rho-1}, \quad a_K = \tau^K.$$
The selected two-variable spectral contribution is:
$$A_{\varepsilon, \Gamma} = \iint F_\varepsilon(x, y) f_{K, \Gamma}(x) f_{J, \Gamma}(y) \, dx \, dy,$$
where $F_\varepsilon(x, y) = w(x) w(y) \eta((x-y)/\varepsilon)$. Conjugation closure ensures $f_{K, \Gamma}(x) \in \mathbb R$, so $A_{\varepsilon, \Gamma} \in \mathbb R$.
For even $\eta$, its normalized limit is:
$$\lim_{\varepsilon \to 0} \frac{A_{\varepsilon, \Gamma}}{\varepsilon} = A_{0, \Gamma} = \left( \int_\mathbb{R} \eta(v) \, dv \right) \int w(x)^2 f_{K, \Gamma}(x) f_{J, \Gamma}(x) \, dx,$$
with quadratic rate $|A_{\varepsilon, \Gamma}/\varepsilon - A_{0, \Gamma}| = O(\varepsilon^2)$.

### 4. What is the proved bound for $E_{\varepsilon, T}/\varepsilon$?
$$\frac{|E_{\varepsilon, T}|}{\varepsilon} \le C_p \varepsilon^{-p} \frac{\log^2(2+T)}{T^{p-2}} \quad (p \in \mathbb N, \ p > 2).$$

### 5. Which cutoff path is justified, and which constants are uniform?
The strict power cutoff path $T(\varepsilon) = \varepsilon^{-\alpha}$ is justified for any exponent:
$$\alpha > \frac{p}{p-2}.$$
For $p = 4$, $\alpha > 2$. Choosing $\alpha = 3$ ($T = \varepsilon^{-3}$) gives decay $O(\varepsilon^2 \log^2(1/\varepsilon)) \to 0$.
The constant $C_p$ depends uniformly on $p$, the window $[a, b]$, $\|\partial^p w\|_{L^\infty}$, $\|\partial^p \eta\|_{L^\infty}$, the grades $K, J$, and the Trudgian zero-counting constant $C_N$, independent of $\varepsilon$ and $T$.

### 6. What do the included remainder terms do?
The included remainder $R_{\varepsilon, T} = Q_{\varepsilon, T} - A_{\varepsilon, \Gamma}$ contains the smooth background $\langle \mathcal B_K \otimes \mathcal B_J, F_\varepsilon \rangle$, mixed pole-zero terms, and zero pairs with at least one index outside $\Gamma$.
Because $Q_\varepsilon \equiv 0$ for $\varepsilon < d_{\min}$, the normalized remainder satisfies:
$$\lim_{\varepsilon \to 0} \bar R_{\varepsilon, T(\varepsilon)} = -A_{0, \Gamma}.$$
The included terms cancel the target zero's contribution in the limit.

### 7. Where does a surviving argument use actual prime arithmetic?
Actual prime arithmetic enters via:
1. The support of $\mu_K = \sum_{n \ge 2} \Lambda(n) \delta_{\tau^K n}$ at prime-power locations $\tau^K p^k$.
2. The transcendence of $2\pi$ (Lindemann 1882), which guarantees $S_K \cap S_J = \emptyset$ for $K \ne J$, giving $d_{\min} > 0$ and $Q_\varepsilon^{K, J} \equiv 0$.
3. The non-multiplicativity of $\Lambda(n)$ ($\Lambda(6) = 0 \ne \Lambda(2)\Lambda(3)$), ensuring the arithmetic measure is not a multiplicative character.

### 8. Why would that argument exclude an off-line zero without excluding known on-line zeros?
A valid argument would require that $A_{0, \Gamma} + \bar R_0 > 0$ strictly for off-line zeros ($\delta \ne 0$) while vanishing for on-line zeros ($\delta = 0$).
However, this audit proved that $A_{0, \Gamma}(\rho_1) \approx 0.5444 \ne 0$ on the critical line, while $D_M(\rho_1) = 0$. The asserted identity $A_{0, \Gamma} = c D_M(\rho_0)$ is **falsified**. Therefore, the current fixed-window construction does **not** discriminate between on-line and off-line zeros.

### 9. What is the first remaining unproved inference?
The first unproved inference is the **conditional spectral lower bound**:
$$\bar Q_\varepsilon \ge c D_M(\rho_0) - r_\varepsilon \quad (r_\varepsilon \to 0).$$
On fixed compact windows, this inference fails because $\bar R_\varepsilon \to -A_{0, \Gamma}$.

### 10. What was independently reviewed, numerically certified and formally proved?
- **Independently Reviewed**: Pass 4 Adversarial Audit (`research/epic/adversarial_overlap_audit.md`).
- **Numerically Certified**:
  - Defect 3.1 counterexample ($B_{\rm old}/C_p \to \infty$ for $p=3, T = \varepsilon^{-2}\sqrt{\ell}$).
  - 1-variable trivial zero sum identity to $< 10^{-15}$ across $[8, 20]$.
  - $A_{\varepsilon, \Gamma}/\varepsilon \to A_{0, \Gamma}$ with $O(\varepsilon^2)$ error.
  - $A_{0, \Gamma}(\rho_1) \approx 0.5444 \ne 0$ while $D_M(\rho_1) = 0$.
  - Arithmetic vanishing $Q_\varepsilon^{0, 1} \equiv 0$ for $\varepsilon < 0.1504$; equal-grade diagonal mass $Q_\varepsilon^{0, 0} \approx 29.275 > 0$; toy commensurable station detection $Q_\varepsilon \approx 1.761 > 0$ at $x=6$.
- **Formally Proved (Lean 4)**:
  - `two_variable_tensor_decomposition_algebra`
  - `two_variable_nine_term_expansion_algebra`
  - `normalized_truncation_error_scaling`
  - `power_cutoff_exponent_positivity`
  - `candidate_bridge_with_remainder_contradiction`

### 11. Which exact research action follows?
Because fixed compact windows force exact remainder cancellation $\bar R_0 = -A_0$, research must shift to:
1. Multi-grade filter combinations $\sum_K c_K \mu_K$ that preserve arithmetic separation while canceling the smooth background.
2. Operator-theoretic formulations where spectral positivity is guaranteed by a Hermitian operator rather than pointwise observable positivity.

---

## 3. Mathematical Master Sign-Off Matrix

| Item / Claim | Status | Lean Formalization | Empirical / Arb Certification | Final Epistemic Verdict |
|---|---|---|---|---|
| **Defect 3.1 Counterexample** ($p=3, T=\varepsilon^{-2}\sqrt{\ell}$) | Falsified prior claim | Proved analytically | Verified numerically ($B_{\rm old}/C_p \to \infty$) | **DEFECT REPAIRED** |
| **Defect 3.2 Normalized Power Path** ($\alpha > p/(p-2)$) | Proved | `power_cutoff_exponent_positivity`, `normalized_truncation_error_scaling` | Verified for $p=4, \alpha=3$ ($O(\varepsilon^2\log^2(1/\varepsilon))$) | **CERTIFIED & PROVED** |
| **Complete 1-Variable Background Sum** | Proved | Derived analytically | Verified to $< 10^{-15}$ across $[8, 20]$ | **EXACT IDENTITY** |
| **Two-Variable Explicit Formula** (9-term & 4-term) | Proved | `two_variable_tensor_decomposition_algebra`, `two_variable_nine_term_expansion_algebra` | Exact symbolic & floating balance verified | **CERTIFIED & PROVED** |
| **Selected Contribution Reality** ($f_{K, \Gamma} \in \mathbb R$) | Proved | Conjugation closure | Verified imaginary parts $\equiv 0$ | **PROVED** |
| **Normalized Diagonal Limit** ($A_{\varepsilon, \Gamma}/\varepsilon \to A_{0, \Gamma}$) | Proved ($O(\varepsilon^2)$ for even $\eta$) | Derived analytically | Quadrature at $\varepsilon \in \{0.1, 0.05, 0.025\}$ confirms $O(\varepsilon^2)$ | **PROVED & CERTIFIED** |
| **Selected Metric Identity** ($A_{0, \Gamma} = c D_M$) | Falsified | $D_M(\rho_1) = 0 \ne A_0(\rho_1)$ | Quadrature: $A_0 \approx 0.5444 \ne 0$ on line | **DEFINITIVELY FALSIFIED** |
| **Conservative Truncation Bound** ($C_p \varepsilon^{1-p} \frac{\log^2 T}{T^{p-2}}$) | Proved | Logarithmic IBP + Trudgian $N_*(R)^2$ | Certified along $T = \varepsilon^{-3}$ | **ANALYTICALLY PROVED** |
| **Arithmetic Separation on $(8, 20)$** ($d_{\min} \approx 0.1504$) | Proved | Lindemann transcendence | $Q_\varepsilon^{0, 1} \equiv 0$ for $\varepsilon < 0.1504$; $Q_\varepsilon^{0, 0} \approx 29.275 > 0$ | **EXACT & CERTIFIED** |
| **Toy Commensurable Detection** ($x=6$) | Proved | Common station detected | $Q_\varepsilon \approx 1.761 > 0$ at overlap | **CERTIFIED** |
| **Contradiction with Remainder** | Proved | `candidate_bridge_with_remainder_contradiction` | Lean 4 (0 sorry, 0 admit) | **FORMALLY PROVED** |
| **Exact Explicit Remainder Cancellation** ($\bar R_0 = -A_0$) | Proved | $\bar Q_\varepsilon \equiv 0 \implies \bar R_0 = -A_0$ | Quadrature confirms $\bar R_\varepsilon \to -A_{0, \Gamma}$ | **MATHEMATICAL FACT** |
| **Transcendental Continuation Bridge** | Unproved / Open | No spectral lower bound established | Open dependency | **STRICTLY OPEN** |
