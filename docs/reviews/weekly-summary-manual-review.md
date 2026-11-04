# Weekly summary manual review

I reviewed the endpoint, SQL range, and test after the first implementation.

- The seven-day range includes today and the previous six days
- Check-ins from seven days ago and other habits are excluded by the query
- An unknown habit first returned a count of zero instead of matching the existing 404 behavior
- I added the habit lookup and a test for the 404 response
