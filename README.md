# Starter — Habit Tracker

A tiny FastAPI + SQLite service for habits and daily check-ins. You'll add two features
on branches, open PRs, and run an AI reviewer.

## Setup
```bash
pip install -r requirements.txt
pytest                      # 3 tests should pass
uvicorn main:app --reload   # http://localhost:8000  (docs at /docs)
```

## Endpoints
- `POST /habits` `{ "name": ... }`
- `GET /habits`
- `POST /habits/{id}/checkin` `{ "day": "2026-09-22" }`
- `GET /habits/{id}/checkins`

## Files
- `main.py` — the app
- `test_main.py` — pytest suite
- `docs/TASKS.md` — the two features to implement

## Guardrails

Run these commands from the repository root before pushing a change.

```bash
black --check .
ruff check .
pytest -q
```

`black --check` catches formatting changes. `ruff check` catches common lint problems such as unused imports. `pytest -q` checks the API behavior and exits with a nonzero status when a test fails. GitHub Actions runs the same three commands for pushes and pull requests.
