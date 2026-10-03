# TASK-TC-018: Graded Arithmetic Monoid, Grade Units, and the TC Closure Constraint

**Document ID**: `docs/reviews/TC_GRADED_ARITHMETIC_CLOSURE.md`  
**Author**: Antigravity (Advanced Agentic Coding / DeepMind)  
**Date**: October 3, 2026  
**Status**: `REVIEWED_THEORETICAL`  
**Dependencies**: `docs/reviews/TC_ANALYTIC_ARITHMETIC_INTERTWINING.md`, `MATH_CONTRACT.md` §9.4–§9.5, `TRANSCENDENTAL_CONTINUATION.md` §23–§24  
**Primary Artifact**: `data/tc_graded_arithmetic_closure.json`  
**Test Suite**: `tests/test_tc_graded_arithmetic_closure.py` (13/13 passing)  
**Formalization**: `formal/RiemannScope/GradedMonoid.lean` (`lake build` successful)

---

## Executive Summary

TASK-TC-017 established the rigorous distinction between analytic TC dilation $A_K[\zeta](s) = \zeta(\tau^{-K} s)$ (base power $n \mapsto n^{\tau^{-K}}$, log dilation $x \mapsto \tau^{-K} x$) and arithmetic grid dilation $D_J[\zeta](s) = \tau^{-J s} \zeta(s)$ (linear scaling $n \mapsto \tau^J n$, log translation $x \mapsto x + J \log \tau$), proving their semidirect commutation law $A_K D_J = D_{J \tau^{-K}} A_K$. It also noted that an individual arithmetic grid $L_K = \tau^K (\mathbb{Z} \setminus \{0\})$ is not multiplicatively closed ($L_K \cdot L_K = L_{2K} \ne L_K$).

TASK-TC-018 attacks the resulting algebraic problem directly, answering whether the collection of all TC arithmetic grids forms a coherent multiplicative structure, how analytic dilation acts on it, whether an algebraic closure constraint arises, and resolving the **Governing Decision Point (Fork A vs Fork B)**:

1. **Complete Graded Arithmetic Object**: The full grid family is an $\mathbb{A}_{\mathbb{R}}$-graded commutative monoid $\mathcal{M}_\tau = \mathbb{A}_{\mathbb{R}} \times \mathbb{Z}_{\ne 0}$ (the direct product of the additive group of real algebraic numbers and the multiplicative monoid of nonzero integers) under $(K, n) \star (J, m) = (K+J, n m)$, with realization homomorphism $\Phi_\tau(K, n) = n \tau^K$ mapping into $(\mathbb{R}^\times, \times)$.
2. **Grade Units and Unit Group**: The unit group is $U(\mathcal{M}_\tau) = \mathbb{A}_{\mathbb{R}} \times \{\pm 1\} \cong (\mathbb{A}_{\mathbb{R}}, +) \times (\mathbb{Z}/2\mathbb{Z})$. Every algebraic grade defines an invertible **grade unit** $u_K = (K, 1)$ satisfying $u_K \star u_J = u_{K+J}$ and $u_K^{-1} = u_{-K}$.
3. **No New Primes**: Every element factors uniquely into a grade unit, a sign, and native prime factors:
   $$(K, n) = u_K \star (0, \operatorname{sgn} n) \star \prod_{p \in \mathcal{P}} (0, p)^{v_p(|n|)}.$$
   TC grades do not create new primes; the elements $p \tau^K$ are native primes transported by grade units.
