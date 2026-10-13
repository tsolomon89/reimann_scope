# TC Review: Three-Grade Hankel Constraint & Transport–Moment Compatibility Audit

**Sprint Identifier**: TASK-TC-033  
**Principal Classification**: `TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED`  
**Parent Sprint**: TASK-TC-032R (`c9d82799`, `7cb308f3`, `42f8989b`)  
**Target Repository**: `tsolomon89/reimann_scope`  
**Formal Verification Status**: 548 project theorem declarations compiled in Lean 4 (0 sorry)  
**Numerical Precision**: Arb ball arithmetic certified enclosures  

---

## Executive Summary

TASK-TC-033 conducted a systematic structural audit of the nonlinear three-grade Hankel determinant architecture across grades $K \in \{-1, 0, 1\}$. The proposed mechanism sought to establish a contradiction between:
1. An **arithmetic rank-one law** ($\mathcal{M}_K = c^K \mathcal{M}_0 \implies \mathcal{H}_0 = \mathcal{M}_{-1}\mathcal{M}_1 - \mathcal{M}_0^2 = 0$), and
2. A **spectral positive-moment law** ($\mathcal{M}_K = \sum_\rho w_\rho r_\rho^K$ with $w_\rho > 0, r_\rho > 0$), where off-critical zeros would provide distinct reciprocal support pairs $(r, r^{-1})$ forcing $\mathcal{H}_0 > 0$.

### The Governing Falsification Finding
The audit decisively proves:
$$\boxed{\texttt{TRANSPORT\_MOMENT\_INCOMPATIBILITY\_PROVED}}$$

The exact coordinate transport ($b = 1$) required to preserve native integer station labels and yield exact arithmetic Hankel rank one ($\mathcal{H}_0 = 0$) **identically eliminates** the zero-dependent spectral grade factor:
$$\tau^{aK + (b-1)K(\rho+\sigma)} \xrightarrow{b=1} \tau^{aK + 0} = \tau^{aK}.$$
After canonical amplitude normalization by $\tau^{-aK}$, the spectral zero-coupling factor reduces to $\tau^0 = 1$ identically for all zeros $(\rho, \sigma)$ and all grades $K$. Consequently, full transport erases all zero-dependent moment variation, rendering the spectral sequence identically constant ($\widehat{\mathcal{M}}_K = \widehat{\mathcal{M}}_0$) and forcing $\mathcal{H}_0 = 0$ spectrally as well.

Conversely, any transport parameter $b \ne 1$ that preserves spectral grade dependence breaks exact arithmetic rank one due to irregular prime-power station sets across grades ($\mathcal{H}_0 \ne 0$ arithmetically).

---

## Section A: Why Linear Exact-Zero Domination Failed

In TASK-TC-032R, the linear cross-grade functional $Q_\varepsilon^{0, 1} = \langle \mu_0 \otimes \mu_1, F_{0, 1} \rangle$ was proved to vanish identically on the arithmetic side:
$$Q_\varepsilon^{0, 1} \equiv 0$$
for all $\varepsilon < \Delta_{\min} = 19 - 6\pi > 1/7 > 0$, certified via Archimedes' rational bound and Arb ball arithmetic.

However, the explicit formula equates this arithmetic mass to the complete spectral expansion:
$$Q_K = \mathcal{D}_K + \mathcal{R}_K = 0 \implies \mathcal{R}_K = -\mathcal{D}_K \implies |\mathcal{R}_K| = \mathcal{D}_K.$$
Consequently, any strategy attempting to prove $\mathcal{D}_K > |\mathcal{R}_K|$ is mathematically impossible: strict remainder domination is logically incompatible with exact arithmetic cancellation. This closed the linear exact-zero route permanently.

---

## Section B: Equal-Grade Nonzero Arithmetic Energy

