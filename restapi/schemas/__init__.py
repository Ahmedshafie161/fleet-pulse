# restapi/schemas/__init__.py

# Common responses
from .common import COMMON_200_401_RESPONSES, COMMON_204_401_RESPONSES  # noqa: F401

# Auth schemas
from .auth import TokenSchema  # noqa: F401

# User schemas
from .users import UserPasswordPostSchema, UserResponseSchema  # noqa: F401

# Driver schemas
from .drivers import DriverCreateSchema, DriverPatchSchema, DriverResponseSchema  # noqa: F401

# Fleet config schemas
from .fleet_config import FleetConfigSchema, FleetConfigResponseSchema  # noqa: F401

# Fleet entities (trips, etc.)
from .fleet_entities import TripCreateSchema, TripPatchSchema, TripResponseSchema  # noqa: F401

__all__ = [
    "COMMON_200_401_RESPONSES",
    "COMMON_204_401_RESPONSES",
    "TokenSchema",
    "UserPasswordPostSchema",
    "UserResponseSchema",
    "DriverCreateSchema",
    "DriverPatchSchema",
    "DriverResponseSchema",
    "FleetConfigSchema",
    "FleetConfigResponseSchema",
    "TripCreateSchema", 
    "TripPatchSchema",
    "TripResponseSchema",
]