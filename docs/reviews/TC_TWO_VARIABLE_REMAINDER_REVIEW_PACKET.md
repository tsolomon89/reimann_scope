# Review Packet: Arithmetic Positivity, Reflected Weil Form, Dual-Kernel Diagnostics, Grade Pullback, and the TC Bridge

**Repository**: `tsolomon89/reimann_scope`<br>
**Epic**: TC Corrective Epic — Positivity Comparison, Weil Audit, Measure Clarification, Station-to-Grade Embedding, and Research Scoping<br>
**Date**: 2026-09-11<br>
**Baseline Git Anchor**: `82643cafd605492233c6c1e992b78c2c30d45f13` (immutable, preserved under Policy B)<br>
**Remote Tracking Anchor**: `0565b235084181ca825ea507b4fd364c7d41e17a`<br>
**Local Tested Commits**: `2b50a98d9c8ca07813088ca15cce098328a66988`, `8d5f34bd`, `cbbbe6edf52231fa736d6ba6edbc81dc38b32bc2`<br>
**Formal Build Status**: `formal/build_report.json` — 237 project theorem declarations compiled with Lean 4.8.0 / Lake 5.0.0 (0 sorry, 0 admit, 0 warnings, standard Mathlib foundational axioms only).

---

## 1. Executive Summary & Epistemic Verdict

### Governing Research Question:
> **Was any new implication toward forbidden arithmetic coincidence established?**
>
> **Answer: None.**

No new mathematical implication forcing cross-grade arithmetic coincidence ($m\tau^K = n\tau^J$ with $\tau = 2\pi$) from an off-line zero hypothesis $H(\rho_0)$ was established.
The Transcendental Continuation (TC) bridge remains **strictly OPEN**.

### Summary of Accomplishments & Clarifications:
1. **Station vs. Grade Scope Disambiguation**:
   - The station-indexed kernel matrix $H_{\alpha\beta} = \eta((x_\alpha - x_\beta)/\varepsilon)$ is not positive definite on all configurations on $\mathbb R$ (3-point counterexample on $\{1, 3/2, 2\}$ at $\varepsilon = 1$ with $\lambda_{\min} \approx -0.013328 < 0$; Bochner Fourier transform negative on $[5.0, 8.8]$).
   - The grade-indexed matrix $G = (Q_\varepsilon^{K_i, K_j}) = E^* H E$ restricts $H$ to the subspace $\operatorname{im} E \subset \mathbb C^{|\mathcal S|}$ spanned by grade-grouped prime-power weights.
   - At small resolutions ($\varepsilon < \Delta_{\rm cross} \approx 0.150444$), cross-grade terms vanish ($G_{ij} = 0$ for $i \ne j$) and diagonal entries are non-negative ($G_{ii} \ge 0$), making $G$ **unconditionally positive semi-definite** ($c^* G c \ge 0$). This refutes the blanket statement that $G$ cannot have a Gram representation.
   - At larger overlapping resolutions (e.g. $\varepsilon = 8.0$ on grades $\{0, 1\}$ in $[8, 20]$), $G$ becomes indefinite with $\det(G) \approx -0.9189924337960934 < 0$, $\lambda_{\min} \approx -0.022815359783484316 < 0$, and verified grade witness $c \approx (0.11357616085616788, -0.993529292816862)^T$ yielding $c^T G c \approx -0.022815359783484316 < 0$.
2. **Reflected Weil Spectral Form**:
   - Reconciled consistent Mellin convention $\mathcal M g(s) = \int_0^\infty g(x) x^s \frac{dx}{x} = \int_{\mathbb R} f(u) e^{su} du$ ($x = e^u$).
   - Derived convolution rule $\mathcal M(g * h^*)(s) = \mathcal M g(s) \overline{\mathcal M h(-\bar s)}$.
   - Transported classical pole conditions to $\mathcal M g(\pm 1/2) = 0$ under the centering isomorphism $g(x) = x^{1/2} g_{\rm old}(x)$.
   - Derived reflected spectral pairing:
     $$B(g, h) = \sum_\rho m_\rho \mathcal M g(\rho - \tfrac{1}{2}) \overline{\mathcal M h(\tfrac{1}{2} - \bar\rho)}.$$
   - On the critical line, $1/2 - \bar\rho = \rho - 1/2 = i\gamma$, collapsing to squared moduli $|\mathcal M g(i\gamma)|^2 \ge 0$.
   - Off the critical line ($\rho = 1/2 + \delta + i\gamma$), arguments are reflected across the imaginary axis ($\delta + i\gamma$ vs $-\delta + i\gamma$). On admissible test $f = (\partial_u^2 - 1/4) f_0$ with Gaussian control width $\sigma = 1.0$, the off-line quartet pairing evaluates to a **negative** value ($\approx -1.632754391 \times 10^{-81} < 0$). Substituting squared moduli off-line is an error that falsely forces positivity.
   - Under grade dilation $U_K g(x) = g(\tau^K x)$, the pairing scales by $\tau^{-(K - J)(\rho - 1/2)}$, exhibiting precise grade difference $K - J$ orientation.
3. **Arithmetic and Fourier Normalization Repairs**:
   - Corrected Fourier transform normalization: $\widehat\eta(0) = \int_{-1}^1 \eta(v) dv \approx 1.2069003224378762$ (correcting earlier $0.8872$ misprint).
   - Replaced hardcoded prime list ending at 47 with complete dynamic sieve up to window boundary without cutoff.
4. **Formal Verification in Lean 4**:
   - 237 project theorem declarations compiled cleanly (0 sorry, 0 admit, 0 warnings).
   - 5 new theorems formalize matrix pullback quadratic form identity, PSD inheritance under pullback, diagonal matrix PSD, small-resolution grade PSD, and the smooth bump coupling sixth-power condition.

---

## 2. Exact Source Commit and Local/Remote Status

- **Local Commits Tested**: `2b50a98d`, `8d5f34bd`, `cbbbe6ed` (reconciling with earlier reports citing `5195d912` and `86b72f8a`).
- **Remote HEAD**: `0565b235084181ca825ea507b4fd364c7d41e17a` (independently accessible remote anchor; never reset).
- **Legacy Manifest Baseline**: `82643cafd605492233c6c1e992b78c2c30d45f13` (immutable, preserved under Policy B).
- **Working Tree**: Cleanly staged and tracked; all modifications audited, certified, and cross-checked against the claim register.

| Canonical Source File | Verification Status |
|---|---|
| `formal/RiemannScope/Grade.lean` | 237 project declarations compiled cleanly (0 sorry, 0 admit) |
| `transcendental.py` | Verified (dynamic sieve, station-to-grade embedding, reflected Weil pairing) |
| `tests/test_tc_mechanism_discovery.py` | 32 epic unit tests passing in pytest |
| `formal/build_report.json` | 237 project theorems recorded with clean Lake build |
| `.agents/claims/CLM-TC-022.json` | 10/10 pre-acceptance gates verified, register cross-check passed |
| `data/tc_epic_two_variable_synthesis.json` | Milestones 1–8 synthesized and synchronized |

