from flask import Response, jsonify
from werkzeug.exceptions import HTTPException


def handle_http_exception(e: HTTPException) -> Response:
    """
    Auto handler for specific http exceptions that should return a non-generic description.
    Ex. 400, 404
    """
    response: Response = jsonify(
        {"status": "error", "message": e.description, "code": e.code}
    )

    response.status_code = e.code
    return response


def handle_generic_exception(e: HTTPException) -> Response:
    """
    Auto handler for specific http exceptions that should return a generic description.
    Ex. Server Errors
    """
    response: Response = jsonify(
        {
            "status": "error",
            "message": "Unexpected error on the server side",
            "code": 500,
        }
    )
    response.status_code = 500
    return response

def success_response(code, data) -> Response:
    """
    Returns a successful response with the given data.
    """
    return jsonify({"status": "success", "code": code, "data": data})
