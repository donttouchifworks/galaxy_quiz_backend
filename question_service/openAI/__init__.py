from flask import current_app, jsonify
from openai import OpenAI
from pydantic import BaseModel

from app import logger


class Question(BaseModel):
    question: str
    options: list[str]
    correct_answer: str


class Questions_block(BaseModel):
    questions: list[Question]


def generate_ai_question():
    client = OpenAI(api_key=current_app.config['AI_KEY'])
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a teacher who generates unique and diverse science questions."
            },
            {
                "role": "user",
                "content": "Create a unique 10 and original questions question about the solar system with 4 options: 1 correct answer and 3 plausible but incorrect answers for each question."
            },
            # {
            #     "role": "user",
            #     "content": "Please make sure this question is new and hasn't been used before."
            # }
        ],
        response_format=Questions_block,
    )

    event = completion.choices[0].message.parsed
    questions_list = [q.dict() for q in event.questions]
    return jsonify({
        "questions": questions_list
    })


def generate_question_from_txt(text):
    client = OpenAI(api_key=current_app.config['AI_KEY'])
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a teacher who generates unique and diverse science questions."
            },
            {
                "role": "user",
                "content": f"Create a unique 10 and original questions from the text ({text}) provided with 4 options each: 1 correct answer and 3 plausible but incorrect answers."
            },
            # {
            #     "role": "user",
            #     "content": "Please make sure this question is new and hasn't been used before."
            # }
        ],
        response_format=Questions_block
    )

    event = completion.choices[0].message.parsed
    questions_list = [q.dict() for q in event.questions]
    return jsonify({
        "questions": questions_list
    })