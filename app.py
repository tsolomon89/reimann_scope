"""
app.py — Riemann Microscope / Macroscope Interactive Research Instrument

A high-performance, Desmos-like Plotly Dash dashboard conforming strictly to:
- RIEMANN_MICROSCOPE_SPEC.md
- MATH_CONTRACT.md
- DATA_PROVENANCE.md
- DECISIONS.md
- EXPERIMENT_PROTOCOL.md

Features 4 proof-facing laboratories:
1. 4-Panel Synchronized Microscope / Macroscope (Domain, Trace, Converter, Centrifuge)
2. Cross-Height Coherence Laboratory (Normalized Trajectories P_n(u), Deviation |P_n-u|, Distance Matrix, Taylor Shapes)
3. Bilateral Worldline Laboratory (3D/2D Graded Worldlines, Radial Leaves R_tau=delta, Grade Strip)
4. Proof Programme & Current Research Results (Obligation Dependency Map, Canonical Manifests, Certificate Inventory)
"""

from __future__ import annotations
import os
import glob
import json
from typing import Optional, List, Any, Dict, Tuple
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, State, ctx, dash_table
import dash_bootstrap_components as dbc

import transforms
import zero_finder
import reference_data
import converter
import cache
import transcendental
import math_core
import certification

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# Initialize Dash App with Dark theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP],
    title="Riemann Microscope / Macroscope",
    suppress_callback_exceptions=True
)

server = app.server

# Pre-load reference zeros & initial zero list
REF_ZEROS_STR = reference_data.load_reference_zeros()
INITIAL_ZEROS_FLOAT = [float(s) for s in REF_ZEROS_STR[:40]] if REF_ZEROS_STR else [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073
]

CANONICAL_BLOCK_KEYS = ["low_validation", "medium_research", "high_research", "very_high_sparse"]

# Custom Plotly Template for Desmos-like Dark Aesthetic
DARK_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="#12151c",
    plot_bgcolor="#181c24",
    font=dict(family="Inter, Roboto, sans-serif", color="#e2e8f0", size=11),
    margin=dict(l=50, r=30, t=35, b=40),
    xaxis=dict(gridcolor="#283042", zerolinecolor="#4a5568"),
    yaxis=dict(gridcolor="#283042", zerolinecolor="#4a5568", scaleanchor="x", scaleratio=1.0, constrain="range")
)


def compute_matching_dtick(span: float, target_ticks: int = 6) -> float:
    """Compute a clean, matching metric step size for both X and Y axes."""
    if span <= 0:
        return 1.0
    raw_step = span / target_ticks
    exponent = np.floor(np.log10(raw_step))
    fraction = raw_step / (10 ** exponent)
    if fraction < 1.5:
        nice_fraction = 1.0
    elif fraction < 3.5:
        nice_fraction = 2.0
    elif fraction < 7.5:
        nice_fraction = 5.0
    else:
        nice_fraction = 10.0
    return float(nice_fraction * (10 ** exponent))


# ==============================================================================
# UI HEADER & NAVIGATION
# ==============================================================================

def create_header():
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H4([
                        html.I(className="bi bi-compass me-2 text-info"),
                        "Riemann Scope"
                    ], className="mb-0 text-light fw-bold"),
                    html.Small("Transcendental Continuation & Zero Coherence Research Instrument", className="text-secondary")
                ], width="auto"),
            ], align="center", className="g-0"),
            dbc.Nav([
                dbc.NavItem(
                    html.Div([
                        html.Span("Compute Mode: ", className="text-secondary small me-2"),
                        dbc.RadioItems(
                            id="radio-cert-mode",
                            options=[
                                {"label": "Preview (35 dps)", "value": "preview"},
                                {"label": "Audit (80 dps)", "value": "audit"},
                                {"label": "Certified (FLINT/Arb)", "value": "certified"},
                            ],
                            value="preview",
                            inline=True,
                            className="btn-group text-light small font-monospace",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-info btn-sm",
                            labelCheckedClassName="active btn-info text-dark fw-bold",
                        )
                    ], className="d-flex align-items-center me-3")
                ),
                dbc.NavItem(
                    dbc.Button(
                        [html.I(className="bi bi-file-earmark-code me-1"), "Export Sweep Draft"],
                        id="btn-export-sweep",
                        color="outline-warning",
                        size="sm",
                        className="me-2"
                    )
                ),
                dbc.NavItem(
                    dbc.Button(
                        [html.I(className="bi bi-shield-check me-1"), "Zero Validation"],
                        id="btn-val-report",
                        color="outline-success",
                        size="sm",
                        className="me-2"
                    )
                ),
                dbc.NavItem(
                    dbc.Button(
                        [html.I(className="bi bi-arrow-counterclockwise me-1"), "Reset"],
                        id="btn-reset",
                        color="outline-secondary",
                        size="sm"
                    )
                )
            ], className="ms-auto align-items-center", navbar=True)
        ], fluid=True),
        color="#0d1117",
        dark=True,
        className="border-bottom border-secondary shadow-sm mb-2 py-2"
    )


# ==============================================================================
# TAB 1: 4-PANEL SYNCHRONIZED INSTRUMENT
# ==============================================================================

def create_active_card_panel():
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="bi bi-card-text me-2 text-warning"),
            html.Span("Active Mathematics Card", className="fw-bold small text-light")
        ], className="py-1 px-3 bg-dark border-secondary"),
        dbc.CardBody([
            dcc.Markdown(id="active-math-card", className="small text-light font-monospace")
        ], className="p-3 bg-dark text-light", style={"minHeight": "240px"})
    ], className="border-secondary shadow-sm mb-3")


