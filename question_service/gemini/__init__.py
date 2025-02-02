import google.generativeai as genai
from flask import current_app
from app import app
from pydantic import BaseModel
import json


class question(BaseModel):
    question: str
    options: list[str]
    correct_answer: str


class questions_block(BaseModel):
    title: str
    questions: list[question]


def generate_questions_gemini(prev_questions):
    genai.configure(api_key=app.config['GEMINI_KEY'])
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction="You are a teacher who generates unique and diverse science questions."
    )
    result = model.generate_content(
         f"Create a unique 10 and original questions question about the solar system with 4 options: 1 correct answer and 3 posssible but incorrect answers for each question. Name it 'general questions' as a title. remember this ones where already asked {prev_questions}",
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=questions_block
        ),
    )

    data = json.loads(result.text)
    questions_list = [q for q in data["questions"]]
    return dict(title=data["title"], questions=questions_list)