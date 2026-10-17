# TASK-TC-038R Repair — Zero-Arithmetic Evidence, $\zeta(5)$-2026, and Formal-Provenance Repair

**Repository**: `tsolomon89/reimann_scope`  
**Task ID**: `TASK-TC-038R` (repairing and extending `TASK-TC-038`)  
**Branch Classification**: `ZERO_ARITHMETIC_BRANCH`  
**Starting HEAD**: `92d14a77b93e974658c2b5596a69a1f63a64727f`  
**Substantive `TASK-TC-038` Commit**: `4576c23c38af0224a0f8ddd59fdd922aebab1a0e`  
**Principal Classification**: `ZERO_ARITHMETIC_FRONTIER_CLASSIFIED_INDIVIDUAL_STATUS_OPEN`  
**Secondary Transfer Classification**: `FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED` (`SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT_REPAIRED`)  
**Remaining Zero-Arithmetic Subgates**: `SUBGATE-TC-038A = OPEN` (`ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE`), `SUBGATE-TC-039A = OPEN` (`FAUZAN_HANKEL_TO_ZERO_ARGUMENT_TRANSFER_SUBGATE`)  
**Primary TC Obligation Status**: `OBL-CT-001A = OPEN`  

---

## A. Executive Repair Verdict

`TASK-TC-038R` resolves all six post-sprint review defects identified in `TASK-TC-038`:

1. **2026 Archimedean $\zeta(5)$ Status & Evidence Taxonomy Repaired**:
   We incorporate Aabir Fauzan's 17 September 2026 preprint (*"$\zeta(5)$ is irrational"*, Zenodo record `22826419`, DOI `10.5281/zenodo.22826419`) and public Lean 4 formalization `mo271/Zeta5` (commit `7fe736760f4b96bfdb4334b68e3b3124ecbe10b0`), strictly separating four distinct evidence dimensions:
   - Manuscript claim: `ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM` (`ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM_VERIFIED`),
   - Public Lean 4 formalization: `ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN` (`LEAN_PROVED_EXTERNAL_REPOSITORY`, `SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED`),
   - Transitive axiom and proof-hole audit: `ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN` (`[propext, Classical.choice, Quot.sound]`, `0 sorry`, `0 admit`, `0 axiom` across all 251 `.lean` files in `Apery/` and `Solution.lean`),
   - Conventional journal peer-review status: `ZETA5_CONVENTIONAL_PEER_REVIEW_STATUS_RECORDED` (`PEER_REVIEW_STATUS_PENDING`).
2. **2026 Hankel-Determinant Transfer Audit & `SUBGATE-TC-039A`**:
   The blanket `TASK-TC-038` transfer verdict (`SPECIAL_VALUE_IRRATIONALITY_METHOD_NO_DIRECT_ZERO_LOCATION_TRANSFER`) is restricted to classical hypergeometric/Beukers/motivic/2-adic methods and replaced at the frontier by:
   $$\boxed{\texttt{SPECIAL\_VALUE\_TRANSFER\_REQUIRES\_2026\_HANKEL\_AUDIT\_REPAIRED} \;\longrightarrow\; \texttt{FAUZAN\_HANKEL\_ZERO\_LOCATION\_TRANSFER\_UNRESOLVED}.}$$
   We establish the structural distinction:
   $$\boxed{\texttt{VALUE\_POLYNOMIAL\_ARCHITECTURE\_NEQ\_ARGUMENT\_POLYNOMIAL\_ARCHITECTURE}:}$$
   Fauzan's determinant $\Delta_K(X) = \det_{0 \le i,j < 37n} \mu_X(D_N(t)^6 t^{i+j} / D_K(t))$ constructs an auxiliary polynomial $Q_n(X) \in \mathbb{Z}[X]$ in a **value variable** $X$ evaluated at $X = \zeta(5)$ (entering affinely in the pole functional $\mu_X(1/(t+j^2)) = j^4(X - H_j^{(5)}) - 1/4 + 1/(2j)$), whereas for a nontrivial zero $\rho_1 = \beta_1 + i\gamma_1$, the value $\zeta(\rho_1) = 0$ is already zero and the target $\alpha \in \{\gamma_1, \rho_1\}$ is the **argument** entering nonlinearly inside $n^{-\rho_1}$, $\Gamma(\rho_1/2)$, or $(y^2 + z_{\rho_1}^2)^{-1}$. We isolate the 6-gate architecture `Z1`–`Z6` under `SUBGATE-TC-039A` for `TASK-TC-039`.
3. **Formal Build Provenance Synchronized (`FORMAL_SOURCE_INVENTORY_REPAIRED`)**:
   `"formal/RiemannScope/ZeroArithmeticInvariants.lean"` is added to both `scripts/build_formal.py::FORMAL_SOURCE_FILES` and `certification.py::REQUIRED_FORMAL_SOURCES`, two new algebraic cleanup theorems (`stieltjes_notation_no_effect_algebra`, `s2_equivalent_closed_forms`) are formalized and compiled (`lake build RiemannScope.ZeroArithmeticInvariants`), an automated inventory-synchronization guard is added to `tc/zero_arithmetic_invariants.py` and `tests/test_tc_zero_arithmetic_invariants.py`, and the repository's exact theorem count is updated to **`626`** compiled `theorem` declarations across `30` formal source files (`12` `theorem` declarations and `4` `def` declarations in `ZeroArithmeticInvariants.lean`).
4. **Stieltjes Notation Disambiguated & Canonical $S_2, S_3, S_4$ Formulas Repaired**:
   All zero-sum formulas now write $\gamma_n = \operatorname{Im}(\rho_n)$ exclusively for zero ordinates, $\gamma_E = \gamma_0^{\mathrm{St}}$ for the Euler–Mascheroni constant, and $\gamma_1^{\mathrm{St}}, \gamma_2^{\mathrm{St}}, \gamma_3^{\mathrm{St}}$ for the Stieltjes constants (`STIELTJES_NOTATION_DISAMBIGUATED`). The erroneous historical formula $S_2 = 1 - \frac{\pi^2}{8} + \gamma_{\mathrm{Euler}} + \frac{\gamma_{\mathrm{Euler}}^2}{4} - \gamma_1^{\mathrm{Stieltjes}}$ (which evaluated to $+0.678896\dots$, differing from the true $S_2 = -0.0461543\dots$ by $0.7250507$) is purged from `RESEARCH_HYPOTHESIS.md` and `RESEARCH_LEDGER.md` (`S2_CANONICAL_FORMULA_REPAIRED`), and $S_3, S_4$ are re-verified via three independent routes (`S3_S4_REAUDITED`).
5. **Finite-Exclusion Certification Scope Repaired (`FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED`)**:
   Following Route A (Section 20.1), for the hierarchically pruned box $D \le 4, H \le 100$ ($158{,}062{,}321{,}920$ normalized primitive polynomials), we claim only `CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION` ($0 \notin P(I)$ for all $P$ in the box) under method `HIERARCHICAL_BOX_EXCLUSION` and explicitly set `FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED`, removing the uncertified full-box $\min |P|$ claims (`9.15045e-6`, `1.57896e-5`, `0.571818`) from all prose and artifacts. Certified full-box global minima are reported solely for the exhaustively enumerated box $D \le 4, H \le 3$ ($8{,}160$ polynomials, `EXPLICIT_POLYNOMIAL_ENUMERATION`).
6. **Cardinality & Fixed-Number-Field Northcott Scope Repaired**:
   The misleading "transcendence by cardinality" row is removed from the individual-zero literature table (`CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE`, `NO_INDIVIDUAL_ORDINATE_IRRATIONALITY_OR_TRANSCENDENCE_THEOREM_FOUND`), and Northcott finiteness in a fixed number field $K$ is explicitly qualified as requiring **both bounded degree $[K:\mathbb{Q}] \le D$ and bounded height $H \le H_0$** (`FIXED_NUMBER_FIELD_REQUIRES_BOUNDED_DEGREE_AND_BOUNDED_HEIGHT`).

---

## B. 2026 $\zeta(5)$ Status and Evidence Taxonomy

The `TASK-TC-038` report stated that individual Archimedean $\zeta(5)$ irrationality was open based on preprints through May 2025. Re-auditing the primary literature and public formalization repositories through October 2026 establishes the following four-part taxonomy (never collapsed into a binary status):

| Dimension | Classification Token | Evidence Class / Scope | Verified Facts |
| :--- | :--- | :--- | :--- |
| **1. 2026 Manuscript Claim** | `ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM` (`ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM_VERIFIED`) | `PRIMARY_SOURCE_VERIFIED` | Aabir Fauzan (Aalto University), *"$\zeta(5)$ is irrational"*, 17 September 2026, Zenodo record `22826419`, DOI `10.5281/zenodo.22826419` (`ZETA5_IS_IRRATIONAL.pdf`). Claims Theorem 1.1 ($\zeta(5) \notin \mathbb{Q}$ with irrationality measure $|\zeta(5) - a/b| > b^{-260}$ for $b \gg 1$) and Theorem 2.1 ($\exists Q_n \in \mathbb{Z}[X]$, $\deg Q_n = 37n$, $0 < Q_n(\zeta(5)) < \exp(-139n^2/5)$). |
| **2. Public Lean 4 Formalization** | `ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN` | `LEAN_PROVED_EXTERNAL_REPOSITORY` / `SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED` | Repository `https://github.com/mo271/Zeta5` at commit `7fe736760f4b96bfdb4334b68e3b3124ecbe10b0` (`leanprover/lean4:v4.34.0-rc1`, `mathlib` `f385f9fd18abed332ebcd3df239cb357e264aceb`, `PrimeNumberTheoremAnd` `04d81b2a68ea3548b9990813fdc463c78511f412`). Exports `Apery.irrational_zeta5 : Irrational Apery.zeta5` (`Apery/Main.lean`), `Apery.irrational_five : ∃ x, Irrational x ∧ riemannZeta 5 = x` (`Apery/Main.lean`), and `RiemannZetaValues.irrational_five : ∃ x, Irrational x ∧ riemannZeta 5 = x` (`Solution.lean`), bridged to Mathlib's `riemannZeta 5` via `Apery.riemannZeta_five : riemannZeta 5 = (Apery.zeta5 : ℂ)` (`Apery/Zeta5.lean`). |
| **3. Dependency & Axiom Graph** | `ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN` | `PRIMARY_SOURCE_VERIFIED` | Direct audit of all 251 `.lean` files in `Apery/` and `Solution.lean` confirms `0 sorry`, `0 admit`, `0 axiom`, `0 unsafe`, `0 @[implemented_by]`. `#print axioms Apery.irrational_five` outputs `[propext, Classical.choice, Quot.sound]`, and `.github/workflows/ci.yml` runs `leanprover/comparator` (`config.json`) against `google-deepmind/formal-conjectures` permitting only `["propext", "Classical.choice", "Quot.sound"]`. (The single `sorry` in `Challenge.lean` is the benchmark target statement discharged by `Solution.lean`; the 2 `sorry`s in `PrimeNumberTheoremAnd/Wiener.lean` are outside the import cone of `Apery/PNT.lean`, which uses only `PrimeNumberTheoremAnd.Consequences.chebyshev_asymptotic`.) |
| **4. Conventional Peer Review** | `ZETA5_CONVENTIONAL_PEER_REVIEW_STATUS_RECORDED` (`PEER_REVIEW_STATUS_PENDING`) | `PRIMARY_SOURCE_VERIFIED` | As of October 2026, Fauzan's manuscript is a Zenodo preprint accompanied by the machine-checked `mo271/Zeta5` Lean 4 repository; conventional journal peer-review publication is pending. |

---

## C. Fauzan / `mo271/Zeta5` Architecture Summary

The complete mathematical and formal architecture is stored in `data/fauzan_zeta5_architecture.json` (20 top-level schema keys). Its six core steps are:

1. **Parameters & Node Polynomials (`Apery/Construction.lean`)**:
   For $n \ge 1$, set
   $$K = 40n, \qquad N = 3n, \qquad h = K - N = 37n, \qquad D_m(t) = \prod_{j=1}^m (t + j^2) \in \mathbb{Q}[t].$$
