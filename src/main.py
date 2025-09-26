import logging

from flask import Flask
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

    logger.info(msg="Server Setup Complete...")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
