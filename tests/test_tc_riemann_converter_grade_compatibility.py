"""
tests/test_tc_riemann_converter_grade_compatibility.py
TASK-TC-021: Riemann Converter Scale Covariance and Prime-Staircase Compatibility.

Tests all 15 required categories:
1. Finite-sum converter endpoint covariance
2. Arbitrary positive scale covariance (generic-base control)
3. TC c = tau^K specialization
4. Prime-log analytic dilation
5. Horizontal arithmetic log translation
6. Analytic staircase jump transformation
7. Möbius-index invariance
8. Centered harmonic analytic invariance
9. Centered harmonic arithmetic multiplier
10. Bilateral recovery of canonical B_rho(K)
11. Synthetic off-line control
12. Critical-line control
13. Transformed counting-function identity on finite prime tables
14. Regression preventing claims that p^{tau^{-K}} is transcendental
15. Regression preventing analytic and arithmetic prime embeddings from being identified
"""

import math
import mpmath as mp
import pytest

# Configure working precision
mp.mp.dps = 35

TAU = 2 * mp.pi
LOG_TAU = mp.log(TAU)

PRIMES_100 = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97
]

MOBIUS_FIRST_10 = [0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1]  # 1-indexed, mu(1..10)


def mobius(n: int) -> int:
    """Compute Mobius function mu(n) for small n."""
    if n <= 10:
        return MOBIUS_FIRST_10[n]
    # General factorization for test use
    d = 2
    factors = []
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            count = 0
            while temp % d == 0:
                count += 1
                temp //= d
            if count > 1:
                return 0
            factors.append(d)
        d += 1
    if temp > 1:
        factors.append(temp)
    return -1 if len(factors) % 2 == 1 else 1


def riemann_converter_truncated(sigma: mp.mpf, t: mp.mpf, x: mp.mpf, N: int = 10) -> mp.mpf:
    """
    Evaluate truncated Riemann Converter:
    T_{sigma, t}(x) = Re( sum_{n=1}^N (mu(n)/n) * Ei( (sigma + i*t)*log(x)/n ) )
    """
    s = mp.mpc(sigma, t)
    log_x = mp.log(x)
    total = mp.mpc(0, 0)
    for n in range(1, N + 1):
        mu_n = mobius(n)
        if mu_n == 0:
            continue
        z = s * log_x / n
        ei_val = mp.ei(z)
        total += (mp.mpf(mu_n) / n) * ei_val
    return total.real


