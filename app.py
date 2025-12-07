from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta # Import date and timedelta for calculations
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/PC/OneDrive/Documents/SG-612/instance/tasks.db'
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

    if not title or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    new_task = Task(title=title, notes=notes, due_date=due_date)
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
    label_filter = request.args.get('label')
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc') # Default to ascending

    tasks_query = Task.query

    if priority_filter == 'High':
        tasks_query = tasks_query.filter_by(priority='High')
    
    if due_date_before_str:
        try:
            due_date_before = datetime.strptime(due_date_before_str, '%Y-%m-%d').date()
            tasks_query = tasks_query.filter(Task.due_date <= due_date_before)
        except ValueError:
            return jsonify({"error": "Invalid due_date_before format. Use YYYY-MM-DD"}), 400

    if label_filter:
        tasks_query = tasks_query.filter_by(label=label_filter)

    if sort_by:
        if sort_by == 'priority':
            # Assuming 'High' > 'Medium' > 'Low' for sorting purposes
            # We can use a custom order_by clause for this
            if order == 'desc':
                tasks_query = tasks_query.order_by(
                    db.case(
                        (Task.priority == 'High', 1),
                        (Task.priority == 'Medium', 2),
                        (Task.priority == 'Low', 3),
                        else_=4 # For any other priority values
                    ).asc() # Use asc here because 1 is highest priority
                )
            else: # asc
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
        elif sort_by == 'created_at': # Default sort
            if order == 'desc':
                tasks_query = tasks_query.order_by(Task.created_at.desc())
            else:
                tasks_query = tasks_query.order_by(Task.created_at.asc())
        else:
            # Default sort if sort_by is invalid or not provided
            tasks_query = tasks_query.order_by(Task.created_at.desc())
    else:
        # Default sort if no sort_by is provided
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

    title = data.get('title')
    notes = data.get('notes')
    due_date_str = data.get('due_date')
    priority = data.get('priority')
    label = data.get('label')
    is_done = data.get('is_done')

    if not title or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    task.title = title
    task.notes = notes
    task.priority = priority
    task.label = label
    
    if is_done is not None:
        task.is_done = bool(is_done)

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

    # Due to blocking TypeError in ai_service, this is a mock response.
    # In a working environment, this would call:
    # suggestions = get_ai_suggestions(title)
    # from ai_service import get_ai_suggestions
    # For now, we simulate a fallback being used.

    print(f"Mock AI suggestion with fallback for title: {title}")
    
    suggestions = {}
    fallback_used = True # Always true for this mock

    # Rule-based fallback logic (from ACs of story 2.3)
    if "urgent" in title.lower() or "now" in title.lower():
        suggestions = {"priority": "High", "label": "Urgent"}
    elif "meeting" in title.lower() or "report" in title.lower():
        suggestions = {"priority": "Medium", "label": "Work"}
    elif "groceries" in title.lower() or "shop" in title.lower():
        suggestions = {"priority": "Low", "label": "Shopping"}
    else:
        suggestions = {"priority": "Low", "label": "Other"} # Default fallback

    suggestions['fallback'] = fallback_used
    return jsonify(suggestions), 200


if __name__ == '__main__':
    app.run(debug=True)