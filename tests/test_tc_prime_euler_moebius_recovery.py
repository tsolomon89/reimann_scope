"""Focused mathematical and 256-bit Arb tests for TASK-TC-046:
Prime-by-Prime Möbius Recovery and Arithmetic Cross-Grade Compatibility.

Covers:
1. Three-way agreement of lambda_y(n) = (mu_y * log)(n) across closed-form
   prime-factorization cases (omega_{<=y}(n) in {0, 1, >=2}), Dirichlet
   convolution, and prime-by-prime operator recursion, including explicit
   prime powers p^a (p <= y), r^b (r > y), mixed composites p^a n_{>y}, and
   multi-prime composites.
2. Exact agreement window lambda_y(n) = Lambda(n) for all 2 <= n < 2 q_{>y}
   (where q_{>y} = min{p prime : p > y}), non-negativity Delta_y(n) =
   lambda_y(n) - Lambda(n) >= 0 for all n >= 2, and first discrepancy
   Delta_y(2 q_{>y}) = log 2 > 0 at n = 2 q_{>y}.
3. Exact summatory factorial identity L_y(x) = sum_{d | P_y, d <= x} mu(d) log(floor(x/d)!)
   and L_y(x) = psi(x) for x < 2 q_{>y}.
4. Three-way agreement of W_y(X) across product recursion
   prod_{p<=y}(I - p^{-1/2} D_p) W_log(X), divisor sum
   sum_{m | P_y} mu(m) m^{-1/2} W_log(X/m), and coefficient series
   sum_{n>=2} lambda_y(n) n^{-1/2} h_0(n/X).
5. Two-sided boundary envelope |B_{log,boundary}(u)| <= min((30731/98304) u^{-5/2},
   (92193/131072) u^{5/2}) from the vanishing-moment Stieltjes decomposition.
6. Euler-sieved seed Gram norm ||Psi_y||_{L^2(d^*x)}^2 and low-frequency
   coherent arch spike |E_y(i t_y)|^2 at t_y = pi / log(y).
7. Quantitative comparison bound |W(X) - W_y(X)| <= C_{log,0} X^{5/2} / (2 M^2)
   for y >= M >= max(2, X), and coupled-cutoff bound
   |W(X) - W_{M(X)}(X)| <= (1/2) C_{log,0} = 0.2787147936 < 0.278715 at
   y = M(X) = ceil(max(2, X^{5/4})) across positive, negative, near-zero,
   and increasing rational grades K in A_R.
8. Lean 4 module verification for theorems 44 and 45 and full-tree 256-bit Arb
   round-trip verification for section_15.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

from flint import acb, arb, ctx as flint_ctx

from tc.canonical_theta_correlation_bound import (
    CANONICAL_THETA_CORRELATION_LEAN_DEFS,
    CANONICAL_THETA_CORRELATION_LEAN_THEOREMS,
    PRIME_EULER_MOEBIUS_RECOVERY_STATUS,
    STARTING_HEAD_TC_046,
    TASK_TC_046_ID,
    verify_all_serialized_arb_in_tree,
    verify_canonical_theta_correlation_lean_module,
)
from tc.prime_euler_moebius_recovery import (
    certified_coupled_cutoff_M_X_arb,
    compute_coupled_cutoff_comparison_bound_arb,
    divisors_of_primorial,
    evaluate_H0_critical_line_arb,
    evaluate_b_log_boundary_term_arb,
    evaluate_chebyshev_psi_arb,
    evaluate_euler_dirichlet_poly_acb,
    evaluate_euler_sieved_seed_gram_norm_arb,
    evaluate_euler_spike_interval_gram_lower_bound_arb,
    evaluate_lambda_y_closed_form_arb,
    evaluate_lambda_y_convolution_arb,
    evaluate_lambda_y_recursion_arb,
    evaluate_summatory_L_y_direct_arb,
    evaluate_summatory_L_y_factorial_divisor_sum_arb,
    evaluate_w_log_divisor_aggregated_certified_arb,
    evaluate_w_prime_sum_certified_arb,
    evaluate_w_y_coefficient_certified_arb,
    evaluate_w_y_divisor_sum_certified_arb,
    evaluate_w_y_prime_recursion_certified_arb,
    next_prime_above,
    primes_up_to,
    verify_symbolic_finite_prime_identities,
    von_mangoldt_arb,
)


def test_01_symbolic_finite_prime_euler_identities():
    """Verify exact symbolic identities for finite-prime Euler inversion and prime-power cases."""
    sym = verify_symbolic_finite_prime_identities()
    assert sym["commutation_verified"] is True
    assert sym["two_prime_expansion_verified"] is True
    assert sym["log_additivity_verified"] is True
    assert sym["small_prime_power_equals_log_p"] is True
    assert sym["large_prime_power_equals_b_log_r"] is True
    assert sym["mixed_composite_one_small_prime_equals_log_p"] is True
    assert sym["two_small_primes_vanishes"] is True
    assert sym["coupled_exponent_verified"] is True
    assert sym["coupled_exponent_difference_5_2_minus_2_times_5_4"] == 0


def test_02_lambda_y_three_way_agreement_and_prime_power_cases():
    """Verify closed-form, Dirichlet convolution, and prime-by-prime recursion for lambda_y(n)."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for y in (2, 3, 5, 7, 11):
            for n in range(2, 90):
                lam_cf = evaluate_lambda_y_closed_form_arb(n, y)
                lam_conv = evaluate_lambda_y_convolution_arb(n, y)
                lam_rec = evaluate_lambda_y_recursion_arb(n, y)
                assert bool((lam_cf - lam_conv).contains(0))
                assert bool(abs(lam_cf - lam_conv) < arb("1e-70"))
                assert bool((lam_cf - lam_rec).contains(0))
                assert bool(abs(lam_cf - lam_rec) < arb("1e-70"))

        # Explicit prime-power and composite cases at y = 5 (primes <= 5 are {2, 3, 5}, q_{>5} = 7):
        # 1. Prime power p^a with p <= y: lambda_5(2^3 = 8) = log 2 = Lambda(8), lambda_5(3^2 = 9) = log 3 = Lambda(9)
        for n_pp, p_base in ((4, 2), (8, 2), (16, 2), (9, 3), (27, 3), (25, 5)):
            val = evaluate_lambda_y_closed_form_arb(n_pp, 5)
            vm = von_mangoldt_arb(n_pp)
            assert bool((val - arb(p_base).log()).contains(0))
            assert bool((val - vm).contains(0))

        # 2. Prime power r^b with r > y: lambda_5(7) = log 7 = Lambda(7), but lambda_5(7^2 = 49) = 2 log 7 != Lambda(49) = log 7
        val_7 = evaluate_lambda_y_closed_form_arb(7, 5)
        assert bool((val_7 - arb(7).log()).contains(0))
        val_49 = evaluate_lambda_y_closed_form_arb(49, 5)
        assert bool((val_49 - arb(2) * arb(7).log()).contains(0))
        assert bool(((val_49 - von_mangoldt_arb(49)) - arb(7).log()).contains(0))

        # 3. Mixed composite p^a * n_{>y} with exactly one distinct prime p <= y:
        #    lambda_5(2 * 7 = 14) = log 2, lambda_5(2^2 * 7 = 28) = log 2, lambda_5(3 * 7 = 21) = log 3
        for n_mix, p_small in ((14, 2), (28, 2), (21, 3), (35, 5)):
            val_m = evaluate_lambda_y_closed_form_arb(n_mix, 5)
            assert bool((val_m - arb(p_small).log()).contains(0))
            assert bool(von_mangoldt_arb(n_mix) == 0)

        # 4. Multi-prime composite with >= 2 distinct primes <= y vanishes identically:
        for n_zero in (6, 10, 12, 15, 18, 20, 24, 30, 42, 60):
            val_z = evaluate_lambda_y_closed_form_arb(n_zero, 5)
            assert bool(val_z == 0)
    finally:
        flint_ctx.prec = saved_prec


