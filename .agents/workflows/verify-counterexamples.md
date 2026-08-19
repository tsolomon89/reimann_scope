# Verify Counterexamples Workflow

Use `/verify-counterexamples` to run the negative control suite and confirm that candidate mechanisms do not over-generalize to non-Euler or off-line zeta functions.

## Inputs
None (uses standardized failure controls).

## Ordered Execution Stages

1. **Execute Davenport-Heilbronn Verification**:
   - Refines off-line zero of the Davenport-Heilbronn zeta function at $\sigma \approx 0.8085, t \approx 85.6993$.
   - Confirms that functional equation without Euler product allows zeros off the critical line.

2. **Execute Centrifuge Off-Line Sensitivity Test**:
   - Injects a synthetic zero perturbation $\delta = 10^{-4}$.
   - Evaluates $|q_\rho^K| = \tau^{K\delta}$ at $K=100$.
   - Verifies exponential departure from $1$.

3. **Execute Dirichlet Summation Failure Test**:
   - Evaluates truncated Dirichlet sum inside the critical strip and confirms failure of convergence.

## Execution Command
```bash
python .agents/skills/counterexample-suite/scripts/run_counterexamples.py
```

## Output Artifact
Regression test report confirming that all 3 negative controls passed.
