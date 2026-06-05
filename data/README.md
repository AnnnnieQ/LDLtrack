# Effect Sizes Database

Curated effect sizes from published RCTs and meta-analyses for the LDLtrack project.

## Schema (v1)

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
- Both pooled and by-type rows preserved for modeling flexibility in Milestone 2.2
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

## Source 5: Ras 2014 (Plant Sterols and Stanols)

**Citation**: Ras RT, Geleijnse JM, Trautwein EA. LDL-cholesterol-lowering 
effect of plant sterols and stanols across different dose ranges: a 
meta-analysis of randomised controlled studies. *Br J Nutr* 
2014;112(2):214-219. PMID: 24780090.

**Study design**: Meta-analysis of 124 RCT studies (201 study arms), 
~9,648 subjects total (estimated at avg 48 subjects/arm). Random-effects 
model weighted by inverse variance.

**Rows added**: 6 (one per dose bin: <1.0, 1.0-1.5, 1.5-2.0, 2.0-2.5, 
2.5-3.0, 3.0-4.0 g/d)

**Why 6 rows (dose-response structure)**:
- Paper's core contribution is the dose-response curve, not a single 
  pooled effect estimate
- Each dose bin provides an independent effect + CI, supporting Bayesian 
  dose-response modeling in Milestone 2.2
- 6 rows mirror the paper's Table 1 structure exactly

**Why combined (sterols + stanols pooled), not separated**:
- Paper's main conclusion: sterols and stanols have comparable 
  dose-response relationships (rejects earlier Musa-Veloso 2011 claim 
  that stanols are more effective)
- Low-dose stanol data is statistically weak (n=1 arm at <1.0 g/d, CI 
  crosses zero)
- Users don't distinguish sterols vs stanols in practice (most 
  PS-enriched products don't specify on label)

**Dose range decision**: Used dose bins ≤4 g/d only. Paper explicitly 
excludes >4 g/d data from pooling (scarce, scattered across 5.8-9.0 g/d).
Tool should warn users if input dose exceeds 4 g/d.

**Effect sizes** (% LDL change vs placebo, by dose bin):

| Bin (g/d) | Avg dose | Combined effect | 95% CI |
|-----------|----------|-----------------|--------|
| <1.0 | 0.6 | -5.7% | -7.1, -4.4 |
| 1.0-1.5 | 1.1 | -6.4% | -8.2, -4.6 |
| 1.5-2.0 | 1.7 | -7.6% | -8.4, -6.8 |
| 2.0-2.5 | 2.1 | -8.4% | -9.2, -7.6 |
| 2.5-3.0 | 2.6 | -10.3% | -11.8, -8.9 |
| 3.0-4.0 | 3.3 | -12.4% | -13.6, -11.2 |

**`on_top_of` decision**: NA. Studies compare PS-enriched food vs placebo 
food (e.g., margarine with PS vs margarine without). No specific 
background diet required.

**`n` field convention**: Subjects estimated at 48/arm (paper-reported 
average). Paper's Table 1 reports study arm counts (24/13/55/60/17/27), 
not bin-level subject counts. This is an estimate, not paper-reported value.
See Known Schema Issues below for broader `n` field semantic problem.

**Population caveat**: Mixed normocholesterolemic to mildly 
hypercholesterolemic adults. Paper does not stratify baseline LDL by 
dose bin (`baseline_ldl_mg_dl` = NA for all 6 rows). Paper discussion 
notes baseline LDL is an effect modifier — effect may be larger in 
users with higher baseline LDL.

**Real-world adherence caveat**: Paper notes actual users of PS-enriched 
foods consume on average ~1 g/d (well below 2-3 g/d recommendation). 
Tool should set realistic expectations: while data supports -12% at 
3 g/d, sustained 3 g/d intake is uncommon.

**Conflict of interest note**: Two authors (Ras, Trautwein) employed by 
Unilever, which markets PS-enriched products. Third author (Geleijnse) 
has no conflict. Findings are consistent with prior independent 
meta-analyses (Demonty 2009, Musa-Veloso 2011) on overall dose-response.

## Source 6: Smart 2024 (Exercise Training)

