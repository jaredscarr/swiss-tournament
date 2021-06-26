"""Test user routes."""


def test_create_user_success(client):
    response = client.post(
        "/users/",
        json={"username": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["username"] == "deadpool@example.com"
    assert "id" in data


def test_create_user(client):
    client.post(
        "/users/",
        json={"username": "deadpool@example.com", "password": "chimichangas4life"},
    )
    second_response = client.post(
        "/users/",
        json={"username": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert second_response.status_code == 400, second_response.text
    data = second_response.json()
    assert data["detail"] == "Username already registered"


def test_authed_user(client, user_token_headers):
    response = client.get("/users/me", headers=user_token_headers)
    assert response.status_code == 200, response.text


def test_unauthenticated_user(client):
    response = client.get("/users/me")
    assert response.status_code == 401, response.text
    data = response.json()
    assert data == {"detail": "Not authenticated"}


def test_unauthenticated_user_invalid_credentials(client):
    response = client.get("/users/me", headers={"Authorization": "Bearer NotTheRightToken"})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data == {"detail": "Invalid authentication credentials"}
