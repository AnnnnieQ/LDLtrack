# Sources

This file documents papers and references **actually used** in the project.
Papers are added here only after their data has been extracted and verified.

---

## 1. Karlson BW, Palmer MK, Nicholls SJ, Lundman P, Barter PJ. (2015)

**Title**: "To what extent do high-intensity statins reduce low-density lipoprotein 
cholesterol in each of the four statin benefit groups identified by the 2013 American 
College of Cardiology/American Heart Association guidelines? A VOYAGER meta-analysis."

- Journal: *Atherosclerosis* 2015;241(2):450-454
- PMID: 26074319
- DOI: 10.1016/j.atherosclerosis.2015.05.029
- Database: VOYAGER (sponsored by AstraZeneca)
- Sample: 8,496 patient exposures from 32,258 in VOYAGER (37 RCTs total)
- Data extracted: Figure 1 (LSM percentage change in LDL-C by statin benefit group)
- Coverage in dataset: Atorvastatin 40/80mg, Rosuvastatin 20/40mg (high-intensity statins)
- Rows in dataset: 20
- Verification status: All 20 data points verified against original Figure 1

## 2. Hasan B, Nayfeh T, Alzuabi M, et al. (2020)

**Title**: "Weight Loss and Serum Lipids in Overweight and Obese Adults: A Systematic
Review and Meta-Analysis."

- Journal: *J Clin Endocrinol Metab* 2020;105(12):3695-3703
- PMID: 32954416
- DOI: 10.1210/clinem/dgaa673
- Study type: Systematic review + meta-analysis of RCTs
- Sample: 73 RCTs enrolling 32,496 patients total
  - Lifestyle subset: 30 RCTs, n=2,434
  - Pharmacotherapy subset: 35 RCTs, n=16,333
  - Bariatric surgery subset: 8 RCTs, n=377
- Population: Overweight/obese adults (mean age 48.1, mean BMI 36.3 kg/m², mean weight 101.6 kg)
- Data extracted: Table 1 (per 1-kg weight loss at 12 months) + Figure 2 (baseline lipid values)
- Coverage in dataset: Weight change via 3 mechanisms (lifestyle, pharmacotherapy, bariatric surgery)
- Rows in dataset: 3 (one per mechanism)
- Verification status: All 3 effect estimates verified against Table 1; sample sizes verified
  against Results text; baseline LDL values verified against Figure 2

## 3. Chiavaroli L, Nishi SK, Khan TA, et al. (2018)

**Title**: "Portfolio Dietary Pattern and Cardiovascular Disease: A Systematic Review 
and Meta-analysis of Controlled Trials."

- Journal: *Progress in Cardiovascular Diseases* 2018;61(1):43-53
- PMID: 29807048
- Study type: Systematic review + meta-analysis with GRADE assessment
- Sample: 7 trial comparisons, 439 participants with hyperlipidemia
- Data extracted: Page 7 (efficacy/effectiveness sensitivity analysis) and Figure 2 (overall pooled)
- Rows in dataset: 2 (efficacy and effectiveness subgroups)
  - Efficacy: -0.87 mmol/L (-21%), 5 trials, n=94
  - Effectiveness: -0.50 mmol/L (-11%), 2 trials, n=345
- GRADE certainty: HIGH for LDL-C
- Verification status: Subset estimates verified against Page 7 text; unit conversion verified.
- Rationale for 2 rows: 10 percentage-point difference between subsets reflects fundamentally 
  different real-world scenarios (idealized vs typical adherence), supporting separate 
  modeling rather than averaging.

## 4. Brown L, Rosner B, Willett WW, Sacks FM (1999)

**Title**: Cholesterol-lowering effects of dietary fiber: a meta-analysis

**Journal**: American Journal of Clinical Nutrition 69(1):30-42

**PMID**: 9925120

**Type**: Meta-analysis of 67 controlled trials, ~2990 participants total

**Used for**: Soluble fiber LDL effects (`intervention_category=fiber`)

**Rows in CSV**: 4 — `BROWN_1999_overall`, `BROWN_1999_oat`, 
`BROWN_1999_psyllium`, `BROWN_1999_pectin`

**Key data extracted**: Per-gram LDL change in practical dose range (≤8 g/d).
Overall pooled: -2.20 mg/dL/g (95% CI: -2.71, -1.70).

**Methodology caveats**: Pre-GRADE methodology; effect is "small but real" 
per paper's own conclusion; guar gum excluded due to insufficient data 
in practical dose range.

## 5. Ras RT, Geleijnse JM, Trautwein EA (2014)

**Title**: LDL-cholesterol-lowering effect of plant sterols and stanols 
across different dose ranges: a meta-analysis of randomised controlled 
studies

**Journal**: British Journal of Nutrition 112(2):214-219

**PMID**: 24780090

**Type**: Meta-analysis of 124 RCT studies (201 study arms), 
random-effects model

**Used for**: Plant sterols/stanols dose-response LDL effects 
(`intervention_category=plant_sterols`)

**Rows in CSV**: 6 — `RAS_2014_dose1` through `RAS_2014_dose6` 
(one per dose bin, 0.6-3.3 g/d)

**Key data extracted**: Dose-response curve for combined sterols + 
stanols. Effect ranges from -5.7% (0.6 g/d) to -12.4% (3.3 g/d).

**Methodology caveats**: Open access (CC-BY 3.0); two authors employed 
by Unilever (PS product manufacturer); paper excludes >4 g/d data due 
to scarcity; sterols and stanols pooled per paper's main finding of 
comparable efficacy.

## 6. Smart NA, Downes D, van der Touw T, Hada S, Dieberg G, Pearson MJ, Wolden M, King N, Goodman SPJ (2024)

**Title**: The Effect of Exercise Training on Blood Lipids: A Systematic 
Review and Meta-analysis

**Journal**: Sports Medicine 55(1):67-78 (epub 2024 Sep 27)

**PMID**: 39331324

**Type**: Meta-analysis of 148 RCTs with 227 intervention groups, 
8,673 participants total. Trial Sequence Analysis confirms statistical 
futility.

**Used for**: Exercise effects on LDL (`intervention_category=exercise`)

**Rows in CSV**: 2 — `SMART_2024_aerobic_or_combined` (paper's -7.22 mg/dL 
pooled across AT and CT), `SMART_2024_resistance_only` (qualitative null 
finding per paper Section 3.5)

**Key data extracted**: Overall LDL pooled effect (-7.22 mg/dL, 95% CI 
-9.08 to -5.35). Modality breakdown: AT/CT significant, RT no effect.

**Methodology caveats**: Open access (CC-BY 4.0); 78% of studies had 
moderate-to-low quality (TESTEX <10); 78% had medication confound; high 
heterogeneity (I² > 75%); prediction interval crosses zero (27.9% of 
studies showed no LDL benefit).