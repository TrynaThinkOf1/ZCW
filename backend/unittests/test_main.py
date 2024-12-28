import unittest
from flask_jwt_extended import create_access_token

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, db
from models import User, VerificationCodes

class TestMain(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

            # Add a test user
            test_user = User(
                email="test@example.com",
                first_name="Test",
                last_name="User",
                display_name="TestUser",
                passkey="hashed_test_passkey",
            )
            db.session.add(test_user)
            db.session.commit()

            # Store the test user ID for re-fetching
            self.test_user_id = test_user.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def insert_verification_code(self, code):
        with app.app_context():
            verification = VerificationCodes(code=code)
            db.session.add(verification)
            db.session.commit()

    def test_user_registration_and_login(self):
        self.insert_verification_code("test-code")
        response = self.app.post(
            '/api/code/verify/test-code',
            data={
                'passkey': 'test_passkey',
                'email': 'newuser@example.com',
                'firstName': 'New',
                'lastName': 'User',
                'displayName': 'NewUser',
            }
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('token', data)
        self.assertEqual(data['user']['email'], 'newuser@example.com')

    def test_get_user(self):
        with app.app_context():
            user = User.query.get(self.test_user_id)
            token = create_access_token(identity={"id": user.id})

        response = self.app.get(
            '/api/user/get',
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['user']['email'], "test@example.com")

    def test_create_post(self):
        with app.app_context():
            user = User.query.get(self.test_user_id)
            token = create_access_token(identity={"id": user.id})

        response = self.app.post(
            '/api/post/create',
            headers={"Authorization": f"Bearer {token}"},
            data={"markdownContent": "This is a test post"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('post', data)
        self.assertEqual(data['post']['markdown_content'], "This is a test post")

    def test_update_user(self):
        with app.app_context():
            user = User.query.get(self.test_user_id)
            token = create_access_token(identity={"id": user.id})

        response = self.app.patch(
            '/api/user/update',
            headers={"Authorization": f"Bearer {token}"},
            data={"newDisplayName": "UpdatedUser"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['user']['display_name'], "UpdatedUser")

    def test_delete_user(self):
        with app.app_context():
            user = User.query.get(self.test_user_id)

        response = self.app.delete(
            f'/api/user/delete/{user.email}',
            data={"passkey": "hashed_test_passkey"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], "User Deleted")

if __name__ == "__main__":
    unittest.main()