**Citation**: Smart NA, Downes D, van der Touw T, Hada S, Dieberg G, 
Pearson MJ, Wolden M, King N, Goodman SPJ. The Effect of Exercise 
Training on Blood Lipids: A Systematic Review and Meta-analysis. 
*Sports Medicine* 2025;55(1):67-78 (epub 2024 Sep 27). PMID: 39331324.

**Study design**: Meta-analysis of 148 RCTs with 227 intervention groups, 
8,673 participants total (5,273 exercise / 3,400 sedentary control). For 
LDL analysis specifically: 178 intervention groups, 4,143 exercise + 
2,724 control. Random-effects model with Trial Sequence Analysis (TSA) 
confirming statistical futility for all five lipid outcomes (sufficient 
information size reached).

**Rows added**: 2

**Why 2 rows (modality matters)**:
- Paper reports overall pooled LDL effect of -7.22 mg/dL (95% CI -9.08, 
  -5.35) across all 178 intervention groups
- However, paper Section 3.5 and Figure 7 explicitly show this pooled 
  effect masks important modality differences:
  - AT (aerobic, 164 groups, 92% of pooled): significantly reduces LDL
  - CT (combined AT+RT, 31 groups): largest LDL reduction, significant
  - RT (resistance only, 32 groups): NO LDL effect (only HDL benefit)
- Paper does NOT provide numeric values + CIs separately for AT/CT/RT 
  in LDL — only visualized in Figure 7 bar chart
- Therefore: 2 rows reflect what paper actually reports in numeric form:
  - Row 1: aerobic_or_combined_AT_CT — uses paper's overall -7.22 figure
    (acknowledging this is dominated by AT at 92% weight, applies only to 
    users selecting aerobic or combined exercise)
  - Row 2: resistance_only — qualitative null finding (effect = 0, no CI), 
    documents paper's text claim that RT alone does not lower LDL

**Why not separate AT vs CT into different rows**: Paper does not provide 
numeric CIs for AT-only or CT-only LDL effects. Estimating from Figure 7 
bar chart would violate the data traceability principle (every number 
must be traceable to a paper's explicit numeric report, not inferred from 
visualizations).

**Unit decision**: `mg_dL` (absolute mean difference). Paper uses 
mg/dL as primary unit (also reports mmol/L). Unlike Ras 2014 (% change) 
or Brown 1999 (per-gram), Smart 2024 reports cross-trial pooled absolute 
effect because trials used widely varying exercise doses/durations and 
% change normalization across trials isn't appropriate.

**Effect size**:

| Row | Modality | LDL change | 95% CI |
|-----|----------|-----------|--------|
| Aerobic or Combined | AT or CT | -7.22 mg/dL | -9.08, -5.35 |
| Resistance only | RT alone | 0 mg/dL (null) | N/A (paper text only) |

**`on_top_of` decision**: NA. Paper notes 78% of studies had unknown or 
mixed lipid-lowering medication use, which is a confounding limitation. 
Effect estimates are NOT explicitly "on top of statin" — they represent 
exercise vs no exercise, with medication status mixed/uncontrolled.

**Population caveat**: Adults excluded for CVD, cancer, spinal cord 
injury, HIV, pregnancy. Mixed BMI/age. Paper does not stratify by 
baseline LDL — `baseline_ldl_mg_dl` is NA. Effect may differ for 
hyperlipidemic users.

**Prediction interval caveat**: Paper's 95% prediction interval for LDL 
is -23.54 to +9.10 mg/dL, meaning 27.9% of individual studies showed 
NO benefit from exercise on LDL. Tool should communicate this 
heterogeneity — individual user response is highly variable.

**Clinical context (from paper Section 4.7)**: Exercise-induced LDL 
reduction of 7.22 mg/dL corresponds to approximately 4-5% reduction in 
cardiovascular atherosclerotic event risk (based on Mach et al. 2020 
ESC/EAS Guidelines: every 38.5 mg/dL LDL reduction = 21-25% CVD risk 
reduction). Far below the 50% LDL reduction target for statin therapy. 
Whether exercise + statin effects are additive is an open question per 
paper itself (Section 4.7).

**Methodology strengths**:
- Trial Sequence Analysis confirms statistical futility (no more trials 
  needed to confirm direction of effect)
- Random-effects model
- Pre-registered protocol (OSF)
- Most comprehensive exercise + lipids meta-analysis to date

