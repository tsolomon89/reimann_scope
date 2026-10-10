# TASK-TC-030 Review: Minimal Rank-Two Trinomial Kernel, Relation-Space Rigidity, and Sparse Orbit Theorems

**Authoritative Status**: Research Review & Derivation Artifact  
**Task ID**: TASK-TC-030 / TASK-TC-030R  
**Baseline Git HEAD**: `f74fb15987bdedb6c5d845929df5634bb0c7fc6a`  
**Substantive Parent**: `74469d360fbfdf3fe80370199ed36a83b62816f9`  
**Primary Classification**: `TRINOMIAL_FRONTIER_STRUCTURALLY_CLASSIFIED_EXISTENCE_OPEN`  
**Task Classification**: `TASK_TC_030R_TRINOMIAL_REPAIR_COMPLETE`  
**Lean Formalization**: `formal/RiemannScope/TrinomialKernel.lean` (12 declarations compiled, 0 sorry, total 501 declarations)  
**Machine-Readable Data**: `data/tc_minimal_rank_two_trinomial_kernel.json`  

---

## Executive Summary

TASK-TC-028 and TASK-TC-029 reduced the ambient realization kernel problem $\ker(\operatorname{ev}_\tau)$ to algebraic dependence among finite families of powers $\tau^\alpha$ ($\tau = 2\pi$, $\alpha \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$).
TASK-TC-029 settled:
1. Two-term linear relations (reducing to $S_\tau$);
2. Monomial relations (reducing to Lindemann or $S_\tau$);
3. Quadratic-conjugate product identities (yielding transcendentals over $\mathbb{Q}$ and exact relations over $\overline{\mathbb{Q}}(2\pi)$).

The first genuinely unresolved kernel object is therefore not a generic polynomial. It is a **minimal-support relation with three nonzero terms and affine support rank two**:
$$a_0 + a_1 \tau^\alpha + a_2 \tau^\beta = 0, \qquad a_0, a_1, a_2 \in \overline{\mathbb{Q}}^\times, \quad \frac{\alpha}{\beta} \notin \mathbb{Q}.$$

TASK-TC-030 and TASK-TC-030R establish the complete structural theory of this trinomial frontier:
- **Relation-Space Rigidity**: $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1$. Two independent relations force algebraic coordinates, contradicting $\dim_{\mathbb{Q}} S_\tau \le 1$ via Gelfond-Schneider.
- **Pairwise Exceptional-Direction Exclusion**: $\alpha \notin S_\tau$, $\beta \notin S_\tau$, and $\beta - \alpha \notin S_\tau$.
- **Real Coefficient Normalization**: Direct elementary proof shows that complex conjugation and 1-dimensionality force $(a_0, a_1, a_2)$ to be algebraically equivalent to a real algebraic triple in $\mathbb{A}_{\mathbb{R}}^\times$.
- **Sign Geometry**: Same-sign coefficients cannot vanish with positive generators. Every relation orients into positive affine forms: $Y = u + vX$, $X = u + vY$, or $1 = uX + vY$ ($u, v > 0$).
- **Three-Consecutive Orbit Rigidity**: Nonzero trinomials cannot vanish on three consecutive integer dilations $f(n) = f(n+1) = f(n+2) = 0$.
- **Multiplicative-Group Finiteness**: By Laurent (1984) and Evertse-Schlickewei-Schmidt (2002), for each fixed coefficient triple, solutions $(u, v) \in \Gamma_0 \times \Gamma_0$ are finite. However, **`FINITE_DOES_NOT_IMPLY_EMPTY`**; existence of one relation remains open.
- **Certified Sparse Exclusion**: Certified interval arithmetic (python-flint Arb at 128-bit precision) excludes all $90,828$ normalized trinomials across 36 constant-anchored supports (30 rank-two, 6 rank-one controls) up to degree $D=3$ and height $H=10$ on both canonical rank-two instances.

---

## A. Why Three Terms are the First Open Support

Let $F = \sum_{j=1}^m c_j [K_j] \in \overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}]$ be a nonzero kernel element with minimal support among nonempty vanishing subsums, canonicalized via `canonicalize_group_algebra_terms`.

