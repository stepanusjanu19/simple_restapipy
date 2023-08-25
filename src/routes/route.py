from flask import Blueprint, request
from flask_cors import cross_origin
from src.controller.user_controller import signup_service, signin_service

route = Blueprint("route", __name__)


@route.route("/signup", methods=["POST"])
@cross_origin(supports_credentials=True)
def signup():
    data = request.get_json()
    return signup_service(data)


@route.route("/signin", methods=["POST"])
@cross_origin(supports_credentials=True)
def signin():
    data = request.get_json()
    return signin_service(data)
