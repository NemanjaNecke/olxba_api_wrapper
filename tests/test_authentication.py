import unittest
from unittest.mock import patch, Mock

from olx_api.authentication import OLXAuth


class TestOLXAuth(unittest.TestCase):

    @patch('olx_api.authentication.requests.post')
    def test_login_success(self, mock_post):
        # Set up the mock response for a successful login
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "token": "163|1bA8cqxhtoohFDROFAWYPGhkvYApzLpm2ojzD6Tc",
            "user": {
                "id": 1,
                "type": "shop",
                "email": "email@olx.ba",
                "username": "OLX",
                "first_name": "Svijet",
                "last_name": "Kupoprodaje",
            }
        }
        mock_post.return_value = mock_response

        # Instantiate OLXAuth with credentials
        auth = OLXAuth(username="test@olx.ba", password="password", device_name="integration")
        token = auth.login()

        # Assert that the token and user info were set correctly
        self.assertEqual(token, "163|1bA8cqxhtoohFDROFAWYPGhkvYApzLpm2ojzD6Tc")
        self.assertEqual(auth.user["username"], "OLX")

        # Verify that requests.post was called with the expected arguments
        mock_post.assert_called_once_with(
            "https://api.olx.ba/auth/login",
            json={
                "username": "test@olx.ba",
                "password": "password",
                "device_name": "integration"
            },
            headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': 'olx_api/0.1.0'}
        )

    def test_get_authenticated_headers_without_login(self):
        # Instantiate without logging in
        auth = OLXAuth(username="test@olx.ba", password="password")
        # Expect a ValueError when trying to get headers without a token
        with self.assertRaises(ValueError):
            _ = auth.get_authenticated_headers()

    @patch('olx_api.authentication.requests.post')
    def test_get_authenticated_headers_after_login(self, mock_post):
        # Set up the mock response for login
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "token": "token123",
            "user": {"id": 1, "username": "OLX"}
        }
        mock_post.return_value = mock_response

        auth = OLXAuth(username="test@olx.ba", password="password")
        auth.login()
        headers = auth.get_authenticated_headers()
        self.assertEqual(headers, {"Authorization": "Bearer token123"})

    def test_get_headers_with_old_tokens(self):
        # Test the static method that returns legacy authentication headers
        headers = OLXAuth.get_headers_with_old_tokens(client_id="cid", client_token="ctoken")
        expected = {"OLX-CLIENT-ID": "cid", "OLX-CLIENT-TOKEN": "ctoken"}
        self.assertEqual(headers, expected)


if __name__ == "__main__":
    unittest.main()
