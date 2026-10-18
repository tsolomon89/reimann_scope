# TASK-TC-039R — Newton/Padé/Hankel Asymptotic Repair, Gate-Z5 Lower-Envelope Audit, and \(\pi\leftrightarrow\tau\) Arithmetic-Normalization Analysis

**Task ID:** `TASK-TC-039R`  
**Starting Commit (`HEAD` / `origin/main`):** `e0545d3a01d09da394bf1b74bc7153b14cc365ea`  
**Substantive `TASK-TC-039` Commit:** `f55571b96eb9b4f51a29946ee6b095c840a423e7`  
**Machine Artifact:** [`data/tc_fauzan_zero_argument_asymptotic_repair.json`](file:///C:/Development/Projects/reimann_scope/data/tc_fauzan_zero_argument_asymptotic_repair.json)  
**Implementation Module:** [`tc/fauzan_zero_argument_asymptotic_repair.py`](file:///C:/Development/Projects/reimann_scope/tc/fauzan_zero_argument_asymptotic_repair.py)  
**Formal Lean 4 Module:** [`formal/RiemannScope/FauzanZeroArgumentTransfer.lean`](file:///C:/Development/Projects/reimann_scope/formal/RiemannScope/FauzanZeroArgumentTransfer.lean) (`17` `theorem` declarations, `0` `sorry`, `0` `admit`)  
**Principal Classification:**  
`PROVED_PAPER_DERIVATION_PENDING_ASYMPTOTIC_RIGOR_AUDIT_AND_FIXED_RATIONAL_NORMALIZATION_GAUGES_EQUIVALENT_AT_LEADING_DIOPHANTINE_ORDER`

---

### A. Why TASK-TC-039 required evidence repair

In `TASK-TC-039`, the rationalized-\(\xi\) entire function \(\mathcal{R}_\pi(z) = (2z - 1)\pi^{-2z}\zeta(2z)\) established a valid zero-carrying rational-sampling bridge (\(\mathcal{R}_\pi(\rho/2) = 0\), \(\mathcal{R}_\pi(m) \in \mathbb{Q}_{>0}\)), and constructed zero-independent Newton and multipoint Padé argument polynomials. However, post-sprint audit identified seven technical and structural points requiring rigorous repair:

1. **Upper bound vs. lower envelope at Gate Z5:** An upper bound \(|N_n(\alpha_1)| \le \exp(-(3/2)n^{1/3} + o(n^{1/3}))\) does not by itself rule out anomalous subsequences on which the oscillatory factor \(\cos(\omega n^{1/3} + \phi)\) is superlinearly close to zero. Closing Gate Z5 for the Newton route requires a **two-sided lower envelope** on the structurally positive two-approximant sum \(E_n^{(c)} = |N_n^{(c)}(\alpha_1)|^2 + |N_{n+1}^{(c)}(\alpha_1)|^2\).
2. **Spurious \(\pi^{2/3}\) saddle factor in prose:** One prose equation in `TC_FAUZAN_ZERO_ARGUMENT_TRANSFER.md` wrote \(\exp(-(3/2)\pi^{2/3}n^{1/3})\) alongside the correct \(\exp(-(3/2)n^{1/3})\). Because \(a_m^{(\pi)}\) already divides out \(\pi^{2m}\), the OGF \(A_\pi(t) = \frac{t}{2\sin^2\sqrt{t}}\) is dimensionless in \(t\) and has no \(\pi^{2/3}\) factor in its saddle exponent.
3. **Direct Newton-series equality without Carlson's shortcut:** Claiming \(\sum_{n\ge 0} \Delta^n a_0 \binom{z}{n} = \mathcal{R}(z)\) from agreement at \(z \in \mathbb{Z}_{\ge 0}\) requires either verifying exponential-type hypotheses of Carlson's theorem or giving a direct double-series Fubini proof plus analytic continuation.
4. **Newton denominator upper bound vs. equality:** Divisibility \(L_n \mid n!(2n)!\prod_{(p-1)\mid 2m} p\) immediately gives \(\log L_n \le 3n\log n + O(n)\), whereas a lower bound requires explicit \(p\)-adic valuation analysis (via von Staudt–Clausen and Kummer congruences).
5. **Hankel S-fraction product & subleading coefficient:** The compact S-fraction product formula in prose had a malformed odd-product transcription and undercounted \(4^4 = 256\) as \(4^2 = 16\), reporting \((2\log 2 - 3)n^2\) instead of the true \((4\log 2 - 3)n^2\), and one prose line wrote \(b_0 = -1/2\) instead of \(b_0^{(\pi)} = 1/6 = D_1^{(\pi)}\).
6. **C1 universal denominator degree in prose:** Prose Section O wrote \(\deg_X U_n = 2n - 1\), whereas the code and artifact correctly computed the anti-diagonal multiplicity sum \(\sum_{m=1}^{2n-1} \min(m, 2n-m) = n^2\).
7. **Padé finite evidence vs. all-\(n\) theorem:** Finite certified evaluations on \(1 \le n \le 25\) must be distinguished (`MULTIPOINT_PADE_GATE_Z5_NEGATIVE_NUMERICAL_EVIDENCE`) from an all-\(n\) asymptotic theorem.

Simultaneously, `TASK-TC-039R` re-derives the entire bridge in both \(\pi\) and \(\tau = 2\pi\) normalizations (and the general rational gauge family \(\mathcal{R}_c(z) = c^z \mathcal{R}_\tau(z)\)) to isolate which arithmetic features are intrinsic and which come from choosing \(\pi = \tau/2\).

---

### B. \(\pi\) versus \(\tau\) normalization

Throughout this sprint, every load-bearing identity is expressed in both \(\pi\)-form and \(\tau\)-form with
\[
\boxed{\tau = 2\pi, \qquad \pi = \frac{\tau}{2}.}
\]

| Object | \(\pi\)-normalization (\(c = 4\)) | \(\tau\)-normalization (\(c = 1\)) | Exact scaling / relation |
|---|---|---|---|
| Even-zeta rational core | \(\pi^{-2m}\zeta(2m) = (-1)^{m+1}\frac{2^{2m-1}B_{2m}}{(2m)!}\) | \(\tau^{-2m}\zeta(2m) = (-1)^{m+1}\frac{B_{2m}}{2(2m)!}\) | \(\pi^{-2m}\zeta(2m) = 4^m \tau^{-2m}\zeta(2m)\) |
| Zero-carrying function \(\mathcal{R}(z)\) | \(\mathcal{R}_\pi(z) = (2z-1)\pi^{-2z}\zeta(2z) = \pi^{-z}\frac{\xi(2z)}{\Gamma(z+1)}\) | \(\mathcal{R}_\tau(z) = (2z-1)\tau^{-2z}\zeta(2z) = (2\tau)^{-z}\frac{\xi(2z)}{\Gamma(z+1)}\) | \(\mathcal{R}_\pi(z) = 4^z \mathcal{R}_\tau(z)\) |
| Integer sample \(a_m = \mathcal{R}(m)\) | \(a_m^{(\pi)} = (-1)^{m+1}\frac{(2m-1)2^{2m-1}B_{2m}}{(2m)!}\) | \(a_m^{(\tau)} = (-1)^{m+1}\frac{(2m-1)B_{2m}}{2(2m)!}\) | \(a_m^{(\pi)} = 4^m a_m^{(\tau)}\) |
| Positive moment \(b_m\) | \(b_m^{(\pi)} = \pi^{-2m-2}\zeta(2m+2) = (-1)^m\frac{2^{2m+1}B_{2m+2}}{(2m+2)!}\) | \(b_m^{(\tau)} = \tau^{-2m-2}\zeta(2m+2) = (-1)^m\frac{B_{2m+2}}{2(2m+2)!}\) | \(b_m^{(\pi)} = 4^{m+1} b_m^{(\tau)}\) |
| Moment support atoms | \(q_{\pi,k} = (\pi k)^{-2}\) | \(q_{\tau,k} = (\tau k)^{-2}\) | \(q_{\pi,k} = 4 q_{\tau,k}\) |
| Newton coefficient \(\Delta^n a_0\) | \(\Delta^n a_0^{(\pi)}\), \(\kappa(4) = \frac{3}{2}\) | \(\Delta^n a_0^{(\tau)}\), \(\kappa(1) = \frac{3}{2^{5/3}}\) | \(\kappa(c) = \frac{3}{2^{5/3}}c^{1/3}\) |
| Hankel determinant \(D_n\) | \(D_n^{(\pi)} = \det(b_{i+j}^{(\pi)})_{0\le i,j<n}\) | \(D_n^{(\tau)} = \det(b_{i+j}^{(\tau)})_{0\le i,j<n}\) | \(D_n^{(\pi)} = 4^{n^2} D_n^{(\tau)}\) |
| Sample OGF \(A(t)\) | \(A_\pi(t) = \frac{t}{2\sin^2\sqrt{t}}\), \(R_\pi = \pi^2\) | \(A_\tau(t) = \frac{t}{8\sin^2(\sqrt{t}/2)}\), \(R_\tau = \tau^2\) | \(A_\pi(t) = A_\tau(4t)\) |
| Euler-transformed OGF \(C(w)\) | \(C_\pi(w) = \frac{w}{2(1+w)^2\sin^2\sqrt{\frac{w}{1+w}}}\) | \(C_\tau(w) = \frac{w}{8(1+w)^2\sin^2\left(\frac{1}{2}\sqrt{\frac{w}{1+w}}\right)}\) | \(C_c(w) = \frac{1}{1+w}A_\tau\!\left(\frac{cw}{1+w}\right)\) |

---

### C. Tau-first even-zeta rationalization

Euler's even-zeta theorem is naturally a \(\tau = 2\pi\) identity because the Fourier series of the 1-periodic Bernoulli polynomials \(B_{2m}(\{x\})\) expands in powers of \(e^{2\pi i k x} = e^{i\tau k x}\):

- **\(\pi\)-form:**
  \[
  \zeta(2m) = (-1)^{m+1}\frac{B_{2m}(2\pi)^{2m}}{2(2m)!} \implies \pi^{-2m}\zeta(2m) = (-1)^{m+1}\frac{2^{2m-1}B_{2m}}{(2m)!}.
  \]
- **\(\tau\)-form (primitive arithmetic form):**
  \[
  \boxed{\zeta(2m) = (-1)^{m+1}\frac{B_{2m}\tau^{2m}}{2(2m)!} \implies \tau^{-2m}\zeta(2m) = (-1)^{m+1}\frac{B_{2m}}{2(2m)!} \in \mathbb{Q}_{>0} \quad (m \ge 1).}
  \]

The dyadic numerator factor \(2^{2m} = 4^m\) in \(\pi^{-2m}\zeta(2m)\) is not intrinsic to \(\zeta(2m)\)—it is an artifact of dividing \((2\pi)^{2m} = \tau^{2m}\) by \(\pi^{2m} = (\tau/2)^{2m}\) (`TAU_NORMALIZATION_EXPOSES_EVEN_ZETA_RATIONAL_CORE`, formalized in Lean 4 as `tau_even_zeta_rational_core_identity`).

---

### D. Zero-divisor equivalence

Define the two zero-carrying entire functions:
\[
\boxed{
\mathcal{R}_\pi(z) := (2z-1)\pi^{-2z}\zeta(2z) = \pi^{-z}\frac{\xi(2z)}{\Gamma(z+1)},
\qquad
\mathcal{R}_\tau(z) := (2z-1)\tau^{-2z}\zeta(2z) = (2\tau)^{-z}\frac{\xi(2z)}{\Gamma(z+1)}.
}
\]
Because \(\pi^{-2z} = (\tau/2)^{-2z} = 4^z \tau^{-2z}\) and \(\pi^{-z} = (2\tau/4)^{-z} = 4^z (2\tau)^{-z}\), we have the exact identity
\[
\boxed{\mathcal{R}_\pi(z) = 4^z \mathcal{R}_\tau(z), \qquad 4^z = e^{z\log 4} \ne 0 \quad (\forall z \in \mathbb{C}).}
\]
Consequently, \(\mathcal{R}_\pi\) and \(\mathcal{R}_\tau\) have the **exact same zero divisor** (`PI_TAU_NORMALIZATIONS_HAVE_IDENTICAL_ZERO_DIVISOR`, formalized in Lean 4 as `pi_tau_zero_function_scaling` and `rational_gauge_zero_divisor_invariant`):
\[
\mathcal{R}_\pi(z) = 0 \iff \mathcal{R}_\tau(z) = 0, \qquad \mathcal{R}_\pi(\rho/2) = \mathcal{R}_\tau(\rho/2) = 0
\]
for every nontrivial zero \(\rho\) of \(\zeta(s)\), including \(\alpha_1 = \rho_1/2 = \frac{1}{4} + i\frac{\gamma_1}{2}\).

---

### E. Rational normalization gauge \(c\)

The \(\pi\) and \(\tau\) normalizations are the \(c = 4\) and \(c = 1\) specializations of the one-parameter rational zero-preserving gauge family (`RATIONAL_ZERO_PRESERVING_NORMALIZATION_GAUGE_FAMILY_PROVED`):
\[
\boxed{
\mathcal{R}_c(z) := c^z \mathcal{R}_\tau(z) = (2z-1)c^z\tau^{-2z}\zeta(2z) = \left(\frac{2\tau}{c}\right)^{-z}\frac{\xi(2z)}{\Gamma(z+1)}, \qquad c \in \mathbb{Q}_{>0}.
}
\]
- **Analytic zero structure (invariant under \(c\)):** Because \(c^z = e^{z\log c}\) is entire and nowhere vanishing on \(\mathbb{C}\), every \(\mathcal{R}_c(z)\) has the identical zero divisor \(\{\rho/2 : \xi(\rho) = 0\} \cup \{-1, -2, -3, \dots\}\).
- **Arithmetic interpolation structure (dependent on \(c\)):** Restricting \(\mathcal{R}_c(z)\) to \(m \in \mathbb{Z}_{\ge 0}\) rescales the rational sample sequence by geometric powers \(c^m\):
  \[
  \boxed{a_m^{(c)} := \mathcal{R}_c(m) = c^m a_m^{(\tau)} \in \mathbb{Q}_{>0} \qquad (m \in \mathbb{Z}_{\ge 0}).}
  \]

---

### F. Integer sample sequences

For \(m \in \mathbb{Z}_{\ge 0}\), the integer samples in \(\tau\)-, \(\pi\)-, and general \(c\)-normalization are:
\[
\boxed{
a_m^{(\tau)} = (-1)^{m+1}\frac{(2m-1)B_{2m}}{2(2m)!}, \qquad
a_m^{(\pi)} = 4^m a_m^{(\tau)} = (-1)^{m+1}\frac{(2m-1)2^{2m-1}B_{2m}}{(2m)!}, \qquad
a_m^{(c)} = c^m a_m^{(\tau)}.
}
\]
At \(m = 0\), \(B_0 = 1\) and \(\zeta(0) = -1/2\) give \(a_0^{(\tau)} = a_0^{(\pi)} = a_0^{(c)} = \frac{1}{2}\). The first values are:

| \(m\) | \(a_m^{(\tau)} = \mathcal{R}_\tau(m)\) | \(a_m^{(\pi)} = \mathcal{R}_\pi(m)\) | Exact ratio \(a_m^{(\pi)} / a_m^{(\tau)} = 4^m\) |
|---:|---:|---:|---:|
| \(0\) | \(1/2\) | \(1/2\) | \(1\) |
| \(1\) | \(1/24\) | \(1/6\) | \(4\) |
| \(2\) | \(1/480\) | \(1/30\) | \(16\) |
| \(3\) | \(1/12096\) | \(1/189\) | \(64\) |
| \(4\) | \(1/345600\) | \(1/1350\) | \(256\) |
| \(5\) | \(1/10644480\) | \(1/10395\) | \(1024\) |
| \(6\) | \(691/237758976000\) | \(691/58046625\) | \(4096\) |

This scaling is verified exactly in Python (`compute_gauge_integer_samples`) for \(0 \le m \le 200\) and formalized in Lean 4 as `pi_tau_integer_sample_scaling`.

---

### G. Generating functions \(A_\pi,A_\tau,A_c\)

Applying the differential operator \(1 - 2t\frac{d}{dt}\) to the cotangent generating function \(\frac{1}{4}\sqrt{c t}\cot(\sqrt{c t}/2) = \frac{1}{2} - \sum_{m=1}^\infty c^m \tau^{-2m}\zeta(2m) t^m\) yields the closed-form ordinary generating functions:
\[
\boxed{
A_\tau(t) := \sum_{m=0}^\infty a_m^{(\tau)} t^m = \frac{t}{8\sin^2(\sqrt{t}/2)} \quad (|t| < R_\tau = \tau^2),
}
\]
\[
\boxed{
A_\pi(t) := \sum_{m=0}^\infty a_m^{(\pi)} t^m = A_\tau(4t) = \frac{t}{2\sin^2\sqrt{t}} \quad (|t| < R_\pi = \pi^2 = \tau^2/4),
}
\]
\[
\boxed{
A_c(t) := \sum_{m=0}^\infty a_m^{(c)} t^m = A_\tau(ct) = \frac{ct}{8\sin^2(\sqrt{ct}/2)} \quad \left(|t| < R_c = \frac{\tau^2}{c} = \frac{4\pi^2}{c}\right).
}
\]

---

### H. Positive moment sequences

Removing the linear prefactor \(2m + 1\) from \(a_{m+1}^{(c)}\) defines the strictly positive Hausdorff/Stieltjes moment sequence (`moment_pi_tau_scaling` in Lean 4):
\[
\boxed{
b_m^{(\tau)} := \tau^{-2m-2}\zeta(2m+2) = \frac{a_{m+1}^{(\tau)}}{2m+1} = (-1)^m\frac{B_{2m+2}}{2(2m+2)!} = \sum_{k=1}^\infty q_{\tau,k}^{m+1} \in \mathbb{Q}_{>0}, \qquad q_{\tau,k} = \frac{1}{\tau^2 k^2},
}
\]
\[
\boxed{
b_m^{(\pi)} := \pi^{-2m-2}\zeta(2m+2) = 4^{m+1} b_m^{(\tau)} = \sum_{k=1}^\infty q_{\pi,k}^{m+1}, \qquad q_{\pi,k} = \frac{1}{\pi^2 k^2} = 4 q_{\tau,k},
}
\]
\[
\boxed{
b_m^{(c)} := c^{m+1} b_m^{(\tau)} = \int_0^1 x^m \, d\nu_c(x), \qquad \nu_c = \sum_{k=1}^\infty q_{c,k}\,\delta_{q_{c,k}}, \quad q_{c,k} = c\,q_{\tau,k} = \frac{c}{\tau^2 k^2}.
}
\]
In particular, the zeroth moments (total masses) are
\[
\boxed{b_0^{(\tau)} = \frac{1}{24}, \qquad b_0^{(\pi)} = 4\,b_0^{(\tau)} = \frac{1}{6}}
\]
(repairing the stale value \(-1/2 = \zeta(0)\) that appeared in one prose line of `TC_FAUZAN_ZERO_ARGUMENT_TRANSFER.md`).

---

### I. \(\pi/\tau\) Hankel scaling

Let \(D_n^{(c)} := \det\bigl(b_{i+j}^{(c)}\bigr)_{0\le i,j<n}\) be the \(n \times n\) Hankel determinant of the positive moment sequence \(b_m^{(c)} = c^{m+1}b_m^{(\tau)}\). Since entry \((i, j)\) is \(b_{i+j}^{(c)} = c^{i+j+1}b_{i+j}^{(\tau)} = c^i \cdot c^{j+1} b_{i+j}^{(\tau)}\), multilinearity of the determinant factors \(c^i\) from row \(i\) (\(0 \le i < n\)) and \(c^{j+1}\) from column \(j\) (\(0 \le j < n\)). Because
\[
\sum_{i=0}^{n-1} i + \sum_{j=0}^{n-1} (j+1) = \frac{n(n-1)}{2} + \frac{n(n+1)}{2} = n^2
\]
(formalized in Lean 4 as `hankel_gauge_scaling_exponent`), we obtain the exact Hankel gauge-scaling law (`HANKEL_DETERMINANT_RATIONAL_GAUGE_SCALING_PROVED`):
\[
\boxed{
D_n^{(c)} = c^{n^2} D_n^{(\tau)}, \qquad D_n^{(\pi)} = 4^{n^2} D_n^{(\tau)} = 2^{2n^2} D_n^{(\tau)}.
}
\]
For \(n = 1, 2\):
\[
\boxed{
D_1^{(\tau)} = \frac{1}{24}, \quad D_1^{(\pi)} = 4^1 D_1^{(\tau)} = \frac{1}{6}; \qquad
D_2^{(\tau)} = \frac{1}{4838400}, \quad D_2^{(\pi)} = 4^4 D_2^{(\tau)} = \frac{256}{4838400} = \frac{1}{18900}.
}
\]

---

### J. Correct Lambert–Stieltjes determinant formula

By Lambert's continued fraction for \(\tan\sqrt{t}/\sqrt{t}\), the moment generating function \(B_\pi(t) = \sum_{m=0}^\infty b_m^{(\pi)} t^m = \frac{1 - \sqrt{t}\cot\sqrt{t}}{2t}\) has the exact Stieltjes S-fraction expansion with positive coefficients
\[
c_0 = \frac{1}{6}, \qquad c_k = \frac{1}{(2k+1)(2k+3)} \quad (k \ge 1), \qquad c_{2j-1}c_{2j} = \frac{1}{(4j-1)(4j+1)^2(4j+3)}.
\]
By the Stieltjes–Heilermann Hankel determinant theorem, \(D_r^{(\pi)} / D_{r-1}^{(\pi)} = c_0 \prod_{j=1}^{r-1} (c_{2j-1}c_{2j})\), so taking the product over \(1 \le r \le n\) yields the exact unit-fraction formula:
\[
\boxed{
D_n^{(\pi)} = c_0^n \prod_{j=1}^{n-1} (c_{2j-1}c_{2j})^{n-j} = 6^{-n}\prod_{j=1}^{n-1}\bigl[(4j-1)(4j+1)^2(4j+3)\bigr]^{-(n-j)},
}
\]
and in \(\tau\)-normalization:
\[
\boxed{
D_n^{(\tau)} = 4^{-n^2} D_n^{(\pi)} = 24^{-n}\prod_{j=1}^{n-1}\bigl[16(4j-1)(4j+1)^2(4j+3)\bigr]^{-(n-j)}.
}
\]
Both formulas are verified by exact `fmpq_mat.det()` computation across \(1 \le n \le 15\).

---

### K. Correct Hankel asymptotic

Taking \(-\log D_n^{(\pi)}\) in the exact product formula gives
\[
-\log D_n^{(\pi)} = n\log 6 + \sum_{j=1}^{n-1} (n-j)\log\bigl((4j-1)(4j+1)^2(4j+3)\bigr).
\]
We derive the asymptotic up to \(O(n\log n)\) by two independent methods:

1. **Euler–Maclaurin derivation:** Since \(\log((4j-1)(4j+1)^2(4j+3)) = 4\log(4j) + O(j^{-2}) = 8\log 2 + 4\log j + O(j^{-2})\),
   \[
   \sum_{j=1}^{n-1} (n-j)\cdot 8\log 2 = 8\log 2 \cdot \frac{n(n-1)}{2} = 4\log 2 \cdot n^2 + O(n),
   \]
   and by Euler–Maclaurin summation,
   \[
   4\sum_{j=1}^{n-1} (n-j)\log j = 4\int_1^n (n-x)\log x\,dx + O(n\log n) = 4\left(\frac{1}{2}n^2\log n - \frac{3}{4}n^2\right) + O(n\log n) = 2n^2\log n - 3n^2 + O(n\log n).
   \]
   Adding the two contributions gives
   \[
   \boxed{-\log D_n^{(\pi)} = 2n^2\log n + (4\log 2 - 3)n^2 + O(n\log n).}
   \]
2. **Barnes \(G\)-function cross-check:** Writing \((4j-1)(4j+1)^2(4j+3) = 4^4(j-\frac{1}{4})(j+\frac{1}{4})^2(j+\frac{3}{4})\), the product over \(1 \le j \le r-1\) and \(1 \le r \le n\) expresses \(-\log D_n^{(\pi)}\) as \(4\log 2 \cdot n^2 + \log G(n+\frac{3}{4}) + 2\log G(n+\frac{5}{4}) + \log G(n+\frac{7}{4}) + O(n\log n)\). Applying Barnes' expansion \(\log G(z+1) = \frac{1}{2}z^2\log z - \frac{3}{4}z^2 + O(z\log z)\) four times yields \(4(\frac{1}{2}n^2\log n - \frac{3}{4}n^2) + 4\log 2\cdot n^2 = 2n^2\log n + (4\log 2 - 3)n^2 + O(n\log n)\).

Combining this with \(D_n^{(c)} = c^{n^2} D_n^{(\tau)} = (c/4)^{n^2} D_n^{(\pi)}\) gives for general \(c \in \mathbb{Q}_{>0}\):
\[
\boxed{
-\log D_n^{(c)} = 2n^2\log n + C(c)n^2 + O(n\log n), \qquad C(c) = 6\log 2 - 3 - \log c,
}
\]
with \(C(4) = 4\log 2 - 3 \approx -0.22741127776\) for \(\pi\) and \(C(1) = 6\log 2 - 3 \approx +1.15888308336\) for \(\tau\). Thus \(\pi\)-normalization cancels \(2n^2\) powers of \(2\) from \(\operatorname{den}(D_n^{(\tau)})\), improving only the subleading \(O(n^2)\) term while leaving the leading \(2n^2\log n\) factorial obstruction invariant.

---

### L. Direct Newton-series identity

We prove directly—without invoking Carlson's theorem or integer interpolation uniqueness—that for every fixed gauge \(0 < c < \tau^2 = 4\pi^2\):
\[
\boxed{
\mathcal{R}_c(z) = \sum_{n=0}^\infty \Delta^n a_0^{(c)} \binom{z}{n} \qquad (\forall z \in \mathbb{C})
\qquad (\texttt{NEWTON\_SERIES\_IDENTITY\_FOR\_RATIONALIZED\_XI\_PROVED\_WITHOUT\_CARLSON}).
}
\]

**Proof:**
1. **Mode-by-mode binomial expansion:** For \(0 < c < \tau^2\), every Dirichlet mode \(r_{c,k} := \frac{c}{\tau^2 k^2}\) (\(k \ge 1\)) satisfies \(0 < r_{c,k} \le \frac{c}{\tau^2} < 1\). For each \(k \ge 1\) and all \(z \in \mathbb{C}\), the binomial series for \((1 + (r_{c,k}-1))^z\) and \(z(1 + (r_{c,k}-1))^{z-1}\) converge absolutely:
   \[
   (2z-1)r_{c,k}^z = \sum_{n=0}^\infty \binom{z}{n} d_n(r_{c,k}), \qquad d_n(r) := \sum_{m=0}^n (-1)^{n-m}\binom{n}{m}(2m-1)r^m = (-1)^{n-1}(1-r)^{n-1}\bigl(1 + (2n-1)r\bigr).
   \]
2. **Subtracted difference bound and Fubini interchange on \(\operatorname{Re}(z) > 1/2\):** Subtracting the \(m=0\) term \((-1)^{n-1}\) defines
   \[
   d_n^*(r) := \sum_{m=1}^n (-1)^{n-m}\binom{n}{m}(2m-1)r^m = (-1)^{n-1}\Bigl[(1-r)^{n-1}\bigl(1+(2n-1)r\bigr) - 1\Bigr].
   \]
   For all \(r \in (0, 1)\) and \(n \ge 1\), \((1-r)^{n-1}(1+(2n-1)r) \in (1 - (n-1)r, 1 + 2nr)\) and lies in \((0, 2)\), giving the uniform bound
   \[
   \boxed{|d_n^*(r)| \le \min(1, 2nr) \qquad (\forall r \in (0, 1), \; n \ge 1).}
   \]
   Summing over \(k \ge 1\) by splitting at \(K = \lfloor \sqrt{2cn}/\tau \rfloor\) yields
   \[
   \sum_{k=1}^\infty |d_n^*(r_{c,k})| \le K + \frac{2nc}{\tau^2}\sum_{k=K+1}^\infty \frac{1}{k^2} \le \frac{2\sqrt{2c}}{\tau}\sqrt{n} + 1 = O_c(\sqrt{n}),
   \]
   and \(\sum_{k=1}^\infty d_n^*(r_{c,k}) = \Delta^n a_0^{(c)} - (-1)^{n-1}a_0^{(c)}\). Since \(\bigl|\binom{z}{n}\bigr| = O_z(n^{-\operatorname{Re}(z)-1})\), the double series \(\sum_{n=0}^\infty \sum_{k=1}^\infty \bigl|\binom{z}{n} d_n^*(r_{c,k})\bigr|\) is majorized by \(O_{c,z}\bigl(\sum_{n=1}^\infty n^{-\operatorname{Re}(z)-1/2}\bigr) < \infty\) on the open half-plane \(\operatorname{Re}(z) > 1/2\). By Fubini's theorem and the elementary identity \(\sum_{n=0}^\infty (-1)^{n-1}\binom{z}{n} = -(1-1)^z = 0\) for \(\operatorname{Re}(z) > 0\),
   \[
   \sum_{n=0}^\infty \Delta^n a_0^{(c)}\binom{z}{n} = \sum_{k=1}^\infty (2z-1)r_{c,k}^z = \mathcal{R}_c(z) \qquad \left(\operatorname{Re}(z) > \frac{1}{2}\right).
   \]
3. **Analytic continuation to all of \(\mathbb{C}\):** By the saddle bound \(|\Delta^n a_0^{(c)}| = O(n^{1/2}e^{-\kappa(c)n^{1/3}})\) with \(\kappa(c) > 0\) (Sections N–O), the Newton series \(F_c(z) := \sum_{n=0}^\infty \Delta^n a_0^{(c)}\binom{z}{n}\) converges absolutely and locally uniformly on all compact subsets of \(\mathbb{C}\) to an entire function. Since \(F_c(z)\) and \(\mathcal{R}_c(z)\) are both entire on \(\mathbb{C}\) and agree on the open half-plane \(\operatorname{Re}(z) > 1/2\), the analytic continuation identity theorem forces \(F_c(z) = \mathcal{R}_c(z)\) on all of \(\mathbb{C}\). \(\blacksquare\)

---

### M. Newton convergence domain

We explicitly separate the four analytic domains:
1. **Domain of convergence of the Newton series \(\sum_{n\ge 0} \Delta^n a_0^{(c)}\binom{z}{n}\):** All of \(\mathbb{C}\) (for any fixed \(c > 0\)), because \(|\Delta^n a_0^{(c)}| = O(n^{1/2}e^{-\kappa(c)n^{1/3}})\) decays faster than any power \(n^{-M}\) while \(\bigl|\binom{z}{n}\bigr| = O_z(n^{-\operatorname{Re}(z)-1})\).
2. **Domain of direct double-series Fubini equality with \(\mathcal{R}_c(z)\):** The open half-plane \(\{z \in \mathbb{C} : \operatorname{Re}(z) > 1/2\}\) for \(0 < c < \tau^2\).
3. **Domain of locally uniform convergence:** Every compact subset \(K \subset \mathbb{C}\) by the Weierstrass \(M\)-test.
4. **Domain of analytic-continuation equality \(\sum_{n\ge 0} \Delta^n a_0^{(c)}\binom{z}{n} = \mathcal{R}_c(z)\):** All of \(\mathbb{C}\), including the critical strip \(0 < \operatorname{Re}(z) < 1/2\) and the first zero argument \(\alpha_1 = \frac{1}{4} + i\frac{\gamma_1}{2}\).

---

### N. Correct Nörlund–Rice saddle geometry

By Euler's series transformation, the ordinary generating function of the forward differences \(\Delta^n a_0^{(c)}\) is
\[
\boxed{
C_c(w) := \sum_{n=0}^\infty \Delta^n a_0^{(c)} w^n = \frac{1}{1+w}A_c\!\left(\frac{w}{1+w}\right) = \frac{cw}{8(1+w)^2\sin^2\!\left(\frac{1}{2}\sqrt{\frac{cw}{1+w}}\right)}.
}
\]
Setting \(w = -1 + s\) (\(s = 1 + w \to 0\) in \(\mathbb{C} \setminus (-\infty, 0]\) with principal branch \(\sqrt{s}\)), we have \(\frac{w}{1+w} = -\frac{1-s}{s}\), so
\[
\sin^2\!\left(\frac{1}{2}\sqrt{\frac{cw}{1+w}}\right) = -\sinh^2\!\left(\frac{1}{2}\sqrt{\frac{c(1-s)}{s}}\right) = -\frac{1}{4}\exp\!\left(\frac{\sqrt{c(1-s)}}{\sqrt{s}}\right)\left(1 - O\bigl(e^{-\sqrt{c}/\sqrt{s}}\bigr)\right),
\]
which gives the exact singular form near \(w = -1\):
\[
\boxed{
C_c(-1+s) = \frac{c(1-s)}{2s^2}\exp\!\left(-\frac{\sqrt{c(1-s)}}{\sqrt{s}}\right)\Bigl(1 + O\bigl(e^{-\sqrt{c}/\sqrt{s}}\bigr)\Bigr) \sim \frac{c}{2s^2}\exp\!\left(-\frac{\sqrt{c}}{\sqrt{s}}\right).
}
\]
By Cauchy's theorem, \(\Delta^n a_0^{(c)} = \frac{1}{2\pi i}\oint (-1+s)^{-n-1} C_c(-1+s)\,ds = \frac{(-1)^{n+1}}{2\pi i}\oint (1-s)^{-n-1} C_c(-1+s)\,ds\). The leading saddle action is \(ns - \frac{\sqrt{c}}{\sqrt{s}}\), whose saddle equation
\[
\frac{d}{ds}\left(ns - \frac{\sqrt{c}}{\sqrt{s}}\right) = n + \frac{\sqrt{c}}{2s^{3/2}} = 0 \iff s^{3/2} = -\frac{\sqrt{c}}{2n} = \frac{\sqrt{c}}{2n}e^{\pm i\pi}
\]
has the conjugate saddle pair
\[
\boxed{
s_\pm \sim \left(\frac{\sqrt{c}}{2n}\right)^{2/3} e^{\pm 2\pi i/3}.
}
\]

---

### O. Corrected stretched-exponential constants

Evaluating the saddle action \(-ns_\pm + \frac{\sqrt{c}}{\sqrt{s_\pm}} = -3ns_\pm = 3\cdot 2^{-2/3}c^{1/3}n^{1/3}e^{\mp i\pi/3} = \frac{3}{2^{5/3}}c^{1/3}n^{1/3}(1 \mp i\sqrt{3})\) yields the exact real decay constant and oscillatory phase constant:
\[
\boxed{
\kappa(c) = \frac{3}{2^{5/3}}c^{1/3}, \qquad \omega(c) = \frac{3\sqrt{3}}{2^{5/3}}c^{1/3} = \sqrt{3}\,\kappa(c).
}
\]
In particular:
- **\(\pi\)-normalization (\(c = 4\)):**
  \[
  \boxed{\kappa(4) = \frac{3}{2} = 1.5, \qquad \omega(4) = \frac{3\sqrt{3}}{2} \approx 2.598076211353316}
  \]
  with **no** spurious \(\pi^{2/3}\) factor.
- **\(\tau\)-normalization (\(c = 1\)):**
  \[
  \boxed{\kappa(1) = \frac{3}{2^{5/3}} \approx 0.9449407874211548, \qquad \omega(1) = \frac{3\sqrt{3}}{2^{5/3}} \approx 1.6366852853349013.}
  \]

Carrying out the Gaussian steepest-descent integration over both conjugate saddles \(s_\pm\) gives the full asymptotic (Section 24):
\[
\boxed{
\Delta^n a_0^{(c)} = (-1)^{n+1} K(c) n^{\mu} e^{-\kappa(c)n^{1/3}}\Bigl[\cos\!\bigl(\omega(c)n^{1/3} + \phi(c)\bigr) + O(n^{-\eta})\Bigr],
}
\]
where
\[
\boxed{K(c) = \frac{2\sqrt{c}}{\sqrt{3\pi}}, \qquad \mu = \frac{1}{2}, \qquad \phi(c) = \frac{\pi}{6}, \qquad \eta = \frac{1}{3}.}
\]
With the 1-loop steepest-descent curvature and amplitude correction included (`evaluate_delta_n_a0_saddle_asymptotic`), the relative error against exact rational forward differences \(\Delta^n a_0^{(\pi)}\) is \(3.26 \times 10^{-4}\) at \(n = 120\) and \(9.48 \times 10^{-4}\) at \(n = 200\).

---

### P. Newton remainder at \(\alpha_1\)

At the first zeta-zero argument \(\alpha_1 = \frac{\rho_1}{2} = \frac{1}{4} + i\frac{\gamma_1}{2}\), \(\mathcal{R}_c(\alpha_1) = 0\), so the Newton polynomial evaluation is the negative tail of the convergent Newton series:
\[
N_n^{(c)}(\alpha_1) = -\bigl(\mathcal{R}_c(\alpha_1) - N_n^{(c)}(\alpha_1)\bigr) = -\sum_{k=n+1}^\infty \Delta^k a_0^{(c)} \binom{\alpha_1}{k}.
\]
Using the Gamma-function asymptotic
\[
\binom{\alpha_1}{k} = \frac{(-1)^k}{\Gamma(-\alpha_1)} k^{-\alpha_1-1}\bigl(1 + O(k^{-1})\bigr) = \frac{(-1)^k}{\Gamma(-\alpha_1)} k^{-5/4} e^{-i(\gamma_1/2)\log k}\bigl(1 + O(k^{-1})\bigr),
\]
the alternating signs \((-1)^{k+1}\) in \(\Delta^k a_0^{(c)}\) and \((-1)^k\) in \(\binom{\alpha_1}{k}\) multiply to \(-1\), so the summand is non-alternating in \(k\) and has phase \(\pm\omega(c)k^{1/3} - \frac{\gamma_1}{2}\log k\). Integrating by parts / Euler–Maclaurin over \(k > n\) divides by the derivative of the stretched-exponential exponent, \(\frac{d}{dk}\bigl[(-\kappa(c) \pm i\omega(c))k^{1/3}\bigr] = \frac{1}{3}k^{-2/3}\cdot 2\kappa(c)e^{\pm 2\pi i/3}\), which multiplies the power of \(n\) by \(n^{2/3}\) (\(\frac{1}{2} - \frac{5}{4} + \frac{2}{3} = -\frac{1}{12}\)) and shifts the cosine phase from \(\frac{\pi}{6}\) by \(+\frac{\pi}{3}\) to \(\frac{\pi}{2}\):
\[
\boxed{
N_n^{(c)}(\alpha_1) = \frac{2^{7/6}c^{1/6}}{\sqrt{3\pi}\,\Gamma(-\alpha_1)}\, n^{-1/12 - i\gamma_1/2} e^{-\kappa(c)n^{1/3}}\Bigl[\cos\!\bigl(\omega(c)n^{1/3} + \tfrac{\pi}{2}\bigr) + O(n^{-1/3})\Bigr].
}
\]

---

### Q. Two-consecutive lower envelope

Consider the structurally positive two-approximant quantity
\[
\boxed{E_n^{(c)} := |N_n^{(c)}(\alpha_1)|^2 + |N_{n+1}^{(c)}(\alpha_1)|^2.}
\]
We strictly separate the **Lean-proved finite algebraic skeleton** (`PROVED_ALGEBRAIC_FINITE_STEP_IDENTITY`) from the **analytic saddle/phase lower envelope** (`PROVED_PAPER_DERIVATION_PENDING_ASYMPTOTIC_RIGOR_AUDIT`):

1. **Lean-Proved Finite Algebraic Skeleton (`PROVED_ALGEBRAIC_FINITE_STEP_IDENTITY`):**
   - Exact consecutive-step difference identity:
     \[
     \boxed{N_{n+1}^{(c)}(\alpha_1) - N_n^{(c)}(\alpha_1) = \Delta^{n+1} a_0^{(c)} \binom{\alpha_1}{n+1}.}
     \]
   - Elementary maximum step lower bound:
     \[
     \boxed{\max\bigl(|N_n^{(c)}(\alpha_1)|, |N_{n+1}^{(c)}(\alpha_1)|\bigr) \ge \frac{1}{2}\left|\Delta^{n+1}a_0^{(c)}\binom{\alpha_1}{n+1}\right|.}
     \]
   - Elementary quadratic inequality (`two_phase_cosine_square_lower_bound` in Lean 4):
     \[
     \boxed{3 E_n^{(c)} = 3\bigl(|N_n^{(c)}(\alpha_1)|^2 + |N_{n+1}^{(c)}(\alpha_1)|^2\bigr) \ge |N_n^{(c)}(\alpha_1)|^2 + \bigl|N_{n+1}^{(c)}(\alpha_1) - N_n^{(c)}(\alpha_1)\bigr|^2.}
     \]

2. **Analytic Saddle/Phase Lower Envelope (`PROVED_PAPER_DERIVATION_PENDING_ASYMPTOTIC_RIGOR_AUDIT`):**
   Comparing the oscillatory cosine phases of the two terms on the right-hand side:
   - In \(N_n^{(c)}(\alpha_1)\), the leading saddle cosine factor is \(\cos\theta_{\mathrm{tail}}(n)\) with \(\theta_{\mathrm{tail}}(n) = \omega(c)n^{1/3} + \frac{\pi}{2}\).
   - In \(N_{n+1}^{(c)}(\alpha_1) - N_n^{(c)}(\alpha_1) = \Delta^{n+1}a_0^{(c)}\binom{\alpha_1}{n+1}\), the leading saddle cosine factor is \(\cos\theta_{\mathrm{diff}}(n)\) with \(\theta_{\mathrm{diff}}(n) = \omega(c)n^{1/3} + \frac{\pi}{6} + O(n^{-2/3})\).
   Their leading phase difference is the constant \(O(1)\) angle
   \[
   \boxed{\Delta\theta = \theta_{\mathrm{tail}}(n) - \theta_{\mathrm{diff}}(n) = \frac{\pi}{2} - \frac{\pi}{6} = \frac{\pi}{3}, \qquad \sin^2\!\left(\frac{\pi}{3}\right) = \frac{3}{4} > 0,}
   \]
   giving \(\cos^2(\theta + \frac{\pi}{2}) + \cos^2(\theta + \frac{\pi}{6}) \ge 1 - \cos(\frac{\pi}{3}) = \frac{1}{2} > 0\). Under the paper saddle derivation (which depends on (i) the \(O(n^{-1/3})\) saddle remainder for \(\Delta^n a_0^{(c)}\), (ii) the complex binomial/tail asymptotic for \(N_n^{(c)}(\alpha_1)\), (iii) the \(\pi/3\) phase displacement between tail and increment, and (iv) uniform domination of subleading contour/saddle contributions at the complex node \(\alpha_1 = \frac{1}{4} + i\frac{\gamma_1}{2}\)), this yields the two-sided paper asymptotic enclosure for sufficiently large \(n\):
   \[
   \boxed{
   C_1(c)\, n^{-3/2} e^{-2\kappa(c)n^{1/3}} \le E_n^{(c)} \le C_2(c)\, n^{-1/6} e^{-2\kappa(c)n^{1/3}},
   }
   \]
   and therefore
   \[
   \boxed{
   -\log E_n^{(c)} = 2\kappa(c)n^{1/3} + O(\log n) \implies \lim_{n\to\infty} \frac{-\log E_n^{(c)}}{n} = 0.
   }
   \]

---

### R. Gate-Z5 reassessment

Under the two-sided paper saddle enclosure \(-\log E_n^{(c)} = 2\kappa(c)n^{1/3} + O(\log n)\), no subsequence of \(n\) achieves superlinear logarithmic decay \(-\log E_n^{(c)} \gg n\). After multiplying by the integer-clearing factor \(C_n^{(c)} \ge 1\) to form \(G_n^{(c)}(Y) = C_n^{(c)}\bigl(\mathcal{N}_{N_n^{(c)}}(Y) + \mathcal{N}_{N_{n+1}^{(c)}}(Y)\bigr) \in \mathbb{Z}[Y]\), we have \(G_n^{(c)}(\gamma_1) = C_n^{(c)} E_n^{(c)} \ge E_n^{(c)}\) (with \(C_n^{(c)} E_n^{(c)} \ge \exp(4n\log n + O_c(n)) \to +\infty\)).

Because the analytic saddle remainder bounds (i)–(iv) at the complex node \(\alpha_1 = \frac{1}{4} + i\frac{\gamma_1}{2}\) are established at the level of a paper steepest-descent derivation rather than a formally verified or ball-certified all-\(n\) remainder theorem, the Newton two-approximant lower-envelope status is classified as:
\[
\boxed{\texttt{PROVED\_PAPER\_DERIVATION\_PENDING\_ASYMPTOTIC\_RIGOR\_AUDIT}, \qquad \texttt{SUBGATE-TC-039A} = \texttt{OPEN}.}
\]

---

### S. Newton denominator asymptotics

By the unipotence of the Stirling transition matrices \(z^k = \sum_{j=0}^k S(k, j)\,j!\binom{z}{j}\) and \(k!\binom{z}{k} = \sum_{j=0}^k s(k, j) z^j\) over \(\mathbb{Z}\), the power-basis least common denominator \(L_n^{(c)} := \operatorname{lcm}_{0\le j\le n} \operatorname{den}\bigl([z^j]N_n^{(c)}(z)\bigr)\) satisfies the exact identity
\[
\boxed{
L_n^{(c)} = \operatorname{lcm}_{0\le k\le n} \operatorname{den}\!\left(\frac{\Delta^k a_0^{(c)}}{k!}\right), \qquad M_n^{(c)} \;\Big|\; L_n^{(c)} \;\Big|\; n!\,M_n^{(c)}, \qquad M_n^{(c)} := \operatorname{lcm}_{0\le m\le n} \operatorname{den}(a_m^{(c)}).
}
\]
We separate the unconditional upper bound from the unconditional lower bounds:
1. **Unconditional upper bound:** Since \(\operatorname{den}(a_m^{(\tau)}) \mid 2(2m)!\prod_{(p-1)\mid 2m} p\), Stirling's formula and \(\prod_{p-1\le 2n} p \le 4^{2n}\) give
   \[
   \boxed{\log L_n^{(c)} \le 3n\log n + O_c(n).}
   \]
2. **Unconditional lower bound from sample denominators \(M_n^{(c)}\):** For every odd prime \(p \le 2n+1\) not dividing \(\operatorname{num}(c)\), let \(m_p = \lfloor\frac{n}{(p-1)/2}\rfloor\frac{p-1}{2} \le n\). By the von Staudt–Clausen theorem, \(v_p(B_{2m_p}) = -1\), so \(v_p(\operatorname{den}(a_{m_p}^{(c)})) = 1 + v_p((2m_p)!) - v_p(2m_p-1) \ge \frac{2n}{p-1} - O(\log_p n)\). Summing over \(p \le 2n\) by Mertens' theorem gives \(\log M_n^{(c)} = 2n\log n + O_c(n)\), hence \(\log L_n^{(c)} \ge 2n\log n + O_c(n)\).
3. **Unconditional Kummer ultrametric lower bound:** For every prime \(p \le \sqrt{2n}\) not dividing \(\operatorname{num}(c)\), choose \(k_p = \lfloor\frac{n}{p(p-1)/2}\rfloor\frac{p(p-1)/2} \in (n - p^2/2, n]\). At \(m = k_p\), \((p-1) \mid 2k_p\) so \(v_p(B_{2k_p}) = -1\), and for every \(m < k_p\) we have \(v_p((2m)!) \le v_p((2k_p)!) - 2\), so the top term \(m = k_p\) in \(\Delta^{k_p} a_0^{(c)} / k_p!\) has strictly minimal \(p\)-adic valuation \(-v_p((2k_p)!) - 1 - v_p(k_p!)\). Summing over \(p \le \sqrt{2n}\) yields the unconditional lower bound
   \[
   \boxed{\frac{5}{2}n\log n + O_c(n) \le \log L_n^{(c)} \le 3n\log n + O_c(n),}
   \]
   with \(\log L_n^{(c)} = 3n\log n + O_c(n)\) holding across all regular primes (and verified numerically up to \(n = 200\)).

---

### T. Prime-by-prime \(\pi/\tau\) valuation audit

Since \(a_m^{(\pi)} = 4^m a_m^{(\tau)} = 2^{2m} a_m^{(\tau)}\), we have:
- **Odd primes \(p \ge 3\):**
  \[
  \boxed{v_p\bigl(a_m^{(\pi)}\bigr) = v_p\bigl(a_m^{(\tau)}\bigr) \qquad (\forall p \ge 3, \; \forall m \ge 0).}
  \]
- **Dyadic prime \(p = 2\):** Since \(v_2(B_{2m}) = -1\) for \(m \ge 1\) and \(v_2((2m)!) = 2m - s_2(m)\),
  \[
  \boxed{v_2\bigl(a_m^{(\tau)}\bigr) = -(4m - s_2(m) + 1), \qquad v_2\bigl(a_m^{(\pi)}\bigr) = v_2\bigl(a_m^{(\tau)}\bigr) + 2m = -(2m - s_2(m) + 1).}
  \]
- **Propagation to \(L_n^{(\pi)}\) and \(L_n^{(\tau)}\):** Across all \(1 \le n \le 80\), exact rational computation confirms that \(L_n^{(\tau)} / L_n^{(\pi)}\) is an **exact power of \(2\)**:
  \[
  \boxed{v_p\bigl(L_n^{(\pi)}\bigr) = v_p\bigl(L_n^{(\tau)}\bigr) \quad (\forall p \ge 3), \qquad v_2\bigl(L_n^{(\tau)}\bigr) - v_2\bigl(L_n^{(\pi)}\bigr) = 2n + O(1).}
  \]
This reveals precisely what \(\pi\)-notation was doing: the factor \(4^m = 2^{2m}\) in \(a_m^{(\pi)}\) cancels \(2n\) powers of \(2\) out of the \(4n\) dyadic denominator powers in \(L_n^{(\tau)}\), while leaving **every odd prime \(p \ge 3\)** in \((2m)!\) and \(\operatorname{den}(B_{2m})\) completely untouched!

---

### U. Padé evidence repair

For Route B (multipoint Padé interpolation \(A_n(m) - a_m^{(c)} B_n(m) = 0\) on \(m = 0, \dots, d_A + d_B\)):
- **Proven algebraic properties (`MULTIPOINT_PADE_ARGUMENT_POLYNOMIALIZATION_PROVED`):** Existence holds for all \((d_A, d_B)\) by homogeneous linear algebra over \(\mathbb{Q}\); projective uniqueness (\(\operatorname{nullity} = 1\)) and exact node interpolation are certified for every tested \((d_A, d_B)\) up to \(n = 25\) across \([n/n], [n/(n-1)], [(n-1)/n]\); and at \(z = \alpha_1\) where \(\mathcal{R}_c(\alpha_1) = 0\), the residual satisfies the exact identity \(E_n(\alpha_1) = A_n(\alpha_1) - \mathcal{R}_c(\alpha_1)B_n(\alpha_1) = A_n(\alpha_1)\) (`pade_interpolation_zero_residual_identity`).
- **Scoped Gate-Z5 evidence (`MULTIPOINT_PADE_GATE_Z5_NEGATIVE_NUMERICAL_EVIDENCE`):** On the tested range \(1 \le n \le 25\) (in \(\pi\)-normalization) and \(1 \le n \le 8\) (in \(\tau\)-normalization), the rational quotient \(|A_n(\alpha_1)/B_n(\alpha_1)|\) becomes small (\(4.17 \times 10^{-10}\) at \(n = 25\)) only because \(|B_n(\alpha_1)|\) grows factorially, whereas the primitive integer polynomial evaluation \(|\widetilde{A}_n(\alpha_1)|\) grows rapidly (\(I_{25}^{\mathrm{Pad\acute{e}},\mathbb{Z}} = -186.64\) for \(\pi\); \(I_8^{\mathrm{Pad\acute{e}},\mathbb{Z}} = -58.97\) for \(\tau\)). Because an all-\(n\) closed-form determinant asymptotic for the confluent discrete-moment matrix \(\bigl(\Delta^{d_A+1}[m^j a_m^{(c)}]_{m=r}\bigr)\) remains an open analytic problem, this negative finding is classified strictly as certified finite evidence on the tested range rather than an unproved all-\(n\) theorem.

---

### V. C1 degree repair

For the C1 divided-difference Hankel matrix \(M_n^{(\mathrm{C1})}(X) = \bigl(\frac{a_{i+j+1}^{(c)}}{i+j+1-X}\bigr)_{0\le i,j<n}\), the denominator factor \((m - X)^{-1}\) (\(1 \le m \le 2n-1\)) lies on the anti-diagonal \(i + j + 1 = m\), which has length \(\min(m, 2n-m)\). Hence any permutation product in the Leibniz expansion of \(\det M_n^{(\mathrm{C1})}(X)\) contains at most \(\min(m, 2n-m)\) entries from anti-diagonal \(m\), so the minimal universal polynomial denominator clearing all entries of \(\det M_n^{(\mathrm{C1})}(X)\) is
\[
\boxed{U_n(X) = \prod_{m=1}^{2n-1} (m - X)^{\min(m, 2n-m)}, \qquad \deg_X U_n(X) = \sum_{m=1}^{2n-1} \min(m, 2n-m) = n^2.}
\]
All prose references are synchronized to \(\deg_X U_n = n^2\).

---

### W. Fixed rational gauges

Combining the saddle theorem (Sections N–O), the denominator valuation theorem (Section S), and the Hankel scaling law (Sections I–K), every fixed rational gauge \(c = u/v \in \mathbb{Q}_{>0}\) (\(0 < c < \tau^2\)) preserves:
1. the \(n^{1/3}\) stretched-exponential Newton decay exponent (\(\kappa(c) = \frac{3}{2^{5/3}}c^{1/3}\)):
   `FIXED_RATIONAL_NORMALIZATION_GAUGE_DOES_NOT_CHANGE_NEWTON_STRETCHED_EXPONENT`;
2. the \(n\log n\) leading Newton denominator order (\(\bigl|\log L_n^{(c)} - \log L_n^{(\tau)}\bigr| \le n\log(uv) = O_c(n)\));
3. the \(2n^2\log n\) leading Hankel denominator order (\(-\log D_n^{(c)} = 2n^2\log n + (6\log 2 - 3 - \log c)n^2 + O(n\log n)\)).

This establishes **Decision Tree Outcome D**:
\[
\boxed{\texttt{FIXED\_RATIONAL\_NORMALIZATION\_GAUGES\_EQUIVALENT\_AT\_LEADING\_DIOPHANTINE\_ORDER}.}
\]

---

### X. Variable rational gauges

For a degree-\(n\) integer-cleared ordinate polynomial \(P_n^{(c)}(Y) \in \mathbb{Z}[Y]\), define the normalization-invariant Diophantine efficiency metric:
\[
\boxed{\mathscr{E}_n(c) := \frac{-\log|P_n^{(c)}(\gamma_1)|}{\deg P_n^{(c)}}.}
\]
Gate Z5 requires \(\mathscr{E}_n(c_n) \to +\infty\). Investigating zero-independent variable gauges \(c = c_n \in \mathbb{Q}_{>0}\) reveals an exact **analytic-vs-arithmetic pincer**:
- **Regime 1 (\(0 < c_n < \tau^2\)):** All Dirichlet modes \(r_{c_n,k} = \frac{c_n}{\tau^2 k^2}\) lie in \((0, 1)\), so \(\kappa(c_n) < \frac{3}{2^{5/3}}\tau^{2/3} = \frac{3\pi^{2/3}}{2}\) is bounded above by \(O(1)\). The raw analytic decay remains \(O(n^{1/3})\), while \(\log L_n^{(c_n)} \ge \frac{5}{2}n\log n + O(n)\), giving \(\mathscr{E}_n(c_n) \sim -3\log n \to -\infty\).
- **Regime 2 (\(c_n > \tau^2 = 4\pi^2\), e.g. \(c_n = 2^n\) or \(c_n = \operatorname{lcm}(1, \dots, 2n)\)):** Once \(c_n > \tau^2\), the leading Dirichlet mode \(r_{c_n,1} = \frac{c_n}{\tau^2} > 1\) crosses outside the unit interval, so the sample sequence \(a_m^{(c_n)} \sim (2m-1)(c_n/\tau^2)^m\) **grows exponentially** with \(m\), and the raw analytic evaluation \(|N_n^{(c_n)}(\alpha_1)|\) grows as \((c_n/\tau^2 + 1)^n \to +\infty\) instead of decaying!

| Gauge family | \(n\) | \(\deg P_n^{(c)}\) | \(-\log|N_n^{(c)}(\alpha_1)|\) | \(\log L_n^{(c)}\) | \(\log H(P_n^{(c),\mathrm{prim}})\) | \(\mathscr{E}_n^{\mathrm{prim}}(c)\) |
|---|---:|---:|---:|---:|---:|---:|
| Fixed \(\tau\) (\(c=1\)) | \(15\) | \(30\) | \(+2.426\) | \(109.75\) | \(216.17\) | \(-6.458\) |
| Fixed \(\pi\) (\(c=4\)) | \(15\) | \(30\) | \(+2.596\) | \(88.96\) | \(188.01\) | \(-5.525\) |
| Variable \(c_n = 2^n\) | \(15\) | \(30\) | \(-99.512\) | \(68.16\) | \(188.01\) | \(-5.525\) |
| Variable \(c_n = \operatorname{lcm}(1\dots 2n)\) | \(15\) | \(30\) | \(-364.262\) | \(15.42\) | \(710.89\) | \(-25.134\) |

Thus variable gauges \(c_n\) cannot bypass the factorial obstruction (`variable_gauge_breaks_obstruction = False`).

---

### Y. TC normalization firewall

Although \(\tau = 2\pi\) is the canonical transcendental unit of the `reimann_scope` project, the factor \(\tau^{-2z}\) in \(\mathcal{R}_\tau(z) = (2z-1)\tau^{-2z}\zeta(2z)\) is an **analytic normalization prefactor** cancelling \(\tau^{2m}\) in Euler's even-zeta formula at \(z = m \in \mathbb{Z}_{\ge 0}\). It is **not** a legal geometric TC grade action \(F_\tau(s, k) = f(\tau^{-k} s)\) on the complex argument of \(\zeta\) (`TAU_ANALYTIC_NORMALIZATION_DISTINCT_FROM_TC_GRADE_ACTION`).

---

### Z. Principal classification and exact next theorem

1. **Answer to Governing Question 1 (Was the `TASK-TC-039` Gate-Z5 no-go actually proved?):**
   - For the **Newton route**, `TASK-TC-039R` separates the **Lean-proved finite algebraic step skeleton** (`N_{n+1}^{(c)}(\alpha_1) - N_n^{(c)}(\alpha_1) = \Delta^{n+1}a_0^{(c)}\binom{\alpha_1}{n+1}`, `\max(|N_n^{(c)}|, |N_{n+1}^{(c)}|) \ge \frac{1}{2}|\Delta^{n+1}a_0^{(c)}\binom{\alpha_1}{n+1}|`, and `two_phase_cosine_square_lower_bound`: `3(a^2+b^2) \ge a^2+(b-a)^2`, `PROVED_ALGEBRAIC_FINITE_STEP_IDENTITY`) from the **analytic saddle/phase lower envelope** (`C_1(c)n^{-3/2}e^{-2\kappa(c)n^{1/3}} \le E_n^{(c)} \le C_2(c)n^{-1/6}e^{-2\kappa(c)n^{1/3}}`, `PROVED_PAPER_DERIVATION_PENDING_ASYMPTOTIC_RIGOR_AUDIT`), which depends on the `O(n^{-1/3})` saddle remainder, the complex binomial/tail asymptotic at `\alpha_1`, the `\pi/3` phase displacement, and uniform domination of subleading contour/saddle contributions (`SUBGATE-TC-039A = OPEN`).
   - For the **multipoint Padé route**, algebraic polynomialization is proved for all \(n\) (`MULTIPOINT_PADE_ARGUMENT_POLYNOMIALIZATION_PROVED`), while the Gate-Z5 failure is scoped to certified finite evidence on \(n \le 25\) (`MULTIPOINT_PADE_GATE_Z5_NEGATIVE_NUMERICAL_EVIDENCE`).
2. **Answer to Governing Question 2 (Does \(\tau\)-normalization expose a mathematically different arithmetic route?):**
   - Yes at the level of primitive arithmetic structure: \(\mathcal{R}_\tau(z) = (2z-1)\tau^{-2z}\zeta(2z)\) strips out the artificial \(4^m = 2^{2m}\) dyadic factor from \(\mathcal{R}_\pi(m)\) and exposes the rational core \(\tau^{-2m}\zeta(2m) = (-1)^{m+1}\frac{B_{2m}}{2(2m)!} \in \mathbb{Q}_{>0}\) (`TAU_NORMALIZATION_EXPOSES_EVEN_ZETA_RATIONAL_CORE`).
   - However, at the level of Diophantine approximation order, \(\pi\) (\(c = 4\)) and \(\tau\) (\(c = 1\))—and every fixed rational gauge \(c \in \mathbb{Q}_{>0}\) in \(\mathcal{R}_c(z) = c^z \mathcal{R}_\tau(z)\)—differ only at prime divisors of \(c\) (\(p = 2\) for \(\pi\) vs. \(\tau\)), leaving all odd-prime factorial denominators \((2m)!\), the \(n^{1/3}\) stretched-exponential exponent, the \(n\log n\) Newton denominator class, and the \(2n^2\log n\) Hankel denominator class invariant (`FIXED_RATIONAL_NORMALIZATION_GAUGES_EQUIVALENT_AT_LEADING_DIOPHANTINE_ORDER`).
3. **Exact Next Subgate (`SUBGATE-TC-040A`):**
   - Because any exponential gauge \(c^z \mathcal{R}_\tau(z)\) preserves the \((2m)!\) factorial denominator at all odd primes \(p \ge 3\), `SUBGATE-TC-040A` must target a non-exponential entire multiplier \(F(z) = E(z)\mathcal{R}_\tau(z)\) (where \(E(m)\) supplies the factorial factor \((2m)!\) up to \(\exp(O(m))\) denominators while \(E(\alpha_1) \ne 0\)) or a non-polynomial integral/Hadamard kernel, in parallel with `SUBGATE-TC-038A`.
   - `SUBGATE-TC-039A` remains `OPEN` (pending asymptotic error-term audit), `OBL-CT-001A` remains `OPEN`, and `rh_claimed = False`.