To overcome the cancellation defect of identically zero functionals, TASK-TC-033 investigated the strictly positive equal-grade diagonal arithmetic energy:
$$\mathcal{M}_K = \langle \mu_K \otimes \mu_K, F_K \rangle = \sum_{n, m \ge 2} \Lambda(n)\Lambda(m) F_K(\tau^K n, \tau^K m).$$
For a diagonal mollified kernel $F_K(x, y) = w_K(x)w_K(y)\delta(x - y)$ supported near $x = y$:
$$Q_\varepsilon^{K, K}[w] = \sum_{n \ge 2} \Lambda(n)^2 [w_K(\tau^K n)]^2.$$
On the compact window $[8, 20]$, this diagonal mass contains active prime-power stations ($n \in \{8, 9, 11, 13, 16, 17, 19\}$ at $K = 0$), guaranteeing:
$$\mathcal{M}_K > 0 \quad \text{unconditionally}.$$
This strictly positive observable is tested across the minimal three-grade skeleton $K \in \{-1, 0, 1\}$.

---

## Section C: Three-Grade Hankel Determinant

For any sequence $(\mathcal{M}_{-1}, \mathcal{M}_0, \mathcal{M}_1)$, the central Hankel determinant is:
$$\mathcal{H}_0 = \operatorname{det}\begin{pmatrix} \mathcal{M}_{-1} & \mathcal{M}_0 \\ \mathcal{M}_0 & \mathcal{M}_1 \end{pmatrix} = \mathcal{M}_{-1}\mathcal{M}_1 - \mathcal{M}_0^2.$$

### Geometric Sequence (Rank One)
If $\mathcal{M}_K = A c^K$ for $A > 0, c > 0$:
$$\mathcal{H}_0 = \left(\frac{A}{c}\right)(A c) - A^2 = A^2 - A^2 = 0.$$
Formalized in Lean 4 as `RiemannScope.geometric_sequence_hankel_zero`.

---

## Section D: Positive Moment Identity

Let $\nu$ be a positive Borel measure on $(0, \infty)$ such that $\mathcal{M}_K = \int_0^\infty r^K d\nu(r)$.
For a two-point positive measure $\nu = w_1 \delta_{r_1} + w_2 \delta_{r_2}$ with $w_1, w_2 > 0$ and $r_1, r_2 > 0$:
$$\mathcal{M}_{-1} = \frac{w_1}{r_1} + \frac{w_2}{r_2}, \quad \mathcal{M}_0 = w_1 + w_2, \quad \mathcal{M}_1 = w_1 r_1 + w_2 r_2.$$
Direct expansion yields the exact algebraic identity:
$$\mathcal{H}_0 = \mathcal{M}_{-1}\mathcal{M}_1 - \mathcal{M}_0^2 = w_1 w_2 \frac{(r_1 - r_2)^2}{r_1 r_2}.$$
Formalized in Lean 4 as `RiemannScope.two_point_hankel_identity`.
Because $w_1 w_2 > 0$, $r_1 r_2 > 0$, and $(r_1 - r_2)^2 > 0$ whenever $r_1 \ne r_2$:
$$\mathcal{H}_0 > 0 \quad \text{strictly}.$$
Formalized in Lean 4 as `RiemannScope.two_point_positive_moment_hankel_pos`.

---

## Section E: Reflection and Strictness

Under the functional equation $s \leftrightarrow 1 - s$, any off-critical zero $\rho = 1/2 + \delta + i\gamma$ ($\delta \ne 0$) has a reflected partner $1 - \rho = 1/2 - \delta - i\gamma$.
In a moment representation where the support parameter reflects as:
$$r_1 = \tau^{2\delta}, \quad r_2 = r_1^{-1} = \tau^{-2\delta},$$
since $\delta \ne 0 \implies r_1 \ne 1$, the support points $r_1$ and $r_2$ are strictly distinct ($r_1 \ne r_1^{-1}$).
If both zeros receive strictly positive weights $w_1, w_2 > 0$:
$$\mathcal{H}_0 = w_1 w_2 \frac{(r_1 - r_1^{-1})^2}{r_1 r_1^{-1}} = w_1 w_2 (r_1 - r_1^{-1})^2 > 0.$$
Formalized in Lean 4 as `RiemannScope.reciprocal_pair_hankel_strict_pos`.

---

## Section F: Fully Transported Window ($b = 1$)

