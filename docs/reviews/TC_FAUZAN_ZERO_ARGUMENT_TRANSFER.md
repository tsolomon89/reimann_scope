# TASK-TC-039: Fauzan Hankel Irrationality Architecture Transfer to Zeta-Zero Arguments

## A. TASK-TC-038R Starting Point

`TASK-TC-038R` (`HEAD = 4aa4f12d2c09a285e77c3c27e029f5603d299fa0`, substantive commit `46a39f77a893c972434bb1cc96f8a5e2c2e90660`) audited Aabir Fauzan's September 2026 preprint *On the Irrationality of $\zeta(5)$* (`doi:10.5281/zenodo.22826419`) and its complete Lean 4 formalization in `mo271/Zeta5` (`Apery.irrational_five`, `Apery.irrational_zeta5`, `RiemannZetaValues.irrational_five`). It reconstructed Fauzan's mechanism as the six-step value-polynomial chain:
$$
\boxed{
\text{rational moment functional}
\longrightarrow
\text{Hankel determinant}
\longrightarrow
Q_n(X) \in \mathbb{Z}[X]
\longrightarrow
Q_n(\zeta(5)) > 0
\longrightarrow
Q_n(\zeta(5)) \ll e^{-c n^2}
\longrightarrow
\zeta(5) \notin \mathbb{Q},
}
$$
and isolated the fundamental structural distinction:
$$
\boxed{
\texttt{VALUE\_POLYNOMIAL\_ARCHITECTURE\_NEQ\_ARGUMENT\_POLYNOMIAL\_ARCHITECTURE}:
}
$$
in Fauzan's proof, $X = \zeta(5)$ is a **function value** at the fixed integer argument $s = 5$, whereas at a nontrivial zero $\rho = \beta + i\gamma$, the value $\zeta(\rho) = 0$ is already zero and the arithmetic unknown is the **argument** $\rho$ or ordinate $\gamma = \operatorname{Im}(\rho)$. `TASK-TC-038R` opened `SUBGATE-TC-039A` (`FAUZAN_HANKEL_TO_ZERO_ARGUMENT_TRANSFER_SUBGATE`), structured as the six-gate decision tree **Gates Z1–Z6** with termination at the earliest failed gate.

---

## B. Preflight Evidence Corrections

Before executing the Gate Z1–Z6 audit, four housekeeping evidence items from `TASK-TC-038R` were synchronized across code, artifacts, and canonical prose:

1. **External Lean Dependency Wording (`mo271/Zeta5`)**:
   - In `mo271/Zeta5`, `Apery/PNT.lean` imports `PrimeNumberTheoremAnd.Consequences`, which transitively imports `PrimeNumberTheoremAnd.Wiener`. Thus `PrimeNumberTheoremAnd/Wiener.lean` (which contains two `sorry`-backed declarations) lies **inside** the module transitive import graph (`EXTERNAL_IMPORT_GRAPH_CONTAINS_SORRY_DECLARATIONS`).
   - However, `#print axioms Apery.irrational_five` outputs only the three standard Lean 4 axioms `[propext, Classical.choice, Quot.sound]`, proving that those `sorry`-backed declarations are **not** reached by the target theorem's proof-term axiom closure (`TARGET_THEOREM_AXIOM_CLOSURE_EXCLUDES_SORRY_DECLARATIONS`).
2. **Formal Source-File Count Derived from Inventory**:
   - `tc.zero_arithmetic_invariants.verify_formal_source_inventory_provenance` dynamically derives the module count from `formal/RiemannScope.lean` (`33` local `RiemannScope.*` imports after adding `FauzanZeroArgumentTransfer.lean`) and `scripts/build_formal.py::FORMAL_SOURCE_FILES` / `certification.py::REQUIRED_FORMAL_SOURCES` (`34` files including the umbrella `formal/RiemannScope.lean`, with `643` total `theorem` declarations across the formal suite).
3. **Canonical Numerical Consistency**:
   - Verified repository-wide agreement with machine artifacts:
     - $S_4 = 0.0000736272212616895183267713070306015113128315963\ldots$;
     - Bounded-denominator $q \le 10^4$ rational exclusion for $\gamma_1$: closest rational $94109/6658$ with certified lower bound $|\gamma_1 - p/q| \ge 9.50797348022772 \times 10^{-10}$;
     - Explicit $D \le 4, H \le 3$ global minimum at $\rho_1$: $\min |P(\rho_1)| \ge 14.143565845725995$.
4. **External Theorem Identifiers**:
   - Replaced any occurrence of `irrational_zeta_five` with the exact `mo271/Zeta5` identifiers `Apery.irrational_five`, `Apery.irrational_zeta5`, and `RiemannZetaValues.irrational_five`.

---

## C. Fauzan Architecture Being Transferred

