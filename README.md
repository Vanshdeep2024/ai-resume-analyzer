# AI-Powered Resume Analyzer & Job Matching System

An AI-powered web application that analyzes resumes and evaluates them for ATS readiness, technical skills, career-role compatibility, and job-description matching.

## 🚀 Features

- 📄 PDF Resume Upload
- ⭐ Overall Resume Score
- 🤖 ATS-Friendly Resume Score
- 🎯 Target Job Role Matching
- 🛠️ Technical Skill Detection
- 💪 Resume Strength Analysis
- ⚠️ Resume Weakness Detection
- 🎯 Multiple Career Role Compatibility
- 📌 Job Description Matching
- ✅ Matched Job Keywords
- ❌ Missing Job Keywords
- 📊 Resume Performance Charts
- 📋 Resume Statistics
- 💡 Personalized Resume Recommendations
- 📄 Extracted Resume Text Preview

## 💼 Supported Career Domains

- AI / Machine Learning
- Data Science
- Data Analytics
- Cybersecurity
- Web Development
- Frontend Development
- Backend Development
- Software Development
- Android Development
- Cloud / DevOps
- Database / SQL Development

## 🛠️ Technologies Used

- Python
- Streamlit
- PyPDF2
- Pandas
- Matplotlib
- Scikit-learn
- TF-IDF
- Cosine Similarity
- Regular Expressions

## 🧠 How It Works

1. User uploads a PDF resume.
2. The application extracts text from the PDF.
3. Technical skills are detected from the extracted text.
4. ATS-related resume sections are checked.
5. The resume is compared with the selected career role.
6. Matching and missing skills are identified.
7. The resume can be compared with a job description.
8. TF-IDF and cosine similarity are used for job-description matching.
9. The system generates scores, strengths, weaknesses and recommendations.

## ▶️ How to Run

### 1. Install Python

Make sure Python is installed on your system.

### 2. Install required libraries

```bash
pip install -r requirements.txt