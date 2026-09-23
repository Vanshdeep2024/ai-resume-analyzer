import re
from collections import Counter

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# ROLE SKILLS
# ============================================================

ROLE_SKILLS = {

    "AI / ML Engineer": [
        "python", "machine learning", "deep learning",
        "tensorflow", "pytorch", "scikit-learn",
        "numpy", "pandas", "sql", "nlp",
        "computer vision", "statistics",
        "matplotlib", "data preprocessing",
        "model training"
    ],

    "Data Scientist": [
        "python", "sql", "pandas", "numpy",
        "statistics", "machine learning",
        "data analysis", "data visualization",
        "matplotlib", "seaborn",
        "scikit-learn", "excel",
        "power bi", "tableau"
    ],

    "Data Analyst": [
        "sql", "excel", "python", "pandas",
        "numpy", "data analysis", "statistics",
        "power bi", "tableau",
        "data visualization", "dashboard",
        "matplotlib"
    ],

    "Cybersecurity Analyst": [
        "cybersecurity", "network security",
        "ethical hacking", "penetration testing",
        "nmap", "kali linux", "wireshark",
        "burp suite", "vulnerability assessment",
        "siem", "linux", "firewall",
        "cryptography", "incident response"
    ],

    "Web Developer": [
        "html", "css", "javascript", "react",
        "node.js", "express", "mongodb",
        "mysql", "sql", "rest api",
        "git", "github", "responsive design"
    ],

    "Frontend Developer": [
        "html", "css", "javascript", "react",
        "typescript", "bootstrap",
        "tailwind", "responsive design",
        "git", "github", "figma", "api"
    ],

    "Backend Developer": [
        "python", "java", "node.js",
        "express", "django", "flask",
        "sql", "mysql", "postgresql",
        "mongodb", "rest api",
        "git", "github"
    ],

    "Software Developer": [
        "python", "java", "c++", "javascript",
        "sql", "data structures",
        "algorithms", "oops",
        "git", "github", "rest api",
        "database", "testing"
    ],

    "Android Developer": [
        "java", "kotlin", "android",
        "android studio", "xml",
        "firebase", "sqlite", "api",
        "git", "github", "material design"
    ],

    "Cloud / DevOps Engineer": [
        "aws", "azure", "google cloud",
        "docker", "kubernetes", "linux",
        "jenkins", "terraform",
        "git", "github", "ci/cd",
        "cloud", "bash"
    ],

    "Database / SQL Developer": [
        "sql", "mysql", "postgresql",
        "oracle", "database", "pl/sql",
        "mongodb", "normalization",
        "joins", "stored procedures",
        "database design"
    ]
}


# ============================================================
# FUNCTIONS
# ============================================================

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_pdf_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def find_skills(text):

    text = clean_text(text)

    skills_found = []

    all_skills = set()

    for skills in ROLE_SKILLS.values():
        all_skills.update(skills)

    for skill in sorted(all_skills, key=len, reverse=True):

        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text):
            skills_found.append(skill)

    return sorted(set(skills_found))


def role_analysis(text, role):

    text = clean_text(text)

    required_skills = ROLE_SKILLS[role]

    matched = []
    missing = []

    for skill in required_skills:

        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text):
            matched.append(skill)
        else:
            missing.append(skill)

    if required_skills:
        score = round(
            len(matched) / len(required_skills) * 100
        )
    else:
        score = 0

    return score, matched, missing


def calculate_ats_score(text):

    text_lower = clean_text(text)

    sections = {

        "Contact Information": [
            "email", "phone", "linkedin", "github"
        ],

        "Summary / Objective": [
            "summary", "objective", "profile"
        ],

        "Education": [
            "education", "degree",
            "b.tech", "btech", "bachelor"
        ],

        "Skills": [
            "skills", "technical skills",
            "technologies"
        ],

        "Projects": [
            "projects", "project"
        ],

        "Experience": [
            "experience",
            "internship",
            "work experience"
        ],

        "Certifications": [
            "certification",
            "certifications",
            "certificate"
        ]
    }

    results = {}

    points = 0

    for section, keywords in sections.items():

        found = any(
            keyword in text_lower
            for keyword in keywords
        )

        results[section] = found

        if found:
            points += 1

    score = round(
        points / len(sections) * 100
    )

    # Additional ATS points

    if len(text.split()) >= 250:
        score += 5

    if "github" in text_lower:
        score += 3

    if "linkedin" in text_lower:
        score += 3

    if re.search(
        r"\b\d+%|\b\d+\+|\b\d+\s*(users|customers|projects)\b",
        text_lower
    ):
        score += 5

    score = min(score, 100)

    return score, results


