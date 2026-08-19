# Coding Agent Prompt — Audit/Fix `reimann_scope` and Add Reproducible Batch Sweep Runner

Work in the existing repository `tsolomon89/reimann_scope` on the current `main` branch.

The first version is already built. **Do not rebuild it from scratch.** Preserve the KISS instrument architecture and extend it carefully.

## Read first

Read completely, in this order:

1. `RIEMANN_MICROSCOPE_SPEC.md`
2. `MATH_CONTRACT.md`
3. `DATA_PROVENANCE.md`
4. `DECISIONS.md`
5. `README.md`
6. `EXPERIMENT_PROTOCOL.md`

Then inspect the current implementation and tests.

The goal has two parts:

1. **audit and fix current mathematical/operational defects**;
2. **add a minimal reproducible batch sweep runner** so interactive discoveries can become finite, machine-readable experiments whose artifacts can be committed to GitHub and reviewed later by humans/AI.

Do not turn this into the old `riemann_converter` proof-program architecture.

---

## PART A — Audit and fix the current implementation

### A1. Establish baseline before editing

- record current git SHA;
- run the entire existing test suite;
- record failures/errors/warnings;
- launch the app and exercise primary views if the environment permits;
- do not assume green tests imply mathematical fidelity.

### A2. Precision boundary

Audit for premature use of:

- `float(...)`;
- Python `complex`;
- `numpy.float64`;
- `numpy.complex128`;
- SciPy double-precision functions.

Do not simply remove all float use. Establish two paths:

**Preview/render**
- floats/NumPy/SciPy allowed for responsiveness;
- explicitly labeled preview;
- never authoritative evidence.

**Audit/authoritative**
- decimal-string inputs parsed directly to arbitrary precision;
- use `python-flint`/Arb or `mpmath` at declared dps;
- no binary-float downcast before the authoritative metric is formed.

Add tests that prove this separation.

### A3. Explicit-formula converter fidelity

Audit `converter.py` against `MATH_CONTRACT.md`.

Specifically:

1. verify/document the branch convention for `Li(x^rho)`;
2. inspect the current remainder integral and determine whether it is exact to the declared formula or only an asymptotic/preview approximation;
3. if approximate, split preview vs audit implementations explicitly;
4. provide high-precision audit evaluation;
5. compare against known `pi(x)` over a controlled range and test behavior as genuine-zero count increases;
6. preserve fast cached single-zero updates for interactivity, but cross-check them against full high-precision recomputation.

Do not change the mathematics merely to improve the plot.

### A4. Zero-finder semantics

Audit `zero_finder.py`.

The current sign-bracketing/root-refinement approach is useful discovery, but do not call it a proof of completeness unless a rigorous completeness method is actually implemented.

Use precise language:
- discovered;
- refined;
- residual verified;
- matched against reference.

External reference zeros validate only after discovery and must never seed baseline discovery.

If transformed modes currently only map baseline zeros, implement the missing independent discovery/refinement of zeros of the actual transformed function where the UI/spec claims discovered-vs-predicted comparison.

### A5. Certification language

Audit `certified`, `rigorous`, `contains_zero`, and similar language.

Arb may certify an enclosure of a function evaluation; that alone is not proof that the numerical input is an exact root or that no roots in an interval were missed.

Use technically correct numerical-analysis terminology.

### A6. Transform consistency

Preserve the typed transform design.

Ensure:
- Active Mathematics comes from the same transform object used by evaluation;
- critical-line and zero-map formulas match `MATH_CONTRACT.md`;
- audit calculations do not reuse constructor-level float scales as authoritative quantities.

### A7. Tests

Run the full existing suite after fixes.

Do not loosen mathematically correct tolerances to obtain green status. If a test encoded a wrong assumption, replace it with the correct stronger test and record the reason in `DECISIONS.md`.

---

## PART B — Implement `EXPERIMENT_PROTOCOL.md`

Add:

```text
EXPERIMENT_PROTOCOL.md
research_runner.py
research/
    experiments/
    runs/
    index.json
```

Keep the runner small.

### B1. Experiment YAML

Validate declarative specs containing:
- stable ID;
- title;
- exact hypothesis statement;
- one explicit criterion;
- engine operation;
- parameter space;
- precision;
- output-retention settings.

Support only:
- explicit values;
- linear ranges;
- logarithmic ranges;
- deterministic Cartesian products.

