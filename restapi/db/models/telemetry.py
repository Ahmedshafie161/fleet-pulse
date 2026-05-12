from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from restapi.db.models.base import BaseModel


class Telemetry(BaseModel):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True, index=True)
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed_kmh = Column(Float, nullable=True)
    heading_deg = Column(Float, nullable=True)
    altitude_m = Column(Float, nullable=True)
    odometer_km = Column(Float, nullable=True)
    fuel_level_pct = Column(Float, nullable=True)
    engine_rpm = Column(Integer, nullable=True)
    ignition = Column(String(5), nullable=True)
    source = Column(String(10), nullable=False, default="api")