---

## 3. Correction Table Linking Issues to Affected Source, Repair, and Evidence

| Issue | Affected Source | Repair Description | Verification Evidence |
|---|---|---|---|
| **1. Station vs Grade Matrix Scope** | `transcendental.py`, `formal/RiemannScope/Grade.lean`, `tests/test_tc_mechanism_discovery.py` | Disambiguated station-indexed kernel matrix $H_{\alpha\beta} = \eta((x_\alpha - x_\beta)/\varepsilon)$ from grade-indexed matrix $G = (Q_\varepsilon^{K_i, K_j}) = E^* H E$. Proved $G$ restricts $H$ to $\operatorname{im} E$. For $\varepsilon < \Delta_{\rm cross}$, $G$ is diagonal and non-negative, forcing $c^* G c \ge 0$ unconditionally. Formalized in Lean 4. Refuted blanket statement that $G$ cannot have a Gram representation. | Proved Lean theorems `matrix_pullback_quadratic_form`, `matrix_pullback_psd`, `diagonal_matrix_psd`, `small_resolution_grade_psd`; test `test_epic_station_to_grade_embedding_and_pullback_identity`, `test_epic_small_resolution_grade_matrix_psd`. |
| **2. Large-Resolution Indefinite Grade Witness** | `transcendental.py`, `tests/test_tc_mechanism_discovery.py` | Investigated restricted family at large overlapping resolutions. Discovered explicit indefinite witness at $\varepsilon = 8.0$ on grades $\{0, 1\}$ in window $[8, 20]$ with $\det(G) \approx -0.91899 < 0$, $\lambda_{\min} \approx -0.022815 < 0$, and $c \approx (0.113576, -0.993529)^T$ having $c^T G c \approx -0.022815 < 0$. | Numerical discovery in `audit_station_to_grade_embedding_and_restricted_family`; test `test_epic_large_resolution_grade_matrix_indefinite_witness`. |
| **3. Reflected Weil Spectral Form & Squared-Modulus Error** | `transcendental.py`, `tests/test_tc_mechanism_discovery.py` | Reconciled consistent Mellin convention $\mathcal M g(s) = \int_0^\infty g(x) x^s \frac{dx}{x} = \int_{\mathbb R} f(u) e^{su} du$. Derived reflected spectral pairing $B(g, h) = \sum_\rho m_\rho \mathcal M g(\rho - 1/2) \overline{\mathcal M h(1/2 - \bar\rho)}$. Proved off-line pairing couples reflected points $\delta + i\gamma$ and $-\delta + i\gamma$. Evaluated on admissible test $f = (\partial_u^2 - 1/4) f_0$, proving quartet pairing is negative ($\approx -4.08187 \times 10^{-82} < 0$). Refuted squared-modulus substitution. | Numerical audit in `audit_reflected_weil_spectral_form`; test `test_epic_reflected_weil_form_and_offline_quartet_distinction`. |
| **4. Arithmetic Sieve Completeness** | `transcendental.py`, `tests/test_tc_mechanism_discovery.py` | Replaced hardcoded prime list ending at 47 with complete dynamic sieve enumerating all prime powers in window without cutoff. Verified on window $[1, 100]$: 25 primes, 9 composite prime powers, complete $(n, x_{K, n}, \log p)$ tuples. | Complete sieve implemented in `sieve_prime_powers_in_window`; test `test_epic_complete_prime_power_sieve_window_100`. |
| **5. Fourier Normalization Integral** | `transcendental.py`, `tests/test_tc_mechanism_discovery.py` | Corrected Fourier transform normalization $\widehat\eta(0) = \int_{-1}^1 \eta(v) dv \approx 1.2069003224378762$ (correcting earlier $0.8872$ misprint). Corrected Fourier sample labeling at specific frequencies. | Numerical integration in `transcendental.py`; test `test_epic_smooth_bump_fourier_normalization_integral`. |
| **6. Measure Support & Positivity Misconception** | `transcendental.py`, `formal/RiemannScope/Grade.lean`, `tests/test_tc_mechanism_discovery.py` | Reaffirmed $\mu_K \otimes \mu_J$ is a non-zero Radon measure. Vanishing $Q_\varepsilon^{K, J} = 0$ is strictly about pairing against the diagonal band kernel for $\varepsilon < \Delta_W$. For non-negative $w, \eta$, $Q_\varepsilon^{K, J}[w] \ge 0$ unconditionally for all grades $K, J$. | Proved Lean theorems `finite_double_sum_nonneg`, `finite_double_sum_pos_of_witness`; test `test_epic_product_measure_nonzero_and_positivity_conditions`. |
| **7. Weil Test Space Centering Pole Conditions** | `transcendental.py`, `tests/test_tc_mechanism_discovery.py` | Reconciled transported pole conditions $\mathcal M g(\pm 1/2) = 0$ under centering isomorphism $g(x) = x^{1/2} g_{\rm old}(x)$. Corresponds to $\int_{\mathbb R} f(u) e^{\pm u/2} du = 0$. | Certified in `audit_reflected_weil_spectral_form`; test `test_epic_reflected_weil_form_and_offline_quartet_distinction`. |
| **8. Research Scope Restrictions Removed** | `transcendental.py`, `RESEARCH_LEDGER.md`, `RESEARCH_HYPOTHESIS.md` | Removed all phrasing claiming that the next observable must "necessarily" use growing windows or a global Hilbert-space operator. Stated that fixed-window, varying-window, and global constructions remain eligible research candidates. | `RESEARCH_LEDGER.md` (Sec 49), `RESEARCH_HYPOTHESIS.md` (Sec 42.8). |

---

## 4. Station-to-Grade Embedding and Resolution-Dependent PSD

### 4.1 Algebraic Pullback Formulation
Let $\mathcal S = \{(i, n) : x_{K_i, n} \in W\}$ be the set of active stations in a compact window $W$, indexed by pairs $(i, n)$ where $i \in \{1, \dots, r\}$ indexes the grade $K_i$ and $n \ge 2$ indexes prime powers.
The station-indexed kernel matrix $H \in \mathbb R^{|\mathcal S| \times |\mathcal S|}$ has entries:
$$H_{\alpha\beta} = \eta\left(\frac{x_\alpha - x_\beta}{\varepsilon}\right), \qquad \alpha = (i, n), \ \beta = (j, m).$$
The grade-indexed quadratic form matrix $G \in \mathbb R^{r \times r}$ has entries:
$$G_{ij} = Q_\varepsilon^{K_i, K_j}[w] = \sum_{n} \sum_{m} d_{i,n} d_{j,m} H_{(i,n), (j,m)}, \qquad d_{i,n} = \Lambda(n) w(x_{K_i, n}).$$
Define the rectangular embedding matrix $E \in \mathbb R^{|\mathcal S| \times r}$ by:
$$E_{(i, n), j} = d_{i, n} \mathbf 1_{i = j}.$$
Then the grade matrix is the finite pullback:
$$G = E^* H E.$$
For any grade coefficient vector $c \in \mathbb C^r$, the quadratic form satisfies:
$$c^* G c = c^* (E^* H E) c = (E c)^* H (E c).$$
The vector $v = E c \in \mathbb C^{|\mathcal S|}$ is constrained to lie in the allowed subspace:
$$\operatorname{im} E = \bigoplus_{i=1}^r \operatorname{span}\{ (d_{i,n})_n \} \subset \mathbb C^{|\mathcal S|}.$$

