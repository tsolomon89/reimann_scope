# Review: Zero-Induced Grade-Unit Characters, Unitarity, and the Positive-Definite TC Constraint

**Task**: TASK-TC-019  
**Date**: October 2026  
**Status**: ACCEPTED / RESEARCH SYNTHESIS  
**Evidence Class**: `PROVED_CONDITIONAL` / `EQUIVALENT_REFORMULATION_OF_WEIL`  
**Related Claims**: CLM-CT-028, CLM-CT-029, TC-DISC-034, TC-DISC-035, TC-DISC-036  

---

## Executive Summary

TASK-TC-019 tests the central constraint hypothesis emerging from the graded arithmetic monoid $\mathcal{M}_\tau = \mathbb{A}_{\mathbb{R}} \times \mathbb{Z}_{\ne 0}$ established in TASK-TC-018:
$$\boxed{\text{Riemann Hypothesis} \iff \text{All zero-induced integer-grade characters } \eta_\rho \text{ are unitary}.}$$

We analyze whether zeta arithmetic independently forces this unitarity via a positive-definite bilateral grade correlation sequence $C(K)$ on the integer skeleton $K \in \mathbb{Z}$.

### Key Mathematical Findings
1. **Zero-Induced Grade Character**: For any nontrivial zero $\rho = 1/2 + \delta + i\gamma$, $\eta_\rho(K) \coloneqq \tau^{-K(\rho - 1/2)}$ is a group homomorphism from $(\mathbb{Z}, +)$ to $(\mathbb{C}^\times, \times)$ with modulus $|\eta_\rho(K)| = \tau^{-K\delta}$.
2. **RH as Unitarity**: $|\eta_\rho(K)| = 1$ for all $K \in \mathbb{Z} \iff \delta = 0$. Thus, RH is mathematically equivalent to the statement that the zero-induced grade characters on the integer skeleton $\mathbb{Z}$ are unitary.
3. **Representation Meaning of $B_\rho(K)$**: The spectral detector $B_\rho(K) = 4\sinh^2(K\delta\log\tau/2)$ is identically equal to $|\eta_\rho(K)| + |\eta_\rho(K)|^{-1} - 2$. It is **not** an ad hoc penalty, but the exact **non-unitarity defect** of the zero-induced grade character.
4. **Mellin Dilation Unitarity & Origin of $1/2$ Centering**: Multiplicative dilation $x \mapsto \tau^K x$ is strictly unitary on $L^2(\mathbb{R}_{>0}, dx/x)$. When normalized on $L^2(\mathbb{R}_{>0}, dx)$ as $(U_K f)(x) = \tau^{K/2} f(\tau^K x)$, its Mellin multiplier is $\tau^{-K(s - 1/2)} = \eta_s(K)$. The $1/2$ centering emerges naturally from the Plancherel isometry line $\operatorname{Re}(s) = 1/2$ of the Mellin transform on $L^2(\mathbb{R}_{>0}, dx)$.
5. **Dual = Adjoint**: Inversion $\eta_\rho(K)^{-1}$ equals complex conjugation $\overline{\eta_\rho(K)}$ on $\mathbb{Z}$ if and only if $\delta = 0$.
6. **Herglotz Analysis & Weil Equivalence**: By Herglotz's Theorem (1911), positive-definite sequences on $\mathbb{Z}$ admit only unitary characters in their spectral support. However, connecting an unconditionally positive-definite arithmetic correlation $\langle U_K v, v \rangle$ to a pure sum over zeta zero characters requires the explicit formula. Demanding that the zero quadratic form be positive semi-definite without archimedean contamination is strictly an `EQUIVALENT_REFORMULATION_OF_WEIL`. Unitarity cannot be deduced from arithmetic without establishing the Weil positivity criterion.
7. **Corrections to TASK-TC-018 Overclaims**:
   - The assertion that $n^{\tau^{-K}}$ is transcendental by Gelfond–Schneider is **withdrawn**. Gelfond–Schneider requires an algebraic base $\alpha \ne 0, 1$ and an irrational *algebraic* exponent $\beta$. Here $\tau^{-K}$ is transcendental, so the theorem does not apply.
   - The counter-control $\alpha = \log_2 3$ proves that $\alpha$ is transcendental, yet $2^\alpha = 3 \in \mathbb{Z}$, establishing that exponent transcendence does not imply power transcendence. General transcendence of $n^{\tau^{-K}}$ is classified as **OPEN**, while nonintegrality for witness cases ($1 < 2^{\tau^{-K}} < 2$ for $K > 0$) is proved by elementary interval bounds.
   - The unclosed ambient candidate $\mathbb{A}_{\mathbb{R}} \cdot \tau^{\mathbb{A}_{\mathbb{R}}}$ is replaced by the actual ambient ring $\Gamma_\tau = \operatorname{span}_{\mathbb{A}_{\mathbb{R}}}\{\tau^K : K \in \mathbb{A}_{\mathbb{R}}\}$.

