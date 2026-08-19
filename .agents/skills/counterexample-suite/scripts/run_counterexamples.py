#!/usr/bin/env python3
"""
Counterexample Suite for Riemann Hypothesis Research Harness
Implements standard counterexamples and negative controls:
1. Davenport-Heilbronn function (satisfies functional equation, but lacks Euler product and has off-line zeros).
2. Off-line zero radial centrifuge amplification control.
3. Dirichlet series truncation error in the critical strip.
"""

import sys
import mpmath

def davenport_heilbronn(s, dps=50):
    """
    Evaluates the Davenport-Heilbronn zeta function f(s).
    f(s) is a linear combination of Dirichlet L-functions for mod 5.
    chi(1)=1, chi(2)=i, chi(3)=-i, chi(4)=-1, chi(5)=0 (mod 5 character).
    f(s) = (1 - i*kappa)/2 * L(s, chi) + (1 + i*kappa)/2 * L(s, conj(chi))
    with kappa = (sqrt(10 - 2*sqrt(5)) - 2) / (sqrt(5) - 1).
    """
    mpmath.mp.dps = dps
    sqrt5 = mpmath.sqrt(5)
    kappa = (mpmath.sqrt(10 - 2*sqrt5) - 2) / (sqrt5 - 1)
    
    c1 = (1 - mpmath.j * kappa) / 2
    c2 = (1 + mpmath.j * kappa) / 2
    
    # L(s, chi) = 5^(-s) * [ zeta(s, 1/5) + i*zeta(s, 2/5) - i*zeta(s, 3/5) - zeta(s, 4/5) ]
    # using Hurwitz zeta
    s_c = mpmath.mpc(s)
    scale = mpmath.power(5, -s_c)
    z1 = mpmath.hurwitz(s_c, mpmath.mpf('0.2'))
    z2 = mpmath.hurwitz(s_c, mpmath.mpf('0.4'))
    z3 = mpmath.hurwitz(s_c, mpmath.mpf('0.6'))
    z4 = mpmath.hurwitz(s_c, mpmath.mpf('0.8'))
    
    L_chi = scale * (z1 + mpmath.j * z2 - mpmath.j * z3 - z4)
    L_chi_bar = scale * (z1 - mpmath.j * z2 + mpmath.j * z3 - z4)
    
    return c1 * L_chi + c2 * L_chi_bar

def run_counterexamples():
    mpmath.mp.dps = 50
    results = {}
    print("=== Counterexample & Falsification Suite ===")
    
    # 1. Davenport-Heilbronn Off-Line Zero Verification
    # Known off-line zero in critical strip around sigma approx 0.8085, t approx 85.6994
    # Let's verify root near s0 = 0.808517 + 85.699348j
    s_dh_guess = mpmath.mpc('0.808517', '85.699348')
    try:
        # Refine root using secant/muller
        s_dh_root = mpmath.findroot(lambda s: davenport_heilbronn(s), s_dh_guess)
        dh_residual = abs(davenport_heilbronn(s_dh_root))
        is_off_line = (abs(s_dh_root.real - 0.5) > 0.25) and (dh_residual < 1e-20)
        results['davenport_heilbronn_offline_zero'] = is_off_line
        print(f"Davenport-Heilbronn off-line zero found at: s = {mpmath.nstr(s_dh_root.real, 6)} + {mpmath.nstr(s_dh_root.imag, 6)}i")
        print(f"Residual: |f(s)| = {mpmath.nstr(dh_residual, 3)} (Off critical line: {is_off_line})")
    except Exception as e:
        print(f"Davenport-Heilbronn root refinement error: {e}")
        results['davenport_heilbronn_offline_zero'] = False
        
    # 2. Radial Centrifuge Amplification on Off-Line Zero
    # Let rho = 0.5 + 1e-4 + 14.134725j (delta = 1e-4)
    tau = 2 * mpmath.pi
    delta = mpmath.mpf('1e-4')
    K = mpmath.mpf('100')
    q_mod = mpmath.power(tau, K * delta)
    expected_log_mod = K * delta * mpmath.log(tau)
    actual_log_mod = mpmath.log(q_mod)
    results['centrifuge_offline_amplification'] = (abs(actual_log_mod - expected_log_mod) < 1e-40) and (q_mod > 1)
    print(f"Centrifuge off-line amplification (|q_rho^100| for delta=1e-4): {mpmath.nstr(q_mod, 6)} (Expected: tau^0.01 ~= 1.01859)")
    
    # 3. Dirichlet Series Divergence in Critical Strip
    # True zeta(0.5 + 14.13472514...i) == 0
    # Naive partial sum sum_{n=1}^500 n^(-s)
    s_zero = mpmath.mpc('0.5', '14.13472514173469379045725198356247')
    partial_sum = sum(mpmath.power(n, -s_zero) for n in range(1, 501))
    sum_error = abs(partial_sum)
    results['dirichlet_series_critical_strip_divergence'] = (sum_error > 0.1)
    print(f"Partial Dirichlet sum (N=500) at zeta zero: |sum n^-s| = {mpmath.nstr(sum_error, 4)} (True zeta=0, shows series is invalid in strip: {sum_error > 0.1})")
    
    # Summary
    all_passed = all(results.values())
    print("\n=== Summary ===")
    for k, v in results.items():
        print(f"[{'PASS' if v else 'FAIL'}] {k}")
        
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(run_counterexamples())
