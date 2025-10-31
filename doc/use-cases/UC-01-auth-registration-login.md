# UC-01 — Registration & Login

Status: MVP

- Actors: Visitor, Auth Service, Database
- Trigger: Visitor submits email+password to create an account; later logs in.
- Preconditions: Email is not yet registered; password meets policy.
- Postconditions: User account exists; hashed password stored; JWT issued on login.

Main Flow
1. User submits registration form (email, password).
2. System validates format and uniqueness of email; validates password policy.
3. System hashes password and stores user record.
4. System returns 201 Created with minimal profile (no token).
5. User logs in with email+password.
6. System verifies password, issues access token (JWT) and returns it.

Alternate / Edge Cases
- Duplicate email → 409 Conflict.
- Wrong password → 401 Unauthorized.
- Weak password → 422 Unprocessable Entity.

Data
- Inputs: email (RFC 5322), password (>=8 chars; policy configurable).
- Persistence: users(id, email unique, password_hash, created_at).
- API: POST /auth/register, POST /auth/login, GET /auth/me.

Error Handling
- Sensitive errors are generic (no disclosure of existing accounts).
- Rate-limit login attempts to mitigate brute force.

Non‑Functional
- Password hashing: bcrypt via passlib; constant-time comparisons.
- Token: short-lived access token; optional refresh (later).

Metrics
- Sign‑ups per day; conversion to first login; failed logins.

Open Questions
- Email verification requirement? (Phase-2)
- Social sign‑ins? (Later)

Out of Scope
- Billing and paid features (see UC‑40).