1. **Support Size $m = 1$**:
   $$c_0 \tau^{K_0} = 0.$$
   Since $\tau = 2\pi > 0$, $\tau^{K_0} > 0$ for every real grade $K_0 \in \mathbb{A}_{\mathbb{R}}$. With $c_0 \ne 0$, this product is strictly nonzero. Support size 1 is impossible.

2. **Support Size $m = 2$**:
   $$c_0 \tau^{K_0} + c_1 \tau^{K_1} = 0.$$
   Translating by $-K_0$ (factoring out $\tau^{K_0} > 0$):
   $$c_0 + c_1 \tau^{K_1 - K_0} = 0 \iff \tau^{K_1 - K_0} = -\frac{c_0}{c_1} \in \overline{\mathbb{Q}}^\times.$$
   Setting $\theta = K_1 - K_0 \in \mathbb{A}_{\mathbb{R}}$, this is precisely the condition $\theta \in S_\tau = \{\theta \in \mathbb{A}_{\mathbb{R}} : \tau^\theta \in \overline{\mathbb{Q}}\}$.
   - If $\theta \in \mathbb{Q}$, by Lindemann's theorem (1882), $\tau^\theta \in \overline{\mathbb{Q}} \iff \theta = 0$, which collapses the support to size 1.
   - If $\theta \in \mathbb{A}_{\mathbb{R}} \setminus \mathbb{Q}$, by the Gelfond-Schneider theorem (Baker 1975), $\dim_{\mathbb{Q}} S_\tau \le 1$.
   Thus support size 2 is completely classified by $S_\tau$.

3. **Support Size $m = 3$**:
   Translating one support point to grade zero ($K_0$ as base grade):
   $$a_0 + a_1 \tau^\alpha + a_2 \tau^\beta = 0, \qquad \alpha = K_1 - K_0, \; \beta = K_2 - K_0.$$
   - **Affine Rank 1 ($\alpha / \beta \in \mathbb{Q}$)**:
     Let $\alpha = \frac{p}{d} \theta$ and $\beta = \frac{q}{d} \theta$ with $p, q, d \in \mathbb{Z}$, $\theta \in \mathbb{A}_{\mathbb{R}}$.
     Setting $Z = \tau^{\theta / d} > 0$, the relation becomes:
     $$a_0 + a_1 Z^p + a_2 Z^q = 0.$$
     Clearing denominators yields a univariate polynomial equation with algebraic coefficients $P(Z) = 0$. Since $a_0, a_1, a_2 \ne 0$ and $p \ne q$, $P$ is not identically zero. Hence $Z \in \overline{\mathbb{Q}}$, forcing $\theta / d \in S_\tau$. This reduces affine-rank-one trinomials strictly to $S_\tau$.
   - **Affine Rank 2 ($\alpha / \beta \notin \mathbb{Q}$)**:
     $\alpha$ and $\beta$ are $\mathbb{Q}$-linearly independent. This is the first support class that cannot be reduced to a single generator or $S_\tau$.

$$\boxed{\texttt{FIRST\_OPEN\_KERNEL\_SUPPORT} = \text{three nonzero terms of affine rational rank two}}.$$

---

## B. Definition of the Trinomial Relation Space

For fixed $\alpha, \beta \in \mathbb{A}_{\mathbb{R}}$ with $\alpha / \beta \notin \mathbb{Q}$, let $X = \tau^\alpha$ and $Y = \tau^\beta$.
Define the vector space of linear relations over $\overline{\mathbb{Q}}$:
$$\mathcal{R}_{\alpha, \beta} = \left\{ (a_0, a_1, a_2) \in \overline{\mathbb{Q}}^3 : a_0 + a_1 X + a_2 Y = 0 \right\}.$$

A relation $(a_0, a_1, a_2) \in \mathcal{R}_{\alpha, \beta}$ is **nondegenerate** if $a_0 a_1 a_2 \ne 0$.

---

## C. Relation-Space Dimension Theorem

### Theorem (`RANK_TWO_TRINOMIAL_RELATION_SPACE_AT_MOST_ONE_DIMENSIONAL`)
Let $\alpha, \beta \in \mathbb{A}_{\mathbb{R}}$ be $\mathbb{Q}$-linearly independent. Then:
$$\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1.$$
If a nonzero relation exists, $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} = 1$.

