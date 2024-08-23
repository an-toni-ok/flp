from celery import shared_task

@shared_task(ignore_result=False)
def start_optimization(run_id):
    import json
    from server.RedisManager import RunManager
    from server.optimization import run_optimization

    rm = RunManager(
        user_session_id=None, 
        run_nr=None,
        run_id=run_id
    )

    input_file = f"{run_id}.json"

    with open(input_file, "w") as file:
        file.write(json.dumps(rm.input.json()))

    output = run_optimization(input_file)
    
    rm.finish(output, False)

    return True