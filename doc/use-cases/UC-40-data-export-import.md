# UC-40 — Data Export / Import

Status: Later

- Actors: User
- Trigger: User requests export of their data, or imports from a backup.
- Preconditions: Authenticated user; storage budget/limits defined.
- Postconditions: User safely obtains or restores their data.

Main Flow
1. User requests export (JSON/CSV/ZIP). System prepares and notifies when ready.
2. User downloads via secure, time‑limited link.
3. Import flow: user uploads a valid export file; system validates and applies.

Alternate / Edge Cases
- Partial import conflicts → preview and selective merge.

Data
- Scope: evaluations, problems, actions, logs, settings.

Non‑Functional
- Privacy and security; encryption at rest and in transit.

Metrics
- Export requests; completion; restore success.

Open Questions
- GDPR/CCPA data access tooling.

