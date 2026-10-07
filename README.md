# Self-Service Application Deployment Platform

A small API-driven prototype for a developer self-service deployment workflow.

## Product goal

Reduce the lead time and operational coordination required for routine staging deployments while keeping failure handling explicit and recoverable.

A developer submits a deployment request. The platform validates it, provisions a simulated environment, deploys the requested version, performs a health check, and either completes successfully or rolls back when the health check fails.

## Scope

This is intentionally a prototype. It simulates infrastructure and deployment actions locally instead of provisioning real cloud resources. The focus is the product workflow, API contract, state handling, and failure recovery.

## Architecture

```text
CLI / API client
       |
       v
   FastAPI API
       |
       v
 Deployment Service
       |
       +--> Validator
       +--> Local Provider (simulated provisioning/deployment/health)
       +--> State Machine
       +--> Event History
```

## Workflow

```text
PENDING -> VALIDATING -> PROVISIONING -> DEPLOYING -> HEALTH_CHECKING -> SUCCEEDED
                                                        |
                                                        v
                                                     FAILED
                                                        |
                                                        v
                                                   ROLLING_BACK
                                                        |
                                                        v
                                                   ROLLED_BACK
```

The failure path is deterministic with `simulate_failure=true`, making the behavior easy to demonstrate.

## Setup

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.main:app --reload
```

API documentation is available at `http://127.0.0.1:8000/docs`.

## Successful deployment

```bash
curl -X POST http://127.0.0.1:8000/deployments \
  -H 'Content-Type: application/json' \
  -d '{"application":"orders-api","version":"1.4.2","environment":"staging"}'
```

Then query the returned deployment ID:

```bash
curl http://127.0.0.1:8000/deployments/<ID>
curl http://127.0.0.1:8000/deployments/<ID>/events
```

## Failure and rollback demo

```bash
curl -X POST http://127.0.0.1:8000/deployments \
  -H 'Content-Type: application/json' \
  -d '{"application":"orders-api","version":"1.4.3","environment":"staging","simulate_failure":true}'
```

The deployment ends in `ROLLED_BACK`, with events showing the failure and rollback steps.

## CLI

```bash
python -m app.cli deploy orders-api 1.4.2 staging
python -m app.cli deploy orders-api 1.4.3 staging --simulate-failure
python -m app.cli status <ID>
python -m app.cli events <ID>
```

## Product metric

Primary metric: **deployment lead time** — time from a valid deployment request to a successful or rolled-back terminal state.

Secondary metric: **self-service adoption** — percentage of eligible staging deployments completed through the platform without DevOps intervention.

## Product brief and capability map

See [`docs/product-brief.md`](docs/product-brief.md).

## Production backlog

See [`docs/production-backlog.md`](docs/production-backlog.md). The GitHub issue list is intentionally focused on the work a developer pod would need to turn this prototype into a production platform.

## AI usage

See [`docs/ai-interaction-log.md`](docs/ai-interaction-log.md) for how AI was used to explore the product scope, challenge design decisions, and refine the prototype.

## Design decisions

- **Local simulated provider:** avoids cloud credentials and keeps the prototype reproducible for a reviewer.
- **Explicit state machine:** makes happy-path and failure-path behavior observable and testable.
- **In-memory state:** appropriate for a short prototype; persistence is explicitly a production backlog item.
- **Synchronous workflow:** keeps the demo simple. A production implementation would use durable asynchronous jobs.
- **Deterministic failure flag:** lets a reviewer reproduce rollback without depending on timing or an external system.
- **Thin CLI:** demonstrates a developer-facing self-service surface without spending the timebox on UI polish.
