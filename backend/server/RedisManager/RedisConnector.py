from enum import Enum
from typing import Dict, List

from server.extensions import redis
from .util import RunStatus
from .Errors import InvalidChangeMethod, RunAlreadyExists, RunNotCreated, SessionIdNotSet

class RedisInput(Enum):
    ALL = "all"
    AREAS = "areas"
    R_AREAS = "restricted_areas"
    TECHNOLOGIES = "technologies"
    STEPS = "production_steps"
    MACHINES = "machines"
    OBJECTIVES = "objectives"
    CYCLE_TIME = "target_cycle_time"
    OPERATOR_COST = "hourly_operator_cost"

    def query(self, run_id):
        global redis

        return redis.json().get(run_id, str(self))[0]
    
    def set(self, run_id, data):
        global redis
 
        redis.json().set(run_id, str(self), data)
    
    def __str__(self) -> str:
        if self.value == RedisInput.ALL.value:
            return f"$.input"
        return f"$.input.{self.value}"
    
class RedisRunConfig(Enum):
    ALL = "all"
    OUTPUT = "output"
    EXECUTION_ID = "execution_id"
    STATUS = "status"

    def query(self, run_id):
        global redis
 
        return redis.json().get(run_id, str(self))[0]
    
    def set(self, run_id, data: Dict):
        global redis

        try:
            run_input = redis.json().get(run_id)["input"]
        except:
            raise RunNotCreated(run_id)

        if self.value == RedisRunConfig.ALL.value:
            if data.get("input") is None:
                # Set the input data  to the currently set state 
                # so that the rest of the dict can be updated with 
                # the input data remaining unchanged
                data["input"] = run_input
            elif data["input"] != run_input:
                raise InvalidChangeMethod()

        redis.json().set(run_id, str(self), data)

    def create(session_id):
        """Creates a new run in a session.

        Args:
            session_id (_type_): The user session id.

        Raises:
            SessionIdNotSet: The session id supplied does not exist.

        Returns:
            _type_: The run id of the new run.
        """
        global redis

        try:
            run_nr = redis.json().get(session_id, "$.current_run_nr")[0]
            run_id = f"{session_id}_{run_nr}"
        except TypeError:
            raise SessionIdNotSet(session_id)
        
        redis.json().set(session_id, "$.current_run_nr", run_nr + 1)
        redis.json().arrappend(session_id, "$.run_ids", run_id)

        redis.json().set(run_id, "$", {
            'input': {
                'areas': [], 
                'restricted_areas': [], 
                'technologies': [], 
                'production_steps': [], 
                'machines': [], 
                'objectives': {}, 
                'target_cycle_time': None, 
                'hourly_operator_cost': None
            }, 
            'output': {}, 
            'execution_id': None, 
            'status': RunStatus.INPUT.value
        })

        return run_id
    
    def __str__(self) -> str:
        if self.value == RedisRunConfig.ALL.value:
            return f"$"
        return f"$.{self.value}"

class RedisSession:
    def contains(session_id):
        global redis
 
        return bool(redis.sismember("session_ids", session_id))

    def create_session(session_id):
        global redis
 
        redis.sadd("session_ids", session_id)
        redis.json().set(session_id, "$", {
            "current_run_nr": 0,
            "run_ids": []
        })

    def run_ids(session_id) -> List:
        """Gets the run ids associated with the session id.

        Args:
            session_id (_type_): The session id of the run.

        Raises:
            Exception: Thrown if the Session isn't set.

        Returns:
            int: The run id of the new run.
        """
        global redis

        try:
            run_ids = redis.json().get(session_id, "$.run_ids")
        except TypeError:
            raise SessionIdNotSet(session_id)

        return run_ids

    def current_run_nr(session_id) -> int:
        """Gets the run nr of the current run.

        Args:
            session_id (_type_): The session id of the run.

        Raises:
            Exception: Thrown if the Session isn't set.

        Returns:
            int: The run id of the new run.
        """
        global redis

        try:
            run_nr = redis.json().get(session_id, "$.current_run_nr")[0]
        except TypeError:
            raise SessionIdNotSet(session_id)

        return run_nr

    def create_run(session_id) -> int:
        """Creates a new run in the redis session data storage.

        Args:
            session_id (_type_): The session id where the run is created.

        Raises:
            Exception: Thrown if the Session isn't set.

        Returns:
            int: The run id of the new run.
        """
        global redis

        try:
            run_nr = redis.json().get(session_id, "$.current_run_nr")[0]
            run_id = f"{session_id}_{run_nr}"
        except TypeError:
            raise SessionIdNotSet(session_id)
        
        redis.json().set(session_id, "$.current_run_nr", run_nr + 1)
        redis.json().arrappend(session_id, "$.run_ids", run_id)
        return run_id

class RedisIdCounter:
    def incr():
        global redis

        return redis.incr("session_id_counter")
