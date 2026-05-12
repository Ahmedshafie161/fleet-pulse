from restapi.db.models import FleetConfig
from restapi.schemas.fleet_config import FleetConfigSchema


def _config(ref="cfg_default", display="Default Config"):
    schema = FleetConfigSchema(
        reference_name=ref,
        display_name=display,
        idle_alert_threshold_minutes=15,
        low_fuel_threshold_pct=15.0,
    )
    return FleetConfig.create_or_update(schema, save=True)


class TestListConfigs:
    def test_list_empty(self, client):
        resp = client.get("/api/v1/fleet-config")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_configs(self, client):
        _config()
        resp = client.get("/api/v1/fleet-config")
        assert resp.status_code == 200
        assert len(resp.json()) == 1


class TestCreateConfig:
    def test_create_success(self, client):
        resp = client.post("/api/v1/fleet-config", json={
            "reference_name": "cfg_alpha",
            "display_name": "Alpha Config",
            "idle_alert_threshold_minutes": 20,
            "low_fuel_threshold_pct": 10.0,
        })
        assert resp.status_code == 201
        assert resp.json()["reference_name"] == "cfg_alpha"

    def test_duplicate_display_name_rejected(self, client):
        _config(ref="cfg_a", display="Shared Name")
        resp = client.post("/api/v1/fleet-config", json={
            "reference_name": "cfg_b",
            "display_name": "Shared Name",
            "idle_alert_threshold_minutes": 10,
            "low_fuel_threshold_pct": 15.0,
        })
        assert resp.status_code == 422


class TestActivateConfig:
    def test_activate(self, client):
        _config(ref="cfg_x", display="Config X")
        resp = client.post("/api/v1/fleet-config/cfg_x/activate")
        assert resp.status_code == 200

        active_resp = client.get("/api/v1/fleet-config/active")
        assert active_resp.status_code == 200
        assert active_resp.json()["reference_name"] == "cfg_x"

    def test_activate_not_found(self, client):
        resp = client.post("/api/v1/fleet-config/nonexistent/activate")
        assert resp.status_code == 404


class TestDeleteConfig:
    def test_delete_inactive(self, client):
        _config(ref="cfg_del", display="To Delete")
        resp = client.delete("/api/v1/fleet-config/cfg_del")
        assert resp.status_code == 204

    def test_delete_active_rejected(self, client):
        _config(ref="cfg_active", display="Active Config")
        client.post("/api/v1/fleet-config/cfg_active/activate")
        resp = client.delete("/api/v1/fleet-config/cfg_active")
        assert resp.status_code == 422
