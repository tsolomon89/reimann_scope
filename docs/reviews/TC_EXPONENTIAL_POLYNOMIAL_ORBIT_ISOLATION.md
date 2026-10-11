# Exponential-Polynomial Jet Rigidity and Integer-Dilation Orbit Isolation

**Document**: `docs/reviews/TC_EXPONENTIAL_POLYNOMIAL_ORBIT_ISOLATION.md`  
**Task Reference**: TASK-TC-031  
**Repository Working Tree**: `tsolomon89/reimann_scope`  
**Parent Substantive Commit**: `e54a9d65f0a36094e3fd4be717d0a9c9ec4f226e`  
**Baseline HEAD**: `16aec95997094fec3a298eb5f7596caaff1b3305`  
**Date**: October 2026  
**Primary Classification**: `EXPONENTIAL_POLYNOMIAL_FRONTIER_SHARPENED_EXISTENCE_OPEN`

---

## Executive Summary

TASK-TC-030 and TASK-TC-030R classified the minimal ambient realization kernel support as an affine-rank-two trinomial relation:
$$a_0 + a_1 \tau^\alpha + a_2 \tau^\beta = 0,$$
where $\tau = 2\pi$, $a_0, a_1, a_2 \in \overline{\mathbb{Q}}^\times$, and $\alpha, \beta \in \mathbb{A}_{\mathbb{R}}^\times$ with $\alpha / \beta \notin \mathbb{Q}$.

TASK-TC-031 halts coefficient box expansions and reformulates this relation as an **exponential-polynomial zero problem**:
$$L = \log\tau = \log(2\pi) > 0,$$
$$F(z) = a_0 + a_1 e^{\alpha z} + a_2 e^{\beta z},$$
$$F(L) = 0 \iff a_0 + a_1 \tau^\alpha + a_2 \tau^\beta = 0.$$

By subjecting $F(z)$ to Lindemann–Weierstrass linear independence, relation-space dimension bounds, polynomial differential operators, integer dilation polynomials, and Chebyshev/Wronskian systems, this investigation establishes:

1. **Lindemann–Weierstrass Necessity**: If $F(L) = 0$, then $L = \log(2\pi)$ must be transcendental (`TRINOMIAL_RELATION_IMPLIES_LOG_TAU_TRANSCENDENTAL`). (The arithmetic nature of $\log(2\pi)$ is an open problem in number theory).
2. **Derivative-Jet Rigidity & Zero Simplicity**: For every integer $m \ge 1$, $F^{(m)}(L) \ne 0$. A second vanishing would produce a linearly independent algebraic relation vector $(0, a_1 \alpha^m, a_2 \beta^m)$, forcing $\dim \mathcal{R}_{\alpha, \beta} \ge 2$, contradicting $\dim \le 1$ from Gelfond–Schneider. In particular, $F'(L) \ne 0$, so any hypothetical trinomial zero at $L$ must be **simple** (`TRINOMIAL_ZERO_SIMPLE`, `ALL_POSITIVE_DERIVATIVE_JETS_NONZERO`).
3. **Differential-Operator Rigidity**: For any polynomial $P(T) \in \overline{\mathbb{Q}}[T]$, $P(D)F(L) = 0$ forces $P(0) = P(\alpha) = P(\beta)$ (`DIFFERENTIAL_OPERATOR_RIGIDITY`).
4. **Integer-Dilation Ray Isolation**: For $f(n) = F(nL) = a_0 + a_1 X^n + a_2 Y^n$, if $f(m) = 0$ for $m \ne 0$, then $f(km) \ne 0$ for all $k \in \mathbb{Z} \setminus \{0, 1\}$.
   - For $k \ge 2$, the polynomial $P_k(T) = a_0 + a_1 T^k + a_2(u + v T)^k$ has non-vanishing coefficient $a_2 k u v^{k-1} \ne 0$ at $T^{k-1}$.
   - For $k = -q \le -1$, the polynomial $Q_q(T) = a_0 T^q (u + v T)^q + a_1(u + v T)^q + a_2 T^q$ has non-vanishing leading coefficient $a_0 v^q \ne 0$ at $T^{2q}$.
   Both force $U = \tau^{m\alpha} \in \overline{\mathbb{Q}}$, which implies $\alpha, \beta \in S_\tau$, contradicting $\dim_{\mathbb{Q}} S_\tau \le 1$.
   For the original relation ($m = 1$), $f(n) \ne 0$ for all $n \in \mathbb{Z} \setminus \{0, 1\}$ (`INTEGER_DILATION_RAY_ISOLATION`).
