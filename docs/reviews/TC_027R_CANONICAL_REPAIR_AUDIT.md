# TASK-TC-027R: Canonical Reconciliation Repair and Formal-Claim Cleanup Audit

This audit documents the concise, issue-by-issue repairs applied during **TASK-TC-027R** to ensure complete repository truthfulness, formal claim alignment, and canonical status consistency.

---

## 1. Formal Dependency Registry: Grade Fiber Commutative Ring

- **Defect Found**: Claim `FORMAL-TC-FIBER-RING` cited nonexistent declaration `GradeFiber.add_left_neg` and claimed full `CommRing` and `RingEquiv` while Lean source only contained individual lemma laws without algebraic structure instances.
- **File / Location**: `formal/RiemannScope/FiberArithmetic.lean` and `data/tc_formal_claim_dependency_registry.json`.
- **Repair Applied**: Formalized `add_left_neg`, `equivZ : GradeFiber K ≃ ℤ`, `instance (K : ℝ) : CommRing (GradeFiber K) := (equivZ K).commRing`, and `ringEquivZ : GradeFiber K ≃+* ℤ` with rewrite lemmas. Updated registry with all 16 real Lean declarations verified verbatim against compiled Lean objects.
- **Resulting Evidence Classification**: `FORMAL_LEAN_PROOF` (100% compiled in Mathlib environment, 0 sorry).

---

## 2. Formal Dependency Registry: Riemann Converter Covariance

- **Defect Found**: Claim `FORMAL-TC-RIEMANN-CONVERTER-COVARIANCE` cited nonexistent theorem identifiers (`two_prime_rigidity`, etc.) and attributed the elementary Lean theorem `dilation_translation_multi_prime_rigidity` to external Lindemann transcendence.
- **File / Location**: `data/tc_formal_claim_dependency_registry.json` and `formal/RiemannScope/RiemannConverter.lean`.
- **Repair Applied**: Replaced registry citations with real Lean declarations (`converter_endpoint_scaling`, `converter_contour_height_scaling`, `dilation_translation_coincidence_iff`, `dilation_translation_multi_prime_rigidity`, `centered_harmonic_analytic_invariance`, `centered_harmonic_arithmetic_shift`). Removed external Lindemann dependency from the elementary Lean theorem; added scope note distinguishing the elementary algebraic theorem from its upstream prime-log specialization.
- **Resulting Evidence Classification**: `FORMAL_LEAN_PROOF` (algebraic rigidity) / `EXTERNAL_ANALYTIC_PROOF` (upstream Lindemann prime-log specialization).

---

## 3. Formal Dependency Registry: Local Germ Covariance

- **Defect Found**: Claim `FORMAL-TC-LOCAL-GERM-COVARIANCE` cited invented identifiers (`zero_germ_scaling_weight`, `unit_normalized_germ_invariance_at_zero`, `reflected_germ_pairing_invariance`).
- **File / Location**: `data/tc_formal_claim_dependency_registry.json` and `formal/RiemannScope/LocalGermInvariance.lean`.
- **Repair Applied**: Replaced citations with exact committed Lean declarations (`centered_germ_scaling`, `centered_real_exponent`, `log_modulus_finite_difference`, `harmonic_translation_exponent`, `harmonic_modulus_exponent`, `unit_normalized_germ_invariance`, `reflected_germ_relation`, `reflected_germ_product_exponent_cancel`, `reflected_germ_product_independent`, `germ_modulus_ratio_detector`).
- **Resulting Evidence Classification**: `FORMAL_LEAN_PROOF`.

---

## 4. Canonical Claim Register: Architectural Stratification & Supersession

- **Defect Found**: Historical auxiliary pullback claims (`CLM-TC-001` through `CLM-TC-004`) were listed in `.agents/corpus_map/claim_register.md` as generic `Transcendental Continuation | PROVED / EXACT` without distinguishing them from canonical arithmetic TC or exposing their superseded status.
- **File / Location**: `.agents/corpus_map/claim_register.md`.
- **Repair Applied**: Added `## Transcendental Continuation Architectural Stratification & Supersession Registry` explicitly categorizing `CLM-TC-001` through `CLM-TC-004` as `ANALYTIC_PULLBACK_AUXILIARY` / `SUPERSEDED_HISTORICAL`, and `CLM-TC-005` through `CLM-TC-022` as `CANONICAL_TC` / `CURRENTLY_ACTIVE`. Preserved Policy B grandfathered table line hashing (0 errors).
- **Resulting Evidence Classification**: `SUPERSEDED_HISTORICAL` (`CLM-TC-001`–`004`) / `CURRENTLY_ACTIVE` (`CLM-TC-005`–`022`).

---

## 5. Formal Declaration-Count Scoping

- **Defect Found**: `docs/reviews/TC_FORMAL_CLAIM_ALIGNMENT_AUDIT.md` ambiguously labeled the 338-declaration subtotal across the 11 audited modules as the "Complete TC Suite", creating confusion with the full formal project build count.
- **File / Location**: `docs/reviews/TC_FORMAL_CLAIM_ALIGNMENT_AUDIT.md`.
- **Repair Applied**: Standardized exact terminology: $\boxed{348 = \text{audited canonical TC module declarations}}$ vs $\boxed{466 = \text{all project theorem declarations in the full formal tree}}$.
- **Resulting Evidence Classification**: `AUDIT_CLASSIFICATION`.

