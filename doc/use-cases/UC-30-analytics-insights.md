# UC-30 — Analytics & Insights

Status: Later

- Actors: User, Analytics Engine
- Trigger: User explores trends and insights from evaluations and logs.
- Preconditions: Sufficient historical data exists.
- Postconditions: User gains actionable insight to adjust plan.

Main Flow
1. User views trends per category across weeks/months.
2. System computes correlations (e.g., adherence vs score deltas).
3. User saves insight and adjusts focus areas/actions.

Alternate / Edge Cases
- Sparse data → show guidance to build habits first.

Data
- Aggregates from evaluations and action_logs; derived metrics.

Non‑Functional
- Performant queries; consider pre-aggregation.

Metrics
- Insight usage; improvements after insight adoption.

Open Questions
- Explainability of insights; export options.

