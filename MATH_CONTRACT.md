# Mathematical Contract

This file is the compact implementation-level mathematical contract for the Riemann Microscope / Macroscope.

The purpose is to prevent different modules from silently using different meanings for the same transformation. All identities below should have direct unit tests.

## 1. Constants and coordinates

\[
\tau=2\pi.
\]

Raw coordinate:

\[
s=\sigma+it.
\]

Centered coordinate:

\[
z=s-\frac12=\delta+it.
\]

Therefore

\[
s=\frac12+z,
\qquad
\delta=\Re(s)-\frac12.
\]

At baseline, the critical line is

\[
\Re(s)=\frac12.
\]

## 2. Camera transform

Camera zoom and pan do not alter mathematical coordinates:

\[
T_{\mathrm{camera}}(s)=s.
\]

## 3. Height microscope / macroscope

\[
s_K(u)=\frac12+\delta+i(t_0+\tau^K u).
\]

This changes the sampled ordinate range only. The vertical sampling line remains

\[
\Re(s)=\frac12+\delta.
\]

## 4. Origin coordinate dilation

Define

\[
s'=\tau^K s.
\]

For the same zeta object expressed in the new coordinate:

\[
f_K(s')=\zeta\!\left(\frac{s'}{\tau^K}\right).
\]

If \(\zeta(\rho)=0\), then

\[
f_K(\tau^K\rho)=0.
\]

Hence

