from models.project import Project
from models.user import User
from models.task import Task
from models import db
from sqlalchemy import func

def create_project(form, user_id):
    project = Project(
        project_name=form.project_name.data,
        project_key=form.project_key.data.upper(),
        description=form.description.data,
        project_link=form.project_link.data,
        status=form.status.data
    )
    db.session.add(project)
    db.session.commit()
    user = User.query.get(user_id)
    project.users.append(user)
    for user_id in form.users.data:
        user = User.query.get(user_id)
        if user and user not in project.users:
            project.users.append(user)
    
    db.session.commit()
    return project

def update_project(project_id, form):
    project = Project.query.get_or_404(project_id)
    project.project_name = form.project_name.data
    project.project_key = form.project_key.data.upper()
    project.description = form.description.data
    project.project_link = form.project_link.data
    project.status = form.status.data
    project.users.clear()
    for user_id in form.users.data:
        user = User.query.get(user_id)
        if user:
            project.users.append(user)
    
    db.session.commit()
    return project

def get_user_projects(user_id):
    user = User.query.get(user_id)
    return user.projects if user else []

def get_project_with_stats(project_id):
    project = Project.query.get_or_404(project_id)
    task_stats = db.session.query(
        Task.status,
        func.count(Task.id).label('count')
    ).filter_by(project_id=project_id, is_deleted=False).group_by(Task.status).all()
    
    stats = {status: count for status, count in task_stats}
    total_tasks = Task.query.filter_by(project_id=project_id, is_deleted=False).count()
    from datetime import date
    overdue_tasks = Task.query.filter(
        Task.project_id == project_id,
        Task.is_deleted == False,
        Task.due_date < date.today(),
        Task.status != 'done'
    ).count()
    
    stats['total'] = total_tasks
    stats['overdue'] = overdue_tasks
    
    return project, stats

def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.is_deleted = True
    db.session.commit()

def get_all_projects():
    return Project.query.filter_by(is_deleted=False).all()
