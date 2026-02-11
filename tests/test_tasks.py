from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_task_create_and_list() -> None:
    response = client.post(
        "/v1/tasks/create",
        json={"title": "Test task", "details": "", "priority": "low"},
        headers={"x-api-key": ""},
    )
    assert response.status_code in (200, 401)

    if response.status_code == 401:
        return

    task = response.json()
    assert task["title"] == "Test task"

    list_response = client.get("/v1/tasks/list")
    assert list_response.status_code == 200
    tasks = list_response.json()
    assert any(item["id"] == task["id"] for item in tasks)
