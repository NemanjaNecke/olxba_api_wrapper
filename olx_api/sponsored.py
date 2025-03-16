# olx_api/sponsored.py
from olx_api.base import OLXBase
import requests


class Sponsored(OLXBase):
    """
    Sponsored API Wrapper

    This class provides methods to interact with the OLX API's sponsorship and discount endpoints.
    It inherits common settings from OLXBase (such as BASE_URL, token handling, and header construction).

    Available methods:
      - sponsor_listing: Sponsor a listing with a specified type, duration, refresh interval, and locations.
      - get_sponsoring_price: Retrieve the pricing details for sponsoring a listing.
      - discount_listing: Set a discount price for a listing.
      - finish_discount: Finish an active discount on a listing.

    Usage Example:
        >>> sponsored = Sponsored(token="your_valid_token")
        >>> # Sponsor a listing:
        >>> response = sponsored.sponsor_listing(
        ...     listing_id=40,
        ...     sponsor_type=1,
        ...     days=5,
        ...     refresh_every=3,
        ...     locations=["homepage"]
        ... )
        >>> print(response)
    """

    def __init__(self, token):
        """
        Initializes the Sponsored API wrapper with a valid Bearer token.

        :param token: A valid token for authentication.
        """
        super().__init__(token)

    def sponsor_listing(self, listing_id, sponsor_type, days, refresh_every, locations):
        """
        Sponsors a listing.

        POST /listings/{id}/sponsore

        :param listing_id: ID of the listing.
        :param sponsor_type: Sponsoring type (0, 1, or 2).
        :param days: Number of days (e.g., 1,2,3,5,7,14,21,30).
        :param refresh_every: Refresh interval in hours (0,3,6,8,24).
        :param locations: List of location strings (e.g., ["homepage"]).
        :return: JSON response.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/sponsore"
        payload = {
            "type": sponsor_type,
            "days": days,
            "refresh_every": refresh_every,
            "locations": locations
        }
        response = requests.post(url, json=payload, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def get_sponsoring_price(self, listing_id, sponsor_type, days, refresh_every, locations):
        """
        Retrieves the sponsoring price for a listing.

        GET /listings/{id}/sponsore/price

        :param listing_id: ID of the listing.
        :param sponsor_type: Sponsoring type (0,1,2).
        :param days: Number of days.
        :param refresh_every: Refresh interval in hours.
        :param locations: List of location strings.
        :return: JSON response with pricing details.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/sponsore/price"
        # Since GET requests typically do not include a JSON body,
        # we pass the parameters as query parameters.
        params = {
            "type": sponsor_type,
            "days": days,
            "refresh_every": refresh_every,
            # You might choose to encode the list as a comma‐separated string
            "locations": ",".join(locations)
        }
        response = requests.get(url, headers=self._get_headers(), params=params)
        data = self._handle_response(response)
        return data

    def discount_listing(self, listing_id, price, days):
        """
        Sets a discount price for a listing.

        POST /listings/{id}/discount

        :param listing_id: ID of the listing.
        :param price: New listing price.
        :param days: Number of days (e.g., 3,7,30).
        :return: JSON response.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/discount"
        payload = {"price": price, "days": days}
        response = requests.post(url, json=payload, headers=self._get_headers())
        data = self._handle_response(response)
        return data

    def finish_discount(self, listing_id):
        """
        Finishes an active listing discount.

        POST /listings/{id}/discount/finish

        :param listing_id: ID of the listing.
        :return: JSON response.
        """
        url = f"{self.BASE_URL}/listings/{listing_id}/discount/finish"
        response = requests.post(url, headers=self._get_headers())
        data = self._handle_response(response)
        return data
