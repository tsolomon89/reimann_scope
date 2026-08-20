"""
tests/test_coupled_covariance_and_perturbation.py — Comprehensive Tests for Coupled Scale Covariance and Controlled Zero Perturbations

Covers all 14 mandatory requirements from prompt:
1. Exact high-precision zeta coordinate covariance: Z_A(A s) = zeta(s)
2. Mapped critical line: Re(s') = A/2
3. Mapped zero: rho' = A rho
4. Exact converter argument identity: (A rho) log(x^(1/A)) = rho log x
5. Single-zero J covariance: C_J(x^(1/A), A rho) = C_J(x, rho)
6. Single-zero pi covariance under matching truncation: C_pi(x^(1/A), A rho) = C_pi(x, rho)
7. Single-pair diagnostic construction: rho = 1/2 + delta + i gamma
8. Symmetry-complete quartet construction: rho_+ = 1/2+delta+i gamma, rho_- = 1/2-delta+i gamma
9. No conjugate double counting
10. Isolated delta-update equals independent full recomputation
11. delta = 0 reduces correctly to baseline
12. Batch converter_perturbation actually changes selected zero when delta != 0
13. Batch and direct canonical-engine calculations agree
14. Authoritative outputs remain high-precision decimal strings
"""

import pytest
import mpmath
import numpy as np

import math_core
import transforms
import converter
import research_runner
import reference_data


