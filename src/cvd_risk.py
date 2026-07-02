"""Cardiovascular risk conversion from LDL reduction.

Downstream of the Bayesian model: takes the posterior LDL samples produced by
model_v1.combine() (or predict()) and converts an absolute LDL reduction into
a relative cardiovascular risk reduction (RRR), per the CTT / Mach 2020
proportional-risk relationship.

Pure numpy — no PyMC. The conversion is applied per posterior sample, so the
uncertainty in the LDL reduction propagates straight through to the RRR.

By default the per-mmol/L effect size is fixed (RR_PER_MMOL = 0.78). Passing
sample_effect=True optionally adds the CTT effect-size CI as a second layer of
uncertainty, drawn per sample on the log scale.
"""

import numpy as np

# 1 mmol/L LDL-C = 38.67 mg/dL (standard conversion factor for LDL cholesterol).
MG_DL_PER_MMOL = 38.67

# CTT / Mach 2020: relative risk for major vascular events per 1 mmol/L LDL-C
# reduction. The relationship is proportional (constant per mmol/L), so the RR
# for a total reduction of x mmol/L is RR_PER_MMOL ** x — a multiplicative
# compounding, NOT a linear 0.22 * x.
RR_PER_MMOL = 0.78

# CTT 2010 95% CI for the per-mmol/L RR. The effect size itself is uncertain;
# sampling it (sample_effect=True) adds a second layer of uncertainty on top of
# the LDL-reduction posterior, so the RRR interval reflects both.
RR_PER_MMOL_CI = (0.76, 0.80)
# SE on the log scale, reverse-engineered from the CI (~0.0131). Sampling is
# done on the log scale because RR must stay positive and the CI is roughly
# symmetric in log space, not in RR space.
RR_PER_MMOL_LN_SE = (np.log(RR_PER_MMOL_CI[1]) - np.log(RR_PER_MMOL_CI[0])) / (2 * 1.96)


def cvd_rrr(baseline_ldl, ldl_final, rr_per_mmol=RR_PER_MMOL,
            sample_effect=False, n_samples=None, random_seed=0):
    """Relative cardiovascular risk reduction from an LDL reduction.

    Parameters
    ----------
    baseline_ldl : float
        User's baseline LDL in mg/dL.
    ldl_final : float or np.ndarray
        Predicted final LDL in mg/dL. Typically the per-sample 'ldl_final'
        array from model_v1.combine(), but a scalar works too (point estimate).
    rr_per_mmol : float
        Fixed relative risk per 1 mmol/L LDL reduction. Used only when
        sample_effect=False. Defaults to the CTT 0.78.
    sample_effect : bool
        If False (default, Day 1 behaviour), use the fixed rr_per_mmol.
        If True, draw the per-mmol/L RR per sample on the log scale from
        Normal(ln 0.78, RR_PER_MMOL_LN_SE), adding the CTT effect-size CI as a
        second layer of uncertainty. Each LDL-reduction sample i is paired with
        its own drawn rr_per_i; the two layers are independent.
    n_samples : int or None
        Required only when sample_effect=True AND ldl_final is a scalar (a pure
        point-estimate case): how many effect-size draws to take. Ignored for
        array input, where the count comes from len(ldl_final).
    random_seed : int
        Seed for the effect-size draws (sample_effect=True only).

    Returns
    -------
    dict with keys:
      'rr'  : relative risk vs baseline. Naturally in (0, 1] for an LDL
              reduction (delta >= 0); > 1 if LDL rises (delta < 0), correctly
              indicating increased risk.
      'rrr' : relative risk reduction = 1 - rr.
    """
    # Detect the scalar case on the raw input: np.asarray turns a scalar into a
    # 0-d array, on which np.isscalar returns False. np.ndim == 0 catches both.
    is_scalar_input = np.ndim(ldl_final) == 0

    ldl_final = np.asarray(ldl_final, dtype=float)
    delta_mmol = (baseline_ldl - ldl_final) / MG_DL_PER_MMOL

    if sample_effect:
        if is_scalar_input and n_samples is None:
            raise ValueError(
                "n_samples required when sample_effect=True and ldl_final is scalar"
            )
        rng = np.random.default_rng(random_seed)
        n = n_samples if is_scalar_input else len(delta_mmol)
        # Draw per-mmol/L RR on the log scale so it stays positive.
        rr_per = np.exp(rng.normal(np.log(RR_PER_MMOL), RR_PER_MMOL_LN_SE, n))
    else:
        rr_per = rr_per_mmol                      # Day 1 behaviour: fixed

    rr = rr_per ** delta_mmol                      # per-sample, paired layer-by-layer
    rrr = 1.0 - rr

    return {"rr": rr, "rrr": rrr}


def cvd_arr(rrr, baseline_risk_pct):
    """Absolute cardiovascular risk reduction from a relative risk reduction.

    RRR alone is a multiplier; it does not say how many percentage points of
    risk are actually avoided. That depends on the user's absolute baseline
    risk: a 40% RRR removes 8 points from a 20% baseline but only 2 from a 5%
    baseline. This converts RRR to an absolute reduction (ARR) and the residual
    final risk, per sample so the RRR posterior propagates through.

    Parameters
    ----------
    rrr : float or np.ndarray
        Relative risk reduction (e.g. the 'rrr' array from cvd_rrr).
    baseline_risk_pct : float
        User's 10-year CVD risk in % (0-100), from a doctor or an external
        calculator (PCE / SCORE2). A single scalar applied to every sample.

    Returns
    -------
    dict with keys:
      'arr'        : absolute risk reduction in percentage points,
                     = baseline_risk_pct * rrr, same shape as rrr.
      'final_risk' : residual 10-year risk in %, = baseline_risk_pct - arr.
    """
    rrr = np.asarray(rrr, dtype=float)
    arr = baseline_risk_pct * rrr
    final_risk = baseline_risk_pct - arr
    return {"arr": arr, "final_risk": final_risk}