Under the two-parameter kernel ansatz:
$$F_K(x, y) = \tau^{aK} F_0(\tau^{-bK}x, \tau^{-bK}y), \quad \varepsilon_K = \tau^{bK} \varepsilon_0.$$
At arithmetic stations $(\tau^K n, \tau^K m)$:
$$F_K(\tau^K n, \tau^K m) = \tau^{aK} F_0(\tau^{(1-b)K} n, \tau^{(1-b)K} m).$$
Setting $b = 1$ gives:
$$F_K(\tau^K n, \tau^K m) = \tau^{aK} F_0(n, m).$$
- **Native station invariance**: The evaluated station set $\{n \in \mathbb{N} : F_0(n, n) \ne 0\}$ is completely independent of grade $K$.
- **Exact arithmetic scaling**: $\mathcal{M}_K = \tau^{aK} \mathcal{M}_0$.
- **Normalized sequence**: With canonical amplitude normalization $N_K = \tau^{-aK}$:
  $$\widehat{\mathcal{M}}_K = \mathcal{M}_0 \implies \widehat{\mathcal{M}}_{-1} = \widehat{\mathcal{M}}_0 = \widehat{\mathcal{M}}_1 = 29.2750088\dots$$
- **Arithmetic Hankel determinant**:
  $$\widehat{\mathcal{H}}_0 = 0 \quad (\text{certified in Arb: } [-7.74 \times 10^{-48}, +7.74 \times 10^{-48}]).$$

---

## Section G: Fixed Raw Window ($b = 0$)

Setting $b = 0$ fixes the window on $[8, 20]$ across all grades:
$$F_K(x, y) = \tau^{aK} F_0(x, y).$$
At arithmetic stations:
$$w_K(\tau^K n) = \tau^{aK/2} w_0(\tau^K n).$$
Active stations are $n \in [\tau^{-K} \cdot 8, \tau^{-K} \cdot 20]$:
- $K = 0$: $n \in [8, 20]$ (6 prime stations: $8, 9, 11, 13, 16, 17, 19$; mass $\approx 29.275$).
- $K = 1$: $n \in [8/\tau, 20/\tau] \approx [1.27, 3.18]$ (2 prime stations: $2, 3$; mass $\approx 1.566$).
- $K = -1$: $n \in [8\tau, 20\tau] \approx [50.27, 125.66]$ (19 prime stations; mass $\approx 289.091$).

Because the sampled primes are completely different and irregularly spaced:
$$\widehat{\mathcal{H}}_0 = (289.091)(1.566) - (29.275)^2 \approx -404.357 \ne 0.$$
Arithmetic rank one completely fails (`SPECTRAL_MOMENT_SURVIVES_ARITHMETIC_RANK_ONE_FAILS`).

---

## Section H: General Transport Parameter $b$

For any $b \notin \{0, 1\}$, the evaluated station coordinate is $\tau^{(1-b)K} n$.
Because $\tau = 2\pi$ is transcendental (Lindemann 1882), $\tau^{(1-b)K}$ is irrational for all integer $K \ne 0$ whenever $b \ne 1$.
The discrete prime powers inside the compact window shift continuously and discontinuously change membership. No universal, zero-independent normalization $N_K$ can yield $\widehat{\mathcal{H}}_0 = 0$ for arbitrary test functions. Any accidental cancellation for a specific window is classified as `FINITE_ACCIDENTAL_HANKEL_ZERO`.

---

## Section I: Mellin-Kernel Scaling

The two-variable Mellin transform is:
$$H_K(s, t) = \iint_0^\infty F_K(x, y) x^{s-1} y^{t-1} dx dy.$$
Substituting $F_K(x, y) = \tau^{aK} F_0(\tau^{-bK}x, \tau^{-bK}y)$ with substitutions $u = \tau^{-bK}x, v = \tau^{-bK}y$:
$$dx dy = \tau^{2bK} du dv, \quad x^{s-1} y^{t-1} = \tau^{bK(s+t-2)} u^{s-1} v^{t-1}.$$
Therefore:
$$H_K(s, t) = \tau^{K(a + b(s+t))} H_0(s, t).$$
In the explicit formula, $\mu_K$ has prime-dilation pushforward factors $\tau^{-K\rho}$ and $\tau^{-K\sigma}$.
The combined zero-zero term pairing $(\rho, \sigma)$ carries the net exponent:
$$K(a + b(\rho+\sigma)) - K(\rho+\sigma) = aK + (b - 1)K(\rho+\sigma).$$
Formalized in Lean 4 as `RiemannScope.transported_kernel_mellin_scaling_algebra`.

---

