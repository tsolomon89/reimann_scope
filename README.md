# Riemann Scope

`reimann_scope` is an interactive mathematical research instrument for the Riemann zeta function, its zeros, explicit-formula reconstruction, and a project-defined extension of the zeta domain called **transcendental continuation**.

The application is intended to help discover, visualize, falsify, and formalize a specific path toward a proof of the Riemann Hypothesis. It is not itself a proof engine, and finite numerical agreement is never treated as a proof.

---

## Central research programme

Write a nontrivial zero as

\[
\rho=\frac12+\delta+i\gamma.
\]

RH is the statement

\[
\boxed{\delta=0}
\]

for every nontrivial zero.

The working contradiction programme is:

\[
\boxed{
\begin{aligned}
1.&\ \text{Assume RH is false }(H: \delta_0 \ne 0, \zeta(\rho_0) = 0).\\
2.&\ \text{Then the nontrivial spectrum contains both }
\delta=0\text{ and }\delta_0\neq0\text{ radial classes.}\\
3.&\ \text{Construct the complete }\tau\text{-graded transcendental continuation across }\mathbb A_{\mathbb R}.\\
4.&\ \text{Derive an exact global coherence law across that family.}\\
5.&\ \text{Prove that the law admits only one occupied radial class.}\\
6.&\ \text{Known critical-line zeros fix that class at }\delta=0.\\
7.&\ \delta_0\neq0\text{ is contradictory.}
\end{aligned}
}
\]

### The Earliest Missing Implication
The exact point where deductive proof halts is:

\[
\boxed{
H \Longrightarrow \left| D_b + \Delta_{\mathrm{quartet}}(\rho_0) \right| + \varepsilon_{\mathrm{match}} + \varepsilon_{\mathrm{rec}} < \frac{1}{2} \quad \text{or} \quad \exists K \ne J \in \mathbb A_{\mathbb R}, \; m, n \in \pm\mathbb N : m\tau^K = n\tau^J.
}
\]

Under the critical line, $D_b = S_{\mathrm{selected}} \approx -1/2 < 0$ already holds. Proving that an off-critical zero forces the balance outside $[-1/2 - \varepsilon, -1/2 + \varepsilon]$ against the unselected spectral tail allowance ($\approx 1.036 \times 10^{17}$) is the central open challenge. The project exists to discover, test, or formalize the coupling bridging this gap.

---

## Transcendental continuation

Let

\[
\tau=2\pi.
\]

The canonical grade domain is the field of real algebraic numbers:

\[
\boxed{
K \in \mathbb A_{\mathbb R} = \overline{\mathbb Q} \cap \mathbb R.
}
\]

Define the project-facing extended family:

\[
\boxed{
\mathcal Z_\tau(s,K)=\zeta(\tau^{-K}s),
\qquad
(s,K)\in\mathbb C\times\mathbb A_{\mathbb R}.
}
\]

The ordinary analytically continued zeta function is the native grade:

\[
\boxed{
\mathcal Z_\tau(s,0)=\zeta(s).
}
\]

Thus \(K=0\) is not outside transcendental continuation. It is its standard analytic-continuation state.

The project distinguishes:

- \(K\in\mathbb A_{\mathbb R}\): canonical real algebraic grade domain;
- \(K\in\mathbb Z\): canonical bilateral integer discrete skeleton;
- \(q\in\mathbb Q\): rational/root grade refinement;
- \(k\in\mathbb R\): continuous ambient embedding and scale flow (not canonical domain).

The exact integer-grade skeleton is:

\[
\boxed{
\ldots,\tau^{-2},\tau^{-1},1,\tau,\tau^2,\ldots
}
\]

with

\[
\tau^{-K}=(\tau^K)^{-1}.
\]

See `TRANSCENDENTAL_CONTINUATION.md`.

---

## Graded arithmetic grids and universe

For every algebraic grade \(K \in \mathbb A_{\mathbb R}\), define the nonzero arithmetic grid:

\[
L_K = \{n\tau^K : n \in \pm\mathbb N\}, \qquad \mathfrak L_\tau = \bigcup_{K \in \mathbb A_{\mathbb R}} L_K.
\]