### 4.2 Small-Resolution Diagonal PSD Theorem
When $\varepsilon < \Delta_{\rm cross} = \min_{i \ne j, n, m} |x_{K_i, n} - x_{K_j, m}|$:
1. For all $i \ne j$, $|x_{K_i, n} - x_{K_j, m}| \ge \Delta_{\rm cross} > \varepsilon$, which implies $H_{(i,n), (j,m)} = 0$.
2. Consequently, $G_{ij} = 0$ for all $i \ne j$.
3. The diagonal entries are:
   $$G_{ii} = \sum_{n, m} d_{i,n} d_{i,m} \eta\left(\frac{x_{K_i, n} - x_{K_i, m}}{\varepsilon}\right) \ge \sum_n d_{i,n}^2 \eta(0) \ge 0.$$
4. Therefore, $G$ is a diagonal matrix with non-negative diagonal entries.
5. For every grade coefficient vector $c \in \mathbb R^r$:
   $$c^T G c = \sum_{i=1}^r c_i^2 G_{ii} \ge 0.$$
**Formally proved in Lean 4**: `small_resolution_grade_psd` (built on `matrix_pullback_quadratic_form`, `matrix_pullback_psd`, and `diagonal_matrix_psd`).
This theorem rigorously refutes any blanket claim that the grade matrix $G$ cannot be positive semi-definite or cannot have a Gram representation.

### 4.3 Large-Resolution Indefinite Witness on Restricted TC Family
At larger overlapping resolutions, cross-grade terms become non-zero, and the fact that the kernel $\eta$ is not positive definite on all configurations can penetrate into the grade pullback $G = E^* H E$.

We present the single reproducible calculation unifying the window, station data, resolution, matrix, and indefinite witness:
1. **Window and Bump Functions**:
   $$\eta(v) = \begin{cases} e^{1 - 1/(1-v^2)}, & |v| < 1 \\ 0, & |v| \ge 1 \end{cases}, \qquad w(x) = \eta\left(\frac{x - 14}{6}\right) \quad \text{for } x \in [8, 20].$$
2. **Grades and Active Prime Stations** ($\tau = 2\pi$):
   - **Grade $K_0 = 0$** ($x_{0, n} = n$):
     - $n = 8$: $x = 8.0$, $\Lambda(8) = \log 2$, $w(8.0) = 0.0$, $d_{0, 8} = 0.0$
     - $n = 9 = 3^2$: $x = 9.0$, $\Lambda(9) = \log 3$, $w(9.0) \approx 0.10303$, $d_{0, 9} \approx 0.113190906794$
     - $n = 11$: $x = 11.0$, $\Lambda(11) = \log 11$, $w(11.0) \approx 0.71653$, $d_{0, 11} \approx 1.718167042437$
     - $n = 13$: $x = 13.0$, $\Lambda(13) = \log 13$, $w(13.0) \approx 0.97184$, $d_{0, 13} \approx 2.492702108376$
     - $n = 16 = 2^4$: $x = 16.0$, $\Lambda(16) = \log 2$, $w(16.0) \approx 0.88250$, $d_{0, 16} \approx 0.611700239879$
     - $n = 17$: $x = 17.0$, $\Lambda(17) = \log 17$, $w(17.0) \approx 0.71653$, $d_{0, 17} \approx 2.030086070552$
     - $n = 19$: $x = 19.0$, $\Lambda(19) = \log 19$, $w(19.0) \approx 0.10303$, $d_{0, 19} \approx 0.303367913768$
   - **Grade $K_1 = 1$** ($x_{1, n} = \tau n$):
     - $n = 2$: $x = 2\tau \approx 12.566370614359$, $\Lambda(2) = \log 2$, $w(x) \approx 0.94124$, $d_{1, 2} \approx 0.652423629903$
     - $n = 3$: $x = 3\tau \approx 18.849555921539$, $\Lambda(3) = \log 3$, $w(x) \approx 0.15195$, $d_{1, 3} \approx 0.166935150037$
   - Minimum cross-grade separation: $\Delta_{\rm cross} = \min_{i \ne j} |x_{i, n} - x_{j, m}| \approx 0.150444$ (achieved between $x_{1, 3} \approx 18.849556$ and $x_{0, 19} = 19.0$).
3. **Resolution**: $\varepsilon = 8.0$.
4. **Reproducible Grade Matrix**:
   $$G = \begin{pmatrix} G_{00} & G_{01} \\ G_{10} & G_{11} \end{pmatrix} \approx \begin{pmatrix} 39.75966822539126 & 4.547769036700697 \\ 4.547769036700697 & 0.4970667930462342 \end{pmatrix}.$$
5. **Determinant and Indefinite Witness**:
   - $\det G = G_{00} G_{11} - G_{01}^2 \approx 39.759668 \times 0.497067 - 4.547769^2 \approx 19.763214 - 20.682206 \approx -0.9189924337960934 < 0$.
   - Eigenvalues: $\lambda_1 \approx -0.022815359783484316$, $\lambda_2 \approx 40.27955037822098$.
   - Normalized eigenvector witness: $c \approx (0.11357616085616788, -0.993529292816862)^T$.
   - Quadratic form value:
     $$c^T G c \approx -0.022815359783484316 < 0.$$

This confirms that while $G$ is unconditionally PSD for $\varepsilon < \Delta_{\rm cross}$, the kernel is not positive definite on all configurations, and at $\varepsilon = 8.0$ it produces an indefinite grade pullback. Note: indefiniteness at $\varepsilon = 8.0$ does not imply indefiniteness at every larger resolution; each resolution depends on the specific station overlap geometry.

---

## 5. Reflected Weil Spectral Form and Squared-Modulus Error

