import unittest
from unittest.mock import patch
from main import app, db
from models import User
from utils import hash  # Import the hashing utility

class TestMain(unittest.TestCase):
    def setUp(self):
        """Setup a test client and test database."""
        self.app = app.test_client()
        self.app.testing = True

        # Mock database setup
        with app.app_context():
            db.create_all()
            # Add a mock user for testing, ensuring the passkey is hashed
            self.user = User(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                passkey=hash.hashPasskey("testpass"),  # Save hashed password
                display_name="TestUser",
            )
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        """Clean up after tests."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_user(self):
        """Test the /api/user/get/<email> endpoint."""
        data = {
            "passkey": hash.hashPasskey("testpass"),  # Hash the test passkey
        }
        response = self.app.get(
            "/api/user/get/test@example.com",
            data=data,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.get_json())

    def test_update_user(self):
        """Test the /api/user/update/<email> endpoint."""
        data = {
            "passkey": hash.hashPasskey("testpass"),  # Hash the test passkey
            "newDisplayName": "UpdatedName",
        }
        response = self.app.patch(
            "/api/user/update/test@example.com",
            data=data,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["user"]["display_name"], "UpdatedName"
        )

    def test_delete_user(self):
        """Test the /api/user/delete/<email> endpoint."""
        data = {
            "passkey": hash.hashPasskey("testpass"),  # Hash the test passkey
        }
        response = self.app.delete(
            "/api/user/delete/test@example.com",
            data=data,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "User Deleted"})

if __name__ == "__main__":
    unittest.main()
