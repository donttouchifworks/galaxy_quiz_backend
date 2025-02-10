import json

from pymongo import MongoClient
from app import logger, app
from bson.json_util import dumps, ObjectId


def init_connection():
    try:
        mongo = MongoClient(app.config["MONGO_URI"])
        db = mongo["question_history_service"]
        answers_collection = db["answers"]
        logger.info("Connected to Question History DB")
        return answers_collection
    except Exception as e:
        logger.critical(f"Failed to connect to Question History DB: {e}")
        raise


def get_one_by_id(id):
    try:
        collection = init_connection()
        answer = collection.find_one(id)
        if answer:
            answer["_id"] = str(answer["_id"])
            logger.info(answer)
            return answer
        else:
            return json.dumps({"error": "Question not found"})
    except Exception as e:
        logger.critical(f"Failed to get items from Question History DB (getone): {e}")


def insert_answer(answer):
    try:
        answers_collection = init_connection()
        answer_new = answers_collection.insert_one(answer)

        logger.info(f"Item successfully added {answer_new.inserted_id}")

        submited_answer = answers_collection.find_one({"_id": answer_new.inserted_id})

        submited_answer["_id"] = str(submited_answer["_id"])

        logger.info({"insert answer": submited_answer["_id"]})

        return submited_answer

    except Exception as e:
        logger.critical(f"Failed to add to Question History DB: {e}")
        raise


def get_questions_asked_to_user(user_id):
    try:
        collection = init_connection()
        questions = collection.find({"user_id": user_id})
        question_list = list(questions)
        for question in question_list:
            question["_id"] = str(question["_id"])

        if not question_list:
            logger.info(f"No questions found for user_id: {user_id}")
            return []

        logger.info(f"Found {len(question_list)} questions for user_id: {user_id}")
        return question_list
    except Exception as e:
        logger.critical(f"Failed to get items from Question History DB: {e}")
        raise


def is_question_already_asked(user_id, question_id):
    try:
        collection = init_connection()
        question = collection.find({"user_id": user_id, "question_id": question_id}).limit(1)
        question_list = list(question)

        logger.warn({"Question from db": question_list})

        if question_list:
            return True
        return False
    except Exception as e:
        logger.critical(f"Failed to get items from Question History DB: {e}")




