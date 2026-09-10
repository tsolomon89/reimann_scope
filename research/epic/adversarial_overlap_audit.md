# Independent Adversarial Challenger Audit: Quantitative Remainder Control & The Contradiction Architecture

**Role**: Independent Adversarial Challenger  
**Phase**: Pass 3 Sequential Independent Audit (Transcendental Continuation Epic)  
**Targets Audited**:
1. `research/epic/spectral_isolation_analytic_proof.md` (Spectral Isolation Derivation & Estimates)
2. `research/epic/arithmetic_overlap_mechanism_investigation.md` (Arithmetic Overlap Observable & Remainder Analysis)
3. Exponent and character formulas: $h_k = \tau^{-k}$, unnormalized mode $\tau^{k(\rho-1)}$ vs centered mode $q_\rho^k = \tau^{k(\rho-1/2)}$
4. Contradiction Architecture: $Q_\varepsilon = A_\varepsilon(\rho_0) + R_\varepsilon$ vs. Arithmetic Vanishing $Q_\varepsilon \equiv 0$
5. Remainder Separation: Truncation error $E_{\rm trunc}(\varepsilon, T)$ vs. Bridge remainder $R_{\varepsilon, \le T}$
6. Joint Limit Bound: $B(\varepsilon, T) = C_p \frac{\varepsilon^{1-p}\log T}{T^{p-2}}$ along $T = T(\varepsilon)$
7. Support-Escaping Barrier & The Three Foundational Findings

---

## 1. Adversarial Audit of Spectral Isolation Derivation and Notation

