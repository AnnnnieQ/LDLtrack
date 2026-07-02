import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import streamlit as st

from src.app_models import STATIN_OPTIONS, load_saved_models
from src.model_v1 import predict, combine
from src.cvd_risk import cvd_rrr, cvd_arr

# ---------------------------------------------------------------------------
# Model cache
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner="Loading pre-sampled posteriors...")
def load_all_models():
    """Load app models from pre-sampled posterior files."""
    try:
        return load_saved_models()
    except FileNotFoundError as err:
        st.error(
            "Pre-sampled posterior files were not found. "
            "Run `python scripts/precompute_posteriors.py` before launching or deploying the app."
        )
        st.caption(str(err))
        st.stop()

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

    baseline_risk = st.number_input(
        "10-year cardiovascular risk (%) — optional",
        min_value=0.0, max_value=100.0, value=0.0, step=0.5,
        help="From your doctor or a PCE / SCORE2 calculator. "
             "Leave at 0 to show relative risk reduction only.",
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
    st.subheader("Results")

    if not predictions:
        st.info("Select at least one intervention to see a prediction.")
    else:
        result = combine(baseline_ldl, predictions)

        final_mean = result["ldl_final"].mean()
        final_lo   = np.percentile(result["ldl_final"], 2.5)
        final_hi   = np.percentile(result["ldl_final"], 97.5)
        eff_mean   = result["total_effect"].mean()

        # Per-sample RRR from the LDL-reduction posterior. Fixed CTT 0.78
        # (sample_effect=False) — the effect-size CI second layer is omitted by
        # design (it widens the interval by only ~1pp; see caveat below).
        cvd = cvd_rrr(baseline_ldl, result["ldl_final"])
        rrr_samples = cvd["rrr"]
        rrr_mean = rrr_samples.mean() * 100
        rrr_lo   = np.percentile(rrr_samples, 2.5) * 100
        rrr_hi   = np.percentile(rrr_samples, 97.5) * 100

        metric_cols = st.columns(3 if baseline_risk > 0 else 2)
        with metric_cols[0]:
            st.metric(
                label="Predicted final LDL",
                value=f"{final_mean:.1f} mg/dL",
                delta=f"{eff_mean:.1f}%  (95% CrI {final_lo:.1f}–{final_hi:.1f} mg/dL)",
                delta_color="inverse",
            )
        with metric_cols[1]:
            st.metric(
                label="Relative cardiovascular risk reduction",
                value=f"{rrr_mean:.1f}%",
                delta=f"95% CrI {rrr_lo:.1f}–{rrr_hi:.1f}%",
                delta_color="off",
            )
        if baseline_risk > 0:
            arr_out = cvd_arr(rrr_samples, baseline_risk)
            arr_mean = arr_out["arr"].mean()
            arr_lo   = np.percentile(arr_out["arr"], 2.5)
            arr_hi   = np.percentile(arr_out["arr"], 97.5)
            with metric_cols[2]:
                st.metric(
                    label="Absolute cardiovascular risk reduction",
                    value=f"{arr_mean:.1f} pp",
                    delta=f"95% CrI {arr_lo:.1f}–{arr_hi:.1f} pp",
                    delta_color="off",
                )

        # Bullet chart: show the LDL reduction path, with the credible interval
        # around the predicted final LDL.
        scale_min = min(final_lo, baseline_ldl) - 10
        scale_max = max(final_hi, baseline_ldl) + 10
        scale_span = scale_max - scale_min

        def pct_position(value):
            return max(0, min(100, 100 * (value - scale_min) / scale_span))

        lo_pos = pct_position(final_lo)
        hi_pos = pct_position(final_hi)
        mean_pos = pct_position(final_mean)
        baseline_pos = pct_position(baseline_ldl)
        reduction_left = min(mean_pos, baseline_pos)
        reduction_width = abs(baseline_pos - mean_pos)
        reduction_gradient = (
            "linear-gradient(90deg, #b8e0ea 0%, #219ebc 100%)"
            if mean_pos < baseline_pos
            else "linear-gradient(90deg, #219ebc 0%, #b8e0ea 100%)"
        )

        st.markdown(
            f"""
            <div style="
                margin: 1.2rem 0 1.4rem 0;
                padding: 1.15rem 1.2rem 1rem 1.2rem;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                background: #ffffff;
            ">
              <div style="
                  display: flex;
                  justify-content: space-between;
                  align-items: baseline;
                  margin-bottom: 0.8rem;
              ">
                <div style="font-size: 0.9rem; color: #4b5563; font-weight: 600;">
                  LDL reduction path
                </div>
                <div style="font-size: 0.82rem; color: #6b7280;">
                  95% CrI {final_lo:.1f}-{final_hi:.1f} mg/dL
                </div>
              </div>
              <div style="
                  position: relative;
                  height: 58px;
              ">
                <div style="
                    position: absolute;
                    left: 0;
                    right: 0;
                    top: 25px;
                    height: 10px;
                    border-radius: 999px;
                    background: #eef2f7;
                "></div>
                <div style="
                    position: absolute;
                    left: {reduction_left:.2f}%;
                    width: {reduction_width:.2f}%;
                    top: 24px;
                    height: 12px;
                    border-radius: 999px;
                    background: {reduction_gradient};
                    opacity: 0.82;
                "></div>
                <div style="
                    position: absolute;
                    left: {lo_pos:.2f}%;
                    width: {hi_pos - lo_pos:.2f}%;
                    top: 21px;
                    height: 18px;
                    border-radius: 999px;
                    background: rgba(18, 103, 130, 0.16);
                    border: 1px solid rgba(18, 103, 130, 0.22);
                "></div>
                <div style="
                    position: absolute;
                    left: {mean_pos:.2f}%;
                    top: 21px;
                    width: 18px;
                    height: 18px;
                    margin-left: -9px;
                    border-radius: 50%;
                    background: #126782;
                    border: 3px solid #ffffff;
                    box-shadow: 0 2px 8px rgba(18, 103, 130, 0.25);
                "></div>
                <div style="
                    position: absolute;
                    left: {baseline_pos:.2f}%;
                    top: 16px;
                    width: 0;
                    height: 26px;
                    border-left: 2px dashed #475569;
                "></div>
                <div style="
                    position: absolute;
                    left: {mean_pos:.2f}%;
                    top: 47px;
                    transform: translateX(-50%);
                    color: #126782;
                    font-size: 0.88rem;
                    font-weight: 700;
                    white-space: nowrap;
                ">
                  predicted {final_mean:.1f}
                </div>
                <div style="
                    position: absolute;
                    left: {baseline_pos:.2f}%;
                    top: -2px;
                    transform: translateX(-50%);
                    color: #475569;
                    font-size: 0.76rem;
                    font-weight: 600;
                    white-space: nowrap;
                ">
                  starting {baseline_ldl:.0f}
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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

        with st.expander("About this estimate"):
            st.caption(
                "The 95% credible interval (CrI) reflects uncertainty "
                "in the average dose-response estimated from clinical trials — not a guarantee "
                "that your LDL will fall within this range. Individual response varies. "
                "Exercise effect (Smart 2024) is not stratified by intensity or frequency. "
                "Individual contributions are order-dependent and shown for illustration only; "
                "the combined total is order-independent. "
                "When multiple aggressive interventions are combined, the multiplicative model "
                "can produce predictions below ~25 mg/dL — a level rarely seen clinically. "
                "This is a mathematical artifact of stacking independent % reductions, "
                "not a realistic forecast. The model applies no biological floor. "
                "The 0.78 relative risk per mmol/L comes from statin trials (CTT); applying "
                "it to plant sterols and exercise assumes the benefit per mmol/L is "
                "mechanism-independent, which may overstate benefit if non-receptor-mediated "
                "LDL lowering is less effective, and may understate exercise's total benefit "
                "(which also acts via non-LDL pathways). "
                "The displayed RRR uses the fixed CTT 0.78 and does not include the literature "
                "effect-size CI (0.76–0.80); that second layer was measured to widen the "
                "interval by only ~1 percentage point."
            )
