# olx_api/listings.py
import os
from olx_api.base import OLXBase
import requests


class Listings(OLXBase):
    """
    A Python wrapper for the OLX API's listings endpoints.

    Example usage:

        from olx_api.listings import Items
        items_api = Items(token="your_valid_token")

        # Get a listing by ID
        listing = items_api.get_listing(40)
        print(listing)

        # Create a new listing (saved as DRAFT)
        new_listing = items_api.create_listing(
            title="audi a3",
            short_description="Audi a3",
            description="Detailed description of the Audi a3",
            country_id="BA",     # Example country id
            city_id="123",       # Example city id
            price=11990,
            available=False,
            listing_type="sell",
            state="used"
        )
        print(new_listing)

        # Update a listing
        updated_listing = items_api.update_listing(40, title="audi a3 updated", price=11990)
        print(updated_listing)

        # Publish the listing
        publish_response = items_api.publish_listing(40)
        print(publish_response)
    """

    def __init__(self, token):
        """
        Initializes the Items API wrapper.

        :param token: A valid Bearer token for OLX API authentication.
        """
        super().__init__(token)

    def get_listing(self, listing_id):
        """
        Retrieves a single listing by its ID.

        GET /listings/:id

        :param listing_id: The ID of the listing.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def create_listing(self, title, short_description=None, description=None, country_id=None,
                       city_id=None, price=None, available=None, listing_type=None,
                       state=None, brand_id=None, model_id=None, sku_number=None, attributes=None):
        """
        Creates a new listing. The new listing is saved with a DRAFT status.

        POST /listings

        :param title: Listing title.
        :param short_description: Short description of the listing.
        :param description: Detailed description.
        :param country_id: Country ID (see Location resources).
        :param city_id: City ID (see Location resources).
        :param price: Price of the listing.
        :param available: Boolean indicating availability.
        :param listing_type: "sell", "buy", or "rent".
        :param state: "new" or "used".
        :param brand_id: Brand ID (check Categories for references).
        :param model_id: Model ID.
        :param sku_number: Internal SKU number.
        :param attributes: A list of attribute dicts.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings"
        payload = {"title": title}
        if short_description is not None:
            payload["short_description"] = short_description
        if description is not None:
            payload["description"] = description
        if country_id is not None:
            payload["country_id"] = country_id
        if city_id is not None:
            payload["city_id"] = city_id
        if price is not None:
            payload["price"] = price
        if available is not None:
            payload["available"] = available
        if listing_type is not None:
            payload["listing_type"] = listing_type
        if state is not None:
            payload["state"] = state
        if brand_id is not None:
            payload["brand_id"] = brand_id
        if model_id is not None:
            payload["model_id"] = model_id
        if sku_number is not None:
            payload["sku_number"] = sku_number
        if attributes is not None:
            payload["attributes"] = attributes

        response = requests.post(url, json=payload, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def update_listing(self, listing_id, **kwargs):
        """
        Updates a listing with provided keyword arguments.

        PUT /listings/:id

        :param listing_id: The ID of the listing.
        :param kwargs: Fields to update (e.g., title, description, price).
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}"
        response = requests.put(url, json=kwargs, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def publish_listing(self, listing_id):
        """
        Publishes a listing (activating it).

        POST /listings/:id/publish

        :param listing_id: The ID of the listing.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/publish"
        response = requests.post(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def delete_listing(self, listing_id):
        """
        Deletes a listing.

        DELETE /listings/:id

        :param listing_id: The ID of the listing.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}"
        response = requests.delete(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_refresh_limits(self):
        """
        Retrieves the listing refresh limits.

        GET /listing/refresh/limits

        :return: The JSON response with free_limit, free_count, paid_count, and listing_count.
        """
        url = f"{self.BASE_URL}/listing/refresh/limits"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_listing_limits(self):
        """
        Retrieves the overall listing limits.

        GET /listing-limits

        :return: The JSON response with limits for various categories.
        """
        url = f"{self.BASE_URL}/listing-limits"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def refresh_listing(self, listing_id):
        """
        Refreshes a listing to boost its search ranking.

        PUT /listings/:id/refresh

        :param listing_id: The ID of the listing.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/refresh"
        response = requests.put(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def image_upload(self, listing_id, image_paths):
        """
        Uploads images for a listing by reading image files and sending them as multipart form data.

        POST /listings/:id/image-upload

        The API expects the "images" attribute to be an array of image files.

        :param listing_id: The ID of the listing.
        :param image_paths: A list (or a single string) of file paths for the images to upload.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/image-upload"

        # Ensure image_paths is a list
        if isinstance(image_paths, str):
            image_paths = [image_paths]

        # Build a list of file tuples for the "images" field.
        # Each tuple is in the form: (field_name, (filename, file_object, mime_type))
        files = []
        for path in image_paths:
            try:
                f = open(path, "rb")
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {path}")
            # Adjust MIME type as needed (e.g., 'image/png' for PNG images)
            files.append(('images[]', (os.path.basename(path), f, 'image/jpeg')))

        try:
            # Pass multipart=True so _get_headers does not set a conflicting Content-Type.
            response = requests.post(url, files=files, headers=self._get_headers(multipart=True))
        finally:
            # Ensure all opened files are closed.
            for _, file_tuple in files:
                file_tuple[1].close()

        data = self._handle_response(response)
        return data

    def image_delete(self, listing_id, image_id):
        """
        Deletes an image from a listing.

        POST /listings/:id/image-delete

        :param listing_id: The ID of the listing.
        :param image_id: The ID of the image to delete.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/image-delete"
        payload = {"imageId": image_id}
        response = requests.post(url, json=payload, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def set_main_image(self, listing_id, image_id):
        """
        Sets an image as the main image for a listing.

        PUT /listings/:id/image-main

        :param listing_id: The ID of the listing.
        :param image_id: The ID of the image to set as main.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/image-main"
        payload = {"imageId": image_id}
        response = requests.put(url, json=payload, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def finish_listing(self, listing_id):
        """
        Finishes a listing.

        POST /listings/:id/finish

        :param listing_id: The ID of the listing.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/finish"
        response = requests.post(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def hide_listing(self, listing_id):
        """
        Hides a listing so that it does not show up in searches.

        POST /listings/:id/hide

        :param listing_id: The ID of the listing.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/hide"
        response = requests.post(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def unhide_listing(self, listing_id):
        """
        Unhides a listing.

        POST /listings/:id/unhide

        :param listing_id: The ID of the listing.
        :return: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/unhide"
        response = requests.post(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data
