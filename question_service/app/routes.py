from . import app
from flask import jsonify, request
from ..openAI import generate_question_from_txt
from .pdf_processing import upload_pdf
from .database.db_gateway import get_unasked_questions_db, get_question_by_id_db
from .questions_generator import generate_questions_openAI, generate_questions_Gemini
from .user_questions_gateway import check_user_answered_questions
import random


@app.route('/service', methods=['GET'])
def home():
    return jsonify({"message": "API questions is running!"})


@app.route("/get_question_openAI", methods=["GET"])
def get_question_openai():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON or no data provided"}), 400

    user = data.get("user")

    if not user:
        return jsonify({"error": "User data is missing"}), 400
    user_id = user.get("id")
    questions_asked = check_user_answered_questions(user_id)

    questions_available = get_unasked_questions_db(questions_asked)

    if not questions_available:
        generate_questions_openAI()

    questions_available = get_unasked_questions_db(questions_asked)

    question = random.choice(questions_available)

    question.pop("correct_answer", None)

    return question


@app.route("/get_question_gemini", methods=["GET"])
def get_question_gemini():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON or no data provided"}), 400

    user = data.get("user")

    if not user:
        return jsonify({"error": "User data is missing"}), 400
    user_id = user.get("id")
    questions_asked = check_user_answered_questions(user_id)

    questions_available = get_unasked_questions_db(questions_asked)

    if not questions_available:
        generate_questions_Gemini()

    questions_available = get_unasked_questions_db(questions_asked)

    question = random.choice(questions_available)

    question.pop("correct_answer", None)

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


@app.route('/get_question_by_id/<int:id>', methods=['GET'])
def get_question_by_id(id):
    try:
        question = get_question_by_id_db(id)
        if not question:
            return jsonify({"error": "Question not found"}), 404
        return jsonify(question), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @app.route('/get_all_questions', methods=["GET"])
# def get_all_questions():
#     return get_all_questions_db()
