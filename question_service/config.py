from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    AI_KEY = os.getenv("OPEN_AI_KEY")