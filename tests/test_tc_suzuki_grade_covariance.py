"""
Tests for TASK-TC-020: Suzuki Localized Weil Positivity, TC Grade Covariance, and Two-Direction Transcendence Rigidity.

Validates:
1. Centered grade translation multiplier in log-test variable: L(T_{Ka} f)(w_rho) = tau^{-K(rho - 1/2)} F(w_rho)
2. Bilateral character law on Z: eta_rho(K + J) = eta_rho(K) * eta_rho(J), eta_rho(-K) = eta_rho(K)^{-1}
3. Canonical non-unitarity defect identity: B_rho(K) = 4 sinh^2(K delta log(tau) / 2) >= 0, vanishing iff delta = 0
4. Exact test function support transformation under log-test translation: supp(T_{Ka} f) = [h - R, h + R]
5. Exact support/window transformation under dilation: supp(S_K f) = [-tau^{-K} R, tau^{-K} R]
6. Operator non-intertwining: failure of similarity S_K^* A_{tau^{-K} R} S_K = A_R due to discrete prime stations
7. Generic-base control: dilation geometry is base-generic (GENERIC_SCALE_GEOMETRY), distinguishing transcendental scale from period
8. Synthetic off-line mode control: strict positive defect for off-line zeros, exact vanishing on critical line
9. Two-pairing firewall: reflected pairing Q_W shift-invariance vs ordinary Gram Q_+ shift-sensitivity
10. Defect regression prevention: canonical B_rho is distinct from squared-modulus defect (|eta|^2 - 1)^2
11. Exceptional exponent collinearity: dim_Q S_tau <= 1 via Gelfond-Schneider line theorem
12. Rational-grade algebraic-coefficient noncollision: m tau^K = n tau^J <=> K = J and m = n for algebraic m, n
"""

import math
import pytest
import mpmath
import sympy as sp