---

## Detailed Review Answers (A through O)

### A. What is the zero-induced grade-unit character?

Let $\tau = 2\pi > 1$. For any complex parameter $s = 1/2 + \delta + it \in \mathbb{C}$ (and specifically for a nontrivial zero $\rho = 1/2 + \delta + i\gamma$), the **normalized zero-induced grade-unit character** is defined on the integer grade skeleton $K \in \mathbb{Z}$ by:
$$\boxed{\eta_\rho(K) \coloneqq \tau^{-K\left(\rho - \frac{1}{2}\right)} = \tau^{-K(\delta + i\gamma)} = \tau^{-K\delta} e^{-i K \gamma \log\tau}.}$$

Its modulus is:
$$\boxed{|\eta_\rho(K)| = \tau^{-K\delta}.}$$

---

### B. Why is it a genuine character?

The character $\eta_\rho$ is a group homomorphism from the additive group $(\mathbb{Z}, +)$ to the multiplicative group $(\mathbb{C}^\times, \times)$:
1. **Multiplication Law**:
   $$\eta_\rho(K + J) = \tau^{-(K+J)(\rho - 1/2)} = \tau^{-K(\rho - 1/2)} \tau^{-J(\rho - 1/2)} = \eta_\rho(K) \eta_\rho(J).$$
2. **Identity**:
   $$\eta_\rho(0) = \tau^0 = 1.$$
3. **Inversion**:
   $$\eta_\rho(-K) = \tau^{-(-K)(\rho - 1/2)} = \tau^{K(\rho - 1/2)} = \frac{1}{\eta_\rho(K)} = \eta_\rho(K)^{-1}.$$

Therefore, $\eta_\rho \in \operatorname{Hom}((\mathbb{Z}, +), (\mathbb{C}^\times, \times))$ is a genuine multiplicative character of the integer grade group.

---

### C. Prove RH is equivalent to unitarity of every zero character.

**Definition**: A character $\eta \colon \mathbb{Z} \to \mathbb{C}^\times$ is **unitary** if $|\eta(K)| = 1$ for all $K \in \mathbb{Z}$.

**Theorem (TC Unitarity Reformulation of RH)**:
$$\boxed{\eta_\rho \text{ is unitary on } \mathbb{Z} \iff \delta = 0.}$$
Consequently:
$$\boxed{\text{Riemann Hypothesis} \iff \forall \rho \in \mathcal{Z}(\zeta), \; \eta_\rho \text{ is unitary on } \mathbb{Z}.}$$

*Proof*:
- $(\implies)$: Assume $\eta_\rho$ is unitary on $\mathbb{Z}$. Then $|\eta_\rho(1)| = 1$.  
  By definition, $|\eta_\rho(1)| = \tau^{-\delta}$. Since $\tau = 2\pi > 1$, $\tau^{-\delta} = 1 \iff -\delta \log\tau = 0 \iff \delta = 0$.
- $(\impliedby)$: Assume $\delta = 0$ (the zero lies on the critical line $\operatorname{Re}(\rho) = 1/2$).  
  Then for all $K \in \mathbb{Z}$:
  $$|\eta_\rho(K)| = \tau^{-K \cdot 0} = \tau^0 = 1.$$
  Hence $\eta_\rho$ is unitary on $\mathbb{Z}$.
- Extending to all zeros: RH asserts that $\delta_\rho = 0$ for all nontrivial zeros $\rho$. Therefore, RH holds if and only if every zero-induced grade character $\eta_\rho$ is unitary. $\blacksquare$

---

### D. Prove $B_\rho(K)$ is its nonunitarity defect.

