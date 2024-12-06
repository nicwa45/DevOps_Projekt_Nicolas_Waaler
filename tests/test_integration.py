import unittest
import requests

API_BASE_URL = "https://api.opendota.com/api"

class TestAPI(unittest.TestCase):
    def test_api_connection(self):
        """Test if the API is reachable"""
        response = requests.get(f"{API_BASE_URL}/publicMatches")
        self.assertEqual(response.status_code, 200, "API is not reachable")

    def test_api_response_format(self):
        """Test if the API response has the expected format"""
        response = requests.get(f"{API_BASE_URL}/publicMatches")
        data = response.json()
        self.assertIsInstance(data, list, "API response is not a list")
        if data:
            self.assertIn("match_id", data[0], "Response does not contain 'match_id'")
            self.assertIn("duration", data[0], "Response does not contain 'duration'")

if __name__ == "__main__":
    unittest.main()
