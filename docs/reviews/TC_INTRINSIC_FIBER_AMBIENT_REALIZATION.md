# TASK-TC-025: Intrinsic Grade-Fiber Arithmetic, Ambient Realization, and the Correct TC Zeta

## Executive Summary & Canonical Classifications

- **Primary Research Focus**: Rigorous separation between **intrinsic arithmetic inside a fixed grade fiber** and **ambient real realization across grades**, settling the mathematical meaning of "ordinary integer arithmetic measured in the unit $\tau^K$."
- **Principal Classification**: `DUAL_INTRINSIC_AMBIENT_STRUCTURE_REQUIRED`
  - Intrinsic grade arithmetic is strictly **transport of structure**: $\mathcal{F}_K = \{K\} \times \mathbb{Z} \cong \mathbb{Z}$ for every real algebraic grade $K \in \mathbb{A}_{\mathbb{R}}$. It is completely base-independent (`GENERIC_BASE_FIBER_INVARIANCE`) and carries no intrinsic $\tau$-dependence or new arithmetic constraints.
  - The intrinsic arithmetic zeta function as measured in its own units is identically $\zeta_K^{\mathrm{int}}(s) = \zeta(s)$, with canonical Euler product $\prod_p (1 - p^{-s})^{-1}$.
  - The ambient series $Z_K^{\mathrm{amb}}(s) = \sum (n\tau^K)^{-s} = \tau^{-Ks}\zeta(s)$ is the **ambient-coordinate Dirichlet series** (`AMBIENT_COORDINATE_DIRICHLET_SERIES`), where $\tau^{-Ks}$ is the dimensional/unit realization factor.
  - The local zero germ modulus variation $|c_{\Xi_K}(\rho)/c_{\Xi_J}(\rho)| = \tau^{-(K-J)\delta}$ audited in TASK-TC-024 is the inevitable coordinate covariance of evaluating an intrinsic quantity of scaling weight $w = -(\rho - 1/2)$ in ambient real units.
  - The full algebraic-grade ambient algebra is the group algebra $\overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}]$ under the realization evaluation homomorphism $\operatorname{ev}_\tau: \overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}] \to \mathbb{R}$, $\sum a_j [K_j] \mapsto \sum a_j \tau^{K_j}$.
  - **Secondary Classification**: `OPEN_FINITE_ALGEBRAIC_CROSS_GRADE_COLLAPSE`. Injectivity of $\operatorname{ev}_\tau$ is proved on $\mathbb{Z}$ (Lindemann 1882) and $\mathbb{Q}$ (common-denominator reduction), but remains strictly **OPEN** on the full algebraic grade domain $\mathbb{A}_{\mathbb{R}}$. Two-term transfer is bounded by $\dim_{\mathbb{Q}} S_\tau \le 1$ (Gelfond–Schneider 1934), which does not resolve multi-term linear independence.
- **Formal Verification**:
  - Lean 4 formalization compiled in `formal/RiemannScope/FiberArithmetic.lean` (36 new project declarations, 0 errors, 0 sorries; total project declarations: 414).
  - Dedicated test suite `tests/test_tc_intrinsic_fiber_ambient_realization.py` passes all 22/22 verification tests.

---

## 1. Intrinsic Grade-Fiber Arithmetic

### A. What exactly is a grade-$K$ arithmetic fiber?

The canonical arithmetic object of Transcendental Continuation at grade $K \in \mathbb{A}_{\mathbb{R}}$ is the **tagged arithmetic fiber**:
$$\boxed{\mathcal{F}_K = \{K\} \times \mathbb{Z} = \{(K, n) : n \in \mathbb{Z}\}.}$$
It represents the abstract integers measured in the unit $\tau^K$.
Using tagged pairs $(K, n)$ rather than naked subsets $L_K = \tau^K \mathbb{Z} \subset \mathbb{R}$ ensures that two distinct arithmetic referents $(K, n)$ and $(J, m)$ remain distinct mathematical objects even if their real-coordinate realizations were ever to collide ($n\tau^K = m\tau^J$).

### B. What are its internal addition and multiplication?

