def test_admin_login_page_loads(client):
    response = client.get("/admin/login/")

    assert response.status_code == 200


def test_liveness_probe_returns_ok(client):
    response = client.get("/health/live/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "django-api"


def test_readiness_probe_returns_ok(client, db):
    response = client.get("/health/ready/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["database"] == "available"
