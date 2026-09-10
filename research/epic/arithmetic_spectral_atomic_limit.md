# Arithmetic Measure Pushforward, Complete Spectral Sum, and the Shrinking Localization Limit

**Role**: Arithmetic Researcher  
**Epic Track**: Section 8 — The Arithmetic Bridge Track & Station-Level Contradiction Audit  
**Governing Question**: Does an assumed nontrivial off-critical zero $\rho_0$ ($\Re\rho_0 \ne 1/2$) of $\zeta(s)$ force an arithmetic coincidence in the atomic supports of distinct TC grade layers:
\[
\operatorname{supp}(\mu_K) \cap \operatorname{supp}(\mu_J) \ne \emptyset \quad \text{for some } K \ne J \in \mathbb{Z}?
\]

---

## 1. Concrete Arithmetic Measure Objects and Layer Disjointness

Fix $\tau = 2\pi$. For each integer grade $K \in \mathbb{Z}$, define the arithmetic layer lattice:
\[
L_K = \tau^K \mathbb{Z}, \qquad L_K^+ = \tau^K \mathbb{N}_{\ge 1}.
\]
Define the base arithmetic prime-power measure on $(0, \infty)$:
\[
\mu_0 = \sum_{n \ge 2} \Lambda(n) \delta_n,
\]
where $\Lambda(n)$ is the von Mangoldt function ($\Lambda(p^k) = \log p$ for prime $p$ and $k \ge 1$, and $\Lambda(n) = 0$ otherwise).
For the coordinate dilation operator $D_a(x) = ax$ with $a = \tau^K$, define the pushforward measure:
\[
\mu_K = (D_{\tau^K})_* \mu_0 = \sum_{n \ge 2} \Lambda(n) \delta_{\tau^K n}.
\]

### Proposition 1.1 (Formula Pairing and Grade Sign).
Let $h = \tau^{-k}$ for integer $k \in \mathbb{Z}$. For any test function $\phi \in C_c^\infty((0, \infty))$, the prime-side sum $P_h(\phi) = h \sum_{n \ge 1} \Lambda(n) \phi(hn)$ satisfies:
\[
P_h(\phi) = h \langle \mu_{-k}, \phi \rangle.
\]
In particular, the measure layer index $K$ is related to the dilation grade $k$ by $K = -k$.

*Proof.*
By definition of the pushforward pairing:
\[
\langle \mu_K, \phi \rangle = \left\langle (D_{\tau^K})_* \mu_0, \phi \right\rangle = \langle \mu_0, \phi \circ D_{\tau^K} \rangle = \sum_{n \ge 2} \Lambda(n) \phi(\tau^K n).
\]
For $h = \tau^{-k}$, we have $\tau^K = \tau^{-k} = h$ if and only if $K = -k$.
Multiplying by $h$ gives:
\[
h \langle \mu_{-k}, \phi \rangle = h \sum_{n \ge 2} \Lambda(n) \phi(hn) = P_h(\phi),
\]
since $\Lambda(1) = 0$ (so the sum over $n \ge 1$ is identical to $n \ge 2$). $\square$

### Theorem 1.2 (Unconditional Layer Support Disjointness).
For all distinct integer grades $K \ne J \in \mathbb{Z}$:
\[
\operatorname{supp}(\mu_K) \cap \operatorname{supp}(\mu_J) = \emptyset.
\]

*Proof.*
The support of $\mu_K$ is the discrete set:
\[
\operatorname{supp}(\mu_K) = \left\{ \tau^K p^m : p \text{ prime}, \ m \ge 1 \right\} \subset L_K^+.
\]
Suppose there existed $x \in \operatorname{supp}(\mu_K) \cap \operatorname{supp}(\mu_J)$.
Then there exist primes $p_1, p_2$ and positive integers $m_1, m_2 \ge 1$ such that:
\[
\tau^K p_1^{m_1} = \tau^J p_2^{m_2}.
\]
Since $K \ne J$, assume without loss of generality that $K > J$, so $K - J \ge 1$.
Dividing both sides by $\tau^J p_1^{m_1}$:
\[
\tau^{K - J} = \frac{p_2^{m_2}}{p_1^{m_1}} \in \mathbb{Q}_{>0}.
\]
Recall $\tau = 2\pi$. Thus $(2\pi)^{K - J} \in \mathbb{Q}$, which implies that $\pi$ is an algebraic number (as a root of $q x^{K-J} - p = 0$ for integers $p, q \ge 1$).
However, by Lindemann's theorem (1882), $\pi$ is transcendental over $\mathbb{Q}$.
This contradiction proves that no such station $x$ can exist.
Therefore, $\operatorname{supp}(\mu_K) \cap \operatorname{supp}(\mu_J) = \emptyset$ unconditionally for all $K \ne J$. $\square$

