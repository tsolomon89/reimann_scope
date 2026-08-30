# Mathematical Audit Review: CLM-CT-022 (Derivation Facet)

- **Claim ID**: `CLM-CT-022`
- **Claim Title**: Diagonal Cross-Term Exact Cancelling Variances
- **Review Facet**: Exact Analytical & Symbolic Derivation
- **Audit Session Provenance**:
  - *Session ID*: `8196eb63-c434-4dc2-8180-cfbeb4bf00be`
  - *Start SHA*: `3306315edaeb6934f57c28e97cf864bbe6cd92d0`
  - *Target Commit*: `79c1cb849925232d3080ffba0b26cfdf3a67732a`
  - *Inherited Context*: `MATH_CONTRACT.md`, `CURVATURE_TRANSPORT.md`, `.agents/claims/CLM-CT-022.json`
  - *Tools Used*: SymPy 1.12, Lean 4.14.0 (Mathlib)
  - *Cross-Facet Visibility*: Conducted under independent algebraic derivation rules without assuming numerical outputs.

## 1. Object Derivation from Definitions

For the conditional Dirichlet polynomial model $P(z) = \sum_{n\ge 2} \Lambda(n) n^{-1/2-z}$ with grade dilation $F_h(z) = P(\tau^h z)$:
1. Jet expansion at $h=0$:
   $$\dot F_0(z) = -(\log\tau) z \sum_{n\ge 2} \Lambda(n) (\log n) n^{-1/2-z}$$
   $$\ddot F_0(z) = (\log\tau)^2 \sum_{n\ge 2} \Lambda(n) \left[ -z\log n + z^2(\log n)^2 \right] n^{-1/2-z}$$
2. Centered coordinates $z = a + it$:
   $$\Re\left( -z\log n + z^2(\log n)^2 \right) = -a\log n + (a^2 - t^2)(\log n)^2$$
3. Taking the diagonal expectation under probability density window $W(t)$ with second moment variance $v = \langle t^2 \rangle_W$:
   $$\mathfrak X_{\zeta,\mathrm{diag}}(a, v) = (\log\tau)^2 \sum_{n\ge 2} \Lambda(n)^2 n^{-1-2a} \left[ -a\log n + (a^2 - v)(\log n)^2 \right]$$
4. Defining $S_1(a) = \sum_{n\ge 2}\Lambda(n)^2 n^{-1-2a}\log n$ and $S_2(a) = \sum_{n\ge 2}\Lambda(n)^2 n^{-1-2a}(\log n)^2$:
   $$\mathfrak X_{\zeta,\mathrm{diag}}(a, v) = (\log\tau)^2 \left[ (a^2 - v)S_2(a) - a S_1(a) \right]$$

## 2. Cancellation Root Derivation

Setting $\mathfrak X_{\zeta,\mathrm{diag}}(a, v) = 0$:
$$(a^2 - v)S_2(a) - a S_1(a) = 0 \iff v S_2(a) = a^2 S_2(a) - a S_1(a) \iff v_*(a) = a^2 - a\frac{S_1(a)}{S_2(a)}$$

## 3. Positivity Domain Derivation

Since $\log n \ge \log 2$ for all $n \ge 2$, $S_2(a) \ge (\log 2) S_1(a) > 0$. Thus $\frac{S_1(a)}{S_2(a)} \le \frac{1}{\log 2}$.
For any $a > \frac{1}{\log 2} \approx 1.442695$:
$$v_*(a) \ge a\left(a - \frac{1}{\log 2}\right) > 0$$

## 4. Formalization Verification

Formally proved in Lean 4 without axioms in `formal/RiemannScope/CurvatureTransport.lean`:
- `diagonal_crossterm_algebraic_reduction`
- `diagonal_crossterm_cancelling_variance_zero`
- `cancelling_variance_pos_of_bounds`
- `cancelling_variance_pos_of_log2_bound`
