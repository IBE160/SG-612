import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, Task

class TaskModelCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_task_model(self):
        with app.app_context():
            task = Task(title='Test Task')
            db.session.add(task)
            db.session.commit()
            self.assertEqual(task.title, 'Test Task')
            self.assertEqual(task.is_done, False)
            self.assertEqual(task.priority, 'Medium')

if __name__ == '__main__':
    unittest.main()
