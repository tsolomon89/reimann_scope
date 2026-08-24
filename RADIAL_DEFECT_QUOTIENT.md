# Radial-Defect Quotient, Limiting Invariant \(L_Q\), and Relative Fredholm Theory

Canonical specification for the Radial-Defect Quotient \(Q(z)\), the limiting invariant \(L_Q\), the relative Fredholm determinant formulation, the scoped Projection Trap classification, and the reflection-paired kernel \(\kappa_1\).

---

## 1. Centered Coordinates and Reference Functions

Let the centered complex coordinate be

\[
\boxed{
z = s - \frac12 = \delta + it,
\qquad
s = \frac12 + z.
}
\]

Define the centered completed Riemann zeta function:

\[
\boxed{
\Xi(z) = \xi\left(\frac12 + z\right),
}
\]

where \(\xi(s) = \frac12 s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)\) is the classical Riemann completed xi function.

The nontrivial zeros of \(\zeta(s)\) correspond to the centered zeros of \(\Xi(z)\):

\[
\rho = \frac12 + \lambda,
\qquad
\lambda = \delta + i\gamma.
\]

Let \(\Lambda^+\) be the multiset of centered nontrivial zeros in the upper half-plane (\(\gamma > 0\)), counted with multiplicity.

For each distinct height \(\gamma > 0\), define \(m_\gamma\) as the total multiplicity of **all** upper-half-plane zeros at height \(\gamma\) (including hypothetical off-line zeros \(\delta \ne 0\)).

Define the critical-line baseline reference function:

\[
\boxed{
\Xi^\flat(z) = \prod_{\gamma > 0} \left(1 + \frac{z^2}{\gamma^2}\right)^{m_\gamma}.
}
\]

---

## 2. The Radial-Defect Quotient \(Q(z)\)

The Radial-Defect Quotient is defined as the normalized ratio of the actual completed function to the critical-line baseline reference:

\[
\boxed{
Q(z) = \frac{\Xi(z)}{\Xi(0) \Xi^\flat(z)}.
}
\]

By Hadamard's factorization theorem of genus 1, since \(\Xi(z)\) is an entire function of order 1 and even in \(z\) (\(\Xi(-z) = \Xi(z)\)), the zeros of \(\Xi(z)\) occur in symmetric quartets \(\pm\delta \pm i\gamma\) (for \(\delta \ne 0\)) or pairs \(\pm i\gamma\) (for \(\delta = 0\)).

For a critical-line pair (\(\delta = 0\)), the factor in \(\Xi(z)/\Xi(0)\) is \(1 + z^2/\gamma^2\), which cancels identically with the corresponding factor in \(\Xi^\flat(z)\).

For a hypothetical off-line quartet \(\{\pm\delta \pm i\gamma\}\) with multiplicity \(n_\gamma\) (such that \(m_\gamma = 2n_\gamma\)), the four zeros contribute to \(\Xi(z)/\Xi(0)\) the normalized factor:

\[
\left(1 - \frac{z}{\delta + i\gamma}\right)\left(1 - \frac{z}{-\delta + i\gamma}\right)\left(1 - \frac{z}{\delta - i\gamma}\right)\left(1 - \frac{z}{-\delta - i\gamma}\right)
=
\frac{(z^2 - (\delta+i\gamma)^2)(z^2 - (\delta-i\gamma)^2)}{(\delta^2+\gamma^2)^2}.
\]

Dividing by the corresponding baseline factor in \(\Xi^\flat(z)\), namely \((1 + z^2/\gamma^2)^2 = \frac{(z^2+\gamma^2)^2}{\gamma^4}\), yields the quartet quotient factor:

\[
\boxed{
Q_{\delta,\gamma}(z) = \frac{\gamma^4 \left[ (z^2 - \delta^2 + \gamma^2)^2 + 4\delta^2\gamma^2 \right]}{(\gamma^2+\delta^2)^2 (z^2+\gamma^2)^2}.
}
\]

---

## 3. Real-Axis Factor \(q_{\delta,\gamma}(x)\) and Audited Properties

Evaluating along the real centered axis \(z = x \in \mathbb R\) (corresponding to \(\Re(s) = 1/2 + x, \Im(s) = 0\)):

