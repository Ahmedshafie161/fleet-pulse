from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from restapi.db.models.base import BaseModel

from restapi.schemas.fleet_config import FleetConfigSchema


class FleetConfig(BaseModel):
    __tablename__ = "fleet_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    reference_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    idle_alert_threshold_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=15,
    )

    low_fuel_threshold_pct: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=15.0,
    )

    speed_limit_kmh: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    @classmethod
    def create_or_update(
        cls,
        schema: FleetConfigSchema,
        save: bool = False,
    ) -> "FleetConfig":
        data = schema.model_dump()
        now = datetime.now(UTC)


        session = BaseModel.session()

        existing = (
            session.query(cls)
            .filter_by(reference_name=data["reference_name"])
            .first()
        )

        if existing:
            for key, value in data.items():
                setattr(existing, key, value)

            existing.updated_at = now
            obj = existing

        else:
            obj = cls(
                **data,
                is_active=False,
                created_at=now,
                updated_at=now,
            )

        if save:
            session.add(obj)
            session.commit()
            session.refresh(obj)

        return obj