Each grid has countably infinitely many points (\(|L_K|=\aleph_0\)) and is scale-isomorphic to every other grid.

For any distinct algebraic grades \(J \ne K \in \mathbb A_{\mathbb R}\):

\[
\boxed{
L_J\cap L_K=\emptyset.
}
\]

So the algebraic-grade grids are **scale-isomorphic, equipotent, and arithmetically disjoint** (by Baker's theorem and the transcendence of \(\tau = 2\pi\)).

The organizing intuition of the project is the **TC Coverage Conjecture**: \(\mathfrak L_\tau \stackrel{?}{=} \mathbb R^\times\). In ZFC set theory, \(|\mathfrak L_\tau| = \aleph_0 < |\mathbb R^\times| = 2^{\aleph_0}\), but the topological closure is dense: \(\overline{\mathfrak L_\tau} = \mathbb R\). The coverage conjecture serves as organizing motivation, never as an unproved premise in an RH proof.

A grid point is represented structurally by:

\[
(K,n), \qquad K \in \mathbb A_{\mathbb R}, \; n \in \pm\mathbb N,
\]

with exact symbolic realization \(n\tau^K\).

---

## Zero worldlines and radial leaves

If

\[
\zeta(\rho)=0,
\]

then in the \(k\)-slice

\[
\boxed{
s_\rho(k)=\tau^k\rho
}
\]

is the corresponding zero.

The critical line becomes the critical surface

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

Define normalized radial coordinate

\[
\boxed{
R_\tau(s,k)
=
\tau^{-k}\Re(s)-\frac12.
}
\]

Along the worldline of

\[
\rho=\frac12+\delta+i\gamma,
\]

\[
\boxed{
R_\tau(s_\rho(k),k)=\delta
}
\]

for every real \(k\).

Therefore transcendental continuation partitions possible zero worldlines into exact radial leaves

\[
R_\tau=\delta.
\]

RH becomes:

\[
\boxed{
\text{all actual nontrivial zero worldlines occupy the leaf }R_\tau=0.
}
\]

A false RH would require simultaneous occupation of \(R_\tau=0\) and at least one \(R_\tau\neq0\) leaf.

The research target is **not** to claim that there is literally no geometric room for another leaf. The target is to determine whether the full arithmetic/analytic constraint system permits more than one occupied radial leaf.

---

## Core experimental layers

The application should distinguish four kinds of work.

### 1. Exact gauge / coordinate controls

Verify and visualize exact coordinate transformations of the same mathematical object.

These are calibration identities, not RH evidence.

### 2. Transcendental continuation and compression

Move through \(k\), including negative grades, to compress or expand zeta geometry while preserving exact transform semantics.

Compression does not itself prove anything about RH; it is a way to inspect grade-independent structure.

### 3. Actual cross-height coherence

Compare genuinely different regions of the unmodified zeta function at widely separated zero heights after a fixed normalization.

This is where candidate global invariants may be discovered or falsified.

### 4. Synthetic off-line perturbation

After a candidate invariant exists, introduce a declared symmetry-complete off-line displacement and test whether it violates the retained coherence law.

A perturbed object is a sensitivity diagnostic, not another zeta function.

---

## Full zeta architecture remains visible

The instrument retains:

- the pole at \(s=1\);
- trivial zeros
  \[
  -2,-4,-6,\ldots;
  \]
- nontrivial zeros;
- the complex zeta trace;
- completed-function / \(\xi\) views where useful;
- the explicit formula and prime-counting reconstruction;
- kernel and coordinate transforms;
- \(\tau\)-grade radial diagnostics;
- cross-height and transcendental-continuation views.

For proof-facing work on the nontrivial spectrum, the completed function

\[
\xi(s)
=
\frac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)
\]

is often the cleaner object.

---

## Canonical documentation authority

Read the root documents in this order:

1. `TRANSCENDENTAL_CONTINUATION.md`
2. `RESEARCH_HYPOTHESIS.md`
3. `RESEARCH_LEDGER.md`
4. `MATH_CONTRACT.md`
5. `RADIAL_DEFECT_QUOTIENT.md`
6. `ARITHMETIC_RADIAL_BRIDGE.md`
7. `TRANSCENDENTAL_COHERENCE_EXPERIMENT.md`
8. `EXPERIMENT_PROTOCOL.md`
9. `RIEMANN_MICROSCOPE_SPEC.md`
10. `DATA_PROVENANCE.md`
11. `LEAN_FORMALIZATION_PLAN.md`
12. `DECISIONS.md`
13. `REBUILD_PLAN.md`

If implementation behavior conflicts with an authoritative mathematical document, treat the conflict as a bug until resolved.

---

## Preferred stack

- Python 3.12+
- Plotly Dash
- `python-flint` / Arb where practical for authoritative high-precision evaluation
- `mpmath` as secondary/fallback
- NumPy for arrays/rendering
- Pytest
- Lean + Mathlib as a proof firewall

Keep the system small and auditable. Do not introduce a separate frontend unless a concrete limitation requires it.

---

## Compute tiers

### Preview

For interactive navigation:

- reduced precision;
- reduced path samples;
- cached/reduced work;
- float rendering allowed and clearly labeled.

### Audit

For authoritative experimental output:

- arbitrary/high precision;
- declared precision;
- full selected samples;
- provenance recorded;
- no silent binary-float reduction before the authoritative metric is formed.

The UI must always show which tier is active.

---

## Research interpretation rules

Finite computation may:

- validate an exact control;
- falsify a candidate statement;
- retain an observational pattern;
- identify a candidate invariant;
- characterize a perturbation defect;
- identify a formalization target.

Finite computation must not automatically conclude:

- `supports_rh`
- `refutes_rh`
- `proof_progress`
- probability that RH is true.

The required transition is:

\[
\boxed{
\text{observe}
\to
\text{state}
\to
\text{derive}
\to
\text{prove radial rigidity}
\to
\text{formalize}.
}
\]

If a simple invariant is discovered, stop broad numerical expansion until it is derived or killed.

---

## Authoritative Research Workflow

All local validation, testing, and canonical regeneration workflows are driven by `scripts/workflow.py`:

```bash
# 1. Fast operational verification (Pytest unit/integration suite + spec schema validations)
python scripts/workflow.py check-fast

# 2. Slow numerical regression suite (arbitrary-precision Arb/mpmath sweeps)
python scripts/workflow.py check-numerical

# 3. Read-only artifact validation (mathematical certificates, formal theorems, canonical runs)
python scripts/workflow.py validate-artifacts

# 4. Strict currentness validation against active disk source files
python scripts/workflow.py validate-artifacts --current

# 5. Plan canonical regeneration (inspect component-level staleness relative to current implementation)
python scripts/workflow.py plan-canonical

# 6. Execute selective canonical regeneration (runs only stale/missing/invalid components)
python scripts/workflow.py run-canonical

# 7. Execute targeted experiment runs or complete rebuild
python scripts/workflow.py run-canonical --experiments <exp_id>
python scripts/workflow.py run-canonical --all
```

### Key Workflow Guarantees

- **Selective Execution**: `run-canonical` executes only components classified as stale, missing, or invalid. If all components are current, it exits 0 without modifying files.
- **Atomic Resummarization**: If only summary/diagnostics are stale, `summarize_run` regenerates `summary.json`, `README.md`, and `diagnostics.json` atomically in a staging directory, preserving `results.jsonl` byte-for-byte without rerunning expensive numerical evaluations.
- **Execution vs Summary Provenance**: Manifests cryptographically bind `execution_provenance` (results, spec, math modules, material packages, producing commit) separately from `summary_provenance` (summary, readme, diagnostics, summarizer modules, summary engine, producing commit).
- **Formal Build Report**: `scripts/build_formal.py` and `formal/build_report.json` dynamically track compiled project theorem declarations (currently **127** compiled declarations) and verify them alongside Lean 4 `lake build` compiler output.


### Modular Experiment Handlers


All experiment runners are organized under `research/handlers/` conforming to `ExperimentHandler` (`research/handlers/base.py`). Handlers explicitly declare code modules and material runtime dependencies, enabling fine-grained invalidation without monolithic sweeps. New mathematical campaigns register new handlers via `@register_handler` without modifying core infrastructure.

