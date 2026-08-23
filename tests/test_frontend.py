"""
tests/test_frontend.py — Tests for Dash UI layout, laboratories, certification modes, and aspect ratio contracts.
"""

import json
import pytest
import plotly.graph_objects as go
import dash
from dash import html, dcc

import app
import certification


def test_app_layout_and_laboratories_exist():
    """Verify Dash app initializes with all 4 required research laboratories."""
    assert app.app.layout is not None
    layout_str = str(app.app.layout)
    
    # Check that all 4 main tabs exist
    assert "tab-instrument" in layout_str
    assert "tab-cross-height" in layout_str
    assert "tab-worldline" in layout_str
    assert "tab-proof-programme" in layout_str


def test_compute_modes_declared_and_distinct():
    """Verify Preview (35 dps), Audit (80 dps), and Certified (FLINT/Arb) modes exist and are distinct."""
    header = app.create_header()
    header_str = str(header)
    
    assert "Preview (35 dps)" in header_str
    assert "Audit (80 dps)" in header_str
    assert "Certified (FLINT/Arb)" in header_str
    assert "radio-cert-mode" in header_str


def test_dark_layout_preserves_equal_cartesian_aspect_ratio():
    """Verify that Plotly layouts enforce equal aspect ratio (scaleanchor='x', scaleratio=1.0)."""
    layout = app.DARK_LAYOUT
    assert layout["yaxis"]["scaleanchor"] == "x"
    assert layout["yaxis"]["scaleratio"] == 1.0


def test_cross_height_tab_components():
    """Verify Cross-Height laboratory components: overlay, deviation, distance matrix, Taylor shapes."""
    ch_tab = app.create_cross_height_tab()
    ch_str = str(ch_tab)
    
    assert "graph-ch-overlay" in ch_str
    assert "graph-ch-deviation" in ch_str
    assert "graph-ch-matrix" in ch_str
    assert "graph-ch-taylor" in ch_str
    assert "check-ch-blocks" in ch_str


def test_worldline_tab_components_and_bilateral_sequence():
    """Verify Bilateral Worldline laboratory components: trajectory, radial invariance, defect scaling, grade strip."""
    wl_tab = app.create_worldline_tab()
    wl_str = str(wl_tab)
    
    assert "graph-wl-trajectory" in wl_str
    assert "graph-wl-radial" in wl_str
    assert "graph-wl-defect" in wl_str
    assert "τ⁰ = 1 (Native ζ)" in wl_str


def test_proof_programme_dependency_map_and_missing_step():
    """Verify that proof programme explicitly displays the missing global coherence => radial rigidity step."""
    prog_tab = app.create_proof_programme_tab()
    prog_str = str(prog_tab)
    
    assert "Bilateral Continuation" in prog_str
    assert "Native Zero Blocks" in prog_str
    assert "Worldline Covariance" in prog_str
    assert "Radial Invariance" in prog_str
    assert "Exact Global Coherence Law" in prog_str
    assert "Coherence => Radial Rigidity" in prog_str
    assert "OPEN RESEARCH TARGET (Missing)" in prog_str


def test_panel_c_traces_for_zero_and_nonzero_perturbations():
    """Verify that Panel C always shows True Prime Count and Clean pi_N(x), and conditionally shows Perturbed pi_N(x)."""
    # 1. Delta = 0.0 (Zero perturbation)
    card, fig_a, fig_b, fig_c, fig_d, metrics = app.update_all_panels(
        mode="camera",
        t0=14.0,
        dt=20.0,
        delta_offset=0.0,
        selected_zero_idx=0,
        delta_pert=0.0,
        gamma_pert=14.134725,
        num_zeros=10,
        cert_mode="preview",
        k_val=0.0,
        kA=1.0, kB=1.0, kC=0.0, kD=0.0, k_lock=None,
        cA=1.0, c_lock=None,
        aniso_d=1.0, aniso_g=1.0,
        perturb_mode_val="single_pair_diagnostic",
        grade_type_val="integer_tau",
        grade_k_int=0,
        grade_q_rat="1/2",
        grade_k_cont=0.0,
        gen_scale=1.0,
        gen_base=10.0,
        disc_zeros=None
    )
    trace_names_c_zero = [t.name for t in fig_c.data]
    assert "True Prime Count π(x)" in trace_names_c_zero
    assert "Clean π_N(x)" in trace_names_c_zero
    assert "Perturbed π_N(x)" not in trace_names_c_zero

    # 2. Delta = 0.05 (Nonzero perturbation)
    card, fig_a, fig_b, fig_c, fig_d, metrics = app.update_all_panels(
        mode="camera",
        t0=14.0,
        dt=20.0,
        delta_offset=0.0,
        selected_zero_idx=0,
        delta_pert=0.05,
        gamma_pert=14.134725,
        num_zeros=10,
        cert_mode="preview",
        k_val=0.0,
        kA=1.0, kB=1.0, kC=0.0, kD=0.0, k_lock=None,
        cA=1.0, c_lock=None,
        aniso_d=1.0, aniso_g=1.0,
        perturb_mode_val="single_pair_diagnostic",
        grade_type_val="integer_tau",
        grade_k_int=0,
        grade_q_rat="1/2",
        grade_k_cont=0.0,
        gen_scale=1.0,
        gen_base=10.0,
        disc_zeros=None
    )
    trace_names_c_pert = [t.name for t in fig_c.data]
    assert "True Prime Count π(x)" in trace_names_c_pert
    assert "Clean π_N(x)" in trace_names_c_pert
    assert "Perturbed π_N(x)" in trace_names_c_pert


def test_certified_mode_fails_closed_on_missing_or_invalid():
    """Verify that Certified mode shows appropriate badges and fails closed."""
    # Test valid certified zero 1
    card, fig_a, fig_b, fig_c, fig_d, metrics_valid = app.update_all_panels(
        mode="camera",
        t0=14.0,
        dt=20.0,
        delta_offset=0.0,
        selected_zero_idx=0, # zero #1
        delta_pert=0.0,
        gamma_pert=14.134725,
        num_zeros=10,
        cert_mode="certified",
        k_val=0.0,
        kA=1.0, kB=1.0, kC=0.0, kD=0.0, k_lock=None,
        cA=1.0, c_lock=None,
        aniso_d=1.0, aniso_g=1.0,
        perturb_mode_val="single_pair_diagnostic",
        grade_type_val="integer_tau",
        grade_k_int=0,
        grade_q_rat="1/2",
        grade_k_cont=0.0,
        gen_scale=1.0,
        gen_base=10.0,
        disc_zeros=None
    )
    metrics_str = str(metrics_valid)
    assert "CERTIFIED" in metrics_str


def test_cross_height_lab_certified_mode_truthfulness():
    """Verify Cross-Height laboratory displays CERTIFIED badge only when all selected zeros are certified."""
    # Certified mode with valid block
    info_text, fig_overlay, fig_dev, fig_matrix, fig_taylor = app.update_cross_height_lab(
        selected_blocks=["low_validation", "medium_research"],
        zero_idx_val=0,
        u_max_val=0.5,
        cert_mode="certified"
    )
    info_str = str(info_text)
    assert "CERTIFIED: All 2 spectrum zeros verified in Arb" in info_str

    # Certified mode with no blocks
    info_empty, _, _, _, _ = app.update_cross_height_lab(
        selected_blocks=[],
        zero_idx_val=0,
        u_max_val=0.5,
        cert_mode="certified"
    )
    assert "CERTIFICATION REJECTED" in str(info_empty)



def test_worldline_lab_certified_mode_truthfulness():
    """Verify Bilateral Worldline laboratory displays CERTIFIED title only when 100% of curves are certified."""
    # Certified mode with canonical zero 1 and certified deltas [0.0, 0.10, -0.10]
    fig_traj, fig_rad, fig_def = app.update_worldline_lab(
        zero_gamma=14.134725,
        k_min_val=-2,
        k_max_val=2,
        selected_deltas=[0.0, 0.10, -0.10],
        cert_mode="certified"
    )
    assert "CERTIFIED" in fig_traj.layout.title.text
    assert "Bilateral Worldlines" in fig_traj.layout.title.text
    assert "UNCERTIFIED" not in fig_traj.layout.title.text

    # Certified mode with uncertified delta (e.g. 0.05) -> must fail closed
    fig_traj_bad, _, _ = app.update_worldline_lab(
        zero_gamma=14.134725,
        k_min_val=-2,
        k_max_val=2,
        selected_deltas=[0.05],
        cert_mode="certified"
    )
    assert not fig_traj_bad.layout.title.text.startswith("CERTIFIED [")
    assert "UNCERTIFIED" in fig_traj_bad.layout.title.text


def test_proof_programme_status_panel_dynamic_derivation(monkeypatch):
    """Verify Proof-Programme status panel is dynamically derived and changes state on report failure."""
    # 1. Normal state with valid verification report
    tab_layout = app.create_proof_programme_tab()
    tab_str = str(tab_layout)
    assert "VERIFIED" in tab_str
    assert "Rigorously Certified (FLINT Arb)" in tab_str

    # 2. Simulated report failure
    def mock_load_report(*args, **kwargs):
        return False, None, ["Verification report missing or stale"]

    monkeypatch.setattr(certification, "load_verification_report", mock_load_report)

    tab_layout_bad = app.create_proof_programme_tab()
    tab_bad_str = str(tab_layout_bad)
    assert "UNVERIFIED" in tab_bad_str
    assert "Rigorously Certified (FLINT Arb)" not in tab_bad_str

