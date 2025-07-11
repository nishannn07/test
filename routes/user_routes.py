from flask import render_template, request, redirect, url_for, Blueprint, flash, session
from controllers.user_controller import (
    create_user, get_user_by_username, check_user_password
)
from form.user_form import RegistrationForm, LoginForm

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if get_user_by_username(form.username.data):
            flash('Username already exists!', 'danger')
        else:
            create_user(form)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and check_user_password(user, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@user_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged Out', 'info')
    return redirect(url_for('users.login'))

from form.user_form import RequestResetForm
@user_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        flash('If an account with that email exists, a password reset link has been sent.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)
