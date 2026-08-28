# Curvature-Transport Unification and Theta–Mellin Arithmetic Bridge Specification

**Document Identifier**: `CURVATURE_TRANSPORT.md`  
**Status**: Authoritative Research Specification & Unification Theorem  
**Mathematical Layer**: Transcendental Continuation, Radial Foliation, Fourier Geometry, Spectral Rigidity, Arithmetic Bridge  
**Epistemic Authority**: Proved Geometric & Spectral Invariants (`PROVED / EXACT / FORMALLY_PROVED`); Conditional Reader-Facing Rigidity Theorem; Canonical Open Obligation (`OBL-CT-001`).

---

## 1. Executive Summary & Central Objective

This document establishes the **Curvature-Transport Framework**, unifying 10 core geometric, spectral, and arithmetic constructions of `reimann_scope` as expressions of a single transported invariant:

1. **Circle Geometry**: Circumference $C_K = \tau^{1-K}$, radius $r_K = \tau^{-K}$, and Euclidean curvature $\kappa_K = \tau^K$;
2. **Grade Lattices**: Fundamental angular Fourier frequency lattices $L_K = \tau^K \mathbb{Z}$;
3. **Transcendental-Continuation Zero Worldlines**: $s_\rho(k) = \tau^k \rho$;
4. **Transported Radial Unit**: $r_K = \tau^{-K}$;
5. **Grade Character**: $q_\rho^K = \chi_\rho(K) = \tau^{K(\rho - 1/2)}$;
6. **Reflection-Pair Reciprocal Modes**: $|\chi_{\rho^\#}(K)| = |\chi_\rho(K)|^{-1}$;
7. **Exact $\cosh$ Grade Curvature**: $B_\rho(K) = 2(\cosh(K\delta\log\tau) - 1) = 4\sinh^2\left(\frac{K\delta\log\tau}{2}\right)$;
8. **Separated-Signal Curvature**: $\sum \delta_\rho^2$;
9. **Radial-Defect Quotient Curvature**: $\delta_\rho^2 / \gamma_\rho^2$;
10. **Half-Density Dilation & Theta–Mellin Scaling Law**: $(U_a f)(x) = a^{1/2}f(ax)$ with Mellin character $a^{1/2-s}$.

### The Proof Architecture & The Remaining Open Arrow

The overarching deductive skeleton is:

$$\boxed{
\text{Radial Geometry}
\implies
\text{Unitary Grade Character}
\implies
\text{Positive Reflection-Pair Curvature}
\overset{(\star)}{\implies}
\text{Arithmetic Curvature Identity}
\implies
\mathrm{RH}
}$$

> [!IMPORTANT]
> **Status of Arrow $(\star)$**: The first three steps and the final conditional implication are **EXACT, PROVED, AND FORMALLY VERIFIED IN LEAN 4**. Arrow $(\star)$ (the descent of arithmetic grade-flatness to the positive sum of zero orbit curvatures without cross-term cancellation) is **NOT ASSUMED**; it is rigorously audited and isolated as the repository's canonical open obligation: the **Arithmetic Curvature-Descent Theorem** (`OBL-CT-001`).

---

## 2. Conceptual Distinction Matrix

To preserve complete mathematical rigor, the following concepts are separated without identification:

| Concept | Mathematical Definition | Domain / Space | Role in Program |
|:---|:---|:---|:---|
| **Euclidean Circle Curvature** | $\kappa = 1/r$ | Differential geometry of circles in $\mathbb{R}^2$ | Reciprocal of radial radius $r_K = \tau^{-K}$. |
| **Fourier Frequency Scaling** | $\Delta\omega_K = \tau / C_K = \tau^K$ | Dual angular frequency space | Determines fundamental grade lattice $L_K = \tau^K\mathbb{Z}$. |
| **Conformal Coordinate Dilation** | $s_K = \tau^K s$, $z_K = \tau^K(s-1/2)$ | Complex coordinate plane $\mathbb{C}$ | Origin & centered coordinate dilations in TC. |
| **Half-Density Dilation Character** | $U_a(x^{-s}) = a^{1/2-s}x^{-s}$ | $L^2(\mathbb{R}_{>0}, dx) \to L^2(\mathbb{R}_{>0}, dx)$ | Unitary action whose unitary character axis is $\Re(s)=1/2$. |
| **Reflection-Pair Grade Curvature** | $B_\rho''(0) = 2\delta^2(\log\tau)^2$ | $C^\infty(\mathbb{R}_K \to \mathbb{R}_{\ge 0})$ | Non-negative second variation of reflection pair modulus sum. |
| **Algebraic Spectral Curvatures** | $\mathscr{K}_\tau(\rho) = \delta^2$, $C_\gamma = \sum \delta_{\gamma,a}^2$, $\kappa_1 = \delta^2/\gamma^2$ | Zero divisor $\mathcal{D}_\zeta$ data | Zero-rigidity detectors on candidate zero configurations. |
| **Arithmetic Curvature Functional** | $\mathscr{A}_\tau(\xi) = 0$ | Pure arithmetic space (primes, archimedean factors) | Divisor-independent arithmetic evaluator (OBL-CT-001). |

---

## 3. Exact Radial Geometry

Let $\tau = 2\pi$, and for each grade $K \in \mathbb{Z}$, define:
- Scale factor: $a_K = \tau^K$;
- Transported radial unit: $r_K = a_K^{-1} = \tau^{-K}$;
- Circle circumference: $C_K = \tau r_K = \tau^{1-K}$;
- Circle curvature: $\kappa_K = \frac{1}{r_K} = \tau^K$.

### Exact Identities & Shift Laws

1. **Reciprocity**:
   $$r_K \kappa_K = \tau^{-K} \cdot \tau^K = 1 \quad (\forall K \in \mathbb{Z})$$
2. **Unit Circumference at Grade $K=1$**:
   $$C_1 = \tau \cdot r_1 = \tau \cdot \tau^{-1} = 1, \qquad r_1 = \tau^{-1}, \qquad \kappa_1 = \tau$$
3. **Grade-Shift Transport Laws**:
   $$r_{K+1} = \tau^{-1}r_K, \qquad C_{K+1} = \tau^{-1}C_K, \qquad \kappa_{K+1} = \tau \kappa_K$$
4. **Angular Fourier Frequency Lattice**:
   For a circle of circumference $C_K$, the fundamental periodic boundary condition $f(\theta + C_K) = f(\theta)$ forces Fourier modes $e^{i \omega \theta}$ with $\omega C_K \in 2\pi \mathbb{Z} = \tau \mathbb{Z}$. Thus the dual frequency lattice is:
   $$\Delta\omega_K = \frac{\tau}{C_K} = \frac{\tau}{\tau^{1-K}} = \tau^K \implies L_K = \tau^K \mathbb{Z}$$

### Generic-Base Scale Control $b > 1$

For any real base $b > 1$:
$$a_{K,b} = b^K, \quad r_{K,b} = b^{-K}, \quad C_{K,b} = \tau b^{-K}, \quad \kappa_{K,b} = b^K \implies r_{K,b}\kappa_{K,b} = 1, \quad \frac{\tau}{C_{K,b}} = b^K$$
*Attribution*: Reciprocity, shift laws, and Fourier lattice spacing are generic positive-scale properties. The unit circumference $C_1 = 1$ is specific to choosing the scale generator $b = \tau = 2\pi$. The non-coincidence of lattices $L_K \cap L_L = \{0\}$ ($K \ne L$) relies on the transcendence of $\tau$.

---

## 4. Zero and Radial-Unit Transport

Let a nontrivial zero of $\zeta(s)$ be parameterized by $\rho = \frac{1}{2} + \delta + i\gamma$, with centered coordinate $z_\rho = \rho - \frac{1}{2} = \delta + i\gamma$.

At grade $K$, the centered grade coordinate is:
$$z_{\rho,K} = a_K z_\rho = \tau^K(\delta + i\gamma)$$
The real horizontal displacement at grade $K$ is:
$$d_{\rho,K} = \Re(z_{\rho,K}) = a_K \delta = \tau^K \delta$$

### Transport by the Radial Unit

Multiplying by the transported radial unit $r_K = \tau^{-K}$:
$$r_K z_{\rho,K} = \tau^{-K}(\tau^K z_\rho) = z_\rho$$
$$r_K d_{\rho,K} = \tau^{-K}(\tau^K \delta) = \delta$$
$$(r_K d_{\rho,K})^2 = \delta^2$$

> [!NOTE]
> The normalized radial coordinate $R_\tau(s, K) = \tau^{-K}\Re(s_K) - 1/2$ is **geometric multiplication by the transported radial unit $r_K$**, not merely an algebraic cancellation. A hypothetical off-line zero ($\delta \ne 0$) satisfies $(r_K d_{\rho,K})^2 = \delta^2$ at every grade.

---

## 5. Half-Density Dilation and the Critical Line

For any scale $a > 0$, define the dilation operator on $L^2(\mathbb{R}_{>0}, dx)$:
$$(U_a f)(x) = a^{1/2} f(ax)$$

### Exact $L^2$ Isometry

By substitution $y = ax$, $dx = a^{-1} dy$:
$$\|U_a f\|_2^2 = \int_0^\infty a |f(ax)|^2 dx = \int_0^\infty |f(y)|^2 dy = \|f\|_2^2$$
Thus $U_a$ is an exact unitary operator on $L^2(\mathbb{R}_{>0}, dx)$.

### Pointwise Mellin-Character Action

On the generalized power kernel $x^{-s}$:
$$(U_a(x^{-s}))(x) = a^{1/2} (ax)^{-s} = a^{1/2-s} x^{-s}$$
The scale eigenvalue factor is:
$$\lambda_a(s) = a^{1/2-s} = a^{1/2-\sigma} e^{-it\log a}$$

### The Critical Line as the Unitary Character Axis

For any $a \ne 1$ ($a > 0$):
$$|\lambda_a(s)| = |a^{1/2-s}| = a^{1/2-\Re(s)} = 1 \iff \frac{1}{2} - \Re(s) = 0 \iff \Re(s) = \frac{1}{2}$$

> [!IMPORTANT]
> The critical line $\Re(s) = 1/2$ is the **exact unitary-character axis of half-density dilation**. However, because $x^{-s} \notin L^2(\mathbb{R}_{>0})$, the zeros of an analytically continued Mellin transform are **not** eigenvalues of $U_a$ on $L^2$.

---

## 6. Grade Character and Reflection Curvature

Define the centered grade character for a complex zero $\rho = 1/2 + \delta + i\gamma$:
$$\chi_\rho(K) = a_K^{\rho - 1/2} = \tau^{K(\rho - 1/2)} = \tau^{K(\delta + i\gamma)} = e^{K\delta\log\tau} e^{iK\gamma\log\tau}$$
Its modulus is:
$$|\chi_\rho(K)| = e^{K\delta\log\tau}$$

### Reflection-Pair Reciprocal Modulus

Under Schwarz-reflection pairing $\rho^\# = 1 - \bar\rho = 1/2 - \delta + i\gamma$:
$$|\chi_{\rho^\#}(K)| = e^{K(-\delta)\log\tau} = e^{-K\delta\log\tau} = |\chi_\rho(K)|^{-1}$$
$$|\chi_\rho(K)| \cdot |\chi_{\rho^\#}(K)| = 1 \quad (\forall K \in \mathbb{R})$$

### Phase-Independent Reflection-Pair Defect

Define the reflection-pair defect functional:
$$B_\rho(K) = |\chi_\rho(K)| + |\chi_{\rho^\#}(K)| - 2 = e^{K\delta\log\tau} + e^{-K\delta\log\tau} - 2$$

### Exact $\cosh$ and $\sinh^2$ Representations

1. **Hyperbolic Cosine Form**:
   $$B_\rho(K) = 2(\cosh(K\delta\log\tau) - 1)$$
2. **Squared Hyperbolic Sine Form**:
   $$B_\rho(K) = 4\sinh^2\left(\frac{K\delta\log\tau}{2}\right)$$
3. **Non-Negativity**:
   $$B_\rho(K) \ge 0 \quad (\forall K, \delta \in \mathbb{R})$$
4. **Zero-Rigidity**:
   $$\text{For } K \ne 0: \quad B_\rho(K) = 0 \iff \delta = 0$$

### Native Grade Curvature & The Transported Invariant

Differentiating $B_\rho(K)$ with respect to grade $K$ at $K = 0$:
$$B_\rho'(K) = 2\delta\log\tau \sinh(K\delta\log\tau) \implies B_\rho'(0) = 0$$
$$B_\rho''(K) = 2\delta^2(\log\tau)^2 \cosh(K\delta\log\tau) \implies B_\rho''(0) = 2\delta^2(\log\tau)^2$$

Normalizing by the native scale factor $2(\log\tau)^2$:
$$\boxed{
\mathscr{K}_\tau(\rho) = \frac{B_\rho''(0)}{2(\log\tau)^2} = (r_K d_{\rho,K})^2 = \delta^2
}$$

---

## 7. Unification with Existing Repository Curvatures

The invariant $\mathscr{K}_\tau(\rho) = \delta^2$ reconciles all previously isolated curvature measures across the repository:

1. **Normalized Fibre Curvature**:
   $$C_\gamma = \sum_a \delta_{\gamma,a}^2 = \sum_a \mathscr{K}_\tau(\rho_{\gamma,a})$$
2. **Separated-Signal Curvature**:
   $$\left.\frac{\partial^2}{\partial x^2} M_K(x)\right|_{x=0} = 2 \sum_\gamma |a_K(\gamma)|^2 N_\gamma \sum_a \mathscr{K}_\tau(\rho_{\gamma,a})$$
3. **Radial-Defect Quotient Kernel**:
   $$\kappa_1(\rho, \rho^\#) = \frac{\delta_\rho^2}{\gamma_\rho^2} = \frac{\mathscr{K}_\tau(\rho)}{\gamma_\rho^2}$$
4. **Weighted Relative Spectral Trace**:
   $$T = \operatorname{Tr}\mathcal{R} = \sum_{\lambda\in\Lambda^+} \frac{\mathscr{K}_\tau(\lambda)}{\gamma_\lambda^2}$$

### Finite Positive-Weight Zero-Rigidity Theorem

For any finite zero family $\{\rho_j\}_{j=1}^N$ and strictly positive weights $w_j > 0$:
$$\mathscr{E} = \sum_{j=1}^N w_j \mathscr{K}_\tau(\rho_j) = \sum_{j=1}^N w_j \delta_j^2 \ge 0$$
$$\mathscr{E} = 0 \iff \forall j \in \{1, \dots, N\}, \; \delta_j = 0$$
*(Formally proved in Lean 4: `finite_positive_weight_curvature_rigidity`).*

---

## 8. Theta–Mellin Transport Derivation

For $a > 0$ and $t > 0$, define the scaled partial theta series:
$$\Theta_a^+(t) = \sum_{n=1}^\infty e^{-\pi (an)^2 t}$$

### Mellin Transform for $\Re(s) > 1$

For $\Re(s) > 1$, the integral and sum interchange absolutely:
$$\int_0^\infty \Theta_a^+(t) t^{s/2 - 1} dt = \sum_{n=1}^\infty \int_0^\infty e^{-\pi(an)^2 t} t^{s/2 - 1} dt$$

Substituting $u = \pi(an)^2 t \implies dt = \frac{du}{\pi(an)^2}$, $t^{s/2-1} = (\pi(an)^2)^{1-s/2} u^{s/2-1}$:
$$\int_0^\infty e^{-\pi(an)^2 t} t^{s/2-1} dt = (\pi(an)^2)^{-s/2} \int_0^\infty e^{-u} u^{s/2-1} du = a^{-s} \pi^{-s/2} \Gamma(s/2) n^{-s}$$

Summing over $n \ge 1$:
$$\int_0^\infty \Theta_a^+(t) t^{s/2-1} dt = a^{-s} \pi^{-s/2} \Gamma(s/2) \zeta(s) = a^{-s} \Lambda(s)$$

### Half-Density Normalization

Multiplying by $a^{1/2}$:
$$a^{1/2} \int_0^\infty \Theta_a^+(t) t^{s/2-1} dt = a^{1/2-s} \pi^{-s/2} \Gamma(s/2) \zeta(s) = a^{1/2-s} \Lambda(s)$$

For $a = \tau^K$:
$$\tau^{K/2} \int_0^\infty \Theta_{\tau^K}^+(t) t^{s/2-1} dt = \tau^{-K(s-1/2)} \Lambda(s) = \chi_s(K)^{-1} \Lambda(s)$$

### The Commutative Transport Chain

$$\begin{CD}
\text{Circle Radius } r_K = \tau^{-K} @>>> \text{Fourier Lattice } L_K = \tau^K\mathbb{Z} \\
@VVV @VVV \\
\text{Theta Scaling } \Theta_{\tau^K}^+(t) @>>> \text{Half-Density Mellin } \tau^{-K(s-1/2)}\Lambda(s) \\
@. @VVV \\
@. \text{Grade Character } \chi_s(K) = \tau^{K(s-1/2)}
\end{CD}$$

---

## 9. Arithmetic Curvature-Descent Audit

We audit four prospective candidate classes for constructing an arithmetic curvature bridge:

### Candidate CT-1: Scalar Theta–Mellin Transport
$$F_K(s) = \tau^{-K(s-1/2)} \Lambda(s)$$
At any zero $\rho$ of $\zeta(s)$ ($\Lambda(\rho) = 0$):
$$F_K(\rho) = \tau^{-K(\rho-1/2)} \cdot 0 = 0 \quad (\forall K \in \mathbb{R})$$
Differentiating with respect to $K$:
$$\frac{d^m}{dK^m} F_K(\rho) = (-\log\tau)^m (\rho - 1/2)^m \tau^{-K(\rho-1/2)} \Lambda(\rho) \equiv 0$$
*Conclusion*: Direct scalar differentiation at zeros vanishes identically ($0 \equiv 0$). It does not detect $\delta \ne 0$. Candidate CT-1 is classified as `GRADE_COORDINATE_REDUNDANT` / `FAIL_ARITHMETIC_FIREWALL`.

### Candidate CT-2: Derivatives Evaluated at Zeros
Expressions such as $\partial_s F_K(\rho) = \tau^{-K(\rho-1/2)}\Lambda'(\rho)$ expose $\chi_\rho(K)$, but require zero locations $\rho$ as inputs. By the **Strict Arithmetic Input Firewall**, direct zero evaluation is not an arithmetic construction. Classified as `FAIL_ARITHMETIC_FIREWALL`.

### Candidate CT-3: Unitary Plancherel Norm
The $L^2$ operator norm of $U_a$ is identically $1$ for all $a > 0$. Its spectral representation lives purely on the unitary axis $\Re(s) = 1/2$. Analytically continued zeros off this axis are not $L^2$ spectral data of $U_a$.

### Candidate CT-4: Hadamard / Determinant Curvature Descent
Evaluates whether a divisor-independent arithmetic functional $\mathscr{A}_\tau(\xi) = 0$ exists whose spectral expansion equals $\sum_\rho W_\rho \mathscr{K}_\tau(\rho)$. This requires proving non-cancellation of cross-terms, exact convergence, and remainder bounds.

---

## 10. Symmetry-Complete Polynomial Countermodel

To prove that circle geometry, functional reflection symmetry, coordinate covariance, and positive curvature detection alone do **not** force $\delta = 0$, we analyze the centered polynomial:
$$P_{\delta,\gamma}(z) = \left((z - i\gamma)^2 - \delta^2\right)\left((z + i\gamma)^2 - \delta^2\right) = (z^2 + \gamma^2 - \delta^2)^2 + 4\delta^2\gamma^2$$

### Verified Properties

1. **Even Symmetry**: $P_{\delta,\gamma}(-z) = P_{\delta,\gamma}(z)$ (formally proved in Lean 4: `countermodelPolynomial_even`);
2. **Schwarz Reflection**: $\overline{P_{\delta,\gamma}(\bar z)} = P_{\delta,\gamma}(z)$;
3. **Exact Zeros**: $\{\pm\delta \pm i\gamma\}$ (an off-line quartet for $\delta \ne 0$);
4. **Transported Radial Unit**: $r_K d_{\rho,K} = \tau^{-K}(\tau^K \delta) = \delta$;
5. **Reciprocal Grade Characters**: $|\chi_\rho(K)| \cdot |\chi_{\rho^\#}(K)| = 1$;
6. **Strictly Positive Grade Curvature**: $B_\rho''(0) = 2\delta^2(\log\tau)^2 > 0$ whenever $\delta \ne 0$.

> [!IMPORTANT]
> **Countermodel Significance**: $P_{\delta,\gamma}$ satisfies every geometric, reflection, and curvature-transport property, yet has $\delta \ne 0$. Therefore, **any valid proof of the Riemann Hypothesis via curvature transport must invoke arithmetic structure (the Euler product / prime distribution)** to force total curvature to vanish.

---

## 11. Reader-Facing Transcendental Curvature Rigidity Theorem

> ### **Theorem (Transcendental Curvature Rigidity — Conditional Schema)**
> Let the nontrivial zeros of $\zeta(s)$ be enumerated as $\rho_j = 1/2 + \delta_j + i\gamma_j$. Suppose there exists a divisor-independent arithmetic functional $\mathscr{A}_\tau(\xi)$ constructed from prime powers and archimedean factors such that:
>
> 1. **Arithmetic Vanishing**:
>    $$\mathscr{A}_\tau(\xi) = 0$$
> 2. **Curvature Spectral Expansion**:
>    $$\mathscr{A}_\tau(\xi) = \sum_{\rho\in\Lambda^+/\#} W_\rho \, \mathscr{K}_\tau(\rho)$$
>    under an absolutely convergent sum with strictly positive weights $W_\rho > 0$, where
>    $$\mathscr{K}_\tau(\rho) = \frac{1}{2(\log\tau)^2} \left.\frac{d^2}{dK^2} \left(|\tau^{K(\rho-1/2)}| + |\tau^{K(\rho^\#-1/2)}| - 2\right)\right|_{K=0} = \left(\Re\rho - \frac{1}{2}\right)^2 = \delta_\rho^2$$
>
> **Then** every nontrivial zero satisfies $\Re\rho = 1/2$ ($\delta_\rho = 0$), establishing the Riemann Hypothesis.

*Proof Schema*:
$$0 = \mathscr{A}_\tau(\xi) = \sum_{\rho\in\Lambda^+/\#} W_\rho \delta_\rho^2 \overset{W_\rho > 0, \, \delta_\rho^2 \ge 0}{\implies} \forall \rho, \; \delta_\rho = 0 \iff \Re\rho = \frac{1}{2}.$$
*(Formally proved in Lean 4: `ConditionalCurvatureRigidityBridge.all_defects_zero`).*

---

## 12. Canonical Open Obligation: Arithmetic Curvature-Descent Theorem

Because no divisor-independent arithmetic functional $\mathscr{A}_\tau(\xi)$ has yet been proved to satisfy both $\mathscr{A}_\tau = 0$ and $\mathscr{A}_\tau = \sum W_\rho \delta_\rho^2$, the program's earliest open barrier is recorded as:

$$\boxed{
\textbf{OBL-CT-001: Arithmetic Curvature-Descent Theorem}
}$$

### Exact Quantified Requirements for OBL-CT-001

A valid resolution must construct a functional $\mathscr{A}_\tau$ satisfying:
1. **Zero-Independent Arithmetic Input**: Evaluated solely from primes $\Lambda(n)$, powers $n^{-\sigma}$, and Gamma factors without referencing zero locations $\rho$;
2. **Convergence Domain**: Explicit domain of absolute convergence;
3. **Regularization & Boundary Control**: Certified regularization removing archimedean/pole divergences;
4. **Spectral Expansion**: Proved meromorphic/contour expansion yielding $\sum_{\rho} W_\rho \delta_\rho^2$;
5. **Strict Weight Positivity**: $W_\rho > 0$ for all represented zero orbits;
6. **Involution Pair Isolation**: No unconstrained cross-terms $(\rho_1, \rho_2)$ that fail to cancel;
7. **Limit Order Independence**: Independence from truncation order;
8. **Positivity Firewall**: Preservation of strict positivity under all limits.

### Relationship to CMSA Gate G4

- **Gate G4 Status**: CMSA Gate G4 analyzes translation-average mean-square variations $V_T = \frac{1}{2T}\|\Delta_{H(T)}\|^2 - C_T$. For fixed finite off-line zero configurations, $\Delta(t) \in L^2(\mathbb{R})$, so $\|\Delta\|_{L^2(-T,T)} = \mathcal{O}(1) = o(\sqrt{T})$, rendering $V_T \to 0$ invisible.
- **Curvature Transport Supercedence**: Curvature Transport evaluates the native second grade variation $B_\rho''(0) = 2\delta^2(\log\tau)^2$. Because $B_\rho''(0)$ is non-zero for *any* off-line quartet (including a single finite quartet), Curvature Transport operates at the orbit/divisor level and **supersedes the raw CMSA $1/(2T)$ activation problem**.

---

## 13. Formalization and Verification Inventory

### Lean 4 Compiled Declarations (`RiemannScope.CurvatureTransport`)

| Declaration | Mathematical Content | Epistemic Status |
|:---|:---|:---|
| `radial_unit_curvature_reciprocal` | $r_K \kappa_K = \tau^{-K} \tau^K = 1$ | FORMALLY_PROVED |
| `grade_shift_radius` | $r_{K+1} = \tau^{-1} r_K$ | FORMALLY_PROVED |
| `grade_shift_circumference` | $C_{K+1} = \tau^{-1} C_K$ | FORMALLY_PROVED |
| `grade_shift_curvature` | $\kappa_{K+1} = \tau \kappa_K$ | FORMALLY_PROVED |
| `unit_circumference_K1` | $C_1 = \tau r_1 = 1$ | FORMALLY_PROVED |
| `fourier_lattice_spacing_eq` | $\Delta\omega_K = \tau / C_K = \tau^K$ | FORMALLY_PROVED |
| `centered_radial_unit_transport` | $r_K d_{\rho,K} = \delta$ | FORMALLY_PROVED |
| `transported_squared_defect_invariance` | $(r_K d_{\rho,K})^2 = \delta^2$ | FORMALLY_PROVED |
| `generic_scale_radial_unit_transport` | $b^{-K}(b^K \delta) = \delta$ for generic $b > 0$ | FORMALLY_PROVED |
| `grade_character_complex_product` | $(\delta+i\gamma)\log\tau K = K\delta\log\tau + i K\gamma\log\tau$ | FORMALLY_PROVED |
| `grade_character_modulus_def` | $\|\chi_\rho(K)\| = \exp(K\delta\log\tau)$ | FORMALLY_PROVED |
| `reflection_reciprocal_modulus_prod` | $\|\chi_\rho(K)\| \|\chi_{\rho^\#}(K)\| = 1$ | FORMALLY_PROVED |
| `reflection_pair_defect_cosh` | $B_\rho(K) = 2(\cosh(u)-1)$ | FORMALLY_PROVED |
| `reflection_pair_defect_nonneg` | $B_\rho(K) \ge 0$ | FORMALLY_PROVED |
| `reflection_pair_defect_eq_zero_iff` | $B_\rho(K) = 0 \iff \delta = 0$ for $K \ne 0, \tau > 1$ | FORMALLY_PROVED |
| `native_grade_second_order_taylor_coefficient` | $B''(0)/(2(\log\tau)^2) = \delta^2$ | FORMALLY_PROVED |
| `finite_positive_weight_curvature_rigidity` | $\sum w_j \delta_j^2 = 0 \iff \forall j, \delta_j = 0$ | FORMALLY_PROVED |
| `countermodelPolynomial` | Definition of $P_{\delta,\gamma}(z)$ | DEFINITION |
| `countermodelPolynomial_even` | $P_{\delta,\gamma}(-z) = P_{\delta,\gamma}(z)$ | FORMALLY_PROVED |
| `ConditionalCurvatureRigidityBridge.all_defects_zero` | Conditional Curvature Rigidity Theorem | FORMALLY_PROVED |

### Python Test Suite (`tests/test_curvature_transport.py`)

- `TestRadialGeometryAndLattice`: 25 parameter points testing shift laws, $C_1 = 1$, Fourier spacing, and generic scale base $b \in \{1.5, 2.0, 3.14, 10.0\}$.
- `TestZeroAndRadialUnitTransport`: 24 parameter points testing zero recovery and reciprocal grade character modes.
- `TestReflectionPairCurvature`: 10 parameter points testing $\cosh/\sinh$ equivalence, zero-rigidity, and numerical second derivative convergence to $2\delta^2(\log\tau)^2$.
- `TestThetaMellinAndFalsificationControls`: 24 parameter points testing half-density Mellin scaling, scalar zero multiplication vanishing obstruction, and polynomial countermodel symmetries.
- **Total Suite Result**: 83/83 passed in 2.72s.