Recall the spectral detector $B_\rho(K)$ from TASK-TC-016 through TASK-TC-018:
$$B_\rho(K) = \tau^{K\delta} + \tau^{-K\delta} - 2 = 4\sinh^2\left(\frac{K\delta\log\tau}{2}\right).$$

In terms of the character modulus $|\eta_\rho(K)| = \tau^{-K\delta}$:
$$|\eta_\rho(K)|^{-1} = \tau^{K\delta}.$$

Summing the character modulus and its inverse:
$$\boxed{B_\rho(K) = |\eta_\rho(K)| + |\eta_\rho(K)|^{-1} - 2 = \left( |\eta_\rho(K)|^{1/2} - |\eta_\rho(K)|^{-1/2} \right)^2.}$$

**Properties**:
1. $B_\rho(K) \ge 0$ for all $K \in \mathbb{Z}$ and $\delta \in \mathbb{R}$ (being a squared difference).
2. For $K \ne 0$: $B_\rho(K) = 0 \iff |\eta_\rho(K)| = 1 \iff \eta_\rho$ is unitary $\iff \delta = 0$.
3. Therefore, $B_\rho(K)$ is **precisely the non-unitarity defect** of the zero-induced grade character.

---

### E. Does TC arithmetic naturally produce a positive-definite grade correlation?

**Yes, on the abstract Hilbert-space side.**  
Any unitary representation $U_K$ of the integer grade group $\mathbb{Z}$ on a Hilbert space $\mathcal{H}$ produces an unconditionally positive-definite sequence:
$$C(K) \coloneqq \langle U_K v, v \rangle_{\mathcal{H}}.$$
For any finite choices $c_1, \dots, c_N \in \mathbb{C}$ and $K_1, \dots, K_N \in \mathbb{Z}$:
$$\sum_{i, j=1}^N c_i \overline{c_j} C(K_i - K_j) = \sum_{i, j=1}^N c_i \overline{c_j} \langle U_{K_i - K_j} v, v \rangle = \left\langle \sum_{i=1}^N c_i U_{K_i} v, \; \sum_{j=1}^N c_j U_{K_j} v \right\rangle = \left\| \sum_{i=1}^N c_i U_{K_i} v \right\|_{\mathcal{H}}^2 \ge 0.$$

---

### F. Is that positivity unconditional?

- **On the geometric/operator side**: **Yes.** The positivity $\left\| \sum c_i U_{K_i} v \right\|^2 \ge 0$ is unconditional for any valid inner product space.
- **On the arithmetic/spectral side**: **No.** Positivity becomes conditional the moment one equates $C(K)$ with a sum over zeta zeros via the explicit formula.
  In the explicit formula, the arithmetic sum (prime powers) equals the zero sum **minus** archimedean and pole distributions:
  $$\sum_\rho \widehat{h}(\rho) = \text{Poles} - \text{Primes} - \text{Archimedean}.$$
  Deducing that the zero part alone is positive-definite without prior knowledge of zero locations requires the full power of Weil's positivity criterion.

---

### G. What Hilbert space/norm makes the grade action natural?

Two natural Hilbert spaces arise:
1. **Haar Multiplicative Space**: $L^2(\mathbb{R}_{>0}, dx/x)$. Here the unnormalized dilation $(T_K f)(x) = f(\tau^K x)$ is an exact isometry:
   $$\int_0^\infty |f(\tau^K x)|^2 \frac{dx}{x} = \int_0^\infty |f(u)|^2 \frac{du}{u} = \|f\|^2.$$
2. **Lebesgue Geometric Space**: $L^2(\mathbb{R}_{>0}, dx)$. Here the normalized dilation:
   $$(U_K f)(x) \coloneqq \tau^{K/2} f(\tau^K x)$$
   is an exact isometry:
   $$\int_0^\infty |(U_K f)(x)|^2 dx = \tau^K \int_0^\infty |f(\tau^K x)|^2 dx = \int_0^\infty |f(u)|^2 du = \|f\|^2.$$

---

### H. Is multiplicative scaling unitary under $dx/x$?

**Yes.** Multiplicative dilation $x \mapsto \tau^K x$ preserves the Haar measure $d^\times x = dx/x$ on the multiplicative group $\mathbb{R}_{>0}$:
$$\frac{d(\tau^K x)}{\tau^K x} = \frac{\tau^K dx}{\tau^K x} = \frac{dx}{x}.$$
Therefore, $T_K \colon f(x) \mapsto f(\tau^K x)$ is a unitary operator on $L^2(\mathbb{R}_{>0}, dx/x)$ for every $K \in \mathbb{R}$.

