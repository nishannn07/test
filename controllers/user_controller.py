from models.user import User
from models.login import Login 
from models import db 
def create_user(form):
    new_user = User(username=form.username.data, email=form.email.data)
    db.session.add(new_user)
    db.session.commit()
    new_login = Login(user_id=new_user.id, password=form.password.data)
    db.session.add(new_login)
    db.session.commit()
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user
def check_user_password(user, password):
    if not user:
        return False
    login_entry = Login.query.filter_by(user_id=user.id).first()
    if login_entry and login_entry.password == password:
        return True 
    return False
