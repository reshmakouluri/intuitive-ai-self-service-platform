from uuid import UUID, uuid4
from .models import Deployment, DeploymentEvent, DeploymentRequest, DeploymentState, utc_now
from .provider import LocalDeploymentProvider


class DeploymentNotFound(Exception):
    pass


class DeploymentService:
    def __init__(self, provider: LocalDeploymentProvider | None = None):
        self.provider = provider or LocalDeploymentProvider()
        self.deployments: dict[UUID, Deployment] = {}
        self.events: dict[UUID, list[DeploymentEvent]] = {}

    def _record(self, deployment: Deployment, state: DeploymentState, message: str) -> None:
        now = utc_now()
        deployment.state = state
        deployment.updated_at = now
        self.events[deployment.id].append(DeploymentEvent(timestamp=now, state=state, message=message))

    def create(self, request: DeploymentRequest) -> Deployment:
        now = utc_now()
        deployment = Deployment(
            id=uuid4(), application=request.application, version=request.version,
            environment=request.environment, state=DeploymentState.PENDING,
            created_at=now, updated_at=now,
        )
        self.deployments[deployment.id] = deployment
        self.events[deployment.id] = []
        self._record(deployment, DeploymentState.VALIDATING, "Deployment request validated")
        self._record(deployment, DeploymentState.PROVISIONING, "Provisioning staging environment")
        self.provider.provision(deployment.application, deployment.environment)
        self._record(deployment, DeploymentState.DEPLOYING, f"Deploying version {deployment.version}")
        self.provider.deploy(deployment.application, deployment.version)
        self._record(deployment, DeploymentState.HEALTH_CHECKING, "Running application health check")
        healthy = self.provider.health_check(deployment.application, request.simulate_failure)
        if healthy:
            self._record(deployment, DeploymentState.SUCCEEDED, "Health check passed; deployment completed")
        else:
            deployment.error = "Application health check failed"
            self._record(deployment, DeploymentState.FAILED, deployment.error)
            self._record(deployment, DeploymentState.ROLLING_BACK, "Starting rollback")
            self.provider.rollback(deployment.application, deployment.version)
            self._record(deployment, DeploymentState.ROLLED_BACK, "Rollback completed successfully")
        return deployment

    def get(self, deployment_id: UUID) -> Deployment:
        try:
            return self.deployments[deployment_id]
        except KeyError as exc:
            raise DeploymentNotFound from exc

    def get_events(self, deployment_id: UUID) -> list[DeploymentEvent]:
        self.get(deployment_id)
        return self.events[deployment_id]