---

### I. Where does the $1/2$ centering arise?

The critical line is $\operatorname{Re}(s) = 1/2$, not $\operatorname{Re}(s) = 0$. Why does the character involve $\rho - 1/2$?

The $1/2$ centering is derived from the **Mellin-Plancherel Isometry**:
1. For $f \in L^2(\mathbb{R}_{>0}, dx)$ (with standard Lebesgue measure), the Mellin transform $\mathcal{M}[f](s) = \int_0^\infty f(x) x^{s-1} dx$ satisfies Plancherel's theorem along the critical line $\operatorname{Re}(s) = 1/2$:
   $$\int_0^\infty |f(x)|^2 dx = \frac{1}{2\pi} \int_{-\infty}^\infty \left| \mathcal{M}[f]\left(\frac{1}{2} + it\right) \right|^2 dt.$$
2. The normalized unitary dilation on $L^2(\mathbb{R}_{>0}, dx)$ is $(U_K f)(x) = \tau^{K/2} f(\tau^K x)$.
3. Computing its Mellin transform:
   $$\mathcal{M}[U_K f](s) = \int_0^\infty \tau^{K/2} f(\tau^K x) x^{s-1} dx = \tau^{K/2} \tau^{-Ks} \int_0^\infty f(u) u^{s-1} du = \tau^{-K(s - 1/2)} \mathcal{M}[f](s).$$
4. The multiplier is **identically** the normalized grade character:
   $$\boxed{\mathcal{M}[U_K f](s) = \eta_s(K) \mathcal{M}[f](s), \qquad \eta_s(K) = \tau^{-K(s - 1/2)}.}$$

The $1/2$ centering is therefore **not** inserted manually; it is the unique coordinate shift aligning the multiplicative group action with the Lebesgue-measure Mellin-Plancherel isometry line!

---

### J. How does functional-equation reflection act on the character?

Under functional equation reflection $s \leftrightarrow 1 - s$:
$$\rho \mapsto 1 - \rho = \frac{1}{2} - \delta - i\gamma.$$
Evaluating the grade character at $1 - \rho$:
$$\eta_{1-\rho}(K) = \tau^{-K(1 - \rho - 1/2)} = \tau^{-K(1/2 - \rho)} = \tau^{K(\rho - 1/2)} = \eta_\rho(-K) = \eta_\rho(K)^{-1}.$$
$$\boxed{\text{Functional-equation reflection } s \mapsto 1 - s \iff \text{Grade inversion } K \mapsto -K.}$$

Under Schwarz reflection across the critical line $s \leftrightarrow 1 - \bar{s}$:
$$\rho \mapsto 1 - \bar{\rho} = \frac{1}{2} - \delta + i\gamma.$$
Evaluating the grade character:
$$\eta_{1-\bar{\rho}}(K) = \tau^{-K(-\delta + i\gamma)} = \overline{\eta_\rho(-K)} = \overline{\eta_\rho(K)^{-1}}.$$

---

### K. Does “dual = adjoint” follow independently?

In Pontryagin duality for the group $(\mathbb{Z}, +)$, the dual character is $\eta^*(K) = \overline{\eta(K)}$.  
In group representation theory, an operator character satisfies $\eta(K)^{-1} = \eta^*(K)$ if and only if $\eta$ is unitary.

Comparing inversion and complex conjugation for $\eta_\rho$:
$$\eta_\rho(K)^{-1} = \tau^{K\delta} \tau^{iK\gamma}, \qquad \overline{\eta_\rho(K)} = \tau^{-K\delta} \tau^{iK\gamma}.$$
Equating them:
$$\eta_\rho(K)^{-1} = \overline{\eta_\rho(K)} \iff \tau^{K\delta} = \tau^{-K\delta} \iff \tau^{2K\delta} = 1 \iff \delta = 0.$$
$$\boxed{\text{Dual = Adjoint } (\eta_\rho^{-1} = \overline{\eta_\rho}) \iff \text{Unitarity } (|\eta_\rho| = 1) \iff \delta = 0.}$$

Therefore, "dual = adjoint" does **not** follow independently from the abstract monoid; it is mathematically equivalent to RH.

---

### L. Can Herglotz/Pontryagin theory force unitary zero characters?

