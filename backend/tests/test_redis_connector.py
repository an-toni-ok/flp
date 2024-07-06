import pytest

from redis import Redis

from server.RedisManagerOld.util import RunStatus
from server.RedisManager.RedisConnector import RedisInput, RedisRunConfig, RedisSession, RedisIdCounter
from server.RedisManager.Errors import InvalidChangeMethod, RunAlreadyExists, RunNotCreated, SessionIdNotSet

class TestRedisIdCounter:
    def unset_session_id_counter(self, redis: Redis):
        redis.delete("session_id_counter")

    def test_counter_auto_init(self, redis: Redis):
        self.unset_session_id_counter(redis)

        RedisIdCounter.incr()
        assert int(redis.get("session_id_counter")) == 1

    def test_counter_incr_works(self, redis):
        self.unset_session_id_counter(redis)
        
        value1 = RedisIdCounter.incr() # Init counter
        value2 = RedisIdCounter.incr()
        assert value2 == value1 + 1

class TestRedisSession:
    def unset_session_ids(self, redis: Redis):
        redis.delete("session_ids")

    def test_session_id_check_against_empty_session_ids(self, redis: Redis):
        self.unset_session_ids(redis)

        assert bool(RedisSession.contains("test")) == False

    def test_session_creation(self, redis: Redis):
        self.unset_session_ids(redis)

        session_id = "test"
        RedisSession.create_session(session_id)
        assert session_id in list(redis.smembers("session_ids"))
        assert redis.json().get(session_id) is not None

    def test_session_id_check_after_creation(self, redis: Redis):
        self.unset_session_ids(redis)

        session_id = "test"
        assert RedisSession.contains(session_id) == False
        RedisSession.create_session(session_id)
        assert RedisSession.contains(session_id) == True

    def test_session_run_counter_incr(self, redis: Redis):
        self.unset_session_ids(redis)

        session_id = "test"
        RedisSession.create_session(session_id)
        run_nr = redis.json().get(session_id, "$.current_run_nr")[0]

        RedisSession.create_run(session_id)
        new_run_nr = redis.json().get(session_id, "$.current_run_nr")[0]
        assert new_run_nr == run_nr + 1

    def test_session_run_creation(self, redis: Redis):
        self.unset_session_ids(redis)

        session_id = "test"
        RedisSession.create_session(session_id)
        run_id = RedisSession.create_run(session_id)
        stored_run_ids = redis.json().get(session_id, "$.run_ids")[0]
        assert run_id in stored_run_ids

    def test_creating_run_without_session_existing_raises_error(self, redis: Redis):
        session_id = "test_session_id"
        redis.delete(session_id) # Make sure it doesn't exist
        with pytest.raises(SessionIdNotSet) as err:
            RedisSession.create_run(session_id)

