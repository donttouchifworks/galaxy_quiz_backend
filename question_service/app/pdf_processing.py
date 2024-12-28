from flask import Flask, request, jsonify
import PyPDF2
import os
from app import app


# folder for pdf
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def upload_pdf(file):
    # if 'file' not in request.files:
    #     return jsonify({"error": "File doesn`t exist in request"}), 400
    #
    # file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "file name is empty"}), 400

    # Check if PDF
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "PDF file required"}), 400

    # Temporary save file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # processing PDF
    try:
        with open(filepath, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        return jsonify({"error": f"Processing PDF failture: {str(e)}"}), 500
    finally:
        os.remove(filepath)  # delete file

    return jsonify({"text": text})