from .logger import logger
import requests
from flask import current_app, jsonify, request, Blueprint
from .gateway_middleware import auth_required, user_required


main = Blueprint('main', __name__)


@main.route('/auth/<path:path>', methods=['GET', 'POST'])
def auth_service(path):
    logger.info(f"auth service: {path}")
    service = current_app.config['AUTH_SERVICE_URL']
    url = f"{service}/{path}"
    response = requests.request(method=request.method, url=url, headers=request.headers, json=request.json)
    logger.info(f"auth service: {response}")
    return jsonify(response.json()), response.status_code


# routes for Question Generation Service
@main.route('/questions/<path:path>', methods=['GET', 'POST'])
@user_required
def question_service(path, user):
    logger.info(f"questions service: {path}")

    headers = {key: value for key, value in request.headers.items() if key.lower() not in ["host", "content-length"]}

    headers = {key: value for key, value in request.headers.items() if key.lower() not in ["host", "content-length"]}
    headers['Content-Type'] = 'application/json'

    if request.content_type == "application/json":
        data = request.get_json() or {}
    else:
        data = request.form.to_dict()

    data['user'] = user

    service = current_app.config['QUESTION_SERVICE_URL']
    url = f"{service}/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        # files=files,
        json=data
    )

    logger.info(f"Response from question service: Status {response.status_code}, Body: {response.text}")

    if response.status_code != 200:
        return jsonify(
            {"Error": response.text}, response.status_code
        ),

    return jsonify(response.json()), response.status_code


@main.route('/questions_history/<path:path>', methods=['GET', 'POST'])
@user_required
def questions_history_service(path, user):

    headers = {key: value for key, value in request.headers.items() if key.lower() not in ["host", "content-length"]}
    headers['Content-Type'] = 'application/json'

    if request.content_type == "application/json":
        data = request.get_json() or {}
    else:
        data = request.form.to_dict()

    data['user'] = user


    logger.info(f"Data to send into Questions history: {data}")

    service = current_app.config['QUESTIONS_HISTORY_SERVICE_URL']
    url = f"{service}/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        json=data,
    )

    logger.info(f"Response from question history service: Status {response.status_code}, Body: {response.text}")

    if response.status_code != 200:
        return jsonify({"error": response.text }), response.status_code

    return jsonify(response.json()), response.status_code

# test route
@main.route('/', methods=['GET'])
def home():
    logger.info("test passed gateway service running")
    return jsonify({"message": "API Gateway is running!"})