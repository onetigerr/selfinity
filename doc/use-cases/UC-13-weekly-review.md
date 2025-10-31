# UC-13 — Weekly Review

Status: Phase-2

- Actors: User
- Trigger: At week’s end, user reviews progress, updates scores, and adjusts actions.
- Preconditions: Logs exist for the week; prior evaluation exists.
- Postconditions: New evaluation snapshot; actions updated or rotated.

Main Flow
1. System prompts user to review the week (Friday/Sunday reminder).
2. User views summary: adherence, highlights, blocking issues.
3. User re-evaluates 8 areas; system stores new snapshot.
4. User closes/completes actions; creates new ones for next week.

Alternate / Edge Cases
- No logs this week → show gentle nudge, allow quick review anyway.

Data
- Inputs: summary text (optional), updated scores, action changes.
- Persistence: evaluations, action statuses, weekly summary.

Non‑Functional
- Keep review under 5 minutes end-to-end.

Metrics
- Review completion rate; change in average scores; churn of actions.

Open Questions
- Templates for reflection prompts.

