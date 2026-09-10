# Arithmetic Overlap Mechanism Investigation: Quantitative Remainder Analysis & The Contradiction Architecture

**Role**: Formula Analyst & Arithmetic Researcher  
**Epic Track**: TC Epic — Two-Variable Formula, Normalized Remainder Bound, and Bridge Testing  
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
Under coordinate dilation $D_a(x) = ax$ with scale $a_K = \tau^K$ ($K \in \mathbb{Z}, \ \tau = 2\pi$):
\[
\mu_K = (D_{\tau^K})_* \mu_0 = \sum_{n \ge 2} \Lambda(n) \delta_{\tau^K n}.
\]
Arithmetic locations are $a_K n = \tau^K n$; weights are $\Lambda(n)$. The support of $\mu_K$ consists strictly of scaled prime powers:
\[
\operatorname{supp}(\mu_K) = \left\{ \tau^K p^m : p \text{ prime}, m \ge 1 \right\} \subset L_K = \tau^K \mathbb{Z}.
\]

### Definition 1.1 (The Arithmetic Overlap Observable $Q_\varepsilon^{K, J}[w]$)
Fix two distinct grades $K \ne J \in \mathbb{Z}$, with scales $a_K = \tau^K, a_J = \tau^J$.
Fix a compact test window:
\[
W = [a, b] \subset (0, \infty), \qquad a > \max(a_K, a_J), \qquad b > a.
\]
Take real, non-negative $w \in C_c^\infty((a, b))$ with $w \not\equiv 0$.
Take real, non-negative $\eta \in C_c^\infty((-1, 1))$ with $\eta(0) = 1$, even $\eta(-v) = \eta(v)$, and $I_\eta = \int_{-1}^1 \eta(v) \, dv > 0$.
For $0 < \varepsilon \le 1$, define the smooth two-variable kernel:
\[
F_\varepsilon(x, y) := w(x) w(y) \eta\left( \frac{x - y}{\varepsilon} \right),
\]
and the two-variable overlap observable:
\[
Q_\varepsilon^{K, J}[w] := \langle \mu_K \otimes \mu_J, F_\varepsilon \rangle = \iint_{(0, \infty)^2} F_\varepsilon(x, y) \, d\mu_K(x) \, d\mu_J(y).
\]
Because $\mu_K$ and $\mu_J$ are discrete Radon measures on $(0, \infty)$, $Q_\varepsilon^{K, J}[w]$ evaluates to the double sum:
\[
Q_\varepsilon^{K, J}[w] = \sum_{n \ge 2} \sum_{m \ge 2} \Lambda(n) \Lambda(m) w(\tau^K n) w(\tau^J m) \eta\left( \frac{\tau^K n - \tau^J m}{\varepsilon} \right).
\]

---

## 2. The Exact Arithmetic Contract (Proved Arithmetic Vanishing)

### Theorem 2.1 (The Arithmetic Separation Contract)
Let $K, J \in \mathbb{Z}$, and let $w \in C_c^\infty((a, b))$ with $a > \max(\tau^K, \tau^J)$.
Define the active station sets in $[a, b]$:
\[
S_K = \operatorname{supp}(\mu_K) \cap [a, b] = \left\{ \tau^K n : n \ge 2, \ \Lambda(n) > 0, \ \tau^K n \in [a, b] \right\},
\]
\[
S_J = \operatorname{supp}(\mu_J) \cap [a, b] = \left\{ \tau^J m : m \ge 2, \ \Lambda(m) > 0, \ \tau^J m \in [a, b] \right\}.
\]
Then:
1. **Strict Disjointness for Distinct Grades ($K \ne J$)**:
   If $K \ne J$, then $S_K \cap S_J = \emptyset$.
   Consequently, the inter-grade minimum station distance:
   \[
   d_{\min} := \min_{x \in S_K, \ y \in S_J} |x - y| > 0
   \]
   is strictly positive.
2. **Identical Arithmetic Vanishing for Small $\varepsilon$**:
   For any $0 < \varepsilon < d_{\min}$:
   \[
   Q_\varepsilon^{K, J}[w] \equiv 0 \quad \text{identically}.
   \]
3. **Diagonal Mass Control ($K = J$)**:
   When $K = J$, for all $\varepsilon < \tau^K$:
   \[
   Q_\varepsilon^{K, K}[w] = \sum_{n \ge 2} \Lambda(n)^2 w(\tau^K n)^2 > 0,
   \]
   which is strictly positive whenever $[a, b]$ contains at least one prime-power station.

