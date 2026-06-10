# LDLtrack Model Design v1

Single-intervention Bayesian model. Takes a user's baseline LDL, one
intervention, and a dose, then outputs posterior predicted final LDL
with 95% credible interval.

---

## Model Structure

Bayesian dose-response model with random effects. Non-centered parameterization.

```
# Dose-response (dose is centered: dose_c = dose - mean_dose)
alpha ~ Normal(alpha_prior, alpha_sd)   # effect at mean dose
beta  ~ Normal(beta_prior,  beta_sd)    # change in effect per unit dose

# Between-study heterogeneity (residual after accounting for dose)
tau ~ HalfNormal(5)

# Study-level effects (non-centered)
theta_offset ~ Normal(0, 1, shape=n_studies)
theta_i = alpha + beta * dose_c_i + tau * theta_offset_i

# Likelihood
y_i ~ Normal(theta_i, se_i)

# Prediction for a new patient at a queried dose
offset_new  ~ Normal(0, 1)
theta_new   = alpha + beta * dose_query_c + tau * offset_new
ldl_final   = baseline_ldl * (1 + theta_new / 100)
```

Centering dose makes alpha = "effect at mean dose", reduces alpha-beta
correlation. Same motivation as non-centered parameterization.

Using theta_new (not mu) for prediction: includes both uncertainty in the
pooled estimate AND between-study heterogeneity tau. This gives an honest
interval for an individual — it does not shrink as more studies are added.

---

## Data Pipeline

1. Load `effect_sizes_raw.csv`
2. Filter to one intervention_category
3. Drop rows with missing ldl_change_value
4. Convert all units to percent:
   - percent: no change
   - mg_dL: ldl_change_pct = ldl_change_value / baseline_ldl * 100
     TODO (pre-statin): decide which baseline to use and where it comes from
   - mg_dL_per_kg: ldl_change_pct = ldl_change_value * body_weight_kg / baseline_ldl * 100
     TODO (pre-statin): body_weight_kg source not yet defined
   - mg_dL_per_g: ldl_change_pct = ldl_change_value * dose_g / baseline_ldl * 100
     TODO (pre-statin): dose_g source not yet defined
5. Compute SE from CI if ldl_change_se is missing:
   se = (ci_high - ci_low) / (2 * 1.96)
6. For rows still missing SE: assign conservative default (se = 3.0%)
7. Center dose: dose_c = dose_value - dose_value.mean()

---

## Prior Specification

| Parameter | Prior | Rationale |
|---|---|---|
| alpha | Normal(paper_mean_at_avg_dose, wide_sd) | Effect at mean dose |
| beta | Normal(0, 2) | Conservative; centered at 0 to let data determine direction |
| tau | HalfNormal(5) | Allows up to ~10% residual between-study spread |

Priors are set per intervention when the model is instantiated.

---

## Output

- `alpha` posterior: effect at mean dose, 95% CrI
- `beta` posterior: dose-response slope, 95% CrI
- `theta_new` posterior: predicted % effect at queried dose + tau uncertainty
- `ldl_final` posterior: baseline * (1 + theta_new/100), in mg/dL, 95% CrI

---

## Implementation Plan

1. `src/data_loader.py` — load, filter, unit-convert, SE-impute, center dose
2. **Smoke test** (~30 min): pooled model (no dose predictor) just to confirm
   pipeline runs end-to-end. Not committed as a milestone deliverable.
3. `src/model_v1.py` — dose-response PyMC model
4. `notebooks/phase2/milestone22_validation.ipynb` — run on plant sterols,
   validate posterior dose curve against Ras 2014 reported per-dose effects

---

## First Target: Plant Sterols (Ras 2014)

- 6 rows (dose bins: 0.6, 1.0, 1.5, 2.0, 2.5, 3.3 g/day)
- Unit: percent (no conversion needed)
- SE available for all rows (derived from CI)
- No on_top_of constraint
- Cleanest dose-response signal in the dataset: single paper, uniform
  population, monotone dose-response — ideal for learning dose predictor
  before tackling statin complexity

**Validation note**: linear dose assumption may underfit at the high end.
Plant sterol effect is saturation-type (cholesterol absorption inhibition
has a ceiling), so the 3.3 g/day point may be systematically overestimated
by a straight line. Check residuals at high dose. Fallback: log(dose) or
a saturation (Michaelis-Menten) function.

**Implementation gotcha**: when predicting at a user-queried dose,
center it using the *training set* mean_dose, not the query value itself.
`dose_query_c = dose_query - mean_dose_from_training_data`