def create_controls_panel():
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="bi bi-sliders me-2 text-info"),
            html.Span("Instrument & Transformation Controls", className="fw-bold small text-light")
        ], className="py-1 px-3 bg-dark border-secondary"),
        dbc.CardBody([
            dbc.Tabs([
                dbc.Tab(label="Transform Mode", tab_id="tab-mode", children=[
                    html.Div([
                        html.Label("Transformation Family:", className="fw-bold small text-light mt-2"),
                        dcc.Dropdown(
                            id="transform-mode-select",
                            options=[
                                {"label": "Transcendental Continuation: Z_tau(s, k) = zeta(tau^(-k) s)", "value": "transcendental"},
                                {"label": "Camera / Viewport Translation", "value": "camera"},
                                {"label": "Height Microscope s_K(u) = 1/2 + delta + i(t0 + u/tau^K)", "value": "height"},
                                {"label": "Origin Coordinate Dilation: s' = tau^K s", "value": "origin_dilation"},
                                {"label": "Centered Coordinate Dilation: s' = 1/2 + tau^K (s - 1/2)", "value": "centered_dilation"},
                                {"label": "Argument Transform: f_K(s) = zeta(tau^K s)", "value": "argument"},
                                {"label": "Full Kernel Lab: Z_{A,B,C,D}(s)", "value": "kernel_lab"},
                                {"label": "Centered Kernel: Z_A(s) = A zeta(1/2 + A(s - 1/2))", "value": "centered_kernel"},
                                {"label": "Anisotropic Coordinate Deformation: (delta', gamma')", "value": "anisotropic"},
                            ],
                            value="transcendental",
                            clearable=False,
                            className="dash-dropdown-dark mb-3"
                        ),

                        # Transcendental Continuation Sub-panel
                        html.Div(id="container-mode-transcendental", children=[
                            html.Label("Transcendental Continuation Grade Taxonomy:", className="fw-bold small text-light"),
                            dbc.RadioItems(
                                id="radio-grade-type",
                                options=[
                                    {"label": "Integer Grade K in Z (tau^K)", "value": "integer_tau"},
                                    {"label": "Rational Grade q = n/d in Q (tau^q)", "value": "rational_tau"},
                                    {"label": "Continuous Grade k in R (tau^k)", "value": "continuous_tau"},
                                    {"label": "Generic Scale / Non-tau Base (b^k)", "value": "generic_scale"},
                                ],
                                value="integer_tau",
                                className="text-light small mb-2 font-monospace"
                            ),
                            # Integer Sub-control
                            html.Div(id="subcontainer-grade-integer", children=[
                                html.Label("Canonical Bilateral Grade K in Z:", className="small text-light"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button("-1 (tau^(-1))", id="btn-k-minus", size="sm", color="outline-info", className="w-100")
                                    ], width=3),
                                    dbc.Col([
                                        dbc.Input(id="input-grade-k-int", type="number", value=0, step=1, size="sm", className="text-center font-monospace")
                                    ], width=3),
                                    dbc.Col([
                                        dbc.Button("+1 (tau^1)", id="btn-k-plus", size="sm", color="outline-info", className="w-100")
                                    ], width=3),
                                    dbc.Col([
                                        dbc.Button("K=0 (Native)", id="btn-k-reset-zero", size="sm", color="outline-secondary", className="w-100")
                                    ], width=3),
                                ], className="g-1 mb-2"),
                                html.Small("Note: K=0 is identically ordinary analytically continued zeta (tau^0=1).", className="text-secondary d-block mb-2")
                            ]),
                            # Rational Sub-control
                            html.Div(id="subcontainer-grade-rational", style={"display": "none"}, children=[
                                html.Label("Rational Grade q = n/d:", className="small text-light"),
                                dbc.Input(id="input-grade-q-rat", type="text", value="1/2", size="sm", className="font-monospace mb-2"),
                            ]),
                            # Continuous Sub-control
                            html.Div(id="subcontainer-grade-continuous", style={"display": "none"}, children=[
                                html.Label("Continuous Grade k in R:", className="small text-light"),
                                dcc.Slider(id="slider-grade-k-cont", min=-5.0, max=5.0, step=0.1, value=0.0,
                                           marks={-5: "-5", -2: "-2", 0: "0", 2: "+2", 5: "+5"},
                                           tooltip={"placement": "bottom", "always_visible": False}),
                            ]),
                            # Generic Sub-control
                            html.Div(id="subcontainer-grade-generic", style={"display": "none"}, children=[
                                dbc.Row([
                                    dbc.Col([
                                        html.Label("Scale A:", className="small text-light"),
                                        dbc.Input(id="input-generic-scale", type="number", value=2.0, step=0.1, size="sm")
                                    ], width=6),
                                    dbc.Col([
                                        html.Label("Base b:", className="small text-light"),
                                        dbc.Input(id="input-generic-base", type="number", value=10.0, step=0.1, size="sm")
                                    ], width=6),
                                ], className="mb-2")
                            ]),

                            # Compression / Expansion Calculator
                            html.Div([
                                html.Label("Compression Grade Inversion Calculator:", className="fw-bold small text-info mt-1"),
                                dbc.Row([
                                    dbc.Col([
                                        html.Label("Source Height t_src:", className="small text-light"),
                                        dbc.Input(id="input-comp-source", type="number", value=1419.42, step=1.0, size="sm")
                                    ], width=5),
                                    dbc.Col([
                                        html.Label("Target Height t_tgt:", className="small text-light"),
                                        dbc.Input(id="input-comp-target", type="number", value=14.13, step=0.1, size="sm")
                                    ], width=5),
                                    dbc.Col([
                                        dbc.Button("Derive", id="btn-comp-derive", color="info", size="sm", className="mt-4 w-100")
                                    ], width=2)
                                ], className="g-2 mb-1"),
                                html.Div(id="comp-result-display", className="small font-monospace text-warning")
                            ], className="p-2 border border-secondary rounded bg-black bg-opacity-25 mt-2 mb-2")
                        ]),

                        # Scale Transforms Sub-panel
                        html.Div(id="container-mode-scale", style={"display": "none"}, children=[
                            html.Label("Scale Grade k:", className="fw-bold small text-light mt-1"),
                            dcc.Slider(id="slider-k", min=-3.0, max=3.0, step=0.25, value=0.0,
                                       marks={-3: "-3", -2: "-2", -1: "-1", 0: "0", 1: "+1", 2: "+2", 3: "+3"},
                                       tooltip={"placement": "bottom", "always_visible": False}),
                        ]),

                        # Kernel Lab Sub-panel
                        html.Div(id="container-mode-kernel", style={"display": "none"}, children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Scale A:", className="small text-light"),
                                    dcc.Slider(id="slider-kernel-A", min=0.1, max=4.0, step=0.1, value=1.0,
                                               marks={0.5: "0.5", 1.0: "1.0", 2.0: "2.0", 4.0: "4.0"},
                                               tooltip={"placement": "bottom", "always_visible": False}),
                                ], width=6),
                                dbc.Col([
                                    html.Label("Scale B (B = 1/A):", className="small text-light"),
                                    dcc.Slider(id="slider-kernel-B", min=0.1, max=4.0, step=0.1, value=1.0,
                                               marks={0.5: "0.5", 1.0: "1.0", 2.0: "2.0", 4.0: "4.0"},
                                               tooltip={"placement": "bottom", "always_visible": False}),
                                ], width=6)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Pre-shift C:", className="small text-light"),
                                    dbc.Input(id="input-kernel-C", type="number", value=0.0, step=0.1, size="sm")
                                ], width=6),
                                dbc.Col([
                                    html.Label("Post-shift D:", className="small text-light"),
                                    dbc.Input(id="input-kernel-D", type="number", value=0.0, step=0.1, size="sm")
                                ], width=6)
                            ], className="mb-2"),
                            dbc.Checklist(
                                id="check-kernel-lock",
                                options=[{"label": "Lock Inverse Scale Invariant (B = 1/A, C = D = 0)", "value": "lock"}],
                                value=["lock"],
                                className="text-light small mb-2"
                            )
                        ]),

                        # Centered Kernel Sub-panel
                        html.Div(id="container-mode-centered-kernel", style={"display": "none"}, children=[
                            html.Label("Centered Kernel Scale A:", className="small text-light"),
                            dcc.Slider(id="slider-centered-kernel-A", min=0.1, max=4.0, step=0.1, value=1.0,
                                       marks={0.5: "0.5", 1.0: "1.0", 2.0: "2.0", 4.0: "4.0"},
                                       tooltip={"placement": "bottom", "always_visible": False}),
                            dbc.Checklist(
                                id="check-centered-kernel-lock",
                                options=[{"label": "Lock Invariants (Fix Critical Line Re=1/2)", "value": "lock"}],
                                value=["lock"],
                                className="text-light small mb-2"
                            )
                        ]),

                        # Anisotropic Sub-panel
                        html.Div(id="container-mode-aniso", style={"display": "none"}, children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Label("A_delta (Real Dilation):", className="small text-light"),
                                    dcc.Slider(id="slider-aniso-delta", min=0.1, max=3.0, step=0.1, value=1.0,
                                               marks={0.5: "0.5", 1.0: "1.0", 2.0: "2.0"},
                                               tooltip={"placement": "bottom", "always_visible": False}),
                                ], width=6),
                                dbc.Col([
                                    html.Label("A_gamma (Imag Dilation):", className="small text-light"),
                                    dcc.Slider(id="slider-aniso-gamma", min=0.1, max=3.0, step=0.1, value=1.0,
                                               marks={0.5: "0.5", 1.0: "1.0", 2.0: "2.0"},
                                               tooltip={"placement": "bottom", "always_visible": False}),
                                ], width=6)
                            ])
                        ])
                    ])
                ]),
                dbc.Tab(label="Domain & Viewport", tab_id="tab-domain", children=[
                    html.Div([
                        html.Label("Center Height (t0):", className="fw-bold small text-light mt-2"),
                        dcc.Slider(id="slider-t0", min=0.0, max=100.0, step=0.5, value=14.0,
                                   marks={0: "0", 14: "γ₁", 21: "γ₂", 50: "50", 100: "100"},
                                   tooltip={"placement": "bottom", "always_visible": False}),
                        html.Label("Height Span (Δt):", className="fw-bold small text-light mt-1"),
                        dcc.Slider(id="slider-dt", min=2.0, max=50.0, step=1.0, value=20.0,
                                   marks={2: "2", 10: "10", 20: "20", 50: "50"},
                                   tooltip={"placement": "bottom", "always_visible": False}),
                        html.Label("Critical Line Real Offset (δ = σ - 1/2):", className="fw-bold small text-light mt-1"),
                        dcc.Slider(id="slider-delta-offset", min=-0.5, max=0.5, step=0.01, value=0.0,
                                   marks={-0.5: "-0.5", 0: "0.0 (Line)", 0.5: "+0.5"},
                                   tooltip={"placement": "bottom", "always_visible": False}),
                    ])
                ]),
                dbc.Tab(label="Zero & Converter", tab_id="tab-converter", children=[
                    html.Div([
                        html.Label("Select Reference Zero:", className="fw-bold small text-light mt-2"),
                        dcc.Dropdown(
                            id="dropdown-selected-zero",
                            options=[
                                {"label": f"Zero #{i+1}: γ = {z:.6f}", "value": i}
                                for i, z in enumerate(INITIAL_ZEROS_FLOAT[:20])
                            ],
                            value=0,
                            clearable=False,
                            className="dash-dropdown-dark mb-2"
                        ),
                        html.Label("Perturbation Protocol:", className="fw-bold small text-light"),
                        dbc.RadioItems(
                            id="radio-perturb-mode",
                            options=[
                                {"label": "Single-Pair Diagnostic: (1/2+δ, γ)", "value": "single_pair_diagnostic"},
                                {"label": "Symmetry-Complete Quartet: ±δ, ±γ", "value": "symmetry_complete_quartet"},
                            ],
                            value="single_pair_diagnostic",
                            className="text-light small mb-2 font-monospace"
                        ),
                        html.Label("Radial Perturbation Preset (δ):", className="fw-bold small text-light"),
                        dbc.ButtonGroup([
                            dbc.Button("0.0", id="preset-0", size="sm", color="secondary"),
                            dbc.Button("10⁻⁸", id="preset-1e8", size="sm", color="secondary"),
                            dbc.Button("10⁻⁶", id="preset-1e6", size="sm", color="secondary"),
                            dbc.Button("10⁻⁴", id="preset-1e4", size="sm", color="secondary"),
                            dbc.Button("10⁻²", id="preset-1e2", size="sm", color="secondary"),
                        ], className="mb-2 w-100"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("δ = Re(ρ) - 1/2:", className="small text-light"),
                                dbc.Input(id="input-delta-pert", type="number", value=0.0, step=0.0001, size="sm")
                            ], width=6),
                            dbc.Col([
                                html.Label("γ = Im(ρ):", className="small text-light"),
                                dbc.Input(id="input-gamma-pert", type="number", value=INITIAL_ZEROS_FLOAT[0], step=0.001, size="sm")
                            ], width=6)
                        ], className="mb-2"),
                        html.Label("Converter Zero Count (N):", className="fw-bold small text-light mt-1"),
                        dcc.Slider(id="slider-num-zeros", min=1, max=30, step=1, value=15,
                                   marks={1: "1", 10: "10", 20: "20", 30: "30"},
                                   tooltip={"placement": "bottom", "always_visible": False}),
                    ])
                ])
            ], id="controls-tabs", active_tab="tab-mode")
        ], className="p-3")
    ], className="border-secondary shadow-sm mb-3")


