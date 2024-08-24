from flask import Blueprint, request, Response, session, current_app, render_template

from server.RedisManager.util import RunStatus
from server.decorators import validate
from server.schemas import SCHEMA

from server.RedisManager import RunManager, SessionManager

routes = Blueprint('routes', __name__)

@routes.get("/", defaults={"path": ""})
@routes.get("/<path:path>")
def index(path):
    return render_template("index.html")

@routes.get("/load")
def load():
    sm = SessionManager(session["id"])
    rm = RunManager(sm.session_id, sm.current_run_nr)

    return {
        "data": rm.input.json(),
        "status": rm.status
    }

@routes.get('/runs')
def runs():
    sm = SessionManager(session["id"])

    completed_runs = []
    for id in sm.run_ids:
        rm = RunManager(None, None, run_id=id)
        if (rm.status == RunStatus.COMPLETED):
            run_nr = id.split("_")[1]
            completed_runs.append(run_nr)

    return completed_runs

@routes.get("/run/<int:nr>")
def run_nr(nr):
    sm = SessionManager(session["id"])
    rm = RunManager(sm.session_id, nr)
    
    return rm.json()

@routes.get("/new")
def run():
    sm = SessionManager(session["id"])
    RunManager.create(sm.session_id)

    return Response(status=200)

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
    
    return {
        "status": rm.status,
        "output": rm.output
    }
