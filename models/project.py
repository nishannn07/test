from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin
from .association import user_project_association

class Project(db.Model, TimestampMixin):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    project_name = Column(String(150), nullable=False)
    project_key = Column(String(10), unique=True, nullable=False)
    project_link = Column(String(255))
    description = Column(Text)
    status = Column(String(50), default="active")
    
    users = relationship("User", secondary=user_project_association, back_populates="projects")
    comments = relationship("Comment", back_populates="project")
    tasks = relationship("Task", back_populates="project")
    dashboards = relationship("Dashboard", back_populates="project")
    activities = relationship("ActivityLog", back_populates="project")
