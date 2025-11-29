from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from ai_service import get_ai_suggestions

# --- Applikasjonsoppsett ---
app = Flask(__name__)
# Konfigurerer databasen til å bruke en SQLite-fil
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiserer database-utvidelsen
db = SQLAlchemy(app)

# --- Database-modell ---
# Dette definerer strukturen for 'tasks'-tabellen i databasen.
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    label = db.Column(db.String(50), nullable=True, default='Other')
    priority = db.Column(db.String(20), nullable=True, default='Medium')
    is_done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        """Gjør om Task-objektet til en dictionary for enkel JSON-konvertering."""
        return {
            'id': self.id,
            'title': self.title,
            'notes': self.notes,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'label': self.label,
            'priority': self.priority,
            'is_done': self.is_done,
            'created_at': self.created_at.isoformat()
        }

# --- API-ruter ---

@app.route("/")
def index():
    # Dette er bare en midlertidig landingsside for å bekrefte at serveren kjører.
    # Du vil erstatte dette med din hovedside (dashboard) i Uke 3.
    return "<h1>Smart To-Do AI serveren kjører!</h1><p>Database er konfigurert. Klar til å motta API-kall.</p>"

@app.route("/api/tasks", methods=['POST'])
def create_task():
    """Oppretter en ny oppgave."""
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Mangler tittel for oppgaven'}), 400

    new_task = Task(
        title=data['title'],
        notes=data.get('notes'),
        label=data.get('label', 'Other'),
        priority=data.get('priority', 'Medium')
        # due_date kan også legges til her, men krever parsing fra string til datetime
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route("/api/tasks", methods=['GET'])
def get_tasks():
    """Henter alle oppgaver."""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Oppdaterer en eksisterende oppgave."""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    task.title = data.get('title', task.title)
    task.notes = data.get('notes', task.notes)
    task.label = data.get('label', task.label)
    task.priority = data.get('priority', task.priority)
    task.is_done = data.get('is_done', task.is_done)

    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Sletter en oppgave."""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task with ID {task_id} was deleted.'})


@app.route("/api/suggest", methods=['POST'])
def handle_suggestions():
    """
    Dette er endepunktet som frontend vil kalle for 'Magic Fill'-knappen.
    Den forventer en JSON-body med en 'title'-nøkkel.
    f.eks: {"title": "Study for math exam"}
    """
    # Hent data fra requesten
    data = request.get_json()
    
    if not data or 'title' not in data:
        # Returner en feilmelding hvis requesten er ugyldig
        return jsonify({"error": "Mangler 'title' i request body"}), 400
        
    task_title = data['title']
    
    # Kall vår AI-tjeneste for å få forslag
    suggestions = get_ai_suggestions(task_title)
    
    # Returner forslagene som JSON
    return jsonify(suggestions)

# --- Custom CLI-kommandoer ---
@app.cli.command("init-db")
def init_db_command():
    """Oppretter databasetabellene."""
    with app.app_context():
        db.create_all()
    print("Database initialisert og 'tasks.db' er opprettet.")


# --- Kjøre applikasjonen ---

# For å kjøre serveren, skriv i terminalen:
# 1. $env:FLASK_APP = "app.py"
# 2. python -m flask run
#
# (På Mac/Linux: export FLASK_APP=app.py)
if __name__ == '__main__':
    # Denne linjen lar deg kjøre med 'python app.py', men 'flask run' er anbefalt for utvikling.
    app.run(debug=True)
