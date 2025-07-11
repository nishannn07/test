from flask import Flask, redirect, url_for, session
from flask_migrate import Migrate
from flask_mailman import Mail
from models import db
import models.user, models.project, models.task, models.role, models.comment, models.login, models.dashboard, models.notification, models.team
from routes.main_routes import main_bp
from routes.user_routes import user_bp
from routes.task_routes import tasks_bp
from routes.project_routes import projects_bp
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_be_changed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rnishan:nishan@localhost:5432/jira'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com' 
app.config['MAIL_PASSWORD'] = 'your_app_password'
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(projects_bp)
@app.route('/')
def home():
    return redirect(url_for('main.index'))
if __name__ == '__main__':
    app.run(debug=True)