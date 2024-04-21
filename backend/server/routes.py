from flask import Blueprint
from celery.result import AsyncResult
from server.celery_tasks import add_together

routes = Blueprint('routes', __name__)

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