from enum import Enum
from typing import Dict, List

from server.extensions import redis
from .util import RunStatus
from .Errors import InvalidChangeMethod, RunAlreadyExists, RunNotCreated, SessionIdNotSet

class RedisInput(Enum):
    """Interaction with the Redis Run data input storage.

    Allows setting and querying input fields of a run. The chosen enum option is set or queried.
    """
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
        """Gets the value of the key corresponding to the Enum key.

        Args:
            run_id (_type_): The id of the run

        Returns:
            _type_: The value of the key corresponding to the Enum key
        """
        global redis

        return redis.json().get(run_id, str(self))[0]
    
    def set(self, run_id, data):
        """Sets the value of the key corresponding to the Enum key

        Args:
            run_id (_type_): The id of the run
            data (Dict): The data to set the value to

        Raises:
            RunNotCreated: No run with the id run_id exists
            InvalidChangeMethod: Setting input data with this function is not allowed
        """
        global redis
 
        redis.json().set(run_id, str(self), data)
    
    def __str__(self) -> str:
        """The string formatting method of the class

        Returns:
            str: The value returned when formatting the class as a string.
        """
        if self.value == RedisInput.ALL.value:
            return f"$.input"
        return f"$.input.{self.value}"
    
class RedisRunConfig(Enum):
    """Interaction with the Redis Run data storage (with the exception of the input, use RedisInput for this).

    Allows setting or quering management data of a run or for creation of a new run. The chosen enum option is set or queried.
    """
    ALL = "all"
    OUTPUT = "output"
    STATUS = "status"

    def query(self, run_id):
        """Gets the value of the key corresponding to the Enum key.

        Args:
            run_id (_type_): The id of the run

        Returns:
            _type_: The value of the key corresponding to the Enum key
        """
        global redis
 
        return redis.json().get(run_id, str(self))[0]
    
    def set(self, run_id, data: Dict):
        """Sets the value of the key corresponding to the Enum key

        Args:
            run_id (_type_): The id of the run
            data (Dict): The data to set the value to

        Raises:
            RunNotCreated: No run with the id run_id exists
            InvalidChangeMethod: Setting input data with this function is not allowed
        """
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
            run_nr = redis.json().get(session_id, "$.current_run_nr")[0] + 1
            run_id = f"{session_id}_{run_nr}"
        except TypeError:
            raise SessionIdNotSet(session_id)
        
        redis.json().set(session_id, "$.current_run_nr", run_nr)
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
            'status': RunStatus.INPUT.value
        })

        return run_id
    
    def __str__(self) -> str:
        """The string formatting method of the class

        Returns:
            str: The value returned when formatting the class as a string.
        """
        if self.value == RedisRunConfig.ALL.value:
            return f"$"
        return f"$.{self.value}"

class RedisSession:
    """Contains methods for interaction with the Redis Session data storage.
    """
    def contains(session_id):
        """Checks if session_id is already used.

        Args:
            session_id (_type_): The session id to check for

        Returns:
            Bool: Is the session id saved
        """
        global redis
 
        return bool(redis.sismember("session_ids", session_id))

    def create_session(session_id):
        """Creates an entry in Redis for the session id.

        Args:
            session_id (_type_): The session id
        """
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

class RedisIdCounter:
    """Wraps the incr Function for the Redis key 'session_id_counter'.
    """

    def incr():
        """Returns the value of the Redis field 'session_id_counter' and increments it.

        This funcion is atomic.

        Returns:
            _type_: The value of the session_id_counter before the increment.
        """
        global redis

        return redis.incr("session_id_counter")
