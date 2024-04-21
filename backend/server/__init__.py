from celery import Celery, Task
from flask import Flask

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
    return celery_app

def create_app() -> Flask:
    """Flask Application factory pattern.

    Returns:
        Flask: The created Flask app instance
    """
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)

    from server.routes import routes

    app.register_blueprint(routes)

    return app