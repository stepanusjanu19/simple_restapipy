import datetime
from src.model.user_model import User
from src.utils.PasswordEncrypt import encrypt_pass, compare_pass
from src.utils.JwtToken import generate_token
from src.config.config import setting
from src.utils.Logging import Logging
from flask import jsonify, request, current_app

log = Logging(current_app)


def signup_service(user):
    try:
        email_check = User.objects[:1](email=user["email"])
        if email_check:
            request.response_code = 409
            log.warning("Email its already exists")
            return jsonify({"message": "Email its already exists", "status": 409}), 409
        else:
            name = user["name"]
            email = user["email"]
            image = user["image"]
            mobile = user["mobile"]
            password = encrypt_pass(user["password"])

            user = User(
                name=name, email=email, image=image, mobile=mobile, password=password
            )

            user.save()
            request.response_code = 201
            log.debug("Success Sign Up Data")
            return jsonify({"message": "Success Sign Up Data", "status": 201}), 201
    except Exception as e:
        request.response_code = 500
        log.error(str(e))
        return jsonify({"message": str(e)}), 500


def signin_service(user_cred):
    try:
        email_check = User.objects[:1](email=user_cred["email"])
        if not email_check:
            request.response_code = 404
            log.warning("Email does not exists")
            return jsonify({"message": "Email does not exists", "status": 404}), 404
        else:
            for data in email_check:
                payload = {
                    "email": data["email"],
                    "_id": str(data["id"]),
                    "exp": datetime.datetime.utcnow()
                    + datetime.timedelta(minutes=90, seconds=60),
                }

                secret = setting.token_secret

                if compare_pass(user_cred["password"], data["password"]):
                    token = generate_token(payload, secret)
                    request.response_code = 200
                    log.debug("Success Sign In, Please Add your Auth to Access Data.")
                    return (
                        jsonify(
                            {
                                "message": "Success Sign In, Please Add your Auth to Access Data.",
                                "token": token,
                            }
                        ),
                        200,
                    )
                else:
                    request.response_code = 401
                    log.warning(
                        "Wrong password or email, please try fill again with true"
                    )
                    return (
                        jsonify(
                            {
                                "message": "Wrong password or email, please try fill again with true"
                            }
                        ),
                        401,
                    )
    except Exception as e:
        request.response_code = 500
        log.error(str(e))
        return jsonify({"message": str(e)}), 500
