from .database.db_gateway import get_all_questions_db, insert_questions
from .openAI import generate_ai_question
from .gemini import generate_questions_gemini
from . import logger


def generate_questions_openAI():
    prev_questions = get_all_questions_db()
    questions=generate_ai_question(prev_questions)
    logger.info(questions)
    converted_questions = convert_correct_answer_to_index(questions['questions'])
    insert_questions(converted_questions, questions['title'])
    return converted_questions


def generate_questions_Gemini():
    prev_questions = get_all_questions_db()
    questions= generate_questions_gemini(prev_questions)
    logger.info(questions)
    converted_questions = convert_correct_answer_to_index(questions['questions'])
    insert_questions(converted_questions, questions['title'])
    return converted_questions


def convert_correct_answer_to_index(questions):
    converted = []
    for question in questions:
        logger.info(f"Processing question: {question}")
        if "correct_answer" in question and "options" in question:
            try:
                question["correct_answer"] = question["options"].index(question["correct_answer"])
                converted.append(question)
            except ValueError:
                logger.warning(f"Skipping question, correct answer '{question['correct_answer']}' not found in {question['options']}")
    logger.info(f"Converted questions count: {len(converted)}")
    return converted