def resume_statistics(text):

    words = re.findall(
        r"\b[\w+#./-]+\b",
        text
    )

    sentences = re.split(
        r"[.!?]+",
        text
    )

    lines = [
        line for line in text.splitlines()
        if line.strip()
    ]

    return {
        "Words": len(words),
        "Characters": len(text),
        "Lines": len(lines),
        "Sentences": len(
            [s for s in sentences if s.strip()]
        )
    }


def get_strengths(text, skills, ats_score):

    text_lower = clean_text(text)

    strengths = []

    if len(skills) >= 8:
        strengths.append(
            "Strong technical skill coverage"
        )

    elif len(skills) >= 4:
        strengths.append(
            "Good technical skill base"
        )

    if "project" in text_lower or "projects" in text_lower:
        strengths.append(
            "Projects section is present"
        )

    if "internship" in text_lower or "experience" in text_lower:
        strengths.append(
            "Experience or internship information is included"
        )

    if "github" in text_lower:
        strengths.append(
            "GitHub profile is mentioned"
        )

    if "linkedin" in text_lower:
        strengths.append(
            "LinkedIn profile is mentioned"
        )

    if (
        "certification" in text_lower
        or "certificate" in text_lower
    ):
        strengths.append(
            "Certifications are included"
        )

    if re.search(
        r"\b\d+%|\b\d+\+|\b\d+\s*(users|customers|projects)\b",
        text_lower
    ):
        strengths.append(
            "Resume contains measurable achievements"
        )

    if ats_score >= 75:
        strengths.append(
            "Strong ATS-friendly structure"
        )

    return strengths


def get_weaknesses(
    text,
    skills,
    ats_score,
    sections
):

    text_lower = clean_text(text)

    weaknesses = []

    if len(text.split()) < 180:
        weaknesses.append(
            "Resume is short; add relevant achievements and project details"
        )

    if not sections["Summary / Objective"]:
        weaknesses.append(
            "Add a professional summary"
        )

    if not sections["Projects"]:
        weaknesses.append(
            "Add 2–4 relevant projects"
        )

    if not sections["Experience"]:
        weaknesses.append(
            "Add internship, training or practical experience"
        )

    if not sections["Certifications"]:
        weaknesses.append(
            "Add relevant certifications or training"
        )

    if "github" not in text_lower:
        weaknesses.append(
            "Add GitHub profile"
        )

    if "linkedin" not in text_lower:
        weaknesses.append(
            "Add LinkedIn profile"
        )

    if not re.search(
        r"\b\d+%|\b\d+\+|\b\d+\s*(users|customers|projects)\b",
        text_lower
    ):
        weaknesses.append(
            "Add measurable results to project/experience bullets"
        )

    if len(skills) < 5:
        weaknesses.append(
            "Add more relevant technical skills"
        )

    if ats_score < 60:
        weaknesses.append(
            "Improve ATS-friendly formatting and section headings"
        )

    return weaknesses


def job_similarity(resume, job):

    if not job.strip():
        return 0

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        matrix = vectorizer.fit_transform(
            [
                clean_text(resume),
                clean_text(job)
            ]
        )

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        return round(similarity * 100)

    except Exception:
        return 0