5. **Base-One Lindemann Specialization**: For the canonical pair $\alpha = 1, \beta = \sqrt{2}$, $U = \tau^m = (2\pi)^m \in \overline{\mathbb{Q}}$ directly contradicts Lindemann's 1882 theorem on the transcendence of $\pi$, without requiring the external Gelfond–Schneider theorem for $S_\tau$ (`BASE_ONE_ORBIT_ISOLATION_BY_LINDEMANN`).
6. **Chebyshev System & Real-Zero Count**: The Wronskian $W(x) = e^{(\lambda_0+\lambda_1+\lambda_2)x} \prod_{i<j}(\lambda_j - \lambda_i)$ is strictly positive on all of $\mathbb{R}$. Thus $\{e^{\lambda_0 x}, e^{\lambda_1 x}, e^{\lambda_2 x}\}$ is an Extended Complete Chebyshev (ECT) system, proving $F(x)$ has **at most two real zeros** counting multiplicity (`AT_MOST_TWO_REAL_EXPONENTIAL_POLYNOMIAL_ZEROS`).
7. **Three Zero Notions Distinguished**:
   - Real zeros of $F(x)$: $\le 2$ on $\mathbb{R}$ (ECT bound).
   - Integer dilation zeros $f(n) = F(nL)$: at most two integers in $\mathbb{Z}$ ($n = 1$ and $n = 0$ if $a_0+a_1+a_2=0$).
   - Ambient-kernel relation $F(L) = 0$: existence remains **open**.
8. **Functional-Transcendence Firewall**: Functional independence of $e^{\alpha z}, e^{\beta z}$ over $\mathbb{C}(z)$ (Ax–Schanuel, differential Galois theory) does not specialize to arithmetic independence at transcendental evaluation points $z = \log(2\pi)$ (`FUNCTIONAL_RESULT_DOES_NOT_SPECIALIZE_AUTOMATICALLY`).
9. **Conservative Classification**: The status remains `EXPONENTIAL_POLYNOMIAL_FRONTIER_SHARPENED_EXISTENCE_OPEN`. No claim of original trinomial nonexistence is made; `NO_ZETA_TO_KERNEL_BRIDGE_FOUND` and `NO_RH_IMPLICATION` are strictly preserved.

---

## A. Exponential-Polynomial Reformulation

Let $\tau = 2\pi > 1$. The fundamental base logarithm is:
$$L = \log\tau = \log(2\pi) \approx 1.8378770664\dots > 0.$$

Given any three-term ambient candidate relation with algebraic coefficients $a_0, a_1, a_2 \in \overline{\mathbb{Q}}^\times$ and algebraic exponents $\alpha, \beta \in \mathbb{A}_{\mathbb{R}}^\times$ with $\alpha \ne \beta$ and $\alpha/\beta \notin \mathbb{Q}$:
$$a_0 + a_1 \tau^\alpha + a_2 \tau^\beta = 0,$$
we associate the entire function of one complex variable:
$$F(z) = a_0 + a_1 e^{\alpha z} + a_2 e^{\beta z}, \qquad z \in \mathbb{C}.$$

Since $\tau^\gamma = e^{\gamma \log\tau} = e^{\gamma L}$ for every real $\gamma$:
$$F(L) = a_0 + a_1 e^{\alpha L} + a_2 e^{\beta L} = a_0 + a_1 \tau^\alpha + a_2 \tau^\beta.$$

Thus:
$$\boxed{F(L) = 0 \iff a_0 + a_1 \tau^\alpha + a_2 \tau^\beta = 0.}$$

For every integer $n \in \mathbb{Z}$, the integer dilation orbit $f(n)$ studied in TASK-TC-030 is precisely the evaluation of $F$ on the infinite cyclic arithmetic progression $L\mathbb{Z}$:
$$f(n) = F(nL) = a_0 + a_1 e^{n\alpha L} + a_2 e^{n\beta L} = a_0 + a_1 (\tau^\alpha)^n + a_2 (\tau^\beta)^n = a_0 + a_1 X^n + a_2 Y^n.$$

Canonical terminology is defined as:
- `EXPONENTIAL_POLYNOMIAL`: The entire function $F(z) = a_0 + a_1 e^{\alpha z} + a_2 e^{\beta z}$.
- `LOG_TAU_EVALUATION`: The evaluation of $F(z)$ at $z = L = \log(2\pi)$.
- `INTEGER_DILATION_ORBIT`: The sequence $f(n) = F(nL)$ for $n \in \mathbb{Z}$.

---

## B. Why a Relation Forces $\log(2\pi)$ Transcendental

### Theorem (Lindemann–Weierstrass Necessity)
If $F(L) = 0$, then $L = \log(2\pi)$ must be transcendental.

### Proof
Assume for contradiction that $L \in \overline{\mathbb{Q}}$.
Since $2\pi \ne 1$, $L \ne 0$.
The three exponents:
$$\lambda_0 = 0, \qquad \lambda_1 = \alpha L, \qquad \lambda_2 = \beta L$$
are algebraic numbers.
Moreover, they are pairwise distinct:
- $\lambda_1 - \lambda_0 = \alpha L \ne 0$ because $\alpha \ne 0$ and $L \ne 0$.
- $\lambda_2 - \lambda_0 = \beta L \ne 0$ because $\beta \ne 0$ and $L \ne 0$.
- $\lambda_2 - \lambda_1 = (\beta - \alpha) L \ne 0$ because $\alpha \ne \beta$ and $L \ne 0$.