4. **Quotient Recovers Integer Arithmetic**: The quotient by grade units recovers ordinary integer arithmetic: $\mathcal{M}_\tau / U_{\mathrm{grade}} \cong (\mathbb{Z}_{\ne 0}, \times)$. Every element $(K, n)$ projects onto the single arithmetic referent $n$.
5. **Dirichlet Character and Refined Euler Product**: The canonical character $\chi_s(K, n) = \tau^{-Ks} n^{-s}$ yields $D_K[\zeta](s) = \chi_s(u_K) \zeta(s) = \tau^{-Ks} \prod_p (1 - p^{-s})^{-1}$. The fixed-grade Dirichlet series is a global grade-unit twist of the universal native Euler product, not an independent Euler product.
6. **Rational-Grade Escape Theorem**: For every nonzero rational grade $K \in \mathbb{Q} \setminus \{0\}$ and nonzero algebraic grade $J \in \mathbb{A}_{\mathbb{R}} \setminus \{0\}$, $J \tau^{-K}$ is transcendental, hence $J \tau^{-K} \notin \mathbb{A}_{\mathbb{R}}$. Under analytic dilation, $(J, n) \mapsto (J \tau^{-K}, n^{\tau^{-K}})$ simultaneously escapes both the algebraic grade domain $\mathbb{A}_{\mathbb{R}}$ and the integer base lattice $\mathbb{Z}$.
7. **Resolution of Governing Decision Point (Fork B)**: Algebraic-grade coordinate closure is NOT an intrinsic requirement of the Riemann zeta function or TC; it is an imposed convention on the indexing set. The escape $J \tau^{-K} \notin \mathbb{A}_{\mathbb{R}}$ is an unconditional property of $\tau$ that holds identically whether RH is true or false ($\delta$-independent). Therefore, **Fork B is proved**: analytic dilation naturally escapes into the ambient completion $\mathbb{A}_{\mathbb{R}} \cdot \tau^{\mathbb{A}_{\mathbb{R}}} \subset \mathbb{R}$, with no contradiction and no required closure.
8. **Origin of the Spectral Detector $B_\rho(K)$**: The true spectral detector does not arise from coordinate closure; it is the **bilateral reflection defect of the normalized grade-unit character**:
   $$|\widehat{\chi}_\rho(u_K)| + |\widehat{\chi}_{1-\rho}(u_K)| - 2 = \tau^{K \delta} + \tau^{-K \delta} - 2 = 4\sinh^2\left(\frac{K \delta \log \tau}{2}\right) = B_\rho(K),$$
   which is strictly positive off-line ($\delta \ne 0$) and vanishes if and only if $\delta = 0$.

---

## Detailed Audit Questions (A through O)

### A. What is the correct complete arithmetic object behind the grids?

The previous sprint correctly noted that an individual arithmetic grid $L_K = \tau^K (\mathbb{Z} \setminus \{0\})$ is not multiplicatively closed:
$$\tau^K n \cdot \tau^K m = \tau^{2K} nm \in L_{2K} \ne L_K \qquad (K \ne 0).$$
However, the collection of all grids together carries a canonical multiplicative structure.

The correct algebraic object is the **$\mathbb{A}_{\mathbb{R}}$-graded commutative monoid**:
$$\mathcal{M}_\tau = \mathbb{A}_{\mathbb{R}} \times \mathbb{Z}_{\ne 0},$$
or for positive arithmetic, $\mathcal{M}_\tau^+ = \mathbb{A}_{\mathbb{R}} \times \mathbb{Z}_{\ge 1}$.

As an abstract algebraic structure, $\mathcal{M}_\tau$ is the **direct product monoid**:
$$\mathcal{M}_\tau = (\mathbb{A}_{\mathbb{R}}, +) \times (\mathbb{Z}_{\ne 0}, \times),$$
formed by the additive abelian group of real algebraic numbers $(\mathbb{A}_{\mathbb{R}}, +)$ and the commutative multiplicative monoid of nonzero integers $(\mathbb{Z}_{\ne 0}, \times)$.

It is graded by the group $(\mathbb{A}_{\mathbb{R}}, +)$:
$$\mathcal{M}_\tau = \bigsqcup_{K \in \mathbb{A}_{\mathbb{R}}} \mathcal{M}_{\tau, K}, \qquad \mathcal{M}_{\tau, K} = \{K\} \times \mathbb{Z}_{\ne 0},$$
satisfying the grading property:
$$\mathcal{M}_{\tau, K} \star \mathcal{M}_{\tau, J} \subseteq \mathcal{M}_{\tau, K+J}.$$

---

### B. Is it multiplicatively closed?

