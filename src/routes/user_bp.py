# mypy: check-untyped-defs

from flask import Blueprint, Response, abort, request
from psycopg2.errors import NoData, NoDataFound, UniqueViolation
from pydantic import ValidationError

from src.core import User
from src.data import (
    TransactionManager,
    delete_user,
    get_user_id,
    save_user,
    update_user,
)
from src.routes.responses import success_response

user_blueprint: Blueprint = Blueprint("user_bp", __name__, url_prefix="/users")


@user_blueprint.route("/<user_id>", methods=["GET"])
def _get_user_id_route(user_id):
    try:
        with TransactionManager() as conn:
            user: User = get_user_id(user_id, conn)
            user.password = "secret"  # HACK: YOU SHOULD FIGURE OUT HOW TO NOT HAVE PASSWORDS ALL OVER THE PLACE

            response: Response = success_response(200, user.model_dump())
            response.status_code = 200
            return response

    except (NoData, NoDataFound) as e:
        # TODO: add logging here with e
        print(e)
        abort(404, description=f"User with id {user_id} not found")
    except Exception as e:
        # TODO: add logging here with e
        print(e)
        abort(500)


@user_blueprint.route("/", methods=["POST"])
def _post_user_route():
    try:
        if not request.is_json:
            raise TypeError("Request content must be json")

        content = request.get_json()
        user: User = User(
            id=None, username=content["username"], password=content["password"]
        )

        with TransactionManager() as conn:
            user_id: int = save_user(user, conn)

            response: Response = success_response(
                201, {"msg": "Object has been created successfully", "id": user_id}
            )
            response.status_code = 201
            return response

    except UniqueViolation as e:
        # TODO: add logging here with e
        print(e)
        abort(
            400,
            description="Username must be unique",
        )

    except (ValidationError, TypeError, KeyError) as e:
        # TODO: add logging here with e
        print(e)
        abort(
            400,
            description="Invalid request data (make sure all fields are full and properly formatted)",
        )

    except Exception as e:
        # TODO: add logging here with e
        print(e)
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
            # probably don't need to get the user but i don't think it hurts too much for now
            # WARN: other than the password stuff but i should fix that elsewhere anyways
            user_upd: User = update_user(user, conn)

            response: Response = success_response(
                201, {"msg": "Object has been updated successfully", "id": user_upd.id}
            )
            response.status_code = 201
            return response

    except UniqueViolation as e:
        # TODO: add logging here with e
        print(e)
        abort(
            400,
            description="Username must be unique",
        )

    except (ValidationError, TypeError, KeyError) as e:
        # TODO: add logging here with e
        print(e)
        abort(
            400,
            description="Invalid request data (make sure all fields are full and properly formatted)",
        )

    except Exception as e:
        # TODO: add logging here with e
        print(e)
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
        # TODO: add logging here with e
        abort(404, description="User not found")
    except Exception:
        # TODO: add logging here with e
        abort(500)