**Herglotz's Theorem (1911)** states that a sequence $C \colon \mathbb{Z} \to \mathbb{C}$ is positive definite if and only if there exists a finite positive Borel measure $\mu$ on the unit circle $\mathbb{T} = \{z \in \mathbb{C} : |z| = 1\}$ such that:
$$C(K) = \int_{\mathbb{T}} z^K d\mu(z).$$

Every character occurring in the spectral decomposition of a positive-definite sequence on $\mathbb{Z}$ has form $z^K$ with $|z| = 1$ — it is **strictly unitary**.

If $\eta_\rho(K) = q_\rho^K$ with $q_\rho = \tau^{-(\rho - 1/2)} = \tau^{-(\delta + i\gamma)}$, then:
$$|q_\rho| = \tau^{-\delta}.$$
- If $\delta = 0$, $q_\rho \in \mathbb{T}$, so $\eta_\rho$ can be a spectral atom of a Herglotz measure.
- If $\delta \ne 0$, $|q_\rho| \ne 1$, so $q_\rho \notin \mathbb{T}$. The sequence $K \mapsto q_\rho^K$ is **exponentially unbounded** in one direction and **cannot** be represented by a positive measure on $\mathbb{T}$.

---

### M. Do the zeta zeros actually occur as spectral characters of the arithmetic correlation?

**Only via the Explicit Formula, which includes archimedean and pole terms.**  
If we construct an arithmetic correlation from prime powers:
$$C_{\mathrm{arith}}(K) = \sum_{n=1}^\infty \frac{\Lambda(n)}{\sqrt{n}} \psi(K, \log n),$$
the Riemann-Weil explicit formula expresses $C_{\mathrm{arith}}(K)$ as:
$$C_{\mathrm{arith}}(K) = \text{Pole Terms} - \sum_\rho \widehat{\psi}(K, \rho) - \text{Archimedean Integral}.$$
The zeros appear as the **negative-spectral component** balancing the prime and archimedean components. They do **not** appear as the isolated, independent spectral decomposition of an arithmetic state $\langle U_K v, v \rangle$.

---

### N. Is this equivalent to Weil positivity/RH?

**Yes.** Classification:
$$\boxed{\texttt{EQUIVALENT\_REFORMULATION\_OF\_WEIL}}$$

**Proof of Equivalence**:
1. By Weil's Criterion (1952), RH is equivalent to the positive definiteness of the quadratic functional $W(f * \tilde{f}) \ge 0$ on test functions on $\mathbb{R}_{>0}$.
2. In TC language, a positive-definite grade correlation whose spectral measure isolates the zero characters $\eta_\rho$ exists if and only if the zero contribution $\sum_\rho |\mathcal{M}[f](\rho)|^2$ is dominated by the arithmetic/archimedean form.
3. Asserting that the zero characters $\eta_\rho$ must be unitary because the grade action is unitary on arithmetic data assumes that the arithmetic inner product pushes forward to a positive measure on the zero spectrum. This pushforward is positive if and only if Weil's positivity holds.
4. Hence, the positive-definite TC constraint does not bypass Weil; it is an exact, elegant reformulation of Weil positivity in the category of graded monoid unit characters.

---

### O. What is now the earliest missing implication toward RH?

The earliest missing implication is:
$$\boxed{\begin{gathered}
\text{Prove that the arithmetic same-referent equivalence forces the}\\
\text{explicit formula discrepancy functional } \Delta_K[\psi] \coloneqq \int \psi_K d(\mu_K^{\mathrm{analytic}} - \mu_K^{\mathrm{grid}})\\
\text{to dominate the omitted archimedean tail without assuming Weil positivity.}
\end{gathered}}$$

Until this arithmetic domination is proved from first principles without circularity, the unitarity reformulation remains a sharp diagnostic characterization of RH, not a finished proof.

---

## Deliverables & Registry Cross-Reference
- Formal Lean 4 module: [formal/RiemannScope/GradeCharacter.lean](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/GradeCharacter.lean)
- Test suite: [tests/test_tc_grade_character_unitarity.py](file:///c:/Development/Projects/reimann_scope/tests/test_tc_grade_character_unitarity.py)
- Data specification: [data/tc_grade_character_unitarity.json](file:///c:/Development/Projects/reimann_scope/data/tc_grade_character_unitarity.json)
