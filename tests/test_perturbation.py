"""
tests/test_perturbation.py — Tests for Single-Zero Perturbation Cache Equivalence

Trust test 9 from SPEC.md §12.
"""

import pytest
import numpy as np
import converter
import reference_data


def test_perturbation_delta_update_vs_full():
    """
    Trust Test 9: Verify that single-zero Delta C update is mathematically identical
    to full recomputation with the perturbed zero.
    """
    x_grid = np.linspace(2.0, 30.0, 30)
    ref_zeros = [complex(0.5, float(s)) for s in reference_data.load_reference_zeros()[:10]]
    
    rec_cache = converter.PrimeReconstructionCache(x_grid, ref_zeros)
    
    # Perturb the first zero rho_1 by delta = 0.05
    orig_rho_1 = ref_zeros[0]
    pert_rho_1 = complex(0.5 + 0.05, orig_rho_1.imag)
    
    # 1. Delta-update method
    clean_pi, pert_pi_fast = rec_cache.reconstruct_pi_perturbed(
        num_zeros=10,
        perturbed_zero_idx=0,
        perturbed_rho=pert_rho_1
    )
    
    # 2. Full recomputation method
    perturbed_zeros_list = list(ref_zeros)
    perturbed_zeros_list[0] = pert_rho_1
    full_cache = converter.PrimeReconstructionCache(x_grid, perturbed_zeros_list)
    pert_pi_full = full_cache.reconstruct_pi_n(num_zeros=10)
    
    # Verify exact agreement (< 1e-10)
    max_diff = np.max(np.abs(pert_pi_fast - pert_pi_full))
    assert max_diff < 1e-10, f"Perturbation delta update differed from full recomputation by {max_diff}"
