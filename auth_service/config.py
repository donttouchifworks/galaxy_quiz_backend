import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_local_key")
    MONGO_URI = os.getenv("MONGO_URI")
    ACCESS_TOKEN_EXPIRY_MINUTES = 120
    REFRESH_TOKEN_EXPIRY_DAYS = 7


class Config_dev:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_local_key")
    MONGO_URI = os.getenv("mongodb://localhost:27017")
    ACCESS_TOKEN_EXPIRY_MINUTES = 999
    REFRESH_TOKEN_EXPIRY_DAYS = 7