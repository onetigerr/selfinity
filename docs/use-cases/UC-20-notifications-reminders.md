# UC-20 — Reminders & Notifications

Status: Later

- Actors: User, Notification Service
- Trigger: Time-based or event-based reminders for reviews and actions.
- Preconditions: User enabled notifications and set preferences.
- Postconditions: User receives timely reminders across channels.

Main Flow
1. User configures reminder schedule (daily action reminders; weekly review).
2. System schedules jobs and delivers notifications (push/email/SMS).
3. User taps notification → deep link opens relevant view.

Alternate / Edge Cases
- Do‑not‑disturb windows; time zone changes; channel fallback.

Data
- Preferences: quiet hours, channels, cadence.
- Delivery logs for debugging and metrics.

Non‑Functional
- Reliable delivery; idempotent; respect privacy and user consent.

Metrics
- Open rates; completion after reminder; opt‑outs.

Open Questions
- Which channels first? (email, push); provider choice.

