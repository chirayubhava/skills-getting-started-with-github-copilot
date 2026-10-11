from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def setup_function():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu"],
            },
        }
    )


def test_unregister_participant_removes_email():
    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"


def test_unregister_participant_raises_if_not_signed_up():
    response = client.delete("/activities/Programming Class/signup?email=not-registered@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