def create_instrument_tab():
    return html.Div([
        dbc.Row([
            # Panel A: Domain Plane
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-diagram-3 me-2 text-info"),
                        html.Span("Panel A: Domain Plane (s = σ + it)", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-domain-plane",
                            style={"height": "380px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        )
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=6),

            # Panel B: Complex Zeta Trace
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-activity me-2 text-success"),
                        html.Span("Panel B: Complex Zeta Trace (Re ζ, Im ζ)", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-zeta-trace",
                            style={"height": "380px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        )
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=6),
        ], className="g-3 mb-1"),

        dbc.Row([
            # Panel C: Riemann Converter
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-bar-chart-steps me-2 text-warning"),
                        html.Span("Panel C: Riemann Converter (Prime Staircase π_N(x))", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-converter",
                            style={"height": "320px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        ),
                        html.Div(id="converter-metrics-display", className="small font-monospace p-2 border-top border-secondary bg-black bg-opacity-25 text-light")
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=6),

            # Panel D: Radial Centrifuge
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-arrow-repeat me-2 text-danger"),
                        html.Span("Panel D: Radial Centrifuge (K ↦ log |q_ρ^K|)", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-centrifuge",
                            style={"height": "380px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        )
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=6),
        ], className="g-3 mb-3"),

        # Row 2: Active Mathematics Card + Controls
        dbc.Row([
            dbc.Col([
                create_active_card_panel()
            ], xs=12, lg=5),
            dbc.Col([
                create_controls_panel()
            ], xs=12, lg=7)
        ], className="g-3 mb-4")
    ])


# ==============================================================================
# TAB 2: CROSS-HEIGHT COHERENCE LABORATORY
# ==============================================================================

def create_cross_height_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-sliders me-2 text-info"),
                        html.Span("Cross-Height Controls & Spectrum Selection", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        html.Label("Select Height Blocks to Compare:", className="small fw-bold text-light"),
                        dbc.Checklist(
                            id="check-ch-blocks",
                            options=[
                                {"label": "Low Validation Block (n=1..10, γ~14..50)", "value": "low_validation"},
                                {"label": "Medium Research Block (n=100..104, γ~236..243)", "value": "medium_research"},
                                {"label": "High Research Block (n=1000..1002, γ~1419..1422)", "value": "high_research"},
                                {"label": "Very High Sparse Block (n=10000..10002, γ~9877..9880)", "value": "very_high_sparse"},
                            ],
                            value=["low_validation", "medium_research", "high_research", "very_high_sparse"],
                            className="text-light small font-monospace mb-3"
                        ),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Relative Zero Index inside Block:", className="small text-light"),
                                dbc.Input(id="input-ch-zero-idx", type="number", value=0, min=0, max=9, step=1, size="sm")
                            ], width=6),
                            dbc.Col([
                                html.Label("Normalized Interval [-u_max, u_max]:", className="small text-light"),
                                dcc.Slider(id="slider-ch-umax", min=0.1, max=1.0, step=0.05, value=0.5,
                                           marks={0.1: "0.1", 0.5: "0.5", 1.0: "1.0"},
                                           tooltip={"placement": "bottom", "always_visible": False})
                            ], width=6)
                        ], className="mb-2"),
                        html.Div(id="ch-selected-zero-info", className="small font-monospace text-info p-2 bg-black bg-opacity-25 border border-secondary rounded")
                    ], className="p-3")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-bezier2 me-2 text-warning"),
                        html.Span("Normalized Derivative-Normalized Trajectory Overlay: u ↦ P_n(u)", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-ch-overlay",
                            style={"height": "340px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        )
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=8),
        ], className="g-3 mb-2"),

        dbc.Row([
            # Deviation Plot
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-graph-up me-2 text-danger"),
                        html.Span("Trajectory Deviation: |P_n(u) - u| vs u", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-ch-deviation",
                            style={"height": "320px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        )
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=6),

            # Distance Matrix Heatmap
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-grid-3x3-gap me-2 text-success"),
                        html.Span("Cross-Height Pairwise Distance Matrix (L^∞ / L_2)", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-ch-matrix",
                            style={"height": "320px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        )
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=6),
        ], className="g-3 mb-2"),

        dbc.Row([
            # Taylor-Shape View
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-bar-chart me-2 text-primary"),
                        html.Span("Taylor Shape Coefficients |c_{2,n}| and |c_{3,n}| vs log(γ_n)", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-ch-taylor",
                            style={"height": "300px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        )
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12)
        ], className="g-3 mb-4")
    ])


# ==============================================================================
# TAB 3: BILATERAL WORLDLINE LABORATORY
# ==============================================================================

def create_worldline_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-sliders me-2 text-info"),
                        html.Span("Worldline & Radial Leaf Parameters", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        html.Label("Select Zero Root (γ):", className="small text-light"),
                        dcc.Dropdown(
                            id="dropdown-wl-zero",
                            options=[
                                {"label": f"Zero #{i+1}: γ = {z:.6f} (Low Block)", "value": z}
                                for i, z in enumerate(INITIAL_ZEROS_FLOAT[:10])
                            ] + [
                                {"label": "Zero #100: γ = 236.524230 (Medium Block)", "value": 236.524230},
                                {"label": "Zero #1000: γ = 1419.422481 (High Block)", "value": 1419.422481},
                                {"label": "Zero #10000: γ = 9877.782654 (Very High Block)", "value": 9877.782654},
                            ],
                            value=INITIAL_ZEROS_FLOAT[0],
                            clearable=False,
                            className="dash-dropdown-dark mb-3"
                        ),
                        html.Label("Bilateral Grade Sweep Range K in [K_min, K_max]:", className="small text-light"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("K_min:", className="small text-secondary"),
                                dbc.Input(id="input-wl-kmin", type="number", value=-5, step=1, size="sm")
                            ], width=6),
                            dbc.Col([
                                html.Label("K_max:", className="small text-secondary"),
                                dbc.Input(id="input-wl-kmax", type="number", value=5, step=1, size="sm")
                            ], width=6),
                        ], className="mb-3"),
                        html.Label("Synthetic Radial Offsets δ = Re(s) - 1/2:", className="small text-light"),
                        dbc.Checklist(
                            id="check-wl-deltas",
                            options=[
                                {"label": "δ = 0.00 (Actual Zero Worldline on Critical Surface)", "value": 0.0},
                                {"label": "δ = +0.10 (Synthetic Coarse Outer Leaf)", "value": 0.10},
                                {"label": "δ = -0.10 (Synthetic Coarse Inner Leaf)", "value": -0.10},
                                {"label": "δ = +0.01 (Synthetic Fine Outer Perturbation)", "value": 0.01},
                                {"label": "δ = -0.01 (Synthetic Fine Inner Perturbation)", "value": -0.01},
                            ],
                            value=[0.0, 0.10, -0.10],
                            className="text-light small font-monospace mb-3"
                        ),

                        html.Div([
                            html.Span("Canonical Grade Sequence: ", className="fw-bold text-light d-block mb-1"),
                            html.Span("... τ⁻², τ⁻¹, τ⁰ = 1 (Native ζ), τ¹, τ², ...", className="font-monospace text-info small")
                        ], className="p-2 border border-secondary rounded bg-black bg-opacity-25")
                    ], className="p-3")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-bounding-box-circles me-2 text-warning"),
                        html.Span("Bilateral Graded Worldlines s_ρ(K) = τ^K · ρ in Complex Plane", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-wl-trajectory",
                            style={"height": "360px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        )
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=8),
        ], className="g-3 mb-2"),

        dbc.Row([
            # Normalized Radial Invariance View
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-shield-check me-2 text-success"),
                        html.Span("Normalized Radial Coordinate Invariance: K ↦ R_τ(s_ρ(K), K) = δ", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-wl-radial",
                            style={"height": "320px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        )
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=6),

            # Defect Scaling View
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-arrows-expand me-2 text-info"),
                        html.Span("Hyperbolic Defect Scaling: |Re(s) - τ^K / 2| = τ^K |δ|", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="graph-wl-defect",
                            style={"height": "320px", "width": "100%"},
                            config={"responsive": True, "scrollZoom": True, "displayModeBar": "hover"}
                        )
                    ], className="p-1")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=6),
        ], className="g-3 mb-4")
    ])


# ==============================================================================
# TAB 4: PROOF PROGRAMME & CURRENT RESEARCH RESULTS
# ==============================================================================

def create_proof_programme_tab():
    # Load index data
    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "research", "index.json")
    runs_list = []
    if os.path.exists(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                idx = json.load(f)
                runs_list = idx.get("runs", [])
        except Exception:
            runs_list = []

    # Load verification report
    rep_ok, rep, rep_errs = certification.load_verification_report()
    cert_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "certificates")
    zeros_count = len(glob.glob(os.path.join(cert_dir, "zeros", "*.json")))
    trivial_count = len(glob.glob(os.path.join(cert_dir, "trivial_zeros", "*.json")))
    blocks_count = len(glob.glob(os.path.join(cert_dir, "blocks", "*.json")))
    worldlines_count = len(glob.glob(os.path.join(cert_dir, "worldlines", "*.json")))
    inventory_count = zeros_count + trivial_count + blocks_count + worldlines_count

    if rep_ok and rep:
        status_color = "success"
        flint_v = rep.get("dependency_fingerprint", {}).get("python_flint", "0.6.0")
        commit_s = str(rep.get("producing_git_commit", "clean"))[:7]
        cert_alert = dbc.Alert(
            f"Certification Status: VERIFIED ({rep.get('passed_count')}/{rep.get('total_inventory')} certificates valid, 0 failures) — Engine: python-flint {flint_v} (Commit {commit_s})",
            color="success",
            className="small py-2 mb-0 font-monospace"
        )
        stage2_status, stage2_color = "Rigorously Certified (FLINT Arb)", "success"
        stage3_status, stage3_color = "Rigorously Certified (FLINT Arb)", "success"
        stage4_status, stage4_color = "Formally Proved & Certified", "success"
    elif rep and rep.get("failed_count", 0) > 0:
        cert_alert = dbc.Alert(
            f"Certification Status: FAILED ({rep.get('failed_count')} certificate failures detected). Failures: {rep.get('failures', [])[:2]}",
            color="danger",
            className="small py-2 mb-0 font-monospace"
        )
        stage2_status, stage2_color = "UNVERIFIED / FAILING", "danger"
        stage3_status, stage3_color = "UNVERIFIED / FAILING", "danger"
        stage4_status, stage4_color = "UNVERIFIED / FAILING", "danger"
    else:
        err_msg = rep_errs[0] if rep_errs else "report absent or stale"
        cert_alert = dbc.Alert(
            f"Certification Status: UNVERIFIED ({err_msg}). Run `python scripts/verify_certificates.py` to certify.",
            color="secondary",
            className="small py-2 mb-0 font-monospace"
        )
        stage2_status, stage2_color = "UNVERIFIED", "secondary"
        stage3_status, stage3_color = "UNVERIFIED", "secondary"
        stage4_status, stage4_color = "UNVERIFIED", "secondary"

    prog_stages = [
        {"stage": "1. Bilateral Continuation", "requirement": "Construct graded family Z_tau(s, k) = zeta(tau^(-k) s)", "status": "Constructed & Formally Checked (Lean 4)", "color": "success"},
        {"stage": "2. Native Zero Blocks", "requirement": "Rigorously certify zero isolation and simplicity in Arb", "status": stage2_status, "color": stage2_color},
        {"stage": "3. Worldline Covariance", "requirement": "Z_tau(tau^K rho, K) = zeta(rho) for all K in Z", "status": stage3_status, "color": stage3_color},
        {"stage": "4. Radial Invariance", "requirement": "R_tau(s_rho(k), k) = delta invariant across all grades", "status": stage4_status, "color": stage4_color},
        {"stage": "5. Cross-Height Observations", "requirement": "Evaluate normalized trajectory distances L_inf, L_2", "status": "Active Research Campaign", "color": "info"},
        {"stage": "6. Exact Global Coherence Law", "requirement": "Derive universal multi-height trajectory constraint law", "status": "OPEN RESEARCH TARGET (Missing)", "color": "warning"},
        {"stage": "7. Coherence => Radial Rigidity", "requirement": "Prove global coherence forbids multiple occupied radial leaves", "status": "OPEN RESEARCH TARGET (Missing)", "color": "danger"},
        {"stage": "8. Contradiction (delta_0 = 0)", "requirement": "Functional equation reflection closes unique radial class: delta_0 = -delta_0 => delta_0 = 0", "status": "Not Reached (Conditional on Rigidity)", "color": "secondary"},
    ]

    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-diagram-2 me-2 text-warning"),
                        html.Span("Proof-Programme Logical Dependency Obligations Map", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        html.P(
                            "This status panel tracks the formal and computational proof obligations of the transcendental continuation programme. "
                            "Notice that the missing deductive link (Stage 6-7: zeta-specific global coherence => radial rigidity) remains explicitly highlighted as open research and is not assumed as a premise.",
                            className="small text-secondary mb-3"
                        ),
                        html.Table([
                            html.Thead([
                                html.Tr([
                                    html.Th("Programme Stage"),
                                    html.Th("Required Mathematical State"),
                                    html.Th("Instrument Status"),
                                ])
                            ]),
                            html.Tbody([
                                html.Tr([
                                    html.Td(st["stage"], className="fw-bold"),
                                    html.Td(st["requirement"], className="small"),
                                    html.Td(dbc.Badge(st["status"], color=st["color"], className="p-1 font-monospace small")),
                                ]) for st in prog_stages
                            ])
                        ], className="table table-dark table-sm table-striped border-secondary mb-0")
                    ], className="p-3")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-award me-2 text-success"),
                        html.Span(f"Machine-Verifiable Certificate Inventory ({inventory_count} Artifacts)", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        html.P(
                            "Rigorous mathematical certificates generated via FLINT/Arb ball arithmetic and verified independently via SHA-256 and ball enclosure bounds.",
                            className="small text-secondary mb-2"
                        ),
                        html.Ul([
                            html.Li([html.Strong(f"Nontrivial Zero Certificates ({zeros_count}): "), "Certified simple zeros across 4 spectrum blocks (Low n=1..100, Medium n=100..104, High n=1000..1002, Very High n=10000..10002). 0 ∉ ζ'(B_n) verified in Arb."], className="small text-light mb-1"),
                            html.Li([html.Strong(f"Trivial Zero Controls ({trivial_count}): "), "Certified trivial zeros s_m = -2m (m=1..100) with non-vanishing derivative 0 ∉ ζ'(-2m) proving simplicity and local isolation."], className="small text-light mb-1"),
                            html.Li([html.Strong(f"Block Certificates ({blocks_count}): "), f"{blocks_count} complete block certificates verifying Turing zero counts N(t_max)-N(t_min) and consecutiveness."], className="small text-light mb-1"),
                            html.Li([html.Strong(f"Worldline Certificates ({worldlines_count}): "), f"{worldlines_count} bilateral worldline certificates across grades K in [-5..5] and radial leaves δ."], className="small text-light mb-1"),
                        ]),
                        cert_alert
                    ], className="p-3")
                ], className="border-secondary shadow-sm mb-3")
            ], xs=12, lg=6),
        ], className="g-3 mb-2"),


        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="bi bi-journal-code me-2 text-info"),
                        html.Span(f"Current Canonical Research Experiment Results ({len(runs_list)} Active Sweeps)", className="fw-bold small text-light")
                    ], className="py-1 px-3 bg-dark border-secondary"),
                    dbc.CardBody([
                        html.Table([
                            html.Thead([
                                html.Tr([
                                    html.Th("Experiment ID"),
                                    html.Th("Epistemic Class"),
                                    html.Th("Status"),
                                    html.Th("Criterion Met"),
                                    html.Th("Source Commit"),
                                    html.Th("Dirty"),
                                ])
                            ]),
                            html.Tbody([
                                html.Tr([
                                    html.Td(r.get("experiment_id"), className="font-monospace small fw-bold"),
                                    html.Td(dbc.Badge(r.get("epistemic_class", "exact_control"), color="info" if r.get("epistemic_class") == "exact_control" else ("warning" if r.get("epistemic_class") == "observational_pattern" else "secondary"), className="p-1")),
                                    html.Td(r.get("status")),
                                    html.Td(
                                        dbc.Badge("PASS", color="success", className="p-1") if r.get("criterion_met") is True
                                        else (dbc.Badge("OBSERVATIONAL", color="info", className="p-1") if r.get("criterion_met") is None else dbc.Badge("FAIL", color="danger", className="p-1"))
                                    ),
                                    html.Td(r.get("git_commit", "N/A")[:8], className="font-monospace small"),
                                    html.Td(str(r.get("git_dirty", False))),
                                ]) for r in runs_list
                            ])
                        ], className="table table-dark table-sm table-striped border-secondary mb-0")
                    ], className="p-3")
                ], className="border-secondary shadow-sm mb-4")
            ], xs=12)
        ], className="g-3 mb-4")
    ])