def job_keywords(resume, job):

    resume = clean_text(resume)
    job = clean_text(job)

    words = re.findall(
        r"[a-zA-Z][a-zA-Z0-9+#./-]{2,}",
        job
    )

    stop_words = {
        "the", "and", "for", "with",
        "this", "that", "are", "you",
        "will", "have", "has", "from",
        "your", "our", "into", "using",
        "years", "year", "work",
        "working", "team", "role",
        "candidate", "strong", "good"
    }

    unique_words = []

    for word in words:

        if word not in stop_words:
            if word not in unique_words:
                unique_words.append(word)

    matched = [
        word for word in unique_words
        if word in resume
    ]

    missing = [
        word for word in unique_words
        if word not in resume
    ]

    return matched[:20], missing[:20]


# ============================================================
# HEADER
# ============================================================

st.title("📄 AI Resume Analyzer")

st.write(
    "Analyze your resume for ATS score, skills, strengths, "
    "weaknesses, career roles and job-description matching."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Analysis Settings")

selected_role = st.sidebar.selectbox(
    "🎯 Select Target Role",
    list(ROLE_SKILLS.keys())
)

st.sidebar.write(
    "Supports AI/ML, Data Science, Cybersecurity, "
    "Web Development, Software, Android, Cloud/DevOps "
    "and Database roles."
)


# ============================================================
# UPLOAD RESUME
# ============================================================

uploaded_file = st.file_uploader(
    "📤 Upload your Resume PDF",
    type=["pdf"]
)


# ============================================================
# JOB DESCRIPTION
# ============================================================

st.header("🎯 Job Description Matcher")

job_description = st.text_area(
    "Paste the Job Description here (optional):",
    height=180,
    placeholder=(
        "Example: We are looking for a Python Developer "
        "with knowledge of SQL, Machine Learning, Git and REST API."
    )
)


# ============================================================
# ANALYSIS
# ============================================================

if uploaded_file is not None:

    try:

        # ----------------------------------------------------
        # PDF TEXT EXTRACTION
        # ----------------------------------------------------

        text = extract_pdf_text(
            uploaded_file
        )

        if not text.strip():

            st.error(
                "❌ No readable text found in this PDF. "
                "Please upload a text-based PDF."
            )

            st.stop()

        st.success(
            "✅ Resume uploaded successfully!"
        )


        # ----------------------------------------------------
        # BASIC ANALYSIS
        # ----------------------------------------------------

        skills = find_skills(text)

        stats = resume_statistics(text)

        ats_score, section_results = (
            calculate_ats_score(text)
        )


        # ----------------------------------------------------
        # TARGET ROLE
        # ----------------------------------------------------

        role_score, role_matched, role_missing = (
            role_analysis(
                text,
                selected_role
            )
        )


        # ----------------------------------------------------
        # OVERALL SCORE
        # ----------------------------------------------------

        skill_component = min(
            100,
            len(skills) * 5
        )

        overall_score = round(
            role_score * 0.45
            + ats_score * 0.40
            + skill_component * 0.15
        )

        overall_score = min(
            100,
            overall_score
        )


        # ====================================================
        # SCORE DASHBOARD
        # ====================================================

        st.divider()

        st.header("📊 Resume Score Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "⭐ Overall Score",
            f"{overall_score}%"
        )

        col2.metric(
            "🎯 Role Match",
            f"{role_score}%"
        )

        col3.metric(
            "🤖 ATS Score",
            f"{ats_score}%"
        )

        col4.metric(
            "🛠️ Skills Found",
            len(skills)
        )

        st.progress(
            overall_score / 100
        )


        # ====================================================
        # SCORE CHART
        # ====================================================

        st.subheader("📈 Resume Score Analysis")

        chart_data = pd.DataFrame({
            "Metric": [
                "Overall",
                "Role Match",
                "ATS"
            ],
            "Score": [
                overall_score,
                role_score,
                ats_score
            ]
        })

        fig, ax = plt.subplots(
            figsize=(8, 4)
        )

        ax.bar(
            chart_data["Metric"],
            chart_data["Score"]
        )

        ax.set_ylim(0, 100)

        ax.set_ylabel(
            "Score (%)"
        )

        ax.set_title(
            "Resume Performance"
        )

        st.pyplot(fig)

        plt.close(fig)


        # ====================================================
        # STRENGTHS / WEAKNESSES
        # ====================================================

        strengths = get_strengths(
            text,
            skills,
            ats_score
        )

        weaknesses = get_weaknesses(
            text,
            skills,
            ats_score,
            section_results
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "💪 Resume Strengths"
            )

            for item in strengths:

                st.success(
                    "✓ " + item
                )

        with col2:

            st.subheader(
                "⚠️ Resume Weaknesses"
            )

            for item in weaknesses:

                st.warning(
                    "• " + item
                )


        # ====================================================
        # SKILLS
        # ====================================================

        st.divider()

        st.header(
            "🛠️ Technical Skill Analysis"
        )

        if skills:

            st.write(
                "**Detected Skills:**"
            )

            st.write(
                ", ".join(
                    skill.title()
                    for skill in skills
                )
            )

        else:

            st.warning(
                "No skills from the current database detected."
            )


        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                f"✅ Skills Matching {selected_role}"
            )

            if role_matched:

                for skill in role_matched:

                    st.write(
                        "✓",
                        skill.title()
                    )

            else:

                st.info(
                    "No target-role skills detected."
                )


        with col2:

            st.subheader(
                f"❌ Skills Missing for {selected_role}"
            )

            if role_missing:

                for skill in role_missing:

                    st.write(
                        "•",
                        skill.title()
                    )

            else:

                st.success(
                    "Excellent! All listed role skills found."
                )


        # ====================================================
        # CAREER ROLE COMPATIBILITY
        # ====================================================

        st.divider()

        st.header(
            "🎯 Career Role Compatibility"
        )

        role_scores = {}

        for role in ROLE_SKILLS:

            score, _, _ = role_analysis(
                text,
                role
            )

            role_scores[role] = score


        role_df = pd.DataFrame(
            sorted(
                role_scores.items(),
                key=lambda x: x[1],
                reverse=True
            ),
            columns=[
                "Career Role",
                "Match Score"
            ]
        )

        st.dataframe(
            role_df,
            use_container_width=True,
            hide_index=True
        )


        fig2, ax2 = plt.subplots(
            figsize=(10, 5)
        )

        top_roles = (
            role_df
            .head(7)
            .iloc[::-1]
        )

        ax2.barh(
            top_roles["Career Role"],
            top_roles["Match Score"]
        )

        ax2.set_xlim(
            0,
            100
        )

        ax2.set_xlabel(
            "Match Score (%)"
        )

        ax2.set_title(
            "Top Career Matches"
        )

        st.pyplot(fig2)

        plt.close(fig2)


        # ====================================================
        # JOB DESCRIPTION MATCHING
        # ====================================================

        if job_description.strip():

            st.divider()

            st.header(
                "🎯 Job Description Match"
            )

            jd_score = job_similarity(
                text,
                job_description
            )

            st.metric(
                "Resume ↔ Job Similarity",
                f"{jd_score}%"
            )

            st.progress(
                jd_score / 100
            )


            matched_words, missing_words = (
                job_keywords(
                    text,
                    job_description
                )
            )


            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    "✅ Job Keywords Found"
                )

                if matched_words:

                    st.write(
                        ", ".join(
                            matched_words
                        )
                    )

                else:

                    st.info(
                        "No strong keyword overlap detected."
                    )


            with col2:

                st.subheader(
                    "❌ Job Keywords Missing"
                )

                if missing_words:

                    st.write(
                        ", ".join(
                            missing_words
                        )
                    )

                else:

                    st.success(
                        "Most detected keywords are present."
                    )


        # ====================================================
        # ATS SECTION CHECK
        # ====================================================

        st.divider()

        st.header(
            "🤖 ATS Section Check"
        )

        section_df = pd.DataFrame({

            "Resume Section":
                list(section_results.keys()),

            "Status": [
                "✅ Detected"
                if value
                else "❌ Missing"

                for value
                in section_results.values()
            ]
        })

        st.dataframe(
            section_df,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # RESUME STATISTICS
        # ====================================================

        st.divider()

        st.header(
            "📋 Resume Statistics"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Words",
            stats["Words"]
        )

        c2.metric(
            "Characters",
            stats["Characters"]
        )

        c3.metric(
            "Lines",
            stats["Lines"]
        )

        c4.metric(
            "Sentences",
            stats["Sentences"]
        )


        # ====================================================
        # RECOMMENDATIONS
        # ====================================================

        st.divider()

        st.header(
            "💡 Personalized Recommendations"
        )

        recommendations = []

        if role_score < 50:

            recommendations.append(
                f"Add more skills and projects related to {selected_role}."
            )

        elif role_score < 75:

            recommendations.append(
                f"Strengthen your {selected_role} profile "
                "by adding missing role-specific skills."
            )

        else:

            recommendations.append(
                f"Your resume has strong alignment with {selected_role}."
            )


        if ats_score < 60:

            recommendations.append(
                "Improve ATS structure using standard headings "
                "such as Skills, Projects, Education and Experience."
            )


        if stats["Words"] < 250:

            recommendations.append(
                "Add concise project achievements and measurable outcomes."
            )


        if "github" not in clean_text(text):

            recommendations.append(
                "Add a GitHub profile to showcase your projects."
            )


        if "linkedin" not in clean_text(text):

            recommendations.append(
                "Add your LinkedIn profile."
            )


        for recommendation in recommendations:

            st.info(
                "💡 " + recommendation
            )


        # ====================================================
        # RESUME PREVIEW
        # ====================================================

        st.divider()

        st.header(
            "📄 Resume Preview"
        )

        with st.expander(
            "View Extracted Resume Text"
        ):

            st.text_area(
                "Extracted Text",
                text,
                height=350
            )


    except Exception as e:

        st.error(
            "❌ Error while analyzing the resume."
        )

        st.exception(e)


else:

    st.info(
        "👆 Upload a PDF resume above to start analysis."
    )

    st.markdown("""
    ### 🚀 Features

    ✅ Overall Resume Score  
    ✅ ATS Score  
    ✅ Target Role Matching  
    ✅ Technical Skill Detection  
    ✅ Resume Strengths  
    ✅ Resume Weaknesses  
    ✅ Career Role Compatibility  
    ✅ Job Description Matching  
    ✅ Missing Job Keywords  
    ✅ ATS Section Check  
    ✅ Resume Statistics  
    ✅ Personalized Recommendations  
    ✅ Resume Text Preview  

    **Supported domains:**

    AI/ML • Data Science • Data Analytics • Cybersecurity •
    Web Development • Frontend • Backend • Software Development •
    Android • Cloud/DevOps • Database/SQL
    """)
 # ====================================================
# PERSONALIZED IMPROVEMENTS
# ====================================================

st.divider()

st.header("🔮 Personalized Improvements")

improvements = []

# Use resume text safely
resume_text = ""

if "text" in locals():
    resume_text = text.lower()

# GitHub
if resume_text and "github" not in resume_text:
    improvements.append(
        "Add your GitHub profile to showcase your technical projects."
    )

# LinkedIn
if resume_text and "linkedin" not in resume_text:
    improvements.append(
        "Add your LinkedIn profile for a stronger professional presence."
    )

# ATS
if "ats_score" in locals() and ats_score < 70:
    improvements.append(
        "Improve ATS compatibility by using clear headings, relevant keywords "
        "and simple formatting."
    )

# Projects
if "section_results" in locals():
    if not section_results.get("Projects", False):
        improvements.append(
            "Add 2–4 relevant projects with technologies used and measurable results."
        )

# Experience
if "section_results" in locals():
    if not section_results.get("Experience", False):
        improvements.append(
            "Add internship, training, freelance or practical experience if available."
        )

# Achievement-based descriptions
if resume_text and not re.search(r"\b\d+%", resume_text):
    improvements.append(
        "Strengthen project descriptions by adding measurable results "
        "such as accuracy, performance improvement or number of users."
    )

# Display
if improvements:
    for i, improvement in enumerate(improvements, 1):
        st.info(f"💡 {i}. {improvement}")
else:
    st.success(
        "🎉 Your resume looks strong! No major improvements detected."
    )