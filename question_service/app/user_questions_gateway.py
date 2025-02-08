from . import app
from flask import jsonify
import requests


def check_user_answered_questions(id):
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

    answers = []
    # for nums in range(1, 2):
    #     answers.append(nums)
    return questions_list


def user_answered(id, right):
    return True