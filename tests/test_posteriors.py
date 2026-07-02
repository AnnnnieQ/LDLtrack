"""Tests for pre-sampled posterior artifacts used by the deployed app."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app_models import MODEL_SPECS, load_saved_models, posterior_path
from src.model_v1 import combine, predict


def test_all_posterior_files_exist():
    """Deployment depends on committed NetCDF posterior files."""
    for spec in MODEL_SPECS.values():
        path = posterior_path(spec)
        assert path.exists(), f"missing posterior file: {path}"


def test_saved_posteriors_load_with_expected_variables():
    """Saved InferenceData files should load and retain expected posterior vars."""
    models = load_saved_models()

    assert set(models) == set(MODEL_SPECS)

    for label, model in models.items():
        posterior = model["idata"].posterior
        assert "alpha" in posterior
        if MODEL_SPECS[label]["mode"] == "dose_response":
            assert "beta" in posterior


def test_saved_posterior_prediction_matches_expected_combo():
    """Round-trip NetCDF posterior should preserve app-level predictions."""
    models = load_saved_models()
    baseline_ldl = 150.0

    preds = [
        predict(
            models["Atorvastatin 40 mg"]["idata"],
            models["Atorvastatin 40 mg"]["data"],
            baseline_ldl=baseline_ldl,
        ),
        predict(
            models["plant_sterols"]["idata"],
            models["plant_sterols"]["data"],
            baseline_ldl=baseline_ldl,
            dose_query=2.0,
        ),
        predict(
            models["exercise"]["idata"],
            models["exercise"]["data"],
            baseline_ldl=baseline_ldl,
        ),
    ]
    result = combine(baseline_ldl, preds)

    # Expected from local MCMC before serialization: ~69 mg/dL.
    assert np.isclose(result["ldl_final"].mean(), 69.1, atol=0.5)


if __name__ == "__main__":
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
