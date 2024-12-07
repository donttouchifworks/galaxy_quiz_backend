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
                "content": "You are a teacher that want to teach people and make them upgrading their knowledge in science"
            },
            {
                "role": "user",
                "content": "Create a question about solar system with 4 options: 1 correct answer, "
                           "3 false answers but with sense in it."
            },
        ],
        response_format=Question,
    )

    event = completion.choices[0].message.parsed
    print(event)
    return jsonify({
        "question": event.question,
        "correct_answer": event.correct_answer,
        "options": event.options
    })


def get_key():
    return current_app.config['AI_KEY']
