# Effect Sizes Database

Curated effect sizes from published RCTs and meta-analyses for the LDLtrack project.

## Schema (v2)

This CSV uses a 21-column schema designed to handle heterogeneous intervention types
(pharmacological, lifestyle, combination). Each row represents one effect size estimate
from a specific paper for a specific intervention-population combination.

Key columns:
- `intervention_category`: high-level type (statin, weight_change, diet, fiber, plant_sterols, exercise, combination_drug)
- `intervention_subtype`: mechanism/method when relevant (e.g., via_diet_exercise vs via_pharmacotherapy)
- `dose_unit`: unit of dose (mg, g, kg_lost, min_per_week)
- `ldl_change_unit`: unit of effect (percent, mg_dL, mg_dL_per_kg, mg_dL_per_g)
- `on_top_of`: for combination therapies, what base treatment is assumed
- `evidence_quality`: tag for source quality and study characteristics

## Sources Currently Included

### 1. Karlson BW et al. 2015 (VOYAGER meta-analysis)
- *Atherosclerosis* 241(2):450-454 | PMID: 26074319
- 8,496 patient exposures from 32,258 in VOYAGER database (37 RCTs)
- Data extracted: Figure 1 (LSM percentage change in LDL-C by statin benefit group)
- Coverage: Atorvastatin 40/80mg, Rosuvastatin 20/40mg across 5 patient subgroups
- Rows: 20 | Verification: All values verified against original Figure 1
- Standard errors: Visually estimated from error bars (1.0-1.5%)

### 2. Hasan B et al. 2020 (Weight loss meta-analysis)
- *J Clin Endocrinol Metab* 105(12):3695-3703 | PMID: 32954416
- 73 RCTs total enrolling 32,496 patients, broken into 3 mechanism subsets:
  - Lifestyle (diet/exercise/both): 30 RCTs, n=2,434
  - Pharmacotherapy: 35 RCTs, n=16,333
  - Bariatric surgery: 8 RCTs, n=377
- Population: overweight/obese adults (mean BMI 36.3 kg/m²)
- Data extracted: Table 1 (per 1-kg weight loss at 12 months)
- Rows: 3 (one per mechanism)

### 3. Chiavaroli L et al. 2018 (Portfolio Diet meta-analysis)
- *Prog Cardiovasc Dis* 61(1):43-53 | PMID: 29807048
- 7 trial comparisons, 439 participants with hyperlipidemia (no diabetes, no CVD history)
- Population: Middle-aged (median 57y), overweight (median BMI 27), hyperlipidemic 
  (median baseline LDL 4.4 mmol/L = ~170 mg/dL)
- Intervention: Portfolio dietary pattern (4 components: nuts, plant protein, viscous 
  fibre, plant sterols) on background of NCEP Step II diet
- Data extracted: Page 7 sensitivity analysis (efficacy vs effectiveness subsets)
- Rows: 2 (separated by adherence level)
  - **Efficacy** (5 trials, n=94, metabolically-controlled feeding, >90% adherence): 
    **-21%** LDL (95% CI: -23 to -17%)
  - **Effectiveness** (2 trials, n=345, dietary advice only, <50% adherence): 
    **-11%** LDL (95% CI: -14 to -9%)
- GRADE: HIGH certainty for LDL-C
- Notes: Both subsets show I² = 0% (no within-group heterogeneity), confirming adherence 
  is the primary driver of variability in pooled analyses.
  
  ## Source 4: Brown 1999 (Soluble Fiber)

**Citation**: Brown L, Rosner B, Willett WW, Sacks FM. Cholesterol-lowering 
effects of dietary fiber: a meta-analysis. *Am J Clin Nutr* 1999;69(1):30-42. 
PMID: 9925120.

**Study design**: Meta-analysis of 67 controlled trials, total ~2990 participants.
Linear regression on type and dose of soluble fiber.

**Rows added**: 4 (1 overall pooled + 3 by fiber type: oat, psyllium, pectin)

**Why 4 rows**:
- Paper reports both pooled "all fibers" effect and by-type effects in Table 2
- Abstract claims "no significant difference between oat, psyllium, pectin"
  (statistical claim: CIs overlap)
- Point estimates differ: oat -1.43, psyllium -2.59, pectin -2.13 mg/dL/g
- Both pooled and by-type rows preserved for modeling flexibility in Week 2
- Guar gum excluded: paper reports insufficient data in practical dose range

**Dose range decision**: Used **practical range (≤8 g/d for LDL)** data only,
not full range (2-30 g/d). Reasons:
- Paper footnote 2: dose response is non-linear at higher doses
- Abstract's headline -0.057 mmol/L/g figure is from practical range
- Real-world users consume 2-10 g/d soluble fiber, matching this range
- Full range estimates would systematically underestimate effect at typical doses

