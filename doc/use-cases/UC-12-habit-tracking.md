# UC-12 — Habit Tracking

Status: Phase-2

- Actors: User
- Trigger: User tracks execution of assigned actions as habits.
- Preconditions: At least one action exists (UC‑11).
- Postconditions: Execution logs stored; streaks and adherence are computed.

Main Flow
1. User sees daily/weekly checklist of active actions.
2. User marks an action as done or skipped with optional note.
3. System records a log entry with timestamp and outcome.
4. System updates streaks/adherence metrics.

Alternate / Edge Cases
- Backfill logs for past days (limited window).
- Skip with reason (illness, travel) excluded from penalty (optional).

Data
- Logs: action_logs(id, action_id, date, outcome{done,skipped}, note).
- Aggregates: adherence per action; streak counters.

Non‑Functional
- Quick interactions; mobile‑friendly.

Metrics
- Daily completion rate; average adherence; streak length.

Open Questions
- Reminders integration (UC‑20); calendar sync.

