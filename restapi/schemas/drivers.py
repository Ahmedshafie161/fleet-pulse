from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DriverCreateSchema(BaseModel):
    first_name: str
    last_name: str
    license_number: str
    license_expiry: datetime
    phone: Optional[str] = None
    email: Optional[str] = None


class DriverPatchSchema(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    license_expiry: Optional[datetime] = None
    is_active: Optional[bool] = None
    assigned_vehicle_id: Optional[int] = None


class DriverResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    license_number: str
    license_expiry: datetime
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool
    assigned_vehicle_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
