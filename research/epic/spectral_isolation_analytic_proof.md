# Analytic Proof of Whole-Spectrum Log-Gaussian Spectral Isolation

**Role**: Spectral Analyst  
**Epic Track**: Section 7E — Primary Candidate for Whole-Spectrum Approximation  
**Target Statement**: For every fixed nontrivial zero $\rho_0 = \beta_0 + i\gamma_0$ ($0 < \beta_0 < 1$) of the Riemann zeta function $\zeta(s)$ and every fixed nonempty finite integer grade block $I \subset \mathbb{Z}$,
\[
\lim_{L \to \infty} \max_{k \in I} \left| Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k \right| = 0,
\]
where $\phi_L \in C_c^\infty((0, \infty))$ is an explicitly constructed smooth compactly supported test function, $m_{\rho_0}$ is the multiplicity of $\rho_0$, and $q_\rho = \tau^{\rho - 1/2}$ ($\tau = 2\pi$).

---

## 1. Setup, Competitor Set, and Cancellation Polynomial

Let $\rho_0 = \beta_0 + i\gamma_0$ be an actual nontrivial zero of $\zeta(s)$, so $\zeta(\rho_0) = 0$ with $0 < \beta_0 < 1$.
Fix the band half-width $\Delta = 3$. Define the near-band competitor set:
\[
C = \left\{ \rho \in \mathbb{C} : \zeta(\rho) = 0, \ 0 < \Re\rho < 1, \ \rho \ne \rho_0, \ |\Im\rho - \gamma_0| \le 3 \right\}.
\]

### Lemma 1.1 (Finiteness of the Competitor Set).
The set $C$ is finite: $d := |C| < \infty$.

*Proof.*
The Riemann zeta function $\zeta(s)$ is meromorphic on $\mathbb{C}$ with its only pole at $s=1$. Its nontrivial zeros lie in the open critical strip $0 < \Re s < 1$. In the compact rectangle
\[
K_0 = [0, 1] \times [\gamma_0 - 3, \gamma_0 + 3] \subset \mathbb{C},
\]
$\zeta(s)$ is holomorphic. Since $\zeta(s)$ is not identically zero, its zeros in $K_0$ cannot have an accumulation point by the identity theorem for holomorphic functions. Therefore, $K_0 \cap \zeta^{-1}(\{0\})$ is a finite set.
By the Riemann-von Mangoldt formula, the number of zeros in $K_0$ satisfies:
\[
|C| \le N(\gamma_0 + 3) - N(\gamma_0 - 3) = \frac{3}{\pi} \log\left(2 + |\gamma_0|\right) + O(1) < \infty. \quad \square
\]

### Definition 1.2 (Cancellation Polynomial).
Define the monic normalized cancellation polynomial:
\[
P(z) = \prod_{\rho \in C} \left(1 - \frac{z}{\rho - \rho_0}\right).
\]
If $C = \emptyset$, set $P(z) \equiv 1$.
Properties of $P(z)$:
1. $P(0) = 1$.
2. $\deg P = d = |C|$.
3. For every competitor zero $\rho \in C$, $z = \rho - \rho_0$ is a root of $P$:
   \[
   P(\rho - \rho_0) = 0.
   \]
4. There exists a constant $C_P > 0$ depending only on $\rho_0$ and $C$ such that for all $s = \beta + i\gamma$ with $0 \le \beta \le 1$:
   \[
   |P(s - \rho_0)| \le C_P \left(1 + |\gamma - \gamma_0|\right)^d.
   \]

---

## 2. Test Function Family and Normalization

Choose once and for all a fixed smooth cutoff function $\chi \in C^\infty(\mathbb{R})$ satisfying:
- $0 \le \chi(u) \le 1$ for all $u \in \mathbb{R}$,
- $\chi(u) = 1$ for $u \in [2, 16]$,
- $\chi(u) = 0$ for $u \le 1$ and $u \ge 17$.

For each scale parameter $L \ge 1$, let
\[
H_L(t) = \frac{1}{\sqrt{4\pi L}} \exp\left(-\frac{(t - 6L)^2}{4L}\right).
\]
Define the truncated log-Gaussian kernel:
\[
g_L(t) = \frac{1}{c_L} H_L(t) \chi(t/L), \quad \text{where } c_L = \int_\mathbb{R} H_L(t) \chi(t/L) \, dt.
\]
By construction:
\[
\int_\mathbb{R} g_L(t) \, dt = 1, \qquad \operatorname{supp}(g_L) \subset (L, 17L).
\]

