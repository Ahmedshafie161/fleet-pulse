from .user import User
from .vehicle import Vehicle
from .driver import Driver
from .trip import Trip
from .telemetry import Telemetry
from .alert import Alert
from .maintenance import MaintenanceRecord
from .fleet_config import FleetConfig

__all__ = [
    "Vehicle",
    "Telemetry",
    "Alert",
    "MaintenanceRecord",
    "FleetConfig",
    "Trip",
    "Driver",
    "User",
]