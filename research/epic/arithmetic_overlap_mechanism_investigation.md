# Arithmetic Overlap Mechanism Investigation & Exact Arithmetic Contract

**Role**: Arithmetic Researcher  
**Epic Track**: Section 8 & Arithmetic Overlap Observable Investigation  
**Primary Question**: Does compatibility of the complete arithmetic and analytic descriptions across separated grades $K \ne J$ force persistent overlap of arithmetic measures in a fixed compact window?

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

### Definition 1.1 (The Arithmetic Overlap Observable $Q_\varepsilon^{K, J}[w]$).
Fix two distinct grades $K \ne J \in \mathbb{Z}$.
Fix a non-negative, non-zero test window $w \in C_c^\infty((0, \infty))$ with compact support:
\[
\operatorname{supp}(w) \subset [a, b] \subset (0, \infty) \quad (0 < a < b < \infty).
\]
Fix a non-negative mollifier $\eta \in C_c^\infty((-1, 1))$ with $\eta(0) = 1$ and $0 \le \eta(u) \le 1$.
For $\varepsilon > 0$, define the overlap observable:
\[
Q_\varepsilon^{K, J}[w] := \iint_{(0, \infty)^2} w(x) w(y) \eta\left( \frac{x - y}{\varepsilon} \right) d\mu_K(x) d\mu_J(y).
\]
Because $\mu_K$ and $\mu_J$ are discrete Radon measures on $(0, \infty)$, $Q_\varepsilon^{K, J}[w]$ can be written as the double sum:
\[
Q_\varepsilon^{K, J}[w] = \sum_{n \ge 2} \sum_{m \ge 2} \Lambda(n) \Lambda(m) w(\tau^K n) w(\tau^J m) \eta\left( \frac{\tau^K n - \tau^J m}{\varepsilon} \right).
\]

---

## 2. The Exact Arithmetic Contract

### Theorem 2.1 (The Arithmetic Contract).
Let $K, J \in \mathbb{Z}$, and let $w \in C_c^\infty((0, \infty))$ with $\operatorname{supp}(w) \subset [a, b]$.
Define the active station sets in $[a, b]$:
\[
S_K = \operatorname{supp}(\mu_K) \cap [a, b] = \left\{ \tau^K n : n \ge 2, \ \tau^K n \in [a, b] \right\},
\]
\[
S_J = \operatorname{supp}(\mu_J) \cap [a, b] = \left\{ \tau^J m : m \ge 2, \ \tau^J m \in [a, b] \right\}.
\]
Then:
1. **Finiteness**: $S_K$ and $S_J$ are finite sets:
   \[
   |S_K| \le \frac{b - a}{\tau^K} + 1 < \infty, \qquad |S_J| \le \frac{b - a}{\tau^J} + 1 < \infty.
   \]
2. **Disjointness for Distinct Grades ($K \ne J$)**:
   If $K \ne J$, then:
   \[
   S_K \cap S_J = \emptyset.
   \]
   In particular, if both $S_K$ and $S_J$ are non-empty, the minimum station distance:
   \[
   d_{\min} := \min_{x \in S_K, \ y \in S_J} |x - y| > 0
   \]
   is strictly positive.
3. **Identical Vanishing for Small $\varepsilon$ ($K \ne J$)**:
   For any $0 < \varepsilon < d_{\min}$:
   \[
   Q_\varepsilon^{K, J}[w] = 0 \quad \text{identically}.
   \]
   *(If $S_K = \emptyset$ or $S_J = \emptyset$, $Q_\varepsilon^{K, J}[w] = 0$ for all $\varepsilon > 0$.)*
4. **Positivity Implication**:
   If for a fixed window $w$ and fixed grades $K \ne J$, $Q_\varepsilon^{K, J}[w] > 0$ for arbitrarily small $\varepsilon > 0$, then there exist non-zero integer witnesses $n^*, m^* \in \mathbb{Z}_{\ge 2}$ such that:
   \[
   \tau^K n^* = \tau^J m^* \iff m^* \tau^J = n^* \tau^K.
   \]
