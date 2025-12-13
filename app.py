from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta # Import date and timedelta for calculations
import os

# Import the get_ai_suggestions function
from ai_service import get_ai_suggestions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'tasks.db')}"
# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Medium')
    label = db.Column(db.String(50), nullable=True)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Task('{self.title}', '{self.due_date}', '{self.priority}')"

@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    db.create_all()
    print('Initialized the database.')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    notes = data.get('notes')
    due_date_str = data.get('due_date')
    priority = data.get('priority', 'Medium') # Default to 'Medium' if not provided
    label = data.get('label')

    if not title or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    new_task = Task(
        title=title, 
        notes=notes, 
        due_date=due_date,
        priority=priority,
        label=label
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "id": new_task.id,
        "title": new_task.title,
        "notes": new_task.notes,
        "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
        "priority": new_task.priority,
        "label": new_task.label,
        "is_done": new_task.is_done,
        "created_at": new_task.created_at.isoformat()
    }), 201

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    priority_filter = request.args.get('priority')
    due_date_before_str = request.args.get('due_date_before')
    due_date_within_days_str = request.args.get('due_date_within_days') # New parameter
    label_filter = request.args.get('label')
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')

    tasks_query = Task.query

    valid_priorities = ['High', 'Medium', 'Low']
    if priority_filter:
        if priority_filter in valid_priorities:
            tasks_query = tasks_query.filter_by(priority=priority_filter)
        else:
            # If an invalid priority is requested, return an empty set of tasks
            tasks_query = tasks_query.filter(Task.priority == "InvalidPriorityFilter") 
    
    # Handle due_date_within_days
    if due_date_within_days_str:
        try:
            due_date_within_days = int(due_date_within_days_str)
            if due_date_within_days < 0:
                return jsonify({"error": "due_date_within_days must be non-negative"}), 400
            
            # Calculate the date 'due_date_within_days' from today
            target_date = date.today() + timedelta(days=due_date_within_days)
            tasks_query = tasks_query.filter(Task.due_date <= target_date)
        except ValueError:
            return jsonify({"error": "Invalid due_date_within_days format. Must be an integer."}), 400

    elif due_date_before_str: # Only process due_date_before if due_date_within_days is not present
        try:
            due_date_before = datetime.strptime(due_date_before_str, '%Y-%m-%d').date()
            tasks_query = tasks_query.filter(Task.due_date <= due_date_before)
        except ValueError:
            return jsonify({"error": "Invalid due_date_before format. Use YYYY-MM-DD"}), 400

    if label_filter:
        tasks_query = tasks_query.filter_by(label=label_filter)

    if sort_by:
        if sort_by == 'priority':
            if order == 'desc':
                tasks_query = tasks_query.order_by(
                    db.case(
                        (Task.priority == 'High', 1),
                        (Task.priority == 'Medium', 2),
                        (Task.priority == 'Low', 3),
                        else_=4
                    ).asc()
                )
            else:
                tasks_query = tasks_query.order_by(
                    db.case(
                        (Task.priority == 'Low', 1),
                        (Task.priority == 'Medium', 2),
                        (Task.priority == 'High', 3),
                        else_=4
                    ).asc()
                )
        elif sort_by == 'due_date':
            if order == 'desc':
                tasks_query = tasks_query.order_by(Task.due_date.desc())
            else:
                tasks_query = tasks_query.order_by(Task.due_date.asc())
        elif sort_by == 'created_at':
            if order == 'desc':
                tasks_query = tasks_query.order_by(Task.created_at.desc())
            else:
                tasks_query = tasks_query.order_by(Task.created_at.asc())
        else:
            tasks_query = tasks_query.order_by(Task.created_at.desc())
    else:
        tasks_query = tasks_query.order_by(Task.created_at.desc())

    tasks = tasks_query.all()
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            "id": task.id,
            "title": task.title,
            "notes": task.notes,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "priority": task.priority,
            "label": task.label,
            "is_done": task.is_done,
            "created_at": task.created_at.isoformat()
        })
    return jsonify(tasks_data), 200

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = db.session.get(Task, task_id) # Using db.session.get for primary key lookup
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()

    if 'title' in data:
        title = data.get('title')
        if not title or not title.strip():
            return jsonify({"error": "Title cannot be empty"}), 400
        task.title = title

    if 'notes' in data:
        task.notes = data.get('notes')

    if 'priority' in data:
        task.priority = data.get('priority')

    if 'label' in data:
        task.label = data.get('label')
    
    if 'is_done' in data:
        task.is_done = bool(data.get('is_done'))

    if 'due_date' in data:
        due_date_str = data.get('due_date')
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        else:
            task.due_date = None

    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "notes": task.notes,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "priority": task.priority,
        "label": task.label,
        "is_done": task.is_done,
        "created_at": task.created_at.isoformat()
    }), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    db.session.delete(task)
    db.session.commit()
    return '', 204 # 204 No Content

@app.route('/api/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    title = data.get('title')

    if not title or not title.strip():
        return jsonify({"error": "Title is required for suggestions"}), 400

    try:
        suggestions = get_ai_suggestions(title)
        # The ai_service.py already handles fallbacks internally if Gemini API fails
        return jsonify(suggestions), 200
    except ValueError as e: # Catch ValueErrors from ai_service (e.g., missing API key)
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # Generic error handling for unexpected issues from ai_service
        print(f"Error getting AI suggestions: {e}")
        return jsonify({"error": "Failed to get AI suggestions due to an internal error."}), 500


if __name__ == '__main__':
    app.run(debug=True)