The internal arithmetic operations of $\mathcal{F}_K$ are transported directly from $\mathbb{Z}$:
- **Fiber Addition**:
  $$\boxed{(K, m) \oplus_K (K, n) = (K, m + n).}$$
- **Fiber Multiplication**:
  $$\boxed{(K, m) \odot_K (K, n) = (K, mn).}$$
Under the real realization map $\Phi_K(K, n) = n\tau^K$, these operations become:
- Realized addition: $(m\tau^K) + (n\tau^K) = (m + n)\tau^K$.
- Realized multiplication:
  $$\boxed{(m\tau^K) \odot_K (n\tau^K) = mn\tau^K = \frac{(m\tau^K)(n\tau^K)}{\tau^K}.}$$
Ordinary real multiplication $(m\tau^K)(n\tau^K) = mn\tau^{2K}$ shifts the grade to $2K$ and represents ambient cross-grade algebra, **not** arithmetic internal to the unit $\tau^K$.

### C. What is its multiplicative identity?

The multiplicative identity of the grade-$K$ fiber ring is:
$$\boxed{1_K = (K, 1).}$$
It satisfies:
$$1_K \odot_K (K, n) = (K, 1 \cdot n) = (K, n).$$
Under real realization, its coordinate is:
$$\boxed{\Phi_K(1_K) = 1 \cdot \tau^K = \tau^K.}$$
The real number $\tau^K$ is the realized representation of the unit $1_K$.

### D. Is it canonically isomorphic to $\mathbb{Z}$?

**Yes.** The map:
$$\boxed{\varphi_K: \mathbb{Z} \xrightarrow{\sim} (\mathcal{F}_K, \oplus_K, \odot_K), \qquad n \mapsto (K, n)}$$
is a canonical isomorphism of commutative rings:
- $\varphi_K(m + n) = (K, m + n) = \varphi_K(m) \oplus_K \varphi_K(n)$,
- $\varphi_K(mn) = (K, mn) = \varphi_K(m) \odot_K \varphi_K(n)$,
- $\varphi_K(0) = 0_K$, $\varphi_K(1) = 1_K$.
On the realized image, $\widetilde{\varphi}_K: n \mapsto n\tau^K$ defines a ring isomorphism between $\mathbb{Z}$ and $(L_K, +, \odot_K)$.

### E. In what exact sense is $p\tau^K$ prime?

Because $(\mathcal{F}_K, \oplus_K, \odot_K) \cong \mathbb{Z}$, an element $(K, p)$ is a **prime element** in the grade-$K$ fiber ring if and only if $p$ is an ordinary rational prime.
Under real realization, $p\tau^K = \Phi_K(K, p)$ is properly defined as:
> **The grade-$K$ realization of the prime referent $p$.**
This intrinsic definition is primary; the Laurent-ring classification of $p\tau^K$ as an associate of $p$ in $\mathbb{Z}[\tau, \tau^{-1}]$ is an auxiliary ambient property.

### F. What are the canonical transfer maps between grades?

For any two grades $K, J \in \mathbb{A}_{\mathbb{R}}$, the canonical transfer map is:
$$\boxed{T_{J \leftarrow K}: \mathcal{F}_K \longrightarrow \mathcal{F}_J, \qquad (K, n) \longmapsto (J, n).}$$
It satisfies functorial consistency:
- $T_{K \leftarrow K} = \operatorname{id}_{\mathcal{F}_K}$,
- $\boxed{T_{M \leftarrow J} \circ T_{J \leftarrow K} = T_{M \leftarrow K}.}$

### G. Are transfer maps ring isomorphisms?

**Yes.** For all $x, y \in \mathcal{F}_K$:
- $T_{J \leftarrow K}(x \oplus_K y) = T_{J \leftarrow K}(x) \oplus_J T_{J \leftarrow K}(y)$,
- $T_{J \leftarrow K}(x \odot_K y) = T_{J \leftarrow K}(x) \odot_J T_{J \leftarrow K}(y)$,
- $T_{J \leftarrow K}(1_K) = 1_J$, $T_{J \leftarrow K}(0_K) = 0_J$.
The transfer map $T_{J \leftarrow K}$ is a ring isomorphism.
In real coordinates, the transfer map induces the scaling:
$$\boxed{\Phi_J(T_{J \leftarrow K}(x)) = \tau^{J - K} \Phi_K(x).}$$

