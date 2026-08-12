import unittest
import json
import os
import sys

# Ensure project path is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, get_db_connection, init_db

class OnlineFeedbackCollectorTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        self.client = app.test_client()
        init_db()

    def test_01_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Online Feedback", response.data)
        self.assertIn(b"Feedback Form", response.data)

    def test_02_submit_feedback_valid(self):
        payload = {
            "name": "Test User",
            "email": "testuser@example.com",
            "rating": 5,
            "comments": "Automated integration test submission - excellent app!"
        }
        response = self.client.post('/submit-feedback',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn("submitted successfully", data['message'])

    def test_03_submit_feedback_invalid(self):
        payload = {
            "name": "",
            "email": "invalid-email",
            "rating": 6,
            "comments": "Short"
        }
        response = self.client.post('/submit-feedback',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_04_api_feedback(self):
        response = self.client.get('/api/feedback')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['count'], 1)
        self.assertIsInstance(data['feedback'], list)

    def test_05_admin_unauthorized_redirect(self):
        response = self.client.get('/admin-dashboard', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

    def test_06_admin_login_failure(self):
        payload = {"username": "admin", "password": "wrongpassword"}
        response = self.client.post('/login',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_07_admin_login_success_and_dashboard(self):
        payload = {"username": "admin", "password": "admin123"}
        response = self.client.post('/login',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

        # Now test dashboard access with active session client
        dash_response = self.client.get('/admin-dashboard')
        self.assertEqual(dash_response.status_code, 200)
        self.assertIn(b"Analytics & Feedback Management", dash_response.data)
        self.assertIn(b"Total Submissions", dash_response.data)

    def test_08_csv_export(self):
        # First log in
        self.client.post('/login', data=json.dumps({"username": "admin", "password": "admin123"}), content_type='application/json')
        response = self.client.get('/export-csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')
        self.assertIn(b"ID,Name,Email,Rating,Comments,Date Submitted", response.data)

    def test_09_logout(self):
        self.client.post('/login', data=json.dumps({"username": "admin", "password": "admin123"}), content_type='application/json')
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Admin Sign In", response.data)

if __name__ == "__main__":
    unittest.main()
