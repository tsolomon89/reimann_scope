# Experiment Protocol — Batch Sweep and Research Artifact Contract

## 0. Authority and scope

This document is the canonical contract for reproducible finite experiments in `reimann_scope`.

It supplements:

- `TRANSCENDENTAL_CONTINUATION.md` — framework definition;
- `RESEARCH_HYPOTHESIS.md` — proof-facing programme;
- `RESEARCH_LEDGER.md` — current claim status;
- `MATH_CONTRACT.md` — exact mathematical identities;
- `TRANSCENDENTAL_COHERENCE_EXPERIMENT.md` — central campaign;
- `DATA_PROVENANCE.md` — external-data trust;
- `RIEMANN_MICROSCOPE_SPEC.md` — interactive instrument behavior.

The interactive application and batch runner must use the same canonical mathematical engine.

The batch layer is a recorder and evaluator of explicitly stated finite hypotheses. It is not a proof DAG, theorem scorer, or automated RH verdict system.

---

# 1. Research workflow

The canonical workflow is

\[
\boxed{
\text{exact statement}
\to
\text{control}
\to
\text{finite experiment}
\to
\text{persist}
\to
\text{review}
\to
\text{kill / retain}
\to
\text{derive}
\to
\text{formalize}.
}
\]

For the central programme:

\[
\boxed{
\text{gauge}
\to
\text{compression}
\to
\text{actual cross-height}
\to
\text{candidate coherence}
\to
\text{radial perturbation}
\to
\text{algebra}.
}
\]

An experiment is admitted only after its mathematical prediction and falsification condition are written.

---

# 2. Epistemic classes

Every experiment declares one:

```text
exact_control
scale_structure_observation
observational_pattern
sensitivity_diagnostic
candidate_invariant
formalization_regression
```

Meaning:

### `exact_control`

Tests a mathematically derived identity.

Failure indicates implementation/numerical error or a misstated contract.

### `scale_structure_observation`

Characterizes transcendental-continuation/compression behavior without asserting a new invariant.

### `observational_pattern`

Searches for a preregistered finite pattern.

### `sensitivity_diagnostic`

Tests response to a declared synthetic modification.

### `candidate_invariant`

Tests a specifically stated potential law that may later be derived.

### `formalization_regression`

Numerically checks examples of a theorem already formalized or paper-proved.

---

# 3. Object relationship

Every experiment must state which mathematical relationship is being tested:

```text
same_object_coordinate_control
actual_cross_height_comparison
synthetic_modified_object
grade_constraint_comparison
```

Do not mix these classes inside one result without separate metrics and labels.

---

# 4. Repository layout

Use:

```text
research/
    experiments/
        *.yaml
    runs/
        <run_id>/
            manifest.json
            results.jsonl
            summary.json
            README.md
    index.json
research_runner.py
```

The runner remains small.

Do not create a second mathematical engine inside the research layer.

---

# 5. Experiment specification

Each experiment is a declarative YAML document.

Recommended schema:

```yaml
schema_version: "2"

id: transcendental-radial-001
title: Bilateral radial invariant across integer tau grades

research_question: >
  Does the implemented worldline preserve normalized radial
  coordinate across positive and negative integer grades?

epistemic_class: exact_control

object_relationship: same_object_coordinate_control

hypothesis:
  statement: >
    For rho = 1/2 + delta + i gamma and s_K = tau^K rho,
    R_tau(s_K,K) = delta exactly.

prediction:
  statement: >
    The maximum high-precision residual is below the declared tolerance.

falsification:
  statement: >
    Any residual above tolerance after precision convergence
    falsifies the implementation of the stated identity.

interpretation_limit:
  statement: >
    Passing this coordinate control is not evidence for RH.

formalization_target:
  statement: >
    This identity should be formalized as a coordinate theorem.

criterion:
  metric: max_abs_radial_residual
  operator: "<="
  threshold: "1e-50"
  aggregation: max_abs

engine:
  operation: transcendental_radial_worldline

parameters:
  delta:
    kind: explicit
    values: ["-0.01", "0", "0.01"]
  gamma:
    kind: explicit
    values: ["14.134725141734693790457251983562"]
  K:
    kind: linear
    start: "-20"
    stop: "20"
    step: "1"

precision:
  dps: 100

outputs:
  retain_points: true
```

