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

    def test_upload_pdf_no_file(self):
        """Vérifie qu'un upload sans fichier renvoie une erreur 400"""
        response = self.client.post("/api/upload-pdf")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])

    def test_upload_pdf_invalid_extension(self):
        """Vérifie qu'un fichier non PDF est refusé"""
        import io
        data = {"file": (io.BytesIO(b"fake txt content"), "test.txt")}
        response = self.client.post("/api/upload-pdf", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 400)
        res = response.get_json()
        self.assertFalse(res["success"])


if __name__ == "__main__":
    unittest.main()
