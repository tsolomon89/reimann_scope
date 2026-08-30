# Derivation Review for Claim CLM-CT-029

**Claim ID**: `CLM-CT-029`  
**Reviewer Role**: Agent A — Derivation  
**Date**: August 30, 2026  

## Mathematical Derivation & Route Reconciliation

1. **Spectral Isomorphism of Zero-Rigid Quantities**:
   All 5 surviving routes in the repository evaluate quadratic defect quantities of the form:
   $$\mathcal{E}_{\text{spec}} = \sum_{\rho} w_\rho \Psi(\delta_\rho),$$
   where $w_\rho > 0$, $\Psi(\delta) \ge 0$, and $\Psi(\delta) = 0 \iff \delta = 0$:
   - **RDQ**: $\operatorname{Tr}\mathcal{R} = \sum_{\rho} \frac{\delta_\rho^2}{\gamma_\rho^2}$ ($w_\rho = 1/\gamma_\rho^2, \Psi(\delta) = \delta^2$).
   - **Curvature Transport**: $\mathscr{K}_\tau(\rho) = \sum_{\rho} \delta_\rho^2$ ($w_\rho = 1, \Psi(\delta) = \delta^2$).
   - **Weil-Hermitian**: $\mathcal{D}_{\text{WH}}(\rho) = \sum_{\rho} \frac{2\delta_\rho^2}{|\rho|^2|1-\rho|^2}$ ($w_\rho = \frac{2}{|\rho|^2|1-\rho|^2}, \Psi(\delta) = \delta^2$).
   - **CMSA**: Gate G4 regularized quadratic response $\Delta S_W = \sum_\rho w_\rho \delta_\rho^2$.
   - **Sesquilinear Form**: Fibre curvature $M_K''(0) = 2 \sum_{\gamma} |a_K|^2 N_\gamma \sum_a \delta_{\gamma,a}^2$.

2. **Formal Unification in Lean 4**:
   Formally proved in `formal/RiemannScope/CurvatureTransport.lean` (`master_radial_defect_unification` and `finite_positive_weight_curvature_rigidity`):
   $$\sum_{j} w_j d_j = 0 \iff \forall j, d_j = 0 \quad (w_j > 0, d_j \ge 0).$$
   Thus, vanishing of any one of these spectral representations is strictly equivalent to the vanishing of all others and equivalent to $\mathrm{RH}$.

3. **Master Obstruction**:
   None of these five routes provides an arithmetic calculation that evaluates to 0 without using the zero list.
   They all share the exact same missing arithmetic obligation:
   $$\text{OBL-RADIAL-DEFECT-DESCENT}: \quad \text{Prove } \mathcal{A}_{\text{arith}} = 0 \text{ from prime/functional equation data alone}.$$

**Conclusion**: Exactly ONE viable radial descent branch remains (`ONE_VIABLE_RADIAL_DESCENT_BRANCH_REMAINS`).
