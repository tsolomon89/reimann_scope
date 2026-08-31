# Derivation Review for Claim CLM-CT-029

**Claim ID**: `CLM-CT-029`
**Reviewer Role**: Agent A — Spectral Formulation Mapping & Arithmetic Obligations
**Status**: `SHARED_SPECTRAL_ZERO_SET_WITH_DISTINCT_ARITHMETIC_OBLIGATIONS`
**Date**: August 31, 2026 (Audit Repair Sprint)

> [!NOTE]
> **Historical Provenance Note**: This review supersedes the August 30, 2026 review. The claim establishes that the five spectral zero-rigidity representations in the repository share the exact critical-line spectral zero set, while maintaining distinct arithmetic representations and unproved arithmetic descent obligations without functional route isomorphism.

## Mathematical Mapping & Master Obligation

1. **Five Spectral Zero-Rigidity Formulations**:
   - **Radial-Defect Quotient (RDQ)**: $\operatorname{Tr}(R) = \sum_\rho \frac{\delta_\rho^2}{\gamma_\rho^2}$.
   - **Curvature Transport**: $\frac{\mathcal B_\rho''(0)}{2(\log\tau)^2} = \delta_\rho^2$.
   - **Weil-Hermitian Involution Defect**: $\operatorname{Defect}(\rho) = \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2}$.
   - **CMSA Resolvent Response**: $\Delta Z_\sigma(z) = \frac{2\delta_\rho^2}{(z-i\gamma)((z-i\gamma)^2-\delta^2)}$.
   - **Fibre Sesquilinear Form**: $\mathcal M_K''(0) = 2N_\gamma \sum_\rho \delta_\rho^2$.

2. **Shared Spectral Zero Set**:
   All 5 formulations satisfy the same zero-rigidity equivalence on the spectral side:
   $$\sum_j w_j \delta_j^2 = 0 \iff \forall j, \delta_j = 0 \iff \zeta(s) \text{ has no off-line zeros in the critical strip}.$$
   The spectral zero set $\{ \rho \in \mathbb{C} : \zeta(\rho) = 0 \}$ is identical across all 5 representations.

3. **Distinct Arithmetic Representations & Unproved Obligations**:
   While their spectral vanishing conditions are equivalent, their arithmetic representations differ:
   - RDQ couples to finite-difference prime trace sums.
   - Curvature Transport couples to windowed grade jet cross-terms $\langle G_0, \ddot G_0\rangle_W$.
   - Weil-Hermitian defect couples to the global explicit formula distribution $W_{\text{prime}}(f * f^*)$.
   - CMSA couples to integrated quartet resolvent integrals.
   None of these five spectral representations autonomously computes $\mathcal A_{\text{arith}} = 0$. All five remain dependent on the single Master Arithmetic Descent Obligation `OBL-RADIAL-DEFECT-DESCENT`.

**Assigned Classification**: `SHARED_SPECTRAL_ZERO_SET_WITH_DISTINCT_ARITHMETIC_OBLIGATIONS`.
