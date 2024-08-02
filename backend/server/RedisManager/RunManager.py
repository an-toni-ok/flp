from redis import Redis
from typing import Dict
from logging import Logger

from server.celery_tasks import start_optimization
from .RunInput import RunInput
from .util import RunStatus, RunInputType
from .RedisConnector import RedisRunConfig, RedisSession

class RunManager:
    def __init__(self, user_session_id, run_nr, run_id=None):
        if run_id:
            self.run_id = run_id
        else:
            self.run_id = f"{user_session_id}_{run_nr}"

        self.input = RunInput(run_id=self.run_id)

    @classmethod
    def init_new_run(cls, user_session_id):
        run_id = RedisSession.create_run(user_session_id)
        RedisRunConfig.create(run_id)
        
        return cls(
            user_session_id, 
            user_session_id=None, 
            run_nr=None, 
            run_id=run_id
        )

    @property
    def output(self):
        return RedisRunConfig.OUTPUT.query(self.run_id)
    
    @property
    def execution_id(self):
        return RedisRunConfig.EXECUTION_ID.query(self.run_id)
    
    @property
    def status(self):
        return RunStatus[RedisRunConfig.STATUS.query(self.run_id)]

    def start(self):
        if self.status is not RunStatus.INPUT:
            raise Exception("Run is not in the Input stage.")

        if not self.input.is_startable(): 
            raise Exception("Not all fields are set.")
        
        start_optimization.delay(self.run_id)

    def finish(self, output: Dict, error: bool):
        if self.status is not RunStatus.RUNNING:
            raise Exception("Run is not running.")

        # Set output data in redis
        RedisRunConfig.OUTPUT.set(self.run_id, output)
        if (error):
            RedisRunConfig.STATUS.set(self.run_id, RunStatus.ERROR.value)
        else:
            RedisRunConfig.STATUS.set(self.run_id, RunStatus.COMPLETED.value)