**Evidence Class**: `PROVED_PAPER_DERIVATION` + `PROVED_WITH_EXTERNAL_GELFOND_SCHNEIDER`.  
**Lean Core**: `RiemannScope.trinomial_two_relations_cramer`.

### Invariant Proof
Suppose $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \ge 2$.
Then there exist two $\overline{\mathbb{Q}}$-linearly independent relation vectors $(a_0, a_1, a_2)$ and $(b_0, b_1, b_2)$ such that:
$$a_0 + a_1 X + a_2 Y = 0, \qquad b_0 + b_1 X + b_2 Y = 0.$$
Form the $2 \times 3$ algebraic coefficient matrix:
$$M = \begin{pmatrix} a_0 & a_1 & a_2 \\ b_0 & b_1 & b_2 \end{pmatrix}.$$
Because the rows are linearly independent over $\overline{\mathbb{Q}}$, $\operatorname{rank}_{\overline{\mathbb{Q}}}(M) = 2$.
The right nullspace $\ker(M) \subset \mathbb{C}^3$ is 1-dimensional and spanned by the vector of signed $2 \times 2$ minors:
$$\mathbf{v} = (\Delta_0, -\Delta_1, \Delta_2),$$
where:
$$\Delta_0 = a_1 b_2 - a_2 b_1, \qquad \Delta_1 = a_0 b_2 - a_2 b_0, \qquad \Delta_2 = a_0 b_1 - a_1 b_0.$$
Because $(1, X, Y)^T \in \ker(M)$ and $\dim \ker(M) = 1$, $(1, X, Y)^T = c \cdot \mathbf{v}$ for some $c \in \mathbb{C}^\times$.
Examining the first coordinate:
$$1 = c \cdot \Delta_0.$$
Therefore $\Delta_0 \ne 0$ is **strictly guaranteed** whenever $(1, X, Y)$ satisfies both relations, and $c = 1 / \Delta_0$.
Solving explicitly:
$$X = -\frac{\Delta_1}{\Delta_0} = \frac{a_2 b_0 - a_0 b_2}{a_1 b_2 - a_2 b_1} \in \overline{\mathbb{Q}}, \qquad Y = \frac{\Delta_2}{\Delta_0} = \frac{a_0 b_1 - a_1 b_0}{a_1 b_2 - a_2 b_1} \in \overline{\mathbb{Q}}.$$
Thus both $X = \tau^\alpha$ and $Y = \tau^\beta$ are algebraic:
$$\tau^\alpha \in \overline{\mathbb{Q}} \implies \alpha \in S_\tau, \qquad \tau^\beta \in \overline{\mathbb{Q}} \implies \beta \in S_\tau.$$
By the external Gelfond-Schneider / Baker theorem, $\dim_{\mathbb{Q}} S_\tau \le 1$.
Consequently, any two elements of $S_\tau$ are $\mathbb{Q}$-linearly dependent.
However, by hypothesis, $\alpha / \beta \notin \mathbb{Q}$, so $\alpha$ and $\beta$ are $\mathbb{Q}$-linearly independent. Contradiction.
Therefore $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1$. $\blacksquare$

---

## D. Exceptional-Direction Exclusion

### Theorem (`PAIRWISE_EXCEPTIONAL_DIRECTIONS_EXCLUDED`)
Assume there exists a nondegenerate relation $a_0 + a_1 X + a_2 Y = 0$ ($a_0 a_1 a_2 \ne 0$). Then:
$$\alpha \notin S_\tau, \qquad \beta \notin S_\tau, \qquad \beta - \alpha \notin S_\tau.$$

**Evidence Class**: `LEAN_PROVED_SOLVING_IDENTITIES` feeding `PROVED_PAPER_DERIVATION` + `EXTERNAL_GELFOND_SCHNEIDER`.

### Proof
1. If $\alpha \in S_\tau$, then $X \in \overline{\mathbb{Q}}$. Since $a_2 \ne 0$:
   $$Y = \frac{-a_0 - a_1 X}{a_2} \in \overline{\mathbb{Q}}.$$
   Then $\beta \in S_\tau$, which forces $\alpha / \beta \in \mathbb{Q}$, contradiction. (Lean 4: `RiemannScope.trinomial_exceptional_x_forces_exceptional_y`).
