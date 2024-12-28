import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    ACCESS_TOKEN_EXPIRY_MINUTES = 60
    REFRESH_TOKEN_EXPIRY_DAYS = 7
