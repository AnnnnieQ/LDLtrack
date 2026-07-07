import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import streamlit as st

from src.app_models import STATIN_OPTIONS, load_saved_models
from src.model_v1 import predict, combine
from src.cvd_risk import cvd_rrr, cvd_arr

# ---------------------------------------------------------------------------
# Theme, logo, and animation (injected once)
# ---------------------------------------------------------------------------

LDL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --ldl-teal: #126782;
  --ldl-teal-mid: #219ebc;
  --ldl-teal-light: #b8e0ea;
  --ldl-ink: #1f2937;
  --ldl-muted: #6b7280;
  --ldl-border: #e6e9ee;
}

html, body, .stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont,
  "Segoe UI", Roboto, sans-serif; }

/* Streamlit's fixed top toolbar is transparent and floats over the content, so
   anything scrolled to the very top (e.g. the chart) gets clipped under it.
   Hide it — the menu isn't needed for this demo. */
[data-testid="stHeader"] { display: none; }

/* Tighten the default page frame and cap line length. */
.block-container { padding-top: 2.1rem; padding-bottom: 3rem; max-width: 1180px; }

/* Header / logo */
.ldl-header { display: flex; align-items: center; margin: 0 0 2px 0; }
.ldl-wordmark { font-size: 1.95rem; font-weight: 700; letter-spacing: -0.025em;
  color: var(--ldl-ink); line-height: 1; }
.ldl-wordmark .accent { color: var(--ldl-teal); }

/* Metric cards */
[data-testid="stMetric"] {
  background: #ffffff;
  border: 1px solid var(--ldl-border);
  border-radius: 12px;
  padding: 14px 16px 12px 16px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.05);
  transition: transform .18s ease, box-shadow .18s ease;
  animation: ldlFadeUp .45s ease both;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(18, 103, 130, 0.12);
}
[data-testid="stMetricLabel"] p { font-weight: 600; color: var(--ldl-muted); }
[data-testid="stMetricValue"] { color: var(--ldl-ink); font-weight: 700; }

