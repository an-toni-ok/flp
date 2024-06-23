from flask import Blueprint, request, Response, session, current_app
from celery.result import AsyncResult

from server.celery_tasks import add_together
from server.decorators import validate
from server.schemas import SCHEMA
from server.extensions import redis_client

from server.RedisManager.RunManager import RunManager
from server.RedisManager.SessionManager import SessionManager
from server.RedisManager.util import RunInputType


routes = Blueprint('routes', __name__)

@routes.post("/area")
@validate(SCHEMA.AREAS)
def area():
    input_data = request.get_json()
    sm = SessionManager(
        session_id=session["id"], 
        redis=redis_client,
        logger=current_app.logger
    )
    current_app.logger.debug(f"Recieved input data on endpoint /area in session {sm.session_id}. Data is {input_data}.")
    rm: RunManager = sm.load_run(
        redis=redis_client, 
        logger=current_app.logger
    )
    rm.set_input(input_data, RunInputType.AREA, redis_client)
    
    return Response(status=200)

@routes.post("/process")
@validate(SCHEMA.PRODUCTION_STEPS)
def process():
    input_data = request.get_json()
    sm = SessionManager(
        session_id=session["id"], 
        redis=redis_client,
        logger=current_app.logger
    )
    current_app.logger.debug(f"Recieved input data on endpoint /process in session {sm.session_id}. Data is {input_data}.")
    rm: RunManager = sm.load_run(
        redis=redis_client, 
        logger=current_app.logger
    )
    rm.set_input(input_data, RunInputType.STEPS, redis_client)
    
    return Response(status=200)

@routes.post("/machines")
@validate(SCHEMA.MACHINES)
def machines():
    input_data = request.get_json()
    sm = SessionManager(
        session_id=session["id"], 
        redis=redis_client,
        logger=current_app.logger
    )
    current_app.logger.debug(f"Recieved input data on endpoint /area in session {sm.session_id}. Data is {input_data}.")
    rm: RunManager = sm.load_run(
        redis=redis_client, 
        logger=current_app.logger
    )
    rm.set_input(input_data, RunInputType.MACHINES, redis_client)
    
    return Response(status=200)

@routes.post("/objectives")
@validate(SCHEMA.OBJECTIVES)
def objectives():
    input_data = request.get_json()
    sm = SessionManager(
        session_id=session["id"], 
        redis=redis_client,
        logger=current_app.logger
    )
    current_app.logger.debug(f"Recieved input data on endpoint /area in session {sm.session_id}. Data is {input_data}.")
    rm: RunManager = sm.load_run(
        redis=redis_client, 
        logger=current_app.logger
    )
    rm.set_input(input_data, RunInputType.OBJECTIVES, redis_client)
    
    return Response(status=200)

@routes.post("/optimize")
def optimize_start():
    sm = SessionManager(
        session_id=session["id"], 
        redis=redis_client,
        logger=current_app.logger
    )
    rm: RunManager = sm.load_run(
        redis=redis_client, 
        logger=current_app.logger
    )
    rm.start_run(redis=redis_client)

    return Response(status=200)

@routes.get("/optimize")
def optimize_status():
    return Response(status=200)

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
