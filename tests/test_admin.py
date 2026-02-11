from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_admin_info_requires_key_or_is_configured() -> None:
    response = client.get("/v1/admin/info")
    assert response.status_code in (200, 401)

    if response.status_code == 200:
        payload = response.json()
        assert "app" in payload
        assert "uptime_seconds" in payload
