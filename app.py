import streamlit as st
import pandas as pd
from pypdf import PdfReader

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="ATS Resume Analyser | AI Skill Matcher",
    page_icon="🔍",
    layout="wide"
)

# Title and Description
st.title("🔍 ATS Resume Analyser")
st.subheader("Deep-scan resumes against required skills in seconds.")
st.write("---")

# ==========================
# Load Skills
# ==========================
try:
    with open("skills.txt", "r", encoding="utf-8") as f:
        required_skills = [
            line.strip().lower()
            for line in f
            if line.strip()
        ]
except Exception:
    st.error("❌ 'skills.txt' file nahi mili! Kripya apne project folder me ye file banayein.")
    st.stop()

# Display Target Skills
st.subheader("🎯 Target Skills to Match")
st.info(", ".join(required_skills))

# ==========================
# PDF Upload Section
# ==========================
st.subheader("📤 Upload Resumes")
uploaded_files = st.file_uploader(
    "Drag and drop or browse PDF resumes here",
    type=["pdf"],
    accept_multiple_files=True
)

# ==========================
# Analyze Button & Logic
# ==========================
if st.button("🚀 Start Analysis"):

    results = []

    if not uploaded_files:
        st.warning("⚠️ Kripya scan karne ke liye kam se kam ek PDF resume upload karein.")
        st.stop()

    # Progress bar for visual effect
    progress = st.progress(0)

    for index, file in enumerate(uploaded_files):
        text = ""

        try:
            reader = PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            text = text.lower()
            
            # Spaces remove karna matching accurate banane ke liye
            normalized_text = text.replace(" ", "")

            matched = []
            missing = []

            for skill in required_skills:
                skill_clean = skill.lower().replace(" ", "")

                if skill_clean in normalized_text:
                    matched.append(skill)
                else:
                    missing.append(skill)

            # Score Calculation
            score = round((len(matched) / len(required_skills)) * 100, 2)

            results.append({
                "Resume Name": file.name,
                "Match Score (%)": score,
                "Matched Skills": ", ".join(matched) if matched else "None",
                "Missing Skills": ", ".join(missing) if missing else "None"
            })

        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")

        # Update progress bar
        progress.progress((index + 1) / len(uploaded_files))

    # ==========================
    # Display Results
    # ==========================
    # Sort results by higher score
    results.sort(key=lambda x: x["Match Score (%)"], reverse=True)

    st.success("✅ Scanning and Analysis Complete!")
    st.write("---")

    # Leaderboard / Ranking Table
    st.subheader("🏆 Candidate Ranking Leaderboard")
    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

    # Best Candidate Spotlight
    if results:
        best = results[0]
        st.write("---")
        st.subheader("🥇 Top Candidate Spotlight")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Highest Match Score", value=f"{best['Match Score (%)']}%")
            st.success(f"**Best Profile:** {best['Resume Name']}")
        
        with col2:
            st.markdown(f"**🟩 Matched:** {best['Matched Skills']}")
            st.markdown(f"**🟥 Missing:** {best['Missing Skills']}")

        # ==========================
        # Generate & Download Report
        # ==========================
        report = "===== ATS Resume Analyser REPORT =====\n\n"
        for i, r in enumerate(results, start=1):
            report += f"Rank #{i}\n"
            report += f"Candidate Resume : {r['Resume Name']}\n"
            report += f"Match Score      : {r['Match Score (%)']}%\n"
            report += f"Matched Skills   : {r['Matched Skills']}\n"
            report += f"Missing Skills   : {r['Missing Skills']}\n"
            report += "-" * 40 + "\n"

        st.write("---")
        st.download_button(
            label="📥 Download Full X-Ray Report",
            data=report,
            file_name="ResumeXray_Report.txt",
            mime="text/plain"
        )