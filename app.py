from flask import Flask
from flask_login import LoginManager
from models import db, User, WorkoutType, Exercise
from datetime import datetime
import os
import pandas as pd

# Import blueprints
from blueprints.main import main_bp
from blueprints.auth import auth_bp
from blueprints.workouts import workouts_bp
from blueprints.schedule import schedule_bp
from blueprints.custom_workouts import custom_workouts_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(workouts_bp)
app.register_blueprint(schedule_bp)
app.register_blueprint(custom_workouts_bp)

def init_workout_types():
    """Initialize default workout types if none exist"""
    if WorkoutType.query.count() == 0:
        default_types = [
            WorkoutType(name='Running', description='Cardiovascular exercise', default_duration=30, default_calories=300),
            WorkoutType(name='Cycling', description='Bike riding workout', default_duration=45, default_calories=400),
            WorkoutType(name='Swimming', description='Full body water workout', default_duration=30, default_calories=350),
            WorkoutType(name='Weight Training', description='Strength building exercises', default_duration=60, default_calories=250),
            WorkoutType(name='Yoga', description='Flexibility and mindfulness', default_duration=45, default_calories=150),
            WorkoutType(name='HIIT', description='High intensity interval training', default_duration=30, default_calories=400),
            WorkoutType(name='Walking', description='Low impact cardio', default_duration=30, default_calories=150),
            WorkoutType(name='Pilates', description='Core strengthening', default_duration=45, default_calories=200),
        ]
        db.session.add_all(default_types)
        db.session.commit()

def load_exercises_from_excel():
    """Load exercises from Excel file into database"""
    if Exercise.query.count() == 0:
        # Get the absolute path to the Excel file
        base_dir = os.path.abspath(os.path.dirname(__file__))
        excel_path = os.path.join(base_dir, 'data', 'Comprehensive_Exercise_List.xlsx')
        
        if os.path.exists(excel_path):
            print(f"Loading exercises from: {excel_path}")
            df = pd.read_excel(excel_path)
            exercises = []
            for _, row in df.iterrows():
                exercise = Exercise(
                    name=row['Exercise'],
                    category=row['Category'],
                    primary_muscle_groups=row['Primary Muscle Groups'],
                    equipment=row['Equipment'],
                    difficulty=row['Difficulty'],
                    workout_goal=row['Workout Goal'],
                    location=row['Location']
                )
                exercises.append(exercise)
            db.session.add_all(exercises)
            db.session.commit()
            print(f"Loaded {len(exercises)} exercises from Excel file")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_workout_types()
        load_exercises_from_excel()
    app.run(host='0.0.0.0', port=5000, debug=True)
