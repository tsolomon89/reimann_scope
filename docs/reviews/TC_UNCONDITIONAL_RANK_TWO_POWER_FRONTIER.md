# TASK-TC-029: Unconditional Rank-Two Algebraic-Power Frontier

## Executive Summary

This research report documents the completion of **TASK-TC-029**, systematically resolving the mathematical and architectural status of the unconditional rank-two algebraic-power frontier in `RiemannScope`.

The core question investigated is:
$$\text{What, if anything, can be proved unconditionally about } (2\pi)^\alpha, (2\pi)^\beta \text{ for } \alpha/\beta \notin \mathbb{Q}?$$

### Key Findings
1. **The Opening Gate Implementation Repairs**:
   All five targeted defects from the post-TASK-TC-028R audit have been repaired, tested, and certified:
   - `compute_rational_support_rank` now fails closed with `ValueError("EXACT_RANK_UNRESOLVED: ...")` when exact number-field reduction fails, never returning an unjustified fallback rank `2`.
   - `expr_to_arb` now fails closed with `ValueError("UNSUPPORTED_EXACT_EXPRESSION_FOR_ARB: ...")` on expressions outside the certified algebraic grammar, eliminating uncertified decimal fallback conversions.
   - The zeta-to-kernel firewall parses arguments semantically via regular expressions; `zeta(2n+1)`, `zeta(21)`, `zeta(3)`, and `zeta(5)` are classified as `ALGEBRAICITY_UNPROVED`, while `zeta(2)` and `zeta(4)` are classified as `PROVED_TRANSCENDENTAL`.
   - The logarithm firewall rule is scoped to logarithms of algebraic non-units (`log(p)` $\to$ `PROVED_TRANSCENDENTAL`), while logarithms of transcendental bases (`log(2*pi)`, `log(tau)`) are classified as `ALGEBRAICITY_UNPROVED`.
   - Lean theorem reporting references only actual committed Lean identifiers; Schanuel Case B is corrected to "algebraic multiple of $L$"; and $(\sqrt{2}, \sqrt{3})$ as well as $(1, \sqrt{2})$ are designated as canonical minimal rank-two open instances (`CANONICAL_MINIMAL_RANK_TWO_OPEN_INSTANCE`).

