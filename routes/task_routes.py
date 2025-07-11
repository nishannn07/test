from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.task_controller import (
    create_task, update_task, get_task_with_details, get_tasks_by_user,
    add_comment, log_time, search_tasks
)
from controllers.project_controller import get_user_projects
from form.task_form import TaskForm, CommentForm, TimeLogForm
from models.user import User
from models.project import Project

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/new', methods=['GET', 'POST'])
def new_task():
    if 'user_id' not in session:
        flash('Please login to create tasks', 'warning')
        return redirect(url_for('users.login'))
    
    form = TaskForm()
    form.assigned_to.choices = [(0, 'Unassigned')] + [(u.id, u.username) for u in User.query.all()]
    user_projects = get_user_projects(session['user_id'])
    form.project_id.choices = [(p.id, p.project_name) for p in user_projects]
    
    if not user_projects:
        flash('You need to be part of a project to create tasks', 'warning')
        return redirect(url_for('projects.list'))
    
    if form.validate_on_submit():
        task = create_task(form, session['user_id'])
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.view_task', task_id=task.id))
    
    return render_template('task_form.html', form=form, title='Create Task')

@tasks_bp.route('/<int:task_id>')
def view_task(task_id):
    if 'user_id' not in session:
        flash('Please login to view tasks', 'warning')
        return redirect(url_for('users.login'))
    
    task = get_task_with_details(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('main.index'))
    
    comment_form = CommentForm()
    time_form = TimeLogForm()
    
    return render_template('task_detail.html', task=task, 
                         comment_form=comment_form, time_form=time_form)

@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    if 'user_id' not in session:
        flash('Please login to edit tasks', 'warning')
        return redirect(url_for('users.login'))
    
    task = get_task_with_details(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('main.index'))
    
    form = TaskForm(obj=task)
    form.assigned_to.choices = [(0, 'Unassigned')] + [(u.id, u.username) for u in User.query.all()]
    user_projects = get_user_projects(session['user_id'])
    form.project_id.choices = [(p.id, p.project_name) for p in user_projects]
    
    if form.validate_on_submit():
        update_task(task_id, form, session['user_id'])
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.view_task', task_id=task_id))
    
    return render_template('task_form.html', form=form, task=task, title='Edit Task')

@tasks_bp.route('/<int:task_id>/comment', methods=['POST'])
def add_task_comment(task_id):
    if 'user_id' not in session:
        flash('Please login to add comments', 'warning')
        return redirect(url_for('users.login'))
    
    form = CommentForm()
    if form.validate_on_submit():
        add_comment(task_id, form.content.data, session['user_id'])
        flash('Comment added successfully!', 'success')
    
    return redirect(url_for('tasks.view_task', task_id=task_id))

@tasks_bp.route('/<int:task_id>/time', methods=['POST'])
def log_task_time(task_id):
    if 'user_id' not in session:
        flash('Please login to log time', 'warning')
        return redirect(url_for('users.login'))
    
    form = TimeLogForm()
    if form.validate_on_submit():
        log_time(task_id, form.hours_spent.data, form.description.data, 
                form.work_date.data, session['user_id'])
        flash('Time logged successfully!', 'success')
    
    return redirect(url_for('tasks.view_task', task_id=task_id))

@tasks_bp.route('/my-tasks')
def my_tasks():
    if 'user_id' not in session:
        flash('Please login to view your tasks', 'warning')
        return redirect(url_for('users.login'))
    
    tasks = get_tasks_by_user(session['user_id'])
    return render_template('my_tasks.html', tasks=tasks)