5. **Diagonal Control ($K = J$)**:
   When $K = J$, for all $\varepsilon < \tau^K$:
   \[
   Q_\varepsilon^{K, K}[w] = \sum_{n \ge 2} \Lambda(n)^2 w(\tau^K n)^2.
   \]
   This limit is strictly positive whenever $[a, b]$ contains at least one prime-power point $\tau^K p^m$.

*Proof.*
1. Since $\tau^K > 0$ and $[a, b]$ is bounded, $n$ is restricted to $a/\tau^K \le n \le b/\tau^K$, which contains finitely many integers. Thus $S_K$ is finite. The same holds for $S_J$.
2. Suppose $x \in S_K \cap S_J$. Then $x = \tau^K n = \tau^J m$ for integers $n, m \ge 2$.
   Since $K \ne J$, assume without loss of generality $K > J$.
   Then:
   \[
   \tau^{K - J} = \frac{m}{n} \in \mathbb{Q}_{>0}.
   \]
   However, $\tau = 2\pi$. By Lindemann's theorem (1882), $\pi$ is transcendental over $\mathbb{Q}$, hence $\tau = 2\pi$ is transcendental, and any positive integer power $\tau^{K - J}$ ($K - J \ge 1$) is transcendental.
   A transcendental number cannot equal a rational number $m/n \in \mathbb{Q}$.
   Therefore, no such $x$ exists: $S_K \cap S_J = \emptyset$.
   Since $S_K$ and $S_J$ are finite, the set of pairwise distances $\{ |x - y| : x \in S_K, y \in S_J \}$ is finite and contains only strictly positive real numbers. Its minimum $d_{\min}$ is therefore strictly positive.
3. For any $x \in S_K$ and $y \in S_J$, $|x - y| \ge d_{\min}$.
   If $\varepsilon < d_{\min}$, then $\frac{|x - y|}{\varepsilon} \ge \frac{d_{\min}}{\varepsilon} > 1$.
   Since $\operatorname{supp}(\eta) \subset (-1, 1)$, $\eta(u) = 0$ for all $|u| \ge 1$.
   Hence $\eta\left(\frac{x - y}{\varepsilon}\right) = 0$ for every pair $(x, y) \in S_K \times S_J$.
   Since $w(x) = 0$ for $x \notin S_K$ and $w(y) = 0$ for $y \notin S_J$, every term in the double sum vanishes. Thus $Q_\varepsilon^{K, J}[w] = 0$.
4. Suppose $\exists \varepsilon_k \downarrow 0$ such that $Q_{\varepsilon_k}^{K, J}[w] > 0$.
   Since $w \ge 0, \Lambda \ge 0, \eta \ge 0$, a sum of non-negative terms is positive if and only if at least one term is non-zero.
   Thus for each $k$, there exists $(x_k, y_k) \in S_K \times S_J$ such that:
   \[
   |x_k - y_k| < \varepsilon_k.
   \]
   Since $S_K \times S_J$ is a finite set, there are only finitely many possible pairs $(x, y)$. By the Pigeonhole Principle, at least one pair $(x^*, y^*) \in S_K \times S_J$ must occur for infinitely many $k$.
   For this pair:
   \[
   |x^* - y^*| < \varepsilon_k \quad \text{for arbitrarily small } \varepsilon_k \implies |x^* - y^*| = 0 \implies x^* = y^*.
   \]
   Let $x^* = \tau^K n^*$ and $y^* = \tau^J m^*$. Then $\tau^K n^* = \tau^J m^*$ with $n^*, m^* \ge 2$, establishing the coincidence.
