import unittest
from unittest.mock import patch, Mock
from olx_api.users import Users

class TestUsersAPI(unittest.TestCase):
    def setUp(self):
        # Set up a dummy token and the Users API wrapper instance
        self.token = "dummy_token"
        self.api = Users(token=self.token)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    @patch('olx_api.users.requests.get')
    def test_get_active_listings(self, mock_get):
        fake_response = {
            "data": [
                {
                    "id": 50,
                    "title": "audi a3",
                    "price": 15.5,
                    "display_price": "15,50 KM",
                }
            ],
            "meta": {
                "total": 1,
                "last_page": 1,
                "current_page": 1,
                "per_page": 20,
                "selected_category": 0
            }
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        username = "testuser"
        result = self.api.get_active_listings(username)
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            f"https://api.olx.ba/users/{username}/listings",
            headers=self.headers,
            params={"page": 1}
        )

    @patch('olx_api.users.requests.get')
    def test_get_finished_listings(self, mock_get):
        fake_response = {
            "data": [
                {
                    "id": 50,
                    "title": "audi a3",
                    "price": 15.5,
                    "display_price": "15,50 KM",
                }
            ],
            "meta": {
                "total": 1,
                "last_page": 1,
                "current_page": 1,
                "per_page": 20,
                "selected_category": 0
            }
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        user_id = 123
        result = self.api.get_finished_listings(user_id)
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            f"https://api.olx.ba/users/{user_id}/listings/finished",
            headers=self.headers,
            params={"page": 1}
        )

    @patch('olx_api.users.requests.get')
    def test_get_inactive_listings(self, mock_get):
        fake_response = {
            "data": [
                {
                    "id": 50,
                    "title": "audi a3",
                    "price": 15.5,
                    "display_price": "15,50 KM",
                }
            ],
            "meta": {
                "total": 1,
                "last_page": 1,
                "current_page": 1,
                "per_page": 20,
                "selected_category": 0
            }
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        user_id = 123
        result = self.api.get_inactive_listings(user_id)
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            f"https://api.olx.ba/users/{user_id}/listings/inactive",
            headers=self.headers,
            params={"page": 1}
        )

    @patch('olx_api.users.requests.get')
    def test_get_expired_listings(self, mock_get):
        fake_response = {
            "data": [
                {
                    "id": 50,
                    "title": "audi a3",
                    "price": 15.5,
                    "display_price": "15,50 KM",
                }
            ],
            "meta": {
                "total": 1,
                "last_page": 1,
                "current_page": 1,
                "per_page": 20,
                "selected_category": 0
            }
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        user_id = 123
        result = self.api.get_expired_listings(user_id)
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            f"https://api.olx.ba/users/{user_id}/listings/expired",
            headers=self.headers,
            params={"page": 1}
        )

    @patch('olx_api.users.requests.get')
    def test_get_hidden_listings(self, mock_get):
        fake_response = {
            "data": [
                {
                    "id": 50,
                    "title": "audi a3",
                    "price": 15.5,
                    "display_price": "15,50 KM",
                }
            ],
            "meta": {
                "total": 1,
                "last_page": 1,
                "current_page": 1,
                "per_page": 20,
                "selected_category": 0
            }
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        user_id = 123
        result = self.api.get_hidden_listings(user_id)
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            f"https://api.olx.ba/users/{user_id}/listings/hidden",
            headers=self.headers,
            params={"page": 1}
        )

if __name__ == "__main__":
    unittest.main()
