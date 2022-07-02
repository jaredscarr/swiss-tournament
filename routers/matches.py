from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
import models
from database import get_db

router = APIRouter()


@router.get('/matches', response_model=List[schemas.Match])
def get_matches(
    tournament_id: int,
    round:int = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament = crud.get_tournament_by_id(db=db, tournament_id=tournament_id)

    if not tournament or tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail='Not found.')

    return crud.get_matches(db=db, tournament_id=tournament_id, round=round)


@router.get('/matches/match_competitors', response_model=List[schemas.Match], status_code=status.HTTP_201_CREATED)
def match_competitors(
    tournament_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament = crud.get_tournament_by_id(db=db, tournament_id=tournament_id)

    if not tournament or tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail='Not found.')

    competitors = crud.get_tournament_competitors(db=db, tournament_id=tournament_id)

    if len(competitors) % 2 != 0:
        raise HTTPException(status_code=404, detail='Must have an even number of competitors to begin.')

    round = crud.get_current_round(db=db, tournament_id=tournament_id)
    matches = crud.get_matches(db=db, tournament_id=tournament_id, round=round)
    # if it's not the very fist round where there are no matches yet, thus no round to increment
    if (len(matches) > 0):
        round += 1

    return crud.get_round(
        db=db, tournament_id=tournament_id, competitors=competitors, round=round
    )


@router.post('/matches', response_model=schemas.Match, status_code=status.HTTP_201_CREATED)
def create_match(
    match: schemas.MatchCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament = crud.get_tournament_by_id(db=db, tournament_id=match.tournament_id)

    if not tournament or tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail='Not found.')

    if not match.competitor_one or not crud.get_competitor(db=db, competitor_id=match.competitor_one):
        raise HTTPException(status_code=404, detail='Not found.')

    if not match.competitor_two or not crud.get_competitor(db=db, competitor_id=match.competitor_two):
        raise HTTPException(status_code=404, detail='Not found.')
        
    return crud.create_match(
        db=db,
        tournament_id=tournament.id,
        competitor_one=match.competitor_one,
        competitor_two=match.competitor_two
    )


@router.put('/matches', response_model=schemas.Match)
def update_match(
    match: schemas.MatchUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament = crud.get_tournament_by_id(db=db, tournament_id=match.tournament_id)

    if not tournament or tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail='Not found.')

    match_exists = crud.get_match_by_id(db=db, tournament_id=match.tournament_id, match_id=match.id)

    if not match_exists:
        raise HTTPException(status_code=404, detail='Not found.')

    return crud.update_match(
        db=db,
        tournament_id=match.tournament_id,
        match_id=match.id,
        winner_id=match.winner_id
    )
