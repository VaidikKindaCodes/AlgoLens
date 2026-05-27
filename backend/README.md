# AlgoLens Backend

FastAPI backend with access/refresh token authentication.

## Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Set a unique, random `SECRET_KEY` in `.env` before deploying. SQLite is used by
default; set `DATABASE_URL` to a PostgreSQL URL in production.

Interactive API documentation is available at `http://localhost:8000/docs`.

## Authentication API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register` | Create an account |
| `POST` | `/api/v1/auth/login` | Receive access and refresh tokens |
| `POST` | `/api/v1/auth/refresh` | Rotate a refresh token |
| `POST` | `/api/v1/auth/logout` | Revoke one refresh token |
| `POST` | `/api/v1/auth/logout-all` | Revoke all user sessions |
| `GET` | `/api/v1/auth/me` | Read the authenticated user |

Send access tokens as `Authorization: Bearer <token>`. Refresh tokens are
single-use: a successful refresh revokes the old token and returns a new pair.

## Tests

```powershell
pytest
```
