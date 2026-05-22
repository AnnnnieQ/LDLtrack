# LDLtrack 🫀

> **A Bayesian decision-support tool for personalized LDL-C management** — synthesizing evidence from randomized controlled trials into individualized predictions with explicit uncertainty quantification.

🚧 **Status**: Phase 2 in progress — Bayesian model implementation

🔗 **Live Demo**: *(coming soon)*
📊 **Methodology**: [data/README.md](data/README.md)
📝 **Data Sources**: [SOURCES.md](SOURCES.md)

---

## Why This Project?

Existing LDL-C calculators (e.g., [lipidtools.com](https://lipidtools.com/calculator-pages/ldlc/), ACC's [LDL-C Lowering Therapy tool](https://tools.acc.org/LDL/ldlc_lowering_therapy/)) suffer from three key limitations:

1. **Pharmacology only** — Lifestyle interventions (diet, exercise, weight loss) are not modeled, despite strong evidence for their LDL-lowering effects.
2. **Single-point estimates** — No uncertainty quantification, despite substantial heterogeneity in individual response.
3. **One-size-fits-all** — No effect modification by patient characteristics.

LDLtrack addresses these gaps by:

- ✅ Integrating pharmacological + dietary + lifestyle interventions
- ✅ Using Bayesian hierarchical modeling with proper uncertainty propagation
- ✅ Producing posterior predictive distributions rather than single numbers
- ✅ Incorporating effect modification by user characteristics where evidence supports it

## Evidence Base

39 effect sizes curated from 8 landmark RCTs and meta-analyses across 7 intervention categories:

| Category | Source | Rows |
|---|---|---|
| Statin (4 agents × 5 subgroups) | VOYAGER (Karlson 2015) | 20 |
| Weight loss (3 mechanisms) | Hasan 2020 | 3 |
| Portfolio diet (efficacy + effectiveness) | Chiavaroli 2018 | 2 |
| Soluble fiber (pooled + by type) | Brown 1999 | 4 |
| Plant sterols (dose-response, 6 bins) | Ras 2014 | 6 |
| Exercise (aerobic/combined vs resistance) | Smart 2024 | 2 |
| Ezetimibe added to statin | Cannon 2015 (IMPROVE-IT) | 1 |
| PCSK9 inhibitor added to statin | Sabatine 2017 (FOURIER) | 1 |

See [data/README.md](data/README.md) for per-paper extraction methodology.

## Tech Stack

PyMC · ArviZ · NumPy · Pandas · Plotly · Streamlit

## Roadmap

- [x] **Phase 1** — Evidence extraction from RCTs and meta-analyses (8 papers, 39 rows)
- [ ] **Phase 2** — Bayesian model in PyMC + toy Streamlit demo
    - [ ] Milestone 2.1: PyMC + Bayesian basics
    - [ ] Milestone 2.2: Single-intervention LDLtrack model
    - [ ] Milestone 2.3: Multi-intervention combination + Streamlit demo
- [ ] **Phase 3** — Schema v2 refactor, CVD risk reduction, full UI polish, deployment

Detailed feature plans in [docs/feature_roadmap.md](docs/feature_roadmap.md).

## ⚠️ Disclaimer

This is an educational and research tool. **It is NOT medical advice.** All treatment decisions should be made in consultation with a licensed physician.

## License

MIT

## Contact

Built by Anni — UCLA MDSH '28 (Fall 2026 cohort).