# FDA Verify (Django) — Postgres setup

This project defaults to SQLite for local development but can use PostgreSQL when environment variables are provided.

Quick steps to run with Postgres on macOS (zsh):

1) Install and start Postgres (Homebrew):

```bash
brew install postgresql
brew services start postgresql
```

2) Create a database and user (example):

```bash
# open psql as current user
psql postgres

# inside psql:
CREATE USER fda_user WITH PASSWORD 'change_me';
CREATE DATABASE fda_db OWNER fda_user;
GRANT ALL PRIVILEGES ON DATABASE fda_db TO fda_user;
\q
```

3) Export environment variables for Django (zsh):

```bash
export POSTGRES_DB=fda_db
export POSTGRES_USER=fda_user
export POSTGRES_PASSWORD='change_me'
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

Or set a single `DATABASE_URL` instead:

```bash
export DATABASE_URL='postgres://fda_user:change_me@localhost:5432/fda_db'
```

4) Install Python dependencies (use a virtualenv):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5) Run migrations and start server:

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

6) Test the verify endpoint (curl example):

```bash
curl -X POST http://127.0.0.1:8000/api/verify/ \
  -H "Content-Type: application/json" \
  -d '{"identifier":"0851234567890"}'
```

Notes / Troubleshooting
- If `POSTGRES_DB` or `DATABASE_URL` are not set, the project will continue to use `db.sqlite3`.
- If Django fails to start after setting env vars, check Postgres is running and credentials are correct.
- Consider using `psycopg2-binary` (already in `requirements.txt`) for simpler local setup. For production, switch to `psycopg2`.
- For parsing `DATABASE_URL` robustly, you can add `dj-database-url` and update `core/settings.py` accordingly.

If you want, I can also:
- add a small management command to test DB connectivity,
- add `dj-database-url` support,
- or create a `.env.example` file for dev.