2. **Rational Moment Functional $\mu_X$ & Hankel Matrix $G_K(X)$ (`Apery/Construction.lean`)**:
   Define a $\mathbb{Q}$-linear functional $\mu_X$ on rational functions $P(t)/D_K(t)$ (decomposed by polynomial division and partial fractions at $t = -j^2$, $1 \le j \le K$) by:
   $$\mu(t^e) := (-1)^e B_{2e+2} \frac{(2e+3)(2e+4)(2e+5)}{24} \in \mathbb{Q}, \qquad \mu_X\!\left(\frac{1}{t+j^2}\right) := j^4\!\left(X - H_j^{(5)}\right) - \frac{1}{4} + \frac{1}{2j} \in \mathbb{Q}[X],$$
   where $H_j^{(5)} = \sum_{v=1}^j v^{-5}$. Form the $h \times h$ ($37n \times 37n$) Hankel matrix and its determinant:
   $$G_K(X)_{i,j} := \mu_X\!\left(\frac{D_N(t)^6 t^{i+j}}{D_K(t)}\right) \quad (0 \le i,j < h), \qquad \Delta_K(X) := \det G_K(X) \in \mathbb{Q}[X], \qquad F_K(X) := S_K \Delta_K(X),$$
   where $S_K = \frac{(K!)^{2h} 4^{h-1}}{(N!)^{12h} \prod_{i=1}^{h-1} ((2i)!)^2}$.
3. **Exact Degree $\deg F_K(X) = 37n$ (`Apery/Degree.lean`, `Apery.natDegree_F`)**:
   Because $D_N(-j^2) = 0$ for $1 \le j \le N$, $X$ enters $G_K(X)_{i,j}$ only via the $h = K - N$ simple poles $N < j \le K$, and each entry is affine in $X$. The coefficient of $X^h$ in $\Delta_K(X)$ is $\det(V^T \operatorname{diag}(w_k) V) = (\det V)^2 \prod_{k=0}^{h-1} w_k \ne 0$ at distinct nodes $x_k = -(N+1+k)^2$ with nonzero weights $w_k = D_N(x_k)^6 (N+1+k)^4 / D_K'(x_k)$, proving $\deg \Delta_K = \deg F_K = h = 37n$.
4. **Hermite Identity & Gram Positivity at $X = \zeta(5)$ (`Apery/HermiteFormula.lean`, `Apery/Positivity.lean`)**:
   With the positive Bose–Einstein derivative weight
   $$w(y) := \frac{(2\pi)^4 y^5}{12} \sum_{\ell=1}^\infty \ell^4 e^{-2\pi \ell y} = \frac{y^5}{12}\frac{d^4}{dy^4}\!\left(\frac{1}{e^{2\pi y}-1}\right) > 0 \quad (y > 0),$$
   four integrations by parts against the Mittag-Leffler expansion of $(e^{2\pi y}-1)^{-1}$ prove $\int_0^\infty y^{2e} w(y)\,dy = \mu(t^e)$ and
   $$\int_0^\infty \frac{w(y)}{y^2 + j^2}\,dy = j^4\!\left(\zeta(5) - H_j^{(5)}\right) - \frac{1}{4} + \frac{1}{2j} = \mu_{\zeta(5)}\!\left(\frac{1}{t+j^2}\right).$$
   Thus at $X = \zeta(5)$, $G_K(\zeta(5))_{i,j} = \int_0^\infty (y^2)^{i+j} \nu_n(y)\,dy$ is the Gram matrix of $\{1, y^2, \dots, y^{2(h-1)}\}$ against the positive measure $\nu_n(y)\,dy = \frac{D_N(y^2)^6}{D_K(y^2)}w(y)\,dy$ on $(0, \infty)$, forcing $\Delta_K(\zeta(5)) > 0$ (`Apery.Δ_pos`) and $Q_n(\zeta(5)) > 0$.
5. **Three-Regime $p$-adic Valuation Lower Bounds & Integrality (`Apery/Norm.lean`, `Apery/Growth.lean`)**:
   Bounding the Gauss valuation $v_p^G(F_K) \ge L_p(n, p)$ across:
   - *Small primes* ($400p \le K$): binomial integer-valued polynomial basis $q_i(-z^2) = \binom{z+i}{2i} + \binom{z+i-1}{2i}$, giving $L_{\mathrm{small}}(n,p) = -(6h\lfloor\log_p(5K)\rfloor + h v_p(24))$ (`Apery/Arith/SmallPrimeF.lean`);
   - *Inner primes* ($K/400 < p \le K/3$): residue-class polynomial basis mod $p$ and water-filling allocation `w_cap` across quadratic residue classes (`Apery/Arith/InnerAlloc.lean`);
   - *Outer primes* ($K/3 < p \le 2h$): von Staudt–Clausen integrality of Bernoulli moments, harmonic congruences for $H_j^{(5)}$, and Schur-complement low-rank reduction (`Apery/Arith/OuterEntryMain.lean`);
   - *Large primes* ($p > 2h = 74n$): $v_p^G(F_K) \ge 0$ (`GV_F_big`);
   the normalizer $m_N(n) := \prod_{p \le 2h} p^{-L_p(n,p)}$ clears all denominators so $Q_n(X) := m_N(n)F_K(X) \in \mathbb{Z}[X]$ (`Apery.normalization`), with $\log m_N(n) \le (A_{\mathrm{eff}} + \varepsilon)K^2$ ($A_{\mathrm{eff}} = 1.36$) by the Prime Number Theorem $\theta(x) \sim x$ (`Apery.growth_mN`).
6. **Andréief Integral, Potential-Theory Decay, & Irrationality Contradiction (`Apery/DetIntegral.lean`, `Apery/RealBound.lean`, `Apery/Main.lean`)**:
   By Andréief's identity, $\Delta_K(\zeta(5)) = \frac{1}{h!}\int_{(0,\infty)^h} \prod_{a<b}(y_a^2 - y_b^2)^2 \prod_{j=0}^{h-1}\nu_n(y_j)\,dy$. Comparing the Vandermonde logarithmic energy against an explicit 16-component arcsine equilibrium measure $\rho$ (verified on 684 intervals in `Apery/EnergyConst.lean`) yields
   $$\log F_K(\zeta(5)) \le U K^2 + 27 K \log K + 200 K, \qquad U = -\frac{2733991}{2000000} = -1.3669955 < -A_{\mathrm{eff}} = -1.36.$$
   Hence $0 < Q_n(\zeta(5)) = m_N(n)F_K(\zeta(5)) < \exp(-c_{\mathrm{Lean}} n^2)$ eventually with $c_{\mathrm{Lean}} = -800(A_{\mathrm{eff}} + U) = 5.5964 > 0$ ($c_{\mathrm{paper}} = 139/5 = 27.8$). If $\zeta(5) = a/b$ ($b \ge 1$), then $b^{37n}Q_n(a/b) \in \mathbb{Z}_{\ge 1}$, contradicting $b^{37n}Q_n(\zeta(5)) < b^{37n}e^{-c n^2} \to 0$ (`Apery.irrational_of_eventually_exists_int_poly`).

### Documented Deviations Between Fauzan's Paper and `mo271/Zeta5`
Our source audit identified three deliberate proof modifications in `mo271/Zeta5`:
- **`DEV-1` (Outer-range rank loss)**: Proposition 4.3 of the paper uses rank loss $\min(r, z)$ for $K/3 < p \le 2h$; `Apery/Arith/OuterEntryMain.lean` replaces $\min(r, z)$ by the simpler upper bound $r$ via a direct Schur-complement pivot, increasing the asymptotic normalizer constant by $\frac{9}{640} = 0.0140625$.
- **`DEV-2` (Cutoff $M = 400$ vs. $M = 200$)**: To compensate for $+\frac{9}{640}$, `Apery/Norm.lean` increases the small/inner prime cutoff from $M = 200$ to $M_{\mathrm{cut}} = 400$, where the inner-range tail over $20 \le x \le 400$ contributes $\le -0.053462$, keeping the total normalizer constant $1.348003\dots < A_{\mathrm{eff}} = 1.36 < -U = 1.3669955$.
- **`DEV-3` (Direct algebraic partial fractions vs. Tate algebras)**: Instead of formalizing $p$-adic Tate algebras (Section 3.3 of the paper), `Apery/Arith/ClassPF.lean` proves the class-wise partial-fraction expansion `tauX_direct` directly over $\mathbb{Q}[t]$ by algebraic induction.

---

## D. Value-Polynomial versus Argument-Polynomial Distinction

A critical structural distinction governs any attempt to transfer Fauzan's 2026 Hankel architecture to the nontrivial zeros of $\zeta(s)$:
$$\boxed{\texttt{VALUE\_POLYNOMIAL\_ARCHITECTURE\_NEQ\_ARGUMENT\_POLYNOMIAL\_ARCHITECTURE}.}$$

1. **Value-Polynomial Architecture (Fauzan 2026 for $\zeta(5)$)**:
   - The argument $s = 5 \in \mathbb{Z}_{\ge 2}$ is **fixed and rational**.
   - The indeterminate $X$ represents the **value** $\zeta(5)$, which enters *affinely* in the simple-pole moments $\mu_X(1/(t+j^2)) = j^4(X - H_j^{(5)}) - 1/4 + 1/(2j)$.
   - Consequently, $G_K(X)_{i,j}$ is automatically degree $\le 1$ in $X$, and $\Delta_K(X) = \det G_K(X) \in \mathbb{Q}[X]$ is automatically a polynomial in the value variable $X$ of degree $h = 37n$.
2. **Argument-Polynomial Architecture (Required for a Zeta Zero $\rho_1 = \beta_1 + i\gamma_1$)**:
   - At a nontrivial zero $\rho_1$, the value $\zeta(\rho_1) = 0$ (and $\xi(\rho_1) = 0$) is **already rational (zero)**.
   - The unknown quantity whose arithmetic nature is sought is the **argument** $\alpha \in \{\gamma_1, \rho_1\}$.
   - In every standard analytic representation of $\zeta(s)$ or $\xi(s)$ — Dirichlet/approximating sums $\sum n^{-s}$, theta-Mellin integrals $\int_0^\infty (\theta(it)-1)t^{s/2-1}\,dt$, or Hadamard/explicit-formula kernels $(y^2 + z_\rho^2)^{-1}$ — the zero argument $\rho_1$ or $\gamma_1$ enters **transcendentally in the exponent $n^{-\rho_1}$ or nonlinearly in the denominator $(y^2 + z_{\rho_1}^2)^{-1}$**, not affinely as a value scalar with rational coefficients.
3. **Mandatory Substitution Firewall (`DO_NOT_SUBSTITUTE_5_TO_RHO_SYMBOLICALLY`)**:
   One cannot substitute $5 \mapsto \rho_1$ in Fauzan's weight $w(y) = \frac{y^5}{12}\frac{d^4}{dy^4}(e^{2\pi y}-1)^{-1}$ or harmonic numbers $H_j^{(5)} = \sum_{v=1}^j v^{-5}$: the 4-fold integration by parts in `Apery/HermiteFormula.lean` requires $s - 1 = 4 \in \mathbb{Z}_{\ge 1}$, and $H_j^{(\rho_1)} = \sum_{v=1}^j v^{-\rho_1}$ is a transcendental exponential sum rather than a rational number with controlled prime denominators.

### Diophantine Lower-Bound Asymmetry Between $D = 1$ ($\gamma_1 \notin \mathbb{Q}$) and $D \ge 2$ ($\alpha \notin \overline{\mathbb{Q}}$)
Suppose an argument-polynomial sequence $P_n(X) \in \mathbb{Z}[X]$ of degree $d_n \le C n$ and naive coefficient height $H(P_n)$ satisfies $P_n(\alpha) \ne 0$. By the Liouville–Mahler inequality, if $\alpha \in \overline{\mathbb{Q}}$ has algebraic degree $D = [\mathbb{Q}(\alpha):\mathbb{Q}]$ and Mahler measure $M(\alpha)$:
$$\boxed{\log |P_n(\alpha)| \ge -(D - 1)\log H(P_n) - d_n \log M(\alpha) - (D - 1)\log(d_n + 1).}$$
- **Case $D = 1$ (Irrationality of $\gamma_1 \in \mathbb{R}$, $\gamma_1 \notin \mathbb{Q}$)**:
  Here $D - 1 = 0$, so **the coefficient height term $-(D-1)\log H(P_n)$ vanishes identically**! Explicitly, if $\gamma_1 = a/b$ ($b \ge 1$), then $b^{d_n}P_n(a/b) \in \mathbb{Z} \setminus \{0\}$, so $|P_n(\gamma_1)| \ge b^{-d_n} = e^{-d_n \log b}$. Therefore, if $d_n = O(n)$, **any** quadratic log-decay $\log |P_n(\gamma_1)| \le -c n^2$ ($c > 0$) suffices to prove $\gamma_1 \notin \mathbb{Q}$, even if $\log H(P_n) = O(n^2)$!
