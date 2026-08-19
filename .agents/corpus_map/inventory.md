# Corpus Inventory and Coverage Record

This document records the inspection and coverage of all Markdown files in the repository root.

## Inspection Date
2026-08-19

## Root Markdown Files Inventory

| Filename | Lines | Bytes | SHA-256 (computed) | Coverage Status | Role in Research Programme |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `README.md` | 155 | 4,158 | `dc1a3fb3b1fa6f8ca735e592f03f7e5306ec4a9e22e92cbb41a0ba61907cb51a` | Complete (100%) | Project overview, scope, authority hierarchy, compute tiers, definition of done |
| `MATH_CONTRACT.md` | 443 | 5,203 | `037b58c7e6c43fa9fe0d3c01c0dc65163152784cfbc97858c2794719e7592cf1` | Complete (100%) | Authoritative implementation-level mathematical contract, exact identities, test vectors A–F |
| `DECISIONS.md` | 108 | 3,632 | `ad8fcb972e2cf6311dd6dc12480e6fe1c633a69b766fa0c4dd9cf477cb54c414` | Complete (100%) | Append-only architectural and mathematical decisions log |
| `DATA_PROVENANCE.md` | 196 | 4,965 | `a8d5e1f0e4ff656aaec48464319522956cf996ce08b8b09339e16ef9a17387cb` | Complete (100%) | Standards for external datasets, baseline zero validation rules, prime generation |
| `RIEMANN_MICROSCOPE_SPEC.md` | 599 | 10,398 | `4b09ec25439c636f2f9bcf0bb539446d61f71dfb1b5e5c7075c3dbb93ef2d34a` | Complete (100%) | Canonical specification for math, UI, panels A–D, Kernel Lab, responsiveness tiers |
| `RIEMANN_MICROSCOPE_CODING_AGENT_PROMPT.md` | 393 | 8,534 | `d55263ca773ebf1e5699478f6c3eb45c2faad2eb6eb2c62c2f30b91d29528e54` | Complete (100%) | Instructions for building the standalone Dash/Python application |

---

## Detailed Section-by-Section Coverage Log

### 1. `README.md`
- **Lines 1–13**: Title, authority hierarchy (`SPEC.md` > `MATH_CONTRACT.md` > `DATA_PROVENANCE.md` > `DECISIONS.md`).
- **Lines 14–32**: Scope (complex trace, sampling path, zero discovery, transformations, prime staircase, zero perturbation, $\tau$-grade amplification $q_\rho^K$).
- **Lines 33–72**: Preferred stack (Python 3.12+, Dash, python-flint/Arb, mpmath, numpy, pytest) and expected repository layout.
- **Lines 73–102**: Installation, run, test commands.
- **Lines 103–128**: Compute tiers: Preview (30–40 digits, 200–500 samples, <200ms) vs Audit (80+ digits, 1000–5000 samples).
- **Lines 129–139**: Baseline startup behavior at $k=0$.
- **Lines 140–155**: Definition of done and anti-proof boundary.

### 2. `MATH_CONTRACT.md`
- **Lines 1–38**: Constants ($\tau=2\pi$), raw coordinate $s=\sigma+it$, centered coordinate $z=s-1/2=\delta+it$, critical line $\Re(s)=1/2$.
- **Lines 39–46**: Camera transform $T_{\mathrm{camera}}(s)=s$.
- **Lines 47–58**: Height microscope $s_K(u)=1/2+\delta+i(t_0+\tau^K u)$.
- **Lines 59–96**: Origin coordinate dilation $s'=\tau^K s$, image critical line $\Re(s')=\tau^K/2$, zero map $\rho'=\tau^K\rho$.
- **Lines 97–124**: Centered coordinate dilation $s'=1/2+\tau^K(s-1/2)$, image critical line $\Re(s')=1/2$, zero map $\rho'=1/2+\tau^K(\rho-1/2)$.
- **Lines 125–150**: Argument transform $f_K(s)=\zeta(\tau^K s)$, zero map $s=\rho/\tau^K$, image line $\Re(s)=1/(2\tau^K)$.
- **Lines 151–200**: Kernel transform $\mathcal{Z}_{A,C,B,D}(s)=e^{-C(Bs+D)}\zeta(A(Bs+D))$, zero map $s_\rho=(\rho/A-D)/B$.
- **Lines 201–222**: Inverse Scale Lock $AB=1 \implies \mathcal{Z}_{A,0,1/A,0}(s)=\zeta(s)$.
- **Lines 223–242**: Centered kernel mode $\mathcal{Z}^{\mathrm{ctr}}_{A,B}(z)=\zeta(1/2+ABz)$.
- **Lines 243–252**: Anisotropic centered deformation $z=\delta+i\gamma \mapsto A_\delta\delta+iA_\gamma\gamma$ (`NON-HOLOMORPHIC DEFORMATION`).
- **Lines 253–308**: Zero character $q_\rho = \tau^{\rho-1/2} = \tau^\delta e^{i\gamma\log\tau}$, $q_\rho^K = \tau^{K\delta}e^{iK\gamma\log\tau}$, $|q_\rho^K|=\tau^{K\delta}$, $\log|q_\rho^K|=K\delta\log\tau$, $\frac{d}{dK}\log|q_\rho^K|=\delta\log\tau$.
- **Lines 309–340**: Converter formulas $J_N(x)$ and $\pi_N(x)$ using Riemann explicit formula and Möbius inversion.
- **Lines 341–432**: Deterministic test vectors A through F.
- **Lines 433–443**: Forbidden shortcuts (no Dirichlet sums in critical strip, no seeding from reference zeros, no conflation of dilations/arguments, no binary float intermediate conversions).