### Lemma 2.1 (Gaussian Normalization Error).
For all $L \ge 1$, the normalization constant $c_L$ satisfies:
\[
0 < 1 - c_L \le \frac{1}{2\sqrt{\pi L}} e^{-4L}.
\]

*Proof.*
Since $\chi(u) = 1$ on $[2, 16]$ and $0 \le \chi(u) \le 1$ elsewhere:
\[
1 - c_L = \int_\mathbb{R} (1 - \chi(t/L)) H_L(t) \, dt = \int_{-\infty}^{2L} (1 - \chi(t/L)) H_L(t) \, dt + \int_{16L}^\infty (1 - \chi(t/L)) H_L(t) \, dt.
\]
Using $0 \le 1 - \chi \le 1$:
\[
1 - c_L \le \int_{-\infty}^{2L} H_L(t) \, dt + \int_{16L}^\infty H_L(t) \, dt.
\]
Substitute $u = \frac{t - 6L}{2\sqrt{L}}$. Then $dt = 2\sqrt{L} \, du$ and $H_L(t) \, dt = \frac{1}{\sqrt{\pi}} e^{-u^2} \, du$.
For $t = 2L$, $u = \frac{-4L}{2\sqrt{L}} = -2\sqrt{L}$.
For $t = 16L$, $u = \frac{10L}{2\sqrt{L}} = 5\sqrt{L}$.
Thus:
\[
1 - c_L \le \frac{1}{\sqrt{\pi}} \int_{-\infty}^{-2\sqrt{L}} e^{-u^2} \, du + \frac{1}{\sqrt{\pi}} \int_{5\sqrt{L}}^\infty e^{-u^2} \, du = \frac{1}{2} \operatorname{erfc}(2\sqrt{L}) + \frac{1}{2} \operatorname{erfc}(5\sqrt{L}).
\]
Using the standard complementary error function bound $\operatorname{erfc}(x) \le \frac{1}{\sqrt{\pi} x} e^{-x^2}$ for $x > 0$:
\[
\frac{1}{2} \operatorname{erfc}(2\sqrt{L}) \le \frac{1}{4\sqrt{\pi L}} e^{-4L}, \qquad \frac{1}{2} \operatorname{erfc}(5\sqrt{L}) \le \frac{1}{10\sqrt{\pi L}} e^{-25L}.
\]
For $L \ge 1$, $e^{-25L} \le e^{-21} e^{-4L} \ll e^{-4L}$. Therefore:
\[
1 - c_L \le \left(\frac{1}{4\sqrt{\pi L}} + \frac{1}{10\sqrt{\pi L}} e^{-21}\right) e^{-4L} \le \frac{1}{2\sqrt{\pi L}} e^{-4L}. \quad \square
\]

### Definition 2.2 (The Test Function $\phi_L$).
Define the smooth test function on $(0, \infty)$:
\[
\phi_L(x) = x^{-\rho_0} \left[ P(-\partial_t) g_L(t) \right]_{t = \log x}.
\]
Since $\operatorname{supp}(g_L) \subset (L, 17L)$, the support of $\phi_L$ is:
\[
\operatorname{supp}(\phi_L) \subset \left[e^L, e^{17L}\right] \subset (0, \infty).
\]
In particular, $\phi_L \in C_c^\infty((0, \infty))$.
Its lower support bound is $a_L = e^L$.

---

## 3. Mellin Transform and Mode Annihilation

### Proposition 3.1 (Mellin Transform Representation).
The Mellin transform $\widetilde\phi_L(s) = \int_0^\infty \phi_L(x) x^{s-1} \, dx$ is entire and given by:
\[
\widetilde\phi_L(s) = P(s - \rho_0) \int_\mathbb{R} g_L(t) e^{(s - \rho_0)t} \, dt.
\]

*Proof.*
Substitute $x = e^t$, $dx = e^t \, dt$:
\[
\widetilde\phi_L(s) = \int_\mathbb{R} \left( e^{-\rho_0 t} [P(-\partial_t) g_L(t)] \right) e^{(s-1)t} e^t \, dt = \int_\mathbb{R} [P(-\partial_t) g_L(t)] e^{(s - \rho_0)t} \, dt.
\]
Let $P(z) = \sum_{j=0}^d c_j z^j$ with $c_0 = 1$.
For each monomial $(-\partial_t)^j$, since $g_L$ has compact support in $(L, 17L)$, integration by parts $j$ times with vanishing boundary terms yields:
\[
\int_\mathbb{R} (-\partial_t)^j g_L(t) \cdot e^{(s - \rho_0)t} \, dt = (s - \rho_0)^j \int_\mathbb{R} g_L(t) e^{(s - \rho_0)t} \, dt.
\]
Summing over $j = 0, \dots, d$ proves the proposition. $\square$