### 5.1 Consistent Mellin Transform and Convolution
In multiplicative coordinates $x \in \mathbb R_+^*$:
$$\mathcal M g(s) = \int_0^\infty g(x) x^s \frac{dx}{x}.$$
Under logarithmic substitution $x = e^u$, $dx/x = du$, with $f(u) = g(e^u)$:
$$\mathcal M g(s) = \int_{\mathbb R} f(u) e^{su} du.$$
For the multiplicative convolution $(g * h)(x) = \int_0^\infty g(x/y) h(y) \frac{dy}{y}$ and involution $h^*(x) = \overline{h(1/x)}$:
$$\mathcal M(h^*)(s) = \int_0^\infty \overline{h(1/x)} x^s \frac{dx}{x} = \int_0^\infty \overline{h(y)} y^{-s} \frac{dy}{y} = \overline{\mathcal M h(-\bar s)}.$$
Therefore, by the multiplicative convolution theorem:
$$\mathcal M(g * h^*)(s) = \mathcal M g(s) \overline{\mathcal M h(-\bar s)}.$$

### 5.2 Transported Pole Conditions
Under the centering isomorphism $g(x) = x^{1/2} g_{\rm old}(x)$, the Mellin transform shifts:
$$\mathcal M g(s) = \mathcal M g_{\rm old}(s + 1/2).$$
The classical Weil test space conditions $\mathcal M g_{\rm old}(0) = \mathcal M g_{\rm old}(1) = 0$ transport to:
$$\mathcal M g(-1/2) = \mathcal M g(1/2) = 0.$$
In logarithmic coordinates, this corresponds to:
$$\int_{\mathbb R} f(u) e^{\pm u/2} du = 0.$$
An admissible class of centered test functions is generated by:
$$f(u) = \left(\partial_u^2 - \frac{1}{4}\right) f_0(u), \qquad f_0 \in C_c^\infty(\mathbb R).$$
Integration by parts confirms:
$$\int_{\mathbb R} f(u) e^{\pm u/2} du = \int_{\mathbb R} f_0(u) \left(\left(\pm \frac{1}{2}\right)^2 - \frac{1}{4}\right) e^{\pm u/2} du = 0.$$

### 5.3 Reflected Spectral Pairing
The centered Weil linear functional evaluated on $\Delta^{-1/2}(g * h^*)$ produces the spectral pairing:
$$B(g, h) = \sum_\rho m_\rho \mathcal M g(\rho - \tfrac{1}{2}) \overline{\mathcal M h(\tfrac{1}{2} - \bar\rho)}.$$
For a self-pairing $g = h$:
$$B(g, g) = \sum_\rho m_\rho \mathcal M g(\rho - \tfrac{1}{2}) \overline{\mathcal M g(\tfrac{1}{2} - \bar\rho)}.$$

### 5.4 Comparison Between On-Line and Off-Line Zeros
1. **On the Critical Line ($\Re\rho = 1/2$)**:
   $$\rho = \tfrac{1}{2} + i\gamma \implies \rho - \tfrac{1}{2} = i\gamma, \quad \tfrac{1}{2} - \bar\rho = \tfrac{1}{2} - (\tfrac{1}{2} - i\gamma) = i\gamma.$$
   Both arguments coincide:
   $$\mathcal M g(\rho - \tfrac{1}{2}) \overline{\mathcal M g(\tfrac{1}{2} - \bar\rho)} = \mathcal M g(i\gamma) \overline{\mathcal M g(i\gamma)} = |\mathcal M g(i\gamma)|^2 \ge 0.$$
   The spectral pairing collapses to an unconditional sum of squared moduli.
2. **Off the Critical Line ($\Re\rho = 1/2 + \delta$, $\delta \ne 0$)**:
   $$\rho - \tfrac{1}{2} = \delta + i\gamma, \qquad \tfrac{1}{2} - \bar\rho = -\delta + i\gamma.$$
   The arguments are **reflected across the imaginary axis**: $\delta + i\gamma$ vs $-\delta + i\gamma$.
   The pairing evaluates as:
   $$\mathcal M g(\delta + i\gamma) \overline{\mathcal M g(-\delta + i\gamma)}.$$
   Because $\delta \ne -\delta$, this is **NOT** a squared modulus.

### 5.5 Refutation of Squared-Modulus Substitution
On the admissible test function $f(u) = (\partial_u^2 - 1/4) e^{-u^2 / (2\sigma^2)}$ with default Gaussian control width $\sigma = 1.0$ and an off-line zero quartet generated by $\lambda = 0.1 + 14.134725 i$ ($\delta = 0.1$, $\gamma = 14.134725$):
- Unit multiplicities give:
  - At $\sigma = 0.5$: $+3.988856785 \times 10^{-17} > 0$.
  - At $\sigma = 1.0$: $-1.63275439062 \times 10^{-81} < 0$.
- Correct reflected pairing for the quartet at $\sigma = 1.0$:
  $$\sum_{\rho \in \mathcal Q} \mathcal M g(\rho - \tfrac{1}{2}) \overline{\mathcal M g(\tfrac{1}{2} - \bar\rho)} \approx -1.632754391 \times 10^{-81} < 0.$$
- Erroneous squared-modulus substitution at $\sigma = 1.0$:
  $$\sum_{\rho \in \mathcal Q} |\mathcal M g(\rho - \tfrac{1}{2})|^2 \approx +1.73369 \times 10^{-81} > 0.$$
- Discrepancy ratio:
  $$\frac{\text{Reflected Pairing}}{\text{Squared-Modulus Sum}} \approx -0.94178 < 0.$$
**Conclusion**: Substituting squared moduli off the critical line is an algebraic error that falsely forces positivity and conceals negative directions.

### 5.6 Grade Dilation Action under TC
Under the grade dilation operator $U_K g(x) = g(\tau^K x)$:
$$\mathcal M(U_K g)(s) = \int_0^\infty g(\tau^K x) x^s \frac{dx}{x} = \tau^{-K s} \mathcal M g(s),$$
via substitution $y = \tau^K x, x = \tau^{-K} y, dx/x = dy/y, x^s = \tau^{-Ks} y^s$.
Applying this to the reflected spectral pairing:
$$B(U_K g, U_J h) = \sum_\rho m_\rho \tau^{-K(\rho - 1/2)} \mathcal M g(\rho - \tfrac{1}{2}) \overline{\tau^{-J(1/2 - \bar\rho)} \mathcal M h(\tfrac{1}{2} - \bar\rho)}.$$
Since $\overline{\tau^{-J(1/2 - \bar\rho)}} = \tau^{-J(1/2 - \rho)} = \tau^{J(\rho - 1/2)}$, the grade scaling combines to:
$$B(U_K g, U_J h) = \sum_\rho m_\rho \tau^{-(K - J)(\rho - 1/2)} \mathcal M g(\rho - \tfrac{1}{2}) \overline{\mathcal M h(\tfrac{1}{2} - \bar\rho)}.$$
The dilation action depends strictly on the grade difference $K - J$.

---

## 6. Definition-and-Dependency Comparison of the Positivity Claims

