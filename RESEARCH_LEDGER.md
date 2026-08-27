# Research Ledger

This file records the current canonical status of research claims in `reimann_scope`.

It is not a historical narrative. Git history preserves superseded paths.

Every proof-facing claim should be classified as one of:

- **PROVED**
- **FALSE**
- **CIRCULAR**
- **KNOWN INSUFFICIENT**
- **OPEN**
- **RESEARCH REQUIREMENT**
- **DESIGN DEFINITION**

No agent should promote a claim without changing its classification here and documenting the reason.

---

# 1. Central framework

| ID | Statement | Classification | Reason |
|---|---|---|---|
| TC-001 | `Transcendental continuation` is the project-defined extension \(\mathcal Z_\tau(s,k)=\zeta(\tau^{-k}s)\). | **DESIGN DEFINITION** | This names the formal framework used by the repo. |
| TC-002 | \(k=0\) recovers ordinary analytically continued zeta: \(\mathcal Z_\tau(s,0)=\zeta(s)\). | **PROVED** | Direct substitution. |
| TC-003 | Integer \(K\) gives the canonical bilateral grade family \(\tau^K\). | **DESIGN DEFINITION** | Canonical project skeleton. |
| TC-004 | Rational grades provide root refinements; real grades provide the full positive continuous scale axis. | **PROVED** | \(\tau^\mathbb R=\mathbb R_{>0}\); rational powers give roots. |
| TC-005 | Transcendental continuation is standard established terminology in analytic number theory. | **FALSE** | It is a project-defined term. |
| TC-006 | The framework itself proves RH. | **FALSE** | It supplies an extended geometry and candidate constraints only. |

---

# 2. Parallel construction and lattice claims

Define

\[
L_K=\tau^K\mathbb Z.
\]

| ID | Statement | Classification | Reason |
|---|---|---|---|
| L-001 | Every \(L_K\) has cardinality \(\aleph_0\). | **PROVED** | Scaling is a bijection from \(\mathbb Z\). |
| L-002 | Distinct integer-grade lattices satisfy \(L_J\cap L_K=\{0\}\). | **PROVED** | A nonzero intersection would make \(\tau^{K-J}\) rational. |
| L-003 | Distinct rational-grade lattices also intersect only at \(0\). | **PROVED** | Nonzero rational powers of transcendental \(\tau\) are transcendental. |
| L-004 | The integer/rational grade lines are scale-isomorphic but arithmetically noncoincident. | **PROVED / TERMINOLOGY** | Summarizes L-001 through L-003. |
| L-005 | Distinct arbitrary real-grade lattices are always noncoincident. | **FALSE** | Example \(k=\log_\tau 2\) gives \(L_k=2\mathbb Z\). |
| L-006 | The coordinate spaces of distinct grades are non-isomorphic. | **FALSE** | Multiplication by the scale ratio gives an invertible real map. |
| L-007 | Parallel construction means one line must be finitely traversed to reach another. | **FALSE** | The framework constructs grades by making grade part of the coordinate. |
| L-008 | Exact symbolic grade identity and finite numerical realization are the same thing. | **FALSE** | The repo explicitly separates them. |

---

# 3. Computation and finite realization

| ID | Statement | Classification | Reason |
|---|---|---|---|
| N-001 | \(\tau^K\) is exactly specifiable symbolically for integer \(K\). | **PROVED / STANDARD** | It is an exact mathematical expression. |
| N-002 | A finite positional numerical representation exhausts the full real value of nonzero \(\tau^K\). | **FALSE** | Its positional expansion is nonterminating. |
| N-003 | Authoritative numerical work should distinguish exact symbolic referent from finite numerical realization. | **RESEARCH REQUIREMENT** | Prevents false exactness claims. |
| N-004 | The repo must take a position on philosophical disputes over the word `computable`. | **FALSE AS REQUIREMENT** | Use `exactly specified, finitely realized` instead. |
| N-005 | Audit computations may silently downcast to binary float. | **FALSE** | Authoritative metrics require arbitrary/high precision. |

---

# 4. Zero worldlines and radial leaves

For a native zero

\[
\rho=\frac12+\delta+i\gamma,
\]

define

\[
s_\rho(k)=\tau^k\rho
\]

and

\[
R_\tau(s,k)=\tau^{-k}\Re(s)-\frac12.
\]

| ID | Statement | Classification | Reason |
|---|---|---|---|
| W-001 | \(s_\rho(k)\) is a zero of \(\mathcal Z_\tau(\cdot,k)\). | **PROVED** | \(\zeta(\tau^{-k}\tau^k\rho)=\zeta(\rho)=0\). |
| W-002 | The critical line becomes \(\Re(s)=\tau^k/2\). | **PROVED** | Origin-dilation image. |
| W-003 | \(R_\tau(s_\rho(k),k)=\delta\) along every zero worldline. | **PROVED** | Exact cancellation. |
| W-004 | Transcendental continuation preserves normalized radial class. | **PROVED** | W-003. |
| W-005 | Compression forces an off-line worldline to intersect the critical surface. | **FALSE** | Absolute defect shrinks but normalized \(\delta\) remains nonzero. |
| W-006 | The existence of multiple mathematical radial leaves is contradictory. | **FALSE** | The ambient geometry permits them. |
| W-007 | RH is equivalent to all actual nontrivial zero worldlines occupying \(R_\tau=0\). | **PROVED REFORMULATION** | Equivalent to \(\Re(\rho)=1/2\). |

---

# 5. Central contradiction programme

