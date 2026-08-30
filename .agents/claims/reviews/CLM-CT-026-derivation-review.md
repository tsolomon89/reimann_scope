# Derivation Review for Claim CLM-CT-026

**Claim ID**: `CLM-CT-026`  
**Reviewer Role**: Agent A — Derivation  
**Date**: August 30, 2026  

## Mathematical Derivation

1. **Prime-Side Object and Centered Dilation**:
   Let $z = a + it$ with $a > 1/2$, so that $\sigma = 1/2 + a > 1$.
   The prime logarithmic derivative is:
   $$P(s) = -\frac{\zeta'}{\zeta}(s) = \sum_{n=2}^\infty \Lambda(n) n^{-s}.$$
   Under centered grade action $s_h = 1/2 + \tau^h z$, $F_h(t) = P(s_h)$.
   At $h=0$:
   $$F_0(t) = \sum_{n=2}^\infty c_n e^{-it\log n}, \quad c_n = \Lambda(n)n^{-1/2-a}.$$

2. **Termwise Grade Derivatives**:
   $$\frac{d}{dh} n^{-\tau^h z} \Big|_{h=0} = -(\log\tau) z (\log n) n^{-z},$$
   $$\frac{d^2}{dh^2} n^{-\tau^h z} \Big|_{h=0} = (\log\tau)^2 [-z\log n + z^2(\log n)^2] n^{-z}.$$
   Thus:
   $$\dot F_0(t) = -(\log\tau)\sum_{n=2}^\infty c_n (a+it)(\log n) e^{-it\log n},$$
   $$\ddot F_0(t) = (\log\tau)^2 \sum_{n=2}^\infty c_n [-(a+it)\log n + (a+it)^2(\log n)^2] e^{-it\log n}.$$

3. **Convergence and Fubini Interchange**:
   Since $\Lambda(n) \le \log n$ and $\sigma = 1/2+a > 1$, we have:
   $$|c_n|(\log n)^j \le n^{-\sigma}(\log n)^{j+1}, \quad j \in \{0, 1, 2\}.$$
   For any Schwartz window $W \in \mathcal{S}(\mathbb{R})$, the moments $\mu_k = \int |t|^k |W(t)| dt < \infty$ are finite.
   The double series-integral converges absolutely:
   $$\sum_{m,n \ge 2} |c_m c_n| \int |W(t)| (|a+it|\log n + |a+it|^2(\log n)^2) dt \le \left(\sum_{m \ge 2} |c_m|\right) \sum_{n \ge 2} |c_n| [ (a\mu_0+\mu_1)\log n + (a^2\mu_0+2a\mu_1+\mu_2)(\log n)^2 ] < \infty.$$
   By Fubini-Tonelli, integration and double summation commute.

4. **Kernel Formula**:
   $$\langle F_0, \ddot F_0\rangle_W = (\log\tau)^2 \sum_{m,n \ge 2} c_m \overline{c_n} \mathcal{I}_{m,n}(W),$$
   where $\mathcal{I}_{m,n}(W) = (-aL_n + a^2L_n^2)\widehat W(\xi_{mn}) + i(L_n-2aL_n^2)\widehat{tW}(\xi_{mn}) - L_n^2\widehat{t^2W}(\xi_{mn})$.

**Conclusion**: The derivation is exact, mathematically rigorous, and fully justified by classical analysis.
