from flask import Blueprint, request, abort
from celery.result import AsyncResult

from server.celery_tasks import add_together
from server.decorators import validate
from server.schemas import SCHEMA

routes = Blueprint('routes', __name__)

@routes.post("/area")
@validate(SCHEMA.AREAS)
def area():
    areas = request.get_json()

    return areas


@routes.post("/process")
@validate(SCHEMA.PRODUCTION_STEPS)
def process():
    process = request.get_json()

    return process


@routes.post("/machines")
@validate(SCHEMA.MACHINES)
def machines():
    process = request.get_json()

    return process


@routes.post("/objectives")
@validate(SCHEMA.OBJECTIVES)
def objectives():
    process = request.get_json()

    return process


@routes.post("/optimize")
def optimize_start():
    process = request.get_json()

    return process


@routes.get("/optimize")
def optimize_status():
    process = request.get_json()

    return process

@routes.get("/add/<num1>/<num2>")
def add_route(num1: str, num2: str) -> dict[str, object]:
    result = add_together.delay(int(num1), int(num2))
    return {"result_id": result.id}

@routes.get("/result/<id>")
def get_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }
