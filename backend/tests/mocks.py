from enum import Enum
from typing import Dict, List

from server.RedisManager.Errors import InvalidChangeMethod
from server.RedisManagerOld.util import RunStatus
from server.RedisManager.RedisConnector import RedisInput, RedisRunConfig

mock_input_data = {
    'areas': [], 
    'restricted_areas': [], 
    'technologies': [], 
    'production_steps': [], 
    'machines': [], 
    'objectives': {}, 
    'target_cycle_time': None, 
    'hourly_operator_cost': None
}

class MockRedisInput(Enum):
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
        global mock_input_data
        if self.value == RedisInput.ALL.value:
            return mock_input_data
        return mock_input_data.get(self.value)

    def set(self, run_id, data):
        global mock_input_data
        if self.value == RedisInput.ALL.value:
            mock_input_data = data
            return
        mock_input_data[self.value] = data

    def hidden_set(self, label: str, data: Dict|List|int):
        global mock_input_data
        mock_input_data[label] = data

    def hidden_reset(self):
        global mock_input_data
        mock_input_data = {}
    
    def __str__(self) -> str:
        if self.value == RedisInput.ALL.value:
            return f"$.input"
        return f"$.input.{self.value}" 

mock_run_config_data = {
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
}

class MockRedisRunConfig(Enum):
    ALL = "all"
    OUTPUT = "output"
    EXECUTION_ID = "execution_id"
    STATUS = "status"

    def query(self, run_id):
        global mock_run_config_data
        if self.value == RedisRunConfig.ALL.value:
            return mock_run_config_data
        return mock_run_config_data.get(self.value)
    
    def set(self, run_id, data: Dict):
        global mock_run_config_data

        if self.value == RedisRunConfig.ALL.value:
            if data.get("input") is None:
                # Set the input data  to the currently set state 
                # so that the rest of the dict can be updated with 
                # the input data remaining unchanged
                data["input"] = mock_input_data
            elif data["input"] != mock_input_data:
                raise InvalidChangeMethod()
            
            mock_run_config_data = data
            return

        mock_run_config_data[self.value, data]

    def create(run_id):
        return
    
    def __str__(self) -> str:
        if self.value == RedisRunConfig.ALL.value:
            return f"$"
        return f"$.{self.value}"