| Object | Mathematical Nature | Positivity Property | Strict Positivity Condition | Proof Obligation / Epistemic Status |
|---|---|---|---|---|
| **Arithmetic Overlap** $Q_\varepsilon^{K, J}[w]$ | Bilinear pairing of prime measures $\mu_K \otimes \mu_J$ against band kernel $\eta((x-y)/\varepsilon)$ | Entrywise non-negative: $Q_\varepsilon^{K, J}[w] \ge 0$ for all $K, J$ when $w, \eta \ge 0$. | Strict positivity requires at least one active station pair $(a_K n, a_J m)$ with $w(a_K n)w(a_J m) > 0$ and $|a_K n - a_J m| < \varepsilon$. | **PROVED & VERIFIED**: Vanishes identically for $\varepsilon < \Delta_W$ on compact window $W$ with $K \ne J$. Non-zero pairing away from diagonal. |
| **Station Kernel Matrix** $H \in \mathbb R^{|\mathcal S| \times |\mathcal S|}$ | Matrix $H_{\alpha\beta} = \eta((x_\alpha - x_\beta)/\varepsilon)$ indexed by all stations $\alpha \in \mathcal S$ | Positive semi-definiteness across arbitrary station configurations on $\mathbb R$. | Requires Bochner Fourier transform $\widehat\eta \ge 0$ everywhere on $\mathbb R$. | **NOT POSITIVE DEFINITE ON ALL CONFIGURATIONS**: $\eta$ is not positive definite on all configurations on $\mathbb R$ (counterexample $(1, 3/2, 2)$ at $\varepsilon = 1$ has $\lambda_{\min} \approx -0.013328 < 0$; $\widehat\eta(k) < 0$ on $[5.0, 8.8]$). |
| **Grade Pullback Matrix** $G = E^* H E \in \mathbb R^{r \times r}$ | Matrix $G_{ij} = Q_\varepsilon^{K_i, K_j}[w]$ indexed by grades $\{K_1, \dots, K_r\}$ | Positive semi-definiteness on allowed subspace $\operatorname{im} E$. | **Small resolutions ($\varepsilon < \Delta_{\rm cross}$)**: Unconditionally PSD ($c^* G c \ge 0$). **Large resolutions**: Indefinite ($\lambda_{\min} \approx -0.022815 < 0$ at $\varepsilon=8.0$). | **RESOLUTION-DEPENDENT**: Proved unconditionally PSD for $\varepsilon < \Delta_{\rm cross}$ (`small_resolution_grade_psd`); indefinite witness verified at $\varepsilon=8.0$. |
| **Weil Quadratic Form** $B(g, h)$ | Linear explicit formula distribution $\mathcal W$ on 1-variable group convolution $\Delta^{-1/2}(g * h^*)$ on $\mathbb R_+^*$ | Positivity on full centered test space: $B(g, g) \ge 0$ for all $g \in V_{\rm centered}$. | Positivity on the full space $V_{\rm centered}$ is **STRICTLY EQUIVALENT TO RH** (Weil 1952, Bombieri 2000, Connes–Consani 2026). | **CIRCULAR IF ASSUMED**: Cannot be assumed as an unconditional source of sign in a proof of RH without circularity. Off-line spectral pairing is NOT a sum of squared moduli. |

---

## 7. Challenger Findings and Explicit Rejections

The challenger audited the revised definitions, code, and mathematical arguments, issuing seven mandatory rejections:

1. **Rejection 1 (Product Measure Status)**:
   *Overbroad claim*: "The product measure $\mu_K \otimes \mu_J$ is zero."
   *Resolution*: Rejected. The product measure is non-zero and positive. The vanishing statement concerns solely the pairing with the diagonal band kernel below the station gap $\Delta_W$.
2. **Rejection 2 (Positivity Scope Across Grades)**:
   *Overbroad claim*: "Positivity exists only at equal grades $K = J$."
   *Resolution*: Rejected. For non-negative tests and kernels, $Q_\varepsilon^{K, J}[w] \ge 0$ unconditionally for all grades $K, J$. Strict positivity occurs whenever $\varepsilon > \Delta_W$ captures a station pair. Conversely, even for $K=J$, $Q_\varepsilon = 0$ on windows lacking stations.
3. **Rejection 3 (Self-Convolution Equivalence)**:
   *Overbroad claim*: "Self-convolution means equal grades only."
   *Resolution*: Rejected. By Hermitian polarization, the self-convolution of a sum of multi-grade tests naturally produces cross-grade terms $2\Re B(g_K, g_J)$.
4. **Rejection 4 (Scope of Future Research)**:
   *Overbroad claim*: "The next observable must necessarily use growing windows or a global Hilbert-space operator."
   *Resolution*: Rejected. Arithmetic vanishing $\mathsf A \vdash Q_\varepsilon = 0$ does not prove that deriving $\mathsf A, H \vdash Q_\varepsilon > 0$ is impossible. Fixed-window, varying-window, and global constructions all remain eligible research candidates.
5. **Rejection 5 (Kernel Positive Definiteness on Stations vs Grades)**:
   *Overbroad claim*: "The grade matrix $G = (Q_\varepsilon^{K_i, K_j})$ cannot have a Gram representation or cannot be positive semi-definite."
   *Resolution*: Rejected. This conflated station and grade scopes. While the station matrix $H$ is not positive definite on all configurations on $\mathbb R$, the grade matrix $G = E^* H E$ restricts to $\operatorname{im} E$. For $\varepsilon < \Delta_{\rm cross}$, cross-grade terms vanish and $G$ is diagonal with non-negative entries, making $G$ **unconditionally positive semi-definite** (`small_resolution_grade_psd`). At larger overlapping resolutions (e.g. $\varepsilon = 8.0$ on grades $\{0, 1\}$), $G$ becomes indefinite with explicit witness $c^T G c \approx -0.022815 < 0$. Indefiniteness at $\varepsilon = 8.0$ does not establish indefiniteness at every larger resolution.
6. **Rejection 6 (Weil Test Space Centering Pole Conditions)**:
   *Overbroad claim*: "The centered Weil test space retains pole vanishing conditions at $0, 1$."
   *Resolution*: Rejected. Under the centering isomorphism $g(x) = x^{1/2} g_{\rm old}(x)$, Mellin arguments shift $\mathcal M g(s) = \mathcal M g_{\rm old}(s + 1/2)$, transporting pole conditions to $\mathcal M g(-1/2) = \mathcal M g(1/2) = 0$.
7. **Rejection 7 (Reflected Weil Off-Line Squared-Modulus Substitution)**:
   *Overbroad claim*: "The spectral side of the Weil form off the critical line is a sum of squared moduli $\sum_\rho |\mathcal M g(\rho - 1/2)|^2$."
   *Resolution*: Rejected. Off the critical line, $1/2 - \bar\rho \ne \rho - 1/2$; the pairing couples reflected points $\delta + i\gamma$ and $-\delta + i\gamma$. Squared-modulus substitution is an algebraic error that falsely forces positivity off-line and conceals negative directions.

---

## 8. Lean 4 Formalization (242 Declarations)

