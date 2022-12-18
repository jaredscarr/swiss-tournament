from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# used in models.py
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print('------> ERROR in database.get_db: ')
        print(e)
    finally:
        db.close()
