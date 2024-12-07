from flask import request, jsonify
from app import app, db, logger
from app.utils import hash_password, verify_password, generate_access_token, generate_refresh_token
from app.auth_middleware import token_required
from marshmallow import ValidationError
from app.schemas import RegisterSchema, LoginSchema


@app.route('/', methods=['GET'])
def test_service():
    return jsonify({"message": "Auth service is running"})


@app.route("/register", methods=["POST"])
def register():
    logger.info("register route accessed")
    try:
        schema = RegisterSchema()
        data = schema.load(request.json)

        if db.users.find_one({"email": data["email"]}):
            logger.warning(f"Registration failed: User {data['email']} already exists")
            return jsonify({"message": "User already exists"}), 400

        hashed_password = hash_password(data["password"])
        db.users.insert_one({"email": data["email"], "password": hashed_password})
        logger.info(f"User {data['email']} registered successfully")

        access_token = generate_access_token(data["email"])
        refresh_token = generate_refresh_token(data["email"])

        return jsonify({
            "user": data['email'],
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 201
    except ValidationError as ve:
        logger.warning(f"Validation error: {ve.messages}")
        return jsonify({"errors": ve.messages}), 400
    except Exception as e:
        logger.error(f"Error during registration: {type(e).__name__} - {e}")
        return jsonify({"message": "Internal server error"}), 500


@app.route("/login", methods=["POST"])
def login():
    logger.info("login route accessed")
    try:
        schema = LoginSchema()
        data = schema.load(request.json)

        user = db.users.find_one({"email": data["email"]})
        if not user or not verify_password(data["password"], user["password"]):
            logger.warning(f"Login failed: Invalid credentials for {data['email']}")
            return jsonify({"message": "Invalid credentials"}), 401

        access_token = generate_access_token(user["email"])
        refresh_token = generate_refresh_token(user["email"])

        logger.info(f"User {data['email']} logged in successfully")
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    except ValidationError as ve:
        logger.warning(f"Validation error: {ve.messages}")
        return jsonify({"errors": ve.messages}), 400
    except Exception as e:
        logger.error(f"Error during login: {type(e).__name__} - {e}")
        return jsonify({"message": "Internal server error"}), 500


@app.route("/auth/verify", methods=["GET"])
@token_required
def verify():
    """
    Verify token endpoint.
    Requires the Authorization header with a Bearer token.
    """
    logger.info(f"Token verification successful for user: {request.user['email']}")
    return jsonify({"message": "Token is valid", "user": request.user["email"]}), 200


@app.route("/auth/refresh", methods=["POST"])
def refresh_token():
    logger.info("refresh token route accessed")
    try:
        data = request.json
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            return jsonify({"message": "Refresh token is missing"}), 400

        try:
            decoded = jwt.decode(refresh_token, Config.SECRET_KEY, algorithms=["HS256"])
            email = decoded["email"]

            # generate new access token
            new_access_token = generate_access_token(email)
            return jsonify({"access_token": new_access_token}), 200
        except jwt.ExpiredSignatureError:
            logger.warning("Refresh token expired")
            return jsonify({"message": "Refresh token expired"}), 401
        except jwt.InvalidTokenError:
            logger.warning("Invalid refresh token")
            return jsonify({"message": "Invalid refresh token"}), 401
    except Exception as e:
        logger.error(f"Error during token refresh: {type(e).__name__} - {e}")
        return jsonify({"message": "Internal server error"}), 500

