from django.test import TestCase, Client

class QnaBotAPITests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_wrong_username_or_password(self):
        """
        Tests the case where required files are missing in the request.
        """
        
        response = self.client.post(
            "/api/tokens/login",
            {
                "username": "newton",
                "password": "12345"
            },
        )
        self.assertEqual(response.status_code, 401)  # Check for Bad Request (401)
        self.assertEqual(response.data['error'], "Username or password is wrong")