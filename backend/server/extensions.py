import logging
import sys
from celery import Celery, Task
from flask import Flask
from redis import Redis

redis_client = None

def init_redis(app):
    global redis_client
    redis_client = Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'],
        password=app.config['REDIS_PASSWORD'],
        decode_responses=True
    )

def celery_init_app(app: Flask) -> Celery:
    """Initializes Celery based of the flask app instance.

    This creates and returns a Celery app object. Celery 
    configuration is taken from the CELERY key in the Flask 
    configuration. The Celery app is set as the default, so 
    that it is seen during each request. The Task subclass 
    automatically runs task functions with a Flask app 
    context active, so that services like your database 
    connections are available.

    Args:
        app (Flask): Flask app instance

    Returns:
        Celery: Initialized Celery Instance
    """
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    setup_logger(app)
    return celery_app

def setup_logger(app: Flask):
    logger = logging.getLogger()
    logger.setLevel(app.config['LOG_LEVEL'])

    if app.config['LOG_TO_STDOUT']:
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = logging.FileHandler(app.config['LOG_FILE'])

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)