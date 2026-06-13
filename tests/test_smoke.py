def test_admin_login_page_loads(client):
    response = client.get("/admin/login/")

    assert response.status_code == 200
