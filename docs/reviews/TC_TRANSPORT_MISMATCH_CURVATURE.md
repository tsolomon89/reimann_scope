# Infinitesimal Transport-Mismatch Curvature and Non-Scalar Arithmetic Descent (`TASK-TC-034` / `TASK-TC-034R`)

**Task ID:** `TASK-TC-034` (Repaired in `TASK-TC-034R`)  
**Starting Commit (`TASK-TC-034R`):** `9f4701280a05c5c4ba9dc8be8d2bdb968588c799`  
**Substantive Parent (`TASK-TC-034`):** `684c324960c8cfb3014808004926bb4d157c2fd9`  
**Audited Obligation:** `OBL-CT-001A` (`OPEN`)  
**Principal Classification:** `MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A`  
**Task Completion Classification:** `TASK_TC_034R_TRANSPORT_CURVATURE_REPAIR_COMPLETE`  
**Secondary Classifications:** `COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED`, `COMPACT_SUPPORT_ARITHMETIC_CURVATURE_SIGN_INDEFINITE`, `COMPACT_SUPPORT_NEGATIVE_ARITHMETIC_CURVATURE_CERTIFIED`, `COMPACT_SUPPORT_POSITIVE_ARITHMETIC_CURVATURE_CERTIFIED`, `FINITE_ACCIDENTAL_ARITHMETIC_CURVATURE_ZERO`, `THETA_MELLIN_AUDIT_CONDITIONAL`, `SPECTRAL_CURVATURE_IS_SIGNED_OR_DOUBLE_SUM`, `CURVATURE_POSITIVITY_IS_RH_EQUIVALENT`, `GENERIC_SCALE_CURVATURE`, `OBL_CT_001A_OPEN`, `CANDIDATE_FAILURE_DOES_NOT_REFUTE_TC`  
**Evidence Class Split:**
- `LEAN_PROVED` (`formal/RiemannScope/TransportMismatchCurvature.lean`, 18 declarations: 1 `def` + 17 `theorem`s, bringing repository compiled `theorem` declarations to **565**; 0 `sorry`, 0 `admit`, no nonstandard project axioms introduced): algebraic curvature determinant `curvatureDet`, Lagrange sum-of-squares identities, Euler-homogeneous moment consequence ($A_1=dA_0, A_2=d^2A_0 \implies A_0A_2-A_1^2=0$), grade-$K$ normalization independence, even second-difference identity, centered pairing algebra, signed-weight countermodel, and generic-base scaling identity.
- `PROVED_PAPER_DERIVATION`: compact-support Euler-PDE homogeneity no-go ($F_0 \in C_c^\infty((0,\infty)^2), \mathcal E F_0 = d F_0 \implies F_0 \equiv 0$), smooth $C^\infty$ plateau compactification $\mathrm{X}_N$ preserving station jets up to order $2$, and complete two-variable explicit formula spectral pairing analysis.
- `CERTIFIED_FINITE` (128-bit outward Arb ball arithmetic in `tc/transport_mismatch_curvature.py` and `data/tc_transport_mismatch_curvature.json`): complete compact-support arithmetic curvature enclosures $\sup \mathfrak C_{\mathrm{arith}}(\widetilde G_-) < 0$ and $\inf \mathfrak C_{\mathrm{arith}}(\widetilde G_+) > 0$ for $\widetilde G_\pm = \mathrm{X}_{15} G_\pm \in C_c^\infty((0,\infty)^2)$.
- `CONDITIONAL` / `OPEN`: candidate bilinear theta–Mellin audit (`CANDIDATE_THETA_MELLIN_AUDIT` / `THETA_MELLIN_AUDIT_CONDITIONAL`) and canonical open obligation `OBL-CT-001A`.

---

### A. TASK-TC-033 transport–moment incompatibility

In `TASK-TC-033` (`docs/reviews/TC_THREE_GRADE_HANKEL_CONSTRAINT.md`), the transported two-variable kernel family
$$F_{K,b}(x,y) = \tau^{aK} F_0\!\left(\tau^{-bK}x, \tau^{-bK}y\right), \qquad \tau = 2\pi,$$
was audited across grades $K \in \{-1, 0, +1\}$. That audit established the theorem **`TRANSPORT_MOMENT_INCOMPATIBILITY_PROVED`**:
1. At the unique label-preserving transport $b = 1$, every grade samples the identical native prime-power stations $(n,m)$ with $F_{K,1}(\tau^K n, \tau^K m) = \tau^{aK} F_0(n,m)$, yielding an exact rank-one geometric sequence $M_K = \tau^{aK} M_0$ with vanishing three-grade Hankel determinant $\mathcal H_0(M) = M_{-1}M_1 - M_0^2 = 0$, **but** simultaneously canceling the zero-dependent spectral grade factor:
   $$\tau^{(b-1)K(\rho+\sigma)}\Big|_{b=1} = 1.$$
