from urllib.error import URLError
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from typing import Dict

from app.config import settings
import app.crud as crud
from app.database import Base, get_db
from app.main import app
import app.models as models


URL_PREFIX = '/api/v1/swiss-tournament'


def get_test_db_uri() -> str:
    return f'{settings.SQLALCHEMY_DATABASE_URI}_test'


@pytest.fixture()
def test_db():
    """
    Modify the db session to automatically roll back after each test.
    This is to avoid tests affecting the database state of other tests.
    """
    # Connect to the test database
    engine = create_engine(
        get_test_db_uri(),
    )

    connection = engine.connect()
    trans = connection.begin()

    # Run a parent transaction that can roll back all changes
    test_session_maker = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    test_session = test_session_maker()
    test_session.begin_nested()

    @event.listens_for(test_session, 'after_transaction_end')
    def restart_savepoint(s, transaction):
        if transaction.nested and not transaction._parent.nested:
            s.expire_all()
            s.begin_nested()

    yield test_session

    # Roll back the parent transaction after the test is complete
    test_session.close()
    trans.rollback()
    connection.close()


@pytest.fixture(scope='session', autouse=True)
def create_test_db():
    """Create a test database and use it for the whole test session."""

    test_db_url = get_test_db_uri()

    # Create the test database
    assert not database_exists(
        test_db_url
    ), 'Test database already exists. Aborting tests.'
    create_database(test_db_url)
    test_engine = create_engine(test_db_url)
    Base.metadata.create_all(test_engine)

    # Run the tests
    yield

    # Drop the test database
    drop_database(test_db_url)


@pytest.fixture()
def client(test_db):
    """Get a TestClient instance that reads/writes to the test database."""

    def get_test_db():
        yield test_db

    app.dependency_overrides[get_db] = get_test_db

    yield TestClient(app)


@pytest.fixture
def test_password() -> str:
    return 'securepassword'


def get_password_hash() -> str:
    """Password hashing can be expensive so a mock will be much faster."""
    return 'supersecrethash'


@pytest.fixture()
def test_user(test_db) -> models.User:
    """Make a test user in the database."""
    user = models.User(
        username="fake@email.com",
        hashed_password=get_password_hash(),
        is_active=True,
    )
    test_db.add(user)
    test_db.commit()
    yield user


@pytest.fixture()
def test_tournament(test_db, test_user) -> models.Tournament:
    """Create a test tournament in the database."""
    tournament = models.Tournament(
        name='Knights of the Round of the Table',
        owner_id=test_user.id,
    )
    test_db.add(tournament)
    test_db.commit()
    yield tournament


@pytest.fixture()
def test_competitor_one(test_db, test_tournament) -> models.Competitor:
    """Create a test competitor in the database."""
    competitor = models.Competitor(
        name='Percival',
        tournament_id=test_tournament.id,
        wins=0,
        losses=0,
    )
    test_db.add(competitor)
    test_db.commit()
    yield competitor


@pytest.fixture()
def test_competitor_two(test_db, test_tournament) -> models.Competitor:
    """Create a test competitor in the database."""
    competitor = models.Competitor(
        name='Merlin',
        tournament_id=test_tournament.id,
        wins=0,
        losses=0,
    )
    test_db.add(competitor)
    test_db.commit()
    yield competitor


@pytest.fixture()
def test_match(test_db, test_tournament, test_competitor_one, test_competitor_two) -> models.Match:
    """Create a match in the database."""
    match = models.Match(
        tournament_id=test_tournament.id,
        competitor_one=test_competitor_one.id,
        competitor_two=test_competitor_two.id,
        round=0,
        winner_id=None,
        loser_id=None,
    )
    test_db.add(match)
    test_db.commit()
    yield match
    

def verify_password_mock(first: str, second: str) -> bool:
    return True


@pytest.fixture()
def user_token_headers(
    client: TestClient, test_user, test_password, monkeypatch
) -> Dict[str, str]:
    monkeypatch.setattr(crud, 'verify_password', verify_password_mock)

    login_data = {
        'username': test_user.username,
        'password': test_password,
    }
    r = client.post(f'{URL_PREFIX}/token', data=login_data)
    tokens = r.json()
    a_token = tokens['access_token']
    headers = {'Authorization': f'Bearer {a_token}'}
    yield headers