By the **Lindemann–Weierstrass Theorem** (F. Lindemann 1882, K. Weierstrass 1885):
> If $\theta_1, \dots, \theta_N$ are distinct algebraic numbers, then their exponentials $e^{\theta_1}, \dots, e^{\theta_N}$ are linearly independent over the field of algebraic numbers $\overline{\mathbb{Q}}$.

Applying this theorem to $\{0, \alpha L, \beta L\}$:
$$e^0 = 1, \qquad e^{\alpha L}, \qquad e^{\beta L}$$
are linearly independent over $\overline{\mathbb{Q}}$.
Therefore, any linear relation:
$$a_0 \cdot 1 + a_1 e^{\alpha L} + a_2 e^{\beta L} = 0$$
with coefficients $a_0, a_1, a_2 \in \overline{\mathbb{Q}}$ implies:
$$a_0 = a_1 = a_2 = 0.$$
This directly contradicts the hypothesis that $a_0, a_1, a_2 \in \overline{\mathbb{Q}}^\times$.
Hence, $L = \log(2\pi)$ cannot be algebraic; it must be transcendental. $\blacksquare$

### Arithmetic Status of $\log(2\pi)$
In current mathematical literature, the arithmetic nature of $\log(2\pi)$ is an **unsolved open problem** (Waldschmidt 2004, Baker 1975, Murty & Rath 2014):
- It is unknown whether $\log(2\pi)$ is rational, algebraic irrational, or transcendental.
- Schanuel's conjecture implies that $\pi$ and $\log(2\pi)$ are algebraically independent, so $\log(2\pi)$ is conjecturally transcendental.
- Unconditionally, however, no proof of transcendence exists.

Therefore, $F(L) = 0 \implies L \text{ is transcendental}$ is a necessary condition, but does not yet yield a contradiction.

---

## C. Derivative-Jet Rigidity and Zero Simplicity

### Theorem (Derivative-Jet Rigidity)
Let $F(z) = a_0 + a_1 e^{\alpha z} + a_2 e^{\beta z}$ with $a_0, a_1, a_2 \in \overline{\mathbb{Q}}^\times$ and incommensurable $\alpha, \beta \in \mathbb{A}_{\mathbb{R}}^\times$.
If $F(L) = 0$, then:
$$F^{(m)}(L) \ne 0 \qquad \text{for every integer } m \ge 1.$$
In particular, $F'(L) \ne 0$, so the zero of $F$ at $L$ is strictly **simple**.

### Proof
For any $m \ge 1$, differentiating $F(z) = a_0 + a_1 e^{\alpha z} + a_2 e^{\beta z}$ $m$ times gives:
$$F^{(m)}(z) = a_1 \alpha^m e^{\alpha z} + a_2 \beta^m e^{\beta z}.$$
Evaluating at $z = L$:
$$F^{(m)}(L) = 0 \cdot 1 + (a_1 \alpha^m) X + (a_2 \beta^m) Y, \qquad X = \tau^\alpha, \; Y = \tau^\beta.$$

This corresponds to the coefficient vector in $\overline{\mathbb{Q}}^3$:
$$v_m = (0, a_1 \alpha^m, a_2 \beta^m).$$

Recall from TASK-TC-030R that the algebraic relation space for $(1, X, Y)$ is defined as:
$$\mathcal{R}_{\alpha, \beta} = \{(c_0, c_1, c_2) \in \overline{\mathbb{Q}}^3 : c_0 + c_1 X + c_2 Y = 0\}.$$
By the relation-space dimension theorem (proved via Gelfond–Schneider):
$$\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1.$$

Now compare $v_m$ with the original relation vector $v_0 = (a_0, a_1, a_2)$:
1. $v_0 \in \mathcal{R}_{\alpha, \beta}$ since $F(L) = 0$.
2. Suppose $F^{(m)}(L) = 0$. Then $v_m \in \mathcal{R}_{\alpha, \beta}$.
3. Are $v_0$ and $v_m$ linearly dependent in $\overline{\mathbb{Q}}^3$?
   Suppose $v_m = \lambda v_0$ for some $\lambda \in \overline{\mathbb{Q}}$.
   Looking at the first coordinate:
   $$0 = \lambda a_0.$$
   Since $a_0 \ne 0$, this forces $\lambda = 0$.
   Looking at the second coordinate:
   $$a_1 \alpha^m = \lambda a_1 = 0 \cdot a_1 = 0.$$
   However, $a_1 \ne 0$ and $\alpha \ne 0$, so $a_1 \alpha^m \ne 0$. Contradiction!
4. Hence $v_0$ and $v_m$ are linearly independent vectors in $\mathcal{R}_{\alpha, \beta}$.
5. This implies $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \ge 2$.
6. But $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1$, a contradiction.

Therefore $F^{(m)}(L) \ne 0$ for every $m \ge 1$.
For $m = 1$, $F'(L) \ne 0$. Since $F(L) = 0$ and $F'(L) \ne 0$, the zero at $L$ has multiplicity exactly 1 (simple). $\blacksquare$

---

## D. Differential-Operator Rigidity

