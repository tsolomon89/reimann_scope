---
name: zeta-proof-audit
description: Comprehensive theorem-level mathematical claim audit capability. Enforces strict 18-field claim specifications, 10 mandatory pre-acceptance gates, Lean formalization loops, and executable anti-pattern validation before any claim classification is accepted.
---

# Zeta Proof Audit Skill

This skill provides an audit framework to ensure mathematical claims in the repository are derived from first principles, challenged adversarially, verified symbolically, checked against counterexamples, and formally verified in Lean 4 before being classified as proved, closed, or accepted.

## 1. Claim Specification Schema

Every consequential mathematical claim proposed in this repository must provide an exact JSON or YAML claim specification containing all 18 mandatory fields:

```json
{
  "claim_id": "CLM-...",
  "statement": "Exact mathematical proposition in LaTeX",
  "quantified_variables": ["List of all bound and free variables"],
  "variable_domains": {"var": "exact mathematical domain"},
  "hypotheses": ["Explicit list of every hypothesis and condition"],
  "object_studied": "Precise mathematical object (e.g., prime-only Dirichlet series P(z), completed xi-function \\xi(s), windowed L^2 inner product)",
  "fourier_normalization": "Fourier transform convention (e.g. \\widehat f(\\xi) = \\int f(t) e^{-it\\xi} dt)",
  "multiplicity_convention": "Zero/pole multiplicity treatment",
  "measure_and_window": "Exact integration measure and window class (e.g. W \\in C_c^\\infty(\\mathbb R), W \\ge 0, \\int W = 1)",
  "order_of_limits": "Explicit limit ordering (e.g. N \\to \\infty before T \\to \\infty, or h \\to 0 at fixed T)",
  "exact_conclusion": "Strict mathematical conclusion",
  "logical_negation": "Exact logical negation \\neg (conclusion)",
  "epistemic_role": "ALGEBRAIC_IDENTITY | FINITE_ANALYTIC_COMPONENT | LOAD_BEARING_ANALYTIC_THEOREM | NO_GO_COMPONENT | COUNTERMODEL | HEURISTIC",
  "dependencies": ["List of upstream claims, lemmas, and external theorems"],
  "proof_artifact": "Path to Lean formalization, SymPy script, or certified derivation",
  "falsification_attempts": ["Summary of adversarial checks, counterexamples, boundary limits, and zero-crossings tested"],
  "computational_evidence": ["Arb ball enclosures, mpmath evaluations, regression test paths"],
  "external_sources": [{"source": "Citation", "theorem": "Thm number/page", "statement": "Text", "hypotheses_map": "Mapping to repo"}],
  "remaining_analytic_dependencies": ["List of unproved analytical obligations required for global validity"]
}
```

> [!CRITICAL]
> **Object-Identity Rule**: The `object_studied` field strictly forbids renaming or substituting mathematical objects without an explicit theorem. For example, a Dirichlet polynomial $P(z) = \sum_{n \le N} \Lambda(n) n^{-1/2-z}$ or prime-only series may **never** be labeled as "the completed Riemann zeta function" $\xi(s)$ without explicitly restoring the gamma factor, pole terms, and proving convergence.

---

## 2. The 10 Mandatory Pre-Acceptance Gates

Before any claim can be classified as `PROVED`, `CLOSED`, or `ACCEPTED`, it must pass all 10 gates:

### Gate 1: Object-Identity Audit
Confirm that the formula derives from the named mathematical object, including pole, gamma, prime, window, Jacobian, and subtraction terms where applicable.
* **Failure mode**: Omitting the archimedean $\Gamma$-factor or pole subtraction while claiming a result for $\xi(s)$.

### Gate 2: Quantifier Audit
Rewrite the claim with explicit quantifiers ($\forall, \exists$). Determine whether it concerns:
* all parameters ($\forall a > 0, \forall v \ge 0$);
* some parameters ($\exists v > 0$);
* a fixed canonical parameter ($v = v_0$);
* sampled parameters ($a \in \{1, 2\}$);
* an asymptotic limit ($T \to \infty$ or $h \to 0$).
* **Failure mode**: Generalizing a point evaluation $a=1, v=0$ to a universal $\forall a, v$ theorem.

### Gate 3: Negation-First Audit
Formulate the exact logical negation of the proposed theorem before attempting proof. Actively seek to construct a witness for the negation.
* **Failure mode**: Searching only for confirming instances while ignoring parameters where the claim fails.