2. If $\beta \in S_\tau$, then $Y \in \overline{\mathbb{Q}}$. Since $a_1 \ne 0$:
   $$X = \frac{-a_0 - a_2 Y}{a_1} \in \overline{\mathbb{Q}},$$
   similarly forcing $\alpha \in S_\tau$, contradiction. (Lean 4: `RiemannScope.trinomial_exceptional_y_forces_exceptional_x`).
3. If $\beta - \alpha \in S_\tau$, then $Z = Y / X = \tau^{\beta - \alpha} \in \overline{\mathbb{Q}}^\times$.
   Dividing the relation by $X > 0$:
   $$\frac{a_0}{X} + a_1 + a_2 Z = 0 \implies \frac{a_0}{X} = -a_1 - a_2 Z.$$
   If $a_1 + a_2 Z = 0$, then $a_0 / X = 0 \implies a_0 = 0$, contradicting nondegeneracy ($a_0 \ne 0$).
   Thus $a_1 + a_2 Z \ne 0$, and:
   $$X = \frac{-a_0}{a_1 + a_2 Z} \in \overline{\mathbb{Q}}^\times.$$
   This forces $X \in \overline{\mathbb{Q}}$, hence $\alpha \in S_\tau$, reducing to Case 1. (Lean 4: `RiemannScope.trinomial_exceptional_ratio_forces_exceptional_coordinates`). $\blacksquare$

---

## E. Real Coefficient Normalization

### Theorem (`TRINOMIAL_COEFFICIENTS_REAL_NORMALIZABLE`)
If a nondegenerate trinomial relation exists with coefficients in $\overline{\mathbb{Q}}$, it is algebraically equivalent to one with coefficients in $\mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$.

**Evidence Class**: `PROVED_PAPER_DERIVATION`.

### Direct Elementary Proof
Since $\tau > 0$ and $\alpha, \beta \in \mathbb{R}$, the generators $X = \tau^\alpha > 0$ and $Y = \tau^\beta > 0$ are real numbers.
Taking complex conjugation of $a_0 + a_1 X + a_2 Y = 0$:
$$\overline{a_0} + \overline{a_1} X + \overline{a_2} Y = 0.$$
Thus $(\overline{a_0}, \overline{a_1}, \overline{a_2}) \in \mathcal{R}_{\alpha, \beta}$.
By Section C, $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1$.
Therefore:
$$(\overline{a_0}, \overline{a_1}, \overline{a_2}) = \lambda (a_0, a_1, a_2)$$
for some $\lambda \in \overline{\mathbb{Q}}^\times$.
Conjugating again yields $a_j = \overline{\lambda} \, \overline{a_j} = \lambda \overline{\lambda} a_j$, so $\lambda \overline{\lambda} = 1$.
We choose the phase multiplier:
$$\mu = \begin{cases} 1 + \lambda & \text{if } \lambda \ne -1, \\ i & \text{if } \lambda = -1. \end{cases}$$
Then:
- If $\lambda = -1$: $\overline{\mu a_j} = -i \overline{a_j} = -i (-a_j) = i a_j = \mu a_j$.
- If $\lambda \ne -1$:
  $$\overline{\mu a_j} = (1 + \overline{\lambda}) \overline{a_j} = (1 + \overline{\lambda}) \lambda a_j = (\lambda + \lambda \overline{\lambda}) a_j = (\lambda + 1) a_j = \mu a_j.$$
Thus $\mu a_j \in \mathbb{A}_{\mathbb{R}}$ for all $j$, and every nonzero trinomial relation can be rescaled to real algebraic coefficients. $\blacksquare$

---

## F. Sign Geometry

### Theorem (`MIXED_SIGN_NECESSARY`)
Let $a_0 + a_1 X + a_2 Y = 0$ be a normalized real relation with $a_0, a_1, a_2 \in \mathbb{A}_{\mathbb{R}}^\times$ and $X, Y > 0$.
Then the coefficients cannot all have the same sign. Exactly one coefficient has sign opposite to the other two.

