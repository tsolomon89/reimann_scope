# TASK-TC-056: Prime-Chain Contraction, Uniform Total Contraction Bound, and Signed Mixed-Prime Energy Analysis

- **Task ID**: `TASK-TC-056`
- **Parent Epic**: `EPIC-TC-042` (`SUBGATE-TC-043A`)
- **Reviewed Baseline (`TC-055R2`)**:
  - Merged `main` (`TC-054R2` merge): `8a898c60b7c4cb56543a3d1e7960c39e00027c22`
  - Reviewed `TC-055R2` implementation: `10f4f51246818e9d914113771ae906643dae9fa9`
  - Reviewed `TC-055R2` tip: `9a3755d977518ca6f0f1fb7ed3386e6a4a97d3ea`
- **Branch**: `task/tc-056-prime-chain-contraction-and-mixed-prime-energy`
- **Gate & Proof Status**: `SUBGATE-TC-043A: OPEN`, `rh_proved: false`
- **Primary Implementation, Formalization & Artifact**:
  - Python Arb generator & verifier: [`tc/prime_chain_contraction.py`](../../tc/prime_chain_contraction.py) (reusing [`tc/liouville_square_dilation.py`](../../tc/liouville_square_dilation.py))
  - Lean 4 formalization: [`formal/RiemannScope/LiouvilleSquareDilation.lean`](../../formal/RiemannScope/LiouvilleSquareDilation.lean) (Theorems 17–20; 20 compiled public theorems total, `0 sorry`, `0` custom `axiom`)
  - Certified 256-bit Arb artifact: [`data/tc_prime_chain_contraction.json`](../../data/tc_prime_chain_contraction.json)
  - Test suite & negative controls: [`tests/test_tc_prime_chain_contraction.py`](../../tests/test_tc_prime_chain_contraction.py)

---

## 1. Baseline Conventions, Circle Constant $\tau$, and Schedule Scope

Throughout this derivation and all associated code and artifacts:

1. **Circle Constant and Coordinates**: $\tau$ denotes the **sole** circle constant (one full turn in radians). Complex arguments are written $z = a + i b$ with real coordinates $a, b \in \mathbb{R}$, and nontrivial zeta zeros are written $\rho = x + i y$ with $x, y \in \mathbb{R}$.
2. **Admissible $\tau$-Grades vs. Auxiliary Arithmetic Scales**: Transcendental Continuation (TC) grades $K$ belong to the real algebraic numbers $\mathbb{A}_{\mathbb{R}}$, including negative real algebraic grades. Auxiliary prime-power scales $p^k$ and dyadic block cutoffs $2^j$ used below index finite arithmetic decompositions on $(0, \infty)$; they do **not** automatically define admissible algebraic $\tau$-grade shifts ($p^k = \tau^K$ with $K \in \mathbb{A}_{\mathbb{R}} \setminus \{0\}$ is impossible by Lindemann–Weierstrass / Gelfond–Schneider).
3. **Finite Gaussian Observable and Weighted Energy**: For $X > 0$ and integer $T \ge 0$,
   $$\varphi_n(X) := X^{5/2} n^{-3} \exp\!\left(-\frac{X^2}{n^2}\right) \quad (n \ge 1), \qquad Q_T(X) := \sum_{1 \le n \le T} \lambda(n)\varphi_n(X),$$
   and for $Y > 0$ and integers $m, n \ge 1$,
   $$K_Y(m, n) := \int_Y^{\tau Y} \varphi_m(X)\varphi_n(X)\,\frac{dX}{X}, \qquad E_T(Y) := \int_Y^{\tau Y} Q_T(X)^2\,\frac{dX}{X}, \qquad D_T(Y) := \sum_{1 \le n \le T} K_Y(n, n)$$
   (with empty sums equal to $0$ when $T = 0$).
4. **Exact Truncation Schedule and Two-Way $L^2$ Tail Transfer**: In the research estimates for $Y \ge 1$, we use the exact schedule
   $$T(Y) := \lceil Y^{5/4} \rceil \qquad (T(1) = 1),$$
   computed by exact integer arithmetic (`(T - 1)^4 < Y^5 <= T^4` on rational/integer inputs, rejecting binary `float`) and kept distinct from the companion prime-sieve schedule $M(Y) := \lceil \max(2, Y^{5/4}) \rceil$ ($M(1) = 2$). For $Q_\lambda(X) := \sum_{n \ge 1} \lambda(n)\varphi_n(X)$ and $E_\lambda(Y) := \int_Y^{\tau Y} Q_\lambda(X)^2\,\frac{dX}{X}$, the truncation-energy remainder $\mathcal{R}_{\mathrm{tail}}(Y, T) := \int_Y^{\tau Y} |Q_\lambda(X) - Q_T(X)|^2\,\frac{dX}{X}$ satisfies (`TC-055R2` §4)
   $$\mathcal{R}_{\mathrm{tail}}(Y, T) \le \frac{(\tau^5 - 1)Y^5}{20 T^4}, \qquad \mathcal{R}_{\mathrm{tail}}(Y, T(Y)) \le \frac{\tau^5 - 1}{20} \in [489.5814956564503252203860960694969703685 \pm 2.00 \times 10^{-38}] \quad (Y \ge 1),$$ <!-- tc-enclosure: observable="uniform_cap_tau5_minus_1_over_20" params="precision_bits=256" json_path="section_1_and_2_baseline_and_cleanup.truncation_energy_and_two_way_L2_transfer.uniform_cap_tau5_minus_1_over_20" -->
   together with both directions of the $L^2([Y, \tau Y], dX/X)$ triangle-inequality transfer:
   $$E_\lambda(Y) \le 2 E_T(Y) + 2 \mathcal{R}_{\mathrm{tail}}(Y, T), \qquad E_T(Y) \le 2 E_\lambda(Y) + 2 \mathcal{R}_{\mathrm{tail}}(Y, T).$$

---

## 2. Completion of the Five `TC-055R2` Mathematical Cleanups

### 2.1 Explicit Finite Set of Primes $P$
Every smooth/coprime factorization and grouped-fiber theorem in Lean (`formal/RiemannScope/LiouvilleSquareDilation.lean`) and Python (`tc/liouville_square_dilation.py`, `tc/prime_chain_contraction.py`) takes an explicit finite set of primes $P$ (`P : Finset ℕ` with hypothesis `hP : ∀ p ∈ P, Nat.Prime p`, including $P = \varnothing$ where $N_\varnothing = \prod_{p \in \varnothing} p = 1$ and $\mathcal{S}(\varnothing) = \{1\}$). In Python, `validate_prime_set_tuple(primes_P)` rejects non-integers, booleans, non-primes, and duplicate primes.

### 2.2 Exact Uncoupled Cutoff Excess Witness $w(6)$ at $(P = \{2\}, T = 3)$
Comparing the uncoupled product sum $\sum_{m \in \mathcal{S}(P),\, m \le T}\sum_{1 \le r \le T,\, \gcd(r, N_P)=1} \lambda(m)\lambda(r) w(m r)$ against the true coupled finite sum $\sum_{1 \le n \le T} \lambda(n) w(n)$ at $P = \{2\}$, $T = 3$:
- The $2$-smooth integers $\le 3$ are $m \in \{1, 2\}$, and the odd integers $\le 3$ are $r \in \{1, 3\}$.
- Only $(m, r) = (2, 3)$ violates $m r \le 3$, contributing $\lambda(2)\lambda(3) w(6) = (-1)(-1) w(6) = w(6)$.
Thus the exact uncoupled excess at $(P = \{2\}, T = 3)$ is $w(6)$, which is nonzero **if and only if** $w(6) \ne 0$. In particular, for the concrete positive Gaussian observable $w(n) = \varphi_n(X)$ ($X > 0$), $\varphi_6(X) > 0$; at $X = 4$,
$$\varphi_6(4) \in [0.09498968717480808625948451542684510853395 \pm 3.00 \times 10^{-42}].$$ <!-- tc-enclosure: observable="phi_6_at_X_4" params="precision_bits=256" json_path="section_1_and_2_baseline_and_cleanup.uncoupled_excess_w6_witness_P2_T3.phi_6_at_X_4" -->

### 2.3 Necessary vs. Sufficient Admissible Polylogarithmic Cutoff Scales $u(Y)$
In the smooth/rough split at prime cutoff $u = u(Y) \ge 3$ with fixed $\eta \in (0, 1)$, the smooth prime Euler factor grows as $\exp\!\left(O_\eta\!\left(\frac{u^{1-\eta}}{\log u}\right)\right)$, requiring $\frac{u(Y)^{1-\eta}}{(1-\eta)\log u(Y)} \le \varepsilon \log Y$ (or $o(\log Y)$) for $Y^\varepsilon$ compatibility:
- **Sufficient (strictly smaller) scale**: $u(Y) \ll (\log Y)^{1/(1-\eta)}$ gives $\frac{u(Y)^{1-\eta}}{\log u(Y)} \ll_\eta \frac{\log Y}{\log\log Y} = o(\log Y)$, which is sufficient for *every* $\varepsilon > 0$ simultaneously, **not** necessary.
- **Sharp admissible scale**: For fixed $\eta \in (0, 1)$ and $\varepsilon > 0$, set
  $$u(Y) := c\,(\log Y \log\log Y)^{1/(1-\eta)} \qquad (Y \ge e^e).$$
  Then $(1 - \eta)\log u(Y) = (1 - \eta)\log c + \log\log Y + \log\log\log Y = (1 + o_{\eta, c}(1))\log\log Y$, whence
  $$\frac{u(Y)^{1-\eta}}{(1 - \eta)\log u(Y)} = \frac{c^{1-\eta}\,\log Y \log\log Y}{(1 + o_{\eta, c}(1))\log\log Y} = c^{1-\eta}(1 + o_{\eta, c}(1))\log Y.$$
  Consequently, $u(Y) = c\,(\log Y \log\log Y)^{1/(1-\eta)}$ is **admissible** whenever $0 < c < \varepsilon^{1/(1-\eta)}$ (so $c^{1-\eta} < \varepsilon$), and **necessary** in the asymptotic order $u(Y) = O_{\eta, \varepsilon}\!\left((\log Y \log\log Y)^{1/(1-\eta)}\right)$ (specifically $\limsup_{Y \to \infty} u(Y) / (\log Y \log\log Y)^{1/(1-\eta)} \le \varepsilon^{1/(1-\eta)}$). At $\eta = 1/2, \varepsilon = 1/4, c = 1/32, \log Y = 1000$:
  $$\frac{\sqrt{u(Y)}}{(1 - \eta)\log u(Y)\,\log Y} \in [0.1718078989402312469669704074210509615688 \pm 1.00 \times 10^{-41}] < \frac{1}{4}.$$ <!-- tc-enclosure: observable="sample_eta_half_eps_quarter_c_1_over_32_logY_1000_ratio" params="precision_bits=256" json_path="section_1_and_2_baseline_and_cleanup.admissible_polylogarithmic_scale_correction.sample_eta_half_eps_quarter_c_1_over_32_logY_1000_ratio" -->

### 2.4 Complete Dominated & Bounded Convergence Proof of Finite-$S$ Leading Asymptotics
Let $S$ be any finite set of primes and let $a_S(n) := (-1)^{\sum_{p \in S} v_p(n)}$ be the completely multiplicative $S$-parity weight ($a_S(p) = -1$ for $p \in S$, $a_S(q) = +1$ for $q \notin S$).

**Proposition 2.1 (Finite-$S$ Pointwise and Energy Leading Asymptotics).** *Define $b_S := \mu * a_S$, where $\mu$ is the Möbius function. Then:*
1. *$a_S = \mathbf{1} * b_S$, $b_S$ is multiplicative and supported on the $S$-smooth integers $\mathcal{S}(S)$, with $b_S(1) = 1$, $b_S(p^k) = 2(-1)^k$ for $p \in S, k \ge 1$, and $b_S(q^k) = 0$ for $q \notin S, k \ge 1$.*
2. *The Dirichlet series $\sum_{d \ge 1} \frac{b_S(d)}{d}$ converges absolutely:*
   $$A_S := \sum_{d \ge 1} \frac{|b_S(d)|}{d} = \prod_{p \in S}\left(1 + \sum_{k \ge 1}\frac{2}{p^k}\right) = \prod_{p \in S}\frac{p + 1}{p - 1} < \infty, \qquad m_S := \sum_{d \ge 1} \frac{b_S(d)}{d} = \prod_{p \in S}\left(1 + \sum_{k \ge 1}\frac{2(-1)^k}{p^k}\right) = \prod_{p \in S}\frac{p - 1}{p + 1} > 0.$$
3. *For the unweighted series $Q_{\mathbf{1}}(w) := \sum_{n \ge 1} \varphi_n(w)$ ($w > 0$), we have the global uniform majorant across **all** $w > 0$:*
   $$\sup_{w > 0} \frac{Q_{\mathbf{1}}(w)}{\sqrt{w}} \le M_{\mathbf{1}} := \frac{1}{2} + C_{1,\mathrm{uni}} = \frac{1}{2} + 2\left(\frac{3}{2 e}\right)^{3/2} \in [1.319832557883720076781582020759507823709 \pm 2.00 \times 10^{-40}],$$ <!-- tc-enclosure: observable="M_1" params="precision_bits=256" json_path="section_1_and_2_baseline_and_cleanup.finite_S_global_uniform_majorant_M1.M_1" -->
   *with $M_{\mathbf{1}} - \zeta(3) \in [0.1177756547241257913818438592480578329438 \pm 4.00 \times 10^{-41}] > 0$,* <!-- tc-enclosure: observable="M_1_minus_zeta_3" params="precision_bits=256" json_path="section_1_and_2_baseline_and_cleanup.finite_S_global_uniform_majorant_M1.M_1_minus_zeta_3" -->
   *and $\lim_{w \to \infty} \frac{Q_{\mathbf{1}}(w)}{\sqrt{w}} = \frac{1}{2}$.*
4. *Consequently, as $X \to \infty$ and $Y \to \infty$,*
   $$\lim_{X \to \infty} \frac{Q_{a_S}(X)}{\sqrt{X}} = \frac{m_S}{2}, \qquad \lim_{Y \to \infty} \frac{E_{a_S}(Y)}{Y} = \frac{\tau - 1}{4}\,m_S^2.$$

*Proof.* (1)–(2) By Möbius inversion, $a_S = \mathbf{1} * b_S$ with $b_S$ multiplicative because $a_S$ and $\mu$ are multiplicative. On prime powers, $b_S(p^k) = a_S(p^k) - a_S(p^{k-1})$ ($k \ge 1$). If $q \notin S$, $a_S(q^k) = 1$ for all $k \ge 0$, so $b_S(q^k) = 1 - 1 = 0$; if $p \in S$, $a_S(p^k) = (-1)^k$, so $b_S(p^k) = (-1)^k - (-1)^{k-1} = 2(-1)^k$. Since $S$ is finite, the finite Euler products for $\sum_d |b_S(d)|/d$ and $\sum_d b_S(d)/d$ converge absolutely to $A_S$ and $m_S$.

(3) Fix $w > 0$ and set $g_w(t) := w^{5/2} t^{-3} e^{-w^2/t^2}$ for $t > 0$, $g_w(0) := 0$. Substituting $u = w/t$ ($du = -w t^{-2} dt$) gives $\int_0^\infty g_w(t)\,dt = \sqrt{w}\int_0^\infty u\,e^{-u^2}\,du = \frac{1}{2}\sqrt{w}$. Moreover, $g_w'(t) = w^{5/2} t^{-6}(2 w^2 - 3 t^2)e^{-w^2/t^2}$ vanishes uniquely on $(0, \infty)$ at $t_* = w\sqrt{2/3}$, increasing from $0$ on $(0, t_*]$ to $\max_{t > 0} g_w(t) = g_w(t_*) = w^{-1/2}(3/(2e))^{3/2}$ and decreasing to $0$ on $[t_*, \infty)$. By first-order Euler–Maclaurin (`TC-054R` Lemma 2.1) applied on $[0, \infty)$,
$$\left|Q_{\mathbf{1}}(w) - \frac{1}{2}\sqrt{w}\right| = \left|\sum_{n \ge 1} g_w(n) - \int_0^\infty g_w(t)\,dt\right| \le \frac{1}{2}\int_0^\infty |g_w'(t)|\,dt = g_w(t_*) = \left(\frac{3}{2e}\right)^{3/2} w^{-1/2}.$$
For $w \ge 1$, $w^{-1} \le 1$ immediately gives $Q_{\mathbf{1}}(w)/\sqrt{w} \le \frac{1}{2} + (3/(2e))^{3/2} w^{-1} \le M_{\mathbf{1}}$ and $\lim_{w \to \infty} Q_{\mathbf{1}}(w)/\sqrt{w} = 1/2$; while for $0 < w < 1$, $Q_{\mathbf{1}}(w)/\sqrt{w} = w^2 \sum_{n \ge 1} n^{-3} e^{-w^2/n^2} \le \zeta(3) < M_{\mathbf{1}}$. Thus $0 < Q_{\mathbf{1}}(w)/\sqrt{w} \le M_{\mathbf{1}}$ holds globally for **every** $w > 0$.

(4) For every $X > 0$, $\sum_{d \in \mathcal{S}(S)} |b_S(d)| \sum_{k \ge 1} \varphi_{d k}(X) = \sqrt{X} \sum_{d \in \mathcal{S}(S)} \frac{|b_S(d)|}{d}\,\frac{Q_{\mathbf{1}}(X/d)}{\sqrt{X/d}} \le \sqrt{X}\,A_S M_{\mathbf{1}} < \infty$ (using $\varphi_{d k}(X) = d^{-1/2}\varphi_k(X/d)$). By Fubini's theorem,
$$\frac{Q_{a_S}(X)}{\sqrt{X}} = \sum_{d \in \mathcal{S}(S)} \frac{b_S(d)}{d}\,\frac{Q_{\mathbf{1}}(X/d)}{\sqrt{X/d}}.$$
Each term is dominated uniformly in $X > 0$ by $\frac{|b_S(d)|}{d} M_{\mathbf{1}}$ with $\sum_{d \in \mathcal{S}(S)} \frac{|b_S(d)|}{d} M_{\mathbf{1}} = A_S M_{\mathbf{1}} < \infty$, and for each fixed $d \in \mathcal{S}(S)$, $\lim_{X \to \infty} \frac{Q_{\mathbf{1}}(X/d)}{\sqrt{X/d}} = \frac{1}{2}$. By Dominated Convergence on $\ell^1(\mathcal{S}(S))$, $\lim_{X \to \infty} \frac{Q_{a_S}(X)}{\sqrt{X}} = \frac{1}{2}\sum_{d \in \mathcal{S}(S)}\frac{b_S(d)}{d} = \frac{m_S}{2}$. Next, setting $X = Y u$ ($u \in [1, \tau]$, $dX/X = du/u$),
$$\frac{E_{a_S}(Y)}{Y} = \int_1^\tau \left(\frac{Q_{a_S}(Y u)}{\sqrt{Y u}}\right)^2 du.$$
The integrand converges pointwise on $[1, \tau]$ to $(m_S/2)^2$ as $Y \to \infty$ and is uniformly bounded by $(A_S M_{\mathbf{1}})^2$ on $[1, \tau]$. By Bounded Convergence on $[1, \tau]$, $\lim_{Y \to \infty} \frac{E_{a_S}(Y)}{Y} = (\tau - 1)\frac{m_S^2}{4}$. (No unproved sharp $O(X^{-1/2})$ or $O(1)$ multi-prime error rate is claimed.) $\blacksquare$

### 2.5 Fixed-$P$ Smooth-Fiber Decay Is a Sparsity Bound, Not Signed Cancellation
For any finite prime set $P$, cutoff $L \ge 0$, and $0 \le \eta < 5/2$, writing $u = w / m > 0$ gives $w^{5/2} m^{-3} e^{-w^2/m^2} = w^\eta m^{-1/2-\eta} \cdot u^{5/2-\eta} e^{-u^2} \le c_\eta w^\eta m^{-1/2-\eta}$ where $c_\eta := \sup_{u > 0} u^{5/2-\eta} e^{-u^2} = \left(\frac{5 - 2\eta}{4 e}\right)^{(5 - 2\eta)/4}$ ($c_0 \in [0.3786774237973017179648688732911923409458 \pm 5.00 \times 10^{-41}]$, <!-- tc-enclosure: observable="c_0_sparsity" params="precision_bits=256" json_path="section_1_and_2_baseline_and_cleanup.fixed_P_smooth_fiber_sparsity_audit.c_0_sparsity" -->
$c_{1/4} \in [0.3706511019414340541102507060436134268255 \pm 5.00 \times 10^{-41}]$). <!-- tc-enclosure: observable="c_quarter_sparsity" params="precision_bits=256" json_path="section_1_and_2_baseline_and_cleanup.fixed_P_smooth_fiber_sparsity_audit.c_quarter_sparsity" -->
Therefore
$$|Q_{\lambda, \mathcal{S}(P), L}(w)| \le Q_{\mathbf{1}, \mathcal{S}(P), L}(w) \le c_\eta w^\eta \sum_{m \in \mathcal{S}(P)} m^{-1/2-\eta} = c_\eta w^\eta \prod_{p \in P}\left(1 - p^{-1/2-\eta}\right)^{-1}.$$
Because the identical upper bound holds for the unsigned all-$+1$ smooth sum $Q_{\mathbf{1}, \mathcal{S}(P), L}(w)$, fixed-$P$ smooth-fiber decay reflects multiplicative sparsity of $\mathcal{S}(P)$ and absolute convergence of $\sum_{m \in \mathcal{S}(P)} m^{-1/2-\eta}$, **not** Liouville sign cancellation.

---

## 3. Finite Prime Filtration and Exact Ascending-Prime Telescoping

Let $P$ be a finite set of primes, $N_P := \prod_{p \in P} p$, and $\mathcal{S}(P) := \{m \in \mathbb{Z}_{\ge 1} : q \mid m \implies q \in P\}$. For integer $T \ge 0$ and $1 \le r \le T$ with $\gcd(r, N_P) = 1$, define the actual cofactor fiber
$$F_{P, r}(X) := \sum_{\substack{m \in \mathcal{S}(P) \\ m r \le T}} \lambda(m r)\varphi_{m r}(X) = \frac{\lambda(r)}{\sqrt{r}}\,Q_{\lambda, \mathcal{S}(P), \lfloor T / r \rfloor}\!\left(\frac{X}{r}\right),$$
and the grouped squared-fiber energy
$$V_P(Y, T) := \sum_{\substack{1 \le r \le T \\ \gcd(r, N_P) = 1}} \int_Y^{\tau Y} F_{P, r}(X)^2\,\frac{dX}{X}.$$

> **Semantic Scope Note.** $V_P(Y, T)$ is strictly the finite sum of $L^2([Y, \tau Y], dX/X)$ squared norms of the grouped functions $F_{P, r}$. Because distinct grouped fibers $F_{P, r_1}, F_{P, r_2}$ have strictly positive inner products on $[Y, \tau Y]$ when unweighted and non-orthogonal inner products when weighted, $V_P$ is **never** called or treated as an orthogonal projection, conditional expectation, or martingale.

**Theorem 3.1 (Filtration Endpoints, Coupled Prime-Adjoining, and Telescoping; Formal Pointwise Core: `finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056`).** *For every $Y > 0$ and integer $T \ge 0$:*
1. **Endpoints**:
   $$V_\varnothing(Y, T) = D_T(Y), \qquad V_{\{\text{primes } \le T\}}(Y, T) = E_T(Y)$$
   *(and more generally $V_P(Y, T) = E_T(Y)$ whenever $P$ contains every prime $\le T$, since $\gcd(r, N_P) = 1$ with $1 \le r \le T$ then forces $r = 1$).*
2. **Coupled Prime-Adjoining Fiber Identity**: *For any prime $p \notin P$ and $1 \le s \le T$ with $\gcd(s, N_P p) = 1$,*
   $$F_{P \cup \{p\}, s}(X) = \sum_{\substack{k \ge 0 \\ s p^k \le T}} F_{P, s p^k}(X),$$
   *where every inner cutoff $\lfloor T / (s p^k) \rfloor$ remains coupled to $s p^k$.*
3. **Stepwise Energy Increment**: *For any prime $p \notin P$,*
   $$\Delta_{P, p}(Y, T) := V_{P \cup \{p\}}(Y, T) - V_P(Y, T) = 2 \sum_{\substack{1 \le s \le T \\ \gcd(s, N_P p) = 1}} \sum_{\substack{0 \le k < l \\ s p^l \le T}} \int_Y^{\tau Y} F_{P, s p^k}(X) F_{P, s p^l}(X)\,\frac{dX}{X}$$
   *(which vanishes identically whenever $p > T$, since $s \ge 1$ and $l \ge 1$ force $s p^l \ge p > T$).*
4. **Ascending-Prime Telescoping**: *Let $p_1 < p_2 < \dots < p_J \le T$ be all primes $\le T$ and $P_{j-1} := \{p_1, \dots, p_{j-1}\}$ ($P_0 = \varnothing$). Then*
   $$E_T(Y) = D_T(Y) + \sum_{j = 1}^J \Delta_{P_{j-1}, p_j}(Y, T).$$

