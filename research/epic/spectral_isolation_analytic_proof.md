# Analytic Proof of Whole-Spectrum Log-Gaussian Spectral Isolation

**Role**: Spectral Analyst
**Epic Track**: Section 7E — Primary Candidate for Whole-Spectrum Mode Isolation
**Target Statement**: For every fixed nontrivial zero $\rho_0 = \beta_0 + i\gamma_0$ ($0 < \beta_0 < 1$) of the Riemann zeta function $\zeta(s)$, every nonempty finite integer grade block $I \subset \mathbb{Z}$, and every $\varepsilon > 0$, there exists an explicitly constructed smooth compactly supported test function $\phi_L \in C_c^\infty((0, \infty))$ such that:
\[
\max_{k \in I} \left| Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k \right| < \varepsilon,
\]
where $m_{\rho_0}$ is the multiplicity of $\rho_0$, $q_{\rho_0} = \tau^{\rho_0 - 1/2}$ ($\tau = 2\pi$), and $Y_\phi(k)$ is the centered explicit-formula observable.

---

## 1. Explicit Formula Notation & Exponent Derivation

### 1.1 The Smoothed Riemann Explicit Formula
Let $\phi \in C_c^\infty((0, \infty))$ with compact support $\operatorname{supp}(\phi) \subset [a, b]$ where $0 < a < b < \infty$.
Define its Mellin transform:
\[
\widetilde\phi(s) = \int_0^\infty \phi(x) x^{s-1} \, dx.
\]
Because $\phi$ is smooth and compactly supported on $(0, \infty)$, $\widetilde\phi(s)$ is an entire function of $s \in \mathbb{C}$ that decays faster than any inverse power of $|s|$ in any vertical strip:
\[
\forall \sigma_1 \le \sigma_2, \ \forall N \ge 0, \quad \sup_{\sigma_1 \le \Re(s) \le \sigma_2} |s|^N |\widetilde\phi(s)| < \infty.
\]

