---
name: circularity-detector
description: Screens proposed mathematical arguments and proof steps for circular dependencies on known RH equivalences (Weil positivity, Li's criterion, Mertens bounds, Beurling-Nyman) and pseudo-symmetries.
---

# Circularity Detector Skill

Use this skill when auditing a mathematical derivation or proposed lemma to verify that it does not assume an equivalent form of the Riemann Hypothesis or smuggle in unproven premises.

## Decision Procedure for Circularity Screening

1. **Premise Inventory**:
   - Extract all explicit and implicit assumptions used in the proposed step.

2. **Equivalence Cross-Check**:
   - Check against [references/rh_equivalences.md](./references/rh_equivalences.md).
   - Flag any assumption involving:
     - Positivity of Weil quadratic forms / explicit formula test functions.
     - Positivity of Li's coefficients ($\lambda_n \ge 0$).
     - Density bounds in Nyman-Beurling approximation.
     - Mertens function growth bounds ($M(x) = O(x^{1/2+\varepsilon})$).
     - Global zero-free half-plane assumptions ($\Re(s) > 1/2$).
     - Scale invariance $\zeta(\tau^K s) = \zeta(s)$.

3. **Status Assignment**:
   - If circularity or equivalent assumption is found, mark the claim as `Circular or potentially circular`.
   - Record the exact circular premise in the audit report.