5. When $K = J$, $S_K = S_J$. The diagonal terms have $x = y = \tau^K n$, so $\frac{x - y}{\varepsilon} = 0$ and $\eta(0) = 1$.
   The off-diagonal terms have $x = \tau^K n, y = \tau^K m$ with $n \ne m$.
   Since $n, m \in \mathbb{Z}$, $|x - y| = \tau^K |n - m| \ge \tau^K$.
   For $\varepsilon < \tau^K$, $\frac{|x - y|}{\varepsilon} > 1 \implies \eta\left(\frac{x - y}{\varepsilon}\right) = 0$.
   Thus all off-diagonal terms vanish, leaving strictly the diagonal mass:
   \[
   Q_\varepsilon^{K, K}[w] = \sum_{n \ge 2} \Lambda(n)^2 w(\tau^K n)^2. \quad \square
   \]

---

## 3. Two-Variable Graded Explicit Formula for $Q_\varepsilon^{K, J}[w]$

To investigate whether spectral modes can force positivity of $Q_\varepsilon^{K, J}[w]$, we derive its two-variable explicit formula representation.

Define the smooth two-variable test kernel:
\[
F_\varepsilon(x, y) = w(x) w(y) \eta\left( \frac{x - y}{\varepsilon} \right) \in C_c^\infty((0, \infty)^2).
\]
Then:
\[
Q_\varepsilon^{K, J}[w] = \langle \mu_K \otimes \mu_J, F_\varepsilon \rangle.
\]

### Proposition 3.1 (One-Variable Pushforward Formula).
For any $f \in C_c^\infty((a_K, \infty))$ with $a_K = \tau^K$:
\[
\langle \mu_K, f \rangle = a_K^{-1} \widetilde f(1) - \sum_{\rho \in Z_{\rm nt}} m_\rho a_K^{-\rho} \widetilde f(\rho) - \sum_{j \ge 1} a_K^{2j} \widetilde f(-2j),
\]
where $\widetilde f(s) = \int_0^\infty f(x) x^{s-1} \, dx$.

*Proof.*
$\langle \mu_K, f \rangle = \sum_{n \ge 2} \Lambda(n) f(\tau^K n)$. Let $\phi(u) = f(\tau^K u)$.
Then $\widetilde\phi(s) = \int_0^\infty f(\tau^K u) u^{s-1} \, du = \tau^{-Ks} \int_0^\infty f(x) x^{s-1} \, dx = a_K^{-s} \widetilde f(s)$.
The standard smoothed explicit formula on $\phi$ gives:
\[
\sum_{n \ge 2} \Lambda(n) \phi(n) = \widetilde\phi(1) - \sum_{\rho} m_\rho \widetilde\phi(\rho) - \sum_{j \ge 1} \widetilde\phi(-2j).
\]
Substituting $\widetilde\phi(s) = a_K^{-s} \widetilde f(s)$ proves the formula. $\square$

### Proposition 3.2 (Two-Variable Representation).
For a shared window $w$ supported on $[a, b]$ with $a > \max(a_K, a_J)$, applying Proposition 3.1 in $x$ and $y$ successively:
\[
Q_\varepsilon^{K, J}[w] = \mathcal{M}_{1, 1}(\varepsilon) - \mathcal{M}_{1, \rm spec}(\varepsilon) - \mathcal{M}_{\rm spec, 1}(\varepsilon) + \mathcal{M}_{\rm spec, spec}(\varepsilon) + \mathcal{R}_{\rm bg}(\varepsilon),
\]
where:
- $\mathcal{M}_{1, 1}(\varepsilon) = a_K^{-1} a_J^{-1} \widetilde F_\varepsilon(1, 1)$,
- $\mathcal{M}_{1, \rm spec}(\varepsilon) = a_K^{-1} \sum_{\rho_2} m_{\rho_2} a_J^{-\rho_2} \widetilde F_\varepsilon(1, \rho_2)$,
- $\mathcal{M}_{\rm spec, 1}(\varepsilon) = a_J^{-1} \sum_{\rho_1} m_{\rho_1} a_K^{-\rho_1} \widetilde F_\varepsilon(\rho_1, 1)$,
- $\mathcal{M}_{\rm spec, spec}(\varepsilon) = \sum_{\rho_1, \rho_2} m_{\rho_1} m_{\rho_2} a_K^{-\rho_1} a_J^{-\rho_2} \widetilde F_\varepsilon(\rho_1, \rho_2)$,
- $\widetilde F_\varepsilon(s_1, s_2) = \iint_0^\infty w(x) w(y) \eta\left(\frac{x - y}{\varepsilon}\right) x^{s_1 - 1} y^{s_2 - 1} \, dx \, dy$,
- $\mathcal{R}_{\rm bg}(\varepsilon)$ contains all terms involving trivial zeros $s_1 = -2j$ or $s_2 = -2\ell$.