**Yes.** The multiplication law is:
$$(K, n) \star (J, m) = (K + J, n m).$$
- **Closure**: For any $K, J \in \mathbb{A}_{\mathbb{R}}$ and $n, m \in \mathbb{Z}_{\ne 0}$, $K + J \in \mathbb{A}_{\mathbb{R}}$ (since $\mathbb{A}_{\mathbb{R}}$ is an additive group) and $nm \in \mathbb{Z}_{\ne 0}$.
- **Identity**: $e = (0, 1)$ satisfies $(K, n) \star (0, 1) = (K, n)$.
- **Associativity and Commutativity**: Inherited directly from addition on $\mathbb{A}_{\mathbb{R}}$ and multiplication on $\mathbb{Z}_{\ne 0}$.

The **realization map** is defined by:
$$\Phi_\tau: \mathcal{M}_\tau \to \mathbb{R}^\times, \qquad \Phi_\tau(K, n) = n \tau^K.$$
It is an exact monoid homomorphism:
$$\Phi_\tau((K, n) \star (J, m)) = \Phi_\tau(K+J, nm) = (nm) \tau^{K+J} = (n \tau^K)(m \tau^J) = \Phi_\tau(K, n) \Phi_\tau(J, m).$$
The image $\Phi_\tau(\mathcal{M}_\tau) = L_\tau = \bigcup_{K \in \mathbb{A}_{\mathbb{R}}} L_K$ is a closed multiplicative submonoid of $(\mathbb{R}^\times, \times)$.

---

### C. What are its units?

An element $(K, n) \in \mathcal{M}_\tau$ is invertible if and only if there exists $(J, m) \in \mathcal{M}_\tau$ such that:
$$(K, n) \star (J, m) = (K + J, nm) = (0, 1).$$
This requires:
$$K + J = 0 \implies J = -K \in \mathbb{A}_{\mathbb{R}},$$
$$nm = 1 \text{ in } \mathbb{Z}_{\ne 0} \implies n = m \in \{1, -1\}.$$

Therefore, the unit group of $\mathcal{M}_\tau$ is:
$$U(\mathcal{M}_\tau) = \mathbb{A}_{\mathbb{R}} \times \{1, -1\} \cong (\mathbb{A}_{\mathbb{R}}, +) \times (\mathbb{Z}/2\mathbb{Z}).$$

For the positive monoid $\mathcal{M}_\tau^+ = \mathbb{A}_{\mathbb{R}} \times \mathbb{Z}_{\ge 1}$, the unit group consists entirely of the **grade units**:
$$U_{\mathrm{grade}} = \{ u_K = (K, 1) : K \in \mathbb{A}_{\mathbb{R}} \} \cong (\mathbb{A}_{\mathbb{R}}, +).$$

The grade units satisfy:
- $u_K \star u_J = (K+J, 1) = u_{K+J}$,
- $u_0 = (0, 1) = e$,
- $u_K^{-1} = (-K, 1) = u_{-K}$.

---

### D. Does ordinary prime factorization survive up to grade units?

**Yes.** In $\mathcal{M}_\tau$, an element $(K, n)$ is irreducible if and only if $|n| = p$ is a prime number in $\mathbb{Z}_{\ge 1}$.

Every element $(K, n) \in \mathcal{M}_\tau$ has a unique canonical factorization:
$$(K, n) = u_K \star (0, \operatorname{sgn} n) \star \prod_{p \in \mathcal{P}} (0, p)^{v_p(|n|)},$$
where $\mathcal{P} = \{2, 3, 5, 7, 11, \dots\}$ is the set of native primes and $v_p(|n|)$ is the standard $p$-adic valuation.

**Theorem (TC grades do not create new primes)**:  
The prime elements of $\mathcal{M}_\tau$ modulo the unit group $U(\mathcal{M}_\tau)$ are in canonical bijection with the native rational primes:
$$\mathrm{Irr}(\mathcal{M}_\tau) / U(\mathcal{M}_\tau) \cong \mathcal{P}.$$
The elements $p \tau^K = \Phi_\tau(u_K \star (0, p))$ are NOT independent primes. They are simply the native prime elements $(0, p)$ transported by the grade unit $u_K$.

---

### E. Does quotienting by grade units recover native integer arithmetic?

**Yes.** Consider the equivalence relation on $\mathcal{M}_\tau$ induced by the grade-unit action:
$$(K, n) \sim_{U_{\mathrm{grade}}} (J, m) \iff \exists A \in \mathbb{A}_{\mathbb{R}} : (K, n) = u_A \star (J, m) = (J+A, m).$$
This equivalence holds if and only if $n = m$.

