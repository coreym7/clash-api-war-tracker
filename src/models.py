from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import ForeignKeyConstraint


Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    tag = Column(String, primary_key=True)  # <- must be here
    name = Column(String)
    active = Column(Boolean, default=True)
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)

    participations = relationship('Participation', back_populates='player')

class War(Base):
    __tablename__ = 'wars'

    id = Column(Integer, primary_key=True)
    war_tag = Column(String, unique=True)
    clan_name = Column(String)
    clan_tag = Column(String)
    opponent_name = Column(String)
    opponent_tag = Column(String)
    team_size = Column(Integer)
    result = Column(String)
    state = Column(String)
    start_time = Column(String)
    end_time = Column(String)

    participations = relationship(
        'Participation',
        back_populates='war',
        cascade='all, delete-orphan'
    )


class Participation(Base):
    __tablename__ = 'participation'

    player_tag = Column(String, ForeignKey('players.tag'), primary_key=True)
    war_id = Column(Integer, ForeignKey('wars.id', ondelete='CASCADE'), primary_key=True)

    in_war = Column(Boolean)
    attacks_used = Column(Integer)
    total_stars = Column(Integer)
    new_stars = Column(Integer)
    average_percent = Column(Float)

    player = relationship('Player', back_populates='participations')
    war = relationship('War', back_populates='participations')

    attacks = relationship(
        'Attack',
        back_populates='participation',
        cascade='all, delete-orphan'
    )



class Attack(Base):
    __tablename__ = 'attacks'

    id = Column(Integer, primary_key=True)
    player_tag = Column(String, nullable=False)
    war_id = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['player_tag', 'war_id'],
            ['participation.player_tag', 'participation.war_id'],
            ondelete='CASCADE'
        ),
    )

    attack_number = Column(Integer)
    stars = Column(Integer)
    destruction_percent = Column(Float)
    target_tag = Column(String)
    target_position = Column(Integer)
    mirror_attack = Column(Boolean)
    new_stars = Column(Integer)
    mirror_delta = Column(Integer)
    attack_time = Column(Integer)  # stored in seconds

    participation = relationship(
        'Participation',
        back_populates='attacks',
        primaryjoin="and_(Attack.player_tag==Participation.player_tag, Attack.war_id==Participation.war_id)"
    )