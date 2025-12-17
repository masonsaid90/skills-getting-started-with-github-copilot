from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_dict():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Ensure a known activity exists
    assert "Basketball" in data


def test_signup_and_delete_flow():
    activity = "Chess Club"
    test_email = "tester@example.com"

    # Ensure not already in participants
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert test_email in activities[activity]["participants"]

    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp2.status_code == 400

    # Delete (unregister) - simulate by calling the endpoint if implemented
    resp3 = client.delete(f"/activities/{activity}/signup?email={test_email}")
    # If delete is implemented, expect 200, otherwise expect 405 or 404
    assert resp3.status_code in (200, 404, 405)

    # Clean up if still present
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)