---

## 4. Asymptotic Scaling Analysis as $\varepsilon \to 0$

Let us analyze the behavior of the two-variable transform $\widetilde F_\varepsilon(s_1, s_2)$ as $\varepsilon \downarrow 0$:
Substitute $y = x - \varepsilon u$.
Since $\operatorname{supp}(\eta) \subset (-1, 1)$, the integral over $y$ becomes an integral over $u \in (-1, 1)$ with Jacobian factor $\varepsilon$:
\[
\widetilde F_\varepsilon(s_1, s_2) = \varepsilon \int_0^\infty dx \, x^{s_1 - 1} w(x) \int_{-1}^1 du \, \eta(u) w(x - \varepsilon u) (x - \varepsilon u)^{s_2 - 1}.
\]
Expanding $w(x - \varepsilon u) = w(x) - \varepsilon u w'(x) + O(\varepsilon^2)$ and $(x - \varepsilon u)^{s_2 - 1} = x^{s_2 - 1} - \varepsilon u (s_2 - 1) x^{s_2 - 2} + O(\varepsilon^2)$:
\[
\widetilde F_\varepsilon(s_1, s_2) = \varepsilon \left( \int_{-1}^1 \eta(u) \, du \right) \left( \int_0^\infty w(x)^2 x^{s_1 + s_2 - 2} \, dx \right) + O(\varepsilon^2).
\]

### Lemma 4.1 (Linear $\varepsilon$-Scaling of Smooth Spectral Terms).
For every pair $(s_1, s_2) \in \mathbb{C}^2$, as $\varepsilon \to 0$:
\[
\widetilde F_\varepsilon(s_1, s_2) = \varepsilon \|\eta\|_{L^1} \widetilde{w^2}(s_1 + s_2 - 1) + O(\varepsilon^2),
\]
where $\widetilde{w^2}(s) = \int_0^\infty w(x)^2 x^{s-1} \, dx$.
In particular, for any finite spectral cutoffs $T_1, T_2 < \infty$:
\[
\sum_{|\gamma_1| \le T_1, |\gamma_2| \le T_2} m_{\rho_1} m_{\rho_2} a_K^{-\rho_1} a_J^{-\rho_2} \widetilde F_\varepsilon(\rho_1, \rho_2) = O(\varepsilon) \to 0 \quad \text{as } \varepsilon \to 0.
\]

---

## 5. Audit of the Candidate Bridge Inequality

We now evaluate the candidate bridge inequality proposed in research discussions:
\[
Q_\varepsilon^{K, J}[w] \ge c D_{K - J}(\rho_0) - r_\varepsilon \quad (\text{Hypothetical Bridge Inequality}),
\]
where $c > 0$, $r_\varepsilon \to 0$ as $\varepsilon \to 0$, and
\[
D_M(\rho_0) = 4\sinh^2\left( \frac{M(\Re\rho_0 - 1/2)\log\tau}{2} \right).
\]

