from typing import List, Optional
from pydantic import BaseModel


class TournamentBase(BaseModel):
    name: str
    description: Optional[str] = None


class TournamentCreate(TournamentBase):
    pass


class Tournament(TournamentBase):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int

    class Config:
        orm_mode = True


class WinBase(BaseModel):
    winner_id: int


class WinCreate(WinBase):
    pass


class Win(WinBase):
    id: int
    tournament_id: int
    match_id: int
    winner_id: int

    class Config:
        orm_mode = True


class LossBase(BaseModel):
    loser_id: int


class LossCreate(LossBase):
    pass


class Loss(LossBase):
    id: int
    tournament_id: int
    match_id: int
    loser_id: int

    class Config:
        orm_mode = True


class MatchBase(BaseModel):
    tournament_id: int
    winner_id: int
    loser_id: int


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int
    tournament_id: int
    winner_id: int
    loser_id: int

    class Config:
        orm_mode = True


class CompetitorBase(BaseModel):
    name: str


class CompetitorCreate(CompetitorBase):
    pass


class Competitor(CompetitorBase):
    id: int
    name: str
    tournament_id: int
    wins: List[Win] = []
    losses: List[Loss] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    username: str
    is_active: bool
    tournaments: List[Tournament] = []

    class Config:
        orm_mode = True