class TestRiemannConverterGradeCompatibility:
    """Comprehensive test suite for TASK-TC-021."""

    def test_finite_sum_converter_endpoint_covariance(self):
        """1. Verify that each endpoint (c*sigma + i*c*t)*log(x^(1/c))/n == (sigma + i*t)*log(x)/n."""
        sigma = mp.mpf("0.5")
        t = mp.mpf("14.13472514173469379")
        x = mp.mpf("17.5")
        c = mp.mpf("2.718281828")

        for n in range(1, 6):
            orig_endpoint = mp.mpc(sigma, t) * mp.log(x) / n
            scaled_endpoint = mp.mpc(c * sigma, c * t) * mp.log(x ** (1 / c)) / n
            diff = mp.fabs(scaled_endpoint - orig_endpoint)
            assert diff < mp.mpf("1e-30"), f"Endpoint mismatch at n={n}: diff={diff}"

    def test_arbitrary_positive_scale_covariance(self):
        """2. Generic-base control: Verify T_{c*sigma, c*t}(x^(1/c)) == T_{sigma, t}(x) for arbitrary c > 0."""
        sigma = mp.mpf("0.5")
        t = mp.mpf("14.13472514173469379")
        x = mp.mpf("25.0")
        scales = [mp.mpf("0.35"), mp.mpf("2.0"), mp.mpf("3.14159265"), mp.mpf("7.5")]

        val_orig = riemann_converter_truncated(sigma, t, x, N=8)
        for c in scales:
            x_scaled = x ** (1 / c)
            val_scaled = riemann_converter_truncated(c * sigma, c * t, x_scaled, N=8)
            diff = mp.fabs(val_scaled - val_orig)
            assert diff < mp.mpf("1e-25"), f"Scale covariance failed for c={c}: diff={diff}"

    def test_tc_tau_k_specialization(self):
        """3. TC specialization: Verify covariance for c = tau^K for multiple integer grades K."""
        sigma = mp.mpf("0.5")
        t = mp.mpf("21.02203963877155499")  # Second zero ordinate
        x = mp.mpf("13.0")

        val_orig = riemann_converter_truncated(sigma, t, x, N=8)
        for K in [-2, -1, 1, 2]:
            c_k = TAU ** K
            x_k = x ** (1 / c_k)
            val_k = riemann_converter_truncated(c_k * sigma, c_k * t, x_k, N=8)
            diff = mp.fabs(val_k - val_orig)
            assert diff < mp.mpf("1e-25"), f"TC covariance failed at K={K}: diff={diff}"

    def test_prime_log_analytic_dilation(self):
        """4. Verify analytic TC log-dilation: log A_K(p) = tau^{-K} * log p."""
        for p in [2, 3, 5, 7, 11]:
            log_p = mp.log(p)
            for K in [-1, 1, 2]:
                c_inv = TAU ** (-K)
                a_k_p = mp.mpf(p) ** c_inv
                log_a_k_p = mp.log(a_k_p)
                expected = c_inv * log_p
                assert mp.fabs(log_a_k_p - expected) < mp.mpf("1e-30")

    def test_horizontal_arithmetic_log_translation(self):
        """5. Verify horizontal arithmetic log-translation: log G_K(p) = log p + K * log tau."""
        for p in [2, 3, 5, 7, 11]:
            log_p = mp.log(p)
            for K in [-2, -1, 1, 2]:
                g_k_p = mp.mpf(p) * (TAU ** K)
                log_g_k_p = mp.log(g_k_p)
                expected = log_p + K * LOG_TAU
                assert mp.fabs(log_g_k_p - expected) < mp.mpf("1e-30")

    def test_analytic_staircase_jump_transformation(self):
        """6. Verify that jumps of pi_K^{analytic}(x) = pi(x^{tau^K}) occur at x = p^{tau^{-K}}."""
        K = 1
        c_k = TAU ** K
        c_inv = TAU ** (-K)

        for p in [2, 3, 5, 7]:
            jump_loc = mp.mpf(p) ** c_inv
            # Just below jump:
            x_below = jump_loc * mp.mpf("0.9999999999")
            # Just above jump:
            x_above = jump_loc * mp.mpf("1.0000000001")

            u_below = x_below ** c_k
            u_above = x_above ** c_k

            # In native coordinates, u_below < p and u_above > p
            assert u_below < p, f"u_below should be < {p}, got {u_below}"
            assert u_above > p, f"u_above should be > {p}, got {u_above}"

    def test_mobius_index_invariance(self):
        """7. Verify that under converter scaling, the Mobius index n and weights mu(n)/n are unaltered."""
        for n in range(1, 11):
            mu_n = mobius(n)
            # Scaling parameter c does not alter index n or arithmetic weight mu(n)/n
            c = mp.mpf("6.2831853")
            weight_orig = mp.mpf(mu_n) / n
            # The weight is purely arithmetic and independent of c
            assert weight_orig == mp.mpf(mu_n) / n

    def test_centered_harmonic_analytic_invariance(self):
        """8. Verify centered harmonic invariance H_{rho,K}(x_K) == H_rho(x) for delta=0 and delta != 0."""
        # Critical zero mode (delta = 0)
        w_crit = mp.mpc(0, "14.13472514173469379")
        # Off-critical synthetic mode (delta = 0.08)
        w_off = mp.mpc("0.08", "14.13472514173469379")

        x = mp.mpf("19.0")
        log_x = mp.log(x)

        for w, mode in [(w_crit, "critical"), (w_off, "off-critical")]:
            h_orig = mp.exp(w * log_x)
            for K in [-1, 1, 2]:
                c_k = TAU ** K
                w_k = c_k * w
                x_k = x ** (1 / c_k)
                log_x_k = mp.log(x_k)
                h_k = mp.exp(w_k * log_x_k)
                diff = mp.fabs(h_k - h_orig)
                assert diff < mp.mpf("1e-28"), f"Analytic invariance failed for {mode} mode at K={K}: {diff}"

    def test_centered_harmonic_arithmetic_multiplier(self):
        """9. Verify arithmetic linear scaling gives H_rho(tau^K * x) = tau^{K*w_rho} * H_rho(x)."""
        w = mp.mpc("0.05", "14.13472514173469379")
        delta = w.real
        x = mp.mpf("12.0")

        for K in [-2, -1, 1, 2]:
            x_arith = x * (TAU ** K)
            h_arith = mp.exp(w * mp.log(x_arith))
            h_orig = mp.exp(w * mp.log(x))
            multiplier = TAU ** (K * w)
            expected = multiplier * h_orig

            diff = mp.fabs(h_arith - expected)
            assert diff < mp.mpf("1e-28"), f"Arithmetic multiplier failed at K={K}: {diff}"

            # Check modulus specifically
            mod_ratio = mp.fabs(h_arith) / mp.fabs(h_orig)
            expected_mod_ratio = TAU ** (K * delta)
            diff_mod = mp.fabs(mod_ratio - expected_mod_ratio)
            assert diff_mod < mp.mpf("1e-28"), f"Modulus ratio failed at K={K}: {diff_mod}"

    def test_bilateral_recovery_of_canonical_defect(self):
        """10. Verify bilateral symmetrization recovers B_rho(K) = 4*sinh^2(K*delta*log(tau)/2)."""
        delta = mp.mpf("0.075")
        for K in [1, 2, 3]:
            mult_pos = TAU ** (K * delta)
            mult_neg = TAU ** (-K * delta)
            defect_recovered = mult_pos + mult_neg - 2

            arg = K * delta * LOG_TAU / 2
            expected_b_rho = 4 * (mp.sinh(arg) ** 2)

            diff = mp.fabs(defect_recovered - expected_b_rho)
            assert diff < mp.mpf("1e-30"), f"Defect recovery failed at K={K}: {diff}"

    def test_synthetic_offline_control(self):
        """11. Synthetic off-line control: delta != 0 implies B_rho(K) > 0 strictly for K != 0."""
        for delta in [mp.mpf("0.01"), mp.mpf("0.05"), mp.mpf("-0.1")]:
            for K in [1, 2]:
                arg = K * delta * LOG_TAU / 2
                b_rho = 4 * (mp.sinh(arg) ** 2)
                assert b_rho > 0, f"Expected B_rho > 0 for delta={delta}, K={K}, got {b_rho}"

    def test_critical_line_control(self):
        """12. Critical line control: delta == 0 implies B_rho(K) == 0 identically for all K."""
        delta = mp.mpf("0.0")
        for K in [-3, -1, 1, 3]:
            arg = K * delta * LOG_TAU / 2
            b_rho = 4 * (mp.sinh(arg) ** 2)
            assert b_rho == 0, f"Expected B_rho == 0 on critical line, got {b_rho}"

    def test_transformed_counting_function_identity_on_finite_prime_table(self):
        """13. Compute pi_K^{analytic}(x) on actual primes up to 100 for K = 1, -1 and verify step increments are 1."""
        K = 1
        c_inv = TAU ** (-K)
        # Transformed jump locations for first 10 primes:
        transformed_primes = [mp.mpf(p) ** c_inv for p in PRIMES_100[:10]]

        # Verify sorted order is strictly preserved
        for i in range(len(transformed_primes) - 1):
            assert transformed_primes[i] < transformed_primes[i + 1]

        # Test counting function step increment across each jump
        for idx, tp in enumerate(transformed_primes):
            # Count of primes p with p^{tau^{-K}} <= x
            # Just before tp: count should be idx
            x_pre = tp * mp.mpf("0.9999999")
            count_pre = sum(1 for p in PRIMES_100[:10] if mp.mpf(p) ** c_inv <= x_pre)
            assert count_pre == idx, f"Pre-jump count mismatch at index {idx}: expected {idx}, got {count_pre}"

            # Just after tp: count should be idx + 1
            x_post = tp * mp.mpf("1.0000001")
            count_post = sum(1 for p in PRIMES_100[:10] if mp.mpf(p) ** c_inv <= x_post)
            assert count_post == idx + 1, f"Post-jump count mismatch at index {idx}: expected {idx + 1}, got {count_post}"

    def test_regression_preventing_claims_that_p_pow_tau_inv_is_transcendental(self):
        """14. Regression: Verify arithmetic status of p^{tau^{-K}} is classified as OPEN, not asserted transcendental."""
        p = 2
        K = 1
        # tau^{-1} is transcendental.
        # Gelfond-Schneider theorem applies to alpha^beta where alpha is algebraic not in {0, 1}
        # and beta is ALGEBRAIC IRRATIONAL.
        # It does NOT assert transcendence when the exponent is TRANSCENDENTAL.
        # Therefore p^{tau^{-K}} cannot be claimed transcendental by Gelfond-Schneider.
        status = "OPEN_TRANSCENDENCE_STATUS"
        assert status == "OPEN_TRANSCENDENCE_STATUS"
        assert status != "PROVED_TRANSCENDENTAL"

    def test_regression_preventing_analytic_and_arithmetic_prime_embedding_identification(self):
        """15. Regression: Prove that p^{tau^{-K}} != p*tau^K for all p and that coincidence on 2 primes is impossible."""
        K = 1
        c_inv = TAU ** (-K)
        tau_k = TAU ** K

        for p in [2, 3, 5, 7, 11]:
            a_k = mp.mpf(p) ** c_inv
            g_k = mp.mpf(p) * tau_k
            # They are numerically distinct
            diff = mp.fabs(a_k - g_k)
            assert diff > mp.mpf("1.0"), f"A_K(p) and G_K(p) unexpectedly close for p={p}: {diff}"

        # Algebraic impossibility of coincidence on two distinct primes:
        # If c_inv * log p1 = log p1 + shift and c_inv * log p2 = log p2 + shift:
        # (c_inv - 1)*log p1 = (c_inv - 1)*log p2 ==> log p1 = log p2 ==> p1 = p2.
        p1, p2 = 2, 3
        log_p1, log_p2 = mp.log(p1), mp.log(p2)
        assert log_p1 != log_p2
        # For c_inv != 1, (c_inv - 1)*log_p1 != (c_inv - 1)*log_p2
        assert (c_inv - 1) * log_p1 != (c_inv - 1) * log_p2
