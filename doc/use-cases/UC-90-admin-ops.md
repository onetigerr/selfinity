# UC-90 — Admin & Ops

Status: Later

- Actors: Operator/Admin, Monitoring
- Trigger: Operational tasks: health, migrations, access management.
- Preconditions: Proper roles and tooling available.
- Postconditions: System remains healthy and auditable.

Main Flow
1. Health checks and readiness probes (HTTP).
2. Apply DB migrations; rollback plan documented.
3. Manage flagged content or abuse (if any social features later).

Data
- Operational logs; audit trail for admin actions.

Non‑Functional
- Least privilege; infrastructure as code; backups.

Open Questions
- Incident response runbooks; SLO/SLIs.

