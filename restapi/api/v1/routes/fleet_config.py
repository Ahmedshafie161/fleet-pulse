from fastapi import APIRouter, Depends, HTTPException, status

from restapi.core.auth import get_current_user
from restapi.db.models import FleetConfig, User  
from restapi.schemas.fleet_config import FleetConfigResponseSchema, FleetConfigSchema

router = APIRouter(prefix="/fleet-config", tags=["fleet-config"])


@router.get("", response_model=list[FleetConfigResponseSchema])
def list_configs(current_user: User = Depends(get_current_user)):
    session = FleetConfig.session()
    return session.query(FleetConfig).all()


@router.get("/active", response_model=FleetConfigResponseSchema)
def get_active_config(current_user: User = Depends(get_current_user)):
    session = FleetConfig.session()
    cfg = session.query(FleetConfig).filter_by(is_active=True).first()
    if not cfg:
        raise HTTPException(status_code=404, detail="No active configuration")
    return cfg


@router.post("", response_model=FleetConfigResponseSchema, status_code=status.HTTP_201_CREATED)
def create_config(body: FleetConfigSchema, current_user: User = Depends(get_current_user)):
    session = FleetConfig.session()
    duplicate = session.query(FleetConfig).filter_by(display_name=body.display_name).first()
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A config with this display_name already exists",
        )
    return FleetConfig.create_or_update(body, save=True)


@router.post("/{reference_name}/activate", response_model=FleetConfigResponseSchema)
def activate_config(reference_name: str, current_user: User = Depends(get_current_user)):
    session = FleetConfig.session()
    cfg = session.query(FleetConfig).filter_by(reference_name=reference_name).first()
    if not cfg:
        raise HTTPException(status_code=404, detail="Configuration not found")
    session.query(FleetConfig).update({"is_active": False})
    cfg.is_active = True
    session.commit()
    session.refresh(cfg)
    return cfg


@router.delete("/{reference_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_config(reference_name: str, current_user: User = Depends(get_current_user)):
    session = FleetConfig.session()
    cfg = session.query(FleetConfig).filter_by(reference_name=reference_name).first()
    if not cfg:
        raise HTTPException(status_code=404, detail="Configuration not found")
    if cfg.is_active:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cannot delete the active configuration",
        )
    session.delete(cfg)
    session.commit()