from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


FuelType = Literal["diesel", "petrol", "electric", "hybrid", "hydrogen", "lpg"]


class VehicleCreateSchema(BaseModel):
    vin: str = Field(..., min_length=17, max_length=17, description="17-character VIN")
    plate: str = Field(..., min_length=1, max_length=20)
    make: str
    model: str
    year: int = Field(..., ge=1980, le=2100)
    fuel_type: FuelType = "diesel"
    odometer_km: float = Field(0.0, ge=0)


class VehiclePatchSchema(BaseModel):
    plate: Optional[str] = None
    odometer_km: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None
    firmware_version: Optional[str] = None


class VehicleResponseSchema(BaseModel):
    id: int
    vin: str
    plate: str
    make: str
    model: str
    year: int
    fuel_type: str
    odometer_km: float
    is_active: bool
    firmware_version: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
