import unittest
from unittest.mock import patch, Mock
from olx_api.listings import Listings

class TestItemsAPI(unittest.TestCase):
    def setUp(self):
        # Use a dummy token for testing
        self.token = "dummy_token"
        self.api = Listings(token=self.token)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    @patch('olx_api.listings.requests.get')
    def test_get_listing(self, mock_get):
        # Setup a fake listing response
        fake_listing = {
            "id": 40,
            "type": "single",
            "title": "audi a3",
            "slug": "audi-a3",
            "short_description": "Audi a3",
            "additional": {"description": "opis oglasa"},
            "price": 11990,
            "display_price": "11.990 KM",
            # other fields...
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_listing
        mock_get.return_value = mock_response

        listing = self.api.get_listing(40)
        self.assertEqual(listing, fake_listing)
        mock_get.assert_called_once_with(
            "https://api.olx.ba/listings/40", headers=self.headers
        )

    @patch('olx_api.listings.requests.post')
    def test_create_listing(self, mock_post):
        # Setup a fake response for listing creation
        fake_response_data = {
            "id": 40,
            "type": "single",
            "title": "audi a3",
            "slug": "audi-a3",
            "short_description": "Audi a3",
            # other fields...
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response_data
        mock_post.return_value = mock_response

        new_listing = self.api.create_listing(
            title="audi a3",
            short_description="Audi a3",
            description="Detailed description of Audi a3",
            country_id="BA",
            city_id="123",
            price=11990,
            available=False,
            listing_type="sell",
            state="used"
        )
        self.assertEqual(new_listing, fake_response_data)
        mock_post.assert_called_once_with(
            "https://api.olx.ba/listings",
            json={
                "title": "audi a3",
                "short_description": "Audi a3",
                "description": "Detailed description of Audi a3",
                "country_id": "BA",
                "city_id": "123",
                "price": 11990,
                "available": False,
                "listing_type": "sell",
                "state": "used"
            },
            headers=self.headers
        )

    @patch('olx_api.listings.requests.put')
    def test_update_listing(self, mock_put):
        # Setup a fake response for updating a listing
        updated_data = {
            "id": 40,
            "title": "audi a3 updated",
            "price": 11990
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = updated_data
        mock_put.return_value = mock_response

        result = self.api.update_listing(40, title="audi a3 updated", price=11990)
        self.assertEqual(result, updated_data)
        mock_put.assert_called_once_with(
            "https://api.olx.ba/listings/40",
            json={"title": "audi a3 updated", "price": 11990},
            headers=self.headers
        )

    @patch('olx_api.listings.requests.post')
    def test_publish_listing(self, mock_post):
        # Setup fake response for publishing a listing
        fake_response = {"message": "Oglas je uspjesno objavljen", "status": "active"}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_post.return_value = mock_response

        result = self.api.publish_listing(40)
        self.assertEqual(result, fake_response)
        mock_post.assert_called_once_with(
            "https://api.olx.ba/listings/40/publish", headers=self.headers
        )

    @patch('olx_api.listings.requests.delete')
    def test_delete_listing(self, mock_delete):
        # Setup fake response for deleting a listing
        fake_response = {"message": "Uspješno ste izbrisali oglas"}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_delete.return_value = mock_response

        result = self.api.delete_listing(40)
        self.assertEqual(result, fake_response)
        mock_delete.assert_called_once_with(
            "https://api.olx.ba/listings/40", headers=self.headers
        )

    @patch('olx_api.listings.requests.get')
    def test_get_refresh_limits(self, mock_get):
        # Setup fake response for refresh limits
        fake_limits = {"free_limit": 750, "free_count": 0, "paid_count": 0, "listing_count": 3}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_limits
        mock_get.return_value = mock_response

        result = self.api.get_refresh_limits()
        self.assertEqual(result, fake_limits)
        mock_get.assert_called_once_with(
            "https://api.olx.ba/listing/refresh/limits", headers=self.headers
        )

    @patch('olx_api.listings.requests.get')
    def test_get_listing_limits(self, mock_get):
        fake_limits = {
            "data": {
                "cars": {"limit": 0, "listings": 0},
                "real-estate": {"limit": 0, "listings": 1},
                "other": {"limit": 0, "listings": 8},
            }
        }
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_limits
        mock_get.return_value = mock_response

        result = self.api.get_listing_limits()
        self.assertEqual(result, fake_limits)
        mock_get.assert_called_once_with(
            "https://api.olx.ba/listing-limits", headers=self.headers
        )

    @patch('olx_api.listings.requests.put')
    def test_refresh_listing(self, mock_put):
        fake_response = {"message": "Artikal je uspjesno obnovljen."}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_put.return_value = mock_response

        result = self.api.refresh_listing(40)
        self.assertEqual(result, fake_response)
        mock_put.assert_called_once_with(
            "https://api.olx.ba/listings/40/refresh", headers=self.headers
        )

    @patch('olx_api.listings.requests.post')
    def test_image_upload(self, mock_post):
        fake_response = [
            {
                "id": 44,
                "name": "img-1679924109-fd89f8c193d2.jpeg",
                "main": False,
                "order": 0,
                "sizes": {
                    "sm": "listings/40/sm/img-1679924109-fd89f8c193d2.jpeg",
                    "lg": "listings/40/lg/img-1679924109-fd89f8c193d2.jpeg"
                },
                "created_at": "2023-03-27T13:35:11.000000Z"
            }
        ]
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_post.return_value = mock_response

        images = ["image1.jpg", "image2.jpg"]  # Example image representations
        result = self.api.image_upload(40, images)
        self.assertEqual(result, fake_response)
        mock_post.assert_called_once_with(
            "https://api.olx.ba/listings/40/image-upload",
            json={"images": images},
            headers=self.headers
        )

    @patch('olx_api.listings.requests.post')
    def test_image_delete(self, mock_post):
        fake_response = {"success": True}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_post.return_value = mock_response

        result = self.api.image_delete(40, 1)
        self.assertEqual(result, fake_response)
        mock_post.assert_called_once_with(
            "https://api.olx.ba/listings/40/image-delete",
            json={"imageId": 1},
            headers=self.headers
        )

    @patch('olx_api.listings.requests.put')
    def test_set_main_image(self, mock_put):
        fake_response = {"success": True}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_put.return_value = mock_response

        result = self.api.set_main_image(40, 1)
        self.assertEqual(result, fake_response)
        mock_put.assert_called_once_with(
            "https://api.olx.ba/listings/40/image-main",
            json={"imageId": 1},
            headers=self.headers
        )

    @patch('olx_api.listings.requests.post')
    def test_finish_listing(self, mock_post):
        fake_response = {"message": "Listing finished"}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_post.return_value = mock_response

        result = self.api.finish_listing(40)
        self.assertEqual(result, fake_response)
        mock_post.assert_called_once_with(
            "https://api.olx.ba/listings/40/finish",
            headers=self.headers
        )

    @patch('olx_api.listings.requests.post')
    def test_hide_listing(self, mock_post):
        fake_response = {"message": "Listing hidden"}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_post.return_value = mock_response

        result = self.api.hide_listing(40)
        self.assertEqual(result, fake_response)
        mock_post.assert_called_once_with(
            "https://api.olx.ba/listings/40/hide",
            headers=self.headers
        )

    @patch('olx_api.listings.requests.post')
    def test_unhide_listing(self, mock_post):
        fake_response = {"message": "Listing unhidden"}
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = fake_response
        mock_post.return_value = mock_response

        result = self.api.unhide_listing(40)
        self.assertEqual(result, fake_response)
        mock_post.assert_called_once_with(
            "https://api.olx.ba/listings/40/unhide",
            headers=self.headers
        )

if __name__ == "__main__":
    unittest.main()
