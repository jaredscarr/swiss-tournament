from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tournaments = relationship('Tournament', back_populates='owner')


class Tournament(Base):

    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='tournaments')
    matches = relationship('Match')


class Competitor(Base):

    __tablename__ = 'competitors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))

    wins = relationship('Win')
    losses = relationship('Loss')


class Win(Base):

    __tablename__ = 'wins'

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    match_id = Column(Integer, ForeignKey('matches.id'))
    winner_id = Column(Integer, ForeignKey('competitors.id'))

    winner = relationship('Competitor', back_populates='wins')


class Loss(Base):

    __tablename__ = 'losses'

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    match_id = Column(Integer, ForeignKey('matches.id'))
    loser_id = Column(Integer, ForeignKey('competitors.id'))

    loser = relationship('Competitor', back_populates='losses')


class Match(Base):

    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    winner_id = Column(Integer, ForeignKey('competitors.id'))
    loser_id = Column(Integer, ForeignKey('competitors.id'))
