"""
tests/test_precision_no_float.py — Certified High-Precision Audit Tests

Verifies:
1. Reference zero matching and validation maintains arbitrary precision (> 53 bits / 15 decimal digits) without float downcast.
2. SHA-256 provenance hashes match disk bytes exactly.
3. Transcendental continuation evaluations maintain exact precision without float loss.
"""

import pytest
import mpmath
import reference_data
import math_core
import transcendental
import transforms


def test_reference_zero_arbitrary_precision_matching():
    """Verify that reference zero lookup and matching operates at 80 dps without float downcasts."""
    dps = 80
    with mpmath.workdps(dps + 10):
        # Known ordinate from vendored reference
        ref_zeros = reference_data.load_reference_zeros()
        gamma_str = ref_zeros[0]
        
        # Perturb slightly by 1e-25 (which IEEE-754 float would completely erase!)
        gamma_perturbed = str(math_core.to_mpf(gamma_str, dps=dps) + mpmath.mpf('1e-25'))
        
        # Exact match with candidate
        val_exact = reference_data.validate_zero_discovery([gamma_str], t_min="10.0", t_max="20.0", tolerance="1e-35", dps=dps)
        assert val_exact["matched_count"] == 1
        assert len(val_exact["unmatched_discovered"]) == 0
        
        # Perturbed match with tight tolerance of 30 digits should FAIL to match
        val_tight = reference_data.validate_zero_discovery([gamma_perturbed], t_min="10.0", t_max="20.0", tolerance="1e-30", dps=dps)
        assert val_tight["matched_count"] == 0
        assert len(val_tight["unmatched_discovered"]) == 1
        
        # Perturbed match with loose tolerance of 20 digits should SUCCEED
        val_loose = reference_data.validate_zero_discovery([gamma_perturbed], t_min="10.0", t_max="20.0", tolerance="1e-20", dps=dps)
        assert val_loose["matched_count"] == 1


def test_provenance_sha256_integrity():
    """Verify that all files listed in provenance.json match their recorded SHA-256 hashes."""
    is_valid = reference_data.verify_provenance()
    assert is_valid is True, "Provenance validation failed!"


def test_transcendental_high_precision_no_float_downcast():
    """Verify that transcendental operations maintain 80-digit precision beyond IEEE-754 limits."""
    dps = 80
    with mpmath.workdps(dps + 10):
        k_val = 3
        grade = transcendental.IntegerTauGrade(K=k_val)
        
        scale = grade.numeric_scale(dps=dps)
        tau = math_core.get_tau(dps=dps)
        expected_scale = tau ** k_val
        
        diff = abs(scale - expected_scale)
        assert diff < mpmath.mpf('1e-70'), f"Scale precision loss: {diff}"


def test_explicit_formula_high_precision_no_float_downcast():
    """Verify that explicit-formula evaluations, integrals, and defect decompositions maintain 80+ dps without float downcasts."""
    dps = 80
    with mpmath.workdps(dps + 20):
        ref_zeros = reference_data.load_reference_zeros()[:20]
        # Exact evaluation at 80 dps
        eval_res = math_core.explicit_formula_eval(
            j=1, K=0, zeros_ordinates=ref_zeros, prime_cutoff=1000, dps=dps
        )
        assert isinstance(eval_res["spectral_sum"], mpmath.mpf)
        assert isinstance(eval_res["gamma_term"], mpmath.mpf)
        assert isinstance(eval_res["residual"], mpmath.mpf)
        assert isinstance(eval_res["t_max"], mpmath.mpf)

        # Defect decomposition at 80 dps
        defect_res = math_core.finite_divisor_defect_radial_quartet_decomposed(
            j=1, K=0, gamma_a=ref_zeros[0], gamma_b=ref_zeros[1], delta="1e-35", dps=dps
        )
        assert isinstance(defect_res["radial_defect"], mpmath.mpf)
        assert isinstance(defect_res["merge_defect"], mpmath.mpf)
        # Radial defect for 1e-35 delta is non-zero in 80 dps but would be completely zero under float
        assert defect_res["radial_defect"] != mpmath.mpf(0)

