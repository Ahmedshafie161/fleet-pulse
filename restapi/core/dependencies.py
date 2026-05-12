from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from restapi.db.session import SessionLocal
from restapi.core.auth import get_current_user


def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_active_user(current_user=Depends(get_current_user)):
    if not getattr(current_user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )
    return current_user



class PaginationParams:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit
