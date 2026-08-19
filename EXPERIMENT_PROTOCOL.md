# EXPERIMENT_PROTOCOL.md — Batch Sweep and Research Artifact Contract

## 0. Authority and scope

This document is the canonical contract for reproducible batch experiments in `reimann_scope`.

It supplements:

- `RIEMANN_MICROSCOPE_SPEC.md` — interactive instrument/product behavior;
- `MATH_CONTRACT.md` — exact mathematical identities;
- `DATA_PROVENANCE.md` — trusted external data and validation rules;
- `DECISIONS.md` — consequential implementation decisions.

The interactive scope and the batch runner MUST use the same mathematical engine. The batch system must not duplicate formulas from `math_core.py`, `transforms.py`, `converter.py`, or zero-finding code.

The batch layer is a **recorder and evaluator of explicitly stated finite hypotheses**. It is not a proof DAG, theorem scorer, automated hypothesis generator, or replacement for mathematical reasoning.

---

# 1. Research workflow

The intended workflow is:

\[
\boxed{
\text{interactive exploration}
\to
\text{state a finite hypothesis}
\to
\text{declare a parameter space}
\to
\text{run sweep}
\to
\text{persist artifacts}
\to
\text{review}
\to
\text{kill, refine, or formalize}
}
\]

An experiment is admitted only after its hypothesis and success/failure criterion are written explicitly.

A run may conclude only whether its own declared criterion was met over its declared finite parameter space.

It must never automatically conclude that RH is supported, refuted, proved, or made more likely.

---

# 2. Repository layout

Add:

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
EXPERIMENT_PROTOCOL.md
```

Do not add a large framework unless the simple file contract becomes insufficient.

---

# 3. Experiment specification

Each experiment is a declarative YAML document.

Minimum schema:

```yaml
schema_version: "1"
id: radial-scale-001
title: Off-line radial amplification under tau grade

hypothesis:
  statement: >
    For fixed gamma and nonzero delta, log|q_rho^K| is linear in K
    with slope delta*log(tau).

criterion:
  metric: max_abs_slope_error
  operator: "<="
  threshold: "1e-30"

engine:
  operation: centrifuge

parameters:
  delta:
    kind: explicit
    values: ["-0.01", "-0.001", "0", "0.001", "0.01"]
  gamma:
    kind: explicit
    values: ["14.134725141734693790457251983562"]
  K:
    kind: linear
    start: "-100"
    stop: "100"
    step: "1"

precision:
  dps: 80

outputs:
  retain_points: true
