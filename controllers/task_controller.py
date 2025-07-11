from models.task import Task
from models.project import Project
from models.user import User
from models.comment import Comment
from models.time_log import TimeLog
from models.activity_log import ActivityLog
from models import db
from datetime import datetime

def create_task(form, user_id):
    task = Task(
        title=form.title.data,
        description=form.description.data,
        work_type=form.work_type.data,
        priority=form.priority.data,
        status=form.status.data,
        assigned_to=form.assigned_to.data if form.assigned_to.data != 0 else None,
        project_id=form.project_id.data,
        due_date=form.due_date.data,
        estimated_hours=form.estimated_hours.data,
        story_points=form.story_points.data,
        reporter_id=user_id
    )
    db.session.add(task)
    db.session.commit()
    log_activity(user_id, task.id, task.project_id, 'created', f'Task "{task.title}" created')
    return task

def update_task(task_id, form, user_id):
    task = Task.query.get_or_404(task_id)
    old_status = task.status
    old_assignee = task.assigned_to
    
    task.title = form.title.data
    task.description = form.description.data
    task.work_type = form.work_type.data
    task.priority = form.priority.data
    task.status = form.status.data
    task.assigned_to = form.assigned_to.data if form.assigned_to.data != 0 else None
    task.due_date = form.due_date.data
    task.estimated_hours = form.estimated_hours.data
    task.story_points = form.story_points.data
    
    db.session.commit()
    if old_status != task.status:
        log_activity(user_id, task.id, task.project_id, 'status_changed', 
                    f'Status changed from {old_status} to {task.status}')
    if old_assignee != task.assigned_to:
        old_name = User.query.get(old_assignee).username if old_assignee else 'Unassigned'
        new_name = User.query.get(task.assigned_to).username if task.assigned_to else 'Unassigned'
        log_activity(user_id, task.id, task.project_id, 'assigned', 
                    f'Assignee changed from {old_name} to {new_name}')
    
    return task

def get_tasks_by_project(project_id):
    return Task.query.filter_by(project_id=project_id, is_deleted=False).all()

def get_tasks_by_user(user_id):
    return Task.query.filter_by(assigned_to=user_id, is_deleted=False).all()

def get_task_with_details(task_id):
    return Task.query.filter_by(id=task_id, is_deleted=False).first()

def add_comment(task_id, content, user_id):
    comment = Comment(
        content=content,
        task_id=task_id,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()
    task = Task.query.get(task_id)
    log_activity(user_id, task_id, task.project_id, 'commented', 'Added a comment')
    return comment

def log_time(task_id, hours, description, work_date, user_id):
    time_log = TimeLog(
        task_id=task_id,
        user_id=user_id,
        hours_spent=hours,
        description=description,
        work_date=work_date
    )
    db.session.add(time_log)
    db.session.commit()
    task = Task.query.get(task_id)
    log_activity(user_id, task_id, task.project_id, 'time_logged', 
                f'Logged {hours} hours')
    return time_log

def log_activity(user_id, task_id, project_id, action, description):
    activity = ActivityLog(
        user_id=user_id,
        task_id=task_id,
        project_id=project_id,
        action=action,
        description=description
    )
    db.session.add(activity)
    db.session.commit()

def get_project_tasks_by_status(project_id):
    tasks = Task.query.filter_by(project_id=project_id, is_deleted=False).all()
    
    task_board = {
        'todo': [],
        'in_progress': [],
        'in_review': [],
        'done': []
    }
    
    for task in tasks:
        if task.status in task_board:
            task_board[task.status].append(task)
    
    return task_board

def search_tasks(query, user_id):
    user = User.query.get(user_id)
    project_ids = [p.id for p in user.projects]
    
    tasks = Task.query.filter(
        Task.project_id.in_(project_ids),
        Task.is_deleted == False,
        Task.title.contains(query)
    ).all()
    
    return tasks
