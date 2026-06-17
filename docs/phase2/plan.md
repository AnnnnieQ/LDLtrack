# Phase 2 Plan & Project Context

This document captures planning context not otherwise visible in the repo
(milestones, day-by-day schedule, working preferences, decisions made in
planning discussions). Claude Code should read this first each session.

---

## Project Goal (Recap)

LDLtrack is a Bayesian decision-support tool for personalized LDL-C
reduction. It synthesizes evidence from RCTs/meta-analyses into individual
predictions with explicit uncertainty quantification.

**Personal motivation**: Owner's partner has high coronary artery calcium
(CAC) and high LDL — there is a real family health decision behind this,
not just a portfolio exercise.

**Career motivation**: Portfolio piece for 2027 data science internship
applications, targeting health-sector ML roles (Genentech, Tempus,
Flatiron Health, Verily). Owner starts UCLA MDSH (Master of Data Science
in Health) in Fall 2026.

**Internship timeline context**: Applications open ~Sep-Nov 2026. Phase 2
should finish by ~mid-June 2026, leaving Phase 3 polish through summer.

---

## Phase Structure

- **Phase 1 — Data collection** ✅ COMPLETE
  - 2026-05-06 to 2026-05-19 (13 days)
  - 8 papers, 39 effect-size rows, 21-column schema
  - 6 Known Schema Issues documented in data/README.md for Phase 3

- **Phase 2 — Bayesian model** ✅ COMPLETE
  - Goal: working PyMC model + toy Streamlit demo
  - 3 milestones (below)
  - Realistic estimate: ~3 weeks

- **Phase 3 — Refinement** (not yet planned)
  - Schema v2 refactor (resolve the 6 Known Schema Issues)
  - CVD risk reduction calculation (Mach 2020 formula)
  - Full Streamlit UI polish + deployment

Note: project uses "Phase" naming, NOT "Week" naming. Earlier handoff
docs may say "Week 1/2/3" — that scheme is deprecated. Phase 1 actually
took 13 days, so phase labels are tied to milestones, not calendar weeks.

---

## Phase 2 Goal (Detailed)

Build a Bayesian model that takes a user's baseline LDL and chosen
interventions, and outputs predicted final LDL with a credible interval.

Scope for Phase 2 = single-intervention model + multiplicative
combination of multiple interventions + a quick Streamlit demo.

**Explicitly OUT of Phase 2 scope** (deferred to Phase 3):
- Schema v2 refactor (splitting population/n columns, adding
  effect_timing/baseline_timing/cost_tier/control_type fields)
- CVD risk reduction calculation
- Full polished UI / multi-step wizard
- Deployment (Streamlit Cloud / Hugging Face)
- Adding more papers
- Hierarchical model with subgroup covariates

---

## Milestones

### Milestone 2.1 — PyMC + Bayesian basics (~7 days)

Goal: be able to independently write a simple PyMC model, run MCMC,
and interpret the posterior + diagnostics.

Approach: learn-by-doing. Short videos/docs only (owner cannot sustain
long videos or long docs). Most time spent writing and running code.

- [x] **Day 1** — Env setup (PyMC 5.28 + ArviZ in conda env `ldltrack`)
      + grid approximation by hand (coin flip: 7/10 heads, estimate p).
      Covered prior/likelihood/posterior intuition + prior-strength
      experiment. Notebook in notebooks/scratch/ (gitignored).
- [x] **Day 2** — Redo the coin flip in PyMC; understand how MCMC
      sampling replaces grid approximation. Basic PyMC syntax
      (pm.Model, prior, likelihood, pm.sample). Read trace plots.
- [x] **Day 3** — PyMC linear regression (follow official tutorial,
      modify fake data, rerun).