# ==============================================================================
# MODALS & EXPORT DEFINITIONS
# ==============================================================================

def create_validation_modal():
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Independent Zero Discovery & Reference Validation"), className="bg-dark text-light border-secondary"),
        dbc.ModalBody([
            html.P("At baseline k=0, zeros are discovered via independent Hardy Z(t) scanning and certified root refinement before comparison to reference tables.", className="small text-secondary"),
            html.Div(id="val-report-content", className="font-monospace small")
        ], className="bg-dark text-light"),
        dbc.ModalFooter(
            dbc.Button("Close", id="btn-close-modal", className="ms-auto", color="secondary", size="sm"),
            className="bg-dark border-secondary"
        )
    ], id="modal-val-report", size="lg", is_open=False)


def create_export_modal():
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Export Current State as Sweep Draft"), className="bg-dark text-light border-secondary"),
        dbc.ModalBody([
            html.P("Export current transformation parameters, sampling bounds, and Active Mathematics metadata as a declarative YAML experiment spec conforming to EXPERIMENT_PROTOCOL.md.", className="small text-secondary"),
            dcc.Textarea(
                id="textarea-sweep-draft",
                style={"width": "100%", "height": "340px", "backgroundColor": "#12151c", "color": "#00ff88", "fontFamily": "monospace", "fontSize": "12px"},
                readOnly=True
            ),
            dcc.Download(id="download-sweep-yaml")
        ], className="bg-dark text-light"),
        dbc.ModalFooter([
            dbc.Button([html.I(className="bi bi-download me-1"), "Download .yaml"], id="btn-download-yaml", color="success", size="sm", className="me-2"),
            dbc.Button("Close", id="btn-close-export-modal", color="secondary", size="sm")
        ], className="bg-dark border-secondary")
    ], id="modal-export-sweep", size="lg", is_open=False)


# ==============================================================================
# MAIN APP LAYOUT
# ==============================================================================

app.layout = html.Div([
    create_header(),
    create_validation_modal(),
    create_export_modal(),
    dcc.Store(id="store-audit-mode", data=False),
    dcc.Store(id="store-discovered-zeros", data=INITIAL_ZEROS_FLOAT),

    dbc.Container([
        dbc.Tabs([
            dbc.Tab(label="Microscope / Macroscope (4-Panel Visualizer)", tab_id="tab-instrument", children=create_instrument_tab()),
            dbc.Tab(label="Cross-Height Coherence Laboratory", tab_id="tab-cross-height", children=create_cross_height_tab()),
            dbc.Tab(label="Bilateral Worldline Laboratory", tab_id="tab-worldline", children=create_worldline_tab()),
            dbc.Tab(label="Proof Programme & Canonical Research Results", tab_id="tab-proof-programme", children=create_proof_programme_tab()),
        ], id="main-nav-tabs", active_tab="tab-instrument", className="mb-3")
    ], fluid=True)
], style={"backgroundColor": "#090c10", "minHeight": "100vh", "color": "#e2e8f0"})


# ==============================================================================
# INTERACTIVE CALLBACKS
# ==============================================================================

@app.callback(
    [
        Output("container-mode-transcendental", "style"),
        Output("container-mode-scale", "style"),
        Output("container-mode-kernel", "style"),
        Output("container-mode-centered-kernel", "style"),
        Output("container-mode-aniso", "style"),
    ],
    Input("transform-mode-select", "value")
)
def toggle_mode_control_visibility(mode: str):
    show = {"display": "block"}
    hide = {"display": "none"}
    return (
        show if mode == "transcendental" else hide,
        show if mode in ["height", "origin_dilation", "centered_dilation", "argument"] else hide,
        show if mode == "kernel_lab" else hide,
        show if mode == "centered_kernel" else hide,
        show if mode == "anisotropic" else hide,
    )


@app.callback(
    [
        Output("subcontainer-grade-integer", "style"),
        Output("subcontainer-grade-rational", "style"),
        Output("subcontainer-grade-continuous", "style"),
        Output("subcontainer-grade-generic", "style"),
    ],
    Input("radio-grade-type", "value")
)
def toggle_grade_subcontainers(grade_type: str):
    show = {"display": "block"}
    hide = {"display": "none"}
    return (
        show if grade_type == "integer_tau" else hide,
        show if grade_type == "rational_tau" else hide,
        show if grade_type == "continuous_tau" else hide,
        show if grade_type == "generic_scale" else hide,
    )


@app.callback(
    Output("input-grade-k-int", "value"),
    [
        Input("btn-k-minus", "n_clicks"),
        Input("btn-k-plus", "n_clicks"),
        Input("btn-k-reset-zero", "n_clicks"),
    ],
    State("input-grade-k-int", "value"),
    prevent_initial_call=True
)
def step_integer_grade(n_minus, n_plus, n_reset, current_k):
    t_id = ctx.triggered_id
    curr = int(current_k or 0)
    if t_id == "btn-k-minus":
        return curr - 1
    elif t_id == "btn-k-plus":
        return curr + 1
    elif t_id == "btn-k-reset-zero":
        return 0
    return curr


@app.callback(
    Output("comp-result-display", "children"),
    Input("btn-comp-derive", "n_clicks"),
    [
        State("input-comp-source", "value"),
        State("input-comp-target", "value"),
    ],
    prevent_initial_call=True
)
def compute_compression_summary(n_clicks, src_h, tgt_h):
    if src_h and tgt_h and src_h > 0 and tgt_h > 0:
        info = transcendental.derive_compression_grade(str(src_h), str(tgt_h), dps=30)
        return html.Div([
            html.Span(f"Derived continuous grade: k = {info['k']:.6f} | Scale factor A = {info['scale_A']:.6f}", className="d-block"),
            html.Span(f"Nearest integer grade: K = {info['nearest_integer_K']} (error Δk = {info['integer_defect']:.4f})", className="d-block text-info")
        ])
    return "Enter positive source and target heights."


@app.callback(
    Output("input-delta-pert", "value"),
    [
        Input("preset-0", "n_clicks"),
        Input("preset-1e8", "n_clicks"),
        Input("preset-1e6", "n_clicks"),
        Input("preset-1e4", "n_clicks"),
        Input("preset-1e2", "n_clicks"),
    ],
    prevent_initial_call=True
)
def set_delta_preset(p0, p1e8, p1e6, p1e4, p1e2):
    t_id = ctx.triggered_id
    presets = {
        "preset-0": 0.0,
        "preset-1e8": 1e-8,
        "preset-1e6": 1e-6,
        "preset-1e4": 1e-4,
        "preset-1e2": 1e-2,
    }
    return presets.get(t_id, 0.0)


