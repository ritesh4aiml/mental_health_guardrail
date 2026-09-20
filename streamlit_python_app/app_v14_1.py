
import re, json, time
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Mental Health Guardrail Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CONFIG
# ============================================================
DEFAULT_MODERATE = 0.35
DEFAULT_HIGH = 0.65
DEFAULT_CRITICAL = 0.85

HIGH_PATTERNS = [
    r"\bi want to die\b", r"\bi want to kill myself\b", r"\bkill myself\b",
    r"\bend my life\b", r"\bsuicide\b", r"\bsuicidal\b",
    r"\bno reason to live\b", r"\bbetter off dead\b",
    r"\bi can't go on\b", r"\bi cannot go on\b"
]
CRITICAL_PATTERNS = [
    r"\bi have a plan\b", r"\bhave a specific plan\b",
    r"\bgoing to kill myself\b", r"\bgoing to end my life\b",
    r"\babout to kill myself\b", r"\btonight i will\b",
    r"\btonight i am going to\b", r"\bhave the means\b"
]
DISTRESS_TERMS = [
    "hopeless", "worthless", "alone", "overwhelmed", "can't cope",
    "cannot cope", "depressed", "anxious", "panic", "helpless"
]

DEMOS = {
    "🟢 Everyday question": "What are some ways to improve my sleep quality?",
    "🟡 Emotional distress": "I have been feeling very low, overwhelmed and alone lately.",
    "🟠 High-risk": "I feel hopeless and I want to kill myself. I don't see a reason to live.",
    "🔴 Critical": "I have a specific plan to kill myself tonight and I have the means."
}

if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ============================================================
# LOGIC
# ============================================================
def find_patterns(text):
    text = text.lower()
    high = [p for p in HIGH_PATTERNS if re.search(p, text)]
    critical = [p for p in CRITICAL_PATTERNS if re.search(p, text)]
    distress = [x for x in DISTRESS_TERMS if x in text]
    return high, critical, distress

def demo_classifier_score(text):
    high, critical, distress = find_patterns(text)
    if critical:
        return 0.97
    if high:
        return 0.82
    return min(0.10 + 0.10 * len(distress), 0.58)

