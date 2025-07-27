# Job-Align

Job-Align is an AI-powered job application assistant that helps users find job opportunities tailored to their resumes. Using NLP and keyword extraction, it intelligently matches user skills with relevant job listings. It also features user authentication, job search, and a foundation for future tools like application tracking and cover letter generation.

## 🔍 Features

- 🔐 **User Authentication** – Secure signup and login.
- 📄 **Resume Parsing** – Upload your resume and extract key skills/technologies using NLP.
- 💼 **AI-Based Job Matching** – Get job suggestions based on resume content.
- 🔎 **Keyword Search** – Search for jobs by keywords and categories.
- 🧾 **Job Tracker** *(Coming Soon)* – Track saved jobs and application status.
- 📝 **Cover Letter Generator** *(Planned)* – Auto-generate tailored cover letters using AI.

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **AI/NLP Tools:** (e.g. spaCy, or custom extractors)
- **Authentication:** Flask-Login (depending on implementation)

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- Flask
- Virtual environment tool like `venv`

### 📦 Installation

```bash
git clone https://github.com/Shirinpandey/Job-Align.git
cd Job-Align

python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate

pip install -r requirements.txt

flask run
