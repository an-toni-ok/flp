from redis import Redis
from typing import Dict
from logging import Logger

from server.celery_tasks import start_optimization
from .RunInput import RunInputData
from .util import RunStatus, RunInputType

class RunManager:
    def __init__(self, user_session_id, run_nr, redis: Redis, logger: Logger):
        self.logger = logger

        self.run_id = f"{user_session_id}_{run_nr}"

        run_data = redis.json().get(self.run_id)
        self.logger.debug(f"Loaded run data for run {run_nr} of session {user_session_id} (run_id: {self.run_id}). Data is {run_data}")

        self.input = RunInputData(run_id=self.run_id, redis=redis, logger=logger)
        self.output = run_data["output"]
        self.execution_id = run_data["execution_id"]

    @classmethod
    def init_new_run(cls, user_session_id, redis: Redis, logger: Logger):
        old_current_run_nr = redis.json().get(user_session_id)["current_run_nr"]
        run_nr = old_current_run_nr + 1
        redis.json().set(user_session_id, "$.current_run_nr", run_nr)
        run_id = f"{user_session_id}_{run_nr}"
        redis.json().arrappend(user_session_id, "$.run_ids", run_id)

        if redis.json().get(run_id, "$"):
            # do not allow overwriting existing data
            raise Exception("Run id already set.")

        redis.json().set(run_id, "$", {
            'input': {
                'areas': {}, 
                'restricted_areas': {}, 
                'technologies': [], 
                'production_steps': {}, 
                'machines': {}, 
                'objectives': {}, 
                'target_cycle_time': None, 
                'hourly_operator_cost': None
            }, 
            'output': {}, 
            'execution_id': None, 
            'status': RunStatus.INPUT.value
        })
        logger.debug(f"Base redis entry was created for run nr {run_nr} of session {user_session_id}")
        
        return cls(user_session_id, run_nr, redis, logger)

    def set_input(self, data: Dict, data_type: RunInputType, redis: Redis):
        self.input.set_input(
            data=data,
            data_type=data_type,
            redis=redis
        )

    def start_run(self, redis: Redis):
        if self.get_run_status(redis) is not RunStatus.INPUT:
            raise Exception("Run is not in the Input stage.")

        if not self.input.check_all_inputs_set(): 
            raise Exception("Not all fields are set.")
        
        # Start run
        self.execution_id = start_optimization.delay(self.run_id)
        redis.json().set(
            self.run_id, 
            "$.execution_id", 
            self.execution_id
        )
        redis.json().set(
            self.run_id, 
            "$.status", 
            RunStatus.RUNNING.value
        )

    def complete_run(self, redis: Redis, output: Dict, error: bool):
        if self.get_run_status(redis) is not RunStatus.RUNNING:
            raise Exception("Run is not running.")

        # Set output data in redis
        redis.json().set(
            self.run_id,
            "$.output",
            output
        )
        status = RunStatus.COMPLETED.value if not error else RunStatus.ERROR.value
        redis.json().set(self.run_id, "$.status", status)

    def get_output(self, redis: Redis):
        run_status = self.get_run_status()
        if run_status not in [RunStatus.COMPLETED, RunStatus.ERROR]:
            raise Exception("Run not yet completed.")
        
        output = redis.json().get(self.run_id, "$")["output"]
        if run_status is RunStatus.ERROR:
            raise Exception(f"During the run execution the following error occurred: {output}")
        
        return output

    def get_run_status(self, redis: Redis):
        # Another connection by the same user to the server or a Run completing might change the Status in the Redis server instance. Therefore it's best to query the value whenever needing it.
        return RunStatus[redis.json().get(self.run_id)["status"]]
