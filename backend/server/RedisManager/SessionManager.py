from redis import Redis

from typing import List
from logging import Logger

from .RunManager import RunManager

class SessionManager:
    def __init__(self, session_id, redis: Redis, logger: Logger):
        self.logger = logger

        if not redis.sismember("session_ids", session_id):
            redis.sadd("session_ids", session_id)
            self.logger.debug(f"Unregistered Session id \"{session_id}\" was added.")
        self.session_id = session_id

        data = redis.json().get(session_id)
        self.current_run_nr: int = data["current_run_nr"]
        self.run_ids: List = data["run_ids"]

    @classmethod
    def init_new_session(cls, redis: Redis, logger: Logger):
        # Initialize the counter (this will only be done if the
        # field does not exist so far)
        redis.setnx("session_id_counter", 0)

        session_id = None
        unique_session_id = False
        while not unique_session_id:
            # Atomic action, therefore threadsafe
            counter_value = redis.incr("session_id_counter")
            logger.debug(f"Trying to create session id from \"basehash{counter_value}\"")
            session_id = hash(f"basehash{counter_value}")

            # Check for hash collision
            if not redis.sismember("session_ids", session_id):
                redis.sadd("session_ids", session_id)
                logger.debug(f"Session id \"{session_id}\" set.")
                unique_session_id = True        

        redis.json().set(session_id, "$", {
            "current_run_nr": 0,
            "run_ids": []
        })
        
        # Create the first run
        logger.debug(f"Creating first run for session \"{session_id}\"")
        RunManager.init_new_run(
            session_id, 
            redis=redis, 
            logger=logger
        )
        return cls(session_id, redis, logger)
    
    def load_run(self, redis: Redis, logger: Logger, run_nr=None) -> RunManager:
        if run_nr is None:
            run_nr = self.current_run_nr

        return RunManager(self.session_id, run_nr, redis, logger)