class TestRedisRunConfig:
    def reset_test_run(self, redis: Redis, run_id="test_run", delete_only=False):
        redis.delete(run_id)
        if delete_only:
            return
        RedisRunConfig.create(run_id)

    def get_set_comparison_data(self, field: RedisRunConfig, field_value, redis: Redis):
        run_id = "test_run"
        self.reset_test_run(redis, run_id=run_id)

        field.set(run_id, field_value)
        redis_run_data = redis.json().get(run_id)
        real_data = None
        match field:
            case RedisRunConfig.ALL:
                real_data = redis_run_data
            case RedisRunConfig.OUTPUT:
                real_data = redis_run_data["output"]
            case RedisRunConfig.EXECUTION_ID:
                real_data = redis_run_data["execution_id"]
            case RedisRunConfig.STATUS:
                real_data = redis_run_data["status"]
        return { "expected": field_value, "real": real_data }

    def set_and_get_query_comparison_data(self, field: RedisRunConfig, field_value, redis: Redis):
        run_id = "test_run"
        self.reset_test_run(redis, run_id=run_id)

        field.set(run_id, field_value)
        real_data = field.query(run_id)
        return { "expected": field_value, "real": real_data }

    def test_created_run_has_correct_skeleton(self, redis: Redis):
        run_id = "test_run"
        self.reset_test_run(redis, run_id=run_id, delete_only=True)
        init_data = {
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
        }

        RedisRunConfig.create(run_id)
        test_run = redis.json().get(run_id)
        assert test_run == init_data

    def test_creation_of_existing_run_raises_error(self, redis: Redis):
        run_id = "test_run"
        self.reset_test_run(redis, run_id=run_id, delete_only=True)

        RedisRunConfig.create(run_id)

        with pytest.raises(RunAlreadyExists):
            RedisRunConfig.create(run_id)

    def test_setting_option_of_non_existant_run_raises_error(self, redis: Redis):
        run_id = "test_run"
        self.reset_test_run(redis, run_id=run_id, delete_only=True)
        test_data = {
            'output': {
                "test": "test"
            }, 
            'execution_id': 1, 
            'status': RunStatus.COMPLETED.value
        }

        with pytest.raises(RunNotCreated) as err:
            RedisRunConfig.ALL.set(run_id, test_data)

    def test_setting_all_option_with_new_input_raises_error(self, redis: Redis):
        run_id = "test_run"
        self.reset_test_run(redis, run_id=run_id, delete_only=True)
        test_data = {
            'output': {
                "test": "test"
            }, 
            'execution_id': 1, 
            'status': RunStatus.COMPLETED.value,
            'input': {"areas": "test"}
        }

        RedisRunConfig.create(run_id)
        with pytest.raises(InvalidChangeMethod) as err:
            RedisRunConfig.ALL.set(run_id, test_data)

        redis_test_data = redis.json().get(run_id)
        assert redis_test_data["input"] != test_data["input"]

    def test_setting_all_option(self, redis: Redis):
        test_data = {
            'output': {
                "test": "test"
            }, 
            'execution_id': 1, 
            'status': RunStatus.COMPLETED.value
        }
        comparison_data = self.get_set_comparison_data(
            RedisRunConfig.ALL, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_output_option(self, redis: Redis):
        test_output = {
            "test": "test"
        }
        comparison_data = self.get_set_comparison_data(
            RedisRunConfig.STATUS, 
            test_output,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_execution_id_option(self, redis: Redis):
        comparison_data = self.get_set_comparison_data(
            RedisRunConfig.EXECUTION_ID, 
            1,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_status_option(self, redis: Redis):
        comparison_data = self.get_set_comparison_data(
            RedisRunConfig.STATUS, 
            RunStatus.COMPLETED.value,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_all_option(self, redis: Redis):
        test_data = {
            'output': {
                "test": "test"
            }, 
            'execution_id': 1, 
            'status': RunStatus.COMPLETED.value
        }
        comparison_data = self.set_and_get_query_comparison_data(
            RedisRunConfig.ALL, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_output_option(self, redis: Redis):
        test_output = {
            "test": "test"
        }
        comparison_data = self.set_and_get_query_comparison_data(
            RedisRunConfig.STATUS, 
            test_output,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_execution_id_option(self, redis: Redis):
        comparison_data = self.set_and_get_query_comparison_data(
            RedisRunConfig.EXECUTION_ID, 
            1,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_status_option(self, redis: Redis):
        comparison_data = self.set_and_get_query_comparison_data(
            RedisRunConfig.STATUS, 
            RunStatus.COMPLETED.value,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

class TestRedisInput:
    def reset_test_run_input(self, redis: Redis, run_id="test_run"):
        if redis.json().get(run_id) is None:
            RedisRunConfig.create(run_id)
        
        redis.json().set(run_id, "$.input", {
            'areas': {}, 
            'restricted_areas': {}, 
            'technologies': [], 
            'production_steps': {}, 
            'machines': {}, 
            'objectives': {}, 
            'target_cycle_time': None, 
            'hourly_operator_cost': None
        })

    def get_set_comparison_data(self, field: RedisInput, field_value, redis: Redis):
        run_id = "test_run"
        self.reset_test_run_input(redis, run_id=run_id)

        field.set(run_id, field_value)
        redis_run_data = redis.json().get(run_id)["input"]
        real_data = None
        match field:
            case RedisInput.ALL:
                real_data = redis_run_data
            case RedisInput.AREAS:
                real_data = redis_run_data["areas"]
            case RedisInput.R_AREAS:
                real_data = redis_run_data["restricted_areas"]
            case RedisInput.TECHNOLOGIES:
                real_data = redis_run_data["technologies"]
            case RedisInput.STEPS:
                real_data = redis_run_data["production_steps"]
            case RedisInput.MACHINES:
                real_data = redis_run_data["machines"]
            case RedisInput.OBJECTIVES:
                real_data = redis_run_data["objectives"]
            case RedisInput.CYCLE_TIME:
                real_data = redis_run_data["target_cycle_time"]
            case RedisInput.OPERATOR_COST:
                real_data = redis_run_data["hourly_operator_cost"]
        return { "expected": field_value, "real": real_data }

    def set_and_get_query_comparison_data(self, field: RedisInput, field_value, redis: Redis):
        run_id = "test_run"
        self.reset_test_run_input(redis, run_id=run_id)

        field.set(run_id, field_value)
        real_data = field.query(run_id)
        return { "expected": field_value, "real": real_data }

    def test_setting_all_option(self, redis: Redis):
        test_data = {
            'areas': { "test": "test" }, 
            'restricted_areas': { "test": "test" }, 
            'technologies': [ "test", "test", "test" ], 
            'production_steps': { "test": "test" }, 
            'machines': { "test": "test" }, 
            'objectives': { "test": "test" }, 
            'target_cycle_time': 1, 
            'hourly_operator_cost': 1
        }
        comparison_data = self.get_set_comparison_data(
            RedisInput.ALL, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_areas_option(self, redis: Redis):
        test_data = { "test": "test" }
        comparison_data = self.get_set_comparison_data(
            RedisInput.AREAS, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_r_areas_option(self, redis: Redis):
        test_data = { "test": "test" }
        comparison_data = self.get_set_comparison_data(
            RedisInput.R_AREAS, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_technologies_option(self, redis: Redis):
        test_data = [ "test", "test", "test" ]
        comparison_data = self.get_set_comparison_data(
            RedisInput.TECHNOLOGIES, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_steps_option(self, redis: Redis):
        test_data = { "test": "test" }
        comparison_data = self.get_set_comparison_data(
            RedisInput.STEPS, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_machines_option(self, redis: Redis):
        test_data = { "test": "test" }
        comparison_data = self.get_set_comparison_data(
            RedisInput.MACHINES, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_objectives_option(self, redis: Redis):
        test_data = { "test": "test" }
        comparison_data = self.get_set_comparison_data(
            RedisInput.OBJECTIVES, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_cycle_time_option(self, redis: Redis):
        test_data = 1
        comparison_data = self.get_set_comparison_data(
            RedisInput.CYCLE_TIME, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_setting_operator_cost_option(self, redis: Redis):
        test_data = 1
        comparison_data = self.get_set_comparison_data(
            RedisInput.OPERATOR_COST, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_all_option(self, redis: Redis):
        test_data = {
            'areas': { "test": "test" }, 
            'restricted_areas': { "test": "test" }, 
            'technologies': [ "test", "test", "test" ], 
            'production_steps': { "test": "test" }, 
            'machines': { "test": "test" }, 
            'objectives': { "test": "test" }, 
            'target_cycle_time': 1, 
            'hourly_operator_cost': 1
        }
        comparison_data = self.set_and_get_query_comparison_data(
            RedisInput.ALL, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_areas_option(self, redis: Redis):
        test_data = { "test": "test" }
        comparison_data = self.set_and_get_query_comparison_data(
            RedisInput.AREAS, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_r_areas_option(self, redis: Redis):
        test_data = { "test": "test" }
        comparison_data = self.set_and_get_query_comparison_data(
            RedisInput.R_AREAS, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_technologies_option(self, redis: Redis):
        test_data = [ "test", "test", "test" ]
        comparison_data = self.set_and_get_query_comparison_data(
            RedisInput.TECHNOLOGIES, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_steps_option(self, redis: Redis):
        test_data = { "test": "test" }
        comparison_data = self.set_and_get_query_comparison_data(
            RedisInput.STEPS, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_machines_option(self, redis: Redis):
        test_data = { "test": "test" }
        comparison_data = self.set_and_get_query_comparison_data(
            RedisInput.MACHINES, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_objectives_option(self, redis: Redis):
        test_data = { "test": "test" }
        comparison_data = self.set_and_get_query_comparison_data(
            RedisInput.OBJECTIVES, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_cycle_time_option(self, redis: Redis):
        test_data = 1
        comparison_data = self.set_and_get_query_comparison_data(
            RedisInput.CYCLE_TIME, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]

    def test_query_operator_cost_option(self, redis: Redis):
        test_data = 1
        comparison_data = self.set_and_get_query_comparison_data(
            RedisInput.OPERATOR_COST, 
            test_data,
            redis
        )
        assert comparison_data["expected"] == comparison_data["real"]