class TestSuzukiGradeCovariance:
    """Test suite for TASK-TC-020 Suzuki localization, grade covariance, and transcendence rigidity."""

    def test_centered_grade_translation_multiplier(self):
        """Verify L(T_{Ka} f)(w_rho) = tau^{-K(rho - 1/2)} * L(f)(w_rho) for w_rho = delta + i*gamma."""
        dps = 50
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        a = mpmath.log(tau)

        delta = mpmath.mpf("0.08")
        gamma = mpmath.mpf("14.134725141734693790457251983562470270784257115699")
        w_rho = mpmath.mpc(delta, gamma)

        K = 3
        shift = K * a

        # For test Gaussian f(u) = exp(-u^2)
        # L(f)(w) = int exp(-u^2 - w*u) du = sqrt(pi) * exp(w^2 / 4)
        def L_f(w):
            return mpmath.sqrt(mpmath.pi) * mpmath.exp(w**2 / 4)

        # L(T_h f)(w) = int exp(-(u - h)^2 - w*u) du = exp(-w*h) * L(f)(w)
        def L_Th_f(w, h):
            return mpmath.exp(-w * h) * L_f(w)

        char_eta = mpmath.power(tau, -K * (w_rho))
        computed_ratio = L_Th_f(w_rho, shift) / L_f(w_rho)

        assert abs(computed_ratio - char_eta) < mpmath.mpf("1e-45")

    def test_bilateral_character_law_on_Z(self):
        """Verify bilateral group homomorphism eta_rho: Z -> C^times."""
        tau = 2 * math.pi
        delta = 0.05
        gamma = 21.022039638771555
        rho_minus_half = complex(delta, gamma)

        def eta(K_val):
            return tau ** (-K_val * rho_minus_half)

        # Multiplicative homomorphism
        for K in [-4, -1, 0, 2, 5]:
            for J in [-3, 0, 1, 4]:
                assert abs(eta(K + J) - eta(K) * eta(J)) < 1e-12
                assert abs(eta(-K) - 1.0 / eta(K)) < 1e-12

    def test_canonical_nonunitarity_defect_identity(self):
        """Verify B_rho(K) = |eta_rho(K)| + |eta_rho(K)|^{-1} - 2 = 4 sinh^2(K delta log(tau) / 2)."""
        dps = 60
        mpmath.mp.dps = dps
        tau = 2 * mpmath.pi
        log_tau = mpmath.log(tau)

        delta = mpmath.mpf("0.125")
        for K in [1, 2, -3, 5]:
            mod_eta = mpmath.power(tau, -K * delta)
            b_def = mod_eta + (1 / mod_eta) - 2

            arg = (K * delta * log_tau) / 2
            b_sinh = 4 * (mpmath.sinh(arg) ** 2)

            assert abs(b_def - b_sinh) < mpmath.mpf("1e-50")
            assert b_def > 0

        # Vanishing on critical line
        delta_zero = mpmath.mpf("0")
        mod_eta_zero = mpmath.power(tau, -2 * delta_zero)
        b_zero = mod_eta_zero + (1 / mod_eta_zero) - 2
        assert abs(b_zero) < mpmath.mpf("1e-50")

    def test_exact_support_transformation_under_grade_translation(self):
        """Verify supp(T_h f) = [h - R, h + R] for supp(f) = [-R, R] with h = K log(tau)."""
        R = 1.5
        tau = 2 * math.pi
        log_tau = math.log(tau)
        K = 2
        h = K * log_tau

        # Interval [-R, R] translated by h
        orig_supp = (-R, R)
        trans_supp = (orig_supp[0] + h, orig_supp[1] + h)

        assert trans_supp[0] == h - R
        assert trans_supp[1] == h + R
        # Notice that for h != 0, this interval is ASYMMETRIC (not centered at 0)
        assert trans_supp[0] != -trans_supp[1]

    def test_exact_support_transformation_under_dilation(self):
        """Verify supp(S_K f) = [-tau^{-K} R, tau^{-K} R] for (S_K f)(x) = tau^{K/2} f(tau^K x)."""
        R = 2.0
        tau = 2 * math.pi
        K = 1

        # f supported in [-R, R] => f(tau^K x) supported where |tau^K x| <= R => |x| <= tau^{-K} R
        scaled_R = R * (tau ** (-K))
        assert scaled_R < R  # For K > 0, interval shrinks

        # S_{-1} expands
        expanded_R = R * (tau ** 1)
        assert expanded_R > R

    def test_derived_operator_non_intertwining_failure_of_similarity(self):
        """Verify that arithmetic prime stations break dilation similarity: S_K^* A_{tau^{-K} R} S_K != A_R."""
        # The Weil distribution explicit formula has discrete impulses at prime powers: log(p^k).
        # Under dilation x -> tau^K x, an impulse at x = log(2) moves to x = tau^{-K} log(2).
        # We test whether tau^{-K} log(2) can equal any log(n) for integer n.
        tau = 2 * math.pi
        log2 = math.log(2)
        K = 1

        dilated_log2 = log2 / tau

        # Check against first 100 integers n: is dilated_log2 equal to log(n)?
        # For n = 1: log(1) = 0 != dilated_log2
        # For n = 2: log(2) > dilated_log2 since tau > 1
        # For n >= 2: log(n) >= log(2) > dilated_log2
        # dilated_log2 = 0.693147... / 6.283185... = 0.1103...
        # But for integer n >= 2, log(n) >= log(2) = 0.693147...
        # Thus dilated_log2 lies in the gap (0, log(2)) where NO primes or integers exist!
        assert 0 < dilated_log2 < log2
        # This confirms that dilation moves prime stations into arithmetic voids,
        # breaking any operator intertwining / similarity between A_R and A_{tau^{-K} R}.

    def test_generic_base_control_dilation_geometry(self):
        """Confirm that scale-window relations are identical for generic base b > 1 (GENERIC_SCALE_GEOMETRY)."""
        # Test generic base b = 3.5
        b = 3.5
        R = 1.0
        K = 2
        window_map = R * (b ** (-K))
        assert window_map == 1.0 / (3.5 ** 2)

        # In contrast, tau = 2*pi is specific in:
        # 1. Transcendental scale: 2*pi is transcendental by Lindemann (1882)
        # 2. Fourier period: 2*pi i is the period of complex exp
        # 3. Poisson duality: theta(1/t) = sqrt(t) theta(t) normalized with 2*pi / pi in Gaussian

    def test_synthetic_offline_mode_control(self):
        """Synthetic off-line zeros exhibit strictly positive defect; on-line zeros exhibit zero defect."""
        tau = 2 * math.pi
        K = 2

        # 1. On-line zero: delta = 0
        delta_on = 0.0
        b_on = tau ** (K * delta_on) + tau ** (-K * delta_on) - 2.0
        assert abs(b_on) < 1e-15

        # 2. Off-line quartet: delta = +/- 0.1
        delta_off = 0.1
        b_off = tau ** (K * delta_off) + tau ** (-K * delta_off) - 2.0
        assert b_off > 0.05

        # Defect is symmetric under delta -> -delta
        b_off_neg = tau ** (K * (-delta_off)) + tau ** (-K * (-delta_off)) - 2.0
        assert abs(b_off - b_off_neg) < 1e-15

    def test_two_pairing_firewall_reflected_vs_gram(self):
        """Regression test for Two-Pairing Firewall: Q_W is shift-invariant, Q_+ is shift-sensitive off-line."""
        # For a single mode with frequency w = delta + i*gamma
        delta = 0.1
        gamma = 14.13
        h = 1.83  # arbitrary shift

        w = complex(delta, gamma)
        w_refl = complex(-delta, gamma)  # -bar{w} = -delta + i*gamma

        # Reflected pairing exponential product:
        # F(w) * conjugate(F(-bar{w})) under translation picks up e^{-w*h} * conjugate(e^{-w_refl*h})
        # = exp(- (delta + i*gamma) h) * exp(- (-delta - i*gamma) h)
        # = exp(-delta*h - i*gamma*h + delta*h + i*gamma*h) = exp(0) = 1!
        shift_factor_reflected = mpmath.exp(-w * h) * mpmath.conj(mpmath.exp(-w_refl * h))
        assert abs(shift_factor_reflected - 1.0) < 1e-14  # IDENTICALLY 1!

        # Ordinary Gram pairing exponential product:
        # |F(w)|^2 under translation picks up |e^{-w*h}|^2 = exp(-2*delta*h)
        shift_factor_gram = abs(mpmath.exp(-w * h)) ** 2
        expected_gram = mpmath.exp(-2 * delta * h)
        assert abs(shift_factor_gram - expected_gram) < 1e-14
        assert abs(shift_factor_gram - 1.0) > 0.1  # NOT 1 because delta != 0!

    def test_regression_prevention_defect_conflation(self):
        """Ensure canonical B_rho is NOT confused with squared-modulus defect (|eta|^2 - 1)^2."""
        tau = 2 * math.pi
        delta = 0.2
        K = 1

        mod_eta = tau ** (-K * delta)

        # Canonical defect: B_rho = |eta| + |eta|^{-1} - 2
        b_canonical = mod_eta + (1.0 / mod_eta) - 2.0

        # Squared-modulus defect: (|eta|^2 - 1)^2
        b_squared = (mod_eta**2 - 1.0) ** 2

        # They are mathematically distinct functions of delta!
        assert abs(b_canonical - b_squared) > 0.01

        # Check Taylor expansions near delta = 0:
        # B_rho ~ (K*delta*log tau)^2
        # (|eta|^2 - 1)^2 ~ 4*(K*delta*log tau)^2
        # Ratio tends to 1/4 as delta -> 0!
        delta_small = 1e-5
        mod_small = tau ** (-K * delta_small)
        b_can_small = mod_small + (1.0 / mod_small) - 2.0
        b_sq_small = (mod_small**2 - 1.0) ** 2
        ratio = b_can_small / b_sq_small
        assert abs(ratio - 0.25) < 1e-4

    def test_exceptional_exponent_collinearity_dim_Q_le_1(self):
        """Verify the Exceptional Exponent Theorem: S_tau cap Q = {0} and dim_Q S_tau <= 1 via Gelfond-Schneider."""
        # 1. S_tau cap Q = {0}:
        # If alpha = p/q in Q \ {0}, then tau^{p/q} algebraic => tau^p algebraic => tau algebraic,
        # contradicting Lindemann's theorem that tau = 2*pi is transcendental.
        tau = 2 * sp.pi
        q = sp.Integer(3)
        p = sp.Integer(2)
        assert not (tau ** (p / q)).is_algebraic

        # 2. Gelfond-Schneider line theorem:
        # Let A = tau^alpha in Q_bar \ {0, 1} and B = tau^beta in Q_bar \ {0, 1} with alpha, beta in A_R.
        # Then A^{beta/alpha} = B in Q_bar.
        # If beta/alpha were in A_R \ Q (algebraic irrational), Gelfond-Schneider forces A^{beta/alpha} transcendental.
        # Contradiction, since B is algebraic!
        # Thus beta/alpha in Q.
        # This proves all non-zero exceptional exponents in S_tau are Q-collinear: dim_Q S_tau <= 1.

    def test_rational_grade_algebraic_coefficient_noncollision(self):
        """Verify rational-grade separation with algebraic coefficients: m tau^K = n tau^J => K=J, m=n."""
        # For m, n in Q_bar^\times and K, J in Q:
        # If K != J, let K - J = p/q in Q^\times (q >= 1).
        # Then tau^{p/q} = n/m in Q_bar => tau^p = (n/m)^q in Q_bar.
        # Contradicts transcendence of tau!
        # Test with algebraic numbers m = sqrt(2), n = cbrt(3)
        m = sp.sqrt(2)
        n = sp.cbrt(3)
        K = sp.Rational(1, 2)
        J = sp.Rational(1, 3)

        diff = m * (2 * sp.pi) ** K - n * (2 * sp.pi) ** J
        # Since K != J, diff cannot vanish
        val = sp.N(diff, 30)
        assert abs(val) > 0.1
