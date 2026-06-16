import numpy as np
import pandas as pd
from pathlib import Path

DEFAULT_SE = 3.0  # fallback SE when CI is absent and ldl_change_se is NaN

DATA_PATH = Path(__file__).parent.parent / "data" / "effect_sizes_raw.csv"


def _compute_se(row) -> float:
    """Return SE for one row: ldl_change_se → CI derivation → DEFAULT_SE."""
    val = row["ldl_change_se"]
    if not (isinstance(val, float) and np.isnan(val)):
        return float(val)
    ci_low  = row["ci_low"]
    ci_high = row["ci_high"]
    if not (isinstance(ci_low, float) and np.isnan(ci_low)) and \
       not (isinstance(ci_high, float) and np.isnan(ci_high)):
        return (float(ci_high) - float(ci_low)) / (2 * 1.96)
    return DEFAULT_SE


def load_intervention(intervention_category: str,
                      csv_path: Path = DATA_PATH) -> dict:
    """Load all rows for one intervention category (percent unit only).

    Returns a dict for build_model with mode='dose_response':
      y_obs      - LDL change (%), shape (n_studies,)
      se         - standard error (%), shape (n_studies,)
      dose_c     - centered dose, shape (n_studies,)
      mean_dose  - training-set mean dose (needed to center dose_query)
      dose_raw   - uncentered dose values, for plotting
      labels     - study_id strings
      n_studies  - int
      unit       - 'percent'
    """
    df = pd.read_csv(csv_path)

    subset = df[df["intervention_category"] == intervention_category].copy()
    subset = subset.dropna(subset=["ldl_change_value"]).reset_index(drop=True)

    if subset.empty:
        raise ValueError(f"No rows found for intervention_category={intervention_category!r}")

    # Only percent supported here — non-percent interventions use load_single_row
    unit_vals = subset["ldl_change_unit"].unique()
    non_pct = [u for u in unit_vals if u != "percent"]
    if non_pct:
        raise NotImplementedError(
            f"Unit conversion not implemented for: {non_pct}. "
            "Use load_single_row() for non-percent interventions."
        )

    y_obs = subset["ldl_change_value"].values.astype(float)
    se    = np.array([_compute_se(subset.iloc[i]) for i in range(len(subset))])

    dose_raw  = subset["dose_value"].values.astype(float)
    mean_dose = dose_raw.mean()
    dose_c    = dose_raw - mean_dose

    return {
        "y_obs":     y_obs,
        "se":        se,
        "dose_c":    dose_c,
        "mean_dose": mean_dose,
        "dose_raw":  dose_raw,
        "labels":    subset["study_id"].tolist(),
        "n_studies": len(subset),
        "unit":      "percent",
    }


def load_single_row(intervention_category: str,
                    filters: dict,
                    csv_path: Path = DATA_PATH) -> dict:
    """Load exactly one row identified by category + additional filters.

    Does NOT convert units — raw ldl_change_value and its unit are returned
    as-is. Unit conversion (e.g. mg/dL → %) happens in predict() because
    it requires user-provided baseline_ldl.

    Parameters
    ----------
    intervention_category : str
        Value of the intervention_category column (e.g. 'statin', 'exercise').
    filters : dict
        Additional column→value filters to isolate one row. Examples:
          statin:   {'intervention_specific': 'atorvastatin',
                     'dose_value': 40, 'population': 'all_patients'}
          exercise: {'intervention_subtype': 'aerobic_or_combined_AT_CT'}

    Returns a dict for build_model with mode='intercept_only':
      y_obs      - raw LDL change value, shape (1,)
      se         - standard error in same unit, shape (1,)
      n_studies  - 1
      labels     - [study_id]
      unit       - ldl_change_unit string ('percent' or 'mg_dL', etc.)
    """
    df = pd.read_csv(csv_path)

    mask = df["intervention_category"] == intervention_category
    for col, val in filters.items():
        mask = mask & (df[col] == val)

    subset = df[mask].dropna(subset=["ldl_change_value"]).reset_index(drop=True)

    if subset.empty:
        raise ValueError(
            f"No rows found for category={intervention_category!r}, filters={filters}"
        )
    if len(subset) > 1:
        raise ValueError(
            f"Expected 1 row but got {len(subset)}. Refine filters: {filters}\n"
            f"Matching study_ids: {subset['study_id'].tolist()}"
        )

    row   = subset.iloc[0]
    y_obs = np.array([float(row["ldl_change_value"])])
    se    = np.array([_compute_se(row)])
    unit  = str(row["ldl_change_unit"])

    return {
        "y_obs":     y_obs,
        "se":        se,
        "n_studies": 1,
        "labels":    [str(row["study_id"])],
        "unit":      unit,
    }
