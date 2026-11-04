# Validation manual review

I reviewed the route changes and tests before opening the pull request.

- Empty names were rejected and the stored name was trimmed
- The first date check accepted `20260922` even though the documented API format uses dashes
- I added a round trip date check and a test that rejects the compact date form
- The change stays limited to input validation and does not change the existing endpoints
