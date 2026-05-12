from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from restapi.db.models.base import BaseModel


class Trip(BaseModel):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    start_lat = Column(Float, nullable=True)
    start_lng = Column(Float, nullable=True)
    end_lat = Column(Float, nullable=True)
    end_lng = Column(Float, nullable=True)
    distance_km = Column(Float, nullable=True)
    max_speed_kmh = Column(Float, nullable=True)
    avg_speed_kmh = Column(Float, nullable=True)
    fuel_consumed_l = Column(Float, nullable=True)
    status = Column(String(20), nullable=False, default="in_progress")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
