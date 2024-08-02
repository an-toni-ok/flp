from typing import Dict

from server.celery_tasks import start_optimization
from .RunInput import RunInput
from .util import RunStatus
from .Errors import RunNotStartable, RunNotRunning
from .RedisConnector import RedisRunConfig, RedisSession

class RunManager:
    def __init__(self, user_session_id, run_nr, run_id=None):
        """Creates a RunManager.

        Args:
            user_session_id (_type_): The user session id.
            run_nr (_type_): The number of the run.
            run_id (_type_, optional): The id of the run usable in place of the user_session_id and run_nr. Defaults to None.
        """
        if run_id:
            self.run_id = run_id
        else:
            self.run_id = f"{user_session_id}_{run_nr}"

        self.input = RunInput(run_id=self.run_id)

    @classmethod
    def create(cls, user_session_id):
        """Creates a new run and returns its associated run manager.

        Args:
            user_session_id (_type_): The user session id.

        Returns:
            RunManager: The run manager for the new run.
        """
        run_id = RedisRunConfig.create(user_session_id)
        
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
        """Starts the execution of a run.

        Raises:
            RunNotStartable: The run is not startable
        """
        if self.status is not RunStatus.INPUT:
            raise RunNotStartable(run_id=self.run_id, text="Run is not in the Input stage.")

        if not self.input.is_startable(): 
            raise RunNotStartable(run_id=self.run_id, text="Not all fields are set.")
        
        start_optimization.delay(self.run_id)

    def finish(self, output: Dict, error: bool):
        """Finishes the execution of a run.

        Args:
            output (Dict): The output of the optimization.
            error (bool): An error occurred.

        Raises:
            RunNotRunning: The run is not running.
        """
        if self.status is not RunStatus.RUNNING:
            raise RunNotRunning(run_id=self.run_id)

        # Set output data in redis
        RedisRunConfig.OUTPUT.set(self.run_id, output)
        if (error):
            RedisRunConfig.STATUS.set(self.run_id, RunStatus.ERROR.value)
        else:
            RedisRunConfig.STATUS.set(self.run_id, RunStatus.COMPLETED.value)
