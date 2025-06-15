def test_should_login(client):
    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert "Welcome, john@simplylift.co" in response.data.decode()


def test_should_not_login(client):
    response = client.post("/showSummary", data={"email": "john@abc.co"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Invalid credentials." in response.data.decode()


def test_should_not_submit(client):
    response = client.post("/showSummary", data={"email": "123"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Invalid credentials." in response.data.decode()