- **Case $D \ge 2$ (Algebraicity exclusion for $\gamma_1 \in \overline{\mathbb{Q}}$ of degree $D \ge 2$, or ANY algebraicity exclusion for non-real $\rho_1 = \beta_1 + i\gamma_1$ where $[\mathbb{Q}(\rho_1):\mathbb{Q}] \ge 2$)**:
  Here $D - 1 \ge 1$, so $-(D - 1)\log H(P_n)$ **does not vanish**:
  - If $\log H(P_n) \sim A n^2$ (as in Fauzan's normalizer where $\log m_N(n) \sim A_{\mathrm{eff}} K^2 = 1600 A_{\mathrm{eff}} n^2$) and $\log |P_n(\alpha)| \le -c n^2$, then excluding degree $D$ requires $c > (D - 1)A$, and excluding all algebraic degrees $D \ge 2$ simultaneously requires either $\log H(P_n) = o(n^2)$ or super-quadratic decay.

---

## E. Special-Value Transfer Reopening and `SUBGATE-TC-039A`

| Method Family | Representative Works | Transfer Verdict to Zero Locations | Reason |
| :--- | :--- | :--- | :--- |
| **Classical Hypercube / Padé / Hypergeometric / Motivic / $p$-adic** | Apéry (1979), Beukers (1979), Ball–Rivoal (2001), Zudilin (2001), Brown (2014), Lai–Sprang–Zudilin (2025) | `SPECIAL_VALUE_IRRATIONALITY_METHOD_HAS_NO_DIRECT_ZERO_LOCATION_TRANSFER` | Requires fixed integer weight/pole order $m \in \mathbb{Z}_{\ge 2}$ and forms linear combinations of values $\zeta(m)$, which collapse at $\zeta(\rho) = 0$. |
| **2026 Hankel / Hermite / Gram / Potential-Theoretic Determinant** | Fauzan (Sep 2026), `mo271/Zeta5` | `FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED` (`SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT_REPAIRED`) | Introduces a $37n \times 37n$ Hankel determinant $\det G_K(X)$ with $O(n)$ degree and $O(n^2)$ Vandermonde energy decay; whether an analogous determinant can be built in an **argument** variable $X \in \{\gamma_1, \rho_1\}$ is a concrete open research question isolated as `SUBGATE-TC-039A`. |

### Six-Gate Architecture for `TASK-TC-039` (`SUBGATE-TC-039A`)
- **Gate `Z1` (Zero-location target representation)**: Construct a zero-independent moment functional or Hankel matrix whose indeterminate $X$ is the zero ordinate $X = \gamma_1$ or complex zero location $X = \rho_1$ (an argument-polynomial architecture, not a value-polynomial architecture).
- **Gate `Z2` (Algebraic polynomiality)**: Prove that the resulting Hankel determinant $\Delta_n(X)$ belongs to $\mathbb{Q}[X]$ with controlled degree $\deg P_n \le C n$ and becomes $P_n(X) \in \mathbb{Z}[X]$ under explicit arithmetic normalization.
- **Gate `Z3` (Nonvanishing at the zero)**: Prove $P_n(\alpha) \ne 0$ for $\alpha \in \{\gamma_1, \rho_1\}$; the defining equation $\zeta(\rho_1) = 0$ must not force the auxiliary Hankel determinant to vanish identically.
- **Gate `Z4` (Arithmetic denominator/height control)**: Bound $\deg P_n \le C n$ and coefficient height $\log H(P_n) \le C' n^2$ (or $C' n$) via explicit $p$-adic valuation bounds.
- **Gate `Z5` (Analytic smallness)**: Prove superexponential decay $0 < |P_n(\alpha)| \le \exp(-c n^2)$ (via Andréief / Vandermonde logarithmic energy or contour saddle bounds) with $c$ strictly exceeding the Liouville/Mahler denominator/height constant.
- **Gate `Z6` (Irrationality/algebraicity contradiction)**: Combine Gates `Z1`–`Z5` with the rational clearing bound (for $\gamma_1 \notin \mathbb{Q}$) or the Liouville–Mahler algebraic lower bound (for $\alpha \notin \overline{\mathbb{Q}}$), terminating at the earliest failed gate.

---

## F. Formal-Provenance Repair and Build Inventory Synchronization

In `TASK-TC-038`, `formal/RiemannScope/ZeroArithmeticInvariants.lean` was imported in `formal/RiemannScope.lean` and compiled by `lake build`, but was omitted from the explicit Python provenance lists `scripts/build_formal.py::FORMAL_SOURCE_FILES` and `certification.py::REQUIRED_FORMAL_SOURCES`.

In `TASK-TC-038R`:
1. `"formal/RiemannScope/ZeroArithmeticInvariants.lean"` is added to both `scripts/build_formal.py::FORMAL_SOURCE_FILES` and `certification.py::REQUIRED_FORMAL_SOURCES` (`FORMAL_SOURCE_INVENTORY_REPAIRED`, `FORMAL_SOURCE_INVENTORY_SYNCHRONIZED`).
2. `verify_formal_source_inventory_provenance()` in `tc/zero_arithmetic_invariants.py` (tested in `tests/test_tc_zero_arithmetic_invariants.py`) parses every `import RiemannScope.<Module>` line in `formal/RiemannScope.lean` and verifies that `FORMAL_SOURCE_FILES` and `REQUIRED_FORMAL_SOURCES` match `formal/RiemannScope.lean` 1-to-1 (`30` local modules + umbrella `formal/RiemannScope.lean` = `31` formal source files).
3. Two additional theorems (`stieltjes_notation_no_effect_algebra` and `s2_equivalent_closed_forms`) were added to `formal/RiemannScope/ZeroArithmeticInvariants.lean` and verified with `lake build`.
4. **Exact Formal Counts (`ZERO_ARITHMETIC_MODULE_INCLUDED_IN_BUILD_PROVENANCE`)**:
   - `formal/RiemannScope/ZeroArithmeticInvariants.lean` SHA256: `e209bea9bf48de3bcddbb941198dc295dab323f89a4df4e896d89c9a373306c0`,
   - `theorem` declarations in `ZeroArithmeticInvariants.lean`: **`12`** (plus `4` `def` declarations = `16` total declarations; `0 sorry`, `0 admit`, `0 axiom`),
   - Total `theorem` declarations across all `31` files in `FORMAL_SOURCE_FILES`: **`626`**.

---

## G. Stieltjes Notation Policy (`STIELTJES_NOTATION_DISAMBIGUATED`)

To eliminate any symbol collision between the $n$-th zeta-zero ordinate $\gamma_n = \operatorname{Im}(\rho_n)$ and the $k$-th Stieltjes constant in the Laurent expansion of $\zeta(s)$ at $s = 1$, the repository enforces the following notation policy across all code, JSON artifacts, Lean docstrings, and Markdown documents:
$$\boxed{
\begin{aligned}
\gamma_n &= \operatorname{Im}(\rho_n) \in \mathbb{R}_{>0} &&\text{(nontrivial zeta-zero ordinate, } n \ge 1\text{)}, \\
\gamma_E &= \gamma_0^{\mathrm{St}} \approx 0.5772156649\dots &&\text{(Euler–Mascheroni constant)}, \\
\gamma_k^{\mathrm{St}} &:= \lim_{M\to\infty}\left(\sum_{m=1}^M \frac{(\log m)^k}{m} - \frac{(\log M)^{k+1}}{k+1}\right) &&\text{(}k\text{-th Stieltjes constant, } k \ge 1\text{)},
\end{aligned}
}$$
with Laurent expansion:
$$\zeta(s) = \frac{1}{s-1} + \gamma_E + \sum_{k=1}^\infty \frac{(-1)^k}{k!}\gamma_k^{\mathrm{St}}(s-1)^k.$$

---

## H. $S_2, S_3, S_4$ Canonical Formula Repair (`S2_CANONICAL_FORMULA_REPAIRED`, `S3_S4_REAUDITED`)

### 1. Removal of the Erroneous Historical $S_2$ Formula
During `TASK-TC-038`, `RESEARCH_HYPOTHESIS.md` and `RESEARCH_LEDGER.md` contained an erroneous transcription:
$$S_2^{\text{erroneous}} = 1 - \frac{\pi^2}{8} + \gamma_{\mathrm{Euler}} + \frac{\gamma_{\mathrm{Euler}}^2}{4} - \gamma_1^{\mathrm{Stieltjes}} \approx +0.678896401207\dots,$$
which differs from the true value $S_2 \approx -0.0461543172958\dots$ by $\Delta = -0.725050718503\dots$ because $\gamma_E + \frac{1}{4}\gamma_E^2 - \gamma_1^{\mathrm{St}}$ is not the second logarithmic derivative of $(s-1)\zeta(s)$ at $s=1$. All instances of this erroneous formula have been removed and replaced by the two equivalent exact canonical closed forms:
$$\boxed{S_2 = \sum_{\rho} \frac{1}{\rho^2} = 1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1^{\mathrm{St}} = 1 - \frac{\pi^2}{24} + 2\zeta''(0) + \log^2(2\pi) \approx -0.04615431729580460275710799037907730353027,}$$
bridged by the identity $2\zeta''(0) + \log^2(2\pi) = \gamma_E^2 - \frac{\pi^2}{12} + 2\gamma_1^{\mathrm{St}}$ (formalized in Lean 4 as `s2_equivalent_closed_forms`).

### 2. Three-Route Independent Re-Audit of $S_2, S_3, S_4$
Each of $S_2, S_3, S_4$ was re-verified in `tc/zero_arithmetic_invariants.py` by three independent routes:
1. **Route 1 (Exact SymPy Laurent series of $\log\xi(1+u)$ at $u=0$ and $\log\xi(s)$ at $s=0$)**: Exact symbolic match (`residual = 0`).
2. **Route 2 (50-dps `mpmath` numerical differentiation of $\log\xi(s)$ at $s=0$ and $s=1$ vs. closed form)**:
   - $|S_2^{\text{deriv}} - S_2^{\text{closed}}| = 1.00 \times 10^{-51}$,
   - $|S_3^{\text{deriv}} - S_3^{\text{closed}}| < 10^{-49}$ for $S_3 = 1 - \frac{7}{8}\zeta(3) + \gamma_E^3 + 3\gamma_E\gamma_1^{\mathrm{St}} + \frac{3}{2}\gamma_2^{\mathrm{St}}$,
   - $|S_4^{\text{deriv}} - S_4^{\text{closed}}| < 10^{-49}$ for $S_4 = 1 - \frac{\pi^4}{96} + \gamma_E^4 + 4\gamma_E^2\gamma_1^{\mathrm{St}} + 2(\gamma_1^{\mathrm{St}})^2 + 2\gamma_E\gamma_2^{\mathrm{St}} + \frac{2}{3}\gamma_3^{\mathrm{St}}$.
3. **Route 3 (Direct partial sum over the first 200 conjugate zero pairs plus Riemann–von Mangoldt asymptotic tail integral $\int_{T_{200}}^\infty 2\operatorname{Re}((1/2+it)^{-m})\frac{\log(t/2\pi)}{2\pi}\,dt$)**:
   - $S_2$: tail-corrected residual $2.18 \times 10^{-6}$,
   - $S_3$: tail-corrected residual $3.18 \times 10^{-9}$,
   - $S_4$: tail-corrected residual $1.27 \times 10^{-9}$.

---

## I. Finite-Exclusion Certification Scope Repair (`FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED`)

Post-sprint review identified that in `TASK-TC-038`, `_certify_real_ball_polynomial_box` and `_certify_rho1_polynomial_box` used hierarchical outward interval pruning to exclude branches where $0 \notin P(I)$, and recorded `min_lower_bound` only over the unpruned leaf polynomials (and in `_certify_rho1_polynomial_box`, updated `min_lower_bound` on imaginary-part pruned branches $(0, a_1, a_2, a_3, a_4)$ without checking $\gcd(a_1, a_2, a_3, a_4) = 1$ or optimizing over $a_0$). While **outward interval pruning rigorously certifies $0 \notin P(I)$ for every polynomial in the pruned branch** (because each individual evaluation $P(\alpha)$ lies inside the branch interval enclosure), the minimum over evaluated leaves is **not** a certified global minimum of $|P(\alpha)|$ over the entire $D \le 4, H \le 100$ box.

In accordance with **Route A (Section 20.1)**, we separate the two finite polynomial regimes strictly:

