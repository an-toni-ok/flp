from enum import Enum

class RunStatus(str, Enum):
    INPUT = "INPUT"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

class RunInputType(Enum):
    AREA = "areas"
    STEPS = "steps"
    MACHINES = "machines"
    OBJECTIVES = "objectives"