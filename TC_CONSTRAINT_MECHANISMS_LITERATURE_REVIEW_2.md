# TC constraint mechanisms: a theorem-level literature review

**Research date:** 3 October 2026.  
**Scope:** The TC formulation in the supplied brief, classical sources and selected recent primary literature. This is a literature and hypothesis audit, not a verification of the current repository.

**Conventions:** \(\tau=2\pi>1\); grades are bilateral integers unless a card explicitly enlarges the group; zeros are nontrivial zeta zeros counted with multiplicity. Positive-base powers use the real logarithm. Write \(\xi(s)=\tfrac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)\), the entire completed function. Fourier-frequency cards use \(z_\rho=-i(\rho-1/2)\); Part IV uses the equivalent Laplace variable \(w_\rho=\rho-1/2\).

## Part I — Executive conclusion

**Yes. The constraint mechanism TC seeks has established mathematical realizations. The closest is positive-definite harmonic analysis: Herglotz–Bochner, implemented through GNS and the spectral theorem.** A positive, translation-invariant correlation on a bilateral grade group admits a unitary representation. Applying that conclusion to every zeta zero also requires a faithful identification of those zeros with the resulting Hilbert-space spectrum.

The seven most relevant mechanisms are:

1. **Herglotz–Bochner/GNS:** positivity of all finite correlation matrices produces a positive spectral measure and unitary translation.
2. **Sz.-Nagy’s theorem:** uniformly bounded positive and negative powers of a bounded invertible Hilbert-space operator imply similarity to a unitary.
3. **Frame consistency and bilateral orbit frames:** redundant coefficients satisfy projection equations; a genuine bilateral operator-orbit frame forces unitary similarity, with a significant spectral-type restriction.
4. **Mellin–Plancherel:** normalized dilation explains the centering at \(1/2\), but does not identify zeros with the unitary spectrum.
5. **Weil positivity and de Branges:** positivity can force zero location; the full zeta-specific hypotheses are already RH-equivalent.
6. **Poisson duality, period lattices and Tate twists:** these supply structural uses of \(2\pi i\), including integer grading by period powers. A geometric bridge to TC remains unspecified.
7. **Dense-action and multi-scale rigidity:** genuine simultaneous invariances or independent functional equations can force constancy or rationality. Coordinate pullbacks alone are weaker.

Precise theorem statements and sources appear in Part III. The central synthesis is:

> **TC needs positivity, shift invariance and faithful zero-spectrum identification for the same object. Obtaining those properties separately does not establish their conjunction.**

| Construction | Positivity | Simultaneous-shift invariance | Zero information |
|---|---|---|---|
| Centered Weil pairing | Full assertion is RH-equivalent | Holds algebraically | Exact reflected pairing over all zeros |
| Ordinary Gram sum at actual zeros | Automatic | With complete visibility, critical-line support is required | Retains off-line displacement |
| Correlation using only real ordinates | Automatic | Automatic | Discards off-line displacement |
| Coordinate pullbacks of an analytic function | No Hilbert positivity supplied | Coordinate consistency holds | Permits off-line zeros |

This is a diagnosis of the supplied formulation, not a claim that a repository file has made an invalid substitution.

**Priority question 1 — arithmetic correlations:** Herglotz is the exact theorem for positive-definite sequences on \(\mathbb Z\); Bochner covers continuous positive-type functions on locally compact abelian groups; GNS constructs the Hilbert representation. “Arithmetic” is not itself a sufficient hypothesis. Boundedness of an arbitrary scalar correlation also does not imply positivity.

**Priority question 2 — redundancy:** frame theory rigorously realizes the statement that redundancy creates coefficient constraints. If \(C\) is a frame analysis operator and \(S=C^*C\), legitimate coefficients satisfy \(c=CS^{-1}C^*c\). This describes the image of the original object in coefficient space. Further assumptions are needed to restrict the object itself. A bilateral operator-orbit frame supplies such assumptions, but is too restrictive for a naive pure-point zero model.

**Priority question 3 — unitarity axis:** \(\Re s=1/2\) is the Mellin–Plancherel line for \(L^2(dx)\) in the usual convention, and a unitary axis for Eisenstein scattering. Neither alone proves RH. In modular scattering, a zeta zero enters at \(s=\rho/2\), as a resonance pole rather than automatically as a self-adjoint eigenvalue.

**Conclusion:** the abstract implication from suitable positivity or bilateral bounds to unitarity is available. The missing contribution must be an arithmetic proof that one faithful TC realization satisfies those hypotheses.

## Part II — Constraint mechanism taxonomy

Evidence labels apply to particular statements:

- **PROVED_STANDARD_THEOREM:** established under the stated hypotheses.
- **PROVED_SPECIAL_CASE:** proved in a narrower setting; recent preprint results are identified separately.
- **RH_EQUIVALENT:** the zeta-specific premise is known equivalent to RH.
- **CONJECTURAL:** an unproved assertion or bridge.
- **ANALOGY_ONLY:** structural resemblance without an applicable theorem.
- **NOT_APPLICABLE:** necessary hypotheses fail.

Relevance measures structural proximity, not the probability of proving RH. The table summarizes cards below; it does not independently assert their missing hypotheses.

| Mechanism | Established theorem | Constraint produced | Why \(2\pi\) matters | TC correspondence | Missing premise | Circularity risk | Relevance |
|---|---|---|---|---|---|---|---|
| Herglotz | Positive-definite sequences | Positive unit-circle measure | Angular units | Bilateral grade correlation | Toeplitz positivity and faithful identification | High for full Weil form | DIRECT |
| Bochner/GNS | Positive type and unitary realization | Unitary spectral representation | Fourier convention | Continuous/discrete grades | Positivity; continuity where needed | High if postulated | DIRECT |
| Pontryagin duality | LCA duality | Identifies unitary characters | Circle period | \(\widehat{\mathbb Z}=\mathbb T\) | Membership in unitary dual | Definitional if assumed | HIGH |
| Bilateral boundedness | Sz.-Nagy | Similarity to unitary | None specific | Grade-step operator | Common Hilbert norm and uniform bounds | Bounds may re-encode RH | DIRECT |
| Mellin–Plancherel | Plancherel under logarithmic coordinates | Unit imaginary exponent | Transform units | Centering at \(s-1/2\) | Actual zero-spectrum identification | High at identification step | HIGH |
| Affine/wavelet representation | Calderón reconstruction | Reproducing projection | Fourier convention | Translation and dilation | Admissibility and arithmetic intertwiner | Analogy without bridge | MEDIUM |
| Tight frames | Frame operator/Naimark | Coefficient range equations | None necessary | Redundant grade data | Frame bounds and Hilbert space | Positivity already in hypotheses | HIGH |
| Bilateral orbit frames | Operator-orbit classification | Unitary similarity; absolutely continuous type | Circle parameter | \(\{T^Kv\}\) | Complete frame; bounded invertible \(T\) | Atomic model is excluded | HIGH |
| Functional equation/intertwiners | Scattering adjoint/inverse relations | Unitarity on boundary axis | Completed zeta factors | Inverse versus conjugate | Zero/eigenvalue map | Unconditional unitarity is insufficient | HIGH |
| Poisson summation | Dual-lattice formula | Exact lattice compatibility | Reciprocal-lattice units | Grade lattices | A zero-sensitive arithmetic restriction | Identity alone gives no exclusion | HIGH |
| Weil criterion | Explicit-formula positivity | Critical-line support | Fourier/gamma factors | Arithmetic quadratic form | Full positivity proof | Known RH-equivalent | DIRECT |
| de Branges | Hermite–Biehler theory | Real zeros of associated functions | Not essential | Centered xi kernels | Required HB inequality | Precise zeta versions RH-equivalent | HIGH |
| Self-adjoint spectral theory | Spectral theorem/Stone | Real generator spectrum | Evolution units | \(e^{-iK\log\tau H}\) | Self-adjoint domain and full zero match | Identification may contain RH | HIGH |
| Selberg trace formula | Laplacian/zero correspondence | Line or exceptional real interval | Geometry | Arithmetic/spectral duality | Riemann-zeta counterpart | Analogy only | MEDIUM |
| Lindemann–Weierstrass | Algebraic-exponent rigidity | Forbidden exact coincidences | Period transcendence | Rational-grade separation | Algebraic data at the required point | No zero exclusion alone | MEDIUM |
| Gelfond–Schneider | Algebraic base/irrational algebraic exponent | Transcendence | Base \(2\pi\) fails hypothesis | Algebraic-grade collisions | Algebraic-base comparison | Misapplication risk | LOW directly |
| Baker | Algebraic logarithms | Linear-form rigidity | \(2\pi i\), not \(\log(2\pi)\) | Logarithmic identities | Eligible logarithms | Missing hypothesis | LOW directly |
| Ax–Lindemann/Ax–Schanuel | Functional transcendence | Dimension bounds | Exponential uniformization | Families of exponentials | Nonconstant family and specialization control | Constants do not inherit it | LOW directly |
| Periods/Tate twists | Comparison structures | Weight/integral compatibility | Powers of \(2\pi i\) | Period grades | Geometric object and comparison maps | Analogy is not construction | HIGH conceptually |
| Gluing/descent | Sheaf gluing | Global object from compatible data | None necessary | Grade transitions | Nontrivial local admissibility | Current cocycle automatic | LOW as exclusion |
| Multi-period rigidity | Dense-subgroup invariance | Constancy | Incommensurability | Exact scale invariance | Actual invariant observable | Covariance is weaker | MEDIUM |
| Mahler consistency | Adamczewski–Bell | Rationality | None specific | Independent scale equations | Mahler equations over rational functions | Current definition lacks them | MEDIUM |
| Almost-periodic Dirichlet series | Bohr/translate rigidity | Restricted translate limits | Phase torus | Prime frequencies | Valid domain and exact hypotheses | Universality blocks naive extension | MEDIUM |

## Part III — Detailed theorem cards