@app.callback(
    Output("input-gamma-pert", "value"),
    Input("dropdown-selected-zero", "value"),
    State("store-discovered-zeros", "data")
)
def update_gamma_from_dropdown(selected_idx, disc_zeros):
    zeros = disc_zeros or INITIAL_ZEROS_FLOAT
    if selected_idx is not None and 0 <= selected_idx < len(zeros):
        return zeros[selected_idx]
    return 14.134725


@app.callback(
    [Output("modal-val-report", "is_open"), Output("val-report-content", "children")],
    [Input("btn-val-report", "n_clicks"), Input("btn-close-modal", "n_clicks")],
    State("modal-val-report", "is_open"),
    prevent_initial_call=True
)
def toggle_validation_report_modal(n_open, n_close, is_open):
    if not is_open:
        report = zero_finder.generate_baseline_validation_report(dps=40)
        prov = reference_data.load_provenance()
        ref_meta = prov.get("reference_datasets", {}).get("zeta_zeros", {})
        source_name = ref_meta.get("source", "Odlyzko Tables")
        sha_str = ref_meta.get("sha256", "N/A")[:16] + "..." if ref_meta.get("sha256") else "N/A"

        content = html.Div([
            html.Table([
                html.Tr([html.Th("Validation Status:"), html.Td(dbc.Badge("PASS", color="success") if report["status"] == "PASS" else dbc.Badge("FAIL", color="danger"))]),
                html.Tr([html.Th("Zeros Evaluated:"), html.Td(str(report["zeros_evaluated"]))]),
                html.Tr([html.Th("Max Ordinate Discrepancy:"), html.Td(f"{report['max_difference']:.2e}")]),
                html.Tr([html.Th("RMS Ordinate Difference:"), html.Td(f"{report['rms_difference']:.2e}")]),
                html.Tr([html.Th("Max Residual |ζ(1/2+iγ)|:"), html.Td(f"{report['max_residual']:.2e}")]),
                html.Tr([html.Th("Discovery Engine:"), html.Td("Hardy Z(t) Sign Change + Brent Root Refinement")]),
                html.Tr([html.Th("Reference Source:"), html.Td(source_name)]),
                html.Tr([html.Th("Provenance SHA-256:"), html.Td(sha_str)])
            ], className="table table-dark table-sm table-striped mt-2")
        ])
        return True, content
    return False, dash.no_update


@app.callback(
    [Output("modal-export-sweep", "is_open"), Output("textarea-sweep-draft", "value")],
    [Input("btn-export-sweep", "n_clicks"), Input("btn-close-export-modal", "n_clicks")],
    [
        State("modal-export-sweep", "is_open"),
        State("transform-mode-select", "value"),
        State("slider-t0", "value"),
        State("slider-dt", "value"),
        State("slider-delta-offset", "value"),
        State("dropdown-selected-zero", "value"),
        State("input-delta-pert", "value"),
        State("input-gamma-pert", "value"),
        State("slider-num-zeros", "value"),
        State("radio-cert-mode", "value"),
        State("slider-k", "value"),
        State("slider-kernel-A", "value"),
        State("slider-kernel-B", "value"),
        State("input-kernel-C", "value"),
        State("input-kernel-D", "value"),
        State("check-kernel-lock", "value"),
        State("slider-centered-kernel-A", "value"),
        State("slider-aniso-delta", "value"),
        State("slider-aniso-gamma", "value"),
    ],
    prevent_initial_call=True
)
def toggle_export_modal(
    n_open, n_close, is_open,
    mode, t0, dt, delta_offset, selected_zero_idx, delta_pert, gamma_pert, num_zeros, cert_mode,
    k_val, kA, kB, kC, kD, k_lock, cA, aniso_d, aniso_g
):
    if not is_open:
        op = "transcendental_worldline" if mode == "transcendental" else "zeta_trace_compare"
        dps = 80 if cert_mode in ["audit", "certified"] else 35
        k_str = f"{k_val:.4g}" if k_val is not None else "0.0"
        d_str = f"{delta_pert:.6g}" if delta_pert is not None else "0.0"
        g_str = f"{gamma_pert:.6g}" if gamma_pert is not None else "14.134725"

        yaml_text = f"""schema_version: "2"
id: sweep-draft-{mode.replace('_', '-')}-001
title: "Interactive Sweep Draft — {mode.replace('_', ' ').title()}"
epistemic_class: exact_control
object_relationship: same_object_coordinate_control

hypothesis:
  statement: "State the exact mathematical hypothesis to test over this parameter space."

criterion:
  metric: max_residual
  operator: "<="
  threshold: "1e-35"

engine:
  operation: {op}

parameters:
  k:
    kind: explicit
    values: ["{k_str}"]
  delta:
    kind: explicit
    values: ["{d_str}"]
  gamma:
    kind: explicit
    values: ["{g_str}"]

precision:
  dps: {dps}

outputs:
  retain_points: true
"""
        return True, yaml_text
    return False, dash.no_update


@app.callback(
    Output("download-sweep-yaml", "data"),
    Input("btn-download-yaml", "n_clicks"),
    State("textarea-sweep-draft", "value"),
    prevent_initial_call=True
)
def download_sweep_yaml(n_clicks, yaml_content):
    if yaml_content:
        return dict(content=yaml_content, filename="sweep_draft.yaml")
    return dash.no_update


# ==============================================================================
# MAIN SYNCHRONIZED UPDATE CALLBACK (4 Panels + Active Math Card)
# ==============================================================================

