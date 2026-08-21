# Riemann Scope Rebuild Plan

## 0. Objective

Reconfigure the existing `reimann_scope` application around the canonical framework now defined in:

- `TRANSCENDENTAL_CONTINUATION.md`
- `RESEARCH_HYPOTHESIS.md`
- `MATH_CONTRACT.md`

The application should preserve correct existing functionality while changing its research ontology from:

```text
a zeta visualizer with several scale transforms
```

to:

```text
a transcendental-continuation instrument designed to search for
a zeta-specific coherence law that may imply radial rigidity.
```

The rebuild is not a greenfield rewrite unless the audit demonstrates that a smaller rewrite is safer than incremental modification.

---

# 1. Cold-reader success criterion

After reading the root docs, a new coding/research agent should be able to state:

> Riemann Scope studies the analytically continued zeta function as the native \(k=0\) slice of a \(\tau\)-generated extended \((s,k)\)-domain called transcendental continuation. Integer \(K\) values form canonical bilateral grades. Each nontrivial zero generates a zero worldline with an invariant normalized radial leaf. The proof search asks whether the simultaneous analytic/arithmetic constraints across the grade family permit more than one occupied radial leaf. The application uses exact controls, compression, actual cross-height comparison, and synthetic radial perturbation to discover or falsify the missing coherence/radial-rigidity theorem.

If an agent instead concludes merely:

> compare some scaled zeta plots

the rebuild has failed conceptually.

---

# 2. Documentation authority

The application must treat the root docs in this order:

1. `TRANSCENDENTAL_CONTINUATION.md`
2. `RESEARCH_HYPOTHESIS.md`
3. `RESEARCH_LEDGER.md`
4. `MATH_CONTRACT.md`
5. `TRANSCENDENTAL_COHERENCE_EXPERIMENT.md`
6. `EXPERIMENT_PROTOCOL.md`
7. `RIEMANN_MICROSCOPE_SPEC.md`
8. `DATA_PROVENANCE.md`
9. `LEAN_FORMALIZATION_PLAN.md`
10. `DECISIONS.md`
11. `REBUILD_PLAN.md`
12. `README.md`

The code must not infer mathematical semantics from old agent prompts.

---

# 3. Documentation cleanup

After the canonical docs are installed and verified:

- remove obsolete root coding-agent prompt documents from the live root;
- retain them through Git history;
- update `.agents` corpus maps and rules;
- remove references to `SPEC.md` if the actual canonical file is `RIEMANN_MICROSCOPE_SPEC.md`;
- update any stale description that says tau is merely an arbitrary scale slider;
- update any stale definition using real-valued `K` where the new contract requires real \(k\) and integer \(K\).

Do not delete valid historical decisions from `DECISIONS.md`.

---

# 4. Phase A — audit before modification

Before code changes:

1. run the entire current test suite;
2. inspect current canonical run index;
3. inventory current mathematical modules;
4. map every UI control to its mathematical operation;
5. identify where `k`, `K`, `A`, and scale are currently conflated;
6. identify where current transformed-zero logic assumes old semantics;
7. verify converter branch/remainder implementation;
8. verify current run artifacts still correspond to the code SHA recorded.

Record the audit before changing behavior.

Do not weaken valid tests to make the rebuild pass.

---

# 5. Phase B — introduce grade types

The code should represent semantic scale classes explicitly.

At minimum distinguish:

```text
ContinuousGrade(k)
IntegerTauGrade(K)
RationalTauGrade(q)
GenericScale(A)
```

The exact Python types may be dataclasses, tagged structures, or another simple representation.

Do not build an elaborate type system if a small explicit structure suffices.

Each grade object should be able to provide:

- symbolic expression;
- high-precision numeric scale;
- semantic type;
- inverse grade;
- display label.

---

# 6. Phase C — canonical transcendental module

Add or refactor a canonical module, likely:

```text
transcendental.py
```

Responsibilities:

- evaluate \(\tau\) at requested precision;
- compute scale from \(k,K,q\);
- define \(\mathcal Z_\tau(s,k)\);
- define \(\mathcal X_\tau(s,k)\) where used;
- map zero worldlines;
- compute critical-surface coordinate;
- compute absolute radial defect;
- compute normalized radial coordinate;
- generate Active Mathematics metadata.

No UI code should duplicate these formulas.

---

# 7. Phase D — preserve generic transforms

Keep existing explicit transform families:

- camera;
- height sampling;
- generic origin dilation;
- centered dilation;
- argument transform;
- kernel transform;
- anisotropic deformation.

Refactor only enough to make the new taxonomy unambiguous.

Transcendental continuation should call or share the canonical origin-dilation machinery rather than create another incompatible implementation.

---

# 8. Phase E — native \(k=0\) state

Default app startup should now explicitly report:

```text
TRANSCENDENTAL CONTINUATION GRADE: k = 0
NATIVE ANALYTIC SLICE
```

while still behaving exactly like the ordinary zeta application.

Regression requirement:

\[
\boxed{
\mathcal Z_\tau(s,0)=\zeta(s)
}
\]

to authoritative precision.

All existing native zeta behavior should remain intact.

---

# 9. Phase F — bilateral integer grade UI

Add canonical controls for:

\[
K\in\mathbb Z.
\]

Required:

- step backward;
- step forward;
- direct integer entry;
- return to \(K=0\);
- display \(\tau^K\);
- display reciprocal symmetry;
- support both positive and negative \(K\).

Do not implement integer grade merely as snapping a floating-point slider without preserving the exact integer semantic state.

---

# 10. Phase G — continuous and rational grades

Continuous mode:

\[
k\in\mathbb R.
\]

Use for:

- interpolation;
- animation;
- target-height compression.

Rational mode:

\[
q\in\mathbb Q.
\]

Use exact rational parsing for inputs such as:

```text
1/2
-3/2
7/4
```

Do not force rational grade through decimal conversion before forming the symbolic grade expression.

---

# 11. Phase H — symbolic versus numerical display

Every tau grade view should show:

```text
GRADE TYPE
EXACT SYMBOLIC SCALE
NUMERICAL SCALE
PRECISION
```

Example:

```text
INTEGER GRADE
K = -4
SCALE = τ^-4
NUMERIC = 0.000641...
AUDIT = 100 dps
```

This is a first-class requirement, not cosmetic copy.

---

# 12. Phase I — zero worldline engine

For a native zero \(\rho\), implement:

\[
\boxed{
s_\rho(k)=\tau^k\rho.
}
\]

Support:

- single selected zero;
- multiple selected zeros;
- integer-grade sample worldline;
- continuous worldline preview;
- actual/nontrivial zeros;
- synthetic perturbation worldlines kept separately.

Add direct tests against `MATH_CONTRACT.md`.

---

# 13. Phase J — critical surface and radial leaves

Implement:

\[
\boxed{
\Re(s)=\frac{\tau^k}{2}
}
\]

and

\[
\boxed{
R_\tau(s,k)
=
\tau^{-k}\Re(s)-\frac12.
}
\]

UI must show:

- active critical line;
- absolute radial displacement;
- normalized radial leaf.

For selected worldline, verify:

\[
R_\tau=\delta.
\]

Never infer one-leaf occupancy from this identity.

---

# 14. Phase K — worldline visualization

Add a simple visualization that makes the enlarged domain visible.

Preferred approach:

- preserve the current 2D domain plane as primary;
- add optional 3D worldline view with axes:
  - \(\Re(s)\);
  - \(\Im(s)\);
  - \(k\);
- display critical surface;
- display selected zero worldlines;
- allow finite grade-window selection.

Do not build an expensive 3D framework if Plotly's built-in graph objects suffice.

The view is explanatory and diagnostic.

---

# 15. Phase L — compression / expansion workflow

Add:

```text
Compress selected region to target height
Expand selected region
Set continuous k
Set integer K
```

For target-height mode:

- derive \(k\);
- show derived \(k\);
- show nearest integer \(K\);
- preserve the fact that this may not be a canonical integer grade.

Show before/after:

- zero height;
- critical-line coordinate;
- absolute radial defect;
- normalized radial leaf;
- complex path.

---

# 16. Phase M — arithmetic grade-line explanation

Implement a small optional educational/research card for:

\[
L_K=\tau^K\mathbb Z.
\]

It should state:

- infinitely many points on each line;
- same countable cardinality;
- scale isomorphism;
- distinct integer grades share only \(0\);
- this arithmetic fact does not automatically prove zero-worldline disjointness.

Do not spend major UI complexity on visualizing infinite arithmetic lines.

The purpose is to document the grade ontology.

---

# 17. Phase N — high-zero block data architecture

Refactor data access to support:

- low validation block;
- medium research block;
- high research block;
- very-high sparse block;
- optional unusual-gap block.

