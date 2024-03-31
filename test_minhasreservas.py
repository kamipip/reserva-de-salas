from datetime import datetime
import unittest
from unittest.mock import patch
from main import app

class TestMinhasReservas(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_minhas_reservas_no_user_logged_in(self):
        # Simulate no user logged in
        with self.app as client:
            response = client.get('/minhas-reservas')
            self.assertEqual(response.status_code, 302)  # Redirect code

if __name__ == '__main__':
    unittest.main()
