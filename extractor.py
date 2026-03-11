import re
import spacy

nlp = spacy.load("en_core_web_sm")

SECTION_HEADERS = {
    'summary':        ['summary', 'objective', 'career objective', 'profile',
                       'about me', 'introduction', 'professional summary',
                       'about', 'overview', 'personal statement'],
    'skills':         ['skills', 'technical skills', 'technologies', 'competencies',
                       'expertise', 'tools', 'tech stack', 'core skills',
                       'skills & technologies', 'programming languages',
                       'skills and technologies', 'technical expertise'],
    'education':      ['education', 'academic', 'qualification', 'degree',
                       'educational background', 'academics'],
    'experience':     ['experience', 'work experience', 'employment',
                       'work history', 'internship', 'internships',
                       'professional experience', 'industry experience',
                       'job experience', 'career history', 'positions held'],
    'projects':       ['projects', 'personal projects', 'academic projects',
                       'project work', 'key projects', 'notable projects'],
    'certifications': ['certifications', 'certificates', 'certified',
                       'courses', 'training', 'online courses', 'licenses',
                       'certifications & achievements', 'achievements'],
    'awards':         ['awards', 'honours', 'honors',
                       'accomplishments', 'recognition', 'prizes'],
    'activities':     ['activities', 'extracurricular', 'societies',
                       'volunteering', 'leadership', 'clubs',
                       'co-curricular', 'extra curricular', 'community',
                       'societies / clubs', 'societies and clubs'],
}

# Phone

def extract_phone(text):
    patterns = [
        r'\+91[\s\-]?\d{5}[\s\-]?\d{5}',
        r'\+91[\s\-]?\d{10}',
        r'\+91\s?\d{10}',
        r'0\d{10}',
        r'\b[6-9]\d{9}\b',           # Indian mobile numbers starting with 6-9
        r'\(\d{3}\)[\s\-]?\d{3}[\s\-]?\d{4}',
        r'\d{3}[\s\-]\d{3}[\s\-]\d{4}',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group().strip()
    return ""

# Email

def extract_email(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(pattern, text)
    return matches[0] if matches else ""

# LinkedIn

def extract_linkedin(text):
    patterns = [
        r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_%/]+',
        r'(?:www\.)?linkedin\.com/in/[a-zA-Z0-9\-_%/]+',
        r'linkedin\.com/in/[a-zA-Z0-9\-_%/]+',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            url = match.group().strip().rstrip('/')
            if not url.startswith('http'):
                url = 'https://' + url
            return url
    return ""

# GitHub 

def extract_github(text):
    patterns = [
        r'https?://(?:www\.)?github\.com/[a-zA-Z0-9\-_%]+',
        r'(?:www\.)?github\.com/[a-zA-Z0-9\-_%]+',
        r'github\.com/[a-zA-Z0-9\-_%]+',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            url = match.group().strip().rstrip('/')
            if not url.startswith('http'):
                url = 'https://' + url
            return url
    return ""

# Name

def extract_name(text):
    doc = nlp(text[:800])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            if len(name.split()) >= 2:
                return name

    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:5]:
        if len(line.split()) <= 6 and not re.search(r'[\d@|•]', line):
            if not any(kw in line.lower() for kw in ['resume', 'cv', 'curriculum']):
                return line
    return ""

# Summary

def extract_summary(text, sections):
    
    if sections.get('summary', '').strip():
        return sections['summary']


    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    contact_done = False
    summary_lines = []

    for line in lines:
        # Skip name line
        if not contact_done:
            if '@' in line or '+91' in line or 'linkedin' in line.lower():
                contact_done = True
                continue
            continue

        # After contact, collect lines until next section header
        line_lower = line.lower()
        is_header = any(
            any(kw in line_lower for kw in kws)
            for kws in SECTION_HEADERS.values()
        )
        if is_header and len(line) < 60:
            break

        summary_lines.append(line)

    return ' '.join(summary_lines).strip()

# Section Splitter

def split_into_sections(text):
    lines = text.split('\n')
    sections = {}
    current_section = 'header'
    current_text = []

    for line in lines:
        stripped = line.strip()
        line_lower = stripped.lower()
        matched_section = None

        if stripped and len(stripped) < 80:
            for section, keywords in SECTION_HEADERS.items():
                for kw in keywords:
                    if line_lower == kw or line_lower.startswith(kw):
                        matched_section = section
                        break
                if matched_section:
                    break

        if matched_section:
            sections[current_section] = '\n'.join(current_text).strip()
            current_section = matched_section
            current_text = []
        else:
            current_text.append(line)

    sections[current_section] = '\n'.join(current_text).strip()
    return sections

# Skills

KNOWN_SKILLS = [
    # Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c',
    'ruby', 'go', 'rust', 'swift', 'kotlin', 'php', 'r', 'matlab',
    'sql', 'html', 'css', 'bash', 'scala', 'dart', 'perl',
    # Frameworks
    'react', 'reactjs', 'angular', 'vue', 'vuejs', 'node.js', 'nodejs',
    'express', 'django', 'flask', 'spring', 'fastapi', 'next.js', 'nextjs',
    'nuxt', 'svelte', 'laravel', 'bootstrap', 'tailwind', 'jquery',
    # Data / ML / AI
    'pandas', 'numpy', 'scikit-learn', 'sklearn', 'tensorflow', 'pytorch',
    'keras', 'matplotlib', 'seaborn', 'spacy', 'nltk', 'opencv', 'huggingface',
    'transformers', 'xgboost', 'lightgbm', 'hadoop', 'spark', 'insightface',
    'machine learning', 'deep learning', 'computer vision', 'nlp',
    # Databases
    'postgresql', 'mysql', 'mongodb', 'redis', 'sqlite', 'oracle',
    'firebase', 'supabase', 'elasticsearch', 'cassandra', 'dynamodb',
    # Cloud / DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'github',
    'gitlab', 'jenkins', 'terraform', 'linux', 'nginx', 'heroku', 'vercel',
    'raspberry pi',
    # Tools
    'figma', 'jira', 'notion', 'postman', 'tableau', 'powerbi',
    'excel', 'jupyter', 'jupyter notebook', 'vscode', 'android studio',
    # Other
    'rest api', 'graphql', 'microservices', 'agile', 'scrum',
    'data science', 'data analysis', 'blockchain', 'web3',
    'cloud computing', 'data visualisation', 'data visualization',
    'ms office', 'windows',
]

def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return found

# Main Extractor

def extract_all(text):
    sections = split_into_sections(text)

    # Skills — search skills section first, then full text
    skills_text = sections.get('skills', '')
    if not skills_text:
        skills_text = text

    result = {
        'name':           extract_name(text),
        'email':          extract_email(text),
        'phone':          extract_phone(text),
        'linkedin':       extract_linkedin(text),
        'github':         extract_github(text),
        'summary':        extract_summary(text, sections),
        'skills':         extract_skills(skills_text),
        'education':      sections.get('education', ''),
        'experience':     sections.get('experience', ''),
        'projects':       sections.get('projects', ''),
        'certifications': sections.get('certifications', ''),
        'awards':         sections.get('awards', ''),
        'activities':     sections.get('activities', ''),
    }

    return result