from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from . import db
from .mixins import TimestampMixin

class Task(db.Model, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    work_type = Column(String(50), nullable=False)
    priority = Column(String(50), default="medium", nullable=False)
    summary = Column(Text)
    status = Column(String(50), default="todo", nullable=False)
    due_date = Column(Date)
    estimated_hours = Column(Float)
    story_points = Column(Integer)

    assigned_to = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    reporter_id = Column(Integer, ForeignKey('users.id'))

    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_tasks")
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="reported_tasks")
    project = relationship("Project", back_populates="tasks")
    comments = relationship("Comment", back_populates="task")
    time_logs = relationship("TimeLog", back_populates="task")
    activities = relationship("ActivityLog", back_populates="task")
