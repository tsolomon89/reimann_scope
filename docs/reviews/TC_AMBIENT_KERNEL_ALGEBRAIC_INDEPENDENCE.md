# TC Ambient Realization Kernel, Algebraic-Power Independence, and Zeta-Bridge Firewall

**Task**: TASK-TC-028 / TASK-TC-028R  
**Date**: October 9, 2026  
**Status**: COMPLETE (REPAIRED)  
**Primary Classification**: `FINITE_KERNEL_REDUCES_TO_ALGEBRAIC_INDEPENDENCE`  
**Secondary Classifications**:
- `RANK_ZERO_TRIVIAL`
- `RANK_ONE_KERNEL_CLASSIFIED`
- `ONE_EXCEPTIONAL_Q_DIRECTION_ONLY`
- `HIGHER_RANK_ALGEBRAIC_INDEPENDENCE_OPEN`
- `SCHANUEL_IMPLIES_FULL_FINITE_RANK_INJECTIVITY`
- `PAIRWISE_TRANSCENDENCE_INSUFFICIENT`
- `NO_ZETA_TO_KERNEL_BRIDGE_FOUND`
- `ZERO_ARITHMETIC_TRACK_LOGICALLY_DISTINCT`
- `CERTIFIED_FINITE_RELATION_EXCLUSION`
- `LEAN_PROVED_ALGEBRAIC_SKELETON`

---

## Executive Summary

TASK-TC-025 through TASK-TC-027R completed the canonical formulation of Transcendental Continuation (TC), establishing the ring equivalence $\operatorname{GradeFiber}(K) \simeq_{\mathrm{ring}} \mathbb{Z}$ and proving that multi-grade transfers are strictly functorial with trivial cocycles ($c(M, J)c(J, K) = c(M, K)$). All prospective TC-to-RH mechanisms based on unit rescaling, local-germ covariance, grade-character unitarity, and moving-zero pullbacks $\zeta(\tau^{-K}s)$ have been formally settled and frozen.

TASK-TC-028 and TASK-TC-028R investigate the remaining open TC-specific mathematical structure: the **ambient realization evaluation map**
$$\operatorname{ev}_\tau: \mathbb{A}_{\mathbb{R}}[\mathbb{A}_{\mathbb{R}}] \longrightarrow \mathbb{R}, \qquad \tau = 2\pi,$$
and its complex algebraic coefficient counterpart $\operatorname{ev}_\tau: \overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}] \longrightarrow \mathbb{C}$, evaluating finite linear combinations:
$$\operatorname{ev}_\tau\left(\sum_{j=1}^m a_j [K_j]\right) = \sum_{j=1}^m a_j (2\pi)^{K_j}, \qquad a_j \in \overline{\mathbb{Q}}, \; K_j \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}.$$

This sprint rigorously establishes:
1. **Support Translation Invariance**: Kernel vanishing depends strictly on affine differences among grades ($\sum a_j \tau^{K_j} = 0 \iff \sum a_j \tau^{K_j - K_0} = 0$).
2. **Rational Support Rank $r(S)$**: Defined as $\dim_{\mathbb{Q}} \operatorname{span}_{\mathbb{Q}} \{K_j - K_0\}$, base-grade invariant, and computed via exact algebraic number field primitive elements.
3. **Exact Rank-Zero Classification ($r=0$)**: Vanishes if and only if $\sum a_j = 0$ (trivial coefficient cancellation within a single grade).
4. **Exact Rank-One Classification ($r=1$)**: Injectivity on a rational line $\overline{\mathbb{Q}}[\mathbb{Q}\alpha]$ holds if and only if $\alpha \notin S_\tau = \{\alpha \in \mathbb{A}_{\mathbb{R}} : \tau^\alpha \in \overline{\mathbb{Q}}\}$. If $\alpha \in S_\tau$, an explicit non-zero kernel witness is $[\alpha] - A[0]$ with $A = \tau^\alpha \in \overline{\mathbb{Q}}$. By external Gelfond–Schneider, $\dim_{\mathbb{Q}} S_\tau \le 1$, so at most one rational line can contain non-trivial kernel elements.
5. **Canonical Reduction for Higher Rank ($r \ge 2$)**: Finite evaluation kernel relations of rational support rank $r$ reduce precisely to multivariate algebraic-dependence relations among $r$ algebraic powers of $2\pi$.
6. **Corrected & Strengthened Schanuel Theorem**: A rigorous two-case application of Schanuel's conjecture proves:
   $$\operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}\left(\tau^{\alpha_1}, \dots, \tau^{\alpha_r}\right) = r.$$
   Consequently, **Schanuel's conjecture implies full finite-rank injectivity of $\operatorname{ev}_\tau$ on every finite algebraic-grade support**.
7. **Arithmetically Precise Firewall Audit**: $\zeta(2n+1)$ and $\Gamma(\rho)$ are classified as `ALGEBRAICITY_UNPROVED` (inadmissible as proved algebraic coefficients, but not proved non-algebraic; irrational does not mean transcendental). The audit finding `NO_ZETA_TO_KERNEL_BRIDGE_FOUND` establishes that examined familiar zeta structures furnish no bridge, without asserting a nonexistence theorem.
8. **Clarified Base-Grade Arithmetic**: Grade $1 \in \mathbb{A}_{\mathbb{R}}$ is algebraic; what is transcendental is $\tau^1 = 2\pi$, equivalently $1 \notin S_\tau$.
9. **Rigorous Scope Delineation**:
   - `LEAN_PROVED`: The algebraic skeleton and low-arity lemmas in `RiemannScope.AmbientKernel` (2- and 3-term translation invariance, 2- and 3-term rank-zero cancellation, real affine difference identity, bivariate monomial clearing identity, and abstract 2-term impossibility).
   - `PROVED_PAPER_DERIVATION`: Full group algebra $\overline{\mathbb{Q}}[\mathbb{Q}\alpha]$ injectivity, equality of $\mathbb{Q}$-spans and dimensions, multivariate algebraic-dependence equivalence, and the two-case Schanuel conditional theorem.

---

## Section A. Exact Evaluation-Map Definition

Let $\mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$ denote the field of real algebraic numbers, and $\tau = 2\pi$. The group algebra $\overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}]$ has basis elements $[K]$ for $K \in \mathbb{A}_{\mathbb{R}}$, with group multiplication $[K][J] = [K + J]$.

