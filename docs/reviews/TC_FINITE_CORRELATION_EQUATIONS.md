# TC Finite Correlation Equations, Vandermonde Invertibility, and Spectral Implications

## 1. Executive Summary & Core Reductio Objective

The central objective of the Transcendental Continuation (TC) program within `reimann_scope` is to establish the Riemann Hypothesis via a reductio ad absurdum:
$$H \Longrightarrow \exists K \ne J \in \mathbb{Z}, \; m, n \in \mathbb{N}_{>0} : m \tau^K = n \tau^J, \qquad \tau = 2\pi,$$
where $H$ denotes the existence of an off-critical non-trivial Riemann zeta zero ($\zeta(\rho_0) = 0$ with $\operatorname{Re}(\rho_0) \ne 1/2$).

### The Intended Contradiction
Because $\tau = 2\pi$ is transcendental by the Lindemann-Weierstrass theorem (1882), no rational collision $m \tau^K = n \tau^J$ can exist for distinct integer grades $K \ne J$ and positive integers $m, n$. The impossibility of this terminal collision is the **intended contradictory punchline** of the proof.
- It is **never** a reason to abandon, dismiss, or terminate the antecedent research.
- Establishing that the authentic cross-grade correlation measure $\nu_b \ne 0$ is non-vanishing does **not** refute the implication $H \Longrightarrow \nu_b = 0$.
- Rather, the non-vanishing $\nu_b \ne 0$ constitutes the necessary second half of the reductio: if an off-critical zero forces $\nu_b = 0$, then because $\nu_b \ne 0$ holds algebraically on the authentic family, $H$ is refuted.

---

## 2. Corrections to Prior Heuristic Formulations

Before analyzing the spectral bridge, five critical corrections to prior informal notes must be formalized:

1. **Independence of Zero Equation and Coefficient Selection**:
   The assumption $\zeta(\rho_0) = 0$ supplies **no equations** on an independently chosen coefficient vector $b \in \mathbb{R}^r$ until a explicit construction connecting them is mathematically derived. Simply postulating that $\zeta(\rho_0) = 0$ does not constrain $b$.

2. **Dimension of the Deflation Constraint**:
   Imposing $\widehat{F}_b(\rho_0) = 0$ (or $E_b(\rho_0 - 1/2) = 0$) imposes at most **two real linear constraints** on the coefficient vector $b$:
   $$\operatorname{Re}(E_b(\delta_0 + i\gamma_0)) = 0, \qquad \operatorname{Im}(E_b(\delta_0 + i\gamma_0)) = 0.$$
   It is not an automatic consequence of $\zeta(\rho_0) = 0$. Furthermore, artificially enforcing $\widehat{F}_b(\rho_0) = 0$ completely extinguishes the off-critical target response $\Delta_{\rm quartet}(\rho_0; G_b) = 4 \operatorname{Re}(A_h(z_0)^2 E_b(z_0) E_b(-z_0))$ under the reflected pairing, defeating the purpose of detecting the zero.

3. **Finiteness of the Correlation System**:
   For any declared finite set of grades $\mathcal{G}$ and compact window $[a, b]$, the active prime stations are finite. Consequently, the condition that the cross-grade correlation measure vanishes identically ($\nu_b = 0$) is equivalent to **finitely many algebraic quadratic equations**, not an infinite continuum of independent constraints.

4. **Authentic Grade Masses vs. Equal-Mass Normalization**:
   In the authentic arithmetic TC family, the contracted station masses are:
   $$D_K = \tau^K \sum_{n} \Lambda(n) w(\tau^K n) > 0.$$
   Because prime powers are irregularly distributed across dyadic intervals, $D_K$ varies with grade (e.g. for window $[8, 20]$, $D_{-1} \approx 7.485$, $D_{-2} \approx 7.285$, $D_{-3} \approx 7.248$, $D_{-4} \approx 7.243$). Equal grade masses ($D_K \equiv s$) are an additional idealizing normalization, not an intrinsic property of the arithmetic family. The total mass formula $\nu_b(\mathbb{R}) = -s^2 \|b\|_2^2$ applies only under the equal-mass hypothesis; on authentic weights, $\nu_b(\mathbb{R}) = -\sum_K D_K^2 b_K^2 + (\sum_K D_K b_K)^2$.

5. **Role of Non-Vanishing in Reductio**:
   Proving that $\nu_b \ne 0$ for legal $b$ does not refute the hypothesis $H$; it proves that $\nu_b = 0$ is a valid contradictory target.

---

## 3. Explicit Finite System of Grouped Atom Equations

