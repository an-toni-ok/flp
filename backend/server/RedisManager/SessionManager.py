from .RedisConnector import RedisSession, RedisIdCounter

class SessionManager:
    def __init__(self, session_id):
        if not RedisSession.contains(session_id):
            RedisSession.create_session(session_id)

        self.session_id = session_id

    @classmethod
    def create(cls):
        session_id = None
        unique_session_id = False
        while not unique_session_id:
            # Atomic action, therefore threadsafe
            counter_value = RedisIdCounter.incr()
            session_id = hash(f"basehash{counter_value}")

            # Check for hash collision
            if not RedisSession.contains(session_id):
                RedisSession.create_session(session_id)
                unique_session_id = True
        
        return cls(session_id)

    @property
    def current_run_nr(self):
        return RedisSession.current_run_nr(self.session_id)

    @property
    def run_ids(self):
        return RedisSession.run_ids(self.session_id)