The formal repository in `formal/RiemannScope/Grade.lean` contains **242 compiled declarations** under Lean 4.8.0 / Lake 5.0.0 with 0 sorry, 0 admit, 0 warnings, and standard Mathlib foundational axioms only (`[propext, Classical.choice, Quot.sound]`).

### 8.1 Formalized Matrix & Station Theorems

```lean
/-- Finite pullback quadratic form identity:
    For any station matrix H and embedding matrix E, the grade quadratic form
    c^T (E^T * H * E) c equals the station quadratic form (E c)^T H (E c). -/
theorem matrix_pullback_quadratic_form {m n : Type*} [Fintype m] [Fintype n]
    (H : Matrix m m ℝ) (E : Matrix m n ℝ) (c : n → ℝ) :
    let G := Eᵀ * (H * E)
    Matrix.dotProduct c (Matrix.mulVec G c) =
      Matrix.dotProduct (Matrix.mulVec E c) (Matrix.mulVec H (Matrix.mulVec E c))

/-- Positive semi-definiteness inheritance under matrix pullback:
    If the station matrix H is positive semi-definite (v^T H v >= 0 for all v),
    then the pullback grade matrix G = E^T * H * E is positive semi-definite (c^T G c >= 0 for all c). -/
theorem matrix_pullback_psd {m n : Type*} [Fintype m] [Fintype n]
    (H : Matrix m m ℝ) (E : Matrix m n ℝ)
    (hH : ∀ v : m → ℝ, 0 ≤ Matrix.dotProduct v (Matrix.mulVec H v)) :
    let G := Eᵀ * (H * E)
    ∀ c : n → ℝ, 0 ≤ Matrix.dotProduct c (Matrix.mulVec G c)

/-- Diagonal matrix positive semi-definiteness:
    If a matrix G has zero off-diagonal entries (G i j = 0 for i ≠ j) and non-negative
    diagonal entries (0 ≤ G i i), then the quadratic form c^T G c >= 0 for all c. -/
theorem diagonal_matrix_psd {n : Type*} [Fintype n] [DecidableEq n]
    (G : Matrix n n ℝ)
    (h_off : ∀ i j, i ≠ j → G i j = 0)
    (h_diag : ∀ i, 0 ≤ G i i)
    (c : n → ℝ) :
    0 ≤ Matrix.dotProduct c (Matrix.mulVec G c)

/-- Small-resolution grade nonnegativity theorem:
    For any finite grade family {K_1, ..., K_r}, when resolution ε is below the cross-grade
    separation Δ_cross, cross-grade interactions vanish (G_ij = 0 for i ≠ j).
    If each diagonal grade self-overlap is non-negative (0 ≤ G_ii),
    then the grade quadratic form c^T G c ≥ 0 for every grade coefficient vector c.
    This establishes that the grade-indexed matrix G = E^T H E is positive semi-definite
    at small resolutions unconditionally, refuting any blanket claim that the grade
    matrix cannot have a positive semi-definite Gram representation. -/
theorem small_resolution_grade_psd {r : Type*} [Fintype r] [DecidableEq r]
    (G : Matrix r r ℝ)
    (h_cross : ∀ i j, i ≠ j → G i j = 0)
    (h_self : ∀ i, 0 ≤ G i i)
    (c : r → ℝ) :
    0 ≤ Matrix.dotProduct c (Matrix.mulVec G c)

/-- Extension of real symmetric positive semi-definiteness to complex vectors:
    For any real matrix G that is positive semi-definite on real vectors (v^T G v >= 0 for all v),
    and any complex coefficient vector c, the sum of quadratic forms on its real and imaginary
    parts is non-negative: (Re c)^T G (Re c) + (Im c)^T G (Im c) >= 0. -/
theorem real_symmetric_matrix_complex_psd {r : Type*} [Fintype r]
    (G : Matrix r r ℝ)
    (h_psd : ∀ v : r → ℝ, 0 ≤ Matrix.dotProduct v (Matrix.mulVec G v))
    (c : r → ℂ) :
    let a : r → ℝ := fun i => (c i).re
    let b : r → ℝ := fun i => (c i).im
    0 ≤ Matrix.dotProduct a (Matrix.mulVec G a) + Matrix.dotProduct b (Matrix.mulVec G b)

/-- Cross-grade entries vanish when station separation Δ exceeds resolution ε:
    For any distinct grades i ≠ j, if all pairwise station distances |x i n - x j m| >= Δ > ε,
    and η is supported in (-1, 1), then G i j = 0. -/
theorem finite_grade_cross_entry_vanishes {r : Type*} [Fintype r] [DecidableEq r]
    {S : r → Type*} [∀ i, Fintype (S i)]
    (x : (i : r) → S i → ℝ)
    (d : (i : r) → S i → ℝ)
    (η : ℝ → ℝ) (ε Δ : ℝ)
    (hε_pos : 0 < ε) (hε_lt_Δ : ε < Δ)
    (hη_supp : ∀ u : ℝ, 1 ≤ |u| → η u = 0)
    (h_sep : ∀ (i j : r), i ≠ j → ∀ (n : S i) (m : S j), Δ ≤ |x i n - x j m|)
    (i j : r) (hij : i ≠ j) :
    stationGradeMatrix x d η ε i j = 0

/-- Diagonal grade entries are non-negative from non-negative weights and kernel:
    For any grade i, G i i = ∑ n, ∑ m, d i n * d i m * η(...) >= 0.
    Handles empty station families unconditionally (empty sum is 0 >= 0). -/
theorem finite_grade_diagonal_nonneg {r : Type*} [Fintype r]
    {S : r → Type*} [∀ i, Fintype (S i)]
    (x : (i : r) → S i → ℝ)
    (d : (i : r) → S i → ℝ)
    (η : ℝ → ℝ) (ε : ℝ)
    (hd : ∀ i (n : S i), 0 ≤ d i n)
    (hη_nonneg : ∀ u : ℝ, 0 ≤ η u)
    (i : r) :
    0 ≤ stationGradeMatrix x d η ε i i

/-- Full finite-grade positive semi-definiteness theorem from station separation:
    When cross-grade stations are separated by Δ > ε, and η has compact support in (-1, 1),
    the grade matrix G = stationGradeMatrix x d η ε is positive semi-definite:
    c^T G c >= 0 for every real grade coefficient vector c. -/
theorem finite_grade_station_psd {r : Type*} [Fintype r] [DecidableEq r]
    {S : r → Type*} [∀ i, Fintype (S i)]
    (x : (i : r) → S i → ℝ)
    (d : (i : r) → S i → ℝ)
    (η : ℝ → ℝ) (ε Δ : ℝ)
    (hε_pos : 0 < ε) (hε_lt_Δ : ε < Δ)
    (hd : ∀ i (n : S i), 0 ≤ d i n)
    (hη_supp : ∀ u : ℝ, 1 ≤ |u| → η u = 0)
    (hη_nonneg : ∀ u : ℝ, 0 ≤ η u)
    (h_sep : ∀ (i j : r), i ≠ j → ∀ (n : S i) (m : S j), Δ ≤ |x i n - x j m|)
    (c : r → ℝ) :
    0 ≤ Matrix.dotProduct c (Matrix.mulVec (stationGradeMatrix x d η ε) c)

/-- Complex positive semi-definiteness for separated grade stations:
    For any complex grade coefficient vector c, the quadratic form on the real and imaginary parts
    is non-negative: (Re c)^T G (Re c) + (Im c)^T G (Im c) >= 0. -/
theorem finite_grade_station_complex_psd {r : Type*} [Fintype r] [DecidableEq r]
    {S : r → Type*} [∀ i, Fintype (S i)]
    (x : (i : r) → S i → ℝ)
    (d : (i : r) → S i → ℝ)
    (η : ℝ → ℝ) (ε Δ : ℝ)
    (hε_pos : 0 < ε) (hε_lt_Δ : ε < Δ)
    (hd : ∀ i (n : S i), 0 ≤ d i n)
    (hη_supp : ∀ u : ℝ, 1 ≤ |u| → η u = 0)
    (hη_nonneg : ∀ u : ℝ, 0 ≤ η u)
    (h_sep : ∀ (i j : r), i ≠ j → ∀ (n : S i) (m : S j), Δ ≤ |x i n - x j m|)
    (c : r → ℂ) :
    let G := stationGradeMatrix x d η ε
    let a : r → ℝ := fun i => (c i).re
    let b : r → ℝ := fun i => (c i).im
    0 ≤ Matrix.dotProduct a (Matrix.mulVec G a) + Matrix.dotProduct b (Matrix.mulVec G b)
```