**Methodology weaknesses**:
- 78% of included trials had unknown or mixed lipid-lowering medication 
  status, confounding the "exercise effect" estimate (cannot cleanly 
  separate exercise contribution from concurrent statin use)
- Most trials short duration (typically 12-26 weeks); long-term sustained 
  exercise effects on LDL not well characterized
- Substantial heterogeneity across trials in exercise dose, intensity, 
  duration, and modality limits precision for any specific prescription
- Wide 95% prediction interval (-23.54 to +9.10 mg/dL) indicates ~28% of 
  individual studies showed no LDL benefit — pooled mean obscures 
  responder/non-responder variability

## Source 7: Cannon 2015 (IMPROVE-IT — Ezetimibe Added to Statin)

**Citation**: Cannon CP, Blazing MA, Giugliano RP, et al. Ezetimibe Added 
to Statin Therapy after Acute Coronary Syndromes. *New England Journal of 
Medicine* 2015;372(25):2387-2397. PMID: 26039521.

**Trial name**: IMPROVE-IT (IMProved Reduction of Outcomes: Vytorin 
Efficacy International Trial)

**Study design**: Single large RCT, double-blind, placebo-controlled. 
N=18,144 patients post-ACS (within 10 days of acute coronary syndrome), 
randomized 1:1 to simvastatin 40mg + ezetimibe 10mg vs simvastatin 40mg + 
placebo. Median 6-year follow-up. Primary endpoint: composite of CV death, 
nonfatal MI, unstable angina requiring rehospitalization, coronary 
revascularization (≥30 days post-randomization), or nonfatal stroke.

**Rows added**: 1

**Why 1 row**: Single RCT, single intervention (ezetimibe 10mg), single 
comparison (vs placebo on top of identical simvastatin background). No 
subgroup analysis needed for MVP — paper reports consistent benefit 
across nearly all prespecified subgroups (Fig. S2).

**Effect size decision (-24% over `percent` unit)**:
- Paper reports three related LDL difference figures:
  - 1-year mean LDL: 69.9 (statin) vs 53.2 (statin+ezetimibe) = 
    -16.7 mg/dL absolute, **~24% relative on top of statin baseline**
  - Time-weighted 6-year average: 69.5 vs 53.7 = -15.8 mg/dL
  - Imputed difference (CTT methodology): 12.8 mg/dL
- Chose -24% (percent) as the headline figure because:
  - Paper Discussion uses this as primary characterization
  - `percent` unit aligns with VOYAGER, Chiavaroli, Ras 2014 rows
  - Cross-baseline applicable (users on statin with LDL 70 or 80 get 
    same -24%)

**`baseline_ldl_mg_dl=69.5` decision**: This is the statin-alone group's 
time-weighted average LDL, NOT the randomization-baseline LDL (which was 
93.8 mg/dL pre-statin-titration). Rationale: ezetimibe's -24% effect is 
measured against "already-on-statin LDL", so for user-facing prediction, 
the relevant baseline is "LDL while on statin". Users entering "I'm on 
statin with LDL 70 considering adding ezetimibe" will get correct 
prediction: 70 × 0.76 = 53 mg/dL.

**`on_top_of=simvastatin_40mg_moderate_intensity`**: First non-NA value 
for this field in the dataset. This row should not be applied as 
standalone effect — only as additive to a statin background. Note: paper 
used simvastatin 40mg (moderate intensity); ezetimibe + high-intensity 
statin combination has NOT been studied in equivalent RCT, so 
extrapolation beyond moderate statin background carries uncertainty.

**CI/SE not available**: Paper reports LDL difference with P<0.001 but no 
explicit CI for the LDL change itself. CIs reported (0.89-0.99) are for 
the primary clinical endpoint HR (0.936), not for LDL change. Therefore 
`ldl_change_se`, `ci_low`, `ci_high` are all NA. This is the first row 
with this CI pattern — see Known Schema Issues for handling guidance.

**Clinical context (CVD risk reduction)**:
- 7-year primary endpoint event rate: 34.7% (statin) vs 32.7% 
  (statin+ezetimibe), absolute risk reduction 2.0 percentage points
- HR 0.936 (95% CI 0.89-0.99), P=0.016
- NNT = 50 (one CV event prevented per 50 patients treated for 7 years)
- Translates to ~6.4% relative reduction in major vascular events
- Per Mach 2020 formula (every 38.5 mg/dL LDL reduction → 21-25% CVD 
  risk reduction), expected reduction would be ~9.4%; observed 6.4% is 
  in the expected range

