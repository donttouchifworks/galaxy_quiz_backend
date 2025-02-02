from .db_gateway import get_all_questions_db, insert_questions
from openAI import generate_ai_question
from gemini import generate_questions_gemini

def generate_questions_openAI():
    prev_questions = get_all_questions_db()
    questions=generate_ai_question(prev_questions)
    insert_questions(questions['questions'], questions['title'])
    return questions


def generate_questions_Gemini():
    prev_questions = get_all_questions_db()
    questions= generate_questions_gemini(prev_questions)
    insert_questions(questions['questions'], questions['title'])
    return questions