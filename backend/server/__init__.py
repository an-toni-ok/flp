from celery import Celery, Task
from flask import Flask, jsonify, request, session

from server.extensions import init_redis

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
        SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
    #     CELERY=dict(
    #         broker_url="redis://redis",
    #         result_backend="redis://redis",
    #         task_ignore_result=True,
    #     ),
    )

    from server.config import Config
    app.config.from_object(Config)

    app.config.from_prefixed_env()
    celery_init_app(app)
    init_redis(app)

    @app.errorhandler(400)
    def invalid_request_data(e):
        return jsonify(error=str(e)), 400
    
    @app.before_request
    def assign_session_token():
        from server.redis_util import ensure_data_settable
        from server.extensions import redis_client

        if "id" in session:
            try:
                # The tokens are in an integer format, if the conversion
                # to int throws an error the token isn't valid
                session_id = str(int(session['id']))
                
                if not bool(redis_client.sismember("session_ids", session_id)):
                    # Token not yet saved, but valid
                    redis_client.sadd("session_ids", session_id)
                ensure_data_settable(session_id)
                return
            except:
                # Invalid token
                pass

        # Generate a new token
        counter = 0
        while True:
            session_id = str(hash(request.origin + str(counter)))
            if not bool(redis_client.sismember("session_ids", session_id)):
                # Store the session_id in redis before the session, so
                # that the same id cannot be used twice because of
                # network errors when writing it to redis. 
                redis_client.sadd("session_ids", session_id)
                ensure_data_settable(session_id)
                session["id"] = session_id
                break
            counter += 1

    from server.routes import routes

    app.register_blueprint(routes)

    return app