Every block carries role:

```text
validation
research_input
```

Do not require one giant continuous zero file.

Update provenance handling before the central coherence experiment.

---

# 18. Phase O — cross-height engine

Add canonical mathematical functions for:

\[
\Delta_n
=
\frac{\tau}
{\log(\gamma_n/\tau)}
\]

and

\[
P_n(u)
=
\frac{
\zeta(
\frac12+i(\gamma_n+\Delta_nu)
)
}{
i\Delta_n\zeta'(\rho_n)
}.
\]

Requirements:

- verified/simple-selected-zero guard;
- arbitrary precision in Audit;
- fixed \(u\)-grid;
- no normalization fit after seeing result;
- coefficient extraction;
- path metrics.

---

# 19. Phase P — cross-height UI

Add Coherence mode with:

- block selector;
- zero selector;
- raw local trace overlay;
- normalized path overlay;
- normalization mode;
- coefficient table/plot;
- pairwise distance matrix;
- precision/provenance panel;
- candidate invariant slot.

Do not label visual similarity as proof evidence.

---

# 20. Phase Q — grade-constraint runner

Add canonical operation for candidate grade quantities:

```text
grade_constraint
```

The implementation should be intentionally narrow.

A new grade quantity is added only when its mathematics is defined first.

Support bilateral grade sets:

\[
K=-N,\ldots,N.
\]

Persist exact symbolic grade metadata.

---

# 21. Phase R — constraint-intersection experiments

The runner should be able to compare:

- actual on-line spectrum inputs;
- synthetic mixed radial leaves;
- positive/negative grade constraints;
- generic-base controls.

The implementation may compute finite intersections/residual stacks.

It must not claim that finite \(K\) establishes the infinite-grade theorem.

---

# 22. Phase S — perturbation refactor

Keep existing perturbation behavior as useful diagnostic functionality, but make theorem-facing perturbation symmetry-complete.

Explicitly label:

```text
SYNTHETIC MODIFIED OBJECT
```

Only elevate perturbation into the central campaign after a candidate coherence invariant is identified.

At that point compute:

\[
\Delta I(\delta,K).
\]

---

# 23. Phase T — converter preservation and clarification

Preserve:

- explicit formula;
- true \(\pi(x)\);
- reconstructed \(\pi_N(x)\);
- exact remainder series;
- selected-zero contribution;
- clean/perturbed difference.

Clarify:

- trivial zeros / archimedean correction remain part of the full formula;
- RH-specific proof mode may use xi separately;
- converter covariance is a coordinate control.

Do not remove the converter merely because the new framework is proof-facing.

---

# 24. Phase U — generic-base controls

Add a small generic base pathway:

\[
b>1.
\]

The user should be able to run a theorem-facing grade observation with:

```text
TAU
GENERIC BASE
```

This is a control layer.

Do not rebrand the primary UI around arbitrary base.

---

# 25. Phase V — Active Mathematics refactor

Update Active Mathematics metadata so every mode declares:

```text
mode
epistemic_class
object_relationship
grade_type
symbolic_scale
numeric_scale
precision
domain_map
function
critical_line
zero_map
radial_coordinate
allowed_interpretation
```

The display is generated from the evaluator object.

No manually maintained explanatory copy that can drift from the engine.

---

# 26. Phase W — research runner schema v2

Upgrade batch specs according to `EXPERIMENT_PROTOCOL.md`.

Preserve compatibility with current canonical runs where practical, but do not keep ambiguous old semantics merely for backwards compatibility.

If old experiment specs use real-valued `K`, migrate them explicitly to:

- `continuous_k`; or
- `integer_K`

according to actual intended semantics.

Document every migration.

---

# 27. Phase X — canonical run migration

Current exact/control runs should be classified under the new ontology.

Likely categories:

```text
same_object_coordinate_control
grade_constraint_comparison
synthetic_modified_object
```

Do not rerun everything automatically.

Rerun only where:

- semantic meaning changed;
- old parameter naming is ambiguous;
- new metadata is required for the result to remain canonical.

Git history preserves old artifacts.

---

# 28. Phase Y — Lean foundation

Add `formal/` according to `LEAN_FORMALIZATION_PLAN.md`.

Initial formal scope:

- generic scale algebra;
- centered/origin dilation;
- tau grade group;
- generic continuation family;
- zero worldline;
- radial invariant;
- integer lattice noncoincidence;
- generic-base zero character;
- symmetric defect;
- abstract radial-rigidity contradiction skeleton.

