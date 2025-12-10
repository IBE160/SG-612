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

def test_suggest_api_integration(client):
    """Test the POST /api/suggest endpoint integrates with ai_service."""
    mock_suggestions = {"priority": "High", "label": "Development"}
    
    with patch('ai_service.get_ai_suggestions', return_value=mock_suggestions) as mock_ai_service:
        response = client.post('/api/suggest', json={'title': 'Develop new feature'})
        assert response.status_code == 200
        assert response.get_json() == mock_suggestions
        mock_ai_service.assert_called_once_with('Develop new feature')

    # Test without title
    response_no_title = client.post('/api/suggest', json={})
    assert response_no_title.status_code == 400
    assert response_no_title.get_json()['error'] == 'Title is required for suggestions'

    # Test ai_service raising an exception (ValueError specifically)
    with patch('ai_service.get_ai_suggestions', side_effect=ValueError("API key missing")) as mock_ai_service_error:
        response_ai_error = client.post('/api/suggest', json={'title': 'Test AI error'})
        assert response_ai_error.status_code == 500
        assert response_ai_error.get_json()['error'] == 'API key missing'
        mock_ai_service_error.assert_called_once_with('Test AI error')

    # Test ai_service raising a generic exception
    with patch('ai_service.get_ai_suggestions', side_effect=Exception("Unexpected error")) as mock_ai_service_generic_error:
        response_generic_error = client.post('/api/suggest', json={'title': 'Test generic error'})
        assert response_generic_error.status_code == 500
        assert response_generic_error.get_json()['error'] == 'Failed to get AI suggestions due to an internal error.'
        mock_ai_service_generic_error.assert_called_once_with('Test generic error')

def test_suggest_api_fallback(client):
    """Test the POST /api/suggest endpoint returns fallback and flag on ai_service failure."""
    # Simulate ai_service.get_ai_suggestions raising an exception,
    # which should trigger the rule-based fallback inside ai_service.
    # We'll mock ai_service.get_ai_suggestions to return a specific fallback dict
    # that we expect after the changes in ai_service.py.
    mock_fallback_response = {"priority": "Low", "label": "Shopping", "fallback": True}

    with patch('ai_service.get_ai_suggestions', side_effect=Exception("Gemini API error")) as mock_ai_service_fail:
        response = client.post('/api/suggest', json={'title': 'Buy groceries for the week'})
        assert response.status_code == 200
        assert response.get_json() == mock_fallback_response
        mock_ai_service_fail.assert_called_once_with('Buy groceries for the week')

    # Test another keyword for fallback
    mock_fallback_response_work = {"priority": "Medium", "label": "Work", "fallback": True}
    with patch('ai_service.get_ai_suggestions', side_effect=Exception("Gemini API error")) as mock_ai_service_fail_work:
        response_work = client.post('/api/suggest', json={'title': 'Prepare monthly report'})
        assert response_work.status_code == 200
        assert response_work.get_json() == mock_fallback_response_work
        mock_ai_service_fail_work.assert_called_once_with('Prepare monthly report')

    # Test default fallback
    mock_fallback_response_default = {"priority": "Low", "label": "Other", "fallback": True}
    with patch('ai_service.get_ai_suggestions', side_effect=Exception("Gemini API error")) as mock_ai_service_fail_default:
        response_default = client.post('/api/suggest', json={'title': 'Random task no keywords'})
        assert response_default.status_code == 200
        assert response_default.get_json() == mock_fallback_response_default
        mock_ai_service_fail_default.assert_called_once_with('Random task no keywords')

# Test for filtering tasks by priority
def test_get_tasks_filter_by_priority(client):
    with app.app_context():
        # Add some test tasks
        db.session.add(Task(title="High Priority Task 1", priority="High"))
        db.session.add(Task(title="Medium Priority Task", priority="Medium"))
        db.session.add(Task(title="High Priority Task 2", priority="High"))
        db.session.add(Task(title="Low Priority Task", priority="Low"))
        db.session.commit()

        # Test filtering by High priority
        response = client.get('/api/tasks?priority=High')
        assert response.status_code == 200
        tasks = response.get_json()
        assert len(tasks) == 2
        assert all(task['priority'] == 'High' for task in tasks)
        assert tasks[0]['title'] == 'High Priority Task 1'
        assert tasks[1]['title'] == 'High Priority Task 2'

        # Test no priority filter (should return all tasks, default sort is by created_at desc)
        response_all = client.get('/api/tasks')
        assert response_all.status_code == 200
        all_tasks = response_all.get_json()
        assert len(all_tasks) == 4
        # Since default sort is created_at desc, the order should be:
        # Low, High2, Medium, High1
        assert all_tasks[0]['title'] == 'Low Priority Task' # Latest created
        assert all_tasks[1]['title'] == 'High Priority Task 2'
        assert all_tasks[2]['title'] == 'Medium Priority Task'
        assert all_tasks[3]['title'] == 'High Priority Task 1'

        # Test filtering by a non-existent priority
        response_none = client.get('/api/tasks?priority=NonExistent')
        assert response_none.status_code == 200
        none_tasks = response_none.get_json()
        assert len(none_tasks) == 0

        # Test filtering by Medium priority (should return 1)
        response_medium = client.get('/api/tasks?priority=Medium')
        assert response_medium.status_code == 200
        medium_tasks = response_medium.get_json()
        assert len(medium_tasks) == 1
        assert medium_tasks[0]['title'] == 'Medium Priority Task'
        assert medium_tasks[0]['priority'] == 'Medium'
