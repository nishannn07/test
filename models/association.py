from sqlalchemy import Table, Column, Integer, ForeignKey
from . import db
user_role_association = Table(
    'user_role',
    db.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)
user_project_association = Table(
    'user_project',
    db.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True)
)
team_user_association = Table(
    'team_user',
    db.metadata,
    Column('team_id', Integer, ForeignKey('teams.team_id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)
