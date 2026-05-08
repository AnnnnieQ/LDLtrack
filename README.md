# LDLtrack 🫀

> **A Bayesian decision-support tool for personalized LDL-C management** — synthesizing evidence from randomized controlled trials into individualized predictions with explicit uncertainty quantification.

🚧 **Status**: Work in Progress (Week 1 of 4)

🔗 **Live Demo**: *(coming soon)*
📊 **Methodology**: [docs/methodology.md](docs/methodology.md)
📝 **Data Sources**: [docs/data_sources.md](docs/data_sources.md)

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

## Tech Stack

- **Statistical Modeling**: PyMC, ArviZ
- **Numerics**: NumPy, SciPy, Pandas
- **Visualization**: Plotly, Matplotlib
- **Web App**: Streamlit
- **Deployment**: Streamlit Community Cloud

## Roadmap

- [x] **Week 1**: Evidence extraction from RCTs and meta-analyses
- [ ] **Week 2**: Bayesian hierarchical model + Monte Carlo simulation
- [ ] **Week 3**: Intervention combination logic + Streamlit web app
- [ ] **Week 4**: Validation, deployment, polishing

## ⚠️ Disclaimer

This is an educational and research tool. **It is NOT medical advice.** All treatment decisions should be made in consultation with a licensed physician.

## License

MIT

## Contact

Built by Anni — UCLA MDSH '28 (Fall 2026 cohort).