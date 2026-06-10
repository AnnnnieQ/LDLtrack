import numpy as np
import pandas as pd
from pathlib import Path

DEFAULT_SE = 3.0  # fallback SE (%) when CI is absent and ldl_change_se is NaN

DATA_PATH = Path(__file__).parent.parent / "data" / "effect_sizes_raw.csv"


def load_intervention(intervention_category: str,
                      csv_path: Path = DATA_PATH) -> dict:
    """Load and preprocess one intervention category for model_v1.

    Returns a dict with arrays ready for PyMC:
      y_obs      - LDL change (%), shape (n_studies,)
      se         - standard error (%), shape (n_studies,)
      dose_c     - centered dose (original unit), shape (n_studies,)
      mean_dose  - training-set mean dose; use this to center a query dose
      dose_raw   - uncentered dose values, for plotting
      labels     - study_id strings, for diagnostics
      n_studies  - int
    """
    df = pd.read_csv(csv_path)

    subset = df[df["intervention_category"] == intervention_category].copy()
    subset = subset.dropna(subset=["ldl_change_value"]).reset_index(drop=True)

    if subset.empty:
        raise ValueError(f"No rows found for intervention_category={intervention_category!r}")

    # Unit conversion to percent
    # TODO (pre-statin): mg_dL, mg_dL_per_kg, mg_dL_per_g conversions need
    # baseline_ldl, body_weight_kg, and dose_g sources — not yet defined.
    unit = subset["ldl_change_unit"].unique()
    non_pct = [u for u in unit if u != "percent"]
    if non_pct:
        raise NotImplementedError(
            f"Unit conversion not yet implemented for: {non_pct}. "
            "Only 'percent' rows are supported in v1."
        )

    y_obs = subset["ldl_change_value"].values.astype(float)

    # SE: use ldl_change_se if present, else derive from CI, else use default
    se = subset["ldl_change_se"].values.astype(float)
    for i in range(len(se)):
        if np.isnan(se[i]):
            ci_low = subset["ci_low"].iloc[i]
            ci_high = subset["ci_high"].iloc[i]
            if not (np.isnan(ci_low) or np.isnan(ci_high)):
                se[i] = (float(ci_high) - float(ci_low)) / (2 * 1.96)
            else:
                se[i] = DEFAULT_SE

    dose_raw = subset["dose_value"].values.astype(float)
    mean_dose = dose_raw.mean()
    dose_c = dose_raw - mean_dose  # center using training-set mean

    return {
        "y_obs": y_obs,
        "se": se,
        "dose_c": dose_c,
        "mean_dose": mean_dose,   # needed to center dose_query at prediction time
        "dose_raw": dose_raw,
        "labels": subset["study_id"].tolist(),
        "n_studies": len(subset),
    }
