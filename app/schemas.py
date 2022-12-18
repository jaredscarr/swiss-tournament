from typing import List, Optional
from pydantic import BaseModel


class TournamentBase(BaseModel):
    name: str
    description: Optional[str] = None


class TournamentCreate(TournamentBase):
    name: str
    description: Optional[str] = None


class Tournament(TournamentBase):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    in_progress: Optional[int] = None
    in_progress_round: Optional[int] = None
    complete: Optional[bool] = False

    class Config:
        orm_mode = True


class TournamentUpdate(TournamentBase):
    id: int
    name: str
    description: Optional[str] = None
    in_progress: Optional[int] = None
    in_progress_round: Optional[int] = None
    complete: Optional[bool] = False


class MatchBase(BaseModel):
    tournament_id: int
    competitor_one: int
    competitor_two: Optional[int]
    round: int
    winner_id: Optional[int]
    loser_id: Optional[int]


class MatchCreate(MatchBase):
    tournament_id: int
    competitor_one: int
    competitor_two: Optional[int]
    round: int
    winner_id: Optional[int]
    loser_id: Optional[int]


class MatchUpdate(MatchBase):
    id: int
    tournament_id: int
    winner_id: Optional[int]
    loser_id: Optional[int]


class Match(MatchBase):
    id: int
    tournament_id: int
    competitor_one: int
    competitor_two: Optional[int]
    winner_id: Optional[int]
    loser_id: Optional[int]

    class Config:
        orm_mode = True


class CompetitorBase(BaseModel):
    name: str
    tournament_id: int


class CompetitorCreate(CompetitorBase):
    name: str
    tournament_id: int


class CompetitorUpdate(CompetitorBase):
    id: int
    name: str
    wins: Optional[int]
    losses: Optional[int]


class Competitor(CompetitorBase):
    id: int
    name: str
    tournament_id: int
    wins: Optional[int]
    losses: Optional[int]

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
