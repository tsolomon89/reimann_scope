# Curvature-Transport Unification and Theta–Mellin Arithmetic Bridge Specification

**Document Identifier**: `CURVATURE_TRANSPORT.md`  
**Status**: Authoritative Research Specification & Unification Theorem  
**Mathematical Layer**: Transcendental Continuation, Radial Foliation, Fourier Geometry, Spectral Rigidity, Arithmetic Bridge  
**Epistemic Authority**: Proved Geometric & Spectral Invariants (`PROVED / EXACT / FORMALLY_PROVED`); Conditional Reader-Facing Rigidity Theorem; Canonical Open Obligation (`OBL-CT-001A`).

---

## 1. Executive Summary & Central Objective

This document establishes the **Curvature-Transport Framework**, unifying 10 core geometric, spectral, and arithmetic constructions of `reimann_scope` as expressions of a single transported invariant:

1. **Circle Geometry**: Circumference $C_K = \tau^{1-K}$, radius $r_K = \tau^{-K}$, and Euclidean curvature $\kappa_K = \tau^K$ for integer grade checkpoints $K \in \mathbb{Z}$;
2. **Grade Lattices**: Fundamental angular Fourier frequency lattices $L_K = \tau^K \mathbb{Z}$;
3. **Transcendental-Continuation Zero Worldlines**: $s_\rho(k) = \tau^k \rho$ for continuous grade $k \in \mathbb{R}$;
4. **Transported Radial Unit**: $r_K = \tau^{-K}$;
5. **Continuous Grade Character**: $\chi_\rho(k) = \tau^{k(\rho - 1/2)}$;
6. **Reflection-Pair Reciprocal Modes**: $|\chi_{\rho^\#}(k)| = |\chi_\rho(k)|^{-1}$;
7. **Exact $\cosh$ Grade Curvature**: $B_\rho(k) = 2(\cosh(k\delta\log\tau) - 1) = 4\sinh^2\left(\frac{k\delta\log\tau}{2}\right)$;
8. **Separated-Signal Curvature**: $\sum \delta_\rho^2$;
9. **Radial-Defect Quotient Curvature**: $\delta_\rho^2 / \gamma_\rho^2$;
10. **Half-Density Dilation & Theta–Mellin Scaling Law**: $(U_a f)(x) = a^{1/2}f(ax)$ with Mellin character $a^{1/2-s}$.

### The Proof Architecture & The Central Open Question

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
> **Central Mathematical Investigation of Arrow $(\star)$**:
> $$\boxed{
> \text{Does any coherent non-scalar arithmetic curvature functional exist?}
> }$$
> The first three steps and the final conditional implication are **EXACT, PROVED, AND FORMALLY VERIFIED IN LEAN 4**. Arrow $(\star)$ (the descent of arithmetic grade-flatness to the positive sum of zero orbit curvatures without cross-term cancellation) is **NOT ASSUMED**; it is rigorously audited and isolated as the repository's canonical earliest open obligation: the **Non-Scalar Arithmetic Functional Construction** (`OBL-CT-001A`).

---

## 2. Conceptual Distinction Matrix

To preserve complete mathematical rigor, the following concepts are separated without identification:

| Concept | Mathematical Definition | Domain / Space | Role in Program |
|:---|:---|:---|:---|
| **Euclidean Circle Curvature** | $\kappa_K = 1/r_K = \tau^K$ | Discrete circle geometry ($K \in \mathbb{Z}$) | Reciprocal of radial radius $r_K = \tau^{-K}$. |
| **Fourier Frequency Scaling** | $\Delta\omega_K = \tau / C_K = \tau^K$ | Dual angular frequency space | Determines fundamental grade lattice $L_K = \tau^K\mathbb{Z}$. |
| **Continuous Coordinate Dilation** | $s_k = \tau^k s$, $z_k = \tau^k(s-1/2)$ | Complex plane $\mathbb{C}$ ($k \in \mathbb{R}$) | Origin & centered coordinate dilations in TC. |
| **Half-Density Dilation Character** | $U_a(x^{-s}) = a^{1/2-s}x^{-s}$ | $L^2(\mathbb{R}_{>0}, dx) \to L^2(\mathbb{R}_{>0}, dx)$ | Unitary action whose unitary character axis is $\Re(s)=1/2$. |
| **Continuous Reflection Curvature** | $B_\rho''(0) = \left.\frac{d^2}{dk^2} B_\rho(k)\right|_{k=0} = 2\delta^2(\log\tau)^2$ | $C^\infty(\mathbb{R}_k \to \mathbb{R}_{\ge 0})$ | Non-negative second variation of reflection pair modulus sum. |
| **Algebraic Spectral Curvatures** | $\mathscr{K}_\tau(\rho) = \delta^2$, $C_\gamma = \sum \delta_{\gamma,a}^2$, $\kappa_1 = \delta^2/\gamma^2$ | Zero divisor $\mathcal{D}_\zeta$ data | Zero-rigidity detectors on candidate zero configurations. |
| **Arithmetic Curvature Functional** | $\mathscr{A}_\tau(\xi) = 0$ | Pure arithmetic space (primes, archimedean factors) | Divisor-independent arithmetic evaluator (OBL-CT-001A). |

---

## 3. Exact Radial Geometry and Lattice Scaling

Let $\tau = 2\pi$. We distinguish:
- **Continuous grade parameter** $k \in \mathbb{R}$ for continuous scaling, differentiation, and curvature;
- **Discrete integer grade checkpoints** $K \in \mathbb{Z}$ for bilateral checkpoint lattices and ray sampling.

For each integer grade $K \in \mathbb{Z}$, define:
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

At continuous grade $k \in \mathbb{R}$, the centered grade coordinate is:
$$z_{\rho}(k) = \tau^k z_\rho = \tau^k(\delta + i\gamma)$$
The real horizontal displacement at grade $k$ is:
$$d_{\rho}(k) = \Re(z_{\rho}(k)) = \tau^k \delta$$

### Transport by the Radial Unit

Multiplying by the transported radial unit $r(k) = \tau^{-k}$:
$$r(k) z_{\rho}(k) = \tau^{-k}(\tau^k z_\rho) = z_\rho$$
$$r(k) d_{\rho}(k) = \tau^{-k}(\tau^k \delta) = \delta$$
$$(r(k) d_{\rho}(k))^2 = \delta^2$$

> [!NOTE]
> The normalized radial coordinate $R_\tau(s, k) = \tau^{-k}\Re(s_k) - 1/2$ is **geometric multiplication by the transported radial unit $r(k)$**, not merely an algebraic cancellation. A hypothetical off-line zero ($\delta \ne 0$) satisfies $(r(k) d_{\rho}(k))^2 = \delta^2$ at every grade.

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

## 6. Continuous Grade Character and Reflection Curvature

Define the centered grade character for a complex zero $\rho = 1/2 + \delta + i\gamma$ and continuous grade $k \in \mathbb{R}$:
$$\chi_\rho(k) = \tau^{k(\rho - 1/2)} = \tau^{k(\delta + i\gamma)} = e^{k\delta\log\tau} e^{ik\gamma\log\tau}$$
Its modulus is:
$$|\chi_\rho(k)| = e^{k\delta\log\tau}$$

### Reflection-Pair Reciprocal Modulus

Under Schwarz-reflection pairing $\rho^\# = 1 - \bar\rho = 1/2 - \delta + i\gamma$:
$$|\chi_{\rho^\#}(k)| = e^{k(-\delta)\log\tau} = e^{-k\delta\log\tau} = |\chi_\rho(k)|^{-1}$$
$$|\chi_\rho(k)| \cdot |\chi_{\rho^\#}(k)| = 1 \quad (\forall k \in \mathbb{R})$$

### Phase-Independent Reflection-Pair Defect

Define the reflection-pair defect functional for continuous grade $k \in \mathbb{R}$:
$$B_\rho(k) = |\chi_\rho(k)| + |\chi_{\rho^\#}(k)| - 2 = e^{k\delta\log\tau} + e^{-k\delta\log\tau} - 2$$

### Exact $\cosh$ and $\sinh^2$ Representations

1. **Hyperbolic Cosine Form**:
   $$B_\rho(k) = 2(\cosh(k\delta\log\tau) - 1)$$
2. **Squared Hyperbolic Sine Form**:
   $$B_\rho(k) = 4\sinh^2\left(\frac{k\delta\log\tau}{2}\right)$$
3. **Non-Negativity**:
   $$B_\rho(k) \ge 0 \quad (\forall k, \delta \in \mathbb{R})$$
4. **Zero-Rigidity**:
   $$\text{For } k \ne 0: \quad B_\rho(k) = 0 \iff \delta = 0$$

### Continuous Grade Curvature & The Transported Invariant

Differentiating $B_\rho(k)$ with respect to continuous grade $k$ at $k = 0$:
$$B_\rho'(k) = \frac{d}{dk} B_\rho(k) = 2\delta\log\tau \sinh(k\delta\log\tau) \implies B_\rho'(0) = 0$$
$$B_\rho''(k) = \frac{d^2}{dk^2} B_\rho(k) = 2\delta^2(\log\tau)^2 \cosh(k\delta\log\tau) \implies B_\rho''(0) = 2\delta^2(\log\tau)^2$$

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

## 8. Complete Theta–Mellin Proof and Interchange Justification

For $a > 0$ and $t > 0$, define the scaled partial theta series:
$$\Theta_a^+(t) = \sum_{n=1}^\infty e^{-\pi (an)^2 t}$$
Let $s = \sigma + i\eta \in \mathbb{C}$ with $\sigma = \Re(s) > 1$.

### Step 1: Explicit Absolute Convergence and Fubini/Tonelli Justification

We evaluate the double integral/sum of absolute values on $\mathbb{R}_{>0} \times \mathbb{N}_{\ge 1}$:
$$\sum_{n=1}^\infty \int_0^\infty \left| e^{-\pi a^2 n^2 t} t^{s/2 - 1} \right| dt = \sum_{n=1}^\infty \int_0^\infty e^{-\pi a^2 n^2 t} t^{\sigma/2 - 1} dt$$
Applying the real substitution $u = \pi a^2 n^2 t \implies dt = \frac{du}{\pi a^2 n^2}$:
$$\int_0^\infty e^{-\pi a^2 n^2 t} t^{\sigma/2 - 1} dt = (\pi a^2 n^2)^{-\sigma/2} \int_0^\infty e^{-u} u^{\sigma/2 - 1} du = a^{-\sigma} \pi^{-\sigma/2} \Gamma(\sigma/2) n^{-\sigma}$$
Summing over $n \ge 1$:
$$\sum_{n=1}^\infty \int_0^\infty \left| e^{-\pi a^2 n^2 t} t^{s/2 - 1} \right| dt = a^{-\sigma} \pi^{-\sigma/2} \Gamma(\sigma/2) \sum_{n=1}^\infty n^{-\sigma} = a^{-\sigma} \pi^{-\sigma/2} \Gamma(\sigma/2) \zeta(\sigma) < \infty$$
Since $\sigma > 1$, $\zeta(\sigma) < \infty$ and $\Gamma(\sigma/2) < \infty$. By **Tonelli's Theorem**, the integrand is in $L^1(\mathbb{R}_{>0} \times \mathbb{N}, dt \otimes d\mu)$, which rigorously justifies the interchange of summation and integration via **Fubini's Theorem**.

### Step 2: Complex Mellin Transform for $\Re(s) > 1$

By Fubini interchange:
$$\int_0^\infty \Theta_a^+(t) t^{s/2 - 1} dt = \sum_{n=1}^\infty \int_0^\infty e^{-\pi a^2 n^2 t} t^{s/2 - 1} dt = \sum_{n=1}^\infty a^{-s} \pi^{-s/2} \Gamma(s/2) n^{-s} = a^{-s} \pi^{-s/2} \Gamma(s/2) \zeta(s) = a^{-s} \Lambda(s)$$

### Step 3: Half-Density Dilation Identity

Multiplying by $a^{1/2}$:
$$a^{1/2} \int_0^\infty \Theta_a^+(t) t^{s/2 - 1} dt = a^{1/2-s} \pi^{-s/2} \Gamma(s/2) \zeta(s) = a^{1/2-s} \Lambda(s)$$
For $a = \tau^k$ ($k \in \mathbb{R}$):
$$\tau^{k/2} \int_0^\infty \Theta_{\tau^k}^+(t) t^{s/2 - 1} dt = \tau^{-k(s-1/2)} \Lambda(s) = \chi_s(k)^{-1} \Lambda(s)$$

### Step 4: Scaled Jacobi Theta and Poisson Summation

Let $\theta(t) = \sum_{n\in\mathbb{Z}} e^{-\pi n^2 t} = 1 + 2\Theta_1^+(t)$.
By Poisson summation on $f_t(x) = e^{-\pi x^2 t}$ with Fourier transform $\hat{f}_t(\xi) = \frac{1}{\sqrt{t}}e^{-\pi \xi^2 / t}$:
$$\theta(t) = \frac{1}{\sqrt{t}} \theta\left(\frac{1}{t}\right)$$
For dilation parameter $a > 0$, evaluating along lattice $a\mathbb{Z}$ gives the scaled transformation:
$$\theta(a^2 t) = \frac{1}{a\sqrt{t}} \theta\left(\frac{1}{a^2 t}\right)$$
Expressed in terms of the partial series $\Theta_a^+(t) = \frac{\theta(a^2 t) - 1}{2}$:
$$\Theta_a^+(t) = \frac{1}{a\sqrt{t}} \Theta_1^+\left(\frac{1}{a^2 t}\right) + \frac{1}{2a\sqrt{t}} - \frac{1}{2}$$

### Domain, Branch, and Tail Bound Specifications

- **Branch Convention**: $t^{s/2-1} = \exp((s/2 - 1)\log t)$ with principal real branch $\log t \in \mathbb{R}$ for $t > 0$.
- **Boundary Behavior**: At $t \to 0^+$, $\Theta_a^+(t) \sim \frac{1}{2a\sqrt{t}}$, so $\Theta_a^+(t) t^{\sigma/2-1} \sim \frac{1}{2a} t^{\sigma/2 - 3/2}$, integrable at $0$ iff $\sigma/2 - 3/2 > -1 \iff \sigma > 1$. At $t \to \infty$, $\Theta_a^+(t) = \mathcal{O}(e^{-\pi a^2 t})$.
- **No Analytic Smuggling**: The unregularized Mellin integral is **strictly restricted to $\Re(s) > 1$** and is never evaluated directly inside the critical strip without meromorphic regularization.
- **Explicit Dirichlet Tail Bounds**:
  - Unnormalized Tail Bound:
    $$\text{Tail}_{\text{unnorm}}(\sigma, N) = a^{-\sigma}\pi^{-\sigma/2}|\Gamma(s/2)|\frac{N^{1-\sigma}}{\sigma-1}$$
  - Half-Density Tail Bound:
    $$\text{Tail}_{\text{half-density}}(\sigma, N) = a^{1/2-\sigma}\pi^{-\sigma/2}|\Gamma(s/2)|\frac{N^{1-\sigma}}{\sigma-1}$$

---

## 9. Scalar-Transport No-Go Theorem

Let $L(s)$ be independent of grade and define the scalar-transported family:
$$F(k, s) = g(k, s) L(s)$$
where $g(k, s)$ is sufficiently differentiable in $k \in \mathbb{R}$.

> ### **Theorem (Scalar-Transport No-Go Theorem)**
> 1. **Derivative Vanishing at Zeros**: If $L(\rho) = 0$, then for every derivative order $m \ge 0$:
>    $$\left.\frac{\partial^m}{\partial k^m} F(k, \rho)\right|_{k=0} = \left.\frac{\partial^m g(k, \rho)}{\partial k^m}\right|_{k=0} \cdot L(\rho) = 0 \equiv 0$$
> 2. **Zero-Divisor Preservation**: If $g(k, s) \ne 0$ on domain $\Omega$, then:
>    $$F(k, s) = 0 \iff L(s) = 0$$
>    Multiplication by $g$ preserves all root locations and multiplicities without modification.
> 3. **Logarithmic Derivative Anomaly-Free Decomposition**: On any domain where $g(k, s) L(s) \ne 0$:
>    $$\partial_s \log F(k, s) = \partial_s \log L(s) + \partial_s \log g(k, s)$$
>    For $g(k, s) = \tau^{-k(s-1/2)}$, $\partial_s \log g = -k\log\tau$. The grade correction is purely coordinate/archimedean and supplies zero spectral divisor data.
> 4. **Transported Zero Worldline Pullback**: Along the zero worldline $s(k) = 1/2 + \tau^k(\rho - 1/2)$, the pullback $F_k(s(k)) = L(\rho) = 0$ vanishes identically, and directional derivatives along the worldline vanish identically.

### Candidate Classifications

- **Candidate CT-1 (Scalar Theta–Mellin Transport)**: $F_k(s) = \tau^{-k(s-1/2)}\Lambda(s)$. Evaluates scalar multiplication. Classified as `GRADE_COORDINATE_REDUNDANT`.
- **Candidate CT-2 (Direct Zero Evaluation / Differentiation)**: Evaluating $\partial_s F_k(\rho) = \tau^{-k(\rho-1/2)}\Lambda'(\rho)$ requires zero locations $\rho$ as inputs, violating the Strict Arithmetic Input Firewall. Classified as `FAIL_ARITHMETIC_FIREWALL`.

---

## 10. Minimum Structure for Curvature Descent

The target quadratic defect
$$\delta_\rho^2 = \left(\Re\rho - \frac{1}{2}\right)^2$$
is non-holomorphic as a 1-point function of $\rho$.

> ### **Theorem (Scoped One-Point Holomorphic Obstruction)**
> No fixed holomorphic local kernel $H(z)$ can equal $(\Re z)^2$ on an open set in $\mathbb{C}$.
> *Proof*:
> For $z = x + iy$, $(\Re z)^2 = x^2$.
> Evaluating the Cauchy-Riemann Wirtinger derivative:
> $$\frac{\partial}{\partial \bar z} (x^2) = \frac{1}{2}\left(\frac{\partial}{\partial x} + i\frac{\partial}{\partial y}\right) x^2 = \frac{1}{2}(2x) = x = \Re z = \delta$$
> For any off-line point ($\delta \ne 0$), $\frac{\partial}{\partial \bar z} (x^2) \ne 0$, violating the Cauchy-Riemann equations.

*Consequence*: Direct linear 1-point holomorphic explicit formula test functions cannot produce $\delta_\rho^2$. Any valid non-scalar arithmetic curvature functional must employ at least one of:
1. A two-slot or sesquilinear pairing kernel;
2. A contour boundary / noncommutation term;
3. A Hadamard / Fredholm determinant regularization;
4. A noncommuting completion anomaly.

---

## 11. Curvature Transport versus CMSA Gate G4

| Dimension | Curvature Transport | CMSA Gate G4 |
|:---|:---|:---|
| **Primary Mathematical Target** | $\mathscr{K}_\tau(\rho) = B_\rho''(0)/(2(\log\tau)^2) = \delta^2$ | $V_T = \frac{1}{2T}\|\Delta_{H(T)}\|^2 - C_T$ |
| **Spectral Detector Level** | Native 2nd grade variation $B_\rho''(0) = 2\delta^2(\log\tau)^2$ | Translation-average mean square on $\mathbb{R}$ |
| **Fixed Finite Perturbation Status** | Non-zero ($B_\rho''(0) > 0$) for any finite off-line quartet | Invisible ($V_T \to 0$) due to $\Delta \in L^2(\mathbb{R})$ ($o(\sqrt{T})$) |
| **Arithmetic Input** | Requires non-scalar functional $\mathscr{A}_\tau(\xi)$ | Arithmetic completed log-derivative $A(u)$ |
| **Diagonal vs Off-Diagonal** | Requires reflection-pair isolation | Bilinear $J_T, K_T$ cross-term kernel integration |
| **Infinite Limit Barrier** | Summability of $\sum W_\rho \delta_\rho^2$ | Growing perturbation schedule $H(T) = cT$ |
| **Positivity Target** | Weight positivity $W_\rho > 0$ | Direct energy vs cross-term $E_T - C_T > 0$ |
| **Current Epistemic Status** | Bypasses detector-level invisibility; arithmetic functional OPEN (`OBL-CT-001A`) | Gate G4 OPEN (`OBL-CMSA-003-G4-COFINAL-ESTIMATE`) |

> [!IMPORTANT]
> Curvature Transport operates at the orbit/divisor level and **bypasses fixed-finite $L^2$ translation invisibility at the spectral detector level**. However, Curvature Transport **does not solve CMSA Gate G4**. Whether a non-scalar arithmetic curvature functional avoids or reproduces the CMSA pair-isolation/infinite-limit barrier remains an open research problem.

---

## 12. Symmetry-Complete Polynomial Countermodel

To prove that circle geometry, functional reflection symmetry, coordinate covariance, and positive curvature detection alone do **not** force $\delta = 0$, we analyze the centered polynomial:
$$P_{\delta,\gamma}(z) = \left((z - i\gamma)^2 - \delta^2\right)\left((z + i\gamma)^2 - \delta^2\right) = (z^2 + \gamma^2 - \delta^2)^2 + 4\delta^2\gamma^2$$

### Verified Properties

1. **Even Symmetry**: $P_{\delta,\gamma}(-z) = P_{\delta,\gamma}(z)$ (formally proved in Lean 4: `countermodelPolynomial_even`);
2. **Schwarz Reflection**: $\overline{P_{\delta,\gamma}(\bar z)} = P_{\delta,\gamma}(z)$ (`PROVED / EXACT / PARTIALLY_FORMALIZED`);
3. **Exact Zeros**: Four roots $\{\pm\delta \pm i\gamma\}$ (formally proved in Lean 4: `countermodelPolynomial_root_pos_pos`, `countermodelPolynomial_root_neg_pos`, `countermodelPolynomial_root_pos_neg`, `countermodelPolynomial_root_neg_neg`);
4. **Transported Radial Unit**: $r(k) d_\rho(k) = \tau^{-k}(\tau^k \delta) = \delta$;
5. **Reciprocal Grade Characters**: $|\chi_\rho(k)| \cdot |\chi_{\rho^\#}(k)| = 1$;
6. **Strictly Positive Grade Curvature**: $B_\rho''(0) = 2\delta^2(\log\tau)^2 > 0$ for $\delta \ne 0, \tau > 1$ (formally proved in Lean 4: `reflection_grade_curvature_pos`).

---

## 13. Geometric Involution Discrepancy ($J$ versus $C$)

Let $Z$ denote the multiset of nontrivial zeros of $\zeta(s)$ counted with multiplicity. For any $\rho = \beta + i\gamma = 1/2 + \delta + i\gamma \in Z$:

Define the two fundamental zero involutions:
1. **Functional Reflection Involution**:
   $$J(\rho) = 1 - \rho = \frac{1}{2} - \delta - i\gamma$$
2. **Complex Conjugation Involution**:
   $$C(\rho) = \bar\rho = \frac{1}{2} + \delta - i\gamma$$

### Exact Involution Difference and Squared Discrepancy
$$\boxed{
J(\rho) - C(\rho) = (1 - \rho) - \bar\rho = 1 - 2\Re(\rho) = - 2\delta_\rho
}$$
$$(Formally proved in Lean 4: `weil_involution_difference`).$$

Taking the squared complex modulus yields:
$$\boxed{
|J(\rho) - C(\rho)|^2 = |-2\delta_\rho|^2 = 4\delta_\rho^2
}$$
$$(Formally proved in Lean 4: `weil_involution_norm_sq_discrepancy`).$$

### Geometric Characterization
1. **Coincidence on Critical Line**:
   $$J(\rho) = C(\rho) \iff \delta_\rho = 0 \iff \Re(\rho) = \frac{1}{2}$$
2. **Discrepancy Measure**:
   The second-order continuous grade curvature $B_\rho''(0) = 2\delta_\rho^2(\log\tau)^2$ is directly proportional to the squared geometric discrepancy between functional reflection $J$ and complex conjugation $C$:
   $$B_\rho''(0) = \frac{(\log\tau)^2}{2} |J(\rho) - C(\rho)|^2$$

---

## 14. Canonical Weil–Hermitian Curvature Identity

### Pointwise Rational Identity
For any complex zero $\rho = \beta + i\gamma = 1/2 + \delta + i\gamma$ ($\rho \notin \{0, 1\}$):
- Moduli: $|\rho|^2 = \beta^2 + \gamma^2$, $|1-\rho|^2 = (1-\beta)^2 + \gamma^2$;
- Symmetrized Hermitian term: $T_{\text{sym}}(\rho) = \frac{1}{2}\left(\frac{1}{|\rho|^2} + \frac{1}{|1-\rho|^2}\right) = \frac{\beta^2 - \beta + 1/2 + \gamma^2}{|\rho|^2|1-\rho|^2}$;
- Weil pairing term: $T_{\text{weil}}(\rho) = \Re\left(\frac{1}{\rho(1-\rho)}\right) = \frac{\beta(1-\beta) + \gamma^2}{|\rho|^2|1-\rho|^2}$.

Subtracting the Weil pairing from the symmetrized Hermitian term:
$$T_{\text{sym}}(\rho) - T_{\text{weil}}(\rho) = \frac{(\beta^2 - \beta + 1/2 + \gamma^2) - (\beta - \beta^2 + \gamma^2)}{|\rho|^2|1-\rho|^2} = \frac{2\beta^2 - 2\beta + 1/2}{|\rho|^2|1-\rho|^2} = \frac{(1-2\beta)^2}{2|\rho|^2|1-\rho|^2}$$

Since $1-2\beta = -2\delta$, $(1-2\beta)^2 = 4\delta^2$, yielding the exact rational identity:
$$\boxed{
\frac{1}{2}\left(\frac{1}{|\rho|^2} + \frac{1}{|1-\rho|^2}\right) - \Re\left(\frac{1}{\rho(1-\rho)}\right) = \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2} = \frac{B_\rho''(0)}{(\log\tau)^2 |\rho|^2|1-\rho|^2} \ge 0
}$$
$$(Formally proved in Lean 4: `pointwise_weil_curvature_identity_algebraic`, `pointwise_weil_curvature_nonneg`, `pointwise_weil_curvature_zero_iff`).$$

### Summation Over the Discrete Zeta Divisor
Summing over all nontrivial zeros $Z$ counting multiplicity:
1. **Multiplicities & Functional Equation Symmetry**: Since $\xi(s) = \xi(1-s)$, the multiset $Z$ is invariant under $\rho \mapsto 1-\rho$. Since $\sum_\rho 1/|\rho|^2 < \infty$ converges absolutely, reindexing yields:
   $$\sum_{\rho \in Z} \frac{1}{2}\left(\frac{1}{|\rho|^2} + \frac{1}{|1-\rho|^2}\right) = \sum_{\rho \in Z} \frac{1}{|\rho|^2} =: N_\xi$$
2. **Classical Completed-$\xi$ Hadamard Sum Identity**:
   From the Hadamard product of $\xi(s) = \xi(0) \prod_\rho (1 - s/\rho) e^{s/\rho}$ evaluated at $s = 0, 1$:
   $$\sum_{\rho \in Z} \frac{1}{\rho(1-\rho)} = 2 + \gamma_{\text{Euler}} - \log(4\pi) =: C_\xi \approx 0.0461914179322420...$$
   Since $C_\xi \in \mathbb{R}$, $\sum_\rho \Re\left(\frac{1}{\rho(1-\rho)}\right) = \sum_\rho \frac{1}{\rho(1-\rho)} = C_\xi$.

### Canonical Curvature Spectral Target
Subtracting the two identities gives the exact global formula:
$$\boxed{
N_\xi - C_\xi = \sum_{\rho \in Z} \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2} = \sum_{\rho \in Z} \frac{B_\rho''(0)}{(\log\tau)^2 |\rho|^2|1-\rho|^2} \ge 0
}$$
with **strict equality $N_\xi - C_\xi = 0$ if and only if every $\delta_\rho = 0$ (the Riemann Hypothesis)**.

---

## 15. The Arithmetic Weil Functional and the GNS Positivity Barrier

### Multiplicative Test Functions and the Weil Form
For an admissible test function $g(x)$ on $\mathbb{R}_{>0}$ with Mellin transform $\hat g(s) = \int_0^\infty g(x) x^s \frac{dx}{x}$:
- **Weil Analytic Pairing**:
  $$Q_W(g) = \sum_{\rho \in Z} \hat g(\rho)\hat g(1-\rho)$$
  Constructed from the arithmetic explicit formula without using zeros:
  $$Q_W(g) = \hat g(0)\hat g(1) + \hat g(1)\hat g(0) - \sum_{n=1}^\infty \frac{\Lambda(n)}{\sqrt{n}}\left[g(n) + g\left(\frac{1}{n}\right)\right] - \mathcal{W}_{\text{arch}}(g)$$
- **Canonical Limiting Test Function $g_0 = \mathbf{1}_{(0,1)}$**:
  $\hat g_0(s) = 1/s$, $\hat g_0(1-s) = 1/(1-s)$, recovering:
  $$Q_W(g_0) = \sum_{\rho \in Z} \frac{1}{\rho(1-\rho)} = C_\xi$$
- **Hermitian Companion Functional**:
  $$Q_H(g) = \sum_{\rho \in Z} |\hat g(\rho)|^2, \qquad Q_H(g_0) = \sum_{\rho \in Z} \frac{1}{|\rho|^2} = N_\xi$$

### Attempted GNS / Positive-Type Factorization
With involution $g^*(x) = x^{-1}\overline{g(1/x)}$, the Mellin transform satisfies $\widehat{g^*}(s) = \overline{\hat g(1 - \bar s)}$.
Then $Q_W(g * g^*) = \sum_\rho \hat g(\rho) \overline{\hat g(\bar\rho)}$.
Under conjugation symmetry $\rho \leftrightarrow \bar\rho$, this formally matches $\sum_\rho |\hat g(\rho)|^2 = Q_H(g)$.

### The Positive-Type Barrier & Falsification Witness
Why cannot $Q_H(g)$ be constructed purely from local arithmetic data without assuming RH?
1. **Local Prime Distribution Indefiniteness**:
   The prime distribution contribution is $- \sum_{n=2}^\infty \frac{\Lambda(n)}{\sqrt{n}} [g(n) + g(1/n)]$.
   For localized test functions at prime nodes $u_p = \log p$, the local diagonal weights are $- \frac{\log p}{\sqrt{p}} < 0$.
   All eigenvalues of the pure local-prime Gram matrix are **strictly negative** (verified in `evaluate_finite_prime_weil_gram_matrix`).
2. **Global Balance Obligation**:
   Positivity $Q_W(g * g^*) \ge 0$ is NOT a local property; it requires precise, non-local cancellation between the negative prime distribution, the positive Archimedean distribution ($\log\pi + \psi$), and the pole distribution.
3. **Circularity of GNS Premise**:
   Weil's Criterion (Weil 1952, Bombieri 2000) states that $Q_W(g * g^*) \ge 0$ for all admissible $g$ is **strictly equivalent to the Riemann Hypothesis**.
   Therefore, defining an arithmetic Hilbert space norm $\|Jg\|^2 = Q_W(g * g^*)$ by assuming positivity $Q_W(g * g^*) \ge 0$ without a zero-independent positive factorization is logically circular.

---

## 16. Coordinate-Pulled Zero Worldlines versus Fixed Multipliers

To resolve the distinction between scalar multipliers and coordinate dilations:

1. **Fixed-Zero Scalar Multipliers**:
   For $F(k, s) = g(k, s) L(s)$ with fixed point $\rho$ ($L(\rho) = 0$):
   $F(k, \rho) = g(k, \rho) \cdot 0 = 0$ and $\partial_k^m F(k, \rho) \equiv 0$ identically for all $m \ge 0$.
   *(Formally proved in Lean 4: `scalar_multiplier_zero_preservation`, `algebraic_grade_derivative_factor_vanishing`).*
2. **Coordinate-Pulled Zero Worldlines**:
   For the coordinate-pulled family $L_k(s) = L(1/2 + \tau^{-k}(s - 1/2))$ along the moving worldline $s_\rho(k) = 1/2 + \tau^k(\rho - 1/2)$:
   $$L_k(s_\rho(k)) = L\left(\frac{1}{2} + \tau^{-k}(\tau^k(\rho - 1/2))\right) = L(\rho) = 0 \quad (\forall k \in \mathbb{R})$$
   *(Formally proved in Lean 4: `coordinate_pulled_affine_zero_worldline`).*
3. **Unpulled Function Counterexample**:
   For static $L(s) = s - \rho$, evaluated at the moving worldline $s_\rho(k)$:
   $$L(s_\rho(k)) = s_\rho(k) - \rho = (\tau^k - 1)(\rho - 1/2) \ne 0 \quad (k \ne 0, \rho \ne 1/2)$$
   *(Formally proved in Lean 4: `unpulled_affine_zero_worldline_eval`).*
   Similarly, the static product $F(k, s_\rho(k)) = g(k, s_\rho(k)) (\tau^k - 1)(\rho - 1/2) \ne 0$ generically.

---

## 17. Candidate Classification & Status

Based on rigorous auditing of all 8 criteria:
- **Pointwise Weil–Curvature Identity**: Proved algebraically & in Lean 4 (`pointwise_weil_curvature_identity_algebraic`);
- **Involution Discrepancy**: Proved $|J - C|^2 = 4\delta^2$ in Lean 4 (`weil_involution_norm_sq_discrepancy`);
- **Discrete Zeta Divisor Summation**: Derived exact target $N_\xi - C_\xi = \sum \frac{2\delta^2}{|\rho|^2|1-\rho|^2}$;
- **Zero-Independent Arithmetic Norm Construction**: **OPEN** (`OBL-CT-001A`);
- **GNS Arithmetic Factorization**: Falsified at local level due to strictly negative prime eigenvalues (`FAIL_POSITIVE_TYPE_FACTORIZATION` / Weil circularity).

$$\boxed{
\textbf{Official Classification: } \texttt{EXACT\_CURVATURE\_IDENTITY\_PROVED\_ARITHMETIC\_NORM\_OPEN}
}$$

---

## 18. Formalization and Verification Inventory

### Lean 4 Compiled Declarations (`RiemannScope.CurvatureTransport` — 37 Declarations)

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
| `grade_character_complex_product` | $(\delta+i\gamma)\log\tau k = k\delta\log\tau + i k\gamma\log\tau$ ($k \in \mathbb{R}$) | FORMALLY_PROVED |
| `grade_character_modulus_def` | $\|\chi_\rho(k)\| = \exp(k\delta\log\tau)$ | FORMALLY_PROVED |
| `reflection_reciprocal_modulus_prod` | $\|\chi_\rho(k)\| \|\chi_{\rho^\#}(k)\| = 1$ | FORMALLY_PROVED |
| `reflection_pair_defect_cosh` | $B_\rho(k) = 2(\cosh(u)-1)$ | FORMALLY_PROVED |
| `reflection_pair_defect_nonneg` | $B_\rho(k) \ge 0$ | FORMALLY_PROVED |
| `reflection_pair_defect_eq_zero_iff` | $B_\rho(k) = 0 \iff \delta = 0$ for $k \ne 0, \tau > 1$ | FORMALLY_PROVED |
| `native_grade_second_order_taylor_coefficient` | Algebraic Taylor normalization $(2\delta^2(\log\tau)^2)/(2(\log\tau)^2) = \delta^2$ | FORMALLY_PROVED (ALGEBRAIC) |
| `reflection_grade_curvature_pos` | $2\delta^2(\log\tau)^2 > 0$ for $\delta \ne 0, \tau > 1$ | FORMALLY_PROVED |
| `scalar_multiplier_zero_preservation` | $L = 0 \implies g \cdot L = 0$ | FORMALLY_PROVED |
| `scalar_multiplier_nonzero_root_iff` | $g \ne 0 \implies (g \cdot L = 0 \iff L = 0)$ | FORMALLY_PROVED |
| `algebraic_grade_derivative_factor_vanishing` | $(c \cdot g_k) \cdot L = 0$ for $L = 0$ | FORMALLY_PROVED |
| `finite_positive_weight_curvature_rigidity` | $\sum w_j \delta_j^2 = 0 \iff \forall j, \delta_j = 0$ | FORMALLY_PROVED |
| `countermodelPolynomial` | Definition of $P_{\delta,\gamma}(z)$ | DEFINITION |
| `countermodelPolynomial_even` | $P_{\delta,\gamma}(-z) = P_{\delta,\gamma}(z)$ | FORMALLY_PROVED |
| `countermodelPolynomial_root_pos_pos` | $P_{\delta,\gamma}(\delta + i\gamma) = 0$ | FORMALLY_PROVED |
| `countermodelPolynomial_root_neg_pos` | $P_{\delta,\gamma}(-\delta + i\gamma) = 0$ | FORMALLY_PROVED |
| `countermodelPolynomial_root_pos_neg` | $P_{\delta,\gamma}(\delta - i\gamma) = 0$ | FORMALLY_PROVED |
| `countermodelPolynomial_root_neg_neg` | $P_{\delta,\gamma}(-\delta - i\gamma) = 0$ | FORMALLY_PROVED |
| `weil_involution_difference` | $J(\rho) - C(\rho) = - 2\delta$ | FORMALLY_PROVED |
| `weil_involution_norm_sq_discrepancy` | Complex.normSq $(J(\rho) - C(\rho)) = 4\delta^2$ | FORMALLY_PROVED |
| `pointwise_weil_curvature_numerator_identity` | $(N_1 + N_2) - 2(\beta(1-\beta) + \gamma^2) = 4\delta^2$ | FORMALLY_PROVED |
| `pointwise_weil_curvature_identity_algebraic` | Rational Weil-Hermitian curvature identity | FORMALLY_PROVED |
| `pointwise_weil_curvature_weight_pos` | Weight $2/D > 0$ for $D > 0$ | FORMALLY_PROVED |
| `pointwise_weil_curvature_nonneg` | Curvature defect $(2\delta^2)/D \ge 0$ for $D > 0$ | FORMALLY_PROVED |
| `pointwise_weil_curvature_zero_iff` | Curvature defect $(2\delta^2)/D = 0 \iff \delta = 0$ | FORMALLY_PROVED |
| `coordinate_pulled_affine_zero_worldline` | $L_k(s_\rho(k)) = 0$ identically | FORMALLY_PROVED |
| `unpulled_affine_zero_worldline_eval` | $L(s_\rho(k)) = (\tau^k - 1) z_0$ | FORMALLY_PROVED |
| `ConditionalCurvatureRigidityBridge.all_defects_zero` | Conditional Curvature Rigidity Theorem | FORMALLY_PROVED |

### Python Test Suites
- **`tests/test_curvature_transport.py`**: 99/99 passed.
- **`tests/test_weil_curvature.py`**: 13/13 passed.
- **Total Combined Verified Tests**: 112/112 passed.