Do not block the interactive rebuild on a complete zeta formalization.

---

# 29. Agent harness update

Update `.agents` so research/coding agents must read:

1. `TRANSCENDENTAL_CONTINUATION.md`
2. `RESEARCH_HYPOTHESIS.md`
3. `RESEARCH_LEDGER.md`
4. `MATH_CONTRACT.md`
5. `TRANSCENDENTAL_COHERENCE_EXPERIMENT.md`
6. `EXPERIMENT_PROTOCOL.md`
7. `research/index.json`

Rules:

- do not infer project purpose from old prompts;
- do not collapse \(k,K,q,A\);
- do not claim arithmetic lattice noncoincidence proves zero-set noncoincidence;
- do not convert coordinate covariance into RH evidence;
- do not re-open killed/circular branches without addressing their kill reason;
- do not run broad numerical sweeps without a stated prediction and falsifier;
- if a simple invariant appears, stop and derive it.

---

# 30. Historical prompt cleanup

Once the new docs and `.agents` configuration are live:

remove from the live root any obsolete files such as:

```text
RIEMANN_MICROSCOPE_CODING_AGENT_PROMPT.md
REIMANN_SCOPE_FIX_AND_BATCH_AGENT_PROMPT.md
```

provided all still-valid requirements have been absorbed into canonical docs.

Git history remains the archive.

---

# 31. Test migration

Do not delete existing mathematically valid tests.

Add:

```text
test_transcendental.py
test_grade_types.py
test_tau_lattices.py
test_zero_worldlines.py
test_radial_leaves.py
test_compression.py
test_cross_height.py
test_grade_constraints.py
```

Update old tests only where terminology/semantics genuinely changed.

Never weaken a tolerance without mathematical/numerical justification.

---

# 32. Rebuild sequencing

Recommended order:

### Step 1 — docs/harness

- install canonical docs;
- update `.agents`;
- clean stale prompts.

### Step 2 — audit/tests

- run baseline;
- map current semantics;
- record drift.

### Step 3 — grade ontology

- implement \(k,K,q,A\) separation;
- add symbolic grade handling.

### Step 4 — transcendental core

- slices;
- worldlines;
- critical surface;
- radial coordinate.

### Step 5 — UI continuation mode

- bilateral grades;
- continuous interpolation;
- worldline view;
- compression.

### Step 6 — data blocks

- high sparse provenance.

### Step 7 — coherence engine/UI

- \(P_n\);
- coefficients;
- metrics.

### Step 8 — grade constraints

- finite bilateral candidate relations.

### Step 9 — perturbation integration

- only against retained candidate invariant.

### Step 10 — Lean

- formal foundation;
- candidate theorem later.

---

# 33. Do-not-do list

Do not:

- rebuild into a web SaaS architecture;
- add a general theorem graph;
- add dozens of speculative RH experiments;
- replace exact symbolic grade identity with decimal-only state;
- claim \(L_K\) noncoincidence proves RH;
- claim continuous \(k\) consists only of transcendental scale values;
- call \(k=\log_\tau2\) a transcendental scale merely because the base is tau;
- claim compression makes an off-line zero intersect the critical line;
- call a perturbed synthetic function `zeta`;
- claim finite high-zero tests establish an infinite theorem;
- formalize the desired coherence law as an axiom.

---

# 34. Definition of done

The reconfiguration is complete when:

1. native \(k=0\) zeta remains correct;
2. integer, rational, continuous, and generic scale semantics are explicit;
3. negative and positive integer grades work;
4. exact symbolic grade metadata is preserved;
5. zero worldlines are correct;
6. the critical surface is correct;
7. radial leaf invariance is correct;
8. compression/expansion is visually and numerically auditable;
9. arithmetic grade-line noncoincidence is documented without overclaim;
10. sparse high-zero blocks are provenance-safe;
11. actual cross-height paths can be compared;
12. bilateral grade constraints can be run;
13. generic-base controls exist;
14. perturbation is correctly labeled and secondary to baseline coherence;
15. current exact controls still pass;
16. batch artifacts are reproducible and current-canonical;
17. the initial Lean layer builds;
18. a cold-reading agent can identify the exact missing theorem:
    \[
    \text{Transcendental Coherence}
    \Rightarrow
    \text{Transcendental Radial Rigidity}.
    \]

At that point, stop rebuilding the instrument and run the research campaign.
