# TASK-TC-030 Review: Minimal Rank-Two Trinomial Kernel, Relation-Space Rigidity, and Sparse Orbit Theorems

**Authoritative Status**: Research Review & Derivation Artifact  
**Task ID**: TASK-TC-030  
**Baseline Git HEAD**: `ae8a8dd6e39bb8d713cfc92fbf0dce38ad6fd090`  
**Primary Classification**: `TRINOMIAL_FRONTIER_STRUCTURALLY_CLASSIFIED_EXISTENCE_OPEN`  
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

TASK-TC-030 establishes the complete structural theory of this trinomial frontier:
- **Relation-Space Rigidity**: $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1$. Two independent relations force algebraic coordinates, contradicting $\dim_{\mathbb{Q}} S_\tau \le 1$.
- **Pairwise Exceptional-Direction Exclusion**: $\alpha \notin S_\tau$, $\beta \notin S_\tau$, and $\beta - \alpha \notin S_\tau$.
- **Real Coefficient Normalization**: Complex conjugation and 1-dimensionality force $(a_0, a_1, a_2)$ to be algebraically equivalent to a real algebraic triple in $\mathbb{A}_{\mathbb{R}}^\times$.
- **Sign Geometry**: Same-sign coefficients cannot vanish with positive generators. Every relation orients into positive affine forms: $Y = u + vX$, $X = u + vY$, or $1 = uX + vY$ ($u, v > 0$).
- **Three-Consecutive Orbit Rigidity**: Nonzero trinomials cannot vanish on three consecutive integer dilations $f(n) = f(n+1) = f(n+2) = 0$.
- **Multiplicative-Group Finiteness**: By Laurent (1984) and Evertse-Schlickewei-Schmidt (2002), for each fixed coefficient triple, solutions $(u, v) \in \Gamma^2$ are finite. However, **`FINITE_DOES_NOT_IMPLY_EMPTY`**; existence of one relation remains open.
- **Certified Sparse Exclusion**: Certified interval arithmetic (python-flint Arb at 128-bit precision) excludes all $90,828$ normalized trinomials across 36 supports up to degree $D=3$ and height $H=10$ on both canonical rank-two instances.

---

## A. Why Three Terms are the First Open Support

Let $F = \sum_{j=1}^m c_j [K_j] \in \overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}]$ be a nonzero kernel element with minimal support among nonempty vanishing subsums.

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

### Proof
Suppose $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \ge 2$.
Then there exist two $\overline{\mathbb{Q}}$-linearly independent relation vectors $(a_0, a_1, a_2)$ and $(b_0, b_1, b_2)$ such that:
$$a_0 + a_1 X + a_2 Y = 0, \qquad b_0 + b_1 X + b_2 Y = 0.$$
Consider the linear system for $(X, Y)$:
$$\begin{pmatrix} a_1 & a_2 \\ b_1 & b_2 \end{pmatrix} \begin{pmatrix} X \\ Y \end{pmatrix} = \begin{pmatrix} -a_0 \\ -b_0 \end{pmatrix}.$$
Let $\Delta = a_1 b_2 - a_2 b_1$.
1. If $\Delta \ne 0$, by Cramer's rule:
   $$X = \frac{a_2 b_0 - a_0 b_2}{a_1 b_2 - a_2 b_1} \in \overline{\mathbb{Q}}, \qquad Y = \frac{a_0 b_1 - a_1 b_0}{a_1 b_2 - a_2 b_1} \in \overline{\mathbb{Q}}.$$
   (Formalized in Lean 4: `trinomial_two_relations_cramer`).
2. If $\Delta = 0$, then $(a_1, a_2)$ and $(b_1, b_2)$ are proportional over $\overline{\mathbb{Q}}$. Since the vectors $(a_0, a_1, a_2)$ and $(b_0, b_1, b_2)$ are linearly independent, subtracting a suitable scalar multiple yields a relation with $a_1' = a_2' = 0$ and $a_0' \ne 0$, so $a_0' \cdot 1 = 0$, contradiction.

Thus $\Delta \ne 0$ and both $X = \tau^\alpha$ and $Y = \tau^\beta$ are algebraic:
$$\tau^\alpha \in \overline{\mathbb{Q}} \implies \alpha \in S_\tau, \qquad \tau^\beta \in \overline{\mathbb{Q}} \implies \beta \in S_\tau.$$
By external Gelfond-Schneider / Baker transcendence theory, $\dim_{\mathbb{Q}} S_\tau \le 1$.
Consequently, any two elements of $S_\tau$ are $\mathbb{Q}$-linearly dependent.
However, by hypothesis, $\alpha / \beta \notin \mathbb{Q}$, so $\alpha$ and $\beta$ are $\mathbb{Q}$-linearly independent. Contradiction.
Therefore $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} \le 1$. $\blacksquare$