Let $D = \frac{d}{dz}$. For any non-constant polynomial $P(T) = \sum_{j=0}^d c_j T^j \in \overline{\mathbb{Q}}[T]$, the differential operator $P(D) = \sum_{j=0}^d c_j D^j$ acts on $F(z)$ by:
$$P(D)F(z) = a_0 P(0) + a_1 P(\alpha) e^{\alpha z} + a_2 P(\beta) e^{\beta z}.$$

Evaluating at $z = L$:
$$P(D)F(L) = a_0 P(0) \cdot 1 + a_1 P(\alpha) \cdot X + a_2 P(\beta) \cdot Y.$$

### Theorem (Differential-Operator Rigidity)
Suppose $F(L) = 0$ and $P(D)F(L) = 0$ for $P(T) \in \overline{\mathbb{Q}}[T]$.
Then:
$$P(0) = P(\alpha) = P(\beta).$$

### Proof
The relation vector associated with $P(D)F(L) = 0$ is:
$$v_P = (a_0 P(0), a_1 P(\alpha), a_2 P(\beta)) \in \mathcal{R}_{\alpha, \beta}.$$
Since $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1$ and $v_0 = (a_0, a_1, a_2) \in \mathcal{R}_{\alpha, \beta}$ is non-zero, $v_P$ must be a scalar multiple of $v_0$:
$$v_P = \lambda v_0 \quad \text{for some } \lambda \in \overline{\mathbb{Q}}.$$
Equating coordinates:
$$a_0 P(0) = \lambda a_0 \implies \lambda = P(0) \quad (\text{since } a_0 \ne 0),$$
$$a_1 P(\alpha) = \lambda a_1 \implies P(\alpha) = \lambda = P(0) \quad (\text{since } a_1 \ne 0),$$
$$a_2 P(\beta) = \lambda a_2 \implies P(\beta) = \lambda = P(0) \quad (\text{since } a_2 \ne 0).$$
Thus:
$$P(0) = P(\alpha) = P(\beta). \quad \blacksquare$$

### Recovery of Jet Rigidity
For $P(T) = T^m$ ($m \ge 1$), $P(0) = 0$, while $P(\alpha) = \alpha^m \ne 0$ because $\alpha \ne 0$.
The equality $P(0) = P(\alpha)$ fails. Therefore $P(D)F(L) = F^{(m)}(L) \ne 0$ is recovered instantly as a special case.

---

## E. Positive Integer Dilation Exclusion

Let $f(n) = a_0 + a_1 X^n + a_2 Y^n$.
Assume $f(m) = 0$ for some $m \in \mathbb{Z} \setminus \{0\}$.
Define:
$$U = X^m = \tau^{m\alpha}, \qquad V = Y^m = \tau^{m\beta}.$$
Then $a_0 + a_1 U + a_2 V = 0$. Since $a_2 \ne 0$:
$$V = u + v U, \qquad u = -\frac{a_0}{a_2} \ne 0, \quad v = -\frac{a_1}{a_2} \ne 0.$$

Now consider an integer multiplier $k \ge 2$, and suppose $f(km) = 0$:
$$a_0 + a_1 U^k + a_2 V^k = 0.$$
Substitute $V = u + v U$:
$$a_0 + a_1 U^k + a_2 (u + v U)^k = 0.$$
Define the polynomial $P_k(T) \in \overline{\mathbb{Q}}[T]$:
$$P_k(T) = a_0 + a_1 T^k + a_2 (u + v T)^k.$$

### Lemma (Non-vanishing of $P_k$)
For every integer $k \ge 2$, $P_k(T)$ is not the zero polynomial.

### Proof
Expand $a_2 (u + v T)^k$ via the binomial theorem:
$$a_2 (u + v T)^k = a_2 \sum_{j=0}^k \binom{k}{j} u^{k-j} v^j T^j.$$
Consider the coefficient of $T^{k-1}$ ($j = k - 1$):
$$\text{coeff}\left(a_2 (u + v T)^k, T^{k-1}\right) = a_2 \binom{k}{k-1} u^1 v^{k-1} = a_2 k u v^{k-1}.$$
In the remaining terms $a_0 + a_1 T^k$:
- $a_0$ has degree 0.
- $a_1 T^k$ has degree $k$.
Since $k \ge 2$, the degree $k - 1$ satisfies $0 < k - 1 < k$.
Thus $T^{k-1}$ does not appear in $a_0 + a_1 T^k$.
Therefore, the coefficient of $T^{k-1}$ in $P_k(T)$ is precisely:
$$c_{k-1} = a_2 k u v^{k-1}.$$
Since $a_2 \ne 0$, $k \ge 2$, $u \ne 0$, and $v \ne 0$, this coefficient is strictly non-zero:
$$c_{k-1} \ne 0.$$
Hence $P_k(T)$ cannot be the zero polynomial. $\blacksquare$

