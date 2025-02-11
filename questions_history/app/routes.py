from app import app, logger
from flask import jsonify, request
from .db_gateway import insert_answer, get_questions_asked_to_user, is_question_already_asked
from .question_validation import validate_question, get_question
import redis
import json
from datetime import datetime, timedelta
from bson.json_util import dumps
# import pika

# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


@app.route("/service", methods=["GET"])
def service_check():
    return jsonify({"question history status": "active"})


@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON or no data provided"}), 400

        logger.info(f"Submit answer data: {data}")

        user = data.get("user")
        if not user:
            return jsonify({"error": "User data is missing"}), 400

        user_id = user.get("id")
        question_id = data.get("question_id")
        answer = data.get("answer")

        if not all([user_id, question_id, answer]):
            return jsonify({"error": "Missing required fields"}), 400

        question = get_question(question_id)
        if not question:
            return jsonify({"error": "Question not found"}), 400

        is_answer_correct = validate_question(question_id, answer)

        if not isinstance(is_answer_correct, bool):
            return jsonify({"error": "Invalid answer validation result"}), 400

        logger.info(f"Answer correctness: {is_answer_correct}")

        is_question_asked = is_question_already_asked(user_id, question_id)

        if is_question_asked:
            return jsonify({"Message": "question already asked"}), 400

        answer = {
            "user_id": user_id,
            "question_id": question_id,
            "answer": answer,
            "is_correct": is_answer_correct
        }

        submitted_answer = insert_answer(answer)

        return jsonify({"message": "Answer submitted successfully", "data": submitted_answer}), 200

    except Exception as e:
        logger.error(f"Error submitting answer: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/get_questions_asked", methods=["GET", "POST"])
def get_asked_questions():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON or no data provided"}), 400

        logger.info(f"Submit answer data: {data}")

        user = data.get("user")
        if not user:
            return jsonify({"error": "User data is missing"}), 400

        user_id = user.get("id")
        logger.info(request)
        questions = get_questions_asked_to_user(user_id)
        logger.info({"guestions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "questions": questions
    })