import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path to import api_client
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import GuanabaraAPI

class TestGuanabaraAPI(unittest.TestCase):
    def setUp(self):
        self.api = GuanabaraAPI()

    @patch('api_client.requests.Session.post')
    def test_get_trips_success(self, mock_post):
        # Configure the mock to return a response with an OK status code
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'trips': []}
        mock_post.return_value = mock_response

        # Call the method
        result = self.api.get_trips("Origin", "Destination", "2026-03-01")

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result, {'trips': []})
        mock_post.assert_called_once()
        
        # Check if payload contains correct date
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['departureDate'], "2026-03-01T00:00:00.000Z")

    @patch('api_client.requests.Session.post')
    def test_get_trips_failure(self, mock_post):
        # Configure the mock to return a 404 status
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_post.return_value = mock_response

        # Call the method
        result = self.api.get_trips("Origin", "Destination", "2026-03-01")

        # Assertions
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
