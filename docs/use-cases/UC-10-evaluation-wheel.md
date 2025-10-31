# UC-10 — Wheel Evaluation

Status: MVP

- Actors: User
- Trigger: User performs a new evaluation of eight life areas.
- Preconditions: Authenticated user; categories defined.
- Postconditions: A dated evaluation with 8 scores is stored.

Main Flow
1. User opens evaluation view with 8 categories (0–100 scale).
2. User enters scores; system validates range and type.
3. User submits; system stores evaluation snapshot with timestamp.
4. System optionally suggests areas to focus (lowest deltas).

Alternate / Edge Cases
- Partial input → prompt to complete; allow draft save (Phase‑2).
- Re‑evaluation within same week → mark as additional snapshot.

Data
- Inputs: scores[health, spirituality, friends, family, work_income, home, fun, rest].
- Persistence: evaluations(user_id, timestamp, scores json/columns).
- API: POST /evaluations, GET /evaluations/latest, GET /evaluations/:id.

Non‑Functional
- Keep write path fast; avoid complex transactions.

Metrics
- Completion rate per week; average scores; variance.

Open Questions
- Allow custom categories? If so, migration and UI impact.