**Unit conversion**: Paper reports in mmol/L/g. Converted to mg/dL/g using 
factor 38.67 (per paper's Table 2 footnote 3: divide by 0.02586).
All 4 row values verified by manual calculation.

**Effect sizes** (per gram soluble fiber daily, practical dose range):

| Row | n studies | n subjects | LDL (mg/dL/g) | 95% CI |
|-----|-----------|------------|---------------|--------|
| Overall pooled | 22 | 1,151 | -2.20 | -2.71, -1.70 |
| Oat products | 13 | 867 | -1.43 | -1.55, -1.31 |
| Psyllium | 4 | 151 | -2.59 | -5.65, -0.54 |
| Pectin | 4 | 117 | -2.13 | -3.36, -0.85 |

**`on_top_of` decision**: NA. Paper explicitly tests background diet as 
covariate and finds effect is independent of background dietary fat content 
(Results paragraph 4). Contrast with Chiavaroli 2018 where Portfolio Diet 
effect is on top of NCEP Step II diet — there `on_top_of` field is populated.

**Population caveat**: Mixed sample across the 67 trials per Table 1:
21 healthy / 30 hyperlipidemic / 9 DM / 5 DM+hyperlipidemic / 2 other.
Mean baseline LDL = 4.25 ± 0.72 mmol/L = 164 ± 28 mg/dL.
Effect may differ in users with much lower baseline LDL (<130 mg/dL); 
% effect likely similar, absolute effect likely smaller.

**Methodology caveat**: Pre-GRADE methodology (1999 paper). Quality assessment
not done by modern systematic review standards. Treat as moderate-quality
evidence despite large trial count.

---

## Known Schema Issues (to revisit in Week 4)

**`population` column inconsistency**: Current granularity varies across rows:
- VOYAGER rows use short labels (e.g., `ASCVD`, `diabetes`)
- Hasan/Chiavaroli/Brown rows use long composite strings 
  (e.g., `hyperlipidemic_adults_no_DM_no_CVD`)
- Long strings encode multiple dimensions in one field (lipid status + 
  comorbidities + baseline values), violating one-fact-per-column principle
- Some information is redundant with `baseline_ldl_mg_dl` column

**Planned resolution (Week 4)**: Split `population` into orthogonal columns:
`population_category`, `has_dm`, `has_cvd`, `baseline_bmi`, etc. 
Decision deferred until all Week 1 papers extracted to see full schema needs.

**`intervention_subtype` semantics**: Currently used for both mechanism 
classification (e.g., `via_diet_exercise`) and chemical classification 
(e.g., `soluble_fiber_beta_glucan`). May need to split into two fields, 
or accept as a flexible "细分维度" field. Revisit Week 4.

## Important Caveats

### Weight Loss Effects and BMI Extrapolation
Hasan 2020 reports effects in a population with **mean BMI 36.3 kg/m²** (severely obese).
The per-kg effect values (lifestyle: -1.28 mg/dL/kg; pharma: -1.67 mg/dL/kg) are 
population means.

**Why this matters**:
- LDL response to weight loss may differ across BMI ranges
- We do NOT rescale effects based on user BMI (no BMI-stratified data available)
- The Bayesian model will use wider priors for weight_change interventions to reflect
  generalizability uncertainty
- The tool's UI will warn users with BMI < 30 that effects are extrapolated from a 
  different population

### Portfolio Diet Adherence Variability
Chiavaroli 2018 reveals striking adherence-dependent effects, encoded as two rows:

| Adherence | LDL Reduction | n trials | n patients |
|-----------|---------------|----------|------------|
| Strict (foods provided) | **-21%** | 5 | 94 |
| Real-world (advice only) | **-11%** | 2 | 345 |

Both subsets show I² = 0% (no within-group heterogeneity), so adherence is the primary 
driver of the variability seen in pooled analyses. This duality lets users in the tool 
select expected adherence rather than getting a single averaged estimate.

### Portfolio Diet NCEP Background
All Portfolio Diet effects are measured **on top of** an NCEP Step II diet (≤30% fat, 
<7% saturated fat, <200 mg/day cholesterol). The Portfolio Diet alone (without NCEP 
background) has not been studied in this meta-analysis. Users on typical Western diets 
may see additional benefit from baseline diet modification before adding Portfolio 
components.

### Time-Course of Effects
Different interventions take different times to reach full effect. The CSV currently 
records 12-month effects (for time-dependent interventions like weight loss) or trial 
endpoint effects (for pharmacologic interventions). The `notes` column documents 
time-course information where known.

**MVP approach**: Use trial endpoint / 12-month values as default predictions.
**V2 expansion (Week 4-5)**: Add time horizon selector and progressive effect curves.

### Statistical Heterogeneity (I²)
Hasan 2020 reports very high I² (>80%) for LDL effects, indicating substantial 
between-trial heterogeneity. This is reflected in the wide confidence intervals and 
will be modeled via wider Bayesian priors for these interventions.

### Statistical Significance
- Bariatric surgery's per-kg LDL effect (-0.33 mg/dL) is **NOT statistically significant** 
  (CI: -0.77 to +0.10 crosses zero). This is preserved in the CSV but the Bayesian model 
  will treat this as a high-uncertainty estimate.

### Bariatric Surgery — Surprising Finding
Despite producing the largest weight loss, bariatric surgery has the smallest per-kg 
LDL effect (and is not statistically significant). This reflects mechanism-specific 
effects beyond simple weight reduction. The tool's UI should educate users on this.