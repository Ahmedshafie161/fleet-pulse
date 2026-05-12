from typing import ClassVar, Optional, Type, TypeVar

from sqlalchemy.orm import DeclarativeBase, Session

T = TypeVar("T", bound="BaseModel")


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    _session: ClassVar[Optional[Session]] = None

    @classmethod
    def set_session(cls, session: Session) -> None:
        BaseModel._session = session

    @classmethod
    def session(cls) -> Session:
        if cls._session is None:
            raise RuntimeError("Database session has not been configured")
        return cls._session

    @classmethod
    def create(cls: Type[T], save: bool = False, **kwargs) -> T:
        obj = cls(**kwargs)

        if save:
            session = cls.session()
            session.add(obj)
            session.commit()
            session.refresh(obj)

        return obj