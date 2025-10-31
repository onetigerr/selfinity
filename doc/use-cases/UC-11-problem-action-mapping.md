# UC-11 — Problem → Action Mapping

Status: MVP

- Actors: User
- Trigger: After evaluation, user lists concrete problems and assigns one actionable step for each.
- Preconditions: At least one evaluation exists.
- Postconditions: A set of problem/action pairs exists and can be tracked.

Main Flow
1. User selects a category and adds a problem statement.
2. User defines a single, specific action to address it.
3. System stores pair with status (planned, active, done) and priority.

Alternate / Edge Cases
- Multiple actions per problem (Phase‑2) → keep one primary action in MVP.
- Problem archived → keep history, exclude from active plans.

Data
- Entities: problems(id, user_id, category, text, status); actions(id, problem_id, text, cadence, status).
- API: CRUD for problems and actions.

Non‑Functional
- Encourage small, testable actions; keep UI friction low.

Metrics
- Number of active problems; actions completed per week.

Open Questions
- Cadence presets (daily/weekly) vs free‑form.