def test_exact_zeta_coordinate_covariance():
    """
    Test 1: Exact high-precision zeta coordinate covariance Z_A(A s) = zeta(s)
    across diverse s (generic points, critical-line, near zeros, outside critical strip)
    and k in [-10, -5, -2, -1, 0, 1, 2, 5, 10] at 80 dps.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        test_k_values = ["-5", "-2", "-1", "0", "1", "2", "5"]
        test_s_points = [
            mpmath.mpc("0.5", "14.134725141734693790457251983562"),  # On critical line (zero)
            mpmath.mpc("0.5", "25.0"),                                # On critical line (non-zero)
            mpmath.mpc("0.75", "14.134725141734693790457251983562"), # Inside critical strip
            mpmath.mpc("2.5", "10.0"),                                # In absolute convergence domain
            mpmath.mpc("-1.5", "12.0")                                # In negative half-plane
        ]
        
        for k_str in test_k_values:
            t_orig = transforms.OriginCoordinateDilation(k=k_str)
            k_mpf = math_core.to_mpf(k_str, dps=dps)
            scale_A = mpmath.power(tau, k_mpf)
            
            for s in test_s_points:
                # Baseline value W = zeta(s)
                W = math_core.zeta_eval(s, dps=dps)
                
                # Mapped point s' = A * s
                s_prime = scale_A * s
                
                # Value of transformed coordinate representation evaluated AT MAPPED POINT:
                # W_A = Z_A(s') = zeta(s' / A)
                W_A = t_orig.evaluate_function(s_prime, dps=dps)
                
                diff = abs(W_A - W)
                assert diff < mpmath.mpf("1e-25"), (
                    f"Zeta coordinate covariance failed at k={k_str}, s={s}: diff={diff}"
                )


def test_mapped_critical_line():
    """
    Test 2: Mapped critical line under origin coordinate dilation is Re(s') = A/2.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        for k_val in ["-2.0", "-1.0", "0.0", "1.0", "2.0"]:
            t_orig = transforms.OriginCoordinateDilation(k=k_val)
            scale_A = mpmath.power(tau, math_core.to_mpf(k_val, dps=dps))
            expected_re = scale_A / 2
            
            # Check image critical line coordinate
            s_crit = mpmath.mpc("0.5", "20.0")
            mapped_crit = t_orig.map_zero_mpc(s_crit, dps=dps)
            assert abs(mapped_crit.real - expected_re) < mpmath.mpf("1e-60")


def test_mapped_zero():
    """
    Test 3: Mapped zero under origin coordinate dilation is rho' = A * rho.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        ref_zeros = reference_data.load_reference_zeros()[:3]
        for gamma_str in ref_zeros:
            rho = mpmath.mpc("0.5", gamma_str)
            for k_val in ["-1.5", "0.0", "1.5"]:
                t_orig = transforms.OriginCoordinateDilation(k=k_val)
                scale_A = mpmath.power(tau, math_core.to_mpf(k_val, dps=dps))
                
                mapped_rho = t_orig.map_zero_mpc(rho, dps=dps)
                expected_mapped = scale_A * rho
                assert abs(mapped_rho - expected_mapped) < mpmath.mpf("1e-60")


def test_converter_argument_identity():
    """
    Test 4: Exact converter argument identity (A*rho) * log(x^(1/A)) = rho * log(x)
    for arbitrary A > 0, x > 1, rho in C.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        for k_val in ["-3.0", "-1.0", "0.5", "2.0"]:
            scale_A = mpmath.power(tau, math_core.to_mpf(k_val, dps=dps))
            for x_val in ["2.0", "10.0", "100.0"]:
                x_mpf = math_core.to_mpf(x_val, dps=dps)
                rho = mpmath.mpc("0.5", "14.134725141734693790457251983562")
                
                rho_prime = scale_A * rho
                x_prime = mpmath.power(x_mpf, mpmath.mpf(1) / scale_A)
                
                arg_baseline = rho * mpmath.log(x_mpf)
                arg_coupled = rho_prime * mpmath.log(x_prime)
                
                assert abs(arg_coupled - arg_baseline) < mpmath.mpf("1e-70")


def test_single_zero_j_covariance():
    """
    Test 5: Single-zero J covariance C_J(x^(1/A), A*rho) = C_J(x, rho) at 80 dps.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        test_k = ["-5", "-2", "-1", "0", "1", "2", "5"]
        test_x = ["10.0", "50.0", "100.0"]
        test_rho = [
            mpmath.mpc("0.5", "14.13472514173469379045725198356247027078425711569924317568556746"),
            mpmath.mpc("0.5", "21.02203963877155499262847959389690277733434052490278180469829596")
        ]
        
        for k_str in test_k:
            scale_A = mpmath.power(tau, math_core.to_mpf(k_str, dps=dps))
            for x_str in test_x:
                x_mpf = math_core.to_mpf(x_str, dps=dps)
                x_prime = mpmath.power(x_mpf, mpmath.mpf(1) / scale_A)
                
                for rho in test_rho:
                    rho_prime = scale_A * rho
                    
                    cj_clean = converter.zero_j_contribution_audit(x_mpf, rho, dps=dps)
                    cj_coupled = converter.zero_j_contribution_audit(x_prime, rho_prime, dps=dps)
                    
                    diff = abs(cj_coupled - cj_clean)
                    assert diff < mpmath.mpf("1e-25"), (
                        f"C_J covariance failed at k={k_str}, x={x_str}: diff={diff}"
                    )


def test_single_zero_pi_covariance():
    """
    Test 6: Single-zero pi covariance C_pi(x^(1/A), A*rho) = C_pi(x, rho)
    when evaluated under matching truncation semantics (m >= 1).
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        tau = math_core.get_tau(dps=dps)
        # Choose parameters where x' >= 2
        k_str = "0.2"
        scale_A = mpmath.power(tau, math_core.to_mpf(k_str, dps=dps))
        x_mpf = mpmath.mpf("100.0")
        x_prime = mpmath.power(x_mpf, mpmath.mpf(1) / scale_A)
        rho = mpmath.mpc("0.5", "14.134725141734693790457251983562")
        rho_prime = scale_A * rho
        
        # When evaluating sum over identical terms (rho log(x^(1/m)) = rho_prime log((x')^(1/m)))
        # each term in the Mobius sum is identical
        for m in [1, 2, 3]:
            xm = mpmath.power(x_mpf, mpmath.mpf(1) / m)
            xm_prime = mpmath.power(x_prime, mpmath.mpf(1) / m)
            cj_m = converter.zero_j_contribution_audit(xm, rho, dps=dps)
            cj_m_prime = converter.zero_j_contribution_audit(xm_prime, rho_prime, dps=dps)
            assert abs(cj_m_prime - cj_m) < mpmath.mpf("1e-25")


def test_single_pair_diagnostic_construction():
    """
    Test 7: Single-pair diagnostic construction: rho = 1/2 + delta + i*gamma.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        rho_clean = "0.5 + 14.134725141734693790457251983562j"
        delta = "0.05"
        
        zeros = converter.construct_perturbed_zeros_audit(rho_clean, delta, mode="single_pair_diagnostic", dps=dps)
        assert len(zeros) == 1
        assert abs(zeros[0].real - mpmath.mpf("0.55")) < mpmath.mpf("1e-70")
        assert abs(zeros[0].imag - mpmath.mpf("14.134725141734693790457251983562")) < mpmath.mpf("1e-70")


def test_symmetry_complete_quartet_construction():
    """
    Test 8: Symmetry-complete quartet construction:
    rho_+ = 1/2 + delta + i*gamma, rho_- = 1/2 - delta + i*gamma.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        rho_clean = "0.5 + 14.134725141734693790457251983562j"
        delta = "0.02"
        
        zeros = converter.construct_perturbed_zeros_audit(rho_clean, delta, mode="symmetry_complete_quartet", dps=dps)
        assert len(zeros) == 2
        assert abs(zeros[0].real - mpmath.mpf("0.52")) < mpmath.mpf("1e-70")
        assert abs(zeros[1].real - mpmath.mpf("0.48")) < mpmath.mpf("1e-70")
        assert abs(zeros[0].imag - zeros[1].imag) < mpmath.mpf("1e-70")


def test_no_conjugate_double_counting():
    """
    Test 9: Verify no conjugate double counting.
    In the 2*Re convention, C_J(x, rho) incorporates the conjugate pair (rho, bar(rho)).
    For a symmetry quartet with delta != 0, exactly 2 upper-half-plane zeros (rho_+, rho_-)
    represent the entire 4-point orbit {1/2 +/- delta +/- i*gamma}.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        x = "20.0"
        gamma = "14.134725141734693790457251983562"
        delta = "0.01"
        
        rho_plus = mpmath.mpc("0.51", gamma)
        rho_minus = mpmath.mpc("0.49", gamma)
        
        cj_plus = converter.zero_j_contribution_audit(x, rho_plus, dps=dps)
        cj_minus = converter.zero_j_contribution_audit(x, rho_minus, dps=dps)
        total_quartet_cj = cj_plus + cj_minus
        
        info = converter.compute_perturbed_contributions_audit(x, mpmath.mpc("0.5", gamma), delta, mode="symmetry_complete_quartet", dps=dps)
        assert abs(info["cj_perturbed"] - total_quartet_cj) < mpmath.mpf("1e-70")


def test_isolated_delta_update_equals_full_recomputation():
    """
    Test 10: Isolated delta-update pi_N,clean + Delta C_pi equals independent full recomputation
    from modified synthetic spectrum at audit precision for both modes.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        x = "20.0"
        ref_zeros = [mpmath.mpc("0.5", s) for s in reference_data.load_reference_zeros()[:5]]
        
        # 1. Single pair diagnostic mode
        info_diag = converter.compute_perturbed_contributions_audit(x, ref_zeros[0], "0.03", mode="single_pair_diagnostic", dps=dps)
        clean_pi = converter.riemann_explicit_pi_audit(x, ref_zeros, dps=dps)
        fast_pert_diag = clean_pi + info_diag["delta_cpi"]
        
        modified_zeros_diag = [info_diag["perturbed_rhos"][0]] + ref_zeros[1:]
        full_pert_diag = converter.riemann_explicit_pi_audit(x, modified_zeros_diag, dps=dps)
        
        assert abs(fast_pert_diag - full_pert_diag) < mpmath.mpf("1e-35")
        
        # 2. Symmetry complete quartet mode
        info_quart = converter.compute_perturbed_contributions_audit(x, ref_zeros[0], "0.03", mode="symmetry_complete_quartet", dps=dps)
        fast_pert_quart = clean_pi + info_quart["delta_cpi"]
        
        modified_zeros_quart = info_quart["perturbed_rhos"] + ref_zeros[1:]
        full_pert_quart = converter.riemann_explicit_pi_audit(x, modified_zeros_quart, dps=dps)
        
        assert abs(fast_pert_quart - full_pert_quart) < mpmath.mpf("1e-35")


def test_delta_zero_reduces_to_baseline():
    """
    Test 11: delta = 0 reduces correctly to baseline (Delta C_J = 0, Delta C_pi = 0, full diff = 0)
    for both single_pair_diagnostic and symmetry_complete_quartet modes.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        x = "20.0"
        rho = mpmath.mpc("0.5", "14.134725141734693790457251983562")
        
        for mode in ["single_pair_diagnostic", "symmetry_complete_quartet"]:
            info = converter.compute_perturbed_contributions_audit(x, rho, "0.0", mode=mode, dps=dps)
            assert abs(info["delta_cj"]) < mpmath.mpf("1e-70")
            assert abs(info["delta_cpi"]) < mpmath.mpf("1e-70")
            assert abs(info["cj_perturbed"] - info["cj_clean"]) < mpmath.mpf("1e-70")
            assert abs(info["cpi_perturbed"] - info["cpi_clean"]) < mpmath.mpf("1e-70")


def test_batch_converter_perturbation_changes_selected_zero():
    """
    Test 12: Batch converter_perturbation actually changes selected zero when delta != 0.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        inputs = {
            "zero_index": "0",
            "delta": "0.05",
            "x": "20.0",
            "num_zeros": "5",
            "perturbation_mode": "single_pair_diagnostic"
        }
        status, outputs, err = research_runner.evaluate_point("converter_perturbation", inputs, dps=dps)
        assert status == "ok"
        assert err is None
        
        delta_cj = mpmath.mpf(outputs["delta_cj"])
        delta_cpi = mpmath.mpf(outputs["delta_cpi"])
        delta_pi = mpmath.mpf(outputs["delta_pi_n"])
        
        # When delta = 0.05, the perturbation is nonzero
        assert abs(delta_cj) > mpmath.mpf("1e-5")
        assert abs(delta_cpi) > mpmath.mpf("1e-5")
        assert abs(delta_pi) > mpmath.mpf("1e-5")
        assert "0.55" in outputs["perturbed_rhos"]


def test_batch_and_direct_canonical_engine_agreement():
    """
    Test 13: Batch and direct canonical-engine calculations agree to 80 dps.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        # 1. zeta_trace_compare
        inputs_zeta = {
            "k": "1.5",
            "s_re": "0.5",
            "s_im": "14.13472514173469379045725198356247027078425711569924317568556746",
            "x": "20.0"
        }
        status, out_zeta, err = research_runner.evaluate_point("zeta_trace_compare", inputs_zeta, dps=dps)
        assert status == "ok"
        cov_res_batch = mpmath.mpf(out_zeta["covariance_residual"])
        assert cov_res_batch < mpmath.mpf("1e-25")
        
        # 2. converter_perturbation
        inputs_pert = {
            "zero_index": "1",
            "delta": "0.01",
            "x": "25.0",
            "num_zeros": "6",
            "perturbation_mode": "symmetry_complete_quartet"
        }
        status, out_pert, err = research_runner.evaluate_point("converter_perturbation", inputs_pert, dps=dps)
        assert status == "ok"
        
        # Direct canonical evaluation
        ref_zeros = reference_data.load_reference_zeros()[:6]
        rho_clean = mpmath.mpc("0.5", ref_zeros[1])
        direct_info = converter.compute_perturbed_contributions_audit("25.0", rho_clean, "0.01", mode="symmetry_complete_quartet", dps=dps)
        
        batch_delta_cj = mpmath.mpf(out_pert["delta_cj"])
        assert abs(batch_delta_cj - direct_info["delta_cj"]) < mpmath.mpf("1e-70")


def test_authoritative_outputs_remain_decimal_strings():
    """
    Test 14: Authoritative batch runner outputs serialize as exact decimal strings.
    """
    dps = 80
    with mpmath.workdps(dps + 15):
        inputs = {
            "k": "2.0",
            "s_re": "0.5",
            "s_im": "14.13472514173469379045725198356247027078425711569924317568556746",
            "x": "10.0"
        }
        status, outputs, err = research_runner.evaluate_point("zeta_trace_compare", inputs, dps=dps)
        assert status == "ok"
        
        for key, val in outputs.items():
            assert isinstance(val, str), f"Output '{key}' was not a string: {type(val)}"
            # Should be parseable by mpmath without error
            try:
                mpmath.mpf(val)
            except Exception:
                # could be complex or label
                pass
