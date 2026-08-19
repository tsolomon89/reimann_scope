---
name: exact-symbolic-verifier
description: Performs exact symbolic and algebraic verification of mathematical contract identities, coordinate dilations, kernel invariants, and centrifuge relations using SymPy.
---

# Exact Symbolic Verifier Skill

Use this skill to execute exact symbolic checks on coordinate transformations, kernel exponent pairings, zero mapping formulas, and centrifuge derivative relations.

## Execution Entry Point

Run the deterministic SymPy verification script:

```bash
python .agents/skills/exact-symbolic-verifier/scripts/verify_symbolic.py
```

## Verified Identities and Contracts

1. **Origin Coordinate Dilation**: $s' = \tau^K s \implies \Re(s') = \tau^K/2$, $\rho' = \tau^K \rho$.
2. **Centered Coordinate Dilation**: $s' = 1/2 + \tau^K(s-1/2) \implies \Re(s') = 1/2$, $\rho' = 1/2 + \tau^K(\rho-1/2)$.
3. **Inverse Scale Lock**: $AB = 1 \implies (Bs)(A\log n) = s\log n \implies \mathcal{Z}_{A,0,1/A,0}(s) = \zeta(s)$.
4. **General Kernel Zero Map**: $s_\rho = \frac{\rho/A - D}{B}$.
5. **Radial Centrifuge Modulus & Derivative**:
   $$\log |q_\rho^K| = K\delta\log\tau, \qquad \frac{d}{dK}\log |q_\rho^K| = \delta\log\tau.$$
6. **On-Line Invariance**: $\delta = 0 \implies |q_\rho^K| = 1$ for all $K \in \mathbb{R}$.

## Expected Output
The script prints `[PASS]` for all 9 symbolic contract verifications and returns exit code `0`.
