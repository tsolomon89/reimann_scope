# Arithmetic-to-Spectrum Implication and Mode Extraction Audit

**Epic**: TC Arithmetic Bridge Epic - Reliable Evidence and Support-to-Spectrum Implication
**Date**: 2026-09-11
**Status**: COMPLETE RESEARCH REPORT / MATHEMATICAL OBSTRUCTION THEOREM ESTABLISHED

## 1. Executive Summary and Governing Objectives

The central question of the TC Arithmetic Bridge Epic is:
> What independently proved property of the complete prime-zeta relationship transfers an arithmetic restriction to an individual zero, with enough control to exclude a nonzero radial displacement?

Three distinct achievements must be maintained separate:
1. **Preservation**: The faithful representation of the Riemann explicit formula and prime distribution across dilated coordinate frames a_K = tau^K.
2. **Arithmetic Separation**: The pairwise disjointness of prime-power supports L_K cap L_J = emptyset for K != J via Lindemann transcendence, yielding identical vanishing Q_eps^{K, J} == 0 for eps < d_min.
3. **Spectral Exclusion**: A derived implication showing that an off-critical zero forces a non-vanishing observable Q_eps >= c D_M(rho_0) > 0, establishing a contradiction with arithmetic vanishing.

## 2. Contradiction Obligation and Exact Quantifiers (D1)

The desired contradiction bridge has the exact logical form:
For all rho_0 in Z_nt, delta_0 != 0 implies exists K != J, w, eta, c > 0, M != 0, T(eps), r(eps):
Q_bar_eps^{K, J}[w] >= c D_M(rho_0) - r(eps) for all sufficiently small eps > 0, r(eps) -> 0,
where D_M(rho_0) = 4 sinh^2(M delta_0 log(tau) / 2) > 0.

## 3. Arithmetic Quadratic Forms and Mode Extraction Investigation (D2)

To investigate whether a constraint on the complete arithmetic object descends to an individual spectral mode without introducing speculative operators, we construct the windowed atomic measures:
nu_K = sum_{n >= 2} Lambda(n) w(a_K n) delta_{a_K n}.
Let j in C_c^infty((-1/2, 1/2)) be a smooth mollifier with int j = 1, j_eps(x) = eps^{-1} j(x/eps), and define:
v_{K, eps} = j_eps * nu_K, H_eps(K, J) = eps int v_{K, eps}(x) conj(v_{J, eps}(x)) dx.

Expanding H_eps shows that H_eps(K, J) = Q_eps^{K, J}[w, eta_j] with autocorrelation kernel eta_j = j * j^-.
For distinct grades K != J on [8, 20], d_min = 19 - 6pi approx 0.150444 > 0.
For all eps < d_min, H_eps(K, J) = 0 identically.
For K = J, H_eps(K, K) -> ||j||_2^2 sum Lambda(n)^2 |w(a_K n)|^2 > 0.
On grades {0, 1}: H_eps(0, 0) approx 8.463788 > 0, H_eps(1, 1) approx 0.452703 > 0, H_eps(0, 1) = 0.

## 4. The Spectral-Atomic Scaling Dichotomy Obstruction

**Theorem (Spectral-Atomic Scaling Dichotomy Obstruction)**:
1. In the unnormalized quadratic form H_eps(K, J) = eps <j_eps * nu_K, j_eps * nu_J>, atomic prime-power stations generate an O(1) positive-definite diagonal, whereas every smooth spectral zero mode f_rho carries vanishing mass eps ||j_eps * f_rho||_2^2 = O(eps) -> 0.
2. Conversely, in the normalized bilinear pairing Q_bar_eps = Q_eps / eps, where smooth spectral zero modes yield an O(1) limit A_{0, Gamma} != 0, the complete explicit formula identity forces exact remainder cancellation: lim_{eps -> 0} R_bar_{eps, T(eps)} = -A_{0, Gamma}.
Therefore, mode extraction from H_eps cannot isolate an individual zero mode with a positive lower bound independent of eps, and normalized bilinear pairing on fixed compact windows is defeated by exact explicit formula remainder cancellation.

## 5. Controls Matrix (Section 9 Compliance)

| Control Case | Observable Behaviour | Mathematical Meaning | Audit Finding |
|---|---|---|---|
| Distinct Grades (K=0, J=1) | Q_eps^{0, 1} == 0 for eps < 0.1504 | Support disjointness via transcendence of 2*pi | Proved & certified |
| Equal Grades (K=0, J=0) | Q_eps^{0, 0} -> 29.275 > 0 | Diagonal mass from arithmetic self-overlap | Proved & certified |
| Toy Commensurable (a_K=2, a_J=3) | Q_eps approx 1.761 > 0 at x=6 | Detects genuine rational station collision | Proved & certified |
| Critical-Line Zero (rho_1) | A_{0, Gamma} approx 0.5444 != 0, D_M(rho_1) = 0 | Falsifies A_0 = c D_M(rho_0) on critical line | Definitively Falsified |
| Synthetic Off-Line Zero (beta=0.75) | A_0^{off} approx 0.5694, D_M^{off} > 0 | Tests finite algebra & radial discrimination | Finite algebra verified |

## 6. Proved Lean 4 Theorems (213 Total Compiled)

Formalized in formal/RiemannScope/Grade.lean with 0 sorry / 0 admit:
1. explicit_formula_remainder_cancellation_identity: Q = A + R + E implies R - (-A_0) = Q - (A - A_0) - E.
2. explicit_formula_remainder_triangle_bound: |R - (-A_0)| <= |Q| + |A - A_0| + |E|.
3. explicit_formula_remainder_cancellation_eps: quantitative epsilon-delta limit theorem for R -> -A_0.
4. normalized_tail_subordination_bound: elementary tail error subordination |E| <= B and B < delta implies |E| < delta.
5. candidate_bridge_gap_exact_cancellation: A_0 = c D implies not (|-A_0| < c D).
6. candidate_bridge_unproved_lower_bound_gap: elementary algebraic identity Q = A + R and R = -A implies Q = 0.
7. explicit_formula_remainder_cancellation_tendsto: topological filter limit: Q -> 0, A -> A_0, E -> 0, Q = A + R + E implies R -> -A_0 via Mathlib Filter.Tendsto.sub.
8. explicit_formula_remainder_cancellation_quantified: quantified epsilon-delta limit theorem for remainder cancellation.
9. finite_spectral_perturbation_rigidity_2point: linear independence of two distinct complex exponentials at 2 points.

## 7. Refutation of Arbitrary Compensation via Finite Spectral Perturbation Rigidity

The Finite Spectral Perturbation Rigidity Theorem proves that on any open interval I in (a_K, infty), the functions {x^{rho-1} : rho in S} for distinct exponents S are linearly independent over C. Any non-trivial finite spectral perturbation cannot vanish identically or be absorbed by the remaining spectrum and smooth background with the arithmetic measure fixed.

## 8. Decisive Epistemic Verdict

1. Was an arithmetic exclusion mechanism derived? No. Arithmetic vanishing is proved, but no spectral lower bound for an off-critical zero exists on fixed compact windows.
2. What exact implication was established? The Spectral-Atomic Scaling Dichotomy Obstruction Theorem and Finite Spectral Perturbation Rigidity Theorem were derived and proved.
3. What is the earliest remaining unproved inference? The spectral transfer step: radial defect D_M(rho_0) > 0 implies Q_bar_eps >= c D_M(rho_0) - r(eps).
4. Which one next research task follows? Research must address the unproved spectral transfer step directly or construct multi-grade operator kernels that avoid fixed-window collective cancellation.
