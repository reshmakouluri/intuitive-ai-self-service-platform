from fastapi.testclient import TestClient
from app.main import app, service

client = TestClient(app)


def setup_function():
    service.deployments.clear()
    service.events.clear()


def test_successful_deployment():
    response = client.post("/deployments", json={"application": "orders-api", "version": "1.4.2", "environment": "staging"})
    assert response.status_code == 201
    deployment = response.json()
    assert deployment["state"] == "SUCCEEDED"
    events = client.get(f"/deployments/{deployment['id']}/events").json()
    assert [event["state"] for event in events] == ["VALIDATING", "PROVISIONING", "DEPLOYING", "HEALTH_CHECKING", "SUCCEEDED"]


def test_failed_health_check_rolls_back():
    response = client.post("/deployments", json={"application": "orders-api", "version": "1.4.3", "environment": "staging", "simulate_failure": True})
    assert response.status_code == 201
    deployment = response.json()
    assert deployment["state"] == "ROLLED_BACK"
    assert deployment["error"] == "Application health check failed"
    events = client.get(f"/deployments/{deployment['id']}/events").json()
    assert [event["state"] for event in events][-3:] == ["FAILED", "ROLLING_BACK", "ROLLED_BACK"]


def test_only_staging_is_supported():
    response = client.post("/deployments", json={"application": "orders-api", "version": "1.0", "environment": "production"})
    assert response.status_code == 422