### Algebraic Consequence
Since $P_k(T) \in \overline{\mathbb{Q}}[T] \setminus \{0\}$ and $P_k(U) = 0$, $U = \tau^{m\alpha}$ is an algebraic number:
$$U \in \overline{\mathbb{Q}}.$$
Then $V = u + v U \in \overline{\mathbb{Q}}$ as well, so:
$$\tau^{m\alpha} \in \overline{\mathbb{Q}} \quad \text{and} \quad \tau^{m\beta} \in \overline{\mathbb{Q}}.$$
By definition of the exceptional exponent group $S_\tau$:
$$m\alpha \in S_\tau, \qquad m\beta \in S_\tau.$$
Since $S_\tau$ is a $\mathbb{Q}$-vector subspace of $\mathbb{R}$ and $m \in \mathbb{Z} \setminus \{0\}$:
$$\alpha \in S_\tau, \qquad \beta \in S_\tau.$$
By the external Gelfond–Schneider dimension theorem (Baker 1975):
$$\dim_{\mathbb{Q}} S_\tau \le 1.$$
Since $\alpha \ne 0$ and $\beta \ne 0$, both belonging to a 1-dimensional $\mathbb{Q}$-subspace forces:
$$\frac{\alpha}{\beta} \in \mathbb{Q},$$
which directly contradicts the hypothesis $\alpha/\beta \notin \mathbb{Q}$!

Therefore:
$$\boxed{f(m) = 0 \implies f(km) \ne 0 \quad \text{for every integer } k \ge 2.}$$

---

## F. Negative Integer Dilation Exclusion

Now let $k = -q$ where $q \ge 1$ is an integer ($k \le -1$).
Suppose $f(-qm) = 0$:
$$a_0 + a_1 U^{-q} + a_2 V^{-q} = 0.$$
Since $U = \tau^{m\alpha} > 0$ and $V = \tau^{m\beta} > 0$, multiply by $U^q V^q \ne 0$:
$$a_0 U^q V^q + a_1 V^q + a_2 U^q = 0.$$
Substitute $V = u + v U$:
$$a_0 U^q (u + v U)^q + a_1 (u + v U)^q + a_2 U^q = 0.$$
Define the polynomial $Q_q(T) \in \overline{\mathbb{Q}}[T]$:
$$Q_q(T) = a_0 T^q (u + v T)^q + a_1 (u + v T)^q + a_2 T^q.$$

### Lemma (Non-vanishing of $Q_q$)
For every integer $q \ge 1$, $Q_q(T)$ is not the zero polynomial.

### Proof
Examine the degrees of each term in $Q_q(T)$:
1. In $a_0 T^q (u + v T)^q$, the highest power of $T$ is $T^q \cdot (v T)^q = v^q T^{2q}$. Its degree is $2q$.
2. In $a_1 (u + v T)^q$, the degree is at most $q$.
3. In $a_2 T^q$, the degree is $q$.
Since $q \ge 1$, $2q > q$.
Thus, no other term can cancel the leading term of degree $2q$.
The leading coefficient of $Q_q(T)$ at $T^{2q}$ is:
$$d_{2q} = a_0 v^q.$$
Since $a_0 \ne 0$ and $v = -a_1/a_2 \ne 0$:
$$d_{2q} \ne 0.$$
Hence $Q_q(T)$ is a non-zero polynomial of degree $2q$. $\blacksquare$

### Algebraic Consequence
Since $Q_q(U) = 0$ with $Q_q(T) \in \overline{\mathbb{Q}}[T] \setminus \{0\}$, $U = \tau^{m\alpha} \in \overline{\mathbb{Q}}$.
As before, this forces $\alpha, \beta \in S_\tau \implies \alpha/\beta \in \mathbb{Q}$, contradiction.

Therefore:
$$\boxed{f(m) = 0 \implies f(km) \ne 0 \quad \text{for every integer } k \le -1.}$$

---

## G. Integer-Dilation Ray Isolation

Combining the positive multiplier exclusion ($k \ge 2$) and negative multiplier exclusion ($k \le -1$):

### Theorem (Integer-Dilation Ray Isolation)
Let $f(n) = a_0 + a_1 X^n + a_2 Y^n$ with $a_0, a_1, a_2 \in \overline{\mathbb{Q}}^\times$ and $\alpha/\beta \notin \mathbb{Q}$.
If $f(m) = 0$ for some non-zero integer $m$, then:
$$\boxed{f(km) \ne 0 \qquad \text{for every integer } k \in \mathbb{Z} \setminus \{0, 1\}.}$$

For the original ambient trinomial relation ($m = 1$, $f(1) = 0$):
$$\boxed{f(n) \ne 0 \qquad \text{for all } n \in \mathbb{Z} \setminus \{0, 1\}.}$$

### Status of $k = 0$
The integer $k = 0$ is **explicitly not excluded** by this theorem:
$$f(0) = a_0 + a_1 + a_2.$$
This is a constant sum of the coefficients. If $a_0 + a_1 + a_2 = 0$, $f(0) = 0$ independently of $\tau, \alpha, \beta$.
However, $f(0) = 0$ and $f(1) = 0$ together cannot force $f(2) = 0$, $f(3) = 0$, or $f(-1) = 0$.

### Comparison with Previous Status
In TASK-TC-030, the finding was `NO_CANONICAL_ORBIT_VANISHING_PROPAGATION`: vanishing at $n = 1$ does not force vanishing at $n = 2$.
TASK-TC-031 **sharply strengthens** this finding to `INTEGER_DILATION_RAY_ISOLATION`: vanishing at $n = 1$ strictly **forbids** vanishing at any other non-zero integer $n \in \mathbb{Z} \setminus \{0, 1\}$.

