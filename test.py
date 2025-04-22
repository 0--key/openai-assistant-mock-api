import unittest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is saved in main.py

client = TestClient(app)

class TestCreateAssistant(unittest.TestCase):

    def test_create_assistant_with_valid_headers(self):
        request_data = {
            "instructions": "You are a personal math tutor.",
            "name": "Math Tutor",
            "description": "The description of the assistant.",
            "tools": [{"type": "code_interpreter"}],
            "model": "gpt-4-turbo",
            "temperature": 0.8,
            "top_p": 1.0
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-the-mock-key-for-openai-simulation-on-localhost",
            "OpenAI-Beta": "assistants=v2"
        }

        response = client.post("/v1/assistants", json=request_data, headers=headers)

        expected_response = {
            "id": "asst_abc123",
            "object": "assistant",
            "created_at": response.json()["created_at"],
            "name": "Math Tutor",
            "description": "The description of the assistant.",
            "model": "gpt-4-turbo",
            "instructions": "You are a personal math tutor.",
            "tools": [
                {"type": "code_interpreter"}
            ],
            "metadata": {},
            "top_p": 1.0,
            "temperature": 0.8,
            "response_format": "auto"
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), expected_response)

    def test_create_assistant_with_invalid_authorization(self):
        request_data = {
            "instructions": "You are a personal math tutor.",
            "name": "Math Tutor",
            "description": "The description of the assistant.",
            "tools": [{"type": "code_interpreter"}],
            "model": "gpt-4-turbo",
            "temperature": 0.8,
            "top_p": 1.0
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer invalid_key",
            "OpenAI-Beta": "assistants=v2"
        }

        response = client.post("/v1/assistants", json=request_data, headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(response.json(), {"detail": "Unauthorized"})

    # def test_create_assistant_with_invalid_content_type(self):
    #     request_data = {
    #         "instructions": "You are a personal math tutor.",
    #         "name": "Math Tutor",
    #         "description": "The description of the assistant.",
    #         "tools": [{"type": "code_interpreter"}],
    #         "model": "gpt-4-turbo",
    #         "temperature": 0.8,
    #         "top_p": 1.0
    #     }

    #     headers = {
    #         "Content-Type": "text/plain",  # Invalid Content-Type
    #         "Authorization": "Bearer sk-the-mock-key-for-openai-simulation-on-localhost",
    #         "OpenAI-Beta": "assistants=v2"
    #     }

    #     response = client.post("/v1/assistants", json=request_data, headers=headers)
    #     self.assertEqual(response.status_code, 415)
    #     self.assertDictEqual(response.json(), {"detail": "Unsupported Media Type"})

    def test_create_assistant_with_invalid_openai_beta(self):
        request_data = {
            "instructions": "You are a personal math tutor.",
            "name": "Math Tutor",
            "description": "The description of the assistant.",
            "tools": [{"type": "code_interpreter"}],
            "model": "gpt-4-turbo",
            "temperature": 0.8,
            "top_p": 1.0
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-the-mock-key-for-openai-simulation-on-localhost",
            "OpenAI-Beta": "invalid_value"  # Invalid OpenAI-Beta header
        }

        response = client.post("/v1/assistants", json=request_data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {"detail": "Invalid OpenAI-Beta header"})
