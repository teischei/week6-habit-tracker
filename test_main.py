from datetime import date, timedelta

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_and_list_habit():
    r = client.post("/habits", json={"name": "Read 20 minutes"})
    assert r.status_code == 200
    hid = r.json()["id"]
    r2 = client.get("/habits")
    assert r2.status_code == 200
    assert any(h["id"] == hid for h in r2.json())


def test_checkin_flow():
    hid = client.post("/habits", json={"name": "Stretch"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 200
    r2 = client.get(f"/habits/{hid}/checkins")
    assert r2.json() == ["2026-09-22"]


def test_checkin_unknown_habit_404():
    r = client.post("/habits/99999/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 404


def test_weekly_summary_counts_only_the_last_seven_days():
    habit_id = client.post("/habits", json={"name": "Walk"}).json()["id"]
    other_habit_id = client.post("/habits", json={"name": "Draw"}).json()["id"]
    today = date.today()

    for day in (today, today - timedelta(days=1), today - timedelta(days=6)):
        client.post(f"/habits/{habit_id}/checkin", json={"day": day.isoformat()})
    client.post(
        f"/habits/{habit_id}/checkin",
        json={"day": (today - timedelta(days=7)).isoformat()},
    )
    client.post(f"/habits/{other_habit_id}/checkin", json={"day": today.isoformat()})

    response = client.get(f"/habits/{habit_id}/summary")

    assert response.status_code == 200
    assert response.json() == {"habit_id": habit_id, "checkins": 3}


def test_weekly_summary_unknown_habit_returns_404():
    response = client.get("/habits/99999/summary")

    assert response.status_code == 404
    assert response.json()["detail"] == "unknown habit"
