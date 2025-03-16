import unittest
from unittest.mock import patch, Mock
from olx_api.locations import Locations

class TestLocationsAPI(unittest.TestCase):
    def setUp(self):
        # Set up a dummy token and an instance of Locations
        self.token = "dummy_token"
        self.api = Locations(token=self.token)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    @patch('olx_api.locations.requests.get')
    def test_get_cities(self, mock_get):
        fake_response = {
            "data": [
                {"id": 1, "name": "Federacija BiH", "code": "FBIH", "cantons": []},
                {"id": 2, "name": "Republika srpska", "code": "RS", "cantons": []},
                {"id": 3, "name": "Brcko Distrikt", "code": "BD", "cantons": []},
            ]
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        result = self.api.get_cities()
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            "https://api.olx.ba/cities", headers=self.headers
        )

    @patch('olx_api.locations.requests.get')
    def test_get_countries(self, mock_get):
        fake_response = {
            "data": [
                {"id": 49, "name": "Bosna i Hercegovina", "code": "BA"}
            ]
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        result = self.api.get_countries()
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            "https://api.olx.ba/countries", headers=self.headers
        )

    @patch('olx_api.locations.requests.get')
    def test_get_city(self, mock_get):
        fake_response = {
            "id": 1,
            "name": "Sarajevo",
            "zip_code": 71000,
            "lat": "43.8519774",
            "lon": "18.3866868",
            "parent_id": None,
            "pop": 10,
            "country_id": 49,
            "canton_id": 9,
            "state_id": 1,
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        city_id = 1
        result = self.api.get_city(city_id)
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            f"https://api.olx.ba/cities/{city_id}",
            headers=self.headers
        )

    @patch('olx_api.locations.requests.get')
    def test_get_country_states(self, mock_get):
        fake_response = {
            "data": [
                {"id": 1, "name": "Federacija BiH", "code": "FBIH", "cantons": []},
                {"id": 2, "name": "Republika srpska", "code": "RS", "cantons": []},
                {"id": 3, "name": "Brcko Distrikt", "code": "BD", "cantons": []},
            ]
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        result = self.api.get_country_states()
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            "https://api.olx.ba/country-states", headers=self.headers
        )

    @patch('olx_api.locations.requests.get')
    def test_get_canton_cities(self, mock_get):
        fake_response = {
            "data": [
                {
                    "id": 133,
                    "name": "Centar",
                    "location": {"lat": "43.8575641", "lon": "18.4149369"},
                    "canton_id": 9
                },
                {
                    "id": 132,
                    "name": "Novi Grad",
                    "location": {"lat": "43.8404514", "lon": "18.324795"},
                    "canton_id": 9
                },
            ]
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        canton_id = 9
        result = self.api.get_canton_cities(canton_id)
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            f"https://api.olx.ba/cantons/{canton_id}/cities",
            headers=self.headers
        )


if __name__ == "__main__":
    unittest.main()