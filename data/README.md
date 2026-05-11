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

## Important Caveats

### Weight Loss Effects and BMI Extrapolation
Hasan 2020 reports effects in a population with **mean BMI 36.3 kg/m²** (severely obese).
The per-kg effect values (lifestyle: -1.28 mg/dL/kg; pharma: -1.67 mg/dL/kg) are population means.

**Why this matters**:
- LDL response to weight loss may differ across BMI ranges
- We do **NOT** rescale effects based on user BMI (no BMI-stratified data available)
- The Bayesian model will use **wider priors** for weight_change interventions to reflect
  generalizability uncertainty
- The tool's UI will warn users with BMI < 30 that effects are extrapolated from a 
  different population

**Future improvement**: Search for BMI-stratified meta-analyses in Week 4-5 if available.

### Time-Course of Effects
Different interventions take different times to reach full effect. The CSV currently
records 12-month effects, but `notes` column documents the time-course where known:
- Statins: stable effect at 4-6 weeks
- Weight loss (lifestyle): gradual buildup, ~30% at 3mo, ~70% at 6mo, full at 12mo
- Weight loss (pharma): faster buildup, peaks around 6mo
- Bariatric surgery: rapid initial change, plateau at 12mo

**MVP approach**: Use 12-month values as default predictions.
**V2 expansion (Week 4-5)**: Add time horizon selector (3mo / 6mo / 12mo).

### Statistical Heterogeneity (I²)
Hasan 2020 reports very high I² (>80%) for LDL effects, indicating substantial 
between-trial heterogeneity. This is reflected in the wide confidence intervals and
will be modeled via wider Bayesian priors for these interventions.

### Statistical Significance
- Bariatric surgery's per-kg LDL effect (-0.33 mg/dL) **is NOT statistically significant** 
  (CI: -0.77 to +0.10 crosses zero). This is preserved in the CSV but the Bayesian model 
  will treat this as a high-uncertainty estimate.

### Bariatric Surgery LDL Effect Surprising Finding
Despite producing the largest weight loss, bariatric surgery has the **smallest per-kg
LDL effect** (and is not statistically significant). This reflects mechanism-specific
effects beyond simple weight reduction. The tool's UI should educate users on this.

## Planned Additions

The following papers are candidates for data extraction in upcoming days:

### Week 1 remaining (Days 4-5)
- Chiavaroli L et al. (2018). Portfolio Diet meta-analysis. *Prog Cardiovasc Dis* | PMID: 29807048
- Brown L et al. (1999). Soluble fiber meta-analysis. *Am J Clin Nutr* | PMID: 9925120
- Ras RT et al. (2014). Plant sterols dose-response meta-analysis | PMID: 24780031
- Smart NA et al. (2024). Exercise meta-analysis. *Sports Medicine* | PMID: 39331324
- Cannon CP et al. (2015). IMPROVE-IT (ezetimibe + statin) | PMID: 26039521
- Sabatine MS et al. (2017). FOURIER (PCSK9 inhibitor) | PMID: 28304224

### Week 4 (statin coverage expansion)
- Jones PH et al. (2003). STELLAR trial — multi-statin head-to-head | PMID: 12888132
- Heart Protection Study (HPS, 2002): simvastatin 40mg
- CARDS (Colhoun 2004): atorvastatin 10mg in diabetes | PMID: 15325833
- ASCOT-LLA (Sever 2003): atorvastatin 10mg in hypertension | PMID: 12686036
- JUPITER (Ridker 2008): rosuvastatin 20mg primary prevention | PMID: 18997196