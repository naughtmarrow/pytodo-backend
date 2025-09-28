# mypy: check-untyped-defs
import logging

from flask import Blueprint, abort, request
from flask_login import (  # type: ignore
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from psycopg2.errors import (
    NoData,
    UniqueViolation,
)  # probably should change this to use custom errors like "User Error" to decide what to send back
from pydantic import ValidationError  # same as above here...

from src.core import User, check_password, set_password
from src.data import (
    TransactionManager,
    delete_user,
    get_user_id,
    get_user_password,
    save_user,
    update_user,
)
from src.routes.responses import success_response

_logger = logging.getLogger("USERROUTE")
user_blueprint: Blueprint = Blueprint("user_bp", __name__, url_prefix="/users")

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    with TransactionManager() as conn:
        return get_user_id(user_id, conn)


@user_blueprint.route("/login", methods=["POST"])
def _login_user_route():
    try:
        if not request.is_json:
            raise TypeError("Request content must be json")

        content = request.get_json()

        username = content["username"]
        raw_text_password = content["password"]

        with TransactionManager() as conn:
            user_id, password_hash = get_user_password(username, conn)

            valid_user = check_password(password_hash, raw_text_password)
            if not valid_user:
                raise ValidationError
            else:
                user = load_user(user_id)
                login_user(user)

            return success_response(
                201, {"msg": "User has been verified successfully", "id": user.id}
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


@user_blueprint.route("/logout", methods=["GET"])
@login_required
def _logout_user_route():
    logout_user()
    return success_response(200, {"msg:", "Logged out succesfully"})


@user_blueprint.route("/", methods=["POST"])
def _post_user_route():
    try:
        if not request.is_json:
            raise TypeError("Request content must be json")

        content = request.get_json()
        new_user: User = User(
            id=None, username=content["username"], password=None, authenticated=False
        )

        raw_text_password = content["password"]
        set_password(new_user, raw_text_password)

        with TransactionManager() as conn:
            user_id: int = save_user(new_user, conn)

            return success_response(
                201, {"msg": "Object has been created successfully", "id": user_id}
            )

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
@login_required
def _put_user_route():
    try:
        if not request.is_json:
            raise TypeError("Request content must be json")

        content = request.get_json()
        user: User = User(
            current_user.id,
            username=content["username"],
            password=None,  # maybe i should remove the password altogether, no need to have it here i don't think
        )

        with TransactionManager() as conn:
            user_id = update_user(user, conn)  # this method does not call a password

            return success_response(
                201, {"msg": "Object has been updated successfully", "id": user_id}
            )

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


@user_blueprint.route("/", methods=["DELETE"])
@login_required
def _delete_user_route():
    try:
        with TransactionManager() as conn:
            user = get_user_id(current_user.id, conn)
            delete_user(user, conn)
            logout_user()

            return success_response(
                200, {"msg": "Object has been deleted successfully"}
            )

    except NoData:
        abort(404, description="User not found")
    except Exception as e:
        _logger.error(msg=f"Unkwown error in DELETE user route: {e}")
        abort(500)
