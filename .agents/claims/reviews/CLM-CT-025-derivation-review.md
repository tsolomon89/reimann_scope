# Mathematical Audit Review: CLM-CT-025 (Derivation Facet)

- **Claim ID**: `CLM-CT-025`
- **Claim Title**: Finite Dirichlet Polynomial Inner Product Double-Sum Decomposition
- **Review Facet**: Exact Analytical & Symbolic Derivation
- **Audit Session Provenance**:
  - *Session ID*: `8196eb63-c434-4dc2-8180-cfbeb4bf00be`
  - *Start SHA*: `3306315edaeb6934f57c28e97cf864bbe6cd92d0`
  - *Target Commit*: `79c1cb849925232d3080ffba0b26cfdf3a67732a`
  - *Inherited Context*: `math_core.py`, `.agents/claims/CLM-CT-025.json`
  - *Tools Used*: Lean 4.14.0 (Mathlib), SymPy 1.12
  - *Cross-Facet Visibility*: Structural derivation of finite double-sum identity.

## 1. Mathematical Object Formulation

Let $F_0(t) = \sum_{n=2}^N c_n e^{-it\log n}$ with $c_n = \Lambda(n) n^{-1/2-a}$ on $\Re(z) = a > 0$.
The second grade dilation jet is:
$$\ddot F_0(t) = (\log\tau)^2 \sum_{n=2}^N c_n \left[ -(a+it)\log n + (a+it)^2(\log n)^2 \right] e^{-it\log n}$$

Taking the inner product under an admissible smooth window $W \in \mathcal S(\mathbb R)$ or $W \in C_c^\infty(\mathbb R)$:
$$\langle F_0, \ddot F_0 \rangle_W = \int_{-\infty}^\infty W(t) F_0(t) \overline{\ddot F_0(t)} dt$$

Substituting the finite sums and interchanging with the integral:
$$\langle F_0, \ddot F_0 \rangle_W = (\log\tau)^2 \sum_{m,n=2}^N c_m \overline{c_n} \mathcal I_{m,n}(W)$$
where with $L_n = \log n$ and $\xi_{mn} = \log(m/n)$:
$$\mathcal I_{m,n}(W) = \int_{-\infty}^\infty W(t) e^{-it\xi_{mn}} \left[ -(a-it)L_n + (a-it)^2 L_n^2 \right] dt$$

Expanding the polynomial in $-it$:
$$-(a-it)L_n + (a-it)^2 L_n^2 = (-a L_n + a^2 L_n^2) + (L_n - 2a L_n^2)(it) + L_n^2 (it)^2$$
Expressing in terms of Fourier transforms $\widehat f(\xi) = \int_{-\infty}^\infty f(t) e^{-it\xi} dt$:
$$\mathcal I_{m,n}(W) = (-a L_n + a^2 L_n^2)\widehat W(\xi_{mn}) + i(L_n - 2a L_n^2)\widehat{tW}(\xi_{mn}) - L_n^2 \widehat{t^2 W}(\xi_{mn})$$

## 2. Real-Part Cross-Term Projection

The target real cross-term $\mathfrak X_{N,W} = \Re\langle F_0, \ddot F_0 \rangle_W$ is:
$$\boxed{\mathfrak X_{N,W} = (\log\tau)^2 \Re \sum_{m,n\le N} c_m \overline{c_n} \mathcal I_{m,n}(W)}$$

## 3. General Finite Decomposition in Lean 4

Formalized generally over any `Finset` product in `formal/RiemannScope/CurvatureTransport.lean`:
```lean
theorem finset_double_sum_diag_offdiag_decomp {α : Type*} [DecidableEq α] (s : Finset α) (f : α × α → ℝ) :
    (∑ p ∈ (s ×ˢ s).filter (fun p => p.1 = p.2), f p) + (∑ p ∈ (s ×ˢ s).filter (fun p => p.1 ≠ p.2), f p) =
      ∑ p ∈ s ×ˢ s, f p
```
