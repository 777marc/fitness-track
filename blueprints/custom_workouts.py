from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Exercise, CustomWorkout, CustomWorkoutExercise

custom_workouts_bp = Blueprint('custom_workouts', __name__)

@custom_workouts_bp.route('/workout-designer')
@login_required
def workout_designer():
    categories = db.session.query(Exercise.category).distinct().all()
    categories = [c[0] for c in categories]
    
    difficulties = db.session.query(Exercise.difficulty).distinct().all()
    difficulties = [d[0] for d in difficulties]
    
    equipment = db.session.query(Exercise.equipment).distinct().all()
    equipment = [e[0] for e in equipment]
    
    custom_workouts = CustomWorkout.query.filter_by(user_id=current_user.id).order_by(CustomWorkout.created_at.desc()).all()
    
    return render_template('custom_workouts/workout_designer.html', 
                         categories=categories,
                         difficulties=difficulties,
                         equipment_list=equipment,
                         custom_workouts=custom_workouts)

@custom_workouts_bp.route('/api/exercises')
@login_required
def get_exercises():
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    equipment = request.args.get('equipment')
    search = request.args.get('search', '').lower()
    
    query = Exercise.query
    
    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if equipment:
        query = query.filter_by(equipment=equipment)
    if search:
        query = query.filter(Exercise.name.ilike(f'%{search}%'))
    
    exercises = query.all()
    
    return jsonify([{
        'id': ex.id,
        'name': ex.name,
        'category': ex.category,
        'muscle_groups': ex.primary_muscle_groups,
        'equipment': ex.equipment,
        'difficulty': ex.difficulty,
        'goal': ex.workout_goal,
        'location': ex.location
    } for ex in exercises])

@custom_workouts_bp.route('/workout-designer/save', methods=['POST'])
@login_required
def save_custom_workout():
    data = request.get_json()
    
    workout_name = data.get('name')
    workout_description = data.get('description', '')
    exercises = data.get('exercises', [])
    
    if not workout_name or not exercises:
        return jsonify({'error': 'Workout name and exercises are required'}), 400
    
    custom_workout = CustomWorkout(
        name=workout_name,
        description=workout_description,
        user_id=current_user.id
    )
    db.session.add(custom_workout)
    db.session.flush()
    
    for idx, ex_data in enumerate(exercises):
        workout_exercise = CustomWorkoutExercise(
            custom_workout_id=custom_workout.id,
            exercise_id=ex_data['id'],
            sets=ex_data.get('sets'),
            reps=ex_data.get('reps'),
            duration=ex_data.get('duration'),
            order=idx,
            notes=ex_data.get('notes', '')
        )
        db.session.add(workout_exercise)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Custom workout saved successfully!',
        'workout_id': custom_workout.id
    })

@custom_workouts_bp.route('/workout-designer/<int:id>')
@login_required
def view_custom_workout(id):
    workout = CustomWorkout.query.get_or_404(id)
    
    if workout.user_id != current_user.id:
        flash('You can only view your own workouts.', 'danger')
        return redirect(url_for('custom_workouts.workout_designer'))
    
    exercises = CustomWorkoutExercise.query.filter_by(custom_workout_id=id).order_by(CustomWorkoutExercise.order).all()
    
    return render_template('custom_workouts/custom_workout_view.html', workout=workout, exercises=exercises)

@custom_workouts_bp.route('/workout-designer/<int:id>/delete', methods=['POST'])
@login_required
def delete_custom_workout(id):
    workout = CustomWorkout.query.get_or_404(id)
    
    if workout.user_id != current_user.id:
        flash('You can only delete your own workouts.', 'danger')
        return redirect(url_for('custom_workouts.workout_designer'))
    
    db.session.delete(workout)
    db.session.commit()
    flash('Custom workout deleted successfully!', 'success')
    return redirect(url_for('custom_workouts.workout_designer'))
