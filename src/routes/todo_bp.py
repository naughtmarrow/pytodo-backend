# mypy: check-untyped-defs
import logging
from datetime import datetime
from typing import Dict, List

from flask import Blueprint, Response, abort, request
from flask_login import login_required, current_user  # type: ignore
from psycopg2.errors import NoData, NoDataFound
from pydantic import ValidationError

from src.core import Todo
from src.data import (
    TransactionManager,
    delete_todo,
    get_todo_id,
    get_todos_from_user,
    save_todo,
    update_todo,
)
from src.routes.responses import success_response

_logger = logging.getLogger("TODOROUTE")
todo_blueprint: Blueprint = Blueprint("todo_bp", __name__, url_prefix="/todos")


@todo_blueprint.route("/", methods=["GET"])
@login_required
def _get_todos_from_user_route():
    try:
        with TransactionManager() as conn:
            tdlist: List[Todo] = get_todos_from_user(current_user.id, conn)
            tdlist_dict: List[Dict] = []
            for x in tdlist:
                tdlist_dict.append(x.model_dump())

            response: Response = success_response(200, tdlist_dict)
            response.status_code = 200

            return response
    except (NoData, NoDataFound):
        abort(404, description="No todos found for given user")
    except Exception as e:
        _logger.error(msg=f"Unkwown error in todo GET list from user route: {e}")
        abort(500)


@todo_blueprint.route("/", methods=["POST"])
@login_required
def _post_todo_route():
    try:
        if not request.is_json:
            raise TypeError("Request content must be json")

        content = request.get_json()
        todo: Todo = Todo(
            id=None,
            user_id=current_user.id,
            description=content["description"],
            date_created=datetime.now(),  # HACK: PROBABLY SHOULD DO THIS IN SOME SORT OF CONSTRUCTOR
            date_due=content["date_due"],
            priority=content["priority"],
            completed=content["completed"],
        )

        with TransactionManager() as conn:
            todo_id: int = save_todo(todo, conn)

            response: Response = success_response(
                201, {"msg": "Object has been created successfully", "id": todo_id}
            )
            response.status_code = 201
            return response

    except (ValidationError, TypeError, KeyError) as e:
        _logger.warn(msg=f"Validation error in POST todo route: {e}")
        abort(
            400,
            description="Invalid request data (make sure all fields are full and properly formatted)",
        )

    except Exception as e:
        _logger.error(msg=f"Unkwown error in POST todo route: {e}")
        abort(500)


@todo_blueprint.route("/", methods=["PUT"])
@login_required
def _put_todo_route():
    try:
        if not request.is_json:
            raise TypeError("Request content must be json")

        content = request.get_json()
        todo: Todo = Todo(
            id=content["id"],
            user_id=current_user.id,
            description=content["description"],
            date_created=content["date_created"], # just easier this way honestly
            date_due=content["date_due"],
            priority=content["priority"],
            completed=content["completed"],
        )

        with TransactionManager() as conn:
            todo_id: Todo = update_todo(todo, conn)

            response: Response = success_response(
                201, {"msg": "Object has been updated successfully", "id": todo_id}
            )
            response.status_code = 201
            return response

    except (ValidationError, TypeError, KeyError) as e:
        _logger.warn(msg=f"Validation error in PUT todo route: {e}")
        abort(
            400,
            description="Invalid request data (make sure all fields are full and properly formatted)",
        )

    except Exception as e:
        _logger.error(msg=f"Unkwown error in PUT todo route: {e}")
        abort(500)


@todo_blueprint.route("/<todo_id>", methods=["DELETE"])
@login_required
def _delete_todo_route(todo_id):
    try:
        with TransactionManager() as conn:
            todo = get_todo_id(todo_id, conn)
            delete_todo(todo, conn)

            response: Response = success_response(
                200, {"msg": "Object has been deleted successfully"}
            )
            response.status_code = 200
            return response

    except NoData:
        abort(404, description="Todo not found")
    except Exception as e:
        _logger.error(msg=f"Unkwown error in PUT todo route: {e}")
        abort(500)
