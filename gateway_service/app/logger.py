import logging
from flask import current_app, request


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


@current_app.after_request
def log_response_info(response):
    logger.info(
        f"Response: Status: {response.status_code} "
        f"Headers: {dict(response.headers)} "
        f"Body: {response.get_data(as_text=True)}"
    )
    return response


@current_app.before_request
def log_request_info():
    logger.info(
        f"Request: {request.method} {request.url} "
        f"Headers: {dict(request.headers)} "
        f"Body: {request.get_data(as_text=True)}"
        )