---

## 6. Multi-Grade Naturality & Finite-Path Scoping

- **Defect Found**: Prose documentation asserted arbitrary finite-path loop triviality and arbitrary $r$-ary naturality as if fully formalized in Lean, whereas Lean proves unary, binary, and 2-, 3-, 4-step compositions.
- **File / Location**: `docs/reviews/TC_FORMAL_CLAIM_ALIGNMENT_AUDIT.md` and `docs/reviews/TC_CANONICAL_STATE_AND_MULTIGRADE_NATURALITY_EPIC.md`.
- **Repair Applied**: Scoped explicitly: Unary and binary naturality are Lean-proved; finite-arity extension is routine paper derivation (`PROVED_PAPER_DERIVATION`). Low-order loops (2, 3, 4 steps) are Lean-proved; arbitrary finite paths are `PROVED_PAPER_DERIVATION`.
- **Resulting Evidence Classification**: `FORMAL_LEAN_PROOF` (unary, binary, 2-, 3-, 4-step) / `PROVED_PAPER_DERIVATION` (arbitrary paths / arity).

---

## 7. Canonical vs Historical Pullback Terminology

- **Defect Found**: Historical sections in `MATH_CONTRACT.md` and `TRANSCENDENTAL_CONTINUATION.md` contained ambiguous, canonical-sounding prose ("The project-defined transcendental-continuation family uses origin-dilation semantics") and un-scoped titles ("Transcendental continuation", "Completed transcendental continuation", "Zero worldlines").
- **File / Location**: `MATH_CONTRACT.md` (§3, §4, §5) and `TRANSCENDENTAL_CONTINUATION.md` (§10, §11).
- **Repair Applied**: Retitled sections with explicit "Auxiliary analytic pullback" scoping and updated text to "The historical auxiliary analytic-pullback family uses origin-dilation semantics."
- **Resulting Evidence Classification**: `HISTORICAL_AUXILIARY_DIAGNOSTIC`.

---

## 8. Exceptional Set $S_\tau$ Notation Standardization

- **Defect Found**: The canonical exceptional set $S_\tau$ was occasionally written as $\alpha \in \mathbb{R}$ without the algebraic restriction, and was overloaded with the historical lattice union symbol $\bigcup_{K \in \mathbb{Z}} L_K$.
- **File / Location**: `TRANSCENDENTAL_CONTINUATION.md`, `MATH_CONTRACT.md`, and `docs/TC_CURRENT_CANONICAL_STATUS.md`.
- **Repair Applied**: Standardized definition to $\boxed{S_\tau = \{\alpha \in \mathbb{A}_{\mathbb{R}} : \tau^\alpha \in \overline{\mathbb{Q}}\}}$. Designated the countable dense lattice union as $\mathfrak{L}_\tau = \bigcup_{K \in \mathbb{Z}} L_K$ and added an explicit notation warning distinguishing the two.
- **Resulting Evidence Classification**: `CANONICAL_SPECIFICATION`.

---

## 9. Rank-One Support Theorem Derivation and Upstream Attribution

- **Defect Found**: Rank-one support theorem lacked an explicit step-by-step polynomial reduction derivation and loosely attributed the entire deduction to Lindemann and Gelfond–Schneider.
- **File / Location**: `TRANSCENDENTAL_CONTINUATION.md` §32.4.
- **Repair Applied**: Provided the exact 8-step single-variable polynomial reduction in $X = \tau^{\alpha/D}$ over $\overline{\mathbb{Q}}$ (and $\mathbb{A}_{\mathbb{R}}$) forcing $X \in \overline{\mathbb{Q}}$ hence $\alpha \in S_\tau$. Clarified that Lindemann (1882) and Gelfond–Schneider (1934) are upstream external theorems establishing properties of $S_\tau$.
- **Resulting Evidence Classification**: `PROVED_PAPER_DERIVATION` (polynomial reduction) / `EXTERNAL_ANALYTIC_PROOF` (upstream transcendence theorems).

---

## 10. Canonical Status Document Evidence Section

- **Defect Found**: `docs/TC_CURRENT_CANONICAL_STATUS.md` lacked a structured, 5-part evidence classification summary.
- **File / Location**: `docs/TC_CURRENT_CANONICAL_STATUS.md`.
- **Repair Applied**: Added Section 6 "Evidence Status Summary" with subsections:
  1. *Lean proved*: Exact algebraic/fiber/transfer statements;
  2. *External theorem*: Lindemann, Gelfond–Schneider;
  3. *Paper derivation*: Complex analytic continuation, divisor multiplicity preservation, arbitrary finite paths;
  4. *Audit findings*: "No object found" results;
  5. *Open*: $\ker(\operatorname{ev}_\tau)$ on full algebraic grades and any zeta-to-kernel bridge.
- **Resulting Evidence Classification**: `CANONICAL_STATUS_SUMMARY`.
