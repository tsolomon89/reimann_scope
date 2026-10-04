# Riemann Converter Grade Covariance and Prime-Staircase Compatibility

**Document ID**: `docs/reviews/TC_RIEMANN_CONVERTER_GRADE_COMPATIBILITY.md`  
**Task Reference**: `TASK-TC-021`  
**Author**: Antigravity (Advanced Agentic Coding / Riemann Scope Research Lead)  
**Status**: `COMPLETED`  
**Classification**: `PURE_CONVERTER_COVARIANCE_AND_ARITHMETIC_REALIZATION_MISMATCH`  
**Associated Artifact**: [`data/tc_riemann_converter_grade_compatibility.json`](file:///C:/Development/Projects/reimann_scope/data/tc_riemann_converter_grade_compatibility.json)  
**Formal Proof Module**: [`formal/RiemannScope/RiemannConverter.lean`](file:///C:/Development/Projects/reimann_scope/formal/RiemannScope/RiemannConverter.lean)  
**Dedicated Test Suite**: [`tests/test_tc_riemann_converter_grade_compatibility.py`](file:///C:/Development/Projects/reimann_scope/tests/test_tc_riemann_converter_grade_compatibility.py) (15 unit tests passing)

---

## 1. Executive Summary & Governing Question

This sprint investigates the concrete mathematical mechanism by which the Riemann explicit formula and its single-frequency building block—termed the **Riemann Converter**—tunes logarithmic coordinates into the prime-counting staircase, and tests whether reciprocal coordinate scaling under Transcendental Continuation (TC) creates an authentic constraint on off-critical zeta zeros.

The governing questions are:
1. **Why does the same harmonic tuning survive when a complex zero is transformed by TC and the spatial coordinate is transformed reciprocally?**
2. **Does the TC arithmetic grade realization $L_K = \{n\tau^K : n \in \mathbb{Z} \setminus \{0\}\}$ force a compatibility condition between the analytic prime embedding $p^{\tau^{-K}}$ and the arithmetic embedding $p\tau^K$ that an off-critical zero cannot satisfy?**

### Definitive Conclusions:
1. **Exact Converter Scale-Covariance**: The identity
   $$T_{c\sigma, ct}\left(x^{1/c}\right) = T_{\sigma, t}(x)$$
   is an **exact mathematical theorem** holding term-by-term for every $n \ge 1$, for every finite truncation, and for any positive real scale factor $c > 0$. Specializing to $c = \tau^K = (2\pi)^K$ yields exact TC covariance.
2. **Generic Scale Geometry**: Generic-base controls ($c = 2, 3, \pi, \sqrt{2}$) show that this covariance holds identically for every base. It is a fundamental conformal symmetry of the logarithmic integral $\operatorname{Li}(x^s) = \operatorname{Ei}(s\log x)$, classified as `GENERIC_CONVERTER_SCALE_COVARIANCE`.
3. **Analytic Dilation vs. Arithmetic Translation**:
   - Analytic TC $\zeta(\tau^{-K} s)$ induces logarithmic **dilation**: $u = \log x \mapsto \tau^{-K} u$, moving prime stations to $A_K(p) = p^{\tau^{-K}}$.
   - Arithmetic TC realization maps primes to $G_K(p) = p\tau^K$, which is logarithmic **translation**: $u \mapsto u + K\log\tau$.
4. **Canonical Defect Provenance**: On the centered harmonic $H_\rho(x) = x^{\rho - 1/2}$, analytic reciprocal scaling is strictly invariant ($|H_{K}| = x^\delta$), whereas arithmetic translation introduces the modulus factor $\tau^{K\delta}$. Bilateral symmetrization recovers the canonical TC non-unitarity defect:
   $$\tau^{K\delta} + \tau^{-K\delta} - 2 = 4\sinh^2\left(\frac{K\delta\log\tau}{2}\right) = B_\rho(K).$$
5. **No Induced Compatibility**: Candidate intrinsic prime invariants (prime labels, ordinal jump heights $\Delta\pi = 1$, Möbius weights $\mu(n)/n$) do **not** force $A_K(p) = G_K(p)$. In fact, setting $H_\rho(A_K(p)) = H_\rho(G_K(p))$ across any two distinct primes is **mathematically impossible** (multi-prime rigidity theorem).
6. **Principal Classification**: `PURE_CONVERTER_COVARIANCE_AND_ARITHMETIC_REALIZATION_MISMATCH`.

---

## 2. Answers to Canonical Sprint Questions (A through O)

### A. What exactly is the supplied Riemann Converter?
The displayed function in the prompt and video artifact is:
$$T_{\sigma,t}(x) = \Re\left( \sum_{n=1}^{\infty} \frac{\mu(n)}{n} \int_{-\infty+i\,t\log(x)/n}^{(\sigma+it)\log(x)/n} \frac{e^z}{z}\,dz \right).$$
It takes a complex frequency parameter $s = \sigma + it$ and converts it into a real-valued spatial waveform along $x > 1$.

### B. What standard explicit-formula object does it equal?
Making the substitution $z = \frac{s\log x}{n}$, the contour integral from $-\infty + i\Im(z)$ to $\Re(z) + i\Im(z)$ is the standard definition of the exponential integral $\operatorname{Ei}(z)$ along a horizontal contour avoiding the negative real branch cut.
Since $\operatorname{Ei}\left(\frac{s\log x}{n}\right) = \operatorname{Li}\left(x^{s/n}\right)$, the formula rewrites in standard notation as:
$$\boxed{T_{\sigma, t}(x) = \Re\left( \sum_{n=1}^\infty \frac{\mu(n)}{n} \operatorname{Ei}\left(\frac{(\sigma+it)\log x}{n}\right) \right) = \Re\left( \sum_{n=1}^\infty \frac{\mu(n)}{n} \operatorname{Li}\left(x^{(\sigma+it)/n}\right) \right).}$$
This is precisely the **Möbius-inverted Riemann/Gram harmonic building block** of the prime-counting function $\pi(x)$. In Riemann's 1859 explicit formula:
$$\pi(x) = \sum_{n=1}^\infty \frac{\mu(n)}{n} J\left(x^{1/n}\right), \qquad J(x) = \operatorname{Li}(x) - \sum_\rho \operatorname{Li}(x^\rho) - \log 2 + \int_x^\infty \frac{dt}{t(t^2-1)\log t}.$$
Each zero $\rho = \sigma + it$ (paired with $\overline{\rho}$) contributes $-2 T_{\sigma, t}(x)$ to $\pi(x)$.

### C. Prove or reject: $T_{\tau^K s}(x^{\tau^{-K}}) = T_s(x)$.
**PROVED**.
Let $c > 0$ be any real scale factor, and set $s = \sigma + it$. Consider the $n$-th integral in $T_{c\sigma, ct}(x^{1/c})$:
- Upper limit:
  $$\frac{(c\sigma + ict)\log(x^{1/c})}{n} = \frac{c(\sigma + it) \cdot \frac{1}{c}\log x}{n} = \frac{(\sigma + it)\log x}{n} = \frac{s\log x}{n}.$$
- Lower contour imaginary height:
  $$\frac{(ct)\log(x^{1/c})}{n} = \frac{ct \cdot \frac{1}{c}\log x}{n} = \frac{t\log x}{n}.$$
- Integrand: $\frac{e^z}{z} dz$.
- The integration path is the identical horizontal ray from $-\infty + i\frac{t\log x}{n}$ to $\frac{\sigma\log x}{n} + i\frac{t\log x}{n}$.
- Summation index: $n$ ranges over $\mathbb{N}$, and the weights $\frac{\mu(n)}{n}$ contain no dependence on $c$.
Therefore, term-by-term and for the entire sum:
$$\boxed{T_{c\sigma, ct}\left(x^{1/c}\right) = T_{\sigma, t}(x).}$$
Specializing to $c = \tau^K$ yields $T_{\tau^K s}(x^{\tau^{-K}}) = T_s(x)$ identically.

### D. What is the prime-side counting function of $\zeta(\tau^{-K} s)$?
For $\Re(s) > \tau^K$, the logarithmic derivative of $\zeta_K(s) = \zeta(\tau^{-K} s)$ is:
$$\log \zeta(\tau^{-K} s) = \sum_{p} \sum_{m=1}^\infty \frac{1}{m} p^{-m \tau^{-K} s} = \sum_{p} \sum_{m=1}^\infty \frac{1}{m} \left(p^{m \tau^{-K}}\right)^{-s} = s \int_1^\infty J_K(x) x^{-s-1} dx.$$
Hence, the prime-power counting function is:
$$J_K(x) = \sum_{p^m \le x^{\tau^K}} \frac{1}{m} = J\left(x^{\tau^K}\right).$$
Applying Möbius inversion to obtain the prime-counting function $\pi_K(x)$:
$$\pi_K(x) = \sum_{n=1}^\infty \frac{\mu(n)}{n} J_K\left(x^{1/n}\right) = \sum_{n=1}^\infty \frac{\mu(n)}{n} J\left(\left(x^{\tau^K}\right)^{1/n}\right) = \pi\left(x^{\tau^K}\right).$$
Thus:
$$\boxed{N_K(x) = N\left(x^{\tau^K}\right)}.$$

### E. Where do its staircase jumps occur?
For $\pi_K(x) = \pi(x^{\tau^K})$, a jump occurs whenever $x^{\tau^K} = p \in \mathbb{P}$, which gives:
$$\boxed{x = p^{\tau^{-K}}}.$$
For the prime-power counting function $J_K(x)$, jumps occur at:
$$\boxed{x = p^{m\tau^{-K}} = \left(p^{\tau^{-K}}\right)^m}.$$

### F. What discrete information remains integer-valued?
1. **Ordinal step count increment**: $\Delta \pi_K = 1 \in \mathbb{Z}$ at each prime jump.
2. **Möbius index**: $n \in \mathbb{N} = \{1, 2, 3, \dots\}$.
3. **Prime referents**: $p \in \mathbb{P} = \{2, 3, 5, 7, \dots\}$.
4. **Prime power exponents**: $m \in \mathbb{N} = \{1, 2, 3, \dots\}$.
*Non-integer quantities*: The spatial jump coordinates $x = p^{\tau^{-K}}$ are **not** integers. For rational $K \ne 0$, their arithmetic status is open (algebraic raised to transcendental power).

### G. What is the arithmetic meaning of $n\tau^K$ in the staircase picture?
In the repository's graded arithmetic monoid $\mathcal{M}_\tau = \mathbb{A}_{\mathbb{R}} \times \mathbb{Z}_{\ne 0}$, the map $\Phi_\tau(K, n) = n\tau^K$ is the canonical real realization homomorphism. In the staircase picture, this can be interpreted as:
- **Interpretation A (Horizontal)**: $\pi_K^{\text{horiz}}(x) = \pi(x/\tau^K)$, placing jumps at $p\tau^K$.
- **Interpretation B (Vertical)**: $\pi_K^{\text{vert}}(x) = \tau^K \pi(x)$, scaling count heights.
- **Interpretation C (Abstract Graded)**: Jump heights remain $1 \in \mathbb{Z}$, while primes carry abstract pairs $(K, p) \in \mathcal{M}_\tau$.
Interpretation A produces the arithmetic grid dilation $D_K[\zeta](s) = \tau^{-Ks}\zeta(s)$, which is distinct from the analytic converter staircase $\pi(x^{\tau^K})$.

### H. Compare: $p^{\tau^{-K}}$ with $p\tau^K$.
- **Analytic Embedding**: $A_K(p) = p^{\tau^{-K}}$. For rational $K \ne 0$, $A_K(p)$ is an algebraic integer raised to a transcendental exponent; its transcendence status is `OPEN_TRANSCENDENCE_STATUS`.
- **Arithmetic Embedding**: $G_K(p) = p\tau^K$. For rational $K \ne 0$, $p \in \overline{\mathbb{Q}}^\times$ and $\tau^K$ is transcendental by Lindemann (1882); thus $G_K(p)$ is **rigorously transcendental**.
- **Numerical Distinction**: For $K = 1, p = 2$: $A_1(2) = 2^{1/(2\pi)} \approx 1.1166$, whereas $G_1(2) = 2(2\pi) \approx 12.5664$.

### I. Derive the log-space dilation/translation distinction.
In logarithmic coordinates $u = \log x$:
$$\log A_K(p) = \tau^{-K} \log p \qquad \text{(Multiplicative dilation: } u \mapsto \tau^{-K} u\text{)}.$$
$$\log G_K(p) = \log p + K\log\tau \qquad \text{(Additive translation: } u \mapsto u + K\log\tau\text{)}.$$
Dilation and translation do not commute in $\operatorname{Aff}_+(\mathbb{R})$: $[S_K, T_J](u) = (1 - \tau^{-J}) K\log\tau \ne 0$.

### J. Derive the centered harmonic transformation.
For centered coordinate $w_\rho = \rho - 1/2 = \delta + i\gamma$, the normalized harmonic is:
$$H_\rho(x) = x^{w_\rho} = e^{w_\rho \log x}, \qquad |H_\rho(x)| = x^\delta.$$
Under analytic reciprocal scaling $w_{\rho, K} = \tau^K w_\rho$ and $x_K = x^{\tau^{-K}}$:
$$H_{\rho, K}(x_K) = e^{(\tau^K w_\rho)(\tau^{-K}\log x)} = e^{w_\rho \log x} = H_\rho(x).$$
Both phase $\gamma \log x$ and radial modulus $x^\delta$ are **strictly invariant**.

### K. Does the arithmetic realization introduce the factor $\tau^{K(\rho - 1/2)}$?
**YES**. Under the horizontal arithmetic realization $x \mapsto \tau^K x$:
$$H_\rho\left(\tau^K x\right) = e^{w_\rho(\log x + K\log\tau)} = \tau^{K w_\rho} e^{w_\rho \log x} = \tau^{K(\rho - 1/2)} H_\rho(x).$$
The modulus transforms by:
$$\left|H_\rho\left(\tau^K x\right)\right| = \tau^{K\delta} |H_\rho(x)|.$$

### L. Does the comparison recover $B_\rho(K)$?
**YES**. Reflecting grades $K \mapsto -K$ and taking the bilateral sum:
$$\frac{\left|H_\rho\left(\tau^K x\right)\right|}{|H_\rho(x)|} + \frac{\left|H_\rho\left(\tau^{-K} x\right)\right|}{|H_\rho(x)|} - 2 = \tau^{K\delta} + \tau^{-K\delta} - 2 = 4\sinh^2\left(\frac{K\delta\log\tau}{2}\right) = B_\rho(K).$$
The canonical TC non-unitarity defect is thus derived directly from the contrast between converter-invariant analytic scaling and arithmetic linear grade realization.

### M. Is equality of the two representations actually required?
**NO**. Equality $H_\rho(A_K(p)) = H_\rho(G_K(p))$ is not required by any arithmetic or analytic axiom. If it were required for all primes $p$, we would have:
$$p^{\tau^{-K}(\rho - 1/2)} = \tau^{K(\rho - 1/2)} p^{\rho - 1/2} \implies \left(\tau^{-K} - 1\right)\log p = K\log\tau.$$
Because the RHS is independent of $p$, this would force $\log p_1 = \log p_2$ for any two primes, which is a **blatant contradiction**.

### N. Is there an intrinsic prime-referent quantity that forces equality?
**NO**. The intrinsic invariants of a prime referent (its combinatorial index $\pi(p) \in \mathbb{N}$, its step height $\Delta \pi = 1$, its Möbius weight $\mu(n)/n$, and its prime label $p$) are discrete topological/combinatorial properties. None of them constrain the metric location of $p$ in physical coordinates to satisfy a translation invariance that conflicts with logarithmic dilation.

### O. What is now the earliest missing bridge?
The earliest remaining missing bridge is:
$$\boxed{
\begin{gathered}
\textbf{Construct an authentic arithmetic functional or boundary condition that directly forces}\\
\textbf{the physical prime stations to obey the translation group action without breaking}\\
\textbf{the conformal scaling symmetry of the explicit formula.}
\end{gathered}
}$$

---

## 3. Formalization & Test Verification Summary

### Lean 4 Formal Verification
Module: [`formal/RiemannScope/RiemannConverter.lean`](file:///C:/Development/Projects/reimann_scope/formal/RiemannScope/RiemannConverter.lean)  
Imported in: [`formal/RiemannScope.lean`](file:///C:/Development/Projects/reimann_scope/formal/RiemannScope.lean)  
Inventory: Included in `certification.py` and `scripts/build_formal.py`.  
Status: `lake build` compiled **333 total project theorem declarations** with **0 errors, 0 sorries**.
Formalized theorems:
1. `converter_endpoint_scaling`: $((c : \mathbb{C}) \cdot s) \cdot ((\log x : \mathbb{C}) / c) = s \cdot \log x$.
2. `converter_contour_height_scaling`: $(c \cdot t) \cdot (\log x / c) = t \cdot \log x$.
3. `analytic_log_station`: $\tau^{-K}\log p$.
4. `arithmetic_log_station`: $\log p + \text{shift}$.
5. `dilation_translation_coincidence_iff`: Coincidence condition on a single prime.
6. `dilation_translation_multi_prime_rigidity`: Rigorous proof that dilation and translation cannot coincide on two distinct primes ($p_1 \ne p_2$).
7. `centered_harmonic_analytic_invariance`: Exact invariance of $(c \cdot w) \cdot (\log x / c) = w \cdot \log x$.
8. `centered_harmonic_arithmetic_shift`: $w \cdot (\log x + \text{shift}) = w \cdot \log x + w \cdot \text{shift}$.
9. `centered_harmonic_real_shift`: Real part is $\delta \cdot \text{shift}$.
10. `radial_defect_form`: $y + y^{-1} - 2 = (y - 1)^2 / y$.

### Dedicated Pytest Suite
Test module: [`tests/test_tc_riemann_converter_grade_compatibility.py`](file:///C:/Development/Projects/reimann_scope/tests/test_tc_riemann_converter_grade_compatibility.py)  
Execution: **15/15 passed in 0.24s**.
- Tested finite-sum converter endpoint covariance to $10^{-30}$.
- Tested arbitrary positive scale covariance ($c = 0.35, 2.0, \pi, 7.5$) to $10^{-25}$.
- Tested TC $c = \tau^K$ covariance for $K \in \{-2, -1, 1, 2\}$ to $10^{-25}$.
- Verified analytic log-dilation and arithmetic log-translation.
- Verified analytic staircase jump transformations on primes up to 100.
- Verified centered harmonic invariance and arithmetic multiplier $\tau^{K\delta}$.
- Verified bilateral recovery of canonical $B_\rho(K)$.
- Enforced regression preventing claims of transcendence for $p^{\tau^{-K}}$.
- Enforced regression preventing identification of $A_K(p)$ and $G_K(p)$.

---

## 4. Methodological Epistemics & Legacy Boundary Check

- **Immutable Baseline**: Immutable git baseline commit `82643cafd605492233c6c1e992b78c2c30d45f13` in `.agents/corpus_map/legacy_claim_manifest.json` remains **untouched**.
- **No Overclaiming**: The scale covariance of the Riemann converter is recognized as a generic coordinate property (`GENERIC_CONVERTER_SCALE_COVARIANCE`), not an RH mechanism.
- **Firewall Intact**: No positivity, frame, or Suzuki machinery has been imported into this purely explicit-formula analysis.
- **Arithmetic Status**: $p^{\tau^{-K}}$ is classified as `OPEN_TRANSCENDENCE_STATUS`.