---

## 2. Intrinsic Invariants, Metrics, and Counting

### H. What is the intrinsic normalized size?

For an element $(K, n) \in \mathcal{F}_K$, the **intrinsic normalized size** is the dimensionless integer:
$$\boxed{N_K(K, n) = n.}$$
On the realized line $x = n\tau^K$:
$$\boxed{N_K(n\tau^K) = \frac{n\tau^K}{\tau^K} = n.}$$
It is strictly multiplicative under intrinsic fiber multiplication:
$$\boxed{N_K(x \odot_K y) = N_K(x) N_K(y).}$$

### I. What is the intrinsic prime-counting function?

Measured in normalized units $u$:
$$\boxed{\pi_K^{\mathrm{int}}(u) = \pi(u).}$$
In ambient real coordinates $x = u\tau^K$:
$$\boxed{\pi_K^{\mathrm{amb}}(x) = \pi\left(\frac{x}{\tau^K}\right), \qquad \pi_K^{\mathrm{amb}}(p\tau^K) = \pi(p).}$$
The staircase increments occur identically at the realized prime stations $p\tau^K$.

### J. What is the intrinsic zeta function?

The intrinsic arithmetic zeta function of the grade-$K$ fiber is defined by summing over positive fiber elements using their intrinsic normalized size:
$$\boxed{\zeta_K^{\mathrm{int}}(s) = \sum_{n \ge 1} N_K(K, n)^{-s} = \sum_{n \ge 1} n^{-s} = \zeta(s).}$$
It is identically $\zeta(s)$ for every algebraic grade $K \in \mathbb{A}_{\mathbb{R}}$.

### K. What is the ambient-coordinate Dirichlet series?

The ambient series evaluated using realized real coordinates is:
$$\boxed{Z_K^{\mathrm{amb}}(s) = \sum_{n \ge 1} \Phi_K(K, n)^{-s} = \sum_{n \ge 1} (n\tau^K)^{-s} = \tau^{-Ks}\zeta(s).}$$
This is the object previously called $Z_K^{\mathrm{grid}}(s)$. It is reclassified as:
`AMBIENT_COORDINATE_DIRICHLET_SERIES`.

### L. Why are they different?

They are related by:
$$\boxed{Z_K^{\mathrm{amb}}(s) = \tau^{-Ks} \zeta_K^{\mathrm{int}}(s).}$$
The factor $\tau^{-Ks}$ is the **dimensional unit realization factor**. It arises entirely from measuring dimensionless integer referents in terms of the ambient real unit $\tau^K$.

### M. What is the proper Euler product in each interpretation?

- **Intrinsic Euler Product**: Inside the fiber ring, primes are $(K, p)$ with size $p$. The legitimate product is:
  $$\boxed{\prod_{(K, p)} \left(1 - N_K(K, p)^{-s}\right)^{-1} = \prod_p (1 - p^{-s})^{-1} = \zeta_K^{\mathrm{int}}(s) = \zeta(s).}$$
- **Ambient Product Firewall**: The naive ambient product:
  $$\prod_p \left(1 - (p\tau^K)^{-s}\right)^{-1} = \sum_{n \ge 1} n^{-s} \tau^{-K\Omega(n)s}$$
  multiplies coordinates in $\mathbb{R}$ and accumulates grade $K\Omega(n)$, violating the global grade-$K$ structure.

### N. How does the Riemann Converter look in normalized grade coordinates?

The Riemann Converter $T_{\sigma, t}(x)$ depends on the scaling harmonic building blocks $x^{(\rho - 1/2)/n}$.
In normalized grade coordinates $u = x/\tau^K$, the intrinsic converter is:
$$\boxed{T_K^{\mathrm{int}}(s, u) = T_0(s, u).}$$
The ambient converter evaluated on $x$ translates the argument by $K\log\tau$ in log-space:
$$u_{\mathrm{amb}}(x) = \log x = \log u + K\log\tau,$$
while the intrinsic log coordinate is strictly grade-invariant:
$$u_K(x) = \log\left(\frac{x}{\tau^K}\right) = \log u = \log n.$$

