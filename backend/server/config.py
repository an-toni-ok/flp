import os
import logging

class Config:    
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    CELERY=dict(
        broker_url="redis://redis",
        result_backend="redis://redis",
        task_ignore_result=True,
    )
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or True
    LOG_FILE = os.environ.get('LOG_FILE') or 'app.log'
    LOG_LEVEL = logging.DEBUG
