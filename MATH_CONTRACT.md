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
2. **Missing Theorem Status**:
   - Inferring radial rigidity (\(\Delta\mathcal D_{\mathrm{rad}} = 0\)) from the projected-divisor defect remains an unproved theorem requiring a global arithmetic or spectral constraint.

## 36.5 Countermodel Controls and Epistemic Classification

1. **Structural Countermodels**:
   - Davenport–Heilbronn and Epstein zeta functions possess functional-equation reflection symmetry \(\delta \mapsto -\delta\) and exact coordinate covariance, yet possess off-line zeros.
   - They serve as structural countermodels demonstrating that functional symmetry and coordinate covariance alone are mathematically insufficient to exclude off-line zeros.
   - We do not claim their off-line zeros are caused by one isolated missing ingredient unless proved.
2. **Epistemic Classification**:
   - The finite second-order radial response construction is classified as an **exact finite synthetic sensitivity diagnostic**.
   - It validates the local quadratic Taylor fidelity (\(\mathcal O(\delta^2)\) relative error \(< 0.04\%\)), while finite NNLS compensation remains heterogeneous and dependent on the chosen test family.

