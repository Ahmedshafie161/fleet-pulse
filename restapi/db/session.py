from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

from restapi.core.config import settings


def _make_engine():
    db_file: str = settings.DATABASE_FILE
    url = "sqlite:///:memory:" if db_file == ":memory:" else f"sqlite:///{db_file}"
    connect_args = {
        "check_same_thread": False,
        "timeout": 10.0,
    }
    engine = create_engine(url, connect_args=connect_args)
    
    if db_file != ":memory:":
        with engine.begin() as conn:
            conn.execute(text("PRAGMA journal_mode=WAL"))
            conn.execute(text("PRAGMA synchronous=NORMAL"))
    
    return engine


engine = _make_engine()
SessionLocal: scoped_session = scoped_session(sessionmaker(bind=engine))
