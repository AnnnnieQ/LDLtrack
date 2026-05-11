# LDLtrack Feature Roadmap

This document tracks planned features across the project's 6-week timeline.
Features are deferred to later phases based on MVP-first principles.

---

## Phase 1: MVP (Week 1-3)

### Core Functionality
- [x] Data: VOYAGER high-intensity statins (20 effect sizes)
- [x] Data: Hasan 2020 weight loss (3 mechanism-stratified rows)
- [ ] Data: Chiavaroli 2018 Portfolio Diet
- [ ] Data: Brown 1999 soluble fiber
- [ ] Data: Ras 2014 plant sterols
- [ ] Data: Smart 2024 exercise
- [ ] Data: IMPROVE-IT (ezetimibe)
- [ ] Data: FOURIER (PCSK9i)
- [ ] Bayesian hierarchical model (PyMC)
- [ ] Streamlit web app deployment
- [ ] Basic UI: intervention selection + LDL prediction output

### Intentionally Excluded from MVP
- ❌ Mid/low intensity statins (Week 4)
- ❌ Time horizon selector (Week 4-5)
- ❌ LDL trajectory visualization (Week 5-6)
- ❌ Subgroup analysis (Week 5-6)
- ❌ Mobile responsive design (Week 6)

---

## Phase 2: V2 Expansion (Week 4-5)

### Data Expansion
- [ ] STELLAR trial (Jones 2003) — head-to-head statin comparisons
- [ ] HPS, CARDS, ASCOT-LLA, JUPITER — additional statin coverage
- [ ] BMI-stratified weight loss meta-analyses (if available)

### Modeling
- [ ] Time-dependent effect curves
  - Statins: full effect by 4-6 weeks
  - Lifestyle weight loss: gradual buildup (30%/70%/100% at 3/6/12 months)
  - Pharma weight loss: peaks at 6 months, slight decline by 12
- [ ] Effect modification by user characteristics
  - Age, sex, ASCVD status, diabetes

### UI
- [ ] Time horizon selector (3mo / 6mo / 12mo)
- [ ] Per-intervention contribution breakdown
- [ ] Out-of-distribution warnings (e.g., for BMI < 30 user)
- [ ] Educational tooltips on intervention mechanisms

### Validation
- [ ] Hold-out trial validation
- [ ] Calibration plot (predicted vs observed)
- [ ] Sensitivity analyses (priors, SE assumptions)

---

## Phase 3: V3 Finalization (Week 6)

### Visualization
- [ ] LDL trajectory chart (Plotly): show effect curve over time
- [ ] Forest plot of effect sizes by category
- [ ] Posterior predictive distribution display

### Documentation
- [ ] Comprehensive methodology.md
- [ ] data_sources.md with PRISMA-style flow
- [ ] limitations.md
- [ ] Demo video (5 min)
- [ ] Optional: blog post on Medium / personal website

### Polish
- [ ] Mobile-responsive UI
- [ ] Loading states, error handling
- [ ] Final deployment to Streamlit Cloud (custom URL if possible)
- [ ] Resume bullets and elevator pitch

---

## Time-Course of Effects (Reference)

| Intervention | Onset | Peak Effect | Notes |
|-------------|-------|------------|-------|
| Statin | 1 week | 4-6 weeks ⚡ | Stable thereafter |
| Ezetimibe | 1 week | 2 weeks ⚡ | Stable thereafter |
| PCSK9i | 1-2 weeks | 2-4 weeks ⚡ | Injection schedule |
| Bempedoic acid | 2 weeks | 4-8 weeks | Similar to statin |
| Portfolio Diet | 2-4 weeks | 6-8 weeks | Food-based |
| Soluble fiber | 1-2 weeks | 4-6 weeks | Direct absorption effect |
| Plant sterols | 2-4 weeks | 4-8 weeks | Similar to fiber |
| Weight loss (lifestyle) | 3 months | 6-12 months ⏳ | Gradual buildup |
| Weight loss (pharma) | 1-3 months | 6 months | Faster than lifestyle |
| Weight loss (surgery) | 1-3 months | 6-12 months | Rapid then plateau |
| Exercise | 8-12 weeks | 3-6 months ⏳ | Fitness-dependent |

Reference: derived from clinical guidelines (2018 ACC/AHA, 2019 ESC/EAS) and 
intervention-specific RCTs.