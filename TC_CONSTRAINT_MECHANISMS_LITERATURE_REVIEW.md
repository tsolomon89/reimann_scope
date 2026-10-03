# AI-Driven Literature Review: Established Constraint Mechanisms Relevant to Transcendental Continuation (TC)

**Document Type:** Formal Mathematical Literature Review & Theoretical Synthesis (Revision 2 — Audited & Corrected)  
**Project:** Riemann Scope / Transcendental Continuation (TC)  
**Date:** October 2026  
**Status:** REVISED & AUDITED  
**License & Terms Notice:** This review incorporates literature retrieved via the arXiv API in accordance with arXiv's Terms of Use (https://info.arxiv.org/help/api/index.html). Individual paper citations and URLs are recorded in the references.

---

## Table of Contents

1. [Executive Summary & The Core Structural Problem](#1-executive-summary--the-core-structural-problem)
2. [Part I: Executive Conclusion — Primary Established Mechanisms](#part-i-executive-conclusion--primary-established-mechanisms)
3. [Part II: Constraint Mechanism Taxonomy](#part-ii-constraint-mechanism-taxonomy)
4. [Part III: Detailed Theorem Cards (19 Candidate Mechanisms)](#part-iii-detailed-theorem-cards)
   - [Card 1: Herglotz Representation Theorem (1911)](#card-1-herglotz-representation-theorem-1911)
   - [Card 2: Bochner's Theorem on Locally Compact Abelian Groups (1932/1940)](#card-2-bochners-theorem-on-locally-compact-abelian-groups-19321940)
   - [Card 3: Pontryagin Duality and the Unitary Dual of $\mathbb{Z}$ (1934)](#card-3-pontryagin-duality-and-the-unitary-dual-of-mathbbz-1934)
   - [Card 4: Mellin–Plancherel Theorem on the Critical Axis (1897/1910/1948)](#card-4-mellinplancherel-theorem-on-the-critical-axis-189719101948)
   - [Card 5: Unitary Principal Series of $\mathrm{SL}(2, \mathbb{R})$ (1946/1947/1954)](#card-5-unitary-principal-series-of-mathrmsl2-mathbbr-194619471954)
   - [Card 6: Normalized Intertwining Operators and Centered Unitary Axis (Langlands–Shahidi)](#card-6-normalized-intertwining-operators-and-centered-unitary-axis-langlandsshahidi)
   - [Card 7: Automorphic Scattering Matrix Unitarity on the Critical Axis (Selberg/Lax–Phillips)](#card-7-automorphic-scattering-matrix-unitarity-on-the-critical-axis-selberglaxphillips)
   - [Card 8: Stone–von Neumann Theorem and Canonical Commutation Relations (1930/1931)](#card-8-stonevon-neumann-theorem-and-canonical-commutation-relations-19301931)
   - [Card 9: Iterated Operator Representations and Dynamical Sampling (Christensen–Hasannasab / Aldroubi et al.)](#card-9-iterated-operator-representations-and-dynamical-sampling-christensenhasannasab--aldroubi-et-al)
   - [Card 10: Frame Range Projection and Redundancy Consistency Equations (Duffin–Schaeffer)](#card-10-frame-range-projection-and-redundancy-consistency-equations-duffinschaeffer)
   - [Card 11: Hermite–Biehler Theorem and de Branges Positivity (1856/1879/1968)](#card-11-hermitebiehler-theorem-and-de-branges-positivity-185618791968)
   - [Card 12: Weil's Explicit-Formula Positivity Criterion (1952)](#card-12-weils-explicit-formula-positivity-criterion-1952)
   - [Card 13: Li's Criterion on Conformal Disk Images (1997)](#card-13-lis-criterion-on-conformal-disk-images-1997)
   - [Card 14: Nyman–Beurling / Báez-Duarte Closure Criterion (1950/1955/2003)](#card-14-nymanbeurling--b%C3%A1ez-duarte-closure-criterion-195019552003)
   - [Card 15: Selberg Trace Formula Geodesic–Spectral Positivity (1956)](#card-15-selberg-trace-formula-geodesicspectral-positivity-1956)
   - [Card 16: Lindemann's Transcendence Theorem and Lattice Disjointness (1882)](#card-16-lindemanns-transcendence-theorem-and-lattice-disjointness-1882)
   - [Card 17: Linear Independence of Logarithms: Rational Independence vs. Baker's Theorem](#card-17-linear-independence-of-logarithms-rational-independence-vs-bakers-theorem)
   - [Card 18: Ax–Schanuel Functional Transcendence Theorem (1971)](#card-18-axschanuel-functional-transcendence-theorem-1971)
   - [Card 19: Voronin's Universality Theorem as an Analytic Flexibility Barrier (1975)](#card-19-voronins-universality-theorem-as-an-analytic-flexibility-barrier-1975)
5. [Part IV: Direct TC Correspondences](#part-iv-direct-tc-correspondences)
6. [Part V: Known Barriers, False Routes, and Structural Obstructions](#part-v-known-barriers-false-routes-and-structural-obstructions)
7. [Part VI: Recommended Mathematical Experiments](#part-vi-recommended-mathematical-experiments)
8. [Comprehensive Comparison Matrix (Section 17 Table)](#comprehensive-comparison-matrix-section-17-table)
9. [Detailed Resolution of Highest-Priority Question (Section 18)](#detailed-resolution-of-highest-priority-question-section-18)
10. [Detailed Resolution of Second Highest-Priority Question (Section 19)](#detailed-resolution-of-second-highest-priority-question-section-19)
11. [Detailed Resolution of Third Highest-Priority Question (Section 20)](#detailed-resolution-of-third-highest-priority-question-section-20)
12. [Part VII: Final Synthesis and Next Proof Target (Section 21)](#part-vii-final-synthesis-and-next-proof-target-section-21)
13. [References & Citations](#references--citations)

---

# 1. Executive Summary & The Core Structural Problem

### 1.1 The Motivating Pattern in Transcendental Continuation (TC)
The Transcendental Continuation (TC) programme considers a single mathematical object—the Riemann zeta function $\zeta(s)$—and examines an infinite family of exact representations indexed by a discrete grade scale $K \in \mathbb{Z}$:
$$\mathcal{Z}_\tau(s, K) = \zeta(\tau^{-K} s), \qquad \tau = 2\pi.$$
For any non-trivial zero $\rho = \frac{1}{2} + \delta + i\gamma$, the grade transformation induces a bilateral geometric sequence of evaluations in centered coordinates $z = s - 1/2 = \delta + i\gamma$:
$$\eta_\rho(K) = \tau^{-K(\rho - 1/2)} = \tau^{-K(\delta + i\gamma)}.$$
The modulus of this grade factor is:
$$|\eta_\rho(K)| = \tau^{-K\delta}.$$
Consequently, the character $K \mapsto \eta_\rho(K)$ is **unitary** on $\mathbb{Z}$ if and only if the off-line displacement vanishes:
$$\boxed{|\eta_\rho(K)| = 1 \quad \forall K \in \mathbb{Z} \iff \delta = 0.}$$

### Canonical Repository Grade Defect Definition
The canonical grade reflection defect in the repository is defined by:
$$\boxed{B_\rho(K) = |\eta_\rho(K)| + |\eta_\rho(K)|^{-1} - 2 = \tau^{K\delta} + \tau^{-K\delta} - 2 = 4\sinh^2\left(\frac{K\delta \log \tau}{2}\right) \ge 0.}$$
This non-negative functional vanishes if and only if $\delta = 0$:
$$B_\rho(K) = 0 \iff \delta = 0.$$
*(Note: A squared-modulus defect $|\eta(K)|^2 + |\eta(K)|^{-2} - 2 = 4\sinh^2(K\delta \log \tau)$ can also be considered as a diagnostic variant, but the single-power defect with argument $\frac{K\delta\log\tau}{2}$ remains the canonical definition across all repository contracts and verification suites).*

The conceptual thesis of TC is:
$$\boxed{\text{same information} \Longrightarrow \text{many exact representations across transcendental grades} \Longrightarrow \text{compatibility / invariance / positivity / rigidity} \Longrightarrow \text{constraint } (\delta = 0).}$$

The central open question of the programme is:
> **Why should the characters selected by the zeta spectrum be unitary?**  
> Or equivalently: **What established arithmetic or analytic constraint forces a positive grade defect to vanish?**

### 1.2 Purpose of This Review
This literature review conducts an exhaustive mathematical survey across established disciplines—harmonic analysis, representation theory, automorphic forms, frame theory, dynamical sampling, transcendence theory, and spectral geometry—to determine:
1. Does this exact constraint mechanism already exist under another mathematical language?
2. Under what established hypotheses does positivity, boundedness, self-adjointness, or redundancy force bilateral spectral characters to be unitary?
3. Where does the transcendental period $2\pi$ act as an active arithmetic constraint rather than an arbitrary normalization convention?
4. What are the fatal pitfalls, circularities, and mathematical barriers that any viable TC constraint mechanism must surmount?

---

# Part I: Executive Conclusion — Primary Established Mechanisms

The deep literature review identifies **six established theorem-level constraint mechanisms**, with the pairing of **Mellin–Plancherel** and **Frame Range Consistency** emerging as the most structurally aligned foundation for Transcendental Continuation:

### 1. Primary Architecture: Mellin–Plancherel + Frame Range Consistency
- **Mellin–Plancherel (Mellin 1897 / Titchmarsh 1948):** Normalized multiplicative dilation on $L^2(\mathbb{R}_{>0}, dx)$ has multiplier $\tau^{-K(s-1/2)}$. This proves that the critical line $\mathrm{Re}(s) = 1/2$ is the canonical unitary axis of multiplicative harmonic analysis, completely independent of the Riemann Hypothesis.
- **Frame Range Consistency (Duffin–Schaeffer 1952 / Daubechies 1986):** Frame theory provides the exact mathematical formulation of the TC premise: *"redundancy adds no new information, but imposes exact compatibility constraints."* For any overcomplete frame, the analysis operator $T$ maps into a proper closed subspace of $\ell^2$, and valid coefficient vectors must satisfy the range projection identity:
  $$\boxed{(I - P) c = 0, \qquad P = T(T^* T)^{-1} T^*.}$$
  This mechanism is fundamentally distinct from assuming positivity of the zero quadratic form. It offers an open, non-circular route to explore whether an off-line zero character $c_K = \tau^{-K(\delta+i\gamma)}$ fails the range condition of an authentic overcomplete frame.

### 2. Rational Linear Independence of Transcendental Periods (Proved vs. Open Baker)
- **Proved Theorem (Lindemann 1882 + Fundamental Theorem of Arithmetic):** The period $\log(2\pi)$ and the prime logarithms $\{\log p\}$ are **provably linearly independent over $\mathbb{Q}$**:
  $$m_0 \log(2\pi) + \sum_{j=1}^r m_j \log p_j = 0 \quad (m_j \in \mathbb{Z}) \implies m_0 = m_1 = \cdots = m_r = 0.$$
  *(Proof: $(2\pi)^{m_0} \prod p_j^{m_j} = 1$; if $m_0 \ne 0$, $\pi$ would be algebraic, contradicting Lindemann; hence $m_0 = 0$, and unique factorization gives $m_j = 0$).*
- **Open Status:** Linear independence over $\overline{\mathbb{Q}}$ (with algebraic coefficients) cannot be deduced from Baker's theorem because $2\pi$ is transcendental.

### 3. Herglotz Representation Theorem on Discrete Groups (Herglotz 1911)
- **Theorem:** A sequence $C: \mathbb{Z} \to \mathbb{C}$ is positive-definite if and only if it is the Fourier–Stieltjes transform of a non-negative measure on the circle $\mathbb{T} = \mathbb{R}/\mathbb{Z}$:
  $$C(K) = \int_{\mathbb{T}} e^{2\pi i K \theta} \, d\mu(\theta).$$
  Positivity on $\mathbb{Z}$ forces the spectral support strictly onto unitary characters ($|\chi| = 1$), uniformly bounding $|C(K)| \le C(0)$.

### 4. Normalized Intertwining Operators (Langlands–Shahidi)
- **Theorem:** In centered spectral parameters $\lambda \in \mathfrak{a}_\mathbb{C}^*$ ($s = 1/2 + \lambda$), normalized intertwining operators satisfy the involution identity $N(\lambda) N(-\lambda) = I$ and the adjoint formula $N(\lambda)^* = N(-\overline{\lambda})$.
- **Unitarity Axis:** $N(\lambda)^* = N(\lambda)^{-1} \iff -\overline{\lambda} = -\lambda \iff \lambda \in i\mathbb{R} \iff \mathrm{Re}(s) = 1/2$.
  Under its canonical realization, the intertwining operator is unitary strictly on the critical axis.

### 5. Selberg Trace Formula and the Geometric Laplacian Spectrum (Selberg 1956)
- **Theorem:** For a compact hyperbolic surface $\Gamma \backslash \mathbb{H}$, Laplace eigenvalues $\lambda_n = 1/4 + r_n^2 \ge 0$ are real.
- **Precision:** Zeros of the Selberg zeta function are forced onto the critical line $\mathrm{Re}(s) = 1/2$ (when $\lambda_n \ge 1/4$) **or the exceptional real segment $[0, 1]$** (when $0 \le \lambda_n < 1/4$). Self-adjointness restricts zeros to $\frac{1}{2} + i\mathbb{R} \cup [0, 1]$, not universally onto the critical line alone.

### 6. Lindemann Transcendence and Lattice Disjointness (Lindemann 1882)
- **Theorem:** For $K \ne J \in \mathbb{Z}$ and $m, n \in \mathbb{Z} \setminus \{0\}$, the equality $m(2\pi)^K = n(2\pi)^J$ is impossible because $\pi$ is transcendental. This certifies the target contradiction of the TC reductio argument.

---

# Part II: Constraint Mechanism Taxonomy

To systematically classify how mathematical constraints arise across representation systems, we organize established mathematics into twelve structural paradigms:

```
                                  CONSTRAINT MECHANISMS
                                            │
        ┌───────────────────────────────────┼──────────────────────────────────┐
        ▼                                   ▼                                  ▼
   [SPECTRAL / POSITIVITY]             [REPRESENTATION / FRAME]         [ALGEBRAIC / GEOMETRIC]
   • Positivity (Herglotz/Bochner)     • Overcomplete Redundancy        • Transcendence (Lindemann/Baker)
   • Unitarity (Mellin-Plancherel)     • Frame Range Consistency        • Rational Independence (Proved)
   • Self-Adjointness (Selberg/Weyl)   • Duality & Adjointness          • Lattice Duality (Poisson / 2π)
   • Operator Inversion (Shahidi)      • Cocycle / Descent Gluing       • Multi-Scale Rigidity (Kronecker/Bohr)
```

### 1. Positivity
*Principle:* Requiring a quadratic form to be positive semidefinite ($B(f, f) \ge 0$) forces all spectral decomposition measures to be non-negative, eliminates negative spectral components, and establishes Cauchy–Schwarz bounds $|B(f, g)|^2 \le B(f, f) B(g, g)$.
*Primary Examples:* Herglotz (1911), Bochner (1932), Weil Positivity Criterion (1952), Li's Criterion (1997).

### 2. Unitarity
*Principle:* Transformations that preserve the Hilbert norm ($\|U f\| = \|f\|$) have spectrum confined strictly to the unit circle $\mathbb{T} = \{z \in \mathbb{C} : |z| = 1\}$.
*Primary Examples:* Mellin–Plancherel theorem on $L^2(\mathbb{R}_{>0}, dx)$, canonical $L^2$ realization of the unitary principal series of $\mathrm{SL}(2, \mathbb{R})$, Langlands–Shahidi normalized intertwining operators on $\lambda \in i\mathbb{R}$.

### 3. Self-Adjointness
*Principle:* An operator equal to its Hilbert adjoint ($H = H^*$) has purely real spectrum ($\sigma(H) \subset \mathbb{R}$). Parameterized as $\lambda_n = s_n(1-s_n) = 1/4 + r_n^2$, real eigenvalues $\lambda_n \ge 0$ force $r_n \in \mathbb{R}$ ($\mathrm{Re}(s_n) = 1/2$) or $r_n \in i[-1/2, 1/2]$ ($s_n \in [0, 1]$ real).
*Primary Examples:* Laplace–Beltrami operator on hyperbolic manifolds (Selberg 1956), Hilbert–Pólya programme.

### 4. Overcomplete Redundancy
*Principle:* Representing a vector in a space of higher dimension or redundant index set introduces non-trivial linear relations among the representation coefficients.
*Primary Examples:* Frame theory (Duffin–Schaeffer 1952), continuous wavelet transform (Calderón 1964).

### 5. Frame Range Consistency
*Principle:* The image of the analysis operator $T: \mathcal{H} \to \ell^2(I)$ is a proper closed subspace. Any valid coefficient vector must lie in the range of the projection $P = T(T^* T)^{-1} T^*$, yielding explicit compatibility equations $(I - P)c = 0$.
*Primary Examples:* Daubechies–Grossmann–Meyer (1986), Casazza (2000).

### 6. Duality and Adjointness
*Principle:* Intertwining an operator with its dual or adjoint forces symmetry across a reflection axis. On the fixed axis of the involution, the operator must be self-adjoint or unitary.
*Primary Examples:* Pontryagin duality, Riemann functional equation as Fourier duality on $\mathbb{A}_\mathbb{Q}$, scattering matrix reflection $\phi(s)^{-1} = \phi(1-s) = \overline{\phi(s)}$.

### 7. Cocycle and Descent Gluing
*Principle:* When an object is specified across overlapping charts or scale grades, the transition isomorphisms must satisfy the transitivity cocycle $g_{ik} = g_{jk} \circ g_{ij}$.
*Primary Examples:* Grothendieck descent theory, sheaf cohomology.

### 8. Transcendence Rigidity
*Principle:* Transcendental numbers cannot satisfy non-trivial polynomial relations with algebraic coefficients.  
*(Important Negative Boundary: General statements such as "powers of transcendental numbers cannot be algebraic" are FALSE: $b = 2^{1/\sqrt{2}}$ is transcendental, but $b^{\sqrt{2}} = 2 \in \mathbb{Q}$. Transcendence rigidity must be established theorem-by-theorem with exact hypotheses).*
*Primary Examples:* Hermite (1873, $e$), Lindemann (1882, $\pi$), Gelfond–Schneider (1934), Baker (1966).

### 9. Functional Transcendence
*Principle:* Analytic functions satisfying differential equations cannot satisfy unanticipated algebraic relations unless they arise from geometric subgroups.
*Primary Examples:* Ax–Schanuel (1971), Ax–Lindemann–Weierstrass (Pila–Wilkie).

### 10. Lattice Duality and Exponential Periods
*Principle:* The kernel of the complex exponential map $\exp: \mathbb{C} \to \mathbb{C}^\times$ is discrete and equal to $2\pi i \mathbb{Z}$. In Fourier analysis, this period defines the dual lattice $\Lambda^*$ and governs exact Poisson summation identities.
*Primary Examples:* Poisson summation formula, Jacobi theta inversion $\theta(-1/\tau) = \sqrt{\tau/i} \, \theta(\tau)$.

### 11. Group-Action Rigidity
*Principle:* Non-commuting group actions (such as translation and dilation in the $ax+b$ group) impose rigid structural constraints via canonical commutation relations.
*Primary Examples:* Kirillov orbit method, Stone–von Neumann theorem.

### 12. Scale Rigidity
*Principle:* If an analytic function is invariant under two incommensurable multiplicative scales, the generated group of scales is dense, forcing the function to be constant.
*Primary Examples:* Multi-period rigidity, Kronecker–Weyl equidistribution theorem.

---

# Part III: Detailed Theorem Cards

Below are 19 detailed theorem cards evaluating candidate constraint mechanisms using the project's standard triage template.

---

### Card 1: Herglotz Representation Theorem (1911)
- **Mathematical Domain:** Classical Harmonic Analysis / Spectral Measure Theory on $\mathbb{Z}$
- **The Theorem:** A sequence $(c_K)_{K \in \mathbb{Z}} \subset \mathbb{C}$ is positive-definite (i.e., for every finite sequence $(\xi_K)_{K=-N}^N$, $\sum_{J, K=-N}^N c_{J-K} \xi_J \overline{\xi_K} \ge 0$) if and only if there exists a unique non-negative finite Borel measure $\mu \ge 0$ on the circle $\mathbb{T} = \mathbb{R}/\mathbb{Z}$ such that:
  $$c_K = \int_{\mathbb{T}} e^{2\pi i K \theta} \, d\mu(\theta) \qquad \forall K \in \mathbb{Z}.$$
- **Constraint Mechanism:** $\text{Positivity on } \mathbb{Z} \Longrightarrow \text{Spectral measure supported strictly on unitary characters } |e^{2\pi i \theta}| = 1$. The Cauchy–Schwarz inequality for positive-definite sequences immediately forces uniform boundedness: $|c_K| \le c_0$. Any isolated non-unitary character $\eta(K) = \tau^{-K(\delta + i\gamma)}$ with $\delta \ne 0$ grows exponentially ($\tau^{|K||\delta|}$) in at least one direction as $|K| \to \infty$, which is mathematically incompatible with positive-definiteness.
- **Relationship to TC:**
  - Grade index $K \in \mathbb{Z} \longleftrightarrow$ Group element in $\mathbb{Z}$.
  - Grade evaluation $\eta_\rho(K) = \tau^{-K(\rho - 1/2)} \longleftrightarrow$ Group character $\chi(K)$.
  - Unitarity condition $\delta = 0 \longleftrightarrow$ Character lives on the dual circle $\mathbb{T}$.
- **Missing Hypothesis:** TC must prove that the sequence of grade projections $C(K) = \langle F_K, F_0 \rangle$ or the contracted grade Gram matrix $W_{J, K}$ is **positive-definite as a bilateral sequence on $\mathbb{Z}$**.
- **Circularity Risk:** `HIGH / RH_EQUIVALENT`. Proving that $C(K)$ is positive-definite on $\mathbb{Z}$ requires bounding the sum over zeros, which is typically equivalent to already knowing that no exponentially growing terms ($\tau^{K\delta}$) exist, i.e., assuming RH.
- **Relevance Score:** `DIRECT`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Herglotz, G. (1911). *Über Potenzreihen mit positivem reellen Teil im Einheitsskreis*. Ber. Verh. Sachs. Ges. Wiss. Leipzig, 63, 501–511.

---

### Card 2: Bochner's Theorem on Locally Compact Abelian Groups (1932/1940)
- **Mathematical Domain:** Abstract Harmonic Analysis / Duality Theory
- **The Theorem:** Let $G$ be a locally compact abelian (LCA) group and $\widehat{G}$ its Pontryagin dual. A continuous function $f: G \to \mathbb{C}$ is positive-definite if and only if it is the Fourier–Stieltjes transform of a unique non-negative finite regular Borel measure $\mu \ge 0$ on $\widehat{G}$:
  $$f(x) = \int_{\widehat{G}} \chi(x) \, d\mu(\chi).$$
- **Constraint Mechanism:** Every character $\chi \in \widehat{G}$ is by definition **unitary** ($|\chi(x)| = 1$). Positivity of $f$ guarantees that its harmonic decomposition contains zero non-unitary exponential components.
- **Relationship to TC:**
  - LCA group $G = (\mathbb{R}, +)$ in logarithmic coordinates $u = \log x \longleftrightarrow$ Station coordinate space.
  - Scale dilations $u \mapsto u + K \log \tau \longleftrightarrow$ Discrete subgroup $\Gamma = \log \tau \cdot \mathbb{Z} \subset \mathbb{R}$.
- **Missing Hypothesis:** Proving that the continuous grade-correlation kernel on $\mathbb{R}$ is positive-definite without truncating the physical domain or omitting positive spectral tails.
- **Circularity Risk:** `RH_EQUIVALENT`.
- **Relevance Score:** `HIGH`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Bochner, S. (1932). *Vorlesungen über Fouriersche Integrale*. Akademische Verlagsgesellschaft, Leipzig; Weil, A. (1940). *L'intégration dans les groupes topologiques et ses applications*. Hermann, Paris.

---

### Card 3: Pontryagin Duality and the Unitary Dual of $\mathbb{Z}$ (1934)
- **Mathematical Domain:** Topological Algebra / Pontryagin Duality
- **The Theorem:** For the discrete group $(\mathbb{Z}, +)$, the algebraic homomorphisms into $\mathbb{C}^\times$ form the multiplicative group $\mathrm{Hom}(\mathbb{Z}, \mathbb{C}^\times) \cong \mathbb{C}^\times$ via $\chi \mapsto \chi(1)$. The Pontryagin dual $\widehat{\mathbb{Z}}$, defined as the group of *continuous unitary homomorphisms* into $\mathbb{T} = U(1)$, is topologically isomorphic to the circle $\mathbb{T}$:
  $$\widehat{\mathbb{Z}} \cong \mathbb{R} / \mathbb{Z} = \mathbb{T}.$$
  A homomorphism $\chi_z(K) = z^K$ is bounded on $\mathbb{Z}$ if and only if $|z| = 1$.
- **Constraint Mechanism:** Any condition imposing uniform boundedness ($\sup_{K \in \mathbb{Z}} |\chi(K)| < \infty$) on a representation of $\mathbb{Z}$ forces the character to lie in the unitary dual $\widehat{\mathbb{Z}}$.
- **Relationship to TC:**
  - $\eta_\rho(K) = (\tau^{-(\delta + i\gamma)})^K = z^K$ with $z = \tau^{-\delta - i\gamma}$.
  - $|z| = \tau^{-\delta} = 1 \iff \delta = 0$.
- **Missing Hypothesis:** An independent analytical principle that forces the grade action on the zeta spectrum to be uniformly bounded for all $K \in \mathbb{Z}$.
- **Circularity Risk:** `LOW` (as an algebraic fact), but promoting boundedness to a proof of $\delta = 0$ is `RH_EQUIVALENT`.
- **Relevance Score:** `DIRECT`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Pontryagin, L. S. (1934). *The theory of topological commutative groups*. Annals of Mathematics, 35(2), 361–388.

---

### Card 4: Mellin–Plancherel Theorem on the Critical Axis (1897/1910/1948)
- **Mathematical Domain:** Functional Analysis / Multiplicative Harmonic Analysis
- **The Theorem:** Let $L^2(\mathbb{R}_{>0}, dx)$ be the Hilbert space with standard Lebesgue measure, and let $\mathcal{M}_{1/2}$ be the centered Mellin transform:
  $$\mathcal{M}_{1/2} f(t) = \int_0^\infty f(x) x^{1/2 + it} \, \frac{dx}{x} = \int_0^\infty f(x) x^{-1/2 + it} \, dx.$$
  Then $\mathcal{M}_{1/2}$ is a unitary Hilbert space isomorphism:
  $$\mathcal{M}_{1/2}: L^2(\mathbb{R}_{>0}, dx) \xrightarrow{\sim} L^2\left(\mathbb{R}, \frac{dt}{2\pi}\right),$$
  satisfying the exact isometry identity:
  $$\int_0^\infty |f(x)|^2 \, dx = \frac{1}{2\pi} \int_{-\infty}^\infty |\mathcal{M}_{1/2} f(t)|^2 \, dt.$$
- **Constraint Mechanism:** The line $\mathrm{Re}(s) = 1/2$ is the unique vertical axis in the complex plane where the multiplicative dilation characters $x^{s-1/2} = x^{it}$ are unitary with respect to the change-of-measure isomorphism between $L^2(\mathbb{R}_{>0}, dx)$ and the Haar space $L^2(\mathbb{R}_{>0}, dx/x)$.
- **Relationship to TC:**
  - Explains precisely why the centered coordinate $z = s - 1/2$ is universal: it maps the non-unitary Mellin domain directly onto the unitary axis $i\mathbb{R}$.
- **Missing Hypothesis:** Showing that the arithmetic zeta zero evaluations interact with test functions strictly within the $L^2$ isometry domain without boundary/regularization defects.
- **Circularity Risk:** `NONE` (standard proved theorem).
- **Relevance Score:** `DIRECT`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Mellin, H. (1897). *Über die fundamentale Wichtigkeit des Satzes von Cauchy für die Theorie der Gamma- und hypergeometrischen Funktionen*. Acta Soc. Sci. Fennicae, 21(1); Titchmarsh, E. C. (1948). *Introduction to the Theory of Fourier Integrals*. Oxford University Press.

---

### Card 5: Unitary Principal Series of $\mathrm{SL}(2, \mathbb{R})$ (1946/1947/1954)
- **Mathematical Domain:** Representation Theory of Reductive Lie Groups
- **The Theorem:** Let $G = \mathrm{SL}(2, \mathbb{R})$ and $B = MAN$ the standard Borel subgroup. Consider the parabolic induction $\pi_s = \operatorname{Ind}_B^G(\chi_s)$, where $\chi_s\begin{pmatrix} a & b \\ 0 & a^{-1} \end{pmatrix} = |a|^{2s}$.
  The representation $\pi_s$ is unitary under the canonical $L^2(K)$ compact-picture inner product if and only if:
  $$\mathrm{Re}(s) = \frac{1}{2} \qquad (s = 1/2 + it, \; t \in \mathbb{R}).$$
  *(Precision on Complementary Series: For real parameters $s \in (0, 1) \setminus \{1/2\}$, $\pi_s$ can be unitarized with a different, non-local intertwining inner product. Therefore, being off the unitary axis does not forbid all Hilbert space structures, but it strictly rules out the canonical $L^2$ realization).*
- **Constraint Mechanism:** Canonical $L^2$ representation unitarity strictly confines the induction parameter $s$ to the critical line $\mathrm{Re}(s) = 1/2$.
- **Relationship to TC:**
  - Demonstrates that representation theory naturally identifies $\mathrm{Re}(s) = 1/2$ as the canonical unitary axis under standard Lebesgue/Haar measures.
- **Missing Hypothesis:** Establishing an explicit representation-theoretic embedding where individual off-line zeta zeros act as induction parameters.
- **Circularity Risk:** `LOW` as representation theory; `HIGH` if asserting that zeta zeros are automorphic parameters.
- **Relevance Score:** `HIGH`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Gelfand, I. M., & Naimark, M. A. (1946). *Unitary representations of the Lorentz group*. Izv. Akad. Nauk SSSR Ser. Mat., 11(5), 411–504; Bargmann, V. (1947). *Irreducible unitary representations of the Lorentz group*. Annals of Mathematics, 48(3), 568–640; Harish-Chandra. (1954). *Representations of semi-simple Lie groups II*. Trans. Amer. Math. Soc., 76, 26–65.

---

### Card 6: Normalized Intertwining Operators and Centered Unitary Axis (Langlands–Shahidi)
- **Mathematical Domain:** Automorphic Forms / Langlands Programme
- **The Theorem:** In the theory of parabolic induction for reductive groups (Langlands 1976, Arthur 1989, Shahidi 1990), let $\lambda \in \mathfrak{a}_\mathbb{C}^*$ be the centered spectral parameter (related to the classical $s$-parameter by $s = 1/2 + \lambda$). The standard intertwining operator $M(w, \lambda): I(\lambda) \to I(w\lambda)$ is normalized by scalar $L$-factors:
  $$N(w, \lambda) = r(w, \lambda)^{-1} M(w, \lambda).$$
  For the simple reflection $w_0$ with $w_0^2 = 1$ ($w_0\lambda = -\lambda$), the normalized operator satisfies:
  1. **Involution identity:** $N(w_0, \lambda) N(w_0, -\lambda) = I \implies N(w_0, \lambda)^{-1} = N(w_0, -\lambda)$.
  2. **Adjoint relation:** Under the canonical compact picture, $N(w_0, \lambda)^* = N(w_0, -\overline{\lambda})$.
  3. **Unitary axis:**
     $$N(w_0, \lambda)^* = N(w_0, \lambda)^{-1} \iff -\overline{\lambda} = -\lambda \iff \overline{\lambda} = \lambda \text{ (in purely imaginary coordinate system)} \iff \lambda \in i\mathbb{R}.$$
     In classical coordinates, $\lambda \in i\mathbb{R} \iff \mathrm{Re}(s) = 1/2$.
- **Constraint Mechanism:** Unitarity $N^* = N^{-1}$ holds on the imaginary axis $\lambda \in i\mathbb{R}$, translating to the critical line $\mathrm{Re}(s) = 1/2$.
- **Relationship to TC:**
  - Provides a deep automorphic analogue to the TC reflection identity $\eta^{-1} = \overline{\eta} \iff \delta = 0$.
- **Missing Hypothesis:** Constructing an intertwining operator whose normalizing factors explicitly govern individual off-line Riemann zeta zeros.
- **Circularity Risk:** `MEDIUM`. The Langlands–Shahidi normalization is proved independently of RH, but isolating zero locations from operator poles requires non-tempered spectral control.
- **Relevance Score:** `HIGH`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Langlands, R. P. (1976). *On the Functional Equations Satisfied by Eisenstein Series*. Lecture Notes in Math., Vol. 544, Springer-Verlag; Arthur, J. (1989). *Intertwining operators and residues I. Weighted characters*. J. Funct. Anal., 84(1), 19–84; Shahidi, F. (1990). *A proof of Langlands' conjecture on Plancherel measures; complementary series for p-adic groups*. Annals of Mathematics, 132(2), 273–330.

---

### Card 7: Automorphic Scattering Matrix Unitarity on the Critical Axis (Selberg/Lax–Phillips)
- **Mathematical Domain:** Spectral Theory / Scattering Theory of Automorphic Functions
- **The Theorem:** On the modular surface $X = \mathrm{PSL}(2, \mathbb{Z}) \backslash \mathbb{H}$, the continuous spectrum of the Laplace–Beltrami operator $\Delta$ is described by the non-holomorphic Eisenstein series $E(z, s)$. Its constant term scattering matrix is:
  $$\phi(s) = \sqrt{\pi} \frac{\Gamma(s - 1/2) \zeta(2s - 1)}{\Gamma(s) \zeta(2s)} = \frac{\xi(2s - 1)}{\xi(2s)}.$$
  The scattering operator satisfies the functional equation $\phi(s) \phi(1-s) = 1$ and the real symmetry $\phi(\overline{s}) = \overline{\phi(s)}$.
  On the line $\mathrm{Re}(s) = 1/2$, $\phi(s)$ is strictly **unitary**:
  $$|\phi(1/2 + it)| = 1 \qquad \forall t \in \mathbb{R}.$$
- **Constraint Mechanism:** Unitarity of physical wave scattering on the modular surface forces the scattering matrix to have modulus 1 on the critical line $\mathrm{Re}(s) = 1/2$.
- **Relationship to TC:**
  - Shows that the ratio of xi functions is unitary precisely on $\mathrm{Re}(s) = 1/2$.
- **Missing Hypothesis & The Resonances Barrier:** The zeros of $\zeta(2s)$ in the denominator of $\phi(s)$ generate poles of $\phi(s)$ at $s = \rho/2 = 1/4 + \delta/2 + i\gamma/2$. These poles lie in the half-plane $\mathrm{Re}(s) < 1/2$ (the *unphysical sheet*). In Lax–Phillips scattering theory, these poles are **scattering resonances**, NOT eigenvalues! Self-adjointness of the Laplacian on the automorphic surface does not constrain the locations of resonances in the non-physical sheet.
- **Circularity Risk:** `HIGH`. Proving that resonances cannot have $\delta \ne 0$ is strictly equivalent to RH.
- **Relevance Score:** `HIGH`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Selberg, A. (1956). *Harmonic analysis and discontinuous groups in weakly symmetric Riemannian spaces with applications to Dirichlet series*. J. Indian Math. Soc., 20, 47–87; Lax, P. D., & Phillips, R. S. (1976). *Scattering Theory for Automorphic Functions*. Annals of Mathematics Studies, No. 87, Princeton University Press.

---

### Card 8: Stone–von Neumann Theorem and Canonical Commutation Relations (1930/1931)
- **Mathematical Domain:** Quantum Mechanics / Operator Algebras
- **The Theorem:** Let $U(t) = e^{i t P}$ and $V(s) = e^{i s X}$ be strongly continuous one-parameter unitary groups on a separable Hilbert space $\mathcal{H}$ satisfying the Weyl form of the canonical commutation relations (CCR):
  $$U(t) V(s) = e^{i s t} V(s) U(t) \qquad \forall s, t \in \mathbb{R}.$$
  Then $\mathcal{H}$ decomposes into a direct sum of invariant subspaces, on each of which the pair $(U, V)$ is unitarily equivalent to the standard Schrödinger representation on $L^2(\mathbb{R})$.
- **Constraint Mechanism:** Non-commutation of translation and modulation operators produces **complete structural rigidity**: there is only one irreducible unitary representation up to unitary equivalence.
- **Relationship to TC:**
  - TC studies the interplay between translation in log-space ($u \mapsto u + \log p$) and dilation ($u \mapsto \tau^K u$).
- **Missing Hypothesis:** The TC translation and dilation operators act on the same coordinate axis (dilations act as translations of $\log x$), so they do not satisfy the Heisenberg CCR $U V = e^{i s t} V U$, but rather the affine group relation $D_a T_b = T_{a b} D_a$.
- **Circularity Risk:** `NONE` (standard theorem), but `ANALOGY_ONLY` for the Heisenberg group.
- **Relevance Score:** `MEDIUM`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Stone, M. H. (1930). *Linear transformations in Hilbert space. III. Operational methods and group theory*. Proc. Natl. Acad. Sci. U.S.A., 16(2), 172–175; von Neumann, J. (1931). *Die Eindeutigkeit der Schrödingerschen Operatoren*. Math. Ann., 104, 570–578.

---

### Card 9: Iterated Operator Representations and Dynamical Sampling (Christensen–Hasannasab / Aldroubi et al.)
- **Mathematical Domain:** Applied Harmonic Analysis / Frame Theory / Dynamical Sampling
- **The Theorems:**
  1. *Christensen & Hasannasab (2017, IEOT / arXiv:1704.08918):*  
     Let $\mathcal{H}$ be a separable Hilbert space and $\{f_k\}_{k \in \mathbb{Z}}$ a frame for $\mathcal{H}$. The frame is representable by iterates of a bounded operator $T \in B(\mathcal{H})$ ($f_k = T^k f_0$) if and only if the kernel of the synthesis operator $\ker(T^*)$ is shift-invariant in $\ell^2(\mathbb{Z})$.
  2. *Aldroubi, Cabrelli, Molter, & Petrosyan (2017, JFA / arXiv:1602.04527):*  
     For a **normal operator** $A \in B(\mathcal{H})$, the system of iterations $\{A^n g\}_{n \ge 0, g \in \mathcal{G}}$ forms a Bessel sequence if and only if the spectral measure of $A$ restricted to the cyclic subspace is supported on the closed unit disk $\mathbb{D} = \{|z| \le 1\}$. For bilateral sequences $\{A^k g\}_{k \in \mathbb{Z}}$, the Bessel condition under normality forces the spectral measure onto the unit circle $\mathbb{T} = \{|z| = 1\}$.
  3. *Derived Norm-Growth Proposition:*  
     If an operator $T$ has an isolated eigenmode $v_\lambda$ with eigenvalue $\lambda$ ($T^* v_\lambda = \lambda v_\lambda$), then $|\langle v_\lambda, T^K v \rangle|^2 = |\lambda|^{2K} |\langle v_\lambda, v \rangle|^2$. For the bilateral sum $\sum_{K \in \mathbb{Z}} |\langle v_\lambda, T^K v \rangle|^2$ to be finite, one must have $|\lambda| = 1$ (since $|\lambda| > 1$ blows up as $K \to +\infty$, and $|\lambda| < 1$ blows up as $K \to -\infty$).
- **Constraint Mechanism:** Bilateral $\ell^2$ Bessel energy bounds $\sum_{K \in \mathbb{Z}} |\langle w, T^K v \rangle|^2 < \infty$ exclude isolated eigenvalues with $|\lambda| \ne 1$.
- **Separation from Frame Range Consistency:**  
  *Crucial Distinction:* This Bessel growth argument concerns $\ell^2$ summability of operator powers. It must NOT be confused with **Frame Range Consistency** (Card 10), which is an algebraic projection property of redundant coefficient spaces.
- **Circularity Risk:** `HIGH / RH_EQUIVALENT` when applied directly to zero pairings, because requiring $\sum_{K \in \mathbb{Z}} |\eta_\rho(K)|^2 < \infty$ assumes $\delta = 0$ in advance.
- **Relevance Score:** `HIGH`
- **Evidence Classification:** `PROVED_SPECIAL_CASE` (normal operators / cyclic point spectrum)
- **Citation:** Christensen, O., & Hasannasab, M. (2017). *Operator representations of frames: boundedness, duality, and stability*. Integral Equations and Operator Theory, 88(4), 483–499; Aldroubi, A., Cabrelli, C., Molter, U., & Petrosyan, A. (2017). *Iterative actions of normal operators*. Journal of Functional Analysis, 272(3), 1121–1146.

---

### Card 10: Frame Range Projection and Redundancy Consistency Equations (Duffin–Schaeffer)
- **Mathematical Domain:** Hilbert Space Frame Theory
- **The Theorem:** Let $\mathcal{F} = \{f_i\}_{i \in I}$ be a frame for Hilbert space $\mathcal{H}$ with frame operator $S = T^* T = \sum_{i \in I} f_i \otimes f_i^*$. The analysis operator $T: \mathcal{H} \to \ell^2(I)$ is an injective topological embedding with closed range $\operatorname{Ran}(T) \subset \ell^2(I)$.
  The orthogonal projection operator $P: \ell^2(I) \to \operatorname{Ran}(T)$ is given by:
  $$P = T S^{-1} T^*.$$
  A sequence $c = (c_i)_{i \in I} \in \ell^2(I)$ is the frame coefficient sequence of some vector $v \in \mathcal{H}$ ($c = Tv$) **if and only if** it satisfies the **redundancy consistency equation**:
  $$\boxed{(I - P) c = 0 \iff c_i = \sum_{j \in I} (T S^{-1} T^*)_{i, j} c_j \qquad \forall i \in I.}$$
  Furthermore, the redundancy of the frame is precisely the nullspace $\ker(T^*) = \operatorname{Ran}(T)^\perp$:
  $$\ker(T^*) = \left\{ d \in \ell^2(I) : \sum_{i \in I} d_i f_i = 0 \right\}.$$
- **Constraint Mechanism:** $\text{Redundancy} \iff \ker(T^*) \ne \{0\} \Longrightarrow \text{Exact linear compatibility equations among representation coefficients}$.
- **Relationship to TC:**
  - This is the exact mathematical formulation of the TC premise: *"redundancy adds no new information, but imposes exact compatibility constraints."*
  - Distinct from Bessel growth: Frame range consistency investigates whether an off-line zero sequence $c_K = \tau^{-K(\delta+i\gamma)}$ lies in the kernel of $(I - P)$ without first requiring $\ell^2$ convergence.
- **Missing Hypothesis:** Constructing an authentic redundant frame from the TC grade family whose range projection projector $P$ acts on zero profiles.
- **Circularity Risk:** `LOW / OPEN`. This mechanism is not trivially equivalent to Weil positivity.
- **Relevance Score:** `DIRECT`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Duffin, R. J., & Schaeffer, A. C. (1952). *A class of nonharmonic Fourier series*. Trans. Amer. Math. Soc., 72(2), 341–366; Daubechies, I., Grossmann, A., & Meyer, Y. (1986). *Painless nonorthogonal expansions*. Journal of Mathematical Physics, 27(5), 1271–1283; Casazza, P. G. (2000). *The art of frame theory*. Taiwanese J. Math., 4(2), 129–201.

---

### Card 11: Hermite–Biehler Theorem and de Branges Positivity (1856/1879/1968)
- **Mathematical Domain:** Complex Analysis / Spaces of Entire Functions
- **The Theorem:** An entire function $E(z) = A(z) - i B(z)$ (with $A, B$ real on $\mathbb{R}$) satisfies the Hermite–Biehler condition:
  $$|E(z)| > |E(\overline{z})| \qquad \forall z \in \mathbb{C}^+ = \{z : \mathrm{Im}(z) > 0\},$$
  if and only if:
  1. $A(z)$ and $B(z)$ have only real zeros, which are strictly interlacing.
  2. The phase function $\theta(t) = -\arg E(t)$ is strictly increasing: $\theta'(t) = \frac{A'(t)B(t) - A(t)B'(t)}{|E(t)|^2} > 0$ for all $t \in \mathbb{R}$.
  3. All zeros of $E(z)$ lie strictly in the open lower half-plane $\mathbb{C}^-$.
  The de Branges space $\mathcal{H}(E)$ has positive reproducing kernel:
  $$K(w, z) = \frac{E(z)\overline{E(w)} - \overline{E(\overline{z})} E(\overline{w})}{2\pi i (\overline{w} - z)}.$$
- **Constraint Mechanism:** Positivity of the metric in $\mathcal{H}(E)$ forces $E$ to be Hermite–Biehler, which forces the zeros of its real part $A(t) = \xi(1/2 - it)$ to be strictly real.
- **Relationship to TC:**
  - Real zeros of $A(t)$ correspond to critical-line zeros $\mathrm{Re}(\rho) = 1/2$.
- **The Conrey–Li Barrier:** Louis de Branges attempted to construct a family of spaces $\mathcal{H}(E)$ whose ordering would force $\xi(s)$ to have only real zeros. In 2000, Conrey and Li proved that de Branges' proposed positivity conditions **fail** for the Riemann xi function because the gamma factor growth violates the necessary space monotonicity.
- **Circularity Risk:** `REFUTED_WITHIN_SCOPE` for de Branges' specific axioms; `RH_EQUIVALENT` in general.
- **Relevance Score:** `HIGH`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** de Branges, L. (1968). *Hilbert Spaces of Entire Functions*. Prentice-Hall; Conrey, J. B., & Li, X.-J. (2000). *A note on some positivity conditions related to zeta- and L-functions*. Int. Math. Res. Not., 2000(18), 929–940; Lagarias, J. C. (1999). *Hilbert spaces of entire functions and Dirichlet L-functions*. Frontiers in Number Theory, Physics, and Geometry, Vol. 1.

---

### Card 12: Weil's Explicit-Formula Positivity Criterion (1952)
- **Mathematical Domain:** Analytic Number Theory / Distribution Theory
- **The Theorem:** Let $\mathcal{W}$ be the Weil distribution on $\mathbb{R}_{>0}^\times$. For any test function $f$ of the form $F = f * f^*$ (where $f^*(x) = x^{-1} \overline{f(1/x)}$), the explicit formula evaluates to:
  $$\mathcal{W}(f * f^*) = \log \pi |f(1)|^2 + \int_0^\infty \dots - \sum_\rho \mathcal{M}F(\rho).$$
  On the critical line $\rho = 1/2 + i\gamma$, $\mathcal{M}(f * f^*)(\rho) = |\mathcal{M}f(1/2 + i\gamma)|^2 \ge 0$.
  **Weil's Theorem:** The Riemann Hypothesis holds if and only if $\mathcal{W}(f * f^*) \ge 0$ for all valid test functions $f$.
- **Constraint Mechanism:** Quadratic positivity $B(f, f) = \mathcal{W}(f * f^*) \ge 0$ prevents negative spectral zero contributions $-\sum_\rho \mathcal{M}F(\rho)$ from driving the form negative.
- **Relationship to TC:**
  - Direct foundation of the TC auxiliary Weil route.
- **Missing Hypothesis:** Proving that the Weil form is positive semidefinite across the entire test function space without assuming RH.
- **Circularity Risk:** `RH_EQUIVALENT`.
- **Relevance Score:** `DIRECT`
- **Evidence Classification:** `RH_EQUIVALENT`
- **Citation:** Weil, A. (1952). *Sur les "formules explicites" de la théorie des nombres premiers*. Medd. Lunds Univ. Mat. Sem., Tome Suppl., 252–265; Bombieri, E. (2000). *Problems of the Millennium: The Riemann Hypothesis*. Clay Mathematics Institute.

---

### Card 13: Li's Criterion on Conformal Disk Images (1997)
- **Mathematical Domain:** Complex Analysis / Conformal Mapping
- **The Theorem (Li 1997):** Let $\lambda_n = \sum_\rho [1 - (1 - 1/\rho)^n]$. The Riemann Hypothesis holds if and only if:
  $$\lambda_n \ge 0 \qquad \forall n \in \{1, 2, 3, \dots\}.$$
- **Constraint Mechanism:** The conformal map $w = 1 - 1/s$ maps the critical line $\mathrm{Re}(s) = 1/2$ onto the unit circle $|w| = 1$, and maps the off-critical half-plane $\mathrm{Re}(s) > 1/2$ into the open unit disk $|w| < 1$. If $\mathrm{Re}(\rho) = 1/2$, then $|1 - 1/\rho| = 1$, and $\sum_{\rho, \overline{\rho}} [1 - (1 - 1/\rho)^n] = 2 - 2\cos(n \theta_\rho) \ge 0$. If an off-line zero existed ($\delta > 0$), $|1 - 1/\rho| > 1$, and $(1 - 1/\rho)^n$ would grow exponentially as $n \to \infty$, forcing $\lambda_n < 0$.
- **Relationship to TC:**
  - Identical geometric mechanism: conformal projection to a unit circle where critical-line zeros produce non-negative cosines and off-line zeros produce unbounded exponential modes.
- **Missing Hypothesis:** Proving $\lambda_n \ge 0$ independently of the zero locations.
- **Circularity Risk:** `RH_EQUIVALENT`.
- **Relevance Score:** `HIGH`
- **Evidence Classification:** `RH_EQUIVALENT`
- **Citation:** Li, X.-J. (1997). *The positivity of a sequence of numbers and the Riemann hypothesis*. Journal of Number Theory, 65(2), 325–333; Bombieri, E., & Lagarias, J. C. (1999). *Complements to Li's criterion for the Riemann hypothesis*. J. Number Theory, 77(2), 274–287.

---

### Card 14: Nyman–Beurling / Báez-Duarte Closure Criterion (1950/1955/2003)
- **Mathematical Domain:** Functional Analysis / Approximation Theory
- **The Theorem:** Let $\rho_\alpha(x) = \{\alpha/x\} - \alpha\{1/x\}$ on $(0, 1)$. The Riemann Hypothesis holds if and only if the constant function $\mathbf{1}$ belongs to the $L^2(0, 1)$ closure of the linear span of $\{\rho_\alpha : 0 < \alpha \le 1\}$. Báez-Duarte (2003) simplified this to natural integer dilations: $\lim_{N \to \infty} \inf_{c_k} \| \mathbf{1} - \sum_{k=1}^N c_k \rho(k/x) \|_{L^2(0, 1)} = 0$.
- **Constraint Mechanism:** Approximation density in Hilbert space. If $\zeta(s)$ had a zero in $\mathrm{Re}(s) > 1/2$, the linear functional evaluating $\zeta$ at that zero would be a bounded functional annihilating the span, preventing closure.
- **Relationship to TC:**
  - Dilation span of step/fractional functions.
- **Missing Hypothesis:** Constructing explicit approximating coefficients whose rate of convergence does not degrade.
- **Circularity Risk:** `RH_EQUIVALENT`.
- **Relevance Score:** `MEDIUM`
- **Evidence Classification:** `RH_EQUIVALENT`
- **Citation:** Nyman, B. (1950). *On the One-Dimensional Translation Group and Semi-Group in Certain Function Spaces*. Ph.D. thesis, Uppsala; Beurling, A. (1955). *A closure problem related to the Riemann Zeta-function*. Proc. Natl. Acad. Sci. U.S.A., 41(5), 312–314; Báez-Duarte, L. (2003). *A strengthening of the Nyman-Beurling criterion for the Riemann hypothesis*. Atti Accad. Naz. Lincei Cl. Sci. Fis. Mat. Natur. Rend. Lincei (9) Mat. Appl., 14(1), 5–11.

---

### Card 15: Selberg Trace Formula Geodesic–Spectral Positivity (1956)
- **Mathematical Domain:** Differential Geometry / Spectral Geometry
- **The Theorem:** For a compact hyperbolic surface $X = \Gamma \backslash \mathbb{H}$, the Selberg zeta function $Z_X(s) = \prod_{p} \prod_{k=0}^\infty (1 - N(p)^{-(s+k)})$ has all its non-trivial complex zeros on $\mathrm{Re}(s) = 1/2$ or on the real interval $[0, 1]$.
- **Constraint Mechanism:** Zeros are defined by $\lambda_n = s_n(1 - s_n) = 1/4 + r_n^2$, where $\lambda_n$ are eigenvalues of the Laplace–Beltrami operator $\Delta = -y^2(\partial_x^2 + \partial_y^2)$. Because $\Delta \ge 0$ is self-adjoint on compact $X$, $\lambda_n \in \mathbb{R}_{\ge 0}$:
  - If $\lambda_n \ge 1/4$, $r_n \in \mathbb{R} \implies \mathrm{Re}(s_n) = 1/2$ (critical line).
  - If $0 \le \lambda_n < 1/4$, $r_n \in i[-1/2, 1/2] \implies s_n \in [0, 1]$ (real segment).
  - **Self-adjointness confines zeros to $\frac{1}{2} + i\mathbb{R} \cup [0, 1]$, not universally to the critical line alone.**
- **Relationship to TC:**
  - Prototype of provable critical-line zero location via an authentic self-adjoint geometric Laplacian.
- **Missing Hypothesis:** The Riemann zeta zeros have prime numbers $p$ in their Euler product, which do not correspond to geodesic lengths on any known smooth compact Riemannian manifold.
- **Circularity Risk:** `NONE` for Selberg zeta (`PROVED_STANDARD_THEOREM`); `ANALOGY_ONLY` for Riemann zeta.
- **Relevance Score:** `HIGH`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Selberg, A. (1956). *Harmonic analysis and discontinuous groups...* J. Indian Math. Soc., 20, 47–87; Hejhal, D. A. (1976). *The Selberg Trace Formula for PSL(2, R)*. Lecture Notes in Math., Vol. 548, Springer-Verlag.

---

### Card 16: Lindemann's Transcendence Theorem and Lattice Disjointness (1882)
- **Mathematical Domain:** Transcendence Theory / Diophantine Approximation
- **The Theorem:** If $\alpha \in \overline{\mathbb{Q}} \setminus \{0\}$, then $e^\alpha$ is transcendental. In particular, because $e^{\pi i} = -1 \in \overline{\mathbb{Q}}$, $\pi$ is transcendental over $\mathbb{Q}$. Consequently, $\tau = 2\pi$ is transcendental, and for any non-zero integer $m \ne 0$, $(2\pi)^m \notin \mathbb{Q}$.
- **Constraint Mechanism:** For $K \ne J \in \mathbb{Z}$ and $m, n \in \mathbb{Z} \setminus \{0\}$, the equality $m(2\pi)^K = n(2\pi)^J$ would imply $(2\pi)^{K-J} = n/m \in \mathbb{Q}$, which contradicts the transcendence of $\pi$.
- **Relationship to TC:**
  - Directly validates the core TC reductio implication:
    $$H \Longrightarrow \exists K \ne J, \; m, n \in \mathbb{Z} \setminus \{0\} : m \tau^K = n \tau^J.$$
    The target equality is a certified mathematical impossibility.
- **Missing Hypothesis:** The derivation proving that an off-line zero $H$ actually forces the coincidence $m \tau^K = n \tau^J$.
- **Circularity Risk:** `NONE`.
- **Relevance Score:** `DIRECT`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Lindemann, F. (1882). *Über die Zahl $\pi$*. Mathematische Annalen, 20(2), 213–225.

---

### Card 17: Linear Independence of Logarithms: Rational Independence vs. Baker's Theorem
- **Mathematical Domain:** Transcendence Theory / Diophantine Approximation
- **The Theorem (Proved Rational Linear Independence):**  
  Let $p_1, \dots, p_r$ be distinct prime numbers. Then:
  $$\boxed{\log(2\pi), \log p_1, \dots, \log p_r \text{ are linearly independent over } \mathbb{Q}.}$$
  *Proof:* Suppose $q_0 \log(2\pi) + \sum_{j=1}^r q_j \log p_j = 0$ with $q_j \in \mathbb{Q}$. Clearing denominators gives:
  $$m_0 \log(2\pi) + \sum_{j=1}^r m_j \log p_j = 0 \qquad (m_j \in \mathbb{Z}).$$
  Exponentiating yields:
  $$(2\pi)^{m_0} \prod_{j=1}^r p_j^{m_j} = 1 \iff (2\pi)^{m_0} = \prod_{j=1}^r p_j^{-m_j}.$$
  If $m_0 \ne 0$, then $(2\pi)^{m_0} \in \mathbb{Q}^\times$, so $2\pi = (\prod p_j^{-m_j})^{1/m_0} \in \overline{\mathbb{Q}}$, contradicting the transcendence of $\pi$ (Lindemann 1882). Thus $m_0 = 0$. Unique prime factorization in $\mathbb{Z}$ then forces $m_1 = \cdots = m_r = 0$. $\blacksquare$
- **The Baker Boundary (Open Status over $\overline{\mathbb{Q}}$):**  
  Baker's theorem (1966) establishes linear independence over $\overline{\mathbb{Q}}$ for logarithms of *algebraic* numbers. Because $2\pi$ is transcendental, $\log(2\pi)$ is the logarithm of a transcendental number. Therefore, Baker's theorem **does NOT apply** to linear combinations with algebraic coefficients:
  $$\boxed{\mathbb{Q}\text{-linear independence: PROVED}} \qquad \text{vs.} \qquad \boxed{\overline{\mathbb{Q}}\text{-linear independence: generally OPEN}}.$$
- **Significance for TC:** Proves rigorously that the grade scale $\log(2\pi)$ and the prime station scales $\{\log p\}$ are strictly incommensurable over $\mathbb{Q}$, ruling out any accidental rational resonance.
- **Circularity Risk:** `NONE` (for $\mathbb{Q}$-linear independence).
- **Relevance Score:** `DIRECT`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM` (over $\mathbb{Q}$)
- **Citation:** Lindemann, F. (1882); Baker, A. (1966). *Linear forms in the logarithms of algebraic numbers I*. Mathematika, 13(2), 204–216.

---

### Card 18: Ax–Schanuel Functional Transcendence Theorem (1971)
- **Mathematical Domain:** Model Theory / Functional Transcendence
- **The Theorem:** Let $y_1, \dots, y_n \in \mathbb{C}[[t]]$ (or any differential field of characteristic 0) be analytic functions that are $\mathbb{Q}$-linearly independent modulo $\mathbb{C}$. Then:
  $$\mathrm{tr.deg}_\mathbb{C} \, \mathbb{C}(y_1, \dots, y_n, e^{y_1}, \dots, e^{y_n}) \ge n + \mathrm{rank}\left( \frac{\partial y_i}{\partial t_j} \right).$$
- **Constraint Mechanism:** Guarantees that no unanticipated algebraic relation can hold among analytic exponential functions unless they arise from linear dependencies.
- **Relationship to TC:**
  - Could govern the algebraic independence of grade functions $\zeta(\tau^{-K} s)$ viewed as differential variables.
- **The Constant Numbers Barrier:** Ax–Schanuel applies strictly to **functions** (differential fields with non-zero derivations), NOT to numbers! It does not prove Schanuel's conjecture for the constants $2\pi, e, \log(2\pi)$.
- **Circularity Risk:** `NONE` (proved theorem), but applies only to functional configurations.
- **Relevance Score:** `MEDIUM`
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Ax, J. (1971). *On Schanuel's conjectures*. Annals of Mathematics, 93(2), 252–268; Pila, J. (2011). *O-minimality and the André-Oort conjecture for $\mathbb{C}^n$*. Annals of Mathematics, 173(3), 1779–1840.

---

### Card 19: Voronin's Universality Theorem as an Analytic Flexibility Barrier (1975)
- **Mathematical Domain:** Analytic Number Theory / Value Distribution Theory
- **The Theorem:** Let $0 < r < 1/4$ and let $f(s)$ be a non-vanishing continuous function on the disk $|s| \le r$ that is analytic in $|s| < r$. Then for any $\epsilon > 0$:
  $$\liminf_{T \to \infty} \frac{1}{T} \operatorname{meas}\left\{ t \in [0, T] : \max_{|s| \le r} \left| \zeta\left( s + \frac{3}{4} + it \right) - f(s) \right| < \epsilon \right\} > 0.$$
- **Constraint Mechanism:** **Negative Constraint / Anti-Rigidity.** Proves that $\zeta(s)$ has **maximum possible analytic flexibility** in the critical strip $1/2 < \sigma < 1$. It can uniformly approximate *any* analytic function on small disks.
- **Significance for TC:** **Severe Obstruction.** Any attempt to prove that off-line zeros cannot exist based on generic "analytic rigidity", smoothness, or overdetermined analytic conditions inside the strip is directly refuted by Voronin universality: $\zeta(s)$ is flexible enough to mimic arbitrary zeros unless the specific global Euler product and exact functional equation are explicitly utilized.
- **Circularity Risk:** `NONE` (established theorem proving flexibility).
- **Relevance Score:** `HIGH` (as an adversarial constraint)
- **Evidence Classification:** `PROVED_STANDARD_THEOREM`
- **Citation:** Voronin, S. M. (1975). *Theorem on the "universality" of the Riemann zeta-function*. Izv. Akad. Nauk SSSR Ser. Mat., 39(3), 475–486; Bagchi, B. (1981). *The Statistical Behaviour and Universality Properties of the Riemann Zeta-Function and Other Allied Dirichlet Series*. Ph.D. thesis, Indian Statistical Institute, Calcutta.

---

# Part IV: Direct TC Correspondences

For the mechanisms classified as `DIRECT` or `HIGH` relevance, we establish the explicit dictionary mapping established mathematical objects to TC objects:

### Dictionary 1: Frame Range Consistency $\longleftrightarrow$ TC Multi-Grade Redundancy
| Established Mathematical Object (Duffin–Schaeffer / Daubechies) | Transcendental Continuation (TC) Object |
| :--- | :--- |
| Hilbert space $\mathcal{H}$ | Hilbert space of admissible Schwartz test functions on $\mathbb{R}_{>0}^\times$ |
| Frame elements $\{f_K\}_{K \in I}$ | Graded family of representation profiles $\{F_K\}_{K=-M}^M$ |
| Analysis operator $T: \mathcal{H} \to \ell^2(I)$ | Grade expansion operator $T: v \mapsto (\langle v, F_K \rangle)_{K}$ |
| Synthesis operator $T^*: \ell^2(I) \to \mathcal{H}$ | Grade reconstruction operator $T^*: c \mapsto \sum_K c_K F_K$ |
| Frame operator $S = T^* T$ | Contracted grade metric operator $S = \sum_K F_K \otimes F_K^*$ |
| Range projection $P = T S^{-1} T^*$ | Authentic grade subspace projection operator |
| Redundancy constraint $(I - P) c = 0$ | Multi-grade compatibility constraint on zero evaluations |
| Nullspace $\ker(T^*) \ne \{0\}$ | Grade continuum cancellation subspace ($\sum_K b_K F_K = 0$) |

### Dictionary 2: Mellin–Plancherel Dilation $\longleftrightarrow$ TC Centered Coordinate
| Established Mathematical Object (Mellin / Titchmarsh) | Transcendental Continuation (TC) Object |
| :--- | :--- |
| Coordinate space $(\mathbb{R}_{>0}^\times, dx)$ | Station coordinate space on the positive half-line |
| Haar measure space $(\mathbb{R}_{>0}^\times, dx/x)$ | Multiplicative group space in log-coordinates $u = \log x$ |
| Shift factor $x^{-1/2}$ in change of measure | Centered coordinate shift $s - 1/2 = z$ |
| Unitary characters $x^{it}$ on Haar space | Critical-line characters $x^{i\gamma}$ ($\delta = 0$) |
| Dilation multiplier $\tau^{-K(s-1/2)}$ | Grade evolution character $\eta(K) = \tau^{-K(\rho - 1/2)}$ |
| Plancherel isometry axis $\mathrm{Re}(s) = 1/2$ | Canonical TC critical line |

### Dictionary 3: Herglotz Representation $\longleftrightarrow$ TC Grade Correlation
| Established Mathematical Object (Herglotz 1911) | Transcendental Continuation (TC) Object |
| :--- | :--- |
| Discrete abelian group $\mathbb{Z}$ | Bilateral grade group $\mathbb{Z} = \{K\}$ |
| Unitary dual $\widehat{\mathbb{Z}} = \mathbb{T} = \mathbb{R}/\mathbb{Z}$ | Unitary grade characters $(\delta = 0)$ |
| Positive-definite sequence $C(K)$ | Contracted grade correlation $C(K) = \langle F_K, F_0 \rangle$ |
| Spectral measure $\mu \ge 0$ on $\mathbb{T}$ | Non-negative zero spectral measure $d\mu(\gamma)$ |
| Boundedness $|C(K)| \le C(0)$ | Absence of exponential off-line growth ($\delta = 0$) |

---

# Part V: Known Barriers, False Routes, and Structural Obstructions

To maintain absolute mathematical integrity, we document the structural obstructions that refute naive implementations of TC constraint hypotheses:

### 1. The Descent / Cocycle Triviality Barrier
- **Tempting Hypothesis:** "Because $\mathcal{Z}_\tau(s, K) = \zeta(\tau^{-K} s)$ represents the same global object across different grade charts with transition functions $s_J = \tau^{J-K} s_K$, sheaf descent or cocycle consistency equations will force a constraint on the zeros."
- **Mathematical Refutation:** The transition maps $\sigma_{K \to J}(s) = \tau^{K-J} s$ form a 1-cocycle on the cyclic group $(\mathbb{Z}, +)$. Because $\tau^{J-L} \cdot \tau^{K-J} = \tau^{K-L}$ is an exact algebraic identity in the field of scales, the cocycle condition $g_{JL} \circ g_{KJ} = g_{KL}$ is satisfied **identically and trivially** for *any* arbitrary holomorphic function $f(s)$. It contains zero information about the zeros of $\zeta(s)$ and imposes no constraint on $\delta$.

### 2. The Scale-Genericity Barrier
- **Tempting Hypothesis:** "The bilateral grade centering second difference $C_h = 4\sinh^2(h \log \tau / 2) > 0$ depends crucially on $\tau = 2\pi$."
- **Mathematical Refutation:** As proved in repository verification suite `tests/test_bilateral_second_variation.py` (`TestBilateralScaleSpecificity`), the identity:
  $$\tau^{K\delta} + \tau^{-K\delta} - 2 = 4\sinh^2\left(\frac{K\delta \log a}{2}\right) > 0 \quad (\delta \ne 0)$$
  holds for **every real scale $a > 1$**, including rational scales $a = 2, 3$ and algebraic scales $a = \sqrt{2}$. The positivity of the defect is a property of the hyperbolic sine function on $\mathbb{R}$, completely independent of $2\pi$ or arithmetic transcendence. Any argument relying solely on the positivity of this defect is scale-generic and cannot invoke $2\pi$-specific transcendence.

### 3. The Transcendence Hypothesis Misapplication Barrier
- **Tempting Hypothesis:** "Applying Baker's theorem to linear forms in $\log(2\pi)$ and $\log p$ proves they cannot satisfy algebraic relations."
- **Mathematical Refutation:**
  1. Rational linear independence of $\log(2\pi)$ and $\{\log p\}$ is **provable from first principles** combined with Lindemann's theorem (Card 17).
  2. However, Baker's theorem requires logarithms of **algebraic numbers**. Because $2\pi$ is transcendental, Baker's theorem **does NOT apply** to linear combinations with algebraic coefficients.
  3. Asserting that $(2\pi)^\alpha$ is transcendental for irrational algebraic $\alpha$ requires **Schanuel's Conjecture**, which is an unproved open conjecture (`CONJECTURAL`).
  4. Broad generalizations like "powers of transcendental numbers cannot be algebraic" are mathematically false ($b = 2^{1/\sqrt{2}}$ is transcendental, but $b^{\sqrt{2}} = 2 \in \mathbb{Q}$).

### 4. The Automorphic Resonance vs. Eigenvalue Barrier
- **Tempting Hypothesis:** "Because the Eisenstein scattering matrix $\phi(s) = \xi(2s-1)/\xi(2s)$ is unitary on $\mathrm{Re}(s) = 1/2$, the zeros of $\xi(2s)$ in the denominator must lie on the critical line."
- **Mathematical Refutation:** The poles of $\phi(s)$ produced by zeros of $\xi(2s)$ lie at $s = \rho/2 = 1/4 + \delta/2 + i\gamma/2 \in (0, 1/2) \times i\mathbb{R}$, which is in the left half-plane $\mathrm{Re}(s) < 1/2$. In Lax–Phillips scattering theory, these are **scattering resonances**, NOT discrete eigenvalues. The self-adjointness of the Laplacian on $L^2(\mathrm{PSL}(2, \mathbb{Z}) \backslash \mathbb{H})$ constrains discrete eigenvalues in $\mathrm{Re}(s) \ge 1/2$, but provides no geometric barrier preventing resonances from existing off the line $\mathrm{Re}(s) = 1/4$ (which corresponds to $\delta \ne 0$).

### 5. Voronin Universality and the Flexibility Barrier
- **Tempting Hypothesis:** "Analytic continuation across multiple grades creates an overdetermined system that eliminates zeros."
- **Mathematical Refutation:** Voronin's Universality Theorem (1975) proves that $\zeta(s)$ is maximally flexible in the strip $1/2 < \sigma < 1$. It can approximate any non-vanishing analytic target arbitrarily well. General analytic arguments that do not enforce the exact Euler product and global Poisson theta inversion fail because local analytic flexibility allows arbitrary zero placements.

---

# Part VI: Recommended Mathematical Experiments

Based on this literature review, the following four rigorous analytic/symbolic investigations are recommended:

### Experiment 1: The Frame Range Projection Nullspace Test (TC-FRAME-01)
- **Objective:** Discretize the grade family $\{F_K\}_{K=-M}^M$ on an admissible function space $\mathcal{H}$, form the frame operator $S = \sum_{K} F_K \otimes F_K^*$, and compute the range projection operator:
  $$P = T S^{-1} T^*.$$
- **Method:** Test whether an injected off-line zero sequence $c_K = \tau^{-K(\delta + i\gamma)}$ ($\delta \ne 0$) violates the range condition:
  $$\|(I - P) c\|_{\ell^2} > 0$$
  on a finite grade window $[-M, M]$ without requiring an a priori $\ell^2$ norm bound.
- **Goal:** Determine whether frame redundancy creates an active constraint that separates critical from off-critical zeros.

### Experiment 2: The Multi-Scale Commutator Defect Test
- **Objective:** Evaluate the commutator $[D_\tau, T_p]$ between the grade dilation operator $D_\tau$ and prime station translation $T_p$ in log-coordinates.
- **Method:** Using the proved $\mathbb{Q}$-linear independence of $\log(2\pi)$ and $\{\log p\}$, evaluate whether the generated group of affine transformations forms an ergodic action that forces spectral measures to be invariant.
- **Goal:** Determine whether the non-commutation of proved incommensurable scales creates analytic rigidity.

### Experiment 3: Normalized Intertwining Parameterization Audit
- **Objective:** Implement the exact centered spectral parameterization $\lambda = s - 1/2$ for the normalized intertwining operator $N(\lambda)$ on the completed Archimedean-prime kernel.
- **Method:** Verify the adjoint formula $N(\lambda)^* = N(-\overline{\lambda})$ and calculate the exact defect of unitarity $N(\lambda)^* N(\lambda) - I$ for off-line displacements $\lambda = \delta + i\gamma$.
- **Goal:** Provide an exact operator-theoretic dictionary for the TC reflection defect $B_\rho(K)$.

### Experiment 4: The Dynamical Sampling Bessel Energy Boundary
- **Objective:** Evaluate the bilateral grade energy sum $S_N = \sum_{K=-N}^N |\langle w, F_K \rangle|^2$ for authentic prime-windowed test functions.
- **Method:** Quantify the exact growth rate of $S_N$ as a function of $N$ for critical zeros ($\delta = 0$) versus synthetic off-line zeros ($\delta > 0$).
- **Goal:** Determine whether the Bessel boundary can be certified on a finite compact window.

---

# Comprehensive Comparison Matrix (Section 17 Table)

The table below synthesizes the 19 evaluated mechanisms against the Transcendental Continuation framework:

| Mechanism | Established Theorem | Constraint Produced | Why $2\pi$ Matters | TC Correspondence | Missing Premise | Circularity Risk | Relevance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Frame Range Consistency** | Duffin & Schaeffer (1952) | Range projection $(I - P)c = 0$ imposes equations from redundancy | Redundant sampling grid density | Redundancy of multi-grade representations | Evaluating range projection on non-unitary zero profiles | `LOW / OPEN` | `DIRECT` |
| **Mellin–Plancherel** | Mellin (1897), Titchmarsh (1948) | Multiplicative $L^2$ isometry holds on $\mathrm{Re}(s) = 1/2$ | Normalizes Fourier transform of $\log x$ | Centered coordinate $s - 1/2$ is the unitary axis | Admissible $L^2$ probe regularization | `NONE` (proved) | `DIRECT` |
| **Rational Linear Independence** | Lindemann (1882) + Arithmetic | $\log(2\pi)$ and $\{\log p\}$ are $\mathbb{Q}$-linearly independent | $2\pi$ is transcendental period of $\exp$ | Scale $\tau$ and prime scales $p$ are strictly incommensurable | Elevating $\mathbb{Q}$-independence to $\overline{\mathbb{Q}}$ requires Baker extension | `NONE` (proved over $\mathbb{Q}$) | `DIRECT` |
| **Herglotz Representation** | Herglotz (1911) | Positive-definiteness on $\mathbb{Z} \implies$ measure on $\mathbb{T}$ ($|\chi| = 1$) | Dual circle $\mathbb{T} = \mathbb{R}/\mathbb{Z}$ has period $2\pi$ | $\eta_\rho(K)$ must be unitary if grade sequence is positive-definite | Proving grade correlation sequence is positive-definite on $\mathbb{Z}$ | `HIGH / RH_EQUIV` | `DIRECT` |
| **Bochner's Theorem** | Bochner (1932) | Continuous positive-definiteness $\implies$ measure on unitary dual | Defines self-dual Fourier transform | Continuous grade correlation kernel is positive-definite | Complete positive tail enclosure $R_U \ge 0$ | `HIGH / RH_EQUIV` | `HIGH` |
| **Pontryagin Dual of $\mathbb{Z}$** | Pontryagin (1934) | Bounded homomorphisms of $\mathbb{Z}$ are unitary ($|z| = 1$) | Exponential map kernel is $2\pi i \mathbb{Z}$ | $\eta_\rho(K) = z^K$ bounded $\iff \delta = 0$ | Proving grade action is uniformly bounded on $\mathbb{Z}$ | `LOW` (algebraic), `RH_EQUIV` (analytic) | `DIRECT` |
| **Unitary Principal Series** | Bargmann (1947), Harish-Chandra (1954) | Induced representation of $\mathrm{SL}(2, \mathbb{R})$ unitary $\iff \mathrm{Re}(s) = 1/2$ under canonical $L^2$ | Modulates $K$-type decomposition | Zeta zeros as spectral parameters of group representation | Coupling individual off-line zeros to automorphic representations | `LOW` (rep. theory), `HIGH` (zeros) | `HIGH` |
| **Normalized Intertwining** | Langlands (1976), Shahidi (1990) | $N(\lambda)^* = N(\lambda)^{-1} \iff \lambda \in i\mathbb{R} \iff \mathrm{Re}(s) = 1/2$ | $2\pi$ appears in gamma factor of $r(s)$ | Inversion $\eta^{-1} = \overline{\eta} \iff \delta = 0$ | Constructing localized intertwining operator for zero set | `MEDIUM` | `HIGH` |
| **Automorphic Scattering** | Selberg (1956), Lax–Phillips (1976) | Scattering matrix $|\phi(1/2+it)| = 1$ unitary on critical line | Normalization of modular Eisenstein series | Ratio $\xi(2s-1)/\xi(2s)$ is unitary on $\mathrm{Re}(s) = 1/2$ | Proving resonances in $\mathrm{Re}(s) < 1/2$ cannot exist off-line | `HIGH / RH_EQUIV` | `HIGH` |
| **Stone–von Neumann** | Stone (1930), von Neumann (1931) | Uniqueness of irreducible unitary CCR representation | Period of Weyl displacement phase $e^{i s t}$ | Non-commutation of dilation and station translation | Commutator in log-space is affine, not Heisenberg | `NONE` (proved) | `MEDIUM` |
| **Iterated Frame Orbits** | Christensen–Hasannasab (2017), Aldroubi (2017) | Bilateral Bessel orbit under normal operator $\implies$ spectrum on $\mathbb{T}$ | Generator scale $\tau = 2\pi$ | $\lambda_\rho = \tau^{-\delta-i\gamma} \implies \tau^{-\delta} = 1 \iff \delta = 0$ | Embedding grade family as a Bessel sequence in Hilbert space | `HIGH / RH_EQUIV` | `HIGH` |
| **Hermite–Biehler / de Branges** | de Branges (1968), Conrey–Li (2000) | Metric positivity forces phase monotonicity and real zeros | Growth of gamma factor $\Gamma(s/2)$ | Real zeros of $A(t) \iff \mathrm{Re}(\rho) = 1/2$ | Establishing de Branges space ordering without Conrey–Li failure | `REFUTED_WITHIN_SCOPE` | `HIGH` |
| **Weil Positivity** | Weil (1952), Bombieri (2000) | Quadratic form $W(f * f^*) \ge 0 \iff$ RH holds | Fourier self-duality of explicit formula | Core of TC auxiliary Weil route | Proving $W(f * f^*) \ge 0$ unconditionally | `RH_EQUIVALENT` | `DIRECT` |
| **Li's Criterion** | Li (1997) | Positivity $\lambda_n \ge 0 \iff$ zeros on $|w| = 1$ | Conformal map circle normalization | Projection to unit circle where off-line modes blow up | Proving $\lambda_n \ge 0$ without zero summation | `RH_EQUIVALENT` | `HIGH` |
| **Nyman–Beurling** | Nyman (1950), Beurling (1955) | Density of fractional parts $\iff$ no zeros in $\sigma > 1/2$ | Periodicity of fractional part $\{x\}$ | Dilation span closure in Hilbert space | Constructing approximating coefficients with uniform bounds | `RH_EQUIVALENT` | `MEDIUM` |
| **Selberg Trace Formula** | Selberg (1956) | Laplacian $\Delta \ge 0$ self-adjoint $\implies$ zeros on $\frac{1}{2}+i\mathbb{R} \cup [0, 1]$ | Geodesic length spectrum normalization | Real spectrum forces zeros onto line or real axis | Riemann zeros do not correspond to smooth compact manifold | `NONE` (Selberg), `ANALOGY` (Riemann) | `HIGH` |
| **Lindemann Transcendence** | Lindemann (1882) | $\pi \notin \overline{\mathbb{Q}} \implies m(2\pi)^K \ne n(2\pi)^J$ ($K \ne J$) | $2\pi$ is transcendental period of $\exp$ | Authorizes TC reductio target contradiction | Proving off-line zero forces integer lattice coincidence | `NONE` (proved) | `DIRECT` |
| **Ax–Schanuel** | Ax (1971) | Functional transcendence of differential exponentials | Differential period of $\exp(y)$ | Functional independence of grade representations | Applies to differential functions, not constant numbers | `NONE` (proved) | `MEDIUM` |
| **Voronin Universality** | Voronin (1975) | Uniform approximation of arbitrary analytic targets | Governs ergodic translation flow | **Adversarial barrier:** proves $\zeta(s)$ is maximally flexible | Overcoming flexibility by enforcing global Euler product | `NONE` (proved barrier) | `HIGH` |

---

# Detailed Resolution of Highest-Priority Question (Section 18)

> **"Is there already a standard theorem saying that an arithmetic correlation indexed by a bilateral grade group must decompose into unitary characters under positivity, boundedness, self-adjointness, or redundancy constraints? If yes, identify the theorem exactly. What would TC have to prove in order to satisfy its hypotheses?"**

### 1. The Definitive Mathematical Answer
**YES.** Two classical theorems provide this exact assertion:

1. **Herglotz's Representation Theorem (1911):**  
   Any positive-definite sequence $C: \mathbb{Z} \to \mathbb{C}$ decomposes uniquely into a non-negative spectral measure supported **strictly on unitary characters**:
   $$C(K) = \int_{\mathbb{T}} e^{2\pi i K \theta} \, d\mu(\theta).$$
   No character with modulus different from 1 can appear in the spectral decomposition because Cauchy–Schwarz forces uniform boundedness: $|C(K)| \le C(0)$.

2. **Aldroubi, Cabrelli, Molter, & Petrosyan (2017) / Christensen & Hasannasab (2017):**  
   For a normal operator $T$ on a Hilbert space, if the bilateral orbit $\{T^K v\}_{K \in \mathbb{Z}}$ satisfies an upper frame (Bessel) energy bound $\sum_{K \in \mathbb{Z}} |\langle w, T^K v \rangle|^2 \le B \|w\|^2 < \infty$, then **all point spectrum eigenvalues of $T$ must lie strictly on the unit circle $\mathbb{T}$** ($|\lambda| = 1$).

### 2. What TC Would Have to Prove
To invoke these theorems to prove that the characters $\eta_\rho(K) = \tau^{-K(\rho - 1/2)}$ must be unitary ($\delta = 0$), TC must prove one of the following:

- **Route A (Herglotz Positivity):**  
  TC must construct a grade correlation sequence $C(K) = \langle F_K, F_0 \rangle$ that is **positive-definite on the discrete group $\mathbb{Z}$**:
  $$\sum_{J, K=-N}^N \xi_J \overline{\xi_K} C(J - K) \ge 0 \qquad \forall (\xi_K) \subset \mathbb{C}.$$
- **Route B (Bessel Orbit Energy):**  
  TC must prove that the bilateral family of grade profiles $\{F_K\}_{K \in \mathbb{Z}}$ forms a **Bessel sequence** in an authentic Hilbert space $\mathcal{H}$ containing the zero evaluation functionals:
  $$\sum_{K=-\infty}^\infty |\langle w_\rho, F_K \rangle_\mathcal{H}|^2 < \infty.$$

### 3. The Inescapable Circularity Barrier
If an off-line zero $\rho = 1/2 + \delta + i\gamma$ with $\delta \ne 0$ exists, its pairing with the grade family scales as:
$$|\langle w_\rho, F_K \rangle| \asymp \tau^{-K\delta}.$$
Because $K$ ranges bilaterally over $\mathbb{Z} = (-\infty, +\infty)$, this term **diverges exponentially** as $K \to +\infty$ (if $\delta < 0$) or as $K \to -\infty$ (if $\delta > 0$).
Consequently:
$$\sum_{K=-\infty}^\infty |\langle w_\rho, F_K \rangle|^2 = \infty.$$
Therefore:
> **Proving that the grade correlation sequence is positive-definite or that the grade orbit is a Bessel sequence requires in advance showing that the bilateral sum converges, which is mathematically equivalent to already knowing that $\delta = 0$.**

---

# Detailed Resolution of Second Highest-Priority Question (Section 19)

> **"Does the conceptual statement 'redundancy creates constraint' already have a standard mathematical realization through frame theory? Specifically determine whether an overcomplete orbit/frame $\{U_K v\}$ has coefficient-consistency conditions that could exclude a nonunitary spectral mode. If yes, give exact frame identities. If not, explain why the analogy fails."**

### 1. Frame Realization of "Redundancy Creates Constraint"
**YES.** Frame theory provides the exact, canonical mathematical formulation of this principle.
For an overcomplete frame $\mathcal{F} = \{f_K\}_{K \in I}$ in Hilbert space $\mathcal{H}$ with frame operator $S = \sum_{K \in I} f_K \otimes f_K^*$, the analysis operator $T: \mathcal{H} \to \ell^2(I)$ has a non-trivial orthogonal complement $\ker(T^*) = \operatorname{Ran}(T)^\perp \ne \{0\}$.

The exact frame consistency equations are:
$$\boxed{(I - P) c = 0, \qquad P = T(T^* T)^{-1} T^* = T S^{-1} T^*.}$$
In component form, any valid representation vector $c_K = \langle v, f_K \rangle$ must satisfy:
$$c_K = \sum_{J \in I} G_{K, J}^\dagger c_J,$$
where $G^\dagger = T S^{-1} T^*$ is the pseudo-inverse Gram projection.
Furthermore, any vector $d \in \ker(T^*)$ yields an exact linear dependency:
$$\sum_{K \in I} d_K f_K = 0.$$
Redundancy adds zero new information to $\mathcal{H}$, but strictly confines the coefficient space $\ell^2(I)$ to the range of $P$, eliminating all vectors in $\ker(T^*)$.

### 2. Can Frame Redundancy Exclude a Non-Unitary Spectral Mode?
**YES, but with an essential structural distinction:**

- **Distinction between Frame Consistency and Bessel Growth:**  
  1. *Bessel Growth Argument:* As shown in Card 9, if $\{T^K v\}_{K \in \mathbb{Z}}$ is a Bessel sequence, non-unitary eigenvalues are excluded by norm divergence. But as noted in Section 18, this relies on assuming bilateral $\ell^2$ energy bounds, which is circularly equivalent to RH.
  2. *Frame Range Consistency:* Frame range consistency $(I - P)c = 0$ is an **algebraic and geometric projection condition**. It asks whether an off-line zero sequence $c_K = \tau^{-K(\delta+i\gamma)}$ can lie in the range of the projection $P$ associated with a multi-grade frame, **without first requiring $c \in \ell^2$ or assuming positivity of the zero quadratic form**.
- **The Christensen–Deng–Heil Structural Boundary:**  
  By the Christensen–Deng–Heil Theorem (1999), the orbit $\{U^K v\}_{K \in \mathbb{Z}}$ of a single vector under a single unitary operator $U$ **can never be an overcomplete frame for an infinite-dimensional Hilbert space**. It is either an orthogonal sequence or a Riesz basis. In a Riesz basis, $T$ is surjective ($\operatorname{Ran}(T) = \ell^2(\mathbb{Z})$), which means **there is zero redundancy** ($\ker(T^*) = \{0\}$).
- **The Path Forward for TC:**  
  To obtain authentic redundancy ($\ker(T^*) \ne \{0\}$), TC must **not** rely on a single-operator unitary orbit. Authentic redundancy requires either:
  1. A finite-dimensional truncated grade family $K \in \{-M, \dots, M\}$ on a subspace, OR
  2. Multiple generators (e.g. combined prime station and grade translations), OR
  3. A two-parameter affine group action (dilation and translation).
  This preserves the frame-consistency branch as an open, viable research obligation.

---

# Detailed Resolution of Third Highest-Priority Question (Section 20)

> **"Determine whether $\mathrm{Re}(s) = 1/2$ is already a known unitarity axis in one or more established representation-theoretic constructions associated with: Mellin transforms, Eisenstein series, normalized intertwining operators, scattering matrices, automorphic $L$-functions. If yes, identify the exact operator and theorem."**

### 1. Definitive Mathematical Answer
**YES.** The line $\mathrm{Re}(s) = 1/2$ is universally established across modern representation theory, harmonic analysis, and automorphic forms as the **canonical unitarity axis**.

### 2. Authoritative Operators and Theorems

#### A. The Mellin–Plancherel Isometry Operator
- **Operator:** The centered Mellin transform $\mathcal{M}_{1/2}: L^2(\mathbb{R}_{>0}, dx) \to L^2(\mathbb{R}, dt/2\pi)$.
- **Theorem:** Mellin (1897), Titchmarsh (1948). The map $f \mapsto \mathcal{M}_{1/2} f$ is a unitary isomorphism if and only if $\mathrm{Re}(s) = 1/2$. The centering $s - 1/2 = it$ exactly aligns standard Lebesgue measure $dx$ with the unitary Haar characters $x^{it}$ of the dilation group $\mathbb{R}_{>0}^\times$.

#### B. The Normalized Intertwining Operator (Langlands–Shahidi)
- **Operator:** The normalized standard intertwining operator $N(\lambda) = r(\lambda)^{-1} M(\lambda)$ in centered spectral parameter $\lambda \in \mathfrak{a}_\mathbb{C}^*$ ($s = 1/2 + \lambda$).
- **Theorem:** Arthur (1989), Shahidi (1990).
  The operator satisfies the involution formula $N(\lambda) N(-\lambda) = I$ and the adjoint formula $N(\lambda)^* = N(-\overline{\lambda})$.
  Consequently:
  $$N(\lambda)^* = N(\lambda)^{-1} \iff -\overline{\lambda} = -\lambda \iff \overline{\lambda} = \lambda \iff \lambda \in i\mathbb{R} \iff \mathrm{Re}(s) = \frac{1}{2}.$$
  **The normalized intertwining operator is unitary if and only if $\mathrm{Re}(s) = 1/2$.**

#### C. The Automorphic Scattering Matrix (Selberg / Lax–Phillips)
- **Operator:** The non-holomorphic Eisenstein scattering matrix $\phi(s) = \frac{\xi(2s-1)}{\xi(2s)}$ on $\mathrm{PSL}(2, \mathbb{Z}) \backslash \mathbb{H}$.
- **Theorem:** Selberg (1956); Lax & Phillips (1976).
  The scattering matrix satisfies $\phi(s) \phi(1-s) = 1$ and $\phi(\overline{s}) = \overline{\phi(s)}$.
  On the line $\mathrm{Re}(s) = 1/2$:
  $$\phi(s)^{-1} = \phi(1-s) = \phi(\overline{s}) = \overline{\phi(s)} \implies |\phi(1/2 + it)| = 1.$$
  **The scattering operator is strictly unitary on $\mathrm{Re}(s) = 1/2$.**

#### D. The Unitary Principal Series of Reductive Lie Groups
- **Operator:** The induced representation $\pi_s = \operatorname{Ind}_B^G(|a|^{2s})$ for $G = \mathrm{SL}(2, \mathbb{R})$.
- **Theorem:** Bargmann (1947), Harish-Chandra (1954).
  The induced representation is unitary under the canonical $L^2$ inner product **if and only if $\mathrm{Re}(s) = 1/2$** (with complementary series requiring non-standard inner products).

---

# Part VII: Final Synthesis and Next Proof Target (Section 21)

### 1. Best Established Architecture
The most faithful, non-circular mathematical architecture structurally aligned with Transcendental Continuation is:
$$\boxed{\textbf{Mellin–Plancherel} \quad + \quad \textbf{Frame Range Consistency}}.$$

### 2. Why
1. **Mellin–Plancherel** explains why the centered coordinate $z = s - 1/2$ is universal: normalized multiplicative dilation on $L^2(dx)$ has multiplier $\tau^{-K(s-1/2)}$, establishing $\mathrm{Re}(s) = 1/2$ as the natural unitary axis independently of RH.
2. **Frame Range Consistency** formalizes the original TC vision that *"redundancy adds no new information, but imposes exact coefficient compatibility constraints"* through the projection identity $(I - P) c = 0$.
3. Unlike the bilateral Bessel-orbit route or Herglotz positivity, **Frame Range Consistency does not immediately presuppose $\ell^2$ summability of the zero evaluation sequence or positivity of the zero quadratic form**, keeping the research branch open.

### 3. What TC Already Has
- **Canonical Defect Formula:** $B_\rho(K) = \tau^{K\delta} + \tau^{-K\delta} - 2 = 4\sinh^2(K\delta \log \tau / 2) \ge 0$, vanishing if and only if $\delta = 0$.
- **Proved Rational Period Independence:** $\log(2\pi)$ and $\{\log p\}$ are provably linearly independent over $\mathbb{Q}$ (Card 17).
- **Algebraic Reductio Contradiction:** Lindemann's theorem guarantees that $m(2\pi)^K \ne n(2\pi)^J$ is an authentic, certified contradiction.
- **Centering Symmetry:** The centered coordinate $z = s - 1/2 = \delta + i\gamma$ aligns with the unitary axis of multiplicative harmonic analysis.

### 4. What TC Lacks
TC lacks an explicit construction realizing the grade family $\{F_K\}_{K=-M}^M$ as an authentic redundant frame on a concrete function space where the range projection $(I - P) c = 0$ actively rejects the non-unitary sequence $c_K = \tau^{-K(\delta+i\gamma)}$.

### 5. Is It Plausibly Independent of RH?
- **Frame Range Consistency:** `PLAUASIBLY_INDEPENDENT`. Because $(I - P)c = 0$ is a projection identity on a coefficient space, testing whether a specific sequence $c$ lies in $\operatorname{Ran}(T)$ is a geometric subspace membership problem, not a sign-definiteness assumption.
- **Bilateral Bessel Summability / Herglotz Positivity:** `KNOWN_EQUIVALENT_TO_RH`.

### 6. Next Concrete Proof Target
To test whether Transcendental Continuation can establish an active constraint through frame range consistency, the next precise mathematical target is:

$$\boxed{\begin{aligned}
&\textbf{Target Statement (TC-FRAME-01):} \\
&\text{Let } \mathcal{H} \text{ be an admissible Schwartz test function space on } \mathbb{R}_{>0}^\times, \text{ and let } \{F_K\}_{K=-M}^M \\
&\text{be a finite multi-grade family. Construct the frame operator } S = \sum_{K=-M}^M F_K \otimes F_K^* \text{ and range} \\
&\text{projection } P = T S^{-1} T^*. \text{ Determine whether the sequence of zero evaluations } c_K(\rho) = \tau^{-K(\rho-1/2)} \\
&\text{satisfies } \|(I - P) c(\rho)\| > 0 \text{ for any off-line zero } \mathrm{Re}(\rho) \ne 1/2, \text{ without requiring } c \in \ell^2(\mathbb{Z}) \\
&\text{or assuming Weil positivity.}
\end{aligned}}$$

---

# References & Citations

1. Aldroubi, A., Cabrelli, C., Molter, U., & Petrosyan, A. (2017). *Iterative actions of normal operators*. Journal of Functional Analysis, 272(3), 1121–1146. [DOI: 10.1016/j.jfa.2016.11.003](https://doi.org/10.1016/j.jfa.2016.11.003). [arXiv:1602.04527](https://arxiv.org/abs/1602.04527)
2. Arthur, J. (1989). *Intertwining operators and residues I. Weighted characters*. Journal of Functional Analysis, 84(1), 19–84. [DOI: 10.1016/0022-1236(89)90048-X](https://doi.org/10.1016/0022-1236(89)90048-X)
3. Ax, J. (1971). *On Schanuel's conjectures*. Annals of Mathematics, 93(2), 252–268. [DOI: 10.2307/1970774](https://doi.org/10.2307/1970774)
4. Báez-Duarte, L. (2003). *A strengthening of the Nyman-Beurling criterion for the Riemann hypothesis*. Atti Accad. Naz. Lincei Cl. Sci. Fis. Mat. Natur. Rend. Lincei (9) Mat. Appl., 14(1), 5–11.
5. Baker, A. (1966). *Linear forms in the logarithms of algebraic numbers I*. Mathematika, 13(2), 204–216. [DOI: 10.1112/S002557930000397X](https://doi.org/10.1112/S002557930000397X)
6. Bargmann, V. (1947). *Irreducible unitary representations of the Lorentz group*. Annals of Mathematics, 48(3), 568–640. [DOI: 10.2307/1969129](https://doi.org/10.2307/1969129)
7. Beurling, A. (1955). *A closure problem related to the Riemann Zeta-function*. Proceedings of the National Academy of Sciences U.S.A., 41(5), 312–314. [DOI: 10.1073/pnas.41.5.312](https://doi.org/10.1073/pnas.41.5.312)
8. Bochner, S. (1932). *Vorlesungen über Fouriersche Integrale*. Akademische Verlagsgesellschaft, Leipzig.
9. Bombieri, E. (2000). *Problems of the Millennium: The Riemann Hypothesis*. Clay Mathematics Institute.
10. Bombieri, E., & Lagarias, J. C. (1999). *Complements to Li's criterion for the Riemann hypothesis*. Journal of Number Theory, 77(2), 274–287. [DOI: 10.1006/jnth.1999.2392](https://doi.org/10.1006/jnth.1999.2392)
11. Casazza, P. G. (2000). *The art of frame theory*. Taiwanese Journal of Mathematics, 4(2), 129–201. [DOI: 10.11650/twjm/1500407287](https://doi.org/10.11650/twjm/1500407287)
12. Christensen, O., Deng, B., & Heil, C. (1999). *Density of Gabor frames*. Applied and Computational Harmonic Analysis, 7(3), 292–304. [DOI: 10.1006/acha.1999.0272](https://doi.org/10.1006/acha.1999.0272)
13. Christensen, O., & Hasannasab, M. (2017). *Operator representations of frames: boundedness, duality, and stability*. Integral Equations and Operator Theory, 88(4), 483–499. [DOI: 10.1007/s00020-017-2380-6](https://doi.org/10.1007/s00020-017-2380-6). [arXiv:1704.08918](https://arxiv.org/abs/1704.08918)
14. Conrey, J. B., & Li, X.-J. (2000). *A note on some positivity conditions related to zeta- and L-functions*. International Mathematics Research Notices, 2000(18), 929–940. [DOI: 10.1155/S1073792800000508](https://doi.org/10.1155/S1073792800000508)
15. Daubechies, I., Grossmann, A., & Meyer, Y. (1986). *Painless nonorthogonal expansions*. Journal of Mathematical Physics, 27(5), 1271–1283. [DOI: 10.1063/1.527388](https://doi.org/10.1063/1.527388)
16. de Branges, L. (1968). *Hilbert Spaces of Entire Functions*. Prentice-Hall, Englewood Cliffs, NJ.
17. Duffin, R. J., & Schaeffer, A. C. (1952). *A class of nonharmonic Fourier series*. Transactions of the American Mathematical Society, 72(2), 341–366. [DOI: 10.1090/S0002-9947-1952-0047179-6](https://doi.org/10.1090/S0002-9947-1952-0047179-6)
18. Gelfand, I. M., & Naimark, M. A. (1946). *Unitary representations of the Lorentz group*. Izv. Akad. Nauk SSSR Ser. Mat., 11(5), 411–504.
19. Harish-Chandra. (1954). *Representations of semi-simple Lie groups II*. Transactions of the American Mathematical Society, 76(1), 26–65. [DOI: 10.1090/S0002-9947-1954-0059950-5](https://doi.org/10.1090/S0002-9947-1954-0059950-5)
20. Hejhal, D. A. (1976). *The Selberg Trace Formula for PSL(2, R)*. Lecture Notes in Mathematics, Vol. 548, Springer-Verlag, Berlin.
21. Herglotz, G. (1911). *Über Potenzreihen mit positivem reellen Teil im Einheitsskreis*. Ber. Verh. Sachs. Ges. Wiss. Leipzig, 63, 501–511.
22. Langlands, R. P. (1976). *On the Functional Equations Satisfied by Eisenstein Series*. Lecture Notes in Mathematics, Vol. 544, Springer-Verlag, Berlin.
23. Lax, P. D., & Phillips, R. S. (1976). *Scattering Theory for Automorphic Functions*. Annals of Mathematics Studies, No. 87, Princeton University Press.
24. Li, X.-J. (1997). *The positivity of a sequence of numbers and the Riemann hypothesis*. Journal of Number Theory, 65(2), 325–333. [DOI: 10.1006/jnth.1997.2137](https://doi.org/10.1006/jnth.1997.2137)
25. Lindemann, F. (1882). *Über die Zahl $\pi$*. Mathematische Annalen, 20(2), 213–225. [DOI: 10.1007/BF01446522](https://doi.org/10.1007/BF01446522)
26. Mellin, H. (1897). *Über die fundamentale Wichtigkeit des Satzes von Cauchy für die Theorie der Gamma- und hypergeometrischen Funktionen*. Acta Societatis Scientiarum Fennicae, 21(1), 1–115.
27. Nyman, B. (1950). *On the One-Dimensional Translation Group and Semi-Group in Certain Function Spaces*. Ph.D. thesis, University of Uppsala.
28. Pontryagin, L. S. (1934). *The theory of topological commutative groups*. Annals of Mathematics, 35(2), 361–388. [DOI: 10.2307/1968438](https://doi.org/10.2307/1968438)
29. Selberg, A. (1956). *Harmonic analysis and discontinuous groups in weakly symmetric Riemannian spaces with applications to Dirichlet series*. Journal of the Indian Mathematical Society, 20, 47–87.
30. Shahidi, F. (1990). *A proof of Langlands' conjecture on Plancherel measures; complementary series for p-adic groups*. Annals of Mathematics, 132(2), 273–330. [DOI: 10.2307/1971524](https://doi.org/10.2307/1971524)
31. Stone, M. H. (1930). *Linear transformations in Hilbert space. III. Operational methods and group theory*. Proceedings of the National Academy of Sciences U.S.A., 16(2), 172–175. [DOI: 10.1073/pnas.16.2.172](https://doi.org/10.1073/pnas.16.2.172)
32. Titchmarsh, E. C. (1948). *Introduction to the Theory of Fourier Integrals*. 2nd ed., Oxford University Press.
33. von Neumann, J. (1931). *Die Eindeutigkeit der Schrödingerschen Operatoren*. Mathematische Annalen, 104, 570–578. [DOI: 10.1007/BF01457956](https://doi.org/10.1007/BF01457956)
34. Voronin, S. M. (1975). *Theorem on the "universality" of the Riemann zeta-function*. Izv. Akad. Nauk SSSR Ser. Mat., 39(3), 475–486.
35. Weil, A. (1952). *Sur les "formules explicites" de la théorie des nombres premiers*. Meddelanden Från Lunds Universitets Matematiska Seminarium, Tome Supplémentaire, 252–265.
36. Yakaboylu, E. (2024). *Nontrivial Riemann Zeros as Spectrum*. arXiv:2408.15135 [math-ph]. [https://arxiv.org/abs/2408.15135](https://arxiv.org/abs/2408.15135)
37. Hamann, L. (2022). *Geometric Eisenstein Series, Intertwining Operators, and Shin's Averaging Formula*. arXiv:2209.08175 [math.NT]. [https://arxiv.org/abs/2209.08175](https://arxiv.org/abs/2209.08175)
38. Chen, D., King, E. J., & Shonkwiler, C. (2025). *Approximately Dual and Pseudo-Dual Probabilistic Frames*. Applied and Computational Harmonic Analysis, 84, 101885. arXiv:2505.13885 [math.FA]. [https://arxiv.org/abs/2505.13885](https://arxiv.org/abs/2505.13885)
39. Bownik, M., & van Velthoven, J. T. (2025). *Frame redundancy and Beurling density*. arXiv:2509.11887 [math.FA]. [https://arxiv.org/abs/2509.11887](https://arxiv.org/abs/2509.11887)
40. Gonçalves, F. (2023). *A classification of Fourier summation formulas and crystalline measures*. arXiv:2312.11185 [math.CA]. [https://arxiv.org/abs/2312.11185](https://arxiv.org/abs/2312.11185)
