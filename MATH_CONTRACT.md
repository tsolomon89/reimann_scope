# Mathematical Contract

This is the authoritative implementation-level mathematical contract for `reimann_scope`.

Its purpose is to prevent the UI, numerical engine, batch runner, and formal layer from silently using different meanings for the same transformation or research object.

Every identity marked **EXACT** should have a direct unit or formal regression test where practical.

---

# 1. Constants and coordinates

Use

\[
\boxed{\tau=2\pi.}
\]

Ordinary complex coordinate:

\[
\boxed{s=\sigma+it.}
\]

Centered coordinate:

\[
\boxed{
z=s-\frac12=\delta+it.
}
\]

Therefore

\[
s=\frac12+z
\]

and

\[
\boxed{
\delta=\Re(s)-\frac12.
}
\]

The ordinary critical line is

\[
\boxed{
\Re(s)=\frac12.
}
\]

---

# 2. Grade notation

The repository distinguishes three grade types.

## 2.1 Continuous grade

\[
\boxed{k\in\mathbb R.}
\]

Define

\[
\boxed{
a(k)=\tau^k.
}
\]

Then

\[
a(k)>0,
\]

\[
a(k_1+k_2)=a(k_1)a(k_2),
\]

\[
a(-k)=a(k)^{-1},
\]

and

\[
a(0)=1.
\]

Since \(k\mapsto\tau^k\) is a bijection,

\[
\boxed{
\tau^\mathbb R=\mathbb R_{>0}.
}
\]

## 2.2 Canonical integer grade

\[
\boxed{K\in\mathbb Z.}
\]

Define

\[
\boxed{
A_K=\tau^K.
}
\]

The canonical bilateral sequence is

\[
\ldots,\tau^{-2},\tau^{-1},1,\tau,\tau^2,\ldots
\]

with

\[
A_{-K}=A_K^{-1}.
\]

## 2.3 Rational/root grade

For

\[
q\in\mathbb Q,
\]

define

\[
\boxed{
A_q=\tau^q.
}
\]

Rational grades contain exact root refinements of the integer-grade family.

Do not use one variable interchangeably for continuous \(k\), integer \(K\), and rational \(q\).

---

# 3. Transcendental continuation

The project-defined transcendental-continuation family uses origin-dilation semantics.

Define

\[
\boxed{
\mathcal Z_\tau(s,k)
=
\zeta(\tau^{-k}s).
}
\]

This is an exact family built from the analytically continued zeta function.

At native grade,

\[
\boxed{
\mathcal Z_\tau(s,0)=\zeta(s).
}
\]

For any \(u\in\mathbb C\),

\[
\boxed{
\mathcal Z_\tau(\tau^k u,k)=\zeta(u).
}
\]

This is **EXACT COORDINATE COVARIANCE**.

It is not an RH result.

---

# 4. Completed transcendental continuation

Define

\[
\boxed{
\xi(s)
=
\frac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s).
}
\]

For proof-facing nontrivial-zero work, define

\[
\boxed{
\mathcal X_\tau(s,k)
=
\xi(\tau^{-k}s).
}
\]

Then

\[
\boxed{
\mathcal X_\tau(s,0)=\xi(s).
}
\]

The zeros of \(\xi\) are the nontrivial zeros of \(\zeta\).

---

# 5. Zero worldlines

Let

\[
\zeta(\rho)=0.
\]

Then

\[
\mathcal Z_\tau(s,k)=0
\]

iff

\[
\tau^{-k}s=\rho.
\]

Hence the exact zero map is

\[
\boxed{
s_\rho(k)=\tau^k\rho.
}
\]

At integer grade,

\[
\boxed{
s_{\rho,K}=\tau^K\rho.
}
\]

Define the continuous zero worldline

\[
\boxed{
W_\rho
=
\{(\tau^k\rho,k):k\in\mathbb R\}.
}
\]

For proof-facing nontrivial zeros, the same map holds for \(\mathcal X_\tau\).

---

# 6. Critical surface

The ordinary critical line is

\[
\Re(s)=\frac12.
\]

Under grade \(k\), its image is

\[
\boxed{
\Re(s)=\frac{\tau^k}{2}.
}
\]

Define

\[
\boxed{
\mathcal C_\tau
=
\left\{
(s,k):
\Re(s)=\frac{\tau^k}{2}
\right\}.
}
\]

A critical-line zero worldline lies entirely on \(\mathcal C_\tau\).

---

# 7. Transcendental radial coordinate

Define

\[
\boxed{
R_\tau(s,k)
=
\tau^{-k}\Re(s)-\frac12.
}
\]

Let

\[
\rho=\frac12+\delta+i\gamma.
\]

Along its worldline,

\[
s_\rho(k)
=
\tau^k
\left(
\frac12+\delta+i\gamma
\right).
\]

Then

\[
\boxed{
R_\tau(s_\rho(k),k)=\delta.
}
\]

This is an **EXACT WORLDLINE INVARIANT**.

It is a coordinate identity.

It does not prove that only \(\delta=0\) occurs.

---

# 8. Radial leaves

For each

\[
\delta\in\mathbb R,
\]

define

\[
\boxed{
\mathcal R_\delta
=
\{(s,k):R_\tau(s,k)=\delta\}.
}
\]

The critical surface is

\[
\boxed{
\mathcal R_0=\mathcal C_\tau.
}
\]

A native zero

\[
\rho=\frac12+\delta+i\gamma
\]

generates a worldline entirely contained in \(\mathcal R_\delta\).

RH is equivalent to:

\[
\boxed{
\text{all nontrivial zero worldlines occupy }\mathcal R_0.
}
\]

---

# 9. Arithmetic grade lattices

For integer grade,

\[
\boxed{
L_K=\tau^K\mathbb Z.
}
\]

Each is countably infinite and scale-isomorphic to \(\mathbb Z\).

For distinct integers \(J\neq K\),

\[
\boxed{
L_J\cap L_K=\{0\}.
}
\]

Reason:

A nonzero common point would imply

\[
\tau^{K-J}\in\mathbb Q,
\]

contradicting transcendence of \(\tau\).

For distinct rational grades \(r\neq q\),

\[
\boxed{
\tau^r\mathbb Z
\cap
\tau^q\mathbb Z
=
\{0\}.
}
\]

Do not extend this result to arbitrary real grades.

Do not infer from arithmetic-lattice noncoincidence that zeta zero sets at distinct grades are automatically disjoint.

---

# 10. Structural versus numerical grade representation

An integer-grade point can be represented structurally by

\[
\boxed{
(K,n)
}
\]

with numerical realization

\[
n\tau^K.
\]

The structural pair is exact.

The authoritative numerical realization is finite-precision/arbitrary-precision and must carry declared precision.

The implementation must not represent \(\tau\) by a hand-entered authoritative decimal constant.

Compute it from the high-precision library.

---

# 11. Camera transform

Camera zoom and pan do not alter mathematical coordinates.

\[
\boxed{
T_{\mathrm{camera}}(s)=s.
}
\]

Classification:

```text
RENDERING ONLY
```

---

# 12. Height microscope / macroscope

For selected center \(t_0\), centered horizontal displacement \(\delta\), and continuous scale \(k\), define

\[
\boxed{
s_k(u)
=
\frac12+\delta+i(t_0+\tau^k u).
}
\]

This changes only the sampled ordinate range.

The sampling line remains

\[
\boxed{
\Re(s)=\frac12+\delta.
}
\]

Classification:

```text
SAMPLING-RANGE TRANSFORM
```

This is not the same object as transcendental continuation of the complete \(s\)-coordinate.

---

# 13. Generic origin coordinate dilation

For arbitrary positive scale

\[
A>0,
\]

define

\[
\boxed{
s'=As.
}
\]

For the same zeta object expressed in the new coordinate,

\[
\boxed{
f_A(s')=\zeta(s'/A).
}
\]

If

\[
\zeta(\rho)=0,
\]

then

\[
\boxed{
\rho'=A\rho.
}
\]

The critical line maps to

