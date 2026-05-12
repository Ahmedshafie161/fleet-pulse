class TestGetUsers:
    def test_list_users(self, client, admin_user):
        resp = client.get("/api/v1/users")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1
        assert resp.json()[0]["username"] == "admin"


class TestChangePassword:
    def test_change_password_success(self, client):
        resp = client.post("/api/v1/users/password", json={
            "old_password": "admin1234",
            "new_password": "newpassword99",
        })
        assert resp.status_code == 204

    def test_wrong_old_password(self, client):
        resp = client.post("/api/v1/users/password", json={
            "old_password": "wrongpassword",
            "new_password": "newpassword99",
        })
        assert resp.status_code == 422

    def test_short_new_password(self, client):
        resp = client.post("/api/v1/users/password", json={
            "old_password": "admin1234",
            "new_password": "short",
        })
        assert resp.status_code == 422