### Corollary 3.2 (Target Normalization and Near-Band Annihilation).
1. At the target zero $s = \rho_0$:
   \[
   \widetilde\phi_L(\rho_0) = P(0) \int_\mathbb{R} g_L(t) \, dt = 1 \cdot 1 = 1.
   \]
2. For every competitor zero $\rho \in C$:
   \[
   \widetilde\phi_L(\rho) = P(\rho - \rho_0) \int_\mathbb{R} g_L(t) e^{(\rho - \rho_0)t} \, dt = 0 \cdot \int_\mathbb{R} g_L(t) e^{(\rho - \rho_0)t} \, dt = 0.
   \]

---

## 4. Decomposition of the Transform and the Exponent Bound

Write $g_L(t) = \frac{1}{c_L} [H_L(t) + r_L(t)]$, where
\[
r_L(t) = (\chi(t/L) - 1) H_L(t).
\]
Note that $\chi(t/L) - 1 = 0$ on $[2L, 16L]$, so $r_L(t)$ is supported on $(-\infty, 2L] \cup [16L, \infty)$.
Thus, for any $s \in \mathbb{C}$:
\[
\widetilde\phi_L(s) = \frac{P(s - \rho_0)}{c_L} \left[ \int_\mathbb{R} H_L(t) e^{(s - \rho_0)t} \, dt + \int_\mathbb{R} r_L(t) e^{(s - \rho_0)t} \, dt \right].
\]

### Lemma 4.1 (Untruncated Gaussian Transform).
For $z = s - \rho_0 = \sigma + i\tau_0$:
\[
\int_\mathbb{R} H_L(t) e^{zt} \, dt = \exp\left(L z^2 + 6L z\right).
\]

*Proof.*
Substitute $u = t - 6L$:
\[
\int_\mathbb{R} \frac{1}{\sqrt{4\pi L}} e^{-u^2/(4L)} e^{z(u + 6L)} \, du = e^{6Lz} \frac{1}{\sqrt{4\pi L}} \int_\mathbb{R} e^{-(u^2 - 4Lzu)/(4L)} \, du.
\]
Completing the square in the exponent: $u^2 - 4Lzu = (u - 2Lz)^2 - 4L^2 z^2$.
Thus:
\[
\int_\mathbb{R} e^{-(u - 2Lz)^2/(4L) + Lz^2} \, du = e^{Lz^2} \int_\mathbb{R} e^{-(u - 2Lz)^2/(4L)} \, du = e^{Lz^2} \sqrt{4\pi L}.
\]
Multiplying by $\frac{e^{6Lz}}{\sqrt{4\pi L}}$ gives $\exp(Lz^2 + 6Lz)$. $\square$

### Lemma 4.2 (Exponent Bound Outside the Canceled Band).
*(Formally verified in Lean 4 as `RiemannScope.gaussian_exponent_band_bound`)*
For all $\sigma \in [-1, 1]$ and all $\tau_0 \in \mathbb{R}$ with $|\tau_0| \ge 3$:
\[
\Re(z^2 + 6z) = \sigma^2 + 6\sigma - \tau_0^2 \le -2.
\]

*Proof.*
The quadratic function $f(\sigma) = \sigma^2 + 6\sigma$ on $[-1, 1]$ is strictly increasing since $f'(\sigma) = 2\sigma + 6 \ge 4 > 0$.
Its maximum on $[-1, 1]$ is attained at $\sigma = 1$:
\[
\max_{\sigma \in [-1, 1]} (\sigma^2 + 6\sigma) = 1^2 + 6(1) = 7.
\]
Since $|\tau_0| \ge 3$, we have $\tau_0^2 \ge 9$. Therefore:
\[
\sigma^2 + 6\sigma - \tau_0^2 \le 7 - 9 = -2. \quad \square
\]