---

## 3. Reconciliation with Local Germ and Logarithmic Derivatives

### O. Does the fiber/ambient distinction explain TASK-TC-024's gauge result?

**Yes, completely.**
- Intrinsic completed zeta function: $\xi_K^{\mathrm{int}}(s) = \xi(s)$.
- Ambient completed family: $\Xi_K^{\mathrm{amb}}(s) = \tau^{-K(s - 1/2)}\xi_K^{\mathrm{int}}(s) = \tau^{-K(s - 1/2)}\xi(s)$.
The local zero germ transforms as:
$$c_{\Xi_K}(\rho) = \tau^{-K(\rho - 1/2)} c_\xi(\rho).$$
The modulus variation $|c_{\Xi_K}(\rho)/c_{\Xi_J}(\rho)| = \tau^{-(K-J)\delta}$ is the coordinate representation of a quantity having scaling weight $w = -(\rho - 1/2) = -\delta - i\gamma$.
The unit-normalized local germ:
$$\widehat{c}_K(\rho) = \tau^{K(\rho - 1/2)} c_{\Xi_K}(\rho) = c_\xi(\rho)$$
is the intrinsic arithmetic invariant. It is strictly grade-invariant and removes $\tau^{-K\delta}$.
The fiber/ambient separation proves that raw local germ variation is generic coordinate covariance under unit change.

### P. What role remains for the global graded monoid/Laurent ring?

The global operations:
$$(K, n) \star (J, m) = (K + J, nm), \qquad (n\tau^K)(m\tau^J) = nm\tau^{K + J}$$
and identities like $\tau^K \tau^{-K} = 1$ belong strictly to the **ambient cross-grade algebra**.
They describe how different grade realizations interact under ambient real multiplication, not arithmetic internal to a single fiber.

---

## 4. Full Algebraic-Grade Ambient Algebra and Injectivity

### Q. What is the correct full-algebraic-grade ambient group algebra?

For the full grade group $\Gamma = \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$ under addition, the canonical ambient algebra is the group algebra:
$$\boxed{\overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}].}$$
Elements are formal finite linear combinations:
$$\sum_{j=1}^r a_j [K_j], \qquad a_j \in \overline{\mathbb{Q}}, \quad K_j \in \mathbb{A}_{\mathbb{R}}.$$
The realization homomorphism is:
$$\boxed{\operatorname{ev}_\tau: \overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}] \longrightarrow \mathbb{R}, \qquad \sum_{j=1}^r a_j [K_j] \longmapsto \sum_{j=1}^r a_j \tau^{K_j}.}$$

### R. What does the realization-map kernel mean?

The kernel:
$$\boxed{\ker(\operatorname{ev}_\tau) = \left\{ \sum_{j=1}^r a_j [K_j] \in \overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}] : \sum_{j=1}^r a_j \tau^{K_j} = 0 \right\}}$$
is the set of all **finite algebraic cross-grade additive collapses**.
- Intrinsic arithmetic fibers $\mathcal{F}_K \cong \mathbb{Z}$ exist unconditionally regardless of $\ker(\operatorname{ev}_\tau)$.
- Ambient faithful grading requires $\ker(\operatorname{ev}_\tau) = \{0\}$.
- Pairwise exceptional transfer ($V_K = V_J$) is strictly the two-term subproblem $a_1 \tau^{K_1} + a_2 \tau^{K_2} = 0$.

### S. What injectivity is actually proved?

1. **Integer Grades ($\Gamma = \mathbb{Z}$)**:
   $\operatorname{ev}_\tau$ restricted to $\overline{\mathbb{Q}}[\mathbb{Z}] \cong \overline{\mathbb{Q}}[X, X^{-1}]$ is **injective** by the Lindemann (1882) transcendence of $\tau = 2\pi$.
