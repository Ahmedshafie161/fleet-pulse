import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, UTC

import pytest
from dynaconf import Dynaconf  # type: ignore[import-untyped]
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

# -------------------------------------------------------------------
# Settings BEFORE importing app - monkeypatch config module
# -------------------------------------------------------------------

from restapi.core import config

config.settings = Dynaconf(
    settings_file=[],
    environments=False,
)

config.settings.PROJECT_NAME = "FleetPulse Test"
config.settings.SECRET_KEY = "test-secret-key"
config.settings.ACCESS_TOKEN_EXPIRE_MINUTES = 5
config.settings.DATABASE_FILE = ":memory:"

# -------------------------------------------------------------------
# Create ONE shared in-memory DB
# -------------------------------------------------------------------

_test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=_test_engine,
    )
)

# -------------------------------------------------------------------
# Import models AFTER engine exists
# -------------------------------------------------------------------

from restapi.db.models.base import Base, BaseModel
from restapi.db.models import User

Base.metadata.create_all(bind=_test_engine)

BaseModel.set_session(TestingSessionLocal)  # type: ignore[arg-type]

# -------------------------------------------------------------------
# IMPORTANT: monkeypatch app DB session
# -------------------------------------------------------------------

import restapi.db.session as db_session_module

db_session_module.engine = _test_engine
db_session_module.SessionLocal = TestingSessionLocal

# -------------------------------------------------------------------
# Import app LAST
# -------------------------------------------------------------------

from restapi.server import app
from restapi.core.auth import get_password_hash

# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clean_db():
    yield

    TestingSessionLocal.rollback()

    for table in reversed(Base.metadata.sorted_tables):
        TestingSessionLocal.execute(table.delete())

    TestingSessionLocal.commit()


@pytest.fixture
def admin_user():
    return User.create(
        save=True,
        username="admin",
        password=get_password_hash("admin1234"),
        created_at=datetime.now(UTC),
    )


@pytest.fixture
def client(admin_user):
    with TestClient(app) as c:
        resp = c.post(
            "/api/v1/auth/login",
            data={
                "username": "admin",
                "password": "admin1234",
            },
        )

        token = resp.json()["access_token"]

        c.headers.update(
            {"Authorization": f"Bearer {token}"}
        )

        yield c