---

## 2. Atom Extraction Under Shrinking Localization Tests

Let $\psi \in C_c^\infty(\mathbb{R})$ be a fixed standard bump function satisfying:
- $\operatorname{supp}(\psi) \subset [-1, 1]$,
- $\psi(u) \ge 0$ for all $u \in \mathbb{R}$,
- $\psi(0) = 1$,
- $\int_{-1}^1 \psi(u) \, du = \|\psi\|_{L^1} > 0$.

For any point $x > 0$ and any scale parameter $\varepsilon > 0$, define the unnormalized shrinking test:
\[
\psi_{x, \varepsilon}(t) = \psi\left(\frac{t - x}{\varepsilon}\right).
\]
Its support is $\operatorname{supp}(\psi_{x, \varepsilon}) \subset [x - \varepsilon, x + \varepsilon]$.

### Proposition 2.1 (Prime-Side Atom Extraction).
For any fixed $x > 0$ and grade $K \in \mathbb{Z}$:
\[
\lim_{\varepsilon \downarrow 0} \langle \mu_K, \psi_{x, \varepsilon} \rangle =
\begin{cases}
\Lambda(n), & \text{if } x = \tau^K n \text{ for some integer } n \ge 2, \\
0, & \text{if } x \notin L_K^+.
\end{cases}
\]

*Proof.*
We have:
\[
\langle \mu_K, \psi_{x, \varepsilon} \rangle = \sum_{n \ge 2} \Lambda(n) \psi\left(\frac{\tau^K n - x}{\varepsilon}\right).
\]
Since $L_K = \tau^K \mathbb{Z}$ is a discrete lattice with minimum positive spacing $\tau^K$:
1. If $x = \tau^K n_0$ for some $n_0 \ge 2$:
   For all $\varepsilon < \tau^K$, for every $n \ne n_0$, $|\tau^K n - x| = |\tau^K(n - n_0)| \ge \tau^K > \varepsilon$.
   Thus $\frac{\tau^K n - x}{\varepsilon} \notin [-1, 1]$, so $\psi\left(\frac{\tau^K n - x}{\varepsilon}\right) = 0$ for all $n \ne n_0$.
   The sum collapses to a single term:
   \[
   \langle \mu_K, \psi_{x, \varepsilon} \rangle = \Lambda(n_0) \psi(0) = \Lambda(n_0) \cdot 1 = \Lambda(n_0).
   \]
2. If $x \notin L_K^+$:
   The distance $\delta_x := \operatorname{dist}(x, L_K^+) = \inf_{n \ge 1} |x - \tau^K n| > 0$.
   For all $\varepsilon < \delta_x$, every station $\tau^K n$ lies strictly outside $[x - \varepsilon, x + \varepsilon]$, so every summand vanishes identically:
   \[
   \langle \mu_K, \psi_{x, \varepsilon} \rangle = 0.
   \]
Taking $\varepsilon \downarrow 0$ establishes the claim. $\square$

---

## 3. Spectral Side Representation of the Shrinking Test

Now consider the complete smoothed explicit formula for $\psi_{x, \varepsilon}$.
For $h = \tau^K$ (i.e. grade index $k = -K$), provided $\varepsilon < x$ so that $\operatorname{supp}(\psi_{x, \varepsilon}) \subset (0, \infty)$:
\[
\langle \mu_K, \psi_{x, \varepsilon} \rangle = \tau^{-K} \left[ \widetilde\psi_{x, \varepsilon}(1) - \sum_{\rho} m_\rho \widetilde\psi_{x, \varepsilon}(\rho) \tau^{K(1 - \rho)} - B_{\tau^K}(\psi_{x, \varepsilon}) \right],
\]
where the sum over $\rho$ runs over all nontrivial zeros of $\zeta(s)$, and $B_h$ is the trivial-zero background integral:
\[
B_{\tau^K}(\psi_{x, \varepsilon}) = \tau^K \int_1^\infty \frac{\psi_{x, \varepsilon}(\tau^K u)}{u(u^2 - 1)} \, du.
\]

