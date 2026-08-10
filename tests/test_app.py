import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        """Vérifie que la route /health renvoie 200 OK et {"status": "ok"}"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_index_page(self):
        """Vérifie que la page d'accueil / charge correctement"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Solife", response.data)


if __name__ == "__main__":
    unittest.main()
