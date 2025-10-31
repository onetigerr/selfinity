# UC-02 — Password Reset

Status: Phase-2

- Actors: User, Mailer, Auth Service
- Trigger: User requests password reset for their email.
- Preconditions: Account exists; email delivery configured.
- Postconditions: User can set a new password using a time-limited token.

Main Flow
1. User submits email to request password reset.
2. System generates a signed, time-limited token and sends email with link.
3. User opens link, provides new password.
4. System validates token, updates password hash, invalidates existing sessions.

Alternate / Edge Cases
- Email not found → return 200 (don’t disclose existence).
- Token expired/invalid → 400 with generic error; option to request again.

Data
- Inputs: email; new_password.
- Persistence: password_hash updated; token blacklist or version bump.
- API: POST /auth/reset/request, POST /auth/reset/confirm.

Non‑Functional
- Token TTL 15–60 minutes; single-use.
- Rate limiting per IP and per account.

Metrics
- Reset requests; completion rate; email bounces.

Open Questions
- UI for password reset; localization.