2. **The Sharp Unconditional Boundary**:
   We establish the definitive boundary separating unconditionally proved theorems, reductions to lower-rank sets, and open transcendence conjectures:
   - **Rank 0**: Unconditionally trivial coefficient cancellation ($\sum c_i = 0$).
   - **Rank 1 Rational**: Unconditionally injective by Lindemann (1882) ($\tau^{p/q} \notin \overline{\mathbb{Q}}$).
   - **Rank 1 Irrational**: Completely classified by $S_\tau$; Gelfond-Schneider forces $\dim_{\mathbb{Q}} S_\tau \le 1$.
   - **Rank 2 Linear Binomials**: $c_1 X + c_2 Y = 0$ ($c_1, c_2 \in \overline{\mathbb{Q}}^\times$) forces $Y/X = \tau^{\beta - \alpha} \in \overline{\mathbb{Q}}$. For rational difference $\beta - \alpha \in \mathbb{Q} \setminus \{0\}$, this is **unconditionally impossible** by Lindemann. For irrational differences, it reduces strictly to $\beta - \alpha \in S_\tau$.
   - **Rank 2 Monomials**: For $M_{m,n} = X^m Y^n = \tau^{m\alpha + n\beta}$ with $(m,n) \neq (0,0)$:
     - If $m\alpha + n\beta \in \mathbb{Q} \setminus \{0\}$, $M_{m,n}$ is **unconditionally transcendental** by Lindemann (1882). No algebraic monomial relation exists.
     - If $m\alpha + n\beta \notin \mathbb{Q}$, $M_{m,n} \in \overline{\mathbb{Q}} \iff m\alpha + n\beta \in S_\tau$ (reduces to $\dim_{\mathbb{Q}} S_\tau \le 1$).
   - **Rank 2 Quadratic Conjugates**: For $\alpha = a + b\sqrt{d}, \alpha' = a - b\sqrt{d} \in \mathbb{Q}(\sqrt{d})$ ($a, b \in \mathbb{Q}^\times$), generators $X = \tau^\alpha, X' = \tau^{\alpha'}$ satisfy the unconditional trace/norm product law:
     $$X \cdot X' = \tau^{\alpha + \alpha'} = \tau^{2a} = (2\pi)^{2a}.$$
     For $2a = p/q \in \mathbb{Q} \setminus \{0\}$, $(X X')^q = (2\pi)^p$. By Lindemann, $X \cdot X'$ is **unconditionally transcendental** over $\mathbb{Q}$. This provides an exact algebraic relation over $\overline{\mathbb{Q}}(2\pi)$, while independence over $\overline{\mathbb{Q}}$ alone remains open unconditionally.
   - **Rank 2 General Polynomials**: $P(X, Y) = 0$ over $\overline{\mathbb{Q}}$ remains an open problem in modern transcendental number theory. Certified finite relation exclusion is established via Arb interval arithmetic. Under Schanuel's Conjecture, no non-trivial polynomial relation can exist.

---

## 1. Opening Gate Repairs & Regression Audit

| Gate Defect | Root Cause | Implemented Repair | Verification Status |
| :--- | :--- | :--- | :--- |
| **1. Exact Rank Fallback** | Silent fallback `return 2, diffs` on exception | Raises `ValueError("EXACT_RANK_UNRESOLVED: ...")` | Passed (`test_25_fail_closed_exact_rational_support_rank`) |
| **2. `expr_to_arb` Fallback** | Uncertified decimal `str(s.evalf(...))` | Raises `ValueError("UNSUPPORTED_EXACT_EXPRESSION_FOR_ARB: ...")` | Passed (`test_26_fail_closed_expr_to_arb_unsupported`) |
| **3. Firewall Rule Ordering** | Substring `"zeta(2"` matched `zeta(2n+1)` and `zeta(21)` | Semantic regex parsing in `classify_firewall_token` | Passed (`test_27_firewall_semantic_regex_order_and_log_rules`) |
| **4. Broad Logarithm Rule** | `"log("` classified all logs as transcendental | Distinguishes algebraic non-units (`log(p)`) from transcendental bases (`log(2*pi)`) | Passed (`test_27_firewall_semantic_regex_order_and_log_rules`) |
| **5. Lean Identifiers & Wording** | Invented friendly Lean identifiers in report; "rational multiple" in Case B | Reports cite exact committed Lean names; Schanuel Case B corrected to "algebraic multiple of $L$"; `CANONICAL_MINIMAL_RANK_TWO_OPEN_INSTANCE` adopted | Verified across codebase and docs |

---

## 2. Mathematical Frontier: Unconditional vs Conditional Status

### Canonical Families Investigated

1. **Base-One Canonical Instance**: $\alpha_1 = 1, \alpha_2 = \sqrt{2}$, with generators $X = 2\pi, Y = (2\pi)^{\sqrt{2}}$.
   - $X$ is proved transcendental by Lindemann (1882).
   - Is $Y = (2\pi)^{\sqrt{2}}$ transcendental?
     - *Gelfond-Schneider (1934)*: Requires an algebraic base $a \in \overline{\mathbb{Q}} \setminus \{0, 1\}$. Because $2\pi$ is transcendental, Gelfond-Schneider is **inapplicable**.
     - *Six Exponentials Theorem (Siegel 1949, Lang 1966, Ramachandra 1968)*: For matrices involving $\log(2\pi)$ and $1$, the exponential entries include $e, 2\pi, e^{\sqrt{2}}$, which are already transcendental. Hence Six Exponentials is **trivially satisfied** without forcing $(2\pi)^{\sqrt{2}}$ to be transcendental.
     - *Four Exponentials Conjecture*: Trivially satisfied by the transcendence of $e$ and $2\pi$.
     - *Status*: Unconditionally open in current literature (Waldschmidt, Nesterenko, Roy).
     - *Arb Certification*: Proved $|P(X, Y)| > 0$ for all non-zero $P \in \mathbb{Z}[X, Y]$ with degree $\le 1$ and height $\le 2$ (124 polynomials).
     - *Conditional Status*: Proved algebraically independent under Schanuel's Conjecture.

2. **Incommensurable Radicals Canonical Instance**: $\alpha = \sqrt{2}, \beta = \sqrt{3}$, with generators $X = (2\pi)^{\sqrt{2}}, Y = (2\pi)^{\sqrt{3}}$.
   - Support rank of $\{0, \sqrt{2}, \sqrt{3}\}$ is 2; with 1 it is rank 3.
   - Gelfond-Schneider and Six Exponentials are similarly inapplicable to force independence unconditionally.
   - *Arb Certification*: Certified finite relation exclusion up to degree 1, height 2 (124 polynomials).
   - *Conditional Status*: Proved algebraically independent under Schanuel's Conjecture.

3. **Quadratic Conjugate Family**: $\alpha = a + b\sqrt{d}, \alpha' = a - b\sqrt{d}$ ($a, b \in \mathbb{Q}^\times, d \in \mathbb{Z}_{>0}$ square-free).
   - Trace is rational: $\operatorname{Tr}(\alpha) = \alpha + \alpha' = 2a = p/q \in \mathbb{Q}^\times$.
   - Norm is rational: $N(\alpha) = \alpha \alpha' = a^2 - db^2 \in \mathbb{Q}$.
   - **Unconditional Trace/Norm Product Identity**:
     $$X \cdot X' = \tau^\alpha \cdot \tau^{\alpha'} = \tau^{2a} = (2\pi)^{2a}.$$
     Taking $q$-th powers:
     $$(X \cdot X')^q = (2\pi)^p.$$
   - **Transcendence**: By Lindemann (1882), $(2\pi)^p$ is transcendental, so $X \cdot X'$ is **unconditionally transcendental** over $\mathbb{Q}$.
   - **Algebraic Independence**:
     - Over $\overline{\mathbb{Q}}(2\pi)$, $X$ and $X'$ have transcendence degree at most 1 via the polynomial $(X X')^q - (2\pi)^p = 0$.
     - Over $\overline{\mathbb{Q}}$ alone, no non-zero polynomial relation exists conditionally by Schanuel's Conjecture; unconditionally it is certified finite relation exclusion.

