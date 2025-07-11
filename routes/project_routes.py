from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.project_controller import (
    create_project, update_project, get_user_projects, get_project_with_stats,
    delete_project, get_all_projects
)
from controllers.task_controller import get_project_tasks_by_status
from form.project_form import ProjectForm
from models.user import User

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/')
def list():
    if 'user_id' not in session:
        flash('Please login to view projects', 'warning')
        return redirect(url_for('users.login'))
    
    projects = get_user_projects(session['user_id'])
    return render_template('projects.html', projects=projects)

@projects_bp.route('/new', methods=['GET', 'POST'])
def new_project():
    if 'user_id' not in session:
        flash('Please login to create projects', 'warning')
        return redirect(url_for('users.login'))
    
    form = ProjectForm()
    form.users.choices = [(u.id, u.username) for u in User.query.all()]
    
    if form.validate_on_submit():
        project = create_project(form, session['user_id'])
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects.view_project', project_id=project.id))
    
    return render_template('project_form.html', form=form, title='Create Project')

@projects_bp.route('/<int:project_id>')
def view_project(project_id):
    if 'user_id' not in session:
        flash('Please login to view projects', 'warning')
        return redirect(url_for('users.login'))
    
    project, stats = get_project_with_stats(project_id)
    return render_template('project_detail.html', project=project, stats=stats)

@projects_bp.route('/<int:project_id>/board')
def kanban_board(project_id):
    if 'user_id' not in session:
        flash('Please login to view board', 'warning')
        return redirect(url_for('users.login'))
    
    project, stats = get_project_with_stats(project_id)
    task_board = get_project_tasks_by_status(project_id)
    
    return render_template('kanban_board.html', project=project, 
                         task_board=task_board, stats=stats)

@projects_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    if 'user_id' not in session:
        flash('Please login to edit projects', 'warning')
        return redirect(url_for('users.login'))
    
    project, _ = get_project_with_stats(project_id)
    form = ProjectForm(obj=project)
    form.users.choices = [(u.id, u.username) for u in User.query.all()]
    form.users.data = [u.id for u in project.users]
    
    if form.validate_on_submit():
        update_project(project_id, form)
        flash('Project updated successfully!', 'success')
        return redirect(url_for('projects.view_project', project_id=project_id))
    
    return render_template('project_form.html', form=form, project=project, title='Edit Project')

@projects_bp.route('/<int:project_id>/delete', methods=['POST'])
def delete_project_route(project_id):
    if 'user_id' not in session:
        flash('Please login to delete projects', 'warning')
        return redirect(url_for('users.login'))
    
    delete_project(project_id)
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('projects.list'))
