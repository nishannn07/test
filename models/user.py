from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin
from .association import *

class User(db.Model, TimestampMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    
    roles = relationship("Role", secondary=user_role_association, back_populates="users")
    projects = relationship("Project", secondary=user_project_association, back_populates="users")
    teams = relationship("Team", secondary=team_user_association, back_populates="members")
    comments = relationship("Comment", back_populates="user")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
    reported_tasks = relationship("Task", foreign_keys="Task.reporter_id", back_populates="reporter")
    notifications = relationship("Notification", back_populates="user")
    logins = relationship("Login", back_populates="user")
    time_logs = relationship("TimeLog", back_populates="user")
    activities = relationship("ActivityLog", back_populates="user")