The ambient evaluation map is the algebra homomorphism:
$$\operatorname{ev}_\tau: \overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}] \longrightarrow \mathbb{C}, \qquad [K] \longmapsto \tau^K = (2\pi)^K.$$
Restricted to real algebraic coefficients, it maps $\mathbb{A}_{\mathbb{R}}[\mathbb{A}_{\mathbb{R}}] \to \mathbb{R}$.

For a finite formal sum $F = \sum_{j=1}^m a_j [K_j]$ with distinct grades $K_j \in \mathbb{A}_{\mathbb{R}}$ and non-zero algebraic coefficients $a_j \in \overline{\mathbb{Q}} \setminus \{0\}$, the support is:
$$\operatorname{supp}(F) = \{K_1, \dots, K_m\}.$$
An element $F$ lies in the ambient kernel $\ker(\operatorname{ev}_\tau)$ if and only if:
$$\boxed{\sum_{j=1}^m a_j (2\pi)^{K_j} = 0.}$$

Canonical preprocessing rules:
- Combine equal grades: $\sum_{K_j = K} a_j [K] \mapsto (\sum a_j)[K]$.
- Discard zero coefficients: drop terms where $a_j = 0$.
- Ensure distinct, sorted support.

---

## Section B. Support Translation Invariance

**Theorem (Support Translation Invariance)**:  
*For any reference grade $K_0 \in \mathbb{A}_{\mathbb{R}}$,*
$$\sum_{j=1}^m a_j \tau^{K_j} = \tau^{K_0} \sum_{j=1}^m a_j \tau^{K_j - K_0}.$$
*Because $\tau = 2\pi > 0$, the scalar factor $\tau^{K_0} > 0$ never vanishes. Consequently,*
$$\boxed{\sum_{j=1}^m a_j \tau^{K_j} = 0 \iff \sum_{j=1}^m a_j \tau^{K_j - K_0} = 0.}$$

*Proof*: By the real power addition law for positive base $\tau > 0$, $\tau^{K_j} = \tau^{K_0 + (K_j - K_0)} = \tau^{K_0} \tau^{K_j - K_0}$. Factoring $\tau^{K_0}$ out of the finite sum gives the identity. Since $\tau^{K_0} \ne 0$, the product vanishes if and only if the sum of translated terms vanishes. $\blacksquare$

*Lean 4 Verification*: Formalized in `RiemannScope.AmbientKernel` as `tau_pow_translation`, `sum_tau_pow_translation_two`, `sum_tau_pow_translation_three`, `sum_tau_pow_zero_iff_translated_zero_two`, and `sum_tau_pow_zero_iff_translated_zero_three`.

*Corrollary*: Ambient kernel questions are strictly affine: they depend solely on relative grade differences $\{K_j - K_0\}$, completely invariant under rigid translations of the support.

---

## Section C. Rational Support Rank

**Definition (Rational Support Rank)**:  
Let $S = \{K_1, \dots, K_m\} \subset \mathbb{A}_{\mathbb{R}}$ be a finite support set. Choose a base grade $K_0 \in S$. The rational support rank $r(S)$ is:
$$\boxed{r(S) = \dim_{\mathbb{Q}} \operatorname{span}_{\mathbb{Q}} \{ K_j - K_0 : j = 1, \dots, m \}.}$$

**Theorem (Base-Grade Independence)**:  
*The rational support rank $r(S)$ is independent of the choice of base grade $K_0 \in S$.*

*Proof*: Let $K_0, K_0' \in S$ be two base grades. For any $K \in S$:
$$K - K_0' = (K - K_0) - (K_0' - K_0).$$
Since $K_0' \in S$, the difference $(K_0' - K_0)$ lies in $V = \operatorname{span}_{\mathbb{Q}} \{K_j - K_0\}$. Therefore, every generator $(K - K_0')$ belongs to $V$, implying $\operatorname{span}_{\mathbb{Q}} \{K_j - K_0'\} \subseteq V$. By symmetry, swapping $K_0$ and $K_0'$ yields the reverse inclusion. Thus the $\mathbb{Q}$-linear subspaces coincide, and their dimensions are identical: $\dim_{\mathbb{Q}} V' = \dim_{\mathbb{Q}} V$. $\blacksquare$

*Formal Verification Scope*: Formalized in `RiemannScope.AmbientKernel` as `base_change_linear_span` (affine difference identity of real numbers) and `support_affine_difference_base_change`. Full equality of $\mathbb{Q}$-spans and vector space dimensions is a `PROVED_PAPER_DERIVATION`.

---

## Section D. Rank-Zero Classification

**Theorem (Rank-Zero Triviality)**:  
*If $r(S) = 0$, then all grades in the support coincide: $K_1 = \dots = K_m = K_0$. In this case,*
$$\boxed{\sum_{j=1}^m a_j \tau^{K_j} = 0 \iff \sum_{j=1}^m a_j = 0.}$$

*Proof*: $r(S) = 0$ implies that $K_j - K_0 = 0$ for all $j$, so $K_j = K_0$. The sum becomes $(\sum_{j=1}^m a_j)\tau^{K_0} = 0$. Since $\tau^{K_0} \ne 0$, the evaluation vanishes if and only if $\sum a_j = 0$. $\blacksquare$

*Classification*: `RANK_ZERO_TRIVIAL_COEFFICIENT_CANCELLATION`.  
This is purely linear cancellation in the coefficient field $\overline{\mathbb{Q}}$, not a cross-grade kernel phenomenon.

*Lean 4 Verification*: Formalized in `RiemannScope.AmbientKernel` as `rank_zero_evaluation_factor`, `rank_zero_kernel_iff`, and `rank_zero_kernel_three_iff`.

---

## Section E. Exact Rank-One Theorem

Suppose $r(S) = 1$. Then all grade differences lie on a single rational line:
$$K_j - K_0 = q_j \alpha, \qquad q_j \in \mathbb{Q}, \quad \alpha \in \mathbb{A}_{\mathbb{R}} \setminus \{0\}.$$

Recall the Gelfond–Schneider exceptional exponent set:
$$\boxed{S_\tau = \{\alpha \in \mathbb{A}_{\mathbb{R}} : \tau^\alpha \in \overline{\mathbb{Q}}\}.}$$

