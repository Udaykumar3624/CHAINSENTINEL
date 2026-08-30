# 🔐 ChainSentinel Authentication System Architecture (SIH26146)

This document details the production-ready JWT authentication architecture, password security, session handling, and database integration implemented in ChainSentinel.

---

## 📈 1. Authentication Flow Diagram

```
User (Browser)
   │
   ├── 1. Enters Credentials on /login
   │
   ▼
POST /api/v1/auth/login ──► FastAPI Auth Route (app.api.routes.auth)
   │                           │
   │                           ├── Query User by Username/Email
   │                           ├── Verify bcrypt Password Hash
   │                           └── Sign JWT Access Token (HS256)
   ▼
Returns Access Token + User Info
   │
   ├── Stores Token in localStorage ('chainsentinel_token')
   ├── Attaches 'Authorization: Bearer <token>' to all API calls
   │
   ▼
Protected APIs (/dashboard, /dataset, /alerts, /cases, /analyze)
   │
   ├── Verified by FastAPI get_current_user Dependency
   └── 401 Unauthorized Automatically Clears Session & Redirects to /login
```

---

## 🔑 2. Seeded Demo Investigator Credentials

For rapid SIH evaluation and local testing:

- **Username**: `demo.investigator`
- **Password**: `Investigator2026!`
- **Email**: `demo.investigator@chainsentinel.gov`
- **Role**: `LEAD_INVESTIGATOR`

*Note: Demo account configuration is read dynamically from environment variables (`DEMO_USERNAME`, `DEMO_PASSWORD`, `DEMO_EMAIL`) and seeded on startup if no investigator account exists in the database.*

---

## 🛡️ 3. Security Highlights

- **Bcrypt Password Hashing**: Passwords are hashed using salt rounds prior to persistence. Plaintext passwords are never logged, stored, or returned.
- **JWT Authorization**: Bearer token authentication with configurable expiration (`ACCESS_TOKEN_EXPIRE_MINUTES`).
- **CORS Hardening**: Origin list is explicitly validated against `CORS_ORIGINS` environment settings.
- **Zero Exposure**: Password hashes are excluded from `UserResponse` Pydantic models.