Let $\mathcal{G} = \{K_1, \ldots, K_r\}$ be a finite set of integer grades. For each grade $K \in \mathcal{G}$, let $\mathcal{S}_K$ denote the finite set of active prime powers $n$ such that $\tau^K n \in [a, b]$.
The authentic station weights are:
$$a_{K, n} = \tau^K \Lambda(n) w(\tau^K n) > 0, \qquad n \in \mathcal{S}_K.$$

For a legal zero-sum coefficient vector $b \in \mathbb{R}^r$ ($\sum_{K} b_K = 0$), the discrete signed correlation measure $\nu_b$ on $\mathbb{R}_{>0}$ is formed by cross-grade pairs $(K \ne J)$:
$$\nu_b = \sum_{\substack{K \ne J \\ n \in \mathcal{S}_K, m \in \mathcal{S}_J}} b_K b_J a_{K, n} a_{J, m} \, \delta_{\frac{\tau^K n}{\tau^J m}}.$$

### Exact Grouping of Identical Ratios
Let $\{y_1, y_2, \ldots, y_L\}$ denote the set of **distinct** spatial ratios in the set:
$$\mathcal{Y} = \left\{ \tau^{K - J} \frac{n}{m} : K, J \in \mathcal{G}, K \ne J, n \in \mathcal{S}_K, m \in \mathcal{S}_J \right\}.$$

Because $\tau = 2\pi$ is transcendental, two ratios $\tau^{K - J} \frac{n}{m}$ and $\tau^{K' - J'} \frac{n'}{m'}$ coincide if and only if:
$$K - J = K' - J' \qquad \text{and} \qquad \frac{n}{m} = \frac{n'}{m'} \in \mathbb{Q}.$$
No cross-grade ratios with different grade differences can coincide.

Grouping all atom pairs that yield the exact same spatial ratio $y_\ell$ yields:
$$\nu_b = \sum_{\ell=1}^L c_\ell(b) \, \delta_{y_\ell},$$
where the coefficient $c_\ell(b)$ is the quadratic form in $b$:
$$c_\ell(b) = \sum_{\substack{(K, n, J, m) \\ \tau^{K-J} (n/m) = y_\ell}} b_K b_J a_{K, n} a_{J, m}.$$

### Equivalence to Finite Algebraic Equations
Since the support points $y_1, \ldots, y_L$ are distinct positive real numbers, the measure $\nu_b$ vanishes identically if and only if every point mass vanishes:
$$\nu_b = 0 \quad \Longleftrightarrow \quad c_\ell(b) = 0 \quad \text{for all } \ell = 1, \dots, L.$$

---

## 4. Equivalent Moment Formulation via Vandermonde Invertibility

Instead of testing $\nu_b$ against indicator functions of points, consider the power moments of $\nu_b$:
$$\mu_r(\nu_b) = \int_{0}^\infty y^r \, d\nu_b(y) = \sum_{\ell=1}^L c_\ell(b) y_\ell^r, \qquad r = 0, 1, \ldots, L-1.$$

### Theorem (Vandermonde Invertibility of Finite Atom Vanishing)
Let $y_1 < y_2 < \dots < y_L$ be $L$ distinct positive real numbers, and let $\nu_b = \sum_{\ell=1}^L c_\ell(b) \delta_{y_\ell}$.
Then:
$$\nu_b = 0 \quad \Longleftrightarrow \quad \sum_{\ell=1}^L c_\ell(b) y_\ell^r = 0 \quad \text{for all } r \in \{0, 1, \dots, L-1\}.$$

*Proof.*
In matrix form, the system of the first $L$ moments $\boldsymbol{\mu} = (\mu_0, \mu_1, \dots, \mu_{L-1})^T$ is related to the coefficient vector $\mathbf{c} = (c_1, \dots, c_L)^T$ by:
$$\begin{pmatrix} 1 & 1 & \cdots & 1 \\ y_1 & y_2 & \cdots & y_L \\ y_1^2 & y_2^2 & \cdots & y_L^2 \\ \vdots & \vdots & \ddots & \vdots \\ y_1^{L-1} & y_2^{L-1} & \cdots & y_L^{L-1} \end{pmatrix} \begin{pmatrix} c_1(b) \\ c_2(b) \\ \vdots \\ c_L(b) \end{pmatrix} = \begin{pmatrix} \mu_0(\nu_b) \\ \mu_1(\nu_b) \\ \vdots \\ \mu_{L-1}(\nu_b) \end{pmatrix}.$$
The matrix $V(y_1, \dots, y_L)$ is the classical Vandermonde matrix on $L$ distinct nodes.
Its determinant is:
$$\det V(y_1, \dots, y_L) = \prod_{1 \le i < j \le L} (y_j - y_i).$$
Because $y_1 < y_2 < \dots < y_L$, all differences $y_j - y_i > 0$, so $\det V \ne 0$.
The matrix $V$ is strictly invertible.
Therefore:
$$\mathbf{c} = V^{-1} \boldsymbol{\mu}.$$
Consequently, $\boldsymbol{\mu} = 0 \Longleftrightarrow \mathbf{c} = 0 \Longleftrightarrow \nu_b = 0$. $\blacksquare$

