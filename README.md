# Automated Resume Parser
> Python · pandas · spaCy · NLP

NLP-based system to extract structured information from resumes automatically. Implements a document processing pipeline for parsing resumes in PDF and DOCX formats. Achieves 85–90% extraction accuracy.

## Features
- Extracts **13 fields** — name, email, phone, LinkedIn, GitHub, summary, skills, education, experience, projects, certifications, awards, and societies
- Supports **PDF and DOCX** formats via pdfplumber and python-docx
- **spaCy NER** for intelligent name detection
- **Regex pipelines** for contact details and URLs
- **100+ skill matching** across languages, frameworks, ML/AI tools
- REST API + drag-and-drop web interface

## Setup
```bash
git clone https://github.com/palak-yadav01/resume-parser.git
cd resume-parser
python -m venv venv && venv\Scripts\activate
pip install spacy pdfplumber python-docx pandas flask flask-cors
python -m spacy download en_core_web_sm
python app.py
Open index.html → upload resume → instant structured output.
API
POST /parse   →  multipart/form-data (PDF or DOCX)  →  JSON
GET  /health  →  server status
Stack
Python 3.11 spaCy pdfplumber python-docx pandas Flask
## SCREENSHOTS
<img width="1664" height="815" alt="Screenshot 2026-03-11 182220" src="https://github.com/user-attachments/assets/89a4158c-9a8d-4f33-987c-595db8520001" />
<img width="1643" height="916" alt="Screenshot 2026-03-11 182122" src="https://github.com/user-attachments/assets/28bfaeaf-88c3-4bec-a0fd-76fa97ea8ec8" />

Author
Palak Yadav — github.com/palak-yadav01
