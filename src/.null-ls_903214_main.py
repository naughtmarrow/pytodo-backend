# mypy: check-untyped-defs
import logging
import os

from flask import Flask, make_response
from werkzeug.exceptions import HTTPException

from src.data import ping_db
from src.routes import (
    handle_generic_exception,
    handle_http_exception,
    todo_blueprint,
    user_blueprint,
)


def create_app():
    logging.basicConfig(
        filename="log/test.log",
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s @ %(name)s] %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    logger = logging.getLogger(__name__)

    logger.info(msg="Starting Server...")

    if not ping_db():
        raise Exception("Database must be started for app to run")

    app = Flask(__name__)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(todo_blueprint)

    app.register_error_handler(500, handle_generic_exception)
    app.register_error_handler(HTTPException, handle_http_exception)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    from dotenv import load_dotenv
    load_dotenv()
    frontend_url: str = (
        f"{os.getenv('PROTOCOPROTOCOLL')}://{os.getenv('FRONT_HOST')}:{os.getenv('FRONT_PORT')}"
    )

    @app.before_request # type: ignore
    def handle_preflight(request):
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = frontend_url
            response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Max-Age'] = '86400'
            return response

    @app.after_request
    def security_headers(response):
        csp = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "form-action 'self'"

            "frame-ancestors 'none'; " # important for xss prevention
        ) # might need to add more stuff later also this goes in the frontend once i do the division

        response.headers['Content-Security-Policy'] = csp


        response.headers['Access-Control-Allow-Origin'] = frontend_url
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'

        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Permissions-Policy'] = 'interest-cohort=()' # goes in the frontend

        response.headers.pop('Server', None)
        response.headers.pop('X-Powered-By', None)
        response.headers['X-DNS-Prefetch-Control'] = 'off' # also in the frontend


    logger.info(msg="Server Setup Complete...")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