| Box Regime | Space Size (Normalized Primitive) | Method Label | Exclusion Status | Global Minimum Status | Certified Bounds |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Small Box: $1 \le d \le 4, H \le 3$** | $8{,}160$ polynomials | `EXPLICIT_POLYNOMIAL_ENUMERATION` | `CERTIFIED_FINITE_ALGEBRAIC_RELATION_EXCLUSION` | **Certified Global Minimum over $D \le 4, H \le 3$** (`full_box_global_minimum_certified = True`) | $\min |P(\gamma_1)| \ge 11.134725141734695$, $\min |P(\gamma_1+1/2)| \ge 11.634725141734695$, $\min |P(\rho_1)| \ge 14.143565845725995$ |
| **Large Box: $1 \le d \le 4, H \le 100$** | $158{,}062{,}321{,}920$ polynomials | `HIERARCHICAL_BOX_EXCLUSION` | `CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION` | **`FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED`** (`full_box_global_minimum_certified = False`) | $P(\gamma_1) \ne 0$, $P(\gamma_1+1/2) \ne 0$, and $P(\rho_1) \ne 0$ certified for all $158{,}062{,}321{,}920$ normalized primitive polynomials; no global minimum $|P|$ is claimed over the pruned $H \le 100$ box. |

---

## J. Cardinality and Fixed-Number-Field Scope Repair

1. **Cardinality Firewall (`CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE`)**:
   Because the set of nontrivial zeros $\{\rho_n\}_{n \ge 1}$ and the set of positive ordinates $\{\gamma_n\}_{n \ge 1}$ are **countably infinite** while $\overline{\mathbb{Q}}$ is also countably infinite, Cantor's cardinality argument ($\mathbb{R} \setminus \overline{\mathbb{Q}}$ uncountable) tells us **nothing** about whether any or infinitely many $\gamma_n$ are transcendental. The misleading status label `"PROVED_WITH_EXTERNAL_THEOREM (transcendence by cardinality only)"` in Section F of the `TASK-TC-038` report has been removed and replaced by:
   $$\boxed{\texttt{CARDINALITY\_DOES\_NOT\_IMPLY\_ZERO\_ORDINATE\_TRANSCENDENCE} \quad\text{and}\quad \texttt{NO\_INDIVIDUAL\_ORDINATE\_IRRATIONALITY\_OR\_TRANSCENDENCE\_THEOREM\_FOUND}.}$$
2. **Northcott Fixed-Number-Field Qualification (`FIXED_NUMBER_FIELD_REQUIRES_BOUNDED_DEGREE_AND_BOUNDED_HEIGHT`)**:
   A fixed number field $K / \mathbb{Q}$ (such as $\mathbb{Q}$ itself) is an **infinite** set containing elements of arbitrarily large height. Northcott's theorem guarantees finiteness only for the subset of algebraic numbers of **bounded degree $\le D$ and bounded height $\le H$** (or within a bounded archimedean interval $|\gamma| \le T$ when denominators/heights are bounded). Every reference to fixed number fields in the report and code now states explicitly that **both bounded degree and bounded height** are required for Northcott finiteness.

---

## K. Re-Audited Literature Matrix

| Claim / Question | Repaired Status Classification | Source Verification | Primary-Source Explanation |
| :--- | :--- | :--- | :--- |
| $\rho_n \notin \mathbb{Q}$ for all nontrivial zeros $\rho_n$ | `PROVED` | `PRIMARY_SOURCE_VERIFIED` | $\zeta(s) < 0$ on $(0, 1)$ implies $\operatorname{Im}(\rho_n) = \gamma_n \ne 0$, so $\rho_n \notin \mathbb{R} \supset \mathbb{Q}$ (Titchmarsh 1986, §2.12). |
| $\gamma_n \notin \mathbb{Q}$ for any individual $n \ge 1$ | `NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT` (`OPEN_IN_LITERATURE`) | `NO_PRIMARY_SOURCE_FOUND` | No theorem in the primary literature proves irrationality of $\gamma_1$ or any individual ordinate $\gamma_n$. |
| $\rho_n \notin \overline{\mathbb{Q}}$ or $\gamma_n \notin \overline{\mathbb{Q}}$ for any individual $n \ge 1$ | `NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT` (`OPEN_IN_LITERATURE`) | `NO_PRIMARY_SOURCE_FOUND` | No theorem in the primary literature proves transcendence of any individual $\rho_n$ or $\gamma_n$. |
| Infinitely many distinct ordinates $\gamma_n$ exist; $\ge 40.89\%$ are simple | `PROVED_WITH_EXTERNAL_THEOREM` | `PRIMARY_SOURCE_VERIFIED` | Hardy (1914); Selberg (1942); Bui–Conrey–Young (2011). Note: countability of $\{\gamma_n\}$ means `CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE`, and Northcott finiteness applies only to $\{\alpha \in \overline{\mathbb{Q}} : [\mathbb{Q}(\alpha):\mathbb{Q}] \le D,\; H(\alpha) \le H\}$ (`FIXED_NUMBER_FIELD_REQUIRES_BOUNDED_DEGREE_AND_BOUNDED_HEIGHT`). |
| $\mathbb{Q}$-linear independence of positive ordinates $\{\gamma_n\}_{n \ge 1}$ | `CONDITIONAL_ON_NAMED_CONJECTURE` (`LI`) | `PRIMARY_SOURCE_VERIFIED` | Linear Independence Conjecture (Wintner 1935; Ingham 1942; Rubinstein–Sarnak 1994); open. |
| Archimedean $\zeta(5) \notin \mathbb{Q}$ | `ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM` + `ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN` (`LEAN_PROVED_EXTERNAL_REPOSITORY`, `SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED`, `ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN`, `PEER_REVIEW_STATUS_PENDING`) | `PRIMARY_SOURCE_VERIFIED` | Fauzan (17 Sep 2026, Zenodo `22826419`) and public Lean 4 repository `mo271/Zeta5` (`7fe736760f4b96bfdb4334b68e3b3124ecbe10b0`), exporting `Apery.irrational_five` and `RiemannZetaValues.irrational_five` with standard axioms `[propext, Classical.choice, Quot.sound]` and `0 sorry`. |
| 2-adic $\zeta_2(5) \notin \mathbb{Q}$ | `PROVED_WITH_EXTERNAL_THEOREM` | `PRIMARY_SOURCE_VERIFIED` | Lai–Sprang–Zudilin (May 2025, `arXiv:2505.05005v2`). |

---

## L. Re-Audited Lean Theorem Table (`formal/RiemannScope/ZeroArithmeticInvariants.lean`)

All `12` `theorem` declarations and `4` `def` declarations in `formal/RiemannScope/ZeroArithmeticInvariants.lean` compile cleanly with `0 sorry`, `0 admit`, and no custom axioms (`626` total `theorem` declarations across the `31` files in `FORMAL_SOURCE_FILES`):

| # | Lean Declaration Name | Kind | Mathematical Statement Formalized |
| :--- | :--- | :--- | :--- |
| 1 | `shiftedOrdinate` | `def` | $\tilde{\gamma}(\gamma) := \gamma + \frac{1}{2}$ |
| 2 | `shifted_ordinate_sub_half` | `theorem` | $\tilde{\gamma}(\gamma) - \frac{1}{2} = \gamma$ |
| 3 | `shifted_ordinate_rational_iff` | `theorem` | $(\exists q \in \mathbb{Q},\; (q:\mathbb{R}) = \gamma + \frac{1}{2}) \iff (\exists q \in \mathbb{Q},\; (q:\mathbb{R}) = \gamma)$ |
| 4 | `shifted_ordinate_algebraic_iff` | `theorem` | $\operatorname{IsAlgebraic} \mathbb{Q} (\gamma + \frac{1}{2}) \iff \operatorname{IsAlgebraic} \mathbb{Q} \gamma$ |
| 5 | `shifted_ordinate_transcendental_iff` | `theorem` | $\operatorname{Transcendental} \mathbb{Q} (\gamma + \frac{1}{2}) \iff \operatorname{Transcendental} \mathbb{Q} \gamma$ |
| 6 | `complex_zero_re_im_algebraicity` | `theorem` | $(\beta:\mathbb{C}) = \frac{(\beta+i\gamma)+(\beta-i\gamma)}{2} \;\wedge\; (\gamma:\mathbb{C}) = \frac{(\beta+i\gamma)-(\beta-i\gamma)}{2i}$ |
| 7 | `reflection_reciprocal_identity` | `theorem` | $\rho \ne 0 \implies 1 - \rho \ne 0 \implies \frac{1}{\rho} + \frac{1}{1-\rho} = \frac{1}{\rho(1-\rho)}$ |
| 8 | `centeredQuartetPoly` | `def` | $Q_{z}(X) := (X - z)(X + z)(X - \bar{z})(X + \bar{z})$ |
| 9 | `centeredQuartetC2` | `def` | $c_2(\delta, \gamma) := -2(\delta^2 - \gamma^2)$ |
| 10 | `centeredQuartetC0` | `def` | $c_0(\delta, \gamma) := (\delta^2 + \gamma^2)^2$ |
| 11 | `centered_quartet_polynomial_identity` | `theorem` | $Q_{\delta+i\gamma}(X) = X^4 - 2(\delta^2 - \gamma^2)X^2 + (\delta^2 + \gamma^2)^2$ |
| 12 | `centered_quartet_coefficients_real` | `theorem` | $\operatorname{Im}(c_2(\delta,\gamma)) = 0 \;\wedge\; \operatorname{Im}(c_0(\delta,\gamma)) = 0 \;\wedge\; 0 \le c_0(\delta,\gamma)$ |
| 13 | `li_first_coefficient_finite_algebra_identity` | `theorem` | $\rho \ne 0 \implies 1 - \rho \ne 0 \implies (1 - (1 - \rho^{-1})) + (1 - (1 - (1-\rho)^{-1})) = \frac{1}{\rho(1-\rho)}$ |
| 14 | `reciprocal_power_log_derivative_sign_identity` | `theorem` | $(1 - s) - (1 - \rho) = -(s - \rho) \;\wedge\; (\rho - \frac{1}{2}) + ((1 - \rho) - \frac{1}{2}) = 0$ |
| 15 | `stieltjes_notation_no_effect_algebra` | `theorem` | Substituting disambiguated symbol $\gamma_1^{\mathrm{St}}$ in $1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1^{\mathrm{St}}$ preserves the exact algebraic expression |
| 16 | `s2_equivalent_closed_forms` | `theorem` | $(2 z_0'' + L^2 = \gamma_E^2 - \frac{\pi^2}{12} + 2\gamma_1^{\mathrm{St}}) \implies 1 - \frac{\pi^2}{24} + 2 z_0'' + L^2 = 1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1^{\mathrm{St}}$ |

---

## M. Reassessed Principal Classification

After incorporating the 2026 $\zeta(5)$ development and repairing formal provenance, Stieltjes notation, and finite-exclusion certification scope:
$$\boxed{\texttt{ZERO\_ARITHMETIC\_FRONTIER\_CLASSIFIED\_INDIVIDUAL\_STATUS\_OPEN}}$$
remains the accurate principal classification for the arithmetic nature of the nontrivial zeros of $\zeta(s)$, paired with the repaired secondary transfer classification:
$$\boxed{\texttt{FAUZAN\_HANKEL\_ZERO\_LOCATION\_TRANSFER\_UNRESOLVED} \quad (\texttt{SPECIAL\_VALUE\_TRANSFER\_REQUIRES\_2026\_HANKEL\_AUDIT\_REPAIRED}).}$$

---

## N. Exact Remaining Subgates (`SUBGATE-TC-038A`, `SUBGATE-TC-039A`, `OBL-CT-001A`)

1. **`SUBGATE-TC-038A = OPEN` (`ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE`)**:
   Prove irrationality of the first reflection-invariant symmetric zero sum $2\lambda_1 = \sum_\rho \frac{1}{\rho(1-\rho)} = 2 + \gamma_E - \log(4\pi)$ (equivalently $\gamma_E - \log(4\pi) \notin \mathbb{Q}$), or prove $\dim_{\mathbb{Q}}\operatorname{span}_{\mathbb{Q}}(1, S_1, S_2) \ge 2$ where $S_2 = 1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1^{\mathrm{St}}$. (Scoped strictly to global symmetric zero-sum constants.)
