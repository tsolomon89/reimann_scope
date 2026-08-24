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
| EF-018 | The critical-line projection \(\mathcal P_0(\mathcal D_\zeta)\) is not known to be the zero divisor of any zeta function and has no independent arithmetic representation; inferring \(\Delta\mathcal D_{\mathrm{rad}} = 0\) without assuming RH is the Projection Trap. | **OPEN OBLIGATION (PROJECTION TRAP)** | Open research obligation (OBL-EF-003) requiring an independent global constraint. |

