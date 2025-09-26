from flask import Flask
from werkzeug.exceptions import HTTPException

from src.routes import handle_generic_exception, handle_http_exception, user_blueprint, todo_blueprint


def create_app():
    app = Flask(__name__)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(todo_blueprint)

    app.register_error_handler(500, handle_generic_exception)
    app.register_error_handler(HTTPException, handle_http_exception)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
