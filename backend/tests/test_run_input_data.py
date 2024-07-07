from ast import Tuple
from typing import Dict, List
import pytest
from unittest.mock import patch

from server.RedisManager.util import RunStatus
from server.RedisManager.RedisConnector import RedisInput, RedisRunConfig
from server.RedisManager.RunInput import RunInput
# from server.RedisManager.util import RunStatus

from mocks import MockRedisRunConfig, MockRedisInput

def area_test_data():
    return {
        "areas": [
            {
                "x_position": 1,
                "y_position": 1,
                "x_dimension": 5,
                "y_dimension": 5
            }
        ],
        "restricted_areas": [
            {
                "x_position": 2,
                "y_position": 2,
                "x_dimension": 2,
                "y_dimension": 2   
            }
        ]
    }

def steps_test_data():
    return [
        {
            "technology": "tech_test",
            "work_content": 1,
            "machine_time": "20",
        }
    ]

def machines_test_data():
    return [
        { 
            "technologies": [
                "test_tech1",
                "test_tech2"
            ],
            "hourly_rate": 1,
            "investment_cost": 1,
            "additional_machine_time": 1,
            "x_dimension": 1,
            "y_dimension": 1,
            "x_position": 1,
            "y_position": 1,
            "rotation": 90
        }
    ]

def objectives_test_data():
    return {
        "objectives": { 
            "invest": True,
            "cost_per_part": True,
            "used_area": True,
            "number_operators": True
        },
        "target_cycle_time": 1,
        "hourly_operator_cost": 1
    }

def complete_test_data():
    steps_data = steps_test_data()                    
    machine_data = machines_test_data()
    area_data = area_test_data()
    objectives_data = objectives_test_data()

    technologies = set()
    for step in steps_data:
        technologies.add(step["technology"])
    for machine in machine_data:
        for tech in machine["technologies"]:
            technologies.add(tech)
    technologies = list(technologies)

    return {
        "areas": area_data["areas"],
        "restricted_areas": area_data["restricted_areas"],
        "technologies": technologies,
        "production_steps": steps_data,
        "machines": machine_data,
        'objectives': objectives_data["objectives"], 
        'target_cycle_time': objectives_data["target_cycle_time"], 
        'hourly_operator_cost': objectives_data["hourly_operator_cost"]                
    }

class TestRunInputProperties:
    def test_property_area(self):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            # monkeypatch.setattr('server.RedisManager.RedisConnector', RedisInput, MockRedisInput)
            data = area_test_data()
            MockRedisInput.ALL.hidden_set("areas", data["areas"])
            MockRedisInput.ALL.hidden_set("restricted_areas", data["restricted_areas"])
            
            ri = RunInput("test")
            assert ri.areas == data

    def test_property_steps(self):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            data = steps_test_data()
            MockRedisInput.ALL.hidden_set("production_steps", data)
            ri = RunInput("test")

            assert ri.steps == data

    def test_property_machines(self):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            data = machines_test_data()
            MockRedisInput.ALL.hidden_set("machines", data)
            ri = RunInput("test")

            assert ri.machines == data

    def test_property_objectives(self):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            data = objectives_test_data()
            MockRedisInput.ALL.hidden_set("objectives", data["objectives"])
            MockRedisInput.ALL.hidden_set("target_cycle_time", data["target_cycle_time"])
            MockRedisInput.ALL.hidden_set("hourly_operator_cost", data["hourly_operator_cost"])

            ri = RunInput("test")
            assert ri.objectives == data

    def test_json_file_returns_all(self):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            complete_data = complete_test_data()

            for label, value in complete_data.items():
                MockRedisInput.ALL.hidden_set(label, value)

            ri = RunInput("test")
            assert ri.json() == complete_data
            

