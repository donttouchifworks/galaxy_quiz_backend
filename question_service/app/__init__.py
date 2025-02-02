from flask import Flask, request
from config import Config
import logging
from time import sleep

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

from .db_model import create_table, get_db_connection, check_table_exists

# @app.after_request
# def log_response_info(response):
#     logger.info(
#         f"Response: Status: {response.status_code} "
#         f"Headers: {dict(response.headers)} "
#         f"Body: {response.get_data(as_text=True)}"
#     )
#     return response


# @app.before_request
# def log_request_info():
#     logger.info(
#         f"Request: {request.method} {request.url} "
#         f"Headers: {dict(request.headers)} "
#         f"Body: {request.get_data(as_text=True)}"
#     )

print("connecting to db...")
while True:
    try:
        conn = get_db_connection()
        conn.close()
        break
    except:
        print("connecting to db failed restarting...")
        sleep(2)

from app import routes