def test_03_agreement_threshold_2_q_gt_y_and_summatory_factorial_identity():
    """Verify lambda_y(n) = Lambda(n) for 2 <= n < 2 q_{>y}, first discrepancy at 2 q_{>y}, and factorial identity for L_y(x)."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        for y in (2, 3, 5, 7, 11, 13, 17, 19, 23):
            q_gt = next_prime_above(y)
            first_diff = None
            for n in range(2, 2 * q_gt + 15):
                diff = evaluate_lambda_y_closed_form_arb(n, y) - von_mangoldt_arb(n)
                # Non-negativity Delta_y(n) >= 0 for all n >= 2
                assert bool(diff.contains(0)) or bool(diff > arb(0))
                if first_diff is None and not (
                    bool(diff.contains(0)) and bool(abs(diff) < arb("1e-70"))
                ):
                    first_diff = n
            assert first_diff == 2 * q_gt
            diff_at_2q = evaluate_lambda_y_closed_form_arb(
                2 * q_gt, y
            ) - von_mangoldt_arb(2 * q_gt)
            assert bool((diff_at_2q - arb(2).log()).contains(0))
            assert bool(abs(diff_at_2q - arb(2).log()) < arb("1e-70"))

            # Verify L_y(x) = sum_{d | P_y, d <= x} mu(d) log(floor(x/d)!) and L_y(x) = psi(x) for x < 2 q_{>y}
            for x_test in (2 * q_gt - 1, 2 * q_gt, 2 * q_gt + 7):
                l_dir = evaluate_summatory_L_y_direct_arb(x_test, y)
                l_fac = evaluate_summatory_L_y_factorial_divisor_sum_arb(x_test, y)
                psi_x = evaluate_chebyshev_psi_arb(x_test)
                assert bool((l_dir - l_fac).contains(0))
                assert bool(abs(l_dir - l_fac) < arb("1e-70"))
                if x_test < 2 * q_gt:
                    assert bool((l_dir - psi_x).contains(0))
                    assert bool(abs(l_dir - psi_x) < arb("1e-70"))
                elif x_test == 2 * q_gt:
                    assert bool(((l_dir - psi_x) - arb(2).log()).contains(0))
    finally:
        flint_ctx.prec = saved_prec


def test_04_three_way_W_y_operator_divisor_coefficient_equivalence():
    """Verify product recursion, divisor sum, and coefficient series for W_y(X) agree in 256-bit Arb."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        tau_a = arb(2) * arb.pi()
        for y in (2, 3, 5, 7):
            for X_a in (arb(1), tau_a ** (arb(1) / arb(2)), tau_a):
                rec_res = evaluate_w_y_prime_recursion_certified_arb(
                    X_a, y=y, k_max=1500, prec_bits=256
                )
                div_res = evaluate_w_y_divisor_sum_certified_arb(
                    X_a, y=y, k_max=1500, prec_bits=256
                )
                coeff_res = evaluate_w_y_coefficient_certified_arb(
                    X_a, y=y, n_max=1500, prec_bits=256
                )
                p_ball = rec_res["enclosure_arb"]
                d_ball = div_res["enclosure_arb"]
                c_ball = coeff_res["enclosure_arb"]
                assert bool((p_ball - d_ball).contains(0))
                assert bool(abs(arb(p_ball.mid()) - arb(d_ball.mid())) < arb("1e-70"))
                assert bool(p_ball.overlaps(c_ball))
                assert bool(d_ball.overlaps(c_ball))
    finally:
        flint_ctx.prec = saved_prec