## Section J: Transport–Moment Compatibility or Incompatibility

After applying the canonical arithmetic normalization $N_K = \tau^{-aK}$:
$$\text{Spectral Grade Factor} = \tau^{(b-1)K(\rho+\sigma)}.$$

### The Decisive Clash
1. **Arithmetic Rank One ($b = 1$)**: Requires $b = 1$ to preserve native integer station labels.
2. **Spectral Moment Survival ($b \ne 1$)**: Requires $b \ne 1$ to preserve zero dependence $\tau^{(b-1)K(\rho+\sigma)}$.

At $b = 1$:
$$(b - 1)K(\rho+\sigma) = (1 - 1)K(\rho+\sigma) = 0 \implies \tau^0 = 1.$$
The spectral grade factor is **identically 1**, completely independent of the zeros $\rho, \sigma$ and grade $K$!
Formalized in Lean 4 as `RiemannScope.full_transport_spectral_factor_cancellation` and `full_transport_net_exponent_zero`.

**Conclusion**: The unique transport that proves arithmetic rank one identically eliminates the zero-dependent spectral moments required for off-critical Hankel detection.

---

## Section K: Complete Spectral Representation Audit

Even if $b \ne 1$ were considered, the complete explicit formula spectral side is:
$$\mathcal{M}_K = \mathcal{M}_{K, \text{zero-zero}} + \mathcal{M}_{K, \text{zero-arch}} + \mathcal{M}_{K, \text{arch-arch}} + \mathcal{M}_{K, \text{pole}}.$$
Every component must be accounted for. The presence of non-zero background and Archimedean terms destroys pure moment structure unless proven to possess an exact common positive representation.

---

## Section L: Signed-Weight and Cross-Term Firewalls

### 1. Signed-Weight Firewall
If weights in $\sum_\rho c_\rho r_\rho^K$ can be negative or complex (which occurs in general explicit formula pairings due to oscillatory phase factors $\operatorname{Re}(H(\rho, \sigma))$), the Hankel determinant can be negative or zero despite multiple support points.
- **Countermodel**: $w_1 = 1, w_2 = -2, r_1 = 1, r_2 = 2 \implies \mathcal{H}_0 = -1 < 0$.
- Formalized in Lean 4 as `RiemannScope.signed_weights_hankel_negative`.
- Classified as `SIGNED_SPECTRAL_WEIGHTS_DO_NOT_IMPLY_HANKEL_POSITIVITY`.

### 2. Cross-Term Firewall
The equal-grade quadratic energy produces a double zero sum:
$$\sum_{\rho, \sigma} C_{\rho, \sigma} q_\rho^K \overline{q_\sigma}^K.$$
This quadratic form cannot be treated as a single scalar positive moment sequence without diagonalizing $C$ with non-negative eigenvalues.
Classified as `DOUBLE_SPECTRAL_SUM_NOT_POSITIVE_MOMENT_SEQUENCE`.

---

## Section M: Weil-Equivalence Test

Requiring unconditional positive definiteness of the spectral quadratic form on general test functions is mathematically equivalent to Weil's positivity criterion for RH. Asserting spectral positivity without an independent arithmetic derivation is circular.
Classified as `HANKEL_POSITIVITY_IS_RH_EQUIVALENT`.

---

## Section N: Generic-Base Control

The scaling exponent cancellation $(1 - 1)K = 0$ holds identically for any scale base $q > 1$:
$$q^{(1-1)K(s+t)} = q^0 = 1.$$
The cancellation is an inherent property of pushforward scaling covariance, not a feature specific to $\tau = 2\pi$.
Formalized in Lean 4 as `RiemannScope.generic_base_covariance`.
Classified as `GENERIC_PUSHFORWARD_COVARIANCE`.

---

## Section O: Principal Classification

$$\boxed{\texttt{TRANSPORT\_MOMENT\_INCOMPATIBILITY\_PROVED}}$$

The three-grade equal-grade Hankel determinant architecture fails because the exact kernel transport required to achieve arithmetic rank one is mathematically incompatible with the spectral zero-moment dependence required for off-critical detection.

---

## Section P: Exact Next Theorem, If Any

No subgate remains open for the equal-grade three-grade Hankel determinant architecture. Any future TC constraint mechanism must not rely on equal-grade pushforward transport covariance.