\[
\boxed{\rho'=\tau^K\rho}.
\]

The image of the ordinary critical line is

\[
\boxed{\Re(s')=\frac{\tau^K}{2}}.
\]

This does **not** assert

\[
\zeta(\tau^K s)=\zeta(s).
\]

## 5. Centered coordinate dilation

Define

\[
s'=\frac12+\tau^K\left(s-\frac12\right),
\qquad
z'=\tau^K z.
\]

For the same object in the new centered coordinate:

\[
f_K(s')=\zeta\!\left(\frac12+\frac{s'-\frac12}{\tau^K}\right).
\]

The exact zero map is

\[
\boxed{\rho'=\frac12+\tau^K\left(\rho-\frac12\right)}.
\]

The critical line is fixed geometrically:

\[
\boxed{\Re(s')=\frac12}.
\]

## 6. Argument transform

Define

\[
f_K(s)=\zeta(\tau^K s).
\]

Then

\[
f_K(s)=0\iff \tau^K s=\rho,
\]

so

\[
\boxed{s=\rho/\tau^K}.
\]

Critical-line zeros map to

\[
\boxed{\Re(s)=\frac{1}{2\tau^K}}.
\]

## 7. Kernel transformation

Start from

\[
n^{-s}=e^{-s\log n}.
\]

Transform

\[
\log n\mapsto A\log n+C
\]

and

\[
s\mapsto Bs+D.
\]

Then

\[
\left(e^C n^A\right)^{-(Bs+D)}
=
e^{-C(Bs+D)}n^{-A(Bs+D)}.
\]

Therefore, where the Dirichlet series converges,

\[
\mathcal Z_{A,C,B,D}(s)
=
e^{-C(Bs+D)}\zeta(A(Bs+D)).
\]

The analytically continued right-hand side is the canonical implementation elsewhere.

The exponential prefactor does not create zeros, so for \(AB\neq0\):

\[
A(Bs+D)=\rho
\]

gives

\[
\boxed{s_\rho=\frac{\rho/A-D}{B}}.
\]

## 8. Inverse Scale Lock

When enabled:

\[
\boxed{AB=1}.
\]

Then

\[
(Bs)(A\log n)=s\log n.
\]

For \(C=D=0\):

\[
\mathcal Z_{A,0,1/A,0}(s)=\zeta(s).
\]

This is an exact identity.

## 9. Centered kernel mode

Let

\[
s=\frac12+z.
\]

Define

\[
\boxed{\mathcal Z^{\mathrm{ctr}}_{A,B}(z)=\zeta\left(\frac12+ABz\right)}.
\]

When \(AB=1\):

\[
\mathcal Z^{\mathrm{ctr}}_{A,1/A}(z)=\zeta\left(\frac12+z\right).
\]

## 10. Anisotropic centered deformation

For exploratory visualization only:

\[
z=\delta+i\gamma\mapsto A_\delta\delta+iA_\gamma\gamma.
\]

If \(A_\delta\neq A_\gamma\), label it `NON-HOLOMORPHIC DEFORMATION`.

## 11. Zero character

For

\[
\rho=\frac12+\delta+i\gamma,
\]

define

\[
\boxed{q_\rho=\tau^{\rho-\frac12}}.
\]

Hence

\[
q_\rho=\tau^\delta e^{i\gamma\log\tau}
\]

and

\[
\boxed{|q_\rho|=\tau^\delta}.
\]

Under real grade \(K\):

\[
\boxed{q_\rho^K=\tau^{K\delta}e^{iK\gamma\log\tau}},
\]

so

\[
\boxed{|q_\rho^K|=\tau^{K\delta}},
\]

\[
\boxed{\log|q_\rho^K|=K\delta\log\tau},
\]

and

\[
\boxed{\frac{d}{dK}\log|q_\rho^K|=\delta\log\tau}.
\]

For \(\delta=0\):

\[
|q_\rho^K|=1
\]

for all \(K\).

## 12. Converter formulas

For positive-imaginary nontrivial zeros included through a declared cutoff:

\[
J_N(x)
=
\operatorname{Li}(x)
-
2\Re\sum_\rho \operatorname{Li}(x^\rho)
-
\log 2
+
\int_x^\infty\frac{du}{u(u^2-1)\log u}.
\]

Then

\[
\pi_N(x)
=
\sum_{m\ge1}\frac{\mu(m)}{m}J_N(x^{1/m}),
\]

stopping once

\[
x^{1/m}<2.
\]

Use one documented branch convention consistently for complex logarithms and \(\operatorname{Li}(x^\rho)\).

### 12.1 Exact Coupled Converter Covariance

Define the signed single-zero contribution of a conjugate pair \(\rho, \bar{\rho}\) to \(J(x)\) as:

\[
C_J(x, \rho) = -2\Re\left[\operatorname{Ei}(\rho\log x)\right].
\]

Let \(A = \tau^k\), and transform simultaneously:

\[
\rho' = A\rho,
\qquad
\log x' = \frac{\log x}{A} \iff x' = x^{1/A}.
\]

Then

\[
\rho'\log x' = (A\rho)\left(\frac{\log x}{A}\right) = \rho\log x.
\]

Therefore

\[
\operatorname{Ei}(\rho'\log x') = \operatorname{Ei}(\rho\log x).
\]

Hence the signed single-zero \(J\) contribution obeys the exact covariance:

\[
\boxed{C_J(x^{1/A}, A\rho) = C_J(x, \rho)}.
\]

Because the same cancellation occurs after replacing \(x\) by \(x^{1/m}\):

\[
(A\rho)\log\left((x^{1/A})^{1/m}\right) = (A\rho)\frac{\log x}{mA} = \rho\frac{\log x}{m},
\]

the Möbius-inverted single-zero contribution \(C_\pi(x, \rho) = \sum_{m\ge1}\frac{\mu(m)}{m}C_J(x^{1/m}, \rho)\) also obeys the corresponding coupled covariance:

\[
\boxed{C_\pi(x^{1/A}, A\rho) = C_\pi(x, \rho)},
\]

subject to matching truncation and domain semantics.

*Note:* This is an exact covariance under the explicitly coupled change of coordinates, **not** a non-trivial automorphism of \(\zeta(s)\).


## 13. Deterministic test vectors

### A — Identity

\[
K=0.
\]

All scale factors equal 1.

### B — Origin dilation

\[
K=1.
\]

Expected image critical line:

\[
\Re(s')=\tau/2=\pi.
\]

Expected zero map:

\[
\rho'=\tau\rho.
\]

### C — Centered dilation

\[
K=1.
\]

Expected image critical line:

\[
\Re(s')=1/2.
\]

Expected zero map:

\[
\rho'=1/2+\tau(\rho-1/2).
\]

### D — Inverse kernel lock

\[
A=2,
\qquad
B=1/2,
\qquad
C=D=0.
\]

Expected:

\[
AB=1
\]

and

\[
\mathcal Z_{2,0,1/2,0}(s)=\zeta(s).
\]

### E — Radial centrifuge

Take

\[
\delta=10^{-4},
\qquad
K=100.
\]

Expected:

\[
\log|q_\rho^K|=0.01\log\tau.
\]

### F — On-line centrifuge

For \(\delta=0\) and arbitrary tested \(K\):

\[
|q_\rho^K|=1.
\]

## 14. Forbidden shortcuts

Do not:

- evaluate \(\sum n^{-s}\) in the critical strip as if it were the analytic continuation;
- use reference zeros as discovery seeds in baseline validation;
- infer same-object status from visual similarity;
- treat coordinate dilation and argument transformation as interchangeable;
- convert high-precision decimal inputs through binary float before evaluation;
- silently change branch conventions between modules.
