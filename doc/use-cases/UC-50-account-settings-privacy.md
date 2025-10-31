# UC-50 — Account & Privacy

Status: MVP

- Actors: User
- Trigger: User manages account settings and privacy controls.
- Preconditions: Authenticated user.
- Postconditions: Preferences persisted; data usage transparent.

Main Flow
1. User updates profile (name, timezone), password, and session management.
2. User manages privacy: analytics opt‑in, data export, delete account.
3. System confirms critical actions (delete) and logs events.

Alternate / Edge Cases
- Require re‑auth for sensitive changes.

Data
- Profile, security events, privacy flags.

Non‑Functional
- Compliant defaults; clear consent flows.

Metrics
- Account changes frequency; deletion requests.

Open Questions
- Regional compliance (GDPR) scope.

