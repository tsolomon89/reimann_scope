# TASK-TC-031R: Exponential-Polynomial Evidence Scope Alignment and Chebyshev ECT Hierarchy Audit

## Status
- **Principal Classification**: `EXPONENTIAL_POLYNOMIAL_FRONTIER_SHARPENED_EXISTENCE_OPEN`
- **Corrective Mission**: TASK-TC-031R
- **Substantive Commit Target**: Commit 1 of TASK-TC-031R
- **Evidence Alignment Status**: Fully reconciled across Lean 4, SymPy, Arb, and canonical literature citations.

---

## 1. Executive Summary of Corrective Action

An independent review of TASK-TC-031 identified that while the paper-level mathematics, Python symbolic/interval engines, and 14 compiled Lean declarations were mathematically sound, the completion report presentation suffered from two categories of defects:
1. **Misstated Lean Scope**: Overstated Lean theorem coverage by using mathematical paper theorem names (`lindemann_weierstrass_necessity`, `trinomial_zero_simple`, `positive_derivative_jets_nonzero`, `differential_operator_rigidity`, `integer_dilation_ray_isolation`, `base_one_orbit_isolation_by_lindemann`, `at_most_two_real_exponential_polynomial_zeros`) rather than the actual committed Lean theorem identifiers. The Lean module formalizes the exact **algebraic skeleton**, while number-theoretic and analytic foundations (Lindemann–Weierstrass 1885, Gelfond–Schneider 1934, Karlin–Studden 1966) remain paper proofs and external theorems.
2. **Presentation Defects**:
   - A flawed derivative-jet deduction sentence in the report summary that claimed $(2\pi)^{\alpha-\beta} \in \overline{\mathbb{Q}}$ contradicts $\alpha/\beta \notin \mathbb{Q}$ by itself (which is invalid because a single irrational direction is compatible with $\dim_{\mathbb{Q}} S_\tau \le 1$). The correct proof is the relation-space dimension bound $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1$.
   - Positive-dilation coefficient discussion that vacillated between the top-degree $U^k$ coefficient and the $U^{k-1}$ coefficient, whereas $[T^{k-1}]P_k(T) = a_2 k u v^{k-1} \ne 0$ alone establishes non-vanishing of $P_k(T)$.
   - Incomplete ECT Wronskian hierarchy (formalizing only $W_2$ rather than all successive Wronskians $W_0, W_1, W_2$).

TASK-TC-031R completely resolves each of these defects:
- Formalizes the complete successive Wronskian hierarchy $W_0, W_1, W_2 > 0$ in Lean 4 (adding 3 new theorems, bringing the module to 17 theorems and the project total to **518 compiled declarations, 0 sorry**).
- Establishes a rigorous evidence classification mapping table separating Lean algebraic lemmas, paper derivations, and external theorems.
- Corrects all derivative-jet, positive-dilation, and ECT citations across repository documentation.

---

## 2. Complete Mapping of Lean 4 Formal Declarations

The Lean 4 module `formal/RiemannScope/ExponentialPolynomialRigidity.lean` contains exactly 17 verified theorems (0 sorry):

