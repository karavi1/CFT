import pytest
from uuid import UUID, uuid4

def test_create_exercise(client):
    response = client.post("/exercises/", json={
        "name": "Bench Press",
        "primary_muscles": ["chest", "triceps"],
        "secondary_muscles": ["shoulders"],
        "description": "Upper-body compound pressing movement"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bench Press"
    assert "id" in data
    assert isinstance(UUID(data["id"]), UUID)

def test_create_exercise_minimal_fields(client):
    response = client.post("/exercises/", json={
        "name": "Lunge",
        "primary_muscles": ["quads"]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Lunge"
    assert data["primary_muscles"] == ["quads"]
    assert data["secondary_muscles"] is None or data["secondary_muscles"] == []
    assert data.get("description") in (None, "")

def test_get_exercise_by_id(client):
    # Create exercise
    response = client.post("/exercises/", json={
        "name": "Squat",
        "primary_muscles": ["quads", "glutes"]
    })
    exercise_id = response.json()["id"]

    # Fetch by ID
    get_response = client.get(f"/exercises/{exercise_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Squat"

def test_get_exercise_by_id_not_found(client):
    response = client.get(f"/exercises/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise not found"

def test_get_all_exercises(client):
    client.post("/exercises/", json={
        "name": "Deadlift",
        "primary_muscles": ["back", "glutes"]
    })
    client.post("/exercises/", json={
        "name": "Overhead Press",
        "primary_muscles": ["shoulders"]
    })

    response = client.get("/exercises/")
    assert response.status_code == 200
    exercises = response.json()
    assert isinstance(exercises, list)
    names = [e["name"] for e in exercises]
    assert "Deadlift" in names
    assert "Overhead Press" in names

def test_delete_exercise(client):
    response = client.post("/exercises/", json={
        "name": "Barbell Row",
        "primary_muscles": ["back"]
    })
    exercise_id = response.json()["id"]

    delete_response = client.delete(f"/exercises/{exercise_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() is True

    # Confirm it's gone
    get_response = client.get(f"/exercises/{exercise_id}")
    assert get_response.status_code == 404

def test_delete_exercise_not_found(client):
    response = client.delete(f"/exercises/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise not found"

def test_create_duplicate_exercise(client):
    exercise_data = {"name": "Deadlift", "primary_muscles": ["back"]}

    first = client.post("/exercises/", json=exercise_data)
    assert first.status_code == 200

    second = client.post("/exercises/", json=exercise_data)
    assert second.status_code == 409
    assert "already exists" in second.json()["detail"]

def test_update_exercise(client):
    create_resp = client.post("/exercises/", json={
        "name": "Cable Row",
        "primary_muscles": ["back"]
    })
    exercise_id = create_resp.json()["id"]

    patch_resp = client.patch(f"/exercises/?exercise_id={exercise_id}", json={
        "description": "Updated description"
    })

    assert patch_resp.status_code == 200
    assert patch_resp.json()["description"] == "Updated description"

def test_create_batch_exercises(client):
    payload = [
        {"name": "Pushup_Batch1", "primary_muscles": ["chest"]},
        {"name": "Plank_Batch1", "primary_muscles": ["core"]}
    ]

    response = client.post("/exercises/batch/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), f"Unexpected response: {data}"
    assert len(data) == 2
    print(data)
    names = [e["name"] for e in data]
    assert "Pushup_Batch1" in names
    assert "Plank_Batch1" in names