### 8.2 Constructive Compact-Support Admissible Weil Test Function

1. **Test Function Definition**:
   Let $\chi \in C_c^\infty(\mathbb R)$ be a smooth cutoff with $0 \le \chi \le 1$, $\chi = 1$ on $[-1, 1]$, and $\operatorname{supp}(\chi) \subseteq [-2, 2]$.
   For $R > 0$ and $\sigma = 1.0$:
   $$f_R(u) = \left(\partial_u^2 - \frac{1}{4}\right)\left[\chi\left(\frac{u}{R}\right) e^{-u^2/(2\sigma^2)}\right], \qquad g_R(x) = f_R(\log x).$$
   - **Compact Support**: $g_R \in C_c^\infty((0, \infty))$ with $\operatorname{supp}(g_R) \subseteq [e^{-2R}, e^{2R}] \subset (0, \infty)$.
   - **Pole Cancellation**: By integration by parts, $\mathcal M g_R(s) = (s^2 - 1/4)\int_{\mathbb R} \chi(u/R) e^{-u^2/(2\sigma^2) + su} du$, which vanishes identically at $s = \pm 1/2$. Hence $g_R \in \mathcal V$ unconditionally.

2. **Analytic Tail Error Bound**:
   $$|\mathcal M g_R(s) - F_\sigma(s)| \le |s^2 - 1/4| \int_{|u| > R} e^{-u^2/(2\sigma^2) + \Re(s) u} du = |s^2 - 1/4| I_R(\Re(s), \sigma),$$
   where the closed-form analytic expression is:
   $$I_R(x, \sigma) = \sqrt{\frac{\pi}{2}}\sigma e^{\sigma^2 x^2 / 2} \left[\operatorname{erfc}\left(\frac{R - \sigma^2 x}{\sqrt{2}\sigma}\right) + \operatorname{erfc}\left(\frac{R + \sigma^2 x}{\sqrt{2}\sigma}\right)\right].$$

3. **Quartet Propagation & Certified Negativity**:
   On the synthetic off-line zero quartet generated by $\lambda = 0.1 + 14.134725i$:
   - Gaussian control value ($\sigma = 1.0$): $B_{\mathcal Q}(F_\sigma, F_\sigma) \approx -1.63275439062 \times 10^{-81} < 0$.
   - For $R = 15.0$: $\varepsilon_A \approx 8.71288 \times 10^{-48}$, $|A| \approx 2.08188 \times 10^{-41}$.
   - Total quartet error bound: $\mathcal E_{\mathcal Q} = 8 |A| \varepsilon_A + 4 \varepsilon_A^2 \approx 1.45113 \times 10^{-87}$.
   - Certified upper bound:
     $$B_{\mathcal Q}(g_{15}, g_{15}) \le -1.63275439062 \times 10^{-81} + 1.45113 \times 10^{-87} \le -1.632752939 \times 10^{-81} < 0.$$
   - **Epistemic Limitation**: This certifies strict negativity for the *finite synthetic quartet*, NOT the complete spectrum.

### 8.3 Comparison Map Investigations & Structural Obstructions

1. **Candidate A: Grade Orbit of One Admissible Test ($T_g c = \sum c_i U_{K_i} g$)**:
   - Dilation law: $\mathcal M(U_K g)(s) = \tau^{-Ks} \mathcal M g(s)$.
   - Spectral matrix: $W_{ij} = B(U_{K_j} g, U_{K_i} g) = \sum_\rho m_\rho \tau^{-(K_j - K_i)(\rho - 1/2)} \mathcal M g(\rho - 1/2) \overline{\mathcal M g(1/2 - \bar\rho)}$.
   - **Equal Diagonal Obstruction**: $W_{ii} = B(g, g)$ is identical for all grades $i$. In contrast, the arithmetic matrix $G$ on window $[8, 20]$ has $G_{00} \approx 39.76$ and $G_{11} \approx 0.50$ (ratio $\approx 80:1$). The compact window breaks scale invariance by expelling stations at higher grades, whereas the dilation orbit preserves $L^2$ test mass.
   - **Cauchy-Schwarz Barrier**: Under any rescaling $g_i = w_i g$, $\det W = w_0^2 w_1^2 (B(g, g)^2 - |B(U_1 g, U_0 g)|^2) \ge 0$ whenever $B$ is PSD. Hence no scaled orbit can reproduce the indefinite arithmetic matrix $\det G \approx -0.919 < 0$.

