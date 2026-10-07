class LocalDeploymentProvider:
    """A deterministic local stand-in for cloud/container operations."""

    def provision(self, application: str, environment: str) -> str:
        return f"environment-ready:{application}:{environment}"

    def deploy(self, application: str, version: str) -> str:
        return f"deployment-ready:{application}:{version}"

    def health_check(self, application: str, simulate_failure: bool) -> bool:
        return not simulate_failure

    def rollback(self, application: str, version: str) -> str:
        return f"rollback-complete:{application}:{version}"