2. **`SUBGATE-TC-039A = OPEN` (`FAUZAN_HANKEL_TO_ZERO_ARGUMENT_TRANSFER_SUBGATE`)**:
   Determine across Gates `Z1`–`Z6` in `TASK-TC-039` whether a Hankel/Hermite/Gram/potential-theoretic determinant architecture can construct an auxiliary polynomial $P_n(X) \in \mathbb{Z}[X]$ in a zero-location **argument** $X \in \{\gamma_1, \rho_1\}$ with certified nonvanishing $P_n(X) \ne 0$, linear degree $d_n = O(n)$, controlled coefficient height $\log H(P_n)$, and quadratic log-decay $\log |P_n(X)| \le -c n^2$ beating the Liouville–Mahler lower bound.
3. **`OBL-CT-001A = OPEN`**:
   The primary TC spectral-to-arithmetic bridge obligation remains open and untouched under the scope firewall.

---

## O. Complete Modified-File Inventory (`TASK-TC-038R`)

| File | Role in `TASK-TC-038R` |
| :--- | :--- |
| `data/fauzan_zeta5_architecture.json` | New machine-readable artifact recording all 20 required keys of Fauzan's Sep 2026 $\zeta(5)$ preprint, `mo271/Zeta5` Lean 4 formalization, 3 paper-vs-Lean deviations, and Gates `Z1`–`Z6` for `SUBGATE-TC-039A`. |
| `data/tc_zero_arithmetic_invariants.json` | Updated artifact containing all 35 original keys and all 28 required `TASK-TC-038R` repair keys. |
| `tc/zero_arithmetic_invariants.py` | Updated with 2026 $\zeta(5)$ taxonomy, Fauzan Hankel transfer audit, Liouville–Mahler $D=1$ vs. $D \ge 2$ analysis, Stieltjes notation disambiguation, $S_2/S_3/S_4$ 3-route re-audit, Route A finite-exclusion scope repair, cardinality/Northcott repair, and formal inventory provenance verifier. |
| `tc/__init__.py` | Exports all new `TASK-TC-038R` constants and functions. |
| `formal/RiemannScope/ZeroArithmeticInvariants.lean` | Added `stieltjes_notation_no_effect_algebra` and `s2_equivalent_closed_forms` (`12` `theorem` declarations, `0 sorry`). |
| `formal/RiemannScope/README.md` | Updated theorem counts (`12` theorems in `ZeroArithmeticInvariants.lean`, `626` total across `30` modules). |
| `scripts/build_formal.py` | Added `"formal/RiemannScope/ZeroArithmeticInvariants.lean"` to `FORMAL_SOURCE_FILES`. |
| `certification.py` | Added `"formal/RiemannScope/ZeroArithmeticInvariants.lean"` to `REQUIRED_FORMAL_SOURCES`. |
| `formal/build_report.json` | Regenerated formal build provenance report including `ZeroArithmeticInvariants.lean` and `626` theorems. |
| `docs/reviews/TC_ZERO_ARITHMETIC_INVARIANTS.md` | Prepended `# TASK-TC-038R Repair` (Sections A–O) and repaired all affected body sections below. |
| `RESEARCH_HYPOTHESIS.md` | Removed erroneous $S_2$ formula, removed uncertified full-box $\min |P|$ claims, updated $\zeta(5)$-2026 status, `SUBGATE-TC-038A`/`SUBGATE-TC-039A`, and theorem count (`626`). |
| `RESEARCH_LEDGER.md` | Repaired `TASK-TC-038` entry and added `TASK-TC-038R` entry. |
| `MATH_CONTRACT.md` | Updated $\zeta(5)$-2026 taxonomy, Stieltjes notation $\gamma_k^{\mathrm{St}}$, finite-exclusion scope, and `SUBGATE-TC-038A`/`SUBGATE-TC-039A`. |
| `TRANSCENDENTAL_CONTINUATION.md` | Updated $\zeta(5)$-2026 taxonomy, Stieltjes notation, and `SUBGATE-TC-038A`/`SUBGATE-TC-039A`. |
| `docs/TC_CURRENT_CANONICAL_STATUS.md` | Updated canonical status for `TASK-TC-038R`, $\zeta(5)$-2026, Stieltjes notation, finite-exclusion scope, and theorem count (`626`). |
| `.agents/corpus_map/obligation_register.md` | Narrowed `SUBGATE-TC-038A` to `ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE` and registered `SUBGATE-TC-039A`. |
| `.agents/research/state.json` & `.agents/research/queue.json` | Updated mission state to `TASK-TC-038R` complete and queued `SUBGATE-TC-039A` (`TASK-TC-039`). |
| `tests/test_tc_zero_arithmetic_invariants.py` | Extended to cover all 30 required `TASK-TC-038R` regression tests. |

---
---

# TASK-TC-038 — Arithmetic Nature of Nontrivial Zeros, Exact Zero-Sum Invariants, and Special-Value Transfer Audit (Repaired Body)

**Repository**: `tsolomon89/reimann_scope`  
**Task ID**: `TASK-TC-038` (repaired in `TASK-TC-038R`)  
**Branch Classification**: `ZERO_ARITHMETIC_BRANCH`  
**Starting HEAD (`TASK-TC-038`)**: `63770418ca4b4498b0c9300a854e45d52434f52b`  
**Substantive Parent (`TASK-TC-038`)**: `70c757ce6cead947fc806b2dadd78f2de0363fc6`  
**Principal Classification**: `ZERO_ARITHMETIC_FRONTIER_CLASSIFIED_INDIVIDUAL_STATUS_OPEN`  
**Secondary Transfer Classification**: `FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED` (`SPECIAL_VALUE_TRANSFER_REQUIRES_2026_HANKEL_AUDIT_REPAIRED`)  
**Shifted-Ordinate Classification**: `SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE`  
**Primary TC Obligation Status**: `OBL-CT-001A = OPEN`  
**Exact Remaining Zero-Arithmetic Subgates**: `SUBGATE-TC-038A = OPEN`, `SUBGATE-TC-039A = OPEN`  

---

## A. Executive Verdict

Following the completion and evidence repair of the TC bigraded character projection audit (`TASK-TC-037` / `TASK-TC-037R`), `TASK-TC-038` (and its repair `TASK-TC-038R`) pivots from constructing new TC projectors to a rigorous mathematical, symbolic, primary-literature, and certified finite-interval audit of the **arithmetic nature of the nontrivial zeros of $\zeta(s)$ themselves and of canonical symmetric invariants built from them**.

1. **Principal Classification**:
   $$\boxed{\texttt{ZERO\_ARITHMETIC\_FRONTIER\_CLASSIFIED\_INDIVIDUAL\_STATUS\_OPEN}}$$
   with repaired secondary methodological transfer verdict:
   $$\boxed{\texttt{FAUZAN\_HANKEL\_ZERO\_LOCATION\_TRANSFER\_UNRESOLVED} \quad (\texttt{SPECIAL\_VALUE\_TRANSFER\_REQUIRES\_2026\_HANKEL\_AUDIT\_REPAIRED}).}$$
2. **Candidate-Object Equivalence (`SHIFTED_ORDINATE_ARITHMETICALLY_EQUIVALENT_TO_ORDINATE`)**:
   Because $\frac{1}{2} \in \mathbb{Q} \subset \overline{\mathbb{Q}}$ and both $\mathbb{Q}$ and $\overline{\mathbb{Q}}$ are fields closed under addition and subtraction, the shifted ordinate $\tilde{\gamma}_n := \gamma_n + \frac{1}{2}$ satisfies
   $$\gamma_n + \frac{1}{2} \in \mathbb{Q} \iff \gamma_n \in \mathbb{Q}, \qquad \gamma_n + \frac{1}{2} \in \overline{\mathbb{Q}} \iff \gamma_n \in \overline{\mathbb{Q}}, \qquad \gamma_n + \frac{1}{2} \notin \overline{\mathbb{Q}} \iff \gamma_n \notin \overline{\mathbb{Q}},$$
   with minimal-polynomial degree invariant ($\deg_{\mathbb{Q}}(\gamma_n + 1/2) = \deg_{\mathbb{Q}}(\gamma_n)$) via the explicit integer-polynomial bijection $Q(Y) = 2^d P(Y - 1/2)$. Therefore $\gamma_n + 1/2$ does **not** define a distinct arithmetic question from $\gamma_n$. By contrast, the full complex zero $\rho_n = \beta_n + i\gamma_n$ satisfies unconditionally $\rho_n \in \overline{\mathbb{Q}} \iff (\beta_n \in \overline{\mathbb{Q}} \text{ and } \gamma_n \in \overline{\mathbb{Q}})$ (using complex conjugation $\bar{\rho}_n = \beta_n - i\gamma_n$ and $i \in \overline{\mathbb{Q}}$), while $\rho_n \notin \mathbb{Q}$ unconditionally because $\zeta(s) < 0$ on $(0, 1)$ implies $\gamma_n \ne 0$.
3. **Individual Zero Arithmetic Status (`NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT` / `OPEN_IN_LITERATURE`)**:
   Primary-source audit of the analytic number theory and transcendence literature confirms that for every individual nontrivial zero $\rho_n = \beta_n + i\gamma_n$ ($n \ge 1$):
   - $\rho_n \notin \mathbb{Q}$ is **proved unconditionally** ($\operatorname{Im}(\rho_n) = \gamma_n \ne 0$).
   - Whether $\gamma_n \notin \mathbb{Q}$ for any individual $n$ (in particular $\gamma_1 \approx 14.13472514$) has **`NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT`** (`OPEN_IN_LITERATURE`).
   - Whether $\rho_n \notin \overline{\mathbb{Q}}$ or $\gamma_n \notin \overline{\mathbb{Q}}$ for any individual $n$ has **`NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT`** (`OPEN_IN_LITERATURE`).
   - Because $\{\gamma_n\}_{n \ge 1}$ is countably infinite, Cantor cardinality does **not** imply that any $\gamma_n$ is transcendental (`CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE`), and Northcott finiteness applies only to algebraic numbers of **both bounded degree and bounded height** (`FIXED_NUMBER_FIELD_REQUIRES_BOUNDED_DEGREE_AND_BOUNDED_HEIGHT`).
   - Linear independence over $\mathbb{Q}$ of the positive ordinates $\{\gamma_n\}_{n \ge 1}$ is the classical **Linear Independence Conjecture (LI)** (`CONDITIONAL_ON_NAMED_CONJECTURE`).
   - None of the nine major transcendence theorem families (Lindemann–Weierstrass, Gelfond–Schneider, Baker, Siegel–Shidlovsky, Schneider–Lang, Nesterenko, Chudnovsky, Rohrlich–Lang, Hölder–Ostrowski) applies to $\zeta(\rho_n) = 0$ inside $0 < \operatorname{Re}(s) < 1$.
