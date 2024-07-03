import pytest
from redis import Redis
from server import create_app
from server.RedisManagerOld.SessionManager import SessionManager

@pytest.fixture(scope="class", autouse=True)
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture(scope="class", autouse=True)
def redis(app) -> Redis:
    from server.extensions import redis

    return redis

@pytest.fixture(scope="class")
def session_manager(app) -> SessionManager:
    from server.extensions import redis

    return SessionManager.init_new_session(
        redis, app.logger
    )

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()