- [x] **Day 4** — PyMC Bayesian meta-analysis / hierarchical partial
      pooling example (closest to LDLtrack's use case).
- [x] **Day 5** — Toy model on a real LDLtrack data subset (e.g., the
      4 VOYAGER all_patients rows: a mini random-effects meta-analysis).
- [x] **Day 6** — Debug + improve toy model + ArviZ visualization.
- [x] **Day 7** — Cleanup + milestone commit.

Milestone 2.1 exit criteria: can write a simple PyMC model unaided,
run sampling, read a trace plot to judge convergence (R-hat < 1.01),
and understand the hierarchical structure of a Bayesian meta-analysis.

### Milestone 2.2 — Single-intervention LDLtrack model (~7-10 days) ✅ COMPLETE

Goal: PyMC model that ingests the LDLtrack CSV and, for a single
intervention, outputs posterior + predicted final LDL + 95% CrI,
roughly consistent with paper-reported effects.

Includes: model design doc (docs/model_design_v1.md), src/data_loader.py,
src/model_v1.py, a validation notebook, ArviZ posterior visualization.

### Milestone 2.3 — Combination + Streamlit demo (~7 days) ✅ COMPLETE

Goal: a localhost-runnable Streamlit app where a user inputs baseline
LDL + selects 2-3 interventions and sees predicted final LDL + chart.

Includes: multiplicative combination on % scale, basic Streamlit UI,
pre-computed posterior loaded at startup.

Delivered: app.py (statin × 4 + plant sterols dose-response + exercise);
combine() with independent shuffle; build_model mode flag; load_single_row;
mg_dL → % unit conversion in predict(); edge-case validated.

---

## Key Design Questions for Milestone 2.2 (resolved in 2.2/2.3)

1. **Unit handling** — Resolved: mg/dL→% conversion done in predict() at
   inference time using user baseline as the denominator; applied only to
   the exercise row (Smart 2024 reports in mg/dL). mg_dL_per_kg and
   mg_dL_per_g units are not yet handled — rows using those units are
   excluded from the Phase 2 MVP and deferred to Phase 3 schema v2.
2. **Combination** — Resolved: multiplicative on % scale via combine() with
   per-sample shuffle for independence. on_top_of constraints NOT implemented
   in the 3-intervention MVP (statin, plant sterols, exercise have no
   mutual dependencies); deferred to Phase 3.
3. **Priors** — Resolved: alpha_mu from paper point estimates; alpha_sd set
   to ~3× CI half-width so the single-row likelihood dominates.
4. **Missing SE rows** — Resolved: Cannon 2015 and Smart 2024 RT-null row
   excluded (no SE); both deferred to Phase 3.
5. **Output** — Resolved: predict() returns posterior theta_new (% change)
   and ldl_final (mg/dL); 95% CrI displayed in Streamlit app.

---

## Known Cross-Row Data Caveats (relevant when modeling)

- 4 different ldl_change_unit values — likelihood must be unit-aware.
- on_top_of field: some rows are standalone, some require a statin or
  NCEP diet background.
- Cannon 2015 baseline (69.5) is a 1-year on-treatment value;
  Sabatine 2017 baseline (92) is a randomization baseline. Same
  on_top_of=statin tag but different baseline timing semantics — see
  Known Schema Issue #6 in data/README.md.
- VOYAGER rows have baseline_ldl_mg_dl = NA.
- Some rows have no CI (Cannon 2015; Smart 2024 RT-null row).

---

## Working Preferences

- **Language**: discussion in Chinese; all repo files (code, comments,
  docs, commit messages) in English only. Verify no Chinese characters
  before committing.
- **Format**: keep responses short. Owner cannot sustain long videos or
  long docs — prefer short clips and search-style doc reading.
- **Learning style**: learn-by-doing. Hands-on coding over passive
  consumption. Explain concepts concretely with small numeric examples.
- **Commit style**: short messages — 1-line title (~50 chars) + 2-3 line
  explanation. No bullet lists. No "Day N" prefix in commit titles.
- **Git workflow**: `git add .` (not `git add *`). Verify staged files
  before commit. `.gitignore` is a hard filter.
- **Decision style**: present options with trade-offs, don't fake a
  single recommendation. Owner pushes back on inconsistencies — take
  those observations seriously.
- **CSV editing**: never edit the CSV in Numbers/Excel (breaks format).
  Use a text editor or VS Code.

---

## Notebook Organization

- `notebooks/scratch/` — learning/practice notebooks. GITIGNORED.
  Not shown on GitHub. All Milestone 2.1 day notebooks go here.
- `notebooks/phase2/` — display-worthy notebooks (e.g., the real
  LDLtrack model validation notebook from Milestone 2.2 onward).
  These ARE committed.

---

## Environment

- macOS, Apple Silicon (osx-arm64)
- conda env: `ldltrack`, Python 3.11, via Miniforge
- PyMC 5.28.5, ArviZ 0.23.4
- Repo: github.com/anni-qi/LDLtrack (SSH)
- Working dir: ~/Desktop/LDLtrack
- Jupyter kernel registered as "Python (ldltrack)"

---

## Known Limitations (deferred to Phase 3)

- **Exercise dose-response**: Smart 2024's LDL meta-regression included no
  exercise-dose predictor (only age and study size), so the exercise effect
  is not stratified by frequency or intensity. Phase 3 should seek a
  dose-stratified LDL meta-analysis.
- **Biological floor**: The multiplicative combination applies no biological
  floor. At low baseline LDL with multiple strong interventions, the model
  can predict <~25 mg/dL — a clinically implausible level. Phase 3 should
  add a soft floor (e.g., logistic saturation or a 25 mg/dL lower bound).

---

## Current Status

  Phase 2 complete. Milestones 2.1, 2.2, 2.3 all done.
  Deliverables: PyMC Bayesian models (intercept_only + dose_response modes),
  data_loader, predict(), combine(), milestone22/23 validation notebooks,
  and localhost Streamlit demo (app.py).
  Next: Phase 3 — schema v2 refactor, CVD risk calculation, UI polish, deployment.
