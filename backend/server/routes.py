from flask import Blueprint, request, abort
from celery.result import AsyncResult

from server.celery_tasks import add_together
from server.decorators import validate
from server.schemas import SCHEMA

from redis import Redis

routes = Blueprint('routes', __name__)
redis = Redis("redis", 6379, 0, decode_responses=True)

@routes.post("/area")
@validate(SCHEMA.AREAS)
def area():
    areas = request.get_json()
    redis.json().set('areas', '$', areas)
    return areas

@routes.post("/process")
@validate(SCHEMA.PRODUCTION_STEPS)
def process():
    process = request.get_json()
    redis.json().set('process', '$', process)
    return process

@routes.post("/machines")
@validate(SCHEMA.MACHINES)
def machines():
    machines = request.get_json()
    redis.json().set('machines', '$', machines)
    return machines

@routes.post("/objectives")
@validate(SCHEMA.OBJECTIVES)
def objectives():
    objectives = request.get_json()
    redis.json().set('objectives', '$', objectives)
    return objectives

@routes.post("/optimize")
def optimize_start():
    return {}

@routes.get("/optimize")
def optimize_status():
    return {}

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
