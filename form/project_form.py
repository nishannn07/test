from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    project_key = StringField('Project Key', validators=[DataRequired()])
    description = TextAreaField('Description')
    project_link = StringField('Project Link')
    status = SelectField('Status', choices=[
        ('active', 'Active'), ('on_hold', 'On Hold'), ('completed', 'Completed')
    ], default='active')
    users = SelectMultipleField('Team Members', coerce=int)
    submit = SubmitField('Save Project')