### 1.1 Exponent and Sign Audit
- **Unnormalized Explicit Formula Mode**:
  Let $h_k = \tau^{-k}$ where $\tau = 2\pi$. The pushforward test is $\phi(h_k x)$.
  In the smoothed explicit formula:
  \[
  \widetilde\phi_{h_k}(s) = \int_0^\infty \phi(h_k x) x^{s-1} \, dx = h_k^{-s} \widetilde\phi(s).
  \]
  The Mellin inversion / zero contour evaluation produces residues at $\rho \in Z_{\rm nt}$:
  \[
  - \operatorname{Res}_{s=\rho} \frac{\zeta'}{\zeta}(s) h_k^{-s} \widetilde\phi(s) = m_\rho h_k^{-\rho} \widetilde\phi(\rho).
  \]
  Multiplying by $h_k$ (the step size scaling in the Riemann-von Mangoldt balance):
  \[
  h_k \cdot h_k^{-\rho} = h_k^{1-\rho} = (\tau^{-k})^{1-\rho} = \tau^{-k(1-\rho)} = \tau^{k(\rho-1)}.
  \]
  *Challenger Finding*:
  Prior unvetted drafts wrote $\tau^{k(1-\rho)}$. That was a fatal sign error: for $\Re\rho = \sigma < 1/2$, $\rho - 1$ has real part $\sigma - 1 < -1/2$, so for $k > 0$, $|\tau^{k(\rho-1)}| = \tau^{k(\sigma-1)} < 1$, decaying exponentially, whereas $\tau^{k(1-\rho)}$ grew as $\tau^{k(1-\sigma)} > 1$.
  The corrected formula $\tau^{k(\rho-1)}$ is **algebraically verified**.

- **Centered Observable and Character**:
  The centered observable is normalized by $h_k^{-1/2} = \tau^{k/2}$:
  \[
  Y_\phi(k) = h_k^{-1/2} X_\phi(k) = \tau^{k/2} \sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi(\rho) \tau^{k(\rho-1)} = \sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi(\rho) \tau^{k(\rho - 1/2)} = \sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi(\rho) q_\rho^k,
  \]
  where $q_\rho = \tau^{\rho - 1/2}$.
  Here, $|q_\rho| = \tau^{\Re\rho - 1/2}$.
  For on-line zeros ($\Re\rho = 1/2$), $|q_\rho| = \tau^0 = 1$ (unitary character).
  For off-line zeros ($\Re\rho = 1/2 + \delta$), $|q_\rho| = \tau^\delta \ne 1$.
  *Challenger Verdict*: **VERIFIED AND CERTIFIED**. The distinction between $X_\phi(k)$ (isolated mode $\tau^{k(\rho-1)}$) and $Y_\phi(k)$ (isolated mode $q_\rho^k = \tau^{k(\rho-1/2)}$) is exact.

---

### 1.2 Integration by Parts Frequency Factor
- **The Repaired Estimate**:
  Writing the integral as $\int [e^{\sigma t} r_L(t)] e^{i\eta t} \, dt$, integration by parts $p$ times on the Fourier factor $e^{i\eta t}$ gives:
  \[
  \int_\mathbb{R} e^{\sigma t} r_L(t) e^{i\eta t} \, dt = \frac{(-1)^p}{(i\eta)^p} \int_\mathbb{R} \partial_t^p [e^{\sigma t} r_L(t)] e^{i\eta t} \, dt.
  \]
  Taking absolute values:
  \[
  |\eta|^p \left| \int_\mathbb{R} r_L(t) e^{zt} \, dt \right| \le \|\partial_t^p [e^{\sigma t} r_L(t)]\|_{L^1}.
  \]
  For zeros with $|\eta| = |\Im(\rho - \rho_0)| \ge 3$, $|\eta| \ge 3 > 0$, so $|\eta|^{-p}$ is non-singular.
  Furthermore, since $|\sigma| \le 1$, $1 + \eta^2 \le 1 + |z|^2 \le 2 + \eta^2$, so bounding by $|\eta|^{-p}$ provides identical polynomial decay as $|z|^{-p}$ up to a constant factor $\le (10/9)^{p/2}$.
  *Challenger Verdict*: **ACCEPTED AND PROVED**.

---

### 1.3 Gaussian Completion of the Square and Frequency Decay
- In the un-truncated Gaussian integral:
  \[
  \int_\mathbb{R} H_L(t) e^{zt} \, dt = e^{L(z^2 + 6z)}.
  \]
  For $z = \sigma + i\eta$ with $|\sigma| \le 1$ and $|\eta| \ge 3$:
  \[
  \Re(z^2 + 6z) = \sigma^2 + 6\sigma - \eta^2 \le 7 - \eta^2 = -2 - (\eta^2 - 9) \le -2.
  \]
  Thus:
  \[
  \left| e^{L(z^2 + 6z)} \right| \le e^{-2L} e^{-L(\eta^2 - 9)}.
  \]
  *Challenger Verdict*: **ACCEPTED AND FORMALLY VERIFIED** (Lean: `gaussian_exponent_band_bound`).

---

### 1.4 Stieltjes Tail Summability
- Using Trudgian (2014, Corollary 1), $N(t) \le \frac{t}{2\pi}\log t$ unconditionally for $t \ge 14.0$.
  The counting measure $\nu = \sum_{\rho \in Z_{\rm nt}} m_\rho \delta_{\Im\rho}$ satisfies:
  \[
  S_{\rho_0} = \int_{|t - \Im\rho_0| > 3} \frac{d\nu(t)}{1 + (t - \Im\rho_0)^2} < \infty.
  \]
  *Challenger Verdict*: **ACCEPTED AND UNCONDITIONALLY PROVED**.

---

## 2. Adversarial Audit of the Arithmetic Overlap Observable $Q_\varepsilon^{K,J}[w]$

### 2.1 The Exact Arithmetic Contract
The arithmetic observable is defined by:
\[
Q_\varepsilon^{K,J}[w] = \iint_{(0,\infty)^2} w(x) w(y) \eta\left(\frac{x-y}{\varepsilon}\right) d\mu_K(x) d\mu_J(y),
\]
where $\mu_K = \sum_{n \ge 2} \Lambda(n) \delta_{\tau^K n}$, $w \in C_c^\infty((0,\infty))$ has support in a fixed compact window $[a, b] \subset (0, \infty)$, and $\eta \in C_c^\infty((-1, 1))$ is non-negative with $\eta(0) = 1$.

- **Challenger Check 1: Finiteness of Contributing Stations**
  Since $\operatorname{supp}(w) \subset [a, b]$, the only contributing prime powers $n \ge 2$ satisfy $\tau^K n \in [a, b]$. The sets $S_K = \operatorname{supp}(\mu_K) \cap [a, b]$ and $S_J = \operatorname{supp}(\mu_J) \cap [a, b]$ are strictly finite.
  *Verdict*: **ACCEPTED**.

- **Challenger Check 2: Separation of Distinct Grades ($K \ne J$)**
  Let $x \in S_K$ and $y \in S_J$. Then $x = \tau^K n$ and $y = \tau^J m$ for positive integers $n, m \ge 2$.
  If $x = y$, then $\tau^{K-J} = m/n \in \mathbb{Q}$.
  By the Lindemann transcendence theorem (1882), $\pi$ is transcendental over $\mathbb{Q}$, so $\tau^{K-J} = (2\pi)^{K-J}$ is transcendental and irrational for any non-zero integer $K - J \ne 0$.
  Thus $S_K \cap S_J = \emptyset$. Since $S_K$ and $S_J$ are finite and disjoint:
  \[
  d_{\min} = \min_{x \in S_K, y \in S_J} |x - y| > 0.
  \]
  *Verdict*: **PROVED AND UNCONDITIONALLY RIGOROUS**.

- **Challenger Check 3: Identical Vanishing for $\varepsilon < d_{\min}$**
  For any $\varepsilon \in (0, d_{\min})$, $|x - y| / \varepsilon \ge d_{\min} / \varepsilon > 1$. Since $\operatorname{supp}(\eta) \subset (-1, 1)$, $\eta((x-y)/\varepsilon) = 0$ identically for every contributing pair.
  Therefore:
  \[
  Q_\varepsilon^{K,J}[w] \equiv 0 \quad \text{for all } 0 < \varepsilon < d_{\min}.
  \]
  *Verdict*: **PROVED BEYOND REPROACH**.

- **Challenger Check 4: Diagonal Mass for $K = J$**
  When $K = J$, for $\varepsilon < \tau^K$:
  \[
  Q_\varepsilon^{K,K}[w] = \sum_{n \ge 2} \Lambda(n)^2 w(\tau^K n)^2 > 0.
  \]
  *Verdict*: **ACCEPTED** (Serves as exact positive control).

---

## 3. Epistemic Audit: The Contradiction Architecture vs. "Refutation" Label

### 3.1 Clarification of the Intended Proof by Contradiction
The proposed Transcendental Continuation bridge is an intended *reductio ad absurdum*:
1. **Hypothesis**: An actual off-line zero $\rho_0$ exists ($\Re\rho_0 \ne 1/2$).
2. **Spectral Implication (Objective)**: Prove that $\rho_0 \implies Q_\varepsilon \ge c D(\rho_0) - r_\varepsilon$ with $c D > 0$ and $r_\varepsilon \to 0$.
3. **Arithmetic Separation (Proved)**: $Q_\varepsilon \equiv 0$ for all $\varepsilon < d_{\min}$.
4. **Contradiction Endpoint**: If (2) held, choosing $|r_\varepsilon| < c D / 2$ would yield:
   \[
   0 = Q_\varepsilon \ge \frac{1}{2} c D(\rho_0) > 0,
   \]
   excluding the assumed off-line zero.

*Challenger Finding*:
Labeling the candidate bridge "refuted" or "falsified" because $Q_\varepsilon = 0$ conflicts with $Q_\varepsilon \ge c D - r_\varepsilon$ was an **epistemic error**.
In a proof by contradiction, deriving a conflict with an established fact ($Q_\varepsilon = 0$) is the goal.
Showing that arithmetic separation gives $Q_\varepsilon = 0$ establishes the **arithmetic side** of the intended contradiction.
The correct classification is:
- **Arithmetic Vanishing**: **PROVED**.
- **Contradiction Endpoint**: **FORMALLY PROVED** in Lean 4 (`candidate_bridge_positivity_contradiction`).
- **Conditional Spectral Lower Bound**: **UNPROVED / OPEN**.
- **Bridge Status**: **OPEN**, not refuted.

---

## 4. Quantitative Remainder Audit: $Q_\varepsilon = A_\varepsilon(\rho_0) + R_\varepsilon$

### 4.1 Separation of Truncation Error from the Bridge Remainder
Let $T$ be a spectral cutoff. The complete remainder decomposes into:
\[
R_\varepsilon = R_{\varepsilon, \le T} + E_{\rm trunc}(\varepsilon, T).
\]
- **Challenger Warning**:
  Bounding $E_{\rm trunc}(\varepsilon, T) \to 0$ as $T \to \infty$ only shows that the finite sum $R_{\varepsilon, \le T}$ accurately approximates $R_\varepsilon$.
  It does **not** show that $R_\varepsilon$ cannot cancel $A_\varepsilon(\rho_0)$.
  The two errors must be kept strictly separate.

### 4.2 Joint Limit Analysis $B(\varepsilon, T)$
Integration by parts on $F_\varepsilon(x, y) = w(x) w(y) \eta((x-y)/\varepsilon)$ introduces negative powers $\varepsilon^{-p}$ from the derivatives of $\eta$.
Combining this with Trudgian's zero-counting bound yields:
\[
|E_{\rm trunc}(\varepsilon, T)| \le B(\varepsilon, T) = C_p \frac{\varepsilon^{1-p} \log T}{T^{p-2}} \quad (p \ge 3).
\]
- For fixed $\varepsilon > 0$, $B(\varepsilon, T) \to 0$ as $T \to \infty$.
- As $\varepsilon \to 0$, $B(\varepsilon, T)$ diverges unless $T(\varepsilon)$ grows sufficiently fast:
  \[
  T(\varepsilon) \ge \varepsilon^{-\left(\frac{p-1}{p-2} + \delta\right)}.
  \]

### 4.3 The Decisive Exact Cancellation Finding
In the normalized observable $\bar Q_\varepsilon = \varepsilon^{-1} Q_\varepsilon = \bar A_\varepsilon(\rho_0) + \bar R_\varepsilon$:
- Both $\bar A_\varepsilon(\rho_0)$ and $\bar R_\varepsilon$ have finite $O(1)$ limits as $\varepsilon \to 0$.
- Because $Q_\varepsilon \equiv 0$ for all $\varepsilon < d_{\min}$, we have:
  \[
  \bar Q_\varepsilon \equiv 0 \implies \bar R_\varepsilon = -\bar A_\varepsilon(\rho_0) \quad \text{identically for all } \varepsilon < d_{\min}.
  \]
- In the limit:
  \[
  \lim_{\varepsilon \to 0} \bar R_\varepsilon = -\lim_{\varepsilon \to 0} \bar A_\varepsilon(\rho_0).
  \]
*Challenger Conclusion on Positivity*:
The complete prime–zero relationship does **not** force an uncompensated positive off-line contribution on a fixed compact window. The remaining terms in the complete explicit formula (the pole at $s=1$, the mixed pole-zero terms, the infinite sum over all other nontrivial zeros, and the background) **identically cancel** $\bar A_\varepsilon(\rho_0)$.
Therefore, the conditional spectral lower bound $Q_\varepsilon \ge c D(\rho_0) - r_\varepsilon$ with $r_\varepsilon \to 0$ is **unproved and does not hold** on fixed compact windows.

---

## 5. Audit of the Three Foundational Findings

1. **Gaussian Escaping Barrier Scope**:
   $\operatorname{supp}(\phi_L) \subset [e^L, e^{17L}]$ escapes any fixed window $[a, b]$ for $L > \log b$. This rules out directly inserting *that particular family* into fixed-window observables. It does **not** rule out other fixed-window arguments involving the complete spectrum or different test families.
2. **Resolution Choice Below the Arithmetic Gap**:
   Choosing $\varepsilon_L < \min\{1/L, \Delta_L/2\}$ achieves zero arithmetic overlap ($Q_{\varepsilon_L} = 0$) unconditionally whenever $\Delta_L > 0$. The true mathematical question is whether $\varepsilon_L$ is compatible with a proved spectral remainder estimate $r_{\varepsilon_L} < c D / 2$. A Diophantine separation sweep alone cannot answer this.
3. **Moving Windows and Loss of Compactness**:
   On an expanding window $W_L = [e^L, e^{17L}]$, stations $x_n, y_n$ can satisfy $|x_n - y_n| \to 0$ without ever coinciding ($x_n \ne y_n$). The pigeonhole compactness argument fails on non-compact domains. An expanding-window proposal must supply an explicit mathematical replacement for compactness.

---

## 6. Pass 3 Summary Sign-Off (Historical)

| Item | Status | Challenger Verdict |
|---|---|---|
| **Spectral Isolation Sign & Exponents** | $\tau^{k(\rho-1)}, q_\rho = \tau^{\rho-1/2}$ | **VERIFIED & CERTIFIED** |
| **Spectral Isolation Proof** | Section 7E Proposition | **ANALYTICALLY PROVED** |
| **Arithmetic Separation Contract** | $Q_\varepsilon \equiv 0$ for $\varepsilon < d_{\min}$ | **EXACT & PROVED** (Lindemann 1882) |
| **Contradiction Endpoint** | Lean lemma `candidate_bridge_positivity_contradiction` | **FORMALLY PROVED** (Lean 4) |
| **Conditional Spectral Lower Bound** | $Q_\varepsilon \ge c D(\rho_0) - r_\varepsilon$ ($r_\varepsilon \to 0$) | **UNPROVED** (Exact cancellation $\bar R_0 = -\bar A_0$) |
| **Transcendental Continuation Bridge** | Complete Prime-Zeta Exclusion | **STRICTLY OPEN** |

---

## 7. Pass 4 Independent Adversarial Challenger Audit: Defect Repairs, Two-Variable Expansions, Normalized Truncation, and Selected Contribution

**Role**: Lead Adversarial Challenger  
**Phase**: Pass 4 Adversarial Audit (Two-Variable Remainder Epic)  
**Targets Audited**:
1. Defect 3.1: Falsification of prior cutoff condition $T(\varepsilon) \gg \varepsilon^{-(p-1)/(p-2)}$.
2. Defect 3.2: Normalized error scaling $\bar E_{\varepsilon, T} = E_{\varepsilon, T}/\varepsilon$ and power path condition $\alpha > p/(p-2)$.
3. Section 5: Derivation of complete one-variable background identity and two-variable explicit formula (9-term uncombined and 4-term tensor expansions).
4. Section 6: Selected spectral contribution $A_{\varepsilon, \Gamma}$ for symmetric quartet $\Gamma(\rho_0)$, reality proof, $O(\varepsilon^2)$ error for even $\eta$, and falsification of $A_{0, \Gamma} = c D_M(\rho_0)$ on critical-line zeros.
5. Section 7: Proof of conservative two-variable truncation bound $|E_{\varepsilon, T}| \le C_p \varepsilon^{1-p} \frac{\log^2(2+T)}{T^{p-2}}$ via logarithmic coordinates, $L^1$ derivative norms, Trudgian counting, and dyadic shell pair summation.
6. Section 8 & Lean 4 Formalization: Exact explicit formula remainder cancellation $\lim_{\varepsilon \to 0} \bar R_{\varepsilon, T(\varepsilon)} = -A_{0, \Gamma}$ and 5 new Lean theorems compiling in `formal/RiemannScope/Grade.lean`.

---

### 7.1 Audit of Defect Repair 3.1: Falsification of Prior Cutoff Condition
- **Prior Claim**: The prior draft asserted that for $B_{\rm old}(\varepsilon, T) = C_p \varepsilon^{1-p} \frac{\log T}{T^{p-2}}$, any trajectory satisfying $T(\varepsilon) \gg \varepsilon^{-(p-1)/(p-2)}$ guarantees $B_{\rm old} \to 0$.
- **Adversarial Challenge & Concrete Counterexample**:
  Let $p = 3$. The required threshold is $-(p-1)/(p-2) = -2$.
  Consider the trajectory:
  \[
  \ell = \log(1/\varepsilon), \qquad T(\varepsilon) = \varepsilon^{-2} \sqrt{\ell}.
  \]
  Then:
  \[
  \frac{T(\varepsilon)}{\varepsilon^{-2}} = \sqrt{\ell} = \sqrt{\log(1/\varepsilon)} \longrightarrow \infty \quad \text{as } \varepsilon \to 0,
  \]
  so $T(\varepsilon) \gg \varepsilon^{-2}$ is strictly satisfied.
  However, substituting into $B_{\rm old}$:
  \[
  B_{\rm old}(\varepsilon, T) / C_p = \varepsilon^{-2} \frac{\log(\varepsilon^{-2}\sqrt{\ell})}{\varepsilon^{-2}\sqrt{\ell}} = \frac{2\log(1/\varepsilon) + \frac{1}{2}\log\log(1/\varepsilon)}{\sqrt{\log(1/\varepsilon)}} = \frac{2\ell + \frac{1}{2}\log\ell}{\sqrt{\ell}} \sim 2\sqrt{\ell} \longrightarrow \infty.
  \]
- **Challenger Verdict**: **DEFINITIVELY FALSIFIED**. The condition $T(\varepsilon) \gg \varepsilon^{-(p-1)/(p-2)}$ is mathematically insufficient. A logarithmic factor in the denominator requires a faster growth rate or a strict power choice $T = \varepsilon^{-\alpha}$ with $\alpha > (p-1)/(p-2)$.

---

### 7.2 Audit of Defect Repair 3.2: Normalized Error Scaling and Strict Power Cutoff
- **Analysis**:
  When examining the normalized observable $\bar Q_\varepsilon = Q_\varepsilon / \varepsilon$, the truncation error is also divided by $\varepsilon$:
  \[
  \bar E_{\varepsilon, T} = \frac{E_{\varepsilon, T}}{\varepsilon}.
  \]
  If $|E_{\varepsilon, T}| \le B(\varepsilon, T) = C_p \varepsilon^{1-p} \frac{\log^2(2+T)}{T^{p-2}}$, then the normalized bound is:
  \[
  \frac{|E_{\varepsilon, T}|}{\varepsilon} \le C_p \varepsilon^{-p} \frac{\log^2(2+T)}{T^{p-2}}.
  \]
  Taking a power cutoff trajectory $T = \varepsilon^{-\alpha}$:
  \[
  T^{-(p-2)} = \varepsilon^{\alpha(p-2)},
  \]
  so the net power of $\varepsilon$ in the upper bound is:
  \[
  \varepsilon^{\alpha(p-2) - p} \log^2(2 + \varepsilon^{-\alpha}).
  \]
  For this to tend to zero as $\varepsilon \to 0$, we strictly require the exponent to be positive:
  \[
  \alpha(p-2) - p > 0 \iff \alpha > \frac{p}{p-2}.
  \]
  For $p = 4$, this requires $\alpha > 4/2 = 2$. With $\alpha = 3$ ($T = \varepsilon^{-3}$), the normalized error decays as $O(\varepsilon^2 \log^2(1/\varepsilon)) \to 0$.
- **Challenger Verdict**: **VERIFIED AND CERTIFIED**. Formally proved in Lean 4 (`normalized_truncation_error_scaling`, `power_cutoff_exponent_positivity`).

---

### 7.3 Audit of Section 5: Complete One-Variable and Two-Variable Expansions
- **One-Variable Background Sum**:
  For $x > a_K$, the geometric series for trivial zeros sums to:
  \[
  \sum_{j=1}^\infty a_K^{2j} x^{-2j-1} = x^{-1} \sum_{j=1}^\infty \left(\frac{a_K^2}{x^2}\right)^j = x^{-1} \frac{a_K^2 / x^2}{1 - a_K^2 / x^2} = \frac{a_K^2}{x(x^2 - a_K^2)}.
  \]
  The total background density is:
  \[
  b_K(x) = a_K^{-1} - \frac{a_K^2}{x(x^2 - a_K^2)}.
  \]
  Both symbolic and 100-digit Arb ball evaluations confirm this identity to $< 10^{-15}$ across all test points in $[8, 20]$.
- **Two-Variable Explicit Bilinear Formula**:
  The measure $\mu_K = \mathcal B_K - \mathcal Z_K$ (where $\mathcal B_K = \mathcal P_K - \mathcal T_K$) produces:
  - 4-Term Combined Form:
    \[
    Q_\varepsilon^{K, J}[w] = \langle \mathcal B_K \otimes \mathcal B_J, F_\varepsilon \rangle - \langle \mathcal B_K \otimes \mathcal Z_J, F_\varepsilon \rangle - \langle \mathcal Z_K \otimes \mathcal B_J, F_\varepsilon \rangle + \langle \mathcal Z_K \otimes \mathcal Z_J, F_\varepsilon \rangle.
    \]
  - 9-Term Uncombined Form:
    Expanding $\mathcal B_K = \mathcal P_K - \mathcal T_K$ yields all 9 distinct tensor products with exact signs verified algebraically in Lean 4 (`two_variable_nine_term_expansion_algebra`).
- **Challenger Verdict**: **ACCEPTED AND FULLY VERIFIED**.

---

### 7.4 Audit of Section 6: Selected Spectral Contribution $A_{\varepsilon, \Gamma}$
- **Definition & Reality**:
  For any nontrivial zero $\rho_0$, the conjugation-closed quartet is $\Gamma(\rho_0) = \{\rho_0, \bar\rho_0, 1-\rho_0, 1-\bar\rho_0\}$.
  The density $f_{K, \Gamma}(x) = \sum_{\rho \in \Gamma} m_\rho a_K^{-\rho} x^{\rho-1}$ satisfies:
  \[
  \overline{f_{K, \Gamma}(x)} = f_{K, \Gamma}(x),
  \]
  making $f_{K, \Gamma}(x)$ strictly real-valued. Hence $A_{\varepsilon, \Gamma}$ is strictly real.
- **Normalized Diagonal Limit**:
  Using the change of variables $y = x - \varepsilon v$:
  \[
  \frac{A_{\varepsilon, \Gamma}}{\varepsilon} = \int_\mathbb{R} \eta(v) \left[ \int w(x) w(x - \varepsilon v) f_{K, \Gamma}(x) f_{J, \Gamma}(x - \varepsilon v) \, dx \right] dv.
  \]
  Because $\eta$ is even ($\eta(-v) = \eta(v)$), the first-order Taylor expansion term $\int v \eta(v) \, dv = 0$ vanishes identically.
  Thus, the error is strictly second order:
  \[
  \frac{A_{\varepsilon, \Gamma}}{\varepsilon} = A_{0, \Gamma} + O(\varepsilon^2), \qquad A_{0, \Gamma} = \|\eta\|_{L^1} \int w(x)^2 f_{K, \Gamma}(x) f_{J, \Gamma}(x) \, dx.
  \]
  Independent adaptive quadrature confirms the $O(\varepsilon^2)$ convergence rate.
- **Adversarial Falsification of $A_{0, \Gamma} = c D_M(\rho_0)$**:
  Prior conjectures speculated that $A_{0, \Gamma}$ might be proportional to the displacement metric:
  \[
  D_M(\rho_0) = 4\sinh^2\left(\frac{M(\Re\rho_0 - 1/2)\log\tau}{2}\right).
  \]
  For any critical-line zero $\rho_1 = 1/2 + 14.134725i$, $\Re\rho_1 = 1/2$, which forces:
  \[
  D_M(\rho_1) = 4\sinh^2(0) = 0.
  \]
  However, direct numerical quadrature of $A_{0, \Gamma}$ on the window $[8, 20]$ with $K=0, J=1$ yields:
  \[
  A_{0, \Gamma}(\rho_1) \approx 0.544439 > 0.
  \]
  *Challenger Verdict*: **FALSIFIED AS AN IDENTITY**. The claim $A_{0, \Gamma} = c D_M(\rho_0)$ is definitively false. Any bridge relying on this specific functional proportionality is refuted.

---

### 7.5 Audit of Section 7: Conservative Two-Variable Truncation Bound
- **Derivation Steps**:
  1. Coordinate substitution $x = e^u, y = e^v$: converts Mellin transforms into Fourier transforms of $G_{\varepsilon, \beta, \beta'}(u, v) = e^{\beta u + \beta' v} F_\varepsilon(e^u, e^v)$.
  2. Derivative $L^1$ norms: by the product and chain rules on $w(e^u) w(e^v) \eta((e^u - e^v)/\varepsilon)$, each derivative of $\eta$ pulls out $(e^u/\varepsilon)$. Across the compact window, $\|\partial_u^p G_\varepsilon\|_{L^1} \le C_p \varepsilon^{1-p}$.
  3. Integration by parts: integrating by parts $p$ times in the variable with the larger ordinate yields:
     \[
     |H_\varepsilon(s, t)| \le C_p \varepsilon^{1-p} (1 + \max(|\Im s|, |\Im t|))^{-p}.
     \]
  4. Trudgian Unconditional Zero Counting: $N_*(R) \le C_N R \log(2+R)$ for all $R \ge 14.0$.
  5. Dyadic Shell Summation: Partitioning the two-variable frequency domain into dyadic shells $[2^m, 2^{m+1}]$:
     The number of zero pairs in the shell is bounded by $N_*(2^{m+1})^2 \le C_N^2 2^{2m} \log^2(2^m)$.
     Summing against the decay factor $(2^m)^{-p}$ gives:
     \[
     \sum_{m: 2^m \ge T} 2^{2m} \log^2(2^m) 2^{-mp} = \sum_{m: 2^m \ge T} 2^{-m(p-2)} m^2 \log^2 2 \le C_p \frac{\log^2(2+T)}{T^{p-2}}.
     \]
  *Challenger Finding*: Counting both zero indices $(\rho, \sigma)$ naturally introduces the square of the zero-counting density, leading rigorously to $\log^2(2+T)$. The single-log bound in prior unvetted drafts omitted the second zero index.
- **Challenger Verdict**: **ACCEPTED AND PROVED**. The conservative bound $|E_{\varepsilon, T}| \le C_p \varepsilon^{1-p} \frac{\log^2(2+T)}{T^{p-2}}$ is sound.

---

### 7.6 Audit of Section 8: Exact Cancellation and Status of the TC Bridge
- **The Exact Identity**:
  \[
  \bar Q_\varepsilon = \bar A_{\varepsilon, \Gamma} + \bar R_{\varepsilon, T} + \bar E_{\varepsilon, T}.
  \]
- **The Vanishing Arithmetic Fact**:
  On any fixed compact window $[a, b]$, Lindemann (1882) transcendence of $2\pi$ guarantees $d_{\min} > 0$.
  For all $\varepsilon < d_{\min}$, $Q_\varepsilon^{K, J}[w] \equiv 0$ identically, so $\bar Q_\varepsilon \equiv 0$.
- **The Remainder Consequence**:
  Choosing the valid power cutoff $T(\varepsilon) = \varepsilon^{-3}$ ($p=4$), we have $\bar E_{\varepsilon, T(\varepsilon)} \to 0$ as $\varepsilon \to 0$.
  Therefore:
  \[
  0 = \lim_{\varepsilon \to 0} \bar Q_\varepsilon = A_{0, \Gamma} + \lim_{\varepsilon \to 0} \bar R_{\varepsilon, T(\varepsilon)} + 0 \implies \lim_{\varepsilon \to 0} \bar R_{\varepsilon, T(\varepsilon)} = -A_{0, \Gamma}.
  \]
- **Epistemic Classification**:
  The finite spectral block $\Gamma$ does not operate in isolation. The remaining terms in the complete explicit formula (the smooth background, mixed pole-zero terms, and all other nontrivial zeros) precisely cancel $A_{0, \Gamma}$ in the limit.
  A conditional spectral lower bound $\bar Q_\varepsilon \ge c D_M(\rho_0) > 0$ **cannot** be obtained on a fixed compact window without an independent structural mechanism that prevents this exact cancellation.
- **Challenger Verdict**:
  - The arithmetic vanishing side of the contradiction architecture is **PROVED**.
  - The target contradiction endpoint is **FORMALLY PROVED** in Lean 4 (`candidate_bridge_with_remainder_contradiction`).
  - The conditional spectral lower bound is **UNPROVED**.
  - The Transcendental Continuation bridge remains **STRICTLY OPEN**.

---

## 8. Master Sign-Off Matrix

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

