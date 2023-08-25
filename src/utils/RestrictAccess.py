from flask import request, abort

# from src.config.config import setting


class RestrictAccess:
    def __init__(self, app, header_name, header_value):
        self.app = app
        self.protected_routes = [
            "/api",
        ]
        self.header_name = header_name
        self.header_value = header_value

        self.app.before_request(self.check_custom_header)

    def check_custom_header(self):
        if request.path.startswith(tuple(self.protected_routes)):
            custom_header = request.headers.get(self.header_name)
            if custom_header != self.header_value:
                abort(403)
