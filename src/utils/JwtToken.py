import jwt
from flask import make_response, request
from src.config.config import setting


# generate token function
def generate_token(payload, secret):
    return jwt.encode(payload, secret, algorithm="HS256")


# validate token function
def validate_token(func):
    secret = setting.token_secret

    def wrapper(*args, **kwargs):
        try:
            token = request.headers["token"]
        except Exception as e:
            return make_response({"message": "Unauthorized, Token not provided"}, 401)

        try:
            jwt.decode(token, secret, algorithms=["HS256"])
            return func(*args, **kwargs)
        except Exception as e:
            return make_response({"message": "Invalid token provided"}, 401)

    return wrapper