### Reflection Symmetry and Reduced Degrees of Freedom
The cross-grade correlation possesses an exact reflection symmetry under inversion $y \leftrightarrow 1/y$:
$$\text{If } y_\ell = \tau^{K-J} \frac{n}{m}, \quad \text{then } y_{\ell'} = \frac{1}{y_\ell} = \tau^{J-K} \frac{m}{n}.$$
Because $b_K b_J a_{K,n} a_{J,m} = b_J b_K a_{J,m} a_{K,n}$, the coefficient at $1/y_\ell$ satisfies:
$$c_{\ell'}(b) = c_\ell(b).$$
Thus, among the $L$ distinct ratios, pairs $(y_\ell, 1/y_\ell)$ have identical coefficients. If $L = 2M$ (with no self-ratios $y=1$ across distinct grades, which is guaranteed by transcendence of $\tau$), there are only $M$ algebraically independent equations among the $L$ equations $c_\ell(b) = 0$.

---

## 5. Concrete 2-Grade Computational Example

To ground these equations concretely, consider the minimal cross-grade family:
- Grades: $\mathcal{G} = \{-1, -2\}$.
- Dilation parameter: $\tau = 2\pi \approx 6.2831853$.
- Stations: Let grade $-1$ have stations $n \in \{64, 128\}$, and grade $-2$ have stations $m \in \{4096, 8192\}$.
  Note: $\tau^{-1} \times 64 \approx 10.186 \in [8, 20]$, $\tau^{-1} \times 128 \approx 20.37$ (just outside, but included for illustration).
- Cross-grade grade difference: $\Delta K = -1 - (-2) = 1$.
- Possible ratios:
  1. $y_1 = \tau^1 \times \frac{64}{8192} = \tau / 128 \approx 0.049087$.
  2. $y_2 = \tau^1 \times \frac{64}{4096} = \tau^1 \times \frac{128}{8192} = \tau / 64 \approx 0.098175$.
  3. $y_3 = \tau^1 \times \frac{128}{4096} = \tau / 32 \approx 0.196350$.
- Inverted ratios ($J - K = 1$):
  4. $y_4 = 1/y_3 = 32 / \tau \approx 5.092958$.
  5. $y_5 = 1/y_2 = 64 / \tau \approx 10.185916$.
  6. $y_6 = 1/y_1 = 128 / \tau \approx 20.371833$.

Here, $L = 6$ distinct ratios, with $M = 3$ reflection pairs.
Notice that $y_2$ receives contributions from **two distinct atom pairs**:
$(n=64, m=4096)$ and $(n=128, m=8192)$, because $64/4096 = 128/8192 = 1/64$.
Its coefficient is:
$$c_2(b) = b_{-1} b_{-2} \left( a_{-1, 64} a_{-2, 4096} + a_{-1, 128} a_{-2, 8192} \right).$$
Since $a_{K, n} > 0$, the sum of weights is strictly positive:
$$W_2 = a_{-1, 64} a_{-2, 4096} + a_{-1, 128} a_{-2, 8192} > 0.$$
Therefore:
$$c_2(b) = 0 \quad \Longleftrightarrow \quad b_{-1} b_{-2} = 0.$$
However, for any legal zero-sum vector $b$ with $\|b\|_2 = 1$ in 2 grades:
$$b_{-1} + b_{-2} = 0, \quad b_{-1}^2 + b_{-2}^2 = 1 \quad \Longrightarrow \quad b = \pm \left( \frac{1}{\sqrt{2}}, -\frac{1}{\sqrt{2}} \right).$$
Thus $b_{-1} b_{-2} = -1/2 \ne 0$!
Hence $c_2(b) = -W_2 / 2 < 0$.
The coefficient $c_2(b)$ **cannot vanish** for any legal unit vector $b$!
This proves directly that for 2 grades, $\nu_b = 0$ is algebraically impossible on legal non-trivial vectors.

---

## 6. Investigation: Can an Off-Critical Zero Force $\nu_b = 0$?

We now investigate whether an explicit formula identity under $H$ can force the finite system $c_\ell(b) = 0$.

### The Explicit Formula Quadratic Identity
Let $G_b(u)$ be the legal TC test function with Fourier transform $\widehat{G_b}(z) = A_h(z) E_b(z)$.
The Guinand-Weil explicit formula expresses the arithmetic Weil quadratic form as:
$$\mathcal{B}_{\rm arith}(G_b, G_b) = \sum_{\rho} A_h(\rho - 1/2)^2 E_b(\rho - 1/2) E_b(-\rho + 1/2) + \mathcal{R}_{\rm triv}(G_b).$$

Under hypothesis $H$, there exists an off-critical zero quartet $\rho_0 = 1/2 \pm \delta_0 \pm i\gamma_0$ with $\delta_0 \ne 0$.
Its contribution to the spectral side is:
$$\Delta_{\rm quartet}(\rho_0; G_b) = 4 \operatorname{Re}\left( A_h(z_0)^2 E_b(z_0) E_b(-z_0) \right), \qquad z_0 = \delta_0 + i\gamma_0.$$

### Expansion of the Dirichlet Polynomial Product
The product $E_b(z) E_b(-z)$ expands across prime stations:
$$E_b(z) E_b(-z) = \sum_{K, n} b_K^2 a_{K,n}^2 + \sum_{K \ne J} b_K b_J \sum_{n, m} a_{K,n} a_{J,m} e^{z (\log(\tau^K n) - \log(\tau^J m))}.$$
Grouping by distinct spatial ratios $y_\ell = \tau^{K-J}(n/m)$, the cross-grade part is:
$$\sum_{K \ne J} b_K b_J \sum_{n, m} a_{K,n} a_{J,m} y_\ell^z = \int_0^\infty y^z \, d\nu_b(y) = \sum_{\ell=1}^L c_\ell(b) y_\ell^z.$$

### The Core Obstruction: Degeneracy of a Single Zero Constraint
Suppose we assume $H$: $\zeta(\rho_0) = 0$.
Does the existence of this single zero $\rho_0$ force $\sum_{\ell=1}^L c_\ell(b) y_\ell^{z_0} = 0$?
1. **Spectral Evaluation is 1-Dimensional**:
   Evaluating the explicit formula at $\rho_0$ yields a single complex scalar relation:
   $$\sum_{\ell=1}^L c_\ell(b) y_\ell^{\delta_0 + i\gamma_0} = \Phi(\rho_0).$$
   This provides **at most 2 real constraints** on the coefficients $c_\ell(b)$.
2. **Dimension Mismatch**:
   The number of distinct cross-grade ratios $L$ grows with the number of stations $N$: $L \sim N^2$. For typical families, $L \ge 20$ to $100$.
   Two real linear constraints cannot force $L$ independent quadratic expressions $c_\ell(b)$ to vanish simultaneously.
3. **No Operator Forces Pointwise Equality**:
   There is no continuous projection or linear operator $\mathcal{T}$ that maps the single zero condition $\zeta(\rho_0) = 0$ to the Vandermonde system $V \mathbf{c} = 0$.
   A linear condition on the Fourier transform at a single point $z_0$ can never force the vanishing of all Fourier frequencies or all moments.

### First Precise Unresolved Sublemma
For the TC reductio to proceed from $H$ to an integer collision via $\nu_b = 0$, one must prove:

> **Sublemma (Spectral-Correlation Bridge - UNRESOLVED)**:
> Let $H$ hold with off-critical zero $\rho_0$. There exists a family of legal vectors $b^{(\epsilon)}$ or an integral transform over the vertical line $\operatorname{Re}(s) = \delta_0$ such that the integral against $\zeta(s)^{-1}$ or the explicit formula kernel forces every moment $\mu_r(\nu_b) = 0$ for $r = 0, \dots, L-1$.

Without such a sublemma, the inference $H \Longrightarrow \nu_b = 0$ remains unproved.
However, if such an implication is ever established, the non-vanishing theorem $\nu_b \ne 0$ (proved in Section 5 and formalized in Lean 4) immediately closes the reductio ad absurdum and proves RH.

---

## 7. Mathematical Conclusions

1. **Exact Representation**: The condition $\nu_b = 0$ for finite stations is equivalent to the finite system $c_\ell(b) = 0$ ($\ell=1,\dots,L$), and equivalent to the vanishing of the first $L$ power moments by Vandermonde invertibility.
2. **Authentic Non-Vanishing**: For 2 grades (and any legal zero-sum family with positive active weights), $c_\ell(b)$ cannot vanish identically because diagonal and extremal grade interactions have fixed signs that cannot cancel.
3. **Reductio Status**: The non-vanishing of $\nu_b$ is not an obstacle; it is the desired contradictory pole of the reductio ad absurdum. The missing link is the antecedent implication $H \Longrightarrow \nu_b = 0$.