\[
\boxed{
q_{\delta,\gamma}(x) = \frac{\gamma^4 \left[ (x^2 + \gamma^2 - \delta^2)^2 + 4\delta^2\gamma^2 \right]}{(\gamma^2+\delta^2)^2 (x^2+\gamma^2)^2}.
}
\]

### Property 1: Boundedness and Positivity
\[
\boxed{
0 < q_{\delta,\gamma}(x) \le 1 \quad \forall x \in \mathbb R.
}
\]
Equality \(q_{\delta,\gamma}(x) = 1\) holds if and only if \(x = 0\) (when \(\delta \ne 0\)). If \(\delta = 0\), \(q_{0,\gamma}(x) \equiv 1\).

*Proof*:
Subtracting \(q_{\delta,\gamma}(x)\) from 1:
\[
1 - q_{\delta,\gamma}(x) = \frac{x^2 \delta^2 \gamma^4 \left[ 2(\gamma^2+\delta^2)x^2 + 2(\gamma^2+\delta^2)^2 + 4\gamma^2(\gamma^2-\delta^2) \right]}{(\gamma^2+\delta^2)^2 (x^2+\gamma^2)^2} \ge 0.
\]
Because \(\delta^2 < 1/4 < \gamma_1^2 \approx 199.8\), the numerator is strictly positive for all \(x \ne 0\).

### Property 2: Unique Extremum
The unique minimum of \(q_{\delta,\gamma}(x)\) occurs at:
\[
\boxed{
x_*^2 = \delta^2 + 3\gamma^2.
}
\]

### Property 3: Exact Minimum Value
Writing the scale-invariant ratio \(r = \frac{\delta^2}{\gamma^2}\):
\[
\boxed{
q_{\min} = q_{\delta,\gamma}(x_*) = \frac{4}{(1+r)^2(4+r)}.
}
\]

### Property 4: Exact Uniform Domination Estimate
\[
\boxed{
\sup_{x\in\mathbb R} |\log q_{\delta,\gamma}(x)| = 2\log(1+r) + \log\left(1 + \frac{r}{4}\right) \le \frac{9}{4}r.
}
\]
*Significance*: Because \(\sum_{\gamma} \frac{\delta^2}{\gamma^2} < \infty\), the bound \(\frac{9}{4}\frac{\delta^2}{\gamma^2}\) provides the uniform domination necessary for absolute and uniform convergence and limit/product interchange.

---

## 4. The Limiting Invariant \(L_Q\) and Spectral Equivalence

Taking the asymptotic limit as \(x \to \infty\) along the real centered axis:

\[
\lim_{x\to\infty} q_{\delta,\gamma}(x) = \frac{\gamma^4}{(\gamma^2+\delta^2)^2} = \left(\frac{\gamma^2}{\gamma^2+\delta^2}\right)^2 = (1+r)^{-2}.
\]

Therefore, the limiting invariant is:

\[
\boxed{
L_Q = \lim_{x\to\infty} Q(x) = \prod_{\text{off-line quartets}} \left(\frac{\gamma^2}{\gamma^2+\delta^2}\right)^{2n_\gamma}.
}
\]

### Spectral Equivalence
\[
\boxed{
0 < L_Q \le 1,
\qquad
L_Q = 1 \iff \mathrm{RH}.
}
\]

> [!IMPORTANT]
> \(L_Q = 1 \iff \mathrm{RH}\) is an exact **spectral equivalence**. It is not an arithmetic proof of RH, because evaluating \(L_Q\) directly from \(Q(x)\) requires knowledge of the zero divisor.

---

## 5. Exact Relationship to EF-013 and Audited Withdrawal

Define the single-zero radial defect:

\[
\boxed{
d(\delta,\gamma) = \log\left(1 + \frac{\delta^2}{\gamma^2}\right).
}
\]

For the test function \(H(z) = \log z\), the projection-subtracted quartet response is:

\[
2\Re\log(\delta+i\gamma) - 2\Re\log(i\gamma) = \log(\delta^2+\gamma^2) - \log(\gamma^2) = \log\left(1 + \frac{\delta^2}{\gamma^2}\right) = d(\delta,\gamma).
\]

Thus, the \(L_Q\) defect already lies inside the projection-subtracted EF-013 construction:

\[
-\log L_Q = 2 \sum_{\text{quartets}} d(\delta,\gamma).
\]

