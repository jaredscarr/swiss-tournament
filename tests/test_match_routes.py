"""Test match routes."""


URL_PREFIX = '/api/v1/swiss-tournament'


def test_get_matches_for_tournament_no_matches(client, user_token_headers, test_tournament):
    # The order matters here so keep this at the top. The test database
    # is persisted so even though the transaction is rolled back the id is not reused
    response = client.get(
        f'{URL_PREFIX}/matches?tournament_id={test_tournament.id}',
        headers=user_token_headers
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 0, len(data)


def test_create_match_success(
    client, user_token_headers, test_tournament, test_competitor_one, test_competitor_two
):
    json_data = {
        'tournament_id': test_tournament.id,
        'competitor_one': test_competitor_one.id,
        'competitor_two': test_competitor_two.id,
        'round': 0,
        'winner_id': None,
        'losser_id': None
    }
    response = client.post(
        f'{URL_PREFIX}/matches',
        headers=user_token_headers,
        json=json_data
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['competitor_one'] == test_competitor_one.id
    assert data['competitor_two'] == test_competitor_two.id
    assert data['tournament_id'] == test_tournament.id
    assert 'id' in data
    response = client.get(
        f'{URL_PREFIX}/matches?tournament_id={test_tournament.id}',
        headers=user_token_headers
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1, len(data)


def test_tournament_does_not_exist(
    client, user_token_headers, test_competitor_one, test_competitor_two
):
    json_data = {
        'tournament_id': 2000,
        'competitor_one': test_competitor_one.id,
        'competitor_two': test_competitor_two.id,
        'round': 0,
        'winner_id': None,
        'losser_id': None
    }
    response = client.post(
        f'{URL_PREFIX}/matches',
        headers=user_token_headers,
        json=json_data
    )

    assert response.status_code == 404, response.text
    data = response.json()
    assert data == {'detail': 'Not found.'}


def test_unauthenticated_user(
    client, test_competitor_one, test_competitor_two
):
    json_data = {
        'tournament_id': 2000,
        'competitor_one': test_competitor_one.id,
        'competitor_two': test_competitor_two.id,
        'round': 0,
        'winner_id': None,
        'losser_id': None
    }
    response = client.post(
        f'{URL_PREFIX}/matches',
        json=json_data
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data == {'detail': 'Not authenticated'}


def test_invalid_creds(
    client, test_competitor_one, test_competitor_two
):
    json_data = {
        'tournament_id': 2000,
        'competitor_one': test_competitor_one.id,
        'competitor_two': test_competitor_two.id,
        'round': 0,
        'winner_id': None,
        'losser_id': None
    }
    response = client.post(
        f'{URL_PREFIX}/matches',
        headers={'Authorization': 'Bearer Wrong Code'},
        json=json_data
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data == {'detail': 'Invalid authentication credentials'}


def test_update_match_with_winner_success(
    client, user_token_headers, test_tournament, test_match, test_competitor_one, test_competitor_two
):
    assert test_competitor_one.wins == 0
    assert test_match.winner_id == None
    json_data = {
        'id': test_match.id,
        'tournament_id': test_tournament.id,
        'competitor_one': test_competitor_one.id,
        'competitor_two': test_competitor_two.id,
        'round': 0,
        'winner_id': test_competitor_one.id,
        'losser_id': test_competitor_two.id
    }
    response = client.put(
        f'{URL_PREFIX}/matches',
        headers=user_token_headers,
        json=json_data
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['winner_id'] == test_competitor_one.id
    response = client.get(
        f'{URL_PREFIX}/competitors?tournament_id={test_tournament.id}',
        headers=user_token_headers
    )
    assert response.status_code == 200, response.text
    data = response.json()
    for c in data:
        if c['id'] == test_competitor_one.id:
            assert c['wins'] == 1
            assert c['losses'] == 0
        if c['id'] == test_competitor_two.id:
            assert c['wins'] == 0
            assert c['losses'] == 1
    


def test_update_match_tournament_not_found(
    client, user_token_headers, test_match, test_competitor_one, test_competitor_two
):
    json_data = {
        'id': test_match.id,
        'tournament_id': 2000,
        'competitor_one': test_competitor_one.id,
        'competitor_two': test_competitor_two.id,
        'round': 0,
        'winner_id': None,
        'losser_id': None
    }
    response = client.put(
        f'{URL_PREFIX}/matches',
        headers=user_token_headers,
        json=json_data
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data == {'detail': 'Not found.'}


def test_updated_match_match_not_found(
    client, user_token_headers, test_tournament, test_competitor_one, test_competitor_two
):
    json_data = {
        'id': 600,
        'tournament_id': test_tournament.id,
        'competitor_one': test_competitor_one.id,
        'competitor_two': test_competitor_two.id,
        'round': 0,
        'winner_id': None,
        'losser_id': None
    }
    response = client.put(
        f'{URL_PREFIX}/matches',
        headers=user_token_headers,
        json=json_data
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data == {'detail': 'Not found.'}


def test_create_and_get_success(
    client, user_token_headers, test_tournament, test_competitor_one, test_competitor_two
):
    json_data = {
        'tournament_id': test_tournament.id,
        'competitor_one': test_competitor_one.id,
        'competitor_two': test_competitor_two.id,
        'round': 0,
        'winner_id': None,
        'losser_id': None
    }
    response = client.post(
        f'{URL_PREFIX}/matches',
        headers=user_token_headers,
        json=json_data
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert 'id' in data.keys()
    match_id = data['id']
    response = client.get(
        f'{URL_PREFIX}/matches?tournament_id={test_tournament.id}',
        headers=user_token_headers
    )
    data = response.json()
    assert data[0]['id'] == match_id


def test_create_match_competitor_one_not_found(
    client, user_token_headers, test_tournament, test_competitor_two
):
    json_data = {
        'tournament_id': test_tournament.id,
        'competitor_one': 46768,
        'competitor_two': test_competitor_two.id,
        'round': 0,
        'winner_id': None,
        'losser_id': None
    }
    response = client.post(
        f'{URL_PREFIX}/matches',
        headers=user_token_headers,
        json=json_data
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data == {'detail': 'Not found.'}


def test_create_match_competitor_two_not_found(
    client, user_token_headers, test_tournament, test_competitor_one
):
    json_data = {
        'tournament_id': test_tournament.id,
        'competitor_one': test_competitor_one.id,
        'competitor_two': 46768,
        'round': 0,
        'winner_id': None,
        'losser_id': None
    }
    response = client.post(
        f'{URL_PREFIX}/matches',
        headers=user_token_headers,
        json=json_data
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data == {'detail': 'Not found.'}


def test_match_competitors_even_success(client, user_token_headers, test_tournament):
    team_names = ['pirates', 'jaguars', 'falcons', 'arrows', 'crushers', 'smashers']
    for name in team_names:
        response = client.post(
            f'{URL_PREFIX}/competitors',
            headers=user_token_headers,
            json={'name': name, 'tournament_id': test_tournament.id},
        )
        assert response.status_code == 201, response.text
    response = client.get(
        f'{URL_PREFIX}/competitors?tournament_id={test_tournament.id}',
        headers=user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 6

    round = 0
    while len(data) != 0:
        response = client.get(
            f'{URL_PREFIX}/matches/match_competitors?tournament_id={test_tournament.id}&round={round}',
            headers=user_token_headers
        )
        assert response.status_code == 200
        data = response.json()
        # Assert that each id is matched only one time PER ROUND
        competitor_ids = []
        for match in data:
            assert match['round'] == round
            assert match['competitor_one'] != match['competitor_two']
            if match['competitor_one']:
                competitor_ids.append(match['competitor_one'])
            if match['competitor_two']:
                competitor_ids.append(match['competitor_two'])
        assert len(set(competitor_ids)) == len(competitor_ids)
        round += 1

        
def test_match_competitors_uneven_success(client, user_token_headers, test_tournament):
    team_names = ['pirates', 'jaguars', 'falcons', 'crushers', 'smashers']
    for name in team_names:
        response = client.post(
            f'{URL_PREFIX}/competitors',
            headers=user_token_headers,
            json={'name': name, 'tournament_id': test_tournament.id},
        )
        assert response.status_code == 201, response.text
    response = client.get(
        f'{URL_PREFIX}/competitors?tournament_id={test_tournament.id}',
        headers=user_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

    round = 0
    while len(data) != 0:
        response = client.get(
            f'{URL_PREFIX}/matches/match_competitors?tournament_id={test_tournament.id}&round={round}',
            headers=user_token_headers
        )
        assert response.status_code == 200
        data = response.json()
        # Assert that each id is matched only one time PER ROUND
        competitor_ids = []
        for match in data:
            assert match['round'] == round
            assert match['competitor_one'] != match['competitor_two']
            if match['competitor_one']:
                competitor_ids.append(match['competitor_one'])
            if match['competitor_two']:
                competitor_ids.append(match['competitor_two'])
        assert len(set(competitor_ids)) == len(competitor_ids)
        round += 1
