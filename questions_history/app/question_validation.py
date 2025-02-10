from . import app
from . import logger
import requests
from flask import jsonify


def validate_question(question_id, answer_given):
    """

    :param question_id:
    :param answer_given:
    :return:
    True or False if question exist otherwise mistake
    """
    try:
        question = get_question(question_id)

        if not question:
            return jsonify({"error": "Question doesn't exist"}), 404
        if 0 < answer_given > 3:
            return jsonify({"error": "Wrong answer range"}), 404
        correct = validate_answer_given(str(answer_given), question)
        return correct
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_question(question_id):
    """
    Get question by ID.
    If question exist return data otherwise NONE
    """
    try:
        logger.info(question_id)
        service = app.config["QUESTIONS_SERVICE"]
        url = f"{service}/get_question_by_id/{question_id}"
        response = requests.get(url=url)

        if response.status_code == 200:
            question_data = response.json()
            return question_data if question_data else None
        else:
            logger.error(f"Failed to retrieve question: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error fetching question: {str(e)}")
        return None


def validate_answer_given(given_answer, question):
    if given_answer == question['correct_answer']:
        return True
    return False