### 3. `DECISIONS.md`
- **Lines 1–30**: Append-only policy, decision template.
- **Lines 31–43**: Decision: Minimal research-instrument architecture (Python-first, Plotly Dash).
- **Lines 44–56**: Decision: Transform classes remain explicit and separate.
- **Lines 57–69**: Decision: Reference zeros are validation-only (discovery-first).
- **Lines 70–84**: Decision: Analytic continuation is authoritative in critical strip (Dirichlet series $\sum n^{-s}$ does not converge).
- **Lines 85–95**: Decision: $\tau=2\pi$ is default scale base, not an assumed zeta symmetry.
- **Lines 96–108**: Decision: Future features require a prior mathematical statement.

### 4. `DATA_PROVENANCE.md`
- **Lines 1–20**: Core rule: Discovery before validation; reference data must never seed the search.
- **Lines 21–34**: Sourcing standards for reference zeta zeros.
- **Lines 35–71**: Vendored zero snapshot requirements ($10^3$ to $10^4$ zeros, `data/provenance.json`).
- **Lines 72–90**: `scripts/fetch_reference_zeros.py` requirements.
- **Lines 91–113**: Zero-validation report metrics and tolerance standards.
- **Lines 114–129**: Prime data generation (deterministic sieve baseline).
- **Lines 130–148**: High-precision constants ($\tau$) and numeric representation (exact decimal strings).
- **Lines 149–166**: Transformed zero validation rules and provenance change logs.
- **Lines 167–196**: Initial provenance JSON schema.

### 5. `RIEMANN_MICROSCOPE_SPEC.md`
- **Lines 1–16**: Purpose (interactive instrument, not proof engine).
- **Lines 17–55**: Coordinates ($s=\sigma+it$, $z=s-1/2=\delta+it$, $\tau=2\pi$).
- **Lines 56–144**: Transformation definitions: Camera, Height, Origin Dilation, Centered Dilation, Argument Transform.
- **Lines 145–221**: Kernel Lab: $(A,B,C,D)$, Inverse Scale Lock ($AB=1$), Centered Kernel, Anisotropic Deformation.
- **Lines 222–324**: Four synchronized panels: Panel A (Domain Plane), Panel B (Complex Zeta Trace), Panel C (Riemann Converter), Panel D (Centrifuge / Radial Character).
- **Lines 325–375**: Zero discovery via Hardy $Z$-function, root refinement, residual verification, reference validation.
- **Lines 376–411**: Zero perturbation ($\delta,\gamma$), radial presets ($0, 10^{-8}, 10^{-6}, 10^{-4}, 10^{-2}$), cached delta update $\Delta C_n(x)$.
- **Lines 412–434**: Responsiveness: Preview tier (30–40 dps, <200ms) vs Audit tier (80+ dps).
- **Lines 435–444**: Numeric input parsing via high-precision decimal strings.
- **Lines 445–493**: Active Mathematics card mandatory specification and example card.
- **Lines 494–532**: Preferred stack and repository structure.
- **Lines 533–562**: 11 mandatory trust tests before UI polish.
- **Lines 563–585**: 14 acceptance criteria for MVP.
- **Lines 586–599**: Protocol for future additions (must start from explicit lemma/proof step).

### 6. `RIEMANN_MICROSCOPE_CODING_AGENT_PROMPT.md`
- **Lines 1–39**: Objective, hard constraints (KISS, Dash, no Next.js, no proof DAG/verdict badges, no conflation of transformations).
- **Lines 40–90**: Canonical coordinates and transformation objects.
- **Lines 91–131**: Kernel Lab equations and labels.
- **Lines 132–202**: Panels A–D details.
- **Lines 203–248**: Zero discovery workflow and reference data provenance.
- **Lines 249–267**: Single-zero perturbation caching.
- **Lines 268–284**: Responsiveness tiers.
- **Lines 285–329**: Active Mathematics card specification.
- **Lines 330–360**: 11 trust tests and suggested repository files.
- **Lines 361–393**: Implementation order (14 steps) and definition of done.
