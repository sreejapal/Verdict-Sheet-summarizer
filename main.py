from flask import Flask, render_template, request, send_file, url_for
import os
from fpdf import FPDF
import uuid
import sys
from werkzeug.utils import secure_filename

# Set up absolute paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
SUMMARY_FOLDER = os.path.join(BASE_DIR, 'summary_pdfs')

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SUMMARY_FOLDER, exist_ok=True)

# Make sure custom modules can be imported
sys.path.append(BASE_DIR)

# Import your functions
from scripts.extract_text import extract_text_from_pdf
from my_custom_summarizer.summarize import summarize_text

# Initialize Flask app
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'pdf_file' not in request.files:
        return "No file part", 400

    file = request.files['pdf_file']
    if file.filename == '':
        return "No selected file", 400

    if not file.filename.lower().endswith('.pdf'):
        return "Only PDF files allowed", 400

    try:
        # Save uploaded file
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(pdf_path)

        # Extract text and summarize
        extracted_text = extract_text_from_pdf(pdf_path)
        summary = summarize_text(extracted_text)

        # Create summary PDF
        summary_filename = f"summary_{filename}"
        summary_pdf_path = os.path.join(SUMMARY_FOLDER, summary_filename)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in summary.split('\n'):
            if line.strip():
                pdf.multi_cell(0, 10, line.strip())
        pdf.output(summary_pdf_path)

        # Optional: delete original upload
        os.remove(pdf_path)

        return render_template('result.html', summary=summary, pdf_url=url_for('download_file', filename=summary_filename))

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(SUMMARY_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

import webbrowser
import threading

if __name__ == '__main__':
    port = 5000
    url = f'http://127.0.0.1:{port}/'

    # Open in a new browser tab after 1 second
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    app.run(debug=True, port=port)
