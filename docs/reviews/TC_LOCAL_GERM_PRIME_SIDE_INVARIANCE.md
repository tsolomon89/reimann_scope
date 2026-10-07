# TASK-TC-024: Local Zero Germ, Prime-Side Unit Change, and Intrinsic Grade Invariance

## Executive Summary & Canonical Classifications

- **Primary Research Focus**: Investigation of the local zero germ of the centered completed grid zeta family $\Xi_K(s) = \tau^{-K(s-1/2)}\xi(s)$ at nontrivial zeros $\rho = 1/2 + \delta + i\gamma$, its transformation law under arithmetic grade change $K \in \mathbb{A}_{\mathbb{R}}$, and whether its modulus variation $\tau^{-(K-J)\delta}$ carries any intrinsic prime-side arithmetic meaning or is merely coordinate/normalization covariance.
- **Principal Classification**: `LOCAL_GERM_IS_GENERIC_GAUGE_DATA`
  - The local zero germ transformation $c_{\Xi_K}(\rho) = \tau^{-K(\rho-1/2)} c_\xi(\rho)$ is proved to be a generic entire-function property (`GENERIC_NONVANISHING_PREFACTOR_COVARIANCE`) that holds for **any** holomorphic function multiplied by $e^{-a(s-s_0)}$.
  - Multiplication by $\tau^{-K(s-1/2)}$ leaves the zero divisor and canonical Weierstrass product completely unchanged, altering only the linear coefficient of the nonvanishing exponential Hadamard prefactor ($B \mapsto B - K\log\tau$).
  - The local zero germ has scaling weight $-(\rho - 1/2) = -\delta - i\gamma$ under arithmetic unit change. Demanding that its numerical magnitude remain unchanged under a unit change from $\tau^J$ to $\tau^K$ is physically and mathematically unjustified.
  - The unit-normalized germ $\widehat{c}_K(\rho) = \tau^{K(\rho-1/2)} c_{\Xi_K}(\rho) = c_\xi(\rho)$ is completely grade-invariant, removing the $\tau^{-K\delta}$ modulus variation entirely.
  - The local-germ route toward an RH proof is formally **FROZEN**.
- **Epistemic Correction from TASK-TC-023**:
  - The phrase `NO_TWO_DIRECTION_ZETA_TRANSFER` has been corrected throughout repository documentation to `NO_TWO_DIRECTION_ZETA_TRANSFER_FOUND` within audited structures. No theorem of impossibility was proved or is claimed.
- **Formal Verification**:
  - Lean 4 formalization compiled in `formal/RiemannScope/LocalGermInvariance.lean` (16 project theorems, 0 errors, 0 sorries; total project declarations: 378).
  - Dedicated test suite `tests/test_tc_local_germ_prime_side_invariance.py` passes all 16/16 verification tests.

---

## 1. Local Zero Germ and Generic Gauge Control

### A. What exactly is the local zero germ?

Let $F(s)$ be a holomorphic function in a neighborhood of $\rho \in \mathbb{C}$ with a zero of order $m \ge 1$:
$$F(s) = \sum_{k=m}^\infty c_k (s - \rho)^k, \qquad c_m \ne 0.$$
The **leading local zero germ** of $F$ at $\rho$ is the first non-vanishing Taylor coefficient:
$$\boxed{c_F(\rho) = \frac{F^{(m)}(\rho)}{m!}.}$$
For a simple zero ($m = 1$), this is simply the derivative $F'(\rho)$.

### B. How does it transform under arithmetic grade change?

