from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FleetConfigSchema(BaseModel):
 
    reference_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique machine-readable identifier, e.g. 'cfg_default'.",
    )
    display_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Human-readable label, e.g. 'Default Configuration'.",
    )
    idle_alert_threshold_minutes: int = Field(
        default=15,
        ge=1,
        description="Minutes of engine idle before an idle alert is raised.",
    )
    low_fuel_threshold_pct: float = Field(
        default=15.0,
        ge=0.0,
        le=100.0,
        description="Fuel level percentage below which a low-fuel alert fires.",
    )
    speed_limit_kmh: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Fleet-wide speed limit in km/h. None means no global limit.",
    )


class FleetConfigResponseSchema(BaseModel):
   
    id: int
    reference_name: str
    display_name: str
    is_active: bool
    idle_alert_threshold_minutes: int
    low_fuel_threshold_pct: float
    speed_limit_kmh: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
