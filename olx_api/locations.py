# olx_api/locations.py
from olx_api.base import OLXBase
import requests


class Locations(OLXBase):
    """
    Locations API Wrapper

    This class provides methods to interact with location-related endpoints of the OLX API.
    It inherits from OLXBase, which sets up the base URL and any common configuration.

    The available methods include:
      - get_cities: Retrieve a list of all cities.
      - get_countries: Retrieve a list of all countries.
      - get_city: Get detailed information about a specific city by its ID.
      - get_country_states: Retrieve a list of all country states.
      - get_canton_cities: Retrieve cities belonging to a specific canton.

    Usage Example:
        >>> locations = Locations(token="your_valid_token")
        >>> all_cities = locations.get_cities()
        >>> all_countries = locations.get_countries()
        >>> city_details = locations.get_city(1)
        >>> states = locations.get_country_states()
        >>> canton_cities = locations.get_canton_cities(canton_id=9)
    """
    def __init__(self, token):
        """
        Initializes the Locations API wrapper.

        :param token: A valid Bearer token for authentication.
        """
        super().__init__(token)

    def get_cities(self):
        """
        Retrieves a list of all cities.

        GET /cities
        """
        url = f"{self.BASE_URL}/cities"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_countries(self):
        """
        Retrieves a list of all countries.

        GET /countries
        """
        url = f"{self.BASE_URL}/countries"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_city(self, city_id):
        """
        Retrieves details for a single city by its ID.

        GET /cities/:id
        """
        url = f"{self.BASE_URL}/cities/{city_id}"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_country_states(self):
        """
        Retrieves a list of all country states.

        GET /country-states
        """
        url = f"{self.BASE_URL}/country-states"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_canton_cities(self, canton_id):
        """
        Retrieves a list of cities for a given canton.

        GET /cantons/:id/cities
        """
        url = f"{self.BASE_URL}/cantons/{canton_id}/cities"
        response = requests.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data