For the canonical centered completed grid family:
$$\Xi_K(s) = \tau^{-K(s - 1/2)}\xi(s), \qquad \tau = 2\pi, \quad K \in \mathbb{A}_{\mathbb{R}},$$
let $\rho = 1/2 + \delta + i\gamma$ be a zero of $\xi(s)$ of multiplicity $m$. Expanding $\tau^{-K(s - 1/2)}$ around $s = \rho$:
$$\tau^{-K(s - 1/2)} = \tau^{-K(\rho - 1/2)} \tau^{-K(s - \rho)} = \tau^{-K(\rho - 1/2)} \left[ 1 - K(\log\tau)(s - \rho) + O((s - \rho)^2) \right].$$
Multiplying by $\xi(s) = c_\xi(\rho)(s - \rho)^m + O((s - \rho)^{m+1})$ yields:
$$\Xi_K(s) = \tau^{-K(\rho - 1/2)} c_\xi(\rho)(s - \rho)^m + O((s - \rho)^{m+1}).$$
Therefore:
$$\boxed{c_{\Xi_K}(\rho) = \frac{\Xi_K^{(m)}(\rho)}{m!} = \tau^{-K(\rho - 1/2)} c_\xi(\rho).}$$
The ratio between two grades $K$ and $J$ is:
$$\boxed{\frac{c_{\Xi_K}(\rho)}{c_{\Xi_J}(\rho)} = \tau^{-(K - J)(\rho - 1/2)} = \tau^{-(K - J)\delta} e^{-i(K - J)\gamma \log\tau}.}$$
In modulus:
$$\boxed{\left| \frac{c_{\Xi_K}(\rho)}{c_{\Xi_J}(\rho)} \right| = \tau^{-(K - J)\delta}.}$$

### C. Is that transformation zeta-specific?

**No.** This transformation is entirely generic.
Let $F(s)$ be an **arbitrary** holomorphic function with a zero of order $m$ at $\rho$, and let:
$$F_K(s) = e^{-KL(s - s_0)} F(s)$$
for any non-zero real constant $L$ and any fixed reference point $s_0 \in \mathbb{C}$. Then:
$$\boxed{c_{F_K}(\rho) = e^{-KL(\rho - s_0)} c_F(\rho),}$$
and
$$\boxed{\left| \frac{c_{F_K}(\rho)}{c_{F_J}(\rho)} \right| = e^{-(K - J)L \operatorname{Re}(\rho - s_0)}.}$$
The TC local-germ detector follows entirely from this generic theorem of complex analysis.
Classification: `GENERIC_NONVANISHING_PREFACTOR_COVARIANCE`.

---

## 2. Hadamard Factorization and Normalization Data

### D. How does multiplication by a nonvanishing exponential alter Hadamard factorization?

The completed Riemann zeta function $\xi(s)$ is an entire function of order 1. By the Hadamard factorization theorem:
$$\xi(s) = e^{A + B s} \prod_\rho E\left(\frac{s}{\rho}\right) = e^{A + B s} \prod_\rho \left(1 - \frac{s}{\rho}\right) e^{s/\rho}.$$
When we form $\Xi_K(s) = e^{-KL(s - 1/2)}\xi(s)$ (with $L = \log\tau$):
$$\Xi_K(s) = \exp\left( (A + \tfrac{1}{2}KL) + (B - KL)s \right) \prod_\rho E\left(\frac{s}{\rho}\right).$$
- **Zero Divisor**: Completely unchanged. The zeros $\rho$ and their multiplicities $m_\rho$ are identical for all $K$.
- **Canonical Product**: $\prod_\rho E(s/\rho)$ is completely unchanged.
- **Hadamard Prefactor**: Only the non-vanishing exponential prefactor changes:
  $$A \mapsto A + \tfrac{1}{2}KL, \qquad B \mapsto B - KL.$$
The local-germ magnitude variation is precisely the standard freedom of multiplying an entire function by $e^{as + b}$.

### E. Which zero data are normalization invariant?