---

## D. Exceptional-Direction Exclusion

### Theorem (`PAIRWISE_EXCEPTIONAL_DIRECTIONS_EXCLUDED`)
Assume there exists a nondegenerate relation $a_0 + a_1 X + a_2 Y = 0$ ($a_0 a_1 a_2 \ne 0$). Then:
$$\alpha \notin S_\tau, \qquad \beta \notin S_\tau, \qquad \beta - \alpha \notin S_\tau.$$

### Proof
1. If $\alpha \in S_\tau$, then $X \in \overline{\mathbb{Q}}$. Since $a_2 \ne 0$:
   $$Y = \frac{-a_0 - a_1 X}{a_2} \in \overline{\mathbb{Q}}.$$
   Then $\beta \in S_\tau$, which forces $\alpha / \beta \in \mathbb{Q}$, contradiction. (Lean 4: `trinomial_exceptional_x_forces_exceptional_y`).
2. If $\beta \in S_\tau$, then $Y \in \overline{\mathbb{Q}}$. Since $a_1 \ne 0$:
   $$X = \frac{-a_0 - a_2 Y}{a_1} \in \overline{\mathbb{Q}},$$
   similarly forcing $\alpha \in S_\tau$, contradiction. (Lean 4: `trinomial_exceptional_y_forces_exceptional_x`).
3. If $\beta - \alpha \in S_\tau$, then $Z = Y / X = \tau^{\beta - \alpha} \in \overline{\mathbb{Q}}^\times$.
   Dividing the relation by $X > 0$:
   $$\frac{a_0}{X} + a_1 + a_2 Z = 0 \implies \frac{a_0}{X} = -a_1 - a_2 Z.$$
   If $-a_1 - a_2 Z = 0$, then $a_0 / X = 0 \implies a_0 = 0$, contradicting nondegeneracy.
   Thus $-a_1 - a_2 Z \ne 0$, and:
   $$X = \frac{-a_0}{a_1 + a_2 Z} \in \overline{\mathbb{Q}}^\times.$$
   This forces $X \in \overline{\mathbb{Q}}$, hence $\alpha \in S_\tau$, reducing to Case 1. (Lean 4: `trinomial_exceptional_ratio_forces_exceptional_coordinates`). $\blacksquare$

---

## E. Real Coefficient Normalization

### Theorem (`TRINOMIAL_COEFFICIENTS_REAL_NORMALIZABLE`)
If a nondegenerate trinomial relation exists with coefficients in $\overline{\mathbb{Q}}$, it is algebraically equivalent to one with coefficients in $\mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$.

### Proof
Since $\tau > 0$ and $\alpha, \beta \in \mathbb{R}$, the generators $X = \tau^\alpha > 0$ and $Y = \tau^\beta > 0$ are real numbers.
Taking complex conjugation of $a_0 + a_1 X + a_2 Y = 0$:
$$\overline{a_0} + \overline{a_1} X + \overline{a_2} Y = 0.$$
Thus $(\overline{a_0}, \overline{a_1}, \overline{a_2}) \in \mathcal{R}_{\alpha, \beta}$.
By Section C, $\dim_{\overline{\mathbb{Q}}} \mathcal{R}_{\alpha, \beta} = 1$.
Therefore:
$$(\overline{a_0}, \overline{a_1}, \overline{a_2}) = \lambda (a_0, a_1, a_2)$$
for some $\lambda \in \overline{\mathbb{Q}}^\times$.
Conjugating again yields $a_j = \overline{\lambda} \, \overline{a_j} = |\lambda|^2 a_j$, so $|\lambda|^2 = 1$.
We seek $\mu \in \overline{\mathbb{Q}}^\times$ such that $\mu a_j \in \mathbb{R}$ for all $j$:
$$\overline{\mu a_j} = \mu a_j \iff \overline{\mu} \lambda a_j = \mu a_j \iff \mu = \overline{\mu} \lambda.$$
- If $\lambda = -1$: $\overline{a_j} = -a_j$, so $a_j \in i \mathbb{R}$. Setting $\mu = i \in \overline{\mathbb{Q}}^\times$ gives $\mu a_j = i a_j \in \mathbb{R}$.
- If $\lambda \ne -1$: Choose $\mu = 1 + \lambda \in \overline{\mathbb{Q}}^\times$.
  Then $\overline{\mu} = 1 + \overline{\lambda} = 1 + \lambda^{-1} = \frac{\lambda + 1}{\lambda} = \frac{\mu}{\lambda}$, so $\overline{\mu} \lambda = \mu$.
