"""Tests for src/cvd_risk.cvd_rrr (fixed and sampled CTT effect size)."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.cvd_risk import cvd_rrr, MG_DL_PER_MMOL, RR_PER_MMOL


def _synthetic_ldl_posterior(n=8000, baseline=150.0, mean_final=90.0, sd=8.0, seed=1):
    """A fake LDL-reduction posterior (no MCMC) for interval-width comparisons."""
    rng = np.random.default_rng(seed)
    return rng.normal(mean_final, sd, n)


def _ci_width(x):
    return np.percentile(x, 97.5) - np.percentile(x, 2.5)


def test_known_point_estimate():
    """150 -> 69 mg/dL = 81 mg/dL = 2.095 mmol/L -> RR 0.78^2.095 ~ 0.594."""
    out = cvd_rrr(150.0, 69.0)

    delta_mmol = (150.0 - 69.0) / MG_DL_PER_MMOL
    expected_rr = RR_PER_MMOL ** delta_mmol      # ~0.5943

    assert np.isclose(out["rr"], expected_rr)
    assert np.isclose(out["rrr"], 1.0 - expected_rr)
    # Sanity: should land near the worked example of ~40.6% RRR.
    assert np.isclose(out["rrr"], 0.406, atol=0.005)


def test_zero_reduction_gives_zero_rrr():
    """No LDL change -> RR = 1, RRR = 0."""
    out = cvd_rrr(150.0, 150.0)
    assert np.isclose(out["rr"], 1.0)
    assert np.isclose(out["rrr"], 0.0)


def test_ldl_increase_gives_negative_rrr():
    """LDL rises above baseline -> RR > 1, RRR < 0 (increased risk)."""
    out = cvd_rrr(150.0, 170.0)
    assert out["rr"] > 1.0
    assert out["rrr"] < 0.0


def test_per_sample_array_input():
    """Array input (posterior samples) maps elementwise, shape preserved."""
    ldl_final = np.array([69.0, 150.0, 170.0])
    out = cvd_rrr(150.0, ldl_final)

    assert out["rr"].shape == ldl_final.shape
    assert out["rrr"].shape == ldl_final.shape
    # First reduces (RRR > 0), second flat (RRR = 0), third rises (RRR < 0).
    assert out["rrr"][0] > 0.0
    assert np.isclose(out["rrr"][1], 0.0)
    assert out["rrr"][2] < 0.0


def test_one_mmol_matches_ctt_anchor():
    """A reduction of exactly 1 mmol/L should give RR = RR_PER_MMOL (0.78)."""
    ldl_final = 150.0 - MG_DL_PER_MMOL          # drop exactly 1 mmol/L
    out = cvd_rrr(150.0, ldl_final)
    assert np.isclose(out["rr"], RR_PER_MMOL)
    assert np.isclose(out["rrr"], 1.0 - RR_PER_MMOL)


def test_sample_effect_returns_array_shape():
    """sample_effect=True over an array returns same-shape arrays."""
    ldl_final = _synthetic_ldl_posterior()
    out = cvd_rrr(150.0, ldl_final, sample_effect=True, random_seed=0)
    assert out["rr"].shape == ldl_final.shape
    assert out["rrr"].shape == ldl_final.shape


def test_sample_effect_mean_close_to_fixed():
    """Sampling the effect size is centered on 0.78, so the RRR mean barely moves."""
    ldl_final = _synthetic_ldl_posterior()
    fixed = cvd_rrr(150.0, ldl_final)
    sampled = cvd_rrr(150.0, ldl_final, sample_effect=True, random_seed=0)
    assert np.isclose(fixed["rrr"].mean(), sampled["rrr"].mean(), atol=0.01)


def test_sample_effect_widens_interval():
    """Adding the CTT layer widens the RRR interval — but only a little (SE~0.013)."""
    ldl_final = _synthetic_ldl_posterior()
    fixed = cvd_rrr(150.0, ldl_final)
    sampled = cvd_rrr(150.0, ldl_final, sample_effect=True, random_seed=0)
    w_fixed = _ci_width(fixed["rrr"])
    w_sampled = _ci_width(sampled["rrr"])
    assert w_sampled > w_fixed
    # Second layer is small: should not blow the interval up (sanity guard).
    assert w_sampled < 2.0 * w_fixed


def test_scalar_sample_effect_requires_n_samples():
    """Scalar ldl_final + sample_effect=True without n_samples must raise."""
    try:
        cvd_rrr(150.0, 90.0, sample_effect=True)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError when n_samples is missing")
    # With n_samples it works and returns that many draws.
    out = cvd_rrr(150.0, 90.0, sample_effect=True, n_samples=4000, random_seed=0)
    assert out["rrr"].shape == (4000,)


if __name__ == "__main__":
    # Runs without pytest: execute every test_* function and report.
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
