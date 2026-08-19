---
name: counterexample-suite
description: Tests proposed mathematical mechanisms and invariance claims against standard counterexamples (Davenport-Heilbronn zeta function, off-line zero test cases, Dirichlet series truncation).
---

# Counterexample Suite Skill

Use this skill to subject candidate mathematical claims, symmetry assertions, or zero-localization mechanisms to established counterexamples.

## Execution Entry Point

Run the deterministic counterexample regression suite:

```bash
python .agents/skills/counterexample-suite/scripts/run_counterexamples.py
```

## Standard Counterexample Controls

1. **Davenport-Heilbronn Function**:
   - Satisfies the Riemann functional equation: $f(s) = \chi(s) f(1-s)$.
   - Has real values on the critical line.
   - **Crucial distinction**: Does NOT possess an Euler product.
   - **Result**: Possesses infinitely many zeros off the critical line in the critical strip (e.g. at $\sigma \approx 0.8085, t \approx 85.6993$).
   - **Audit role**: Proves that functional equation + critical-line reality does NOT imply RH without Euler product structure.

2. **Centrifuge Off-Line Amplification Control**:
   - Tests that any synthetic off-line zero ($\delta \neq 0$) experiences strict exponential growth $|q_\rho^K| = \tau^{K\delta} \neq 1$.

3. **Dirichlet Divergence Control**:
   - Confirms that naive Dirichlet series summation diverges / fails in the critical strip.
