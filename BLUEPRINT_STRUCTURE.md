# Flask Application Blueprint Structure

This application is organized using Flask Blueprints for better code organization and maintainability.

## Blueprint Organization

### 1. **Main Blueprint** (`blueprints/main.py`)

- **Route**: `/`
- **Purpose**: Public landing page
- **Routes**:
  - `GET /` - Landing page (no authentication required)

### 2. **Auth Blueprint** (`blueprints/auth.py`)

- **Purpose**: User authentication and account management
- **Routes**:
  - `GET/POST /register` - User registration
  - `GET/POST /login` - User login
  - `GET /logout` - User logout

### 3. **Workouts Blueprint** (`blueprints/workouts.py`)

- **Purpose**: Workout history and CRUD operations
- **Routes**:
  - `GET /dashboard` - User dashboard with workout history and upcoming workouts
  - `GET/POST /workout/new` - Add new workout
  - `GET/POST /workout/<id>/edit` - Edit existing workout
  - `POST /workout/<id>/delete` - Delete workout
  - `GET /stats` - Workout statistics (placeholder)

### 4. **Schedule Blueprint** (`blueprints/schedule.py`)

- **Purpose**: Weekly workout scheduling and planning
- **Routes**:
  - `GET /schedule` - Weekly calendar view
  - `GET/POST /schedule/add` - Schedule a new workout
  - `POST /schedule/<id>/delete` - Delete scheduled workout
  - `POST /schedule/<id>/complete` - Mark workout as complete (adds to history)
  - `POST /schedule/<id>/incomplete` - Mark workout as incomplete (removes from history)

### 5. **Custom Workouts Blueprint** (`blueprints/custom_workouts.py`)

- **Purpose**: Custom workout designer with exercise library
- **Routes**:
  - `GET /workout-designer` - Workout designer page
  - `GET /api/exercises` - API endpoint for exercise search/filtering
  - `POST /workout-designer/save` - Save custom workout
  - `GET /workout-designer/<id>` - View custom workout details
  - `POST /workout-designer/<id>/delete` - Delete custom workout

## Application Structure

```
fitness-track/
├── app.py                      # Main application file (blueprint registration, config)
├── models.py                   # Database models
├── forms.py                    # WTForms definitions
├── blueprints/
│   ├── __init__.py
│   ├── main.py                 # Landing page
│   ├── auth.py                 # Authentication
│   ├── workouts.py             # Workout CRUD
│   ├── schedule.py             # Workout scheduling
│   └── custom_workouts.py      # Custom workout designer
├── templates/                  # Jinja2 templates
├── static/                     # CSS, JS, images
└── data/                       # Exercise data files
```

## Benefits of Blueprint Organization

1. **Separation of Concerns**: Each blueprint handles a specific domain
2. **Maintainability**: Easier to locate and modify specific functionality
3. **Scalability**: New features can be added as new blueprints
4. **Reusability**: Blueprints can be easily reused in other projects
5. **Team Collaboration**: Different team members can work on different blueprints
6. **Testing**: Easier to write isolated tests for each blueprint

## URL Prefixes

Currently, all blueprints are registered without URL prefixes. To add prefixes in the future:

```python
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(workouts_bp, url_prefix='/workouts')
```

## Adding a New Blueprint

1. Create new file in `blueprints/` directory
2. Define blueprint: `my_bp = Blueprint('my_blueprint', __name__)`
3. Add routes using `@my_bp.route()`
4. Import and register in `app.py`: `app.register_blueprint(my_bp)`
