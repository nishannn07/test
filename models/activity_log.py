from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin

class ActivityLog(db.Model, TimestampMixin):
    __tablename__ = 'activity_logs'
    
    id = Column(Integer, primary_key=True)
    action = Column(String(100), nullable=False)
    description = Column(Text)
    old_value = Column(Text)
    new_value = Column(Text)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    
    user = relationship("User", back_populates="activities")
    task = relationship("Task", back_populates="activities")
    project = relationship("Project", back_populates="activities")