---

## H. Base-One Lindemann Specialization

For the canonical base-one instance:
$$\alpha = 1, \qquad \beta = \sqrt{2},$$
the generators are:
$$X = \tau = 2\pi, \qquad Y = (2\pi)^{\sqrt{2}}.$$
Here the orbit-isolation contradiction can be obtained **without invoking the external Gelfond–Schneider theorem for $S_\tau$**.

### Proof via Lindemann (1882)
Suppose $f(m) = 0$ and $f(km) = 0$ for $k \ge 2$ or $k \le -1$.
As proved above, the polynomial identity forces:
$$U = X^m = (2\pi)^m \in \overline{\mathbb{Q}}.$$
Since $m \in \mathbb{Z} \setminus \{0\}$, if $(2\pi)^m \in \overline{\mathbb{Q}}$, then $2\pi$ is the root of $T^m - U = 0$ (if $m > 0$) or $U T^{|m|} - 1 = 0$ (if $m < 0$).
Therefore:
$$2\pi \in \overline{\mathbb{Q}} \implies \pi \in \overline{\mathbb{Q}}.$$
However, Lindemann's celebrated 1882 theorem proves unconditionally that $\pi$ is **transcendental**!
This directly contradicts $2\pi \in \overline{\mathbb{Q}}$.

### Evidence Classification
- Classification: `BASE_ONE_ORBIT_ISOLATION_BY_LINDEMANN`.
- Evidence Class: `PROVED_WITH_EXTERNAL_LINDEMANN`.
- This branch is entirely independent of $S_\tau$, depending only on classical 19th-century transcendence of $\pi$.

---

## I. Wronskian and Chebyshev System Structure

Consider the three exponential basis functions:
$$\phi_0(x) = e^{\lambda_0 x}, \qquad \phi_1(x) = e^{\lambda_1 x}, \qquad \phi_2(x) = e^{\lambda_2 x},$$
where $\lambda_0 < \lambda_1 < \lambda_2$ are real exponents formed by ordering $\{0, \alpha, \beta\}$.

### Theorem (Wronskian Formula)
The Wronskian determinant $W(x) = W(\phi_0, \phi_1, \phi_2)(x)$ is given identically by:
$$\boxed{W(x) = e^{(\lambda_0 + \lambda_1 + \lambda_2) x} (\lambda_1 - \lambda_0) (\lambda_2 - \lambda_0) (\lambda_2 - \lambda_1).}$$

### Proof
By definition:
$$W(x) = \det \begin{pmatrix} e^{\lambda_0 x} & e^{\lambda_1 x} & e^{\lambda_2 x} \\ \lambda_0 e^{\lambda_0 x} & \lambda_1 e^{\lambda_1 x} & \lambda_2 e^{\lambda_2 x} \\ \lambda_0^2 e^{\lambda_0 x} & \lambda_1^2 e^{\lambda_1 x} & \lambda_2^2 e^{\lambda_2 x} \end{pmatrix}.$$
Factoring $e^{\lambda_j x}$ from each column:
$$W(x) = e^{(\lambda_0 + \lambda_1 + \lambda_2) x} \det \begin{pmatrix} 1 & 1 & 1 \\ \lambda_0 & \lambda_1 & \lambda_2 \\ \lambda_0^2 & \lambda_1^2 & \lambda_2^2 \end{pmatrix}.$$
The remaining matrix is a classic $3 \times 3$ Vandermonde matrix, whose determinant is:
$$V(\lambda_0, \lambda_1, \lambda_2) = (\lambda_1 - \lambda_0)(\lambda_2 - \lambda_0)(\lambda_2 - \lambda_1).$$
Thus:
$$W(x) = e^{(\lambda_0 + \lambda_1 + \lambda_2) x} (\lambda_1 - \lambda_0) (\lambda_2 - \lambda_0) (\lambda_2 - \lambda_1). \quad \blacksquare$$

### Strict Positivity on $\mathbb{R}$
Since $\lambda_0 < \lambda_1 < \lambda_2$:
$$\lambda_1 - \lambda_0 > 0, \qquad \lambda_2 - \lambda_0 > 0, \qquad \lambda_2 - \lambda_1 > 0.$$
Furthermore, the exponential factor $e^{(\sum \lambda_i) x} > 0$ for every $x \in \mathbb{R}$.
Therefore:
$$\boxed{W(x) > 0 \qquad \text{for all } x \in \mathbb{R}.}$$

Similarly, the lower-order Wronskians are strictly positive:
- $W_1(x) = e^{\lambda_0 x} > 0$.
- $W_2(x) = e^{(\lambda_0 + \lambda_1) x} (\lambda_1 - \lambda_0) > 0$.

---

## J. Real-Zero Count