4. **Exact Symmetric Zero-Sum Invariants Derived and Verified (`STIELTJES_NOTATION_DISAMBIGUATED`)**:
   While individual zeros resist existing Diophantine methods, symmetric sums over all nontrivial zeros are **analytically closed in terms of classical constants** via the Hadamard factorization of $\xi(s) = \frac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$ (writing $\gamma_E = \gamma_0^{\mathrm{St}}$ for Euler's constant and $\gamma_k^{\mathrm{St}}$ for the Stieltjes constants):
   - $S_1 = \sum_\rho^{\mathrm{sym}} \frac{1}{\rho} = 1 + \frac{\gamma_E}{2} - \log(2\sqrt{\pi}) = \lambda_1 \approx 0.0230957089661210338143102479065$,
   - $\sum_\rho \frac{1}{\rho(1-\rho)} = 2 S_1 = 2\lambda_1 = 2 + \gamma_E - \log(4\pi) \approx 0.0461914179322420676286204958130$ (converging **absolutely** without grouping because $|\rho(1-\rho)| \sim \gamma_\rho^2$),
   - $S_2 = \sum_\rho \frac{1}{\rho^2} = 1 - \frac{\pi^2}{24} + 2\zeta''(0) + \log^2(2\pi) = 1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1^{\mathrm{St}} \approx -0.0461543172958046027571079903791$,
   - $S_3 = 1 - \frac{7}{8}\zeta(3) + \gamma_E^3 + 3\gamma_E\gamma_1^{\mathrm{St}} + \frac{3}{2}\gamma_2^{\mathrm{St}} \approx -0.000111158231452105922762668238915$,
   - $S_4 = 1 - \frac{\pi^4}{96} + \gamma_E^4 + 4\gamma_E^2\gamma_1^{\mathrm{St}} + 2(\gamma_1^{\mathrm{St}})^2 + 2\gamma_E\gamma_2^{\mathrm{St}} + \frac{2}{3}\gamma_3^{\mathrm{St}} \approx +0.0000736272212616895183267713070306$,
   - Centered odd sums $\Sigma_{2m-1}^{\mathrm{sym}} = \sum_\rho^{\mathrm{sym}} (\rho - 1/2)^{-(2m-1)} = 0$ identically, and $\Sigma_2 = \sum_\rho (\rho - 1/2)^{-2} = 8 - \frac{1}{4}\psi_1(1/4) - \left.\frac{d^2}{ds^2}\log(-\zeta(s))\right|_{s=1/2} \approx -0.0462099862308379415778676208607$.
   However, the irrationality and transcendence of every one of these nonzero exact combinations ($S_1$, $2S_1$, $S_2$, $S_3$, $S_4$, $\Sigma_2$, $\lambda_n$) remain **`OPEN_IN_LITERATURE`** (`SUBGATE-TC-038A`) because the $\mathbb{Q}$-algebraic independence of $\gamma_E$, $\log(4\pi)$, and the Stieltjes constants $\gamma_k^{\mathrm{St}}$ is unproved.
5. **Primary-Source Verification of $\zeta(5)$ (Repaired for September 2026) & Special-Value Transfer Audit**:
   - In September 2026, Aabir Fauzan released the preprint *"$\zeta(5)$ is irrational"* (Zenodo `22826419`) together with the public Lean 4 formalization `mo271/Zeta5` (`7fe736760f4b96bfdb4334b68e3b3124ecbe10b0`), proving `Apery.irrational_five` and `RiemannZetaValues.irrational_five` with `0 sorry` and standard axioms `[propext, Classical.choice, Quot.sound]` (`ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM`, `ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN`, `LEAN_PROVED_EXTERNAL_REPOSITORY`, `SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED`, `ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN`, `PEER_REVIEW_STATUS_PENDING`).
   - Classical special-value methods (Apéry–Beukers integrals, Ball–Rivoal–Zudilin hypergeometric series, Brown's $\mathcal{M}_{0,n}$ periods, and Lai–Sprang–Zudilin 2-adic holonomic constructions) have no direct zero-location transfer (`SPECIAL_VALUE_IRRATIONALITY_METHOD_HAS_NO_DIRECT_ZERO_LOCATION_TRANSFER`). Fauzan's 2026 Hankel/Hermite/Gram/potential-theoretic determinant architecture constructs a **value polynomial** $Q_n(X) \in \mathbb{Z}[X]$ evaluated at $X = \zeta(5)$, whereas zero locations require an **argument polynomial** $P_n(X) \in \mathbb{Z}[X]$ evaluated at $X \in \{\gamma_1, \rho_1\}$ (`VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE`); whether this determinant mechanism can transfer is classified as `FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED` and isolated as `SUBGATE-TC-039A` (Gates `Z1`–`Z6`) for `TASK-TC-039`.
6. **Certified 128-bit Arb Finite Exclusions (Repaired Scope)**:
   - Using 128-bit outward Arb/Acb interval arithmetic, we certify `CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION` across all $158{,}062{,}321{,}920$ normalized primitive integer polynomials of degree $1 \le d \le 4$ and height $H \le 100$ for $\gamma_1$, $\gamma_1 + 1/2$, and $\rho_1 = 1/2 + i\gamma_1$ (`HIERARCHICAL_BOX_EXCLUSION`, with `FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED` on the pruned $H \le 100$ box), and we certify exact full-box global minima on the exhaustively enumerated box $D = 4, H = 3$ ($8{,}160$ normalized primitive polynomials, `EXPLICIT_POLYNOMIAL_ENUMERATION`: $\min |P(\gamma_1)| \ge 11.134725141734695$, $\min |P(\gamma_1+1/2)| \ge 11.634725141734695$, $\min |P(\rho_1)| \ge 14.143565845725995$).
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
| **Candidate 1** | $\gamma_n = \operatorname{Im}(\rho_n) > 0$ | $\mathbb{R}_{>0}$ | Primary real ordinate; rationality and algebraicity `NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT` (`OPEN_IN_LITERATURE`) |
| **Candidate 2** | $\rho_n = \beta_n + i\gamma_n = \frac{1}{2} + \delta_n + i\gamma_n$ | $\{s \in \mathbb{C} : 0 < \operatorname{Re}(s) < 1\}$ | Primary complex zero; $\rho_n \notin \mathbb{Q}$ `PROVED`; algebraicity `NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT` (`OPEN_IN_LITERATURE`) |
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

## F. Primary-Source Audit of Individual Zero Arithmetic (Repaired in `TASK-TC-038R`)

Every claim below was audited against primary sources (using `literature-search-arxiv` and standard reference monographs) and classified using the strict tokens of Sections 8, 22, 23, and 43:

| Question | Status Classification | Source Verification | Primary-Source Explanation |
| :--- | :--- | :--- | :--- |
| Is $\rho_n \notin \mathbb{Q}$ for every nontrivial zero $\rho_n$? | `PROVED` | `PRIMARY_SOURCE_VERIFIED` | Since $\zeta(s) < 0$ on $(0, 1)$ via $\eta(s) = (1-2^{1-s})\zeta(s) > 0$, every nontrivial zero in $0 < \operatorname{Re}(s) < 1$ has $\operatorname{Im}(\rho_n) \ne 0$, hence $\rho_n \notin \mathbb{R} \supset \mathbb{Q}$ (Titchmarsh 1986, §2.12). |
| Is $\gamma_1 \notin \mathbb{Q}$ (or any individual $\gamma_n \notin \mathbb{Q}$) proved? | `NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT` (`OPEN_IN_LITERATURE`) | `NO_PRIMARY_SOURCE_FOUND` | No theorem in the peer-reviewed or preprint literature establishes irrationality of $\gamma_1$ or any individual ordinate $\gamma_n$. |
| Is $\rho_1 \notin \overline{\mathbb{Q}}$ or $\gamma_1 \notin \overline{\mathbb{Q}}$ proved? | `NO_RESULT_FOUND_AFTER_PRIMARY_SOURCE_AUDIT` (`OPEN_IN_LITERATURE`) | `NO_PRIMARY_SOURCE_FOUND` | No theorem in the literature proves transcendence of any individual nontrivial zero $\rho_n$ or ordinate $\gamma_n$. |
| Does set cardinality imply transcendence of any $\gamma_n$, or does Northcott exclude fixed number fields unconditionally? | `CARDINALITY_DOES_NOT_IMPLY_ZERO_ORDINATE_TRANSCENDENCE` / `NO_INDIVIDUAL_ORDINATE_IRRATIONALITY_OR_TRANSCENDENCE_THEOREM_FOUND` | `PRIMARY_SOURCE_VERIFIED` | Hardy (1914), Selberg (1942), and Bui–Conrey–Young (2011) prove infinitely many distinct simple ordinates $\gamma_n$ exist, but $\{\gamma_n\}_{n \ge 1}$ and $\overline{\mathbb{Q}}$ are both **countably infinite**, so Cantor cardinality does **not** imply that any $\gamma_n$ is transcendental. Furthermore, a fixed number field $K$ is infinite; Northcott's theorem guarantees finiteness only for algebraic numbers of **both bounded degree $\le D$ and bounded height $\le H$** (`FIXED_NUMBER_FIELD_REQUIRES_BOUNDED_DEGREE_AND_BOUNDED_HEIGHT`). |
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
   - **Why Bessel zeros succeed where $\zeta(\rho) = 0$ fails**: $z^{-\nu} J_\nu(z)$ is a **Siegel $E$-function** satisfying a linear differential equation over $\mathbb{Q}(z)$, namely $z^2 y'' + z y' + (z^2 - \nu^2)y = 0$, with Taylor coefficients $c_k$ having factorial denominators $O((k!)^{-2})$ and algebraic growth. By contrast, $\zeta(s)$ and $\xi(s)$ are **differentially transcendental** (Hilbert 1900; Ostrowski 1920) — they satisfy no algebraic differential equation over $\mathbb{C}(s)$ — and their Taylor coefficients involve transcendental Stieltjes constants $\gamma_k^{\mathrm{St}}$ rather than algebraic rationals.

---

## H. Transcendence-Theorem Applicability Matrix

The following matrix audits all nine major transcendence theorem families against the target equation $\zeta(\rho) = 0$ for $\rho \in \{0 < \operatorname{Re}(s) < 1\} \cap \overline{\mathbb{Q}}$:

| Theorem Family | Exact Hypotheses | Target Attempted from $\zeta(\rho) = 0$ | Exact Missing Hypothesis | Applicability Classification |
| :--- | :--- | :--- | :--- | :--- |
| **1. Lindemann–Weierstrass** (1882/1885) | Distinct $\alpha_1, \dots, \alpha_m \in \overline{\mathbb{Q}} \implies e^{\alpha_1}, \dots, e^{\alpha_m}$ are algebraically independent over $\overline{\mathbb{Q}}$. | Apply to $p^{-\rho} = e^{-\rho \log p}$ under $\rho \in \overline{\mathbb{Q}}$. | The exponents $-\rho \log p$ are **transcendental** ($\log p \notin \overline{\mathbb{Q}}$ for prime $p$), not algebraic; and $\sum_{n=1}^\infty n^{-\rho}$ is an infinite series that diverges in $0 < \operatorname{Re}(\rho) < 1$. | `DOES_NOT_APPLY_MISSING_ALGEBRAIC_EXPONENT_AND_FINITENESS` |
| **2. Gelfond–Schneider** (1934) | $\alpha \in \overline{\mathbb{Q}} \setminus \{0, 1\}$ and $\beta \in \overline{\mathbb{Q}} \setminus \mathbb{Q} \implies \alpha^\beta \notin \overline{\mathbb{Q}}$. | Deduce $p^{-\rho} \notin \overline{\mathbb{Q}}$ for prime $p$ and $\rho \in \overline{\mathbb{Q}} \setminus \mathbb{Q}$, and seek contradiction with $\zeta(\rho) = 0$. | Gives $p^{-\rho} \notin \overline{\mathbb{Q}}$ for each prime $p$ when $\rho \in \overline{\mathbb{Q}} \setminus \mathbb{Q}$, but $\zeta(\rho) = 0$ does **not** force any single $p^{-\rho}$ or finite $\overline{\mathbb{Q}}$-combination of $p^{-\rho}$ to be algebraic. | `INDIVIDUAL_PRIME_POWERS_TRANSCENDENTAL_NO_CONTRADICTION_WITH_ZETA_ZERO` |
| **3. Baker's Theorem on Linear Forms in Logarithms** (1966) | $\beta_0 + \sum_{j=1}^m \beta_j \log \alpha_j \ne 0$ (with quantitative lower bound) for $\alpha_j \in \overline{\mathbb{Q}}^\times$, $\beta_j \in \overline{\mathbb{Q}}$. | Apply to $\sum_p c_p (-\rho \log p)$ or functional-equation phase $\log \chi(\rho) = 2\pi i k$. | $\zeta(\rho) = 0$ is a zero of an analytic continuation of an infinite sum of exponentials $\exp(-\rho \log n)$, not a linear form in logarithms of algebraic numbers; and $\chi(\rho) \ne 0$ for $0 < \operatorname{Re}(\rho) < 1$. | `DOES_NOT_APPLY_ZETA_ZERO_NOT_LINEAR_FORM_IN_LOGS` |
| **4. Siegel–Shidlovsky $E$-Function Theory** (1929/1959) | Tuple $(f_1(z), \dots, f_m(z))$ of Siegel $E$-functions ($\overline{\mathbb{Q}}$ Taylor coefficients with factorial denominators) satisfying a linear ODE system over $\mathbb{C}(z)$. | Treat $\xi(s)$ or $\zeta(s)$ as an $E$-function evaluated at $s = \rho \in \overline{\mathbb{Q}}$. | Both hypotheses fail: (i) $\zeta(s)$ and $\xi(s)$ satisfy **no** linear or algebraic ODE over $\mathbb{C}(s)$ (Hilbert–Ostrowski); (ii) Taylor coefficients of $\xi(s)$ or $\zeta(s)$ at any rational point are transcendental (involving $\gamma_E, \log\pi, \gamma_k^{\mathrm{St}}$), not in $\overline{\mathbb{Q}}$. | `DOES_NOT_APPLY_NOT_E_FUNCTION_NO_ODE_OVER_Q_S` |
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

## M. Second Reciprocal Zero Sum $S_2$ and Higher $S_m$ (`STIELTJES_NOTATION_DISAMBIGUATED`)

### 1. General Logarithmic Derivative Identity ($m \ge 2$)
Differentiating $\frac{\xi'(s)}{\xi(s)} = -\sum_{m=1}^\infty S_m s^{m-1}$ around $s = 0$ (and around $s = 1$ using $\xi(1-s) = \xi(s)$, formalized in Lean 4 as `reciprocal_power_log_derivative_sign_identity`):
$$\boxed{S_m := \sum_{\rho} \frac{1}{\rho^m} = -\frac{1}{(m-1)!} \left.\frac{d^m}{ds^m} \log \xi(s)\right|_{s=0} = \frac{(-1)^{m+1}}{(m-1)!} \left.\frac{d^m}{ds^m} \log \xi(s)\right|_{s=1} \qquad (m \ge 1).}$$
For every integer $m \ge 2$, $S_m$ **converges absolutely** by partial summation against $N(T) = \frac{T}{2\pi}\log\frac{T}{2\pi} - \frac{T}{2\pi} + O(\log T) = O(T\log T)$, since $\int_2^\infty T^{-m}\log T\,dT < \infty$ for $m \ge 2$.

### 2. Explicit Derivation of $S_2$ at both $s = 0$ and $s = 1$
Using the regular part at $s = 0$:
$$\frac{\xi'(s)}{\xi(s)} = \frac{1}{s-1} - \frac{1}{2}\log\pi + \frac{1}{2}\psi\!\left(1 + \frac{s}{2}\right) + \frac{\zeta'(s)}{\zeta(s)},$$
differentiating at $s = 0$ gives:
$$-\left.\frac{d}{ds}\frac{\xi'(s)}{\xi(s)}\right|_{s=0} = 1 - \frac{1}{4}\psi_1(1) - \left.\frac{d}{ds}\frac{\zeta'(s)}{\zeta(s)}\right|_{s=0}.$$
Since $\psi_1(1) = \zeta(2) = \frac{\pi^2}{6}$ and $\left.\frac{d}{ds}\frac{\zeta'(s)}{\zeta(s)}\right|_{s=0} = \frac{\zeta''(0)}{\zeta(0)} - \left(\frac{\zeta'(0)}{\zeta(0)}\right)^2 = -2\zeta''(0) - \log^2(2\pi)$:
$$\boxed{S_2 = 1 - \frac{\pi^2}{24} + 2\zeta''(0) + \log^2(2\pi).}$$
Expanding identically at $s = 1$ using the Laurent expansion $\zeta(s) = \frac{1}{s-1} + \gamma_E - \gamma_1^{\mathrm{St}}(s-1) + \frac{\gamma_2^{\mathrm{St}}}{2}(s-1)^2 - \dots$ (where $\gamma_k^{\mathrm{St}}$ are the Stieltjes constants, distinct from the zero ordinates $\gamma_n = \operatorname{Im}(\rho_n)$) and $\frac{1}{2}\psi(s/2)$ at $s = 1$ ($\psi_1(1/2) = \frac{\pi^2}{2}$):
$$\boxed{S_2 = 1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1^{\mathrm{St}} \approx -0.0461543172958046027571079903790773035302679623.}$$
Both expressions agree symbolically and to 50 decimal digits (residual $1.00 \times 10^{-51}$), linked by the classic functional-equation identity $2\zeta''(0) + \log^2(2\pi) = \gamma_E^2 - \frac{\pi^2}{12} + 2\gamma_1^{\mathrm{St}}$ (`s2_equivalent_closed_forms`).

### 3. Hierarchy Table for $S_1, S_2, S_3, S_4$

| $m$ | Convergence | Logarithmic Derivative Formula | Exact Closed-Form Expression | 50-Digit Numerical Value |
| :--- | :--- | :--- | :--- | :--- |
| $1$ | Conditionally convergent ($|\operatorname{Im}\rho| \le T$) | $-\left.\frac{d}{ds}\log\xi(s)\right|_{s=0}$ | $1 + \frac{\gamma_E}{2} - \log(2\sqrt{\pi})$ | $+0.02309570896612103381431024790649529162193$ |
| $2$ | Absolutely convergent | $-\left.\frac{d^2}{ds^2}\log\xi(s)\right|_{s=0}$ | $1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1^{\mathrm{St}}$ | $-0.04615431729580460275710799037907730353027$ |
| $3$ | Absolutely convergent | $-\frac{1}{2!}\left.\frac{d^3}{ds^3}\log\xi(s)\right|_{s=0}$ | $1 - \frac{7}{8}\zeta(3) + \gamma_E^3 + 3\gamma_E\gamma_1^{\mathrm{St}} + \frac{3}{2}\gamma_2^{\mathrm{St}}$ | $-0.0001111582314521059227626682389145784739642$ |
| $4$ | Absolutely convergent | $-\frac{1}{3!}\left.\frac{d^4}{ds^4}\log\xi(s)\right|_{s=0}$ | $1 - \frac{\pi^4}{96} + \gamma_E^4 + 4\gamma_E^2\gamma_1^{\mathrm{St}} + 2(\gamma_1^{\mathrm{St}})^2 + 2\gamma_E\gamma_2^{\mathrm{St}} + \frac{2}{3}\gamma_3^{\mathrm{St}}$ | $+0.00007362722126168951832677130703060151131283$ |

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
- $\lambda_2 = 2S_1 - S_2 = 1 + \gamma_E - 2\log(2\sqrt{\pi}) - \gamma_E^2 + \frac{\pi^2}{8} - 2\gamma_1^{\mathrm{St}} \approx +0.0923457352280466703857284861921$,
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

## Q. Arithmetic Status of Exact Zero-Sum Constants (`STIELTJES_NOTATION_DISAMBIGUATED`)

| Invariant | Exact Closed-Form Expression | Rationality Known? | Irrationality Known? | Transcendence Known? | Main Unresolved Constants Included |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $S_1 = \lambda_1 = \sum_\rho^{\mathrm{sym}} \rho^{-1}$ | $1 + \frac{\gamma_E}{2} - \log(2\sqrt{\pi})$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\gamma_E$, $\log(2\sqrt{\pi})$ (though $\log(2\sqrt{\pi}) \notin \overline{\mathbb{Q}}$, its $\mathbb{Q}$-independence from $\gamma_E$ is open) |
| $\sum_\rho \frac{1}{\rho(1-\rho)} = 2S_1 = 2\lambda_1$ | $2 + \gamma_E - \log(4\pi)$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\gamma_E - \log(4\pi)$ |
| $S_2 = \sum_\rho \rho^{-2}$ | $1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1^{\mathrm{St}}$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\gamma_E$, $\gamma_1^{\mathrm{St}}$ (first Stieltjes constant), $\pi^2$ |
| $S_3 = \sum_\rho \rho^{-3}$ | $1 - \frac{7}{8}\zeta(3) + \gamma_E^3 + 3\gamma_E\gamma_1^{\mathrm{St}} + \frac{3}{2}\gamma_2^{\mathrm{St}}$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\zeta(3)$, $\gamma_E$, $\gamma_1^{\mathrm{St}}$, $\gamma_2^{\mathrm{St}}$ |
| $S_4 = \sum_\rho \rho^{-4}$ | $1 - \frac{\pi^4}{96} + \gamma_E^4 + 4\gamma_E^2\gamma_1^{\mathrm{St}} + 2(\gamma_1^{\mathrm{St}})^2 + 2\gamma_E\gamma_2^{\mathrm{St}} + \frac{2}{3}\gamma_3^{\mathrm{St}}$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\pi^4$, $\gamma_E$, $\gamma_1^{\mathrm{St}}, \gamma_2^{\mathrm{St}}, \gamma_3^{\mathrm{St}}$ |
| $\Sigma_2 = \sum_\rho (\rho-1/2)^{-2}$ | $8 - \frac{1}{4}\psi_1(1/4) - \left.\frac{d^2}{ds^2}\log(-\zeta(s))\right|_{s=1/2}$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | Catalan's constant $G$ (via $\psi_1(1/4) = \pi^2 + 8G$), $\zeta'(1/2)/\zeta(1/2)$, $\zeta''(1/2)/\zeta(1/2)$ |
| $\lambda_n$ ($n \ge 1$) | $\sum_{j=1}^n (-1)^{j-1}\binom{n}{j} S_j$ | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | No (`OPEN_IN_LITERATURE`) | $\gamma_E, \log(4\pi), \pi^{2k}, \zeta(2k+1), \gamma_1^{\mathrm{St}}, \dots, \gamma_{n-1}^{\mathrm{St}}$ |

---

## R. Current Status of $\zeta(5)$ and Odd Zeta Values (Repaired in `TASK-TC-038R`)

In accordance with Sections 4–8 of `TASK-TC-038R`, we updated the primary-source literature and formalization verification of $\zeta(5)$ through October 2026:

1. **Archimedean $\zeta(5) = \sum_{n=1}^\infty n^{-5} \in \mathbb{R}$ (September 2026 Development)**:
   - **2026 Preprint Claim (`ZETA5_IRRATIONALITY_2026_PREPRINT_CLAIM`)**: On 17 September 2026, Aabir Fauzan (Aalto University) posted *"$\zeta(5)$ is irrational"* (Zenodo record `22826419`, DOI `10.5281/zenodo.22826419`), constructing a $37n \times 37n$ Hankel determinant $\Delta_K(X)$ ($K=40n, N=3n, h=37n$) whose normalization $Q_n(X) = m_N(n)S_K\Delta_K(X) \in \mathbb{Z}[X]$ has degree $37n$ and satisfies $0 < Q_n(\zeta(5)) < \exp(-c n^2)$, proving $\zeta(5) \notin \mathbb{Q}$.
   - **Public Lean 4 Formalization (`ZETA5_IRRATIONALITY_FORMALIZED_IN_LEAN`, `LEAN_PROVED_EXTERNAL_REPOSITORY`, `SOURCE_AUDITED_BUILD_NOT_LOCALLY_REPRODUCED`)**: The companion repository `https://github.com/mo271/Zeta5` (commit `7fe736760f4b96bfdb4334b68e3b3124ecbe10b0`) formalizes the proof in Lean 4 (`v4.34.0-rc1`) across 251 `.lean` files in `Apery/` plus `Solution.lean`, exporting `Apery.irrational_zeta5 : Irrational Apery.zeta5`, `Apery.irrational_five : ∃ x, Irrational x ∧ riemannZeta 5 = x`, and `RiemannZetaValues.irrational_five : ∃ x, Irrational x ∧ riemannZeta 5 = x`.
   - **Dependency & Axiom Graph (`ZETA5_FORMALIZATION_DEPENDENCY_GRAPH_CLEAN`)**: Direct audit of `Apery/` and `Solution.lean` confirms `0 sorry`, `0 admit`, `0 axiom`, and `#print axioms Apery.irrational_five` = `[propext, Classical.choice, Quot.sound]`.
   - **Conventional Peer Review (`PEER_REVIEW_STATUS_PENDING`)**: Conventional journal peer review of the September 2026 preprint is pending as of October 2026. (Earlier July 2024 preprint `arXiv:2407.07121` by S. Suman remains refuted by Chen et al. `arXiv:2411.16774v3`.)
2. **Classical & 2-adic Odd Zeta Theorems in Peer-Reviewed Literature**:
   - **Apéry (1979) / Beukers (1979)**: $\zeta(3) \notin \mathbb{Q}$ (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).
   - **Rivoal (2000) & Ball–Rivoal (2001)**: $\dim_{\mathbb{Q}} \operatorname{span}_{\mathbb{Q}}(1, \zeta(3), \zeta(5), \dots, \zeta(2n+1)) \ge \frac{1 + o(1)}{1 + \log 2}\log n$ (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).
   - **Zudilin (2001, `arXiv:math/0104249v1`)**: At least one of $\{\zeta(5), \zeta(7), \zeta(9), \zeta(11)\}$ is irrational (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).
   - **Rivoal–Zudilin (2018/2020, `arXiv:1803.03160v1`)**: At least two of $\{\zeta(5), \zeta(7), \dots, \zeta(69)\}$ are irrational (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).
   - **Fischler–Sprang–Zudilin (2019, `arXiv:1803.08905v2`)**: At least $2^{(1-\varepsilon)\frac{\log s}{\log\log s}}$ odd zeta values up to $s$ are irrational (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).
   - **Lai–Sprang–Zudilin (May 2025, `arXiv:2505.05005v2`)**: The 2-adic Kubota–Leopoldt zeta value $\zeta_2(5) \in \mathbb{Q}_2$ is irrational (`PROVED`, `PRIMARY_SOURCE_VERIFIED`).

---

## S. Special-Value Method Transfer Test (Repaired in `TASK-TC-038R`)

See Repair Sections **C**, **D**, and **E** above for the complete comparison between classical linear-form methods (`SPECIAL_VALUE_IRRATIONALITY_METHOD_HAS_NO_DIRECT_ZERO_LOCATION_TRANSFER`) and Fauzan's 2026 Hankel determinant architecture (`FAUZAN_HANKEL_ZERO_LOCATION_TRANSFER_UNRESOLVED`, `VALUE_POLYNOMIAL_ARCHITECTURE_NEQ_ARGUMENT_POLYNOMIAL_ARCHITECTURE`, `SUBGATE-TC-039A`).

---

## T. Auxiliary-Polynomial Requirements for $\rho_1$ and $\gamma_1$

To prove that $\alpha \in \{\rho_1, \gamma_1\}$ is irrational or transcendental via an auxiliary polynomial sequence $P_n(X) \in \mathbb{Z}[X]$ of degree $d_n \le C n$ and naive height $H(P_n)$:
1. **Nonvanishing certificate**: $P_n(\alpha) \ne 0$ for infinitely many $n$.
2. **Liouville–Mahler algebraic lower bound**: If $\alpha \in \overline{\mathbb{Q}}$ has degree $D = [\mathbb{Q}(\alpha):\mathbb{Q}]$ and Mahler measure $M(\alpha)$, then
   $$\log |P_n(\alpha)| \ge -(D - 1)\log H(P_n) - d_n \log M(\alpha) - (D - 1)\log(d_n + 1).$$
   - For $D = 1$ ($\gamma_1 \in \mathbb{Q}$), $(D-1)\log H(P_n) = 0$, so any quadratic log-decay $\log |P_n(\gamma_1)| \le -c n^2$ ($c > 0$) with $d_n = O(n)$ proves $\gamma_1 \notin \mathbb{Q}$ regardless of whether $\log H(P_n) = O(n^2)$.
   - For $D \ge 2$ (needed for non-real $\rho_1$ or algebraic $\gamma_1$ of degree $D \ge 2$), $(D-1)\log H(P_n)$ does not vanish, so quadratic log-height $\log H(P_n) \sim A n^2$ competes directly with $-c n^2$.
3. **Why naive Taylor/Dirichlet truncations do not supply $P_n(X) \in \mathbb{Z}[X]$**:
   - Truncating the Taylor series of $\xi(s)$ or $\zeta(s)$ produces coefficients involving $\log\pi, \gamma_E$, and the Stieltjes constants $\gamma_k^{\mathrm{St}} \notin \mathbb{Q}$.
   - Truncating $\sum_{m=1}^N m^{-s}$ produces exponential polynomials in $p^{-s}$, not algebraic polynomials in $s$.
   - Whether a Hankel/Hermite/Gram determinant in an argument variable $X \in \{\gamma_1, \rho_1\}$ can overcome these barriers is tracked under `SUBGATE-TC-039A` (Gates `Z1`–`Z6`).

---

## U. Gamma and Differential-Transcendence Firewalls

### 1. Gamma-Function Arithmetic Firewall (Section 28)
In $\xi(s) = \frac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$:
- $\Gamma(s/2)$ has **no zeros anywhere in $\mathbb{C}$** ($\frac{1}{\Gamma(z)}$ is entire) and its poles lie at $s \in \{0, -2, -4, -6, \dots\}$, which are disjoint from the critical strip $0 < \operatorname{Re}(s) < 1$.
- Consequently, inside $0 < \operatorname{Re}(s) < 1$, the factor $\frac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)$ is **everywhere finite and nonvanishing**, so:
  $$\xi(\rho) = 0 \iff \zeta(\rho) = 0 \qquad (0 < \operatorname{Re}(\rho) < 1).$$

### 2. Differential-Transcendence Firewall (Section 29)
By Hölder (1887) for $\Gamma(s)$ and Hilbert (1900) / Ostrowski (1920) for $\zeta(s)$, neither $\Gamma(s)$ nor $\zeta(s)$ satisfies any nontrivial algebraic differential equation over $\mathbb{C}[s]$. However, $g(s) := 1/\Gamma(s)$ is an entire differentially transcendental function whose zero set is $\{0, -1, -2, \dots\} \subset \mathbb{Z} \subset \mathbb{Q}$, proving:
$$\boxed{\texttt{DIFFERENTIAL\_TRANSCENDENCE\_DOES\_NOT\_DETERMINE\_ZERO\_ARITHMETIC}.}$$

---

## V. Certified Finite Polynomial and Bounded-Denominator Exclusions (Repaired Scope)

All finite computational exclusions are executed in 128-bit outward Arb/Acb ball arithmetic (`tc/zero_arithmetic_invariants.py`) and strictly separated from analytic proofs.

### 1. Certified First-Zero Enclosures (128-bit Arb IVT)
Using the real critical-line Hardy/xi function $\operatorname{Re}(\pi^{-it/2}\Gamma(1/4 + it/2)\zeta(1/2 + it))$, 128-bit Arb certifies a strict sign change across $[\gamma_1 - 10^{-30}, \gamma_1 + 10^{-30}]$, giving the certified outward enclosures:
- $\gamma_1 \in [14.134725141734693790457251983562470270784257115699 \pm 10^{-30}]$,
- $\gamma_1 + \frac{1}{2} \in [14.634725141734693790457251983562470270784257115699 \pm 10^{-30}]$,
- $\rho_1 = \frac{1}{2} + i\gamma_1$.

### 2. Polynomial Normalization Rules (Section 31)
Every candidate polynomial $P(X) = a_0 + a_1 X + \dots + a_d X^d \in \mathbb{Z}[X]$ is normalized so that $1 \le d \le D$, $a_d \ge 1$, $\max_{0 \le j \le d} |a_j| \le H$, $\gcd(|a_0|, \dots, |a_d|) = 1$, and the zero polynomial is excluded.

### 3. Certified Finite Algebraic-Relation Exclusions (`CERTIFIED_FINITE_DEGREE_HEIGHT_ALGEBRAICITY_EXCLUSION`)
1. **Exhaustive Enumeration on Small Box ($D = 4, H = 3$, `EXPLICIT_POLYNOMIAL_ENUMERATION`)**:
   All $8{,}160$ normalized primitive polynomials with $1 \le d \le 4$ and $H \le 3$ are evaluated individually in 128-bit Arb/Acb arithmetic on $\gamma_1$, $\gamma_1 + 1/2$, and $\rho_1$, yielding **certified full-box global minima** over $D \le 4, H \le 3$:
   - $\min_{1 \le d \le 4, H \le 3} |P(\gamma_1)|_{\text{lower}} = 11.134725141734695 > 0$,
   - $\min_{1 \le d \le 4, H \le 3} |P(\gamma_1 + 1/2)|_{\text{lower}} = 11.634725141734695 > 0$,
   - $\min_{1 \le d \le 4, H \le 3} |P(\rho_1)|_{\text{lower}} = 14.143565845725995 > 0$.
2. **Hierarchical Outward Box Exclusion on Large Box ($D \le 4, H \le 100$, `HIERARCHICAL_BOX_EXCLUSION`, `FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED`)**:
   Across all $158{,}062{,}321{,}920$ normalized primitive integer polynomials with $1 \le d \le 4$ and $\max_j |a_j| \le 100$ ($12{,}175$ for $d=1$; $3{,}355{,}121$ for $d=2$; $749{,}507{,}743$ for $d=3$; $157{,}309{,}446{,}881$ for $d=4$), 128-bit outward Arb/Acb branch-and-leaf interval enclosures certify:
   $$\boxed{\forall P \in \mathcal{P}_{\mathrm{prim}}(D \le 4, H \le 100): \quad 0 \notin P(I_{\gamma_1}), \quad 0 \notin P(I_{\gamma_1+1/2}), \quad 0 \notin P(I_{\rho_1}).}$$
   Because pruned branches are excluded in aggregate without minimizing $|P|$ over every pruned lattice point (`Route A`, Section 20.1), no global minimum $|P|$ is claimed over the $D \le 4, H \le 100$ box (`FULL_BOX_GLOBAL_MINIMUM_NOT_CERTIFIED`).

### 4. Certified Bounded-Denominator Rational Exclusion (`CERTIFIED_BOUNDED_DENOMINATOR_RATIONAL_EXCLUSION`)
Across all rational numbers $p/q$ with $1 \le q \le 10{,}000$ and $p \in \mathbb{Z}$, 128-bit Arb certifies $0 \notin q I_{\gamma_1} - p$ and $0 \notin q I_{\gamma_1+1/2} - p$:
$$\min_{\substack{1 \le q \le 10000 \\ p \in \mathbb{Z}}} \left|\gamma_1 - \frac{p}{q}\right| \ge 9.50797348022772 \times 10^{-10} > 0 \quad \text{at } \frac{p}{q} = \frac{94109}{6658},$$
$$\min_{\substack{1 \le q \le 10000 \\ p \in \mathbb{Z}}} \left|\left(\gamma_1 + \frac{1}{2}\right) - \frac{p}{q}\right| \ge 9.50797348022772 \times 10^{-10} > 0 \quad \text{at } \frac{p}{q} = \frac{48719}{3329}.$$

### 5. Diagnostic PSLQ Firewall (`NUMERICAL_EVIDENCE_ONLY`)
An 80-digit `mpmath.pslq` diagnostic check on $[1, \gamma_1, \dots, \gamma_1^4]$ and $[1, \gamma_1 + 1/2, \dots, (\gamma_1 + 1/2)^4]$ with `maxcoeff=1000` returns `None` (no relation found). This is classified solely as `NUMERICAL_EVIDENCE_ONLY` and never promoted to a mathematical proof or certified exclusion.

---

## W. TC Interaction and Ambient-Kernel Firewall

We audited whether an assumed algebraic zero $\rho \in \overline{\mathbb{Q}}$ or algebraic ordinate $\gamma \in \overline{\mathbb{Q}}$ interacts with the TC ambient kernel or the exceptional exponent set $\mathcal{S}_\tau := \{\alpha \in \mathbb{A}_{\mathbb{R}} : \tau^\alpha \in \overline{\mathbb{Q}}\}$, $\mathbb{A}_{\mathbb{R}} = \overline{\mathbb{Q}} \cap \mathbb{R}$, $\tau = 2\pi$:
1. When $\rho = \beta + i\gamma$ is a nontrivial zero ($\gamma \ne 0$), $K\rho \notin \mathbb{R}$ for $K \in \mathbb{A}_{\mathbb{R}} \setminus \{0\}$, so $\tau^{K\rho}$ is not a positive real ambient grade.
2. Even if $\rho \in \overline{\mathbb{Q}}$ so $\beta, \gamma, \delta \in \mathbb{A}_{\mathbb{R}}$, $\zeta(\rho) = 0$ imposes no algebraic relation on $\tau^\beta$, $\tau^\gamma$, or $\tau^{2\delta_\rho}$ (`ALGEBRAIC_ZERO_DOES_NOT_AUTOMATICALLY_ENTER_AMBIENT_KERNEL`).

---

## X. Exact Remaining Subgates (`SUBGATE-TC-038A`, `SUBGATE-TC-039A`, `OBL-CT-001A`)

1. **`OBL-CT-001A = OPEN`**: The primary TC spectral-to-arithmetic bridge obligation remains open; `TASK-TC-038` / `TASK-TC-038R` is recorded on `ZERO_ARITHMETIC_BRANCH`.
2. **`SUBGATE-TC-038A = OPEN` (`ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE`)**:
   Prove irrationality of $2\lambda_1 = 2 + \gamma_E - \log(4\pi)$ (equivalently $\gamma_E - \log(4\pi) \notin \mathbb{Q}$), or prove $\dim_{\mathbb{Q}}\operatorname{span}_{\mathbb{Q}}(1, S_1, S_2) \ge 2$ where $S_2 = 1 + \gamma_E^2 - \frac{\pi^2}{8} + 2\gamma_1^{\mathrm{St}}$.
3. **`SUBGATE-TC-039A = OPEN` (`FAUZAN_HANKEL_TO_ZERO_ARGUMENT_TRANSFER_SUBGATE`)**:
   Test Gates `Z1`–`Z6` in `TASK-TC-039` to determine whether Fauzan's 2026 Hankel/Hermite/Gram/potential-theoretic determinant architecture can be adapted from value-polynomial evaluation at $X = \zeta(5)$ to argument-polynomial evaluation at $X \in \{\gamma_1, \rho_1\}$.
