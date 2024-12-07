import logging
from flask import Flask, request
from pymongo import MongoClient
from config import Config

# Flask app
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

# connect to Mongo
try:
    mongo = MongoClient(app.config["MONGO_URI"])
    db = mongo["auth_service"]
    logger.info("Connected to MongoDB")
except Exception as e:
    logger.critical(f"Failed to connect to MongoDB: {e}")
    raise


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


from app import routes