**Evidence Class**: `LEAN_PROVED` (`RiemannScope.trinomial_same_sign_pos_impossible`, `RiemannScope.trinomial_same_sign_neg_impossible`).

Multiplying by $\pm 1$ gives exactly three positive affine orientations ($u, v \in \mathbb{A}_{\mathbb{R}}^{>0}$):
1. **$Y$ affine in $X$**: $a_2$ opposite sign $\implies Y = u + vX$ with $u = -a_0/a_2 > 0, v = -a_1/a_2 > 0$.
2. **$X$ affine in $Y$**: $a_1$ opposite sign $\implies X = u + vY$ with $u = -a_0/a_1 > 0, v = -a_2/a_1 > 0$.
3. **Unit affine in $X, Y$**: $a_0$ opposite sign $\implies 1 = uX + vY$ with $u = -a_1/a_0 > 0, v = -a_2/a_0 > 0$. $\blacksquare$

---

## G. Affine Exceptional Locus

Define the affine exceptional relation locus:
$$\mathcal{A}_\tau = \left\{ (\alpha, \beta) \in \mathbb{A}_{\mathbb{R}}^2 : 1, \tau^\alpha, \tau^\beta \text{ are linearly dependent over } \overline{\mathbb{Q}} \right\}.$$

The genuine minimal rank-two locus is:
$$\mathcal{A}_\tau^\circ = \mathcal{A}_\tau \setminus \left( (S_\tau \times \mathbb{A}_{\mathbb{R}}) \cup (\mathbb{A}_{\mathbb{R}} \times S_\tau) \cup \{(\alpha, \beta) : \beta - \alpha \in S_\tau\} \cup \{(\alpha, \beta) : \alpha / \beta \in \mathbb{Q}\} \right).$$
The open question is whether $\mathcal{A}_\tau^\circ$ is empty.

---

## H. Grade-Dilation Orbit & No Propagation

Given a candidate relation $f(1) = a_0 + a_1 X + a_2 Y = 0$, define the grade-dilation sequence:
$$f(n) = a_0 + a_1 X^n + a_2 Y^n, \qquad n \in \mathbb{Z}.$$

### Theorem (`NO_CANONICAL_ORBIT_VANISHING_PROPAGATION`)
A single relation $f(1) = 0$ **does not force** $f(2) = 0, f(3) = 0$, or any further orbit vanishing:
- Example: $X = 2, Y = 3$ with $a_0 = -5, a_1 = 1, a_2 = 1$.
  $f(1) = -5 + 2 + 3 = 0$.
  $f(2) = -5 + 4 + 9 = 8 \ne 0$.
TC transport does not produce an automatic contradictory chain of zero equations.

---

## I. Three-Point Orbit Rigidity

### Theorem (`THREE_CONSECUTIVE_DILATION_ORBIT_RIGIDITY`)
Let $1, X, Y$ be pairwise distinct positive reals. If for some integer $n$,
$$f(n) = f(n+1) = f(n+2) = 0,$$
then $a_0 = a_1 = a_2 = 0$.

**Evidence Class**: `LEAN_PROVED` (`RiemannScope.trinomial_three_consecutive_orbit_rigidity`).

### Proof
The system is $M_n \mathbf{a} = \mathbf{0}$, where:
$$\det(M_n) = X^n Y^n (X - 1)(Y - 1)(Y - X).$$
(Lean 4: `RiemannScope.trinomial_three_consecutive_orbit_determinant`).
Since $X, Y > 0$ and $1, X, Y$ are pairwise distinct, $\det(M_n) \ne 0$ (Lean 4: `RiemannScope.trinomial_three_consecutive_orbit_det_ne_zero`).
Therefore $a_0 = a_1 = a_2 = 0$. $\blacksquare$

---

## J. Generalized Vandermonde Theorem

