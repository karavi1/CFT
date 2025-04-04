import pytest
from uuid import uuid4

def setup_logged_workout(client):
    # Create user and exercise
    client.post("/users/", json={"email": "logapi@example.com", "username": "logapiuser"})
    client.post("/exercises/", json={"name": "Row", "primary_muscles": ["back"]})

    # Create workout with one logged exercise
    resp = client.post("/workouts/", json={
        "username": "logapiuser",
        "notes": "Back day",
        "logged_exercises": [{
            "name": "Row",
            "sets": 3,
            "reps": 10,
            "weight": 80.0
        }]
    })
    return resp.json()["id"]  # workout_id

def test_log_new_exercise(client):
    workout_id = setup_logged_workout(client)

    # Get the exercise ID
    ex_resp = client.get("/exercises/")
    exercise_id = ex_resp.json()[0]["id"]

    # Log another exercise
    log_resp = client.post(f"/logged_exercises/{workout_id}/log", json={
        "exercise_id": exercise_id,
        "sets": 4,
        "reps": 6,
        "weight": 90.0
    })

    assert log_resp.status_code == 200
    data = log_resp.json()
    assert data["sets"] == 4
    assert data["workout_id"] == workout_id

def test_get_logged_exercises_by_workout(client):
    workout_id = setup_logged_workout(client)

    response = client.get(f"/logged_exercises/{workout_id}/entries")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "sets" in data[0]

def test_delete_logged_exercise(client):
    workout_id = setup_logged_workout(client)

    # Get exercise_id from the existing log
    log_resp = client.get(f"/logged_exercises/{workout_id}/entries")
    assert log_resp.status_code == 200
    exercise_id = log_resp.json()[0]["exercise"]["id"]

    # Delete it
    del_resp = client.delete(f"/logged_exercises/{workout_id}/entry/{exercise_id}")
    assert del_resp.status_code == 200
    assert del_resp.json() is True

    # Confirm it's gone
    confirm = client.get(f"/logged_exercises/{workout_id}/entries")
    assert len(confirm.json()) == 0

def test_delete_logged_exercise_not_found(client):
    workout_id = setup_logged_workout(client)
    fake_exercise_id = uuid4()

    response = client.delete(f"/logged_exercises/{workout_id}/entry/{fake_exercise_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Logged exercise not found"