No adaptive search yet.

Parameter values are decimal strings/high-precision values.

### B2. Reuse the canonical engine

The runner MUST call existing canonical implementations.

Do not duplicate:
- zeta evaluation;
- tau/centrifuge formulas;
- transforms;
- zero maps;
- explicit formula;
- perturbation math.

If reusable math currently lives only in a Dash callback, refactor it into a canonical function used by both UI and runner.

### B3. Run artifacts

Every run creates:

```text
research/runs/<run_id>/
    manifest.json
    results.jsonl
    summary.json
    README.md
```

`manifest.json` records:
- run/spec IDs;
- spec SHA-256;
- producing git SHA;
- git dirty state;
- timestamps/status;
- dps;
- parameter-space declaration;
- points requested/completed;
- tau as decimal string;
- runtime/package versions;
- relevant source hashes;
- data-provenance identifiers.

`results.jsonl`:
- one line per point;
- deterministic point IDs;
- authoritative numeric values as decimal strings;
- failed points retained;
- incremental writes/flushes.

`summary.json`:
- primary AI-facing artifact;
- hypothesis;
- status;
- point counts;
- deterministic metrics;
- extrema/anomalies;
- declared criterion;
- observed value;
- `criterion_met: true|false|null`.

Do not emit `supports_rh`, `refutes_rh`, `proof_progress`, or `theory_fit`.

Generated run `README.md` is a concise human digest only.

### B4. Index

Maintain `research/index.json`.

A future AI should locate prior runs by reading:
1. index;
2. run summary;
3. manifest;
4. results only when needed.

### B5. Resume/checkpoint

Support commands equivalent to:

```bash
python research_runner.py run research/experiments/foo.yaml
python research_runner.py run research/experiments/foo.yaml --resume <run_id>
python research_runner.py summarize <run_id>
```

Resume must:
- verify spec hash;
- verify code/git compatibility;
- skip completed points;
- append missing results;
- refuse unsafe mixed-state merges.

A partial run is never marked complete.

### B6. Interactive → batch bridge

Add:

`Export Current State as Sweep Draft`

Export current:
- transform mode;
- transform parameters;
- t0/span;
- delta/gamma;
- zero count;
- precision tier;
- Active Mathematics metadata;
- placeholders for hypothesis and criterion.

Do not invent the hypothesis/range/criterion.

### B7. Example infrastructure controls only

Add at most three example YAML experiments:

1. centrifuge identity:
   `log|q_rho^K| = K*delta*log(tau)`;
2. inverse kernel identity with `AB=1`, `C=D=0`;
3. one exact transform/zero-map identity.

These prove the runner works; they are not a proof programme.

### B8. Git policy

Do not auto-commit after every point or run.

Canonical flow:
1. code/tests committed;
2. sweep run from clean commit;
3. artifacts inspected;
4. completed textual artifacts committed in one clean commit when requested.

Keep initial sweeps small enough that full `results.jsonl` can live in GitHub.

---

## PART C — `.agents` guidance

Update `.agents` minimally so future agents know:

When reviewing previous numerical experiments, inspect:
1. `research/index.json`
2. `summary.json`
3. `manifest.json`
4. `results.jsonl` if point-level detail is required
5. experiment YAML
6. source code only to audit an implementation/metric

Do not create a new evidence/proof ontology.

---

## Required new tests

Add tests for:
- YAML validation;
- deterministic explicit/linear/log expansion;
- Cartesian-product ordering;
- decimal-string preservation;
- stable point IDs;
- spec hashing;
- git SHA and dirty-state capture;
- incremental JSONL persistence;
- incomplete-run semantics;
- resume;
- resume refusal for mismatched state;
- deterministic summaries;
- criterion evaluation;
- index updates;
- interactive-engine vs batch-engine equality for the same parameter point;
- preview-vs-audit separation where relevant.

Run the original suite plus new tests before finishing.

---

## Final report back to me

Report:

1. baseline test status before changes;
2. mathematical/operational defects found;
3. fixes made;
4. any spec amendments and why;
5. batch-runner files added;
6. example sweeps executed and criterion results;
7. final complete test-suite result;
8. exact git commit(s) created;
9. anything still approximate, incomplete, or not rigorous.

Do not claim RH support or proof progress from infrastructure controls.