For any three distinct integers $n_1 < n_2 < n_3$ and distinct positive bases $0 < x_1 < x_2 < x_3$:
$$V(n_1, n_2, n_3) = \det \begin{pmatrix} x_1^{n_1} & x_2^{n_1} & x_3^{n_1} \\ x_1^{n_2} & x_2^{n_2} & x_3^{n_2} \\ x_1^{n_3} & x_2^{n_3} & x_3^{n_3} \end{pmatrix} > 0.$$
By Chebyshev system theory (Karlin 1968), $f(n_1) = f(n_2) = f(n_3) = 0 \implies a_0 = a_1 = a_2 = 0$.
- Status: `PROVED_PAPER_DERIVATION` (general distinct integers); `LEAN_PROVED` for consecutive triples.

---

## K. Multiplicative-Group / S-Unit Theorem Audit

Primary literature reviewed:
1. **Evertse (1984)**: *On sums of S-units and linear recurrences*, Invent. Math. 73, 117–137.
2. **Evertse, Schlickewei, Schmidt (2002)**: *Linear equations in elements of groups of finite rank*, Ann. of Math. 155, 807–836.

### Exact Multiplicative Groups:
1. **Base Group**: $\Gamma_0 = \langle X, Y \rangle \subset \mathbb{R}_{>0}^\times$. For $\alpha / \beta \notin \mathbb{Q}$, $\Gamma_0 \cong \mathbb{Z}^2$ (rank 2).
2. **Ambient Solution Group**: The equation $a_0 + a_1 u + a_2 v = 0$ with independently varying $(u, v) \in \Gamma_0^2$ lives in $\Gamma_0 \times \Gamma_0$, a free abelian group of **rank 4**.
3. **Diagonal Orbit Group**: $\Delta_{\alpha, \beta} = \{(X^n, Y^n) : n \in \mathbb{Z}\}$ is a cyclic group of **rank 1**.

By the Evertse-Schlickewei-Schmidt theorem on linear equations in groups of finite rank, the number of nondegenerate solutions $(u, v) \in \Gamma_0 \times \Gamma_0$ to $a_0 + a_1 u + a_2 v = 0$ for a **fixed** algebraic triple $(a_0, a_1, a_2)$ is **finite**.

---

## L. Laurent / Mordell–Lang Audit

Primary literature reviewed:
1. **Laurent (1984)**: *Équations diophantiennes exponentielles*, Invent. Math. 78, 299–327.
2. **Hindry (1988)**: *Autour d'une conjecture de Serge Lang*, Ann. of Math. 128, 97–137.

### Subtorus Non-Degeneracy:
The affine line $L \subset \mathbb{G}_m^2$ defined by $a_0 + a_1 u + a_2 v = 0$ ($a_0 a_1 a_2 \ne 0$) contains no translate of an algebraic subtorus $u^p v^q = c$ in $\mathbb{G}_m^2$.
By Laurent's theorem, $L \cap (\Gamma_0 \times \Gamma_0)$ is finite:
$$\boxed{\texttt{FIXED\_COEFFICIENT\_TRINOMIAL\_SOLUTIONS\_FINITE}}.$$

### The Critical Non-Implication:
$$\boxed{\texttt{FINITE\_DOES\_NOT\_IMPLY\_EMPTY}}.$$
Finiteness of solutions for a given $(a_0, a_1, a_2)$ does **not** prove that $(X, Y)$ is not a solution, nor does it constrain relations when coefficients vary over $\overline{\mathbb{Q}}$.

---

## M. Canonical Examples

1. **Base-One Instance**:
   $$1, \quad 2\pi, \quad (2\pi)^{\sqrt{2}}, \qquad \alpha = 1, \; \beta = \sqrt{2}.$$
2. **Radical Pair Instance**:
   $$1, \quad (2\pi)^{\sqrt{2}}, \quad (2\pi)^{\sqrt{3}}, \qquad \alpha = \sqrt{2}, \; \beta = \sqrt{3}.$$

---

## N. Certified Sparse Exclusions & Support Accounting

Using `python-flint` Arb interval ball arithmetic at 128-bit precision, we evaluate:
$$V = a_0 + a_1 (X^{i_1} Y^{j_1}) + a_2 (X^{i_2} Y^{j_2})$$
over all 36 constant-anchored monomial supports up to degree $D = 3$ and primitive mixed-sign integer coefficient triples $\|a\|_\infty \le 10$.

