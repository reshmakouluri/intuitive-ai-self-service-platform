# Product Brief & Capability Map

## User

Application developers who need to deploy a service to a non-production environment without opening a DevOps ticket or coordinating manually with an infrastructure team.

## Problem

Routine deployments can create avoidable queue time when developers depend on DevOps engineers for repeatable provisioning, deployment, validation, and rollback steps. This consumes platform capacity and makes deployment lead time dependent on human availability.

## Solution

Provide a self-service deployment API and thin CLI. A developer submits an application, version, and target environment. The platform owns the workflow: validate, provision, deploy, health-check, and either complete or rollback.

The prototype deliberately simulates infrastructure operations so the reviewer can run it locally without cloud credentials.

## Product hypothesis

If eligible staging deployments can be completed through a consistent self-service workflow, then deployment lead time and DevOps coordination effort should decrease without reducing operational safety.

## Success metric

Primary: median deployment lead time from accepted request to terminal state.

Secondary: percentage of eligible staging deployments completed through self-service without DevOps intervention.

A useful future guardrail metric is rollback rate by application/version.

## Capability map

| Capability | Prototype | Production pod would add |
|---|---|---|
| Deployment API | FastAPI endpoint | API versioning, gateway, rate limits |
| Request validation | Pydantic | Policy engine, service catalog integration |
| Workflow orchestration | In-process state machine | Durable async workflow engine/queue |
| Environment provisioning | Local simulator | Kubernetes/ECS/cloud provider integration |
| Deployment | Local simulator | Real artifact/image deployment |
| Health validation | Deterministic check | Real readiness, smoke and synthetic checks |
| Failure handling | Explicit failure state | Failure classification and recovery policies |
| Rollback | Simulated rollback | Provider-native rollback/version restoration |
| Deployment history | In-memory events | Persistent event/audit store |
| Developer surface | CLI + API docs | Web portal, service catalog integration |
| Identity/access | Not included | SSO, RBAC, service ownership |
| Secrets | Not included | Secret manager integration |
| Observability | Event history | Metrics, traces, logs, SLOs and alerts |

## Explicitly out of scope

- Real cloud infrastructure creation
- Production authentication/authorization
- Persistent database
- Multi-region deployment
- Progressive delivery/canary releases
- Secrets management
- Full web UI

These are intentionally left for the production pod because the assessment values a narrow, demonstrable end-to-end workflow over breadth.

## What I would hand to the developer pod

The pod receives the product brief, capability map, API contract, state model, working prototype, tests, and production backlog. The first production increment should replace the local provider with one real deployment target while adding durable workflow state and identity controls.
