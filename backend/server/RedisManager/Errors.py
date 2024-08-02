class RunAlreadyExists(Exception):
    def __init__(self, run_id=""):
        super().__init__(f"Run (run_id: { run_id }) already exists")

class RunNotCreated(Exception):
    def __init__(self, run_id=""):
        super().__init__(f"Run (run_id: { run_id }) is not created")

class RunNotStartable(Exception):
    def __init__(self, run_id="", text=""):
        super().__init__(f"Run (run_id: { run_id }) { text }")

class RunNotRunning(Exception):
    def __init__(self, run_id=""):
        super().__init__(f"Run (run_id: { run_id }) is not running")

class InvalidChangeMethod(Exception):
    def __init__(self, message="Input data cannot be changed with the RedisRunConfig. Use the RedisInput class instead."):
        super().__init__(message)

class SessionIdNotSet(Exception):
    def __init__(self, session_id=""):
        super().__init__(f"Session (session_id: { session_id }) not set.")

class InputNotSettable(Exception):
    def __init__(self, status=""):
        super().__init__(f"Run status (status: { status }) doesn't allow changing the input.")