### Support Universe Accounting:
- Total degree $\le 3$ monomials: 10 ($1, X, Y, X^2, XY, Y^2, X^3, X^2Y, XY^2, Y^3$).
- Total 3-monomial subsets in box: $\binom{10}{3} = 120$.
- **Constant-anchored supports tested**: $\binom{9}{2} = 36$ supports.
- **Partition of tested supports**:
  - $30$ genuine affine-rank-two supports;
  - $6$ affine-rank-one control supports ($X$-axis: $\{1, X, X^2\}, \{1, X, X^3\}, \{1, X^2, X^3\}$; $Y$-axis: $\{1, Y, Y^2\}, \{1, Y, Y^3\}, \{1, Y^2, Y^3\}$).
- **Candidate Count Partition**:
  - $2,523$ normalized coefficient triples per support;
  - $30 \times 2,523 = 75,690$ rank-two candidates;
  - $6 \times 2,523 = 15,138$ rank-one control candidates;
  - Total candidates certified: $90,828$.

| Canonical Instance | Constant-Anchored Supports Tested | Normalized Trinomials | Smallest Certified Lower Bound | Smallest Candidate $(a_0, a_1, a_2, M_1, M_2)$ | Scope | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Base-One** $(1, 2\pi, (2\pi)^{\sqrt{2}})$ | 36 (30 rank 2, 6 rank 1) | 90,828 | **0.02262** | $(9, 4, -10, Y, X)$ | Constant-anchored campaign | `CERTIFIED_FINITE_TRINOMIAL_EXCLUSION` |
| **Radical Pair** $(1, (2\pi)^{\sqrt{2}}, (2\pi)^{\sqrt{3}})$ | 36 (30 rank 2, 6 rank 1) | 90,828 | **0.08095** | $(6, 5, -9, XY, X^2)$ | Constant-anchored campaign | `CERTIFIED_FINITE_TRINOMIAL_EXCLUSION` |

**Honest Campaign Scope**: This campaign certifies nonvanishing only on the explicit finite set of 90,828 constant-anchored candidates. It does not certify general 3-monomial supports (which would require a Laurent box with negative exponents) nor arbitrary algebraic coefficients.

---

## O. Exact Remaining Open Problem

$$\boxed{
\begin{gathered}
\text{Do there exist } \alpha, \beta \in \mathbb{A}_{\mathbb{R}} \text{ with } \frac{\alpha}{\beta} \notin \mathbb{Q} \\
\text{and nonzero real algebraic coefficients } a_0, a_1, a_2 \in \mathbb{A}_{\mathbb{R}}^\times \text{ such that} \\
a_0 + a_1 (2\pi)^\alpha + a_2 (2\pi)^\beta = 0 \; ?
\end{gathered}
}$$
with $\alpha \notin S_\tau, \beta \notin S_\tau, \beta - \alpha \notin S_\tau$, and mixed coefficient signs.

Status:
$$\boxed{\texttt{MINIMAL\_RANK\_TWO\_TRINOMIAL\_EXISTENCE\_OPEN}}.$$

---

## P. Lean 4 Formalization Evidence Table

