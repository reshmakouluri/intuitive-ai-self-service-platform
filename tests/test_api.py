from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_successful_deployment():
    response = client.post(
        "/deployments",
        json={
            "application": "orders-api",
            "version": "1.4.2",
            "environment": "staging",
            "simulate_failure": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCEEDED"
    assert any(event["state"] == "PROVISIONING" for event in data["events"])
    assert any(event["state"] == "DEPLOYING" for event in data["events"])
    assert any(event["state"] == "HEALTH_CHECKING" for event in data["events"])
    assert any(event["state"] == "SUCCEEDED" for event in data["events"])


def test_failed_deployment_rolls_back():
    response = client.post(
        "/deployments",
        json={
            "application": "orders-api",
            "version": "1.4.3",
            "environment": "staging",
            "simulate_failure": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ROLLED_BACK"
    assert any(event["state"] == "FAILED" for event in data["events"])
    assert any(event["state"] == "ROLLING_BACK" for event in data["events"])
    assert any(event["state"] == "ROLLED_BACK" for event in data["events"])


def test_missing_deployment_returns_404():
    response = client.get("/deployments/does-not-exist")

    assert response.status_code == 404
