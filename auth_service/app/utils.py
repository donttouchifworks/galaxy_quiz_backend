import bcrypt
import jwt
from datetime import datetime, timedelta
from config import Config


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def generate_access_token(email):
    expiration = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRY_MINUTES)
    token = jwt.encode({"email": email, "exp": expiration}, Config.SECRET_KEY, algorithm="HS256")
    return token


def generate_refresh_token(email):
    expiration = datetime.utcnow() + timedelta(days=Config.REFRESH_TOKEN_EXPIRY_DAYS)
    token = jwt.encode({"email": email, "exp": expiration}, Config.SECRET_KEY, algorithm="HS256")
    return token
