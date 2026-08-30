# Derivation Review for Claim CLM-CT-027

**Claim ID**: `CLM-CT-027`  
**Reviewer Role**: Agent A — Derivation  
**Date**: August 30, 2026  

## Mathematical Derivation

1. **Completed Logarithmic Derivative**:
   $$\xi(s) = \frac{1}{2} s(s-1) \pi^{-s/2} \Gamma(s/2) \zeta(s).$$
   Taking the logarithmic derivative:
   $$G(s) = -\frac{\xi'}{\xi}(s) = -\frac{1}{s} - \frac{1}{s-1} + \frac{1}{2}\log\pi - \frac{1}{2}\psi(s/2) - \frac{\zeta'}{\zeta}(s) = A(s) + P(s),$$
   where $A(s) = -\frac{1}{s} - \frac{1}{s-1} + \frac{1}{2}\log\pi - \frac{1}{2}\psi(s/2)$ and $P(s) = -\frac{\zeta'}{\zeta}(s)$.

2. **Grade Derivatives**:
   Under $s_h = 1/2 + \tau^h z$ ($z = a+it$), $\frac{d s_h}{dh}\big|_{h=0} = \lambda z$ with $\lambda = \log\tau$.
   $$\dot G_0 = \lambda z G'(s), \quad \ddot G_0 = \lambda^2 [ z G'(s) + z^2 G''(s) ].$$
   Componentwise:
   - $A'(s) = \frac{1}{s^2} + \frac{1}{(s-1)^2} - \frac{1}{4}\psi'(s/2)$, $A''(s) = -\frac{2}{s^3} - \frac{2}{(s-1)^3} - \frac{1}{8}\psi''(s/2)$.
   - $P'(s) = -\sum_{n=2}^\infty \Lambda(n)(\log n) n^{-s}$, $P''(s) = \sum_{n=2}^\infty \Lambda(n)(\log n)^2 n^{-s}$.
   - $\ddot A_0 = \lambda^2 [ z A'(s) + z^2 A''(s) ]$, $\ddot P_0 = \lambda^2 [ z P'(s) + z^2 P''(s) ]$.

3. **Four-Block Expansion**:
   $$\mathfrak X_{\xi, W} = \Re\langle G_0, \ddot G_0\rangle_W = \Re\langle A+P, \ddot A+\ddot P\rangle_W = I_{PP} + I_{PA} + I_{AP} + I_{AA},$$
   where $I_{PP} = \Re\langle P, \ddot P\rangle_W$, $I_{PA} = \Re\langle P, \ddot A\rangle_W$, $I_{AP} = \Re\langle A, \ddot P\rangle_W$, $I_{AA} = \Re\langle A, \ddot A\rangle_W$.

4. **Independent Numerical Evaluation**:
   Evaluated at $a = 1.5, \sigma_W = 1.0$:
   - $I_{PP} \approx +3.2646096$
   - $I_{PA} \approx -3.2856896$
   - $I_{AP} \approx -3.4233085$
   - $I_{AA} \approx +3.4683204$
   - Sum $I_{\text{sum}} = +0.0239319822796...$
   - Direct integration of $G_0 \overline{\ddot G_0}$: $I_{\text{direct}} = +0.0239319822796...$
   - Agreement: $|I_{\text{direct}} - I_{\text{sum}}| < 10^{-50}$.

**Conclusion**: The completed-$\xi$ cross-term decomposition is algebraically exact and numerically verified to high precision.
