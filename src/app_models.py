from pathlib import Path

import arviz as az

from src.data_loader import load_intervention, load_single_row
from src.model_v1 import build_model, sample_model


POSTERIOR_DIR = Path(__file__).resolve().parent.parent / "artifacts" / "posteriors"

STATIN_OPTIONS = {
    "Atorvastatin 40 mg": {
        "intervention_specific": "atorvastatin",
        "dose_value": 40,
    },
    "Atorvastatin 80 mg": {
        "intervention_specific": "atorvastatin",
        "dose_value": 80,
    },
    "Rosuvastatin 20 mg": {
        "intervention_specific": "rosuvastatin",
        "dose_value": 20,
    },
    "Rosuvastatin 40 mg": {
        "intervention_specific": "rosuvastatin",
        "dose_value": 40,
    },
}

MODEL_SPECS = {
    "Atorvastatin 40 mg": {
        "slug": "statin_atorvastatin_40mg",
        "kind": "single_row",
        "category": "statin",
        "filters": {**STATIN_OPTIONS["Atorvastatin 40 mg"], "population": "all_patients"},
        "alpha_mu": -50,
        "alpha_sd": 5,
        "mode": "intercept_only",
        "seed": 1,
    },
    "Atorvastatin 80 mg": {
        "slug": "statin_atorvastatin_80mg",
        "kind": "single_row",
        "category": "statin",
        "filters": {**STATIN_OPTIONS["Atorvastatin 80 mg"], "population": "all_patients"},
        "alpha_mu": -50,
        "alpha_sd": 5,
        "mode": "intercept_only",
        "seed": 2,
    },
    "Rosuvastatin 20 mg": {
        "slug": "statin_rosuvastatin_20mg",
        "kind": "single_row",
        "category": "statin",
        "filters": {**STATIN_OPTIONS["Rosuvastatin 20 mg"], "population": "all_patients"},
        "alpha_mu": -50,
        "alpha_sd": 5,
        "mode": "intercept_only",
        "seed": 3,
    },
    "Rosuvastatin 40 mg": {
        "slug": "statin_rosuvastatin_40mg",
        "kind": "single_row",
        "category": "statin",
        "filters": {**STATIN_OPTIONS["Rosuvastatin 40 mg"], "population": "all_patients"},
        "alpha_mu": -50,
        "alpha_sd": 5,
        "mode": "intercept_only",
        "seed": 4,
    },
    "plant_sterols": {
        "slug": "plant_sterols_dose_response",
        "kind": "intervention",
        "category": "plant_sterols",
        "alpha_mu": -8.0,
        "alpha_sd": 2.5,
        "mode": "dose_response",
        "seed": 5,
    },
    "exercise": {
        "slug": "exercise_aerobic_combined",
        "kind": "single_row",
        "category": "exercise",
        "filters": {"intervention_subtype": "aerobic_or_combined_AT_CT"},
        "alpha_mu": -7.22,
        "alpha_sd": 2,
        "mode": "intercept_only",
        "seed": 6,
    },
    "Ezetimibe 10 mg": {
        "slug": "ezetimibe_10mg_added_to_statin",
        "kind": "single_row",
        "category": "combination_drug",
        "filters": {"intervention_specific": "ezetimibe"},
        "alpha_mu": -24,
        "alpha_sd": 8,
        "mode": "intercept_only",
        "seed": 7,
    },
    "PCSK9 inhibitor": {
        "slug": "pcsk9_evolocumab_added_to_statin",
        "kind": "single_row",
        "category": "combination_drug",
        "filters": {"intervention_specific": "evolocumab"},
        "alpha_mu": -59,
        "alpha_sd": 5,
        "mode": "intercept_only",
        "seed": 8,
    },
    "Portfolio diet (real-world)": {
        "slug": "portfolio_diet_real_world",
        "kind": "single_row",
        "category": "diet",
        "filters": {"intervention_subtype": "full_4_components_real_world"},
        "alpha_mu": -11,
        "alpha_sd": 5,
        "mode": "intercept_only",
        "seed": 9,
    },
    "Portfolio diet (strict)": {
        "slug": "portfolio_diet_strict",
        "kind": "single_row",
        "category": "diet",
        "filters": {"intervention_subtype": "full_4_components_strict_adherence"},
        "alpha_mu": -21,
        "alpha_sd": 5,
        "mode": "intercept_only",
        "seed": 10,
    },
    "fiber": {
        "slug": "fiber_soluble_pooled",
        "kind": "single_row",
        "category": "fiber",
        "filters": {"intervention_specific": "soluble_fiber_pooled"},
        "alpha_mu": -2.2,
        "alpha_sd": 1.0,
        "mode": "intercept_only",
        "seed": 11,
    },
    "weight_loss": {
        "slug": "weight_loss_lifestyle",
        "kind": "single_row",
        "category": "weight_change",
        "filters": {"intervention_subtype": "via_diet_exercise"},
        "alpha_mu": -1.28,
        "alpha_sd": 0.8,
        "mode": "intercept_only",
        "seed": 12,
    },
}


def load_data_for_spec(spec: dict) -> dict:
    """Load model input data for one app intervention spec."""
    if spec["kind"] == "intervention":
        return load_intervention(spec["category"])
    if spec["kind"] == "single_row":
        return load_single_row(spec["category"], spec["filters"])
    raise ValueError(f"Unknown model spec kind: {spec['kind']!r}")


def sample_idata_for_spec(spec: dict, draws: int = 2000):
    """Build and sample one app model spec."""
    data = load_data_for_spec(spec)
    model = build_model(
        data,
        alpha_mu=spec["alpha_mu"],
        alpha_sd=spec["alpha_sd"],
        mode=spec["mode"],
    )
    return sample_model(model, random_seed=spec["seed"], draws=draws)


def posterior_path(spec: dict, posterior_dir: Path = POSTERIOR_DIR) -> Path:
    """NetCDF path for one pre-sampled posterior."""
    return posterior_dir / f"{spec['slug']}.nc"


def save_all_posteriors(posterior_dir: Path = POSTERIOR_DIR, draws: int = 2000,
                        overwrite: bool = False) -> list[Path]:
    """Sample every app model once and save its posterior as NetCDF."""
    posterior_dir.mkdir(parents=True, exist_ok=True)
    written = []

    for label, spec in MODEL_SPECS.items():
        path = posterior_path(spec, posterior_dir)
        if path.exists() and not overwrite:
            written.append(path)
            continue

        print(f"Sampling {label} -> {path}")
        idata = sample_idata_for_spec(spec, draws=draws)
        tmp_path = path.with_suffix(".tmp.nc")
        if tmp_path.exists():
            tmp_path.unlink()
        idata.to_netcdf(tmp_path, engine="h5netcdf")
        tmp_path.replace(path)
        written.append(path)

    return written


def load_saved_models(posterior_dir: Path = POSTERIOR_DIR) -> dict:
    """Load all app model data + pre-sampled posteriors from disk."""
    models = {}
    missing = []

    for label, spec in MODEL_SPECS.items():
        path = posterior_path(spec, posterior_dir)
        if not path.exists():
            missing.append(path)
            continue

        models[label] = {
            "idata": az.from_netcdf(path, engine="h5netcdf"),
            "data": load_data_for_spec(spec),
        }

    if missing:
        missing_str = "\n".join(str(p) for p in missing)
        raise FileNotFoundError(
            "Missing pre-sampled posterior files. Run "
            "`python scripts/precompute_posteriors.py` first:\n"
            f"{missing_str}"
        )

    return models
