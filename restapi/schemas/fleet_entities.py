from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

# ── Trips ─────────────────────────────────────────────────────────────────────

TripStatus = Literal["in_progress", "completed", "cancelled"]


class TripCreateSchema(BaseModel):
    vehicle_id: int
    driver_id: Optional[int] = None
    start_lat: Optional[float] = Field(None, ge=-90, le=90)
    start_lng: Optional[float] = Field(None, ge=-180, le=180)


class TripPatchSchema(BaseModel):
    ended_at: Optional[datetime] = None
    end_lat: Optional[float] = Field(None, ge=-90, le=90)
    end_lng: Optional[float] = Field(None, ge=-180, le=180)
    distance_km: Optional[float] = Field(None, ge=0)
    max_speed_kmh: Optional[float] = Field(None, ge=0)
    avg_speed_kmh: Optional[float] = Field(None, ge=0)
    fuel_consumed_l: Optional[float] = Field(None, ge=0)
    status: Optional[TripStatus] = None


class TripResponseSchema(BaseModel):
    id: int
    vehicle_id: int
    driver_id: Optional[int] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    start_lat: Optional[float] = None
    start_lng: Optional[float] = None
    end_lat: Optional[float] = None
    end_lng: Optional[float] = None
    distance_km: Optional[float] = None
    max_speed_kmh: Optional[float] = None
    avg_speed_kmh: Optional[float] = None
    fuel_consumed_l: Optional[float] = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Telemetry ─────────────────────────────────────────────────────────────────

class TelemetryCreateSchema(BaseModel):
    vehicle_id: int
    trip_id: Optional[int] = None
    recorded_at: Optional[datetime] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    speed_kmh: Optional[float] = Field(None, ge=0)
    heading_deg: Optional[float] = Field(None, ge=0, lt=360)
    altitude_m: Optional[float] = None
    odometer_km: Optional[float] = Field(None, ge=0)
    fuel_level_pct: Optional[float] = Field(None, ge=0, le=100)
    engine_rpm: Optional[int] = Field(None, ge=0)
    ignition: Optional[Literal["on", "off"]] = None
    source: Literal["mqtt", "api", "sim"] = "api"


class TelemetryResponseSchema(BaseModel):
    id: int
    vehicle_id: int
    trip_id: Optional[int] = None
    recorded_at: datetime
    latitude: float
    longitude: float
    speed_kmh: Optional[float] = None
    heading_deg: Optional[float] = None
    altitude_m: Optional[float] = None
    odometer_km: Optional[float] = None
    fuel_level_pct: Optional[float] = None
    engine_rpm: Optional[int] = None
    ignition: Optional[str] = None
    source: str

    model_config = {"from_attributes": True}


# ── Alerts ────────────────────────────────────────────────────────────────────

AlertType = Literal["speeding", "geofence_enter", "geofence_exit", "low_fuel", "idle", "harsh_braking", "harsh_acceleration"]
AlertSeverity = Literal["info", "warning", "critical"]


class AlertCreateSchema(BaseModel):
    vehicle_id: int
    driver_id: Optional[int] = None
    trip_id: Optional[int] = None
    alert_type: AlertType
    severity: AlertSeverity = "warning"
    message: str = Field(..., max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)


class AlertResponseSchema(BaseModel):
    id: int
    vehicle_id: int
    driver_id: Optional[int] = None
    trip_id: Optional[int] = None
    alert_type: str
    severity: str
    message: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_acknowledged: bool
    acknowledged_at: Optional[datetime] = None
    triggered_at: datetime

    model_config = {"from_attributes": True}


# ── Maintenance ───────────────────────────────────────────────────────────────

MaintenanceStatus = Literal["scheduled", "in_progress", "completed", "overdue"]


class MaintenanceCreateSchema(BaseModel):
    vehicle_id: int
    service_type: str
    scheduled_at: Optional[datetime] = None
    next_service_km: Optional[float] = Field(None, ge=0)
    next_service_date: Optional[datetime] = None
    technician: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)
    cost_eur: Optional[float] = Field(None, ge=0)


class MaintenancePatchSchema(BaseModel):
    status: Optional[MaintenanceStatus] = None
    completed_at: Optional[datetime] = None
    odometer_at_service_km: Optional[float] = Field(None, ge=0)
    next_service_km: Optional[float] = Field(None, ge=0)
    next_service_date: Optional[datetime] = None
    technician: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)
    cost_eur: Optional[float] = Field(None, ge=0)


class MaintenanceResponseSchema(BaseModel):
    id: int
    vehicle_id: int
    service_type: str
    status: str
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    odometer_at_service_km: Optional[float] = None
    next_service_km: Optional[float] = None
    next_service_date: Optional[datetime] = None
    technician: Optional[str] = None
    notes: Optional[str] = None
    cost_eur: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
