from flask import Flask, jsonify, request, json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from src.routes.route import route
from src.config.config import setting
from src.utils.RestrictAccess import RestrictAccess
from src.utils.Logging import Logging
from mongoengine import connect

app = Flask(__name__)
log = Logging(app)


# index route
@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        request.response_code = 200
        log.debug("PY API, Welcome.")
        return jsonify({"message": "PY API"}), 200


# cors
CORS(app, supports_credentials=True)

# restrict access
RestrictAccess(app, header_name="X-Custom-Header", header_value=setting.xcustom)

# prefix
app.register_blueprint(route, url_prefix="/api")


# error handler
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    request.response_code = e.code
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    log.error(e.name)
    return response


# connect data
connect(host=setting.mongo_uri)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=setting.debugging,
        passthrough_errors=setting.passthrough_errors,
        use_debugger=setting.use_debugger,
        use_reloader=setting.use_reloader,
    )
