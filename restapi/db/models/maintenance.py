from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from restapi.db.models.base import BaseModel


class MaintenanceRecord(BaseModel):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    service_type = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="scheduled")
    scheduled_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    odometer_at_service_km = Column(Float, nullable=True)
    next_service_km = Column(Float, nullable=True)
    next_service_date = Column(DateTime, nullable=True)
    technician = Column(String(200), nullable=True)
    notes = Column(String(500), nullable=True)
    cost_eur = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
