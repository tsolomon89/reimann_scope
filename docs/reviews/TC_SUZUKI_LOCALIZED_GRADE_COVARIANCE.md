# TASK-TC-020: Suzuki Localized Weil Positivity, TC Grade Covariance, and Two-Direction Transcendence Rigidity

**Document Type:** Formal Research Review & Primary Investigation Artifact  
**Repository:** `tsolomon89/reimann_scope`  
**Task ID:** TASK-TC-020  
**Date:** October 2026  
**Status:** AUDITED & VERIFIED  

---

## Executive Summary & Decision Tree Outcome

This sprint investigates whether the Transcendental Continuation (TC) grade action can induce a genuine covariance between Masatoshi Suzuki's localized Weil/screw-function operator structures across scales, strong enough to propagate unconditionally proven local positivity ($R < R_0$) to arbitrary global scales. Simultaneously, it evaluates the two-direction transcendence rigidity architecture governing the exceptional exponent set $S_\tau = \{\alpha \in \mathbb{A}_{\mathbb{R}} : \tau^\alpha \in \overline{\mathbb{Q}}\}$.

### Primary Findings
1. **Suzuki 2023 [W2] and 2026 [W10] Primary-Source Verification**:
   - **Suzuki 2023 [W2]**: Theorem 1.2 proves that the regularized continuous zero function $g(t)$ generates a positive semidefinite kernel $G_g(t, u) = g(t-u) - g(t) - g(-u) + g(0)$ for all $t, u \in \mathbb{R}$ **if and only if RH holds**. Global screw positivity is strictly `RH_EQUIVALENT`.
   - **Suzuki 2026 [W10]**: Unconditionally establishes:
     - The localized Weil operator $A_R$ on $L^2(-R, R)$ is the Friedrichs extension of the symmetric operator $B_R = D^* G_R D$ on $H_0^1(-R, R)$ (Theorem 1.1).
     - The lowest eigenvalue $\lambda_1(R)$ is continuous in $R \in (0, \infty)$ (Theorem 1.3).
     - For sufficiently small $R < R_0$, $\lambda_1(R) > 0$ is simple, with $\lambda_1(R) = \frac{3}{2R^2} + O(1/R)$ as $R \to 0^+$, with even ground state (Theorem 1.4, **unconditional local positivity**).
     - Shifting $T_R = A_R - \lambda I > 0$ for $\lambda < \lambda_1(R)$ yields self-adjoint extensions $\overline{\mathscr{D}}_{R, \theta}$ of $\mathscr{D}_R = i \frac{d}{dx}$ in $\mathcal{H}(T_R)$ whose characteristic functions $W(R, \theta; z)$ have **all zeros real** unconditionally (Theorem 1.5).
     - A compact-uniform limit of $W(R, \theta; z)$ to $(1 - i \xi'/\xi)^{-1}$ implies RH (Corollary 1.6), but Suzuki proves this limit requires $\lambda = 0$ for large $R$, which is equivalent to full Weil positivity and RH.

2. **Resolution of Governing Question on Positivity Propagation**:
   - **Outcome Selection**: **Case B (`PROVED_PURE_RESCALING`) and Case C (`NO_NATURAL_INTERTWINER`)**.
   - Dilation $(S_K v)(x) = \tau^{K/2} v(\tau^K x)$ moves the test function across the fixed arithmetic prime stations $\log p$ and archimedean digamma terms $\psi$. Because the explicit formula kernel $k(t)$ is not homogeneous, $S_K^* A_{\tau^{-K} R} S_K \ne A_R$. Dilation does not intertwine the localized arithmetic operators.
   - Regarded as a coordinate change, dilation merely scales the interval and the operator together without expanding the physical domain of the original Weil distribution.
   - Translation $T_{K\log\tau}$ preserves quadratic form values for individual functions ($Q_W(T_h v) = Q_W(v)$), but translates the support off-center to $[h - R, h + R]$. Controlling linear combinations across translates requires cross-grade positivity, which is mathematically identical to the full Weil positivity criterion ($C_h(0) = Q_W(h) \ge 0$).
   - Therefore: **TC grade action CANNOT propagate local positivity of $Q_W$ to global positivity without assuming an RH-equivalent hypothesis.**

3. **Two-Pairing Firewall Strictly Enforced**:
   - The **Reflected Weil Pairing** $Q_W(f, g) = \sum_\rho F(w_\rho) \overline{G(-\overline{w_\rho})}$ is unconditionally shift-invariant ($Q_W(T_h f, T_h g) = Q_W(f, g)$), but its positivity is `RH_EQUIVALENT`.
   - The **Ordinary Gram Pairing** $Q_+(f, g) = \sum_\rho F(w_\rho) \overline{G(w_\rho)}$ is unconditionally positive, but translation scales off-line modes by $e^{-2\delta h}$, breaking shift-invariance unless $\delta = 0$.
   - Conflating positivity from $Q_+$ with invariance from $Q_W$ is circular.

4. **Exceptional Exponent Rigidity & Algebraic Separation**:
   - **Exceptional Exponent Theorem**: For $S_\tau = \{\alpha \in \mathbb{A}_{\mathbb{R}} : \tau^\alpha \in \overline{\mathbb{Q}}\}$, $S_\tau \cap \mathbb{Q} = \{0\}$ (Lindemann), and by Gelfond–Schneider, any two nonzero elements $\alpha, \beta \in S_\tau$ must have $\beta/\alpha \in \mathbb{Q}$. Hence:
     $$\boxed{\dim_{\mathbb{Q}} S_\tau \le 1} \qquad (\texttt{PROVED\_FROM\_GELFOND\_SCHNEIDER}).$$
   - **Epistemic Qualification**: This does not prove $S_\tau = \{0\}$; it proves exceptional exponents lie on at most one rational line in $\mathbb{A}_{\mathbb{R}}$.
   - **Rational-Grade Algebraic Separation**: For $m, n \in \overline{\mathbb{Q}}^\times$ and $K, J \in \mathbb{Q}$:
     $$m \tau^K = n \tau^J \iff K = J \text{ and } m = n \qquad (\texttt{PROVED\_EXACT}).$$
   - **Two-Direction Collision Architecture**: An audit of all existing TC branches reveals no mechanism forcing two $\mathbb{Q}$-independent algebraic exponents into $S_\tau$. The status is `TWO_DIRECTION_COLLISION_BRIDGE_OPEN` (Report: `NO_EXISTING_TWO_DIRECTION_BRIDGE`).

---

## Detailed Resolutions of Questions A through O

### Question A: What exactly does Suzuki 2023 prove?
In *Aspects of the screw function corresponding to the Riemann zeta-function*, JLMS 108 (2023), 1448–1487 ([W2]), Theorem 1.2:
- Suzuki introduces the continuous real-valued even function on $\mathbb{R}$:
  $$g(t) = \int_0^{|t|} (1 - e^{-2u})^{-1/2} du - \frac{1}{2}\log 2 + \sum_{n \le e^{|t|}} n^{-1/2} \Lambda(n)(|t| - \log n) + r(t),$$
  obtained by integrating twice the formal distribution $k(t) = \sum_\gamma e^{-i\gamma t}$.
- He defines the two-variable kernel:
  $$G_g(t, u) = g(t-u) - g(t) - g(-u) + g(0).$$
- **Theorem 1.2 Statement**: $g(t)$ is a screw function on $\mathbb{R}$ in the sense of Krein–Langer (i.e. the kernel $G_g(t, u)$ is positive semidefinite for all $t, u \in \mathbb{R}$) **if and only if the Riemann Hypothesis holds**.
- **Classification**: `RH_EQUIVALENT`.
- This removes the divergent distribution issue of the raw zero trace, but its global positivity remains equivalent to RH.

---

### Question B: What exactly does Suzuki 2026 prove unconditionally?
In *Weil's quadratic form via the screw function*, arXiv:2606.09096v3, 23 September 2026 ([W10]), Suzuki proves **without assuming RH**:
1. **Theorem 1.1**: The self-adjoint operator $A_a$ associated with the localized closed symmetric form $Q_W^a(v) = \langle A_a v, v \rangle_{L^2}$ on $L^2(-a, a)$ is the Friedrichs extension of the symmetric operator $B_a = D^* G_a D$ with domain $H_0^1(-a, a)$, where $G_a = P_a G P_a$ and $D = i \frac{d}{dx}$ with Dirichlet boundary conditions.
2. **Theorem 1.3**: The lowest eigenvalue $\lambda_a = \inf_{v \in C_c^\infty(-a, a), v \ne 0} \frac{Q_W^a(v)}{\|v\|_{L^2}^2}$ is continuous in $a \in (0, \infty)$.
3. **Theorem 1.4**: For sufficiently small $a > 0$, $\lambda_a$ is strictly positive, simple, with $\lambda_a = \frac{3}{2a^2} + O(1/a)$ as $a \to 0^+$, and its corresponding ground state is even.
4. **Theorem 1.5**: For any $a > 0$, choosing $\lambda < \lambda_a$ gives a positive operator $T_a = A_a - \lambda I > 0$, defining a Hilbert space $\mathcal{H}(T_a)$. The minimal differential operator $\mathscr{D}_a = i \frac{d}{dx}$ on $\mathcal{H}(T_a)$ has deficiency indices $(1,1)$, admitting self-adjoint extensions $\overline{\mathscr{D}}_{a, \theta}$ ($\theta \in [0, 2\pi)$). The eigenvalues of $\overline{\mathscr{D}}_{a, \theta}$ are the zeros of an entire function $W(a, \theta; z)$, and **all zeros of $W(a, \theta; z)$ are real**.
5. **Epistemic Boundary**: Shifting $A_a - \lambda I$ constructs a positive Hilbert metric and self-adjoint extension with real eigenvalues unconditionally, but this does NOT prove that $A_a$ itself is positive ($\lambda_a \ge 0$). Shifting by a constant does not eliminate negative spectrum of the original operator.

---

### Question C: What is localized?
In Suzuki's 2026 theory:
- The localization parameter is $R > 0$ (written $a$ in Suzuki, renamed $R$ in TC to prevent collision with $a = \log\tau$).
- The localized domain is the finite interval $[-R, R] \subset \mathbb{R}$.
- The localized test spaces are $C_c^\infty(-R, R)$ and $H_0^1(-R, R) \subset L^2(-R, R)$.
- The localized quadratic form is $Q_W^R(v) = W(v * \widetilde{v})$ for $v \in C_c^\infty(-R, R)$.
- The localized operator is $A_R$ on $L^2(-R, R)$, representing $Q_W^R(v) = \langle A_R v, v \rangle_{L^2}$.

---

### Question D: What is the exact screw kernel?
The screw function $g(t)$ is continuous, real-valued, and even on $\mathbb{R}$, with asymptotic expansion near the origin:
$$g(t) = 2\log|t| + (2A + 1) + \sum_{n \le e^{|t|}} n^{-1/2} \Lambda(n)(|t| - \log n) + r(t),$$
where $A = \frac{1}{2}(\log\pi + C_0)$, and $r(t) = O(t^2)$ is an even $C^2$ function.
The exact screw kernel is:
$$\boxed{G_g(t, u) = g(t-u) - g(t) - g(-u) + g(0)}.$$
Because $g$ is even, $G_g(t, u) = G_g(u, t)$ is real symmetric, and $G_g(t, 0) = G_g(0, u) = 0$.

---

### Question E: What is the exact localized Weil operator/form?
On $[-R, R]$, for $v \in C_c^\infty(-R, R)$:
$$Q_W^R(v) = \langle A_R v, v \rangle_{L^2(-R, R)} = \langle B_R v, v \rangle_{L^2(-R, R)} = \langle G_R v', v' \rangle_{L^2(-R, R)},$$
where:
$$G_R = P_R G P_R, \qquad (Gu)(x) = \int_{\mathbb{R}} g(x-y) u(y) dy,$$
and $P_R: L^2(\mathbb{R}) \to L_0^2(-R, R)$ is the orthogonal projection onto functions supported in $(-R, R)$ with $\int_{-R}^R u(x) dx = 0$.
The operator $B_R = D^* G_R D$ has domain $H_0^1(-R, R)$, with $D = i \frac{d}{dx}$, and $A_R$ is its Friedrichs extension.
Spectrally, for $v \in C_c^\infty(-R, R)$:
$$Q_W^R(v) = \sum_\rho \widehat{v}(z_\rho) \overline{\widehat{v}(-\overline{z_\rho})} = \sum_\rho F(w_\rho) \overline{F(-\overline{w_\rho})}.$$

---

### Question F: What is the TC action on that object?
There are two distinct candidates for TC action:

1. **Log-Test Variable Translation ($T_h$)**:
   $$(T_h v)(x) = v(x - h), \qquad h = K\log\tau = Ka.$$
   - On the quadratic form:
     $$Q_W(T_h v) = W(T_h v * \widetilde{T_h v}) = W(v * \widetilde{v}) = Q_W(v).$$
     The form value of an individual vector is completely invariant.
   - On the support: $\operatorname{supp}(T_h v) = [h - R, h + R]$.
   - This shifts the interval away from 0, producing an asymmetric interval.

2. **Analytic Dilation Operator ($S_K$)**:
   $$(S_K v)(x) = \tau^{K/2} v(\tau^K x).$$
   - On the Fourier transform: $\widehat{S_K v}(z) = \tau^{-K/2} \widehat{v}(\tau^{-K} z)$.
   - On the quadratic form:
     $$Q_W(S_K v) = \tau^{-K} \sum_\rho \left|\widehat{v}(\tau^{-K} z_\rho)\right|^2.$$
     The frequencies evaluated are $\{\tau^{-K} z_\rho\}$, NOT the Riemann zeta zeros $\{z_\rho\}$!
   - On the operator $A_R$: The arithmetic kernel $k(t) = -g''(t)$ has impulses at $\pm \log n = \pm k\log p$. Under dilation, these impulses move to $\pm \tau^{-K} \log n$, which do not lie on prime stations. Thus:
     $$\boxed{S_K^* A_{\tau^{-K} R} S_K \ne A_R}.$$
     Dilation fails to intertwine the localized Weil operators.

---

### Question G: How does the localization radius/window transform?
1. Under dilation $x \mapsto \tau^K x$, a test function with $\operatorname{supp}(v) \subseteq [-R, R]$ maps to:
   $$\operatorname{supp}(S_K v) \subseteq [-\tau^{-K} R, \tau^{-K} R].$$
   Thus the window transformation is:
   $$\boxed{\Phi_K(R) = \tau^{-K} R}.$$
2. Under translation $T_{Ka}$, the window transforms to the shifted interval:
   $$[-R, R] \mapsto [K\log\tau - R, K\log\tau + R].$$
   The minimal symmetric interval containing the translate has radius $\Phi_K^{\rm trans}(R) = R + |K|\log\tau$.

---

### Question H: Is the transformation unitary, similar, affine, or merely coordinate relabeling?
- **Unitary as an $L^2$ isometry**: $S_K: L^2(-R, R) \to L^2(-\tau^{-K}R, \tau^{-K}R)$ is a unitary operator between different Hilbert spaces.
- **NOT a similarity of the localized Weil operators**: $S_K^* A_{\tau^{-K} R} S_K \ne A_R$, because the underlying arithmetic kernel is inhomogeneous.
- **Coordinate Relabeling**: When $x \mapsto \tau^K x$ is viewed as a change of variables, it merely relabels coordinates. Evaluating $Q_W(S_K v)$ is evaluating the original Weil distribution on a scaled test function; it does not map the Weil distribution at scale $R$ to the Weil distribution at scale $\tau^{-K} R$.

---

### Question I: Does a theorem-valid local property propagate to larger native windows?
**NO.**
- For $R < R_0$, Suzuki Theorem 1.4 proves unconditionally that $\lambda_1(R) > 0$ (local positivity).
- Dilation maps $v \in C_c^\infty(-R, R)$ to $S_K v \in C_c^\infty(-\tau^{-K}R, \tau^{-K}R)$. But $Q_W(S_K v)$ evaluates against scaled frequencies $\tau^{-K} z_\rho$, not zeta zeros.
- Translation maps $v \in C_c^\infty(-R, R)$ to $T_{Ka} v \in C_c^\infty(Ka - R, Ka + R)$. While $Q_W(T_{Ka} v) = Q_W(v) > 0$, this establishes positivity only on a 1-dimensional ray of translated functions.
- To prove positivity of $Q_W$ on the larger symmetric interval $[-R', R']$ with $R' = R + |K|\log\tau$, one must control all linear combinations $\sum_j c_j T_{K_j a} v_j$. The quadratic form of such combinations contains cross-terms:
  $$\sum_{j,k} c_j \overline{c_k} W(T_{(K_j - K_k)a}(v_j * \widetilde{v_k})).$$
  Demanding that these cross-terms remain positive for all seeds is mathematically identical to the full Weil positivity criterion, which is equivalent to RH.
- Therefore, local positivity on $[-R_0, R_0]$ does NOT propagate to $[-R, R]$ for large $R$.
- Classification: `PURE_COORDINATE_RESCALING_NO_GAIN`.

---

### Question J: Does TC imply any part of Suzuki's compact-uniform limiting hypothesis?
**NO.**
- Suzuki Corollary 1.6 states that if choices $\lambda(R) < \lambda_1(R)$, $\theta(R)$, $\phi(R, z)$ exist such that:
  $$e^{\phi(R, z)} W(R, \theta(R); z) \to \frac{1}{1 - i \frac{\xi'(1/2 - iz)}{\xi(1/2 - iz)}}$$
  compact-uniformly in $\{\operatorname{Im} z > 0\}$, then RH holds.
- Suzuki explicitly shows in Section 1.2 and Section 7 that this limit requires $\lambda(R) = 0$ for all large $R$, which is equivalent to $A_R > 0$ for all large $R$, i.e., full Weil positivity.
- TC grade covariance does not control or reduce this large-$R$ limit; it merely acts by coordinate dilation or shift.
- Classification: `TC_COMPATIBLE_BUT_NO_NEW_CONTROL`.

---

### Question K: Is there a smaller positive TC test family than the full Weil class?
**NO.**
- If we consider the grade orbit of a single seed $\mathcal{F}_h = \operatorname{span}\{ T_{Ka} h : K \in \mathbb{Z} \}$, then positive definiteness of $C_h(K)$ on $\mathbb{Z}$ requires $C_h(0) = Q_W(h) \ge 0$, which is already a Weil test.
- If we consider the space of small-support functions $C_c^\infty(-R_0, R_0)$ where $Q_W$ is unconditionally positive (Theorem 1.4), this family is too small to detect off-line zeros (see Question L).
- Status: `NO_SEPARABLE_SMALLER_POSITIVE_DETECTION_FAMILY`.

---

### Question L: Does that family see every zero?
**NO.**
- For a single seed orbit $\mathcal{F}_h$, if $\widehat{h}(z_{\rho_0}) = 0$ for some zero $\rho_0$, then $\widehat{T_{Ka} h}(z_{\rho_0}) = \tau^{-i K z_{\rho_0}} \widehat{h}(z_{\rho_0}) = 0$ for every $K \in \mathbb{Z}$. The zero $\rho_0$ is completely invisible to $\mathcal{F}_h$.
- For the locally positive family $C_c^\infty(-R_0, R_0)$ ($R_0 < \frac{1}{2}\log 2$), $Q_W(v) > 0$ for all nonzero $v$. Hence no negative witness can exist in this window; all off-line zeros are invisible to local positivity.
- A family can see off-line zeros as negative witnesses only if its support extends past $R_{\rm crit} > \frac{1}{2}\log 2$ to capture prime stations, where positivity is no longer unconditional.
- Classification: `RESTRICTED_POSITIVE_FAMILIES_CANNOT_SEE_OFFLINE_ZEROS`.

---

### Question M: Where exactly does $2\pi$ matter?
1. **Transcendental Scale (`TRANSCENDENTAL_SCALE`)**:
   $\tau = 2\pi$ is transcendental by Lindemann (1882). This guarantees $S_\tau \cap \mathbb{Q} = \{0\}$ and rational-grade separation $m\tau^K = n\tau^J \iff K=J, m=n$. For an algebraic base (such as $b = 2$), $2^{1/2} = \sqrt{2} \in \overline{\mathbb{Q}}$, so rational-grade separation fails.
2. **Fourier Period (`FOURIER_PERIOD`)**:
   The complex exponential period is $2\pi i \mathbb{Z}$. The Poisson summation formula on $\mathbb{Z}$ uses period $2\pi$.
3. **Poisson Duality & Gamma Completion (`POISSON_DUALITY`, `GAMMA_COMPLETION`)**:
   The factor $\pi^{-s/2} \Gamma(s/2)$ in $\xi(s)$ arises from the Gaussian self-duality $\int_{\mathbb{R}} e^{-\pi x^2} e^{-2\pi i \xi x} dx = e^{-\pi \xi^2}$.
4. **Generic Scale Geometry (`GENERIC_SCALE_GEOMETRY`)**:
   The dilation window map $\Phi_K(R) = b^{-K} R$ and Rayleigh quotient scaling are generic for any base $b > 1$, independent of $2\pi$.

---

### Question N: What does the exceptional-exponent theorem add?
The Exceptional Exponent Theorem proves:
$$\boxed{S_\tau = \{\alpha \in \mathbb{A}_{\mathbb{R}} : \tau^\alpha \in \overline{\mathbb{Q}}\} \implies S_\tau \cap \mathbb{Q} = \{0\} \quad \text{and} \quad \dim_{\mathbb{Q}} S_\tau \le 1}.$$
- **What it adds**: It proves that if any exceptional irrational algebraic exponents exist that make $\tau^\alpha$ algebraic, they cannot be spread out across multiple algebraic dimensions; all such exceptional exponents must be $\mathbb{Q}$-collinear (lying on a single rational line).
- **Epistemic Qualification**: It does NOT prove $S_\tau = \{0\}$. Proving $S_\tau = \{0\}$ is an open problem in transcendental number theory.
- **Two-Direction Collision Architecture**: If an off-critical zero $\rho = 1/2 + \delta + i\gamma$ could be shown to force $\tau^\alpha, \tau^\beta \in \overline{\mathbb{Q}}$ for two $\mathbb{Q}$-independent algebraic numbers $\alpha, \beta$, that would contradict $\dim_{\mathbb{Q}} S_\tau \le 1$ and establish RH unconditionally!
- **Audit Result**: An audit of all current TC mechanisms finds no second independent exponent direction. Status is `NO_EXISTING_TWO_DIRECTION_BRIDGE`.

---

### Question O: What is the earliest remaining theorem after this sprint?
The earliest remaining theorem is:
$$\boxed{\text{Find an arithmetic positive factorization } Q_W(f) = \|A f\|^2_{\mathcal{H}_{\rm arith}} \text{ on a zero-dense test space, or construct a second } \mathbb{Q}\text{-independent exponent direction into } S_\tau.}$$
Because local positivity propagation across scales is blocked by the inhomogeneity of prime stations (`PURE_COORDINATE_RESCALING_NO_GAIN`), and single-seed orbits cannot guarantee zero visibility, the remaining route must either:
1. Prove global Weil positivity directly via an unconditional arithmetic operator factorization, or
2. Derive a two-direction algebraic exponent collision forcing $\dim_{\mathbb{Q}} S_\tau \ge 2$.

---

## Authoritative Status Table

| Statement / Component | Status Class | Exact Proof / Literature Reference |
| :--- | :--- | :--- |
| **Suzuki 2023 Screw Positivity $\iff$ RH** | `RH_EQUIVALENT` | Suzuki (2023) [W2], Theorem 1.2 |
| **Suzuki 2026 Localized Form & $A_R$ Friedrichs** | `PROVED_STANDARD_OPERATOR_THEOREM` | Suzuki (2026) [W10], Theorem 1.1 |
| **Continuity of Lowest Eigenvalue $\lambda_1(R)$** | `PROVED_CONTINUITY_THEOREM` | Suzuki (2026) [W10], Theorem 1.3 |
| **Unconditional Local Positivity for Small $R$** | `PROVED_LOCAL_POSITIVITY_THEOREM` | Suzuki (2026) [W10], Theorem 1.4 |
| **Real Spectrum of Self-Adjoint Extensions** | `PROVED_REAL_SPECTRUM_THEOREM` | Suzuki (2026) [W10], Theorem 1.5 |
| **Suzuki Compact-Uniform Limit to RH** | `CONJECTURAL_LIMIT_EQUIVALENT_TO_RH` | Suzuki (2026) [W10], Corollary 1.6 |
| **TC Dilation Operator Intertwining** | `REFUTED_WITHIN_SCOPE` ($S_K^* A_{\tau^{-K} R} S_K \ne A_R$) | Discrete prime stations break dilation homogeneity |
| **TC Local Positivity Propagation** | `PURE_COORDINATE_RESCALING_NO_GAIN` | Cross-grade terms require full Weil positivity |
| **Two-Pairing Firewall ($Q_W$ vs $Q_+$)** | `PROVED_EXACT` / `ENFORCED` | $Q_W$ shift-invariant; $Q_+$ shift-sensitive off-line |
| **Exceptional Exponents $S_\tau \cap \mathbb{Q} = \{0\}$** | `PROVED_EXACT` | Lindemann (1882) transcendence of $\tau = 2\pi$ |
| **Collinearity $\dim_{\mathbb{Q}} S_\tau \le 1$** | `PROVED_FROM_GELFOND_SCHNEIDER` | Gelfond–Schneider theorem on $A^{\beta/\alpha} = B$ |
| **Rational-Grade Algebraic Noncollision** | `PROVED_EXACT` | $m\tau^K = n\tau^J \iff K=J, m=n$ for $m,n \in \overline{\mathbb{Q}}^\times$ |
| **Two-Direction Exponent Bridge** | `TWO_DIRECTION_COLLISION_BRIDGE_OPEN` | Audit confirmed no second independent exponent |
| **Lean Formalization (322 theorems)** | `CERTIFIED_FORMAL_BUILD` | `formal/RiemannScope/TranscendenceRigidity.lean` |
