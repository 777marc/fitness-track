from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Workout, ScheduledWorkout, WorkoutType, CustomWorkout
from forms import ScheduledWorkoutForm
from datetime import datetime, timedelta
from collections import defaultdict

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.route('/schedule')
@login_required
def schedule():
    week_offset = request.args.get('week', 0, type=int)
    
    today = datetime.utcnow().date()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    
    scheduled_workouts = ScheduledWorkout.query.filter(
        ScheduledWorkout.user_id == current_user.id,
        ScheduledWorkout.scheduled_date >= week_dates[0],
        ScheduledWorkout.scheduled_date <= week_dates[6]
    ).all()
    
    workouts_by_date = defaultdict(list)
    for workout in scheduled_workouts:
        workouts_by_date[workout.scheduled_date].append(workout)
    
    return render_template('schedule/schedule.html', 
                         week_dates=week_dates,
                         workouts_by_date=workouts_by_date,
                         today=today,
                         week_offset=week_offset)

@schedule_bp.route('/schedule/add', methods=['GET', 'POST'])
@login_required
def add_scheduled_workout():
    form = ScheduledWorkoutForm()
    form.workout_type.choices = [(0, '-- Select Workout Type --')] + [(wt.id, wt.name) for wt in WorkoutType.query.all()]
    form.custom_workout.choices = [(0, '-- Select Custom Workout --')] + [(cw.id, cw.name) for cw in CustomWorkout.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        workout_type_id = form.workout_type.data if form.workout_type.data != 0 else None
        custom_workout_id = form.custom_workout.data if form.custom_workout.data != 0 else None
        
        if not workout_type_id and not custom_workout_id:
            flash('Please select either a workout type or a custom workout.', 'danger')
            return render_template('schedule/schedule_form.html', form=form)
        
        if workout_type_id and custom_workout_id:
            flash('Please select only one: either a workout type or a custom workout.', 'danger')
            return render_template('schedule/schedule_form.html', form=form)
        
        scheduled_workout = ScheduledWorkout(
            workout_type_id=workout_type_id,
            custom_workout_id=custom_workout_id,
            scheduled_date=form.scheduled_date.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(scheduled_workout)
        db.session.commit()
        flash('Workout scheduled successfully!', 'success')
        return redirect(url_for('schedule.schedule'))
    
    return render_template('schedule/schedule_form.html', form=form)

@schedule_bp.route('/schedule/<int:id>/delete', methods=['POST'])
@login_required
def delete_scheduled_workout(id):
    scheduled_workout = ScheduledWorkout.query.get_or_404(id)
    
    if scheduled_workout.user_id != current_user.id:
        flash('You can only delete your own scheduled workouts.', 'danger')
        return redirect(url_for('schedule.schedule'))
    
    db.session.delete(scheduled_workout)
    db.session.commit()
    flash('Scheduled workout deleted successfully!', 'success')
    return redirect(url_for('schedule.schedule'))

@schedule_bp.route('/schedule/<int:id>/complete', methods=['POST'])
@login_required
def complete_scheduled_workout(id):
    scheduled_workout = ScheduledWorkout.query.get_or_404(id)
    
    if scheduled_workout.user_id != current_user.id:
        flash('You can only complete your own scheduled workouts.', 'danger')
        return redirect(request.referrer or url_for('schedule.schedule'))
    
    # Mark as completed
    scheduled_workout.completed = True
    
    # Create workout history entry if it doesn't exist
    if not scheduled_workout.workout_id:
        # Determine duration and calories
        duration = 0
        calories = 0
        exercise_name = scheduled_workout.get_name()
        
        if scheduled_workout.workout_type:
            duration = scheduled_workout.workout_type.default_duration or 30
            calories = scheduled_workout.workout_type.default_calories or 200
        elif scheduled_workout.custom_workout:
            # Estimate based on number of exercises (assuming 5 min per exercise)
            num_exercises = len(scheduled_workout.custom_workout.exercises)
            duration = num_exercises * 5
            calories = duration * 7  # Rough estimate: 7 calories per minute
        
        # Create workout entry
        workout = Workout(
            exercise=exercise_name,
            duration=duration,
            calories=calories,
            notes=scheduled_workout.notes or f"Completed scheduled workout: {exercise_name}",
            date=scheduled_workout.scheduled_date,
            user_id=current_user.id
        )
        db.session.add(workout)
        db.session.flush()  # Get the workout ID
        scheduled_workout.workout_id = workout.id
    
    db.session.commit()
    flash('Workout marked as completed and added to history!', 'success')
    return redirect(request.referrer or url_for('schedule.schedule'))

@schedule_bp.route('/schedule/<int:id>/incomplete', methods=['POST'])
@login_required
def incomplete_scheduled_workout(id):
    scheduled_workout = ScheduledWorkout.query.get_or_404(id)
    
    if scheduled_workout.user_id != current_user.id:
        flash('You can only modify your own scheduled workouts.', 'danger')
        return redirect(request.referrer or url_for('schedule.schedule'))
    
    # Mark as not complete
    scheduled_workout.completed = False
    
    # Remove workout history entry if it exists
    if scheduled_workout.workout_id:
        workout = Workout.query.get(scheduled_workout.workout_id)
        if workout:
            db.session.delete(workout)
        scheduled_workout.workout_id = None
    
    db.session.commit()
    flash('Workout marked as not complete and removed from history.', 'info')
    return redirect(request.referrer or url_for('schedule.schedule'))
