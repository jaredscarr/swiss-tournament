from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

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
def get_tournament_competitors(db: Session, tournament_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Competitor)
        .filter(models.Competitor.tournament_id == tournament_id)
        .order_by(models.Competitor.wins.desc())
        .offset(skip)
        .limit(100)
        .all()
    )


def get_competitor(db: Session, competitor_id: int):
    return db.query(models.Competitor).filter(models.Competitor.id == competitor_id).first()


def create_competitor(db: Session, name: str, tournament_id: int):
    db_competitor = models.Competitor(name=name, tournament_id=tournament_id, wins=0, losses=0)
    db.add(db_competitor)
    db.commit()
    db.refresh(db_competitor)
    return db_competitor


def update_competitor(
    db: Session,
    competitor_id: int,
    competitor_name: str,
    wins: int,
    losses: int
):
    competitor = get_competitor(db=db, competitor_id=competitor_id)
    competitor.name = competitor_name
    competitor.wins = wins
    competitor.losses = losses
    db.add(competitor)
    db.commit()
    db.refresh(competitor)
    return competitor


# Match
def get_matches(db: Session, tournament_id: int, round: int):
    if (round):
        return (
            db.query(models.Match)
            .filter(
                # using "==" instead of "is" to work with sqlalchemy
                models.Match.tournament_id == tournament_id,
                models.Match.round == round
            )
            .all()
        )
    else:
        return (
            db.query(models.Match)
            .filter(
                # using "==" instead of "is" to work with sqlalchemy
                models.Match.tournament_id == tournament_id,
            )
            .all()
        )


def get_match_by_id(db: Session, tournament_id: int, match_id: int):
    return (
        db.query(models.Match)
        .filter(
            models.Match.tournament_id == tournament_id,
            models.Match.id == match_id
        )
        .first()
    )

#TODO: remove tournament id
def get_matches_by_competitor(db: Session, tournament_id: int, competitor_id: int):
    return (
        db.query(models.Match)
        .filter(
            (models.Match.competitor_one == competitor_id) |
            (models.Match.competitor_two == competitor_id)
        )
        .all()
    )


def create_match(
    db: Session,
    tournament_id: int,
    competitor_one: int,
    competitor_two: int,
    round: int = 0
):
    comp_one = get_competitor(db=db, competitor_id=competitor_one)
    comp_two = get_competitor(db=db, competitor_id=competitor_two)
    db_match = models.Match(
        tournament_id=tournament_id,
        competitor_one=competitor_one,
        competitor_two=competitor_two,
        round=round
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match
    

def update_match(db: Session, tournament_id: int, match_id: int, winner_id: int):
    match = get_match_by_id(db=db, tournament_id=tournament_id, match_id=match_id)
    if(not match):
        return
    if (match.competitor_one == winner_id):
        winner = get_competitor(db=db, competitor_id=match.competitor_one)
        loser = get_competitor(db=db, competitor_id=match.competitor_two)
    else:
        winner = get_competitor(db=db, competitor_id=match.competitor_two)
        loser = get_competitor(db=db, competitor_id=match.competitor_one)
    wins = winner.wins + 1
    losses = loser.losses + 1
    update_competitor(
        db=db,
        competitor_id=winner.id,
        competitor_name=winner.name,
        wins=wins,
        losses=winner.losses
    )
    update_competitor(
        db=db,
        competitor_id=loser.id,
        competitor_name=loser.name,
        wins=loser.wins,
        losses=losses)
    match.winner_id = winner.id
    match.loser_id = loser.id
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def get_current_round(db: Session, tournament_id: int):
    max_round_match = (
        db.query(models.Match)
        .filter(
            models.Match.tournament_id == tournament_id,
        )
        .order_by(models.Match.round.desc())
        .first()
    )
    return max_round_match.round if max_round_match else 0


def get_round(db: Session, tournament_id: int, competitors: list, round: int):
    # track each player that has been matched for this round so they are not matched again
    matched_players_for_round = []
    for competitor in competitors:
        if competitor.id not in matched_players_for_round:
            print(f'    Competitor ID: {competitor.id}')
            matched_players_for_round.append(competitor.id)
            other_comps_ids = [
                c.id for c in db.query(models.Competitor).filter(
                    (models.Competitor.id != competitor.id)
                )
                .order_by(models.Competitor.wins.desc())
                .all()
            ]
            matched = None
            if (round == 0): # This is the first round they haven't played anyone
                round = 0
                # match to a competitor that has not been matched in this round already
                if len(other_comps_ids) > 0:
                    for c in other_comps_ids:
                        if c not in matched_players_for_round:
                            matched = c
                if (not matched):
                    return get_matches(db=db, tournament_id=tournament_id, round=round)
            else:
                played_ids = []
                competitor_matches = get_matches_by_competitor(
                    db=db,
                    tournament_id=tournament_id,
                    competitor_id=competitor.id
                )
                for match in competitor_matches:
                    if (match.competitor_one == competitor.id):
                        played_ids.append(match.competitor_two)
                    else:
                        played_ids.append(match.competitor_one)
                print(f'    Played: {[player for player in played_ids]}')
                available_matches = [c for c in other_comps_ids if c not in played_ids and c not in matched_players_for_round]
                print(f'    Available: {available_matches}')
                # take the first available (prev sorted in above query)
                if (len(available_matches) == 0): # they have been matched to everyone
                    return get_matches(db=db, tournament_id=tournament_id, round=round)
                matched = available_matches[0]
            matched_players_for_round.append(matched)
            create_match(
                db=db,
                tournament_id=tournament_id,
                competitor_one=competitor.id,
                competitor_two=matched,
                round=round
            )
    return get_matches(db=db, tournament_id=tournament_id, round=round)
