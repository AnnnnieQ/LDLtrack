import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from src.data_loader import load_intervention, load_single_row
from src.model_v1 import build_model, sample_model, predict, combine

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STATIN_OPTIONS = {
    "Atorvastatin 40 mg":  {"intervention_specific": "atorvastatin", "dose_value": 40},
    "Atorvastatin 80 mg":  {"intervention_specific": "atorvastatin", "dose_value": 80},
    "Rosuvastatin 20 mg":  {"intervention_specific": "rosuvastatin", "dose_value": 20},
    "Rosuvastatin 40 mg":  {"intervention_specific": "rosuvastatin", "dose_value": 40},
}

# ---------------------------------------------------------------------------
# Model cache (MCMC runs once at startup)
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner="Running MCMC — one-time setup, ~30 seconds...")
def load_all_models():
    """Pre-sample all intervention models. Cached across reruns."""
    models = {}

    # Statin: prior centered at -50% (published high-intensity statin literature range),
    # independent of the specific row's observed value. alpha_sd=5 is wide enough
    # that the single-row likelihood dominates (posterior ≈ Normal(y_obs, se)).
    statin_seeds = [1, 2, 3, 4]
    for (label, filters), seed in zip(STATIN_OPTIONS.items(), statin_seeds):
        data = load_single_row("statin", {**filters, "population": "all_patients"})
        model = build_model(data, alpha_mu=-50, alpha_sd=5, mode="intercept_only")
        idata = sample_model(model, random_seed=seed, draws=2000)
        models[label] = {"idata": idata, "data": data}

    data_sterols = load_intervention("plant_sterols")
    model_sterols = build_model(data_sterols, alpha_mu=-8.0, alpha_sd=2.5, mode="dose_response")
    idata_sterols = sample_model(model_sterols, random_seed=5, draws=2000)
    models["plant_sterols"] = {"idata": idata_sterols, "data": data_sterols}

    data_ex = load_single_row("exercise",
                              {"intervention_subtype": "aerobic_or_combined_AT_CT"})
    model_ex = build_model(data_ex, alpha_mu=-7.22, alpha_sd=2, mode="intercept_only")
    idata_ex = sample_model(model_ex, random_seed=6, draws=2000)
    models["exercise"] = {"idata": idata_ex, "data": data_ex}

    return models

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

st.set_page_config(page_title="LDLtrack", layout="wide")
st.title("LDLtrack")
st.caption("Bayesian LDL reduction estimator — combines evidence from landmark RCTs.")

models = load_all_models()

col_in, col_out = st.columns([1, 1.6], gap="large")

# ── Inputs ──────────────────────────────────────────────────────────────────
with col_in:
    st.subheader("Inputs")

    baseline_ldl = st.number_input(
        "Baseline LDL (mg/dL)", min_value=60, max_value=280, value=150, step=1
    )

    st.markdown("---")
    st.markdown("**Statin**")
    statin_choice = st.selectbox("Drug and dose", ["None"] + list(STATIN_OPTIONS.keys()))

    st.markdown("---")
    st.markdown("**Plant sterols**")
    sterols_on   = st.checkbox("Include plant sterols")
    sterols_dose = st.slider("Dose (g/day)", 0.6, 3.3, 2.0, step=0.1,
                             disabled=not sterols_on)

    st.markdown("---")
    st.markdown("**Exercise**")
    exercise_on = st.checkbox("Include aerobic / combined exercise")

# ── Compute predictions ──────────────────────────────────────────────────────
predictions = []   # list of predict() dicts, in fixed order
layer_labels = []  # human-readable name per prediction

if statin_choice != "None":
    m = models[statin_choice]
    predictions.append(predict(m["idata"], m["data"], baseline_ldl=baseline_ldl))
    layer_labels.append(statin_choice)

if sterols_on:
    m = models["plant_sterols"]
    predictions.append(predict(m["idata"], m["data"],
                               baseline_ldl=baseline_ldl, dose_query=sterols_dose))
    layer_labels.append(f"Plant sterols {sterols_dose:.1f} g/day")

if exercise_on:
    m = models["exercise"]
    predictions.append(predict(m["idata"], m["data"], baseline_ldl=baseline_ldl))
    layer_labels.append("Aerobic/combined exercise")

# ── Outputs ──────────────────────────────────────────────────────────────────
with col_out:
    st.subheader("Predicted LDL")

    if not predictions:
        st.info("Select at least one intervention to see a prediction.")
    else:
        result = combine(baseline_ldl, predictions)

        final_mean = result["ldl_final"].mean()
        final_lo   = np.percentile(result["ldl_final"], 2.5)
        final_hi   = np.percentile(result["ldl_final"], 97.5)
        eff_mean   = result["total_effect"].mean()

        st.metric(
            label="Predicted final LDL",
            value=f"{final_mean:.1f} mg/dL",
            delta=f"{eff_mean:.1f}%  (95% CrI {final_lo:.1f}–{final_hi:.1f} mg/dL)",
            delta_color="inverse",
        )

        # Histogram
        fig, ax = plt.subplots(figsize=(6, 2.5))
        ax.hist(result["ldl_final"], bins=60, density=True,
                color="steelblue", alpha=0.7, edgecolor="none")
        ax.axvline(final_mean, color="steelblue", lw=2)
        ax.axvline(final_lo,   color="steelblue", lw=1.2, linestyle="--")
        ax.axvline(final_hi,   color="steelblue", lw=1.2, linestyle="--")
        ax.axvline(baseline_ldl, color="firebrick", lw=2, label=f"Baseline {baseline_ldl}")
        ax.set_xlabel("Predicted final LDL (mg/dL)")
        ax.set_yticks([])
        ax.legend(fontsize=8)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # Contribution breakdown (fixed order, mean effects only)
        st.markdown("**Individual effects** *(fixed order: drug → supplement → lifestyle)*")
        running_ldl = float(baseline_ldl)
        rows = []
        for label, pred in zip(layer_labels, predictions):
            eff_pct  = pred["theta_new"].mean()
            ldl_after = running_ldl * (1 + eff_pct / 100)
            delta_mg  = ldl_after - running_ldl
            rows.append({
                "Intervention": label,
                "Effect (%)":   f"{eff_pct:.1f}%",
                "ΔLDLmg/dL":   f"{delta_mg:.1f}",
                "LDL after":    f"{ldl_after:.1f}",
            })
            running_ldl = ldl_after

        for r in rows:
            st.markdown(
                f"- **{r['Intervention']}**: {r['Effect (%)']} "
                f"→ {r['ΔLDLmg/dL']} mg/dL  (LDL: {r['LDL after']} mg/dL)"
            )

        st.markdown("---")
        st.caption(
            "**About this estimate**: The 95% credible interval (CrI) reflects uncertainty "
            "in the average dose-response estimated from clinical trials — not a guarantee "
            "that your LDL will fall within this range. Individual response varies. "
            "Exercise effect (Smart 2024) is not stratified by intensity or frequency. "
            "Individual contributions are order-dependent and shown for illustration only; "
            "the combined total is order-independent. "
            "When multiple aggressive interventions are combined, the multiplicative model "
            "can produce predictions below ~25 mg/dL — a level rarely seen clinically. "
            "This is a mathematical artifact of stacking independent % reductions, "
            "not a realistic forecast. The model applies no biological floor."
        )