### Herglotz representation

**Domain:** harmonic analysis on \(\mathbb Z\). **Classification:** `PROVED_STANDARD_THEOREM`. **Relevance:** `DIRECT`.

**Theorem.** A sequence \(a:\mathbb Z\to\mathbb C\) satisfies
\[
\sum_{j,k}c_j\overline{c_k}a(j-k)\ge0
\]
for every finitely supported \(c\) exactly when \(a(n)=\int_{\mathbb T}z^n\,d\mu(z)\) for a unique finite positive measure \(\mu\). Its mass is \(a(0)\); no continuity assumption is necessary. The normalized existence statement appears in [H1, Theorem 1].

**Constraint:** positive Toeplitz correlations have positive spectral measures supported on unitary characters.

**TC correspondence and missing premise.** Grade \(K\) becomes the group index; \(\eta_\rho(K)=q_\rho^K\) is a candidate spectral mode. TC needs an arithmetic correlation satisfying every finite positivity inequality, followed by a faithful theorem identifying its spectral components with the zeros. A formal exponential expansion is insufficient. A positive Gram kernel need not be Toeplitz: \(q^j\overline{q^k}\) is positive for every \(q\ne0\), including nonunitary \(q\).

**Circularity:** if the required positivity is precisely the full Weil quadratic-form positivity, it is RH-equivalent. A weaker correlation might simply fail to detect some zeros.

### Bochner and GNS

**Domain:** harmonic analysis and unitary representations. **Classification:** `PROVED_STANDARD_THEOREM`. **Relevance:** `DIRECT`.

**Theorems.** For a locally compact abelian group \(G\), a continuous positive-definite function is the Fourier transform of a unique finite positive measure on its unitary dual [H2, §36A]. GNS realizes a continuous positive-type function on a topological group as \(a(g)=\langle U(g)v,v\rangle\), with \(U\) strongly continuous and unitary and \(v\) cyclic. This realization is unique up to cyclic unitary equivalence [H3].

**TC correspondence.** Set \(\langle e_J,e_K\rangle=a(J-K)\), quotient the nullspace, and complete. Grade shifts then act unitarily. For real grades, Bochner gives ordinary Fourier frequencies; continuity becomes essential.

**Missing premise and circularity.** The positive form must be proved before GNS is invoked. Every zero mode must survive the nullspace quotient and belong to the resulting spectral representation. Constructing an unrelated positive Hilbert space establishes neither property. These requirements can encode the same missing positivity as Weil’s criterion.

### Pontryagin duality and bounded characters

**Domain:** locally compact abelian groups. **Classification:** `PROVED_STANDARD_THEOREM`. **Relevance:** `HIGH`.

**Theorem.** The Pontryagin dual of \(\mathbb Z\) is \(\mathbb T\): its unitary characters are \(K\mapsto e^{iK\theta}\) [H4, §2]. Unitarity is part of this dual’s definition. General homomorphisms \(\mathbb Z\to\mathbb C^\times\) also include \(K\mapsto q^K\) with \( |q|\ne1\).

**TC deduction.** A globally bounded multiplicative character of any group is unitary: applying boundedness to every positive and negative power of an element proves its modulus is one. Thus bilateral boundedness of \(\eta_\rho\) is exactly \(\delta=0\). Integer grades identify ordinates modulo \(2\pi/\log\tau\), so faithful spectral identification must address aliasing.

**Missing premise and circularity.** TC must prove boundedness or positive type, rather than select the unitary dual by definition. For rational or real-algebraic grades given the discrete topology, the dual is larger than the real-frequency exponential family. Additional continuity is needed to recover that family. These conclusions require no transcendence of the scaling base.

### Sz.-Nagy’s unitarization theorem

**Domain:** Hilbert-space operator theory. **Classification:** `PROVED_STANDARD_THEOREM`. **Relevance:** `DIRECT`.

**Theorem.** A bounded invertible operator \(T\) is similar to a unitary operator exactly when \(\sup_{K\in\mathbb Z}\|T^K\|<\infty\). With common bound \(M\), a positive invertible \(Q\) can be chosen with \(M^{-1}I\le Q\le MI\) and \(QTQ^{-1}\) unitary [H5, Theorem I, p.152].

**TC correspondence.** Let \(T\) implement grade increment. If every \(q_\rho=\tau^{-(\rho-1/2)}\) belongs to its genuine spectrum, this theorem forces \( |q_\rho|=1\), hence \(\delta=0\).

**Missing premise and circularity.** TC needs a positive arithmetic Hilbert norm, bounded invertible grade action, a bound uniform over both signs of grade, and zero-to-spectrum inclusion. Individual boundedness of each power is insufficient. Unlike an orbit-frame requirement, this theorem permits pure-point spectrum. Whether its arithmetic hypotheses admit a proof independent of RH is unknown; asserting boundedness in a diagonal zero model merely restates RH.

### Mellin–Plancherel and the half-density

**Domain:** multiplicative harmonic analysis. **Classification:** `PROVED_STANDARD_THEOREM`. **Relevance:** `HIGH`.

**Theorem.** Logarithmic coordinates identify \(L^2(\mathbb R_+,dx/x)\) with \(L^2(\mathbb R,dy)\); multiplicative unitary characters are \(x^{it}\). On \(L^2(\mathbb R_+,dx)\), normalized dilations \(D_af(x)=a^{-1/2}f(x/a)\) are unitary. The Mellin transform \(Mf(s)=\int_0^\infty f(x)x^{s-1}dx\) satisfies
\[
\|f\|_2^2=\frac1{2\pi}\int_\mathbb R|Mf(1/2+it)|^2dt.
\]
See [H6, Eq.1.14.38] and [H7, Theorem 11.3.1.1].

**TC correspondence.** The half-density naturally explains centering by \(1/2\); restricting dilation to \(a=\tau^K\) gives the grade subgroup.

**Missing premise and circularity.** Mellin unitarity is independent of RH. TC must identify zeta zeros with actual spectral parameters of an arithmetic unitary representation. Formal powers with complex exponents exist without belonging to that spectrum. The choice of measure determines the unitarity axis; weighted measures can produce other vertical lines.

### Frame consistency and bilateral orbit rigidity

**Domain:** Hilbert frames and dynamical sampling. **Classification:** `PROVED_STANDARD_THEOREM`. **Relevance:** `HIGH`.

**Theorems.** Suppose \(A\|x\|^2\le\sum_k|\langle x,f_k\rangle|^2\le B\|x\|^2\), with \(0<A\le B<\infty\). Let \(C\) be analysis and \(S=C^*C\). Valid analysis coefficients satisfy \(Pc=c\), where \(P=CS^{-1}C^*\) is the orthogonal projection onto \(\operatorname{ran}C\). All synthesis coefficients for \(x\) are \(CS^{-1}x+\ker C^*\) [H8]. This is an exact realization of redundancy imposing coefficient equations.

For bounded invertible \(T\), a bilateral frame \(\{T^Kv\}_{K\in\mathbb Z}\) is similar to \(\{z^K\}_{K\in\mathbb Z}\) on \(L^2(E,m)\), with \(E\subset\mathbb T\) of positive arc measure [H9, Theorem 4.8]. Hence \(T\) is similar to unitary.

**TC deduction and limitation.** Bilateral reindexing gives \(TST^*=S\); thus \(S^{-1/2}TS^{1/2}\) is unitary. Redundancy itself is not decisive: the conclusion also holds for a basis orbit. More seriously, the theorem requires absolutely continuous spectral type. An unweighted complete bilateral orbit cannot be a frame in a pure-point unitary zero model: its coefficients against an eigenvector have constant modulus, contradicting either the upper bound or completeness.

**Missing premise/circularity.** TC needs actual frame bounds, orbit structure, and faithful spectral inclusion. A naive pure-point orbit target is too strong even assuming RH; ordinary coefficient consistency alone imposes no critical-line restriction.

### Affine representations and wavelets

**Domain:** wavelet analysis. **Classification:** `PROVED_STANDARD_THEOREM`; TC applicability `ANALOGY_ONLY`. **Relevance:** `MEDIUM`.

**Theorem.** The full affine group acts unitarily through \(\pi(b,a)f(x)=|a|^{-1/2}f((x-b)/a)\). For \(0<C_\psi=\int|\widehat\psi(\xi)|^2d\xi/|\xi|<\infty\), its wavelet transform satisfies \(W_\psi^*W_\psi=C_\psi I\) using Haar measure \(db\,da/a^2\). Its range has an explicit reproducing projection [H10, §1 and §3.1]. Restricting to positive scales requires separate frequency-half-space normalization.

**TC correspondence.** Translation and dilation supply a group action; reconstruction gives exact compatibility equations among redundant coefficients.

**Missing premise/circularity.** TC must establish an arithmetic Hilbert representation, admissibility, and faithful zero correspondence. Group noncommutation alone supplies no positivity: twisting by \(\pi_c(b,a)=|a|^c\pi(b,a)\) preserves the group relations but produces nonunitary growth for real \(c\ne0\). Wavelet reconstruction itself is independent of RH.

### Reproducing-kernel Hilbert spaces

**Domain:** positive kernels. **Classification:** `PROVED_STANDARD_THEOREM`. **Relevance:** `HIGH`.

**Theorem.** Every positive semidefinite kernel determines a unique reproducing-kernel Hilbert space, and every RKHS kernel is positive semidefinite [H11]. If a group preserves the kernel, its action on kernel sections extends to a unitary representation.

**TC correspondence.** Grades can label kernel sections. Positivity plus simultaneous grade invariance would construct the required unitary action.

**Missing premise/circularity.** Both properties must follow from arithmetic, with all zero modes surviving completion and quotient. Kernel existence alone does not constrain zeros: \(f(z)\overline{f(w)}\) is positive for any analytic \(f\), regardless of zero location. A stronger zero-detection theorem remains necessary and may reintroduce RH-equivalent positivity.

### Weil positivity and its distributional representation