### Gate 4: Symbolic Elimination & Equality-Case Audit
If the target expression is algebraic or affine in any parameter (e.g. affine in window variance $v$):
1. Set the expression equal to zero and solve for the parameter symbolically: $v_*(a)$.
2. Check if $v_*(a)$ is feasible within the allowed parameter domain (e.g., $v_*(a) > 0$).
3. Substitute $v_*(a)$ back to verify exact cancellation to zero.
4. Only if no feasible solution exists may a non-vanishing or strict sign theorem be asserted.
* **Failure mode**: Claiming $\mathfrak X_\zeta \ne 0$ when $v_*(a) = a^2 - a S_1(a)/S_2(a) > 0$ is a valid positive variance.

### Gate 5: Dominance and Boundary Audit
Audit all parameter boundaries ($a \to 0^+$, $a \to \infty$, $v \to 0$, $v \to \infty$):
* Compute small-parameter and large-parameter asymptotic expansions.
* Identify which power actually dominates (e.g. quadratic $a^2$ vs linear $a$).
* Ensure endpoint behaviors are not fallaciously assumed to hold across the entire interior.

### Gate 6: Diagonal / Off-Diagonal Audit
For every inner product, mean square, or quadratic functional of Dirichlet series:
$$\langle F, G \rangle_W = \sum_{m,n} c_m \bar d_n \int W(t) e^{-it\log(m/n)} dt$$
* Explicitly separate the diagonal sum ($m = n$) from the off-diagonal double sum ($m \ne n$).
* Any claim of exact diagonalization requires an explicit infinite-mean theorem (e.g. Bohr/Besicovitch) and cannot retain a finite-window variance $\langle t^2 \rangle_W$ without an explicit theorem.

### Gate 7: Interchange Audit
For every interchange of limits, derivatives, and integrals:
$$\frac{d}{dh} \int W(t) |F_h(t)|^2 dt, \quad \int \sum \leftrightarrow \sum \int, \quad \lim_{T\to\infty} \sum \leftrightarrow \sum \lim_{T\to\infty}$$
Record the dominating function, uniform convergence theorem, or Sobolev bound justifying the interchange.

### Gate 8: Independent Derivation Audit
Derive the decisive expression by two independent routes (e.g., frequency-domain Fourier transform vs time-domain differential operator, or algebraic expansion vs contour integration). Tests must not calculate expected values by calling the same code under test.

### Gate 9: Adversarial Falsification Audit
Construct adversarial test cases:
* Exact cancellation points.
* Extreme aspect ratios.
* Non-Euler Dirichlet series (Davenport-Heilbronn) to test if Euler product is truly load-bearing.
* Off-line synthetic zeros ($\delta \ne 0$).

### Gate 10: Evidence Classification Audit
Strictly distinguish proof from computation:
* Floating-point checks, high-precision Arb evaluations, and passing test grids are **numerical evidence**, never mathematical proofs.
* Proof requires formal symbolic reduction or certified Lean 4 deduction.

---

## 3. Executable Enforcement

Run the automated claim validator:

```bash
python .agents/skills/zeta-proof-audit/scripts/audit_claim_spec.py --claim-file <path_to_spec.json>
```

Or run the full audit test suite:

```bash
pytest .agents/verification/test_claim_audit_gates.py
```

---

## 4. Lean 4 Formalization Loop

For any theorem formalized in Lean 4:

1. **State the finite theorem honestly**: Include all explicit hypotheses; do not embed unproved asymptotic assumptions in definitions.
2. **Compile**: Run `lake build` in `formal/`.
3. **Inspect earliest failure**: Analyze the first error or missing tactic step.
4. **Narrow repair**: Fix the mathematical hypothesis or proof step.
5. **Iterate until zero sorry/admit**: Ensure `lake build` compiles cleanly with no `sorry`, no `admit`, and no undeclared axioms.

---

## 5. Independent Red-Team Protocol

When evaluating high-stakes claims:
1. **Derivation Role**: Derives the identity from first principles.
2. **Falsification Role**: Given the exact statement and quantifier domain, actively attempts to find counterexamples, zero-crossings, and boundary violations without reading the derivation's optimistic steps.
3. **Synthesis**: Reconcile both reports. If a single counterexample or zero-crossing is found, the universal claim must be rejected or restricted.