### Theorem 5.1 (Refutation of the Candidate Bridge Inequality for Fixed Windows).
Let $K \ne J$ be fixed distinct grades. Let $w \in C_c^\infty((0, \infty))$ be a fixed window with compact support $[a, b]$.
Let $\rho_0 = \beta_0 + i\gamma_0$ be an off-line zero candidate with $\beta_0 \ne 1/2$.
Then:
The inequality
\[
Q_\varepsilon^{K, J}[w] \ge c D_{K - J}(\rho_0) - r_\varepsilon \quad (\text{with } c > 0, \ r_\varepsilon \to 0)
\]
**CANNOT HOLD**.

*Proof.*
Since $\beta_0 \ne 1/2$ and $K - J \ne 0$, the displacement factor is strictly positive:
\[
D_{K - J}(\rho_0) = 4\sinh^2\left( \frac{(K - J)(\beta_0 - 1/2)\log\tau}{2} \right) > 0.
\]
If the candidate inequality held with $c > 0$, then because $r_\varepsilon \to 0$, there exists $\varepsilon_0 > 0$ such that for all $0 < \varepsilon < \varepsilon_0$:
\[
r_\varepsilon \le \frac{1}{2} c D_{K - J}(\rho_0).
\]
Consequently, for all $0 < \varepsilon < \varepsilon_0$:
\[
Q_\varepsilon^{K, J}[w] \ge \frac{1}{2} c D_{K - J}(\rho_0) > 0.
\]
However, by Theorem 2.1 (Arithmetic Contract, Part 3):
Since $K \ne J$ and $w$ is supported in $[a, b]$, either $S_K$ or $S_J$ is empty (in which case $Q_\varepsilon^{K, J}[w] = 0$ for all $\varepsilon$), or both are non-empty and their minimum distance $d_{\min} > 0$ is strictly positive by Lindemann (1882).
In both cases:
\[
Q_\varepsilon^{K, J}[w] = 0 \quad \text{for all } 0 < \varepsilon < d_{\min}.
\]
Choosing $\varepsilon < \min(\varepsilon_0, d_{\min})$:
\[
0 = Q_\varepsilon^{K, J}[w] \ge \frac{1}{2} c D_{K - J}(\rho_0) > 0,
\]
which is a direct contradiction ($0 > 0$). $\square$

---

## 6. Interaction Between Gaussian Isolation and Fixed-Window Localization

We now address why the Section 7E whole-spectrum isolating Gaussian family $\phi_L$ cannot simply be inserted into the arithmetic overlap observable $Q_\varepsilon^{K, J}[w]$.

### Theorem 6.1 (Support Disjointness Barrier).
Let $\phi_L(x)$ be the Section 7E log-Gaussian test family with $L \ge 2$.
Let $[a, b] \subset (0, \infty)$ be any fixed compact arithmetic window.
Then for all:
\[
L > \log b,
\]
we have:
\[
\operatorname{supp}(\phi_L) \cap [a, b] = \emptyset.
\]
Consequently, restricting $\phi_L$ to any fixed arithmetic window $[a, b]$ yields the identically zero function for all sufficiently large $L$:
\[
w(x) \phi_L(x) \equiv 0 \quad \text{for all } L > \log b.
\]

*Proof.*
By Definition 3.2, $\phi_L(x) = x^{-\rho_0} [P(-\partial_t) g_L(t)]_{t = \log x}$.
The kernel $g_L(t) = c_L^{-1} H_L(t) \chi(t/L)$ is supported in $(L, 17L)$.
Therefore, $\log x \in (L, 17L) \implies x \in (e^L, e^{17L})$.
The lower support bound is $a_L = e^L$.
If $L > \log b$, then $e^L > b$.
Since $[a, b]$ lies entirely below $b < e^L$, the sets $[a, b]$ and $[e^L, e^{17L}]$ are completely disjoint. $\square$

