# LDLtrack Feature Roadmap

This document tracks planned features across the project's 6-week timeline.
Features are deferred to later phases based on MVP-first principles.

---

## Phase 1: MVP (Week 1-3)

### Core Functionality
- [ ] Data: ~30 effect sizes across major intervention categories
  - Statins (high-intensity) ✅
  - Weight change (lifestyle / pharma / surgery) ✅
  - Diet patterns (Portfolio Diet, etc.)
  - Dietary supplements (soluble fiber, plant sterols)
  - Exercise
  - Combination therapy (statin + ezetimibe, PCSK9i)
- [ ] Bayesian hierarchical model (PyMC)
- [ ] Streamlit web app deployment
- [ ] Basic UI: intervention selection + LDL prediction output

### Intentionally Excluded from MVP
- ❌ Mid/low intensity statins (Week 4)
- ❌ Time horizon selector (Week 4-5)
- ❌ LDL trajectory visualization (Week 5-6)
- ❌ Subgroup analysis beyond what data permits (Week 5-6)
- ❌ Mobile responsive design (Week 6)

---

## Phase 2: V2 Expansion (Week 4-5)

### Data Expansion
- [ ] Mid/low intensity statin coverage (head-to-head trials)
- [ ] BMI-stratified weight loss meta-analyses (if available)

### Modeling
- [ ] Time-dependent effect curves
  - Statins: full effect by 4-6 weeks
  - Lifestyle weight loss: gradual buildup (30%/70%/100% at 3/6/12 months)
  - Pharma weight loss: peaks at 6 months, slight decline by 12
- [ ] Effect modification by user characteristics (age, sex, ASCVD status, diabetes)

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
- [ ] LDL trajectory chart (Plotly): effect curve over time
- [ ] Forest plot of effect sizes by category
- [ ] Posterior predictive distribution display

### Documentation
- [ ] Comprehensive methodology.md
- [ ] data_sources.md with PRISMA-style flow
- [ ] limitations.md
- [ ] Demo video (5 min)
- [ ] Optional: blog post

### Polish
- [ ] Mobile-responsive UI
- [ ] Loading states, error handling
- [ ] Final deployment to Streamlit Cloud
- [ ] Resume bullets and elevator pitch

---

## Time-Course of Effects (Reference)

Used for Phase 2 time-dependent modeling. Derived from clinical guidelines 
(2018 ACC/AHA, 2019 ESC/EAS) and intervention-specific literature.

| Intervention | Onset | Peak Effect |
|-------------|-------|------------|
| Statin | 1 week | 4-6 weeks ⚡ |
| Ezetimibe | 1 week | 2 weeks ⚡ |
| PCSK9i | 1-2 weeks | 2-4 weeks ⚡ |
| Portfolio Diet | 2-4 weeks | 6-8 weeks |
| Soluble fiber | 1-2 weeks | 4-6 weeks |
| Plant sterols | 2-4 weeks | 4-8 weeks |
| Weight loss (lifestyle) | 3 months | 6-12 months ⏳ |
| Weight loss (pharma) | 1-3 months | 6 months |
| Weight loss (surgery) | 1-3 months | 6-12 months |
| Exercise | 8-12 weeks | 3-6 months ⏳ |