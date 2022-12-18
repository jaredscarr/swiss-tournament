from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session
from typing import List

import app.crud as crud
import app.schemas as schemas
import app.models as models
from app.database import get_db

router = APIRouter()


@router.get('/competitors', response_model=List[schemas.Competitor])
def get_competitors(
    tournament_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament = crud.get_tournament_by_id(db=db, tournament_id=tournament_id)

    if not tournament or tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail='Not found.')

    return crud.get_tournament_competitors(db=db, tournament_id=tournament_id)


@router.post('/competitors', response_model=schemas.Competitor, status_code=status.HTTP_201_CREATED)
def create_competitor(
    competitor: schemas.CompetitorCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament = crud.get_tournament_by_id(db=db, tournament_id=competitor.tournament_id)

    if not tournament or tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail='Not found.')
        
    return crud.create_competitor(db=db, name=competitor.name, tournament_id=competitor.tournament_id)


@router.put('/competitors', response_model=schemas.Competitor)
def update_competitor(
    competitor: schemas.CompetitorUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(crud.get_current_user)
):
    tournament = crud.get_tournament_by_id(db=db, tournament_id=competitor.tournament_id)

    if not tournament or tournament.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail='Not found.')

    competitor_exists = crud.get_competitor(db=db, competitor_id=competitor.id)

    if not competitor_exists:
        raise HTTPException(status_code=404, detail='Not found.')

    return crud.update_competitor(
        db=db,
        competitor_id=competitor.id,
        competitor_name=competitor.name,
        wins=competitor.wins,
        losses=competitor.losses
    )