From [fauzan_zeta5_architecture.json](file:///c:/Development/Projects/reimann_scope/data/fauzan_zeta5_architecture.json):

| Component | Fauzan $\zeta(5)$ Architecture (`mo271/Zeta5`) |
|---|---|
| Parameter schedule | $K = 40n, \; N = 3n, \; h = K - N = 37n$ |
| Hankel matrix | $G_K(X)_{i,j} = \mu_X\!\left(\frac{D_N(t)^6 t^{i+j}}{D_K(t)}\right) \in \mathbb{Q}[X], \quad 0 \le i,j < 37n$ |
| Rational determinant | $\Delta_K(X) = \det G_K(X) \in \mathbb{Q}[X], \quad \deg \Delta_K = 37n$ |
| Rescaled / integer polynomial | $F_K(X) = S_K \Delta_K(X) \in \mathbb{Q}[X], \quad Q_n(X) = m_N(n) F_K(X) \in \mathbb{Z}[X]$ |
| Positivity at $X = \zeta(5)$ | Hermite formula $\int_0^\infty \frac{w(y)}{y^2 + j^2}\,dy = j^4(\zeta(5) - H_j^{(5)}) - \frac{1}{4} + \frac{1}{2j}$ turns $G_K(\zeta(5))$ into a positive-definite Gram matrix on $L^2((0,\infty), \nu_n(y)\,dy)$, so $Q_n(\zeta(5)) > 0$ |
| Analytic decay vs. normalizer | $\frac{1}{n^2}\log F_K(\zeta(5)) \lesssim -5.6034$ vs. $\frac{1}{n^2}\log m_N(n) \lesssim +0.0070$, yielding $0 < Q_n(\zeta(5)) \le \exp(-5.5964 n^2)$ |
| Irrationality contradiction | If $\zeta(5) = a/b$, then $b^{37n} Q_n(a/b) \in \mathbb{Z}_{\ge 1}$ while $b^{37n} Q_n(\zeta(5)) \to 0$ |

---

## D. Why Value-Polynomial and Argument-Polynomial Problems Differ

In Fauzan's proof:
1. The argument $s = 5$ is a fixed positive odd integer, which fixes the differential operator $\frac{d^4}{dy^4}\!\left(\frac{1}{e^{2\pi y}-1}\right)$, the weight $w(y) \propto y^5 \sum_{\ell \ge 1} \ell^4 e^{-2\pi \ell y} > 0$, the partial-sum poles $H_j^{(5)} \in \mathbb{Q}$, and the Bernoulli monomial moments $\mu(t^e) \in \mathbb{Q}$.
2. The target $\zeta(5)$ enters the moment functional $\mu_X$ **affinely as a value** inside $\mu_X(1/(t+j^2)) = j^4(X - H_j^{(5)}) - \frac{1}{4} + \frac{1}{2j}$.

At a nontrivial zero $\rho = \beta + i\gamma$ (such as $\rho_1 = \frac{1}{2} + i\gamma_1$):
1. The value $\zeta(\rho) = 0$ is already rational (zero), so a value-polynomial in $X = \zeta(\rho)$ merely evaluates $Q_n(0) \in \mathbb{Z}$, yielding no information about $\rho$ or $\gamma$.
2. In standard representations of $\zeta(s)$ or $\xi(s)$, the argument $s$ enters inside transcendental kernel functions ($n^{-s} = e^{-s\log n}$, $\pi^{-s/2}$, $\Gamma(s/2)$), which are **not** algebraic polynomials in $s$.
3. Converting Fauzan's paradigm to zero locations therefore requires constructing a zero-independent auxiliary polynomial $P_n(X) \in \mathbb{Z}[X]$ in the **argument variable** $X = \alpha_1 = \rho_1/2$ or $X = \gamma_1$ through rational interpolation, multipoint Padé approximation, or argument-coupled Hankel determinants of a rationally sampled entire surrogate of $\xi$.

---

## E. Gate Definitions Z1–Z6

| Gate | Name | Requirement | TASK-TC-039 / TC-039R Status |
|---|---|---|---|
| **Z1** | Argument-Target Representation | Construct an entire surrogate $\mathcal{R}_c(z) = (2z-1)c^z\tau^{-2z}\zeta(2z)$ ($c=4$ for $\mathcal{R}_\pi$, $c=1$ for $\mathcal{R}_\tau$) with $\mathcal{R}_c(\rho/2) = 0$ at nontrivial zeros and exact rational values $\mathcal{R}_c(m) = a_m^{(c)} \in \mathbb{Q}$ at all integers $m \in \mathbb{Z}_{\ge 0}$ | **`Z1_ARGUMENT_TARGET_REPRESENTATION_PROVED`** |
| **Z2** | Algebraic Argument Polynomiality | Construct deterministic, zero-independent polynomial families $P_n(X) \in \mathbb{Q}[X]$ (and cleared $\widetilde{P}_n(X) \in \mathbb{Z}[X]$) from $(a_m^{(c)})_{m \ge 0}$ without using $\gamma_1$ or $\rho_1$ in coefficients | **`Z2_ALGEBRAIC_ARGUMENT_POLYNOMIALITY_PROVED`** |
| **Z3** | Structural Nonvanishing | Prove $P_n(\alpha_1) \ne 0$ (or $G_n(\gamma_1) > 0$) structurally on an infinite cofinal subsequence without circularly assuming $\alpha_1 \notin \overline{\mathbb{Q}}$ | **`Z3_COFINAL_STRUCTURAL_NONVANISHING_PROVED_FOR_TWO_APPROXIMANT_NORM_SUM`** |
| **Z4** | Degree & Denominator Complexity | Quantify $\deg P_n = d_n$, denominator $\operatorname{lcm}$ $L_n$, and height $\log H(\widetilde{P}_n)$ across $\pi$- and $\tau$-normalizations | **`Z4_DEGREE_AND_DENOMINATOR_COMPLEXITY_QUANTIFIED_FACTORIAL_DENOMINATOR_OBSTRUCTION`** |
| **Z5** | Analytic Smallness at Zero | Achieve $\mathcal{I}_n = \frac{-\log|\widetilde{P}_n(\alpha_1)|}{d_n} \to +\infty$ for integer polynomials $\widetilde{P}_n \in \mathbb{Z}[X]$ | **`Z5_SUPERLINEAR_LOG_SMALLNESS_FAILED_IN_TESTED_NEWTON_PADE_HANKEL_CLASSES`** *(Earliest Failed Gate)* |
| **Z6** | Diophantine Contradiction | Combine Z1–Z5 to deduce $\gamma_1 \notin \mathbb{Q}$ (or $\gamma_1 \notin \overline{\mathbb{Q}}$) | **`Z6_NOT_REACHED_TERMINATED_AT_GATE_Z5`** |

---

## F. Rationalized-$\xi$ Construction

Define the rationalized-$\xi$ function in $\pi$-normalization ($\mathcal{R}_\pi$) and $\tau$-normalization ($\mathcal{R}_\tau$, where $\tau = 2\pi$):
$$
\boxed{
\mathcal{R}_\pi(z) := \frac{\pi^{-z}\xi(2z)}{\Gamma(z+1)} = (2z - 1)\pi^{-2z}\zeta(2z) = 4^z \mathcal{R}_\tau(z), \qquad \mathcal{R}_\tau(z) := \frac{2^z \tau^{-z}\xi(2z)}{\Gamma(z+1)} = (2z - 1)\tau^{-2z}\zeta(2z).
}
$$

1. **Equivalence of the definitions**: Since $\xi(s) = \frac{1}{2}s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s)$, substituting $s = 2z$ gives $\xi(2z) = z(2z-1)\pi^{-z}\Gamma(z)\zeta(2z)$. Dividing by $\pi^z \Gamma(z+1) = \pi^z z\Gamma(z)$ yields $(2z-1)\pi^{-2z}\zeta(2z) = 4^z(2z-1)\tau^{-2z}\zeta(2z)$ identically on $\mathbb{C}$.
2. **Entirety and removable singularity at $z = 1/2$**: Because $\pi^{-z}$, $\xi(2z)$, and $1/\Gamma(z+1)$ are entire on $\mathbb{C}$, $\mathcal{R}_\pi(z)$ and $\mathcal{R}_\tau(z)$ are entire on $\mathbb{C}$. At $z = 1/2$, the simple pole $\zeta(1 + 2\varepsilon) = \frac{1}{2\varepsilon} + \gamma_E + O(\varepsilon)$ cancels against $(2z - 1) = 2\varepsilon$, giving:
   $$
   \mathcal{R}_\pi\!\left(\frac{1}{2}\right) = \frac{1}{\pi}, \qquad \mathcal{R}_\tau\!\left(\frac{1}{2}\right) = \frac{1}{\tau}.
   $$
3. **Zero mapping**: Inside the critical strip $0 < \operatorname{Re}(2z) < 1$ (i.e., $0 < \operatorname{Re}(z) < 1/2$), $\pi^{-z} \ne 0$, $\tau^{-z} \ne 0$, and $\operatorname{Re}(z+1) \in (1, 3/2)$ where $\Gamma(z+1)$ has neither zeros nor poles. Therefore:
   $$
   \xi(\rho) = 0 \Longleftrightarrow \mathcal{R}_\pi\!\left(\frac{\rho}{2}\right) = 0 \Longleftrightarrow \mathcal{R}_\tau\!\left(\frac{\rho}{2}\right) = 0.
   $$
   For the first nontrivial critical-line zero $\rho_1 = \frac{1}{2} + i\gamma_1$, the scaled zero argument is:
   $$
   \boxed{
   \alpha_1 := \frac{\rho_1}{2} = \frac{1}{4} + i\frac{\gamma_1}{2}, \qquad \mathcal{R}_\pi(\alpha_1) = \mathcal{R}_\tau(\alpha_1) = 0.
   }
   $$
   In addition, $\mathcal{R}_\pi(-m) = \mathcal{R}_\tau(-m) = 0$ at all negative integers $z = -1, -2, \dots$ (the trivial zeros of $\zeta(2z)$ / poles of $\Gamma(z+1)$).

---

## G. Rational Samples at Nonnegative Integers

By Euler's even-zeta theorem, for every integer $m \ge 1$:
$$
\zeta(2m) = (-1)^{m+1}\frac{\tau^{2m} B_{2m}}{2(2m)!} = (-1)^{m+1}\frac{(2\pi)^{2m} B_{2m}}{2(2m)!},
$$
where $B_{2m} \in \mathbb{Q}$ is the $2m$-th Bernoulli number ($B_0 = 1, B_2 = 1/6, B_4 = -1/30, B_6 = 1/42, \dots$). Thus $\tau$-normalization exposes the pure Bernoulli-factorial rational core $a_m^{(\tau)} = \mathcal{R}_\tau(m) = (-1)^{m+1}\frac{(2m-1)B_{2m}}{2(2m)!}$, while $\pi$-normalization scales by $4^m$:
$$
\boxed{
a_m := a_m^{(\pi)} = \mathcal{R}_\pi(m) = 4^m a_m^{(\tau)} = (-1)^{m+1}\frac{(2m-1) 2^{2m-1} B_{2m}}{(2m)!} \in \mathbb{Q}_{>0} \qquad (\forall m \ge 0).
}
$$
At $m = 0$, the formula gives $a_0^{(\pi)} = a_0^{(\tau)} = \frac{1}{2}$, which agrees with $(-1)\zeta(0) = -(-1/2) = 1/2$.