```

Required fields:

- `schema_version`
- `id`
- `title`
- `hypothesis.statement`
- `criterion`
- `engine.operation`
- `parameters`
- `precision.dps`

Reject malformed specs before computation begins.

---

# 4. Parameter-space constructors

MVP supports only:

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

Use decimal/high-precision stepping, not repeated binary-float addition.

## Logarithmic

```yaml
kind: log
base: "10"
exponents: ["-12", "-10", "-8", "-6", "-4", "-2"]
```

## Cartesian product

Multiple declared parameters form a deterministic Cartesian product in declared parameter order.

No adaptive search in MVP.

---

# 5. Engine operations

The runner orchestrates existing mathematical code.

Initial permitted operations should remain small, for example:

- `centrifuge`
- `transform_zero_map`
- `kernel_identity`
- `zeta_trace_compare`
- `converter_perturbation`

Each must call the canonical math implementation.

Do not implement a second copy of a transform or explicit formula inside `research_runner.py`.

If an experiment needs new mathematics, add/test that mathematics in the canonical engine first, then expose it to the runner.

---

# 6. Run identity

Use a unique run ID such as:

```text
20260819T163000Z_radial-scale-001_<short-hash>
```

Every completed run is immutable. A rerun creates a new directory.

---

# 7. `manifest.json`

Create the manifest before evaluating points.

Minimum fields:

```json
{
  "schema_version": "1",
  "run_id": "...",
  "experiment_id": "radial-scale-001",
  "experiment_spec_sha256": "...",
  "git_commit": "...",
  "git_dirty": false,
  "started_at": "...Z",
  "completed_at": null,
  "status": "running",
  "precision": {"dps": 80},
  "parameter_space": {},
  "points_requested": 1000,
  "points_completed": 0,
  "tau": "6.28318...",
  "runtime": {
    "python": "...",
    "platform": "...",
    "packages": {}
  },
  "data_provenance": {},
  "code_modules": {}
}
```

Rules:

- `git_commit` is the code SHA that generated the run.
- Record `git_dirty`.
- Prefer canonical runs from clean commits.
- Hash the exact experiment spec.
- Record hashes of the relevant mathematical source files.
- `status` is `running`, `complete`, `incomplete`, or `failed`.
- A partial run is never marked complete.

---

# 8. `results.jsonl`

One JSON object per evaluated point.

Example:

```json
{"point_id":0,"inputs":{"delta":"0.0001","gamma":"14.1347...","K":"-100"},"outputs":{"log_modulus":"-0.018378..."},"status":"ok"}
```

Rules:

- one line = one independently readable point;
- canonical high-precision numbers serialize as decimal strings;
- plotting floats are not authoritative stored values;
- deterministic `point_id`;
- failed points remain present with status/error;
- write and flush incrementally;
- resume from `results.jsonl` + `manifest.json`.

---

# 9. `summary.json`

This is the primary AI-facing artifact.

Minimum shape:

```json
{
  "schema_version": "1",
  "run_id": "...",
  "experiment_id": "radial-scale-001",
  "status": "complete",
  "hypothesis": "...",
  "points_requested": 1407,
  "points_completed": 1407,
  "points_failed": 0,
  "metrics": {
    "max_abs_slope_error": "2.1e-76"
  },
  "criterion": {
    "metric": "max_abs_slope_error",
    "operator": "<=",
    "threshold": "1e-30",
    "observed": "2.1e-76",
    "criterion_met": true
  },
  "extrema": {},
  "anomalies": [],
  "warnings": []
}
```

Allowed:

- `criterion_met: true`
- `criterion_met: false`
- `criterion_met: null` for incomplete/invalid

Forbidden in MVP:

- `supports_rh`
- `refutes_rh`
- `proof_progress`
- `theory_fit`

---

# 10. Generated run `README.md`

Generate a concise digest with:

- experiment title/id;
- run ID;
- git SHA;
- clean/dirty state;
- precision;
- parameter-space summary;
- point counts;
- criterion and observed metric;
- extrema/anomalies;
- artifact paths;
- explicit statement that the result applies only to the declared finite sweep.

Do not duplicate large point tables in Markdown.

---

# 11. `research/index.json`

Maintain a chronological machine-readable index.

Each entry:

```json
{
  "run_id": "...",
  "experiment_id": "...",
  "timestamp": "...Z",
  "git_commit": "...",
  "status": "complete",
  "criterion_met": true,
  "summary_path": "research/runs/.../summary.json",
  "manifest_path": "research/runs/.../manifest.json",
  "results_path": "research/runs/.../results.jsonl"
}
```

This is the first file an AI agent should inspect when asked what experiments have been run.

---

# 12. Resume/checkpoint behavior

Support:

```bash
python research_runner.py run research/experiments/<spec>.yaml
python research_runner.py run research/experiments/<spec>.yaml --resume <run_id>
python research_runner.py summarize <run_id>
```

Resume must:

- confirm experiment-spec hash;
- confirm code/git compatibility or refuse;
- skip completed `point_id`s;
- append missing results;
- recompute summary after execution;
- never merge results from different code/spec states silently.

---

# 13. Interactive → batch bridge

Add `Export Current State as Sweep Draft` to the Dash app.

Export current:

- transformation mode;
- transform parameters;
- `t0`, span, delta, gamma as applicable;
- zero count;
- precision tier;
- Active Mathematics metadata;
- placeholders for hypothesis and criterion.

Do not invent hypothesis, range, or pass/fail criterion.

---

# 14. Git commit policy

The runner should not auto-commit by default.

Recommended canonical workflow:

1. fix code;
2. run tests;
3. commit code;
4. run sweep from clean commit;
5. inspect artifacts;
6. commit completed run artifacts in one clean commit when requested.

Do not commit after every point.

Keep initial sweeps small enough that full textual `results.jsonl` can live in GitHub.

---

# 15. AI-agent consumption contract

Update `.agents` so future agents inspect runs in this order:

1. `research/index.json`
2. selected `summary.json`
3. `manifest.json`
4. `results.jsonl` if point-level inspection is needed
5. experiment YAML
6. source code only when auditing a metric/implementation

Agents must distinguish:

- exact algebraic control;
- numerical observation;
- incomplete/failed run;
- criterion result;
- broader mathematical inference, which occurs outside the runner.

---

# 16. Pre-extension audit/fix gate

Before implementing batch infrastructure, audit the current first version.

## Precision boundary

Authoritative math must not silently reduce to Python `float`, `complex128`, or SciPy double precision before the authoritative metric is formed.

Establish:

- **audit/authoritative path:** arbitrary precision;
- **preview/render path:** float allowed and labeled.

## Converter fidelity

Audit the explicit formula against `MATH_CONTRACT.md`.

Specifically:

- document/test the complex branch convention for `Li(x^rho)`;
- verify the remainder integral is the declared object rather than an undocumented asymptotic approximation;
- separate preview approximations from audit calculations;
- compare against known prime counts;
- cross-check fast single-zero delta updates against full high-precision recomputation.

## Zero-discovery semantics

Do not call a sign-scan proof of completeness unless a rigorous completeness method is implemented.

Use `discovered`, `refined`, `residual_verified`, `matched`.

Reference zeros remain validation-only.

## Transformed-zero discovery

Where the UI/spec claims discovered-vs-predicted transformed zeros, independently discover/refine zeros of the actual transformed function rather than only mapping the baseline set.

## Certification terminology

Audit `certified`, `rigorous`, `contains_zero`, etc.

An Arb function-value enclosure is not automatically proof that the numerical input is the exact root or that no roots were missed.

## Tests first

Run the entire existing test suite before changes and after changes.

Do not weaken correct mathematical tests to obtain green status.

---

# 17. Required new batch tests

Add tests for:

1. YAML validation;
2. deterministic explicit/linear/log expansion;
3. Cartesian-product ordering;
4. decimal-string precision preservation;
5. stable point IDs;
6. spec SHA hashing;
7. git SHA capture;
8. git dirty-state capture;
9. incremental JSONL writes;
10. resume;
11. refusal to resume mismatched state;
12. incomplete-run semantics;
13. deterministic summaries;
14. criterion evaluation;
15. index updates;
16. interactive-engine vs batch-engine equality for the same point;
17. no duplicate math implementation.

---

# 18. Initial infrastructure-control experiments

Add only 2–3 tiny examples:

## A — Centrifuge identity

\[
\log|q_\rho^K|=K\delta\log\tau.
\]

## B — Inverse kernel lock

For \(AB=1\), \(C=D=0\):

\[
\mathcal Z_{A,0,1/A,0}(s)=\zeta(s).
\]

## C — One exact zero-map transform

For example origin or centered coordinate dilation.

These validate infrastructure only.

---

# 19. Definition of done

The extension is complete when:

1. current defects found by the audit are fixed or explicitly documented;
2. all existing tests pass without weakened valid tolerances;
3. YAML expands deterministically to a finite parameter space;
4. a run creates manifest/results/summary/README;
5. interruption/resume works;
6. high-precision values survive serialization as decimal strings;
7. run artifacts are tied to producing code/spec/data;
8. `research/index.json` makes prior runs AI-readable;
9. Dash exports current state as a sweep draft;
10. batch and interactive paths use the same canonical math engine;
11. example control sweeps execute successfully;
12. no theorem/proof ontology is introduced.
