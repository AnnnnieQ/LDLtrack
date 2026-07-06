# LDLtrack

> **A Bayesian decision-support tool for personalized LDL-C management** — synthesizing evidence from randomized controlled trials into individualized predictions with explicit uncertainty quantification.

**Status**: Phase 3 in progress — deployed Streamlit demo + cardiovascular risk conversion

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

The deployed app currently supports:

- Statins: atorvastatin 40/80 mg and rosuvastatin 20/40 mg
- Plant sterols: dose-response prediction from 0.6-3.3 g/day
- Aerobic/combined exercise
- Multiplicative combination of selected interventions
- Posterior uncertainty via pre-sampled NetCDF artifacts
- Relative and absolute cardiovascular risk reduction estimates

## Tech Stack

PyMC · ArviZ · NumPy · Pandas · Streamlit

## Roadmap

- [x] **Phase 1** — Evidence extraction from RCTs and meta-analyses (8 papers, 39 rows)
- [x] **Phase 2** — Bayesian model in PyMC + toy Streamlit demo
    - [x] Milestone 2.1: PyMC + Bayesian basics
    - [x] Milestone 2.2: Single-intervention LDLtrack model
    - [x] Milestone 2.3: Multi-intervention combination + Streamlit demo
- [ ] **Phase 3** — CVD risk conversion, UI polish, deployment, schema v2 refactor
    - [x] Milestone 3.1: Cardiovascular risk conversion
    - [x] Milestone 3.4: UI polish + public Streamlit deployment
    - [ ] Schema v2 refactor and additional intervention support

Detailed feature plans in [docs/feature_roadmap.md](docs/feature_roadmap.md).

## ⚠️ Disclaimer

This is an educational and research tool. **It is NOT medical advice.** All treatment decisions should be made in consultation with a licensed physician.

## License

MIT

## Contact

Built by Anni — UCLA MDSH '28 (Fall 2026 cohort).
