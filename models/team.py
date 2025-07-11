from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin
from .association import team_user_association

class Team(db.Model, TimestampMixin):
    __tablename__ = 'teams'

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String(50), nullable=False)
    description = Column(Text)

    members = relationship("User", secondary=team_user_association, back_populates="teams")