2. For any finite displacement $b \neq 1$, the spectral factor $\tau^{(b-1)K(\rho+\sigma)}$ retains grade variation, **but** the arithmetic side evaluates $F_0(\tau^{(1-b)K}n, \tau^{(1-b)K}m)$ at shifted stations across grades, destroying the rank-one arithmetic identity $\mathcal H_0(M) = 0$.

`TASK-TC-034` tests whether the missing constraint resides in the **infinitesimal second variation (curvature)** around the unique compatible transport $b = 1$ ($b = 1 + \eta$, $\eta \to 0$) rather than in finitely displaced transport values.

---

### B. Hypothesis versus implementation

In accordance with the Section 2 Hypothesis-Fidelity Rule, we maintain a strict separation between four levels:

1. **General TC Hypothesis:**
   $$\boxed{\text{The same arithmetic object across transcendental grades implies a constraint.}}$$
2. **Candidate Implementation (`TASK-TC-034`):**
   $$\boxed{\text{The constraint is the infinitesimal transport-mismatch curvature around } b = 1.}$$
3. **Admissible Test Space / Kernel Class:** Smooth compactly supported two-variable kernels $F_0 \in C_c^\infty((0,\infty)^2)$ (Phase I) and candidate bilinear scale-mismatched theta–Mellin forms (Phase II).
4. **Scope of Negative Conclusions (`CANDIDATE_FAILURE_DOES_NOT_REFUTE_TC`):** Failure of this infinitesimal mismatch-curvature candidate on compactly supported two-variable kernels and candidate bilinear theta–Mellin forms refutes **this candidate implementation and test space**, **never** the general TC hypothesis.

---

### C. Relative transport parameter

Write the transport exponent around the unique label-preserving point $b = 1$ as
$$b = 1 + \eta, \qquad \eta \in \mathbb{R},$$
and define the mismatch-transported kernel
$$F_{K,\eta}(x,y) = \tau^{aK} F_0\!\left(\tau^{-(1+\eta)K}x, \tau^{-(1+\eta)K}y\right).$$
Pairing $F_{K,\eta}$ against the grade-$K$ prime-power measure $\mu_K = \sum_{n\ge 2}\Lambda(n)\delta_{\tau^K n}$ and normalizing out the scalar amplitude $\tau^{aK}$ yields the normalized equal-grade arithmetic mismatch energy:
$$\widehat{\mathcal M}_K(\eta) = \tau^{-aK}\langle \mu_K \otimes \mu_K, F_{K,\eta}\rangle = \sum_{n,m\ge 2}\Lambda(n)\Lambda(m)\,F_0\!\left(\tau^{-\eta K}n, \tau^{-\eta K}m\right).$$
At the compatibility point $\eta = 0$:
$$\widehat{\mathcal M}_K(0) = \sum_{n,m\ge 2}\Lambda(n)\Lambda(m)F_0(n,m) = \widehat{\mathcal M}_0(0) \qquad \forall K \in \mathbb{R},$$
recovering the exact value-level compatibility of `TASK-TC-033`.

---

### D. Arithmetic Euler derivatives

Define the two-variable Euler scaling generator:
$$\mathcal E = x\frac{\partial}{\partial x} + y\frac{\partial}{\partial y}.$$
Writing $u = -\eta K \log\tau$, the chain rule along the scaling ray $(e^u x, e^u y)$ gives
$$\left.\frac{\partial^j}{\partial \eta^j} F_0\!\left(\tau^{-\eta K}x, \tau^{-\eta K}y\right)\right|_{\eta=0} = (-K\log\tau)^j \bigl(\mathcal E^j F_0\bigr)(x,y) \qquad (j \ge 0).$$
When $F_0 \in C_c^\infty((0,\infty)^2)$ has compact support, only finitely many prime-power pairs $(n,m)$ lie in a neighborhood of $\operatorname{supp}(F_0)$ for $|\eta|$ sufficiently small, so differentiation under the sum is exact with no infinite-series tail issue. Defining the zero-independent arithmetic Euler moments
$$A_j(F_0) = \sum_{n,m\ge 2}\Lambda(n)\Lambda(m)\bigl(\mathcal E^j F_0\bigr)(n,m),$$
we obtain:
$$\widehat{\mathcal M}_K^{(j)}(0) = (-K\log\tau)^j A_j(F_0),$$
and in particular:
$$\widehat{\mathcal M}_K(0) = A_0(F_0), \qquad \widehat{\mathcal M}_K'(0) = -K\log\tau\,A_1(F_0), \qquad \widehat{\mathcal M}_K''(0) = K^2(\log\tau)^2 A_2(F_0).$$

---

### E. Arithmetic curvature determinant, smooth compactification, and certified sign indefiniteness