---

# 6. Required specification fields

Required:

- `schema_version`
- `id`
- `title`
- `research_question`
- `epistemic_class`
- `object_relationship`
- `hypothesis.statement`
- `prediction.statement`
- `falsification.statement`
- `interpretation_limit.statement`
- `engine.operation`
- `parameters`
- `precision.dps`

For theorem-facing experiments, also require:

- `formalization_target.statement`

For exact binary controls, require `criterion`.

For purely observational experiments, criterion aggregation may be `none`.

---

# 7. Criterion semantics

Schema:

```yaml
criterion:
  metric: <metric_name>
  operator: "<=" | "<" | ">=" | ">" | "==" | "!="
  threshold: "<decimal_string>"
  aggregation: max_abs | max | min | all | none
```

`none` means:

```json
{
  "criterion_met": null
}
```

Do not coerce an observational pattern into a binary theorem-like result.

---

# 8. Parameter constructors

Supported MVP constructors:

## Explicit

```yaml
kind: explicit
values: ["0", "0.1", "1"]
```

## Linear

```yaml
kind: linear
start: "-10"
stop: "10"
step: "0.25"
```

Use high-precision decimal stepping.

## Logarithmic

```yaml
kind: log
base: "10"
exponents: ["-12", "-10", "-8", "-6"]
```

## Integer grade

```yaml
kind: integer_grade
start: -20
stop: 20
step: 1
```

This constructor semantically means

\[
K\in\mathbb Z.
\]

## Rational grade

```yaml
kind: rational_grade
values: ["-3/2", "-1", "-1/2", "0", "1/2", "1", "3/2"]
```

Parse exactly as rationals before evaluating \(\tau^q\).

## Cartesian product

Multiple parameters form a deterministic Cartesian product in declared order.

No adaptive search in the canonical first campaign unless separately approved.

---

# 9. Canonical engine operations

Initial/current operations may include:

```text
zeta_value
zero_discovery
transform_zero_map
kernel_identity
converter
converter_perturbation
centrifuge
symmetric_centrifuge_defect
transcendental_slice
transcendental_zero_worldline
transcendental_radial_worldline
compression_expansion
cross_height_path
cross_height_coefficients
grade_constraint
candidate_invariant_perturbation
```

Every operation must call canonical code in the mathematical engine.

No formula duplication inside `research_runner.py`.

---

# 10. Grade semantics in experiments

Do not serialize one field called `k` and infer its intended type.

Use separate schema fields when appropriate:

```text
continuous_k
integer_K
rational_q
generic_scale_A
```

The runner may derive

\[
A=\tau^k
\]

internally, but it must preserve the declared semantic source.

For a canonical integer-grade run, persist both:

```json
{
  "integer_K": "-3",
  "scale_expression": "tau^-3",
  "scale_numeric": "..."
}
```

The symbolic expression is part of the authoritative metadata.

---

# 11. Exact grade / finite realization metadata

Every run involving transcendental grades records:

```json
{
  "tau": {
    "symbolic": "2*pi",
    "numeric": "...",
    "precision_dps": 100,
    "library": "..."
  }
}
```

For each nonzero grade, preserve the exact symbolic referent where possible:

```text
tau^K
tau^(p/q)
```

Do not store only the decimal approximation and discard the grade identity.

---

# 12. Data-block inputs

Experiments using external zero data must identify blocks by immutable block ID.

Example:

```yaml
data:
  zero_blocks:
    - low-validation-v1
    - high-sparse-v1
```

