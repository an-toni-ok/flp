from celery import shared_task

@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    return a + b

@shared_task(ignore_result=False)
def start_optimization(run_id):
    import json
    from server.RedisManager import RunInput, RunManager
    from server.optimization import run_optimization

    ri = RunInput(run_id)
    rm = RunManager(
        user_session_id=None, 
        run_nr=None,
        run_id=run_id
    )

    input_file = f"{run_id}.json"

    with open(input_file, "w") as file:
        file.write(json.dumps(ri.json()))

    run_optimization(input_file)
    
    rm.finish({}, False)

    return True