from functools import wraps
from flask import request, jsonify, current_app
import requests
from .logger import logger


# def user_needed(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if not hasattr(request, 'token'):
#             return False
#
#         try:
#             headers = {key: value for key, value in request.headers if key.lower() != "host"}
#             response = requests.post(f"{app.config["AUTH_SERVICE_URL"]}/verify", headers={"Authorization": token})
#             logger.info(f"response from auth_service: {response.status_code} - {response.text}")
#             data = response.json()
#
#             print(f"🔍 response from auth_service: {data}")
#
#             return data.get("valid", False)
#         except requests.exceptions.RequestException as e:
#             logger.warning(f"Error on token validation: {e}")
#             return False


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Extracting the token from the 'Authorization' header
        auth_token = request.headers.get("Authorization")

        if not auth_token:
            return jsonify({"error": "Unauthorized, token missing"}), 401

        # Removing the "Bearer" prefix from the token if present
        token = auth_token.split(" ")[1] if "Bearer" in auth_token else auth_token

        try:
            # URL of the auth service to verify the token
            auth_service = current_app.config["AUTH_SERVICE_URL"]
            response = requests.post(
                f"{auth_service}/verify",
                headers={"Authorization": f"Bearer {token}"}
            )

            # Log the response for debugging
            logger.info(f"response from auth_service: {response.status_code} - {response.text}")
            data = response.json()

            print(f"🔍 response from auth_service: {data}")

            if not data.get("valid", False):
                return jsonify({"error": "Invalid token"}), 401

            return f(*args, **kwargs)

        except requests.exceptions.RequestException as e:
            logger.warning(f"Error on token validation: {e}")
            return jsonify({"error": "Service unavailable"}), 503

    return decorated


def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Extracting the token from the 'Authorization' header
        auth_token = request.headers.get("Authorization")

        if not auth_token:
            return jsonify({"error": "Unauthorized, token missing"}), 401

        # Removing the "Bearer" prefix from the token if present
        token = auth_token.split(" ")[1] if "Bearer" in auth_token else auth_token

        try:
            # URL of the auth service to verify the token
            auth_service = current_app.config["AUTH_SERVICE_URL"]
            response = requests.post(
                f"{auth_service}/profile",
                headers={"Authorization": f"Bearer {token}"}
            )

            # Log the response for debugging
            logger.info(f"response from auth_service: {response.status_code} - {response.text}")
            data = response.json()

            if not data.get("user", False):
                return jsonify({"error": "Invalid user"}), 401
            else:
                user = data.get('user')
                return f(*args, **kwargs, user=user)

        except requests.exceptions.RequestException as e:
            logger.warning(f"Error on token validation: {e}")
            return jsonify({"error": "Service unavailable"}), 503

    return decorated