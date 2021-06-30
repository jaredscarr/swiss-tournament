from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
import models
from database import get_db

router = APIRouter()


@router.get('/{tournament_id}/competitors/', response_model=List[schemas.Competitor])
def get_competitors(
    tournament_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament = crud.get_tournament_by_id(db=db, tournament_id=tournament_id)

    if not tournament or tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not found.")

    return crud.get_tournament_competitors(db=db, tournament_id=tournament_id)


@router.post('/{tournament_id}/competitors/', response_model=schemas.Competitor, status_code=status.HTTP_201_CREATED)
def create_competitor(
    tournament_id: int,
    competitor: schemas.CompetitorCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament = crud.get_tournament_by_id(db=db, tournament_id=tournament_id)

    if not tournament or tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not found.")

    return crud.create_competitor(db=db, name=competitor.name, tournament_id=tournament_id)


@router.put('/{tournament_id}/competitors/{competitor_id}/', response_model=schemas.Competitor)
def update_competitor(
    tournament_id: int,
    competitor_id: int,
    competitor: schemas.CompetitorUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament = crud.get_tournament_by_id(db=db, tournament_id=tournament_id)

    if not tournament or tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not found.")

    if not competitor:
        raise HTTPException(status_code=404, detail="Not found.")

    return crud.update_competitor(db=db, competitor_id=competitor_id, name=competitor.name, wins=competitor.wins, losses=competitor.losses)