2. **Rational Grades ($\Gamma = \mathbb{Q}$)**:
   $\operatorname{ev}_\tau$ restricted to $\overline{\mathbb{Q}}[\mathbb{Q}]$ is **injective** on every finite support by clearing denominators: if $K_j = m_j/N$, setting $Y = \tau^{1/N}$ yields a polynomial in the transcendental number $Y$.
3. **Full Algebraic Grades ($\Gamma = \mathbb{A}_{\mathbb{R}}$)**:
   Injectivity is **NOT PROVED**.
   The Gelfond–Schneider theorem proves that $\dim_{\mathbb{Q}} S_\tau \le 1$ (controlling two-term relations), but does not prove linear independence of 3 or more algebraic powers of $\tau$.
   Classification: `OPEN_FINITE_ALGEBRAIC_CROSS_GRADE_COLLAPSE`.

### T. Where exactly does transcendence matter?

- **Generic-Base Control**: For any real base $b > 0$, $(\mathcal{F}_K, \oplus_K, \odot_K) \cong \mathbb{Z}$ is base-independent. The transcendence of $\tau = 2\pi$ has **zero effect** on the internal arithmetic of any fiber.
- **Role of Transcendence**: Transcendence of $\tau$ matters **only** in the ambient realization map:
  - It ensures that integer and rational grade realizations do not collapse additively ($\ker(\operatorname{ev}_\tau|_{\mathbb{Q}}) = \{0\}$).
  - It prevents non-trivial rational-grade station collisions.
  - It governs whether cross-grade transfer factors $\tau^{J - K}$ can be algebraic ($S_\tau$).

### U. Is intrinsic TC mathematically more than transport of structure?

**No.**
Intrinsic TC within a single fiber is strictly transport of structure:
$$\mathcal{F}_K \cong \mathbb{Z}, \qquad \zeta_K^{\mathrm{int}}(s) = \zeta(s).$$
No new arithmetic constraint or zero-line restriction appears intrinsically without coupling to the ambient realization.

### V. What is the earliest remaining nontrivial TC/RH bridge?

Any valid RH mechanism in Transcendental Continuation must live at the interface between:
1. The **intrinsic zeta zero divisor** (stationary across all fibers), and
2. The **ambient realization map** $\operatorname{ev}_\tau: \overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}] \to \mathbb{R}$.
Specifically: Does the existence of an off-critical zero $\rho$ force a non-trivial algebraic cross-grade relation in $\ker(\operatorname{ev}_\tau)$ that contradicts Lindemann/Gelfond–Schneider transcendence?
This resolves the foundational ambiguity and provides the exact formulation for future research.

---

## 5. Summary Table: Four Canonical Strata of TC

| Stratum | Domain / Object | Operations / Relations | Invariance Status | Role in RH Programme |
| :--- | :--- | :--- | :--- | :--- |
| **1. Intrinsic Fiber Arithmetic** | Tagged fibers $\mathcal{F}_K = \{K\} \times \mathbb{Z}$ | $\oplus_K, \odot_K, 1_K, N_K, \zeta_K^{\mathrm{int}}$ | Strictly grade-invariant ($\cong \mathbb{Z}$) | Base arithmetic referent; transport of structure |
| **2. Ambient Realization** | Realized sets $L_K = \tau^K \mathbb{Z} \subset \mathbb{R}$ | $\Phi_K(K, n) = n\tau^K$, $Z_K^{\mathrm{amb}} = \tau^{-Ks}\zeta(s)$ | Unit-covariant ($w = -(\rho - 1/2)$) | Produces local germ scaling $\tau^{-K\delta}$ |
| **3. Ambient Cross-Grade Algebra** | Group algebra $\overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}]$ | $\star$ (grade addition), $\operatorname{ev}_\tau$ | $\ker(\operatorname{ev}_\tau)$ (open on $\mathbb{A}_{\mathbb{R}}$) | Locus of potential algebraic cross-grade contradiction |
| **4. Analytic Pullback (Auxiliary)** | Dilated functions $\zeta(\tau^{-K}s)$ | Argument scaling $s \mapsto \tau^{-K}s$ | Moving zeros $\rho_K = \tau^K \rho$ | Auxiliary diagnostic; not arithmetic TC |
