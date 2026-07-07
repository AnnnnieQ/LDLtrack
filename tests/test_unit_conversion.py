"""Tests for user-dose unit conversion in predict()."""

import sys
from pathlib import Path

import arviz as az
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.model_v1 import predict


def _idata_with_alpha(alpha_value: float):
    """Create a tiny posterior with a fixed alpha sample."""
    return az.from_dict(posterior={"alpha": np.array([[alpha_value]])})


def test_mg_dl_per_g_uses_unit_dose_then_baseline_conversion():
    idata = _idata_with_alpha(-2.20)
    data = {"unit": "mg_dL_per_g"}

    result = predict(idata, data, baseline_ldl=150, unit_dose=5)

    assert np.isclose(result["theta_new"][0], -7.3333333333)
    assert np.isclose(result["ldl_final"][0], 139.0)


def test_mg_dl_per_kg_uses_unit_dose_then_baseline_conversion():
    idata = _idata_with_alpha(-1.28)
    data = {"unit": "mg_dL_per_kg"}

    result = predict(idata, data, baseline_ldl=150, unit_dose=5)

    assert np.isclose(result["theta_new"][0], -4.2666666667)
    assert np.isclose(result["ldl_final"][0], 143.6)


def test_per_unit_effect_requires_unit_dose():
    idata = _idata_with_alpha(-1.28)

    for unit in ["mg_dL_per_kg", "mg_dL_per_g"]:
        try:
            predict(idata, {"unit": unit}, baseline_ldl=150)
        except ValueError:
            continue
        raise AssertionError(f"Expected ValueError for unit={unit!r}")


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
