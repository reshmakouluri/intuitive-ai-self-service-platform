# Production Backlog

These are written as GitHub-ready issues. Priority reflects the smallest path from prototype to a safe internal platform.

## P0 — Durable workflow and persistence

**Problem:** In-memory state disappears when the process restarts and cannot safely coordinate concurrent deployments.

**Acceptance criteria:** Deployment state and event history survive restart; duplicate requests are handled idempotently; concurrent deployments have explicit locking/queue behavior.

## P0 — Authentication and RBAC

**Problem:** Any caller could currently create a deployment.

**Acceptance criteria:** SSO/OIDC authentication; roles for developer, platform operator, and administrator; authorization based on application ownership/environment.

## P0 — Real deployment provider

**Problem:** The prototype only simulates infrastructure and deployment.

**Acceptance criteria:** Deploy one supported target such as Kubernetes/ECS; capture provider operation IDs; surface provider failures without losing workflow state.

## P0 — Production health and rollback policy

**Problem:** A boolean simulated health check is insufficient for production.

**Acceptance criteria:** Configurable readiness/smoke checks; timeout and retry policy; rollback to last known-good version; explicit terminal state when rollback itself fails.

## P1 — Observability and SLOs

**Problem:** Operators need to understand platform health and deployment performance.

**Acceptance criteria:** Metrics for request count, deployment lead time, success/rollback rate and workflow duration; structured logs; traces; alerts tied to service objectives.

## P1 — Secrets and configuration

**Problem:** Real deployments require application configuration without exposing secrets.

**Acceptance criteria:** Integrate an approved secret manager; no secrets in request payloads or logs; documented rotation behavior.

## P1 — Service catalog integration

**Problem:** Developers should not have to type arbitrary application/environment values.

**Acceptance criteria:** Application ownership, permitted environments and deployment metadata come from a service catalog.

## P1 — Progressive delivery

**Problem:** A single health check after full rollout may expose users to a bad release.

**Acceptance criteria:** Support canary or staged rollout with automated health gates and rollback.

## P2 — Developer portal

**Problem:** CLI/API is enough for the prototype but not the most discoverable self-service experience.

**Acceptance criteria:** Simple portal showing eligible applications, deployment form, current status, events, and rollback outcome.

## P2 — Notifications and audit

**Acceptance criteria:** Optional Slack/email notifications; immutable audit trail containing actor, application, version, environment, timestamps and outcome.