| ID | Statement | Classification | Reason |
|---|---|---|---|
| R-001 | If RH is false, the actual nontrivial spectrum contains an occupied \(R_\tau\neq0\) leaf in addition to established \(R_\tau=0\) zeros. | **PROVED CONDITIONAL STRUCTURE** | Definition of a counterexample plus known on-line zeros. |
| R-002 | A counterexample generates a bilateral transcendental radial defect worldline. | **PROVED** | Exact worldline and grade formulas. |
| R-003 | The complete grade family may impose a global coherence law not reducible to coordinate covariance. | **OPEN** | Central discovery target. |
| R-004 | Such a coherence law forces only one occupied radial leaf. | **OPEN** | Missing radial-rigidity theorem. |
| R-005 | `Transcendental Coherence -> Transcendental Radial Rigidity` is the central missing implication. | **OPEN / CURRENT TARGET** | Core proof programme. |
| R-006 | Global participation of all zeros in one xi/zeta object automatically forces one radial leaf. | **FALSE AS AN INFERENCE** | Global dependence does not by itself equal radial rigidity. |
| R-007 | An off-line zero is impossible because there is literally no geometric space left between grade lines. | **FALSE / UNSUPPORTED** | Countable/dense families do not fill the continuum in that sense. |
| R-008 | The train-line intuition is better represented as intersection of exact grade constraints than literal intersection of points. | **CURRENT FORMULATION** | Mathematically stronger and avoids the space-filling error. |

---

# 6. Constraint-intersection programme

Let \(\mathcal C_K\) denote the exact analytic/arithmetic constraint set associated with grade \(K\).

| ID | Statement | Classification | Reason |
|---|---|---|---|
| CI-001 | The actual spectrum must satisfy all correctly derived grade constraints simultaneously. | **PROVED AS LOGIC** | If each constraint follows from the same object, all apply. |
| CI-002 | \(\bigcap_K\mathcal C_K\) permits only one radial leaf. | **OPEN** | This is a candidate rigidity theorem, not yet known. |
| CI-003 | Independent noncoincident arithmetic grade lattices automatically imply CI-002. | **FALSE AS AN INFERENCE** | Additional zeta-specific coupling is required. |
| CI-004 | The proof search should look for an exact incompatibility of mixed radial exponents across all required grades. | **RESEARCH REQUIREMENT** | Current no-compensation direction. |

---

# 7. Tau-grade zero character

For

\[
q_\rho=\tau^{\rho-\frac12},
\]

| ID | Statement | Classification | Reason |
|---|---|---|---|
| Z-001 | \(|q_\rho|=\tau^\delta\). | **PROVED** | Exact algebra. |
| Z-002 | \(|q_\rho^K|=\tau^{K\delta}\) for integer \(K\), positive or negative. | **PROVED** | Exact algebra. |
| Z-003 | \(\delta=0\) implies \(|q_\rho^K|=1\) for all bilateral grades. | **PROVED** | Z-002. |
| Z-004 | \(\delta\neq0\) produces expansion in one grade direction and contraction in the other. | **PROVED** | Z-002. |
| Z-005 | Grade amplification itself excludes off-line zeros. | **KNOWN INSUFFICIENT** | No exclusion law follows from amplification alone. |
| Z-006 | Bilateral boundedness of one isolated mode is a weaker non-circular intermediate statement than RH. | **CIRCULAR** | It is already equivalent to \(\delta=0\) for that mode. |

---

# 8. Exact symmetry-complete defect

For

\[
\rho_\pm=\frac12\pm\delta+i\gamma,
\qquad
\rho_0=\frac12+i\gamma,
\]

define

\[
D_K=q_+^K+q_-^K-2q_0^K.
\]

| ID | Statement | Classification |
|---|---|---|
| D-001 | \(D_K=2e^{iK\gamma\log\tau}[\cosh(K\delta\log\tau)-1]\). | **PROVED** |
| D-002 | \(|D_K|=4\sinh^2(K\delta\log\tau/2)\). | **PROVED** |
| D-003 | The defect is even in \(\delta\). | **PROVED** |
| D-004 | Near \(K\delta=0\), \(|D_K|\sim(K\delta\log\tau)^2\). | **PROVED** |
| D-005 | The symmetry-complete defect proves RH. | **KNOWN INSUFFICIENT** |

---

# 9. Spectrum-wide grade identity

For \(K>0\),

\[
\sum_\rho\frac{q_\rho^K}{\rho}
=
\tau^{-K/2}
\left[
\tau^K-\psi(\tau^K)-\log\tau
-\frac12\log(1-\tau^{-2K})
\right].
\]

| ID | Statement | Classification |
|---|---|---|
| A-001 | A genuine global arithmetic grade identity exists. | **PROVED** |
| A-002 | The identity proves grade language is connected to the complete zero sum. | **PROVED** |
| A-003 | The displayed arithmetic realization is bilateral in \(K\). | **FALSE / NOT ESTABLISHED** |
| A-004 | Existence of the identity alone forces one radial class. | **KNOWN INSUFFICIENT** |
| A-005 | Bounding the identity at RH scale gives a non-circular intermediate proof. | **CIRCULAR / RH-STRENGTH** |

---

# 10. Coordinate covariance versus coherence

| ID | Statement | Classification |
|---|---|---|
| G-001 | \(\mathcal Z_\tau(\tau^k s,k)=\zeta(s)\). | **PROVED** |
| G-002 | Whole-path agreement under this exact transform is RH evidence. | **FALSE** |
| G-003 | Coordinate covariance is a required implementation control. | **RESEARCH REQUIREMENT** |
| G-004 | A useful coherence law must contain information beyond G-001. | **RESEARCH REQUIREMENT** |
| G-005 | A visually identical coordinate copy is evidence of inter-zero rigidity. | **FALSE** |

---

# 11. Cross-height coherence

For verified simple zeros

\[
\rho_n=\frac12+i\gamma_n,
\]

define a baseline local scale

\[
\Delta_n
=
\frac{\tau}{\log(\gamma_n/\tau)}
\]

and normalized path

\[
P_n(u)
=
\frac{
\zeta(\frac12+i(\gamma_n+\Delta_nu))
}{
i\Delta_n\zeta'(\rho_n)
}.
\]

