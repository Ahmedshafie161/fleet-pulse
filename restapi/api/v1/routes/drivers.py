from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status

from restapi.core.auth import get_current_user
from restapi.db.models import Driver, User  
from restapi.schemas.drivers import DriverCreateSchema, DriverPatchSchema, DriverResponseSchema

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.get("", response_model=list[DriverResponseSchema])
def list_drivers(current_user: User = Depends(get_current_user)):
    session = Driver.session()
    return session.query(Driver).all()


@router.post("", response_model=DriverResponseSchema, status_code=status.HTTP_201_CREATED)
def create_driver(body: DriverCreateSchema, current_user: User = Depends(get_current_user)):
    session = Driver.session()
    existing = session.query(Driver).filter_by(license_number=body.license_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="License number already registered",
        )
    now = datetime.now(timezone.utc)
    return Driver.create(
        save=True,
        **body.model_dump(),
        is_active=True,
        created_at=now,
        updated_at=now,
    )


@router.get("/{driver_id}", response_model=DriverResponseSchema)
def get_driver(driver_id: int, current_user: User = Depends(get_current_user)):
    session = Driver.session()
    d = session.get(Driver, driver_id)
    if not d:
        raise HTTPException(status_code=404, detail="Driver not found")
    return d


@router.patch("/{driver_id}", response_model=DriverResponseSchema)
def patch_driver(
    driver_id: int,
    body: DriverPatchSchema,
    current_user: User = Depends(get_current_user),
):
    session = Driver.session()
    d = session.get(Driver, driver_id)
    if not d:
        raise HTTPException(status_code=404, detail="Driver not found")
    for key, value in body.model_dump(exclude_none=True).items():
        setattr(d, key, value)
    d.updated_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(d)
    return d


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver(driver_id: int, current_user: User = Depends(get_current_user)):
    session = Driver.session()
    d = session.get(Driver, driver_id)
    if not d:
        raise HTTPException(status_code=404, detail="Driver not found")
    session.delete(d)
    session.commit()