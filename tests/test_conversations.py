from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_conversation_create_and_message() -> None:
    response = client.post(
        "/v1/conversations/create",
        json={"title": "Test conversation"},
        headers={"x-api-key": ""},
    )
    assert response.status_code in (200, 401)

    if response.status_code == 401:
        return

    conversation = response.json()
    conv_id = conversation["id"]

    msg_response = client.post(
        f"/v1/conversations/{conv_id}/message",
        json={"role": "user", "content": "Hello"},
    )
    assert msg_response.status_code == 200
    payload = msg_response.json()
    assert payload["id"] == conv_id
    assert payload["messages"]