### Corollary 4.3 (Exponential Decay of the Untruncated Transform).
For all $s = \beta + i\gamma$ with $0 \le \beta \le 1$ and $|\gamma - \gamma_0| \ge 3$:
\[
\left|\exp\left(L(s - \rho_0)^2 + 6L(s - \rho_0)\right)\right| \le e^{7L} e^{-L(\gamma - \gamma_0)^2} \le e^{-2L}.
\]
In particular, for $|\gamma - \gamma_0| \ge 4$, $e^{-L(\gamma - \gamma_0)^2} \le e^{-16L}$, so the untruncated Gaussian decays at rate $\le e^{-9L}$.

---

## 5. Cutoff Remainder Derivatives and Frequency Decay

Now consider the truncated piece $r_L(t) = (\chi(t/L) - 1) H_L(t)$.
Let $z = s - \rho_0 = \sigma + i\tau_0$ with $|\sigma| \le 1$ and $|\tau_0| = |\gamma - \gamma_0| \ge 3$.

### Lemma 5.1 (Cutoff Remainder $L^1$ Derivative Bound).
For each fixed non-negative integer $p \ge 0$, there exists a constant $C_{p, \chi}$ depending only on $p$ and the fixed cutoff $\chi$ such that for all $L \ge 1$:
\[
\sup_{|\sigma| \le 1} \left\| \partial_t^p \left( e^{\sigma t} r_L(t) \right) \right\|_{L^1(\mathbb{R})} \le C_{p, \chi} L^{-1/2} e^{-2L}.
\]

*Proof.*
We have $r_L(t) = (\chi(t/L) - 1) H_L(t)$.
By Leibniz's product rule:
\[
\partial_t^p \left( e^{\sigma t} (\chi(t/L) - 1) H_L(t) \right) = \sum_{j=0}^p \binom{p}{j} \partial_t^j [e^{\sigma t} (\chi(t/L) - 1)] \partial_t^{p-j} H_L(t).
\]
Now consider the two disjoint regions where $\chi(t/L) - 1 \ne 0$:
1. **Left tail**: $t \le 2L$. Here $u = \frac{t - 6L}{2\sqrt{L}} \le -2\sqrt{L}$.
   In this region, $e^{\sigma t} \le e^{|\sigma| t} \le e^{2L}$ (since $\sigma \le 1, t \le 2L$).
   The Gaussian $H_L(t) = \frac{1}{\sqrt{4\pi L}} e^{-(t - 6L)^2/(4L)}$.
   Notice that:
   \[
   e^{\sigma t} H_L(t) = \frac{1}{\sqrt{4\pi L}} \exp\left( \sigma t - \frac{(t - 6L)^2}{4L} \right) = \frac{1}{\sqrt{4\pi L}} \exp\left( 6L\sigma + L\sigma^2 - \frac{(t - 6L - 2L\sigma)^2}{4L} \right).
   \]
   At $t = 2L$, the exponent is:
   \[
   \sigma(2L) - \frac{(2L - 6L)^2}{4L} = 2L\sigma - \frac{16L^2}{4L} = 2L\sigma - 4L = 2L(\sigma - 2) \le 2L(1 - 2) = -2L!
   \]
   For all $t \le 2L$, since $\sigma \le 1 < 3$, the function $h(t) = \sigma t - \frac{(t - 6L)^2}{4L}$ is strictly increasing in $t$:
   \[
   h'(t) = \sigma - \frac{t - 6L}{2L} \ge -1 - \frac{2L - 6L}{2L} = -1 - (-2) = +1 > 0.
   \]
   Therefore, for all $t \le 2L$:
   \[
   \sigma t - \frac{(t - 6L)^2}{4L} \le h(2L) \le -2L.
   \]
2. **Right tail**: $t \ge 16L$. Here $u = \frac{t - 6L}{2\sqrt{L}} \ge 5\sqrt{L}$.
   At $t = 16L$, the exponent is:
   \[
   \sigma(16L) - \frac{(16L - 6L)^2}{4L} = 16L\sigma - \frac{100L^2}{4L} = 16L\sigma - 25L = L(16\sigma - 25) \le L(16(1) - 25) = -9L!
   \]
   For $t \ge 16L$:
   \[
   h'(t) = \sigma - \frac{t - 6L}{2L} \le 1 - \frac{16L - 6L}{2L} = 1 - 5 = -4 < 0.
   \]
   Therefore, $h(t)$ is strictly decreasing on $[16L, \infty)$, so for all $t \ge 16L$:
   \[
   \sigma t - \frac{(t - 6L)^2}{4L} \le h(16L) \le -9L \le -2L.
   \]