### Reasons for Bridge Failure
The failure of EF-013 to provide an arithmetic proof of RH stems from three distinct causes:
1. **Test-Class Inadmissibility**: \(H(z) = \log z\) is outside the admissible Riemann–Weil test class due to its logarithmic branch point at \(z=0\), growth at infinity, and test-domain restrictions.
2. **The Projected-Divisor Problem**: The subtraction \(2\Re\log(i\gamma)\) is evaluated on the projected divisor \(\mathcal P_0(\mathcal D_\zeta)\), which has no established independent arithmetic representation.
3. **Finite Non-Compensation**: Finite basis non-compensation (EF-016) was not established across the full zero spectrum.

### Audited Withdrawal
> [!NOTE]
> The historical conjecture that EF-013 had the "wrong \(\gamma\)-curvature" was audited and found to be incorrect: \(H(z)=\log z\) yields exactly the curvature \(d(\delta,\gamma)\). The claim of wrong \(\gamma\)-curvature is **withdrawn** and preserved in the ledger with its mathematical justification.

---

## 6. Scoped Classification of the Projection Trap (EF-018 / OBL-EF-003)

The Projection Trap is formally classified with precise method-class boundaries:

\[
\boxed{
\begin{aligned}
\textbf{CLOSED:}&\ \text{For fixed linear combinations of direct one-point holomorphic} \\
&\ \text{Riemann–Weil statistics over an open displacement family.} \\
\textbf{OPEN:}&\ \text{For nonlinear paired, determinantal, operator, or independently} \\
&\ \text{constructed comparison objects.}
\end{aligned}
}
\]

- The no-go result proves that no linear 1-point test function can independently evaluate the projected divisor \(\mathcal P_0(\mathcal D_\zeta)\) from arithmetic data alone.
- It does **not** prove that nonlinear paired or determinantal constructions are impossible.

---

## 7. Relative Fredholm Formulation

Define the positive diagonal trace-class spectral operator \(\mathcal R\) on the Hilbert space \(\ell^2(\Lambda^+)\) of upper-half-plane zeros:

\[
\boxed{
\mathcal R e_\lambda = \frac{\delta_\lambda^2}{\gamma_\lambda^2} e_\lambda,
\qquad
\lambda = \delta_\lambda + i\gamma_\lambda \in \Lambda^+.
}
\]

(For critical-line zeros \(\delta_\lambda = 0\), the diagonal entry is 0).

### Properties:
1. **Positivity**: \(\mathcal R \ge 0\).
2. **Trace Class**: Because \(\sum_\lambda \frac{1}{\gamma_\lambda^2} < \infty\) and \(|\delta_\lambda| < 1/2\):
   \[
   \operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \frac{\delta_\lambda^2}{\gamma_\lambda^2} < \infty.
   \]
3. **Fredholm Determinant**:
   \[
   \boxed{
   \det_{\mathrm F}(I + \mathcal R) = \prod_{\lambda\in\Lambda^+} \left(1 + \frac{\delta_\lambda^2}{\gamma_\lambda^2}\right) = L_Q^{-1}.
   }
   \]
4. **Logarithmic Determinant**:
   \[
   \boxed{
   -\log L_Q = \operatorname{Tr}\log(I + \mathcal R) = \log\det_{\mathrm F}(I + \mathcal R).
   }
   \]
5. **RH Equivalence**:
   \[
   \boxed{
   \operatorname{Tr}\mathcal R = 0 \iff \mathcal R = 0 \iff \mathrm{RH},
   \qquad
   \det_{\mathrm F}(I + \mathcal R) = 1 \iff \mathrm{RH}.
   }
   \]

> [!CAUTION]
> Do not decompose \(\log\det_{\mathrm F}(I+\mathcal R)\) into divergent raw sums such as \(\sum \log|z| - \sum \log|\Im z|\). The relative determinant is the canonical, unconditionally convergent object.

---

## 8. Target Hierarchy

The target representations for an arithmetic bridge are structured hierarchically:

```mermaid
graph TD
    Op["Operator Target: Arithmetic operator isospectral to R"] --> DetFam["Determinant Family: D_zeta(t) = det_F(I + t R)"]
    DetFam --> ScalDet["Scalar Determinant Target: D_zeta(1) = L_Q^(-1)"]
    DetFam --> MinScal["Minimal Scalar Target: Tr(R) = sum (delta^2 / gamma^2)"]
    MinScal -. "Logically Equivalent to RH" .-> ScalDet
```

