from flask import request, jsonify
import jwt
from functools import wraps
from config import Config
from app import logger


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            logger.warning("Missing token in request")
            return jsonify({"message": "Token is missing!"}), 401

        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            request.user = decoded_token
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return jsonify({"message": "Invalid token!"}), 401

        return f(*args, **kwargs)

    return decorated

