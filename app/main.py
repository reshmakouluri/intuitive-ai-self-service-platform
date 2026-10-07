from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
import time

app = FastAPI(
    title="Self-Service Deployment Platform",
    description="Prototype API for self-service application deployments.",
    version="1.0.0",
)

deployments = {}


class DeploymentRequest(BaseModel):
    application: str
    version: str
    environment: str
    simulate_failure: bool = False


@app.get("/")
def root():
    return {
        "service": "self-service-deployment-platform",
        "status": "running"
    }


@app.post("/deployments")
def create_deployment(request: DeploymentRequest):
    deployment_id = str(uuid4())

    events = []

    def add_event(state, message):
        events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "state": state,
            "message": message
        })

    add_event("PENDING", "Deployment request received")
    add_event("VALIDATING", "Validating deployment request")
    add_event("PROVISIONING", "Provisioning deployment environment")
    add_event("DEPLOYING", f"Deploying {request.application}:{request.version}")
    add_event("HEALTH_CHECKING", "Running application health checks")

    if request.simulate_failure:
        add_event("FAILED", "Health check failed")
        add_event("ROLLING_BACK", "Rolling back deployment")
        add_event("ROLLED_BACK", "Deployment successfully rolled back")
        status = "ROLLED_BACK"
    else:
        add_event("SUCCEEDED", "Deployment completed successfully")
        status = "SUCCEEDED"

    deployment = {
        "id": deployment_id,
        "application": request.application,
        "version": request.version,
        "environment": request.environment,
        "status": status,
        "created_at": datetime.utcnow().isoformat(),
        "events": events
    }

    deployments[deployment_id] = deployment

    return deployment


@app.get("/deployments")
def list_deployments():
    return list(deployments.values())


@app.get("/deployments/{deployment_id}")
def get_deployment(deployment_id: str):
    deployment = deployments.get(deployment_id)

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    return deployment


@app.get("/deployments/{deployment_id}/events")
def get_deployment_events(deployment_id: str):
    deployment = deployments.get(deployment_id)

    if not deployment:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )

    return deployment["events"]