**Landmark significance**: IMPROVE-IT was the first large RCT to:
1. Prove a non-statin LDL-lowering agent reduces hard CVD outcomes
2. Demonstrate "lower is better" extends below LDL 70 mg/dL
3. Influence ACC/AHA 2018 and ESC/EAS 2019 guideline shifts toward 
   stricter LDL targets (<70 for high-risk, <55 for very-high-risk)

**Population caveat**: Trial enrolled post-ACS patients only (secondary 
prevention, high CVD risk). Effect may not generalize to:
- Primary prevention populations (no prior ASCVD)
- Users not on statin background
- Users on high-intensity statin (paper used moderate-intensity 
  simvastatin 40mg)

**Safety**: No significant differences vs statin alone for muscle, 
gallbladder, hepatic adverse effects, or cancer. Ezetimibe is well-
tolerated when added to statin. Hemorrhagic stroke nonsignificantly 
higher with ezetimibe (0.8% vs 0.6%, P=0.11) — small absolute numbers.

**Funding disclosure**: Trial funded by Merck (ezetimibe manufacturer). 
Independent data analysis by DCRI. Results published in NEJM with 
extensive peer review. Findings have been independently replicated and 
incorporated into multiple international guidelines.

## Source 8: Sabatine 2017 (FOURIER — Evolocumab PCSK9i Added to Statin)

**Citation**: Sabatine MS, Giugliano RP, Keech AC, et al. Evolocumab and 
Clinical Outcomes in Patients with Cardiovascular Disease. *New England 
Journal of Medicine* 2017;376(18):1713-22. PMID: 28304224.

**Trial name**: FOURIER (Further Cardiovascular Outcomes Research with 
PCSK9 Inhibition in Subjects with Elevated Risk)

**Study design**: Single RCT, double-blind, placebo-controlled, 
multinational (1242 sites, 49 countries). N = 27,564 (evolocumab arm 
13,784; placebo arm 13,780). Median follow-up 2.2 years.

**Rows added**: 1

**Why 1 row**: Single RCT, single intervention class, single comparison 
(evolocumab vs placebo on top of statin). Paper reports benefit 
consistent across both dosing regimens (140 mg q2wk and 420 mg monthly) 
and across baseline LDL quartiles — single row sufficient for MVP.

**Population**: Established ASCVD (MI 80.9%, nonhemorrhagic stroke 19.5%, 
PAD 13.5%; overlap allowed). Age 40-85 (mean 62.5). Required to be on 
optimized lipid-lowering therapy — preferably high-intensity statin, 
minimum atorvastatin 20 mg or equivalent, ± ezetimibe. Eligibility: 
fasting LDL ≥70 mg/dL OR non-HDL ≥100 mg/dL on statin. 69.5% on high-
intensity statin, 30.2% moderate-intensity, 5.2% on ezetimibe at baseline.

**Intervention**: Evolocumab 140 mg SC every 2 weeks OR 420 mg SC monthly 
(patient preference). Both regimens captured in single row.

**Key numbers**:
- `ldl_change_value = -59` (percent): LSM percentage reduction at 48 
  weeks vs placebo (paper headline figure, 95% CI 58-60).
- `baseline_ldl_mg_dl = 92`: Median LDL at randomization, on statin, 
  pre-evolocumab (IQR 80-109). NOT a time-weighted on-treatment value 
  — this is the pre-randomization median while patients were already 
  on statin therapy.
- `ci_low = -60, ci_high = -58`: Paper reports 95% CI for LSM percentage 
  reduction (different from Cannon 2015, which reports P-value but no 
  LDL CI).
- `n = 13784`: Evolocumab arm size.

**Effect timing caveat**: The -59% figure is a 48-week landmark, NOT a 
time-weighted average. Figure 1 shows LDL reduction peaked at ~61% 
(weeks 12-24), held ~58-59% through week 72, then mildly attenuated to 
54% by week 168. Paper text describes the effect as "sustained without 
evidence of attenuation," but the over-time data in Figure 1 shows 
modest drift. Modeling implication: this row's effect represents peak-
to-mid-trial reduction; long-term real-world effect likely 2-4 
percentage points lower in absolute terms.

**Baseline timing note (cross-row consistency)**: This row's 
`baseline_ldl_mg_dl = 92` is the randomization baseline (pre-
intervention, on statin). Cannon 2015's `baseline_ldl_mg_dl = 69.5` is 
a 1-year on-treatment value (statin-alone group's LDL after a year of 
simvastatin). Both rows have `on_top_of = ...statin...`, but the 
baseline semantic differs. See Known Schema Issue #6 (effect/baseline 
timing).

**CVD outcomes (not in CSV, documented for context)**:
- Primary composite endpoint (CV death, MI, stroke, unstable angina 
  hospitalization, coronary revascularization): HR 0.85 (95% CI 0.79-
  0.92), P<0.001.
- Key secondary (CV death, MI, stroke): HR 0.80 (95% CI 0.73-0.88), 
  P<0.001.
- No effect on cardiovascular mortality (HR 1.05, 95% CI 0.88-1.25) or 
  all-cause mortality (HR 1.04, 95% CI 0.91-1.19).
- NNT = 74 over 2.2 years to prevent one CV death, MI, or stroke.

**Safety**: No significant difference in overall adverse events, serious 
adverse events, new-onset diabetes (HR 1.05, 95% CI 0.94-1.17), 
neurocognitive events, or muscle-related events. Only nominally 
significant difference: injection-site reactions (2.1% vs 1.6%, 
P<0.001), mostly mild, <0.1% discontinuation.

**Access caveats (not in CSV — potential Phase 3 schema addition)**: 
Evolocumab is ~$5,000-7,000/year US, requires prior authorization, and 
is SC injection. This contrasts with ezetimibe (~$30/month generic, 
oral). User-facing tool should eventually reflect this access tier 
difference.

**Funding/COI**: Funded by Amgen (evolocumab manufacturer). Sponsor 
collaborated on design and held raw database; TIMI Study Group conducted 
analyses independently.

---

## Known Schema Issues (to revisit in Phase 3)

### Issue 1: `population` column inconsistency

Current granularity varies across rows:
- VOYAGER rows use short labels (e.g., `ASCVD`, `diabetes`)
- Hasan/Chiavaroli/Brown rows use long composite strings 
  (e.g., `hyperlipidemic_adults_no_DM_no_CVD`)
- Long strings encode multiple dimensions in one field (lipid status + 
  comorbidities + baseline values), violating one-fact-per-column principle
- Some information is redundant with `baseline_ldl_mg_dl` column

**Planned resolution (Phase 3)**: Split `population` into orthogonal columns:
`population_category`, `has_dm`, `has_cvd`, `baseline_bmi`, etc. 
Decision deferred until all Phase 1 papers extracted to see full schema needs.

### Issue 2: `intervention_subtype` semantics

Currently used for both mechanism classification (e.g., `via_diet_exercise`) 
and chemical classification (e.g., `soluble_fiber_beta_glucan`). May need 
to split into two fields, or accept as a flexible sub-classification 
dimension. Revisit Phase 3.

### Issue 3: `n` column semantic inconsistency

Currently the `n` field contains five different meanings across rows:

| Paper | Semantic | Example values |
|-------|----------|----------------|
| VOYAGER | patient exposures (IPD level) | 1147, 1726, 2423 |
| Hasan 2020 | subjects in mechanism subset | 2434, 16333, 377 |
| Chiavaroli 2018 | subjects in trial sub-analysis | 94, 345 |
| Brown 1999 | subjects in dose range | 1151, 867, 151, 117 |
| Ras 2014 | estimated subjects (arms × avg 48) | 1152, 624, 2640, ... |
| Cannon 2015, Sabatine 2017 | arm size (one trial group) | 9067, 13784 |

Mixing these in one field is risky for Bayesian likelihood weighting 
(patient exposures ≠ unique subjects ≠ estimated subjects). Milestone 2.2
modeling will use SE/CI for likelihood rather than n directly, 
sidestepping this issue for MVP.

**Planned resolution (Phase 3)**: Split `n` into three orthogonal columns:
- `n_subjects` — unique participant count (single RCTs, meta-analysis subsets)
- `n_arms` or `n_strata` — study arms in meta-analyses
- `n_exposures` — IPD-level exposures (VOYAGER-style data)

