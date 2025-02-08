from flask import Flask, request, jsonify
import PyPDF2
import os
from . import app

# folder for pdf
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def upload_pdf(file):
    # if not file:
    #     return jsonify({"error": "File doesn`t exist in request"}), 400

    if file.filename == '':
        return jsonify({"error": "file name is empty"}), 400

    # Check if PDF
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "PDF file required"}), 400

    # Temporary save file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    text = ""
    # processing PDF
    try:
        with open(filepath, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        return jsonify({"error": f"Processing PDF failture: {str(e)}"}), 400
    finally:
        os.remove(filepath)  # delete file

    if text == "":
        raise ValueError("this pdf can't be read")

    return text