| ID | Statement | Classification |
|---|---|---|
| X-001 | \(P_n(0)=0\) and \(P_n'(0)=1\). | **PROVED for simple zeros** |
| X-002 | This removes selected zero location, local mean scale, first-order magnitude, and first-order orientation. | **PROVED** |
| X-003 | All \(P_n\) converge to one universal path. | **OPEN** |
| X-004 | Some simpler invariant of the \(P_n\) is height-independent. | **OPEN** |
| X-005 | Cross-height normalization is the definition of transcendental continuation. | **FALSE** |
| X-006 | Cross-height comparison is one instrument for discovering a zeta-specific coherence law. | **CURRENT RESEARCH ROLE** |

---

# 12. Compression and high-height work

| ID | Statement | Classification |
|---|---|---|
| H-001 | Any finite height can be compressed into an ordinary coordinate range by nonzero scale. | **PROVED** |
| H-002 | Origin compression also scales absolute radial displacement. | **PROVED** |
| H-003 | Normalized radial class remains unchanged under compression. | **PROVED** |
| H-004 | Compression alone forces RH. | **FALSE** |
| H-005 | Widely separated high-zero blocks are required to test a claimed height-independent coherence law. | **RESEARCH REQUIREMENT** |
| H-006 | Verifying more high zeros on the line is itself proof evidence. | **FALSE AS PROJECT INFERENCE** |

---

# 13. Synthetic perturbation

| ID | Statement | Classification |
|---|---|---|
| P-001 | Synthetic perturbation is a valid sensitivity diagnostic of a declared modified object. | **VALID METHODOLOGY** |
| P-002 | A synthetically moved-zero object is another Riemann zeta function. | **FALSE** |
| P-003 | Moving one synthetic zero changes the global function. | **PROVED** |
| P-004 | Moving one zero necessarily moves all other zeros. | **FALSE** |
| P-005 | Perturbation should be used to test a retained candidate invariant, not to manufacture proof evidence. | **RESEARCH REQUIREMENT** |
| P-006 | A symmetry-complete split defect is even and begins quadratically in \(\delta\). | **PROVED** |

---

# 14. Converter claims

| ID | Statement | Classification |
|---|---|---|
| CV-001 | The explicit formula requires the nontrivial zero contribution and the trivial-zero/archimedean remainder. | **PROVED / STANDARD** |
| CV-002 | The exact remainder can be written \(\sum_{m\ge1}E_1(2m\log x)\). | **PROVED** |
| CV-003 | Coupled transformation \(x\mapsto x^{1/A},\rho\mapsto A\rho\) preserves the single-zero Ei argument. | **PROVED** |
| CV-004 | Converter covariance under that coupled change is a nontrivial zeta automorphism. | **FALSE** |
| CV-005 | Symmetric converter split has generic quadratic small-\(\delta\) behavior. | **PROVED** |
| CV-006 | The observed ratio \(S(\delta)/S(\delta/2)\to4\) proves an exact universal hyperbolic law. | **FALSE** |

---

# 15. External falsification controls

These are conceptual boundary controls, not app features.

| ID | Mechanism | Classification | Control |
|---|---|---|---|
| F-001 | Central reflection/functional-equation symmetry alone forces criticality. | **KNOWN INSUFFICIENT** | Davenport–Heilbronn-type controls. |
| F-002 | Positive generalized prime-power towers alone force criticality. | **KNOWN INSUFFICIENT** | Beurling generalized systems. |
| F-003 | Additive lattice/theta self-duality alone forces criticality. | **KNOWN INSUFFICIENT** | Epstein-zeta controls. |
| F-004 | Because additive-only and multiplicative-only mechanisms separately fail, their conjunction also fails. | **FALSE INFERENCE** | Separate witnesses do not close the intersection. |
| F-005 | Generic central FE + generic Euler product narrowly characterizes ordinary zeta. | **KNOWN TOO COARSE** | Broader \(L\)-function classes exist. |

---

# 16. Tau-specificity

| ID | Statement | Classification |
|---|---|---|
| T-001 | Tau is the canonical project grade generator. | **DESIGN DEFINITION** |
| T-002 | The modulus identity \(b^{K\delta}\) can be formed for any base \(b>1\). | **PROVED** |
| T-003 | Therefore every tau-based observation is automatically arbitrary. | **FALSE INFERENCE** |
| T-004 | Any claim of genuinely tau-specific proof leverage must identify an exact place where \(\tau=2\pi\) matters beyond generic scaling. | **RESEARCH REQUIREMENT** |
| T-005 | Generic-base controls are required for theorem-facing tau claims. | **RESEARCH REQUIREMENT** |

---

# 17. Current research stop condition

The next work should not broaden into additional RH machinery until the following question is tested:

\[
\boxed{
\text{Do the exact parallel grade constraints of transcendental continuation}
\text{ reveal a nontrivial zeta-specific coherence law that forbids}
\text{ simultaneous occupancy of multiple radial leaves?}
}
\]

If no such law survives the declared controls, the current proof programme should be revised or killed.

If a simple law survives, broad computation should stop until that law is algebraically derived or falsified.

---

# 18. Explicit formula discrimination framework

| ID | Statement | Classification | Reason |
|---|---|---|---|
| EF-001 | \(\operatorname{EF}[h; \mathcal D, \mathcal A]\) is the Riemann–Weil explicit formula residual with Weil normalization. | **DESIGN DEFINITION** | Project authoritative explicit formula definition. |
| EF-002 | The true zeta divisor satisfies \(\operatorname{EF}[h; \mathcal D_\zeta, \mathcal A_\zeta] = 0\) for admissible test functions. | **PROVED / STANDARD** | Classical Riemann–Weil explicit formula theorem. |
| EF-003 | Grade-\(K\) test function \(h_{K,j}(t) = H_j(a_K t)\) has Fourier transform \(\widehat h_{K,j}(x) = a_K^{-1} \widehat H_j(a_K^{-1} x)\). | **PROVED** | Change of variables in Fourier integral. |
| EF-004 | Prime frequencies in grade \(K\) scale as \(a_K^{-1} \log n = \tau^{-K} \log n\). | **PROVED** | Follows from EF-003. |
| EF-005 | \(\mathcal C_{K,j}[H] \equiv \mathcal C_0[H(a_K \cdot)]\). | **PROVED** | Direct coordinate pullback identity. |
| EF-006 | The grade-\(K\) constraint family is coordinate-redundant with the expanded \(K=0\) native basis \(\{ H_j(a_K \cdot) \}\). | **PROVED / REDUNDANT** | The span of grade-\(K\) constraints is identical to scaled native constraints (exact theoretical classification: `coordinate_redundant`; relative to an unexpanded finite basis: `finite_basis_enrichment_only`). |
| EF-007 | Isolated zero-divisor modifications produce non-zero finite divisor defects \(\Delta \mathcal C_{K,j} = \langle\Delta\mathcal D, h_{K,j}\rangle\) while holding \(\mathcal A_\zeta\) fixed. | **PROVED** | Exact algebraic cancellation of unchanged arithmetic, pole, and gamma terms. |
| EF-008 | Radial quartet substitution decomposes into height-merging baseline \(\Delta\mathcal C^{\mathrm{merge}}\) and pure radial defect \(\Delta\mathcal C^{\mathrm{radial}}(\delta)\), with \(\Delta\mathcal C^{\mathrm{radial}}(0)=0\). | **PROVED** | Exact algebraic decomposition of four-zero symmetric sum. |
| EF-009 | Defect exposure under fixed arithmetic data proves radial rigidity of actual zeta zeros. | **FALSE INFERENCE** | Modifying zero divisor with fixed \(\mathcal A\) is a local sensitivity diagnostic of a synthetic object; it does not model an alternative zeta function or prove global non-compensation. |
| EF-010 | Independent Fourier numerical quadrature in native variable \(u = a_K t\) over compact effective support achieves certified error bound \(\le 10^{-45}\) without frequency aliasing. | **PROVED / IMPLEMENTED** | Panel-subdivided tanh-sinh quadrature control verified across all 90 \((K, j, x)\) channels. |
| EF-011 | Prospective cross-grade joint arithmetic constraints without test function dilation are mathematically distinct from \(\mathcal C_{K,j}\) and categorized as open candidates. | **CLASSIFICATION RULE** | Prevents conflating coordinate dilation with non-trivial joint arithmetic restrictions. |

---

# 19. Second-order radial sensitivity and quadratic energy analysis

| ID | Statement | Classification | Reason |
|---|---|---|---|
| EF-012 | Radial projection \(\mathcal P_0(\rho) = 1/2 + i\gamma\) and radial defect divisor \(\Delta\mathcal D_{\mathrm{rad}} = \mathcal D - \mathcal P_0(\mathcal D)\). | **DESIGN DEFINITION** | Rigorous projection of zero divisor to critical line. |
| EF-013 | Pure radial defect Taylor expansion satisfies \(\Delta\mathcal C_h[\mathcal O(\rho)] = -2\delta^2 h''(\gamma) + \mathcal O(\delta^4) = -2 u h''(\gamma) + \mathcal O(u^2)\). | **PROVED** | Exact holomorphic Taylor expansion of even test function along imaginary displacement. |
| EF-014 | Multi-orbit response matrix \(K_{(K,j), n} = -2 a_K^2 H_j''(a_K \gamma_n)\) defines quadratic energy \(E(u) = u^T K^T K u\). | **PROVED** | Exact linear matrix response in orbit variables \(u_n = \delta_n^2\). |
| EF-015 | Orbit variables \(u_n = \delta_n^2 \ge 0\) are strictly non-negative for all real radial displacements \(\delta_n \in \mathbb R\). | **PROVED** | Fundamental algebraic property of squares in \(\mathbb R\). |
| EF-016 | Finite non-negative least squares (NNLS) compensation \(K_{-n} u_{-n} \approx K_n u_n\) with \(u \ge 0\) yields heterogeneous diagnostic results in the 30-channel basis over 100 zeros (compensation found in 8 cases for zeros 10 and 50 at the \(10^{-5}\) threshold; compensation not found at this threshold in 8 cases for zeros 1 and 100) due to finite basis nullity \(\approx 85\) and condition number \(\sim 10^{15}\). | **HETEROGENEOUS FINITE OBSERVATION** | Verified in `explicit-formula-radial-second-variation-001`. |
| EF-017 | Avoiding RH in the calculation of the Taylor response does not prove that inferring radial rigidity from the projected-divisor defect \(\Delta\mathcal D_{\mathrm{rad}}\) is non-circular or complete. | **METHODOLOGICAL STATUS** | Exact Taylor derivation is unconditioned, but downstream radial-rigidity deduction remains open. |
| EF-018 | The critical-line projection \(\mathcal P_0(\mathcal D_\zeta)\) has no independent arithmetic representation for direct 1-point linear explicit formula statistics; Cauchy-Riemann equations prove that \(\delta\)-independence of \(2\Re G(\delta+i\gamma)\) forces \(G\) to be constant, establishing the Projection Trap. | **SCOPED PROJECTION TRAP** | **CLOSED** for fixed linear combinations and locally uniform limits of direct one-point holomorphic Riemann–Weil statistics over an open displacement family; **OPEN** for nonlinear paired, determinantal, operator, or independently constructed comparison objects (OBL-EF-003 / OBL-RDQ-001). |

---

# 20. Radial-Defect Quotient, limiting invariant \(L_Q\), and relative Fredholm formulation

| ID | Statement | Classification | Reason |
|---|---|---|---|
| RDQ-001 | Baseline completed reference function \(\Xi^\flat(z) = \prod_{\gamma>0}(1 + z^2/\gamma^2)^{m_\gamma}\) matches \(\Xi(z)\) for all critical-line zeros (\(\delta=0\)), with \(m_\gamma = m_{0,\gamma} + 2\sum_j n_{j,\gamma}\). | **PROVED / EXACT** | Exact factorization cancellation for \(\delta=0\) pairs \(\pm i\gamma\) in paired Hadamard product. |
| RDQ-002 | Radial-Defect Quotient \(Q(z) = \frac{\Xi(z)}{\Xi(0)\Xi^\flat(z)}\) decomposes on off-line quartets into real-axis factor \(q_{\delta,\gamma}(x) = \frac{\gamma^4[(x^2+\gamma^2-\delta^2)^2+4\delta^2\gamma^2]}{(\gamma^2+\delta^2)^2(x^2+\gamma^2)^2}\). | **PROVED / EXACT** | Exact algebraic normalization of 4-zero product divided by baseline factor. |
| RDQ-003 | Real-axis factor satisfies \(0 < q_{\delta,\gamma}(x) \le 1\) for all \(x \in \mathbb R\), with exact factorization \(1 - q_{\delta,\gamma}(x) = \frac{\delta^2 x^2 [(\delta^2+2\gamma^2)x^2 + 2\gamma^2(\delta^2+3\gamma^2)]}{(\delta^2+\gamma^2)^2(x^2+\gamma^2)^2} \ge 0\). | **PROVED / EXACT** | Exact rational difference factorization; equality iff \(x=0\) (for \(\delta \ne 0\)) and \(q_{0,\gamma}(x) \equiv 1\). |
| RDQ-004 | Unique minimum in \(u = x^2\) at \(u_* = \delta^2 + 3\gamma^2\), corresponding to two real minimizers \(x = \pm\sqrt{\delta^2 + 3\gamma^2}\). | **PROVED / EXACT** | Exact derivative root analysis of rational function. |
| RDQ-005 | For \(r = \delta^2/\gamma^2\), the minimum value is \(q_{\min} = \frac{4}{(1+r)^2(4+r)}\). | **PROVED / EXACT** | Direct evaluation at \(x = \pm\sqrt{\delta^2+3\gamma^2}\). |
| RDQ-006 | Exact uniform estimate \(\sup_x \|\log q_{\delta,\gamma}(x)\| = 2\log(1+r) + \log(1+r/4) \le \frac{9}{4}r\) supplies domination for infinite product/limit interchange. | **PROVED / EXACT** | Exact calculus extremum of log-ratio and \(\sum n_j \delta_j^2/\gamma_j^2 < \infty\). |
| RDQ-007 | Limiting invariant \(L_Q = \lim_{x\to\infty} Q(x) = \prod_{j} (\frac{\gamma_j^2}{\gamma_j^2+\delta_j^2})^{2n_j}\) satisfies \(0 < L_Q \le 1\), with \(L_Q = 1 \iff \mathrm{RH}\). | **PROVED SPECTRAL EQUIVALENCE** | Asymptotic limit of uniform convergent product; exact spectral criterion. |
| RDQ-008 | For \(H(z) = \log z\), projection-subtracted quartet response is \(2\Re\log(\delta+i\gamma) - 2\Re\log(i\gamma) = \log(1+\delta^2/\gamma^2) = d(\delta,\gamma)\). | **PROVED / EXACT** | Exact complex logarithm real-part identity. |
| RDQ-009 | The defect \(-\log L_Q = 2\sum n_j d(\delta_j,\gamma_j)\) lies inside the projection-subtracted EF-013 construction; its bridge failure is due to test-class inadmissibility, the projected-divisor problem, and unproved finite compensation. | **METHODOLOGICAL STATUS** | Rigorous attribution of EF-013 structural content. |
| RDQ-010 | Positive diagonal spectral operator \(\mathcal R e_\lambda = \frac{\delta_\lambda^2}{\gamma_\lambda^2} e_\lambda\) on \(\ell^2(\Lambda^+)\) is trace-class with \(\operatorname{Tr}\mathcal R = \sum \frac{\delta^2}{\gamma^2} < \infty\). | **PROVED / EXACT** | Convergence follows from \(\sum \gamma^{-2} < \infty\) and \(|\delta| < 1/2\). |
| RDQ-011 | Relative Fredholm determinant satisfies \(\det_{\mathrm F}(I + \mathcal R) = L_Q^{-1}\) and \(-\log L_Q = \operatorname{Tr}\log(I+\mathcal R) = \log\det_{\mathrm F}(I+\mathcal R)\). | **PROVED / EXACT** | Classical spectral theory of positive trace-class operators. |
| RDQ-012 | Minimal scalar target \(\operatorname{Tr}\mathcal R = 0 \iff \mathcal R = 0 \iff \mathrm{RH}\) is logically equivalent to RH and structurally minimal. | **PROVED EQUIVALENCE** | Non-negativity of eigenvalues \(\delta^2/\gamma^2 \ge 0\). |
| RDQ-013 | Rational pairing kernel \(\kappa_1(z,w) = \frac{4zw}{(z+w)^2} - 1\) satisfies \(\kappa_1(\lambda, \lambda^\#) = \frac{\delta^2}{\gamma^2}\) for \(\lambda^\# = -\bar\lambda\). | **PROVED / EXACT** | Exact rational algebraic identity with \((z+z^\#)^2 = -4\gamma^2\) and \(zz^\# = -(\delta^2+\gamma^2)\). |
| RDQ-014 | Relative trace satisfies \(\operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \kappa_1(\lambda, \lambda^\#)\). | **PROVED / EXACT** | Substitution of RDQ-013 into trace definition. |
| RDQ-015 | Divisor-independent arithmetic evaluation of \(\operatorname{Tr}\mathcal R\) or \(D_\zeta(1)\) by isolating \((\lambda, \lambda^\#)\) without constructing the projected divisor is the live open theorem. | **OPEN / LIVE TARGET** | Central research goal (OBL-RDQ-001). |

---

# 21. Withdrawn claims register

| ID | Historical Claim | Former Status | Withdrawn Status | Reason for Withdrawal |
|---|---|---|---|---|
| WDR-001 | EF-013 failed because the explicit formula had the "wrong \(\gamma\)-curvature". | FORMER WORKING CONJECTURE | **WITHDRAWN (AUDITED)** | Audited exact identity shows \(H(z)=\log z\) projection-subtraction yields \(2\Re\log(\delta+i\gamma) - 2\Re\log(i\gamma) = \log(1+\delta^2/\gamma^2) = d(\delta,\gamma)\), which matches the exact \(L_Q\) curvature. The failure is due to test function inadmissibility, projected-divisor lack of arithmetic representation, and unproved finite compensation. |

---

# 22. Arithmetic Radial Bridge claims

| ID | Statement | Classification | Reason |
|---|---|---|---|
| ARB-001 | Determinant target \(D := -\log L_Q = \log\det_{\mathrm F}(I+\mathcal R) = \sum 2n_j \log(1+r_j)\). | **DESIGN DEFINITION / EXACT** | Fundamental Fredholm determinant defect invariant. |
| ARB-002 | Trace target \(T := \operatorname{Tr}\mathcal R = \sum_{\lambda\in\Lambda^+} \frac{\delta_\lambda^2}{\gamma_\lambda^2} = \sum 2n_j r_j\). | **DESIGN DEFINITION / EXACT** | Minimal scalar first-moment radial defect invariant. |
| ARB-003 | Regularized weighted target \(T_a = \sum_{\lambda\in\Lambda^+} w_a(\lambda) \kappa_1(\lambda, \lambda^\#) = \sum w_a(\lambda) \frac{\delta_\lambda^2}{\gamma_\lambda^2}\) with \(w_a(\lambda) > 0\). | **DESIGN DEFINITION / EXACT** | Analytically regularized positive radial defect detector. |
| ARB-004 | Spectral equivalences \(D = 0 \iff L_Q = 1 \iff \mathrm{RH}\) and \(T = 0 \iff \mathrm{RH}\). | **PROVED SPECTRAL EQUIVALENCE** | Non-negativity of radial defect terms \(r_j = \delta_j^2/\gamma_j^2 \ge 0\). |
| ARB-005 | Grade center \(c_K = \tau^K/2\), centered coordinate \(z_K = s_K - c_K = \tau^K z\), and centered completed function \(\Xi_K(\tau^K z) = \Xi_0(z)\). | **PROVED / EXACT** | Exact geometric alignment of critical line under origin dilation. |
| ARB-006 | Grade invariance of normalized radial ratio: \(\frac{(\tau^K\delta)^2}{(\tau^K\gamma)^2} = \frac{\delta^2}{\gamma^2} = r\). | **PROVED / EXACT** | Scale factor \(\tau^{2K}\) cancels identically between numerator and denominator. |
| ARB-007 | Covariance Countermodel: abstract off-line quartet \(\mathcal Q_{\delta,\gamma} = \{1/2 \pm \delta \pm i\gamma\}\) (\(\delta \ne 0\)) is closed under reflection, conjugation, and transport, proving covariance \(\ne\) rigidity. | **PROVED / COUNTERMODEL** | Formalized in Lean 4 (`covariance_countermodel_offline_compatible`). |
| ARB-008 | Finite-family weighted sum vanishing firewall: \(\sum w_i r_i = 0 \iff \forall i, r_i = 0\) for \(w_i > 0, r_i \ge 0\). | **PROVED / FORMALLY_PROVED** | Formalized in Lean 4 (`list_weighted_sum_nonneg_eq_zero_iff`). |
| ARB-009 | Candidate A (linear grade differences) collapses to native explicit formula \(\mathcal C_0[H \circ \tau^K] - \mathcal C_0[H]\) and produces only 1-point direct sums. | **PROVED / FALSIFIED** | Exact SymPy reduction and negative control verification. |
| ARB-010 | Candidate B (bilinear cross-grade \(D_K(s)\overline{D_L(s)}\)) produces an unrestricted double sum over all zero pairs \((\rho_1, \rho_2)\), failing pair isolation. | **PROVED / FALSIFIED** | Spectral expansion contains off-diagonal cross-terms that do not vanish on-line. |
| ARB-011 | Candidate C (tensor-square trace identity) fails pair isolation without zero-divisor projection. | **PROVED / FALSIFIED** | Doubled trace formula does not restrict to diagonal involution pair. |
| ARB-012 | Candidate D (log-derivative contour identity) fails pair isolation due to double residue cross-terms across the critical strip. | **PROVED / FALSIFIED** | Contour integration does not eliminate off-diagonal zero pairings. |
| ARB-013 | Candidate E (relative determinant from arithmetic space) lacks zero-independent construction. | **OPEN / UNPROVED** | No known arithmetic operator isospectral to \(\mathcal R\) without zero divisor. |
| ARB-014 | Candidate F (grade-indexed prime-power pairing) lacks closed-form pairing kernel. | **OPEN / UNPROVED** | Arithmetic kernel isolating \(\delta^2/\gamma^2\) unproved. |
| ARB-015 | Candidate G (weighted regularized bridge) spectral detector \(T_a > 0 \iff \delta \ne 0\) is proved, while arithmetic realization \(\mathfrak A_{K,a}^{\mathrm{arith}}\) is open. | **SPECTRAL_PROVED_ARITH_OPEN / LIVE** | Live candidate under regularized Mellin transform analysis. |
| ARB-016 | Strict Arithmetic Input Firewall enforces zero-independent arithmetic evaluators. | **METHODOLOGICAL STATUS** | Pure arithmetic data boundary enforced in `math_core.py`. |
| ARB-017 | Scoped One-Point No-Go Theorem is closed for linear 1-point statistics and open for nonlinear/paired forms. | **PROVED BOUNDARY** | Cauchy-Riemann analysis on \(2\Re G(\delta+i\gamma)\). |
| ARB-018 | Divisor-independent closure of \(\mathfrak A_{K,X}^{\mathrm{arith}} = X\) and \(\mathfrak A_{K,X}^{\mathrm{arith}} = 0\) remains the central open obligation (OBL-RDQ-001). | **OPEN / LIVE TARGET** | Central research obligation of the Riemann Scope program. |

---

# 23. Separated Signal Bridge and Algebraic Curvature Claims

| ID | Statement | Classification | Reason |
|---|---|---|---|
| SSB-001 | Arbitrary finite curvature identity \(\sum_{i,j=1}^N (d_i + d_j)^2 = 2N \sum_{i=1}^N d_i^2 + 2(\sum_{i=1}^N d_i)^2\). | **PROVED / FORMALLY_PROVED** | Proved in Lean 4 (`RiemannScope.list_pairs_sq_sum_eq`) for arbitrary real lists. |
| SSB-002 | Curvature non-negativity and zero-rigidity: \(\sum_{i,j=1}^N (d_i + d_j)^2 \ge 0\) with equality iff \(\forall i, d_i = 0\). | **PROVED / FORMALLY_PROVED** | Proved in Lean 4 (`RiemannScope.list_pairs_sq_sum_nonneg`, `list_pairs_sq_sum_eq_zero_iff`). |
| SSB-003 | Universal scale dilation cancellation \(s D_s(su) = f(u)\) for all \(s > 0\). | **PROVED / FORMALLY_PROVED** | Proved in Lean 4 (`RiemannScope.generic_scale_dilation_cancellation`). |
| SSB-004 | Candidate SS1 (Cauchy-Riemann Holomorphic Rigidity) fails Gate 1 & 4. | **PROVED / FALSIFIED** | Cauchy-Riemann rigidity forces $\partial_{\bar s} \mathcal S(s,s) = 0$. |
| SSB-005 | Candidate SS2 (Polarized Bilinear Cross-Difference) fails Gate 2 & 5. | **PROVED / FALSIFIED** | Unrestricted double-sum cross-terms without involution-pair isolation; limiting off-diagonal cancellation unproved. |
| SSB-006 | Candidate SS3 (Cramér Logarithmic Phase Variance) fails Gate 4 & 6. | **PROVED / FALSIFIED** | Divergent transform outside critical strip; firewall violation. |
| SSB-007 | Candidate SS4 (Transcendental Scale Non-Resonance) fails Gate 2 & 3. | **SCOPED STATUS** | Single grades coordinate-redundant (PROVED); bounded search (NUMERICAL EVIDENCE ONLY); exact non-resonance for $2\pi$ OPEN. |
| SSB-008 | Candidate SS5 (Direct Positive Quadratic Kernel) fails Gate 1 & 6. | **PROVED / FALSIFIED** | Direct 1-point holomorphic realization closed; nonlinear sesquilinear open. |

---

# 24. Complete Finite Spectral Expansion and CMSA Suite Claims

| ID | Statement | Classification | Reason |
|---|---|---|---|
| CMSA-001 | Completed logarithmic derivative identity $P(u) = A(u) - \Xi'/\Xi(u-1/2)$ for $\Re(u) > 1$. | **PROVED / EXACT** | Proved analytically from Hadamard product and completed xi definition. |
| CMSA-002 | Completed mean-square anchor $\mathcal A(\sigma) = \lim_{T\to\infty} \frac{1}{2T}\int_{-T}^T |A(\sigma+it) - \Xi'/\Xi(\sigma-1/2+it)|^2 dt - \sum \frac{\Lambda(n)^2}{n^{2\sigma}} = 0$. | **PROVED / EXACT** | Unconditional arithmetic anchor identity for $\sigma > 1$. |
| CMSA-003 | Exact translation kernel $J_T(p,q) = \frac{\log\frac{p+iT}{p-iT} + \log\frac{q+iT}{q-iT}}{2Ti(p+q)}$. | **PROVED / EXACT** | Exact elementary antiderivative integration. |
| CMSA-004 | Exact paired zero-zero kernel $K_T(\lambda, \mu; a) = m_\lambda m_\mu \sum_{\varepsilon, \eta \in \{\pm 1\}} J_T(a - \varepsilon\lambda, a - \eta\bar\mu)$. | **PROVED / EXACT** | Substitution into paired Hadamard resolvent product. |
| CMSA-005 | Complete finite spectral expansion $S_{N,T}(\sigma) = I_{AA} - I_{AZ} - I_{ZA} + I_{ZZ}$ is an exact algebraic decomposition verified numerically ($< 10^{-15}$). | **PROVED / VERIFIED** | Verified in arbitrary precision via `evaluate_complete_finite_spectral_expansion`. |
| CMSA-006 | Real-axis spectral defect formula $\Delta(\delta) = \frac{4z\delta^2(z^2 - 3\gamma^2 - \delta^2)}{(z^2+\gamma^2)[(z^2+\gamma^2-\delta^2)^2+4\delta^2\gamma^2]}$. | **PROVED / EXACT** | Exact rational difference algebra on real axis $z = \sigma - 1/2 > 0$. |
| CMSA-007 | Real-axis defect sign transition: $\Delta(\delta) < 0$ for $z^2 < 3\gamma^2 + \delta^2$, positive for $z^2 > 3\gamma^2 + \delta^2$. | **PROVED / EXACT** | Strict sign determined by quadratic factor $z^2 - 3\gamma^2 - \delta^2$. |
| CMSA-008 | Gate G4 (Infinite Spectral Interchange) is the exact earliest analytic barrier: individual zero resolvents integrate to zero under $1/2T$ scaling. | **IDENTIFIED OPEN OBSTRUCTION** | Proved from $L^2(\mathbb R)$ resolvent norm $\frac{\pi}{\sigma-\Re\rho}$. |
| CMSA-009 | Finite raw Fejér response and zero-independent additive scalar-subtraction class classified as `FAIL_RADIAL_POSITIVITY`; full infinite CMSA-1 and CMSA-2 functionals classified as `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`; finite algebraic identity classified as `FINITE_IDENTITY_PROVED_G4_OPEN`. | **STANDARDIZED CLASSIFICATION** | Closed finite expansion, negative finite Fejér response, open infinite limit interchange. |
| CMSA-010 | Candidate CMSA-3 classified as `GRADE_COORDINATE_REDUNDANT`. | **PROVED REDUNDANCY** | Formalized in Lean 4 (`generic_scale_dilation_cancellation`). |

---

# 25. Gate G4 Infinite Regularization and Window Suite Claims

| ID | Statement | Classification | Reason |
|---|---|---|---|
| G4-001 | Fejér windowed zero kernel has exact elementary closed form: $J_T^{\text{Fejér}}(p,q) = \frac{I_T(p)+I_T(q)}{T(p+q)}$. | **PROVED / EXACT** | Proved analytically and verified numerically ($< 10^{-40}$) via `exact_fejer_zero_kernel_J_T`. |
| G4-002 | Asymptotic transition formula across regimes 1–4 matches $J_T$ to machine precision: $\frac{\arctan((T-\gamma)/a) + \arctan((T+\gamma)/a)}{2aT}$. | **PROVED / EXACT** | Proved by direct real-part integration on $[-T, T]$. |
| G4-003 | Cofinal boundary layer limit independence: fixed-truncation vanishing $\forall H, \lim_{n\to\infty} f(H,n) = 0$ does not imply cofinal vanishing $\lim_{n\to\infty} f(H(n),n) = 0$. | **PROVED / FORMALLY_PROVED** | Formalized in Lean 4 with Mathlib Filter.Tendsto (`tendsto_cofinal_fixed_zero`, `not_tendsto_cofinal_diagonal_zero`, `finite_sum_tendsto_interchange`). |
| G4-004 | Finite windowed quadratic expansion decomposes as $(A-Z)^2 = A^2 - 2AZ + Z^2 = AA - AZ - ZA + ZZ$. | **PROVED / FORMALLY_PROVED** | Formalized in Lean 4 (`RiemannScope.finite_quadratic_expansion_identity`, `finite_quadratic_four_term_decomposition`, `complex_quadratic_four_term_expansion`, `complex_finset_sum_mul_star`, `complex_finset_normSq_eq_double_sum_re`). |
| G4-005 | Four tested window families (Rectangular, Fejér, Abel-Poisson, Gaussian) all achieve exact finite expansion and remain open at Gate G4. | **CLASSIFIED / G4_OPEN** | Documented in `CMSA_GATE_G4.md`. |
| G4-006 | Raw finite Fejér response $\Delta S_W$ and additive reference class fail radial positivity (`FAIL_RADIAL_POSITIVITY`), with compact witness WIT-02 certified strictly negative in Arb (`CERTIFIED_NEGATIVE_ARB_BALL`). | **FAIL_RADIAL_POSITIVITY / CERTIFIED (WIT-02)** | Enclosed in outward-rounded Arb ball arithmetic for WIT-02; infinite CMSA-1/2 remain `INCONCLUSIVE_WITH_PRECISE_EARLIEST_OPEN_SUBGATE`. |
| G4-007 | Gate G4 Regularized Bridge Rigidity: any valid instance of `ConditionalG4RegularizedBridge` forces all represented zero defects to vanish ($d_j = 0$). | **PROVED / FORMALLY_PROVED** | Formalized in Lean 4 (`RiemannScope.ConditionalG4RegularizedBridge.all_defects_zero`). |
| G4-008 | Arithmetic independence firewall strictly prevents zero loading during arithmetic anchor evaluation. | **PROVED / ENFORCED** | Verified via mock testing in `test_cmsa_gate_g4.py`. |
| G4-009 | Second-order radial response coefficient $C_W(\sigma, \gamma, T) = -2\Re \int W_T(t) F_0(t) \overline{D_\gamma(z)} dt$ governs leading variation $\Delta S_W = \delta^2 C_W + O(\delta^4)$ conditionally under uniform domination hypotheses. | **PROVED / EXACT (CONDITIONAL)** | Proved analytically and verified numerically in `evaluate_g4_radial_response_coefficient`. |
| G4-010 | Negative radial sign witness suite: Fejér WIT-02 certified via Arb ball arithmetic; WIT 1, 3, 4 supported by high-precision numerical evidence. | **CERTIFIED_ARB / NUMERICAL_EVIDENCE** | Verified in `tests/test_cmsa_gate_g4.py` (`certify_g4_fejer_witness_arb`, `evaluate_g4_radial_sign_evidence`). |
| G4-011 | Proved absolutely convergent $\ell^1$ Dirichlet-series mean-square lemma for $\sum |a_n| < \infty$. | **PROVED / EXACT** | 4-step proof documented in `CMSA_GATE_G4.md` §4 replacing external Carlson dependency labels. |
| G4-012 | Additive-Reference Invariance No-Go Theorem: $(S_W(Z_\delta)-R) - (S_W(Z_0)-R) \equiv S_W(Z_\delta) - S_W(Z_0)$. | **PROVED / FORMALLY_PROVED** | Formalized in Lean 4 (`RiemannScope.additive_reference_subtraction_invariance`). |
| G4-013 | Mathlib `Filter.Tendsto` theorems for cofinal sequences and finite-sum limit interchange. | **PROVED / FORMALLY_PROVED** | Formalized in Lean 4 (`tendsto_cofinal_fixed_zero`, `not_tendsto_cofinal_diagonal_zero`, `finite_sum_tendsto_interchange`). |
| G4-014 | Conditional hypotheses for integrated pointwise delta expansions (window integrability, denominator separation, uniform domination, dominated convergence). | **PROVED / CONDITIONAL BOUNDARY** | Documented in `MATH_CONTRACT.md` §42.8 and `CMSA_GATE_G4.md` §6. |
| G4-015 | Abstract finite Dirichlet kernel decomposition under explicit kernel and linear pairing hypotheses. | **PROVED / FORMALLY_PROVED** | Formalized in Lean 4 (`abstract_finite_kernel_decomposition`, `linear_operator_finite_double_sum_interchange`, `abstract_windowed_kernel_expansion`). |
| G4-016 | Discrete grade-covariant schedule classification $H(\tau T) = \tau H(T)$ proves linear schedules $H_c(T) = cT$ are covariant, non-unique, and general periodic form $H(T) = T q(\log_\tau T)$; falsifies unique schedule determination by grade covariance alone. | **PROVED / FORMALLY_PROVED** | Formalized in Lean 4 (`linear_schedule_grade_covariant`, `grade_covariant_schedule_nonuniqueness`, `periodic_modulated_schedule_covariant`). |
| G4-017 | Certificate generation purity refactoring: pure dictionary return by default with optional `output_path`, preventing noncanonical test runs from mutating canonical on-disk certificate artifacts. | **PROVED / ENFORCED** | Verified via regression test `test_unit_tests_do_not_modify_tracked_canonical_certificates` in `tests/test_certification.py`. |