/* Gentle stagger across the metric row */
[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"] { animation-delay: .07s; }
[data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetric"] { animation-delay: .14s; }

/* Keyframes */
@keyframes ldlFadeUp { from { opacity: 0; transform: translateY(9px); } to { opacity: 1; transform: none; } }
@keyframes ldlGrowX  { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes ldlPop {
  0%   { opacity: 0; transform: scale(.4); }
  60%  { opacity: 1; transform: scale(1.12); }
  100% { opacity: 1; transform: scale(1); }
}
@keyframes ldlFadeIn { from { opacity: 0; } to { opacity: 1; } }

/* Respect users who prefer reduced motion. */
@media (prefers-reduced-motion: reduce) {
  [data-testid="stMetric"], .ldl-anim-card, .ldl-anim-bar,
  .ldl-anim-band, .ldl-anim-marker, .ldl-anim-fade {
    animation: none !important;
    transition: none !important;
  }
}
</style>
"""

# Wordmark-only header — minimal, no icon/badge. "track" carries the teal accent.
LDL_HEADER = """
<div class="ldl-header">
  <span class="ldl-wordmark">LDL<span class="accent">track</span></span>
</div>
"""

# ---------------------------------------------------------------------------
# Model cache
# ---------------------------------------------------------------------------

MODEL_CACHE_VERSION = "3.3B_per_unit_interventions"

@st.cache_resource(show_spinner="Loading pre-sampled posteriors...")
def load_all_models(model_cache_version: str):
    """Load app models from pre-sampled posterior files."""
    _ = model_cache_version
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

st.set_page_config(page_title="LDLtrack", page_icon="📉", layout="wide")
st.markdown(LDL_CSS, unsafe_allow_html=True)
st.markdown(LDL_HEADER, unsafe_allow_html=True)
st.caption(
    "Choose LDL-lowering options you are considering, then see the predicted "
    "LDL change and estimated cardiovascular risk reduction."
)
st.info(
    "Educational portfolio demo only — not medical advice. Review treatment "
    "decisions with a licensed clinician."
)

models = load_all_models(MODEL_CACHE_VERSION)

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
    statin_selected = statin_choice != "None"

    st.markdown("**Add-on medication**")
    if not statin_selected:
        st.session_state["ezetimibe_on"] = False
        st.session_state["pcsk9_on"] = False
    ezetimibe_on = st.checkbox(
        "Add ezetimibe",
        key="ezetimibe_on",
        disabled=not statin_selected,
    )
    pcsk9_on = st.checkbox(
        "Add PCSK9 inhibitor",
        key="pcsk9_on",
        disabled=not statin_selected,
    )
    if not statin_selected:
        st.caption("Ezetimibe and PCSK9 inhibitor estimates require a statin background.")

    st.markdown("---")
    st.markdown("**Diet and supplements**")
    portfolio_on = st.checkbox("Include Portfolio diet")
    portfolio_choice = st.selectbox(
        "Portfolio diet adherence",
        ["Real-world adherence", "Strict efficacy trial"],
        disabled=not portfolio_on,
    )

    st.markdown("**Plant sterols**")
    sterols_on   = st.checkbox("Include plant sterols")
    sterols_dose = st.slider("Dose (g/day)", 0.6, 3.3, 2.0, step=0.1,
                             disabled=not sterols_on)

    fiber_on = st.checkbox("Include soluble fiber")
    fiber_dose = st.number_input(
        "Fiber (g/day)",
        min_value=0.0,
        max_value=8.0,
        value=5.0,
        step=0.5,
        disabled=not fiber_on,
    )
    if fiber_on:
        st.caption("Fiber estimates are capped at the practical evidence range of 8 g/day.")

    st.markdown("---")
    st.markdown("**Lifestyle**")
    weight_loss_on = st.checkbox("Include weight loss")
    weight_loss_lb = st.number_input(
        "Weight to lose (lb)",
        min_value=0,
        max_value=60,
        value=10,
        step=1,
        disabled=not weight_loss_on,
    )
    exercise_on = st.checkbox("Include aerobic / combined exercise")

# ── Compute predictions ──────────────────────────────────────────────────────
predictions = []   # list of predict() dicts, in fixed order
layer_labels = []  # human-readable name per prediction

if statin_choice != "None":
    m = models[statin_choice]
    predictions.append(predict(m["idata"], m["data"], baseline_ldl=baseline_ldl))
    layer_labels.append(statin_choice)

if ezetimibe_on:
    m = models["Ezetimibe 10 mg"]
    predictions.append(predict(m["idata"], m["data"], baseline_ldl=baseline_ldl))
    layer_labels.append("Ezetimibe 10 mg")

if pcsk9_on:
    m = models["PCSK9 inhibitor"]
    predictions.append(predict(m["idata"], m["data"], baseline_ldl=baseline_ldl))
    layer_labels.append("PCSK9 inhibitor")

if portfolio_on:
    portfolio_key = (
        "Portfolio diet (strict)"
        if portfolio_choice == "Strict efficacy trial"
        else "Portfolio diet (real-world)"
    )
    m = models[portfolio_key]
    predictions.append(predict(m["idata"], m["data"], baseline_ldl=baseline_ldl))
    layer_labels.append(portfolio_key)

if sterols_on:
    m = models["plant_sterols"]
    predictions.append(predict(m["idata"], m["data"],
                               baseline_ldl=baseline_ldl, dose_query=sterols_dose))
    layer_labels.append(f"Plant sterols {sterols_dose:.1f} g/day")

if fiber_on:
    m = models["fiber"]
    predictions.append(predict(m["idata"], m["data"],
                               baseline_ldl=baseline_ldl, unit_dose=fiber_dose))
    layer_labels.append(f"Soluble fiber {fiber_dose:.1f} g/day")

if weight_loss_on:
    m = models["weight_loss"]
    weight_loss_kg = weight_loss_lb * 0.4536
    predictions.append(predict(m["idata"], m["data"],
                               baseline_ldl=baseline_ldl, unit_dose=weight_loss_kg))
    layer_labels.append(f"Weight loss {weight_loss_lb} lb")

if exercise_on:
    m = models["exercise"]
    predictions.append(predict(m["idata"], m["data"], baseline_ldl=baseline_ldl))
    layer_labels.append("Aerobic/combined exercise")

# ── Outputs ──────────────────────────────────────────────────────────────────
with col_out:
    st.subheader("Results")

    if not predictions:
        st.info(
            "Select at least one intervention on the left to see a prediction. "
            "Example: choose a statin, add plant sterols, or include aerobic exercise."
        )
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

        st.markdown(
            f"**Summary:** Your LDL is predicted to move from "
            f"**{baseline_ldl:.0f}** to about **{final_mean:.1f} mg/dL**, "
            f"with an estimated **{rrr_mean:.1f}% relative cardiovascular risk reduction**."
        )

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
                delta=f"Likely range {rrr_lo:.1f}-{rrr_hi:.1f}%",
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
                    delta=f"Likely range {arr_lo:.1f}-{arr_hi:.1f} pp",
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
        # Grow the reduction bar outward from the baseline end so the animation
        # reads as "starting LDL moving toward the predicted value".
        reduction_origin = "right" if mean_pos < baseline_pos else "left"

        st.markdown(
            f"""
            <div class="ldl-anim-card" style="
                margin: 1.2rem 0 1.4rem 0;
                padding: 1.15rem 1.2rem 1rem 1.2rem;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                background: #ffffff;
                animation: ldlFadeUp .5s ease both;
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
                <div class="ldl-anim-bar" style="
                    position: absolute;
                    left: {reduction_left:.2f}%;
                    width: {reduction_width:.2f}%;
                    top: 24px;
                    height: 12px;
                    border-radius: 999px;
                    background: {reduction_gradient};
                    opacity: 0.82;
                    transform-origin: {reduction_origin};
                    animation: ldlGrowX .6s .12s cubic-bezier(.22,.61,.36,1) both;
                "></div>
                <div class="ldl-anim-band" style="
                    position: absolute;
                    left: {lo_pos:.2f}%;
                    width: {hi_pos - lo_pos:.2f}%;
                    top: 21px;
                    height: 18px;
                    border-radius: 999px;
                    background: rgba(18, 103, 130, 0.16);
                    border: 1px solid rgba(18, 103, 130, 0.22);
                    transform-origin: center;
                    animation: ldlGrowX .55s .18s ease-out both;
                "></div>
                <div class="ldl-anim-marker" style="
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
                    animation: ldlPop .5s .34s cubic-bezier(.22,.61,.36,1) both;
                "></div>
                <div style="
                    position: absolute;
                    left: {baseline_pos:.2f}%;
                    top: 16px;
                    width: 0;
                    height: 26px;
                    border-left: 2px dashed #475569;
                "></div>
                <div class="ldl-anim-fade" style="
                    position: absolute;
                    left: {mean_pos:.2f}%;
                    top: 47px;
                    transform: translateX(-50%);
                    color: #126782;
                    font-size: 0.88rem;
                    font-weight: 700;
                    white-space: nowrap;
                    animation: ldlFadeIn .4s .42s ease both;
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
                "Ezetimibe and PCSK9 inhibitor estimates come from trials where patients were "
                "already taking statins, so the app only enables them after a statin is selected. "
                "Portfolio diet estimates were measured on top of an NCEP Step II diet background. "
                "Weight-loss effect is from a severely obese population (mean BMI ~36); "
                "users with normal or mildly elevated BMI may see a smaller LDL effect. "
                "Weight loss achieved through diet or exercise may overlap with those "
                "interventions if also selected, which can double-count some benefit. "
                "Fiber effect uses the practical dose range (<=8 g/day) and a "
                "higher-baseline trial population; absolute effect may be smaller at "
                "lower baseline LDL. "
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
                "interval by only ~1 percentage point. "
                "This tool is for education and portfolio demonstration only, not medical advice; "
                "treatment decisions should be made with a licensed clinician."
            )