**Theorem (Exact Rank-One Dichotomy)**:  
*Let $\alpha \in \mathbb{A}_{\mathbb{R}} \setminus \{0\}$. The evaluation map $\operatorname{ev}_\tau$ restricted to $\overline{\mathbb{Q}}[\mathbb{Q}\alpha]$ is injective if and only if $\alpha \notin S_\tau$.*

*Proof*:  
1. **($\implies$)**: Suppose $\alpha \in S_\tau$. Then by definition, $\tau^\alpha = A$ for some algebraic number $A \in \overline{\mathbb{Q}}$ ($A > 0$). Consider the element $F = [\alpha] - A[0] \in \overline{\mathbb{Q}}[\mathbb{Q}\alpha]$. Its support is $\{0, \alpha\}$, which has $r(S) = 1$ and non-zero coefficients $(1, -A)$. Then:
$$\operatorname{ev}_\tau(F) = 1 \cdot \tau^\alpha - A \cdot \tau^0 = A - A = 0.$$
Thus $F \in \ker(\operatorname{ev}_\tau) \setminus \{0\}$, so $\operatorname{ev}_\tau$ is not injective on $\overline{\mathbb{Q}}[\mathbb{Q}\alpha]$.

2. **($\impliedby$)**: Suppose $\alpha \notin S_\tau$, meaning $\tau^\alpha$ is transcendental. Suppose for contradiction that there exists a non-zero element $F = \sum_{j=1}^m c_j [q_j \alpha] \in \ker(\operatorname{ev}_\tau)$ with $c_j \in \overline{\mathbb{Q}} \setminus \{0\}$ and pairwise distinct rationals $q_j \in \mathbb{Q}$.  
Write $q_j = m_j / D$ with a common positive integer denominator $D \ge 1$ and integers $m_j \in \mathbb{Z}$. Then:
$$\sum_{j=1}^m c_j \tau^{(m_j/D)\alpha} = \sum_{j=1}^m c_j \left(\tau^{\alpha/D}\right)^{m_j} = 0.$$
Setting $X = \tau^{\alpha/D} > 0$, this is a non-trivial Laurent polynomial $\sum_{j=1}^m c_j X^{m_j} = 0$. Multiplying by $X^N$ where $N = -\min_j m_j \ge 0$, we obtain:
$$P(X) = \sum_{j=1}^m c_j X^{m_j + N} = 0.$$
Here $P(X) \in \overline{\mathbb{Q}}[X]$ is a non-zero polynomial with algebraic coefficients and degree $\max_j (m_j + N) \ge 1$ (since the $q_j$ are distinct and $m \ge 2$). Because $P(X) = 0$, the real number $X = \tau^{\alpha/D}$ is algebraic: $X \in \overline{\mathbb{Q}}$.  
Because algebraic numbers form a field algebraically closed under integer powers, $X^D = (\tau^{\alpha/D})^D = \tau^\alpha$ must also be algebraic: $\tau^\alpha \in \overline{\mathbb{Q}}$.  
This contradicts the hypothesis $\alpha \notin S_\tau$. Therefore no such non-trivial relation can vanish, and $\operatorname{ev}_\tau$ is injective on $\overline{\mathbb{Q}}[\mathbb{Q}\alpha]$. $\blacksquare$

*Classification*: `RANK_ONE_KERNEL_CLASSIFIED`.

*Formal Verification Scope*: Formalized in `RiemannScope.AmbientKernel` as `s_tau_explicit_kernel_witness`, `s_tau_explicit_kernel_witness_scaled`, and `rank_one_injective_of_transcendental_power` (proving the impossibility of a 2-term relation $c_1 \tau^\alpha + c_0 = 0$ with $c_1 \ne 0$ under an abstract algebraicity predicate). Injectivity of the full group algebra $\overline{\mathbb{Q}}[\mathbb{Q}\alpha]$ on arbitrary finite support is a `PROVED_PAPER_DERIVATION` via Laurent polynomial clearing.

---

## Section F. Exceptional-Set Relation

The Gelfond–Schneider theorem (1934) establishes that for algebraic base $a \in \overline{\mathbb{Q}} \setminus \{0, 1\}$ and irrational algebraic exponent $b \in \overline{\mathbb{Q}} \setminus \mathbb{Q}$, $a^b$ is transcendental.

In TASK-TC-023, this was applied externally to directions in $S_\tau$: if $\alpha_1, \alpha_2 \in S_\tau \setminus \{0\}$, then $\tau^{\alpha_1} = A_1 \in \overline{\mathbb{Q}}$ and $\tau^{\alpha_2} = A_2 \in \overline{\mathbb{Q}}$ force $(A_1)^{\alpha_2 / \alpha_1} = \tau^{\alpha_2} = A_2$. Since the base $A_1 \in \overline{\mathbb{Q}}$ is algebraic, Gelfond–Schneider forces the ratio $\alpha_2 / \alpha_1$ to be rational:
$$\boxed{\dim_{\mathbb{Q}} S_\tau \le 1.}$$

**Consequence for the Ambient Kernel**:
- There exists at most **one** rational line $\mathbb{Q}\alpha_0$ in $\mathbb{A}_{\mathbb{R}}$ along which $\operatorname{ev}_\tau$ can fail to be injective.
- For all other rational directions $\mathbb{Q}\beta$ ($\beta \notin \mathbb{Q}\alpha_0$), $\operatorname{ev}_\tau$ is **unconditionally injective**.
- What $S_\tau$ does **not** control: It controls only individual algebraic powers and collinear pairs. It provides zero control over multi-term relations across independent directions ($r \ge 2$), because such relations involve algebraic dependence among transcendental powers, not individual algebraicity.

---

## Section G. Higher-Rank Multivariate Reduction

Now consider finite support sets of rational rank $r \ge 2$.

**Theorem (Multivariate Laurent Reduction)**:  
*Let $S = \{K_1, \dots, K_m\}$ have rational rank $r \ge 2$. Let $\alpha_1, \dots, \alpha_r$ be a $\mathbb{Q}$-basis of $\operatorname{span}_{\mathbb{Q}} \{K_j - K_0\}$. Then any kernel relation $\sum_{j=1}^m a_j \tau^{K_j} = 0$ is equivalent to the vanishing of a non-zero multivariate algebraic polynomial:*
$$\boxed{Q(X_1, \dots, X_r) = 0, \qquad Q \in \overline{\mathbb{Q}}[X_1, \dots, X_r] \setminus \{0\},}$$
*evaluated at $X_\ell = \tau^{\alpha_\ell / D}$ for a common integer denominator $D \ge 1$.*

