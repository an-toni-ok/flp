from flask import Flask, jsonify, request, session

from server.extensions import init_redis, celery_init_app, setup_logger
from server.RedisManager.SessionManager import SessionManager


def create_app() -> Flask:
    """Flask Application factory pattern.

    Returns:
        Flask: The created Flask app instance
    """
    app = Flask(__name__)
    
    # Configuration of extensions and flask
    app.config.from_mapping(
        SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
    )

    from server.config import Config
    app.config.from_object(Config)
    app.config.from_prefixed_env()
    celery_init_app(app)
    init_redis(app)
    setup_logger(app)

    # Configure error handling
    @app.errorhandler(400)
    def invalid_request_data(e):
        return jsonify(error=str(e)), 400
    
    # Configure initial session token assignment 
    # and reassignment on requests
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