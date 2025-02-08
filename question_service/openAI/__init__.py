from flask import current_app, jsonify
from openai import OpenAI
from pydantic import BaseModel, field_validator
from ..app import app


class Question(BaseModel):
    question: str
    options: list[str]
    correct_answer: str


class Questions_block(BaseModel):
    title: str
    questions: list[Question]


def generate_ai_question(prev_questions):
    client = OpenAI(api_key=app.config['AI_KEY'])
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a teacher who generates unique and diverse science questions."
            },
            {
                "role": "user",
                "content": f"Create a unique 10 and original questions question about the solar system with 4 options: 1 correct answer and 3 posssible but incorrect answers for each question. Name it 'general questions' as a title. remember this ones where already asked {prev_questions}"
            },
        ],
        response_format=Questions_block,
    )

    event = completion.choices[0].message.parsed
    questions_list = [q.dict() for q in event.questions]

    return dict(title=event.title, questions=questions_list)


def generate_question_from_txt(text):
    client = OpenAI(api_key=app.config['AI_KEY'])
    print('request')
    print(text)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a teacher who generates unique and diverse science questions."
            },
            {
                "role": "user",
                "content": f"Create a unique 10 and original questions from the text ({text}) provided with 4 options each: 1 correct answer and 3 plausible but incorrect answers. Also acording to a text create a title that represents questions block"
            },
        ],
        response_format=Questions_block
    )

    event = completion.choices[0].message.parsed
    print(event)
    questions_list = [q.dict() for q in event.questions]
    return jsonify({
        "questions": questions_list
    })