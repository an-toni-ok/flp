from .RunManager import RunManager
from .RedisConnector import RedisSession, RedisIdCounter

class SessionManager:
    """Management class for Sessions.
    """
    def __init__(self, session_id):
        """Loads a session. 
        
        If the provided session id is not stored in redis it will be added instead.

        Args:
            session_id (_type_): Die id der Session
        """
        if not RedisSession.contains(session_id):
            RedisSession.create_session(session_id)
            RunManager.create(session_id)

        self.session_id = session_id

    @classmethod
    def create(cls):
        """Creates a session.

        Returns:
            SessionManager: The Session Manager for the created Session.
        """
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
        
        RunManager.create(session_id)
        return cls(session_id)

    @property
    def current_run_nr(self):
        """Returns the current run nr stored in redis.

        Returns:
            _type_: the current run nr.
        """
        return RedisSession.current_run_nr(self.session_id)

    @property
    def run_ids(self):
        """Returns the run ids stored in redis.

        Returns:
            Array: All run ids of the session.
        """
        return RedisSession.run_ids(self.session_id)