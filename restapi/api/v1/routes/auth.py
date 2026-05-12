from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from restapi.core.auth import create_access_token, verify_password
from restapi.core.config import settings 
from restapi.db.models import User
from restapi.schemas.auth import TokenSchema
from restapi.schemas.common import COMMON_200_401_RESPONSES

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=TokenSchema,
    responses=COMMON_200_401_RESPONSES,
)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        session = User.session()
        user = session.query(User).filter_by(username=form_data.username).first()
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        expires = timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(data={"sub": user.username}, expires_delta=expires)
        return TokenSchema(access_token=token)
    finally:
        session.close()