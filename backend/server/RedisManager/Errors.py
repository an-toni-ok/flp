class RunAlreadyExists(Exception):
    def __init__(self, message="Run already exists"):
        super().__init__(message)

class RunNotCreated(Exception):
    def __init__(self, message="Run is not created"):
        super().__init__(message)

class InvalidChangeMethod(Exception):
    def __init__(self, message="Input data cannot be changed with the RedisRunConfig. Use the RedisInput class instead."):
        super().__init__(message)

class SessionIdNotSet(Exception):
    def __init__(self, message="Session not set."):
        super().__init__(message)
