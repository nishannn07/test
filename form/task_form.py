from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    work_type = SelectField('Type', choices=[
        ('story', 'Story'), ('bug', 'Bug'), ('task', 'Task'), ('epic', 'Epic')
    ], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('lowest', 'Lowest'), ('low', 'Low'), ('medium', 'Medium'), 
        ('high', 'High'), ('highest', 'Highest')
    ], default='medium')
    status = SelectField('Status', choices=[
        ('todo', 'To Do'), ('in_progress', 'In Progress'), 
        ('in_review', 'In Review'), ('done', 'Done')
    ], default='todo')
    assigned_to = SelectField('Assignee', coerce=int, validators=[Optional()])
    project_id = SelectField('Project', coerce=int, validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[Optional()])
    estimated_hours = FloatField('Estimated Hours', validators=[Optional()])
    story_points = IntegerField('Story Points', validators=[Optional()])
    submit = SubmitField('Save Task')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')

class TimeLogForm(FlaskForm):
    hours_spent = FloatField('Hours Spent', validators=[DataRequired()])
    description = StringField('Work Description')
    work_date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Log Time')
