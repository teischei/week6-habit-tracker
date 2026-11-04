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


def test_rejects_blank_habit_name():
    r = client.post("/habits", json={"name": "   "})
    assert r.status_code == 422
    assert r.json()["detail"] == "name must not be blank"


def test_rejects_malformed_checkin_day():
    hid = client.post("/habits", json={"name": "Meditate"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": "not-a-date"})
    assert r.status_code == 422
    assert r.json()["detail"] == "day must use YYYY-MM-DD"


def test_rejects_checkin_day_without_dashes():
    hid = client.post("/habits", json={"name": "Journal"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": "20260922"})
    assert r.status_code == 422
    assert r.json()["detail"] == "day must use YYYY-MM-DD"
