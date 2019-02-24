from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class JobPosterform(FlaskForm):
    job_description = StringField('Job Details', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    start_time_options =[('Morning','Anytime by 12pm'),('Afternoon','Anytime by 5pm'),('Evening','Anytime by 9pm')]
    start_time = SelectField(u'Start Time', choices = start_time_options)
    submit = SubmitField('Post Job')
