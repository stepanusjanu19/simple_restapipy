import logging
import colorlog
from flask import request


class RequestInfoFilter(logging.Filter):
    def filter(self, record):
        record.method = request.method if request else "N/A"
        record.ip = request.remote_addr if request else "N/A"
        record.response_code = (
            request.response_code if hasattr(request, "response_code") else 200
        )
        return True


# declare class logging
class Logging:
    def __init__(self, app=None):
        self.logger = logging.getLogger(__name__)
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        log_format = colorlog.ColoredFormatter(
            "%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s - Method: %(method)s - IP: %(ip)s - Response Code: %(response_code)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )

        log_handler = logging.StreamHandler()
        log_handler.setFormatter(log_format)
        log_handler.addFilter(RequestInfoFilter())
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logging.DEBUG)

        @app.before_request
        def before_request():
            self.logger.debug(
                "Request to %s - Method: %s - IP: %s",
                request.path,
                request.method,
                request.remote_addr,
            )

        @app.after_request
        def after_request(response):
            self.logger.info(
                "Request to %s - Method: %s - IP: %s - Response Code: %s",
                request.path,
                request.method,
                request.remote_addr,
                response.status,
            )

            return response

        @app.errorhandler(Exception)
        def log_exception(error):
            self.logger.error(
                "An error occurred: %s - Method: %s - IP: %s",
                str(error),
                request.method,
                request.remote_addr,
            )

    # log level function
    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