*Proof*:  
1. By support translation invariance, $\sum a_j \tau^{K_j} = 0 \iff \sum a_j \tau^{K_j - K_0} = 0$.
2. Decompose each difference in the rational basis: $K_j - K_0 = \sum_{\ell=1}^r q_{j\ell} \alpha_\ell$ with $q_{j\ell} \in \mathbb{Q}$.
3. Choose a common denominator $D \ge 1$ such that $D q_{j\ell} = m_{j\ell} \in \mathbb{Z}$ for all $j, \ell$.
4. Setting $X_\ell = \tau^{\alpha_\ell / D} > 0$, the power evaluates as:
$$\tau^{K_j - K_0} = \prod_{\ell=1}^r \tau^{(m_{j\ell}/D)\alpha_\ell} = \prod_{\ell=1}^r X_\ell^{m_{j\ell}}.$$
5. The sum becomes a Laurent polynomial relation:
$$P(X_1, \dots, X_r) = \sum_{j=1}^m a_j \prod_{\ell=1}^r X_\ell^{m_{j\ell}} = 0.$$
6. Multiply by the clearing monomial $\prod_{\ell=1}^r X_\ell^{N_\ell}$ where $N_\ell = -\min_j m_{j\ell} \ge 0$. Since $X_\ell > 0$, this monomial is strictly positive and does not alter vanishing.
7. The resulting expression $Q(X_1, \dots, X_r) = \sum_{j=1}^m a_j \prod_{\ell=1}^r X_\ell^{m_{j\ell} + N_\ell}$ has non-negative exponents and algebraic coefficients $a_j$. Because the support points $K_j$ are distinct and $F \ne 0$, $Q$ is not the zero polynomial. Thus $Q(X_1, \dots, X_r) = 0$ is a non-trivial algebraic dependence relation over $\overline{\mathbb{Q}}$. $\blacksquare$

*Formal Verification Scope*: Formalized in `RiemannScope.AmbientKernel` as `bivariate_monomial_clearing` (algebra identity for bivariate common-power factoring). The general $r$-variate Laurent reduction and equivalence theorem is a `PROVED_PAPER_DERIVATION`.

---

## Section H. Algebraic-Independence Equivalence

**Theorem (Equivalence Between Kernel Injectivity and Algebraic Independence)**:  
*Let $\alpha_1, \dots, \alpha_r \in \mathbb{A}_{\mathbb{R}}$ be $\mathbb{Q}$-linearly independent. Let $\Gamma = \mathbb{Q}\alpha_1 \oplus \cdots \oplus \mathbb{Q}\alpha_r$. Then:*
$$\boxed{\operatorname{ev}_\tau \text{ is injective on } \overline{\mathbb{Q}}[\Gamma] \iff \{\tau^{\alpha_1}, \dots, \tau^{\alpha_r}\} \text{ are algebraically independent over } \overline{\mathbb{Q}}.}$$

*Proof*:  
- **($\implies$)**: Suppose $\tau^{\alpha_1}, \dots, \tau^{\alpha_r}$ are algebraically dependent over $\overline{\mathbb{Q}}$. Then there exists a non-zero polynomial $R(Y_1, \dots, Y_r) = \sum a_{i_1, \dots, i_r} Y_1^{i_1} \cdots Y_r^{i_r} = 0$ with $a_{\vec{i}} \in \overline{\mathbb{Q}}$. Each monomial evaluates to $\tau^{\sum_\ell i_\ell \alpha_\ell}$. The element $F = \sum a_{\vec{i}} [\sum_\ell i_\ell \alpha_\ell] \in \overline{\mathbb{Q}}[\Gamma]$ is non-zero (since the basis exponents are distinct by $\mathbb{Q}$-linear independence of the $\alpha_\ell$) and satisfies $\operatorname{ev}_\tau(F) = 0$. Thus $\operatorname{ev}_\tau$ is not injective on $\overline{\mathbb{Q}}[\Gamma]$.
- **($\impliedby$)**: Suppose $\operatorname{ev}_\tau$ is not injective on $\overline{\mathbb{Q}}[\Gamma]$. By Section G, there exists a non-zero polynomial relation $Q(X_1, \dots, X_r) = 0$ for $X_\ell = \tau^{\alpha_\ell / D}$. Thus $X_1, \dots, X_r$ are algebraically dependent over $\overline{\mathbb{Q}}$, so:
$$\operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}(X_1, \dots, X_r) < r.$$
Consider the subfield $K = \overline{\mathbb{Q}}(\tau^{\alpha_1}, \dots, \tau^{\alpha_r})$ and the extension field $L = \overline{\mathbb{Q}}(X_1, \dots, X_r)$. Since $X_\ell^D = \tau^{\alpha_\ell} \in K$, each $X_\ell$ satisfies the monic polynomial $T^D - \tau^{\alpha_\ell} = 0$ over $K$, so $[L : K] \le D^r < \infty$.  
A standard theorem of field theory states that a finite algebraic extension preserves transcendence degree:
$$\operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}(\tau^{\alpha_1}, \dots, \tau^{\alpha_r}) = \operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}(X_1, \dots, X_r) < r.$$
Hence the generators $\tau^{\alpha_1}, \dots, \tau^{\alpha_r}$ are algebraically dependent over $\overline{\mathbb{Q}}$. $\blacksquare$

*Fundamental Conclusion*:  
$$\boxed{\begin{gathered}\textbf{Finite TC ambient-kernel relations of rational support rank } r \\ \textbf{are precisely algebraic-dependence relations among } r \textbf{ algebraic powers of } 2\pi.\end{gathered}}$$

---

## Section I. Canonical Minimal Rank-Two Open Instance

With $r=0$ trivial and $r=1$ completely classified by $S_\tau$, the boundary of current human mathematical knowledge occurs at **rational support rank $r=2$**, which represents the minimal unresolved rational support rank.

A clean canonical concrete representative is:
$$\boxed{\textbf{CANONICAL MINIMAL RANK-TWO OPEN INSTANCE:}}$$
$$\alpha_1 = \sqrt{2}, \qquad \alpha_2 = \sqrt{3}.$$
Does there exist any non-zero bivariate polynomial $P \in \overline{\mathbb{Q}}[X, Y]$ such that:
$$\boxed{P\left((2\pi)^{\sqrt{2}}, (2\pi)^{\sqrt{3}}\right) = 0 \quad?}$$