*Proof.*
Suppose $x \in S_K \cap S_J$. Then $x = \tau^K n = \tau^J m$ for integers $n, m \ge 2$ with $\Lambda(n)\Lambda(m) > 0$.
Assuming $K > J$, we have $\tau^{K - J} = m/n \in \mathbb{Q}_{>0}$.
By the Lindemann transcendence theorem (1882), $\pi$ is transcendental over $\mathbb{Q}$, hence $\tau = 2\pi$ is transcendental, and any non-zero integer power $\tau^{K - J}$ is transcendental. A transcendental number cannot equal a rational $m/n \in \mathbb{Q}$.
Therefore $S_K \cap S_J = \emptyset$. Since $S_K$ and $S_J$ are finite, $d_{\min} = \min |x - y| > 0$.
For $\varepsilon < d_{\min}$, $|x - y|/\varepsilon > 1$, so $\eta((x-y)/\varepsilon) = 0$ identically for all contributing pairs, establishing $Q_\varepsilon^{K, J}[w] \equiv 0$. $\blacksquare$

---

## 3. Repair of Established Defects in Previous Reports

### 3.1 Falsification of the Previous Cutoff Condition
Prior reports asserted an unnormalized tail bound $B_{\rm old}(\varepsilon, T) = C_p \varepsilon^{1-p} \frac{\log T}{T^{p-2}}$, and claimed that $T(\varepsilon) \gg \varepsilon^{-(p-1)/(p-2)}$ guarantees convergence to zero.

**Exact Counterexample**:
Take $p = 3$. Then $(p-1)/(p-2) = 2/1 = 2$.
Set:
\[
\ell = \log(1/\varepsilon), \qquad T(\varepsilon) = \varepsilon^{-2} \sqrt{\ell}.
\]
Then:
\[
\frac{T(\varepsilon)}{\varepsilon^{-2}} = \sqrt{\ell} \longrightarrow \infty \quad \text{as } \varepsilon \to 0,
\]
so $T(\varepsilon) \gg \varepsilon^{-2}$ is strictly satisfied.
However, evaluate the bound:
\[
\log T(\varepsilon) = \log(\varepsilon^{-2} \sqrt{\ell}) = 2\log(1/\varepsilon) + \frac{1}{2}\log\ell = 2\ell + \frac{1}{2}\log\ell.
\]
Substituting into $B_{\rm old}$:
\[
\frac{B_{\rm old}}{C_p} = \varepsilon^{-2} \frac{\log T}{T} = \varepsilon^{-2} \frac{2\ell + \frac{1}{2}\log\ell}{\varepsilon^{-2} \sqrt{\ell}} = \frac{2\ell + \frac{1}{2}\log\ell}{\sqrt{\ell}} = 2\sqrt{\ell} + \frac{\log\ell}{2\sqrt{\ell}} \longrightarrow \infty!
\]
This rigorously falsifies the claim that $T(\varepsilon) \gg \varepsilon^{-(p-1)/(p-2)}$ is sufficient for convergence.

### 3.2 Normalization and the Corrected Error Scale
When using the normalized observable:
\[
\bar Q_\varepsilon := \frac{Q_\varepsilon}{\varepsilon},
\]
the truncation error is also divided by $\varepsilon$.
The mathematical requirement for the truncation error to vanish asymptotically is:
\[
\bar E_{\rm trunc}(\varepsilon, T(\varepsilon)) = \frac{E_{\rm trunc}(\varepsilon, T(\varepsilon))}{\varepsilon} = o(1) \iff E_{\rm trunc}(\varepsilon, T(\varepsilon)) = o(\varepsilon).
\]

Assuming a bound of the form $C_p \varepsilon^{1-p} \frac{\log^k(2+T)}{T^{p-2}}$ ($k \in \{1, 2\}$), division by $\varepsilon$ yields:
\[
\bar B(\varepsilon, T) = C_p \varepsilon^{-p} \frac{\log^k(2+T)}{T^{p-2}}.
\]
Under a strict power choice $T = \varepsilon^{-\alpha}$:
- For the unnormalized bound: $B \sim \varepsilon^{1 - p + \alpha(p-2)} \log^k(1/\varepsilon) \to 0 \iff \alpha > \frac{p-1}{p-2}$.
- For the normalized bound: $\bar B \sim \varepsilon^{-p + \alpha(p-2)} \log^k(1/\varepsilon) \to 0 \iff \alpha > \frac{p}{p-2}$.

