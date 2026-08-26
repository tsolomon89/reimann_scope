# Lean Formalization Plan

## 0. Role of Lean

Lean is the proof firewall for `reimann_scope`.

The interactive application and numerical experiments are used to discover, falsify, and refine candidate mathematical statements.

Lean is used to ensure that:

- exact coordinate claims really follow;
- transcendence assumptions are not silently strengthened;
- invalid implications are not smuggled into the proof path;
- a retained candidate coherence law is separated from the radial-rigidity implication it still needs.

Do not begin by attempting to formalize all of analytic number theory.

---

# 1. Initial formal directory

Recommended:

```text
formal/
    lakefile.toml
    lean-toolchain
    RiemannScope/
        Basic.lean
        Grade.lean
        TranscendentalContinuation.lean
        TauLattice.lean
        ZeroWorldline.lean
        RadialLeaf.lean
        ZeroCharacter.lean
        SymmetricDefect.lean
        Contradiction.lean
        README.md
```

Use Mathlib.

Names may be adjusted to fit Mathlib conventions.

---

# 2. Formal status classes

The repo should distinguish:

```text
FORMALIZED
PAPER_PROVED
NUMERICALLY_VALIDATED
OBSERVED
CONJECTURAL
FALSE
CIRCULAR
KNOWN_INSUFFICIENT
```

Lean success can upgrade a suitable exact claim to `FORMALIZED`.

Finite numerical agreement cannot do so.

---

# 3. Phase 1 — generic scale algebra

Formalize for positive real base/scale.

For

\[
A>0,
\]

prove basic origin dilation:

\[
T_A(s)=As.
\]

For

\[
s=\frac12+\delta+i\gamma,
\]

prove:

\[
\boxed{
T_A(s)
=
\frac A2+A\delta+iA\gamma.
}
\]

Formalize:

\[
\Re(T_A(s))=\frac A2
\]

when

\[
\Re(s)=\frac12.
\]

No zeta theorem is needed.

---

# 4. Phase 2 — centered dilation

Define:

\[
C_A(s)
=
\frac12+A\left(s-\frac12\right).
\]

Prove:

\[
\boxed{
C_A\left(
\frac12+\delta+i\gamma
\right)
=
\frac12+A\delta+iA\gamma.
}
\]

Prove that the critical line is fixed:

\[
\Re(s)=\frac12
\Longrightarrow
\Re(C_A(s))=\frac12.
\]

This should remain explicitly separate from origin dilation.

---

# 5. Phase 3 — tau-grade group

Define:

\[
\tau=2\pi.
\]

For real

\[
k,
\]

define:

\[
a(k)=\tau^k.
\]

Prove:

\[
a(0)=1,
\]

\[
a(k_1+k_2)=a(k_1)a(k_2),
\]

\[
a(-k)=a(k)^{-1}.
\]

Specialize integer grade:

\[
A_K=\tau^K,
\qquad
K\in\mathbb Z.
\]

Prove bilateral inverse relation:

\[
\boxed{
A_KA_{-K}=1.
}
\]

---

# 6. Phase 4 — transcendental continuation as a generic coordinate family

Before depending on formalized zeta infrastructure, define a generic function

\[
f:\mathbb C\to\mathbb C
\]

and its tau continuation:

\[
\boxed{
F_\tau(s,k)
=
f(\tau^{-k}s).
}
\]

Prove the exact covariance:

\[
\boxed{
F_\tau(\tau^k u,k)=f(u).
}
\]

This captures the coordinate mathematics independently of zeta.

Then, if Mathlib's zeta definitions are suitable, specialize to zeta.

---

# 7. Phase 5 — generic zero worldline

Assume:

\[
f(\rho)=0.
\]

Prove:

\[
\boxed{
F_\tau(\tau^k\rho,k)=0.
}
\]

Define worldline:

\[
W_\rho(k)=\tau^k\rho.
\]

This should be formalized before introducing any RH-specific statement.

---

# 8. Phase 6 — critical surface and radial coordinate

Define:

\[
\boxed{
R_\tau(s,k)
=
\tau^{-k}\Re(s)-\frac12.
}
\]

For

\[
\rho=\frac12+\delta+i\gamma,
\]

prove:

\[
\boxed{
R_\tau(\tau^k\rho,k)=\delta.
}
\]

This is one of the highest-value initial formal theorems.

Also prove:

\[
\delta=0
\Longleftrightarrow
W_\rho(k)
\text{ lies on }
\Re(s)=\tau^k/2
\]

for every \(k\).

