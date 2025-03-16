import unittest
from unittest.mock import patch, Mock
from olx_api.sponsored import Sponsored

class TestSponsoredAPI(unittest.TestCase):
    def setUp(self):
        self.token = "dummy_token"
        self.api = Sponsored(token=self.token)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        self.listing_id = 40

    @patch('olx_api.sponsored.requests.post')
    def test_sponsor_listing(self, mock_post):
        fake_response = {
            "message": "Listing sponsored successfully",
            "status": "sponsored"
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_post.return_value = mock_response

        sponsor_type = 1
        days = 5
        refresh_every = 3
        locations = ["homepage"]

        result = self.api.sponsor_listing(self.listing_id, sponsor_type, days, refresh_every, locations)
        self.assertEqual(result, fake_response)
        mock_post.assert_called_once_with(
            f"https://api.olx.ba/listings/{self.listing_id}/sponsore",
            json={
                "type": sponsor_type,
                "days": days,
                "refresh_every": refresh_every,
                "locations": locations
            },
            headers=self.headers
        )

    @patch('olx_api.sponsored.requests.get')
    def test_get_sponsoring_price(self, mock_get):
        fake_response = {
            "search": 50,
            "refresh": 100,
            "locations": 40,
            "extras": 0,
            "total": 190
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        sponsor_type = 1
        days = 5
        refresh_every = 3
        locations = ["homepage"]
        # We encode the list as a comma-separated string for query parameters
        expected_params = {
            "type": sponsor_type,
            "days": days,
            "refresh_every": refresh_every,
            "locations": "homepage"
        }

        result = self.api.get_sponsoring_price(self.listing_id, sponsor_type, days, refresh_every, locations)
        self.assertEqual(result, fake_response)
        mock_get.assert_called_once_with(
            f"https://api.olx.ba/listings/{self.listing_id}/sponsore/price",
            headers=self.headers,
            params=expected_params
        )

    @patch('olx_api.sponsored.requests.post')
    def test_discount_listing(self, mock_post):
        fake_response = {"message": "Discount set successfully"}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_post.return_value = mock_response

        price = 100.0
        days = 5

        result = self.api.discount_listing(self.listing_id, price, days)
        self.assertEqual(result, fake_response)
        mock_post.assert_called_once_with(
            f"https://api.olx.ba/listings/{self.listing_id}/discount",
            json={"price": price, "days": days},
            headers=self.headers
        )

    @patch('olx_api.sponsored.requests.post')
    def test_finish_discount(self, mock_post):
        fake_response = {"message": "Discount finished successfully"}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_post.return_value = mock_response

        result = self.api.finish_discount(self.listing_id)
        self.assertEqual(result, fake_response)
        mock_post.assert_called_once_with(
            f"https://api.olx.ba/listings/{self.listing_id}/discount/finish",
            headers=self.headers
        )


if __name__ == "__main__":
    unittest.main()
