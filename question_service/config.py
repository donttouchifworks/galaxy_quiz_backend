from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    AI_KEY = os.getenv("OPEN_AI_KEY")
    GEMINI_KEY=os.getenv("GEMINI_API_KEY")
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('PORT')
    QUESTION_HISTORY_SERVICE = 'http://questions_history_service:8003/'