| $m$ | Exact $a_m = \mathcal{R}_\pi(m) \in \mathbb{Q}_{>0}$ | Decimal Approximation | $\log \operatorname{den}(a_m)$ |
|---|---|---|---|
| $0$ | $1/2$ | $5.000000 \times 10^{-1}$ | $0.6931$ |
| $1$ | $1/6$ | $1.666667 \times 10^{-1}$ | $1.7918$ |
| $2$ | $1/30$ | $3.333333 \times 10^{-2}$ | $3.4012$ |
| $3$ | $1/189$ | $5.291005 \times 10^{-3}$ | $5.2417$ |
| $4$ | $1/1350$ | $7.407407 \times 10^{-4}$ | $7.2079$ |
| $5$ | $1/10395$ | $9.620010 \times 10^{-5}$ | $9.2491$ |
| $6$ | $691/58046625$ | $1.190422 \times 10^{-5}$ | $17.8768$ |
| $7$ | $2/1403325$ | $1.425187 \times 10^{-6}$ | $14.1544$ |
| $8$ | $3617/21709437750$ | $1.666096 \times 10^{-7}$ | $23.8010$ |
| $9$ | $43867/2292899734125$ | $1.913167 \times 10^{-8}$ | $28.4608$ |
| $10$ | $174611/80596287646875$ | $2.166489 \times 10^{-9}$ | $32.0205$ |

Classification: **`RATIONALIZED_XI_RATIONAL_INTEGER_SAMPLING_PROVED`**.

---

## H. Bernoulli Generating Function

Consider the ordinary generating functions $A_\pi(t) := \sum_{m=0}^\infty a_m^{(\pi)} t^m$ and $A_\tau(t) := \sum_{m=0}^\infty a_m^{(\tau)} t^m$. Using the cotangent expansion:
$$
\frac{\sqrt{t}\cot\sqrt{t}}{2} = \sum_{m=0}^\infty (-1)^m \frac{2^{2m-1} B_{2m}}{(2m)!} t^m \qquad (|t| < \pi^2),
$$
and applying the operator $1 - 2t\frac{d}{dt}$ (which multiplies $t^m$ by $1 - 2m = -(2m-1)$) yields the closed forms:
$$
\boxed{
A_\pi(t) = \frac{t}{2\sin^2\sqrt{t}} \quad (|t| < \pi^2), \qquad A_\tau(t) = A_\pi(t/4) = \frac{t}{8\sin^2(\sqrt{t}/2)} \quad (|t| < \tau^2 = 4\pi^2).
}
$$

---

## I. Positive Moment Subsequence

For $m \ge 1$, dividing $a_m^{(c)} = (2m-1)c^m\tau^{-2m}\zeta(2m)$ by $(2m-1)$ gives the strictly positive rational Hausdorff/Stieltjes moment sequence (with $b_0^{(\pi)} = \pi^{-2}\zeta(2) = 1/6 > 0$ and $b_0^{(\tau)} = \tau^{-2}\zeta(2) = 1/24 > 0$, shifting off $m = 0$ where $a_0/(2\cdot 0 - 1) = -1/2 < 0$):
$$
\boxed{
b_{m-1}^{(\pi)} := \frac{a_m^{(\pi)}}{2m-1} = \pi^{-2m}\zeta(2m) = \sum_{k=1}^\infty (\pi k)^{-2m} \in \mathbb{Q}_{>0}, \qquad b_{m-1}^{(\tau)} := \frac{a_m^{(\tau)}}{2m-1} = \tau^{-2m}\zeta(2m) = 4^{-m} b_{m-1}^{(\pi)} \in \mathbb{Q}_{>0},
}
$$
with generating functions $B_\pi(t) = \frac{1 - \sqrt{t}\cot\sqrt{t}}{2t}$ ($|t| < \pi^2$) and $B_\tau(t) = \frac{1 - (\sqrt{t}/2)\cot(\sqrt{t}/2)}{8t} = \frac{1}{4}B_\pi(t/4)$ ($|t| < \tau^2$).

---

## J. Newton Argument-Polynomial Construction

Using the forward differences $\Delta^k a_0^{(c)} = \sum_{j=0}^k (-1)^{k-j}\binom{k}{j}a_j^{(c)} \in \mathbb{Q}$ at the nonnegative integers $0, 1, \dots, n$, the degree-$n$ Newton interpolation polynomial of $\mathcal{R}_c(z)$ is:
$$
\boxed{
N_n^{(c)}(z) := \sum_{k=0}^n (\Delta^k a_0^{(c)})\binom{z}{k} \in \mathbb{Q}[z], \qquad N_n^{(c)}(m) = a_m^{(c)} = \mathcal{R}_c(m) \quad (0 \le m \le n).
}
$$
Expanding $\binom{z}{k} = \frac{z(z-1)\cdots(z-k+1)}{k!}$ gives $N_n^{(c)}(z) = \sum_{j=0}^n c_{n,j}^{(c)} z^j \in \mathbb{Q}[z]$, and multiplying by $L_n^{(c)} := \operatorname{lcm}(\operatorname{den}(c_{n,0}^{(c)}), \dots, \operatorname{den}(c_{n,n}^{(c)}))$ produces the primitive integer polynomial:
$$
\widetilde{N}_n^{(c)}(z) := L_n^{(c)} N_n^{(c)}(z) \in \mathbb{Z}[z].
$$
Crucially, $N_n^{(c)}$ and $\widetilde{N}_n^{(c)}$ are constructed purely from the Bernoulli rational sequence $(a_m^{(c)})_{0 \le m \le n}$ (`candidate_coefficients_depend_on_gamma1 = False`).

Classification: **`NEWTON_ARGUMENT_POLYNOMIALIZATION_PROVED`**.

---

## K. Newton Remainder and Direct Convergence Without Carlson

Because $\mathcal{R}_c(\alpha_1) = 0$, the exact evaluation of $N_n^{(c)}$ at the zero argument $\alpha_1 = \rho_1/2$ equals minus the interpolation remainder:
$$
N_n^{(c)}(\alpha_1) = N_n^{(c)}(\alpha_1) - \mathcal{R}_c(\alpha_1) = -R_n^{(c)}(\alpha_1) = -\sum_{k=n+1}^\infty (\Delta^k a_0^{(c)})\binom{\alpha_1}{k}.
$$
Notice that $\mathcal{R}_c(z)$ has Stirling vertical growth $|\mathcal{R}_c(\sigma \pm it)| \asymp |t|^{\sigma - 1/2} e^{\pi |t|/2}$ of superexponential order $1$ along $\operatorname{Re}(z) \to -\infty$, so Carlson's uniqueness theorem is **not** invoked. Instead, as proved in [TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md) (§K), for any $0 < c < \tau^2$ (including $c = 1$ and $c = 4$):
1. The stretched-exponential coefficient bound $|\Delta^n a_0^{(c)}| = O(n^{1/2}\exp(-\kappa(c)n^{1/3}))$ ($\kappa(c) = \frac{3}{2^{5/3}}c^{1/3} > 0$) combined with polynomial binomial growth $|\binom{z}{n}| = O_K(n^{\max_K(-\operatorname{Re}(z))-1})$ proves that $F_c(z) := \sum_{n=0}^\infty (\Delta^n a_0^{(c)})\binom{z}{n}$ converges **absolutely and locally uniformly on all of $\mathbb{C}$** to an entire function;
2. On the open half-plane $\operatorname{Re}(z) > 1/2$, absolute Fubini interchange of the subtracted Dirichlet-binomial double series proves directly that $F_c(z) = \mathcal{R}_c(z)$ on $\{z \in \mathbb{C} : \operatorname{Re}(z) > 1/2\}$;
3. By the open-set identity theorem for analytic functions, $F_c(z) = \mathcal{R}_c(z)$ holds **on all of $\mathbb{C}$**, including at $\alpha_1 = \frac{1}{4} + i\frac{\gamma_1}{2}$ (`NEWTON_SERIES_IDENTITY_FOR_RATIONALIZED_XI_PROVED_WITHOUT_CARLSON`).

---

## L. Newton Finite-Difference Asymptotics and Saddle Repair

We compare the finite differences of $b_m^{(c)}$ with those of $a_m^{(c)} = (2m-1)c^m\tau^{-2m}\zeta(2m)$:

1. **Positive Moment Differences**: Since $b_{m-1}^{(c)} = \sum_{k=1}^\infty q_{k,c}^m$ with $q_{k,c} = c(\tau k)^{-2} \in (0, 1)$,
   $$
   (-1)^n \Delta^n b_0^{(c)} = \sum_{k=1}^\infty q_{k,c}(1 - q_{k,c})^n = \frac{\sqrt{c}}{4\sqrt{\pi}} n^{-1/2} + O(n^{-1}) > 0 \qquad (\forall n \ge 0).
   $$
2. **Exact Cancellation of Algebraic Powers and Repaired Saddle Exponent**:
   For $q_c(x) = c(\tau x)^{-2}$, the continuous integral vanishes identically via the exact derivative identity:
   $$
   \int_{\sqrt{c}/\tau}^\infty q_c(x)(1 - q_c(x))^{n-1}\bigl(1 - (2n+1)q_c(x)\bigr)\,dx = \left[-\frac{c}{\tau^2 x}\left(1 - \frac{c}{\tau^2 x^2}\right)^n\right]_{\sqrt{c}/\tau}^\infty = 0!
   $$
   Equivalently, the Euler difference generating function:
   $$
   C_c(w) := \sum_{n=0}^\infty (\Delta^n a_0^{(c)}) w^n = \frac{1}{1+w}\,A_c\!\left(\frac{w}{1+w}\right) = \frac{c w}{8(1+w)^2 \sin^2\!\left(\frac{1}{2}\sqrt{\frac{c w}{1+w}}\right)}
   $$
   satisfies $C_c(-1+s) \sim \frac{c}{2s^2}\exp(-\sqrt{c}/\sqrt{s})$ as $s = 1+w \to 0$ ($\operatorname{Re}(s) > 0$). Because $a_m^{(c)}$ already normalizes out $\pi^{-2m}$ (or $\tau^{-2m}$), no factor of $\pi$ appears inside $\exp(-\sqrt{c}/\sqrt{s})$ (`pi_pow_2_over_3_contamination_present = False`). Steepest-descent analysis around the conjugate saddles $s_\pm = (\frac{\sqrt{c}}{2n})^{2/3} e^{\pm 2\pi i/3}$ yields the exact asymptotic ([TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md) §M):
   $$
   \boxed{
   \Delta^n a_0^{(c)} = (-1)^{n+1}\frac{2\sqrt{c}}{\sqrt{3\pi}} n^{1/2}\exp\!\bigl(-\kappa(c)n^{1/3}\bigr)\!\left[\cos\!\bigl(\omega(c)n^{1/3} + \tfrac{\pi}{6}\bigr) + O(n^{-1/3})\right],
   }
   $$
   where $\kappa(c) = \frac{3}{2^{5/3}}c^{1/3}$ and $\omega(c) = \sqrt{3}\,\kappa(c)$. In particular:
   $$
   \boxed{
   \kappa_\pi = \kappa(4) = \frac{3}{2} = 1.5, \qquad \kappa_\tau = \kappa(1) = \frac{3}{2^{5/3}} \approx 0.94494079.
   }
   $$
   At $n = 200$, $|\Delta^{200} b_0^{(\pi)}| = 1.999937 \times 10^{-2}$ ($\approx \frac{1}{2\sqrt{200\pi}}$), whereas $|\Delta^{200} a_0^{(\pi)}| = 2.882330 \times 10^{-3}$ and $|\Delta^{200} a_0^{(\tau)}| = 2.660662 \times 10^{-2}$.


---

## M. Newton Irrationality Kill Test

Let us evaluate the Newton polynomials $N_n(\alpha_1)$ and primitive integer polynomials $\widetilde{N}_n(\alpha_1) = L_n N_n(\alpha_1)$ at the certified 128-bit Acb enclosure of $\alpha_1 = \frac{1}{4} + i\frac{\gamma_1}{2}$:

| $n$ | $d_n$ | $\log L_n$ | $\log H(\widetilde{N}_n)$ | $-\log|N_n(\alpha_1)|$ | $\mathcal{I}_n^{\mathrm{rat}} = \frac{-\log|N_n(\alpha_1)|}{n}$ | $-\log|\widetilde{N}_n(\alpha_1)|$ | $\mathcal{I}_n^{\mathrm{int}} = \frac{-\log|\widetilde{N}_n(\alpha_1)|}{n}$ |
|---|---|---|---|---|---|---|---|
| $5$ | $5$ | $14.7297$ | $14.0366$ | $-2.7372$ | $-0.5474$ | $-17.4670$ | $-3.4934$ |
| $10$ | $10$ | $52.7084$ | $52.0152$ | $-5.1272$ | $-0.5127$ | $-57.8355$ | $-5.7836$ |
| $20$ | $20$ | $134.7307$ | $134.2086$ | $-5.2251$ | $-0.2613$ | $-139.9558$ | $-6.9978$ |
| $40$ | $40$ | $342.2742$ | $341.5859$ | $-5.5093$ | $-0.1377$ | $-347.7835$ | $-8.6946$ |
| $80$ | $80$ | $838.5343$ | $837.8412$ | $-4.4355$ | $-0.0554$ | $-842.9699$ | $-10.5371$ |
| $120$ | $120$ | $1406.0734$ | $1405.3803$ | $-3.8758$ | $-0.0323$ | $-1409.9492$ | $-11.7496$ |
| $160$ | $160$ | $1989.9417$ | $1989.2486$ | $-3.0570$ | $-0.0191$ | $-1992.9988$ | $-12.4562$ |
| $200$ | $200$ | $2629.3406$ | $2628.6475$ | $-2.8159$ | $-0.0141$ | $-2632.1566$ | $-13.1608$ |

**Exact Obstruction at Gate Z5**:
1. **Stretched-exponential remainder vs. linear degree**: Because $-\log|N_n(\alpha_1)| \asymp n^{1/3}$ while $d_n = n$, even the *un-cleared* rational ratio satisfies:
   $$
   \mathcal{I}_n^{\mathrm{rat}} = \frac{-\log|N_n(\alpha_1)|}{n} = O(n^{-2/3}) \longrightarrow 0 \not\to +\infty.
   $$
2. **Factorial + Bernoulli denominator growth**: Clearing denominators to obtain $\widetilde{N}_n \in \mathbb{Z}[z]$ multiplies $N_n$ by $L_n = \operatorname{lcm}_{0 \le j \le n}\operatorname{den}(c_{n,j})$, where $n!$ from $\binom{z}{k}$ and $(2k)!$ from $a_k$ give $\log L_n = 3n\log n + O(n)$. Hence:
   $$
   \mathcal{I}_n^{\mathrm{int}} = \frac{-\log|\widetilde{N}_n(\alpha_1)|}{n} \sim -3\log n \longrightarrow -\infty.
   $$
Classification: **`NEWTON_ARGUMENT_POLYNOMIAL_ROUTE_INSUFFICIENT_SMALLNESS`**.

---

## N. Real Ordinate Norm-Polynomial Conversion

To test the real ordinate $\gamma_1 \in \mathbb{R}$ directly via $\alpha(Y) := \frac{1}{4} + i\frac{Y}{2}$, for any polynomial $P(z) = \sum_{j=0}^d c_j z^j \in \mathbb{Q}[z]$ we define its conjugate-paired norm polynomial:
$$
\boxed{
\mathcal{N}_P(Y) := P\!\left(\frac{1}{4} + i\frac{Y}{2}\right) \overline{P}\!\left(\frac{1}{4} - i\frac{Y}{2}\right) \in \mathbb{Q}[Y].
}
$$
Because $\overline{P(z)} = P(\bar{z})$ for $P \in \mathbb{Q}[z]$, $\mathcal{N}_P(Y)$ is invariant under $i \mapsto -i$, so all odd powers of $i$ cancel identically and $\mathcal{N}_P(Y) \in \mathbb{Q}[Y]$ has rational coefficients, degree $\deg \mathcal{N}_P \le 2\deg P$, and satisfies:
$$
\mathcal{N}_P(Y) = \left|P\!\left(\frac{1}{4} + i\frac{Y}{2}\right)\right|^2 \ge 0 \qquad (\forall Y \in \mathbb{R}).
$$
Clearing the denominators of $P(1/4 + iY/2)$ by $4^d \operatorname{lcm}(\operatorname{den}(c_j))^2$ produces the integer polynomial $\widetilde{\mathcal{N}}_P(Y) \in \mathbb{Z}[Y]$. These three properties are formally proved in Lean 4 (`argument_norm_polynomial_real`, `argument_norm_polynomial_nonneg`, `argument_norm_polynomial_degree_bound`).