### Lemma 3.1 (Mellin Transform Scaling of the Shrinking Test).
For any $s \in \mathbb{C}$ and $x > 0$, as $\varepsilon \downarrow 0$:
\[
\widetilde\psi_{x, \varepsilon}(s) = \varepsilon \cdot x^{s-1} \|\psi\|_{L^1} + O(\varepsilon^2).
\]

*Proof.*
By definition of the Mellin transform:
\[
\widetilde\psi_{x, \varepsilon}(s) = \int_{x - \varepsilon}^{x + \varepsilon} \psi\left(\frac{t - x}{\varepsilon}\right) t^{s - 1} \, dt.
\]
Substitute $u = \frac{t - x}{\varepsilon}$, so $t = x + \varepsilon u$ and $dt = \varepsilon \, du$:
\[
\widetilde\psi_{x, \varepsilon}(s) = \varepsilon \int_{-1}^1 \psi(u) (x + \varepsilon u)^{s - 1} \, du.
\]
Expanding $(x + \varepsilon u)^{s - 1}$ in powers of $\varepsilon$:
\[
(x + \varepsilon u)^{s - 1} = x^{s - 1} \left(1 + \frac{\varepsilon u}{x}\right)^{s - 1} = x^{s - 1} \left(1 + (s - 1) \frac{\varepsilon u}{x} + O\left(\frac{|s - 1|^2 \varepsilon^2}{x^2}\right)\right).
\]
Integrating against $\psi(u)$:
\[
\widetilde\psi_{x, \varepsilon}(s) = \varepsilon x^{s - 1} \int_{-1}^1 \psi(u) \, du + \varepsilon^2 \frac{s - 1}{x} x^{s - 1} \int_{-1}^1 u \psi(u) \, du + O\left(|s|^2 \varepsilon^3\right).
\]
Since $\|\psi\|_{L^1} = \int_{-1}^1 \psi(u) \, du$, this proves the lemma. (If $\psi$ is chosen even, the linear term in $\varepsilon$ vanishes exactly, giving $\widetilde\psi_{x, \varepsilon}(s) = \varepsilon x^{s - 1} \|\psi\|_{L^1} + O(\varepsilon^3)$). $\square$

### Corollary 3.2 (Annihilation of Finite Zero Modes in the Atom Limit).
For any fixed finite set of zeros $S \subset \{\rho : \zeta(\rho) = 0\}$:
\[
\lim_{\varepsilon \downarrow 0} \sum_{\rho \in S} m_\rho \widetilde\psi_{x, \varepsilon}(\rho) \tau^{K(1 - \rho)} = 0.
\]

*Proof.*
By Lemma 3.1, for each $\rho \in S$:
\[
\left| \widetilde\psi_{x, \varepsilon}(\rho) \right| \le \varepsilon x^{\Re\rho - 1} \|\psi\|_{L^1} + C(\rho, x) \varepsilon^2.
\]
Since $S$ is finite, we can sum the bounds:
\[
\left| \sum_{\rho \in S} m_\rho \widetilde\psi_{x, \varepsilon}(\rho) \tau^{K(1 - \rho)} \right| \le \varepsilon \|\psi\|_{L^1} \sum_{\rho \in S} m_\rho x^{\Re\rho - 1} \tau^{K(1 - \Re\rho)} + O(\varepsilon^2) \to 0 \quad \text{as } \varepsilon \downarrow 0. \quad \square
\]

---

## 4. The Infinite Collective Mechanism of Atom Formation