4. **Monomial Reductions**:
   - Every Laurent monomial $M_{m,n} = X^m Y^n = \tau^{m\alpha + n\beta}$ corresponds to a single grade $\theta = m\alpha + n\beta$.
   - **Rational Case** ($\theta \in \mathbb{Q} \setminus \{0\}$): $M_{m,n} = \tau^{p/q}$ is **unconditionally transcendental** (Lindemann 1882). No non-trivial algebraic monomial relation of rational grade can exist.
   - **Irrational Case** ($\theta \notin \mathbb{Q}$): $M_{m,n} \in \overline{\mathbb{Q}} \iff \theta \in S_\tau$. Reduces strictly to the rank-1 classification set $S_\tau$, which satisfies $\dim_{\mathbb{Q}} S_\tau \le 1$ unconditionally.

---

## 3. Sharp Unconditional Boundary Matrix

```
+------------------------------------+---------------------------------------+---------------------------------------+
| Support / Relation Class           | Unconditional Status                  | Conditional Status (Schanuel)         |
+------------------------------------+---------------------------------------+---------------------------------------+
| Rank 0 (Identical grades)          | PROVED_EXACT_EQUIVALENCE              | PROVED_EXACT_EQUIVALENCE              |
|                                    | sum c_i * tau^K0 = 0 <==> sum c_i = 0 | Injective on non-zero quotient        |
+------------------------------------+---------------------------------------+---------------------------------------+
| Rank 1 Rational (alpha in Q \ {0}) | PROVED_INJECTIVE_LINDEMANN            | PROVED_INJECTIVE_LINDEMANN            |
|                                    | tau^(p/q) transcendental (1882)       | ev_tau injective on Q*alpha           |
+------------------------------------+---------------------------------------+---------------------------------------+
| Rank 1 Irrational (alpha not in Q) | EXACTLY_CLASSIFIED_BY_S_TAU           | PROVED_INJECTIVE_SCHANUEL             |
|                                    | dim_Q S_tau <= 1 (Gelfond-Schneider)  | S_tau = {0}, ev_tau injective         |
+------------------------------------+---------------------------------------+---------------------------------------+
| Rank 2 Linear Binomials            | PARTIALLY_PROVED_LINDEMANN_AND_REDUC. | PROVED_INJECTIVE_SCHANUEL             |
| c1 * X + c2 * Y = 0                | Rational diffs impossible; irrat.->S_t| No non-trivial linear relations       |
+------------------------------------+---------------------------------------+---------------------------------------+
| Rank 2 Monomials                   | PARTIALLY_PROVED_LINDEMANN_AND_REDUC. | PROVED_INJECTIVE_SCHANUEL             |
| X^m * Y^n in Q_bar                 | Rational grades trans.; irrat.->S_tau | No non-trivial algebraic monomials    |
+------------------------------------+---------------------------------------+---------------------------------------+
| Rank 2 Quadratic Conjugates        | PROVED_TRANSCENDENTAL_OVER_QBAR_TAU   | PROVED_INJECTIVE_SCHANUEL_OVER_QBAR   |
| X * X' = (2*pi)^(2a)               | Exact relation over Q_bar(2*pi)       | trdeg_Qbar(X, X') = 2                 |
+------------------------------------+---------------------------------------+---------------------------------------+
| Rank 2 General Polynomials         | OPEN_FRONTIER_WITH_CERTIFIED_EXCLUS.  | PROVED_INJECTIVE_SCHANUEL             |
| P(X, Y) = 0 over Q_bar             | Certified finite box exclusions (Arb) | trdeg_Qbar(X, Y) = 2                  |
+------------------------------------+---------------------------------------+---------------------------------------+
```

