from datetime import datetime

from pydantic import BaseModel, field_validator, ConfigDict


class UserResponseSchema(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not v:
            raise ValueError("Username cannot be empty")
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 50:
            raise ValueError("Username must be at most 50 characters")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not v:
            raise ValueError("Password cannot be empty")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserPasswordPostSchema(BaseModel):
    old_password: str
    new_password: str

    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        if not v:
            raise ValueError("Password cannot be empty")
        if len(v) < 8:
            raise ValueError("New password must be at least 8 characters")
        return v
