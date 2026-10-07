from uuid import UUID
from fastapi import FastAPI, HTTPException
from .models import Deployment, DeploymentEvent, DeploymentRequest
from .service import DeploymentNotFound, DeploymentService

app = FastAPI(title="Self-Service Deployment Platform", version="0.1.0")
service = DeploymentService()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/deployments", response_model=Deployment, status_code=201)
def create_deployment(request: DeploymentRequest) -> Deployment:
    return service.create(request)


@app.get("/deployments/{deployment_id}", response_model=Deployment)
def get_deployment(deployment_id: UUID) -> Deployment:
    try:
        return service.get(deployment_id)
    except DeploymentNotFound:
        raise HTTPException(status_code=404, detail="Deployment not found")


@app.get("/deployments/{deployment_id}/events", response_model=list[DeploymentEvent])
def get_events(deployment_id: UUID) -> list[DeploymentEvent]:
    try:
        return service.get_events(deployment_id)
    except DeploymentNotFound:
        raise HTTPException(status_code=404, detail="Deployment not found")