The projection map:
$$\pi: \mathcal{M}_\tau \to \mathbb{Z}_{\ne 0}, \qquad \pi(K, n) = n$$
is a surjective monoid homomorphism with kernel $\ker \pi = U_{\mathrm{grade}}$.

By the First Isomorphism Theorem for monoids:
$$\mathcal{M}_\tau / U_{\mathrm{grade}} \cong (\mathbb{Z}_{\ne 0}, \times), \qquad \mathcal{M}_\tau^+ / U_{\mathrm{grade}} \cong (\mathbb{Z}_{\ge 1}, \times).$$

This provides a rigorous algebraic foundation for the TC concept of **"many distinct graded representations of one arithmetic referent"**: each coset in $\mathcal{M}_\tau / U_{\mathrm{grade}}$ consists of all pairs $(K, n)$ with $K \in \mathbb{A}_{\mathbb{R}}$, all projecting to the identical native integer $n$.

---

### F. What is the canonical Dirichlet character?

For $s \in \mathbb{C}$ and $(K, n) \in \mathcal{M}_\tau^+$, the canonical Dirichlet character is:
$$\chi_s(K, n) = \Phi_\tau(K, n)^{-s} = (n \tau^K)^{-s} = \tau^{-Ks} n^{-s}.$$

Multiplicativity is exact:
$$\chi_s((K, n) \star (J, m)) = \chi_s(K+J, nm) = \tau^{-(K+J)s} (nm)^{-s} = (\tau^{-Ks} n^{-s})(\tau^{-Js} m^{-s}) = \chi_s(K, n) \chi_s(J, m).$$

Factorization through the grade unit:
$$\chi_s(K, n) = \chi_s(u_K \star (0, n)) = \chi_s(u_K) \chi_s(0, n) = \tau^{-Ks} n^{-s}.$$

Evaluating the character sum over a fixed-grade coset $\mathcal{M}_{\tau, K}^+ = \{K\} \times \mathbb{Z}_{\ge 1}$:
$$\sum_{n=1}^\infty \chi_s(K, n) = \sum_{n=1}^\infty \tau^{-Ks} n^{-s} = \tau^{-Ks} \zeta(s) = D_K[\zeta](s).$$
Thus, arithmetic-grid dilation $D_K[\zeta]$ is precisely the Dirichlet character sum over the grade-$K$ slice of the graded monoid $\mathcal{M}_\tau^+$.

---

### G. What is the proper Euler-product interpretation?

In TASK-TC-017, we proved that treating the elements $\tau^K p$ as independent primes and writing:
$$\prod_{p \in \mathcal{P}} \left(1 - (\tau^K p)^{-s}\right)^{-1} = \sum_{n=1}^\infty \tau^{-K \Omega(n) s} n^{-s} \ne \tau^{-Ks} \zeta(s)$$
fails because $\Omega(n) = \sum v_p(n)$ counts prime factors with multiplicity.

The graded monoid resolves this completely. Since $(K, n) = u_K \star (0, n)$, the grade $K$ belongs to the grade unit $u_K$, not to individual prime factors. The Dirichlet series factors as:
$$D_K[\zeta](s) = \chi_s(u_K) \sum_{n=1}^\infty \chi_s(0, n) = \tau^{-Ks} \prod_{p \in \mathcal{P}} (1 - p^{-s})^{-1}.$$

**Conclusion**:  
The fixed-grade arithmetic grid does not possess an independent prime factorization system or an independent Euler product. It possesses the single, universal native Euler product multiplied by a single global grade-unit twist $\chi_s(u_K) = \tau^{-Ks}$.

---

### H. How does analytic TC dilation act on graded arithmetic coordinates?

Analytic TC dilation acts on complex functions by $A_K[F](s) = F(\tau^{-K} s)$.  
Applied to the canonical Dirichlet character $\chi_s(J, n) = \tau^{-Js} n^{-s}$:
$$A_K[\chi_s(J, n)] = \chi_{\tau^{-K} s}(J, n) = \tau^{-J(\tau^{-K} s)} n^{-\tau^{-K} s} = \tau^{-(J \tau^{-K}) s} (n^{\tau^{-K}})^{-s}.$$

