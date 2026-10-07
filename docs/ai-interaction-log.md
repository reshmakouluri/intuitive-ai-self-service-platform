# AI Interaction Log

AI was used as a design and implementation copilot. The candidate retained responsibility for the product decision, scope, technical trade-offs, review of generated code, and final submission.

## Session summary

### Prompt / direction 1 — Choose a focused platform problem

I asked for a small self-service platform problem that would demonstrate platform/product judgment and an end-to-end workflow within a 2–4 hour assessment timebox.

**AI contribution:** Suggested a self-service application deployment platform with a deterministic success path and a failure/rollback path.

**Candidate decision:** Selected deployment because it maps directly to my experience with CI/CD, cloud infrastructure, production releases, migration/cutover, validation, rollback, and SRE practices.

### Prompt / direction 2 — Keep the prototype runnable locally

I asked how to demonstrate provisioning and deployment without spending the assessment timebox on real AWS resources or credentials.

**AI contribution:** Proposed a local simulated provider behind a small interface. The API and workflow behave like a real platform while provider operations are deterministic and local.

**Candidate decision:** Accepted this approach because the assessment evaluates product judgment and workflow handling rather than cloud-account setup.

### Prompt / direction 3 — Make failure behavior explicit

I asked for a failure mode that a reviewer could reproduce reliably.

**AI contribution:** Proposed a `simulate_failure` request option that causes the health check to fail and drives `FAILED -> ROLLING_BACK -> ROLLED_BACK`.

**Candidate decision:** Kept deterministic failure simulation so the reviewer can verify recovery in one command.

### Prompt / direction 4 — Define production handoff

I asked what a developer pod would need after the prototype.

**AI contribution:** Identified durable workflow state, authentication/RBAC, real provider integration, health/rollback policy, observability, secrets, service catalog integration, progressive delivery, notifications and audit.

**Candidate decision:** Converted these into a prioritized production backlog rather than implementing them in the prototype.

## Course corrections

- Avoided real AWS provisioning to protect the timebox and eliminate credentials/environment dependencies.
- Avoided a full React UI because the CLI provides a thinner, more testable self-service surface for this prototype.
- Kept state transitions explicit rather than hiding workflow behavior in framework code.
- Added event history so a reviewer can see what happened during both success and rollback.

## Human review checklist

Before submission, I reviewed the generated implementation for:

- API request validation
- terminal states and failure transitions
- rollback behavior
- HTTP error handling
- reproducible local setup
- test coverage for success, failure and invalid environment
- consistency between the product brief and implementation
- production backlog boundaries
