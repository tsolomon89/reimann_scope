---
name: arbitrary-precision-falsifier
description: Performs certified arbitrary-precision evaluation and ball arithmetic using python-flint (Arb) and mpmath to test functional equations, zero residuals, and falsify false invariances.
---

# Arbitrary-Precision Falsifier Skill

Use this skill when evaluating mathematical functions, zero residuals, functional equation symmetries, or testing falsification controls at certified arbitrary precision (e.g. 80-100 decimal digits).

## Execution Entry Point

Run the deterministic high-precision verification script:

```bash
python .agents/skills/arbitrary-precision-falsifier/scripts/verify_numerical.py
```

## Numerical Precision Tiers
- **Preview Tier**: 30–40 decimal digits (used for rapid scanning).
- **Audit Tier**: 80–100 decimal digits (used for certified validation and zero enclosures).

## Verified Properties
1. **Certified Zero Residual**: Enclosure of known roots with residual $|\zeta(1/2+i\gamma)| < 10^{-95}$.
2. **Schwarz Reflection**: $|\zeta(\bar s) - \overline{\zeta(s)}| < 10^{-95}$.
3. **Completed Zeta Functional Equation**: $|\xi(s) - \xi(1-s)| < 10^{-95}$.
4. **Certified Ball Arithmetic**: Arb `acb.contains_zero()` root validation.
5. **Negative Control**: Proves that false invariances (e.g. $\zeta(\tau s) = \zeta(s)$) are unambiguously detected and falsified.

## Critical Constraint
Numerical evaluations provide evidence or falsification; they must never be presented as formal proof of the Riemann Hypothesis.
