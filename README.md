# Fitness Tracker App

A Flask-based workout tracking application with user authentication, workout scheduling, and SQLite database.

## Features

- **User Authentication**: Secure registration and login system with password hashing
- **Public Landing Page**: Accessible without authentication
- **Workout Tracking**: Log exercises with duration, calories, and notes
- **Weekly Schedule**: Plan workouts for the week with a visual calendar view
- **Workout Types**: Pre-loaded workout types (Running, Cycling, Yoga, HIIT, etc.)
- **Schedule Management**: Add, delete, and mark workouts as completed
- **Dashboard**: View all your workouts at a glance
- **Statistics**: Track your total workouts, duration, and calories burned
- **CRUD Operations**: Create, read, update, and delete workouts
- **Dark Mode UI**: Modern dark theme with excellent readability
- **Responsive Design**: Bootstrap-powered UI that works on all devices

## Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)

## Installation

### Local Setup

1. Clone the repository or navigate to the project directory:

   ```bash
   cd fitness-track
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

### Docker Setup

1. Build the Docker image:

   ```bash
   docker build -t fitness-tracker .
   ```

2. Run the container:

   ```bash
   docker run -p 5000:5000 -v $(pwd)/instance:/app/instance fitness-tracker
   ```

   Or use Docker Compose:

   ```bash
   docker-compose up
   ```

3. Open your browser and navigate to `http://localhost:5000`

## Project Structure # Main application file with routes

├── models.py # Database models (User, Workout, WorkoutType, ScheduledWorkout)
├── forms.py # WTForms definitions
├── requirements.txt # Python dependencies
├── Dockerfile # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── .gitignore # Git ignore rules
├── templates/ # HTML templates
│ ├── base.html # Base template with dark mode
│ ├── index.html # Landing page
│ ├── login.html # Login page
│ ├── register.html # Registration page
│ ├── dashboard.html # User dashboard
│ ├── workout_form.html # Add/Edit workout
│ ├── schedule.html # Weekly schedule view
│ ├── schedule_form.html # Schedule workout form
│ └── stats.html # Statistics page
└── instance/ ter.html # Registration page
│ ├── dashboard.html # User dashboard
│ ├── workout_form.html # Add/Edit workout
│ └── stats.html # Statistics page
└── instance/ # Database storage (created at runtime)
└── fitness_tracker.db

```

## Usage

1. **Landing Page**: Visit the home page to learn about the app
2. **Dashboard**: View all your completed workouts in a table format
5. **Add Workouts**: Click "Add New Workout" to log your exercises
6. **Schedule Workouts**:
   - Navigate to "Schedule" to see your weekly workout plan
   - Click "Schedule Workout" to add workouts to specific days
   - Select from 8 pre-loaded workout types (Running, Cycling, Swimming, Weight Training, Yoga, HIIT, Walking, Pilates)
   - Navigate between weeks using Previous/Next buttons
   - Mark scheduled workouts as completed
   - Delete scheduled workouts as needed
7. **Edit/Delete**: Modify or remove completed workouts from dashboard
8. **Statistics**: View your fitness progress and totals

## Pre-loaded Workout Types

The app comes with 8 default workout types:

- **Running** - Cardiovascular exercise (30 min, 300 cal)
- **Cycling** - Bike riding workout (45 min, 400 cal)
- **Swimming** - Full body water workout (30 min, 350 cal)
- **Weight Training** - Strength building exercises (60 min, 250 cal)
- **Yoga** - Flexibility and mindfulness (45 min, 150 cal)
- **HIIT** - High intensity interval training (30 min, 400 cal)
- **Walking** - Low impact cardio (30 min, 150 cal)
- **Pilates** - Core strengthening (45 min, 200 cal)format
6. **Edit/Delete**: Modify or remove workouts as needed
7. **Statistics**: View your fitness progress and totals

## Security Notes

- Change the `SECRET_KEY` in production (use environment variable)
- Passwords are hashed using Werkzeug's pbkdf2:sha256
- User sessions are managed with Flask-Login
- CSRF protection enabled via Flask-WTF

## Environment Variables

- `SECRET_KEY`: Secret key for session management (required in production)

## License

This project is open source and available for educational purposes.
```