The runner resolves these through `data/provenance.json`.

A run must record exact checksums for every consumed block.

---

# 13. High-zero input roles

Two distinct roles exist.

## Validation zero block

Used to validate independent zero discovery.

Reference values must not seed the discovery being validated.

## Research-input zero block

Used as trusted coordinates for a high-height structural experiment where independent discovery from scratch is not the claim.

This is allowed if explicitly labeled.

Do not describe a research-input block as independently discovered by the app.

---

# 14. Run identity

Use a unique run ID:

```text
20260821T120000Z_transcendental-coherence-001_<short-hash>
```

A completed run directory is immutable.

A rerun creates a new run ID.

---

# 15. Current-canonical retention policy

Git history is the historical record.

The live working tree should contain only the **current canonical run** for each active experiment unless a comparison explicitly requires multiple current runs.

Therefore:

1. run with a new ID;
2. review it;
3. if it becomes canonical, update `research/index.json`;
4. remove the superseded live canonical run from the working tree in the same research-artifact cleanup;
5. rely on Git history for the previous run.

Do not keep an ever-growing live archive of superseded runs.

A completed run remains immutable while it exists.

---

# 16. `manifest.json`

Minimum fields:

```json
{
  "schema_version": "2",
  "run_id": "...",
  "experiment_id": "...",
  "epistemic_class": "observational_pattern",
  "object_relationship": "actual_cross_height_comparison",
  "experiment_spec_sha256": "...",
  "git_commit": "...",
  "git_dirty": false,
  "started_at": "...Z",
  "completed_at": null,
  "status": "running",
  "precision": {"dps": 100},
  "parameter_space": {},
  "points_requested": 100,
  "points_completed": 0,
  "tau": {
    "symbolic": "2*pi",
    "numeric": "...",
    "precision_dps": 100
  },
  "data_provenance": {},
  "code_modules": {},
  "runtime": {
    "python": "...",
    "platform": "...",
    "packages": {}
  }
}
```

Rules:

- `git_commit` is the producing code SHA;
- record `git_dirty`;
- canonical runs should normally come from clean commits;
- hash the exact experiment spec;
- hash relevant mathematical source files;
- `status` is `running`, `complete`, `incomplete`, or `failed`;
- partial runs are never `complete`.

---

# 17. `results.jsonl`

One object per evaluated point.

Example:

```json
{
  "point_id": 0,
  "inputs": {
    "integer_K": "-10",
    "delta": "0.001",
    "gamma": "14.134725..."
  },
  "symbolic": {
    "scale": "tau^-10"
  },
  "outputs": {
    "radial_class": "0.001",
    "residual": "2.0e-97"
  },
  "status": "ok"
}
```

Rules:

- one line = one independently readable point;
- authoritative high-precision values serialize as strings;
- plotting floats are not authoritative;
- deterministic `point_id`;
- failed points remain present;
- write incrementally;
- support resume.

---

# 18. `summary.json`

Minimum shape:

```json
{
  "schema_version": "2",
  "run_id": "...",
  "experiment_id": "...",
  "status": "complete",
  "epistemic_class": "exact_control",
  "object_relationship": "same_object_coordinate_control",
  "research_question": "...",
  "hypothesis": "...",
  "prediction": "...",
  "falsification": "...",
  "interpretation_limit": "...",
  "points_requested": 123,
  "points_completed": 123,
  "points_failed": 0,
  "metrics": {},
  "criterion": {
    "criterion_met": true
  },
  "extrema": {},
  "anomalies": [],
  "warnings": []
}
```

Forbidden fields:

```text
supports_rh
refutes_rh
proof_progress
theory_fit
rh_probability
```

---

# 19. Generated run `README.md`

Generate a concise human digest containing:

- experiment ID/title;
- research question;
- epistemic class;
- object relationship;
- run ID;
- git SHA;
- clean/dirty state;
- precision;
- data-block IDs/checksums;
- parameter-space summary;
- point counts;
- criterion if any;
- main metrics;
- anomalies;
- interpretation limit;
- artifact paths.

State explicitly:

> This result applies only to the declared finite experiment and does not constitute a proof of RH.

---

# 20. `research/index.json`

The index contains current canonical runs only.

Example:

```json
{
  "schema_version": "2",
  "runs": [
    {
      "run_id": "...",
      "experiment_id": "...",
      "epistemic_class": "exact_control",
      "object_relationship": "same_object_coordinate_control",
      "timestamp": "...Z",
      "git_commit": "...",
      "status": "complete",
      "criterion_met": true,
      "summary_path": "research/runs/.../summary.json",
      "manifest_path": "research/runs/.../manifest.json",
      "results_path": "research/runs/.../results.jsonl"
    }
  ]
}
```

This is the first run artifact an AI agent should inspect.

---

# 21. Resume/checkpoint behavior

Support:

```bash
python research_runner.py run research/experiments/<spec>.yaml
python research_runner.py run research/experiments/<spec>.yaml --resume <run_id>
python research_runner.py summarize <run_id>
```

Resume must:

- confirm spec hash;
- confirm compatible producing code state or refuse;
- skip completed point IDs;
- append missing results;
- recompute summary;
- never merge incompatible run states silently.

---

# 22. Interactive → batch bridge

The Dash app should support:

```text
Export Current State as Sweep Draft
```

Export:

- active mathematical mode;
- continuous \(k\), integer \(K\), rational \(q\), or generic \(A\) semantics;
- source zero block/selected zero;
- \(t_0\), span, \(\delta\), \(\gamma\) as applicable;
- precision tier;
- Active Mathematics metadata;
- placeholders for hypothesis, prediction, falsification, and interpretation limit.

Do not invent the research claim automatically.

---

# 23. Precision boundary

Authoritative calculations must not silently reduce to:

- Python `float`;
- Python binary `complex`;
- NumPy `float64`;
- NumPy `complex128`;
- SciPy double precision

before the authoritative metric is formed.

Maintain:

### Preview path

Float/double precision allowed for responsive display and explicitly labeled.

### Audit path

Arbitrary/high precision throughout the mathematical evaluation and metric construction.

---

# 24. Zero-discovery semantics

Use precise terminology:

```text
candidate
discovered
refined
residual_verified
reference_matched
```

Do not use `complete` or `all zeros found` unless a rigorous completeness method justifies it.

Reference data remains validation-only when the task is validating discovery.

---

# 25. Transformed-zero semantics

For exact transform validation:

- discover/refine zeros of the transformed function independently where feasible;
- compute predicted mapped zeros from the mathematical transform;
- compare afterward.

Do not seed the transformed discovery with the predicted locations and call that independent.

For extremely high research-input zero blocks, direct evaluation at trusted supplied coordinates is allowed if labeled as research input rather than discovery.

---

# 26. Certification terminology

Do not use `certified`, `rigorous`, `proved zero`, or similar language merely because a high-precision function value is small.

If Arb interval methods supply a specific rigorous enclosure theorem, state exactly what has been certified.

An enclosure of a function value is not automatically a proof that no roots were missed in a range.

---

# 27. Initial canonical control experiments

The control suite should include:

1. native grade:
   \[
   \mathcal Z_\tau(s,0)=\zeta(s);
   \]

2. origin worldline:
   \[
   \mathcal Z_\tau(\tau^k\rho,k)=0;
   \]

3. radial invariant:
   \[
   R_\tau(\tau^k\rho,k)=\delta;
   \]

4. centered dilation zero map;

5. inverse kernel lock;

6. zero-character modulus;

7. symmetry-complete grade defect;

8. coupled converter covariance.

These are calibration identities.

---

# 28. Central observational campaign

After controls pass:

1. add high-zero block support;
2. run compression/expansion views;
3. compute actual cross-height normalized paths;
4. evaluate preregistered path/coefficient metrics;
5. test candidate grade constraints bilaterally;
6. run generic-base controls;
7. retain or kill the candidate coherence statement.

Do not begin a new broad perturbation sweep before a baseline coherence candidate exists.

---

# 29. Perturbation campaign

For a retained candidate invariant \(I\):

1. define symmetry-complete off-line perturbation;
2. preserve multiplicity semantics;
3. compute
   \[
   \Delta I(\delta,K);
   \]
4. compare positive/negative \(K\);
5. test whether mixed radial modes can compensate across all declared constraints;
6. do not infer infinite-grade impossibility from finite \(K\) alone.

---

# 30. AI-agent consumption contract

Future agents inspect in this order:

1. `TRANSCENDENTAL_CONTINUATION.md`
2. `RESEARCH_HYPOTHESIS.md`
3. `RESEARCH_LEDGER.md`
4. `MATH_CONTRACT.md`
5. `research/index.json`
6. selected `summary.json`
7. `manifest.json`
8. point-level results if needed
9. experiment YAML
10. source code when auditing implementation

Agents must distinguish:

- exact theorem/identity;
- coordinate control;
- numerical observation;
- synthetic diagnostic;
- conjectural inference;
- false/circular/insufficient branch.

---

# 31. Required batch tests

At minimum:

1. YAML validation;
2. deterministic explicit expansion;
3. deterministic linear expansion;
4. deterministic integer-grade expansion;
5. exact rational-grade parsing;
6. Cartesian-product ordering;
7. decimal-string precision preservation;
8. symbolic grade metadata preservation;
9. stable point IDs;
10. spec hashing;
11. git SHA capture;
12. dirty-state capture;
13. incremental JSONL writes;
14. resume;
15. mismatch refusal;
16. incomplete-run semantics;
17. deterministic summaries;
18. criterion evaluation;
19. canonical index replacement;
20. interactive-engine vs batch-engine equality;
21. no duplicate math implementation.

---

# 32. Definition of done

The batch/research layer is correct when:

1. all exact controls reuse canonical engine code;
2. \(k\), \(K\), \(q\), and generic \(A\) remain semantically distinct;
3. symbolic grade identity survives serialization;
4. authoritative metrics stay high precision;
5. external data are checksum-tied to runs;
6. current canonical runs are obvious in `research/index.json`;
7. Git history, not a growing live folder, preserves superseded runs;
8. cross-height and grade-constraint campaigns are reproducible;
9. perturbation results are labeled synthetic;
10. no automated RH verdict or proof-progress ontology exists.

---

# 33. Explicit Formula Discrimination Suite

The suite comprises three canonical experiments evaluating the Riemann–Weil explicit formula under transcendental continuation:

1. `explicit-formula-native-baseline-001`
   - **Epistemic Class**: `observational_pattern`
   - **Scope**: Validates native explicit formula components, signs, normalization, and truncation error budgets across test functions \(j=1..6\) at \(K=0\) with sensitivity diagnostics for spectral cutoff, prime sieve cutoff, precision, and integration window.
2. `explicit-formula-grade-covariance-001`
   - **Epistemic Class**: `exact_control`
   - **Scope**: Validates exact Fourier scaling \(\widehat h_{K,j}(x) = a_K^{-1} \widehat H_j(a_K^{-1} x)\), pullback identity \(\mathcal C_{K,j}[H] \equiv \mathcal C_0[H(a_K \cdot)]\), numerical quadrature verification, and independent expanded-native basis rank equivalence.
   - **Classifications**: Exact theoretical classification `coordinate_redundant`; finite basis comparison relative to an unexpanded native basis `finite_basis_enrichment_only`.