Thus $(\mu a_0, \mu a_1, \mu a_2) \in \mathbb{A}_{\mathbb{R}}^3 \setminus \{(0,0,0)\}$. $\blacksquare$

---

## F. Sign Geometry

### Theorem (`MIXED_SIGN_NECESSARY`)
Let $a_0 + a_1 X + a_2 Y = 0$ be a normalized real relation with $a_0, a_1, a_2 \in \mathbb{A}_{\mathbb{R}}^\times$ and $X, Y > 0$.
Then the coefficients cannot all have the same sign. Exactly one coefficient has sign opposite to the other two.

### Proof
If $a_0, a_1, a_2 > 0$, then $a_0 + a_1 X + a_2 Y > 0$, impossible. (Lean 4: `trinomial_same_sign_pos_impossible`).  
If $a_0, a_1, a_2 < 0$, then $a_0 + a_1 X + a_2 Y < 0$, impossible. (Lean 4: `trinomial_same_sign_neg_impossible`).  
Among three nonzero real numbers with mixed signs, either one is positive and two are negative, or one is negative and two are positive.
Multiplying by $\pm 1$ gives exactly three positive affine orientations:
1. **$Y$ affine in $X$**: $a_2$ opposite sign $\implies Y = u + vX$ with $u = -a_0/a_2 > 0, v = -a_1/a_2 > 0$.
2. **$X$ affine in $Y$**: $a_1$ opposite sign $\implies X = u + vY$ with $u = -a_0/a_1 > 0, v = -a_2/a_1 > 0$.
3. **Unit affine in $X, Y$**: $a_0$ opposite sign $\implies 1 = uX + vY$ with $u = -a_1/a_0 > 0, v = -a_2/a_0 > 0$. $\blacksquare$

---

## G. Affine Exceptional Locus

Define the affine exceptional relation locus:
$$\mathcal{A}_\tau = \left\{ (\alpha, \beta) \in \mathbb{A}_{\mathbb{R}}^2 : 1, \tau^\alpha, \tau^\beta \text{ are linearly dependent over } \overline{\mathbb{Q}} \right\}.$$

### Distinction from $S_\tau$:
- If $\alpha \in S_\tau$ or $\beta \in S_\tau$, then $(\alpha, \beta) \in \mathcal{A}_\tau$ trivially via a 2-term subrelation.
- If $\alpha / \beta \in \mathbb{Q}$, then $(\alpha, \beta) \in \mathcal{A}_\tau \iff \alpha \in S_\tau$.
- The **genuine minimal rank-two locus** is:
  $$\mathcal{A}_\tau^\circ = \mathcal{A}_\tau \setminus \left( (S_\tau \times \mathbb{A}_{\mathbb{R}}) \cup (\mathbb{A}_{\mathbb{R}} \times S_\tau) \cup \{(\alpha, \beta) : \beta - \alpha \in S_\tau\} \cup \{(\alpha, \beta) : \alpha / \beta \in \mathbb{Q}\} \right).$$
The open question is whether $\mathcal{A}_\tau^\circ$ is empty.

---

## H. Grade-Dilation Orbit

Given a candidate relation $f(1) = a_0 + a_1 X + a_2 Y = 0$, define the grade-dilation sequence:
$$f(n) = a_0 + a_1 X^n + a_2 Y^n, \qquad n \in \mathbb{Z}.$$
This corresponds to dilating the nonzero grades by common integer factor $n$:
$$a_0 \tau^0 + a_1 \tau^{n\alpha} + a_2 \tau^{n\beta} = f(n).$$

### No Canonical Propagation:
$f(1) = 0$ imposes **no automatic constraint** on $f(2), f(3), \ldots$:
- Example: $X = 2, Y = 3$ with $a_0 = -5, a_1 = 1, a_2 = 1$.
  $f(1) = -5 + 2 + 3 = 0$.
  $f(2) = -5 + 4 + 9 = 8 \ne 0$.
TC transport does not imply $f(1) = 0 \implies f(2) = 0$.

---

## I. Three-Point Orbit Rigidity

### Theorem (`THREE_CONSECUTIVE_DILATION_ORBIT_RIGIDITY`)
Let $1, X, Y$ be pairwise distinct positive reals. If for some integer $n$,
$$f(n) = f(n+1) = f(n+2) = 0,$$
then $a_0 = a_1 = a_2 = 0$.

