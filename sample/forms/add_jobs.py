from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job_title = StringField('job_title', validators=[DataRequired()])
    team_lid_id = PasswordField('team_lider_id', validators=[DataRequired()])
    work_size = PasswordField('work_size', validators=[DataRequired()])
    collabarators = StringField('collabarators', validators=[DataRequired()])
    remember_me = BooleanField('is job finished?')
    submit = SubmitField('submit')