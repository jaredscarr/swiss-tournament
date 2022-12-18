"""Test tournament routes."""

URL_PREFIX = '/api/v1/swiss-tournament'


def test_create_tournament_success(client, user_token_headers):
    response = client.post(
        f'{URL_PREFIX}/tournaments',
        headers=user_token_headers,
        json={'name': 'Knights of the Round Table', 'description': 'Melee battle'},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['name'] == 'Knights of the Round Table'
    assert 'id' in data


def test_create_tournament_already_exists(client, user_token_headers):
    client.post(
        f'{URL_PREFIX}/tournaments',
        headers=user_token_headers,
        json={'name': 'Knights of the Round Table', 'description': 'Melee battle'},
    )
    response = client.post(
        f'{URL_PREFIX}/tournaments',
        headers=user_token_headers,
        json={'name': 'Knights of the Round Table', 'description': 'Melee battle'},
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Tournament name already exists.'


def test_unauthenticated_user(client):
    response = client.get(f'{URL_PREFIX}/tournaments')
    assert response.status_code == 401, response.text
    data = response.json()
    assert data == {'detail': 'Not authenticated'}


def test_authenticated_get_own_tournaments(client, user_token_headers):
    for tournament in ['T1', 'T2', 'T3']:
        client.post(
            f'{URL_PREFIX}/tournaments',
            headers=user_token_headers,
            json={'name': tournament},
        )
    response = client.get(f'{URL_PREFIX}/tournaments', headers=user_token_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 3


def test_update_tournament_success(client, user_token_headers):
    post_response = client.post(
        f'{URL_PREFIX}/tournaments',
        headers=user_token_headers,
        json={'name': 'test-tournament-update'},
    )
    
    assert post_response.status_code == 201, post_response.text
    data = post_response.json()
    assert data['complete'] == None
    tournament = data
    json_body = {
        'id': tournament['id'],
        'name': tournament['name'],
        'description': tournament['description'],
        'in_progress': tournament['in_progress'],
        'in_progress_round': tournament['in_progress_round'],
        'complete': True
    }
    put_response = client.put(
        f'{URL_PREFIX}/tournaments',
        headers=user_token_headers,
        json=json_body,
    )
    assert put_response.status_code == 200, put_response.text
    data = put_response.json()
    assert data['complete'] == True


def test_update_tournament_success_with_null_value(client, user_token_headers):
    post_response = client.post(
        f'{URL_PREFIX}/tournaments',
        headers=user_token_headers,
        json={'name': 'test-tournament-update'},
    )
    
    assert post_response.status_code == 201, post_response.text
    data = post_response.json()
    assert data['in_progress'] == None
    tournament = data
    json_body = {
        'id': tournament['id'],
        'name': tournament['name'],
        'description': tournament['description'],
        'in_progress': 67,
        'in_progress_round': 1,
        'complete': None
    }
    put_response = client.put(
        f'{URL_PREFIX}/tournaments',
        headers=user_token_headers,
        json=json_body,
    )
    assert put_response.status_code == 200, put_response.text
    data = put_response.json()
    assert data['in_progress'] == 67
    assert data['in_progress_round'] == 1
    json_body = {
        'id': tournament['id'],
        'name': tournament['name'],
        'description': tournament['description'],
        'in_progress': None,
        'in_progress_round': None,
        'complete': None
    }
  
    put_response_two = client.put(
        f'{URL_PREFIX}/tournaments',
        headers=user_token_headers,
        json=json_body,
    )
    assert put_response_two.status_code == 200, put_response_two.text
    data = put_response_two.json()
    assert data['in_progress'] == None
    assert data['in_progress_round'] == None