\[
\boxed{
\Re(s')=\frac A2.
}
\]

Transcendental continuation is the canonical subfamily

\[
\boxed{
A=\tau^k.
}
\]

---

# 14. Centered coordinate dilation

For

\[
A>0,
\]

define

\[
\boxed{
s'
=
\frac12+A\left(s-\frac12\right).
}
\]

Equivalently,

\[
z'=Az.
\]

The same zeta object in the transformed centered coordinate is

\[
\boxed{
f_A(s')
=
\zeta\left(
\frac12+\frac{s'-\frac12}{A}
\right).
}
\]

The exact zero map is

\[
\boxed{
\rho'
=
\frac12+A\left(\rho-\frac12\right).
}
\]

The critical line remains

\[
\boxed{
\Re(s')=\frac12.
}
\]

This is not the same operation as origin dilation.

---

# 15. Zeta argument transform

Define

\[
\boxed{
f_A(s)=\zeta(As).
}
\]

Then

\[
f_A(s)=0
\iff
As=\rho.
\]

Hence

\[
\boxed{
s=\rho/A.
}
\]

Critical-line zeros map to

\[
\boxed{
\Re(s)=\frac1{2A}.
}
\]

This changes the function being evaluated in the displayed coordinate.

Do not conflate it with origin coordinate dilation.

---

# 16. Kernel transformation

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
e^{-C(Bs+D)}
n^{-A(Bs+D)}.
\]

Where the Dirichlet series converges,

\[
\boxed{
\mathcal Z_{A,C,B,D}(s)
=
e^{-C(Bs+D)}
\zeta(A(Bs+D)).
}
\]

The analytically continued right-hand side is the canonical implementation outside the convergence half-plane.

The exponential prefactor has no zeros.

For

\[
AB\neq0,
\]

the zero map is

\[
\boxed{
s_\rho
=
\frac{\rho/A-D}{B}.
}
\]

---

# 17. Inverse Scale Lock

When enabled,

\[
\boxed{
AB=1.
}
\]

Then

\[
(Bs)(A\log n)=s\log n.
\]

For

\[
C=D=0,
\]

\[
\boxed{
\mathcal Z_{A,0,1/A,0}(s)=\zeta(s).
}
\]

This is an exact identity.

Classification:

```text
EXACT KERNEL PAIRING PRESERVED
```

---

# 18. Centered kernel mode

With

\[
s=\frac12+z,
\]

define

\[
\boxed{
\mathcal Z^{\mathrm{ctr}}_{A,B}(z)
=
\zeta\left(
\frac12+ABz
\right).
}
\]

When

\[
AB=1,
\]

\[
\boxed{
\mathcal Z^{\mathrm{ctr}}_{A,1/A}(z)
=
\zeta\left(
\frac12+z
\right).
}
\]

---

# 19. Anisotropic centered deformation

For exploratory visualization only,

\[
\boxed{
z=\delta+i\gamma
\mapsto
A_\delta\delta+iA_\gamma\gamma.
}
\]

If

\[
A_\delta\neq A_\gamma,
\]

label it:

```text
NON-HOLOMORPHIC DEFORMATION
```

Do not describe it as conformal or analytic.

---

# 20. Tau-grade zero character

For

\[
\rho=\frac12+\delta+i\gamma,
\]

define

\[
\boxed{
q_\rho
=
\tau^{\rho-\frac12}.
}
\]

Using the real logarithm of positive \(\tau\),

\[
q_\rho
=
e^{(\rho-\frac12)\log\tau}
=
\tau^\delta e^{i\gamma\log\tau}.
\]

Therefore

\[
\boxed{
|q_\rho|=\tau^\delta.
}
\]

At integer grade \(K\),

\[
\boxed{
q_\rho^K
=
\tau^{K\delta}
e^{iK\gamma\log\tau}.
}
\]

Hence

\[
\boxed{
|q_\rho^K|
=
\tau^{K\delta},
}
\]

\[
\boxed{
\log|q_\rho^K|
=
K\delta\log\tau.
}
\]

For real grade parameter \(k\), avoid generic complex-power branch ambiguity by defining the continuous grade character directly:

\[
\boxed{
Q_\rho(k)
=
\tau^{k(\rho-\frac12)}
=
e^{k(\rho-\frac12)\log\tau}.
}
\]

Hence

\[
\boxed{
Q_\rho(k)
=
\tau^{k\delta}
e^{ik\gamma\log\tau}
}
\]

and

\[
\boxed{
\frac{d}{dk}
\log|Q_\rho(k)|
=
\delta\log\tau.
}
\]

For

\[
\delta=0,
\]

\[
\boxed{
|q_\rho^K|=1
\quad
\forall K\in\mathbb Z.
}
\]

---

# 21. Symmetry-complete grade defect

Let

\[
\rho_+
=
\frac12+\delta+i\gamma,
\]

\[
\rho_-
=
\frac12-\delta+i\gamma,
\]

and baseline

\[
\rho_0
=
\frac12+i\gamma.
\]

Then

\[
q_+^K
=
\tau^{K\delta}
e^{iK\gamma\log\tau},
\]

\[
q_-^K
=
\tau^{-K\delta}
e^{iK\gamma\log\tau},
\]

\[
q_0^K
=
e^{iK\gamma\log\tau}.
\]

Define

\[
\boxed{
D_K
=
q_+^K+q_-^K-2q_0^K.
}
\]

Then

\[
\boxed{
D_K
=
2e^{iK\gamma\log\tau}
\left[
\cosh(K\delta\log\tau)-1
\right].
}
\]

Therefore

\[
\boxed{
|D_K|
=
4\sinh^2
\left(
\frac{K\delta\log\tau}{2}
\right).
}
\]

Properties:

\[
D_K=0
\quad
\text{for }\delta=0,
\]

\[
D_0=0,
\]

\[
|D_{-K}|=|D_K|,
\]

and near

\[
K\delta=0,
\]

\[
\boxed{
|D_K|
=
(K\delta\log\tau)^2
+
O((K\delta)^4).
}
\]

For fixed nonzero \(\delta\),

\[
|D_K|\to\infty
\]

as

\[
|K|\to\infty.
\]

This is an exact grade-character identity, not a proof of RH.

---

# 22. Explicit formula for \(\psi\)

For suitable \(x>1\), with the nontrivial zero sum interpreted in the standard symmetric sense,

\[
\boxed{
\psi(x)
=
x
-
\sum_\rho\frac{x^\rho}{\rho}
-
\log(2\pi)
-
\frac12\log(1-x^{-2}).
}
\]

Set

\[
x=\tau^K,
\qquad
K>0.
\]

Since

\[
x^\rho
=
\tau^{K/2}q_\rho^K,
\]

we obtain the exact spectrum-wide grade identity

\[
\boxed{
\sum_\rho
\frac{q_\rho^K}{\rho}
=
\tau^{-K/2}
\left[
\tau^K
-
\psi(\tau^K)
-
\log\tau
-
\frac12\log(1-\tau^{-2K})
\right].
}
\]

Important:

- this displayed arithmetic realization uses \(K>0\);
- do not call it bilateral without a separate derivation;
- do not impose an RH-equivalent size bound and call that an intermediate proof.

---

# 23. Riemann explicit-formula converter

For a declared set of positive-imaginary nontrivial zeros,

\[
\boxed{
J_N(x)
=
\operatorname{Li}(x)
-
2\Re
\sum_{0<\Im\rho\le T_N}
\operatorname{Li}(x^\rho)
-
\log2
+
R(x),
}
\]

where

\[
\boxed{
R(x)
=
\int_x^\infty
\frac{du}
{u(u^2-1)\log u}.
}
\]

For

\[
x>1,
\]

use the exact expansion

\[
\boxed{
R(x)
=
\sum_{m=1}^{\infty}
E_1(2m\log x)
=
-
\sum_{m=1}^{\infty}
\operatorname{Ei}(-2m\log x).
}
\]

Then recover the prime-counting approximation through Möbius inversion:

\[
\boxed{
\pi_N(x)
=
\sum_{m\ge1}
\frac{\mu(m)}{m}
J_N(x^{1/m}),
}
\]

stopping once

\[
x^{1/m}<2.
\]

The remainder term encodes the trivial-zero / archimedean correction. The nontrivial-zero sum alone is not the complete formula.

---

# 24. Branch convention for complex \(\operatorname{Li}\)

For real

\[
x>1
\]

and complex \(\rho\), use real

\[
\log x>0
\]

and define

\[
\boxed{
\operatorname{Li}(x^\rho)
=
\operatorname{Ei}(\rho\log x)
}
\]

with one documented principal branch convention for \(\operatorname{Ei}\).

Preview and Audit implementations must use compatible branch semantics.

---

# 25. Single-zero converter contribution

For an upper-half-plane zero and conjugate pair, define

\[
\boxed{
C_J(x,\rho)
=
-2\Re
\operatorname{Ei}(\rho\log x).
}
\]

For Möbius inversion,

\[
\boxed{
C_\pi(x,\rho)
=
\sum_{m\ge1}
\frac{\mu(m)}{m}
C_J(x^{1/m},\rho),
}
\]

subject to the same truncation rule as the full converter.

---

# 26. Coupled converter covariance

Let

\[
A>0.
\]

Transform

\[
\rho'=A\rho
\]

and

\[
x'=x^{1/A}.
\]

Then

\[
\rho'\log x'
=
A\rho
\frac{\log x}{A}
=
\rho\log x.
\]

Therefore

\[
\boxed{
C_J(x^{1/A},A\rho)
=
C_J(x,\rho).
}
\]

Similarly,

\[
\boxed{
C_\pi(x^{1/A},A\rho)
=
C_\pi(x,\rho)
}
\]

under matching domain and truncation semantics.

This is exact coupled coordinate covariance, not a nontrivial automorphism of zeta.

---

# 27. Symmetry-complete converter split

Let

\[
C(\beta)
\]

be a sufficiently smooth converter contribution at fixed \(x,\gamma\).

Define

\[
\boxed{
S(\delta)
=
C\left(\frac12+\delta\right)
+
C\left(\frac12-\delta\right)
-
2C\left(\frac12\right).
}
\]

Then

\[
\boxed{
S(-\delta)=S(\delta),
}
\]

\[
\boxed{
S(0)=0,
}
\]

and Taylor expansion gives

\[
\boxed{
S(\delta)
=
C''\left(\frac12\right)\delta^2
+
O(\delta^4).
}
\]

Therefore, where the quadratic coefficient is nonzero,

\[
\boxed{
\frac{S(\lambda\delta)}{S(\delta)}
\to
\lambda^2
}
\]

as

\[
\delta\to0.
\]

In particular,

\[
S(\delta)/S(\delta/2)\to4
\]

is generic quadratic-even behavior, not evidence of an exact universal hyperbolic converter law.

---

# 28. Local cross-height normalization

For a numerically verified simple critical-line zero

\[
\rho_n
=
\frac12+i\gamma_n,
\]

define the baseline asymptotic mean-spacing scale

\[
\boxed{
\Delta_n
=
\frac{\tau}
{\log(\gamma_n/\tau)}.
}
\]

Define

\[
\boxed{
s_n(u)
=
\frac12+i(\gamma_n+\Delta_nu).
}
\]

Then define derivative-normalized path

\[
\boxed{
P_n(u)
=
\frac{
\zeta(s_n(u))
}{
i\Delta_n\zeta'(\rho_n)
}.
}
\]

Since

\[
\zeta(\rho_n)=0,
\]

\[
\boxed{
P_n(0)=0.
}
\]

Differentiating in \(u\),

\[
\boxed{
P_n'(0)=1.
}
\]

This normalization is valid only for a verified simple zero with numerically well-conditioned nonzero derivative.

---

# 29. Local shape coefficients

Expand

\[
P_n(u)
=
u
+
c_{2,n}u^2
+
c_{3,n}u^3
+\cdots.
\]

Then

\[
\boxed{
c_{m,n}
=
\frac{
(i\Delta_n)^{m-1}
\zeta^{(m)}(\rho_n)
}{
m!\zeta'(\rho_n)
},
\qquad
m\ge2.
}
\]

These are defined observables.

They are not asserted to be constant, convergent, or RH-forcing.

---

# 30. Generic-base control

For any

\[
b>1,
\]

define

\[
\boxed{
q_{\rho,b}
=
b^{\rho-\frac12}.
}
\]

Then

\[
\boxed{
|q_{\rho,b}^K|
=
b^{K\delta}.
}
\]

Therefore the bare radial-amplification formula is generic in the positive base.

Any claim of specifically tau-dependent proof leverage must identify an additional exact property tied to

\[
\tau=2\pi.
\]

---

# 31. Exact versus conjectural classifications

Every active mathematics card or research artifact should classify a formula as one of:

```text
EXACT_IDENTITY
COORDINATE_CONTROL
DEFINED_OBSERVABLE
NUMERICAL_OBSERVATION
CANDIDATE_INVARIANT
CONJECTURAL_IMPLICATION
SYNTHETIC_DIAGNOSTIC
```

Do not display a conjectural implication as an exact identity.

---

# 32. Forbidden shortcuts

The implementation must not:

1. use the raw Dirichlet series
   \[
   \sum n^{-s}
   \]
   as the numerical definition of zeta in the critical strip;

2. seed baseline zero discovery from the external reference list and then call the result independent validation;

3. conflate camera, height sampling, origin dilation, centered dilation, argument scaling, kernel transformation, or transcendental continuation;

4. treat integer \(K\) and real \(k\) as semantically interchangeable;

5. infer zero-slice disjointness from arithmetic-lattice noncoincidence;

6. claim that compression forces an off-line zero onto the critical surface;

7. call synthetic moved-zero configurations another zeta function;

8. silently cast authoritative decimal inputs to Python `float` or NumPy `complex128` before the authoritative metric is formed;

9. infer RH from finite zero verification;

10. promote an RH-equivalent bound as a softer intermediate lemma.

---

# 33. Deterministic trust vectors

These are minimum mathematical regression vectors.

## Vector A — native transcendental grade

Set

\[
k=0.
\]

Require

\[
\boxed{
\mathcal Z_\tau(s,0)=\zeta(s).
}
\]

## Vector B — grade composition

For arbitrary test values \(k_1,k_2\),

\[
\boxed{
\tau^{k_1+k_2}
=
\tau^{k_1}\tau^{k_2}
}
\]

to declared precision.

## Vector C — reciprocal grades

For nonzero integer \(K\),

\[
\boxed{
\tau^K\tau^{-K}=1.
}
\]

## Vector D — zero worldline

For a reference zero \(\rho\) and selected real \(k\),

\[
\boxed{
\mathcal Z_\tau(\tau^k\rho,k)=0
}
\]

to the declared numerical residual tolerance.

## Vector E — critical surface

For

\[
s=\frac12+it,
\]

require

\[
\boxed{
\Re(\tau^k s)=\frac{\tau^k}{2}.
}
\]

## Vector F — radial invariant

For

\[
\rho=\frac12+\delta+i\gamma,
\]

require

\[
\boxed{
R_\tau(\tau^k\rho,k)=\delta.
}
\]

## Vector G — origin dilation

For generic \(A>0\),

\[
\boxed{
f_A(A s)=\zeta(s).
}
\]

## Vector H — centered dilation

For

\[
s'
=
\frac12+A(s-\frac12),
\]

require inverse mapping back to the original zeta argument.

## Vector I — argument transform zero map

For

\[
f_A(s)=\zeta(As),
\]

require predicted zero

\[
s=\rho/A.
\]

## Vector J — inverse kernel lock

For

\[
AB=1,
\quad
C=D=0,
\]

require

\[
\boxed{
\mathcal Z_{A,0,B,0}(s)=\zeta(s).
}
\]

## Vector K — zero character

Require

\[
\boxed{
|q_\rho^K|=\tau^{K\delta}.
}
\]

## Vector L — symmetric grade defect

Require

\[
\boxed{
|D_K|
=
4\sinh^2
\left(
\frac{K\delta\log\tau}{2}
\right).
}
\]

## Vector M — converter remainder

Audit numerical integration of

\[
R(x)
\]

against the \(E_1\) series at controlled \(x\).

## Vector N — converter covariance

Require

\[
\boxed{
C_J(x^{1/A},A\rho)=C_J(x,\rho).
}
\]

## Vector O — split quadratic behavior

For sufficiently small declared \(\delta\), verify the computed split against the exact Taylor expansion order without claiming an exact hyperbolic converter law.

## Vector P — cross-height normalization

At a verified simple zero require

\[
\boxed{
P_n(0)=0,
\qquad
P_n'(0)=1
}
\]

to declared numerical tolerance.

---

# 34. Proof-facing non-identity

The following is deliberately **not** part of the mathematical contract:

\[
\boxed{
\text{Transcendental Coherence}
\Longrightarrow
\text{one occupied radial leaf}.
}
\]

That is the central open research theorem.

The implementation may test candidate forms but must not encode the conclusion as an identity, axiom, or automatic verdict.

---

# 35. Riemann–Weil Explicit Formula & Grade-Indexed Constraints

## 35.1 Authoritative explicit formula normalization

For an even holomorphic test function \(h(t)\) on \(|\Im(t)| \le 1/2 + \delta\) satisfying rapid Schwartz decay on \(\mathbb R\), define the Fourier transform convention:

\[
\boxed{
\widehat h(x) = \int_{-\infty}^\infty h(t) e^{-i x t} \, dt = 2 \int_0^\infty h(t) \cos(x t) \, dt.
}
\]

The Riemann–Weil Explicit Formula residual is defined as:

\[
\boxed{
\operatorname{EF}[h; \mathcal D, \mathcal A] = \sum_{\rho \in \mathcal D} h\left(\frac{\rho - 1/2}{i}\right) - \left[ 2 \Re h(i/2) - \frac{1}{\pi} \sum_{n=1}^\infty \frac{\Lambda(n)}{\sqrt{n}} \widehat h(\log n) + \frac{1}{\pi} \int_0^\infty h(t) \Re\left(\psi\left(\frac{1}{4} + \frac{it}{2}\right) - \log \pi\right) dt \right],
}
\]

where:
- \(\mathcal D\) is the zero divisor (for native \(\zeta\), \(\rho_n = 1/2 \pm i\gamma_n\));
- \(\mathcal A\) represents the fixed arithmetic data: primes, von Mangoldt weights \(\Lambda(n)\), pole at \(s=1\), and gamma factor \(\Gamma(s/2)\);
- \(\psi(z) = \Gamma'(z)/\Gamma(z)\) is the digamma function;
- \(2 \Re h(i/2)\) is the pole contribution at \(s=0, 1\).

For the true zeta divisor \(\mathcal D_\zeta\) and arithmetic data \(\mathcal A_\zeta\):

\[
\boxed{
\operatorname{EF}[h; \mathcal D_\zeta, \mathcal A_\zeta] = 0.
}
\]

## 35.2 Definition of \(\mathcal C_{K,j}\) and Fourier grade scaling

For a shared test function \(H_j(t)\) defined in grade coordinates, the grade-\(K\) representation induces:

\[
\boxed{
h_{K,j}(t) = H_j(a_K t), \qquad a_K = \tau^K = (2\pi)^K.
}
\]

The grade constraint is defined as:

\[
\boxed{
\mathcal C_{K,j} = \operatorname{EF}[h_{K,j}; \mathcal D_\zeta, \mathcal A_\zeta].
}
\]

Under the project Fourier convention, the Fourier transform scales as:

\[
\boxed{
\widehat h_{K,j}(x) = a_K^{-1} \widehat H_j(a_K^{-1} x).
}
\]

Therefore, prime frequencies scale as \(a_K^{-1} \log n = \tau^{-K} \log n\).

## 35.3 Mandatory coordinate-equivalence control

By direct substitution, the grade-\(K\) constraint is an evaluation of the native explicit formula against a scaled test function:

\[
\boxed{
\mathcal C_K[H] \equiv \mathcal C_0[H \circ a_K].
}
\]

The constraint subspace spanned by \(\{ \mathcal C_{K,j} : K \in \mathcal K, j \in \mathcal J \}\) is identical to that spanned by the expanded \(K=0\) native basis \(\{ \mathcal C_0[H_j(a_K \cdot)] : K \in \mathcal K, j \in \mathcal J \}\).
The exact theoretical classification is:

\[
\boxed{
\text{coordinate\_redundant}
}
\]

When compared strictly against a finite unexpanded \(K=0\) basis \(\{ H_j(t) \}\), the classification is:

\[
\boxed{
\text{finite\_basis\_enrichment\_only}
}
\]

These two classifications address distinct mathematical questions and must never be combined into a single interchangeable label.

## 35.4 Finite divisor defect \(\Delta \mathcal C_{K,j}\) and decomposition

When arithmetic data \(\mathcal A_\zeta\) is held fixed while the zero divisor is modified \(\mathcal D \to \mathcal D + \Delta \mathcal D\), all arithmetic, pole, and gamma terms cancel identically:

\[
\boxed{
\Delta \mathcal C_{K,j} = \operatorname{EF}[h_{K,j}; \mathcal D_\zeta + \Delta\mathcal D, \mathcal A_\zeta] - \operatorname{EF}[h_{K,j}; \mathcal D_\zeta, \mathcal A_\zeta] = \langle \Delta\mathcal D, h_{K,j} \rangle = \sum_{\rho \in \mathcal D_{\text{new}}} h_{K,j}\left(\frac{\rho - 1/2}{i}\right) - \sum_{\rho \in \mathcal D_{\text{old}}} h_{K,j}\left(\frac{\rho - 1/2}{i}\right).
}
\]

A non-zero divisor perturbation produces a non-zero defect on at least some separating test functions in the infinite space of admissible test functions, though it may have smaller projection onto any finite selected family.

- **Critical-line height perturbation**: For \(1/2 \pm i\gamma_n \mapsto 1/2 \pm i(\gamma_n + \varepsilon)\):
  - Exact defect:
    \[
    \Delta \mathcal C_{K,j}(\varepsilon) = 2 \left[ H_j(a_K(\gamma_n + \varepsilon)) - H_j(a_K \gamma_n) \right].
    \]
  - Linearized defect and Jacobian column:
    \[
    \Delta \mathcal C_{K,j}^{\mathrm{linear}}(\varepsilon) = 2 a_K H_j'(a_K \gamma_n) \varepsilon = J_{(K,j), n} \varepsilon.
    \]
  - Non-linear remainder:
    \[
    R_{K,j}(\varepsilon) = \Delta \mathcal C_{K,j}(\varepsilon) - \Delta \mathcal C_{K,j}^{\mathrm{linear}}(\varepsilon) = \mathcal O(\varepsilon^2).
    \]

- **Symmetry-complete radial quartet decomposition**: Replacing pairs \(1/2 \pm i\gamma_a\) and \(1/2 \pm i\gamma_b\) with quartet \(1/2 \pm \delta \pm i\gamma_0\) (\(\gamma_0 = (\gamma_a + \gamma_b)/2\), total 4 zeros):
  - Height-merging baseline defect (independent of \(\delta\)):
    \[
    \Delta \mathcal C_{K,j}^{\mathrm{merge}} = 4 H_j(a_K \gamma_0) - 2 H_j(a_K \gamma_a) - 2 H_j(a_K \gamma_b).
    \]
  - Pure radial defect (strictly vanishes at \(\delta = 0\), even in \(\delta\)):
    \[
    \Delta \mathcal C_{K,j}^{\mathrm{radial}}(\delta) = 4 \Re\left[ H_j(a_K(\gamma_0 + i\delta)) \right] - 4 H_j(a_K \gamma_0) = 4 \Re\left[ H_j(a_K \gamma_0 + i a_K \delta) - H_j(a_K \gamma_0) \right].
    \]
  - Total defect:
    \[
    \Delta \mathcal C_{K,j}^{\mathrm{total}}(\delta) = \Delta \mathcal C_{K,j}^{\mathrm{merge}} + \Delta \mathcal C_{K,j}^{\mathrm{radial}}(\delta).
    \]

- **Divisor perturbation validation**: Any proposed zero-divisor mutation must be verified by `validate_divisor_perturbation` to confirm symmetry completeness (\(\rho \mapsto \overline\rho\) and \(\rho \mapsto 1-\rho\)) and multiplicity preservation before evaluation. Single un-partnered complex zero mutations are rejected.

- **Epistemic boundary**: These perturbation metrics constitute a local sensitivity diagnostic under frozen arithmetic data. They do not constitute an alternative zeta function or a proof of global non-compensation across the infinite zero set.

## 35.5 Explicit formula grade independence and future candidates

1. The explicit formula family \(\mathcal C_{K,j}\) operates exclusively via the coordinate pullback identity \(\mathcal C_K[H] \equiv \mathcal C_0[H \circ a_K]\) and is **coordinate-redundant** with respect to the native explicit formula evaluated on scaled test functions.
2. Any prospective mathematical mechanism attempting to impose cross-grade constraints without test-function dilation remains an **OPEN / UNDEFINED CANDIDATE** and must not be identified with \(\mathcal C_{K,j}\).
3. The coordinate dilation \(a_K = \tau^K\) does not imply or assume any non-trivial automorphism \(\zeta(\tau^K s) = \zeta(s)\).

# 36. Second-Order Radial Variation and Defect Divisor Formulation

## 36.1 Radial projection operator and defect divisor

Let \(\mathcal D\) be a divisor of points in the critical strip \(0 < \Re(s) < 1\).
For \(\rho = 1/2 + \delta + i\gamma\), define the radial projection onto the critical line:

\[
\boxed{
\mathcal P_0(\rho) = \frac{1}{2} + i\gamma.
}
\]

For a general zero divisor \(\mathcal D = \sum_{\rho} m_\rho [\rho]\), the projected divisor is:

\[
\boxed{
\mathcal P_0(\mathcal D) = \sum_{\rho} m_\rho [\mathcal P_0(\rho)],
}
\]

and the radial defect divisor is:

\[
\boxed{
\Delta\mathcal D_{\mathrm{rad}} = \mathcal D - \mathcal P_0(\mathcal D).
}
\]

For a single symmetry-complete orbit \(\mathcal O(\rho) = \{1/2 \pm \delta \pm i\gamma\}\), the projected divisor is the critical-line pair \(2[1/2 + i\gamma] + 2[1/2 - i\gamma]\), and:

\[
\boxed{
\Delta\mathcal D_{\mathrm{rad}}(\mathcal O(\rho)) = [1/2 + \delta + i\gamma] + [1/2 - \delta + i\gamma] + [1/2 + \delta - i\gamma] + [1/2 - \delta - i\gamma] - 2[1/2 + i\gamma] - 2[1/2 - i\gamma].
}
\]

## 36.2 Exact finite-orbit second-order response

For an even, real-entire test function \(h(t)\) (with \(h(-t) = h(t)\) and \(h(t) \in \mathbb R\) for \(t \in \mathbb R\)), the evaluation on \(\mathcal O(\rho)\) is:

\[
\langle \mathcal O(\rho), h \rangle = 4 \Re\left[ h(\gamma + i\delta) \right].
\]

Holomorphic Taylor expansion along the imaginary displacement \(i\delta\) gives:

\[
h(\gamma + i\delta) = h(\gamma) + i\delta h'(\gamma) - \frac{\delta^2}{2} h''(\gamma) - i\frac{\delta^3}{6} h^{(3)}(\gamma) + \frac{\delta^4}{24} h^{(4)}(\gamma) + \mathcal O(\delta^6).
\]

Taking the real part:

\[
\Re\left[ h(\gamma + i\delta) \right] = h(\gamma) - \frac{\delta^2}{2} h''(\gamma) + \frac{\delta^4}{24} h^{(4)}(\gamma) + \mathcal O(\delta^6).
\]

Therefore, the pure radial defect response is:

\[
\boxed{
\Delta\mathcal C_h[\mathcal O(\rho)] = \langle \Delta\mathcal D_{\mathrm{rad}}(\mathcal O(\rho)), h \rangle = -2\delta^2 h''(\gamma) + \frac{\delta^4}{12} h^{(4)}(\gamma) + \mathcal O(\delta^6).
}
\]

Defining the non-negative second-order orbit variable \(u = \delta^2 \ge 0\):

\[
\boxed{
\Delta\mathcal C_h[\mathcal O(\rho)] = -2 u h''(\gamma) + \mathcal O(u^2).
}
\]

## 36.3 Multi-orbit linearized radial response matrix, quadratic energy, and finite compensation

For \(N\) hypothetical off-line zero orbits \(\{\mathcal O(\rho_n)\}_{n=1}^N\) with distinct ordinates \(\gamma_n\) and radial displacements \(u_n = \delta_n^2 \ge 0\) (\(u \in \mathbb R_+^N\)), the linearized radial defect vector across a family of test functions \(\{h_j\}_{j=1}^M\) is:

\[
\boxed{
\Delta\mathcal C^{\mathrm{linear}}_j = \sum_{n=1}^N K_{j,n} u_n, \qquad K_{j,n} = -2 h''_j(\gamma_n).
}
\]

The single-target quadratic radial energy for orbit \(n\) is:

\[
\boxed{
E(u_n) = \|K_{\cdot, n} u_n\|^2 = u_n^2 \|K_{\cdot, n}\|^2 \ge 0.
}
\]

### Mathematical Distinction: Single-Target Energy vs Subspace Cone Compensation
1. **Single-Target Positivity**: For any non-trivial test packet \(h\) where \(h''(\gamma_n) \ne 0\), the single-target energy \(E(u_n) > 0\) for \(u_n > 0\).
2. **Subspace Non-Negative Compensation**: Single-target positivity does **NOT** preclude non-negative linear combinations of the remaining columns \(K_{-n} u_{-n}\) with \(u_{-n} \ge 0\) from matching or canceling \(K_{\cdot, n} u_n\) in a finite-dimensional test space:
   \[
   \min_{u_{-n} \ge 0} \|K_{\cdot, n} u_n - K_{-n} u_{-n}\|^2.
   \]
3. **Finite Basis Nullity**: In any finite basis of \(M\) test functions (e.g. \(M=30\) channels across 100 zeros), the high numerical nullity (\(\approx 85\)) and ill-conditioning (\(\kappa \sim 10^{15}\)) produce threshold-dependent numerical behavior: compensation was found in the declared basis at the \(10^{-5}\) threshold for interior zeros (zeros 10 and 50 with relative residuals \(< 10^{-6}\)) and was not found at this threshold for peripheral zeros (zeros 1 and 100). This observational diagnostic does not prove nonexistence of a compensating measure or global radial rigidity.

## 36.4 The Projection Trap and Open Mathematical Obligations

1. **The Projection Trap**:
   - The actual zero divisor \(\mathcal D_\zeta = \sum_\rho [\rho]\) has an established arithmetic explicit-formula representation connecting its spectral sum to primes and poles: \(\operatorname{EF}[h; \mathcal D_\zeta, \mathcal A_\zeta] = 0\).
   - However, its critical-line projection \(\mathcal P_0(\mathcal D_\zeta) = \sum_\rho [1/2 + i\gamma_\rho]\) is **NOT** known to be the divisor of any Dirichlet series or Euler product, and has **NO** established independent arithmetic representation.
   - Consequently, \(\langle \mathcal P_0(\mathcal D_\zeta), h \rangle\) cannot be independently evaluated via arithmetic data without already assuming that all zeros lie on the critical line (\(\mathcal D_\zeta = \mathcal P_0(\mathcal D_\zeta)\)), which is circular.
2. **The Scoped One-Point No-Go Theorem**:
   - Let \(H\) be a holomorphic test function defined on a vertical strip containing the critical strip, and let \(G = H + H \circ (-\mathrm{id})\) be the symmetrized even holomorphic function.
   - If the quartet response \(A_H(\delta, \gamma) = 2 \Re G(\delta + i\gamma)\) is independent of \(\delta\) on an open interval \(I \ni 0\) for each \(\gamma\) in an open interval, then Cauchy-Riemann equations force \(G(z)\) to be identically constant.
   - **Scope**: Rigorously proves the **CLOSED** status of `OBL-EF-003` for fixed linear combinations and locally uniform limits of direct 1-point holomorphic Riemann–Weil evaluations.
   - Does **not** preclude nonlinear paired, sesquilinear, determinantal, operator, or zeta-divisor-specific comparison objects (`OBL-RDQ-001`, **OPEN**).

## 36.5 Countermodel Controls and Epistemic Classification

1. **Structural Countermodels**:
   - Davenport–Heilbronn and Epstein zeta functions possess functional-equation reflection symmetry \(\delta \mapsto -\delta\) and exact coordinate covariance, yet possess off-line zeros.
   - They serve as structural countermodels demonstrating that functional symmetry and coordinate covariance alone are mathematically insufficient to exclude off-line zeros.
   - We do not claim their off-line zeros are caused by one isolated missing ingredient unless proved.
2. **Epistemic Classification**:
   - The finite second-order radial response construction is classified as an **exact finite synthetic sensitivity diagnostic**.
   - It validates the local quadratic Taylor fidelity (\(\mathcal O(\delta^2)\) relative error \(< 0.04\%\)), while finite NNLS compensation remains heterogeneous and dependent on the chosen test family.

# 37. Radial-Defect Quotient \(Q(z)\), Limiting Invariant \(L_Q\), and Relative Fredholm Determinants

## 37.1 Centered coordinates and reference objects
In centered coordinate \(z = s - 1/2 = \delta + it\), let \(\Xi(z) = \xi(1/2 + z)\).
Product premises:
1. **Exclusion of Real Nontrivial Zeros**: \(\zeta(s) \ne 0\) for \(s \in (0, 1)\), so \(\gamma = \Im \lambda \ne 0\).
2. **Paired Hadamard Factorization**:
   \[
   \Xi(z) = \Xi(0) \prod_{\lambda \in \Lambda^+} \left(1 - \frac{z^2}{\lambda^2}\right)^{m_\lambda}.
   \]
3. **General Multiplicity Formula**: At each distinct zero height \(\gamma > 0\):
   \[
   m_\gamma = m_{0,\gamma} + 2 \sum_{j} n_{j,\gamma},
   \]
   where \(m_{0,\gamma} \ge 0\) is critical-line multiplicity (\(\delta=0\)) and \(n_{j,\gamma} \ge 0\) is off-line quartet multiplicity for radial orbit \(j\) (\(\delta_{j,\gamma} > 0\)).
4. **Baseline Reference Function**:
   \[
   \boxed{
   \Xi^\flat(z) = \prod_{\gamma > 0} \left(1 + \frac{z^2}{\gamma^2}\right)^{m_\gamma}.
   }
   \]
The Radial-Defect Quotient is:
\[
\boxed{
Q(z) = \frac{\Xi(z)}{\Xi(0) \Xi^\flat(z)} = \prod_{j} \left( Q_{\delta_j,\gamma_j}(z) \right)^{n_j}.
}
\]

## 37.2 Real-axis quartet factor and audited properties
For an off-line quartet \(\{\pm\delta \pm i\gamma\}\), the factor evaluated on \(z = x \in \mathbb R\) is:
\[
\boxed{
q_{\delta,\gamma}(x) = \frac{\gamma^4 \left[ (x^2 + \gamma^2 - \delta^2)^2 + 4\delta^2\gamma^2 \right]}{(\gamma^2+\delta^2)^2 (x^2+\gamma^2)^2}.
}
\]
Exact audited properties:
1. **Positivity, Boundedness, and Exact Defect Factorization**:
   \[
   0 < q_{\delta,\gamma}(x) \le 1 \quad \forall x\in\mathbb R,
   \qquad
   1 - q_{\delta,\gamma}(x) = \frac{\delta^2 x^2 \left[(\delta^2 + 2\gamma^2)x^2 + 2\gamma^2(\delta^2 + 3\gamma^2)\right]}{(\delta^2+\gamma^2)^2 (x^2+\gamma^2)^2} \ge 0.
   \]
   Equality \(q(x)=1\) holds iff \(x=0\) (for \(\delta \ne 0\)) and \(q_{0,\gamma}(x) \equiv 1\).
2. **Extremum in \(u = x^2\) and Real Minimizers**: Unique minimum in \(u = x^2 \ge 0\) at \(u_* = \delta^2 + 3\gamma^2\), corresponding to two real minimizers \(x = \pm\sqrt{\delta^2 + 3\gamma^2}\).
3. **Minimum Value**: \(q_{\min} = \frac{4}{(1+r)^2(4+r)}\) where \(r = \delta^2/\gamma^2\).
4. **Uniform Domination Estimate**:
   \[
   \sup_{x\in\mathbb R} |\log q_{\delta,\gamma}(x)| = 2\log(1+r) + \log\left(1 + \frac{r}{4}\right) \le \frac{9}{4}r.
   \]
5. **Limiting Invariant**:
   \[
   \boxed{
   L_Q = \lim_{x\to\infty} Q(x) = \prod_{j} \left(\frac{\gamma_j^2}{\gamma_j^2+\delta_j^2}\right)^{2n_j} = \prod_j (1 + r_j)^{-2n_j}.
   }
   \]
   Spectral equivalence: \(0 < L_Q \le 1\), and \(L_Q = 1 \iff \mathrm{RH}\).
6. **Grade-Indexed Covariance**: Under grade dilation \(s_K = \tau^K s \implies z_K = \tau^K z\):
   \[
   \boxed{
   Q_K(z_K) = Q_0(\tau^{-K} z_K),
   \qquad
   Q_K(\tau^K z) = Q_0(z),
   }
   \]
   while the displacement spectrum \(\{r_\lambda = \delta_\lambda^2/\gamma_\lambda^2\}\), \(L_Q\), and \(\operatorname{Tr}\mathcal R\) are strictly grade-invariant.

## 37.3 Relative Fredholm spectral formulation
Define the positive diagonal trace-class operator \(\mathcal R\) on \(\ell^2(\Lambda^+)\) by:
\[
\boxed{
\mathcal R e_\lambda = \frac{\delta_\lambda^2}{\gamma_\lambda^2} e_\lambda.
}
\]
Then:
\[
\operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \frac{\delta_\lambda^2}{\gamma_\lambda^2} < \infty,
\qquad
\det_{\mathrm F}(I + \mathcal R) = L_Q^{-1},
\qquad
-\log L_Q = \operatorname{Tr}\log(I + \mathcal R) = \log\det_{\mathrm F}(I + \mathcal R).
\]
Because \(\mathcal R \ge 0\):
\[
\operatorname{Tr}\mathcal R = 0 \iff \mathcal R = 0 \iff \mathrm{RH},
\qquad
\det_{\mathrm F}(I + \mathcal R) = 1 \iff \mathrm{RH}.
\]

## 37.4 Target hierarchy
1. **Minimal Scalar Target**: \(\operatorname{Tr}\mathcal R = \sum \frac{\delta^2}{\gamma^2}\) (RH equivalent, minimal complexity).
2. **Scalar Determinant Target**: \(D_\zeta(1) = \det_{\mathrm F}(I+\mathcal R) = L_Q^{-1}\).
3. **Full Determinant Family**: \(D_\zeta(t) = \det_{\mathrm F}(I + t\mathcal R)\).
4. **Operator Target**: Arithmetic operator isospectral to \(\mathcal R\).

# 38. Reflection-Paired Involution Kernel \(\kappa_1(z,w)\) and Arithmetic Trace Target

## 38.1 Rational involution pairing kernel
For \(z = \delta + i\gamma\), define the involution \(z^\# = -\bar z = -\delta + i\gamma\).
Define the rational kernel:
\[
\boxed{
\kappa_1(z,w) = \frac{4zw}{(z+w)^2} - 1.
}
\]
Exact involution identity:
\[
z + z^\# = 2i\gamma \implies (z+z^\#)^2 = -4\gamma^2,
\qquad
z z^\# = -(\delta^2+\gamma^2).
\]
\[
\boxed{
\kappa_1(z, z^\#) = \frac{4(-(\delta^2+\gamma^2))}{-4\gamma^2} - 1 = \frac{\delta^2+\gamma^2}{\gamma^2} - 1 = \frac{\delta^2}{\gamma^2}.
}
\]
Therefore:
\[
\boxed{
\operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \kappa_1(\lambda, \lambda^\#).
}
\]

## 38.2 Epistemic boundary and open research obligation
1. **Closure under involution**: Functional equation and Schwarz reflection guarantee that the zero set is closed under \(\lambda \mapsto \lambda^\#\).
2. **Open Research Theorem (OBL-RDQ-001)**: Can a divisor-independent arithmetic or spectral construction isolate the pairs \((\lambda, \lambda^\#)\) and evaluate \(\kappa_1\) to compute \(\operatorname{Tr}\mathcal R\) or \(D_\zeta(1)\)?
3. **Grade Invariance**: \(L_Q\), \(\{r_\lambda\}\), and \(\mathcal R\) are grade-invariant under \((x,\delta,\gamma)\mapsto(\tau^K x, \tau^K \delta, \tau^K \gamma)\); grade dilation alone does not force \(\operatorname{Tr}\mathcal R = 0\). Additional zeta-specific arithmetic content is required.

---

# 39. Arithmetic Radial Bridge and Candidate Evaluation Harness

## 39.1 Target distinction
1. **Determinant Target**:
   \[
   D := -\log L_Q = \log\det_{\mathrm F}(I+\mathcal R) = \sum_j 2n_j \log(1+r_j), \qquad \mathfrak A_{K,D}^{\mathrm{arith}} = D.
   \]
2. **Trace Target**:
   \[
   T := \operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \frac{\delta_\lambda^2}{\gamma_\lambda^2} = \sum_j 2n_j r_j, \qquad \mathfrak A_{K,T}^{\mathrm{arith}} = T.
   \]
3. **Regularized Weighted Target**:
   \[
   T_a := \sum_{\lambda\in\Lambda^+} w_a(\lambda) \frac{\delta_\lambda^2}{\gamma_\lambda^2}, \qquad w_a(\lambda) = m_\lambda e^{-a\gamma_\lambda^2} > 0.
   \]

## 39.2 Strict arithmetic input firewall
Permitted: prime powers, von Mangoldt \(\Lambda(n)\), Euler product (\(\Re(s)>1\)), pole at \(s=1\), gamma factor, functional equation \(\xi(s)=\xi(1-s)\), Schwarz reflection, admissible test functions, exact bilateral grades \(K\in\mathbb Z\), transcendental continuation \(\mathcal Z_\tau(s,K)=\zeta(\tau^{-K}s)\).
Forbidden: zero lists, \(\delta_j, \gamma_j, \lambda_j^\#\), projected ordinates, projected divisor \(\mathcal P_0(\mathcal D_\zeta)\), \(\Xi^\flat\), \(Q, L_Q, \mathcal R, D, T\), or circular RH-equivalent definitions.

## 39.3 Grade-centering geometry
Under origin dilation \(s_K = \tau^K s\), the critical line \(\Re(s)=1/2\) maps to \(\Re(s_K) = \tau^K/2 = c_K\).
The centered grade coordinate is:
\[
z_K = s_K - c_K = \tau^K s - \frac{\tau^K}{2} = \tau^K\left(s - \frac{1}{2}\right) = \tau^K z.
\]
The centered completed xi function satisfies:
\[
\Xi_K(z_K) = \xi\left(\frac{1}{2} + \tau^{-K} z_K\right) \implies \Xi_K(\tau^K z) = \Xi_0(z).
\]

## 39.4 Covariance countermodel (Covariance \(\ne\) Rigidity)
The abstract off-line quartet \(\mathcal Q_{\delta,\gamma} = \{1/2 \pm \delta \pm i\gamma\}\) (\(\delta \ne 0\)) is closed under reflection \(s \mapsto 1-s\), conjugation \(s \mapsto \bar s\), involution \(s \mapsto 1-\bar s\), and grade transport, proving that symmetry and covariance are fully compatible with \(\delta \ne 0\). Covariance alone does not force \(\delta = 0\); an independent arithmetic zero-valued anchor \(\mathfrak A_K = 0\) is required.

## 39.5 Candidate classifications
- **Candidate A (Linear Grade Differences)**: `FALSIFIED_FOR_BRIDGE` (collapses to native explicit formula \(\mathcal C_0[H\circ\tau^K]-\mathcal C_0[H]\)).
- **Candidate B (Bilinear Cross-Grade Explicit Formula)**: `FALSIFIED_FOR_PAIR_ISOLATION` (\(D_K(s)\overline{D_L(s)}\) yields unrestricted double sum over all zero pairs; off-diagonal terms contaminate).
- **Candidate C (Tensor-Square Trace Identity)**: `FALSIFIED_FOR_PAIR_ISOLATION` (unrestricted double sum).
- **Candidate D (Log-Derivative Contour Identity)**: `FALSIFIED_FOR_PAIR_ISOLATION` (residue cross-terms across critical strip).
- **Candidate E (Relative Determinant from Arithmetic Space)**: `OPEN_UNPROVED` (no zero-independent operator).
- **Candidate F (Grade-Indexed Prime-Power Pairing)**: `OPEN_UNPROVED` (pairing law unproved).
- **Candidate G (Weighted Regularized Bridge)**: `LIVE_UNDERIVED` (spectral detector \(T_a>0\) proved; arithmetic realization open).

---

# 40. Separated Signal Bridge & Arbitrary Algebraic Curvature Rigidity

## 40.1 Arbitrary Finite Curvature Identity
For any finite collection of real radial displacements \(\{d_i\}_{i=1}^N\), the double sum of squared pairwise sums decomposes exactly:
\[
\sum_{i,j=1}^N (d_i + d_j)^2 = 2N \sum_{i=1}^N d_i^2 + 2\left(\sum_{i=1}^N d_i\right)^2.
\]
1. **Unconditional Non-negativity**: \(\sum_{i,j=1}^N (d_i + d_j)^2 \ge 0\).
2. **Zero-Rigidity**: \(\sum_{i,j=1}^N (d_i + d_j)^2 = 0 \iff \forall i \in \{1,\dots,N\}, d_i = 0\).
3. **Symmetric Reduction**: When \(\sum_{i=1}^N d_i = 0\) (e.g. for reflection-symmetric pairs \(\{\delta, -\delta\}\)), the sum reduces to \(2N \sum d_i^2\).

## 40.2 Separated Signal Candidate Classifications
- **CANDIDATE_SS1 (Cauchy-Riemann Holomorphic Rigidity)**: `FALSIFIED_GATE_1_4` (Cauchy-Riemann forces holomorphic rigidity).
- **CANDIDATE_SS2 (Polarized Bilinear Cross-Difference)**: `FALSIFIED_GATE_2_5` (Unrestricted double-sum cross-term contamination).
- **CANDIDATE_SS3 (Cramér Logarithmic Phase Variance)**: `FALSIFIED_GATE_4_6` (Cramér transformation divergence; arithmetic firewall violation).
- **CANDIDATE_SS4 (Transcendental Scale Non-Resonance)**: `FALSIFIED_GATE_2_3` (Non-resonance does not eliminate off-diagonal zero-pair contamination).
- **CANDIDATE_SS5 (Direct Positive Quadratic Kernel)**: `FALSIFIED_GATE_1_6` (Holomorphic vanishing firewall).

---

# 41. Complete Finite Spectral Expansion & Exact Analytic Kernels

## 41.1 Completed Logarithmic Derivative Identity
For \(\Re(u) > 1\):
\[
P(u) := \sum_{n=2}^\infty \frac{\Lambda(n)}{n^u} = A(u) - \frac{\Xi'}{\Xi}\left(u - \frac{1}{2}\right),
\]
where \(A(u) = \frac{1}{u} + \frac{1}{u-1} - \frac{1}{2}\log \pi + \frac{1}{2}\psi(u/2)\).

## 41.2 Complete Finite Spectral Expansion
For any finite subset of zeros \(\mathcal Z_N = \{\lambda_k = \delta_k + i\gamma_k\}_{k=1}^N\) and \(z = a + it = \sigma - 1/2 + it\):
\[
S_{N, T}(\sigma) := \frac{1}{2T}\int_{-T}^T \left| A(\sigma+it) - \sum_{k=1}^N m_k \frac{2z}{z^2-\lambda_k^2} \right|^2 dt = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ},
\]
where:
1. \(I_{AA} = \frac{1}{2T}\int_{-T}^T |A(\sigma+it)|^2 dt\);
2. \(I_{AZ} = \frac{1}{2T}\int_{-T}^T A(\sigma+it)\overline{Z_N(t)} dt\), \(I_{ZA} = \overline{I_{AZ}}\);
3. \(I_{ZZ} = \sum_{j,k=1}^N K_T(\lambda_j, \lambda_k; a)\), with closed paired zero-zero kernel:
   \[
   K_T(\lambda, \mu; a) = m_\lambda m_\mu \sum_{\varepsilon, \eta \in \{\pm 1\}} J_T(a - \varepsilon\lambda, a - \eta\bar\mu),
   \]
   and exact analytic translation kernel:
   \[
   \boxed{J_T(p, q) := \frac{1}{2T}\int_{-T}^T \frac{dt}{(p+it)(q-it)} = \frac{\log\left(\frac{p+iT}{p-iT}\right) + \log\left(\frac{q+iT}{q-iT}\right)}{2Ti(p+q)}.}
   \]

## 41.3 Exact Real-Axis Spectral Defect Formula
For an off-line quartet \(\{\pm\delta \pm i\gamma\}\) vs on-line pair \(\{0, \pm i\gamma\}\) at \(z = \sigma - 1/2 > 0\):
\[
\boxed{\Delta(\delta) := \frac{4z\delta^2(z^2 - 3\gamma^2 - \delta^2)}{(z^2 + \gamma^2)[(z^2 + \gamma^2 - \delta^2)^2 + 4\delta^2\gamma^2]}.}
\]
Sign behavior: \(\Delta(\delta) < 0\) for \(z^2 < 3\gamma^2 + \delta^2\) (all critical strip ordinates \(\gamma > 14\) at \(z = O(1)\)), transitioning to positive only for \(z > \sqrt{3}\gamma\).

## 41.4 Earliest Infinite Analytic Obstruction (Gate G4)
Individual zero resolvent terms belong to \(L^2(\mathbb R, dt)\) with finite norm \(\frac{\pi}{\sigma-\Re\rho}\), so \(\frac{1}{2T}\int_{-T}^T \frac{dt}{|\sigma-\rho+it|^2} \to 0\) as \(T\to\infty\). The non-zero Besicovitch mean of the arithmetic side is carried by non-uniform infinite collective cancellation. Termwise infinite limit interchange \(\lim_{T\to\infty}\sum_{\lambda,\mu} K_T = \sum_{\lambda,\mu}\lim_{T\to\infty} K_T\) is unproved and false without regularized weighting.

---

# 42. Gate G4 Windowed Expansion & Boundary Layer Limits

## 42.1 Exact Fejér Windowed Kernel
For the triangular / Fejér window \(W_T(t) = \frac{1}{T}(1 - |t|/T)\mathbf 1_{[-T, T]}(t)\):
\[
\boxed{J_T^{\text{Fejér}}(p, q) := \int_{-T}^T \frac{1}{T}\left(1 - \frac{|t|}{T}\right) \frac{dt}{(p+it)(q-it)} = \frac{I_T(p) + I_T(q)}{T(p+q)},}
\]
where
\[
I_T(w) = -\frac{(w+iT)\log(w+iT) + (w-iT)\log(w-iT) - 2w\log w}{T}.
\]

## 42.2 Asymptotic Regimes of \(J_T\)
For \(p = a - i\gamma, q = a + i\gamma\) (\(a > 0\)):
1. \(|\gamma| \ll T\) (Plateau): \(J_T \sim \frac{\pi}{2a T}\).
2. \(\gamma / T \to c \in (0, \infty)\) (Boundary Transition): \(\frac{\arctan((T-\gamma)/a) + \arctan((T+\gamma)/a)}{2a T}\).
3. \(|\gamma| \gg T\) (Outer Tail): \(J_T \sim \frac{1}{\gamma^2 - T^2}\).

## 42.3 Cofinal Limit Independence Countermodel
For \(f(H, T) = H / T\), for any fixed \(H < \infty\), \(\lim_{T\to\infty} f(H, T) = 0\). However, for proportional cofinal schedule \(H(T) = cT\) (\(c \ne 0\)), \(f(cT, T) = c \ne 0\) for all \(T \ne 0\).
Proved in Lean 4 with Mathlib `Filter.Tendsto` and elementary characterizations (`tendsto_cofinal_fixed_zero`, `not_tendsto_cofinal_diagonal_zero`, `finite_sum_tendsto_interchange`, `cofinal_sequence_fixed_limit_zero`, `cofinal_diagonal_not_tendsto_zero`, `cofinal_sequence_diagonal_witness`, `cofinal_schedule_distinct_from_fixed_limit`):
\[
\forall H,\ \operatorname{Tendsto}\left(n \mapsto \frac{H}{n+1}\right)\ \text{atTop}\ (\mathcal N(0)) \centernot\implies \operatorname{Tendsto}\left(n \mapsto \frac{n+1}{n+1}\right)\ \text{atTop}\ (\mathcal N(0)).
\]

## 42.4 Exact Radial Response Coefficient
For an on-line multiplicity-two fibre \(Z_0(z) = \frac{4z}{z^2+\gamma^2}\) replaced by an off-line quartet \(Z_\delta(z) = \frac{4z(z^2+\gamma^2-\delta^2)}{(z^2+\gamma^2-\delta^2)^2+4\delta^2\gamma^2}\):
\[
D_\gamma(z) := \lim_{\delta\to 0} \frac{Z_\delta(z) - Z_0(z)}{\delta^2} = \frac{4z(z^2-3\gamma^2)}{(z^2+\gamma^2)^3}.
\]
The leading variation of the windowed difference \(\Delta S_W = \int W_T(t) (|A-Z_\delta|^2 - |A-Z_0|^2) dt\) is:
\[
\boxed{\Delta S_W(\sigma, \gamma, \delta, T) = \delta^2 C_W(\sigma, \gamma, T) + O(\delta^4),}
\]
where
\[
\boxed{C_W(\sigma, \gamma, T) = -2\Re \int_{\mathbb R} W_T(t) F_0(t) \overline{D_\gamma(\sigma - 1/2 + it)} dt.}
\]
Algebraic numerators verified in Lean 4 over \(\mathbb C\) and \(\mathbb R\) (`complex_radial_defect_difference_numerator`, `complex_radial_second_order_numerator_decomposition`).

## 42.5 Certified Arb Ball Witness and Candidate Classification Matrix
1. **Fejér Witness WIT-02 (Rigorous Arb Ball Certificate)**:
   For \(\sigma=5.0, \gamma=14.0, \delta=0.49, T=16.8\), outward-rounded Arb ball Riemann integration directly across the complete symmetric compact support \([-16.8, 16.8]\) with 50,000 subintervals encloses:
   \[
   \Delta S_{\text{Fejér}} \in [-1.89473 \times 10^{-4}, -1.54203 \times 10^{-4}] \subset (-\infty, 0).
   \]
   Status: `CERTIFIED_NEGATIVE_ARB_BALL`.
2. **Numerical Evidence Witnesses (WIT 1, 3, 4)**:
   - Rectangular (\(\sigma=2.0, \gamma=14.0, \delta=0.1, T=2.8\)): \(\Delta S_W \approx -5.9067 \times 10^{-7}\) (estimated error \(\pm 1.0 \times 10^{-154}\)).
   - Abel-Poisson (\(\sigma=1.01, \gamma=21.0, \delta=0.49, T=1.05\)): \(\Delta S_W \approx -3.4414 \times 10^{-6}\) (estimated error \(\pm 2.0 \times 10^{-6}\)).
   - Gaussian (\(\sigma=1.01, \gamma=14.0, \delta=0.49, T=1.4\)): \(\Delta S_W \approx -7.2473 \times 10^{-5}\) (estimated error \(\pm 2.0 \times 10^{-19}\)).
   Status: `NUMERICAL_EVIDENCE_NEGATIVE`.
3. **Candidate Classification Matrix**:
   - Raw finite Fejér window response: `FAIL_RADIAL_POSITIVITY`.
   - Every zero-independent additive scalar subtraction of that finite Fejér response: `FAIL_RADIAL_POSITIVITY`.
   - Full infinite/cofinal CMSA-1 & CMSA-2 functionals: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
   - Finite algebraic four-term quadratic expansion: `FINITE_IDENTITY_PROVED_G4_OPEN`.
   - Grade coordinate dilation: `GRADE_COORDINATE_REDUNDANT`.
   - `CERTIFIED_NEGATIVE_ARB_BALL`: strictly an evidence/certificate status for WIT-02, never a final candidate classification.
   - **Proved Obstruction Class**: Any candidate family containing the stated finite Fejér functional and modified only by a zero-independent additive scalar reference fails unconditional radial positivity. This does not cover non-additive operators, different pairings, or the complete infinite/cofinal limit.

## 42.6 Proved Absolutely Convergent \(\ell^1\) Dirichlet-Series Mean-Square Lemma
For complex coefficients with \(\sum_{n=1}^\infty |a_n| < \infty\) (including \(a_n = \Lambda(n)n^{-\sigma}, \sigma > 1\) since \(\Lambda(n) \le \log n\)):
1. **Finite Identity**: \(\frac{1}{2T}\int_{-T}^T |\sum_{n=1}^N a_n n^{-it}|^2 dt = \sum_{n=1}^N |a_n|^2 + \sum_{1\le m \ne n \le N} a_m \overline{a_n} \frac{\sin(T\log(n/m))}{T\log(n/m)}\).
2. **Fixed-\(N\) Limit**: For fixed \(N\), off-diagonal terms vanish as \(T \to \infty\).
3. **Uniform Tail**: \(\|P - P_N\|_\infty \le \sum_{n>N} |a_n| =: \varepsilon_N \implies |\|P\|_T^2 - \|P_N\|_T^2| \le 2\varepsilon_N \sum |a_n|\) uniformly in \(T\).
4. **Interchange**: \(\lim_{T\to\infty} \frac{1}{2T}\int_{-T}^T |P(\sigma+it)|^2 dt = \sum_{n=1}^\infty |a_n|^2\).
This internal proof replaces all external Carlson (1914) dependency labels.

## 42.7 Additive-Reference Invariance No-Go Theorem
Let \(S_W(Z) = \int W_T(t) |A(t) - Z(t)|^2 dt\). For any scalar reference term \(R_W(A)\) independent of \(Z, \delta, \gamma\):
\[
\boxed{(S_W(Z_\delta) - R_W(A)) - (S_W(Z_0) - R_W(A)) \equiv S_W(Z_\delta) - S_W(Z_0).}
\]
Consequently, a divisor-independent additive scalar subtraction cannot alter the raw radial difference. It proves that the additive class shares identically whatever sign behaviour the raw functional exhibits. Formally proved in Lean 4 (`RiemannScope.additive_reference_subtraction_invariance`).

## 42.8 Conditional Hypotheses for Integrated Pointwise Expansions
The integrated leading variation \(\Delta S_W = \delta^2 C_W + O(\delta^4)\) is **conditional** on the following four mathematical hypotheses being established for the specified window and domain:
1. **Window Integrability**: \(W_T(t) \ge 0\) with \(W_T \in L^1(\mathbb R) \cap L^\infty(\mathbb R)\) and \(\int_{\mathbb R} W_T(t) dt = 1\).
2. **Denominator Separation**: For all \(\delta \in [0, \delta_0]\) with \(\delta_0 < a = \sigma - 1/2\), the denominators of \(Z_\delta(a+it)\) are separated from zero uniformly: \(|a \pm \delta + i(t \pm \gamma)| \ge a - \delta_0 > 0\).
3. **Uniform Domination**: The Taylor remainder function \(R_4(t, \delta) = \delta^{-4} (|A-Z_\delta|^2 - |A-Z_0|^2 + 2\delta^2 \Re(F_0 \overline{D_\gamma}))\) satisfies \(|R_4(t, \delta)| \le g(t)\) for all \(\delta \in [0, \delta_0]\), where \(g \in L^1(\mathbb R, W_T(t)dt)\).
4. **Legitimacy of Limit Interchange**: Under hypotheses 1–3, the Dominated Convergence Theorem justifies exchanging the limit \(\delta \to 0\) and the integral, establishing \(\lim_{\delta\to 0} \frac{\Delta S_W}{\delta^2} = C_W(\sigma, \gamma, T)\).

## 42.9 Finite Dirichlet-Polynomial Algebraic Identities, Schedule Covariance, and Subcritical Norm Bounds in Lean 4
Formalized in `formal/RiemannScope/ArithmeticBridge.lean`:
1. `complex_finset_sum_mul_star`: \((\sum_{i \in s} b_i) \cdot \overline{(\sum_{j \in s} b_j)} = \sum_{i \in s} \sum_{j \in s} b_i \overline{b_j}\).
2. `complex_finset_normSq_eq_double_sum_re`: \(\operatorname{normSq}(\sum_{i \in s} b_i) = \Re(\sum_{i \in s} \sum_{j \in s} b_i \overline{b_j})\).
3. `abstract_finite_kernel_decomposition`: \((\sum_{i \in s} \sum_{j \in s} K(i, j)) = (\sum_{i \in s} b_i) \cdot \overline{(\sum_{j \in s} b_j)}\) under hypothesis \(K(i, j) = b_i \overline{b_j}\).
4. `linear_operator_finite_double_sum_interchange`: \(L(\sum_{i \in s} \sum_{j \in s} K(i, j)) = \sum_{i \in s} \sum_{j \in s} L(K(i, j))\) for additive maps \(L : \mathbb C \to+ \mathbb C\).
5. `abstract_windowed_kernel_expansion`: \(L(\operatorname{normSq}(\sum_{i \in s} b_i)) = L((\sum_{i \in s} \sum_{j \in s} K(i, j)).\text{re})\).
6. `linear_schedule_grade_covariant`: \(\forall c, \tau\), \(H_c(T) = cT\) is discrete grade-covariant (\(H_c(\tau T) = \tau H_c(T)\)).
7. `grade_covariant_schedule_nonuniqueness`: Grade covariance alone does NOT uniquely select a schedule; for \(c_1 \ne c_2\), \(H_{c_1}\) and \(H_{c_2}\) are covariant and distinct for all \(T > 0\).
8. `periodic_modulated_schedule_covariant`: Periodic modulation in \(\log_\tau T\) preserves grade covariance.
9. `exact_remainder_cancellation`: \(R = F - Z \implies Z + R = F\) identically.
10. `functional_decomposition_independence`: \(\forall f, f(Z + R) = f(F)\) whenever \(R = F - Z\).
11. `complex_squared_norm_difference_expansion`: \(Q(F, \Delta) = \operatorname{normSq}(F+\Delta) - \operatorname{normSq}(F) = \operatorname{normSq}(\Delta) + 2\Re(F\bar\Delta)\).
12. `complex_squared_norm_difference_background_subtraction`: \(Q(F, \Delta) - Q(G, \Delta) = 2\Re((F-G)\bar\Delta)\).
13. `complex_squared_norm_difference_not_background_independent`: Counterexample \(F=1, G=-1, \Delta=1 \implies Q(1, 1)=3 \ne -1=Q(-1, 1)\).
14. `fixed_finite_energy_scaling_zero`: For any constant \(E \in \mathbb R\), \(\lim_{T\to\infty} \left|\frac{E}{2T}\right| = 0\).
15. `subcritical_norm_response_bound_vanishes`: Pointwise/bound lemma establishing that if \(|V| \le x^2/2 + C|x|\) for \(C \ge 0\), then \(|V| < \varepsilon\) whenever \(|x| \le 1\) and \(|x| < \varepsilon / (1/2 + C)\).
16. `subcritical_norm_response_tendsto_zero`: Mathlib `Filter.Tendsto` theorem establishing that for sequence \(x_n \to 0\) and \(C \ge 0\), any sequence \(|V_n| \le x_n^2/2 + C|x_n|\) converges to 0.
17. `resolvent_difference_rational_identity`: \(1/(w-\delta) - 1/w = \delta / (w(w-\delta))\) for \(w \ne 0, w-\delta \ne 0\).
18. `resolvent_reflection_pair_cancellation`: \((1/(w-\delta) - 1/w) + (1/(w+\delta) - 1/w) = 2\delta^2 / (w(w^2-\delta^2))\) for \(w \ne 0, w \pm \delta \ne 0\).
19. `subcritical_norm_contrapositive`: \(\neg \operatorname{Tendsto} V \operatorname{atTop} (\mathcal N 0) \implies \neg \operatorname{Tendsto} x \operatorname{atTop} (\mathcal N 0)\).
20. `not_tendsto_zero_subsequential_lower_bound`: \(\neg \operatorname{Tendsto} x \operatorname{atTop} (\mathcal N 0) \implies \exists \varepsilon > 0, \forall N, \exists n \ge N, |x_n| \ge \varepsilon\).

## 42.10 Schedule Covariance, Background Dependence, and Fixed-Finite Invisibility
### Origin Coordinate Dilation and Schedule Covariance Law
In Transcendental Continuation (TC), the project uses **origin coordinate dilation**:
\[
s_K = \tau^K s, \quad c_K = \frac{\tau^K}{2}, \quad z_K = s_K - c_K = \tau^K\left(s - \frac{1}{2}\right).
\]
On the imaginary axis, ordinate dilates as \(t_K = \tau^K t \implies t' = \tau t\). Scale covariance between window width \(T\) and height cutoff \(H\) requires:
\[
\boxed{H(\tau T) = \tau H(T), \quad \tau = 2\pi.}
\]
- **General Solution (Paper Proved)**: \(H(T) = T \cdot q(\log_\tau T)\) with \(q : \mathbb R \to (0, \infty)\) 1-periodic.
- **Asymptotic Limit Collapse (Paper Proved)**: If \(\lim_{T\to\infty} H(T)/T\) exists and \(\tau > 1\), \(H(T) = cT\).
- **Selection Condition**: Unproved heuristic note; omitted zero bounds do not force \(c \ge 1\) by proved estimate alone.
- **Falsified Premise**: *"Bilateral discrete grade covariance uniquely determines the cofinal schedule."*

### Background-Dependence Theorem & Scope of Additive Invariance
For complex-valued background \(F\) and perturbation \(\Delta\), the squared-norm variation is:
\[
Q(F, \Delta) = |F + \Delta|^2 - |F|^2 = |\Delta|^2 + 2\Re(F\bar\Delta).
\]
For two distinct backgrounds \(F\) and \(G\), \(Q(F, \Delta) - Q(G, \Delta) = 2\Re((F-G)\bar\Delta)\).
The theorem `additive_reference_subtraction_invariance` applies only to outer scalar subtractions \((S - R)\) and does NOT apply to backgrounds placed inside squared norms.
**Correction**: The claim that Case B automatically reduces to the certified finite Fejér response is withdrawn; the sign of \(Q(F_0, \Delta)\) depends explicitly on the completed-function background \(F_0\).

### Fixed Finite Perturbation Invisibility Theorem
**Proof Status**: `PROVED / EXACT / PARTIALLY_FORMALIZED`
- **Paper Proof**: Complete deductive analytic derivation (§42.10).
- **Formalized Lean 4 Component**: `RiemannScope.fixed_finite_energy_scaling_zero` formalizes the scalar sequence limit \(E/(2T) \to 0\) (`FORMALLY_PROVED COMPONENT`).
- **Python Verification**: `math_core.verify_fixed_finite_perturbation_invisibility` evaluates numerical quadrature of finite prime Dirichlet polynomial truncations across sampled windows (`NUMERICAL_EVIDENCE`).

Let \(\sigma > 1\) and \(P_\sigma(t) = \sum_{n=2}^\infty \Lambda(n) n^{-\sigma-it}\). Let \(\Delta(t) = \sum_{j=1}^N \frac{c_j}{a_j + i(t-\gamma_j)}\) with \(N < \infty, a_j > 0\).
Then \(\Delta \in L^2(\mathbb R)\) and:
\[
\lim_{T\to\infty} \frac{1}{2T} \int_{-T}^T \left( |P_\sigma(t) - \Delta(t)|^2 - |P_\sigma(t)|^2 \right) dt = 0.
\]
A fixed finite divisor perturbation cannot produce a nonzero normalized infinite mean response.

### Perturbation Semantics and Candidate Classifications
- **Case A (Recomputed Remainder)**: \(Z_{H,\delta} + R_{H,\delta} \equiv F_\delta\) (collapses algebraically). Classification: `FAIL_LIMIT_ORDER_DEPENDENCE`.
- **Case B (Fixed Finite Perturbation)**: \(Z_{H,\delta} + R_{H,0} = F_0 + \Delta\) (vanishes under infinite mean). Classification: `FAIL_LIMIT_ORDER_DEPENDENCE`.
- **Case C (Growing / Cofinal Perturbation \(\Delta_{H(T)}\))**: Non-fixed perturbation with \(H(T) \to \infty\). Classification: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.
- **Raw Finite Fejér Response**: Retained as `FAIL_RADIAL_POSITIVITY`.

## 42.11 Resolvent Algebra, Subcritical Norm Growth, and the Transcendental Continuation Activation Subgate
### Exact Resolvent Algebra and Reflection Pair Cancellation
For \(a = \sigma - 1/2 > 0, w = a + i(t-\gamma)\), and \(a - \delta > 0\):
\[
\boxed{\int_{-\infty}^\infty |r_\delta(t)|^2 dt = \frac{\pi \delta^2}{a(a-\delta)(2a-\delta)} = \frac{\pi \delta^2}{2a^3} + \mathcal O(\delta^3),}
\]
\[
\boxed{r_\delta(t) + r_{-\delta}(t) = \frac{2\delta^2}{w(w^2-\delta^2)}.}
\]
Exact first-order cancellation suppresses symmetric functional-reflection pairs to \(\mathcal O(\delta^2)\).

### Subcritical Norm Response Vanishing ($o(\sqrt{T})$ Threshold)
**Proof Status**: `PROVED / EXACT / PARTIALLY_FORMALIZED`
- **Paper Proof**: Complete deductive analytic derivation via Cauchy-Schwarz.
- **Formalized Lean 4 Component**: `RiemannScope.subcritical_norm_response_bound_vanishes`, `RiemannScope.subcritical_norm_response_tendsto_zero`, `RiemannScope.subcritical_norm_contrapositive`, `RiemannScope.not_tendsto_zero_subsequential_lower_bound` (`FORMALLY_PROVED COMPONENT`).
- **Python Evaluator**: `math_core.verify_cofinal_subcritical_norm_bound` evaluates the finite-sample bound (`NUMERICAL_EVIDENCE`).

Let \(T > 0\), and let \(P_T, \Delta_T \in L^2(-T, T)\) with \(\frac{1}{2T} \|P_T\|_{L^2(-T, T)}^2 \le M < \infty\) for all large \(T\).
Define the normalized mean-square variation:
\[
V_T = \frac{1}{2T} \int_{-T}^T \left( |P_T(t) - \Delta_T(t)|^2 - |P_T(t)|^2 \right) dt = \frac{\|\Delta_T\|^2}{2T} - \frac{1}{T}\Re\langle P_T, \Delta_T\rangle.
\]
Let \(x_T = \frac{\|\Delta_T\|_{L^2(-T, T)}}{\sqrt{T}}\). Then:
\[
\boxed{|V_T| \le \frac{1}{2} x_T^2 + \sqrt{2M} x_T.}
\]
In particular, if \(\|\Delta_T\|_{L^2(-T, T)} = o(\sqrt{T})\) as \(T \to \infty\) (i.e. \(x_T \to 0\)), then \(\lim_{T\to\infty} V_T = 0\).

**Contrapositive (Subsequential Non-Vanishing Consequence)**:
\[
\boxed{\limsup_{T\to\infty} |V_T| > 0 \implies \frac{\|\Delta_T\|_{L^2(-T, T)}}{\sqrt{T}} \not\to 0 \iff \exists \varepsilon > 0, T_k \to \infty \text{ s.t. } \|\Delta_{T_k}\| \ge \varepsilon\sqrt{T_k}.}
\]
*Distinction*: Does NOT imply an eventual \(\Omega(\sqrt{T})\) lower bound (Counterexample: \(x_n = 1\) for even \(n\), \(1/(n+1)\) for odd \(n\)).

### Withdrawal of the Riemann–von Mangoldt Norm Asymptotic
The assertion \(\|\Delta_{H(T)}\| \sim \sqrt{T \log T}\) based on Riemann–von Mangoldt counting is **WITHDRAWN** due to:
1. On-line zeros have \(\delta_j = 0\) and contribute \(r_j = 0\);
2. Unknown count and distribution of off-line zeros (could be 0, 4, finite, or sparse);
3. Defect variability across mode ordinates;
4. Off-diagonal spectral interference;
5. First-order reflection cancellation (\(r_\delta + r_{-\delta} = \mathcal O(\delta^2)\));
6. Finite interval boundary mode truncation on \([-T, T]\).

### Finite Off-Line Quartet Invisibility & Zero-Rigidity Failure
For any finite off-line zero configuration (such as a single off-line quartet \(\{1/2 \pm \delta \pm i\gamma\}\)), \(\Delta_{H(T)}(t) = \Delta(t) \in L^2(\mathbb R)\) for \(H(T) \ge \gamma\), giving \(\|\Delta_{H(T)}\| = \mathcal O(1) = o(\sqrt{T}) \implies V_T \to 0\).
The normalized mean functional cannot distinguish a finite off-line quartet from RH.
- Fixed / Subcritical Families: `FAIL_LIMIT_ORDER_DEPENDENCE`.
- Growing Cofinal Families: `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`.

### The Transcendental Continuation Activation Theorem (Earliest Open Subgate)
\[
\boxed{\exists \rho \text{ with } \delta_\rho \ne 0 \implies \limsup_{T\to\infty} \frac{\|\Delta^{TC}_T\|_{L^2(-T, T)}}{\sqrt{T}} > 0.}
\]
Requires 8 structural specifications (grade combination operation, non-double-counting proof, grade weights, bilateral convergence over \(K \in \mathbb Z\), height truncation interaction, shift covariance, arithmetic representation, and non-pullback proof).
Designated as the **earliest open subgate** logically preceding \(E_T - C_T\) asymptotic evaluation.