*Proof.* Every pointwise identity holds for arbitrary weights at fixed $X > 0$ and is formally machine-checked in Lean Theorem 17 (`finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056`):
- When $P = \varnothing$, $N_\varnothing = 1$ and $\mathcal{S}(\varnothing) = \{1\}$, so for each $1 \le r \le T$, $F_{\varnothing, r}(X) = \lambda(r)\varphi_r(X)$ and $F_{\varnothing, r}(X)^2 = \varphi_r(X)^2$.
- When $P$ contains all primes $\le T$, any $1 \le r \le T$ with $\gcd(r, N_P) = 1$ has no prime divisor $\le T$, hence $r = 1$, leaving the single fiber $F_{P, 1}(X) = \sum_{1 \le m \le T} \lambda(m)\varphi_m(X) = Q_T(X)$.
- Every $m' \in \mathcal{S}(P \cup \{p\})$ factors uniquely as $m' = m p^k$ with $m \in \mathcal{S}(P)$ and $k = v_p(m') \ge 0$, and $m' s \le T \iff m (s p^k) \le T$ (which requires $s p^k \le T$ since $m \ge 1$). Grouping by $k$ yields (2).
- Similarly, every $1 \le r \le T$ with $\gcd(r, N_P) = 1$ factors uniquely as $r = s p^k$ with $\gcd(s, N_P p) = 1$, $k = v_p(r) \ge 0$, and $s p^k \le T$. Squaring $F_{P \cup \{p\}, s}(X) = \sum_{k: s p^k \le T} F_{P, s p^k}(X)$ gives $\sum_k F_{P, s p^k}(X)^2 + 2\sum_{k < l} F_{P, s p^k}(X) F_{P, s p^l}(X)$; summing over $s$ cancels $\sum_r F_{P, r}(X)^2$.
Integrating the finite sums term-by-term over the compact interval $[Y, \tau Y]$ against the continuous positive measure $dX / X$ yields (1), (3), and telescoping over $j = 1, \dots, J$ yields (4). $\blacksquare$

---

## 4. Single-Prime Gaussian Contraction

Fix a prime $p$, integer $T \ge 0$, cofactor $s \ge 1$ with $\gcd(s, N_P p) = 1$, and smooth factor $m \in \mathcal{S}(P)$. Define the finite prime-power Gaussian chain ($k \ge 0$):
$$a_{s, m, k}(X) := \begin{cases} \varphi_{s m p^k}(X), & s m p^k \le T, \\ 0, & s m p^k > T, \end{cases} \qquad A_{s, m}(X) := \sum_{k \ge 0} (-1)^k a_{s, m, k}(X)$$
(a finite sum supported on $0 \le k \le \lfloor \log_p(T / (s m)) \rfloor$ when $s m \le T$, and identically $0$ when $s m > T$).

**Lemma 4.1 (Consecutive Gaussian Ratio Identity and Unimodality).** *For $X > 0$, prime $p \ge 2$, and every $k \ge 0$ with $s m p^{k+1} \le T$, both $a_{s,m,k}(X)$ and $a_{s,m,k+1}(X)$ are strictly positive and satisfy*
$$\frac{a_{s, m, k+1}(X)}{a_{s, m, k}(X)} = p^{-3} \exp\!\left(\frac{X^2}{(s m)^2}\,p^{-2k}\left(1 - p^{-2}\right)\right).$$
*Because $1 - p^{-2} > 0$ and $p^{-2(k+1)} < p^{-2k}$, this consecutive ratio is strictly decreasing in $k$. Consequently, the finite sequence $(a_{s,m,k}(X))_{k=0}^K$ (extended by zeros for $s m p^k > T$) is nonnegative and unimodal: once $a_{s,m,k+1}(X) \le a_{s,m,k}(X)$ occurs at some $k$, $a_{s,m,j+1}(X) \le a_{s,m,j}(X)$ holds for all $j \ge k$.*

*Proof.* Direct algebra on $\varphi_{s m p^{k+1}}(X) / \varphi_{s m p^k}(X)$ gives $((s m p^{k+1}) / (s m p^k))^{-3} \exp(-X^2 (s m)^{-2}(p^{-2k-2} - p^{-2k})) = p^{-3}\exp((X^2/(s m)^2)p^{-2k}(1 - p^{-2}))$. If $a_{s,m,k+1}(X) \le a_{s,m,k}(X)$ while $s m p^{k+1} \le T$, the ratio at $k$ is $\le 1$; if $s m p^{k+2} \le T$, the ratio at $k+1$ is strictly smaller than at $k$, hence $< 1$, giving $a_{s,m,k+2}(X) < a_{s,m,k+1}(X)$, whereas if $s m p^{k+2} > T$, all subsequent terms are $0 \le a_{s,m,k+1}(X)$. Formally proved in Lean Theorem 19 (`gaussian_prime_chain_unimodal_and_singleton_contraction_tc056`). $\blacksquare$

**Lemma 4.2 (Finite Alternating-Unimodal Contraction; Lean Theorem 18: `finite_alternating_unimodal_chain_contraction_tc056`).** *Let $a_0, a_1, \dots, a_{n-1} \ge 0$ be any finite nonnegative unimodal sequence of length $n \ge 0$ (meaning there exists a peak index $k_*$ such that $a_0 \le \dots \le a_{k_*}$ and $a_{k_*} \ge a_{k_*+1} \ge \dots \ge a_{n-1}$, allowing ties, singletons $n = 1$, empty chains $n = 0$ with empty maximum defined as $0$, and trailing zeros). Then*
$$\left|\sum_{k = 0}^{n - 1} (-1)^k a_k\right| \le \max_{0 \le k < n} a_k, \qquad \left(\sum_{k = 0}^{n - 1} (-1)^k a_k\right)^2 \le \sum_{k = 0}^{n - 1} a_k^2.$$

*Proof.* For $n = 0$, both sides vanish ($0 \le 0$); for $n = 1$, $|a_0| = a_0$ and $a_0^2 \le a_0^2$. In general, split at the peak $k_*$: the prefix $b_j := a_{k_* - j}$ ($0 \le j \le k_*$) and suffix $c_r := a_{k_* + r}$ ($0 \le r < n - k_*$) are both nonincreasing nonnegative sequences starting at $a_{k_*}$. For any nonincreasing sequence $d_0 \ge d_1 \ge \dots \ge d_{m-1} \ge 0$ ($m \ge 1$), standard adjacent pairing gives $0 \le \sum_{r=0}^{m-1}(-1)^r d_r \le d_0$. Writing $\sum_{k=0}^{n-1}(-1)^k a_k = (-1)^{k_*}\!\left(\sum_{j=0}^{k_*}(-1)^j a_{k_*-j} + \sum_{r=0}^{n-1-k_*}(-1)^r a_{k_*+r} - a_{k_*}\right)$, the parenthesized sum is $(B + C - a_{k_*})$ with $0 \le B \le a_{k_*}$ and $0 \le C \le a_{k_*}$, hence lies in $[-a_{k_*}, a_{k_*}]$, proving $|\sum_k (-1)^k a_k| \le a_{k_*} = \max_k a_k$. Squaring gives $(\sum_k (-1)^k a_k)^2 \le a_{k_*}^2 \le \sum_{k=0}^{n-1} a_k^2$ (since all $a_k^2 \ge 0$). Formally proved in Lean Theorem 18 without `sorry`. $\blacksquare$

**Theorem 4.3 (Unconditional Singleton-Prime Gaussian Contraction; Lean Pointwise Instantiation: `gaussian_prime_chain_unimodal_and_singleton_contraction_tc056`).** *For every prime $p$, every $Y > 0$, and every integer $T \ge 0$,*
$$V_{\{p\}}(Y, T) \le D_T(Y),$$
*with **strict inequality** $V_{\{p\}}(Y, T) < D_T(Y)$ whenever $Y > 0$ and $T \ge p$ (and equality $V_{\{p\}}(Y, T) = D_T(Y)$ when $T < p$).*

*Proof.* Take $P = \{p\}$: the coprime cofactors are $1 \le s \le T$ with $p \nmid s$, and $F_{\{p\}, s}(X) = \lambda(s)\sum_{k: s p^k \le T} (-1)^k \varphi_{s p^k}(X) = \lambda(s) A_{s, 1}(X)$. Since $\lambda(s)^2 = 1$, Lemma 4.1 + Lemma 4.2 give pointwise for every $X > 0$:
$$\sum_{\substack{1 \le s \le T \\ p \nmid s}} F_{\{p\}, s}(X)^2 = \sum_{\substack{1 \le s \le T \\ p \nmid s}} A_{s, 1}(X)^2 \le \sum_{\substack{1 \le s \le T \\ p \nmid s}} \sum_{\substack{k \ge 0 \\ s p^k \le T}} \varphi_{s p^k}(X)^2 = \sum_{1 \le n \le T} \varphi_n(X)^2.$$
Integrating over $[Y, \tau Y]$ against $dX / X > 0$ yields $V_{\{p\}}(Y, T) \le D_T(Y)$. When $T \ge p$ and $X > 0$, consider the $s = 1$ chain $(a_0, a_1, \dots, a_K)$ with $K := \lfloor \log_p T \rfloor \ge 1$. Here $a_0 = \varphi_1(X) > 0$ and $a_1 = \varphi_p(X) > 0$. By Lemma 4.2, $A_{1,1}(X)^2 \le (\max_{0 \le k \le K} a_k)^2 = a_{k_*}^2$. Since $K \ge 1$, choosing $j \in \{0, 1\} \setminus \{k_*\}$ gives $a_j > 0$, so $\sum_{k=0}^K a_k^2 - A_{1,1}(X)^2 \ge a_{k_*}^2 + a_j^2 - a_{k_*}^2 = a_j^2 > 0$ for every $X \in [Y, \tau Y]$ (formally proved in Lean Theorem 19). Because the continuous function $X \mapsto \sum_{1 \le n \le T}\varphi_n(X)^2 - \sum_{p \nmid s} F_{\{p\}, s}(X)^2$ is strictly positive on the compact nondegenerate interval $[Y, \tau Y]$ ($Y > 0, \tau > 1$), its integral against $dX/X$ is strictly positive: $D_T(Y) - V_{\{p\}}(Y, T) > 0$. $\blacksquare$

At $Y = 4, T = 6$, certified singleton contractions illustrate Theorem 4.3:
- $p = 2$: $D_6(4) - V_{\{2\}}(4, 6) \in [0.01903040081925498042631326475837387890847 \pm 5.00 \times 10^{-42}] > 0$, <!-- tc-enclosure: observable="contraction_gap_D_minus_V_p" params="Y=4; T=6; p=2" json_path="section_4_single_prime_gaussian_contraction.singleton_contraction_rows[Y=4,T=6,p=2].contraction_gap_D_minus_V_p" -->
- $p = 3$: $D_6(4) - V_{\{3\}}(4, 6) \in [0.002148599064413455560236533257560062162331 \pm 4.00 \times 10^{-43}] > 0$, <!-- tc-enclosure: observable="contraction_gap_D_minus_V_p" params="Y=4; T=6; p=3" json_path="section_4_single_prime_gaussian_contraction.singleton_contraction_rows[Y=4,T=6,p=3].contraction_gap_D_minus_V_p" -->
- $p = 5$: $D_6(4) - V_{\{5\}}(4, 6) \in [3.192334226852521867535143031127922290164 \times 10^{-8} \pm 2.00 \times 10^{-48}] > 0$. <!-- tc-enclosure: observable="contraction_gap_D_minus_V_p" params="Y=4; T=6; p=5" json_path="section_4_single_prime_gaussian_contraction.singleton_contraction_rows[Y=4,T=6,p=5].contraction_gap_D_minus_V_p" -->

---

## 5. Separation of Contraction and Mixed Interaction & $P$-Independence of $C_{P,p}$

For a finite set of primes $P$ and a prime $p \notin P$, define the contraction functional and mixed-interaction functional:
$$C_{P, p}(Y, T) := \sum_{\substack{1 \le s \le T \\ \gcd(s, N_P p) = 1}} \sum_{\substack{m \in \mathcal{S}(P) \\ s m \le T}} \int_Y^{\tau Y} \left(\sum_{k \ge 0} a_{s, m, k}(X)^2 - A_{s, m}(X)^2\right)\frac{dX}{X},$$
$$M_{P, p}(Y, T) := \sum_{\substack{1 \le s \le T \\ \gcd(s, N_P p) = 1}} \sum_{\substack{m, n \in \mathcal{S}(P) \\ m \ne n \\ s m \le T,\; s n \le T}} \lambda(m)\lambda(n) \int_Y^{\tau Y} \left(A_{s, m}(X) A_{s, n}(X) - \sum_{k \ge 0} a_{s, m, k}(X) a_{s, n, k}(X)\right)\frac{dX}{X},$$
where the sum over $m \ne n$ is **ordered** (so **no** extra factor of $2$ is added).

**Theorem 5.1 (Exact Mixed Decomposition and $P$-Independence; Formal Pointwise Core: `mixed_interaction_decomposition_and_p_independence_tc056`).** *For every finite prime set $P$, prime $p \notin P$, $Y > 0$, and integer $T \ge 0$:*
1. **Sign and Decomposition**: $C_{P, p}(Y, T) \ge 0$, and
   $$\Delta_{P, p}(Y, T) = M_{P, p}(Y, T) - C_{P, p}(Y, T).$$
2. **Ordered $k \ne l$ Kernel Expansion**: *Without any extra factor of $2$,*
   $$M_{P, p}(Y, T) = \sum_{\substack{1 \le s \le T \\ \gcd(s, N_P p) = 1}} \sum_{\substack{m, n \in \mathcal{S}(P) \\ m \ne n \\ s m \le T,\; s n \le T}} \lambda(m)\lambda(n) \sum_{\substack{k, l \ge 0,\; k \ne l \\ s m p^k \le T,\; s n p^l \le T}} (-1)^{k + l} K_Y(s m p^k, s n p^l).$$
   *(In particular, $M_{\varnothing, p}(Y, T) = 0$ identically because $\mathcal{S}(\varnothing) = \{1\}$ contains no pair $m \ne n$.)*
3. **$P$-Independence of $C_{P, p}$**: *The map $(s, m) \mapsto r := s m$ is a bijection between $\{(s, m) : \gcd(s, N_P p) = 1,\; m \in \mathcal{S}(P),\; 1 \le s m \le T\}$ and $\{1 \le r \le T : p \nmid r\}$. Since $a_{s, m, k}(X) = \varphi_{r p^k}(X) = a_{r, 1, k}^{\varnothing}(X)$ depends only on the product $r = s m$, $C_{P, p}(Y, T)$ is completely independent of $P$:*
   $$C_{P, p}(Y, T) = C_{\varnothing, p}(Y, T) =: C_p(Y, T) = D_T(Y) - V_{\{p\}}(Y, T).$$
4. **Global Ascending-Prime Formula**: *Writing $M_p(Y, T) := M_{\{\text{primes } < p\}, p}(Y, T)$ (with $M_2(Y, T) = 0$),*
   $$E_T(Y) = D_T(Y) + \sum_{p \le T} M_p(Y, T) - \sum_{p \le T} C_p(Y, T).$$

*Proof.* Identities (1)–(3) hold pointwise at every $X > 0$ and are machine-checked in Lean Theorem 20 (`mixed_interaction_decomposition_and_p_independence_tc056`), while (4) follows immediately by combining Theorem 3.1(4) (Lean Theorem 17(4)) with (1) and (3):
- For $\gcd(s, N_P p) = 1$, $F_{P, s p^k}(X) = \sum_{m \in \mathcal{S}(P), s m p^k \le T} \lambda(s m p^k)\varphi_{s m p^k}(X) = \lambda(s)(-1)^k \sum_{m \in \mathcal{S}(P), s m \le T} \lambda(m) a_{s,m,k}(X)$, and summing over $k \ge 0$ gives $F_{P \cup \{p\}, s}(X) = \lambda(s)\sum_{m \in \mathcal{S}(P), s m \le T} \lambda(m) A_{s,m}(X)$.
- Using $\lambda(s)^2 = 1$ and $\lambda(m)^2 = 1$, expanding $F_{P \cup \{p\}, s}(X)^2 - \sum_{k \ge 0} F_{P, s p^k}(X)^2$ separates the diagonal $m = n$ terms $-\sum_m (\sum_k a_{s,m,k}(X)^2 - A_{s,m}(X)^2)$ from the ordered off-diagonal $m \ne n$ terms $\sum_{m \ne n} \lambda(m)\lambda(n)(A_{s,m}(X)A_{s,n}(X) - \sum_k a_{s,m,k}(X)a_{s,n,k}(X))$.
- Expanding $A_{s,m}(X)A_{s,n}(X) = \sum_{k, l \ge 0} (-1)^{k+l} a_{s,m,k}(X)a_{s,n,l}(X)$ and subtracting the $k = l$ diagonal $\sum_k (-1)^{2k} a_{s,m,k}(X)a_{s,n,k}(X)$ leaves the ordered $k \ne l$ sum.
- Every positive integer $1 \le r \le T$ with $p \nmid r$ factors uniquely as $r = m s$ with $m \in \mathcal{S}(P)$ and $\gcd(s, N_P) = 1$; since $p \nmid r$ and $p \notin P$, $p \nmid s$ as well, so $\gcd(s, N_P p) = 1$. Thus $(s, m) \leftrightarrow r = s m$ is an exact finite bijection, proving $C_{P, p}(Y, T) = C_{\varnothing, p}(Y, T) = D_T(Y) - V_{\{p\}}(Y, T)$.
- Nonnegativity $C_{P,p}(Y, T) \ge 0$ follows from Lemma 4.1 + Lemma 4.2 on every chain $(s, m)$, and (4) follows by substituting (1) and (3) into Theorem 3.1(4). $\blacksquare$

---

## 6. Unconditional Uniform Bound on Total Contraction $\sum_{p \le T} C_p(Y, T)$

Recall from `TC-055R2` Theorem 5.2 (`verify_euler_maclaurin_derivatives_and_constants_arb`) that the infinite diagonal energy $D_E(U) := \sum_{n \ge 1} K_U(n, n)$ ($U > 0$) satisfies
$$D_E(U) \le L_D + C_{D, 2} U^{-2}, \qquad L_D := \frac{3\sqrt{\tau}}{64}\log \tau, \qquad C_{D, 2} := \frac{C_2(1 - \tau^{-2})}{16\sqrt{2}},$$
with certified 256-bit Arb enclosures:
- $L_D \in [0.2159472478105097999629716116351322819076 \pm 4.00 \times 10^{-41}]$, <!-- tc-enclosure: observable="L_D" params="precision_bits=256" json_path="section_6_uniform_total_contraction_bound.L_D" -->
- $C_{D, 2} \in [0.07974240995631961059711944730929191094454 \pm 5.00 \times 10^{-44}]$, <!-- tc-enclosure: observable="C_D2" params="precision_bits=256" json_path="section_6_uniform_total_contraction_bound.C_D2" -->
- $B_D := L_D + 2 C_{D, 2} \in [0.3754320677231490211572105062537161037967 \pm 2.00 \times 10^{-41}]$. <!-- tc-enclosure: observable="B_D_eq_L_D_plus_2_C_D2" params="precision_bits=256" json_path="section_6_uniform_total_contraction_bound.B_D_eq_L_D_plus_2_C_D2" -->

**Theorem 6.1 (Shifted Diagonal Scaling and Uniform Bound on Total Contraction).** *For every integer $d \ge 2$, define $c_d := \sqrt{\frac{1 + d^{-2}}{2}} \in \left[\frac{1}{\sqrt{2}}, 1\right)$ and $A_d(Y) := \sum_{n \ge 1} K_Y(n, n d)$. Then:*
1. **Exact Shifted-Diagonal Change of Variables**: *For every $Y > 0$ and $d \ge 2$,*
   $$A_d(Y) = d^{-3} c_d^{-5} D_E(c_d Y),$$
   *and for every $Y \ge 1$ and $d \ge 2$,*
   $$A_d(Y) \le 2^{5/2} d^{-3} B_D.$$
2. **Exact Finite Alternating Shift Formula**: *For every prime $p$, $Y > 0$, and integer $T \ge 0$,*
   $$C_p(Y, T) = 2 \sum_{\substack{h \ge 1 \\ p^h \le T}} (-1)^{h + 1} \sum_{1 \le n \le \lfloor T / p^h \rfloor} K_Y(n, n p^h).$$
3. **Uniform Total Contraction Bound**: *For every $Y \ge 1$ and every integer $T \ge 0$,*
   $$0 \le \sum_{p \le T} C_p(Y, T) \le 2 \sum_{p} \sum_{h \ge 1} A_{p^h}(Y) \le 2^{7/2} B_D \sum_{p} \frac{1}{p^3 - 1} \le 2^{7/2} B_D \cdot \frac{8}{7}\left(\zeta(3) - 1\right) < 1,$$
   *with certified constants*
   $$\sum_{p} \frac{1}{p^3 - 1} \in [0.1941181698326337922995874849113808374519 \pm 3.00 \times 10^{-41}],$$ <!-- tc-enclosure: observable="prime_sum_1_over_p3_minus_1" params="precision_bits=256" json_path="section_6_uniform_total_contraction_bound.prime_sum_1_over_p3_minus_1" -->
   $$\frac{8}{7}\left(\zeta(3) - 1\right) \in [0.2309221750395363261711293274416571323028 \pm 5.00 \times 10^{-41}],$$ <!-- tc-enclosure: observable="elementary_upper_8_over_7_times_zeta3_minus_1" params="precision_bits=256" json_path="section_6_uniform_total_contraction_bound.elementary_upper_8_over_7_times_zeta3_minus_1" -->
   $$U_{\mathrm{contr,sharp}} := 2^{7/2} B_D \sum_{p} \frac{1}{p^3 - 1} \in [0.8245225510139468806744875745216032453175 \pm 2.00 \times 10^{-41}],$$ <!-- tc-enclosure: observable="uniform_contraction_cap_sharp_2_pow_7_2_B_D_sum_p" params="precision_bits=256" json_path="section_6_uniform_total_contraction_bound.uniform_contraction_cap_sharp_2_pow_7_2_B_D_sum_p" -->
   $$U_{\mathrm{contr,elem}} := 2^{7/2} B_D \cdot \frac{8}{7}\left(\zeta(3) - 1\right) \in [0.9808486295406997551364248253338056621724 \pm 2.00 \times 10^{-41}],$$ <!-- tc-enclosure: observable="uniform_contraction_cap_elementary_closed_form" params="precision_bits=256" json_path="section_6_uniform_total_contraction_bound.uniform_contraction_cap_elementary_closed_form" -->
   $$1 - U_{\mathrm{contr,elem}} \in [0.01915137045930024486357517466619433782758 \pm 4.00 \times 10^{-42}] > 0.$$ <!-- tc-enclosure: observable="one_minus_elementary_cap_margin" params="precision_bits=256" json_path="section_6_uniform_total_contraction_bound.one_minus_elementary_cap_margin" -->

*Proof.*
1. Fix $Y > 0$, $d \ge 2$, and $n \ge 1$. Expanding $\varphi_n(X)\varphi_{n d}(X) = X^5 n^{-6} d^{-3} \exp\!\left(-X^2 n^{-2}(1 + d^{-2})\right) = X^5 n^{-6} d^{-3} \exp\!\left(-2(c_d X)^2 / n^2\right)$ and substituting $W := c_d X$ ($dW / W = dX / X$, mapping $[Y, \tau Y]$ onto $[c_d Y, \tau c_d Y]$) gives
   $$K_Y(n, n d) = d^{-3} c_d^{-5} \int_{c_d Y}^{\tau c_d Y} W^5 n^{-6} \exp\!\left(-\frac{2 W^2}{n^2}\right)\frac{dW}{W} = d^{-3} c_d^{-5} K_{c_d Y}(n, n) > 0.$$
   Since $K_{c_d Y}(n, n) \le n^{-6}\int_{c_d Y}^{\tau c_d Y} W^4\,dW = \frac{\tau^5 - 1}{5}(c_d Y)^5 n^{-6}$, the positive series $\sum_{n \ge 1} K_Y(n, n d)$ converges absolutely to $d^{-3} c_d^{-5} D_E(c_d Y)$. For $d \ge 2$ and $Y \ge 1$, $c_d \ge 1/\sqrt{2}$ implies $c_d^{-5} \le 2^{5/2}$ and $(c_d Y)^{-2} \le 2 Y^{-2} \le 2$, so $D_E(c_d Y) \le L_D + C_{D, 2}(c_d Y)^{-2} \le L_D + 2 C_{D, 2} = B_D$, giving $A_d(Y) \le 2^{5/2} d^{-3} B_D$.
2. By Theorem 5.1(3) and Theorem 3.1(3) with $P = \varnothing$, $C_p(Y, T) = -\Delta_{\varnothing, p}(Y, T) = -2\sum_{1 \le s \le T,\, p \nmid s}\sum_{0 \le k < l,\, s p^l \le T} (-1)^{k + l} K_Y(s p^k, s p^l)$. Setting $h := l - k \ge 1$ and $n := s p^k$, the map $(s, k, l) \mapsto (h, n)$ is a bijection onto $\{(h, n) : h \ge 1,\; p^h \le T,\; 1 \le n \le \lfloor T / p^h \rfloor\}$ (with inverse $s = n / p^{v_p(n)}$, $k = v_p(n)$, $l = k + h$), and $-(-1)^{2k + h} = (-1)^{h + 1}$. Pointwise equivalence is also formally verified in Lean Theorem 20.
3. Because $K_Y(n, n p^h) > 0$ for every $n \ge 1, h \ge 1$ (and in fact dropping the negative even-$h$ terms $(-1)^{h+1} = -1$ already bounds $C_p(Y, T)$ by $2\sum_{h \ge 1 \text{ odd}} \sum_{n \le \lfloor T/p^h\rfloor} K_Y(n, n p^h) \le 2\sum_{h \ge 1} \sum_{n \le \lfloor T/p^h\rfloor} K_Y(n, n p^h)$, or equivalently using $|(-1)^{h+1}| = 1$), monotonicity of nonnegative sums justifies extending $1 \le n \le \lfloor T / p^h \rfloor$ to all $n \ge 1$, $p^h \le T$ to all $h \ge 1$, and $p \le T$ to all primes $p$:
   $$0 \le \sum_{p \le T} C_p(Y, T) \le 2 \sum_{p} \sum_{h \ge 1} A_{p^h}(Y) \le 2^{7/2} B_D \sum_{p} \sum_{h \ge 1} p^{-3 h} = 2^{7/2} B_D \sum_{p} \frac{1}{p^3 - 1}.$$
   Finally, for every prime $p \ge 2$, $\frac{1}{p^3 - 1} = \frac{p^3}{p^3 - 1} p^{-3} \le \frac{8}{7} p^{-3}$, and since the primes form a subset of $\mathbb{Z}_{\ge 2}$, $\sum_p \frac{1}{p^3 - 1} \le \frac{8}{7}\sum_{m \ge 2} m^{-3} = \frac{8}{7}(\zeta(3) - 1) < \infty$, justifying Tonelli's theorem on the positive double sum. $\blacksquare$

> **Architectural Significance & Non-Monotonicity Immunity.** Theorem 6.1 proves unconditionally that the accumulated single-prime contractions across **all** primes $\le T$ remove at most $U_{\mathrm{contr,sharp}} < 0.8246 < 1$ units of energy uniformly for all $Y \ge 1, T \ge 0$. Notably, $T \mapsto C_p(Y, T)$ is **not** monotone increasing and need not satisfy $C_p(Y, T) \le C_p(Y, \infty)$ (for instance, at $p = 2, Y = 1$, $C_2(1, 15) > C_2(1, \infty) > C_2(1, 16)$ due to the negative $h = 4$ shift entering at $T = 16$); Step 3 of Theorem 6.1 is completely immune to this non-monotonicity because it bounds the finite alternating shift sum directly via $K_Y > 0$ and $|(-1)^{h+1}| = 1$ (or by dropping negative even-$h$ shifts) before extending over $n \ge 1, h \ge 1$. Hence singleton contractions alone can never cancel a super-bounded positive surge; any subpower bound on $E_{T(Y)}(Y)$ must come from signed cancellation inside $\sum_{p \le T} M_p(Y, T)$.

---

## 7. Certified Falsification Controls & Multiplicative Parity Controls

### 7.1 Control 7a — Later Prime Additions Need Not Contract ($Y = 4, T = 6, P = \{2\}, p = 3$)
Evaluating $V_{\{2\}}(4, 6)$ and $V_{\{2, 3\}}(4, 6)$ both via exact kernel-matrix grouping and via independent `acb.integral` Gauss–Legendre smooth-fiber quadrature certifies:
- $V_{\{2\}}(4, 6) \in [0.04108068274165805876627229532425443472724 \pm 2.00 \times 10^{-42}]$, <!-- tc-enclosure: observable="V_P2" params="Y=4; T=6; adjoined_prime_p=3" json_path="section_7_falsification_and_parity_controls.control_7a_stepwise_positivity_witness_Y4_T6_P2_p3.V_P2" -->
- $V_{\{2, 3\}}(4, 6) \in [0.04878927689438566504682432312715229376034 \pm 2.00 \times 10^{-42}]$, <!-- tc-enclosure: observable="V_P23" params="Y=4; T=6; adjoined_prime_p=3" json_path="section_7_falsification_and_parity_controls.control_7a_stepwise_positivity_witness_Y4_T6_P2_p3.V_P23" -->
- $\Delta_{\{2\}, 3}(4, 6) = M_{\{2\}, 3}(4, 6) - C_3(4, 6) \in [0.007708594152727606280552027802897859033100 \pm 2.00 \times 10^{-43}] > 0$, <!-- tc-enclosure: observable="Delta_P2_p3" params="Y=4; T=6; adjoined_prime_p=3" json_path="section_7_falsification_and_parity_controls.control_7a_stepwise_positivity_witness_Y4_T6_P2_p3.Delta_P2_p3" -->
where $M_{\{2\}, 3}(4, 6) \in [0.009857193217141061840788561060457921195432 \pm 5.00 \times 10^{-43}]$ <!-- tc-enclosure: observable="M_P2_p3" params="Y=4; T=6; adjoined_prime_p=3" json_path="section_7_falsification_and_parity_controls.control_7a_stepwise_positivity_witness_Y4_T6_P2_p3.M_P2_p3" -->
strictly outweighs $C_3(4, 6) \in [0.002148599064413455560236533257560062162331 \pm 4.00 \times 10^{-43}]$. <!-- tc-enclosure: observable="C_3" params="Y=4; T=6; adjoined_prime_p=3" json_path="section_7_falsification_and_parity_controls.control_7a_stepwise_positivity_witness_Y4_T6_P2_p3.C_3" -->
The outward-rounded lower endpoint of $\Delta_{\{2\}, 3}(4, 6)$ is strictly positive (`> +0.00770859...`), **refuting** any proof strategy that attempts to iterate singleton monotonicity ($\Delta_{P, p} \le 0$).

### 7.2 Control 7b — Refutation of Explicit One-Diagonal Budget per Dyadic Block ($Y = 128, T = 431, 64 \le p < 128$)
At $Y = 128$, $T(128) = \lceil 128^{5/4} \rceil = 431$, across the $13$ primes in the dyadic block $64 \le p < 128$ ($p \in \{67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127\}$), certified both by cross-fiber kernel summation and by independent `acb.integral` quadrature of $V_{P_{<128}}(128, 431) - V_{P_{<64}}(128, 431)$:
- $D_{431}(128) \in [0.1433167490621216536923229185944279250334 \pm 2.00 \times 10^{-42}]$, <!-- tc-enclosure: observable="D_431_128" params="Y=128; T=431" json_path="section_7_falsification_and_parity_controls.control_7b_dyadic_block_surge_Y128_T431_block_64_to_128.D_431_128" -->
- $E_{431}(128) \in [0.02363259184198284689569412394614253221221 \pm 5.00 \times 10^{-43}]$, <!-- tc-enclosure: observable="E_431_128" params="Y=128; T=431" json_path="section_7_falsification_and_parity_controls.control_7b_dyadic_block_surge_Y128_T431_block_64_to_128.E_431_128" -->
- $\sum_{64 \le p < 128} \Delta_p(128, 431) \in [0.1922515942217511282452862066402187681259 \pm 4.00 \times 10^{-41}]$, <!-- tc-enclosure: observable="sum_Delta_64_le_p_lt_128" params="Y=128; T=431" json_path="section_7_falsification_and_parity_controls.control_7b_dyadic_block_surge_Y128_T431_block_64_to_128.sum_Delta_64_le_p_lt_128" -->
- $\frac{\sum_{64 \le p < 128} \Delta_p(128, 431)}{D_{431}(128)} \in [1.341445403135807395858003108107295454023 \pm 3.00 \times 10^{-40}] > 1$, <!-- tc-enclosure: observable="ratio_sum_Delta_over_D_431" params="Y=128; T=431" json_path="section_7_falsification_and_parity_controls.control_7b_dyadic_block_surge_Y128_T431_block_64_to_128.ratio_sum_Delta_over_D_431" -->
with excess margin above $1$ equal to $[0.3414454031358073958580031081072954540233 \pm 2.00 \times 10^{-41}] > 0$. <!-- tc-enclosure: observable="ratio_minus_1_margin" params="Y=128; T=431" json_path="section_7_falsification_and_parity_controls.control_7b_dyadic_block_surge_Y128_T431_block_64_to_128.ratio_minus_1_margin" -->
This outward-certified finite counterexample **refutes** the explicit inequality $\sum_{B \le p < 2 B} \Delta_p(Y, T) \le D_T(Y)$. (As required by `AGENTS.md`, a single finite sample refutes only that explicit constant-$1$ inequality, not an unspecified constant — Section 8.3 below proves analytically why *every* sublinear bound on an isolated block fails as $Y \to \infty$.)

### 7.3 Control 7c — Multiplicative Parity Controls ($a_2$, $a_{\{3,5,7\}}$, and Unsigned $\mathbf{1}$)
For $a_S(n) = (-1)^{\sum_{p \in S} v_p(n)}$, $a_S(p) = -1$ holds **only** for $p \in S$, whereas $a_S(q) = +1$ for $q \notin S$. Accordingly, singleton-prime grouping contracts at $p \in S$ (alternating Gaussian chain) and **expands** at $q \notin S$ (positive non-alternating chain):
- At $(Y = 8, T = 14)$, where $D_{14}(8) \in [0.07199381838328490848566615999421660333095 \pm 2.00 \times 10^{-42}]$: <!-- tc-enclosure: observable="D_14_8" params="Y=8; T=14" json_path="section_7_falsification_and_parity_controls.control_7c_parity_controls_a2_a357_and_unit_Y8_T14.D_14_8" -->
  - Under $a_2$: $V_{\{2\}}^{(a_2)}(8, 14) \in [0.04835623437516580888844323413789981685826 \pm 4.00 \times 10^{-43}] < D_{14}(8)$ (contracts at $2 \in \{2\}$), <!-- tc-enclosure: observable="V_singleton_2_under_a2_contracts" params="Y=8; T=14" json_path="section_7_falsification_and_parity_controls.control_7c_parity_controls_a2_a357_and_unit_Y8_T14.V_singleton_2_under_a2_contracts" -->
    while $V_{\{3\}}^{(a_2)}(8, 14) \in [0.07316183519642907405918609986671065148104 \pm 3.00 \times 10^{-42}] > D_{14}(8)$ (expands at $3 \notin \{2\}$). <!-- tc-enclosure: observable="V_singleton_3_under_a2_expands" params="Y=8; T=14" json_path="section_7_falsification_and_parity_controls.control_7c_parity_controls_a2_a357_and_unit_Y8_T14.V_singleton_3_under_a2_expands" -->
  - Under $a_{\{3,5,7\}}$: $V_{\{2\}}^{(a_{\{3,5,7\}})}(8, 14) \in [0.09574922966870500827335989421796625204502 \pm 7.00 \times 10^{-43}] > D_{14}(8)$ (expands at $2 \notin \{3,5,7\}$), <!-- tc-enclosure: observable="V_singleton_2_under_a357_expands" params="Y=8; T=14" json_path="section_7_falsification_and_parity_controls.control_7c_parity_controls_a2_a357_and_unit_Y8_T14.V_singleton_2_under_a357_expands" -->
    while $V_{\{3\}}^{(a_{\{3,5,7\}})}(8, 14) \in [0.07082580157014074291214622022506191707405 \pm 4.00 \times 10^{-42}] < D_{14}(8)$ (contracts at $3 \in \{3,5,7\}$). <!-- tc-enclosure: observable="V_singleton_3_under_a357_contracts" params="Y=8; T=14" json_path="section_7_falsification_and_parity_controls.control_7c_parity_controls_a2_a357_and_unit_Y8_T14.V_singleton_3_under_a357_contracts" -->
- At $(Y = 32, T = 77)$, where $D_{77}(32) \in [0.1049251689247871304656114521838006037396 \pm 3.00 \times 10^{-41}]$, <!-- tc-enclosure: observable="D_77_32" params="Y=32; T=77" json_path="section_7_falsification_and_parity_controls.control_7c_linear_overtake_Y32_T77.D_77_32" -->
  the linear-$Y$ growth of finite-$S$ parity controls (Proposition 2.1) already overtakes $D_{77}(32)$:
  - $E_{77}^{(a_2)}(32) \in [0.5910096864957524085681904779766936866450 \pm 4.00 \times 10^{-41}] > D_{77}(32)$, <!-- tc-enclosure: observable="E_77_32_a2" params="Y=32; T=77" json_path="section_7_falsification_and_parity_controls.control_7c_linear_overtake_Y32_T77.E_77_32_a2" -->
  - $E_{77}^{(a_{\{3,5,7\}})}(32) \in [0.5282292974508938880187074007664986560952 \pm 2.00 \times 10^{-41}] > D_{77}(32)$, <!-- tc-enclosure: observable="E_77_32_a357" params="Y=32; T=77" json_path="section_7_falsification_and_parity_controls.control_7c_linear_overtake_Y32_T77.E_77_32_a357" -->
  whereas true all-prime Liouville energy remains suppressed at $E_{77}^{(\lambda)}(32) \in [0.03136294235359265630892143096718869405404 \pm 3.00 \times 10^{-42}] < D_{77}(32)$. <!-- tc-enclosure: observable="E_77_32_liouville" params="Y=32; T=77" json_path="section_7_falsification_and_parity_controls.control_7c_linear_overtake_Y32_T77.E_77_32_liouville" -->

---

## 8. Quantified Signed Mixed-Prime Block Estimate Attempt (Theorems 8.A–8.D)

For $Y \ge 1$, $T(Y) = \lceil Y^{5/4} \rceil$, and integer $j \ge 1$, define the half-open dyadic prime blocks and their mixed/contraction sums:
$$I_j(Y) := \{p \text{ prime} : 2^j \le p < 2^{j + 1},\; p \le T(Y)\}, \qquad M_j(Y) := \sum_{p \in I_j(Y)} M_p(Y, T(Y)), \qquad C_j(Y) := \sum_{p \in I_j(Y)} C_p(Y, T(Y)).$$

### 8.1 Theorem 8.A — Conditional Dyadic-Block Transfer Across All $Y \ge 1$

**Theorem 8.A (Conditional Dyadic-Block Transfer).** *Suppose that for every $\delta > 0$ there exists $A_\delta < \infty$ (independent of $Y$, $j$, and prime cutoffs) such that*
$$M_j(Y) - C_j(Y) \le A_\delta Y^\delta \qquad (\forall\,Y \ge 1,\; \forall\,j \ge 1).$$
*Then for every $\varepsilon > 0$ and **all** $Y \ge 1$,*
$$E_{T(Y)}(Y) \le C_\varepsilon Y^\varepsilon, \qquad C_\varepsilon := B_D + \left(1 + \frac{5}{2 e (\log 2)\,\varepsilon}\right) A_{\varepsilon / 2},$$
*and consequently $E_\lambda(Y) \le 2 C_\varepsilon Y^\varepsilon + \frac{\tau^5 - 1}{10}$ for all $Y \ge 1$.*

*Proof.* We treat $Y = 1$ and $Y > 1$ explicitly:
- At $Y = 1$, $T(1) = \lceil 1^{5/4} \rceil = 1 < 2$, so $I_j(1) = \varnothing$ for every $j \ge 1$ ($N_{\mathrm{blocks}}(1) = 0$) and $E_1(1) = D_1(1) \le D_E(1) \le L_D + C_{D, 2} < B_D \le C_\varepsilon \cdot 1^\varepsilon$.
- For $Y > 1$, any nonempty block $I_j(Y)$ satisfies $2^j \le T(Y) < Y^{5/4} + 1 < 2 Y^{5/4}$, so $1 \le j \le J_{\max}(Y) := \lfloor \log_2(2 Y^{5/4}) \rfloor = 1 + \left\lfloor \frac{5}{4 \log 2}\log Y \right\rfloor \le 1 + \frac{5}{4 \log 2}\log Y$.
Applying the hypothesis at $\delta = \varepsilon / 2$ (with $A_{\varepsilon/2} \ge 0$, since empty blocks have $M_j - C_j = 0 \le A_{\varepsilon/2} Y^{\varepsilon/2}$) and $D_{T(Y)}(Y) \le D_E(Y) \le B_D$ ($Y \ge 1$) gives
$$E_{T(Y)}(Y) = D_{T(Y)}(Y) + \sum_{j = 1}^{J_{\max}(Y)} \left(M_j(Y) - C_j(Y)\right) \le B_D + \left(1 + \frac{5}{4 \log 2}\log Y\right) A_{\varepsilon / 2} Y^{\varepsilon / 2}.$$
For all $Y \ge 1$, $Y^{\varepsilon/2} \ge 1$ and $\max_{Y \ge 1} (\log Y) Y^{-\varepsilon / 2} = \frac{2}{e \varepsilon}$ (attained at $\log Y = 2 / \varepsilon$), so $(1 + \frac{5}{4\log 2}\log Y) Y^{\varepsilon/2} \le \left(1 + \frac{5}{2 e (\log 2)\varepsilon}\right) Y^\varepsilon$. Combining with $E_\lambda(Y) \le 2 E_{T(Y)}(Y) + 2\mathcal{R}_{\mathrm{tail}}(Y, T(Y)) \le 2 C_\varepsilon Y^\varepsilon + \frac{\tau^5 - 1}{10}$ completes the proof. $\blacksquare$

### 8.2 Theorem 8.B — Unconditional Mixed-Kernel Regimes: Low-Prime Blocks and Super-$\sqrt{T}$ Blocks

We now expand $M_j(Y)$ into its exact $\lambda(m)\lambda(n)$-weighted Gaussian mixed kernels and establish unconditional bounds at **both** ends of the prime spectrum (retaining all prime multiplicities, hyperbolic cutoffs, asymmetric index ranges, and negative terms).

**Lemma 8.1 (Uniform Shifted Off-Diagonal Kernel Sum Bound).** *For all $Y \ge 1$ and all positive integers $u, v \ge 1$,*
$$\sum_{s = 1}^\infty K_Y(s u, s v) \le \frac{D_*}{\sqrt{u v}}, \qquad D_* := \max\!\left(L_D + 16 C_{D, 2},\; \frac{\zeta(6)(\tau^5 - 1)}{5120}\right) \in [1.945595069851794767473799256941604027154 \pm 3.00 \times 10^{-40}].$$ <!-- tc-enclosure: observable="D_star_shifted_kernel_constant" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8B_unconditional_low_and_top_block_bounds.D_star_shifted_kernel_constant" -->

*Proof.* For $s, u, v \ge 1$, $\varphi_{s u}(X)\varphi_{s v}(X) = X^5 s^{-6} (u v)^{-3} \exp\!\left(-X^2 s^{-2}(u^{-2} + v^{-2})\right)$. Setting $c_{u, v} := \sqrt{(u^{-2} + v^{-2}) / 2}$ and substituting $W := c_{u, v} X$ ($dW / W = dX / X$) yields the exact identity
$$\sum_{s = 1}^\infty K_Y(s u, s v) = (u v)^{-3} c_{u, v}^{-5}\,D_E(c_{u, v} Y) = \frac{2^{5/2} u^2 v^2}{(u^2 + v^2)^{5/2}}\,D_E(c_{u, v} Y).$$
By AM–GM, $u^2 + v^2 \ge 2 u v$, so $\frac{2^{5/2} u^2 v^2}{(u^2 + v^2)^{5/2}} \le \frac{2^{5/2} u^2 v^2}{(2 u v)^{5/2}} = (u v)^{-1/2}$. To bound $D_E(w)$ uniformly for **all** $w = c_{u, v} Y > 0$ (note $c_{u, v}$ can be arbitrarily small when $u, v$ are large!):
- If $w \ge 1/4$, `TC-055R2` Theorem 5.2 gives $D_E(w) \le L_D + C_{D, 2} w^{-2} \le L_D + 16 C_{D, 2}$.
- If $0 < w < 1/4$, bounding $\exp(-2 W^2 / s^2) \le 1$ directly gives $D_E(w) = \sum_{s \ge 1}\int_w^{\tau w} W^4 s^{-6}\,dW \le \zeta(6)\frac{\tau^5 - 1}{5} w^5 < \frac{\zeta(6)(\tau^5 - 1)}{5 \cdot 4^5} = \frac{\zeta(6)(\tau^5 - 1)}{5120}$.
Hence $D_E(c_{u, v} Y) \le D_*$ for all $Y \ge 1, u, v \ge 1$. $\blacksquare$

**Theorem 8.B (Unconditional Low-Prime Block Subpower Bound & Super-$\sqrt{T}$ Block Identity + Top-Block Power Saving).** *Let $Y \ge 1$, $T = T(Y) = \lceil Y^{5/4} \rceil$, and $B := 2^j$ ($j \ge 1$).*
1. **Low-Prime Blocks ($j = 1$ and Polylogarithmic $B$)**: *First, $M_2(Y, T) = 0$ identically. For any $j \ge 1$,*
   $$|M_j(Y)| \le 2 D_* \left(\sum_{p \in I_j(Y)} p^{-1/2}\right) \prod_{q < 2 B} \left(1 - q^{-1/2}\right)^{-2}.$$
   *In particular, using the elementary bound $\sum_{q < 2 B} (-\log(1 - q^{-1/2})) \le 2\sqrt{2 B}$ gives $|M_j(Y)| \ll_\delta Y^\delta$ for $B \ll_\delta (\log Y)^2$ ($Y \ge 2$), while using the PNT asymptotic $\sum_{q < 2 B} (-\log(1 - q^{-1/2})) = (2 + o(1))\frac{\sqrt{2 B}}{\log(2 B)}$ (§2.3) extends this unconditionally to $B \le \frac{\delta^2}{32}(\log Y \log\log Y)^2$ for $Y \ge e^e$.*
2. **Exact Super-$\sqrt{T}$ Block Identity ($B > \sqrt{T}$)**: *Whenever $B > \sqrt{T}$, every $n \le T$ satisfies $v_p(n) \in \{0, 1\}$ for all $p \ge B$ and has at most one prime divisor $\ge B$. Writing $S_{< U, T}(X) := F_{P_{< U}, 1}(X) = \sum_{m \in \mathcal{S}(P_{< U}),\, m \le T} \lambda(m)\varphi_m(X)$, we have the **exact** identity (retaining the negative diagonal prime-fiber term):*
   $$M_j(Y) - C_j(Y) = \int_Y^{\tau Y} \left(S_{< 2 B, T}(X)^2 - S_{< B, T}(X)^2\right)\frac{dX}{X} - \sum_{p \in I_j(Y)} \frac{1}{p}\int_Y^{\tau Y} Q_{\lfloor T / p \rfloor}\!\left(\frac{X}{p}\right)^2\frac{dX}{X}.$$
3. **Top-Block Power Saving ($B \ge Y^{1 + \theta}$, $0 < \theta \le 1/4$)**: *For every super-$\sqrt{T}$ block $B > \sqrt{T}$,*
   $$M_j(Y) - C_j(Y) \le C_{\mathrm{top}}\,Y^3 \sum_{p \in I_j(Y)} p^{-3}, \qquad |M_j(Y) - C_j(Y)| \le \frac{3}{2} C_{\mathrm{top}}\,Y^3 \sum_{p \in I_j(Y)} p^{-3},$$
   *where*
   $$C_{\mathrm{top}} := \frac{2(\tau^3 - 1)\zeta(3) M_{\mathbf{1}}}{3} \in [261.2990547428337411338855133932080948975 \pm 1.00 \times 10^{-38}].$$ <!-- tc-enclosure: observable="top_block_constant_2_tau3_minus_1_zeta3_M1_over_3" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8B_unconditional_low_and_top_block_bounds.top_block_constant_2_tau3_minus_1_zeta3_M1_over_3" -->
   *Consequently, for $B \ge Y^{1 + \theta}$ ($0 < \theta \le 1/4$), $\sum_{p \in I_j(Y)} p^{-3} \ll B^{-2}/\log B$ yields the unconditional power saving $M_j(Y) - C_j(Y) \ll \frac{Y^{1 - 2\theta}}{\log Y}$ (reaching $O\!\left(\frac{Y^{1/2}}{\log Y}\right)$ on the top blocks $B \asymp Y^{5/4}$).*

*Proof.*
1. By Theorem 5.1(2) with $P = P_{< p} := \{q \text{ prime} : q < p\}$, taking absolute values on the ordered sum over $m \ne n \in \mathcal{S}(P_{< p})$ and ordered $k \ne l \ge 0$ (retaining exact cutoffs $s m p^k \le T, s n p^l \le T$, then extending $1 \le s \le T$ with $\gcd(s, N_{P_{\le p}}) = 1$ to all $s \ge 1$ by positivity $K_Y > 0$) gives via Lemma 8.1:
   $$|M_p(Y, T)| \le \sum_{\substack{m, n \in \mathcal{S}(P_{< p}) \\ m \ne n}} \sum_{\substack{k, l \ge 0 \\ k \ne l}} \sum_{s = 1}^\infty K_Y(s m p^k, s n p^l) \le D_* \sum_{m, n \in \mathcal{S}(P_{< p})} (m n)^{-1/2} \sum_{\substack{k, l \ge 0 \\ k \ne l}} p^{-(k + l)/2}.$$
   For $p = 2$, $\mathcal{S}(\varnothing) = \{1\}$ has no $m \ne n$, so $M_2(Y, T) = 0$. For odd $p \in I_j(Y)$ ($p \ge 3$), $\sum_{k \ne l \ge 0} p^{-(k+l)/2} = \left(\sum_{k \ge 0} p^{-k/2}\right)^2 - \sum_{k \ge 0} p^{-k} = (1 - p^{-1/2})^{-2} - (1 - p^{-1})^{-1} = \frac{2 p^{-1/2}}{(1 - p^{-1})(1 - p^{-1/2})} < 2 p^{-1/2}(1 - p^{-1/2})^{-2}$. Multiplying $\left(\sum_{m \in \mathcal{S}(P_{< p})} m^{-1/2}\right)^2 = \prod_{q < p}(1 - q^{-1/2})^{-2}$ by $(1 - p^{-1/2})^{-2}$ produces $\prod_{q \le p}(1 - q^{-1/2})^{-2} \le \prod_{q < 2 B}(1 - q^{-1/2})^{-2}$, proving (1).
2. Assume $B > \sqrt{T}$, so $B^2 > T$. For any $1 \le r \le T$ coprime to $N_{P_{< B}}$, every prime factor of $r$ is $\ge B$. Since the product of any two primes $\ge B$ exceeds $B^2 > T \ge r$, either $r = 1$ (giving fiber $F_{P_{< B}, 1}(X) = S_{< B, T}(X)$) or $r = p$ is a single prime in $[B, T]$, in which case every $m \in \mathcal{S}(P_{< B})$ with $m \le \lfloor T / p \rfloor < T / \sqrt{T} = \sqrt{T} < B$ is automatically $P_{< B}$-smooth! Thus for $r = p \in [B, T]$, $F_{P_{< B}, p}(X) = -\frac{1}{\sqrt{p}} Q_{\lfloor T / p \rfloor}(X / p)$. Applying this to both $U = B$ and $U = 2 B$ ($> \sqrt{T}$),
   $$V_{P_{< B}}(Y, T) = \|S_{< B, T}\|_{L^2}^2 + \sum_{\substack{B \le p \le T \\ p \text{ prime}}} \frac{1}{p}\int_Y^{\tau Y} Q_{\lfloor T / p \rfloor}\!\left(\frac{X}{p}\right)^2\frac{dX}{X},$$
   and subtracting from $V_{P_{< 2 B}}(Y, T)$ cancels all primes $p \ge 2 B$, yielding (2) identically.
3. For $B > \sqrt{T}$, write $H_j(X) := S_{< 2 B, T}(X) - S_{< B, T}(X)$. Every $n \le T$ in $\mathcal{S}(P_{< 2 B}) \setminus \mathcal{S}(P_{< B})$ has a unique prime divisor $p \in I_j(Y)$, and its cofactor $k = n / p \le \lfloor T / p \rfloor < \sqrt{T} < B$ is automatically $P_{< B}$-smooth, so $H_j(X) = -\sum_{p \in I_j(Y)} \sum_{1 \le k \le \lfloor T / p \rfloor} \lambda(k)\varphi_{p k}(X)$. Hence for $X \in [Y, \tau Y]$,
   $$|H_j(X)| \le X^{5/2}\sum_{p \in I_j(Y)} p^{-3} \sum_{1 \le k \le \lfloor T / p \rfloor} k^{-3} \le \zeta(3) X^{5/2} \sum_{p \in I_j(Y)} p^{-3}.$$
   Meanwhile both $|S_{< B, T}(X)|$ and $|S_{< 2 B, T}(X)|$ are bounded by $Q_{\mathbf{1}}(X) \le M_{\mathbf{1}}\sqrt{X}$ (Proposition 2.1(3)), so $|S_{< 2 B, T}(X) + S_{< B, T}(X)| \le 2 M_{\mathbf{1}}\sqrt{X}$. Since the subtracted diagonal prime-fiber sum in (2) is $\ge 0$, retaining its negativity gives the one-sided bound
   $$M_j(Y) - C_j(Y) \le \int_Y^{\tau Y} |H_j(X)|\,|S_{< 2 B, T}(X) + S_{< B, T}(X)|\,\frac{dX}{X} \le 2\zeta(3) M_{\mathbf{1}} \left(\sum_{p \in I_j(Y)} p^{-3}\right) \int_Y^{\tau Y} X^2\,dX = C_{\mathrm{top}} Y^3 \sum_{p \in I_j(Y)} p^{-3}.$$
   Similarly, for the subtracted prime-fiber sum, $|Q_{\lfloor T/p \rfloor}(X/p)| \le Q_{\mathbf{1}}(X/p) \le \zeta(3)(X/p)^{5/2}$, so $\frac{1}{p}\int_Y^{\tau Y} Q_{\lfloor T/p \rfloor}(X/p)^2\frac{dX}{X} \le \zeta(3)^2 \frac{\tau^5 - 1}{5} Y^5 p^{-6}$, and even more simply $\frac{1}{p}\int_Y^{\tau Y} |Q_{\lfloor T/p \rfloor}(X/p)|\,M_{\mathbf{1}}\sqrt{X/p}\frac{dX}{X} \le \frac{1}{2} C_{\mathrm{top}} Y^3 p^{-4} < \frac{1}{2} C_{\mathrm{top}} Y^3 p^{-3}$, giving $|M_j(Y) - C_j(Y)| \le \frac{3}{2} C_{\mathrm{top}} Y^3 \sum_{p \in I_j(Y)} p^{-3}$. $\blacksquare$

### 8.3 Theorem 8.C — Unconditional PNT Refutation of the Localized Single-Block Subpower Conjecture

We now resolve the primary localized single-block conjecture ($M_j(Y) - C_j(Y) \le A_\delta Y^\delta$ for all $Y \ge 1, j \ge 1$) by proving that it is **unconditionally false for every $\delta \in (0, 1)$**.

For $\kappa > 0$ and $u \in [1, \tau]$, define the smooth-cutoff profile and its $L^2([1, \tau], du/u)$ surge constant:
$$\mathcal{C}_\kappa(u) := \int_\kappa^\infty Q_\lambda\!\left(\frac{u}{v}\right)\frac{dv}{v^{1/2}} = \sum_{n = 1}^\infty \lambda(n) u^{5/2} n^{-3} \int_\kappa^\infty v^{-3} e^{-u^2 / (v^2 n^2)}\,dv = \frac{\sqrt{u}}{2} \sum_{n = 1}^\infty \frac{\lambda(n)}{n}\left(1 - \exp\!\left(-\frac{u^2}{\kappa^2 n^2}\right)\right)$$
(by substituting $z = u / (v n)$, $dz = -u (v^2 n)^{-1} dv$, $z\,dz = -u^2 v^{-3} n^{-2} dv$, $\int_0^{u/(\kappa n)} z e^{-z^2}\,dz = \frac{1}{2}(1 - e^{-u^2/(\kappa^2 n^2)})$), and
$$\mathcal{I}(\kappa) := \int_1^\tau \mathcal{C}_\kappa(u)^2\,\frac{du}{u} = \frac{1}{4}\int_1^\tau \left(\sum_{n = 1}^\infty \frac{\lambda(n)}{n}\left(1 - \exp\!\left(-\frac{u^2}{\kappa^2 n^2}\right)\right)\right)^2 du.$$
Certified 256-bit Arb enclosures (`evaluate_smooth_cutoff_surge_I_kappa_arb` with $N_0 = 2400$ terms plus rigorous tail bound $\le \frac{G_{\sup}(\tau^3-1)}{12 \kappa^2 N_0^2} + \frac{\tau^5 - 1}{80 \kappa^4 N_0^4}$) give:
- $\mathcal{I}(1/2) \in [0.0973 \pm 1.50 \times 10^{-5}]$, <!-- tc-enclosure: observable="I_half" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8C_refutation_of_localized_single_block_subpower_conjecture.I_half" -->
- $\mathcal{I}(1) \in [0.21584 \pm 5.00 \times 10^{-6}]$, <!-- tc-enclosure: observable="I_one" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8C_refutation_of_localized_single_block_subpower_conjecture.I_one" -->
- $\mathcal{I}(2) \in [0.33487 \pm 2.00 \times 10^{-6}]$, <!-- tc-enclosure: observable="I_two" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8C_refutation_of_localized_single_block_subpower_conjecture.I_two" -->
- $\mathcal{I}(4) \in [0.262736 \pm 3.00 \times 10^{-7}]$, <!-- tc-enclosure: observable="I_four" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8C_refutation_of_localized_single_block_subpower_conjecture.I_four" -->
with strictly positive consecutive surges near $p \asymp Y$ and a compensating negative drop above $2 Y$:
- $\mathcal{I}(1) - \mathcal{I}(1/2) \in [0.1185 \pm 6.00 \times 10^{-5}] > 0$, <!-- tc-enclosure: observable="I_one_minus_I_half_positive_surge" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8C_refutation_of_localized_single_block_subpower_conjecture.I_one_minus_I_half_positive_surge" -->
- $\mathcal{I}(2) - \mathcal{I}(1) \in [0.11903 \pm 6.00 \times 10^{-6}] > 0$, <!-- tc-enclosure: observable="I_two_minus_I_one_positive_surge" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8C_refutation_of_localized_single_block_subpower_conjecture.I_two_minus_I_one_positive_surge" -->
- $\mathcal{I}(4) - \mathcal{I}(2) \in [-0.07213 \pm 5.00 \times 10^{-6}] < 0$. <!-- tc-enclosure: observable="I_four_minus_I_two_negative_compensating_drop" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8C_refutation_of_localized_single_block_subpower_conjecture.I_four_minus_I_two_negative_compensating_drop" -->

**Theorem 8.C (Unconditional Refutation of the Localized Single-Block Subpower Conjecture).**
1. **Unconditional PNT Rough-Tail Asymptotic**: *Fix $\kappa > 0$. For all sufficiently large $Y$ such that $\kappa Y > \sqrt{T(Y)}$ (which holds for all $Y > (2 / \kappa^2)^4$), let $H_{[\kappa Y, T(Y)]}(X) := S_{< \kappa Y, T(Y)}(X) - Q_{T(Y)}(X)$. Then uniformly for $u \in [1, \tau]$,*
   $$H_{[\kappa Y, T(Y)]}(Y u) = \frac{\sqrt{Y}}{\log Y}\,\mathcal{C}_\kappa(u) + O_\kappa\!\left(\frac{\sqrt{Y}}{(\log Y)^2}\right),$$
   *and hence*
   $$\|H_{[\kappa Y, T(Y)]}\|_{L^2([Y, \tau Y], dX/X)}^2 = \mathcal{I}(\kappa)\,\frac{Y}{(\log Y)^2} + O_\kappa\!\left(\frac{Y}{(\log Y)^3}\right).$$
2. **Unconditional Refutation for Every $\delta \in (0, 1)$**: *There does **not** exist any $\delta_0 \in (0, 1)$ and constant $A_{\delta_0} < \infty$ such that $M_j(Y) - C_j(Y) \le A_{\delta_0} Y^{\delta_0}$ holds for all $Y \ge 1$ and all $j \ge 1$. Indeed, along the dyadic sequence $Y_k := 2^k$ at block index $j = k$ ($B = 2^k = Y_k$), if such a bound held for $\delta_0 \in (0, 1)$, it would force*
   $$M_k(Y_k) - C_k(Y_k) = \left(\mathcal{I}(2) - \mathcal{I}(1) + o(1)\right)\frac{Y_k}{(\log Y_k)^2} \ge 0.1189\,\frac{Y_k}{(\log Y_k)^2},$$
   *contradicting $M_k(Y_k) - C_k(Y_k) \le A_{\delta_0} Y_k^{\delta_0}$ as $k \to \infty$. (For the same reason, even under RH, $M_k(Y_k) - C_k(Y_k) \sim (\mathcal{I}(2) - \mathcal{I}(1)) Y_k / (\log Y_k)^2 \gg Y_k / (\log Y_k)^2$!)*

*Proof.*
- **Step 1 (Exact prime-cofactor formula for $H_{[\kappa Y, T]}$)**: For $\kappa Y > \sqrt{T}$, every integer $1 \le n \le T$ NOT in $\mathcal{S}(P_{< \kappa Y})$ has a unique prime divisor $q \in [\kappa Y, T]$, and its cofactor $m = n / q \le \lfloor T / q \rfloor < \sqrt{T} < \kappa Y$ has all prime factors $< \kappa Y$. Since $\lambda(q m) = -\lambda(m)$ and $\varphi_{q m}(X) = q^{-1/2}\varphi_m(X / q)$,
  $$H_{[\kappa Y, T]}(X) = -\sum_{\substack{1 \le n \le T \\ n \notin \mathcal{S}(P_{< \kappa Y})}} \lambda(n)\varphi_n(X) = \sum_{\kappa Y \le q \le T} \frac{1}{\sqrt{q}}\,Q_{\lfloor T / q \rfloor}\!\left(\frac{X}{q}\right)$$
  (where $q$ runs over primes).
- **Step 2 (Inner cofactor truncation $\lfloor T / q \rfloor \to \infty$ costs $O(1)$ uniformly on $u \in [1, \tau]$)**: For $X = Y u$ ($u \in [1, \tau]$) and $q \le T = \lceil Y^{5/4} \rceil$, writing $L_q := \lfloor T / q \rfloor \ge 1$, the omitted inner tail satisfies
  $$\left|Q_\lambda\!\left(\frac{Y u}{q}\right) - Q_{L_q}\!\left(\frac{Y u}{q}\right)\right| \le (Y u / q)^{5/2} \sum_{m > T / q} m^{-3} \le (\tau Y / q)^{5/2} \cdot \frac{1}{2 (T / q - 1)^2}$$
  for $q \le T / 2$ (and for $T / 2 < q \le T$, $Y / q \le 2 Y / T \le 2 Y^{-1/4}$, so $\sum_{m > L_q} \varphi_m(Y u / q) \le \zeta(3)(\tau Y / q)^{5/2} \ll Y^{-5/8}$). Summing $q^{-1/2}$ times this error over $\kappa Y \le q \le T$: for $\kappa Y \le q \le T / 2$, $T / q - 1 \ge T / (2 q)$, giving $q^{-1/2}(Y/q)^{5/2}(q/T)^2 = Y^{5/2} T^{-2} q^{-1} \le Y^0 q^{-1}$, whose prime sum over $\kappa Y \le q \le T / 2$ is $\ll_\kappa \log(T / Y) / \log Y \ll_\kappa 1$; for $T / 2 < q \le T$, $\sum_{T/2 < q \le T} q^{-1/2} Y^{-5/8} \ll T^{1/2} (\log T)^{-1} Y^{-5/8} = O(1 / \log Y)$.
- **Step 3 (Outer prime tail $q > T$ costs $O(1)$ uniformly on $u \in [1, \tau]$)**: For $q > T \ge Y^{5/4}$ and $u \in [1, \tau]$, $Y u / q < \tau$, so $|Q_\lambda(Y u / q)| \le \zeta(3)(\tau Y / q)^{5/2}$, and $\sum_{q > T} q^{-1/2}|Q_\lambda(Y u / q)| \ll Y^{5/2} \sum_{n > Y^{5/4}} n^{-3} \ll Y^{5/2} (Y^{5/4})^{-2} = O(1)$.
- **Step 4 (Stieltjes representation and uniform derivative bound)**: Combining Steps 1–3 gives uniformly on $u \in [1, \tau]$:
  $$H_{[\kappa Y, T(Y)]}(Y u) = \sum_{q \ge \kappa Y} \frac{1}{\sqrt{q}}\,Q_\lambda\!\left(\frac{Y u}{q}\right) + O_\kappa(1).$$
  Set $\Psi_u(v) := v^{-1/2} Q_\lambda(u / v)$ for $v \ge \kappa$. By termwise differentiation of $Q_\lambda(w) = \sum_{n \ge 1}\lambda(n) w^{5/2} n^{-3} e^{-w^2/n^2}$, both $|Q_\lambda(w)|$ and $|w Q_\lambda'(w)|$ are $\ll \min(w^{5/2}, \sqrt{w})$ for all $w > 0$ (using $M_{\mathbf{1}}\sqrt{w}$ for $w \ge 1$ and $O(w^{5/2})$ for $0 < w < 1$). Since $u \in [1, \tau]$, for $v \ge \kappa$ we have $|\Psi_u(v)| \ll_\kappa \min(v^{-1}, v^{-3})$ and $|\Psi_u'(v)| = |-\frac{1}{2} v^{-3/2} Q_\lambda(u/v) - u v^{-5/2} Q_\lambda'(u/v)| \ll_\kappa \min(v^{-2}, v^{-4})$, so $\int_\kappa^\infty |\Psi_u'(v)|\,dv \ll_\kappa 1$ and $\int_\kappa^\infty v\,|\Psi_u'(v)|(\log(2 + v))^{-2}\,dv \ll_\kappa 1$ uniformly in $u \in [1, \tau]$.
- **Step 5 (Unconditional Prime Number Theorem)**: Writing the prime-counting function as $\vartheta_0(t) := \#\{q \text{ prime} : q \le t\} = \operatorname{li}(t) + R_{\mathrm{PNT}}(t)$ with classical unconditional de la Vallée Poussin error $R_{\mathrm{PNT}}(t) \ll t\exp(-c_0\sqrt{\log t}) \ll t / (\log t)^3$ ($t \ge 2$), Stieltjes integration by parts on $t = Y v \ge \kappa Y$ gives
  $$\sum_{q \ge \kappa Y} \frac{1}{\sqrt{Y}}\Psi_u\!\left(\frac{q}{Y}\right) = \sqrt{Y}\int_\kappa^\infty \frac{\Psi_u(v)}{\log(Y v)}\,dv - \frac{R_{\mathrm{PNT}}((\kappa Y)^-)}{\sqrt{Y}}\Psi_u(\kappa) - \frac{1}{\sqrt{Y}}\int_\kappa^\infty R_{\mathrm{PNT}}(Y v)\Psi_u'(v)\,dv.$$
  Expanding $\frac{1}{\log(Y v)} = \frac{1}{\log Y} - \frac{\log v}{(\log Y)\log(Y v)} = \frac{1}{\log Y} + O_\kappa\!\left(\frac{1 + |\log v|}{(\log Y)^2}\right)$ (since $\int_\kappa^\infty |\Psi_u(v)|(1 + |\log v|)\,dv \ll_\kappa 1$) and bounding the $R_{\mathrm{PNT}}$ boundary and integral terms by $O_\kappa(\sqrt{Y} / (\log Y)^3)$ yields $H_{[\kappa Y, T(Y)]}(Y u) = \frac{\sqrt{Y}}{\log Y}\mathcal{C}_\kappa(u) + O_\kappa\!\left(\frac{\sqrt{Y}}{(\log Y)^2}\right)$ uniformly on $u \in [1, \tau]$. Squaring and integrating against $du / u$ on $[1, \tau]$ proves (1).
- **Step 6 (Proof by contradiction of (2))**: Suppose $M_j(Y) - C_j(Y) \le A_{\delta_0} Y^{\delta_0}$ held for all $Y \ge 1, j \ge 1$ for some $\delta_0 \in (0, 1)$. Summing over all $J_{\max}(Y) = O(1 + \log Y)$ blocks as in Theorem 8.A gives $\|Q_{T(Y)}\|_{L^2}^2 = E_{T(Y)}(Y) \ll_{\delta_0} Y^{\delta_0}\log(2 Y)$, so $\|Q_{T(Y)}\|_{L^2} \ll_{\delta_0} Y^{\delta_0 / 2}\sqrt{\log(2 Y)} = o\!\left(\frac{\sqrt{Y}}{\log Y}\right)$ because $\delta_0 < 1$. Since $S_{< \kappa Y, T(Y)} = Q_{T(Y)} + H_{[\kappa Y, T(Y)]}$, Cauchy–Schwarz gives
  $$\|S_{< \kappa Y, T(Y)}\|_{L^2}^2 = \|H_{[\kappa Y, T(Y)]}\|_{L^2}^2 + O\!\left(\|Q_{T(Y)}\|_{L^2}\|H_{[\kappa Y, T(Y)]}\|_{L^2} + \|Q_{T(Y)}\|_{L^2}^2\right) = \left(\mathcal{I}(\kappa) + o(1)\right)\frac{Y}{(\log Y)^2}.$$
  Also, for the diagonal prime-fiber term in Theorem 8.B(2) on $I_k(Y_k) = [Y_k, 2 Y_k) \cap \mathbb{P}$ ($Y_k = 2^k$, $k \ge 5$, so $B = Y_k > \sqrt{T(Y_k)}$), each $p \in [Y_k, 2 Y_k)$ has $X / p \in [1/2, \tau]$, so $\frac{1}{p}\int_{Y_k}^{\tau Y_k} Q_{\lfloor T/p \rfloor}(X/p)^2\frac{dX}{X} \ll \frac{1}{p}$, and by Chebyshev/Mertens $\sum_{Y_k \le p < 2 Y_k} \frac{1}{p} \ll \frac{1}{\log Y_k} = o\!\left(\frac{Y_k}{(\log Y_k)^2}\right)$. Substituting $\kappa = 2$ and $\kappa = 1$ into Theorem 8.B(2) at $Y = Y_k, B = Y_k$ ($j = k$) therefore forces
  $$M_k(Y_k) - C_k(Y_k) = \|S_{< 2 Y_k, T(Y_k)}\|_{L^2}^2 - \|S_{< Y_k, T(Y_k)}\|_{L^2}^2 - O\!\left(\frac{1}{\log Y_k}\right) = \left(\mathcal{I}(2) - \mathcal{I}(1) + o(1)\right)\frac{Y_k}{(\log Y_k)^2}.$$
  Since $\mathcal{I}(2) - \mathcal{I}(1) > 0.11902 > 0.1189 > 0$ is certified positive, for large $k$ this exceeds $0.1189 Y_k / (\log Y_k)^2$, contradicting $M_k(Y_k) - C_k(Y_k) \le A_{\delta_0} Y_k^{\delta_0}$ ($\delta_0 < 1$). $\blacksquare$

### 8.4 Theorem 8.D — Compensated Multi-Block Grouping Across Super-$\sqrt{T}$ Bands & Surviving Research Target

Theorem 8.C reveals *why* isolated dyadic blocks near $B \asymp Y$ surge positively while blocks above $2 Y$ drop negatively ($\mathcal{I}(4) - \mathcal{I}(2) \approx -0.07213 < 0$): each single block $I_j(Y)$ introduces the artificial sharp prime-smoothness boundary $\pm\|S_{< 2^j, T}\|_{L^2}^2$, whose rough tail $H_{[2^j, T]}$ has size $\asymp \sqrt{Y}/\log Y$ even if $Q_T$ itself cancels! Grouping **all** blocks above an intermediate threshold $U_0(Y) > \sqrt{T(Y)}$ cancels every intermediate $\pm\|S_{< 2^j, T}\|_{L^2}^2$ boundary identically.

**Theorem 8.D (Compensated Multi-Block Super-$\sqrt{T}$ Telescoping, Coupled Buchstab Defect, and Surviving Mixed-Prime Reduction).** *For $Y \ge 1$ and $T = T(Y) = \lceil Y^{5/4} \rceil$, set $U_0(Y) := \lceil 2 Y^{5/8} \rceil$ (so $U_0(Y)^2 \ge 4 Y^{5/4} > T(Y)$, i.e., $U_0(Y) > \sqrt{T(Y)}$ for every $Y \ge 1$). Then:*
1. **Exact Multi-Block Cancellation of Intermediate Smooth-Cutoff Surges**: *Summing $\Delta_p(Y, T) = M_p(Y, T) - C_p(Y, T)$ over the entire super-$\sqrt{T}$ band $U_0(Y) \le p \le T$ cancels every intermediate dyadic boundary surge $\pm\|S_{< 2^j, T}\|_{L^2}^2$ ($U_0(Y) < 2^j \le T$) identically:*
   $$\sum_{U_0(Y) \le p \le T} \left(M_p(Y, T) - C_p(Y, T)\right) = E_T(Y) - \|S_{< U_0(Y), T}\|_{L^2([Y, \tau Y], dX/X)}^2 - \mathcal{R}_{\mathrm{diag\text{-}fib}}(Y; U_0(Y), T),$$
   *or equivalently, writing $H_{[U_0(Y), T]}(X) := \sum_{U_0(Y) \le p \le T} \frac{1}{\sqrt{p}}\,Q_{\lfloor T / p \rfloor}\!\left(\frac{X}{p}\right)$ so $Q_T(X) = S_{< U_0(Y), T}(X) - H_{[U_0(Y), T]}(X)$,*
   $$E_T(Y) = \|S_{< U_0(Y), T}\|_{L^2}^2 + \mathcal{R}_{\mathrm{diag\text{-}fib}}(Y; U_0(Y), T) + \sum_{U_0(Y) \le p \le T} \left(M_p(Y, T) - C_p(Y, T)\right) = \bigl\|S_{< U_0(Y), T} - H_{[U_0(Y), T]}\bigr\|_{L^2([Y, \tau Y], dX/X)}^2,$$
   *where the diagonal prime-fiber sum satisfies unconditionally*
   $$0 \le \mathcal{R}_{\mathrm{diag\text{-}fib}}(Y; U_0(Y), T) := \sum_{U_0(Y) \le p \le T} \frac{1}{p}\int_Y^{\tau Y} Q_{\lfloor T / p \rfloor}\!\left(\frac{X}{p}\right)^2\frac{dX}{X} \le (\tau - 1) M_{\mathbf{1}}^2 Y \sum_{p \ge 2 Y^{5/8}} p^{-2} \ll \frac{Y^{3/8}}{\log(2 Y)}$$
   *(and $\ll_\varepsilon Y^{3\varepsilon / 8}$ under $E_L(W) \ll_\varepsilon W^\varepsilon$, while on $p \ge Y$ it is unconditionally $\ll 1 / \log(2 Y) = O(1)$).*
2. **Simultaneous Sub-$U_0(Y)$ Mixed Expansion & Why $S_{< U_0(Y), T}$ and $H_{[U_0(Y), T]}$ Cannot Be Uncoupled**: *Simultaneously, expanding $V_{P_{< U_0(Y)}}(Y, T)$ from $V_\varnothing(Y, T) = D_T(Y)$ gives*
   $$\|S_{< U_0(Y), T}\|_{L^2}^2 + \mathcal{R}_{\mathrm{diag\text{-}fib}}(Y; U_0(Y), T) = D_T(Y) + \sum_{p < U_0(Y)} M_p(Y, T) - \sum_{p < U_0(Y)} C_p(Y, T).$$
   *Crucially, one **cannot** drop $\sum_{U_0(Y) \le p \le T}(M_p - C_p)$ to claim $E_T(Y) \le \|S_{< U_0(Y), T}\|_{L^2}^2$, nor uncouple $S_{< U_0(Y), T(Y)}$ from $H_{[U_0(Y), T(Y)]}$: because $\mathcal{M}[Q_\lambda](z) = \frac{\zeta(1 + 2 z)}{2\zeta(1/2 + z)}\Gamma(5/4 - z/2)$ satisfies $\mathcal{M}[Q_\lambda](1/2) = 0$ (annihilating the $(\log Y)^{-1}$ PNT term) while $\mathcal{M}[Q_\lambda]'(1/2) = \frac{\zeta(2)}{2} = \frac{\tau^2}{48} \ne 0$, under RH both $H_{[U_0(Y), T(Y)]}(X)$ and $S_{< U_0(Y), T(Y)}(X) = Q_{T(Y)}(X) + H_{[U_0(Y), T(Y)]}(X)$ carry the common Buchstab smooth-cutoff defect $-\frac{\tau^2}{48}\frac{\sqrt{X}}{(\log X)^2}(1 + o(1))$ with $L^2([Y, \tau Y], dX/X)$ norm squared $\sim \frac{(\tau - 1)\tau^4}{2304}\frac{Y}{(\log Y)^4} \not\ll_\varepsilon Y^\varepsilon$ ($\varepsilon \in (0, 1)$), which cancels **only** in the coupled difference $S_{< U_0(Y), T(Y)} - H_{[U_0(Y), T(Y)]}$.*
3. **Unconditional Reduction of `SUBGATE-TC-043A`**: *Define $U_{\mathrm{log}, \delta}(Y) := \frac{\delta^2}{32}(\log Y \log\log Y)^2$ for $Y \ge e^e$ and $U_{\mathrm{log}, \delta}(Y) := 1$ for $1 \le Y < e^e$. Combining Theorems 6.1 ($\sum_{p \le T} C_p < 1$) and 8.B(1) (low primes $p \le U_{\mathrm{log},\varepsilon/4}(Y)$), for **every** $\varepsilon > 0$, $E_{T(Y)}(Y) \ll_\varepsilon Y^\varepsilon$ holds across all $Y \ge 1$ **if and only if** the coupled multi-block mixed-interaction sum across $U_{\mathrm{log},\varepsilon/4}(Y) < p \le T(Y)$ satisfies*
   $$\sum_{U_{\mathrm{log},\varepsilon / 4}(Y) < p \le T(Y)} M_p(Y, T(Y)) \le C_\varepsilon' Y^\varepsilon \qquad \left(\text{equivalently } \bigl\|S_{< U_0(Y), T(Y)} - H_{[U_0(Y), T(Y)]}\bigr\|_{L^2([Y, \tau Y], dX/X)}^2 \ll_\varepsilon Y^\varepsilon\right),$$
   *where on the upper sub-band $Y^{1 + \theta} \le p \le T(Y)$ ($0 < \theta \le 1/4$), Theorem 8.B(3) already unconditionally improves the trivial $O(Y)$ scale to $O\!\left(\frac{Y^{1 - 2\theta}}{\log Y}\right)$ (reaching $O\!\left(\frac{Y^{1/2}}{\log Y}\right)$ near $p \asymp T(Y)$, which unconditionally closes $p \ge Y^{1 + \theta}$ whenever $\varepsilon \ge 1 - 2\theta$, while still requiring signed cancellation from $Y^{1/2}/\log Y$ down to $Y^\varepsilon$ when $0 < \varepsilon < 1/2$).*

*Proof.* Since $U_0(Y) > \sqrt{T(Y)}$, the single-prime cofactor classification from the proof of Theorem 8.B(2) applies directly to $P_{< U_0(Y)}$: every $1 \le r \le T$ coprime to $N_{P_{< U_0(Y)}}$ is either $r = 1$ (fiber $S_{< U_0(Y), T}$) or a single prime $r = p \in [U_0(Y), T]$ (fiber $-p^{-1/2} Q_{\lfloor T / p \rfloor}(X / p)$), so $Q_T(X) = S_{< U_0(Y), T}(X) - H_{[U_0(Y), T]}(X)$ and $V_{P_{< U_0(Y)}}(Y, T) = \|S_{< U_0(Y), T}\|_{L^2}^2 + \mathcal{R}_{\mathrm{diag\text{-}fib}}(Y; U_0(Y), T)$. Subtracting $V_{P_{< U_0(Y)}}(Y, T)$ from $V_{\{\text{primes } \le T\}}(Y, T) = E_T(Y)$ gives (1), and equating $V_{P_{< U_0(Y)}}(Y, T)$ with $D_T(Y) + \sum_{p < U_0(Y)}(M_p - C_p)$ gives the first part of (2). For the unconditional bound on $\mathcal{R}_{\mathrm{diag\text{-}fib}}$, $|Q_L(w)| \le Q_{\mathbf{1}}(w) \le M_{\mathbf{1}}\sqrt{w}$ gives $\frac{1}{p}\int_Y^{\tau Y} Q_{\lfloor T / p \rfloor}(X / p)^2\frac{dX}{X} \le (\tau - 1) M_{\mathbf{1}}^2 \frac{Y}{p^2}$, whose sum over $p \ge U_0(Y) \ge 2 Y^{5/8}$ is $\ll Y^{3/8} / \log(2 Y)$. Under RH, $Q_\lambda(w) \ll_\delta w^\delta$ as $w \to \infty$ and $O(w^{5/2})$ as $w \to 0^+$, so $\int_0^\infty Q_\lambda(w) w^{-3/2}\,dw = \mathcal{M}[Q_\lambda](1/2) = 0$ and $\int_0^\infty Q_\lambda(w) w^{-3/2}\log w\,dw = -\mathcal{M}[Q_\lambda]'(1/2) = -\frac{\tau^2}{48}$ converge absolutely; expanding $\frac{1}{\log X - \log w} = \frac{1}{\log X} + \frac{\log w}{(\log X)^2} + O\!\left(\frac{(\log w)^2}{(\log X)^3}\right)$ in the PNT Stieltjes integral for $H_{[U_0(Y), T(Y)]}(X)$ yields $H_{[U_0(Y), T(Y)]}(X) = -\frac{\tau^2}{48}\frac{\sqrt{X}}{(\log X)^2}(1 + o(1))$. Finally, (3) follows across all $Y \ge 1$ and all $\varepsilon > 0$ from $E_{T(Y)}(Y) = D_{T(Y)}(Y) + \sum_{p \le T(Y)} M_p(Y, T(Y)) - \sum_{p \le T(Y)} C_p(Y, T(Y))$ because $0 \le D_{T(Y)}(Y) \le B_D$, $0 \le \sum_{p \le T(Y)} C_p(Y, T(Y)) < 1$ (Theorem 6.1), and $\left|\sum_{p \le U_{\mathrm{log},\varepsilon/4}(Y)} M_p(Y, T(Y))\right| \ll_\varepsilon Y^{\varepsilon/4}\log(2 Y) \ll_\varepsilon Y^\varepsilon$ (Theorem 8.B(1), with the sum empty on $1 \le Y < e^e$ since $U_{\mathrm{log},\varepsilon/4}(Y) = 1 < 2$). $\blacksquare$

At the Counterexample 7b benchmark $(Y = 128, T = 431)$, across all four super-$\sqrt{T}$ dyadic blocks $B \in \{32, 64, 128, 256\}$ ($32 \le p < 512$):
- $B = 32$ ($32 \le p < 64$): $M_j - C_j \in [0.04957153628931205582927811663203664553798 \pm 1.00 \times 10^{-42}]$, <!-- tc-enclosure: observable="M_j_minus_C_j" params="B=32; two_B=64" json_path="section_8_mixed_prime_block_attempt.theorem_8B_unconditional_low_and_top_block_bounds.super_sqrt_T_block_rows_Y128_T431[B=32].M_j_minus_C_j" -->
- $B = 64$ ($64 \le p < 128$): $M_j - C_j \in [0.1922515942217511282452862066402187681259 \pm 4.00 \times 10^{-41}]$, <!-- tc-enclosure: observable="M_j_minus_C_j" params="B=64; two_B=128" json_path="section_8_mixed_prime_block_attempt.theorem_8B_unconditional_low_and_top_block_bounds.super_sqrt_T_block_rows_Y128_T431[B=64].M_j_minus_C_j" -->
- $B = 128$ ($128 \le p < 256$): $M_j - C_j \in [-0.1192644894628990530954269698892376230976 \pm 4.00 \times 10^{-41}]$, <!-- tc-enclosure: observable="M_j_minus_C_j" params="B=128; two_B=256" json_path="section_8_mixed_prime_block_attempt.theorem_8B_unconditional_low_and_top_block_bounds.super_sqrt_T_block_rows_Y128_T431[B=128].M_j_minus_C_j" -->
- $B = 256$ ($256 \le p \le 431$): $M_j - C_j \in [-0.1406610767695817963999553626510739123310 \pm 4.00 \times 10^{-41}]$, <!-- tc-enclosure: observable="M_j_minus_C_j" params="B=256; two_B=512" json_path="section_8_mixed_prime_block_attempt.theorem_8B_unconditional_low_and_top_block_bounds.super_sqrt_T_block_rows_Y128_T431[B=256].M_j_minus_C_j" -->
whose compensated four-block sum cancels the $+0.19225\dots$ surge completely to a **net negative** contribution:
$$\sum_{32 \le p \le 431} \left(M_p(128, 431) - C_p(128, 431)\right) \in [-0.01810243572141766542081800926805612176476 \pm 2.00 \times 10^{-42}] < 0,$$ <!-- tc-enclosure: observable="compensated_4_block_sum_32_to_512" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8D_compensated_multi_block_telescoping.band_Y128_T431_B_minus_32_B_plus_512.compensated_4_block_sum_32_to_512" -->
while simultaneously certifying that $E_{431}(128)$ strictly exceeds both $\|S_{< 32, 431}\|_{L^2}^2 \in [0.001737253754240212303546347476593669142890 \pm 1.00 \times 10^{-43}]$ <!-- tc-enclosure: observable="S_lt_32_norm_sq" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8D_compensated_multi_block_telescoping.band_Y128_T431_B_minus_32_B_plus_512.S_lt_32_norm_sq" -->
and $\|S_{< 42, 431}\|_{L^2}^2 \in [0.006663989767472066563366985999866433625271 \pm 2.00 \times 10^{-43}]$ <!-- tc-enclosure: observable="S_lt_42_U0_128_norm_sq" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8D_compensated_multi_block_telescoping.band_Y128_T431_B_minus_32_B_plus_512.S_lt_42_U0_128_norm_sq" -->
($U_0(128) = \lceil 2 \cdot 128^{5/8} \rceil = 42$, with $E_{431}(128) - \|S_{< 32, 431}\|_{L^2}^2 \in [0.02189533808774263459214777646954886306932 \pm 5.00 \times 10^{-43}] > 0$ <!-- tc-enclosure: observable="E_431_minus_S_lt_32_positive_gap" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8D_compensated_multi_block_telescoping.band_Y128_T431_B_minus_32_B_plus_512.E_431_minus_S_lt_32_positive_gap" -->
and $E_{431}(128) - \|S_{< 42, 431}\|_{L^2}^2 \in [0.01696860207451078033232713794627609858694 \pm 6.00 \times 10^{-43}] > 0$), <!-- tc-enclosure: observable="E_431_minus_S_lt_42_positive_gap" params="precision_bits=256" json_path="section_8_mixed_prime_block_attempt.theorem_8D_compensated_multi_block_telescoping.band_Y128_T431_B_minus_32_B_plus_512.E_431_minus_S_lt_42_positive_gap" -->
confirming that the super-$U_0$ band sum in Theorem 8.D(1) cannot be dropped.

### 8.5 Exact Surviving Coupled Mixed-Prime Sum and Missing Saving

Combining Theorems 6.1, 8.B, 8.C, and 8.D isolates the exact surviving mathematical obligation for `SUBGATE-TC-043A`:
- **Eliminated regimes and falsified localized shortcuts**:
  1. Total singleton contraction $\sum_{p \le T(Y)} C_p(Y, T(Y)) < 0.8246 < 1$ is uniformly bounded across all $Y \ge 1, T \ge 0$ (Theorem 6.1).
  2. Low-prime mixed interactions $p \le U_{\mathrm{log},\delta}(Y)$ ($U_{\mathrm{log},\delta}(Y) = \frac{\delta^2}{32}(\log Y \log\log Y)^2$ for $Y \ge e^e$ and $1$ for $1 \le Y < e^e$) satisfy $\left|\sum_{p \le U_{\mathrm{log},\delta}(Y)} M_p(Y, T(Y))\right| \ll_\delta Y^\delta\log(2 Y)$ unconditionally (Theorem 8.B(1)), and super-transition blocks $2^j \ge Y^{1 + \theta}$ ($0 < \theta \le 1/4$) satisfy $|M_j(Y) - C_j(Y)| \ll \frac{Y^{1 - 2\theta}}{\log Y}$ unconditionally (Theorem 8.B(3), reaching $O(Y^{1/2}/\log Y)$ near $p \asymp T(Y)$).
  3. Blockwise subpower bounds $M_j(Y) - C_j(Y) \le A_\delta Y^\delta$ ($\delta \in (0, 1)$) are **unconditionally false** due to the smooth-cutoff surge $(\mathcal{I}(2) - \mathcal{I}(1))\frac{Y}{(\log Y)^2}$ at $B \asymp Y$ (Theorem 8.C), and uncoupled smooth-cutoff bounds $\|S_{< U_0(Y), T(Y)}\|_{L^2}^2 \ll_\varepsilon Y^\varepsilon$ fail even under RH due to the $(\log Y)^{-2}$ Buchstab defect ($\mathcal{M}[Q_\lambda]'(1/2) = \frac{\tau^2}{48} \ne 0$, Theorem 8.D(2)).
  4. Summing across all super-$U_0(Y)$ blocks $U_0(Y) \le p \le T(Y)$ ($U_0(Y) = \lceil 2 Y^{5/8} \rceil$) cancels every intermediate $\pm\|S_{< 2^j, T}\|_{L^2}^2$ surge identically while keeping $S_{< U_0(Y), T(Y)}$ and $H_{[U_0(Y), T(Y)]}$ coupled (Theorem 8.D(1)).
- **Exact surviving coupled mixed-prime target**:
  $$\sum_{U_{\mathrm{log},\varepsilon / 4}(Y) < p \le T(Y)} M_p(Y, T(Y)) \le C_\varepsilon' Y^\varepsilon \qquad \left(\text{equivalently } \bigl\|S_{< U_0(Y), T(Y)} - H_{[U_0(Y), T(Y)]}\bigr\|_{L^2([Y, \tau Y], dX/X)}^2 \le C_\varepsilon Y^\varepsilon\right).$$
- **Size of missing saving**: Unconditional Korobov–Vinogradov–Walfisz bounds (`TC-054R` Theorem 9) give $E_{T(Y)}(Y) = \|S_{< U_0(Y), T(Y)} - H_{[U_0(Y), T(Y)]}\|_{L^2}^2 \ll Y\exp(-2 c_2 \Phi(Y))$ with $\Phi(Y) = (\log Y)^{3/5}(\log\log Y)^{-1/5}$, whereas `SUBGATE-TC-043A` requires a full power saving down to $O_\varepsilon(Y^\varepsilon)$ for every $\varepsilon > 0$ (a missing multiplicative saving of order $Y^{1 - \varepsilon}\exp(-2 c_2 \Phi(Y))$).

---

## 9. Formal Lean 4 Scope, Numerical Verification Architecture, and Claim Classification

### 9.1 Formal Lean 4 Scope (`formal/RiemannScope/LiouvilleSquareDilation.lean`, Theorems 17–20)

| Theorem # | Lean Identifier | Proved Statement (`0 sorry`, `0` custom `axiom`) | Formal vs. Analytic Boundary |
| :--- | :--- | :--- | :--- |
| 17 | `finite_prime_adjoining_fiber_and_pointwise_telescoping_tc056` | Endpoints $V_\varnothing^{\mathrm{pt}} = D_T^{\mathrm{pt}}$ and $V_{\{\text{primes}\le T\}}^{\mathrm{pt}} = E_T^{\mathrm{pt}}$, coupled prime-adjoining fiber sum $F_{P\cup\{p\}, s} = \sum_{s p^k \le T} F_{P, s p^k}$, cross-exponent increment $\Delta_{P,p}^{\mathrm{pt}}$, and ascending-prime list telescoping. | Pointwise finite sums in Lean; linearity of $\int_Y^{\tau Y} (\cdot)\,dX/X$ on $[Y, \tau Y]$ proved analytically in §3. |
| 18 | `finite_alternating_unimodal_chain_contraction_tc056` | For any nonnegative unimodal list $a_0, \dots, a_{n-1}$ (empty, 1-term, ties, zero extensions), $|\sum_k (-1)^k a_k| \le \max_k a_k$ and $(\sum_k (-1)^k a_k)^2 \le \sum_k a_k^2$. | Complete unconditional proof in Lean. |
| 19 | `gaussian_prime_chain_unimodal_and_singleton_contraction_tc056` | Consecutive Gaussian ratio identity, monotonic ratio decrease in $k$, unconditional unimodality of `gaussianPrimeChain`, and singleton contraction $V_{\{p\}}^{\mathrm{pt}}(X, T) \le D_T^{\mathrm{pt}}(X)$ with strict $<$ for $X > 0, p \le T$. | Concrete `Real.exp` Gaussian instantiation in Lean; strict integral transfer on $[Y, \tau Y]$ proved analytically in §4. |
| 20 | `mixed_interaction_decomposition_and_p_independence_tc056` | $\Delta_{P,p}^{\mathrm{pt}} = M_{P,p}^{\mathrm{pt}} - C_{P,p}^{\mathrm{pt}}$ ($\lambda(s)^2 = 1$ discharged, ordered $m \ne n$ without extra factor of $2$), ordered $k \ne l$ equivalence, $P$-independence $C_{P,p}^{\mathrm{pt}} = C_{\varnothing, p}^{\mathrm{pt}} = D_T^{\mathrm{pt}} - V_{\{p\}}^{\mathrm{pt}}$ via $r = s m$, and exact finite alternating shift formula. | Complete finite algebraic & bijection proof in Lean; integral transfer and infinite series bound $\sum_p C_p < 1$ proved analytically in §§5–6. |

### 9.2 Five-Category Claim Classification

1. **Formal Lean Theorems (`INDEPENDENT_MATHEMATICAL_AUDIT_PASSED` formal core, `0 sorry`, `0` custom `axiom`)**:
   - Theorems 17–20 in `formal/RiemannScope/LiouvilleSquareDilation.lean` (bringing the module to 20 public theorems).
2. **Analytic Theorems Proved Deductively Outside Lean (`PROVED_ANALYTIC`)**:
   - Proposition 2.1 (Dominated & Bounded Convergence proof of $Q_{a_S}(X)/\sqrt{X} \to m_S/2$ and $E_{a_S}(Y)/Y \to \frac{\tau-1}{4}m_S^2$ via $M_{\mathbf{1}} = \frac{1}{2} + 2(3/(2e))^{3/2}$), sharp admissible polylogarithmic scale (§2.3), smooth-fiber sparsity (§2.5), integrated Theorems 3.1, 4.3, 5.1, Theorem 6.1 ($\sum_{p \le T} C_p(Y, T) \le U_{\mathrm{contr,sharp}} \le U_{\mathrm{contr,elem}} < 1$), Theorem 8.B, Theorem 8.C (unconditional PNT refutation of $M_j(Y) - C_j(Y) \le A_\delta Y^\delta$ for every $\delta \in (0, 1)$), and Theorem 8.D.
3. **Certified Finite Evaluations (`CERTIFIED_FINITE`, 256-bit FLINT/Arb outward intervals)**:
   - Control 7a ($\Delta_{\{2\}, 3}(4, 6) > 0$), Control 7b ($[\sum_{64 \le p < 128}\Delta_p(128, 431)] / D_{431}(128) > 1$), Section 6 contraction caps ($U_{\mathrm{contr,sharp}} < U_{\mathrm{contr,elem}} < 1$), Section 8.3 surge constants ($\mathcal{I}(1) - \mathcal{I}(1/2) > 0$, $\mathcal{I}(2) - \mathcal{I}(1) > 0$, $\mathcal{I}(4) - \mathcal{I}(2) < 0$), and Section 8.4 compensated 4-block cancellation ($< 0$).
4. **Consistency and Falsification Controls**:
   - Dual-path evaluations (kernel-matrix grouping vs. independent `acb.integral` quadrature on $V_P$, $C_{P,p}$, $M_{P,p}$, $\Delta_{P,p}$ — exact mathematical identities rest on Lean/analytic proofs, never on interval overlap alone), parity controls $a_2, a_{\{3,5,7\}}, \mathbf{1}$ (§7.3), and unit-test negative controls for missing $1/r$ cofactor weights, illicit factor-of-$2$ on ordered $m \ne n$, uncoupled cutoffs, and untagged/drifted review intervals.
5. **Conditional / Open Research Statements**:
   - Theorem 8.A (conditional block transfer) and Theorem 8.D(3) (unconditional equivalence reducing `SUBGATE-TC-043A` across all $\varepsilon > 0$ and $Y \ge 1$ to the coupled multi-block mixed-interaction bound $\sum_{U_{\mathrm{log},\varepsilon/4}(Y) < p \le T(Y)} M_p(Y, T(Y)) \le C_\varepsilon' Y^\varepsilon$, equivalently $\|S_{< U_0(Y), T(Y)} - H_{[U_0(Y), T(Y)]}\|_{L^2([Y, \tau Y], dX/X)}^2 \ll_\varepsilon Y^\varepsilon$ at $U_0(Y) = \lceil 2 Y^{5/8} \rceil$).
   - **`SUBGATE-TC-043A` remains `OPEN` and `rh_proved` remains `false`.**
