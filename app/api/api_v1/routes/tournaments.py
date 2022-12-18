from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session
from typing import List

import app.crud as crud
import app.schemas as schemas
import app.models as models
from app.database import get_db


router = APIRouter()


@router.get('/tournaments', response_model=List[schemas.Tournament])
def get_tournaments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    return crud.get_tournaments_by_owner_id(db=db, owner_id=current_user.id)


@router.post('/tournaments', response_model=schemas.Tournament, status_code=status.HTTP_201_CREATED)
def create_own_tournament(
    tournament: schemas.TournamentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament_exists = crud.get_own_tournament_by_name(
        db=db,
        owner_id=current_user.id,
        name=tournament.name
    )

    if tournament_exists:
        raise HTTPException(status_code=400, detail='Tournament name already exists.')
    return crud.create_own_tournament(
        db=db,
        owner_id=current_user.id,
        name=tournament.name,
        description=tournament.description
    )


@router.put('/tournaments', response_model=schemas.Tournament)
def update_tournament(
    tournament: schemas.TournamentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    db_tournament = crud.get_tournament_by_id(db=db, tournament_id=tournament.id)

    if not db_tournament or db_tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail='Not found.')

    return crud.update_tournament(
        db=db,
        id=tournament.id,
        name=tournament.name,
        description=tournament.description,
        in_progress=tournament.in_progress,
        in_progress_round=tournament.in_progress_round,
        complete=tournament.complete
    )