Each row populates only the relevant column(s), others NA. This preserves 
all source information without conflating semantics.

### Issue 4: `ldl_change_unit` heterogeneity (expected, documented)

Effect sizes are recorded in 4 different units across rows:

| Unit | Used by | Meaning |
|------|---------|---------|
| `percent` | VOYAGER, Chiavaroli, Ras 2014, Cannon 2015, Sabatine 2017 | % change in LDL from baseline |
| `mg_dL` | Smart 2024 | Absolute mg/dL change (mean difference) |
| `mg_dL_per_kg` | Hasan 2020 | mg/dL change per 1 kg weight loss |
| `mg_dL_per_g` | Brown 1999 | mg/dL change per 1 g soluble fiber |

This heterogeneity reflects real differences in how source papers report 
effects — it is not a schema bug. Each paper uses its most natural unit.

**Milestone 2.2 modeling implications**:
1. Bayesian likelihood must be unit-aware. Rows with different units 
   should NOT be pooled in the same likelihood term.
2. User-facing output should convert all effects to a single unit 
   (recommended: absolute mg/dL) using:
   - `percent` → `mg_dL`: multiply by user's baseline_ldl / 100
   - `mg_dL_per_X` → `mg_dL`: multiply by user input X
3. Combining multiple interventions is NOT additive in absolute mg/dL.
   Use multiplicative model on % change scale:
   final_LDL = baseline × (1 - effect_1_pct) × (1 - effect_2_pct) × ...
4. `baseline_ldl_mg_dl` column is essential for percent → absolute 
   conversion at prediction time.

### Issue 5: Single-RCT CI reporting variability (updated after Sabatine 2017)

Single-RCT papers vary in whether they report a confidence interval on 
the LDL change itself (separate from clinical endpoint CIs):
- Cannon 2015 (IMPROVE-IT): Reports P-value for LDL change but NO LDL 
  CI; only HR CI for clinical endpoints. → `ci_low = NA, ci_high = NA`
- Sabatine 2017 (FOURIER): Reports both LSM % reduction with 95% CI AND 
  clinical endpoint HRs with CIs. → `ci_low = -60, ci_high = -58`

Not a universal pattern; depends on reporting choices of individual 
trials. Milestone 2.2 modeling implication: rows with missing LDL CI need SE 
imputation strategy (from P-value + n, weakly informative prior, or 
exclusion from likelihood).

This is distinct from meta-analyses (Brown, Ras, Chiavaroli, Smart) 
which typically DO report LDL-specific CIs.

### Issue 6: Effect/baseline timing inconsistency (NEW — flagged with Sabatine 2017)

The `ldl_change_value` and `baseline_ldl_mg_dl` fields collapse different 
timing semantics across rows:

`ldl_change_value` timing:
- VOYAGER: end-of-study mean change (6-week trials)
- Cannon 2015: time-weighted average over follow-up
- Sabatine 2017: 48-week landmark (LSM), not time-weighted
- Smart 2024, Brown, Ras: meta-analytic pooled estimates (study-level effects)
- Hasan 2020: per-unit (kg weight loss) coefficient
- Chiavaroli, others: end-of-intervention mean change

`baseline_ldl_mg_dl` timing:
- Cannon 2015 (69.5): 1-year on-treatment LDL of statin-alone arm
- Sabatine 2017 (92): randomization baseline on statin, pre-evolocumab
- VOYAGER: NA (not reported, pooled across baselines)
- Hasan, Chiavaroli, Brown: trial-level mean baseline

**Modeling implication**: For interventions added on top of statin, the 
row's "baseline" is ambiguous about whether it represents user's 
*current on-statin LDL* (Cannon-style) or *LDL before any statin therapy* 
(not represented in current rows). At prediction time, user input "my 
current LDL on statin is X" maps differently depending on which row's 
semantic is used.

**Planned resolution (Phase 3)**: Add `effect_timing` and `baseline_timing` 
fields.
- `effect_timing`: end_of_study / 48wk_landmark / 1yr_landmark / 
  time_weighted_avg / meta_pooled / per_unit / NA
- `baseline_timing`: pre_treatment / on_treatment_steady_state / 
  randomization_on_statin / NA

---

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
**Phase 3 expansion**: Add time horizon selector and progressive effect curves.

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