---

## 4. Formal Lean 4 Verification

The formal Lean 4 module `formal/RiemannScope/AmbientKernel.lean` contains 0 `sorry` declarations, passes `lake build` with exit code 0, and establishes:

### Actual Committed Lean Identifiers
1. **Support Translation Invariance**:
   - `tau_pow_translation`
   - `sum_tau_pow_translation_two`
   - `sum_tau_pow_translation_three`
   - `sum_tau_pow_zero_iff_translated_zero_two`
   - `sum_tau_pow_zero_iff_translated_zero_three`
2. **Rank-Zero Trivial Cancellation**:
   - `rank_zero_evaluation_factor`
   - `rank_zero_kernel_iff`
   - `rank_zero_kernel_three_iff`
3. **Support Affine Invariance**:
   - `base_change_linear_span`
   - `support_affine_difference_base_change`
4. **Rank-One Classification & Rigidity**:
   - `s_tau_explicit_kernel_witness`
   - `s_tau_explicit_kernel_witness_scaled`
   - `rank_one_injective_of_transcendental_power`
5. **Group-Algebra Law & Laurent Clearing**:
   - `group_algebra_mul_law`
   - `group_algebra_mul_relation_is_structural`
   - `bivariate_monomial_clearing`
   - `pairwise_transcendence_not_algebraic_independence_model`
   - `inverse_pair_algebraic_relation`
6. **Rank-Two Algebraic Power Frontier (TASK-TC-029 Additions)**:
   - `quadratic_conjugate_product_pow`:
     $$\tau^{a+b} \cdot \tau^{a-b} = \tau^{2a}$$
   - `quadratic_conjugate_power_scaling`:
     $$(\tau^{a+b} \cdot \tau^{a-b})^q = (\tau^{2a})^q$$
   - `monomial_exponent_reduction_rank_two`:
     $$(\tau^\alpha)^m \cdot (\tau^\beta)^n = \tau^{m\alpha + n\beta}$$
   - `bivariate_linear_binomial_ratio`:
     $$c_1 X + c_2 Y = 0 \implies Y/X = -c_1 / c_2$$
   - `tau_pow_ratio_sub`:
     $$\tau^\beta / \tau^\alpha = \tau^{\beta - \alpha}$$

---

## 5. Arithmetic Firewall Status

The arithmetic firewall separating the zeta-zero track from the algebraic-power transcendence track remains strictly enforced:
- **Disjoint Tracks**: The zeta-zero arithmetic quantities ($\gamma_1$, $\rho_1$, $\zeta(5)$, $\Gamma(\rho)$) are classified as `ALGEBRAICITY_UNPROVED` and cannot serve as coefficients or grades in the algebraic group algebra $\overline{\mathbb{Q}}[\mathbb{A}_{\mathbb{R}}]$.
- **Zero Bridge Independence**: The audit finding `NO_ZETA_TO_KERNEL_BRIDGE_FOUND` remains an audit finding, completely decoupled from the transcendental number theory frontier of $(2\pi)^\alpha, (2\pi)^\beta$.