3. `explicit-formula-perturbation-rank-001`
   - **Epistemic Class**: `sensitivity_diagnostic`
   - **Scope**: Evaluates finite divisor defects \(\Delta \mathcal C_{K,j} = \langle\Delta\mathcal D, h_{K,j}\rangle\), exact validator rejection of unsymmetric or multiplicity-violating mutations, symmetry-complete radial quartet exact decomposition into height merging \(\Delta\mathcal C^{\mathrm{merge}}\) and pure radial \(\Delta\mathcal C^{\mathrm{radial}}(\delta)\), Jacobian SVD with threshold sweep across \([10^{-18}, 10^{-20}, 10^{-25}, 10^{-30}, 10^{-35}, 10^{-40}]\), rank stability classification `threshold_dependent`, and minimum-norm linearized compensation vectors with forward residuals. Consumes verified zero certificates for all perturbed cases.

---

# 34. Research Instrument Lifecycle and Modular Architecture

The research-instrument architecture guarantees a strict recurring execution cycle:

\[
\text{mathematical formulation}
\rightarrow
\text{small implementation}
\rightarrow
\text{fast operational verification}
\rightarrow
\text{numerical regression}
\rightarrow
\text{canonical execution when required}
\rightarrow
\text{published evidence}.
\]

### 1. Authoritative Workflow Interface (`scripts/workflow.py`)

All development, verification, and canonical publication workflows are standardized via `scripts/workflow.py`:

- `python scripts/workflow.py check-fast`: Runs fast operational unit/integration tests and validates all experiment specification YAMLs (read-only).
- `python scripts/workflow.py check-numerical`: Runs slow arbitrary-precision numerical regression suite (read-only).
- `python scripts/workflow.py validate-artifacts`: Validates all mathematical certificates, formal Lean 4 build report, and canonical run bundles without modifying disk state.
- `python scripts/workflow.py plan-canonical`: Inspects whether any certificates or canonical runs are stale relative to the workspace or git HEAD, reporting exact point counts and reasons (read-only).
- `python scripts/workflow.py run-canonical`: Executes planned canonical regeneration, enforcing clean git worktree before publication.

### 2. Modular Experiment-Handler Boundary (`research/handlers/`)

All canonical experiments implement the `ExperimentHandler` interface (`research/handlers/base.py`):

- **Declaration of Dependencies**: Declares fine-grained source modules, math engines, input data files, and consumed certificates via `declared_dependencies`.
- **Decoupled Evaluation**: Implements `evaluate_point(inputs, dps, param_space, context)`.
- **Isolated Summary Computation**: Implements `compute_summary(results, spec, manifest, status)`.
- **Diagnostic Generation**: Implements `generate_diagnostics(results, spec, run_dir)`.

New experimental campaigns (e.g. \((Q, \Xi^\flat, L_Q)\)) register new handlers via `@register_handler` without modifying core orchestration or historical experiment code.

### 3. Separation of Execution vs Summary Provenance

To maintain byte-level reproducibility and distinguish raw numerical evaluation from digest formatting:

- `execution_provenance`: Captures raw simulation output SHA-256 (`results.jsonl`), producing Git commit, dependency fingerprint, and source code hashes active during point evaluation.
- `summary_provenance`: Captures summary SHA-256 (`summary.json`), digest SHA-256 (`README.md`), diagnostics SHA-256 (`diagnostics.json`), and the summarizer source hash (`research_runner.py`).
- `research_runner.summarize_run` strictly asserts byte-for-byte SHA-256 invariance on `results.jsonl` before and after updating summary metadata.

### 4. Transactional Atomic Swap & Rollback

- Sweeps execute in isolated temporary working directories (`research/runs/.tmp_<exp_id>_<pid>`).
- On successful completion and strict validator passage, the run directory is atomically swapped into `research/runs/<exp_id>`.
- In the event of disk full, power failure, or index update exception, pre-run states are automatically restored byte-for-byte from transactional backup directories (`.bak_<exp_id>_<pid>`).
