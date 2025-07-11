from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from controllers.project_controller import get_user_projects, get_project_with_stats
from controllers.task_controller import get_tasks_by_user, search_tasks
from models.activity_log import ActivityLog
from models.notification import Notification

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('users.login'))
    projects = get_user_projects(session['user_id'])
    tasks = get_tasks_by_user(session['user_id'])
    activities = ActivityLog.query.filter_by(
        user_id=session['user_id']
    ).order_by(ActivityLog.created_at.desc()).limit(10).all()
    return render_template('dashboard.html', 
                         projects=projects, 
                         tasks=tasks, 
                         activities=activities)

@main_bp.route('/search')
def results():
    if 'user_id' not in session:
        flash('Please login to search', 'warning')
        return redirect(url_for('users.login'))
    
    query = request.args.get('q', '')
    tasks = []
    
    if query:
        tasks = search_tasks(query, session['user_id'])
    
    return render_template('search_results.html', tasks=tasks, query=query)

@main_bp.route('/for-you')
def for_you():
    if 'user_id' not in session:
        flash('Please login to view this page', 'warning')
        return redirect(url_for('users.login'))
    assigned_tasks = get_tasks_by_user(session['user_id'])
    user_projects = get_user_projects(session['user_id'])
    project_ids = [p.id for p in user_projects]
    
    activities = ActivityLog.query.filter(
        ActivityLog.project_id.in_(project_ids)
    ).order_by(ActivityLog.created_at.desc()).limit(20).all()
    
    return render_template('for_you.html', 
                         tasks=assigned_tasks, 
                         activities=activities)

@main_bp.route('/notifications')
def notifications():
    if 'user_id' not in session:
        flash('Please login to view notifications', 'warning')
        return redirect(url_for('users.login'))
    
    notifications = Notification.query.filter_by(
        user_id=session['user_id']
    ).order_by(Notification.created_at.desc()).all()
    
    return render_template('notifications.html', notifications=notifications)