Equally, the base-one instance $\alpha_1 = 1, \alpha_2 = \sqrt{2}$ produces generators $X = 2\pi, Y = (2\pi)^{\sqrt{2}}$, which is likewise unresolved by standard classical theorems.

Even the linear case with 4 terms:
$$a_0 + a_1 (2\pi)^{\sqrt{2}} + a_2 (2\pi)^{\sqrt{3}} + a_3 (2\pi)^{\sqrt{2} + \sqrt{3}} = 0, \qquad a_j \in \mathbb{A}_{\mathbb{R}},$$
is an **open problem in transcendental number theory**. No known unconditional theorem proves linear independence of these 4 numbers over $\overline{\mathbb{Q}}$.

---

## Section J. Two-Variable Open Case

For general independent algebraic exponents:
$$X = \tau^\alpha, \qquad Y = \tau^\beta, \qquad \alpha, \beta \in \mathbb{A}_{\mathbb{R}}, \quad \frac{\alpha}{\beta} \notin \mathbb{Q}.$$

- If $\alpha \notin S_\tau$ and $\beta \notin S_\tau$, both $X$ and $Y$ are individually transcendental.
- Pairwise transcendence does **not** exclude algebraic dependence:
  - Example: $u = \pi$ is transcendental, $v = \pi^2$ is transcendental, $v/u = \pi$ is transcendental, yet $v - u^2 = 0$.
  - Example: $u = \pi, v = 1/\pi$ are both transcendental, yet $uv - 1 = 0$.
- Hence, proving that $(2\pi)^\alpha$ and $(2\pi)^\beta$ are individually transcendental provides **zero information** about whether they satisfy an algebraic curve $P(X, Y) = 0$.
- Formalized in Lean 4 as `pairwise_transcendence_not_algebraic_independence_model` and `inverse_pair_algebraic_relation`.

---

## Section K. Applicable Transcendence Theorems: Comprehensive Literature Audit

| Theorem | Primary Reference | Hypotheses | What it Proves | Applies to Base $2\pi$? | Kernel Consequence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lindemann** | Lindemann (1882) | $\alpha \in \overline{\mathbb{Q}} \setminus \{0\}$ | $e^\alpha$ is transcendental; $\pi$ is transcendental. | YES (for $\tau^1 = 2\pi$) | Proves $\tau = 2\pi \notin \overline{\mathbb{Q}}$. Base grade $1 \in \mathbb{A}_{\mathbb{R}}$ is algebraic; what is transcendental is $\tau^1 = 2\pi$, equivalently $1 \notin S_\tau$. |
| **Lindemann–Weierstrass** | Weierstrass (1885) | $\beta_1, \dots, \beta_n \in \overline{\mathbb{Q}}$ $\mathbb{Q}$-linearly independent | $e^{\beta_1}, \dots, e^{\beta_n}$ are algebraically independent over $\overline{\mathbb{Q}}$. | **NO** | $\tau^\alpha = e^{\alpha \log(2\pi)}$. Exponent $\alpha\log(2\pi)$ is **not** algebraic (it involves $\log(2\pi)$). Does not apply. |
| **Gelfond–Schneider** | Gelfond (1934), Schneider (1934) | $a \in \overline{\mathbb{Q}} \setminus \{0, 1\}$, $b \in \overline{\mathbb{Q}} \setminus \mathbb{Q}$ | $a^b$ is transcendental. | **NO (directly)** | Base $2\pi$ is transcendental, violating the algebraic base hypothesis. Applies only to ratios where $2\pi$ cancels ($\dim_{\mathbb{Q}} S_\tau \le 1$). |
| **Six Exponentials** | Eramian (1965), Lang (1966) | $x_1, x_2 \in \mathbb{C}$ $\mathbb{Q}$-indep; $y_1, y_2, y_3 \in \mathbb{C}$ $\mathbb{Q}$-indep | At least one of $e^{x_i y_j}$ ($1 \le i \le 2, 1 \le j \le 3$) is transcendental. | **VACUOUS** | Taking $x = (1, \log\tau)$ and $y_j = \alpha_j$, $e^{1 \cdot \alpha_j}$ are already transcendental by Lindemann. Guarantees nothing about $\tau^{\alpha_j}$. |
| **Four Exponentials** | Open Conjecture | $x_1, x_2$ $\mathbb{Q}$-indep; $y_1, y_2$ $\mathbb{Q}$-indep | At least one of the four $e^{x_i y_j}$ is transcendental. | **VACUOUS** | Again satisfied by $e^{\alpha_1}, e^{\alpha_2}$ being transcendental. |
| **Baker's Theorem** | Baker (1966) | $\alpha_1, \dots, \alpha_n \in \overline{\mathbb{Q}} \setminus \{0\}$, $b_j \in \overline{\mathbb{Q}}$ | $\beta_0 + \sum b_j \log \alpha_j \ne 0$ for non-zero forms. | **NO** | $\log(2\pi)$ is not the logarithm of an algebraic number. Baker applies to algebraic inputs only. |
| **Nesterenko** | Nesterenko (1996) | Modular forms / Eisenstein series | $\pi, e^\pi, \Gamma(1/4)$ are algebraically independent over $\mathbb{Q}$. | **NO** | Powers $(2\pi)^\alpha$ are not generated by Eisenstein series or Ramanujan functions. |
| **Schanuel's Conjecture** | Schanuel (c. 1965) | $z_1, \dots, z_n \in \mathbb{C}$ $\mathbb{Q}$-linearly independent | $\operatorname{trdeg}_{\mathbb{Q}} \mathbb{Q}(z_1, \dots, z_n, e^{z_1}, \dots, e^{z_n}) \ge n$. | **YES (Conditionally)** | Two-case derivation proves full algebraic independence: $\operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}(\tau^{\alpha_1}, \dots, \tau^{\alpha_r}) = r$, implying full finite-rank injectivity of $\operatorname{ev}_\tau$ on all algebraic supports. (See Section L). |

---

## Section L. Corrected & Strengthened Schanuel Conditional Theorem

Schanuel's Conjecture states that if $z_1, \dots, z_n \in \mathbb{C}$ are $\mathbb{Q}$-linearly independent, then:
$$\operatorname{trdeg}_{\mathbb{Q}} \mathbb{Q}\left(z_1, \dots, z_n, e^{z_1}, \dots, e^{z_n}\right) \ge n.$$

