from flask import Flask, request
from config import Config
import logging
import psycopg2

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


def get_db_connection():
    return psycopg2.connect(
        host=app.config["DB_HOST"],  # Хост из переменных окружения
        database=app.config["DB_NAME"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        port=app.config["DB_PORT"]
    )


try:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT version();')
    db_version = cur.fetchone()
    cur.close()
    conn.close()
    logger.info(f"status: success, 'db_version': {db_version}")
except Exception as e:
    logger.info(f"Connecting to DB at {app.config['DB_HOST']}:{app.config['DB_PORT']}")
    logger.info(f"'status': 'error', 'error': {str(e)}")


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