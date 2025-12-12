from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    workouts = db.relationship('Workout', backref='user', lazy=True, cascade='all, delete-orphan')
    scheduled_workouts = db.relationship('ScheduledWorkout', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    calories = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Workout {self.exercise} - {self.date}>'

class WorkoutType(db.Model):
    __tablename__ = 'workout_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    default_duration = db.Column(db.Integer)  # in minutes
    default_calories = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<WorkoutType {self.name}>'

class ScheduledWorkout(db.Model):
    __tablename__ = 'scheduled_workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_type_id = db.Column(db.Integer, db.ForeignKey('workout_types.id'), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    workout_type = db.relationship('WorkoutType', backref='scheduled_workouts')
    
    def __repr__(self):
        return f'<ScheduledWorkout {self.workout_type_id} - {self.scheduled_date}>'
