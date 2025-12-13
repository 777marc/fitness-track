"""
Migration script to add workout_id column to scheduled_workouts table
Run this once to update the database schema
"""
from app import app, db
from models import ScheduledWorkout

with app.app_context():
    # Check if column already exists
    inspector = db.inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('scheduled_workouts')]
    
    if 'workout_id' not in columns:
        print("Adding workout_id column to scheduled_workouts table...")
        with db.engine.connect() as conn:
            conn.execute(db.text('ALTER TABLE scheduled_workouts ADD COLUMN workout_id INTEGER'))
            conn.commit()
        print("Migration completed successfully!")
    else:
        print("workout_id column already exists, no migration needed.")
