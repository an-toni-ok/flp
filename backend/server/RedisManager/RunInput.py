from logging import Logger
from typing import Dict, List
from redis import Redis

from .util import RunInputType, RunStatus

class RunInputData:
    """Manages the Input Data for a run. 
    
    Input data from the endpoints added into this class will automatically stored within redis in the correct format so that a generation of an input file for running the optimization is unnecessary.

    It is assumed that Redis already contains the entry at run_id, therefore the class starts by setting all the internal values to their equivalent in the Redis server. An exception will be thrown if the entry does not exist.

    Methods:
    - set(...): Sets the data of the specified Endpoint internally and on the Redis server.
    - file(): Generates the current input file, if all options are set.
    """
    def __init__(self, run_id, redis: Redis, logger: Logger):
        self.logger = logger

        self.run_id: str = run_id
        input_data = redis.json().get(run_id, '$.input')[0]

        self._areas: Dict = input_data["areas"]
        self._restricted_areas: Dict = input_data["restricted_areas"]
        self._technologies: List[str] = input_data["technologies"]
        self._production_steps: Dict = input_data["production_steps"]
        self._machines: Dict = input_data["machines"]
        self._objectives: Dict = input_data["objectives"]
        self._target_cycle_time: int = input_data["target_cycle_time"]
        self._hourly_operator_cost: int = input_data["hourly_operator_cost"]

    def set_input(self, data: Dict, data_type: RunInputType, redis: Redis):
        # Another connection by the same user to the server or a Run completing might change the Status in the Redis server instance. Therefore it's best to query the value whenever needing it.
        status = RunStatus[redis.json().get(self.run_id)["status"]]
        if status is not RunStatus.INPUT:
            raise Exception("Input data not changable anymore.")
        
        match data_type:
            case RunInputType.AREA:
                self._set_area(data=data, redis=redis)
            case RunInputType.STEPS:
                self._set_steps(data=data, redis=redis)
            case RunInputType.MACHINES:
                self._set_machines(data=data, redis=redis)
            case RunInputType.OBJECTIVES:
                self._set_objectives(data=data, redis=redis)
    
    def get_input_file(self):
        if not self.check_all_inputs_set():
            raise Exception("Not all input's are set")
        
        return {
            "areas": self._areas,
            "restricted_areas": self._restricted_areas,
            "technologies": self._technologies,
            "production_steps": self._production_steps,
            "machines": self._machines,
            "objectives": self._objectives,
            "target_cycle_time": self._target_cycle_time,
            "hourly_operator_cost": self._hourly_operator_cost
        }
    
    def check_all_inputs_set(self):
        """Helper function determining if all inputs are set.

        Returns:
            bool: True if all fields are set.
        """
        return (self._areas and self._restricted_areas and self._production_steps and self._machines and self._technologies and self._objectives and self._target_cycle_time and self._hourly_operator_cost)

    def _update_technologies(self, redis: Redis):
        unique_technologies = set()

        for step in self._production_steps:
            unique_technologies.add(step["technology"])

        for machine in self._machines:
            for technology in machine:
                unique_technologies.add(technology)

        self._technologies = list(unique_technologies)
        redis.json().set(self.run_id, "$.technologies", self._technologies)

    def _set_area(self, data: Dict, redis: Redis):
        self._areas = data["areas"]
        redis.json().set(self.run_id, "$.areas", self._areas)

        self._restricted_areas = data["restricted_areas"]
        redis.json().set(self.run_id, "$.restricted_areas", self._restricted_areas)

    def _set_steps(self, data: Dict, redis: Redis):
        self._production_steps = data
        redis.json().set(self.run_id, "$.production_steps", self._production_steps)

        self._update_technologies(redis=redis)

    def _set_machines(self, data: Dict, redis: Redis):
        self._machines = data
        redis.json().set(self.run_id, "$.machines", self._machines)

        self._update_technologies(redis=redis)

    def _set_objectives(self, data: Dict, redis: Redis):
        self._objectives = {
            "invest": data["invest"],
            "cost_per_part": data["cost_per_part"],
            "used_area": data["used_area"],
            "number_operators": data["number_operators"]
        }
        redis.json().set(self.run_id, "$.objectives", self._objectives)

        self._target_cycle_time = data["target_cycle_time"]
        redis.json().set(self.run_id, "$.target_cycle_time", self._target_cycle_time)

        self._hourly_operator_cost = data["hourly_operator_cost"]
        redis.json().set(self.run_id, "$.hourly_operator_cost", self._hourly_operator_cost)
