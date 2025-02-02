from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# URLs for services
AUTH_SERVICE_URL = "http://auth_service:8001"  # Authentication Service
QUESTION_SERVICE_URL = "http://question_service:8002"  # Question Generation Service

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

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
    if not token:
        return False

    try:
        headers = {key: value for key, value in request.headers if key.lower() != "host"}
        response = requests.post(f"{AUTH_SERVICE_URL}/verify", headers={"Authorization": token})
        logger.info(f"response from auth_service: {response.status_code} - {response.text}")
        data = response.json()

        print(f"🔍 response from auth_service: {data}")

        return data.get("valid", False)
    except requests.exceptions.RequestException as e:
        logger.warning(f"Error on token validation: {e}")
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

    if not verify_token(token):
        logger.warning(f"Validation error, token missing")
        return jsonify({"error": "Unauthorized"}), 401

    headers = {key: value for key, value in request.headers.items() if key.lower() not in ["host", "content-length"]}

    # files = request.files if "file" in request.files else None
    data = request.form if request.form else None

    # logger.info("files :", files)

    url = f"{QUESTION_SERVICE_URL}/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        # files=files,
        data=data
    )

    logger.info(f"Response from question service: Status {response.status_code}, Body: {response.text}")

    # if response.status_code == 413:
    #     return jsonify({"error": "File too large"}), 413

    if response.status_code != 200:
        return jsonify(
            {"error": "Request failed", "status": response.status_code, "body": response.text}), response.status_code
    # try:
    #     response_data = response
    # except ValueError:
    #     logger.error(f"Error decoding JSON response: {response.text}")
    #     return jsonify({"error": "Invalid response from question service"}), 500

    return jsonify(response.json()), response.status_code


# test route
@app.route('/', methods=['GET'])
def home():
    logger.info("test passed gateway service running")
    return jsonify({"message": "API Gateway is running!"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