1. **Minimal Scalar Target**: \(\operatorname{Tr}\mathcal R = \sum \frac{\delta^2}{\gamma^2}\). Vanishing is already RH-equivalent. Structurally simpler than the determinant, but logically equivalent.
2. **Scalar Determinant Target**: \(D_\zeta(1) = \det_{\mathrm F}(I+\mathcal R) = L_Q^{-1}\).
3. **Full Determinant Family**: \(D_\zeta(t) = \det_{\mathrm F}(I + t\mathcal R) = \exp\left(\sum_{k\ge 1} \frac{(-1)^{k+1}}{k} t^k \operatorname{Tr}\mathcal R^k\right)\). Near \(t=0\), generates all trace moments \(\operatorname{Tr}\mathcal R^k\).
4. **Operator Target**: An arithmetic operator sharing the non-zero spectrum of \(\mathcal R\) with multiplicity (literal equality of operators is unnecessary; isospectral realization suffices).

---

## 9. Immediate Live Research Kernel: Reflection-Paired \(\kappa_1\)

For centered coordinates \(z = \delta + i\gamma\), define the involution:

\[
\boxed{
z^\# = -\bar z = -\delta + i\gamma.
}
\]

Define the rational pairing kernel:

\[
\boxed{
\kappa_1(z,w) = \frac{4zw}{(z+w)^2} - 1.
}
\]

### Exact Involution Identity
Evaluating \(\kappa_1\) on the pair \((z, z^\#)\):

\[
z + z^\# = 2i\gamma,
\qquad
z z^\# = -(\delta^2 - \gamma^2 + 2i\delta\gamma)^\# \dots = -(\delta+i\gamma)(\delta-i\gamma) = -(\delta^2+\gamma^2).
\]
\[
\kappa_1(z, z^\#) = \frac{4(-(\delta^2+\gamma^2))}{(2i\gamma)^2} - 1 = \frac{-4(\delta^2+\gamma^2)}{-4\gamma^2} - 1 = \frac{\delta^2+\gamma^2}{\gamma^2} - 1 = \frac{\delta^2}{\gamma^2}.
\]

\[
\boxed{
\kappa_1(\lambda, \lambda^\#) = \frac{\delta^2}{\gamma^2}.
}
\]

Therefore, the relative trace is:

\[
\boxed{
\operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \kappa_1(\lambda, \lambda^\#).
}
\]

### The Open Research Theorem
\[
\boxed{
\text{Can a divisor-independent arithmetic construction isolate the } (\lambda, \lambda^\#) \text{ pairs and evaluate } \kappa_1?
}
\]

- The functional equation \(\xi(s) = \xi(1-s) \iff \Xi(z) = \Xi(-z)\) supplies closure under the involution \(z \mapsto -z\).
- The Schwarz reflection \(\overline{\Xi(z)} = \Xi(\bar z)\) supplies closure under \(z \mapsto \bar z\).
- Together they supply closure under \(z \mapsto z^\# = -\bar z\).
- **The unresolved problem**: Isolating the correct pairs \((\lambda, \lambda^\#)\) without reading the divisor directly.

---

## 10. Transcendental Continuation and Grade Invariance

1. **Radial Class Preservation**: Transcendental continuation \(\mathcal X_\tau(s,k) = \xi(\tau^{-k}s)\) transports zero worldlines \(s_\rho(k) = \tau^k\rho\) while preserving normalized radial coordinate \(R_\tau \equiv \delta\).
2. **Grade Invariance of \(Q\), \(L_Q\), and \(\mathcal R\)**:
   - Under uniform dilation \((x, \delta, \gamma) \mapsto (\tau^K x, \tau^K \delta, \tau^K \gamma)\), the dimensionless ratios \(x/\gamma\) and \(\delta/\gamma\) are strictly invariant.
   - Consequently, \(q_{\delta,\gamma}(x)\), \(Q(z)\), \(L_Q\), and the spectral operator \(\mathcal R\) are **grade-invariant**.
3. **Rigidity Requirement**: Ordinary coordinate grade dilation does not supply the rigidity law. The rigidity source must contain additional zeta-specific arithmetic content (the Euler product / prime structure).