By Mellin inversion on $\Re(s) = c > 1$:
\[
\sum_{n \ge 2} \Lambda(n) \phi(hn) = \frac{1}{2\pi i} \int_{c - i\infty}^{c + i\infty} \left(-\frac{\zeta'}{\zeta}(s)\right) \widetilde\phi(s) h^{-s} \, ds.
\]
Shifting the contour to $\Re(s) = -\infty$ and picking up the residues:
- Pole of $-\zeta'/\zeta(s)$ at $s = 1$ with residue $1$: contribution $h^{-1} \widetilde\phi(1)$.
- Nontrivial zeros $\rho \in Z_{\rm nt}$ of $\zeta(s)$ ($0 < \Re\rho < 1$) with multiplicities $m_\rho$: residue $-m_\rho$, contribution $-\sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi(\rho) h^{-\rho}$.
- Trivial zeros at $s = -2j$ ($j \ge 1$) with residue $-1$: contribution $-\sum_{j \ge 1} \widetilde\phi(-2j) h^{2j}$.
- Holomorphy at $s = 0$: since $\zeta(0) = -1/2 \ne 0$, $-\zeta'/\zeta(s)$ has no pole at $s = 0$ (residue is 0).

Multiplying through by the coordinate dilation factor $h > 0$:
\[
h \sum_{n \ge 2} \Lambda(n) \phi(hn) = \widetilde\phi(1) - \sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi(\rho) h^{1-\rho} - \sum_{j \ge 1} \widetilde\phi(-2j) h^{1+2j}.
\]

### 1.2 Unnormalized vs. Centered Observables
For grade index $k \in \mathbb{Z}$, define the scale factor:
\[
h_k = \tau^{-k} \quad (\tau = 2\pi).
\]
Define the unnormalized observable:
\[
X_\phi(k) := \widetilde\phi(1) - \sum_{j \ge 1} h_k^{1+2j} \widetilde\phi(-2j) - h_k \sum_{n \ge 2} \Lambda(n) \phi(h_k n) = \sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi(\rho) h_k^{1-\rho}.
\]

**Critical Sign Audit**:
Notice the exact power of $\tau$ in $h_k^{1-\rho}$:
\[
h_k^{1-\rho} = \left(\tau^{-k}\right)^{1-\rho} = \tau^{-k(1-\rho)} = \tau^{k(\rho - 1)}.
\]
The unnormalized mode is $\tau^{k(\rho - 1)}$, **NOT** $\tau^{k(1-\rho)}$.

Now define the centered observable and centered character:
\[
Y_\phi(k) := h_k^{-1/2} X_\phi(k) = \tau^{k/2} X_\phi(k), \qquad q_\rho := \tau^{\rho - 1/2}.
\]
Then the spectral expansion becomes:
\[
Y_\phi(k) = \tau^{k/2} \sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi(\rho) \tau^{k(\rho - 1)} = \sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi(\rho) \tau^{k(\rho - 1/2)} = \sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi(\rho) q_\rho^k.
\]
This confirms the exact centered representation:
\[
Y_\phi(k) = \sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi(\rho) q_\rho^k.
\]

---

## 2. Competitor Set Finiteness and Cancellation Polynomial

Fix a nontrivial zero $\rho_0 = \beta_0 + i\gamma_0$ ($0 < \beta_0 < 1$).
Fix band half-width $\Delta = 3$. Define the competitor set:
\[
C = \left\{ \rho \in Z_{\rm nt} \setminus \{\rho_0\} : |\Im\rho - \gamma_0| \le 3 \right\}.
\]

### Lemma 2.1 (Finiteness of the Competitor Set).
The set $C$ is finite: $d := |C| < \infty$.

*Proof.*
The nontrivial zeros of $\zeta(s)$ are isolated in $\mathbb{C}$. In the compact box $K_0 = [0, 1] \times [\gamma_0 - 3, \gamma_0 + 3]$, $\zeta(s)$ is holomorphic and non-zero. By Bolzano-Weierstrass, an infinite zero set in $K_0$ would have an accumulation point, forcing $\zeta \equiv 0$ by the identity theorem, a contradiction.
Quantitatively, by the Riemann-von Mangoldt formula:
\[
|C| \le N(\gamma_0 + 3) - N(\gamma_0 - 3) = \frac{3}{\pi} \log\left(2 + |\gamma_0|\right) + O(1) < \infty. \quad \square
\]

### Definition 2.2 (Cancellation Polynomial).
Define:
\[
P(z) = \prod_{\rho \in C} \left(1 - \frac{z}{\rho - \rho_0}\right) \quad (\text{with } P(z) \equiv 1 \text{ if } C = \emptyset).
\]
Then:
1. $P(0) = 1$.
2. For all $\rho \in C$, $P(\rho - \rho_0) = 0$.
3. $\deg P = d = |C|$.
4. For all $z = \sigma + i\eta$ with $|\sigma| \le 1$:
   \[
   |P(z)| \le \prod_{\rho \in C} \left(1 + \frac{|\sigma| + |\eta|}{|\rho - \rho_0|}\right) \le C_P \left(1 + |\eta|^d\right),
   \]
   where $C_P = \prod_{\rho \in C} \left(1 + \frac{2}{|\rho - \rho_0|}\right) < \infty$.

---

## 3. The Truncated Log-Gaussian Family $\phi_L$

Let $\chi \in C_c^\infty((1, 17))$ be a standard smooth cutoff with $0 \le \chi \le 1$ and $\chi(u) = 1$ for $u \in [2, 16]$.
For $L \ge 2$, define:
\[
H_L(t) = \frac{1}{\sqrt{4\pi L}} \exp\left(-\frac{(t - 6L)^2}{4L}\right), \quad g_L(t) = \frac{1}{c_L} H_L(t) \chi(t/L),
\]
where
\[
c_L = \int_\mathbb{R} H_L(t) \chi(t/L) \, dt.
\]

### Lemma 3.1 (Normalization Enclosure).
For all $L \ge 2$:
\[
0 < 1 - c_L \le \frac{1}{2\sqrt{\pi L}} e^{-4L}, \quad \text{and} \quad c_L \ge 1 - \frac{1}{2\sqrt{2\pi}} e^{-8} > 0.999.
\]

*Proof.*
$1 - c_L = \int_{t \le 2L} (1 - \chi) H_L \, dt + \int_{t \ge 16L} (1 - \chi) H_L \, dt \le \int_{-\infty}^{2L} H_L(t) dt + \int_{16L}^\infty H_L(t) dt$.
Substituting $u = \frac{t - 6L}{2\sqrt{L}}$ gives tails at $u \le -2\sqrt{L}$ and $u \ge 5\sqrt{L}$:
\[
1 - c_L \le \frac{1}{2} \operatorname{erfc}(2\sqrt{L}) + \frac{1}{2} \operatorname{erfc}(5\sqrt{L}) \le \frac{1}{4\sqrt{\pi L}} e^{-4L} + \frac{1}{10\sqrt{\pi L}} e^{-25L} \le \frac{1}{2\sqrt{\pi L}} e^{-4L}. \quad \square
\]

### Definition 3.2 (Test Function $\phi_L$).
Define for $x \in (0, \infty)$:
\[
\phi_L(x) = x^{-\rho_0} \left[ P(-\partial_t) g_L(t) \right]_{t = \log x}.
\]
Because $\operatorname{supp}(g_L) \subset (L, 17L)$, we have $\operatorname{supp}(\phi_L) \subset [e^L, e^{17L}] \subset (0, \infty)$.
Thus $\phi_L \in C_c^\infty((0, \infty))$.

### Proposition 3.3 (Mellin Transform & Exact Cancellation).
The Mellin transform of $\phi_L$ is:
\[
\widetilde\phi_L(s) = P(s - \rho_0) \int_\mathbb{R} g_L(t) e^{(s - \rho_0)t} \, dt.
\]
In particular:
1. Target normalization: $\widetilde\phi_L(\rho_0) = P(0) \int g_L(t) dt = 1.0$ identically for all $L$.
2. Competitor annihilation: $\widetilde\phi_L(\rho) = 0$ for all $\rho \in C$.

*Proof.*
Substitute $x = e^t$, $dx = e^t dt$:
\[
\widetilde\phi_L(s) = \int_\mathbb{R} \left(e^{-\rho_0 t} [P(-\partial_t) g_L(t)]\right) e^{(s-1)t} e^t dt = \int_\mathbb{R} [P(-\partial_t) g_L(t)] e^{(s - \rho_0)t} dt.
\]
Integrating by parts $j$ times on each term $(-\partial_t)^j g_L(t)$ transfers $(-\partial_t)^j$ to $(s - \rho_0)^j$, with boundary terms vanishing due to compact support. Summing over terms in $P$ gives the result. $\square$

---

## 4. Completion of the Square and Cutoff Derivative Estimates

Decompose $g_L(t) = \frac{1}{c_L} [H_L(t) + r_L(t)]$, where $r_L(t) = (\chi(t/L) - 1) H_L(t)$.
Let $z = \rho - \rho_0 = \sigma + i\eta$ with $|\sigma| \le 1$ and $|\eta| \ge 3$.
Then:
\[
\widetilde\phi_L(\rho) = \frac{P(z)}{c_L} \left[ \int_\mathbb{R} H_L(t) e^{zt} \, dt + \int_\mathbb{R} r_L(t) e^{zt} \, dt \right].
\]

### 4.1 Gaussian Completion of the Square with Frequency Decay
For the untruncated Gaussian:
\[
\int_\mathbb{R} H_L(t) e^{zt} \, dt = \exp\left(L z^2 + 6L z\right).
\]
Taking the real part of the exponent:
\[
\Re\left(L z^2 + 6L z\right) = L\left(\sigma^2 + 6\sigma - \eta^2\right).
\]
Since $|\sigma| \le 1$, $\sigma^2 + 6\sigma \le 7$.
Since $|\eta| \ge 3$, write $\eta^2 = 9 + (\eta^2 - 9)$.
Then:
\[
\sigma^2 + 6\sigma - \eta^2 \le 7 - 9 - (\eta^2 - 9) = -2 - (\eta^2 - 9).
\]
Therefore:
\[
\left| \exp\left(L z^2 + 6L z\right) \right| \le e^{-2L} e^{-L(\eta^2 - 9)} \quad (|\sigma| \le 1, \ |\eta| \ge 3).
\]
For $L \ge 2$, $e^{-L(\eta^2 - 9)} \le e^{-2(\eta^2 - 9)}$.
Because $e^{-2(\eta^2 - 9)}$ decays faster than any polynomial in $\eta$, multiplying by $|P(z)| \le C_P(1 + |\eta|^d)$:
\[
\sup_{|\eta| \ge 3} \left[ (1 + \eta^2) C_P (1 + |\eta|^d) e^{-2(\eta^2 - 9)} \right] =: C_0 < \infty.
\]
Therefore:
\[
|P(z)| \left| \int_\mathbb{R} H_L(t) e^{zt} \, dt \right| \le \frac{C_0 e^{-2L}}{1 + \eta^2} \quad (\forall L \ge 2, \ |\eta| \ge 3).
\]

### 4.2 Repaired Integration-by-Parts Estimate for Cutoff Remainder
For $r_L(t) = (\chi(t/L) - 1) H_L(t)$, $r_L(t) \equiv 0$ on $[2L, 16L]$.
Write:
\[
\int_\mathbb{R} r_L(t) e^{zt} \, dt = \int_\mathbb{R} \left(e^{\sigma t} r_L(t)\right) e^{i\eta t} \, dt.
\]
Integrating by parts $p$ times against $e^{i\eta t}$:
\[
\int_\mathbb{R} \left(e^{\sigma t} r_L(t)\right) e^{i\eta t} \, dt = \frac{(-1)^p}{(i\eta)^p} \int_\mathbb{R} \partial_t^p \left(e^{\sigma t} r_L(t)\right) e^{i\eta t} \, dt.
\]
Taking absolute values:
\[
|\eta|^p \left| \int_\mathbb{R} r_L(t) e^{zt} \, dt \right| \le \left\| \partial_t^p \left(e^{\sigma t} r_L(t)\right) \right\|_{L^1(\mathbb{R})}.
\]
*(Note: Integration by parts in $t$ isolates $|\eta|^p = |\Im z|^p$, not $|z|^p$.)*

### Lemma 4.1 ($L^1$ Remainder Derivative Bound).
For each $p \ge 0$, there exists $C_{p, \chi} < \infty$ depending only on $p$ and $\chi$ such that for all $L \ge 2$:
\[
\sup_{|\sigma| \le 1} \left\| \partial_t^p \left(e^{\sigma t} r_L(t)\right) \right\|_{L^1} \le C_{p, \chi} L^{-1/2} e^{-2L}.
\]

*Proof.*
On the left tail $t \le 2L$, the exponent of $e^{\sigma t} H_L(t)$ is $\sigma t - \frac{(t-6L)^2}{4L}$. Its derivative with respect to $t$ is $\sigma - \frac{t-6L}{2L} \ge -1 - (-2) = +1 > 0$, so its maximum on $(-\infty, 2L]$ occurs at $t = 2L$:
\[
\sigma(2L) - \frac{(2L - 6L)^2}{4L} = 2L\sigma - 4L \le 2L(1) - 4L = -2L.
\]
On the right tail $t \ge 16L$, the maximum occurs at $t = 16L$:
\[
\sigma(16L) - \frac{(16L - 6L)^2}{4L} = 16L\sigma - 25L \le 16L - 25L = -9L \le -2L.
\]
Derivatives of $H_L(t)$ generate Hermite polynomials normalized by $L^{-1/2}$, while derivatives of $\chi(t/L)$ scale as $L^{-j}$. Integrating over the tails yields the bound $C_{p, \chi} L^{-1/2} e^{-2L}$. $\square$

Choosing $p = d + 2$ where $d = \deg P$:
\[
|P(z)| \left| \int_\mathbb{R} r_L(t) e^{zt} \, dt \right| \le C_P (1 + |\eta|^d) \frac{C_{d+2, \chi} L^{-1/2} e^{-2L}}{|\eta|^{d+2}} \le \frac{C_1 L^{-1/2} e^{-2L}}{1 + \eta^2},
\]
where $C_1 = C_P C_{d+2, \chi} \sup_{u \ge 3} \frac{(1+u^d)(1+u^2)}{u^{d+2}} < \infty$.

### 4.3 Combined Frequency Bound Outside the Canceled Band
Combining Section 4.1 and Section 4.2, and using $c_L > 0.999$:
\[
|\widetilde\phi_L(\rho)| \le \frac{(C_0 + C_1 L^{-1/2}) e^{-2L}}{1 + (\Im\rho - \gamma_0)^2} \quad \text{for all } \rho \notin C \cup \{\rho_0\}, \ \forall L \ge 2.
\]

---

## 5. Infinite Zero Summability and the Block Isolation Theorem

Define the spectral zero counting measure:
\[
\nu = \sum_{\rho \in Z_{\rm nt}} m_\rho \delta_{\Im\rho}.
\]
Define the frequency tail integral:
\[
S_{\rho_0} := \int_{|t - \gamma_0| > 3} \frac{d\nu(t)}{1 + (t - \gamma_0)^2} = \sum_{\rho \notin C \cup \{\rho_0\}} \frac{m_\rho}{1 + (\Im\rho - \gamma_0)^2}.
\]

### Lemma 5.1 (Finiteness of $S_{\rho_0}$ via Trudgian 2014).
$S_{\rho_0} < \infty$ unconditionally.

*Proof.*
By Lehman (1966) and Trudgian (2014, Corollary 1), the number of zeros $N(t)$ with $0 < \gamma \le t$ satisfies $N(t) \le \frac{t}{2\pi}\log t$ for all $t \ge 14.0$.
By symmetry of nontrivial zeros about the real line ($\rho \leftrightarrow \overline\rho$), zeros with negative ordinates satisfy the identical bound $N_-(t) = N(t)$.
Split the integral $S_{\rho_0}$:
1. For $3 < |t - \gamma_0| \le 14 + |\gamma_0|$: the integration domain is a bounded interval, containing finitely many zeros $N_{\rm mid} < \infty$. Its contribution is at most $N_{\rm mid} / (1 + 3^2) < \infty$.
2. For $|t| \ge T_0 = 14 + |\gamma_0|$: $|t - \gamma_0| \ge |t| - |\gamma_0| \ge \frac{14}{14+|\gamma_0|} |t|$.
   Then by integration by parts:
   \[
   \int_{T_0}^\infty \frac{dN(t)}{t^2} = \left[ \frac{N(t)}{t^2} \right]_{T_0}^\infty + 2 \int_{T_0}^\infty \frac{N(t)}{t^3} \, dt \le \frac{\log T_0}{2\pi T_0} + \frac{1}{\pi} \int_{T_0}^\infty \frac{\log t}{t^2} \, dt < \infty.
   \]
   Summing both positive and negative ordinates, $S_{\rho_0} < \infty$. $\square$

### Theorem 5.2 (Whole-Spectrum Finite-Block Isolation Theorem).
Let $\rho_0 \in Z_{\rm nt}$ be an actual nontrivial zero of $\zeta(s)$.
Let $I \subset \mathbb{Z}$ be any nonempty finite integer grade block.
Then:
\[
\lim_{L \to \infty} \max_{k \in I} \left| Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k \right| = 0.
\]
Moreover, for all $L \ge \max(2, -(\min I)\log\tau)$, the error satisfies the explicit bound:
\[
\max_{k \in I} \left| Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k \right| \le \tau^{B/2} (C_0 + C_1 L^{-1/2}) e^{-2L} S_{\rho_0},
\]
where $B = \max_{k \in I} |k|$.

*Proof.*
When $L > -(\min I)\log\tau$, $e^L > \tau^{-\min I} = \max_{k \in I} h_k$.
Since $\operatorname{supp}(\phi_L) \subset [e^L, e^{17L}]$, the support condition $0 < h_k < e^L$ is satisfied for all $k \in I$.
By the explicit formula:
\[
Y_{\phi_L}(k) = \sum_{\rho \in Z_{\rm nt}} m_\rho \widetilde\phi_L(\rho) q_\rho^k.
\]
By Proposition 3.3:
- $\widetilde\phi_L(\rho_0) = 1$, giving target term $m_{\rho_0} q_{\rho_0}^k$.
- $\widetilde\phi_L(\rho) = 0$ for all $\rho \in C$.
Therefore:
\[
Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k = \sum_{\rho \notin C \cup \{\rho_0\}} m_\rho \widetilde\phi_L(\rho) q_\rho^k.
\]
For each zero in the critical strip, $0 < \Re\rho < 1 \implies |\Re\rho - 1/2| < 1/2$.
Thus:
\[
|q_\rho^k| = \tau^{k(\Re\rho - 1/2)} \le \tau^{|k|/2} \le \tau^{B/2}.
\]
Applying the frequency decay bound from Section 4.3:
\[
\max_{k \in I} \left| Y_{\phi_L}(k) - m_{\rho_0} q_{\rho_0}^k \right| \le \tau^{B/2} \sum_{\rho \notin C \cup \{\rho_0\}} m_\rho |\widetilde\phi_L(\rho)| \le \tau^{B/2} (C_0 + C_1 L^{-1/2}) e^{-2L} S_{\rho_0}.
\]
Since $\tau^{B/2}$, $C_0$, $C_1$, and $S_{\rho_0}$ are finite constants independent of $L$, and $e^{-2L} \to 0$ as $L \to \infty$, the limit holds. $\square$

---

## 6. Critical Scope: Barrier to Fixed-Window Arithmetic Insertion

We record the following crucial structural fact regarding the test family $\phi_L$:
- The support of $\phi_L$ is contained in $[e^L, e^{17L}]$.
- For any fixed compact arithmetic window $[a, b] \subset (0, \infty)$, as soon as $L > \log b$, we have:
  \[
  \operatorname{supp}(\phi_L) \cap [a, b] = \emptyset.
  \]
- Therefore, the Gaussian test family $\phi_L$ **cannot simply be inserted into a fixed-window arithmetic localization observable** $Q_\varepsilon^{K, J}[w]$. Whole-spectrum spectral isolation and fixed-window arithmetic localization require distinct mathematical mechanisms.