### Theorem 4.1 (Atomicity is Exclusively an Infinite Tail Phenomenon).
Let $x = \tau^K n_0 \in L_K^+$ be a prime-power station with $\Lambda(n_0) > 0$.
Then:
1. Every finite subcollection of nontrivial zeros contributes zero atomic mass:
   \[
   \lim_{\varepsilon \downarrow 0} \sum_{\rho \in S} m_\rho \widetilde\psi_{x, \varepsilon}(\rho) \tau^{K(1 - \rho)} = 0 \quad (\forall S \text{ finite}).
   \]
2. The smooth leading term and background terms contribute zero atomic mass:
   \[
   \lim_{\varepsilon \downarrow 0} \widetilde\psi_{x, \varepsilon}(1) = 0, \qquad \lim_{\varepsilon \downarrow 0} B_{\tau^K}(\psi_{x, \varepsilon}) = 0.
   \]
3. The atomic mass $\Lambda(n_0)$ is produced entirely by the non-interchangeability of the limit $\varepsilon \downarrow 0$ with the infinite spectral sum:
   \[
   \Lambda(n_0) = -\tau^{-K} \lim_{\varepsilon \downarrow 0} \sum_{\rho} m_\rho \widetilde\psi_{x, \varepsilon}(\rho) \tau^{K(1 - \rho)} \ne -\tau^{-K} \sum_{\rho} m_\rho \left( \lim_{\varepsilon \downarrow 0} \widetilde\psi_{x, \varepsilon}(\rho) \right) \tau^{K(1 - \rho)} = 0.
   \]

*Proof.*
1. Proved in Corollary 3.2.
2. By Lemma 3.1 with $s = 1$, $\widetilde\psi_{x, \varepsilon}(1) = \varepsilon \|\psi\|_{L^1} \to 0$.
   For the background integral:
   \[
   B_{\tau^K}(\psi_{x, \varepsilon}) = \tau^K \int_{\max(1, (x-\varepsilon)/\tau^K)}^{(x+\varepsilon)/\tau^K} \frac{\psi\left(\frac{\tau^K u - x}{\varepsilon}\right)}{u(u^2 - 1)} \, du.
   \]
   The integration interval has length $\frac{2\varepsilon}{\tau^K}$. Since the integrand is bounded on $[x/2\tau^K, 2x/\tau^K]$, $B_{\tau^K}(\psi_{x, \varepsilon}) = O(\varepsilon) \to 0$ as $\varepsilon \downarrow 0$.
3. By Proposition 2.1, the left-hand side $\lim_{\varepsilon \downarrow 0} \langle \mu_K, \psi_{x, \varepsilon} \rangle = \Lambda(n_0) > 0$.
   Since the finite terms and background terms all vanish as $\varepsilon \downarrow 0$, the non-zero mass $\Lambda(n_0)$ must arise from the non-uniformity of the infinite sum $\sum_{\rho} m_\rho \widetilde\psi_{x, \varepsilon}(\rho)$ as $\varepsilon \downarrow 0$. $\square$

---

## 5. What Does an Off-Critical Zero Force in the Atomic Support?

Now let us examine the central TC bridge hypothesis:
Suppose there exists a nontrivial zero $\rho_0 = \beta_0 + i\gamma_0$ with $\beta_0 \ne 1/2$.
Does this off-critical zero force any change in the atomic support of $\mu_K$, or force an arithmetic coincidence across layers?

### Theorem 5.1 (Off-Critical Zeros Cannot Alter the Atomic Support).
Let $\rho_0$ be an assumed nontrivial zero with $\Re\rho_0 \ne 1/2$.
1. **No Atom Creation**: $\rho_0$ cannot create an atomic point mass at any location $x \notin L_K^+$.
2. **No Atom Displacement**: $\rho_0$ cannot shift the location of any prime-power atom $\tau^K n$ in $\operatorname{supp}(\mu_K)$.
3. **No Cross-Layer Atom Coincidence**: $\rho_0$ cannot force an atom of $\mu_K$ to coincide with an atom of $\mu_J$ for $K \ne J$.