@app.callback(
    [
        Output("active-math-card", "children"),
        Output("graph-domain-plane", "figure"),
        Output("graph-zeta-trace", "figure"),
        Output("graph-converter", "figure"),
        Output("graph-centrifuge", "figure"),
        Output("converter-metrics-display", "children"),
    ],
    [
        Input("transform-mode-select", "value"),
        Input("slider-t0", "value"),
        Input("slider-dt", "value"),
        Input("slider-delta-offset", "value"),
        Input("dropdown-selected-zero", "value"),
        Input("input-delta-pert", "value"),
        Input("input-gamma-pert", "value"),
        Input("slider-num-zeros", "value"),
        Input("radio-cert-mode", "value"),
        Input("slider-k", "value"),
        Input("slider-kernel-A", "value"),
        Input("slider-kernel-B", "value"),
        Input("input-kernel-C", "value"),
        Input("input-kernel-D", "value"),
        Input("check-kernel-lock", "value"),
        Input("slider-centered-kernel-A", "value"),
        Input("check-centered-kernel-lock", "value"),
        Input("slider-aniso-delta", "value"),
        Input("slider-aniso-gamma", "value"),
        Input("radio-perturb-mode", "value"),
        Input("radio-grade-type", "value"),
        Input("input-grade-k-int", "value"),
        Input("input-grade-q-rat", "value"),
        Input("slider-grade-k-cont", "value"),
        Input("input-generic-scale", "value"),
        Input("input-generic-base", "value"),
    ],
    State("store-discovered-zeros", "data")
)
def update_all_panels(
    mode: str,
    t0: Optional[float],
    dt: Optional[float],
    delta_offset: Optional[float],
    selected_zero_idx: Optional[int],
    delta_pert: Optional[float],
    gamma_pert: Optional[float],
    num_zeros: Optional[int],
    cert_mode: str,
    k_val: Optional[float],
    kA: Optional[float],
    kB: Optional[float],
    kC: Optional[float],
    kD: Optional[float],
    k_lock: Optional[List[str]],
    cA: Optional[float],
    c_lock: Optional[List[str]],
    aniso_d: Optional[float],
    aniso_g: Optional[float],
    perturb_mode_val: Optional[str],
    grade_type_val: Optional[str],
    grade_k_int: Optional[int],
    grade_q_rat: Optional[str],
    grade_k_cont: Optional[float],
    gen_scale: Optional[float],
    gen_base: Optional[float],
    disc_zeros: Optional[List[float]]
):
    dps = 80 if cert_mode in ["audit", "certified"] else 35
    n_samples = 500 if cert_mode in ["audit", "certified"] else 250

    t0_val = t0 if t0 is not None else 14.0
    dt_val = dt if dt is not None else 20.0
    delta_offset_val = delta_offset if delta_offset is not None else 0.0
    selected_idx_val = selected_zero_idx if selected_zero_idx is not None else 0
    delta_pert_val = delta_pert if delta_pert is not None else 0.0
    gamma_pert_val = gamma_pert if gamma_pert is not None else INITIAL_ZEROS_FLOAT[0]
    num_zeros_val = num_zeros if num_zeros is not None else 15
    k = k_val if k_val is not None else 0.0

    # 1. Instantiate active Transform Object
    transform_obj: transforms.BaseTransform
    if mode == "transcendental":
        g_type = grade_type_val or "integer_tau"
        if g_type == "integer_tau":
            k_int = grade_k_int if grade_k_int is not None else 0
            grade_obj = transcendental.IntegerTauGrade(K=k_int)
        elif g_type == "rational_tau":
            q_str = grade_q_rat or "1/2"
            grade_obj = transcendental.RationalTauGrade.from_str(q_str)
        elif g_type == "continuous_tau":
            k_cont = grade_k_cont if grade_k_cont is not None else 0.0
            grade_obj = transcendental.ContinuousGrade.from_value(k_cont)
        else:
            a_gen = str(gen_scale if gen_scale is not None else 1.0)
            b_gen = str(gen_base if gen_base is not None else 10.0)
            grade_obj = transcendental.GenericScale(A_str=a_gen, base_str=b_gen)
        transform_obj = transforms.TranscendentalContinuationTransform(grade=grade_obj)
    elif mode == "camera":
        transform_obj = transforms.CameraTransform()
    elif mode == "height":
        transform_obj = transforms.HeightMicroscopeTransform(k=k, t0=t0_val, delta=delta_offset_val)
    elif mode == "origin_dilation":
        transform_obj = transforms.OriginCoordinateDilation(k=k)
    elif mode == "centered_dilation":
        transform_obj = transforms.CenteredCoordinateDilation(k=k)
    elif mode == "argument":
        transform_obj = transforms.ArgumentTransform(k=k)
    elif mode == "kernel_lab":
        A = kA if kA is not None else 1.0
        is_locked = bool(k_lock and "lock" in k_lock)
        B = (1.0 / A) if is_locked else (kB if kB is not None else 1.0)
        C = kC if kC is not None else 0.0
        D = kD if kD is not None else 0.0
        transform_obj = transforms.KernelTransform(A=A, B=B, C=C, D=D, inverse_scale_lock=is_locked)
    elif mode == "centered_kernel":
        A = cA if cA is not None else 1.0
        is_locked = bool(c_lock and "lock" in c_lock)
        transform_obj = transforms.CenteredKernelTransform(A=A, inverse_scale_lock=is_locked)
    elif mode == "anisotropic":
        A_del = aniso_d if aniso_d is not None else 1.0
        A_gam = aniso_g if aniso_g is not None else 1.0
        transform_obj = transforms.AnisotropicDeformation(A_delta=A_del, A_gamma=A_gam)
    else:
        transform_obj = transforms.CameraTransform()

    # Active Card Text
    card_md = transform_obj.get_card_markdown()

    # Compute Complex Trace via Cache
    u_vals, s_coords, re_w, im_w = cache.get_cached_trace(
        transform_obj, t0_val, dt_val, delta_offset_val, n_samples=n_samples, dps=dps
    )

    # Panel A: Domain Plane
    fig_a = go.Figure(layout=DARK_LAYOUT)
    img_re = None
    if isinstance(transform_obj, transforms.TranscendentalContinuationTransform):
        scale_val = float(transform_obj.grade.numeric_scale(dps=15))
        img_re = scale_val / 2.0
    elif isinstance(transform_obj, transforms.OriginCoordinateDilation):
        img_re = transform_obj.scale / 2.0
    elif isinstance(transform_obj, transforms.ArgumentTransform):
        img_re = 1.0 / (2.0 * transform_obj.scale)
    elif isinstance(transform_obj, transforms.KernelTransform):
        if abs(transform_obj.A * transform_obj.B) > 1e-12:
            img_re = (0.5 / transform_obj.A - transform_obj.D) / transform_obj.B

    max_s_re = float(np.max(s_coords.real)) if len(s_coords) > 0 else 0.5
    min_s_re = float(np.min(s_coords.real)) if len(s_coords) > 0 else 0.5
    target_max_x = max(4.0, (img_re * 1.3) if img_re else 4.0, max_s_re + 1.0)
    target_min_x = min(-1.0, min_s_re - 1.0)

    x_min_a, x_max_a = target_min_x, target_max_x
    y_min_a, y_max_a = float(np.min(s_coords.imag)) - 2.0, float(np.max(s_coords.imag)) + 2.0
    dtick_a = compute_matching_dtick(x_max_a - x_min_a, target_ticks=6)

    fig_a.update_layout(
        title=dict(text="Panel A: Domain Plane (s = σ + it)", font=dict(size=12)),
        xaxis=dict(range=[x_min_a, x_max_a], title="Re(s)", dtick=dtick_a, tick0=0),
        yaxis=dict(range=[y_min_a, y_max_a], title="Im(s)", scaleanchor="x", scaleratio=1.0, constrain="range", dtick=dtick_a, tick0=0)
    )

    # Original Critical Line Re(s) = 1/2
    fig_a.add_trace(go.Scatter(
        x=[0.5, 0.5], y=[y_min_a - 10.0, y_max_a + 10.0],
        mode="lines", line=dict(color="#4a5568", dash="dash", width=1.5),
        name="Original Critical Line (Re=1/2)"
    ))

    if img_re is not None and abs(img_re - 0.5) > 1e-4:
        fig_a.add_trace(go.Scatter(
            x=[img_re, img_re], y=[y_min_a - 10.0, y_max_a + 10.0],
            mode="lines", line=dict(color="#00d2ff", dash="dot", width=1.5),
            name="Transformed Critical Surface (Re = τ^k/2)"
        ))

    # Active Sampling Segment s(u)
    fig_a.add_trace(go.Scatter(
        x=s_coords.real, y=s_coords.imag,
        mode="lines", line=dict(color="#00ff88", width=3),
        name="Sampling Path s(u)"
    ))

    # Plot Discovered Zeros in Range
    zeros_in_view = [z for z in (disc_zeros or INITIAL_ZEROS_FLOAT) if (y_min_a - 5.0) <= z <= (y_max_a + 5.0)]
    mapped_zeros_re = []
    mapped_zeros_im = []
    for z in zeros_in_view:
        mapped_z = transform_obj.map_zero(complex(0.5, z))
        mapped_zeros_re.append(mapped_z.real)
        mapped_zeros_im.append(mapped_z.imag)

    fig_a.add_trace(go.Scatter(
        x=mapped_zeros_re, y=mapped_zeros_im,
        mode="markers", marker=dict(color="#ff007f", size=7, symbol="circle"),
        name="Zeta Zeros"
    ))

    # Highlight Selected Zero
    selected_rho = complex(0.5 + delta_pert_val, gamma_pert_val)
    mapped_selected = transform_obj.map_zero(selected_rho)
    fig_a.add_trace(go.Scatter(
        x=[mapped_selected.real], y=[mapped_selected.imag],
        mode="markers", marker=dict(color="#ffea00", size=11, symbol="star"),
        name="Selected Zero"
    ))

    # Panel B: Complex Zeta Trace
    fig_b = go.Figure(layout=DARK_LAYOUT)
    max_trace_val = max(float(np.max(np.abs(re_w))), float(np.max(np.abs(im_w))), 1.5)
    r_limit = max_trace_val * 1.15
    dtick_b = 1.0

    fig_b.update_layout(
        title=dict(text="Panel B: Complex Zeta Trace (Re ζ, Im ζ)", font=dict(size=12)),
        xaxis=dict(range=[-r_limit, r_limit], title="Re ζ(s(u))", dtick=dtick_b, tick0=0),
        yaxis=dict(range=[-r_limit, r_limit], title="Im ζ(s(u))", scaleanchor="x", scaleratio=1.0, constrain="range", dtick=dtick_b, tick0=0)
    )

    fig_b.add_trace(go.Scatter(
        x=[0], y=[0],
        mode="markers", marker=dict(color="#ff007f", size=8, symbol="cross"),
        name="Origin (0,0)"
    ))

    fig_b.add_trace(go.Scatter(
        x=re_w, y=im_w,
        mode="lines",
        line=dict(color="#00d2ff", width=2.5),
        name="Zeta Trace"
    ))

    # Panel C: Riemann Converter
    fig_c = go.Figure(layout=DARK_LAYOUT)
    x_min_c, x_max_c = 0.0, 50.0
    y_min_c, y_max_c = 0.0, 16.0
    dtick_c = 5.0

    fig_c.update_layout(
        title=dict(text=f"Panel C: Prime Reconstruction π_N(x) (N={num_zeros_val})", font=dict(size=12)),
        xaxis=dict(range=[x_min_c, x_max_c], title="x", dtick=dtick_c, tick0=0),
        yaxis=dict(range=[y_min_c, y_max_c], title="Count π(x)", scaleanchor="x", scaleratio=1.0, constrain="range", dtick=dtick_c, tick0=0)
    )

    rec_cache = cache.get_converter_cache(max_x=50.0, n_points=300)
    x_pts = rec_cache.x_grid

    true_pi = reference_data.prime_pi_array(x_pts)
    fig_c.add_trace(go.Scatter(
        x=x_pts, y=true_pi,
        mode="lines", line=dict(color="#a0aec0", width=1.5, shape="hv"),
        name="True Prime Count π(x)"
    ))

    perturb_mode = perturb_mode_val if perturb_mode_val is not None else "single_pair_diagnostic"
    clean_gamma = INITIAL_ZEROS_FLOAT[selected_idx_val] if selected_idx_val < len(INITIAL_ZEROS_FLOAT) else 14.134725
    clean_rho_val = complex(0.5, clean_gamma)

    clean_pi, pert_pi = rec_cache.reconstruct_pi_perturbed(
        num_zeros=num_zeros_val,
        perturbed_zero_idx=selected_idx_val,
        delta=delta_pert_val,
        gamma=gamma_pert_val,
        mode=perturb_mode
    )

    fig_c.add_trace(go.Scatter(
        x=x_pts, y=clean_pi,
        mode="lines", line=dict(color="#00d2ff", width=2),
        name="Clean π_N(x)"
    ))

    if abs(delta_pert_val) > 1e-12:
        fig_c.add_trace(go.Scatter(
            x=x_pts, y=pert_pi,
            mode="lines", line=dict(color="#ffea00", width=2, dash="dash"),
            name="Perturbed π_N(x)"
        ))


    eval_x = 20.0
    cj_c = converter.zero_j_contribution_preview(eval_x, clean_rho_val)
    cpi_c = converter.zero_pi_contribution_preview(eval_x, clean_rho_val)
    if perturb_mode == "symmetry_complete_quartet":
        if abs(delta_pert_val) < 1e-12:
            cj_p = cj_c
            cpi_p = cpi_c
        else:
            rp = complex(0.5 + delta_pert_val, gamma_pert_val)
            rm = complex(0.5 - delta_pert_val, gamma_pert_val)
            cj_p = converter.zero_j_contribution_preview(eval_x, rp) + converter.zero_j_contribution_preview(eval_x, rm)
            cpi_p = converter.zero_pi_contribution_preview(eval_x, rp) + converter.zero_pi_contribution_preview(eval_x, rm)
    else:
        r_pert = complex(0.5 + delta_pert_val, gamma_pert_val)
        cj_p = converter.zero_j_contribution_preview(eval_x, r_pert)
        cpi_p = converter.zero_pi_contribution_preview(eval_x, r_pert)

    idx_20 = int(np.argmin(np.abs(x_pts - 20.0)))
    pi_clean_20 = clean_pi[idx_20]
    pi_pert_20 = pert_pi[idx_20]

    mode_label = "SINGLE-PAIR DIAGNOSTIC" if perturb_mode == "single_pair_diagnostic" else "SYMMETRY-COMPLETE QUARTET"

    # Certification Badge in Certified Mode (Fails Closed with FLINT Replay Verification)
    cert_badge = None
    if cert_mode == "certified":
        cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "certificates", "zeros", f"zero_{selected_idx_val+1:05d}.json")
        if os.path.exists(cert_path):
            is_valid, zc, errs = certification.load_and_verify_certificate(cert_path)
            if is_valid and zc is not None:
                rad_disp = str(zc.get("enclosure", {}).get("imag_rad", ""))[:12]
                cert_badge = dbc.Badge(
                    f"CERTIFIED: Zero #{selected_idx_val+1} simple zero | Enclosure radius: {rad_disp}... | 0 ∉ ζ'(B_{selected_idx_val+1}) | SHA-256 verified",
                    color="success",
                    className="p-1 d-block mb-1 font-monospace"
                )
            else:
                err_str = "; ".join(errs) if errs else "Unknown validation error"
                cert_badge = dbc.Badge(
                    f"CERTIFICATION REJECTED: Zero #{selected_idx_val+1} verification failed: {err_str}",
                    color="danger",
                    className="p-1 d-block mb-1 font-monospace"
                )
        else:
            cert_badge = dbc.Badge(f"CERTIFICATE MISSING: Zero #{selected_idx_val+1} not in certificate store", color="warning", className="p-1 d-block mb-1")

    metrics_ui = html.Div([
        cert_badge if cert_badge else html.Div(),
        html.Div([
            dbc.Badge(f"MODE: {mode_label}", color="warning" if perturb_mode == "single_pair_diagnostic" else "info", className="me-2 p-1"),
            html.Span(f"Selected ρ: 0.5000 + {delta_pert_val:+.4f} + {gamma_pert_val:.4f}i", className="text-warning fw-bold small")
        ], className="mb-1"),
        html.Div([
            html.Span(f"C_J(x=20): clean={cj_c:.6f} | pert={cj_p:.6f} | Δ={cj_p - cj_c:+.6f}", className="d-block text-secondary small"),
            html.Span(f"C_π(x=20): clean={cpi_c:.6f} | pert={cpi_p:.6f} | Δ={cpi_p - cpi_c:+.6f}", className="d-block text-secondary small"),
            html.Span(f"π_N(x=20): clean={pi_clean_20:.4f} | pert={pi_pert_20:.4f} | Δ={pi_pert_20 - pi_clean_20:+.4f}", className="d-block text-info small fw-bold")
        ])
    ])

    # Panel D: Radial Centrifuge
    fig_d = go.Figure(layout=DARK_LAYOUT)
    x_min_d, x_max_d = -20.0, 20.0
    tau_approx = 2.0 * np.pi
    y_limit_d = max(1.0, 20.0 * abs(delta_pert_val) * np.log(tau_approx) * 1.25)
    dtick_d = 5.0

    fig_d.update_layout(
        title=dict(text=f"Panel D: Centrifuge log |q_ρ^K| = K·δ·ln(τ) (δ={delta_pert_val:.4g})", font=dict(size=12)),
        xaxis=dict(range=[x_min_d, x_max_d], title="Grade K", dtick=dtick_d, tick0=0),
        yaxis=dict(range=[-y_limit_d, y_limit_d], title="log |q_ρ^K|", scaleanchor="x", scaleratio=1.0, constrain="range", dtick=dtick_d, tick0=0)
    )

    k_grid = np.linspace(-20.0, 20.0, 100)
    log_mod_vals = k_grid * delta_pert_val * np.log(tau_approx)

    fig_d.add_trace(go.Scatter(
        x=k_grid, y=log_mod_vals,
        mode="lines", line=dict(color="#ffea00", width=2.5),
        name="Amplification Line"
    ))

    fig_d.add_trace(go.Scatter(
        x=[-20, 20], y=[0, 0],
        mode="lines", line=dict(color="#4a5568", dash="dash", width=1),
        name="On-Line Invariant (δ=0)"
    ))

    return card_md, fig_a, fig_b, fig_c, fig_d, metrics_ui


