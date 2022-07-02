"""Test competitor routes."""


def test_get_competitors_for_tournament(client, user_token_headers, test_tournament, test_competitor_one):
    # The order matters here so keep this at the top. The test database
    # is persisted so even though the transaction is rolled back the id is not reused
    response = client.get(f'/competitors?tournament_id={test_tournament.id}', headers=user_token_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1


def test_create_competitor_success(client, user_token_headers, test_tournament):
    response = client.post(
        f'/competitors',
        headers=user_token_headers,
        json={'name': 'Lancelot', 'tournament_id': test_tournament.id},
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data['name'] == 'Lancelot'
    assert data['tournament_id'] == test_tournament.id
    assert 'id' in data


def test_tournament_does_not_exist(client, user_token_headers):
    response = client.post(
        '/competitors',
        headers=user_token_headers,
        json={'name': 'Lancelot', 'tournament_id': 2000000}
    )

    assert response.status_code == 404, response.text
    data = response.json()
    assert data == {'detail': 'Not found.'}


def test_unauthenticated_user(client, test_tournament):
    response = client.post(
        '/competitors',
        json={'name': 'Lancelot', 'tournament_id': test_tournament.id},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data == {'detail': 'Not authenticated'}


def test_unauthenticated_user_incorrect_token(client, test_tournament):
    response = client.post(
        '/competitors',
        headers={'Authorization': 'Bearer NotTheRightToken'},
        json={'name': 'Lancelot', 'tournament_id': test_tournament.id},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data == {'detail': 'Invalid authentication credentials'}


def test_update_wins_to_competitor(client, user_token_headers, test_tournament, test_competitor_one):
    assert test_competitor_one.losses == 0
    json_payload = {
        'id': test_competitor_one.id,
        'name': test_competitor_one.name,
        'tournament_id': test_tournament.id,
        'wins': 1,
        'losses': test_competitor_one.losses,
    }
    response = client.put(
        '/competitors',
        headers=user_token_headers,
        json=json_payload,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['wins'] == 1


def test_update_lose_to_competitor(client, user_token_headers, test_tournament, test_competitor_two):
    assert test_competitor_two.losses == 0
    json_payload = {
        'id': test_competitor_two.id,
        'name': test_competitor_two.name,
        'tournament_id': test_tournament.id,
        'wins': test_competitor_two.wins,
        'losses': 1,
    }
    response = client.put(
        '/competitors',
        headers=user_token_headers,
        json=json_payload,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['losses'] == 1