3. **Derivatives of the Gaussian**:
   Recall that $\partial_t^k H_L(t) = (2\sqrt{L})^{-k} (-1)^k He_k\left(\frac{t - 6L}{2\sqrt{L}}\right) H_L(t)$, where $He_k$ is the Hermite polynomial of degree $k$.
   On $(-\infty, 2L] \cup [16L, \infty)$, the polynomial $|He_k(u)|$ is integrated against the exponentially decaying Gaussian tail $e^{-u^2/2}$, which absorbs any polynomial factors.
4. **Derivatives of the Cutoff**:
   For $j \ge 1$, $\partial_t^j (\chi(t/L)) = L^{-j} \chi^{(j)}(t/L)$, which is bounded by $L^{-j} \|\chi^{(j)}\|_\infty$ and supported only on $[L, 2L] \cup [16L, 17L]$.

Combining these tail estimates and integrating over $t \in (-\infty, 2L] \cup [16L, \infty)$:
\[
\left\| \partial_t^p \left( e^{\sigma t} r_L(t) \right) \right\|_{L^1(\mathbb{R})} \le C_{p, \chi} L^{-1/2} e^{-2L},
\]
where $C_{p, \chi}$ depends only on $p$ and the fixed test profile $\chi$. $\square$

### Lemma 5.2 (Frequency Decay via Integration by Parts).
For all $s = \beta + i\gamma$ with $|\sigma| = |\beta - \beta_0| \le 1$ and $|\tau_0| = |\gamma - \gamma_0| \ge 3$:
\[
\left| \int_\mathbb{R} r_L(t) e^{(s - \rho_0)t} \, dt \right| \le \frac{C_{p, \chi} L^{-1/2} e^{-2L}}{|\gamma - \gamma_0|^p} \quad (\forall p \ge 0).
\]

*Proof.*
We have $\int_\mathbb{R} r_L(t) e^{(s - \rho_0)t} \, dt = \int_\mathbb{R} \left( e^{\sigma t} r_L(t) \right) e^{i\tau_0 t} \, dt$.
Integrating by parts $p$ times:
\[
\int_\mathbb{R} \left( e^{\sigma t} r_L(t) \right) e^{i\tau_0 t} \, dt = \frac{(-1)^p}{(i\tau_0)^p} \int_\mathbb{R} \partial_t^p \left( e^{\sigma t} r_L(t) \right) e^{i\tau_0 t} \, dt.
\]
The boundary terms at $\pm\infty$ vanish because $r_L(t)$ and all its derivatives decay as $e^{-t^2/(4L)} \to 0$.
Taking absolute values:
\[
\left| \int_\mathbb{R} r_L(t) e^{(s - \rho_0)t} \, dt \right| \le \frac{1}{|\tau_0|^p} \left\| \partial_t^p \left( e^{\sigma t} r_L(t) \right) \right\|_{L^1(\mathbb{R})} \le \frac{C_{p, \chi} L^{-1/2} e^{-2L}}{|\gamma - \gamma_0|^p}. \quad \square
\]

---

## 6. Summability Over All Zeros and the Main Limit Theorem

