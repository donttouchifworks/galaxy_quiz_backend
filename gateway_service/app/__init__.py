from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# URLs for services
AUTH_SERVICE_URL = "http://auth_service:8001"  # Authentication Service
QUESTION_SERVICE_URL = "http://question_service:8002"  # Question Generation Service


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


# Middleware for token check
def verify_token(token):
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/verify", headers={"Authorization": token})
        print(response)
        logger.info(f"Response: {response}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logger.warning(f"Not Authorised: {e}")
        return False


# routes for Authentication Service
@app.route('/auth/<path:path>', methods=['GET', 'POST'])
def auth_service(path):
    logger.info(f"auth service: {path}")
    url = f"{AUTH_SERVICE_URL}/{path}"
    response = requests.request(method=request.method, url=url, headers=request.headers, json=request.json)
    logger.info(f"auth service: {response}")
    return jsonify(response.json()), response.status_code


# routes for Question Generation Service
@app.route('/questions/<path:path>', methods=['GET', 'POST'])
def question_service(path):
    token = request.headers.get("Authorization")
    logger.info(f"questions service: {path}")
    if not token or not verify_token(token):
        logger.warning(f"Validation error, token missing")
        return jsonify({"error": "Unauthorized"}), 401

    url = f"{QUESTION_SERVICE_URL}/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        headers={**request.headers, "Content-Type": "application/json"},
    )
    logger.info(f"questions service: {response}")
    return jsonify(response.json()), response.status_code


# test route
@app.route('/', methods=['GET'])
def home():
    logger.info("test passed gateway service running")
    return jsonify({"message": "API Gateway is running!"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

