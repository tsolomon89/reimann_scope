# Audit Mathematical Claim Workflow

Use `/audit-claim` to submit a mathematical claim, transformation formula, or candidate lemma to the rigorous 4-stage verification pipeline.

## Inputs
- Claim text or mathematical formulation.
- Target document/section where claim will reside.

## Ordered Execution Stages

### Stage 1: Corpus Orientation & Premise Audit
1. Audit the claim against [MATH_CONTRACT.md](../../MATH_CONTRACT.md) and [claim_register.md](../corpus_map/claim_register.md).
2. Explicitly list all premises, variables, and coordinate domains.

### Stage 2: Exact Symbolic Verification
1. Run SymPy symbolic verification:
   `python .agents/skills/exact-symbolic-verifier/scripts/verify_symbolic.py`
2. Confirm exact algebraic reduction of exponents, coordinate maps, and zero maps.

### Stage 3: Certified High-Precision Numerical Check
1. Run arbitrary-precision and ball arithmetic check:
   `python .agents/skills/arbitrary-precision-falsifier/scripts/verify_numerical.py`
2. Record certified error bounds and residual statistics.

### Stage 4: Falsification & Circularity Screening
1. Run counterexample controls:
   `python .agents/skills/counterexample-suite/scripts/run_counterexamples.py`
2. Cross-check against [rh_equivalences.md](../skills/circularity-detector/references/rh_equivalences.md).

### Stage 5: Zeta Proof Audit 10-Gate Validation
1. Construct the 18-field claim specification conforming to [zeta-proof-audit SKILL.md](../skills/zeta-proof-audit/SKILL.md).
2. Run the executable gate validator:
   `python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --claim-file <path_to_spec.json>`
3. Ensure all 10 gates pass without violations.
4. Assign canonical status label (`Derived lemma`, `Algebraic identity`, `Circular or potentially circular`, `Falsified`, `Withdrawn`, etc.).

## Output Artifact
Summary audit report with assigned claim-status label, 10-gate validation results, and test evidence.

