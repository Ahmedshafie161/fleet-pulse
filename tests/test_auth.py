from fastapi.testclient import TestClient

from restapi.server import app


class TestLogin:
    def test_login_success(self, admin_user):
        with TestClient(app) as c:
            resp = c.post(
                "/api/v1/auth/login",
                data={"username": "admin", "password": "admin1234"},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, admin_user):
        with TestClient(app) as c:
            resp = c.post(
                "/api/v1/auth/login",
                data={"username": "admin", "password": "wrongpass"},
            )
        assert resp.status_code == 401

    def test_login_unknown_user(self):
        with TestClient(app) as c:
            resp = c.post(
                "/api/v1/auth/login",
                data={"username": "ghost", "password": "whatever"},
            )
        assert resp.status_code == 401