Now let us assemble the complete spectral sum outside the canceled competitor set.
For every nontrivial zero $\rho \notin C \cup \{\rho_0\}$, $|\gamma - \gamma_0| > 3$.
By Proposition 3.1 and the decomposition $g_L = \frac{1}{c_L}(H_L + r_L)$:
\[
\widetilde\phi_L(\rho) = \frac{P(\rho - \rho_0)}{c_L} \left[ \int_\mathbb{R} H_L(t) e^{(\rho - \rho_0)t} \, dt + \int_\mathbb{R} r_L(t) e^{(\rho - \rho_0)t} \, dt \right].
\]
By Lemma 4.1 and Corollary 4.3, for $|\gamma - \gamma_0| \ge 3$:
\[
\left| \int_\mathbb{R} H_L(t) e^{(\rho - \rho_0)t} \, dt \right| \le e^{7L} e^{-L(\gamma - \gamma_0)^2}.
\]
For $|\gamma - \gamma_0| \ge 3$, $(\gamma - \gamma_0)^2 \ge 9 + 6(|\gamma - \gamma_0| - 3) = 6|\gamma - \gamma_0| - 9$.
Thus $e^{7L} e^{-L(\gamma - \gamma_0)^2} \le e^{7L - 9L} e^{-L(|\gamma - \gamma_0|^2 - 9)} \le e^{-2L} e^{-(|\gamma - \gamma_0| - 3)^2}$.
By Lemma 5.2, choose $p = d + 2$, where $d = \deg P = |C|$:
\[
\left| \int_\mathbb{R} r_L(t) e^{(\rho - \rho_0)t} \, dt \right| \le \frac{C_{d+2, \chi} L^{-1/2} e^{-2L}}{|\gamma - \gamma_0|^{d+2}}.
\]
Recalling Definition 1.2, $|P(\rho - \rho_0)| \le C_P (1 + |\gamma - \gamma_0|)^d$.
Therefore:
\[
|P(\rho - \rho_0)| \left| \int_\mathbb{R} r_L(t) e^{(\rho - \rho_0)t} \, dt \right| \le C_P (1 + |\gamma - \gamma_0|)^d \frac{C_{d+2, \chi} L^{-1/2} e^{-2L}}{|\gamma - \gamma_0|^{d+2}} \le \frac{C'_P L^{-1/2} e^{-2L}}{|\gamma - \gamma_0|^2},
\]
for all $|\gamma - \gamma_0| \ge 3$, where $C'_P = C_P C_{d+2, \chi} \sup_{u \ge 3} \frac{(1+u)^d}{u^d} < \infty$.
Combining the untruncated Gaussian and cutoff terms:
\[
|\widetilde\phi_L(\rho)| \le \frac{1}{c_L} \left[ C_P (1 + |\gamma - \gamma_0|)^d e^{7L - L(\gamma - \gamma_0)^2} + \frac{C'_P L^{-1/2} e^{-2L}}{|\gamma - \gamma_0|^2} \right].
\]
For $L \ge 1$, $c_L \ge 1 - \frac{1}{2\sqrt{\pi}} e^{-4} > 0.98 > 1/2$.
Therefore, there exists a constant $M(\rho_0, C)$ independent of $L$ such that for all $\rho \notin C \cup \{\rho_0\}$ and all $L \ge 1$:
\[
m_\rho |\widetilde\phi_L(\rho)| \le M(\rho_0, C) L^{-1/2} e^{-2L} \frac{m_\rho}{|\gamma - \gamma_0|^2}.
\]

### Lemma 6.1 (Summability Over Nontrivial Zeros).
The sum
\[
S_0(\gamma_0) := \sum_{\rho \ne \rho_0} \frac{m_\rho}{|\gamma - \gamma_0|^2}
\]
is finite: $S_0(\gamma_0) < \infty$.

*Proof.*
Split the sum into near zeros with $3 < |\gamma - \gamma_0| \le 10$ and far zeros with $|\gamma - \gamma_0| > 10$.
1. For $3 < |\gamma - \gamma_0| \le 10$: the number of zeros is at most $N(\gamma_0 + 10) - N(\gamma_0 - 10) < \infty$.
   Each term is bounded by $\frac{m_\rho}{3^2} \le \frac{m_\rho}{9}$.
2. For $|\gamma - \gamma_0| > 10$: by the Riemann-von Mangoldt zero counting theorem $N(t) \le \frac{t}{2\pi}\log t$ (unconditionally valid for $t \ge 14.0$ by Lehman 1966 / Trudgian 2014 Cor. 1):
   Using Riemann-Stieltjes integration by parts:
   \[
   \sum_{|\gamma| > T} \frac{m_\rho}{\gamma^2} = \int_T^\infty \frac{1}{t^2} \, dN(t) = \left[ \frac{N(t)}{t^2} \right]_T^\infty + 2 \int_T^\infty \frac{N(t)}{t^3} \, dt \le \frac{1}{\pi} \frac{\log T + 1}{T} < \infty.
   \]
   Thus $S_0(\gamma_0) < \infty$. $\square$

### Theorem 6.2 (Whole-Spectrum Isolation Theorem).
Let $\rho_0$ be an actual nontrivial zero of $\zeta(s)$.
Let $I \subset \mathbb{Z}$ be any nonempty finite integer grade block.
Then:
\[
\lim_{L \to \infty} \max_{k \in I} \left| Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k \right| = 0.
\]

*Proof.*
Let $k \in I$.
By the complete explicit formula for $\phi_L$ (with $0 < h_k < a_L = e^L$ satisfied for all $L > \max(1, -(\min I)\log\tau)$):
\[
Y_{\phi_L}(k) = \sum_{\rho} m_\rho \widetilde\phi_L(\rho) q_\rho^k.
\]
By Corollary 3.2:
- $\widetilde\phi_L(\rho_0) = 1$, so the term for $\rho = \rho_0$ is $m_{\rho_0} q_{\rho_0}^k$.
- $\widetilde\phi_L(\rho) = 0$ for all $\rho \in C$.
Therefore, subtracting the target mode:
\[
Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k = \sum_{\rho \notin C \cup \{\rho_0\}} m_\rho \widetilde\phi_L(\rho) q_\rho^k.
\]
Taking absolute values:
\[
\left| Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k \right| \le \sum_{\rho \notin C \cup \{\rho_0\}} m_\rho |\widetilde\phi_L(\rho)| |q_\rho|^k.
\]
Recall $q_\rho = \tau^{\rho - 1/2}$. Thus $|q_\rho| = \tau^{\Re\rho - 1/2}$.
Since $0 < \Re\rho < 1$, we have $-1/2 < \Re\rho - 1/2 < 1/2$, so $\tau^{-1/2} < |q_\rho| < \tau^{1/2}$.
For $k \in I$:
\[
|q_\rho|^k \le \tau^{|k|/2} \le \tau^{\max_{k \in I} |k|/2} =: K_I < \infty.
\]
Applying the bound from Lemma 6.1:
\[
\max_{k \in I} \left| Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k \right| \le K_I \sum_{\rho \notin C \cup \{\rho_0\}} m_\rho |\widetilde\phi_L(\rho)| \le K_I M(\rho_0, C) S_0(\gamma_0) L^{-1/2} e^{-2L}.
\]
As $L \to \infty$:
\[
L^{-1/2} e^{-2L} \to 0.
\]
Therefore:
\[
\lim_{L \to \infty} \max_{k \in I} \left| Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k \right| = 0. \quad \square
\]

---

## 7. Quantifier Scoping and Reconciliation with Prior Counterexamples

### Critical Distinction 7.1 (Varying Test Family vs Fixed Observable Transport).
Theorem 6.2 proves:
\[
\forall \rho_0, \ \forall I \subset \mathbb{Z} \text{ (finite)}, \ \forall \varepsilon > 0, \quad \exists L = L(I, \varepsilon, \rho_0) : \quad \max_{k \in I} \left| Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k \right| < \varepsilon.
\]
This is an **existential approximation on each compact grade block by an adaptive family $\phi_L$**.
It does **NOT** state that for a single fixed test $\phi$, the sequence $(Y_\phi(k))_{k \in \mathbb{Z}}$ exhibits bilateral exponential growth $|q_{\rho_0}|^k$ as $k \to \pm\infty$.
As illustrated by the counterexample:
\[
Y_L(k) = q^k e^{-k^2/L} \quad (q > 1),
\]
for every fixed finite block $I$, $\max_{k \in I} |Y_L(k) - q^k| \to 0$ as $L \to \infty$; however, for any fixed $L$, $\lim_{k \to \infty} Y_L(k) = 0$.
In Transcendental Continuation, as $k \to \pm\infty$, the dilation scale $h_k = \tau^{-k}$ leaves the valid support interval $(0, a_L)$, transitioning through the support boundary.
Therefore, the dependency graph step from finite-block isolation to single-observable divergence is **invalid without an additional unproved premise of grade-uniform transport**.
Theorem 6.2 is accepted strictly with its precise block-quantified scope.

### Critical Distinction 7.2 (Reconciliation with Paley-Wiener / Jensen Obstruction).
By Farmer (1995) and Conrey (1989), distinct zeros satisfy $N_{\text{distinct}}(T) \ge \frac{0.40}{2\pi} T \log T$.
By Jensen's formula, for any *fixed* non-zero test $\phi \in C_c^\infty((0, \infty))$, its Mellin transform $\widetilde\phi(s)$ is an entire function of exponential type whose zeros in $|s| \le r$ satisfy $n(r) = O(r) \ll T\log T$.
Consequently:
- A single fixed test cannot annihilate all but finitely many distinct zeros of $\zeta(s)$.
- However, Theorem 6.2 does not use a fixed test; it uses a **dynamically scaled family $\phi_L$** whose frequency window expands with $L$, and whose Gaussian tail decays faster than the zero-density growth. This completely reconciles the isolation theorem with Paley-Wiener theory.
