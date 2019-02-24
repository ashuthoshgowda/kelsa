from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class JobSeekerForm(FlaskForm):
    job_description = StringField('Job Description', validators=[DataRequired()])
    post_job = SubmitField('Post Job')