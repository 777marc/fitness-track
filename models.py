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
    custom_workouts = db.relationship('CustomWorkout', backref='user', lazy=True, cascade='all, delete-orphan')
    
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

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    primary_muscle_groups = db.Column(db.String(200))
    equipment = db.Column(db.String(100))
    difficulty = db.Column(db.String(20))
    workout_goal = db.Column(db.String(50))
    location = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<Exercise {self.name}>'

class CustomWorkout(db.Model):
    __tablename__ = 'custom_workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    exercises = db.relationship('CustomWorkoutExercise', backref='custom_workout', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CustomWorkout {self.name}>'

class CustomWorkoutExercise(db.Model):
    __tablename__ = 'custom_workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    custom_workout_id = db.Column(db.Integer, db.ForeignKey('custom_workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration = db.Column(db.Integer)  # in minutes
    order = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    exercise = db.relationship('Exercise', backref='workout_exercises')
    
    def __repr__(self):
        return f'<CustomWorkoutExercise {self.exercise_id} in {self.custom_workout_id}>'
        return f'<ScheduledWorkout {self.workout_type_id} - {self.scheduled_date}>'
