# Guardrails

The project uses three deterministic checks before a pull request is submitted.

```bash
python -m black --check .
python -m ruff check .
python -m pytest -q
```

Black checks formatting and Ruff checks lint problems. Pytest checks expected API behavior. A failing test returns a nonzero exit status, so the GitHub Actions workflow marks the build as failed.