**Domain:** explicit formulas and harmonic analysis. **Classification:** `RH_EQUIVALENT`; the equivalence is an established theorem. **Relevance:** `DIRECT`.

Put \(z_\rho=-i(\rho-\tfrac12)\), use \(\widehat f(z)=\int_{\mathbb R}f(x)e^{-izx}\,dx\), and set \(\widetilde f(x)=\overline{f(-x)}\). The centered Weil distribution is

\[
W(f)=\sum_\rho\widehat f(z_\rho),\qquad f\in C_c^\infty(\mathbb R),
\]

with zero multiplicities. Weil's criterion states

\[
\mathrm{RH}\iff Q_W(h):=W(h*\widetilde h)\ge0
\quad\text{for every }h\in C_c^\infty(\mathbb R).
\]

The explicit formula expresses the same distribution through primes, poles, and the archimedean term. Positivity must hold for arbitrary support, equivalently on every finite window. Bombieri–Lagarias give the multiplicative formulation; Suzuki records the precise centered compact-test formulation and its attribution to Yoshida. [W1, W2]

**Constraint mechanism:** positivity of an arithmetic quadratic form excludes off-line zeros. **TC correspondence:** the centered zero frequency generates \(\eta_\rho(K)=e^{-iK\log(2\pi)z_\rho}\). **Missing premise:** independently prove arithmetic positivity on the full test space, or on a family dense in the appropriate test/form topology. **Circularity risk:** this missing positivity is known equivalent to RH. Positivity on one bounded window or finite-dimensional subspace does not supply the quantified statement. The implication does not depend on the transcendence of \(2\pi\).

### Bochner–Schwartz

**Domain:** distributional harmonic analysis. **Classification:** `PROVED_STANDARD_THEOREM`. **Relevance:** `DIRECT`.

A distribution \(T\) on \(\mathbb R\) is of positive type when \(T(h*\widetilde h)\ge0\) for every compact smooth \(h\). Bochner–Schwartz says precisely that such distributions are Fourier transforms of positive measures of at most polynomial growth. They are automatically tempered; finite total mass is unnecessary. Conversely, Fourier transforms of these measures are positive type. The standard reference is Reed–Simon, Theorem IX.10; a modern published statement appears in Spindeler–Strungaru. [W5]

**Constraint mechanism:** distributional positivity gives a positive spectral measure on real frequencies, hence unitary real-group characters. **TC correspondence:** this applies before restricting log-translations to integer grades. **Missing premise:** prove that the actual arithmetic distribution is positive type. **Circularity risk:** applying it to \(W\) requires Weil positivity. Constructing a different positive distribution would also require proving its exact equality with \(W\). A formal raw zero sum is not a finite correlation to which ordinary Herglotz can immediately be applied.

### The exact passage to bilateral grades

The following is a direct calculation, making the proposed TC correspondence explicit. Let \(a=\log(2\pi)\), \(T_t h(x)=h(x-t)\), and fix \(h\in C_c^\infty(\mathbb R)\). Define

\[
C_h(K)=W\bigl(T_{aK}(h*\widetilde h)\bigr),\qquad K\in\mathbb Z.
\]

This smearing is well-defined. In the spectral expression, translating by \(aK\) multiplies each transformed zero contribution by \(\eta_\rho(K)\). For finitely supported coefficients \(c_j\) and grades \(K_j\), convolution gives

\[
\sum_{j,k}c_j\overline{c_k}C_h(K_j-K_k)
=Q_W\!\left(\sum_jc_jT_{aK_j}h\right).
\]

Consequently Weil positivity implies positive definiteness of every \(C_h\), and Herglotz supplies their positive circle measures. Conversely, positive definiteness for **every seed** \(h\) already gives \(Q_W(h)=C_h(0)\ge0\). Thus the all-seed grade criterion is exactly RH-equivalent; its converse uses only grade zero. A narrower seed family needs a separate density or spectral-detection theorem. Redundancy among grade translates does not prove the required arithmetic positivity.

### Li's criterion

**Domain:** analytic number theory and spectral-location inequalities. **Classification:** `RH_EQUIVALENT`. **Relevance:** `DIRECT`.

For \(n\ge1\), let

\[
\lambda_n=\sum_\rho^*\left[1-\left(1-\frac1\rho\right)^n\right],
\]

where the star means symmetric height summation and zeros retain multiplicity. Li proves \(\mathrm{RH}\iff\lambda_n\ge0\) for every positive integer \(n\). [W3] The Möbius transformation \(\rho\mapsto1-1/\rho\) maps the critical line to the unit circle. Bombieri–Lagarias establish a corresponding location theorem for suitable symmetric multisets, showing that this mechanism is more general than zeta. [W1]

**TC correspondence:** both formulations encode the critical line by unit modulus, using different transformations. **Missing premise:** positivity for every index, obtained independently from arithmetic. **Circularity risk:** known RH equivalence. This comparison prevents treating the unit-circle encoding itself as the missing new theorem. No transcendental scale is needed.

### Nyman–Beurling and Báez-Duarte

**Domain:** Hilbert-space approximation and arithmetic dilations. **Classification:** `RH_EQUIVALENT`. **Relevance:** `HIGH`.

In \(H=L^2((0,\infty),dx)\), put \(r_a(x)=\{1/(ax)\}\) and \(\chi=1_{(0,1]}\). The Nyman–Beurling criterion is

\[
\mathrm{RH}\iff\chi\in\overline{\operatorname{span}\{r_a:a\ge1\}}^{H}.
\]

Báez-Duarte's strengthening proves that the same equivalence holds with only positive integer \(a\). [W4]

**Constraint mechanism:** a specified target must belong to the closure of an arithmetic dilation family. **TC correspondence:** this is an established example where many scaled functions yield an exact completeness criterion. **Missing premise:** prove the approximation distance tends to zero. **Circularity risk:** known RH equivalence. The existence of the dilation family does not establish completeness; nor can integer dilations be replaced without proof by powers of \(2\pi\). Here the decisive structure is arithmetic approximation in a specified Hilbert norm, not transcendence of the dilation parameter.

### Current literature: constructions and unresolved identifications

The following primary papers distinguish legitimate positive models from the unproved identification needed for RH. Publication status is stated separately from mathematical classification.

| Paper | Verified result and hypothesis | Classification and TC consequence |
|---|---|---|
| Suzuki, screw function, 2023 [W2] | Theorem 1.2: the regularized continuous zero function \(g\) has positive kernel \(g(t-u)-g(t)-g(-u)+g(0)\) on all real arguments iff RH. | Published; `RH_EQUIVALENT`. Removes the divergent raw-trace problem; positivity remains to be proved. |
| Suzuki, Li norms, 2023 [W6] | Theorem 1.1: explicit, unconditionally \(L^2\) functions \(G_n\) satisfy \(\lambda_n=(2\pi)^{-1}\|G_n\|_2^2\) for every \(n\ge1\) iff RH. | Published; `RH_EQUIVALENT`. Equality with a positive norm is the missing assertion. |
| Nakamura–Suzuki, infinite divisibility, 2023 [W7] | Theorem 1.1: the specified arithmetic function \(e^{g_\zeta(t)}\) is an infinitely divisible characteristic function iff RH. Theorem 1.2 identifies its Lévy measure under RH. | Published; `RH_EQUIVALENT`. A precise positive-measure formulation, rather than automatic positivity. |
| Suzuki, Weil Hilbert space, 2025 [W8] | Theorem 1.1 assumes RH and identifies the completed Weil-form space with model/de Branges spaces. Section 6 supplies the associated spectral realization. | Published; `PROVED_SPECIAL_CASE`, conditional on RH. The Hilbert metric's positivity is not independently established. |
| Connes–Consani–Moscovici, spectral triples, 2025 [W9] | Theorem 1.1 constructs self-adjoint operators and real-rooted determinant functions assuming a simple lowest truncated Weil eigenvalue with even eigenvector. Section 8 lists missing global hypotheses and convergence. | Preprint; proved-in-paper `PROVED_SPECIAL_CASE`; zeta identification `CONJECTURAL`. Finite constructions do not identify the complete spectrum. |
| Suzuki, Weil form via screw function, September 2026 [W10] | Theorems 1.1/1.3 describe localized operators and continuous lowest eigenvalues. Theorem 1.5 gives unconditional self-adjoint extensions with real-rooted characteristic functions. Corollary 1.6 requires a specified compact-uniform limit to imply RH. | Preprint; proved-in-paper `PROVED_SPECIAL_CASE`; limit `CONJECTURAL`. Shifting a localized form below its spectral lower bound yields a Hilbert metric without proving the original form positive. |

### S1. Hermite–Biehler positivity and de Branges spaces

**Domain:** entire functions and positive kernels. **Status:** `PROVED_STANDARD_THEOREM`; zeta specialization `RH_EQUIVALENT`. **Relevance:** `HIGH`.

