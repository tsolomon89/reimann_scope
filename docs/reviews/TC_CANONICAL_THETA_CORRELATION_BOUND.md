# Canonical Theta Correlation Bound, Arithmetic–Fourier Positive Factorization, Admissible Cross-Grade Compatibility, the Prime-Shift Quadratic Form, Prime-by-Prime Möbius Recovery & Single-Observable Common-Referent Audit (`EPIC-TC-042` / `TASK-TC-042` / `TASK-TC-042R` / `TASK-TC-042R2` / `TASK-TC-042F` / `TASK-TC-043` / `TASK-TC-043R` / `TASK-TC-044` / `TASK-TC-045` / `TASK-TC-045R` / `TASK-TC-045R2` / `TASK-TC-046` / `TASK-TC-047` / `TASK-TC-048`)

## 1. Executive Summary & Status Separation

This document records the complete mathematical derivation, seed defect repair, closed-form multiplicative autocorrelation theorem, exact rational Bernstein weighted kernel envelopes, fixed-seed Riemann Hypothesis equivalence proof, certified arbitrary-precision evaluations, `TASK-TC-042R` and `TASK-TC-042R2` certification/formalization repairs, $\tau$-scaling controls, Lean 4 formalization, arithmetic proof attempts (`SUBGATE-TC-042A` and `SUBGATE-TC-042B`), the **`TASK-TC-042F` Arithmetic–Fourier Positive Factorization** (with bounded reconciliation), **`TASK-TC-043` / `TASK-TC-043R` Admissible Cross-Grade Compatibility & Signed Cross-Grade Cancellation Investigation**, **`TASK-TC-044` Arithmetic Cross-Grade Compatibility, the Prime-Shift Quadratic Form $D_N(f)$, and the Divisor-Aggregated Prime-Shift Functional $W_{\log}(X)$**, **`TASK-TC-045` / `TASK-TC-045R` / `TASK-TC-045R2` Cross-Grade Compatibility, Möbius Recovery of the Actual Arithmetic Profile, and Mathematical Claim / Certificate Repairs**, **`TASK-TC-046` Prime-by-Prime Möbius Recovery and Arithmetic Cross-Grade Compatibility**, **`TASK-TC-047` Common-Referent Observable from Actual Prime/Theta Data and Required Integer-Layer Membership**, and **`TASK-TC-048` A Single Prime/Theta Observable for the Common-Referent Collision Contract** of the complete Weil pairing $Q_\tau(f, g) = W_\xi(f * g^*)$ for **`EPIC-TC-042`**:

$$
C_\tau(0) \ge 0, \qquad |C_\tau(K)| \le C_\tau(0) \quad \forall K \in \overline{\mathbb{Q}} \cap \mathbb{R}, \qquad \tau = 2\pi,
$$

where $C_\tau(K) := W_\xi(h_K)$ is the completed Riemann explicit-formula functional evaluated on the grade-shifted multiplicative autocorrelation $h_K := (T_K \psi_\tau) * \psi_\tau^*$ of the fixed squared pole-regularized theta state $\psi_\tau(x) = x^{1/2}\Phi_1^{(2)}(x)$.

| Dimension | Classification / Status | Scope & Evidence |
| :--- | :--- | :--- |
| **Implementation Status** | `IMPLEMENTED_AND_VERIFIED` | [`tc/canonical_theta_correlation_bound.py`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py), [`tc/prime_euler_moebius_recovery.py`](file:///c:/Development/Projects/reimann_scope/tc/prime_euler_moebius_recovery.py), [`tests/test_tc_canonical_theta_correlation_bound.py`](file:///c:/Development/Projects/reimann_scope/tests/test_tc_canonical_theta_correlation_bound.py), [`tests/test_tc_prime_euler_moebius_recovery.py`](file:///c:/Development/Projects/reimann_scope/tests/test_tc_prime_euler_moebius_recovery.py), [`data/tc_canonical_theta_correlation_bound.json`](file:///c:/Development/Projects/reimann_scope/data/tc_canonical_theta_correlation_bound.json) |
| **Seed Defect Repair (`Section 2`)** | `SEED_DEFECT_REPRODUCED_AND_REPAIRED` | Exact operator derivation $\Phi_t^{(2)}(x) = P(D)^2 G_t(x) = t^{1/4}(r^4 - 7r^3 + \frac{41}{4}r^2 - \frac{9}{4}r)e^{-r}$, repairing the `TC-036R` display typo $r^4 - 6r^3 + \frac{45}{8}r^2 - \frac{3}{8}r$ |
| **Closed-Form Autocorrelation & Bernstein Envelopes (`Section 3`)** | `CLOSED_FORM_AUTOCORRELATION_PROVED` / `BERNSTEIN_KERNEL_ENVELOPES_EXACT_RATIONAL_CERTIFIED` | Exact rational-algebraic formula $h_K(x) = h_0(\tau^K x)$ in $W_\alpha = (\alpha + \alpha^{-1})^2$ (distinct from the prime wavelet sum $W(X)$), eighth-order Euler differential representation, and exact rational Bernstein polynomial certificates for $|g^{(m)}(v)| \le |g^{(m)}(0)| 2^{5/2} (2\cosh v)^{-5/2}$ ($m \in \{0,2,4,6,8\}$) and $|\tilde{h}_0(\alpha)| \le \frac{1032993}{65536}(\alpha+\alpha^{-1})^{-5/2}$ |
| **Fixed-Seed RH Equivalence (`Sections 4 & 5`)** | `FIXED_SEED_RH_EQUIVALENCE_PROVED` | Complete Laplace-resolvent proof that $C_\tau(0) \ge 0 \wedge |C_\tau(K)| \le C_\tau(0)\;(\forall K \in \overline{\mathbb{Q}}\cap\mathbb{R}) \Longleftrightarrow \text{RH}$ (and more generally $\exists M < \infty : |C_\tau(K)| \le M \Longleftrightarrow \text{RH}$) |
| **Numerical Certification (`Sections 5 & 6`, repaired in `TASK-TC-042R` / `TASK-TC-042R2` / `TASK-TC-042F` / `TASK-TC-043` / `TASK-TC-045` / `TASK-TC-045R` / `TASK-TC-045R2` / `TASK-TC-046` / `TASK-TC-046R2`)** | `FINITE_GRID_CORRELATION_BOUND_CERTIFIED` | 256-bit FLINT/Arb ball enclosures with outward-rounded decimal endpoint strings (`lower_dec`, `upper_dec`), outward-rounded float radii (`rad_float_outward`), and `arb.str(40, radius=True)` round-trip verified enclosures across 14 discrete grades and across all exported Arb balls in `section_13` (`26` balls), `section_14` (`122` balls), and `section_15` (`551` balls; `live_original_count_matches_enumerated_total == True`), 512-arc Cauchy circle Taylor remainder bound, `analytic=analytic` branch-cut checking, outward-rounded `flint.arb_mat.det()` Sylvester Gram minors, and derived uniform archimedean integral bound $\le 4.448357 < 4.95$ ($|W_{\mathrm{arch}}(h_K)| \le 5.994279\;\forall K\in\mathbb{R}$) |
| **Local Origin Concavity (`Section 5.3`, repaired in `TASK-TC-042R` / `TASK-TC-042R2`)** | `LOCAL_ORIGIN_CONCAVITY_CERTIFIED` | Certified $C_\tau(0) > 0$, $C_\tau'(0) = 0$, $C_\tau''(0) \approx -0.641739 < 0$, $C_\tau^{(4)}(0) \approx +433.541309 > 0$, scoped sixth-derivative bound $\sup_{|K|\le 0.08}|C_\tau^{(6)}(K)| \le M_6^{\mathrm{arith}} = 27971954.786589753$, and certified exact-rational local intervals $0 < |K| \le 1/20 = 0.05$ for $|C_\tau(K)| < C_\tau(0)$ and $0 \le |K| \le 9/200 = 0.045$ for $C_\tau(K) > 0$ (100% zero-free arithmetic route) and $0 < |K| \le 17/250 = 0.068$ for $|C_\tau(K)| < C_\tau(0)$ and $0 \le |K| \le 1/20 = 0.05$ for $C_\tau(K) > 0$ (unconditional spectral-tail route) |
| **Stieltjes Multiscale Reduction (`Section 7`, repaired in `TASK-TC-042R2` / `TASK-TC-042F`)** | `STIELTJES_IDENTITY_REPAIRED_AND_CERTIFIED` | Removed the extraneous $X^{-1/2}$ factor from the $x$-variable integral, fixed the denominator exponent of $(D_\alpha h_0)(\alpha)$ to $(\alpha+\alpha^{-1})^{19/2}$, certified both Form (A) (in $x$) and Form (B) (in $\alpha = x/X$) at $B = 50$ for $X \in \{1, 4, 100\}$ to $< 3 \times 10^{-31}$, derived the exact $[4, \infty)$ incomplete-Gamma tail bound for `_f_conv_25` at $X = 4$ (`finite_sum_convolution_enclosures_overlap == True`), and extended the empirical $\operatorname{sech}^2$ grid diagnostic cutoff to $25000 \ge 5 e^{8.5} \approx 24574$ |
| **Arithmetic–Fourier Positive Factorization (`Section 9`, `TASK-TC-042F`, reconciled in `TASK-TC-043`)** | `POLE_PNT_ARCHIMEDEAN_CANCELLATION_PROVED_DEFECT_ISOLATED` | Constructed and tested Attempt A ($A_\tau^A, R_\tau^A$) and Attempt B ($A_\tau^B, R_\tau^B$) for the complete Weil pairing $Q_\tau(f, g) = W_\xi(f * g^*)$; proved unconditional reflected grade invariance $Q_\tau(T_K f, T_K g) = Q_\tau(f, g)$, the signature-$(1,1)$ hyperbolic off-line pair block $q(u, v) = 2\operatorname{Re}(u\bar{v})$ with complex conjugate-inverse invariance $q(\lambda u, \bar{\lambda}^{-1} v) = q(u, v)$, quotient unitary grade transport $U_K(A_\tau f) = A_\tau(T_K f)$, and **Universal Pole–PNT–Archimedean Cancellation** across all of $\mathcal{D}$, isolating the exact defect $R_\tau^B(f, g) = -c_\tau^B\langle f, g\rangle_{L^2(d^\times y)} - \int_1^\infty E(x)x^{-3/2}\widetilde{\Phi}_{f,g}(x)\,dx$ ($c_\tau^B = c_\tau - 2 = 3.3721834192256654 \pm 3.92 \times 10^{-56}$) and demonstrating with complete outward Arb error bounds that on $\psi_\tau$ the smooth part $\|A_\tau^B\psi_\tau\|^2 - c_\tau^B\|\psi_\tau\|^2 = -1.0824296878 < 0$ is strictly negative while the signed Chebyshev prime-error correlation $+1.0833801676 > 0$ rescues positivity $C_\tau(0) = +0.0009504798 > 0$ |
| **Admissible Cross-Grade Compatibility & Signed Cancellation (`Section 10`, `TASK-TC-043` / `TASK-TC-043R`)** | `TRANSFER_CANCELLATION_AND_COERCIVE_SEMIBOUNDEDNESS_PROVED_MOVING_SCALE_OBSTRUCTION_ISOLATED` / `TC043R_REPAIRS_CERTIFIED_AND_SIGNED_CANCELLATION_INVESTIGATED` | Formulated the cross-grade compatibility specification on $\mathcal{S}_\tau = \operatorname{span}_{\mathbb{C}}\{T_K \psi_\tau : K \in \overline{\mathbb{Q}}\cap\mathbb{R}\}$; proved complex zero ray collinearity and Lindemann–Weierstrass noncollision for nonzero rational grade differences; audited synthetic off-critical quartet controls; proved the **Attempt B Plancherel Multiplier Identity** $\mu_\tau^B(t) = \operatorname{Re}\psi_{\mathrm{digamma}}(\frac{5}{4} + \frac{it}{2}) - \log\pi - 2$ (certified unique positive root $t_*^B \in [46.4061555, 46.4061557]$), the **Exact Pole-Vanishing Transfer Decomposition** $B_{\mathrm{transfer}}(f) = 2\|f\|_{L^2}^2 - J(f, f) = 4\|R_0 f\|_{L^2}^2 - 2\|f\|_{L^2}^2$ cancelling $89.50\%$ ($+0.9687652063 / 1.0824296878$) of the smooth deficit on $\psi_\tau$ (structural accounting), the **Coercive Norm-Shifted Semiboundedness Reduction** on $\mathcal{H}_{\tau, \mu_0}^B = \mathcal{H}_\tau^B \oplus L^2(\mu_0 d^\times y)$ for normalized $f_\pm^{(K)} = (\psi_\tau \pm T_K\psi_\tau)/\sqrt{2}$, the **Repaired Unsigned Majorant Growth Obstruction** ($A_E(X) \le M_\omega(X)$, $M_\omega(X) \ge c_0\sqrt{X}\,\omega(2X)$, $c_0 = 1.7456980946 < C_{\mathrm{abs}} = 2.4863319706$), and **Candidate IV (`TASK-TC-043R`)**: zero-moment subtracted increment identity $I(X) = I_{\mathrm{inc}}(X) + B_{\mathrm{zm}}(X)$, chordal prime-power Stieltjes equivalence $I_{\mathrm{inc}}(X) = I_{\mathrm{chord}}(X) - I_{\mathrm{drift}}(X) = W(X) - \frac{\psi(X)}{X}B_{\mathrm{boundary}}(X) = I(X) - e(X)B_{\mathrm{boundary}}(X)$, and Chebyshev primitive transfer $e_1(x) = E_1(x)/x^2$ |
| **Prime-Shift Quadratic Form & Divisor-Aggregated $W_{\log}(X)$ (`Section 11`, `TASK-TC-044`)** | `PRIME_SHIFT_QUADRATIC_FORM_DECOMPOSED_DIVISOR_AGGREGATED_W_LOG_UNCONDITIONALLY_BOUNDED_MOEBIUS_OBSTRUCTION_ISOLATED` | Expanded the positive prime-shift quadratic form $D_N(f) = \sum_{2\le n\le N} w_n\|(I-S_n)f\|_{L^2}^2 = 2L_N\|f\|_{L^2}^2 - W_{\mathrm{prime}, N}(f * f^*)$, proved its exact relation to $Q_\tau(f,f)$ and $P_E(f)$ and why $D_N(f) \ge 0$ alone yields only $-2L_N\|f\|_{L^2}^2 \to -\infty$, proved **unconditionally** (without RH) that the divisor-aggregated functional $W_{\log}(X) := \sum_{m=1}^\infty m^{-1/2}W(X/m) = \sum_{k=2}^\infty \frac{\log k}{\sqrt{k}}h_0(k/X)$ satisfies $|W_{\log}(X)| \le \frac{30731}{98304}X^{-5/2} + X^{-1/2}\bigl(\frac{1}{2}M_{\widetilde{h},0}^{(-3/2)}\log X + M_{\widetilde{h},0}^{(-3/2)} + \frac{1}{2}M_{\widetilde{h},\log}^{(-3/2)}\bigr) \le 3.34901$ ($= O(X^{-1/2}\log(X+2)) \to 0$) for all $X \ge 1$ via $H_0(1/2) = H_0'(1/2) = 0$, derived the exact Möbius inversion $W(X) = \sum_{m=1}^\infty \frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$, and isolated the **Möbius De-Aggregation Cancellation Lemma** as the next unproved arithmetic premise |
| **Cross-Grade Compatibility & Möbius Recovery (`Section 12`, `TASK-TC-045` / `TASK-TC-045R` / `TASK-TC-045R2`)** | `MIXED_GRADE_PAIRING_POLARIZED_MERTENS_STIELTJES_REMAINDER_ISOLATED_CLAIMS_AND_CERTIFICATES_REPAIRED` | Repaired `TC-044` Mellin strip derivation ($1/2 < \operatorname{Re}(z) < 5/2$ Fubini–Tonelli interchange, holomorphic continuation of $-H_0(z)\zeta'(z+1/2)$ on the open kernel strip $|\operatorname{Re}(z)| < 5/2$ where $H_0(1/2) = H_0'(1/2) = H_0''(1/2) = 0$ cancels the double pole of $-\zeta'(z+1/2)$, global meromorphic continuation on $\mathbb{C}$ with simple poles from $H_0(z)$ at $z = \pm(2k+1/2)$ ($k \ge 1$) and residue $\operatorname*{Res}_{z=5/2}[-H_0(z)\zeta'(z+1/2)] = \frac{81}{64}(-\zeta'(3)) = +0.2507535262 \ne 0$, Möbius $1/\zeta(z+1/2)$ denominator restoration, and Euler–Maclaurin pole-subtracted regularization on isolated synthetic modes) and outward-rounded decimal/float Arb serialization (`serialize_arb_certified`, `verify_serialized_arb_roundtrip`, `verify_all_serialized_arb_in_tree` across all `26` balls in `section_13` and `122` balls in `section_14`); repaired in `TASK-TC-045R` / `TASK-TC-045R2` the false uniform norm floors on $f_\pm^{(K)}$ ($\|f_-^{(K)}\|_{L^2}^2 = h_0(1) - h_0(\tau^{|K|}) \to 0$ as $K \to 0$, and at $K = \pm 1/4$, $\|f_+^{(\pm 1/4)}\|_{L^2}^2 = h_0(1) + h_0(\tau^{1/4}) = 0.243250897826609 \in (0.2432, 0.2433)$), the false transfer bound `0.633039` (proving the Plancherel bound $|B_{\mathrm{transfer}}(f)| \le 2\|f\|_{L^2}^2$, $|B_{\mathrm{transfer}}(f_\pm^{(K)})| \le 4h_0(1) = 1.9894499352 < 1.98945$, and $|B_{\mathrm{transfer}}(T_K\psi_\tau, T_L\psi_\tau)| \le 2h_0(1) = 0.9947249676 < 0.994725$), and the direct mixed-grade implication chain through $C_\tau(K-L) = Q_\tau(T_K\psi_\tau, T_L\psi_\tau) = B_{\mathrm{known}}(K, L) - R_\mu(\tau^{|K-L|})$ (`|B_known(K, L)| <= 9.27739781 < 9.4468` via the spatial archimedean bound `5.464660`, or `<= 7.07942813 < 7.07943` via the Attempt B Cauchy–Schwarz + Plancherel transfer bound `3.26669033`); proved $|W_{\log}(u)| \le C_{\log,0}\,u^{5/2}$ ($C_{\log,0} = \frac{92193}{32768}(-\zeta'(3)) \le 0.55742959$) for all $u > 0$, uniform convergence of $R_\mu(X)$ on compact intervals $[a, b] \subset (0, \infty)$, continuity of $R_\mu(X)$ and $W(X)$ on $(0, \infty)$, $\sup_{K\in\mathbb{A}_{\mathbb{R}}}|R_\mu(\tau^{|K|})| = \sup_{X\ge 1}|R_\mu(X)|$, simultaneous-grade Toeplitz counterexample control, and the exact Mertens Stieltjes representation $R_\mu(X) = X^{-1/2}\int_0^{X/2} M_{\ge 2}(X/u)\phi_{\log}'(u)\,du$, isolating the **Smooth-Kernel Mertens / Möbius Cancellation Lemma** (`SUBGATE-TC-043A`) |
| **Prime-by-Prime Möbius Recovery (`Section 13`, `TASK-TC-046` / `TASK-TC-046R2`)** | `FINITE_PRIME_EULER_INVERSION_PROVED_COUPLED_CUTOFF_REDUCTION_CERTIFIED_UNIFORM_REMAINDER_OPEN` | Constructed finite-prime Euler inversion $W_y(X) := \sum_{m \mid P_y}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m) = \prod_{p\le y}(I - p^{-1/2}D_p)W_{\log}(X) = \sum_{n\ge 2}\frac{\lambda_y(n)}{\sqrt{n}}h_0(n/X)$ ($P_y = \prod_{p\le y}p$, $\mu_y(m) = \mu(m)\mathbf{1}_{m\mid P_y}$, $\lambda_y = \mu_y * \log$) on the ambient space $\mathcal{F}_{5/2} \subset C((0, \infty))$ before restricting to admissible grade scales $X = \tau^{|K-L|}$ ($K, L \in \mathbb{A}_{\mathbb{R}}$); proved the closed-form prime-power classification ($\lambda_y(n) = \log n$ if $\omega_{\le y}(n)=0$, $\log p$ if $\omega_{\le y}(n)=1$, $0$ if $\omega_{\le y}(n)\ge 2$), the exact summatory factorial identity $L_y(x) = \sum_{d\mid P_y, d\le x}\mu(d)\log(\lfloor x/d\rfloor!)$, and the exact agreement window $\lambda_y(n) = \Lambda(n)$ for all $2 \le n < 2 q_{>y}$ ($q_{>y} = \min\{p \text{ prime} : p > y\}$, first discrepancy $\Delta_y(2q_{>y}) = \log 2 > 0$); proved the critical-line Mellin/Fourier identity $W_y(X) = -\frac{1}{\tau}\int_{-\infty}^\infty E_y(it)H_0(it)\zeta'(1/2+it)X^{it}\,dt$ and Euler-sieved seed Gram bound $\sup_{X>0}|W_y(X)| \le \|\Psi_y\|_{L^2(d^\times x)} N_{\zeta',\tau}$, quantifying both the controlled-width low-frequency interval lower bound $\inf_{t\in I_y}|E_y(it)|^2 = |E_y(i t_{y,-})|^2 = \exp\bigl[(4\cos(\tau/16)+o(1))\sqrt{y}/\log y\bigr]$ ($4\cos(\tau/16) = 2\sqrt{2+\sqrt{2}} \approx 3.695518130045147$, proved via PNT partial summation of the full prime product while refuting the false subproduct inequality at $y = 210$ where $3.3605057481 < 18.2536118944$) on $I_y = [\frac{7\tau}{16\log y}, \frac{\tau}{2\log y}]$ ($|I_y| = \frac{\tau}{16\log y}$) together with Weierstrass product local monotonicity of $H_0(it)$ on $[0, 1]$ ($y \ge 24$, plus 64-subinterval Arb certification on $[0, t_{2,+}]$ for $y \in \{2, 5, 11\}$ and global non-monotonicity $H_0(5i) < H_0(i t_{2,+})$, $H_0(20i) < H_0(0)$), which forces $\|\Psi_y\|_{L^2(d^\times x)}^2 \ge \frac{H_0(0)}{8\log y}|E_y(i t_{y,-})|^2 \to +\infty$ as $y \to \infty$ (establishing failure of the unsplit critical-line Cauchy–Schwarz/Gram-norm bound without refuting boundedness of $W_{M(X)}(X)$ or the concurrent-grade hypothesis), and the horizon collapse of the $m \le M(X)$ divisor sum to $W_{\log}(X) + R_{\mu,M(X)}(X)$ for $y \ge M(X)$; proved $|W(X) - W_y(X)| \le \frac{C_{\log,0}X^{5/2}}{2M^2}$ for $y \ge M \ge \max(2, X)$ and $|W(X) - W_{M(X)}(X)| \le \frac{1}{2}C_{\log,0} = 0.2787147936 < 0.278715$ at $y = M(X) = \lceil\max(2, X^{5/4})\rceil$ (computed as a certified safe integer cutoff directly from the Arb ball enclosure of $(X^5)^{1/4}$ without `float` rounding, with certified regression at $X = 16 \pm 10^{-30}$), establishing $\sup_{X\ge 1}|W_{M(X)}(X)| < \infty \iff \sup_{X\ge 1}|R_{\mu, M(X)}(X)| < \infty \iff \sup_{X\ge 1}|R_\mu(X)| < \infty$ (`SUBGATE-TC-043A`, whereas at $N = \lfloor X\rfloor$ the available small-scale tail estimate grows as $O(\sqrt{X})$) |
| **Common-Referent Prime/Theta Bridge & Single-Observable Collision Audit (`Section 14` & `Section 15`, `TASK-TC-047` / `TASK-TC-048`)** | `COMMON_REFERENT_PRIME_THETA_INTEGER_LAYER_MEMBERSHIP_PROVED_AND_CERTIFIED_SUBGATE_OPEN` / `COUPLED_CUTOFF_JUMP_FORMULA_AND_SINGLE_OBSERVABLE_CANDIDATE_AUDIT_PROVED_COVARIANCE_INVARIANCE_DISCRETENESS_TRILEMMA_ISOLATED_SUBGATE_OPEN` | Constructed $\mathcal{N}_y(x) = \prod_{d\mid P_y, d\le x}(\lfloor x/d\rfloor!)^{\mu(d)} = \prod_{n\le x}m_y(n) \in \mathbb{Z}_{\ge 1}$ and $\mathcal{A}_{K,y}(x) = \mathcal{N}_y(x)\tau^K \in L_K^\times = \tau^K(\mathbb{Z}\setminus\{0\})$ (`CR2`), proved its Chebyshev LCM agreement window $1 \le x < 2 q_{>y}$ and first discrepancy $\mathcal{N}_y(2q_{>y}) = 2\operatorname{lcm}(1, \dots, 2q_{>y})$, and proved the logarithmic-jump reconstruction $W_y(\tau^{K-J}) = \sum_{n\ge 2}\log(\mathcal{A}_{K,y}(n)/\mathcal{A}_{K,y}(n-1))n^{-1/2}h_0(\Phi_J(n)/\Phi_K(1))$ under the explicit lower-endpoint convention $\mathcal{A}_{K,y}(x) = \tau^K$ on $(0, 2)$ (zero atom at $x = 1$); reconciled in `TASK-TC-048` that $\tau^{-K}\mathcal{A}_{K,y}(x) = \mathcal{N}_y(x)$ is unit-converted coordinate recovery (whereas raw $\mathcal{A}_{K,y}(x) \ne \mathcal{A}_{J,y}(x)$ for $K \ne J$), proved the exact right-hand jump formula $F(X_0^+) - F(X_0) = -p^{-1/2}W_{p^-}(X_0/p)$ of $F(X) = W_{M(X)}(X)$ at $X_0 = (p-1)^{4/5}$ (certified strictly positive for $p \in \{3, 5, 7, 11, 13, 17, 19, 23\}$ and proved $> 0$ for all $p$ with $u_p \le 2/9$), corrected the dense-grade-to-all-$X$ extension to use continuity of $W(X)$ plus $|F(X) - W(X)| \le \frac{1}{2}C_{\log,0} < 0.278715$, and audited Candidate 1 ($D_{K,y}^{(1)}(\rho_K) = c_K(\rho_K)\mathcal{N}_y(X_K)\tau^K$) and Candidate 2 ($D_K^{(2\mathrm{A})}(\rho_K) = |H_0(\delta+i\gamma)|^2(\tau^\delta+\tau^{-\delta}-2)$ and $D_{K,y}^{(2\mathrm{B})}(\rho_K) = W_y(\tau^{1+|\delta|}) - W_y(\tau)$), isolating the **Covariance–Invariance–Discreteness Trilemma** while keeping `SUBGATE-TC-043A` `OPEN` |
| **Universal Arithmetic Inequality (`Section 7`, `Section 10`, `Section 11`, `Section 12`, `Section 13`, `Section 14` & `Section 15`)** | `UNIVERSAL_ARITHMETIC_CORRELATION_BOUND_OPEN` | Isolated as `SUBGATE-TC-042A`, `SUBGATE-TC-042B`, and `SUBGATE-TC-043A`: $\exists M < \infty \; \forall X \ge 1 : |R_\mu(X)| := |\sum_{m\ge 2}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)| \le M$ (equivalently $\sup_{X\ge 1}|W_{M(X)}(X)| < \infty$ for $M(X) = \lceil\max(2, X^{5/4})\rceil$) |
| **Formalization Coverage (`Section 8`, expanded in `TASK-TC-042R2`, `TASK-TC-042F`, `TASK-TC-043`, `TASK-TC-043R`, `TASK-TC-044`, `TASK-TC-045`, `TASK-TC-045R`, `TASK-TC-046`, `TASK-TC-047` & `TASK-TC-048`)** | `FORMALIZED_IN_LEAN4_ZERO_SORRY` | [`formal/RiemannScope/CanonicalThetaCorrelationBound.lean`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean): **30 definitions**, **49 theorems**, 0 `sorry`, 0 `admit` (including `prime_euler_multiplicative_integrality_and_grade_layer_membership`, `common_referent_integer_layer_bridge_and_station_ratio_identity`, `coupled_cutoff_prime_step_jump_and_dense_comparison_extension`, and `single_observable_common_referent_candidate_audit_and_trilemma`; Lean scope explicitly distinguished from paper factorial-divisor proofs and finite computational checks) |
| **Independent Review Status** | `AWAITING_INDEPENDENT_REVIEW` | Mathematical status separated from structural and test execution |

---

## 2. Exact Seed Object, Operator Polynomial Repair, and Mellin Transform $F_\tau(s)$

### 2.1 Operator Definition and Reproduction of the `TC-036R` Display Defect

Let $\tau = 2\pi$, $L = \log \tau = \log(2\pi)$, $D = t \frac{d}{dt}$, and
$$
G_t(x) = t^{1/4} \exp\!\left(-\frac{\tau}{2} t x^2\right) = t^{1/4} e^{-r}, \qquad r := \frac{\tau}{2} t x^2 = \pi t x^2 \quad (x > 0, \; t > 0),
$$
$$
P(D) := D^2 - \frac{1}{16} = \left(D - \frac{1}{4}\right)\left(D + \frac{1}{4}\right), \qquad \Phi_t^{(2)}(x) := P(D)^2 G_t(x), \qquad \psi_\tau(x) := x^{1/2} \Phi_1^{(2)}(x).
$$

Because $D(r) = r$ and $D(e^{-r}) = -r e^{-r}$, the action of $D = t\frac{d}{dt}$ on $t^{1/4} p(r) e^{-r}$ for any polynomial $p(r)$ is given by the algebraic step operator
$$
D\bigl(t^{1/4} p(r) e^{-r}\bigr) = t^{1/4} \left[\left(\frac{1}{4} - r\right)p(r) + r p'(r)\right] e^{-r}.
$$

Applying $P(D) = D^2 - \frac{1}{16}$ twice yields:
1. **First application ($p_0(r) = 1$)**:
   - $D(t^{1/4} e^{-r}) = t^{1/4}(\frac{1}{4} - r)e^{-r}$,
   - $D^2(t^{1/4} e^{-r}) = t^{1/4}\bigl((\frac{1}{4} - r)^2 - r\bigr)e^{-r} = t^{1/4}(r^2 - \frac{3}{2}r + \frac{1}{16})e^{-r}$,
   - $P(D)G_t(x) = t^{1/4} P_1(r) e^{-r}$ with
     $$
     P_1(r) = r^2 - \frac{3}{2}r.
     $$
2. **Second application ($P_1(r) = r^2 - \frac{3}{2}r$, $P_1'(r) = 2r - \frac{3}{2}$)**:
   - $D(t^{1/4} P_1(r) e^{-r}) = t^{1/4}\bigl(-r^3 + \frac{15}{4}r^2 - \frac{15}{8}r\bigr)e^{-r}$,
   - $D^2(t^{1/4} P_1(r) e^{-r}) = t^{1/4}\bigl(r^4 - 7r^3 + \frac{83}{8}r^2 - \frac{75}{32}r\bigr)e^{-r}$,
   - Subtracting $\frac{1}{16} P_1(r) = \frac{1}{16}r^2 - \frac{3}{32}r$:
     $$
     \boxed{\Phi_t^{(2)}(x) = P(D)^2 G_t(x) = t^{1/4} P_2(r) e^{-r}, \qquad P_2(r) = r^4 - 7r^3 + \frac{41}{4}r^2 - \frac{9}{4}r.}
     $$

### 2.2 Rising-Pochhammer Mellin Proof and Diagnosis of the Defective Polynomial

For any polynomial $\sum_{j=1}^4 p_j r^j$ with $r = (\tau/2) x^2$ at $t = 1$, substituting $x = ((\tau/2)^{-1} r)^{1/2}$ ($dx/x = \frac{1}{2} dr/r$) gives
$$
\int_0^\infty r^j e^{-r} x^{s-1}\,dx = \frac{1}{2}\left(\frac{\tau}{2}\right)^{-s/2} \Gamma\!\left(\frac{s}{2} + j\right) = \frac{1}{2}\left(\frac{\tau}{2}\right)^{-s/2} \Gamma\!\left(\frac{s}{2}\right) \left(\frac{s}{2}\right)_j,
$$
where $(u)_j = u(u+1)\cdots(u+j-1)$ is the rising Pochhammer symbol.
- For the **exact** coefficients $(p_1, p_2, p_3, p_4) = (-9/4, 41/4, -7, 1)$ with $u = s/2$:
  $$
  \sum_{j=1}^4 p_j (u)_j = -\frac{9}{4}u + \frac{41}{4}u(u+1) - 7u(u+1)(u+2) + u(u+1)(u+2)(u+3) = u^2\left(u - \frac{1}{2}\right)^2 = \frac{s^2(s-1)^2}{16},
  $$
  so multiplying by $\frac{1}{2}(\tau/2)^{-s/2}\Gamma(s/2)$ yields
  $$
  \boxed{F_\tau(s) := \int_0^\infty \Phi_1^{(2)}(x) x^{s-1}\,dx = \frac{s^2(s-1)^2}{32}\left(\frac{\tau}{2}\right)^{-s/2}\Gamma\!\left(\frac{s}{2}\right), \qquad \widehat{\psi_\tau}(z) = F_\tau\!\left(\frac{1}{2} + z\right).}
  $$
- By contrast, for the `TC-036R` display typo $(p_1^{\mathrm{def}}, p_2^{\mathrm{def}}, p_3^{\mathrm{def}}, p_4^{\mathrm{def}}) = (-3/8, 45/8, -6, 1)$:
  $$
  \sum_{j=1}^4 p_j^{\mathrm{def}} \left(\frac{s}{2}\right)_j = \frac{s^4}{16} - \frac{11}{32}s^2 - \frac{3}{8}s,
  $$
  which at $s = 1$ evaluates to $\frac{1}{16} - \frac{11}{32} - \frac{3}{8} = -\frac{21}{32} \ne 0$, failing to annihilate the $s = 1$ pole! Both [`tc/modular_theta_conductor_curvature.py`](file:///c:/Development/Projects/reimann_scope/tc/modular_theta_conductor_curvature.py) and [`docs/reviews/TC_MODULAR_THETA_CONDUCTOR_CURVATURE.md`](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_MODULAR_THETA_CONDUCTOR_CURVATURE.md) have been repaired to use $r^4 - 7r^3 + \frac{41}{4}r^2 - \frac{9}{4}r$, and this identity is formally verified in Lean 4 theorems `seed_second_order_spatial_polynomial`, `seed_mellin_pochhammer_polynomial_identity`, and `defective_seed_mellin_endpoint_nonvanishing`.

### 2.3 Analytic Strip, Endpoint Values, and Open-Strip Nonvanishing

1. **Holomorphy Strip**: Because $\Gamma(s/2)$ has simple poles at $s = 0, -2, -4, \dots$ and the double factor $s^2$ cancels the simple pole at $s = 0$, $F_\tau(s)$ extends holomorphically to $\operatorname{Re}(s) > -2$ (equivalently $\widehat{\psi_\tau}(z)$ is holomorphic on $\operatorname{Re}(z) > -5/2$).
2. **Removable Endpoint Values and Exact Vanishing Orders at $s = 0$, $s = 1$, and $z = \pm 1/2$**:
   - Since $\Gamma(s/2) = \frac{2}{s} - \gamma_E + O(s)$ has a **simple pole** at $s = 0$, one factor of $s$ in $s^2$ cancels the gamma pole and leaves a **simple zero** (order $1$) at $s = 0$: $F_\tau(s) = \frac{s(s-1)^2}{32}(\tau/2)^{-s/2}(s\Gamma(s/2)) = \frac{1}{16}s + O(s^2)$ as $s \to 0$, so $F_\tau(0) = 0$ and $F_\tau'(0) = \frac{1}{16} \ne 0$.
   - At $s = 1$, $\Gamma(1/2) = \sqrt{\pi}$ and $(\tau/2)^{-1/2} = \pi^{-1/2}$ cancel ($\pi^{-1/2}\Gamma(1/2) = 1$), while $(s-1)^2$ vanishes to second order, so $F_\tau(s) = \frac{1}{32}(s-1)^2 + O((s-1)^3)$ has a **double zero** (order $2$) at $s = 1$ ($F_\tau(1) = F_\tau'(1) = 0$, $F_\tau''(1) = \frac{1}{16} = 0.0625 \ne 0$).
   - Consequently, the autocorrelation Mellin transform $H_0(z) = F_\tau(\frac{1}{2}+z)F_\tau(\frac{1}{2}-z)$ vanishes to **triple order** ($1 + 2 = 3$) at $z = \pm 1/2$ (not order $4$: in $h_0(\alpha) = \frac{1}{512}(D_\alpha^2 - 1/4)^4(\alpha + \alpha^{-1})^{-1/2}$, the base kernel $(\alpha + \alpha^{-1})^{-1/2}$ has simple Mellin poles at $z = \pm 1/2$ via $\int_0^\infty \alpha^{z-1}(\alpha+\alpha^{-1})^{-1/2}\,d\alpha = \frac{1}{2\sqrt{\pi}}\Gamma(\frac{1/4+z/2}{1})\Gamma(\frac{1/4-z/2}{1})$, so one factor of $(D_\alpha^2 - 1/4)$ cancels the simple poles at $z = \pm 1/2$ and the remaining three factors produce a triple zero).
3. **Nonvanishing on the Open Critical Strip $0 < \operatorname{Re}(s) < 1$**:
   On $0 < \operatorname{Re}(s) < 1$, $s \ne 0$, $s \ne 1$, $(\tau/2)^{-s/2} = e^{-(s/2)\log\pi} \ne 0$, and $\Gamma(s/2)$ has no zeros anywhere in $\mathbb{C}$. Therefore,
   $$
   F_\tau(s) \ne 0 \quad \forall s \in \mathbb{C} \text{ with } 0 < \operatorname{Re}(s) < 1.
   $$

---

## 3. Exact Closed-Form Autocorrelation $h_K(x)$, Exact Rational Bernstein Envelopes, and Spectral Expansion Without RH

### 3.1 Closed-Form Multiplicative Convolution Theorem and Exact Rational Bernstein Kernel Envelopes

On the multiplicative group $(\mathbb{R}_+, dx/x)$, define grade dilation $(T_K f)(x) := f(\tau^K x)$, involution $f^*(x) := \overline{f(1/x)} = f(1/x)$, and multiplicative convolution
$$
h_K(x) := ((T_K \psi_\tau) * \psi_\tau^*)(x) = \int_0^\infty \psi_\tau(\tau^K x y)\psi_\tau(y)\,\frac{dy}{y} = h_0(\tau^K x).
$$

**Notation Separation (`TASK-TC-042R2`)**: To prevent symbol collision, we denote the symmetric kernel variable of $h_0(\alpha)$ by
$$
W_\alpha := (\alpha + \alpha^{-1})^2 = (2\cosh v)^2 \ge 4 \qquad (\alpha = e^v > 0),
$$
and reserve $W(X) := \sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\, h_0(n/X)$ exclusively for the reflected prime wavelet sum.

**Theorem 3.1 (Closed-Form Rational-Algebraic Autocorrelation & Eighth-Order Euler Representation).**
For every $\alpha = \tau^K x > 0$, $h_K(x) = h_0(\alpha)$ is given in exact closed form (with no Gaussian exponentials or numerical quadrature) by:
$$
\boxed{h_0(\alpha) = \frac{-648 W_\alpha^3 + 58380 W_\alpha^2 - 706860 W_\alpha + 2027025}{512\,\left(\alpha + \alpha^{-1}\right)^{17/2}} = \frac{1}{512}\left(\left(\alpha\frac{d}{d\alpha}\right)^2 - \frac{1}{4}\right)^4 \left(\alpha + \alpha^{-1}\right)^{-1/2}.}
$$
Moreover:
1. **Inversion Symmetry**: $h_0(1/\alpha) = h_0(\alpha)$ for all $\alpha > 0$, so $h_K(1/x) = h_0(\tau^K / x) = h_0(\tau^{-K} x) = h_{-K}(x)$.
2. **Exact Peak Value at $\alpha = 1$ ($W_\alpha = 4$)**:
   $$
   h_0(1) = \|\psi_\tau\|_{L^2(\mathbb{R}_+, dx/x)}^2 = \frac{92193}{512 \times 2^{17/2}} = \frac{92193}{131072\sqrt{2}} \approx 0.49736073812650097.
   $$
3. **Exact Rational Bernstein Proof of the Weighted Decay Envelopes (`certify_weighted_kernel_envelopes_bernstein`)**:
   Set $v = \log\alpha \in \mathbb{R}$ and $S = 2\cosh v = \alpha + \alpha^{-1} \ge 2$, and let $g(v) := h_0(e^v)$ so $g^{(m)}(v) = (D_\alpha^m h_0)(\alpha)$. Because $\frac{d^2}{dv^2}(S^q) = q^2 S^q - 4q(q-1) S^{q-2}$, for every even order $m = 2k \in \{0, 2, 4, 6, 8\}$ the rescaled function $P_m(y) := S^{5/2} g^{(m)}(v)$ is an **exact rational polynomial** of degree $k + 3$ in the bounded variable $y := 4/S^2 = 4/W_\alpha \in (0, 1]$ (with $y = 1 \iff v = 0 \iff \alpha = 1$). Expanding $P_m(y)$ in the Bernstein basis on $N = 8$ uniform rational subintervals $[j/8, (j+1)/8] \subset [0, 1]$ certifies by exact rational arithmetic (`fractions.Fraction`) that every interior Bernstein control point is strictly smaller in magnitude than the $y = 1$ endpoint value $|P_m(1)| = 2^{5/2}|g^{(m)}(0)|$ (with maximum interior-to-endpoint control-point ratios $0.766210, 0.875948, 0.914476, 0.928653, 0.934231 < 1$ for $m = 0, 2, 4, 6, 8$). This proves unconditionally (without invoking Bochner's theorem for weighted decay) that for all $v \in \mathbb{R}$ ($\alpha > 0$) and all $m \in \{0, 2, 4, 6, 8\}$:
   $$
   \boxed{\left|(D_\alpha^m h_0)(\alpha)\right| = \left|g^{(m)}(v)\right| \le \left|g^{(m)}(0)\right| 2^{5/2} \left(\alpha + \alpha^{-1}\right)^{-5/2} \le \left|g^{(m)}(0)\right|.}
   $$
   In particular, at $m = 0$, $|h_0(\alpha)| \le \frac{92193}{32768}(\alpha + \alpha^{-1})^{-5/2}$ for all $\alpha > 0$, and $-\frac{81}{64}\alpha^{-5/2} \le h_0(\alpha) < 0$ for all $\alpha \ge 9$.
4. **First Euler Derivative $(D_\alpha h_0)(\alpha)$ and Stieltjes Kernel $\tilde{h}_0(\alpha)$ Envelope**:
   Differentiating $h_0(\alpha) = N_0(W_\alpha) S^{-17/2}$ via $D_\alpha W_\alpha = 2(\alpha - \alpha^{-1})S$ yields
   $$
   (D_\alpha h_0)(\alpha) = \frac{(\alpha - \alpha^{-1})\left(3240 W_\alpha^3 - 525420 W_\alpha^2 + 9189180 W_\alpha - 34459425\right)}{1024\,\left(\alpha + \alpha^{-1}\right)^{19/2}},
   $$
   and $\tilde{h}_0(\alpha) := \frac{1}{2}h_0(\alpha) - (D_\alpha h_0)(\alpha)$. Expanding $|(D_\alpha h_0)(\alpha) S^{5/2}|^2 = (1 - y) Q_1(y)^2$ in the Bernstein basis on 32 rational subintervals of $[0, 1]$ certifies $|(D_\alpha h_0)(\alpha)| \le \frac{2871}{200}(\alpha + \alpha^{-1})^{-5/2} = 14.355(\alpha + \alpha^{-1})^{-5/2}$ and hence
   $$
   \left|\tilde{h}_0(\alpha)\right| \le \frac{1032993}{65536}\left(\alpha + \alpha^{-1}\right)^{-5/2} \approx 15.761757\left(\alpha + \alpha^{-1}\right)^{-5/2} \quad \forall \alpha > 0.
   $$

### 3.2 Complete Explicit-Formula Functional $C_\tau(K) = W_\xi(h_K)$ and Spectral Expansion Without RH

The centered Mellin transform of $h_K$ is
$$
H_K(z) = \int_0^\infty h_K(x) x^{z-1}\,dx = \tau^{-Kz} F_\tau\!\left(\frac{1}{2} + z\right)\overline{F_\tau\!\left(\frac{1}{2} - \bar{z}\right)} = \tau^{-Kz} F_\tau\!\left(\frac{1}{2} + z\right) F_\tau\!\left(\frac{1}{2} - z\right),
$$
which is holomorphic on $|\operatorname{Re}(z)| < 5/2$ and satisfies $H_K(1/2) = H_K(-1/2) = 0$ because $F_\tau(0) = F_\tau(1) = 0$. Consequently, the pole terms $H_K(1/2) + H_K(-1/2)$ in $W_\xi(h_K)$ vanish identically, and the completed correlation is given unconditionally by:
$$
\begin{aligned}
C_\tau(K) := W_\xi(h_K) &= -\sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\bigl[h_0(\tau^K n) + h_0(\tau^{-K} n)\bigr] - \bigl(\log(2\tau) + \gamma_E\bigr)h_0(\tau^K) \\
&\quad - \int_1^\infty \bigl[h_0(\tau^K x) + h_0(\tau^{-K} x) - 2 x^{-1/2} h_0(\tau^K)\bigr]\frac{x^{1/2}}{x - x^{-1}}\,\frac{dx}{x} \\
&= \sum_\rho m_\rho a_\rho \tau^{-K(\rho - 1/2)}, \qquad a_\rho := F_\tau(\rho)\overline{F_\tau(1 - \bar{\rho})},
\end{aligned}
$$
where the sum runs over all distinct nontrivial zeros $\rho$ of $\zeta(s)$ in $0 < \operatorname{Re}(\rho) < 1$ with multiplicity $m_\rho \ge 1$.
- **Without assuming RH**: Since both $\rho$ and $1 - \bar{\rho}$ lie in the open strip $0 < \operatorname{Re}(s) < 1$ where $F_\tau(s) \ne 0$, every nontrivial zero has **strictly nonvanishing spectral weight** $a_\rho \ne 0$.
- **Reality and Evenness ($C_\tau(-K) = C_\tau(K) \in \mathbb{R}$)**:
  - *Arithmetic proof*: Since $h_0(1/\alpha) = h_0(\alpha)$, $h_0(\tau^K) = h_0(\tau^{-K})$ and $h_0(\tau^K x) + h_0(\tau^{-K} x)$ is invariant under $K \mapsto -K$ for every $x > 0$.
  - *Spectral proof*: Under the zero quartet $\{\rho, \bar{\rho}, 1-\bar{\rho}, 1-\rho\}$ with $\rho = 1/2 + \delta + i\gamma$, the weights satisfy $a_{\bar{\rho}} = \overline{a_\rho}$, $a_{1-\bar{\rho}} = \overline{a_\rho}$, and $a_{1-\rho} = a_\rho$, so the quartet sum is
    $$
    C_{\mathrm{quartet}}(K) = 4\operatorname{Re}(a_\rho)\cosh(KL\delta)\cos(K\gamma L) - 4\operatorname{Im}(a_\rho)\sinh(KL\delta)\sin(K\gamma L),
    $$
    which is manifestly real and even in $K$ (formalized in Lean 4 theorem `quartet_grade_symmetry_and_evenness`).

---

## 4. Equivalent Formulations and Complete Fixed-Seed RH-Equivalence Proof

### 4.1 Equivalent Formulations (`Section 4`)

For the fixed state $\psi_\tau$, the following three statements are equivalent (formalized in `two_by_two_gram_determinant_equivalence`):
- **(A) Canonical Correlation Bound**: $C_\tau(0) \ge 0$ and $|C_\tau(K)| \le C_\tau(0)$ for all $K \in \overline{\mathbb{Q}} \cap \mathbb{R}$.
- **(B) $2 \times 2$ Toeplitz Gram Determinant Nonnegativity**: $C_\tau(0) \ge 0$ and $\Delta_\tau(K) := \det\begin{pmatrix} C_\tau(0) & C_\tau(K) \\ C_\tau(-K) & C_\tau(0) \end{pmatrix} = C_\tau(0)^2 - |C_\tau(K)|^2 \ge 0$ for all $K \in \overline{\mathbb{Q}} \cap \mathbb{R}$.
- **(C) Cyclic Trajectory Cauchy–Schwarz**: $\langle \psi_\tau, \psi_\tau \rangle_\xi \ge 0$ and $|\langle T_K\psi_\tau, \psi_\tau \rangle_\xi|^2 \le \langle T_K\psi_\tau, T_K\psi_\tau \rangle_\xi \langle \psi_\tau, \psi_\tau \rangle_\xi$ along the grade orbit $\{T_K\psi_\tau\}_{K \in \overline{\mathbb{Q}}\cap\mathbb{R}}$.

### 4.2 Complete Proof of Fixed-Seed Equivalence to RH (`Section 5`)

**Theorem 4.1 (Fixed-Seed Correlation Bound $\Longleftrightarrow$ RH).**
Statements (A)–(C) hold if and only if every nontrivial zero $\rho$ of $\zeta(s)$ satisfies $\operatorname{Re}(\rho) = 1/2$.

*Proof.*
1. **Converse ($\text{RH} \implies \text{(A)}$)**:
   If every nontrivial zero satisfies $\rho = 1/2 + i\gamma_\rho$ ($\gamma_\rho \in \mathbb{R}$), then $1 - \bar{\rho} = \rho$, so $a_\rho = |F_\tau(1/2 + i\gamma_\rho)|^2 > 0$. Hence $C_\tau(0) = \sum_\rho m_\rho |F_\tau(\rho)|^2 > 0$, and for every $K \in \mathbb{R}$,
   $$
   |C_\tau(K)| = \left|\sum_\rho m_\rho |F_\tau(\rho)|^2 \tau^{-i K \gamma_\rho}\right| \le \sum_\rho m_\rho |F_\tau(\rho)|^2 = C_\tau(0).
   $$
2. **Forward Direction ($\text{(A)} \implies \text{RH}$)**:
   - *Step 1 (Extension from $\overline{\mathbb{Q}}\cap\mathbb{R}$ to $\mathbb{R}$ by continuity and density)*:
     By Stirling's bound $|a_\rho| \ll |\gamma_\rho|^{15/2} e^{-\pi|\gamma_\rho|/2}$ and $|\tau^{-K(\rho-1/2)}| \le \tau^{|K|/2}$, the series $C_\tau(K) = \sum_\rho m_\rho a_\rho \tau^{-K(\rho-1/2)}$ converges normally on every compact interval $[-K_0, K_0] \subset \mathbb{R}$ and defines a continuous (in fact entire) function of $K$. Since $\overline{\mathbb{Q}} \cap \mathbb{R} \supset \mathbb{Q}$ is dense in $\mathbb{R}$, $|C_\tau(K)| \le C_\tau(0)$ on $\overline{\mathbb{Q}} \cap \mathbb{R}$ implies $|C_\tau(t)| \le C_\tau(0)$ for all $t \in \mathbb{R}$.
   - *Step 2 (Laplace resolvent and normal convergence of partial fractions)*:
     For $\operatorname{Re}(w) > L/2$, since $|\tau^{t(\rho - 1/2)}| = e^{t L \delta_\rho} < e^{t L / 2}$ and $\sum_\rho m_\rho |a_\rho| < \infty$, Fubini's theorem justifies term-by-term Laplace integration:
     $$
     \mathcal{L}[C_\tau(-t)](w) := \int_0^\infty e^{-wt} C_\tau(-t)\,dt = \sum_\rho m_\rho a_\rho \int_0^\infty e^{-(w - L(\rho - 1/2))t}\,dt = \sum_\rho \frac{m_\rho a_\rho}{w - L(\rho - 1/2)} =: \mathcal{R}_\tau(w).
     $$
     Because $\sum_\rho m_\rho |a_\rho| < \infty$, the partial-fraction series $\mathcal{R}_\tau(w)$ converges normally on every compact subset of $\mathbb{C} \setminus \{L(\rho - 1/2)\}$, providing the unique meromorphic continuation of $\mathcal{L}[C_\tau(-t)](w)$ to $\mathbb{C}$.
   - *Step 3 (Right-half-plane holomorphy under $|C_\tau(t)| \le C_\tau(0)$)*:
     Since $|C_\tau(-t)| \le C_\tau(0)$ for all $t \ge 0$, the integral $\int_0^\infty e^{-wt} C_\tau(-t)\,dt$ converges absolutely and defines a **holomorphic** function on the entire open right half-plane $\operatorname{Re}(w) > 0$, bounded by $|\mathcal{L}[C_\tau(-t)](w)| \le C_\tau(0)/\operatorname{Re}(w)$.
   - *Step 4 (Non-cancelling residue at any off-critical zero with $\delta_0 > 0$)*:
     Suppose $\zeta(s)$ has a nontrivial zero $\rho_0 = 1/2 + \delta_0 + i\gamma_0$ with $0 < \delta_0 < 1/2$. Then $w_0 := L(\rho_0 - 1/2) = L\delta_0 + i L\gamma_0$ lies in the open right half-plane $\operatorname{Re}(w_0) = L\delta_0 > 0$. Because the affine map $\rho \mapsto L(\rho - 1/2)$ is injective on $\mathbb{C}$ and the zeros of $\zeta(s)$ are isolated, no distinct zero $\rho \ne \rho_0$ maps to $w_0$. By normal convergence of $\sum_{\rho \ne \rho_0} \frac{m_\rho a_\rho}{w - L(\rho - 1/2)}$ on a small disk around $w_0$, $\mathcal{R}_\tau(w)$ has a simple pole at $w_0$ with residue
     $$
     \operatorname*{Res}_{w = w_0} \mathcal{R}_\tau(w) = m_{\rho_0} a_{\rho_0} = m_{\rho_0} F_\tau(\rho_0)\overline{F_\tau(1 - \bar{\rho}_0)} \ne 0,
     $$
     contradicting the holomorphy of $\mathcal{L}[C_\tau(-t)](w)$ on $\operatorname{Re}(w) > 0$.
   - *Step 5 (Functional-equation reflection for $\delta_0 < 0$)*:
     If $\rho_0 = 1/2 + \delta_0 + i\gamma_0$ had $-1/2 < \delta_0 < 0$, the functional equation $\xi(1-s) = \xi(s)$ yields the reflected zero $\rho_0' = 1 - \bar{\rho}_0 = 1/2 - \delta_0 + i\gamma_0$ with $\operatorname{Re}(\rho_0' - 1/2) = -\delta_0 > 0$, which is ruled out by Step 4. Thus $\delta_0 = 0$ for every nontrivial zero. $\blacksquare$

---

## 5. Certified Numerical Evaluation: Arithmetic vs. Unconditional Spectral Routes (`Sections 6 & 7`, Repaired in `TASK-TC-042R`)

### 5.1 Decoupled, Unconditional Evaluators and `TASK-TC-042R` Certification Repairs

1. **Unconditional Spectral Route (`evaluate_c_tau_spectral_certified`)**:
   - Sums the first 29 nontrivial zero conjugate pairs in $(0, 100]$ using the 100-digit certified enclosures in `data/certificates/zeros/zero_00001.json` .. `zero_00029.json` (which cover $(0, 100]$ with **zero intermediate spectral gaps**, backed by Turing block certificates `block_00001` .. `block_00005`).
   - Bounds all zeros with $|\gamma_\rho| > T = 100$ **unconditionally** using $|\delta_\rho| \le 1/2$ (never setting $\delta_{\max} = 0$), Stirling's complex Gamma remainder bound, and the Backlund–Rosser Riemann–von Mangoldt zero-counting bound:
     $$
     \left|R_{\mathrm{spec}}(K; 100)\right| \le 3.79 \times 10^{-55}\,\tau^{|K|/2} \le 5.91 \times 10^{-52} \quad \forall |K| \le 8.
     $$
   - In `TASK-TC-042R`, `compute_unconditional_spectral_derivative_tail_bound_arb(T_cutoff=100.0, deriv_order=m, K_max=K_max)` computes rigorous off-critical ($|\delta_\rho| \le 1/2$) Backlund–Rosser Stieltjes tail enclosures for higher $K$-derivatives (e.g., $3.79 \times 10^{-55}$ for $m=0$, $1.28 \times 10^{-50}$ for $m=2$, and $4.92 \times 10^{-46}$ for $m=4$ on $|K| \le 0.14$), replacing the earlier hard-coded `1e-45`.
2. **Certified Arithmetic Route (`evaluate_c_tau_arithmetic_certified`) and Taylor/Branch-Cut Repairs**:
   - Evaluates the exact closed-form rational-algebraic kernel $h_0(\tau^{\pm K} n)$ across all 2762 prime powers $2 \le p^k \le N_{\max} = 25000$, plus the unconditional Rosser–Schoenfeld Chebyshev summation-by-parts tail bound.
   - **Reproduction & Repair of the $[0, 0.25]$ Taylor Remainder Defect (`audit_archimedean_taylor_remainder_repair`)**:
     - At `series_order = 36` ($N = 35$ integrated terms, $0 \le k \le 34$) and $K = 0$, the exact omitted Taylor integral on $[0, 0.25]$ is
       $$
       \int_0^{0.25} \sum_{k=35}^\infty c_k u^k\,du = +2.1892962597 \times 10^{-23} \in [2.064 \times 10^{-23}, \; 2.212 \times 10^{-23}]
       $$
       (with $k = 35$ contributing $+1.983506 \times 10^{-23}$ and $k = 36$ contributing $+2.816228 \times 10^{-24}$), which is **$21.89\times$ larger** than the old hard-coded allowance `1e-24`.
     - Replaced the hard-coded `cauchy_tail = arb("1e-24")` with `compute_archimedean_taylor_cauchy_bound_arb`, which covers the circle $|u| = R_c = 1.0 < \pi/2$ by $512$ overlapping complex interval arcs (`analytic=True`) to bound $M(R_c) = \sup_{|u|=R_c}|g_K(u)|$ and upgrades `series_order = 49` ($N = 48$ integrated terms), yielding the certified Cauchy remainder bound $4.5165 \times 10^{-28}$ at $K = 0$ (strictly enclosing the true omitted integral $3.0792 \times 10^{-33}$).
   - **Branch-Cut Analyticity Flag Repair**:
     - Updated `evaluate_h0_acb`, `evaluate_h0_euler_d2_acb`, `evaluate_h0_euler_d4_acb`, `_f_d0_1`, and `_f_1_inf` to forward `analytic=analytic` into `s.sqrt(analytic=analytic)` so that `flint.acb.integral` rigorously checks branch cuts of $(\alpha + \alpha^{-1})^{-17/2}$ along $(-\infty, 0]$ across every complex quadrature ellipse.

### 5.2 Certified Grade Grid Results

| Grade $K$ | Unconditional Spectral $C_\tau^{\mathrm{spec}}(K)$ | Certified Arithmetic $C_\tau^{\mathrm{arith}}(K)$ | Enclosures Overlap | $|C_\tau(K)| / C_\tau(0)$ | $\Delta_\tau(K) = C_\tau(0)^2 - C_\tau(K)^2$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $0$ | $+9.504798117910 \times 10^{-4} \pm 3.79 \times 10^{-55}$ | $+9.50480944 \times 10^{-4} \pm 3.16 \times 10^{-9}$ | `True` | $1.00000000$ | $0$ |
| $1/8$ | $-9.447622082581 \times 10^{-4} \pm 4.25 \times 10^{-55}$ | $-9.44760884 \times 10^{-4} \pm 3.69 \times 10^{-9}$ | `True` | $0.99398451$ | $+1.083624 \times 10^{-8} > 0$ |
| $1/4$ | $+9.286153791481 \times 10^{-4} \pm 4.77 \times 10^{-55}$ | $+9.28617344 \times 10^{-4} \pm 5.48 \times 10^{-9}$ | `True` | $0.97699643$ | $+4.108535 \times 10^{-8} > 0$ |
| $1/2$ | $+8.668613749571 \times 10^{-4} \pm 6.00 \times 10^{-55}$ | $+8.66867062 \times 10^{-4} \pm 1.59 \times 10^{-8}$ | `True` | $0.91202503$ | $+1.519632 \times 10^{-7} > 0$ |
| $1$ | $+6.307301083454 \times 10^{-4} \pm 9.50 \times 10^{-55}$ | $+6.30786123 \times 10^{-4} \pm 1.56 \times 10^{-7}$ | `True` | $0.66359127$ | $+5.055914 \times 10^{-7} > 0$ |
| $\sqrt{2}$ | $+5.441316702609 \times 10^{-4} \pm 1.39 \times 10^{-54}$ | $+5.44507343 \times 10^{-4} \pm 1.05 \times 10^{-6}$ | `True` | $0.57248104$ | $+6.073326 \times 10^{-7} > 0$ |
| $2$ | $-1.133761279092 \times 10^{-4} \pm 2.38 \times 10^{-54}$ | $-1.07832481 \times 10^{-4} \pm 1.55 \times 10^{-5}$ | `True` | $0.11928305$ | $+8.905577 \times 10^{-7} > 0$ |
| $4$ | $-9.234066385075 \times 10^{-4} \pm 1.50 \times 10^{-53}$ | $+7.00765546 \times 10^{-2} \pm 1.51 \times 10^{-1}$ | `True` | $0.97151631$ | $+5.073205 \times 10^{-8} > 0$ |
| $8$ | $+8.437501317607 \times 10^{-4} \pm 5.90 \times 10^{-52}$ | $+7.12794413 \times 10^{-4} \pm 9.12 \times 10^{3}$ | `True` | $0.88770968$ | $+1.914976 \times 10^{-7} > 0$ |
| $-1/4$ | $+9.286153791481 \times 10^{-4} \pm 4.77 \times 10^{-55}$ | $+9.28617344 \times 10^{-4} \pm 5.48 \times 10^{-9}$ | `True` | $0.97699643$ | $+4.108535 \times 10^{-8} > 0$ |
| $-1/2$ | $+8.668613749571 \times 10^{-4} \pm 6.00 \times 10^{-55}$ | $+8.66867062 \times 10^{-4} \pm 1.59 \times 10^{-8}$ | `True` | $0.91202503$ | $+1.519632 \times 10^{-7} > 0$ |
| $-1$ | $+6.307301083454 \times 10^{-4} \pm 9.50 \times 10^{-55}$ | $+6.30786123 \times 10^{-4} \pm 1.56 \times 10^{-7}$ | `True` | $0.66359127$ | $+5.055914 \times 10^{-7} > 0$ |
| $-\sqrt{2}$ | $+5.441316702609 \times 10^{-4} \pm 1.39 \times 10^{-54}$ | $+5.44507343 \times 10^{-4} \pm 1.05 \times 10^{-6}$ | `True` | $0.57248104$ | $+6.073326 \times 10^{-7} > 0$ |
| $-2$ | $-1.133761279092 \times 10^{-4} \pm 2.38 \times 10^{-54}$ | $-1.07832481 \times 10^{-4} \pm 1.55 \times 10^{-5}$ | `True` | $0.11928305$ | $+8.905577 \times 10^{-7} > 0$ |

### 5.3 Repaired Two-Sided Local Theorem at $K = 0$, Scoped $M_6^{\mathrm{arith}}$ Bound, Outward-Rounded Gram Minors, and Quartet Controls

1. **Certified Origin Derivatives & Repaired Two-Sided Local Taylor Enclosures (`TASK-TC-042R` / `TASK-TC-042R2`)**:
   - $C_\tau(0)$, $C_\tau''(0)$, and $C_\tau^{(4)}(0)$ are independently computed and certified via **both** a 100% zero-free arithmetic route (`evaluate_zero_free_arithmetic_euler_derivative_at_zero`) and the unconditional spectral-tail route:
     - $C_\tau^{\mathrm{arith}}(0) = [9.50480944 \times 10^{-4} \pm 3.16 \times 10^{-9}]$, $C_\tau^{\mathrm{spec}}(0) = [9.504798117910 \times 10^{-4} \pm 3.79 \times 10^{-55}]$,
     - $(C_\tau'')^{\mathrm{arith}}(0) = [-0.64173930 \pm 1.52 \times 10^{-7}] < 0$, $(C_\tau'')^{\mathrm{spec}}(0) = [-0.641739264785 \pm 1.28 \times 10^{-50}] < 0$,
     - $(C_\tau^{(4)})^{\mathrm{arith}}(0) = [433.54130868 \pm 5.83 \times 10^{-6}] > 0$, $(C_\tau^{(4)})^{\mathrm{spec}}(0) = [433.541307975303 \pm 4.92 \times 10^{-46}] > 0$ (all three derivative enclosures intersect at $K = 0$).
   - Decomposing $C_\tau''(0)$ into arithmetic components shows that **both** the completed archimedean sector ($W_{\mathrm{arch}}''(0) = -0.25759528 < 0$, arising from $-167.40379948$ archimedean integral curvature plus $+167.14620420$ local constant curvature) **and** the prime-power sector ($W_{\mathrm{prime}}''(0) = -0.38414402 < 0$) are strictly concave at $K = 0$.
   - **Why Two-Sided Bounds Are Required**: Showing $C_\tau(K) < C_\tau(0)$ alone does not establish $|C_\tau(K)| < C_\tau(0)$ unless $C_\tau(K) > -C_\tau(0)$ is also certified (`taylor_two_sided_abs_correlation_bound` and `taylor_sixth_order_two_sided_abs_correlation_bound` in Lean 4). We distinguish the **Taylor lower-bound polynomial roots** from the actual correlation crossings.
   - **Route 1 — 100% Zero-Free 6th-Order Arithmetic Taylor Enclosure (Scoped to $|K| \le 0.08$)**:
     - Using the exact rational Bernstein polynomial certificates $|g^{(6)}(v)| \le |g^{(6)}(0)| 2^{5/2} (2\cosh v)^{-5/2}$ and $|g^{(8)}(v)| \le |g^{(8)}(0)| 2^{5/2} (2\cosh v)^{-5/2}$ (`Section 3.1`), together with the elementary prime-power sum bound
       $$
       \sum_{n \ge 2} \frac{\Lambda(n)}{n^3} \le \frac{\log 2}{8} + \frac{\log 3}{27} + \frac{\log 3}{18} + \frac{1}{36} \approx 0.21614536 < 0.225
       $$
       (and direct certified sum up to $25000$ plus Rosser–Schoenfeld tail $\le 0.164823 < 0.225$), the 6th-derivative bound on the compact interval $|K| \le 0.08$ ($\kappa_{\max} = 0.08 \log\tau$, splitting $(0, 1]$ at $u_0 = \sqrt{4 g_6(0)/g_8(0)} \approx 0.1656$) is certified as:
       $$
       \boxed{\sup_{|K| \le 0.08} \left|C_\tau^{(6)}(K)\right| \le M_6^{\mathrm{arith}} := 27971954.786589753.}
       $$
       *(Note: Because the tail majorant on $[1, \infty)$ and the prime-power sum contain the shift factor $\cosh(5\kappa/2) \le \cosh(0.20\log\tau)$, $M_6^{\mathrm{arith}}$ is explicitly scoped to the compact domain $|K| \le 0.08$, NOT all $K \in \mathbb{R}$.)*
     - Evaluating the 6th-order Taylor lower-bound polynomials in outward-rounded Arb ball arithmetic certifies the **exact rational interval** $0 < |K| \le \frac{1}{20} = 0.05$ for the two-sided inequality $-C_\tau(0) < C_\tau(K) < C_\tau(0)$ (and $0 \le |K| \le \frac{9}{200} = 0.045$ for strict positivity $C_\tau(K) > 0$) with strict positive margins:
       $$
       \forall K \in \left[-\frac{1}{20}, \frac{1}{20}\right] \setminus \{0\} : \quad -C_\tau(0) < C_\tau(K) < C_\tau(0) \quad (\text{upper margin } \ge +8.224 \times 10^{-5} > 0, \; \text{lower abs margin } \ge +6.047 \times 10^{-4} > 0),
       $$
       $$
       \forall K \in \left[-\frac{9}{200}, \frac{9}{200}\right] : \quad C_\tau(K) \ge +5.944 \times 10^{-5} > 0
       $$
       (while the approximate roots of the 6th-order Taylor lower-bound polynomials occur at $|K| \approx 0.04577570$ for $C_\tau(K) > 0$, $|K| \approx 0.05148579$ for $C_\tau(K) < C_\tau(0)$, and $|K| \approx 0.05514312$ for $C_\tau(K) > -C_\tau(0)$).
   - **Route 2 — Unconditional Spectral-Tail 4th-Order Taylor Enclosure (Scoped to $|K| \le 0.14$)**:
     - Using the 29 Turing-certified critical-line zeros in $(0, 100]$ plus the unconditional off-critical ($|\delta_\rho| \le 1/2$) Backlund–Rosser tail bound $4.92 \times 10^{-46}$ for $|\gamma_\rho| > 100$ on $|K| \le 0.14$, we obtain $\sup_{|K|\le 0.14}|C_\tau^{(4)}(K)| \le M_4^{\mathrm{spec}} = 433.54130958$. Evaluating the 4th-order Taylor lower-bound polynomials in Arb ball arithmetic certifies the **exact rational interval** $0 < |K| \le \frac{17}{250} = 0.068$ for $-C_\tau(0) < C_\tau(K) < C_\tau(0)$ (and $0 \le |K| \le \frac{1}{20} = 0.05$ for $C_\tau(K) > 0$) with strict positive margins:
       $$
       \forall K \in \left[-\frac{17}{250}, \frac{17}{250}\right] \setminus \{0\} : \quad -C_\tau(0) < C_\tau(K) < C_\tau(0) \quad (\text{upper margin } \ge +1.097 \times 10^{-3} > 0, \; \text{lower abs margin } \ge +3.102 \times 10^{-5} > 0),
       $$
       with approximate Taylor lower-bound polynomial roots at $|K| \approx 0.05085052$ for $C_\tau(K) > 0$, $|K| \approx 0.06846476$ for $|C_\tau(K)| < C_\tau(0)$, and $|K| \approx 0.13327694$ for $C_\tau(K) < C_\tau(0)$.
2. **Baseline Narrative vs. Artifact Discrepancy Reconciliation (`reconcile_baseline_narrative_discrepancies`)**:
   - **`1943.7705` vs. `433.5413086756161`**: Stale narrative in `docs/TC_CURRENT_CANONICAL_STATUS.md` reported $(C_\tau^{(4)})^{\mathrm{arith}}(0) = +1943.7705$ from an earlier un-normalized draft, whereas the certified fourth derivative at $K = 0$ in the artifact is $C_\tau^{(4)}(0) = [433.54130868 \pm 5.83 \times 10^{-6}]$ (`C_tau_fourth_deriv_0_mid = 433.5413086756161`), and the scoped sixth-derivative bound on $|K| \le 0.08$ is $\sup_{|K|\le 0.08}|C_\tau^{(6)}(K)| \le M_6^{\mathrm{arith}} = 27971954.786589753$.
   - **`0.0566039457` (and `0.0885735048`) vs. Derived Uniform Archimedean Bound `5.994279`**: Stale narrative in `docs/TC_CURRENT_CANONICAL_STATUS.md` used $0.0566039457 + 0.0319695591 = 0.0885735048$ (point values at $K = 1$) while the code used an ad-hoc `4.95`; now the uniform archimedean bound is derived and certified in `derive_and_certify_uniform_archimedean_bound` by splitting $(0, 1]$ at $u_0 = \sqrt{4 g_0(0)/|g_2(0)|} \approx 0.353502$, proving $|I_{\mathrm{arch}}(K)| \le 0.698425 + 1.970473 + 0.383932 + 1.395526 = 4.448357 < 4.95$ and $|W_{\mathrm{arch}}(h_K)| \le 1.545922 + 4.448357 = 5.994279$ for all $K \in \mathbb{R}$ (eliminating the hard-coded `4.95`).
   - **`0.0319695591` vs. `0.6330390930175781` and Certified $W(\tau) = -0.0120819471$**: `0.0319695591` was a stale uncertified draft constant in `docs/TC_CURRENT_CANONICAL_STATUS.md` (paired with `0.0566039457` to give `0.0885735048`). In the certified artifact, the reflected prime wavelet sum at $K = 1$ ($X = \tau = 2\pi$) is $W(\tau) = -0.012081947061365263$ (`[-0.012082 +/- 2.10e-7]`), at $X = 1$ is $W(1) = -0.0574913211$, and the global upper bound on $|P_{\mathrm{fwd}}(X)|$ for all $X \ge 1$ is $\frac{92193}{32768} \times 0.225 = 0.6330390930175781$.
3. **Finite Toeplitz Gram Matrices Certified by Outward-Rounded `flint.arb_mat.det()` Minors**:
   - Positive-definiteness of the finite Toeplitz Gram matrices $[C_\tau(K_i - K_j)]$ is certified via Sylvester's criterion using outward-rounded leading principal minor determinants `flint.arb_mat.det()` on the full `arb` enclosures (with floating-point eigenvalues reported purely as diagnostics):
     - **`rational_6_point_grid` $\{0, 1/8, 1/4, 1/2, 1, 2\}$ (spectral route)**: all 6 leading principal minor determinants are certified strictly positive ($\det_1 \approx 9.505 \times 10^{-4}$, $\det_2 \approx 1.084 \times 10^{-8}$, $\det_3 \approx 1.948 \times 10^{-14}$, $\det_4 \approx 1.052 \times 10^{-19}$, $\det_5 \approx 2.340 \times 10^{-27}$, $\det_6 \approx 1.528 \times 10^{-35} \pm 4.50 \times 10^{-78} > 0$).
     - **`algebraic_5_point_grid` $\{-\sqrt{2}, -1/2, 0, 1/2, \sqrt{2}\}$ (spectral route)**: all 5 leading principal minor determinants are certified strictly positive ($\det_5 \approx 9.959 \times 10^{-30} \pm 6.09 \times 10^{-73} > 0$).
     - **`zero_free_arithmetic_3_point_grid` $\{0, 1/4, 1/2\}$ (100% zero-free arithmetic route)**: all 3 leading principal minor determinants are certified strictly positive ($\det_1 \ge 9.5047 \times 10^{-4} > 0$, $\det_2 \ge 4.1067 \times 10^{-8} > 0$, $\det_3 = [2.25 \times 10^{-13} \pm 9.17 \times 10^{-14}] \ge 1.5886 \times 10^{-13} > 0$).
4. **Synthetic Off-Critical Quartet Controls**:
   - For synthetic off-critical quartets at $\gamma_0 = 14.13472514$ with $\delta_0 \in \{0.05, 0.15, 0.25\}$, $|a_{\rho_0}| > 0$ in every case and $C_{\mathrm{quartet}}(K)$ grows exponentially as $\cosh(K L \delta_0)$, reaching $|C_{\mathrm{quartet}}(K)|/|C_{\mathrm{quartet}}(0)| \approx 1.422, 7.234, 42.615$ by $K = 40 \cdot \frac{2\pi}{\gamma_0 L} \approx 9.67$, violating $|C(K)| \le C(0)$.

---

## 6. Controls on the Role of $\tau = 2\pi$ (`Section 8`)

Replacing the Gaussian width $\tau/2 = \pi$ by $a > 0$ in $G_{t,a}(x) = t^{1/4} e^{-a t x^2}$ and the grade base $\tau$ by $b > 1$ in $(T_{K,b} f)(x) = f(b^K x)$ yields the exact identity (verified to $< 10^{-45}$ across all 5 tested $(a, b)$ pairs and formalized in `gaussian_width_and_grade_base_scaling_identity`):
$$
\boxed{C_{a,b}(K) = \sqrt{\frac{a_0}{a}}\,C_{a_0,\tau}\!\left(K\frac{\log b}{\log \tau}\right), \qquad a_0 = \frac{\tau}{2} = \pi.}
$$
- **Physical-space mechanism**: $\psi_a(x) = (a_0/a)^{1/4}\psi_\tau(\sqrt{a/a_0}\,x)$, so the scale-invariant Haar convolution $dy/y$ factors out $((a_0/a)^{1/4})^2 = \sqrt{a_0/a}$ while $b^K x = \tau^{K \log b / \log\tau} x$.
- **Mellin-space mechanism**: $F_a(s) = (a_0/a)^{s/2} F_\tau(s)$, so on every reflected zero pair $(\rho, 1-\bar{\rho})$ where $\rho + (1-\rho) = 1$, $F_a(\rho)\overline{F_a(1-\bar{\rho})} = \sqrt{a_0/a}\,a_\rho$ is independent of $\rho$.
- **Consequence**: Changing $b > 1$ reparametrizes the grade axis $K \mapsto K \frac{\log b}{\log\tau}$ and changing $a > 0$ scales the correlation by $\sqrt{\pi/a}$. Thus any arithmetic proof of $|C_\tau(K)| \le C_\tau(0)$ must either establish the inequality for all real shifts $\kappa = K \log\tau \in \mathbb{R}$ or use the self-dual Poisson/theta coupling between $\pi^{-s/2}\Gamma(s/2)$ and the integer lattice $\mathbb{Z}$ at $a = \pi = \tau/2$.

---

## 7. Arithmetic Proof Attempts, Repaired Stieltjes Multiscale Reduction, & Substantive Cancellation Attempts (`SUBGATE-TC-042B`) (`Section 9`)

1. **Attempt 1 — Pointwise Kernel Difference $d_K^-(x) = 2h_0(x) - [h_0(\tau^K x) + h_0(\tau^{-K} x)]$ (`POINTWISE_KERNEL_DIFFERENCE_SIGN_FALSIFIED`)**:
   - Because $h_0(\alpha)$ has three sign changes on $\alpha \ge 1$ ($h_0(1) > 0$, $h_0(2) < 0$, $h_0(3) > 0$, and $h_0(\alpha) < 0$ for $\alpha \ge 5$), at $K = 1$ the kernel difference satisfies $d_1^-(3) = +0.248918 > 0$ at $p = 3$ and $d_1^-(7) = -0.401751 < 0$ at $p = 7 \approx \tau$. Term-by-term sign dominance across prime powers is therefore false.
2. **Attempt 2 — Local Concavity & Collaborative Prime/Archimedean Curvature (`LOCAL_ORIGIN_CONCAVITY_CERTIFIED`)**:
   - At $K = 0$, both the completed archimedean sector ($W_{\mathrm{arch}}''(0) = -0.257595 < 0$) and the prime-power sector ($W_{\mathrm{prime}}''(0) = -0.384145 < 0$) are strictly concave, certifying the exact rational interval $0 < |K| \le 1/20 = 0.05$ via the 100% zero-free 6th-order arithmetic route and $0 < |K| \le 17/250 = 0.068$ via the unconditional spectral-tail 4th-order route.
3. **Attempt 3 — Large-$|K|$ Wavelet Decomposition & Reduction to Uniform Prime-Wavelet Boundedness (`SUBGATE-TC-042A` & `SUBGATE-TC-042B`)**:
   - Decomposing $C_\tau(K) = W_{\mathrm{arch}}(h_K) + P_{\mathrm{fwd}}(K) + P_{\mathrm{refl}}(K)$ for $K \ge 0$ (and by evenness $C_\tau(-K) = C_\tau(K)$ for all $K \in \mathbb{R}$):
     - Both the archimedean term and forward prime sum admit derived, unconditional global bounds on $K \ge 0$: $|W_{\mathrm{arch}}(h_K)| \le M_{\mathrm{arch}} = 5.994279$ (with $|I_{\mathrm{arch}}(K)| \le 4.448357 < 4.95$, decaying as $O(\tau^{-3K/2})$) and $|P_{\mathrm{fwd}}(K)| \le M_{\mathrm{fwd}} = 0.633039$ (decaying as $O(\tau^{-5K/2})$).
     - By the Laplace-resolvent argument (`Section 4.2`) and Lean theorem `complete_correlation_bounded_of_reflected_prime_wavelet_bound`, **any finite uniform bound** $|C_\tau(K)| \le M_{\mathrm{total}} < \infty$ on $K \ge 0$ already makes $\mathcal{L}[C_\tau(-t)](w)$ holomorphic on $\operatorname{Re}(w) > 0$ and prevents off-critical zeros.
     - Therefore, proving RH via this route reduces to the **Uniform Prime-Wavelet Boundedness Subgate (`SUBGATE-TC-042B`)** (`investigate_uniform_prime_wavelet_boundedness`):
       $$
       \boxed{\exists M < \infty \; \forall X \ge 1 : \quad \left|W(X)\right| := \left|\sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\, h_0\!\left(\frac{n}{X}\right)\right| \le M.}
       $$
4. **Repaired Stieltjes Chebyshev-Error Identities (Form A in $x$ and Form B in $\alpha = x/X$) (`TASK-TC-042R2`)**:
   - Writing $\psi(x) = \sum_{n \le x} \Lambda(n) = x + E(x)$ and noting that for the actual differentiated seed $\psi_\tau(x) = x^{1/2}\Phi_1^{(2)}(x)$,
     $$
     H_0(1/2) := \int_0^\infty \alpha^{-1/2} h_0(\alpha)\,d\alpha = F_\tau(1) F_\tau(0) = 0 \qquad \left(\text{distinct from } H_0(0) := \int_0^\infty h_0(\alpha)\,\frac{d\alpha}{\alpha} = F_\tau(1/2)^2 \approx 2.82909344 \times 10^{-5} > 0\right),
     $$
     we have $\int_1^\infty x^{-1/2} h_0(x/X)\,dx = X^{1/2} H_0(1/2) - \int_0^1 x^{-1/2} h_0(x/X)\,dx = -\int_0^1 x^{-1/2} h_0(x/X)\,dx$.
   - Since $\frac{d}{dx}\bigl[x^{-1/2} h_0(x/X)\bigr] = -x^{-3/2}\tilde{h}_0(x/X)$ where $\tilde{h}_0(\alpha) := \frac{1}{2}h_0(\alpha) - (D_\alpha h_0)(\alpha)$, Stieltjes integration by parts yields two equivalent exact identities (`verify_finite_cutoff_stieltjes_identities_arb`, formalized in `stieltjes_rescaled_variable_and_erroneous_factor_obstruction`):
     - **Form (A) — Original variable $x$ (no $X^{-1/2}$ factor)**:
       $$
       \boxed{W(X) = h_0\!\left(\frac{1}{X}\right) - \int_0^1 x^{-1/2} h_0\!\left(\frac{x}{X}\right)dx + \int_1^\infty E(x)\,x^{-3/2}\,\tilde{h}_0\!\left(\frac{x}{X}\right)dx.}
       $$
     - **Form (B) — Rescaled variable $\alpha = x/X$ ($x = X\alpha$, $x^{-3/2}\,dx = X^{-1/2}\alpha^{-3/2}\,d\alpha$)**:
       $$
       \boxed{W(X) = h_0\!\left(\frac{1}{X}\right) - \int_0^1 x^{-1/2} h_0\!\left(\frac{x}{X}\right)dx + X^{-1/2}\int_{1/X}^\infty E(X\alpha)\,\alpha^{-3/2}\,\tilde{h}_0(\alpha)\,d\alpha.}
       $$
   - **Finite-Cutoff Identity & Certified Verification at $B = 50$ for $X \in \{1, 4, 100\}$**:
     For any non-prime-power cutoff $B > 1$,
     $$
     \sum_{2 \le n \le B} \frac{\Lambda(n)}{\sqrt{n}} h_0\!\left(\frac{n}{X}\right) = \int_1^B x^{-1/2} h_0\!\left(\frac{x}{X}\right)dx + B^{-1/2} h_0\!\left(\frac{B}{X}\right) E(B) + h_0\!\left(\frac{1}{X}\right) + \int_1^B E(x)\,x^{-3/2}\,\tilde{h}_0\!\left(\frac{x}{X}\right)dx.
     $$
     At $B = 50$ across $X \in \{1, 4, 100\}$, both Form (A) and Form (B) enclose the direct prime-power sum in 256-bit Arb arithmetic with midpoint error $< 3 \times 10^{-31}$, whereas the old formula (which erroneously multiplied the $x$-variable integral by $X^{-1/2}$) fails at $X = 4$ by $2.15176 \times 10^{-2}$ and at $X = 100$ by $4.72372 \times 10^{-2}$.
   - **Uniform Boundary Bound and Equivalence to $I(X)$ (`stieltjes_signed_pairing_uniform_bound_equivalence`)**:
     For all $X \ge 1$, $|B_{\mathrm{boundary}}(X)| := |h_0(1/X) - \int_0^1 x^{-1/2} h_0(x/X)\,dx| \le \frac{92193}{24576} X^{-5/2} \le 3.751197 X^{-5/2}$. Consequently:
     $$
     \sup_{X \ge 1} \left|I(X)\right| < \infty \iff \sup_{X \ge 1} |W(X)| < \infty \iff \sup_{K \in \mathbb{R}} |C_\tau(K)| < \infty, \qquad I(X) := \int_1^\infty E(x)\,x^{-3/2}\,\tilde{h}_0\!\left(\frac{x}{X}\right)dx.
     $$
   - **Certified Point Enclosures at 9 Sample Scales in $[1, 1000]$**:
     At the 9 discrete sample scales $X \in \{1, 2, \pi, \tau, 10, \tau^2, 100, \tau^3, 1000\}$ (finite point certificates, not a continuous interval certificate on $[1, 1000]$), $|W(X)|$ is certified bounded by $\le 0.079372$.
5. **Three Substantive Cancellation Attempts on `SUBGATE-TC-042B` (`execute_subgate_tc042b_cancellation_attempts`)**:
   - **Attempt A — Multiscale Euler-Operator Factorization & Iterated Primitive Transfer (`primitive_transfer_zero_lower_boundary_and_spurious_term_obstruction`)**:
     - Symbolic verification (`sp.simplify == 0`) establishes the exact 9th-order Euler factorization:
       $$
       \tilde{h}_0(\alpha) = \frac{1}{2}h_0(\alpha) - D_\alpha h_0(\alpha) = -\frac{1}{512}\left(D_\alpha - \frac{1}{2}\right)^5 \left(D_\alpha + \frac{1}{2}\right)^4 \left(\alpha + \alpha^{-1}\right)^{-1/2}.
       $$
     - **Operator Multiplicities vs. Mellin Vanishing Orders**: The differential operator has factor multiplicities $5$ at $D_\alpha = +1/2$ and $4$ at $D_\alpha = -1/2$. Because the base kernel $(\alpha + \alpha^{-1})^{-1/2}$ has simple Mellin poles at $z = \pm 1/2$ (corresponding to the simple pole of $\Gamma(s/2)$ at $s = 0$ cancelling one zero of $s^2$ in $F_\tau(s)$), $H_0(z) = F_\tau(\frac{1}{2}+z)F_\tau(\frac{1}{2}-z)$ has a **triple zero** (order $1 + 2 = 3$) at $z = \pm 1/2$, and under the centered Mellin convention $\widehat{f}(z) = \int_0^\infty f(\alpha)\alpha^z\,\frac{d\alpha}{\alpha}$ (where $\widehat{D_\alpha f}(z) = -z\widehat{f}(z)$), $\widehat{\tilde{h}_0}(z) = (\frac{1}{2} + z)H_0(z)$ vanishes to order $4$ at $z = -1/2$ and order $3$ at $z = +1/2$.
     - **Exact Primitive-Transfer Identity Without Spurious Lower-Boundary Term**: With $E_1(x) := \int_1^x E(t)\,dt = \int_1^x [\psi(t) - t]\,dt$ (so $\psi_1(x) := \int_1^x \psi(t)\,dt = \frac{x^2 - 1}{2} + E_1(x)$), the lower boundary vanishes identically ($E_1(1) = 0$) and the upper boundary $E_1(B) B^{-3/2}\tilde{h}_0(B/X) = O(X^{5/2} B^{-2}) \to 0$ as $B \to \infty$, so integration by parts gives
       $$
       \boxed{I(X) = \int_1^\infty E_1(x)\,x^{-5/2}\,h_1\!\left(\frac{x}{X}\right)dx, \qquad h_1(\alpha) := \frac{3}{2}\tilde{h}_0(\alpha) - (D_\alpha \tilde{h}_0)(\alpha),}
       $$
       with **no** $\frac{1}{2}h_1(1/X)$ boundary term (at $B = 50$ across $X \in \{1, 4, 100\}$, the finite-cutoff identity $I_B(X) = E_1(B)B^{-3/2}\tilde{h}_0(B/X) + \int_1^B E_1(x)x^{-5/2}h_1(x/X)\,dx$ is certified in 256-bit Arb to $< 2.3 \times 10^{-69}$, whereas the extraneous term $\frac{1}{2}h_1(1/X)$ at $X = 1$ equals $-7.77359913$, creating a $7.7736$ error). While at the classical PNT exponent $s = 1$ (weights $\Lambda(n)/n$) the integral $\int_1^\infty E(x) x^{-2}\,dx = -\gamma_E - 1$ converges unconditionally because $E_1(x)/x^3$ is integrable, at the critical-line exponent $s = 1/2$ (weights $\Lambda(n)/\sqrt{n}$) each derivative transfer suppresses the high-frequency tail $x \gg X$ by $(X/x)^k$ but on the resonant scale band $x \in [X/4, 4X]$ the scale derivative $\frac{d}{dx}\tilde{h}_0(x/X) = x^{-1}(D_\alpha \tilde{h}_0)(x/X)$ has factor $x^{-1} \asymp X^{-1}$, which balances the extra factor of $x$ in $E_1(x)$.
   - **Attempt B — Signed Dyadic Scale Decomposition (`dyadic_shell_weighted_sum_and_misplaced_factor_obstruction`)**:
     - With shell weights $\omega_j := \int_{2^j}^{2^{j+1}} |\tilde{h}_0(\alpha)|\,\alpha^{-1/2}\,d\alpha > 0$ ($\sum_{j \in \mathbb{Z}} \omega_j \le 16.921 < \infty$), the normalized dyadic shell average in the original variable $x$ on $[2^j X, 2^{j+1} X] \cap [1, \infty)$ (with **no** $X^{-1/2}$ prefactor) is
       $$
       \boxed{\mu_j(X) := \frac{1}{\omega_j} \int_{[2^j X,\, 2^{j+1} X] \cap [1, \infty)} E(x)\,x^{-3/2}\,\tilde{h}_0\!\left(\frac{x}{X}\right)dx, \qquad I(X) = \sum_{j \in \mathbb{Z}} \omega_j \mu_j(X).}
       $$
     - **Why Omitting the Misplaced $X^{-1/2}$ Matters**: Under the elementary Chebyshev estimate $|E(x)| \le A x$, the true shell average satisfies $|\mu_j(X)| \le A X^{1/2}$ (growing like $X^{1/2}$), which isolates the exact signed cancellation requirement on each dyadic shell. Multiplying the $x$-variable integral by $X^{-1/2}$ erroneously represented $X^{-1/2} I(X)$ rather than $I(X)$ (failing at $B = 50$ by $2.15176 \times 10^{-2}$ at $X = 4$ and $4.72372 \times 10^{-2}$ at $X = 100$) and made the shell bound follow trivially from $|E(x)| \le A x$.
   - **Attempt C — Exact Seed-Wavelet Multiplicative Convolution Factorization & $\operatorname{sech}^2$ Local $L^2$ Energy (`single_seed_stieltjes_and_squared_polynomial_identities`, `single_seed_sech_energy_implies_complete_correlation_bound`)**:
     - By Fubini's theorem on $h_0(n/X) = \int_0^\infty \psi_\tau((n/X)y)\psi_\tau(y)\,\frac{dy}{y}$, the reflected prime wavelet sum factors as the multiplicative convolution of the **single-seed prime wavelet** $V_\tau(u)$ with $\psi_\tau$:
       $$
       \boxed{W(X) = \int_0^\infty V_\tau\!\left(\frac{X}{y}\right)\psi_\tau(y)\,\frac{dy}{y} = \int_0^\infty V_\tau(u)\,\psi_\tau\!\left(\frac{X}{u}\right)\frac{du}{u}, \qquad V_\tau(u) := \sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\,\psi_\tau\!\left(\frac{n}{u}\right).}
       $$
     - Because $F_\tau(1) = 0$ already holds for the single seed $\psi_\tau$ prior to squaring, the smooth PNT main term of $V_\tau(u)$ **already vanishes identically** ($\int_0^\infty x^{-1/2}\psi_\tau(x/u)\,dx = u^{1/2}F_\tau(1) = 0$, certified in Arb to $< 2.2 \times 10^{-25}$), and $\psi_\tau(y)$ has Gaussian decay $e^{-\pi y^2}$ for $y \ge 1$. Moreover, Stieltjes integration by parts gives the exact single-seed Chebyshev-error representation (verified at $B = 50$ for $u \in \{1, 2, 4\}$ to $< 3 \times 10^{-36}$):
       $$
       V_\tau(u) = \psi_\tau\!\left(\frac{1}{u}\right) - \int_0^1 x^{-1/2}\psi_\tau\!\left(\frac{x}{u}\right)dx + \int_1^\infty E(x)\,x^{-3/2}\,\tilde{\psi}_\tau\!\left(\frac{x}{u}\right)dx,
       $$
       where $\tilde{\psi}_\tau(\alpha) := \frac{1}{2}\psi_\tau(\alpha) - (D_\alpha \psi_\tau)(\alpha) = \alpha^{1/2}\bigl(2\rho^5 - 22\rho^4 + \frac{125}{2}\rho^3 - \frac{91}{2}\rho^2 + \frac{9}{2}\rho\bigr)e^{-\rho}$ with $\rho = \pi\alpha^2$.
     - **Exact Closed-Form Gaussian Moment Formula for $C_\psi^2$**: Substituting $r = \pi y^2$ in $C_\psi^2 := \int_0^\infty |\psi_\tau(y)|^2(y + y^{-1})^2\,\frac{dy}{y}$ yields the exact closed-form Gaussian moment formula (verified symbolically in SymPy and cross-checked in 256-bit Arb against quadrature on $[0, 4]$ plus the certified $[4, \infty)$ tail bound $e^{-16\pi} \approx 1.48 \times 10^{-22}$):
       $$
       \boxed{C_\psi^2 = \frac{1}{\sqrt{2}}\left(\frac{1143585}{524288\pi} + \frac{92193}{65536} + \frac{12735\pi}{32768}\right) \approx 2.3490149234126213, \qquad C_\psi \approx 1.5326496414421077 < 1.533.}
       $$
     - **Clean $\operatorname{sech}^2$-Weighted Local $L^2$ Energy Target & Repairs 8A/8B**: Writing $X = e^t$ ($t \ge 0$), $u = e^r$ ($r \in \mathbb{R}$), and $v(r) := V_\tau(e^r) = \sum_{n \ge 2} \frac{\Lambda(n)}{\sqrt{n}}\psi_\tau(n e^{-r})$, since $(y + y^{-1})^2 = 4\cosh^2(t - r)$, Cauchy–Schwarz gives
       $$
       |W(e^t)| \le C_\psi\,\sqrt{\mathcal{E}_\tau(t)}, \qquad \mathcal{E}_\tau(t) := \int_{\mathbb{R}} \frac{|v(r)|^2}{4\cosh^2(t - r)}\,dr,
       $$
       reducing `SUBGATE-TC-042B` to the clean single-seed local $L^2$ energy hypothesis:
       $$
       \boxed{\exists M < \infty \quad \forall t \ge 0 : \qquad \mathcal{E}_\tau(t) := \int_{\mathbb{R}} \frac{|v(r)|^2}{4\cosh^2(t - r)}\,dr \le M.}
       $$
       - **Repair 8A (Certified $[4, \infty)$ Tail Bound for Finite-Sum Convolution Verification at $N = 25, X = 4$)**: Adding the analytic $[4, \infty)$ Gaussian tail bound $9.0352 \times 10^{-19}$ ensures `finite_sum_convolution_enclosures_overlap == True` (`abs_diff = 3.04e-31`).
       - **Repair 8B (Prime-Power Cutoff Sensitivity at $X = 100$)**: At $X = 100$ ($t = \log 100 \approx 4.60517$), the quadrature window $r \in [t-4, t+4]$ reaches $u = e^{t+4} = 100 e^4 \approx 5459.82$, requiring prime powers up to $5 \times 100 e^{3.9} \approx 24574$. Truncating at `600` broke the zero-sum PNT cancellation of $\psi_\tau$ near $u \in [600, 5460]$ and produced the artificial inflation $\mathcal{E}_\tau^{\le 600}(\log 100) \approx 0.130633$, whereas with prime-power cutoff `25000` (and sensitivity controls `5000`, `15000`, `25000`), the converged grid diagnostic is $\mathcal{E}_\tau(\log 100) \approx 6.9793 \times 10^{-4}$ (explicitly labeled `TRUNCATED_GRID_DIAGNOSTIC_NOT_CERTIFIED` under evidence class `EMPIRICAL`).

---

## 8. Lean 4 Formalization Summary (`Section 10`, Expanded in `TASK-TC-042R2`, `TASK-TC-042F`, `TASK-TC-043`, `TASK-TC-043R`, `TASK-TC-044`, `TASK-TC-045`, `TASK-TC-045R`, `TASK-TC-046` & `TASK-TC-047`)

Module [`formal/RiemannScope/CanonicalThetaCorrelationBound.lean`](file:///c:/Development/Projects/reimann_scope/formal/RiemannScope/CanonicalThetaCorrelationBound.lean) compiles with `0 sorry` and `0 admit` and formalizes **28 definitions** and **47 theorems** (covering exact polynomial/operator identities, Bernstein endpoint polynomials, conditional Taylor/Laplace/Stieltjes/energy implication schemas, the reconciled `TASK-TC-042F` arithmetic–Fourier factorization identities, the `TASK-TC-043` / `TASK-TC-043R` cross-grade compatibility, transfer-cancellation, coercive-semiboundedness, unsigned-majorant window lower bound, and zero-moment / chordal Stieltjes equivalence theorems, the `TASK-TC-044` prime-shift quadratic form and divisor-aggregated Möbius inversion theorems, the `TASK-TC-045` / `TASK-TC-045R` mixed-grade pairing polarization / Möbius recovery equivalence, small-scale $W_{\log}$ tail / Mertens Stieltjes summation-by-parts, and Plancherel transfer bound / minus-state norm vanishing theorems, the `TASK-TC-046` finite-prime Euler recursion / prime-factorization coefficient classification and coupled prime-cutoff comparison / boundedness equivalence theorems, and the `TASK-TC-047` multiplicative prime-Euler integrality / grade-layer membership and common-referent station-ratio bridge theorems; **scope note**: scalar Lean theorems assuming analytic integral identities formalize the algebraic/deductive implications from those supplied scalar relations, whereas the continuous Stieltjes/Mellin integral derivations and Arb ball enclosures reside in SymPy and Python/FLINT):
1. `seed_first_order_spatial_polynomial`
2. `seed_second_order_spatial_polynomial`
3. `seed_mellin_pochhammer_polynomial_identity`
4. `defective_seed_mellin_endpoint_nonvanishing`
5. `autocorrelation_symmetric_numerator_identity`
6. `mellin_convolution_endpoint_vanishing`
7. `quartet_grade_symmetry_and_evenness`
8. `critical_line_spectral_weight_nonneg_and_triangle_bound`
9. `two_by_two_gram_determinant_equivalence`
10. `gaussian_width_and_grade_base_scaling_identity`
11. `laplace_resolvent_residue_obstruction_schema`
12. `fixed_seed_correlation_bound_implies_critical_line_schema`
13. `laplace_holomorphic_rhp_hypothesis_satisfiable`
14. `second_euler_autocorrelation_at_one`
15. `taylor_two_sided_abs_correlation_bound`
16. `complete_correlation_bounded_of_reflected_prime_wavelet_bound`
17. `stieltjes_rescaled_variable_and_erroneous_factor_obstruction` *(proves equivalence of Form A and Form B Stieltjes expressions and proves that multiplying the $x$-variable integral by $X^{-1/2}$ creates a nonzero discrepancy $(1 - X^{-1/2}) I_{\mathrm{Stieltjes}} \ne 0$ whenever $X \ne 1$ and $I_{\mathrm{Stieltjes}} \ne 0$)*
18. `bernstein_weighted_h0_polynomial_endpoints` *(proves the exact rational polynomial identity for $P_0(y) = S^{5/2} h_0(\alpha)$ in $y = 4/S^2 \in [0, 1]$ and its endpoint values $P_0(0) = -81/64$, $P_0(1) = 92193/32768$)*
19. `taylor_sixth_order_two_sided_abs_correlation_bound` *(proves the conditional 6th-order Taylor algebra implying $-C_0 < C_K < C_0$, $C_K > 0$, and $C_0^2 - C_K^2 > 0$)*
20. `stieltjes_signed_pairing_uniform_bound_equivalence` *(proves that given a uniform bound $|B_{\mathrm{boundary}}(X)| \le B_0$, uniform boundedness of $I(X)$ is equivalent to uniform boundedness of $W(X)$ and implies uniform boundedness of $C_\tau(K)$)*
21. `primitive_transfer_zero_lower_boundary_and_spurious_term_obstruction` *(proves that when $E_1(1) = 0$, the finite-cutoff primitive-transfer identity has zero lower-boundary contribution at $x = 1$, and adding the spurious $\frac{1}{2}h_1(1/X)$ term introduces a nonzero error whenever $h_1(1/X) \ne 0$)*
22. `dyadic_shell_weighted_sum_and_misplaced_factor_obstruction` *(proves that the weighted dyadic shell sum $\sum_j \omega_j \mu_j(X)$ in the original variable $x$ equals $I_B(X)$, whereas multiplying by $X^{-1/2}$ produces $X^{-1/2} I_B(X) \ne I_B(X)$ for $X \ne 1$)*
23. `single_seed_stieltjes_and_squared_polynomial_identities` *(proves the exact polynomial expansion of $P_2(r)^2$ and the single-seed Stieltjes polynomial $\frac{1}{2}P_2(r) - (2r P_2'(r) + \frac{1}{2}P_2(r) - 2r^2 P_2(r)) = 2r^5 - 22r^4 + \frac{125}{2}r^3 - \frac{91}{2}r^2 + \frac{9}{2}r$)*
24. `single_seed_sech_energy_implies_complete_correlation_bound` *(proves that if the $\operatorname{sech}^2$-weighted local $L^2$ energy $\mathcal{E}_\tau(\log X)$ is uniformly bounded by $M_{\mathrm{energy}}$ and $|W(X)|^2 \le C_\psi^2 \mathcal{E}_\tau(\log X)$, then $|C_\tau(K)|$ is uniformly bounded on $K \ge 0$)*
25. `unconditional_reflected_grade_invariance` *(proves $(\lambda z)^k (-\lambda z)^k = z^k (-z)^k$, establishing algebraic grade invariance of reflected pairs $(z_\rho, -z_\rho)$)*
26. `hyperbolic_offline_pair_invariance_and_indefiniteness` *(proves that the $2 \times 2$ hyperbolic pairing $q(u, v) = 2(u_r v_r + u_i v_i)$ under reciprocal real scaling $\lambda \in \mathbb{R} \setminus \{0\}$ satisfies $q(\lambda u, \lambda^{-1} v) = q(u, v)$, has indefinite signature $(1,1)$ with $q(1, -1) = -2 < 0$ and $q(1, 1) = +2 > 0$, and has off-diagonal cross-grade pairing $(\lambda + \lambda^{-1})u$)*
27. `quotient_unitary_grade_transport_of_positivity` *(proves that if $Q_\tau(f, f) = \|A_\tau f\|_{\mathcal{H}_\tau}^2 \ge 0$ with $Q_\tau(T_K f, T_K f) = Q_\tau(f, f)$ and a supplied scalar Cauchy–Schwarz hypothesis, then the grade shift preserves the null-space kernel and induces an isometric quotient operator with $|Q_\tau(T_K f, T_J g)|^2 \le Q_\tau(f, f)Q_\tau(g, g)$; Theorem 32 below removes the scalar Cauchy–Schwarz assumption by deriving $Q_{ff} Q_{gg} - Q_{fg}^2 \ge 0$ directly from quadratic nonnegativity)*
28. `attempt_A_shift_difference_square_identity` *(proves $2(f_0^2 - f_0 f_u) = (f_0 - f_u)^2 + (f_0^2 - f_u^2)$, establishing the real quadratic shift-difference square decomposition; Theorem 31 below proves the full two-sided sesquilinear shift-difference identity)*
29. `attempt_B_universal_pole_pnt_archimedean_cancellation` *(verifies the exact algebraic cancellation of supplied scalar terms representing the growing pole term $\int_1^\infty \Phi(x)x^{1/2}\,\frac{dx}{x}$, the PNT smooth main term $\int_1^\infty \Phi(x)x^{-1/2}\,dx$, and the archimedean tail correction $4\|f\|_{L^2}^2$, reducing $Q_\tau(f, f)$ to $\|A_\tau^B f\|_{\mathcal{H}_\tau}^2 - c_\tau^B\|f\|_{L^2}^2 + P_E(f)$; Theorem 34 below proves the transfer cancellation on $\mathcal{S}_\tau$)*
30. `complex_reflected_pair_conjugate_inverse_invariance` *(proves that for $q(u, v) = 2\operatorname{Re}(u\bar{v})$ and general complex $\lambda = \lambda_r + i\lambda_i \ne 0$, the conjugate-inverse scaling $\bar{\lambda}^{-1} = \lambda / |\lambda|^2$ satisfies $q(\lambda u, \bar{\lambda}^{-1} v) = q(u, v)$, whereas naive complex inverse scaling $\lambda^{-1} v$ fails at $\lambda = i, u = v = 1$ with $q(i, -i) = -2 \ne +2 = q(1, 1)$)*
31. `sesquilinear_shift_difference_identity` *(proves that for a unitary shift $S_u$ with $\langle S_u f, S_u g\rangle = \langle f, g\rangle$ and $\langle f, S_u g\rangle = \langle S_{-u} f, g\rangle$, the two-sided sesquilinear identity $\langle(I - S_u)f, (I - S_u)g\rangle = 2\langle f, g\rangle - \langle S_u f, g\rangle - \langle S_{-u} f, g\rangle = \Phi_{f,g}(1) - \Phi_{f,g}(e^u)$ holds, whereas omitting $\langle S_{-u} f, g\rangle$ leaves a nonzero discrepancy $\langle S_u f, g\rangle - \langle S_{-u} f, g\rangle$ whenever $\langle S_u f, g\rangle \ne \langle S_{-u} f, g\rangle$)*
32. `two_dim_gram_cauchy_schwarz_from_nonneg` *(proves without assuming Cauchy–Schwarz that if the $2\times 2$ quadratic form $Q(x f + y g) = Q_{ff} x^2 + 2 Q_{fg} x y + Q_{gg} y^2 \ge 0$ for all $x, y \in \mathbb{R}$ with $Q_{gg} > 0$, evaluating at $x = Q_{gg}, y = -Q_{fg}$ forces $Q_{ff} Q_{gg} - Q_{fg}^2 \ge 0$, and under grade invariance $Q_{gg} = Q_{ff}$ forces $|Q_{fg}| \le Q_{ff}$)*
33. `cross_grade_complex_zero_ray_collinearity` *(proves that a full complex zero shift $\rho' = r\rho = (r\beta_0, r\gamma_0)$ is collinear with $\rho$, so shifting only the real part to $r\beta_0 = 1/2$ forces $\gamma' = \gamma_0/(2\beta_0) \ne \gamma_0$ whenever $\beta_0 \ne 1/2$ and $\gamma_0 \ne 0$)*
34. `attempt_B_pole_vanishing_transfer_cancellation_on_S_tau` *(proves that on the pole-annihilating graded theta span $\mathcal{S}_\tau$ where $W_{\mathrm{pole}}(f * f^*) = \mathrm{pole}_{\mathrm{pos}} - J = 0$, the transfer quadratic form $B_{\mathrm{transfer}}(f) = 2\|f\|_{L^2}^2 - J = 4\|R_0 f\|_{L^2}^2 - 2\|f\|_{L^2}^2$ cancels identically between $P_E(f) = -W_{\mathrm{prime}}(f * f^*) + B_{\mathrm{transfer}}(f)$ and $D_{\mathrm{smooth}}^B(f) = -W_{\mathrm{arch}}(f * f^*) + B_{\mathrm{transfer}}(f)$)*
35. `coercive_norm_shift_semiboundedness_implies_correlation_bound` *(proves that if $P_E(f_\pm^{(K)}) \ge -(\|A_\tau^B f_\pm^{(K)}\|^2 + \mu_0 \|f_\pm^{(K)}\|^2)$ holds on normalized two-grade combinations $f_\pm^{(K)} = (\psi_\tau \pm T_K \psi_\tau)/\sqrt{2}$ for a finite constant $\mu_0 \ge 0$, then $|C_\tau(K)| \le C_\tau(0) + 2(c_\tau^B + \mu_0)\|\psi_\tau\|_{L^2}^2 < \infty$)*
36. `majorant_without_sign_cancellation_exceeds_fixed_coercive_norm` *(conditional scalar subtraction lemma proving that once a majorant satisfies $M_{\mathrm{maj}} \ge c_0 S - R_{\mathrm{rem}}$ and the hypothesis $c_0 S - R_{\mathrm{rem}} > B_{\mathrm{fixed}}$ is supplied, $M_{\mathrm{maj}} - B_{\mathrm{fixed}} > 0$)*
37. `majorant_window_lower_bound_and_envelope_ordering` *(proves for separated unsigned integrals $A_E(X)$ and $M_\omega(X)$ that $|E(x)| \le x\omega(x) \implies A_E(X) \le M_\omega(X)$, that nonnegativity outside $[X/2, 2X]$ and monotone $\omega(x) \ge \omega(2X)$ on $[X/2, 2X]$ imply $M_\omega(X) \ge c_0\sqrt{X}\,\omega(2X)$, and that $c_0\sqrt{X}\,\omega(2X) > B_{\mathrm{coer}}$ implies $M_\omega(X) - B_{\mathrm{coer}} > 0$)*
38. `zero_moment_subtracted_and_chordal_stieltjes_equivalence` *(proves that under the lower-tail boundary identity $L_{\mathrm{tail}}(X) = -B_{\mathrm{boundary}}(X)$ and Stieltjes identities $W(X) = B_{\mathrm{boundary}}(X) + I(X)$, $I_{\mathrm{chord}}(X) = W(X) - \psi(X)h_0(1/X)$, and $I_{\mathrm{drift}}(X) = \frac{\psi(X)}{X}B_{\mathrm{boundary}}(X) - \psi(X)h_0(1/X)$, the zero-moment subtracted decomposition satisfies $I(X) = I_{\mathrm{inc}}(X) + e(X)B_{\mathrm{boundary}}(X)$ and $I_{\mathrm{inc}}(X) = I_{\mathrm{chord}}(X) - I_{\mathrm{drift}}(X) = W(X) - \frac{\psi(X)}{X}B_{\mathrm{boundary}}(X) = I(X) - e(X)B_{\mathrm{boundary}}(X)$)*
39. `prime_shift_quadratic_form_and_subtracted_finite_part_equivalence` *(proves that for $D_N = 2 L_N \mathrm{norm}_{f} - 2 S_{\mathrm{corr},N}$ and $W_{\mathrm{prime},N} = 2 S_{\mathrm{corr},N}$, subtracting the self-term gives $D_N - 2 L_N \mathrm{norm}_{f} = -W_{\mathrm{prime},N}$, transfers into the truncated Attempt B decomposition as $Q_{\tau,N} = \mathrm{norm}_{A_B} - c_\tau^B \mathrm{norm}_{f} + (D_N - 2 L_N \mathrm{norm}_{f}) + B_{\mathrm{transfer}}$, and shows that $D_N \ge 0$ alone yields only $-W_{\mathrm{prime},N} \ge -2 L_N \mathrm{norm}_{f}$ whereas a subtracted finite-part lower bound $D_N - 2 L_N \mathrm{norm}_{f} \ge -(\mathrm{norm}_{A_B} - B_{\mathrm{transfer}} + \mu_0 \mathrm{norm}_{f})$ is equivalent to the relative semiboundedness hypothesis)*
40. `divisor_aggregated_stieltjes_and_moebius_inversion_identity` *(proves for supplied scalar quantities representing $W_{\log}(X) = B_{\log}(X) + I_{\log}(X)$ that if $|B_{\log}(X)| \le B_{\mathrm{bound}}$ and $|I_{\log}(X)| \le I_{\mathrm{bound}}$, then $|W_{\log}(X)| \le B_{\mathrm{bound}} + I_{\mathrm{bound}}$, and under exact Möbius inversion $W(X) = W_{\log}(X) + R_{\mu}(X)$ any uniform bound $|R_{\mu}(X)| \le R_{\mathrm{bound}}$ yields $|W(X)| \le B_{\mathrm{bound}} + I_{\mathrm{bound}} + R_{\mathrm{bound}}$)*
41. `mixed_grade_pairing_moebius_recovery_and_semiboundedness_equivalence` *(proves for supplied scalar quantities representing the polarized mixed-grade pairing $Q_\tau(T_K\psi_\tau, T_L\psi_\tau) = \langle A_\tau^B T_K\psi_\tau, A_\tau^B T_L\psi_\tau\rangle - c_\tau^B h_0(X) + B_{\mathrm{transfer}} - W(X^{-1}) - W(X)$ and exact Möbius decomposition $W(X) = W_{\log}(X) + R_\mu(X)$ that $Q_\tau(T_K\psi_\tau, T_L\psi_\tau) = B_{\mathrm{known}} - R_\mu(X)$, $|Q_\tau(T_K\psi_\tau, T_L\psi_\tau) + R_\mu(X)| \le B_{\mathrm{smooth\_max}} + W_{\mathrm{inv\_max}} + W_{\log,\mathrm{max}}$, and proves the two-sided triangle equivalence $|W(X)| \le |W_{\log}(X)| + |R_\mu(X)|$ and $|R_\mu(X)| \le |W(X)| + |W_{\log}(X)|$)*
42. `small_scale_w_log_tail_and_mertens_stieltjes_ibp_identity` *(proves that if $|W_{\log}(u)| \le C_{\log,0}\,u^{5/2}$ and $0 < X \le b$ with $m \ge 1$, then $|\mu(m) m^{-1/2} W_{\log}(X/m)| \le C_{\log,0}\,b^{5/2}\,m^{-3}$ whenever $|\mu(m)| \le 1$, and verifies the finite-cutoff Mertens Stieltjes summation-by-parts decomposition $R_{\mu, M}(X) = B_{\mathrm{Mertens}}(X, M) + I_{\mathrm{Mertens}}(X, M)$ and its triangle upper bound)*
43. `transfer_form_plancherel_bound_and_minus_state_vanishing` *(proves from $B_{\mathrm{transfer}}(f) = 2\|f\|_{L^2}^2 - J(f, f)$ and $0 \le J(f, f) \le 4\|f\|_{L^2}^2$ that $-2\|f\|_{L^2}^2 \le B_{\mathrm{transfer}}(f) \le 2\|f\|_{L^2}^2$, proves for two-grade states with $\|f_\pm^{(K)}\|_{L^2}^2 \le 2h_0(1)$ that $-4h_0(1) \le B_{\mathrm{transfer}}(f_\pm^{(K)}) \le 4h_0(1)$, and proves that at $K = 0$ where $h_{0,K} = h_0(1)$ the minus-state norm square $h_0(1) - h_{0,K} = 0$ vanishes)*
44. `finite_prime_euler_recursion_and_coefficient_cases` *(proves the one-prime recursion identity $W_{p_k}(X) = W_{p_{k-1}}(X) - p_k^{-1/2}W_{p_{k-1}}(X/p_k)$, two-prime commutation $(I - p^{-1/2}D_p)(I - q^{-1/2}D_q) = (I - q^{-1/2}D_q)(I - p^{-1/2}D_p)$, the three-case prime-factorization formula for $\lambda_y(n)$ depending on $\omega_{\le y}(n) \in \{0, 1, \ge 2\}$, and explicit prime-power / composite evaluations for $n = p^a$ ($p \le y$, giving $\log p$), $n = r^b$ ($r > y$, giving $b\log r$), $n = p^a r^b$ ($p \le y < r$, giving $\log p$), and $n = p^a q^b$ ($p < q \le y$, giving $0$))*
45. `coupled_prime_cutoff_comparison_and_boundedness_equivalence` *(proves that if $|W(X) - W_y(X)| \le \frac{C_{\log,0}X^{5/2}}{2 M^2}$ and $M^2 \ge X^{5/2}$ with $C_{\log,0} \ge 0$, then $|W(X) - W_y(X)| \le \frac{1}{2}C_{\log,0}$, and proves under $W(X) = W_{\log}(X) + R_\mu(X)$ and $|W_{\log}(X)| \le B_{\log}$ the two-way triangle implications $|W_y(X)| \le M_y \implies |W(X)| \le M_y + \frac{1}{2}C_{\log,0} \wedge |R_\mu(X)| \le M_y + \frac{1}{2}C_{\log,0} + B_{\log}$ and $|R_\mu(X)| \le M_\mu \implies |W(X)| \le B_{\log} + M_\mu \wedge |W_y(X)| \le B_{\log} + M_\mu + \frac{1}{2}C_{\log,0}$)*
46. `prime_euler_multiplicative_integrality_and_grade_layer_membership` *(proves that the multiplicative prime-Euler step factor $m_y(n) = \exp(\lambda_y(n))$ defined by `finitePrimeMultiplicativeFactorCases` satisfies $1 \le m_y(n) \in \mathbb{N}$ for all $n \ge 1$ and $p \ge 2$, matches $(1, n, p, 1)$ across the $\omega_{\le y}(n) \in \{0, 1, \ge 2\}$ cases, and that for any cumulative positive integer product $N_y \ge 1$ and grade scale $\tau^K > 0$, the grade-$K$ realization $\mathcal{A}_{K,y} = N_y\tau^K$ (`gradeLayerRealizedObservable`) is strictly positive, recovers the grade-invariant integer referent $\tau^{-K}\mathcal{A}_{K,y} = N_y$, cancels $\tau^K$ in the consecutive ratio $((N_y\cdot m_{\mathrm{step}})\tau^K)/(N_y\tau^K) = m_{\mathrm{step}}$, and belongs to the nonzero integer layer $L_K^\times = \{x \in \mathbb{R} : \exists m \in \mathbb{Z},\; m \ne 0 \wedge x = m\tau^K\}$)*
47. `common_referent_integer_layer_bridge_and_station_ratio_identity` *(proves that for any grades $K, J$ with scales $\tau^K, \tau^J \ne 0$ and cumulative integer product $N_y \in \mathbb{N}$, $\mathcal{A}_{K,y}$ and $\mathcal{A}_{J,y}$ share the identical normalized fiber size $\tau^{-K}\mathcal{A}_{K,y} = \tau^{-J}\mathcal{A}_{J,y} = N_y$, satisfy the ambient coboundary relation $\mathcal{A}_{K,y} = (\tau^K/\tau^J)\mathcal{A}_{J,y}$, satisfy the cross-grade station-ratio identity $(n\tau^J)/(1\cdot\tau^K) = n/(\tau^K/\tau^J)$, and if any zero-defect-modulated integer-layer observable $D_K = m_K\tau^K = m_J\tau^J$ satisfies layer disjointness $(m_K\tau^K = m_J\tau^J \implies m_K = 0 \wedge m_J = 0)$ and off-critical sensitivity $(\delta \ne 0 \implies m_K \ne 0)$, then $\delta = 0$)*

---

## 9. Arithmetic–Fourier Positive Factorization of the Complete Weil Pairing (`TASK-TC-042F`, `Section 11` — Reconciled in `TASK-TC-043`)

### 9.1 Reuse Map & Where the Missing Implication Remains
1. **`TC-019` (`tc/weil_inner_product.py`)**: Established that $(T_K f)(x) = f(\tau^K x)$ is unitary on $L^2(\mathbb{R}_+, d^\times x)$ with $\widehat{T_K f}(z) = \tau^{-K z}\widehat{f}(z)$ and dual $(T_K^{\mathbb{A}} Z)(z) = \tau^{-K z} Z(z)$. Because $\overline{\tau^{-K z_\rho}} = \tau^{K z_\rho} \iff \operatorname{Re}(z_\rho) = 0$, the spectral zero pairing is a positive-definite inner product with $T_K$ unitary on the zero space if and only if RH holds.
2. **`TC-020` (`tc/weil_positivity.py`)**: Verified localized Weil positivity on finite prime/zero windows (`OBL-TC-020-WEIL-FACTORIZATION`), leaving open an unconditional arithmetic positive factorization $Q_\tau(f, g) = \langle A_\tau f, A_\tau g\rangle_{\mathcal{H}_\tau}$.
3. **`TC-036/036R` (`tc/modular_theta_conductor_curvature.py`)**: Proved canonical theta self-duality at $\tau = 2\pi$ and constructed the bi-annihilating seed $\psi_\tau(x) = x^{1/2}(D^2 - 1/16)^2 e^{-\pi x^2}$ with $C_\tau(K) = Q_\tau(T_K\psi_\tau, \psi_\tau)$.
4. **`TC-037` & `TC-041/041R`**: Proved common-grade projection properties and quartet/remainder accounting, showing that finite-bandwidth projection cannot force positivity without an arithmetic-to-spectral positive factorization.
5. **`TC-042/042R/042R2`**: Derived closed-form $h_0(\alpha)$, certified $C_\tau(K)$ on the 14-grade grid and exact rational local concavity intervals, and reduced uniform correlation boundedness to `SUBGATE-TC-042B`.

### 9.2 Normalized Complete Pairing, Unconditional Grade Invariance, and the Reflected Off-Line Pair Block
On $\mathcal{D} = C_c^\infty(\mathbb{R}_{>0}; \mathbb{C})$ (and rapid-decay pole-annihilating extensions such as $\psi_\tau$) with Haar measure $d^\times x = dx/x$ and centered Mellin transform $\widehat{f}(z) = \int_0^\infty f(x)x^z\,d^\times x$, define $f^*(x) := \overline{f(1/x)}$, $(f * g)(x) := \int_0^\infty f(x/y)g(y)\,d^\times y$, and $Q_\tau(f, g) := W_\xi(f * g^*) = W_{\mathrm{pole}}(f * g^*) + W_{\mathrm{arch}}(f * g^*) - W_{\mathrm{prime}}(f * g^*)$.
- **Unconditional Grade Invariance (Without RH)**: By Haar scale invariance $u = \tau^K y$, $(T_K f) * (T_K g)^* = f * g^*$ holds identically on $\mathcal{D}$ for every $K \in \mathbb{A}_{\mathbb{R}}$, so $Q_\tau(T_K f, T_K g) = Q_\tau(f, g)$ unconditionally (Lean theorem `unconditional_reflected_grade_invariance`).
- **Why Diagonal Grade Invariance Does Not Force Positivity (The Reflected Off-Line Pair Block — Reconciled)**: By the functional equation $\xi(1/2 + z) = \xi(1/2 - z)$ and real symmetry $\overline{\xi(\bar{s})} = \xi(s)$, an off-critical zero $z_\rho = \delta + i\gamma$ ($\delta \ne 0$) pairs with $-\overline{z_\rho} = -\delta + i\gamma$ in $Q_\tau(f, f) = \sum_\rho m_\rho \widehat{f}(z_\rho)\overline{\widehat{f}(-\overline{z_\rho})}$. Setting $u = \widehat{f}(z_\rho)$ and $v = \widehat{f}(-\overline{z_\rho})$, under $T_K$ the coordinate $u$ scales by $\lambda_K = \tau^{-K(\delta + i\gamma)} \in \mathbb{C}^\times$ while $v$ scales by $\tau^{-K(-\delta + i\gamma)} = \tau^{+K\delta}\tau^{-iK\gamma} = \overline{\lambda_K}^{-1}$ (reciprocal modulus with the **same** phase factor $\tau^{-iK\gamma}$, since $\overline{\lambda_K}^{-1} = \lambda_K / |\lambda_K|^2$). Thus the 2-state contribution is the **hyperbolic quadratic form** (Lean theorems `hyperbolic_offline_pair_invariance_and_indefiniteness` and `complex_reflected_pair_conjugate_inverse_invariance`):
  $$
  \boxed{q(u, v) := u\bar{v} + v\bar{u} = 2\operatorname{Re}(u\bar{v}), \qquad q(\lambda u, \bar{\lambda}^{-1} v) = q(u, v) \quad \forall \lambda \in \mathbb{C}^\times.}
  $$
  *(Note: For general complex $\lambda \in \mathbb{C}^\times$, the invariant transformation is $\bar{\lambda}^{-1} v$, not $\lambda^{-1} v$; at $\lambda = i, u = v = 1$, $q(i, -i) = -2 \ne +2 = q(1, 1)$. It restricts to $q(\lambda u, \lambda^{-1}v) = q(u, v)$ only when $\lambda \in \mathbb{R}^\times$.)*
  Thus $q$ is **invariant under diagonal grade shifts** $T_K$ because $\lambda_K \overline{(\overline{\lambda_K}^{-1})} = 1$, yet $q$ has **indefinite signature $(1,1)$** ($q(1, 1) = +2 > 0$, $q(1, -1) = -2 < 0$). What distinguishes the hyperbolic block from a positive-definite block is **positivity on superposition states** $f = \sum_r c_r T_{K_r} f_0$ (equivalently **cross-grade Cauchy–Schwarz** $|Q_\tau(T_K f, f)| \le Q_\tau(f, f)$, since the off-diagonal cross-grade pairing grows unboundedly as $\bigl(\tau^{-K(\delta+i\gamma)} + \tau^{K(\delta-i\gamma)}\bigr)|u|^2 = 2\cosh(K\delta\log\tau)e^{-iK\gamma\log\tau}|u|^2$).

### 9.3 Quotient Unitary Grade Transport Theorem
**Proposition (`quotient_unitary_grade_transport_of_positivity` & `two_dim_gram_cauchy_schwarz_from_nonneg`).** If $Q_\tau(f, g) = \langle A_\tau f, A_\tau g\rangle_{\mathcal{H}_\tau}$ for a linear map $A_\tau : \mathcal{D} \to \mathcal{H}_\tau$ into a Hilbert space $\mathcal{H}_\tau$, then:
1. $Q_\tau(f, f) = \|A_\tau f\|_{\mathcal{H}_\tau}^2 \ge 0$ for all $f \in \mathcal{D}$, and the radical $\mathcal{N}_\tau := \{f \in \mathcal{D} : Q_\tau(f, f) = 0\} = \ker(A_\tau)$ is $T_K$-invariant.
2. Because $\|A_\tau(T_K f)\|_{\mathcal{H}_\tau}^2 = Q_\tau(T_K f, T_K f) = Q_\tau(f, f) = \|A_\tau f\|_{\mathcal{H}_\tau}^2$, the quotient operator $U_K(A_\tau f) := A_\tau(T_K f)$ is well-defined and extends uniquely to a **unitary group** $\{U_K\}_{K \in \mathbb{A}_{\mathbb{R}}}$ on $\overline{A_\tau(\mathcal{D})} \subset \mathcal{H}_\tau$.
3. By 2D quadratic nonnegativity $Q_\tau(x f + y g, x f + y g) \ge 0$ (`two_dim_gram_cauchy_schwarz_from_nonneg`), $|Q_\tau(T_K f, T_J g)| \le \sqrt{Q_\tau(f, f)\,Q_\tau(g, g)}$ for all $K, J \in \mathbb{A}_{\mathbb{R}}$, which on $f = g = \psi_\tau$ directly gives $|C_\tau(K)| \le C_\tau(0)$ and excludes all off-critical zeros via the Laplace-resolvent argument.

### 9.4 Five-Place $\tau = 2\pi$ Coupling Audit & Perturbation Controls
$\tau = 2\pi$ enters the complete explicit-formula pairing in five distinct places:
1. **Place 1 (Fourier Character & Self-Dual Poisson Normalization)**: $e(\xi x) = e^{-i\tau\xi x}$, making $e^{-(\tau/2)x^2}$ the unique self-dual Gaussian under Fourier transform.
2. **Place 2 (Theta Kernel & Conductor Curvature)**: $\theta(\tau, t) = \sum_{n \in \mathbb{Z}} e^{-(\tau/2)n^2 t}$, whose functional equation $\theta(\tau, t) = t^{-1/2}\theta(\tau, 1/t)$ holds if and only if the Gaussian width is $\tau/2 = \pi$.
3. **Place 3 (Completed Zeta Archimedean Gamma Factor)**: $\gamma_\tau(s) = (\tau/2)^{-s/2}\Gamma(s/2)$, generating the constant $-\log(2\tau) = -\log(4\pi)$ in $W_{\mathrm{arch}}(h)$.
4. **Place 4 (Grade Dilation Action)**: $(T_K f)(x) = f(\tau^K x)$ for $K \in \mathbb{A}_{\mathbb{R}}$.
5. **Place 5 (Explicit-Formula Plancherel Measure)**: $\frac{d\gamma}{\tau} = \frac{d\gamma}{2\pi}$ in the zero-counting density $\frac{N(T)}{T} \sim \frac{1}{\tau}\log\frac{T}{\tau e}$.

**Coherent vs. Component-Wise Perturbation Controls**:
- **Coherent rescaling of Place 4 alone ($b > 1$)**: Only reparametrizes the grade axis $C_{\pi, b}(K) = C_{\pi, \tau}(K \frac{\log b}{\log\tau})$.
- **Incoherent perturbation of Place 3 ($\tau_{\mathrm{arch}} \ne 2\pi$ in $(\tau_{\mathrm{arch}}/2)^{-s/2}\Gamma(s/2)$)**: Shifts the local archimedean constant by $\Delta c = -\log(\tau_{\mathrm{arch}}/\tau)$ ($\Delta c = -0.693147$ for $\tau_{\mathrm{arch}} = 4\pi$, $+0.693147$ for $\tau_{\mathrm{arch}} = \pi$) and breaks theta/functional-equation self-duality $\xi(s) = \xi(1-s)$.

### 9.5 Concrete Factorization Attempts A and B, Universal Pole–PNT–Archimedean Cancellation, and Certified Sign-Balance Discovery

We construct and test two explicit arithmetic–Fourier Hilbert-space maps $A_\tau : \mathcal{D} \to \mathcal{H}_\tau$ with exact remainder quadratic forms $R_\tau(f, g) := Q_\tau(f, g) - \langle A_\tau f, A_\tau g\rangle_{\mathcal{H}_\tau}$:

1. **Attempt A — Semilocal Archimedean / Conductor Positive Map $A_\tau^A$**:
   Using the **two-sided sesquilinear shift-difference identity** for unitary $(S_u f)(y) = f(e^u y)$ (`sesquilinear_shift_difference_identity`):
   $$
   \langle (I - S_u)f, (I - S_u)g\rangle_{L^2(d^\times y)} = 2\langle f, g\rangle_{L^2} - \langle S_u f, g\rangle_{L^2} - \langle S_{-u} f, g\rangle_{L^2} = \Phi_{f,g}(1) - \Phi_{f,g}(e^u)
   $$
   *(where $\Phi_{f,g}(e^u) = (f * g^*)(e^u) + (f * g^*)(e^{-u}) = \langle S_{-u} f, g\rangle_{L^2} + \langle S_u f, g\rangle_{L^2}$; on the diagonal $f = g$ with real-valued $f$, $\langle S_{-u} f, f\rangle = \langle S_u f, f\rangle$ so it specializes to $2(\|f\|_{L^2}^2 - \langle S_u f, f\rangle_{L^2})$ as in `attempt_A_shift_difference_square_identity`)*, define
   $$
   \mathcal{H}_\tau^A := L^2\!\left(\mathbb{R}_{>0}, \frac{e^{u/2}}{e^u - e^{-u}}\,du; L^2(\mathbb{R}_{>0}, d^\times y)\right), \qquad (A_\tau^A f)(u, y) := f(y) - f(e^u y).
   $$
   Then for all $f, g$ with $W_{\mathrm{pole}}(f * g^*) = 0$:
   $$
   \boxed{Q_\tau(f, g) = \langle A_\tau^A f, A_\tau^A g\rangle_{\mathcal{H}_\tau^A} + R_\tau^A(f, g), \qquad R_\tau^A(f, g) = -c_\tau \langle f, g\rangle_{L^2(d^\times y)} - W_{\mathrm{prime}}(f * g^*),}
   $$
   where $c_\tau := \log(4\tau) + \gamma_E + \frac{\tau}{4} \approx 5.3721834192256654 > 0$.
   - **Three Structural Obstructions to Attempt A**: (i) the local subtraction $-c_\tau\|f\|_{L^2}^2 < 0$ is strictly negative; (ii) the prime-power sum $-W_{\mathrm{prime}}(f * f^*)$ is left outside the norm square and diverges as $O(X^{1/2})$ unless $H_0(1/2) = 0$; and (iii) $W_{\mathrm{pole}}(f * f^*)$ is not cancelled for general $f \in \mathcal{D}$.

2. **Attempt B — Direct Arithmetic Kernel & Universal Pole–PNT–Archimedean Cancellation $A_\tau^B$ (`attempt_B_universal_pole_pnt_archimedean_cancellation`)**:
   Notice the exact partial-fraction identity on $x = e^u > 1$:
   $$
   \frac{x^{1/2}}{x - x^{-1}} = x^{-1/2} + \frac{x^{-3/2}}{x - x^{-1}}.
   $$
   Because $\int_1^\infty x^{-1/2}\frac{dx}{x} = 2$, splitting the archimedean kernel $\frac{x^{1/2}}{x - x^{-1}}$ into its integrable tail $\frac{x^{-3/2}}{x - x^{-1}}$ (which converges at $x \to \infty$ **without** subtracting $2h(1)$!) and $x^{-1/2}$ shifts the local subtraction from $c_\tau$ down to $c_\tau^B := c_\tau - 2 = \log(4\tau) + \gamma_E + \frac{\tau}{4} - 2 \approx 3.3721834192256654$, while in Stieltjes integration of $W_{\mathrm{prime}}(f * g^*) = \int_1^\infty \Phi_{f,g}(x)x^{-1/2}\,d\psi(x)$ ($\Phi_{f,g}(x) := (f*g^*)(x) + (f*g^*)(1/x)$) with $\psi(x) = x + E(x)$:
   $$
   \boxed{W_{\mathrm{pole}}^{\mathrm{pos}}(f * g^*) - W_{\mathrm{prime}}^{\mathrm{PNT}}(f * g^*) = \int_1^\infty \Phi_{f,g}(x)\,x^{1/2}\,\frac{dx}{x} - \int_1^\infty \Phi_{f,g}(x)\,x^{-1/2}\,dx = 0 \quad \forall f, g \in \mathcal{D}!}
   $$
   That is, the **growing $s = 1$ pole integral $\int_1^\infty \Phi_{f,g}(x)x^{1/2}\,\frac{dx}{x}$ and the PNT smooth main term $\int_1^\infty \Phi_{f,g}(x)x^{-1/2}\,dx$ are the exact same integral and cancel identically on all of $\mathcal{D}$** (even when $f$ does not annihilate the poles!). Furthermore, because $\psi(x) = 0$ on $(0, 2)$, $\psi$ is continuous at $x = 1$ (jump $= 0$; its first jump is $\log 2$ at $x = 2$), and in Stieltjes integration by parts of $-\int_1^\infty \Phi_{f,g}(x)x^{-1/2}\,dE(x)$ on $[1, \infty)$, the **lower integration-by-parts boundary value** $E(1) = \psi(1) - 1 = -1$ produces $\bigl[-E(x)x^{-1/2}\Phi_{f,g}(x)\bigr]_1^\infty = +E(1)\Phi_{f,g}(1) = -\Phi_{f,g}(1) = -2\langle f, g\rangle_{L^2}$, which combines with the $+4\langle f, g\rangle_{L^2}$ archimedean tail shift!
   Defining the decayed shift-difference Hilbert space
   $$
   \mathcal{H}_\tau^B := L^2\!\left(\mathbb{R}_{>0}, \frac{e^{-3u/2}}{e^u - e^{-u}}\,du; L^2(\mathbb{R}_{>0}, d^\times y)\right), \qquad (A_\tau^B f)(u, y) := f(y) - f(e^u y),
   $$
   we obtain the **universal identity on $\mathcal{D}$**:
   $$
   \boxed{Q_\tau(f, g) = \langle A_\tau^B f, A_\tau^B g\rangle_{\mathcal{H}_\tau^B} - c_\tau^B\langle f, g\rangle_{L^2(d^\times y)} + P_E(f, g), \qquad P_E(f, g) := -\int_1^\infty E(x)\,x^{-3/2}\,\widetilde{\Phi}_{f,g}(x)\,dx,}
   $$
   where $c_\tau^B = \log(4\tau) + \gamma_E + \frac{\tau}{4} - 2 \approx 3.3721834192$.
   (Here $\langle A_\tau^B f, A_\tau^B g\rangle_{\mathcal{H}_\tau^B} = \langle A_\tau^A f, A_\tau^A g\rangle_{\mathcal{H}_\tau^A} - 4\langle f, g\rangle_{L^2} + J_{f,g}$ where $J_{f,g} := \int_1^\infty \Phi_{f,g}(x)x^{-1/2}\,\frac{dx}{x}$, and $P_E(f, g) = W_{\mathrm{pole}}(f*g^*) - W_{\mathrm{prime}}(f*g^*) + 2\langle f, g\rangle_{L^2} - J_{f,g}$; on pole-annihilating states where $W_{\mathrm{pole}}(f*g^*) = 0$, the transfer term $B_{\mathrm{transfer}}(f, g) := 2\langle f, g\rangle_{L^2} - J_{f,g}$ cancels identically between the smooth part and $P_E(f, g)$.)

3. **Certified Quantitative Sign-Balance Discovery on $\psi_\tau$ and Multi-Grade Superpositions (With Complete Error Accounting)**:
   Evaluating the Attempt B decomposition on $f = \psi_\tau$ in 256-bit Arb arithmetic (with 512-arc Cauchy circle bound $< 10^{-26}$ on $[0, 0.25]$, $[20, \infty)$ analytic tail bounds $< 10^{-21}$, and Rosser–Schoenfeld prime-power tail bound $1.23 \times 10^{-9}$ for $n > 25{,}000$; half-line integral $J_0 = \int_1^\infty 2h_0(x)x^{-1/2}\,\frac{dx}{x} = +0.0259597613$ and transfer constant $B_{\mathrm{transfer}}(\psi_\tau) = 2h_0(1) - J_0 = +0.9687652063$) reveals a decisive structural fact:
   - $\|A_\tau^B \psi_\tau\|_{\mathcal{H}_\tau^B}^2 = +0.5947678335 > 0$ (spatial and analytic Arb enclosures agree to midpoint diff $< 10^{-25}$),
   - $-c_\tau^B \|\psi_\tau\|_{L^2(d^\times y)}^2 = -3.3721834192 \times 0.4973607381 = -1.6771975212 < 0$,
   - **Net smooth Attempt B part**: $\|A_\tau^B \psi_\tau\|_{\mathcal{H}_\tau^B}^2 - c_\tau^B \|\psi_\tau\|_{L^2}^2 = W_{\mathrm{arch}}(h_0) - B_{\mathrm{transfer}}(\psi_\tau) = -1.0824296878 < 0$ (**strictly negative!**),
   - **Chebyshev prime-error Stieltjes contribution**: $P_E(\psi_\tau) = -\int_1^\infty E(x)x^{-3/2}\widetilde{\Phi}_{\psi_\tau,\psi_\tau}(x)\,dx = -W_{\mathrm{prime}}(h_0) + B_{\mathrm{transfer}}(\psi_\tau) = +1.0833801676 > 0$ (**strictly positive!**),
   - **Net complete pairing**: $Q_\tau(\psi_\tau, \psi_\tau) = C_\tau(0) = -1.0824296878 + 1.0833801676 = +0.0009504798 > 0$.
   *(Note: Older draft values $-0.399957$ and $+0.400908$ arose from conflating $\|A_\tau^B \psi_\tau\|^2 \approx 0.594768$ with $W_{\mathrm{arch}}(h_0) \approx -0.113664$ and setting $J_0 = 0$; they have been purged across code and narrative.)*
   The same sign balance holds across all 4 tested multi-grade superpositions ($T_0 - T_1$, $T_0 + T_1$, $T_{-1} - 2T_0 + T_1$, $T_0 - T_{1/2} + T_1$): in every case the smooth archimedean+PNT part is **strictly negative** ($-2.16455, -2.16517, -6.49334, -2.67139$) and positivity of $Q_\tau(f, f) > 0$ ($+0.002016, +0.001785, +0.006163, +0.001501$) is restored **exclusively** by the positive Chebyshev prime-error Stieltjes integral $P_E(f) > 0$ ($+2.16657, +2.16695, +6.49951, +2.67289$).

---

## 10. Admissible Cross-Grade Compatibility (`TASK-TC-043`, `Section 12`)

### 10.1 Bounded Reconciliation of `TC-042F` (`Section 12.1`)
Before investigating cross-grade compatibility, six defects in `TC-042F` were verified and repaired:
1. **Complex reflected-pair scaling (`defect_1_complex_reflected_pair_scaling`)**: Reconciled $q(\lambda u, \bar{\lambda}^{-1}v) = q(u, v)$ for general complex $\lambda \in \mathbb{C}^\times$, where $\bar{\lambda}^{-1} = \lambda / |\lambda|^2$ (proved in Lean theorem `complex_reflected_pair_conjugate_inverse_invariance`, with explicit counterexample $q(i, -i) = -2 \ne +2 = q(1, 1)$ for naive $\lambda^{-1}$).
2. **Shift-difference sesquilinear identity (`defect_2_shift_difference_sesquilinear_identity`)**: Reconciled the general unitary shift identity $\langle(I - S_u)f, (I - S_u)g\rangle_{L^2(d^\times y)} = 2\langle f, g\rangle_{L^2} - \langle S_u f, g\rangle_{L^2} - \langle S_{-u} f, g\rangle_{L^2} = \Phi_{f,g}(1) - \Phi_{f,g}(e^u)$ (Lean theorem `sesquilinear_shift_difference_identity`).
3. **Stieltjes endpoint at $x = 1$ (`defect_3_stieltjes_endpoint_at_one`)**: Corrected narrative and comments: $\psi(x) = 0$ on $(0, 2)$ is continuous at $x = 1$ ($\psi(1^+) - \psi(1^-) = 0$), and $E(1) = \psi(1) - 1 = -1$ enters as the lower integration-by-parts boundary value $\bigl[-E(x)x^{-1/2}\Phi_{f,g}(x)\bigr]_1^\infty = -\Phi_{f,g}(1) = -2\langle f, g\rangle_{L^2}$.
4. **Conflicting numerical summaries (`defect_4_conflicting_numerical_summaries`)**: Reconciled the exact certified Attempt B values on $\psi_\tau$ (`smooth_part_B = -1.0824296878`, `prime_error_stieltjes_B = +1.0833801676`, `J_0 = +0.0259597613`, `B_transfer = +0.9687652063`) and replaced the stale draft figures `-0.399957, +0.400908` in `closing_questions["question_4_where_prime_or_off_critical_terms_resist"]`.
5. **Complete error accounting (`defect_5_complete_error_accounting`)**: Upgraded `TC-042F` quadrature from truncated $u_{\mathrm{top}} = 12$ to $u_{\mathrm{top}} = 20$ with a 512-arc Cauchy circle bound $< 10^{-26}$ on $[0, 0.25]$, analytic $[20, \infty)$ tail bounds $< 10^{-21}$, and Rosser–Schoenfeld prime-power tail bounds for $n > 25{,}000$, closing the $3.742875 \times 10^{-14}$ spatial-vs-analytic gap to $< 10^{-25}$ with overlapping Arb enclosures.
6. **Formalization scope and provenance (`defect_6_formalization_scope_and_provenance`)**: Proved `two_dim_gram_cauchy_schwarz_from_nonneg` (removing the external scalar Cauchy–Schwarz hypothesis for $2 \times 2$ grade blocks) and `attempt_B_pole_vanishing_transfer_cancellation_on_S_tau`, and documented exact Lean vs. analytic/Arb provenance.

### 10.2 Formal Specification of the Cross-Grade Compatibility Candidate (`Section 12.2`)
On the finite graded theta span
$$
\mathcal{S}_\tau := \left\{\sum_{j=1}^N c_j T_{K_j}\psi_\tau : N < \infty,\; c_j \in \mathbb{C},\; K_j \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}}\cap\mathbb{R}\right\}, \qquad (T_K f)(x) = f(\tau^K x), \quad \tau = 2\pi,
$$
keep the centered spectral variable $z = \rho - \tfrac{1}{2}$ distinct from the uncentered Mellin variable $s$. For the canonical seed
$$
F_\tau(s) = \frac{s^2(s-1)^2}{32}\left(\frac{\tau}{2}\right)^{-s/2}\Gamma\!\left(\frac{s}{2}\right),
$$
the zero at $s = 0$ ($z = -\tfrac{1}{2}$) is **simple** (order 1, since $s^2$ cancels the simple pole $\Gamma(s/2) \sim 2/s$), the zero at $s = 1$ ($z = +\tfrac{1}{2}$) is **double** (order 2), and the autocorrelation transform $H_0(z) = F_\tau(\tfrac{1}{2} + z)F_\tau(\tfrac{1}{2} - z)$ has **triple** zeros (order 3) at $z = \pm\tfrac{1}{2}$. Every $f \in \mathcal{S}_\tau$ is rapid-decay on $\mathbb{R}_{>0}$ and satisfies $\widehat{f}(\pm 1/2) = 0$, so $W_{\mathrm{pole}}(f * g^*) = 0$ identically on $\mathcal{S}_\tau \times \mathcal{S}_\tau$.
- **Exact Compatibility Equation on $\mathcal{S}_\tau \times \mathcal{S}_\tau$**:
  $$
  \boxed{Q_\tau(f, g) = \langle A_\tau^B f, A_\tau^B g\rangle_{\mathcal{H}_\tau^B} - c_\tau^B\langle f, g\rangle_{L^2(d^\times y)} + P_E(f, g) = \sum_\rho m_\rho \widehat{f}(z_\rho)\overline{\widehat{g}(-\overline{z_\rho})} \qquad \forall f, g \in \mathcal{S}_\tau.}
  $$
- **Identities Inherited Automatically from Coordinate Rescaling (Cannot Exclude Off-Critical Zeros Alone)**:
  1. Diagonal grade invariance $(T_K f) * (T_K g)^* = f * g^*$ and $Q_\tau(T_K f, T_K g) = Q_\tau(f, g)$.
  2. Reflected off-line pair invariance $q(\lambda_K u, \overline{\lambda_K}^{-1}v) = q(u, v)$.
  3. Reality and evenness $C_\tau(-K) = C_\tau(K) \in \mathbb{R}$.
  4. Pole vanishing $W_{\mathrm{pole}}(f * g^*) = 0$ and PNT moment vanishing $\int_0^\infty \alpha^{-1/2}h_0(\alpha)\,d\alpha = 0$ on $\mathcal{S}_\tau$.
- **Synthetic Off-Critical Quartet Controls**: Adding a synthetic off-critical quartet at $\frac{1}{2} \pm \delta_0 \pm i\gamma_0$ preserves all 4 coordinate-rescaling identities (and for small quartet weight preserves local concavity $C_{\mathrm{synth}}''(0) < 0$ and $|C_{\mathrm{synth}}(K)| \le C_{\mathrm{synth}}(0)$ up to $K = 4$), but violates: (i) the Euler product over primes, (ii) the discrete prime-power jump structure of $d\psi(x)$ (injecting a smooth oscillatory density $\propto x^{\delta_0}\cos(\gamma_0\log x)$ into $E(x)/x$), and (iii) two-grade Cauchy–Schwarz / coercive semiboundedness at large $K$ ($K = 8$) via $\cosh(K\delta_0\log\tau)$ growth.
- **Cross-Grade Complex Zero Membership & Transcendence Audit (`cross_grade_complex_zero_ray_collinearity`)**:
  Under $\mathcal{Z}_\tau(s, K) = \zeta(\tau^{-K}s)$, a zero $\rho_0 = \beta_0 + i\gamma_0$ has full complex grade-$K$ coordinate $\rho^{(K)} = \tau^K\rho_0 = (\tau^K\beta_0, \tau^K\gamma_0)$, which moves along the **complex ray** $\arg(\rho^{(K)}) = \arg(\rho_0)$. Moving only the real part onto the critical line ($\tau^{\Delta_{\mathrm{re}}}\beta_0 = 1/2$ at $\Delta_{\mathrm{re}} = -\frac{\log(2\beta_0)}{\log\tau}$) scales the imaginary part to $\frac{\gamma_0}{2\beta_0} \ne \gamma_0$ (for $\beta_0 = 0.65, \gamma_0 = 14.134725$, $\tau^{\Delta_{\mathrm{re}}}\gamma_0 = 10.872865 \ne 14.134725$) and does **not** establish zero-set membership. Moreover, while $m\tau^K = n\tau^J$ is unconditionally impossible for all **nonzero rational** grade differences $\Delta = K - J \in \mathbb{Q}\setminus\{0\}$ by Lindemann–Weierstrass ($\tau = 2\pi$ is transcendental), for **irrational algebraic** grade differences $\Delta \in \mathbb{A}_{\mathbb{R}}\setminus\mathbb{Q}$ the algebraic independence of $\tau^\Delta$ remains open in transcendence theory.

### 10.3 Worked Candidates on $\mathcal{S}_\tau$ for the Missing Arithmetic Implication (`Section 12.3`, Repaired in `TASK-TC-043R`)

1. **Candidate I — Attempt B Plancherel Multiplier $\mu_\tau^B(t)$ & Exact Pole-Vanishing Transfer Decomposition on $\mathcal{S}_\tau$ (`attempt_B_pole_vanishing_transfer_cancellation_on_S_tau`)**:
   - **Proved Plancherel Identity**: On $\mathcal{S}_\tau$, the smooth Attempt B quadratic form has the exact Mellin–Plancherel representation
     $$
     \|A_\tau^B f\|_{\mathcal{H}_\tau^B}^2 - c_\tau^B\|f\|_{L^2(d^\times y)}^2 = \frac{1}{\tau}\int_{-\infty}^\infty \mu_\tau^B(t)\,|\widehat{f}(it)|^2\,dt,
     $$
     where by the digamma recurrence $\psi_{\mathrm{digamma}}(z + 1) = \psi_{\mathrm{digamma}}(z) + \frac{1}{z}$ at $z = \frac{1}{4} + \frac{it}{2}$,
     $$
     \boxed{\mu_\tau^B(t) = \operatorname{Re}\psi_{\mathrm{digamma}}\!\left(\frac{1}{4} + \frac{it}{2}\right) - \log\frac{\tau}{2} - 2 + \frac{1}{\frac{1}{4} + t^2} = \operatorname{Re}\psi_{\mathrm{digamma}}\!\left(\frac{5}{4} + \frac{it}{2}\right) - \log\pi - 2.}
     $$
     The multiplier $\mu_\tau^B(t)$ is strictly increasing in $|t|$, negative at low frequencies ($\mu_\tau^B(0) = -c_\tau^B \approx -3.3721834192$), and crosses zero at the unique certified root $t_*^B \in [46.4061555, 46.4061557]$ (`mu_tau_B(46.4061555) < 0 < mu_tau_B(46.4061557)`).
   - **Fourier Identity for $J(f, f)$ vs. Separate Use of Pole Vanishing on $\mathcal{S}_\tau$**: Preserve the linear Euler-resolvent operator $(R_0 f)(x) = \int_0^x (y/x)^{1/2}(D_y f)(y)\,\frac{dy}{y}$ on $L^2(\mathbb{R}_{>0}, d^\times y)$, which has Mellin multiplier $\frac{it}{1/2 + it}$ and satisfies $\|R_0 f\|_{L^2}^2 = \frac{1}{\tau}\int_{\mathbb{R}} \frac{t^2}{t^2 + 1/4}|\widehat{f}(it)|^2\,dt = \|f\|_{L^2}^2 - \frac{1}{4}J(f, f)$. The half-line integral $J(f, f) := \int_1^\infty \Phi_{f,f}(x)x^{-1/2}\,\frac{dx}{x}$ satisfies the quadratic Fourier identity
     $$
     J(f, f) = \frac{1}{\tau}\int_{\mathbb{R}} \frac{|\widehat{f}(it)|^2}{t^2 + 1/4}\,dt = 4\|f\|_{L^2(d^\times y)}^2 - 4\|R_0 f\|_{L^2(d^\times y)}^2.
     $$
     Separately, on $\mathcal{S}_\tau$, the full-pole functional $W_{\mathrm{pole}}(f * f^*) = I_{\mathrm{pole},+}(f, f) + J(f, f) = 0$ vanishes (where $I_{\mathrm{pole},+}(f, f) := \int_1^\infty \Phi_{f,f}(x)x^{1/2}\,\frac{dx}{x}$), so $I_{\mathrm{pole},+}(f, f) = -J(f, f)$. Consequently, the quadratic transfer form
     $$
     \boxed{B_{\mathrm{transfer}}(f) := 2\|f\|_{L^2(d^\times y)}^2 - J(f, f) = 4\|R_0 f\|_{L^2(d^\times y)}^2 - 2\|f\|_{L^2(d^\times y)}^2 = \frac{1}{\tau}\int_{-\infty}^\infty \frac{2t^2 - 1/2}{t^2 + 1/4}\,|\widehat{f}(it)|^2\,dt}
     $$
     appears with identical sign in both $P_E(f)$ and the smooth deficit $D_{\mathrm{smooth}}^B(f) := c_\tau^B\|f\|_{L^2}^2 - \|A_\tau^B f\|_{\mathcal{H}_\tau^B}^2$:
     $$
     P_E(f) = -W_{\mathrm{prime}}(f * f^*) + B_{\mathrm{transfer}}(f), \qquad D_{\mathrm{smooth}}^B(f) = -W_{\mathrm{arch}}(f * f^*) + B_{\mathrm{transfer}}(f).
     $$
     On $f = \psi_\tau$, $B_{\mathrm{transfer}}(\psi_\tau) = +0.9687652063$ equals **$89.50\%$** of $D_{\mathrm{smooth}}^B(\psi_\tau) = +1.0824296878$ and cancels identically between $P_E(\psi_\tau) = +1.0833801676$ and $-D_{\mathrm{smooth}}^B(\psi_\tau)$ inside $Q_\tau(\psi_\tau, \psi_\tau) = P_E(\psi_\tau) - D_{\mathrm{smooth}}^B(\psi_\tau) = -W_{\mathrm{prime}}(h_0) + W_{\mathrm{arch}}(h_0)$. This transfer term is structural accounting of how the pole-vanishing decomposition splits between $D_{\mathrm{smooth}}^B$ and $P_E$, **not** a partial proof of the missing arithmetic inequality.
   - **Certified Plancherel Tail Enclosures & Three-Level Methodological Distinction**:
     Using Olver's complex Stirling bound $|\Gamma(1/4 + it/2)|^2 \le 2\pi(t/2)^{-1/2}e^{-\pi t/2 + 2/(3t)}$ for $t \ge T_{\mathrm{top}} \ge 40$, the $[T_{\mathrm{top}}, \infty)$ Plancherel tails are bounded by $R_{\mathrm{smooth}}(80) < 8.94 \times 10^{-43}$ and $R_{\mathrm{transfer}}(80) < 2.00 \times 10^{-43}$ (at $T_{\mathrm{top}} = 40$, $R_{\mathrm{smooth}}(40) < 6.83 \times 10^{-18}$ and $R_{\mathrm{transfer}}(40) < 2.16 \times 10^{-18}$). Retaining full `arb` enclosures through subtraction confirms $0 \in (\text{Plancherel} - \text{Spatial})$ with certified upper error bound $< 1.1 \times 10^{-35}$, while explicitly distinguishing: (1) the analytic Mellin–Plancherel proof of the identity, (2) certified numerical consistency with infinite-tail enclosures, and (3) truncated numerical diagnostics at $t = 40$ (whose float53 midpoint difference previously rounded to `0.0` while omitting the $[40, \infty)$ tail of $\sim 1.4 \times 10^{-19}$).

2. **Candidate II — Coercive Norm-Shifted Hilbert Space $(\mathcal{H}_{\tau, \mu_0}^B, \mathcal{A}_{\tau, \mu_0}^B)$ & Semiboundedness Reduction (`coercive_norm_shift_semiboundedness_implies_correlation_bound`)**:
   - **Independent Positive Construction**: For any constant $\mu_0 \ge 0$ (e.g., $\mu_0 = 1$), define $\mathcal{H}_{\tau, \mu_0}^B := \mathcal{H}_\tau^B \oplus L^2(\mathbb{R}_{>0}, \mu_0\,d^\times y)$ and $\mathcal{A}_{\tau, \mu_0}^B f := (A_\tau^B f, f)$ with unitary grade representation $\mathcal{U}_K^B(u, v) := (U_K^B u, T_K v)$, constructed **without** assuming $Q_\tau \ge 0$ or RH. Since $\|A_\tau^B f\|_{\mathcal{H}_\tau^B}^2 - c_\tau^B\|f\|_{L^2}^2$ has Plancherel multiplier $\mu_\tau^B(t)$, the positive shifted norm square has multiplier $\mu_\tau^B(t) + c_\tau^B + \mu_0 = \operatorname{Re}\psi_{\mathrm{digamma}}(5/4 + it/2) - \psi_{\mathrm{digamma}}(5/4) + \mu_0 \ge \mu_0$:
     $$
     \|\mathcal{A}_{\tau, \mu_0}^B f\|_{\mathcal{H}_{\tau, \mu_0}^B}^2 = \|A_\tau^B f\|_{\mathcal{H}_\tau^B}^2 + \mu_0\|f\|_{L^2(d^\times y)}^2 = \frac{1}{\tau}\int_{-\infty}^\infty \bigl(\mu_\tau^B(t) + c_\tau^B + \mu_0\bigr)\,|\widehat{f}(it)|^2\,dt \ge \mu_0\|f\|_{L^2}^2,
     $$
     giving on $\psi_\tau$ at $\mu_0 = 1$ the certified coercive norm square $\|\mathcal{A}_{\tau, 1}^B \psi_\tau\|^2 = +1.0921303173$.
   - **Proved Semiboundedness Reduction Theorem on Normalized Two-Grade States**: On the **normalized** two-grade states
     $$
     f_\pm^{(K)} := \frac{\psi_\tau \pm T_K\psi_\tau}{\sqrt{2}} \in \mathcal{S}_\tau, \qquad \|f_\pm^{(K)}\|_{L^2}^2 = h_0(1) \pm h_0(\tau^K) \le 2h_0(1), \qquad Q_\tau(f_\pm^{(K)}, f_\pm^{(K)}) = C_\tau(0) \pm C_\tau(K),
     $$
     if $P_E$ satisfies the uniform lower bound
     $$
     P_E(f_\pm^{(K)}) \ge -\|\mathcal{A}_{\tau, \mu_0}^B f_\pm^{(K)}\|_{\mathcal{H}_{\tau, \mu_0}^B}^2 = -\bigl(\|A_\tau^B f_\pm^{(K)}\|_{\mathcal{H}_\tau^B}^2 + \mu_0\|f_\pm^{(K)}\|_{L^2}^2\bigr)
     $$
     for some fixed finite $\mu_0 \ge 0$, then $C_\tau(0) \pm C_\tau(K) = Q_\tau(f_\pm^{(K)}, f_\pm^{(K)}) \ge -(c_\tau^B + \mu_0)\|f_\pm^{(K)}\|_{L^2}^2 \ge -2(c_\tau^B + \mu_0)h_0(1)$, which forces the uniform cross-grade correlation bound
     $$
     \boxed{|C_\tau(K)| \le C_\tau(0) + 2(c_\tau^B + \mu_0)h_0(1) < \infty \qquad \forall K \in \mathbb{A}_{\mathbb{R}}}
     $$
     ($\le 4.3500704879$ at $\mu_0 = 1$) and **excludes all off-critical zeros** via the Laplace–Carleman resolvent theorem. This scalar reduction is **conditional**: the necessary arithmetic lower bound on $P_E(f_\pm^{(K)})$ has not been established.

3. **Candidate III — Cross-Grade Off-Diagonal Scale Separation & Scoped Monotone Envelope Majorant Obstruction (`majorant_window_lower_bound_and_envelope_ordering`, `majorant_without_sign_cancellation_exceeds_fixed_coercive_norm`)**:
   - **Proved Off-Diagonal Scale Separation on Normalized $f_\pm^{(\Delta)} = (\psi_\tau \pm T_\Delta\psi_\tau)/\sqrt{2}$ ($\Delta = |K - J| > 0$)**:
     - The $L^2$ overlap decays rapidly as $|G_{L^2}(\Delta)| = |h_0(\tau^\Delta)| \le \frac{92193}{32768}\tau^{-5\Delta/2} = O(\tau^{-5\Delta/2})$ ($5.09 \times 10^{-16}$ at $\Delta = 8$),
     - The half-line pole-transfer overlap (with certified $[u_{\mathrm{top}}, \infty)$ tail enclosure) decays as $|J(\Delta)| = O(\Delta\tau^{-\Delta/2})$ ($1.04 \times 10^{-5}$ at $\Delta = 8$),
     - The smooth Attempt B off-diagonal deficit decays exponentially as $|D_{\mathrm{smooth}}^B(\Delta)| = O(\Delta\tau^{-\Delta/2})$ ($-9.99 \times 10^{-6}$ at $\Delta = 8$).
     Consequently, as $\Delta \to \infty$, the coercive norm of the normalized state $f_\pm^{(\Delta)}$ approaches the **finite** limit
     $$
     \lim_{\Delta \to \infty} \|\mathcal{A}_{\tau, \mu_0}^B f_\pm^{(\Delta)}\|_{\mathcal{H}_{\tau, \mu_0}^B}^2 = \|A_\tau^B \psi_\tau\|_{\mathcal{H}_\tau^B}^2 + \mu_0\|\psi_\tau\|_{L^2}^2 = 1.0921303173 \quad (\mu_0 = 1),
     $$
     whereas the off-diagonal prime-error pairing concentrates in the reflected prime-wavelet sum $W(\tau^\Delta) = B_{\mathrm{boundary}}(\tau^\Delta) + I(\tau^\Delta)$ at scale $X = \tau^\Delta$:
     $$
     G_{P_E}(\Delta) = P_E(T_\Delta\psi_\tau, \psi_\tau) = -W(\tau^\Delta) + O(\Delta\tau^{-\Delta/2}).
     $$
   - **Separated Unsigned Integrals & Scoped Monotone Envelope Obstruction**:
     Define separately the actual unsigned integral and the envelope majorant integral:
     $$
     A_E(X) := \int_1^\infty |E(x)|\,x^{-3/2}\,\bigl|\widetilde{h}_0(x/X)\bigr|\,dx, \qquad M_\omega(X) := \int_1^\infty x\,\omega(x)\,x^{-3/2}\,\bigl|\widetilde{h}_0(x/X)\bigr|\,dx.
     $$
     Under an upper envelope $|E(x)| \le x\,\omega(x)$, we have $|I(X)| \le A_E(X) \le M_\omega(X)$ (an upper bound on $A_E(X)$, **not** a lower bound on $A_E(X)$). By the exact antiderivative $\alpha^{-3/2}\widetilde{h}_0(\alpha) = -\frac{d}{d\alpha}\bigl(\alpha^{-1/2}h_0(\alpha)\bigr)$, the signed moment vanishes ($\int_0^\infty \alpha^{-1/2}\widetilde{h}_0(\alpha)\,d\alpha = 0$), whereas 256-bit Arb integration split at the 7 certified positive roots of $\widetilde{h}_0(\alpha) = 0$ establishes the strictly ordered unsigned moments:
     $$
     c_0 := \int_{1/2}^2 \alpha^{-1/2}\bigl|\widetilde{h}_0(\alpha)\bigr|\,d\alpha = 1.7456980946 \pm 4.60 \times 10^{-48} > 0, \qquad C_{\mathrm{abs}} := \int_0^\infty \alpha^{-1/2}\bigl|\widetilde{h}_0(\alpha)\bigr|\,d\alpha = 2.4863319706 \pm 4.39 \times 10^{-46} > c_0.
     $$
     For any nonnegative, nonincreasing envelope $\omega$ on $[1, \infty)$ and $X \ge 2$, restricting $M_\omega(X)$ to $x \in [X/2, 2X] \subset [1, \infty)$ where $\omega(x) \ge \omega(2X)$ yields the majorant lower bound
     $$
     \boxed{M_\omega(X) \ge c_0\sqrt{X}\,\omega(2X) \qquad (X \ge 2).}
     $$
     Within the specified envelope class where $\sqrt{X}\,\omega(2X) \to \infty$ as $X \to \infty$, $M_\omega(\tau^\Delta)$ diverges to $+\infty$ and exceeds the fixed coercive threshold above a finite crossover grade $\Delta_*(\mu_0)$ (for the illustrative constant envelope model $\omega_{\mathrm{Cheb}}(x) = 0.04$, cf. Rosser–Schoenfeld 1962 Thm. 12 one-sided upper bound $\psi(x) < 1.03883\,x$ for all $x > 0$ — note that $|\psi(x)-x| < 0.0397x$ is false at $x = 1$ since $|\psi(1)-1| = 1$ — full-majorant crossover $\Delta_* \approx 3.358$ and window-lower-bound crossover $\Delta_*^{\mathrm{win}} \approx 3.742$; for the illustrative sub-exponential model $\omega_{\mathrm{dLVP}}(x) = \exp(-0.2\sqrt{\log x})$, cf. Rosser–Schoenfeld 1962 Thm. 10 two-sided bound $|\psi(x)-x| < x(\log x)^2\exp(-\sqrt{\log x/R})$ for $x \ge 2$, $\Delta_* \approx 0.001$ and $\Delta_*^{\mathrm{win}} \approx 0.590$). The unsupported claim that *every* unsigned estimate must fail is withdrawn; in Lean 4, `majorant_window_lower_bound_and_envelope_ordering` formalizes $A_E \le M_\omega$ and $c_0\sqrt{X}\omega(2X) \le M_\omega$, while `majorant_without_sign_cancellation_exceeds_fixed_coercive_norm` is documented as a conditional scalar subtraction lemma under the threshold hypothesis $B_{\mathrm{fixed}} < c_0\cdot\text{scale\_factor}$.

### 10.4 Signed Cross-Grade Cancellation Investigation (`TASK-TC-043R`, `Section 12.5`)

1. **Zero-Moment Subtracted Identity & Lower-Tail Boundary Term (`Candidate IV`)**:
   With $e(x) := E(x)/x = \psi(x)/x - 1$ and $k(\alpha) := \alpha^{-1/2}\widetilde{h}_0(\alpha)$, for every $X \ge 1$ both $\int_{1/X}^\infty e(X\alpha)k(\alpha)\,d\alpha$ and $\int_{1/X}^\infty e(X)k(\alpha)\,d\alpha$ converge absolutely since $e(x) = O(1)$ on $[1, \infty)$ and $|k(\alpha)| \le \frac{1032993}{65536}\alpha^{-3}$ as $\alpha \to \infty$. Using $\int_0^\infty k(\alpha)\,d\alpha = 0$ ($\int_{1/X}^\infty k(\alpha)\,d\alpha = -\int_0^{1/X} k(\alpha)\,d\alpha$) gives
   $$
   \boxed{I(X) = \sqrt{X}\int_{1/X}^\infty \bigl[e(X\alpha) - e(X)\bigr] k(\alpha)\,d\alpha - \sqrt{X}\,e(X)\int_0^{1/X} k(\alpha)\,d\alpha =: I_{\mathrm{inc}}(X) + B_{\mathrm{zm}}(X).}
   $$
   Integrating $\alpha^{-1}k(\alpha) = -\frac{d}{d\alpha}\bigl(\alpha^{-1/2}h_0(\alpha)\bigr)$ by parts on $[0, 1/X]$ proves the exact **Lower-Tail Boundary Identity**:
   $$
   \sqrt{X}\int_0^{1/X} k(\alpha)\,d\alpha = \int_0^1 x^{-1/2}h_0(x/X)\,dx - h_0(1/X) = -B_{\mathrm{boundary}}(X),
   $$
   where $W(X) = B_{\mathrm{boundary}}(X) + I(X)$ and $|B_{\mathrm{boundary}}(X)| \le \frac{92193}{24576}X^{-5/2}$ for all $X \ge 1$. Hence $B_{\mathrm{zm}}(X) = e(X)\,B_{\mathrm{boundary}}(X) = O(X^{-5/2})$ is uniformly bounded and decays rapidly as $X \to \infty$.

2. **Chordal Prime-Power Stieltjes Equivalence & Exact Reappearance of $W(X)$ (`zero_moment_subtracted_and_chordal_stieltjes_equivalence`)**:
   Preserving the sign structure and decomposing the increment into its prime-power jump chord and smooth dilation drift,
   $$
   e(X\alpha) - e(X) = \frac{\psi(X\alpha) - \psi(X)}{X\alpha} - \left(1 - \frac{1}{\alpha}\right)\frac{\psi(X)}{X}, \qquad I_{\mathrm{inc}}(X) = I_{\mathrm{chord}}(X) - I_{\mathrm{drift}}(X),
   $$
   we evaluate both integrals in closed form:
   - Using $\int_{1/X}^\infty k(\alpha)\,d\alpha = B_{\mathrm{boundary}}(X)/\sqrt{X}$ and $\int_{1/X}^\infty \alpha^{-1}k(\alpha)\,d\alpha = \bigl[-\alpha^{-1/2}h_0(\alpha)\bigr]_{1/X}^\infty = \sqrt{X}\,h_0(1/X)$,
     $$
     I_{\mathrm{drift}}(X) := \sqrt{X}\frac{\psi(X)}{X}\int_{1/X}^\infty \left(1 - \frac{1}{\alpha}\right)k(\alpha)\,d\alpha = \frac{\psi(X)}{X}\,B_{\mathrm{boundary}}(X) - \psi(X)h_0(1/X) = O(X^{-3/2}).
     $$
   - By the exact $x$-variable differential identity $x^{-3/2}\widetilde{h}_0(x/X)\,dx = -d\bigl[x^{-1/2}h_0(x/X)\bigr]$ (with **no** extraneous $\sqrt{X}$ factor, since $\frac{d}{dx}\bigl[x^{-1/2}h_0(x/X)\bigr] = -\frac{1}{2}x^{-3/2}h_0(x/X) + x^{-3/2}(x/X)h_0'(x/X) = -x^{-3/2}\widetilde{h}_0(x/X)$), Stieltjes integration by parts of $\psi(x) - \psi(X)$ on $[1, \infty)$ gives $\bigl[-(\psi(x) - \psi(X))x^{-1/2}h_0(x/X)\bigr]_1^\infty + \int_1^\infty x^{-1/2}h_0(x/X)\,d\psi(x)$ (with lower-endpoint term $+\bigl(\psi(1) - \psi(X)\bigr)h_0(1/X) = -\psi(X)h_0(1/X)$ since $\psi(1) = 0$, and jump sum $\sum_{n\ge 2}\frac{\Lambda(n)}{\sqrt{n}}h_0(n/X) = W(X)$):
     $$
     I_{\mathrm{chord}}(X) := \sqrt{X}\int_{1/X}^\infty \frac{\psi(X\alpha) - \psi(X)}{X\alpha}\,k(\alpha)\,d\alpha = \int_1^\infty \bigl(\psi(x) - \psi(X)\bigr)\,x^{-3/2}\widetilde{h}_0(x/X)\,dx = W(X) - \psi(X)h_0(1/X).
     $$
   Subtracting $I_{\mathrm{drift}}(X)$ from $I_{\mathrm{chord}}(X)$ cancels the $O(X^{-3/2})$ endpoint term $-\psi(X)h_0(1/X)$ identically and proves:
   $$
   \boxed{I_{\mathrm{inc}}(X) = I_{\mathrm{chord}}(X) - I_{\mathrm{drift}}(X) = W(X) - \frac{\psi(X)}{X}\,B_{\mathrm{boundary}}(X) = I(X) - e(X)\,B_{\mathrm{boundary}}(X).}
   $$
   Thus subtracting the zero moment and splitting into prime-power increments isolates the harmless $O(X^{-5/2})$ lower-tail boundary term $B_{\mathrm{zm}}(X)$, while the full prime-wavelet sum $W(X)$ **reappears identically** inside the chordal jump integral $I_{\mathrm{chord}}(X)$.

3. **Next Justified Refinement — Chebyshev Primitive Transfer $e_1(x) = E_1(x)/x^2$**:
   Define $E_1(x) := \int_1^x E(t)\,dt = \int_1^x [\psi(t) - t]\,dt$ ($E_1(1) = 0$), so that $\psi_1(x) := \int_1^x \psi(t)\,dt = \frac{x^2 - 1}{2} + E_1(x)$, and define the normalized primitive error $e_1(x) := E_1(x)/x^2$, which satisfies $(2 + D_x)e_1(x) = e(x)$. Integrating by parts on $[1/X, \infty)$ transfers $(2 + D_\alpha)$ to its $d\alpha$-adjoint $(1 - D_\alpha)$ with zero lower boundary term at $\alpha = 1/X$ (since $e_1(1) = 0$):
   $$
   k_1(\alpha) := (1 - D_\alpha)k(\alpha) = \alpha^{-1/2}\!\left(\frac{3}{2} - D_\alpha\right)\!\left(\frac{1}{2} - D_\alpha\right)h_0(\alpha) = \alpha^{-1/2}h_1(\alpha), \qquad \int_0^\infty k_1(\alpha)\,d\alpha = 0,
   $$
   $$
   \boxed{I(X) = \sqrt{X}\int_{1/X}^\infty e_1(X\alpha)\,k_1(\alpha)\,d\alpha = \sqrt{X}\int_{1/X}^\infty \bigl[e_1(X\alpha) - e_1(X)\bigr] k_1(\alpha)\,d\alpha - \sqrt{X}\,e_1(X)\int_0^{1/X} k_1(\alpha)\,d\alpha,}
   $$
   where $\int_0^{1/X} k_1(\alpha)\,d\alpha = 2\int_0^{1/X} k(\alpha)\,d\alpha - \frac{1}{X}k(1/X) = O(X^{-3})$ (all verified to 256-bit Arb precision across $X \in \{1, 2, 4, \tau\}$).
   - **What Improves**: Unlike $e(x) = E(x)/x$, which has jump discontinuities at every prime power and only conditionally convergent zero sum $-\sum_\rho \frac{x^{\rho-1}}{\rho}$, the normalized primitive $e_1(x) = E_1(x)/x^2$ is continuous, piecewise $C^1$, and has the **unconditionally and absolutely convergent** explicit expansion $e_1(x) = -\sum_\rho \frac{x^{z_\rho - 1/2}}{\rho(\rho+1)} + O(x^{-1})$ ($\sum_\rho |\rho(\rho+1)|^{-1} < \infty$).
   - **Where the Obligation Reappears**: With $z_\rho = \rho - \tfrac{1}{2}$, Mellin integration of $\alpha^{z_\rho - 1/2}$ against $k_1(\alpha) = \alpha^{-1/2}h_1(\alpha)$ multiplies $H_0(z_\rho)$ by $\mathcal{M}[h_1](z_\rho) = \bigl(z_\rho + \tfrac{1}{2}\bigr)\bigl(z_\rho + \tfrac{3}{2}\bigr)H_0(z_\rho) = \rho(\rho+1)H_0(z_\rho)$ (note that $\bigl(z_\rho + \tfrac{1}{2}\bigr)\bigl(z_\rho + \tfrac{3}{2}\bigr) = \rho(\rho+1)$, whereas $z_\rho(1+z_\rho) = \rho^2 - \tfrac{1}{4} \ne \rho(\rho+1)$), cancelling $\frac{1}{\rho(\rho+1)}$ and preserving $X^{z_\rho}H_0(z_\rho)$; spatially, since $c_1 := \int_{1/2}^2 |k_1(\alpha)|\,d\alpha = 11.4897566721 \pm 5.30 \times 10^{-48} > 0$ ($C_{1,\mathrm{abs}} = \int_0^\infty |k_1(\alpha)|\,d\alpha = 14.7563989427 \pm 5.99 \times 10^{-46}$), any monotone unsigned envelope $|e_1(x)| \le \omega_1(x)$ with $\sqrt{X}\omega_1(2X) \to \infty$ still yields a majorant $\ge c_1\sqrt{X}\,\omega_1(2X) \to \infty$.

---

## 11. Arithmetic Cross-Grade Compatibility and the Prime-Shift Quadratic Form (`TASK-TC-044`, `Section 13`)

### 11.1 Baseline Recovery & Sufficient Relative Semiboundedness vs. Full Weil Positivity (`Section 13.1`)
On the normalized two-grade test states $f_\pm^{(K)} = \frac{\psi_\tau \pm T_K\psi_\tau}{\sqrt{2}} \in \mathcal{S}_\tau$ ($K \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}}\cap\mathbb{R}$), the complete explicit-formula pairing splits as
$$
Q_\tau\bigl(f_\pm^{(K)}, f_\pm^{(K)}\bigr) = C_\tau(0) \pm C_\tau(K) = \|A_\tau^B f_\pm^{(K)}\|_{\mathcal{H}_\tau^B}^2 - c_\tau^B\|f_\pm^{(K)}\|_{L^2(d^\times x)}^2 + P_E\bigl(f_\pm^{(K)}\bigr),
$$
where $c_\tau^B = \log(4\tau) + \gamma_E + \frac{\tau}{4} - 2 = 3.3721834192256654 \pm 3.92 \times 10^{-56}$ and $P_E(f) = -W_{\mathrm{prime}}(f * f^*) + B_{\mathrm{transfer}}(f)$.
- **Full Weil Positivity (`OBL-TC-020-WEIL-FACTORIZATION`)**: Requires $Q_\tau(f, f) \ge 0$ for all $f \in \mathcal{D}$, which forces $|C_\tau(K)| \le C_\tau(0)$ directly via 2D Cauchy–Schwarz (`two_dim_gram_cauchy_schwarz_from_nonneg`).
- **Sufficient Relative Semiboundedness (`SUBGATE-TC-043A`)**: Requires only the weaker **one-way sufficient condition**
  $$
  \boxed{\exists \mu_0 \in [0, \infty) \quad \forall K \in \mathbb{A}_{\mathbb{R}} : \qquad P_E\bigl(f_\pm^{(K)}\bigr) \ge -\Bigl(\|A_\tau^B f_\pm^{(K)}\|_{\mathcal{H}_\tau^B}^2 + \mu_0\|f_\pm^{(K)}\|_{L^2}^2\Bigr),}
  $$
  which allows $Q_\tau\bigl(f_\pm^{(K)}, f_\pm^{(K)}\bigr)$ to be negative down to $-(c_\tau^B + \mu_0)\|f_\pm^{(K)}\|_{L^2}^2 \ge -2(c_\tau^B + \mu_0)h_0(1)$ while still forcing the uniform correlation bound $|C_\tau(K)| \le C_\tau(0) + 2(c_\tau^B + \mu_0)h_0(1) < \infty$ (`coercive_norm_shift_semiboundedness_implies_correlation_bound`) and therefore excluding all off-critical zeros via the Laplace–Carleman resolvent theorem. Meanwhile, uniform boundedness of $W(\tau^{|K|}) = \sum_{n\ge 2}\frac{\Lambda(n)}{\sqrt{n}}h_0(n/\tau^{|K|})$ (equivalently $R_\mu(\tau^{|K|})$) across $K \in \mathbb{A}_{\mathbb{R}}$ (`SUBGATE-TC-042B`) forces the correlation bound $|C_\tau(K)| \le 9.27739781 + M_\mu$ directly through the mixed-grade identity $C_\tau(K - L) = B_{\mathrm{known}}(K, L) - R_\mu(\tau^{|K-L|})$ (`mixed_grade_pairing_moebius_recovery_and_semiboundedness_equivalence`) without dividing by $\|f_-^{(K)}\|_{L^2}^2 = h_0(1) - h_0(\tau^{|K|})$ (which vanishes as $K \to 0$).

### 11.2 The Prime-Shift Quadratic Form $D_N(f)$ and Subtracted Finite-Part Analysis (`Section 13.2`, `prime_shift_quadratic_form_and_subtracted_finite_part_equivalence`)
On $L^2((0, \infty), d^\times x)$ ($d^\times x = dx/x$), define the unitary prime-power dilation shifts $(S_n f)(x) := f(nx)$ ($\|S_n f\|_{L^2} = \|f\|_{L^2}$, $S_n^* = S_n^{-1}$) and actual prime-power weights $w_n := \frac{\Lambda(n)}{\sqrt{n}}$ for $n \ge 2$. For any finite cutoff $N \ge 2$, define
$$
D_N(f) := \sum_{2 \le n \le N} w_n\,\|(I - S_n)f\|_{L^2(d^\times x)}^2 \ge 0, \qquad L_N := \sum_{2 \le n \le N} w_n = \sum_{2 \le n \le N}\frac{\Lambda(n)}{\sqrt{n}}.
$$
1. **Exact Norm-Correlation Expansion**:
   Since $\|(I - S_n)f\|_{L^2}^2 = \|f\|_{L^2}^2 + \|S_n f\|_{L^2}^2 - 2\operatorname{Re}\langle f, S_n f\rangle_{L^2} = 2\|f\|_{L^2}^2 - 2\operatorname{Re}\langle f, S_n f\rangle_{L^2}$, summing over $2 \le n \le N$ gives
   $$
   D_N(f) = 2L_N\|f\|_{L^2(d^\times x)}^2 - 2\sum_{2 \le n \le N} w_n\operatorname{Re}\langle f, S_n f\rangle_{L^2(d^\times x)}.
   $$
2. **Translation to the Repository's Prime Contribution $W_{\mathrm{prime}, N}(f * f^*)$**:
   With $f^*(y) = \overline{f(1/y)}$ and $(f * f^*)(x) = \int_0^\infty f(xy)\overline{f(y)}\,\frac{dy}{y} = \langle S_x f, f\rangle_{L^2}$, we have $(f * f^*)(1/x) = \overline{(f * f^*)(x)} = \langle f, S_x f\rangle_{L^2}$, so $\Phi_{f,f}(n) := (f * f^*)(n) + (f * f^*)(1/n) = 2\operatorname{Re}\langle f, S_n f\rangle_{L^2}$. Therefore the correlation sum is **literally** the repository's truncated prime-power functional:
   $$
   \boxed{W_{\mathrm{prime}, N}(f * f^*) := \sum_{2 \le n \le N}\frac{\Lambda(n)}{\sqrt{n}}\,\Phi_{f,f}(n) = 2\sum_{2 \le n \le N} w_n\operatorname{Re}\langle f, S_n f\rangle_{L^2}, \qquad D_N(f) - 2L_N\|f\|_{L^2}^2 = -W_{\mathrm{prime}, N}(f * f^*).}
   $$
3. **Relationship to $P_E(f)$ and $Q_\tau(f, f)$ on $\mathcal{S}_\tau$**:
   Passing to the rapidly convergent limit $N \to \infty$ on $\mathcal{S}_\tau$:
   $$
   \lim_{N\to\infty}\bigl(D_N(f) - 2L_N\|f\|_{L^2}^2\bigr) = -W_{\mathrm{prime}}(f * f^*) = P_E(f) - B_{\mathrm{transfer}}(f),
   $$
   $$
   \boxed{Q_\tau(f, f) = \|A_\tau^B f\|_{\mathcal{H}_\tau^B}^2 - c_\tau^B\|f\|_{L^2}^2 + B_{\mathrm{transfer}}(f) + \lim_{N\to\infty}\bigl(D_N(f) - 2L_N\|f\|_{L^2}^2\bigr).}
   $$
4. **Central Question Resolution — Does Canonical Completion Control the Subtracted Finite Part from $D_N(f) \ge 0$ Alone?**:
   **No.** While $D_N(f) \ge 0$ is unconditionally positive by construction, subtracting $2L_N\|f\|_{L^2}^2$ gives only the trivial lower bound
   $$
   D_N(f) - 2L_N\|f\|_{L^2}^2 = -W_{\mathrm{prime}, N}(f * f^*) \ge -2L_N\|f\|_{L^2}^2,
   $$
   where $L_N = \sum_{2\le n\le N}\frac{\Lambda(n)}{\sqrt{n}} = 2\sqrt{N} + O\bigl(\sqrt{N}/\log N\bigr) \to +\infty$ as $N \to \infty$. Even at a scale-matched finite cutoff $N(K) \asymp \tau^{|K|}$ required to resolve the shifted packet $T_K\psi_\tau$ supported near $x \asymp \tau^{-K}$, the subtracted term $-2L_{N(K)}\|f_\pm^{(K)}\|_{L^2}^2 \asymp -4\tau^{|K|/2}h_0(1) \to -\infty$ (reaching $-91.0368$ already at $K = 3, N(3) = 2480$), whereas the canonical Attempt B completion $\|A_\tau^B f_\pm^{(K)}\|_{\mathcal{H}_\tau^B}^2 - c_\tau^B\|f_\pm^{(K)}\|_{L^2}^2 + B_{\mathrm{transfer}}(f_\pm^{(K)}) = W_{\mathrm{arch}}(f_\pm^{(K)} * (f_\pm^{(K)})^*)$ remains $O(1)$ (`-0.113664` as $|K| \to \infty$). On $f = \psi_\tau$, the subtracted difference $D_N(\psi_\tau) - 2L_N\|\psi_\tau\|_{L^2}^2$ converges to $-2W(1) = +0.1146149592409334$ solely because the **correlation sum** $2\sum_{n\le N} w_n\operatorname{Re}\langle\psi_\tau, S_n\psi_\tau\rangle = 2W_{\le N}(1) = -0.1146149592409334$ converges by PNT zero-moment cancellation ($H_0(1/2) = 0$), not because $D_N(f) \ge 0$ controls $2L_N\|f\|_{L^2}^2$.

### 11.3 Concrete Arithmetic Compatibility Candidate — Divisor-Aggregated Functional $W_{\log}(X)$ & Exact Möbius Inversion (`Section 13.3`, `divisor_aggregated_stieltjes_and_moebius_inversion_identity`)
Because $D_N(f) \ge 0$ uses only the Hilbert-space norm of individual shifts $S_n$ without using multiplicative prime-factorization relations across grades, we investigate the concrete arithmetic candidate induced by the **fundamental divisor-sum identity of the von Mangoldt function**:
$$
\sum_{d \mid k} \Lambda(d) = \log k \qquad (\forall k \ge 1).
$$
1. **Cross-Scale Divisor-Aggregated Functional $W_{\log}(X)$**:
   Aggregating $W(X/m) = \sum_{n\ge 2}\frac{\Lambda(n)}{\sqrt{n}}h_0\!\left(\frac{mn}{X}\right)$ along the harmonic divisor lattice $X \mapsto X/m$ ($m \ge 1$) with weight $m^{-1/2}$ yields ($k = mn$):
   $$
   \boxed{W_{\log}(X) := \sum_{m=1}^\infty \frac{1}{\sqrt{m}}\,W\!\left(\frac{X}{m}\right) = \sum_{k=2}^\infty \frac{\sum_{d\mid k}\Lambda(d)}{\sqrt{k}}\,h_0\!\left(\frac{k}{X}\right) = \sum_{k=2}^\infty \frac{\log k}{\sqrt{k}}\,h_0\!\left(\frac{k}{X}\right).}
   $$
2. **Unconditional Proof that $W_{\log}(X) = O\bigl(X^{-1/2}\log(X+2)\bigr) \to 0$ across All Scales $X \ge 1$**:
   - **Double Vanishing of Zeroth and First Logarithmic Moments at $z = 1/2$**: Since $H_0(z) = \int_0^\infty \alpha^{z - 1}h_0(\alpha)\,d\alpha$ has a **triple zero** at $z = \pm 1/2$, both the zeroth and first logarithmic moments vanish identically:
     $$
     H_0(1/2) = \int_0^\infty \alpha^{-1/2}h_0(\alpha)\,d\alpha = 0, \qquad H_0'(1/2) = \int_0^\infty \alpha^{-1/2}(\log\alpha)\,h_0(\alpha)\,d\alpha = 0.
     $$
     Consequently, $\int_0^\infty x^{-1/2}(\log x)\,h_0(x/X)\,dx = \sqrt{X}(\log X)H_0(1/2) + \sqrt{X}H_0'(1/2) = 0$ vanishes identically for every $X > 0$!
   - **Stieltjes Integration by Parts with Stirling's Log-Sum Error $E_{\log}(x)$**:
     Write $\vartheta_{\log}(x) := \sum_{2\le k\le x}\log k = \log\lfloor x\rfloor! = \int_1^x \log t\,dt + E_{\log}(x)$ where $\int_1^x \log t\,dt = x\log x - x + 1$ and $E_{\log}(1) = 0$. By Robbins (1955) / Euler–Maclaurin Stirling bounds, the log-sum remainder satisfies the **unconditional** $O(\log x)$ bound
     $$
     |E_{\log}(x)| \le \frac{1}{2}\log x + 1 \qquad (\forall x \ge 1),
     $$
     in stark contrast to Chebyshev's prime error $E(x) = \psi(x) - x = O\bigl(x\exp(-c\sqrt{\log x})\bigr)$. Integrating $W_{\log}(X) = \int_1^\infty x^{-1/2}h_0(x/X)\,d\vartheta_{\log}(x)$ by parts on $[1, \infty)$ using $x^{-3/2}\widetilde{h}_0(x/X)\,dx = -d\bigl[x^{-1/2}h_0(x/X)\bigr]$ and $E_{\log}(1) = 0$ yields the exact identity:
     $$
     \boxed{W_{\log}(X) = B_{\log,\mathrm{boundary}}(X) + I_{\log}(X), \qquad B_{\log,\mathrm{boundary}}(X) := -\int_0^1 x^{-1/2}(\log x)\,h_0(x/X)\,dx, \qquad I_{\log}(X) := \int_1^\infty E_{\log}(x)\,x^{-3/2}\widetilde{h}_0(x/X)\,dx.}
     $$
   - **Certified Explicit Bounds**:
     - For $x \in (0, 1]$ and $X \ge 1$, $|h_0(x/X)| \le \frac{92193}{32768}(x/X)^{5/2}$ and $\int_0^1 x^2(-\log x)\,dx = \frac{1}{9}$, proving
       $$
       \bigl|B_{\log,\mathrm{boundary}}(X)\bigr| \le \frac{92193}{294912}\,X^{-5/2} = \frac{30731}{98304}\,X^{-5/2} \approx 0.3126119\,X^{-5/2} \qquad (\forall X \ge 1).
       $$
     - Changing variables $x = X\alpha$ in $I_{\log}(X)$ gives $I_{\log}(X) = X^{-1/2}\int_{1/X}^\infty E_{\log}(X\alpha)\,\alpha^{-3/2}\widetilde{h}_0(\alpha)\,d\alpha$. Since $\alpha^{-3/2}\widetilde{h}_0(\alpha) = -\frac{d}{d\alpha}\bigl(\alpha^{-1/2}h_0(\alpha)\bigr)$, the total variation of $\alpha^{-1/2}h_0(\alpha)$ on $(0, \infty)$ across the 7 positive roots $\alpha_1 < \dots < \alpha_7$ of $\widetilde{h}_0(\alpha) = 0$ gives the exact certified moments:
       $$
       M_{\widetilde{h},0}^{(-3/2)} := \int_0^\infty \alpha^{-3/2}\bigl|\widetilde{h}_0(\alpha)\bigr|\,d\alpha = 2\sum_{j=1}^7 \bigl|\alpha_j^{-1/2}h_0(\alpha_j)\bigr| = 2.4304910449396404 \pm 1.0 \times 10^{-47},
       $$
       $$
       M_{\widetilde{h},\log}^{(-3/2)} := \int_0^\infty \alpha^{-3/2}|\log\alpha|\,\bigl|\widetilde{h}_0(\alpha)\bigr|\,d\alpha = 1.2118101520691849 \pm 1.71 \times 10^{-20}.
       $$
     - Combining these with $|E_{\log}(X\alpha)| \le \frac{1}{2}\log X + \frac{1}{2}|\log\alpha| + 1$ establishes the **unconditional theorem** for all $X \ge 1$:
       $$
       \boxed{\bigl|W_{\log}(X)\bigr| \le \frac{30731}{98304}\,X^{-5/2} + X^{-1/2}\!\left(\frac{1}{2}M_{\widetilde{h},0}^{(-3/2)}\log X + M_{\widetilde{h},0}^{(-3/2)} + \frac{1}{2}M_{\widetilde{h},\log}^{(-3/2)}\right) \le 3.34901 \qquad (\forall X \ge 1),}
       $$
       with $\lim_{X\to\infty} W_{\log}(X) = 0$.
3. **Exact Möbius Inversion Identity & Where the Arithmetic Obligation Concentrates**:
   By $\sum_{d\mid m}\mu(d) = \delta_{m,1}$ and absolute convergence of $\sum_{m,n\ge 1} m^{-1/2}n^{-1/2}\Lambda(n)\bigl|h_0(mn/X)\bigr| < \infty$, $W(X)$ is recovered from $W_{\log}(X/m)$ by **exact Möbius inversion**:
   $$
   \boxed{W(X) = \sum_{m=1}^\infty \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right) = W_{\log}(X) + \sum_{m=2}^\infty \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right).}
   $$
   - **Why Naive Triangle Inequality Fails on Möbius De-Aggregation**: Substituting the unconditional upper bound $|W_{\log}(Y)| \le C\,Y^{-1/2}\log(Y+2)$ for $1 \le m \le X$ with $|\mu(m)| \le 1$ yields the unsigned sum
     $$
     \sum_{1 \le m \le X} \frac{1}{\sqrt{m}}\left(\frac{X}{m}\right)^{-1/2}\log\!\left(\frac{X}{m} + 2\right) = X^{-1/2}\sum_{1 \le m \le X}\log\!\left(\frac{X}{m} + 2\right) = O(X^{1/2}),
     $$
     diverging as $O(X^{1/2})$ because $\sum_{m\le X} 1 = X$. Thus **harmonic divisor aggregation $W \mapsto W_{\log}$ is unconditionally $O(X^{-1/2}\log X) \to 0$**, and the entire open arithmetic obligation of `SUBGATE-TC-043A` / `SUBGATE-TC-042B` concentrates into signed cancellation of $\mu(m)$ across the de-aggregation sum $\sum_{m\ge 2}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$.

### 11.4 Four-Category Premise Classification & Next Focused Mathematical Lemma (`Section 13.4`)
Every statement in `TASK-TC-044` is classified into four disjoint categories:
1. **Category (i) — Already Proved in the Repository**:
   - Relative semiboundedness one-way reduction $P_E(f_\pm^{(K)}) \ge -(\|A_\tau^B f_\pm^{(K)}\|^2 + \mu_0\|f_\pm^{(K)}\|^2) \implies |C_\tau(K)| \le C_\tau(0) + 2(c_\tau^B + \mu_0)h_0(1)$ (`coercive_norm_shift_semiboundedness_implies_correlation_bound`).
   - Equivalence of uniform boundedness of $W(X)$ with uniform boundedness of the Stieltjes signed pairing $I(X)$ (`stieltjes_signed_pairing_uniform_bound_equivalence`), and direct mixed-grade bound $|C_\tau(K - L) + R_\mu(\tau^{|K-L|})| = |B_{\mathrm{known}}(K, L)| \le 9.27739781$ (`mixed_grade_pairing_moebius_recovery_and_semiboundedness_equivalence`, avoiding division by $\|f_-^{(K)}\|_{L^2}^2 \to 0$ as $K \to 0$).
   - Chordal Stieltjes equivalence $I_{\mathrm{inc}}(X) = W(X) - \frac{\psi(X)}{X}B_{\mathrm{boundary}}(X)$ (`zero_moment_subtracted_and_chordal_stieltjes_equivalence`).
   - Laplace–Carleman resolvent exclusion of off-critical zeros under uniform correlation boundedness (`fixed_seed_correlation_bound_implies_critical_line_schema`).
2. **Category (ii) — Unconditional External Theorems Cited Precisely**:
   - **Fundamental Divisor-Sum Identity**: $\sum_{d\mid k}\Lambda(d) = \log k$ for all $k \ge 1$ (Hardy & Wright 2008, Thm. 296).
   - **Möbius Inversion Formula**: $\sum_{d\mid m}\mu(d) = \delta_{m,1}$ and $\Lambda(k) = \sum_{d\mid k}\mu(d)\log(k/d)$ (Hardy & Wright 2008, Thms. 263 & 297).
   - **Stirling / Robbins Factorial Remainder Bound**: $\log n! = n\log n - n + \frac{1}{2}\log(2\pi n) + \theta_n/(12n)$ ($0 < \theta_n < 1$, Robbins 1955), implying $|E_{\log}(x)| \le \frac{1}{2}\log x + 1$ for all $x \ge 1$.
   - **Rosser–Schoenfeld (1962) Explicit Chebyshev Bounds**: Thm. 12 ($\psi(x) < 1.03883\,x$ for $x > 0$) and Thm. 10 (two-sided bound for $x \ge 2$).
3. **Category (iii) — New Statements Proved Unconditionally in `TASK-TC-044`**:
   - **Prime-Shift Quadratic Form & Subtracted Finite-Part Identity**: $D_N(f) - 2L_N\|f\|_{L^2}^2 = -W_{\mathrm{prime}, N}(f * f^*)$ and $Q_\tau(f, f) = \|A_\tau^B f\|^2 - c_\tau^B\|f\|^2 + B_{\mathrm{transfer}}(f) + \lim_{N\to\infty}(D_N(f) - 2L_N\|f\|^2)$, with proof that $D_N(f) \ge 0$ alone gives only $-2L_N\|f\|_{L^2}^2 \to -\infty$ (`prime_shift_quadratic_form_and_subtracted_finite_part_equivalence`).
   - **Unconditional Uniform Bound & $O(X^{-1/2}\log X)$ Decay of Divisor-Aggregated $W_{\log}(X)$**: $|W_{\log}(X)| \le \frac{30731}{98304}X^{-5/2} + X^{-1/2}\bigl(\frac{1}{2}M_{\widetilde{h},0}^{(-3/2)}\log X + M_{\widetilde{h},0}^{(-3/2)} + \frac{1}{2}M_{\widetilde{h},\log}^{(-3/2)}\bigr) \le 3.34901$ for all $X \ge 1$ (`divisor_aggregated_stieltjes_and_moebius_inversion_identity` + 256-bit Arb moment enclosures).
   - **Exact Cross-Scale Möbius Inversion Identity**: $W(X) = \sum_{m=1}^\infty \frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ for all $X > 0$.
4. **Category (iv) — Unproved Premise (Next Focused Mathematical Lemma for `SUBGATE-TC-043A` / `SUBGATE-TC-042B`)**:
   - **Möbius De-Aggregation Cancellation Lemma**:
     $$
     \boxed{\sup_{X \ge 1}\left|\sum_{m=2}^\infty \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right)\right| < \infty.}
     $$

### 11.5 Diagnostic Controls — Modified Weights vs. Authentic $\Lambda(n)/\sqrt{n}$ and Synthetic Off-Critical Quartet Under Divisor Aggregation (`Section 13.5`)
| Scale $X$ | Authentic $W(X)$ ($\frac{\Lambda(n)}{\sqrt{n}}$) | Divisor-Aggregated $W_{\log}(X)$ ($\frac{\log k}{\sqrt{k}}$, **PROVED $O(X^{-1/2}\log X)$**) | Unweighted $W_{\mathrm{unit}}(X)$ ($\frac{1}{\sqrt{n}}$, **CONTROL**, $O(X^{-1/2})$) | Unsigned Möbius Majorant $\sum_{m=1}^{200}\frac{|\mu(m)|}{\sqrt{m}}|W_{\log}(X/m)|$ |
| :--- | :--- | :--- | :--- | :--- |
| $X = 1$ | $-0.057307455318$ | $-0.044061156600$ (cert: $-0.044061379 \pm 5.38\times 10^{-9}$) | $-0.103362365060$ | $+0.061397347638$ |
| $X = 2$ | $+0.079372001214$ | $+0.070509661671$ (cert: $+0.070508401 \pm 3.04\times 10^{-8}$) | $+0.178682055439$ | $+0.129600184365$ |
| $X = \tau \approx 6.2832$ | $-0.012079386190$ | $-0.000706958056$ (cert: $-0.000729007 \pm 5.32\times 10^{-7}$) | $-0.006980150157$ | $+0.155417346475$ |
| $X = 10$ | $-0.002408453742$ | $-0.000083266284$ (cert: $-0.000153717 \pm 1.70\times 10^{-6}$) | $+0.000861813453$ | $+0.149154208225$ |
| $X = 100$ | $+0.003121797023$ | $+0.022411024261$ (cert: $+0.000536768 \pm 5.38\times 10^{-4}$) | $+0.002496628804$ | $+0.893336077631$ |

- **Spectral Aggregation via Common Mellin Strip $\frac{1}{2} < \operatorname{Re}(z) < \frac{5}{2}$, Meromorphic Continuation, and Synthetic Off-Critical Quartet Regularization (Repaired in `TASK-TC-045` Defect 3A & `TASK-TC-045R` Step 5)**:
  Define the scale Mellin transform and kernel Mellin transform explicitly:
  $$
  \mathcal{M}_X[F](z) := \int_0^\infty F(X)\,X^{-z}\,\frac{dX}{X}, \qquad H_0(z) := \int_0^\infty h_0(\alpha)\,\alpha^z\,\frac{d\alpha}{\alpha} = F_\tau\!\left(\frac{1}{2} + z\right)F_\tau\!\left(\frac{1}{2} - z\right).
  $$
  Because $|h_0(\alpha)| \le \frac{92193}{32768}(\alpha + \alpha^{-1})^{-5/2}$, $H_0(z)$ converges absolutely on the open kernel strip $|\operatorname{Re}(z)| < \frac{5}{2}$ and $\mathcal{M}_X[h_0(n/X)](z) = n^{-z}H_0(z)$. For $\operatorname{Re}(z) > \frac{1}{2}$ ($\sigma = \operatorname{Re}(z) + \frac{1}{2} > 1$), $\sum_{n\ge 2}\Lambda(n)n^{-(z+1/2)} = -\frac{\zeta'(z+1/2)}{\zeta(z+1/2)}$ and $\sum_{k\ge 2}(\log k)k^{-(z+1/2)} = -\zeta'(z+1/2)$ converge absolutely. Thus on the **common absolute-convergence strip $\frac{1}{2} < \operatorname{Re}(z) < \frac{5}{2}$**, Fubini–Tonelli interchange yields
  $$
  \mathcal{M}_X[W](z) = -H_0(z)\,\frac{\zeta'(z + 1/2)}{\zeta(z + 1/2)}, \qquad \mathcal{M}_X[W_{\log}](z) = \left(\sum_{m=1}^\infty m^{-(z+1/2)}\right)\mathcal{M}_X[W](z) = -H_0(z)\,\zeta'(z + 1/2).
  $$
  - **Holomorphic Continuation on the Open Kernel Strip $|\operatorname{Re}(z)| < \frac{5}{2}$ vs. Global Meromorphic Structure on $\mathbb{C}$ (`TASK-TC-045R` Step 5)**:
    By analytic/meromorphic continuation from $\frac{1}{2} < \operatorname{Re}(z) < \frac{5}{2}$, harmonic divisor aggregation cancels the poles of $-\zeta'(z+1/2)/\zeta(z+1/2)$ at all actual nontrivial zeros $\rho = \frac{1}{2} + z_\rho$ of $\zeta(s)$ **irrespective of their real parts**, and inside the open kernel strip $|\operatorname{Re}(z)| < \frac{5}{2}$ the triple zero $H_0(1/2) = H_0'(1/2) = H_0''(1/2) = 0$ cancels the double pole of $-\zeta'(z+1/2)$ at $z = 1/2$, making $-H_0(z)\zeta'(z+1/2)$ **holomorphic on the open strip $|\operatorname{Re}(z)| < \frac{5}{2}$**.
    Globally on $\mathbb{C}$, however, $h_0(\alpha) = -\frac{81}{64}\alpha^{\mp 5/2} + O(\alpha^{\mp 9/2})$ has power-law $5/2$ decay as $\alpha \to \infty$ and $\alpha \downarrow 0$ (`H_0(z) = F_\tau(1/2 + z)F_\tau(1/2 - z)` where $F_\tau(s) = \frac{s^2(s-1)^2}{32}\pi^{-s/2}\Gamma(s/2)$ has simple poles from $\Gamma(s/2)$ at $s = -2k \le -2$), so $H_0(z)$ is **meromorphic on $\mathbb{C}$ with simple poles at $z = \pm(2k + 1/2)$ ($k \ge 1$)**. In particular, at the strip boundary point $z = 5/2$ ($s = z + 1/2 = 3$), $H_0(z) \sim \int_1^\infty (-\frac{81}{64}\alpha^{-5/2})\alpha^{z-1}\,d\alpha = \frac{+81/64}{z - 5/2}$ has a simple pole with exact residue $\operatorname*{Res}_{z=5/2} H_0(z) = +\frac{81}{64}$ while $-\zeta'(3) = +0.19812624288563685 \pm 1.15 \times 10^{-41} \ne 0$, so $-H_0(z)\zeta'(z+1/2) = H_0(z)(-\zeta'(z+1/2))$ is **meromorphic (not entire) on $\mathbb{C}$** with a simple pole at $z = 5/2$ of nonvanishing residue
    $$
    \operatorname*{Res}_{z = 5/2}\bigl[-H_0(z)\,\zeta'(z + 1/2)\bigr] = \frac{81}{64}\bigl(-\zeta'(3)\bigr) = +0.25075352615213414 \pm 1.46 \times 10^{-41} \ne 0.
    $$
    Meanwhile, Möbius inversion $W(X) = \sum_{m\ge 1}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ multiplies by $\sum_{m\ge 1}\mu(m)m^{-(z+1/2)} = 1/\zeta(z+1/2)$ on $\operatorname{Re}(z) > \frac{1}{2}$ and **restores the denominator $\zeta(z+1/2)$** (and thus the poles at all nontrivial zeros $\rho = 1/2 + z_\rho$) under meromorphic continuation.
  On an **isolated homogeneous synthetic mode** $X^{\rho_0 - 1/2}$ with $0 < \operatorname{Re}(\rho_0) < 1$ (e.g., $\rho_0 = 0.7 + 14.1347251417i$), the unsubtracted Dirichlet series $\sum_{m=1}^\infty m^{-\rho_0}$ **diverges** (a numerical value of $\zeta(\rho_0)$ does not make the ordinary series converge on an isolated mode, whereas $\sum_{m\ge 1} m^{-1/2}W(X/m)$ converges on actual $W(X)$ because $W(u) = O(u^{5/2})$ as $u \downarrow 0$). Instead, the **Euler–Maclaurin pole-subtracted regularization**
  $$
  \lim_{M\to\infty}\left(\sum_{m=1}^M m^{-\rho_0} - \frac{M^{1-\rho_0}}{1-\rho_0} - \frac{1}{2}M^{-\rho_0}\right) = \zeta(\rho_0) \ne 0 \qquad \bigl(|\zeta(\rho_0)| = 0.1464535770 > 0.1\bigr)
  $$
  converges and leaves the non-vanishing regularized amplitude $|\zeta(\rho_0)H_0(z_0)| = 6.962515 \times 10^{-5} > 0$.

---

## 12. Cross-Grade Compatibility and Möbius Recovery of the Actual Arithmetic Profile (`TASK-TC-045` / `TASK-TC-045R`, `Section 14`)

### 12.1 Recovered Arithmetic Result & Repaired Direct Implication Chain (`Section 14.1`, Repaired in `TASK-TC-045R` Steps 2, 3 & 4)

1. **Recovered Definitions and Exact Möbius Recovery Equivalence**:
   Using the canonical autocorrelation $h_0(\alpha)$, `TASK-TC-044` established:
   $$
   W(X) = \sum_{n\ge 2}\frac{\Lambda(n)}{\sqrt{n}}\,h_0\!\left(\frac{n}{X}\right), \qquad W_{\log}(X) = \sum_{m\ge 1}\frac{W(X/m)}{\sqrt{m}} = \sum_{k\ge 2}\frac{\log k}{\sqrt{k}}\,h_0\!\left(\frac{k}{X}\right),
   $$
   with the unconditional bound $|W_{\log}(X)| \le 3.3490080247 < 3.34901$ and $W_{\log}(X) = O\bigl(X^{-1/2}\log(X+2)\bigr)$ ($X \ge 1$). Exact Möbius inversion recovers $W(X)$ as
   $$
   \boxed{W(X) = W_{\log}(X) + R_\mu(X), \qquad R_\mu(X) := \sum_{m=2}^\infty \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right).}
   $$
   Because $|W_{\log}(X)| \le M_{\log} < 3.34901$ is unconditionally bounded on $[1, \infty)$, the triangle inequalities
   $$
   |W(X)| \le |W_{\log}(X)| + |R_\mu(X)|, \qquad |R_\mu(X)| \le |W(X)| + |W_{\log}(X)|
   $$
   imply that **uniform boundedness of $R_\mu(X)$ on $[1, \infty)$ is strictly equivalent to uniform boundedness of $W(X)$ on $[1, \infty)$**. Naming $R_\mu(X)$ isolates the $m \ge 2$ signed Möbius recovery remainder and does **not** independently establish the missing estimate.

2. **Repair of the False Uniform Norm Floors on $f_\pm^{(K)}$ (`TASK-TC-045R` / `TASK-TC-045R2` Step 2)**:
   For the coefficient-normalized two-grade states $f_\pm^{(K)} = \frac{\psi_\tau \pm T_K\psi_\tau}{\sqrt{2}} \in \mathcal{S}_\tau$ ($X_K := \tau^{|K|} \ge 1$, $h_0(1) = \frac{92193}{131072\sqrt{2}} = 0.49736248380990124\dots$), the exact $L^2$ norm identity and valid upper bound are
   $$
   \bigl\|f_\pm^{(K)}\bigr\|_{L^2(d^\times x)}^2 = h_0(1) \pm h_0\bigl(\tau^{|K|}\bigr), \qquad 0 \le \bigl\|f_\pm^{(K)}\bigr\|_{L^2(d^\times x)}^2 \le 2h_0(1) = 0.99472496761980248\dots \qquad (\forall K \in \mathbb{A}_{\mathbb{R}}).
   $$
   - For the **plus state** $f_+^{(K)}$, evaluating at the admissible rational grade $K = \pm\tfrac{1}{4} \in \mathbb{A}_{\mathbb{R}}$ yields
     $$
     h_0\bigl(\tau^{1/4}\bigr) = -0.254111585983292\dots, \qquad \bigl\|f_+^{(\pm 1/4)}\bigr\|_{L^2(d^\times x)}^2 = h_0(1) + h_0\bigl(\tau^{1/4}\bigr) = 0.243250897826609\dots \in (0.2432, 0.2433),
     $$
     which disproves the discarded uniform plus-state floor claims ($0.4968506338$, $0.4946950365$, and $0.258495$). No positive lower bound on $\|f_+^{(K)}\|_{L^2}^2$ is needed or claimed, because the repaired direct mixed-grade correlation argument does not divide by $\|f_\pm^{(K)}\|_{L^2}^2$.
   - For the **minus state** $f_-^{(K)}$, continuity of $h_0(\alpha)$ at $\alpha = 1$ gives
     $$
     \bigl\|f_-^{(K)}\bigr\|_{L^2(d^\times x)}^2 = h_0(1) - h_0\bigl(\tau^{|K|}\bigr) \longrightarrow 0 \qquad (K \to 0),
     $$
     including along nonzero admissible rational grades $K = 1/n \in \mathbb{A}_{\mathbb{R}} \setminus \{0\}$ (certified in 256-bit Arb: $\|f_-^{(0)}\|_{L^2}^2 = 0$; $\|f_-^{(\pm 1/1000)}\|_{L^2}^2 = 2.68872306 \times 10^{-5}$; $\|f_-^{(\pm 1/100)}\|_{L^2}^2 = 2.68509890 \times 10^{-3}$; note also that $h_0(1) - \max_{\alpha\ge 2}|h_0(\alpha)| = 0.2584950550 > 0$ holds only on the restricted domain $|K| \ge \frac{\log 2}{\log\tau} \approx 0.37715$, where $\tau^{|K|} \ge 2$).
   - **Consequence**: Excluding $K = 0$ does **not** produce a uniform positive lower bound on $\|f_-^{(K)}\|_{L^2}^2$ over $\mathbb{A}_{\mathbb{R}} \setminus \{0\}$, and dividing $\sup_K |P_E(f_-^{(K)})|$ by $\|f_-^{(K)}\|_{L^2}^2$ is invalid as $K \to 0$. The false uniform norm-floor claims and the resulting division construction of $\mu_0$ are withdrawn; `coercive_norm_shift_semiboundedness_implies_correlation_bound` is preserved strictly as a **conditional one-way theorem** (if a finite $\mu_0 \ge 0$ exists satisfying $P_E(f_\pm^{(K)}) \ge -(\|A_\tau^B f_\pm^{(K)}\|^2 + \mu_0\|f_\pm^{(K)}\|_{L^2}^2)$, then $|C_\tau(K)| \le C_\tau(0) + 2(c_\tau^B + \mu_0)h_0(1)$), distinguished from any unproved converse.

3. **Repair of the False Transfer-Term Bound `0.633039` (`TASK-TC-045R` / `TASK-TC-045R2` Step 3, `transfer_form_plancherel_bound_and_minus_state_vanishing`)**:
   - **Established Transfer-Form Definitions & Reproduced Counterexample to `0.633039`**:
     By Section 10.2, the Volterra-type operator $R_0$ and half-line $x^{-1/2}$ integral $J(f, f)$ (which satisfies $I_{\mathrm{pole},+}(f, f) + J(f, f) = W_{\mathrm{pole}}(f * f^*) = 0$ on $\mathcal{S}_\tau$, whereas $J(\psi_\tau, \psi_\tau) = +0.0259597612733706 \ne 0$ itself does not vanish on the canonical seed) on $\mathcal{S}_\tau \subset L^2(\mathbb{R}_{>0}, d^\times x)$ are
     $$
     (R_0 f)(x) = \int_0^x (y/x)^{1/2}(D_y f)(y)\,\frac{dy}{y}, \qquad D_y = y\frac{d}{dy},
     $$
     $$
     J(f, f) = \int_1^\infty \Phi_{f,f}(x)x^{-1/2}\,\frac{dx}{x} = \frac{1}{\tau}\int_{\mathbb{R}} \frac{|\widehat{f}(it)|^2}{t^2 + 1/4}\,dt = 4\|f\|_{L^2(d^\times x)}^2 - 4\|R_0 f\|_{L^2(d^\times x)}^2,
     $$
     and the transfer form is $B_{\mathrm{transfer}}(f) = 2\|f\|_{L^2(d^\times x)}^2 - J(f, f) = 4\|R_0 f\|_{L^2(d^\times x)}^2 - 2\|f\|_{L^2(d^\times x)}^2$. On the seed state $\psi_\tau$, $J(\psi_\tau, \psi_\tau) = 0.0259597612733706$ and $B_{\mathrm{transfer}}(\psi_\tau) = 2h_0(1) - J(\psi_\tau, \psi_\tau) = +0.9687652063464319$. Therefore:
     - at $K = 0$, $f_+^{(0)} = \sqrt{2}\psi_\tau$ has $B_{\mathrm{transfer}}(f_+^{(0)}) = 2\,B_{\mathrm{transfer}}(\psi_\tau) = +1.9375304126928638 > 0.633039$,
     - as $|K| \to \infty$, $B_{\mathrm{transfer}}(f_\pm^{(K)}) \to B_{\mathrm{transfer}}(\psi_\tau) = +0.9687652063464319 > 0.633039$ (already $0.96875498 > 0.633039$ at $K = 8$).
     The number `0.633039` was traced to the earlier loose forward-prime bound $\frac{92193}{32768} \times 0.225 = 0.6330390930175781$ from `section_8` (`verify_forward_prime_bound`) and is not a bound on $B_{\mathrm{transfer}}(f_\pm^{(K)})$.
   - **Proved Plancherel Bound on $B_{\mathrm{transfer}}$**:
     Since $0 < \frac{1}{t^2 + 1/4} \le 4$ for all $t \in \mathbb{R}$, Plancherel's theorem gives $0 \le J(f, f) \le 4\|f\|_{L^2(d^\times x)}^2$ and hence $B_{\mathrm{transfer}}(f) = 2\|f\|_{L^2(d^\times x)}^2 - J(f, f) \in \bigl[-2\|f\|_{L^2(d^\times x)}^2, +2\|f\|_{L^2(d^\times x)}^2\bigr]$ for every $f \in \mathcal{S}_\tau$ (Lean 4 Theorem 43 `transfer_form_plancherel_bound_and_minus_state_vanishing`). Since $0 \le \|f_\pm^{(K)}\|_{L^2}^2 = h_0(1) \pm h_0(\tau^{|K|}) \le 2h_0(1)$, this proves for all $K \in \mathbb{A}_{\mathbb{R}}$:
     $$
     \boxed{\bigl|B_{\mathrm{transfer}}(f)\bigr| \le 2\|f\|_{L^2(d^\times x)}^2 \quad (\forall f \in \mathcal{S}_\tau), \qquad \bigl|B_{\mathrm{transfer}}\bigl(f_\pm^{(K)}\bigr)\bigr| \le 2\bigl\|f_\pm^{(K)}\bigr\|_{L^2}^2 \le 4h_0(1) = 1.9894499352 < 1.98945.}
     $$
     For the polarized bilinear form $B_{\mathrm{transfer}}(f, g) = \frac{1}{\tau}\int_{\mathbb{R}} b(t)\widehat{f}(it)\overline{\widehat{g}(it)}\,dt$, the Fourier multiplier $b(t) := 2 - \frac{1}{t^2 + 1/4}$ satisfies $b(t) \in [-2, 2]$ ($|b(t)| \le 2$) for all $t \in \mathbb{R}$, so ordinary $L^2$ Cauchy–Schwarz gives $|B_{\mathrm{transfer}}(f, g)| \le 2\|f\|_{L^2(d^\times x)}\|g\|_{L^2(d^\times x)}$ directly (without assuming positivity of the signed form), and in particular for single-grade states $T_K\psi_\tau, T_L\psi_\tau$:
     $$
     \boxed{\bigl|B_{\mathrm{transfer}}(T_K\psi_\tau, T_L\psi_\tau)\bigr| \le 2\|T_K\psi_\tau\|_{L^2}\|T_L\psi_\tau\|_{L^2} = 2h_0(1) = 0.9947249676 < 0.994725 \qquad (\forall K, L \in \mathbb{A}_{\mathbb{R}}).}
     $$
     Using both scale directions $W_{\mathrm{prime}}\bigl(f_\pm^{(K)} * (f_\pm^{(K)})^*\bigr) = 2W(1) \pm \bigl[W_{\log}(X_K) + R_\mu(X_K) + W(X_K^{-1})\bigr]$ ($X_K = \tau^{|K|} \ge 1$, $|W(X_K^{-1})| \le C_{W,0} X_K^{-5/2}$ with $C_{W,0} = \frac{92193}{32768}(-\zeta'(3)/\zeta(3)) = 0.4637297832$, and $W(1) = -0.05730748512 < 0$), any bound $\sup_{X\ge 1}|R_\mu(X)| \le M_\mu$ implies the uniform bound on $P_E(f_\pm^{(K)})$:
     $$
     \bigl|P_E\bigl(f_\pm^{(K)}\bigr)\bigr| \le 2|W(1)| + M_{\log} + M_\mu + C_{W,0} + 4h_0(1) = 5.9168026853 + M_\mu < 5.91681 + M_\mu.
     $$

4. **Repaired Direct Mixed-Grade Implication Chain (`TASK-TC-045R` Step 4, `mixed_grade_pairing_moebius_recovery_and_semiboundedness_equivalence`)**:
   Instead of dividing by $\|f_-^{(K)}\|_{L^2}^2$, the implication from $\sup_{X\ge 1}|R_\mu(X)| \le M_\mu$ to uniform boundedness of $C_\tau(K)$ proceeds **directly** through the exact mixed-grade polarization identity on $T_K\psi_\tau, T_L\psi_\tau \in \mathcal{S}_\tau$ ($\Delta := K - L$, $X_\Delta := \tau^{|K-L|} \ge 1$):
   $$
   \boxed{C_\tau(K - L) = Q_\tau(T_K\psi_\tau, T_L\psi_\tau) = B_{\mathrm{known}}(K, L) - R_\mu\bigl(\tau^{|K - L|}\bigr),}
   $$
   where $B_{\mathrm{known}}(K, L)$ retains $B_{\mathrm{transfer}}(T_K\psi_\tau, T_L\psi_\tau)$ inside $W_{\mathrm{arch}}(h_{K-L}) = \langle A_\tau^B T_K\psi_\tau, A_\tau^B T_L\psi_\tau\rangle_{\mathcal{H}_\tau^B} - c_\tau^B h_0(X_\Delta) + B_{\mathrm{transfer}}(T_K\psi_\tau, T_L\psi_\tau)$ and preserves both scale directions $X_\Delta = \tau^{|K-L|} \ge 1$ and $X_\Delta^{-1} = \tau^{-|K-L|} \le 1$:
   $$
   B_{\mathrm{known}}(K, L) := W_{\mathrm{arch}}(h_{K-L}) - W(X_\Delta^{-1}) - W_{\log}(X_\Delta).
   $$
   Every constant entering $B_{\mathrm{known}}(K, L)$ is traced explicitly via two independent unconditional routes:
   - **Route A (Global Spatial Archimedean Bound)**:
     $|W_{\mathrm{arch}}(h_{K-L})| \le 5.464660$ (Section 6.1), $|W(X_\Delta^{-1})| \le C_{W,0} = 0.4637297832$, and $|W_{\log}(X_\Delta)| \le M_{\log} = 3.3490080247$, giving
     $$
     \bigl|B_{\mathrm{known}}(K, L)\bigr| \le 5.464660 + 0.4637297832 + 3.3490080247 = 9.2773978079 < 9.4468.
     $$
   - **Route B (Attempt B Cauchy–Schwarz + Plancherel Transfer Bound)**:
     $|\langle A_\tau^B T_K\psi_\tau, A_\tau^B T_L\psi_\tau\rangle_{\mathcal{H}_\tau^B}| \le \|A_\tau^B\psi_\tau\|_{\mathcal{H}_\tau^B}^2 = 0.5947678335$, $|c_\tau^B h_0(X_\Delta)| \le c_\tau^B h_0(1) = 1.6771975213$, and $|B_{\mathrm{transfer}}(T_K\psi_\tau, T_L\psi_\tau)| \le 2h_0(1) = 0.9947249676$, giving $|W_{\mathrm{arch}}(h_{K-L})| \le 3.2666903224$ and hence the sharper uniform bound
     $$
     \bigl|B_{\mathrm{known}}(K, L)\bigr| \le 3.2666903224 + 0.4637297832 + 3.3490080247 = 7.0794281303 < 7.07943.
     $$
   Consequently, if $\sup_{X\ge 1}|R_\mu(X)| \le M_\mu < \infty$, then for **all** $K, L \in \mathbb{A}_{\mathbb{R}}$ (with no division by $\|f_-^{(K)}\|_{L^2}^2$ and no restriction away from $K = L$),
   $$
   \boxed{\bigl|C_\tau(K - L)\bigr| = \bigl|Q_\tau(T_K\psi_\tau, T_L\psi_\tau)\bigr| \le 9.27739781 + M_\mu \quad (\text{and } \le 7.07942813 + M_\mu),}
   $$
   which at $L = 0$ gives $\sup_{K\in\mathbb{A}_{\mathbb{R}}}|C_\tau(K)| \le M < \infty$ and excludes all off-critical zeros via the Laplace–Carleman resolvent theorem (`fixed_seed_correlation_bound_implies_critical_line_schema`).

### 12.2 Repair of the Two Remaining `TC-044` Defects & Full-Tree Arb Round-Trip Verification (`Section 14.2`, Expanded in `TASK-TC-045R` Step 6)

1. **Defect 3A — Spectral Aggregation Strip & Synthetic-Quartet Regularization**:
   - Explicitly defined $\mathcal{M}_X[F](z) = \int_0^\infty F(X)X^{-z}\,\frac{dX}{X}$ and $H_0(z) = \int_0^\infty h_0(\alpha)\alpha^z\,\frac{d\alpha}{\alpha}$, proved $\mathcal{M}_X[h_0(n/X)](z) = n^{-z}H_0(z)$ symbolically, justified Fubini–Tonelli interchange on the common absolute-convergence strip $\frac{1}{2} < \operatorname{Re}(z) < \frac{5}{2}$, verified the strip identities at $z = 1.25$ ($s = 1.75$) in 256-bit Arb (`strip_aggregation_identity_encloses_zero == True`, `strip_moebius_identity_encloses_zero == True`), and certified the meromorphic pole residue $\operatorname*{Res}_{z=5/2}[-H_0(z)\zeta'(z+1/2)] = \frac{81}{64}(-\zeta'(3)) = +0.2507535262 \ne 0$ at $z = 5/2$.
   - Certified the Euler–Maclaurin pole-subtracted regularization on the synthetic off-critical mode $\rho_0 = 0.7 + 14.1347251417i$ across $M \in \{100, 1000, 5000\}$: while the unsubtracted partial sum $\sum_{m=1}^M m^{-\rho_0}$ diverges with distance $> 0.13$ from $\zeta(\rho_0)$, the order-1 Euler–Maclaurin subtracted error drops from $5.12 \times 10^{-3}$ ($M = 100$) to $1.01 \times 10^{-4}$ ($M = 1000$) to $1.62 \times 10^{-5}$ ($M = 5000$), and the order-2 error drops to $1.52 \times 10^{-8}$ at $M = 5000$.
2. **Defect 3B — Outward-Rounded Serialization & Full-Tree Round-Trip Interval Containment**:
   - Implemented [`serialize_arb_certified`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L7260-L7294) and [`verify_serialized_arb_roundtrip`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L7297-L7321) using exact binary mantissa-exponent conversion `ep_arb.man_exp()` in Python `Decimal` with `ROUND_FLOOR` (minus 1 decimal ULP) for `lower_dec`, `ROUND_CEILING` (plus 1 decimal ULP) for `upper_dec`, and `rad_float_outward = math.nextafter(float(abs(ball - arb(float(ball.mid()))).upper()), math.inf)` (note: this uses exact binary `man_exp()` with `Decimal` outward rounding, not a `flint.arf` wrapper).
   - Implemented [`verify_all_serialized_arb_in_tree`](file:///c:/Development/Projects/reimann_scope/tc/canonical_theta_correlation_bound.py#L7324-L7379) in `TASK-TC-045R` / `TASK-TC-045R2` to recursively enumerate and verify **every** exported certified Arb ball in `section_13` (`26` balls) and `section_14` (`122` balls; `148` total) against the live original 256-bit `flint.arb` ball (`live_original_count_matches_enumerated_total == True`, `all_enclose_original_256bit_arb_ball == True`, verified across all three reconstructions `arb.union(arb(lower_dec), arb(upper_dec))`, `arb(arb_ball_str)`, and `arb(mid_float, rad_float_outward)`).

### 12.3 Continuity and the Role of Algebraic Grades $\mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}}\cap\mathbb{R}$ (`Section 14.3`)

1. **Small-Scale $O(u^{5/2})$ Bound for $W_{\log}(u)$ (`small_scale_w_log_tail_and_mertens_stieltjes_ibp_identity`)**:
   By the exact rational Bernstein envelope $|h_0(\alpha)| \le \frac{92193}{32768}(\alpha + \alpha^{-1})^{-5/2} \le \frac{92193}{32768}\alpha^{-5/2}$ applied at $\alpha = k/u$, every term of $W_{\log}(u)$ satisfies $\bigl|\frac{\log k}{\sqrt{k}}h_0(k/u)\bigr| \le \frac{92193}{32768}\,u^{5/2}(\log k)k^{-3}$, proving for **all $u > 0$**:
   $$
   \boxed{\bigl|W_{\log}(u)\bigr| \le C_{\log,0}\,u^{5/2}, \qquad C_{\log,0} := \frac{92193}{32768}\sum_{k=2}^\infty \frac{\log k}{k^3} = \frac{92193}{32768}\bigl(-\zeta'(3)\bigr) = 0.5574295871 \pm 2.58 \times 10^{-41}.}
   $$
   Moreover, note that $h_0(\alpha)$ **changes sign** on $(0, \infty)$ (positive near $\alpha = 1$ with $h_0(1) = +0.4973624838 > 0$, and negative on the asymptotic tail $\alpha \ge 9$ with $h_0(9) = -0.000341130295 < 0$ and power-law $5/2$ decay $h_0(\alpha) \sim -\frac{81}{64}\alpha^{-5/2}$ as $\alpha \to \infty$, so $W(1) = -0.05730748512 < 0$ is negative because $n \ge 2$ samples the tail of $h_0$). For $0 < u \le 2/9$, every summand index $k \ge 2$ satisfies $k/u \ge 9$, where $h_0(k/u) \in \bigl[-\frac{81}{64}(u/k)^{5/2}, 0\bigr)$, so $\lim_{u\downarrow 0} u^{-5/2}|W_{\log}(u)| = \frac{81}{64}(-\zeta'(3)) = 0.2507535262$ (certified across $u \in \{1, 1/2, 1/4, 1/\tau, 1/10, 1/\tau^2, 1/100\}$).
2. **Compact-Interval Uniform Convergence and Continuity of $R_\mu(X)$ and $W(X)$**:
   On any compact interval $X \in [a, b] \subset (0, \infty)$ and for every $m \ge 2$,
   $$
   \left|\frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right)\right| \le m^{-1/2} C_{\log,0}\!\left(\frac{X}{m}\right)^{5/2} \le C_{\log,0}\,b^{5/2}\,m^{-3}, \qquad \sum_{m=M}^\infty \left|\frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right)\right| \le \frac{C_{\log,0}\,b^{5/2}}{2(M - 1)^2}.
   $$
   By the Weierstrass $M$-test, $R_\mu(X) = \sum_{m=2}^\infty \frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ converges uniformly on every compact interval $[a, b] \subset (0, \infty)$. Since each summand is continuous on $(0, \infty)$, **$W_{\log}(X)$, $R_\mu(X)$, and $W(X) = W_{\log}(X) + R_\mu(X)$ are continuous on $(0, \infty)$**.
3. **Density of $\mathbb{A}_{\mathbb{R}}$ and Supremum Equality**:
   Because $\mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}}\cap\mathbb{R}$ is dense in $\mathbb{R}$ and $K \mapsto \tau^{|K|}$ maps $\mathbb{A}_{\mathbb{R}}$ onto a dense subset of $[1, \infty)$, continuity of $R_\mu(X)$ and $W(X)$ on $[1, \infty)$ implies
   $$
   \boxed{\sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|R_\mu(\tau^{|K|})\bigr| = \sup_{X \ge 1} \bigl|R_\mu(X)\bigr|, \qquad \sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|W(\tau^{|K|})\bigr| = \sup_{X \ge 1} \bigl|W(X)\bigr|.}
   $$
   Narrowly stated: **restricting the continuous scalar bound to algebraic grade labels $K \in \mathbb{A}_{\mathbb{R}}$ does not weaken its uniform boundedness requirement across scales $X \ge 1$.**

### 12.4 Main Investigation — Mixed-Grade Pairing Polarization & Mertens Stieltjes Representation of $R_\mu(X)$ (`Section 14.4`)

1. **Exact Mixed-Grade Pairing Polarization (`mixed_grade_pairing_moebius_recovery_and_semiboundedness_equivalence`)**:
   For any pair of concurrent algebraic grades $K, L \in \mathbb{A}_{\mathbb{R}}$ with $\Delta := K - L$ and $X_\Delta := \tau^{|K - L|} \ge 1$, polarizing the Attempt B decomposition on $\mathcal{S}_\tau$ with prime, pole, archimedean, transfer, and normalization terms intact yields:
   $$
   \boxed{Q_\tau(T_K\psi_\tau, T_L\psi_\tau) = \langle A_\tau^B T_K\psi_\tau, A_\tau^B T_L\psi_\tau\rangle_{\mathcal{H}_\tau^B} - c_\tau^B h_0(X_\Delta) + B_{\mathrm{transfer}}(T_K\psi_\tau, T_L\psi_\tau) - W(X_\Delta^{-1}) - W_{\log}(X_\Delta) - R_\mu(X_\Delta) = B_{\mathrm{known}}(K, L) - R_\mu(X_\Delta),}
   $$
   where $B_{\mathrm{transfer}}(T_K\psi_\tau, T_L\psi_\tau)$ is retained inside $W_{\mathrm{arch}}(h_{K-L}) = \langle A_\tau^B T_K\psi_\tau, A_\tau^B T_L\psi_\tau\rangle_{\mathcal{H}_\tau^B} - c_\tau^B h_0(X_\Delta) + B_{\mathrm{transfer}}(T_K\psi_\tau, T_L\psi_\tau)$ and every term of $B_{\mathrm{known}}(K, L)$ is unconditionally bounded across all $K, L \in \mathbb{A}_{\mathbb{R}}$:
   $$
   \bigl|B_{\mathrm{known}}(K, L)\bigr| \le \bigl|W_{\mathrm{arch}}(h_{K-L})\bigr| + \bigl|W(X_\Delta^{-1})\bigr| + \bigl|W_{\log}(X_\Delta)\bigr| \le 5.464660 + 0.4637297832 + 3.3490080247 = 9.2773978079 < 9.4468
   $$
   (and $\le 3.2666903224 + 0.4637297832 + 3.3490080247 = 7.0794281303 < 7.07943$ via the Attempt B Cauchy–Schwarz + Plancherel transfer bound).
   Thus **for every pair of grades $(K, L)$, the mixed-grade pairing $Q_\tau(T_K\psi_\tau, T_L\psi_\tau)$ and the negative Möbius remainder $-R_\mu(\tau^{|K-L|})$ differ by at most $9.2774 < 9.4468$ (and $7.0795$ via Attempt B)**.

| Grade Difference $\Delta = K - L$ | Scale $X_\Delta = \tau^{|\Delta|}$ | Authentic $W(X_\Delta)$ | Divisor-Aggregated $W_{\log}(X_\Delta)$ | Direct Möbius Remainder $R_\mu(X_\Delta)$ | Consistency $\bigl|W - (W_{\log} + R_\mu)\bigr|$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $\Delta = 0.0$ | $1.000000$ | $-0.0573074796$ | $-0.0440613787$ | $-0.0132461009$ | $0 \in \text{diff}$ ($< 6.97 \times 10^{-8}$) |
| $\Delta = 0.5$ | $2.506628$ | $+0.0558632744$ | $+0.0725782839$ | $-0.0167150096$ | $0 \in \text{diff}$ ($< 6.91 \times 10^{-7}$) |
| $\Delta = 1.0$ | $6.283185$ | $-0.0120796090$ | $-0.0007290073$ | $-0.0113506019$ | $0 \in \text{diff}$ ($< 6.89 \times 10^{-6}$) |
| $\Delta = 1.5$ | $15.749610$ | $+0.0029755348$ | $-0.0000180909$ | $+0.0029936243$ | $0 \in \text{diff}$ ($< 6.88 \times 10^{-5}$) |
| $\Delta = 2.0$ | $39.478418$ | $-0.0019168088$ | $-0.0000178962$ | $-0.0018989212$ | $0 \in \text{diff}$ ($< 6.88 \times 10^{-4}$) |

2. **Simultaneous-Grade Covariance & Continuous Hermitian Toeplitz Counterexample Control**:
   The concurrent grade action satisfies simultaneous-grade shift covariance $Q_\tau(T_{K+S}\psi_\tau, T_{L+S}\psi_\tau) = Q_\tau(T_K\psi_\tau, T_L\psi_\tau)$ and Hermitian symmetry $Q_\tau(T_L\psi_\tau, T_K\psi_\tau) = Q_\tau(T_K\psi_\tau, T_L\psi_\tau)$ for all $K, L, S \in \mathbb{A}_{\mathbb{R}}$. However, the explicit continuous Hermitian Toeplitz counterexample kernel
   $$
   K_{\mathrm{model}}(K, L) := C_\tau(0)\cosh\bigl(\delta_0(K - L)\log\tau\bigr)\cos\bigl(\gamma_0(K - L)\log\tau\bigr) \qquad (\delta_0 = 0.2,\; \gamma_0 = 14.1347251417)
   $$
   satisfies simultaneous-grade covariance $K_{\mathrm{model}}(K+S, L+S) = K_{\mathrm{model}}(K, L)$, Hermitian symmetry, diagonal positivity $K_{\mathrm{model}}(K, K) = C_\tau(0) > 0$, and real-analytic continuity on $\mathbb{R} \times \mathbb{R}$, yet its envelope grows exponentially as $C_\tau(0)\cosh(\delta_0|K-L|\log\tau) \to +\infty$ (reaching $9.4900\,C_\tau(0)$ at $|K - L| = 8$). Thus **simultaneous-grade covariance and Hermitian symmetry alone do not bound $R_\mu(\tau^{|K-L|})$**.

3. **Exact Mertens Stieltjes Summation-by-Parts Representation of $R_\mu(X)$ (`small_scale_w_log_tail_and_mertens_stieltjes_ibp_identity`)**:
   Define the summatory Möbius (Mertens) remainder $M_{\ge 2}(y) := \sum_{2 \le m \le y}\mu(m) = M(y) - 1$ ($y \ge 2$, and $0$ for $y < 2$) and the smooth rescaled profile $\phi_{\log}(u) := u^{1/2}W_{\log}(u) = \sum_{k=2}^\infty \frac{\log k}{\sqrt{k}}\,u^{1/2}h_0(k/u)$. Since $\alpha = k/u$ has $\frac{d\alpha}{du} = -\frac{\alpha}{u}$, differentiating with respect to $u$ gives the exact derivative identity (verified symbolically in SymPy and in 256-bit Arb):
   $$
   \phi_{\log}'(u) = +u^{-1/2}\sum_{k=2}^\infty \frac{\log k}{\sqrt{k}}\,\widetilde{h}_0\!\left(\frac{k}{u}\right), \qquad \widetilde{h}_0(\alpha) = \frac{1}{2}h_0(\alpha) - \alpha h_0'(\alpha).
   $$
   For any finite cutoff $M \ge 2$ and $X > 0$, summation by parts of $R_{\mu, M}(X) = X^{-1/2}\sum_{m=2}^M \mu(m)\phi_{\log}(X/m)$ gives
   $$
   R_{\mu, M}(X) = M_{\ge 2}(M)M^{-1/2}W_{\log}(X/M) + X^{-1/2}\int_{X/M}^{X/2} M_{\ge 2}\!\left(\frac{X}{u}\right)\phi_{\log}'(u)\,du,
   $$
   certified in 256-bit Arb at $M = 16, K = 24$ across $X \in \{1, 2, 4, \tau\}$ to $< 10^{-50}$ (discrete Abel form) and $< 10^{-24}$ (continuous Stieltjes integral form). Since $|M_{\ge 2}(M)|M^{-1/2}|W_{\log}(X/M)| \le C_{\log,0}X^{5/2}M^{-2} \to 0$ as $M \to \infty$, taking $M \to \infty$ yields the **exact infinite Mertens Stieltjes representation**:
   $$
   \boxed{R_\mu(X) = X^{-1/2}\int_0^{X/2} M_{\ge 2}\!\left(\frac{X}{u}\right)\phi_{\log}'(u)\,du = X^{1/2}\int_2^\infty M_{\ge 2}(y)\,\phi_{\log}'\!\left(\frac{X}{y}\right)\frac{dy}{y^2}.}
   $$
   - **Why Unconditional Pointwise Mertens Bounds Do Not Suffice**:
     Inserting the strongest known unconditional zero-free-region Mertens bounds $|M(y)| \le C_\mu y\exp(-c_\mu\sqrt{\log y})$ (Schoenfeld 1969; El Marraki 1995; Titchmarsh 1986, §14.26) into the absolute-value integral yields an unsigned upper bound
     $$
     |R_\mu(X)| \le X^{1/2}\int_0^{X/2} \left|\frac{M_{\ge 2}(X/u)}{X/u}\right| u^{-1}\bigl|\phi_{\log}'(u)\bigr|\,du = O\!\left(X^{1/2}\exp\!\left(-c_\mu'\sqrt{\log X}\right)\right),
     $$
     whose right-hand side grows as $X \to \infty$ because the prefactor $X^{-1/2}$ cancels only half a power of $y = X/u \asymp X$. This growing unsigned upper bound shows that **an unsigned pointwise Mertens bound is insufficient** to establish an $O(1)$ bound on $R_\mu(X)$ (it does **not** prove that $R_\mu(X)$ itself diverges). Achieving an $O(1)$ bound on $R_\mu(X)$ requires exploiting **signed oscillation of $M_{\ge 2}(X/u)$ against the smooth derivative kernel $\phi_{\log}'(u)$** (`SUBGATE-TC-043A`: **Smooth-Kernel Mertens / Möbius Cancellation Lemma for $R_\mu(X)$**).

---

## 13. Prime-by-Prime Möbius Recovery and Arithmetic Cross-Grade Compatibility (`TASK-TC-046`, `Section 15`)

### 13.1 Recovered Mathematical Obligation & Ambient Space vs. Admissible Grades Bookkeeping (`Section 15.1`)

1. **Recovered Obligation from `TC-044` and `TC-045` / `TC-045R` / `TC-045R2`**:
   With $\tau = 2\pi$, $K \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}}\cap\mathbb{R}$ (including positive, negative, and zero grades), $\mathcal{Z}_\tau(s, K) = \zeta(\tau^{-K}s)$, and complex zero scaling $\rho \mapsto \tau^K\rho$, the reflected prime-power sum, divisor-aggregated profile, and Möbius remainder at scale $X = \tau^{|K-L|} \ge 1$ are
   $$
   W(X) = \sum_{n\ge 2}\frac{\Lambda(n)}{\sqrt{n}}\,h_0\!\left(\frac{n}{X}\right), \qquad W_{\log}(X) = \sum_{n\ge 2}\frac{\log n}{\sqrt{n}}\,h_0\!\left(\frac{n}{X}\right), \qquad R_\mu(X) = \sum_{m\ge 2}\frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right),
   $$
   related by the exact identity $W(X) = W_{\log}(X) + R_\mu(X)$, where:
   - $\bigl|W_{\log}(X)\bigr| \le 3.3490080247 < 3.34901$ unconditionally for all $X \ge 1$ (`TC-044`),
   - $\bigl|W_{\log}(u)\bigr| \le C_{\log,0}\,u^{5/2}$ unconditionally for all $u > 0$ with $C_{\log,0} = \frac{92193}{32768}(-\zeta'(3)) = 0.5574295871 \pm 2.58 \times 10^{-41}$ (`TC-045`),
   - $C_\tau(K - L) = Q_\tau(T_K\psi_\tau, T_L\psi_\tau) = B_{\mathrm{known}}(K, L) - R_\mu(\tau^{|K-L|})$ with $\bigl|B_{\mathrm{known}}(K, L)\bigr| \le 7.0794281303 < 7.07943$ (`TC-045R` / `TC-045R2`),
   - leaving the single missing uniform arithmetic estimate $\sup_{X\ge 1}|R_\mu(X)| < \infty$ (`SUBGATE-TC-043A`).

2. **Ambient Function Space vs. Admissible Algebraic Grade Labels**:
   Because $\tau = 2\pi$ is transcendental (by Lindemann–Weierstrass), $\log_\tau p = \frac{\log p}{\log(2\pi)}$ is not rational and cannot be assumed to lie in $\mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}}\cap\mathbb{R}$ (for instance, $\log_\tau 2 = 0.3771458599\dots$, $\log_\tau 3 = 0.5978137345\dots$, $\log_\tau 5 = 0.8754298932\dots$). To avoid any unproven arithmetic assumption about $\log_\tau p$:
   - Define the ambient space of continuous profiles on $(0, \infty)$ with $u^{5/2}$ small-scale decay and polynomial large-scale growth:
     $$
     \mathcal{F}_{5/2} := \Bigl\{F \in C((0, \infty)) : |F(u)| = O(u^{5/2}) \text{ as } u \to 0^+, \; |F(X)| = O(X^\theta) \text{ as } X \to \infty\Bigr\},
     $$
     and the commuting multiplicative scale-dilation operators $(D_p F)(X) := F(X/p)$ on $\mathcal{F}_{5/2}$ (along with the unitary prime dilations $(U_p f)(x) := f(x/p)$ on $L^2(\mathbb{R}_{>0}, d^\times x)$).
   - Every finite-prime Euler operator $\prod_{p\le y}(I - p^{-1/2}D_p)$ maps $\mathcal{F}_{5/2}$ into $\mathcal{F}_{5/2}$ and defines a continuous function $W_y(X)$ on all of $(0, \infty)$.
   - The concurrent grade family then restricts $W_y(X)$ to the admissible grade scales $X = \tau^{|K-L|}$ ($K, L \in \mathbb{A}_{\mathbb{R}}$). Since $\mathbb{A}_{\mathbb{R}}$ is dense in $\mathbb{R}$ and $W_y$ is continuous on $[1, \infty)$,
     $$
     \sup_{K \in \mathbb{A}_{\mathbb{R}}} \bigl|W_y(\tau^{|K|})\bigr| = \sup_{X \ge 1} \bigl|W_y(X)\bigr|.
     $$

### 13.2 Exact Finite-Prime Euler Inversion, Prime-Power Classification, and Agreement Threshold $2 q_{>y}$ (`Section 15.2`)

1. **Operator Product, Divisor Sum, and One-Prime Recursion (`finite_prime_euler_recursion_and_coefficient_cases`)**:
   For $y \ge 2$, let $p_1 = 2 < p_2 < \dots < p_r \le y$ be the primes up to $y$, $P_y := \prod_{p\le y} p$ the primorial, and $\mu_y(m) := \mu(m)\mathbf{1}_{m \mid P_y}$. Since $D_p D_q = D_{p q} = D_q D_p$ commute on $\mathcal{F}_{5/2}$ and expanding $\prod_{p\le y}(I - p^{-1/2}D_p)$ produces each squarefree divisor $m = \prod_{p\in S} p \mid P_y$ with coefficient $(-1)^{|S|} m^{-1/2} = \mu(m) m^{-1/2}$,
   $$
   \boxed{W_y(X) := \sum_{m \mid P_y} \frac{\mu(m)}{\sqrt{m}}\,W_{\log}\!\left(\frac{X}{m}\right) = \left[\prod_{p\le y}\bigl(I - p^{-1/2}D_p\bigr)\right] W_{\log}(X),}
   $$
   satisfying the exact one-prime recursion and telescoping difference identity ($W_{p_0} := W_{\log}$):
   $$
   W_{p_k}(X) = W_{p_{k-1}}(X) - p_k^{-1/2} W_{p_{k-1}}\!\left(\frac{X}{p_k}\right), \qquad R_{\mu, y}(X) := W_y(X) - W_{\log}(X) = -\sum_{k=1}^r p_k^{-1/2} W_{p_{k-1}}\!\left(\frac{X}{p_k}\right).
   $$

2. **Closed-Form Coefficient Formula $\lambda_y = \mu_y * \log$ and Explicit Prime-Power Behavior**:
   Expanding $W_{\log}(X/m) = \sum_{k\ge 2}(\log k)k^{-1/2}h_0(k m / X)$ and grouping by $n = m k \ge 2$ ($m \mid \gcd(n, P_y)$) yields
   $$
   W_y(X) = \sum_{n=2}^\infty \frac{\lambda_y(n)}{\sqrt{n}}\,h_0\!\left(\frac{n}{X}\right), \qquad \lambda_y(n) := (\mu_y * \log)(n) = \sum_{\substack{d \mid n \\ d \mid P_y}} \mu(d)\log\!\left(\frac{n}{d}\right).
   $$
   Factoring $n = \prod_{i=1}^s p_i^{a_i}$ ($a_i \ge 1$) and letting $\omega_{\le y}(n) := \#\{p \mid n : p \le y\}$ denote the number of distinct prime divisors of $n$ at most $y$, using $\sum_{d \mid \gcd(n, P_y)}\mu(d) = \mathbf{1}_{\omega_{\le y}(n) = 0}$ and $\sum_{d \mid \gcd(n, P_y),\, p \mid d}\mu(d) = -\mathbf{1}_{\{p\text{ is the unique prime }\le y\text{ dividing }n\}}$ gives the exact three-case closed form:
   $$
   \boxed{\lambda_y(n) = \begin{cases}
   \log n & \text{if } \omega_{\le y}(n) = 0 \quad (\text{no prime divisor } \le y), \\
   \log p & \text{if } \omega_{\le y}(n) = 1 \quad (p \le y \text{ is the unique prime divisor } \le y \text{ of } n), \\
   0 & \text{if } \omega_{\le y}(n) \ge 2 \quad (\text{at least two distinct prime divisors } \le y).
   \end{cases}}
   $$
   In particular, prime powers and mixed prime-power composites behave as follows:
   - **Pure prime powers $n = p^a$ with $p \le y$ ($a \ge 1$)**: $\omega_{\le y}(p^a) = 1$, so $\lambda_y(p^a) = \log p = \Lambda(p^a)$ identically for all exponents $a \ge 1$ (since $\mu_y(1)\log(p^a) + \mu_y(p)\log(p^{a-1}) = a\log p - (a-1)\log p = \log p$).
   - **Pure prime powers $n = r^b$ with $r > y$ ($b \ge 1$)**: $\omega_{\le y}(r^b) = 0$, so $\lambda_y(r^b) = b\log r$. For $b = 1$ (prime $r > y$), $\lambda_y(r) = \log r = \Lambda(r)$; for $b \ge 2$, $\lambda_y(r^b) = b\log r > \log r = \Lambda(r^b)$ with surplus $(b - 1)\log r > 0$.
   - **Mixed prime-power composites $n = p^a n_{>y}$ with $p \le y$, $a \ge 1$, and $n_{>y} > 1$ coprime to $P_y$**: $\omega_{\le y}(n) = 1$, so $\lambda_y(n) = \log p > 0$ whereas $\Lambda(n) = 0$.
   - **Composites with $\omega_{\le y}(n) \ge 2$**: $\lambda_y(n) = 0 = \Lambda(n)$ identically.

3. **Exact Agreement Window with $\Lambda(n)$ and First Discrepancy at $2 q_{>y}$**:
   Let $q_{>y} := \min\{p \text{ prime} : p > y\} > y$. Then:
   - The sieve surplus $\Delta_y(n) := \lambda_y(n) - \Lambda(n)$ satisfies $\Delta_y(n) \ge 0$ for **all** $n \ge 2$, and $0 \le \lambda_y(n) \le \log n$.
   - Every integer $n \ge 2$ with $\Delta_y(n) > 0$ is either a mixed composite $p^a n_{>y}$ ($p \le y$, $n_{>y} \ge q_{>y}$, so $n \ge 2 q_{>y}$) or a $y$-rough composite ($n \ge q_{>y}^2 > 2 q_{>y}$).
   - Therefore,
     $$
     \boxed{\lambda_y(n) = \Lambda(n) \quad \forall\, 2 \le n < 2 q_{>y} \quad (\text{in particular for all } 2 \le n \le 2y + 1),}
     $$
     and the **first discrepancy** occurs at $n_{\min}(y) = 2 q_{>y}$, where $\lambda_y(2 q_{>y}) = \log 2 > 0 = \Lambda(2 q_{>y})$ (verified in 256-bit Arb across $y \in \{2, 3, 5, 7, 11, 13, 17, 19, 23, 29\}$).

4. **Exact Summatory Factorial Identity for $L_y(x) := \sum_{2\le n\le x}\lambda_y(n)$**:
   Summing $\lambda_y = \mu_y * \log$ against $L(z) = \sum_{2\le k\le z}\log k = \log(\lfloor z\rfloor!)$ gives the exact summatory factorial identity:
   $$
   \boxed{L_y(x) := \sum_{2\le n\le x}\lambda_y(n) = \sum_{\substack{d \mid P_y \\ d \le x}} \mu(d)\,L\!\left(\frac{x}{d}\right) = \sum_{\substack{d \mid P_y \\ d \le x}} \mu(d)\log\!\bigl(\lfloor x/d\rfloor!\bigr),}
   $$
   with $L_{p_k}(x) = L_{p_{k-1}}(x) - L_{p_{k-1}}(x/p_k)$ and $L_y(x) = \psi(x)$ for all $x < 2 q_{>y}$.

### 13.3 Quantitative Compatibility Analysis & Exact Obstructions (`Section 15.3`)

1. **Stieltjes Decomposition of $W_y(X)$ with Cutoff Boundaries Retained**:
   Writing $L(z) = M_{\log}(z) + E_{\log}(z)$ with $M_{\log}(z) = (z\log z - z + 1)\mathbf{1}_{z\ge 1}$ ($dM_{\log}(z) = \log z\,dz$ on $[1, \infty)$) and $E_{\log}(z) = \log(\lfloor z\rfloor!) - (z\log z - z + 1)$, define
   $$
   L_y(x) = M_y(x) + E_y(x), \qquad M_y(x) := \sum_{\substack{d \mid P_y \\ d \le x}} \mu(d)\,M_{\log}\!\left(\frac{x}{d}\right), \qquad E_y(x) := \sum_{\substack{d \mid P_y \\ d \le x}} \mu(d)\,E_{\log}\!\left(\frac{x}{d}\right).
   $$
   Because $H_0(1/2) = H_0'(1/2) = 0$ forces the full-line smooth logarithmic integral $\int_0^\infty u^{-1/2}(\log u)h_0(u/Y)\,du = 0$ to vanish identically at every scale $Y = X/d > 0$, Stieltjes integration by parts yields
   $$
   \boxed{W_y(X) = B_y(X) + I_y(X), \qquad B_y(X) = \sum_{d \mid P_y}\frac{\mu(d)}{\sqrt{d}}\,B_{\log,\mathrm{boundary}}\!\left(\frac{X}{d}\right), \qquad I_y(X) = \int_1^\infty E_y(x)\,x^{-3/2}\,\widetilde{h}_0\!\left(\frac{x}{X}\right)dx,}
   $$
   where $B_{\log,\mathrm{boundary}}(u) = -\int_0^1 t^{-1/2}(\log t)h_0(t/u)\,dt$ satisfies the certified two-sided envelope $\bigl|B_{\log,\mathrm{boundary}}(u)\bigr| \le \min\!\bigl(\frac{30731}{98304}u^{-5/2},\; \frac{92193}{131072}u^{5/2}\bigr)$ for all $u > 0$. Retaining the lower step cutoffs $x \ge d$ in $M_y(x)$ is essential because for divisors $d \asymp X$, $B_{\log,\mathrm{boundary}}(X/d) = O(1)$ and unsigned summation over $d \mid P_y$ grows as $O(X^{1/2})$ whenever $y \ge X$.

2. **Mechanism A — Critical-Line Mellin/Fourier Representation, Euler-Sieved Seed Gram Norm, and the Low-Frequency Coherent Arch Spike**:
   On $|\operatorname{Re}(z)| < 5/2$, $\mathcal{M}_X[W_y](z) = -E_y(z)H_0(z)\zeta'(z + 1/2)$, where
   $$
   E_y(z) := \prod_{p\le y}\bigl(1 - p^{-(z+1/2)}\bigr) = \sum_{m \mid P_y} \mu(m)\,m^{-(z+1/2)}
   $$
   is an **entire** Dirichlet polynomial and the triple zero $H_0(1/2) = H_0'(1/2) = H_0''(1/2) = 0$ cancels the double pole of $-\zeta'(z + 1/2)$ at $z = 1/2$. Thus $\mathcal{M}_X[W_y](z)$ is holomorphic across the entire open strip $|\operatorname{Re}(z)| < 5/2$ (with no poles at nontrivial zeros of $\zeta$). Shifting the Mellin inversion contour to $\operatorname{Re}(z) = 0$ ($z = it$) crosses zero poles and gives the exact critical-line Fourier representation and Euler-sieved seed Gram bound:
   $$
   \boxed{W_y(X) = -\frac{1}{\tau}\int_{-\infty}^\infty E_y(it)\,H_0(it)\,\zeta'\!\left(\frac{1}{2} + it\right)X^{it}\,dt, \qquad \sup_{X > 0}\bigl|W_y(X)\bigr| \le \|\Psi_y\|_{L^2(d^\times x)}\,N_{\zeta',\tau},}
   $$
   where $\Psi_y := \bigl[\prod_{p\le y}(I - p^{-1/2}U_p)\bigr]\psi_\tau$ has exact Gram norm squared $\|\Psi_y\|_{L^2(d^\times x)}^2 = \sum_{m_1, m_2 \mid P_y}\frac{\mu(m_1)\mu(m_2)}{\sqrt{m_1 m_2}}\,h_0(m_1/m_2) = \frac{1}{\tau}\int_{-\infty}^\infty |E_y(it)|^2 H_0(it)\,dt$ and $N_{\zeta',\tau}^2 := \frac{1}{\tau}\int_{-\infty}^\infty |\zeta'(1/2+it)|^2 |F_\tau(1/2+it)|^2\,dt < \infty$.
   - **Controlled-Width Low-Frequency Interval Lower Bound and Divergence of the Unsplit Gram-Norm Estimate as $y \to \infty$**:
     Write $E_y(it) = \prod_{p\le y}\bigl(1 - p^{-1/2 - it}\bigr)$ and retain the controlled-width frequency interval ($\tau = 2\pi$):
     $$
     I_y := [t_{y,-}, \, t_{y,+}] = \left[\frac{7\tau}{16\log y}, \, \frac{\tau}{2\log y}\right] = \left[\frac{7\pi}{8\log y}, \, \frac{\pi}{\log y}\right], \qquad |I_y| = \frac{\tau}{16\log y} = \frac{\pi}{8\log y} > 0, \qquad a := \frac{7\tau}{16} = \frac{7\pi}{8}, \quad t_{y,-} = \frac{a}{\log y}.
     $$
     1. *Euler-Factor Monotonicity on $I_y$*:
        For every prime $p \le y$ and every $t \in \bigl[0, \frac{\tau}{2\log y}\bigr]$, the phase satisfies $0 \le t\log p \le \frac{\tau}{2} = \pi$, where $\sin(t\log p) \ge 0$. Hence
        $$
        \frac{d}{dt}\bigl|1 - p^{-1/2 - it}\bigr|^2 = \frac{d}{dt}\bigl(1 + p^{-1} - 2p^{-1/2}\cos(t\log p)\bigr) = 2p^{-1/2}\log p\,\sin(t\log p) \ge 0,
        $$
        so $|E_y(it)|^2$ is monotonically non-decreasing in $t$ on $I_y$ and attains its exact interval minimum at the left endpoint:
        $$
        \inf_{t \in I_y}\bigl|E_y(it)\bigr|^2 = \bigl|E_y(i t_{y,-})\bigr|^2.
        $$
     2. *Complete Logarithmic-Product Derivation of the Left-Endpoint Asymptotic and Refutation of the False Subproduct Inequality*:
        - **Removal of the False Subproduct Claim and Certified $y = 210$ Counterexample**:
          An earlier version claimed $|E_y(i t_{y,-})|^2 \ge \prod_{y^{16/21}\le p\le y}(1 + p^{-1/2} + p^{-1})$ and assigned the right-endpoint exponential coefficient $4$ to the left endpoint. Both statements are false: the subproduct discards lower-prime factors $p < y^{16/21}$ that are strictly less than $1$ whenever $\cos(t_{y,-}\log p) > \frac{1}{2}p^{-1/2}$ (and the displayed subproduct itself has leading exponential coefficient $2$, not $4$). At $y = 210$, certified 256-bit Arb evaluation (`certify_subproduct_counterexample_at_y210_arb`) gives disjoint 40-digit exported enclosures refuting the inequality:
          $$
          \bigl|E_{210}(i t_{210,-})\bigr|^2 \in \bigl[3.360505748107591748433727329931049784134 \pm 2.76\times 10^{-40}\bigr] \approx 3.3605057481 \;<\; 18.2536118944 \approx \bigl[18.25361189443124292062507273824985611480 \pm 3.55\times 10^{-39}\bigr] \ni \prod_{210^{16/21}\le p\le 210}\!\left(1 + \frac{1}{\sqrt{p}} + \frac{1}{p}\right),
          $$
          where the omitted lower-prime product over $p < 210^{16/21} \approx 58.790877$ equals $0.0558540314 < 1$ (while the upper-prime actual product $\prod_{59\le p\le 210} g_p(t_{210,-})$ over $59 \le p \le 210$ equals $60.1658585001$).
        - **Full Logarithmic Expansion Retaining All Prime Factors $p \le y$**:
          Since $|p^{-1/2 - it}| = p^{-1/2} \le 2^{-1/2} < 1$ for every prime $p \ge 2$, expanding $\log(1 - p^{-1/2 - it}) = -\sum_{k=1}^\infty \frac{1}{k}p^{-k/2 - ikt\log p}$ across all $p \le y$ gives
          $$
          \log\bigl|E_y(it)\bigr|^2 = 2\operatorname{Re}\sum_{p\le y}\log\bigl(1 - p^{-1/2 - it}\bigr) = -2\sum_{p\le y} p^{-1/2}\cos(t\log p) + R_{\ge 2}(y, t),
          $$
          where the $k \ge 2$ higher-power tail is bounded uniformly in $t \in \mathbb{R}$ by
          $$
          \bigl|R_{\ge 2}(y, t)\bigr| = \left|2\sum_{p\le y}\sum_{k=2}^\infty \frac{p^{-k/2}\cos(k t\log p)}{k}\right| \le \sum_{p\le y}\frac{p^{-1}}{1 - p^{-1/2}} \le (2 + \sqrt{2})\sum_{p\le y} p^{-1} = O\!\left(\sum_{p\le y} p^{-1}\right) = O(\log\log y) = o\!\left(\frac{\sqrt{y}}{\log y}\right)
          $$
          by Mertens' bound $\sum_{p\le y} p^{-1} = \log\log y + O(1)$.
        - **Prime Number Theorem with Partial Summation**:
          For any fixed $a \in \mathbb{R}$, set $\phi_y(x) := x^{-1/2}\cos\!\bigl(a\,\frac{\log x}{\log y}\bigr)$ on $[2, y]$, so $\phi_y'(x) = -\frac{1}{2}x^{-3/2}\cos\!\bigl(a\,\frac{\log x}{\log y}\bigr) - \frac{a}{\log y}x^{-3/2}\sin\!\bigl(a\,\frac{\log x}{\log y}\bigr)$. By the classical **Prime Number Theorem** ($\pi(x) = \frac{x}{\log x}(1 + o(1))$ as $x \to \infty$; Hadamard 1896, de la Vallée Poussin 1896) and Stieltjes/Abel partial summation on $[2^-, y]$:
          $$
          \sum_{p\le y} p^{-1/2}\cos\!\left(a\,\frac{\log p}{\log y}\right) = \pi(y)\,\phi_y(y) - \int_2^y \pi(x)\,\phi_y'(x)\,dx.
          $$
          The upper boundary term is $\pi(y)\phi_y(y) = \bigl(\cos a + o(1)\bigr)\frac{\sqrt{y}}{\log y}$. In $-\int_2^y \pi(x)\phi_y'(x)\,dx$, the sine derivative term is $O\!\bigl(\frac{|a|}{\log y}\int_2^y \frac{x^{-1/2}}{\log x}\,dx\bigr) = O\!\bigl(\frac{\sqrt{y}}{(\log y)^2}\bigr) = o\!\bigl(\frac{\sqrt{y}}{\log y}\bigr)$, and splitting $[2, y]$ at $y_0 = y/(\log y)^2$ gives $\frac{1}{2}\int_{y_0}^y \frac{x}{\log x}(1 + o(1))x^{-3/2}\cos\!\bigl(a\frac{\log x}{\log y}\bigr)dx = \bigl(\cos a + o(1)\bigr)\frac{\sqrt{y}}{\log y} + O\!\bigl(\frac{\sqrt{y}\log\log y}{(\log y)^2}\bigr)$, so
          $$
          \sum_{p\le y} p^{-1/2}\cos\!\left(a\,\frac{\log p}{\log y}\right) = \bigl(2\cos a + o(1)\bigr)\frac{\sqrt{y}}{\log y} \qquad (y \to \infty).
          $$
          (The classical arithmetic input is the Prime Number Theorem $\pi(x) \sim x/\log x$ together with Mertens' bound $\sum_{p\le y} p^{-1} = O(\log\log y)$; numerical samples do not establish this asymptotic.)
          Evaluating at $a = \frac{7\tau}{16} = \frac{\tau}{2} - \frac{\tau}{16}$, where $-2\cos(7\tau/16) = 2\cos(\tau/16) = \sqrt{2 + \sqrt{2}}$, yields the exact left-endpoint asymptotic:
          $$
          \boxed{\log\bigl|E_y(i t_{y,-})\bigr|^2 = \bigl(4\cos(\tau/16) + o(1)\bigr)\frac{\sqrt{y}}{\log y}, \qquad 4\cos(\tau/16) = 4\cos(\pi/8) = 2\sqrt{2 + \sqrt{2}} \approx 3.695518130045147,}
          $$
          whereas at the right endpoint $t_{y,+} = \frac{\tau}{2\log y}$ ($a_+ = \tau/2$, $\cos(\tau/2) = -1$), $\log|E_y(i t_{y,+})|^2 = \bigl(4 + o(1)\bigr)\frac{\sqrt{y}}{\log y}$.
     3. *Proved Local Monotonicity of $H_0(it)$ on $[0, 1]$ and Finite-Table Interval Coverage*:
        - **Failure of Global Monotonicity**:
          The kernel $H_0(it) = \frac{(t^2+1/4)^4}{1024}(\tau/2)^{-1/2}\bigl|\Gamma(1/4 + it/2)\bigr|^2$ is **not** globally increasing on $t \ge 0$; by Stirling's formula, $H_0(it) = O(|t|^{15/2} e^{-\tau |t|/4}) \to 0$ as $t \to \infty$ (certified in 256-bit Arb: $H_0(i t_{2,+}) \approx 0.34890917 > H_0(5i) \approx 0.34638197 > H_0(10i) \approx 0.02358028 > H_0(20i) \approx 6.381676 \times 10^{-7} < H_0(0) \approx 2.829093 \times 10^{-5}$).
        - **Canonical Weierstrass Product and Local Monotonicity on $0 \le t \le 1$**:
          Applying the Weierstrass product for $1/\Gamma(s)$ to $|\Gamma(1/4 + it/2)|^2 / \Gamma(1/4)^2 = (1 + v)^{-1}\prod_{n=1}^\infty \bigl(1 + \frac{v}{(4n+1)^2}\bigr)^{-1}$ with $v = 4t^2$ and $(1 + 4t^2)^4 = (1 + v)^4$ yields the canonical product identity:
          $$
          \boxed{\frac{H_0(it)}{H_0(0)} = (1 + v)^3 \prod_{n=1}^\infty \left(1 + \frac{v}{(4n + 1)^2}\right)^{-1}, \qquad v = 4t^2.}
          $$
          On any compact interval $v \in [0, V]$, each logarithmic derivative term satisfies $\bigl|\frac{d}{dv}\log\bigl(1 + \frac{v}{(4n+1)^2}\bigr)\bigr| = \frac{1}{(4n+1)^2 + v} \le \frac{1}{(4n+1)^2} < \frac{1}{16 n^2}$ with $\sum_{n=1}^\infty \frac{1}{16 n^2} = \frac{\tau^2}{384} < \infty$, justifying term-by-term differentiation by the Weierstrass M-test. For $0 \le t \le 1$ ($0 \le v \le 4$):
          $$
          \boxed{\frac{d}{dv}\log\frac{H_0(it)}{H_0(0)} = \frac{3}{1 + v} - \sum_{n=1}^\infty \frac{1}{(4n + 1)^2 + v} \ge \frac{3}{5} - \frac{\tau^2}{384} \approx 0.4971916208 > 0.}
          $$
          Hence $H_0(it)$ is strictly increasing on $0 \le t \le 1$. Since $t_{y,+} = \frac{\tau}{2\log y} = \frac{\pi}{\log y} \le 1 \iff y \ge e^\pi \approx 23.14069$, we have $I_y \subset [0, 1]$ for all integer $y \ge 24$ (verified in Arb: $t_{23,+} \approx 1.0019 > 1 > t_{24,+} \approx 0.9885$), proving $\inf_{t\in I_y} H_0(it) = H_0(i t_{y,-}) > H_0(0)$ for all integer $y \ge 24$.
        - **Finite-Table Coverage for $y < 24$ ($y \in \{2, 5, 11\}$)**:
          On $0 \le t \le 2$ ($0 \le v \le 16$, covering $y = 5, 11$), $\frac{d}{dv}\log\frac{H_0(it)}{H_0(0)} \ge \frac{3}{17} - \frac{\tau^2}{384} \approx 0.07366221 > 0$. Across the full interval $[0, t_{2,+}]$ ($t_{2,+} = \frac{\pi}{\log 2} \approx 4.53236$, $v \in [0, 82.1692]$, covering $y \in \{2, 5, 11\}$), a 64-subinterval Arb partition $[v_{j-1}, v_j]$ with analytic tail bound $\sum_{n=201}^\infty \frac{1}{(4n+1)^2+v} < \int_{200}^\infty \frac{dx}{16x^2} = \frac{1}{3200}$ certifies $\frac{d}{dv}\log\frac{H_0(it)}{H_0(0)} \ge +0.0014860189 > 0$ on every subinterval, and direct 64-subinterval Arb ball evaluation of $H_0(it)$ on $I_y$ independently encloses $\inf_{t\in I_y} H_0(it) \ge H_{0,\min}^{\mathrm{sub}}(I_y) > H_0(0)$ for every table row.
     4. *Completed Integrated Gram-Norm Divergence and Scope*:
        Combining $\inf_{t\in I_y}|E_y(it)|^2 = |E_y(i t_{y,-})|^2$ with the local kernel bound gives, for all integer $y \ge 24$ (and all certified finite-table rows):
        $$
        \boxed{\|\Psi_y\|_{L^2(d^\times x)}^2 = \frac{1}{\tau}\int_{-\infty}^\infty |E_y(it)|^2 H_0(it)\,dt \ge \frac{2}{\tau}\int_{t_{y,-}}^{t_{y,+}} |E_y(it)|^2 H_0(it)\,dt \ge \frac{H_0(0)}{8\log y}\,\bigl|E_y(i t_{y,-})\bigr|^2 = \frac{H_0(0)}{8\log y}\exp\!\left[\bigl(4\cos(\tau/16) + o(1)\bigr)\frac{\sqrt{y}}{\log y}\right] \longrightarrow +\infty \quad (y \to \infty).}
        $$
        In 256-bit Arb, $|E_y(i t_{y,+})|^2$ grows from $2.91421$ ($y = 2$), $4.90328$ ($y = 5$), $3.70191$ ($y = 11$), $4.80466$ ($y = 31$), $9.66092$ ($y = 97$), $38.8152$ ($y = 199$), $389.181$ ($y = 499$), $6228.89$ ($y = 997$), $3.57730 \times 10^5$ ($y = 1999$), $1.00839 \times 10^9$ ($y = 4999$) to $6.65784855 \times 10^{12}$ ($y = 9973$, with left-endpoint minimum $|E_y(i t_{y,-})|^2 \approx 3.99370923 \times 10^8$ and lower-bound expression $\frac{H_0(0)}{8\log y}|E_y(i t_{y,-})|^2 \approx 153.3859466 \gg h_0(1) = 0.49736$). **Scope**: This proves that the unsplit critical-line Cauchy–Schwarz / Gram-norm estimate $\|\Psi_y\|_{L^2(d^\times x)} N_{\zeta',\tau}$ diverges as $y \to \infty$; it does **not** establish divergence of $W_{M(X)}(X)$, failure of the concurrent-grade hypothesis, or closure of the arithmetic cancellation obligation.

3. **Mechanism B — Prime-by-Prime Recursion & Coupled-Cutoff Horizon Collapse vs. Scale-Horizon Tail Growth**:
   - In the recursion $W_{p_k}(X) = W_{p_{k-1}}(X) - p_k^{-1/2}W_{p_{k-1}}(X/p_k)$, evaluating the $O(u^{-1/2}\log(u+2))$ decay of $W_{\log}(u)$ at $u = X/m \ge 1$ yields $m^{-1/2}(X/m)^{-1/2} = X^{-1/2}$, canceling the $m^{-1/2}$ weight identically across all $m \le X$.
   - Whenever $y \ge N \ge 2$, every integer $1 \le m \le N$ has all prime factors $\le m \le N \le y$, so $m \mid P_y \iff \mu(m) \ne 0$ and $\mu_y(m) = \mu(m)$ for all $1 \le m \le N$. Splitting at the bare scale horizon $N = \lfloor X\rfloor$ leaves the small-scale tail bound $\frac{C_{\log,0}X^{5/2}}{2\lfloor X\rfloor^2} = O(\sqrt{X})$, which grows with $X$ and does **not** yield a uniform $O(1)$ equivalence with $W(X)$. At the coupled cutoff $N = M(X) = \lceil\max(2, X^{5/4})\rceil$, the $m > M(X)$ tail is uniformly bounded by $\frac{1}{2}C_{\log,0} < 0.278715$, and for $y \ge M(X)$ the $m \le M(X)$ divisor sum of $W_y(X)$ **collapses term-by-term to the additive Möbius truncation** $W_{\log}(X) + R_{\mu, M(X)}(X)$, while on the coefficient side $\lambda_{M(X)}(n) = \Lambda(n)$ for all $2 \le n < 2 q_{>M(X)}$ ($> 2M(X) \ge 2X^{5/4}$).

### 13.4 Quantitative Coupled-Cutoff Passage to $W(X)$ (`Section 15.4`)

1. **Exact Tail-Comparison Theorem (`coupled_prime_cutoff_comparison_and_boundedness_equivalence`)**:
   Since $W(X) = \sum_{m=1}^\infty \frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ and $W_y(X) = \sum_{m\mid P_y}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ share every squarefree $m \le y$, any squarefree $m$ omitted by $W_y(X)$ has a prime factor $p > y$ and hence $m \ge y + 1 > M$. Using $|W_{\log}(u)| \le C_{\log,0}\,u^{5/2}$ at $u = X/m$ gives, for all $X \ge 1$ and all $y \ge M \ge \max(2, X)$:
   $$
   \boxed{\bigl|W(X) - W_y(X)\bigr| = \bigl|R_\mu(X) - R_{\mu, y}(X)\bigr| \le \sum_{m > M} m^{-1/2}\,C_{\log,0}\!\left(\frac{X}{m}\right)^{5/2} \le \frac{C_{\log,0}\,X^{5/2}}{2 M^2}.}
   $$
2. **Coupled Prime Cutoff $y = M(X) := \lceil\max(2, X^{5/4})\rceil$ (Certified Safe Integer Cutoff in Arb without `float` Rounding)**:
   Choosing $y = M(X) := \lceil\max(2, X^{5/4})\rceil \ge X^{5/4}$ — computed directly from the Arb ball enclosure `((X_arb**5).root(4)).upper().ceil().unique_fmpz()` without passing through binary64 `float` (so `certified_coupled_cutoff_M_X_arb` returns a certified safe integer cutoff $M \ge \max(2, X^{5/4})$: if the input interval crosses an integer boundary, `upper().ceil()` may exceed the exact minimal ceiling by $1$ while preserving $M \ge X^{5/4}$ and $M^2 \ge X^{5/2}$, whereas at $X = 16 + 10^{-30}$ where $X^{5/4} = 32 + 2.5\times 10^{-30} + \cdots > 32$, it returns the exact ceiling $M(X) = 33$ while `ceil(float(...))` rounds down to $32$) — yields $M(X)^2 \ge X^{5/2}$ for all $X \ge 1$, and therefore
   $$
   \boxed{\sup_{X \ge 1}\bigl|W(X) - W_{M(X)}(X)\bigr| = \sup_{X \ge 1}\bigl|R_\mu(X) - R_{\mu, M(X)}(X)\bigr| \le \frac{1}{2}C_{\log,0} = \frac{92193}{65536}\bigl(-\zeta'(3)\bigr) = 0.2787147936 < 0.278715.}
   $$
   By the smooth/rough tail partition $R_\mu(X) - R_{\mu, M(X)}(X) = T_{\mathrm{smooth}, M(X)}(X) + T_{\mathrm{rough}, M(X)}(X)$, the additive truncation $R_{\mu, M(X)}(X) := \sum_{2\le m\le M(X)}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ also satisfies $\bigl|W_{M(X)}(X) - (W_{\log}(X) + R_{\mu, M(X)}(X))\bigr| \le \frac{1}{2}C_{\log,0} < 0.278715$. Consequently,
   $$
   \sup_{X \ge 1}\bigl|W_{M(X)}(X)\bigr| < \infty \iff \sup_{X \ge 1}\bigl|R_{\mu, M(X)}(X)\bigr| < \infty \iff \sup_{X \ge 1}\bigl|W(X)\bigr| < \infty \iff \sup_{X \ge 1}\bigl|R_\mu(X)\bigr| < \infty \iff \sup_{K \in \mathbb{A}_{\mathbb{R}}}\bigl|C_\tau(K)\bigr| < \infty \iff \text{RH}.
   $$

| Admissible Grade $K \in \mathbb{A}_{\mathbb{R}}$ | Scale $X_K = \tau^{|K|}$ | Coupled Cutoff $M(X_K)$ | Agreement Window $2 q_{>M(X_K)}$ | Certified $W(X_K)$ | Certified $W_{M(X_K)}(X_K)$ | Actual $\bigl|W - W_{M(X_K)}\bigr|$ | Proven Tail Bound $\frac{C_{\log,0}X_K^{5/2}}{2 M(X_K)^2}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $K = 0$ | $1.000000$ | $2$ | $6$ | $-0.0573074851$ | $-0.0252160046$ | $0.0320914805$ | $0.0696786984 \le 0.278715$ |
| $K = \pm 1/100$ | $1.018548$ | $2$ | $6$ | $-0.0588212584$ | $-0.0252936818$ | $0.0335275766$ | $0.0729400143 \le 0.278715$ |
| $K = \pm 1/4$ | $1.582981$ | $2$ | $6$ | $+0.0784856931$ | $+0.1753559540$ | $0.0968702609$ | $0.2194922886 \le 0.278715$ |
| $K = \pm 1/2$ | $2.506628$ | $4$ | $10$ | $+0.0558632743$ | $+0.0528822749$ | $0.0029809994$ | $0.1736218991 \le 0.278715$ |
| $K = \pm 1$ | $6.283185$ | $10$ | $22$ | $-0.0120796090$ | $-0.0149335756$ | $0.0028539666$ | $0.2765240899 \le 0.278715$ |
| $K = \pm 3/2$ | $15.749610$ | $32$ | $66$ | $+0.0029755342$ | $+0.0033828290$ | $0.0004072948$ | $0.2683565224 \le 0.278715$ |
| $K = \pm 2$ | $39.478418$ | $100$ | $202$ | $-0.0019168122$ | $-0.0018874957$ | $0.0000293165$ | $0.2749033540 \le 0.278715$ |

### 13.5 Outcome Classification & Remaining Obligation (`SUBGATE-TC-043A`)

- **Why Finite-Prime Euler Inversion Is an Exact Quantitative Equivalence / Reformulation, Not an Unconditional Closure**:
  Finite-prime Euler inversion establishes:
  1. an exact prime-by-prime operator product $W_y(X) = \prod_{p\le y}(I - p^{-1/2}D_p)W_{\log}(X)$ whose coefficients $\lambda_y(n)$ agree identically with $\Lambda(n)$ for all $2 \le n < 2 q_{>y}$,
  2. an unconditional uniform bound for each fixed $y$ via the Euler-sieved seed Gram norm $\|\Psi_y\|_{L^2(d^\times x)}$, and
  3. a quantitative coupled-cutoff reduction showing that $W_{M(X)}(X)$ and $W_{\log}(X) + R_{\mu, M(X)}(X)$ at $M(X) = \lceil\max(2, X^{5/4})\rceil$ approximate $W(X)$ within $\frac{1}{2}C_{\log,0} < 0.278715$ for all $X \ge 1$.
  However, the unsplit critical-line Gram norm $\|\Psi_y\|_{L^2(d^\times x)}^2 \ge \frac{H_0(0)}{8\log y}|E_y(i t_{y,-})|^2 = \frac{H_0(0)}{8\log y}\exp\bigl[(4\cos(\tau/16) + o(1))\frac{\sqrt{y}}{\log y}\bigr] \to +\infty$ ($4\cos(\tau/16) = 2\sqrt{2+\sqrt{2}} \approx 3.695518130045147$, proved for $y \ge 24$ via the Weierstrass product local monotonicity of $H_0(it)$ on $[0, 1]$ and PNT partial summation of the full prime product) diverges as $y \to \infty$ over the controlled-width low-frequency interval $I_y = [\frac{7\tau}{16\log y}, \frac{\tau}{2\log y}]$, and at $y \ge M(X)$ the divisor range $m \le M(X)$ of $W_y(X)$ collapses term-by-term to $W_{\log}(X) + R_{\mu, M(X)}(X)$ (while at $N = \lfloor X\rfloor$ the available small-scale tail estimate grows as $O(\sqrt{X})$). Assuming uniform boundedness of $W(X)$, $R_\mu(X)$, $W_{M(X)}(X)$, or $R_{\mu, M(X)}(X)$ without proof would be circular with `SUBGATE-TC-043A`.
- **Remaining Open Obligation (`SUBGATE-TC-043A`, Status: `OPEN`)**:
  Prove without assuming RH or universal Weil positivity that there exists $M_\mu < \infty$ such that for all $X \ge 1$, $\bigl|R_\mu(X)\bigr| \le M_\mu$ (equivalently, $\bigl|W_{M(X)}(X)\bigr| \le M_y$ or $\bigl|R_{\mu, M(X)}(X)\bigr| \le M_{\mathrm{trunc}}$ at the coupled cutoff $M(X) = \lceil\max(2, X^{5/4})\rceil$, where $|W(X) - W_{M(X)}(X)| < 0.278715$ and $|W_{M(X)}(X) - (W_{\log}(X) + R_{\mu, M(X)}(X))| < 0.278715$; by contrast, at $N = \lfloor X\rfloor$ the available small-scale tail estimate grows as $O(\sqrt{X})$).

---

## 14. Common-Referent Observable from Actual Prime/Theta Data and Required Integer-Layer Membership (`TASK-TC-047`, `Section 16`)

### 14.1 Construction of the Multiplicative Prime-Euler Observable $\mathcal{N}_y(x)$ and Grade-$K$ Realization $\mathcal{A}_{K,y}(x) \in L_K^\times$ (`Section 16.1–16.2`)

Starting from the actual prime-by-prime Euler weights $\lambda_y(n) = (\mu_y * \log)(n)$ and summatory factorial-divisor function $L_y(x) = \sum_{2\le n\le x}\lambda_y(n) = \sum_{d \mid P_y, d\le x}\mu(d)\log(\lfloor x/d\rfloor!)$ established in `TASK-TC-046` (`tc/prime_euler_moebius_recovery.py`) together with the canonical graded ring family $\Phi_K : (\mathbb{Z}_K, \oplus_K, \odot_K) \xrightarrow{\sim} L_K = \tau^K\mathbb{Z} \subset \mathbb{R}$ ($\Phi_K(\operatorname{fromZ}(K, m)) = m\tau^K$, $N_K(x) = \tau^{-K}x$; `formal/RiemannScope/GradedRingIso.lean`), `TASK-TC-047` (`tc/common_referent_prime_theta_bridge.py`) constructs the multiplicative prime-Euler factor $m_y(n)$, cumulative factorial-ratio observable $\mathcal{N}_y(x)$, and grade-$K$ integer-layer realization $\mathcal{A}_{K,y}(x)$:
$$
\boxed{m_y(n) := \exp\bigl(\lambda_y(n)\bigr) = \prod_{d \mid \gcd(n, P_y)}\left(\frac{n}{d}\right)^{\mu(d)} = \begin{cases} 1, & n = 1 \text{ or } \omega_{\le y}(n) \ge 2, \\ n, & n \ge 2 \text{ and } \omega_{\le y}(n) = 0, \\ p, & n = p^a n_{>y} \text{ with } \omega_{\le y}(n) = 1 \text{ ($p \le y$, $a \ge 1$)}, \end{cases}}
$$
$$
\boxed{\mathcal{N}_y(x) := \exp\bigl(L_y(x)\bigr) = \prod_{\substack{d \mid P_y \\ d \le x}}\bigl(\lfloor x/d\rfloor!\bigr)^{\mu(d)} = \prod_{1\le n\le \lfloor x\rfloor} m_y(n), \qquad \mathcal{A}_{K,y}(x) := \Phi_K\bigl(\operatorname{fromZ}(K, \mathcal{N}_y(x))\bigr) = \mathcal{N}_y(x)\,\tau^K.}
$$

**Theorem (`prime_euler_multiplicative_integrality_and_grade_layer_membership`).** For every real $x \ge 1$, every prime cutoff $y \ge 2$, and every concurrent grade $K \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$:
1. **Unconditional Positive-Integer Membership of the Alternating Factorial Product**:
   Even though $\prod_{d\mid P_y, d\le x}(\lfloor x/d\rfloor!)^{\mu(d)}$ divides by $\lfloor x/d\rfloor!$ for every squarefree divisor $d \mid P_y$ with $\mu(d) = -1$, expanding $\lfloor x/d\rfloor! = \prod_{1\le j\le x/d} j$ and setting $n = d j$ yields $\mathcal{N}_y(x) = \prod_{1\le n\le \lfloor x\rfloor} m_y(n)$. Since $m_y(n) \in \{1, p, n\} \subset \mathbb{Z}_{\ge 1}$ divides $n$ for every $n \ge 1$, every factorial denominator divides the numerator identically (`Fraction.denominator == 1`), so $\mathcal{N}_y(x) \in \mathbb{Z}_{\ge 1}$ is unconditionally a positive integer, and for every prime $p$ its Legendre valuation satisfies $E_{y,p}(x) := v_p(\mathcal{N}_y(x)) = \sum_{d\mid P_y, d\le x}\mu(d)\,v_p(\lfloor x/d\rfloor!) \ge 0$.
2. **Exact Chebyshev LCM Agreement Window and First Discrepancy Factor**:
   For all $1 \le x < 2 q_{>y}$ (where $q_{>y} = \min\{p \text{ prime} : p > y\}$), $m_y(n) = e^{\Lambda(n)}$ for all $1 \le n \le \lfloor x\rfloor$, and hence
   $$
   \boxed{\mathcal{N}_y(x) = e^{\psi(x)} = \operatorname{lcm}(1, 2, \dots, \lfloor x\rfloor) \in \mathbb{Z}_{\ge 1} \qquad (1 \le x < 2 q_{>y}), \qquad \mathcal{N}_y(2 q_{>y}) = 2\,\operatorname{lcm}(1, 2, \dots, 2 q_{>y}).}
   $$
   In particular, at the coupled prime cutoff $y = M(X) = \lceil\max(2, X^{5/4})\rceil$, $\mathcal{N}_{M(X)}(x) = \operatorname{lcm}(1, \dots, \lfloor x\rfloor)$ holds across the entire super-scale horizon $1 \le x < 2 q_{>M(X)}$ ($> 2 M(X) \ge 2 X^{5/4}$).
3. **Required Grade-Layer Membership (`CR2`) vs. Unit-Converted Coordinate Recovery (Not Raw `CR1`)**:
   Since $\mathcal{N}_y(x) \in \mathbb{Z}_{\ge 1} \subset \mathbb{Z} \setminus \{0\}$, the grade-$K$ observable satisfies required integer-layer membership unconditionally:
   $$
   \boxed{\mathcal{A}_{K,y}(x) = \mathcal{N}_y(x)\,\tau^K \in L_K^\times = \tau^K(\mathbb{Z}\setminus\{0\}) \subset L_K = \tau^K\mathbb{Z} \qquad \forall K \in \mathbb{A}_{\mathbb{R}}, \;\; \forall x \ge 1, \;\; \forall y \ge 2.}
   $$
   Dividing by $\tau^K$ recovers the intrinsic integer coordinate $N_K(\mathcal{A}_{K,y}(x)) = \tau^{-K}\mathcal{A}_{K,y}(x) = \mathcal{N}_y(x) = N_J(\mathcal{A}_{J,y}(x)) \in \mathbb{Z}_{\ge 1}$, whereas the **raw external values** satisfy $\mathcal{A}_{K,y}(x) = \tau^{K-J}\mathcal{A}_{J,y}(x) > 0$ and are **strictly unequal whenever $K \ne J$** (so $\tau^{-K}\mathcal{A}_{K,y}(x) = \tau^{-J}\mathcal{A}_{J,y}(x)$ is unit-converted coordinate recovery, **not** raw external `CR1`).

| Prime Cutoff $y$ | Next Prime $q_{>y}$ | First Discrepancy $2 q_{>y}$ | Verified Range $1 \le n \le n_{\max}$ | All Factorial-Ratio Denominators $= 1$ | Exact $\mathcal{N}_y(2q_{>y}-1) = \operatorname{lcm}(1,\dots,2q_{>y}-1)$ | Exact $\mathcal{N}_y(2q_{>y}) = 2\,\operatorname{lcm}(1,\dots,2q_{>y})$ | Ratio $\frac{\mathcal{N}_y(2q_{>y})}{\operatorname{lcm}(1,\dots,2q_{>y})}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $y = 2$ | $3$ | $6$ | $1 \le n \le 45$ | `True` | $60$ | $120$ | $2$ |
| $y = 3$ | $5$ | $10$ | $1 \le n \le 45$ | `True` | $2520$ | $5040$ | $2$ |
| $y = 5$ | $7$ | $14$ | $1 \le n \le 45$ | `True` | $360360$ | $720720$ | $2$ |
| $y = 7$ | $11$ | $22$ | $1 \le n \le 45$ | `True` | $232792560$ | $465585120$ | $2$ |
| $y = 11$ | $13$ | $26$ | $1 \le n \le 45$ | `True` | $26771144400$ | $53542288800$ | $2$ |
| $y = 13$ | $17$ | $34$ | $1 \le n \le 45$ | `True` | $144403552893600$ | $288807105787200$ | $2$ |

### 14.2 Mellin–Stieltjes & Cross-Grade Station-Ratio Bridge to $W_y(\tau^{K-J})$ (`Section 16.3`)

**Theorem (`common_referent_integer_layer_bridge_and_station_ratio_identity`).** For any concurrent grades $K, J \in \mathbb{A}_{\mathbb{R}}$ with relative scale $X_{K,J} := \tau^{K-J}$ ($K \ge J$):
1. **Explicit Lower-Endpoint Stieltjes Convention & Consecutive Ratio Scale Cancellation**: Extend $\mathcal{A}_{K,y}(x)$ constantly as $\tau^K$ below $1$ (so $\mathcal{A}_{K,y}(x) = \tau^K$ for all $x \in (0, 2)$), or integrate over the open half-line $(1, \infty)$, so that $d(\log\mathcal{A}_{K,y})(x)$ has **zero atom at $x = 1$** (no artificial $K\log\tau$ boundary term). Inside the nonzero integer layer $L_K^\times = \tau^K(\mathbb{Z}\setminus\{0\})$, the consecutive step ratio at integers $n \ge 2$ cancels $\tau^K$ identically and equals the local prime-Euler integer factor:
   $$
   \frac{\mathcal{A}_{K,y}(n)}{\mathcal{A}_{K,y}(n-1)} = \frac{\mathcal{N}_y(n)\,\tau^K}{\mathcal{N}_y(n-1)\,\tau^K} = m_y(n) \in \mathbb{Z}_{\ge 1}, \qquad \log\left(\frac{\mathcal{A}_{K,y}(n)}{\mathcal{A}_{K,y}(n-1)}\right) = \lambda_y(n).
   $$
2. **Cross-Grade Station Ratio and Exact Stieltjes Bridge**: The kernel argument $n / X_{K,J} = n / \tau^{K-J}$ is the exact ratio of the $n$-th integer-layer station $\Phi_J(n) = n\tau^J \in L_J^\times$ at grade $J$ to the unit station $\Phi_K(1) = \tau^K \in L_K^\times$ at grade $K$:
   $$
   \frac{\Phi_J(n)}{\Phi_K(1)} = \frac{n\tau^J}{1\cdot\tau^K} = \frac{n}{\tau^{K-J}} = \frac{n}{X_{K,J}},
   $$
   so under the lower-endpoint convention $\mathcal{A}_{K,y}(x) = \tau^K$ on $(0, 2)$ (or integration over $(1, \infty)$), the finite-prime theta-wavelet profile $W_y(X_{K,J})$ is generated directly by the integer-layer observables $\mathcal{A}_{K,y}(n) \in L_K^\times$ and the cross-grade station ratios $\Phi_J(n)/\Phi_K(1)$:
   $$
   \boxed{W_y(\tau^{K-J}) = \int_{(1, \infty)} x^{-1/2}\,h_0\!\left(\frac{x\tau^J}{\tau^K}\right) d\bigl(\log\mathcal{A}_{K,y}(x)\bigr) = \sum_{n=2}^\infty \log\!\left(\frac{\mathcal{A}_{K,y}(n)}{\mathcal{A}_{K,y}(n-1)}\right) n^{-1/2}\,h_0\!\left(\frac{\Phi_J(n)}{\Phi_K(1)}\right).}
   $$
3. **Avoidance of the Self-Dual Peak $\alpha = 1$ Across Nonzero Rational Grade Differences**:
   By Lindemann's theorem ($\tau = 2\pi \notin \overline{\mathbb{Q}}$), for every nonzero rational grade difference $K - J \in \mathbb{Q} \setminus \{0\}$, the integer layers are disjoint outside zero ($L_K \cap L_J = \{0\}$), so $\Phi_J(n) = n\tau^J \ne m\tau^K = \Phi_K(m)$ for all $n, m \in \mathbb{Z} \setminus \{0\}$. In particular, no prime-power station $n \ge 2$ at grade $J$ ever lands at the self-dual autocorrelation peak $\Phi_J(n)/\Phi_K(1) = 1$ of grade $K$.
4. **Distinction Between Paper Derivation, Finite Computation, and Lean 4 Scope**:
   - **Mathematical Derivation**: Proves unconditionally for all real $x \ge 1$ and integer $y \ge 2$ that $\mathcal{N}_y(x) = \prod_{d\mid P_y, d\le x}(\lfloor x/d\rfloor!)^{\mu(d)} = \prod_{n\le x}m_y(n) \in \mathbb{Z}_{\ge 1}$, $\mathcal{N}_y(x) = \operatorname{lcm}(1, \dots, \lfloor x\rfloor)$ for $1 \le x < 2 q_{>y}$, $\mathcal{N}_y(2q_{>y}) = 2\operatorname{lcm}(1, \dots, 2q_{>y})$, and $\mathcal{A}_{K,y}(x) = \mathcal{N}_y(x)\tau^K \in L_K^\times$.
   - **Finite Computational Verification**: Certifies exact integer/rational denominator cancellation (`Fraction.denominator == 1`) for $y \in \{2, 3, 5, 7, 11, 13\}$ and $1 \le n \le \max(45, 2q_{>y}+6)$, and 256-bit Arb ball enclosures across 15 positive and negative grades $K \in \mathbb{A}_{\mathbb{R}}$.
   - **Lean 4 Scope**: The Lean 4 theorems `prime_euler_multiplicative_integrality_and_grade_layer_membership` and `common_referent_integer_layer_bridge_and_station_ratio_identity` prove the algebraic consequences for supplied integer inputs (`finitePrimeMultiplicativeFactorCases`, step-ratio cancellation of $\tau^K$, coboundary relation $\mathcal{A}_{K,y} = \tau^{K-J}\mathcal{A}_{J,y}$, station-ratio identity $\Phi_J(n)/\Phi_K(1) = n/\tau^{K-J}$, and conditional collision implication under supplied `CR1` + `CR2` + `CR3` hypotheses); they do **not** internally formalize the full alternating factorial-product divisor cancellation or derive the missing `CR1` + `CR2` + `CR3` collision hypotheses from actual prime/theta data.

### 14.3 Rigorous Three-Class `CR1`–`CR2`–`CR3` Bridge Audit & Open Obligation (`Section 16.4`, `SUBGATE-TC-043A = OPEN`)

| Observable Class Constructed from Actual Prime/Theta Data | `CR1` (Raw Cross-Grade Equality $D_K = D_J$) | `CR2` (Discrete Scaled Integer-Layer Membership) | `CR3` (Sensitivity to Off-Critical Zeros $\delta = \operatorname{Re}(\rho) - 1/2 \ne 0$) |
| :--- | :--- | :--- | :--- |
| **Class I — Intrinsic Fiber Coordinate** $N_K(\mathcal{A}_{K,y}(x)) = \tau^{-K}\mathcal{A}_{K,y}(x) = \mathcal{N}_y(x)$ | Unit-converted coordinate recovery after dividing by $\tau^K, \tau^J$ (**not** raw external `CR1`, since $\mathcal{A}_{K,y}(x) \ne \mathcal{A}_{J,y}(x)$ for $K \ne J$) | Lives in the single base ring $\mathbb{Z}_{\ge 1}$ (not in $L_K \cap L_J$ for $K \ne J$) | Purely arithmetic carrier independent of $\delta$ |
| **Class II — Ambient Integer-Layer Observable** $\mathcal{A}_{K,y}(x) = \mathcal{N}_y(x)\,\tau^K \in L_K^\times$ | **Fails raw `CR1`**: obeys the scale coboundary $\mathcal{A}_{K,y}(x) = \tau^{K-J}\mathcal{A}_{J,y}(x) \ne \mathcal{A}_{J,y}(x)$ for $K \ne J$; ambient equality $m_K\tau^K = m_J\tau^J$ for rational $K \ne J$ forces $m_K = m_J = 0$ (`L_K \cap L_J = \{0\}`) | **Proved Unconditionally**: $\mathcal{A}_{K,y}(x) \in L_K^\times = \tau^K(\mathbb{Z}\setminus\{0\}) \subset L_K = \tau^K\mathbb{Z}$ for all $x \ge 1$, $y \ge 2$, $K \in \mathbb{A}_{\mathbb{R}}$ | Conditional reductio schema (`common_referent_integer_layer_bridge_and_station_ratio_identity`): requires a zero-defect-modulated integer-layer observable $D_K = m_K(\delta)\tau^K \in L_K$ satisfying $D_K = D_J$ for $K \ne J$ and $\delta \ne 0 \implies m_K(\delta) \ne 0$ |
| **Class III — Coupled Theta-Wavelet Profile** $F(X) = W_{M(X)}(X)$ ($X = \tau^{K-J}$) | Shift-invariant across simultaneous grade translations $(K, J) \mapsto (K+A, J+A)$ | Piecewise continuous Mellin–Stieltjes integral over the integer-layer jumps $\log(\mathcal{A}_{K,M(X)}(n)/\mathcal{A}_{K,M(X)}(n-1))$ weighted by $n^{-1/2}h_0(\Phi_J(n)/\Phi_K(1)) \in \mathbb{R}$ (with right-hand jumps $-p^{-1/2}W_{p^-}(X_0/p)$ at $X_0 = (p-1)^{4/5}$) | **Proved**: $\sup_{X\ge 1}|W_{M(X)}(X)| < \infty \iff \sup_{X\ge 1}|R_\mu(X)| < \infty \iff \sup_{K\in\mathbb{A}_{\mathbb{R}}}|C_\tau(K)| < \infty \iff \text{RH}$ (dense-grade extension uses continuity of $W(X)$ + uniform comparison $|F(X)-W(X)| \le \frac{1}{2}C_{\log,0} < 0.278715$, **never** continuity of $F(X)$) |

---

## 15. Coupled-Cutoff Piecewise Continuity & Right-Hand Jump Formula and Single-Observable Common-Referent Audit (`TASK-TC-048`, `Section 17`)

### 15.1 Piecewise Continuity and Exact Right-Hand Jump Formula for $F(X) = W_{M(X)}(X)$ (`Section 17.2`, Theorem 48)

1. **Continuity of Fixed-$y$ $W_y(X)$ vs. Piecewise Continuity of $F(X) := W_{M(X)}(X)$**:
   For any fixed prime cutoff $y \ge 2$, $W_y(X) = \sum_{m\mid P_y}\frac{\mu(m)}{\sqrt{m}}W_{\log}(X/m)$ is a finite linear combination of dilates of the continuous function $W_{\log} \in C((0, \infty))$ and is therefore continuous on $(0, \infty)$.
   By contrast, for the coupled cutoff schedule $M(X) = \lceil\max(2, X^{5/4})\rceil$, $M(X) = 2$ on $[1, 2^{4/5}]$ and $M(X) = m + 1$ on each half-open interval $(m^{4/5}, (m+1)^{4/5}]$ ($m \ge 2$). Hence $F(X) := W_{M(X)}(X)$ is continuous on each half-open interval $(m^{4/5}, (m+1)^{4/5}]$ and left-continuous at $X_m = m^{4/5}$, while across $X_m = m^{4/5}$:
   - If $m + 1$ is **composite** (e.g. $m + 1 = 4$, $X_0 = 3^{4/5}$), no new prime enters the primorial ($P_{m+1} = P_m$), so $W_{m+1}(X) \equiv W_m(X)$ and $F(X_m^+) - F(X_m) = 0$.
   - If $m + 1 = p \ge 3$ is **prime**, let $X_0 := (p - 1)^{4/5}$. Then $M(X_0) = p - 1$ and $\lim_{X \to X_0^+} M(X) = p$. By continuity of $W_{p^-}$ and $W_p$ at $X_0$ together with the one-prime Euler recursion $W_p(X) = (I - p^{-1/2}D_p)W_{p^-}(X) = W_{p^-}(X) - p^{-1/2}W_{p^-}(X/p)$, the exact right-hand jump is:
     $$
     \boxed{F(X_0^+) - F(X_0) = W_p(X_0) - W_{p^-}(X_0) = -p^{-1/2}\,W_{p^-}\!\left(\frac{X_0}{p}\right), \qquad X_0 = (p - 1)^{4/5},}
     $$
     where $W_{p^-} = W_{p-1}$ includes precisely the primes strictly below $p$ (`coupled_cutoff_prime_step_jump_and_dense_comparison_extension`).
2. **Exact Nonvanishing & Sign Criterion for the Prime-Step Jump**:
   Since $p^{-1/2} > 0$, $F(X_0^+) - F(X_0) \ne 0 \iff W_{p^-}((p-1)^{4/5}/p) \ne 0$.
   - **Small-Prime Regime ($p \in \{3, 5, 7, 11, 13, 17, 19, 23\}$)**: For $u_p := (p - 1)^{4/5}/p$, the leading station ratio $\alpha_2(p) = 2/u_p \in [3.298770, 3.879892]$ lies in the positive lobe $(\alpha_2^*, \alpha_3^*) \approx (2.6941, 8.6213)$ of $h_0(\alpha)$ (where $W = (\alpha + 1/\alpha)^2 \in (W_2, W_3) \approx (9.3873, 76.3403)$ makes $-648 W^3 + 58380 W^2 - 706860 W + 2027025 > 0$). Thus $W_{p^-}(u_p) > 0$ and the right-hand jump $F(X_0^+) - F(X_0) = -p^{-1/2}W_{p^-}(u_p) < 0$ is certified strictly negative and nonzero in 256-bit Arb.
   - **Asymptotic Negative-$h_0$-Tail Regime ($p \ge 1901$)**: Since $W_{p^-}(u_p) = \sum_{n=2}^\infty \frac{\lambda_{p^-}(n)}{\sqrt{n}}h_0(n / u_p)$ has nonnegative coefficients $\lambda_{p^-}(n) \ge 0$ with $\lambda_{p^-}(2) = \log 2 > 0$, and $h_0(\alpha) < 0$ strictly for all $\alpha \ge 9 > \alpha_3^* \approx 8.6213$, for every prime $p \ge 1901$ (where $u_p := (p - 1)^{4/5}/p \le 2/9$), every station satisfies $n / u_p \ge 2 / u_p \ge 9$, so $W_{p^-}(u_p) < 0$ strictly and $F(X_0^+) - F(X_0) = -p^{-1/2}W_{p^-}(u_p) > 0$ strictly (certified at $p = 1901$).
3. **Corrected Extension from Dense Grade Samples $K \in \mathbb{A}_{\mathbb{R}}$ to All Real Scales $X \ge 1$**:
   Because $F(X) = W_{M(X)}(X)$ has right-hand jumps at prime thresholds $X_0 = (p - 1)^{4/5}$, one must **never** invoke continuity of $F(X)$ to pass from dense grade samples $K \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}}\cap\mathbb{R}$ to all $X \ge 1$. Instead, $W(X) = W_{\log}(X) + R_\mu(X)$ **is** continuous on $[1, \infty)$ by the compact-interval Weierstrass M-test, and the uniform comparison $|F(X) - W(X)| \le \frac{1}{2}C_{\log,0} < 0.278715$ holds for **all** real $X \ge 1$. Therefore:
   $$
   \sup_{K \in \mathbb{A}_{\mathbb{R}}}\bigl|F(\tau^{|K|})\bigr| \le M_F \implies \sup_{K \in \mathbb{A}_{\mathbb{R}}}\bigl|W(\tau^{|K|})\bigr| \le M_F + \frac{1}{2}C_{\log,0} \xrightarrow[\text{density of }\mathbb{A}_{\mathbb{R}}]{\text{continuity of }W} \sup_{X \ge 1}\bigl|W(X)\bigr| \le M_F + \frac{1}{2}C_{\log,0} \implies \sup_{X \ge 1}\bigl|F(X)\bigr| \le M_F + C_{\log,0}.
   $$

| Prime $p$ | Threshold $X_0 = (p-1)^{4/5}$ | Argument $u_p = X_0 / p$ | Min Station $\alpha_{\min} = 2 / u_p$ | Certified $F(X_0) = W_{p^-}(X_0)$ | Certified $F(X_0^+) = W_p(X_0)$ | Certified $W_{p^-}(X_0 / p)$ | Right-Hand Jump $F(X_0^+) - F(X_0) = -p^{-1/2}W_{p^-}(X_0/p)$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $p = 3$ | $1.7411011266$ | $0.5803670422$ | $3.4460950650$ | $+0.0356464373$ | $+0.0175094943$ | $+0.0314139880 > 0$ | $-0.0181368744 < 0$ |
| $p = 5$ | $3.0314331330$ | $0.6062866266$ | $3.2987697769$ | $+0.0522622747$ | $+0.0367813476$ | $+0.0346161691 > 0$ | $-0.0154808214 < 0$ |
| $p = 7$ | $4.1929627126$ | $0.5989946732$ | $3.3389278559$ | $-0.0009208039$ | $-0.0139485227$ | $+0.0344677794 > 0$ | $-0.0130275961 < 0$ |
| $p = 11$ | $6.3095734448$ | $0.5735975859$ | $3.4867650234$ | $+0.0030218458$ | $-0.0067136049$ | $+0.0322883852 > 0$ | $-0.0097353144 < 0$ |
| $p = 13$ | $7.3003721027$ | $0.5615670848$ | $3.5614622973$ | $+0.0044388096$ | $-0.0041581867$ | $+0.0309964113 > 0$ | $-0.0085968577 < 0$ |
| $p = 17$ | $9.1895868400$ | $0.5405639318$ | $3.6998398940$ | $+0.0069563004$ | $+0.0000631652$ | $+0.0284205477 > 0$ | $-0.0068929953 < 0$ |
| $p = 19$ | $10.0975963090$ | $0.5314524373$ | $3.7632718557$ | $+0.0050901147$ | $-0.0011533536$ | $+0.0272140393 > 0$ | $-0.0062433288 < 0$ |
| $p = 23$ | $11.8559987448$ | $0.5154782063$ | $3.8798924485$ | $+0.0058919327$ | $+0.0006804552$ | $+0.0249927064 > 0$ | $-0.0052113395 < 0$ |
| $p = 1901$ (tail) | $419.8655250932$ | $0.2208656103$ | $9.0552802685 \ge 9$ | — | — | $-0.0017401386 < 0$ | $+0.0000399104 > 0$ |
| $m+1 = 4$ (composite) | $2.4082246853$ | $0.6020561713$ | $3.3219491668$ | $+0.0934148036$ | $+0.0934148036$ | $+0.0347595163 > 0$ | $0.0000000000$ ($P_4 = P_3 = 6$) |

### 15.2 Single-Observable Common-Referent Candidate Audit (`CR1` + `CR2` + `CR3`) and the Covariance–Invariance–Discreteness Trilemma (`Section 17.3`, Theorem 49)

For a hypothetical nontrivial zero $\rho = \frac{1}{2} + \delta + i\gamma$ ($\delta = \operatorname{Re}(\rho) - \frac{1}{2} \in (-1/2, 1/2)$), $\rho_K = \tau^K\rho$, and two concurrent grades $K, J \in \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}}\cap\mathbb{R}$ with a justified nonzero rational difference $K - J \in \mathbb{Q}\setminus\{0\}$ (canonical pair $K = 0, J = 1$), the original common-referent collision contract (`common_referent_collision_theorem` in `formal/RiemannScope/Grade.lean`) requires **one and the same single observable** $D_K(\rho_K)$ to satisfy simultaneously:
- **CR1 (Raw Cross-Grade Equality)**: $D_K(\rho_K) = D_J(\rho_J) = D(\rho)$ as the exact same external real value in $\mathbb{R}$,
- **CR2 (Discrete Scaled Integer-Layer Membership)**: $D_K(\rho_K) = m_K\tau^K \in L_K = \tau^K\mathbb{Z}$ and $D_J(\rho_J) = m_J\tau^J \in L_J = \tau^J\mathbb{Z}$ with $m_K, m_J \in \mathbb{Z}$,
- **CR3 (One-Way Off-Critical Sensitivity)**: $\delta \ne 0 \implies D(\rho) \ne 0$ (never strengthened to a biconditional).

| Single-Observable Candidate Family | Exact Formula & Transformation Law under $\rho_K = \tau^K\rho$ | `CR1` ($D_K(\rho_K) = D_J(\rho_J)$) | `CR2` ($D_K(\rho_K) \in L_K = \tau^K\mathbb{Z}$) | `CR3` ($\delta \ne 0 \implies D(\rho) \ne 0$) |
| :--- | :--- | :--- | :--- | :--- |
| **Candidate 1A (Unmodulated Grade-$K$ Prime-Euler Carrier)** | $D_{K,y}^{(1\mathrm{A})}(\rho_K) := \mathcal{A}_{K,y}(\tau^{-K}|\rho_K|) = \mathcal{N}_y(|\rho|)\,\tau^K$; transforms with **weight $1$**: $D_{K,y}^{(1\mathrm{A})}(\rho_K) = \tau^{K-J}D_{J,y}^{(1\mathrm{A})}(\rho_J)$ | **Fails**: since $\mathcal{N}_y(|\rho|) \ge 1$, $D_{1,y}^{(1\mathrm{A})} - D_{0,y}^{(1\mathrm{A})} = \mathcal{N}_y(|\rho|)(\tau - 1) > 0$ (and at raw scale $|\rho_K|$, $\mathcal{N}_y(\tau|\rho|)\tau > \mathcal{N}_y(|\rho|)$) | **Proved Unconditionally**: $\mathcal{N}_y(|\rho|) \in \mathbb{Z}_{\ge 1} \implies D_{K,y}^{(1\mathrm{A})}(\rho_K) \in L_K^\times \subset L_K = \tau^K\mathbb{Z}$ | Vacuously nonzero ($D_{K,y}^{(1\mathrm{A})} > 0$ for all $\delta$, independent of whether $\delta = 0$ or $\delta \ne 0$) |
| **Candidate 1B (Zero-Defect-Modulated Prime-Euler Carrier)** | $D_{K,y}^{(1\mathrm{B})}(\rho_K) := m_K(\rho_K)\,\mathcal{N}_y(|\rho|)\,\tau^K$ with integer multiplier $M_K = m_K(\rho_K)\mathcal{N}_y(|\rho|) \in \mathbb{Z}$ | At $K = 0, J = 1$, $L_0 \cap L_1 = \{0\}$ (Lindemann), so **CR1 $\land$ CR2 $\iff M_0 = M_1 = 0$**; by `invariant_covariant_observable_vanishing` (`Grade.lean`), any multiplier extending continuously to a real interval $I \subset \mathbb{R}$ while taking integer values on $I \cap \mathbb{A}_{\mathbb{R}}$ is a constant $M_0 \in \mathbb{Z}$ (failing `CR1` if $M_0 \ne 0$, failing `CR3` if $M_0 = 0$) | Preserved only if $M_K \in \mathbb{Z}$ | Incompatible with `CR1` + `CR2` unless $\delta \ne 0$ is already impossible |
| **Candidate 2A (Normalized Pullback Theta-Zero Radial Defect)** | $D_K^{(2\mathrm{A})}(\rho_K) := \bigl|H_0(\tau^{-K}\rho_K - \tfrac{1}{2})\bigr|^2(\tau^{\tau^{-K}\operatorname{Re}(\rho_K)-1/2} + \tau^{-(\tau^{-K}\operatorname{Re}(\rho_K)-1/2)} - 2) = |H_0(\delta + i\gamma)|^2(\tau^\delta + \tau^{-\delta} - 2)$; transforms with **weight $0$** | **Proved Unconditionally**: $\tau^{-K}\rho_K = \rho = \tau^{-J}\rho_J \implies D_K^{(2\mathrm{A})}(\rho_K) = D_J^{(2\mathrm{A})}(\rho_J)$ as the exact same external real value for all $K, J \in \mathbb{A}_{\mathbb{R}}$ | **Equivalent to $\delta = 0$ (Not Unconditionally Proved)**: on $\|\delta\| < 1/2$, $\|\gamma\| \ge 14.13$, $0 \le D^{(2\mathrm{A})}(\rho) < 1$, so even at $K = 0$ ($L_0 = \mathbb{Z}$), $D_0^{(2\mathrm{A})}(\rho) \in \mathbb{Z} \iff D^{(2\mathrm{A})}(\rho) = 0 \iff \delta = 0$, and at $K = 0, J = 1$, $D^{(2\mathrm{A})}(\rho) \in L_0 \cap L_1 = \{0\} \iff \delta = 0$ | **Proved Unconditionally (One-Way)**: $H_0(z) = \frac{(z^2-1/4)^4}{1024\sqrt{\pi}}\Gamma(\frac{1+2z}{4})\Gamma(\frac{1-2z}{4})$ has zeros only at $z = \pm 1/2$ because $1/\Gamma$ is entire on $\mathbb{C}$, so $\|H_0(\delta+i\gamma)\|^2 > 0$ on the critical strip, and $\tau^\delta + \tau^{-\delta} - 2 = (\tau^{\delta/2} - \tau^{-\delta/2})^2 > 0$ for $\delta \ne 0$ |
| **Candidate 2B (Prime-Euler Stieltjes Shift Difference)** | $D_{K,y}^{(2\mathrm{B})}(\rho_K) := W_y(\tau^{1 + |\delta(\rho_K)|}) - W_y(\tau) = \int_{(1, \infty)} x^{-1/2}[h_0(x/\tau^{1+|\delta|}) - h_0(x/\tau)]\,d\log\mathcal{A}_{K,y}(x)$ | **Proved Unconditionally**: $d\log\mathcal{A}_{K,y}(x) = d\log\mathcal{N}_y(x)$ cancels $\tau^K$ and $\delta(\rho_K) = \delta$ is grade-invariant | **Fails for $\delta \ne 0$**: takes non-integer continuous real values in $(-1, 1)\setminus\{0\}$ | Vanishes at $\delta = 0$; certified nonzero for $\delta \in \{1/20, 1/10, 1/4\}$ at $y = 28$ |

- **Covariance–Invariance–Discreteness Trilemma (`single_observable_common_referent_candidate_audit_and_trilemma`)**:
  At any rational grade difference $K - J \in \mathbb{Q}\setminus\{0\}$ (such as $K = 0, J = 1$), Lindemann's theorem gives $L_K \cap L_J = \tau^K\mathbb{Z} \cap \tau^J\mathbb{Z} = \{0\}$ (without ever assuming layer separation for arbitrary irrational algebraic grade differences $K - J \in (\overline{\mathbb{Q}}\cap\mathbb{R})\setminus\mathbb{Q}$, which remains open in transcendental number theory). Consequently, for any single observable $D_K(\rho_K)$, $\text{CR1} \land \text{CR2} \iff D_K(\rho_K) = D_J(\rho_J) = 0$.
  - Arithmetic prime-Euler carriers $\mathcal{A}_{K,y}(x) = \mathcal{N}_y(x)\tau^K$ satisfy `CR2` unconditionally with $\mathcal{N}_y(x) \ge 1$, so they transform with weight $1$ ($\mathcal{A}_{K,y} = \tau^{K-J}\mathcal{A}_{J,y} \ne \mathcal{A}_{J,y}$) and fail raw `CR1`.
  - Spectral/theta pullback observables $D_K^{(2\mathrm{A})}(\rho_K) = |H_0(\delta+i\gamma)|^2(\tau^\delta+\tau^{-\delta}-2)$ satisfy raw `CR1` and one-way `CR3` ($\delta \ne 0 \implies D^{(2\mathrm{A})}(\rho) > 0$) unconditionally, so `CR2` ($D_K^{(2\mathrm{A})}(\rho_K) \in L_K$) holds if and only if $D^{(2\mathrm{A})}(\rho) = 0 \iff \delta = 0$, which is equivalent to RH for $\rho$ rather than an independent consequence of prime/theta algebra.
- **Status of `SUBGATE-TC-043A` (`OPEN`)**:
  `SUBGATE-TC-043A` remains `OPEN` and the common-referent bridge is **not** marked complete: closing `SUBGATE-TC-043A` requires either proving the uniform signed Möbius cancellation bound $\sup_{X\ge 1}|R_\mu(X)| < \infty$ (equivalently $\sup_{X\ge 1}|W_{M(X)}(X)| < \infty$), or deriving an independent arithmetic-spectral identity that forces a raw-invariant, off-line-sensitive observable $D_K(\rho_K)$ to lie in $L_K = \tau^K\mathbb{Z}$ without assuming $\delta = 0$.







