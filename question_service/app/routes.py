import logging

from app import app, logger
from flask import jsonify, request
from openAI import generate_ai_question, generate_question_from_txt
from app.pdf_processing import upload_pdf


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API questions is running!"})


@app.route('/generate', methods=['GET'])
def generate_question():
    question = generate_ai_question()
    return question

@app.route('/generate_from_pdf', methods=["POST"])
def generate_from_pdf():
    if 'file' not in request.files:
        logger.warn(f"/generate_from_pdf file error: No file found")
        return jsonify({"error": "File doesn`t exist in request"}), 400

    text = upload_pdf(request.files['file'])
    questions = generate_question_from_txt(text)
    return questions