Put \(E^{\#}(z)=\overline{E(\bar z)}\). If an entire function satisfies

\[
|E^{\#}(z)|<|E(z)|\qquad(\Im z>0),
\]

then \(A=(E+E^{\#})/2\) and \(B=(E^{\#}-E)/(2i)\) have only real zeros. If E has no real zeros, those zeros are simple. The associated de Branges kernel is positive definite:

\[
K_E(w,z)=
\frac{E(z)\overline{E(w)}-E^{\#}(z)\overline{E^{\#}(w)}}
{2\pi i(\bar w-z)}.
\]

This is a genuine positivity-to-location theorem. It localizes zeros of A and B, not zeros of E itself. [S1]

**TC correspondence:** seek an arithmetic positive kernel with centered ξ as its associated real entire function. A nonreal zero would force \(E^{\#}=\pm E\), contradicting the strict modulus inequality.

**Missing premise and circularity:** Suzuki proves

\[
\mathrm{RH}\iff
E_\omega(z)=\xi(\tfrac12+\omega-iz)
\text{ is Hermite–Biehler for every }\omega>0.
\]

Membership is unconditional for \(\omega>1/2\); reaching arbitrarily small positive shifts is the unresolved part. [S2, Propositions 2.1–2.2] TC must establish the kernel inequality independently and retain the full zero divisor. Requiring a strict realization without real zeros for \(A=\xi(1/2-iz)\) additionally imposes simplicity; the shifted family avoids that extra conjecture. [S2, introduction]

### S2. Functional equations as inverse/adjoint identities

**Domain:** automorphic spectral theory. **Status:** `PROVED_STANDARD_THEOREM`. **Relevance:** `HIGH`.

For a cofinite Fuchsian group with standard cusp normalizations, Eisenstein scattering satisfies

\[
E(z,s)=\Phi(s)E(z,1-s),\qquad
\Phi(s)\Phi(1-s)=I.
\]

The scattering matrix is unitary on \(\Re s=1/2\), interpreting removable singularities by continuation. These are meromorphic identities; poles away from that axis are allowed. [S3, §2.6; Iwaniec, Theorem 6.6]

Normalized SL₂(R) principal-series intertwiners give an explicit operator version:

\[
Q(w^{-1},\sigma,-z)Q(w,\sigma,z)=I,
\quad
Q(w,\sigma,z)^*=Q(w^{-1},\sigma,\bar z).
\]

Thus imaginary z gives a unitary Q. Here \(\sigma=\pm\) specifies parity and the Hilbert norm is the prescribed induced-representation norm. [S4, p. 246]

**TC correspondence:** centering changes reflection into negation. TC has \(\eta_{1-\rho}=\eta_\rho^{-1}\) and \(\eta_{\bar\rho}=\overline{\eta_\rho}\). Spectrum symmetry supplies these partners; it does not identify inverse and adjoint for each mode.

**Missing premise and circularity:** construct the representation and prove that every relevant arithmetic mode belongs to its unitary spectrum. Assuming a purely imaginary inducing parameter already assumes the required location. Complementary-series unitarity with another invariant norm cannot be silently substituted for this particular character condition.

### S3. Modular scattering: the parameter caveat

**Domain:** Eisenstein series. **Status:** `PROVED_SPECIAL_CASE`; direct inference to RH `NOT_APPLICABLE`. **Relevance:** `HIGH` as a diagnostic.

For the modular group, set \(\Lambda(s)=\pi^{-s/2}\Gamma(s/2)\zeta(s)\), without the polynomial factor used in ξ. The constant term is

\[
y^s+\varphi(s)y^{1-s},\qquad
\varphi(s)=\frac{\Lambda(2s-1)}{\Lambda(2s)}.
\]

Müller verifies this coefficient and constructs self-adjoint cut-off Laplacians whose eigenvalues describe zeros of the different combination \(a^s\Lambda(2s)+a^{1-s}\Lambda(2s-1)\). [S5, equations (0.2), (2.1), Theorems 0.1–0.2]

**TC check, derived from these formulas:** on \(s=1/2+it\), the functional equation makes φ the quotient of \(\overline{\Lambda(1+2it)}\) by \(\Lambda(1+2it)\), hence unimodular where defined. A zeta zero ρ instead produces a pole at \(s=\rho/2\). Under RH these poles lie on \(\Re s=1/4\), not the scattering unitary axis.

**Missing premise:** identify the Riemann divisor with genuine unitary spectral values, rather than meromorphic resonances. Physical scattering unitarity alone imposes no required resonance-line conclusion. Replacing ζ by a symmetric combination changes the zero-location problem.

### S4. Self-adjointness, Stone, and Hilbert–Pólya

**Domain:** Hilbert-space spectral theory. **Status:** theorem `PROVED_STANDARD_THEOREM`; arithmetic realization `CONJECTURAL`. **Relevance:** `DIRECT`.

A densely defined self-adjoint H has real spectrum; \(U(t)=e^{-itH}\) is a strongly continuous unitary group. Conversely, a weakly continuous one-parameter unitary group has a self-adjoint generator. [S6, Theorem 5.2] A formal differential expression or symmetric operator without a proved self-adjoint domain is insufficient.

**TC correspondence:** define

\[
h_\rho=-i(\rho-\tfrac12)=\gamma-i\delta,
\qquad
\eta_\rho(K)=e^{-iK(\log\tau)h_\rho}.
\]

If every \(h_\rho\) belongs to the spectrum of self-adjoint H, then every δ vanishes. Merely realizing the ordinates γ as eigenvalues proves nothing about δ: ordinates are real even for off-line zeros.

**Missing premise and circularity:** a positive Hilbert realization must preserve all zeros and multiplicities through an exact spectral, trace, or determinant identity. Defining the space from an assumed critical-line spectrum would be circular. The value τ only chooses a sampling interval here.

Berry–Keating's xp proposal relates counting asymptotics and dynamics; it does not supply the complete arithmetic spectral identification. [S7] Connes's absorption-spectrum construction distinguishes critical zeros from possible noncritical resonances and reduces RH to a remaining trace-formula condition. [S8] These examples locate the gap precisely: arithmetic spectral interpretation is weaker than positive self-adjoint realization of every centered zero.

### S5. Selberg's successful spectral model and its exceptions

**Domain:** hyperbolic spectral geometry. **Status:** `PROVED_SPECIAL_CASE`; transfer to ζ `ANALOGY_ONLY`. **Relevance:** `HIGH`.

For compact hyperbolic X without boundary, Selberg zeta zeros in the critical strip are either on \(\Re s=1/2\) or real. [S9, Theorem 1.2]

**Mechanism:** the spectral relation is \(\lambda_j=s_j(1-s_j)\). Self-adjointness makes λ real. Eigenvalues \(\lambda_j\ge1/4\) give \(s_j=1/2\pm i\sqrt{\lambda_j-1/4}\); smaller eigenvalues give real exceptions. Compactness makes the below-threshold spectrum finite. Self-adjointness alone does not prove the threshold bound.

**TC correspondence and missing premise:** an exact trace formula identifies the geometric spectral object before positivity constrains its zeros. TC needs that identification for Riemann arithmetic. The prime/geodesic analogy does not supply it, and a squared spectral parameter would require excluding small-eigenvalue exceptions separately.

### T1. Lindemann–Weierstrass and rational-grade separation

**Domain:** transcendental number theory. **Classification:** `PROVED_STANDARD_THEOREM`. **Relevance:** `HIGH` for arithmetic grids; `LOW` for spectral unitarity.

**Theorem.** If \(a_1,\ldots,a_r\) are distinct algebraic numbers, then \(e^{a_1},\ldots,e^{a_r}\) are linearly independent over \(\overline{\mathbb Q}\). Consequently \(e^a\) is transcendental for nonzero algebraic \(a\), and \(\pi\) is transcendental because \(e^{i\pi}=-1\). [T1]

**Constraint and TC correspondence.** An elementary consequence is
\[
m\tau^K=n\tau^J,
\quad m,n\in\overline{\mathbb Q}^{\times},\quad K,J\in\mathbb Q
\quad\Longrightarrow\quad K=J,\ m=n.
\]
Indeed, if \(K-J=a/b\ne0\), then \(\tau^a=(n/m)^b\) is algebraic, which would make \(\tau\) algebraic. Equivalently, distinct rational grades satisfy
\[
\tau^K\overline{\mathbb Q}\cap\tau^J\overline{\mathbb Q}=\{0\}.
\]
This argument covers positive and negative grades and works for every positive transcendental generator.

**Missing hypothesis.** TC must establish that the *same displacement or witness* belongs to both grids. Coordinate changes alone do not establish simultaneous membership. **Circularity risk:** none in the arithmetic theorem; the unproved membership bridge carries the substantive burden.

### T2. Gelfond–Schneider, Baker, and algebraic grades

**Domain:** numerical transcendence. **Classification:** `PROVED_STANDARD_THEOREM`; direct use with \(\tau\) as an algebraic base is `NOT_APPLICABLE`. **Relevance:** `MEDIUM`.

**Theorems.** Gelfond–Schneider says that algebraic \(a\ne0,1\) and algebraic irrational \(b\) make every value of \(a^b\) transcendental. Baker says that Q-linearly independent logarithms \(\lambda_j\) of algebraic numbers remain linearly independent over \(\overline{\mathbb Q}\); its stronger form includes \(1\). [T1, T2]

**TC barrier.** The base \(2\pi\) is transcendental. Its logarithm is not itself a logarithm of an algebraic number; the construction supplies no eligible logarithmic representation to which Baker’s theorem directly applies. The number \(2\pi i\), being a logarithm of \(1\), belongs to that space. These are different inputs. Neither theorem directly settles \(\tau^{\sqrt2}\); no unconditional resolution of that value was located in this review.

**An elementary useful consequence.** For real algebraic exponents, define
\[
S_\tau=\{a\in\overline{\mathbb Q}\cap\mathbb R:
\tau^a\in\overline{\mathbb Q}\}.
\]
Positive real powers make this a Q-vector space. The preceding argument gives \(S_\tau\cap\mathbb Q=\{0\}\). If nonzero \(a,b\in S_\tau\), set \(A=\tau^a\). Since \(A^{b/a}=\tau^b\) is algebraic, Gelfond–Schneider forces \(b/a\in\mathbb Q\). Therefore
\[
\dim_{\mathbb Q}S_\tau\le1.
\]
Any exceptional collision exponents lie on one rational line; proving that the line is absent remains additional work. Transcendence alone cannot guarantee absence: \(t=2^{\sqrt2}\) is transcendental but \(t^{\sqrt2}=4\). [T3]

**Missing hypothesis / circularity.** A suitable algebraic base or verified logarithmic relation is missing. Even complete uniqueness of algebraic grading would require a separate bridge to zeta-zero displacements before implying RH.

### T3. Six exponentials and the conjectural four-exponentials replacement

**Domain:** exponential algebra. **Classification:** six exponentials `PROVED_STANDARD_THEOREM`; four exponentials `CONJECTURAL`. **Relevance:** `LOW` without new arithmetic inputs.

**Theorem.** If \(x_1,x_2\) are Q-linearly independent and \(y_1,y_2,y_3\) are Q-linearly independent, at least one of the six values \(e^{x_i y_j}\) is transcendental. Replacing the triple by a Q-independent pair gives the four-exponentials conjecture. [T4]

**Constraint.** A complete rectangular array of algebraic exponential values is incompatible with these independent exponent directions.

**TC correspondence and missing hypothesis.** Integer multiples of a single grade provide one rational direction, regardless of how many identities are written down. TC would need the independent directions and algebraicity of *all six* cross-values. If one entry is already \(\tau\), its known transcendence satisfies the conclusion without constraining anything else. **Circularity risk:** none intrinsically; replacing the theorem by its conjectural four-value strengthening creates an additional unproved premise.

### T4. Schneider–Lang and Mahler specialization

**Domain:** arithmetic properties of analytic functions. **Classification:** `PROVED_STANDARD_THEOREM`; current direct application `NOT_APPLICABLE`. **Relevance:** `LOW`.

**Schneider–Lang theorem.** Let \(F\) be a number field and \(f_1,\ldots,f_N\) finite-order meromorphic functions. Suppose \(F[f_1,\ldots,f_N]\) is stable under differentiation and has transcendence degree at least two over \(F\). There are only finitely many common regular points where all values belong to the *same* field \(F\). [T5]

**Nishioka’s Mahler theorem.** Let integer \(q\ge2\), and let algebraic-coefficient power series satisfy \(f(z)=A(z)f(z^q)\), with \(A\in\mathrm{GL}_m(\overline{\mathbb Q}(z))\). At algebraic \(\alpha\), \(0<|\alpha|<1\), where every \(A(\alpha^{q^k})\) exists and is invertible, the transcendence degree of the values equals that of the functions. The associated lifting theorem lifts homogeneous algebraic relations among these values to functional relations. [T6]

**TC correspondence and missing hypotheses.** Schneider–Lang constrains repeated common arithmetic values through differential closure; Mahler theory constrains specializations through a specified functional equation. The identity defining a grade pullback supplies neither. In particular, \((\tau^z)'=(\log\tau)\tau^z\) does not provide a differential system over a number field, and \(s\mapsto s/\tau\) is not the Mahler substitution \(z\mapsto z^q\). **Circularity risk:** not intrinsically RH; the required arithmetic analytic systems remain unconstructed.

### T5. Ax–Schanuel: functional independence

**Domain:** functional transcendence. **Classification:** `PROVED_STANDARD_THEOREM`; numerical specialization to fixed TC constants `NOT_APPLICABLE`. **Relevance:** `MEDIUM` for a future functional formulation.

**Precise formulation.** If \(y_1,\ldots,y_n\in t\mathbb C[[t]]\) are Q-linearly independent, Ax’s theorem gives
\[
\operatorname{trdeg}_{\mathbb C(t)}
\mathbb C(t)(y_1,\ldots,y_n,e^{y_1},\ldots,e^{y_n})\ge n.
\]
This is a function-field theorem; numerical Schanuel remains a conjecture. [T2]

**Constraint and missing hypothesis.** The theorem controls functional algebraic relations after constants have been removed. Constants \(a\log\tau\) do not satisfy its nonconstant hypotheses. Replacing them by functions can establish functional independence, but evaluation at \(\log\tau\) requires a separate specialization theorem. TC needs an appropriate nonconstant locus and control of that particular evaluation. **Circularity risk:** functional independence is independent of RH; importing numerical Schanuel silently would introduce a different major conjecture.

### T6. Laurent’s theorem and unlikely intersections

**Domain:** Diophantine geometry of multiplicative tori. **Classification:** stated results `PROVED_STANDARD_THEOREM`; general Zilber–Pink extensions `CONJECTURAL`. **Relevance:** `MEDIUM` as a possible formulation, presently `ANALOGY_ONLY`.

**Theorems.** For a finite-Q-rank subgroup \(\Gamma\subset\mathbb G_m^n(\mathbb C)\), the Zariski closure of any subset of \(\Gamma\) is a finite union of algebraic-subgroup cosets. A related curve theorem says that an irreducible algebraic curve not contained in any translate of a proper algebraic subgroup meets the union of codimension-two subgroups finitely. [T7]

**Constraint.** Excessive intersections acquire algebraic subgroup structure; the conclusion is not universal disjointness.

**TC correspondence and missing hypotheses.** Fixed finitely many scales generate an eligible finite-rank group, even with transcendental generators. Allowing every integer multiplier introduces all primes and infinite rank; allowing every real algebraic exponent also gives infinite rank. TC must specify a fixed finite-rank subgroup, an algebraic variety, and the required nondegeneracy. A single exceptional point is not excluded. **Circularity risk:** none intrinsically; an analytic zeta locus cannot simply be declared an algebraic variety.

### T7. Fourier lattices, exponential periods, and Tate twists

**Domain:** harmonic analysis, complex geometry, period theory. **Classification:** lattice duality and exponential sequence `PROVED_STANDARD_THEOREM`; TC’s motivic identification `ANALOGY_ONLY`. **Relevance:** `HIGH` as structural language.

**Theorems and identities.** For a full lattice \(\Lambda\subset\mathbb R^d\), define \(\Lambda^*=\{\xi:\langle\lambda,\xi\rangle\in\mathbb Z\}\). With Fourier kernel \(e^{-2\pi i\langle x,\xi\rangle}\), Schwartz functions satisfy
\[
\sum_{\lambda\in\Lambda}f(\lambda)
=\operatorname{covol}(\Lambda)^{-1}
\sum_{\xi\in\Lambda^*}\widehat f(\xi).
\]
A character descends to the quotient precisely when it annihilates the lattice. [T8] On a complex manifold, the sheaf sequence
\[
0\longrightarrow2\pi i\mathbb Z\longrightarrow\mathcal O
\xrightarrow{\exp}\mathcal O^*\longrightarrow1
\]
is exact. Local logarithms differ by integral periods, with a cocycle obstruction to choosing a global logarithm. [T9]

**TC correspondence.** For \(\Lambda_K=\tau^K\mathbb Z\), normalized Fourier duality gives \(\Lambda_K^*=\tau^{-K}\mathbb Z\); angular-frequency units give \(\tau^{1-K}\mathbb Z\). The discrete pairing is structural; the placement of \(2\pi\) depends on units. These statements do not require its transcendence or force membership of one scalar in both lattices.

**Tate precedent.** Period theory explicitly extends its period ring to \(\mathcal P[1/(2\pi i)]\); integer powers of \(2\pi i\) correspond to Tate twists. Completeness of the standard integral rules for *all* period identities is the Kontsevich–Zagier conjecture. [T10] Thus bilateral integer period scaling has established language, but arbitrary algebraic grades do not automatically become Tate twists.

**Missing hypothesis / circularity.** TC needs an actual comparison or monodromy object linked to zeta zeros. Its scalar transition maps already satisfy their cocycle identically. The grade exponential uses \(\log\tau\), with imaginary period \(2\pi i/\log\tau\); identifying that with the exponential’s original period would skip the needed bridge. None of these standard identities independently forces the spectral defect to vanish.

### Descent and gluing: compatibility with no automatic spectral restriction

**Domain:** sheaves, bundles and descent. **Classification:** PROVED_STANDARD_THEOREM; TC exclusion application ANALOGY_ONLY. **Relevance:** LOW as an exclusion mechanism.

**Theorem.** Given sheaves \(\mathcal F_i\) on an open cover and overlap isomorphisms \(\phi_{ij}\) satisfying \(\phi_{jk}\phi_{ij}=\phi_{ik}\) on triple overlaps, a global sheaf with those identifications exists, uniquely up to the compatible isomorphism. Compatible local sections are the equalizer of the two restriction maps. [R1, Lemmas 6.33.2–6.33.4]

**Constraint:** arbitrary collections of local data must satisfy overlap equations.

**TC deduction.** The scalar transitions \(\phi_{KJ}(s)=\tau^{J-K}s\) satisfy the cocycle because \(\tau^{L-J}\tau^{J-K}=\tau^{L-K}\). This holds for every starting scalar and every positive base. It restricts arbitrary tuples of coordinates, but not the scalar that generates them.

**Missing premise/circularity:** genuinely independent local admissibility conditions, such as algebraic or integral structures, would be needed for an exclusion result. No additional zero constraint follows from this trivial cocycle. Gauge descriptions and redundant linear codes have the same distinction: image relations are real constraints on encodings, but do not necessarily remove any source objects.

### Dense invariance and two incommensurable scales

**Domain:** topological dynamics. **Classification:** PROVED_STANDARD_THEOREM; elementary proof below. **Relevance:** MEDIUM.

**Statement.** Let \(f:(0,\infty)\to\mathbb C\) be continuous. If \(f(ax)=f(x)=f(bx)\) for all \(x>0\), where \(a,b>1\) and \(\log a/\log b\notin\mathbb Q\), then \(f\) is constant.

**Proof.** Set \(g(u)=f(e^u)\). Its periods include the dense subgroup \(\mathbb Z\log a+\mathbb Z\log b\); continuity makes every real number a period. This argument is complete and does not require a transcendence theorem.

**TC correspondence.** Exact multi-scale invariance could produce rigidity. Powers of one base with integer grades are commensurate. Allowing rational grades makes the scale group dense, but only a genuinely invariant continuous observable is then forced constant. Two algebraic grades with irrational ratio also produce dense logarithmic translations.

**Missing premise/circularity:** \(\mathcal Z_\tau(\tau^Ks,K)=\zeta(s)\) compares different coordinate descriptions. It is not the assertion \(\zeta(\tau^Ks)=\zeta(s)\). The latter fails. A useful TC application must name another observable with independently proved invariance. Two real-incommensurable complex periods can instead generate a discrete lattice, allowing nonconstant meromorphic elliptic functions; the real dense-subgroup proof must not be applied to that setting.

### Independent Mahler equations and consistent systems

**Domain:** difference equations and arithmetic dynamics. **Classification:** PROVED_STANDARD_THEOREM; current TC application NOT_APPLICABLE. **Relevance:** MEDIUM.

**Theorem.** If integers \(p,q\ge2\) are multiplicatively independent and a formal Laurent series over \(\mathbb C\) satisfies nontrivial linear \(p\)- and \(q\)-Mahler equations with rational-function coefficients, it is rational. Adamczewski–Bell prove the power-series result; Schäfke–Singer give a direct Laurent-series formulation. [R2, R3, Theorem 1]

For a vector solution of \(y(x^p)=A(x)y(x)\), \(y(x^q)=B(x)y(x)\), the consistency condition is
\[
A(x^q)B(x)=B(x^p)A(x),
\qquad A,B\in{\rm GL}_n(\mathbb C(x)).
\]
The rational-coefficient and independence assumptions make this substantially stronger than formal group commutation.

**TC correspondence/missing premise:** this is a proved example where two exact representations force rigidity. TC has not supplied two such Mahler equations. Generic \(q\)-difference or renormalization language supplies no universal rigidity theorem without coefficient, domain and regularity assumptions. **Circularity:** none intrinsic; the necessary functional equations would be new input.

### Almost periodicity, prime phases and universality

**Domain:** Dirichlet series. **Classification:** PROVED_STANDARD_THEOREM; transfer to critical-line exclusion ANALOGY_ONLY. **Relevance:** MEDIUM.

**Theorems.** Dirichlet series are Bohr almost periodic on closed strips strictly inside their half-plane of uniform convergence. Perelli–Righetti, Theorem 1, characterizes simultaneous translate approximation for series with a common integral exponent basis and finite uniform-convergence abscissae: targets holomorphic near compact subsets with accumulation points are approximable exactly when they are vector-equivalent through one common Bohr phase twist. [R4]

For zeta, logarithms of primes form the integral basis. By contrast, Voronin universality says a nonvanishing function continuous on a disk \(|z|\le r<1/4\), holomorphic inside, is uniformly approximable by \(\zeta(3/4+z+it)\); the successful shifts have positive lower density. [R5]

**TC correspondence:** phase compatibility produces real restrictions in the convergence half-plane. It does not extend unchanged into the universality strip.

**Missing premise/circularity:** almost periods are approximate recurrences, not exact invariances. Universality demonstrates flexibility of analytic values and blocks a naive rigidity claim; it neither disproves RH nor decides the distribution of off-line zeros. A proposed TC relation must specify its domain and exact strength.

### An explicit Weyl-relation compatibility check

**Domain:** Fourier and Heisenberg representations. **Classification:** PROVED_STANDARD_THEOREM, with the relevant identity derived here. **Relevance:** MEDIUM.

On \(L^2(\mathbb R)\), let \(T_bf(x)=f(x-b)\) and \(M_\xi f(x)=e^{2\pi i\xi x}f(x)\). Substitution gives
\[
T_bM_\xi=e^{-2\pi ib\xi}M_\xi T_b.
\]
Thus these operators commute exactly when \(b\xi\in\mathbb Z\). This is a genuine discrete compatibility condition tied to the exponential period; angular-frequency units move the \(2\pi\) into the condition. It is the same annihilator pairing underlying lattice duality.

**TC correspondence/missing premise:** an arithmetic construction could require a specific translation and modulation to commute, thereby selecting lattice pairs. TC has not derived that requirement or connected the selected pairs to zero displacements. Both operators are already unitary by their definitions; the commutator does not prove unitarity of an independently given nonunitary grade action. The affine counterexample above shows why noncommutation alone is insufficient.

## Part IV — Direct TC correspondences and the exact gap

The calculations in this part are deductions made in this review, with their standard ingredients cited in Part III. The proved elementary lemmas and counterexamples in Parts IV–V are classified PROVED_SPECIAL_CASE; proposed arithmetic bridges remain CONJECTURAL. No novelty is claimed for these deductions.

### 1. Grades, characters and two different actions

Set \(a=\log\tau>0\), \(w_\rho=\rho-1/2=\delta+i\gamma\), and
\[
\lambda_\rho=e^{-aw_\rho},\qquad \eta_\rho(K)=\lambda_\rho^K.
\]
For \(K\in\mathbb Z\), this is a homomorphism into \(\mathbb C^\times\). Calling it a *unitary* character already requires \(|\lambda_\rho|=1\). Directly,
\[
\sup_{K\in\mathbb Z}|\eta_\rho(K)|<\infty
\iff |\lambda_\rho|=1
\iff\delta=0.
\]
Positive grades alone permit decaying off-line modes. Negative grades supply the other direction. No sign of \(s\) restricts \(K\).

For nonreal grades \(K\), the modulus instead depends on \(\Re(Kw_\rho)\); the real-grade criterion cannot be transferred unchanged. The real-algebraic-grade conclusions in the transcendence cards make no claim about all complex algebraic grades.

These identities hold for every real base \(b>1\). Their validity alone does not select \(2\pi\).

The pullback \(\mathcal Z_\tau(s,K)=\zeta(\tau^{-K}s)\) gives zero coordinates \(s_\rho(K)=\tau^K\rho\) and transitions \(s_J=\tau^{J-K}s_K\), but supplies no Hilbert norm.

A precise realization of the *character* uses a logarithmic test variable. For \(f\in C_c^\infty(\mathbb R)\), put
\[
F(w)=\int_{\mathbb R}f(u)e^{-wu}\,du,\qquad
(T_hf)(u)=f(u-h).
\]
Then
\[
\mathcal L(T_{Ka}f)(w_\rho)=\eta_\rho(K)F(w_\rho).
\]
Dilation of the original complex argument and translation of this test variable are distinct constructions until an intertwining identity connects them.

### 2. The two pairings that must not be exchanged

Let \(\widetilde g(u)=\overline{g(-u)}\). Define
\[
W(h)=\sum_\rho\mathcal Lh(w_\rho),\qquad
Q_W(f,g)=W(f*\widetilde g)
=\sum_\rho F(w_\rho)\overline{G(-\overline{w_\rho})}.
\]
Zeros are counted with multiplicity. Compact smooth support gives rapid transform decay uniformly in the fixed strip containing the \(w_\rho\), making these sums absolutely convergent. The explicit formula supplies the same \(W\) through prime powers, poles and the archimedean factor; all these terms must be retained.

Convolution gives, without RH,
\[
Q_W(T_hf,T_hg)=Q_W(f,g).
\]
The missing property is \(Q_W(f,f)\ge0\) on the full test space: precisely Weil positivity.

The ordinary Gram pairing
\[
Q_+(f,g)=\sum_\rho F(w_\rho)\overline{G(w_\rho)}
\]
is positive automatically, but translation multiplies each diagonal summand by \(e^{-2h\delta}\). Its invariance does not follow. On RH the two pairings coincide. Borrowing positivity from \(Q_+\) and invariance from \(Q_W\) without proving their identity assumes the missing bridge.

### 3. A direct support lemma for the positive defect

Let \(\nu\) be a finite positive measure on \(\mathbb C^\times\), with finite fourth absolute moment, and define genuine mixed moments
\[
G(k,l)=\int\lambda^k\overline\lambda^{\,l}\,d\nu,\qquad k,l\in\{0,1,2\}.
\]
If \(G(0,0)=G(1,1)=G(2,2)\), then
\[
0=G(2,2)-2G(1,1)+G(0,0)
=\int(|\lambda|^2-1)^2\,d\nu.
\]
Hence \(\nu\) is supported on the unit circle. This is an elementary positivity-and-invariance mechanism with no transcendence assumption.

For a bilateral zeta version, choose strictly positive summable weights, such as \(v_\rho=(1+|\rho|^2)^{-2}\), and set
\[
G(K,L)=\sum_\rho v_\rho\eta_\rho(K)\overline{\eta_\rho(L)}.
\]
The sums converge for every fixed pair of grades because the \(\lambda_\rho\) lie in a fixed compact annulus. Then
\[
G(1,1)+G(-1,-1)-2G(0,0)
=\sum_\rho v_\rho B_\rho(2).
\]
Every term on the right is nonnegative. Stationarity of this same positive kernel forces every defect to vanish. The formula is not an independent proof of stationarity: constructing it from zeros merely exposes the missing condition.

### 4. Exact correspondences

| Known theorem object | TC candidate | Required verification |
|---|---|---|
| \(K\in\mathbb Z\) | Bilateral grade | Common group action |
| Unit-circle character | \(\eta_\rho(K)\) | Actual spectral occurrence, not just formal exponent |
| Positive stationary kernel | Arithmetic grade correlation | All finite coefficient tests |
| GNS Hilbert quotient | Arithmetic test space modulo null vectors | Positivity; no loss of needed modes |
| Bounded invertible \(T\) | One grade step | Uniform bilateral powers or adequate spectral bounds |
| Frame analysis range | Consistent grade coefficients | Frame bounds and range projection |
| Mellin spectral parameter | \(-i(\rho-1/2)\) | Faithful spectral membership |
| Hermite–Biehler family | Shifted centered xi | Required modulus inequality |
| Weil distribution | Prime/archimedean quadratic form | Exact identity, domain and positivity |
| Tate-twisted comparison object | Period grading | Actual geometry and compatible realizations |

## Part V — Known barriers and negative findings

### Coordinate consistency permits off-line quartets

For \(0<d<1/2\), \(t>0\), and \(w=s-1/2\),
\[
F(s)=((w-d)^2+t^2)((w+d)^2+t^2)
\]
is real entire, satisfies \(F(s)=F(1-s)\), and has zeros \(1/2\pm d\pm it\). Its pullbacks \(F(\tau^{-K}s)\) obey all the elementary TC transition identities. This control lacks zeta arithmetic; it proves that coordinate consistency and reflection alone cannot be the exclusion principle.

### Gram positivity is not stationary positivity

For any \(\lambda\ne0\), the rank-one kernel \(G(K,L)=\lambda^K\overline\lambda^{\,L}\) is positive semidefinite. Simultaneous shift multiplies it by \(|\lambda|^2\). Herglotz concerns a positive *difference kernel* \(c(K-L)\), not an arbitrary Gram matrix.

Boundedness alone also fails: \(c(0)=1\), \(c(\pm1)=2\), and \(c(K)=0\) otherwise is bounded but its \(2\times2\) Toeplitz matrix is not positive.

### Herglotz uniqueness does not cover arbitrary complex moment representations

For every \(r>0\),
\[
\int_0^{2\pi}(re^{i\theta})^K\frac{d\theta}{2\pi}
=\begin{cases}1,&K=0,\\0,&K\ne0,\end{cases}
\qquad K\in\mathbb Z.
\]
Thus positive angular measures on off-unit circles have the same bilateral Laurent moments as Haar measure on the unit circle. Herglotz uniqueness is among measures **on the unit circle**. This continuous example is not a zeta model; it disproves the unrestricted inference from a displayed exponential decomposition to its purported spectral support. Genuine mixed moments, or actual operator-spectrum identification, supply stronger information.

### Formal eigenfunctions do not establish Hilbert spectral membership

A unitary translation operator has formal exponential eigenfunctions with arbitrary complex exponents in larger distribution spaces. Its spectral theorem constrains its Hilbert spectrum. A zero mode must be an actual spectral point or a suitably bounded eigenfunctional, with domains specified. Building a self-adjoint operator whose eigenvalues are merely the real ordinates \(\gamma\) discards the very displacement under investigation.

### Integer sampling aliases heights

The map \(\gamma\mapsto e^{-i\gamma\log\tau}\) identifies heights modulo \(2\pi/\log\tau\). It does not turn an individual off-unit modulus into a unit modulus, but it prevents full height recovery from one grade lattice. One seed may also miss modes. Passing to rational or real grades can remove aliasing for the specified continuous exponential family, but requires explicit topology and continuity assumptions.

### A bilateral orbit frame can be too strong

An unweighted complete bilateral orbit frame forces absolutely continuous unitary spectral type. If a unitary \(U\) has an eigenvector \(x\), then \(|\langle x,U^Kv\rangle|\) is constant in \(K\); the Bessel bound forces that constant to vanish, and completeness then fails on \(x\). A pure-point Hilbert–Pólya model cannot have this particular frame. Grade weights change the invariance identity. Bilateral boundedness is less restrictive.

### Arithmetic-grid separation does not place zeros on those grids

Rational-grade collision exclusion requires nonzero algebraic coefficients. It does not imply that a zero displacement is algebraic, or belongs simultaneously to two arithmetic grids. Algebraic irrational grades require additional arguments. A failure of Gelfond–Schneider or Baker hypotheses cannot be replaced by intuition that a transcendental base remains transcendental under every algebraic power.

### The exponential period and the TC scaling logarithm differ

The identity \(e^{2\pi i}=1\) concerns the exponential period. TC uses
\[
\exp[-K(\rho-1/2)\log(2\pi)].
\]
A period theorem about \(2\pi i\mathbb Z\) does not automatically become a theorem about powers of \(2\pi\). A cycle, lattice, comparison map or monodromy construction must connect them.

### Scattering, self-adjointness and positivity do different jobs

A unitary scattering matrix may have off-axis resonance poles. A self-adjoint operator may have negative spectrum. Thus self-adjointness of an operator representing Weil’s form does not prove that form nonnegative. A Hilbert–Pólya construction needs full centered-zero identification as well as self-adjointness.

### Finite families do not replace full theorem hypotheses

Herglotz requires every finite coefficient test. Weil requires the full prescribed function class. Restricted grade families need a density or zero-detection theorem. Positivity on separate cyclic subspaces does not prove positivity of their joint span without cross-seed terms. No finite computation is used here as evidence for a global claim.

### Functional theorems do not specialize automatically to constants

Ax-type theorems need nonconstant functions or dimension hypotheses. Numerical specialization can lose their information. Torus intersection theorems need a specified algebraic variety and suitable subgroup. Mere membership of \(\tau\) in \(\mathbb C^\times\) supplies neither.

### Novel terminology is not a novelty result

The critical-line/unit-modulus equivalence and the abstract representation mechanisms are established. A new TC theorem must provide a new arithmetic bridge, a sufficient smaller test class with a proved detection property, or an independently constructed object satisfying a known theorem’s hypotheses.

## Part VI — Recommended mathematical investigations

1. **Identify the exact pairing.** Write the arithmetic form, domain and involution explicitly. Derive its zero-side expansion and grade-transformation law. Determine whether positivity and invariance are being asserted for that same form.
2. **Seek an arithmetic positive factorization.** Retain the prime, pole and archimedean terms. A proved identity \(Q_W(f,f)=\|Af\|^2\) for an independently constructed arithmetic \(A\) would supply GNS’s input.
3. **Prove visibility of every zero.** Specify actual spectral membership, bounded evaluation functionals, or a negative-test detection theorem. Resolve convergence, nullspaces and aliasing.
4. **Investigate bilateral norm bounds.** If a positive Hilbert realization already exists independently, test uniform control of both \(T^K\) and \(T^{-K}\). Avoid imposing an orbit frame incompatible with the desired spectral type.
5. **Locate the genuinely period-specific step.** Replace \(\tau\) by arbitrary \(b>1\). If every argument survives, the mechanism is scale-generic. A period-specific branch must identify the extra structure using \(2\pi i\).
6. **Compare the full condition with known criteria.** Prove whether the proposed test family recovers Weil positivity, a de Branges condition, or a genuinely different sufficient assertion. Establish the necessary topology and density.

These are analytic/theorem investigations. The structural questions do not require larger numerical searches.

## Part VII — Final synthesis

### Best established mechanism

**Herglotz–Bochner with GNS.** For the complete arithmetic zeta distribution, **Weil’s positivity criterion** is the nearest established bridge to the zeros.

### Why

A positive stationary correlation yields unitary grade evolution. A faithfully represented zero must then satisfy \(|\tau^{-(\rho-1/2)}|=1\), giving \(\Re\rho=1/2\).

### What TC already has

From the supplied formulation: bilateral grades, exact transitions, characters attached to zeros, the correct critical-line equivalence, and a nonnegative defect. The established centered Weil framework also provides an exact arithmetic–spectral identity and unconditional simultaneous-shift invariance.

### What TC lacks

An independently proved **positive invariant realization that retains every relevant zero mode**. For Weil’s form, positivity is missing. For the ordinary Gram form, invariance and an arithmetic identification are missing. These are alternative versions of the bridge.

### Is it plausibly independent of RH?

The abstract representation theorems are independent of RH. Full Weil positivity and unitarity of all displayed zero characters are **known equivalent to RH**. The existence of a new independently justified TC arithmetic construction establishing them is **unknown**. None of the retrieved theorems supplies that construction from coordinate identities alone.

### Next proof target

For the exact centered arithmetic explicit-formula distribution, investigate
\[
\boxed{
W_{\rm arith}(f*\widetilde f)\ge0
\quad\text{for every }f\in C_c^\infty(\mathbb R),
\qquad \widetilde f(u)=\overline{f(-u)}.
}
\]
This is **RH_EQUIVALENT**, not a new result obtained by renaming a hypothesis. The substantive TC task is to derive it through an independently justified arithmetic factorization or norm. The smallest useful preceding audit is to identify which pairing the present arithmetic construction actually represents.

**The sharp question:** What arithmetic structure makes the exact reflected Weil pairing positive, or makes an independently positive, zero-sensitive Gram pairing invariant under both grade directions?

## References and source notes

The keyed references below identify inspected sources. Theorem numbers refer to the linked edition; manuscript and journal pagination can differ. Recent preprint assertions are separated from published equivalences. Unsuccessful theorem searches are not treated as proofs that a statement is globally open.

[H1] T. Tlas, *Nonstandard Proofs of Herglotz, Bochner and Bochner–Minlos Theorems*, Theorem 1. [Author PDF](https://bpb-eu-w2.wpmucdn.com/sites.aub.edu.lb/dist/3/101/files/2020/01/herglotzsubject.pdf).

[H2] L. H. Loomis, *An Introduction to Abstract Harmonic Analysis* (1953), §36A, pp.141–142. [Text](https://people.math.harvard.edu/~shlomo/212a/loomis.pdf).

[H3] M. Bays, *GNS constructions, and functions of positive type*, pp.2–3. [Notes](https://people.maths.ox.ac.uk/bays/misc/gns/gns.pdf).

[H4] R. van Dobben de Bruyn, *Locally compact abelian groups*, §2. [Notes](https://webspace.science.uu.nl/~dobbe012/doc/LCA.pdf).

[H5] B. Sz.-Nagy, *On uniformly bounded linear transformations in Hilbert space*, Acta Sci. Math.11(3),152–157; commonly cited 1947, archive catalog 1948. [Original](https://real.mtak.hu/212276/1/math_011_fasc_003_152-157.pdf).

[H6] NIST DLMF, §1.14(iv). [Eq.1.14.38](https://dlmf.nist.gov/1.14#E38).

[H7] J. Bertrand, P. Bertrand, J.-P. Ovarlez, *The Mellin Transform*, Ch.11, *The Transforms and Applications Handbook*, 2nd ed. (2000). [Author copy](https://www.jeanphilippeovarlez.com/publications/ewExternalFiles/the%20mellin%20.pdf).

[H8] C. Heil, *Frames and Time-Frequency Analysis*, day 1, Corollary 11, Theorem 12, Problem 8.18. [Notes](https://heil.math.gatech.edu/umd/day1.pdf).

[H9] O. Christensen, M. Hasannasab, F. Philipp, *Frame properties of operator orbits*, Math. Nachr.293(2020),52–66. DOI [10.1002/mana.201800344](https://doi.org/10.1002/mana.201800344); [arXiv version](https://arxiv.org/pdf/1804.03438), Theorem 4.8.

[H10] A. Grossmann, J. Morlet, T. Paul, *Transforms associated to square integrable group representations. II: Examples*, Ann. Inst. H. Poincaré45(3)(1986),293–309. [Original](https://www.numdam.org/item/AIHPA_1986__45_3_293_0.pdf).

[H11] N. Aronszajn, *Theory of Reproducing Kernels*, Trans. AMS68(3)(1950),337–404, Part I. DOI10.1090/S0002-9947-1950-0051437-7. [Scan](https://pages.stat.wisc.edu/~wahba/stat860public/pdf2/aronszajn.pdf).

- **[W1]** E. Bombieri and J. C. Lagarias, *Complements to Li's criterion for the Riemann hypothesis*, J. Number Theory **77** (1999), 274–287, Theorem 1, corollary, §3. [Author manuscript](https://websites.umich.edu/~lagarias/doc/bombieri.pdf).
- **[W2]** M. Suzuki, *Aspects of the screw function corresponding to the Riemann zeta-function*, J. London Math. Soc. **108** (2023), 1448–1487, Theorem 1.2, §3.2. [DOI](https://doi.org/10.1112/jlms.12785).
- **[W3]** X.-J. Li, *The Positivity of a Sequence of Numbers and the Riemann Hypothesis*, J. Number Theory **65** (1997), 325–333, Theorem 1. [DOI](https://doi.org/10.1006/jnth.1997.2137).
- **[W4]** L. Báez-Duarte, *A strengthening of the Nyman–Beurling criterion for the Riemann hypothesis*, Rend. Lincei Mat. Appl. **14** (2003), 5–11, Theorem 1.1. [Manuscript](https://arxiv.org/abs/math/0202141).
- **[W5]** T. Spindeler and N. Strungaru, *Tempered distributions with translation bounded measure as Fourier transform and the generalized Eberlein decomposition*, Math. Nachrichten **297** (2024). [DOI](https://doi.org/10.1002/mana.202100658). Standard theorem: Reed–Simon, *Methods of Modern Mathematical Physics II*, Theorem IX.10.
- **[W6]** M. Suzuki, *Li coefficients as norms of functions in a model space*, J. Number Theory **252** (2023), 177–194. [DOI](https://doi.org/10.1016/j.jnt.2023.05.007).
- **[W7]** T. Nakamura and M. Suzuki, *On infinitely divisible distributions related to the Riemann hypothesis*, Statistics & Probability Letters **201** (2023), 109889. [DOI](https://doi.org/10.1016/j.spl.2023.109889).
- **[W8]** M. Suzuki, *On the Hilbert space derived from the Weil distribution*, Canadian J. Math., online 3 November 2025. [DOI](https://doi.org/10.4153/S0008414X25101739).
- **[W9]** A. Connes, C. Consani and H. Moscovici, *Zeta Spectral Triples*, [arXiv:2511.22755v1](https://arxiv.org/html/2511.22755v1), 27 November 2025, Theorem 1.1, §8.
- **[W10]** M. Suzuki, *Weil's quadratic form via the screw function*, [arXiv:2606.09096v3](https://arxiv.org/html/2606.09096v3), 23 September 2026, Theorems 1.1, 1.3, 1.5 and Corollary 1.6.

- **[S1]** Jeffrey C. Lagarias, *Hilbert Spaces of Entire Functions, Automorphic L-Functions, and Schroedinger Operators* (2012), de Branges overview. [Author slides](https://websites.umich.edu/~lagarias/TALK-SLIDES/benasque-riemann2012jun.pdf).
- **[S2]** Masatoshi Suzuki, *Hamiltonians arising from L-functions in the Selberg class*, Journal of Functional Analysis (2021), Propositions 2.1–2.2. [arXiv:1606.05726](https://arxiv.org/pdf/1606.05726).
- **[S3]** Etienne Le Masson and Tuomas Sahlsten, *Quantum ergodicity for Eisenstein series on hyperbolic surfaces of large genus*, Mathematische Annalen 389 (2024), 845–898, §2.6. [DOI](https://doi.org/10.1007/s00208-023-02671-1).
- **[S4]** A. W. Knapp and E. M. Stein, *Intertwining operators for SL(n,R)*, in *Studies in Mathematical Physics* (Princeton, 1976), 239–267, p.246. [Author reprint](https://www.math.stonybrook.edu/~aknapp/pdf-files/bargmann.pdf).
- **[S5]** Werner Müller, *A spectral interpretation of the zeros of the constant term of certain Eisenstein series* (2007 preprint). [Author manuscript](https://www.math.uni-bonn.de/people/mueller/papers/zeros.pdf).
- **[S6]** Gerald Teschl, *Mathematical Methods in Quantum Mechanics*, GSM 99 (AMS, 2009), Theorem 5.2, p.124. [Author edition](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf).
- **[S7]** M. V. Berry and J. P. Keating, *The Riemann Zeros and Eigenvalue Asymptotics*, SIAM Review 41(2) (1999), 236–266. [DOI](https://doi.org/10.1137/S0036144598347497).
- **[S8]** Alain Connes, *Trace formula in noncommutative geometry and the zeros of the Riemann zeta function*, Selecta Mathematica 5 (1999), 29–106. [arXiv:math/9811068](https://arxiv.org/abs/math/9811068).
- **[S9]** Mark Pollicott and Polina Vytnova, *Zeros of the Selberg zeta function for symmetric infinite area hyperbolic surfaces*, Geometriae Dedicata (online 2018), Theorem 1.2. [DOI](https://doi.org/10.1007/s10711-018-0386-6).

- **[T1]** M. Waldschmidt, “Elliptic Functions and Transcendence,” *Surveys in Number Theory* (2008), 143–188, Theorems 6, 7, 9. [Author PDF](https://webusers.imj-prg.fr/~michel.waldschmidt/articles/pdf/SurveyTrdceEllipt2006.pdf).
- **[T2]** S. Dasgupta, “Ranks of matrices of logarithms of algebraic numbers I: the theorems of Baker and Waldschmidt–Masser” (2023), Theorems 1.1–1.2, 3.1. [arXiv:2303.02037](https://arxiv.org/abs/2303.02037).
- **[T3]** D. Marques and J. Sondow, “Schanuel’s conjecture and algebraic powers \(z^w\) and \(w^z\) with \(z\) and \(w\) transcendental” (2010/2011), Table 1. [arXiv:1010.6216](https://arxiv.org/abs/1010.6216).
- **[T4]** M. Waldschmidt, “The Four Exponentials Problem and the Schanuel Conjecture,” LNM 2313 (2023), 579–592, §4, Conjecture 2 and Theorem 3. [Author PDF](https://webusers.imj-prg.fr/~michel.waldschmidt/articles/pdf/FourExponentialsSchanuel.pdf).
- **[T5]** K. Soundararajan, *Transcendental Number Theory*, notes by I. Petrow (2011), §13, p.49, corrected restatement of Theorem 22. [Course notes](https://math.stanford.edu/~ksound/TransNotes.pdf).
- **[T6]** B. Adamczewski and C. Faverjon, “A new proof of Nishioka’s theorem in Mahler’s method,” *C. R. Math.* 361 (2023), 1011–1028, Theorems 1–2. [DOI](https://doi.org/10.5802/crmath.458).
- **[T7]** P. Corvaja and U. Zannier, “Finiteness theorems on elliptical billiards and a variant of the dynamical Mordell–Lang conjecture” (2023), Theorems 2.6–2.7; original Laurent theorem: *Invent. Math.* 78 (1984), DOI 10.1007/BF01388597. [Modern theorem statements](https://doi.org/10.1112/plms.12561).
- **[T8]** L. Silberman, *Fourier Series and the Poisson Summation Formula*, §§1–3, Exercises 2, 7, 13. [Notes](https://personal.math.ubc.ca/~lior/teaching/1011/613D_F10/Fourier+PoissonSum.pdf).
- **[T9]** P. L. Clark, *On Hodge Theory and DeRham Cohomology of Variétés* (2003), §2.1. [Notes](https://www.math.mcgill.ca/goren/SeminarOnCohomology/derham4.pdf).
- **[T10]** M. Kontsevich and D. Zagier, “Periods” (2001), Conjecture 1; PDF pp.8,12. [Author PDF](https://www.ihes.fr/~maxim/TEXTS/Periods.pdf).

[R1] The Stacks Project, *Glueing sheaves*, Section 6.33, Lemmas 6.33.2–6.33.4, tag 00AK, accessed 3 October 2026. [Theorem statements](https://stacks.math.columbia.edu/tag/00AK).

[R2] B. Adamczewski and J. P. Bell, *A problem about Mahler functions*, Ann. Sc. Norm. Super. Pisa (5) 17 (2017), 1301–1355. [DOI](https://doi.org/10.2422/2036-2145.201606_010); [author text](https://adamczewski.perso.math.cnrs.fr/Cobham.pdf).

[R3] R. Schäfke and M. F. Singer, *Mahler equations and rationality*, arXiv:1605.08830v2 (2017), Theorem 1 and Proposition 3. [Full text](https://arxiv.org/html/1605.08830v2).

[R4] A. Perelli and M. Righetti, *A rigidity theorem for translates of uniformly convergent Dirichlet series*, arXiv:1702.01683 (2017), Theorem 1. [Full text](https://arxiv.org/html/1702.01683v1).

[R5] Y. Lamzouri, S. Lester and M. Radziwiłł, *An effective universality theorem for the Riemann zeta-function*, arXiv:1611.10325v2 (2016), introduction and Theorem 1.1. [Full text](https://arxiv.org/html/1611.10325v2).

