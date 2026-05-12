from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from restapi.core.auth import get_current_user
from restapi.db.models import Trip, Vehicle, User  
from restapi.schemas.fleet_entities import TripCreateSchema, TripPatchSchema, TripResponseSchema

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("", response_model=list[TripResponseSchema])
def list_trips(
    vehicle_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),  
):
    q = Trip.session().query(Trip)  
    if vehicle_id is not None:
        q = q.filter(Trip.vehicle_id == vehicle_id)
    return q.all()


@router.post("", response_model=TripResponseSchema, status_code=status.HTTP_201_CREATED)
def create_trip(
    body: TripCreateSchema,
    current_user: User = Depends(get_current_user),
):
    session = Trip.session()
    if not session.get(Vehicle, body.vehicle_id):
        raise HTTPException(status_code=404, detail="Vehicle not found")
    now = datetime.utcnow()
    return Trip.create(
        save=True,
        **body.model_dump(),
        started_at=now,
        status="in_progress",
        created_at=now,
    )


@router.get("/{trip_id}", response_model=TripResponseSchema)
def get_trip(
    trip_id: int,
    current_user: User = Depends(get_current_user),
):
    session = Trip.session()
    t = session.get(Trip, trip_id)
    if not t:
        raise HTTPException(status_code=404, detail="Trip not found")
    return t


@router.patch("/{trip_id}", response_model=TripResponseSchema)
def patch_trip(
    trip_id: int,
    body: TripPatchSchema,
    current_user: User = Depends(get_current_user),
):
    session = Trip.session()
    t = session.get(Trip, trip_id)
    if not t:
        raise HTTPException(status_code=404, detail="Trip not found")
    for key, value in body.model_dump(exclude_none=True).items():
        setattr(t, key, value)
    session.commit()
    session.refresh(t)
    return t