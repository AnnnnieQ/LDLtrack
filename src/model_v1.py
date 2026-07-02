import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pymc as pm


def build_model(data: dict,
                alpha_mu: float,
                alpha_sd: float,
                mode: str = 'dose_response') -> "pm.Model":
    """Bayesian LDL reduction model for a single intervention.

    Parameters
    ----------
    data : dict
        Output of data_loader.load_intervention() or load_single_row().
    alpha_mu : float
        Prior mean for alpha (effect at mean dose for dose_response;
        effect estimate for intercept_only), in %.
    alpha_sd : float
        Prior SD for alpha. Use ~3x the paper-reported CI half-width.
    mode : str
        'dose_response'  — alpha + beta * dose_c. Use when rows span a
                           continuous dose range from one paper (e.g. plant
                           sterols). No tau — avoids tau->0 boundary issues.
        'intercept_only' — alpha only. Use when the user selects a single
                           row (e.g. statin: one drug/dose; exercise: one
                           modality). Posterior ≈ Normal(y_obs, se).
        'hierarchical'   — alpha + beta * dose_c + tau * theta_offset.
                           Use when rows come from multiple independent
                           studies. Not used in Milestone 2.3.

    Note: dose_query and baseline_ldl are NOT model parameters.
    Call predict() after sampling to get predictions at any input
    without re-running MCMC.
    """
    y_obs     = data["y_obs"]
    se        = data["se"]
    n_studies = data["n_studies"]

    import pymc as pm

    with pm.Model() as model:
        alpha = pm.Normal("alpha", mu=alpha_mu, sigma=alpha_sd)

        if mode == 'dose_response':
            dose_c = data["dose_c"]
            beta   = pm.Normal("beta", mu=0, sigma=2)
            theta  = pm.Deterministic("theta", alpha + beta * dose_c)

        elif mode == 'intercept_only':
            theta = pm.Deterministic("theta", alpha * np.ones(n_studies))

        elif mode == 'hierarchical':
            dose_c       = data["dose_c"]
            beta         = pm.Normal("beta", mu=0, sigma=2)
            tau          = pm.HalfNormal("tau", sigma=5)
            theta_offset = pm.Normal("theta_offset", mu=0, sigma=1, shape=n_studies)
            theta        = pm.Deterministic(
                "theta", alpha + beta * dose_c + tau * theta_offset
            )

        else:
            raise ValueError(f"Unknown mode {mode!r}. "
                             "Choose 'dose_response', 'intercept_only', or 'hierarchical'.")

        pm.Normal("obs", mu=theta, sigma=se, observed=y_obs)

    return model


def sample_model(model: "pm.Model",
                 draws: int = 2000,
                 tune: int = 1000,
                 chains: int = 4,
                 target_accept: float = 0.9,
                 random_seed: int = 42):
    """Run MCMC on a model returned by build_model."""
    import pymc as pm

    with model:
        idata = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            random_seed=random_seed,
            progressbar=True,
        )
    return idata


def predict(idata,
            data: dict,
            baseline_ldl: float,
            dose_query: float = None) -> dict:
    """Compute predictions from posterior samples (no re-sampling needed).

    Works for any baseline_ldl without rebuilding the model. For
    dose_response mode, also accepts dose_query to evaluate the curve at
    a specific dose. For intercept_only mode, dose_query is unused.

    Parameters
    ----------
    idata : arviz.InferenceData
        Output of sample_model().
    data : dict
        Same data dict passed to build_model() — needed for mean_dose.
    baseline_ldl : float
        User's baseline LDL in mg/dL.
    dose_query : float or None
        Dose in original units (uncentered). Required for dose_response
        mode; ignored for intercept_only.

    Returns
    -------
    dict with keys:
      'theta_new'  : predicted % LDL change, shape (n_samples,)
      'ldl_final'  : predicted final LDL in mg/dL, shape (n_samples,)
    """
    alpha_s = idata.posterior["alpha"].values.flatten()

    if "beta" in idata.posterior:
        # dose_response or hierarchical mode
        beta_s = idata.posterior["beta"].values.flatten()
        dose_query_c = dose_query - data["mean_dose"]
        theta_new_s = alpha_s + beta_s * dose_query_c

        if "tau" in idata.posterior:
            tau_s = idata.posterior["tau"].values.flatten()
            rng = np.random.default_rng(seed=0)
            offset_new = rng.normal(0, 1, len(alpha_s))
            theta_new_s = theta_new_s + tau_s * offset_new
    else:
        # intercept_only mode — dose_query is irrelevant
        theta_new_s = alpha_s

    # Unit conversion: if raw model output is in mg_dL, convert to % now
    # so that combine() and ldl_final both operate on a consistent % scale.
    # exercise_pct = -7.22 / baseline_ldl * 100  (user baseline as denominator)
    unit = data.get("unit", "percent")
    if unit == "mg_dL":
        theta_new_s = theta_new_s / baseline_ldl * 100

    ldl_final_s = baseline_ldl * (1 + theta_new_s / 100)

    return {"theta_new": theta_new_s, "ldl_final": ldl_final_s}


def combine(baseline_ldl: float, predictions: list) -> dict:
    """Combine multiple intervention predictions multiplicatively.

    Each intervention's % effect is applied in sequence to the running LDL:
      final = baseline × Π(1 + theta_i / 100)

    Multiplication is commutative so order doesn't affect the result.
    Note: for interventions with absolute effects converted to % using
    user baseline (e.g. exercise), the % will vary by individual and the
    absolute reduction implied may differ from the paper-reported value
    when applied after other interventions — this is a known approximation.

    Parameters
    ----------
    baseline_ldl : float
        User's baseline LDL in mg/dL.
    predictions : list of dict
        Each dict is a predict() output with key 'theta_new' (% samples).
        All dicts must have the same number of samples.

    Returns
    -------
    dict with keys:
      'ldl_final'     : combined predicted LDL in mg/dL, shape (n_samples,)
      'total_effect'  : total % reduction, shape (n_samples,)
    """
    n = len(predictions[0]["theta_new"])
    for pred in predictions:
        if len(pred["theta_new"]) != n:
            raise ValueError(
                f"All predictions must have the same number of samples. "
                f"Got {len(pred['theta_new'])} vs {n}."
            )

    rng = np.random.default_rng(seed=0)
    ldl = np.full(n, float(baseline_ldl))
    for pred in predictions:
        theta = pred["theta_new"].copy()
        rng.shuffle(theta)  # break chain-block alignment; interventions are independent
        ldl = ldl * (1 + theta / 100)

    total_effect = (ldl - baseline_ldl) / baseline_ldl * 100

    return {"ldl_final": ldl, "total_effect": total_effect}