### Theorem (At Most Two Real Zeros)
Let $F(x) = c_0 e^{\lambda_0 x} + c_1 e^{\lambda_1 x} + c_2 e^{\lambda_2 x}$ with real coefficients $(c_0, c_1, c_2) \ne (0, 0, 0)$ and pairwise distinct real exponents $\lambda_0 < \lambda_1 < \lambda_2$.
Then $F(x)$ has **at most two real zeros**, counted with multiplicity:
$$\boxed{\#\{x \in \mathbb{R} : F(x) = 0\} \le 2.}$$

### Proof
Because the sequential Wronskians $W_1(x), W_2(x), W(x)$ are strictly positive on the entire real line $\mathbb{R}$, the system $\{e^{\lambda_0 x}, e^{\lambda_1 x}, e^{\lambda_2 x}\}$ is an **Extended Complete Chebyshev (ECT) system** on $\mathbb{R}$ in the sense of Karlin & Studden (1966, Chapter 1, Theorem 1.1).
By the fundamental theorem of ECT systems:
> Every non-trivial real linear combination of $n$ elements in an ECT system has at most $n - 1$ real zeros, counting multiplicity.

For $n = 3$, the bound is $3 - 1 = 2$. $\blacksquare$

### Direct Elementary Rolle Proof
Alternatively, divide $F(x)$ by $e^{\lambda_0 x} > 0$:
$$G(x) = c_0 + c_1 e^{(\lambda_1 - \lambda_0) x} + c_2 e^{(\lambda_2 - \lambda_0) x}.$$
$G(x)$ has the identical real zeros and multiplicities as $F(x)$.
Differentiating:
$$G'(x) = c_1 (\lambda_1 - \lambda_0) e^{(\lambda_1 - \lambda_0) x} + c_2 (\lambda_2 - \lambda_0) e^{(\lambda_2 - \lambda_0) x}.$$
Divide $G'(x)$ by $e^{(\lambda_1 - \lambda_0) x} > 0$:
$$H(x) = c_1 (\lambda_1 - \lambda_0) + c_2 (\lambda_2 - \lambda_0) e^{(\lambda_2 - \lambda_1) x}.$$
Since $\lambda_2 - \lambda_1 > 0$, the function $x \mapsto e^{(\lambda_2 - \lambda_1) x}$ is strictly monotonic on $\mathbb{R}$.
Therefore $H(x)$ is strictly monotonic, so $H(x)$ has at most 1 real zero.
Consequently $G'(x)$ has at most 1 real zero.
By Rolle's theorem, between any two zeros of $G$, $G'$ must vanish.
Hence $G(x)$ (and thus $F(x)$) has at most $1 + 1 = 2$ real zeros counting multiplicity. $\blacksquare$

---

## K. Sign-Variation Refinement

The generalized Descartes rule of signs for exponential polynomials (Laguerre 1883, Pólya & Szegő 1925, Karlin & Studden 1966) gives a sharper bound based on the number of sign variations $v(c_0, c_1, c_2)$ of the coefficients:

| Sign Pattern | Sign Variations $v$ | Maximum Real Zeros (with multiplicity) | Behavior |
|:---|:---:|:---:|:---|
| $(+, +, +)$ or $(-, -, -)$ | 0 | **0** | $F(x)$ has constant sign everywhere; zero impossible. |
| $(+, +, -)$ or $(+, -, -)$ or $(-, -, +)$ or $(-, +, +)$ | 1 | **at most 1** | $G'(x)$ has no zeros (same-sign terms); $G(x)$ is strictly monotonic. |
| $(+, -, +)$ or $(-, +, -)$ | 2 | **at most 2** | Full Chebyshev bound applies; at most 2 real zeros. |

### Consequence for Minimal Ambient Relation
For positive generators $X = \tau^\alpha > 0, Y = \tau^\beta > 0$, TASK-TC-030 proved that mixed signs are necessary for $a_0 + a_1 X + a_2 Y = 0$.
The sign-variation theorem shows:
- If the sign pattern has $v = 1$ relative to the exponent order, $F(x)$ has **at most one real zero**.
- If $F(L) = 0$, $L$ is the **unique real zero** of $F$ on all of $\mathbb{R}$!
- If the sign pattern has $v = 2$, $F(x)$ has at most two real zeros.

---

## L. Functional-Transcendence Firewall

A critical epistemic requirement of TASK-TC-031 is to prevent invalid inferences from functional transcendence theorems to the arithmetic evaluation at $L = \log(2\pi)$:

| Theorem | Hypotheses & Domain | What it Proves Functionally | Does it Specialize to $z = \log(2\pi)$? | Obstruction |
|:---|:---|:---|:---:|:---|
| **Ax–Schanuel** (Ax 1971) | Analytic functions $f_1, \dots, f_n$ over $\mathbb{C}$ | $\operatorname{trdeg}_{\mathbb{C}} \mathbb{C}(z, e^{\alpha z}, e^{\beta z}) \ge 2$ over $\mathbb{C}(z)$ | **NO** | Functional transcendence over $\mathbb{C}(z)$ requires the full **arithmetic Schanuel conjecture** to specialize at specific complex numbers. |
| **Differential Galois Theory** (Kolchin 1973) | Differential field $(\mathbb{C}(z), d/dz)$ | $e^{\alpha z}$ and $e^{\beta z}$ are algebraically independent over $\mathbb{C}(z)$ | **NO** | Differential automorphisms do not constrain evaluations at transcendental points. |
| **Siegel–Shidlovskii Theory** (1929/1959) | $E$-functions satisfying linear ODEs | Values at algebraic points have transcendence degree matching the functions | **NO** | Applies strictly to **algebraic arguments** $z \in \overline{\mathbb{Q}}$. Here $z = L = \log(2\pi)$ is not known algebraic (and by Section B, is transcendental if a relation holds). |

**Firewall Classification**: `FUNCTIONAL_RESULT_DOES_NOT_SPECIALIZE_AUTOMATICALLY`.  
Functional transcendence does not prove that $a_0 + a_1 \tau^\alpha + a_2 \tau^\beta \ne 0$.

---

## M. Exact Remaining Open Relation

The exact open mathematical frontier is:

$$\boxed{\exists? \; a_0, a_1, a_2 \in \overline{\mathbb{Q}}^\times, \quad \alpha, \beta \in \mathbb{A}_{\mathbb{R}}^\times, \quad \frac{\alpha}{\beta} \notin \mathbb{Q} \quad : \quad a_0 + a_1 (2\pi)^\alpha + a_2 (2\pi)^\beta = 0.}$$

Every deduction in TASK-TC-031 operates conditional on the hypothetical existence of such a relation:
$$\begin{aligned}
F(L) = 0 &\Longrightarrow L = \log(2\pi) \text{ is transcendental}, \\
F(L) = 0 &\Longrightarrow F^{(m)}(L) \ne 0 \quad (m \ge 1), \\
F(L) = 0 &\Longrightarrow F(nL) \ne 0 \quad (n \in \mathbb{Z} \setminus \{0, 1\}), \\
F(L) = 0 &\Longrightarrow F \text{ has at most two real zeros on } \mathbb{R}.
\end{aligned}$$

A hypothetical trinomial zero at $L$ is therefore **not** part of a dense cluster or periodic orbit:
It is an **arithmetically isolated, strictly simple, non-recurring exponential-polynomial zero**.

Whether even one such event exists in nature remains **OPEN**.

---

## N. Implications for Transcendental Continuation (TC)

1. **Sharpened Trinomial Frontier**:
   The trinomial frontier has advanced from mere non-propagation (`NO_CANONICAL_ORBIT_VANISHING_PROPAGATION` in TASK-TC-030) to **integer-dilation ray isolation** (`INTEGER_DILATION_RAY_ISOLATION` in TASK-TC-031).
2. **Exclusion of Higher Monomial Relations**:
   Any ambient relation cannot repeat along any integer dilation ray $n = 2, 3, \dots$ or $n = -1, -2, \dots$.
3. **Jet Rigidity**:
   Local Taylor series expansions of $F$ at $L$ are non-degenerate: no higher-order vanishing can occur.
4. **Finite Real Zeros**:
   By the Chebyshev system theorem, $F(x)$ cannot vanish more than twice on the entire real line.

---

## O. Non-Implications for the Riemann Hypothesis (RH)

1. **`NO_ZETA_TO_KERNEL_BRIDGE_FOUND` Preserved**:
   No connection exists between ambient-kernel trinomial relations and nontrivial zeros $\rho$ of $\zeta(s)$.
2. **`NO_RH_IMPLICATION` Preserved**:
   Proving that a hypothetical trinomial relation has isolated dilation orbits and simple jets has **zero logical consequence** for the Riemann Hypothesis or the critical line $\operatorname{Re}(s) = 1/2$.
3. **No Unconditional Nonexistence Claim**:
   The existence of the trinomial relation is **not** refuted. The principal classification remains `EXPONENTIAL_POLYNOMIAL_FRONTIER_SHARPENED_EXISTENCE_OPEN`.

---

## P. Formalization Summary

- **Lean 4 Module**: `formal/RiemannScope/ExponentialPolynomialRigidity.lean`
- **Root Import**: `formal/RiemannScope.lean`
- **Total Project Theorems**: 515 (an increase of 14 theorems from 501 in TASK-TC-030R)
- **Lean Build**: 0 errors, 0 warnings, 0 sorries (`✔ Built RiemannScope.ExponentialPolynomialRigidity`)
- **Key Formalized Theorems**:
  - `trinomial_derivative_relation_vector`
  - `trinomial_derivative_relation_not_proportional`
  - `differential_operator_constant_support_values`
  - `integer_dilation_positive_polynomial_identity_k2`
  - `integer_dilation_positive_polynomial_identity_k3`
  - `integer_dilation_positive_nonzero_coeff_k2`
  - `integer_dilation_positive_nonzero_coeff_k3`
  - `integer_dilation_negative_polynomial_identity_q1`
  - `integer_dilation_negative_polynomial_identity_q2`
  - `integer_dilation_negative_leading_coeff_q1`
  - `integer_dilation_negative_leading_coeff_q2`
  - `three_exponential_wronskian_algebraic_identity`
  - `three_exponential_wronskian_pos_of_ordered`
  - `base_one_second_dilation_quadratic_identity`
