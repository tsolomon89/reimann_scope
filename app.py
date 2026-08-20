"""
app.py — Riemann Microscope / Macroscope Interactive Application

Minimal, high-performance, Desmos-like Plotly Dash dashboard conforming to:
- RIEMANN_MICROSCOPE_SPEC.md
- MATH_CONTRACT.md
- DATA_PROVENANCE.md
- DECISIONS.md

All 4 panels feature equal Cartesian scaling and identical metric step sizes (dtick) on both axes:
- 1 mathematical unit in X == 1 mathematical unit in Y (scaleanchor="x", scaleratio=1.0, constrain="range")
- Ticks and grid lines on both X and Y increment by the exact same metric step (xaxis.dtick == yaxis.dtick, tick0=0)
- Every single grid cell rendered is a geometrically perfect square with equal metric scales on X and Y.
"""

from __future__ import annotations
import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc

import transforms
import reference_data
import converter
import cache

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
# UI LAYOUT COMPONENTS
# ==============================================================================

def create_header():
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H4([
                        html.I(className="bi bi-compass me-2 text-info"),
                        "Riemann Microscope / Macroscope"
                    ], className="mb-0 text-light fw-bold"),
                    html.Small("Interactive Geometric & Arithmetic Zeta Instrument", className="text-secondary")
                ], width="auto"),
            ], align="center", className="g-0"),
            dbc.Nav([
                dbc.NavItem(
                    html.Div([
                        dbc.Badge(
                            "Preview Tier: 35 dps (Sub-200ms)",
                            id="tier-badge",
                            color="info",
                            className="p-2 me-2 font-monospace fs-7"
                        )
                    ])
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
                        [html.I(className="bi bi-shield-check me-1"), "Audit Mode (80+ dps)"],
                        id="btn-audit",
                        color="outline-success",
                        size="sm",
                        className="me-2"
                    )
                ),
                dbc.NavItem(
                    dbc.Button(
                        [html.I(className="bi bi-table me-1"), "Zero Validation Report"],
                        id="btn-val-report",
                        color="outline-info",
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
            ], className="ms-auto", navbar=True)
        ], fluid=True),
        color="#0d1117",
        dark=True,
        className="border-bottom border-secondary shadow-sm mb-3 py-2"
    )



def create_active_card_panel():
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="bi bi-card-checklist me-2 text-warning"),
            html.Span("Active Mathematics Card", className="fw-bold")
        ], className="py-2 bg-dark border-secondary"),
        dbc.CardBody([
            dcc.Markdown(id="active-math-card", className="small font-monospace mb-0 text-light")
        ], className="p-3 bg-opacity-10 bg-black")
    ], className="border-secondary shadow-sm mb-3")


