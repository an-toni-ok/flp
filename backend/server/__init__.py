from flask import Flask, jsonify, request, session

from server.extensions import init_redis, celery_init_app, setup_logger
from server.RedisManager import SessionManager


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
        if "id" in session:
            sm = SessionManager(session_id=session["id"])
            app.logger.debug(f"Attempting to log in session id \"{session['id']}\".")
        else:
            sm: SessionManager = SessionManager.create()
            app.logger.debug(f"Created session with id \"{ sm.session_id }\".")
            session["id"] = sm.session_id

    # register the blueprint routes
    from server.routes import routes

    app.register_blueprint(routes)

    return app