import numpy as np
from src.data_loader import load_intervention, load_single_row
from src.model_v1 import build_model, sample_model, predict, combine

STATIN_OPTIONS = {
    'atv40': {'intervention_specific': 'atorvastatin', 'dose_value': 40},
    'atv80': {'intervention_specific': 'atorvastatin', 'dose_value': 80},
    'rsv20': {'intervention_specific': 'rosuvastatin', 'dose_value': 20},
    'rsv40': {'intervention_specific': 'rosuvastatin', 'dose_value': 40},
}

print('Loading models...')
models = {}
for (label, filters), seed in zip(STATIN_OPTIONS.items(), [1, 2, 3, 4]):
    data = load_single_row('statin', {**filters, 'population': 'all_patients'})
    model = build_model(data, alpha_mu=-50, alpha_sd=5, mode='intercept_only')
    models[label] = {'idata': sample_model(model, random_seed=seed, draws=2000), 'data': data}

data_st = load_intervention('plant_sterols')
models['sterols'] = {
    'idata': sample_model(build_model(data_st, alpha_mu=-8.0, alpha_sd=2.5, mode='dose_response'), random_seed=5, draws=2000),
    'data': data_st,
}

data_ex = load_single_row('exercise', {'intervention_subtype': 'aerobic_or_combined_AT_CT'})
models['ex'] = {
    'idata': sample_model(build_model(data_ex, alpha_mu=-7.22, alpha_sd=2, mode='intercept_only'), random_seed=6, draws=2000),
    'data': data_ex,
}
print('Models ready.\n')


def pp(key, dose=None, baseline=150):
    m = models[key]
    return predict(m['idata'], m['data'], baseline_ldl=baseline, dose_query=dose)


def show(label, preds, baseline):
    r = combine(baseline, preds)
    f = r['ldl_final']
    eff = r['total_effect'].mean()
    neg = (f < 0).any()
    print(f'  {label}')
    print(f'    final={f.mean():.1f}  CrI=[{np.percentile(f,2.5):.1f}, {np.percentile(f,97.5):.1f}]'
          f'  effect={eff:.1f}%  negative={neg}')


print('=== A: selection coverage ===')
show('only atv80            (exp ~73.5)',  [pp('atv80')], 150)
show('only sterols 2.0      (exp ~137.3)', [pp('sterols', 2.0)], 150)
show('only exercise         (exp ~142.8)', [pp('ex')], 150)
show('statin + sterols',                   [pp('atv80'), pp('sterols', 2.0)], 150)
show('statin + exercise',                  [pp('atv80'), pp('ex')], 150)
show('sterols + exercise',                 [pp('sterols', 2.0), pp('ex')], 150)
show('all three',                          [pp('atv80'), pp('sterols', 2.0), pp('ex')], 150)

print('\n=== B: baseline extremes ===')
show('baseline 60, all three (no negatives)', [pp('atv80', baseline=60), pp('sterols', 2.0, 60), pp('ex', baseline=60)], 60)
show('baseline 280, atv80   (exp ~137.2)',     [pp('atv80', baseline=280)], 280)

print('\n=== C: sterols dose extremes ===')
show('sterols 0.6 g/day     (exp effect ~-5%)',  [pp('sterols', 0.6)], 150)
show('sterols 3.3 g/day     (exp effect ~-11%)', [pp('sterols', 3.3)], 150)
e06 = pp('sterols', 0.6)['theta_new'].mean()
e33 = pp('sterols', 3.3)['theta_new'].mean()
print(f'  dose effects: 0.6g={e06:.1f}%  3.3g={e33:.1f}%  (monotone: {e06 > e33})')
