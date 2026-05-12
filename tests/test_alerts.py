from datetime import datetime

from restapi.db.models import Alert, Vehicle


def _make_vehicle():
    return Vehicle.create(
        save=True,
        vin="1HGCM82633A000001",
        plate="HB-TEST-001",
        make="Scania",
        model="R500",
        year=2022,
        fuel_type="diesel",
        odometer_km=0.0,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


def _make_alert(vehicle_id, **kwargs):
    defaults = dict(
        alert_type="speeding",
        severity="warning",
        message="Speed limit exceeded at 130 km/h",
        is_acknowledged=False,
        triggered_at=datetime.utcnow(),
    )
    defaults.update(kwargs)
    return Alert.create(save=True, vehicle_id=vehicle_id, **defaults)


class TestListAlerts:
    def test_list_empty(self, client):
        resp = client.get("/api/v1/alerts")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_filter_by_vehicle(self, client):
        v = _make_vehicle()
        _make_alert(v.id)
        resp = client.get(f"/api/v1/alerts?vehicle_id={v.id}")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_filter_unacknowledged(self, client):
        v = _make_vehicle()
        _make_alert(v.id, is_acknowledged=False)
        _make_alert(v.id, is_acknowledged=True, acknowledged_at=datetime.utcnow())
        resp = client.get("/api/v1/alerts?acknowledged=false")
        assert resp.status_code == 200
        assert all(not a["is_acknowledged"] for a in resp.json())


class TestCreateAlert:
    def test_create_alert(self, client):
        v = _make_vehicle()
        resp = client.post("/api/v1/alerts", json={
            "vehicle_id": v.id,
            "alert_type": "low_fuel",
            "severity": "critical",
            "message": "Fuel below 10%",
        })
        assert resp.status_code == 201
        assert resp.json()["alert_type"] == "low_fuel"

    def test_unknown_vehicle_rejected(self, client):
        resp = client.post("/api/v1/alerts", json={
            "vehicle_id": 9999,
            "alert_type": "speeding",
            "severity": "warning",
            "message": "test",
        })
        assert resp.status_code == 404


class TestAcknowledgeAlert:
    def test_acknowledge(self, client):
        v = _make_vehicle()
        a = _make_alert(v.id)
        resp = client.post(f"/api/v1/alerts/{a.id}/acknowledge")
        assert resp.status_code == 200
        assert resp.json()["is_acknowledged"] is True

    def test_double_acknowledge_rejected(self, client):
        v = _make_vehicle()
        a = _make_alert(v.id, is_acknowledged=True, acknowledged_at=datetime.utcnow())
        resp = client.post(f"/api/v1/alerts/{a.id}/acknowledge")
        assert resp.status_code == 422
