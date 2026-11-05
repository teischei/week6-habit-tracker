# Week 6 Writeup

## Overview

This project is a small FastAPI habit tracker. I completed two tasks on separate branches and pull requests. I used Graphite Chat for one AI review and saved the review result in each PR discussion. Both PRs also have a passing Graphite AI Reviews check. I also ran CodeRabbit on both PRs, and its automatic bot reviews are visible on the pull requests.

| Pull request | Feature | Main commits |
| --- | --- | --- |
| [PR 4](https://github.com/teischei/week6-habit-tracker/pull/4) | validation | [implementation](https://github.com/teischei/week6-habit-tracker/commit/6776d43326ba6772fbab0d803358ae1b3369c27b) and [manual review fix](https://github.com/teischei/week6-habit-tracker/commit/a733bb029a44127dda982e5cdc460d490c60dfae) |
| [PR 5](https://github.com/teischei/week6-habit-tracker/pull/5) | weekly summary | [implementation](https://github.com/teischei/week6-habit-tracker/commit/e454577063f37c6b6df1a8176b6534576a4590b4) and [manual review fix](https://github.com/teischei/week6-habit-tracker/commit/e2f052fdbbc48c93d9a6955191e38698206ba50b) |

## Guardrails

I added Black, Ruff, pytest, and a GitHub Actions workflow. The commands are documented in `README.md` and `docs/guardrails.md`.

```bash
python -m black --check .
python -m ruff check .
python -m pytest -q
```

Black catches formatting differences and Ruff catches lint issues such as unused imports. Pytest checks the API behavior. I confirmed that a temporary test containing `assert False` made pytest return a failure result, then removed the temporary file before committing. GitHub Actions runs the same commands on every push and pull request.

## PR 4 validation

The validation feature rejects blank habit names and invalid check-in days. My manual review found that `date.fromisoformat` accepts the compact form `20260922`, even though the API says it uses `YYYY-MM-DD`. I added a round trip check with `isoformat()` and a test for the compact form before opening the PR.

Graphite returned ACCEPT and agreed that the final date validation rejects compact, week-date, and impossible-date values. It was better than my review at listing remaining test gaps. It suggested a positive test proving that a name with extra spaces is trimmed, plus more invalid date examples. CodeRabbit made the same main testing point in a more specific way. It suggested posting a padded habit name and checking the trimmed value in both the create response and the habit list. That was useful because it tied the missing test to the two API paths a user sees. My review was stronger at finding the exact behavior problem before the PR was opened and turning it into a small fix. Graphite also noticed that FastAPI can return a different 422 detail shape for request-model errors, but I kept the current response shape because changing it would be outside this small feature.

## PR 5 weekly summary

The weekly summary endpoint returns the number of check-ins from today through the previous six days. My manual review found that an unknown habit returned a successful count of zero. I fixed that by checking for the habit first and returning the same 404 response as the existing check-in route.

Graphite returned ACCEPT and confirmed that the seven-day range and 404 behavior were correct. It was better at identifying broader product decisions. It pointed out that duplicate same-day check-ins can make the count exceed seven, and that the API does not say whether it is counting check-ins or distinct days. It also suggested tests for zero check-ins and future-dated check-ins. CodeRabbit found another important dependency. Because this branch began from the guardrail branch, it did not include the check-in date validation from PR 4. CodeRabbit explained that noncanonical stored dates can be missed by the summary query. This was a stronger finding than my review because I focused on the new route and did not check how date input on a separate branch affects the SQL comparison. My review was more useful for the immediate API consistency issue because I found and fixed the missing 404 before the PR. Graphite was less useful for deciding whether duplicate check-ins should count as events or days, since that needs product direction rather than a code-only answer.

## What I learned

Guardrails and AI review help in different ways. Black, Ruff, and pytest give fast and repeatable feedback about formatting, linting, and behavior that already has tests. My own review caught concrete problems in each feature because I checked the route behavior line by line. Graphite and CodeRabbit were especially useful for finding missing edge cases and connections between separate changes. I would use AI review as a second reader and then verify its suggestions with the code, tests, and the intended product behavior.
