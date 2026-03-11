# Flask web server for Resume Parser

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from parser.pdf_reader import read_pdf
from parser.docx_reader import read_docx
from parser.extractor import extract_all

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload and parse resume

@app.route('/parse', methods=['POST'])
def parse_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF and DOCX files allowed'}), 400

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Read text based on file type
    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        text = read_pdf(filepath)
    else:
        text = read_docx(filepath)

    if not text:
        return jsonify({'error': 'Could not extract text from file'}), 400

    # Extract all fields
    result = extract_all(text)
    result['filename'] = file.filename
    result['raw_text_length'] = len(text)

    # Save result to outputs folder as JSON
    output_file = os.path.join(OUTPUT_FOLDER, file.filename + '.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"✅ Parsed: {file.filename}")
    return jsonify(result)

# Health check

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Resume Parser is running!'})

# Start server

if __name__ == '__main__':
    print("✅ Resume Parser API running on http://localhost:5000")
    app.run(debug=True, port=5000)