| Mathematical Claim | Lean Theorem | What Lean Proves | Additional Paper Step | External Theorem |
| :--- | :--- | :--- | :--- | :--- |
| **Support Translation** | `RiemannScope.trinomial_support_translation` | Factoring $\tau^{K_0}$ from 3-term sum for $\tau > 0$ | None | None |
| **Same-Sign Positivity** | `RiemannScope.trinomial_same_sign_pos_impossible` | $a_0 + a_1 X + a_2 Y \ne 0$ for $a_j, X, Y > 0$ | None | None |
| **Same-Sign Negativity** | `RiemannScope.trinomial_same_sign_neg_impossible` | $a_0 + a_1 X + a_2 Y \ne 0$ for $a_j < 0, X, Y > 0$ | None | None |
| **Cramer Coordinate Determination** | `RiemannScope.trinomial_two_relations_cramer` | Expresses $X, Y$ as rational functions of coefficients when $\Delta_0 \ne 0$ | Invariant nullspace proof that $\Delta_0 \ne 0$ is guaranteed, and field closure of $\overline{\mathbb{Q}}$ | Gelfond-Schneider ($\dim_{\mathbb{Q}} S_\tau \le 1$) |
| **Exceptional $X$ Solves $Y$** | `RiemannScope.trinomial_exceptional_x_forces_exceptional_y` | $Y = (-a_0 - a_1 X)/a_2$ for $a_2 \ne 0$ | Field closure of $\overline{\mathbb{Q}}$ and $S_\tau$ membership | Gelfond-Schneider ($\dim_{\mathbb{Q}} S_\tau \le 1$) |
| **Exceptional $Y$ Solves $X$** | `RiemannScope.trinomial_exceptional_y_forces_exceptional_x` | $X = (-a_0 - a_2 Y)/a_1$ for $a_1 \ne 0$ | Field closure of $\overline{\mathbb{Q}}$ and $S_\tau$ membership | Gelfond-Schneider ($\dim_{\mathbb{Q}} S_\tau \le 1$) |
| **Exceptional Ratio Solves $X$** | `RiemannScope.trinomial_exceptional_ratio_forces_exceptional_coordinates` | $X = -a_0 / (a_1 + a_2(Y/X))$ when denom $\ne 0$ | Proof that denom $\ne 0$ because $a_1 + a_2(Y/X) = 0 \implies a_0 = 0$, and field closure | Gelfond-Schneider ($\dim_{\mathbb{Q}} S_\tau \le 1$) |
| **Consecutive Orbit Determinant** | `RiemannScope.trinomial_three_consecutive_orbit_determinant` | $\det(M_n) = X^n Y^n (X-1)(Y-1)(Y-X)$ | None | None |
| **Orbit Determinant Nonvanishing** | `RiemannScope.trinomial_three_consecutive_orbit_det_ne_zero` | $\det(M_n) \ne 0$ for distinct positive bases | None | None |
| **Three-Consecutive Orbit Rigidity** | `RiemannScope.trinomial_three_consecutive_orbit_rigidity` | $f(n)=f(n+1)=f(n+2)=0 \implies a_j = 0$ | Dilation does not canonically propagate $f(1)=0$ into higher zeros | None |
| **Distinct Powers of $\tau > 1$** | `RiemannScope.tau_powers_pairwise_distinct_of_ne` | $\tau^\alpha \ne \tau^\beta$ for $\tau > 1, \alpha \ne \beta$ | None | None |
| **Non-Unit Power for Exponent $\ne 0$** | `RiemannScope.tau_pow_ne_one_of_ne_zero` | $\tau^\alpha \ne 1$ for $\tau > 1, \alpha \ne 0$ | None | None |

---

## Q. Non-Implications for RH

1. This task does not establish the Riemann Hypothesis, nor does it establish a bridge from $\zeta(s)$ to the ambient realization kernel.
2. `NO_ZETA_TO_KERNEL_BRIDGE_FOUND` remains strictly intact as an audit finding.
3. Positivity or certified nonvanishing on finite sparse grids does not establish transcendence or absence of relations on the continuum.

---

## Principal and Secondary Classifications

- **Primary**: `TRINOMIAL_FRONTIER_STRUCTURALLY_CLASSIFIED_EXISTENCE_OPEN`
- **Task Classification**: `TASK_TC_030R_TRINOMIAL_REPAIR_COMPLETE`
- **Secondary**:
  - `FIRST_OPEN_SUPPORT_SIZE_THREE`
  - `AFFINE_RANK_TWO_TRINOMIAL`
  - `RELATION_SPACE_AT_MOST_ONE_DIMENSIONAL`
  - `PAIRWISE_EXCEPTIONAL_DIRECTIONS_EXCLUDED`
  - `TRINOMIAL_COEFFICIENTS_REAL_NORMALIZABLE`
  - `MIXED_SIGN_NECESSARY`
  - `THREE_CONSECUTIVE_DILATION_ORBIT_RIGIDITY`
  - `FIXED_COEFFICIENT_SOLUTIONS_FINITE`
  - `FINITE_DOES_NOT_IMPLY_EMPTY`
  - `NO_CANONICAL_ORBIT_VANISHING_PROPAGATION`
  - `CERTIFIED_FINITE_TRINOMIAL_EXCLUSION`
  - `NO_ZETA_TO_KERNEL_BRIDGE_FOUND`