The arithmetic transport curvature is defined by
$$\mathfrak C_{\mathrm{arith}}(F_0) = A_0(F_0)A_2(F_0) - A_1(F_0)^2.$$
For any nonzero grade $K \neq 0$, the $(-K\log\tau)$ factors cancel upon normalization (`mismatch_curvature_k_independent` in `formal/RiemannScope/TransportMismatchCurvature.lean`):
$$\mathfrak C_{\mathrm{arith}}(F_0) = \frac{\widehat{\mathcal M}_K(0)\widehat{\mathcal M}_K''(0) - \bigl(\widehat{\mathcal M}_K'(0)\bigr)^2}{K^2(\log\tau)^2}.$$

#### 1. Explicit Smooth Compactification Operator $\mathrm{X}_N$ (`TASK-TC-034R` Sections 4–5)
To construct genuine compactly supported witnesses in $C_c^\infty((0,\infty)^2)$ whose **complete infinite arithmetic sums** are finite without truncation, define:
$$h(t) = \begin{cases} 0, & t \le 0, \\ e^{-1/t}, & t > 0, \end{cases} \qquad S(t) = \frac{h(t)}{h(t) + h(1-t)},$$
and the one-dimensional $C^\infty$ plateau cutoff for $0 < a < b < c < d$:
$$\chi_{a,b,c,d}(x) = S\!\left(\frac{x-a}{b-a}\right) S\!\left(\frac{d-x}{d-c}\right).$$
For $N = 15$, choose rational endpoints:
$$a = \frac{3}{2} = 1.5, \qquad b = \frac{7}{4} = 1.75, \qquad c = N + \frac{1}{4} = 15.25, \qquad d = N + \frac{1}{2} = 15.5,$$
and set $\mathrm{X}_{15}(x,y) = \chi_{15}(x)\chi_{15}(y)$ and $\widetilde G_{15}(x,y) = \mathrm{X}_{15}(x,y)G(x,y)$.
- **Complete Support Boundary:** $\operatorname{supp}(\widetilde G_{15}) \subset [1.5, 15.5]^2 \subset (0,\infty)^2$. Every integer $n \ge 16$ (and $n \le 1$) lies strictly outside $[1.5, 15.5]$, so $(\mathcal E^j \widetilde G_{15})(n,m) = 0$ for all $\max(n,m) \ge 16$.
- **Order-2 Jet Preservation at Active Stations:** Every active prime-power station $n \in \{2, 3, 4, 5, 7, 8, 9, 11, 13\}$ lies strictly inside the open plateau $(1.75, 15.25)$ where $\mathrm{X}_{15} \equiv 1$, $\mathcal E\mathrm{X}_{15} \equiv 0$, and $\mathcal E^2\mathrm{X}_{15} \equiv 0$. Consequently:
  $$(\mathcal E^j \widetilde G_{15})(n,m) = (\mathcal E^j G)(n,m) \qquad \forall\, 2 \le n,m \le 15, \; j \in \{0,1,2\},$$
  and the finite sum over $2 \le n,m \le 15$ ($81$ active pairs) is the **complete infinite arithmetic sum** $A_j(\widetilde G_{15})$ (`COMPLETE_COMPACT_SUPPORT_SUM`), not a truncation of an infinite series.

#### 2. Outward 128-bit Arb Certified Compact-Support Witnesses (`TASK-TC-034R` Sections 6–8, 10)
Using exact analytic formulas for $G_\pm, \mathcal E G_\pm, \mathcal E^2 G_\pm$ and computing $\Lambda(n) = \log p$ inside 128-bit Arb (`certify_compact_witness_curvature_arb` in `tc/transport_mismatch_curvature.py`, which fails closed with `ARB_CERTIFICATION_NOT_AVAILABLE` if `flint` is unavailable):
1. **Negative-Curvature Compact-Support Witness $\widetilde G_- = \mathrm{X}_{15} G_- \in C_c^\infty((0,\infty)^2)$ (`COMPACT_SUPPORT_NEGATIVE_ARITHMETIC_CURVATURE_CERTIFIED`):**
   $$G_-(x,y) = \exp\!\left(-\frac{3}{2}w^2\right), \quad (\mathcal E G_-)(x,y) = -6w\,G_-(x,y), \quad (\mathcal E^2 G_-)(x,y) = (36w^2 - 12)\,G_-(x,y), \quad w = \log\frac{xy}{16}.$$
   Complete compact-support Arb enclosure:
   $$\mathfrak C_{\mathrm{arith}}(\widetilde G_-) \in [-6442.34295182745976846022999751473105 \pm 8.42 \times 10^{-33}] \implies \sup \mathfrak C_{\mathrm{arith}}(\widetilde G_-) < 0.$$
2. **Positive-Curvature Compact-Support Witness $\widetilde G_+ = \mathrm{X}_{15} G_+ \in C_c^\infty((0,\infty)^2)$ (`COMPACT_SUPPORT_POSITIVE_ARITHMETIC_CURVATURE_CERTIFIED`):**
   $$G_+(x,y) = \cosh\!\left(\frac{6}{5}w\right)\exp\!\left(-\frac{2}{25}w^2\right), \qquad w = \log\frac{xy}{25}, \quad a = \frac{6}{5}, \quad b = \frac{2}{25},$$
   $$(\mathcal E G_+)(x,y) = 2\bigl(a\sinh(aw) - 2bw\cosh(aw)\bigr)e^{-bw^2}, \qquad (\mathcal E^2 G_+)(x,y) = 4\Bigl[\bigl(a^2 - 2b + 4b^2w^2\bigr)\cosh(aw) - 4abw\sinh(aw)\Bigr]e^{-bw^2}.$$
   Complete compact-support Arb enclosure:
   $$\mathfrak C_{\mathrm{arith}}(\widetilde G_+) \in [+191887.248334839729574771407499577571 \pm 6.37 \times 10^{-31}] \implies \inf \mathfrak C_{\mathrm{arith}}(\widetilde G_+) > 0.$$
3. **Sign-Indefiniteness Theorem (`COMPACT_SUPPORT_ARITHMETIC_CURVATURE_SIGN_INDEFINITE`):**
   $$\exists\, F_-, F_+ \in C_c^\infty((0,\infty)^2), \quad F_- \ge 0, \; F_+ \ge 0, \quad \mathfrak C_{\mathrm{arith}}(F_-) < 0, \quad \mathfrak C_{\mathrm{arith}}(F_+) > 0.$$
   This supersedes the earlier `FINITE_TRUNCATION_SIGN_INDEFINITENESS_OBSERVED` status.

#### 3. Accidental-Zero Boundary (`FINITE_ACCIDENTAL_ARITHMETIC_CURVATURE_ZERO`, `TASK-TC-034R` Section 9)
We explicitly distinguish two scopes where an accidental zero curvature occurs:
- **Complete-support plateau kernel $\mathrm{X}_3$ on $(1.5, 3.5)^2$:** The complete support of $\mathrm{X}_3$ contains only active stations $\{2,3\}$, which lie inside the flat plateau $[1.75, 3.25]^2$ where $\mathcal E\mathrm{X}_3 = \mathcal E^2\mathrm{X}_3 = 0$, giving $A_1(\mathrm{X}_3) = A_2(\mathrm{X}_3) = 0$ and $\mathfrak C_{\mathrm{arith}}(\mathrm{X}_3) = 0$. This is an accidental plateau zero (placing the cutoff ramp in the integer-free gap $(3.25, 3.5)$), not Euler homogeneity $\mathcal E\mathrm{X}_3 = d\mathrm{X}_3$.
- **Fixed kernel $F_{\mathrm{acc}}$ on $(1.5, 5.5)^2$ across restricted subset vs. complete support:** Holding $F_{\mathrm{acc}}(x,y) = \chi_{1.5, 1.75, 3.25, 5.5}(x)\chi_{1.5, 1.75, 3.25, 5.5}(y)$ fixed, its restricted partial sum on $\{2,3\}$ ($n_{\max}=3$) has zero curvature ($0.0$), whereas its **complete support sum** on $\{2,3,4,5\}$ ($n_{\max}=5$) has strictly negative curvature ($\approx -267.198 < 0$) because stations $4$ and $5$ lie on the transition ramp $(3.25, 5.5)$.

---

### F. Positive exponential curvature identity

For any finite exponential mixture with positive weights
$$M(\eta) = \sum_{j=1}^r w_j e^{\eta x_j}, \qquad w_j > 0, \; x_j \in \mathbb{R},$$
Lagrange's identity gives:
$$M(0)M''(0) - M'(0)^2 = \left(\sum_{i=1}^r w_i\right)\left(\sum_{j=1}^r w_j x_j^2\right) - \left(\sum_{i=1}^r w_i x_i\right)^2 = \frac{1}{2}\sum_{i,j=1}^r w_i w_j (x_i - x_j)^2 \ge 0.$$
This is machine-checked in Lean 4 (`single_exponential_log_curvature_zero`, `two_exponential_curvature_identity`, `two_exponential_positive_log_curvature`, `positive_finite_exponential_curvature_nonneg`, `three_exponential_curvature_identity`, `three_exponential_curvature_nonneg`, and `reciprocal_pair_curvature_strict_pos` in `formal/RiemannScope/TransportMismatchCurvature.lean`). When weights are allowed to be signed ($w_1 = 1, w_2 = -2, x_1 = 0, x_2 = 1$), $M(0)M''(0) - M'(0)^2 = -2 < 0$ (`signed_weight_curvature_negative`).

---

### G. Mellin-side mismatch derivatives

Under the repository's two-variable Mellin convention,
$$H_{K,\eta}(s,t) = \iint_{(0,\infty)^2} F_{K,\eta}(x,y)\,x^{s-1}y^{t-1}\,dx\,dy = \tau^{K(a + (1+\eta)(s+t))} H_0(s,t).$$
Combining $H_{K,\eta}(s,t)$ with the grade-$K$ prime-measure scaling factors $\tau^{-K(s+t)}$ and normalizing by $\tau^{-aK}$ yields the net spectral mismatch factor (`mellin_mismatch_net_exponent` in `TransportMismatchCurvature.lean`):
$$\tau^{\eta K(s+t)} = \exp\bigl(\eta K(s+t)\log\tau\bigr).$$
Its first and second $\eta$-derivatives at $\eta = 0$ are:
$$\left.\partial_\eta \tau^{\eta K(s+t)}\right|_{\eta=0} = K\log\tau\,(s+t), \qquad \left.\partial_\eta^2 \tau^{\eta K(s+t)}\right|_{\eta=0} = K^2(\log\tau)^2(s+t)^2.$$

---

### H. Centering and pairing audit

Let $\rho = \tfrac{1}{2} + \delta_\rho + i\gamma_\rho$ denote a nontrivial zero with radial displacement $\delta_\rho = \operatorname{Re}(\rho) - \tfrac{1}{2}$ and ordinate $\gamma_\rho = \operatorname{Im}(\rho)$. Under the half-density centered convention ($(xy)^{-1/2}$), the centered exponent is $(s - \tfrac{1}{2}) + (t - \tfrac{1}{2}) = s + t - 1$:

| Pairing | Second Variable $t$ | Centered Exponent $(s-\tfrac{1}{2})+(t-\tfrac{1}{2})$ | Even Mismatch Defect $\tau^{\eta K E} + \tau^{-\eta K E} - 2$ | Second Variation at $\eta=0$ | Scope |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Conjugate Pairing** | $t = \bar\rho = \tfrac{1}{2} + \delta_\rho - i\gamma_\rho$ | $2\delta_\rho$ (real radial) | $2\bigl(\cosh(2\eta K\delta_\rho\log\tau)-1\bigr) \ge 0$ | $+4K^2(\log\tau)^2\delta_\rho^2 \ge 0$ | `DIAGONAL_CONJUGATE_BLOCK_ONLY` |
| **FE Reflection Pairing** | $t = 1 - \bar\rho = \tfrac{1}{2} - \delta_\rho + i\gamma_\rho$ | $2i\gamma_\rho$ (purely imaginary ordinate) | $2\bigl(\cos(2\eta K\gamma_\rho\log\tau)-1\bigr) \le 0$ | $-4K^2(\log\tau)^2\gamma_\rho^2 \le 0$ | Off-critical ordinate/phase |
| **General Zero-Zero Pairing** | $t = \sigma = \tfrac{1}{2} + \delta_\sigma + i\gamma_\sigma$ | $(\delta_\rho + \delta_\sigma) + i(\gamma_\rho + \gamma_\sigma)$ | Complex oscillatory cross-term | $K^2(\log\tau)^2\bigl((\delta_\rho+\delta_\sigma)+i(\gamma_\rho+\gamma_\sigma)\bigr)^2$ | Unrestricted double sum |

Because $\widehat{\mathcal M}_K(\eta) = \langle \mu_K \otimes \mu_K, F_{K,\eta}\rangle$ is a bilinear pairing of two prime-power sums, the explicit formula naturally induces the **unrestricted general zero-zero double sum** over all pairs $(\rho,\sigma)$ plus pole, trivial-zero, and Archimedean background terms (`UNRESTRICTED_DOUBLE_ZERO_SUM_WITH_BACKGROUND`).

---

### I. Homogeneous-kernel candidate

If a kernel $F_0$ satisfies the Euler homogeneity equation $\mathcal E F_0 = d F_0$ for a constant $d \in \mathbb{R}$, then $\mathcal E^2 F_0 = d^2 F_0$, so $A_1(F_0) = d A_0(F_0)$ and $A_2(F_0) = d^2 A_0(F_0)$, and therefore (`homogeneous_arithmetic_curvature_zero` in `TransportMismatchCurvature.lean`):
$$\mathfrak C_{\mathrm{arith}}(F_0) = A_0(d^2 A_0) - (d A_0)^2 = 0.$$
*(Note: Lean formalizes the algebraic moment identity $A_0(d^2 A_0) - (d A_0)^2 = 0$; on noncompact homogeneous functions $x^\alpha y^\beta$, any numerical evaluation up to $n_{\max}$ is strictly a `FINITE_TRUNCATION_DIAGNOSTIC`.)*

---

### J. Compact-support homogeneity obstruction (`PROVED_PAPER_DERIVATION`)

**Theorem (`NONZERO_COMPACT_SUPPORT_HOMOGENEOUS_KERNEL_IMPOSSIBLE` / `COMPACT_SUPPORT_HOMOGENEITY_NO_GO_PAPER_PROVED`):**
$$\left(F_0 \in C_c^\infty((0,\infty)^2) \;\wedge\; \mathcal E F_0 = d F_0\right) \Longrightarrow F_0 \equiv 0.$$

**Evidence Status:** `PROVED_PAPER_DERIVATION` (not formalized in Lean).

**Proof:**
1. Fix any $(x_0, y_0) \in (0,\infty)^2$.
2. Define $g(r) = F_0(rx_0, ry_0)$ for $r > 0$.
3. By the chain rule, Euler homogeneity $\mathcal E F_0 = d F_0$ gives $r g'(r) = d\,g(r)$.
4. Integrating on $(0,\infty)$ yields $g(r) = r^d g(1)$.
5. If $g(1) \neq 0$, then $g(r) \neq 0$ for every $r > 0$.
6. The support $\operatorname{supp}(F_0)$ therefore contains the entire unbounded positive ray $\{(rx_0, ry_0) : r > 0\}$, contradicting compact support in $(0,\infty)^2$.
7. Thus $F_0(x_0, y_0) = g(1) = 0$ for every $(x_0, y_0) \in (0,\infty)^2$. $\square$

---

### K. Complete spectral curvature

On the spectral side, the second $\eta$-derivative at $\eta = 0$ of the normalized explicit-formula expansion of $\widehat{\mathcal M}_K(\eta)$ has the form:
$$\widehat{\mathcal M}_K''(0) = K^2(\log\tau)^2 \left[ \sum_{\rho,\sigma} H_0(\rho,\sigma)(\rho+\sigma)^2 + \mathcal B_{\mathrm{pole}}'' + \mathcal B_{\mathrm{triv}}'' + \mathcal B_{\mathrm{arch}}'' \right].$$
The complete spectral curvature is classified as **`SPECTRAL_CURVATURE_IS_SIGNED_OR_DOUBLE_SUM`** (Outcome D).

---

### L. Off-diagonal and background terms

All mandatory firewalls are enforced:
1. **Zero-zero cross terms:** Present for all pairs $(\rho,\sigma)$ with $\sigma \neq \bar\rho$.
2. **Pole, trivial-zero, and Archimedean terms:** Present in the complete expansion.
3. **No diagonal projection or remainder subordination:** Projecting onto the conjugate diagonal $t = \bar\rho$ without an arithmetic mechanism is classified as `SELECTED_CURVATURE_BLOCK_ONLY` (`DIAGONAL_CONJUGATE_BLOCK_ONLY`). Treating off-diagonal and background terms as a subordinate remainder is closed by `TASK-TC-032R` (`EXACT_CANCELLATION_BLOCKS_STRICT_SUBORDINATION_ROUTE`).

---

### M. Existing Curvature Transport reconciliation

On the centered conjugate block $t = \bar\rho$, we have the exact identity:
$$\tau^{2\eta K\delta_\rho} + \tau^{-2\eta K\delta_\rho} - 2 = 2\bigl(\cosh(2\eta K\delta_\rho\log\tau) - 1\bigr) = B_\rho(2\eta K).$$
Explicit scope boundaries (`TASK-TC-034R` Section 12):
- This equality is exact on the centered conjugate block;
- It reproduces the existing spectral detector $B_\rho(2\eta K)$ from `CURVATURE_TRANSPORT.md`;
- The complete arithmetic functional induces an unrestricted double zero sum plus pole/trivial-zero/Archimedean background;
- No positive diagonal projection has been derived;
- No new arithmetic descent has been constructed.

Classification:
$$\boxed{\texttt{MISMATCH\_CURVATURE\_REDUCES\_TO\_EXISTING\_OBL\_CT\_001A}.}$$

---

### N. Conditional Theta–Mellin audit (`TASK-TC-034R` Section 11)

The candidate bilinear scale-mismatched theta–Mellin functional
$$\mathcal Q_\Theta(\eta; \Phi_0) = \iint_{(0,\infty)^2} \Theta_1^+(t_1)\Theta_1^+(t_2)\,\Phi_0\!\left(\tau^{-\eta K}t_1, \tau^{-\eta K}t_2\right)\frac{dt_1}{t_1}\frac{dt_2}{t_2}, \qquad \Theta_1^+(t) = \sum_{n=1}^\infty e^{-\pi n^2 t},$$
is audited using explicit evidence statuses rather than unconditional Booleans:

| Property | Repaired Evidence Status |
| :--- | :--- |
| Purely theta/arithmetic defined | `PROVED_BY_DEFINITION` |
| Zero-independent definition | `PROVED_BY_DEFINITION` |
| Exact scale-flatness law | `FALSE` ($\Theta_1^+$ is multi-exponential and no nonzero convergent $\Phi_0$ on $(0,\infty)^2$ is Euler-homogeneous) |
| Convergence on regularized space | `CONDITIONAL_ON_REGULARIZATION` |
| Second mismatch variation | `FORMAL_CANDIDATE_NOT_DERIVED` |
| $\delta^2$ detection | `DIAGONAL_CONJUGATE_BLOCK_ONLY` |
| Complete zero/pole/Archimedean expansion | `COMPLETE_EXPANSION_NOT_DERIVED` |
| Positive complete spectral curvature | `RH_EQUIVALENT_IF_POSITIVE` |
| Closes `OBL-CT-001A` | `FALSE` |
| Overall classification | `CANDIDATE_THETA_MELLIN_AUDIT` (`THETA_MELLIN_AUDIT_CONDITIONAL`) |

---

### O. Tau-specificity

Repeating the Euler-generator and mismatch-curvature derivation for an arbitrary scale base $q > 1$ (`generic_base_mismatch_curvature_scaling` in `TransportMismatchCurvature.lean` and `evaluate_generic_base_mismatch_control` on the compactly supported witness $\widetilde G_-$ in `tc/transport_mismatch_curvature.py`):
$$\widehat{\mathcal M}_K^{(j)}(0; q) = (-K\log q)^j A_j(F_0), \qquad \frac{\widehat{\mathcal M}_K(0;q)\widehat{\mathcal M}_K''(0;q) - \bigl(\widehat{\mathcal M}_K'(0;q)\bigr)^2}{K^2(\log q)^2} = A_0(F_0)A_2(F_0) - A_1(F_0)^2.$$
Because no step in the Euler mismatch-curvature algebra uses a $\tau$-specific theorem, this step is classified as **`GENERIC_SCALE_CURVATURE`**.

---

### P. Weil-equivalence audit

Asserting global positivity of a reflected Hermitian spectral curvature form across all admissible test functions is equivalent to the Weil positivity criterion and is therefore classified as:
$$\boxed{\texttt{CURVATURE\_POSITIVITY\_IS\_RH\_EQUIVALENT}.}$$

---

### Q. Exact Lean 4 Theorem Map (`formal/RiemannScope/TransportMismatchCurvature.lean`)

`formal/RiemannScope/TransportMismatchCurvature.lean` contains **18 declarations** (`1 def` + `17 theorem` declarations; 0 `sorry`, 0 `admit`, no nonstandard project axioms introduced), bringing the repository's compiled `theorem` count in `formal/build_report.json` to **565**:

| # | Identifier | Kind | Exact Statement Scope | Algebraic Only | Paper Step Supported | External Dependency |
|---|---|---|---|---|---|---|
| 1 | `curvatureDet` | `def` | `A0 * A2 - A1 ^ 2` | Yes | Section 6 curvature determinant | None |
| 2 | `single_exponential_log_curvature_zero` | `theorem` | `curvatureDet w (w * x) (w * x ^ 2) = 0` | Yes | Section 7 single-exponential baseline | None |
| 3 | `two_exponential_curvature_identity` | `theorem` | `curvatureDet (w1+w2) (w1*x1+w2*x2) (w1*x1^2+w2*x2^2) = w1*w2*(x1-x2)^2` | Yes | Section 7 two-point Lagrange identity | None |
| 4 | `two_exponential_positive_log_curvature` | `theorem` | `0 < w1, 0 < w2, x1 != x2 ==> 0 < curvatureDet ...` | Yes | Section 7 two-point strict positivity | None |
| 5 | `positive_finite_exponential_curvature_nonneg` | `theorem` | `0 <= w1, 0 <= w2 ==> 0 <= curvatureDet ...` | Yes | Section 7 two-point nonnegativity | None |
| 6 | `three_exponential_curvature_identity` | `theorem` | `curvatureDet (w1+w2+w3) ... = sum_{i<j} w_i w_j (x_i-x_j)^2` | Yes | Section 7 three-point Lagrange identity | None |
| 7 | `three_exponential_curvature_nonneg` | `theorem` | `0 <= w1, w2, w3 ==> 0 <= curvatureDet ...` | Yes | Section 7 three-point nonnegativity | None |
| 8 | `reciprocal_pair_curvature_strict_pos` | `theorem` | `0 < w1, 0 < w2, x != 0 ==> 0 < curvatureDet (w1+w2) (w1*x+w2*(-x)) ...` | Yes | Section 7/9 opposite-exponent pair positivity | None |
| 9 | `homogeneous_arithmetic_curvature_zero` | `theorem` | `curvatureDet A0 (d * A0) (d ^ 2 * A0) = 0` | Yes | Section 11 algebraic moment consequence of homogeneity | None |
| 10 | `arithmetic_zero_curvature_and_spectral_positive_contradiction` | `theorem` | `C = 0 -> 0 < C -> False` | Yes | Conditional zero-vs-positive incompatibility | None |
| 11 | `euler_generator_scaling_algebra` | `theorem` | `curvatureDet A0 (-K*log_tau*A1) (K^2*log_tau^2*A2) = K^2*log_tau^2*curvatureDet A0 A1 A2` | Yes | Section 5/6 Euler scaling factorization | None |
| 12 | `mismatch_curvature_k_independent` | `theorem` | `K != 0, log_tau != 0 ==> curvatureDet ... / (K^2*log_tau^2) = curvatureDet A0 A1 A2` | Yes | Section 6 $K$-independence after normalization | None |
| 13 | `even_second_difference_quadratic_ident` | `theorem` | `(M0 + eta*M1 + 1/2*eta^2*M2) + (M0 - eta*M1 + 1/2*(-eta)^2*M2) - 2*M0 = eta^2*M2` | Yes | Section 10 symmetric second difference | None |
| 14 | `centered_conjugate_pairing_radial` | `theorem` | `(1/2 + delta - 1/2) + (1/2 + delta - 1/2) = 2 * delta` | Yes | Section 9 centered conjugate radial exponent | None |
| 15 | `centered_reflection_pairing_real_zero` | `theorem` | `(1/2 + delta - 1/2) + (1 - (1/2 + delta) - 1/2) = 0` | Yes | Section 9 centered reflection real-part cancellation | None |
| 16 | `mellin_mismatch_net_exponent` | `theorem` | `(K*(a + (1+eta)*(s+t)) - K*(s+t)) - a*K = eta*K*(s+t)` | Yes | Section 8 Mellin mismatch net exponent | None |
| 17 | `signed_weight_curvature_negative` | `theorem` | `w1=1, w2=-2, x1=0, x2=1 ==> curvatureDet ... < 0` | Yes | Section 14/16 signed-weight countermodel | None |
| 18 | `generic_base_mismatch_curvature_scaling` | `theorem` | `K != 0, log_q != 0 ==> curvatureDet ... / (K^2*log_q^2) = curvatureDet A0 A1 A2` | Yes | Section 19 generic-base scale covariance control | None |

**Explicitly NOT formalized in Lean:**
- the compact-support Euler-PDE no-go (`PROVED_PAPER_DERIVATION`);
- the full two-variable explicit formula;
- the theta–Mellin regularized descent;
- positivity of the complete spectral curvature;
- `OBL-CT-001A`.

---

### R. Principal classification, cutoff implementation note, & Canonical Non-Scalar Selector Problem (`OBL-CT-001A`)

- **Task Completion Status:** `TASK_TC_034R_TRANSPORT_CURVATURE_REPAIR_COMPLETE`
- **Principal Classification:** `MISMATCH_CURVATURE_REDUCES_TO_OBL_CT_001A`
- **`OBL-CT-001A` Status:** `OPEN` (`OBL_CT_001A_OPEN`)
- **Mathematical $C^\infty$ Cutoff vs. Floating-Point Transition Evaluator:** The mathematical plateau cutoff uses the exact $C^\infty$ function $h(t) = e^{-1/t}$ ($t > 0$), $0$ ($t \le 0$). The IEEE-754 binary64 callable `flat_transition_h_jet(t)` used away from active stations includes an underflow shortcut (`inv_t > 700.0`) where $e^{-1/t} < e^{-700} \approx 9.86 \times 10^{-305}$, whereas `flat_transition_h_jet_arb(t, prec_bits)` evaluates the mathematical $C^\infty$ jet in outward Arb ball arithmetic without any threshold shortcut. Neither transition evaluator affects the certified arithmetic curvature sums at integer stations, because all contributing stations $2 \le n \le 15$ lie strictly inside the plateau $[1.75, 15.25]^2$ where the cutoff is returned identically as $(1,0,0)$, and all excluded integers $n \le 1$ or $n \ge 16$ lie strictly outside $(1.5, 15.5)^2$ where it is $(0,0,0)$.

> **Remaining Theorem & Canonical Non-Scalar Selector Problem (`OBL-CT-001A`):** Arithmetic label compatibility ($b = 1$) makes mismatch curvature $\mathfrak C_{\mathrm{arith}}(F) = A_0 A_2 - A_1^2$ grade-invariant, but does not make it zero, positive, or sign-definite (`COMPACT_SUPPORT_ARITHMETIC_CURVATURE_SIGN_INDEFINITE`). The next substantive problem under `OBL-CT-001A` is the **Selector Problem**: *What $\zeta$-specific principle selects one canonical non-scalar arithmetic functional whose law is stronger than generic grade invariance, while its complete spectral expansion isolates a positive radial moment in $\delta_\rho^2$ without assuming Weil positivity?*

