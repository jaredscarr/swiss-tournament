# swiss-tournament

Swiss style tournament api built with FastAPI. If there are an odd number of competitors then one
match per round will have a bye. Tie-breaker involves a new tournament for those players
to compete again.

### Setup

- clone repo
- create virtual environment with python 3.9+
- pip install -r requirements.txt
- Install postgresql and create a database. User must have CREATE/UPDATE permissions
- create a .env file see FastApi docs for help
  - SECRET_KEY=secret_key
  - ALGORITHM=algorithm
  - TOKEN_URL=token
  - ACCESS_TOKEN_EXPIRE_MINUTES=minutes
  - CORS_ORIGINS=localhost, localhost:8080
  - POSTGRES_SERVER=server
  - POSTGRES_USER=user
  - POSTGRES_PASSWORD=password
  - POSTGRES_DB=database
  - SQLALCHEMY_DATABASE_URI=uri
- Alembic
  One way to do this quickly is to delete the migrations files in the alembic/verions/ and then run:
  - alembic init
  - run first migration
  - alembic revision -m "create account table"
  - alembic upgrade head

### Run Tests

Run `pytest` from root directory

### To start

Run `uvicorn app.main:app --reload` from root directory
visit {host}/docs to see endpoints

### Tools

- FastAPI
- postgresql
- sqlalchemy
- Alembic
- pytest
