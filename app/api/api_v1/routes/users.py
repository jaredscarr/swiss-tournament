from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

import app.crud as crud
import app.models as models
import app.schemas as schemas
from app.config import settings
from app.database import get_db
from app.dependencies import create_access_token


router = APIRouter()


@router.post('/token')
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=400,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/users', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=username)
    if db_user:
        raise HTTPException(status_code=400, detail='Username already registered')
    return crud.create_user(db=db, username=username, password=password)


@router.get('/users/me', response_model=schemas.User)
async def read_users_me(
    current_user: models.User = Depends(crud.get_current_active_user)
):
    return current_user