---

## O. Consecutive-Approximant Strict Positivity

How can Gate Z3 (structural nonvanishing at $\gamma_1$) be proved without knowing beforehand that $\gamma_1 \notin \overline{\mathbb{Q}}$?
Consider two consecutive Newton polynomials $N_n(z)$ and $N_{n+1}(z)$:
$$
N_{n+1}(z) - N_n(z) = (\Delta^{n+1} a_0)\binom{z}{n+1} = \frac{\Delta^{n+1} a_0}{(n+1)!}\prod_{m=0}^n (z - m).
$$
1. **Consecutive Common-Root Theorem**: If $\Delta^{n+1}a_0 \ne 0$ and $z \in \mathbb{C}$ satisfies $N_n(z) = N_{n+1}(z) = 0$, then $\prod_{m=0}^n (z - m) = 0$, so $z = m \in \{0, 1, \dots, n\}$.
2. **Exclusion at Nodes**: At every node $m \in \{0, 1, \dots, n\}$, $N_n(m) = a_m > 0$, so $N_n(m) \ne 0$. Therefore $\gcd(N_n, N_{n+1}) = 1$ in $\mathbb{Q}[z]$ and $N_n, N_{n+1}$ have **no common complex root** $z \in \mathbb{C}$.
3. **Strict Positivity on $\mathbb{R}$**: Consequently, the two-approximant integer norm-sum polynomial:
   $$
   \boxed{
   G_n(Y) := C_n\bigl(\mathcal{N}_{N_n}(Y) + \mathcal{N}_{N_{n+1}}(Y)\bigr) \in \mathbb{Z}[Y], \qquad \deg G_n = 2n + 2,
   }
   $$
   satisfies $G_n(Y) > 0$ for **every** $Y \in \mathbb{R}$ (and in particular $G_n(\gamma_1) \in \mathbb{Z}_{\ge 1}$ whenever $\gamma_1 = p/q$, after multiplying by $q^{2n+2}$) for every $n$ with $\Delta^{n+1}a_0 \ne 0$.
4. **Cofinal Infinitude**: Because $a_m > 0$ and $\lim_{m\to\infty} a_m = 0 \ne a_0 = 1/2$, the sequence $(a_m)$ is not a polynomial in $m$, so $\Delta^{n+1}a_0 \ne 0$ for infinitely many $n \in \mathbb{N}$ (and is certified for every $0 \le n \le 200$).

These theorems are formalized with 0 `sorry` in `formal/RiemannScope/FauzanZeroArgumentTransfer.lean` (`newton_consecutive_common_root_forces_node`, `newton_consecutive_no_common_root_of_nonzero_samples`, `two_approximant_norm_sum_strict_pos`).
Classification: **`Z3_COFINAL_STRUCTURAL_NONVANISHING_PROVED_FOR_TWO_APPROXIMANT_NORM_SUM`**.

---

## P. Multipoint Padé Construction

Because Route A (Newton polynomial interpolation) fails Gate Z5 due to slow $O(n^{1/3})$ log-remainder decay and $3n\log n$ denominator growth, we test **Route B: Multipoint Padé Approximation** on the integer nodes $m = 0, 1, \dots, d_A + d_B$.
For a fixed deterministic degree schedule $(d_A, d_B) \in \{[n/n], [n/(n-1)], [(n-1)/n]\}$ with $M = d_A + d_B$, we seek polynomials $A_n(z) = \sum_{j=0}^{d_A} p_j z^j \in \mathbb{Q}[z]$ and $B_n(z) = \sum_{k=0}^{d_B} q_k z^k \in \mathbb{Q}[z]$ satisfying the linearized homogeneous interpolation system:
$$
\boxed{
A_n(m) - a_m B_n(m) = 0 \qquad (m = 0, 1, \dots, d_A + d_B).
}
$$
This is a system of $M + 1$ exact rational linear equations in $M + 2$ unknowns $(p_0, \dots, p_{d_A}, q_0, \dots, q_{d_B})$ with coefficient matrix $L_{m,j} = m^j$ ($0 \le j \le d_A$) and $L_{m, d_A+1+k} = -a_m m^k$ ($0 \le k \le d_B$).

---

## Q. Padé Determinant and Arithmetic Normalization

Across all three deterministic schedules $[n/n]$ ($1 \le n \le 25$), $[n/(n-1)]$ ($1 \le n \le 15$), and $[(n-1)/n]$ ($1 \le n \le 15$):
- Exact rational Gaussian elimination over $\mathbb{Q}$ (`flint.fmpq_mat`) certifies **full row rank $M+1$ and nullspace dimension $1$** at every tested $n$, with $B_n(0) \ne 0$, leading coefficient of $B_n$ nonzero, and $\gcd(A_n, B_n) = 1$.
- Thus $(A_n, B_n)$ is **projectively unique** up to a nonzero scalar $\lambda \in \mathbb{Q}^\times$.
- However, scalar normalization matters critically at Gate Z5:
  1. **$B_n(0) = 1$ normalization**: fixes the constant term of $B_n$ to $1$;
  2. **Monic $B_n$ normalization**: fixes the leading coefficient $q_{d_B} = 1$;
  3. **Canonical primitive integer normalization $\widetilde{A}_n \in \mathbb{Z}[z]$**: multiplies $A_n$ by $\operatorname{lcm}(\operatorname{den}) / \gcd(\operatorname{num})$ so that $\widetilde{A}_n(z) \in \mathbb{Z}[z]$ has coprime integer coefficients. This is the unique normalization admissible for the integer-polynomial irrationality lemma (`rational_evaluation_integer_clearing`).

---

## R. Padé Analytic Residual

At the zero argument $\alpha_1 = \rho_1/2$ where $\mathcal{R}(\alpha_1) = 0$, the linearized Padé residual satisfies the exact identity (formalized as `pade_interpolation_zero_residual_identity`):
$$
\boxed{
R_n(\alpha_1) := A_n(\alpha_1) - \mathcal{R}(\alpha_1) B_n(\alpha_1) = A_n(\alpha_1).
}
$$
Dividing by $B_n(\alpha_1) \ne 0$ gives the rational approximant error:
$$
\frac{A_n(\alpha_1)}{B_n(\alpha_1)} = \frac{A_n(\alpha_1)}{B_n(\alpha_1)} - \mathcal{R}(\alpha_1) = \frac{1}{2\pi i}\int_{\mathcal{C}_n} \frac{\mathcal{R}(w)}{B_n(w) B_n(\alpha_1)(w - \alpha_1)}\prod_{m=0}^{d_A+d_B} \frac{\alpha_1 - m}{w - m}\,dw.
$$
Why does the rational quotient $|A_n(\alpha_1)/B_n(\alpha_1)|$ become small ($4.17 \times 10^{-10}$ at $n = 25$ for $[n/n]$), while the primitive integer polynomial $|\widetilde{A}_n(\alpha_1)|$ blows up?
Because the nodal product $\prod_{m=0}^{2n}|\alpha_1 - m| \sim (2n)! |\Gamma(-\alpha_1)|^{-1}$ grows factorially, and the denominator polynomial $B_n(z)$ absorbs that factorial growth by having $|B_n(\alpha_1)| \asymp (2n)!$ (when normalized by $B_n(0)=1$). The numerator $A_n(\alpha_1)$ alone does **not** carry the $1/B_n(\alpha_1)$ factor, and clearing the rational denominators of $A_n(z)$ to form $\widetilde{A}_n(z) \in \mathbb{Z}[z]$ introduces $\log H(\widetilde{A}_n) \sim 6n^2 \log n$ (reaching $4665.84$ at $n = 25$).

---

## S. Padé Irrationality Kill Test

