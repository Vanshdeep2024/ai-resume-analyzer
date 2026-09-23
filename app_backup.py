import streamlit as st
import re
from pypdf import PdfReader


# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)


# --------------------------------
# TITLE
# --------------------------------

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and get an instant AI-based resume analysis."
)


# --------------------------------
# SKILLS DATABASE
# --------------------------------

skills_list = [
    "python",
    "java",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "numpy",
    "pandas",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "computer vision",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "power bi",
    "excel"
]


# --------------------------------
# RESUME SECTIONS
# --------------------------------

sections = {
    "Education": [
        "education",
        "university",
        "college",
        "degree",
        "b.tech",
        "btech",
        "bachelor"
    ],

    "Experience": [
        "experience",
        "work experience",
        "employment",
        "internship"
    ],

    "Projects": [
        "projects",
        "project"
    ],

    "Certifications": [
        "certification",
        "certifications",
        "certificate"
    ],

    "Skills": [
        "skills",
        "technical skills",
        "technologies"
    ]
}


# --------------------------------
# PDF UPLOAD
# --------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload your Resume (PDF)",
    type=["pdf"]
)


# --------------------------------
# ANALYSIS
# --------------------------------

if uploaded_file is not None:

    st.success("✅ Resume uploaded successfully!")

    # Read PDF
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"


    # Convert to lowercase
    text_lower = text.lower()


    # --------------------------------
    # SKILL DETECTION
    # --------------------------------

    detected_skills = []

    for skill in skills_list:

        if skill in text_lower:

            detected_skills.append(skill)


    # --------------------------------
    # SECTION DETECTION
    # --------------------------------

    detected_sections = {}

    for section, keywords in sections.items():

        found = False

        for keyword in keywords:

            if keyword in text_lower:

                found = True
                break

        detected_sections[section] = found


    # --------------------------------
    # CONTACT INFORMATION
    # --------------------------------

    email_found = bool(
        re.search(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            text
        )
    )

    phone_found = bool(
        re.search(
            r'(\+91[\-\s]?)?[6-9]\d{9}',
            text
        )
    )


    # --------------------------------
    # SCORE CALCULATION
    # --------------------------------

    score = 0


    # Skills
    if len(detected_skills) >= 5:
        score += 20

    elif len(detected_skills) >= 3:
        score += 15

    elif len(detected_skills) >= 1:
        score += 10


    # Sections
    for found in detected_sections.values():

        if found:
            score += 10


    # Contact
    if email_found:
        score += 5

    if phone_found:
        score += 5


    # Maximum possible from above = 80
    # Add base points
    score = min(score + 20, 100)


    # --------------------------------
    # RESULTS
    # --------------------------------

    st.divider()

    st.header("📊 Resume Analysis")


    # Score
    st.metric(
        "Overall Resume Score",
        f"{score}/100"
    )


    # --------------------------------
    # SCORE MESSAGE
    # --------------------------------

    if score >= 80:

        st.success(
            "🌟 Strong resume! Your resume contains most important sections."
        )

    elif score >= 60:

        st.warning(
            "👍 Good resume, but there is room for improvement."
        )

    else:

        st.error(
            "⚠️ Your resume needs improvement."
        )


    # --------------------------------
    # CONTACT INFORMATION
    # --------------------------------

    st.subheader("📞 Contact Information")

    col1, col2 = st.columns(2)

    with col1:

        if email_found:
            st.success("✅ Email Found")
        else:
            st.error("❌ Email Missing")

    with col2:

        if phone_found:
            st.success("✅ Phone Found")
        else:
            st.error("❌ Phone Missing")


    # --------------------------------
    # RESUME SECTIONS
    # --------------------------------

    st.subheader("📑 Resume Sections")

    for section, found in detected_sections.items():

        if found:

            st.success(
                f"✅ {section}"
            )

        else:

            st.warning(
                f"⚠️ {section} Missing"
            )


    # --------------------------------
    # SKILLS
    # --------------------------------

    st.subheader("💻 Skills Detected")

    if detected_skills:

        st.write(
            ", ".join(
                skill.title()
                for skill in detected_skills
            )
        )

    else:

        st.warning(
            "No technical skills detected."
        )


    # --------------------------------
    # RESUME STATISTICS
    # --------------------------------

    st.subheader("📈 Resume Statistics")

    words = text.split()

    characters = len(text)

    word_count = len(words)

    page_count = len(reader.pages)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Pages",
            page_count
        )

    with col2:

        st.metric(
            "Words",
            word_count
        )

    with col3:

        st.metric(
            "Characters",
            characters
        )


    # --------------------------------
    # SUGGESTIONS
    # --------------------------------

    st.subheader("💡 Suggestions")

    suggestions = []


    if not detected_sections["Projects"]:

        suggestions.append(
            "Add a Projects section with 2–3 relevant projects."
        )


    if not detected_sections["Certifications"]:

        suggestions.append(
            "Add relevant certifications or courses."
        )


    if not detected_sections["Experience"]:

        suggestions.append(
            "Add internship, training or practical experience."
        )


    if len(detected_skills) < 5:

        suggestions.append(
            "Add more relevant technical skills."
        )


    if not email_found:

        suggestions.append(
            "Add a professional email address."
        )


    if not phone_found:

        suggestions.append(
            "Add your contact number."
        )


    if suggestions:

        for suggestion in suggestions:

            st.info(
                "💡 " + suggestion
            )

    else:

        st.success(
            "🎉 Your resume looks well structured!"
        )


    # --------------------------------
    # TEXT PREVIEW
    # --------------------------------

    with st.expander("👀 View Extracted Resume Text"):

        st.text(
            text[:5000]
        )


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "AI Resume Analyzer • Python • NLP • Streamlit"
)