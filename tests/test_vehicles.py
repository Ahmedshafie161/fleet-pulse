from datetime import datetime

from restapi.db.models import Vehicle


def _make_vehicle(**kwargs):
    defaults = dict(
        vin="1HGCM82633A123456",
        plate="B-FP-001",
        make="Mercedes",
        model="Actros",
        year=2022,
        fuel_type="diesel",
        odometer_km=0.0,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    defaults.update(kwargs)
    return Vehicle.create(save=True, **defaults)


class TestVehiclesList:
    def test_list_empty(self, client):
        resp = client.get("/api/v1/vehicles")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_vehicles(self, client):
        _make_vehicle()
        resp = client.get("/api/v1/vehicles")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_requires_auth(self):
        from fastapi.testclient import TestClient
        from restapi.server import app
        with TestClient(app) as c:
            resp = c.get("/api/v1/vehicles")
        assert resp.status_code == 401


class TestCreateVehicle:
    def test_create_success(self, client):
        resp = client.post("/api/v1/vehicles", json={
            "vin": "1HGCM82633A123456",
            "plate": "HB-FP-001",
            "make": "Volvo",
            "model": "FH16",
            "year": 2023,
            "fuel_type": "diesel",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["vin"] == "1HGCM82633A123456"
        assert data["make"] == "Volvo"

    def test_duplicate_vin_rejected(self, client):
        _make_vehicle(vin="1HGCM82633A123456")
        resp = client.post("/api/v1/vehicles", json={
            "vin": "1HGCM82633A123456",
            "plate": "HB-FP-002",
            "make": "DAF",
            "model": "XF",
            "year": 2021,
        })
        assert resp.status_code == 422

    def test_invalid_vin_length(self, client):
        resp = client.post("/api/v1/vehicles", json={
            "vin": "SHORT",
            "plate": "HB-FP-003",
            "make": "MAN",
            "model": "TGX",
            "year": 2020,
        })
        assert resp.status_code == 422


class TestPatchVehicle:
    def test_patch_plate(self, client):
        v = _make_vehicle()
        resp = client.patch(f"/api/v1/vehicles/{v.id}", json={"plate": "HB-NEW-001"})
        assert resp.status_code == 200
        assert resp.json()["plate"] == "HB-NEW-001"

    def test_patch_not_found(self, client):
        resp = client.patch("/api/v1/vehicles/9999", json={"plate": "X"})
        assert resp.status_code == 404


class TestDeleteVehicle:
    def test_delete_success(self, client):
        v = _make_vehicle()
        resp = client.delete(f"/api/v1/vehicles/{v.id}")
        assert resp.status_code == 204

    def test_delete_not_found(self, client):
        resp = client.delete("/api/v1/vehicles/9999")
        assert resp.status_code == 404