| # | Lean 4 Theorem Identifier | Exact Mathematical Scope Formalized in Lean | Full Result Epistemic Role |
|---|---|---|---|
| 1 | `trinomial_derivative_relation_vector` | $0 \cdot 1 + (a_1 \alpha_m) X + (a_2 \beta_m) Y = a_1 \alpha_m X + a_2 \beta_m Y$ | Algebraic identity of derivative-jet evaluation |
| 2 | `trinomial_derivative_relation_not_proportional` | $(0, a_1 \alpha_m, a_2 \beta_m)$ is not proportional to $(a_0, a_1, a_2)$ when $a_0 \ne 0$ and $a_1 \alpha_m \ne 0$ | Linear independence in relation space $\mathcal{R}_{\alpha, \beta}$ |
| 3 | `differential_operator_constant_support_values` | $(a_0 p_0, a_1 p_\alpha, a_2 p_\beta) = c(a_0, a_1, a_2)$ with $a_j \ne 0$ forces $p_0 = p_\alpha = p_\beta = c$ | Differential-operator rigidity proportionality |
| 4 | `integer_dilation_positive_polynomial_identity_k2` | $a_0 + a_1 U^2 + a_2(u + v U)^2 = (a_0 + a_2 u^2) + (2 a_2 u v) U + (a_1 + a_2 v^2) U^2$ | $k=2$ positive dilation polynomial algebra |
| 5 | `integer_dilation_positive_polynomial_identity_k3` | $a_0 + a_1 U^3 + a_2(u + v U)^3$ expands identically with distinguished term $(3 a_2 u v^2) U^2$ | $k=3$ positive dilation polynomial algebra |
| 6 | `integer_dilation_positive_nonzero_coeff_k2` | $2 a_2 u v \ne 0$ when $a_2, u, v \ne 0$ | Linear coefficient of $P_2(T)$ is non-zero |
| 7 | `integer_dilation_positive_nonzero_coeff_k3` | $3 a_2 u v^2 \ne 0$ when $a_2, u, v \ne 0$ | Quadratic coefficient of $P_3(T)$ is non-zero |
| 8 | `integer_dilation_negative_polynomial_identity_q1` | $a_0 U V + a_1 V + a_2 U = (a_1 u) + (a_0 u + a_1 v + a_2) U + (a_0 v) U^2$ | $q=1$ negative dilation polynomial algebra |
| 9 | `integer_dilation_negative_polynomial_identity_q2` | Cleared denominator form expands identically with leading term $(a_0 v^2) U^4$ | $q=2$ negative dilation polynomial algebra |
| 10 | `integer_dilation_negative_leading_coeff_q1` | $a_0 v \ne 0$ when $a_0, v \ne 0$ | Leading coefficient of $Q_1(T)$ is non-zero |
| 11 | `integer_dilation_negative_leading_coeff_q2` | $a_0 v^2 \ne 0$ when $a_0, v \ne 0$ | Leading coefficient of $Q_2(T)$ is non-zero |
| 12 | `one_exponential_wronskian_pos` | $W_0(x) = E_0 > 0$ for $E_0 > 0$ | Order 0 Wronskian of ECT hierarchy |
| 13 | `two_exponential_wronskian_algebraic_identity` | $E_0 (l_1 E_1) - E_1 (l_0 E_0) = (E_0 E_1)(l_1 - l_0)$ | Order 1 Wronskian factorization |
| 14 | `two_exponential_wronskian_pos_of_ordered` | $0 < (E_0 E_1)(l_1 - l_0)$ for $E_0, E_1 > 0$ and $l_0 < l_1$ | Order 1 Wronskian strict positivity |
| 15 | `three_exponential_wronskian_algebraic_identity` | $3 \times 3$ Wronskian determinant factors identically into $(E_0 E_1 E_2) \prod_{i<j} (l_j - l_i)$ | Order 2 Wronskian factorization |
| 16 | `three_exponential_wronskian_pos_of_ordered` | $0 < (E_0 E_1 E_2) \prod_{i<j} (l_j - l_i)$ for $E_j > 0$ and $l_0 < l_1 < l_2$ | Order 2 Wronskian strict positivity |
| 17 | `base_one_second_dilation_quadratic_identity` | Second dilation equation for $U = 2\pi$ rearranges to standard quadratic | Base-one quadratic form algebra |

---

## 3. Epistemic Classification of Full Mathematical Results

