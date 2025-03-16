# olx_api/users.py
from olx_api.base import OLXBase
import requests


class Users(OLXBase):

    def __init__(self, token):
        """
        Initializes the Users API wrapper.

        :param token: A valid Bearer token for authentication.
        """
        super().__init__(token)
        self.token = token

    def get_active_listings(self, username, page=1):
        """
        Retrieves active listings for a given username.

        GET /users/:username/listings

        :param username: The username for which to retrieve listings.
        :param page: Page number (default is 1).
        :return: JSON response from the API.
        """
        url = f"{self.BASE_URL}/users/{username}/listings"
        params = {"page": page}
        response = requests.get(url, headers=self._get_headers(), params=params)
        data = self._handle_response(response)
        return data

    def get_finished_listings(self, user_id, page=1):
        """
        Retrieves finished listings for a given user ID.

        GET /users/:id/listings/finished

        :param user_id: The user ID.
        :param page: Page number.
        :return: JSON response from the API.
        """
        url = f"{self.BASE_URL}/users/{user_id}/listings/finished"
        params = {"page": page}
        response = requests.get(url, headers=self._get_headers(), params=params)
        data = self._handle_response(response)
        return data

    def get_inactive_listings(self, user_id, page=1):
        """
        Retrieves inactive listings for a given user ID.

        GET /users/:id/listings/inactive

        :param user_id: The user ID.
        :param page: Page number.
        :return: JSON response from the API.
        """
        url = f"{self.BASE_URL}/users/{user_id}/listings/inactive"
        params = {"page": page}
        response = requests.get(url, headers=self._get_headers(), params=params)
        data = self._handle_response(response)
        return data

    def get_expired_listings(self, user_id, page=1):
        """
        Retrieves expired listings for a given user ID.

        GET /users/:id/listings/expired

        :param user_id: The user ID.
        :param page: Page number.
        :return: JSON response from the API.
        """
        url = f"{self.BASE_URL}/users/{user_id}/listings/expired"
        params = {"page": page}
        response = requests.get(url, headers=self._get_headers(), params=params)
        data = self._handle_response(response)
        return data

    def get_hidden_listings(self, user_id, page=1):
        """
        Retrieves hidden listings for a given user ID.

        GET /users/:id/listings/hidden

        :param user_id: The user ID.
        :param page: Page number.
        :return: JSON response from the API.
        """
        url = f"{self.BASE_URL}/users/{user_id}/listings/hidden"
        params = {"page": page}
        response = requests.get(url, headers=self._get_headers(), params=params)
        data = self._handle_response(response)
        return data
