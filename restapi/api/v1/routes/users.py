from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone
import logging

from restapi.core.auth import get_current_user, get_password_hash, verify_password
from restapi.db.models import User
from restapi.schemas.common import COMMON_200_401_RESPONSES, COMMON_204_401_RESPONSES
from restapi.schemas.users import UserPasswordPostSchema, UserResponseSchema, UserCreateSchema

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses=COMMON_200_401_RESPONSES,
)
def create_user(body: UserCreateSchema):
    """Create a new user. No authentication required."""
    try:
        session = User.session()
        
        existing = session.query(User).filter_by(username=body.username).first()
        if existing:
            logger.warning(f"Registration failed: username '{body.username}' already exists")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username already exists",
            )
        
        now = datetime.now(timezone.utc)
        user = User.create(
            save=True,
            username=body.username,
            password=get_password_hash(body.password),
            is_active=True,
            created_at=now,
        )
        logger.info(f"User '{body.username}' created successfully with ID {user.id}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user '{body.username}': {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.get(
    "",
    response_model=list[UserResponseSchema],
        responses=COMMON_200_401_RESPONSES,
)
def list_users(current_user: User = Depends(get_current_user)):
    session = User._session
    return session.query(User).all() if session else []

@router.post(
    "/password",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=COMMON_204_401_RESPONSES,
)
def change_password(
    body: UserPasswordPostSchema,
    current_user: User = Depends(get_current_user),
):
    if not verify_password(body.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Old password is incorrect",
        )
    current_user.password = get_password_hash(body.new_password)
    session = User._session
    if session:
        session.commit()