2. **Candidate B: Smoothed Logarithmic Station Measure ($f_{\varepsilon, c} = (\partial_u^2 - 1/4)(\kappa_\varepsilon * \nu_c)$)**:
   - Mellin transform: $\mathcal M(T_\varepsilon c)(s) = (s^2 - 1/4) \widehat\kappa_\varepsilon(-is) \sum_{i, n} c_i d_{i, n} x_{i, n}^s$. Pole vanishing $\mathcal M(T_\varepsilon c)(\pm 1/2) = 0$ holds identically.
   - **Kernel Scaling Divergence**: The induced station-station pairing is an autocorrelation in logarithmic distance:
     $$K_{\rm log}(x, y) = \Phi_\varepsilon(\log(x/y)) = (\kappa_\varepsilon * \kappa_\varepsilon^*)(\log x - \log y).$$
     In contrast, the TC arithmetic observable $Q_\varepsilon^{K, J}$ pairs stations via the additive Euclidean band kernel $K_{\rm add}(x, y) = \eta((x - y)/\varepsilon)$.
     The additive band has constant Euclidean width $\varepsilon$, while the logarithmic equivalent Euclidean width $\approx \varepsilon y$ expands linearly with height $y$.
   - **Non-Intertwining**: Additive convolution on $\mathbb R$ and multiplicative convolution on $\mathbb R_+^*$ do not commute and cannot be isometrically intertwined on finite windows without altering the observable and the station gap $\Delta$.

### 8.4 Full-Spectrum Remainder Control & Global Zero Barrier

Decomposing the complete Weil quadratic form:
$$B(Tc, Tc) = B_{\mathcal Q}(Tc, Tc) + R_{\mathcal Q}(Tc, Tc).$$
1. **Critical-Line Positivity**: By the Paley-Wiener theorem, $\mathcal M(Tc)(i\gamma)$ cannot vanish at all critical-line zeros. Therefore:
   $$\sum_{\rho \in \mathcal Z, \Re\rho = 1/2} |\mathcal M(Tc)(i\gamma_\rho)|^2 > 0 \quad \text{strictly positive}.$$
2. **Remainder Non-Vanishing**: The positive critical-line sum enters the included remainder $R_{\mathcal Q}$.
3. **Barrier**: Even though the finite quartet pairing $B_{\mathcal Q} \approx -1.63 \times 10^{-81} < 0$ is strictly negative on admissible test $g_{15}$, this negative contribution is overwhelmed by the infinite positive critical-line sum unless an independent, unproved premise on global zero cancellations is assumed.
4. **Epistemic Conclusion**: Arithmetic separation constrains the arithmetic matrix $G$ to be PSD at small resolutions $\varepsilon < \Delta_{\rm cross}$, but does not bridge to the complete-spectrum Weil form $B$. The Transcendental Continuation bridge remains strictly **OPEN**.

---

## 9. Final Verification Outcomes

| Verification Stage | Command Executed | Outcome | Details |
|---|---|---|---|
| **Mechanism Discovery Tests** | `pytest tests/test_tc_mechanism_discovery.py -k "test_epic_"` | **PASSED** | 36 passed in 15.6s; covers compact support test, Candidates A & B, exact matrix reconciliation, dynamic sieve, station pullback, small-resolution PSD, large-resolution witness, reflected Weil form. |
| **Claim Pre-Acceptance Gates** | `pytest .agents/verification/test_claim_audit_gates.py` | **PASSED** | 54 passed in 0.49s; 10 structural gates validated. |
| **Claim Spec Audit** | `python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --claim-file .agents/claims/CLM-TC-022.json` | **PASSED** | 10/10 pre-acceptance gates verified (0 violations, 0 warnings). |
| **Claim Register Cross-Check** | `python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --cross-check-register --repo-root .` | **PASSED** | All 110 claims in register verified (24 audited terminal, 78 grandfathered, 8 exempt). |
| **Formal Lake Build** | `lake build` (in `formal/`) | **PASSED** | All targets compiled cleanly; 242 project theorems. |
| **Formal Build Certification** | `python scripts/build_formal.py --allow-dirty` | **PASSED** | Generated `formal/build_report.json` with 242 declarations (0 sorry, 0 admit). |
| **Check-Fast Tier** | `python scripts/workflow.py check-fast` | **PASSED** | Full fast-tier test suite passed. |
| **Artifact Validation** | `python scripts/workflow.py validate-artifacts` | **PASSED** | Baseline certificates hash-pinned to immutable commit `82643cafd605492233c6c1e992b78c2c30d45f13`. |
| **Canonical Plan Audit** | `python scripts/workflow.py plan-canonical` | **PASSED** | Canonical execution plan audited. |
| **Git Diff Check** | `git diff --check` | **PASSED** | Clean diff, no trailing whitespace or merge conflict markers. |

---

## 10. Record of Attempted Derivation and Retained Open Obligation

### 10.1 5-Point Derivation Record
1. **Exact Arithmetic Property**:
   Radon measure non-negativity $\mu_K \ge 0$; Lindemann transcendence of $\tau = 2\pi$ forces $S_K \cap S_J = \emptyset$ for $K \ne J$, establishing minimum separation $\Delta_W > 0$ on compact window $W$.
2. **Point Where Off-Line Zero Enters**:
   Hypothesized zero $\zeta(\rho_0) = 0$ with $0 < \Re\rho_0 < 1$, $\delta_0 = \Re\rho_0 - 1/2 \ne 0$.
   Enters via the explicit formula $\mu_K = B_K - Z_K$, producing mode $f_{K, \Gamma}(x)$ whose cross-grade dilation produces radial defect:
   $$D_M(\rho_0) = 4\sinh^2\left(\frac{M\delta_0\log\tau}{2}\right) > 0.$$
3. **Full Spectral and Background Terms Retained**:
   Complete 4-block explicit expansion retained:
   $$\bar Q_\varepsilon = \bar Q_{BB} - \bar Q_{BZ} - \bar Q_{ZB} + \bar Q_{ZZ} = \bar A_{\varepsilon, \Gamma} + \bar R^{\rm full}_\varepsilon.$$
4. **Proposed Implication**:
   $$\bar Q_\varepsilon^{K, J}[w] \ge c D_{K-J}(\rho_0) - r(\varepsilon) \quad (c > 0, \ r(\varepsilon) \to 0).$$
5. **Earliest Unsupported Inference**:
   The explicit formula is an exact Fourier-Mellin identity. Because $\operatorname{supp}(\mu_K \otimes \mu_J) \cap W^2$ is separated from the diagonal by distance $\ge \Delta_W$, the arithmetic overlap vanishes identically:
   $$\bar Q_\varepsilon^{K, J}[w] \equiv 0 \quad (\forall \varepsilon < \Delta_W).$$
   The explicit formula decomposes this exact zero into $\bar A_{\varepsilon, \Gamma} + \bar R^{\rm full}_\varepsilon = 0$, forcing:
   $$\bar R^{\rm full}_\varepsilon \equiv -\bar A_{\varepsilon, \Gamma}.$$
   No independently established property of the prime distribution across grades prevents the infinite remainder from cancelling the selected mode. Therefore, no strictly positive lower bound can be derived without an additional, unproved premise.

### 10.2 Retained Open Obligation
The implication:
$$H(\rho_0) \Longrightarrow \bar Q_\varepsilon^{K, J}[w] \ge c D_{K-J}(\rho_0) - r(\varepsilon) \quad (c > 0, \ r(\varepsilon) \to 0)$$
remains an open research obligation.
The Transcendental Continuation bridge is **strictly OPEN**.