### Proof
The system is $M_n \mathbf{a} = \mathbf{0}$, where:
$$M_n = \begin{pmatrix} 1 & X^n & Y^n \\ 1 & X^{n+1} & Y^{n+1} \\ 1 & X^{n+2} & Y^{n+2} \end{pmatrix}.$$
Subtract row 1 from row 2 and row 2 from row 3:
$$\det(M_n) = X^n Y^n (X - 1)(Y - 1)(Y - X).$$
(Formalized in Lean 4: `trinomial_three_consecutive_orbit_determinant`).
Since $X, Y > 0$ and $1, X, Y$ are pairwise distinct:
$$X^n \ne 0, \quad Y^n \ne 0, \quad X - 1 \ne 0, \quad Y - 1 \ne 0, \quad Y - X \ne 0.$$
Thus $\det(M_n) \ne 0$. (Lean 4: `trinomial_three_consecutive_orbit_det_ne_zero`).
Since the determinant is nonzero, the only solution to $M_n \mathbf{a} = \mathbf{0}$ is $a_0 = a_1 = a_2 = 0$. (Lean 4: `trinomial_three_consecutive_orbit_rigidity`). $\blacksquare$

---

## J. Generalized Vandermonde Theorem

For any three distinct integers $n_1 < n_2 < n_3$ and distinct positive bases $0 < x_1 < x_2 < x_3$:
$$V(n_1, n_2, n_3) = \det \begin{pmatrix} x_1^{n_1} & x_2^{n_1} & x_3^{n_1} \\ x_1^{n_2} & x_2^{n_2} & x_3^{n_2} \\ x_1^{n_3} & x_2^{n_3} & x_3^{n_3} \end{pmatrix}.$$
By the classical theory of generalized Vandermonde matrices / Chebyshev systems (Gantmacher & Krein 1950, Karlin 1968), $V(n_1, n_2, n_3) > 0$.
Therefore, $f(n_1) = f(n_2) = f(n_3) = 0 \implies a_0 = a_1 = a_2 = 0$.
- Status: `PROVED_PAPER_DERIVATION` (general distinct integers); `LEAN_PROVED` for consecutive triples.

---

## K. Multiplicative-Group / S-Unit Theorem Audit

Primary literature reviewed:
1. **Evertse (1984)**: *On sums of S-units and linear recurrences*, Invent. Math. 73, 117–137.
2. **Evertse, Schlickewei, Schmidt (2002)**: *Linear equations in elements of groups of finite rank*, Ann. of Math. 155, 807–836.

Let $\Gamma = \langle X, Y \rangle \subset \mathbb{R}_{>0}^\times$.
Because $\alpha / \beta \notin \mathbb{Q}$, $X^u Y^v = 1 \implies u\alpha + v\beta = 0 \implies u = v = 0$.
Thus $\Gamma \cong \mathbb{Z}^2$ is a free abelian group of rank 2.
Consider the linear equation:
$$a_0 + a_1 u + a_2 v = 0, \qquad (u, v) \in \Gamma^2.$$
The Evertse-Schlickewei-Schmidt theorem bounds the number of nondegenerate solutions in terms of the rank $r = 2$ and the number of terms $k = 3$:
$$\text{Number of solutions} \le A(3, 2) < \infty.$$
Thus, for any **fixed** algebraic triple $(a_0, a_1, a_2)$, the number of solutions in $\Gamma^2$ is **finite**.

---

## L. Laurent / Mordell–Lang Audit

Primary literature reviewed:
1. **Laurent (1984)**: *Équations diophantiennes exponentielles*, Invent. Math. 78, 299–327.
2. **Hindry (1988)**: *Autour d'une conjecture de Serge Lang*, Ann. of Math. 128, 97–137.

### Subtorus Non-Degeneracy:
Consider the affine line $L \subset \mathbb{G}_m^2$ defined by $a_0 + a_1 u + a_2 v = 0$ with $a_0 a_1 a_2 \ne 0$.
A 1-dimensional algebraic subtorus $T \subset \mathbb{G}_m^2$ is defined by a monomial relation $u^p v^q = 1$ with $(p, q) \ne (0, 0) \in \mathbb{Z}^2$.
A coset translate $c \cdot T$ has parametric form $u^p v^q = c$.
Can $L$ contain a coset $c \cdot T$?
- If $(p, q) = (1, 0)$, $u = c$ (vertical line). In $L$, $a_0 + a_1 c + a_2 v = 0 \implies v$ is constant, not a 1D curve.
- If $(p, q) = (0, 1)$, horizontal line.
- If $p \cdot q \ne 0$, $u^p v^q = c$ is a nonlinear curve in the plane. A line cannot contain a nonlinear curve.