Certified 128-bit Acb evaluations of the $[n/n]$ multipoint Padé family at $\alpha_1 = \frac{1}{4} + i\frac{\gamma_1}{2}$:

| $n$ | $d_A$ | Rank / Nullity | $-\log\left|\frac{A_n(\alpha_1)}{B_n(\alpha_1)}\right|$ | $\mathcal{I}_n(A_n^{(B(0)=1)})$ | $\mathcal{I}_n(A_n^{(\mathrm{monic})})$ | $\log H(\widetilde{A}_n)$ | $-\log|\widetilde{A}_n(\alpha_1)|$ | $\mathcal{I}_n(\widetilde{A}_n) = \frac{-\log|\widetilde{A}_n(\alpha_1)|}{d_A}$ |
|---|---|---|---|---|---|---|---|---|
| $2$ | $2$ | $5 / 1$ | $+2.9933$ | $-0.3297$ | $-0.4465$ | $11.7761$ | $-13.1286$ | $-6.5643$ |
| $5$ | $5$ | $11 / 1$ | $+6.7615$ | $-0.0792$ | $-0.5960$ | $106.4247$ | $-107.5141$ | $-21.5028$ |
| $10$ | $10$ | $21 / 1$ | $+11.2313$ | $+0.0083$ | $-0.9195$ | $547.0894$ | $-547.6991$ | $-54.7699$ |
| $15$ | $15$ | $31 / 1$ | $+14.8525$ | $+0.0208$ | $-1.1995$ | $1426.4507$ | $-1426.8312$ | $-95.1221$ |
| $20$ | $20$ | $41 / 1$ | $+18.2598$ | $+0.0219$ | $-1.4235$ | $2780.3965$ | $-2780.6517$ | $-139.0326$ |
| $25$ | $25$ | $51 / 1$ | $+21.5988$ | $+0.0206$ | $-1.6077$ | $4665.8428$ | $-4666.0200$ | $-186.6408$ |

For $[n/(n-1)]$ at $n = 25$, $\mathcal{I}_{25}(\widetilde{A}_{25}) = -176.9193$; for $[(n-1)/n]$ at $n = 25$, $\mathcal{I}_{25}(\widetilde{A}_{24}) = -186.3569$.
Thus multipoint Padé passes Gate Z2 (`MULTIPOINT_PADE_ARGUMENT_POLYNOMIALIZATION_PROVED`) but fails Gate Z5 (`MULTIPOINT_PADE_ARGUMENT_POLYNOMIALIZATION_PROVED_BUT_FAILS_GATE_Z5_INTEGER_SMALLNESS`).

---

## T. Positive Rational Hankel Determinant

Turning to **Route C**, let $D_n := \det(b_{i+j})_{0 \le i,j < n}$ be the Hankel determinant of the positive rational moment sequence $b_j = \pi^{-2(j+1)}\zeta(2j+2) = \sum_{k=1}^\infty q_k^{j+1}$.
By Lambert's continued fraction for $\tan\sqrt{t}$, the generating function $B(t) = \frac{1 - \sqrt{t}\cot\sqrt{t}}{2t}$ has the exact Stieltjes continued fraction (S-fraction):
$$
\boxed{
B(t) = \cfrac{c_0}{1 - \cfrac{c_1 t}{1 - \cfrac{c_2 t}{1 - \ddots}}}, \qquad c_0 = \frac{1}{6}, \quad c_k = \frac{1}{(2k+1)(2k+3)} \quad (k \ge 1).
}
$$
By Stieltjes's determinant theorem (1894), the Hankel determinant $D_n^{(\pi)} = \det(b_{i+j}^{(\pi)})_{0 \le i,j < n}$ equals:
$$
\boxed{
D_n^{(\pi)} = c_0^n c_1^{n-1} c_2^{n-2}\cdots c_{n-1}^1 = 6^{-n}\prod_{j=1}^{n-1}\bigl[(4j-1)(4j+1)^2(4j+3)\bigr]^{-(n-j)} = 4^{n^2} D_n^{(\tau)} \in \mathbb{Q}_{>0}.
}
$$
**Remarkable Exact Arithmetic Property**: Every $D_n^{(\pi)}$ and $D_n^{(\tau)}$ is an **exact unit fraction** ($\operatorname{num}(D_n^{(\pi)}) = \operatorname{num}(D_n^{(\tau)}) = 1$ for all $n \ge 1$, with $D_1^{(\pi)} = 1/6, D_1^{(\tau)} = 1/24$ and $D_2^{(\pi)} = 1/18900, D_2^{(\tau)} = 1/4838400$)!

| $n$ | Exact $D_n^{(\pi)} = \det(b_{i+j}^{(\pi)})_{0 \le i,j < n}$ | $\operatorname{num}(D_n^{(\pi)})$ | $-\log D_n^{(\pi)} = \log\operatorname{den}(D_n^{(\pi)})$ | $\frac{-\log D_n^{(\pi)}}{n^2 \log(n+1)}$ |
|---|---|---|---|---|
| $1$ | $1/6$ | $1$ | $1.791759$ | $2.584963$ |
| $2$ | $1/18900$ | $1$ | $9.846917$ | $2.240763$ |
| $3$ | $1/371319795000$ | $1$ | $26.640330$ | $2.135215$ |
| $4$ | $1/203425339131180416250000$ | $1$ | $53.669586$ | $2.084174$ |
| $5$ | $1 / \operatorname{den}(D_5)$ | $1$ | $92.017758$ | $2.054244$ |
| $6$ | $1 / \operatorname{den}(D_6)$ | $1$ | $142.534909$ | $2.034679$ |
| $8$ | $1 / \operatorname{den}(D_8)$ | $1$ | $282.771791$ | $2.010859$ |
| $10$ | $1 / \operatorname{den}(D_{10})$ | $1$ | $478.878535$ | $1.997079$ |
| $12$ | $1 / \operatorname{den}(D_{12})$ | $1$ | $734.354509$ | $1.988220$ |
| $15$ | $1 / \operatorname{den}(D_{15})$ | $1$ | $1235.032779$ | $1.979751$ |

---

## U. Andréief/Vandermonde Determinant Decay

By the discrete Andréief / Cauchy–Binet identity applied to $\mu = \sum_{k=1}^\infty q_k \delta_{q_k}$:
$$
\boxed{
D_n = \det(b_{i+j})_{0 \le i,j < n} = \sum_{1 \le k_1 < k_2 < \dots < k_n} \left(\prod_{r=1}^n q_{k_r}\right) \prod_{1 \le a < b \le n} (q_{k_a} - q_{k_b})^2 > 0.
}
$$
We verify numerically on finite $M$-term truncations ($n = 3, M = 10$, error $2.15 \times 10^{-11}$) that the sum of Vandermonde squares reproduces $\det(b_{i+j}^{(M)})$ to machine precision.
From the closed product formula for $D_n^{(c)} = c^{n^2} D_n^{(\tau)}$, Stirling's approximation gives the exact super-quadratic decay ([TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md) §J):
$$
\boxed{
-\log D_n^{(\pi)} = 2n^2 \log n + (4\log 2 - 3)n^2 + O(n\log n), \qquad -\log D_n^{(\tau)} = 2n^2 \log n + (6\log 2 - 3)n^2 + O(n\log n).
}
$$
However, because $D_n^{(c)} = 1/\operatorname{den}(D_n^{(c)})$ is a unit fraction for both $c = 4$ and $c = 1$, clearing denominators yields $\operatorname{den}(D_n^{(c)})\cdot D_n^{(c)} = 1$, which has **zero** net decay margin and does not depend on the zero argument $\alpha_1$.

---

## V. Argument-Coupling Attempts

We tested all three candidate mechanisms for coupling the zero argument $X = \alpha_1$ or $X = \gamma_1$ polynomially into the Route C Hankel determinant:

