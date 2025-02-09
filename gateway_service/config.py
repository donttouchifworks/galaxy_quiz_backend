import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL')  # Authentication Service
    QUESTION_SERVICE_URL = os.getenv('QUESTION_SERVICE_URL')  # Question Generation Service
    QUESTIONS_HISTORY_SERVICE_URL = os.getenv('QUESTIONS_HISTORY_SERVICE_URL')  # Questions History Service
    DEBUG=os.getenv('DEBUG')