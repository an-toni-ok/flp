from celery import shared_task

@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    return a + b

@shared_task(ignore_result=False)
def start_optimization(run_id) -> int:
    return True