*Proof.*
1. By definition, $\mu_K = \sum_{n \ge 2} \Lambda(n) \delta_{\tau^K n}$. The support of $\mu_K$ is determined entirely by the prime powers $p^m$ and the dilation $\tau^K$. The location of the atoms is a purely arithmetic property of the integers $\mathbb{N}$ and the map $D_{\tau^K}$.
   The explicit formula is an identity between distributions in $\mathcal{D}'((0, \infty))$. An identity cannot alter the definition of the left-hand side.
   Specifically, for any $x \notin L_K^+$, Proposition 2.1 proves that $\lim_{\varepsilon \downarrow 0} \langle \mu_K, \psi_{x, \varepsilon} \rangle = 0$ identically, regardless of whether $\zeta(s)$ has off-critical zeros.
2. The atom locations are $\{ \tau^K p^m : p \text{ prime}, m \ge 1 \}$, which are invariant fixed points of the distribution's singular support $\operatorname{sing\,supp}(\mu_K)$.
   By Lemma 3.1, the individual mode $\rho_0$ contributes:
   \[
   \tau^{-K} m_{\rho_0} \widetilde\psi_{x, \varepsilon}(\rho_0) \tau^{K(1 - \rho_0)} = \varepsilon \cdot \tau^{-K} m_{\rho_0} x^{\rho_0 - 1} \|\psi\|_{L^1} \tau^{K(1 - \rho_0)} + O(\varepsilon^2).
   \]
   As $\varepsilon \downarrow 0$, this contribution vanishes at rate $O(\varepsilon)$ at every point $x$.
   Its effect in the distribution is a smooth function $\tau^{-K} m_{\rho_0} x^{\rho_0 - 1} \tau^{K(1 - \rho_0)} \in C^\infty((0, \infty))$.
   Adding a $C^\infty$ function to a distribution does not change its singular support:
   \[
   \operatorname{sing\,supp}(\mu_K + f) = \operatorname{sing\,supp}(\mu_K) \quad (\forall f \in C^\infty).
   \]
3. By Theorem 1.2, $\operatorname{supp}(\mu_K) \cap \operatorname{supp}(\mu_J) = \emptyset$ holds unconditionally by Lindemann's transcendence of $2\pi$. Since the atomic support is identical to $\operatorname{supp}(\mu_K)$ and remains unchanged by $\rho_0$, no cross-layer atom coincidence $\operatorname{supp}(\mu_K) \cap \operatorname{supp}(\mu_J) \ne \emptyset$ can ever be produced by $\rho_0$. $\square$

---

## 6. Synthesis: The Unbridged Gap to the Arithmetic Coincidence

The preceding derivations establish the exact status of the arithmetic track:

1. **What is Established**:
   - Arithmetic layers are unconditionally disjoint: $L_K \cap L_J = \{0\}$ for $K \ne J$ (Lindemann 1882).
   - Prime measures $\mu_K$ have disjoint supports: $\operatorname{supp}(\mu_K) \cap \operatorname{supp}(\mu_J) = \emptyset$ for $K \ne J$.
   - Atom extraction via shrinking tests $\lim_{\varepsilon \downarrow 0} \langle \mu_K, \psi_{x, \varepsilon} \rangle = \Lambda(n) \delta_{x, \tau^K n}$ is an infinite spectral collective phenomenon; every finite set of zero modes contributes zero atomic mass.
   - An off-critical zero $\rho_0$ ($\Re\rho_0 \ne 1/2$) contributes a smooth function $x^{\rho_0 - 1}$ that vanishes in the shrinking localization limit and cannot shift or create discrete delta atoms.
2. **What Remains Open**:
   - The TC forbidden-coincidence bridge seeks to deduce:
     \[
     \exists \rho_0 \text{ with } \zeta(\rho_0) = 0, \ 0 < \Re\rho_0 < 1, \ \Re\rho_0 \ne \tfrac{1}{2} \implies \exists K \ne J, \ m, n \in \mathbb{Z}\setminus\{0\}: m\tau^K = n\tau^J.
     \]
   - Since $\operatorname{supp}(\mu_K) \cap \operatorname{supp}(\mu_J) = \emptyset$, this coincidence is impossible in the actual arithmetic support.
   - Therefore, any proof of this implication must establish that the assumed off-critical zero forces a contradiction with some other structural property (such as positivity, Euler product consistency, or Weil distribution pairing), rather than expecting a physical station collision in $\operatorname{supp}(\mu_K)$.
   - The arithmetic coincidence bridge remains **STRICTLY OPEN**.
