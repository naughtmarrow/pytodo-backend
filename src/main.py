# mypy: check-untyped-defs
import logging
import os

from flask import Flask, abort, jsonify, make_response, request
from flask_wtf import ( # type: ignore # for some reason mypy struggles with these
    CSRFProtect,
)
from flask_wtf.csrf import generate_csrf  # type: ignore
from werkzeug.exceptions import HTTPException

from src.data import ping_db
from src.routes import (
    handle_generic_exception,
    handle_http_exception,
    login_manager,
    todo_blueprint,
    user_blueprint,
)

csrf = CSRFProtect()


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

    from dotenv import load_dotenv

    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    if os.getenv("Protocol") == "http":
        app.config["WTF_CSRF_SSL_STRICT"] = False
    elif os.getenv("Protocol") == "https":
        app.config["WTF_CSRF_SSL_STRICT"] = True

    csrf.init_app(app)  # adds csrf tokens to all requests/responses
    login_manager.init_app(app)  # sets up the session management

    app.register_blueprint(user_blueprint)
    app.register_blueprint(todo_blueprint)

    app.register_error_handler(500, handle_generic_exception)
    app.register_error_handler(HTTPException, handle_http_exception)

    frontend_url: str = (
        f"{os.getenv('PROTOCOL')}://{os.getenv('FRONT_HOST')}:{os.getenv('FRONT_PORT')}"
    )

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers["Access-Control-Allow-Origin"] = frontend_url
            response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE"
            response.headers["Access-Control-Allow-Headers"] = (
                "Content-Type,Authorization,X-CSRF-Token"
            )
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Max-Age"] = "86400"
            return response

    @app.before_request
    def enforce_json():  # for a bit extra csrf protection since this is a pure json api anyways
        if request.method in [
            "GET",
            "OPTIONS",
        ]:  # these are just get/preflights so we skip
            return

        content_type = request.headers.get("Content-Type", "")
        if not content_type.startswith(
            "application/json"
        ):  # check the content type is json first, not in additional types
            abort(400, description="Content must be json")

        try:
            if request.get_data():
                request.get_json(force=True)  # check that it is valid json
        except Exception as e:
            logger.info(f"json enforcement method caught {e}")

    @app.after_request
    def security_headers(response):
        csp = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'; "  # important for xss prevention
        )  # might need to add more stuff later also this goes in the frontend once i do the division

        response.headers["Content-Security-Policy"] = csp

        response.headers["Access-Control-Allow-Origin"] = frontend_url
        response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE"
        response.headers["Access-Control-Allow-Headers"] = (
            "Content-Type,Authorization,X-CSRF-Token"
        )
        response.headers["Access-Control-Allow-Credentials"] = "true"

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Permissions-Policy"] = (
            "interest-cohort=()"  # goes in the frontend
        )

        response.headers["Server"] = (
            "Pytodo"  # version is hidden in gunicorn but just in case, probably should use a reverse proxy anyways
        )
        response.headers["X-Powered-By"] = "Caffeine"
        response.headers["X-DNS-Prefetch-Control"] = "off"  # also in the frontend

        return response

    @app.route("/csrf")
    def _get_csrf_token():
        return jsonify({"csrf_token": generate_csrf()})

    @app.route("/")
    def _hello_world():
        return "Server up"

    logger.info(msg="Server Setup Complete...")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
