from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Workout, WorkoutType, ScheduledWorkout
from forms import LoginForm, RegisterForm, WorkoutForm, ScheduledWorkoutForm
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Public landing page
@app.route('/')
def index():
    return render_template('index.html')

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already registered. Please use a different one.', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Protected routes
@app.route('/dashboard')
@login_required
def dashboard():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    return render_template('dashboard.html', workouts=workouts)

@app.route('/workout/new', methods=['GET', 'POST'])
@login_required
def new_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(
            exercise=form.exercise.data,
            duration=form.duration.data,
            calories=form.calories.data,
            notes=form.notes.data,
            date=form.date.data,
            user_id=current_user.id
        )
        db.session.add(workout)
        db.session.commit()
        flash('Workout added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('workout_form.html', form=form, title='New Workout')

@app.route('/workout/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_workout(id):
    workout = Workout.query.get_or_404(id)
    
    if workout.user_id != current_user.id:
        flash('You can only edit your own workouts.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = WorkoutForm()
    if form.validate_on_submit():
        workout.exercise = form.exercise.data
        workout.duration = form.duration.data
        workout.calories = form.calories.data
        workout.notes = form.notes.data
        workout.date = form.date.data
        db.session.commit()
        flash('Workout updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.exercise.data = workout.exercise
        form.duration.data = workout.duration
        form.calories.data = workout.calories
        form.notes.data = workout.notes
        form.date.data = workout.date
    
    return render_template('workout_form.html', form=form, title='Edit Workout')

@app.route('/workout/<int:id>/delete', methods=['POST'])
@login_required
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    
    if workout.user_id != current_user.id:
        flash('You can only delete your own workouts.', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/stats')
@login_required
def stats():
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    
    total_workouts = len(workouts)
    total_duration = sum(w.duration for w in workouts)
    total_calories = sum(w.calories for w in workouts)
    
    stats_data = {
        'total_workouts': total_workouts,
        'total_duration': total_duration,
        'total_calories': total_calories
    }
    
    return render_template('stats.html', stats=stats_data, workouts=workouts)

@app.route('/schedule')
@login_required
def schedule():
    # Get the current week start (Monday)
    today = datetime.utcnow().date()
    week_offset = request.args.get('week', 0, type=int)
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    
    # Generate the week's dates
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    
    # Get scheduled workouts for the week
    scheduled_workouts = ScheduledWorkout.query.filter(
        ScheduledWorkout.user_id == current_user.id,
        ScheduledWorkout.scheduled_date >= week_dates[0],
        ScheduledWorkout.scheduled_date <= week_dates[6]
    ).all()
    
    # Organize workouts by date
    workouts_by_date = {date: [] for date in week_dates}
    for workout in scheduled_workouts:
        if workout.scheduled_date in workouts_by_date:
            workouts_by_date[workout.scheduled_date].append(workout)
    
    return render_template('schedule.html', 
                         week_dates=week_dates, 
                         workouts_by_date=workouts_by_date,
                         week_offset=week_offset,
                         today=today)

@app.route('/schedule/add', methods=['GET', 'POST'])
@login_required
def add_scheduled_workout():
    form = ScheduledWorkoutForm()
    
    # Populate workout types
    workout_types = WorkoutType.query.all()
    form.workout_type.choices = [(wt.id, wt.name) for wt in workout_types]
    
    if form.validate_on_submit():
        scheduled_workout = ScheduledWorkout(
            workout_type_id=form.workout_type.data,
            scheduled_date=form.scheduled_date.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(scheduled_workout)
        db.session.commit()
        flash('Workout scheduled successfully!', 'success')
        return redirect(url_for('schedule'))
    
    return render_template('schedule_form.html', form=form, title='Schedule Workout')

@app.route('/schedule/<int:id>/delete', methods=['POST'])
@login_required
def delete_scheduled_workout(id):
    scheduled_workout = ScheduledWorkout.query.get_or_404(id)
    
    if scheduled_workout.user_id != current_user.id:
        flash('You can only delete your own scheduled workouts.', 'danger')
        return redirect(url_for('schedule'))
    
    db.session.delete(scheduled_workout)
    db.session.commit()
    flash('Scheduled workout deleted successfully!', 'success')
    return redirect(url_for('schedule'))

@app.route('/schedule/<int:id>/complete', methods=['POST'])
@login_required
def complete_scheduled_workout(id):
    scheduled_workout = ScheduledWorkout.query.get_or_404(id)
    
    if scheduled_workout.user_id != current_user.id:
        flash('You can only complete your own scheduled workouts.', 'danger')
        return redirect(url_for('schedule'))
    
    scheduled_workout.completed = True
    db.session.commit()
    flash('Workout marked as completed!', 'success')
    return redirect(url_for('schedule'))

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_workout_types()
    app.run(host='0.0.0.0', port=5000, debug=True)
