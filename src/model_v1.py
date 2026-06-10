import numpy as np
import pymc as pm


def build_model(data: dict,
                alpha_mu: float,
                alpha_sd: float,
                hierarchical: bool = False) -> pm.Model:
    """Bayesian dose-response model for a single intervention.

    Parameters
    ----------
    data : dict
        Output of data_loader.load_intervention().
    alpha_mu : float
        Prior mean for alpha (pooled effect at mean dose, %).
    alpha_sd : float
        Prior SD for alpha. Use ~3x the paper-reported CI half-width.
    hierarchical : bool
        False (default): pure dose-response regression.
          Use when all rows come from one paper (e.g. plant sterols).
        True: adds tau + theta_offset random effects.
          Use when rows come from multiple independent studies.

    Note: dose_query and baseline_ldl are NOT model parameters.
    Call predict() after sampling to get predictions at any dose/baseline
    without re-running MCMC.

    Model structure (hierarchical=False)
    -------------------------------------
    alpha ~ Normal(alpha_mu, alpha_sd)
    beta  ~ Normal(0, 2)
    theta_i = alpha + beta * dose_c_i
    y_i ~ Normal(theta_i, se_i)

    Model structure (hierarchical=True)
    -------------------------------------
    Same as above, plus:
    tau          ~ HalfNormal(5)
    theta_offset ~ Normal(0, 1, shape=n_studies)   # non-centered
    theta_i       = alpha + beta * dose_c_i + tau * theta_offset_i
    """
    y_obs     = data["y_obs"]
    se        = data["se"]
    dose_c    = data["dose_c"]
    n_studies = data["n_studies"]

    with pm.Model() as model:
        alpha = pm.Normal("alpha", mu=alpha_mu, sigma=alpha_sd)
        beta  = pm.Normal("beta",  mu=0, sigma=2)

        if hierarchical:
            tau = pm.HalfNormal("tau", sigma=5)
            theta_offset = pm.Normal("theta_offset", mu=0, sigma=1, shape=n_studies)
            theta = pm.Deterministic(
                "theta", alpha + beta * dose_c + tau * theta_offset
            )
        else:
            theta = pm.Deterministic(
                "theta", alpha + beta * dose_c
            )

        pm.Normal("obs", mu=theta, sigma=se, observed=y_obs)

    return model


def sample_model(model: pm.Model,
                 draws: int = 2000,
                 tune: int = 1000,
                 chains: int = 4,
                 target_accept: float = 0.9,
                 random_seed: int = 42):
    """Run MCMC on a model returned by build_model."""
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


def predict(idata, data: dict, dose_query: float, baseline_ldl: float) -> dict:
    """Compute predictions from posterior samples (no re-sampling needed).

    Works for any dose_query / baseline_ldl without rebuilding the model.
    If tau is present in idata (hierarchical=True), samples a new individual's
    offset to include between-study heterogeneity in the interval.

    Parameters
    ----------
    idata : arviz.InferenceData
        Output of sample_model().
    data : dict
        Same data dict passed to build_model() — needed for mean_dose.
    dose_query : float
        Dose in original units (uncentered).
    baseline_ldl : float
        User's baseline LDL in mg/dL.

    Returns
    -------
    dict with keys:
      'theta_new'  : predicted % LDL change, shape (n_samples,)
      'ldl_final'  : predicted final LDL in mg/dL, shape (n_samples,)
    """
    alpha_s = idata.posterior["alpha"].values.flatten()
    beta_s  = idata.posterior["beta"].values.flatten()

    dose_query_c = dose_query - data["mean_dose"]

    if "tau" in idata.posterior:
        tau_s = idata.posterior["tau"].values.flatten()
        rng = np.random.default_rng(seed=0)
        offset_new = rng.normal(0, 1, len(alpha_s))
        theta_new_s = alpha_s + beta_s * dose_query_c + tau_s * offset_new
    else:
        theta_new_s = alpha_s + beta_s * dose_query_c

    ldl_final_s = baseline_ldl * (1 + theta_new_s / 100)

    return {"theta_new": theta_new_s, "ldl_final": ldl_final_s}
