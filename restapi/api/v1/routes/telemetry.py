from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from restapi.core.auth import get_current_user
from restapi.db.models import Telemetry, Vehicle
from restapi.schemas.fleet_entities import TelemetryCreateSchema, TelemetryResponseSchema

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.get("", response_model=list[TelemetryResponseSchema])
def list_telemetry(
    vehicle_id: Optional[int] = None,
    trip_id: Optional[int] = None,
    current_user=Depends(get_current_user),
):
    q = Telemetry._session.query(Telemetry)
    if vehicle_id is not None:
        q = q.filter(Telemetry.vehicle_id == vehicle_id)
    if trip_id is not None:
        q = q.filter(Telemetry.trip_id == trip_id)
    return q.all()


@router.post("", response_model=TelemetryResponseSchema, status_code=status.HTTP_201_CREATED)
def create_telemetry(body: TelemetryCreateSchema, current_user=Depends(get_current_user)):
    if not Vehicle._session.get(Vehicle, body.vehicle_id):
        raise HTTPException(status_code=404, detail="Vehicle not found")
    data = body.model_dump()
    if not data.get("recorded_at"):
        data["recorded_at"] = datetime.utcnow()
    return Telemetry.create(save=True, **data)