1. **Candidate C1 — Divided-Difference Resolvent**:
   $$
   r_m(X) := \frac{\mathcal{R}_c(m) - \mathcal{R}_c(X)}{m - X}.
   $$
   At $X = \alpha_1$, $\mathcal{R}_c(\alpha_1) = 0$, so $r_m(\alpha_1) = \frac{a_m^{(c)}}{m - \alpha_1}$. Forming the $n \times n$ Hankel matrix $H_{i,j}^{\mathrm{C1}}(X) = \frac{a_{i+j}^{(c)}}{i+j-X}$ and clearing the exact minimal common denominator $\Phi_n(X) := \prod_{m=0}^{2n-2}(m - X)^{\min(m+1, 2n-1-m)}$ (whose total degree is $\sum_{m=0}^{2n-2}\min(m+1, 2n-1-m) = n^2$) produces a polynomial $P_n^{\mathrm{C1}}(X) := \Phi_n(X)\det H_n^{\mathrm{C1}}(X) \in \mathbb{Q}[X]$ of exact degree $\deg P_n^{\mathrm{C1}} = \sum_{m=1}^{2n-1}\min(m, 2n-m) = n^2$. However, dropping $\mathcal{R}_c(X)$ means the matrix entries $\frac{a_m^{(c)}}{m - X}$ no longer encode $\mathcal{R}_c(\alpha_1) = 0$: at $X = \alpha_1$, $P_n^{\mathrm{C1}}(\alpha_1)$ has no zero-induced cancellation (`-\log|P_n^{\mathrm{C1}}(\alpha_1)| < 0` for $n \le 6$), while clearing the rational denominators of $a_m^{(c)}$ adds $\log\operatorname{den} \sim 2n^2\log n$.
2. **Candidate C2 — Conjugate-Paired Real Resolvent for the Ordinate**:
   Pairing $(m - \alpha(Y))(m - \overline{\alpha(Y)}) = (m - 1/4)^2 + Y^2/4$ produces rational functions of $Y^2$. However, under the discrete measure $\mu_c = \sum_{k=1}^\infty q_{k,c} \delta_{q_{k,c}}$, the integer index $m$ appears in the **exponent** of the moments $b_{m-1}^{(c)} = \int u^{m-1}\,d\mu_c(u)$, whereas in Fauzan's $\zeta(5)$ Hermite identity the summation index $j$ appears in the **denominator** $\int \frac{w(y)}{y^2 + j^2}\,dy$. Turning $\mathcal{R}_c(\alpha(Y)) = 0$ into a moment identity for $\mu_c$ inserts $q_{k,c}^{\alpha(Y)} = c^{\alpha(Y)}(\tau k)^{-1/2 - iY}$, which is an **exponential Dirichlet polynomial** in $Y$, not an algebraic polynomial in $\mathbb{Q}[Y]$.
3. **Candidate C3 — Interpolation/Hankel Hybrid (Padé Hankel Determinants)**:
   By Hadamard's theorem, the Hankel determinants $H_n^{(k)}(z)$ of the sequence $a_m^{(c)}$ are exact scalar multiples of the multipoint Padé denominators/numerators audited in Route B, and therefore inherit Route B's exact failure at Gate Z5 ($\mathcal{I}_{25}(\widetilde{A}_{25}^{(\pi)}) = -186.64 < 0$ and $\mathcal{I}_{25}(\widetilde{A}_{25}^{(\tau)}) = -179.96 < 0$).

Classification: **`FAUZAN_HANKEL_ARGUMENT_TRANSFER_BLOCKED_BY_TARGET_COUPLING_AND_FACTORIAL_MOMENT_DENOMINATORS`**.

---

## W. Algebraicity/Transcendence Extension

Because the irrationality architecture terminated at Gate Z5, the secondary transcendence target ($\rho_1 \notin \overline{\mathbb{Q}}$ or $\gamma_1 \notin \overline{\mathbb{Q}}$) is not entered beyond recording the exact Liouville–Mahler lower bound criterion:
For $\alpha \in \overline{\mathbb{Q}}$ of degree $D = [\mathbb{Q}(\alpha):\mathbb{Q}]$ and Mahler measure $M(\alpha)$, and any $P_n \in \mathbb{Z}[X]$ of degree $d_n$ and height $H(P_n)$ with $P_n(\alpha) \ne 0$ (Waldschmidt 2000, Lemma 3.14):
$$
|P_n(\alpha)| \ge (d_n + 1)^{-(D-1)} H(P_n)^{-(D-1)} M(\alpha)^{-d_n},
$$
requiring $-\log|P_n(\alpha)| > (D-1)\log H(P_n) + d_n\log M(\alpha) + (D-1)\log(d_n + 1)$.

---

## X. Literature Theorem Table

| Theorem | Hypotheses | Our Object | Hypotheses Verified? | Evidence Class |
|---|---|---|---|---|
| Euler's Even-Zeta Formula (Euler 1740; Titchmarsh 1986 §2.4) | $m \in \mathbb{Z}_{\ge 1}$ | $a_m^{(c)} = \mathcal{R}_c(m) = (-1)^{m+1}\frac{(2m-1)c^m B_{2m}}{2(2m)!}$ ($c=4$ for $\pi$, $c=1$ for $\tau$) | Yes (verified symbolically and exactly for $0 \le m \le 200$) | `PROVED` |
| Direct Newton Series Convergence & Identity Without Carlson ([TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md) §K) | $0 < c < \tau^2$, $|\Delta^n a_0^{(c)}| = O(n^{1/2}\exp(-\kappa(c)n^{1/3}))$, subtracted Dirichlet-binomial Fubini on $\operatorname{Re}(z) > 1/2$ + open-set identity theorem | $\mathcal{R}_c(z) = \sum_{k=0}^\infty (\Delta^k a_0^{(c)})\binom{z}{k}$ with $\kappa(c) = \frac{3}{2^{5/3}}c^{1/3}$ ($\kappa(4) = 3/2, \kappa(1) = 3/2^{5/3}$) | Yes (proved directly on $\operatorname{Re}(z) > 1/2$ and extended to $\mathbb{C}$ without Carlson) | `PROVED` |
| Nörlund–Rice Integral Representation (Nörlund 1924; Flajolet–Sedgewick 1995) | Analytic continuation of sample function across contour enclosing $\{0, \dots, n\}$ | $R_n^{(c)}(z) = \mathcal{R}_c(z) - N_n^{(c)}(z)$ and $\Delta^n a_0^{(c)} = \frac{1}{2\pi i}\oint_{|w|=r} C_c(w)w^{-n-1}\,dw$ | Yes ($\mathcal{R}_c(w)$ is entire on $\mathbb{C}$ and $C_c(w)$ is analytic on $|w|<1$) | `PROVED` |
| Hausdorff / Stieltjes Moment Positivity & Hankel Determinants (Stieltjes 1894; Widder 1941) | Nonnegative measure $\mu_c$ on $[0, c/\tau^2]$ with infinite support | $b_j^{(c)} = \int_0^1 u^j\,d\mu_c(u) = \sum_{k=1}^\infty q_{k,c}^{j+1}$, $D_n^{(c)} = \det(b_{i+j}^{(c)})_{0 \le i,j < n} > 0$ | Yes (verified via Lambert S-fraction and discrete Andréief identity) | `PROVED` |
| Lambert–Stieltjes Continued Fraction Determinant Identity (Lambert 1768; Wall 1948) | S-fraction $B_c(t) = \cfrac{c_0^{(c)}}{1 - \cfrac{c_1^{(c)} t}{1 - \cdots}}$ with $c_k^{(c)} > 0$ | $c_0^{(c)} = c/24, \; c_k^{(c)} = \frac{c}{4(2k+1)(2k+3)}$ | Yes (gives exact unit-fraction formula for $D_n^{(\pi)}$ and $D_n^{(\tau)}$ for all $n \ge 1$) | `PROVED` |
| Von Staudt–Clausen Theorem (1840) | $B_{2m}$ for $m \ge 1$ | Denominators of $a_m^{(c)}$ and $b_{m-1}^{(c)}$ combine $(2m)!$ with $\prod_{(p-1)\mid 2m} p$ | Yes (verified on $0 \le m \le 200$) | `PROVED` |
| Integer-Polynomial Superlinear Irrationality Schema | $P_n \in \mathbb{Z}[X]$, $\deg P_n = d_n \ge 1$, $P_n(\alpha) \ne 0$, $-\log|P_n(\alpha)| / d_n \to +\infty$ | Applied to $\widetilde{N}_n^{(c)}, G_n^{(c)}, \widetilde{A}_n^{(c)}$ | Schema proved in Lean 4 (`superlinear_log_smallness_irrationality_schema`), and two-step lower envelope proves Z5 failure in Newton class | `PROVED_CONDITIONAL` |
| Liouville–Mahler Algebraic Approximation Lower Bound (Waldschmidt 2000, Lemma 3.14) | $\alpha \in \overline{\mathbb{Q}}$ of degree $D$, $P_n \in \mathbb{Z}[X]$, $P_n(\alpha) \ne 0$ | Secondary transcendence target $\alpha_1 \in \overline{\mathbb{Q}}$ | Recorded for completeness; not reached because irrationality terminated at Gate Z5 | `PROVED_CONDITIONAL` |

---

## Y. Earliest Failed Gate

$$
\boxed{
\texttt{EARLIEST\_FAILED\_GATE} = \texttt{Z5}
\quad
(\texttt{Z5\_SUPERLINEAR\_LOG\_SMALLNESS\_FAILED\_IN\_TESTED\_NEWTON\_PADE\_HANKEL\_CLASSES}).
}
$$

- **Gates Z1, Z2, Z3, and Z4 succeed**:
  - **Z1**: $\mathcal{R}_c(z) = (2z-1)c^z\tau^{-2z}\zeta(2z)$ ($c=4$ for $\mathcal{R}_\pi$, $c=1$ for $\mathcal{R}_\tau$) is entire, vanishes at $\alpha_1 = \rho_1/2$, and takes strictly positive rational values $a_m^{(c)} \in \mathbb{Q}_{>0}$ at all $m \in \mathbb{Z}_{\ge 0}$.
  - **Z2**: Both Newton interpolation $N_n^{(c)}(z) \in \mathbb{Q}[z]$ and multipoint Padé numerators $A_n^{(c)}(z) \in \mathbb{Q}[z]$ (plus the real ordinate norm polynomials $\mathcal{N}_P(Y) \in \mathbb{Q}[Y]$) are zero-independent polynomials in the zero argument.
  - **Z3**: The two-approximant norm sum $G_n^{(c)}(Y) = C_n(|N_n^{(c)}(\alpha(Y))|^2 + |N_{n+1}^{(c)}(\alpha(Y))|^2) \in \mathbb{Z}[Y]$ is strictly positive on all of $\mathbb{R}$ for the infinite cofinal set of $n$ with $\Delta^{n+1}a_0^{(c)} \ne 0$.
  - **Z4**: Exact degree and denominator/height growth are quantified ($\log L_n^{(c)} = 3n\log n + O(n)$ for Newton; $\log H(\widetilde{A}_n^{(c)}) \sim 6n^2\log n$ for $[n/n]$ Padé; $\log\operatorname{den}(D_n^{(c)}) = 2n^2\log n + O(n^2)$ for Hankel).
- **Gate Z5 fails across all three tested routes (repaired and audited in `TASK-TC-039R`, [TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md](file:///c:/Development/Projects/reimann_scope/docs/reviews/TC_039R_PI_TAU_ASYMPTOTIC_REPAIR.md))**:
  - **Route A (Newton)**: Exact boundary cancellation of $\frac{d}{dx}\!\left[\frac{c}{\tau^2 x}(1 - \frac{c}{\tau^2 x^2})^n\right]$ at $x = \sqrt{c}/\tau$ and $x = \infty$ plus the two-approximant phase-separation lower envelope ($\Delta\theta = \pi/3$, $\sin^2(\pi/3) = 3/4 > 0$) proves $E_n^{(c)} = |N_n^{(c)}(\alpha_1)|^2 + |N_{n+1}^{(c)}(\alpha_1)|^2 = \Theta(e^{-2\kappa(c)n^{1/3}})$ ($\kappa_\pi = 3/2, \kappa_\tau = 3/2^{5/3}$), so $\mathcal{I}_n(\widetilde{N}_n^{(c)}) \sim -3\log n \to -\infty$ (`Z5_NEWTON_ROUTE_GENUINELY_FAILS_BY_TWO_STEP_LOWER_ENVELOPE_AND_FACTORIAL_DENOMINATORS`).
  - **Route B (Multipoint Padé)**: $|A_n^{(c)}(\alpha_1)/B_n^{(c)}(\alpha_1)|$ decays exponentially only because $|B_n^{(c)}(\alpha_1)| \asymp (2n)!$ grows factorially; the integer numerator polynomial alone satisfies $\mathcal{I}_{25}(\widetilde{A}_{25}^{(\pi)}) = -186.64 < 0$ and $\mathcal{I}_{25}(\widetilde{A}_{25}^{(\tau)}) = -179.96 < 0$ (`Z5_PADE_FINITE_WINDOW_NEGATIVE_ASYMPTOTIC_OPEN`).
  - **Route C (Hankel Determinant)**: $D_n^{(\pi)} = 4^{n^2}D_n^{(\tau)} \in \mathbb{Q}_{>0}$ are exact unit fractions with $-\log D_n^{(\pi)} = 2n^2\log n + (4\log 2 - 3)n^2 + O(n\log n)$, and coupling the zero argument $X = \alpha_1$ via C1 ($\deg P_n^{\mathrm{C1}} = n^2$)/C2/C3 either loses zero cancellation, requires non-polynomial $q_{k,c}^X$, or reduces to Route B (`Z5_HANKEL_ROUTE_BLOCKED_BY_UNIT_FRACTION_CANCELLATION_AND_TARGET_COUPLING`).

---

## Z. Principal Classification and Exact Next Theorem

### Principal Classification

$$
\boxed{
\begin{gathered}
\texttt{RATIONALIZED\_XI\_RATIONAL\_INTEGER\_SAMPLING\_PROVED} \\
\texttt{TAU\_NORMALIZATION\_EXPOSES\_EVEN\_ZETA\_RATIONAL\_CORE} \\
\texttt{NEWTON\_SERIES\_IDENTITY\_FOR\_RATIONALIZED\_XI\_PROVED\_WITHOUT\_CARLSON} \\
\texttt{Z5\_NEWTON\_ROUTE\_GENUINELY\_FAILS\_BY\_TWO\_STEP\_LOWER\_ENVELOPE\_AND\_FACTORIAL\_DENOMINATORS} \\
\texttt{Z5\_PADE\_FINITE\_WINDOW\_NEGATIVE\_ASYMPTOTIC\_OPEN} \\
\texttt{Z5\_HANKEL\_ROUTE\_BLOCKED\_BY\_UNIT\_FRACTION\_CANCELLATION\_AND\_TARGET\_COUPLING} \\
\texttt{PI\_AND\_TAU\_BELONG\_TO\_ONE\_EXPONENTIAL\_GAUGE\_FAMILY\_NO\_FIXED\_GAUGE\_SAVES\_Z5}
\end{gathered}
}
$$

### Subgate & Obligation Status

- **`SUBGATE-TC-039A`**: `REPAIRED_NEWTON_HANKEL_CLOSED_AT_Z5_PADE_ASYMPTOTIC_DELIMITER_EXPLICIT`
- **`SUBGATE-TC-038A`**: `OPEN` (`ZERO_SUM_CONSTANT_ARITHMETIC_SUBGATE`)
- **`SUBGATE-TC-040A` (Exact Next Subgate)**: `NON_FACTORIAL_ARITHMETIC_ARGUMENT_OPERATOR_OR_ZERO_SUM_INDEPENDENCE_SUBGATE` (`OPEN`):
  > Either (i) prove irrationality / $\mathbb{Q}$-linear independence of the exact global symmetric zero-sum invariants $2\lambda_1 = 2 + \gamma_E - \log(4\pi)$ and $S_2 = 1 + \gamma_E^2 - \pi^2/8 + 2\gamma_1^{\mathrm{St}}$ (`SUBGATE-TC-038A`), or (ii) construct an arithmetic zero-argument operator whose rational evaluations avoid the $(2m)!$ Euler–Bernoulli factorial denominators that force $\log L_n = \Theta(n\log n)$ in Newton interpolation and $\log\operatorname{den}(D_n) = \Theta(n^2\log n)$ in even-zeta Hankel determinants.
- **`OBL-CT-001A`**: `OPEN`
- **`rh_claimed`**: `False`

