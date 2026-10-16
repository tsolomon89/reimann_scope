# TASK-TC-038 — Arithmetic Nature of Nontrivial Zeros, Exact Zero-Sum Invariants, and Special-Value Transfer Audit

**Repository**: `tsolomon89/reimann_scope`  
**Task ID**: `TASK-TC-038`  
**Branch Classification**: `ZERO_ARITHMETIC_BRANCH`  
**Starting HEAD**: `63770418ca4b4498b0c9300a854e45d52434f52b`  
**Substantive Parent**: `70c757ce6cead947fc806b2dadd78f2de0363fc6`  
**Principal Classification**: `ZERO_ARITHMETIC_FRONTIER_CLASSIFIED_INDIVIDUAL_STATUS_OPEN`  
**Secondary Transfer Classification**: `SPECIAL_VALUE_IRRATIONALITY_METHOD_NO_DIRECT_ZERO_LOCATION_TRANSFER`  
**Shifted-Ordinate Classification**: `SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE`  
**Primary TC Obligation Status**: `OBL-CT-001A = OPEN`  
**Exact Remaining Zero-Arithmetic Subgate**: `SUBGATE-TC-038A`  

---

## A. Executive Verdict

Following the completion and evidence repair of the TC bigraded character projection audit (`TASK-TC-037` / `TASK-TC-037R`), `TASK-TC-038` pivots from constructing new TC projectors to a rigorous mathematical, symbolic, primary-literature, and certified finite-interval audit of the **arithmetic nature of the nontrivial zeros of $\zeta(s)$ themselves and of canonical symmetric invariants built from them**.

1. **Principal Classification**:
   $$\boxed{\texttt{ZERO\_ARITHMETIC\_FRONTIER\_CLASSIFIED\_INDIVIDUAL\_STATUS\_OPEN}}$$
   with secondary methodological transfer verdict:
   $$\boxed{\texttt{SPECIAL\_VALUE\_IRRATIONALITY\_METHOD\_NO\_DIRECT\_ZERO\_LOCATION\_TRANSFER}}.$$
2. **Candidate-Object Equivalence (`SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE`)**:
   Because $\frac{1}{2} \in \mathbb{Q} \subset \overline{\mathbb{Q}}$ and both $\mathbb{Q}$ and $\overline{\mathbb{Q}}$ are fields closed under addition and subtraction, the shifted ordinate $\tilde{\gamma}_n := \gamma_n + \frac{1}{2}$ satisfies
   $$\gamma_n + \frac{1}{2} \in \mathbb{Q} \iff \gamma_n \in \mathbb{Q}, \qquad \gamma_n + \frac{1}{2} \in \overline{\mathbb{Q}} \iff \gamma_n \in \overline{\mathbb{Q}}, \qquad \gamma_n + \frac{1}{2} \notin \overline{\mathbb{Q}} \iff \gamma_n \notin \overline{\mathbb{Q}},$$
   with minimal-polynomial degree invariant ($\deg_{\mathbb{Q}}(\gamma_n + 1/2) = \deg_{\mathbb{Q}}(\gamma_n)$) via the explicit integer-polynomial bijection $Q(Y) = 2^d P(Y - 1/2)$. Therefore $\gamma_n + 1/2$ does **not** define a distinct arithmetic question from $\gamma_n$. By contrast, the full complex zero $\rho_n = \beta_n + i\gamma_n$ satisfies unconditionally $\rho_n \in \overline{\mathbb{Q}} \iff (\beta_n \in \overline{\mathbb{Q}} \text{ and } \gamma_n \in \overline{\mathbb{Q}})$ (using complex conjugation $\bar{\rho}_n = \beta_n - i\gamma_n$ and $i \in \overline{\mathbb{Q}}$), while $\rho_n \notin \mathbb{Q}$ unconditionally because $\zeta(s) < 0$ on $(0, 1)$ implies $\gamma_n \ne 0$.
3. **Individual Zero Arithmetic Status (`OPEN_IN_LITERATURE`)**:
   Primary-source audit of the analytic number theory and transcendence literature confirms that for every individual nontrivial zero $\rho_n = \beta_n + i\gamma_n$ ($n \ge 1$):
   - $\rho_n \notin \mathbb{Q}$ is **proved unconditionally** ($\operatorname{Im}(\rho_n) = \gamma_n \ne 0$).
   - Whether $\gamma_n \notin \mathbb{Q}$ for any individual $n$ (in particular $\gamma_1 \approx 14.13472514$) is **`OPEN_IN_LITERATURE`**.
   - Whether $\rho_n \notin \overline{\mathbb{Q}}$ or $\gamma_n \notin \overline{\mathbb{Q}}$ for any individual $n$ is **`OPEN_IN_LITERATURE`**.
   - Linear independence over $\mathbb{Q}$ of the positive ordinates $\{\gamma_n\}_{n \ge 1}$ is the classical **Linear Independence Conjecture (LI)** (`CONDITIONAL_ON_NAMED_CONJECTURE`).
   - None of the nine major transcendence theorem families (Lindemann–Weierstrass, Gelfond–Schneider, Baker, Siegel–Shidlovsky, Schneider–Lang, Nesterenko, Chudnovsky, Rohrlich–Lang, Hölder–Ostrowski) applies to $\zeta(\rho_n) = 0$ inside $0 < \operatorname{Re}(s) < 1$.
4. **Exact Symmetric Zero-Sum Invariants Derived and Verified**:
   While individual zeros resist existing Diophantine methods, symmetric sums over all nontrivial zeros are **analytically closed in terms of classical constants** via the Hadamard factorization of $\xi(s) = \frac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$:
   - $S_1 = \sum_\rho^{\mathrm{sym}} \frac{1}{\rho} = 1 + \frac{\gamma_E}{2} - \log(2\sqrt{\pi}) = \lambda_1 \approx 0.0230957089661210338143102479065$,
   - $\sum_\rho \frac{1}{\rho(1-\rho)} = 2 S_1 = 2\lambda_1 = 2 + \gamma_E - \log(4\pi) \approx 0.0461914179322420676286204958130$ (converging **absolutely** without grouping because $|\rho(1-\rho)| \sim \gamma_\rho^2$),
   - $S_2 = \sum_\rho \frac{1}{\rho^2} = 1 - \frac{\pi^2}{24} + 2\zeta''(0) + \log^2(2\pi) = 1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1 \approx -0.0461543172958046027571079903791$,
   - $S_3 = 1 - \frac{7}{8}\zeta(3) + \gamma_E^3 + 3\gamma_E\gamma_1 + \frac{3}{2}\gamma_2 \approx -0.000111158231452105922762668238915$,
   - $S_4 = 1 - \frac{\pi^4}{96} + \gamma_E^4 + 4\gamma_E^2\gamma_1 + 2\gamma_1^2 + 2\gamma_E\gamma_2 + \frac{2}{3}\gamma_3 \approx +0.0000736272212616895183267713070306$,
   - Centered odd sums $\Sigma_{2m-1}^{\mathrm{sym}} = \sum_\rho^{\mathrm{sym}} (\rho - 1/2)^{-(2m-1)} = 0$ identically, and $\Sigma_2 = \sum_\rho (\rho - 1/2)^{-2} = 8 - \frac{1}{4}\psi_1(1/4) - \left.\frac{d^2}{ds^2}\log(-\zeta(s))\right|_{s=1/2} \approx -0.0462099862308379415778676208607$.
   However, the irrationality and transcendence of every one of these nonzero exact combinations ($S_1$, $2S_1$, $S_2$, $S_3$, $S_4$, $\Sigma_2$, $\lambda_n$) remain **`OPEN_IN_LITERATURE`** because the $\mathbb{Q}$-algebraic independence of $\gamma_E$, $\log(4\pi)$, and the Stieltjes constants $\gamma_k$ is unproved.
