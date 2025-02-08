from flask import Flask, request, jsonify
import logging
from config import Config, Config_dev


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        from . import logger
        from .routes import main
        app.register_blueprint(main)

    return app




# URLs for services

#
# app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

# logger setup



# @app.after_request
# def log_response_info(response):
#     logger.info(
#         f"Response: Status: {response.status_code} "
#         f"Headers: {dict(response.headers)} "
#         f"Body: {response.get_data(as_text=True)}"
#     )
#     return response
#
#
# @app.before_request
# def log_request_info():
#     logger.info(
#         f"Request: {request.method} {request.url} "
#         f"Headers: {dict(request.headers)} "
#         f"Body: {request.get_data(as_text=True)}"
#     )

# routes for Authentication Service


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=8000)
