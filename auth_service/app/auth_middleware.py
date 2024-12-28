from flask import request, jsonify
import jwt
from functools import wraps
from config import Config
from app import logger

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")
        logger.info(f"Token: {token}")
        if not token or not token.startswith("Bearer "):
            return jsonify({"message": "Token is missing or invalid format"}), 401

        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])

            request.user = {"email": decoded_token.get("email")}
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"message": f"Token verification failed: {str(e)}"}), 400

        return f(*args, **kwargs)

    return decorated
