# Use Cases

This folder contains structured, implementation-oriented use cases for Selfinity. Each use case follows a consistent template so it can be expanded and traced into requirements, API endpoints, UI, and tests.

Conventions
- IDs: `UC-XX` grouped by domain (01–09 auth/account, 10–19 evaluation & planning, 20–29 reminders/engagement, 30–39 analytics, 40–49 data/interop, 90–99 admin/ops).
- Status: MVP, Phase-2, Later.
- Links: each UC in its own file. Keep titles short, actionable.
 - Tests: each UC is annotated with coverage — Covered | Partial | Planned | None.

Index
- [UC-01 — Registration & Login](./UC-01-auth-registration-login.md) — Status: MVP — Tests: Covered (backend/tests/test_auth.py, backend/tests/test_auth_integration.py)
- [UC-02 — Password Reset](./UC-02-auth-password-reset.md) — Status: Phase-2 — Tests: None
- [UC-10 — Wheel Evaluation](./UC-10-evaluation-wheel.md) — Status: MVP — Tests: None
- [UC-11 — Problem → Action Mapping](./UC-11-problem-action-mapping.md) — Status: MVP — Tests: None
- [UC-12 — Habit Tracking](./UC-12-habit-tracking.md) — Status: Phase-2 — Tests: None
- [UC-13 — Weekly Review](./UC-13-weekly-review.md) — Status: Phase-2 — Tests: None
- [UC-20 — Reminders & Notifications](./UC-20-notifications-reminders.md) — Status: Later — Tests: None
- [UC-30 — Analytics & Insights](./UC-30-analytics-insights.md) — Status: Later — Tests: None
- [UC-40 — Data Export / Import](./UC-40-data-export-import.md) — Status: Later — Tests: None
- [UC-50 — Account & Privacy](./UC-50-account-settings-privacy.md) — Status: MVP — Tests: None
- [UC-90 — Admin & Ops](./UC-90-admin-ops.md) — Status: Later — Tests: None

Also see:
- Domain and roadmap: `doc/phase-1.md`, `doc/phase-2.md`.
- Backend API foundations: `backend/app`.
