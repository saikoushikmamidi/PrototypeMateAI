import streamlit as st
from ai_engine import analyze_idea
from classifier import classify_idea
from demo_inputs import DEMO_IDEAS
from utils import (
    calculate_score,
    estimate_cost,
    format_plan_text,
    generate_pdf
)

st.set_page_config(page_title="PrototypeMate AI", layout="wide")

st.title("🚀 PrototypeMate AI")
st.subheader("AI-Powered Rapid Prototype Requirement Analyzer")

idea = st.text_area("Describe your idea")

demo = st.selectbox("Or try a demo idea", ["None"] + list(DEMO_IDEAS.keys()))
if demo != "None":
    idea = DEMO_IDEAS[demo]

if st.button("Analyze & Generate Prototype Plan"):
    if not idea.strip():
        st.warning("Please enter an idea")
    else:
        with st.spinner("Analyzing idea with AI..."):
            domain, complexity = classify_idea(idea)
            result = analyze_idea(idea, domain, complexity)
            score = calculate_score(result, complexity)
            cost = estimate_cost(complexity)

        st.success("Analysis Complete")

        # ---------------- METRICS ----------------
        st.metric("Requirement Clarity Score", f"{score}%")
        st.metric("Estimated Cost", cost)

        # ---------------- CORE SECTIONS ----------------
        st.header("🧩 Problem Statement")
        st.write(result["problem_statement"])

        st.header("👥 Target Users")
        st.write(result["target_users"])

        st.header("📌 MVP Features")
        st.write(result["mvp_features"])

        st.header("🛠 Tech Stack")
        st.write(result["tech_stack"])

        st.header("⏳ Timeline")
        st.write(result["timeline"])

        st.header("📊 Success Metrics")
        st.write(result["success_metrics"])

        st.header("⚠ Risks")
        st.write(result["risks"])

        st.header("❓ Missing Requirements")
        st.write(result["missing_requirements"])

        st.header("🚀 Future Enhancements")
        st.write(result["future_enhancements"])

        st.header("🔗 Reference Links")
        st.write(result["reference_links"])

        st.header("🧾 Executive Summary")
        st.write(result["executive_summary"])

        # ---------------- DOWNLOADS ----------------
        plan_text = format_plan_text(
            idea, domain, complexity, result, score, cost
        )

        st.download_button(
            "📄 Download Plan (Text)",
            plan_text,
            "prototype_plan.txt"
        )

        st.download_button(
            "📄 Download Plan (PDF)",
            generate_pdf(plan_text),
            "prototype_plan.pdf"
        )
