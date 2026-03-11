# pdf_reader.py — Extracts raw text from PDF resumes

import pdfplumber

def read_pdf(file_path):
    
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
    
    return text.strip()