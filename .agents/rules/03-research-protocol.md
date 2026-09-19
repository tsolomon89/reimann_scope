---
trigger: model_decision
description: Protocol for research workflow stages, research loop, escalation of unresolved checks, baseline zero discovery independence, and evaluating new mathematical assertions.
---

# Research Execution Protocol

When conducting mathematical audits, running experiments, or evaluating new claims, follow these standard operational modes:

1. **Distinct Research Modes**:
   - **Setup / Ingestion Mode**: Read relevant corpus files, `.agents/research/state.json`, and claim registers before taking action.
   - **Exact Audit Mode**: Verify symbolic identities via SymPy, exact algebra, or Lean 4 before numerical work.
   - **Numerical / Falsification Mode**: Test candidate behaviors against high-precision ball arithmetic (Arb/Flint) and counterexample suites.
   - **Assertion Mode**: Record conclusions with explicit claim-status labels (`PROPOSED`, `EMPIRICAL`, `NUMERICALLY_UNRESOLVED`, `CERTIFIED_FINITE`, `PROVED_CONDITIONAL`, `REFUTED_WITHIN_SCOPE`, `AWAITING_INDEPENDENT_REVIEW`).

2. **Persistent Research Loop**:
   When pursuing open mathematical objectives:
   1. **Select Obligation**: Identify a tractable, consequential TC obligation from `.agents/research/queue.json` and declare what would falsify the candidate conjecture.
   2. **Derive / Implement**: Derive the decisive calculation or lemma, declaring all assumptions, controls, and error bounds.
   3. **Execute & Refine**: Run the calculation. If discretization uncertainty or mesh limits overwhelm the signal, perform genuine refinement ($n \to 2n$) or record `NUMERICALLY_UNRESOLVED`. Retain failures as scoped negative evidence.
   4. **Independent Review**: Challenge the strongest conclusion via independent review in `.agents/claims/reviews/` with explicit objection logging.
   5. **Evidence-Bounded Acceptance**: Accept only the conclusion strictly warranted by the evidence.
   6. **Autonomous Continuation**: Update `.agents/research/queue.json` and `.agents/research/state.json`, then execute the next queued action.

3. **Escalation of Unresolved Checks into Research Obligations**:
   - An unresolved or failed mathematical check creates an active research obligation.
   - It **never** authorizes a success claim, a universal obstruction claim, or premature termination of the research mission.
   - When a numerical or analytical obstacle is encountered, formulate the missing estimate or counterexample explicitly and add it to the research queue.

4. **Zero Discovery Independence**:
   - Baseline zero discovery must execute independently on the Hardy $Z$-function: $Z(t) = e^{i\theta(t)}\zeta(1/2+it)$.
   - External reference zero tables (e.g. Odlyzko datasets) must **never** seed or guide the discovery algorithm.
   - Comparison with reference data occurs strictly post-discovery to produce a validation report.

5. **Multi-Stage Claim Evaluation Pipeline**:
   - **Stage 1 (Symbolic)**: Check exact algebraic identities under `MATH_CONTRACT.md`.
   - **Stage 2 (Numerical)**: Check certified error bounds and residuals $|\zeta(s)| < \varepsilon$ with explicit error budgets.
   - **Stage 3 (Falsification)**: Test whether the property holds on non-Euler counterexamples (Davenport-Heilbronn).
   - **Stage 4 (Circularity)**: Screen against known RH-equivalent assumptions.

6. **Batch Sweep and Experiment Review Order**:
   When reviewing previous numerical experiments, inspect artifacts strictly in this order:
   1. `research/index.json` (chronological index of all executed runs)
   2. `research/runs/<run_id>/summary.json` (primary AI-facing summary and criterion evaluation)
   3. `research/runs/<run_id>/manifest.json` (provenance, git commit, parameter space, runtime environment)
   4. `research/runs/<run_id>/results.jsonl` (only if point-level inspection is needed)
   5. Experiment YAML spec (`research/experiments/*.yaml`)
   6. Source code only to audit a specific metric or canonical engine implementation.

7. **Mandatory Pre-Acceptance Claim Audit Gates (`zeta-proof-audit`)**:
   Before any mathematical claim can be registered as `PROVED`, `CLOSED`, or `ACCEPTED`:
   - It must provide a machine-readable JSON specification conforming to the schema (19 mandatory core fields plus declared analytical metadata).
   - It must pass all 10 pre-acceptance gates validated by `.agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py`.
   - Never classify a prime-only Dirichlet polynomial as "completed zeta" without an explicit completion bridge.
   - Never assert universal non-vanishing without symbolic elimination / cancellation-case analysis.
   - Never claim diagonalization of finite-window inner products without rigorous off-diagonal analysis.
   - Require independent review artifacts bound to input digests for any terminal status.
