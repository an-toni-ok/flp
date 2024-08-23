from typing import Dict, List, Tuple

from .RedisConnector import RedisInput, RedisRunConfig
from .Errors import InputNotSettable
from .util import RunStatus

class RunInput:
    """Sets and gets input data.
    """
    def __init__(self, run_id):
        """Creates a RunInput class for a run

        Args:
            run_id (_type_): The id of the run
        """
        self.run_id: str = run_id

        self._areas = None
        self._steps = None
        self._machines = None
        self._objectives = None

    def json(self):
        """Returns the input data as json

        Returns:
            Dict: The input data
        """
        return RedisInput.ALL.query(self.run_id)

    def _assure_input_settable(self):
        status = RunStatus[RedisRunConfig.STATUS.query(self.run_id)]
        if not status == RunStatus.INPUT:
            raise InputNotSettable(status.value)
        
    def is_startable(self) -> bool:
        """Checks if all necessary fields are set for
        starting the automation.

        Returns:
            Boolean: The automation is startable.
        """
        return (
            self.areas["areas"] and self.steps and self.machines and self.objectives["objectives"] and self.objectives["target_cycle_time"] and self.objectives["hourly_operator_cost"]
        )

    @property
    def areas(self):
        return {
            "areas": RedisInput.AREAS.query(self.run_id),
            "restricted_areas": RedisInput.R_AREAS.query(self.run_id)
        }

    @property
    def steps(self):
        return RedisInput.STEPS.query(self.run_id)

    @property
    def machines(self):
        return RedisInput.MACHINES.query(self.run_id)

    @property
    def objectives(self):
        return {
            "objectives": RedisInput.OBJECTIVES.query(self.run_id),
            "target_cycle_time": RedisInput.CYCLE_TIME.query(self.run_id),
            "hourly_operator_cost": RedisInput.OPERATOR_COST.query(self.run_id)
        }

    def _set_technologies(self):
        """Collects all the technologies in the
        machines and production steps and saves them.
        """
        machines = self.machines
        steps = self.steps
        
        unique_technologies = set()
        if steps:
            for step in steps:
                step_tech = step.get("technology")
                if step_tech is not None:
                    unique_technologies.add(step_tech)

        if machines:
            for machine in machines:
                machine_tech = machine.get("technologies")
                if machine_tech is not None:
                    for technology in machine_tech:
                        unique_technologies.add(technology)

        technologies = list(unique_technologies)
        RedisInput.TECHNOLOGIES.set(self.run_id, technologies)

    @areas.setter
    def areas(self, data: Dict):
        self._assure_input_settable()
        
        if data == self.areas:
            return

        RedisInput.AREAS.set(self.run_id, data["areas"])
        RedisInput.R_AREAS.set(self.run_id, data["restricted_areas"])

    @steps.setter
    def steps(self, data: List):
        self._assure_input_settable()
        
        if data == self.steps:
            return

        # Update steps
        RedisInput.STEPS.set(self.run_id, data)
        # Update technologies
        self._set_technologies()

    @machines.setter
    def machines(self, data: List):
        self._assure_input_settable()
        
        if data == self.machines:
            return 

        # Update Machines
        RedisInput.MACHINES.set(self.run_id, data)
        # Update technologies
        self._set_technologies()

    @objectives.setter
    def objectives(self, data: Dict):
        self._assure_input_settable()

        if data == self.objectives:
            return
        
        RedisInput.OBJECTIVES.set(self.run_id, data["objectives"])
        RedisInput.CYCLE_TIME.set(self.run_id, data["target_cycle_time"])
        RedisInput.OPERATOR_COST.set(self.run_id, data["hourly_operator_cost"])
        
    def __eq__(self, other) -> bool:
        """Comparison method for class instances.

        Args:
            other (_type_): comparison object

        Returns:
            bool: Comparison result
        """
        # This method needs to be implemented in order for
        # comparisons to work. If it is not implemented the 
        # comparison is done by memory addresses.
        if not isinstance(other, RunInput):
            return False
        return self.run_id == other.run_id
