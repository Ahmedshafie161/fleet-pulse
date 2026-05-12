from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from restapi.core.auth import get_current_user
from restapi.db.models import Alert, Vehicle
from restapi.schemas.fleet_entities import AlertCreateSchema, AlertResponseSchema

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponseSchema])
def list_alerts(
    vehicle_id: Optional[int] = None,
    acknowledged: Optional[str] = None,   
    current_user=Depends(get_current_user),
):
    q = Alert._session.query(Alert)
    if vehicle_id is not None:
        q = q.filter(Alert.vehicle_id == vehicle_id)
    if acknowledged is not None:
        is_ack = acknowledged.strip().lower() == "true"
        q = q.filter(Alert.is_acknowledged == is_ack)
    return q.all()


@router.post("", response_model=AlertResponseSchema, status_code=status.HTTP_201_CREATED)
def create_alert(body: AlertCreateSchema, current_user=Depends(get_current_user)):
    if not Vehicle._session.get(Vehicle, body.vehicle_id):
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return Alert.create(
        save=True,
        **body.model_dump(),
        is_acknowledged=False,
        triggered_at=datetime.utcnow(),
    )


@router.post("/{alert_id}/acknowledge", response_model=AlertResponseSchema)
def acknowledge_alert(alert_id: int, current_user=Depends(get_current_user)):
    a = Alert._session.get(Alert, alert_id)
    if not a:
        raise HTTPException(status_code=404, detail="Alert not found")
    if a.is_acknowledged:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Alert is already acknowledged",
        )
    a.is_acknowledged = True
    a.acknowledged_at = datetime.utcnow()
    Alert._session.commit()
    Alert._session.refresh(a)
    return a