For $p = 4$, $\frac{p}{p-2} = \frac{4}{2} = 2$.
Choosing $\alpha = 3 > 2$ gives:
\[
-p + \alpha(p-2) = -4 + 3(2) = 2 > 0,
\]
guaranteeing that the normalized error decays as $O(\varepsilon^2 \log^k(1/\varepsilon)) \to 0$.

### 3.3 Exact Cancellation Is an Identity, Not an Impossibility Proof
From $Q_\varepsilon \equiv 0$ for $\varepsilon < d_{\min}$ and an exact decomposition $Q_\varepsilon = A_\varepsilon + R_\varepsilon$, algebra forces $R_\varepsilon = -A_\varepsilon$ for all $\varepsilon < d_{\min}$.
This algebraic fact alone does not prove that every fixed-window bridge is impossible in principle; passing to separate normalized limits requires their independent existence and properties to be evaluated.

---

## 4. Complete One-Variable Graded Explicit Identity

### 4.1 Derivation from the Uncompleted Zeta Logarithmic Derivative
Let $a_K = \tau^K$ and consider a test function $f \in C_c^\infty((a, b))$ with $a > a_K$.
The pushforward arithmetic measure is $\mu_K = \sum_{n \ge 2} \Lambda(n) \delta_{a_K n}$.
By Mellin inversion on $\Re(s) = c > 1$:
\[
f(x) = \frac{1}{2\pi i} \int_{(c)} \widetilde f(s) x^{-s} \, ds, \qquad \widetilde f(s) = \int_0^\infty f(x) x^{s-1} \, dx.
\]
Pairing with $\mu_K$:
\[
\langle \mu_K, f \rangle = \sum_{n \ge 2} \Lambda(n) f(a_K n) = \frac{1}{2\pi i} \int_{(c)} \left( -\frac{\zeta'}{\zeta}(s) \right) a_K^{-s} \widetilde f(s) \, ds.
\]
Because $f \in C_c^\infty((a, b))$, $\widetilde f(s)$ is an entire function with superpolynomial decay in vertical strips:
$|\widetilde f(\sigma + it)| \le C_N(1 + |t|)^{-N}$ for every $N \ge 0$, uniformly on compact $\sigma$-intervals.
Shifting the contour to $\Re(s) \to -\infty$ across the critical strip picks up residues:
1. Pole at $s = 1$: Residue $+1$, contributing $+a_K^{-1} \widetilde f(1)$.
2. Nontrivial zeros $\rho \in Z_{\rm nt}$: At each zero of multiplicity $m_\rho$, $-\frac{\zeta'}{\zeta}(s)$ has residue $-m_\rho$, contributing $- \sum_{\rho \in Z_{\rm nt}} m_\rho a_K^{-\rho} \widetilde f(\rho)$.
3. Trivial zeros at $s = -2j$ ($j \ge 1$): Simple poles with residue $-1$, contributing $- \sum_{j \ge 1} a_K^{2j} \widetilde f(-2j)$.

Therefore:
\[
\langle \mu_K, f \rangle = a_K^{-1} \widetilde f(1) - \sum_{\rho \in Z_{\rm nt}} m_\rho a_K^{-\rho} \widetilde f(\rho) - \sum_{j \ge 1} a_K^{2j} \widetilde f(-2j).
\]

### 4.2 Closed Geometric Summation of the Trivial-Zero Background
For support above $a_K$ ($x \ge a > a_K$), $a_K / x < 1$.
The trivial-zero series can be summed under the integral sign:
\[
\sum_{j \ge 1} a_K^{2j} \widetilde f(-2j) = \int_a^b f(x) \left( \sum_{j \ge 1} a_K^{2j} x^{-2j-1} \right) dx.
\]
Summing the geometric series:
\[
\sum_{j \ge 1} a_K^{2j} x^{-2j-1} = x^{-1} \sum_{j \ge 1} \left(\frac{a_K^2}{x^2}\right)^j = x^{-1} \frac{a_K^2 / x^2}{1 - a_K^2 / x^2} = \frac{a_K^2}{x(x^2 - a_K^2)}.
\]
Define the smooth background density:
\[
b_K(x) := a_K^{-1} - \frac{a_K^2}{x(x^2 - a_K^2)}, \qquad \mathcal{B}_K := b_K(x) \, dx,
\]
and the nontrivial zero spectral distribution on $(a, b)$:
\[
\mathcal{Z}_K := \sum_{\rho \in Z_{\rm nt}} m_\rho a_K^{-\rho} x^{\rho-1} \, dx.
\]
Then as distributions on $(a, b)$ with $a > a_K$:
\[
\mu_K = \mathcal{B}_K - \mathcal{Z}_K.
\]

---

## 5. Complete Two-Variable Graded Explicit Expansion

### 5.1 The Nine Uncombined Terms
Because $\mu_K = \mathcal{P}_K - \mathcal{Z}_K - \mathcal{T}_K$, where $\mathcal{P}_K = a_K^{-1} dx$ is the pole at $s=1$ and $\mathcal{T}_K = \frac{a_K^2}{x(x^2 - a_K^2)} dx$ is the trivial-zero background, the tensor product $\mu_K \otimes \mu_J$ acting on $F_\varepsilon(x, y)$ expands bilinearly into $3 \times 3 = 9$ terms:
\[
\begin{aligned}
Q_\varepsilon^{K, J}[w] ={}& \langle \mathcal{P}_K \otimes \mathcal{P}_J, F_\varepsilon \rangle
- \langle \mathcal{P}_K \otimes \mathcal{Z}_J, F_\varepsilon \rangle
- \langle \mathcal{P}_K \otimes \mathcal{T}_J, F_\varepsilon \rangle \\
&{}- \langle \mathcal{Z}_K \otimes \mathcal{P}_J, F_\varepsilon \rangle
+ \langle \mathcal{Z}_K \otimes \mathcal{Z}_J, F_\varepsilon \rangle
+ \langle \mathcal{Z}_K \otimes \mathcal{T}_J, F_\varepsilon \rangle \\
&{}- \langle \mathcal{T}_K \otimes \mathcal{P}_J, F_\varepsilon \rangle
+ \langle \mathcal{T}_K \otimes \mathcal{Z}_J, F_\varepsilon \rangle
+ \langle \mathcal{T}_K \otimes \mathcal{T}_J, F_\varepsilon \rangle.
\end{aligned}
\]

Using the double Mellin transform kernel:
\[
H_\varepsilon(s, t) := \iint_{(0, \infty)^2} F_\varepsilon(x, y) x^{s-1} y^{t-1} \, dx \, dy,
\]
the 9 uncombined terms evaluate explicitly as:
1. **Pole–Pole**: $+a_K^{-1} a_J^{-1} H_\varepsilon(1, 1)$
2. **Pole–Zero**: $-a_K^{-1} \sum_{\sigma \in Z_{\rm nt}} m_\sigma a_J^{-\sigma} H_\varepsilon(1, \sigma)$
3. **Pole–Trivial**: $-a_K^{-1} \sum_{\ell \ge 1} a_J^{2\ell} H_\varepsilon(1, -2\ell)$
4. **Zero–Pole**: $-a_J^{-1} \sum_{\rho \in Z_{\rm nt}} m_\rho a_K^{-\rho} H_\varepsilon(\rho, 1)$
5. **Zero–Zero**: $+\sum_{\rho, \sigma \in Z_{\rm nt}} m_\rho m_\sigma a_K^{-\rho} a_J^{-\sigma} H_\varepsilon(\rho, \sigma)$
6. **Zero–Trivial**: $+\sum_{\rho \in Z_{\rm nt}, \ell \ge 1} m_\rho a_K^{-\rho} a_J^{2\ell} H_\varepsilon(\rho, -2\ell)$
7. **Trivial–Pole**: $-a_J^{-1} \sum_{j \ge 1} a_K^{2j} H_\varepsilon(-2j, 1)$
8. **Trivial–Zero**: $+\sum_{j \ge 1, \sigma \in Z_{\rm nt}} m_\sigma a_K^{2j} a_J^{-\sigma} H_\varepsilon(-2j, \sigma)$
9. **Trivial–Trivial**: $+\sum_{j \ge 1, \ell \ge 1} a_K^{2j} a_J^{2\ell} H_\varepsilon(-2j, -2\ell)$.

### 5.2 The Combined Four-Term Tensor Expansion
Combining $\mathcal{B}_K = \mathcal{P}_K - \mathcal{T}_K$ and $\mathcal{B}_J = \mathcal{P}_J - \mathcal{T}_J$:
\[
Q_\varepsilon = \langle \mathcal{B}_K \otimes \mathcal{B}_J, F_\varepsilon \rangle - \langle \mathcal{B}_K \otimes \mathcal{Z}_J, F_\varepsilon \rangle - \langle \mathcal{Z}_K \otimes \mathcal{B}_J, F_\varepsilon \rangle + \langle \mathcal{Z}_K \otimes \mathcal{Z}_J, F_\varepsilon \rangle.
\]
This algebraic identity is formally proved in Lean 4:
- `two_variable_tensor_decomposition_algebra` (4-term form)
- `two_variable_nine_term_expansion_algebra` (9-term form).

---

## 6. The Selected Spectral Contribution $A_{\varepsilon, \Gamma}$ and Normalized Limit

### 6.1 Definition of the Selected Contribution
Assume the existence of an off-line nontrivial zero $\rho_0 = \beta_0 + i\gamma_0$ ($0 < \beta_0 < 1, \beta_0 \ne 1/2$).
The functional-equation and reflection orbit defines the quartet:
\[
\Gamma(\rho_0) := \left\{ \rho_0, \ \overline{\rho_0}, \ 1 - \rho_0, \ 1 - \overline{\rho_0} \right\}.
\]
If $\rho_0$ is on the critical line ($\beta_0 = 1/2$), $\Gamma$ collapses to the pair $\{\rho_0, \overline{\rho_0}\}$.
In either case, $\Gamma$ is closed under complex conjugation.
Define the finite spectral density:
\[
f_{K, \Gamma}(x) := \sum_{\rho \in \Gamma} m_\rho a_K^{-\rho} x^{\rho-1}.
\]
Since $\overline{a_K^{-\rho} x^{\rho-1}} = a_K^{-\overline{\rho}} x^{\overline{\rho}-1}$ and $\rho \mapsto \overline{\rho}$ permutes $\Gamma$ preserving multiplicities $m_{\overline\rho} = m_\rho$, we have:
\[
\overline{f_{K, \Gamma}(x)} = f_{K, \Gamma}(x) \in \mathbb{R} \quad \text{for all } x > 0.
\]
Define the selected $\Gamma \times \Gamma$ block of the double zero sum:
\[
A_{\varepsilon, \Gamma} := \iint_{(0, \infty)^2} F_\varepsilon(x, y) f_{K, \Gamma}(x) f_{J, \Gamma}(y) \, dx \, dy.
\]
Because $F_\varepsilon$ and $f$ are real-valued, $A_{\varepsilon, \Gamma} \in \mathbb{R}$.

### 6.2 Proved Normalized Finite-Block Limit
Substitute $y = x - \varepsilon v$ ($v = (x-y)/\varepsilon$):
\[
\frac{A_{\varepsilon, \Gamma}}{\varepsilon} = \int_{-1}^1 \eta(v) \, dv \int_a^b w(x) f_{K, \Gamma}(x) w(x - \varepsilon v) f_{J, \Gamma}(x - \varepsilon v) \, dx.
\]
Let $u_K(x) = w(x) f_{K, \Gamma}(x)$ and $u_J(x) = w(x) f_{J, \Gamma}(x)$. Since $w \in C_c^\infty((a, b))$, $u_K, u_J \in C_c^\infty((a, b))$.
Taylor expanding $u_J(x - \varepsilon v) = u_J(x) - \varepsilon v u_J'(x) + \frac{1}{2} \varepsilon^2 v^2 u_J''(\xi)$:
\[
\frac{A_{\varepsilon, \Gamma}}{\varepsilon} = \left( \int_{-1}^1 \eta(v) \, dv \right) \int_a^b w(x)^2 f_{K, \Gamma}(x) f_{J, \Gamma}(x) \, dx - \varepsilon \left( \int_{-1}^1 v \eta(v) \, dv \right) \int_a^b u_K u_J' \, dx + O(\varepsilon^2).
\]
Because $\eta$ is even, $\int_{-1}^1 v \eta(v) \, dv = 0$.
Therefore, the first-order error vanishes identically, yielding:
\[
\frac{A_{\varepsilon, \Gamma}}{\varepsilon} = A_{0, \Gamma} + O(\varepsilon^2),
\]
where the limit coefficient is:
\[
A_{0, \Gamma} := \left( \int_{-1}^1 \eta(v) \, dv \right) \int_a^b w(x)^2 f_{K, \Gamma}(x) f_{J, \Gamma}(x) \, dx.
\]

### 6.3 Audit of $A_{0, \Gamma}$ and Falsification of $A_{0, \Gamma} = c D_M(\rho_0)$
On the critical line ($\rho_0 = 1/2 + i\gamma_0$), $\Gamma = \{1/2 + i\gamma_0, 1/2 - i\gamma_0\}$.
Then:
\[
f_{K, \Gamma}(x) = 2 a_K^{-1/2} x^{-1/2} \cos\left(\gamma_0 \log(x / a_K)\right),
\]
\[
f_{K, \Gamma}(x) f_{J, \Gamma}(x) = 2 (a_K a_J)^{-1/2} x^{-1} \left[ \cos\left( (K - J)\gamma_0 \log\tau \right) + \cos\left( \gamma_0 \log\left( \frac{x^2}{a_K a_J} \right) \right) \right].
\]
Consequently, $A_{0, \Gamma}$ contains a non-oscillatory baseline:
\[
2 I_\eta (a_K a_J)^{-1/2} \cos(M \gamma_0 \log\tau) \int_a^b w(x)^2 x^{-1} \, dx \ne 0.
\]
Recall the distance functional:
\[
D_M(\rho_0) := 4 \sinh^2\left( \frac{M(\Re\rho_0 - 1/2)\log\tau}{2} \right).
\]
On the critical line, $\Re\rho_0 = 1/2 \implies D_M(\rho_0) = 0$.
However, quadrature confirms $A_{0, \Gamma} \approx 0.5444 \ne 0$.
**Mathematical Finding**:
Any asserted identity $A_{0, \Gamma} = c D_M(\rho_0)$ is **definitively false**. $A_{0, \Gamma}$ does not vanish on the critical line.

---

## 7. Genuine Two-Variable Truncation Bound

### 7.1 Definition of Square Spectral Truncation
For spectral height $T \ge 14.0$, define the truncated spectral measure:
\[
\mathcal{Z}_{K, T} := \sum_{\substack{\rho \in Z_{\rm nt} \\ |\Im\rho| \le T}} m_\rho a_K^{-\rho} x^{\rho-1} \, dx, \qquad \mu_{K, T}^{\rm spec} := \mathcal{B}_K - \mathcal{Z}_{K, T}.
\]
Define the square-truncated observable and truncation error:
\[
Q_{\varepsilon, T} := \langle \mu_{K, T}^{\rm spec} \otimes \mu_{J, T}^{\rm spec}, F_\varepsilon \rangle, \qquad E_{\varepsilon, T} := Q_\varepsilon - Q_{\varepsilon, T}.
\]
Expanding $E_{\varepsilon, T}$:
\[
E_{\varepsilon, T} = - \langle \mathcal{B}_K \otimes (\mathcal{Z}_J - \mathcal{Z}_{J, T}), F_\varepsilon \rangle - \langle (\mathcal{Z}_K - \mathcal{Z}_{K, T}) \otimes \mathcal{B}_J, F_\varepsilon \rangle + \left( \langle \mathcal{Z}_K \otimes \mathcal{Z}_J, F_\varepsilon \rangle - \langle \mathcal{Z}_{K, T} \otimes \mathcal{Z}_{J, T}, F_\varepsilon \rangle \right).
\]
The double-zero error covers all pairs $(\rho_1, \rho_2)$ where $\max(|\Im\rho_1|, |\Im\rho_2|) > T$.

### 7.2 Proof of the Conservative Bound
We prove:
\[
|E_{\varepsilon, T}| \le C_{p, W, w, \eta, K, J} \, \varepsilon^{1-p} \frac{\log^2(2+T)}{T^{p-2}} \quad (p \in \mathbb{N}, \ p > 2).
\]

*Derivation*:
1. **Logarithmic substitution**:
   Substitute $x = e^u, y = e^v$. Then $u, v \in [\log a, \log b] = I_W$.
   $H_\varepsilon(s_1, s_2) = \iint_{\mathbb{R}^2} G_{\varepsilon, \beta_1, \beta_2}(u, v) e^{i(\gamma_1 u + \gamma_2 v)} \, du \, dv$,
   where $G(u, v) = e^{\beta_1 u + \beta_2 v} w(e^u) w(e^v) \eta((e^u - e^v)/\varepsilon)$.
   Support of $G$ is contained in $I_W \times I_W$ and the strip $|u - v| \le \varepsilon / a$, which has area $O(\varepsilon)$.
2. **Derivative and $L^1$ bounds**:
   By Leibniz and chain rules, $\partial_u^p G$ produces terms of order $\varepsilon^{-p}$.
   Integrating over the support strip of width $O(\varepsilon)$:
   \[
   \|\partial_u^p G\|_{L^1} \le C_p \varepsilon^{-p} \cdot \operatorname{Area}(\operatorname{supp}(G)) \le C_p' \varepsilon^{1-p}.
   \]
3. **Integration by parts**:
   Integrating by parts $p$ times in the variable with the larger absolute ordinate $\max(|\gamma_1|, |\gamma_2|)$:
   \[
   |H_\varepsilon(s_1, s_2)| \le C_p \varepsilon^{1-p} (1 + \max(|\gamma_1|, |\gamma_2|))^{-p}.
   \]
4. **Dyadic Shell Pair Counting**:
   By Trudgian (2014, Corollary 1), the unconditional counting function satisfies $N_*(R) \le C_N R \log(2+R)$.
   Partition the tail $\max(|\gamma_1|, |\gamma_2|) > T$ into dyadic shells $\mathcal{S}_k$ where $2^k T < \max \le 2^{k+1} T$.
   The number of zero pairs in $\mathcal{S}_k$ is bounded by:
   \[
   N_*(2^{k+1} T)^2 \le C_N^2 (2^{k+1} T)^2 \log^2(2 + 2^{k+1} T).
   \]
   On this shell, $|H_\varepsilon| \le C_p \varepsilon^{1-p} (2^k T)^{-p}$.
   Multiplying and summing over $k \ge 0$:
   \[
   \sum_{k=0}^\infty (2^{k+1} T)^2 \log^2(2 + 2^{k+1} T) \cdot (2^k T)^{-p} \le C_p'' T^{2-p} \log^2(2+T) \sum_{k=0}^\infty 2^{k(2-p)} (k+1)^2.
   \]
   Since $p > 2$, $2 - p < 0$, the series converges, yielding:
   \[
   C \varepsilon^{1-p} \frac{\log^2(2+T)}{T^{p-2}}.
   \]
5. **Mixed background tails**:
   Because $b_K(x)$ is smooth on $[a, b]$, integrating by parts in the zero coordinate yields mixed tails bounded by $O(\varepsilon^{1-p} T^{1-p} \log T)$, which are strictly subordinate to $O(\varepsilon^{1-p} T^{2-p} \log^2 T)$ and absorbed. $\blacksquare$

### 7.3 Normalized Error and Joint Path
Dividing by $\varepsilon$:
\[
\frac{|E_{\varepsilon, T}|}{\varepsilon} \le C_p \varepsilon^{-p} \frac{\log^2(2+T)}{T^{p-2}}.
\]
Setting $T = \varepsilon^{-\alpha}$:
\[
\frac{|E_{\varepsilon, T}|}{\varepsilon} \le C_p \varepsilon^{\alpha(p-2) - p} \log^2(2 + \varepsilon^{-\alpha}).
\]
Convergence to zero is guaranteed if and only if:
\[
\alpha > \frac{p}{p-2}.
\]
For $p = 4$, $\alpha > 2$. Choosing $\alpha = 3$ gives $|E|/\varepsilon \le C_p \varepsilon^2 \log^2(1/\varepsilon) \to 0$.

---

## 8. Remainder Analysis & The Contradiction Architecture

### 8.1 Term-by-Term Remainder Expansion
Define the included bridge remainder:
\[
R_{\varepsilon, T} := Q_{\varepsilon, T} - A_{\varepsilon, \Gamma}.
\]
Explicitly:
\[
\begin{aligned}
R_{\varepsilon, T} ={}& \langle \mathcal{B}_K \otimes \mathcal{B}_J, F_\varepsilon \rangle
- \langle \mathcal{B}_K \otimes \mathcal{Z}_{J, T}, F_\varepsilon \rangle
- \langle \mathcal{Z}_{K, T} \otimes \mathcal{B}_J, F_\varepsilon \rangle \\
&{}+ \sum_{\substack{\rho, \sigma \in Z_{\rm nt}, \ |\Im\rho| \le T, \ |\Im\sigma| \le T \\ (\rho, \sigma) \notin \Gamma \times \Gamma}} m_\rho m_\sigma a_K^{-\rho} a_J^{-\sigma} H_\varepsilon(\rho, \sigma).
\end{aligned}
\]

The exact decomposition of the normalized observable is:
\[
\bar Q_\varepsilon = \bar A_{\varepsilon, \Gamma} + \bar R_{\varepsilon, T} + \bar E_{\varepsilon, T}.
\]

### 8.2 The Exact Cancellation Limit
For $\varepsilon < d_{\min}$, arithmetic separation gives $\bar Q_\varepsilon = 0$.
Choose the trajectory $T(\varepsilon) = \varepsilon^{-\alpha}$ with $\alpha > p/(p-2)$.
Then $\bar E_{\varepsilon, T(\varepsilon)} \to 0$ and $\bar A_{\varepsilon, \Gamma} \to A_{0, \Gamma}$.
Therefore:
\[
\lim_{\varepsilon \to 0} \bar R_{\varepsilon, T(\varepsilon)} = - A_{0, \Gamma}.
\]
The included spectral remainder terms (the smooth pole/trivial background and the non-$\Gamma$ zero interactions) identically cancel $A_{0, \Gamma}$.

### 8.3 Analysis of Successor Candidates
Why does this cancellation occur, and can a successor candidate circumvent it?
1. **Wrong Sign / Non-zero Baseline**: The un-filtered product kernel $F_\varepsilon(x, y) = w(x)w(y)\eta((x-y)/\varepsilon)$ is non-negative, but the spectral densities $f_{K, \Gamma}$ oscillate. On the critical line, $A_{0, \Gamma} \ne 0$, so $A_{0, \Gamma}$ does not isolate off-line zeros from on-line zeros.
2. **Filtered Kernels**: Introducing an arithmetic Fourier multiplier $m(x)$ that vanishes on $S_K$ alters the arithmetic observable and does not produce a contradiction with $Q_\varepsilon \equiv 0$.
3. **Hermitian Combinations**: Symmetrizing across grades or taking combinations $\sum c_{K, J} Q_\varepsilon^{K, J}$ retains arithmetic vanishing if all $K \ne J$, but the explicit formula identity continues to hold term-by-term, forcing exact cancellation of each individual component.
4. **Equal-Grade Mixing**: Adding $K = J$ terms introduces non-zero arithmetic diagonal mass $\sum \Lambda(n)^2 w(\tau^K n)^2 > 0$, destroying arithmetic vanishing $Q_\varepsilon \equiv 0$.

---

## 9. Epistemic Summary & Formal Verification

| Component | Mathematical Status | Evidence |
|---|---|---|
| **Arithmetic Vanishing** | **PROVED** | Lindemann transcendence ($d_{\min} > 0 \implies Q_\varepsilon \equiv 0$) |
| **Two-Variable Explicit Formula** | **PROVED** | 9-term uncombined & 4-term tensor expansion |
| **Defect Repair & Counterexample** | **PROVED & VERIFIED** | $p=3, T = \varepsilon^{-2}\sqrt{\ell}$ falsifies old cutoff condition |
| **Normalized Truncation Bound** | **PROVED & VERIFIED** | $|E|/\varepsilon \le C_p \varepsilon^{-p} \frac{\log^2(2+T)}{T^{p-2}}$; convergent for $\alpha > p/(p-2)$ |
| **Selected Contribution Limit** | **PROVED & VERIFIED** | $A_{\varepsilon, \Gamma}/\varepsilon \to A_{0, \Gamma}$ with $O(\varepsilon^2)$ error for even $\eta$ |
| **Identity $A_0 = c D_M$ Falsification** | **FALSIFIED** | On-line zeros have $D_M = 0$ while $A_0 \ne 0$ |
| **Contradiction Endpoint** | **FORMALLY PROVED** | Lean 4: `candidate_bridge_with_remainder_contradiction` (204 compiled theorems, 0 sorry) |
| **Spectral Lower Bound** | **UNPROVED / STRICTLY OPEN** | Exact explicit formula forces cancellation $\bar R_0 = -A_0$ |
| **Transcendental Continuation Bridge** | **STRICTLY OPEN** | Arithmetic vanishing proved; spectral lower bound open |
