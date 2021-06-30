from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
import models
from database import get_db

router = APIRouter()


@router.get('/tournaments/', response_model=List[schemas.Tournament])
def get_tournaments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    return crud.get_tournaments_by_owner_id(db=db, owner_id=current_user.id)


@router.post('/tournaments/', response_model=schemas.Tournament, status_code=status.HTTP_201_CREATED)
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
        raise HTTPException(status_code=400, detail="Tournament name already exists.")
    return crud.create_own_tournament(
        db=db,
        owner_id=current_user.id,
        name=tournament.name,
        description=tournament.description
    )
