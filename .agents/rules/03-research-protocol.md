---
trigger: model_decision
description: Protocol for research workflow stages, baseline zero discovery vs validation independence, and evaluating new mathematical assertions.
---

# Research Execution Protocol

When conducting mathematical audits, running experiments, or evaluating new claims, follow these standard operational modes:

1. **Distinct Research Modes**:
   - **Setup / Ingestion Mode**: Read relevant corpus files and registers before taking action.
   - **Exact Audit Mode**: Verify symbolic identities via SymPy / exact algebra before numerical work.
   - **Numerical / Falsification Mode**: Test candidate behaviors against high-precision ball arithmetic (Arb/Flint) and counterexample suites.
   - **Assertion Mode**: Record conclusions with explicit claim-status labels (`Derived lemma`, `Numerical observation`, `Falsified`, etc.).

2. **Zero Discovery Independence**:
   - Baseline zero discovery must execute independently on the Hardy $Z$-function: $Z(t) = e^{i\theta(t)}\zeta(1/2+it)$.
   - External reference zero tables (e.g. Odlyzko datasets) must **never** seed or guide the discovery algorithm.
   - Comparison with reference data occurs strictly post-discovery to produce a validation report.

3. **Multi-Stage Claim Evaluation Pipeline**:
   - **Stage 1 (Symbolic)**: Check exact algebraic identities under `MATH_CONTRACT.md`.
   - **Stage 2 (Numerical)**: Check certified error bounds and residuals $|\zeta(s)| < \varepsilon$.
   - **Stage 3 (Falsification)**: Test whether the property holds on non-Euler counterexamples (Davenport-Heilbronn).
   - **Stage 4 (Circularity)**: Screen against known RH-equivalent assumptions.

4. **Batch Sweep and Experiment Review Order**:
   When reviewing previous numerical experiments, inspect artifacts strictly in this order:
   1. `research/index.json` (chronological index of all executed runs)
   2. `research/runs/<run_id>/summary.json` (primary AI-facing summary and criterion evaluation)
   3. `research/runs/<run_id>/manifest.json` (provenance, git commit, parameter space, runtime environment)
   4. `research/runs/<run_id>/results.jsonl` (only if point-level inspection is needed)
   5. Experiment YAML spec (`research/experiments/*.yaml`)
   6. Source code only to audit a specific metric or canonical engine implementation.

