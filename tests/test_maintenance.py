from datetime import datetime

from restapi.db.models import MaintenanceRecord, Vehicle


def _vehicle():
    return Vehicle.create(
        save=True, vin="VIN00000000000001", plate="HB-MNT-001",
        make="Iveco", model="Daily", year=2021, fuel_type="diesel",
        odometer_km=50000.0, is_active=True,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )


class TestMaintenanceList:
    def test_list_empty(self, client):
        assert client.get("/api/v1/maintenance").json() == []

    def test_filter_by_vehicle(self, client):
        v = _vehicle()
        MaintenanceRecord.create(
            save=True, vehicle_id=v.id, service_type="oil_change",
            status="scheduled", created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
        )
        resp = client.get(f"/api/v1/maintenance?vehicle_id={v.id}")
        assert len(resp.json()) == 1


class TestCreateMaintenance:
    def test_create_success(self, client):
        v = _vehicle()
        resp = client.post("/api/v1/maintenance", json={
            "vehicle_id": v.id,
            "service_type": "tyre_rotation",
            "next_service_km": 70000.0,
        })
        assert resp.status_code == 201
        assert resp.json()["service_type"] == "tyre_rotation"
        assert resp.json()["status"] == "scheduled"

    def test_unknown_vehicle(self, client):
        resp = client.post("/api/v1/maintenance", json={
            "vehicle_id": 9999,
            "service_type": "oil_change",
        })
        assert resp.status_code == 404


class TestPatchMaintenance:
    def test_mark_completed(self, client):
        v = _vehicle()
        r = MaintenanceRecord.create(
            save=True, vehicle_id=v.id, service_type="brake_service",
            status="scheduled", created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
        )
        resp = client.patch(f"/api/v1/maintenance/{r.id}", json={
            "status": "completed",
            "odometer_at_service_km": 52000.0,
            "cost_eur": 380.0,
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "completed"