# ==============================================================================
# TAB 2 CALLBACKS: CROSS-HEIGHT LABORATORY
# ==============================================================================

@app.callback(
    [
        Output("ch-selected-zero-info", "children"),
        Output("graph-ch-overlay", "figure"),
        Output("graph-ch-deviation", "figure"),
        Output("graph-ch-matrix", "figure"),
        Output("graph-ch-taylor", "figure"),
    ],
    [
        Input("check-ch-blocks", "value"),
        Input("input-ch-zero-idx", "value"),
        Input("slider-ch-umax", "value"),
        Input("radio-cert-mode", "value")
    ]
)
def update_cross_height_lab(selected_blocks, zero_idx_val, u_max_val, cert_mode):
    dps = 40 if cert_mode in ["audit", "certified"] else 25
    u_max = float(u_max_val or 0.5)
    zero_idx = int(zero_idx_val or 0)
    blocks = selected_blocks if selected_blocks is not None else CANONICAL_BLOCK_KEYS


    # 1. Gather zeros for selected blocks
    block_colors = {
        "low_validation": "#00d2ff",
        "medium_research": "#00ff88",
        "high_research": "#ffea00",
        "very_high_sparse": "#ff007f"
    }

    u_grid = np.linspace(-u_max, u_max, 41)

    fig_overlay = go.Figure(layout=DARK_LAYOUT)
    fig_overlay.update_layout(
        title=dict(text=f"Normalized Paths u ↦ P_n(u) in Complex Plane (u ∈ [-{u_max}, {u_max}])", font=dict(size=12)),
        xaxis=dict(title="Re P_n(u)", zeroline=True, dtick=0.2),
        yaxis=dict(title="Im P_n(u)", scaleanchor="x", scaleratio=1.0, constrain="range", zeroline=True, dtick=0.2),
        showlegend=True
    )
    # Unit Tangent Marker at u=0
    fig_overlay.add_trace(go.Scatter(
        x=[0], y=[0], mode="markers", marker=dict(color="#ffffff", size=8, symbol="cross"),
        name="Common Tangent Origin (u=0)"
    ))

    fig_dev = go.Figure(layout=DARK_LAYOUT)
    fig_dev.update_layout(
        title=dict(text=f"Trajectory Deviation |P_n(u) - u| vs u", font=dict(size=12)),
        xaxis=dict(title="u", dtick=0.2),
        yaxis=dict(title="|P_n(u) - u|", dtick=0.1),
        showlegend=True
    )

    selected_zero_labels = []
    selected_ordinates = []
    matrix_labels = []
    block_eval_pts = {}

    for b_key in blocks:
        blk = reference_data.get_zero_block(b_key)
        ords = blk.get("ordinates", [])
        if not ords:
            continue
        g_str = ords[zero_idx % len(ords)]
        selected_ordinates.append((b_key, g_str))
        label = f"{blk.get('name', b_key).split('(')[0].strip()} (γ ≈ {float(g_str):.2f})"
        matrix_labels.append(f"{b_key[:4]}_z{zero_idx}")

        # Precompute zeta'(rho_n) once for this zero
        zp = transcendental.evaluate_zeta_derivative_at_zero(g_str, dps=dps)

        # Evaluate P_n(u) curve
        p_re_list, p_im_list, dev_list = [], [], []
        c_pts = []
        for u_val in u_grid:
            p_res = transcendental.evaluate_derivative_normalized_path(g_str, str(u_val), dps=dps, zeta_prime=zp)
            re_val = float(p_res["P_n_re"])
            im_val = float(p_res["P_n_im"])
            p_re_list.append(re_val)
            p_im_list.append(im_val)
            c_val = complex(re_val, im_val)
            c_pts.append(c_val)
            dev_list.append(abs(c_val - u_val))

        block_eval_pts[b_key] = c_pts
        col = block_colors.get(b_key, "#ffffff")
        fig_overlay.add_trace(go.Scatter(
            x=p_re_list, y=p_im_list, mode="lines",
            line=dict(color=col, width=2.5),
            name=label
        ))
        fig_dev.add_trace(go.Scatter(
            x=u_grid, y=dev_list, mode="lines",
            line=dict(color=col, width=2.5),
            name=label
        ))
        selected_zero_labels.append(f"• {label}: γ = {g_str[:12]}...")

    # Pairwise Distance Matrix Heatmap (using cached point arrays)
    N = len(selected_ordinates)
    dist_matrix = np.zeros((N, N))
    hover_matrix = []

    for i in range(N):
        hover_row = []
        for j in range(N):
            if i == j:
                dist_matrix[i, j] = 0.0
                hover_row.append(f"Same zero: {matrix_labels[i]}")
            else:
                b1 = selected_ordinates[i][0]
                b2 = selected_ordinates[j][0]
                pts1 = block_eval_pts.get(b1, [])
                pts2 = block_eval_pts.get(b2, [])
                if pts1 and pts2:
                    diffs = [abs(p1 - p2) for p1, p2 in zip(pts1, pts2)]
                    l_inf = max(diffs)
                    l_2 = float(np.sqrt(np.mean([d**2 for d in diffs])))

                else:
                    l_inf, l_2 = 0.0, 0.0
                dist_matrix[i, j] = l_inf
                hover_row.append(f"Pair: {matrix_labels[i]} vs {matrix_labels[j]}<br>L_inf: {l_inf:.4f}<br>L_2: {l_2:.4f}")
        hover_matrix.append(hover_row)

    fig_matrix = go.Figure(layout=DARK_LAYOUT)
    fig_matrix.add_trace(go.Heatmap(
        z=dist_matrix,
        x=matrix_labels,
        y=matrix_labels,
        hovertext=hover_matrix,
        hoverinfo="text",
        colorscale="Viridis",
        colorbar=dict(title="L^∞ Dist")
    ))
    fig_matrix.update_layout(
        title=dict(text="Pairwise Discrete Path Distance Matrix (L^∞)", font=dict(size=12)),
        xaxis=dict(title="Target Zero Block"),
        yaxis=dict(title="Source Zero Block")
    )

    # Taylor Shape Plot
    all_sample_zeros = [
        ("Zero #1", 14.134725),
        ("Zero #2", 21.022040),
        ("Zero #5", 37.586178),
        ("Zero #10", 49.773832),
        ("Zero #100", 236.524230),
        ("Zero #1000", 1419.422481),
        ("Zero #10000", 9877.782654)
    ]
    log_gammas = []
    abs_c2_list = []
    abs_c3_list = []
    for name, g in all_sample_zeros:
        t_info = transcendental.extract_taylor_shape_coefficients(str(g), dps=dps)
        log_gammas.append(np.log(g))
        abs_c2_list.append(float(t_info["abs_c2"]))
        abs_c3_list.append(float(t_info["abs_c3"]))

    fig_taylor = go.Figure(layout=DARK_LAYOUT)
    fig_taylor.add_trace(go.Scatter(
        x=log_gammas, y=abs_c2_list, mode="lines+markers",
        line=dict(color="#00d2ff", width=2), marker=dict(size=8),
        name="|c_{2,n}| = |(i·Δ_n·ζ''(ρ_n)) / (2·ζ'(ρ_n))|"
    ))
    fig_taylor.add_trace(go.Scatter(
        x=log_gammas, y=abs_c3_list, mode="lines+markers",
        line=dict(color="#ffea00", width=2), marker=dict(size=8),
        name="|c_{3,n}| = |((i·Δ_n)^2·ζ'''(ρ_n)) / (6·ζ'(ρ_n))|"
    ))

    fig_taylor.update_layout(
        title=dict(text="Taylor Shape Coefficients |c_2|, |c_3| across Spectrum Heights log(γ_n)", font=dict(size=12)),
        xaxis=dict(title="log(γ_n)", dtick=1.0),
        yaxis=dict(title="Normalized Magnitude", dtick=0.2),
        showlegend=True
    )

    info_children = []
    if cert_mode == "certified":
        all_passed = True
        failed_msgs = []
        for b_key, g_str in selected_ordinates:
            blk = reference_data.get_zero_block(b_key)
            ords = blk.get("ordinates", [])
            idx_in_blk = zero_idx % len(ords)
            if b_key == "low_validation":
                global_idx = 1 + idx_in_blk
            elif b_key == "medium_research":
                global_idx = 100 + idx_in_blk
            elif b_key == "high_research":
                global_idx = 1000 + idx_in_blk
            elif b_key == "very_high_sparse":
                global_idx = 10000 + idx_in_blk
            else:
                global_idx = 1 + idx_in_blk

            cert_path = os.path.join(REPO_ROOT, "data", "certificates", "zeros", f"zero_{global_idx:05d}.json")
            if not os.path.exists(cert_path):
                all_passed = False
                failed_msgs.append(f"Zero #{global_idx} certificate missing on disk")
            else:
                try:
                    with open(cert_path, "r", encoding="utf-8") as f:
                        zc = json.load(f)
                    ok, errs = certification.verify_certificate(zc, check_provenance=True)
                    if not ok or zc.get("status") != "simple_zero_certified":
                        all_passed = False
                        failed_msgs.append(f"Zero #{global_idx} verification failed: {'; '.join(errs)}")
                except Exception as e:
                    all_passed = False
                    failed_msgs.append(f"Zero #{global_idx} parse error: {e}")

        if all_passed and selected_ordinates:
            info_children.append(
                dbc.Badge(f"CERTIFIED: All {len(selected_ordinates)} spectrum zeros verified in Arb (FLINT 0.6.0)", color="success", className="d-block p-1 mb-2 font-monospace")
            )
        else:
            err_summary = "; ".join(failed_msgs[:2]) if failed_msgs else "No spectrum zeros selected"
            info_children.append(
                dbc.Badge(f"CERTIFICATION REJECTED: {err_summary}", color="danger", className="d-block p-1 mb-2 font-monospace")
            )

    info_children.extend([
        html.Span(f"Comparing {len(selected_ordinates)} spectrum blocks at zero index {zero_idx}:", className="fw-bold d-block mb-1"),
        html.Div([html.Span(lbl, className="d-block text-light") for lbl in selected_zero_labels])
    ])
    info_text = html.Div(info_children)

    return info_text, fig_overlay, fig_dev, fig_matrix, fig_taylor


