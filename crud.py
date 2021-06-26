from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from database import get_db
from dependencies import TokenData, oauth2_scheme
from config import settings
import models
import schemas


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# USER
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db=db, username=username)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid authentication credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
       
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db=db, username=token_data.username)

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Not found.')
    return current_user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# TOURNAMENT
def get_tournaments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tournament).offset(skip).limit(limit).all()


def get_tournament_by_id(db: Session, tournament_id: int):
    return db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()


def get_tournaments_by_owner_id(db: Session, owner_id: int):
    return db.query(models.Tournament).filter(models.Tournament.owner_id == owner_id).all()


def get_own_tournament_by_name(db: Session, owner_id: int, name: str):
    return db.query(models.Tournament).filter(models.Tournament.owner_id == owner_id).filter(models.Tournament.name == name).first()


def create_own_tournament(db: Session, owner_id: int, name: str, description: str):
    db_tournament = models.Tournament(name=name, description=description, owner_id=owner_id)
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


# COMPETITOR
def create_competitor(db: Session, name: str, tournament_id: int):
    db_competitor = models.Competitor(name=name, tournament_id=tournament_id)
    db.add(db_competitor)
    db.commit()
    db.refresh(db_competitor)
    return db_competitor


def get_tournament_competitors(db: Session, tournament_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Competitor)
        .filter(models.Competitor.tournament_id == tournament_id)
        .offset(skip)
        .limit(100)
        .all()
    )
