from restapi.db.models.user import User
from restapi.db.models.vehicle import Vehicle
from restapi.db.models.driver import Driver
from restapi.db.models.trip import Trip
from restapi.db.models.telemetry import Telemetry
from restapi.db.models.alert import Alert
from restapi.db.models.maintenance import MaintenanceRecord
from restapi.db.models.fleet_config import FleetConfig

__all__ = [
    "User",
    "Vehicle",
    "Driver",
    "Trip",
    "Telemetry",
    "Alert",
    "MaintenanceRecord",
    "FleetConfig",
]
