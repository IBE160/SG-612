import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory SQLite for tests
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_task_model_fields(client):

    with app.app_context():

        # Test default values

        task = Task(title="Test Task")

        db.session.add(task)

        db.session.commit()

        retrieved_task = Task.query.filter_by(title="Test Task").first()



        assert retrieved_task.title == "Test Task"

        assert retrieved_task.notes is None

        assert retrieved_task.due_date is None

        assert retrieved_task.priority == "Medium"

        assert retrieved_task.label is None

        assert retrieved_task.is_done is False

        assert retrieved_task.created_at is not None



        # Test setting all fields

        from datetime import date

        task_full = Task(

            title="Full Task",

            notes="Some notes",

            due_date=date(2025, 12, 31),

            priority="High",

            label="Work",

            is_done=True

        )

        db.session.add(task_full)

        db.session.commit()

        retrieved_task_full = Task.query.filter_by(title="Full Task").first()



        assert retrieved_task_full.title == "Full Task"

        assert retrieved_task_full.notes == "Some notes"

        assert retrieved_task_full.due_date == date(2025, 12, 31)

        assert retrieved_task_full.priority == "High"

        assert retrieved_task_full.label == "Work"

        assert retrieved_task_full.is_done is True

        assert retrieved_task_full.created_at is not None

def test_create_task_api(client):
    """Test the POST /api/tasks endpoint."""
    # Test successful creation
    response = client.post('/api/tasks', json={
        'title': 'API Test Task',
        'notes': 'Some notes for the API test',
        'due_date': '2025-12-25'
    })
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['title'] == 'API Test Task'
    assert json_data['notes'] == 'Some notes for the API test'
    assert json_data['id'] is not None

    # Verify it's in the database
    with app.app_context():
        task = Task.query.filter_by(title='API Test Task').first()
        assert task is not None
        assert task.notes == 'Some notes for the API test'

    # Test validation: missing title
    response_fail = client.post('/api/tasks', json={
        'notes': 'This should fail'
    })
    assert response_fail.status_code == 400
    json_data_fail = response_fail.get_json()
    assert json_data_fail['error'] == 'Title is required'

    # Test validation: empty title
    response_empty = client.post('/api/tasks', json={
        'title': '   ',
        'notes': 'This should also fail'
    })
    assert response_empty.status_code == 400
    assert response_empty.get_json()['error'] == 'Title is required'
