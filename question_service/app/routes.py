import logging

from app import app, logger
from flask import jsonify, request
from openAI import generate_ai_question, generate_question_from_txt
from .pdf_processing import upload_pdf
from .db_gateway import get_unasked_questions_db
from gemini import generate_questions_gemini
from .questions_generator import generate_questions_openAI, generate_questions_Gemini
from .user_questions_gateway import check_user_answered_questions
import random


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API questions is running!"})




#Test route TODO define route to generate questions for a user
# @app.route('/generate', methods=['GET'])
# def generate_question():
#     questions_asked = check_user_answered_questions()
#     if not questions_asked:
#         generate_questions_openAI()
#
#     questions_available = get_unasked_questions_db(questions_asked)
#
#     if not questions_available:
#         generate_questions_openAI()
#
#     questions_available = get_unasked_questions_db(questions_asked)
#
#     question = random.choice(questions_available)
#
#
#     return question
#
#
# @app.route("/generate_gemini", methods=["GET"])
# def generate_question_gemini():
#     questions=generate_questions_Gemini()
#     return questions


@app.route("/get_question_openAI", methods=["GET"])
def get_question_openAI():
    questions_asked = check_user_answered_questions()
    if not questions_asked:
        generate_questions_openAI()

    questions_available = get_unasked_questions_db(questions_asked)

    if not questions_available:
        generate_questions_openAI()

    questions_available = get_unasked_questions_db(questions_asked)

    question = random.choice(questions_available)


    return question

@app.route("/get_question_gemini", methods=["GET"])
def get_question_gemini():
    questions_asked = check_user_answered_questions()
    if not questions_asked:
        generate_questions_Gemini()

    questions_available = get_unasked_questions_db(questions_asked)

    if not questions_available:
        generate_questions_Gemini()

    questions_available = get_unasked_questions_db(questions_asked)

    question = random.choice(questions_available)


    return question


@app.route('/generate_from_pdf', methods=["POST"])
def generate_from_pdf():
    file = request.files.get('file')
    print(file)
    file = request.files["file"]

    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)

    if file_size > 10 * 1024 * 1024:
        return jsonify({"error": "File too large"}), 413

    if not file:
        return jsonify({"error": "File doesn't exist in request"}), 400

    try:
        text = upload_pdf(request.files['file'])
        print(text)
    except ValueError as e:
        return jsonify({"error": str(e)})

    questions = generate_question_from_txt(text)

    return questions


# @app.route('/get_all_questions', methods=["GET"])
# def get_all_questions():
#     return get_all_questions_db()
