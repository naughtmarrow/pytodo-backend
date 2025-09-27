# mypy: check-untyped-defs
import logging

from flask import Blueprint, Response, abort, request
from psycopg2.errors import (
    NoData,
    NoDataFound,
    UniqueViolation,
)  # probably should change this to use custom errors like "User Error" to decide what to send back
from pydantic import ValidationError  # same as above here...

from src.core import User, check_password, set_password
from src.data import (
    TransactionManager,
    delete_user,
    get_user_id,
    get_user_id_from_name,
    get_user_password,
    save_user,
    update_user,
)
from src.routes.responses import success_response

_logger = logging.getLogger("USERROUTE")
user_blueprint: Blueprint = Blueprint("user_bp", __name__, url_prefix="/users")


# WARN: probably should depreciate this method in the future once sessions are properly configured
@user_blueprint.route("/<user_id>", methods=["GET"])
def _get_user_id_route(user_id):
    try:
        with TransactionManager() as conn:
            user: User = get_user_id(user_id, conn)
            user.password = (
                None  #  we don't want to ever send a password to the frontend
            )

            response: Response = success_response(200, user.model_dump())
            response.status_code = 200
            return response

    except (NoData, NoDataFound):
        abort(404, description=f"User with id {user_id} not found")
    except Exception as e:
        _logger.error(msg=f"Unkwown error in todo GET list from user route: {e}")
        abort(500)


# WARN: probably should use a form and flaskwtf instead of raw json in the future
@user_blueprint.route("/login", methods=["POST"])
def _login_user_route():
    try:
        if not request.is_json:
            raise TypeError("Request content must be json")

        content = request.get_json()

        username = content["username"]
        raw_text_password = content["password"]


        with TransactionManager() as conn:
            password_hash = get_user_password(username, conn)

            valid_user = check_password(password_hash, raw_text_password)
            if not valid_user:
                raise ValidationError
            else:
                user_id = get_user_id_from_name(username, conn)

            response: Response = success_response(
                201, {"msg": "User has been verified successfully", "id": user_id}
            )
            response.status_code = 201
            return response

    except UniqueViolation as e:
        _logger.warn(msg=f"Unique Violation in POST user route: {e}")
        abort(
            400,
            description="Username must be unique",
        )

    except (ValidationError, TypeError, KeyError) as e:
        _logger.warn(msg=f"Validation error in POST user route: {e}")
        abort(
            400,
            description="Invalid request data (make sure all fields are full and properly formatted)",
        )

    except Exception as e:
        _logger.error(msg=f"Unkwown error in POST user route: {e}")
        abort(500)


# WARN: probably should use a form and flaskwtf instead of raw json in the future
@user_blueprint.route("/", methods=["POST"])
def _post_user_route():
    try:
        if not request.is_json:
            raise TypeError("Request content must be json")

        content = request.get_json()
        new_user: User = User(id=None, username=content["username"], password=None)

        raw_text_password = content["password"]
        set_password(new_user, raw_text_password)

        with TransactionManager() as conn:
            user_id: int = save_user(new_user, conn)

            response: Response = success_response(
                201, {"msg": "Object has been created successfully", "id": user_id}
            )
            response.status_code = 201
            return response

    except UniqueViolation as e:
        _logger.warn(msg=f"Unique Violation in POST user route: {e}")
        abort(
            400,
            description="Username must be unique",
        )

    except (ValidationError, TypeError, KeyError) as e:
        _logger.warn(msg=f"Validation error in POST user route: {e}")
        abort(
            400,
            description="Invalid request data (make sure all fields are full and properly formatted)",
        )

    except Exception as e:
        _logger.error(msg=f"Unkwown error in POST user route: {e}")
        abort(500)


@user_blueprint.route("/", methods=["PUT"])
def _put_user_route():
    try:
        if not request.is_json:
            raise TypeError("Request content must be json")

        content = request.get_json()
        user: User = User(
            id=content["id"], username=content["username"], password=content["password"]
        )

        with TransactionManager() as conn:
            user_id = update_user(user, conn)

            response: Response = success_response(
                201, {"msg": "Object has been updated successfully", "id": user_id}
            )
            response.status_code = 201
            return response

    except UniqueViolation as e:
        _logger.warn(msg=f"Unique Violation in POST user route: {e}")
        abort(
            400,
            description="Username must be unique",
        )

    except (ValidationError, TypeError, KeyError) as e:
        _logger.warn(msg=f"Validation error in PUT user route: {e}")
        abort(
            400,
            description="Invalid request data (make sure all fields are full and properly formatted)",
        )

    except Exception as e:
        _logger.error(msg=f"Unkwown error in PUT user route: {e}")
        abort(500)


@user_blueprint.route("/<user_id>", methods=["DELETE"])
def _delete_user_route(user_id):
    try:
        with TransactionManager() as conn:
            user = get_user_id(user_id, conn)
            delete_user(user, conn)

            response: Response = success_response(
                200, {"msg": "Object has been deleted successfully"}
            )
            response.status_code = 200
            return response

    except NoData:
        abort(404, description="User not found")
    except Exception as e:
        _logger.error(msg=f"Unkwown error in DELETE user route: {e}")
        abort(500)