Let $\alpha_1, \dots, \alpha_r \in \mathbb{A}_{\mathbb{R}}$ be a $\mathbb{Q}$-basis of a rational support space of rank $r \ge 1$. Put:
$$L = \log\tau = \log(2\pi), \qquad X_j = e^{\alpha_j L} = \tau^{\alpha_j} \quad (j = 1, \dots, r).$$

We prove that Schanuel's conjecture implies full algebraic independence of $\{X_1, \dots, X_r\}$ over $\overline{\mathbb{Q}}$ by considering two mutually exclusive cases:

### Case A: $1, \alpha_1, \dots, \alpha_r$ are $\mathbb{Q}$-linearly independent
Consider the $r + 2$ complex numbers:
$$z_0 = i\pi, \quad z_{\log} = L, \quad z_1 = \alpha_1 L, \quad \dots, \quad z_r = \alpha_r L.$$
- $z_0 = i\pi$ is purely imaginary, whereas $L, \alpha_1 L, \dots, \alpha_r L$ are non-zero real numbers.
- Among the real numbers, linear independence over $\mathbb{Q}$ reduces to the linear independence of $1, \alpha_1, \dots, \alpha_r$ over $\mathbb{Q}$ (dividing through by $L \ne 0$).
- Hence, $z_0, z_{\log}, z_1, \dots, z_r$ are $r + 2$ complex numbers that are $\mathbb{Q}$-linearly independent.

Their exponentials are:
$$e^{z_0} = e^{i\pi} = -1, \quad e^{z_{\log}} = e^L = 2\pi, \quad e^{z_j} = e^{\alpha_j L} = X_j \quad (j = 1, \dots, r).$$

Applying Schanuel's conjecture to these $r + 2$ numbers:
$$\operatorname{trdeg}_{\mathbb{Q}} \mathbb{Q}\left(i\pi, L, \alpha_1 L, \dots, \alpha_r L, -1, 2\pi, X_1, \dots, X_r\right) \ge r + 2.$$

Notice that over $\overline{\mathbb{Q}}$:
1. $2\pi = -2i(i\pi)$ is algebraic over $i\pi$.
2. Each $\alpha_j L$ is algebraic over the field generated by $L$ (since $\alpha_j \in \mathbb{A}_{\mathbb{R}} \subset \overline{\mathbb{Q}}$).
3. $-1$ is rational.

Therefore, the generated field is an algebraic extension of the field generated by the $r + 2$ elements:
$$\overline{\mathbb{Q}}\left(i\pi, L, X_1, \dots, X_r\right).$$
Consequently:
$$\operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}\left(i\pi, L, X_1, \dots, X_r\right) \ge r + 2.$$
Because there are exactly $r + 2$ displayed generators, their transcendence degree cannot exceed $r + 2$. Therefore, they must have transcendence degree exactly $r + 2$, meaning that **all $r + 2$ generators are mutually algebraically independent over $\overline{\mathbb{Q}}$**. In particular:
$$\boxed{\operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}\left(X_1, \dots, X_r\right) = r.}$$

### Case B: $1 \in \operatorname{span}_{\mathbb{Q}}\{\alpha_1, \dots, \alpha_r\}$
Because $1$ lies in the rational span of the basis, there exist rational coefficients $q_j \in \mathbb{Q}$ such that:
$$1 = \sum_{j=1}^r q_j \alpha_j.$$
Multiplying by $L = \log\tau$:
$$L = \sum_{j=1}^r q_j (\alpha_j L).$$
Clearing denominators with a common positive integer $D \ge 1$ ($n_j = D q_j \in \mathbb{Z}$):
$$\tau^D = \prod_{j=1}^r X_j^{n_j}.$$
Thus $\tau = 2\pi$ is algebraic over $\overline{\mathbb{Q}}(X_1, \dots, X_r)$. Since $i\pi = \tau / (2i)$, $i\pi$ is also algebraic over $\overline{\mathbb{Q}}(X_1, \dots, X_r)$.

Now consider the $r + 1$ numbers:
$$z_0 = i\pi, \quad z_1 = \alpha_1 L, \quad \dots, \quad z_r = \alpha_r L.$$
These $r + 1$ numbers are $\mathbb{Q}$-linearly independent: $i\pi$ is purely imaginary, and the real numbers $\alpha_1 L, \dots, \alpha_r L$ are $\mathbb{Q}$-linearly independent because $\alpha_1, \dots, \alpha_r$ form a $\mathbb{Q}$-basis.

Their exponentials are $-1, X_1, \dots, X_r$. Applying Schanuel's conjecture:
$$\operatorname{trdeg}_{\mathbb{Q}} \mathbb{Q}\left(i\pi, \alpha_1 L, \dots, \alpha_r L, -1, X_1, \dots, X_r\right) \ge r + 1.$$

Over $\overline{\mathbb{Q}}$:
- $i\pi \in \overline{\mathbb{Q}}(X_1, \dots, X_r)$.
- Each $\alpha_j L$ is an algebraic multiple of $L$ (since $\alpha_j \in \mathbb{A}_{\mathbb{R}} \subset \overline{\mathbb{Q}}$).
Thus the only possible additional transcendence degree contributed by the logarithmic side $\{i\pi, \alpha_1 L, \dots, \alpha_r L\}$ over $\overline{\mathbb{Q}}(X_1, \dots, X_r)$ is at most $1$ (contributed by $L$). Therefore:
$$\operatorname{trdeg}_{\mathbb{Q}} \mathbb{Q}\left(i\pi, \alpha_1 L, \dots, \alpha_r L, -1, X_1, \dots, X_r\right) \le 1 + \operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}\left(X_1, \dots, X_r\right).$$
Combining this with Schanuel's lower bound gives:
$$r + 1 \le 1 + \operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}\left(X_1, \dots, X_r\right) \implies \operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}\left(X_1, \dots, X_r\right) \ge r.$$
Since there are only $r$ generators $X_1, \dots, X_r$, the transcendence degree is bounded by $r$, hence:
$$\boxed{\operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}\left(X_1, \dots, X_r\right) = r.}$$

