from fastapi.testclient import TestClient

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.main import app


client = TestClient(app)


def test_advanced_filter_by_priority():
    """Create tasks with different priorities and filter by high priority."""
    # Create a high priority task
    response = client.post(
        "/v1/tasks/create",
        json={"title": "Urgent task", "details": "High priority", "priority": "high"},
    )
    assert response.status_code == 200
    high_task = response.json()

    # Create a low priority task
    response = client.post(
        "/v1/tasks/create",
        json={"title": "Low priority task", "details": "Can wait", "priority": "low"},
    )
    assert response.status_code == 200

    # Filter by high priority
    response = client.get("/v1/tasks/filter?priority=high")
    assert response.status_code == 200
    filtered = response.json()
    assert len(filtered) >= 1
    assert any(t["id"] == high_task["id"] for t in filtered)


def test_advanced_filter_by_status():
    """Create tasks with different statuses and filter."""
    # Create a done task
    response = client.post(
        "/v1/tasks/create",
        json={"title": "Completed task", "details": "", "priority": "medium"},
    )
    assert response.status_code == 200
    task_id = response.json()["id"]

    # Mark as done
    client.patch(f"/v1/tasks/{task_id}/status", json={"status": "done"})

    # Filter by done status
    response = client.get("/v1/tasks/filter?status=done")
    assert response.status_code == 200
    filtered = response.json()
    assert len(filtered) >= 1
    assert any(t["id"] == task_id for t in filtered)


def test_advanced_filter_with_title_query():
    """Filter tasks by title/details text query."""
    # Create a task with unique text
    response = client.post(
        "/v1/tasks/create",
        json={
            "title": "Unique search term test",
            "details": "This is searchable",
            "priority": "medium",
        },
    )
    assert response.status_code == 200
    task = response.json()

    # Filter by title query
    response = client.get("/v1/tasks/filter?title_query=search%20term")
    assert response.status_code == 200
    filtered = response.json()
    assert len(filtered) >= 1
    assert any(t["id"] == task["id"] for t in filtered)


def test_advanced_filter_combined():
    """Test multiple filters together."""
    # Create tasks
    response = client.post(
        "/v1/tasks/create",
        json={"title": "Combined test", "details": "", "priority": "high"},
    )
    assert response.status_code == 200

    # Filter by priority AND title
    response = client.get(
        "/v1/tasks/filter?priority=high&title_query=Combined"
    )
    assert response.status_code == 200
    filtered = response.json()
    assert all(t["priority"] == "high" for t in filtered)
    assert all("Combined" in t["title"] or "Combined" in t["details"] for t in filtered)


def test_filter_returns_timestamp_fields():
    """Ensure filter response includes created_at and updated_at."""
    # Create a task
    response = client.post(
        "/v1/tasks/create",
        json={"title": "Timestamp test", "details": "", "priority": "medium"},
    )
    assert response.status_code == 200

    # Filter and check fields
    response = client.get("/v1/tasks/filter")
    assert response.status_code == 200
    filtered = response.json()
    assert len(filtered) >= 1
    task = filtered[0]
    assert "created_at" in task
    assert "updated_at" in task
    assert task["created_at"]  # Should have ISO format timestamp
    assert task["updated_at"]  # Should have ISO format timestamp