5. **Primary-Source Verification of $\zeta(5)$ (`ZETA5_CURRENT_STATUS_VERIFIED`) & Special-Value Transfer Audit**:
   - In the Archimedean setting, the individual irrationality of $\zeta(5) \in \mathbb{R}$ remains **`OPEN_IN_LITERATURE`** (verified up to May 2025 in Lai–Lupu–Sprang `arXiv:2505.23088v1`; the July 2024 `math.GM` preprint `arXiv:2407.07121` claiming Archimedean irrationality was explicitly refuted by Chen et al. in `arXiv:2411.16774v3`). What is proved in primary literature is Apéry's theorem $\zeta(3) \notin \mathbb{Q}$ (1979), the Ball–Rivoal infinite odd-zeta theorem (2000/2001), Zudilin's one-of-four theorem $\{\zeta(5),\zeta(7),\zeta(9),\zeta(11)\} \not\subset \mathbb{Q}$ (2001, `arXiv:math/0104249v1`), Rivoal–Zudilin's two-among-$\{\zeta(5),\dots,\zeta(69)\}$ (`arXiv:1803.03160v1`), Fischler–Sprang–Zudilin (`arXiv:1803.08905v2`), and the May 2025 breakthrough by Lai–Sprang–Zudilin (`arXiv:2505.05005v2`) proving the irrationality of the **2-adic** zeta value $\zeta_2(5) \notin \mathbb{Q}$.
   - Special-value irrationality methods (Apéry–Beukers integrals, Ball–Rivoal–Zudilin well-poised hypergeometric series, Brown's $\mathcal{M}_{0,n}$ period integrals, and 2-adic holonomic constructions) evaluate unknown values at **fixed positive integer weights/multiplicities $m \in \mathbb{Z}_{\ge 2}$**; replacing $m$ by a critical-strip zero $\rho$ where $\zeta(\rho) = 0$ destroys both the integer pole multiplicity in partial-fraction expansions and the linear form $A_n \zeta(m) + B_n$ (`SPECIAL_VALUE_IRRATIONALITY_METHOD_HAS_NO_DIRECT_ZERO_LOCATION_TRANSFER`).
6. **Certified 128-bit Arb Finite Exclusions**:
   - Using 128-bit outward Arb/Acb interval arithmetic, we certify `CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION` across all $158{,}062{,}321{,}920$ normalized primitive integer polynomials of degree $1 \le d \le 4$ and height $H \le 100$ for $\gamma_1$ ($\min |P(\gamma_1)| \ge 9.15045 \times 10^{-6} > 0$), $\gamma_1 + 1/2$ ($\min |P(\gamma_1 + 1/2)| \ge 1.57896 \times 10^{-5} > 0$), and $\rho_1 = 1/2 + i\gamma_1$ ($\min |P(\rho_1)| \ge 0.571818 > 0$), plus explicit polynomial-by-polynomial enumeration of all $8{,}160$ normalized primitive polynomials for $D = 4, H = 3$.
   - We certify `CERTIFIED_BOUNDED_DENOMINATOR_RATIONAL_EXCLUSION` for all rational numbers $p/q$ with $1 \le q \le 10{,}000$ ($\min_{1 \le q \le 10000} |\gamma_1 - p/q| \ge 9.50797 \times 10^{-10} > 0$ at $p/q = 94109/6658$).

---

## B. Preflight `TASK-TC-037R` Status Repair

Before initiating `TASK-TC-038`, two residual status/witness items from `TASK-TC-037R` were repaired and synchronized across the repository (`tc/grade_character_projection.py`, `tc/__init__.py`, `tests/test_tc_grade_character_projection.py`, `data/tc_grade_character_projection.json`, `docs/reviews/TC_GRADE_CHARACTER_REFLECTION_PROJECTION.md`, `CURVATURE_TRANSPORT.md`, `ARITHMETIC_RADIAL_BRIDGE.md`, `CMSA_GATE_G4.md`, and canonical status ledgers):

1. **Zero-Free Strip Status Correction**:
   Because `TASK-TC-037R` proved via 128-bit Arb interval arithmetic that the inversion-even Mellin transform $\widehat{\Psi}_{1,+}(z)$ changes sign on the critical line $z = i\gamma$ (and hence vanishes in $(-1/2, 1/2) \times i\mathbb{R}$ by the Intermediate Value Theorem), the misleading status token `INVERSION_EVEN_MELLIN_WEIGHT_ZERO_FREE_STRIP_OPEN` was replaced as the canonical Mellin-strip status by:
   $$\boxed{\texttt{INVERSION\_EVEN\_MELLIN\_ZERO\_FREE\_STRIP\_FALSE}},$$
   paired with the distinct open question at actual zeta-zero ordinates:
   $$\boxed{\texttt{STRICT\_REFLECTION\_WEIGHT\_AT\_ZETA\_ZERO\_ORDINATES\_OPEN}}.$$
2. **Synchronized Critical-Line Sign-Change Witness Pair**:
   All prose, code, JSON artifacts, and tests are synchronized to the single canonical witness pair $(\gamma_a, \gamma_b) = (0.25, 1.0)$:
   $$\widehat{\Psi}_{1,+}(i \cdot 0.25) = +0.005930018171819737 > 0, \qquad \widehat{\Psi}_{1,+}(i \cdot 1.0) = -0.01007544310514176 < 0 \qquad (\text{128-bit Arb}).$$

---

## C. Candidate Object Definitions: $\gamma_n$, $\rho_n$, $\gamma_n + 1/2$

We distinguish three candidate objects associated with the $n$-th nontrivial zero of $\zeta(s)$ in the upper half-strip ($\gamma_n > 0$):

| Candidate | Definition | Ambient Domain | Arithmetic Status |
| :--- | :--- | :--- | :--- |
| **Candidate 1** | $\gamma_n = \operatorname{Im}(\rho_n) > 0$ | $\mathbb{R}_{>0}$ | Primary real ordinate; rationality and algebraicity `OPEN_IN_LITERATURE` |
| **Candidate 2** | $\rho_n = \beta_n + i\gamma_n = \frac{1}{2} + \delta_n + i\gamma_n$ | $\{s \in \mathbb{C} : 0 < \operatorname{Re}(s) < 1\}$ | Primary complex zero; $\rho_n \notin \mathbb{Q}$ `PROVED`; algebraicity `OPEN_IN_LITERATURE` |
| **Candidate 3** | $\tilde{\gamma}_n = \gamma_n + \frac{1}{2}$ | $\mathbb{R}_{>1/2}$ | Real affine translate of $\gamma_n$; `SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE` |

Note that on the critical line ($\beta_n = 1/2$), the full complex zero is $\rho_n = \frac{1}{2} + i\gamma_n \in \mathbb{C} \setminus \mathbb{R}$, **not** the real number $\gamma_n + \frac{1}{2}$.

---

## D. Shifted-Ordinate Redundancy Theorem

**Theorem D.1 (`shifted_ordinate_rational_iff`, `shifted_ordinate_algebraic_iff`, `shifted_ordinate_transcendental_iff` in `formal/RiemannScope/ZeroArithmeticInvariants.lean`)**:
For every real number $\gamma \in \mathbb{R}$:
1. $\gamma + \frac{1}{2} \in \mathbb{Q} \iff \gamma \in \mathbb{Q}$.
2. $\gamma + \frac{1}{2} \in \overline{\mathbb{Q}} \iff \gamma \in \overline{\mathbb{Q}}$.
3. $\gamma + \frac{1}{2}$ is transcendental over $\mathbb{Q}$ if and only if $\gamma$ is transcendental over $\mathbb{Q}$.
4. The generated number fields coincide: $\mathbb{Q}(\gamma + 1/2) = \mathbb{Q}(\gamma)$, and $\deg_{\mathbb{Q}}(\gamma + 1/2) = \deg_{\mathbb{Q}}(\gamma)$.
5. Explicitly, if $P(X) = \sum_{k=0}^d a_k X^k \in \mathbb{Z}[X]$ has degree $d \ge 1$ and satisfies $P(\gamma) = 0$, then
   $$Q(Y) := 2^d P\!\left(Y - \frac{1}{2}\right) = \sum_{j=0}^d \left(\sum_{k=j}^d a_k \binom{k}{j} (-1)^{k-j} 2^{d-k}\right) Y^j \in \mathbb{Z}[Y]$$
   has integer coefficients, degree $d$, and satisfies $Q(\gamma + 1/2) = 0$, with Coefficient-Bound Transformation $H(Q) \le 3^d H(P)$.

**Classification**:
$$\boxed{\texttt{SHIFTED\_ORDINATE\_ARITHMETICALLY\_EQUIVALENT\_TO\_ORDINATE}.}$$

---

## E. Full-Zero versus Ordinate Algebraicity Diagram

Let $\rho = \beta + i\gamma$ be any nontrivial zero of $\zeta(s)$ with $\beta, \gamma \in \mathbb{R}$ and $\gamma > 0$. Because $\zeta(\bar{s}) = \overline{\zeta(s)}$ for all $s \in \mathbb{C} \setminus \{1\}$, $\bar{\rho} = \beta - i\gamma$ is also a nontrivial zero of $\zeta(s)$.

### 1. Unconditional Equivalences (Formalized in `complex_zero_re_im_algebraicity`)
Since $\overline{\mathbb{Q}} \subset \mathbb{C}$ is a field closed under complex conjugation ($\alpha \in \overline{\mathbb{Q}} \implies \bar{\alpha} \in \overline{\mathbb{Q}}$, as both satisfy the same rational polynomial) and $i \in \overline{\mathbb{Q}}$ ($i^2 + 1 = 0$):
$$\beta = \frac{\rho + \bar{\rho}}{2}, \qquad \gamma = \frac{\rho - \bar{\rho}}{2i}.$$
Consequently, **unconditionally** (without assuming RH):
$$\boxed{\rho = \beta + i\gamma \in \overline{\mathbb{Q}} \iff \left(\beta \in \overline{\mathbb{Q}} \;\wedge\; \gamma \in \overline{\mathbb{Q}}\right).}$$
Contrapositively:
- $\gamma \notin \overline{\mathbb{Q}} \implies \rho \notin \overline{\mathbb{Q}}$ (unconditional),
- $\beta \notin \overline{\mathbb{Q}} \implies \rho \notin \overline{\mathbb{Q}}$ (unconditional),
- $\rho \notin \overline{\mathbb{Q}} \implies (\beta \notin \overline{\mathbb{Q}} \;\vee\; \gamma \notin \overline{\mathbb{Q}})$ (unconditional, but without knowing $\beta \in \overline{\mathbb{Q}}$ one cannot deduce $\gamma \notin \overline{\mathbb{Q}}$ alone).

Moreover, for rationality:
$$\boxed{\rho_n \notin \mathbb{Q} \quad \text{unconditionally for all } n \ge 1,}$$
because $(1 - 2^{1-s})\zeta(s) = \sum_{m=1}^\infty (-1)^{m-1} m^{-s} > 0$ for all $s \in (0, 1)$ while $1 - 2^{1-s} < 0$ on $(0, 1)$, so $\zeta(s) < 0$ on $(0, 1)$ and $\gamma_n = \operatorname{Im}(\rho_n) \ne 0$.

### 2. Conditional Equivalences Assuming RH ($\beta = 1/2 \in \mathbb{Q}$)
Only under the hypothesis $\beta_n = 1/2$ (`CONDITIONAL_ON_RH`) does $\beta_n \in \mathbb{Q} \subset \overline{\mathbb{Q}}$ hold automatically, yielding:
$$\text{Under } \beta_n = \frac{1}{2}: \qquad \rho_n = \frac{1}{2} + i\gamma_n \in \overline{\mathbb{Q}} \iff \gamma_n \in \overline{\mathbb{Q}}, \qquad \rho_n \in \mathbb{Q}(i) \iff \gamma_n \in \mathbb{Q}.$$
Unconditional and RH-conditional implications are kept strictly separated throughout `tc/zero_arithmetic_invariants.py` and `data/tc_zero_arithmetic_invariants.json`.

---

## F. Primary-Source Audit of Individual Zero Arithmetic

Every claim below was audited against primary sources (using `literature-search-arxiv` and standard reference monographs) and classified using the strict tokens of Sections 8 and 44:

| Question | Status Classification | Source Verification | Primary-Source Explanation |
| :--- | :--- | :--- | :--- |
| Is $\rho_n \notin \mathbb{Q}$ for every nontrivial zero $\rho_n$? | `PROVED` | `PRIMARY_SOURCE_VERIFIED` | Since $\zeta(s) < 0$ on $(0, 1)$ via $\eta(s) = (1-2^{1-s})\zeta(s) > 0$, every nontrivial zero in $0 < \operatorname{Re}(s) < 1$ has $\operatorname{Im}(\rho_n) \ne 0$, hence $\rho_n \notin \mathbb{R} \supset \mathbb{Q}$ (Titchmarsh 1986, §2.12). |
| Is $\gamma_1 \notin \mathbb{Q}$ (or any individual $\gamma_n \notin \mathbb{Q}$) proved? | `OPEN_IN_LITERATURE` | `NO_PRIMARY_SOURCE_FOUND` | No theorem in the peer-reviewed or arXiv literature establishes irrationality of $\gamma_1$ or any individual ordinate $\gamma_n$. |
| Is $\rho_1 \notin \overline{\mathbb{Q}}$ or $\gamma_1 \notin \overline{\mathbb{Q}}$ proved? | `OPEN_IN_LITERATURE` | `NO_PRIMARY_SOURCE_FOUND` | No theorem in the literature proves transcendence of any individual nontrivial zero $\rho_n$ or ordinate $\gamma_n$. |
| Are infinitely many distinct ordinates $\gamma_n$ irrational / transcendental? | `PROVED_WITH_EXTERNAL_THEOREM` (transcendence by cardinality only) | `PRIMARY_SOURCE_VERIFIED` | Hardy (1914) and Selberg (1942) prove infinitely many distinct $\gamma_n$ exist; Bui–Conrey–Young (2011) prove $\ge 40.89\%$ of zeros are simple and distinct (`TASK-TC-037R`). Only a cardinality consequence applies: an uncountable set yields transcendental elements, whereas $\{\gamma_n\}_{n \ge 1}$ is **countable**, so cardinality alone does **not** prove transcendence of any $\gamma_n$; however, only finitely many $\gamma_n$ can lie in any fixed number field $K$ of bounded height. Whether even one $\gamma_n$ is transcendental remains `OPEN_IN_LITERATURE`. |
| Are the positive ordinates $\{\gamma_n\}_{n \ge 1}$ linearly independent over $\mathbb{Q}$? | `CONDITIONAL_ON_NAMED_CONJECTURE` (Linear Independence Conjecture `LI`) | `PRIMARY_SOURCE_VERIFIED` | Coined by Wintner (1935) / Ingham (1942) and studied by Rubinstein–Sarnak (1994, *Exp. Math.* 3, 173–197). Under `LI`, at most one $\gamma_n$ could be rational, and every zero is simple; `LI` itself is completely open. |

---

## G. Broader $L$-Function and $E$-Function Comparison

To test whether zero-location transcendence is known for adjacent analytic classes, we audited four comparison classes:

1. **Dirichlet $L(s, \chi)$ and Automorphic $L$-Functions**:
   - **Status**: `NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT` / `OPEN_IN_LITERATURE`.
   - Just as for $\zeta(s)$, no theorem establishes the irrationality or transcendence of any individual nontrivial critical-strip zero of a primitive Dirichlet $L(s, \chi)$ or cuspidal automorphic $L(s, \pi)$. The Grand Simplicity Hypothesis (GSH, Rubinstein–Sarnak 1994) conjectures $\mathbb{Q}$-linear independence of all positive ordinates across primitive $L(s, \chi)$, which remains open.
2. **Dedekind $\zeta_K(s)$ and Epstein Zeta Functions**:
   - **Status**: `NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT` for Dedekind $\zeta_K(s)$.
   - For Epstein zeta functions $\zeta_Q(s)$ with class number $h(D) \ge 2$, Davenport–Heilbronn (1936) proved the existence of infinitely many off-critical zeros in $\operatorname{Re}(s) > 1$ and $1/2 < \operatorname{Re}(s) < 1$, but the arithmetic nature (algebraicity vs. transcendence) of individual off-critical zeros is likewise open.
3. **Exponential Polynomials $\sum_{j=1}^m a_j e^{\alpha_j z}$**:
   - **Status**: Partial results via **Lindemann–Weierstrass** and **Gelfond–Schneider**, with general case governed by **Schanuel's Conjecture** (`CONDITIONAL_ON_NAMED_CONJECTURE`).
   - For a simple two-term exponential polynomial $e^z - a = 0$ with $a \in \overline{\mathbb{Q}} \setminus \{0, 1\}$, every root $z = \log a + 2\pi i k$ is transcendental by Lindemann–Weierstrass ($z \in \overline{\mathbb{Q}} \setminus \{0\} \implies e^z \notin \overline{\mathbb{Q}}$). For $2^{-s} + 3^{-s} = 0$, $s = \frac{(2k+1)\pi i}{\log(3/2)}$ has ratio $\frac{\log 2}{\log 3} \notin \overline{\mathbb{Q}}$ by Gelfond–Schneider, but the individual root involves $\pi / \log(3/2)$ whose transcendence requires Schanuel's conjecture. Crucially, $\zeta(s)$ is an **infinite** Dirichlet series whose representation $\sum_{n=1}^\infty n^{-s}$ does not converge in $0 < \operatorname{Re}(s) < 1$, so exponential-polynomial theorems do not transfer.
4. **Bessel Functions $J_\nu(z)$ and Siegel $E$-Functions (Siegel 1929 / Shidlovsky 1959)**:
   - **Status**: `PROVED_WITH_EXTERNAL_THEOREM` for $E$-functions (`PRIMARY_SOURCE_VERIFIED`).
   - By the **Siegel–Shidlovsky theorem** (Siegel 1929; Shidlovsky 1959, *Izv. Akad. Nauk SSSR Ser. Mat.* 23, 35–66), if $\nu \in \mathbb{Q}$, every nonzero zero $\alpha \ne 0$ of $J_\nu(z) = 0$ (and of $J'_\nu(z) = 0$) is **transcendental** ($\alpha \notin \overline{\mathbb{Q}}$).
   - **Why Bessel zeros succeed where $\zeta(\rho) = 0$ fails**: $z^{-\nu} J_\nu(z)$ is a **Siegel $E$-function** satisfying a linear differential equation over $\mathbb{Q}(z)$, namely $z^2 y'' + z y' + (z^2 - \nu^2)y = 0$, with Taylor coefficients $c_k$ having factorial denominators $O((k!)^{-2})$ and algebraic growth. By contrast, $\zeta(s)$ and $\xi(s)$ are **differentially transcendental** (Hilbert 1900; Ostrowski 1920) — they satisfy no algebraic differential equation over $\mathbb{C}(s)$ — and their Taylor coefficients involve transcendental Stieltjes constants rather than algebraic rationals.

---

## H. Transcendence-Theorem Applicability Matrix

The following matrix audits all nine major transcendence theorem families against the target equation $\zeta(\rho) = 0$ for $\rho \in \{0 < \operatorname{Re}(s) < 1\} \cap \overline{\mathbb{Q}}$:

| Theorem Family | Exact Hypotheses | Target Attempted from $\zeta(\rho) = 0$ | Exact Missing Hypothesis | Applicability Classification |
| :--- | :--- | :--- | :--- | :--- |
| **1. Lindemann–Weierstrass** (1882/1885) | Distinct $\alpha_1, \dots, \alpha_m \in \overline{\mathbb{Q}} \implies e^{\alpha_1}, \dots, e^{\alpha_m}$ are algebraically independent over $\overline{\mathbb{Q}}$. | Apply to $p^{-\rho} = e^{-\rho \log p}$ under $\rho \in \overline{\mathbb{Q}}$. | The exponents $-\rho \log p$ are **transcendental** ($\log p \notin \overline{\mathbb{Q}}$ for prime $p$), not algebraic; and $\sum_{n=1}^\infty n^{-\rho}$ is an infinite series that diverges in $0 < \operatorname{Re}(\rho) < 1$. | `DOES_NOT_APPLY_MISSING_ALGEBRAIC_EXPONENT_AND_FINITENESS` |
| **2. Gelfond–Schneider** (1934) | $\alpha \in \overline{\mathbb{Q}} \setminus \{0, 1\}$ and $\beta \in \overline{\mathbb{Q}} \setminus \mathbb{Q} \implies \alpha^\beta \notin \overline{\mathbb{Q}}$. | Deduce $p^{-\rho} \notin \overline{\mathbb{Q}}$ for prime $p$ and $\rho \in \overline{\mathbb{Q}} \setminus \mathbb{Q}$, and seek contradiction with $\zeta(\rho) = 0$. | Gives $p^{-\rho} \notin \overline{\mathbb{Q}}$ for each prime $p$ when $\rho \in \overline{\mathbb{Q}} \setminus \mathbb{Q}$, but $\zeta(\rho) = 0$ does **not** force any single $p^{-\rho}$ or finite $\overline{\mathbb{Q}}$-combination of $p^{-\rho}$ to be algebraic. | `INDIVIDUAL_PRIME_POWERS_TRANSCENDENTAL_NO_CONTRADICTION_WITH_ZETA_ZERO` |
| **3. Baker's Theorem on Linear Forms in Logarithms** (1966) | $\beta_0 + \sum_{j=1}^m \beta_j \log \alpha_j \ne 0$ (with quantitative lower bound) for $\alpha_j \in \overline{\mathbb{Q}}^\times$, $\beta_j \in \overline{\mathbb{Q}}$. | Apply to $\sum_p c_p (-\rho \log p)$ or functional-equation phase $\log \chi(\rho) = 2\pi i k$. | $\zeta(\rho) = 0$ is a zero of an analytic continuation of an infinite sum of exponentials $\exp(-\rho \log n)$, not a linear form in logarithms of algebraic numbers; and $\chi(\rho) \ne 0$ for $0 < \operatorname{Re}(\rho) < 1$. | `DOES_NOT_APPLY_ZETA_ZERO_NOT_LINEAR_FORM_IN_LOGS` |
| **4. Siegel–Shidlovsky $E$-Function Theory** (1929/1959) | Tuple $(f_1(z), \dots, f_m(z))$ of Siegel $E$-functions ($\overline{\mathbb{Q}}$ Taylor coefficients with factorial denominators) satisfying a linear ODE system over $\mathbb{C}(z)$. | Treat $\xi(s)$ or $\zeta(s)$ as an $E$-function evaluated at $s = \rho \in \overline{\mathbb{Q}}$. | Both hypotheses fail: (i) $\zeta(s)$ and $\xi(s)$ satisfy **no** linear or algebraic ODE over $\mathbb{C}(s)$ (Hilbert–Ostrowski); (ii) Taylor coefficients of $\xi(s)$ or $\zeta(s)$ at any rational point are transcendental (involving $\gamma_E, \log\pi, \gamma_k$), not in $\overline{\mathbb{Q}}$. | `DOES_NOT_APPLY_NOT_E_FUNCTION_NO_ODE_OVER_Q_S` |
| **5. Schneider–Lang Criterion** (1949/1966) | Meromorphic functions $f_1, \dots, f_d$ of finite order generating a field $K(f_1, \dots, f_d)$ mapped into itself by $d/ds$, taking values in a number field $K$ at $m$ distinct points. | Apply to $(s, \zeta(s))$ or $(s, \xi(s))$ at $\rho, 1-\rho, \bar{\rho}, 1-\bar{\rho}$. | The ring $K[s, \zeta(s), \zeta'(s), \dots]$ has **infinite transcendence degree** over $K(s)$ under $d/ds$ because $\zeta(s)$ satisfies no algebraic differential equation. | `DOES_NOT_APPLY_DIFFERENTIAL_RING_NOT_FINITELY_GENERATED` |
| **6. Nesterenko's Modular Independence Theorem** (1996) | For $\tau \in \mathbb{H}$, $\operatorname{tr.deg}_{\mathbb{Q}} \mathbb{Q}(e^{2\pi i \tau}, E_2(\tau), E_4(\tau), E_6(\tau)) \ge 3$ (yielding algebraicity independence of $\pi, e^\pi, \Gamma(1/4)$). | Apply to Mellin transform $\xi(s) = \int_0^\infty (\theta(it)-1) t^{s/2-1} dt$. | Nesterenko's theorem controls pointwise evaluations of modular forms $E_2, E_4, E_6$ at fixed CM points $\tau \in \mathbb{H}$ via Ramanujan's ODE system; the Mellin integral integrates over all $t \in (0, \infty)$ with weight $t^{\rho/2-1}$, destroying the finite-dimensional modular ODE structure. | `DOES_NOT_APPLY_MELLIN_INTEGRAL_BREAKS_POINTWISE_MODULAR_ODE` |
| **7. Chudnovsky / Elliptic Period Transcendence** (1976/1984) | Periods and quasi-periods $\omega_1, \omega_2, \eta_1, \eta_2$ of elliptic curves defined over $\overline{\mathbb{Q}}$. | Interpret $\rho_n$ or $S_m$ as elliptic curve periods over $\overline{\mathbb{Q}}$. | Nontrivial zeros $\rho_n$ of $\zeta(s)$ are neither periods nor quasi-periods of elliptic curves or abelian varieties over $\overline{\mathbb{Q}}$. | `DOES_NOT_APPLY_ZETA_ZEROS_NOT_ELLIPTIC_PERIODS` |
| **8. Rohrlich–Lang / $\Gamma$-Value Relations** (Lang 1966; Rohrlich 1978) | All universal multiplicative relations among $\Gamma(a)$ for $a \in \mathbb{Q}$ come from reflection, multiplication (Gauss), and translation relations. | Use $\Gamma(\rho/2) / \Gamma((1-\rho)/2)$ in $\zeta(\rho) = \chi(\rho)\zeta(1-\rho)$ at $\rho \in \overline{\mathbb{Q}}$. | When $\zeta(\rho) = 0$ and $\zeta(1-\rho) = 0$, the functional equation reduces to $0 = \chi(\rho) \cdot 0$, which eliminates $\chi(\rho)$ completely! | `DOES_NOT_APPLY_CHI_RHO_MULTIPLIED_BY_ZERO_AT_ZETA_ZERO` |
| **9. Hölder–Ostrowski Differential Transcendence** (1887/1920) | $\Gamma(s)$ and $\zeta(s)$ satisfy no nontrivial algebraic differential equation $P(s, f(s), f'(s), \dots, f^{(k)}(s)) = 0$ over $\mathbb{C}[s]$. | Conclude from differential transcendence of $\zeta(s)$ that $\zeta(\rho) = 0 \implies \rho \notin \overline{\mathbb{Q}}$. | **Logically invalid**: Differential transcendence of $f(s)$ over $\mathbb{C}(s)$ does **not** imply that the zeros of $f$ are transcendental numbers (Section U). | `DOES_NOT_APPLY_DIFFERENTIAL_TRANSCENDENCE_ALLOWS_ALGEBRAIC_ZEROS` |

---

## I. Functional-Equation Algebraicity Test

Suppose for contradiction (or structural test) that a nontrivial zero $\rho = \beta + i\gamma$ of $\zeta(s)$ is algebraic ($\rho \in \overline{\mathbb{Q}}$, with $0 < \beta < 1$ and $\gamma > 0$). We test what the functional equation
$$\xi(s) = \xi(1-s), \qquad \zeta(s) = \chi(s)\zeta(1-s), \qquad \chi(s) = 2^s \pi^{s-1} \sin\!\left(\frac{\pi s}{2}\right)\Gamma(1-s)$$
forces at $s = \rho$:

1. **Symmetry Orbit Closure**:
   Since $\rho \in \overline{\mathbb{Q}}$, all four points of the symmetry orbit
   $$\mathcal{O}(\rho) = \{\rho,\; 1-\rho,\; \bar{\rho},\; 1-\bar{\rho}\} \subset \overline{\mathbb{Q}}$$
   are algebraic numbers of the same degree over $\mathbb{Q}$, and $\zeta(s) = 0$ at all four points.
2. **Simultaneous Vanishing Absorbs $\chi(\rho)$**:
   In the asymmetric functional equation $\zeta(\rho) = \chi(\rho)\zeta(1-\rho)$, the factor $\chi(\rho)$ is finite and nonzero on $0 < \operatorname{Re}(s) < 1$ (since $\Gamma(1-s)$ has no zeros and no poles for $\operatorname{Re}(s) < 1$, and $\sin(\pi s/2) \ne 0$ for $\operatorname{Im}(s) \ne 0$). However, because **both** $\zeta(\rho) = 0$ and $\zeta(1-\rho) = 0$, the equation evaluates at $s = \rho$ to:
   $$0 = \chi(\rho) \cdot 0.$$
   Therefore **no algebraic value, rational value, or unit modulus constraint is imposed on $\chi(\rho)$**.
3. **Logarithmic Derivative at Simple Zeros**:
   If $\rho$ is a simple zero of multiplicity $m_\rho = 1$, differentiating $\xi(s) = \xi(1-s)$ gives $\xi'(\rho) = -\xi'(1-\rho) \ne 0$, and differentiating $\zeta(s) = \chi(s)\zeta(1-s)$ gives $\zeta'(\rho) = -\chi(\rho)\zeta'(1-\rho)$. Since neither $\zeta'(\rho)$ nor $\zeta'(1-\rho)$ is constrained to lie in $\overline{\mathbb{Q}}$, the ratio $-\zeta'(\rho)/\zeta'(1-\rho) = \chi(\rho)$ produces no Diophantine contradiction.

**Classification**:
$$\boxed{\texttt{FUNCTIONAL\_EQUATION\_DOES\_NOT\_EXCLUDE\_ALGEBRAIC\_ZERO}.}$$

---

## J. Euler-Product Critical-Strip Firewall

For $\operatorname{Re}(s) > 1$, the Euler product converges absolutely:
$$\zeta(s) = \prod_{p \text{ prime}} \left(1 - p^{-s}\right)^{-1}, \qquad \operatorname{Re}(s) > 1.$$
If $s \in \overline{\mathbb{Q}} \setminus \mathbb{Q}$, Gelfond–Schneider implies $p^{-s} \notin \overline{\mathbb{Q}}$ for every prime $p$, and each Euler factor $(1 - p^{-s})^{-1} \ne 0$.

However:
1. Inside the critical strip $0 < \operatorname{Re}(s) < 1$, the infinite product $\prod_p (1 - p^{-s})^{-1}$ and the Dirichlet series $\sum_{n=1}^\infty n^{-s}$ **do not converge** to $\zeta(s)$ (indeed, by conditional/Voronin universality behavior in $1/2 < \operatorname{Re}(s) < 1$, truncated Euler products do not control individual zeros).
2. Nonvanishing of each individual Euler factor $1 - p^{-\rho} \ne 0$ (which holds for every $\rho$ with $\operatorname{Re}(\rho) > 0$ since $|p^{-\rho}| = p^{-\beta} < 1$) does **not** prevent the analytic continuation $\zeta(\rho)$ from vanishing in $0 < \operatorname{Re}(\rho) < 1$.

**Classification**:
$$\boxed{\texttt{EULER\_PRODUCT\_NONVANISHING\_NOT\_AVAILABLE\_IN\_CRITICAL\_STRIP}.}$$

---

## K. Exact Hadamard Factorization of $\xi(s)$

We use the canonical completed Riemann xi function:
$$\xi(s) := \frac{1}{2} s(s-1)\pi^{-s/2}\Gamma\!\left(\frac{s}{2}\right)\zeta(s) = s(s-1)\pi^{-s/2}\Gamma\!\left(\frac{s}{2}+1\right)\zeta(s).$$
- **Value at $s = 0$ and $s = 1$**: Since $\lim_{s\to 0} s\Gamma(s/2) = 2$ and $\zeta(0) = -\frac{1}{2}$, we have:
  $$\xi(0) = \frac{1}{2} (-1) \cdot 1 \cdot 2 \cdot \left(-\frac{1}{2}\right) = \frac{1}{2} = \xi(1).$$
- **Hadamard Factorization (Hadamard 1893; Davenport 2000, Ch. 12; Edwards 1974, Ch. 2)**:
  Since $\xi(s)$ is an entire function of order $1$ with zeros exclusively at the nontrivial zeros $\rho$ of $\zeta(s)$ (counted with multiplicity):
  $$\boxed{\xi(s) = \xi(0) e^{B_{\mathrm{Had}} s} \prod_{\rho} \left(1 - \frac{s}{\rho}\right) e^{s/\rho}, \qquad \xi(0) = \frac{1}{2},}$$
  where the exponential constant is:
  $$\boxed{B_{\mathrm{Had}} = \frac{\xi'(0)}{\xi(0)} = -1 - \frac{\gamma_E}{2} + \frac{1}{2}\log(4\pi) = -S_1 \approx -0.0230957089661210338143102479065.}$$
- **Paired Product Without Exponential Convergence Factors**:
  When zeros are grouped symmetrically by $|\operatorname{Im}(\rho)| \le T$ (or paired as $(\rho, 1-\rho)$ / $(\rho, \bar{\rho})$), the factors $\sum_{|\operatorname{Im}\rho|\le T} \frac{1}{\rho}$ converge to $S_1 = -B_{\mathrm{Had}}$, so the exponential factors cancel:
  $$\boxed{\xi(s) = \frac{1}{2} \lim_{T\to\infty} \prod_{|\operatorname{Im}(\rho)| \le T} \left(1 - \frac{s}{\rho}\right) = \frac{1}{2} \prod_{\{\rho, 1-\rho\}} \left(1 - \frac{s(1-s)}{\rho(1-\rho)}\right).}$$

---

## L. First Reciprocal Zero Sum $S_1$ and Reflection-Invariant Sum

### 1. First Reciprocal Sum $S_1$
Taking the logarithmic derivative of the Hadamard product gives:
$$\frac{\xi'(s)}{\xi(s)} = B_{\mathrm{Had}} + \sum_{\rho} \left(\frac{1}{s - \rho} + \frac{1}{\rho}\right) = \lim_{T\to\infty} \sum_{|\operatorname{Im}(\rho)| \le T} \frac{1}{s - \rho}.$$
Evaluating at $s = 0$ (or $s = 1$, using $\xi'(1)/\xi(1) = -\xi'(0)/\xi(0)$):
$$\frac{\xi'(s)}{\xi(s)} = \frac{1}{s} + \frac{1}{s-1} - \frac{1}{2}\log\pi + \frac{1}{2}\psi\!\left(\frac{s}{2}\right) + \frac{\zeta'(s)}{\zeta(s)}.$$
Using $\psi(s/2) = -\frac{2}{s} - \gamma_E + \frac{\pi^2}{12}s + O(s^2)$ as $s \to 0$, the $1/s$ poles cancel and:
$$\frac{\xi'(0)}{\xi(0)} = -1 - \frac{1}{2}\log\pi - \frac{\gamma_E}{2} + \frac{\zeta'(0)}{\zeta(0)}.$$
Since $\zeta(0) = -1/2$ and $\zeta'(0) = -\frac{1}{2}\log(2\pi)$, we have $\frac{\zeta'(0)}{\zeta(0)} = \log(2\pi)$, so:
$$\boxed{S_1 := \lim_{T\to\infty} \sum_{|\operatorname{Im}(\rho)| \le T} \frac{1}{\rho} = -\frac{\xi'(0)}{\xi(0)} = \frac{\xi'(1)}{\xi(1)} = 1 + \frac{\gamma_E}{2} - \frac{1}{2}\log(4\pi) = 1 + \frac{\gamma_E}{2} - \log(2\sqrt{\pi}).}$$
- **Convergence status**: Conditionally convergent — requires symmetric height pairing $|\operatorname{Im}(\rho)| \le T$ (or pairing $\rho$ with $1-\rho$ or $\bar{\rho}$), since $\sum_{0 < \gamma_\rho \le T} \gamma_\rho^{-1} \sim \frac{1}{4\pi}(\log T)^2 \to \infty$.
- **50-digit value (verified by SymPy and mpmath, residual $1.04 \times 10^{-51}$)**:
  $$S_1 = 0.023095708966121033814310247906495291621929098192089.$$

### 2. Reflection-Invariant Reciprocal Sum (`reflection_reciprocal_identity` in Lean 4)
For any $\rho \notin \{0, 1\}$, we have the exact algebraic identity (formalized in Lean 4 as `reflection_reciprocal_identity`):
$$\boxed{\frac{1}{\rho} + \frac{1}{1-\rho} = \frac{1}{\rho(1-\rho)}.}$$
Summing over all nontrivial zeros $\rho$ (each zero $\rho$ paired with its functional-equation partner $1-\rho$, noting that both $\rho$ and $1-\rho$ are included in the sum over all zeros):
$$\boxed{\sum_{\rho} \frac{1}{\rho(1-\rho)} = \sum_{\rho}^{\mathrm{sym}} \left(\frac{1}{\rho} + \frac{1}{1-\rho}\right) = 2 S_1 = 2\lambda_1 = 2 + \gamma_E - \log(4\pi).}$$
- **Absolute convergence**: Because $|\rho(1-\rho)| = \gamma_\rho^2 + O(1)$, we have $\sum_\rho |\rho(1-\rho)|^{-1} \ll \sum_\rho \gamma_\rho^{-2} < \infty$, so $\sum_\rho \frac{1}{\rho(1-\rho)}$ **converges absolutely without any grouping convention**.
- **50-digit value**:
  $$\sum_{\rho} \frac{1}{\rho(1-\rho)} = 2 S_1 = 2\lambda_1 = 0.046191417932242067628620495812990583243858196384178.$$

---

## M. Second Reciprocal Zero Sum $S_2$ and Higher $S_m$

### 1. General Logarithmic Derivative Identity ($m \ge 2$)
Differentiating $\frac{\xi'(s)}{\xi(s)} = -\sum_{m=1}^\infty S_m s^{m-1}$ around $s = 0$ (and around $s = 1$ using $\xi(1-s) = \xi(s)$, formalized in Lean 4 as `reciprocal_power_log_derivative_sign_identity`):
$$\boxed{S_m := \sum_{\rho} \frac{1}{\rho^m} = -\frac{1}{(m-1)!} \left.\frac{d^m}{ds^m} \log \xi(s)\right|_{s=0} = \frac{(-1)^m}{(m-1)!} \left.\frac{d^m}{ds^m} \log \xi(s)\right|_{s=1} \qquad (m \ge 1).}$$
For every integer $m \ge 2$, $S_m$ **converges absolutely** by partial summation against $N(T) = \frac{T}{2\pi}\log\frac{T}{2\pi} - \frac{T}{2\pi} + O(\log T) = O(T\log T)$, since $\int_2^\infty T^{-m}\log T\,dT < \infty$ for $m \ge 2$.

### 2. Explicit Derivation of $S_2$ at both $s = 0$ and $s = 1$
Using the regular part at $s = 0$:
$$\frac{\xi'(s)}{\xi(s)} = \frac{1}{s-1} - \frac{1}{2}\log\pi + \frac{1}{2}\left(\psi\!\left(1 + \frac{s}{2}\right) - \frac{\zeta'(s)}{\zeta(s)}\cdot (-2)\right),$$
differentiating at $s = 0$ gives:
$$-\left.\frac{d}{ds}\frac{\xi'(s)}{\xi(s)}\right|_{s=0} = 1 - \frac{1}{4}\psi_1(1) - \left.\frac{d}{ds}\frac{\zeta'(s)}{\zeta(s)}\right|_{s=0}.$$
Since $\psi_1(1) = \zeta(2) = \frac{\pi^2}{6}$ and $\left.\frac{d}{ds}\frac{\zeta'(s)}{\zeta(s)}\right|_{s=0} = \frac{\zeta''(0)}{\zeta(0)} - \left(\frac{\zeta'(0)}{\zeta(0)}\right)^2 = -2\zeta''(0) - \log^2(2\pi)$:
$$\boxed{S_2 = 1 - \frac{\pi^2}{24} + 2\zeta''(0) + \log^2(2\pi).}$$
Expanding identically at $s = 1$ using the Laurent expansion $\zeta(s) = \frac{1}{s-1} + \gamma_E - \gamma_1(s-1) + \frac{\gamma_2}{2}(s-1)^2 - \dots$ (where $\gamma_k$ are the Stieltjes constants) and $\frac{1}{2}\psi(s/2)$ at $s = 1$ ($\psi_1(1/2) = \frac{\pi^2}{2}$):
$$\boxed{S_2 = 1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1 \approx -0.0461543172958046027571079903790773035302679623.}$$
Both expressions agree symbolically and to 50 decimal digits (residual $1.00 \times 10^{-51}$), linked by the classic functional-equation identity $2\zeta''(0) + \log^2(2\pi) = \gamma_E^2 - \frac{\pi^2}{12} + 2\gamma_1$.

### 3. Hierarchy Table for $S_1, S_2, S_3, S_4$

| $m$ | Convergence | Logarithmic Derivative Formula | Exact Closed-Form Expression | 50-Digit Numerical Value |
| :--- | :--- | :--- | :--- | :--- |
| $1$ | Conditionally convergent ($|\operatorname{Im}\rho| \le T$) | $-\left.\frac{d}{ds}\log\xi(s)\right|_{s=0}$ | $1 + \frac{\gamma_E}{2} - \log(2\sqrt{\pi})$ | $+0.02309570896612103381431024790649529162193$ |
| $2$ | Absolutely convergent | $-\left.\frac{d^2}{ds^2}\log\xi(s)\right|_{s=0}$ | $1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1$ | $-0.04615431729580460275710799037907730353027$ |
| $3$ | Absolutely convergent | $-\frac{1}{2!}\left.\frac{d^3}{ds^3}\log\xi(s)\right|_{s=0}$ | $1 - \frac{7}{8}\zeta(3) + \gamma_E^3 + 3\gamma_E\gamma_1 + \frac{3}{2}\gamma_2$ | $-0.0001111582314521059227626682389145784739642$ |
| $4$ | Absolutely convergent | $-\frac{1}{3!}\left.\frac{d^4}{ds^4}\log\xi(s)\right|_{s=0}$ | $1 - \frac{\pi^4}{96} + \gamma_E^4 + 4\gamma_E^2\gamma_1 + 2\gamma_1^2 + 2\gamma_E\gamma_2 + \frac{2}{3}\gamma_3$ | $+0.00007362722126168951832677130703060151131283$ |

---

## N. Centered Zero Invariants $\Sigma_{2m}$ and Quartet Polynomial

In centered coordinates $z_\rho := \rho - \frac{1}{2} = \delta_\rho + i\gamma_\rho$, let $\Xi(z) := \xi\!\left(\frac{1}{2} + z\right) = \Xi(-z)$.

1. **Identical Vanishing of Odd Centered Sums**:
   Since $z_{1-\rho} = -z_\rho$, every reflection pair $\{\rho, 1-\rho\}$ satisfies $z_\rho^{-(2m-1)} + z_{1-\rho}^{-(2m-1)} = 0$. Equivalently, $\log\Xi(z)$ is an even analytic function around $z = 0$, so all odd derivatives vanish:
   $$\boxed{\Sigma_{2m-1}^{\mathrm{sym}} := \lim_{T\to\infty} \sum_{|\gamma_\rho|\le T} \frac{1}{(\rho - 1/2)^{2m-1}} = 0 \qquad (\forall m \ge 1).}$$
2. **Even Centered Sums $\Sigma_{2m}$**:
   $$\boxed{\Sigma_{2m} := \sum_{\rho} \frac{1}{(\rho - 1/2)^{2m}} = -\frac{1}{(2m-1)!} \left.\frac{d^{2m}}{dz^{2m}} \log\Xi(z)\right|_{z=0}.}$$
   For $m = 1$ ($2m = 2$):
   $$\Sigma_2 = \sum_{\rho} \frac{1}{(\rho - 1/2)^2} = 8 - \frac{1}{4}\psi_1\!\left(\frac{1}{4}\right) - \left.\frac{d^2}{ds^2}\log(-\zeta(s))\right|_{s=1/2} \approx -0.04620998623083794157786762086067802800676,$$
   and for $m = 2$ ($2m = 4$):
   $$\Sigma_4 = \sum_{\rho} \frac{1}{(\rho - 1/2)^4} = -\frac{1}{6}\left.\frac{d^4}{dz^4}\log\Xi(z)\right|_{z=0} \approx +0.0000743451985705393723297325249434811569073.$$
   Note that while odd centered sums simplify to $0$, the even centered sums $\Sigma_{2m}$ involve $\zeta^{(k)}(1/2)/\zeta(1/2)$ and $\psi_{2m-1}(1/4)$ (e.g. $\psi_1(1/4) = \pi^2 + 8G$ with Catalan's constant $G$), which are not simpler arithmetically than the $s=0/1$ invariants $S_m$.
3. **Centered Symmetry-Quartet Polynomial (`centered_quartet_polynomial_identity` and `centered_quartet_coefficients_real` in Lean 4)**:
   For a full quartet $\{z, -z, \bar{z}, -\bar{z}\}$ with $z = \delta + i\gamma$, the monic quartet polynomial is:
   $$\boxed{Q_{\delta,\gamma}(X) = (X - z)(X + z)(X - \bar{z})(X + \bar{z}) = (X^2 - z^2)(X^2 - \bar{z}^2) = X^4 - 2(\delta^2 - \gamma^2)X^2 + (\delta^2 + \gamma^2)^2.}$$
   - The coefficients $c_2 = -2(\delta^2 - \gamma^2)$ and $c_0 = (\delta^2 + \gamma^2)^2$ are **always real** (`centered_quartet_coefficients_real`).
   - On the critical line ($\delta = 0$), $Q_{0,\gamma}(X) = (X^2 + \gamma^2)^2$.
   - The polynomial $Q_{\delta,\gamma}(X)$ has algebraic coefficients ($Q_{\delta,\gamma}(X) \in \overline{\mathbb{Q}}[X]$) if and only if $\delta^2 - \gamma^2 \in \overline{\mathbb{Q}}$ and $\delta^2 + \gamma^2 \in \overline{\mathbb{Q}}$, which (since $\delta, \gamma \in \mathbb{R}$) holds if and only if $\delta \in \overline{\mathbb{Q}}$ and $\gamma \in \overline{\mathbb{Q}}$, i.e., if and only if $\rho = \frac{1}{2} + \delta + i\gamma \in \overline{\mathbb{Q}}$.

---

## O. Li Coefficients and RH Firewall

The Keiper–Li coefficients (Keiper 1992; Li 1997; Bombieri–Lagarias 1999; Lagarias 2004 `arXiv:math/0404394v4`) are defined for $n \ge 1$ by:
$$\lambda_n := \sum_{\rho} \left[1 - \left(1 - \frac{1}{\rho}\right)^n\right] = \frac{1}{(n-1)!} \left.\frac{d^n}{ds^n} \left[s^{n-1}\log\xi(s)\right]\right|_{s=1}.$$
Expanding $(1 - 1/\rho)^n$ by the binomial theorem yields the exact finite polynomial relation in the reciprocal power sums $S_1, \dots, S_n$:
$$\boxed{\lambda_n = \sum_{j=1}^n (-1)^{j-1} \binom{n}{j} S_j.}$$
For $n = 1, 2, 3, 4$:
- $\lambda_1 = S_1 = 1 + \frac{\gamma_E}{2} - \log(2\sqrt{\pi}) \approx +0.0230957089661210338143102479065$,
- $\lambda_2 = 2S_1 - S_2 = 1 + \gamma_E - 2\log(2\sqrt{\pi}) - \gamma_E^2 + \frac{\pi^2}{8} - 2\gamma_1 \approx +0.0923457352280466703857284861921$,
- $\lambda_3 = 3S_1 - 3S_2 + S_3 \approx +0.2076389205543248037906597343219$,
- $\lambda_4 = 4S_1 - 6S_2 + 4S_3 - S_4 \approx +0.3687904794922416385931523699666$.

Notice that for $n = 1$, combining $(\rho, 1-\rho)$ gives the exact identity (formalized in Lean 4 as `li_first_coefficient_finite_algebra_identity`):
$$\left[1 - \left(1 - \frac{1}{\rho}\right)\right] + \left[1 - \left(1 - \frac{1}{1-\rho}\right)\right] = \frac{1}{\rho} + \frac{1}{1-\rho} = \frac{1}{\rho(1-\rho)}.$$

**Mandatory RH-Equivalence Firewall**:
By Li's Theorem (1997), $\lambda_n \ge 0$ for all $n \ge 1$ (or $\lambda_n > 0$ for all $n \ge 1$) is **logically equivalent to the Riemann Hypothesis**:
$$\boxed{\texttt{LI\_COEFFICIENT\_POSITIVITY\_IS\_RH\_EQUIVALENT}.}$$
Computing $\lambda_1, \dots, \lambda_N > 0$ for finitely many $N$ is a finite consequence of exact low-order derivatives of $\log\xi(s)$ at $s=1$ and **never** proves RH or individual-zero arithmetic properties.

---

## P. Superzeta / Zeta-of-Zeros Audit

We audited the primary literature on spectral zeta functions built over the nontrivial zeros (Voros 2003 `arXiv:math/0311029v1`; Voros 2010 monograph *Zeta Functions over Zeros of Zeta Functions*; Arias de Reyna `arXiv:1403.4558v2`; Cramér 1919; Guinand 1955):

1. **First-Kind Voros Superzeta Function**:
   $$\mathcal{Z}(s, v) := \sum_{\rho} \left(\frac{1}{2} + v - \rho\right)^{-s} = \sum_{k=1}^\infty \left(v - i\tau_k\right)^{-s} + \left(v + i\tau_k\right)^{-s} \qquad (\operatorname{Re}(s) > 1),$$
   where $\rho_k = \frac{1}{2} \pm i\tau_k$ ($\tau_k = -i(\rho_k - 1/2)$).
   - At $v = \frac{1}{2}$ and integer $s = m \ge 2$, $\mathcal{Z}(m, 1/2) = \sum_\rho (1-\rho)^{-m} = \sum_\rho \rho^{-m} = S_m$.
   - At $v = 0$ and even integer $s = 2m \ge 2$, $\mathcal{Z}(2m, 0) = (-1)^m \sum_\rho (\rho - 1/2)^{-2m} = (-1)^m \Sigma_{2m}$.
2. **Second-Kind Voros Superzeta Function**:
   $$\mathcal{Z}(s) := \sum_{k=1}^\infty \left(\tau_k^2\right)^{-s} = \sum_{k=1}^\infty \left(-\left(\rho_k - \frac{1}{2}\right)^2\right)^{-s} \qquad (\operatorname{Re}(s) > 1/2).$$
   - Meromorphically continued to $\mathbb{C}$ via Mellin–Barnes integrals of $\xi'(s)/\xi(s)$ (Voros `arXiv:0311029v1`), with poles at $s = \frac{1}{2} - n$ ($n \ge 0$) arising from the asymptotic Weyl–Riemann–von Mangoldt expansion of $N(T)$.
   - At positive integer arguments $s = m \in \mathbb{Z}_{\ge 1}$, $\mathcal{Z}(m) = \frac{1}{2}(-1)^m \Sigma_{2m}$, reducing to finite polynomials in the derivatives of $\log\Xi(z)$ at $z = 0$ (i.e. combinations of $\pi, \log 2, \psi_{2k-1}(1/4)$, and $\zeta^{(k)}(1/2)/\zeta(1/2)$).
3. **Verdict**: Superzeta functions package the exact symmetric invariants $S_m$ and $\Sigma_{2m}$ into a meromorphic generating family, **confirming that analytic continuation controls symmetric moments of the zero set without isolating or determining the arithmetic nature of any individual zero $\rho_n$**.

---

## Q. Arithmetic Status of Exact Zero-Sum Constants

| Invariant | Exact Closed-Form Expression | Rationality Known? | Irrationality Known? | Transcendence Known? | Main Unresolved Constants Included |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $S_1 = \lambda_1 = \sum_\rho^{\mathrm{sym}} \rho^{-1}$ | $1 + \frac{\gamma_E}{2} - \log(2\sqrt{\pi})$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\gamma_E$, $\log(2\sqrt{\pi})$ (though $\log(2\sqrt{\pi}) \notin \overline{\mathbb{Q}}$, its $\mathbb{Q}$-independence from $\gamma_E$ is open) |
| $\sum_\rho \frac{1}{\rho(1-\rho)} = 2S_1 = 2\lambda_1$ | $2 + \gamma_E - \log(4\pi)$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\gamma_E - \log(4\pi)$ |
| $S_2 = \sum_\rho \rho^{-2}$ | $1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\gamma_E$, $\gamma_1$ (first Stieltjes constant), $\pi^2$ |
| $S_3 = \sum_\rho \rho^{-3}$ | $1 - \frac{7}{8}\zeta(3) + \gamma_E^3 + 3\gamma_E\gamma_1 + \frac{3}{2}\gamma_2$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\zeta(3)$, $\gamma_E$, $\gamma_1$, $\gamma_2$ |
| $S_4 = \sum_\rho \rho^{-4}$ | $1 - \frac{\pi^4}{96} + \gamma_E^4 + 4\gamma_E^2\gamma_1 + 2\gamma_1^2 + 2\gamma_E\gamma_2 + \frac{2}{3}\gamma_3$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\pi^4$, $\gamma_E$, $\gamma_1, \gamma_2, \gamma_3$ |
| $\Sigma_2 = \sum_\rho (\rho-1/2)^{-2}$ | $8 - \frac{1}{4}\psi_1(1/4) - \left.\frac{d^2}{ds^2}\log(-\zeta(s))\right|_{s=1/2}$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | Catalan's constant $G$ (via $\psi_1(1/4) = \pi^2 + 8G$), $\zeta'(1/2)/\zeta(1/2)$, $\zeta''(1/2)/\zeta(1/2)$ |
| $\lambda_n$ ($n \ge 1$) | $\sum_{j=1}^n (-1)^{j-1}\binom{n}{j} S_j$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\gamma_E, \log(4\pi), \pi^{2k}, \zeta(2k+1), \gamma_1, \dots, \gamma_{n-1}$ |

---

## R. Current Status of $\zeta(5)$ and Odd Zeta Values

In accordance with Section 23 of `TASK-TC-038`, we performed a primary-source literature verification of the status of $\zeta(5)$ (`ZETA5_CURRENT_STATUS_VERIFIED`, `PRIMARY_SOURCE_VERIFIED`):

1. **Archimedean $\zeta(5) = \sum_{n=1}^\infty n^{-5} \in \mathbb{R}$**:
   - **Status**: **`OPEN_IN_LITERATURE`** (individual irrationality of Archimedean $\zeta(5)$ is **not** proved).
   - **Verification against recent preprints**: A July 2024 preprint by S. Suman (`arXiv:2407.07121` [math.GM], *"A note on the Irrationality of $\zeta(5)$ and Higher Odd Zeta Values"*) claimed to prove $\zeta(5) \notin \mathbb{Q}$; this claim was **explicitly refuted** in November 2024 by K. Chen, W. He, Y. He, Y. Huang, Y. Li, Q. Tang, L. Wu, S. Xu, S. Yang, and Z. Yu (`arXiv:2411.16774v3`, *"A Note on a Recent Attempt to Prove the Irrationality of $\zeta(5)$"*), who showed that the denominator estimate in Lemma 2.5 fails because $d_n \to \infty$. Furthermore, L. Lai, C. Lupu, and J. Sprang (May 2025, `arXiv:2505.23088v1`) explicitly reconfirm in their opening sentences that *"not even the irrationality of $\zeta(5)$ is known."*
2. **Exact Verified Theorems in Primary Literature on Odd Zeta Values**:
   - **Apéry (1979) / Beukers (1979)**: $\zeta(3) \notin \mathbb{Q}$ (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).
   - **Rivoal (2000, *C. R. Acad. Sci. Paris* 331, 267–270) & Ball–Rivoal (2001, *Invent. Math.* 146, 193–207)**:
     $$\dim_{\mathbb{Q}} \operatorname{span}_{\mathbb{Q}}\bigl(1, \zeta(3), \zeta(5), \dots, \zeta(2n+1)\bigr) \ge \frac{1 + o(1)}{1 + \log 2}\log n,$$
     so infinitely many odd zeta values $\zeta(2k+1)$ are irrational (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).
   - **Zudilin (2001, *Russ. Math. Surveys* 56(4), 149–150; 2002, *Izv. Math.* 66, 489–542; `arXiv:math/0104249v1`, `arXiv:math/0206176v2`)**: At least one of the four odd zeta values $\{\zeta(5), \zeta(7), \zeta(9), \zeta(11)\}$ is irrational (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).
   - **Rivoal–Zudilin (2018/2020, *Compos. Math.* 156; `arXiv:1803.03160v1`)**: At least two of $\{\zeta(5), \zeta(7), \dots, \zeta(69)\}$ are irrational (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).
   - **Fischler–Sprang–Zudilin (2019, *Compos. Math.* 155(5), 938–952; `arXiv:1803.08905v2`)**: At least $2^{(1-\varepsilon)\frac{\log s}{\log\log s}}$ odd zeta values up to $s$ are irrational (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).
   - **Lai–Sprang–Zudilin (May 2025, `arXiv:2505.05005v2`, *"A note on the irrationality of $\zeta_2(5)$"*)**: Building on Calegari–Dimitrov–Tang's holonomic proof of $\zeta_2(3) \notin \mathbb{Q}$, the **2-adic Kubota–Leopoldt zeta value** $\zeta_2(5) \in \mathbb{Q}_2$ is proved irrational (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).

**Classification**:
$$\boxed{\texttt{ZETA5\_CURRENT\_STATUS\_VERIFIED}.}$$

---

## S. Special-Value Method Transfer Test

### 1. Structural Comparison Table (Section 24)

| Feature | Special-Value Arithmetic ($\zeta(m)$ at $m \in \mathbb{Z}_{\ge 2}$) | Zero-Location Arithmetic ($\zeta(\rho) = 0$ in $0 < \operatorname{Re}(\rho) < 1$) |
| :--- | :--- | :--- |
| **Argument known?** | **Yes**: fixed positive integer $m \in \mathbb{Z}_{\ge 2}$ (known rational/integer input). | **No**: $\rho = \beta + i\gamma \in \{0 < \operatorname{Re}(s) < 1\}$ is the unknown target. |
| **Value known?** | **No**: $\zeta(m) \in \mathbb{R}$ is the unknown target whose irrationality is tested. | **Yes**: $\zeta(\rho) = 0$ is fixed identically to zero. |
| **Integral / series representation usable?** | **Yes**: Beukers hypercube integrals $\int_{[0,1]^m}$ and Ball–Rivoal hypergeometric series $\sum_{k=1}^\infty R_n(k)$ with integer pole multiplicity $m$. | **No**: $m$ enters as the integer dimension of $[0,1]^m$ or the integer pole order of $(k+j)^{-m}$ in partial-fraction decomposition; neither exists for non-integer complex $\rho$. |
| **Padé / linear-form construction target** | Linear form $L_n = A_n \zeta(m) + B_n$ (or $\sum_j A_{n,j}\zeta(2j+1) + B_n$) with $A_n, B_n \in \mathbb{Q}$ and denominator $d_n^m$. | Replacing $m \mapsto \rho$ in $A_n \zeta(\rho) + B_n$ gives $A_n \cdot 0 + B_n = B_n$, which eliminates $\zeta(\rho)$ completely and produces no small linear form in $\rho$. |
| **Algebraic-number input available?** | **Yes**: integer shifts $k+1, \dots, k+n \in \mathbb{Q}$ allow $\operatorname{lcm}(1,\dots,n)^m$ denominator control. | Only under a reductio assumption $\rho \in \overline{\mathbb{Q}}$, where $\rho$ appears in the exponent $k^{-\rho}$. |
| **Auxiliary polynomial target** | Rational function $R_n(t)$ with integer poles whose residues produce rational combinations of $\zeta(j)$. | Would require $P_n(X) \in \mathbb{Z}[X]$ with $0 < |P_n(\rho)| < C^{-n}$, which $\zeta(\rho) = 0$ does not generate. |

### 2. Method-by-Method Transfer Test (Section 25)
1. **Apéry (1979) / Beukers (1979) hypercube integral $I_n = \int_{[0,1]^m} \frac{P_n(x_1)\cdots P_n(x_m)}{1 - x_1\cdots x_m} dx_1\cdots dx_m$**:
   - *Object produced for $\zeta(m)$*: $I_n = A_n \zeta(m) - B_n$ with $d_n^m I_n \in \mathbb{Z}$ and $0 < |I_n| \to 0$ (for $m = 2, 3$).
   - *What fails when $m \mapsto \rho$*: The dimension $m$ of $[0,1]^m$ must be a positive integer; even in fractional Mellin form, $\zeta(\rho) = 0$ makes $A_n \zeta(\rho) - B_n = -B_n = O(1) \ne o(1)$.
2. **Ball–Rivoal (2001) / Zudilin (2001) / Fischler–Sprang–Zudilin (2019) hypergeometric series $\sum_{k=1}^\infty R_n(k)$**:
   - *Object produced for $\zeta(m)$*: $L_n = a_0 + \sum_{j=1}^s a_j \zeta(2j+1)$ via partial-fraction expansion of $R_n(t) = n!^{s-2r} \frac{\prod_{j=0}^{rn}(t-j)}{\prod_{j=0}^n (t+j)^s}$.
   - *What fails when $m \mapsto \rho$*: The partial-fraction decomposition into Hurwitz shifts $\sum_{k=1}^\infty (k+j)^{-m}$ requires $m \in \{1, \dots, s\}$ to be a **positive integer pole multiplicity** of $(t+j)^{-s}$; a complex zero $\rho$ cannot serve as a rational-function pole multiplicity.
3. **Brown (2014/2016) moduli space $\mathcal{M}_{0,n}$ period integrals**:
   - *Object produced for $\zeta(m)$*: Motivic period linear forms in multiple zeta values of integer weight.
   - *What fails when $m \mapsto \rho$*: $\mathcal{M}_{0,n}$ periods are algebraic-geometric periods of mixed Tate motives over $\mathbb{Z}$ (integer weights only); critical-strip zeros $\rho$ are not weights of mixed Tate motives.
4. **Calegari–Dimitrov–Tang (2024) / Lai–Sprang–Zudilin (2025) 2-adic holonomic method for $\zeta_2(5)$**:
   - *Object produced for $\zeta_2(5)$*: 2-adic rational approximations $p_n/q_n$ to $\zeta_2(5)$ in $\mathbb{Q}_2$.
   - *What fails when $m \mapsto \rho$*: Constructs $p$-adic linear forms in fixed integer-weight $p$-adic zeta values; does not act on Archimedean critical-strip zero arguments $\rho$.

**Classification**:
$$\boxed{\texttt{SPECIAL\_VALUE\_IRRATIONALITY\_METHOD\_HAS\_NO\_DIRECT\_ZERO\_LOCATION\_TRANSFER}.}$$

---

## T. Auxiliary-Polynomial Requirements for $\rho_1$ and $\gamma_1$

To prove that $\alpha \in \{\rho_1, \gamma_1\}$ is irrational or transcendental via an auxiliary polynomial sequence $P_n(X) \in \mathbb{Z}[X]$, five mathematical ingredients are strictly required:
1. A sequence of nonzero integer polynomials $P_n(X) \in \mathbb{Z}[X] \setminus \{0\}$ of degree $d_n \le D_n$ and height $H(P_n) \le e^{h_n}$.
2. **Nonvanishing certificate**: $P_n(\alpha) \ne 0$ for infinitely many $n$.
3. **Analytic upper bound**: $|P_n(\alpha)| \le \exp(-U_n)$ derived from an analytic identity (such as Cauchy/Schwarz/Jensen on an auxiliary entire function with high-order zeros).
4. **Liouville / Mahler algebraic lower bound**: If $\alpha \in \overline{\mathbb{Q}}$ has degree $d = [\mathbb{Q}(\alpha):\mathbb{Q}]$ and Mahler measure $M(\alpha)$, then $P_n(\alpha) \ne 0$ implies
   $$|P_n(\alpha)| \ge (d_n + 1)^{-(d-1)} H(P_n)^{-(d-1)} M(\alpha)^{-d_n d}.$$
5. **Asymptotic contradiction inequality**: $U_n > (d-1)h_n + d \log M(\alpha) \cdot d_n$ as $n \to \infty$.

**Why $\zeta(\rho_1) = 0$ and $\Xi(i\gamma_1) = 0$ do not supply $P_n(X) \in \mathbb{Z}[X]$**:
- Truncating the Taylor series of $\xi(s)$ or $\zeta(s)$ produces polynomials whose coefficients involve $\log\pi, \gamma_E$, and the Stieltjes constants $\gamma_k$ (which are transcendental/unknown, not in $\mathbb{Z}$ or $\overline{\mathbb{Q}}$).
- Truncating the Dirichlet series $\sum_{m=1}^N m^{-s}$ produces Dirichlet polynomials in $p^{-s} = e^{-s\log p}$, not algebraic polynomials in $s$, and $\sum_{m=1}^N m^{-\rho_1}$ does not converge to $0$ in $0 < \operatorname{Re}(s) < 1$.
- Replacing $\rho_1$ by $\gamma_1$ via $\Xi(i\gamma_1) = \sum_{m=0}^\infty c_{2m}\gamma_1^{2m} = 0$ has Taylor coefficients $c_{2m} = (-1)^m \frac{\Xi^{(2m)}(0)}{(2m)!}$ which are themselves unknown transcendental combinations (related to $\Sigma_{2m}$), so neither $\rho_1$ nor $\gamma_1$ is privileged with an integer-coefficient auxiliary polynomial construction.

---

## U. Gamma and Differential-Transcendence Firewalls

### 1. Gamma-Function Arithmetic Firewall (Section 28)
In $\xi(s) = \frac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$:
- $\Gamma(s/2)$ has **no zeros anywhere in $\mathbb{C}$** ($\frac{1}{\Gamma(z)}$ is entire) and its poles lie at $s \in \{0, -2, -4, -6, \dots\}$, which are disjoint from the critical strip $0 < \operatorname{Re}(s) < 1$.
- Consequently, inside $0 < \operatorname{Re}(s) < 1$, the factor $\frac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)$ is **everywhere finite and nonvanishing**, so:
  $$\xi(\rho) = 0 \iff \zeta(\rho) = 0 \qquad (0 < \operatorname{Re}(\rho) < 1).$$
- Whether $\Gamma(\rho/2)$ is transcendental or unknown at $\rho \in \overline{\mathbb{Q}}$ does **not** create any obstruction to $\zeta(\rho) = 0$, because a nonzero transcendental prefactor multiplied by $0$ equals $0$.

### 2. Differential-Transcendence Firewall (Section 29)
By Hölder (1887) for $\Gamma(s)$ and Hilbert (1900) / Ostrowski (1920) for $\zeta(s)$, neither $\Gamma(s)$ nor $\zeta(s)$ satisfies any nontrivial algebraic differential equation $P(s, f(s), f'(s), \dots, f^{(k)}(s)) = 0$ over $\mathbb{C}[s]$.

**Explicit Counterexample Proving Differential Transcendence Does Not Forbid Algebraic Zeros**:
Since $\Gamma(s)$ is differentially transcendental over $\mathbb{C}(s)$ and its reciprocal $1/\Gamma(s)$ is entire, the function
$$g(s) := \frac{1}{\Gamma(s)}$$
is an entire differentially transcendental function (if $g$ satisfied an algebraic ODE over $\mathbb{C}(s)$, then $\Gamma = 1/g$ would also satisfy an algebraic ODE over $\mathbb{C}(s)$, contradicting Hölder's theorem). Yet the zero set of $g(s)$ is
$$\{s \in \mathbb{C} : g(s) = 0\} = \{0, -1, -2, -3, \dots\} \subset \mathbb{Z} \subset \mathbb{Q} \subset \overline{\mathbb{Q}},$$
consisting **entirely of rational integers**! More generally, for any algebraic number $\alpha \in \overline{\mathbb{Q}}$, $f_\alpha(s) := (s - \alpha)\zeta(s)$ is differentially transcendental over $\mathbb{C}(s)$ and vanishes at the algebraic point $s = \alpha$.

**Classification**:
$$\boxed{\texttt{DIFFERENTIAL\_TRANSCENDENCE\_DOES\_NOT\_DETERMINE\_ZERO\_ARITHMETIC}.}$$

---

## V. Certified Finite Polynomial and Bounded-Denominator Exclusions

All finite computational exclusions are executed in 128-bit outward Arb/Acb ball arithmetic (`tc/zero_arithmetic_invariants.py`) and strictly separated from analytic proofs.

### 1. Certified First-Zero Enclosures (128-bit Arb IVT)
Using the real critical-line Hardy/xi function $\operatorname{Re}(\pi^{-it/2}\Gamma(1/4 + it/2)\zeta(1/2 + it))$, 128-bit Arb certifies a strict sign change across $[\gamma_1 - 10^{-30}, \gamma_1 + 10^{-30}]$, giving the certified outward enclosures:
- $\gamma_1 \in [14.134725141734693790457251983562470270784257115699 \pm 10^{-30}]$,
- $\gamma_1 + \frac{1}{2} \in [14.634725141734693790457251983562470270784257115699 \pm 10^{-30}]$,
- $\rho_1 = \frac{1}{2} + i\gamma_1$.

### 2. Polynomial Normalization Rules (Section 31)
Every candidate polynomial $P(X) = a_0 + a_1 X + \dots + a_d X^d \in \mathbb{Z}[X]$ is normalized so that:
- $1 \le d \le D$ with leading coefficient $a_d \ge 1$ ($a_d > 0$),
- $\max_{0 \le j \le d} |a_j| \le H$,
- $\gcd(|a_0|, |a_1|, \dots, |a_d|) = 1$,
- the zero polynomial is excluded.

### 3. Certified Finite Algebraic-Relation Exclusion (`CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION`)
1. **Explicit Individual Enumeration ($D = 4, H = 3$)**:
   All $8{,}160$ normalized primitive polynomials with $1 \le d \le 4$ and $H \le 3$ are evaluated individually in 128-bit Arb/Acb arithmetic on $\gamma_1$, $\gamma_1 + 1/2$, and $\rho_1$:
   - $\min_{P} |P(\gamma_1)|_{\text{lower}} = 11.134725141734695 > 0$,
   - $\min_{P} |P(\gamma_1 + 1/2)|_{\text{lower}} = 11.634725141734695 > 0$,
   - $\min_{P} |P(\rho_1)|_{\text{lower}} = 14.143565845725995 > 0$.
2. **Full $D \le 4, H \le 100$ Outward Arb/Acb Box+Leaf Certificate**:
   Across all $158{,}062{,}321{,}920$ normalized primitive integer polynomials with $1 \le d \le 4$ and $\max_j |a_j| \le 100$ ($12{,}175$ for $d=1$; $3{,}355{,}121$ for $d=2$; $749{,}507{,}743$ for $d=3$; $157{,}309{,}446{,}881$ for $d=4$):
   - **For $\gamma_1$**: Certified $0 \notin P(I_{\gamma_1})$ for all $158{,}062{,}321{,}920$ primitive polynomials, with global minimum certified lower bound:
     $$\min_{\substack{1 \le d \le 4 \\ H(P) \le 100}} |P(\gamma_1)| \ge 9.15045298643503 \times 10^{-6} > 0 \quad \text{at } P(X) = 6X^4 - 82X^3 - 45X^2 + 73X + 28.$$
   - **For $\gamma_1 + 1/2$**: Certified $0 \notin P(I_{\gamma_1+1/2})$ for all $158{,}062{,}321{,}920$ primitive polynomials, with global minimum certified lower bound:
     $$\min_{\substack{1 \le d \le 4 \\ H(P) \le 100}} |P(\gamma_1 + 1/2)| \ge 1.57896475847535 \times 10^{-5} > 0 \quad \text{at } P(X) = 3X^4 - 49X^3 + 69X^2 + 76X + 82.$$
   - **For $\rho_1 = 1/2 + i\gamma_1$**: Certified $0 \notin P(I_{\rho_1})$ for all $158{,}062{,}321{,}920$ primitive polynomials, with global minimum certified lower bound:
     $$\min_{\substack{1 \le d \le 4 \\ H(P) \le 100}} |P(\rho_1)| \ge 0.571817936443205 > 0 \quad \text{at } (a_0, a_1, a_2, a_3, a_4) = (0, 100, 99, 1, 0).$$

### 4. Certified Bounded-Denominator Rational Exclusion (`CERTIFIED_BOUNDED_DENOMINATOR_RATIONAL_EXCLUSION`)
Across all rational numbers $p/q$ with $1 \le q \le 10{,}000$ and $p \in \mathbb{Z}$, 128-bit Arb certifies $0 \notin q I_{\gamma_1} - p$ and $0 \notin q I_{\gamma_1+1/2} - p$:
$$\min_{\substack{1 \le q \le 10000 \\ p \in \mathbb{Z}}} \left|\gamma_1 - \frac{p}{q}\right| \ge 9.50797348022772 \times 10^{-10} > 0 \quad \text{at } \frac{p}{q} = \frac{94109}{6658},$$
$$\min_{\substack{1 \le q \le 10000 \\ p \in \mathbb{Z}}} \left|\left(\gamma_1 + \frac{1}{2}\right) - \frac{p}{q}\right| \ge 9.50797348022772 \times 10^{-10} > 0 \quad \text{at } \frac{p}{q} = \frac{48719}{3329}.$$

### 5. Diagnostic PSLQ Firewall (`NUMERICAL_EVIDENCE_ONLY`)
An 80-digit `mpmath.pslq` diagnostic check on $[1, \gamma_1, \dots, \gamma_1^4]$ and $[1, \gamma_1 + 1/2, \dots, (\gamma_1 + 1/2)^4]$ with `maxcoeff=1000` returns `None` (no relation found). In strict compliance with Section 33, this is classified solely as `NUMERICAL_EVIDENCE_ONLY` and never promoted to a mathematical proof or certified exclusion.

---

## W. TC Interaction and Ambient-Kernel Firewall

We audited whether an assumed algebraic zero $\rho \in \overline{\mathbb{Q}}$ or algebraic ordinate $\gamma \in \overline{\mathbb{Q}}$ interacts with the TC ambient kernel or the exceptional exponent set
$$\mathcal{S}_\tau := \left\{\alpha \in \mathbb{A}_{\mathbb{R}} : \tau^\alpha \in \overline{\mathbb{Q}}\right\}, \qquad \mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}, \qquad \tau = 2\pi.$$

1. **Complex-Exponent Domain Firewall (Section 36)**:
   The canonical TC grade variable lives in $\mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$, where $\tau^K \in \mathbb{R}_{>0}$ is a positive real scale. When $\rho = \beta + i\gamma$ is a nontrivial zero ($\gamma \ne 0$), the product $K\rho = K\beta + iK\gamma \notin \mathbb{R}$ is non-real for every $K \in \mathbb{A}_{\mathbb{R}} \setminus \{0\}$, so $\tau^{K\rho} = \tau^{K\beta} e^{i K\gamma \log\tau}$ is **not** a positive real ambient grade.
2. **Real Exponents Tested Under $\rho \in \overline{\mathbb{Q}}$ (Section 37)**:
   If $\rho = \beta + i\gamma \in \overline{\mathbb{Q}}$, then $\beta, \gamma, \delta = \beta - 1/2 \in \mathbb{A}_{\mathbb{R}}$. However:
   - $\zeta(\rho) = 0$ imposes **no** algebraic relation on $\tau^\beta$, $\tau^\gamma$, or $\tau^{2\delta_\rho}$,
   - As established in `TASK-TC-037` / `TASK-TC-037R`, the diagonal grade character $q_{\rho,\rho} = \tau^{2\delta_\rho}$ is nonunitary when $\delta_\rho \ne 0$, and no zero-independent arithmetic identity forces $\tau^{2\delta_\rho} \in \overline{\mathbb{Q}}$.

**Classification**:
$$\boxed{\texttt{ALGEBRAIC\_ZERO\_DOES\_NOT\_AUTOMATICALLY\_ENTER\_AMBIENT\_KERNEL}.}$$

---

## X. Exact Remaining Subgate for `TASK-TC-039`

1. **Primary TC Obligation**: `OBL-CT-001A = OPEN` remains unchanged; `TASK-TC-038` is recorded as a distinct `ZERO_ARITHMETIC_BRANCH`.
2. **Answer to the Governing Question**:
   Current analytic and Diophantine methods control **only global symmetric invariants of the zero set** ($S_m = \sum_\rho \rho^{-m}$, the reflection-invariant sum $\sum_\rho \frac{1}{\rho(1-\rho)} = 2S_1 = 2\lambda_1$, the centered sums $\Sigma_{2m}$, the Li coefficients $\lambda_n$, and Voros superzeta values), while **no established transcendence theorem interacts strongly enough with $\zeta(\rho) = 0$ in $0 < \operatorname{Re}(\rho) < 1$ to exclude algebraicity or rationality of any individual zero ordinate $\gamma_n$**.
3. **Strongest Exact Zero-Sum Invariant Isolated**:
   The absolutely convergent reflection-invariant reciprocal sum
   $$\sum_{\rho} \frac{1}{\rho(1-\rho)} = 2 S_1 = 2\lambda_1 = 2 + \gamma_E - \log(4\pi),$$
   together with the absolutely convergent second reciprocal power sum
   $$S_2 = \sum_{\rho} \frac{1}{\rho^2} = 1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1.$$
4. **Single Smallest Missing Theorem (`SUBGATE-TC-038A`) for `TASK-TC-039`**:
   $$\boxed{\texttt{SUBGATE-TC-038A}: \quad \text{Prove irrationality of } 2\lambda_1 = 2 + \gamma_E - \log(4\pi) \;\text{(equivalently } \gamma_E - \log(4\pi) \notin \mathbb{Q}\text{)}, \text{ or prove } \dim_{\mathbb{Q}}\operatorname{span}_{\mathbb{Q}}(1, S_1, S_2) \ge 2.}$$

---

## Y. Complete Modified-File Inventory

| File | Role in `TASK-TC-038` |
| :--- | :--- |
| `formal/RiemannScope/ZeroArithmeticInvariants.lean` | Lean 4 formalization of all 9 required zero-arithmetic and symmetric zero-sum theorems (`10` `theorem` declarations total; `0 sorry, 0 admit, no nonstandard project axioms introduced`). |
| `formal/RiemannScope.lean` | Root Lean import adding `RiemannScope.ZeroArithmeticInvariants`. |
| `formal/RiemannScope/README.md` | Module documentation and theorem inventory updated (`624` total compiled `theorem` declarations across `30` modules). |
| `tc/zero_arithmetic_invariants.py` | Complete Python implementation of candidate classification, shifted-ordinate redundancy, primary-source literature & transcendence audits, symbolic/mpmath derivations of $S_1, S_2, S_3, S_4, \Sigma_{2m}, \lambda_n$, $\zeta(5)$ & special-value transfer audit, and 128-bit Arb finite polynomial/rational exclusions. |
| `tc/grade_character_projection.py` | Preflight `TASK-TC-037R` status repair (`INVERSION_EVEN_MELLIN_ZERO_FREE_STRIP_FALSE`, `STRICT_REFLECTION_WEIGHT_AT_ZETA_ZERO_ORDINATES_OPEN`, synchronized witness $(0.25, 1.0)$). |
| `tc/__init__.py` | Package exports for `tc.zero_arithmetic_invariants` and updated `TASK-TC-037R` status tokens. |
| `data/tc_zero_arithmetic_invariants.json` | Machine-readable artifact containing all 35 required keys for `TASK-TC-038`. |
| `data/tc_grade_character_projection.json` | Updated `TASK-TC-037R` artifact with repaired Mellin-strip status and $(0.25, 1.0)$ witness. |
| `docs/reviews/TC_ZERO_ARITHMETIC_INVARIANTS.md` | This comprehensive mathematical and primary-literature audit report (Sections A–Y). |
| `docs/reviews/TC_GRADE_CHARACTER_REFLECTION_PROJECTION.md` | Synchronized `TASK-TC-037R` review report. |
| `docs/TC_CURRENT_CANONICAL_STATUS.md` | Canonical status updated with `TASK-TC-037R` housekeeping and `TASK-TC-038` (`ZERO_ARITHMETIC_BRANCH`). |
| `MATH_CONTRACT.md` | Contract addendum for `TASK-TC-038` and `TASK-TC-037R` status synchronization. |
| `TRANSCENDENTAL_CONTINUATION.md` | Programme ledger updated for `TASK-TC-038` and `TASK-TC-037R` status repair. |
| `CURVATURE_TRANSPORT.md` | Synchronized `TASK-TC-037R` status tokens and $(0.25, 1.0)$ witness. |
| `ARITHMETIC_RADIAL_BRIDGE.md` | Synchronized `TASK-TC-037R` status tokens and $(0.25, 1.0)$ witness. |
| `CMSA_GATE_G4.md` | Synchronized `TASK-TC-037R` status tokens and $(0.25, 1.0)$ witness. |
| `RESEARCH_HYPOTHESIS.md` | Updated with `TASK-TC-038` (`ZERO_ARITHMETIC_BRANCH`) and `TASK-TC-037R` status repair. |
| `RESEARCH_LEDGER.md` | Updated with `TASK-TC-038` ledger entry and `TASK-TC-037R` status repair. |
| `.agents/corpus_map/obligation_register.md` | Updated with `SUBGATE-TC-038A` (`ZERO_ARITHMETIC_BRANCH`) while preserving `OBL-CT-001A = OPEN`. |
| `.agents/research/state.json` | Updated active sprint state to `TASK-TC-038`. |
| `.agents/research/queue.json` | Marked `TASK-TC-038` completed and queued `SUBGATE-TC-038A`. |
| `tests/test_tc_zero_arithmetic_invariants.py` | Comprehensive pytest suite covering all 32 required tests from Section 45. |
| `tests/test_tc_grade_character_projection.py` | Updated for `INVERSION_EVEN_MELLIN_ZERO_FREE_STRIP_FALSE` and `STRICT_REFLECTION_WEIGHT_AT_ZETA_ZERO_ORDINATES_OPEN`. |
