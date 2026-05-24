# Security Model

## Principles

- Isolate tenant data by organization and account boundary.
- Store raw incident payloads only when needed for replay and auditing.
- Mask or avoid personally identifiable information wherever possible.
- Require approval for risky, destructive, or high-blast-radius actions.
- Keep every AI recommendation explainable and auditable.

## Controls

- OAuth for Salesforce authorization
- JWT or session tokens for Zentom dashboard access
- Role-based access for admin, approver, and viewer personas
- Action allowlist for automation
- Policy engine decision records
- Replay records for model input, model output, policy output, and final action
- Audit logs for all user-approved and system-suggested actions

