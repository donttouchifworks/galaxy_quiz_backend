from flask import Flask, request
from config import Config
from pymongo import MongoClient
import logging

app = Flask(__name__)
app.config.from_object(Config)

# logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


try:
    mongo = MongoClient(app.config["MONGO_URI"])
    db = mongo["question_history_service"]
    logger.info("Connected to Question History DB")
except Exception as e:
    logger.critical(f"Failed to connect to Question History DB: {e}")
    raise


from .routes import *


@app.after_request
def log_response_info(response):
    logger.info(
        f"Response: Status: {response.status_code} "
        f"Headers: {dict(response.headers)} "
        f"Body: {response.get_data(as_text=True)}"
    )
    return response


@app.before_request
def log_request_info():
    logger.info(
        f"Request: {request.method} {request.url} "
        f"Headers: {dict(request.headers)} "
        f"Body: {request.get_data(as_text=True)}"
    )