from . import app, logger
from flask import jsonify
import requests

def check_user_answered_questions(id):
    try:
        service = app.config['QUESTION_HISTORY_SERVICE']
        url = f"{service}get_questions_asked"
        data = {"user": {"id": id}}
        response = requests.post(url=url, json=data)

        if response.status_code == 200:
            questions_list= []
            questions = response.json()
            for item in questions['questions']:
                questions_list.append(item['question_id'])
                print(questions_list)
    except Exception as e:
        logger.warning(f"Error in fetching asked questions: {str(e)}")
        return jsonify({"Error": e})

    answers = []
    # for nums in range(1, 2):
    #     answers.append(nums)
    return questions_list


def user_answered(id, right):
    return True