This formalizes radial-leaf invariance without assuming RH.

---

# 9. Phase 7 — arithmetic tau lattices

Define:

\[
L_K=\{\tau^K n:n\in\mathbb Z\}.
\]

Use a Mathlib theorem establishing transcendence of \(\pi\), or isolate that theorem as an explicit dependency if theorem naming/library availability differs.

From transcendence of \(\tau=2\pi\), prove for

\[
K\neq J:
\]

\[
\boxed{
L_K\cap L_J=\{0\}.
}
\]

Do not formalize the false statement that the coordinate spaces are non-isomorphic.

Where useful, formalize the scaling bijection between lines.

---

# 10. Phase 8 — rational-grade lattice refinement

If practical, formalize:

\[
r,q\in\mathbb Q,
\qquad
r\neq q
\]

implies

\[
\boxed{
\tau^r\mathbb Z
\cap
\tau^q\mathbb Z
=
\{0\}.
}
\]

This requires a clean formal treatment of rational real powers and the fact that a nonzero rational power of a transcendental positive real remains transcendental.

If Mathlib makes this disproportionately expensive, record it as `PAPER_PROVED` and defer formalization.

Do not block the core project on this refinement.

---

# 11. Phase 9 — generic-base zero character

Prefer a generic base

\[
b>1
\]

first.

Define:

\[
q_b(\rho)
=
\exp\left(
(\rho-\frac12)\log b
\right).
\]

For

\[
\rho=\frac12+\delta+i\gamma,
\]

prove:

\[
\boxed{
|q_b(\rho)|=b^\delta.
}
\]

For integer \(K\), prove:

\[
\boxed{
|q_b(\rho)^K|
=
b^{K\delta}.
}
\]

Then specialize to

\[
b=\tau.
\]

This formal ordering prevents generic scale facts from being mislabeled tau-specific.

---

# 12. Phase 10 — symmetric grade defect

For:

\[
\rho_\pm
=
\frac12\pm\delta+i\gamma,
\]

\[
\rho_0
=
\frac12+i\gamma,
\]

define:

\[
D_K=q_+^K+q_-^K-2q_0^K.
\]

Prove:

\[
\boxed{
D_K
=
2e^{iK\gamma\log\tau}
[
\cosh(K\delta\log\tau)-1
].
}
\]

Then:

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

This is a calibration theorem, not an RH theorem.

---

# 13. Phase 11 — abstract contradiction skeleton

Do not initially formalize the missing coherence law as an axiom about zeta.

Instead formalize the logic abstractly.

Let:

```text
Zero
radial : Zero → ℝ
coherent : Set Zero → Prop
```

or an equivalent structure.

Formalize:

> If a spectrum satisfies a property that implies all of its members have the same radial value, and the spectrum contains one member with radial value zero, then every member has radial value zero.

Then formalize contradiction form:

> If the same spectrum contains a member with nonzero radial value, contradiction follows.

This theorem should make the missing mathematical hypothesis explicit.

---

# 14. Candidate radial-rigidity interface

Create an abstract theorem interface such as:

```text
TranscendentalCoherence spectrum → SingleRadialLeaf spectrum
```

but do **not** instantiate it for zeta until the theorem is actually derived.

The codebase must make it impossible to mistake the abstract implication skeleton for a proof that zeta satisfies the premise.

---

# 15. What Lean should make impossible to hide

The formal architecture should expose the failure of the following implications:

\[
\text{coordinate covariance}
\not\Rightarrow
\text{RH},
\]

\[
\text{arithmetic lattice noncoincidence}
\not\Rightarrow
\text{zeta zero-set noncoincidence},
\]

\[
\text{global function changes after synthetic zero movement}
\not\Rightarrow
\text{all other zeros move},
\]

\[
\text{bilateral grade amplification}
\not\Rightarrow
\text{radial impossibility},
\]

\[
\text{finite grade tests}
\not\Rightarrow
\text{infinite-grade rigidity}.
\]

These need not all be named theorems.

They must not appear as assumptions disguised as definitions.

---

# 16. When to formalize actual zeta/xi mathematics

Do not build a huge formal analytic-number-theory layer merely because the project concerns RH.

Move deeper only when there is a specific retained statement, for example:

\[
\boxed{
I_K=C
}
\]

or

\[
\boxed{
F(I_{K-1},I_K,I_{K+1})=0.
}
\]

Then:

1. define the exact zeta/xi object;
2. import/prove only the dependencies required;
3. prove the coherence identity;
4. separately prove or refute radial rigidity.