In terms of coordinate pairs, analytic TC dilation induces the transformation:
$$(J, n) \mapsto \left( J \tau^{-K}, \; n^{\tau^{-K}} \right).$$

---

### I. Does analytic dilation preserve the canonical algebraic grade domain?

**No.** Analytic TC dilation simultaneously escapes **both** canonical coordinates:
1. **Grade Coordinate Escape**: $J \mapsto J \tau^{-K}$. For $K \in \mathbb{Q} \setminus \{0\}$ and $J \in \mathbb{A}_{\mathbb{R}} \setminus \{0\}$, $J \tau^{-K} \notin \mathbb{A}_{\mathbb{R}}$ (escapes algebraic numbers into transcendental reals by Lindemann's theorem).
2. **Base Coordinate Escape**: $n \mapsto n^{\tau^{-K}}$. For $K \ne 0$ and $n \ge 2$, $n^{\tau^{-K}} \notin \mathbb{Z}$ (escapes integers into non-integer reals).
   - *Elementary Nonintegrality Witness*: For $K > 0$ and $n = 2$, since $\tau = 2\pi > 1$, we have $0 < \tau^{-K} < 1$, which implies $1 < 2^{\tau^{-K}} < 2$. The open interval $(1, 2)$ contains no integers, proving rigorously that $2^{\tau^{-K}} \notin \mathbb{Z}$.
   - *Transcendence Status Classification*: The arithmetic nature of $n^{\tau^{-K}}$ (algebraic irrational vs. transcendental) is classified as **OPEN**. Note that Gelfond–Schneider requires an algebraic base $\alpha \ne 0, 1$ and an irrational *algebraic* exponent $\beta$. Here the exponent $\tau^{-K}$ is transcendental, so Gelfond–Schneider does not apply.
   - *Counter-Control ($\alpha = \log_2 3$)*: Let $\alpha = \log_2 3$. Then $2^\alpha = 3 \in \mathbb{Z}$. The exponent $\alpha$ is irrational (since $2^p = 3^q$ has no integer solutions), and if $\alpha$ were algebraic, Gelfond–Schneider would force $2^\alpha = 3$ to be transcendental, contradiction. Hence $\alpha$ is transcendental, yet $2^\alpha$ is an integer. This proves:
     $$\alpha \text{ transcendental} \not\Rightarrow n^\alpha \text{ transcendental}.$$
     Therefore, base transcendence of $n^{\tau^{-K}}$ must not be asserted as a theorem; exact elementary nonintegrality suffices.

---

### J. Prove the rational-grade escape theorem.

**Theorem (Rational-Grade Escape)**:  
For every nonzero rational grade $K \in \mathbb{Q} \setminus \{0\}$ and every nonzero real algebraic number $J \in \mathbb{A}_{\mathbb{R}} \setminus \{0\}$:
$$J \tau^{-K} \notin \mathbb{A}_{\mathbb{R}}.$$

*Proof*:  
Assume for contradiction that $J \tau^{-K} \in \mathbb{A}_{\mathbb{R}}$.  
Since $\mathbb{A}_{\mathbb{R}}$ is an algebraically closed subfield of $\mathbb{R}$ under field operations, and $J \in \mathbb{A}_{\mathbb{R}} \setminus \{0\}$, the quotient is algebraic:
$$\frac{J \tau^{-K}}{J} = \tau^{-K} \in \mathbb{A}_{\mathbb{R}}.$$
Since $K \in \mathbb{Q} \setminus \{0\}$, we can write $K = a/b$ with $a \in \mathbb{Z} \setminus \{0\}$ and $b \in \mathbb{Z}_{\ge 1}$.  
Raising to the integer power $-b \in \mathbb{Z} \setminus \{0\}$:
$$(\tau^{-a/b})^{-b} = \tau^a = (2\pi)^a \in \mathbb{A}_{\mathbb{R}}.$$
If $a > 0$, $(2\pi)^a \in \mathbb{A}_{\mathbb{R}} \implies 2\pi$ is a root of $X^a - c = 0$ for some algebraic $c$, so $2\pi \in \mathbb{A}_{\mathbb{R}}$, implying $\pi \in \mathbb{A}_{\mathbb{R}}$.  
If $a < 0$, $(2\pi)^a = 1/(2\pi)^{|a|} \in \mathbb{A}_{\mathbb{R}} \implies (2\pi)^{|a|} \in \mathbb{A}_{\mathbb{R}} \implies \pi \in \mathbb{A}_{\mathbb{R}}$.  
By Lindemann's Theorem (1882), $\pi$ is transcendental, so $\pi \notin \mathbb{A}_{\mathbb{R}}$.  
This contradiction proves that $J \tau^{-K} \notin \mathbb{A}_{\mathbb{R}}$. $\blacksquare$

---

### K. Is closure under analytic action actually required?

**No.** This directly resolves the **Governing Decision Point (Fork A vs Fork B)** in favor of **Fork B**:

- **Hypothesis A (Closure Required)**: Would claim that TC requires the operator action to close within the canonical algebraic-grade monoid $\mathcal{M}_\tau = \mathbb{A}_{\mathbb{R}} \times \mathbb{Z}_{\ne 0}$, so that $J \tau^{-K} \notin \mathbb{A}_{\mathbb{R}}$ represents an obstruction to off-critical zeros.
- **Hypothesis B (Ambient Escape)**: Recognizes that $\mathbb{A}_{\mathbb{R}}$ is merely an algebraic skeleton chosen to index grades. The operators $A_K$ and $D_J$ act on meromorphic functions $\mathcal{M}(\mathbb{C})$ for any real parameters $J, K \in \mathbb{R}$.

**Why Fork B is mathematically forced**:
1. The escape $J \tau^{-K} \notin \mathbb{A}_{\mathbb{R}}$ is an **unconditional algebraic fact** that depends only on the transcendence of $\pi$. It holds identically whether RH is true or false ($\delta$-independent).
2. The Riemann zeta function $\zeta(s)$, its zeros, and its functional equation have no axiomatic constraint demanding that dilations must leave an algebraic subfield $\mathbb{A}_{\mathbb{R}}$ invariant.
3. If one were to declare $J \tau^{-K} \notin \mathbb{A}_{\mathbb{R}}$ to be an obstruction, one would be committing the **fallacy of imposed domain restriction**: inventing an artificial boundary on grades and then claiming a contradiction because an external group action crosses that boundary.
4. In contrast, the authentic spectral detector $B_\rho(K) = 4\sinh^2(K \delta \log \tau / 2)$ vanishes if and only if $\delta = 0$. The reflection defect genuinely measures off-line displacement; algebraic-grade escape does not.

Therefore, **Fork B is conclusively established**: analytic dilation naturally escapes into an ambient completion with no contradiction and no required closure. Algebraic-grade escape is NOT the RH mechanism, and the repository must never treat it as one.

---

### L. What is the minimal ambient closure?

The set $\{a \tau^K : a, K \in \mathbb{A}_{\mathbb{R}}\}$ is not closed under addition. The actual additive and multiplicative closure generated by the TC actions is the ambient ring:
$$\Gamma_\tau \coloneqq \operatorname{span}_{\mathbb{A}_{\mathbb{R}}} \{ \tau^K : K \in \mathbb{A}_{\mathbb{R}} \} = \left\{ \sum_{j=1}^r a_j \tau^{K_j} : r \ge 1, \; a_j \in \mathbb{A}_{\mathbb{R}}, \; K_j \in \mathbb{A}_{\mathbb{R}} \right\}.$$

**Properties of $\Gamma_\tau$**:
1. $\mathbb{A}_{\mathbb{R}} \subseteq \Gamma_\tau$ (for $K = 0$, $a \tau^0 = a$).
2. $\Gamma_\tau$ is closed under addition by construction.
3. $\Gamma_\tau$ is closed under multiplication: $(\sum a_j \tau^{K_j})(\sum b_l \tau^{J_l}) = \sum_{j, l} (a_j b_l) \tau^{K_j + J_l} \in \Gamma_\tau$ since $a_j b_l \in \mathbb{A}_{\mathbb{R}}$ and $K_j + J_l \in \mathbb{A}_{\mathbb{R}}$.
4. $\Gamma_\tau$ is closed under analytic dilation $g \mapsto g \tau^{-K}$ for all $K \in \mathbb{A}_{\mathbb{R}}$.
5. $\Gamma_\tau$ is countable (finite combinations of countable elements over countable field $\mathbb{A}_{\mathbb{R}}$).

For the positive base coordinate, the logarithmic lattice generated by prime powers under $\tau^{\mathbb{A}_{\mathbb{R}}}$ scaling is:
$$\Lambda_\tau \coloneqq \operatorname{span}_{\mathbb{Z}} \{ \tau^K \log p : K \in \mathbb{A}_{\mathbb{R}}, \; p \in \mathcal{P} \}.$$
The corresponding multiplicative ambient group is:
$$\exp(\Lambda_\tau) = \left\{ \prod_{j=1}^r (p_j^{\tau^{K_j}})^{c_j} : c_j \in \mathbb{Z}, \; K_j \in \mathbb{A}_{\mathbb{R}}, \; p_j \in \mathcal{P} \right\} \subset \mathbb{R}_{>0}.$$

The ambient monoid generated by TC actions is therefore:
$$\mathcal{M}_\tau^{\mathrm{ambient}} \coloneqq \Gamma_\tau \times \exp(\Lambda_\tau) \subset \mathbb{R} \times \mathbb{R}_{>0}.$$

---

### M. Does the quotient referent survive analytic dilation?

**No, not at the discrete level.**  
The native referent of $(J, n)$ under $\pi$ is $n \in \mathbb{Z}_{\ne 0}$. Under analytic dilation, $n \mapsto n^{\tau^{-K}} \notin \mathbb{Z}$.

In log-space $x = \log n$, the referent transforms by dilation:
$$x \mapsto \tau^{-K} x.$$
Thus, while the discrete integer identity is lost, the referent transforms **equivariantly under the continuous dilation flow** on $\mathbb{R}_{>0}$.

---

### N. Does any genuine closure/invariance law produce $B_\rho$?

**YES.** The spectral detector $B_\rho(K)$ emerges directly from the **bilateral reflection defect of the normalized grade-unit character**.

For any grade unit $u_K = (K, 1)$, its character evaluation is:
$$\chi_s(u_K) = \tau^{-Ks}.$$
On the critical line $\Re(s) = 1/2$, the modulus is $|\chi_{1/2 + i\gamma}(u_K)| = \tau^{-K/2}$.  
Normalizing by the critical-line modulus yields:
$$\widehat{\chi}_s(u_K) = \frac{\chi_s(u_K)}{\tau^{-K/2}} = \tau^{-K(s - 1/2)}.$$

Now evaluate $\widehat{\chi}_s(u_K)$ at an off-critical zero $\rho = 1/2 + \delta + i\gamma$ and its functional equation reflection $1 - \rho = 1/2 - \delta - i\gamma$:
$$|\widehat{\chi}_\rho(u_K)| = |\tau^{-K(\delta + i\gamma)}| = \tau^{-K \delta},$$
$$|\widehat{\chi}_{1-\rho}(u_K)| = |\tau^{-K(-\delta - i\gamma)}| = \tau^{K \delta}.$$

The bilateral symmetrization minus the baseline critical-line value ($\delta = 0 \implies 1 + 1 = 2$) is:
$$\boxed{ |\widehat{\chi}_\rho(u_K)| + |\widehat{\chi}_{1-\rho}(u_K)| - 2 = \tau^{K \delta} + \tau^{-K \delta} - 2 = 4 \sinh^2\left(\frac{K \delta \log \tau}{2}\right) = B_\rho(K)! }$$

This is an **exact algebraic theorem**:  
$B_\rho(K)$ is identically the reflection defect of the grade-unit character under the functional equation involution $s \leftrightarrow 1 - s$.  
It is strictly positive for any off-line zero ($\delta \ne 0$) and vanishes if and only if $\delta = 0$.

---

### O. What is now the earliest missing implication toward RH?

The earliest missing implication is **Layer 3 of the TC Programme**:
Construct an admissible test function $\psi_K$ or integral kernel that couples the arithmetic discrepancy functional:
$$\Delta_K[\psi] = \int_0^\infty \psi_K(x) \, d\left(\mu_K^{\mathrm{analytic}} - \mu_K^{\mathrm{grid}}\right)(x)$$
to the spectral reflection defect sum:
$$\Delta_K[\psi] = \sum_{\rho \in Z^+} w_\rho B_\rho(K), \qquad w_\rho > 0,$$
and derive from an authentic, zero-independent principle that $\Delta_K[\psi]$ must vanish or satisfy a bound that forbids off-line zeros.

---

## Generic-Base Control: Algebraic vs Transcendental Bases

To verify which features are specific to $\tau = 2\pi$, we perform the generic-base control with base $b > 1$:
1. **Graded Monoid Structure**: $\mathcal{M}_b = \mathbb{A}_{\mathbb{R}} \times \mathbb{Z}_{\ne 0}$ is identical for any base $b$.
2. **Grade Units and Factorization**: $u_K = (K, 1)$, $\mathcal{M}_b / U_{\mathrm{grade}} \cong \mathbb{Z}_{\ne 0}$, and factorization into native primes hold for any base $b$.
3. **Bilateral Reflection Defect**: The identity:
   $$b^{K \delta} + b^{-K \delta} - 2 = 4 \sinh^2\left(\frac{K \delta \log b}{2}\right) = B_\rho(K; b)$$
   holds for ANY base $b > 1$.
4. **Algebraic-Grade Escape Status**:
   - For an **algebraic base** (e.g. $b = 2$): For rational grades $K \in \mathbb{Q}$, $b^{-K} = 2^{-K}$ is algebraic! Therefore:
     $$J \in \mathbb{A}_{\mathbb{R}}, K \in \mathbb{Q} \implies J b^{-K} \in \mathbb{A}_{\mathbb{R}}.$$
     **Algebraic-grade closure HOLDS for algebraic bases!**
   - For a **transcendental base** (e.g. $b = \tau = 2\pi$): $b^{-K}$ is transcendental for $K \in \mathbb{Q} \setminus \{0\}$, so $J \tau^{-K} \notin \mathbb{A}_{\mathbb{R}}$.
     **Algebraic-grade closure FAILS for transcendental bases.**

This proves that:
- The reflection defect $B_\rho(K)$ is a universal property of exponential characters under reflection.
- Algebraic-grade escape is specific to transcendental bases like $\tau = 2\pi$.

---

## Terminology Correction from TASK-TC-017: Affine Group Structure

In TASK-TC-017, the operator relation $A_K D_J = D_{J \tau^{-K}} A_K$ was described as generating $\mathbb{R} \rtimes \tau^{\mathbb{A}_{\mathbb{R}}} \cong \operatorname{Aff}_+(\mathbb{R})$.

**Audit and Correction**:
- The full positive affine group $\operatorname{Aff}_+(\mathbb{R}) = \mathbb{R} \rtimes \mathbb{R}_{>0}$ is an uncountable 2-dimensional Lie group of cardinality $2^{\aleph_0}$.
- The subgroup generated by the allowed TC operations on algebraic grades is:
  $$G_{\mathrm{TC}} = \mathcal{T}_{\mathrm{closure}} \rtimes \tau^{\mathbb{A}_{\mathbb{R}}},$$
  where $\mathcal{T}_{\mathrm{closure}} = \operatorname{span}_{\mathbb{Z}} \{ K \tau^{-J} \log \tau : K, J \in \mathbb{A}_{\mathbb{R}} \}$.
- Since $\mathbb{A}_{\mathbb{R}}$ is countable, $G_{\mathrm{TC}}$ is a **countable, dense, proper subgroup** of $\operatorname{Aff}_+(\mathbb{R})$, NOT the entire Lie group $\operatorname{Aff}_+(\mathbb{R})$.
- All documentation is updated to specify $G_{\mathrm{TC}} \subsetneq \operatorname{Aff}_+(\mathbb{R})$ as a dense proper subgroup.

---

## Test and Verification Status

- Unit test suite: `tests/test_tc_graded_arithmetic_closure.py` — **13 passed in 0.58s**.
- Formal verification: `formal/RiemannScope/GradedMonoid.lean` — `lake build` compiled with **exit code 0**.
- Claim spec audit: `audit_claim_spec.py --cross-check-register --repo-root .` — **110/110 passed**.
