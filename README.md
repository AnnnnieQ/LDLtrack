# LDLtrack

> **A Bayesian decision-support tool for personalized LDL-C management** — synthesizing evidence from randomized controlled trials into individualized predictions with explicit uncertainty quantification.

**Status**: Phase 3 core complete — deployed demo with 8 intervention options; schema v2 deferred to backlog

**Live Demo**: [ldltrack.streamlit.app](https://ldltrack.streamlit.app/)  
**Methodology**: [data/README.md](data/README.md)  
**Data Sources**: [SOURCES.md](SOURCES.md)

---

## Why This Project?

Existing LDL-C calculators (e.g., [lipidtools.com](https://lipidtools.com/calculator-pages/ldlc/), ACC's [LDL-C Lowering Therapy tool](https://tools.acc.org/LDL/ldlc_lowering_therapy/)) suffer from three key limitations:

1. **Pharmacology only** — Lifestyle interventions (diet, exercise, weight loss) are not modeled, despite strong evidence for their LDL-lowering effects.
2. **Single-point estimates** — No uncertainty quantification, despite substantial heterogeneity in individual response.
3. **Limited personalization** — Most tools provide fixed population-average effects.

LDLtrack addresses these gaps by:

- ✅ Integrating pharmacological + dietary + lifestyle interventions
- ✅ Using Bayesian models with per-sample uncertainty propagation
- ✅ Producing posterior predictive distributions rather than single numbers

## Evidence Base

39 effect sizes curated from 8 landmark RCTs and meta-analyses across 8 intervention categories:

| Category | Source | Rows |
|---|---|---|
| Statin (2 agents × 2 doses × 5 populations) | VOYAGER (Karlson 2015) | 20 |
| Weight loss (3 mechanisms) | Hasan 2020 | 3 |
| Portfolio diet (efficacy + effectiveness) | Chiavaroli 2018 | 2 |
| Soluble fiber (pooled + by type) | Brown 1999 | 4 |
| Plant sterols (dose-response, 6 bins) | Ras 2014 | 6 |
| Exercise (aerobic/combined vs resistance) | Smart 2024 | 2 |
| Ezetimibe added to statin | Cannon 2015 (IMPROVE-IT) | 1 |
| PCSK9 inhibitor added to statin | Sabatine 2017 (FOURIER) | 1 |

See [data/README.md](data/README.md) for per-paper extraction methodology.

## Current Demo

The deployed app currently supports 8 intervention options:

| Intervention | App behavior |
|---|---|
| Statin | User selects atorvastatin 40/80 mg or rosuvastatin 20/40 mg |
| Ezetimibe | Enabled only after a statin is selected |
| PCSK9 inhibitor | Enabled only after a statin is selected |
| Portfolio diet | User selects real-world adherence or strict efficacy-trial setting |
| Plant sterols | Dose-response prediction from 0.6-3.3 g/day |
| Soluble fiber | Per-g dose input up to 8 g/day |
| Lifestyle weight loss | Per-kg effect with lb input in the app |
| Aerobic/combined exercise | Single pooled aerobic/combined exercise estimate |

Outputs include multiplicative combination of selected interventions,
posterior uncertainty via pre-sampled NetCDF artifacts, and relative and
absolute cardiovascular risk reduction estimates.

## Tech Stack

PyMC · ArviZ · NumPy · Pandas · Streamlit

## Roadmap

- [x] **Phase 1** — Evidence extraction from RCTs and meta-analyses (8 papers, 39 rows)
- [x] **Phase 2** — Bayesian model in PyMC + toy Streamlit demo
    - [x] Milestone 2.1: PyMC + Bayesian basics
    - [x] Milestone 2.2: Single-intervention LDLtrack model
    - [x] Milestone 2.3: Multi-intervention combination + Streamlit demo
- [ ] **Phase 3** — CVD risk conversion, intervention expansion, UI polish, deployment, schema v2 backlog
    - [x] Milestone 3.1: Cardiovascular risk conversion
    - [x] Milestone 3.2: Schema v2 skipped by decision; deferred to backlog
    - [x] Milestone 3.3: Additional intervention support
    - [x] Milestone 3.4: UI polish + public Streamlit deployment
    - [ ] Schema v2 refactor and deeper validation case studies

Current project plan and status are tracked in [docs/project_plan.md](docs/project_plan.md).

## ⚠️ Disclaimer

This is an educational and research tool. **It is NOT medical advice.** All treatment decisions should be made in consultation with a licensed physician.

## License

MIT

## Contact

Built by Anni — UCLA MDSH '28 (Fall 2026 cohort).