If Mathlib lacks a required theorem, document the missing dependency rather than silently axiomatizing the desired result.

---

# 17. Numeric/Lean handshake

The numerical application should export theorem-facing candidate statements in human-readable form.

A useful artifact may include:

```text
candidate name
exact mathematical definition
observed parameter domain
controls passed
counterexamples tested
proposed theorem statement
known missing assumptions
```

Lean should not ingest raw experimental output as proof.

The experiment identifies what to formalize.

---

# 18. CI integration

The formal layer should run independently:

```bash
cd formal
lake build
```

CI may contain separate jobs:

```text
python-tests
lean-build
```

Failure of Lean does not silently downgrade to a numerical check.

---

# 19. Initial definition of done

The first Lean integration is complete when:

1. generic origin dilation is formalized;
2. centered dilation is formalized;
3. tau-grade group identities are formalized;
4. generic transcendental-continuation coordinate covariance is formalized;
5. generic zero worldline is formalized;
6. radial invariant is formalized;
7. integer tau-lattice noncoincidence is formalized or its exact transcendence dependency is clearly isolated;
8. generic-base zero-character modulus is formalized;
9. symmetric grade defect is formalized;
10. the abstract radial-rigidity contradiction skeleton is formalized;
11. no unproved zeta-specific coherence theorem is encoded as an axiom.

---

# 20. Long-term proof target

The eventual formal target is:

\[
\boxed{
\text{Zeta Transcendental Coherence}
\Longrightarrow
\text{Single Radial Leaf}
\Longrightarrow
\text{RH}.
}
\]

At present, only the logical skeleton and prerequisite coordinate/grade identities are candidates for formalization.

The first implication remains the central mathematical discovery problem.

---

# 21. Phase 12 — Radial-defect quotient and involution pairing firewalls

Formalize finite algebraic firewall theorems in Lean 4 without introducing unproved infinite analytic axioms:

1. **Rational involution pairing identity** (`kappa1_involutionSharp_eq_of_im_ne_zero`):
   For \(\kappa_1(z,w) = \frac{4zw}{(z+w)^2} - 1\) and \(z^\# = -\bar z = -\delta + i\gamma\), prove in \(\mathbb C\):
   \[
   \kappa_1(z, z^\#) = \frac{\delta^2}{\gamma^2}, \qquad z = \delta + i\gamma, \ \gamma \ne 0.
   \]
2. **Finite trace non-negativity and vanishing** (`list_sum_nonneg_eq_zero_iff`):
   For any finite list \(l\) of non-negative displacement ratios \(r_n = \delta_n^2 / \gamma_n^2 \ge 0\), prove:
   \[
   l.\mathrm{sum} = 0 \iff \forall x \in l,\ x = 0.
   \]
3. **Finite determinant product equivalence** (`list_prod_one_plus_nonneg_eq_one_iff`):
   For any finite list \(l\) of non-negative displacement ratios \(x \ge 0\), prove:
   \[
   (l.\mathrm{map}(1 + \cdot)).\mathrm{prod} = 1 \iff \forall x \in l,\ x = 0.
   \]

Do not formalize infinite Hadamard products, infinite Fredholm determinants, or explicit-formula arithmetic representations as axioms. Record infinite analytic convergence as an explicit future formalization obligation.

---

# 22. Phase 13 — Arithmetic Radial Bridge, Weighted Positivity, and Covariance Countermodel

Formalize exact coordinate centering, weighted sum positivity, the covariance countermodel, and the conditional bridge interface in Lean 4:

1. **Grade-Centering Geometry** (`RiemannScope.Grade`):
   - `gradeCenter (K : ℤ) : ℝ := integerGradeScale K / 2`
   - `centeredGradeCoord (K : ℤ) (s : ℂ) : ℂ := ⟨integerGradeScale K * s.re - gradeCenter K, integerGradeScale K * s.im⟩`
   - Theorem `centeredGradeCoord_eq_tau_pow_mul_z`:
     \[
     z_K = \tau^K(s - 1/2) \in \mathbb C.
     \]
2. **Arbitrary Finite-Family Weighted Positivity Firewall** (`list_weighted_sum_nonneg_eq_zero_iff`):
   For any strictly positive weight list \(w\) and non-negative defect list \(l\) of matching length:
   \[
   (w \odot l).\mathrm{sum} = 0 \iff \forall x \in l,\ x = 0.
   \]
3. **Covariance Countermodel** (`offlineQuartet`, `covariance_countermodel_offline_compatible`):
   Prove that an abstract off-line quartet \(\mathcal Q_{\delta,\gamma} = \{1/2 \pm \delta \pm i\gamma\}\) (\(\delta \ne 0\)) is closed under functional reflection \(s \mapsto 1-s\) and complex conjugation \(s \mapsto \bar s\), demonstrating that reflection symmetries and coordinate covariance are jointly compatible with off-line zeros (\(\delta \ne 0\)).
4. **Conditional Arithmetic Radial Bridge Interface** (`ConditionalArithmeticRadialBridge`):
   Structure containing zero defects, non-negative bounds, arithmetic evaluator, spectral evaluator, bridge identity \(\forall K, \mathfrak A_K = X\), and arithmetic vanishing anchor \(\exists K, \mathfrak A_K = 0\).
   Theorem `ConditionalArithmeticRadialBridge.all_defects_zero`: prove that any valid instance forces all represented defects to vanish (\(r_j = 0 \implies \delta_j = 0\)).

---

# 23. Phase 14 — Arbitrary Finite Curvature and Separated Signal Bridge

Formalize arbitrary finite curvature decomposition, nonnegativity, and zero-rigidity in Lean 4:

1. **Arbitrary Real-List Pairwise Squared-Sum Decomposition** (`list_pairs_sq_sum_eq`):
   For any real list \(l\) of length \(N\):
   \[
   \sum_{i,j} (d_i + d_j)^2 = 2N \sum d_i^2 + 2\left(\sum d_i\right)^2.
   \]
2. **Symmetric Curvature Reduction** (`list_pairs_sq_sum_symmetric`):
   When \(\sum d_i = 0\), \(\sum_{i,j} (d_i + d_j)^2 = 2N \sum d_i^2\).
3. **Unconditional Non-negativity and Rigidity** (`list_pairs_sq_sum_nonneg`, `list_pairs_sq_sum_eq_zero_iff`):
   Prove \(\sum_{i,j} (d_i + d_j)^2 \ge 0\), vanishing iff \(\forall x \in l, x = 0\).
4. **Conditional Separated Signal Bridge Interface** (`ConditionalSeparatedSignalBridge`):
   Prove `all_variances_zero`: any valid arithmetic-anchored separated signal bridge forces all represented radial variances to vanish.

---

# 24. Phase 15 — Universal Scale Dilation Invariance and Completed Log-Derivative

Formalize universal scale dilation cancellation and coordinate redundancy in Lean 4:

1. **Universal Scale Dilation Cancellation** (`generic_scale_dilation_cancellation`):
   For any strictly positive scale \(s > 0\) and function \(f\), with \(D_s(f)(u) := f(u/s) / s\):
   \[
   s D_s(f)(su) = f(u).
   \]
2. **Conditional Completed Logarithmic Derivative Decomposition** (`ConditionalCompletedLogDerivativeDecomposition`):
   Prove `coordinate_redundant`: the normalized dilated completed logarithmic derivative \(\tau^K D_K^\xi(\tau^K u) = \xi'/\xi(u)\) is strictly coordinate-redundant for all integer grades \(K \in \mathbb Z\).

---

# 25. Phase 16 — Gate G4 Windowed Expansion, Cofinal Limit Independence, and Conditional Regularized Bridge

Formalize Gate G4 windowed expansion identities, cofinal limit countermodels, and conditional regularized bridge rigidity in Lean 4:

1. **Finite Windowed Quadratic Expansion** (`finite_quadratic_expansion_identity`, `finite_quadratic_four_term_decomposition`):
   - Prove \((A - Z)^2 = A^2 - 2AZ + Z^2\).
   - Prove \((A - Z)^2 = A \cdot A - A \cdot Z - Z \cdot A + Z \cdot Z\).
2. **Cofinal Limit Independence Countermodel** (`cofinal_schedule_distinct_from_fixed_limit`):
   - For \(f(H, T) = H / T\), prove that \((c \cdot T) / T = c\) for all \(T \ne 0\).
   - Demonstrates that fixed-truncation limits \(\forall H, \lim_{T\to\infty} f(H, T) = 0\) do not imply cofinal limit vanishing \(\lim_{T\to\infty} f(H(T), T) = 0\).
3. **Conditional Gate G4 Regularized Bridge Interface** (`ConditionalG4RegularizedBridge`):
   - Structure modeling the passage of the finite CMSA expansion to an exact positive radial-defect functional.
   - Theorem `ConditionalG4RegularizedBridge.all_defects_zero`: prove that any valid regularized bridge with zero arithmetic anchor forces all represented zero defects to vanish (\(d_j = 0\)).


