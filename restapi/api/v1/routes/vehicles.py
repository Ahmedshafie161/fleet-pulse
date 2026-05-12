from datetime import UTC, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from restapi.core.auth import get_current_user
from restapi.db.models import Vehicle

from restapi.schemas.common import (
    COMMON_200_401_404_RESPONSES,
    COMMON_201_401_RESPONSES,
    COMMON_204_401_404_RESPONSES,
)
from restapi.schemas.vehicles import (
    VehicleCreateSchema,
    VehiclePatchSchema,
    VehicleResponseSchema,
)

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
)


@router.get(
    "",
    response_model=list[VehicleResponseSchema],
)
def list_vehicles(
    current_user: Any = Depends(get_current_user),
):
    session = Vehicle.session()

    return session.query(Vehicle).all()


@router.post(
    "",
    response_model=VehicleResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses=COMMON_201_401_RESPONSES,
)
def create_vehicle(
    body: VehicleCreateSchema,
    current_user: Any = Depends(get_current_user),
):
    session = Vehicle.session()

    existing = (
        session.query(Vehicle)
        .filter_by(vin=body.vin)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A vehicle with this VIN already exists",
        )

    now = datetime.now(UTC)

    return Vehicle.create(
        save=True,
        **body.model_dump(),
        created_at=now,
        updated_at=now,
    )


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponseSchema,
    responses=COMMON_200_401_404_RESPONSES,
)
def get_vehicle(
    vehicle_id: int,
    current_user: Any = Depends(get_current_user),
):
    session = Vehicle.session()

    vehicle = session.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    return vehicle


@router.patch(
    "/{vehicle_id}",
    response_model=VehicleResponseSchema,
    responses=COMMON_200_401_404_RESPONSES,
)
def patch_vehicle(
    vehicle_id: int,
    body: VehiclePatchSchema,
    current_user: Any = Depends(get_current_user),
):
    session = Vehicle.session()

    vehicle = session.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    for key, value in body.model_dump(exclude_none=True).items():
        setattr(vehicle, key, value)

    setattr(vehicle, "updated_at", datetime.now(UTC))
    session.commit()
    session.refresh(vehicle)

    return vehicle


@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=COMMON_204_401_404_RESPONSES,
)
def delete_vehicle(
    vehicle_id: int,
    current_user: Any = Depends(get_current_user),
):
    session = Vehicle.session()

    vehicle = session.get(Vehicle, vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    session.delete(vehicle)
    session.commit()