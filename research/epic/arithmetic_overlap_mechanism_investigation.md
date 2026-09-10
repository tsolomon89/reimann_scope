# Arithmetic Overlap Mechanism Investigation: Quantitative Remainder Analysis & The Contradiction Architecture

**Role**: Arithmetic Researcher  
**Epic Track**: Section 8 & Arithmetic Overlap Observable Investigation  
**Primary Question**: Does the complete prime–zero relationship force a positive off-line contribution that the remaining spectral and background terms cannot cancel?

---

## 1. Concrete Arithmetic Measures & Overlap Observable

Let $\Lambda(n)$ be the von Mangoldt function on $\mathbb{N}_{\ge 1}$.
Recall that $\Lambda$ is **non-multiplicative**:
\[
\Lambda(6) = 0 \ne \Lambda(2)\Lambda(3) = \log 2 \cdot \log 3 \approx 0.7618 > 0.
\]
The prime-power structure enters exclusively via the Dirichlet series logarithmic derivative on $\Re(s) > 1$:
\[
-\frac{\zeta'}{\zeta}(s) = \sum_{n \ge 2} \Lambda(n) n^{-s}.
\]

Define the positive, locally finite prime-power measure on $(0, \infty)$:
\[
\mu_0 = \sum_{n \ge 2} \Lambda(n) \delta_n.
\]
Under coordinate dilation $D_a(x) = ax$ with scale $a = \tau^K$ ($K \in \mathbb{Z}, \ \tau = 2\pi$):
\[
\mu_K = (D_{\tau^K})_* \mu_0 = \sum_{n \ge 2} \Lambda(n) \delta_{\tau^K n}.
\]
The support of $\mu_K$ consists strictly of scaled prime powers:
\[
\operatorname{supp}(\mu_K) = \left\{ \tau^K p^m : p \text{ prime}, m \ge 1 \right\} \subset L_K = \tau^K \mathbb{Z}.
\]

### Definition 1.1 (The Arithmetic Overlap Observable $Q_\varepsilon^{K, J}[w]$)
Fix two distinct grades $K \ne J \in \mathbb{Z}$.
Fix a non-negative, non-zero test window $w \in C_c^\infty((0, \infty))$ with compact support:
\[
\operatorname{supp}(w) \subset [a, b] \subset (0, \infty) \quad (0 < a < b < \infty).
\]
Fix a non-negative mollifier $\eta \in C_c^\infty((-1, 1))$ with $\eta(0) = 1$, $\eta(-u) = \eta(u)$, and $I_\eta = \int_{-1}^1 \eta(u) \, du > 0$.
For $\varepsilon > 0$, define the two-variable overlap observable:
\[
Q_\varepsilon^{K, J}[w] := \iint_{(0, \infty)^2} w(x) w(y) \eta\left( \frac{x - y}{\varepsilon} \right) d\mu_K(x) d\mu_J(y).
\]
Because $\mu_K$ and $\mu_J$ are discrete Radon measures on $(0, \infty)$, $Q_\varepsilon^{K, J}[w]$ evaluates to the double sum:
\[
Q_\varepsilon^{K, J}[w] = \sum_{n \ge 2} \sum_{m \ge 2} \Lambda(n) \Lambda(m) w(\tau^K n) w(\tau^J m) \eta\left( \frac{\tau^K n - \tau^J m}{\varepsilon} \right).
\]

---

## 2. The Exact Arithmetic Contract (Proved Arithmetic Vanishing)

### Theorem 2.1 (The Arithmetic Separation Contract)
Let $K, J \in \mathbb{Z}$, and let $w \in C_c^\infty((0, \infty))$ with $\operatorname{supp}(w) \subset [a, b]$.
Define the active station sets in $[a, b]$:
\[
S_K = \operatorname{supp}(\mu_K) \cap [a, b] = \left\{ \tau^K n : n \ge 2, \ \Lambda(n) > 0, \ \tau^K n \in [a, b] \right\},
\]
\[
S_J = \operatorname{supp}(\mu_J) \cap [a, b] = \left\{ \tau^J m : m \ge 2, \ \Lambda(m) > 0, \ \tau^J m \in [a, b] \right\}.
\]
Then:
1. **Finiteness**: $S_K$ and $S_J$ are strictly finite:
   \[
   |S_K| \le \frac{b - a}{\tau^K} + 1 < \infty, \qquad |S_J| \le \frac{b - a}{\tau^J} + 1 < \infty.
   \]
2. **Strict Disjointness for Distinct Grades ($K \ne J$)**:
   If $K \ne J$, then $S_K \cap S_J = \emptyset$.
   Consequently, if both $S_K$ and $S_J$ are non-empty, the inter-grade minimum station distance:
   \[
   d_{\min} := \min_{x \in S_K, \ y \in S_J} |x - y| > 0
   \]
   is strictly positive.
3. **Identical Arithmetic Vanishing for Small $\varepsilon$**:
   For any $0 < \varepsilon < d_{\min}$:
   \[
   Q_\varepsilon^{K, J}[w] \equiv 0 \quad \text{identically}.
   \]
   *(If $S_K = \emptyset$ or $S_J = \emptyset$, $Q_\varepsilon^{K, J}[w] = 0$ for all $\varepsilon > 0$.)*
4. **Diagonal Mass Control ($K = J$)**:
   When $K = J$, for all $\varepsilon < \tau^K$:
   \[
   Q_\varepsilon^{K, K}[w] = \sum_{n \ge 2} \Lambda(n)^2 w(\tau^K n)^2 > 0,
   \]
   which is strictly positive whenever $[a, b]$ contains at least one prime-power station $\tau^K p^m$.

*Proof.*
1. Since $\tau^K > 0$ and $[a, b]$ is compact, $n$ is restricted to $[a/\tau^K, b/\tau^K]$, containing finitely many integers. Thus $S_K$ and $S_J$ are finite.
2. Suppose $x \in S_K \cap S_J$. Then $x = \tau^K n = \tau^J m$ for integers $n, m \ge 2$ with $\Lambda(n)\Lambda(m) > 0$.
   Since $K \ne J$, assume $K > J$. Then:
   \[
   \tau^{K - J} = \frac{m}{n} \in \mathbb{Q}_{>0}.
   \]
   However, $\tau = 2\pi$. By the Lindemann transcendence theorem (1882), $\pi$ is transcendental over $\mathbb{Q}$, hence $\tau = 2\pi$ is transcendental, and any positive integer power $\tau^{K - J}$ is transcendental. A transcendental number cannot equal a rational $m/n \in \mathbb{Q}$.
   Therefore, no such $x$ can exist: $S_K \cap S_J = \emptyset$. Since $S_K$ and $S_J$ are finite, the finite set of positive distances $\{|x - y| : x \in S_K, y \in S_J\}$ attains a strictly positive minimum $d_{\min} > 0$.
3. For every $(x, y) \in S_K \times S_J$, $|x - y| \ge d_{\min}$. If $\varepsilon < d_{\min}$, then $|x - y| / \varepsilon \ge d_{\min} / \varepsilon > 1$. Since $\operatorname{supp}(\eta) \subset (-1, 1)$, $\eta((x-y)/\varepsilon) = 0$ for all contributing pairs. Since $w$ vanishes outside $[a, b]$, every term in the double sum vanishes identically: $Q_\varepsilon^{K, J}[w] = 0$.
4. For $K = J$, diagonal pairs have $x = y = \tau^K n \implies (x-y)/\varepsilon = 0 \implies \eta(0) = 1$. Off-diagonal pairs have $|x - y| = \tau^K |n - m| \ge \tau^K$. For $\varepsilon < \tau^K$, all off-diagonal terms vanish, isolating the positive diagonal sum. $\blacksquare$

---

## 3. The Unabridged Two-Variable Graded Explicit Formula

To analyze the spectral expansion of $Q_\varepsilon^{K, J}[w]$, define the two-variable smooth kernel:
\[
F_\varepsilon(x, y) := w(x) w(y) \eta\left( \frac{x - y}{\varepsilon} \right) \in C_c^\infty((0, \infty)^2).
\]
Its two-variable Mellin transform is:
\[
\widetilde F_\varepsilon(s_1, s_2) = \iint_{(0, \infty)^2} F_\varepsilon(x, y) x^{s_1 - 1} y^{s_2 - 1} \, dx \, dy.
\]
By Mellin inversion on lines $\Re(s_1) = c_1 > 1, \Re(s_2) = c_2 > 1$:
\[
Q_\varepsilon^{K, J}[w] = \left(\frac{1}{2\pi i}\right)^2 \int_{(c_1)} \int_{(c_2)} \left(-\frac{\zeta'}{\zeta}(s_1)\right) \left(-\frac{\zeta'}{\zeta}(s_2)\right) \tau^{-K s_1 - J s_2} \widetilde F_\varepsilon(s_1, s_2) \, ds_1 \, ds_2.
\]

Shifting the contours across the critical strips to $\Re(s) = -\delta < 0$ and picking up the residues at $s = 1$, the nontrivial zeros $\rho \in Z_{\rm nt}$, and the trivial zeros $s = -2j$:

### Proposition 3.1 (Complete Unabridged Two-Variable Explicit Expansion)
\[
Q_\varepsilon^{K, J}[w] = \mathcal{M}_{1, 1}(\varepsilon) - \mathcal{M}_{1, \rm spec}(\varepsilon) - \mathcal{M}_{\rm spec, 1}(\varepsilon) + \mathcal{M}_{\rm spec, spec}(\varepsilon) + \mathcal{R}_{\rm bg}(\varepsilon),
\]
where each term is explicitly given by:
1. **Pole–Pole Residue**:
   \[
   \mathcal{M}_{1, 1}(\varepsilon) = \tau^{-K - J} \widetilde F_\varepsilon(1, 1) = \tau^{-K - J} \iint_{(0, \infty)^2} w(x) w(y) \eta\left(\frac{x - y}{\varepsilon}\right) \, dx \, dy.
   \]
2. **Mixed Pole–Zero Residues**:
   \[
   \mathcal{M}_{1, \rm spec}(\varepsilon) = \tau^{-K} \sum_{\rho_2 \in Z_{\rm nt}} m_{\rho_2} \tau^{-J \rho_2} \widetilde F_\varepsilon(1, \rho_2),
   \]
   \[
   \mathcal{M}_{\rm spec, 1}(\varepsilon) = \tau^{-J} \sum_{\rho_1 \in Z_{\rm nt}} m_{\rho_1} \tau^{-K \rho_1} \widetilde F_\varepsilon(\rho_1, 1).
   \]
3. **Double Spectral Zero–Zero Sum**:
   \[
   \mathcal{M}_{\rm spec, spec}(\varepsilon) = \sum_{\rho_1 \in Z_{\rm nt}} \sum_{\rho_2 \in Z_{\rm nt}} m_{\rho_1} m_{\rho_2} \tau^{-K \rho_1 - J \rho_2} \widetilde F_\varepsilon(\rho_1, \rho_2).
   \]
4. **Complete Background Term $\mathcal{R}_{\rm bg}(\varepsilon)$**:
   \[
   \mathcal{R}_{\rm bg}(\varepsilon) = \sum_{j \ge 1} \sum_{\ell \ge 1} \tau^{2jK + 2\ell J} \widetilde F_\varepsilon(-2j, -2\ell) - \tau^{-K} \sum_{\ell \ge 1} \tau^{2\ell J} \widetilde F_\varepsilon(1, -2\ell) - \tau^{-J} \sum_{j \ge 1} \tau^{2jK} \widetilde F_\varepsilon(-2j, 1)
   \]
   \[
   + \sum_{\rho_1 \in Z_{\rm nt}} \sum_{\ell \ge 1} m_{\rho_1} \tau^{-K\rho_1 + 2\ell J} \widetilde F_\varepsilon(\rho_1, -2\ell) + \sum_{j \ge 1} \sum_{\rho_2 \in Z_{\rm nt}} m_{\rho_2} \tau^{2jK - J\rho_2} \widetilde F_\varepsilon(-2j, \rho_2) + \mathcal{I}_{\rm arch}(\varepsilon),
   \]
   where $\mathcal{I}_{\rm arch}(\varepsilon)$ denotes the contour integrals along the shifted vertical lines $\Re(s) = -\delta$.

---

## 4. Quantitative Remainder Decomposition: $Q_\varepsilon = A_\varepsilon(\rho_0) + R_\varepsilon$

Assume the existence of an actual off-line nontrivial zero:
\[
\rho_0 = \beta_0 + i\gamma_0 \quad (0 < \beta_0 < 1, \ \beta_0 \ne 1/2).
\]
By the functional equation $\zeta(s) = \chi(s)\zeta(1-s)$ and Schwarz reflection $\zeta(\overline{s}) = \overline{\zeta(s)}$, an off-line zero occurs in a quartet:
\[
\mathcal{Q}(\rho_0) = \left\{ \rho_0, \ \overline{\rho_0}, \ 1 - \rho_0, \ 1 - \overline{\rho_0} \right\}.
\]

### Definition 4.1 (Isolated Off-Line Zero Contribution $A_\varepsilon(\rho_0)$)
Define the contribution of the off-line quartet $\mathcal{Q}(\rho_0)$ in the double spectral sum:
\[
A_\varepsilon(\rho_0) := \sum_{\rho_1 \in \mathcal{Q}(\rho_0)} \sum_{\rho_2 \in \mathcal{Q}(\rho_0)} m_{\rho_1} m_{\rho_2} \tau^{-K \rho_1 - J \rho_2} \widetilde F_\varepsilon(\rho_1, \rho_2).
\]
Then the observable decomposes exactly as:
\[
Q_\varepsilon^{K, J}[w] = A_\varepsilon(\rho_0) + R_\varepsilon,
\]
where the complete remainder $R_\varepsilon$ is defined by:
\[
R_\varepsilon := \mathcal{M}_{1, 1}(\varepsilon) - \mathcal{M}_{1, \rm spec}(\varepsilon) - \mathcal{M}_{\rm spec, 1}(\varepsilon) + \sum_{\substack{(\rho_1, \rho_2) \in Z_{\rm nt}^2 \\ (\rho_1, \rho_2) \notin \mathcal{Q}(\rho_0)^2}} m_{\rho_1} m_{\rho_2} \tau^{-K \rho_1 - J \rho_2} \widetilde F_\varepsilon(\rho_1, \rho_2) + \mathcal{R}_{\rm bg}(\varepsilon).
\]

---

## 5. Separation of Truncation Error from the Bridge Remainder

Let $T \ge 14.0$ be a spectral height cutoff.
Partition the non-target nontrivial zeros into:
- Near/intermediate spectrum: $Z_T = \{ \rho \in Z_{\rm nt} \setminus \mathcal{Q}(\rho_0) : |\Im\rho| \le T \}$,
- Tail spectrum: $Z_{>T} = \{ \rho \in Z_{\rm nt} : |\Im\rho| > T \}$.

The complete remainder $R_\varepsilon$ separates strictly into:
\[
R_\varepsilon = R_{\varepsilon, \le T} + E_{\rm trunc}(\varepsilon, T),
\]
where:

### 1. The Truncated Bridge Remainder $R_{\varepsilon, \le T}$:
\[
R_{\varepsilon, \le T} := \mathcal{M}_{1, 1}(\varepsilon) - \mathcal{M}_{1, \le T}(\varepsilon) - \mathcal{M}_{\le T, 1}(\varepsilon) + \sum_{\substack{\rho_1, \rho_2 \in Z_T \cup \mathcal{Q}(\rho_0) \\ (\rho_1, \rho_2) \notin \mathcal{Q}(\rho_0)^2}} m_{\rho_1} m_{\rho_2} \tau^{-K \rho_1 - J \rho_2} \widetilde F_\varepsilon(\rho_1, \rho_2) + \mathcal{R}_{\rm bg, \le T}(\varepsilon).
\]
This contains all low-frequency spectral interactions, the pole at $s=1$, the background terms, and the cross-terms between $\mathcal{Q}(\rho_0)$ and the on-line zeros below height $T$.

### 2. The Spectral Truncation Error $E_{\rm trunc}(\varepsilon, T)$:
\[
E_{\rm trunc}(\varepsilon, T) := \sum_{\substack{\rho_1 \in Z_{>T} \text{ or } \rho_2 \in Z_{>T}}} m_{\rho_1} m_{\rho_2} \tau^{-K \rho_1 - J \rho_2} \widetilde F_\varepsilon(\rho_1, \rho_2) - \mathcal{M}_{1, >T}(\varepsilon) - \mathcal{M}_{>T, 1}(\varepsilon) + \mathcal{R}_{\rm bg, >T}(\varepsilon).
\]

> [!IMPORTANT]
> **Crucial Distinction**: Bounding $E_{\rm trunc}(\varepsilon, T) \to 0$ as $T \to \infty$ only certifies that the finite sum $R_{\varepsilon, \le T}$ accurately approximates the full remainder $R_\varepsilon$. It does **not** show that $R_{\varepsilon, \le T}$ is small or that its terms cannot cancel $A_\varepsilon(\rho_0)$. The two errors must be governed separately.

---

## 6. Specification of the Joint Limit Bound $B(\varepsilon, T)$

To quantify $E_{\rm trunc}(\varepsilon, T)$, substitute $y = x - \varepsilon u$ in $\widetilde F_\varepsilon(\rho_1, \rho_2)$:
\[
\widetilde F_\varepsilon(\rho_1, \rho_2) = \varepsilon \int_a^b dx \, w(x) x^{\rho_1 - 1} \int_{-1}^1 du \, \eta(u) w(x - \varepsilon u) (x - \varepsilon u)^{\rho_2 - 1}.
\]
Integration by parts $p$ times in $x$ gives:
\[
|\widetilde F_\varepsilon(\rho_1, \rho_2)| \le \frac{1}{|\gamma_1|^p} \int_a^b \left| \partial_x^p \left( w(x) x^{\beta_1 - 1} \int_{-1}^1 \eta(u) w(x - \varepsilon u) (x - \varepsilon u)^{\rho_2 - 1} du \right) \right| dx.
\]
Because $\partial_x$ falls on both $w(x)$ and $w(x - \varepsilon u)$, derivatives of the mollifier $\eta((x-y)/\varepsilon)$ introduce negative powers of $\varepsilon$:
\[
\left\| \partial_x^p F_\varepsilon \right\|_{L^\infty} \le C_p(w) \|\eta\|_{C^p} \, \varepsilon^{-p}.
\]
Consequently, for any $p \ge 3$:
\[
|\widetilde F_\varepsilon(\rho_1, \rho_2)| \le \frac{C_p(w, \eta) \, \varepsilon^{1 - p}}{(1 + |\gamma_1|)^p}.
\]
Applying Trudgian's unconditional zero-counting bound $N(t) \le \frac{t}{2\pi}\log t$ for $t \ge 14.0$:
\[
\sum_{|\gamma| > T} \frac{1}{(1 + |\gamma|)^p} = \int_T^\infty \frac{dN(t)}{t^p} \le \frac{p}{2\pi} \int_T^\infty \frac{\log t}{t^p} dt \le \frac{p}{2\pi(p-1)} \frac{\log T}{T^{p-1}} + \frac{1}{2\pi(p-1)^2 T^{p-1}}.
\]
Summing over the two-variable tail:

### Lemma 6.1 (Joint Truncation Bound $B(\varepsilon, T)$)
For any $p \ge 3$, there exists a constant $C_p > 0$ depending only on $w, \eta, K, J$ such that:
\[
|E_{\rm trunc}(\varepsilon, T)| \le B(\varepsilon, T) := C_p \frac{\varepsilon^{1 - p} \log T}{T^{p-2}}.
\]

### Analysis of the Joint Limit Trajectory $T = T(\varepsilon)$:
- For any **fixed** $\varepsilon > 0$, $\lim_{T \to \infty} B(\varepsilon, T) = 0$.
- However, as $\varepsilon \to 0$, the factor $\varepsilon^{1-p}$ diverges.
- To maintain control of the truncation error ($B(\varepsilon, T(\varepsilon)) \to 0$ as $\varepsilon \to 0$), the spectral cutoff $T(\varepsilon)$ must grow fast enough to beat the singularity:
  \[
  \frac{\log T(\varepsilon)}{T(\varepsilon)^{p-2}} \ll \varepsilon^{p-1} \implies T(\varepsilon) \ge \left( \frac{1}{\varepsilon} \right)^{\frac{p-1}{p-2} + \delta} \quad (\delta > 0).
  \]
  For example, taking $p = 4$ requires $T(\varepsilon) \ge \varepsilon^{-3/2 - \delta}$.

---

## 7. The Core Research Question: Positivity vs. Exact Cancellation

We now investigate the decisive research question:
> **Does the complete prime–zero relationship force a positive off-line contribution that the remaining terms cannot cancel?**
> Specifically: Under the assumption of an actual off-line zero $\rho_0$, can one establish:
> \[
> A_\varepsilon(\rho_0) \ge c D(\rho_0), \qquad |R_\varepsilon| \le r_\varepsilon \to 0,
> \]
> with $c > 0$ independent of every varying cutoff or localization parameter?

### 7.1 Quantitative Asymptotic Scaling of $A_\varepsilon(\rho_0)$
Substitute $y = x - \varepsilon u$ in $\widetilde F_\varepsilon(\rho_1, \rho_2)$:
\[
\widetilde F_\varepsilon(\rho_1, \rho_2) = \varepsilon \int_{-1}^1 \eta(u) du \int_a^b w(x)^2 x^{\rho_1 + \rho_2 - 2} dx + \varepsilon^2 \int_{-1}^1 u \eta(u) du \int_a^b \dots + O(\varepsilon^3).
\]
Since $\eta$ is even, $\int_{-1}^1 u \eta(u) du = 0$.
Let $I_\eta = \int_{-1}^1 \eta(u) du > 0$, and $\widetilde{w^2}(s) = \int_a^b w(x)^2 x^{s-1} dx$.
Then:
\[
\widetilde F_\varepsilon(\rho_1, \rho_2) = \varepsilon I_\eta \, \widetilde{w^2}(\rho_1 + \rho_2 - 1) + O(\varepsilon^3).
\]
Therefore, the isolated zero term evaluates to:
\[
A_\varepsilon(\rho_0) = \varepsilon I_\eta \sum_{\rho_1, \rho_2 \in \mathcal{Q}(\rho_0)} m_{\rho_1} m_{\rho_2} \tau^{-K \rho_1 - J \rho_2} \widetilde{w^2}(\rho_1 + \rho_2 - 1) + O(\varepsilon^3).
\]
Consequently:
\[
\lim_{\varepsilon \to 0} A_\varepsilon(\rho_0) = 0.
\]
$A_\varepsilon(\rho_0)$ vanishes linearly with $\varepsilon$. It **does not** remain bounded below by a fixed non-zero constant $c D(\rho_0) > 0$ as $\varepsilon \to 0$.

### 7.2 The Normalized Observable $\bar Q_\varepsilon := \varepsilon^{-1} Q_\varepsilon$
To investigate whether an $O(1)$ lower bound exists, define the normalized observable:
\[
\bar Q_\varepsilon^{K, J}[w] := \frac{1}{\varepsilon} Q_\varepsilon^{K, J}[w] = \bar A_\varepsilon(\rho_0) + \bar R_\varepsilon,
\]
where:
\[
\bar A_\varepsilon(\rho_0) := \frac{A_\varepsilon(\rho_0)}{\varepsilon} = I_\eta \sum_{\rho_1, \rho_2 \in \mathcal{Q}(\rho_0)} m_{\rho_1} m_{\rho_2} \tau^{-K \rho_1 - J \rho_2} \widetilde{w^2}(\rho_1 + \rho_2 - 1) + O(\varepsilon^2),
\]
\[
\bar R_\varepsilon := \frac{R_\varepsilon}{\varepsilon}.
\]
As $\varepsilon \to 0$, $\bar A_\varepsilon(\rho_0)$ has a well-defined non-zero limit:
\[
\bar A_0(\rho_0) := \lim_{\varepsilon \to 0} \bar A_\varepsilon(\rho_0) = I_\eta \sum_{\rho_1, \rho_2 \in \mathcal{Q}(\rho_0)} m_{\rho_1} m_{\rho_2} \tau^{-K \rho_1 - J \rho_2} \widetilde{w^2}(\rho_1 + \rho_2 - 1).
\]
For conjugate pairs $(\rho_0, \overline{\rho_0})$ with $\rho_0 = \beta_0 + i\gamma_0$:
\[
\rho_0 + \overline{\rho_0} - 1 = 2\beta_0 - 1 = 2(\beta_0 - 1/2) \ne 0.
\]
The grade character factor is:
\[
\tau^{-K\rho_0 - J\overline{\rho_0}} + \tau^{-K\overline{\rho_0} - J\rho_0} = 2 \tau^{-(K+J)\beta_0} \cos\left( (K - J)\gamma_0 \log\tau \right).
\]

### 7.3 The Exact Cancellation Mechanism
Now apply Theorem 2.1 (Arithmetic Contract):
For distinct grades $K \ne J$, Lindemann transcendence guarantees $S_K \cap S_J = \emptyset$, so $d_{\min} > 0$.
For all $0 < \varepsilon < d_{\min}$:
\[
Q_\varepsilon^{K, J}[w] \equiv 0 \implies \bar Q_\varepsilon^{K, J}[w] = \frac{0}{\varepsilon} \equiv 0.
\]
Because the explicit formula identity holds identically for every $\varepsilon > 0$:
\[
\bar Q_\varepsilon^{K, J}[w] = \bar A_\varepsilon(\rho_0) + \bar R_\varepsilon \equiv 0 \quad \text{for all } 0 < \varepsilon < d_{\min}.
\]
Therefore:
\[
\bar R_\varepsilon = -\bar A_\varepsilon(\rho_0) \quad \text{identically for all } 0 < \varepsilon < d_{\min}!
\]
Taking $\varepsilon \to 0$:
\[
\lim_{\varepsilon \to 0} \bar R_\varepsilon = -\bar A_0(\rho_0).
\]

### Mathematical Theorem 7.2 (The Exact Cancellation Identity)
The complete prime–zero explicit formula forces:
\[
\bar R_0 = -\bar A_0(\rho_0).
\]
That is: the sum of the pole terms, the mixed pole-zero terms, the infinite sum over all other nontrivial zeros, and the background terms **identically cancels** the off-line zero contribution $\bar A_0(\rho_0)$ on any fixed compact window for all $\varepsilon < d_{\min}$.

**Research Implication**:
The remainder $\bar R_\varepsilon$ **cannot** be made arbitrarily small independently of $\bar A_\varepsilon(\rho_0)$.
If an off-line zero existed, its contribution $\bar A_0(\rho_0)$ is precisely cancelled by the remaining terms in the complete distribution.
Therefore:
- In the fixed-window framework, an off-line zero does **not** force an uncompensated positive excess.
- The conditional spectral lower bound $Q_\varepsilon \ge c D(\rho_0) - r_\varepsilon$ with $r_\varepsilon \to 0$ **does not hold** on fixed compact windows.
- The bridge classification is: **Arithmetic vanishing proved; conditional spectral lower bound unproved**.

---

## 8. The Three Foundational Findings

### Finding 1: Scope of the Gaussian Escaping Barrier
The Section 7E log-Gaussian test family $\phi_L(x)$ has support $\operatorname{supp}(\phi_L) \subset [e^L, e^{17L}]$. For any fixed window $[a, b]$, $\operatorname{supp}(\phi_L) \cap [a, b] = \emptyset$ for all $L > \log b$.
- This proves that the *specific* family $\phi_L$ escapes every fixed window.
- It does **not** rule out every fixed-window argument. Other families of test functions (e.g., fixed smooth bumps $w \in C_c^\infty((a, b))$) or global two-variable distributions remain eligible for fixed-window analysis.

### Finding 2: Resolution Below the Arithmetic Gap Is Already Possible
Whenever $\Delta_L := \min \{ |x - y| : x \in S_K, y \in S_J \} > 0$, choosing:
\[
0 < \varepsilon_L < \min\left\{ \frac{1}{L}, \ \frac{\Delta_L}{2} \right\}
\]
guarantees $Q_{\varepsilon_L} = 0$ identically.
- Thus, achieving zero overlap on the arithmetic side is already mathematically trivial.
- The true, substantive bottleneck is whether such a resolution $\varepsilon_L$ is compatible with a proved spectral remainder estimate:
  \[
  B(\varepsilon_L, T) \le C_p \frac{\varepsilon_L^{1-p} \log T}{T^{p-2}} < \frac{c D}{2}.
  \]
  As shown in Section 6, shrinking $\varepsilon_L$ forces $T$ to grow at least as $\varepsilon_L^{-(p-1)/(p-2)}$, and even with $T \to \infty$, the remaining non-tail terms $\bar R_{\varepsilon, \le T}$ cancel $\bar A_\varepsilon(\rho_0)$. A Diophantine separation sweep alone cannot bridge this gap.

### Finding 3: Moving Windows Lose the Exact-Coincidence Conclusion
If one attempts to track the escaping Gaussian family by expanding the window $W_L = [e^L, e^{17L}]$:
- On an unbounded or expanding domain, stations $x_n \in S_K(L)$ and $y_n \in S_J(L)$ can satisfy $|x_n - y_n| \to 0$ as $L \to \infty$ without ever coinciding ($x_n \ne y_n$ for all $n$).
- The Lindemann compactness argument (Theorem 2.1, Part 4: pigeonhole extraction of a single pair $(x^*, y^*)$ from a finite set) **fails** on non-compact domains where infinitely many pairs exist.
- Any expanding-window proposal must supply an explicit mathematical replacement for the compactness argument to deduce an exact coincidence $m\tau^K = n\tau^J$.

---

## 9. Epistemic Classification & Lean 4 Formalization

The formalization in `formal/RiemannScope/Grade.lean` establishes:
```lean
theorem candidate_bridge_positivity_contradiction (Q c D : ℝ)
    (hQ_nonpos : Q ≤ 0)
    (h_lower : c * D ≤ Q)
    (hc : c > 0)
    (hD : D > 0) : False := by
  have h_pos : c * D > 0 := mul_pos hc hD
  linarith
```
- **What this lemma proves**: It formalizes the contradiction endpoint of the *reductio ad absurdum*:
  If an argument were to establish $Q \le 0$ (arithmetic vanishing) and independently derive $Q \ge c D > 0$ (conditional spectral lower bound), then `False` would result, excluding the hypothesis.
- **What this lemma does NOT prove**: It does not supply the missing spectral lower bound $Q \ge c D - r_\varepsilon$, nor does it estimate the remainder $R_\varepsilon$.

### Final Classification
- **Arithmetic Side**: **PROVED** (Theorem 2.1: $Q_\varepsilon \equiv 0$ for $\varepsilon < d_{\min}$).
- **Contradiction Endpoint**: **FORMALLY PROVED** in Lean 4 (`candidate_bridge_positivity_contradiction`).
- **Conditional Spectral Lower Bound**: **UNPROVED / STRICTLY OPEN** (Section 7: complete explicit formula forces exact cancellation $\bar R_0 = -\bar A_0(\rho_0)$).
- **Transcendental Continuation Bridge**: **STRICTLY OPEN**.
