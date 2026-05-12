from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from restapi.core.auth import get_current_user
from restapi.db.models import MaintenanceRecord, Vehicle
from restapi.schemas.fleet_entities import (
    MaintenanceCreateSchema,
    MaintenancePatchSchema,
    MaintenanceResponseSchema,
)

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.get("", response_model=list[MaintenanceResponseSchema])
def list_maintenance(
    vehicle_id: Optional[int] = None,
    current_user=Depends(get_current_user),
):
    q = MaintenanceRecord._session.query(MaintenanceRecord)
    if vehicle_id is not None:
        q = q.filter(MaintenanceRecord.vehicle_id == vehicle_id)
    return q.all()


@router.post("", response_model=MaintenanceResponseSchema, status_code=status.HTTP_201_CREATED)
def create_maintenance(body: MaintenanceCreateSchema, current_user=Depends(get_current_user)):
    if not Vehicle._session.get(Vehicle, body.vehicle_id):
        raise HTTPException(status_code=404, detail="Vehicle not found")
    now = datetime.utcnow()
    return MaintenanceRecord.create(
        save=True,
        **body.model_dump(),
        status="scheduled",
        created_at=now,
        updated_at=now,
    )


@router.patch("/{record_id}", response_model=MaintenanceResponseSchema)
def patch_maintenance(
    record_id: int,
    body: MaintenancePatchSchema,
    current_user=Depends(get_current_user),
):
    r = MaintenanceRecord._session.get(MaintenanceRecord, record_id)
    if not r:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    for key, value in body.model_dump(exclude_none=True).items():
        setattr(r, key, value)
    r.updated_at = datetime.utcnow()
    MaintenanceRecord._session.commit()
    MaintenanceRecord._session.refresh(r)
    return r