def create_controls_panel():
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="bi bi-sliders me-2 text-primary"),
            html.Span("Transformation & Kernel Lab Controls", className="fw-bold")
        ], className="py-2 bg-dark border-secondary"),
        dbc.CardBody([
            dbc.Tabs([
                dbc.Tab(label="Transform Mode", tab_id="tab-mode", children=[
                    html.Div([
                        html.Label("Active Transformation:", className="fw-bold small text-light mt-2"),
                        dcc.Dropdown(
                            id="transform-mode-select",
                            options=[
                                {"label": "1. Camera Only (Rendering)", "value": "camera"},
                                {"label": "2. Height Microscope / Macroscope", "value": "height"},
                                {"label": "3. Origin Coordinate Dilation (s' = τ^k s)", "value": "origin_dilation"},
                                {"label": "4. Centered Coordinate Dilation (s' = 1/2 + τ^k z)", "value": "centered_dilation"},
                                {"label": "5. Argument Transform (f(s) = ζ(τ^k s))", "value": "argument"},
                                {"label": "6. Kernel Lab (Dirichlet Scaling)", "value": "kernel_lab"},
                                {"label": "7. Centered Kernel Mode", "value": "centered_kernel"},
                                {"label": "8. Anisotropic Deformation", "value": "anisotropic"}
                            ],
                            value="height",
                            clearable=False,
                            className="text-dark small mb-3"
                        ),
                        # Container 1: Grade k slider for height, origin, centered, argument
                        html.Div(id="container-mode-scale", children=[
                            html.Label("Scale Grade k (Scale = τ^k):", className="fw-bold small text-light mt-1"),
                            dcc.Slider(
                                id="slider-k", min=-2.0, max=2.0, step=0.05, value=0.0,
                                marks={-2: "-2", -1: "-1", 0: "0", 1: "1", 2: "2"},
                                tooltip={"placement": "bottom", "always_visible": False}
                            )
                        ], style={"display": "block"}),

                        # Container 2: Kernel Lab controls
                        html.Div(id="container-mode-kernel", children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Label("A (log n scale):", className="small text-light"),
                                    dcc.Slider(id="slider-kernel-A", min=0.2, max=3.0, step=0.1, value=1.0,
                                               tooltip={"placement": "bottom", "always_visible": False})
                                ], width=6),
                                dbc.Col([
                                    html.Label("B (s scale):", className="small text-light"),
                                    dcc.Slider(id="slider-kernel-B", min=0.2, max=3.0, step=0.1, value=1.0,
                                               tooltip={"placement": "bottom", "always_visible": False})
                                ], width=6),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("C (log n shift):", className="small text-light"),
                                    dbc.Input(id="input-kernel-C", type="number", value=0.0, step=0.1, size="sm")
                                ], width=6),
                                dbc.Col([
                                    html.Label("D (s shift):", className="small text-light"),
                                    dbc.Input(id="input-kernel-D", type="number", value=0.0, step=0.1, size="sm")
                                ], width=6),
                            ], className="mb-2"),
                            dbc.Checklist(
                                options=[{"label": " Inverse Scale Lock (AB = 1)", "value": "lock"}],
                                value=["lock"],
                                id="check-kernel-lock",
                                switch=True,
                                className="small text-warning"
                            )
                        ], style={"display": "none"}),

                        # Container 3: Centered Kernel controls
                        html.Div(id="container-mode-centered-kernel", children=[
                            html.Label("Kernel Parameter A (with B = 1/A):", className="fw-bold small text-light mt-1"),
                            dcc.Slider(id="slider-centered-kernel-A", min=0.2, max=3.0, step=0.1, value=1.0,
                                       tooltip={"placement": "bottom", "always_visible": False}),
                            dbc.Checklist(
                                options=[{"label": " Inverse Scale Lock (AB = 1)", "value": "lock"}],
                                value=["lock"],
                                id="check-centered-kernel-lock",
                                switch=True,
                                className="small text-warning"
                            )
                        ], style={"display": "none"}),

                        # Container 4: Anisotropic deformation controls
                        html.Div(id="container-mode-aniso", children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Label("A_δ (Real / δ scaling):", className="small text-light"),
                                    dcc.Slider(id="slider-aniso-delta", min=0.2, max=3.0, step=0.1, value=1.0,
                                               tooltip={"placement": "bottom", "always_visible": False})
                                ], width=6),
                                dbc.Col([
                                    html.Label("A_γ (Imag / γ scaling):", className="small text-light"),
                                    dcc.Slider(id="slider-aniso-gamma", min=0.2, max=3.0, step=0.1, value=1.0,
                                               tooltip={"placement": "bottom", "always_visible": False})
                                ], width=6),
                            ])
                        ], style={"display": "none"}),
                    ])
                ]),
                dbc.Tab(label="Sampling Range", tab_id="tab-sampling", children=[
                    html.Div([
                        html.Label("Base Height t₀:", className="fw-bold small text-light mt-2"),
                        dcc.Slider(id="slider-t0", min=10.0, max=100.0, step=0.5, value=14.0,
                                   marks={10: "10", 25: "25", 50: "50", 75: "75", 100: "100"},
                                   tooltip={"placement": "bottom", "always_visible": False}),
                        html.Label("Height Span Δt:", className="fw-bold small text-light mt-2"),
                        dcc.Slider(id="slider-dt", min=5.0, max=50.0, step=1.0, value=20.0,
                                   marks={5: "5", 15: "15", 30: "30", 50: "50"},
                                   tooltip={"placement": "bottom", "always_visible": False}),
                        html.Label("Critical Line Offset δ (Re(s) = 1/2 + δ):", className="fw-bold small text-light mt-2"),
                        dcc.Slider(id="slider-delta-offset", min=-0.5, max=0.5, step=0.01, value=0.0,
                                   marks={-0.5: "-0.5", 0: "0.0", 0.5: "0.5"},
                                   tooltip={"placement": "bottom", "always_visible": False}),
                    ])
                ]),
                dbc.Tab(label="Perturbation & Primes", tab_id="tab-perturb", children=[
                    html.Div([
                        html.Label("Perturbation Semantics:", className="fw-bold small text-light mt-2"),
                        dbc.RadioItems(
                            id="radio-perturb-mode",
                            options=[
                                {"label": " SINGLE-PAIR DIAGNOSTIC (ρ = 1/2+δ+iγ)", "value": "single_pair_diagnostic"},
                                {"label": " SYMMETRY-COMPLETE QUARTET (1/2±δ±iγ)", "value": "symmetry_complete_quartet"},
                            ],
                            value="single_pair_diagnostic",
                            className="small text-warning mb-2"
                        ),
                        html.Label("Select Zero to Perturb:", className="fw-bold small text-light mt-2"),
                        dcc.Dropdown(

                            id="dropdown-selected-zero",
                            options=[
                                {"label": f"Zero #{i+1} (γ ≈ {INITIAL_ZEROS_FLOAT[i]:.4f})", "value": i}
                                for i in range(min(15, len(INITIAL_ZEROS_FLOAT)))
                            ],
                            value=0,
                            clearable=False,
                            className="text-dark small mb-2"
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

        # Row 1: 4 Synchronized Panels (2x2 Full Responsive Grid with 1x1 Square Coordinate System)
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

    ], fluid=True)
], style={"backgroundColor": "#090c10", "minHeight": "100vh", "color": "#e2e8f0"})


# ==============================================================================
# CALLBACKS & INTERACTIVE LOGIC
# ==============================================================================

@app.callback(
    [
        Output("container-mode-scale", "style"),
        Output("container-mode-kernel", "style"),
        Output("container-mode-centered-kernel", "style"),
        Output("container-mode-aniso", "style"),
    ],
    Input("transform-mode-select", "value")
)
def toggle_mode_control_visibility(mode: str):
    """Toggle visibility of specific control sections based on active mode."""
    show = {"display": "block"}
    hide = {"display": "none"}
    
    scale_style = show if mode in ["height", "origin_dilation", "centered_dilation", "argument"] else hide
    kernel_style = show if mode == "kernel_lab" else hide
    ctr_kernel_style = show if mode == "centered_kernel" else hide
    aniso_style = show if mode == "anisotropic" else hide
    
    return scale_style, kernel_style, ctr_kernel_style, aniso_style


@app.callback(
    Output("slider-kernel-B", "value"),
    [Input("slider-kernel-A", "value"), Input("check-kernel-lock", "value")],
    State("slider-kernel-B", "value")
)
def sync_kernel_lock(a_val, lock_vals, current_b):
    """Sync B = 1/A when Inverse Scale Lock is ON."""
    if lock_vals and "lock" in lock_vals and a_val and a_val > 0:
        return round(1.0 / float(a_val), 3)
    return current_b


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
def set_radial_preset(c0, c8, c6, c4, c2):
    """Handle preset radial perturbation buttons."""
    triggered_id = ctx.triggered_id
    if triggered_id == "preset-0":
        return 0.0
    elif triggered_id == "preset-1e8":
        return 1e-8
    elif triggered_id == "preset-1e6":
        return 1e-6
    elif triggered_id == "preset-1e4":
        return 1e-4
    elif triggered_id == "preset-1e2":
        return 1e-2
    return 0.0


@app.callback(
    Output("input-gamma-pert", "value"),
    Input("dropdown-selected-zero", "value"),
    State("store-discovered-zeros", "data")
)
def update_selected_zero_gamma(zero_idx: int, zeros_list: list):
    """Update selected zero ordinate input when dropdown changes."""
    if zeros_list and 0 <= zero_idx < len(zeros_list):
        return float(zeros_list[zero_idx])
    return 14.134725


@app.callback(
    [
        Output("store-audit-mode", "data"),
        Output("tier-badge", "children"),
        Output("tier-badge", "color")
    ],
    [
        Input("btn-audit", "n_clicks"),
        Input("btn-reset", "n_clicks")
    ],
    State("store-audit-mode", "data"),
    prevent_initial_call=True
)
def toggle_audit_mode(n_audit, n_reset, current_state):
    """Toggle between Preview Tier (35 dps) and Certified Audit Tier (80+ dps)."""
    triggered_id = ctx.triggered_id
    if triggered_id == "btn-reset":
        return False, "Preview Tier: 35 dps (Sub-200ms)", "info"
    new_state = not current_state
    if new_state:
        return True, "Audit Tier: 80+ dps (Certified)", "success"
    else:
        return False, "Preview Tier: 35 dps (Sub-200ms)", "info"


@app.callback(
    [Output("modal-val-report", "is_open"), Output("val-report-content", "children")],
    [Input("btn-val-report", "n_clicks"), Input("btn-close-modal", "n_clicks")],
    [State("modal-val-report", "is_open"), State("store-discovered-zeros", "data")],
    prevent_initial_call=True
)
def toggle_val_report(n_open, n_close, is_open, disc_zeros):
    """Populate and toggle the zero validation report modal."""
    if not is_open:
        report = reference_data.validate_zero_discovery(disc_zeros or INITIAL_ZEROS_FLOAT, 10.0, 60.0, tolerance=1e-5)
        prov = reference_data.load_provenance()
        
        status_badge = dbc.Badge("VERIFIED PASS", color="success", className="fs-6 p-2 mb-3") if report["passed"] else dbc.Badge("DISCOVERY MISMATCH", color="danger", className="fs-6 p-2 mb-3")
        
        content = html.Div([
            status_badge,
            html.Table([
                html.Tr([html.Th("Searched Ordinate Interval:"), html.Td(f"[{report['t_min']:.1f}, {report['t_max']:.1f}]")]),
                html.Tr([html.Th("Independently Discovered Roots:"), html.Td(f"{report['discovered_count']}")]),
                html.Tr([html.Th("Reference Table Roots in Range:"), html.Td(f"{report['reference_count']}")]),
                html.Tr([html.Th("Matched Zero Count:"), html.Td(f"{report['matched_count']}")]),
                html.Tr([html.Th("Max |γ_found - γ_ref|:"), html.Td(f"{report['max_difference']:.2e}")]),
                html.Tr([html.Th("RMS Ordinate Difference:"), html.Td(f"{report['rms_difference']:.2e}")]),
                html.Tr([html.Th("Max Residual |ζ(1/2+iγ)|:"), html.Td(f"{report['max_residual']:.2e}")]),
                html.Tr([html.Th("Reference Source:"), html.Td(prov.get("zeta_zeros", {}).get("source_name", "Vendored Tables"))]),
                html.Tr([html.Th("Provenance SHA-256:"), html.Td(prov.get("zeta_zeros", {}).get("sha256", "N/A")[:16] + "...")])
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
        State("store-audit-mode", "data"),
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
    mode, t0, dt, delta_offset, selected_zero_idx, delta_pert, gamma_pert, num_zeros, audit_mode,
    k_val, kA, kB, kC, kD, k_lock, cA, aniso_d, aniso_g
):
    """Generate and display the declarative YAML sweep draft based on current UI state."""
    if not is_open:
        # Determine engine operation
        if mode == "height":
            op = "zeta_trace_compare"
        elif mode in ["origin_dilation", "centered_dilation", "argument"]:
            op = "transform_zero_map"
        elif mode in ["kernel_lab", "centered_kernel"]:
            op = "kernel_identity"
        else:
            op = "centrifuge"

        dps = 80 if audit_mode else 35
        k_str = f"{k_val:.4g}" if k_val is not None else "0.0"
        d_str = f"{delta_pert:.6g}" if delta_pert is not None else "0.0"
        g_str = f"{gamma_pert:.6g}" if gamma_pert is not None else "14.134725"

        yaml_text = f"""schema_version: "1"
id: sweep-draft-{mode.replace('_', '-')}-001
title: "Interactive Sweep Draft — {mode.replace('_', ' ').title()}"

hypothesis:
  statement: "TODO: State the exact mathematical hypothesis to test over this finite parameter space."

criterion:
  metric: max_residual
  operator: "<="
  threshold: "1e-20"

engine:
  operation: {op}

parameters:
  mode:
    kind: explicit
    values: ["{mode}"]
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
    """Trigger client-side file download of the generated sweep YAML."""
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
        Input("store-audit-mode", "data"),
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
    ],
    State("store-discovered-zeros", "data")
)
def update_all_panels(
    mode: str,
    t0: float,
    dt: float,
    delta_offset: float,
    selected_zero_idx: int,
    delta_pert: float,
    gamma_pert: float,
    num_zeros: int,
    audit_mode: bool,
    k_val: float,
    kA: float,
    kB: float,
    kC: float,
    kD: float,
    k_lock: list,
    cA: float,
    c_lock: list,
    aniso_d: float,
    aniso_g: float,
    perturb_mode_val: str,
    disc_zeros: list
):

    """
    Unified callback to update the Active Mathematics Card and all 4 panels
    with 1x1 isotropic square Cartesian grids, matching metric scale steps (dtick),
    and sub-100ms preview latency.
    """
    dps = 80 if audit_mode else 35
    n_samples = 500 if audit_mode else 250
    
    t0 = float(t0 if t0 is not None else 14.0)
    dt = float(dt if dt is not None else 20.0)
    delta_offset = float(delta_offset if delta_offset is not None else 0.0)
    delta_pert = float(delta_pert if delta_pert is not None else 0.0)
    gamma_pert = float(gamma_pert if gamma_pert is not None else INITIAL_ZEROS_FLOAT[0])
    num_zeros = int(num_zeros if num_zeros is not None else 15)

    # 1. Instantiate active Transform Object
    transform_obj: transforms.BaseTransform
    if mode == "camera":
        transform_obj = transforms.CameraTransform()

    elif mode == "height":
        k = float(k_val if k_val is not None else 0.0)
        transform_obj = transforms.HeightMicroscopeTransform(k=k, t0=t0, delta=delta_offset)
    elif mode == "origin_dilation":
        k = float(k_val if k_val is not None else 0.0)
        transform_obj = transforms.OriginCoordinateDilation(k=k)
    elif mode == "centered_dilation":
        k = float(k_val if k_val is not None else 0.0)
        transform_obj = transforms.CenteredCoordinateDilation(k=k)
    elif mode == "argument":
        k = float(k_val if k_val is not None else 0.0)
        transform_obj = transforms.ArgumentTransform(k=k)
    elif mode == "kernel_lab":
        A = float(kA if kA is not None else 1.0)
        is_locked = bool(k_lock and "lock" in k_lock)
        B = (1.0 / A) if is_locked else float(kB if kB is not None else 1.0)
        C = float(kC if kC is not None else 0.0)
        D = float(kD if kD is not None else 0.0)
        transform_obj = transforms.KernelTransform(A=A, B=B, C=C, D=D, inverse_scale_lock=is_locked)
    elif mode == "centered_kernel":
        A = float(cA if cA is not None else 1.0)
        is_locked = bool(c_lock and "lock" in c_lock)
        transform_obj = transforms.CenteredKernelTransform(A=A, inverse_scale_lock=is_locked)
    elif mode == "anisotropic":
        A_del = float(aniso_d if aniso_d is not None else 1.0)
        A_gam = float(aniso_g if aniso_g is not None else 1.0)
        transform_obj = transforms.AnisotropicDeformation(A_delta=A_del, A_gamma=A_gam)
    else:
        transform_obj = transforms.CameraTransform()

    # Active Card Text
    card_md = transform_obj.get_card_markdown()

    # Compute Complex Trace via Cache
    u_vals, s_coords, re_w, im_w = cache.get_cached_trace(
        transform_obj, t0, dt, delta_offset, n_samples=n_samples, dps=dps
    )

    # --------------------------------------------------------------------------
    # Panel A: Domain Plane (Matching dtick on X and Y)
    # --------------------------------------------------------------------------
    fig_a = go.Figure(layout=DARK_LAYOUT)
    x_min_a, x_max_a = -1.0, 4.0
    y_min_a, y_max_a = t0 - 2.0, t0 + dt + 2.0
    dtick_a = 5.0
    
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

    # Transformed Image Critical Line
    img_re = None
    if isinstance(transform_obj, transforms.OriginCoordinateDilation):
        img_re = transform_obj.scale / 2.0
    elif isinstance(transform_obj, transforms.ArgumentTransform):
        img_re = 1.0 / (2.0 * transform_obj.scale)
    elif isinstance(transform_obj, transforms.KernelTransform):
        if abs(transform_obj.A * transform_obj.B) > 1e-12:
            img_re = (0.5 / transform_obj.A - transform_obj.D) / transform_obj.B

    if img_re is not None and abs(img_re - 0.5) > 1e-4:
        fig_a.add_trace(go.Scatter(
            x=[img_re, img_re], y=[y_min_a - 10.0, y_max_a + 10.0],
            mode="lines", line=dict(color="#00d2ff", dash="dot", width=1.5),
            name="Image Critical Line"
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
    selected_rho = complex(0.5 + delta_pert, gamma_pert)
    mapped_selected = transform_obj.map_zero(selected_rho)
    fig_a.add_trace(go.Scatter(
        x=[mapped_selected.real], y=[mapped_selected.imag],
        mode="markers", marker=dict(color="#ffea00", size=11, symbol="star"),
        name="Selected Zero"
    ))

    # --------------------------------------------------------------------------
    # Panel B: Complex Zeta Trace (Matching dtick on X and Y)
    # --------------------------------------------------------------------------
    fig_b = go.Figure(layout=DARK_LAYOUT)
    max_trace_val = max(float(np.max(np.abs(re_w))), float(np.max(np.abs(im_w))), 1.5)
    r_limit = max_trace_val * 1.15
    dtick_b = 1.0

    fig_b.update_layout(
        title=dict(text="Panel B: Complex Zeta Trace (Re ζ, Im ζ)", font=dict(size=12)),
        xaxis=dict(range=[-r_limit, r_limit], title="Re ζ(s(u))", dtick=dtick_b, tick0=0),
        yaxis=dict(range=[-r_limit, r_limit], title="Im ζ(s(u))", scaleanchor="x", scaleratio=1.0, constrain="range", dtick=dtick_b, tick0=0)
    )

    # Origin Marker (0,0)
    fig_b.add_trace(go.Scatter(
        x=[0], y=[0],
        mode="markers", marker=dict(color="#ff007f", size=8, symbol="cross"),
        name="Origin (0,0)"
    ))

    # Complex Path
    fig_b.add_trace(go.Scatter(
        x=re_w, y=im_w,
        mode="lines",
        line=dict(color="#00d2ff", width=2.5),
        name="Zeta Trace"
    ))

    # --------------------------------------------------------------------------
    # Panel C: Riemann Converter (Matching dtick on X and Y)
    # --------------------------------------------------------------------------
    fig_c = go.Figure(layout=DARK_LAYOUT)
    x_min_c, x_max_c = 0.0, 50.0
    y_min_c, y_max_c = 0.0, 16.0
    dtick_c = 5.0

    fig_c.update_layout(
        title=dict(text=f"Panel C: Prime Reconstruction π_N(x) (N={num_zeros})", font=dict(size=12)),
        xaxis=dict(range=[x_min_c, x_max_c], title="x", dtick=dtick_c, tick0=0),
        yaxis=dict(range=[y_min_c, y_max_c], title="Count π(x)", scaleanchor="x", scaleratio=1.0, constrain="range", dtick=dtick_c, tick0=0)
    )

    rec_cache = cache.get_converter_cache(max_x=50.0, n_points=300)
    x_pts = rec_cache.x_grid
    
    # Ground Truth Prime Staircase
    true_pi = reference_data.prime_pi_array(x_pts)
    fig_c.add_trace(go.Scatter(
        x=x_pts, y=true_pi,
        mode="lines", line=dict(color="#a0aec0", width=1.5, shape="hv"),
        name="True Prime Count π(x)"
    ))

    perturb_mode = perturb_mode_val if perturb_mode_val is not None else "single_pair_diagnostic"
    clean_gamma = INITIAL_ZEROS_FLOAT[selected_zero_idx] if selected_zero_idx < len(INITIAL_ZEROS_FLOAT) else 14.134725
    clean_rho_val = complex(0.5, clean_gamma)
    
    # Clean & Perturbed Reconstruction
    clean_pi, pert_pi = rec_cache.reconstruct_pi_perturbed(
        num_zeros=num_zeros,
        perturbed_zero_idx=selected_zero_idx,
        delta=delta_pert,
        gamma=gamma_pert,
        mode=perturb_mode
    )

    fig_c.add_trace(go.Scatter(
        x=x_pts, y=clean_pi,
        mode="lines", line=dict(color="#00ff88", width=2),
        name="Clean π_N(x)"
    ))

    if abs(delta_pert) > 1e-10 or abs(gamma_pert - clean_gamma) > 1e-4:
        fig_c.add_trace(go.Scatter(
            x=x_pts, y=pert_pi,
            mode="lines", line=dict(color="#ff007f", dash="dot", width=2),
            name="Perturbed π_N(x)"
        ))

    # Single-Zero Isolated Contribution Metrics at x=20.0
    eval_x = 20.0
    if audit_mode:
        contrib_info = converter.compute_perturbed_contributions_audit(
            str(eval_x), clean_rho_val, str(delta_pert), mode=perturb_mode, dps=80
        )
        cj_clean_str = f"{float(contrib_info['cj_clean']):.6f}"
        cj_pert_str = f"{float(contrib_info['cj_perturbed']):.6f}"
        cj_diff_str = f"{float(contrib_info['delta_cj']):.6f}"
        cpi_clean_str = f"{float(contrib_info['cpi_clean']):.6f}"
        cpi_pert_str = f"{float(contrib_info['cpi_perturbed']):.6f}"
        cpi_diff_str = f"{float(contrib_info['delta_cpi']):.6f}"
    else:
        cj_c = converter.zero_j_contribution_preview(eval_x, clean_rho_val)
        cpi_c = converter.zero_pi_contribution_preview(eval_x, clean_rho_val)
        if perturb_mode == "symmetry_complete_quartet":
            if abs(delta_pert) < 1e-12:
                cj_p = cj_c
                cpi_p = cpi_c
            else:
                rp = complex(0.5 + delta_pert, gamma_pert)
                rm = complex(0.5 - delta_pert, gamma_pert)
                cj_p = converter.zero_j_contribution_preview(eval_x, rp) + converter.zero_j_contribution_preview(eval_x, rm)
                cpi_p = converter.zero_pi_contribution_preview(eval_x, rp) + converter.zero_pi_contribution_preview(eval_x, rm)
        else:
            r_pert = complex(0.5 + delta_pert, gamma_pert)
            cj_p = converter.zero_j_contribution_preview(eval_x, r_pert)
            cpi_p = converter.zero_pi_contribution_preview(eval_x, r_pert)
        cj_clean_str = f"{cj_c:.6f}"
        cj_pert_str = f"{cj_p:.6f}"
        cj_diff_str = f"{cj_p - cj_c:+.6f}"
        cpi_clean_str = f"{cpi_c:.6f}"
        cpi_pert_str = f"{cpi_p:.6f}"
        cpi_diff_str = f"{cpi_p - cpi_c:+.6f}"

    idx_20 = int(np.argmin(np.abs(x_pts - 20.0)))
    pi_clean_20 = clean_pi[idx_20]
    pi_pert_20 = pert_pi[idx_20]
    pi_diff_20 = pi_pert_20 - pi_clean_20
    
    mode_label = "SINGLE-PAIR DIAGNOSTIC" if perturb_mode == "single_pair_diagnostic" else "SYMMETRY-COMPLETE QUARTET"
    
    metrics_ui = html.Div([
        html.Div([
            dbc.Badge(f"MODE: {mode_label}", color="warning" if perturb_mode == "single_pair_diagnostic" else "info", className="me-2 p-1"),
            html.Span(f"Selected ρ: 0.5000 + {delta_pert:+.4f} + {gamma_pert:.4f}i", className="text-warning fw-bold small")
        ], className="mb-1"),
        html.Div([
            html.Span(f"C_J(x=20): clean={cj_clean_str} | pert={cj_pert_str} | Δ={cj_diff_str}", className="d-block text-secondary small"),
            html.Span(f"C_π(x=20): clean={cpi_clean_str} | pert={cpi_pert_str} | Δ={cpi_diff_str}", className="d-block text-secondary small"),
            html.Span(f"π_N(x=20): clean={pi_clean_20:.4f} | pert={pi_pert_20:.4f} | Δ={pi_diff_20:+.4f}", className="d-block text-info small fw-bold")
        ])
    ])

    # --------------------------------------------------------------------------
    # Panel D: Radial Centrifuge (Matching dtick on X and Y)
    # --------------------------------------------------------------------------
    fig_d = go.Figure(layout=DARK_LAYOUT)
    x_min_d, x_max_d = -20.0, 20.0
    tau_approx = 2.0 * np.pi
    y_limit_d = max(1.0, 20.0 * abs(delta_pert) * np.log(tau_approx) * 1.25)
    dtick_d = 5.0

    fig_d.update_layout(
        title=dict(text=f"Panel D: Centrifuge log |q_ρ^K| = K·δ·ln(τ) (δ={delta_pert:.4g})", font=dict(size=12)),
        xaxis=dict(range=[x_min_d, x_max_d], title="Grade K", dtick=dtick_d, tick0=0),
        yaxis=dict(range=[-y_limit_d, y_limit_d], title="log |q_ρ^K|", scaleanchor="x", scaleratio=1.0, constrain="range", dtick=dtick_d, tick0=0)
    )

    k_grid = np.linspace(-20.0, 20.0, 100)
    log_mod_vals = k_grid * delta_pert * np.log(tau_approx)

    fig_d.add_trace(go.Scatter(
        x=k_grid, y=log_mod_vals,
        mode="lines", line=dict(color="#ffea00", width=2.5),
        name="Amplification Line"
    ))

    # Reference zero line (delta = 0)
    fig_d.add_trace(go.Scatter(
        x=[-20, 20], y=[0, 0],
        mode="lines", line=dict(color="#4a5568", dash="dash", width=1),
        name="On-Line Invariant (δ=0)"
    ))

    return card_md, fig_a, fig_b, fig_c, fig_d, metrics_ui



# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    print("Starting Riemann Microscope / Macroscope on http://127.0.0.1:8050 ...")
    app.run(debug=False, host="127.0.0.1", port=8050)