def test_05_stieltjes_boundary_envelope_and_critical_line_spike():
    """Verify two-sided boundary envelope for B_{log,boundary}(u), Gram norm ||Psi_y||_{L^2}^2, and low-frequency spike."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # 1. Two-sided boundary envelope |B_{log,boundary}(u)| <= min((30731/98304) u^{-5/2}, (92193/131072) u^{5/2})
        c_large = arb(30731) / arb(98304)
        c_small = arb(92193) / arb(131072)
        for u_val in (arb("0.1"), arb("0.25"), arb("0.5"), arb(1), arb(2), arb(4), arb(10)):
            b_u = evaluate_b_log_boundary_term_arb(u_val)
            b_hi = c_large * (u_val ** (-arb("2.5")))
            b_lo = c_small * (u_val ** arb("2.5"))
            env = b_hi if bool(b_hi <= b_lo) else b_lo
            assert bool(abs(b_u) <= env)

        # 2. Euler-sieved seed Gram norm ||Psi_y||_{L^2(d^*x)}^2 > 0
        for y in (2, 3, 5, 7, 11, 13):
            g_res = evaluate_euler_sieved_seed_gram_norm_arb(y, prec_bits=256)
            assert bool(g_res["gram_norm_sq_arb"] > arb("0.5"))
            assert bool(g_res["gram_norm_arb"] > arb("0.7"))

        # 3. Critical-line H_0(0) > 0, low-frequency coherent spike at t_y = pi / log(y),
        #    and controlled-width frequency interval Gram-norm lower bound on I_y = [7*pi / (8*log y), pi / log y]
        h0_0 = evaluate_H0_critical_line_arb(arb(0))
        assert bool(h0_0 > arb("2.82e-5")) and bool(h0_0 < arb("2.83e-5"))

        prev_spike = arb(0)
        for y in (11, 31, 97, 199, 499, 997):
            t_y = arb.pi() / arb(y).log()
            e_ty = evaluate_euler_dirichlet_poly_acb(acb(arb(0), t_y), y)
            e_sq = abs(e_ty) ** 2
            h0_ty = evaluate_H0_critical_line_arb(t_y)
            assert bool(h0_ty > h0_0)
            assert bool(e_sq > prev_spike)
            prev_spike = e_sq
        assert bool(prev_spike > arb(6000))

        prev_gram_lb = arb(0)
        for y in (97, 199, 499, 997, 1999, 4999, 9973):
            iv = evaluate_euler_spike_interval_gram_lower_bound_arb(y, prec_bits=256)
            assert iv["monotonicity_verified"] is True
            assert iv["H0_monotonicity_verified"] is True
            assert bool(iv["interval_width_arb"] > arb(0))
            assert bool(iv["e_sq_at_minus_arb"] <= iv["e_sq_at_plus_arb"])
            assert bool(iv["gram_sq_lb_H0_0_arb"] <= iv["gram_sq_lb_H0_minus_arb"])
            assert bool(iv["gram_sq_lb_H0_0_arb"] > prev_gram_lb)
            prev_gram_lb = iv["gram_sq_lb_H0_0_arb"]
        assert bool(prev_gram_lb > arb(153))
    finally:
        flint_ctx.prec = saved_prec


def test_06_coupled_cutoff_comparison_bound_across_admissible_grades():
    """Verify |W(X) - W_{M(X)}(X)| <= C_{log,0} X^{5/2} / (2 M(X)^2) <= (1/2) C_{log,0} < 0.278715 across rational grades and X = 16 +/- 10^{-30} ceiling regression."""
    saved_prec = flint_ctx.prec
    try:
        flint_ctx.prec = 256
        # Near-integer ceiling regression without float rounding loss:
        x_below_16 = arb(16) - arb("1e-30")
        x_exact_16 = arb(16)
        x_above_16 = arb(16) + arb("1e-30")
        assert certified_coupled_cutoff_M_X_arb(x_below_16, prec_bits=256) == 32
        assert certified_coupled_cutoff_M_X_arb(x_exact_16, prec_bits=256) == 32
        assert certified_coupled_cutoff_M_X_arb(x_above_16, prec_bits=256) == 33

        # Reproduce why binary64 float rounding fails at X = 16 + 10^{-30}:
        u_above_16 = (x_above_16**5).root(4)
        assert bool(u_above_16 > arb(32))
        naive_float_cutoff = int(math.ceil(float(u_above_16.upper())))
        assert naive_float_cutoff == 32
        assert not bool(arb(naive_float_cutoff) >= u_above_16)

        cmp_above_16 = compute_coupled_cutoff_comparison_bound_arb(
            x_above_16, prec_bits=256
        )
        assert cmp_above_16["M_X"] == 33
        assert cmp_above_16["M_X_ge_X_pow_5_4"] is True
        assert cmp_above_16["M_X_sq_ge_X_pow_5_2"] is True
        assert cmp_above_16["satisfies_uniform_bound"] is True

        tau_a = arb(2) * arb.pi()
        for k_frac in (
            Fraction(0, 1),
            Fraction(1, 100),
            Fraction(-1, 100),
            Fraction(1, 4),
            Fraction(-1, 4),
            Fraction(1, 2),
            Fraction(-1, 2),
            Fraction(1, 1),
            Fraction(-1, 1),
        ):
            abs_k = abs(k_frac)
            k_arb = arb(abs_k.numerator) / arb(abs_k.denominator)
            X_a = tau_a**k_arb
            cmp_info = compute_coupled_cutoff_comparison_bound_arb(X_a, prec_bits=256)
            M_X = cmp_info["M_X"]
            bound_M = cmp_info["bound_at_M_X_arb"]
            half_c = cmp_info["half_c_log_0_arb"]
            assert cmp_info["satisfies_uniform_bound"] is True
            assert bool(bound_M <= half_c)
            assert bool(half_c < arb("0.278715"))

            w_act = evaluate_w_prime_sum_certified_arb(X_a, n_max=2000, prec_bits=256)[
                "enclosure_arb"
            ]
            w_y = evaluate_w_y_coefficient_certified_arb(
                X_a, y=M_X, n_max=2000, prec_bits=256
            )["enclosure_arb"]
            w_log = evaluate_w_log_divisor_aggregated_certified_arb(
                X_a, k_max=2000, prec_bits=256
            )["enclosure_arb"]
            diff = abs(w_act - w_y)
            assert bool(diff.lower() <= bound_M.upper())
            # Also verify W_y(X) = W_log(X) + sum_{m | P_y, m>=2} mu(m) m^{-1/2} W_log(X/m)
            w_y_div = evaluate_w_y_divisor_sum_certified_arb(
                X_a, y=M_X, k_max=2000, prec_bits=256
            )["enclosure_arb"]
            assert bool(w_y.overlaps(w_y_div))
            assert bool((w_y_div - w_log).overlaps(w_y - w_log))
    finally:
        flint_ctx.prec = saved_prec


def test_07_lean_module_and_artifact_section_15():
    """Verify Lean 4 module theorems 44 & 45 and section_15 of data/tc_canonical_theta_correlation_bound.json."""
    lean_audit = verify_canonical_theta_correlation_lean_module()
    assert lean_audit["exists"] is True
    assert lean_audit["contains_sorry"] is False
    assert lean_audit["contains_admit"] is False
    assert lean_audit["matches_exact"] is True
    assert len(CANONICAL_THETA_CORRELATION_LEAN_DEFS) == 26
    assert len(CANONICAL_THETA_CORRELATION_LEAN_THEOREMS) == 45
    assert "finitePrimeEulerRecursionStep" in CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert "finitePrimeCoeffCases" in CANONICAL_THETA_CORRELATION_LEAN_DEFS
    assert (
        "finite_prime_euler_recursion_and_coefficient_cases"
        in CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    )
    assert (
        "coupled_prime_cutoff_comparison_and_boundedness_equivalence"
        in CANONICAL_THETA_CORRELATION_LEAN_THEOREMS
    )

    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "tc_canonical_theta_correlation_bound.json"
    )
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert payload["prime_euler_moebius_recovery_task_id"] == TASK_TC_046_ID
    assert (
        payload["status_dimensions"]["prime_euler_moebius_recovery_status"]
        == PRIME_EULER_MOEBIUS_RECOVERY_STATUS
    )
    sec15 = payload[
        "section_15_prime_by_prime_moebius_recovery_and_euler_compatibility"
    ]
    assert sec15["task_id"] == TASK_TC_046_ID
    assert sec15["inspected_baseline"] == STARTING_HEAD_TC_046
    s2 = sec15["section_2_finite_prime_euler_inversion_and_coefficients"]
    win = s2["exact_agreement_window_with_von_mangoldt"]
    assert win["all_three_lambda_methods_agree_up_to_120"] is True
    assert win["all_delta_nonnegative_verified"] is True
    assert all(
        row["exact_agreement_for_all_2_le_n_lt_2_q_gt_y"]
        and row["discrepancy_at_2_q_gt_y_equals_log_2"]
        for row in win["threshold_verification_table"]
    )
    assert all(
        row["factorial_identity_encloses_zero"]
        and row["prime_step_recursion_encloses_zero"]
        and row["equals_psi_below_2_q_gt_y"]
        for row in s2["summatory_verification_checks"]
    )
    assert all(
        row["prod_minus_divisor_encloses_zero"]
        and row["coeff_minus_divisor_encloses_zero"]
        and row["coeff_minus_prod_encloses_zero"]
        for row in s2["three_way_W_y_representation_checks"]
    )
    s3 = sec15["section_3_quantitative_compatibility_and_obstruction_analysis"]
    mech_a = s3["mechanism_A_critical_line_mellin_fourier_and_gram_bound"]
    assert "does NOT establish failure" in mech_a["low_frequency_coherent_arch_obstruction"]
    spike_rows = mech_a["low_frequency_spike_table"]
    assert len(spike_rows) == 11
    assert all(
        row["interval_monotonicity_E_y_sq_and_H0_verified"] is True
        for row in spike_rows
    )
    assert (
        spike_rows[-1]["integrated_gram_norm_sq_lower_bound_via_H0_0_certified"][
            "mid_float"
        ]
        > 153.0
    )

    s4 = sec15["section_4_coupled_cutoff_passage_and_grade_certification"]
    ceil_regs = {
        row["X_label"]: row for row in s4["certified_cutoff_ceiling_regression"]
    }
    assert ceil_regs["16 - 10^{-30}"]["certified_M_X"] == 32
    assert ceil_regs["16"]["certified_M_X"] == 32
    assert ceil_regs["16 + 10^{-30}"]["certified_M_X"] == 33
    assert ceil_regs["16 + 10^{-30}"]["naive_float_ceil_value"] == 32
    assert all(
        row["matches_expected_M_X"]
        and row["M_X_ge_X_pow_5_4_verified"]
        and row["M_X_sq_ge_X_pow_5_2_verified"]
        and row["satisfies_uniform_bound"]
        for row in s4["certified_cutoff_ceiling_regression"]
    )
    assert len(s4["certified_coupled_grade_table"]) == 13
    assert all(
        row["abs_W_minus_W_M_X_below_analytic_bound"]
        and row["abs_W_minus_W_M_X_below_half_C_log_0"]
        and row["abs_T_smooth_below_analytic_bound"]
        and row["smooth_plus_rough_partition_encloses_zero"]
        for row in s4["certified_coupled_grade_table"]
    )
    rem_obl = sec15["section_5_outcome_and_remaining_obligation"][
        "remaining_open_obligation"
    ]
    assert rem_obl["subgate_id"] == "SUBGATE-TC-043A"
    assert rem_obl["status"] == "OPEN"
    assert "|R_{mu, M(X)}(X)| <= M_trunc" in rem_obl["exact_surviving_lemma"]
    assert "|R_{mu, floor(X)}(X)| <=" not in rem_obl["exact_surviving_lemma"]
    assert "O(sqrt(X))" in rem_obl["exact_surviving_lemma"]

    rt15 = sec15["full_section_15_tree_roundtrip_verification"]
    assert rt15["all_enclose_original_256bit_arb_ball"] is True
    assert rt15["live_original_count_matches_enumerated_total"] is True
    assert (
        rt15["compared_against_live_original_arb_count"]
        == rt15["total_certified_arb_balls_checked"]
        == len(rt15["checked_paths"])
    )
    enum15 = verify_all_serialized_arb_in_tree(sec15, path_prefix="section_15")
    assert (
        rt15["compared_against_live_original_arb_count"]
        == enum15["total_certified_arb_balls_checked"]
    )
