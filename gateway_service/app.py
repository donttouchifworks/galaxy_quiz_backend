from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URLs for services
AUTH_SERVICE_URL = "http://auth_service:8001"  # Authentication Service
QUESTION_SERVICE_URL = "http://question_service:8002"  # Question Generation Service


# Middleware for token check
def verify_token(token):
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/auth/verify", headers={"Authorization": token})
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


# routes for Authentication Service
@app.route('/auth/<path:path>', methods=['GET', 'POST'])
def auth_service(path):
    url = f"{AUTH_SERVICE_URL}/auth/{path}"
    response = requests.request(method=request.method, url=url, headers=request.headers, json=request.json)
    return jsonify(response.json()), response.status_code


# routes for Question Generation Service
@app.route('/questions/<path:path>', methods=['GET', 'POST'])
def question_service(path):
    token = request.headers.get("Authorization")
    if not token or not verify_token(token):
        return jsonify({"error": "Unauthorized"}), 401

    url = f"{QUESTION_SERVICE_URL}/questions/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        headers={**request.headers, "Content-Type": "application/json"},
    )
    return jsonify(response.json()), response.status_code


# test route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API Gateway is running!"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

