from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = IntegerField('Team leader', validators={DataRequired()})
    job_desc = TextAreaField('Job description', validators={DataRequired()})
    work_size = IntegerField('Work size (in hours)', validators={DataRequired()})
    collaborators = StringField('Collaborators of this job', validators={DataRequired()})
    start_date = DateField('Start date', validators={DataRequired()})
    end_date = DateField('End date', validators={DataRequired()})
    submit = SubmitField('Submit')
