from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
import json


class QnaBotAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_user("testing")
        self.client.force_authenticate(user=user)

    def test_missing_questions_file(self):
        """
        Tests the case where required files are missing in the request.
        """
        response = self.client.post("/api/qna/bot")
        self.assertEqual(response.status_code, 400)  # Check for Bad Request (400)
        self.assertEqual(response.data['error'], "questions file is required")
    
    def test_missing_content_files(self):
        """
        Tests the case where required files are missing in the request.
        """
        
        json_data = {
            "questions": ["What is the purpose of this document?"]
        }

        with open('questions.json', 'w') as f:
            json.dump(json_data, f)  # Create a temporary JSON file for testing
        question_file = SimpleUploadedFile("questions.json", open('questions.json', 'rb').read(), content_type="application/json")

        response = self.client.post(
            "/api/qna/bot",
            {
                "questions": question_file
            },
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "content file is required")
    
    def test_invalid_file_type(self):
        """
        Tests the case where an unsupported file type is uploaded.
        """

        text_content = b"This is some text content"
        text_file = SimpleUploadedFile("invalid.txt", text_content, content_type="text/plain")

        with open('questions.json', 'w') as f:
            json.dump({"questions": ["Invalid test"]}, f)
        question_file = SimpleUploadedFile("questions.json", open('questions.json', 'rb').read(), content_type="application/json")

        response = self.client.post(
            "/api/qna/bot",
            {
                "content": text_file,
                "questions": question_file
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Unsupported file type")
    
    def tearDown(self):
        pass