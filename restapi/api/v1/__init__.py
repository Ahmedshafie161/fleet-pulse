from fastapi import APIRouter

from restapi.api.v1.routes import (
    alerts,
    auth,
    drivers,
    fleet_config,
    maintenance,
    telemetry,
    trips,
    users,
    vehicles,
)

router = APIRouter()

# Auth (no JWT required on login itself — handled inside the route)
router.include_router(auth.router)

# User management
router.include_router(users.router)

# Core fleet resources
router.include_router(vehicles.router)
router.include_router(drivers.router)

# Operational data
router.include_router(trips.router)
router.include_router(telemetry.router)
router.include_router(alerts.router)
router.include_router(maintenance.router)

# Configuration
router.include_router(fleet_config.router)