class TestRunInputSetters:
    def test_setter_area(self, monkeypatch: pytest.MonkeyPatch):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            monkeypatch.setattr(RedisRunConfig, "query", lambda _ , run_id : RunStatus.INPUT.value)
            data = area_test_data()
            ri = RunInput("test")
            ri.areas = data
            assert ri.areas == data

    def test_setter_steps(self, monkeypatch: pytest.MonkeyPatch):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            monkeypatch.setattr(RedisRunConfig, "query", lambda _ , run_id : RunStatus.INPUT.value)
            data = steps_test_data()
            ri = RunInput("test")
            ri.steps = data
            assert ri.steps == data

    def test_setter_machines(self, monkeypatch: pytest.MonkeyPatch):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            monkeypatch.setattr(RedisRunConfig, "query", lambda _ , run_id : RunStatus.INPUT.value)
            data = machines_test_data()
            ri = RunInput("test")
            ri.machines = data
            assert ri.machines == data

    def test_setter_objectives(self, monkeypatch: pytest.MonkeyPatch):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            monkeypatch.setattr(RedisRunConfig, "query", lambda _ , run_id : RunStatus.INPUT.value)
            data = objectives_test_data()
            ri = RunInput("test")
            ri.objectives = data
            assert ri.objectives == data

    def test_setting_steps_sets_technology(self, monkeypatch: pytest.MonkeyPatch):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            monkeypatch.setattr(RedisRunConfig, "query", lambda _ , run_id : RunStatus.INPUT.value)

            ri = RunInput("test")
            ri.steps = []
            ri.machines = []

            steps_data = steps_test_data()
            ri.steps = steps_data
            
            step_technology = set()
            for step in steps_data:
                step_technology.add(step["technology"])
            assert MockRedisInput.TECHNOLOGIES.query("test") == list(step_technology)

    def test_setting_machines_sets_technology(self, monkeypatch: pytest.MonkeyPatch):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            monkeypatch.setattr(RedisRunConfig, "query", lambda _ , run_id : RunStatus.INPUT.value)

            ri = RunInput("test")
            ri.steps = []
            ri.machines = []

            machine_data = machines_test_data()
            ri.machines = machine_data

            machine_technology = set()
            for machine in machine_data:
                for tech in machine["technologies"]:
                    machine_technology.add(tech)
            assert MockRedisInput.TECHNOLOGIES.query("test") == list(machine_technology)

    def test_setting_steps_and_machines_sets_technology(self, monkeypatch: pytest.MonkeyPatch):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            monkeypatch.setattr(RedisRunConfig, "query", lambda _ , run_id : RunStatus.INPUT.value)

            ri = RunInput("test")

            steps_data = steps_test_data()
            ri.steps = steps_data
            machine_data = machines_test_data()
            ri.machines = machine_data

            technologies = set()
            for step in steps_data:
                technologies.add(step["technology"])
            for machine in machine_data:
                for tech in machine["technologies"]:
                    technologies.add(tech)

            assert MockRedisInput.TECHNOLOGIES.query("test") == list(technologies)

    def test_setting_everything_returns_correct_json(self, monkeypatch: pytest.MonkeyPatch):
        with patch('server.RedisManager.RunInput.RedisInput', MockRedisInput):
            monkeypatch.setattr(RedisRunConfig, "query", lambda _ , run_id : RunStatus.INPUT.value)

            steps_data = steps_test_data()                    
            machine_data = machines_test_data()
            area_data = area_test_data()
            objectives_data = objectives_test_data()

            complete_data = complete_test_data()

            ri = RunInput("test")
            ri.areas = area_data
            ri.steps = steps_data
            ri.machines = machine_data
            ri.objectives = objectives_data
            json_file = ri.json()
            assert json_file == complete_data

class TestRunInputComparison:
    def test_false_with_other_run_id(self):
        ri_1 = RunInput("test")
        ri_2 = RunInput("test1")

        assert ri_1 != ri_2

    def test_true_with_same_run_id(self):
        ri_1 = RunInput("test")
        ri_2 = RunInput("test")

        assert ri_1 == ri_2