### Remark 6.2 (The Centering Dilemma).
If one attempts to prevent the support from escaping by recentering the Gaussian at a fixed $t_0 \in \log[a, b]$:
Let $g_{L, t_0}(t) = \frac{1}{\sqrt{4\pi L}} e^{-(t - t_0)^2 / (4L)} \chi(t)$.
Then $t_0$ is fixed, so as $L \to \infty$, the Gaussian variance $\sigma^2 = 2L \to \infty$.
A Gaussian with fixed center and infinite variance becomes flat on $[a, b]$, rather than concentrating in frequency!
Conversely, concentrating in frequency requires the log-shift $6L$ in $H_L(t) = \frac{1}{\sqrt{4\pi L}} e^{-(t-6L)^2/(4L)}$, which forces the support center to $e^{6L} \to \infty$.
This establishes a **fundamental trade-off**:
- Whole-spectrum mode isolation requires large scale $L \to \infty$ with support escaping to $\infty$.
- Arithmetic station comparison requires a fixed compact window $[a, b]$.

---

## 7. Preliminary Obstruction for Smooth Densities in Strip Pairing

### Proposition 7.1 (Vanishing Strip Pairing for Smooth Densities).
Let $f, g \in C^1([a, b])$ be two smooth continuous densities on $[a, b]$.
Let $w \in C_c^\infty((a, b))$ and let $\eta \in C_c^\infty((-1, 1))$ with $\eta \ge 0$.
Define the strip pairing:
\[
I_\varepsilon[f, g] := \iint_{[a, b]^2} w(x) w(y) \eta\left( \frac{x - y}{\varepsilon} \right) f(x) g(y) \, dx \, dy.
\]
Then:
1. $I_\varepsilon[f, g] = \varepsilon \|\eta\|_{L^1} \int_a^b w(x)^2 f(x) g(x) \, dx + O(\varepsilon^2)$.
2. In particular:
   \[
   \lim_{\varepsilon \to 0} I_\varepsilon[f, g] = 0.
   \]
3. Dividing by $\varepsilon$ produces a density-overlap limit:
   \[
   \lim_{\varepsilon \to 0} \frac{1}{\varepsilon} I_\varepsilon[f, g] = \|\eta\|_{L^1} \int_a^b w(x)^2 f(x) g(x) \, dx.
   \]
   However, for discrete arithmetic measures $\mu_K, \mu_J$ with $K \ne J$, by Theorem 2.1:
   \[
   \frac{1}{\varepsilon} Q_\varepsilon^{K, J}[w] = \frac{0}{\varepsilon} = 0 \quad \text{for all } \varepsilon < d_{\min}.
   \]
   Thus the discrete ratio is identically zero, completely disconnected from the smooth continuous density overlap integral.

---

## 8. Conclusion: Status of the Arithmetic Coincidence Bridge

1. **Was an arithmetic exclusion mechanism found?**
   **NO**. The arithmetic overlap observable $Q_\varepsilon^{K, J}[w]$ vanishes identically for all $\varepsilon < d_{\min}$ on any fixed compact window and distinct grades $K \ne J$.
2. **What prevents the bridge from closing?**
   - In a fixed window $[a, b]$, the arithmetic station gap $d_{\min} > 0$ is strictly positive by Lindemann (1882), ensuring $Q_\varepsilon^{K, J}[w] = 0$ for all small $\varepsilon$.
   - Any off-line zero $\rho_0$ contributes a smooth density $t^{\rho_0 - 1}$ that scales down linearly as $O(\varepsilon) \to 0$ in the two-variable kernel $\widetilde F_\varepsilon$, exactly matching the behavior of on-line zeros and failing to produce discrete atomic mass.
   - The Section 7E Gaussian isolating family $\phi_L$ has support escaping to $[e^L, e^{17L}]$, disjoint from any fixed window $[a, b]$ for $L > \log b$.
3. **Epistemic Classification**:
   The arithmetic coincidence bridge remains **STRICTLY OPEN**.
