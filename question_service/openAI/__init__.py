from flask import current_app, jsonify
from openai import OpenAI
from pydantic import BaseModel


class Question(BaseModel):
    question: str
    options: list[str]
    correct_answer: str


def make_test_request():
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
                "content": "Create a unique and original question about the solar system with 4 options: 1 correct answer and 3 plausible but incorrect answers."
            },
            {
                "role": "user",
                "content": "Please make sure this question is new and hasn't been used before."
            }
        ],
        response_format=Question,
    )

    event = completion.choices[0].message.parsed
    return jsonify({
        "question": event.question,
        "correct_answer": event.correct_answer,
        "options": event.options
    })
