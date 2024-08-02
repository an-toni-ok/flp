from flask import Blueprint, request, Response, session, current_app, render_template
from celery.result import AsyncResult

from server.celery_tasks import add_together
from server.decorators import validate
from server.schemas import SCHEMA

from server.RedisManager.RunManager import RunManager
from server.RedisManager.SessionManager import SessionManager

routes = Blueprint('routes', __name__)

@routes.get("/")
def index():
    return render_template("index.html")

@routes.post("/area")
@validate(SCHEMA.AREAS)
def area():
    input_data = request.get_json()
    sm = SessionManager(session["id"])
    current_app.logger.debug(
        f"Loaded session with id \"{ sm.session_id }\"."
    )

    rm = RunManager(sm.session_id, sm.current_run_nr)
    current_app.logger.debug(f"Loaded run with id \"{ rm.run_id }\".")
    
    rm.input.areas = input_data
    return Response(status=200)

@routes.post("/process")
@validate(SCHEMA.PRODUCTION_STEPS)
def process():
    input_data = request.get_json()
    sm = SessionManager(session["id"])
    rm = RunManager(sm.session_id, sm.current_run_nr)
    rm.input.steps = input_data
    
    return Response(status=200)

@routes.post("/machines")
@validate(SCHEMA.MACHINES)
def machines():
    input_data = request.get_json()
    sm = SessionManager(session["id"])
    rm = RunManager(sm.session_id, sm.current_run_nr)
    rm.input.machines = input_data
    
    return Response(status=200)

@routes.post("/objectives")
@validate(SCHEMA.OBJECTIVES)
def objectives():
    input_data = request.get_json()
    sm = SessionManager(session["id"])
    rm = RunManager(sm.session_id, sm.current_run_nr)
    rm.input.objectives = input_data
    
    return Response(status=200)

@routes.post("/optimize")
def optimize_start():
    sm = SessionManager(session["id"])
    rm = RunManager(sm.session_id, sm.current_run_nr)
    rm.start()

    return Response(status=200)

@routes.get("/optimize")
def optimize_status():
    sm = SessionManager(session["id"])
    rm = RunManager(sm.session_id, sm.current_run_nr)
    
    return Response(rm.status, status=200)

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
