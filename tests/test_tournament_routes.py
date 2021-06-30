"""Test tournament routes."""


def test_create_tournament_success(client, user_token_headers):
    response = client.post(
        "/tournaments/",
        headers=user_token_headers,
        json={"name": "Knights of the Round Table", "description": "Melee battle"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Knights of the Round Table"
    assert "id" in data


def test_create_tournament_already_exists(client, user_token_headers):
    client.post(
        "/tournaments/",
        headers=user_token_headers,
        json={"name": "Knights of the Round Table", "description": "Melee battle"},
    )
    response = client.post(
        "/tournaments/",
        headers=user_token_headers,
        json={"name": "Knights of the Round Table", "description": "Melee battle"},
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Tournament name already exists."


def test_unauthenticated_user(client):
    response = client.get("/tournaments/")
    assert response.status_code == 401, response.text
    data = response.json()
    assert data == {"detail": "Not authenticated"}


def test_authenticated_get_own_tournaments(client, user_token_headers):
    for tournament in ['T1', 'T2', 'T3']:
        client.post(
            "/tournaments/",
            headers=user_token_headers,
            json={"name": tournament},
        )
    response = client.get("/tournaments/", headers=user_token_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 3