| Full Mathematical Result | True Evidence Classification | Lean Formalization Role | External Dependency |
|---|---|---|---|
| **$\log(2\pi)$ Necessity** | `PROVED_WITH_EXTERNAL_LINDEMANN_WEIERSTRASS` | None (pure reduction) | Lindemann–Weierstrass Theorem (1885) |
| **All Derivative Jets Non-Zero** ($m \ge 1$) | `PROVED_PAPER_DERIVATION + EXTERNAL_GELFOND_SCHNEIDER` | Proves $v_m$ non-proportional to $v_0$ (`trinomial_derivative_relation_not_proportional`) | Gelfond–Schneider Theorem (1934) / Baker (1975) for $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1$ |
| **Simple Zero at $L$** ($F'(L) \ne 0$) | `PROVED_PAPER_DERIVATION + EXTERNAL_GELFOND_SCHNEIDER` | $m=1$ instance of non-proportionality | Gelfond–Schneider |
| **Differential-Operator Rigidity** | `PROVED_PAPER_DERIVATION + EXTERNAL_GELFOND_SCHNEIDER` | Proves support value equality from proportionality (`differential_operator_constant_support_values`) | Gelfond–Schneider |
| **Integer-Dilation Ray Isolation** ($\forall k \in \mathbb{Z} \setminus \{0, 1\}$) | `PROVED_PAPER_DERIVATION + EXTERNAL_GELFOND_SCHNEIDER` | Proves polynomial identities & non-zero coefficients for $k=2,3$ and $q=1,2$ | Gelfond–Schneider (forces $U \in \overline{\mathbb{Q}} \implies \alpha, \beta \in S_\tau$) |
| **Base-One Orbit Isolation** | `PROVED_WITH_EXTERNAL_LINDEMANN` | Proves quadratic identity for $k=2$ (`base_one_second_dilation_quadratic_identity`) | Lindemann (1882) transcendence of $\pi$ |
| **At Most Two Real Zeros** | `PROVED_WITH_EXTERNAL_CHEBYSHEV_THEOREM` | Proves all successive Wronskians $W_0, W_1, W_2 > 0$ (`one_exponential_wronskian_pos`, `two_...`, `three_...`) | Karlin & Studden (1966, Chapter XI, Theorem 1.1); Pólya & Szegő (1925, Part V, No. 75) |

---

## 4. Rigorous Formulation of Derivative-Jet Rigidity

### The Defect in the Preliminary Completion Report
The preliminary completion report contained an abbreviated proof statement:
> "$F^{(m)}(L) = 0 \implies (2\pi)^{\alpha-\beta} \in \overline{\mathbb{Q}}$, contradicting $\alpha/\beta \notin \mathbb{Q}$."

This deduction is **invalid as stated**. A single algebraic relation $(2\pi)^{\alpha-\beta} \in \overline{\mathbb{Q}}$ implies $\alpha - \beta \in S_\tau$. The Gelfond–Schneider theorem guarantees $\dim_{\mathbb{Q}} S_\tau \le 1$. If $S_\tau$ were non-trivial, it could contain a single non-zero direction $\theta_0 \in \mathbb{A}_{\mathbb{R}} \setminus \mathbb{Q}$. Then $\alpha - \beta \in S_\tau$ simply means $\alpha - \beta = q \theta_0$ for some $q \in \mathbb{Q}$, which does **not** contradict the irrational ratio condition $\alpha/\beta \notin \mathbb{Q}$.

### The Correct Relation-Space Proof
The valid mathematical proof proceeds strictly through the relation space $\mathcal{R}_{\alpha, \beta}$:
1. Let $\mathcal{R}_{\alpha, \beta} = \{(c_0, c_1, c_2) \in \overline{\mathbb{Q}}^3 : c_0 + c_1 X + c_2 Y = 0\}$ where $X = \tau^\alpha, Y = \tau^\beta$.
2. By the relation-space dimension theorem (TASK-TC-030R), $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1$. (Any two independent linear relations on $(1, X, Y)$ allow solving for $X$ and $Y$ by Cramer's rule, forcing both $X \in \overline{\mathbb{Q}}$ and $Y \in \overline{\mathbb{Q}}$, which means $\alpha \in S_\tau$ and $\beta \in S_\tau$. Since $\dim_{\mathbb{Q}} S_\tau \le 1$ and $\alpha, \beta \ne 0$, this would force $\alpha/\beta \in \mathbb{Q}$, contradicting incommensurability).
3. The hypothetical relation $F(L) = 0$ gives $v_0 = (a_0, a_1, a_2) \in \mathcal{R}_{\alpha, \beta}$ with $a_0 \ne 0$.
4. The $m$-th derivative relation $F^{(m)}(L) = 0$ gives $v_m = (0, a_1 \alpha^m, a_2 \beta^m) \in \mathcal{R}_{\alpha, \beta}$.
5. In Lean theorem `trinomial_derivative_relation_not_proportional`, we formally prove that $v_m$ cannot be a scalar multiple of $v_0$ because its first coordinate is $0$ while $a_0 \ne 0$, yet its second coordinate $a_1 \alpha^m \ne 0$.
6. Thus $v_0$ and $v_m$ are linearly independent vectors in $\mathcal{R}_{\alpha, \beta}$.
7. This forces $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \ge 2$, contradicting $\dim \le 1$.
8. Therefore $F^{(m)}(L) \ne 0$ for all $m \ge 1$. In particular, $F'(L) \ne 0$, so any zero is simple. $\blacksquare$

---

## 5. Clean Positive-Dilation Coefficient Presentation

### The Defect in the Preliminary Completion Report
The preliminary report vacillated between analyzing the top-degree $U^k$ coefficient (which is $a_1 + a_2 v^k$) and noting that it might cancel, then shifting to the $U^{k-1}$ coefficient.

### The Clean Proof
There is no reason to analyze the top-degree coefficient $U^k$ at all. The proof requires only demonstrating that $P_k(T) \in \overline{\mathbb{Q}}[T]$ is a non-zero polynomial:

1. Let $f(m) = a_0 + a_1 U + a_2 V = 0$ with $U = X^m, V = Y^m$. Then $V = u + v U$ where $u = -a_0/a_2 \ne 0$ and $v = -a_1/a_2 \ne 0$.
2. For $k \ge 2$, the equation $f(km) = a_0 + a_1 U^k + a_2 V^k = 0$ becomes $P_k(U) = 0$, where:
   $$P_k(T) = a_0 + a_1 T^k + a_2(u + v T)^k.$$
3. In the binomial expansion $a_2(u + v T)^k = a_2 \sum_{j=0}^k \binom{k}{j} u^{k-j} v^j T^j$, the coefficient of $T^{k-1}$ is:
   $$[T^{k-1}] a_2(u + v T)^k = a_2 \binom{k}{k-1} u^1 v^{k-1} = a_2 k u v^{k-1}.$$
4. In the remaining terms $a_0 + a_1 T^k$, the exponents are $0$ and $k$. Since $k \ge 2$, the integer $k - 1$ satisfies $0 < k - 1 < k$.
5. Thus neither $a_0$ nor $a_1 T^k$ contributes to the $T^{k-1}$ term.
6. Therefore:
   $$\boxed{[T^{k-1}] P_k(T) = a_2 k u v^{k-1} \ne 0.}$$
7. Since $a_2 \ne 0$, $k \ge 2$, $u \ne 0$, and $v \ne 0$, this coefficient is strictly non-zero.
8. A polynomial with a non-zero coefficient at degree $k - 1 \ge 1$ cannot be the zero polynomial.
9. Hence $P_k(T) \in \overline{\mathbb{Q}}[T] \setminus \{0\}$, forcing $U = \tau^{m\alpha} \in \overline{\mathbb{Q}}$, which by Gelfond–Schneider completes the contradiction. $\blacksquare$

---

## 6. Precise Chebyshev ECT Dependency & Successive Wronskians

### Definition (Extended Complete Chebyshev System)
Let $\{u_0(x), u_1(x), \dots, u_n(x)\}$ be $n$-times continuously differentiable functions on an interval $I$.
The system is an **Extended Complete Chebyshev (ECT) system** on $I$ (Karlin & Studden 1966, Chapter XI, Theorem 1.1, p. 376) if and only if all the successive Wronskian determinants:
$$W_k(x) = W(u_0, u_1, \dots, u_k)(x) = \det \left[ u_j^{(i)}(x) \right]_{0 \le i, j \le k} > 0 \quad (\text{or } < 0)$$
for all $x \in I$ and all $k = 0, 1, \dots, n$.

### Theorem (Zero Count on ECT Systems)
If $\{u_0, \dots, u_n\}$ is an ECT system on $I$, then every non-trivial real linear combination $\sum_{j=0}^n c_j u_j(x)$ has at most $n$ zeros on $I$, counted with multiplicity (Karlin & Studden 1966, Theorem 1.1; Pólya & Szegő 1925, Part V, No. 75).

### Application to the Trinomial Basis $\{e^{\lambda_0 x}, e^{\lambda_1 x}, e^{\lambda_2 x}\}$
For ordered real exponents $\lambda_0 < \lambda_1 < \lambda_2$:
1. **Order 0**:
   $$W_0(x) = u_0(x) = e^{\lambda_0 x} > 0 \quad \forall x \in \mathbb{R}.$$
   *(Lean 4 theorem: `one_exponential_wronskian_pos`)*
2. **Order 1**:
   $$W_1(x) = \det \begin{pmatrix} e^{\lambda_0 x} & e^{\lambda_1 x} \\ \lambda_0 e^{\lambda_0 x} & \lambda_1 e^{\lambda_1 x} \end{pmatrix} = e^{(\lambda_0 + \lambda_1)x} (\lambda_1 - \lambda_0) > 0 \quad \forall x \in \mathbb{R}.$$
   *(Lean 4 theorems: `two_exponential_wronskian_algebraic_identity`, `two_exponential_wronskian_pos_of_ordered`)*
3. **Order 2**:
   $$W_2(x) = \det \begin{pmatrix} e^{\lambda_0 x} & e^{\lambda_1 x} & e^{\lambda_2 x} \\ \lambda_0 e^{\lambda_0 x} & \lambda_1 e^{\lambda_1 x} & \lambda_2 e^{\lambda_2 x} \\ \lambda_0^2 e^{\lambda_0 x} & \lambda_1^2 e^{\lambda_1 x} & \lambda_2^2 e^{\lambda_2 x} \end{pmatrix} = e^{(\lambda_0 + \lambda_1 + \lambda_2)x} (\lambda_1 - \lambda_0)(\lambda_2 - \lambda_0)(\lambda_2 - \lambda_1) > 0 \quad \forall x \in \mathbb{R}.$$
   *(Lean 4 theorems: `three_exponential_wronskian_algebraic_identity`, `three_exponential_wronskian_pos_of_ordered`)*

Because all successive Wronskians $W_0(x), W_1(x), W_2(x)$ are strictly positive everywhere on $\mathbb{R}$, $\{e^{\lambda_0 x}, e^{\lambda_1 x}, e^{\lambda_2 x}\}$ forms a verified ECT system on $\mathbb{R}$.
Therefore, $F(x) = a_0 + a_1 e^{\alpha x} + a_2 e^{\beta x}$ has at most $3 - 1 = 2$ real zeros on $\mathbb{R}$, counted with multiplicity. $\blacksquare$

---

## 7. Retained Research Boundaries

1. **`EXPONENTIAL_POLYNOMIAL_FRONTIER_SHARPENED_EXISTENCE_OPEN` Preserved**:
   No nonexistence theorem has been obtained for the minimal trinomial relation $a_0 + a_1(2\pi)^\alpha + a_2(2\pi)^\beta = 0$. The existence question remains strictly open in transcendental number theory.
2. **`NO_ZETA_TO_KERNEL_BRIDGE_FOUND` Preserved**:
   No connection has been found between ambient-kernel trinomial relations and non-trivial zeros $\rho$ of the Riemann zeta function.
3. **`NO_RH_IMPLICATION` Preserved**:
   Proving that a hypothetical trinomial relation has isolated dilation orbits and simple jets has zero logical consequence for the Riemann Hypothesis.