| Quantity | Mathematical Expression | Classification | Reason |
|:---|:---|:---:|:---|
| Zero Location | $\rho$ | `ZERO_DIVISOR_INVARIANT` | Root of $F(s) = 0$; unaffected by $e^{as+b} \ne 0$. |
| Zero Multiplicity | $m = \operatorname{ord}_{s=\rho}(F)$ | `ZERO_DIVISOR_INVARIANT` | Order of zero is invariant under multiplication by units. |
| Log-Derivative Residue | $\operatorname{Res}_{s=\rho}(F'/F) = m$ | `ZERO_DIVISOR_INVARIANT` | Cauchy integral $\frac{1}{2\pi i}\oint \frac{F'}{F} ds = m$ is homotopy invariant. |
| Canonical Product | $\prod_\rho E(s/\rho)$ | `ZERO_DIVISOR_INVARIANT` | Determined purely by zero locations. |
| Leading Germ | $c_F(\rho) = F^{(m)}(\rho)/m!$ | `NORMALIZATION_DEPENDENT` | Transforms as $c_{F_K}(\rho) = e^{-a(\rho-s_0)} c_F(\rho)$. |
| Regularized Constant | $h_{\rho} = \lim_{s\to\rho}(F'/F - m/(s-\rho))$ | `NORMALIZATION_DEPENDENT` | Transforms as $h_{\rho, K} = h_\rho - KL$. |
| Hadamard Linear Exponent | $B$ | `NORMALIZATION_DEPENDENT` | Shifts by $-KL$. |

### F. Which zero data detect $\delta$?

- The leading local germ modulus: $|c_{\Xi_K}(\rho)| = \tau^{-K\delta} |c_\xi(\rho)|$.
- The finite difference of log-moduli: $\log|c_{\Xi_K}(\rho)| - \log|c_{\Xi_J}(\rho)| = -(K - J)\delta\log\tau$.
- The centered harmonic translation multiplier: $|H_\rho(x + KL)/H_\rho(x)| = \tau^{K\delta}$.
- The bilateral defect: $B_\rho(K) = |\tau^{-K(\rho-1/2)}| + |\tau^{K(\rho-1/2)}| - 2 = 4\sinh^2(K\delta\log\tau / 2)$.

### G. Are those $\delta$-sensitive data intrinsic?

**No.** Every $\delta$-sensitive quantity above is strictly **normalization-dependent** (`DELTA_SENSITIVE_BUT_NORMALIZATION_DEPENDENT`).
In physical terms, $c_{\Xi_K}(\rho)$ has conformal scaling weight:
$$w = -(\rho - 1/2) = -\delta - i\gamma.$$
When the unit of the arithmetic system is scaled by $\tau^K$, the numerical coordinate of any object with scaling weight $w$ transforms by $(\tau^K)^w = \tau^{-K(\rho - 1/2)}$. Demanding that $|c_{\Xi_K}(\rho)| = |c_{\Xi_J}(\rho)|$ across distinct units is mathematically equivalent to asserting that the weight is zero, which assumes $\delta = 0$.

---

## 3. Logarithmic Derivative and Prime-Side Structures

### H. What does $Z_K'/Z_K$ do under grade change?

For the canonical grid zeta $Z_K(s) = \tau^{-Ks}\zeta(s)$:
$$\log Z_K(s) = -Ks\log\tau + \log\zeta(s).$$
Differentiating:
$$\boxed{\frac{Z_K'}{Z_K}(s) = -K\log\tau + \frac{\zeta'}{\zeta}(s),}$$
$$\boxed{-\frac{Z_K'}{Z_K}(s) = K\log\tau - \frac{\zeta'}{\zeta}(s) = K\log\tau + \sum_{n=1}^\infty \frac{\Lambda(n)}{n^s} \qquad (\operatorname{Re}(s) > 1).}$$

### I. How should the $K\log\tau$ term be interpreted?

The extra $K\log\tau$ is an **additive constant baseline**, entirely independent of $s$.
It reflects the global grade unit $\tau^{-Ks}$ attached to the Dirichlet series. It does not shift the prime stations $\log n$ or alter their weights $\Lambda(n)$.

### J. Is the geometric shifted-prime measure the same object as the Euler-product prime distribution?

**No.** They are fundamentally distinct mathematical objects:
1. **Geometric Shifted Prime Measure**:
   $$\mu_K^{\text{geom}} = \sum_n \Lambda(n) \delta_{\log n + K\log\tau}.$$
   Its Laplace transform is:
   $$\int_0^\infty e^{-sx} d\mu_K^{\text{geom}}(x) = \sum_n \Lambda(n) e^{-s(\log n + K\log\tau)} = \tau^{-Ks} \sum_n \frac{\Lambda(n)}{n^s} = \tau^{-Ks} \left(-\frac{\zeta'}{\zeta}(s)\right).$$
2. **Logarithmic Derivative of Grid Zeta**:
   $$-\frac{Z_K'}{Z_K}(s) = K\log\tau - \frac{\zeta'}{\zeta}(s).$$
The geometric prime measure translates every prime station by $K\log\tau$ in log-space, producing a **multiplicative factor** $\tau^{-Ks}$ on the Laplace transform. The grid zeta applies one global unit $\tau^{-Ks}$ to the entire series, producing an **additive shift** $K\log\tau$ in the logarithmic derivative.
Furthermore, the naive Euler product over shifted primes $\prod_p (1 - (p\tau^K)^{-s})^{-1}$ would assign weights $\tau^{-K\Omega(n)s}$, violating global grade $K$ (the TASK-TC-022 firewall).

### K. Does the explicit formula contain local derivative magnitudes such as $|\xi'(\rho)|$?

**No.** In the explicit formula (Riemann, Guinand, Weil), zeros enter exclusively as poles of $-\frac{\zeta'}{\zeta}(s)$ or $-\frac{\xi'}{\xi}(s)$ against test functions:
$$\frac{1}{2\pi i} \oint_\Gamma h(s) \left(-\frac{\xi'}{\xi}(s)\right) ds = \sum_\rho m_\rho h(\rho).$$
At a simple zero ($m_\rho = 1$), the residue is identically 1, completely independent of the value of $\xi'(\rho)$ or $\zeta'(\rho)$.
The explicit formula records **zero locations and multiplicities**, never local derivative magnitudes.

### L. Is there an exact prime-side formula for the leading zero germ?

**No.** No such functional was found in the standard explicit-formula structures audited. The prime counting distribution depends only on the zero divisor (locations and multiplicities), with no dependence on local derivative values.

---

## 4. Normalization and Invariance

### M. Is the normalized germ grade invariant?

**Yes.** Define the canonical unit-normalized local germ:
$$\boxed{\widehat{c}_K(\rho) = \tau^{K(\rho - 1/2)} c_{\Xi_K}(\rho).}$$
Substituting $c_{\Xi_K}(\rho) = \tau^{-K(\rho - 1/2)} c_\xi(\rho)$:
$$\boxed{\widehat{c}_K(\rho) = \tau^{K(\rho - 1/2)} \tau^{-K(\rho - 1/2)} c_\xi(\rho) = c_\xi(\rho).}$$
$\widehat{c}_K(\rho)$ is identically $c_\xi(\rho)$ for every $K \in \mathbb{A}_{\mathbb{R}}$.

### N. Does normalization remove the $\delta$-detector?

**Yes.** Normalization removes the $\tau^{-K\delta}$ modulus variation completely:
$$\boxed{|\widehat{c}_K(\rho)| = |c_\xi(\rho)|}$$
for all $K$, regardless of whether $\delta = 0$ or $\delta \ne 0$.
The detector $\tau^{-K\delta}$ was merely measuring the coordinate unit weight $\tau^K$, not an intrinsic arithmetic inconsistency.

---

## 5. Unitarity, Representations, and Weil Positivity

### O. Does log-coordinate grade translation define a unitary representation?

On $L^2(\mathbb{R}, dx)$, translation $(T_a f)(x) = f(x - a)$ is an unconditional unitary operator:
$$\|T_a f\|_{L^2} = \|f\|_{L^2}.$$
This is a standard theorem of harmonic analysis (Stone's theorem).

### P. Are zeta zeros genuine spectral characters of that unitary representation?

**No.** The centered zero mode is:
$$f_\rho(x) = e^{(\rho - 1/2)x} = e^{(\delta + i\gamma)x}.$$
Plane-wave critical-line characters ($\delta = 0$) are also generally not elements of $L^2(\mathbb{R})$; they are generalized unitary Fourier characters. The meaningful distinction is unit modulus versus exponential growth/decay under translation.
When $\delta \ne 0$, $f_\rho(x)$ grows exponentially as $x \to +\infty$ (if $\delta > 0$) or as $x \to -\infty$ (if $\delta < 0$).
Therefore:
$$\boxed{f_\rho \notin L^2(\mathbb{R}).}$$
It is not an eigenmode of the unitary translation representation on $L^2(\mathbb{R})$. It is a generalized eigenfunction in an exponentially weighted space $L^2(\mathbb{R}, e^{-2\delta x} dx)$, where translation is non-unitary and has operator norm multiplier $e^{\delta a} = \tau^{K\delta}$.
Off-line zeros can appear in Laplace/Dirichlet expansions without contradicting the unitarity of translations on $L^2(\mathbb{R})$.

### Q. Does this reduce to Weil/Herglotz positivity?

**Yes.** Asserting that the arithmetic prime distribution generates a positive-definite translation kernel on $L^2(\mathbb{R})$ whose complete spectrum coincides with the zeta zeros is precisely Weil's explicit formula positivity / the Hilbert-Pólya conjecture.
Classification: `RH_EQUIVALENT_REFORMULATION`.

### R. Does corrected arithmetic TC supply any previously missing hypothesis?

**No.** The arithmetic TC grid $L_K = \tau^K \mathbb{Z}$ rigorously separates grid stations across grades (Lindemann 1882), but:
1. Coordinate translations do not force off-line zero modes into $L^2(\mathbb{R})$.
2. The local zero germ scales by the generic non-vanishing prefactor $\tau^{-K(\rho - 1/2)}$.
3. No unconditional arithmetic theorem forces unit-dependent local derivatives to be invariant across distinct units.

---

## 6. Comprehensive Audit of Candidate Invariants

### S. Is there any intrinsic, grade-independent, $\delta$-sensitive quantity?

**No.** Every candidate quantity audited in the repository falls into one of two mutually exclusive categories:

| Candidate Observable | Grade Invariant? | Normalization Invariant? | $\delta$-Sensitive? | Final Classification |
|:---|:---:|:---:|:---:|:---|
| Zero Location $\rho$ | Yes | Yes | No ($\rho$ is given) | `GRADE_INVARIANT_NO_DELTA` |
| Zero Multiplicity $m$ | Yes | Yes | No | `GRADE_INVARIANT_NO_DELTA` |
| Log-Derivative Residue $\operatorname{Res}(F'/F)$ | Yes | Yes | No | `GRADE_INVARIANT_NO_DELTA` |
| Normalized Germ $\widehat{c}_K(\rho)$ | Yes | Yes | No (cancels $\delta$) | `GRADE_INVARIANT_NO_DELTA` |
| Reflected Germ Product $c_{\Xi_K}(\rho) c_{\Xi_K}(1-\rho)$ | Yes | No | No (cancels $\tau^K$) | `GRADE_INVARIANT_NO_DELTA` |
| Bilateral Grade Product $|\eta_\rho(K)| |\eta_\rho(K)|^{-1}$ | Yes | Yes | No (identically 1) | `GRADE_INVARIANT_NO_DELTA` |
| Raw Local Germ Modulus $\|c_{\Xi_K}(\rho)\|$ | No | No | Yes ($\tau^{-K\delta}$) | `DELTA_SENSITIVE_BUT_NORMALIZATION_DEPENDENT` |
| Germ Modulus Ratio $\|c_{\Xi_K}(\rho)/c_{\Xi_J}(\rho)\|$ | No | No | Yes ($\tau^{-(K-J)\delta}$) | `DELTA_SENSITIVE_BUT_NORMALIZATION_DEPENDENT` |
| Grade Character $\eta_\rho(K)$ | No | No | Yes ($\tau^{-K\delta}$) | `DELTA_SENSITIVE_BUT_NORMALIZATION_DEPENDENT` |
| Non-Unitarity Defect $B_\rho(K)$ | No | No | Yes ($4\sinh^2$) | `DELTA_SENSITIVE_BUT_NORMALIZATION_DEPENDENT` |
| Centered Harmonic Multiplier | No | No | Yes ($\tau^{K\delta}$) | `DELTA_SENSITIVE_BUT_NORMALIZATION_DEPENDENT` |

Result: **There is no genuinely intrinsic, grade-independent, $\delta$-sensitive quantity.**
`GENUINELY_INTRINSIC_DELTA_SENSITIVE`: **0 candidates found.**

---

## 7. Governing Conclusion and Next Research Direction

### T. What is the next theorem?

The local zero germ magnitude variation:
$$\left| \frac{c_{\Xi_K}(\rho)}{c_{\Xi_J}(\rho)} \right| = \tau^{-(K-J)\delta}$$
is entirely the coordinate/normalization covariance of a unit-dependent quantity under arithmetic scaling. It does not provide an independent mechanism to force $\delta = 0$.
The local-germ bridge route is formally **FROZEN**.

### Next Research Question:
Can the discrete arithmetic prime-power stations $p^k \tau^K$ in the faithful graded algebra $\mathcal{R}_\tau = \mathbb{Z}[\tau, \tau^{-1}]$ constrain off-critical zeros through a **global trace invariant** (such as incommensurable station support collisions) that does not depend on local zero derivative magnitudes or non-vanishing gauge prefactors?
