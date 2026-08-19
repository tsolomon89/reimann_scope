"""
tests/test_converter.py — Tests for Riemann Explicit Formula and Prime Counting Reconstruction

Trust test 8 from SPEC.md §12.
"""

import pytest
import numpy as np
import converter
import reference_data


def test_mobius_values():
    """Verify Mobius inversion lookup matches standard arithmetic definition."""
    assert converter.mobius(1) == 1
    assert converter.mobius(2) == -1
    assert converter.mobius(3) == -1
    assert converter.mobius(4) == 0
    assert converter.mobius(6) == 1
    assert converter.mobius(12) == 0
    assert converter.mobius(30) == -1


def test_reconstruction_prime_staircase():
    """
    Trust Test 8: Converter reconstructs prime staircase pi_N(x)
    approximating true pi(x) over [2, 30].
    """
    x_grid = np.linspace(2.0, 30.0, 50)
    ref_zeros = [complex(0.5, float(s)) for s in reference_data.load_reference_zeros()[:25]]
    
    rec_cache = converter.PrimeReconstructionCache(x_grid, ref_zeros)
    pi_recon = rec_cache.reconstruct_pi_n(num_zeros=25)
    pi_true = reference_data.prime_pi_array(x_grid)
    
    # At x = 20: true pi(20) = 8 (2, 3, 5, 7, 11, 13, 17, 19)
    idx_20 = np.argmin(np.abs(x_grid - 20.0))
    assert abs(pi_recon[idx_20] - 8.0) < 1.5
    
    # Mean absolute error between reconstructed and true staircase is modest
    mae = np.mean(np.abs(pi_recon - pi_true))
    assert mae < 1.8, f"MAE {mae} was too large"
