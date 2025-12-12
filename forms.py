from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class WorkoutForm(FlaskForm):
    exercise = StringField('Exercise Type', validators=[DataRequired(), Length(max=100)])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    calories = IntegerField('Calories Burned', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    date = DateField('Date', format='%Y-%m-%d', default=datetime.utcnow().date, validators=[DataRequired()])
    submit = SubmitField('Save Workout')

class ScheduledWorkoutForm(FlaskForm):
    workout_type = SelectField('Workout Type', coerce=int, validators=[DataRequired()])
    scheduled_date = DateField('Scheduled Date', format='%Y-%m-%d', default=datetime.utcnow().date, validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Schedule Workout')