# ==============================================================================
# TAB 3 CALLBACKS: BILATERAL WORLDLINE LABORATORY
# ==============================================================================

@app.callback(
    [
        Output("graph-wl-trajectory", "figure"),
        Output("graph-wl-radial", "figure"),
        Output("graph-wl-defect", "figure"),
    ],
    [
        Input("dropdown-wl-zero", "value"),
        Input("input-wl-kmin", "value"),
        Input("input-wl-kmax", "value"),
        Input("check-wl-deltas", "value"),
        Input("radio-cert-mode", "value")
    ]
)
def update_worldline_lab(zero_gamma, k_min_val, k_max_val, selected_deltas, cert_mode):
    dps = 40 if cert_mode in ["audit", "certified"] else 25
    gamma = float(zero_gamma or INITIAL_ZEROS_FLOAT[0])
    k_min = int(k_min_val if k_min_val is not None else -5)
    k_max = int(k_max_val if k_max_val is not None else 5)
    deltas = selected_deltas or [0.0]

    k_range = list(range(k_min, k_max + 1))

    # Map selected zero gamma to exact index
    gamma_to_idx = {
        14.134725: 1,
        21.022040: 2,
        25.010858: 3,
        236.524230: 100,
        1419.422481: 1000,
        9877.782654: 10000
    }
    z_idx = None
    for g_val, idx_val in gamma_to_idx.items():
        if abs(gamma - g_val) < 1e-4:
            z_idx = idx_val
            break

    all_certified = True
    unverified_reasons = []
    src_cert_hash = ""

    if cert_mode == "certified":
        if z_idx is None:
            all_certified = False
            unverified_reasons.append(f"Selected gamma {gamma} is not a canonical certified zero")
        else:
            # Check source zero cert
            src_path = os.path.join(REPO_ROOT, "data", "certificates", "zeros", f"zero_{z_idx:05d}.json")
            if not os.path.exists(src_path):
                all_certified = False
                unverified_reasons.append(f"Source zero #{z_idx} certificate missing")
            else:
                try:
                    with open(src_path, "r", encoding="utf-8") as f:
                        szc = json.load(f)
                    ok, errs = certification.verify_certificate(szc, check_provenance=True)
                    if not ok:
                        all_certified = False
                        unverified_reasons.append(f"Source zero #{z_idx} invalid: {'; '.join(errs[:1])}")
                    else:
                        src_cert_hash = str(szc.get("certificate_hash", ""))
                except Exception as e:
                    all_certified = False
                    unverified_reasons.append(f"Source zero #{z_idx} unreadable: {e}")

            # Check worldline certs for all deltas and grades
            for d in deltas:
                for K in k_range:
                    k_str = f"Kp{K}" if K >= 0 else f"Km{abs(K)}"
                    d_tag = "pos0p00" if abs(d) < 1e-6 else ("pos0p10" if abs(d - 0.10) < 1e-4 else ("neg0p10" if abs(d + 0.10) < 1e-4 else ("pos0p01" if abs(d - 0.01) < 1e-4 else ("neg0p01" if abs(d + 0.01) < 1e-4 else None))))
                    if d_tag is None:
                        all_certified = False
                        unverified_reasons.append(f"Delta {d} has no canonical certificate")
                        continue

                    wl_filename = f"worldline_z{z_idx:05d}_{k_str}_delta_{d_tag}.json"
                    wl_path = os.path.join(REPO_ROOT, "data", "certificates", "worldlines", wl_filename)
                    if not os.path.exists(wl_path):
                        all_certified = False
                        unverified_reasons.append(f"Missing certificate for z={z_idx}, K={K}, delta={d}")
                    else:
                        try:
                            with open(wl_path, "r", encoding="utf-8") as f:
                                wlc = json.load(f)
                            ok, errs = certification.verify_certificate(wlc, check_provenance=True)
                            if not ok:
                                all_certified = False
                                unverified_reasons.append(f"Invalid certificate for z={z_idx}, K={K}, delta={d}: {'; '.join(errs[:1])}")
                        except Exception as e:
                            all_certified = False
                            unverified_reasons.append(f"Unreadable certificate for z={z_idx}, K={K}, delta={d}: {e}")

    hash_display = f" [{src_cert_hash[:12]}...]" if src_cert_hash else ""
    cert_prefix = f"CERTIFIED{hash_display} " if (cert_mode == "certified" and all_certified) else ""
    uncert_notice = f" [UNCERTIFIED: {unverified_reasons[0]}]" if (cert_mode == "certified" and not all_certified and unverified_reasons) else ""


    fig_traj = go.Figure(layout=DARK_LAYOUT)
    fig_traj.update_layout(
        title=dict(text=f"{cert_prefix}Bilateral Worldlines in Complex Plane for γ = {gamma:.4f}{uncert_notice}", font=dict(size=12)),
        xaxis=dict(title="Re(s)", zeroline=True),
        yaxis=dict(title="Im(s)", scaleanchor="x", scaleratio=1.0, constrain="range", zeroline=True),
        showlegend=True
    )

    fig_rad = go.Figure(layout=DARK_LAYOUT)
    fig_rad.update_layout(
        title=dict(text=f"{cert_prefix}Normalized Radial Coordinate K ↦ R_τ(s_ρ(K), K){uncert_notice}", font=dict(size=12)),
        xaxis=dict(title="Bilateral Grade K", dtick=1),
        yaxis=dict(title="R_τ(s, K)", dtick=0.05),
        showlegend=True
    )

    fig_def = go.Figure(layout=DARK_LAYOUT)
    fig_def.update_layout(
        title=dict(text=f"Hyperbolic Defect Scaling: |Re(s) - τ^K / 2| = τ^K |δ|{uncert_notice}", font=dict(size=12)),
        xaxis=dict(title="Bilateral Grade K", dtick=1),
        yaxis=dict(title="Defect |Re(s) - σ_c(K)|", type="log"),
        showlegend=True
    )

    delta_colors = {
        0.0: "#00ff88",
        0.10: "#ffea00",
        -0.10: "#ff007f",
        0.01: "#00d2ff",
        -0.01: "#ff9900"
    }

    for d in deltas:
        re_pts, im_pts, r_tau_pts, defect_pts = [], [], [], []
        col = delta_colors.get(d, "#ffffff")
        is_actual = (d == 0.0)
        label = f"δ = {d:+.2f} ({'Actual Zero Worldline' if is_actual else 'Synthetic Radial Leaf'})"

        for K in k_range:
            g_obj = transcendental.IntegerTauGrade(K=K)
            s_pt = transcendental.zero_worldline_point(complex(0.5, gamma), g_obj, delta=str(d), dps=dps)
            re_pts.append(float(s_pt.real))
            im_pts.append(float(s_pt.imag))

            r_val = float(transcendental.normalized_radial_leaf(s_pt, g_obj, dps=dps))
            r_tau_pts.append(r_val)

            sigma_c = float(transcendental.critical_surface_sigma(g_obj, dps=dps))
            defect_pts.append(max(1e-15, abs(float(s_pt.real) - sigma_c)))

        fig_traj.add_trace(go.Scatter(
            x=re_pts, y=im_pts, mode="lines+markers",
            line=dict(color=col, width=2.5 if is_actual else 1.5, dash="solid" if is_actual else "dot"),
            marker=dict(size=7 if is_actual else 5),
            name=label
        ))

        fig_rad.add_trace(go.Scatter(
            x=k_range, y=r_tau_pts, mode="lines+markers",
            line=dict(color=col, width=2.5 if is_actual else 1.5),
            marker=dict(size=7 if is_actual else 5),
            name=label
        ))

        if not is_actual:
            fig_def.add_trace(go.Scatter(
                x=k_range, y=defect_pts, mode="lines+markers",
                line=dict(color=col, width=2),
                marker=dict(size=6),
                name=label
            ))

    return fig_traj, fig_rad, fig_def



# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    print("Starting Riemann Microscope / Macroscope on http://127.0.0.1:8050 ...")
    app.run(debug=False, host="127.0.0.1", port=8050)