Thus $L$ contains **no** positive-dimensional subtorus coset!
By Laurent's theorem, $L \cap \Gamma$ is finite:
$$\boxed{\texttt{FIXED\_COEFFICIENT\_TRINOMIAL\_SOLUTIONS\_FINITE}}.$$

### The Critical Non-Implication:
$$\boxed{\texttt{FINITE\_DOES\_NOT\_IMPLY\_EMPTY}}.$$
Finiteness of solutions for a given $(a_0, a_1, a_2)$ does **not** imply that the specific point $(u, v) = (X, Y)$ is not a solution, nor does it exclude the existence of another triple $(a_0', a_1', a_2')$ having $(X, Y)$ as its unique solution!
Thus, Laurent and ESS do not resolve the existence question.

---

## M. Canonical Examples

We isolate two canonical minimal rank-two instances:
1. **Base-One Instance**:
   $$1, \quad 2\pi, \quad (2\pi)^{\sqrt{2}}.$$
   Here $\alpha = 1, \beta = \sqrt{2}$, with ratio $\alpha / \beta = 1/\sqrt{2} \notin \mathbb{Q}$.
2. **Radical Pair Instance**:
   $$1, \quad (2\pi)^{\sqrt{2}}, \quad (2\pi)^{\sqrt{3}}.$$
   Here $\alpha = \sqrt{2}, \beta = \sqrt{3}$, with ratio $\sqrt{2/3} \notin \mathbb{Q}$.

Neither is called "the" unique minimal instance; both represent authentic, minimal rank-two instances.

---

## N. Certified Sparse Exclusions

Using `python-flint` Arb interval ball arithmetic at 128-bit precision, we evaluate:
$$V = a_0 + a_1 (X^{i_1} Y^{j_1}) + a_2 (X^{i_2} Y^{j_2})$$
over all 36 distinct monomial supports up to degree $D = 3$ and all normalized primitive mixed-sign integer coefficient triples $\|a\|_\infty \le 10$:

| Canonical Instance | Monomial Supports | Normalized Trinomials | Smallest Certified Lower Bound | Smallest Candidate $(a_0, a_1, a_2, M_1, M_2)$ | Time (s) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Base-One** $(1, 2\pi, (2\pi)^{\sqrt{2}})$ | 36 | 90,828 | **0.02262** | $(9, 4, -10, Y, X)$ | 0.257 | `CERTIFIED_FINITE_TRINOMIAL_EXCLUSION` |
| **Radical Pair** $(1, (2\pi)^{\sqrt{2}}, (2\pi)^{\sqrt{3}})$ | 36 | 90,828 | **0.08095** | $(6, 5, -9, XY, X^2)$ | 0.270 | `CERTIFIED_FINITE_TRINOMIAL_EXCLUSION` |

### Strict Certification Safeguards:
1. No midpoints used: every distance is an Arb `abs_lower()` interval bound.
2. Fails closed on unsupported expressions.
3. Exact synthetic controls ($Y = 1 + X$ and $Y = X^2$) contain 0 and return `RELATION_DETECTED` rather than falsely certifying exclusion.

---

## O. Exact Remaining Open Problem

After all reductions (Section A–L), the exact open mathematical core is:
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

## P. Implications for TC

1. **Separation by Support Complexity**: The ambient-kernel programme is now cleanly separated by support complexity ($m = 1, 2, 3$) as well as rational support rank ($r = 0, 1, 2$).
2. **Finite-Dimensional Relation Rigidity**: A genuine rank-two kernel element cannot belong to a high-dimensional relation space; it is rigid ($\dim \mathcal{R}_{\alpha, \beta} = 1$).
3. **No Automatic Contradiction**: A single trinomial relation does not propagate into an infinite contradictory grade orbit under TC dilation. Orbit rigidity shows that vanishing on 3 consecutive grades is impossible, but a single relation remains geometrically unconstrained by dilation alone.

---

## Q. Non-Implications for RH

1. This task does not establish the Riemann Hypothesis, nor does it establish a bridge from $\zeta(s)$ to the ambient realization kernel.
2. `NO_ZETA_TO_KERNEL_BRIDGE_FOUND` remains strictly intact as an audit finding.
3. Positivity or certified nonvanishing on finite sparse grids does not establish transcendence or absence of relations on the continuum.

---

## Principal and Secondary Classifications

- **Primary**: `TRINOMIAL_FRONTIER_STRUCTURALLY_CLASSIFIED_EXISTENCE_OPEN`
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
  - `NO_CANONICAL_RELATION_PROPAGATION`
  - `CERTIFIED_FINITE_TRINOMIAL_EXCLUSION`
  - `NO_ZETA_TO_KERNEL_BRIDGE_FOUND`