def assess(text, moderate_t, high_t, critical_t):
    model_score = demo_classifier_score(text)
    high, critical, distress = find_patterns(text)
    rule_score = 0.99 if critical else (0.90 if high else 0.0)
    final = max(model_score, rule_score)

    if final >= critical_t:
        tier = "CRITICAL"
    elif final >= high_t:
        tier = "HIGH"
    elif final >= moderate_t:
        tier = "MODERATE"
    else:
        tier = "NONE"

    return {
        "text": text,
        "model_score": model_score,
        "rule_score": rule_score,
        "final_score": final,
        "tier": tier,
        "high_hits": high,
        "critical_hits": critical,
        "distress_hits": distress,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def baseline_response(text):
    return ("Thank you for sharing this. It may help to pause, identify what is making "
            "the situation difficult, and consider a small practical next step. If the "
            "distress is significant, speaking with someone you trust can help.")

def guarded_response(result):
    tier = result["tier"]
    if tier == "CRITICAL":
        return ("Your message indicates an immediate safety concern. Please move away "
                "from anything you could use to hurt yourself and contact local emergency "
                "services or an appropriate crisis service now. If possible, stay with a "
                "trusted person and tell them directly that you need immediate support.")
    if tier == "HIGH":
        return ("I'm concerned about the level of distress in your message. Please seek "
                "immediate support from a trusted person, qualified mental-health professional, "
                "or appropriate local crisis/emergency service. Avoid being alone if you may be at risk.")
    if tier == "MODERATE":
        return ("It sounds like you may be under significant emotional pressure. Consider "
                "talking with someone you trust and contacting a qualified mental-health "
                "professional if these feelings persist or become harder to manage.")
    return baseline_response(result["text"])

def tier_description(tier):
    return {
        "NONE": "No meaningful elevated-risk signal was detected.",
        "MODERATE": "Possible emotional distress; supportive follow-up is appropriate.",
        "HIGH": "Strong safety indicators; immediate human support should be encouraged.",
        "CRITICAL": "Immediate safety concern; urgent emergency/crisis support should be prioritized."
    }[tier]

def gauge(score):
    # simple horizontal gauge using matplotlib
    fig, ax = plt.subplots(figsize=(9, 1.2))
    ax.barh([0], [1], height=.42)
    ax.barh([0], [score], height=.42)
    ax.axvline(DEFAULT_MODERATE, linestyle="--", linewidth=1)
    ax.axvline(DEFAULT_HIGH, linestyle="--", linewidth=1)
    ax.axvline(DEFAULT_CRITICAL, linestyle="--", linewidth=1)
    ax.set_xlim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Guard score")
    ax.set_title(f"Final risk score: {score:.3f}")
    fig.tight_layout()
    return fig

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.title("🛡️ Guardrail Lab")
    page = st.radio(
        "Explore",
        ["Live Assessment", "Dashboard", "Architecture", "Dataset Explorer",
         "Evaluation Lab", "Thesis View", "Safety & Limitations"]
    )

    st.divider()
    st.subheader("Live thresholds")
    moderate_t = st.slider("Moderate threshold", 0.10, 0.80, DEFAULT_MODERATE, 0.01)
    high_t = st.slider("High threshold", moderate_t + 0.05, 0.95, DEFAULT_HIGH, 0.01)
    critical_t = st.slider("Critical threshold", high_t + 0.05, 0.99, DEFAULT_CRITICAL, 0.01)

    st.caption("Changing these sliders immediately changes tier assignment. "
               "The demo scorer is intentionally transparent; connect your trained model for final thesis runs.")

# ============================================================
# HEADER
# ============================================================
st.title("🛡️ Dual-Model Mental-Health Guardrail")
st.caption("Interactive research dashboard — baseline generation + risk detection + rule-based safety net + tiered escalation")

if page == "Live Assessment":
    st.header("🔎 Live message assessment")
    st.write("Test a message and watch the complete safety pipeline update dynamically.")

    left, right = st.columns([1.35, 1], gap="large")

    with left:
        demo = st.selectbox("Try a prepared scenario", ["Custom"] + list(DEMOS.keys()))
        text_default = "" if demo == "Custom" else DEMOS[demo]
        text = st.text_area(
            "Message to analyse",
            value=text_default,
            height=170,
            placeholder="Enter a mental-health message..."
        )

        a, b, c = st.columns(3)
        with a:
            run = st.button("🚀 Analyse", type="primary", use_container_width=True)
        with b:
            clear = st.button("🧹 Clear", use_container_width=True)
        with c:
            if st.button("🎲 Random demo", use_container_width=True):
                text = list(DEMOS.values())[len(st.session_state.history) % len(DEMOS)]

        if clear:
            st.session_state.last_result = None
            st.rerun()

        if run and text.strip():
            result = assess(text, moderate_t, high_t, critical_t)
            st.session_state.last_result = result
            st.session_state.history.append(result)

    result = st.session_state.last_result

    with right:
        st.subheader("Pipeline status")
        steps = [
            ("1", "Message", bool(text.strip())),
            ("2", "Classifier", result is not None),
            ("3", "Rule net", result is not None),
            ("4", "Risk fusion", result is not None),
            ("5", "Escalation", result is not None),
            ("6", "Response", result is not None),
        ]
        for n, label, done in steps:
            st.write(("✅" if done else "⏳") + f"  **{n}. {label}**")

    if result:
        st.divider()
        st.subheader("📊 Dynamic risk result")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Classifier", f"{result['model_score']:.3f}")
        m2.metric("Rule override", f"{result['rule_score']:.3f}")
        m3.metric("Final score", f"{result['final_score']:.3f}")
        m4.metric("Tier", result["tier"])

        st.pyplot(gauge(result["final_score"]), use_container_width=True)
        st.info(tier_description(result["tier"]))

        ev1, ev2 = st.columns(2)
        with ev1:
            st.markdown("### 🔬 Evidence detected")
            st.write("Explicit high-risk:", result["high_hits"] or "None")
            st.write("Imminent-risk:", result["critical_hits"] or "None")
            st.write("Distress terms:", result["distress_hits"] or "None")
        with ev2:
            st.markdown("### 🧮 Score composition")
            st.write(f"Model contribution: **{result['model_score']:.3f}**")
            st.write(f"Rule contribution: **{result['rule_score']:.3f}**")
            st.write(f"Final = max(model, rule): **{result['final_score']:.3f}**")

        st.divider()
        before, after = st.columns(2)
        with before:
            st.subheader("Before — baseline")
            st.info(baseline_response(result["text"]))
        with after:
            st.subheader("After — guarded")
            st.warning(guarded_response(result))

        audit = json.dumps(result, indent=2)
        st.download_button("⬇️ Export this assessment as JSON", audit,
                           file_name="guardrail_assessment.json",
                           mime="application/json")

elif page == "Dashboard":
    st.header("📈 Interactive dashboard")
    hist = pd.DataFrame(st.session_state.history)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Assessments", len(hist))
    c2.metric("Average score", f"{hist.final_score.mean():.3f}" if len(hist) else "—")
    c3.metric("High/Critical", int(hist.tier.isin(["HIGH","CRITICAL"]).sum()) if len(hist) else 0)
    c4.metric("Critical", int((hist.tier=="CRITICAL").sum()) if len(hist) else 0)

    if len(hist):
        st.subheader("Live assessment history")
        st.dataframe(hist[["timestamp","tier","model_score","rule_score","final_score","text"]],
                     use_container_width=True, hide_index=True)

        left, right = st.columns(2)
        with left:
            st.subheader("Score trajectory")
            chart = hist.reset_index()
            st.line_chart(chart, x="index", y="final_score")
        with right:
            st.subheader("Tier distribution")
            st.bar_chart(hist["tier"].value_counts())

        st.download_button("⬇️ Export history CSV",
                           hist.to_csv(index=False),
                           file_name="guardrail_history.csv",
                           mime="text/csv")
    else:
        st.info("Run a few assessments on the Live Assessment page to populate this dashboard.")
        st.markdown("### Suggested interactive sequence")
        st.write("1. Test a normal message → 2. test distress → 3. test high-risk → 4. change thresholds → 5. test again.")

elif page == "Architecture":
    st.header("🏗️ Explore the architecture")
    st.write("Use the controls below to reveal how each layer contributes to the final decision.")

    layers = {
        "1 — Dataset & preprocessing": "Loads dialogue records, normalizes text, validates fields, records exclusions and prepares train/validation/test data.",
        "2 — Qwen response layer": "Generates the baseline natural-language response.",
        "3 — RoBERTa risk layer": "Estimates elevated safety risk from the user's message.",
        "4 — Rule-based safety net": "Searches for explicit high-risk and imminent-risk expressions.",
        "5 — Risk fusion": "Combines model confidence and explicit rule evidence.",
        "6 — Escalation engine": "Maps the final score to NONE, MODERATE, HIGH or CRITICAL.",
        "7 — Guarded response": "Uses the tier to determine the safety-oriented response strategy.",
        "8 — Evaluation": "Measures classification performance, missed risk, over-escalation and response behavior."
    }
    selected = st.select_slider("Move through the pipeline", options=list(layers.keys()))
    for key in layers:
        if list(layers).index(key) <= list(layers).index(selected):
            st.success(f"**{key}** — {layers[key]}")

    st.subheader("System flow")
    st.graphviz_chart("""
    digraph {
      rankdir=LR;
      node [shape=box, style="rounded,filled", fillcolor="#eef2ff"];
      A[label="MHDialog"];
      B[label="Preprocessing"];
      C[label="Qwen baseline"];
      D[label="RoBERTa risk"];
      E[label="Rule safety net"];
      F[label="Risk fusion"];
      G[label="NONE / MODERATE / HIGH / CRITICAL"];
      H[label="Guarded response"];
      I[label="Evaluation"];
      A->B; B->C; B->D; B->E; D->F; E->F; F->G; G->H; C->I; H->I;
    }
    """)

elif page == "Dataset Explorer":
    st.header("🗃️ Dataset Explorer & EDA")
    st.write("The project uses the IkeZhang/MHDialog dataset. Upload your prepared CSV to reproduce the notebook-style EDA interactively.")

    uploaded = st.file_uploader("Upload prepared dataset CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.success(f"Loaded {len(df):,} records and {len(df.columns)} columns.")
        st.dataframe(df.head(25), use_container_width=True)

        c1,c2 = st.columns(2)
        with c1:
            col = st.selectbox("Distribution column", df.columns)
            st.bar_chart(df[col].astype(str).value_counts().head(20))
        with c2:
            st.subheader("Missing values")
            miss = df.isna().sum().sort_values(ascending=False).head(20)
            st.bar_chart(miss)

        st.subheader("Quick statistics")
        st.write(df.describe(include="all").T)
        st.download_button("⬇️ Download cleaned preview",
                           df.head(1000).to_csv(index=False),
                           file_name="dataset_preview.csv", mime="text/csv")
    else:
        st.info("No CSV uploaded yet.")
        st.markdown("### Dataset fields used in the project")
        st.table(pd.DataFrame({
            "Field": ["Dialogue", "Dialog Intent", "Concern Type", "Level"],
            "Purpose": ["Conversation content", "Dialogue intent", "Concern category", "Original risk-related label"]
        }))
        st.markdown("### Original Level categories")
        st.write("Not Related · No · Minor · Moderate · Severe · Unsure")

elif page == "Evaluation Lab":
    st.header("🧪 Evaluation Lab")
    st.write("This section makes the thesis evaluation concepts interactive rather than presenting them as static text.")

    st.subheader("Metric explorer")
    tp = st.slider("True positives (TP)", 0, 100, 70)
    fn = st.slider("False negatives (FN)", 0, 100, 10)
    fp = st.slider("False positives (FP)", 0, 100, 15)
    tn = st.slider("True negatives (TN)", 0, 100, 80)

    precision = tp/(tp+fp) if tp+fp else 0
    recall = tp/(tp+fn) if tp+fn else 0
    f1 = 2*precision*recall/(precision+recall) if precision+recall else 0
    fnr = fn/(tp+fn) if tp+fn else 0

    a,b,c,d = st.columns(4)
    a.metric("Precision", f"{precision:.3f}")
    b.metric("Recall", f"{recall:.3f}")
    c.metric("F1", f"{f1:.3f}")
    d.metric("FNR", f"{fnr:.3f}")

    st.subheader("Confusion matrix")
    cm = pd.DataFrame([[tn,fp],[fn,tp]], index=["Actual negative","Actual positive"],
                      columns=["Predicted negative","Predicted positive"])
    st.dataframe(cm, use_container_width=True)

    st.subheader("Why FNR matters")
    st.warning("For a safety-oriented system, missed high-risk cases can be especially important. "
               "Therefore recall and false-negative rate should be interpreted alongside precision and F1.")

    st.subheader("Bootstrap confidence interval concept")
    st.write("The thesis can use non-parametric bootstrap resampling of the held-out test set to quantify uncertainty. "
             "Wide intervals are expected when the test set is small; they should be reported rather than hidden.")

elif page == "Thesis View":
    st.header("🎓 Thesis presentation mode")
    st.write("A concise, viva-friendly view of the complete project.")

    tabs = st.tabs(["Problem", "Method", "Contribution", "Evaluation", "Conclusion"])
    with tabs[0]:
        st.subheader("Problem")
        st.write("General-purpose LLMs can generate fluent responses without consistently detecting or escalating safety-critical mental-health content.")
    with tabs[1]:
        st.subheader("Method")
        st.write("Experimental quantitative design using MHDialog, Qwen response generation, a RoBERTa risk classifier, a transparent rule-based safety net, risk fusion and four-tier escalation.")
    with tabs[2]:
        st.subheader("Contribution")
        st.write("A transparent hybrid guardrail architecture that combines learned risk detection with explicit safety rules and an auditable escalation policy.")
    with tabs[3]:
        st.subheader("Evaluation")
        st.write("Held-out classification metrics, high-risk recall, false-negative rate, MCC, escalation behaviour, bootstrap uncertainty and baseline-versus-guarded response analysis.")
    with tabs[4]:
        st.subheader("Conclusion")
        st.write("The system should be judged primarily by whether it reduces dangerous missed detections while keeping unnecessary escalation manageable. Results must be interpreted with dataset and sample-size limitations.")

elif page == "Safety & Limitations":
    st.header("⚠️ Safety, limitations and ethics")
    st.error("This application is a research prototype. It is not a clinical diagnostic system or an emergency/crisis service.")
    for title, body in [
        ("False negatives", "The classifier or rules may miss indirect, ambiguous or culturally varied expressions of risk."),
        ("False positives", "Explicit patterns may trigger on figurative or non-crisis language."),
        ("Calibration", "A model probability should not automatically be treated as a clinically calibrated risk probability."),
        ("Generative variability", "Qwen responses can vary between runs and should be evaluated systematically."),
        ("Dataset limitations", "Open or synthetic dialogue datasets may not represent real-world crisis populations."),
        ("Human oversight", "Any deployment requires domain, clinical and safety review."),
        ("Emergency handling", "Users in immediate danger should be directed to appropriate local emergency or crisis resources rather than relying on this research application.")
    ]:
        with st.expander(title):
            st.write(body)

st.divider()
st.caption("Research prototype • Dynamic demonstration scorer by default • Replace demo inference with the trained RoBERTa/Qwen pipeline for final thesis experiments.")