### Fundamental Schanuel Theorem
In both Case A and Case B, the transcendence degree is maximal:
$$\boxed{\operatorname{trdeg}_{\overline{\mathbb{Q}}} \overline{\mathbb{Q}}\left(\tau^{\alpha_1}, \dots, \tau^{\alpha_r}\right) = r.}$$
By the equivalence theorem established in Section H, algebraic independence of $\{\tau^{\alpha_1}, \dots, \tau^{\alpha_r}\}$ over $\overline{\mathbb{Q}}$ is equivalent to the injectivity of $\operatorname{ev}_\tau$ on $\overline{\mathbb{Q}}[\mathbb{Q}\alpha_1 \oplus \cdots \oplus \mathbb{Q}\alpha_r]$. Therefore:

$$\boxed{\begin{gathered}\textbf{Theorem (Schanuel Full-Injectivity Conditional Theorem):} \\ \textbf{Schanuel's Conjecture implies that the ambient realization evaluation map } \operatorname{ev}_\tau \\ \textbf{is injective on every finite algebraic-grade support } S \subset \mathbb{A}_{\mathbb{R}}.\end{gathered}}$$

This materially strengthens the transcendence picture: the non-injectivity of $\operatorname{ev}_\tau$ is not an open structural phenomenon, but would constitute a counterexample to Schanuel's conjecture!

---

## Section M. Four/Six Exponentials Audit

The Six Exponentials Theorem states that if $x_1, x_2$ are $\mathbb{Q}$-linearly independent and $y_1, y_2, y_3$ are $\mathbb{Q}$-linearly independent, then at least one of the 6 numbers $e^{x_i y_j}$ is transcendental.

Suppose we set $x_1 = 1, x_2 = \log(2\pi)$, and choose algebraic numbers $y_1 = \alpha_1, y_2 = \alpha_2, y_3 = \alpha_3$. Then the 6 numbers in the matrix are:
$$\begin{pmatrix} e^{\alpha_1} & e^{\alpha_2} & e^{\alpha_3} \\ (2\pi)^{\alpha_1} & (2\pi)^{\alpha_2} & (2\pi)^{\alpha_3} \end{pmatrix}.$$
By Lindemann's Theorem (1882), $e^{\alpha_j}$ is **already transcendental** for every non-zero algebraic $\alpha_j$!  
Therefore, the first row already contains transcendental numbers. The Six Exponentials Theorem is fully satisfied by the first row alone, providing **zero mathematical constraint** on the second row $(2\pi)^{\alpha_j}$.

The identical phenomenon occurs for the Four Exponentials Conjecture: the algebraic row $e^{\alpha_j}$ already guarantees transcendence, leaving the $(2\pi)^{\alpha_j}$ row completely unconstrained.

---

## Section N. Bounded Computational Exclusions and Certified Rigor

To verify that no small or accidental algebraic relation exists for canonical rank-two supports, high-precision numerical searches and certified interval exclusions were executed.

### 1. High-Precision PSLQ Search
- **Support**: $\alpha = \sqrt{2}, \beta = \sqrt{3}$.
- **Generators**: $X = (2\pi)^{\sqrt{2}} \approx 13.452307777$, $Y = (2\pi)^{\sqrt{3}} \approx 24.126153440$.
- **Monomial Basis**: $\{1, X, Y, X^2, XY, Y^2\}$ (total degree $\le 2$).
- **Working Precision**: 80 decimal digits.
- **Search Bound**: $\|c\|_\infty \le 1000$.
- **Result**: `None` (no integer relation found).

### 2. Certified Arb Ball Arithmetic Exclusions
Using `flint.arb` with guaranteed interval arithmetic enclosure:
- **Native Algebraic Enclosure**: Exponents $\sqrt{2}, \sqrt{3}$ are enclosed directly inside Arb via `expr_to_arb()` (`arb(2).sqrt()`, `arb(3).sqrt()`, and `2 * arb.pi()`), avoiding decimal-string roundtripping.
- **Certified Lower Distance**: Distance is computed via `float(val.abs_lower())`, which gives a mathematically certified lower bound on the distance of the entire interval/ball from zero (not merely its midpoint).

| Support $(\alpha, \beta)$ | Monomial Basis | Max Degree | Height Bound $H$ | Polynomials Tested | Status | Min Certified Distance | Evidence Class |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $(\sqrt{2}, \sqrt{3})$ | $\{1, X, Y\}$ | 1 | 5 | 1,330 | `CERTIFIED_NONZERO` | $> 0.116921$ | `CERTIFIED_FINITE_RELATION_EXCLUSION` |
| $(\sqrt{2}, \sqrt{3})$ | $\{1, X, Y, X^2, XY, Y^2\}$ | 2 | 2 | 15,624 | `CERTIFIED_NONZERO` | $> 0.201733$ | `CERTIFIED_FINITE_RELATION_EXCLUSION` |

*Evidence Class*: `CERTIFIED_FINITE_RELATION_EXCLUSION`.  
*Explicit Boundary*: This certified exclusion rigorously proves that no non-zero polynomial of degree $\le 2$ with coefficients $|c_{ij}| \le 2$ vanishes at $((2\pi)^{\sqrt{2}}, (2\pi)^{\sqrt{3}})$. It does **not** constitute mathematical proof of algebraic independence.

---

## Section O. Zeta-Bridge Firewall

A legitimate mathematical bridge from the Riemann zeta function to the ambient realization kernel must produce an element $F = \sum a_j [K_j] \in \overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}]$ that vanishes under $\operatorname{ev}_\tau$, where:
1. Every coefficient $a_j$ is **proved to be algebraic** ($a_j \in \overline{\mathbb{Q}}$).
2. Every grade $K_j$ is **proved to be algebraic** ($K_j \in \mathbb{A}_{\mathbb{R}}$).

### Firewall Checklist

