from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Workout, ScheduledWorkout
from forms import WorkoutForm
from datetime import datetime, timedelta

workouts_bp = Blueprint('workouts', __name__)

@workouts_bp.route('/dashboard')
@login_required
def dashboard():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    
    # Get upcoming scheduled workouts for the next 7 days
    today = datetime.utcnow().date()
    end_date = today + timedelta(days=7)
    upcoming_workouts = ScheduledWorkout.query.filter(
        ScheduledWorkout.user_id == current_user.id,
        ScheduledWorkout.scheduled_date >= today,
        ScheduledWorkout.scheduled_date <= end_date
    ).order_by(ScheduledWorkout.scheduled_date).all()
    
    return render_template('workouts/dashboard.html', workouts=workouts, upcoming_workouts=upcoming_workouts)

@workouts_bp.route('/workout/new', methods=['GET', 'POST'])
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
        return redirect(url_for('workouts.dashboard'))
    return render_template('workouts/workout_form.html', form=form, title='Add Workout')

@workouts_bp.route('/workout/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_workout(id):
    workout = Workout.query.get_or_404(id)
    
    if workout.user_id != current_user.id:
        flash('You can only edit your own workouts.', 'danger')
        return redirect(url_for('workouts.dashboard'))
    
    form = WorkoutForm()
    if form.validate_on_submit():
        workout.exercise = form.exercise.data
        workout.duration = form.duration.data
        workout.calories = form.calories.data
        workout.notes = form.notes.data
        workout.date = form.date.data
        db.session.commit()
        flash('Workout updated successfully!', 'success')
        return redirect(url_for('workouts.dashboard'))
    elif request.method == 'GET':
        form.exercise.data = workout.exercise
        form.duration.data = workout.duration
        form.calories.data = workout.calories
        form.notes.data = workout.notes
        form.date.data = workout.date
    
    return render_template('workouts/workout_form.html', form=form, title='Edit Workout')

@workouts_bp.route('/workout/<int:id>/delete', methods=['POST'])
@login_required
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    
    if workout.user_id != current_user.id:
        flash('You can only delete your own workouts.', 'danger')
        return redirect(url_for('workouts.dashboard'))
    
    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted successfully!', 'success')
    return redirect(url_for('workouts.dashboard'))

@workouts_bp.route('/stats')
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
    
    return render_template('workouts/stats.html', stats=stats_data, workouts=workouts)