| Candidate Quantity | Mathematical Origin | Arithmetic Status | Firewall Verdict | Reason |
| :--- | :--- | :--- | :--- | :--- |
| $\gamma_n$ | Zeta zero ordinate $\rho_n = 1/2 + i\gamma_n$ | `ALGEBRAICITY_UNPROVED` | **REJECTED** | Algebraicity unproved. Cannot appear as proved algebraic grade or coefficient. |
| $\rho_n$ | Nontrivial zero | `ALGEBRAICITY_UNPROVED` | **REJECTED** | Algebraicity unproved. |
| $\log p$ | Prime weight $\Lambda(n)$ | `PROVED_TRANSCENDENTAL` | **REJECTED** | Transcendental by Lindemann (1882). Cannot appear in algebraic coefficient field. |
| $\zeta(2n)$ | Euler special value | `PROVED_TRANSCENDENTAL` | **REJECTED** | $\zeta(2n) = (-1)^{n+1} B_{2n} (2\pi)^{2n} / (2(2n)!)$ is a non-zero rational multiple of $\pi^{2n}$. |
| $\zeta(2n+1)$ | Odd zeta values ($\zeta(3)$, $\zeta(5)$, etc.) | `ALGEBRAICITY_UNPROVED` | **REJECTED** | Apéry (1978) proved $\zeta(3) \notin \mathbb{Q}$; recent results establish $\zeta(5) \notin \mathbb{Q}$. But irrational does not mean transcendental; algebraicity is unproved. Inadmissible as proved algebraic coefficient. |
| $\Gamma(\rho)$ | Gamma functional factor | `ALGEBRAICITY_UNPROVED` | **REJECTED** | At nontrivial zeros, lacks any known arithmetic classification licensing algebraicity. Inadmissible as proved algebraic coefficient. |
| $\sum \Lambda(n) n^{-s}$ | Dirichlet series / Explicit formula | `INFINITE_DISTRIBUTION` | **REJECTED** | Infinite distribution; kernel is defined on finite supports. |

**Firewall Finding**:  
$$\boxed{\texttt{NO\_ZETA\_TO\_KERNEL\_BRIDGE\_FOUND}}$$
This is strictly an **audit finding** over all examined standard zeta structures, explicit formulas, and special values: they fail to furnish proved algebraic coefficients and grades. This establishes that no bridge has been found, without asserting an unproved universal nonexistence theorem.

---

## Section P. Relation to Zero-Arithmetic Research

The repository contains separate investigations concerning the arithmetic nature of nontrivial zeros (e.g. $\gamma_1, \rho_1$).

We explicitly establish that **zero arithmetic and TC ambient kernel transcendence are logically distinct**:
1. If $\gamma_1$ were proved transcendental, it would immediately disqualify $\gamma_1$ from appearing as a canonical TC grade ($K \in \mathbb{A}_{\mathbb{R}}$).
2. If $\gamma_1$ were proved algebraic, it could legally be considered as a grade, but producing a vanishing sum $\sum a_j (2\pi)^{K_j} = 0$ would still require an entirely new algebraic relation that the zeta functional equation does not provide.
3. Proving a zeta zero transcendental creates no algebraic relation among powers $(2\pi)^\alpha$.
4. Conversely, resolving the ambient kernel $\ker(\operatorname{ev}_\tau)$ over $\mathbb{A}_{\mathbb{R}}$ is an intrinsic problem of transcendental number theory that operates independently of the Riemann Hypothesis.

---

## Section Q. Final Kernel Classification & Scope Delineation

### Primary Classification
$$\boxed{\texttt{FINITE\_KERNEL\_REDUCES\_TO\_ALGEBRAIC\_INDEPENDENCE}}$$
The ambient evaluation kernel on finite supports of rational rank $r$ is completely reduced to the algebraic independence of $r$ algebraic powers of $2\pi$. The rank-zero case is trivial coefficient cancellation, the rank-one case is completely classified by $S_\tau$, and higher ranks $r \ge 2$ constitute an open problem in transcendental number theory.

### Secondary Classifications
- `RANK_ZERO_TRIVIAL`: $r=0$ vanishes iff sum of coefficients vanishes.
- `RANK_ONE_KERNEL_CLASSIFIED`: $r=1$ injective iff $\alpha \notin S_\tau$.
- `ONE_EXCEPTIONAL_Q_DIRECTION_ONLY`: $\dim_{\mathbb{Q}} S_\tau \le 1$ via Gelfond–Schneider.
- `HIGHER_RANK_ALGEBRAIC_INDEPENDENCE_OPEN`: $r \ge 2$ is an open transcendence problem.
- `SCHANUEL_IMPLIES_FULL_FINITE_RANK_INJECTIVITY`: Two-case Schanuel proof establishes full injectivity conditional on Schanuel's conjecture.
- `PAIRWISE_TRANSCENDENCE_INSUFFICIENT`: Pairwise separation does not imply algebraic independence.
- `NO_ZETA_TO_KERNEL_BRIDGE_FOUND`: Audit finding: standard zeta quantities fail the algebraic firewall.
- `ZERO_ARITHMETIC_TRACK_LOGICALLY_DISTINCT`: Independent of zeta-zero transcendence.
- `CERTIFIED_FINITE_RELATION_EXCLUSION`: Verified via Arb ball arithmetic with native algebraic enclosure and interval lower bounds.

### Verification Scope Delineation
- $\boxed{\texttt{LEAN\_PROVED: algebraic skeleton / low arity}}$:
  - 2- and 3-term support translation invariance (`sum_tau_pow_zero_iff_translated_zero_two`, `three`)
  - 2- and 3-term rank-zero coefficient cancellation (`rank_zero_kernel_iff`, `three_iff`)
  - Base-grade difference identity of real numbers (`base_change_linear_span`)
  - 2-term explicit kernel witness for $\alpha \in S_\tau$ (`s_tau_explicit_kernel_witness`)
  - 2-term linear impossibility under abstract algebraicity predicate (`rank_one_injective_of_transcendental_power`)
  - Group algebra structural multiplication law (`group_algebra_mul_law`)
  - Bivariate monomial clearing identity (`bivariate_monomial_clearing`)
  - Abstract pairwise countermodel $v = u^2$ (`pairwise_transcendence_not_algebraic_independence_model`)
- $\boxed{\texttt{PROVED\_PAPER\_DERIVATION: full rank-one and higher-rank classification}}$:
  - Full group algebra $\overline{\mathbb{Q}}[\mathbb{Q}\alpha]$ injectivity on arbitrary finite support via Laurent polynomial clearing
  - Equality of $\mathbb{Q}$-spans and exact dimension invariance under base-grade change
  - General $r$-variate Laurent polynomial reduction to algebraic independence
  - Two-case Schanuel conditional theorem proving $\operatorname{trdeg} = r$ and full finite-rank injectivity of $\operatorname{ev}_\tau$

---

## Section R. Exact Next Mathematical Problem

With the conditional injectivity under Schanuel settled, future research investigating unconditional ambient realization should address the minimal concrete problem:

$$\boxed{\text{Determine unconditionally whether } (2\pi)^{\sqrt{2}} \text{ and } (2\pi)^{\sqrt{3}} \text{ are algebraically independent over } \overline{\mathbb{Q}}.}$$
